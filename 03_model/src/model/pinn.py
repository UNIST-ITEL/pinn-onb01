"""
pinn.py — Main Physics-Informed Neural Network for pool boiling ONB prediction.

Section 4.3 (Phase A): 1D steady heat conduction along the heater thickness
direction, conditioned on a surface descriptor latent vector. The architecture
is intentionally modular so we can extend to 2D (Phase B) and time-dependent
bubble cycles (Phase C) without rewriting the core MLP.

Pipeline
--------
              surface_features (dict)
                       │
                       ▼
              SurfaceEncoder ──► z_surface  ∈ R^{B x latent_dim}
                                     │
   spatial_z (B,1) ──┐                │       (optional) operating (B,2)
                     ▼                ▼            │
            ─────────────────  conditioning  ──────┘
              ("concat"  → torch.cat)
              ("film"    → per-layer (gamma, beta) modulation)
                                     │
                                     ▼
                       Main MLP (5 hidden, tanh, 64)
                                     │
            ┌────────────────────────┼──────────────────────────┐
            ▼                        ▼                          ▼
        T_star head             ΔT_ONB_star head            q_ONB_star head
        (linear, 1)             (linear → softplus)         (linear → softplus)

Naming follows CLAUDE.md (variables suffixed `_star` are nondimensional).

Authors: PINN-ONB01 project (pinn-architecture-designer agent)
Date   : 2026-05-10
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import torch
from torch import nn

from ..utils.nondim import NondimScales, scales_for
from .surface_encoder import (
    NUMERIC_CHANNELS,
    SurfaceEncoder,
    SurfaceFeatures,
    encode_batch_to_tensors,
)

# ---------------------------------------------------------------------------
# Reproducibility helper
# ---------------------------------------------------------------------------
def set_seed(seed: int = 0) -> None:
    """Fix seeds for ``torch`` (CPU/CUDA) and ``numpy``-like determinism."""
    import random

    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


# ---------------------------------------------------------------------------
# Output dataclass
# ---------------------------------------------------------------------------
@dataclass
class PINNOutputs:
    """Bundle of network outputs (all nondimensional).

    Attributes
    ----------
    T_star : (B, 1)
        Nondimensional temperature field at the queried spatial coordinate.
        Required for autograd-based PDE residual evaluation.
    delta_T_onb_star : (B, 1)
        ONB superheat prediction (positive by construction via softplus).
    q_onb_star : (B, 1)
        ONB heat flux prediction (positive by construction via softplus).
    z_surface : (B, latent_dim)
        Surface latent vector — exposed for diagnostic / regularisation use.
    """

    T_star: torch.Tensor
    delta_T_onb_star: torch.Tensor
    q_onb_star: torch.Tensor
    z_surface: torch.Tensor

    # ---- convenience ------------------------------------------------------
    def as_dict(self) -> dict[str, torch.Tensor]:
        return {
            "T_star": self.T_star,
            "delta_T_onb_star": self.delta_T_onb_star,
            "q_onb_star": self.q_onb_star,
            "z_surface": self.z_surface,
        }


# ---------------------------------------------------------------------------
# Activation factory
# ---------------------------------------------------------------------------
_ACTIVATIONS: dict[str, type[nn.Module]] = {
    "tanh": nn.Tanh,
    "gelu": nn.GELU,
    "silu": nn.SiLU,
    "relu": nn.ReLU,
}


def _make_activation(name: str) -> nn.Module:
    name = name.lower().strip()
    if name not in _ACTIVATIONS:
        raise ValueError(
            f"Unknown activation '{name}'. Choose from {list(_ACTIVATIONS)}"
        )
    return _ACTIVATIONS[name]()


def _xavier_init(layer: nn.Linear, gain: float = 1.0) -> None:
    nn.init.xavier_normal_(layer.weight, gain=gain)
    if layer.bias is not None:
        nn.init.zeros_(layer.bias)


def _kaiming_init(layer: nn.Linear) -> None:
    nn.init.kaiming_normal_(layer.weight, nonlinearity="relu")
    if layer.bias is not None:
        nn.init.zeros_(layer.bias)


# ---------------------------------------------------------------------------
# FiLM conditioning module
# ---------------------------------------------------------------------------
class FiLMLayer(nn.Module):
    """Feature-wise Linear Modulation: h <- gamma(z) * h + beta(z).

    A small linear maps ``z_cond`` -> (gamma, beta), both of shape
    ``(B, hidden_dim)``. ``gamma`` is shifted by 1 so the layer initialises
    near-identity (helpful when the encoder is still untrained).
    """

    def __init__(self, cond_dim: int, hidden_dim: int) -> None:
        super().__init__()
        self.proj = nn.Linear(cond_dim, 2 * hidden_dim)
        # Initialise near-identity: gamma~1, beta~0
        nn.init.zeros_(self.proj.weight)
        nn.init.zeros_(self.proj.bias)

    def forward(self, h: torch.Tensor, z_cond: torch.Tensor) -> torch.Tensor:
        gamma_beta = self.proj(z_cond)
        gamma, beta = gamma_beta.chunk(2, dim=-1)
        return (1.0 + gamma) * h + beta


# ---------------------------------------------------------------------------
# Output head
# ---------------------------------------------------------------------------
class _OutputHead(nn.Module):
    """Two-layer head with optional positive activation.

    The final linear initialises with very small gain to avoid exploding
    extrapolations early in training.
    """

    def __init__(
        self,
        in_dim: int,
        hidden_dim: int,
        out_dim: int = 1,
        activation: str = "tanh",
        positive: bool = False,
        small_init: float = 0.01,
    ) -> None:
        super().__init__()
        self.fc1 = nn.Linear(in_dim, hidden_dim)
        self.act = _make_activation(activation)
        self.fc2 = nn.Linear(hidden_dim, out_dim)
        self.positive = positive

        # Tanh-friendly init for the first projection,
        # very small init for the output to keep predictions tame.
        _xavier_init(self.fc1, gain=nn.init.calculate_gain(activation if activation in ("tanh", "relu") else "tanh"))
        _xavier_init(self.fc2, gain=small_init)

    def forward(self, h: torch.Tensor) -> torch.Tensor:
        y = self.fc2(self.act(self.fc1(h)))
        if self.positive:
            # softplus keeps outputs strictly positive — physically required
            # for delta_T_onb_star and q_onb_star.
            y = torch.nn.functional.softplus(y)
        return y


# ---------------------------------------------------------------------------
# Main PINN module
# ---------------------------------------------------------------------------
class PoolBoilingPINN(nn.Module):
    """Pool boiling ONB PINN — Phase A architecture.

    Inputs (forward signature)
    --------------------------
    surface_z : (B, 1) float tensor
        Spatial coordinate along the heater (already nondimensional in Phase A:
        ``z / L_heater`` typically in [0, 1]).
    surface_features : dict[str, Tensor]
        Output of :func:`encode_batch_to_tensors` — keys ``numeric``
        ``(B, NUMERIC_CHANNELS)`` and ``category_id`` ``(B,) int64``.
        Passed straight to ``SurfaceEncoder``.
    operating : (B, 2) float tensor or None
        Optional operating-condition vector. Currently expected to carry
        ``(P_star, delta_T_sub_star)`` — both nondimensional. Provide ``None``
        to disable.

    Outputs
    -------
    PINNOutputs dataclass holding T_star, delta_T_onb_star, q_onb_star, z_surface.

    Notes
    -----
    * All hidden layers are pre-LayerNorm-free (PINN tradition); FiLM provides
      the conditioning channel when ``conditioning='film'``.
    * Output heads are independent — ``T_star`` is differentiable wrt.
      ``surface_z`` (autograd-ready for PDE residuals).
    """

    SUPPORTED_CONDITIONING: tuple[str, ...] = ("concat", "film")

    def __init__(
        self,
        encoder: SurfaceEncoder | None = None,
        *,
        spatial_dim: int = 1,
        operating_dim: int = 2,
        latent_dim: int = 16,
        hidden_dim: int = 64,
        n_layers: int = 5,
        activation: str = "tanh",
        conditioning: Literal["concat", "film"] = "concat",
        head_hidden: int = 32,
        seed: int | None = None,
    ) -> None:
        super().__init__()

        if seed is not None:
            set_seed(int(seed))

        if conditioning not in self.SUPPORTED_CONDITIONING:
            raise ValueError(
                f"conditioning must be one of {self.SUPPORTED_CONDITIONING}, "
                f"got '{conditioning}'"
            )
        if n_layers < 2:
            raise ValueError("n_layers must be >= 2")

        # --- Sub-modules -------------------------------------------------
        self.encoder = encoder if encoder is not None else SurfaceEncoder(latent_dim=latent_dim)
        # Sanity: encoder latent must match expected latent_dim
        if self.encoder.output_dim != latent_dim:
            raise ValueError(
                f"latent_dim mismatch: encoder.output_dim={self.encoder.output_dim} "
                f"but PINN latent_dim={latent_dim}"
            )

        self.spatial_dim = int(spatial_dim)
        self.operating_dim = int(operating_dim)
        self.latent_dim = int(latent_dim)
        self.hidden_dim = int(hidden_dim)
        self.n_layers = int(n_layers)
        self.activation_name = activation
        self.conditioning = conditioning
        self.head_hidden = int(head_hidden)

        # --- Backbone construction --------------------------------------
        # Concat: spatial + operating + latent are all stacked into the
        # first linear input. FiLM: only spatial + operating go in; latent
        # modulates each hidden layer separately.
        if conditioning == "concat":
            in_dim = spatial_dim + operating_dim + latent_dim
        else:  # film
            in_dim = spatial_dim + operating_dim

        layers: list[nn.Module] = []
        film_layers: list[FiLMLayer] = []
        prev = in_dim
        for _ in range(n_layers):
            lin = nn.Linear(prev, hidden_dim)
            _xavier_init(lin, gain=nn.init.calculate_gain(activation if activation in ("tanh", "relu") else "tanh"))
            layers.append(lin)
            if conditioning == "film":
                film_layers.append(FiLMLayer(latent_dim, hidden_dim))
            prev = hidden_dim
        self.backbone_linear = nn.ModuleList(layers)
        self.backbone_film = nn.ModuleList(film_layers) if conditioning == "film" else None
        # One activation instance is fine — stateless modules.
        self.backbone_act = _make_activation(activation)

        # --- Output heads -----------------------------------------------
        # T_star : unconstrained sign (small final-layer init)
        # delta_T_onb_star, q_onb_star : strictly positive via softplus
        self.head_T = _OutputHead(
            in_dim=hidden_dim,
            hidden_dim=head_hidden,
            out_dim=1,
            activation=activation,
            positive=False,
        )
        self.head_dT_onb = _OutputHead(
            in_dim=hidden_dim,
            hidden_dim=head_hidden,
            out_dim=1,
            activation=activation,
            positive=True,
        )
        self.head_q_onb = _OutputHead(
            in_dim=hidden_dim,
            hidden_dim=head_hidden,
            out_dim=1,
            activation=activation,
            positive=True,
        )

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------
    @property
    def n_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters())

    @property
    def n_parameters_encoder(self) -> int:
        return sum(p.numel() for p in self.encoder.parameters())

    @property
    def n_parameters_backbone(self) -> int:
        n = sum(p.numel() for p in self.backbone_linear.parameters())
        if self.backbone_film is not None:
            n += sum(p.numel() for p in self.backbone_film.parameters())
        return n

    @property
    def n_parameters_heads(self) -> int:
        return (
            sum(p.numel() for p in self.head_T.parameters())
            + sum(p.numel() for p in self.head_dT_onb.parameters())
            + sum(p.numel() for p in self.head_q_onb.parameters())
        )

    # ------------------------------------------------------------------
    # Backbone forward (shared by full forward + PDE-only forward)
    # ------------------------------------------------------------------
    def _backbone(
        self,
        spatial_z: torch.Tensor,
        z_surface: torch.Tensor,
        operating: torch.Tensor | None,
    ) -> torch.Tensor:
        # Build first-layer input
        if operating is None:
            operating = torch.zeros(
                spatial_z.shape[0], self.operating_dim,
                dtype=spatial_z.dtype, device=spatial_z.device,
            )
        if operating.shape[-1] != self.operating_dim:
            raise ValueError(
                f"operating must have last-dim={self.operating_dim}, "
                f"got {operating.shape[-1]}"
            )

        if self.conditioning == "concat":
            x = torch.cat([spatial_z, operating, z_surface], dim=-1)
        else:  # film
            x = torch.cat([spatial_z, operating], dim=-1)

        h = x
        for i, lin in enumerate(self.backbone_linear):
            h = lin(h)
            if self.backbone_film is not None:
                h = self.backbone_film[i](h, z_surface)
            h = self.backbone_act(h)
        return h

    # ------------------------------------------------------------------
    # Forward (full)
    # ------------------------------------------------------------------
    def forward(
        self,
        surface_z: torch.Tensor,
        surface_features: dict[str, torch.Tensor],
        operating: torch.Tensor | None = None,
    ) -> PINNOutputs:
        if surface_z.dim() != 2 or surface_z.shape[-1] != self.spatial_dim:
            raise ValueError(
                f"surface_z must be (B, {self.spatial_dim}); got {tuple(surface_z.shape)}"
            )

        z_surface = self.encoder(surface_features)  # (B, latent_dim)

        if z_surface.shape[0] != surface_z.shape[0]:
            raise ValueError(
                f"Batch mismatch: surface_z has B={surface_z.shape[0]} "
                f"but encoded surface batch B={z_surface.shape[0]}"
            )

        h = self._backbone(surface_z, z_surface, operating)

        T_star = self.head_T(h)
        dT_onb = self.head_dT_onb(h)
        q_onb = self.head_q_onb(h)

        return PINNOutputs(
            T_star=T_star,
            delta_T_onb_star=dT_onb,
            q_onb_star=q_onb,
            z_surface=z_surface,
        )

    # ------------------------------------------------------------------
    # DeepXDE-friendly PDE forward
    # ------------------------------------------------------------------
    def forward_for_pde(
        self,
        spatial_z: torch.Tensor,
        z_surface: torch.Tensor,
        operating: torch.Tensor | None = None,
    ) -> torch.Tensor:
        """Return only ``T_star`` given a *pre-encoded* surface latent.

        DeepXDE's PDE solver typically requires a single-tensor output and a
        callable that maps a spatial query to that tensor. We assume the
        caller has cached ``z_surface`` at the start of training (it does not
        depend on ``spatial_z``) and passes it back here.

        Parameters
        ----------
        spatial_z : (B, spatial_dim) — usually requires_grad=True for autograd.
        z_surface : (B, latent_dim)  — output of ``self.encoder``.
        operating : (B, operating_dim) or None.

        Returns
        -------
        T_star : (B, 1)
        """
        if spatial_z.dim() != 2 or spatial_z.shape[-1] != self.spatial_dim:
            raise ValueError(
                f"spatial_z must be (B, {self.spatial_dim}); got {tuple(spatial_z.shape)}"
            )
        if z_surface.dim() != 2 or z_surface.shape[-1] != self.latent_dim:
            raise ValueError(
                f"z_surface must be (B, {self.latent_dim}); got {tuple(z_surface.shape)}"
            )
        h = self._backbone(spatial_z, z_surface, operating)
        return self.head_T(h)

    # ------------------------------------------------------------------
    # MLflow logging hook (placeholder — implemented by training-orchestrator)
    # ------------------------------------------------------------------
    def mlflow_log_architecture(self) -> dict[str, int | str]:
        """Return a small dict suitable for ``mlflow.log_params``."""
        return {
            "arch.spatial_dim": self.spatial_dim,
            "arch.operating_dim": self.operating_dim,
            "arch.latent_dim": self.latent_dim,
            "arch.hidden_dim": self.hidden_dim,
            "arch.n_layers": self.n_layers,
            "arch.activation": self.activation_name,
            "arch.conditioning": self.conditioning,
            "arch.head_hidden": self.head_hidden,
            "arch.n_parameters_total": self.n_parameters,
            "arch.n_parameters_encoder": self.n_parameters_encoder,
            "arch.n_parameters_backbone": self.n_parameters_backbone,
            "arch.n_parameters_heads": self.n_parameters_heads,
        }


# ---------------------------------------------------------------------------
# Self-test / smoke check
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PoolBoilingPINN smoke test")
    parser.add_argument(
        "--csv",
        type=str,
        default=str(
            Path(__file__).resolve().parents[3]
            / "02_data" / "processed" / "onb_dataset.csv"
        ),
        help="Path to onb_dataset.csv (for fetching SFC-001 features)",
    )
    parser.add_argument(
        "--conditioning",
        choices=PoolBoilingPINN.SUPPORTED_CONDITIONING,
        default="concat",
    )
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    set_seed(args.seed)

    print("=" * 72)
    print("PoolBoilingPINN smoke test")
    print("=" * 72)

    # ---- Build model -------------------------------------------------
    model = PoolBoilingPINN(
        latent_dim=16,
        hidden_dim=64,
        n_layers=5,
        activation="tanh",
        conditioning=args.conditioning,
        seed=args.seed,
    )
    model.eval()

    print(
        f"\n[arch] conditioning   : {model.conditioning}\n"
        f"[arch] params total   : {model.n_parameters:,}\n"
        f"[arch]   encoder      : {model.n_parameters_encoder:,}\n"
        f"[arch]   backbone     : {model.n_parameters_backbone:,}\n"
        f"[arch]   heads        : {model.n_parameters_heads:,}"
    )

    # ---- Construct a tiny surface batch from real CSV (or fallback) --
    csv_path = Path(args.csv)
    if csv_path.is_file():
        from .surface_encoder import load_features_from_dataset

        feats, sids = load_features_from_dataset(csv_path)
        by_id = {f.surface_id: f for f in feats}
        if "SFC-001" in by_id:
            base_feat = by_id["SFC-001"]
            print(f"\n[data] using SFC-001: Ra={base_feat.Ra_m*1e6:.4f} um, "
                  f"theta={(math.degrees(base_feat.theta_rad) if base_feat.theta_rad else None)} deg, "
                  f"fluid={base_feat.fluid}")
        else:
            base_feat = feats[0]
            print(f"\n[data] SFC-001 missing; using {base_feat.surface_id}")
    else:
        # Fallback synthetic surface
        base_feat = SurfaceFeatures(
            Ra_m=1e-6, theta_rad=math.radians(45.0),
            category_id=1, surface_id="SYN-001", fluid="water",
        )
        print(f"\n[data] CSV not found; using synthetic {base_feat.surface_id}")

    # ---- Test 1: 2 query points, batch dim = 2 -----------------------
    surface_features_b2 = encode_batch_to_tensors([base_feat, base_feat])
    surface_z_b2 = torch.tensor([[0.5], [1.0]], dtype=torch.float32, requires_grad=True)
    operating_b2 = torch.tensor(
        [[1.0, 0.05], [1.0, 0.05]], dtype=torch.float32
    )  # (P_star, delta_T_sub_star)
    out2 = model(surface_z_b2, surface_features_b2, operating_b2)
    print("\n[test-1] B=2 query")
    print(f"  T_star            shape={tuple(out2.T_star.shape)}      "
          f"values={out2.T_star.flatten().tolist()}")
    print(f"  delta_T_onb_star  shape={tuple(out2.delta_T_onb_star.shape)} "
          f"values={out2.delta_T_onb_star.flatten().tolist()}")
    print(f"  q_onb_star        shape={tuple(out2.q_onb_star.shape)}     "
          f"values={out2.q_onb_star.flatten().tolist()}")
    print(f"  z_surface         shape={tuple(out2.z_surface.shape)}")

    # Range sanity (tanh outputs imply T_star ~ O(0.01) early, dT/q > 0 by softplus)
    assert out2.delta_T_onb_star.min().item() > 0.0, "delta_T_onb_star must be positive"
    assert out2.q_onb_star.min().item() > 0.0, "q_onb_star must be positive"

    # ---- Test 2: batch B=8 inference --------------------------------
    feats_b8 = [base_feat] * 8
    surface_features_b8 = encode_batch_to_tensors(feats_b8)
    surface_z_b8 = torch.linspace(0.0, 1.0, steps=8).unsqueeze(-1)
    out8 = model(surface_z_b8, surface_features_b8)
    print("\n[test-2] B=8 batch inference (operating=None)")
    print(f"  T_star            shape={tuple(out8.T_star.shape)}")
    print(f"  T_star range      [{out8.T_star.min().item():+.4f}, {out8.T_star.max().item():+.4f}]")
    print(f"  delta_T_onb_star  range [{out8.delta_T_onb_star.min().item():.4e}, "
          f"{out8.delta_T_onb_star.max().item():.4e}]")
    print(f"  q_onb_star        range [{out8.q_onb_star.min().item():.4e}, "
          f"{out8.q_onb_star.max().item():.4e}]")
    assert out8.T_star.shape == (8, 1)
    assert out8.delta_T_onb_star.shape == (8, 1)
    assert out8.q_onb_star.shape == (8, 1)

    # ---- Test 3: PDE autograd compatibility -------------------------
    surface_z_b2.requires_grad_(True)
    out_pde = model(surface_z_b2, surface_features_b2, operating_b2)
    T = out_pde.T_star
    grad_T = torch.autograd.grad(
        outputs=T,
        inputs=surface_z_b2,
        grad_outputs=torch.ones_like(T),
        create_graph=True,
        retain_graph=True,
    )[0]
    grad2_T = torch.autograd.grad(
        outputs=grad_T,
        inputs=surface_z_b2,
        grad_outputs=torch.ones_like(grad_T),
        create_graph=True,
    )[0]
    print("\n[test-3] PDE autograd")
    print(f"  dT*/dz*           shape={tuple(grad_T.shape)}    values={grad_T.flatten().tolist()}")
    print(f"  d2T*/dz*2         shape={tuple(grad2_T.shape)}   values={grad2_T.flatten().tolist()}")
    assert grad_T.shape == surface_z_b2.shape
    assert grad2_T.shape == surface_z_b2.shape
    assert torch.isfinite(grad_T).all() and torch.isfinite(grad2_T).all()

    # ---- Test 4: forward_for_pde (cached encoder path) --------------
    with torch.no_grad():
        z_surf = model.encoder(surface_features_b2)
    spatial_z_pde = surface_z_b2.detach().clone().requires_grad_(True)
    T_only = model.forward_for_pde(spatial_z_pde, z_surf, operating_b2)
    grad_only = torch.autograd.grad(T_only.sum(), spatial_z_pde, create_graph=True)[0]
    print("\n[test-4] forward_for_pde (DeepXDE-style)")
    print(f"  T_star            shape={tuple(T_only.shape)}")
    print(f"  dT*/dz*           shape={tuple(grad_only.shape)}  finite="
          f"{bool(torch.isfinite(grad_only).all())}")

    # ---- Test 5: FiLM mode (separate run) ---------------------------
    print("\n[test-5] FiLM conditioning sanity")
    film_model = PoolBoilingPINN(
        latent_dim=16, hidden_dim=64, n_layers=5,
        activation="tanh", conditioning="film", seed=args.seed,
    )
    film_model.eval()
    film_out = film_model(surface_z_b2, surface_features_b2, operating_b2)
    print(f"  params total      : {film_model.n_parameters:,}")
    print(f"    backbone (incl. FiLM): {film_model.n_parameters_backbone:,}")
    print(f"  T_star            shape={tuple(film_out.T_star.shape)}")
    assert film_out.T_star.shape == (2, 1)

    # ---- MLflow architecture summary --------------------------------
    print("\n[mlflow] log_params payload:")
    for k, v in model.mlflow_log_architecture().items():
        print(f"  {k:38s} = {v}")

    print("\n[ok] all smoke tests passed.")
