"""fig:uq — deep-ensemble (K=5) UQ: parity ±2σ, calibration, std vs pressure.

Loads the 5 ensemble members (phase2_v11ens_s42..s46, shared split_seed=42),
computes mean/std on the test split, and the (epistemic-only) calibration.
Also writes analysis/tables/ensemble_uq_test.csv. Uses math.erf (no scipy).
"""
from __future__ import annotations
import warnings; warnings.filterwarnings("ignore")
import math
import numpy as np, pandas as pd, torch
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader
from figlib import (PROJ, set_style, save_fig, load_dataframe)
from train import build_model, load_config
from data.dataset import collate_fn

SEEDS = [42, 43, 44, 45, 46]


def main() -> None:
    set_style()
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    ds, df = load_dataframe("test")
    loader = lambda: DataLoader(ds, batch_size=64, shuffle=False, collate_fn=collate_fn)

    preds_dT, preds_q = [], []
    for s in SEEDS:
        cfg = load_config(str(PROJ / "experiments" / "configs" / f"phase2_v11ens_s{s}.yaml"))
        m = build_model(cfg, device)
        ck = PROJ / "experiments" / "checkpoints" / f"phase2_v11ens_s{s}" / "best_model.pt"
        m.load_state_dict(torch.load(str(ck), map_location=device)["model_state"]); m.eval()
        pdT, pq = [], []
        with torch.no_grad():
            for b in loader():
                o = m(b["x_star"].to(device),
                      {k: v.to(device) for k, v in b["surface_features"].items()},
                      b["flow_numeric"].to(device))
                pdT.append((o.delta_T_onb_star.squeeze(-1) * b["dT_ref"].to(device)).cpu().numpy())
                pq.append((o.q_onb_star.squeeze(-1) * b["q_ref"].to(device)).cpu().numpy())
        preds_dT.append(np.concatenate(pdT)); preds_q.append(np.concatenate(pq))

    P_dT = np.stack(preds_dT); P_q = np.stack(preds_q)
    mean_dT, std_dT = P_dT.mean(0), P_dT.std(0)
    has_dT = (df["delta_T_onb_K"] > 0).values
    true_dT = df["delta_T_onb_K"].values

    out = df.copy()
    out["ens_mean_dT"] = mean_dT; out["ens_std_dT"] = std_dT
    out["ens_mean_q_kW"] = P_q.mean(0) / 1e3; out["ens_std_q_kW"] = P_q.std(0) / 1e3
    (PROJ / "analysis" / "tables").mkdir(parents=True, exist_ok=True)
    out.to_csv(PROJ / "analysis" / "tables" / "ensemble_uq_test.csv", index=False)

    t = true_dT[has_dT]; mu = mean_dT[has_dT]; sd = std_dT[has_dT]
    err = np.abs(mu - t)
    cov = lambda scale: np.mean(err <= scale * sd)
    scales = np.linspace(0.3, 10, 400)
    s68 = scales[int(np.argmin([abs(cov(s) - 0.68) for s in scales]))]
    gauss = lambda k: math.erf(k / math.sqrt(2))

    fig, ax = plt.subplots(1, 3, figsize=(16, 5))
    lo, hi = 1, t.max() * 1.3
    ax[0].fill_between([lo, hi], [lo * 0.8, hi * 0.8], [lo * 1.2, hi * 1.2], color="gray", alpha=0.12, label="±20%")
    ax[0].plot([lo, hi], [lo, hi], "k--", lw=1)
    ax[0].errorbar(t, mu, yerr=2 * sd, fmt="o", ms=5, color="#2196F3", ecolor="#90CAF9",
                   elinewidth=1.2, capsize=2, alpha=0.85, label="ens. mean ±2σ")
    ax[0].set_xscale("log"); ax[0].set_yscale("log"); ax[0].set_xlim(lo, hi); ax[0].set_ylim(lo, hi)
    ax[0].set_aspect("equal"); ax[0].set_xlabel("Measured $\\Delta T_{ONB}$ [K]")
    ax[0].set_ylabel("Predicted $\\Delta T_{ONB}$ [K]")
    ax[0].set_title("(a)", loc="left", fontweight="bold", fontsize=12); ax[0].legend(fontsize=8, loc="upper left")

    ks = np.linspace(0.1, 3.5, 40)
    ax[1].plot(ks, [gauss(k) for k in ks], "k--", lw=1, label="Gaussian ideal")
    ax[1].plot(ks, [cov(k) for k in ks], "o-", ms=3, color="#E91E63", label="epistemic only")
    ax[1].plot(ks, [cov(k * s68) for k in ks], "s-", ms=3, color="#4CAF50", label=f"recalibrated (×{s68:.1f})")
    ax[1].set_xlabel("$k$  (interval half-width in units of $\\sigma$)"); ax[1].set_ylabel("Observed coverage")
    ax[1].set_title("(b)", loc="left", fontweight="bold", fontsize=12); ax[1].legend(fontsize=8); ax[1].set_ylim(0, 1.02)

    ax[2].scatter(df.loc[has_dT, "P_kPa"] / 1000, sd, s=32, c="#FF9800", alpha=0.85, edgecolor="none")
    ax[2].set_xscale("log"); ax[2].set_xlabel("Pressure [MPa]")
    ax[2].set_ylabel("Epistemic std $\\Delta T$ [K]"); ax[2].set_title("(c)", loc="left", fontweight="bold", fontsize=12)
    save_fig(fig, "ensemble_uq")
    print(f"recalibration factor ≈ {s68:.1f};  mean std {sd.mean():.3f} K;  "
          f"1σ cov {cov(1)*100:.0f}%  2σ cov {cov(2)*100:.0f}%")


if __name__ == "__main__":
    main()
