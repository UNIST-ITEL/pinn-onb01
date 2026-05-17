# BibTeX Audit Report — references.bib
Date: 2026-05-14
Auditor: bibtex-curator agent (Claude Sonnet 4.6)

---

## Summary

| Metric | Value |
|--------|-------|
| Total entries (final) | 28 |
| DOI verified (CrossRef) | 21 |
| PASS (no change needed) | 17 |
| FIXED | 5 |
| URL-only / no DOI | 3 (`lakshminarayanan2017`, `kingma2014adam`, `zuber1959`) |
| New entry added | 1 (`paszke2019pytorch`) |
| Citation key case fixes in .tex | 3 (`Basu2002`, `Jones2009`, `Lakshminarayanan2017` → lowercase) |
| Backup | `references.bib.bak` |

---

## Per-Entry Verification Results

### Classical ONB correlations

| Key | DOI status | Changes |
|-----|------------|---------|
| `hsu1962` | PASS | Author expanded to full given name already correct; publisher added (ASME International) |
| `davis1966` | PASS | Title case normalized to sentence case; publisher added (Wiley) |
| `bergles1964` | PASS | publisher added (ASME International) |
| `sato1964` | FIXED | Author names updated from initials to full names: `Sato, Takashi` and `Matsumura, Hirohisa` (CrossRef canonical); publisher added |
| `basu2002` | FIXED | Author full names updated: `Basu, Nilanjana`, `Warrier, Gopinath R.`, `Dhir, Vijay K.`; title word "During" capitalized; publisher added |

### Surface modification sources

| Key | DOI status | Changes |
|-----|------------|---------|
| `betz2013` | FIXED | Author given name corrected: `Kim, Chang-Jin` (CrossRef: `Chang-Jin "CJ"`); publisher added |
| `bourdon2012` | PASS | publisher added (ACS) |
| `bourdon2015` | PASS | `number` field removed (issue not present in CrossRef record); publisher added |
| `phan2009` | FIXED | Author given names updated to full forms: `Phan, Hai Trieu`, `Caney, Nadia`, etc.; LaTeX escape added for `{\'e}` and `{\^o}`; publisher added |
| `jo2011` | FIXED | Author given names updated to full forms: `Jo, HangJin`, `Ahn, Ho Seon`, etc.; publisher added |
| `jones2009` | FIXED | `pages` field retained as article number `121009` (CrossRef has no page range, only `article-number: 121009`); publisher added |
| `jabardo2009` | FIXED | Author full names updated: `Jabardo, Jos{\'e} M. Saiz`, `Ribatski, Gherhardt`, `Stelute, Elvio`; LaTeX escape added; publisher added |

### PINN and ML for heat transfer

| Key | DOI status | Changes |
|-----|------------|---------|
| `raissi2019` | PASS | Author initials retained (CrossRef records them as `M.`, `P.`, `G.E.`); publisher added |
| `lu2021` | PASS | Author full names updated from CrossRef; publisher added |
| `cai2021` | FIXED | `number` field added (`12`); full author names from CrossRef; publisher added |
| `zobeiry2021` | PASS | Full author names; publisher added |
| `hobold2018` | **CRITICAL FIX** | **Old DOI `10.1016/j.ijheatmasstransfer.2018.12.181` was incorrect — pointed to an ice accretion paper (Gao et al., 2019).** Corrected to `10.1016/j.ijheatmasstransfer.2018.12.170` (Hobold & da Silva, "Visualization-based nucleate boiling heat flux quantification using machine learning", IJHMT 134, 511-520, 2019). Year corrected from 2018 to 2019. |

### Deep learning methods

| Key | DOI status | Changes |
|-----|------------|---------|
| `lakshminarayanan2017` | UNVERIFIED (NeurIPS proceedings, no CrossRef DOI) | Full author given names added; URL retained |
| `perez2018film` | PASS | Full author names from CrossRef; journal field corrected to "Proceedings of the AAAI Conference on Artificial Intelligence"; `volume=32`, `number=1` added; publisher added |
| `kingma2014adam` | UNVERIFIED (ICLR, no CrossRef DOI) | Full author names added: `Kingma, Diederik P.` and `Ba, Jimmy`; `note` field with arXiv number added |
| `liu1989lbfgs` | PASS | Full author names from CrossRef: `Liu, Dong C.` and `Nocedal, Jorge`; publisher added |
| `mckay1979lhs` | PASS | publisher added (Informa UK Limited) |
| `paszke2019pytorch` | **NEW ENTRY** | Added to bib; was cited in `4_architecture.tex` as `\citealp{paszke2019pytorch}` but was missing from bib. NeurIPS 2019 proceedings; URL to proceedings page. No CrossRef DOI found. |

### Textbooks and tools

| Key | DOI status | Changes |
|-----|------------|---------|
| `incropera` | N/A (book) | Full author names expanded; `address` field added |
| `lienhard1981` | N/A (book) | Full author names corrected: `Lienhard, John H., IV` and `Lienhard, John H., V`; publisher corrected to `Phlogiston Press`; `address` field added |
| `zuber1959` | UNVERIFIED (OSTI tech report) | Entry type changed from `@article` to `@techreport`; `institution`, `number` fields added; `journal` field removed |
| `rohatgi_wpd` | N/A (misc) | Author full first name added: `Rohatgi, Ankit` |

### Statistics

| Key | DOI status | Changes |
|-----|------------|---------|
| `simpson1951` | PASS | Journal name updated to canonical CrossRef form: "Journal of the Royal Statistical Society: Series B (Statistical Methodology)"; publisher added |

---

## Citation Key Case Fixes (in .tex files)

Three citation keys in `05_manuscript/sections/5_3_ensemble_uq.tex` used incorrect upper-case forms:

| File | Old key | Corrected to |
|------|---------|-------------|
| `5_3_ensemble_uq.tex` line 22 | `Lakshminarayanan2017` | `lakshminarayanan2017` |
| `5_3_ensemble_uq.tex` line 59 | `Basu2002` | `basu2002` |
| `5_3_ensemble_uq.tex` line 59 | `Jones2009` | `jones2009` |

---

## Key Counts (Final State)

- Bib entries: **28**
- Tex citation keys (unique): **28**
- Unmatched (missing from bib): **0**
- Unused (in bib but not cited): **0**

---

## Additional Recommendations

1. **`hobold2018` year mismatch**: The key name says "2018" but the paper was published online in 2019 (received 2018, available 2019). The key has been kept as `hobold2018` for consistency with existing .tex citations, but the `year` field is corrected to `2019`.

2. **`jones2009` pages field**: CrossRef reports only `article-number: 121009` with no page range. The `pages = {121009}` entry reflects this ASME article-number format, which is the standard citation practice for ASME Trans. post-2009.

3. **`zuber1959` DOI**: No DOI is registered for this 1959 AEC technical report. The OSTI URL (`https://www.osti.gov/biblio/4175511`) is the canonical public access point. An alternative published version exists (Zuber, N., Trans. ASME 80, 711-720, 1958) but that paper addresses nucleate boiling mechanism more broadly; the tech report is the correct source for the CHF hydrodynamic theory and non-dimensional scales cited in Section 2.4.

4. **`kingma2014adam` and `lakshminarayanan2017`**: Neither paper has a CrossRef DOI (ICLR and NeurIPS proceedings respectively were not registered with CrossRef for those years). The arXiv URL for Kingma and the NeurIPS proceedings URL for Lakshminarayanan are the best available stable identifiers.

5. **`paszke2019pytorch`**: This entry was missing from the bib file despite being cited in `4_architecture.tex`. It has been added. The NeurIPS 2019 proceedings paper does not have a CrossRef DOI; the proceedings URL is used.

6. **Future entries to consider**: If a pressure-dependent ONB correlation (e.g., Rohsenow 1952) or a CHF correlation (Zuber 1958 Trans. ASME) is cited in the revised manuscript, entries should be added following the same `{firstauthor}{year}{firstword}` key convention.
