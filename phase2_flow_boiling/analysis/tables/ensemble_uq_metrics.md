# Phase 2 Deep Ensemble UQ (K=5, v11 config, split_seed=42 fixed)

_2026-05-31. seeds 42-46, identical train/val/test split (58 test rows)._

## Member test RMSE_ΔT
| seed | RMSE_ΔT (K) |
|---|---|
| 42 | 2.264 |
| 43 | 2.236 |
| 44 | 1.636 |
| 45 | 1.758 |
| 46 | 1.585 |

## Ensemble (mean prediction) vs single v11
| metric | ensemble K=5 | single v11 |
|---|---|---|
| RMSE_ΔT | **1.725 K** | 1.84 K |
| R²_ΔT | **0.796** | 0.768 |
| RMSE_q | 152 kW/m² | 144 kW/m² |
| R²_q | 0.709 | 0.741 |

> Ensembling improved ΔT (1.84→1.72K, R² 0.768→0.796); q ~unchanged.

## Calibration (epistemic-only)
- mean epistemic std = 0.51 K
- 1σ coverage = 28% (ideal 68%), 2σ = 42% (ideal 95%) → **epistemic underestimates total uncertainty**
- recalibration factor ≈ **4.7×** to reach 68% at 1σ
- Deep-ensemble epistemic captures only model-disagreement; dominant uncertainty
  is aleatoric (digitization + experimental scatter, ~1K), not modelled here →
  heteroscedastic head (deferred) needed for full calibration. A simple 4.7×
  scaling gives well-calibrated intervals as an interim fix.

## Uncertainty vs pressure (epistemic std ΔT)
| range | n | mean std | mean \|err\| |
|---|---|---|---|
| <0.2 MPa | 21 | 0.66 K | 0.91 K |
| 0.2-1 MPa | 2 | 0.25 K | 0.20 K |
| 1-3 MPa | 8 | 0.32 K | 1.37 K |
| ≥3 MPa | 3 | 0.31 K | 0.88 K |

> Epistemic std does NOT strongly flag the high-P region — the 5 members agree
> there (Wang anchors in train) yet retain ~0.9K error → residual is
> aleatoric/structural, not model-variance. Honest UQ limitation documented.
