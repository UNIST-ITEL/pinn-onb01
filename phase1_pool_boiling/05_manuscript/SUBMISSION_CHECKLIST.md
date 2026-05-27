# IJHMT Submission Checklist — PINN-ONB01

**Manuscript:** Surface-Conditioned Physics-Informed Neural Network for Pool-Boiling Onset of Nucleate Boiling
**Target journal:** International Journal of Heat and Mass Transfer (Elsevier)
**Corresponding author:** Jaeseon Lee (UNIST), JaeseonLee@unist.ac.kr
**ORCID (corresponding):** 0000-0003-1996-6086
**Prepared:** 2026-05-18 (revised)

---

## 1. Manuscript files

| Item | File | Status |
|---|---|---|
| Main manuscript LaTeX | `main.tex` | ✅ |
| Main manuscript PDF | `main.pdf` (36 pages, 1.5 MB) | ✅ |
| Bibliography | `references.bib` (31 entries, all CrossRef-verified) | ✅ |
| Graphical abstract | `figures/graphical_abstract.{png,pdf,eps}` (16×5.5 cm, 300 dpi) | ✅ |
| BibTeX-style file | elsarticle-num-names (built-in) | ✅ |
| Section files | `sections/0_abstract.tex`, `0_highlights.tex`, `0_nomenclature.tex`, `1`–`6_*.tex` | ✅ |
| Class file | elsarticle (Elsevier-supplied) | ✅ |

## 2. Frontmatter

| Item | Status | Note |
|---|---|---|
| Title | ✅ | "Surface-Conditioned Physics-Informed Neural Network for Pool-Boiling Onset of Nucleate Boiling" |
| Authors (4) | ✅ | Jaeseon Lee*, Gyuchang Kim, Eunjeong Ko, Yujin Kim |
| Corresponding author | ✅ | Jaeseon Lee (UNIST) — `\corref{cor1}` |
| Affiliation | ✅ | Innovative Thermal Engineering Lab, UNIST |
| Email + Tel + Fax | ✅ | JaeseonLee@unist.ac.kr / +82-52-217-2342 / +82-52-217-2419 |
| ORCID (corresponding) | ✅ | 0000-0003-1996-6086 (Jaeseon Lee) |
| ORCID (Gyuchang Kim) | ⚠️ | TBD — collect before portal entry |
| ORCID (Eunjeong Ko) | ⚠️ | TBD — collect before portal entry |
| ORCID (Yujin Kim) | ⚠️ | TBD — collect before portal entry |
| Highlights (5 bullets, ≤85 chars each) | ✅ | All 5 within limit |
| Abstract (200–250 words) | ✅ | 248 words |
| Keywords (4–6) | ✅ | 5 keywords |
| Nomenclature | ✅ | Roman 34 + Greek 17 + Abbrev. 20 |

## 3. Body content

| Item | Status | Note |
|---|---|---|
| §1 Introduction | ✅ | 972 words, recent PINN-boiling literature (Jalili 2025, Li-Kharangate 2025, Huang 2024) cited |
| §2 Mathematical Formulation | ✅ | 855 words, Biot-number argument for 1D added |
| §3 Data and Surface Characterization | ✅ | 933 words, FC-77 exclusion academically defended |
| §4 PINN Architecture and Training | ✅ | 1,373 words, "physics-regularized regressor" philosophy stated |
| §5 Results and Discussion | ✅ | 2,718 words, Simpson's paradox thermodynamic mechanism added |
| §6 Conclusions and Future Work | ✅ | 520 words |
| Total body word count | ✅ | ~7,371 words (IJHMT typical 6,000-8,000) |
| Acknowledgements | ✅ | NRF + KETEP grants |
| CRediT author contributions | ✅ | 4 authors, roles per CRediT taxonomy |
| Data availability statement | ✅ | Open-source release upon acceptance |
| Declaration of competing interests | ✅ | None declared |
| References | ✅ | 31 entries, all DOI/URL present |

## 4. Figures

| Item | Status | Note |
|---|---|---|
| Main figures | ✅ | 9 figures (Fig. 1–9), filenames `fig01_*` … `fig09_*` match body numbering |
| Resolution | ✅ | All 300 dpi (PIL-verified) |
| Format — PDF | ✅ | 9/9 present (`05_manuscript/figures/*.pdf`) |
| Format — EPS | ⚠️ | 8/9 OK; `fig07_physics_trends_composite.eps` is 24 MB (raster-embedded PNG bitmaps). **Recommendation: submit PDF figures only.** |
| Format — PNG | ✅ | 9/9 present (review proofs) |
| Inline citations | ✅ | All 9 figures referenced via `\cref{fig:...}` in body |
| Caption style | ✅ | All start uppercase, end with period |
| Graphical abstract | ✅ | `graphical_abstract.{png,pdf,eps}` 16×5.5 cm, 300 dpi |

## 5. Tables

| Item | Status | Note |
|---|---|---|
| Main tables | ✅ | 6 tables (`tab:dataset`, `tab:level1`, `tab:forward`, `tab:per_fluid`, `tab:per_paper`, `tab:physics`, `tab:hyperparameters`) |
| Caption position | ✅ | Above tabular |
| Cross-referenced | ✅ | All cited via `\cref{tab:...}` |

## 6. Supplementary material

| Item | Status | Note |
|---|---|---|
| `supplementary.tex` | ✅ | ~290 lines, native-tone polished |
| `supplementary.pdf` | ✅ | 7 pages, 1.32 MB |
| Supp. figures | ✅ | 10 figures (S1–S10), `\textbf{...}` lead-in |
| Supp. tables | ✅ | 3 tables (S1 surface inventory, S2 HPO top-5 trials, S3 phase progression) |
| §S5 Hyperparameter optimization | ✅ | Optuna 30 trials summary + importance ranking |
| §S6 Model design progression | ✅ | Phase A→Dbal→E ablation-style table |
| Numbering scheme | ✅ | `\renewcommand{\thefigure}{S\arabic{figure}}` |
| References to main text | ✅ | Free prose ("released in the supplementary material") — Elsevier convention |

## 7. Cover letter

| Item | Status | Note |
|---|---|---|
| `cover_letter.tex` | ✅ | letter class, IJHMT format |
| `cover_letter.pdf` | ✅ | 2 pages, 89 KB |
| Letterhead with sender info | ✅ | UNIST address, email, tel |
| Addressed to Editor-in-Chief | ✅ | International Journal of Heat and Mass Transfer |
| 5 contributions listed | ✅ | Curated dataset, surface-conditioned PINN, 5-term loss, Hsu inverse, V&V |
| Novelty statement | ✅ | First combination of pool-boiling ONB + PINN + multi-fluid + inverse cavity |
| Non-duplicate publication declaration | ✅ | |
| Conflicts of interest declaration | ✅ | |
| Open-source release commitment | ✅ | |

## 8. Build / compile checks

| Item | Status | Note |
|---|---|---|
| `latexmk -pdf main.tex` | ✅ | 0 errors, 0 undefined references |
| `latexmk -pdf supplementary.tex` | ✅ | 0 errors |
| `pdflatex cover_letter.tex` | ✅ | 0 errors |
| BibTeX warnings | ⚠️ | 1 minor: `perez2018film` empty pages (AAAI 2018 online-only; intrinsic) |
| Overfull `\hbox` warnings | ⚠️ | 1 residual: §2 (~31 pt, cosmetic; emergencystretch=5em applied) |
| Undefined references | ✅ | 0 |
| Undefined citations | ✅ | 0 |

## 9. IJHMT-specific requirements

| Requirement | Status | Note |
|---|---|---|
| Elsevier `elsarticle` class | ✅ | review,1p,12pt,a4paper |
| Manuscript word count (typical 6,000–8,000) | ✅ | 7,371 words body |
| Highlights — 3–5 bullets, ≤85 chars | ✅ | 5 bullets, all within 85 |
| References style — Elsevier numerical names | ✅ | `\bibliographystyle{elsarticle-num-names}` |
| US English | ✅ | Native-tone passes confirmed |
| Author CRediT statement | ✅ | Included |
| Data availability statement | ✅ | Included |
| Declaration of competing interests | ✅ | Included |
| Graphical abstract | ✅ | Generated; can be uploaded as supplementary asset |

## 10. To do before clicking "Submit"

- [ ] Co-author ORCIDs (Gyuchang Kim, Eunjeong Ko, Yujin Kim) — collect and add to portal metadata
- [ ] Finalize the open-source dataset URL (GitHub / Zenodo / OSF) and update `Data availability` if URL ready
- [ ] Verify all author affiliations are current
- [ ] Confirm corresponding author's institutional email matches portal account
- [ ] Read each PDF (main + supplementary + cover letter) one last time
- [ ] Optional: Run a friendly co-author / advisor review
- [ ] Suggested reviewers (Elsevier portal asks 3–5; not in this checklist)
- [ ] Verify acknowledgement grant numbers with funding office
- [ ] Final commit + tag in git (`v1.0-submitted`)

## 11. Submission package contents (zip)

Assembled in `SUBMISSION/` folder:
1. `PINN-ONB01_main.pdf` — manuscript (36 pages, 1.5 MB)
2. `PINN-ONB01_supplementary.pdf` — supplementary material (7 pages, 1.3 MB)
3. `PINN-ONB01_cover_letter.pdf` — cover letter (2 pages, 138 KB)
4. `graphical_abstract.pdf` — graphical abstract (1 page, 80 KB)
5. `figures_pdf/fig01_*.pdf` … `fig09_*.pdf` — 9 high-resolution figures (300 dpi)
6. `PINN-ONB01_submission_20260518.zip` — packed bundle (3.7 MB)
7. `SUBMISSION_CHECKLIST.md` (this file) — internal reference (do not upload)

If the portal requests LaTeX source:
- `main.tex`, `sections/*.tex`, `references.bib`, `supplementary/supplementary.tex`
- Use Elsevier `elsarticle` class, `elsarticle-num-names` bib style

## 12. Post-submission tracking

| Task | Owner | Due |
|---|---|---|
| Monitor portal status (Editor decision) | Corresponding author | within 6–12 weeks |
| Prepare rebuttal letter (drawn from `04_analysis/reviewer_rebuttal.md`) | All authors | upon first decision |
| Optional 5 manuscript additions per Rebuttal Appendix B | All authors | upon major revision |
| Reference document: `04_analysis/reviewer_rebuttal.md` (20 anticipated questions, 35 KB) | Corresponding author | review pre-submission |
