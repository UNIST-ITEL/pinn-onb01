"""
flow_boiling_pinn.py — Phase 2 Flow Boiling ONB PINN.

Architecture (plan.md § 4.2, M4 scope):
    ┌─────────────────┐    ┌──────────────────┐
    │ Surface Encoder │    │  Flow Encoder    │
    │ (Phase 1 xfer)  │    │  (Phase 2 new)   │
    │ → z_s ∈ ℝ^16   │    │  → z_f ∈ ℝ^8    │
    └────────┬────────┘    └───────┬──────────┘
             │                    │
             ▼                    ▼
        ┌───────────────────────────────┐
        │  Dual-FiLM Backbone           │
        │  per-layer:                   │
        │   h ← FiLM_s(h, z_s)         │
        │   h ← FiLM_f(h, z_f)         │
        │  6 hidden layers, width 96    │
        │  tanh activation              │
        └──────┬──────────────┬─────────┘
               │              │
        ┌──────▼──────┐ ┌─────▼──────┐
        │  T_star     │ │ ONB heads  │
        │  (autograd) │ │ ΔT + q''   │
        └─────────────┘ └────────────┘

M4 scope: data loss + Hsu soft constraint + monotonicity.
M7-M9 will add NS/energy PDE residuals (continuity + momentum + energy).

Spatial coordinate: x_star = x/L_channel ∈ [0, 1] (1D axial).
    For data points without known ONB location, default x_star = 0.5.
"""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import torch
from torch import nn

# ── Phase 1 imports (read-only) ───────────────────────────────────────────────
# Add phase1/03_model (parent of src/) so that relative imports inside src work:
#   src.model.surface_encoder does: from ..utils.nondim import ...
_P1_MODEL_ROOT = (
    Path(__file__).resolve().parents[4]   # PINN-ONB01/
    / "phase1_pool_boiling" / "03_model"  # .../03_model/  (parent of src/)
)


def _import_phase1():
    """Lazily add Phase 1 03_model root to sys.path and import SurfaceEncoder."""
    p1 = str(_P1_MODEL_ROOT)
    if p1 not in sys.path:
        sys.path.insert(0, p1)
    from src.model.surface_encoder import SurfaceEncoder, NUMERIC_CHANNELS
    return SurfaceEncoder, NUMERIC_CHANNELS


from model.flow_encoder import FlowEncoder, FLOW_NUMERIC_CHANNELS


# ── FiLM layer (same design as Phase 1) ──────────────────────────────────────
class FiLMLayer(nn.Module):
    """h ← (1 + γ(z)) · h + β(z)  initialised near-identity."""

    def __init__(self, cond_dim: int, hidden_dim: int) -> None:
        super().__init__()
        self.proj = nn.Linear(cond_dim, 2 * hidden_dim)
        nn.init.zeros_(self.proj.weight)
        nn.init.zeros_(self.proj.bias)

    def forward(self, h: torch.Tensor, z: torch.Tensor) -> torch.Tensor:
        gb = self.proj(z)
        gamma, beta = gb.chunk(2, dim=-1)
        return (1.0 + gamma) * h + beta


# ── Output head (identical to Phase 1 _OutputHead) ───────────────────────────
class _OutputHead(nn.Module):
    def __init__(
        self,
        in_dim: int,
        hidden_dim: int,
        positive: bool = False,
        small_init: float = 0.01,
    ) -> None:
        super().__init__()
        self.fc1 = nn.Linear(in_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, 1)
        self.positive = positive
        nn.init.xavier_normal_(self.fc1.weight, gain=nn.init.calculate_gain("tanh"))
        nn.init.zeros_(self.fc1.bias)
        nn.init.xavier_normal_(self.fc2.weight, gain=small_init)
        nn.init.zeros_(self.fc2.bias)

    def forward(self, h: torch.Tensor) -> torch.Tensor:
        y = self.fc2(torch.tanh(self.fc1(h)))
        return torch.nn.functional.softplus(y) if self.positive else y


# ── Outputs dataclass ─────────────────────────────────────────────────────────
@dataclass
class FlowBoilingOutputs:
    """All network outputs (nondimensional).

    T_star          : (B, 1) — temperature field (autograd-ready)
    delta_T_onb_star: (B, 1) — wall superheat at ONB (> 0 by softplus)
    q_onb_star      : (B, 1) — heat flux at ONB (> 0 by softplus)
    z_surface       : (B, latent_s) — surface latent
    z_flow          : (B, latent_f) — flow latent
    """
    T_star: torch.Tensor
    delta_T_onb_star: torch.Tensor
    q_onb_star: torch.Tensor
    z_surface: torch.Tensor
    z_flow: torch.Tensor

    def as_dict(self) -> dict[str, torch.Tensor]:
        return {k: getattr(self, k) for k in self.__dataclass_fields__}


# ── Main model ────────────────────────────────────────────────────────────────
class FlowBoilingPINN(nn.Module):
    """Phase 2 Flow Boiling ONB PINN with Dual-FiLM conditioning.

    Parameters
    ----------
    surface_latent_dim : int
        Must match the Phase 1 SurfaceEncoder latent dim (default 16).
    flow_latent_dim : int
        FlowEncoder output dim (default 8).
    hidden_dim : int
        Backbone hidden width (default 96; Phase 1 used 64).
    n_layers : int
        Number of backbone tanh layers (default 6).
    head_hidden : int
        Output head hidden width (default 48).
    freeze_surface_encoder : bool
        If True, surface encoder weights are frozen (Stage 1 of transfer).
    """

    def __init__(
        self,
        *,
        surface_latent_dim: int = 16,
        flow_latent_dim: int = 8,
        hidden_dim: int = 96,
        n_layers: int = 6,
        head_hidden: int = 48,
        flow_encoder_hidden: int = 32,
        flow_encoder_dropout: float = 0.1,
        freeze_surface_encoder: bool = False,
        seed: int | None = None,
    ) -> None:
        super().__init__()

        if seed is not None:
            torch.manual_seed(seed)

        # ── Sub-modules ───────────────────────────────────────────────────
        SurfaceEncoder, _ = _import_phase1()
        self.surface_encoder = SurfaceEncoder(latent_dim=surface_latent_dim)
        self.flow_encoder = FlowEncoder(
            latent_dim=flow_latent_dim,
            hidden_dim=flow_encoder_hidden,
            dropout=flow_encoder_dropout,
        )

        if freeze_surface_encoder:
            for p in self.surface_encoder.parameters():
                p.requires_grad_(False)

        self.surface_latent_dim = surface_latent_dim
        self.flow_latent_dim = flow_latent_dim
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers

        # ── Backbone (spatial_dim=1 → x/L) ────────────────────────────────
        # Input: x_star (B,1)
        backbone_linears: list[nn.Module] = []
        surface_films: list[nn.Module] = []
        flow_films: list[nn.Module] = []

        prev = 1  # spatial_dim
        for _ in range(n_layers):
            lin = nn.Linear(prev, hidden_dim)
            nn.init.xavier_normal_(lin.weight, gain=nn.init.calculate_gain("tanh"))
            nn.init.zeros_(lin.bias)
            backbone_linears.append(lin)
            surface_films.append(FiLMLayer(surface_latent_dim, hidden_dim))
            flow_films.append(FiLMLayer(flow_latent_dim, hidden_dim))
            prev = hidden_dim

        self.backbone_linear = nn.ModuleList(backbone_linears)
        self.surface_film = nn.ModuleList(surface_films)
        self.flow_film = nn.ModuleList(flow_films)

        # ── Output heads ──────────────────────────────────────────────────
        self.head_T      = _OutputHead(hidden_dim, head_hidden, positive=False)
        self.head_dT_onb = _OutputHead(hidden_dim, head_hidden, positive=True)
        self.head_q_onb  = _OutputHead(hidden_dim, head_hidden, positive=True)

    # ── Parameter counts ──────────────────────────────────────────────────────
    @property
    def n_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters())

    @property
    def n_trainable(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def parameter_summary(self) -> dict[str, int]:
        return {
            "surface_encoder": sum(p.numel() for p in self.surface_encoder.parameters()),
            "flow_encoder":    sum(p.numel() for p in self.flow_encoder.parameters()),
            "backbone":        sum(p.numel() for p in self.backbone_linear.parameters()),
            "surface_film":    sum(p.numel() for p in self.surface_film.parameters()),
            "flow_film":       sum(p.numel() for p in self.flow_film.parameters()),
            "heads":           (sum(p.numel() for p in self.head_T.parameters())
                                + sum(p.numel() for p in self.head_dT_onb.parameters())
                                + sum(p.numel() for p in self.head_q_onb.parameters())),
        }

    # ── Backbone (shared forward) ─────────────────────────────────────────────
    def _backbone(
        self,
        x_star: torch.Tensor,
        z_surface: torch.Tensor,
        z_flow: torch.Tensor,
    ) -> torch.Tensor:
        h = x_star
        for i, lin in enumerate(self.backbone_linear):
            h = lin(h)
            h = self.surface_film[i](h, z_surface)   # surface conditioning
            h = self.flow_film[i](h, z_flow)          # flow conditioning
            h = torch.tanh(h)
        return h

    # ── Full forward ─────────────────────────────────────────────────────────
    def forward(
        self,
        x_star: torch.Tensor,
        surface_features: dict[str, torch.Tensor],
        flow_numeric: torch.Tensor,
    ) -> FlowBoilingOutputs:
        """
        Parameters
        ----------
        x_star : (B, 1) — normalised axial location x/L ∈ [0, 1]
        surface_features : dict from encode_batch_to_tensors (Phase 1 format)
        flow_numeric : (B, FLOW_NUMERIC_CHANNELS) — from encode_flow_batch

        Returns
        -------
        FlowBoilingOutputs
        """
        z_s = self.surface_encoder(surface_features)  # (B, latent_s)
        z_f = self.flow_encoder(flow_numeric)          # (B, latent_f)
        h   = self._backbone(x_star, z_s, z_f)

        return FlowBoilingOutputs(
            T_star=self.head_T(h),
            delta_T_onb_star=self.head_dT_onb(h),
            q_onb_star=self.head_q_onb(h),
            z_surface=z_s,
            z_flow=z_f,
        )

    # ── PDE-only forward (M7-M9: NS + energy residuals) ──────────────────────
    def forward_for_pde(
        self,
        x_star: torch.Tensor,
        z_surface: torch.Tensor,
        z_flow: torch.Tensor,
    ) -> torch.Tensor:
        """Return T_star given pre-encoded latents (autograd-ready).

        z_surface and z_flow are cached outside the PDE residual loop to avoid
        re-running the encoders for every collocation batch.
        """
        h = self._backbone(x_star, z_surface, z_flow)
        return self.head_T(h)

    # ── Transfer learning helpers ─────────────────────────────────────────────
    def load_phase1_weights(self, checkpoint_path: str | Path) -> None:
        """Load Phase 1 pool-boiling PINN checkpoint into surface encoder + backbone.

        Phase 1 key prefix: 'encoder.*' → surface_encoder.*
                            'backbone_linear.*' → backbone_linear.*
                            'backbone_film.*' → surface_film.*  (first n_layers)
                            'head_*' → ignored (head shapes differ)
        """
        ckpt = torch.load(checkpoint_path, map_location="cpu", weights_only=True)
        state = ckpt.get("model_state_dict", ckpt)

        mapping = {}
        for k, v in state.items():
            if k.startswith("encoder."):
                mapping["surface_encoder." + k[len("encoder."):]] = v
            elif k.startswith("backbone_linear."):
                mapping[k] = v
            elif k.startswith("backbone_film."):
                # Phase 1 has single FiLM; map to surface_film in Phase 2
                mapping["surface_" + k] = v

        missing, unexpected = self.load_state_dict(mapping, strict=False)
        n_loaded = len(mapping) - len(missing)
        print(
            f"[transfer] loaded {n_loaded}/{len(mapping)} keys from Phase 1 checkpoint\n"
            f"  missing   : {len(missing)}\n"
            f"  unexpected: {len(unexpected)}"
        )

    def freeze_surface_encoder(self) -> None:
        for p in self.surface_encoder.parameters():
            p.requires_grad_(False)

    def unfreeze_surface_encoder(self) -> None:
        for p in self.surface_encoder.parameters():
            p.requires_grad_(True)

    def mlflow_log_architecture(self) -> dict[str, int | str | float]:
        ps = self.parameter_summary()
        return {
            "arch.surface_latent_dim": self.surface_latent_dim,
            "arch.flow_latent_dim":    self.flow_latent_dim,
            "arch.hidden_dim":         self.hidden_dim,
            "arch.n_layers":           self.n_layers,
            "arch.n_parameters_total": self.n_parameters,
            "arch.n_trainable":        self.n_trainable,
            **{f"arch.n_params_{k}": v for k, v in ps.items()},
        }


# ── Smoke test ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    _SRC = Path(__file__).resolve().parents[1]
    if str(_SRC) not in sys.path:
        sys.path.insert(0, str(_SRC))
    from model.flow_encoder import FlowFeatures, encode_flow_batch

    torch.manual_seed(0)

    model = FlowBoilingPINN(seed=0)
    model.eval()

    ps = model.parameter_summary()
    print("[arch] FlowBoilingPINN parameter summary:")
    for k, v in ps.items():
        print(f"  {k:20s}: {v:7,d}")
    print(f"  {'TOTAL':20s}: {model.n_parameters:7,d}")
    print(f"  {'TRAINABLE':20s}: {model.n_trainable:7,d}")

    # Dummy surface features (Phase 1 format)
    try:
        SurfaceEncoder, NUMERIC_CHANNELS = _import_phase1()
        from src.model.surface_encoder import encode_batch_to_tensors, SurfaceFeatures
        sf = SurfaceFeatures(Ra_m=1e-6, theta_rad=math.radians(30), category_id=1,
                             surface_id="TEST", fluid="water")
        surf_batch = encode_batch_to_tensors([sf, sf])
    except Exception as e:
        print(f"[warn] surface encode failed ({e}); using zeros")
        surf_batch = {
            "numeric":     torch.zeros(2, 9),
            "category_id": torch.zeros(2, dtype=torch.long),
        }

    # Flow features
    ff = FlowFeatures.from_dataset_row(
        G_kg_m2s=500, D_h_mm=12.1, channel_type="tube_circular",
        delta_T_sub_K=30.0, fluid="water", P_kPa=101.325, q_onb_W_m2=5e5,
    )
    flow_num = encode_flow_batch([ff, ff])  # (2, 9)

    x_star = torch.tensor([[0.3], [0.7]])
    out = model(x_star, surf_batch, flow_num)

    print("\n[test] forward pass:")
    print(f"  x_star              : {x_star.flatten().tolist()}")
    print(f"  T_star              : {out.T_star.flatten().tolist()}")
    print(f"  delta_T_onb_star    : {out.delta_T_onb_star.flatten().tolist()}")
    print(f"  q_onb_star          : {out.q_onb_star.flatten().tolist()}")
    print(f"  z_surface shape     : {tuple(out.z_surface.shape)}")
    print(f"  z_flow    shape     : {tuple(out.z_flow.shape)}")

    assert out.delta_T_onb_star.min().item() > 0, "ΔT_onb must be positive"
    assert out.q_onb_star.min().item() > 0, "q_onb must be positive"

    # PDE autograd
    x_pde = torch.tensor([[0.5], [0.5]], requires_grad=True)
    with torch.no_grad():
        z_s = model.surface_encoder(surf_batch)
        z_f = model.flow_encoder(flow_num)
    T = model.forward_for_pde(x_pde, z_s, z_f)
    dT_dx = torch.autograd.grad(T.sum(), x_pde, create_graph=True)[0]
    print(f"\n[test] PDE autograd dT*/dx* : {dT_dx.flatten().tolist()}")
    assert torch.isfinite(dT_dx).all(), "grad must be finite"

    print("\n[ok] all smoke tests passed.")
