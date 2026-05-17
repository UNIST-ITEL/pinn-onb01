# Section 3 (Data and Surface Characterization) — Native English Tone Review

**Reviewer role**: Senior native English editor (IJHMT-equivalent journal)
**File reviewed**: `05_manuscript/sections/3_data.tex`
**Date**: 2026-05-17
**Method**: section-drafter agent (B7 pass) — diagnostic, no edits applied

---

## Findings

### 1. Opening sentence is grammatically thin and abstract
- **Issue**: The leading sentence uses an unidiomatic singular "corpus" framing as a precondition. Native usage would more naturally state what was assembled.
- **Original**: "Training and validation of the PINN require a curated pool-boiling corpus."
- **Suggestion**: "Training and validating the PINN required a curated pool-boiling corpus, which we assembled as described below."
- **Why**: Aligns tense with the past-tense methodology register used in the rest of the section and removes the floating "require/requires" timing ambiguity.

### 2. Long appositive interrupts the second sentence
- **Issue**: The four-stage list embedded as an appositive ("comprising selection, digitization, standardization, and per-surface bookkeeping") is awkward inside the main clause. Native style would either split or move it to the end.
- **Original**: "This section documents the four-stage curation pipeline, comprising selection, digitization, standardization, and per-surface bookkeeping, that produces the corpus in \cref{tab:dataset}."
- **Suggestion**: "This section documents a four-stage curation pipeline — selection, digitization, standardization, and per-surface bookkeeping — that produced the dataset summarized in \cref{tab:dataset}."
- **Why**: The em-dash form is more idiomatic for parenthetical enumerations and "produced" matches past-tense methodology. ("the four-stage" with a definite article is also odd because no pipeline has been introduced yet.)

### 3. "Released so preprocessing can be audited" is awkward
- **Issue**: "Released so X can be audited" reads as a translation. "At the figure level" is also ambiguous.
- **Original**: "The dataset is released so preprocessing can be audited at the figure level."
- **Suggestion**: "We release the dataset together with the per-figure preprocessing records to allow independent auditing."
- **Why**: Specifies what "figure level" means (per-figure records) and gives an explicit agent.

### 4. Citation placement disrupts flow in §3.1
- **Issue**: The parenthetical "(\citealp{...} and 18 additional references)" interrupts the sentence and is hard to parse aloud.
- **Original**: "Candidates were drawn from a structured literature survey (\citealp{betz2013,...} and \num{18} additional references)."
- **Suggestion**: "Candidates were drawn from a structured literature survey that screened \num{25} primary references, of which seven (\citealp{betz2013,...}) ultimately supplied data."
- **Why**: Improves linear readability and conveys the funnel from survey to retained sources in one sentence.

### 5. Enumerated criteria lack parallel grammatical structure
- **Issue**: Items (i)-(iv) mix noun phrases with verbal phrases ("pool boiling on...", "a boiling curve allowing...", "at least one...", "stated fluid and pressure"). Native parallelism would lead with the same part of speech.
- **Original**: "(i) pool boiling on a planar or large-cylinder heater so 1D applies; (ii) a boiling curve allowing ONB localization; (iii) at least one quantitative surface descriptor ...; (iv) stated fluid and pressure."
- **Suggestion**: "(i) pool boiling on a planar or large-cylinder heater (so that a 1D treatment is justified); (ii) a published boiling curve from which the ONB can be localized; (iii) at least one quantitative surface descriptor ($R_a$, $\theta$, or an unambiguous coating identity); (iv) an explicitly stated working fluid and pressure."
- **Why**: All four items now begin with a noun phrase and read in parallel; "so 1D applies" is jargon that benefits from a brief clarifier.

### 6. "Seven primary sources resulted" is an unnatural construction
- **Issue**: "Resulted" used intransitively this way is a translation tell.
- **Original**: "Seven primary sources resulted."
- **Suggestion**: "Seven primary sources passed all four criteria."
- **Why**: Idiomatic and reinforces the screening logic just stated.

### 7. "Manually verified before manual click tracing" is repetitive
- **Issue**: "Manually ... manual" within five words is awkward.
- **Original**: "Axis calibration used tick labels, with log axes manually verified before manual click tracing."
- **Suggestion**: "Axes were calibrated from tick labels, and logarithmic scales were verified by hand before point-by-point tracing."
- **Why**: Eliminates the repetition; "by hand" / "point-by-point" distinguish two distinct manual operations.

### 8. "Each series was required to be monotonic" — verb voice and tense
- **Issue**: "Was required to be" is overly bureaucratic and slightly stilted.
- **Original**: "Each series was required to be monotonic in $q''$, and violations were flagged rather than deleted."
- **Suggestion**: "We required each series to be monotonic in $q''$; violations were flagged for review rather than deleted."
- **Why**: Active voice for the design choice followed by passive for the resulting action is the standard methodology register.

### 9. "Digitized ranges were cross-checked against reported units"
- **Issue**: Cross-checking a range against a unit is not quite logical; the intent is presumably to verify that the digitized numerical range matched what the source paper reported.
- **Original**: "Digitized ranges were cross-checked against reported units."
- **Suggestion**: "The digitized numerical ranges were cross-checked against the values reported in the source text."
- **Why**: Precision: ranges are checked against reported values, not against units per se.

### 10. "Totalling" — UK spelling and inelegant phrasing
- **Issue**: "Totalling" is British; the manuscript otherwise uses US English. The phrasing also chains numbers in a way that is hard to scan.
- **Original**: "The protocol produced \num{53} raw curve files totalling \num{1361} points ($\sim$\num{25.7} points per figure)."
- **Suggestion**: "The protocol produced \num{53} raw curve files containing \num{1361} points in total (mean \num{25.7} points per figure)."
- **Why**: US "containing ... in total"; "mean" is more precise than the squiggle.

### 11. "An open-source standardization script" — vague agent
- **Issue**: Saying a script "applies" things feels disembodied; native methodology usually attributes actions to the authors and then describes the artifact.
- **Original**: "Raw curves were converted to a common schema by an open-source standardization script. The script applies unit factors to SI ..."
- **Suggestion**: "We converted the raw curves to a common schema using an open-source standardization script. The script converts units to SI (e.g., kW/m$^{2} \to$ W/m$^{2}$), ..."
- **Why**: "Converts units to SI" is more accurate than "applies unit factors to SI"; the second sentence also reads better with a parenthetical example.

### 12. "Recognizes figures with $h$ on either axis" is ambiguous
- **Issue**: "On either axis" could mean "on one axis or the other", but is colloquial here.
- **Original**: "It recognizes figures with $h$ on either axis and reconstructs $\Delta T_{\mathrm{wall}} = q''/h$ when needed."
- **Suggestion**: "When the heat-transfer coefficient $h$ is reported on either the abscissa or the ordinate, the script reconstructs $\Delta T_{\mathrm{wall}} = q''/h$."
- **Why**: Spelling out the axis names removes ambiguity and reads less casually.

### 13. Comma splice / over-stacked clause in §3.4
- **Issue**: "A clear example is the polished copper of \citet{jabardo2009} run with both R-123 and R-134a, whose card then carries a one-to-many mapping." The "whose" refers ambiguously to "copper" rather than to the surface entry.
- **Original**: "A clear example is the polished copper of \citet{jabardo2009} run with both R-123 and R-134a, whose card then carries a one-to-many mapping."
- **Suggestion**: "For example, the polished copper substrate of \citet{jabardo2009} was tested in both R-123 and R-134a; the corresponding surface card therefore carries a one-to-many fluid mapping."
- **Why**: Resolves the dangling "whose", uses past tense consistent with reporting prior experiments, and reads more naturally.

### 14. "Ten high-level categories grouped by source paper and material support stratified sampling" — garden path
- **Issue**: The reader parses "categories grouped by source paper and material" as a noun phrase, then trips over the verb "support".
- **Original**: "Ten high-level categories grouped by source paper and material support stratified sampling."
- **Suggestion**: "Ten high-level categories, grouped by source paper and material, support stratified sampling."
- **Why**: Comma framing of the participial phrase prevents the garden-path reading.

### 15. "Of these, X were manual" — count-verb agreement and listing style
- **Issue**: The long parenthetical figure list reads like a database dump in the middle of a sentence.
- **Original**: "Of these, \num{24} were manual (BETZ Fig.~4, JO Fig.~3, PHAN Fig.~12a, BOURDON-2012 Fig.~4, BOURDON-2015 Fig.~3, JABARDO Fig.~9a/9c)."
- **Suggestion**: "Of these, \num{24} were assigned manually from clearly identifiable inflection points (see Fig.~4 of BETZ, Fig.~3 of JO, Fig.~12a of PHAN, Fig.~4 of BOURDON-2012, Fig.~3 of BOURDON-2015, and Fig.~9a/9c of JABARDO)."
- **Why**: Adds the reason for manual assignment and conforms to the more standard "Fig.~N of Author" pattern in English journals.

### 16. "Came from a slope-change heuristic ... picking the first point" — dangling participle
- **Issue**: "Picking" grammatically attaches to "the remaining 58", not the heuristic.
- **Original**: "The remaining \num{58} came from a slope-change heuristic in $\log q''$--$\log\Delta T_{\mathrm{wall}}$ space, picking the first point where the local slope exceeds the natural-convection slope by $\sim$\num{1.5}."
- **Suggestion**: "The remaining \num{58} were assigned by a slope-change heuristic in $\log q''$--$\log\Delta T_{\mathrm{wall}}$ space: the heuristic selects the first point at which the local slope exceeds the natural-convection slope by a factor of approximately \num{1.5}."
- **Why**: Splits the sentence at a colon and gives "select" a proper subject. "By a factor of $\sim$1.5" is unitless and clearer than "by $\sim$1.5".

### 17. "Overridden when inconsistent with ... or the Hsu envelope" — ellipsis confusion
- **Issue**: It is unclear whether the override removed the point, replaced it with the manual label, or shifted it to the envelope boundary.
- **Original**: "Nine labels were overridden when inconsistent with the physical interval $2 \le \Delta T_{\mathrm{ONB}} \le \SI{30}{\kelvin}$ or the Hsu envelope."
- **Suggestion**: "Nine heuristic labels were overridden when they fell outside the physically admissible interval $2 \le \Delta T_{\mathrm{ONB}} \le \SI{30}{\kelvin}$ or violated the Hsu envelope; in each case the manual label was retained."
- **Why**: Specifies the action taken on override and clarifies which labels were affected (heuristic, not manual).

### 18. "Backs out" is colloquial
- **Issue**: "Back out" for "infer" is informal and unusual in a journal context.
- **Original**: "For each label, \cref{subsec:hsu} backs out an effective $r_c$ as a weak label."
- **Suggestion**: "For each label, the procedure of \cref{subsec:hsu} infers an effective $r_c$ that is retained as a weak supervisory signal."
- **Why**: "Infers" is the standard verb; "weak supervisory signal" is the established ML term and is more informative than bare "weak label".

### 19. "Two release tables are produced" — passive without agent and present tense
- **Issue**: Tense slips into the present here while the rest of the paragraph is in the past.
- **Original**: "Two release tables are produced: the full curated curve table (\num{1361} rows, 14 columns) and the ONB-label subset (\num{82} rows, 12 columns)."
- **Suggestion**: "The pipeline produced two release tables: the full curated curve table (\num{1361} rows, 14 columns) and the ONB-label subset (\num{82} rows, 12 columns)."
- **Why**: Restores tense consistency and gives the action a clear subject.

### 20. "Bracketing ... and extending into the refrigerant low-superheat regime"
- **Issue**: "Bracketing" implies the dataset surrounds the canonical window, which is not quite the meaning. "Encompasses" or "spans" is closer.
- **Original**: "$\SI{0.7}{\kelvin} \le \Delta T_{\mathrm{ONB}} \le \SI{24.9}{\kelvin}$, bracketing the canonical 2--\SI{30}{\kelvin} water window and extending into the refrigerant low-superheat regime."
- **Suggestion**: "$\SI{0.7}{\kelvin} \le \Delta T_{\mathrm{ONB}} \le \SI{24.9}{\kelvin}$, covering most of the canonical water window (\SIrange{2}{30}{\kelvin}) and extending below it into the low-superheat regime characteristic of refrigerants."
- **Why**: "Covering" is more accurate, the \SIrange macro is the siunitx idiom for ranges, and the qualification "characteristic of refrigerants" is more idiomatic than "refrigerant low-superheat regime".

### 21. "After a post-CHF filter" — abrupt qualifier
- **Issue**: The reader has not been told that CHF filtering was performed.
- **Original**: "Labeled heat flux ranges from $\sim$\SI{0.1}{\kilo\watt\per\square\meter} to \SI{1434}{\kelvin}\per\square\meter} after a post-CHF filter."
- **Suggestion**: "After removing points beyond the critical heat flux (CHF) of each surface, the labeled heat flux spans approximately \SIrange{0.1}{1434}{\kilo\watt\per\square\meter}."
- **Why**: Introduces the CHF filter as an action before quoting its consequence and uses \SIrange.

### 22. "CoolProp does not validate it" is imprecise
- **Issue**: "Validate" suggests CoolProp judges the data, but the intended meaning is that CoolProp does not provide a validated equation of state for FC-77.
- **Original**: "FC-77 is released but excluded from PINN training because CoolProp does not validate it; effective $n=\num{77}$."
- **Suggestion**: "FC-77 entries are released but excluded from PINN training because CoolProp does not provide a validated equation of state for this fluid; the effective training count is therefore $n=\num{77}$."
- **Why**: Removes the ambiguity around "validate" and makes the consequence ("therefore") explicit.

### 23. "Water runs are near atmospheric" — register slip
- **Issue**: Telegraphic and slightly informal.
- **Original**: "Water runs are near atmospheric."
- **Suggestion**: "All water experiments were conducted at near-atmospheric pressure."
- **Why**: Restores full clause structure and matches the past-tense reporting register.

### 24. "The only pressure leverage in the corpus"
- **Issue**: "Leverage" is journalistic/financial jargon when used this way; native scientific usage prefers "variability" or "lever arm".
- **Original**: "JABARDO refrigerant data span reduced pressures $p_r \approx 0.06$--$0.26$, the only pressure leverage in the corpus."
- **Suggestion**: "The JABARDO refrigerant data span reduced pressures $p_r \approx \numrange{0.06}{0.26}$ and provide the only pressure variation available in the present corpus."
- **Why**: "Provide the only pressure variation" is the standard phrasing; the definite article on "JABARDO refrigerant data" is also more natural.

---

## Overall impression

Section 3 is technically thorough and the four-stage pipeline structure is appropriate for a data section in IJHMT. The principal weaknesses are register slippage (multiple shifts between present and past tense within the same paragraph), occasional colloquialisms ("backs out", "leverage", "bracketing"), and several parallelism failures in the enumerated criteria. A consistent pass to (i) hold the past-passive methodology register, (ii) parallelise enumerated lists, and (iii) replace informal verbs with their scientific equivalents would lift the section to publication-ready native quality without changing any technical content. A handful of dangling participles and one ambiguous "whose" should be repaired in the same pass.

## Strengths

1. Each subsection has a clear topic sentence and the section as a whole follows a logical funnel (selection → digitization → standardization → cards → labeling → statistics).
2. Quantitative bookkeeping (49 surfaces, 1361 points, 82 ONB labels) is reported consistently and traceably across the prose and the table.
3. The justification for excluding FC-77 from training and for the CHF filter shows methodological transparency that referees will appreciate.
