"""fig:dist — marginal distributions of the curated ONB dataset (6 panels)."""
from __future__ import annotations
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from figlib import CSV, set_style, save_fig


def _hist(ax, series, xlabel, log=False, bins=20):
    v = series.replace(-1, np.nan).dropna()
    if log:
        v = v[v > 0]
        ax.set_xscale("log")
        bins = np.logspace(np.log10(v.min()), np.log10(v.max()), bins)
    ax.hist(v, bins=bins, color="#42A5F5", edgecolor="k", lw=0.4)
    ax.set_xlabel(xlabel); ax.set_ylabel("count"); ax.set_title(f"n={len(v)}", fontsize=9)


def main() -> None:
    set_style()
    df = pd.read_csv(CSV)
    df = df[(df.delta_T_onb_K > 0) | (df.q_onb_W_m2 > 0)].copy()
    fig, axs = plt.subplots(2, 3, figsize=(13, 7))
    _hist(axs[0, 0], df.P_kPa / 1000, "Pressure [MPa]", log=True)
    _hist(axs[0, 1], df.D_h_mm, "$D_h$ [mm]", log=True)
    _hist(axs[0, 2], df.G_kg_m2s, "Mass flux G [kg m$^{-2}$s$^{-1}$]")
    _hist(axs[1, 0], df.delta_T_sub_K, "Inlet/local subcooling $\\Delta T_{sub}$ [K]")
    _hist(axs[1, 1], df.delta_T_onb_K, "$\\Delta T_{ONB}$ [K]")
    _hist(axs[1, 2], df.q_onb_W_m2 / 1e3, "$q''_{ONB}$ [kW m$^{-2}$]", log=True)
    fig.tight_layout()
    save_fig(fig, "fig_data_distributions")


if __name__ == "__main__":
    main()
