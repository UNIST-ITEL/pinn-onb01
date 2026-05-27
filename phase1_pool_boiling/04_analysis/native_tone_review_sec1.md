# Section 1 (Introduction) — Native English Tone Review

**Reviewer role**: Senior native English editor (IJHMT-equivalent journal)
**File reviewed**: `05_manuscript/sections/1_introduction.tex`
**Date**: 2026-05-17
**Method**: section-drafter agent (B7 pass) — diagnostic, no edits applied

---

## Findings (20 substantive items)

### 1. Paragraph 1 — "Engineered surfaces now combine..."
- **Issue**: Sentence flow / cohesion, awkward phrasing
- **Original**: "Engineered surfaces now combine roughness control, wettability tailoring, biphilic patterning, and nano-/micro-structuring, and such surfaces shift $\Delta T_{\mathrm{ONB}}$ by more than..."
- **Suggestion**: "Engineered surfaces now combine roughness control, wettability tailoring, biphilic patterning, and nano-/micro-structuring; collectively, these treatments shift $\Delta T_{\mathrm{ONB}}$ by more than..."
- **Why**: Repeated "and such surfaces" is clumsy; semicolon + connector reads more naturally.

### 2. Paragraph 1 — "Yet design practice still relies..."
- **Issue**: Sentence fragmentation, choppy rhythm
- **Original**: "Yet design practice still relies on correlations. Their residual scatter remains \SIrange{20}{30}{\percent}. The consequences are..."
- **Suggestion**: "Yet design practice still relies on correlations whose residual scatter remains 20-30\%, with consequences including oversized exchangers, conservative safety margins, and an inability to exploit engineered-surface performance."
- **Why**: Three short consecutive sentences sound staccato; combining yields the cadence expected in IJHMT prose.

### 3. Paragraph 2 — "The dominant analytical framework dates to Hsu... He derived..."
- **Issue**: Article usage / register
- **Original**: "The dominant analytical framework dates to Hsu~\citep{hsu1962}. He derived..."
- **Suggestion**: "The dominant analytical framework dates to Hsu~\citep{hsu1962}, who derived..."
- **Why**: Relative clause avoids abrupt pronoun "He," which feels informal/biographical.

### 4. Paragraph 2 — "gave an explicit closed form"
- **Issue**: Word choice precision
- **Original**: "Davis and Anderson~\citep{davis1966} gave an explicit closed form"
- **Suggestion**: "Davis and Anderson~\citep{davis1966} derived an explicit closed-form expression"
- **Why**: "Gave" is colloquial; "derived" matches surrounding technical register. "Closed form" is normally hyphenated when prenominal.

### 5. Paragraph 2 — "The five correlations share two structural limitations"
- **Issue**: Awkward phrasing / counting mismatch
- **Original**: "The five correlations share two structural limitations."
- **Suggestion**: "These correlations share two structural limitations."
- **Why**: Only four citation groups were just listed; "the five" forces the reader to count back.

### 6. Paragraph 2 — "Multi-descriptor evidence contradicts this reduction."
- **Issue**: Word choice / register
- **Original**: "Multi-descriptor evidence contradicts this reduction."
- **Suggestion**: "Evidence using multiple descriptors contradicts this simplification."
- **Why**: "Multi-descriptor evidence" reads as compressed jargon. "Reduction" is ambiguous (could mean numerical reduction).

### 7. Paragraph 3 — "A notable example is..."
- **Issue**: Wordiness / hedge
- **Original**: "Data-driven approaches have been applied to related boiling problems. A notable example is the CHF work of Hobold and da Silva~\citep{hobold2018}."
- **Suggestion**: "Data-driven approaches have been applied to related boiling problems, notably the CHF study of Hobold and da Silva~\citep{hobold2018}."
- **Why**: "A notable example is" is the kind of filler native editors routinely strike.

### 8. Paragraph 3 — "They embed governing PDEs..."
- **Issue**: Sentence length / run-on with stacked participles
- **Original**: "They embed governing PDEs and physical constraints as soft losses during training, compensating for limited data with mechanistic regularization and producing models that respect conservation laws in extrapolation"
- **Suggestion**: Split into two: "They embed governing PDEs and physical constraints as soft losses during training. This compensates for limited data with mechanistic regularization and yields models that respect conservation laws under extrapolation."
- **Why**: Two trailing "-ing" clauses stacked after a comma feel like translated prose; splitting clarifies agency.

### 9. Paragraph 3 — "To our knowledge, no PINN study..."
- **Issue**: Sentence flow / parallelism
- **Original**: "To our knowledge, no PINN study has targeted pool-boiling ONB with explicit surface-modification conditioning. None has integrated curated multi-source datasets..."
- **Suggestion**: "To our knowledge, no PINN study has targeted pool-boiling ONB with explicit surface-modification conditioning, nor has any integrated curated multi-source datasets for cross-fluid generalization."
- **Why**: "None has" sounds stilted; "nor has any" is standard native idiom for paired negatives.

### 10. Paragraph 4 — "First... Second... Third... Fourth..."
- **Issue**: Repetition / awkward phrasing
- **Original**: "the intersection of pool-boiling ONB and PINN is empty. Second, the intersection of surface modification and PINN is likewise empty"
- **Suggestion**: "no published PINN study addresses pool-boiling ONB. Second, none addresses surface modification, although correlation- and CFD-based baselines exist..."
- **Why**: "Intersection is empty" is set-theoretic jargon; repeated twice reads as translated.

### 11. Paragraph 4 — "Forward problems were pioneered by... Neither addresses..."
- **Issue**: Sentence flow / abrupt insertion
- **Original**: "Forward problems were pioneered by~\citet{raissi2019} and thermal inverse problems by~\citet{cai2021}. Neither addresses pool-boiling ONB."
- **Suggestion**: "Although \citet{raissi2019} pioneered forward PINN formulations and \citet{cai2021} extended them to thermal inverse problems, neither addressed pool-boiling ONB."
- **Why**: Current pair feels parenthetical and disconnected; concessive clause integrates with gap statement.

### 12. Paragraph 5 — "The contributions are fivefold."
- **Issue**: Register / cliché
- **Original**: "The contributions are fivefold."
- **Suggestion**: "This work makes five contributions." or "We report five principal contributions."
- **Why**: "Fivefold" is acceptable but slightly stiff/old-fashioned.

### 13. Paragraph 5 — "Thirty-seven are newly digitized."
- **Issue**: Number formatting / sentence fragmentation
- **Original**: "$49$ surface descriptor cards. Thirty-seven are newly digitized. Each encodes..."
- **Suggestion**: "49 surface-descriptor cards, of which 37 are newly digitized; each encodes $R_a$, $\theta$, $r_c$, $N_s$, and a categorical paper tag."
- **Why**: Three back-to-back short sentences interrupt flow. Native style would not switch to spelled-out "Thirty-seven" when "49" was just numerical.

### 14. Paragraph 5 — "A compact encoder modulates..."
- **Issue**: Punctuation / comma splice tendency
- **Original**: "A compact encoder modulates the temperature-field network through feature-wise linear modulation (FiLM), and the total parameter count is $24\,005$."
- **Suggestion**: "A compact encoder modulates the temperature-field network through feature-wise linear modulation (FiLM); the total parameter count is 24,005."
- **Why**: Two clauses are only loosely related; semicolon flags shift better than coordinating "and."

### 15. Paragraph 5 — "An inverse-problem study recovers..."
- **Issue**: Verb tense consistency
- **Original**: "An inverse-problem study recovers active cavity radii... Recovered radii were evaluated against... The analysis uncovers a Simpson-type reversal..."
- **Suggestion**: Single tense, e.g., past throughout: "An inverse-problem study recovered active cavity radii from ONB observations using the Hsu relation; the recovered radii were evaluated against the physical band... and revealed a Simpson-type reversal..."
- **Why**: Mixing present ("recovers", "uncovers") with past ("were evaluated") within one item is a classic non-native tell.

### 16. Paragraph 5 — "passed four-of-four..."
- **Issue**: Awkward phrasing / hyphenation
- **Original**: "passed four-of-four Level~1 code-verification tests... eight-of-nine Level~3 physical-consistency tests"
- **Suggestion**: "passed all four Level-1 code-verification tests... and eight of nine Level-3 physical-consistency tests"
- **Why**: "Four-of-four" hyphenated as a unit is non-standard.

### 17. Paragraph 5 — "This is a 53\% reduction over..."
- **Issue**: Word choice precision
- **Original**: "This is a \SI{53}{\percent} reduction over the best classical correlation."
- **Suggestion**: "This represents a 53\% reduction relative to the best classical correlation."
- **Why**: "Reduction over" is non-idiomatic. "Relative to" or "compared with" is standard.

### 18. Paragraph 6 — Five consecutive "Section X..." openings
- **Issue**: Repetitive sentence opening (B6 LanguageTool also caught this)
- **Suggestion**: Vary at least two openings, e.g., "The governing equations, Hsu criterion, and non-dimensional scales are introduced in Section~\ref{sec:formulation}." Or merge two sections into one sentence with a semicolon.
- **Why**: Anaphoric "Section X / Section Y / Section Z" feels monotonous.

### 19. Paragraph 1 — "Pool boiling dissipates high heat fluxes through a passive mechanism."
- **Issue**: Opening sentence impact
- **Suggestion**: "Pool boiling is a passive mechanism capable of dissipating high heat fluxes." or "Pool boiling removes high heat fluxes passively, without external power input."
- **Why**: Current opener lacks the framing native readers expect from a first sentence; conflates subject and predicate awkwardly.

### 20. Paragraph 4 — "It provides a reproducible baseline..."
- **Issue**: Pronoun referent ambiguity
- **Original**: "The present study addresses these four gaps in a single framework. It provides a reproducible baseline..."
- **Suggestion**: "The present study addresses these four gaps in a single framework and provides a reproducible baseline..."
- **Why**: Standalone "It" weakens cohesion; coordination is cleaner.

---

## Overall impression

The Introduction is clearly structured and substantively strong; a native reader would follow the argument easily and recognize the gap statement and contributions as well organized. The most pervasive weakness is a staccato rhythm produced by short, declarative sentences placed in succession (paragraphs 1, 3, and 5 are most affected). This pattern, combined with several set-theoretic and translated-sounding constructions ("the intersection ... is empty," "multi-descriptor evidence," "reduction over"), is the main fingerprint of non-native authorship. Tense mixing inside the Contributions block and the monotonous "Section X states..." cadence in the closing paragraph would also be noted by a copy editor. None of the issues are content-level; with light rephrasing the section would read as natively authored IJHMT prose.

## Strengths

1. Citation placement and density are appropriate and match IJHMT conventions.
2. Technical vocabulary (FiLM, deep ensemble, Hsu criterion, biphilic) is used precisely and without overhedging.
3. The gap analysis and contributions are quantitatively framed (RMSE, n, ranges), which native reviewers value.

---

## B6 LanguageTool (en-US) comparison

LanguageTool found 54 raw issues; after filtering pandoc citation-strip artifacts (whitespace/spelling rules disabled), 4 remained:
1. `each treats surface character` — flagged as plural noun after "each" (false positive; "each" here is pronoun referring to "five correlations")
2-4. Three consecutive "Section X..." openings in Paragraph 6 (same as item 18 above)

B6 contributed 1 actionable insight (item 18). B7 contributed 19 additional substantive items not caught by LT.
