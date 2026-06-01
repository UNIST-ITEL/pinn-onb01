"""fig:coverage — parameter-space coverage map (D_h vs P, size~G, colour=source)."""
from __future__ import annotations
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from figlib import CSV, set_style, save_fig, SOURCE_LABELS


def main() -> None:
    set_style()
    df = pd.read_csv(CSV)
    df = df[(df.delta_T_onb_K > 0) | (df.q_onb_W_m2 > 0)].copy()
    srcs = list(SOURCE_LABELS)
    colors = cm.tab10(np.linspace(0, 1, len(srcs)))

    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    for s, c in zip(srcs, colors):
        d = df[df.paper_id == s]
        if not len(d):
            continue
        P = d.P_kPa.replace(-1, np.nan) / 1000
        G = d.G_kg_m2s.replace(-1, np.nan).fillna(300)
        ax.scatter(d.D_h_mm, P, s=np.clip(G / 8, 8, 120), color=c, alpha=0.65,
                   edgecolor="k", lw=0.3, label=SOURCE_LABELS[s])
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("Hydraulic diameter $D_h$ [mm]"); ax.set_ylabel("Pressure $P$ [MPa]")
    ax.set_title("Dataset coverage (marker size $\\propto$ mass flux $G$)")
    ax.legend(fontsize=7.5, ncol=2, loc="lower right", framealpha=0.9)
    ax.axhspan(0.09, 0.25, color="gray", alpha=0.06)
    ax.annotate("micro-\nchannel", (0.36, 0.13), fontsize=7.5, color="#555")
    ax.annotate("nuclear\nhigh-P", (4.5, 13), fontsize=7.5, color="#B71C1C")
    save_fig(fig, "fig_coverage_map")


if __name__ == "__main__":
    main()
