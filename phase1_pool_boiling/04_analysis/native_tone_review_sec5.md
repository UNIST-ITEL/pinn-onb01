# Section 5 (Results and Discussion) — Native English Tone Review

**Reviewer role**: Senior native English editor (IJHMT-equivalent journal)
**File reviewed**: `05_manuscript/sections/5_results_discussion.tex`
**Date**: 2026-05-17
**Method**: section-drafter agent (B7 pass) — diagnostic, no edits applied

---

## Findings (22 substantive items, grouped by subsection)

### Section opener (lines 10-18)

#### 1. Repetitive "Section X reports/presents/addresses…" cascade (line 10-18)
The five-sentence preamble reads as a mechanical roll call: "reports", "reports", "presents", "addresses", "treats", "collects". Native style alternates verbs and uses parallel infinitive forms, e.g., "Section 5.2 evaluates forward $\Delta T_{\mathrm{ONB}}$ predictions against five classical correlations; Section 5.3 develops a deep-ensemble UQ analysis; Section 5.4 audits physical-trend consistency; Section 5.5 addresses…". The word "treats" in particular is unusual register for results sections.

#### 2. "in increasing physical scope" — vague claim (line 10)
The phrase suggests a deliberate ordering, but code verification (5.1) is a methodology check and does not lie on the same "scope" axis as the inverse problem. Either delete the qualifier or replace with "in the order followed in the rest of the paper".

---

### Subsection 5.1: Code verification (Level 1)

#### 3. "The numerical infrastructure was verified" — vague subject (line 24)
"Infrastructure" is a project-management word, not a technical noun in the verification literature. Native phrasing would be "The numerical implementation" or "The solver and its autograd backbone were verified". Also, "infrastructure" implies a broader system than what was actually tested (four small problems).

#### 4. "All four passed" — fragmented from preceding sentence (line 25)
A native editor would join: "All four tests passed (Table 1, Fig. 1)." Alternatively, "All four reference cases were reproduced to within…" gives a more quantitative opening. The bare "All four passed" reads like a checkbox status.

#### 5. Inconsistent ordinal labelling: "Test (i)" through "Test (iv)" (lines 27-37)
Roman numerals in parentheses are acceptable but unusual for IJHMT, which typically uses "Test 1" or numbered list items. More important, the four sentences all open with "Test (i) is…", "Test (ii) verifies…", "Test (iii) compares…", "Test (iv) checks…" — the parallel verbs differ (one is a copula, three are active), which makes the paragraph feel uneven. Use consistent verb pattern: "Test 1 reproduces…; Test 2 confirms…; Test 3 reproduces…; Test 4 verifies…".

#### 6. "with closed-form or correlation references" — awkward noun stacking (line 25)
"Correlation references" is opaque. Suggested rewrite: "with closed-form solutions or established correlations as references".

---

### Subsection 5.2: Forward prediction

#### 7. "evaluate on" vs. "are evaluated on" — verb-form inconsistency (lines 81-84)
Lines 82-84 alternate active and passive in close proximity: "Five classical correlations… are evaluated on the FC-77-excluded subset… Bergles–Rohsenow and Basu are valid only for water… and evaluate on smaller subsets, whereas the PINN evaluates on the full 77". The active "evaluates on" treats the model as the agent of its own assessment, which is wrong — the authors evaluate the model on a subset. Recommended: "are evaluated on" throughout, or recast as "we evaluated".

#### 8. Headline number-then-percent pattern repeated three times in one paragraph (lines 109-112)
"reduces RMSE from \SI{7.21}{K} … to \SI{3.42}{K}, a $52.6\%$ reduction. MAE falls from \SI{5.85}{K} to \SI{2.21}{K}, and $R^2$ shifts from negative to $+0.44$, while MRE drops from above $95\%$ … to $61.4\%$." Three "from X to Y" structures in adjacent sentences. Vary the framing: "MAE falls to \SI{2.21}{K} (from \SI{5.85}{K})"; "the coefficient of determination becomes positive ($R^2=+0.44$) for the first time"; "the mean relative error contracts to $61.4\%$".

#### 9. "act as a single-fluid constant" — opaque idiom (line 114)
A "single-fluid constant" is not a standard term. The intended meaning seems to be "does not collapse to a fluid-averaged constant". Recommended: "the model does not reduce to a single-fluid offset" or "the prediction is not a per-fluid constant".

#### 10. "The comparison is conservative for two reasons" — register slippage (lines 115-117)
"Conservative" in this construction is journalistic. In statistics/ML "conservative" usually means an upper bound; here you mean the comparison understates the PINN advantage. Suggested: "Two factors bias the comparison against the PINN. First, classical correlations are evaluated only on their natively valid subset. Second, the PINN is evaluated on the full $n=77$ corpus, including the more challenging refrigerants, with the test partition held out from training."

#### 11. "with the test partition unseen during weight updates" — redundancy with "held out" (line 119)
"Unseen during weight updates" is a wordy synonym for "held out". Replace with "and on held-out points only".

#### 12. "PINN error is unevenly distributed" — preposition gap (line 143)
Idiomatic: "PINN error is unevenly distributed *across fluids*". Without the prepositional phrase the reader does not know the dimension of variation.

#### 13. "whose uniform fabrication is absorbed more effectively by the encoder" — anthropomorphism + passive (line 150)
"Whose uniform fabrication is absorbed" is awkward — fabrication is not the thing absorbed; the encoder absorbs the *variance* (or lack of it). Recommended: "from a single laboratory whose homogeneous fabrication route is more easily captured by the encoder".

#### 14. "degrades gracefully" — borderline jargon (line 175)
This is acceptable ML idiom but slightly informal for IJHMT. Consider "degrades smoothly" or "degrades in proportion to the per-source sample size".

#### 15. "the tuned balance prevents the sparse ONB loss from being drowned out by the PDE residual" — colloquial verb (line 207-208)
"Drowned out" is conversational. Use "from being overwhelmed by" or "from being dominated by".

#### 16. "$3.5\times$ broader scope" — unit mismatch (line 221)
A "broader scope" is qualitative; coupling it to a multiplicative number reads strangely. Recommended: "extends the valid envelope from $n=22$ to $n=77$, $3.5\times$ more test points" or "a $3.5\times$ increase in the size of the evaluable test set".

---

### Subsection 5.3: Uncertainty quantification

#### 17. "A deterministic network provides no intrinsic confidence measure" — bald opening (line 237)
Opens 5.3 without transition. Native editors prefer either a one-clause transition or a more specific opening tied to the previous paragraph. Suggested: "The forward errors in Section 5.2 are point predictions; they carry no confidence interval. To quantify prediction uncertainty we used the deep-ensemble approach of \citet{lakshminarayanan2017}."

#### 18. "Only weight initialization differed" — sentence fragment in spirit (line 245)
The sentence is grammatical but very short and ends abruptly between two longer sentences. Either fold into the preceding sentence ("…on the identical 77-point dataset, differing only in weight initialization.") or expand ("Only the random seed for weight initialization differed across the $K=10$ instances.").

#### 19. "consistent with the $\pm 20\%$ ONB repeatability typically reported" — needs hedging fix (line 255)
"Typically reported" is informal. Use "commonly reported in the literature" or, more precisely, "consistent with the $\pm 20\%$ run-to-run scatter reported for ONB measurements".

#### 20. "Intervals are sufficient and locally conservative" — undefined adjectives (line 263)
"Sufficient" for what? "Locally conservative" is not a standard UQ term. Recommended: "The intervals therefore over-cover the data slightly, which is acceptable for the engineering use of the model." Or, if you mean coverage > nominal: "The empirical coverage exceeds the nominal $95\%$, indicating a small but conservative bias in the intervals."

#### 21. "Epistemic dominates by $\sim 2.9\times$ aleatoric" — missing preposition and awkward comparison (line 285)
Should be "Epistemic uncertainty dominates aleatoric by a factor of $\sim 2.9$" or "exceeds the aleatoric component by a factor of 2.9". The current phrasing reads as if "aleatoric" were the unit.

#### 22. "Additional data, not precision improvement, is therefore the efficient route" — number agreement (line 287)
With a compound subject of the form "X, not Y", the verb agrees with X: "Additional data are…" ("data" plural in formal scientific register, especially IJHMT). Also "efficient route to reducing total uncertainty" is fine but pairs awkwardly with "Additional data are"; consider "Additional measurements, rather than tighter optimisation, are therefore the most efficient route to reducing total uncertainty."

#### 23. "two-three measurements above" — informal hyphenation (line 320)
"Two-three" is colloquial. Use "two or three measurements above $\SI{200}{kW/m^2}$".

---

### Subsection 5.4: Physical consistency tests

#### 24. "The trained model was subjected to a Level 3 consistency battery" — heavy noun phrase (line 330)
"Was subjected to a consistency battery" reads as forensic language. Native phrasing: "We audited the trained model with a Level 3 battery of physical-consistency tests" or "The trained model was evaluated against a Level 3 consistency battery".

#### 25. "the qualitative physics has been internalised" — verb choice + UK spelling (line 335)
"Internalised" is anthropomorphic and the spelling is British (note: CLAUDE.md mandates US English — should be "internalized" if retained). Better: "the model reproduces the qualitative physics" or "the dominant physical trends have been learned correctly".

#### 26. "Earlier checkpoints showed a sign-flip artefact" — UK spelling (line 369)
"Artefact" should be "artifact" under US English convention.

#### 27. "$R_a$ and $\theta$ are weakly anti-correlated across sources" — minor article issue (line 376)
Fine, but the immediately following clause ("but the encoder sees both descriptors independently") uses "sees", which is anthropomorphic. Suggest "the encoder receives both descriptors as independent inputs".

#### 28. "PDE residual on a dense interior grid is $\sim 0.36$" — missing units (line 404)
The bracketed clarification "(non-dimensional)" arrives on the next line. Native style integrates: "is approximately $0.36$ in non-dimensional units". Avoid splitting the qualifier across sentences.

---

### Subsection 5.5: Inverse problem

#### 29. "The framework can be used in inverse mode" — vague + redundant (line 419)
"Can be used in inverse mode" mixes engineering register with ML jargon. Native phrasing: "The framework also supports inverse use: given an ONB observation, it can recover a per-surface cavity radius $r_c$. The main inverse result is the Hsu-based analytical inverse; a PINN-augmented variant is reported as supplementary."

#### 30. "Sixty percent of surfaces fall within the canonical $1$–$\SI{100}{\micro\meter}$ band" (line 431)
Mixing spelled-out "Sixty percent" with later numerical "$40\%$" is inconsistent. IJHMT prefers numerals with the percent symbol throughout: "$60\%$ of surfaces fall…".

#### 31. "This naively implies" — register slip (line 440)
"Naively" is fine in some venues but mildly editorial. Replace with "On its face this would imply" or "Read at face value, this suggests…".

#### 32. "These match SEM-reported features where available" — under-evidenced claim (line 465)
"Match" is strong; without quantitative comparison or a citation it reads as hand-waving. Suggested: "These are within an order of magnitude of SEM-reported feature sizes where such measurements are available (Table/citation)." If no citation exists, soften to "consistent with the order of magnitude reported for the corresponding SEM features".

#### 33. "stuck at initialization" — informal phrasing (line 483)
"Stuck at initialization" is appropriate in a lab notebook but informal for a journal. Recommended: "remained at the initial value" or "did not move from initialisation, indicating insensitivity of the forward model to $r_c$ in this regime".

#### 34. "is a waypoint toward future work" — metaphor mismatch (line 487)
"Waypoint" is navigational and unusual here. Use "represents a preliminary step toward future work that will use experimentally measured cavity distributions as hard labels".

---

### Subsection 5.6: Limitations

#### 35. "Four limitations deserve attention" — anthropomorphic opener (line 493)
"Deserve attention" is unusual. Native style: "Four limitations remain" or "We note four limitations of the present study".

#### 36. "Distribution is uneven" — missing article (line 500)
"The distribution is uneven (…)" reads better. Bare nouns without articles in the abstract sense ("Distribution") are a non-native tic.

#### 37. "co-located SEM" — abbreviation expansion (line 513)
"Co-located SEM measurements" — first appearance of SEM in this subsection is bare. Consider "co-located scanning electron microscopy (SEM) of the boiling surfaces".

---

## Overall impression

Section 5 is technically dense and well structured. The six subsections are clearly delineated, the tables and figures are properly cross-referenced, and the quantitative claims are paired with appropriate hedging where uncertainty is present. The principal weaknesses are stylistic rather than substantive: (i) a tendency toward anthropomorphic language ("the encoder sees", "internalised", "qualitative physics has been internalised"); (ii) recurrent informal idioms ("stuck at initialization", "drowned out", "two-three measurements", "waypoint"); (iii) two UK-spelled words in a US-spelling manuscript; (iv) inconsistent voice and tense across closely paired sentences in 5.2; and (v) several places where additional prepositions or articles would smooth a non-native phrasing into idiomatic English. None of these are blockers for submission, but they collectively give the section a slightly uneven register that an IJHMT copy editor would flag.

## Strengths

- Numerical claims are uniformly precise and paired with sample sizes; the per-fluid and per-paper breakdowns model best practice for honest reporting.
- The Simpson's paradox subsection is conceptually clear and correctly identifies confounding without overclaiming.
- The Limitations subsection is appropriately self-critical and links back to the UQ priorities, which strengthens the manuscript's coherence.
- Tense usage in the methodology and results paragraphs is largely correct (past for actions, present for general truths).
- Figures and tables are introduced before being discussed in detail, following IJHMT convention.
