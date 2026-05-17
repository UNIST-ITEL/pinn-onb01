"""
analyze_ensemble.py — Deep Ensemble UQ analysis for PINN-ONB01 (Section 5.3).

Loads K ensemble checkpoints, predicts on all 43 ONB data points, computes
uncertainty statistics, and generates 5 figures + metrics table.

Outputs
-------
04_analysis/tables/ensemble_predictions.csv
04_analysis/tables/ensemble_metrics.md
04_analysis/figures/ensemble_parity_with_errorbars.png
04_analysis/figures/ensemble_std_vs_qflux.png
04_analysis/figures/ensemble_std_by_category.png
04_analysis/figures/ensemble_std_by_fluid.png
04_analysis/figures/ensemble_epistemic_vs_aleatoric.png

Usage:
    python 04_analysis/scripts/analyze_ensemble.py [--ckpt-dir <path>]
"""

from __future__ import annotations

import math
import sys
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import torch
import yaml

# ---------------------------------------------------------------------------
# Project root and path setup
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "03_model"))

from src.training.ensemble import collect_ensemble_predictions  # type: ignore
from src.training.dataset import OnbDataset  # type: ignore

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
CKPT_DIR = ROOT / "03_model" / "checkpoints" / "ensemble_phaseB"
CONFIG_PATH = ROOT / "03_model" / "configs" / "baseline_phaseB.yaml"
CSV_PATH = ROOT / "02_data" / "processed" / "onb_dataset.csv"
FIG_DIR = ROOT / "04_analysis" / "figures"
TABLE_DIR = ROOT / "04_analysis" / "tables"

FIG_DIR.mkdir(parents=True, exist_ok=True)
TABLE_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Correlation model reference values from correlation_metrics.md
# ---------------------------------------------------------------------------
CORR_METRICS: dict[str, dict[str, float]] = {
    "Hsu (1962)":            {"RMSE_K": 7.43, "MAE_K": 6.07, "R2": -0.978, "n": 43},
    "Davis-Anderson (1966)": {"RMSE_K": 16.47,"MAE_K": 10.26,"R2": -8.721, "n": 43},
    "Bergles-Rohsenow (1964)":{"RMSE_K": 7.87,"MAE_K": 6.37, "R2": -0.874, "n": 33},
    "Sato-Matsumura (1964)": {"RMSE_K": 7.43, "MAE_K": 6.07, "R2": -0.978, "n": 43},
    "Basu et al. (2002)":    {"RMSE_K": 7.21, "MAE_K": 5.85, "R2": -0.208, "n": 22},
}

# Single phaseB model (from pinn_metrics_baseline_phaseB.md)
SINGLE_MODEL_METRICS: dict[str, float] = {
    "RMSE_K": 5.55, "MAE_K": 4.62, "R2": -0.105, "n": 43,
}


# ===========================================================================
# Metrics helper
# ===========================================================================

def compute_metrics(obs: np.ndarray, pred: np.ndarray) -> dict[str, float]:
    err = pred - obs
    rmse = float(np.sqrt(np.mean(err**2)))
    mae = float(np.mean(np.abs(err)))
    ss_res = float(np.sum(err**2))
    ss_tot = float(np.sum((obs - np.mean(obs))**2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-10 else float("nan")
    mre = float(np.mean(np.abs(err) / np.maximum(np.abs(obs), 1e-6)) * 100.0)
    return {"RMSE_K": rmse, "MAE_K": mae, "R2": r2, "MRE_pct": mre, "n": int(len(obs))}


# ===========================================================================
# Figure 1: Parity plot with error bars
# ===========================================================================

def plot_parity_errorbars(df: pd.DataFrame, out_png: Path) -> None:
    obs = df["obs_dT_K"].to_numpy()
    pred_mean = df["pred_mean_K"].to_numpy()
    pred_std_total = df["pred_std_total_K"].to_numpy()
    covered = df["covered_95"].to_numpy().astype(bool)
    coverage_pct = covered.mean() * 100.0

    vmin = 0.0
    vmax = max(obs.max(), pred_mean.max()) * 1.15

    fig, ax = plt.subplots(figsize=(7, 6), dpi=130)

    # Green = covered, red = outside CI
    yerr_95 = 1.96 * pred_std_total
    for i in range(len(obs)):
        color = "#2ca02c" if covered[i] else "#d62728"
        ax.errorbar(
            obs[i], pred_mean[i],
            yerr=yerr_95[i],
            fmt="o", color=color, alpha=0.75,
            markersize=5, capsize=3, linewidth=0.8,
            elinewidth=0.8,
        )

    ax.plot([vmin, vmax], [vmin, vmax], "k--", lw=1.5, label="parity")
    for k, ls, lab in [(1.3, ":", "±30%"), (1.5, "-.", "±50%")]:
        ax.plot([vmin, vmax], [vmin*k, vmax*k], color="gray", ls=ls, lw=0.8)
        ax.plot([vmin, vmax], [vmin/k, vmax/k], color="gray", ls=ls, lw=0.8,
                label=lab)

    green_patch = mpatches.Patch(color="#2ca02c", alpha=0.75, label=f"Inside 95% CI ({covered.sum()}/{len(obs)})")
    red_patch   = mpatches.Patch(color="#d62728", alpha=0.75, label=f"Outside 95% CI ({(~covered).sum()}/{len(obs)})")
    ax.legend(handles=[green_patch, red_patch] + ax.get_lines()[:3], fontsize=8, loc="upper left")

    m = compute_metrics(obs, pred_mean)
    ax.set_xlim(vmin, vmax)
    ax.set_ylim(vmin, vmax)
    ax.set_xlabel(r"Observed $\Delta T_{ONB}$ [K]", fontsize=11)
    ax.set_ylabel(r"Ensemble-mean $\Delta T_{ONB}$ [K]", fontsize=11)
    ax.set_title(
        f"Deep Ensemble parity — RMSE={m['RMSE_K']:.2f} K  R²={m['R2']:.3f}  "
        f"Coverage={coverage_pct:.1f}%",
        fontsize=10,
    )
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_png, dpi=130)
    plt.close(fig)
    print(f"[figure] → {out_png}")


# ===========================================================================
# Figure 2: σ vs q''
# ===========================================================================

def plot_std_vs_qflux(df: pd.DataFrame, out_png: Path) -> None:
    q = df["q_flux_W_m2"].to_numpy() / 1e3  # kW/m²
    std_epi = df["pred_std_epi_K"].to_numpy()
    std_total = df["pred_std_total_K"].to_numpy()

    fig, ax = plt.subplots(figsize=(7, 5), dpi=130)

    sc = ax.scatter(q, std_epi, c=std_epi, cmap="YlOrRd", s=50,
                    edgecolors="k", linewidths=0.4, zorder=3,
                    label=r"$\sigma_{epi}$ (epistemic)")
    ax.scatter(q, std_total, c="none", edgecolors="royalblue", s=50,
               linewidths=0.8, zorder=2, label=r"$\sigma_{total}$")

    plt.colorbar(sc, ax=ax, label=r"$\sigma_{epi}$ [K]")

    # Training data q'' range
    q_min, q_max = q.min(), q.max()
    ax.axvspan(q_min, q_max, alpha=0.07, color="green", label="Training range")

    ax.set_xlabel(r"Heat flux $q''$ [kW/m²]", fontsize=11)
    ax.set_ylabel(r"Uncertainty $\sigma$ [K]", fontsize=11)
    ax.set_title(r"Epistemic uncertainty vs. heat flux", fontsize=11)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_png, dpi=130)
    plt.close(fig)
    print(f"[figure] → {out_png}")


# ===========================================================================
# Figure 3: σ by source category (paper)
# ===========================================================================

def plot_std_by_category(df: pd.DataFrame, out_png: Path) -> None:
    papers = sorted(df["source_paper"].unique())
    data_by_paper = [df[df["source_paper"] == p]["pred_std_epi_K"].to_numpy() for p in papers]
    n_by_paper    = [len(df[df["source_paper"] == p]) for p in papers]

    fig, ax = plt.subplots(figsize=(9, 5), dpi=130)
    bp = ax.boxplot(
        data_by_paper, patch_artist=True, notch=False,
        medianprops={"color": "black", "linewidth": 1.5},
    )
    colors = plt.cm.tab10(np.linspace(0, 1, len(papers)))  # type: ignore[attr-defined]
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)

    ax.set_xticks(range(1, len(papers) + 1))
    ax.set_xticklabels(
        [f"{p}\n(N={n})" for p, n in zip(papers, n_by_paper)],
        rotation=30, ha="right", fontsize=8,
    )
    ax.set_ylabel(r"Epistemic $\sigma_{epi}$ [K]", fontsize=11)
    ax.set_title("Epistemic uncertainty by source paper", fontsize=11)
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_png, dpi=130)
    plt.close(fig)
    print(f"[figure] → {out_png}")


# ===========================================================================
# Figure 4: σ by fluid
# ===========================================================================

def plot_std_by_fluid(df: pd.DataFrame, out_png: Path) -> None:
    fluids = sorted(df["fluid"].unique())
    data_by_fluid = [df[df["fluid"] == f]["pred_std_epi_K"].to_numpy() for f in fluids]
    n_by_fluid    = [len(df[df["fluid"] == f]) for f in fluids]

    fig, ax = plt.subplots(figsize=(6, 5), dpi=130)
    palette = ["tab:blue", "tab:orange", "tab:green", "tab:red"]
    bp = ax.boxplot(
        data_by_fluid, patch_artist=True, notch=False,
        medianprops={"color": "black", "linewidth": 1.5},
    )
    for i, patch in enumerate(bp["boxes"]):
        patch.set_facecolor(palette[i % len(palette)])
        patch.set_alpha(0.6)

    ax.set_xticks(range(1, len(fluids) + 1))
    ax.set_xticklabels(
        [f"{f}\n(N={n})" for f, n in zip(fluids, n_by_fluid)],
        fontsize=10,
    )
    ax.set_ylabel(r"Epistemic $\sigma_{epi}$ [K]", fontsize=11)
    ax.set_title("Epistemic uncertainty by fluid", fontsize=11)
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_png, dpi=130)
    plt.close(fig)
    print(f"[figure] → {out_png}")


# ===========================================================================
# Figure 5: Epistemic vs aleatoric comparison
# ===========================================================================

def plot_epistemic_vs_aleatoric(df: pd.DataFrame, out_png: Path) -> None:
    idx = np.arange(len(df))
    epi = df["pred_std_epi_K"].to_numpy()
    ale = df["pred_std_ale_K"].to_numpy()

    fig, ax = plt.subplots(figsize=(10, 4), dpi=130)

    ax.bar(idx, epi, label=r"Epistemic $\sigma_{epi}$", color="steelblue", alpha=0.7)
    ax.bar(idx, ale, bottom=0, label=r"Aleatoric $\sigma_{ale}$ (±20% lit. est.)",
           color="tomato", alpha=0.5)

    ax.set_xlabel("ONB data point index", fontsize=10)
    ax.set_ylabel(r"$\sigma$ [K]", fontsize=11)
    ax.set_title("Epistemic vs. aleatoric uncertainty (all 43 ONB points)", fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_png, dpi=130)
    plt.close(fig)
    print(f"[figure] → {out_png}")


# ===========================================================================
# Metrics table
# ===========================================================================

def write_metrics_table(df: pd.DataFrame, out_md: Path) -> str:
    """Write ensemble_metrics.md and return the table string for console."""
    obs  = df["obs_dT_K"].to_numpy()
    pred = df["pred_mean_K"].to_numpy()
    overall = compute_metrics(obs, pred)
    coverage = df["covered_95"].mean() * 100.0
    mean_sigma = float(df["pred_std_total_K"].mean())
    max_sigma  = float(df["pred_std_total_K"].max())
    max_idx    = int(df["pred_std_total_K"].idxmax())
    max_surface  = df.iloc[max_idx]["surface_id"]
    max_fluid    = df.iloc[max_idx]["fluid"]
    max_paper    = df.iloc[max_idx]["source_paper"]

    mean_epi = float(df["pred_std_epi_K"].mean())
    mean_ale = float(df["pred_std_ale_K"].mean())
    dominant = "epistemic" if mean_epi > mean_ale else "aleatoric"

    K = sum(1 for c in df.columns if c.startswith("pred_seed_"))

    lines: list[str] = []
    lines.append("# Deep Ensemble UQ — Metrics Report (Section 5.3)\n")
    lines.append(f"Members: K = {K}\n")
    lines.append(f"Aleatoric assumption: fixed ±20% of prediction (literature-typical for ONB)\n")

    lines.append("\n## Overall ensemble performance\n")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Ensemble mean RMSE | {overall['RMSE_K']:.2f} K |")
    lines.append(f"| Ensemble mean MAE  | {overall['MAE_K']:.2f} K |")
    lines.append(f"| Ensemble mean R²   | {overall['R2']:.3f} |")
    lines.append(f"| 95% CI Coverage    | {coverage:.1f}% (target: 95%) |")
    lines.append(f"| Mean σ_total        | {mean_sigma:.2f} K |")
    lines.append(f"| Max σ_total         | {max_sigma:.2f} K ({max_surface}, {max_fluid}, {max_paper}) |")
    lines.append(f"| Mean σ_epi          | {mean_epi:.2f} K |")
    lines.append(f"| Mean σ_ale          | {mean_ale:.2f} K |")
    lines.append(f"| Dominant uncertainty | {dominant} |")

    lines.append("\n## Fluid breakdown\n")
    lines.append("| Fluid | n | RMSE [K] | MAE [K] | R² | Coverage [%] | Mean σ_epi [K] |")
    lines.append("|-------|---|----------|---------|-----|-------------|---------------|")
    for fluid in sorted(df["fluid"].unique()):
        sub = df[df["fluid"] == fluid]
        m = compute_metrics(sub["obs_dT_K"].to_numpy(), sub["pred_mean_K"].to_numpy())
        cov = sub["covered_95"].mean() * 100.0
        me = sub["pred_std_epi_K"].mean()
        lines.append(
            f"| {fluid} | {m['n']} | {m['RMSE_K']:.2f} | {m['MAE_K']:.2f} "
            f"| {m['R2']:.3f} | {cov:.1f} | {me:.2f} |"
        )

    lines.append("\n## Source paper breakdown\n")
    lines.append("| Paper | n | RMSE [K] | MAE [K] | R² | Coverage [%] | Mean σ_epi [K] |")
    lines.append("|-------|---|----------|---------|-----|-------------|---------------|")
    for paper in sorted(df["source_paper"].unique()):
        sub = df[df["source_paper"] == paper]
        m = compute_metrics(sub["obs_dT_K"].to_numpy(), sub["pred_mean_K"].to_numpy())
        cov = sub["covered_95"].mean() * 100.0
        me = sub["pred_std_epi_K"].mean()
        lines.append(
            f"| {paper} | {m['n']} | {m['RMSE_K']:.2f} | {m['MAE_K']:.2f} "
            f"| {m['R2']:.3f} | {cov:.1f} | {me:.2f} |"
        )

    lines.append("\n## Model comparison\n")
    lines.append("| Model | RMSE [K] | MAE [K] | R² | n |")
    lines.append("|-------|----------|---------|-----|---|")
    for name, m in CORR_METRICS.items():
        lines.append(f"| {name} | {m['RMSE_K']:.2f} | {m['MAE_K']:.2f} | {m['R2']:.3f} | {m['n']} |")
    sm = SINGLE_MODEL_METRICS
    lines.append(
        f"| PINN phaseB (single) | {sm['RMSE_K']:.2f} | {sm['MAE_K']:.2f} | {sm['R2']:.3f} | {sm['n']} |"
    )
    lines.append(
        f"| **PINN phaseB Ensemble (K={K})** | **{overall['RMSE_K']:.2f}** | "
        f"**{overall['MAE_K']:.2f}** | **{overall['R2']:.3f}** | **{overall['n']}** |"
    )

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(lines) + "\n")
    print(f"[table] → {out_md}")

    return "\n".join(lines)


# ===========================================================================
# Main
# ===========================================================================

def main(ckpt_dir: Path = CKPT_DIR) -> None:
    import argparse

    ap = argparse.ArgumentParser(description="Analyze Deep Ensemble UQ results")
    ap.add_argument("--ckpt-dir", type=Path, default=CKPT_DIR)
    ap.add_argument("--config", type=Path, default=CONFIG_PATH)
    ap.add_argument("--csv", type=Path, default=CSV_PATH)
    args = ap.parse_args()

    ckpt_dir   = args.ckpt_dir.resolve()
    config_path = args.config.resolve()
    csv_path    = args.csv.resolve()

    config = yaml.safe_load(config_path.read_text())

    # --- Collect predictions -------------------------------------------------
    print(f"[analyze] Loading ensemble from {ckpt_dir}")
    df = collect_ensemble_predictions(
        checkpoint_dir=ckpt_dir,
        csv_path=csv_path,
        config=config,
    )

    # --- Save predictions CSV ------------------------------------------------
    pred_csv = TABLE_DIR / "ensemble_predictions.csv"
    # Columns per spec:
    csv_cols = [
        "source_paper", "surface_id", "fluid", "q_flux_W_m2",
        "obs_dT_K", "pred_mean_K", "pred_std_epi_K",
        "pred_std_ale_K", "pred_std_total_K",
        "lower_95_K", "upper_95_K", "covered_95",
    ]
    # Also include figure_ref if present
    if "figure_ref" in df.columns:
        csv_cols = ["source_paper", "figure_ref"] + csv_cols[1:]
    df[csv_cols].to_csv(pred_csv, index=False)
    print(f"[analyze] Predictions saved → {pred_csv}")

    # --- Print summary -------------------------------------------------------
    obs = df["obs_dT_K"].to_numpy()
    pred = df["pred_mean_K"].to_numpy()
    m = compute_metrics(obs, pred)
    coverage = df["covered_95"].mean() * 100.0
    mean_epi = df["pred_std_epi_K"].mean()
    mean_ale = df["pred_std_ale_K"].mean()
    mean_total = df["pred_std_total_K"].mean()
    max_total  = df["pred_std_total_K"].max()
    K = sum(1 for c in df.columns if c.startswith("pred_seed_"))

    print(f"\n{'='*60}")
    print(f"Deep Ensemble UQ Summary")
    print(f"{'='*60}")
    print(f"Members: K = {K}")
    print(f"Ensemble RMSE = {m['RMSE_K']:.2f} K  MAE = {m['MAE_K']:.2f} K  R² = {m['R2']:.3f}")
    print(f"95% CI Coverage = {coverage:.1f}%  (target: 95%)")
    print(f"Mean σ_epi = {mean_epi:.2f} K  Mean σ_ale = {mean_ale:.2f} K  Mean σ_total = {mean_total:.2f} K")
    print(f"Max σ_total = {max_total:.2f} K")

    # --- Figures -------------------------------------------------------------
    plot_parity_errorbars(df, FIG_DIR / "ensemble_parity_with_errorbars.png")
    plot_std_vs_qflux(df, FIG_DIR / "ensemble_std_vs_qflux.png")
    plot_std_by_category(df, FIG_DIR / "ensemble_std_by_category.png")
    plot_std_by_fluid(df, FIG_DIR / "ensemble_std_by_fluid.png")
    plot_epistemic_vs_aleatoric(df, FIG_DIR / "ensemble_epistemic_vs_aleatoric.png")

    # --- Metrics table -------------------------------------------------------
    write_metrics_table(df, TABLE_DIR / "ensemble_metrics.md")

    print(f"\n[analyze] All outputs written to {ROOT / '04_analysis'}")


if __name__ == "__main__":
    main()
