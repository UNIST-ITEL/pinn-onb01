"""fig:arch — surface- and flow-conditioned PINN architecture schematic.

Pure matplotlib block diagram (no model). Box coordinates are manual; adjust the
box()/arrow() calls to restyle.
"""
from __future__ import annotations
import warnings; warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from figlib import set_style, save_fig


def main() -> None:
    set_style()
    fig, ax = plt.subplots(figsize=(11, 5.2)); ax.set_xlim(0, 15); ax.set_ylim(0, 8); ax.axis("off")

    def box(x, y, w, h, txt, fc, fs=9.5, bold=False):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.12",
                     fc=fc, ec="#333", lw=1.3))
        ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=fs,
                fontweight="bold" if bold else "normal", zorder=5)

    def arrow(x1, y1, x2, y2, c="#333", lw=1.6, style="-|>"):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=14,
                     lw=lw, color=c, shrinkA=2, shrinkB=2))

    C_in, C_enc, C_frozen, C_back, C_head, C_loss = "#E3F2FD", "#BBDEFB", "#C8E6C9", "#FFE0B2", "#F8BBD0", "#ECEFF1"
    box(0.2, 6.1, 3.0, 1.3, "Surface descriptor $\\mathbf{s}$\n$R_a,\\ \\theta,\\ $category", C_in, fs=9)
    box(0.2, 3.4, 3.0, 1.5, "Flow descriptor $\\mathbf{f}$ (11 ch)\nRe, G, Bo, We, $\\Delta T_{sub}$,\n$D_h$, geom., $\\mathbf{P_r}$", C_in, fs=8.5)
    box(0.2, 1.5, 3.0, 1.0, "axial $x^{*}\\in[0,1]$", C_in, fs=9)
    box(4.0, 6.0, 3.2, 1.5, "Surface Encoder\n(Phase-1, FROZEN)", C_frozen, fs=9, bold=True)
    box(4.0, 3.5, 3.2, 1.4, "Flow Encoder\n(new)", C_enc, fs=9, bold=True)
    ax.text(5.6, 5.78, "transfer-learned", ha="center", fontsize=7.5, style="italic", color="#2E7D32")
    box(7.9, 6.2, 1.7, 1.1, "$\\mathbf{z}_s$\n(16)", C_enc, fs=9)
    box(7.9, 3.7, 1.7, 1.1, "$\\mathbf{z}_f$\n(8)", C_enc, fs=9)
    box(10.3, 3.7, 2.4, 3.6, "FiLM-conditioned\nMLP backbone\n(6 layers, in $x^{*}$)", C_back, fs=9, bold=True)
    box(13.0, 6.2, 1.8, 1.0, "$\\Delta T_{ONB}^{*}$", C_head, fs=10, bold=True)
    box(13.0, 4.9, 1.8, 1.0, "$q_{ONB}^{*}$", C_head, fs=10, bold=True)
    box(13.0, 3.6, 1.8, 1.0, "$T^{*}(x^{*})$", C_head, fs=9)
    arrow(3.2, 6.75, 4.0, 6.75); arrow(3.2, 4.15, 4.0, 4.2)
    arrow(7.2, 6.75, 7.9, 6.75); arrow(7.2, 4.2, 7.9, 4.25)
    arrow(9.6, 6.75, 10.3, 6.2, c="#E65100"); arrow(9.6, 4.25, 10.3, 4.6, c="#E65100")
    ax.text(9.95, 5.55, "FiLM", ha="center", fontsize=7.5, color="#E65100")
    arrow(3.2, 2.0, 10.3, 3.9)
    arrow(12.7, 6.0, 13.0, 6.7); arrow(12.7, 5.5, 13.0, 5.4); arrow(12.7, 4.6, 13.0, 4.1)
    box(4.0, 0.15, 8.7, 1.0, "Loss:  data ($\\Delta T,q$)  +  flow-aware Hsu collocation  "
        "+  one-sided Hsu coupling ($\\Delta T^{*}\\!\\geq\\! C\\sqrt{q^{*}}$)  +  monotonicity (Re,G,$\\Delta T_{sub}$)",
        C_loss, fs=8.2)
    arrow(13.9, 6.2, 13.9, 1.15, c="#777", lw=1.0); arrow(8.4, 3.6, 8.4, 1.15, c="#777", lw=1.0)
    ax.set_title("Surface- and flow-conditioned PINN architecture", fontsize=11, fontweight="bold", pad=8)
    save_fig(fig, "architecture")


if __name__ == "__main__":
    main()
