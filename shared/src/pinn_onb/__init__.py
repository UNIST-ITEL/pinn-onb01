"""pinn_onb — shared package for PINN-BOILING workspace.

Phase 1 (pool boiling ONB), Phase 1.5 (in-house augmentation),
and Phase 2 (flow boiling) all import from this package.

Stage 1 status (2026-05-19; path updated 2026-05-27): SKELETON.
    Phase 1 source code now lives under
    ``phase1_pool_boiling/03_model/src/`` (relocated from the workspace
    root on 2026-05-27, folder names kept). This package re-exports those
    modules transparently so that downstream phase code can already say
    ``import pinn_onb`` without caring about the underlying location.
    Stage 2 (after Phase 1 acceptance) will physically move the code
    into this package and remove the path-injection shim below.
"""
from __future__ import annotations

import sys
from pathlib import Path

# --- Stage 1 shim: inject phase1_pool_boiling/03_model/src into sys.path
# so the legacy Phase 1 modules (model, loss, training, utils) become
# importable as regular top-level packages. Stage 2 will replace this with
# real code under pinn_onb/model, pinn_onb/loss, etc.
_WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
_LEGACY_SRC = _WORKSPACE_ROOT / "phase1_pool_boiling" / "03_model" / "src"
if _LEGACY_SRC.is_dir() and str(_LEGACY_SRC) not in sys.path:
    sys.path.insert(0, str(_LEGACY_SRC))

__version__ = "0.1.0-dev"
__stage__ = "1"  # workspace restructure stage: 1=skeleton, 2=full migration

__all__ = ["__version__", "__stage__"]
