"""
evaluate.py — Phase 2 PINN evaluation + classical correlation comparison.

Generates (plan.md §5.1 Level 4):
  analysis/figures/parity_dT_onb.pdf   — PINN + 5 correlations parity plot
  analysis/figures/parity_q_onb.pdf    — q_ONB parity plot
  analysis/tables/metrics.csv          — RMSE/MAE/R² per method and fluid
  analysis/tables/per_paper.csv        — RMSE breakdown by paper_id

Usage:
  cd phase2_flow_boiling
  # After training:
  python experiments/src/evaluate.py \
      --config experiments/configs/phase2_baseline_v1.yaml \
      --checkpoint experiments/checkpoints/phase2_baseline_v1/best_model.pt

  # Correlations only (no PINN checkpoint needed):
  python experiments/src/evaluate.py \
      --config experiments/configs/phase2_baseline_v1.yaml \
      --no-pinn
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader

_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from correlations import (
    CorrelationResult,
    _metrics,
    basu_dT_from_q,
    bergles_rohsenow_dT_from_q,
    evaluate_correlation,
    get_rho_v,
    hsu_dT_from_q,
    kandlikar_dT_from_q,
    sato_matsumura_dT_from_q,
)
from data.dataset import FlowBoilingDataset, collate_fn
from model.flow_boiling_pinn import FlowBoilingPINN
from train import build_datasets, build_loaders, build_model, evaluate, load_config
from utils.nondim_flow import compute_flow_nondim, FlowNondimScales

_PROJ = Path(__file__).resolve().parents[2]


# ── Build a raw evaluation table from the dataset ────────────────────────────

def build_eval_table(
    datasets: tuple[FlowBoilingDataset, FlowBoilingDataset, FlowBoilingDataset],
    csv_path: Path,
) -> pd.DataFrame:
    """Merge raw CSV with split labels for per-row analysis."""
    raw = pd.read_csv(csv_path)
    # Attach split column by matching indices
    # (datasets were created with same seed → reproducible)
    train_ds, val_ds, test_ds = datasets

    def _indices(ds: FlowBoilingDataset) -> list[int]:
        return ds._df.index.tolist()

    raw = raw.copy()
    raw["split"] = "train"
    raw.loc[_indices(val_ds),  "split"] = "val"
    raw.loc[_indices(test_ds), "split"] = "test"
    return raw


# ── PINN predictions on the raw CSV rows ─────────────────────────────────────

@torch.no_grad()
def pinn_predictions(
    model:    FlowBoilingPINN,
    train_ds: FlowBoilingDataset,
    val_ds:   FlowBoilingDataset,
    test_ds:  FlowBoilingDataset,
    cfg:      dict,
    device:   torch.device,
) -> tuple[np.ndarray, np.ndarray]:
    """Return (pred_dT_K, pred_q_Wm2) aligned with all rows (train+val+test order)."""
    all_ds_splits = [("train", train_ds), ("val", val_ds), ("test", test_ds)]
    pred_dT_list, pred_q_list = [], []

    for _, ds in all_ds_splits:
        loader = DataLoader(ds, batch_size=64, shuffle=False, collate_fn=collate_fn)
        model.eval()
        for batch in loader:
            x    = batch["x_star"].to(device)
            sf   = {k: v.to(device) for k, v in batch["surface_features"].items()}
            fn   = batch["flow_numeric"].to(device)
            out  = model(x, sf, fn)
            dT_ref  = batch["dT_ref"].to(device)
            q_ref_b = batch["q_ref"].to(device)
            pred_dT_list.append((out.delta_T_onb_star.squeeze(-1) * dT_ref).cpu().numpy())
            pred_q_list.append((out.q_onb_star.squeeze(-1) * q_ref_b).cpu().numpy())

    return np.concatenate(pred_dT_list), np.concatenate(pred_q_list)


# ── Classical correlation predictions ────────────────────────────────────────

def correlation_predictions(raw: pd.DataFrame) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    """
    For each row in raw CSV, compute ΔT_ONB and q_ONB via each correlation.

    Uses measured q_onb as input to predict ΔT (forward direction).
    Uses measured ΔT_onb as input to predict q (inverse direction).
    Returns dict of {corr_name: (pred_dT_K, pred_q_Wm2)}.
    """
    n = len(raw)
    results: dict[str, tuple[np.ndarray, np.ndarray]] = {}

    # Initialise with NaN
    def _nan() -> np.ndarray:
        return np.full(n, np.nan)

    names = [
        "Hsu_1962", "Sato-Matsumura_1964",
        "Bergles-Rohsenow_1964", "Kandlikar_1991", "Basu_2002",
    ]
    pred_dT = {k: _nan() for k in names}
    pred_q  = {k: _nan() for k in names}

    for i, row in raw.iterrows():
        fluid  = str(row["fluid"])
        P_kPa  = float(row["P_kPa"]) if row["P_kPa"] > 0 else 101.325
        P_Pa   = P_kPa * 1e3
        G      = float(row["G_kg_m2s"])
        D_h_m  = float(row["D_h_mm"]) * 1e-3

        try:
            sc     = compute_flow_nondim(fluid, P_kPa)
            rho_v  = get_rho_v(fluid, P_Pa, sc.T_sat_K)
            props  = dict(sigma=sc.sigma, T_sat_K=sc.T_sat_K,
                          k_l=sc.k_l, h_fg=sc.h_fg, rho_v=rho_v)
            Pr     = sc.cp_l * sc.mu_l / sc.k_l
            Re     = G * D_h_m / sc.mu_l if G > 0 and D_h_m > 0 else 5000.0
        except Exception:
            continue

        q_meas  = row["q_onb_W_m2"]    if row["q_onb_W_m2"]   > 0 else np.nan
        dT_meas = row["delta_T_onb_K"] if row["delta_T_onb_K"] > 0 else np.nan

        def _safe(fn, *args, **kwargs) -> float:
            try:
                v = float(fn(*args, **kwargs))
                return v if np.isfinite(v) and v > 0 else np.nan
            except Exception:
                return np.nan

        # Forward: q → ΔT
        if np.isfinite(q_meas):
            pred_dT["Hsu_1962"][i]              = _safe(hsu_dT_from_q,             q_meas, **props)
            pred_dT["Sato-Matsumura_1964"][i]   = _safe(sato_matsumura_dT_from_q,  q_meas, **props)
            pred_dT["Bergles-Rohsenow_1964"][i] = _safe(bergles_rohsenow_dT_from_q, q_meas, P_Pa=P_Pa, fluid=fluid)
            pred_dT["Kandlikar_1991"][i]        = _safe(kandlikar_dT_from_q,        q_meas, **props, Re=Re, Pr=Pr, D_h_m=D_h_m)
            theta = float(row["theta_deg"]) if row["theta_deg"] > 0 else 35.0
            pred_dT["Basu_2002"][i]             = _safe(basu_dT_from_q,             q_meas, **props, theta_deg=theta)

        # Inverse: ΔT → q
        if np.isfinite(dT_meas):
            from correlations import hsu_q_from_dT, sato_matsumura_q_from_dT, bergles_rohsenow_q_from_dT, kandlikar_q_from_dT, basu_q_from_dT
            pred_q["Hsu_1962"][i]              = _safe(hsu_q_from_dT,             dT_meas, **props)
            pred_q["Sato-Matsumura_1964"][i]   = _safe(sato_matsumura_q_from_dT,  dT_meas, **props)
            pred_q["Bergles-Rohsenow_1964"][i] = _safe(bergles_rohsenow_q_from_dT, dT_meas, P_Pa=P_Pa, fluid=fluid)
            pred_q["Kandlikar_1991"][i]        = _safe(kandlikar_q_from_dT,        dT_meas, **props)
            theta = float(row["theta_deg"]) if row["theta_deg"] > 0 else 35.0
            pred_q["Basu_2002"][i]             = _safe(basu_q_from_dT,             dT_meas, **props, theta_deg=theta)

    return {k: (pred_dT[k], pred_q[k]) for k in names}


# ── Metrics table ─────────────────────────────────────────────────────────────

def build_metrics_table(
    raw:      pd.DataFrame,
    corr_preds: dict[str, tuple[np.ndarray, np.ndarray]],
    pinn_dT:  np.ndarray | None,
    pinn_q:   np.ndarray | None,
    split:    str = "all",
) -> pd.DataFrame:
    """RMSE/MAE/R² for PINN + each correlation, optionally filtered by split."""
    if split != "all":
        mask = (raw["split"] == split).values
    else:
        mask = np.ones(len(raw), dtype=bool)

    true_dT = raw["delta_T_onb_K"].values.astype(float)
    true_q  = raw["q_onb_W_m2"].values.astype(float)
    true_dT[true_dT <= 0] = np.nan
    true_q[true_q <= 0]   = np.nan

    rows = []
    methods: dict[str, tuple[np.ndarray, np.ndarray]] = {}

    if pinn_dT is not None and pinn_q is not None:
        methods["PINN (Phase 2)"] = (pinn_dT, pinn_q)
    methods.update(corr_preds)

    for name, (pred_dT, pred_q) in methods.items():
        rm_dT, mae_dT, r2_dT, n_dT = _metrics(pred_dT[mask], true_dT[mask])
        rm_q,  mae_q,  r2_q,  n_q  = _metrics(pred_q[mask],  true_q[mask])
        rows.append({
            "method":    name,
            "rmse_dT_K": rm_dT,   "mae_dT_K": mae_dT,  "r2_dT": r2_dT,  "n_dT": n_dT,
            "rmse_q_kW": rm_q/1e3 if not np.isnan(rm_q) else np.nan,
            "mae_q_kW":  mae_q/1e3 if not np.isnan(mae_q) else np.nan,
            "r2_q":      r2_q,    "n_q": n_q,
        })
    return pd.DataFrame(rows)


def build_per_fluid_table(
    raw:      pd.DataFrame,
    corr_preds: dict[str, tuple[np.ndarray, np.ndarray]],
    pinn_dT:  np.ndarray | None,
    pinn_q:   np.ndarray | None,
) -> pd.DataFrame:
    """Per-fluid RMSE for PINN and each correlation (test split only)."""
    mask_test = (raw["split"] == "test").values
    true_dT   = raw["delta_T_onb_K"].values.astype(float)
    true_dT[true_dT <= 0] = np.nan

    rows = []
    for fluid in sorted(raw["fluid"].unique()):
        fluid_mask = (raw["fluid"] == fluid).values & mask_test
        if fluid_mask.sum() == 0:
            continue
        methods: dict[str, np.ndarray] = {}
        if pinn_dT is not None:
            methods["PINN"] = pinn_dT
        for name, (pred_dT, _) in corr_preds.items():
            methods[name] = pred_dT
        row = {"fluid": fluid, "n_test": int(fluid_mask.sum())}
        for mname, pred_dT in methods.items():
            rmse, *_ = _metrics(pred_dT[fluid_mask], true_dT[fluid_mask])
            row[f"rmse_dT_{mname[:4]}"] = rmse
        rows.append(row)
    return pd.DataFrame(rows)


# ── Parity plot ───────────────────────────────────────────────────────────────

def plot_parity(
    raw:           pd.DataFrame,
    corr_preds:    dict[str, tuple[np.ndarray, np.ndarray]],
    pinn_dT:       np.ndarray | None,
    out_dir:       Path,
    split:         str = "test",
) -> None:
    """Parity plot: predicted vs measured ΔT_ONB for PINN + correlations."""
    try:
        import matplotlib.pyplot as plt
        import matplotlib as mpl
        mpl.rcParams.update({
            "font.size": 11, "axes.labelsize": 12,
            "figure.dpi": 150, "savefig.bbox": "tight",
        })
    except ImportError:
        print("  [warn] matplotlib not available — skipping parity plot")
        return

    if split != "all":
        mask = (raw["split"] == split).values
    else:
        mask = np.ones(len(raw), dtype=bool)

    true_dT = raw["delta_T_onb_K"].values.astype(float)
    true_dT[true_dT <= 0] = np.nan
    t = true_dT[mask]

    _COLORS = {
        "PINN (Phase 2)":         "tab:blue",
        "Hsu_1962":               "tab:orange",
        "Sato-Matsumura_1964":    "tab:green",
        "Bergles-Rohsenow_1964":  "tab:red",
        "Kandlikar_1991":         "tab:purple",
        "Basu_2002":              "tab:brown",
    }
    _MARKERS = {
        "PINN (Phase 2)":         "o",
        "Hsu_1962":               "s",
        "Sato-Matsumura_1964":    "^",
        "Bergles-Rohsenow_1964":  "D",
        "Kandlikar_1991":         "v",
        "Basu_2002":              "P",
    }

    fig, ax = plt.subplots(figsize=(6, 6))
    all_vals = t[np.isfinite(t)].tolist()

    methods: dict[str, np.ndarray] = {}
    if pinn_dT is not None:
        methods["PINN (Phase 2)"] = pinn_dT
    for name, (pred_dT, _) in corr_preds.items():
        methods[name] = pred_dT

    for name, pred in methods.items():
        p = pred[mask]
        fm = np.isfinite(p) & np.isfinite(t)
        if fm.sum() == 0:
            continue
        rmse, _, r2, n = _metrics(p[fm], t[fm])
        label = f"{name.replace('_', ' ')}  RMSE={rmse:.2f} K (n={n})"
        ax.scatter(t[fm], p[fm],
                   color=_COLORS.get(name, "gray"),
                   marker=_MARKERS.get(name, "x"),
                   s=30, alpha=0.7, label=label)
        all_vals.extend(p[fm].tolist())

    lim = (0, max(all_vals) * 1.05) if all_vals else (0, 30)
    ax.plot(lim, lim, "k--", lw=1.0, label="±0%")
    ax.fill_between(lim, [v * 0.8 for v in lim], [v * 1.2 for v in lim],
                    alpha=0.08, color="gray", label="±20%")

    ax.set_xlim(lim); ax.set_ylim(lim)
    ax.set_xlabel(r"Measured $\Delta T_\mathrm{ONB}$ [K]")
    ax.set_ylabel(r"Predicted $\Delta T_\mathrm{ONB}$ [K]")
    ax.set_title(f"ONB Wall Superheat Parity — {split} split")
    ax.legend(fontsize=8, loc="upper left")
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)

    out_dir.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        path = out_dir / f"parity_dT_onb_{split}.{ext}"
        fig.savefig(path)
        print(f"  Saved: {path.relative_to(_PROJ)}")
    plt.close(fig)


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 2 evaluation pipeline")
    parser.add_argument("--config",     required=True)
    parser.add_argument("--checkpoint", default=None,
                        help="Trained model checkpoint (omit with --no-pinn)")
    parser.add_argument("--no-pinn",    action="store_true",
                        help="Skip PINN; run classical correlations only")
    parser.add_argument("--split",      default="test",
                        choices=["train", "val", "test", "all"],
                        help="Which split to evaluate (default: test)")
    parser.add_argument("--device",     default="cpu")
    args = parser.parse_args()

    cfg    = load_config(args.config)
    device = torch.device(args.device)

    # ── Resolve paths ─────────────────────────────────────────────────────────
    csv_path = Path(cfg["data"]["csv_path"])
    if not csv_path.is_absolute():
        csv_path = _PROJ / csv_path

    out_fig = _PROJ / "analysis" / "figures"
    out_tbl = _PROJ / "analysis" / "tables"
    out_fig.mkdir(parents=True, exist_ok=True)
    out_tbl.mkdir(parents=True, exist_ok=True)

    # ── Data ──────────────────────────────────────────────────────────────────
    print("\nLoading datasets...")
    train_ds, val_ds, test_ds = build_datasets(cfg)
    print(f"  train={len(train_ds)}  val={len(val_ds)}  test={len(test_ds)}")

    raw = build_eval_table((train_ds, val_ds, test_ds), csv_path)
    # Re-index to be contiguous (train → val → test order)
    raw = pd.concat([
        train_ds._df.assign(split="train"),
        val_ds._df.assign(split="val"),
        test_ds._df.assign(split="test"),
    ], ignore_index=True)

    # ── PINN predictions ──────────────────────────────────────────────────────
    pinn_dT = pinn_q = None
    if not args.no_pinn:
        if args.checkpoint is None:
            # Try default checkpoint location
            ckpt_default = (_PROJ / cfg.get("logging", {}).get("checkpoint_dir", "experiments/checkpoints")
                            / cfg.get("experiment", {}).get("name", "run") / "best_model.pt")
            if ckpt_default.is_file():
                args.checkpoint = str(ckpt_default)
                print(f"  Found checkpoint: {ckpt_default.relative_to(_PROJ)}")
            else:
                print("  [warn] No checkpoint provided/found — skipping PINN evaluation")
                args.no_pinn = True

        if not args.no_pinn:
            print("\nLoading PINN model...")
            model = build_model(cfg, device)
            ckpt_path = Path(args.checkpoint)
            if not ckpt_path.is_absolute():
                ckpt_path = _PROJ / ckpt_path
            ckpt = torch.load(ckpt_path, map_location=device, weights_only=True)
            model.load_state_dict(ckpt["model_state"])
            print(f"  Loaded: {ckpt_path.name}  val_loss={ckpt.get('val_loss', '?')}")

            pinn_dT, pinn_q = pinn_predictions(
                model, train_ds, val_ds, test_ds, cfg, device
            )
            print(f"  PINN predictions: {len(pinn_dT)} rows")

    # ── Classical correlations ─────────────────────────────────────────────────
    print("\nComputing classical correlations...")
    corr_preds = correlation_predictions(raw)
    for name, (pd_, pq) in corr_preds.items():
        n_dT = int(np.isfinite(pd_).sum())
        n_q  = int(np.isfinite(pq).sum())
        print(f"  {name:<28s}: n_dT={n_dT:3d}  n_q={n_q:3d}")

    # ── Metrics table ─────────────────────────────────────────────────────────
    print(f"\nMetrics ({args.split} split):")
    df_metrics = build_metrics_table(raw, corr_preds, pinn_dT, pinn_q, split=args.split)
    print(df_metrics.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    metrics_path = out_tbl / f"metrics_{args.split}.csv"
    df_metrics.to_csv(metrics_path, index=False, float_format="%.4f")
    print(f"\n  Saved: {metrics_path.relative_to(_PROJ)}")

    # ── Per-fluid table ───────────────────────────────────────────────────────
    df_fluid = build_per_fluid_table(raw, corr_preds, pinn_dT, pinn_q)
    fluid_path = out_tbl / "per_fluid.csv"
    df_fluid.to_csv(fluid_path, index=False, float_format="%.4f")
    print(f"  Saved: {fluid_path.relative_to(_PROJ)}")

    # ── Parity plot ───────────────────────────────────────────────────────────
    print(f"\nGenerating parity plot ({args.split} split)...")
    plot_parity(raw, corr_preds, pinn_dT, out_fig, split=args.split)

    # ── M4 Go/No-Go summary ───────────────────────────────────────────────────
    pinn_row = df_metrics[df_metrics["method"] == "PINN (Phase 2)"]
    if not pinn_row.empty:
        rmse_val = pinn_row.iloc[0]["rmse_dT_K"]
        status   = "GO ✓" if rmse_val <= 8.0 else "NO-GO ✗  (target ≤ 8 K)"
        print(f"\n  M4 Go/No-Go  PINN RMSE_ΔT ({args.split}) = {rmse_val:.2f} K  →  {status}")

    print("\nDone.")


if __name__ == "__main__":
    main()
