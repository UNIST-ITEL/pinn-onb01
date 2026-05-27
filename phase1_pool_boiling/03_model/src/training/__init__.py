"""
training package — Phase 1-4 sequential PINN training pipeline.

Sub-modules
-----------
dataset     : OnbDataset (torch.utils.data.Dataset), DataLoader helpers
lhs_sampler : LHSCollocationSampler for collocation point generation
train       : run_training / run_phase entry-points + Phase 1-4 loops
"""

from __future__ import annotations

from .dataset import OnbDataset, onb_collate_fn, build_dataloaders
from .lhs_sampler import LHSCollocationSampler
from .train import run_training, run_phase

__all__ = [
    "OnbDataset",
    "onb_collate_fn",
    "build_dataloaders",
    "LHSCollocationSampler",
    "run_training",
    "run_phase",
]
