# Speaker Notes — 2026 Lab Seminar (Phase 1)

**Total**: 25 min talk + 10 min Q&A = 35 min
**Buffer**: 5 min (안전 margin)
**Effective speaking**: 20 min for 15 slides ≈ **80 sec/slide 평균**

---

## Slide 1 — Title (60 sec)

- 인사 + 본인 소개 (이름, 소속)
- "오늘은 PINN 을 활용한 풀비등 ONB 예측 연구를 소개드리겠습니다.
   IJHMT 에 5월 18일 제출했고 현재 review 대기 중입니다."
- 다음 슬라이드로 넘어가기 전: "공동저자 김규창, 고은정, 김유진 학생들이 함께
  작업했습니다."

## Slide 2 — Outline (45 sec)

- 5개 핵심 챕터 안내
- "전체 25분 talk + 10분 Q&A 예정입니다."
- 청중 attention 유도: "특히 결과 부분 (3-4분 차) 에서 흥미로운
  발견 한 가지를 공유드리겠습니다 — Simpson reversal."

## Slide 3 — Problem (120 sec)

- ONB 의 산업적 중요성: 전자기기 냉각, 원자로 안전, 냉동 시스템 등
- Boiling curve schematic 설명: NC → ONB → nucleate → CHF
- **핵심 강조**: classical correlation 의 한계
  - "20-30% scatter — 산업 design point 결정에는 너무 큼"
  - "표면 개질 (wettability, biphilic, nano-coating) 미반영"
- "그래서 학습 기반 접근이 필요한 시점입니다."

## Slide 4 — Why PINN here? (90 sec)

- 데이터 부족 (n=82) → 순수 ML 어려움
- 풍부한 물리 (Hsu, conduction, NC) → physics regularizer 적합
- "Jalili 2025 등 최근 1년 사이 PINN-ONB 연구가 활발해졌습니다.
   우리 연구의 차별점은 surface descriptor encoding 입니다."
- → 다음 슬라이드: 본격적 접근법

## Slide 5 — Approach overview (90 sec)

- 1단어로 정리: "**Surface-conditioned PINN**"
- 다이어그램 따라 input → encoder → PDE → output 흐름 설명
- "이 framework 가 본 발표의 backbone 입니다.
   다음 3 슬라이드에서 각 component 를 자세히."

## Slide 6 — Mathematical formulation (180 sec — 가장 dense)

- "수학 부분이 가장 dense 합니다. lab seminar니까 자세히 가겠습니다."
- 1D Laplace 가정의 정당화: "heater thickness ≪ lateral, Biot << 1"
- Hsu 식 — discriminant ≥ 0 조건이 ONB 식으로 reduce 되는 과정
  ($\Delta T_{ONB} = \sqrt{8C_2\sigma T_{sat} q'' / k_l \rho_v h_{fg}}$)
- "여기서 $C_1, C_2$ 가 contact angle 의존성을 담고 있어서
   wettability 가 자연스럽게 반영됩니다."
- → "이 식이 soft constraint 로 loss 에 들어갑니다."

## Slide 7 — Surface encoder (120 sec)

- FiLM 의 직관: "activation 을 surface 마다 scale + shift"
- "왜 FiLM? — concat 보다 더 적은 parameter 로 강한 conditioning"
- Latent dim 16, hidden 64, layers 5 → 24,005 parameter
- "이 사이즈는 우리 dataset 크기 대비 적절합니다 — 너무 크면 overfit"

## Slide 8 — Composite loss + training (90 sec)

- 5개 손실 항 하나씩 짧게:
  - PDE: 물리 방정식 만족
  - BC: 경계 조건
  - Data: ONB 실측값 fit
  - Hsu: nucleation soft constraint
  - Monotonicity: 5 trends 강제
- 4-phase training: warmup → synthetic → fine-tune → inverse
- "Adam 으로 시작, L-BFGS 로 마무리 — fine-tuning 효과 큽니다."

## Slide 9 — Dataset (90 sec)

- 7 papers / 49 surfaces / 1361 points / 82 ONB labels
- 4 fluids 분포 — "water dominant 하지만 R-134a/R-123 도 의미 있음"
- "FC-77 은 CoolProp 미지원으로 학습 제외 — n=77 effective"
- "이 dataset 도 acceptance 후 GitHub + Zenodo 로 open-source 공개"

## Slide 10 — **Main result: parity plot** (150 sec — KEY)

- **잠시 멈춰서 figure 보여줌**
- "PINN RMSE 3.42 K. 가장 가까운 classical 인 Basu et al. 가 7.21 K — **53% 개선**"
- R² 도 음수에서 +0.44 로 — "Basu 는 mean predictor 보다 못함"
- Per-fluid: water 4.1, R-134a 2.8, R-123 1.6 K — "refrigerant 가 더 잘 맞음"
- "다음 슬라이드에서 그 이유를 보겠습니다."

## Slide 11 — Refrigerant subset (90 sec)

- 6-panel parity (5 classical + PINN)
- **−65~67% 개선** 강조: "Refrigerant 데이터 가장 큰 개선"
- 이유: "Refrigerant data 는 water 처럼 surface 개질-confounding 이 적어서
   surface descriptor 신호가 명확히 모델에 잡힙니다."
- 이는 **clean Ra effect** 가 R-134a/R-123 에서만 관찰되는 결과로 이어집니다 (다음 슬라이드).

## Slide 12 — Physics validation (90 sec)

- "9개 물리 테스트 중 8개 PASS — 5 monotonicity trends + energy/Hsu"
- 1개 mixed: water dataset 의 Ra-confound (BETZ smooth+coated vs JONES rough+plain)
- "이는 모델 결함 아니라 dataset 한계 — Phase 1.5 에서 보강 예정"

## Slide 13 — Deep ensemble UQ (90 sec)

- K=10 ensemble (seeds 42-51)
- 95% credible interval 의 empirical coverage 가 **98.7%** — "well calibrated, 보수적"
- σ_epi vs σ_ale — "epistemic dominant. 데이터 늘리면 줄어들 부분"
- "잘 모르는 surface 에 대해 wide CI 출력 — OOD detection 가능"

## Slide 14 — Hsu inverse + **Simpson's paradox** (120 sec — INTERESTING)

- "특별한 발견 한 가지 공유드립니다."
- ONB measurement → Hsu inversion → r_c distribution
- Mean r_c = 3.21 μm, 60% in [1, 100] μm — 물리적 reasonable
- **Simpson reversal**: aggregate Ra↑ ↔ r_c 약한 +; per-category Ra ↑ ↔ r_c −
- "표면 family 가 confounding variable 이었습니다. lab data 보강이 답이 될 것입니다."

## Slide 15 — Future work + Q&A (90 sec)

- **Phase 1.5** (현재 시작): in-house lab data (laser, corrosion, biphilic)
- **Phase 2**: forced convection flow boiling (Re, subcooling 추가)
- **Phase 3+**: foundation model, multi-fluid 확장
- Code + dataset 공개 약속
- "감사합니다. 질문 받겠습니다."

---

## 시간 점검 표

| 슬라이드 | 시간 (sec) | 누적 (sec) | 누적 (min:sec) |
|---|---|---|---|
| 1 Title         |  60 |   60 | 1:00 |
| 2 Outline       |  45 |  105 | 1:45 |
| 3 Problem       | 120 |  225 | 3:45 |
| 4 Why PINN      |  90 |  315 | 5:15 |
| 5 Overview      |  90 |  405 | 6:45 |
| 6 Math          | 180 |  585 | 9:45 |
| 7 Encoder       | 120 |  705 | 11:45 |
| 8 Loss/training |  90 |  795 | 13:15 |
| 9 Dataset       |  90 |  885 | 14:45 |
| 10 **Parity**   | 150 | 1035 | 17:15 |
| 11 Refrigerant  |  90 | 1125 | 18:45 |
| 12 Physics      |  90 | 1215 | 20:15 |
| 13 UQ           |  90 | 1305 | 21:45 |
| 14 **Inverse**  | 120 | 1425 | 23:45 |
| 15 Future + Q&A |  90 | 1515 | **25:15** |

**합계 25 min 15 sec** → 거의 정확. **버퍼 부족 시 슬라이드 6 또는 8 짧게 (전체 30 sec 단축).**

---

## Q&A 대비 — Top 6 예상 질문 + 짧은 답변 (각 30-45 sec)

### Q1. "왜 deep ensemble 만으로 충분한가? Bayesian PINN 은?"

**A**: "Bayesian 도 검토했지만 학습 비용이 K=10 ensemble 대비 5-10배.
Calibration 결과 (coverage 98.7%) 가 이미 충분히 좋아서 본 paper 에서는
ensemble 선택. 향후 BNN 비교는 Phase 1.5/2 에서 (Bayesian PINN, ICHMT
또는 별도 short paper)."

### Q2. "Hsu criterion 이 너무 단순한 모델 아닌가?"

**A**: "Soft constraint 로 들어갔습니다 — hard 가정이 아닙니다.
Loss term 가중치 w_Hsu 가 작아서 violation 도 허용합니다. Hsu 가 잘 안 맞는
경우 data term 이 압도하도록 설계. 결과: 8/9 trends PASS, Hsu envelope 도
대부분 만족."

### Q3. "n=82 는 너무 작지 않나?"

**A**: "맞습니다 — 제일 큰 한계입니다. Physics constraint 가 그래서 들어간 거고,
deep ensemble 의 wide CI 가 작은 데이터를 인지하는 신호 역할 합니다.
Phase 1.5 에서 lab 자체 데이터로 +20-50 labels 보강 진행 중."

### Q4. "Surface category 임베딩이 무엇을 학습한 건가?"

**A**: "현재는 black-box 입니다 — SHAP 또는 t-SNE 시각화는 future work.
다만 Simpson reversal 분석에서 category 가 표면 family 의 confound 를 capture
한다는 간접 증거 보였습니다."

### Q5. "Simpson reversal 이 artifact 아닐까?"

**A**: "JABARDO Cu 데이터로 cross-check 했습니다. 단일 lab 의 single material
(Cu) 의 R-134a 데이터 만 보면 Ra ↑ ↔ r_c − 가 −0.5 ~ −0.7 Spearman.
Aggregate 의 + 상관은 lab 간 표면 처리 차이 때문."

### Q6. "Flow boiling 확장 가능성?"

**A**: "Phase 2 plan 보유 — transfer learning 기반.
`phase2_flow_boiling/plan.md` 에 12개월 plan 작성. Phase 1.5 완료 후
바로 진입."

---

## 시각화 tip — 발표 중 실시간

- Slide 10 (parity): "PINN 점들이 대각선에 가까이 모여있고 — classical 점들이
  넓게 흩어진 것 보이시죠?"
- Slide 12 (trends): "각 subpanel 의 직선이 우리가 예측한 monotonicity 입니다."
- Slide 14 (Simpson): "왼쪽 aggregate 와 오른쪽 per-category 의 추세 부호가
  다르다는 게 핵심 — 이게 Simpson 입니다."

## 발표 전 마지막 체크리스트

- [ ] Slide deck PPTX/PDF 파일이 USB 또는 cloud 에 있음
- [ ] HDMI 케이블 / 어댑터 확인
- [ ] 시계 또는 timer (25 min)
- [ ] 발표 본인 ORCID 표기 (0000-0003-1996-6086)
- [ ] Backup slides (HPO 표, 4-phase progression) 도 같은 PPTX 안에
- [ ] Q&A 1-6 의 답변 머릿속 정리
