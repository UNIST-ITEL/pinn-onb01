"""fig:concept — (a) ONB identification from a boiling curve (schematic);
(b) Hsu criterion as a one-sided lower bound, using REAL v11 data.

Panel (a) is a schematic: the wall temperature is continuous in q'' and the
single-phase and nucleate-boiling branches MEET at ONB (the slope drops); the
dashed line is the single-phase extrapolation (the overheating boiling avoids).

Panel (b) plots the measured ONB superheat against the per-point saturated-pool
Hsu superheat ΔT_Hsu,sat (computed with correct fluid properties); the diagonal
is the one-sided lower bound ΔT_ONB ≥ ΔT_Hsu,sat that the coupling enforces.
"""
from __future__ import annotations
import csv
import warnings; warnings.filterwarnings("ignore")
import numpy as np
import matplotlib.pyplot as plt
from figlib import set_style, save_fig, CSV


def _hsu_lower_bound_data():
    """Return (dT_hsu_sat[K], dT_measured[K]) for all rows with valid q & ΔT.

    Uses the project's saturated-pool Hsu superheat with per-point properties
    (CoolProp via compute_flow_nondim), so the bound is correct across the
    atmospheric-to-16 MPa, water / water_DIW dataset.
    """
    from correlations import hsu_dT_from_q, get_rho_v
    from utils.nondim_flow import compute_flow_nondim

    def _f(x):
        try:
            return float(x)
        except (TypeError, ValueError):
            return None

    hsu, meas = [], []
    for r in csv.DictReader(open(CSV)):
        q, dT = _f(r["q_onb_W_m2"]), _f(r["delta_T_onb_K"])
        if not (q and dT and q > 0 and dT > 0):
            continue
        P_kPa = _f(r["P_kPa"])
        P_kPa = P_kPa if (P_kPa and P_kPa > 0) else 101.325
        try:
            sc = compute_flow_nondim(r["fluid"], P_kPa)
            rho_v = get_rho_v(r["fluid"], P_kPa * 1e3, sc.T_sat_K)
            dh = float(hsu_dT_from_q(q, sigma=sc.sigma, T_sat_K=sc.T_sat_K,
                                     k_l=sc.k_l, h_fg=sc.h_fg, rho_v=rho_v))
        except Exception:
            continue
        if np.isfinite(dh) and dh > 0:
            hsu.append(dh); meas.append(dT)
    return np.asarray(hsu), np.asarray(meas)


def main() -> None:
    set_style()
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.6))

    # ── (a) ONB identification: continuous T_w(q'') with a slope change at ONB ──
    q = np.linspace(0, 400, 300)
    qonb, Tsat, TwONB = 180.0, 110.0, 116.0      # ΔT_ONB = 6 K
    slope_sp, slope_b = 0.089, 0.016             # single-phase steep, boiling shallow
    T0 = TwONB - slope_sp * qonb                 # single-phase intercept (~100 °C)
    Tw_sp = T0 + slope_sp * q
    Tw_boil = TwONB + slope_b * (q - qonb)
    m_sp, m_ex = q <= qonb, q >= qonb

    axs[0].plot(q[m_sp], Tw_sp[m_sp], "-", color="#1565C0", lw=2.4, label="single-phase")
    # single-phase extrapolation beyond ONB — the overheating that boiling avoids
    q_ex = q[(q >= qonb) & (Tw_sp <= 129)]
    axs[0].plot(q_ex, T0 + slope_sp * q_ex, "--", color="#1565C0", lw=1.4, alpha=0.75)
    axs[0].text(q_ex[-1], T0 + slope_sp * q_ex[-1] + 0.4, "single-phase\n(extrapolated)",
                color="#1565C0", fontsize=8, ha="right", va="bottom")
    axs[0].plot(q[m_ex], Tw_boil[m_ex], "-", color="#C62828", lw=2.4, label="nucleate boiling")
    axs[0].axhline(Tsat, ls=":", color="#777", lw=1.2)
    axs[0].text(5, Tsat + 0.7, "$T_{sat}$", color="#777", fontsize=9)

    axs[0].plot([qonb], [TwONB], "o", ms=11, mfc="#FDD835", mec="k", zorder=5)
    axs[0].annotate("ONB", (qonb, TwONB), (qonb - 100, TwONB + 7), fontsize=10, fontweight="bold",
                    arrowprops=dict(arrowstyle="->", lw=1.3))
    axs[0].annotate("", (qonb, Tsat), (qonb, TwONB),
                    arrowprops=dict(arrowstyle="<->", color="#388E3C", lw=1.4))
    axs[0].text(qonb + 6, (Tsat + TwONB) / 2, "$\\Delta T_{ONB}$", color="#388E3C", fontsize=10)
    axs[0].set_xlabel("Heat flux $q''$ [kW m$^{-2}$]")
    axs[0].set_ylabel("Wall temperature $T_w$ [$^\\circ$C]")
    axs[0].set_ylim(96, 132)
    axs[0].set_title("(a)", loc="left", fontweight="bold", fontsize=11)
    axs[0].legend(fontsize=8.5, loc="upper left")

    # ── (b) Hsu saturated superheat as a one-sided lower bound (real data) ──
    hsu, meas = _hsu_lower_bound_data()
    lim = float(max(hsu.max(), meas.max())) * 1.05
    xx = np.array([0.0, lim])
    axs[1].fill_between(xx, 0, xx, color="#FFCDD2", alpha=0.5,
                        label="forbidden ($\\Delta T_{ONB}<\\Delta T_{Hsu,sat}$)")
    axs[1].plot(xx, xx, "-", color="#C62828", lw=2.2,
                label="Hsu lower bound ($\\Delta T_{ONB}=\\Delta T_{Hsu,sat}$)")
    axs[1].scatter(hsu, meas, s=26, color="#1565C0", alpha=0.7, edgecolor="k", lw=0.3,
                   label=f"subcooled-flow ONB data (n={len(meas)})")
    axs[1].set_xlabel("$\\Delta T_{Hsu,sat}$ [K]   (saturated-pool Hsu)")
    axs[1].set_ylabel("$\\Delta T_{ONB}$ [K]   (measured)")
    axs[1].set_xlim(0, lim); axs[1].set_ylim(0, lim)
    axs[1].set_aspect("equal", adjustable="box")
    axs[1].set_title("(b)", loc="left", fontweight="bold", fontsize=11)
    axs[1].legend(fontsize=8, loc="upper left")

    fig.tight_layout()
    save_fig(fig, "fig_onb_concept")


if __name__ == "__main__":
    main()
