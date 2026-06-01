"""figlib.py — shared helpers for Phase 2 manuscript figure scripts.

Each fig_*.py script in this folder generates one manuscript figure. Run from
the phase2_flow_boiling/ root, e.g.::

    python analysis/scripts/fig_pressure_trend.py

Every script writes PNG+PDF to analysis/figures/ AND copies both into
manuscript/figures/ (single graphicspath), so editing a figure never leaves the
submission package stale. Shared model/dataset loading and styling live here.

Notes / caveats (see PROGRESS_LOG.md § Figure 인벤토리):
  - scipy is NOT installed → use math.erf for Gaussian coverage.
  - v9 checkpoint has a 9-channel flow encoder; the current code is 11-channel,
    so v9 cannot be loaded with build_model (no pressure-blind overlay).
  - FINAL best model = v11 (phase2_v11_highP_wang).
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt  # noqa: E402

PROJ = Path(__file__).resolve().parents[2]          # phase2_flow_boiling/
SRC = PROJ / "experiments" / "src"
FIG_ANALYSIS = PROJ / "analysis" / "figures"
FIG_MANUSCRIPT = PROJ / "manuscript" / "figures"
CSV = PROJ / "data" / "raw" / "onb_dataset_phase2_raw.csv"

V11_CONFIG = PROJ / "experiments" / "configs" / "phase2_v11_highP_wang.yaml"
V11_CKPT = PROJ / "experiments" / "checkpoints" / "phase2_v11_highP_wang" / "best_model.pt"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def set_style() -> None:
    mpl.rcParams.update({
        "font.family": "sans-serif", "font.size": 10,
        "axes.spines.top": False, "axes.spines.right": False,
        "figure.dpi": 150, "savefig.bbox": "tight",
    })


def save_fig(fig, name: str) -> None:
    """Save <name>.png and <name>.pdf to analysis/figures AND manuscript/figures."""
    FIG_ANALYSIS.mkdir(parents=True, exist_ok=True)
    FIG_MANUSCRIPT.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "pdf"):
        src = FIG_ANALYSIS / f"{name}.{ext}"
        fig.savefig(src)
        shutil.copy(src, FIG_MANUSCRIPT / f"{name}.{ext}")
    plt.close(fig)
    print(f"saved {name}.png/.pdf  →  analysis/figures/ + manuscript/figures/")


def load_v11():
    """Return (model, device) for the FINAL best v11 model, in eval mode."""
    import torch
    from train import build_model, load_config
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    cfg = load_config(str(V11_CONFIG))
    model = build_model(cfg, device)
    state = torch.load(str(V11_CKPT), map_location=device)["model_state"]
    model.load_state_dict(state)
    model.eval()
    return model, device, cfg


def load_dataframe(split: str = "all"):
    """Return (FlowBoilingDataset, its DataFrame) for the given split (seed=42)."""
    from data.dataset import FlowBoilingDataset
    ds = FlowBoilingDataset(str(CSV), split=split, seed=42)
    return ds, ds._df.reset_index(drop=True)


def predict_dT(model, device, ds):
    """Ensemble-free ΔT_ONB [K] prediction over a dataset (in dataset order)."""
    import numpy as np
    import torch
    from torch.utils.data import DataLoader
    from data.dataset import collate_fn
    out = []
    with torch.no_grad():
        for b in DataLoader(ds, batch_size=64, shuffle=False, collate_fn=collate_fn):
            o = model(b["x_star"].to(device),
                      {k: v.to(device) for k, v in b["surface_features"].items()},
                      b["flow_numeric"].to(device))
            out.append((o.delta_T_onb_star.squeeze(-1) * b["dT_ref"].to(device)).cpu().numpy())
    return np.concatenate(out)


# Consistent source labels / order used across figures.
SOURCE_LABELS = {
    "liu2005": "Liu 2005", "forrest2016": "Forrest 2016", "kuang2025": "Kuang 2024",
    "cheng2022": "Cheng 2022", "qu2002": "Qu 2002", "alyahia2017": "Al-Yahia 2017",
    "wang2024": "Wang 2024", "hong2012": "Hong 2012", "kandlikar1991": "Kandlikar 1991",
}
