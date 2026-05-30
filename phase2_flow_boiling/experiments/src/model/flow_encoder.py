"""
flow_encoder.py — Flow condition encoder for Phase 2 flow boiling ONB PINN.

Maps raw flow variables (Re, G, Bo, We, ΔT_sub, D_h, channel type) to a
latent vector z_flow consumed by the FlowBoilingPINN via FiLM conditioning.

Channel layout (FLOW_NUMERIC_CHANNELS = 11):
    0: log10(Re) / 5               -- Re typically 100-100,000; /5 → ~0.4-1.0
    1: log10(G / G_ref)            -- G_ref = 1000 kg/m²s; normalised mass flux
    2: log10(Bo × 1e4 + 1)        -- Boiling number Bo=q''/(G h_fg), small; +1 avoids log(0)
    3: log10(We + 1)               -- Weber number We=G²D_h/(ρ_l σ)
    4: delta_T_sub_star            -- ΔT_sub / T_sat (subcooling ratio)
    5: delta_T_sub_mask            -- 1 if ΔT_sub provided, else 0
    6: log10(D_h_mm + 0.01)        -- D_h in mm; log spans micro(0.05mm) to tube(15mm)
    7: channel_sin                 -- sin encoding of channel_type (see _CHANNEL_ENC)
    8: channel_cos                 -- cos encoding
    9: log10(P_r)                  -- reduced pressure P_r=P/P_crit (v10); P↑→ΔT_ONB↓ (trend #4)
   10: P_mask                      -- 1 if P provided, else 0 (atmospheric imputed)

Channel type encoding (sin/cos of evenly spaced angles, periodic-safe):
    tube_circular   → angle 0
    narrow_channel  → angle 2π/3
    microchannel    → angle 4π/3
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import torch
from torch import nn

# ── Channel type vocabulary ───────────────────────────────────────────────────
CHANNEL_TYPES: tuple[str, ...] = (
    "tube_circular",
    "narrow_channel",
    "microchannel",
)
_N_CHAN = len(CHANNEL_TYPES)
_CHANNEL_ANGLES: dict[str, float] = {
    ch: 2 * math.pi * i / _N_CHAN for i, ch in enumerate(CHANNEL_TYPES)
}


def channel_type_to_sincos(ch: str) -> tuple[float, float]:
    angle = _CHANNEL_ANGLES.get(ch, 0.0)
    return math.sin(angle), math.cos(angle)


# ── Input dimensionality ──────────────────────────────────────────────────────
FLOW_NUMERIC_CHANNELS: int = 11

# Reference values for normalization
_G_REF = 1000.0   # kg/m²s

# Critical pressure [kPa] per fluid for reduced pressure P_r = P/P_crit (v10).
# Used as a direct flow feature so the network can learn the P↑→ΔT_ONB↓ trend
# (CLAUDE.md physical trend #4) instead of inferring it only via properties.
_P_CRIT_KPA: dict[str, float] = {
    "water":  22064.0,
    "R-11":    4408.0,
    "R-113":   3392.0,
    "R-12":    4136.0,
    "R-134a":  4059.0,
    "R-123":   3662.0,
}
_P_ATM_KPA = 101.325


@dataclass(frozen=True)
class FlowFeatures:
    """Raw flow descriptor (SI / mixed units as noted).

    All unknowns should be passed as None — the encoder handles missing values
    via mask channels rather than silent imputation.
    """
    G_kg_m2s: float                  # mass flux [kg/m²s]  (>0; -1 signals unknown)
    D_h_mm: float                    # hydraulic diameter [mm]
    channel_type: str = "tube_circular"
    delta_T_sub_K: float | None = None   # inlet subcooling [K]; None if unknown
    # Derived on demand (optional pre-compute):
    Re: float | None = None          # Reynolds number = G D_h / μ_l
    Bo: float | None = None          # Boiling number  = q'' / (G h_fg)
    We: float | None = None          # Weber number    = G² D_h / (ρ_l σ)
    # Reference to compute derived quantities
    fluid: str = "water"
    P_kPa: float = 101.325

    @classmethod
    def from_dataset_row(
        cls,
        G_kg_m2s: float,
        D_h_mm: float,
        channel_type: str,
        delta_T_sub_K: float | None,
        fluid: str,
        P_kPa: float,
        q_onb_W_m2: float | None = None,   # needed for Bo
    ) -> "FlowFeatures":
        from utils.nondim_flow import compute_flow_nondim

        G = max(G_kg_m2s, 0.0) if G_kg_m2s > 0 else 0.0
        D_h_m = D_h_mm * 1e-3

        Re = Bo = We = None
        if G > 0 and D_h_m > 0:
            try:
                sc = compute_flow_nondim(fluid, P_kPa if P_kPa > 0 else 101.325)
                Re = G * D_h_m / sc.mu_l
                We = G**2 * D_h_m / (sc.rho_l * sc.sigma)
                if q_onb_W_m2 is not None and q_onb_W_m2 > 0 and sc.h_fg > 0:
                    Bo = q_onb_W_m2 / (G * sc.h_fg)
            except Exception:
                pass

        dtsub = float(delta_T_sub_K) if (delta_T_sub_K is not None and delta_T_sub_K > 0) else None

        return cls(
            G_kg_m2s=G_kg_m2s,
            D_h_mm=D_h_mm,
            channel_type=channel_type,
            delta_T_sub_K=dtsub,
            Re=Re, Bo=Bo, We=We,
            fluid=fluid, P_kPa=P_kPa,
        )


def encode_flow_to_tensor(
    feat: FlowFeatures,
    *,
    dtype: torch.dtype = torch.float32,
) -> torch.Tensor:
    """Encode one FlowFeatures → (FLOW_NUMERIC_CHANNELS,) tensor."""
    from utils.nondim_flow import compute_flow_nondim

    G = max(feat.G_kg_m2s, 1.0) if feat.G_kg_m2s > 0 else 1.0

    # Re
    Re_val = feat.Re
    if Re_val is None or Re_val <= 0:
        Re_val = 1.0
    ch0 = math.log10(max(Re_val, 1.0)) / 5.0

    # G
    ch1 = math.log10(G / _G_REF)

    # Bo
    Bo_val = feat.Bo
    ch2 = math.log10(max(Bo_val * 1e4, 0.0) + 1.0) if (Bo_val and Bo_val > 0) else 0.0

    # We
    We_val = feat.We
    ch3 = math.log10(max(We_val, 0.0) + 1.0) if (We_val and We_val > 0) else 0.0

    # ΔT_sub
    if feat.delta_T_sub_K is not None and feat.delta_T_sub_K > 0:
        try:
            sc = compute_flow_nondim(feat.fluid, feat.P_kPa if feat.P_kPa > 0 else 101.325)
            ch4 = feat.delta_T_sub_K / sc.T_sat_K
        except Exception:
            ch4 = feat.delta_T_sub_K / 373.15  # fallback: water at 1 atm
        ch5 = 1.0
    else:
        ch4 = 0.0
        ch5 = 0.0

    # D_h
    ch6 = math.log10(max(feat.D_h_mm, 0.01) + 0.01)

    # Channel type
    s, c = channel_type_to_sincos(feat.channel_type)
    ch7, ch8 = s, c

    # Reduced pressure P_r = P/P_crit (v10). Missing P → atmospheric, mask=0.
    P_crit = _P_CRIT_KPA.get(feat.fluid.split("_")[0], _P_CRIT_KPA["water"])
    if feat.P_kPa is not None and feat.P_kPa > 0:
        P_use = feat.P_kPa
        ch10  = 1.0
    else:
        P_use = _P_ATM_KPA
        ch10  = 0.0
    P_r  = max(P_use / P_crit, 1e-6)
    ch9  = math.log10(P_r)

    return torch.tensor(
        [ch0, ch1, ch2, ch3, ch4, ch5, ch6, ch7, ch8, ch9, ch10],
        dtype=dtype,
    )


def encode_flow_batch(
    feats: Sequence[FlowFeatures],
    *,
    dtype: torch.dtype = torch.float32,
) -> torch.Tensor:
    """Encode a list of FlowFeatures → (B, FLOW_NUMERIC_CHANNELS) tensor."""
    return torch.stack([encode_flow_to_tensor(f, dtype=dtype) for f in feats], dim=0)


# ── Encoder module ────────────────────────────────────────────────────────────

class FlowEncoder(nn.Module):
    """Encode flow conditions to a latent vector z_flow.

    Pipeline
    --------
    numeric (B, FLOW_NUMERIC_CHANNELS)
        ▼ LayerNorm
        ▼ Linear → GELU → Dropout
        ▼ Linear → GELU → Dropout
        ▼ Linear → tanh  (bounded latent in [-1, 1])

    Initialises as near-identity (small weights) so that at the start of
    transfer learning the flow conditioning has minimal disturbance on the
    Phase-1-pretrained backbone.
    """

    def __init__(
        self,
        latent_dim: int = 8,
        hidden_dim: int = 32,
        dropout: float = 0.1,
        small_init: bool = True,
    ) -> None:
        super().__init__()
        self.latent_dim = int(latent_dim)
        self.hidden_dim = int(hidden_dim)

        self.norm = nn.LayerNorm(FLOW_NUMERIC_CHANNELS)
        self.mlp = nn.Sequential(
            nn.Linear(FLOW_NUMERIC_CHANNELS, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, latent_dim),
        )

        if small_init:
            # Keep output near zero at init → FiLM starts as identity
            nn.init.normal_(self.mlp[-1].weight, std=0.01)
            nn.init.zeros_(self.mlp[-1].bias)

    @property
    def output_dim(self) -> int:
        return self.latent_dim

    def forward(self, numeric: torch.Tensor) -> torch.Tensor:
        """
        Parameters
        ----------
        numeric : (B, FLOW_NUMERIC_CHANNELS)

        Returns
        -------
        z_flow : (B, latent_dim)
        """
        z = self.mlp(self.norm(numeric))
        return torch.tanh(z)
