"""
hpo.py — Optuna 베이지안 하이퍼파라미터 탐색 엔진 (PINN-ONB01 Phase 3).

탐색 공간
---------
loss weights : w_pde, w_bc, w_data, w_onb  (LogUniform)
optimizer    : lr_adam                        (LogUniform)
architecture : hidden_dim, latent_dim, n_layers, conditioning

탐색 전략
---------
- Sampler : TPESampler (seed=42)
- Pruner  : MedianPruner (n_startup_trials=5, n_warmup_steps=500)
- Storage : SQLite  (03_model/experiments/hpo_results/study.db)

단축 학습 스케줄 (per trial)
---------------------------
Phase 1 : epochs=300  (warm-up PDE+BC)
Phase 3 : adam_epochs=1500, lbfgs_epochs=500

Authors: PINN-ONB01 project
Date   : 2026-05-13
"""

from __future__ import annotations

import argparse
import copy
import math
import shutil
import sys
import time
import traceback
from pathlib import Path
from typing import Any

import torch
import yaml

# ---------------------------------------------------------------------------
# Optional imports
# ---------------------------------------------------------------------------
try:
    import optuna
    from optuna.samplers import TPESampler
    from optuna.pruners import MedianPruner
    _OPTUNA_AVAILABLE = True
except ImportError:
    _OPTUNA_AVAILABLE = False

try:
    import mlflow  # type: ignore[import]
    _MLFLOW_AVAILABLE = True
except ImportError:
    _MLFLOW_AVAILABLE = False

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    _MPL_AVAILABLE = True
except ImportError:
    _MPL_AVAILABLE = False

# ---------------------------------------------------------------------------
# Project root (03_model parent)
# ---------------------------------------------------------------------------
_THIS_FILE = Path(__file__).resolve()
_PROJECT_ROOT = _THIS_FILE.parents[3]   # PINN-ONB01/
_MODEL_ROOT   = _THIS_FILE.parents[2]   # PINN-ONB01/03_model/

# ---------------------------------------------------------------------------
# Inline imports from training pipeline
# ---------------------------------------------------------------------------
# These must be imported AFTER sys.path adjustments (handled by caller or __main__)
def _import_training_modules():
    from ..train import (
        load_config,
        build_model,
        _build_sampler,
        _run_phase1,
        _run_phase3,
        _validate,
        _load_checkpoint,
    )
    from ...training.dataset import build_dataloaders
    return (
        load_config, build_model, _build_sampler,
        _run_phase1, _run_phase3, _validate, _load_checkpoint,
        build_dataloaders,
    )


# ---------------------------------------------------------------------------
# Config patch helper
# ---------------------------------------------------------------------------

def _patch_config(base_cfg: dict[str, Any], trial_params: dict[str, Any]) -> dict[str, Any]:
    """Apply trial_params onto a deep copy of base_cfg."""
    cfg = copy.deepcopy(base_cfg)

    # Loss weights
    if "w_pde" in trial_params:
        cfg.setdefault("loss_weights", {})["w_pde"]  = trial_params["w_pde"]
    if "w_bc" in trial_params:
        cfg.setdefault("loss_weights", {})["w_bc"]   = trial_params["w_bc"]
    if "w_data" in trial_params:
        cfg.setdefault("loss_weights", {})["w_data"] = trial_params["w_data"]
    if "w_onb" in trial_params:
        cfg.setdefault("loss_weights", {})["w_onb"]  = trial_params["w_onb"]

    # Optimizer
    if "lr_adam" in trial_params:
        cfg.setdefault("training", {}).setdefault("phase3", {})["lr_adam"] = trial_params["lr_adam"]

    # Architecture — must keep latent_dim consistent across encoder & pinn
    if "hidden_dim" in trial_params:
        cfg.setdefault("model", {}).setdefault("pinn", {})["hidden_dim"] = trial_params["hidden_dim"]
    if "latent_dim" in trial_params:
        ld = trial_params["latent_dim"]
        cfg.setdefault("model", {}).setdefault("surface_encoder", {})["latent_dim"] = ld
        # pinn section must match
        cfg["model"].setdefault("pinn", {})["latent_dim"] = ld
    if "n_layers" in trial_params:
        cfg.setdefault("model", {}).setdefault("pinn", {})["n_layers"] = trial_params["n_layers"]
    if "conditioning" in trial_params:
        cfg.setdefault("model", {})["conditioning"] = trial_params["conditioning"]

    # HPO short-training schedule (override full epochs).
    # phaseC dataset is ~12x larger than phaseA; cut epochs accordingly.
    cfg.setdefault("training", {}).setdefault("phase1", {})["epochs"]       = 200
    cfg.setdefault("training", {}).setdefault("phase3", {})["adam_epochs"]  = 800
    cfg.setdefault("training", {}).setdefault("phase3", {})["lbfgs_epochs"] = 200
    # Disable early stopping during HPO (let short schedule run to completion)
    cfg["training"]["phase1"]["early_stop_patience"] = 999
    cfg["training"]["phase3"]["early_stop_patience"] = 999

    return cfg


# ---------------------------------------------------------------------------
# Objective function
# ---------------------------------------------------------------------------

def objective(trial: "optuna.Trial", base_config: dict[str, Any]) -> float:
    """Single HPO trial.

    Builds a fresh model, runs Phase 1 (warm-up) + Phase 3 (fine-tuning),
    then returns val RMSE [K] as the minimisation target.

    GPU OOM and NaN/inf losses are caught → trial pruned with score = inf.
    """
    # Use absolute imports via sys.path (PYTHONPATH=03_model is set by caller)
    from src.training.train import (
        build_model,
        _build_sampler,
        _run_phase1,
        _run_phase3,
        _load_checkpoint,
    )
    from src.training.dataset import build_dataloaders

    # ---- Suggest hyperparameters ------------------------------------------
    params: dict[str, Any] = {
        "w_pde":        trial.suggest_float("w_pde",    0.1,   10.0, log=True),
        "w_bc":         trial.suggest_float("w_bc",     0.1,   10.0, log=True),
        "w_data":       trial.suggest_float("w_data",   1.0,  100.0, log=True),
        "w_onb":        trial.suggest_float("w_onb",    0.1,   50.0, log=True),
        "lr_adam":      trial.suggest_float("lr_adam",  1e-4,   5e-3, log=True),
        "hidden_dim":   trial.suggest_categorical("hidden_dim",  [32, 64, 128]),
        "latent_dim":   trial.suggest_categorical("latent_dim",  [8, 16, 32]),
        "n_layers":     trial.suggest_categorical("n_layers",    [3, 5, 7]),
        "conditioning": trial.suggest_categorical("conditioning", ["concat", "film"]),
    }

    cfg = _patch_config(base_config, params)
    run_name_trial = f"hpo_trial_{trial.number:04d}"
    cfg["run_name"] = run_name_trial

    # Use a fixed seed per trial to reduce variance
    trial_seed = 42
    cfg["seed"] = trial_seed
    torch.manual_seed(trial_seed)

    device = torch.device("cpu")  # M1 CPU — n_jobs=1 serial
    cfg["device"] = "cpu"

    # Silence per-epoch prints during HPO
    import io, contextlib

    # ---- Resolve data path -------------------------------------------------
    data_cfg  = cfg.get("data", {})
    csv_path  = Path(data_cfg.get("csv_path", "02_data/processed/onb_dataset.csv"))
    if not csv_path.is_absolute():
        # Walk up from project root
        candidate = _PROJECT_ROOT
        for _ in range(3):
            if (candidate / csv_path).is_file():
                csv_path = candidate / csv_path
                break
            candidate = candidate.parent

    split_cfg  = data_cfg.get("train_val_test_split", [0.8, 0.1, 0.1])
    batch_size = int(data_cfg.get("batch_size", 16))

    try:
        train_loader, val_loader, test_loader = build_dataloaders(
            csv_path,
            split=tuple(split_cfg),
            batch_size=batch_size,
            skip_unsupported_fluids=True,
            seed=trial_seed,
        )
    except Exception as exc:
        print(f"[HPO Trial {trial.number}] DataLoader failed: {exc}")
        raise optuna.exceptions.TrialPruned()

    # ---- Build model -------------------------------------------------------
    try:
        model = build_model(cfg, device)
    except Exception as exc:
        print(f"[HPO Trial {trial.number}] build_model failed: {exc}")
        raise optuna.exceptions.TrialPruned()

    # ---- Checkpoint dir for this trial ------------------------------------
    ckpt_dir = _MODEL_ROOT / "checkpoints" / "hpo_trials"
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    cfg.setdefault("logging", {})["checkpoint_dir"] = str(ckpt_dir)
    cfg["logging"]["mlflow_uri"]                    = str(_MODEL_ROOT / "experiments")

    sampler = _build_sampler(cfg, device)

    # ---- Phase 1: PDE warm-up ---------------------------------------------
    t0 = time.time()
    try:
        _buf = io.StringIO()
        with contextlib.redirect_stdout(_buf):
            ph1_res = _run_phase1(
                model, cfg, val_loader, sampler, device,
                ckpt_dir, run_name_trial, mlflow_run=None,
            )
    except Exception as exc:
        print(f"[HPO Trial {trial.number}] Phase 1 failed: {exc}")
        raise optuna.exceptions.TrialPruned()

    # Intermediate report after Phase 1
    ph1_val_loss = ph1_res.get("best_val_loss", float("inf"))
    if not math.isfinite(ph1_val_loss):
        raise optuna.exceptions.TrialPruned()

    # Load best Phase 1 checkpoint before Phase 3
    ph1_ckpt = ckpt_dir / run_name_trial / "phase1_best.pt"
    if ph1_ckpt.is_file():
        try:
            from src.training.train import _load_checkpoint
            _load_checkpoint(model, None, ph1_ckpt, device)
        except Exception:
            pass

    # ---- Phase 3: Adam + L-BFGS fine-tuning --------------------------------
    try:
        _buf2 = io.StringIO()
        with contextlib.redirect_stdout(_buf2):
            ph3_res = _run_phase3(
                model, cfg, train_loader, val_loader, sampler,
                device, ckpt_dir, run_name_trial, mlflow_run=None,
            )
    except Exception as exc:
        print(f"[HPO Trial {trial.number}] Phase 3 failed: {exc}")
        raise optuna.exceptions.TrialPruned()

    val_rmse_K = ph3_res.get("val_rmse_K", float("inf"))
    if not math.isfinite(val_rmse_K):
        val_rmse_K = float("inf")

    elapsed = time.time() - t0

    # ---- Report intermediate value for pruning ----------------------------
    trial.report(val_rmse_K, step=1)
    if trial.should_prune():
        raise optuna.exceptions.TrialPruned()

    # ---- Compute test RMSE (secondary) ------------------------------------
    test_rmse_K = float("nan")
    try:
        from src.training.train import _validate, _build_sampler
        from src.loss.loss_functions import LossWeights
        test_vals = _validate(
            model, test_loader, LossWeights(), sampler,
            int(cfg.get("collocation", {}).get("n_points", 2000)),
            0, device, phase=3,
        )
        test_rmse_K = test_vals.get("val/rmse_dT_K", float("nan"))
    except Exception:
        pass

    # Store secondary metrics in trial user_attrs
    trial.set_user_attr("test_rmse_K", test_rmse_K)
    trial.set_user_attr("elapsed_s",   elapsed)

    print(
        f"[HPO Trial {trial.number:3d}] "
        f"val_RMSE={val_rmse_K:.3f} K  "
        f"test_RMSE={test_rmse_K:.3f} K  "
        f"time={elapsed:.0f}s  "
        f"w_data={params['w_data']:.2f}  "
        f"lr={params['lr_adam']:.2e}  "
        f"hidden={params['hidden_dim']}  "
        f"cond={params['conditioning']}"
    )

    # ---- Cleanup trial checkpoints (save disk) ----------------------------
    trial_ckpt_dir = ckpt_dir / run_name_trial
    if trial_ckpt_dir.is_dir():
        shutil.rmtree(trial_ckpt_dir, ignore_errors=True)

    return val_rmse_K


# ---------------------------------------------------------------------------
# run_hpo — main entry point
# ---------------------------------------------------------------------------

def run_hpo(
    base_config_path: Path,
    n_trials: int = 30,
    timeout_hours: float | None = None,
    study_name: str = "baseline_phaseA_hpo",
    storage_dir: Path | None = None,
    pruner_name: str = "median",
    resume: bool = False,
) -> "optuna.Study":
    """Execute full HPO study.

    Parameters
    ----------
    base_config_path : Path
        YAML config used as the base for all trials.
    n_trials : int
        Number of trials (default 30).
    timeout_hours : float | None
        Wall-clock timeout in hours. None = no timeout.
    study_name : str
        Optuna study name (also used for output filenames).
    storage_dir : Path | None
        Directory for SQLite DB. Defaults to 03_model/experiments/hpo_results/.
    pruner_name : str
        "median" or "none".
    resume : bool
        If True, load existing study from storage and continue.

    Returns
    -------
    optuna.Study
    """
    if not _OPTUNA_AVAILABLE:
        raise ImportError("optuna is required. Run: pip install optuna")

    # ---- Load base config --------------------------------------------------
    with open(base_config_path, "r") as fh:
        base_cfg = yaml.safe_load(fh)

    # ---- Storage -----------------------------------------------------------
    if storage_dir is None:
        storage_dir = _MODEL_ROOT / "experiments" / "hpo_results"
    storage_dir.mkdir(parents=True, exist_ok=True)
    db_path   = storage_dir / "study.db"
    storage_url = f"sqlite:///{db_path}"

    # ---- Sampler & Pruner --------------------------------------------------
    sampler = TPESampler(seed=42, n_startup_trials=5)

    if pruner_name == "median":
        pruner = MedianPruner(n_startup_trials=5, n_warmup_steps=0)
    else:
        pruner = optuna.pruners.NopPruner()

    # ---- Create or load study ----------------------------------------------
    study = optuna.create_study(
        study_name=study_name,
        direction="minimize",
        sampler=sampler,
        pruner=pruner,
        storage=storage_url,
        load_if_exists=resume or True,  # always resumable
    )

    print(f"\n{'='*70}")
    print(f"[HPO 시작]")
    print(f"스터디 이름: {study_name}")
    print(f"목표 Trial 수: {n_trials}")
    print(f"Storage: {db_path}")
    print(f"Base config: {base_config_path}")
    print(f"{'='*70}\n")

    timeout_s = timeout_hours * 3600 if timeout_hours is not None else None

    # ---- Optimize ----------------------------------------------------------
    study.optimize(
        lambda trial: objective(trial, base_cfg),
        n_trials=n_trials,
        timeout=timeout_s,
        n_jobs=1,           # serial on M1 CPU
        catch=(Exception,), # catch unexpected errors, mark trial as failed
        show_progress_bar=True,
    )

    # ---- Summary -----------------------------------------------------------
    _print_summary(study, study_name, storage_dir, base_config_path)

    return study


# ---------------------------------------------------------------------------
# Post-study analysis helpers
# ---------------------------------------------------------------------------

def _print_summary(
    study: "optuna.Study",
    study_name: str,
    storage_dir: Path,
    base_config_path: Path,
) -> None:
    """Print summary, save best_trial.yaml, baseline_phaseB.yaml, and figures."""

    completed = [t for t in study.trials if t.state == optuna.trial.TrialState.COMPLETE]
    pruned    = [t for t in study.trials if t.state == optuna.trial.TrialState.PRUNED]
    failed    = [t for t in study.trials if t.state == optuna.trial.TrialState.FAIL]

    print(f"\n{'='*70}")
    print(f"[HPO 완료]")
    print(f"스터디: {study_name}")
    print(f"시도 횟수: {len(study.trials)} (성공 {len(completed)}, 가지치기 {len(pruned)}, 실패 {len(failed)})")

    if not completed:
        print("[HPO] 완료된 trial이 없습니다.")
        return

    best = study.best_trial
    print(f"Best RMSE: {best.value:.3f} K")
    print(f"Best 파라미터:")
    for k, v in best.params.items():
        print(f"  - {k}: {v}")

    test_rmse = best.user_attrs.get("test_rmse_K", float("nan"))
    elapsed   = best.user_attrs.get("elapsed_s",   float("nan"))
    print(f"  test RMSE: {test_rmse:.3f} K")
    print(f"  trial elapsed: {elapsed:.0f} s")

    # ---- Top-5 trials ------------------------------------------------------
    sorted_trials = sorted(completed, key=lambda t: t.value)
    print(f"\nTop-5 trials:")
    print(f"{'rank':>4} {'trial':>6} {'val_RMSE[K]':>11} {'test_RMSE[K]':>12}  params")
    for rank, t in enumerate(sorted_trials[:5], 1):
        tr = t.user_attrs.get("test_rmse_K", float("nan"))
        p_str = "  ".join(f"{k}={v}" for k, v in t.params.items())
        print(f"{rank:4d} {t.number:6d} {t.value:11.3f} {tr:12.3f}  {p_str}")

    # ---- Parameter importances (Optuna built-in) ---------------------------
    print(f"\n주요 영향 인자 (importance):")
    try:
        importances = optuna.importance.get_param_importances(study)
        imp_sorted = sorted(importances.items(), key=lambda x: x[1], reverse=True)
        for rank, (pname, imp) in enumerate(imp_sorted[:5], 1):
            print(f"  {rank}. {pname} ({imp:.4f})")
    except Exception as exc:
        print(f"  [importance 계산 실패: {exc}]")
        imp_sorted = []

    # ---- Save best_trial.yaml ----------------------------------------------
    best_trial_path = storage_dir / "best_trial.yaml"
    best_trial_data = {
        "trial_number": best.number,
        "val_rmse_K":   best.value,
        "test_rmse_K":  test_rmse,
        "params":       best.params,
        "study_name":   study_name,
    }
    with open(best_trial_path, "w") as fh:
        yaml.dump(best_trial_data, fh, allow_unicode=True, sort_keys=False)
    print(f"\n저장: {best_trial_path}")

    # ---- Save baseline_phaseB.yaml -----------------------------------------
    try:
        with open(base_config_path, "r") as fh:
            base_cfg = yaml.safe_load(fh)
        best_cfg = _patch_config(base_cfg, best.params)
        # Restore full training schedule for best config
        best_cfg["run_name"] = "baseline_phaseB"
        best_cfg["training"]["phase1"]["epochs"]      = 500
        best_cfg["training"]["phase3"]["adam_epochs"] = 2000
        best_cfg["training"]["phase3"]["lbfgs_epochs"]= 1000
        best_cfg["training"]["phase1"]["early_stop_patience"] = 200
        best_cfg["training"]["phase3"]["early_stop_patience"] = 200

        phase_b_path = _MODEL_ROOT / "configs" / "baseline_phaseB.yaml"
        with open(phase_b_path, "w") as fh:
            yaml.dump(best_cfg, fh, allow_unicode=True, sort_keys=False)
        print(f"저장: {phase_b_path}")
    except Exception as exc:
        print(f"[WARNING] baseline_phaseB.yaml 저장 실패: {exc}")

    # ---- Figures -----------------------------------------------------------
    _save_figures(study, study_name)

    # ---- Top-10 trials table -----------------------------------------------
    _save_top10_table(sorted_trials, study_name)

    print(f"{'='*70}\n")


def _save_figures(study: "optuna.Study", study_name: str) -> None:
    """Save optimization history, param importances, parallel coordinates."""
    fig_dir = _PROJECT_ROOT / "04_analysis" / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    completed = [t for t in study.trials if t.state == optuna.trial.TrialState.COMPLETE]
    if not completed:
        return

    # ---- 1. Optimization history (matplotlib) ------------------------------
    if _MPL_AVAILABLE:
        try:
            values = [t.value for t in completed]
            trial_nums = [t.number for t in completed]
            best_so_far = [min(values[:i+1]) for i in range(len(values))]

            fig, axes = plt.subplots(1, 2, figsize=(14, 5))

            # Left: trial values + best-so-far
            axes[0].scatter(trial_nums, values, alpha=0.6, s=20, label="trial val RMSE")
            axes[0].plot(trial_nums, best_so_far, "r-", linewidth=1.5, label="best so far")
            axes[0].set_xlabel("Trial number")
            axes[0].set_ylabel("Val RMSE [K]")
            axes[0].set_title(f"Optimization history — {study_name}")
            axes[0].legend()
            axes[0].grid(True, alpha=0.3)

            # Right: parameter importances bar
            try:
                importances = optuna.importance.get_param_importances(study)
                names  = list(importances.keys())
                imps   = list(importances.values())
                # Sort descending
                pairs = sorted(zip(imps, names), reverse=True)
                imps_s  = [p[0] for p in pairs]
                names_s = [p[1] for p in pairs]
                axes[1].barh(names_s, imps_s, color="steelblue")
                axes[1].set_xlabel("Importance")
                axes[1].set_title("Parameter importances")
                axes[1].invert_yaxis()
                axes[1].grid(True, axis="x", alpha=0.3)
            except Exception:
                axes[1].text(0.5, 0.5, "Importance N/A", transform=axes[1].transAxes,
                             ha="center", va="center")

            plt.tight_layout()
            out_path = fig_dir / f"hpo_optimization_history.png"
            plt.savefig(out_path, dpi=150)
            plt.close(fig)
            print(f"저장: {out_path}")
        except Exception as exc:
            print(f"[HPO] optimization history plot 실패: {exc}")

    # ---- 2. Parallel coordinates (plotly -> static PNG if kaleido) ---------
    try:
        import plotly.graph_objects as go

        trial_data = []
        for t in completed:
            row = dict(t.params)
            row["val_rmse_K"] = t.value
            trial_data.append(row)

        if trial_data:
            import pandas as pd
            df_trials = pd.DataFrame(trial_data)

            # Encode categorical columns
            cat_cols = [c for c in df_trials.columns if df_trials[c].dtype == object]
            df_enc = df_trials.copy()
            cat_maps: dict[str, dict] = {}
            for col in cat_cols:
                cats = sorted(df_enc[col].unique().tolist())
                cat_maps[col] = {c: i for i, c in enumerate(cats)}
                df_enc[col] = df_enc[col].map(cat_maps[col])

            dims = []
            for col in df_enc.columns:
                if col == "val_rmse_K":
                    continue
                dims.append(
                    go.parcats.Dimension(
                        values=df_enc[col].tolist(),
                        label=col,
                        tickvals=list(range(len(cat_maps.get(col, {})))),
                        ticktext=list(cat_maps.get(col, {}).keys()) if col in cat_maps else None,
                    )
                    if col in cat_maps else
                    dict(values=df_enc[col].tolist(), label=col)
                )

            # Use plotly express parallel_coordinates (simpler API)
            try:
                import plotly.express as px
                color_col = "val_rmse_K"
                fig_plotly = px.parallel_coordinates(
                    df_enc,
                    color=color_col,
                    color_continuous_scale=px.colors.sequential.Viridis_r,
                    title=f"Parallel coordinates — {study_name}",
                )
                out_path_html = fig_dir / f"hpo_parallel_coord.html"
                fig_plotly.write_html(str(out_path_html))
                print(f"저장: {out_path_html}")

                # Try kaleido for static PNG
                try:
                    out_path_png = fig_dir / f"hpo_parallel_coord.png"
                    fig_plotly.write_image(str(out_path_png), scale=1.5)
                    print(f"저장: {out_path_png}")
                except Exception:
                    pass  # kaleido not installed — HTML only
            except Exception as exc2:
                print(f"[HPO] parallel_coord plot 실패: {exc2}")
    except Exception as exc:
        print(f"[HPO] plotly parallel coord 실패: {exc}")

    # ---- 3. Parameter importances bar (separate PNG) -----------------------
    if _MPL_AVAILABLE:
        try:
            importances = optuna.importance.get_param_importances(study)
            if importances:
                pairs = sorted(importances.items(), key=lambda x: x[1], reverse=True)
                names_s = [p[0] for p in pairs]
                imps_s  = [p[1] for p in pairs]

                fig2, ax2 = plt.subplots(figsize=(8, max(4, len(names_s) * 0.6)))
                bars = ax2.barh(names_s, imps_s, color="steelblue")
                ax2.bar_label(bars, fmt="%.3f", padding=3)
                ax2.set_xlabel("Importance (fANOVA)")
                ax2.set_title(f"HPO Parameter Importances — {study_name}")
                ax2.invert_yaxis()
                ax2.grid(True, axis="x", alpha=0.3)
                plt.tight_layout()
                out_path2 = fig_dir / f"hpo_param_importances.png"
                plt.savefig(out_path2, dpi=150)
                plt.close(fig2)
                print(f"저장: {out_path2}")
        except Exception as exc:
            print(f"[HPO] param_importances plot 실패: {exc}")


def _save_top10_table(
    sorted_trials: list,
    study_name: str,
) -> None:
    """Save top-10 trials as a markdown table."""
    table_dir = _PROJECT_ROOT / "04_analysis" / "tables"
    table_dir.mkdir(parents=True, exist_ok=True)
    out_path = table_dir / "hpo_top10_trials.md"

    lines = [
        f"# HPO Top-10 Trials — {study_name}",
        "",
        "| rank | trial | val_RMSE [K] | test_RMSE [K] | "
        "w_pde | w_bc | w_data | w_onb | lr_adam | hidden_dim | latent_dim | n_layers | conditioning |",
        "|------|-------|-------------|---------------|"
        "------|------|--------|-------|---------|------------|------------|----------|--------------|",
    ]
    for rank, t in enumerate(sorted_trials[:10], 1):
        p = t.params
        tr = t.user_attrs.get("test_rmse_K", float("nan"))
        row = (
            f"| {rank} | {t.number} | {t.value:.3f} | {tr:.3f} | "
            f"{p.get('w_pde', '-'):.3f} | {p.get('w_bc', '-'):.3f} | "
            f"{p.get('w_data', '-'):.2f} | {p.get('w_onb', '-'):.3f} | "
            f"{p.get('lr_adam', '-'):.2e} | {p.get('hidden_dim', '-')} | "
            f"{p.get('latent_dim', '-')} | {p.get('n_layers', '-')} | "
            f"{p.get('conditioning', '-')} |"
        )
        lines.append(row)

    lines += [
        "",
        "Baseline (phaseA): val RMSE = 5.60 K, test RMSE = 5.84 K",
        "",
        f"Generated by hpo.py  —  study: {study_name}",
    ]

    with open(out_path, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"저장: {out_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="PINN-ONB01 Optuna HPO",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.training.hpo --n-trials 30 --study-name baseline_phaseA_hpo
  python -m src.training.hpo --resume --study-name baseline_phaseA_hpo
""",
    )
    parser.add_argument(
        "--base", type=Path,
        default=_MODEL_ROOT / "configs" / "baseline_phaseA.yaml",
        help="Base YAML config path",
    )
    parser.add_argument("--n-trials",      type=int,   default=30,
                        help="Number of trials (default 30)")
    parser.add_argument("--timeout-hours", type=float, default=None,
                        help="Wall-clock timeout in hours")
    parser.add_argument("--study-name",    type=str,   default="baseline_phaseA_hpo",
                        help="Optuna study name")
    parser.add_argument("--storage-dir",   type=Path,
                        default=_MODEL_ROOT / "experiments" / "hpo_results",
                        help="Directory for SQLite storage")
    parser.add_argument("--pruner",        type=str,   default="median",
                        choices=["median", "none"])
    parser.add_argument("--resume", action="store_true",
                        help="Resume an existing study")
    return parser.parse_args()


def _main() -> None:
    args = _parse_args()

    if not _OPTUNA_AVAILABLE:
        print("[HPO] ERROR: optuna is not installed. Run: pip install optuna")
        sys.exit(1)

    study = run_hpo(
        base_config_path=args.base,
        n_trials=args.n_trials,
        timeout_hours=args.timeout_hours,
        study_name=args.study_name,
        storage_dir=args.storage_dir,
        pruner_name=args.pruner,
        resume=args.resume,
    )


if __name__ == "__main__":
    _main()
