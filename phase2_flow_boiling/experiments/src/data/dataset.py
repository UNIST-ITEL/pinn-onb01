"""
dataset.py — Phase 2 flow boiling ONB dataset loader.

Reads onb_dataset_phase2_raw.csv and produces:
  - surface_features dict  (Phase 1 SurfaceEncoder format)
  - flow_numeric tensor    (FlowEncoder format)
  - x_star tensor          (axial location, default 0.5 for parity-plot data)
  - targets dict           {delta_T_onb_K, q_onb_W_m2, delta_T_onb_star, q_onb_star}
  - nondim_scales          FlowNondimScales per fluid

Train/val/test split: 70/15/15, stratified by paper_id to preserve fluid/condition balance.

CLAUDE.md naming: G_kg_m2s, D_h_mm, delta_T_sub_K, q_onb_W_m2, delta_T_onb_K.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Literal

import pandas as pd
import torch
from torch.utils.data import Dataset

_SRC = Path(__file__).resolve().parents[1]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from model.flow_encoder import FlowFeatures, encode_flow_to_tensor
from utils.nondim_flow import compute_flow_nondim

_P1_MODEL_ROOT = (
    Path(__file__).resolve().parents[4]
    / "phase1_pool_boiling" / "03_model"
)
if str(_P1_MODEL_ROOT) not in sys.path:
    sys.path.insert(0, str(_P1_MODEL_ROOT))

from src.model.surface_encoder import (
    SurfaceFeatures,
    encode_features_to_tensor,
    DEFAULT_FLUID_PRESSURES,
)
from src.utils.nondim import scales_for

# ── Default Ra for surfaces without measurement (log10(1)=0 → neutral) ────────
_DEFAULT_RA_UM = 1.0

# ── Nondim reference scales ───────────────────────────────────────────────────
# q_ref: physics-based (ρ_l h_fg √(σ/ρ_l g) g) — ~5×10⁷ W/m² for water
# dT_ref: fixed 20 K — mid-range of physical ONB superheat (2-30 K for water).
#   The capillary temperature σ T_sat/(h_fg ρ_l L_c) ≈ 4 μK for water, so
#   it is always overridden by this floor, giving stable O(1) nondim targets.
_NONDIM_Q_REF   = 1e6    # W/m²  fallback when CoolProp unavailable
_NONDIM_DT_REF  = 20.0   # K     fixed reference for all fluids


def _get_surface_scales(fluid: str, P_kPa: float):
    """Return Phase 1 NondimScales for surface encoder."""
    try:
        P_Pa = (P_kPa * 1e3) if P_kPa > 0 else DEFAULT_FLUID_PRESSURES.get(fluid, 101_325.0)
        return scales_for(fluid.split("_")[0], P=P_Pa)
    except Exception:
        return scales_for("water", P=101_325.0)


def _surface_feat_from_row(row: pd.Series) -> SurfaceFeatures:
    Ra_um = float(row["Ra_um"]) if float(row["Ra_um"]) > 0 else _DEFAULT_RA_UM
    theta_deg = float(row["theta_deg"]) if float(row["theta_deg"]) > 0 else None
    fluid = str(row["fluid"])
    return SurfaceFeatures.from_dataset_row(
        Ra_um=Ra_um,
        theta_deg=theta_deg,
        category=str(row["surface_cat"]),
        surface_id=f"{row['paper_id']}_{row['surface_cat']}",
        fluid=fluid,
    )


def _flow_feat_from_row(row: pd.Series) -> FlowFeatures:
    G = float(row["G_kg_m2s"])
    D_h = float(row["D_h_mm"])
    ch_type = str(row["channel_type"])
    dtsub = float(row["delta_T_sub_K"]) if row["delta_T_sub_K"] > 0 else None
    fluid = str(row["fluid"])
    # Pass raw P (incl. -1 = unknown) so the encoder can set P_mask=0 and
    # impute atmospheric internally; property nondim still falls back to 1 atm.
    P_kPa = float(row["P_kPa"])
    q_onb = float(row["q_onb_W_m2"]) if row["q_onb_W_m2"] > 0 else None
    return FlowFeatures.from_dataset_row(
        G_kg_m2s=max(G, 0.0),
        D_h_mm=max(D_h, 0.01),
        channel_type=ch_type,
        delta_T_sub_K=dtsub,
        fluid=fluid,
        P_kPa=P_kPa,
        q_onb_W_m2=q_onb,
    )


def _hsu_nd_coeff(sc: "FlowNondimScales", q_ref: float, dT_ref: float,
                  fluid: str) -> float:
    """Per-fluid Hsu nondim coefficient C such that dT_star_hsu = C * sqrt(q_star).

    Derived from Hsu (1962): ΔT_ONB = sqrt(8σ T_sat q / (k_l h_fg ρ_v))
    → C = sqrt(8σ T_sat q_ref / (k_l h_fg ρ_v)) / dT_ref
    """
    try:
        import CoolProp.CoolProp as CP
        rho_v = float(CP.PropsSI("D", "P", sc.P_kPa * 1e3, "Q", 1,
                                 fluid.split("_")[0]))
    except Exception:
        rho_v = sc.P_kPa * 1e3 / (461.5 * sc.T_sat_K)  # ideal gas fallback
    rho_v = max(rho_v, 0.01)
    denom = sc.k_l * sc.h_fg * rho_v
    if denom <= 0:
        return 1.0
    A = math.sqrt(8.0 * sc.sigma * sc.T_sat_K * q_ref / denom)
    return A / max(dT_ref, 1e-6)


def _nondim_target(
    q_onb_W_m2: float | None,
    delta_T_onb_K: float | None,
    fluid: str,
    P_kPa: float,
) -> dict[str, float | None]:
    """Nondimensionalise ONB targets using fluid properties."""
    try:
        sc = compute_flow_nondim(fluid, P_kPa if P_kPa > 0 else 101.325)
        q_ref  = sc.rho_l * sc.h_fg * math.sqrt(sc.sigma / (sc.rho_l * 9.81)) * 9.81
        dT_ref = _NONDIM_DT_REF  # fixed 20 K — see constant definition above
        C_hsu  = _hsu_nd_coeff(sc, q_ref, dT_ref, fluid)
    except Exception:
        q_ref  = _NONDIM_Q_REF
        dT_ref = _NONDIM_DT_REF
        C_hsu  = 1.0

    q_star  = q_onb_W_m2 / q_ref   if (q_onb_W_m2  is not None and q_onb_W_m2  > 0) else None
    dT_star = delta_T_onb_K / dT_ref if (delta_T_onb_K is not None and delta_T_onb_K > 0) else None
    return {"q_onb_star": q_star, "delta_T_onb_star": dT_star,
            "q_ref": q_ref, "dT_ref": dT_ref, "C_hsu_nd": C_hsu}


class FlowBoilingDataset(Dataset):
    """PyTorch Dataset for Phase 2 flow boiling ONB data.

    Each item is a dict:
        x_star          : (1,)  float32  — axial location (0.5 default)
        surf_numeric    : (9,)  float32  — surface encoder input
        surf_cat_id     : ()    int64    — surface category id
        flow_numeric    : (9,)  float32  — flow encoder input
        q_onb_W_m2      : scalar float32  — raw target (NaN if absent)
        delta_T_onb_K   : scalar float32  — raw target (NaN if absent)
        q_onb_star      : scalar float32  — nondim target (NaN if absent)
        delta_T_onb_star: scalar float32  — nondim target (NaN if absent)
        has_q           : bool tensor     — q_onb available
        has_dT          : bool tensor     — delta_T_onb available
    """

    def __init__(
        self,
        csv_path: str | Path,
        split: Literal["train", "val", "test", "all"] = "all",
        train_frac: float = 0.70,
        val_frac: float = 0.15,
        seed: int = 42,
        exclude_onb_not_found: bool = True,
        holdout_paper: str | None = None,
    ) -> None:
        self.csv_path = Path(csv_path)
        df = pd.read_csv(self.csv_path)

        if exclude_onb_not_found:
            df = df[~df["notes"].str.contains("ONB_NOT_FOUND", na=False)].copy()

        # Keep rows with at least one valid ONB target
        has_q  = df["q_onb_W_m2"] > 0
        has_dT = df["delta_T_onb_K"] > 0
        df = df[has_q | has_dT].reset_index(drop=True)

        # Leave-one-study-out (LOSO): the held-out paper is the entire test set;
        # train/val are drawn from the remaining studies only. Otherwise use the
        # default per-paper stratified split.
        if holdout_paper is not None:
            df = self._loso_split(df, split, holdout_paper, train_frac, val_frac, seed)
        elif split != "all":
            df = self._stratified_split(df, split, train_frac, val_frac, seed)

        self._df = df.reset_index(drop=True)
        self._precompute()

    def _stratified_split(
        self,
        df: pd.DataFrame,
        split: str,
        train_frac: float,
        val_frac: float,
        seed: int,
    ) -> pd.DataFrame:
        import numpy as np
        rng = np.random.default_rng(seed)
        train_idx, val_idx, test_idx = [], [], []
        for pid in df["paper_id"].unique():
            idx = df.index[df["paper_id"] == pid].tolist()
            rng.shuffle(idx)
            n = len(idx)
            n_train = max(1, int(n * train_frac))
            n_val   = max(1, int(n * val_frac))
            train_idx.extend(idx[:n_train])
            val_idx.extend(idx[n_train: n_train + n_val])
            test_idx.extend(idx[n_train + n_val:])
        mapping = {"train": train_idx, "val": val_idx, "test": test_idx}
        return df.loc[mapping[split]]

    def _loso_split(
        self,
        df: pd.DataFrame,
        split: str,
        holdout_paper: str,
        train_frac: float,
        val_frac: float,
        seed: int,
    ) -> pd.DataFrame:
        """Leave-one-study-out split: holdout_paper -> test; rest -> train/val."""
        import numpy as np
        if holdout_paper not in set(df["paper_id"]):
            raise ValueError(f"holdout_paper '{holdout_paper}' not in dataset")
        if split == "test":
            return df.loc[df.index[df["paper_id"] == holdout_paper].tolist()]
        # train/val drawn from the remaining studies, stratified by paper_id
        rng = np.random.default_rng(seed)
        tr_ratio = train_frac / (train_frac + val_frac)
        train_idx, val_idx = [], []
        rest = [p for p in df["paper_id"].unique() if p != holdout_paper]
        for pid in rest:
            idx = df.index[df["paper_id"] == pid].tolist()
            rng.shuffle(idx)
            n_tr = max(1, int(len(idx) * tr_ratio))
            train_idx.extend(idx[:n_tr])
            val_idx.extend(idx[n_tr:])
        return df.loc[train_idx if split == "train" else val_idx]

    def _precompute(self) -> None:
        """Pre-encode all rows into tensors for fast __getitem__."""
        self._items: list[dict[str, torch.Tensor]] = []

        for _, row in self._df.iterrows():
            fluid  = str(row["fluid"])
            P_kPa  = float(row["P_kPa"]) if row["P_kPa"] > 0 else 101.325

            # Surface encoding
            sf     = _surface_feat_from_row(row)
            sc     = _get_surface_scales(fluid, P_kPa)
            s_num, s_cat = encode_features_to_tensor(sf, sc)

            # Flow encoding
            ff     = _flow_feat_from_row(row)
            f_num  = encode_flow_to_tensor(ff)

            # Targets
            q_raw  = float(row["q_onb_W_m2"])  if row["q_onb_W_m2"]  > 0 else float("nan")
            dT_raw = float(row["delta_T_onb_K"]) if row["delta_T_onb_K"] > 0 else float("nan")

            nd = _nondim_target(
                q_raw  if not math.isnan(q_raw)  else None,
                dT_raw if not math.isnan(dT_raw) else None,
                fluid, P_kPa,
            )
            q_star  = nd["q_onb_star"]  if nd["q_onb_star"]  is not None else float("nan")
            dT_star = nd["delta_T_onb_star"] if nd["delta_T_onb_star"] is not None else float("nan")

            self._items.append({
                "x_star":           torch.tensor([0.5], dtype=torch.float32),
                "surf_numeric":     s_num,
                "surf_cat_id":      s_cat,
                "flow_numeric":     f_num,
                "q_onb_W_m2":       torch.tensor(q_raw,  dtype=torch.float32),
                "delta_T_onb_K":    torch.tensor(dT_raw, dtype=torch.float32),
                "q_onb_star":       torch.tensor(q_star, dtype=torch.float32),
                "delta_T_onb_star": torch.tensor(dT_star, dtype=torch.float32),
                "has_q":            torch.tensor(not math.isnan(q_raw),  dtype=torch.bool),
                "has_dT":           torch.tensor(not math.isnan(dT_raw), dtype=torch.bool),
                # Per-sample nondim scales (needed for dimensional evaluation)
                "dT_ref":    torch.tensor(nd["dT_ref"],   dtype=torch.float32),
                "q_ref":     torch.tensor(nd["q_ref"],    dtype=torch.float32),
                # Hsu coupling coefficient: dT_star_hsu = C_hsu_nd * sqrt(q_star)
                "C_hsu_nd":  torch.tensor(nd["C_hsu_nd"], dtype=torch.float32),
            })

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        return self._items[idx]

    @property
    def n_with_q(self) -> int:
        return sum(1 for item in self._items if item["has_q"])

    @property
    def n_with_dT(self) -> int:
        return sum(1 for item in self._items if item["has_dT"])

    @property
    def n_with_both(self) -> int:
        return sum(1 for item in self._items if item["has_q"] and item["has_dT"])


def collate_fn(batch: list[dict[str, torch.Tensor]]) -> dict[str, torch.Tensor]:
    """Custom collate: stack tensors, keep surface_features in Phase 1 dict format."""
    keys = batch[0].keys()
    out: dict[str, torch.Tensor] = {}
    for k in keys:
        tensors = [b[k] for b in batch]
        if tensors[0].dim() == 0:
            out[k] = torch.stack(tensors)
        else:
            out[k] = torch.stack(tensors, dim=0)
    # Wrap surface features in Phase 1 format
    out["surface_features"] = {
        "numeric":     out.pop("surf_numeric"),
        "category_id": out.pop("surf_cat_id"),
    }
    return out


# ── Quick dataset stats ───────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--csv", default="data/raw/onb_dataset_phase2_raw.csv")
    args = p.parse_args()

    csv = Path(args.csv)
    if not csv.is_file():
        csv = Path(__file__).resolve().parents[4] / "data" / "raw" / "onb_dataset_phase2_raw.csv"

    print(f"Loading: {csv}")
    ds_all   = FlowBoilingDataset(csv, split="all")
    ds_train = FlowBoilingDataset(csv, split="train")
    ds_val   = FlowBoilingDataset(csv, split="val")
    ds_test  = FlowBoilingDataset(csv, split="test")

    print(f"\nDataset split (stratified by paper_id, seed=42):")
    print(f"  total : {len(ds_all):4d}  q={ds_all.n_with_q}  dT={ds_all.n_with_dT}  both={ds_all.n_with_both}")
    print(f"  train : {len(ds_train):4d}  q={ds_train.n_with_q}  dT={ds_train.n_with_dT}")
    print(f"  val   : {len(ds_val):4d}  q={ds_val.n_with_q}  dT={ds_val.n_with_dT}")
    print(f"  test  : {len(ds_test):4d}  q={ds_test.n_with_q}  dT={ds_test.n_with_dT}")

    from torch.utils.data import DataLoader
    loader = DataLoader(ds_train, batch_size=16, collate_fn=collate_fn, shuffle=True)
    batch  = next(iter(loader))
    print(f"\nSample batch keys: {list(batch.keys())}")
    print(f"  x_star          : {batch['x_star'].shape}")
    print(f"  flow_numeric    : {batch['flow_numeric'].shape}")
    print(f"  surf numeric    : {batch['surface_features']['numeric'].shape}")
    print(f"  q_onb_W_m2      : {batch['q_onb_W_m2'].shape}  (NaN: {batch['q_onb_W_m2'].isnan().sum().item()})")
    print(f"  delta_T_onb_K   : {batch['delta_T_onb_K'].shape}  (NaN: {batch['delta_T_onb_K'].isnan().sum().item()})")
