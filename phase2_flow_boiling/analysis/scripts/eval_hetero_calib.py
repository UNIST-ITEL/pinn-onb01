"""Evaluate the single heteroscedastic model's calibration on the test split.

Predicted aleatoric sigma = exp(0.5 * log_var_dT) * dT_ref  [K].
Coverage(k) = fraction of |pred - meas| <= k * sigma. Compare to the ensemble's
epistemic-only under-coverage (28% / 42% at 1/2 sigma; ideal 68% / 95%).
"""
from __future__ import annotations
import sys, math
from pathlib import Path
import numpy as np, torch
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "experiments" / "src"))
from torch.utils.data import DataLoader
from train import build_model, load_config
from data.dataset import FlowBoilingDataset, collate_fn

PROJ = Path(__file__).resolve().parents[2]
CFG  = PROJ / "experiments" / "configs" / "phase2_hetero.yaml"
CKPT = PROJ / "experiments" / "checkpoints" / "phase2_hetero" / "best_model.pt"


def main() -> None:
    dev = torch.device("cpu")
    cfg = load_config(str(CFG))
    model = build_model(cfg, dev)
    state = torch.load(str(CKPT), map_location=dev)["model_state"]
    model.load_state_dict(state); model.eval()

    ds = FlowBoilingDataset(str(PROJ / cfg["data"]["csv_path"]), split="test", seed=42)
    pred, true, sig = [], [], []
    with torch.no_grad():
        for b in DataLoader(ds, batch_size=64, shuffle=False, collate_fn=collate_fn):
            o = model(b["x_star"], {k: v for k, v in b["surface_features"].items()},
                      b["flow_numeric"])
            dT_ref = b["dT_ref"]
            pdt = (o.delta_T_onb_star.squeeze(-1) * dT_ref).numpy()
            sg  = (torch.exp(0.5 * o.log_var_dT.squeeze(-1)) * dT_ref).numpy()
            m   = (b["has_dT"] & torch.isfinite(b["delta_T_onb_K"])).numpy().astype(bool)
            pred.append(pdt[m]); sig.append(sg[m])
            true.append(b["delta_T_onb_K"].numpy()[m])
    pred = np.concatenate(pred); true = np.concatenate(true); sig = np.concatenate(sig)
    err = np.abs(pred - true)
    cov = lambda k: float(np.mean(err <= k * sig))
    rmse = float(np.sqrt(np.mean((pred - true) ** 2)))
    print(f"n_test_dT = {len(err)}")
    print(f"RMSE_dT   = {rmse:.3f} K")
    print(f"mean sigma = {sig.mean():.3f} K  (range {sig.min():.2f}–{sig.max():.2f})")
    print(f"1-sigma coverage = {cov(1)*100:.0f}%  (ideal 68%)")
    print(f"2-sigma coverage = {cov(2)*100:.0f}%  (ideal 95%)")
    print(f"3-sigma coverage = {cov(3)*100:.0f}%  (ideal 99.7%)")
    # mean negative log-likelihood (lower is better-calibrated)
    nll = float(np.mean(0.5 * ((err / sig) ** 2 + np.log(2 * math.pi * sig ** 2))))
    print(f"mean Gaussian NLL = {nll:.3f}")


if __name__ == "__main__":
    main()
