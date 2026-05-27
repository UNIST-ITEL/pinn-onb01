# PINN-ONB01: Surface-Conditioned Physics-Informed Neural Network for Pool-Boiling ONB

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![License: MIT](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE-CODE)
[![License: CC BY 4.0](https://img.shields.io/badge/Data-CC%20BY%204.0-lightgrey.svg)](LICENSE-DATA)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)

Official implementation and dataset for:

> **Lee, J., Kim, G., Ko, E., Kim, Y.** (2026).
> *Surface-Conditioned Physics-Informed Neural Network for Pool-Boiling Onset of Nucleate Boiling.*
> International Journal of Heat and Mass Transfer.
> DOI: [to be assigned upon publication]

---

## Overview

This repository hosts the trained models, source code, and curated dataset for a
Physics-Informed Neural Network (PINN) that predicts the **onset of nucleate
boiling (ONB)** in pool-boiling configurations, conditioned on a learned
**surface-descriptor embedding**.  The framework couples Hsu's nucleation
criterion as a soft physics constraint with a deep-ensemble uncertainty
quantification head.

Headline results (full details in the paper):

| Metric | Best classical correlation | PINN (this work) |
|---|---|---|
| Test RMSE on $\Delta T_{\mathrm{ONB}}$ [K] | _to fill at proof_ | _to fill at proof_ |
| Test MAE [K]   | _to fill_ | _to fill_ |
| $R^2$          | _to fill_ | _to fill_ |
| Spearman $\rho$ vs. $R_a$ (R-134a subset) | n/a | _to fill_ |

The trained PINN out-performs the best classical correlation (Basu et al., 2002)
on the held-out test partition and recovers all five physical monotonicity
trends (q'', $R_a$, $\theta$, $P$, $\Delta T_{\mathrm{sub}}$).

---

## Quick start

```bash
# 1. Clone
git clone https://github.com/UNIST-ITEL/pinn-onb01.git
cd pinn-onb01

# 2. Set up environment (conda recommended)
conda env create -f environment.yml
conda activate pinn-onb01

# 3. Reproduce the headline figures
make figures

# 4. Train a single PINN from scratch
python -m pinn_onb.train --config phase1_pool_boiling/03_model/configs/baseline.yaml

# 5. Reproduce the deep ensemble (K=10)
make ensemble
```

GPU is recommended (training ~30 minutes per seed on a single NVIDIA RTX 3090);
CPU runs work but are noticeably slower.

---

## Repository layout

```
.
├── phase1_pool_boiling/           # Phase 1 deliverables (relocated 2026-05-27)
│   ├── 02_data/
│   │   ├── processed/
│   │   │   ├── boiling_curves.csv # 1361 × 14
│   │   │   ├── onb_dataset.csv    # 82 × 12
│   │   │   └── surface_cards/     # 49 surface descriptor cards (YAML)
│   │   └── raw/
│   │       └── digitization/      # WebPlotDigitizer metadata per paper
│   ├── 03_model/
│   │   ├── src/pinn_onb/          # PyTorch source
│   │   ├── configs/               # YAML hyperparameter configs
│   │   └── checkpoints/ensemble_k10/  # 10 trained PINN ensemble members
│   └── 04_analysis/
│       ├── scripts/               # figure / table reproduction
│       ├── notebooks/             # interactive Jupyter notebooks
│       └── figures/               # PNG outputs
├── LICENSE-CODE                   # MIT (covers all source code)
├── LICENSE-DATA                   # CC-BY-4.0 (covers all CSV/YAML data)
├── CITATION.cff                   # machine-readable citation metadata
├── requirements.txt
└── environment.yml
```

---

## Dataset

The dataset is also archived independently on Zenodo with a permanent DOI:

> **Lee, J., Kim, G., Ko, E., Kim, Y.** (2026).
> *PINN-ONB01 pool-boiling ONB dataset (v1.0)* \[Data set].
> Zenodo. <https://doi.org/10.5281/zenodo.XXXXXXX>

Contents:

- **1361** boiling-curve points (post-standardization), spanning seven primary
  sources: BETZ-2013, BOURDON-2012, BOURDON-2015, JABARDO-2009, JONES-2009,
  JO-2011, PHAN-2009.
- **82** ONB labels (24 manual + 58 heuristic-then-vetted).
- **49** unique surface descriptor cards (YAML), each carrying material,
  treatment, $R_a$, $\theta$, fluid environment, source paper, and
  literature-reported cavity statistics if available.
- **Per-paper digitization metadata** (`.tar.gz` per source) containing the
  raw WebPlotDigitizer project files used to extract every curve.  This
  allows independent reviewers to re-trace any data point back to the
  original figure.

Fluids covered: water, R-123, R-134a, FC-77 (released but excluded from PINN
training because CoolProp does not provide a validated equation of state for
FC-77).

Column schemas, units, and the source-paper mapping are documented in
`phase1_pool_boiling/02_data/processed/README.md`.

---

## Reproducing the paper

| Paper artifact | Command |
|---|---|
| Figures 2--9 | `make figures` |
| Tables 2--5  | `python -m pinn_onb.eval --report tables` |
| Hyperparameter search (top-5 trials, Supp. § S5) | `make hpo` (Optuna TPE, ~6 h GPU) |
| Phase 1--4 training progression (Supp. § S6) | `make phases` |
| Deep ensemble uncertainty quantification (K=10) | `make ensemble` |

Random seeds and exact dependency versions are pinned for bit-exact replay
on Linux x86\_64 with CUDA 12.x and PyTorch 2.x.

---

## Citation

Please cite **both** the paper and the dataset:

```bibtex
@article{lee2026pinn_onb,
  author  = {Lee, Jaeseon and Kim, Gyuchang and Ko, Eunjeong and Kim, Yujin},
  title   = {Surface-Conditioned Physics-Informed Neural Network for
             Pool-Boiling Onset of Nucleate Boiling},
  journal = {International Journal of Heat and Mass Transfer},
  year    = {2026},
  doi     = {10.1016/j.ijheatmasstransfer.2026.XXXXXX}
}

@dataset{lee2026pinn_onb_data,
  author    = {Lee, Jaeseon and Kim, Gyuchang and Ko, Eunjeong and Kim, Yujin},
  title     = {PINN-ONB01 pool-boiling ONB dataset (v1.0)},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.XXXXXXX},
  url       = {https://doi.org/10.5281/zenodo.XXXXXXX}
}
```

Users of the underlying experimental data should additionally cite the
relevant primary sources (mapping provided in
`phase1_pool_boiling/02_data/processed/README.md`).

---

## Licenses

| Component | License |
|---|---|
| Source code (`phase1_pool_boiling/03_model/`, `…/04_analysis/scripts/`, notebooks) | **MIT** — see [LICENSE-CODE](LICENSE-CODE) |
| Curated dataset (`phase1_pool_boiling/02_data/`)               | **CC-BY-4.0** — see [LICENSE-DATA](LICENSE-DATA) |
| Raw figures from primary sources                               | _Not redistributed_ (publisher copyright) |

We redistribute only the numerical values extracted from the public figures of
the seven primary references, together with the per-figure digitization
metadata.  The raw PDFs themselves must be obtained from the original
publishers.

---

## Acknowledgements

This work was supported by:

- National Research Foundation of Korea (NRF) Grants NRF-2023R1A2C2006930
  and NRF-2020R1A5A8018822;
- Korea Institute of Energy Technology Evaluation and Planning (KETEP)
  Grant RS-2024-00436521.

---

## Contact

- **Jaeseon Lee** (corresponding author) — JaeseonLee@unist.ac.kr
- Lab — Innovative Thermal Engineering Laboratory, UNIST
- Issue tracker — please open a [GitHub issue](https://github.com/UNIST-ITEL/pinn-onb01/issues)
  for code, reproducibility, or dataset questions.
