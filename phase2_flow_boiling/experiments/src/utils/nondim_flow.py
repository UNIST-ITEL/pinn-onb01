"""
nondim_flow.py — Flow variable nondimensionalization for Phase 2.

Converts raw SI flow variables to normalized encoder inputs.
CoolProp is used where installed; a lightweight fallback is provided
for water at ~1 atm when CoolProp is unavailable.

Variable naming follows CLAUDE.md:
    G_kg_m2s, delta_T_sub_K, D_h_mm, P_kPa
    nondim outputs suffixed _star.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

# ── Fluid property fallback for water at ~100 kPa ─────────────────────────────
_WATER_FALLBACK = {
    "mu_l":   8.9e-4,    # Pa·s
    "rho_l":  958.0,     # kg/m³  (at ~100°C)
    "sigma":  0.0589,    # N/m
    "h_fg":   2.257e6,   # J/kg
    "cp_l":   4216.0,    # J/(kg·K)
    "k_l":    0.679,     # W/(m·K)
    "T_sat":  373.15,    # K  (at 101.325 kPa)
}

_REFRIG_FALLBACK = {
    "R-11":  {"mu_l": 4.2e-4, "rho_l": 1480, "sigma": 0.018, "h_fg": 182e3,
              "cp_l": 870, "k_l": 0.090, "T_sat": 296.9},
    "R-12":  {"mu_l": 2.7e-4, "rho_l": 1330, "sigma": 0.015, "h_fg": 165e3,
              "cp_l": 930, "k_l": 0.074, "T_sat": 243.4},
    "R-113": {"mu_l": 6.6e-4, "rho_l": 1565, "sigma": 0.017, "h_fg": 147e3,
              "cp_l": 940, "k_l": 0.071, "T_sat": 320.7},
    "FC-72": {"mu_l": 6.4e-4, "rho_l": 1680, "sigma": 0.010, "h_fg": 88e3,
              "cp_l": 1100, "k_l": 0.057, "T_sat": 329.15},
}


def _get_props(fluid: str, P_kPa: float) -> dict[str, float]:
    """Return saturation properties; tries CoolProp first, falls back to table."""
    try:
        import CoolProp.CoolProp as CP
        P_Pa = P_kPa * 1e3
        T_sat = CP.PropsSI("T", "P", P_Pa, "Q", 0, fluid)
        rho_l = CP.PropsSI("D", "P", P_Pa, "Q", 0, fluid)
        mu_l  = CP.PropsSI("V", "P", P_Pa, "Q", 0, fluid)
        sigma = CP.PropsSI("I", "P", P_Pa, "Q", 0, fluid)
        h_fg  = (CP.PropsSI("H", "P", P_Pa, "Q", 1, fluid)
                 - CP.PropsSI("H", "P", P_Pa, "Q", 0, fluid))
        cp_l  = CP.PropsSI("C", "P", P_Pa, "Q", 0, fluid)
        k_l   = CP.PropsSI("L", "P", P_Pa, "Q", 0, fluid)
        return {"mu_l": mu_l, "rho_l": rho_l, "sigma": sigma,
                "h_fg": h_fg, "cp_l": cp_l, "k_l": k_l, "T_sat": T_sat}
    except Exception:
        pass

    # Fallback tables (P_kPa ignored — atmospheric approximation)
    base_fluid = fluid.split("_")[0]  # water_DIW → water
    if base_fluid in ("water", "water_DIW"):
        return dict(_WATER_FALLBACK)
    return dict(_REFRIG_FALLBACK.get(base_fluid, _WATER_FALLBACK))


@dataclass(frozen=True)
class FlowNondimScales:
    """Derived nondimensionalisation scales for one (fluid, P) condition."""
    fluid: str
    P_kPa: float
    T_sat_K: float
    rho_l: float     # kg/m³
    mu_l: float      # Pa·s
    sigma: float     # N/m
    h_fg: float      # J/kg
    cp_l: float      # J/(kg·K)
    k_l: float       # W/(m·K)
    L_c: float       # capillary length [m] = sqrt(σ / (ρ_l g))
    G_ref: float     # reference mass flux [kg/m²s] = ρ_l √(g L_c)


_SCALES_CACHE: dict[tuple[str, float], FlowNondimScales] = {}


def compute_flow_nondim(fluid: str, P_kPa: float) -> FlowNondimScales:
    """Compute (and cache) nondim scales for given fluid and pressure."""
    key = (fluid, round(P_kPa, 1))
    if key in _SCALES_CACHE:
        return _SCALES_CACHE[key]

    props = _get_props(fluid, P_kPa)
    g = 9.81
    L_c = math.sqrt(props["sigma"] / (props["rho_l"] * g))
    G_ref = props["rho_l"] * math.sqrt(g * L_c)
    scales = FlowNondimScales(
        fluid=fluid, P_kPa=P_kPa,
        T_sat_K=props["T_sat"], rho_l=props["rho_l"],
        mu_l=props["mu_l"], sigma=props["sigma"],
        h_fg=props["h_fg"], cp_l=props["cp_l"], k_l=props["k_l"],
        L_c=L_c, G_ref=G_ref,
    )
    _SCALES_CACHE[key] = scales
    return scales
