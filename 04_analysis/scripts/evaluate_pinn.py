"""
phase3_best.pt 체크포인트로 학습된 PINN을 onb_dataset.csv(43 ONB) 전체에 대해 평가.

생성:
  - 04_analysis/tables/pinn_metrics.md   : 전체/유체별/표면별 통계
  - 04_analysis/figures/pinn_parity.png  : PINN parity plot
  - 04_analysis/figures/correlations_with_pinn_parity.png : 6-panel (5 상관식 + PINN)
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import yaml
import matplotlib.pyplot as plt

# Project paths
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "03_model"))

from src.model.pinn import PoolBoilingPINN  # type: ignore
from src.training.dataset import OnbDataset, onb_collate_fn  # type: ignore
from src.utils.nondim import scales_for  # type: ignore
from torch.utils.data import DataLoader


def load_model_from_checkpoint(ckpt_path: Path, config: dict) -> PoolBoilingPINN:
    model_cfg = config.get("model", {})
    pinn_cfg = model_cfg.get("pinn", {})
    enc_cfg = model_cfg.get("surface_encoder", {})

    model = PoolBoilingPINN(
        conditioning=model_cfg.get("conditioning", "concat"),
        latent_dim=int(enc_cfg.get("latent_dim", 16)),
        hidden_dim=int(pinn_cfg.get("hidden_dim", 64)),
        n_layers=int(pinn_cfg.get("n_layers", 5)),
        spatial_dim=1,
    )
    ckpt = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    model.load_state_dict(ckpt["model_state"])
    model.eval()
    return model


@torch.no_grad()
def predict_all(model: PoolBoilingPINN, csv_path: Path) -> pd.DataFrame:
    ds = OnbDataset(csv_path, skip_unsupported_fluids=True)
    loader = DataLoader(ds, batch_size=1, shuffle=False, collate_fn=onb_collate_fn)

    rows = []
    for batch in loader:
        B = batch["delta_T_wall_star"].shape[0]
        surface_batch = {
            "numeric": batch["surface_numeric"],
            "category_id": batch["category_id"],
        }
        z_query = torch.zeros(B, 1)
        # operating = (q_star, ΔT_sub_star) — must match training-time format.
        q_star_b   = batch["q_flux_star"].unsqueeze(-1)
        dTs_star_b = batch["delta_T_sub_star"].unsqueeze(-1)
        operating = torch.cat([q_star_b, dTs_star_b], dim=-1)
        out = model(z_query, surface_batch, operating)

        fluid = batch["fluid"][0]
        P_pa = float(batch["pressure_pa"][0])
        sc = scales_for(fluid, P=P_pa)
        dT_ref = sc.delta_T_ref

        pred_dT_star = float(out.delta_T_onb_star[0].item())
        obs_dT_star = float(batch["delta_T_wall_star"][0].item())
        pred_dT_K = pred_dT_star * dT_ref
        obs_dT_K = obs_dT_star * dT_ref
        q_flux = float(batch["q_flux_star"][0].item()) * sc.q_ref

        rows.append({
            "source_paper": batch["source_paper"][0],
            "figure_ref": batch["figure_ref"][0],
            "surface_id": batch["surface_id"][0],
            "fluid": fluid,
            "q_flux_W_m2": q_flux,
            "obs_delta_T_K": obs_dT_K,
            "pred_delta_T_K": pred_dT_K,
            "error_K": pred_dT_K - obs_dT_K,
            "abs_error_K": abs(pred_dT_K - obs_dT_K),
        })
    return pd.DataFrame(rows)


def compute_metrics(obs: np.ndarray, pred: np.ndarray) -> dict[str, float]:
    err = pred - obs
    rmse = float(np.sqrt(np.mean(err**2)))
    mae = float(np.mean(np.abs(err)))
    ss_res = float(np.sum(err**2))
    ss_tot = float(np.sum((obs - np.mean(obs))**2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    mre = float(np.mean(np.abs(err) / np.maximum(np.abs(obs), 1e-6)) * 100.0)
    return {"RMSE_K": rmse, "MAE_K": mae, "R2": r2, "MRE_pct": mre, "n": int(len(obs))}


def metrics_to_markdown_row(name: str, m: dict[str, float]) -> str:
    return (
        f"| {name} | {m['RMSE_K']:.2f} | {m['MAE_K']:.2f} | "
        f"{m['R2']:.3f} | {m['MRE_pct']:.1f} | {m['n']} |"
    )


def write_metrics(df: pd.DataFrame, out_md: Path) -> None:
    overall = compute_metrics(df["obs_delta_T_K"].to_numpy(), df["pred_delta_T_K"].to_numpy())

    lines = ["# PINN baseline_phaseA 평가 지표\n"]
    lines.append("학습 체크포인트: `03_model/checkpoints/baseline_phaseA/phase3_best.pt`\n")
    lines.append(f"전체 ONB 데이터: **{overall['n']}** (FC-77 5개 제외)\n")
    lines.append("\n## 전체\n")
    lines.append("| 모델 | RMSE [K] | MAE [K] | R² | MRE [%] | n |")
    lines.append("|---|---|---|---|---|---|")
    lines.append(metrics_to_markdown_row("PINN (phase3_best)", overall))

    lines.append("\n## 유체별\n")
    lines.append("| 유체 | RMSE [K] | MAE [K] | R² | MRE [%] | n |")
    lines.append("|---|---|---|---|---|---|")
    for fluid in sorted(df["fluid"].unique()):
        sub = df[df["fluid"] == fluid]
        m = compute_metrics(sub["obs_delta_T_K"].to_numpy(), sub["pred_delta_T_K"].to_numpy())
        lines.append(metrics_to_markdown_row(fluid, m))

    lines.append("\n## 소스 논문별\n")
    lines.append("| 논문 | RMSE [K] | MAE [K] | R² | MRE [%] | n |")
    lines.append("|---|---|---|---|---|---|")
    for paper in sorted(df["source_paper"].unique()):
        sub = df[df["source_paper"] == paper]
        m = compute_metrics(sub["obs_delta_T_K"].to_numpy(), sub["pred_delta_T_K"].to_numpy())
        lines.append(metrics_to_markdown_row(paper, m))

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(lines) + "\n")
    print(f"[write_metrics] → {out_md}")


def plot_parity(df: pd.DataFrame, out_png: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 6), dpi=120)
    obs = df["obs_delta_T_K"].to_numpy()
    pred = df["pred_delta_T_K"].to_numpy()
    vmax = float(max(obs.max(), pred.max())) * 1.1
    vmin = 0.0

    fluids = df["fluid"].unique()
    cmap = {"water": "tab:blue", "R-123": "tab:orange", "R-134a": "tab:green"}
    for fluid in fluids:
        sub = df[df["fluid"] == fluid]
        ax.scatter(
            sub["obs_delta_T_K"], sub["pred_delta_T_K"],
            label=f"{fluid} (n={len(sub)})",
            c=cmap.get(fluid, "gray"), s=40, alpha=0.8, edgecolors="k", linewidths=0.5,
        )

    ax.plot([vmin, vmax], [vmin, vmax], "k--", lw=1, label="parity")
    for k, ls in [(1.3, ":"), (1.5, "-.")]:
        ax.plot([vmin, vmax], [vmin * k, vmax * k], color="gray", ls=ls, lw=0.8)
        ax.plot([vmin, vmax], [vmin / k, vmax / k], color="gray", ls=ls, lw=0.8,
                label=f"±{int((k-1)*100)}%" if k == 1.3 else f"±{int((k-1)*100)}%")
    ax.set_xlim(vmin, vmax)
    ax.set_ylim(vmin, vmax)
    ax.set_xlabel(r"Observed $\Delta T_{ONB}$ [K]")
    ax.set_ylabel(r"PINN-predicted $\Delta T_{ONB}$ [K]")
    overall = compute_metrics(obs, pred)
    ax.set_title(
        f"PINN parity — RMSE={overall['RMSE_K']:.2f} K  "
        f"MAE={overall['MAE_K']:.2f} K  R²={overall['R2']:.3f}  n={overall['n']}"
    )
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(True, alpha=0.3)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_png)
    plt.close(fig)
    print(f"[plot_parity] → {out_png}")


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-name", default="baseline_phaseA",
                    help="run name (e.g. baseline_phaseA, baseline_phaseB)")
    args = ap.parse_args()
    run_name = args.run_name

    config_path = ROOT / "03_model" / "configs" / f"{run_name}.yaml"
    ckpt_path = ROOT / "03_model" / "checkpoints" / run_name / "phase3_best.pt"
    csv_path = ROOT / "02_data" / "processed" / "onb_dataset.csv"

    config = yaml.safe_load(config_path.read_text())
    print(f"[main] run_name: {run_name}")
    print(f"[main] loading checkpoint: {ckpt_path}")
    model = load_model_from_checkpoint(ckpt_path, config)
    print(f"[main] model params: {sum(p.numel() for p in model.parameters()):,}")

    print(f"[main] predicting on full dataset: {csv_path}")
    df = predict_all(model, csv_path)

    # Save predictions CSV
    pred_csv = ROOT / "04_analysis" / "tables" / f"pinn_predictions_{run_name}.csv"
    pred_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(pred_csv, index=False)
    print(f"[main] predictions saved → {pred_csv}")

    # Metrics
    overall = compute_metrics(df["obs_delta_T_K"].to_numpy(), df["pred_delta_T_K"].to_numpy())
    print(f"\n=== {run_name} 전체 평가 (n={overall['n']}) ===")
    print(f"  RMSE = {overall['RMSE_K']:.3f} K")
    print(f"  MAE  = {overall['MAE_K']:.3f} K")
    print(f"  R²   = {overall['R2']:.4f}")
    print(f"  MRE  = {overall['MRE_pct']:.2f} %")

    write_metrics(df, ROOT / "04_analysis" / "tables" / f"pinn_metrics_{run_name}.md")
    plot_parity(df, ROOT / "04_analysis" / "figures" / f"pinn_parity_{run_name}.png")


if __name__ == "__main__":
    main()
