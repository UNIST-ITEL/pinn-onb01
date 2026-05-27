"""
Loss-function subpackage for PINN-ONB01 (Section 4.3).

Four-term composite loss:
    L_total = w_conduction * L_conduction
            + w_bc        * (L_bc_low + L_bc_high)
            + w_data      * (L_data_dT + L_data_q)
            + w_onb       * L_onb

Each term is exposed as an independent function so that the training
orchestrator can log them separately to MLflow and tune weights independently.
"""

from .loss_functions import (
    LossComponents,
    LossWeights,
    loss_bc,
    loss_conduction,
    loss_data,
    loss_onb_hsu,
    total_loss,
)

__all__ = [
    "LossComponents",
    "LossWeights",
    "loss_conduction",
    "loss_bc",
    "loss_data",
    "loss_onb_hsu",
    "total_loss",
]
