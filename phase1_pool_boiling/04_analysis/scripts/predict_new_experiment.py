"""
predict_new_experiment.py — End-to-end inference wrapper for new ONB experiments.

Given a CSV of new pool-boiling ONB observations (same 12-column schema as
``02_data/processed/onb_dataset.csv``), this script:

  1. Validates the input CSV (columns, units, fluid support).
  2. Runs an *applicability domain* check against the training distribution
     and warns when the new rows are outside it (extrapolation).
  3. Runs the K=10 deep-ensemble PINN to obtain mean prediction +
     epistemic/aleatoric/total uncertainty + 95% credible interval.
  4. Evaluates the 5 classical correlations (Hsu, Davis-Anderson,
     Bergles-Rohsenow, Sato-Matsumura, Basu) on the same rows.
  5. If the input CSV carries ground-truth ``delta_T_wall`` values, computes
     RMSE / MAE / R² / 95% coverage for the PINN and every correlation.
  6. Writes the merged predictions, the metrics table, and a 6-panel parity
     plot under ``04_analysis/experiments/<run-name>/``.

USAGE
-----

    # Minimal: predict only, no ground truth comparison required.
    python 04_analysis/scripts/predict_new_experiment.py \\
        --csv 02_data/raw/experiment/my_experiment.csv \\
        --run-name my_experiment_2026

    # Custom output directory:
    python 04_analysis/scripts/predict_new_experiment.py \\
        --csv path/to/new.csv --run-name run1 --out-dir 04_analysis/external/

INPUT CSV SCHEMA (12 columns, identical to onb_dataset.csv)
-----------------------------------------------------------
    source_paper, figure_ref, surface_id, surface_label, fluid,
    delta_T_wall, delta_T_sub, q_flux, Ra_um, theta_deg, category, notes

- ``fluid`` must be one of: water, R-123, R-134a (case-insensitive; FC-77,
  HFE-7100, FC-72, Novec-649 are NOT supported by CoolProp in this build).
- ``q_flux`` is in W/m^2 (NOT kW/m^2).
- ``Ra_um`` is in micrometres (nano-scale entries: 30 nm => 0.030).
- ``theta_deg`` may be empty when not measured.
- ``delta_T_wall`` is the wall superheat at ONB [K]; leave empty for pure
  prediction-only runs.
- ``delta_T_sub`` is the subcooling [K]; 0 for saturated.
- ``category`` is a coarse stratification tag; new experiments may use any
  string (e.g., ``in_house``). The model treats unknown categories as a
  neutral default via its category embedding.

OUTPUTS
-------
    04_analysis/experiments/<run-name>/
        predictions.csv          # one row per input + 7 PINN cols + 5 corr cols
        metrics.md               # PINN vs 5 correlations (RMSE/MAE/R²/coverage)
        parity_combined.png      # 6-panel parity plot (PINN + 5 correlations)
        applicability_report.md  # extrapolation warnings, per-variable ranges

The script is self-contained — it imports the same inference helpers used by
``analyze_ensemble.py`` and ``correlation_comparator.py`` so the numerical
results are bit-identical to those scripts when run on identical data.
"""
from __future__ import annotations

import argparse
import math
import sys
import warnings
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml

# ---------------------------------------------------------------------------
# Project root and module path bootstrap
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "03_model"))
sys.path.insert(0, str(ROOT / "03_model" / "src"))

from src.training.ensemble import collect_ensemble_predictions  # type: ignore  # noqa: E402

# correlation_comparator exposes load_and_predict(data_csv) which adds 5
# classical-correlation columns to the rows.
sys.path.insert(0, str(ROOT / "04_analysis" / "scripts"))
from correlation_comparator import load_and_predict as load_with_correlations  # type: ignore  # noqa: E402


# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------
DEFAULT_CKPT_DIR = ROOT / "03_model" / "checkpoints" / "ensemble_phaseDbal"
DEFAULT_CONFIG   = ROOT / "03_model" / "configs" / "baseline_phaseDbal.yaml"
DEFAULT_OUT_ROOT = ROOT / "04_analysis" / "experiments"


# ---------------------------------------------------------------------------
# Training-distribution bounds (from § Data + onb_dataset.csv statistics).
# Used purely for the applicability-domain check; predictions still run
# even if a row is out-of-band — a warning is emitted.
# ---------------------------------------------------------------------------
TRAINING_BOUNDS: dict[str, tuple[float, float]] = {
    "delta_T_wall_K":      (0.7,  24.9),   # ΔT_ONB range observed in training
    "delta_T_sub_K":       (0.0,  15.0),   # only PHAN reports sub != 0
    "q_flux_W_m2":         (1e2,  1.434e6),
    "Ra_um":               (0.0004, 10.5),
    "theta_deg":           (0.0,  165.0),
}
SUPPORTED_FLUIDS = {"water", "r-123", "r123", "r-134a", "r134a"}
KNOWN_CATEGORIES = {
    "betz", "bourdon12", "bourdon15", "jabardo", "jabardo_br",
    "jabardo_ss", "jones", "jones_F", "jones_w", "jo", "phan",
}

REQUIRED_COLUMNS = [
    "source_paper", "figure_ref", "surface_id", "surface_label", "fluid",
    "delta_T_wall", "delta_T_sub", "q_flux",
    "Ra_um", "theta_deg", "category", "notes",
]


# ===========================================================================
# Validation + applicability domain
# ===========================================================================

def validate_csv(df: pd.DataFrame) -> list[str]:
    """Return a list of validation issues (empty if all good)."""
    issues: list[str] = []
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        issues.append(f"Missing required columns: {missing_cols}")

    if "fluid" in df.columns:
        bad_fluids = set(df["fluid"].astype(str).str.lower().str.strip()) - SUPPORTED_FLUIDS
        if bad_fluids:
            issues.append(
                f"Unsupported fluid(s) {sorted(bad_fluids)} — rows will be "
                f"dropped from PINN inference. Supported: {sorted(SUPPORTED_FLUIDS)}"
            )

    if "q_flux" in df.columns:
        q = pd.to_numeric(df["q_flux"], errors="coerce")
        if (q < 100).any():
            issues.append(
                "Some q_flux values are < 100 W/m^2; double-check that the "
                "unit is W/m^2 (NOT kW/m^2). Multiply by 1000 if needed."
            )

    return issues


def applicability_report(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Per-row + per-variable extrapolation flag."""
    warnings_per_row: list[list[str]] = []
    warnings_summary: list[str] = []

    for _, row in df.iterrows():
        row_warns: list[str] = []
        for col, (lo, hi) in TRAINING_BOUNDS.items():
            csv_col = col.replace("_K", "").replace("_W_m2", "")
            if csv_col == "delta_T_wall":
                if pd.isna(row.get("delta_T_wall")):
                    continue  # prediction-only mode
                v = float(row["delta_T_wall"])
            elif csv_col == "delta_T_sub":
                v = float(row["delta_T_sub"]) if not pd.isna(row.get("delta_T_sub")) else 0.0
            elif csv_col == "q_flux":
                v = float(row["q_flux"])
            elif csv_col == "Ra_um":
                v = float(row["Ra_um"]) if not pd.isna(row.get("Ra_um")) else 0.0
            elif csv_col == "theta_deg":
                if pd.isna(row.get("theta_deg")):
                    continue
                v = float(row["theta_deg"])
            else:
                continue
            if v < lo or v > hi:
                row_warns.append(f"{col}={v:.4g} outside [{lo}, {hi}]")
        warnings_per_row.append(row_warns)

    n_rows = len(df)
    n_extra = sum(1 for w in warnings_per_row if w)
    if n_extra > 0:
        warnings_summary.append(
            f"{n_extra}/{n_rows} rows have at least one variable outside the "
            f"training distribution; predictions for those rows are an "
            f"extrapolation and should be interpreted accordingly."
        )

    if "category" in df.columns:
        new_cats = set(df["category"].astype(str)) - KNOWN_CATEGORIES
        if new_cats:
            warnings_summary.append(
                f"Categories {sorted(new_cats)} not seen during training; "
                f"category embedding will fall back to a neutral default."
            )

    df_out = df.copy()
    df_out["extrapolation_flags"] = ["; ".join(w) if w else "" for w in warnings_per_row]
    return df_out, warnings_summary


# ===========================================================================
# Metrics
# ===========================================================================

def safe_metrics(obs: np.ndarray, pred: np.ndarray) -> dict[str, float]:
    mask = ~(np.isnan(obs) | np.isnan(pred))
    if mask.sum() < 2:
        return {"RMSE_K": float("nan"), "MAE_K": float("nan"),
                "R2": float("nan"), "MRE_pct": float("nan"), "n": int(mask.sum())}
    o = obs[mask]
    p = pred[mask]
    err = p - o
    rmse = float(np.sqrt(np.mean(err**2)))
    mae = float(np.mean(np.abs(err)))
    ss_res = float(np.sum(err**2))
    ss_tot = float(np.sum((o - o.mean())**2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-10 else float("nan")
    mre = float(np.mean(np.abs(err) / np.maximum(np.abs(o), 1e-6)) * 100.0)
    return {"RMSE_K": rmse, "MAE_K": mae, "R2": r2,
            "MRE_pct": mre, "n": int(mask.sum())}


def coverage_95(obs: np.ndarray, lower: np.ndarray, upper: np.ndarray) -> float:
    mask = ~(np.isnan(obs) | np.isnan(lower) | np.isnan(upper))
    if mask.sum() == 0:
        return float("nan")
    o, lo, up = obs[mask], lower[mask], upper[mask]
    inside = ((o >= lo) & (o <= up)).mean()
    return float(inside * 100.0)


# ===========================================================================
# Plotting
# ===========================================================================

def plot_combined_parity(merged: pd.DataFrame, out_path: Path) -> None:
    """6-panel parity: PINN + 5 classical correlations."""
    fluid_colors = {"water": "#1f77b4", "R-123": "#9467bd",
                    "R-134a": "#2ca02c", "FC-77": "#7f7f7f"}

    panels: list[tuple[str, str]] = [
        ("PINN (ensemble mean)", "pred_mean_K"),
        ("Hsu (1962)",           "Hsu_dT_K"),
        ("Davis-Anderson (1966)","Davis_dT_K"),
        ("Bergles-Rohsenow (1964)", "BR_dT_K"),
        ("Sato-Matsumura (1964)","SM_dT_K"),
        ("Basu et al. (2002)",   "Basu_dT_K"),
    ]

    has_obs = "delta_T_wall" in merged.columns and not merged["delta_T_wall"].isna().all()

    fig, axes = plt.subplots(2, 3, figsize=(14, 9), dpi=130)
    axes = axes.flatten()

    for ax, (title, col) in zip(axes, panels):
        if col not in merged.columns:
            ax.set_title(f"{title} — column missing")
            ax.axis("off")
            continue
        pred = pd.to_numeric(merged[col], errors="coerce").to_numpy()
        if has_obs:
            obs = pd.to_numeric(merged["delta_T_wall"], errors="coerce").to_numpy()
            valid = ~(np.isnan(obs) | np.isnan(pred))
            vmax = max(np.nanmax(np.where(valid, obs, 0)),
                       np.nanmax(np.where(valid, pred, 0))) * 1.15
            vmax = max(vmax, 5.0)
            for fl, col_hex in fluid_colors.items():
                m = merged["fluid"].astype(str).str.upper() == fl.upper()
                m = m.to_numpy() & valid
                if not m.any():
                    continue
                ax.scatter(obs[m], pred[m], c=col_hex, edgecolor="black",
                           s=40, alpha=0.8, label=fl, linewidth=0.4)
            ax.plot([0, vmax], [0, vmax], "k--", lw=1.2, label="parity")
            ax.set_xlabel(r"observed $\Delta T_{\mathrm{ONB}}$ [K]")
            ax.set_ylabel(r"predicted $\Delta T_{\mathrm{ONB}}$ [K]")
            ax.set_xlim(0, vmax); ax.set_ylim(0, vmax)
            m_all = safe_metrics(obs, pred)
            ax.set_title(f"{title}\nRMSE={m_all['RMSE_K']:.2f} K, "
                         f"R²={m_all['R2']:.2f}", fontsize=10)
        else:
            ax.hist(pred[~np.isnan(pred)], bins=20, color="#1f77b4",
                    edgecolor="black", alpha=0.7)
            ax.set_xlabel(r"predicted $\Delta T_{\mathrm{ONB}}$ [K]")
            ax.set_ylabel("count")
            ax.set_title(f"{title} (no ground truth)")
        ax.legend(loc="upper left", fontsize=8)
        ax.grid(alpha=0.3)

    fig.suptitle("Predicted vs observed wall superheat at ONB", fontsize=12)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


# ===========================================================================
# Main pipeline
# ===========================================================================

def run_pipeline(
    csv_path: Path,
    run_name: str,
    ckpt_dir: Path = DEFAULT_CKPT_DIR,
    config_path: Path = DEFAULT_CONFIG,
    out_root: Path = DEFAULT_OUT_ROOT,
) -> dict[str, Path]:
    out_dir = out_root / run_name
    out_dir.mkdir(parents=True, exist_ok=True)

    # ---- Step 1: validate -------------------------------------------------
    df_raw = pd.read_csv(csv_path)
    issues = validate_csv(df_raw)
    if any("Missing required columns" in s for s in issues):
        raise RuntimeError("CSV validation failed: " + "; ".join(issues))
    for s in issues:
        warnings.warn(s)

    # ---- Step 2: applicability domain ------------------------------------
    df_checked, ad_summary = applicability_report(df_raw)
    ad_report_path = out_dir / "applicability_report.md"
    with ad_report_path.open("w") as f:
        f.write(f"# Applicability domain report — {run_name}\n\n")
        f.write(f"Source CSV: `{csv_path}`\n\n")
        f.write(f"Total rows: {len(df_raw)}\n\n")
        if ad_summary:
            f.write("## Warnings\n\n")
            for w in ad_summary:
                f.write(f"- {w}\n")
        else:
            f.write("All rows lie within the training distribution.\n")
        f.write("\n## Per-row extrapolation flags\n\n")
        for i, row in df_checked.iterrows():
            flag = row["extrapolation_flags"]
            if flag:
                f.write(f"- row {i} (`{row.get('surface_id', '?')}` / "
                        f"{row.get('fluid', '?')}): {flag}\n")

    # ---- Step 3: PINN ensemble inference ---------------------------------
    config = yaml.safe_load(config_path.read_text())
    df_pinn = collect_ensemble_predictions(
        checkpoint_dir=ckpt_dir,
        csv_path=csv_path,
        config=config,
    )

    # ---- Step 4: classical correlations ----------------------------------
    df_corr = load_with_correlations(data_csv=csv_path)

    # ---- Step 5: merge ---------------------------------------------------
    # Use a composite STRING key to avoid float-precision merge failures.
    # Both pipelines preserve input CSV row order (modulo FC-77 dropping),
    # so we construct a stable key from non-float fields.
    def _key(df):
        return (df["source_paper"].astype(str) + "||"
                + df["figure_ref"].astype(str) + "||"
                + df["surface_id"].astype(str))

    # Rename classical-correlation columns to the public *_dT_K names used
    # downstream in plots and metrics
    corr_rename = {
        "pred_hsu":  "Hsu_dT_K",
        "pred_da":   "Davis_dT_K",
        "pred_br":   "BR_dT_K",
        "pred_sm":   "SM_dT_K",
        "pred_basu": "Basu_dT_K",
    }
    df_corr = df_corr.rename(columns=corr_rename)
    keep_corr = [c for c in corr_rename.values() if c in df_corr.columns]

    df_pinn = df_pinn.copy()
    df_corr_j = df_corr.copy()
    df_pinn["_row_key"] = _key(df_pinn)
    df_corr_j["_row_key"] = _key(df_corr_j)

    merged = df_pinn.merge(
        df_corr_j[["_row_key"] + keep_corr],
        on="_row_key", how="left",
    )

    # Restore the input-CSV ground truth into a uniform column name
    if "obs_dT_K" in merged.columns:
        merged["delta_T_wall"] = merged["obs_dT_K"]

    # Add the per-row extrapolation flag (also key-merge to avoid float issues)
    if "extrapolation_flags" in df_checked.columns:
        df_checked_j = df_checked.copy()
        df_checked_j["_row_key"] = _key(df_checked_j)
        merged = merged.merge(
            df_checked_j[["_row_key", "extrapolation_flags"]],
            on="_row_key", how="left",
        )

    merged = merged.drop(columns=["_row_key"], errors="ignore")

    pred_csv = out_dir / "predictions.csv"
    merged.to_csv(pred_csv, index=False)

    # ---- Step 6: metrics --------------------------------------------------
    metrics_md = out_dir / "metrics.md"
    has_obs = "delta_T_wall" in merged.columns and not merged["delta_T_wall"].isna().all()

    with metrics_md.open("w") as f:
        f.write(f"# Metrics — {run_name}\n\n")
        f.write(f"Rows scored: {len(merged)}\n\n")
        if not has_obs:
            f.write("No ground-truth `delta_T_wall` provided → metrics skipped. "
                    "Predictions only.\n")
            return {"predictions": pred_csv, "metrics": metrics_md,
                    "applicability": ad_report_path}

        obs = pd.to_numeric(merged["delta_T_wall"], errors="coerce").to_numpy()

        pinn_m = safe_metrics(obs, merged["pred_mean_K"].to_numpy())
        pinn_cov = coverage_95(obs,
                               merged["lower_95_K"].to_numpy(),
                               merged["upper_95_K"].to_numpy())

        f.write("## Overall (PINN + 5 classical correlations)\n\n")
        f.write("| Model | n | RMSE [K] | MAE [K] | R² | MRE [%] | 95% coverage [%] |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        f.write(f"| **PINN (ensemble mean)** | {pinn_m['n']} | "
                f"{pinn_m['RMSE_K']:.2f} | {pinn_m['MAE_K']:.2f} | "
                f"{pinn_m['R2']:.3f} | {pinn_m['MRE_pct']:.1f} | "
                f"{pinn_cov:.1f} |\n")

        corr_cols: list[tuple[str, str]] = [
            ("Hsu (1962)",            "Hsu_dT_K"),
            ("Davis-Anderson (1966)", "Davis_dT_K"),
            ("Bergles-Rohsenow (1964)", "BR_dT_K"),
            ("Sato-Matsumura (1964)", "SM_dT_K"),
            ("Basu et al. (2002)",    "Basu_dT_K"),
        ]
        for name, col in corr_cols:
            if col not in merged.columns:
                continue
            pred = pd.to_numeric(merged[col], errors="coerce").to_numpy()
            m = safe_metrics(obs, pred)
            f.write(f"| {name} | {m['n']} | {m['RMSE_K']:.2f} | "
                    f"{m['MAE_K']:.2f} | {m['R2']:.3f} | "
                    f"{m['MRE_pct']:.1f} | — |\n")

        # Per-fluid breakdown
        f.write("\n## Per-fluid (PINN only)\n\n")
        f.write("| Fluid | n | RMSE [K] | MAE [K] | R² |\n|---|---|---|---|---|\n")
        for fl in sorted(merged["fluid"].astype(str).unique()):
            m_f = merged["fluid"].astype(str) == fl
            if not m_f.any():
                continue
            obs_f = pd.to_numeric(merged.loc[m_f, "delta_T_wall"],
                                  errors="coerce").to_numpy()
            pred_f = merged.loc[m_f, "pred_mean_K"].to_numpy()
            mm = safe_metrics(obs_f, pred_f)
            f.write(f"| {fl} | {mm['n']} | {mm['RMSE_K']:.2f} | "
                    f"{mm['MAE_K']:.2f} | {mm['R2']:.3f} |\n")

    # ---- Step 7: parity plot ---------------------------------------------
    parity_png = out_dir / "parity_combined.png"
    plot_combined_parity(merged, parity_png)

    print(f"[predict_new_experiment] Done.")
    print(f"  predictions:   {pred_csv}")
    print(f"  metrics:       {metrics_md}")
    print(f"  parity plot:   {parity_png}")
    print(f"  applicability: {ad_report_path}")

    return {
        "predictions": pred_csv,
        "metrics": metrics_md,
        "parity": parity_png,
        "applicability": ad_report_path,
    }


# ===========================================================================
# CLI
# ===========================================================================

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="End-to-end ONB inference + classical-correlation "
                    "comparison wrapper for new pool-boiling experiments.",
    )
    p.add_argument("--csv", type=Path, required=True,
                   help="Path to the new-experiment CSV (12-column schema).")
    p.add_argument("--run-name", required=True,
                   help="Label for the output sub-directory.")
    p.add_argument("--ckpt-dir", type=Path, default=DEFAULT_CKPT_DIR,
                   help="Deep ensemble checkpoint directory "
                        "(default: ensemble_phaseDbal).")
    p.add_argument("--config", type=Path, default=DEFAULT_CONFIG,
                   help="YAML config matching the checkpoint.")
    p.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_ROOT,
                   help="Parent directory for the run output.")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    if not args.csv.exists():
        raise FileNotFoundError(f"Input CSV not found: {args.csv}")
    if not args.ckpt_dir.exists():
        raise FileNotFoundError(f"Checkpoint directory not found: {args.ckpt_dir}")
    if not args.config.exists():
        raise FileNotFoundError(f"Config not found: {args.config}")

    run_pipeline(
        csv_path=args.csv,
        run_name=args.run_name,
        ckpt_dir=args.ckpt_dir,
        config_path=args.config,
        out_root=args.out_dir,
    )


if __name__ == "__main__":
    main()
