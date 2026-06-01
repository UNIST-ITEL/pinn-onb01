"""fig:ptrend — measured vs predicted ΔT_ONB along pressure sweeps (v11).

Shows the Kuang (G=500, q=300) and Wang (G=1000, q=200) pressure sweeps; the
residual high-P uptick in the Kuang prediction is the documented Pattern-C gap.
"""
from __future__ import annotations
import warnings; warnings.filterwarnings("ignore")
import numpy as np
import matplotlib.pyplot as plt
from figlib import set_style, save_fig, load_v11, load_dataframe, predict_dT


def main() -> None:
    set_style()
    model, device, _ = load_v11()
    ds, df = load_dataframe("all")
    df = df.copy(); df["pred"] = predict_dT(model, device, ds)

    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    sweeps = [("wang2024", 1000, 2e5, "Wang G=1000, q=200", "#1565C0", "o"),
              ("kuang2025", 500, 3e5, "Kuang G=500, q=300", "#C62828", "s")]
    for pid, G, q, lab, c, mk in sweeps:
        d = df[(df.paper_id == pid) & (df.delta_T_onb_K > 0)
               & (np.abs(df.G_kg_m2s - G) < 1) & (np.abs(df.q_onb_W_m2 - q) < 1e4)].sort_values("P_kPa")
        if not len(d):
            continue
        ax.plot(d.P_kPa / 1000, d.delta_T_onb_K, mk + "-", color=c, ms=7, lw=1.6,
                label=f"{lab} (measured)")
        ax.plot(d.P_kPa / 1000, d.pred, mk + "--", color=c, ms=6, mfc="white", lw=1.3,
                label=f"{lab} (PINN v11)")
    ax.set_xscale("log"); ax.set_xlabel("Pressure $P$ [MPa]"); ax.set_ylabel("$\\Delta T_{ONB}$ [K]")
    ax.set_title("Pressure trend recovery: $P\\!\\uparrow\\Rightarrow\\Delta T_{ONB}\\!\\downarrow$ (trend #4)")
    ax.legend(fontsize=8.5, loc="upper right")
    ax.text(0.03, 0.04,
            "corr($P$, predicted $\\Delta T$):  +0.01 (no $P$ feature) $\\rightarrow$ $-$0.69 (v11);  measured $-$0.57",
            transform=ax.transAxes, fontsize=8, va="bottom",
            bbox=dict(boxstyle="round", fc="#FFF9C4", ec="#999", alpha=0.9))
    save_fig(fig, "fig_pressure_trend")


if __name__ == "__main__":
    main()
