"""
loss_functions.py — Phase 2 flow boiling ONB PINN loss functions.

M4 scope (implemented):
    L_data_q      : log-MSE on q_onb predictions (rows with has_q)
    L_data_dT     : MSE on delta_T_onb predictions (rows with has_dT)
    L_hsu_flow    : flow-aware Hsu nucleation criterion soft constraint
    L_mono_Re     : monotonicity Re↑ → ΔT_ONB↓
    L_mono_G      : monotonicity G↑  → ΔT_ONB↓
    L_mono_sub    : monotonicity ΔT_sub↑ → ΔT_ONB↑

M7-M9 stubs (return zero; activated when w > 0):
    L_continuity  : ∇·(ρu) = 0
    L_momentum    : NS x-momentum residual
    L_energy      : energy equation residual

Physical basis:
    Hsu criterion (flow-aware):
        δ_t = C_hsu × D_h / Nu,  Nu = 0.023 Re^0.8 Pr^0.4  (Dittus-Boelter)
        D = 1 - 8 σ T_sat c_pl / (ρ_v h_fg² δ_t)  (nucleation discriminant ≥ 0 at ONB)
        Loss = mean(ReLU(margin - D)²)
"""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

import torch
import torch.nn.functional as F
from torch import Tensor

_SRC = Path(__file__).resolve().parents[1]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from utils.nondim_flow import FlowNondimScales, compute_flow_nondim

if TYPE_CHECKING:
    from model.flow_boiling_pinn import FlowBoilingPINN


# ── Dataclasses ───────────────────────────────────────────────────────────────

@dataclass
class LossComponents:
    L_data_q:      Tensor
    L_data_dT:     Tensor
    L_hsu_flow:    Tensor
    L_hsu_coupling: Tensor
    L_mono_Re:     Tensor
    L_mono_G:      Tensor
    L_mono_sub:    Tensor
    L_continuity:  Tensor
    L_momentum:    Tensor
    L_energy:      Tensor
    total:         Tensor

    def as_dict(self) -> dict[str, float]:
        return {k: float(v.item()) for k, v in self.__dict__.items()}


@dataclass
class LossWeights:
    w_data_q:      float = 1.0
    w_data_dT:     float = 1.0
    w_hsu:         float = 0.5
    w_hsu_coupling: float = 0.0   # Hsu self-consistency: ΔT_pred = Hsu(q_pred)
    w_mono_Re:     float = 0.1
    w_mono_G:      float = 0.1
    w_mono_sub:    float = 0.1
    w_continuity:  float = 0.0
    w_momentum:    float = 0.0
    w_energy:      float = 0.0

    @classmethod
    def from_config(cls, cfg: dict) -> "LossWeights":
        lc = cfg.get("loss", cfg)
        return cls(
            w_data_q=float(lc.get("w_data_q",          1.0)),
            w_data_dT=float(lc.get("w_data_dT",        1.0)),
            w_hsu=float(lc.get("w_hsu",                0.5)),
            w_hsu_coupling=float(lc.get("w_hsu_coupling", 0.0)),
            w_mono_Re=float(lc.get("w_mono_Re",        0.1)),
            w_mono_G=float(lc.get("w_mono_G",          0.1)),
            w_mono_sub=float(lc.get("w_mono_sub",      0.1)),
            w_continuity=float(lc.get("w_continuity",  0.0)),
            w_momentum=float(lc.get("w_momentum",      0.0)),
            w_energy=float(lc.get("w_energy",          0.0)),
        )


# ── Guard ─────────────────────────────────────────────────────────────────────

def _check_finite(t: Tensor, name: str) -> Tensor:
    if not torch.isfinite(t).all():
        n_bad = (~torch.isfinite(t)).sum().item()
        raise ValueError(f"loss_functions: {name} has {n_bad} non-finite values")
    return t


def _safe_finite(t: Tensor, name: str, fallback: float = 0.0) -> Tensor:
    """Like _check_finite but replaces NaN/Inf with fallback instead of crashing."""
    if not torch.isfinite(t).all():
        n_bad = (~torch.isfinite(t)).sum().item()
        import warnings
        warnings.warn(f"loss_functions: {name} has {n_bad} non-finite values — replacing with {fallback}")
        return torch.nan_to_num(t, nan=fallback, posinf=fallback, neginf=fallback)
    return t


# ── Data loss ─────────────────────────────────────────────────────────────────

def loss_data(
    pred_q_onb_star:   Tensor,   # (B,) model prediction, nondim
    pred_dT_onb_star:  Tensor,   # (B,) model prediction, nondim
    true_q_onb_star:   Tensor,   # (B,) ground truth (NaN where unavailable)
    true_dT_onb_star:  Tensor,   # (B,) ground truth (NaN where unavailable)
    has_q:             Tensor,   # (B,) bool
    has_dT:            Tensor,   # (B,) bool
    *,
    log_scale_q: bool = True,
    eps: float = 1e-6,
) -> tuple[Tensor, Tensor]:
    """Return (L_data_q, L_data_dT), each a scalar tensor."""
    device = pred_q_onb_star.device
    zero   = torch.zeros(1, device=device)

    # Flatten predictions to 1-D in case model emits (B, 1)
    pred_q_onb_star  = pred_q_onb_star.squeeze(-1)
    pred_dT_onb_star = pred_dT_onb_star.squeeze(-1)

    # q_onb loss (log-scale MSE to handle order-of-magnitude spread)
    L_q = zero
    if has_q.any():
        mask_q = has_q & torch.isfinite(true_q_onb_star)
        if mask_q.any():
            pq = pred_q_onb_star[mask_q]
            tq = true_q_onb_star[mask_q]
            if log_scale_q:
                L_q = F.mse_loss(
                    torch.log(pq.clamp(min=eps)),
                    torch.log(tq.clamp(min=eps)),
                )
            else:
                L_q = F.mse_loss(pq, tq)

    # delta_T_onb loss (MSE in nondim space)
    L_dT = zero
    if has_dT.any():
        mask_dT = has_dT & torch.isfinite(true_dT_onb_star)
        if mask_dT.any():
            pdt = pred_dT_onb_star[mask_dT]
            tdt = true_dT_onb_star[mask_dT]
            L_dT = F.mse_loss(pdt, tdt)

    return L_q, L_dT


# ── Hsu self-consistency coupling ─────────────────────────────────────────────

def loss_hsu_coupling(
    pred_q_onb_star:  Tensor,   # (B,) or (B,1)  model q prediction (nondim)
    pred_dT_onb_star: Tensor,   # (B,) or (B,1)  model ΔT prediction (nondim)
    C_hsu_nd:         Tensor,   # (B,)  per-sample coefficient (from dataset)
    *,
    eps: float = 1e-6,
) -> Tensor:
    """
    Enforce physical self-consistency between the two model heads.

    Hsu (1962): ΔT_ONB = sqrt(8σ T_sat q / (k_l h_fg ρ_v))
    In nondim:  dT_star = C_hsu_nd * sqrt(q_star)

    Applied to ALL samples — no ground-truth label needed.
    q-only samples (235/378) gain indirect ΔT training signal here.
    """
    q_star  = pred_q_onb_star.squeeze(-1).clamp(min=eps)
    dT_pred = pred_dT_onb_star.squeeze(-1)
    dT_hsu  = C_hsu_nd * torch.sqrt(q_star)
    return F.mse_loss(dT_pred, dT_hsu)


# ── Flow-aware Hsu constraint ─────────────────────────────────────────────────

def _nu_dittus_boelter(Re: Tensor, Pr: Tensor) -> Tensor:
    """Nu = 0.023 Re^0.8 Pr^0.4  (heated wall, turbulent)."""
    return 0.023 * Re.pow(0.8) * Pr.pow(0.4)


def _hsu_discriminant_flow(
    delta_T_onb_K: Tensor,   # (N,) wall superheat at ONB [K]
    q_onb_W_m2:    Tensor,   # (N,) heat flux at ONB [W/m²]
    Re:            Tensor,   # (N,) Reynolds number
    Pr:            Tensor,   # (N,) Prandtl number
    D_h_m:         Tensor,   # (N,) hydraulic diameter [m]
    sc:            FlowNondimScales,
    *,
    C_hsu:    float = 0.5,
    eps:      float = 1e-10,
) -> Tensor:
    """
    Hsu discriminant D = 1 − 8 σ T_sat c_pl / (ρ_v h_fg² δ_t).
    At ONB D should be ≥ 0.  Penalise D < 0 via hinge loss.

    δ_t = C_hsu × D_h / Nu(Re, Pr)    ← flow-modified thermal boundary layer
    """
    # Thermal boundary layer thickness
    Nu    = _nu_dittus_boelter(Re.clamp(min=400.0), Pr.clamp(min=0.5))
    delta_t = C_hsu * D_h_m / Nu.clamp(min=1e-6)

    # Vapour density (ideal gas approximation for ρ_v if not available in scales)
    # Use ρ_v = P_sat / (R_specific * T_sat)  — approximate
    # Better: from CoolProp if available; fallback uses h_fg + Clausius-Clapeyron
    R_water = 461.5  # J/(kg·K) — specific gas constant for water vapour
    P_Pa    = sc.P_kPa * 1e3
    rho_v   = P_Pa / (R_water * sc.T_sat_K)   # approximate for water
    rho_v_t = torch.full_like(delta_t, max(rho_v, 0.01))

    sigma   = sc.sigma
    T_sat   = sc.T_sat_K
    cp_l    = sc.cp_l
    h_fg    = sc.h_fg

    numerator   = 8.0 * sigma * T_sat * cp_l
    denominator = rho_v_t * (h_fg ** 2) * delta_t.clamp(min=eps)

    D = 1.0 - numerator / denominator.clamp(min=eps)
    return D


def loss_hsu_flow(
    model:          "FlowBoilingPINN",
    collocation_batch: dict[str, Tensor],
    sc:             FlowNondimScales,
    *,
    C_hsu:  float = 0.5,
    margin: float = 0.0,
    eps:    float = 1e-10,
) -> Tensor:
    """
    Soft Hsu constraint on collocation points.

    Expects collocation_batch keys:
        x_star, surface_features, flow_numeric,
        Re, Pr, D_h_m                       ← flow scalars for Hsu
        dT_ref, q_ref                        ← nondim scales (same for all rows)
    """
    from model.flow_boiling_pinn import FlowBoilingOutputs

    device = next(model.parameters()).device

    x_star   = collocation_batch["x_star"].to(device)
    surf_num = collocation_batch["surface_features"]["numeric"].to(device)
    surf_cat = collocation_batch["surface_features"]["category_id"].to(device)
    flow_num = collocation_batch["flow_numeric"].to(device)
    Re       = collocation_batch["Re"].to(device)
    Pr       = collocation_batch["Pr"].to(device)
    D_h_m    = collocation_batch["D_h_m"].to(device)
    dT_ref   = float(collocation_batch.get("dT_ref", 1.0))
    q_ref    = float(collocation_batch.get("q_ref",  1.0))

    surface_features = {"numeric": surf_num, "category_id": surf_cat}
    out: FlowBoilingOutputs = model(x_star, surface_features, flow_num)

    # Redimensionalise predictions
    dT_onb_K  = out.delta_T_onb_star * dT_ref
    q_onb_Wm2 = out.q_onb_star * q_ref

    D = _hsu_discriminant_flow(
        dT_onb_K, q_onb_Wm2, Re, Pr, D_h_m, sc,
        C_hsu=C_hsu, eps=eps,
    )

    hinge = F.relu(margin - D)
    return (hinge ** 2).mean()


# ── Monotonicity constraints ──────────────────────────────────────────────────

def _monotone_sweep_loss(
    model:             "FlowBoilingPINN",
    base_surf_numeric: Tensor,    # (9,) — representative surface condition
    base_surf_cat:     Tensor,    # ()   — integer category
    base_flow_numeric: Tensor,    # (FLOW_NUMERIC_CHANNELS,) — base flow condition
    channel_idx:       int,       # which flow_numeric channel to sweep
    n_points:          int,
    sweep_range:       tuple[float, float],
    sign:              float,     # +1 → sweep↑ should cause pred↑; -1 → pred↓
    *,
    margin: float = 1e-3,
) -> Tensor:
    """
    Create a 1D sweep over flow_numeric[channel_idx] and penalise
    violations of the expected monotone direction.

    sign = +1  →  expect  dT_onb↑  as channel↑   (e.g. ΔT_sub↑)
    sign = -1  →  expect  dT_onb↓  as channel↑   (e.g. Re↑, G↑)
    """
    device = next(model.parameters()).device

    sweep_vals = torch.linspace(sweep_range[0], sweep_range[1],
                                n_points, device=device)

    # Build batch: replicate base condition, vary one channel
    flow_batch = base_flow_numeric.unsqueeze(0).expand(n_points, -1).clone()
    flow_batch[:, channel_idx] = sweep_vals

    surf_num = base_surf_numeric.unsqueeze(0).expand(n_points, -1).to(device)
    surf_cat = base_surf_cat.unsqueeze(0).expand(n_points).to(device)
    x_star   = torch.full((n_points, 1), 0.5, device=device)

    surface_features = {"numeric": surf_num, "category_id": surf_cat}
    out = model(x_star, surface_features, flow_batch)
    dT_pred = out.delta_T_onb_star  # (N,)

    # Penalise violations: consecutive differences should have same sign
    diff = dT_pred[1:] - dT_pred[:-1]  # (N-1,)

    if sign > 0:
        # Want dT↑ → penalise negative diffs
        violations = F.relu(margin - diff)
    else:
        # Want dT↓ → penalise positive diffs
        violations = F.relu(margin + diff)

    return (violations ** 2).mean()


def loss_monotonicity_flow(
    model:               "FlowBoilingPINN",
    base_surf_numeric:   Tensor,
    base_surf_cat:       Tensor,
    base_flow_numeric:   Tensor,
    *,
    n_points:            int   = 20,
    sweep_Re_range:      tuple[float, float] = (0.4, 1.0),    # log10(Re)/5 range
    sweep_G_range:       tuple[float, float] = (-0.5, 0.5),   # log10(G/G_ref) range
    sweep_sub_range:     tuple[float, float] = (0.0, 0.25),   # ΔT_sub_star range
    margin:              float = 1e-3,
) -> tuple[Tensor, Tensor, Tensor]:
    """Return (L_mono_Re, L_mono_G, L_mono_sub)."""

    # Flow encoder channel indices (from flow_encoder.py):
    #   0: log10(Re)/5, 1: log10(G/G_ref), 4: delta_T_sub_star

    L_Re = _monotone_sweep_loss(
        model, base_surf_numeric, base_surf_cat, base_flow_numeric,
        channel_idx=0,
        n_points=n_points,
        sweep_range=sweep_Re_range,
        sign=-1,       # Re↑ → dT_onb↓
        margin=margin,
    )
    L_G = _monotone_sweep_loss(
        model, base_surf_numeric, base_surf_cat, base_flow_numeric,
        channel_idx=1,
        n_points=n_points,
        sweep_range=sweep_G_range,
        sign=-1,       # G↑ → dT_onb↓
        margin=margin,
    )
    L_sub = _monotone_sweep_loss(
        model, base_surf_numeric, base_surf_cat, base_flow_numeric,
        channel_idx=4,
        n_points=n_points,
        sweep_range=sweep_sub_range,
        sign=+1,       # ΔT_sub↑ → dT_onb↑
        margin=margin,
    )
    return L_Re, L_G, L_sub


# ── PDE stubs (M7-M9) ─────────────────────────────────────────────────────────

def loss_pde_stub(device: torch.device | str = "cpu") -> Tensor:
    """Placeholder PDE residual — returns 0.  Activated in M7-M9."""
    return torch.zeros(1, device=device)


# ── Total loss ────────────────────────────────────────────────────────────────

def total_loss(
    model:          "FlowBoilingPINN",
    batch:          dict[str, Tensor],
    weights:        LossWeights,
    sc:             FlowNondimScales,
    *,
    collocation_hsu:  dict[str, Tensor] | None = None,
    collocation_mono: dict[str, Tensor] | None = None,
    C_hsu:            float = 0.5,
    hsu_margin:       float = 0.0,
    mono_margin:      float = 1e-3,
    n_mono_points:    int   = 20,
    log_scale_q:      bool  = True,
) -> LossComponents:
    """
    Compute all loss terms and return a LossComponents bundle.

    Parameters
    ----------
    batch : collated DataLoader batch with keys:
        x_star, surface_features, flow_numeric,
        q_onb_star, delta_T_onb_star, has_q, has_dT
    collocation_hsu : extra batch for Hsu collocation points (optional;
        if None, Hsu loss is skipped)
    collocation_mono : dict with keys 'surf_numeric', 'surf_cat_id',
        'flow_numeric' for one representative point used as mono base
        (if None, mono sweeps use mean of batch)
    """
    device = next(model.parameters()).device
    zero   = torch.zeros(1, device=device)

    # ── Forward pass on data batch ───────────────────────────────────────────
    x_star   = batch["x_star"].to(device)
    surf_num = batch["surface_features"]["numeric"].to(device)
    surf_cat = batch["surface_features"]["category_id"].to(device)
    flow_num = batch["flow_numeric"].to(device)
    has_q    = batch["has_q"].to(device)
    has_dT   = batch["has_dT"].to(device)
    true_q   = batch["q_onb_star"].to(device)
    true_dT  = batch["delta_T_onb_star"].to(device)

    surface_features = {"numeric": surf_num, "category_id": surf_cat}
    out = model(x_star, surface_features, flow_num)

    # ── Data losses ──────────────────────────────────────────────────────────
    L_q, L_dT = loss_data(
        out.q_onb_star, out.delta_T_onb_star,
        true_q, true_dT,
        has_q, has_dT,
        log_scale_q=log_scale_q,
    )

    # ── Hsu flow constraint ──────────────────────────────────────────────────
    if weights.w_hsu > 0 and collocation_hsu is not None:
        L_hsu = loss_hsu_flow(
            model, collocation_hsu, sc,
            C_hsu=C_hsu, margin=hsu_margin,
        )
    else:
        L_hsu = zero

    # ── Hsu self-consistency coupling: ΔT_pred = Hsu(q_pred) ────────────────
    if weights.w_hsu_coupling > 0 and "C_hsu_nd" in batch:
        C_hsu_nd = batch["C_hsu_nd"].to(device)
        L_hsu_cp = loss_hsu_coupling(out.q_onb_star, out.delta_T_onb_star, C_hsu_nd)
    else:
        L_hsu_cp = zero

    # ── Monotonicity constraints ─────────────────────────────────────────────
    if (weights.w_mono_Re > 0 or weights.w_mono_G > 0 or weights.w_mono_sub > 0):
        if collocation_mono is not None:
            base_sn  = collocation_mono["surf_numeric"].to(device)
            base_sc_ = collocation_mono["surf_cat_id"].to(device)
            base_fn  = collocation_mono["flow_numeric"].to(device)
        else:
            # Use first element of the batch as representative base
            base_sn  = surf_num[0].detach()
            base_sc_ = surf_cat[0].detach()
            base_fn  = flow_num[0].detach()

        L_Re, L_G, L_sub = loss_monotonicity_flow(
            model, base_sn, base_sc_, base_fn,
            n_points=n_mono_points, margin=mono_margin,
        )
    else:
        L_Re = L_G = L_sub = zero

    # ── PDE stubs (M7-M9) ────────────────────────────────────────────────────
    L_cont = loss_pde_stub(device) if weights.w_continuity > 0 else zero
    L_mom  = loss_pde_stub(device) if weights.w_momentum   > 0 else zero
    L_ene  = loss_pde_stub(device) if weights.w_energy     > 0 else zero

    # ── Weighted sum ─────────────────────────────────────────────────────────
    total = (
        weights.w_data_q       * L_q
      + weights.w_data_dT      * L_dT
      + weights.w_hsu          * L_hsu
      + weights.w_hsu_coupling * L_hsu_cp
      + weights.w_mono_Re      * L_Re
      + weights.w_mono_G       * L_G
      + weights.w_mono_sub     * L_sub
      + weights.w_continuity   * L_cont
      + weights.w_momentum     * L_mom
      + weights.w_energy       * L_ene
    )

    # Note: caller (run_adam_stage) checks torch.isfinite(lc.total) and skips
    # the backward pass if NaN — do NOT zero-out here as that corrupts grads.
    # _check_finite kept for debugging; disable by commenting if needed.
    # _check_finite(total, "total_loss")

    return LossComponents(
        L_data_q     = L_q,
        L_data_dT     = L_dT,
        L_hsu_flow    = L_hsu,
        L_hsu_coupling = L_hsu_cp,
        L_mono_Re     = L_Re,
        L_mono_G     = L_G,
        L_mono_sub   = L_sub,
        L_continuity = L_cont,
        L_momentum   = L_mom,
        L_energy     = L_ene,
        total        = total,
    )


# ── Smoke test ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    from pathlib import Path

    _MODEL_DIR = Path(__file__).resolve().parents[1]
    if str(_MODEL_DIR) not in sys.path:
        sys.path.insert(0, str(_MODEL_DIR))

    from model.flow_boiling_pinn import FlowBoilingPINN

    torch.manual_seed(0)
    device = torch.device("cpu")

    model = FlowBoilingPINN(
        surface_latent_dim=16, flow_latent_dim=8,
        hidden_dim=64, n_layers=4, head_hidden=32,
    ).to(device)
    model.eval()

    B = 16
    sc = compute_flow_nondim("water", 101.325)

    # ── Mock batch ────────────────────────────────────────────────────────────
    batch = {
        "x_star":           torch.rand(B, 1),
        "surface_features": {
            "numeric":      torch.randn(B, 9),
            "category_id":  torch.zeros(B, dtype=torch.long),
        },
        "flow_numeric":     torch.randn(B, 11) * 0.3,
        "q_onb_star":       torch.rand(B) * 2.0 + 0.1,
        "delta_T_onb_star": torch.rand(B) * 5.0 + 0.5,
        "has_q":            torch.ones(B, dtype=torch.bool),
        "has_dT":           torch.ones(B, dtype=torch.bool),
    }

    # ── Mock Hsu collocation batch ────────────────────────────────────────────
    N_hsu = 32
    coll_hsu = {
        "x_star":           torch.rand(N_hsu, 1),
        "surface_features": {
            "numeric":      torch.randn(N_hsu, 9),
            "category_id":  torch.zeros(N_hsu, dtype=torch.long),
        },
        "flow_numeric":     torch.randn(N_hsu, 11) * 0.3,
        "Re":               torch.rand(N_hsu) * 49600 + 400,     # 400-50k
        "Pr":               torch.full((N_hsu,), 1.76),           # water ~100°C
        "D_h_m":            torch.rand(N_hsu) * 0.009 + 0.001,   # 1-10 mm
        "dT_ref":           torch.tensor(50.0),
        "q_ref":            torch.tensor(1e6),
    }

    weights = LossWeights(
        w_data_q=1.0, w_data_dT=1.0, w_hsu=0.5,
        w_mono_Re=0.1, w_mono_G=0.1, w_mono_sub=0.1,
    )

    lc = total_loss(
        model, batch, weights, sc,
        collocation_hsu=coll_hsu,
        n_mono_points=10,
    )

    print("=== Phase 2 Loss Smoke Test ===")
    for k, v in lc.as_dict().items():
        print(f"  {k:<20s}: {v:.6f}")
    print(f"\n  Total (weighted): {lc.total.item():.6f}")
    print("\n[OK] loss_functions.py smoke test passed.")
