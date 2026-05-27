"""
train.py — Phase 1-4 sequential PINN training pipeline (Section 4.5).

Phase 1 : Analytical warm-up        — PDE + BC losses only, no data.
Phase 2 : Synthetic data learning   — PDE + BC + synthetic data (skeleton).
Phase 3 : Experimental fine-tuning  — all four losses, Adam → L-BFGS.
Phase 4 : Inverse problem           — r_c as learnable parameter (skeleton).

Public API
----------
run_training(config_path, phase, checkpoint_dir, mlflow_uri) -> dict
run_phase(phase, model, config, train_loader, val_loader) -> dict

CLI usage (from 03_model/):
    python -m src.training.train --config configs/baseline_phaseA.yaml --phase all
    python -m src.training.train --config configs/baseline_phaseA.yaml \\
        --phase 3 --resume checkpoints/phase2_best.pt

Authors: PINN-ONB01 project
Date   : 2026-05-13
"""

from __future__ import annotations

import argparse
import copy
import math
import time
from pathlib import Path
from typing import Any

import torch
import torch.nn as nn
import yaml
from torch.utils.data import DataLoader

# ---------------------------------------------------------------------------
# Optional MLflow import — gracefully degrade if not installed
# ---------------------------------------------------------------------------
try:
    import mlflow  # type: ignore[import]
    import mlflow.pytorch  # type: ignore[import]
    _MLFLOW_AVAILABLE = True
except ImportError:
    _MLFLOW_AVAILABLE = False
    print("[train] WARNING: mlflow not installed — logging disabled.")

from ..loss.loss_functions import (
    LossComponents,
    LossWeights,
    loss_bc,
    loss_conduction,
    loss_data,
    loss_monotonicity,
    loss_onb_hsu,
    total_loss,
)
from ..model.pinn import PoolBoilingPINN
from ..model.surface_encoder import SurfaceEncoder, encode_batch_to_tensors
from ..utils.nondim import NondimScales, scales_for
from ..utils.properties import saturation_properties
from .dataset import OnbDataset, build_dataloaders
from .lhs_sampler import CollocationDomain, LHSCollocationSampler

# ---------------------------------------------------------------------------
# Timing helper
# ---------------------------------------------------------------------------

def _fmt_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------

def load_config(config_path: Path) -> dict[str, Any]:
    """Load YAML config and return as a plain dict."""
    with open(config_path, "r") as fh:
        cfg = yaml.safe_load(fh)
    return cfg


def _device(cfg: dict[str, Any]) -> torch.device:
    requested = str(cfg.get("device", "cpu"))
    if requested == "cuda" and not torch.cuda.is_available():
        print("[train] WARNING: CUDA requested but not available — using CPU.")
        return torch.device("cpu")
    return torch.device(requested)


# ---------------------------------------------------------------------------
# Checkpoint helpers
# ---------------------------------------------------------------------------

def _save_checkpoint(
    model: PoolBoilingPINN,
    optimizer: torch.optim.Optimizer,
    epoch: int,
    best_val_loss: float,
    path: Path,
    extra: dict[str, Any] | None = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "epoch": epoch,
        "model_state": model.state_dict(),
        "optimizer_state": optimizer.state_dict(),
        "best_val_loss": best_val_loss,
    }
    if extra:
        payload.update(extra)
    torch.save(payload, path)


def _load_checkpoint(
    model: PoolBoilingPINN,
    optimizer: torch.optim.Optimizer | None,
    path: Path,
    device: torch.device,
) -> dict[str, Any]:
    ckpt = torch.load(path, map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model_state"])
    if optimizer is not None and "optimizer_state" in ckpt:
        try:
            optimizer.load_state_dict(ckpt["optimizer_state"])
        except Exception:
            pass  # shape mismatch if switching optimizers between phases
    return ckpt


# ---------------------------------------------------------------------------
# Model builder
# ---------------------------------------------------------------------------

def build_model(cfg: dict[str, Any], device: torch.device) -> PoolBoilingPINN:
    """Construct PoolBoilingPINN from config dict."""
    model_cfg = cfg.get("model", {})
    enc_cfg   = model_cfg.get("surface_encoder", {})
    pinn_cfg  = model_cfg.get("pinn", {})

    latent_dim   = int(enc_cfg.get("latent_dim", 16))
    hidden_dim   = int(pinn_cfg.get("hidden_dim", 64))
    n_layers     = int(pinn_cfg.get("n_layers", 5))
    conditioning = str(model_cfg.get("conditioning", "concat"))

    encoder = SurfaceEncoder(latent_dim=latent_dim)
    model   = PoolBoilingPINN(
        encoder=encoder,
        latent_dim=latent_dim,
        hidden_dim=hidden_dim,
        n_layers=n_layers,
        conditioning=conditioning,
        seed=int(cfg.get("seed", 42)),
    )
    model = model.to(device)
    return model


# ---------------------------------------------------------------------------
# Collocation sampler builder
# ---------------------------------------------------------------------------

def _build_sampler(cfg: dict[str, Any], device: torch.device) -> LHSCollocationSampler:
    domain_cfg = cfg.get("domain", {})
    coll_cfg   = cfg.get("collocation", {})

    fluid_default = str(domain_cfg.get("fluid_default", "water"))
    P_default     = float(domain_cfg.get("P_default", 101_325.0))
    L_plate_m     = float(domain_cfg.get("L_plate_m", 1.0e-3))

    sc = scales_for(fluid_default, P=P_default)
    L_plate_star = LHSCollocationSampler.compute_L_plate_star(L_plate_m, sc.L_c)

    domain = CollocationDomain(L_plate_star=L_plate_star)

    return LHSCollocationSampler(
        domain=domain,
        sample_operating=False,  # Phase 1/2 use spatial-only; Phase 3 data provides q
        device=device,
    )


# ---------------------------------------------------------------------------
# Validation step (used by all phases)
# ---------------------------------------------------------------------------

def _validate(
    model: PoolBoilingPINN,
    val_loader: DataLoader,
    weights: LossWeights,
    sampler: LHSCollocationSampler,
    n_coll: int,
    coll_seed: int,
    device: torch.device,
    phase: int,
) -> dict[str, float]:
    """Compute validation metrics (loss + ΔT_ONB RMSE in K)."""
    model.eval()
    total_mse_dT = 0.0
    n_samples = 0
    total_val_loss = 0.0

    with torch.no_grad():
        for batch in val_loader:
            B = batch["delta_T_wall_star"].shape[0]

            surface_batch = {
                "numeric":     batch["surface_numeric"].to(device),
                "category_id": batch["category_id"].to(device),
            }
            # Replicate surface latent for B samples at a single z* query
            z_query = torch.zeros(B, 1, device=device)
            # operating = (q_star, delta_T_sub_star) — experimental controls.
            q_star_b  = batch["q_flux_star"].unsqueeze(-1).to(device)
            dTs_star_b = batch["delta_T_sub_star"].unsqueeze(-1).to(device)
            operating_b = torch.cat([q_star_b, dTs_star_b], dim=-1)
            out = model(z_query, surface_batch, operating_b)

            # Un-normalise predictions for RMSE
            fluids    = batch["fluid"]
            pressures = batch["pressure_pa"]
            scales_lookup: dict[str, NondimScales] = {}
            delta_T_refs = []
            for f, P in zip(fluids, pressures):
                if f not in scales_lookup:
                    sc = scales_for(f, P=float(P))
                    scales_lookup[f] = sc
                delta_T_refs.append(scales_lookup[f].delta_T_ref)

            dT_ref_t = torch.tensor(delta_T_refs, device=device).unsqueeze(-1)
            pred_dT = out.delta_T_onb_star * dT_ref_t  # [K]

            target_dT_star = batch["delta_T_wall_star"].unsqueeze(-1).to(device)
            target_q_star  = batch["q_flux_star"].unsqueeze(-1).to(device)

            # Data loss only for val metric
            se = (out.delta_T_onb_star - target_dT_star) ** 2
            total_mse_dT  += float(se.sum().item())
            n_samples     += B

            # Approximate total loss (PDE losses need autograd, skip here)
            ld_dT = float((se).mean().item())
            total_val_loss += ld_dT * B

    rmse_star = math.sqrt(total_mse_dT / max(n_samples, 1))
    # Convert to K using water at 1 atm as representative scale
    try:
        sc_w = scales_for("water", P=101_325.0)
        rmse_K = rmse_star * sc_w.delta_T_ref
    except Exception:
        rmse_K = float("nan")

    model.train()
    return {
        "val/mse_dT_star": total_mse_dT / max(n_samples, 1),
        "val/rmse_dT_K":   rmse_K,
        "val/loss_approx": total_val_loss / max(n_samples, 1),
    }


# ===========================================================================
# Phase 1 — Analytical warm-up (PDE + BC, no data)
# ===========================================================================

def _run_phase1(
    model: PoolBoilingPINN,
    config: dict[str, Any],
    val_loader: DataLoader,
    sampler: LHSCollocationSampler,
    device: torch.device,
    checkpoint_dir: Path,
    run_name: str,
    mlflow_run: Any | None,
) -> dict[str, Any]:
    """Phase 1: PDE-only warm-up.

    Enforces that w_data = 0 (warm-up definition); raises if violated.
    """
    ph1 = config.get("phase1", {})
    lw  = config.get("loss_weights", {})

    # --- Guard: w_data must be 0 in warm-up ---
    w_data = float(lw.get("w_data", 10.0))
    # Phase 1 always uses w_data = 0 regardless of config top-level
    w_pde  = float(lw.get("w_pde",  1.0))
    w_bc   = float(lw.get("w_bc",   1.0))
    w_onb  = 0.0  # not active in Phase 1

    epochs    = int(ph1.get("epochs", 500))
    lr        = float(ph1.get("lr", 1.0e-3))
    n_coll    = int(config.get("collocation", {}).get("n_points", 2000))
    resample  = int(config.get("collocation", {}).get("resample_every", 100))
    log_every = int(config.get("logging", {}).get("log_every", 50))

    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    weights   = LossWeights(w_conduction=w_pde, w_bc=w_bc, w_data=0.0, w_onb=0.0)

    # Reference surface: zero surface latent (base condition as per spec)
    z_surface_zero = torch.zeros(n_coll, model.latent_dim, device=device)

    best_val_loss   = float("inf")
    best_epoch      = 0
    best_ckpt_path  = checkpoint_dir / run_name / "phase1_best.pt"
    patience        = int(config.get("training", {}).get("phase1", {}).get(
                          "early_stop_patience", 200))
    epochs_no_improve = 0
    t_start = time.time()

    print(f"\n[Phase 1] epochs={epochs}  lr={lr}  n_coll={n_coll}  device={device}")
    print(f"[Phase 1] Loss weights: w_pde={w_pde}  w_bc={w_bc}  w_data=0.0  w_onb=0.0")

    model.train()
    for epoch in range(1, epochs + 1):
        # Resample collocation points periodically
        if (epoch - 1) % resample == 0:
            coll_seed = (epoch // resample) * 7919
            z_coll = sampler.sample_spatial(n_coll, seed=coll_seed).requires_grad_(True)
            z_coll = z_coll.to(device)
            z_low, z_high = sampler.boundary_points(n_points=min(256, n_coll))
            z_low  = z_low.requires_grad_(True).to(device)
            z_high = z_high.to(device)
            # Zero surface latent = "base condition" warm-up
            z_surf_coll = z_surface_zero[:n_coll]
            z_surf_bc   = torch.zeros(z_low.shape[0], model.latent_dim, device=device)
            q_applied_star = torch.full((z_low.shape[0], 1), 0.01, device=device)
            T_bulk_star    = torch.full((z_low.shape[0], 1), -0.05, device=device)

        optimizer.zero_grad()

        # PDE residual
        L_pde = loss_conduction(model, z_coll, z_surf_coll)

        # BC residuals
        L_bc_low, L_bc_high = loss_bc(
            model,
            z_boundary_low=z_low,
            z_boundary_high=z_high,
            z_surface_cached_low=z_surf_bc,
            z_surface_cached_high=z_surf_bc,
            q_flux_applied_star=q_applied_star,
            T_bulk_star=T_bulk_star,
        )

        # Zero data/onb tensors (not active)
        zero = torch.tensor(0.0, device=device)
        comps = LossComponents(
            L_conduction=L_pde,
            L_bc_low=L_bc_low,
            L_bc_high=L_bc_high,
            L_data_dT=zero,
            L_data_q=zero,
            L_onb=zero,
        )
        L_total = total_loss(comps, weights)

        # Guard: NaN/inf → restore checkpoint and abort
        if not torch.isfinite(L_total):
            print(f"[Phase 1] epoch {epoch}: NaN/inf loss detected — restoring last checkpoint.")
            if best_ckpt_path.is_file():
                _load_checkpoint(model, optimizer, best_ckpt_path, device)
            break

        L_total.backward()
        optimizer.step()

        # --- logging ---
        if epoch % log_every == 0 or epoch == epochs:
            vals = _validate(model, val_loader, weights, sampler, n_coll, epoch, device, phase=1)
            val_loss = vals["val/loss_approx"]

            ld = comps.detach_dict()
            print(
                f"[Phase 1] epoch {epoch:5d}/{epochs}  "
                f"total={L_total.item():.4e}  "
                f"pde={ld['L_conduction']:.3e}  "
                f"bc_low={ld['L_bc_low']:.3e}  bc_high={ld['L_bc_high']:.3e}  "
                f"val_loss={val_loss:.4e}"
            )

            if _MLFLOW_AVAILABLE and mlflow_run is not None:
                mlflow.log_metrics({
                    "loss/conduction": ld["L_conduction"],
                    "loss/bc_low":     ld["L_bc_low"],
                    "loss/bc_high":    ld["L_bc_high"],
                    "loss/data":       0.0,
                    "loss/onb":        0.0,
                    "loss/total":      float(L_total.item()),
                    **vals,
                }, step=epoch)

            # Early stopping & checkpoint
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                best_epoch    = epoch
                epochs_no_improve = 0
                _save_checkpoint(model, optimizer, epoch, best_val_loss, best_ckpt_path)
            else:
                epochs_no_improve += 1
                if epochs_no_improve >= patience:
                    print(f"[Phase 1] Early stopping at epoch {epoch} (patience={patience}).")
                    break

    elapsed = time.time() - t_start
    ld_final = comps.detach_dict()
    print(
        f"\n[학습 완료 — Phase 1]\n"
        f"시간: {_fmt_time(elapsed)}\n"
        f"최종 손실: total={L_total.item():.4e} "
        f"(conduction={ld_final['L_conduction']:.3e}, "
        f"bc={ld_final['L_bc_low']+ld_final['L_bc_high']:.3e}, "
        f"data=0.0, onb=0.0)\n"
        f"체크포인트: {best_ckpt_path}\n"
        f"다음 단계: Phase 2"
    )

    return {
        "final_loss": float(L_total.item()),
        "best_val_loss": best_val_loss,
        "best_epoch": best_epoch,
        "checkpoint": str(best_ckpt_path),
        "elapsed_s": elapsed,
    }


# ===========================================================================
# Phase 2 — Synthetic data (skeleton)
# ===========================================================================

def _run_phase2(
    model: PoolBoilingPINN,
    config: dict[str, Any],
    val_loader: DataLoader,
    sampler: LHSCollocationSampler,
    device: torch.device,
    checkpoint_dir: Path,
    run_name: str,
    mlflow_run: Any | None,
) -> dict[str, Any]:
    """Phase 2: Synthetic data learning.

    Skeleton — synthetic dataset loader is not yet implemented.
    This phase is reserved for 02_data/raw/synthetic/ data.
    """
    print(
        "\n[Phase 2] Synthetic data phase — skeleton only.\n"
        "  02_data/raw/synthetic/ data not yet available.\n"
        "  Skipping to Phase 3."
    )
    ckpt_path = checkpoint_dir / run_name / "phase2_best.pt"

    # Save current model state as the Phase 2 checkpoint so Phase 3 can load it
    ph1_ckpt = checkpoint_dir / run_name / "phase1_best.pt"
    if ph1_ckpt.is_file():
        import shutil
        shutil.copy(ph1_ckpt, ckpt_path)
        print(f"[Phase 2] Forwarded Phase 1 checkpoint → {ckpt_path}")
    else:
        # No prior checkpoint: save current model state
        _dummy_opt = torch.optim.Adam(model.parameters())
        _save_checkpoint(model, _dummy_opt, 0, float("inf"), ckpt_path)

    return {
        "final_loss": float("nan"),
        "best_val_loss": float("nan"),
        "best_epoch": 0,
        "checkpoint": str(ckpt_path),
        "skipped": True,
    }


# ===========================================================================
# Phase 3 — Experimental fine-tuning (Adam → L-BFGS)
# ===========================================================================

def _run_phase3(
    model: PoolBoilingPINN,
    config: dict[str, Any],
    train_loader: DataLoader,
    val_loader: DataLoader,
    sampler: LHSCollocationSampler,
    device: torch.device,
    checkpoint_dir: Path,
    run_name: str,
    mlflow_run: Any | None,
) -> dict[str, Any]:
    """Phase 3: Experimental data fine-tuning with L_ONB schedule."""
    ph3  = config.get("training", {}).get("phase3", {})
    lw   = config.get("loss_weights", {})

    # Loss weights
    w_pde  = float(lw.get("w_pde",  1.0))
    w_bc   = float(lw.get("w_bc",   1.0))
    w_data = float(lw.get("w_data", 10.0))
    w_onb  = float(lw.get("w_onb",  5.0))
    w_mono_ra = float(lw.get("w_mono_ra", 1.0))   # Ra↑→ΔT↓ synthetic sweep penalty
    w_mono_th = float(lw.get("w_mono_th", 1.0))   # θ↑→ΔT↓ synthetic sweep penalty

    adam_epochs  = int(ph3.get("adam_epochs",  2000))
    lbfgs_epochs = int(ph3.get("lbfgs_epochs", 1000))
    lr_adam      = float(ph3.get("lr_adam", 5.0e-4))
    patience     = int(ph3.get("early_stop_patience", 200))

    n_coll   = int(config.get("collocation", {}).get("n_points", 2000))
    resample = int(config.get("collocation", {}).get("resample_every", 100))
    log_every = int(config.get("logging", {}).get("log_every", 50))

    best_ckpt_path = checkpoint_dir / run_name / "phase3_best.pt"
    best_val_loss   = float("inf")
    best_epoch      = 0
    epochs_no_improve = 0

    # ---- w_onb linear schedule: start=0.1 → end=w_onb over adam_epochs ---
    w_onb_start = 0.1
    w_onb_end   = w_onb

    optimizer = torch.optim.Adam(model.parameters(), lr=lr_adam)

    # ---- helper: one training step ----------------------------------------
    def _step(batch: dict, epoch_global: int, z_coll: torch.Tensor,
              z_surf_coll: torch.Tensor, z_low: torch.Tensor, z_high: torch.Tensor,
              z_surf_bc: torch.Tensor, q_applied_star: torch.Tensor,
              T_bulk_star: torch.Tensor, w_onb_current: float) -> tuple[torch.Tensor, LossComponents]:

        surface_batch = {
            "numeric":     batch["surface_numeric"].to(device),
            "category_id": batch["category_id"].to(device),
        }
        B = batch["delta_T_wall_star"].shape[0]
        z_query = torch.zeros(B, 1, device=device)

        target_dT_star = batch["delta_T_wall_star"].unsqueeze(-1).to(device)
        target_q_star  = batch["q_flux_star"].unsqueeze(-1).to(device)
        target_dTs_star = batch["delta_T_sub_star"].unsqueeze(-1).to(device)

        # operating = (q_star, delta_T_sub_star) — experimental controls.
        # The model must learn delta_T_ONB as a function of (surface, q'', ΔT_sub).
        operating_data = torch.cat([target_q_star, target_dTs_star], dim=-1)
        out = model(z_query, surface_batch, operating_data)

        # Operating tensor for PDE/BC collocation: (q_star, -T_bulk_star).
        # -T_bulk_star ≈ ΔT_sub_star (since T_bulk = T_sat − ΔT_sub).
        op_pde = torch.cat(
            [torch.full((z_coll.shape[0], 1), float(q_applied_star.mean().item()), device=device),
             torch.full((z_coll.shape[0], 1), float((-T_bulk_star).mean().item()), device=device)],
            dim=-1,
        )
        op_bc = torch.cat([q_applied_star, -T_bulk_star], dim=-1)
        L_pde = loss_conduction(model, z_coll, z_surf_coll, operating=op_pde)
        L_bc_low, L_bc_high = loss_bc(
            model,
            z_boundary_low=z_low.requires_grad_(True),
            z_boundary_high=z_high,
            z_surface_cached_low=z_surf_bc,
            z_surface_cached_high=z_surf_bc,
            q_flux_applied_star=q_applied_star,
            T_bulk_star=T_bulk_star,
            operating_low=op_bc,
            operating_high=op_bc,
        )
        L_data_dT, L_data_q = loss_data(out, target_dT_star, target_q_star)

        # ONB loss
        fluids_batch    = batch["fluid"]
        pressures_batch = [float(p) for p in batch["pressure_pa"]]
        scales_lookup: dict[str, NondimScales] = {}
        for f, P in zip(fluids_batch, pressures_batch):
            if f not in scales_lookup:
                scales_lookup[f] = scales_for(f, P=P)

        L_onb_val = loss_onb_hsu(out, fluids_batch, pressures_batch, scales_lookup)

        # Monotonicity regularization (Phase B addition)
        L_mono_Ra = loss_monotonicity(model, "Ra", n_points=20, device=device)
        L_mono_th = loss_monotonicity(model, "theta", n_points=20, device=device)

        w_eff = LossWeights(
            w_conduction=w_pde,
            w_bc=w_bc,
            w_data=w_data,
            w_onb=w_onb_current,
        )
        comps = LossComponents(
            L_conduction=L_pde,
            L_bc_low=L_bc_low,
            L_bc_high=L_bc_high,
            L_data_dT=L_data_dT,
            L_data_q=L_data_q,
            L_onb=L_onb_val,
        )
        L_total = (
            total_loss(comps, w_eff)
            + w_mono_ra * L_mono_Ra
            + w_mono_th * L_mono_th
        )
        return L_total, comps

    # ---- Adam phase --------------------------------------------------------
    t_start = time.time()
    print(
        f"\n[Phase 3 — Adam] epochs={adam_epochs}  lr={lr_adam}  "
        f"n_coll={n_coll}  device={device}"
    )

    model.train()
    global_epoch = 0
    last_L_total = torch.tensor(0.0, device=device)
    last_comps: LossComponents | None = None

    for epoch in range(1, adam_epochs + 1):
        global_epoch = epoch

        # Resample collocation points
        if (epoch - 1) % resample == 0:
            coll_seed = epoch * 31337
            z_coll = sampler.sample_spatial(n_coll, seed=coll_seed).requires_grad_(True)
            z_coll = z_coll.to(device)
            z_low, z_high = sampler.boundary_points(n_points=min(256, n_coll))
            z_low  = z_low.to(device)
            z_high = z_high.to(device)
            # For BC, use a representative surface latent = encoder mean
            z_surf_coll = torch.zeros(n_coll, model.latent_dim, device=device)
            z_surf_bc   = torch.zeros(z_low.shape[0], model.latent_dim, device=device)
            q_applied_star = torch.full((z_low.shape[0], 1), 0.01, device=device)
            T_bulk_star    = torch.full((z_low.shape[0], 1), -0.05, device=device)

        # Linear ONB weight schedule
        frac = (epoch - 1) / max(adam_epochs - 1, 1)
        w_onb_current = w_onb_start + frac * (w_onb_end - w_onb_start)

        for batch in train_loader:
            optimizer.zero_grad()

            try:
                L_total, comps = _step(
                    batch, epoch, z_coll, z_surf_coll, z_low, z_high,
                    z_surf_bc, q_applied_star, T_bulk_star, w_onb_current,
                )
            except FloatingPointError as exc:
                print(f"[Phase 3] epoch {epoch}: {exc} — restoring last checkpoint.")
                if best_ckpt_path.is_file():
                    _load_checkpoint(model, optimizer, best_ckpt_path, device)
                break

            if not torch.isfinite(L_total):
                print(f"[Phase 3] epoch {epoch}: NaN/inf loss — restoring checkpoint.")
                if best_ckpt_path.is_file():
                    _load_checkpoint(model, optimizer, best_ckpt_path, device)
                break

            L_total.backward()
            # Gradient clipping for stability
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=10.0)
            optimizer.step()
            last_L_total = L_total.detach()
            last_comps   = comps

        # --- logging ---
        if epoch % log_every == 0 or epoch == adam_epochs:
            vals = _validate(model, val_loader, LossWeights(), sampler, n_coll, epoch, device, phase=3)
            val_loss = vals["val/loss_approx"]

            if last_comps is not None:
                ld = last_comps.detach_dict()
                print(
                    f"[Phase 3-Adam] epoch {epoch:5d}/{adam_epochs}  "
                    f"total={last_L_total.item():.4e}  "
                    f"cond={ld['L_conduction']:.3e}  "
                    f"data_dT={ld['L_data_dT']:.3e}  "
                    f"onb={ld['L_onb']:.3e}  "
                    f"w_onb={w_onb_current:.3f}  "
                    f"val_RMSE_K={vals['val/rmse_dT_K']:.2f}"
                )

                if _MLFLOW_AVAILABLE and mlflow_run is not None:
                    mlflow.log_metrics({
                        "loss/conduction": ld["L_conduction"],
                        "loss/bc_low":     ld["L_bc_low"],
                        "loss/bc_high":    ld["L_bc_high"],
                        "loss/data":       ld["L_data_dT"] + ld["L_data_q"],
                        "loss/onb":        ld["L_onb"],
                        "loss/total":      float(last_L_total.item()),
                        "w_onb_current":   w_onb_current,
                        **vals,
                    }, step=epoch)

            if val_loss < best_val_loss:
                best_val_loss = val_loss
                best_epoch    = epoch
                epochs_no_improve = 0
                _save_checkpoint(model, optimizer, epoch, best_val_loss, best_ckpt_path)
            else:
                epochs_no_improve += 1
                if epochs_no_improve >= patience:
                    print(f"[Phase 3] Early stopping at epoch {epoch} (patience={patience}).")
                    break

    # ---- L-BFGS phase ------------------------------------------------------
    print(f"\n[Phase 3 — L-BFGS] max_iter={lbfgs_epochs}")

    # Freeze heads; fine-tune backbone only (recommended in spec)
    for param in model.head_T.parameters():
        param.requires_grad_(False)
    for param in model.head_dT_onb.parameters():
        param.requires_grad_(False)
    for param in model.head_q_onb.parameters():
        param.requires_grad_(False)

    lbfgs_optimizer = torch.optim.LBFGS(
        [p for p in model.parameters() if p.requires_grad],
        max_iter=lbfgs_epochs,
        history_size=50,
        line_search_fn="strong_wolfe",
    )

    # L-BFGS needs a closure; iterate over one full pass of training data
    try:
        _all_batches = list(train_loader)
    except Exception:
        _all_batches = []

    if _all_batches:
        # Refresh collocation points once for L-BFGS
        z_coll_lbfgs = sampler.sample_spatial(n_coll, seed=99999).requires_grad_(True).to(device)
        z_surf_coll_lbfgs = torch.zeros(n_coll, model.latent_dim, device=device)
        z_low_lbfgs, z_high_lbfgs = sampler.boundary_points(n_points=min(256, n_coll))
        z_low_lbfgs  = z_low_lbfgs.to(device)
        z_high_lbfgs = z_high_lbfgs.to(device)
        z_surf_bc_lbfgs  = torch.zeros(z_low_lbfgs.shape[0], model.latent_dim, device=device)
        q_app_lbfgs      = torch.full((z_low_lbfgs.shape[0], 1), 0.01, device=device)
        T_bulk_lbfgs     = torch.full((z_low_lbfgs.shape[0], 1), -0.05, device=device)

        _lbfgs_batch = _all_batches[0]

        def closure() -> torch.Tensor:
            lbfgs_optimizer.zero_grad()
            L_total_c, _ = _step(
                _lbfgs_batch, 0, z_coll_lbfgs, z_surf_coll_lbfgs,
                z_low_lbfgs, z_high_lbfgs, z_surf_bc_lbfgs,
                q_app_lbfgs, T_bulk_lbfgs, w_onb_end,
            )
            if torch.isfinite(L_total_c):
                L_total_c.backward()
            return L_total_c

        model.train()
        try:
            lbfgs_optimizer.step(closure)
            print("[Phase 3 — L-BFGS] step completed.")
        except Exception as exc:
            print(f"[Phase 3 — L-BFGS] WARNING: {exc}")

    # Re-enable all heads
    for param in model.parameters():
        param.requires_grad_(True)

    # Final validation
    vals_final = _validate(model, val_loader, LossWeights(), sampler, n_coll, 0, device, phase=3)
    val_loss_final = vals_final["val/loss_approx"]
    if val_loss_final < best_val_loss:
        _save_checkpoint(model, lbfgs_optimizer, global_epoch + lbfgs_epochs,
                         val_loss_final, best_ckpt_path)
        best_val_loss = val_loss_final

    elapsed = time.time() - t_start
    print(
        f"\n[학습 완료 — Phase 3]\n"
        f"시간: {_fmt_time(elapsed)}\n"
        f"검증 RMSE: ΔT_ONB {vals_final['val/rmse_dT_K']:.2f} K\n"
        f"체크포인트: {best_ckpt_path}\n"
        f"다음 단계: Phase 4"
    )

    return {
        "final_loss": float(last_L_total.item()) if last_comps else float("nan"),
        "best_val_loss": best_val_loss,
        "best_epoch": best_epoch,
        "checkpoint": str(best_ckpt_path),
        "val_rmse_K": vals_final["val/rmse_dT_K"],
        "elapsed_s": elapsed,
    }


# ===========================================================================
# Phase 4 — Inverse problem (skeleton)
# ===========================================================================

def _run_phase4(
    model: PoolBoilingPINN,
    config: dict[str, Any],
    val_loader: DataLoader,
    device: torch.device,
    checkpoint_dir: Path,
    run_name: str,
    mlflow_run: Any | None,
) -> dict[str, Any]:
    """Phase 4: Inverse problem — r_c estimation from ΔT_ONB.

    Skeleton implementation. The full inverse solver will:
    1. Set inverse_mode=True and add r_c as a learnable nn.Parameter.
    2. Fix backbone weights; optimise only r_c and head_dT_onb.
    3. Use L_onb (Hsu constraint) to recover the r_c distribution.

    Raises ValueError if inverse_mode is not set in config.
    """
    ph4 = config.get("phase4", {})
    if not ph4.get("inverse_mode", False):
        raise ValueError(
            "[Phase 4] inverse_mode must be True in config. "
            "Set phase4.inverse_mode: true  (Section 4.5 requirement)."
        )

    print(
        "\n[Phase 4] Inverse problem phase — skeleton only.\n"
        "  Full implementation deferred to inverse-solver sub-agent.\n"
        "  r_c recovery from experimental ΔT_ONB will be implemented there."
    )
    ckpt_path = checkpoint_dir / run_name / "phase4_best.pt"

    ph3_ckpt = checkpoint_dir / run_name / "phase3_best.pt"
    if ph3_ckpt.is_file():
        import shutil
        shutil.copy(ph3_ckpt, ckpt_path)
        print(f"[Phase 4] Forwarded Phase 3 checkpoint → {ckpt_path}")
    else:
        _dummy_opt = torch.optim.Adam(model.parameters())
        _save_checkpoint(model, _dummy_opt, 0, float("inf"), ckpt_path)

    return {
        "final_loss": float("nan"),
        "best_val_loss": float("nan"),
        "best_epoch": 0,
        "checkpoint": str(ckpt_path),
        "skipped": True,
        "note": "inverse solver skeleton — full implementation pending",
    }


# ===========================================================================
# run_phase — public single-phase entry point
# ===========================================================================

def run_phase(
    phase: int,
    model: nn.Module,
    config: dict[str, Any],
    train_loader: DataLoader,
    val_loader: DataLoader,
) -> dict[str, Any]:
    """Execute a single Phase.

    Parameters
    ----------
    phase : int  — 1, 2, 3, or 4
    model : PoolBoilingPINN
    config : dict loaded from YAML
    train_loader, val_loader : DataLoader

    Returns
    -------
    dict with keys: final_loss, best_epoch, checkpoint
    """
    if not isinstance(model, PoolBoilingPINN):
        raise TypeError(f"model must be PoolBoilingPINN, got {type(model)}")

    device   = next(model.parameters()).device
    ckpt_dir = Path(config.get("logging", {}).get("checkpoint_dir", "03_model/checkpoints"))
    run_name = str(config.get("run_name", "run"))
    sampler  = _build_sampler(config, device)

    if phase == 1:
        return _run_phase1(model, config, val_loader, sampler, device,
                           ckpt_dir, run_name, mlflow_run=None)
    elif phase == 2:
        return _run_phase2(model, config, val_loader, sampler, device,
                           ckpt_dir, run_name, mlflow_run=None)
    elif phase == 3:
        return _run_phase3(model, config, train_loader, val_loader, sampler,
                           device, ckpt_dir, run_name, mlflow_run=None)
    elif phase == 4:
        return _run_phase4(model, config, val_loader, device,
                           ckpt_dir, run_name, mlflow_run=None)
    else:
        raise ValueError(f"Unknown phase {phase}. Must be 1, 2, 3, or 4.")


# ===========================================================================
# run_training — orchestrator
# ===========================================================================

def run_training(
    config_path: Path,
    phase: int | str = "all",
    checkpoint_dir: Path = Path("03_model/checkpoints"),
    mlflow_uri: str = "03_model/experiments",
) -> dict[str, Any]:
    """Run the full or partial training pipeline.

    Parameters
    ----------
    config_path : Path  — path to YAML config
    phase       : int | "all"  — which phase(s) to run
    checkpoint_dir : Path  — base checkpoint directory
    mlflow_uri     : str   — MLflow tracking URI

    Returns
    -------
    dict mapping phase_N → result dict
    """
    config    = load_config(config_path)
    run_name  = str(config.get("run_name", config_path.stem))
    seed      = int(config.get("seed", 42))

    # Override checkpoint/mlflow from args if caller provided them
    if "logging" not in config:
        config["logging"] = {}
    config["logging"]["checkpoint_dir"] = str(checkpoint_dir)
    config["logging"]["mlflow_uri"]     = mlflow_uri

    torch.manual_seed(seed)
    device = _device(config)

    # --- DataLoaders --------------------------------------------------------
    data_cfg  = config.get("data", {})
    csv_path  = Path(data_cfg.get("csv_path", "02_data/processed/onb_dataset.csv"))
    if not csv_path.is_absolute():
        # Walk up from config dir until we find a dir that contains the CSV
        cfg_resolved = Path(config_path).resolve()
        candidate = cfg_resolved.parent
        resolved = None
        for _ in range(5):
            if (candidate / csv_path).is_file():
                resolved = candidate / csv_path
                break
            candidate = candidate.parent
        csv_path = resolved if resolved is not None else cfg_resolved.parents[1] / csv_path

    split_cfg = data_cfg.get("train_val_test_split", [0.8, 0.1, 0.1])
    batch_size = int(data_cfg.get("batch_size", 16))
    skip_unsupported = bool(data_cfg.get("skip_unsupported_fluids", True))

    train_loader, val_loader, test_loader = build_dataloaders(
        csv_path,
        split=tuple(split_cfg),
        batch_size=batch_size,
        skip_unsupported_fluids=skip_unsupported,
        seed=seed,
    )
    print(
        f"[run_training] DataLoaders ready: "
        f"train={len(train_loader.dataset)} "  # type: ignore[union-attr]
        f"val={len(val_loader.dataset)} "      # type: ignore[union-attr]
        f"test={len(test_loader.dataset)}"     # type: ignore[union-attr]
    )

    # --- Model --------------------------------------------------------------
    model = build_model(config, device)
    print(f"[run_training] Model: {model.n_parameters:,} params  device={device}")

    # --- Determine phases to run -------------------------------------------
    if phase == "all":
        phases_to_run = [1, 2, 3, 4]
    elif isinstance(phase, int):
        phases_to_run = [phase]
    else:
        phases_to_run = [int(phase)]

    # --- MLflow setup -------------------------------------------------------
    mlflow_run = None
    if _MLFLOW_AVAILABLE:
        mlflow.set_tracking_uri(mlflow_uri)
        mlflow.set_experiment(run_name)
        mlflow_run = mlflow.start_run(run_name=run_name)
        mlflow.log_params({"config_path": str(config_path), "phases": str(phases_to_run)})
        try:
            arch_params = model.mlflow_log_architecture()
            mlflow.log_params(arch_params)
        except Exception:
            pass
        print(f"[run_training] MLflow run_id: {mlflow_run.info.run_id}")
        print(f"[run_training] MLflow URI: {mlflow_uri}")
    else:
        print(f"[run_training] MLflow not available — logging skipped.")

    sampler = _build_sampler(config, device)
    ckpt_base = checkpoint_dir

    results: dict[str, Any] = {}

    try:
        for ph in phases_to_run:
            print(f"\n{'='*70}\nStarting Phase {ph}\n{'='*70}")

            # Load preceding phase's checkpoint
            prev_ckpt = ckpt_base / run_name / f"phase{ph-1}_best.pt"
            if ph > 1 and prev_ckpt.is_file():
                print(f"[run_training] Loading Phase {ph-1} checkpoint: {prev_ckpt}")
                _load_checkpoint(model, None, prev_ckpt, device)

            if ph == 1:
                res = _run_phase1(model, config, val_loader, sampler, device,
                                  ckpt_base, run_name, mlflow_run)
            elif ph == 2:
                res = _run_phase2(model, config, val_loader, sampler, device,
                                  ckpt_base, run_name, mlflow_run)
            elif ph == 3:
                res = _run_phase3(model, config, train_loader, val_loader, sampler,
                                  device, ckpt_base, run_name, mlflow_run)
            elif ph == 4:
                res = _run_phase4(model, config, val_loader, device,
                                  ckpt_base, run_name, mlflow_run)
            else:
                raise ValueError(f"Unknown phase {ph}")

            results[f"phase{ph}"] = res

            if _MLFLOW_AVAILABLE and mlflow_run is not None:
                mlflow.log_metrics({
                    f"phase{ph}/best_val_loss": res.get("best_val_loss", float("nan")),
                    f"phase{ph}/best_epoch":    float(res.get("best_epoch", 0)),
                }, step=ph)

    finally:
        if _MLFLOW_AVAILABLE and mlflow_run is not None:
            try:
                mlflow.end_run()
            except Exception:
                pass

    return results


# ===========================================================================
# CLI
# ===========================================================================

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="PINN-ONB01 Phase 1-4 training pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.training.train --config configs/baseline_phaseA.yaml --phase all
  python -m src.training.train --config configs/baseline_phaseA.yaml --phase 3 \\
      --resume checkpoints/phase2_best.pt
""",
    )
    parser.add_argument("--config", type=Path, required=True,
                        help="Path to YAML config file")
    parser.add_argument("--phase", default="all",
                        help="Phase to run: 1, 2, 3, 4, or 'all'")
    parser.add_argument("--resume", type=Path, default=None,
                        help="Checkpoint to resume from")
    parser.add_argument("--checkpoint-dir", type=Path,
                        default=Path("03_model/checkpoints"),
                        help="Base checkpoint directory")
    parser.add_argument("--mlflow-uri", type=str,
                        default="03_model/experiments",
                        help="MLflow tracking URI")
    parser.add_argument("--dry-run", action="store_true",
                        help="Validate config and data, do not train")
    return parser.parse_args()


def _main() -> None:
    args = _parse_args()

    config = load_config(args.config)
    print(f"[CLI] config loaded: {args.config}")
    print(f"[CLI] run_name: {config.get('run_name', args.config.stem)}")

    # Parse phase
    phase: int | str
    if args.phase.lower() == "all":
        phase = "all"
    else:
        phase = int(args.phase)

    if args.dry_run:
        # Validate config and data loading only
        data_cfg = config.get("data", {})
        csv_path = Path(data_cfg.get("csv_path", "02_data/processed/onb_dataset.csv"))
        if not csv_path.is_absolute():
            # Resolve relative to project root (parent of 03_model/)
            cfg_resolved = args.config.resolve()
            # Walk up until we find a dir containing 02_data/ or reach root
            candidate = cfg_resolved.parent
            for _ in range(5):
                if (candidate / csv_path).is_file():
                    csv_path = candidate / csv_path
                    break
                candidate = candidate.parent
            else:
                # fallback: relative to config's parent's parent (03_model/..)
                csv_path = cfg_resolved.parents[1] / csv_path
        ds = OnbDataset(csv_path, skip_unsupported_fluids=True)
        print(f"[dry-run] Dataset OK: {len(ds)} samples after filtering.")
        device = _device(config)
        model = build_model(config, device)
        print(f"[dry-run] Model OK: {model.n_parameters:,} params.")
        print("[dry-run] Config validation PASSED — training not started.")
        return

    results = run_training(
        config_path=args.config,
        phase=phase,
        checkpoint_dir=args.checkpoint_dir,
        mlflow_uri=args.mlflow_uri,
    )

    if args.resume is not None:
        print(f"[CLI] Resume from {args.resume} is applied at phase init (see run_training).")

    print("\n[CLI] Training complete. Results:")
    for ph_key, res in results.items():
        print(f"  {ph_key}: best_val_loss={res.get('best_val_loss', 'n/a'):.4e}  "
              f"checkpoint={res.get('checkpoint', 'n/a')}")


if __name__ == "__main__":
    _main()
