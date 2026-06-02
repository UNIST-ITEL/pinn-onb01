"""fig:parity — log-scale ΔT and q parity on the test split (v11).

Writes two files: parity_dT_onb_test and parity_q_onb_test.
"""
from __future__ import annotations
import warnings; warnings.filterwarnings("ignore")
import numpy as np, torch
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader
from figlib import set_style, save_fig, load_v11, load_dataframe
from data.dataset import collate_fn


def _log_parity(ax, true, pred, label, color="#2196F3"):
    lo = min(true.min(), pred.min()) * 0.7
    hi = max(true.max(), pred.max()) * 1.4
    t = np.array([lo, hi])
    ax.fill_between(t, t * 0.8, t * 1.2, color="gray", alpha=0.12, label="±20%")
    ax.plot(t, t, "k--", lw=1.0, label="1:1")
    ax.scatter(true, pred, s=28, color=color, alpha=0.75, zorder=3, label=label)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi); ax.set_aspect("equal")
    ax.legend(fontsize=8.5, loc="upper left")


def _metrics(p, t):
    return (np.sqrt(np.mean((p - t) ** 2)), np.mean(np.abs(p - t)),
            1 - np.sum((p - t) ** 2) / np.sum((t - t.mean()) ** 2), len(p))


def main() -> None:
    set_style()
    model, device, _ = load_v11()
    ds, _ = load_dataframe("test")
    pq, tq, pdT, tdT = [], [], [], []
    with torch.no_grad():
        for b in DataLoader(ds, batch_size=64, shuffle=False, collate_fn=collate_fn):
            o = model(b["x_star"].to(device),
                      {k: v.to(device) for k, v in b["surface_features"].items()},
                      b["flow_numeric"].to(device))
            qr, dr = b["q_ref"].to(device), b["dT_ref"].to(device)
            p_q = (o.q_onb_star.squeeze(-1) * qr).cpu().numpy()
            p_dT = (o.delta_T_onb_star.squeeze(-1) * dr).cpu().numpy()
            mq = (b["has_q"] & torch.isfinite(b["q_onb_W_m2"])).numpy().astype(bool)
            mdT = (b["has_dT"] & torch.isfinite(b["delta_T_onb_K"])).numpy().astype(bool)
            if mq.any():
                pq.append(p_q[mq]); tq.append(b["q_onb_W_m2"].numpy()[mq])
            if mdT.any():
                pdT.append(p_dT[mdT]); tdT.append(b["delta_T_onb_K"].numpy()[mdT])
    pq = np.concatenate(pq) / 1e3; tq = np.concatenate(tq) / 1e3
    pdT = np.concatenate(pdT); tdT = np.concatenate(tdT)

    r, m, r2, n = _metrics(pdT, tdT)
    fig, ax = plt.subplots(figsize=(6, 6))
    _log_parity(ax, tdT, pdT, f"PINN\nRMSE={r:.2f} K  MAE={m:.2f} K\nR²={r2:.3f}  (n={n})")
    ax.set_xlabel("Measured $\\Delta T_{ONB}$ [K]"); ax.set_ylabel("Predicted $\\Delta T_{ONB}$ [K]")
    ax.set_title("(a)", loc="left", fontweight="bold", fontsize=12)
    save_fig(fig, "parity_dT_onb_test")

    r, m, r2, n = _metrics(pq, tq)
    fig, ax = plt.subplots(figsize=(6, 6))
    _log_parity(ax, tq, pq, f"PINN\nRMSE={r:.0f} kW m$^{{-2}}$  MAE={m:.0f} kW m$^{{-2}}$\nR²={r2:.3f}  (n={n})",
                color="#E91E63")
    ax.set_xlabel("Measured $q''_{ONB}$ [kW m$^{-2}$]"); ax.set_ylabel("Predicted $q''_{ONB}$ [kW m$^{-2}$]")
    ax.set_title("(b)", loc="left", fontweight="bold", fontsize=12)
    save_fig(fig, "parity_q_onb_test")


if __name__ == "__main__":
    main()
