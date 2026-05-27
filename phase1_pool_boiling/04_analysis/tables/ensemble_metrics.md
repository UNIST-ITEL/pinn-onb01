# Deep Ensemble UQ — Metrics Report (Section 5.3)

Members: K = 10

Aleatoric assumption: fixed ±20% of prediction (literature-typical for ONB)


## Overall ensemble performance

| Metric | Value |
|--------|-------|
| Ensemble mean RMSE | 3.68 K |
| Ensemble mean MAE  | 2.74 K |
| Ensemble mean R²   | 0.353 |
| 95% CI Coverage    | 98.7% (target: 95%) |
| Mean σ_total        | 4.09 K |
| Max σ_total         | 7.92 K (SFC-015, water, JONES_2009) |
| Mean σ_epi          | 3.85 K |
| Mean σ_ale          | 1.34 K |
| Dominant uncertainty | epistemic |

## Fluid breakdown

| Fluid | n | RMSE [K] | MAE [K] | R² | Coverage [%] | Mean σ_epi [K] |
|-------|---|----------|---------|-----|-------------|---------------|
| R-123 | 10 | 2.12 | 1.71 | 0.179 | 100.0 | 2.44 |
| R-134a | 34 | 1.56 | 1.35 | -0.070 | 100.0 | 1.81 |
| water | 33 | 5.26 | 4.47 | 0.161 | 97.0 | 6.38 |

## Source paper breakdown

| Paper | n | RMSE [K] | MAE [K] | R² | Coverage [%] | Mean σ_epi [K] |
|-------|---|----------|---------|-----|-------------|---------------|
| BETZ_2013 | 10 | 6.11 | 5.78 | -1.033 | 100.0 | 6.75 |
| BOURDON_2012 | 6 | 2.47 | 2.14 | 0.195 | 100.0 | 5.94 |
| BOURDON_2015 | 5 | 5.78 | 5.59 | -0.036 | 100.0 | 6.79 |
| JABARDO_2009 | 44 | 1.70 | 1.43 | 0.299 | 100.0 | 1.96 |
| JONES_2009 | 5 | 2.67 | 2.58 | -0.008 | 100.0 | 5.75 |
| JO_2011 | 2 | 4.26 | 3.53 | 0.097 | 100.0 | 5.69 |
| PHAN_2009 | 5 | 7.29 | 5.81 | -1.510 | 80.0 | 6.67 |

## Model comparison

| Model | RMSE [K] | MAE [K] | R² | n |
|-------|----------|---------|-----|---|
| Hsu (1962) | 7.43 | 6.07 | -0.978 | 43 |
| Davis-Anderson (1966) | 16.47 | 10.26 | -8.721 | 43 |
| Bergles-Rohsenow (1964) | 7.87 | 6.37 | -0.874 | 33 |
| Sato-Matsumura (1964) | 7.43 | 6.07 | -0.978 | 43 |
| Basu et al. (2002) | 7.21 | 5.85 | -0.208 | 22 |
| PINN phaseB (single) | 5.55 | 4.62 | -0.105 | 43 |
| **PINN phaseB Ensemble (K=10)** | **3.68** | **2.74** | **0.353** | **77** |
