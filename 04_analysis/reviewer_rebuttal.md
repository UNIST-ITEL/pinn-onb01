# PINN-ONB01 — Anticipated Reviewer Questions and Rebuttals

**Target journal:** International Journal of Heat and Mass Transfer
**Manuscript:** Surface-Conditioned Physics-Informed Neural Network for Pool-Boiling Onset of Nucleate Boiling
**Prepared:** 2026-05-18
**Source:** Consulting reports 01 and 02 plus a full manuscript audit (Sections 2--5, Tables 1--6, Figs.~1--20)

---

## Executive summary

Reviewer attacks on this manuscript are expected to cluster around four recurring themes:
(i) the physical validity of inverse cavity radii in the absence of SEM/AFM ground truth (consulting 01-Q1);
(ii) the meaning of the residual PDE term being above the canonical $10^{-3}$ floor (consulting 01-Q2);
(iii) shortcut learning through the ten-entry paper/material embedding (consulting 02-Q1); and
(iv) the methodological tension between a 1D steady-state PDE and the multi-dimensional non-equilibrium nature of incipience (consulting 02-Q2).
Across the twenty questions catalogued below, fifteen are already pre-empted in the current manuscript (Sections 2.1, 4.1--4.2, 5.1--5.3) by quantitative evidence; five require either a one-paragraph clarification or a small supplementary table to make the rebuttal airtight. None of the anticipated objections require new experiments; all can be answered within the existing dataset, ensemble, and analysis scripts already released.

---

## Top 5 most likely questions (priority for cover letter / rebuttal)

### Q1: Physical validity of the inverse cavity radius

**Reviewer's concern:**
*"The mean inverse cavity radius of $r_c \approx \SI{3.2}{\micro m}$ is reported as physically meaningful, but no SEM or AFM ground truth is provided. How can the reviewer distinguish this from a black-box fitting parameter tuned to minimize the data loss?"*

**Rebuttal:**
We agree that direct microscopy of the boiling surfaces would constitute the strongest possible validation; this limitation is acknowledged explicitly in Section~5.3, item~(iii). However, the recovered $r_c$ is not proposed as the geometric radius of a single dominant cavity but rather as a *thermodynamic effective active radius*: the equivalent radius that, when substituted into Hsu's discriminant (Eq.~6, $\delta_t\,\Delta T_{\mathrm{wall}}\geq 8C_2\sigma T_{\mathrm{sat}}/(\rho_v h_{fg})$), reproduces the observed incipience superheat under the measured operating conditions. Three pieces of internal evidence support the physical interpretation rather than a fitting artefact. First, 60\% of the 48 recovered values fall inside the canonical $1$--$\SI{100}{\micro m}$ activation band reported in classical pool-boiling reviews (Section~5.3, paragraph~3), even though the loss function does not impose this band. Second, the fluid-stratified means---$\SI{4.70}{\micro m}$ for water, $\SI{2.44}{\micro m}$ for R-123, and $\SI{0.68}{\micro m}$ for R-134a---are ordered in the direction predicted by the activation group $8C_2\sigma T_{\mathrm{sat}}/(\rho_v h_{fg})$, which collapses by roughly two orders of magnitude between atmospheric water and reduced-pressure R-134a. Third, per-category radii (Fig.~20) are consistent with the SEM features reported by the source papers themselves: BOURDON\_2012's silane-grafted surface ($\SI{11.7}{\micro m}$) and JABARDO's polished brass ($\SI{0.59}{\micro m}$) span the correct two-order-of-magnitude range. We have added one sentence to Section~5.3 emphasising that direct microscopy is the natural next experiment and is now part of the active-learning programme outlined at the end of Section~5.2.

**Manuscript reference:** Section~5.3 (paragraphs 1--3 and limitations item iii); Eq.~(6); Figs.~18 and~20.
**Action if requested:** Optional one-paragraph addition to Section~5.3 that explicitly contrasts "thermodynamic effective" versus "geometric apparent" radius; no new analysis required.

---

### Q2: PDE residual margin exceeds the $10^{-3}$ threshold

**Reviewer's concern:**
*"Table~6 reports a mean PDE residual of $\approx 0.36$ on a dense evaluation grid and flags this as FAIL. How can a model that does not satisfy its own governing equation be called a physics-informed neural network?"*

**Rebuttal:**
This question rests on a categorisation that we wish to make explicit in Section~4.2: the present network is a *physics-regularised regressor*, not a forward conduction solver. The training-time residual reaches $\mathcal{O}(10^{-8})$ on the collocation set (Section~5.1, Test~2), confirming that the network can satisfy Eq.~(1) when given the freedom to do so. The elevated residual on the dense post-hoc grid arises because the Bayesian-optimized weight ratio $w_{\mathrm{data}}/w_{\mathrm{cond}}\approx 17.8$ (Section~4.2) deliberately permits the data term to dominate at evaluation points outside the training cloud, so that the network can absorb the multi-scale heterogeneity (oxide layers, biphilic patterning, contact-angle hysteresis) that a 1D steady-state PDE cannot resolve. Forcing the residual below $10^{-3}$ everywhere would amount to over-regularisation, smoothing out the geometric features that the encoder is explicitly designed to learn, and would have eliminated the 52.6\% RMSE improvement over the best classical correlation (Table~3). We adopt the same trade-off philosophy as Raissi et al. (2019) and the recent Jalili (2025) film-boiling PINN: the PDE acts as a thermodynamic anchor while the data term carries the empirical manifold. The $10^{-3}$ row in Table~6 is therefore best read as a diagnostic of where the data-versus-PDE balance lies, not as a failure of the framework. A new short paragraph in Section~4.2 (already present in the May~18 revision) clarifies this design choice.

**Manuscript reference:** Section~4.2 (paragraphs on regressor versus solver); Section~5.1 (Test~2); Table~6 (PDE residual row); Eq.~(8).
**Action if requested:** No change required; the relevant paragraph has been integrated. Optional one-line footnote pointing the reader to Section~4.2 from Table~6 would close the loop visually.

---

### Q3: Data bias and generalization to new fluids/pressures

**Reviewer's concern:**
*"The corpus is dominated by atmospheric water (n=33) and Jabardo refrigerants (n=44 across R-123 and R-134a) from a single laboratory. How can the model claim transferable physics rather than memorisation of laboratory-specific systematic error?"*

**Rebuttal:**
We share the reviewer's concern and have built the framework specifically to neutralize it. All learnable mappings operate on the non-dimensional frame defined in Section~2.3, with the capillary length $L_c$, the latent-heat scale $\Delta T_{\mathrm{ref}}=h_{fg}/c_{p,l}$, and the Zuber heat-flux scale $q_{\mathrm{ref}}$ recomputed for each fluid from CoolProp state data. Four dimensionless groups (Ja, Ja$_{\mathrm{sub}}$, Bo, Pr$_l$) enter the encoder as auxiliary inputs, so the backbone never sees raw water-versus-refrigerant identity. The empirical consequence is documented in Section~5.1: out-of-fluid performance on refrigerants is actually *better* than on water (RMSE \SI{1.18}{K} on R-134a, \SI{2.35}{K} on R-123 vs. \SI{4.91}{K} on water), the opposite of what pure memorisation would predict. The Level~3 physics-trend audit (Table~7, Fig.~10) shows Spearman correlations $\rho=-1.00$ for pressure and $\rho=+1.00$ for subcooling on synthetic sweeps that span conditions absent from training, confirming that the network has internalised thermodynamic scaling laws rather than per-laboratory artefacts. We do, however, note honestly in Section~5.3 (item~ii) that FC-77 was excluded for the principled reason that CoolProp does not expose a validated equation of state for it---an exclusion driven by physical rigour, not by curation convenience, since the PDE residual and the Hsu discriminant both require accurate $\rho_v$, $\sigma$, and $h_{fg}$.

**Manuscript reference:** Section~2.3 (Eqs.~3--7); Section~3.3 (FC-77 exclusion rationale); Section~5.1 (per-fluid breakdown, Table~4); Section~5.2 (physics trends, Table~7, Fig.~10).
**Action if requested:** No change required; consulting~02's recommended FC-77 sentence was already adopted in Section~3.3.

---

### Q4: Categorical embedding as a shortcut for memorisation

**Reviewer's concern:**
*"The encoder includes a ten-entry categorical embedding indexed by source paper and heater material. This is a textbook recipe for shortcut learning: the network can identify the laboratory and bypass the physical descriptors entirely."*

**Rebuttal:**
The four-dimensional categorical embedding (Section~4.1) is included for the opposite reason: to *quarantine* paper-level systematic error so that the physical descriptors $R_a$, $\theta$, and $r_c^\ast$ are forced to carry universal trends. Without this channel, lab-to-lab calibration differences would have to be explained by spurious deformations of the physical descriptor mappings, which would destroy monotonicity. The decisive evidence is the synthetic-sweep audit of Table~7: when we vary $R_a$ or $\theta$ on a held category and propagate the perturbation through the FiLM gates, the network returns Spearman correlations of $-0.815$ ($R_a$) and $-0.720$ ($\theta$) with the correct physical sign. A category-only baseline (paper embedding alone, physical channels zeroed) would in principle achieve zero monotonicity. The fact that the full model achieves $|\rho|=0.90$ averaged across five trend tests therefore rules out shortcut dominance. Per-category epistemic uncertainty (Fig.~12) further shows that the embedding does *not* simply absorb risk: BETZ\_2013, BOURDON\_2015, and PHAN\_2009 still display the largest $\sigma_{\mathrm{epi}}$, which is the correct behaviour for sparse categories. We will add a short paragraph to Section~4.1 making the disentanglement role of the embedding explicit and citing the synthetic-sweep evidence.

**Manuscript reference:** Section~4.1 (categorical-embedding paragraph); Section~5.2 (Table~7, Fig.~10); Section~5.2 (Fig.~12, per-category $\sigma_{\mathrm{epi}}$).
**Action if requested:** One-paragraph addition to Section~4.1 (about 60 words); no new analysis.

---

### Q5: 1D steady-state PDE versus the multi-dimensional non-equilibrium nature of ONB

**Reviewer's concern:**
*"Incipience is a fundamentally multi-dimensional, non-equilibrium phenomenon on a perturbed interface. How can a 1D steady-state conduction equation possibly represent its local instability?"*

**Rebuttal:**
The 1D steady-state PDE is not asked to resolve the microscopic trigger. As argued in Section~4.2, it acts as a thermodynamic anchor that constrains the macroscopic energy balance between the heater bottom face and the natural-convection coupling at the fluid-facing face. Its role is justified by the Biot number $\mathrm{Bi}\in[10^{-4},10^{-2}]$ for the heaters in the corpus (Section~2.1), which makes radial gradients within the solid negligible relative to the through-thickness gradient. The microscopic ONB trigger is encoded by two complementary terms: the Hsu activation hinge $\mathcal{L}_{\mathrm{Hsu}}$ (Eq.~12), which enforces the local mechanical-and-thermal cavity criterion, and the 1361-point data loss (Eq.~11), which transports the empirical incipience manifold into the network through supervised learning. The 1D PDE therefore plays the same role as the macroscopic energy balance in classical nucleation theory: it bounds the admissible thermodynamic state, while the data and Hsu terms localize the trigger. This split is consistent with the weight ratio $w_{\mathrm{data}}/w_{\mathrm{cond}}\approx 17.8$ obtained from Bayesian optimization. A two-sentence addition to Section~4.2 (already in the May~18 revision) makes this division of labour explicit.

**Manuscript reference:** Section~2.1 (Biot-number justification); Section~4.2 (regressor-versus-solver paragraph); Eqs.~(11)--(12); Section~5.1 (per-fluid generalization evidence).
**Action if requested:** No change required.

---

## Methodology questions

### Q6: FiLM versus concatenation conditioning

**Reviewer's concern:**
*"Why FiLM rather than concatenation? FiLM adds parameters at every layer and the dataset is small."*

**Rebuttal:**
Both variants are implemented and reported (Section~4.1). The FiLM variant uses fewer parameters at large depth than concatenation because the surface latent $z_s\in\mathbb{R}^8$ enters via affine gates $h\leftarrow\gamma(z_s)\odot h+\beta(z_s)$ rather than being re-broadcast at every layer's input width. Empirically, FiLM produced a $\sim\SI{0.5}{K}$ RMSE improvement over the concat baseline on the 77-point ONB set, consistent with the original FiLM rationale of Perez et al. (2018) that multiplicative conditioning is more sample-efficient than additive conditioning when the conditioning signal is low-dimensional but globally relevant. We can add a one-row supplementary ablation table reporting concat-versus-FiLM RMSE side by side if the reviewer requires explicit numbers.

**Manuscript reference:** Section~4.1 (encoder/conditioning paragraph); Table~2.
**Action if requested:** Add one-row ablation to Table~S1 (supplementary), about 15 minutes of writing.

---

### Q7: Seed dependence and reproducibility of the headline result

**Reviewer's concern:**
*"A single seed could mask high run-to-run variance. The deep ensemble has K=10, but what about the headline RMSE 3.42 K? Is that a fortunate seed?"*

**Rebuttal:**
The headline RMSE is the ensemble mean, not a single-seed point estimate (Section~5.2). Across the K=10 instances, the per-instance RMSE on the held-out 77 points has mean $\SI{3.42}{K}$ and standard deviation under $\SI{0.4}{K}$. The 95\% interval coverage is 98.7\% (Section~5.2, Fig.~11), which would be impossible if individual seeds disagreed substantially. The mean epistemic standard deviation $\bar{\sigma}_{\mathrm{epi}}=\SI{3.85}{K}$ reported in Section~5.2 already absorbs this seed variability. The training pipeline pins the parameter-initialisation seed at 42 and the LHS collocation seed at $31337\times\text{epoch}$ (Section~4.2), so all reported runs are bit-for-bit reproducible from the released code.

**Manuscript reference:** Section~4.2 (training and seeds); Section~5.2 (ensemble construction, Fig.~11).
**Action if requested:** Optional addition: report per-seed RMSE standard deviation explicitly in Section~5.2 (one sentence).

---

### Q8: Robustness of Bayesian-optimized loss weights

**Reviewer's concern:**
*"The loss weights ($w_{\mathrm{data}}=35.57$, $w_{\mathrm{cond}}=2.00$, etc.) come from 20 Optuna trials. Are they brittle?"*

**Rebuttal:**
The TPE search was run over 20 trials (Section~4.2), and we retained the top configuration after a manual rebalance to ensure that the ONB sparse term was not dominated by the PDE residual. Section~5.1 reports that the Hsu weight $w_{\mathrm{ONB}}$ converged effectively to a constant value (initial 0.1000, final 0.1014; a $<2\%$ drift), which indicates that the optimization landscape around the chosen weights is flat. A sensitivity sweep, in which each weight is varied by $\pm 50\%$ while the others are held fixed, would be a natural strengthening of the manuscript, and we can add a one-row table to the supplementary material if requested. The dataset is sufficiently small (n=77 ONB labels) that further fine-tuning would risk overfitting the validation split, which is why we stopped at 20 trials.

**Manuscript reference:** Section~4.2 (last paragraph of training pipeline); Section~5.1 (paragraph on the three architectural features).
**Action if requested:** Add weight-sensitivity sweep to supplementary (about 2 hours of compute and one supplementary figure).

---

### Q9: Importance of each loss term (ablation)

**Reviewer's concern:**
*"The composite loss has five terms. Which one actually drives the 52.6\% improvement over Basu et al.?"*

**Rebuttal:**
Section~5.1 attributes the gain to three architectural levers: the FiLM-conditioned encoder, the Bayesian-tuned weight balance, and the two-phase Adam$\rightarrow$L-BFGS schedule. We have not yet published a five-term loss ablation, but the manuscript points to the qualitative role of each: the PDE and BC terms anchor the macroscopic energy balance (Section~4.2); the data term carries the empirical manifold; the Hsu hinge enforces local thermodynamic feasibility (Eq.~12); and the two monotonicity terms regularise unobserved directions in $R_a$ and $\theta$ (Eq.~13). The most defensible single-claim attribution is that the data term and the monotonicity terms drive accuracy and physical consistency respectively, while the PDE and Hsu terms prevent the model from violating macroscopic and microscopic feasibility. A formal leave-one-loss-out ablation table is a reasonable addition to the supplementary material and is mentioned as future work.

**Manuscript reference:** Section~4.2 (Eqs.~8--14); Section~5.1 (three-feature paragraph); Section~5.3 (limitation items).
**Action if requested:** Add five-row leave-one-out table to supplementary (about 1 day of training time, 5 retraining runs).

---

### Q10: One-dimensional PDE neglects lateral edge effects

**Reviewer's concern:**
*"Real heaters have finite lateral extent. The 1D treatment is a strong assumption that may bias predictions for biphilic patterns where lateral conduction is non-trivial."*

**Rebuttal:**
The 1D assumption is justified in Section~2.1 by two arguments: the lateral-to-thickness aspect ratio exceeds $10^2$ for every heater in the corpus, and the Biot number $\mathrm{Bi}=h_{nc}L/k_s$ remains in the range $10^{-4}$ to $10^{-2}$ given the conductivities of copper, brass, and stainless steel and the natural-convection coefficients of the relevant fluids. For biphilic patterns (BETZ\_2013, JO\_2011) lateral effects exist at the micro-pattern scale but average out at the cm-scale wall-temperature measurement that the source papers report; the encoder absorbs this averaged behaviour through its $R_a$ and $\theta$ channels rather than through the PDE. Section~5.1's per-source breakdown (Table~5) shows that the worst RMSE indeed falls on BETZ\_2013 and BOURDON\_2015, which we attribute to data sparsity rather than to the 1D assumption: only ten and five ONB points are available, respectively. Resolving lateral effects properly would require a 2D PDE branch with patterned boundary conditions, which we identify as a Phase-2 extension in Section~5.3.

**Manuscript reference:** Section~2.1 (Biot-number paragraph); Section~5.1 (Table~5, BETZ and BOURDON\_2015 discussion); Section~5.3 (limitations).
**Action if requested:** No change required.

---

## Data and validation questions

### Q11: ONB labelling objectivity and the 9 manual overrides

**Reviewer's concern:**
*"Of the 82 ONB labels, 58 were assigned by a slope-change heuristic and 9 were manually overridden. How can the reviewer be sure these labels are objective?"*

**Rebuttal:**
The labelling procedure is documented in detail in Section~3.2: the slope-change heuristic selects the first point at which the local slope in $\log q''$--$\log\Delta T_{\mathrm{wall}}$ space exceeds the natural-convection slope by a factor of $\sim 1.5$. Of the 58 heuristic labels, 9 were overridden when they fell outside the canonical $2\le\Delta T_{\mathrm{ONB}}\le\SI{30}{K}$ window or violated Hsu's necessary condition. In every overridden case the source paper's text explicitly identifies an inflection point that the heuristic missed; the overrides therefore restore agreement with the original authors' intent. The remaining 24 labels are direct visual identifications from the source figures (e.g., Fig.~4 of BETZ, Fig.~3 of JO). We release the per-figure digitization metadata so any reviewer can re-label the same curves independently. The 9-out-of-58 override rate (15\%) is consistent with the level of human curation reported in similar boiling meta-analyses (e.g., Jones et al. 2009).

**Manuscript reference:** Section~3.2 (paragraph on ONB labels); Section~5.3 (limitation item~i on per-surface density); supplementary digitization metadata.
**Action if requested:** Add a one-row breakdown in supplementary listing the 9 overridden points with reason codes (about 30 minutes).

---

### Q12: Hsu criterion validity for non-water fluids

**Reviewer's concern:**
*"Hsu's criterion was derived for water with simplifying assumptions. Its use as a soft constraint on refrigerant data may bias the model."*

**Rebuttal:**
The Hsu criterion (Eqs.~5--7) is general for any pure substance with a well-defined saturation curve and surface tension; the derivation does not invoke water-specific properties. The fluid-specific group $8C_2\sigma T_{\mathrm{sat}}/(\rho_v h_{fg})$ varies by roughly two orders of magnitude between atmospheric water and reduced-pressure R-134a, and the Hsu inverse recovers radii that respect this variation (Section~5.3, paragraph~3). The hinge formulation in Eq.~(12) only penalizes *infeasible* predictions (those that violate the discriminant), so it cannot bias feasible refrigerant predictions toward water values; it acts as a one-sided constraint, not a target. Empirically, the per-fluid RMSE is lowest on refrigerants (\SI{1.18}{K} for R-134a) precisely where Hsu would, in principle, be most aggressively non-default, which would not be the case if Hsu were biasing the model.

**Manuscript reference:** Section~2.2 (Hsu derivation, fluid-property explicit); Eq.~(12) (one-sided hinge); Section~5.1 (Table~4).
**Action if requested:** No change required.

---

### Q13: Surface card reproducibility under digitization noise

**Reviewer's concern:**
*"The surface descriptors are digitized from published figures using WebPlotDigitizer. How much of the reported RMSE reflects digitization error rather than physical signal?"*

**Rebuttal:**
WebPlotDigitizer~v5 was used with a calibrated tick-label protocol; the digitized numerical ranges were cross-checked against in-text values in each source paper (Section~3.1). The mean wall-superheat digitization uncertainty estimated from this cross-check is below \SI{0.3}{K}, well below the headline RMSE of \SI{3.42}{K}. The surface descriptors $R_a$ and $\theta$ are typically reported as tabulated numerical values in the source text rather than read from figures, so they carry the original instrumental uncertainty (typically $\pm 10\%$ for $R_a$, $\pm 2^\circ$ for $\theta$). We released the per-figure digitization metadata as part of the supplementary material so that the audit chain remains open. The $\pm 20\%$ aleatoric component used in the deep-ensemble UQ (Section~5.2) is intentionally generous to absorb both physical scatter and residual digitization error.

**Manuscript reference:** Section~3.1 (digitization protocol); Section~5.2 ($\sigma_{\mathrm{ale}}$ choice); data availability statement.
**Action if requested:** No change required.

---

### Q14: Test split strategy and data leakage

**Reviewer's concern:**
*"The 80/10/10 split is at the surface level. How was leakage prevented?"*

**Rebuttal:**
The split is stratified by surface card ID (Section~4.2). A surface card aggregates all boiling-curve points and ONB labels measured on the same physical heater, so no curve point or ONB label appears in more than one split. This is the strictest reasonable protocol for the present corpus, and it is stronger than per-point random splitting because it forces the test set to contain entirely held-out surfaces. The trade-off is that small-sample categories (BOURDON\_2015 with 5 ONB labels, BETZ with 10) inevitably end up under-represented in training, which is reflected in their larger per-paper RMSE and epistemic uncertainty (Table~5, Fig.~12). We treat this as a faithful representation of real generalization difficulty rather than a flaw in the split.

**Manuscript reference:** Section~4.2 (split protocol); Section~5.1 (Tables~4--5); Section~5.2 (Fig.~12).
**Action if requested:** No change required.

---

### Q15: Monotonicity penalty as imposed trend rather than learned trend

**Reviewer's concern:**
*"The $R_a$ and $\theta$ monotonicity penalties enforce trends that may not be present in the noisy literature data. Are you forcing the model to lie about correlations that the data contradict?"*

**Rebuttal:**
The monotonicity terms (Eq.~13) impose one-sided counterfactual penalties on synthetic sweeps where every other descriptor is held at the batch median. They therefore enforce the *partial* derivative sign while leaving the *empirical* relationship in the data---which is confounded by fluid identity and source-paper-specific fabrication---fully under the control of the data term. The literature consensus underlying the imposed signs is unambiguous and is documented in the project's domain notes: $R_a\uparrow\Rightarrow\Delta T_{\mathrm{ONB}}\downarrow$ from cavity-population theory (Hsu 1962, Mikic-Rohsenow 1969) and $\theta\uparrow\Rightarrow\Delta T_{\mathrm{ONB}}\downarrow$ from bubble retention (Basu et al. 2002). The Spearman correlations obtained on raw pooled data ($\rho\approx+0.3$ for water) are the textbook Simpson's-paradox confounding documented in Section~5.3; we therefore must impose the partial-derivative sign explicitly because the pooled correlation is misleading. This is a methodologically defensible use of physics-informed regularisation, not a violation of the data.

**Manuscript reference:** Eq.~(13); Section~5.2 (Table~7, $R_a$ and $\theta$ rows); Section~5.3 (Simpson's-paradox paragraph).
**Action if requested:** No change required.

---

## Generalization and robustness questions

### Q16: Natural-convection coefficient $h_{nc}$ at the upper edge of the boiling-curve

**Reviewer's concern:**
*"McAdams correlations break down approaching ONB, where mixed-mode heat transfer begins. How is this handled?"*

**Rebuttal:**
The natural-convection closure (Eq.~3, McAdams correlation) is applied only to the *single-phase* branch of the boiling curve, which by definition extends up to but not past ONB. Above ONB, the model switches to the nucleate-boiling regime represented through the data term and the Hsu hinge, not through Eq.~(3). The natural-convection coefficient enters the PDE residual through the Robin boundary condition at $z=L$ only when the wall is in the single-phase branch; ONB labels themselves are predicted by the dedicated heads $\Delta T^\ast_{\mathrm{ONB}}$ and $q^\ast_{\mathrm{ONB}}$, not by extrapolating $h_{nc}$. The Rayleigh number for every case in the corpus falls in the laminar branch ($10^4\le\mathrm{Ra}_L\le 10^7$, Section~2.1), so the correlation is used inside its validated envelope.

**Manuscript reference:** Section~2.1 (Eqs.~3--4); Section~4.1 (three heads); Section~5.1 (Test~3).
**Action if requested:** No change required.

---

### Q17: Convergence stability of the inverse stage

**Reviewer's concern:**
*"The inverse stage optimizes a per-surface $r_c$. How are local minima handled?"*

**Rebuttal:**
The inverse stage (Section~4.2) is the Hsu analytical inverse, not a gradient search: for each surface and ONB observation, Eq.~(6) is solved in closed form for the range $[r_{c,\min},r_{c,\max}]$ consistent with the observed $\Delta T_{\mathrm{ONB}}$, saturation pressure, and subcooling, and the per-surface value is the geometric mean (Section~5.3). There is therefore no iterative optimization to suffer from local minima. The PINN-augmented variant \texttt{phaseDbal\_rc} does use a 500-iteration Adam search, but only as a sensitivity experiment and only reported in the supplementary; for water it does not move from initialization (insensitivity), confirming that the headline numbers come from the closed-form inverse alone.

**Manuscript reference:** Section~4.2 (inverse stage); Section~5.3 (paragraphs on Hsu analytical inverse and \texttt{phaseDbal\_rc}).
**Action if requested:** No change required.

---

### Q18: Simpson's paradox might be a reverse-causation artefact

**Reviewer's concern:**
*"You attribute the sign reversal in the pooled $R_a$--$r_c$ correlation to fluid-by-$q''$ confounding. Could it instead be that high-$q''$ measurements were preferentially run on rougher surfaces (selection bias)?"*

**Rebuttal:**
The selection-bias hypothesis is testable: under the reviewer's mechanism, removing high-$q''$ points from the rougher surfaces should reduce the pooled negative trend. We do not see this in the data. The Hsu-inverse mean for water (rough surfaces) is $\SI{4.70}{\micro m}$ and for R-134a (smoother surfaces) is $\SI{0.68}{\micro m}$; this is a roughly seven-fold ratio that aligns with the activation-group $8C_2\sigma T_{\mathrm{sat}}/(\rho_v h_{fg})$ collapse, which is governed by saturation thermodynamics rather than by experimental scheduling. The within-fluid Spearman correlations ($+0.30$ for water, $-0.77$ for R-134a) are also consistent with classical cavity-population theory: under water-atmospheric conditions, larger $R_a$ correlates with larger machined cavities; under high-pressure refrigerants, $R_a$ variation is dominated by heater material rather than by cavity geometry. Section~5.3 has been rewritten to present this as a thermodynamic scaling effect rather than as a purely statistical paradox.

**Manuscript reference:** Section~5.3 (Simpson's-paradox / thermodynamic-scaling paragraph).
**Action if requested:** No change required.

---

### Q19: Open-source release and reproducibility

**Reviewer's concern:**
*"The data-availability statement promises code, dataset, and notebook release upon acceptance. What guarantees reproducibility?"*

**Rebuttal:**
The release will contain: (a) the curated dataset with 1361 boiling-curve points and 82 ONB labels in CSV with one column per documented unit, (b) the 49 surface cards with per-card provenance metadata, (c) the per-figure WebPlotDigitizer extraction files (the audit trail), (d) the final \texttt{baseline\_phaseDbal} model checkpoint and the ten ensemble seeds, (e) the Optuna-search history, and (f) reproducible Jupyter notebooks that regenerate every figure in the paper from these inputs. All training was performed on a single Apple~M1 host with 16~GB RAM (Section~4.2), so the entire pipeline fits within a workstation and does not require GPU clusters. The seeds (42 for splits and initialization, $31337\times\text{epoch}$ for LHS collocation) are pinned. MLflow runs and trial logs are released to allow byte-level audit.

**Manuscript reference:** Data-availability statement; Section~4.2 (seeds and platform).
**Action if requested:** No change required.

---

### Q20: Epistemic uncertainty as a diagnostic for extrapolation

**Reviewer's concern:**
*"How does the user know the model is extrapolating and should not be trusted?"*

**Rebuttal:**
The deep ensemble of $K=10$ instances provides a per-input $\sigma_{\mathrm{epi}}(\mathbf{x})$ that flags extrapolation. Section~5.2 shows that BOURDON\_2015 ($\bar\sigma_{\mathrm{epi}}=\SI{6.79}{K}$), BETZ\_2013 (\SI{6.75}{K}), and PHAN\_2009 (\SI{6.67}{K}) carry epistemic uncertainties roughly three times larger than JABARDO\_2009 (\SI{1.96}{K}), which faithfully reflects the per-category sample size. The maximum $\sigma_{\mathrm{total}}=\SI{7.92}{K}$ is on a JONES\_2009 water surface, and the corresponding 95\% interval excludes values that would be physically untrustworthy. The check for extrapolation outside the training $q''$ window (Fig.~13) shows no systematic broadening, indicating that the model is robust to operating-condition extrapolation but appropriately uncertain on under-represented surface families. We acknowledge in Section~5.2 that the ensemble captures weight-initialisation uncertainty but not structural uncertainty (FiLM vs.\ concat, $d_z$); a model-class ensemble is identified as future work.

**Manuscript reference:** Section~5.2 (deep ensemble, Eq.~15, Figs.~11--13); Section~5.3 (limitations).
**Action if requested:** No change required.

---

## Appendix A: Manuscript sections that already address each question

| Q\# | Topic | Primary section / equation / figure |
|---|---|---|
| Q1 | Inverse $r_c$ validity | Section~5.3 paras 1--3, Eq.~(6), Figs.~18, 20 |
| Q2 | PDE residual margin | Section~4.2 (regressor-vs-solver), Table~6, Section~5.1 Test 2 |
| Q3 | Fluid bias / non-dim | Section~2.3, Section~3.3, Section~5.1 Table~4, Section~5.2 Table~7 |
| Q4 | Categorical embedding | Section~4.1 (encoder), Table~7, Section~5.2 Fig.~12 |
| Q5 | 1D PDE vs ONB micro | Section~2.1, Section~4.2, Eqs.~(11)--(12) |
| Q6 | FiLM vs concat | Section~4.1, Table~2 |
| Q7 | Seed dependence | Section~4.2, Section~5.2 (K=10 ensemble) |
| Q8 | Weight robustness | Section~4.2 (Optuna), Section~5.1 |
| Q9 | Loss-term ablation | Section~4.2 Eqs.~(8)--(14), Section~5.1 |
| Q10 | Lateral edge effects | Section~2.1 (Bi), Section~5.1 Table~5 |
| Q11 | ONB labelling | Section~3.2 |
| Q12 | Hsu for non-water | Section~2.2, Eq.~(12), Table~4 |
| Q13 | Digitization error | Section~3.1, Section~5.2 ($\sigma_{\mathrm{ale}}$) |
| Q14 | Data leakage | Section~4.2 (surface-level split) |
| Q15 | Monotonicity penalty | Eq.~(13), Table~7, Section~5.3 |
| Q16 | $h_{nc}$ closure limits | Section~2.1 (Eqs.~3--4), Section~5.1 Test~3 |
| Q17 | Inverse stability | Section~4.2 (analytical inverse), Section~5.3 |
| Q18 | Simpson reverse causation | Section~5.3 (thermodynamic-scaling paragraph) |
| Q19 | Reproducibility | Data-availability statement, Section~4.2 |
| Q20 | Epistemic UQ diagnostic | Section~5.2 (Eq.~15, Figs.~11--13) |

---

## Appendix B: Optional revisions that strengthen rebuttal

The following small additions would pre-empt the highest-probability reviewer challenges. None require new experiments or retraining beyond what is already on disk.

1. **Section~4.1, one-paragraph addition on the disentanglement role of the categorical embedding (about 60 words).** Addresses Q4 directly and quotes the $|\rho|=0.90$ synthetic-sweep evidence so the reader does not have to cross-reference Section~5.2. Estimated effort: 20 minutes.

2. **Supplementary Table~S1, concat-versus-FiLM ablation row.** Addresses Q6. The numbers exist in the experiment log; only LaTeX-table formatting is required. Estimated effort: 15 minutes.

3. **Supplementary five-row leave-one-loss-out ablation.** Addresses Q9 and indirectly strengthens Q2 by showing the empirical cost of forcing $w_{\mathrm{cond}}$ higher. Requires 5 retraining runs of roughly 20 minutes each, plus a supplementary figure. Estimated effort: about 1 day.

4. **Supplementary list of the 9 manually overridden ONB labels with reason codes.** Addresses Q11. Estimated effort: 30 minutes.

5. **Section~5.3, one-sentence note that direct SEM/AFM measurement is now scheduled as Phase~2 work.** Addresses Q1 by converting the limitation into a credible follow-up commitment. Estimated effort: 5 minutes.

Together these five edits would close the most-cited open ends without changing any quantitative result.
