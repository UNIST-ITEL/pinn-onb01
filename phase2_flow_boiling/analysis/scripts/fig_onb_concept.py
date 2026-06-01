"""fig:concept — (a) ONB identification from a boiling curve;
(b) Hsu criterion as a one-sided lower bound. Pure matplotlib schematic."""
from __future__ import annotations
import warnings; warnings.filterwarnings("ignore")
import numpy as np
import matplotlib.pyplot as plt
from figlib import set_style, save_fig


def main() -> None:
    set_style()
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.6))

    # (a) ONB identification: T_w vs q
    q = np.linspace(0, 400, 200)
    qonb, Tsat = 180.0, 110.0
    Tw_sp = Tsat - 8 + 0.10 * q
    Tw_boil = Tsat + 2.0 + 0.012 * (q - qonb)
    axs[0].plot(q[q < qonb], Tw_sp[q < qonb], "-", color="#1565C0", lw=2.4, label="single-phase")
    axs[0].plot(q[q >= qonb], Tw_boil[q >= qonb], "-", color="#C62828", lw=2.4, label="nucleate boiling")
    axs[0].axhline(Tsat, ls=":", color="#777", lw=1.2); axs[0].text(5, Tsat + 0.6, "$T_{sat}$", color="#777", fontsize=9)
    TwONB = Tsat + 2.0
    axs[0].plot([qonb], [TwONB], "o", ms=11, mfc="#FDD835", mec="k", zorder=5)
    axs[0].annotate("ONB", (qonb, TwONB), (qonb - 95, TwONB + 5), fontsize=10, fontweight="bold",
                    arrowprops=dict(arrowstyle="->", lw=1.3))
    axs[0].annotate("", (qonb, Tsat), (qonb, TwONB), arrowprops=dict(arrowstyle="<->", color="#388E3C", lw=1.4))
    axs[0].text(qonb + 6, (Tsat + TwONB) / 2, "$\\Delta T_{ONB}$", color="#388E3C", fontsize=10)
    axs[0].set_xlabel("Heat flux $q''$ [kW m$^{-2}$]"); axs[0].set_ylabel("Wall temperature $T_w$ [$^\\circ$C]")
    axs[0].set_title("(a) ONB identification from the boiling curve"); axs[0].legend(fontsize=8.5, loc="upper left")

    # (b) Hsu as one-sided lower bound
    qq = np.linspace(5, 500, 200); C = 0.55
    hsu = C * np.sqrt(qq)
    axs[1].fill_between(qq, 0, hsu, color="#FFCDD2", alpha=0.5, label="forbidden ($\\Delta T<\\Delta T_{Hsu}$)")
    axs[1].plot(qq, hsu, "-", color="#C62828", lw=2.4, label="Hsu saturated lower bound $C\\sqrt{q^{*}}$")
    rng = np.random.default_rng(1)
    qd = rng.uniform(20, 480, 40); dTd = C * np.sqrt(qd) + rng.uniform(2, 12, 40)
    axs[1].scatter(qd, dTd, s=26, color="#1565C0", alpha=0.7, edgecolor="k", lw=0.3, label="subcooled-flow ONB data")
    axs[1].set_xlabel("$q''_{ONB}$ [kW m$^{-2}$]"); axs[1].set_ylabel("$\\Delta T_{ONB}$ [K]")
    axs[1].set_title("(b) Hsu criterion as a one-sided lower bound"); axs[1].legend(fontsize=8, loc="upper left")
    axs[1].set_ylim(0, 28)
    fig.tight_layout()
    save_fig(fig, "fig_onb_concept")


if __name__ == "__main__":
    main()
