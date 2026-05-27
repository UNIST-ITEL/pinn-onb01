"""Model subpackage — Surface encoder and main PINN architecture."""

from .surface_encoder import (
    SurfaceFeatures,
    SurfaceEncoder,
    PAPER_CATEGORIES,
    encode_features_to_tensor,
    encode_batch_to_tensors,
    load_features_from_dataset,
)
from .pinn import (
    PoolBoilingPINN,
    PINNOutputs,
    FiLMLayer,
    set_seed,
)

__all__ = [
    # surface encoder
    "SurfaceFeatures",
    "SurfaceEncoder",
    "PAPER_CATEGORIES",
    "encode_features_to_tensor",
    "encode_batch_to_tensors",
    "load_features_from_dataset",
    # main PINN
    "PoolBoilingPINN",
    "PINNOutputs",
    "FiLMLayer",
    "set_seed",
]
