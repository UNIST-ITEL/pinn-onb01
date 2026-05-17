"""
무차원화 모듈 — SI 변수 ↔ 무차원 변수 양방향 변환.

CLAUDE.md 표기 규칙:
  무차원 변수는 접미 `_star` (예: delta_T_star, q_star, r_star)
  무차원화 길이 척도: 모세관 길이 L_c = sqrt(sigma / (g * (rho_l - rho_v)))
  무차원화 온도 척도: 잠열 기반 ΔT_ref = h_fg / cp_l (Jacob 1 기준)
  무차원화 열유속 척도: q_ref = h_fg * sqrt(sigma * g * (rho_l - rho_v)) / (rho_v^(1/2))
                      (Zuber CHF 스케일)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .properties import GRAVITY, SaturationProperties, saturation_properties


@dataclass(frozen=True)
class NondimScales:
    """무차원화에 사용되는 reference scales (모두 SI 단위)."""
    L_c: float            # 모세관 길이 [m]
    delta_T_ref: float    # 온도 척도 [K] = h_fg / cp_l
    q_ref: float          # 열유속 척도 [W/m²] (Zuber CHF 기준)
    h_ref: float          # HTC 척도 [W/m²K] = q_ref / delta_T_ref
    nu_l: float           # 액체 동점도 [m²/s] (참고용)


def compute_scales(props: SaturationProperties) -> NondimScales:
    """포화 물성치로부터 무차원화 reference scales 계산.

    Zuber CHF 공식 (Lienhard form):
      q_chf = K * h_fg * rho_v^(1/2) * [sigma * g * (rho_l - rho_v)]^(1/4)
    여기서 K ≈ 0.131 (large flat plate). 본 모듈은 K=1을 사용 (reference scale).
    실제 CHF 절대값은 q_ref * 0.131로 추산 가능.
    """
    L_c = (props.sigma / (GRAVITY * (props.rho_l - props.rho_v))) ** 0.5
    delta_T_ref = props.h_fg / props.cp_l
    # Zuber CHF reference (K=1, dimensionally correct)
    q_ref = (
        props.h_fg
        * (props.rho_v ** 0.5)
        * (props.sigma * GRAVITY * (props.rho_l - props.rho_v)) ** 0.25
    )
    h_ref = q_ref / delta_T_ref
    return NondimScales(
        L_c=L_c,
        delta_T_ref=delta_T_ref,
        q_ref=q_ref,
        h_ref=h_ref,
        nu_l=props.nu_l,
    )


# ============================================================================
# 정량 변환 — 단일 값
# ============================================================================

def delta_T_to_star(delta_T: float, scales: NondimScales) -> float:
    """[K] → 무차원."""
    return delta_T / scales.delta_T_ref


def delta_T_from_star(delta_T_star: float, scales: NondimScales) -> float:
    """무차원 → [K]."""
    return delta_T_star * scales.delta_T_ref


def q_to_star(q_flux: float, scales: NondimScales) -> float:
    """[W/m²] → 무차원."""
    return q_flux / scales.q_ref


def q_from_star(q_star: float, scales: NondimScales) -> float:
    """무차원 → [W/m²]."""
    return q_star * scales.q_ref


def length_to_star(length: float, scales: NondimScales) -> float:
    """[m] → 무차원 (capillary length 단위). r_c [μm] 변환 시 1e-6 먼저 곱한 후 호출."""
    return length / scales.L_c


def length_from_star(length_star: float, scales: NondimScales) -> float:
    """무차원 → [m]."""
    return length_star * scales.L_c


# ============================================================================
# 정량 변환 — 배열 (numpy or list)
# ============================================================================

def vec_to_star(values: Sequence[float], ref: float) -> list[float]:
    return [v / ref for v in values]


def vec_from_star(values_star: Sequence[float], ref: float) -> list[float]:
    return [v * ref for v in values_star]


# ============================================================================
# 무차원 수
# ============================================================================

def jacob_subcooled(props: SaturationProperties, delta_T_sub: float) -> float:
    """과냉 Jacob 수 Ja = (rho_l * cp_l * ΔT_sub) / (rho_v * h_fg)."""
    return (props.rho_l * props.cp_l * delta_T_sub) / (props.rho_v * props.h_fg)


def jacob_superheat(props: SaturationProperties, delta_T_wall: float) -> float:
    """벽면 Jacob 수 Ja = (rho_l * cp_l * ΔT_wall) / (rho_v * h_fg).

    핵비등에서 기포 성장 속도와 직결.
    """
    return (props.rho_l * props.cp_l * delta_T_wall) / (props.rho_v * props.h_fg)


def prandtl_l(props: SaturationProperties) -> float:
    """액체 Prandtl 수."""
    return props.Pr_l


def reynolds_bubble(
    props: SaturationProperties,
    bubble_diameter: float,
    bubble_velocity: float,
) -> float:
    """기포 Re 수 = rho_l * D_b * U_b / mu_l."""
    return (props.rho_l * bubble_diameter * bubble_velocity) / props.mu_l


def bond_number(
    props: SaturationProperties,
    length: float,
) -> float:
    """Bond/Eotvos 수 = (rho_l - rho_v) * g * L² / sigma."""
    return ((props.rho_l - props.rho_v) * GRAVITY * length ** 2) / props.sigma


# ============================================================================
# 편의 함수 — fluid 이름 + P → scales
# ============================================================================

def scales_for(fluid: str, P: float = 101325.0) -> NondimScales:
    """fluid 이름과 압력으로부터 직접 NondimScales 산출."""
    props = saturation_properties(fluid, P)
    return compute_scales(props)


# ============================================================================
# 사용 예시
# ============================================================================

if __name__ == "__main__":
    # 1) Water at 1 atm
    print("=== Water at 1 atm ===")
    scales = scales_for("water", P=101325.0)
    print(f"  L_c          = {scales.L_c * 1e3:.3f} mm")
    print(f"  delta_T_ref  = {scales.delta_T_ref:.1f} K")
    print(f"  q_ref        = {scales.q_ref / 1e6:.3f} MW/m²  (Zuber CHF order)")
    print(f"  h_ref        = {scales.h_ref:.0f} W/m²K")

    # 2) ΔT=10K, q=50kW/m² 무차원화
    delta_T = 10.0
    q = 50_000.0
    print(f"\n  ΔT = {delta_T} K → ΔT* = {delta_T_to_star(delta_T, scales):.4f}")
    print(f"  q  = {q/1e3} kW/m² → q* = {q_to_star(q, scales):.4f}")

    # 3) Jacob 수
    props = saturation_properties("water", P=101325.0)
    Ja_super = jacob_superheat(props, delta_T_wall=10.0)
    print(f"\n  Ja_superheat (ΔT_wall=10 K) = {Ja_super:.3f}")

    # 4) Bond 수 (모세관 길이 기준 Bo=1)
    Bo_at_Lc = bond_number(props, scales.L_c)
    print(f"  Bo at L_c              = {Bo_at_Lc:.3f}  (should be 1.0)")

    # 5) R-134a 비교
    print("\n=== R-134a at 5 bar ===")
    scales_r = scales_for("R-134a", P=500_000.0)
    print(f"  L_c          = {scales_r.L_c * 1e3:.3f} mm")
    print(f"  delta_T_ref  = {scales_r.delta_T_ref:.1f} K")
    print(f"  q_ref        = {scales_r.q_ref / 1e3:.0f} kW/m²")
