"""
lhs_sampler.py — Latin Hypercube Sampling for PINN collocation points.

The sampler generates nondimensional spatial coordinates (z_star) along the
heater thickness direction and, optionally, operating-condition vectors
(q_flux_star, delta_T_sub_star).  The physical domain and nondimensionalisation
use the same NondimScales convention as the rest of PINN-ONB01.

Domain
------
* z_star  ∈ [0, L_plate_star]     — thickness direction (nondim)
* q_star  ∈ [q_star_min, q_star_max]      — optional, nondim heat flux
* dT_sub_star ∈ [0, dT_sub_star_max]      — optional, nondim subcooling

Implementation
--------------
Uses ``scipy.stats.qmc.LatinHypercube`` (scipy >= 1.7).  Falls back to
``pyDOE2`` when scipy is not available (older installs).

Authors: PINN-ONB01 project
Date   : 2026-05-13
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

import torch

# ---------------------------------------------------------------------------
# Backend selection
# ---------------------------------------------------------------------------
try:
    from scipy.stats.qmc import LatinHypercube as _ScipyLHS
    _BACKEND = "scipy"
except ImportError:
    try:
        import pyDOE2 as _pyDOE2  # type: ignore[import]
        _BACKEND = "pyDOE2"
    except ImportError:
        raise ImportError(
            "LHSCollocationSampler requires either scipy (>= 1.7) or pyDOE2. "
            "Install one of them: `pip install scipy` or `pip install pyDOE2`."
        )


def _lhs_unit(n_points: int, n_dims: int, seed: int) -> "torch.Tensor":
    """Generate (n_points, n_dims) LHS samples in [0, 1)^n_dims.

    Uses scipy or pyDOE2 depending on availability at import time.
    Returns a float32 CPU tensor.
    """
    if _BACKEND == "scipy":
        sampler = _ScipyLHS(d=n_dims, seed=seed)
        arr = sampler.random(n=n_points)          # (n_points, n_dims) ndarray
        return torch.from_numpy(arr).float()
    else:
        import numpy as np
        arr = _pyDOE2.lhs(n_dims, samples=n_points, random_state=seed)
        return torch.from_numpy(arr.astype("float32"))


# ---------------------------------------------------------------------------
# Domain descriptor
# ---------------------------------------------------------------------------
@dataclass
class CollocationDomain:
    """Physical domain bounds for collocation sampling (all nondimensional).

    Attributes
    ----------
    L_plate_star : float
        Upper bound of the z_star domain (= plate thickness / L_c).
        For a 1 mm Cu plate with L_c ~ 2.5 mm → L_plate_star ≈ 0.4.
        You can also pass the ratio directly here.
    q_star_min, q_star_max : float
        Nondim heat-flux range. Used only when ``sample_operating=True``.
    dT_sub_star_min, dT_sub_star_max : float
        Nondim subcooling range. Used only when ``sample_operating=True``.
    """
    L_plate_star:      float = 1.0
    q_star_min:        float = 0.001
    q_star_max:        float = 0.10
    dT_sub_star_min:   float = 0.0
    dT_sub_star_max:   float = 0.05


# ---------------------------------------------------------------------------
# Main sampler class
# ---------------------------------------------------------------------------
class LHSCollocationSampler:
    """Latin Hypercube collocation point generator for the ONB PINN.

    Usage
    -----
    ::

        sampler = LHSCollocationSampler(
            domain=CollocationDomain(L_plate_star=0.4),
            sample_operating=True,
        )
        z_star, operating = sampler.sample(n_points=2000, seed=0)
        # z_star   : (2000, 1) float32   — spatial coordinate
        # operating: (2000, 2) float32   — (q_star, dT_sub_star)

    When ``sample_operating=False``, ``operating`` is None.

    Parameters
    ----------
    domain : CollocationDomain
    sample_operating : bool
        If True, also sample (q_star, dT_sub_star) in addition to z_star.
    device : str | torch.device
        Target device for returned tensors (default 'cpu').
    dtype : torch.dtype
        Default float32.
    """

    def __init__(
        self,
        domain: CollocationDomain | None = None,
        *,
        sample_operating: bool = False,
        device: str | torch.device = "cpu",
        dtype: torch.dtype = torch.float32,
    ) -> None:
        self.domain = domain if domain is not None else CollocationDomain()
        self.sample_operating = bool(sample_operating)
        self.device = torch.device(device)
        self.dtype = dtype

    # -----------------------------------------------------------------------
    # core sample method
    # -----------------------------------------------------------------------
    def sample(
        self,
        n_points: int,
        seed: int = 0,
    ) -> tuple[torch.Tensor, torch.Tensor | None]:
        """Generate LHS collocation points.

        Parameters
        ----------
        n_points : int
            Number of collocation points.
        seed : int
            RNG seed for reproducibility.

        Returns
        -------
        z_star : (n_points, 1) float32 tensor
            Nondimensional spatial coordinate, z_star ∈ [0, L_plate_star].
            The tensor does NOT have ``requires_grad`` set — callers should
            set ``z_star.requires_grad_(True)`` before passing to the PDE loss.
        operating : (n_points, 2) float32 tensor or None
            Columns: (q_star, dT_sub_star).
            None when ``sample_operating=False``.
        """
        n_dims = 3 if self.sample_operating else 1
        unit = _lhs_unit(n_points, n_dims, seed)   # (n_points, n_dims) in [0,1)

        d = self.domain

        # z_star: scale from [0,1) to [0, L_plate_star)
        z_star = unit[:, 0:1] * d.L_plate_star  # (n_points, 1)
        z_star = z_star.to(device=self.device, dtype=self.dtype)

        if not self.sample_operating:
            return z_star, None

        # q_star
        q_star = unit[:, 1:2] * (d.q_star_max - d.q_star_min) + d.q_star_min

        # dT_sub_star
        dT_sub = unit[:, 2:3] * (d.dT_sub_star_max - d.dT_sub_star_min) + d.dT_sub_star_min

        operating = torch.cat([q_star, dT_sub], dim=-1)
        operating = operating.to(device=self.device, dtype=self.dtype)

        return z_star, operating

    # -----------------------------------------------------------------------
    # convenience: sample z_star only (used in Phase 1 PDE-only warm-up)
    # -----------------------------------------------------------------------
    def sample_spatial(self, n_points: int, seed: int = 0) -> torch.Tensor:
        """Return only z_star, ignoring ``sample_operating``."""
        unit = _lhs_unit(n_points, 1, seed)
        z_star = unit * self.domain.L_plate_star
        return z_star.to(device=self.device, dtype=self.dtype)

    # -----------------------------------------------------------------------
    # convenience: boundary point tensors at z*=0 and z*=L*
    # -----------------------------------------------------------------------
    def boundary_points(
        self,
        n_points: int,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """Return (z_low, z_high) boundary tensors.

        z_low  = zeros (heated wall)
        z_high = L_plate_star (bulk side)

        Both have shape (n_points, 1) and are on the configured device.
        """
        z_low  = torch.zeros(n_points, 1, device=self.device, dtype=self.dtype)
        z_high = torch.full(
            (n_points, 1), self.domain.L_plate_star,
            device=self.device, dtype=self.dtype,
        )
        return z_low, z_high

    # -----------------------------------------------------------------------
    # helper: compute L_plate_star from physical inputs
    # -----------------------------------------------------------------------
    @staticmethod
    def compute_L_plate_star(L_plate_m: float, L_c_m: float) -> float:
        """Nondim plate thickness = L_plate_m / L_c_m."""
        if L_c_m <= 0.0:
            raise ValueError(f"L_c_m must be > 0, got {L_c_m}")
        return L_plate_m / L_c_m


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    print("=" * 60)
    print("LHSCollocationSampler self-test")
    print(f"  backend: {_BACKEND}")
    print("=" * 60)

    # Compute L_plate_star for 1 mm Cu plate, water at 1 atm
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from utils.nondim import scales_for  # type: ignore[import]

    scales = scales_for("water", P=101_325.0)
    L_c = scales.L_c
    L_plate = 1.0e-3   # 1 mm
    L_plate_star = LHSCollocationSampler.compute_L_plate_star(L_plate, L_c)
    print(f"\n  L_c             = {L_c * 1e3:.4f} mm")
    print(f"  L_plate_star    = {L_plate_star:.4f}  (= {L_plate*1e3} mm / {L_c*1e3:.4f} mm)")

    domain = CollocationDomain(
        L_plate_star=L_plate_star,
        q_star_min=0.001, q_star_max=0.10,
        dT_sub_star_min=0.0, dT_sub_star_max=0.05,
    )

    sampler = LHSCollocationSampler(domain=domain, sample_operating=True)
    z_star, operating = sampler.sample(n_points=2000, seed=42)
    print(f"\n  z_star  shape={tuple(z_star.shape)}  "
          f"min={z_star.min().item():.5f}  max={z_star.max().item():.5f}")
    assert z_star.min().item() >= 0.0
    assert z_star.max().item() <= L_plate_star + 1e-6
    assert operating is not None
    print(f"  operating shape={tuple(operating.shape)}  "
          f"q* range=[{operating[:,0].min():.4f}, {operating[:,0].max():.4f}]  "
          f"dT_sub* range=[{operating[:,1].min():.4f}, {operating[:,1].max():.4f}]")

    # spatial-only sampler (Phase 1 warm-up)
    sampler2 = LHSCollocationSampler(domain=domain, sample_operating=False)
    z2, op2 = sampler2.sample(n_points=5000, seed=0)
    assert op2 is None
    print(f"\n  spatial-only: z_star shape={tuple(z2.shape)}  operating={op2}")

    # boundary points
    z_low, z_high = sampler.boundary_points(n_points=32)
    print(f"  z_low  shape={tuple(z_low.shape)}  all-zero={bool((z_low == 0).all())}")
    print(f"  z_high shape={tuple(z_high.shape)}  val={z_high[0].item():.4f} (= L_plate_star)")

    print("\n[lhs_sampler] self-test PASSED")
