"""
surface_encoder.py — Surface conditioning encoder for the ONB PINN.

Section 4.4 (Method B: Surface Embedding). Maps raw surface features
(roughness, contact angle, optional cavity geometry, paper category) to a
latent vector ``z`` consumed by the main PINN as a conditioning input.

Design principles
-----------------
1. Roughness ``Ra`` spans 4 orders of magnitude (0.43 nm -> 10.5 um in the
   current dataset). We always feed ``log10(Ra / 1um)`` and additionally the
   nondimensional ``log10(Ra / L_c)`` when capillary scales are available
   (recommended physical option).
2. Contact angle is mapped through ``cos(theta)`` — this is the variable that
   appears in Young's equation and Hsu's nucleation criterion. We additionally
   keep ``theta / pi`` for redundancy.
3. Missing values (theta unknown, r_c / N_s not yet inferred) are handled with
   explicit binary mask channels rather than imputed silently. The main PINN
   can therefore down-weight features that come from imputed defaults.
4. Paper category is embedded (small embedding table, default 4-d) — this lets
   the encoder absorb paper-specific systematic biases without binding to the
   fluid, which is handled separately by the main PINN through nondim scales.
5. Latent dimension defaults to 16. With only 48 ONB points we deliberately
   keep the encoder small (3-layer MLP, hidden 64, dropout 0.1) to avoid
   overfitting; the latent dim is configurable.

Variable naming follows CLAUDE.md:
    Ra_surface, theta_contact, r_c, N_s,
    nondim variables suffixed with `_star`.

Authors: PINN-ONB01 project (surface encoder agent)
Date   : 2026-05-10
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import torch
from torch import nn

from ..utils.nondim import NondimScales, scales_for

# ---------------------------------------------------------------------------
# Paper category vocabulary
# ---------------------------------------------------------------------------
# Order matters: the integer index is the embedding row.
# Derived from the unique 'category' field in 02_data/processed/onb_dataset.csv.
# 'unknown' is reserved as index 0 so that unseen categories fall back gracefully.
PAPER_CATEGORIES: tuple[str, ...] = (
    "unknown",
    "betz",
    "jo",
    "phan",
    "jones",
    "jones_w",
    "jones_F",
    "bourdon12",
    "bourdon15",
    "jabardo",
)

_CATEGORY_TO_ID: dict[str, int] = {name: i for i, name in enumerate(PAPER_CATEGORIES)}


def category_to_id(name: str | None) -> int:
    """Map a category string to its integer id (0 = unknown)."""
    if name is None:
        return 0
    key = name.strip().lower()
    return _CATEGORY_TO_ID.get(key, 0)


# Default fluid -> pressure map for nondimensionalisation (Phase 1 atmospheric).
DEFAULT_FLUID_PRESSURES: dict[str, float] = {
    "water": 101_325.0,
    "FC-72": 101_325.0,
    "FC-77": 101_325.0,
    "R-123": 101_325.0,
    "R-134a": 500_000.0,   # typical refrigeration test pressure
}


# ---------------------------------------------------------------------------
# Raw feature container
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class SurfaceFeatures:
    """Raw surface descriptor (SI units).

    All physical inputs are expressed in SI; non-numeric optional fields use
    ``None`` to signal missing data — this distinguishes "true zero" from
    "not measured".
    """
    Ra_m: float                      # arithmetic mean roughness [m]
    theta_rad: float | None = None   # static contact angle [rad]
    r_c_m: float | None = None       # active cavity radius [m] (Phase 4)
    N_s_per_m2: float | None = None  # cavity site density [1/m^2] (Phase 4)
    category_id: int = 0             # paper-group id (see PAPER_CATEGORIES)
    surface_id: str = ""             # human-readable id (e.g. "SFC-001")
    fluid: str = "water"             # fluid label, used to pick L_c
    notes: str = ""

    # ---- convenience constructors -----------------------------------------
    @classmethod
    def from_dataset_row(
        cls,
        Ra_um: float,
        theta_deg: float | None,
        category: str,
        surface_id: str = "",
        fluid: str = "water",
        notes: str = "",
        r_c_um: float | None = None,
        N_s_per_cm2: float | None = None,
    ) -> "SurfaceFeatures":
        """Build from typical CSV units (um, deg, sites/cm^2)."""
        Ra_m = float(Ra_um) * 1e-6
        theta_rad = math.radians(float(theta_deg)) if theta_deg is not None else None
        r_c_m = float(r_c_um) * 1e-6 if r_c_um is not None else None
        N_s_per_m2 = float(N_s_per_cm2) * 1e4 if N_s_per_cm2 is not None else None
        return cls(
            Ra_m=Ra_m,
            theta_rad=theta_rad,
            r_c_m=r_c_m,
            N_s_per_m2=N_s_per_m2,
            category_id=category_to_id(category),
            surface_id=surface_id,
            fluid=fluid,
            notes=notes,
        )


# ---------------------------------------------------------------------------
# Vectorisation: SurfaceFeatures -> normalised tensor
# ---------------------------------------------------------------------------
# Numeric channels (continuous):
#   0: log10(Ra_m / 1e-6)               -- 1um reference, paper-style
#   1: log10(max(Ra_m, 1e-12) / L_c)    -- capillary-length nondim
#   2: cos(theta)                        -- Young's equation kernel
#   3: theta / pi                        -- redundant orientation cue
#   4: theta_mask                        -- 1 if theta provided else 0
#   5: log10(max(r_c_m, 1e-12) / L_c)   -- 0 + mask=0 if missing
#   6: r_c_mask
#   7: log10(max(N_s_per_m2, 1.0)) / 6  -- log scale, ~0..1 for 1..1e6 /m^2
#   8: N_s_mask
NUMERIC_CHANNELS: int = 9


def _safe_log10(value: float, eps: float = 1e-30) -> float:
    return math.log10(max(value, eps))


def encode_features_to_tensor(
    features: SurfaceFeatures,
    scales: NondimScales,
    *,
    dtype: torch.dtype = torch.float32,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Vectorise a single :class:`SurfaceFeatures` into (numeric, category_id) tensors.

    Returns
    -------
    numeric : (NUMERIC_CHANNELS,) float tensor
    category_id : () int64 scalar tensor
    """
    Ra_m = max(float(features.Ra_m), 1e-15)

    # 0,1: roughness in two complementary log scales
    Ra_log_um = math.log10(Ra_m / 1e-6)
    Ra_log_star = math.log10(Ra_m / max(scales.L_c, 1e-12))

    # 2,3,4: contact angle (cos primary, theta/pi auxiliary, mask)
    if features.theta_rad is None:
        cos_theta = 0.0          # neutral default (90 deg)
        theta_norm = 0.5         # neutral default
        theta_mask = 0.0
    else:
        cos_theta = math.cos(features.theta_rad)
        theta_norm = features.theta_rad / math.pi
        theta_mask = 1.0

    # 5,6: cavity radius (Phase 4)
    if features.r_c_m is None or features.r_c_m <= 0.0:
        r_c_log_star = 0.0
        r_c_mask = 0.0
    else:
        r_c_log_star = math.log10(features.r_c_m / max(scales.L_c, 1e-12))
        r_c_mask = 1.0

    # 7,8: site density (Phase 4); divide log10 by 6 to keep order-1 magnitude
    if features.N_s_per_m2 is None or features.N_s_per_m2 <= 0.0:
        N_s_log_norm = 0.0
        N_s_mask = 0.0
    else:
        N_s_log_norm = _safe_log10(features.N_s_per_m2) / 6.0
        N_s_mask = 1.0

    numeric = torch.tensor(
        [
            Ra_log_um,
            Ra_log_star,
            cos_theta,
            theta_norm,
            theta_mask,
            r_c_log_star,
            r_c_mask,
            N_s_log_norm,
            N_s_mask,
        ],
        dtype=dtype,
    )
    cat_id = torch.tensor(int(features.category_id), dtype=torch.long)
    return numeric, cat_id


def encode_batch_to_tensors(
    feats: Iterable[SurfaceFeatures],
    scales_lookup: dict[str, NondimScales] | None = None,
    *,
    default_pressures: dict[str, float] | None = None,
    dtype: torch.dtype = torch.float32,
) -> dict[str, torch.Tensor]:
    """Encode a list of features into batched dict[str, Tensor].

    ``scales_lookup`` may be supplied to avoid recomputing CoolProp scales for
    every call (recommended for training loops). When absent we lazily build
    one keyed by ``fluid`` using ``DEFAULT_FLUID_PRESSURES``.
    """
    pressures = {**DEFAULT_FLUID_PRESSURES, **(default_pressures or {})}
    cache: dict[str, NondimScales] = dict(scales_lookup or {})

    numerics: list[torch.Tensor] = []
    cat_ids: list[torch.Tensor] = []
    for f in feats:
        if f.fluid not in cache:
            P = pressures.get(f.fluid, 101_325.0)
            try:
                cache[f.fluid] = scales_for(f.fluid, P=P)
            except Exception:
                # Fallback to water at 1 atm if CoolProp lacks the fluid
                # (e.g. FC-72/FC-77). The category embedding will still
                # capture paper-level differences, and Phase 1 nondim is
                # only loosely sensitive to L_c through the log term.
                cache[f.fluid] = scales_for("water", P=101_325.0)
        num, cid = encode_features_to_tensor(f, cache[f.fluid], dtype=dtype)
        numerics.append(num)
        cat_ids.append(cid)

    return {
        "numeric": torch.stack(numerics, dim=0),
        "category_id": torch.stack(cat_ids, dim=0),
    }


# ---------------------------------------------------------------------------
# CSV loader
# ---------------------------------------------------------------------------
def load_features_from_dataset(
    csv_path: Path | str,
    fluid_default_pressure: dict[str, float] | None = None,  # noqa: ARG001
) -> tuple[list[SurfaceFeatures], list[str]]:
    """Load surface descriptors from ``onb_dataset.csv``.

    The CSV may contain repeated rows for the same ``surface_id``
    (multiple ONB points). We deduplicate by surface_id, keeping the first
    occurrence — Ra/theta are surface-level invariants in Phase 1.

    Returns
    -------
    features : list of SurfaceFeatures (deduplicated by surface_id)
    surface_ids : parallel list of surface ids
    """
    csv_path = Path(csv_path)
    seen: dict[str, SurfaceFeatures] = {}
    order: list[str] = []
    with csv_path.open("r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            sid = row["surface_id"].strip()
            if sid in seen:
                continue
            Ra_um = float(row["Ra_um"]) if row["Ra_um"] != "" else 0.0
            theta_str = row.get("theta_deg", "").strip()
            theta_deg = float(theta_str) if theta_str else None
            feat = SurfaceFeatures.from_dataset_row(
                Ra_um=Ra_um,
                theta_deg=theta_deg,
                category=row.get("category", ""),
                surface_id=sid,
                fluid=row.get("fluid", "water"),
                notes=row.get("notes", ""),
            )
            seen[sid] = feat
            order.append(sid)
    return [seen[s] for s in order], order


# ---------------------------------------------------------------------------
# Encoder module
# ---------------------------------------------------------------------------
class SurfaceEncoder(nn.Module):
    """Encode a surface descriptor to a latent vector.

    Pipeline
    --------
    numeric (B, NUMERIC_CHANNELS)  ──► LayerNorm
    category_id (B,) ──► nn.Embedding(category_count, category_emb_dim)
                                  ▼
                concat → Linear → GELU → Dropout → Linear → GELU → Dropout
                                  ▼
                              Linear → tanh  (bounded latent in [-1, 1])

    The final ``tanh`` keeps latents bounded; the main PINN can rescale freely.
    """

    def __init__(
        self,
        latent_dim: int = 16,
        hidden_dim: int = 64,
        category_count: int = len(PAPER_CATEGORIES),
        category_emb_dim: int = 4,
        dropout: float = 0.1,
        bounded_output: bool = True,
    ) -> None:
        super().__init__()
        self.latent_dim = int(latent_dim)
        self.hidden_dim = int(hidden_dim)
        self.category_count = int(category_count)
        self.category_emb_dim = int(category_emb_dim)
        self.numeric_dim = NUMERIC_CHANNELS
        self.bounded_output = bool(bounded_output)

        self.numeric_norm = nn.LayerNorm(self.numeric_dim)
        self.cat_embedding = nn.Embedding(self.category_count, self.category_emb_dim)
        nn.init.normal_(self.cat_embedding.weight, mean=0.0, std=0.1)

        in_dim = self.numeric_dim + self.category_emb_dim
        self.mlp = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, self.latent_dim),
        )

    # ---- shape contract ---------------------------------------------------
    @property
    def input_dim(self) -> int:
        """Dimension of the numeric channel only (for documentation)."""
        return self.numeric_dim

    @property
    def output_dim(self) -> int:
        return self.latent_dim

    # ---- forward ----------------------------------------------------------
    def forward(self, features_batch: dict[str, torch.Tensor]) -> torch.Tensor:
        """Encode a batched feature dict.

        Parameters
        ----------
        features_batch : dict with keys
            ``numeric``     -- (B, NUMERIC_CHANNELS) float
            ``category_id`` -- (B,) int64

        Returns
        -------
        z : (B, latent_dim) float tensor
        """
        numeric = features_batch["numeric"]
        category_id = features_batch["category_id"]
        if numeric.dim() != 2:
            raise ValueError(
                f"`numeric` must be (B, {self.numeric_dim}); got {tuple(numeric.shape)}"
            )
        if numeric.shape[1] != self.numeric_dim:
            raise ValueError(
                f"`numeric` channel mismatch: expected {self.numeric_dim}, "
                f"got {numeric.shape[1]}"
            )
        if category_id.dim() != 1:
            raise ValueError(
                f"`category_id` must be (B,); got {tuple(category_id.shape)}"
            )

        norm = self.numeric_norm(numeric)
        emb = self.cat_embedding(category_id)
        x = torch.cat([norm, emb], dim=-1)
        z = self.mlp(x)
        if self.bounded_output:
            z = torch.tanh(z)
        return z

    # ---- single-sample convenience ---------------------------------------
    @torch.no_grad()
    def encode(
        self,
        features: SurfaceFeatures,
        scales: NondimScales,
    ) -> torch.Tensor:
        """Encode one :class:`SurfaceFeatures` -> ``(latent_dim,)`` tensor."""
        was_training = self.training
        self.eval()
        try:
            num, cid = encode_features_to_tensor(features, scales)
            batch = {
                "numeric": num.unsqueeze(0),
                "category_id": cid.unsqueeze(0),
            }
            z = self.forward(batch)
            return z.squeeze(0)
        finally:
            if was_training:
                self.train()


# ---------------------------------------------------------------------------
# Self-test / smoke check
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="SurfaceEncoder smoke test")
    parser.add_argument(
        "--csv",
        type=str,
        default=str(
            Path(__file__).resolve().parents[3]
            / "02_data" / "processed" / "onb_dataset.csv"
        ),
        help="Path to onb_dataset.csv",
    )
    parser.add_argument("--latent-dim", type=int, default=16)
    args = parser.parse_args()

    torch.manual_seed(0)

    csv_path = Path(args.csv)
    print(f"[surface_encoder] loading dataset: {csv_path}")
    feats, sids = load_features_from_dataset(csv_path)
    print(f"  unique surfaces : {len(feats)}")
    print(f"  category vocab  : {PAPER_CATEGORIES}")

    # Build encoder
    encoder = SurfaceEncoder(latent_dim=args.latent_dim)
    n_params = sum(p.numel() for p in encoder.parameters())
    print(
        f"[surface_encoder] model params={n_params}, "
        f"input_dim(numeric)={encoder.input_dim}, output_dim={encoder.output_dim}"
    )

    # Pick a few representative surfaces:
    #   SFC-001 BETZ_Hydrophilic   (Ra=0.001 um = 1 nm, theta=20 deg, water)
    #   SFC-029 BOURDON15_OTS      (Ra=0.00043 um = 0.43 nm, theta=101.6 deg, water)
    #   SFC-038 JABARDO_Cu_Ra10p5  (Ra=10.5 um, theta=None, R-123)
    sids_of_interest = ["SFC-001", "SFC-029", "SFC-038"]
    by_id = {f.surface_id: f for f in feats}
    selected = [by_id[s] for s in sids_of_interest if s in by_id]

    if not selected:
        print("[surface_encoder] WARNING: target surfaces not found; using first 3.")
        selected = feats[:3]

    batch = encode_batch_to_tensors(selected)
    print("\n[surface_encoder] batched numeric tensor:")
    for f, row in zip(selected, batch["numeric"]):
        print(f"  {f.surface_id:14s}  fluid={f.fluid:7s}  num={row.tolist()}")

    z = encoder(batch)
    print(f"\n[surface_encoder] latent z shape   : {tuple(z.shape)}")
    print(f"[surface_encoder] latent value range: "
          f"min={z.min().item():+.4f} max={z.max().item():+.4f}  "
          f"mean={z.mean().item():+.4f}  std={z.std().item():.4f}")
    for f, zi in zip(selected, z):
        print(
            f"  {f.surface_id}: "
            f"||z||={zi.norm().item():.4f}, "
            f"first8={[round(v, 3) for v in zi[:8].tolist()]}"
        )

    # Encode-all-surfaces sanity check
    full = encode_batch_to_tensors(feats)
    z_all = encoder(full)
    print(
        f"\n[surface_encoder] full dataset: "
        f"z.shape={tuple(z_all.shape)}  finite={bool(torch.isfinite(z_all).all())}"
    )

    # Single-sample API
    scales_water = scales_for("water", P=101_325.0)
    z_single = encoder.encode(by_id["SFC-001"], scales_water)
    print(
        f"[surface_encoder] single-sample API: z.shape={tuple(z_single.shape)} "
        f"matches batched? "
        f"{torch.allclose(z_single, z[sids_of_interest.index('SFC-001')], atol=1e-6)}"
    )
