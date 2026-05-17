# PINN-ONB01 — Curated Pool-Boiling Dataset

**Version:** 1.0
**Release:** Upon acceptance of the associated IJHMT paper
**License:** [Creative Commons Attribution 4.0 International (CC-BY-4.0)](../../LICENSE-DATA)
**Maintainer:** Innovative Thermal Engineering Laboratory (ITEL), UNIST
**Contact:** Jaeseon Lee `<JaeseonLee@unist.ac.kr>`
**ORCID:** [0000-0003-1996-6086](https://orcid.org/0000-0003-1996-6086)
**Citation DOIs (assigned upon acceptance):**
- Dataset DOI: `10.5281/zenodo.XXXXXXX`  *(Zenodo, to be issued)*
- Paper DOI: `10.1016/j.ijheatmasstransfer.2026.XXXXXX`  *(IJHMT, to be assigned)*

---

## 1. Overview

This package contains the curated pool-boiling corpus used to train and
validate the Physics-Informed Neural Network (PINN) reported in
**Lee et al. (2026)**, *Surface-Conditioned Physics-Informed Neural
Network for Pool-Boiling Onset of Nucleate Boiling*, IJHMT.

The corpus consolidates digitized boiling curves from **seven primary
references** and the associated surface-descriptor metadata.  All
numerical values were extracted from the published figures using
[WebPlotDigitizer v5.x](https://automeris.io/) and standardized to SI
units.

### Quick facts

| Metric | Value |
|---|---|
| Curve points (post-standardization) | **1361** |
| ONB labels | **82** (24 manual + 58 slope-change-then-vetted) |
| Surface descriptor cards | **49** (`SFC-001` … `SFC-049`) |
| Primary sources | **7** journals papers |
| Fluids | **4** (water, R-123, R-134a, FC-77) |
| Wall-superheat range at ONB | $\Delta T_{\mathrm{ONB}} \in [0.7,\ 24.9]\;\mathrm{K}$ |
| Heat-flux range (labelled) | $q'' \in [0.1,\ 1434]\;\mathrm{kW/m^2}$ |

> **Note on FC-77.** Five FC-77 rows from JONES-2009 and JABARDO-2009 are
> included for transparency but are **excluded from PINN training** because
> CoolProp does not currently provide a validated equation of state for this
> fluid (see § 6 below).

---

## 2. Files

```
02_data/
├── processed/
│   ├── README.md                  ← this file
│   ├── boiling_curves.csv         ← 1361 rows × 14 columns
│   └── onb_dataset.csv            ← 82 rows × 12 columns
├── surface_cards/
│   ├── _index.md                  ← human-readable surface-descriptor table
│   └── *.yaml                     ← (49 files) one card per heater surface
└── raw/
    └── literature/
        ├── BETZ_2013/             ← per-paper WebPlotDigitizer projects
        ├── BOURDON_2012/
        ├── BOURDON_2015/
        ├── JABARDO_2009/
        ├── JONES_2009/
        ├── JO_2011/
        ├── PHAN_2009/
        ├── SCHEMA.md              ← naming + per-figure metadata format
        ├── WORKFLOW.md            ← digitization protocol
        ├── digitize_inventory.md  ← per-figure traceability table
        ├── figure_targets.md      ← which figures were digitized and why
        └── _index.md              ← raw-data index
```

The `raw/literature/<SOURCE>/` directories hold the **per-figure
WebPlotDigitizer project files** (`.tar.gz` archives in the public
release).  They contain the calibration metadata, the raw click points,
and the export-time settings, allowing any reviewer to replay the
extraction.  **The underlying PDFs of the primary references are not
redistributed**; only the numerical traces and the WPD project files
created from them are released here.

---

## 3. Column schema — `boiling_curves.csv`

Full boiling-curve corpus (single-phase + nucleate-boiling branches,
post-CHF points removed).

| # | Column | Type | Unit | Description |
|---|---|---|---|---|
| 1 | `source_paper`   | str    | — | Primary reference key (one of seven, see § 5) |
| 2 | `figure_ref`     | str    | — | Figure identifier inside the source (e.g., `Fig4_Hydrophilic`, `Fig10a_Br_Ra0p08P`) |
| 3 | `surface_id`     | str    | — | Stable identifier, format `SFC-NNN` (matches `surface_cards/`) |
| 4 | `surface_label`  | str    | — | Human-readable surface label (e.g., `BETZ_Hydrophilic`) |
| 5 | `fluid`          | str    | — | Working fluid: `water`, `R-123`, `R-134a`, `FC-77` |
| 6 | `delta_T_wall`   | float  | K    | Wall superheat $T_{\mathrm{wall}} - T_{\mathrm{sat}}$ |
| 7 | `delta_T_sub`    | float  | K    | Subcooling $T_{\mathrm{sat}} - T_{\mathrm{bulk}}$ (0 = saturated) |
| 8 | `q_flux`         | float  | W/m² | Applied heat flux |
| 9 | `Ra_um`          | float  | μm   | Arithmetic-mean roughness of the surface (some entries nano-scale → reported as $R_a$ in μm, e.g., `0.001` = 1 nm). See § 4 caveat |
| 10 | `theta_deg`     | float  | °    | Static contact angle (empty if not reported in the source) |
| 11 | `category`      | str    | —    | Coarse category for stratified sampling (see § 5) |
| 12 | `ONB_flag`      | bool   | —    | `True` if this row is the labelled ONB point of its curve |
| 13 | `r_c_um`        | float  | μm   | Inferred active cavity radius from Hsu inversion (only for ONB rows; empty otherwise) |
| 14 | `notes`         | str    | —    | Free-text provenance/QA notes (e.g., `ONB_manual (preserved)`, `ONB_auto (hint=[2.0,7.0]K)`) |

### Conventions

- **SI units everywhere.** Source values reported in kW/m² were
  multiplied by $10^{3}$; values in mW/cm² by $10$; $h$-axis figures
  were converted via $\Delta T_{\mathrm{wall}} = q''/h$.
- **Roughness reporting.** The `Ra_um` column always carries μm.
  Sources reporting in nm have been converted (e.g., `30 nm`
  $\rightarrow$ `0.030`).  When the source reports $S_a$ (areal mean)
  rather than $R_a$ (line mean), the value is treated as the surface
  card's representative roughness and the distinction is recorded in
  `surface_cards/<SFC-NNN>.yaml` under the `roughness:` key.
- **Missing values.** Empty cells indicate a value not reported in the
  source. Downstream code must handle `NaN` explicitly; the PINN
  pipeline imputes through the surface-encoder defaults documented in
  the paper.
- **Heat-flux sign.** All fluxes are reported as positive (heating).

---

## 4. Column schema — `onb_dataset.csv`

Restricted view: one row per ONB label, twelve columns.  This is the
table consumed by the `L_ONB` data loss term in the PINN.

| # | Column | Unit | Description |
|---|---|---|---|
| 1 | `source_paper`   | —    | Same as above |
| 2 | `figure_ref`     | —    | Same as above |
| 3 | `surface_id`     | —    | `SFC-NNN` |
| 4 | `surface_label`  | —    | Human label |
| 5 | `fluid`          | —    | One of four |
| 6 | `delta_T_wall`   | K    | The labelled ONB superheat $\Delta T_{\mathrm{ONB}}$ |
| 7 | `delta_T_sub`    | K    | Subcooling at the ONB point |
| 8 | `q_flux`         | W/m² | $q''_{\mathrm{ONB}}$ |
| 9 | `Ra_um`          | μm   | Same as above |
| 10 | `theta_deg`     | °    | Same as above |
| 11 | `category`      | —    | Same as above |
| 12 | `notes`         | —    | Label provenance (`ONB_manual` vs `ONB_auto`, override notes, etc.) |

`r_c_um` is omitted here; the value can be reconstructed by reading
`boiling_curves.csv` and selecting rows with `ONB_flag == True`, or by
running the Hsu inversion routine in `03_model/src/pinn_onb/hsu.py`.

---

## 5. Source-paper mapping

Required citations for users of the underlying experimental data.

| `source_paper` key | Primary reference | Surfaces | Curves | ONB | Fluid(s) |
|---|---|---|---|---|---|
| `BETZ_2013`     | Betz et al., *Int. J. Heat Mass Transf.* 57, 733–741 (2013)  | 7  | 168 | 10 | water |
| `BOURDON_2012`  | Bourdon et al., *Langmuir* 28, 6557–6564 (2012)              | 5  | 144 | 6  | water |
| `BOURDON_2015`  | Bourdon et al., *Langmuir* 31, 12386–12392 (2015)            | 4  | 75  | 5  | water |
| `JABARDO_2009`  | Jabardo et al., *Exp. Therm. Fluid Sci.* 33, 579–590 (2009)  | 20 | 589 | 44 | R-123 / R-134a / FC-77 |
| `JONES_2009`    | Jones et al., *J. Heat Transfer* 131, 121009 (2009)          | 6  | 320 | 10 | water / FC-77 |
| `JO_2011`       | Jo et al., *Int. J. Heat Mass Transf.* 54, 5643–5652 (2011)  | 2  | 14  | 2  | water |
| `PHAN_2009`     | Phan et al., *Int. J. Heat Mass Transf.* 52, 5459–5471 (2009)| 5  | 51  | 5  | water |
| **Total**       |                                                              | **49** | **1361** | **82** | 4 fluids |

Full bibliographic details are in `05_manuscript/references.bib` of the
source repository.  Per-row provenance (which figure was digitized for
which point) is in the `figure_ref` column.

The coarse `category` column is for stratified-sampling convenience and
should **not** be treated as a model input; surface conditioning is
done exclusively through the surface-card vector.  The categories
appearing in v1.0 are:
`betz`, `bourdon12`, `bourdon15`, `jabardo`, `jabardo_br`, `jabardo_ss`,
`jones`, `jones_F`, `jones_w`, `jo`, `phan`.

---

## 6. Fluid coverage and FC-77 exclusion

| Fluid    | ONB rows | Notes |
|---|---|---|
| Water    | 33 | All seven primary sources except the pure-refrigerant rows of JABARDO_2009. Near atmospheric pressure. |
| R-134a   | 34 | JABARDO_2009 only. $p_r \approx 0.06$–$0.26$. |
| R-123    | 10 | JABARDO_2009 only. $p_r \approx 0.06$. |
| FC-77    | 5  | JONES_2009 + JABARDO_2009. **Released, but excluded from PINN training.** |

**Why FC-77 is released yet excluded.** The PINN evaluates the PDE
residual, the Hsu nucleation discriminant, and the non-dimensional
scales $(L_c, \Delta T_{\mathrm{ref}}, q_{\mathrm{ref}})$ using rigorous
saturated-state properties $(\rho_l, \rho_v, h_{fg}, \sigma, c_{p,l},
k_l)$.  CoolProp does not currently expose a validated equation of state
for FC-77, so these properties would have to be substituted with literature
look-ups of uncertain accuracy. To preserve physical rigour we exclude
the five FC-77 rows from training, but retain them in the released CSVs
so that the exclusion boundary is transparent and auditable. Users who
elect to supply their own FC-77 properties may include those rows by
filtering `fluid != 'FC-77'` to obtain the n = 77 training subset, or
by retaining all 82 rows.

---

## 7. Surface descriptor cards (`surface_cards/`)

Each unique heater is registered as a **surface card** (`SFC-NNN.yaml`).
The 49 cards are the canonical surface metadata source consumed by the
**surface encoder** module of the PINN (see Section 4 of the paper).
Card schema:

```yaml
# surface_cards/SFC-001.yaml  (example)
id: SFC-001
label: BETZ_Hydrophilic
source_paper: BETZ_2013
material: silicon
treatment:
  primary: oxidized
  coating: null
roughness:
  Ra_um: 0.001           # 1 nm
  measurement: nano      # nano | polished | EDM | grit | engineered
  source_type: Ra        # Ra | Sa | RMS | reported_band
contact_angle:
  static_deg: 20.0
  notes: "7-30 deg range reported, midpoint used"
fluid_environment:
  fluids_tested: [water]
  pressure_atm: 1.0
  subcooling_K: 0.0
cavity_statistics:
  r_c_um: null           # populated only if directly reported
  N_s_per_cm2: null
literature_figures:
  - Fig4_Hydrophilic
  - Fig6b_hydrophilic
notes: >
  Oxidized silicon, no patterning.
```

`surface_cards/_index.md` provides the human-readable summary table
covering all 49 cards grouped by source paper, with the
roughness/contact-angle/treatment summary and links into the figure
references.

---

## 8. Digitization metadata (`raw/literature/<SOURCE>/`)

Each per-paper directory contains:

- **WebPlotDigitizer project file(s)** (`.tar` or `.json`) — one per
  digitized figure.  Replaying these in WPD reproduces the exact
  numerical extraction step-by-step.
- **Calibration screenshots** — figure crops with the axis-tick
  calibration points marked.
- **Per-figure README** — axis units, scale (linear/log), and any
  decisions made when the source figure was ambiguous.

The two top-level helper documents in `raw/literature/` are also
released:

- `SCHEMA.md` — the per-column naming convention applied during
  standardization;
- `WORKFLOW.md` — the four-stage curation pipeline
  (*select* → *digitize* → *standardize* → *book-keep*) used to build
  the corpus;
- `digitize_inventory.md` — per-figure traceability table linking each
  raw curve back to a source figure;
- `figure_targets.md` — list of figures selected for digitization and
  the criteria each one satisfies.

---

## 9. ONB labelling protocol

- **24 manual labels** were assigned at clearly identifiable inflection
  points (specific figures listed in Section 3 of the paper).
- **58 heuristic labels** were assigned by detecting the first point at
  which the local slope in $\log q''$–$\log \Delta T_{\mathrm{wall}}$
  space exceeds the natural-convection slope by a factor of
  approximately 1.5; these labels were then individually vetted.
- **Nine heuristic labels were overridden** when they fell outside the
  physically admissible interval
  $2 \le \Delta T_{\mathrm{ONB}} \le 30\;\mathrm{K}$
  or violated the Hsu envelope; in each case the manual label was
  preserved.  The `notes` column records each such intervention.

---

## 10. Reproducing the dataset

The two CSVs in this directory can be regenerated end-to-end from the
WPD project files via:

```bash
cd 02_data/scripts
python build_dataset.py \
    --raw-root ../raw/literature \
    --surface-cards ../surface_cards \
    --out ../processed
```

The script is deterministic given a fixed `_index.md` and a fixed set of
WPD project files. Differences between the regenerated CSVs and the
released CSVs indicate either (a) updates to the WPD projects or
(b) a non-deterministic pandas version mismatch; the
`requirements.txt` in the source repository pins exact versions.

---

## 11. Known limitations

1. **Sample size.** 82 ONB labels remain small for a deep-learning task;
   PINN physics constraints are what keep training tractable. See
   Section 6 of the paper and the Phase 2 follow-up plan for the
   strategy to expand toward $\sim 130$ labels.
2. **Single-pressure dominance.** All water entries are at near-
   atmospheric pressure; only the refrigerant subset of JABARDO_2009
   provides pressure variation (reduced pressures
   $p_r \approx 0.06$–$0.26$).  Generalization above $p_r \approx 0.3$
   has not been validated.
3. **Roughness reporting heterogeneity.** Some sources report $R_a$,
   others $S_a$ or banded ranges. The surface-card YAML preserves the
   original metric in `roughness.source_type`; downstream models treat
   all values as a representative roughness scalar.
4. **Contact-angle reporting heterogeneity.** Some sources report
   static, others advancing, others a range. The card preserves the
   detail in `contact_angle.notes`.
5. **Heater geometry simplification.** All curated entries are
   flat-plate or large-cylinder pool boiling consistent with a 1D
   conduction treatment; small-wire and small-cylinder data were
   excluded at the selection step.

---

## 12. Citation

If you use this dataset in your work, please cite **both** the dataset
and the associated paper, and additionally cite the primary
experimental sources that contributed the rows you used (the mapping
appears in § 5 above and in the `source_paper` column).

```bibtex
@dataset{lee2026pinn_onb_data,
  author    = {Lee, Jaeseon and Kim, Gyuchang and Ko, Eunjeong and Kim, Yujin},
  title     = {PINN-ONB01 pool-boiling ONB dataset (v1.0)},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.XXXXXXX},
  url       = {https://doi.org/10.5281/zenodo.XXXXXXX}
}

@article{lee2026pinn_onb,
  author  = {Lee, Jaeseon and Kim, Gyuchang and Ko, Eunjeong and Kim, Yujin},
  title   = {Surface-Conditioned Physics-Informed Neural Network for
             Pool-Boiling Onset of Nucleate Boiling},
  journal = {International Journal of Heat and Mass Transfer},
  year    = {2026},
  doi     = {10.1016/j.ijheatmasstransfer.2026.XXXXXX}
}
```

---

## 13. License and disclaimer

This dataset is released under
[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/). See
[`../../LICENSE-DATA`](../../LICENSE-DATA) for the full text and
attribution requirement.

**Disclaimer.** The dataset is provided "AS IS" without warranty of any
kind. Numerical values are accurate only to the digitization tolerance
documented in the per-paper digitization metadata. Users should
re-validate any value that drives a safety-critical engineering
decision against the original published figure.

---

## 14. Changelog

| Version | Date | Notes |
|---|---|---|
| 1.0 | 2026-XX-XX (upon acceptance) | Initial public release accompanying Lee et al. (2026). 1361 curve points, 82 ONB labels, 49 surface cards. |

---

## 15. Contact and contributions

- **Bug reports and dataset issues:** open a GitHub issue at
  <https://github.com/UNIST-ITEL/pinn-onb01/issues> with the label
  `dataset`.
- **New surface cards / additional digitizations:** see
  `CONTRIBUTING.md` in the source repository for the surface-card
  schema and the WPD project naming convention.
- **Direct contact:** Jaeseon Lee `<JaeseonLee@unist.ac.kr>`.
