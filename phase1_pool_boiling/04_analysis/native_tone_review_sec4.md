# Section 4 (Architecture and Training) — Native English Tone Review

**Reviewer role**: Senior native English editor (IJHMT-equivalent journal)
**File reviewed**: `05_manuscript/sections/4_architecture.tex`
**Date**: 2026-05-17
**Method**: section-drafter agent (B7 pass) — diagnostic, no edits applied

---

## Findings (16 substantive items)

### 1. Opening sentence — list parallelism and missing article
**Location**: lines 9-11 ("The conditioned PINN combines a surface-descriptor encoder with a one-dimensional conduction backbone, three task-specific heads, and a five-term composite loss.")
**Issue**: The list "with A, B, C, and D" is grammatically uneven. "with" governs the first item, then the subsequent items implicitly share the verb "combines". The result reads awkwardly because "combines X with Y" pairs two things, whereas here four items are combined.
**Suggested revision**: "The conditioned PINN couples a surface-descriptor encoder, a one-dimensional conduction backbone, three task-specific heads, and a five-term composite loss." (Replace "combines...with" with a single verb "couples" or "integrates", letting all four items sit in a flat list.)

### 2. "kept it low" — informal register and ambiguous pronoun
**Location**: lines 13-14 ("We kept it low because only \num{1361} boiling-curve points are available...")
**Issue**: "kept it low" is colloquial for a methods section. The pronoun "it" technically refers to "parameter count" but the antecedent is buried two clauses back.
**Suggested revision**: "The parameter count was deliberately constrained because only \num{1361} boiling-curve points were available, decreasing to \num{1167} after the FC-77 holdout was removed." Note also the tense shift to past for the dataset state.

### 3. Verb tense inconsistency in numeric channel listing
**Location**: lines 22-25 ("The encoder maps the partially observed surface descriptor of each heater to a fixed latent... Its input concatenates nine numeric channels...")
**Issue**: Mostly correct, but "maps" (present, describing model behavior) is fine; the inconsistency emerges later where authors' actions creep in. The list itself is structurally clean.
**Suggested revision**: No change needed in this sentence — flagged for awareness.

### 4. Awkward channel description with mixed grammatical forms
**Location**: lines 25-34 (numeric channel enumeration)
**Issue**: Channels (4), (6), (8) are described as "a binary $\theta$-availability mask", "its availability mask", "its availability mask" — the pronoun "its" loses its antecedent across the list because intervening items are arithmetic expressions, not nouns. A native editor would reword for clarity.
**Suggested revision**: Replace "(6) its availability mask" with "(6) an availability mask for $r_c$" and "(8) its availability mask" with "(8) an availability mask for $N_s$" so each entry stands alone.

### 5. Tense register slip — "Masks separate"
**Location**: lines 38-39 ("Masks separate ``not measured'' from ``measured zero''.")
**Issue**: Acceptable, but the abrupt short sentence breaks the flow. Also, "Masks" without an article is licensed only because of the enumerative context; a native reader expects "The masks separate..."
**Suggested revision**: "The masks distinguish 'not measured' from 'measured zero'." ("Distinguish A from B" is the idiomatic pairing; "separate A from B" sounds physical.)

### 6. "A ten-vocabulary categorical embedding" — modifier ordering
**Location**: lines 39-40 ("A ten-vocabulary categorical embedding indexed by source paper and heater material absorbs paper-level biases without binding to fluid.")
**Issue**: "ten-vocabulary" is non-idiomatic; native usage is "vocabulary of ten" or "ten-entry vocabulary". "without binding to fluid" reads as missing an article — "without binding to the fluid" or, more idiomatic, "without coupling to fluid identity".
**Suggested revision**: "A categorical embedding with a vocabulary of ten entries, indexed by source paper and heater material, absorbs paper-level biases without coupling to fluid identity."

### 7. "It feeds a three-layer MLP" — vague subject reference
**Location**: lines 42-44 ("A scalar layer normalization uses the masks to renormalize only over observed entries. It feeds a three-layer MLP of width \num{64} with GELU activations and dropout \num{0.1}.")
**Issue**: The pronoun "It" technically refers to "layer normalization" but the prior sentence ended with "observed entries", inviting misreading. Native style joins the two ideas.
**Suggested revision**: "Scalar layer normalization renormalizes only over observed entries (using the masks) and then feeds a three-layer MLP of width \num{64} with GELU activations and dropout \num{0.1}."

### 8. "Its inputs are" — fragmented sequence
**Location**: lines 52-57 ("The backbone is fully connected. It uses five hidden layers of width \num{64} with $\tanh$ activations. The smooth activation keeps the second-order derivatives required by \cref{eq:laplace} well-defined under automatic differentiation. Its inputs are...")
**Issue**: Four consecutive short sentences each starting with "It" / "The" / "Its" produce a staccato rhythm. The pronoun "Its" jumps back across an intervening sentence about activations, which slightly obscures the antecedent.
**Suggested revision**: "The backbone is a fully connected network with five hidden layers of width \num{64} and $\tanh$ activations; the smooth activation keeps the second-order derivatives required by \cref{eq:laplace} well-defined under automatic differentiation. The backbone receives $z^{*} \in [0,L^{*}]$, the surface latent $z_s$, and the operating descriptor $(q^{*}_{\mathrm{appl}}, \Delta T^{*}_{\mathrm{sub}})$."

### 9. "We implemented two conditioning strategies" — tense mismatch with surrounding present
**Location**: lines 57-60
**Issue**: The past tense "implemented" is appropriate (authors' action). However, the next sentence, "The \texttt{concat} option stacks all inputs..." uses present, while "The \texttt{film} option, used in the final model, injects..." mixes a past participle ("used") with a present verb ("injects"). The shift is fine in principle but creates a subtle inconsistency a native reviewer would smooth.
**Suggested revision**: Keep "We implemented", then describe the options consistently in present: "The \texttt{concat} variant stacks all inputs into an 11-dimensional vector; the \texttt{film} variant — adopted in the final model — injects $z_s$ at every hidden layer..."

### 10. "FiLM couples...with fewer parameters than concatenation" — comparison fragment
**Location**: lines 62-64
**Issue**: "fewer parameters than concatenation" elides the second half of the comparison. Native readers prefer "fewer parameters than concatenation requires" or "than the concatenation variant".
**Suggested revision**: "FiLM couples the surface latent multiplicatively while using fewer parameters than the concatenation variant."

### 11. "branch from the last representation" — vague terminology
**Location**: lines 63-67 ("Three two-layer task heads of hidden width \num{32} branch from the last representation: $T^{*}$ for the PDE/boundary residuals, and $\Delta T^{*}_{\mathrm{ONB}}$ and $q^{*}_{\mathrm{ONB}}$ via softplus.")
**Issue**: "the last representation" is informal; the standard ML phrase is "the final hidden representation" or "the last hidden layer". The colon-introduced list mixes a residual output with two scalar predictions in an awkward parallel: "$T^{*}$ for the PDE/boundary residuals, and $\Delta T^{*}_{\mathrm{ONB}}$ and $q^{*}_{\mathrm{ONB}}$ via softplus" reads as if all three share "via softplus".
**Suggested revision**: "Three two-layer task heads, each with hidden width \num{32}, branch from the final hidden representation: one head predicts $T^{*}$ for the PDE and boundary residuals, while the other two predict $\Delta T^{*}_{\mathrm{ONB}}$ and $q^{*}_{\mathrm{ONB}}$ through softplus activations."

### 12. "The total reaches \num{24005}" — phrasing
**Location**: line 68
**Issue**: "The total reaches" suggests gradual accumulation, which is odd for a static count. Native usage: "The total is" or "These yield a total of".
**Suggested revision**: "These components yield a total of \num{24005} trainable parameters."

### 13. "evaluated in the nondimensional variables of" — preposition
**Location**: lines 76-78 ("The composite objective comprises PDE, boundary, data, nucleation-prior, and monotonicity-prior terms, evaluated in the nondimensional variables of \cref{subsec:nondim}.")
**Issue**: "evaluated in" is slightly off; native usage is "evaluated using" or "expressed in" the nondimensional variables. "Comprises" is correct (not "comprises of").
**Suggested revision**: "The composite objective comprises PDE, boundary, data, nucleation-prior, and monotonicity-prior terms, each expressed in the nondimensional variables introduced in \cref{subsec:nondim}."

### 14. "via automatic differentiation" — orphaned modifier
**Location**: lines 92-94 ("...via automatic differentiation. The boundary loss combines the Neumann condition...")
**Issue**: The phrase "via automatic differentiation" lands as a sentence fragment after the displayed equation, attached to nothing grammatically. Native style would either integrate it into the preceding sentence (before the equation) or rephrase.
**Suggested revision**: Move it before the equation: "The PDE residual is evaluated by automatic differentiation on $N_{\mathrm{c}}=\num{2000}$ LHS collocation points~\citep{mckay1979lhs} that are refreshed every \num{100} epochs:" (Then drop the trailing "via automatic differentiation." that orphans the post-equation flow.)

### 15. "penalizes joint mismatch in" — preposition and noun choice
**Location**: lines 108-109 ("The supervised data term penalizes joint mismatch in ONB superheat and heat flux over the \num{1361} curated points")
**Issue**: "penalizes joint mismatch in X and Y" is grammatically unusual; native phrasing is "penalizes the joint mismatch between predicted and observed ONB superheat and heat flux" or "penalizes prediction errors in both ONB superheat and heat flux".
**Suggested revision**: "The supervised data term penalizes prediction errors in both ONB superheat and heat flux across the \num{1361} curated points:" (Also "across" reads better than "over" when scanning a dataset.)

### 16. "The weight is ramped linearly from \num{0.1}" — incomplete specification
**Location**: lines 145-146 ("We set $\varepsilon=\num{0.05}$. The weight is ramped linearly from \num{0.1} over the first \num{2000} Adam epochs.")
**Issue**: "ramped linearly from 0.1" omits the endpoint. A native reader would expect "from 0.1 to [final value] over the first 2000 Adam epochs". Without the target, the sentence is incomplete.
**Suggested revision**: "We set $\varepsilon=\num{0.05}$. The Hsu weight $w_{\mathrm{ONB}}$ ramps linearly from \num{0} to its final value of \num{0.10} over the first \num{2000} Adam epochs of the fine-tuning stage." (Fix the start value if needed; the prose currently contradicts itself by saying the ramp starts at 0.1 yet the final weight is also 0.10.)

### 17. "Each stage activates progressively richer loss terms" — modifier mismatch
**Location**: lines 197-198 ("We trained the model in three sequential stages. Each stage activates progressively richer loss terms.")
**Issue**: "progressively richer loss terms" is non-idiomatic. "Progressively" modifies a process, not a set of terms. Native phrasing: "Each subsequent stage activates additional loss terms" or "The stages progressively activate richer subsets of the loss".
**Suggested revision**: "We trained the model in three sequential stages, each activating a richer subset of the loss than the preceding one."

### 18. "We optimized it by \num{500} Adam iterations" — preposition
**Location**: lines 210-213 ("It introduces a per-surface $r_c$ as a learnable parameter. We optimized it by \num{500} Adam iterations at $\eta=\num{1e-3}$ to maximize the Hsu-likelihood of observed ONB points.")
**Issue**: "optimized it by N iterations" is unidiomatic; native usage is "optimized over N iterations" or "for N iterations".
**Suggested revision**: "It introduces a per-surface $r_c$ as a learnable parameter, which we optimized over \num{500} Adam iterations at $\eta=\num{1e-3}$ to maximize the Hsu-likelihood of the observed ONB points."

### 19. "A custom training loop is required" — voice and tense register
**Location**: lines 222-223 ("We implemented the network in PyTorch~2 in single precision~\citep{paszke2019pytorch}. A custom training loop is required for per-phase parameter-freezing and rollback.")
**Issue**: The sudden shift from "We implemented" (past active) to "is required" (present passive, impersonal) is a register break. Also, "is required" sounds like a general claim, but the authors are describing their own design choice.
**Suggested revision**: "We implemented the network in PyTorch~2 in single precision~\citep{paszke2019pytorch}, with a custom training loop to support per-phase parameter freezing and rollback."

### 20. "no surface appears in more than one split, preventing leakage" — comma splice borderline
**Location**: lines 226-228 ("We split the dataset at the surface level (\SI{80}{\percent} train, \SI{10}{\percent} validation, \SI{10}{\percent} test); no surface appears in more than one split, preventing leakage.")
**Issue**: The construction is acceptable, but "preventing leakage" as a participial tail attached to "no surface appears..." reads awkwardly because the act of preventing belongs to the splitting strategy, not to any single surface. Native style prefers an explicit subject.
**Suggested revision**: "We split the dataset at the surface level (\SI{80}{\percent} train, \SI{10}{\percent} validation, \SI{10}{\percent} test); because no surface appears in more than one split, the protocol prevents data leakage."

---

## Overall impression

Section 4 is technically dense, well organized, and the LaTeX/equation infrastructure is uniformly clean. The author clearly controls the architectural vocabulary (FiLM, GELU, LHS, softplus, L-BFGS), and the five-term loss is laid out with admirable rigor. However, the prose oscillates between two competing styles: terse declarative sentences (often 4-8 words) that produce a staccato cadence, and long agglomerated sentences carrying multiple clauses. A native editor's primary recommendation would be to merge adjacent short sentences with semicolons or coordinating conjunctions to recover narrative flow, particularly in the encoder and backbone subsections. A handful of prepositional choices ("evaluated in", "by N iterations", "fewer parameters than concatenation") and a few elided comparisons would be flagged by a native reviewer, but none rises to the level of substantive miscommunication. The most consequential issue is the incomplete ramp specification (item 16), which is genuinely ambiguous and should be fixed before submission. Tense handling is mostly correct: present for model behavior, past for the authors' actions, with only two slips (items 9 and 19). With moderate sentence-level polishing the section will read as fully native.

## Strengths

- Consistent and correct use of mathematical notation; nondimensional variables, units (siunitx), and cross-references are uniformly handled.
- Hyperparameter table is complete, well-captioned, and traceable to the prose.
- Citations are placed where a senior reviewer would expect them (FiLM, Adam, L-BFGS, PyTorch, LHS, Hsu, Raissi).
- Loss decomposition into five named terms with one paragraph each is pedagogically clean — a strong choice for a methods section.
- The "data-dominant" justification of the loss balance, tied to ONB sparsity, is the kind of physical reasoning that distinguishes a PINN paper from a generic ML paper.
- Reproducibility details (seeds, hardware, MLflow, public checkpoint) are itemized — IJHMT reviewers will respond well to this.
