"""
dataset.py — OnbDataset: loads 02_data/processed/onb_dataset.csv and converts
every ONB data point into a nondimensional, surface-encoder-ready sample.

Design decisions
----------------
* FC-77 (and any other CoolProp-unsupported fluid) is silently dropped at
  construction time when ``skip_unsupported_fluids=True`` (default).
* NondimScales are pre-computed once per (fluid, P) pair at construction and
  cached, so the hot DataLoader path does no CoolProp calls.
* Surface features (Ra, theta) come directly from the CSV; r_c and N_s default
  to unknown (mask=0) because they require Phase-4 inverse recovery.
* train/val/test split is done at the surface_id level so that the same
  physical surface never appears in two splits.

Output sample dict keys
-----------------------
delta_T_wall_star   : float32 scalar tensor  (nondim wall superheat)
q_flux_star         : float32 scalar tensor  (nondim heat flux)
delta_T_sub_star    : float32 scalar tensor  (nondim subcooling)
surface_numeric     : (9,) float32 tensor    — numeric channel for SurfaceEncoder
category_id         : int64 scalar tensor    — category embedding index
fluid               : str                    — for diagnostics / MLflow
source_paper        : str
figure_ref          : str
surface_id          : str
pressure_pa         : float                  — dimensional [Pa], for loss_onb_hsu

Authors: PINN-ONB01 project
Date   : 2026-05-13
"""

from __future__ import annotations

import math
import random
from pathlib import Path
from typing import Any

import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset

from ..model.surface_encoder import (
    PAPER_CATEGORIES,
    SurfaceFeatures,
    category_to_id,
    encode_features_to_tensor,
)
from ..utils.nondim import NondimScales, compute_scales
from ..utils.properties import UnsupportedFluidError, saturation_properties

# ---------------------------------------------------------------------------
# Default atmospheric pressure mapping per fluid [Pa]
# ---------------------------------------------------------------------------
_DEFAULT_PRESSURE: dict[str, float] = {
    "water":  101_325.0,
    "r-123":  101_325.0,
    "r123":   101_325.0,
    "r-134a": 500_000.0,   # typical refrigeration test pressure
    "r134a":  500_000.0,
}

# Fluids that CoolProp 7.2 does not support — must be filtered.
_UNSUPPORTED_FLUIDS: frozenset[str] = frozenset({
    "fc-72", "fc72", "fc-77", "fc77", "hfe-7100", "hfe7100", "novec649",
})


def _fluid_pressure(fluid: str) -> float:
    """Return default operating pressure [Pa] for a given fluid label."""
    return _DEFAULT_PRESSURE.get(fluid.strip().lower(), 101_325.0)


def _is_supported(fluid: str) -> bool:
    return fluid.strip().lower() not in _UNSUPPORTED_FLUIDS


# ---------------------------------------------------------------------------
# OnbDataset
# ---------------------------------------------------------------------------
class OnbDataset(Dataset):
    """PyTorch Dataset wrapping ``onb_dataset.csv``.

    Parameters
    ----------
    csv_path : Path | str
        Absolute path to ``02_data/processed/onb_dataset.csv``.
    skip_unsupported_fluids : bool
        Drop rows whose fluid is not supported by CoolProp (default True).
        Set False only for debugging — will raise at property look-up.
    indices : list[int] | None
        If provided, expose only these row indices (used for splits).
    """

    def __init__(
        self,
        csv_path: Path | str,
        *,
        skip_unsupported_fluids: bool = True,
        indices: list[int] | None = None,
    ) -> None:
        super().__init__()
        self.csv_path = Path(csv_path)
        self.skip_unsupported_fluids = skip_unsupported_fluids

        # --- load raw CSV ---------------------------------------------------
        df = pd.read_csv(self.csv_path)

        # normalise column names (strip whitespace)
        df.columns = df.columns.str.strip()

        # --- optionally drop unsupported fluids ----------------------------
        if skip_unsupported_fluids:
            mask_ok = df["fluid"].apply(lambda f: _is_supported(str(f)))
            n_dropped = int((~mask_ok).sum())
            if n_dropped > 0:
                dropped = df.loc[~mask_ok, "fluid"].unique().tolist()
                print(
                    f"[OnbDataset] Skipping {n_dropped} rows "
                    f"with unsupported fluid(s): {dropped}"
                )
            df = df[mask_ok].reset_index(drop=True)

        self._df: pd.DataFrame = df

        # --- pre-compute NondimScales per (fluid, P) -----------------------
        self._scales: dict[str, NondimScales] = {}
        self._pressures: dict[str, float] = {}
        for fluid_raw in df["fluid"].unique():
            fluid = str(fluid_raw)
            P = _fluid_pressure(fluid)
            props = saturation_properties(fluid, P)
            self._scales[fluid] = compute_scales(props)
            self._pressures[fluid] = P

        # --- apply index subset (for splits) --------------------------------
        if indices is not None:
            self._indices: list[int] = list(indices)
        else:
            self._indices = list(range(len(df)))

    # -----------------------------------------------------------------------
    # Dataset protocol
    # -----------------------------------------------------------------------
    def __len__(self) -> int:
        return len(self._indices)

    def __getitem__(self, item: int) -> dict[str, Any]:
        row_idx = self._indices[item]
        row = self._df.iloc[row_idx]

        fluid: str = str(row["fluid"])
        scales = self._scales[fluid]
        P = self._pressures[fluid]

        # --- dimensional quantities from CSV (SI) --------------------------
        delta_T_wall: float = float(row["delta_T_wall"])   # [K]  (T_wall - T_sat)
        delta_T_sub: float  = float(row["delta_T_sub"])    # [K]  (T_sat  - T_bulk)
        q_flux: float       = float(row["q_flux"])         # [W/m²]

        # --- nondimensionalise ---------------------------------------------
        delta_T_wall_star = delta_T_wall / scales.delta_T_ref
        delta_T_sub_star  = delta_T_sub  / scales.delta_T_ref
        q_flux_star       = q_flux       / scales.q_ref

        # --- surface features ----------------------------------------------
        Ra_um_raw = row.get("Ra_um", None)
        Ra_um = float(Ra_um_raw) if (Ra_um_raw is not None and not _is_nan(Ra_um_raw)) else 0.0

        theta_raw = row.get("theta_deg", None)
        theta_deg: float | None = (
            float(theta_raw)
            if (theta_raw is not None and not _is_nan(theta_raw))
            else None
        )

        category_str: str = str(row.get("category", "unknown")).strip()

        # r_c weak label (Hsu inverse per-surface mean); column added in Phase 3.5.
        r_c_raw = row.get("r_c_um", None)
        r_c_um: float | None = (
            float(r_c_raw)
            if (r_c_raw is not None and not _is_nan(r_c_raw))
            else None
        )

        sf = SurfaceFeatures.from_dataset_row(
            Ra_um=Ra_um,
            theta_deg=theta_deg,
            category=category_str,
            surface_id=str(row.get("surface_id", "")),
            fluid=fluid,
            notes=str(row.get("notes", "")),
            r_c_um=r_c_um,
            N_s_per_cm2=None,
        )

        numeric, cat_id = encode_features_to_tensor(sf, scales)

        return {
            "delta_T_wall_star": torch.tensor(delta_T_wall_star, dtype=torch.float32),
            "q_flux_star":       torch.tensor(q_flux_star,       dtype=torch.float32),
            "delta_T_sub_star":  torch.tensor(delta_T_sub_star,  dtype=torch.float32),
            "surface_numeric":   numeric,          # (9,) float32
            "category_id":       cat_id,           # int64 scalar
            "fluid":             fluid,
            "source_paper":      str(row.get("source_paper", "")),
            "figure_ref":        str(row.get("figure_ref", "")),
            "surface_id":        str(row.get("surface_id", "")),
            "pressure_pa":       P,
        }

    # -----------------------------------------------------------------------
    # Convenience: surface_id → category_id mapping
    # -----------------------------------------------------------------------
    @staticmethod
    def surface_category_map(csv_path: Path | str) -> dict[str, int]:
        """Return {surface_id: category_id} for all rows in the CSV."""
        df = pd.read_csv(Path(csv_path))
        df.columns = df.columns.str.strip()
        result: dict[str, int] = {}
        for _, row in df.iterrows():
            sid = str(row["surface_id"]).strip()
            cat = str(row.get("category", "unknown")).strip()
            result[sid] = category_to_id(cat)
        return result

    # -----------------------------------------------------------------------
    # Property access
    # -----------------------------------------------------------------------
    @property
    def all_surface_ids(self) -> list[str]:
        return self._df.iloc[self._indices]["surface_id"].tolist()

    @property
    def all_fluids(self) -> list[str]:
        return self._df.iloc[self._indices]["fluid"].tolist()

    @property
    def nondim_scales(self) -> dict[str, NondimScales]:
        """Cached NondimScales per fluid label — for external use in losses."""
        return dict(self._scales)

    @property
    def pressures(self) -> dict[str, float]:
        """Default operating pressure [Pa] per fluid label."""
        return dict(self._pressures)


# ---------------------------------------------------------------------------
# NaN helper
# ---------------------------------------------------------------------------
def _is_nan(value: Any) -> bool:
    try:
        return math.isnan(float(value))
    except (TypeError, ValueError):
        return True


# ---------------------------------------------------------------------------
# collate function
# ---------------------------------------------------------------------------
def onb_collate_fn(batch: list[dict[str, Any]]) -> dict[str, Any]:
    """Custom collate: stacks tensors, keeps string lists as-is.

    DataLoader default collate converts string lists to awkward nested
    structures; this function keeps them as plain Python lists for easy
    indexing inside the training loop.
    """
    tensor_keys = {
        "delta_T_wall_star", "q_flux_star", "delta_T_sub_star",
        "surface_numeric", "category_id",
    }
    scalar_float_keys = {"pressure_pa"}
    string_keys = {"fluid", "source_paper", "figure_ref", "surface_id"}

    out: dict[str, Any] = {}

    for key in tensor_keys:
        out[key] = torch.stack([b[key] for b in batch], dim=0)

    for key in scalar_float_keys:
        out[key] = [b[key] for b in batch]

    for key in string_keys:
        out[key] = [b[key] for b in batch]

    return out


# ---------------------------------------------------------------------------
# Train / val / test split (surface_id-stratified)
# ---------------------------------------------------------------------------
def build_dataloaders(
    csv_path: Path | str,
    *,
    split: tuple[float, float, float] = (0.8, 0.1, 0.1),
    batch_size: int = 16,
    skip_unsupported_fluids: bool = True,
    seed: int = 42,
    num_workers: int = 0,
) -> tuple[DataLoader, DataLoader, DataLoader]:
    """Build train/val/test DataLoaders with surface_id-level splitting.

    The split is performed at the surface_id level to ensure that data from
    the same physical surface does not bleed across train and validation sets.
    Rows belonging to a given surface_id are either all in train, all in val,
    or all in test.

    Parameters
    ----------
    csv_path : Path | str
        Path to onb_dataset.csv.
    split : (train_frac, val_frac, test_frac)
        Fractions summing to 1.0.
    batch_size : int
    skip_unsupported_fluids : bool
    seed : int
        Random seed for reproducible splits.
    num_workers : int

    Returns
    -------
    (train_loader, val_loader, test_loader)
    """
    assert abs(sum(split) - 1.0) < 1e-6, f"split fractions must sum to 1.0, got {split}"

    # Build a full dataset first (to access df after filtering)
    full_ds = OnbDataset(
        csv_path,
        skip_unsupported_fluids=skip_unsupported_fluids,
    )
    df = full_ds._df

    # Collect unique surface_ids and shuffle deterministically
    unique_sids = df["surface_id"].unique().tolist()
    rng = random.Random(seed)
    rng.shuffle(unique_sids)

    n_total = len(unique_sids)
    n_train = max(1, round(split[0] * n_total))
    n_val   = max(1, round(split[1] * n_total))
    # test gets the remainder
    train_sids = set(unique_sids[:n_train])
    val_sids   = set(unique_sids[n_train : n_train + n_val])
    test_sids  = set(unique_sids[n_train + n_val :])

    # Map surface_id sets to row indices
    def _indices_for(sids: set[str]) -> list[int]:
        return [i for i, sid in enumerate(df["surface_id"].tolist()) if sid in sids]

    train_idx = _indices_for(train_sids)
    val_idx   = _indices_for(val_sids)
    test_idx  = _indices_for(test_sids)

    def _loader(indices: list[int], shuffle: bool) -> DataLoader:
        ds = OnbDataset.__new__(OnbDataset)
        # Shallow-copy the full dataset, then override indices
        ds.csv_path                  = full_ds.csv_path
        ds.skip_unsupported_fluids   = full_ds.skip_unsupported_fluids
        ds._df                       = full_ds._df
        ds._scales                   = full_ds._scales
        ds._pressures                = full_ds._pressures
        ds._indices                  = indices
        return DataLoader(
            ds,
            batch_size=batch_size,
            shuffle=shuffle,
            collate_fn=onb_collate_fn,
            num_workers=num_workers,
            drop_last=False,
        )

    return (
        _loader(train_idx, shuffle=True),
        _loader(val_idx,   shuffle=False),
        _loader(test_idx,  shuffle=False),
    )


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    ROOT = Path(__file__).resolve().parents[3]
    CSV = ROOT / "02_data" / "processed" / "onb_dataset.csv"
    if not CSV.is_file():
        print(f"[dataset] CSV not found at {CSV}; aborting self-test.")
        sys.exit(1)

    print(f"[dataset] loading {CSV}")
    ds = OnbDataset(CSV, skip_unsupported_fluids=True)
    print(f"[dataset] total samples (after FC-77 filter): {len(ds)}")

    sample = ds[0]
    print("\n[dataset] sample keys:", list(sample.keys()))
    for k, v in sample.items():
        if isinstance(v, torch.Tensor):
            print(f"  {k:25s}: shape={tuple(v.shape)}  dtype={v.dtype}  val={v.tolist()}")
        else:
            print(f"  {k:25s}: {v!r}")

    print("\n[dataset] building dataloaders (80/10/10 split)...")
    train_dl, val_dl, test_dl = build_dataloaders(
        CSV, split=(0.8, 0.1, 0.1), batch_size=8, seed=42,
    )
    print(f"  train batches={len(train_dl)}, val batches={len(val_dl)}, test batches={len(test_dl)}")

    batch = next(iter(train_dl))
    print("\n[dataset] first train batch:")
    for k, v in batch.items():
        if isinstance(v, torch.Tensor):
            print(f"  {k:25s}: shape={tuple(v.shape)}  dtype={v.dtype}")
        elif isinstance(v, list):
            print(f"  {k:25s}: list[{len(v)}]  first={v[0]!r}")

    print("\n[dataset] PAPER_CATEGORIES:", PAPER_CATEGORIES)
    cmap = OnbDataset.surface_category_map(CSV)
    print(f"[dataset] surface_category_map has {len(cmap)} entries")
    print("[dataset] self-test PASSED")
