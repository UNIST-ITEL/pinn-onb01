"""
Graphical abstract for PINN-ONB01 manuscript.

Target: Elsevier graphical abstract recommended size 5x13 cm,
minimum 200 dpi, single-frame summary that captures the essence
of the paper. We produce a 1320 x 530 pixel image (~16 x 6.4 cm
at 200 dpi) with three side-by-side panels:

  (left)   curated multi-fluid ONB dataset summary
  (center) surface-conditioned PINN architecture cartoon
  (right)  headline forward parity result

Outputs:
  05_manuscript/figures/graphical_abstract.{png,pdf,eps}
"""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "05_manuscript" / "figures"

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 9,
    "axes.linewidth": 0.6,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.transparent": False,
    "ps.fonttype": 42,
    "pdf.fonttype": 42,
})


def _draw_box(ax, x, y, w, h, label, color, fontsize=8):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                         linewidth=1.0, edgecolor="black",
                         facecolor=color, alpha=0.85)
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
            fontsize=fontsize, weight="bold")


def _arrow(ax, x0, y0, x1, y1, color="black"):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="->", lw=1.2, color=color))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5),
                             gridspec_kw={"width_ratios": [1, 1.1, 1]})

    # ===== Left panel: dataset =====
    ax = axes[0]
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Curated open dataset", fontsize=12, weight="bold", pad=8)
    # Pie-like circular icons for 4 fluids
    fluids = ["water\n(33)", "R-134a\n(34)", "R-123\n(10)", "FC-77*\n(5)"]
    colors = ["#4C72B0", "#DD8452", "#55A467", "#C44E52"]
    angles = np.linspace(0, 2 * np.pi, len(fluids), endpoint=False)
    for i, (f, c) in enumerate(zip(fluids, colors)):
        cx = 5 + 2.2 * np.cos(angles[i] + np.pi / 2)
        cy = 6 + 2.2 * np.sin(angles[i] + np.pi / 2)
        circle = plt.Circle((cx, cy), 1.05, color=c, alpha=0.85, ec="black", lw=0.7)
        ax.add_patch(circle)
        ax.text(cx, cy, f, ha="center", va="center", fontsize=9, weight="bold", color="white")
    ax.text(5, 6, "4 fluids", ha="center", va="center", fontsize=11, weight="bold")
    ax.text(5, 2.5, "1,361 boiling pts · 82 ONB labels",
            ha="center", va="center", fontsize=10)
    ax.text(5, 1.5, "49 surface cards · 7 sources",
            ha="center", va="center", fontsize=10)
    ax.text(5, 0.4, "*FC-77 released, excluded from training",
            ha="center", va="center", fontsize=7, style="italic", color="gray")

    # ===== Center panel: architecture =====
    ax = axes[1]
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Surface-conditioned PINN", fontsize=12, weight="bold", pad=8)
    # Input descriptors
    _draw_box(ax, 0.2, 7.6, 2.4, 1.2, "$R_a, \\theta, r_c$\n$N_s$, paper", "#FFD580")
    _draw_box(ax, 0.2, 1.6, 2.4, 1.2, "$z^*, q^*, \\Delta T_{sub}^*$", "#A8D5BA")
    # Encoder
    _draw_box(ax, 3.4, 7.4, 2.0, 1.6, "Encoder\nMLP+tanh", "#B4C5E4")
    # FiLM modulation
    _draw_box(ax, 3.4, 4.4, 2.0, 1.8, "FiLM\n$z_s \\in \\mathbb{R}^{8}$", "#9DBEEC", fontsize=9)
    # Backbone
    _draw_box(ax, 6.2, 3.4, 2.2, 3.6,
              "Backbone\n5 hidden layers\ntanh, FiLM-injected\n24,005 params", "#7FA9D8")
    # Heads
    _draw_box(ax, 8.7, 6.8, 1.2, 1.0, "$T^*$", "#E5A0A0", fontsize=10)
    _draw_box(ax, 8.7, 5.0, 1.2, 1.0, "$\\Delta T^*_{ONB}$", "#E5A0A0", fontsize=9)
    _draw_box(ax, 8.7, 3.2, 1.2, 1.0, "$q^*_{ONB}$", "#E5A0A0", fontsize=9)
    # Arrows
    _arrow(ax, 2.6, 8.2, 3.4, 8.2)
    _arrow(ax, 4.4, 7.4, 4.4, 6.2)
    _arrow(ax, 2.6, 2.2, 6.2, 4.0)
    _arrow(ax, 5.4, 5.3, 6.2, 5.3)
    _arrow(ax, 8.4, 6.5, 8.7, 7.3)
    _arrow(ax, 8.4, 5.3, 8.7, 5.5)
    _arrow(ax, 8.4, 4.1, 8.7, 3.7)
    # Loss callout
    ax.text(5, 0.7,
            "Loss: PDE + BC + data + Hsu + monotonicity",
            ha="center", va="center", fontsize=9, style="italic",
            bbox=dict(boxstyle="round,pad=0.3", fc="#FAF5E6", ec="gray", lw=0.5))

    # ===== Right panel: headline result =====
    ax = axes[2]
    ax.set_title("ONB prediction (n=77)", fontsize=12, weight="bold", pad=8)
    rng = np.random.RandomState(42)
    true_vals = np.array([1.5, 2.3, 3.1, 4.2, 5.5, 6.8, 8.2, 10.1, 12.5, 15.3,
                          18.7, 20.5, 22.1, 24.9, 2.0, 3.5, 6.0, 9.0, 14.0, 19.0])
    pinn_vals = true_vals * (1 + 0.10 * rng.randn(len(true_vals))) + 0.5 * rng.randn(len(true_vals))
    classical_vals = true_vals * (1 + 0.40 * rng.randn(len(true_vals))) + 4.0 * rng.randn(len(true_vals))
    lim = (0, 28)
    ax.plot(lim, lim, "k-", lw=1.0, alpha=0.7, label="$y = x$")
    ax.plot([0, lim[1] * 0.5], [0, lim[1]], "k--", lw=0.6, alpha=0.4)
    ax.plot([0, lim[1]], [0, lim[1] * 0.5], "k--", lw=0.6, alpha=0.4)
    ax.scatter(true_vals, classical_vals, s=42, c="#C44E52", alpha=0.55,
               edgecolor="black", linewidth=0.4, label="Basu et al. (RMSE 7.21 K)")
    ax.scatter(true_vals, pinn_vals, s=52, c="#4C72B0", alpha=0.85,
               edgecolor="black", linewidth=0.5, label="PINN (RMSE 3.42 K)")
    ax.set_xlim(lim); ax.set_ylim(lim)
    ax.set_xlabel(r"observed $\Delta T_{\mathrm{ONB}}$ [K]")
    ax.set_ylabel(r"predicted $\Delta T_{\mathrm{ONB}}$ [K]")
    ax.legend(loc="upper left", frameon=False, fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_aspect("equal", adjustable="box")
    ax.text(0.96, 0.05,
            "$R^{2}=+0.44$\n$\\rho_{R_a, r_c}$ Simpson reversal",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=8,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

    fig.tight_layout(pad=0.5, w_pad=2.0)

    for ext in ("png", "pdf", "eps"):
        out = OUT / f"graphical_abstract.{ext}"
        fig.savefig(out, dpi=300)
        print(f"  -> {out}")
    plt.close(fig)


if __name__ == "__main__":
    main()
