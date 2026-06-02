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

    # Row centres: surface 6.7, flow 4.3, axial 2.1 — every box is snapped to these.
    CY_S, CY_F, CY_X = 6.7, 4.3, 2.1

    # ── column 1: inputs ──
    box(0.3, CY_S - 0.65, 3.0, 1.3, "Surface descriptor $\\mathbf{s}$\n$R_a,\\ \\theta,\\ $category", C_in, fs=9)
    box(0.3, CY_F - 0.85, 3.0, 1.7, "Flow descriptor $\\mathbf{f}$ (11 ch)\nRe, G, Bo, We, $\\Delta T_{sub}$,\n$D_h$, geom., $\\mathbf{P_r}$", C_in, fs=8.5)
    box(0.3, CY_X - 0.5, 3.0, 1.0, "axial $x^{*}\\in[0,1]$", C_in, fs=9)

    # ── column 2: encoders (equal height, row-centred). Reader-facing labels only:
    #    surface encoder is transfer-learned + frozen, flow encoder is trained. ──
    bstyle = "round,pad=0.04,rounding_size=0.12"
    ax.add_patch(FancyBboxPatch((4.0, CY_S - 0.7), 3.2, 1.4, boxstyle=bstyle, fc=C_frozen, ec="#333", lw=1.3))
    ax.text(5.6, CY_S + 0.24, "Surface Encoder", ha="center", va="center", fontsize=9, fontweight="bold")
    ax.text(5.6, CY_S - 0.26, "transfer-learned, frozen", ha="center", va="center",
            fontsize=7.5, style="italic", color="#2E7D32")
    ax.add_patch(FancyBboxPatch((4.0, CY_F - 0.7), 3.2, 1.4, boxstyle=bstyle, fc=C_enc, ec="#333", lw=1.3))
    ax.text(5.6, CY_F + 0.24, "Flow Encoder", ha="center", va="center", fontsize=9, fontweight="bold")
    ax.text(5.6, CY_F - 0.26, "trained from scratch", ha="center", va="center",
            fontsize=7.5, style="italic", color="#1565C0")

    # ── column 3: latents ──
    box(7.9, CY_S - 0.55, 1.7, 1.1, "$\\mathbf{z}_s$\n(16)", C_enc, fs=9)
    box(7.9, CY_F - 0.55, 1.7, 1.1, "$\\mathbf{z}_f$\n(8)", C_enc, fs=9)

    # ── column 4: backbone (spans both rows) ──
    box(10.3, 3.5, 2.4, 3.8, "FiLM-conditioned\nMLP backbone\n(6 layers, in $x^{*}$)", C_back, fs=9, bold=True)

    # ── column 5: heads (centres 6.7 / 5.4 / 4.1) ──
    box(13.1, 6.2, 1.7, 1.0, "$\\Delta T_{ONB}^{*}$", C_head, fs=10, bold=True)
    box(13.1, 4.9, 1.7, 1.0, "$q_{ONB}^{*}$", C_head, fs=10, bold=True)
    box(13.1, 3.6, 1.7, 1.0, "$T^{*}(x^{*})$", C_head, fs=9)

    # ── forward arrows (horizontal within a row) ──
    arrow(3.3, CY_S, 4.0, CY_S); arrow(3.3, CY_F, 4.0, CY_F)          # inputs → encoders
    arrow(7.2, CY_S, 7.9, CY_S); arrow(7.2, CY_F, 7.9, CY_F)          # encoders → latents
    arrow(9.6, CY_S, 10.3, 6.3, c="#E65100"); arrow(9.6, CY_F, 10.3, 4.5, c="#E65100")  # FiLM conditioning
    arrow(3.3, CY_X, 10.3, 3.7)                                        # axial x* → backbone
    arrow(12.7, 6.4, 13.1, 6.7); arrow(12.7, 5.4, 13.1, 5.4); arrow(12.7, 4.4, 13.1, 4.1)  # backbone → heads

    # ── training objective (right-aligned to the heads' right edge x=14.8) ──
    lx, ly, lw, lh = 7.8, 0.1, 7.0, 1.6
    ax.add_patch(FancyBboxPatch((lx, ly), lw, lh, boxstyle="round,pad=0.04,rounding_size=0.12",
                 fc=C_loss, ec="#333", lw=1.3))
    ax.text(lx + lw / 2, ly + lh - 0.34, "Training objective", ha="center", va="center",
            fontsize=9, fontweight="bold")
    ax.text(lx + lw / 2, ly + 0.55,
            "data ($\\Delta T$, $q$)  +  flow-aware Hsu collocation\n"
            "+ one-sided Hsu coupling ($\\Delta T^{*}\\!\\geq\\!C\\sqrt{q^{*}}$)\n"
            "+ monotonicity (Re, G, $\\Delta T_{sub}$)",
            ha="center", va="center", fontsize=8)

    # ── training loop: outputs → objective (solid); gradients → trainable weights (dashed) ──
    ax.add_patch(FancyArrowPatch((13.9, 3.55), (13.9, 1.7), arrowstyle="-|>",
                 mutation_scale=13, lw=1.3, color="#777", shrinkA=2, shrinkB=2))
    ax.text(13.7, 2.6, "predictions", ha="right", va="center", fontsize=7, color="#666")
    ax.add_patch(FancyArrowPatch((9.5, 1.7), (11.0, 3.5), arrowstyle="-|>",
                 mutation_scale=12, lw=1.2, color="#9E9E9E", linestyle=(0, (4, 3)),
                 shrinkA=2, shrinkB=2))
    ax.text(10.55, 2.55, "backprop\n(Adam$\\to$L-BFGS)", ha="left", va="center",
            fontsize=7, color="#9E9E9E")
    save_fig(fig, "architecture")


if __name__ == "__main__":
    main()
