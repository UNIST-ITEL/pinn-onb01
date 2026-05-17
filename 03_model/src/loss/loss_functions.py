"""
loss_functions.py — 4-term composite loss for the pool-boiling ONB PINN.

Section 4.3 (Phase A) — 1D steady heat conduction with surface conditioning.

The full training objective is

    L_total = w_conduction * L_conduction
            + w_bc        * (L_bc_low + L_bc_high)
            + w_data      * (L_data_dT + L_data_q)
            + w_onb       * L_onb

with each term implemented as an independent, autograd-friendly function so
that:
  * weight tuning / GradNorm-style adaptation is easy,
  * MLflow logs each component separately for diagnostics,
  * physical violations are localised (e.g. is the heated wall BC bad, or is
    the Hsu cavity criterion infeasible?).

Phase A simplifications (relaxed in Phase B/C):
  * 1D PDE   d^2 T* / d z*^2 = 0 (no volumetric heat source).
  * Heated wall BC at z* = 0:   -k_l_star * dT*/dz* = q_flux_applied_star
    (note: in the nondimensional system, k_l_star factor is absorbed into
    q_ref scaling — see properties of NondimScales in utils.nondim).
  * Top BC at z* = L*:          T*(L*) = T_bulk_star  (Dirichlet).
  * L_onb uses Hsu's discriminant > 0 as a soft constraint
    (a stronger (r_c_min < r_c_pred < r_c_max) constraint will be activated
    once r_c is recovered from the inverse problem in Phase 4).

Variable / unit conventions follow CLAUDE.md:
  * SI units throughout for dimensional helpers,
  * `_star` suffix denotes nondimensional quantities,
  * temperatures in K, lengths in m, fluxes in W/m^2 (when dimensional).

Authors: PINN-ONB01 project (loss-functions agent)
Date   : 2026-05-10
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import torch
from torch import nn

from ..model.pinn import PINNOutputs, PoolBoilingPINN
from ..utils.nondim import NondimScales
from ..utils.properties import SaturationProperties, saturation_properties

if TYPE_CHECKING:  # avoid hard import cycles for type checkers only
    pass


# ---------------------------------------------------------------------------
# Bookkeeping containers
# ---------------------------------------------------------------------------
@dataclass
class LossComponents:
    """All scalar loss tensors for one training step.

    Each field is a 0-d ``torch.Tensor`` so that callers can ``.backward()``
    after weighted summation, or log per-component values via
    ``.detach().item()``.
    """

    L_conduction: torch.Tensor
    L_bc_low:     torch.Tensor
    L_bc_high:    torch.Tensor
    L_data_dT:    torch.Tensor
    L_data_q:     torch.Tensor
    L_onb:        torch.Tensor

    # ---- convenience -----------------------------------------------------
    def as_dict(self) -> dict[str, torch.Tensor]:
        return {
            "L_conduction": self.L_conduction,
            "L_bc_low":     self.L_bc_low,
            "L_bc_high":    self.L_bc_high,
            "L_data_dT":    self.L_data_dT,
            "L_data_q":     self.L_data_q,
            "L_onb":        self.L_onb,
        }

    def detach_dict(self) -> dict[str, float]:
        """Return Python floats — for MLflow / printing."""
        return {k: float(v.detach().cpu().item()) for k, v in self.as_dict().items()}


@dataclass
class LossWeights:
    """Scalar weights for the four-term composite loss.

    Defaults reflect Section 4.3 guidance for Phase A:
      * BC must hold tightly for the PDE to be physically meaningful,
      * data fit is the primary supervisory signal (only 48 ONB points),
      * the Hsu soft constraint is ramped up gradually during Phase 3
        (start at 0.1 -> 1.0 -> 10.0 across training).
    """

    w_conduction: float = 1.0
    w_bc:         float = 10.0
    w_data:       float = 100.0
    w_onb:        float = 1.0


# ---------------------------------------------------------------------------
# Numerical guards
# ---------------------------------------------------------------------------
def _check_finite(t: torch.Tensor, name: str) -> None:
    """Raise immediately on inf/NaN in a loss tensor.

    Per CLAUDE.md instructions, loss values must never be silently inf/NaN —
    we want the training loop to halt with diagnostic context.
    """
    if not torch.isfinite(t).all():
        n_nan = int(torch.isnan(t).sum().item())
        n_inf = int(torch.isinf(t).sum().item())
        raise FloatingPointError(
            f"Non-finite values in '{name}': "
            f"shape={tuple(t.shape)}, NaN={n_nan}, Inf={n_inf}, "
            f"min={t.min().item() if t.numel() else 'n/a'}, "
            f"max={t.max().item() if t.numel() else 'n/a'}"
        )


# ===========================================================================
# 1. L_conduction  (PDE residual: d^2 T*/d z*^2 = 0)
# ===========================================================================
def loss_conduction(
    pinn: PoolBoilingPINN,
    spatial_z: torch.Tensor,
    z_surface_cached: torch.Tensor,
    operating: torch.Tensor | None = None,
    q_source_star: float = 0.0,
) -> torch.Tensor:
    """1D steady heat-conduction PDE residual: ``d^2T*/dz*^2 + q'''*/k* = 0``.

    Physical meaning: the predicted nondimensional temperature field along the
    heater thickness must satisfy Laplace's equation. With no volumetric heat
    source (Phase A), this collapses to ``d^2 T*/d z*^2 = 0`` — i.e., the
    profile must be linear in z*, which is the analytical signature of pure
    1D conduction with surface flux + Dirichlet top BC.

    Parameters
    ----------
    pinn : PoolBoilingPINN
        The model. We use ``forward_for_pde`` so that the surface latent is
        cached once per step (it does not depend on z*).
    spatial_z : (N, 1) float tensor, **requires_grad=True**
        Collocation points along the heater thickness (nondimensional).
    z_surface_cached : (N, latent_dim) float tensor
        Pre-computed surface latent — output of ``pinn.encoder(...)``.
    operating : (N, operating_dim) float tensor or None
        Optional operating-condition vector.
    q_source_star : float
        Nondimensional volumetric heat source (default 0 — Phase A).

    Returns
    -------
    torch.Tensor
        Scalar 0-d tensor: mean-squared residual.
    """
    if not spatial_z.requires_grad:
        raise ValueError(
            "spatial_z must have requires_grad=True for autograd-based "
            "PDE residual evaluation."
        )

    T_star = pinn.forward_for_pde(spatial_z, z_surface_cached, operating)

    grad_T = torch.autograd.grad(
        outputs=T_star,
        inputs=spatial_z,
        grad_outputs=torch.ones_like(T_star),
        create_graph=True,
        retain_graph=True,
    )[0]
    grad2_T = torch.autograd.grad(
        outputs=grad_T,
        inputs=spatial_z,
        grad_outputs=torch.ones_like(grad_T),
        create_graph=True,
        retain_graph=True,
    )[0]

    residual = grad2_T + q_source_star
    loss = (residual ** 2).mean()
    _check_finite(loss, "L_conduction")
    return loss


# ===========================================================================
# 2. L_BC  (Neumann at heated wall + Dirichlet at bulk-side)
# ===========================================================================
def loss_bc(
    pinn: PoolBoilingPINN,
    z_boundary_low: torch.Tensor,
    z_boundary_high: torch.Tensor,
    z_surface_cached_low: torch.Tensor,
    z_surface_cached_high: torch.Tensor,
    q_flux_applied_star: torch.Tensor,
    T_bulk_star: torch.Tensor,
    operating_low: torch.Tensor | None = None,
    operating_high: torch.Tensor | None = None,
    k_l_star: float = 1.0,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Boundary-condition residuals at heater bottom (z*=0) and top (z*=L*).

    Physical meaning:
      * **Bottom (heated wall):** prescribed heat flux,
        ``-k_l_star * dT*/dz*|_{z*=0}  =  q_flux_applied_star``.
        This couples the imposed experimental heat flux to the temperature
        gradient that the network must produce.
      * **Top (bulk side):** Dirichlet — ``T*(L*) = T_bulk_star``.  Since the
        bulk-side temperature is approximately the saturated/subcooled bulk
        temperature in pool boiling experiments, we anchor the profile here.

    Parameters
    ----------
    pinn : PoolBoilingPINN
    z_boundary_low : (M, 1) tensor, **requires_grad=True**
        Coordinates at the heated wall (typically all = 0 in nondim units).
    z_boundary_high : (M, 1) tensor
        Coordinates at the bulk-side wall (typically all = L*).
    z_surface_cached_low / _high : (M, latent_dim) tensors
        Pre-computed surface latents matching each boundary batch.
    q_flux_applied_star : (M, 1) tensor
        Applied heat flux (nondimensional) at the heated wall.
    T_bulk_star : (M, 1) tensor
        Nondimensional bulk-side temperature target.
    operating_low / _high : (M, operating_dim) tensors or None
        Operating-condition vectors aligned with each boundary batch.
    k_l_star : float
        Nondimensional liquid (or solid heater) thermal conductivity factor
        in the Neumann condition. Defaults to 1.0 — we assume the
        nondimensionalisation already absorbs the conductivity into q_ref.

    Returns
    -------
    (loss_low, loss_high) : tuple of 0-d tensors
        MSEs at the two boundaries, returned separately so that the
        training loop can detect which boundary diverges.
    """
    # --- Bottom (Neumann) ------------------------------------------------
    if not z_boundary_low.requires_grad:
        raise ValueError(
            "z_boundary_low must have requires_grad=True (Neumann BC needs "
            "dT*/dz* via autograd)."
        )

    T_low = pinn.forward_for_pde(
        z_boundary_low, z_surface_cached_low, operating_low,
    )
    grad_T_low = torch.autograd.grad(
        outputs=T_low,
        inputs=z_boundary_low,
        grad_outputs=torch.ones_like(T_low),
        create_graph=True,
        retain_graph=True,
    )[0]
    # -k * dT/dz = q  ->  residual = -k * dT/dz - q
    residual_low = -k_l_star * grad_T_low - q_flux_applied_star
    loss_low = (residual_low ** 2).mean()

    # --- Top (Dirichlet) -------------------------------------------------
    T_high = pinn.forward_for_pde(
        z_boundary_high, z_surface_cached_high, operating_high,
    )
    residual_high = T_high - T_bulk_star
    loss_high = (residual_high ** 2).mean()

    _check_finite(loss_low,  "L_bc_low")
    _check_finite(loss_high, "L_bc_high")
    return loss_low, loss_high


# ===========================================================================
# 3. L_data  (experimental ONB targets)
# ===========================================================================
def loss_data(
    pinn_outputs: PINNOutputs,
    target_delta_T_onb_star: torch.Tensor,
    target_q_onb_star: torch.Tensor,
    weight_dT: float = 1.0,
    weight_q:  float = 1.0,
    sample_weight: torch.Tensor | None = None,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Mean-squared error between predicted and observed ONB pairs.

    Physical meaning: the network's nondimensional ``delta_T_onb_star`` and
    ``q_onb_star`` heads must reproduce the 48 experimental ONB points
    (Section 4.3 — primary supervision signal).

    Parameters
    ----------
    pinn_outputs : PINNOutputs
    target_delta_T_onb_star : (N, 1) tensor — nondim experimental superheat.
    target_q_onb_star       : (N, 1) tensor — nondim experimental heat flux.
    weight_dT, weight_q : float
        Per-channel scalar weights (kept separate for diagnostic use).
    sample_weight : (N, 1) tensor or None
        Optional per-sample weight (e.g. inverse measurement variance).

    Returns
    -------
    (loss_dT, loss_q) : tuple of 0-d tensors
        Returned separately so that the training loop can monitor which
        channel is harder to fit.
    """
    pred_dT = pinn_outputs.delta_T_onb_star
    pred_q  = pinn_outputs.q_onb_star

    if pred_dT.shape != target_delta_T_onb_star.shape:
        raise ValueError(
            f"Shape mismatch (dT): pred={tuple(pred_dT.shape)} "
            f"vs target={tuple(target_delta_T_onb_star.shape)}"
        )
    if pred_q.shape != target_q_onb_star.shape:
        raise ValueError(
            f"Shape mismatch (q): pred={tuple(pred_q.shape)} "
            f"vs target={tuple(target_q_onb_star.shape)}"
        )

    se_dT = (pred_dT - target_delta_T_onb_star) ** 2
    se_q  = (pred_q  - target_q_onb_star) ** 2

    if sample_weight is not None:
        if sample_weight.shape != pred_dT.shape:
            raise ValueError(
                f"sample_weight shape {tuple(sample_weight.shape)} "
                f"must match prediction shape {tuple(pred_dT.shape)}"
            )
        se_dT = se_dT * sample_weight
        se_q  = se_q  * sample_weight

    loss_dT = weight_dT * se_dT.mean()
    loss_q  = weight_q  * se_q.mean()

    _check_finite(loss_dT, "L_data_dT")
    _check_finite(loss_q,  "L_data_q")
    return loss_dT, loss_q


# ===========================================================================
# 4. L_onb  (Hsu nucleation criterion — soft constraint)
# ===========================================================================
def _hsu_discriminant_torch(
    delta_T_wall: torch.Tensor,
    q_flux:       torch.Tensor,
    sigma:        torch.Tensor,
    T_sat:        torch.Tensor,
    cp_l:         torch.Tensor,
    rho_v:        torch.Tensor,
    h_fg:         torch.Tensor,
    k_l:          torch.Tensor,
    eps:          float = 1e-30,
) -> torch.Tensor:
    """Differentiable form of Hsu (1962) eq. 13 discriminant.

        delta_t   = k_l * delta_T_wall / q_flux                       [m]
        D         = 1 - 8 * sigma * T_sat * cp_l
                     / (rho_v * h_fg^2 * delta_t)

    A non-negative discriminant means a feasible cavity-radius range
    ``(r_c_min, r_c_max)`` exists -> ONB can occur. We return the discriminant
    itself (signed) so the calling loss can apply a hinge.
    """
    delta_t = k_l * delta_T_wall / torch.clamp(q_flux, min=eps)
    denom   = rho_v * h_fg ** 2 * torch.clamp(delta_t, min=eps)
    D = 1.0 - (8.0 * sigma * T_sat * cp_l) / torch.clamp(denom, min=eps)
    return D


def _build_props_tensor(
    fluids: list[str],
    pressures: list[float],
    nondim_scales_per_fluid: dict[str, NondimScales],
    *,
    device: torch.device,
    dtype:  torch.dtype,
) -> dict[str, torch.Tensor]:
    """Vectorise SaturationProperties into per-sample tensors.

    For Phase A all samples are at atmospheric pressure for a given fluid,
    so we look up properties once per (fluid, P) pair via the cached
    ``saturation_properties`` and broadcast.
    """
    sigma  = []
    T_sat  = []
    cp_l   = []
    rho_v  = []
    h_fg   = []
    k_l    = []
    delta_T_ref = []
    q_ref       = []

    for f, P in zip(fluids, pressures):
        props = saturation_properties(f, P=P)
        sigma.append(props.sigma)
        T_sat.append(props.T_sat)
        cp_l.append(props.cp_l)
        rho_v.append(props.rho_v)
        h_fg.append(props.h_fg)
        k_l.append(props.k_l)
        if f in nondim_scales_per_fluid:
            sc = nondim_scales_per_fluid[f]
        else:
            from ..utils.nondim import compute_scales
            sc = compute_scales(props)
        delta_T_ref.append(sc.delta_T_ref)
        q_ref.append(sc.q_ref)

    def _t(values: list[float]) -> torch.Tensor:
        return torch.tensor(values, device=device, dtype=dtype).unsqueeze(-1)

    return {
        "sigma":       _t(sigma),
        "T_sat":       _t(T_sat),
        "cp_l":        _t(cp_l),
        "rho_v":       _t(rho_v),
        "h_fg":        _t(h_fg),
        "k_l":         _t(k_l),
        "delta_T_ref": _t(delta_T_ref),
        "q_ref":       _t(q_ref),
    }


def loss_onb_hsu(
    pinn_outputs: PINNOutputs,
    fluids: list[str],
    pressures: list[float],
    nondim_scales_per_fluid: dict[str, NondimScales],
    *,
    margin: float = 0.1,
    eps: float = 1e-30,
) -> torch.Tensor:
    """Hsu nucleation criterion as a soft constraint on (delta_T_onb, q_onb).

    Phase A formulation: enforce that the Hsu discriminant is non-negative —
    i.e., a feasible active cavity range ``(r_c_min, r_c_max)`` exists at the
    predicted (delta_T_pred, q_pred). Without this, the predicted operating
    point cannot physically support nucleation.

    Hinge form (no penalty when D >= margin):

        L_onb = mean( ReLU(margin - D)^2 )

    where ``D`` is the Hsu (1962) eq. 13 discriminant computed from the
    *dimensional* network predictions:

        delta_T_pred [K]  = delta_T_onb_star * delta_T_ref(fluid)
        q_pred      [W/m^2] = q_onb_star      * q_ref(fluid)

    Parameters
    ----------
    pinn_outputs : PINNOutputs
        Must have positive ``delta_T_onb_star`` and ``q_onb_star`` (guaranteed
        by softplus heads in PoolBoilingPINN).
    fluids : list[str] of length N
        Fluid label per sample, used to look up CoolProp saturation properties.
    pressures : list[float] of length N
        Operating pressure per sample [Pa].
    nondim_scales_per_fluid : dict[str, NondimScales]
        Pre-computed scales for batch dimensionalisation. Missing fluids are
        recomputed on the fly.
    margin : float
        Soft margin on the discriminant (recommend 0.05 - 0.1 in Phase A).
    eps : float
        Numerical guard for divisions.

    Returns
    -------
    torch.Tensor
        Scalar 0-d tensor.

    Notes
    -----
    * Phase 4 upgrade: when r_c is recovered from the inverse problem,
      replace this with the stronger constraint
      ``relu(r_c_min - r_c_pred - m)^2 + relu(r_c_pred - r_c_max - m)^2``.
    * delta_T_onb_star and q_onb_star are guaranteed > 0 by the softplus
      output heads, so no extra positivity penalty is needed here.
    """
    pred_dT_star = pinn_outputs.delta_T_onb_star  # (N, 1)
    pred_q_star  = pinn_outputs.q_onb_star        # (N, 1)

    if pred_dT_star.shape[0] != len(fluids) or pred_q_star.shape[0] != len(fluids):
        raise ValueError(
            f"Batch size mismatch: predictions have {pred_dT_star.shape[0]} "
            f"samples, but fluids list has {len(fluids)}."
        )
    if len(fluids) != len(pressures):
        raise ValueError(
            f"len(fluids)={len(fluids)} must equal len(pressures)={len(pressures)}"
        )

    if (pred_dT_star <= 0.0).any():
        raise ValueError(
            "Negative or zero delta_T_onb_star encountered — output head must "
            "be positive (use softplus). Check PoolBoilingPINN configuration."
        )
    if (pred_q_star <= 0.0).any():
        raise ValueError(
            "Negative or zero q_onb_star encountered — output head must be "
            "positive (use softplus)."
        )

    device = pred_dT_star.device
    dtype  = pred_dT_star.dtype

    props_t = _build_props_tensor(
        fluids, pressures, nondim_scales_per_fluid,
        device=device, dtype=dtype,
    )

    # Re-dimensionalise the network predictions for the Hsu equation.
    delta_T_dim = pred_dT_star * props_t["delta_T_ref"]   # [K]
    q_dim       = pred_q_star  * props_t["q_ref"]         # [W/m^2]

    D = _hsu_discriminant_torch(
        delta_T_wall=delta_T_dim,
        q_flux      =q_dim,
        sigma       =props_t["sigma"],
        T_sat       =props_t["T_sat"],
        cp_l        =props_t["cp_l"],
        rho_v       =props_t["rho_v"],
        h_fg        =props_t["h_fg"],
        k_l         =props_t["k_l"],
        eps         =eps,
    )
    # Hinge: penalise samples where discriminant < margin.
    hinge = torch.relu(margin - D)
    loss = (hinge ** 2).mean()
    _check_finite(loss, "L_onb")
    return loss


# ===========================================================================
# 4b. L_monotonicity  (synthetic sweep regularization for trends)
# ===========================================================================
def loss_monotonicity(
    pinn: PoolBoilingPINN,
    sweep_kind: str,                     # "Ra" or "theta"
    *,
    n_points: int = 20,
    q_star: float = 0.02,                # representative nondim q'' (≈ 1-3 kW/m²)
    delta_T_sub_star: float = 0.0,
    L_c_m: float = 2.5e-3,               # water capillary length (for Ra_log_star)
    category_id: int = 0,                # neutral category
    device: torch.device | None = None,
) -> torch.Tensor:
    """Penalize non-monotonic ΔT_ONB along a synthetic surface sweep.

    Physical expectation (verified by R-134a/R-123 JABARDO data):
      * Ra ↑ → ΔT_ONB ↓ (rougher surface has lower ONB superheat)
      * θ ↑ → ΔT_ONB ↓ (more hydrophobic → easier nucleation)

    The sweep is *synthetic*: a (n_points,) batch where ONLY the swept axis
    varies, all other surface channels held at neutral defaults. This avoids
    contradicting the data (which has confounding co-variation in
    surface/fluid pairs) by regularising on **counterfactual** surfaces.

    Returns a 0-d tensor — hinge penalty on consecutive non-decreasing pairs.
    """
    if device is None:
        device = next(pinn.parameters()).device

    # SurfaceEncoder numeric channel layout (encode_features_to_tensor):
    #  0 Ra_log_um   1 Ra_log_star   2 cos_theta   3 theta_norm   4 theta_mask
    #  5 r_c_log_star  6 r_c_mask  7 N_s_log_norm  8 N_s_mask
    B = n_points
    numeric = torch.zeros(B, 9, device=device)
    # Defaults: theta=90° (neutral), no r_c/N_s mask
    numeric[:, 2] = 0.0          # cos(90)=0
    numeric[:, 3] = 0.5          # 90/180
    numeric[:, 4] = 1.0          # theta_mask
    cat = torch.full((B,), category_id, dtype=torch.long, device=device)

    if sweep_kind == "Ra":
        # log-uniform Ra in [0.01, 50] μm
        Ra_um = torch.logspace(-2.0, math.log10(50.0), B, device=device)
        Ra_m = Ra_um * 1e-6
        numeric[:, 0] = torch.log10(Ra_um)                        # log10(Ra in μm)
        numeric[:, 1] = torch.log10(Ra_m / L_c_m)                 # log10(Ra/L_c)
        x_axis = Ra_um
    elif sweep_kind == "theta":
        # linear θ in [10, 170] degrees
        theta_deg = torch.linspace(10.0, 170.0, B, device=device)
        theta_rad = theta_deg * (math.pi / 180.0)
        numeric[:, 2] = torch.cos(theta_rad)
        numeric[:, 3] = theta_rad / math.pi
        # Set Ra to a moderate default (0.5 μm)
        numeric[:, 0] = math.log10(0.5)
        numeric[:, 1] = math.log10(0.5e-6 / L_c_m)
        x_axis = theta_deg
    else:
        raise ValueError(f"sweep_kind must be 'Ra' or 'theta', got '{sweep_kind}'")

    operating = torch.zeros(B, pinn.operating_dim, device=device)
    operating[:, 0] = q_star
    operating[:, 1] = delta_T_sub_star

    z_query = torch.zeros(B, 1, device=device)
    surface_features = {"numeric": numeric, "category_id": cat}
    out = pinn(z_query, surface_features, operating)

    dT = out.delta_T_onb_star.squeeze(-1)               # (B,)
    diffs = dT[1:] - dT[:-1]                            # (B-1,)
    # Expect ΔT_ONB to decrease (diffs < 0) along increasing x. Penalize positive diffs.
    hinge = torch.relu(diffs)
    loss = (hinge ** 2).mean()
    _check_finite(loss, f"L_monotonicity_{sweep_kind}")
    return loss


# ===========================================================================
# 5. Total loss
# ===========================================================================
def total_loss(
    components: LossComponents,
    weights: LossWeights,
) -> torch.Tensor:
    """Weighted sum of the four loss families (Section 4.3).

    Returns
    -------
    torch.Tensor
        Scalar 0-d tensor, ready for ``.backward()``.
    """
    L = (
        weights.w_conduction * components.L_conduction
        + weights.w_bc      * (components.L_bc_low + components.L_bc_high)
        + weights.w_data    * (components.L_data_dT + components.L_data_q)
        + weights.w_onb     * components.L_onb
    )
    _check_finite(L, "L_total")
    return L


# ===========================================================================
# Self-test (smoke check) — runs all six functions on a tiny synthetic batch.
# ===========================================================================
if __name__ == "__main__":
    print("=" * 72)
    print("Loss-functions smoke test")
    print("=" * 72)

    torch.manual_seed(0)

    # ---- Build a tiny PINN -----------------------------------------------
    pinn = PoolBoilingPINN(
        latent_dim=16, hidden_dim=32, n_layers=3,
        activation="tanh", conditioning="concat", seed=0,
    )
    pinn.eval()

    # ---- Synthetic surface batch (3 samples, water at 1 atm) -------------
    from ..model.surface_encoder import (
        SurfaceFeatures,
        encode_batch_to_tensors,
    )
    from ..utils.nondim import scales_for

    feats = [
        SurfaceFeatures(
            Ra_m=1e-6, theta_rad=math.radians(45.0),
            category_id=1, surface_id=f"SYN-{i:03d}", fluid="water",
        )
        for i in range(3)
    ]
    surface_features = encode_batch_to_tensors(feats)
    fluids    = [f.fluid for f in feats]
    pressures = [101_325.0] * len(feats)

    scales_lookup = {"water": scales_for("water", P=101_325.0)}

    # Pre-encode the surface latent so we can call forward_for_pde at any z*
    with torch.no_grad():
        z_surface = pinn.encoder(surface_features)         # (3, 16)

    # ---- (1) L_conduction -------------------------------------------------
    spatial_z = torch.linspace(0.0, 1.0, 3).unsqueeze(-1).requires_grad_(True)
    operating = torch.zeros(3, pinn.operating_dim)
    L_pde = loss_conduction(pinn, spatial_z, z_surface, operating)
    print(f"\n[1] L_conduction = {L_pde.item():.6e}    "
          f"finite={torch.isfinite(L_pde).item()}    >=0={L_pde.item() >= 0.0}")

    # ---- (2) L_bc ---------------------------------------------------------
    z_low  = torch.zeros(3, 1, requires_grad=True)
    z_high = torch.ones(3, 1)
    q_flux_applied_star = torch.full((3, 1), 0.01)        # nondim heat flux
    T_bulk_star         = torch.full((3, 1), -0.05)       # nondim bulk T
    L_bc_low, L_bc_high = loss_bc(
        pinn,
        z_boundary_low=z_low,
        z_boundary_high=z_high,
        z_surface_cached_low=z_surface,
        z_surface_cached_high=z_surface,
        q_flux_applied_star=q_flux_applied_star,
        T_bulk_star=T_bulk_star,
        operating_low=operating,
        operating_high=operating,
        k_l_star=1.0,
    )
    print(f"[2] L_bc_low     = {L_bc_low.item():.6e}    "
          f"L_bc_high = {L_bc_high.item():.6e}")

    # ---- (3) L_data -------------------------------------------------------
    out = pinn(spatial_z, surface_features, operating)
    target_dT = torch.full_like(out.delta_T_onb_star, 0.05)
    target_q  = torch.full_like(out.q_onb_star,       0.02)
    L_data_dT, L_data_q = loss_data(out, target_dT, target_q)
    print(f"[3] L_data_dT    = {L_data_dT.item():.6e}    "
          f"L_data_q  = {L_data_q.item():.6e}")

    # ---- (4) L_onb (Hsu) --------------------------------------------------
    L_hsu = loss_onb_hsu(
        out,
        fluids=fluids,
        pressures=pressures,
        nondim_scales_per_fluid=scales_lookup,
        margin=0.1,
    )
    print(f"[4] L_onb        = {L_hsu.item():.6e}")

    # ---- (5) Total + backward ---------------------------------------------
    components = LossComponents(
        L_conduction=L_pde,
        L_bc_low=L_bc_low,
        L_bc_high=L_bc_high,
        L_data_dT=L_data_dT,
        L_data_q=L_data_q,
        L_onb=L_hsu,
    )
    weights = LossWeights()  # defaults
    L_total = total_loss(components, weights)
    print(f"\n[5] L_total      = {L_total.item():.6e}")

    # backward — everything must connect to the parameter graph
    L_total.backward()
    n_with_grad = sum(
        1 for p in pinn.parameters() if p.grad is not None and p.grad.abs().sum() > 0
    )
    n_total = sum(1 for _ in pinn.parameters())
    print(f"[6] params with non-zero grad: {n_with_grad} / {n_total}")

    # ---- Sanity assertions ------------------------------------------------
    for name, val in components.detach_dict().items():
        assert math.isfinite(val), f"{name} is not finite: {val}"
        assert val >= 0.0,         f"{name} is negative: {val}"
    assert math.isfinite(L_total.item()) and L_total.item() >= 0.0
    assert n_with_grad > 0, "No parameters received gradients — check graph connectivity."

    print("\n[ok] all six losses finite, non-negative, and autograd-compatible.")
