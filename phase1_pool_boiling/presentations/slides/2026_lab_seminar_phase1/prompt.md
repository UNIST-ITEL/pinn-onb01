# Slide Deck Request — Lab Seminar (Phase 1 PINN-ONB)

## Meta

- **Audience**: Lab seminar (UNIST ITEL internal — boiling / heat-transfer 전공 동료 + 지도교수)
- **Duration**: 25 min talk + 10 min Q&A
- **Slide count target**: 15-17 (excluding title + Q&A invitation)
- **Theme**: academic, minimal, white background, navy / muted-blue accent
- **Equation rendering**: LaTeX preserved (lab seminar이므로 수식 OK)
- **Aspect ratio**: 16:9
- **Submission context**: IJHMT 제출 완료 (2026-05-18), review 대기 중

## Topic

**Surface-Conditioned Physics-Informed Neural Network for Pool-Boiling
Onset of Nucleate Boiling**

- Authors: Jaeseon Lee*, Gyuchang Kim, Eunjeong Ko, Yujin Kim (UNIST ITEL)
- Target journal: International Journal of Heat and Mass Transfer
- Submission date: 2026-05-18

## Narrative arc (15 slides)

1. Title
2. Outline + ONB의 산업적 중요성
3. Problem: ONB 예측의 어려움 — classical correlation 한계
4. Why PINN? — data + physics hybrid의 자연스러운 fit
5. Approach 개요 — Hsu criterion + surface encoder + composite loss
6. Mathematical formulation (Hsu nucleation + 1D conduction + NC BC)
7. Surface encoder + FiLM conditioning
8. Composite loss (5 terms) + 4-phase training
9. Dataset — 49 surfaces, 82 ONB labels, 4 fluids
10. **Main result**: parity plot — PINN vs 5 classical correlations
11. **Ablation**: refrigerant subset −65~67% RMSE 감소 핵심 강조
12. Physics validation — 8/9 trends pass + 1 Simpson reversal
13. Deep ensemble UQ — coverage 98.7%
14. Hsu inverse — Simpson's paradox 발견 (Ra ↑ ↔ r_c ↓ confounded)
15. Future work (Phase 1.5 in-house augmentation, Phase 2 flow boiling)
   + Q&A invitation

## Key numbers to highlight (large font)

- **RMSE 3.42 K** (PINN) vs **7.21 K** (best classical, Basu et al.) — **−53%**
- Refrigerant subset: **−65% ~ −67%** RMSE reduction
- $R^2 = +0.44$ (PINN) vs negative for all classical
- **Coverage 95% credible interval: 98.7%** (target 95%)
- **Hsu inverse**: mean $r_c = 3.21$ μm, **60% in [1, 100] μm** 물리 영역
- **Dataset**: 1361 boiling-curve points, **82 ONB labels**, 49 surfaces, 4 fluids, 7 papers
- **24,005 PINN parameters**, deep ensemble K=10
- Best classical correlation tested: 5 (Hsu 1962, Davis-Anderson 1966, Bergles-Rohsenow 1964, Sato-Matsumura 1964, Basu et al. 2002)

## Per-slide content

### Slide 1 — Title (1 min)

- **Title**: Surface-Conditioned PINN for Pool-Boiling ONB
- Authors: Jaeseon Lee*, Gyuchang Kim, Eunjeong Ko, Yujin Kim
- Affiliation: Innovative Thermal Engineering Laboratory (ITEL), UNIST
- Date: <YYYY-MM-DD>
- Footer: IJHMT submitted 2026-05-18

### Slide 2 — Outline (1 min)

5 bullets:
- Motivation: why ONB prediction matters
- Approach: PINN + Hsu + surface encoder
- Dataset: 7 lab corpus, 49 surfaces
- Results: −53% RMSE vs best classical
- Future: in-house augmentation + flow boiling extension

### Slide 3 — Problem (2 min)

- Pool boiling = 고밀도 열전달의 enabler (CHF의 ~70%까지 안정)
- ONB = nucleate boiling 시작점 — 표면 모드 전환, 효율적 design point
- Classical correlation 한계:
  - Idealized cavity-distribution 가정
  - 측정-예측 scatter 20-30%
  - 표면 개질 (wettability, biphilic, roughness) 미반영
- Figure: boiling curve schematic with ONB marked (or **fig02_correlation_parity** 일부)

### Slide 4 — Why PINN here? (1.5 min)

- Data scarcity (82 labels는 deep ML 표준에 미달)
- 풍부한 physics (Hsu criterion, conduction, NC BC)
- → physics 가 regularizer 역할 → small-data + multi-source 적합
- Recent PINN-ONB trend cite: Jalili 2025, Li-Kharangate 2025, Huang 2024 (1 사이드 mention)

### Slide 5 — Approach overview (1.5 min)

Diagram (Figure-style):
- Inputs: surface descriptors (Ra, θ, r_c, N_s) + heat flux q''
- Surface encoder (FiLM) → latent z
- 1D conduction PINN → T(z)
- Loss: PDE + BC + data + Hsu + monotonicity (5 terms)
- Output: ΔT_ONB prediction

### Slide 6 — Mathematical formulation (3 min, 가장 dense)

- 1D Laplace: $\frac{d^2T}{dz^2} = 0$
- BC: Neumann at heater base ($-k_s\,dT/dz = q''$), Robin/NC at fluid interface
- Natural convection: McAdams Nu = 0.54 Ra^{1/4} (laminar)
- **Hsu nucleation criterion**:
  - $r_{c,min/max} = \frac{\delta_t}{2C_1}\left[1 \mp \sqrt{1 - \frac{8C_2 \sigma T_{sat}}{\delta_t \Delta T_{wall} \rho_v h_{fg}}}\right]$
  - Discriminant condition $\to \Delta T_{ONB} = \sqrt{8 C_2 \sigma T_{sat} q'' / (k_l \rho_v h_{fg})}$
- Dimensionless: $L_c$, $\Delta T_{ref}$, $q_{ref}$

### Slide 7 — Surface encoder (2 min)

- 입력: Ra (μm), θ (°), category (one-hot 10 categories)
- FiLM (Feature-wise Linear Modulation):
  - hidden 활성화 $h$ → $(1 + \gamma(z)) \odot h + \beta(z)$
  - $z$ = surface latent
- Latent dim d_z = 16, hidden_dim = 64, layers = 5
- Parameter count: 24,005

### Slide 8 — Composite loss + training (1.5 min)

- 5 항: $L = w_{PDE}L_{PDE} + w_{BC}L_{BC} + w_{data}L_{data} + w_{ONB}L_{ONB} + w_{mono}L_{mono}$
- 4-phase training: analytical warmup → synthetic → experimental fine-tune → inverse
- Optimizer: Adam → L-BFGS
- HPO via Optuna TPE (30 trials, top-5 reported in supplementary)

### Slide 9 — Dataset (1.5 min)

- Table summary:
  - 7 papers (BETZ, BOURDON-12, BOURDON-15, JABARDO, JONES, JO, PHAN)
  - 49 surfaces, 1361 boiling-curve points, 82 ONB labels
  - 4 fluids: water (33), R-134a (34), R-123 (10), FC-77 (5 — 학습 제외)
  - $\Delta T_{ONB} \in [0.7, 24.9]$ K, $q'' \in [0.1, 1434]$ kW/m²
- Open-source release upon acceptance

### Slide 10 — **Main result: parity plot** (2.5 min) — KEY SLIDE

- **fig03_pinn_parity.png** as the headline visual
- Numbers (large font):
  - PINN: RMSE 3.42 K, R² +0.44
  - Best classical (Basu): 7.21 K, R² −0.21
  - **Improvement: −53%**
- Per-fluid breakdown: water 4.1 K, R-134a 2.8 K, R-123 1.6 K, FC-77 (excluded)

### Slide 11 — Refrigerant subset 강조 (1.5 min)

- **fig02_correlation_parity.png** (PINN vs 5 corrs)
- Highlight: R-134a / R-123 에서 PINN 우위 **−65% ~ −67%**
- 이유: 냉매 데이터는 표면 개질-confounding 적어서 PINN의 surface descriptor가 가장 의미 있게 작동

### Slide 12 — Physics validation (1.5 min)

- **fig07_physics_trends_composite.png**
- 5 monotonicity trends: q ↑→ΔT ↑ / Ra ↑→ΔT ↓ / θ ↑→ΔT ↓ / P ↑→ΔT ↓ / sub ↑→ΔT ↑
- 8 of 9 trends PASS (1 mixed = water dataset confound)
- Energy conservation closure
- Hsu envelope satisfied

### Slide 13 — Deep ensemble UQ (1.5 min)

- **fig04_ensemble_errorbars.png**
- K=10 ensemble, seeds 42-51
- Coverage at nominal 95% = **98.7%** (well calibrated)
- σ_epistemic vs σ_aleatoric breakdown — epistemic dominant
- **fig05_std_by_category.png** brief mention — surface category 별 σ

### Slide 14 — Hsu inverse + Simpson's paradox (2 min) — INTERESTING

- **fig08_inverse_rc_vs_Ra.png** or **fig09_inverse_rc_by_category.png**
- ONB-측정 → r_c 역추정 (Hsu equation inversion)
- Mean r_c = 3.21 μm, 60% in [1, 100] μm 물리 영역
- **Simpson reversal**: aggregate에서 $R_a$ ↑ vs $r_c$ 약한 + 상관; per-category 에서는 − 상관 → **표면 family 변경이 confounding**
- Methodological insight beyond paper number

### Slide 15 — Future work + Q&A (2 min)

- **Phase 1.5** (진행 중): in-house lab data augmentation (laser, corrosion, biphilic)
  - 60-70 surfaces, 100-130 ONB labels 목표
  - Cross-lab generalization (Level 4) 검증
- **Phase 2**: forced-convection subcooled flow boiling
- **Phase 3+**: foundation model, multi-fluid, industrial 응용
- Code + dataset: github.com/UNIST-ITEL/pinn-onb01 (수락 후 공개)
- **Q&A invitation**

## Figures (paths in figure_list.md, separately uploaded to Claude Design)

slide 3: 별도 schematic 없음 — text-only 또는 fig02 발췌
slide 7: surface encoder + FiLM 도식 — Claude Design 에서 자동 생성 또는 사용자 직접 그림
slide 10: fig03_pinn_parity.png — **headline**
slide 11: fig02_correlation_parity.png
slide 12: fig07_physics_trends_composite.png
slide 13: fig04_ensemble_errorbars.png (+ optional fig05)
slide 14: fig08_inverse_rc_vs_Ra.png 또는 fig09_inverse_rc_by_category.png

(상세 경로 → figure_list.md)

## Style notes

- **Equations**: LaTeX render (Claude Design 지원). 핵심만 표시, 부수 derivation 은 backup slide.
- **Bullet density**: 4-5 per slide max. Sub-bullet 1 level까지.
- **Color palette**: navy (#1F4E78) primary text, gray (#7F7F7F) secondary, accent green/red for "improved/worsened" indicator
- **Font**: sans-serif (Helvetica / Arial / Inter). Body 18 pt+, headers 28 pt+.
- **Charts**: 기존 matplotlib figure 그대로 사용 가능 — Claude Design 이 잘 통합
- **References on slides**: 마지막에 references slide 1장 (Hsu 1962, Basu 2002, Jalili 2025, 본 paper bib 31개 중 핵심 5-6개)

## References to cite on slides (Speaker's discretion)

- Hsu 1962 — nucleation criterion 시초
- Basu et al. 2002 — best classical correlation 비교 대상
- Raissi et al. 2019 — original PINN
- Lu et al. 2021 — DeepXDE (방법론 reference)
- Jalili 2025 — recent PINN-ONB
- Li-Kharangate 2025 — cryogenic PINN
- Huang 2024 — bubble dynamics PINN

## Backup slides (Q&A 대비, 시간 부족 시 생략 가능)

- B1: HPO 결과 (Optuna top-5 trials)
- B2: 4-phase training progression
- B3: Per-source RMSE breakdown
- B4: FC-77 exclusion rationale (CoolProp 미지원)
- B5: ΔT_sub effect (PHAN data)

## 청중 예상 Q&A 후보 (Q&A 시간 활용)

1. "왜 deep ensemble만으로 충분한가? Bayesian PINN은?" → 비용/시간 trade-off
2. "Hsu criterion이 너무 단순한 모델 아닌가?" → soft constraint, hard 가정 아님
3. "n=82는 너무 작지 않나?" → Phase 1.5에서 100-130까지 보강 예정
4. "표면 카테고리 임베딩이 무엇을 학습한 건가?" → SHAP 분석은 future work
5. "Simpson reversal은 artifact 가능성?" → JABARDO Cu 데이터 cross-check
6. "Flow boiling 확장 가능성은?" → Phase 2 plan 보유, transfer learning 기반
