# Phase 2 manuscript figure scripts

One script per manuscript figure. **Run from the `phase2_flow_boiling/` root:**

```bash
python analysis/scripts/fig_pressure_trend.py
```

Each script writes `<name>.png` and `<name>.pdf` to **both** `analysis/figures/`
(reproducible source) and `manuscript/figures/` (submission package) via
`figlib.save_fig`, so editing a figure never leaves the paper stale.

| Script | Manuscript label | Section | Source |
|---|---|---|---|
| `fig_architecture.py` | fig:arch | Methods 2.2 | schematic (matplotlib) |
| `fig_onb_concept.py` | fig:concept | Methods 2.3 | schematic |
| `fig_coverage_map.py` | fig:coverage | Data 3.1 | CSV |
| `fig_data_distributions.py` | fig:dist | Data 3.1 | CSV |
| `fig_parity.py` | fig:parity | Results 4.1 | v11 model (test) → 2 files |
| `fig_per_source_rmse.py` | fig:persource | Results 4.1 | v11 model (all) |
| `fig_ablation_progression.py` | fig:ablation | Results 4.2 | hardcoded table values |
| `fig_pressure_trend.py` | fig:ptrend | Results 4.3.2 | v11 model |
| `fig_physics_trends.py` | fig:trends | Results 4.3.3 | v11 model |
| `fig_ensemble_uq.py` | fig:uq | Results 4.4 | 5 ensemble members |
| `fig_design_map.py` | fig:designmap | Discussion 5.1 | v11 model (grid) |

`figlib.py` holds shared style, paths, model/dataset loaders and `save_fig`.

## Caveats
- **scipy not installed** → Gaussian coverage uses `math.erf`.
- **v9 checkpoint is 9-channel** (pre-pressure-feature); the current code is
  11-channel, so v9 cannot be loaded for a pressure-blind overlay.
- FINAL best model = **v11** (`phase2_v11_highP_wang`).
- `fig_ablation_progression.py` values are hardcoded from PROGRESS_LOG's
  experiment table — update them there and here together.
- Regenerate all: `for f in analysis/scripts/fig_*.py; do python "$f"; done`
  (≈ a few minutes; the ensemble figure loads 5 checkpoints).
