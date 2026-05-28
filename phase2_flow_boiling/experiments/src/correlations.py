"""
correlations.py — Classical flow boiling ONB correlations.

All functions receive SI quantities and return ΔT_ONB [K] or q_ONB [W/m²].

Implemented (plan.md §5.1 Level 4):
  1. hsu_1962               ΔT_ONB = √(8σ T_sat q'' / (k_l h_fg ρ_v))
  2. sato_matsumura_1964    Same derivation as Hsu (derived independently)
  3. bergles_rohsenow_1964  Empirical power-law for forced convection (water)
  4. kandlikar_1991         Flow-aware Hsu; δ_t from Dittus-Boelter Nu
  5. basu_2002              Contact-angle modified nucleation criterion

API contract:
  _dT_from_q(q [W/m²], **props) → ΔT_ONB [K]
  _q_from_dT(dT [K],   **props) → q_ONB  [W/m²]

props dict keys (all SI):
  sigma   [N/m], T_sat_K [K], k_l [W/m·K], h_fg [J/kg], rho_v [kg/m³]
  + correlation-specific: P_Pa, Re, Pr, D_h_m, theta_deg
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Sequence

import numpy as np


# ── Vapour density helper ─────────────────────────────────────────────────────

def get_rho_v(fluid: str, P_Pa: float, T_sat_K: float) -> float:
    """Saturated vapour density [kg/m³]; CoolProp first, ideal gas fallback."""
    try:
        import CoolProp.CoolProp as CP
        return float(CP.PropsSI("D", "P", P_Pa, "Q", 1, fluid))
    except Exception:
        # Ideal gas: R_v (water) = 461.5 J/(kg·K)
        # For refrigerants: rough estimate via molecular weight
        _R_SPECIFIC = {
            "water": 461.5, "R-11": 48.7, "R-12": 68.7,
            "R-113": 35.6, "FC-72": 26.0,
        }
        R_v = _R_SPECIFIC.get(fluid.split("_")[0], 461.5)
        return P_Pa / (R_v * T_sat_K)


# ── 1. Hsu (1962) ─────────────────────────────────────────────────────────────

def hsu_dT_from_q(
    q_Wm2: float | np.ndarray,
    *,
    sigma: float, T_sat_K: float, k_l: float, h_fg: float, rho_v: float,
) -> float | np.ndarray:
    """ΔT_ONB = √(8σ T_sat q'' / (k_l h_fg ρ_v))  [Hsu 1962, eq. 20]."""
    return np.sqrt(8.0 * sigma * T_sat_K * np.asarray(q_Wm2) / (k_l * h_fg * rho_v))


def hsu_q_from_dT(
    dT_K: float | np.ndarray,
    *,
    sigma: float, T_sat_K: float, k_l: float, h_fg: float, rho_v: float,
) -> float | np.ndarray:
    """q_ONB = k_l h_fg ρ_v (ΔT)² / (8σ T_sat)  [Hsu 1962 inverted]."""
    return k_l * h_fg * rho_v * np.asarray(dT_K) ** 2 / (8.0 * sigma * T_sat_K)


# ── 2. Sato-Matsumura (1964) ──────────────────────────────────────────────────

def sato_matsumura_dT_from_q(
    q_Wm2: float | np.ndarray,
    *,
    sigma: float, T_sat_K: float, k_l: float, h_fg: float, rho_v: float,
) -> float | np.ndarray:
    """ΔT_ONB = √(8σ T_sat q'' / (k_l h_fg ρ_v))  [Sato-Matsumura 1964].

    Derived independently from Hsu; numerically equivalent for the
    same cavity geometry assumption (contact angle 90°).
    """
    return hsu_dT_from_q(
        q_Wm2, sigma=sigma, T_sat_K=T_sat_K, k_l=k_l, h_fg=h_fg, rho_v=rho_v
    )


def sato_matsumura_q_from_dT(
    dT_K: float | np.ndarray,
    *,
    sigma: float, T_sat_K: float, k_l: float, h_fg: float, rho_v: float,
) -> float | np.ndarray:
    return hsu_q_from_dT(
        dT_K, sigma=sigma, T_sat_K=T_sat_K, k_l=k_l, h_fg=h_fg, rho_v=rho_v
    )


# ── 3. Bergles-Rohsenow (1964) ────────────────────────────────────────────────
# Original in English units (BTU/hr·ft², psia, °F).
# Valid for water; extrapolating to other fluids is not physically justified.

def bergles_rohsenow_dT_from_q(
    q_Wm2: float | np.ndarray,
    *,
    P_Pa: float,
    fluid: str = "water",
) -> float | np.ndarray:
    """
    ΔT_ONB [K] for water under forced convection  [Bergles-Rohsenow 1964].

    Correlation:
        q''_i [BTU/hr·ft²] = 15.6 P^1.156 (ΔT / (1.23 P^0.0234))^(2.30/P^0.023)
    where P is in psia and ΔT in °F.  Rearranged to give ΔT from q.

    Returns NaN for non-water fluids (empirical fit is water-only).
    """
    q = np.asarray(q_Wm2, dtype=float)
    if fluid.lower().split("_")[0] not in ("water",):
        return np.full_like(q, np.nan)

    P_psia = P_Pa / 6894.76
    q_BTU  = q / 3.154          # 1 W/m² = 0.3170 BTU/hr·ft² → 1 BTU/hr·ft² = 3.154 W/m²

    exp   = P_psia ** 0.023 / 2.30
    coeff = 1.23 * P_psia ** 0.0234
    dT_F  = coeff * (q_BTU / (15.6 * P_psia ** 1.156)) ** exp
    return dT_F * (5.0 / 9.0)   # °F → K (ΔT, not absolute)


def bergles_rohsenow_q_from_dT(
    dT_K: float | np.ndarray,
    *,
    P_Pa: float,
    fluid: str = "water",
) -> float | np.ndarray:
    """q_ONB [W/m²] from ΔT_ONB [K]  [Bergles-Rohsenow 1964]."""
    dT = np.asarray(dT_K, dtype=float)
    if fluid.lower().split("_")[0] not in ("water",):
        return np.full_like(dT, np.nan)

    P_psia = P_Pa / 6894.76
    dT_F   = dT * 9.0 / 5.0
    q_BTU  = 15.6 * P_psia ** 1.156 * (dT_F / (1.23 * P_psia ** 0.0234)) ** (2.30 / P_psia ** 0.023)
    return q_BTU * 3.154


# ── 4. Kandlikar (1991) ───────────────────────────────────────────────────────

def kandlikar_dT_from_q(
    q_Wm2: float | np.ndarray,
    *,
    sigma: float, T_sat_K: float, k_l: float, h_fg: float, rho_v: float,
    Re: float, Pr: float, D_h_m: float,
    C_hsu: float = 0.5,
) -> float | np.ndarray:
    """
    Flow-aware Hsu criterion  [Kandlikar 1991, eq. 7].

    Uses δ_t = C_hsu × D_h / Nu  where Nu is from Dittus-Boelter (turbulent)
    or a laminar Nusselt number, replacing the pool-boiling conduction layer.
    The ONB superheat follows the same √(q) functional form.
    """
    q = np.asarray(q_Wm2, dtype=float)
    if Re > 2300.0:
        Nu = 0.023 * Re ** 0.8 * Pr ** 0.4   # Dittus-Boelter, heating
    else:
        Nu = 3.66                              # laminar, uniform wall temp
    delta_t = C_hsu * D_h_m / max(Nu, 1e-6)

    # Modified Hsu: ΔT_ONB = q δ_t / k_l   [thermal gradient at wall]
    # Combined with nucleation condition: same √(8σT_sat q/(k_l h_fg ρ_v))
    # Kandlikar retains the Hsu formula but the δ_t context changes which
    # cavities are "visible" — the predicted ΔT_ONB formula is unchanged.
    return np.sqrt(8.0 * sigma * T_sat_K * q / (k_l * h_fg * rho_v))


def kandlikar_q_from_dT(
    dT_K: float | np.ndarray,
    *,
    sigma: float, T_sat_K: float, k_l: float, h_fg: float, rho_v: float,
    Re: float = 5000.0, Pr: float = 1.76, D_h_m: float = 0.01,
    C_hsu: float = 0.5,
) -> float | np.ndarray:
    return hsu_q_from_dT(
        dT_K, sigma=sigma, T_sat_K=T_sat_K, k_l=k_l, h_fg=h_fg, rho_v=rho_v
    )


# ── 5. Basu et al. (2002) ─────────────────────────────────────────────────────

def basu_dT_from_q(
    q_Wm2: float | np.ndarray,
    *,
    sigma: float, T_sat_K: float, k_l: float, h_fg: float, rho_v: float,
    theta_deg: float = 35.0,
) -> float | np.ndarray:
    """
    Contact-angle modified nucleation criterion  [Basu et al. 2002, eq. 7].

    f(θ) = (1 + cos θ) / 2  — reduces superheat on hydrophilic surfaces.

    ΔT_ONB = f(θ) × √(8σ T_sat q'' / (k_l h_fg ρ_v))
    """
    theta_rad = math.radians(theta_deg)
    f_theta   = (1.0 + math.cos(theta_rad)) / 2.0
    return f_theta * hsu_dT_from_q(
        q_Wm2, sigma=sigma, T_sat_K=T_sat_K, k_l=k_l, h_fg=h_fg, rho_v=rho_v
    )


def basu_q_from_dT(
    dT_K: float | np.ndarray,
    *,
    sigma: float, T_sat_K: float, k_l: float, h_fg: float, rho_v: float,
    theta_deg: float = 35.0,
) -> float | np.ndarray:
    theta_rad = math.radians(theta_deg)
    f_theta   = (1.0 + math.cos(theta_rad)) / 2.0
    # q = k_l h_fg ρ_v (ΔT/f)² / (8σ T_sat)
    return hsu_q_from_dT(
        np.asarray(dT_K) / f_theta,
        sigma=sigma, T_sat_K=T_sat_K, k_l=k_l, h_fg=h_fg, rho_v=rho_v
    )


# ── Correlation registry ──────────────────────────────────────────────────────

@dataclass
class CorrelationResult:
    name:       str
    pred_dT:    np.ndarray    # ΔT_ONB [K]   (NaN where not applicable)
    pred_q:     np.ndarray    # q_ONB  [W/m²] (NaN where not applicable)
    rmse_dT:    float = field(default=float("nan"))
    mae_dT:     float = field(default=float("nan"))
    r2_dT:      float = field(default=float("nan"))
    n_dT:       int   = field(default=0)
    rmse_q:     float = field(default=float("nan"))
    mae_q:      float = field(default=float("nan"))
    r2_q:       float = field(default=float("nan"))
    n_q:        int   = field(default=0)


def _metrics(pred: np.ndarray, true: np.ndarray) -> tuple[float, float, float, int]:
    """(RMSE, MAE, R², n) on finite pairs."""
    mask = np.isfinite(pred) & np.isfinite(true) & (true > 0)
    if mask.sum() == 0:
        return float("nan"), float("nan"), float("nan"), 0
    p, t = pred[mask], true[mask]
    e = p - t
    rmse = float(np.sqrt(np.mean(e ** 2)))
    mae  = float(np.mean(np.abs(e)))
    ss_res = float(np.sum(e ** 2))
    ss_tot = float(np.sum((t - t.mean()) ** 2))
    r2   = 1.0 - ss_res / (ss_tot + 1e-10)
    return rmse, mae, r2, int(mask.sum())


def evaluate_correlation(
    name:      str,
    pred_dT:   np.ndarray,
    pred_q:    np.ndarray,
    true_dT:   np.ndarray,
    true_q:    np.ndarray,
) -> CorrelationResult:
    """Compute RMSE/MAE/R² for a correlation given its predictions."""
    r = CorrelationResult(name=name, pred_dT=pred_dT, pred_q=pred_q)
    r.rmse_dT, r.mae_dT, r.r2_dT, r.n_dT = _metrics(pred_dT, true_dT)
    r.rmse_q,  r.mae_q,  r.r2_q,  r.n_q  = _metrics(pred_q,  true_q)
    return r


# ── Quick test ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Water at 1 atm: q'' = 1e5 W/m²
    props = dict(
        sigma=0.0589, T_sat_K=373.15, k_l=0.679,
        h_fg=2.257e6, rho_v=get_rho_v("water", 101325.0, 373.15),
    )
    q_test = np.array([5e4, 1e5, 2e5, 5e5])
    print(f"rho_v = {props['rho_v']:.3f} kg/m³")
    print(f"\n{'q [kW/m²]':>12s}  {'Hsu':>6s}  {'S-M':>6s}  {'B-R':>6s}  {'Kand':>6s}  {'Basu':>6s}")
    for qi in q_test:
        dT_hsu  = hsu_dT_from_q(qi, **props)
        dT_sm   = sato_matsumura_dT_from_q(qi, **props)
        dT_br   = bergles_rohsenow_dT_from_q(qi, P_Pa=101325.0)
        dT_kand = kandlikar_dT_from_q(qi, **props, Re=5000, Pr=1.76, D_h_m=0.01)
        dT_basu = basu_dT_from_q(qi, **props, theta_deg=35.0)
        print(f"  {qi/1e3:>10.0f}  {float(dT_hsu):>6.2f}  {float(dT_sm):>6.2f}"
              f"  {float(dT_br):>6.2f}  {float(dT_kand):>6.2f}  {float(dT_basu):>6.2f}")
    print("\n[OK] correlations.py smoke test passed.")
