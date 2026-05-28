"""
train.py — Phase 2 Flow Boiling ONB PINN training orchestrator.

3-stage curriculum (plan.md §4.4):
  Stage 1  Adam 2000 ep   surface encoder frozen    lr 1e-3 → 1e-5 cosine
  Stage 2  Adam 3000 ep   full fine-tune             lr 3e-4 → 1e-6 cosine
  Stage 3  L-BFGS 500     final polish               full-batch closure

Usage:
  cd phase2_flow_boiling
  python experiments/src/train.py \
      --config experiments/configs/phase2_baseline_v1.yaml
  python experiments/src/train.py \
      --config experiments/configs/phase2_baseline_v1.yaml \
      --checkpoint experiments/checkpoints/phase2_baseline_v1/best_model.pt \
      --eval-only
"""
from __future__ import annotations

import argparse
import math
import sys
import time
from pathlib import Path
from typing import Any

import torch
import torch.nn as nn
from torch import Tensor
from torch.utils.data import DataLoader

# ── Source root on sys.path ───────────────────────────────────────────────────
_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from data.dataset import FlowBoilingDataset, collate_fn
from loss.loss_functions import LossComponents, LossWeights, total_loss
from model.flow_boiling_pinn import FlowBoilingPINN
from utils.nondim_flow import FlowNondimScales, compute_flow_nondim

# Project root = phase2_flow_boiling/
_PROJ = Path(__file__).resolve().parents[2]


# ── Config ────────────────────────────────────────────────────────────────────

def load_config(path: str | Path) -> dict[str, Any]:
    try:
        import yaml
    except ImportError:
        raise RuntimeError("PyYAML required: pip install pyyaml")
    with open(path) as f:
        return yaml.safe_load(f)


# ── Model ─────────────────────────────────────────────────────────────────────

def build_model(cfg: dict, device: torch.device) -> FlowBoilingPINN:
    m = cfg["model"]
    model = FlowBoilingPINN(
        surface_latent_dim=m.get("surface_latent_dim", 16),
        flow_latent_dim=m.get("flow_latent_dim", 8),
        hidden_dim=m.get("hidden_dim", 96),
        n_layers=m.get("n_layers", 6),
        head_hidden=m.get("head_hidden", 48),
        flow_encoder_hidden=m.get("flow_encoder_hidden", 32),
        flow_encoder_dropout=m.get("flow_encoder_dropout", 0.1),
        seed=cfg.get("experiment", {}).get("seed", 42),
    ).to(device)

    # Phase 1 transfer weights
    p1_ckpt = cfg.get("transfer", {}).get("phase1_checkpoint")
    if p1_ckpt:
        p1_path = Path(p1_ckpt).expanduser()
        if not p1_path.is_absolute():
            p1_path = _PROJ / p1_ckpt
        if p1_path.is_file():
            model.load_phase1_weights(str(p1_path))
        else:
            print(f"  [WARN] Phase 1 checkpoint not found: {p1_ckpt}")

    # Stage 1: freeze surface encoder
    if m.get("freeze_surface_encoder", True):
        model.freeze_surface_encoder()
        print("  Surface encoder: frozen (Stage 1)")

    total_p = sum(p.numel() for p in model.parameters())
    train_p = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"  Parameters: {total_p:,} total, {train_p:,} trainable")
    return model


# ── Data ──────────────────────────────────────────────────────────────────────

def build_datasets(cfg: dict) -> tuple[FlowBoilingDataset, FlowBoilingDataset, FlowBoilingDataset]:
    csv = Path(cfg["data"]["csv_path"])
    if not csv.is_absolute():
        csv = _PROJ / csv
    kw = dict(
        csv_path=csv,
        train_frac=cfg["data"].get("train_frac", 0.70),
        val_frac=cfg["data"].get("val_frac", 0.15),
        seed=cfg.get("experiment", {}).get("seed", 42),
        exclude_onb_not_found=cfg["data"].get("exclude_onb_not_found", True),
    )
    return (
        FlowBoilingDataset(**kw, split="train"),
        FlowBoilingDataset(**kw, split="val"),
        FlowBoilingDataset(**kw, split="test"),
    )


def build_loaders(
    cfg: dict,
    train_ds: FlowBoilingDataset,
    val_ds:   FlowBoilingDataset,
    test_ds:  FlowBoilingDataset,
) -> tuple[DataLoader, DataLoader, DataLoader]:
    bs = cfg["data"].get("batch_size", 32)
    return (
        DataLoader(train_ds, batch_size=bs, shuffle=True,  collate_fn=collate_fn),
        DataLoader(val_ds,   batch_size=bs, shuffle=False, collate_fn=collate_fn),
        DataLoader(test_ds,  batch_size=bs, shuffle=False, collate_fn=collate_fn),
    )


# ── Collocation helpers ───────────────────────────────────────────────────────

def make_hsu_collocation(
    n: int,
    train_ds: FlowBoilingDataset,
    sc: FlowNondimScales,
    device: torch.device,
) -> dict[str, Any]:
    """Build Hsu constraint collocation batch from training surface/flow conditions."""
    idx   = torch.randperm(len(train_ds))[:n].tolist()
    items = [train_ds[i] for i in idx]
    n     = len(items)   # actual count (may be < requested when train_ds is small)

    surf_num = torch.stack([it["surf_numeric"] for it in items]).to(device)
    surf_cat = torch.stack([it["surf_cat_id"]  for it in items]).to(device)
    flow_num = torch.stack([it["flow_numeric"]  for it in items]).to(device)

    # Recover Re and D_h from encoded channels (flow_encoder.py channel layout):
    #   ch0 = log10(Re)/5           → Re    = 10^(5·ch0)
    #   ch6 = log10(D_h_mm + 0.01)  → D_h   = 10^ch6 − 0.01  [mm]
    Re   = (10.0 ** (5.0 * flow_num[:, 0].clamp(-0.2, 1.2))).clamp(min=400.0)
    Dh_m = ((10.0 ** flow_num[:, 6].clamp(-2.0, 1.2)) - 0.01).clamp(min=0.05) * 1e-3

    Pr = sc.cp_l * sc.mu_l / sc.k_l
    Pr_t = torch.full((n,), Pr, device=device)

    dT_ref = max(sc.sigma * sc.T_sat_K / (sc.h_fg * sc.rho_l * sc.L_c), 0.1)
    q_ref  = sc.rho_l * sc.h_fg * math.sqrt(sc.sigma / (sc.rho_l * 9.81)) * 9.81

    return {
        "x_star":           torch.rand(n, 1, device=device),
        "surface_features": {"numeric": surf_num, "category_id": surf_cat},
        "flow_numeric":     flow_num,
        "Re":               Re,
        "Pr":               Pr_t,
        "D_h_m":            Dh_m,
        "dT_ref":           torch.tensor(dT_ref, device=device),
        "q_ref":            torch.tensor(q_ref,  device=device),
    }


def make_mono_base(
    train_ds: FlowBoilingDataset,
    device: torch.device,
) -> dict[str, Tensor]:
    """Single representative training point for monotonicity sweeps."""
    item = train_ds[0]
    return {
        "surf_numeric": item["surf_numeric"].to(device),
        "surf_cat_id":  item["surf_cat_id"].to(device),
        "flow_numeric": item["flow_numeric"].to(device),
    }


# ── Evaluation ────────────────────────────────────────────────────────────────

@torch.no_grad()
def evaluate(
    model:  FlowBoilingPINN,
    loader: DataLoader,
    device: torch.device,
) -> dict[str, float]:
    """RMSE(K), MAE(K), R² for ΔT_onb and q_onb in dimensional units."""
    model.eval()
    pred_dT, true_dT = [], []
    pred_q,  true_q  = [], []

    for batch in loader:
        x    = batch["x_star"].to(device)
        sf   = {k: v.to(device) for k, v in batch["surface_features"].items()}
        fn   = batch["flow_numeric"].to(device)
        out  = model(x, sf, fn)

        # Per-sample nondim → dimensional conversion
        dT_ref = batch["dT_ref"].to(device)   # (B,)
        q_ref  = batch["q_ref"].to(device)    # (B,)
        p_dT   = out.delta_T_onb_star.squeeze(-1) * dT_ref
        p_q    = out.q_onb_star.squeeze(-1)   * q_ref

        t_dT  = batch["delta_T_onb_K"].to(device)
        t_q   = batch["q_onb_W_m2"].to(device)
        hq    = batch["has_q"].to(device)
        hdT   = batch["has_dT"].to(device)

        if hdT.any():
            msk = hdT & torch.isfinite(t_dT)
            pred_dT.append(p_dT[msk])
            true_dT.append(t_dT[msk])
        if hq.any():
            msk = hq & torch.isfinite(t_q)
            pred_q.append(p_q[msk])
            true_q.append(t_q[msk])

    def _m(p_list: list[Tensor], t_list: list[Tensor], suffix: str) -> dict[str, float]:
        if not p_list:
            return {}
        p = torch.cat(p_list)
        t = torch.cat(t_list)
        e = p - t
        rmse = float(e.pow(2).mean().sqrt())
        mae  = float(e.abs().mean())
        r2   = 1.0 - float(e.pow(2).sum()) / (float((t - t.mean()).pow(2).sum()) + 1e-10)
        return {f"rmse_{suffix}": rmse, f"mae_{suffix}": mae,
                f"r2_{suffix}":   r2,   f"n_{suffix}":   len(p)}

    out_m: dict[str, float] = {}
    out_m.update(_m(pred_dT, true_dT, "dT_K"))
    out_m.update(_m(pred_q,  true_q,  "q_Wm2"))
    return out_m


# ── Loss helper (moves batch to device) ──────────────────────────────────────

def _compute_loss(
    model:     FlowBoilingPINN,
    batch:     dict,
    weights:   LossWeights,
    sc:        FlowNondimScales,
    hsu_coll:  dict | None,
    mono_base: dict | None,
    cfg:       dict,
    device:    torch.device,
) -> LossComponents:
    def _to(v: Any) -> Any:
        if isinstance(v, Tensor):
            return v.to(device)
        if isinstance(v, dict):
            return {kk: vv.to(device) if isinstance(vv, Tensor) else vv
                    for kk, vv in v.items()}
        return v

    batch_d = {k: _to(v) for k, v in batch.items()}
    return total_loss(
        model, batch_d, weights, sc,
        collocation_hsu=hsu_coll,
        collocation_mono=mono_base,
        C_hsu=cfg.get("hsu_constraint", {}).get("C_hsu", 0.5),
        n_mono_points=cfg.get("collocation", {}).get("n_mono_points", 20),
    )


# ── MLflow thin wrapper ───────────────────────────────────────────────────────

class _Logger:
    def __init__(self, cfg: dict) -> None:
        uri  = cfg.get("logging", {}).get("mlflow_tracking_uri", "experiments/logs/mlruns")
        name = cfg.get("experiment", {}).get("name", "phase2")
        if not Path(uri).is_absolute():
            uri = str(_PROJ / uri)
        try:
            import mlflow
            mlflow.set_tracking_uri(uri)
            mlflow.set_experiment(name)
            self._run    = mlflow.start_run()
            self._mlflow = mlflow
            self._ok     = True
            print(f"  MLflow run_id: {self._run.info.run_id[:8]}")
        except Exception as e:
            print(f"  [MLflow] disabled ({e})")
            self._ok = False

    def params(self, d: dict) -> None:
        if self._ok:
            try:
                self._mlflow.log_params({str(k): v for k, v in d.items()})
            except Exception:
                pass

    def metrics(self, d: dict[str, float], step: int) -> None:
        if self._ok:
            try:
                self._mlflow.log_metrics(d, step=step)
            except Exception:
                pass

    def finish(self) -> None:
        if self._ok:
            try:
                self._mlflow.end_run()
            except Exception:
                pass


# ── Stage 1 / 2 — Adam ───────────────────────────────────────────────────────

def run_adam_stage(
    stage_name:   str,
    model:        FlowBoilingPINN,
    train_loader: DataLoader,
    val_loader:   DataLoader,
    train_ds:     FlowBoilingDataset,
    weights:      LossWeights,
    sc:           FlowNondimScales,
    stage_cfg:    dict,
    cfg:          dict,
    device:       torch.device,
    ckpt_dir:     Path,
    logger:       _Logger,
    global_step:  int = 0,
) -> tuple[float, int]:
    """Train one Adam stage. Returns (best_val_loss, final_global_step)."""
    epochs    = stage_cfg["epochs"]
    lr        = stage_cfg.get("lr", 1e-3)
    lr_min    = stage_cfg.get("lr_min", 1e-5)
    grad_clip = stage_cfg.get("grad_clip", 1.0)
    log_every = cfg.get("logging", {}).get("log_every_n_epochs", 50)
    save_best = cfg.get("logging", {}).get("save_best", True)
    n_hsu     = cfg.get("collocation", {}).get("n_hsu_points", 500)

    optimizer = torch.optim.Adam(
        filter(lambda p: p.requires_grad, model.parameters()), lr=lr
    )
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=epochs, eta_min=lr_min
    )

    best_val = float("inf")
    t0       = time.time()

    print(f"\n{'='*60}")
    print(f"  {stage_name.upper()}  |  {epochs} epochs  |  lr {lr:.1e} → {lr_min:.1e}")
    print(f"{'='*60}")

    for ep in range(1, epochs + 1):
        model.train()
        # Refresh collocation each epoch for diversity
        hsu_coll  = make_hsu_collocation(n_hsu, train_ds, sc, device)
        mono_base = make_mono_base(train_ds, device)

        train_sum, n_b, n_skipped = 0.0, 0, 0
        for batch in train_loader:
            optimizer.zero_grad()
            lc = _compute_loss(model, batch, weights, sc,
                               hsu_coll, mono_base, cfg, device)
            # Skip batch if loss is non-finite — don't backprop NaN into weights
            if not torch.isfinite(lc.total):
                n_skipped += 1
                continue
            lc.total.backward()
            # Zero NaN gradients (MPS LayerNorm backward can produce NaN for
            # large coupling-loss gradients; zeroing is safer than corrupting weights)
            for p in model.parameters():
                if p.requires_grad and p.grad is not None and p.grad.isnan().any():
                    p.grad[p.grad.isnan()] = 0.0
            if grad_clip > 0:
                nn.utils.clip_grad_norm_(
                    [p for p in model.parameters() if p.requires_grad], grad_clip
                )
            optimizer.step()
            train_sum += lc.total.item()
            n_b += 1
        if n_skipped:
            import warnings
            warnings.warn(f"[{stage_name}] ep {ep}: skipped {n_skipped} NaN batches")

        scheduler.step()
        global_step += 1
        avg_train = train_sum / max(n_b, 1)

        if ep % log_every == 0 or ep == 1 or ep == epochs:
            model.eval()
            val_sum, val_n = 0.0, 0
            with torch.no_grad():
                for vb in val_loader:
                    vlc = _compute_loss(model, vb, weights, sc,
                                        None, None, cfg, device)
                    val_sum += vlc.total.item()
                    val_n   += 1
            avg_val = val_sum / max(val_n, 1)

            lr_now = scheduler.get_last_lr()[0]
            elapsed = time.time() - t0
            print(
                f"  [{stage_name}] ep {ep:>5d}/{epochs}"
                f"  train {avg_train:.4f}  val {avg_val:.4f}"
                f"  lr {lr_now:.2e}  {elapsed:.0f}s"
            )
            logger.metrics(
                {f"{stage_name}/train_loss": avg_train,
                 f"{stage_name}/val_loss":   avg_val,
                 f"{stage_name}/lr":         lr_now},
                step=global_step,
            )

            if save_best and avg_val < best_val:
                best_val = avg_val
                torch.save(
                    {"epoch": ep, "stage": stage_name,
                     "model_state": model.state_dict(),
                     "val_loss": avg_val},
                    ckpt_dir / "best_model.pt",
                )

    return best_val, global_step


# ── Stage 3 — L-BFGS ─────────────────────────────────────────────────────────

def run_lbfgs_stage(
    model:        FlowBoilingPINN,
    train_loader: DataLoader,
    train_ds:     FlowBoilingDataset,
    weights:      LossWeights,
    sc:           FlowNondimScales,
    stage_cfg:    dict,
    cfg:          dict,
    device:       torch.device,
    ckpt_dir:     Path,
    logger:       _Logger,
    global_step:  int = 0,
) -> int:
    """Full-batch L-BFGS fine-tune."""
    max_iter   = stage_cfg.get("max_iter", 500)
    tol_grad   = stage_cfg.get("tolerance_grad", 1e-7)
    tol_change = stage_cfg.get("tolerance_change", 1e-9)
    history    = stage_cfg.get("history_size", 50)
    n_hsu      = cfg.get("collocation", {}).get("n_hsu_points", 500)

    print(f"\n{'='*60}")
    print(f"  STAGE3 L-BFGS  |  max_iter={max_iter}")
    print(f"{'='*60}")

    # Merge all training batches into one full-dataset batch
    all_items: list[dict] = []
    for b in train_loader:
        bs = b["x_star"].shape[0]
        for i in range(bs):
            all_items.append({
                "x_star":           b["x_star"][i],
                "surf_numeric":     b["surface_features"]["numeric"][i],
                "surf_cat_id":      b["surface_features"]["category_id"][i],
                "flow_numeric":     b["flow_numeric"][i],
                "q_onb_W_m2":       b["q_onb_W_m2"][i],
                "delta_T_onb_K":    b["delta_T_onb_K"][i],
                "q_onb_star":       b["q_onb_star"][i],
                "delta_T_onb_star": b["delta_T_onb_star"][i],
                "has_q":            b["has_q"][i],
                "has_dT":           b["has_dT"][i],
                "dT_ref":           b["dT_ref"][i],
                "q_ref":            b["q_ref"][i],
            })
    full_batch = collate_fn(all_items)
    hsu_coll   = make_hsu_collocation(n_hsu, train_ds, sc, device)
    mono_base  = make_mono_base(train_ds, device)

    optimizer = torch.optim.LBFGS(
        [p for p in model.parameters() if p.requires_grad],
        max_iter=max_iter,
        tolerance_grad=tol_grad,
        tolerance_change=tol_change,
        history_size=history,
        line_search_fn="strong_wolfe",
    )

    loss_log: list[float] = []

    def closure() -> Tensor:
        optimizer.zero_grad()
        lc = _compute_loss(model, full_batch, weights, sc,
                           hsu_coll, mono_base, cfg, device)
        lc.total.backward()
        for p in model.parameters():
            if p.requires_grad and p.grad is not None and p.grad.isnan().any():
                p.grad[p.grad.isnan()] = 0.0
        loss_log.append(lc.total.item())
        return lc.total

    model.train()
    t0 = time.time()
    optimizer.step(closure)

    final_loss = loss_log[-1] if loss_log else float("nan")
    print(
        f"  [stage3] final loss={final_loss:.6f}"
        f"  func_evals={len(loss_log)}  t={time.time()-t0:.0f}s"
    )

    torch.save(
        {"stage": "stage3", "model_state": model.state_dict(),
         "final_loss": final_loss},
        ckpt_dir / "final_model.pt",
    )
    logger.metrics({"stage3/final_loss": final_loss}, step=global_step + 1)
    return global_step + 1


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 2 Flow Boiling PINN trainer")
    parser.add_argument("--config",     required=True,       help="YAML config path")
    parser.add_argument("--checkpoint", default=None,        help="Resume checkpoint")
    parser.add_argument("--eval-only",  action="store_true", help="Skip training, evaluate only")
    parser.add_argument("--skip-lbfgs", action="store_true", help="Skip Stage 3")
    parser.add_argument("--device",     default="auto",
                        help="cpu | cuda | mps | auto (default: auto)")
    args = parser.parse_args()

    # ── Device ────────────────────────────────────────────────────────────────
    if args.device == "auto":
        if torch.backends.mps.is_available():
            device = torch.device("mps")
        elif torch.cuda.is_available():
            device = torch.device("cuda")
        else:
            device = torch.device("cpu")
    else:
        device = torch.device(args.device)
    print(f"\nDevice : {device}")

    # ── Config ────────────────────────────────────────────────────────────────
    cfg  = load_config(args.config)
    seed = cfg.get("experiment", {}).get("seed", 42)
    torch.manual_seed(seed)
    print(f"Config : {args.config}  seed={seed}")

    # ── Checkpoint dir ────────────────────────────────────────────────────────
    ckpt_base = Path(cfg.get("logging", {}).get("checkpoint_dir", "experiments/checkpoints"))
    if not ckpt_base.is_absolute():
        ckpt_base = _PROJ / ckpt_base
    run_name = cfg.get("experiment", {}).get("name", "run")
    ckpt_dir = ckpt_base / run_name
    ckpt_dir.mkdir(parents=True, exist_ok=True)

    # ── Data ──────────────────────────────────────────────────────────────────
    print("\nLoading data...")
    train_ds, val_ds, test_ds = build_datasets(cfg)
    train_loader, val_loader, test_loader = build_loaders(cfg, train_ds, val_ds, test_ds)
    print(
        f"  train={len(train_ds)} (q={train_ds.n_with_q}, dT={train_ds.n_with_dT})"
        f"  val={len(val_ds)}  test={len(test_ds)}"
    )

    # Representative fluid for collocation (water at 1 atm)
    sc = compute_flow_nondim("water", 101.325)

    # ── Model ─────────────────────────────────────────────────────────────────
    print("\nBuilding model...")
    model = build_model(cfg, device)

    if args.checkpoint:
        ckpt_path = Path(args.checkpoint)
        if not ckpt_path.is_absolute():
            ckpt_path = _PROJ / ckpt_path
        ckpt_data = torch.load(ckpt_path, map_location=device, weights_only=True)
        model.load_state_dict(ckpt_data["model_state"])
        print(f"  Resumed: {ckpt_path.name}  (val={ckpt_data.get('val_loss', '?'):.4f})")

    # ── Eval-only mode ────────────────────────────────────────────────────────
    if args.eval_only:
        print("\n[eval-only]")
        vm = evaluate(model, val_loader,  device)
        tm = evaluate(model, test_loader, device)
        _print_metrics("Val",  vm)
        _print_metrics("Test", tm)
        _print_go_nogo(vm)
        return

    # ── Weights & MLflow ──────────────────────────────────────────────────────
    weights = LossWeights.from_config(cfg)
    logger  = _Logger(cfg)
    logger.params({
        "n_train": len(train_ds), "n_val": len(val_ds),
        "hidden_dim": cfg["model"].get("hidden_dim"),
        "n_layers":   cfg["model"].get("n_layers"),
        "flow_latent_dim": cfg["model"].get("flow_latent_dim"),
        "w_hsu":     weights.w_hsu,
        "w_mono_Re": weights.w_mono_Re,
    })

    global_step = 0

    # ── Stage 1 (surface encoder frozen) ─────────────────────────────────────
    best_s1, global_step = run_adam_stage(
        "stage1", model, train_loader, val_loader, train_ds,
        weights, sc, cfg["training"]["stage1"], cfg,
        device, ckpt_dir, logger, global_step,
    )
    print(f"\n  Stage 1 best val loss: {best_s1:.6f}")

    # ── Stage 2 (full fine-tune) ──────────────────────────────────────────────
    model.unfreeze_surface_encoder()
    print("\n  Surface encoder: unfrozen (Stage 2)")

    best_s2, global_step = run_adam_stage(
        "stage2", model, train_loader, val_loader, train_ds,
        weights, sc, cfg["training"]["stage2"], cfg,
        device, ckpt_dir, logger, global_step,
    )
    print(f"\n  Stage 2 best val loss: {best_s2:.6f}")

    # Reload best checkpoint before Stage 3
    best_ckpt = ckpt_dir / "best_model.pt"
    if best_ckpt.exists():
        bd = torch.load(best_ckpt, map_location=device, weights_only=True)
        model.load_state_dict(bd["model_state"])
        print(f"  Reloaded best checkpoint (val={bd['val_loss']:.6f})")

    # ── Stage 3 (L-BFGS) ──────────────────────────────────────────────────────
    if not args.skip_lbfgs:
        global_step = run_lbfgs_stage(
            model, train_loader, train_ds,
            weights, sc, cfg["training"]["stage3"], cfg,
            device, ckpt_dir, logger, global_step,
        )
    else:
        print("\n  [skip-lbfgs] Stage 3 skipped.")

    # ── Final evaluation ──────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("  FINAL EVALUATION")
    print(f"{'='*60}")

    val_m  = evaluate(model, val_loader,  device)
    test_m = evaluate(model, test_loader, device)
    _print_metrics("Val",  val_m)
    _print_metrics("Test", test_m)
    _print_go_nogo(val_m)

    logger.metrics(
        {"final/val_rmse_dT_K":  val_m.get("rmse_dT_K",  float("nan")),
         "final/val_r2_dT":      val_m.get("r2_dT_K",    float("nan")),
         "final/test_rmse_dT_K": test_m.get("rmse_dT_K", float("nan")),
         "final/val_rmse_q":     val_m.get("rmse_q_Wm2", float("nan"))},
        step=global_step,
    )
    logger.finish()
    print(f"\n  Checkpoints: {ckpt_dir}")


# ── Reporting helpers ─────────────────────────────────────────────────────────

def _print_metrics(label: str, m: dict[str, float]) -> None:
    print(f"\n{label}:")
    for k, v in m.items():
        print(f"  {k:<22s}: {v:.4g}")


def _print_go_nogo(val_m: dict[str, float]) -> None:
    rmse = val_m.get("rmse_dT_K", float("nan"))
    status = "GO ✓" if rmse <= 8.0 else "NO-GO ✗  (target ≤ 8 K)"
    print(f"\n  M4 Go/No-Go  val RMSE_ΔT = {rmse:.2f} K  →  {status}")


if __name__ == "__main__":
    main()
