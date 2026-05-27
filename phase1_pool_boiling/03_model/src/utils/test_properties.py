"""
test_properties.py — pytest validation suite for properties.py.

Run:
    pytest 03_model/src/utils/test_properties.py -v

Coverage:
    - Water at 1 atm vs. NIST reference values (tol 0.5 %)
    - R-123 and R-134a smoke tests (T_sat in physically plausible range)
    - Hsu cavity radius: physical bounds and discriminant < 0 case
    - Jacob number edge cases
    - Capillary length sign / magnitude
    - Error handling: unsupported fluids, out-of-range pressure,
      above critical pressure
"""

from __future__ import annotations

import math
import pytest

from properties import (
    SaturationProperties,
    saturation_properties,
    jacob_number,
    capillary_length,
    hsu_criterion_cavity_radius,
    UnsupportedFluidError,
    PressureRangeError,
    AboveCriticalPressureError,
)


# ---------------------------------------------------------------------------
# Constants for reference validation
# ---------------------------------------------------------------------------

P_ATM = 101_325.0  # Pa


class TestWaterAt1Atm:
    """Validate water properties at 1 atm against NIST/IAPWS reference."""

    @pytest.fixture(scope="class")
    def props(self) -> SaturationProperties:
        return saturation_properties("water", P=P_ATM)

    REF = {
        "T_sat":  373.124,
        "rho_l":  958.4,
        "rho_v":  0.5977,
        "sigma":  0.0589,
        "h_fg":   2.257e6,
        "mu_l":   2.817e-4,
        "k_l":    0.6770,
        "cp_l":   4216.0,
        "Pr_l":   1.753,
    }
    TOL = 0.005  # 0.5 %

    @pytest.mark.parametrize("attr,ref", REF.items())
    def test_within_tolerance(
        self, props: SaturationProperties, attr: str, ref: float
    ) -> None:
        val = getattr(props, attr)
        rel_err = abs(val - ref) / ref
        assert rel_err < self.TOL, (
            f"{attr}: computed={val:.6g}, ref={ref:.6g}, "
            f"rel_err={rel_err*100:.3f}% > 0.5%"
        )

    def test_nu_l_consistency(self, props: SaturationProperties) -> None:
        """nu_l must equal mu_l / rho_l to within floating-point precision."""
        expected = props.mu_l / props.rho_l
        assert math.isclose(props.nu_l, expected, rel_tol=1e-9)

    def test_pr_l_consistency(self, props: SaturationProperties) -> None:
        """Pr_l must match cp_l * mu_l / k_l to within 0.1%."""
        expected = props.cp_l * props.mu_l / props.k_l
        rel_err = abs(props.Pr_l - expected) / expected
        assert rel_err < 1e-3

    def test_h_fg_positive(self, props: SaturationProperties) -> None:
        assert props.h_fg > 0.0

    def test_rho_ratio(self, props: SaturationProperties) -> None:
        """rho_v must be much smaller than rho_l for subcritical conditions."""
        assert props.rho_v < props.rho_l * 0.01

    def test_frozen_dataclass(self, props: SaturationProperties) -> None:
        with pytest.raises((AttributeError, TypeError)):
            props.T_sat = 400.0  # type: ignore[misc]


class TestR123At1Atm:
    """Smoke test for R-123 (used in Jabardo dataset)."""

    @pytest.fixture(scope="class")
    def props(self) -> SaturationProperties:
        return saturation_properties("R-123", P=P_ATM)

    def test_T_sat_range(self, props: SaturationProperties) -> None:
        # R-123 normal boiling point ≈ 300.97 K
        assert 295.0 < props.T_sat < 310.0

    def test_sigma_positive(self, props: SaturationProperties) -> None:
        assert props.sigma > 0.0

    def test_h_fg_positive(self, props: SaturationProperties) -> None:
        assert props.h_fg > 0.0


class TestR134aAt5Bar:
    """Smoke test for R-134a at 5 bar (used in Jabardo dataset)."""

    @pytest.fixture(scope="class")
    def props(self) -> SaturationProperties:
        return saturation_properties("R-134a", P=5e5)

    def test_T_sat_range(self, props: SaturationProperties) -> None:
        # R-134a at 5 bar ≈ 288.9 K
        assert 280.0 < props.T_sat < 300.0

    def test_all_fields_positive(self, props: SaturationProperties) -> None:
        for field in ("T_sat", "rho_l", "rho_v", "sigma", "h_fg",
                      "mu_l", "k_l", "cp_l", "Pr_l", "nu_l"):
            assert getattr(props, field) > 0.0, f"{field} must be positive"


class TestNovec649:
    """Novec649 is in CoolProp 7.2 but missing sigma, mu, k models.
    Verify it raises UnsupportedFluidError like other incomplete fluids."""

    def test_raises_unsupported(self) -> None:
        with pytest.raises(UnsupportedFluidError, match="Novec649"):
            saturation_properties("Novec649", P=P_ATM)


class TestCaching:
    """Verify that lru_cache returns the same object for repeated calls."""

    def test_same_object_returned(self) -> None:
        a = saturation_properties("water", P=P_ATM)
        b = saturation_properties("water", P=P_ATM)
        assert a is b  # cached: identical object


class TestInputValidation:
    """Input error handling."""

    @pytest.mark.parametrize(
        "fluid",
        ["FC-72", "FC-77", "HFE-7100", "fc72", "hfe7100", "Novec649", "fc-5112"],
    )
    def test_unsupported_fluid_raises(self, fluid: str) -> None:
        with pytest.raises(UnsupportedFluidError):
            saturation_properties(fluid)

    @pytest.mark.parametrize("fluid", ["nitrogen", "co2", "benzene", "Methanol"])
    def test_unknown_fluid_raises(self, fluid: str) -> None:
        with pytest.raises(ValueError):
            saturation_properties(fluid)

    def test_pressure_too_low(self) -> None:
        with pytest.raises(PressureRangeError):
            saturation_properties("water", P=500.0)

    def test_pressure_too_high(self) -> None:
        with pytest.raises(PressureRangeError):
            saturation_properties("water", P=25e6)

    def test_above_critical_pressure(self) -> None:
        # R-134a P_crit ≈ 4.059 MPa; 4.1 MPa should trigger AboveCriticalPressure
        with pytest.raises(AboveCriticalPressureError):
            saturation_properties("R-134a", P=4.1e6)


class TestJacobNumber:
    """Jacob number helper."""

    @pytest.fixture(scope="class")
    def props(self) -> SaturationProperties:
        return saturation_properties("water", P=P_ATM)

    def test_zero_subcooling(self, props: SaturationProperties) -> None:
        assert jacob_number(props, delta_T_sub=0.0) == 0.0

    def test_positive_subcooling(self, props: SaturationProperties) -> None:
        Ja = jacob_number(props, delta_T_sub=5.0)
        assert Ja > 0.0

    def test_linearity(self, props: SaturationProperties) -> None:
        """Ja should scale linearly with delta_T_sub."""
        Ja5 = jacob_number(props, delta_T_sub=5.0)
        Ja10 = jacob_number(props, delta_T_sub=10.0)
        assert math.isclose(Ja10, 2.0 * Ja5, rel_tol=1e-9)

    def test_negative_subcooling_raises(self, props: SaturationProperties) -> None:
        with pytest.raises(ValueError):
            jacob_number(props, delta_T_sub=-1.0)


class TestCapillaryLength:
    """Capillary length helper."""

    @pytest.fixture(scope="class")
    def props(self) -> SaturationProperties:
        return saturation_properties("water", P=P_ATM)

    def test_water_capillary_length_mm_scale(self, props: SaturationProperties) -> None:
        # For water at 1 atm, L_c ≈ 2.5 mm
        L_c = capillary_length(props)
        assert 1e-3 < L_c < 1e-2

    def test_positive(self, props: SaturationProperties) -> None:
        assert capillary_length(props) > 0.0


class TestHsuCavityRadius:
    """Hsu criterion cavity radius helper."""

    @pytest.fixture(scope="class")
    def props(self) -> SaturationProperties:
        return saturation_properties("water", P=P_ATM)

    def test_returns_two_floats(self, props: SaturationProperties) -> None:
        result = hsu_criterion_cavity_radius(props, delta_T_wall=10.0, q_flux=50_000.0)
        assert len(result) == 2
        assert all(isinstance(v, float) for v in result)

    def test_r_c_min_le_r_c_max(self, props: SaturationProperties) -> None:
        r_min, r_max = hsu_criterion_cavity_radius(
            props, delta_T_wall=10.0, q_flux=50_000.0
        )
        assert r_min <= r_max

    def test_r_c_min_positive(self, props: SaturationProperties) -> None:
        r_min, r_max = hsu_criterion_cavity_radius(
            props, delta_T_wall=10.0, q_flux=50_000.0
        )
        assert r_min >= 0.0

    def test_no_solution_returns_zeros(self, props: SaturationProperties) -> None:
        """Very small delta_T_wall or very large q_flux -> negative discriminant."""
        r_min, r_max = hsu_criterion_cavity_radius(
            props, delta_T_wall=0.001, q_flux=1e9
        )
        assert r_min == 0.0
        assert r_max == 0.0

    def test_invalid_dT_wall_raises(self, props: SaturationProperties) -> None:
        with pytest.raises(ValueError):
            hsu_criterion_cavity_radius(props, delta_T_wall=0.0, q_flux=50_000.0)

    def test_invalid_q_flux_raises(self, props: SaturationProperties) -> None:
        with pytest.raises(ValueError):
            hsu_criterion_cavity_radius(props, delta_T_wall=10.0, q_flux=0.0)
