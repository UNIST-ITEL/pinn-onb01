# Section 2 (Mathematical Formulation) — Native English Tone Review

**Reviewer role**: Senior native English editor (IJHMT-equivalent journal)
**File reviewed**: `05_manuscript/sections/2_formulation.tex`
**Date**: 2026-05-17
**Method**: section-drafter agent (B7 pass) — diagnostic, no edits applied

---

## Findings (15 substantive items)

### 1. Subsection 2.1, opening sentence (lines 13-14)
- **Issue**: Article usage / awkward noun string
- **Original**: "The configuration is a horizontal heater of thickness $L$ in a quiescent liquid pool at saturation pressure."
- **Suggestion**: "We consider a horizontal heater of thickness $L$ immersed in a quiescent liquid pool maintained at saturation pressure."
- **Why**: "The configuration is..." reads as a definition stub; native authors typically open with an active framing verb ("We consider", "Consider"). "Maintained at" is the conventional collocation for a pool held at a given pressure.

### 2. Subsection 2.1 (line 14-15)
- **Issue**: Preposition / phrasing
- **Original**: "The coordinate $z$ is normal to the heating surface."
- **Suggestion**: "The $z$-axis is taken normal to the heating surface, with origin at the bottom face."
- **Why**: "The coordinate $z$ is normal to..." treats a scalar as if it had a direction. Native usage: "axis" carries direction; "coordinate" is a value along it. The added "with origin..." removes ambiguity about which end is $z=0$.

### 3. Subsection 2.1 (line 15-16)
- **Issue**: Awkward verb choice
- **Original**: "The bottom face at $z=0$ receives the imposed flux $q''_{\mathrm{applied}}$..."
- **Suggestion**: "A uniform heat flux $q''_{\mathrm{applied}}$ is imposed at the bottom face ($z=0$)..."
- **Why**: A face "receiving" a flux is informal anthropomorphism. Standard heat-transfer prose uses "is imposed at / prescribed at".

### 4. Subsection 2.1 (line 17-18)
- **Issue**: Wordiness / awkward justification
- **Original**: "The lateral extent exceeds $L$ by at least two orders of magnitude, so the field is treated as 1D."
- **Suggestion**: "Because the lateral extent exceeds $L$ by at least two orders of magnitude, the temperature field is treated as one-dimensional."
- **Why**: Spell out "one-dimensional" on first appearance (later "1D" is fine). "So" as a logical connector is acceptable but "Because... ," reads more formally for a methods section.

### 5. Subsection 2.1, itemize block (lines 19-26)
- **Issue**: Register slippage / parallelism
- **Original**: "The model assumes: steady conduction (ONB lies on the steady single-phase branch); no volumetric heat generation; adiabatic lateral boundaries; uniform, temperature-independent $k_s$; laminar natural convection above $z=L$, closed by a Nusselt-type coefficient at $T(L)$."
- **Suggestion**: Rephrase as "The following assumptions are adopted: (i) steady-state conduction, justified by the fact that ONB lies on the steady single-phase branch; (ii) negligible volumetric heat generation; (iii) adiabatic lateral boundaries; (iv) uniform, temperature-independent solid conductivity $k_s$; and (v) laminar natural convection above $z=L$, closed by a Nusselt-type correlation evaluated at $T(L)$."
- **Why**: Itemized bullets are uncommon in journal manuscripts (more typical of preprints/theses); inline numbered enumeration is preferred. "Closed by a coefficient" is loose — closure is by a correlation that yields a coefficient.

### 6. Subsection 2.1, last sentence (lines 27-28)
- **Issue**: Choppy / passive flow
- **Original**: "The same framework applies to horizontal cylinders of large diameter. The derivation is stated for the flat plate."
- **Suggestion**: "The same framework applies to large-diameter horizontal cylinders; for brevity, the derivation is presented for the flat-plate geometry."
- **Why**: Two short declaratives back-to-back read abrupt. The semicolon variant signals continuity. "Stated" is weaker than "presented" or "derived".

### 7. Subsection 2.2 (line 34-35)
- **Issue**: Verb choice (mild Koreanism)
- **Original**: "The temperature distribution $T(z)$ in the heater satisfies the steady, source-free, one-dimensional heat equation"
- **Suggestion**: "The temperature distribution $T(z)$ within the heater is governed by the steady, source-free, one-dimensional heat equation"
- **Why**: "Satisfies" is technically correct but most native heat-transfer texts use "is governed by" when introducing the PDE for the first time. "In the heater" → "within the heater" is more idiomatic.

### 8. Subsection 2.2 (lines 42-48)
- **Issue**: Sentence fragmentation / awkward enumeration
- **Original**: "The closed form is not a substitute for the PINN. It serves three roles: an analytical reference for Level~1 verification, a regularizing signal during warm-up, and the basis of the thermal-boundary-layer thickness $\delta_t$ entering \cref{eq:hsu_rc_range}."
- **Suggestion**: "This closed form does not supplant the PINN; rather, it serves three roles: (i) an analytical reference for Level-1 verification, (ii) a regularizing signal during warm-up, and (iii) the basis for the thermal-boundary-layer thickness $\delta_t$ that enters \cref{eq:hsu_rc_range}."
- **Why**: "Is not a substitute for" is colloquial; "does not supplant ... ; rather, it" is the standard concessive structure. Numbered list items improve scannability inside long sentences.

### 9. Subsection 2.3 (lines 54-55)
- **Issue**: Article / passive register
- **Original**: "\cref{eq:laplace} is closed by a Neumann condition at $z=0$ and a Robin condition at $z=L$."
- **Suggestion**: "Equation~\eqref{eq:laplace} is closed by a Neumann condition at $z=0$ and a Robin condition at $z=L$, given respectively by:"
- **Why**: Starting a sentence with the cleveref-rendered "\cref" may yield lowercase "equation" depending on configuration — verify the rendered output. More importantly, adding "given respectively by:" prepares the reader for the two equations that follow, avoiding the abrupt jump.

### 10. Subsection 2.3 (lines 62-63)
- **Issue**: Awkward connective / hyphenation
- **Original**: "and conjugate coupling with the pool is enforced through Newton's law of cooling using the natural-convection coefficient $h_{nc}$,"
- **Suggestion**: "while conjugate coupling with the pool is enforced via Newton's law of cooling, using the natural-convection coefficient $h_{nc}$:"
- **Why**: "And" linking two boundary conditions is weak after a prior "and"; "while" emphasizes the two-sided nature. Comma before "using" is required because the participial phrase is non-restrictive.

### 11. Subsection 2.3 (lines 70-72)
- **Issue**: Missing copula in a list of definitions
- **Original**: "where $k_l$ is the liquid conductivity, $T_L = T(z=L)$, $T_{\infty}$ the bulk-pool temperature, and subcooling $\Delta T_{\mathrm{sub}} = T_{\mathrm{sat}} - T_{\infty}$."
- **Suggestion**: "where $k_l$ denotes the liquid thermal conductivity, $T_L \equiv T(z{=}L)$ the surface-side temperature, $T_{\infty}$ the bulk-pool temperature, and $\Delta T_{\mathrm{sub}} \equiv T_{\mathrm{sat}} - T_{\infty}$ the subcooling."
- **Why**: Parallelism: each item should have the same grammatical structure ("$X$ the ..."). "Subcooling $\Delta T_{\mathrm{sub}} = ...$" breaks the pattern by leading with the noun. Use $\equiv$ for definitional identity.

### 12. Subsection 2.3 (lines 85-88)
- **Issue**: Sequence of short sentences / awkward registers
- **Original**: "The dataset lies in the laminar branch. The turbulent branch is retained for completeness. When only the bulk-pool temperature is reported, \cref{eq:nc_bc} is replaced by $T(L) = T_{\infty}$ in the data-loss term, while the PDE residual still uses \cref{eq:nc_bc}."
- **Suggestion**: "All cases in the present dataset fall within the laminar branch; the turbulent branch is retained only for completeness. When only the bulk-pool temperature is reported in the source, the Dirichlet substitute $T(L)=T_{\infty}$ is applied in the data-loss term, whereas the PDE residual continues to enforce \cref{eq:nc_bc}."
- **Why**: "Lies in" sounds geometric; "fall within" is the convention for data ranges. "Still uses" is conversational; "continues to enforce" carries the methodological weight expected here.

### 13. Subsection 2.4 (lines 94-98)
- **Issue**: Awkward attribution / wordiness
- **Original**: "Incipience follows the criterion of Hsu~\citep{hsu1962}. The criterion identifies the cavity-radius range satisfying mechanical-equilibrium and thermal-boundary-layer conditions for vapor-embryo growth."
- **Suggestion**: "Incipience is modeled following Hsu's criterion~\citep{hsu1962}, which identifies the range of cavity radii that simultaneously satisfy the mechanical-equilibrium and thermal-boundary-layer conditions required for vapor-embryo growth."
- **Why**: "Follows the criterion of Hsu" is structurally fine but stiff; merging the two sentences with "which" is cleaner. "Satisfying" → "that simultaneously satisfy" emphasizes the dual requirement central to Hsu's analysis.

### 14. Subsection 2.4 (lines 126-129)
- **Issue**: Choppy delivery / weak verb
- **Original**: "\cref{eq:hsu_dt_onb} provides the analytical baseline of Section~\ref{sec:results}. It is embedded as a soft penalty in the composite loss. The $\theta$-dependent prefactor lets the network inherit wettability sensitivity that scalar correlations lack."
- **Suggestion**: "Equation~\eqref{eq:hsu_dt_onb} provides the analytical baseline used in Section~\ref{sec:results} and is embedded as a soft penalty within the composite loss. The $\theta$-dependent prefactor allows the network to inherit a wettability sensitivity that scalar correlations cannot capture."
- **Why**: Three back-to-back declaratives lose momentum. "Lets the network inherit" sounds informal — "allows the network to inherit" matches register. "Lack" is blunt; "cannot capture" is more precise about the mechanism.

### 15. Subsection 2.5 (lines 135-138, 152-164)
- **Issue**: Sentence flow / connectives / "therefore" placement
- **Original**: "References are recomputed per fluid through the routine of Section~\ref{sec:data}. Cross-fluid generalization therefore proceeds in a common frame."
- **Suggestion**: "These reference quantities are recomputed for each fluid using the routine described in Section~\ref{sec:data}, so that cross-fluid generalization is performed in a common non-dimensional frame."
- **Why**: "References" is ambiguous — could be read as bibliographic references. "Per fluid" is informal; "for each fluid" is standard. Placing the conclusion clause inside the same sentence with "so that" avoids a stranded "therefore" sentence.

---

## Overall impression

The section is technically sound and the derivations are presented in a logical order. The English, however, exhibits a recurring pattern of short declarative sentences strung together without connective tissue — a signature of Korean-to-English drafting. Equation introductions and post-equation definitions are generally well-formed, but the "where ... is ... , $X$ the ... , and ..." parallelism breaks down in several places. Article usage is occasionally too sparse before abstract nouns ("steady conduction" should be "steady-state conduction" on first use). Subsections 2.3 and 2.4 would benefit most from re-flowing into longer, connective-rich periods. None of the issues compromise meaning, but a native pass would noticeably elevate the register.

## Strengths

- Equation typography and labeling are consistent and journal-ready.
- Technical vocabulary (Robin condition, conjugate coupling, Zuber CHF scale) is used correctly throughout.
- Variable definitions following equations are largely complete and unambiguous.
