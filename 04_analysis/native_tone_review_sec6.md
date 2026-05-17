# Section 6 (Conclusions) — Native English Tone Review

**Reviewer role**: Senior native English editor (IJHMT-equivalent journal)
**File reviewed**: `05_manuscript/sections/6_conclusions.tex`
**Date**: 2026-05-17
**Method**: section-drafter agent (B7 pass) — diagnostic, no edits applied

---

## Findings (12 substantive items)

### 1. Opening sentence — verb choice and self-reference reads slightly off
**Location**: Line 13 — *"This study delivered the five contributions of \cref{subsec:intro_contributions}."*
**Issue**: "Delivered" is acceptable but mildly commercial-sounding; the construction "the five contributions of [section]" reads as if the contributions belong to the cross-reference rather than to the study. Native usage would attach the cross-reference to the verb or place it parenthetically.
**Suggested revision**: *"This study realized the five contributions outlined in \cref{subsec:intro_contributions}."* or *"We have realized the five contributions set out in \cref{subsec:intro_contributions}."* "Realized", "delivered on", or "addressed" all read more naturally than the bare "delivered the contributions of X" pattern.

---

### 2. Tense control across the contribution paragraph
**Location**: Lines 14-24 — repeated past simple ("We curated... We built... We trained... An inverse study revealed... A three-level verification protocol covered...")
**Issue**: The chain of five past-simple sentences with parallel "We + verbed" starts in the active voice and then quietly switches to inanimate subjects ("An inverse $r_c$ study revealed", "A three-level verification protocol covered"). The register shift dilutes the agentive opening. In a Summary subsection, IJHMT-style writing typically maintains present perfect for the authors' actions ("We have curated... and have built..."), which signals that the contributions persist beyond the study.
**Suggested fix**: Either (a) move the whole block to present perfect for consistency, or (b) keep past simple but reintroduce "We" for the last two sentences: *"We performed an inverse $r_c$ study over 48 surfaces, which revealed..."* and *"We adopted a three-level verification protocol covering..."*.

---

### 3. "Combining... and FiLM modulation" — parallel-list noun-form mismatch
**Location**: Lines 17-19 — *"a surface-conditioned PINN with $24\,005$ parameters, combining a nine-channel encoder, a ten-vocabulary categorical embedding, and FiLM modulation."*
**Issue**: The three list items mix concrete artifacts ("encoder", "embedding") with an operation ("modulation"). A native ear hears the third item as a category mismatch.
**Suggested revision**: *"...combining a nine-channel encoder, a ten-token categorical embedding, and a FiLM modulation layer."* Adding "layer" restores parallel noun structure. Also, "ten-vocabulary" is awkward — "ten-token" or "ten-entry vocabulary" is more idiomatic.

---

### 4. "fusing" is too informal and overlapping with "combining"
**Location**: Lines 19-22 — *"We trained the network with a five-term composite loss fusing the conduction residual, the natural-convection BC, the ONB data, a soft Hsu prior, and $R_a$/$\theta$ monotonicity regularizers."*
**Issue**: "Fusing" implies physical melding and is increasingly seen as a slightly hyped ML buzzword. After "combining" in the previous sentence, the repetition of merger verbs feels stylistically thin. Also, "the ONB data" should be "an ONB data term" because the other four list items are themselves loss terms, not the data itself.
**Suggested revision**: *"We trained the network with a five-term composite loss comprising the conduction residual, the natural-convection BC, an ONB data term, a soft Hsu prior, and $R_a$/$\theta$ monotonicity regularizers."*

---

### 5. "exceeded the overall improvement" — vague comparative
**Location**: Line 34 — *"Refrigerant subsets exceeded the overall improvement."*
**Issue**: This is the most awkward sentence in the section. "Subsets" cannot literally "exceed" an "improvement" — the subjects and metrics do not match. The intent is that the improvement *measured on* refrigerant subsets exceeded the improvement on the full set.
**Suggested revision**: *"Refrigerants benefited disproportionately."* or *"The improvement was larger on refrigerant subsets than on the full set."*

---

### 6. "against \SI{46}{\percent} on water" — preposition choice
**Location**: Lines 35-36 — *"reached \SIrange{65}{67}{\percent} ... against \SI{46}{\percent} on water."*
**Issue**: "Against" for numerical comparisons is acceptable but slightly British/financial in register. "Compared with" or "versus" is more neutral for IJHMT, and the parallel construction would also benefit.
**Suggested revision**: *"...reached \SIrange{65}{67}{\percent} (\SI{1.18}{K} and \SI{2.35}{K}, respectively), compared with \SI{46}{\percent} for water."* Note the added "respectively" disambiguates the numeric pairing.

---

### 7. "with $60\%$ of $48$ surfaces inside $[1,100]\,\si{\micro\meter}$" — register slip
**Location**: Lines 38-40
**Issue**: Two minor issues here. (a) Using a bare percent sign `60\%` while the rest of the section uses `\SI{...}{\percent}` is inconsistent. (b) "Inside" a numerical interval is loose; native technical English prefers "within".
**Suggested revision**: *"...with \SI{60}{\percent} of the 48 surfaces falling within $[1,100]\,\si{\micro\meter}$."*

---

### 8. "Fluid stratification exposed a sign reversal" — verb choice
**Location**: Lines 40-42 — *"Fluid stratification exposed a sign reversal from $\rho=-0.27$ overall to $+0.30$ (water) and $-0.77$ (R-134a)."*
**Issue**: "Exposed" carries a connotation of revealing a hidden flaw, which over-dramatises the finding. "Revealed" is the standard neutral verb. Also, "stratification" is fine but "stratifying by fluid" is more idiomatic when describing an analytical choice.
**Suggested revision**: *"Stratifying by fluid revealed a sign reversal, from $\rho=-0.27$ overall to $+0.30$ on water and $-0.77$ on R-134a."* The prepositions "on water/on R-134a" match the earlier "on water" usage.

---

### 9. "Many surfaces carry only a single ONB observation" — verb register
**Location**: Lines 52-53
**Issue**: "Carry" with surfaces as subject is metaphorical and reads slightly journalistic. Technical writing prefers "have" or a passive construction.
**Suggested revision**: *"Many surfaces have only a single ONB observation, so within-surface $q''$ dependence must be learned through the Hsu prior."* Adding "must be" sharpens the necessity argument.

---

### 10. "not exposed by CoolProp" — preposition and phrasing
**Location**: Lines 53-54 — *"FC-77 was excluded as not exposed by CoolProp."*
**Issue**: "Exposed by" is unidiomatic in a software/library context — APIs *expose* functions, but properties are not "exposed by" the library to the user; they are "supported by" or "available in" the library. Also, "excluded as not..." is elliptical and reads as a clipped note.
**Suggested revision**: *"FC-77 was excluded because its properties are not available in CoolProp."* or *"...because CoolProp does not provide FC-77 property data."*

---

### 11. "Four trajectories are envisaged" — register and word choice
**Location**: Line 65
**Issue**: "Envisaged" is correct British English but slightly old-fashioned, and "trajectories" for research directions is overblown. The standard IJHMT phrasing is "Four directions are pursued/planned" or "We identify four directions for future work."
**Suggested revision**: *"We identify four directions for future work."* This also restores the agentive voice, which is welcome at the start of a forward-looking subsection.

---

### 12. Closing remarks — verb tense and "may" register
**Location**: Lines 82-85 — *"The dataset, trained ensemble, and training/evaluation scripts are released under an open-source license. They provide a reproducible baseline against which future ONB studies may be benchmarked on common ground."*
**Issue**: (a) Two small things in the second sentence: "against which... may be benchmarked" is grammatically fine but "may" weakens what should be an inviting closing statement. (b) "On common ground" is a colloquialism rarely used in technical conclusions.
**Suggested revision**: *"The dataset, trained ensemble, and training/evaluation scripts have been released under an open-source license, providing a reproducible baseline for future ONB studies."* This tightens two sentences into one, removes the colloquialism, and switches "are released" to present perfect, which is the standard tense for archival actions whose effects persist.

---

## Overall impression

Section 6 is concise (509 words), well structured into five clearly labeled subsections, and free of the most common ESL pitfalls (article slips, dangling modifiers, comma splices). The numerical reporting is tight and accurate, and the limitations and future-work paragraphs strike a reasonable balance between candor and ambition.

The principal weaknesses are stylistic rather than grammatical. Three patterns recur. First, several verbs are slightly over-dramatic for a Conclusions section ("delivered", "fusing", "exposed", "envisaged"), and softer, more standard verbs would read as more confident. Second, the agentive "We" opens the Summary paragraph but is then dropped in favor of inanimate subjects, producing a register wobble that is easily fixed. Third, two sentences (items 5 and 10) have subject–predicate mismatches that a native reader will flag immediately as awkward, even though their meaning is recoverable.

No item rises to a substantive content concern, and the quantitative reporting is clean. The section would pass review after light copy-editing.

## Strengths

- Quantitative results are reported with appropriate precision and consistent units, and the percent-improvement framing against the strongest baseline (rather than a cherry-picked weak baseline) projects scientific honesty.
- The Limitations subsection is unusually candid — explicitly acknowledging the PDE-residual / regression trade-off and the absence of co-located SEM/AFM ground truth is the kind of honesty IJHMT reviewers reward.
- The Future Work paragraph is concrete, with numbered trajectories tied to measurable targets (5–10 surfaces, +50 ONB labels, 1D-to-2D promotion). Vague aspirations are avoided.
- The closing remark on open-source release is a strong note to end on, even with the suggested tightening.
- The section avoids the standard Conclusions cliches: no "In conclusion", no "It is worth noting", no "We have shown definitively". Hedging ("may be benchmarked", "is acknowledged") is calibrated rather than excessive.
