# Phase 2 — LOSO + Transfer-Learning Ablation (real training runs, 2026-06-04)

All runs use the v11 architecture/loss and the v11 training budget
(Adam 2000+3000 epochs → L-BFGS), differing only as noted. Test metrics are on
the held-out set; "val" is on the non-held-out studies.

## Leave-one-study-out (LOSO) cross-validation

Each row holds out one study **entirely** as the test set and trains/validates on
the remaining nine (config: `data.holdout_paper`). This probes true
study-to-study extrapolation, unlike the per-study stratified split used for the
headline number.

| Holdout study | regime | n_test (ΔT) | Test ΔT RMSE [K] | Test R²_ΔT | Val ΔT RMSE [K] |
|---|---|---|---|---|---|
| Wang 2024 | high-P 10–16 MPa | 7 | 5.70 | −87.3 | 2.60 |
| Qu 2002 | microchannel 0.35 mm | 11 | 7.70 | −1.51 | 2.31 |
| Liu 2005 | microchannel | 23 | 6.87 | −2.91 | 2.47 |
| Cheng 2022 | narrow channel (central) | 54 | 10.90 | −227 | 2.22 |
| **v11 (stratified split, reference)** | all | 58 | **1.84** | **0.768** | — |

**Reading:** the per-study stratified test error (1.84 K) reflects *interpolation
within sampled studies*; holding out an entire study degrades the wall-superheat
RMSE to 5.7–10.9 K (all R² < 0). Generalization to an unseen study is therefore
poor — even for a central, low-pressure study (Cheng). The model's defensible
operating regime is interpolation within the trained envelope; cross-study
extrapolation is a limitation.

## Transfer-learning ablation (stratified split, n_test ΔT = 36)

| Variant | surface encoder | Test ΔT RMSE [K] | Test R²_ΔT | Test q RMSE [kW/m²] |
|---|---|---|---|---|
| A (= v11) | transferred, **frozen** | 1.84 | 0.768 | 144 |
| B | random init, **trained** | 1.77 | 0.784 | 155 |
| C | random init, **frozen** | 2.36 | 0.618 | 130 |

**Reading:** a trained encoder (B) matches the frozen transferred encoder (A) on
ΔT (1.77 vs 1.84 K) — transfer is *not* required for raw accuracy. However, the
frozen transferred encoder (A) clearly beats the frozen *random* encoder (C,
2.36 K): the transferred representation is an **informative frozen prior**,
worth ~0.5 K when surface descriptors are sparse, at no extra trainable cost.

## Conditional-Nusselt robustness check (Hsu constraint closure)

The flow-aware Hsu constraint uses Nu to set the thermal-boundary-layer
thickness $\delta_t = C\,D_h/Nu$. The main model uses the turbulent
Dittus--Boelter Nu for all rows; the consult flagged this as unphysical for the
low-Reynolds microchannel subset. We added a config-gated regime-dependent Nu
(`loss.hsu_constraint.nu_model = conditional`): laminar $Nu=4.36$ (Re ≤ 2300),
Gnielinski (2300 < Re < 1e4), Dittus--Boelter (Re ≥ 1e4), and retrained.

| Hsu Nu closure | Test ΔT RMSE [K] | R²_ΔT | Test q RMSE [kW/m²] | R²_q |
|---|---|---|---|---|
| Dittus--Boelter (v11, main) | 1.84 | 0.768 | 144 | 0.741 |
| **Conditional (regime-dependent)** | **1.78** | **0.784** | **136** | **0.767** |

The regime-dependent closure is physically preferable and *marginally improves*
all metrics, so the constraint is robust to this choice (and a desk-review attack
on the single-Nu assumption is pre-empted). Config: `phase2_condnu.yaml`.

## Provenance

- Configs: `experiments/configs/phase2_loso_{wang,qu,liu,cheng}.yaml`,
  `phase2_abl_{randtrain,randfrozen}.yaml`.
- Logs: `experiments/logs/loso/*.log`. Checkpoints: `experiments/checkpoints/phase2_{loso_*,abl_*}/`.
- LOSO implemented via `FlowBoilingDataset(holdout_paper=...)` (dataset.py) + `data.holdout_paper` config.
