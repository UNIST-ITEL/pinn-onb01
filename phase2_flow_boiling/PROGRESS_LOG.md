# Phase 2 Progress Log

_Last updated: 2026-05-30_

---

## 세션 요약 (2026-05-29)

### 데이터 수집

| 논문 | 추출 행 수 | 주요 조건 | 비고 |
|---|---|---|---|
| Kuang 2025 | 66 | SUS304, P=0.3~5.0 MPa, G=400~1000, D_h=3.85~7.41mm | Fig 6b/7b/8b/9b/10a/10b |
| Hong 2012 | 6 | Stainless, P=180~195 kPa, G=507~840 | Fig 6/7 |
| Al-Yahia 2017 | 7 | Aluminum, P=101.3 kPa, G=118~473 | Fig 7/8 |
| Cheng 2022 | 54 | Stainless, P=145 kPa, G=100~300, 2채널(D_h=3.50/5.35mm) | Fig 10~13 |
| Qu & Mudawar 2002 | 20 | DIW microchannel, P=120 kPa, G=174~1318, D_h=0.349mm (최소) | Fig 10/11/12 |
| Wang et al. 2024 | 7 | 고압 water, P=10~16 MPa (최대), 60×2mm D_h=3.87mm, boiling curve ONB | Fig 7a/b/c |

> Qu2002: ONB 출구 발생 → delta_T_sub_K=출구(국소) 과냉도(2~30K) 채택. q는 planform-area 기준. ΔT_onb는 Fig12 계열식별 11행만.

---

### 데이터 정제 이력

원시 데이터: **536행** → 정제 후 324행 → Qu2002 +20 (344) → Wang2024 +7 (**351행**)

| 단계 | 변경 대상 | 사유 | 행 수 |
|---|---|---|---|
| v5→v6 | −basu2002 fig11 | 풀비등 parity 데이터 (G=-1, ΔT_sub=-1 전량, series=Past/Pres_theta*) | −88 |
| v5→v6 | −bergles1964 fig7 | P_kPa=-1 (압력 미기록, 유체물성 계산 불가) | −26 |
| v6→v7 | −basu2002 fig10 | G=-1, ΔT_sub=-1 전량 — 풀비등 데이터, q=-1 전부 | −98 |
| v7→v8 | +qu2002 | 마이크로채널 confinement coverage (D_h=0.349mm) | +20 |
| v10→v11 | +wang2024 | 고압 보강 (P=10~16MPa, Pattern C) | +7 |
| **합계** | | | **−185행** |

**최종 dataset (344행) paper별:**

| paper_id | 행 수 |
|---|---|
| liu2005 | 112 |
| forrest2016 | 72 |
| kuang2025 | 66 |
| cheng2022 | 54 |
| qu2002 | 20 |
| alyahia2017 | 7 |
| hong2012 | 6 |
| kandlikar1991 | 4 |
| bergles1964 | 3 |

---

### 훈련 실험 결과 (test split)

| 버전 | 데이터 | train/val/test | RMSE_ΔT | MAE_ΔT | R²_ΔT | RMSE_q | R²_q | 주요 변경 |
|---|---|---|---|---|---|---|---|---|
| v3 | 403행 (원본) | 263/55/60 | 7.56 K | 4.56 K | 0.377 | 1987 kW/m² | 0.516 | Phase 1 transfer |
| v4 | 403행 | 263/55/60 | — | — | — | — | — | w_data_q 1→2 (개선 없음) |
| v5 | 536행 (+4 논문) | 370/77/87 | 5.56 K | 2.82 K | 0.545 | 1211 kW/m² | 0.733 | 데이터 확장 |
| v6 | 422행 (−fig11,−fig7) | 290/61/69 | 4.02 K | 2.43 K | 0.623 | 151 kW/m² | 0.703 | 풀비등/P미상 제거 |
| v7 | 324행 (−fig10) | 222/47/53 | 1.85 K | 1.30 K | 0.769 | 187 kW/m² | 0.544 | basu2002 완전 제거 |
| v8 | 344행 (+qu2002) | 236/50/56 | 2.03 K | 1.41 K | 0.706 | 135 kW/m² | 0.780 | 마이크로채널 추가 (D_h=0.349mm) |
| v9 | 344행 (=v8) | 236/50/56 | 1.91 K | 1.31 K | 0.740 | 154 kW/m² | 0.713 | one-sided Hsu coupling (하한) |
| v10 | 344행 (=v8) | 236/50/56 | 2.00 K | 1.32 K | 0.717 | 148 kW/m² | 0.734 | 환산압력 P_r 직접 입력 (9→11채널) |
| **v11** | **351행 (+wang2024)** | **240/51/58** | **1.84 K** | **1.29 K** | **0.768** | **144 kW/m²** | **0.741** | **고압 데이터 보강 (P=10–16MPa)** |

> v7→v8: q 대폭 개선 (RMSE_q 187→135 kW/m², R²_q 0.544→0.780), ΔT 소폭 후퇴 (1.85→2.03K).
> v8→v9: Hsu coupling 등식→one-sided hinge. ΔT 개선 (2.03→1.91K, R²_ΔT 0.706→0.740), q 소폭 후퇴 (135→154 kW/m²).
> **Pattern B 해소**: cheng2022 test 9행 mean_err +0.03K, RMSE 0.62K (무편향).
> v9→v10: 압력 직접 입력. ΔT 소폭 후퇴 (1.91→2.00K), q 개선 (R²_q 0.713→0.734).
> **Pattern C 부분 해소**: corr(P,예측) +0.010→−0.020 (부호 전환, 실측 −0.137 방향). Fig8b sweep
> 300→3500kPa 하강경향 추종 (v9는 평탄). 고압 bias 3500/4500/5000kPa: v9 +1.9~2.5K → v10 +0.5~1.8K.
> 잔여 오차는 P=4500/5000(각 학습 1점) 외삽 한계 → 데이터 보강 필요.
> v10→v11: Wang2024 고압(10–16MPa) 7행 추가. ΔT 개선 (2.00→1.84K, R²_ΔT 0.717→0.768).
> **Pattern C 경향 학습 확정**: corr(P,예측) +0.010(v9)→−0.020(v10)→**−0.688(v11)** (실측 −0.570 강하게 추종).
> Wang 7행 RMSE 0.63K (고압 anchor 우수). 잔여: kuang P=3.5–5.0MPa(G=500/q=300 특정조건) +1.7K 과대 — 좁은 조건 gap.
> **현재 best = v11** (ΔT 최저 1.84K + 압력 물리 + 고압 커버리지 16MPa).

**v9 vs 기존 상관식 (test n_dT=34, 동일 split):**

| 방법 | RMSE_ΔT | MAE_ΔT | R²_ΔT | RMSE_q | R²_q |
|---|---|---|---|---|---|
| **PINN v9** | **1.91 K** | **1.31 K** | **0.740** | **154 kW/m²** | **0.713** |
| Bergles-Rohsenow 1964 | 3.73 K | 2.96 K | 0.013 | 1670 kW/m² | −59.2 |
| Hsu 1962 | 4.49 K | 3.70 K | −0.436 | 2745 kW/m² | −162 |
| Sato-Matsumura 1964 | 4.49 K | 3.70 K | −0.436 | 2745 kW/m² | −162 |
| Kandlikar 1991 | 4.49 K | 3.70 K | −0.436 | 2745 kW/m² | −162 |
| Basu 2002 | 4.78 K | 3.98 K | −0.625 | 3366 kW/m² | −244 |

> PINN v9: ΔT **1.95배** (vs Bergles 3.73K), q RMSE **11배** (vs Bergles 1670 kW/m²) 우위.

**v7 vs 기존 상관식 (test n_dT=32):**

| 방법 | RMSE_ΔT | MAE_ΔT | R²_ΔT | RMSE_q | R²_q |
|---|---|---|---|---|---|
| PINN v7 | 1.85 K | 1.30 K | 0.769 | 187 kW/m² | 0.544 |
| Bergles-Rohsenow 1964 | 3.82 K | 3.08 K | 0.014 | 1721 kW/m² | −60.1 |
| Hsu 1962 | 4.62 K | 3.86 K | −0.438 | 2829 kW/m² | −164 |
| Sato-Matsumura 1964 | 4.62 K | 3.86 K | −0.438 | 2829 kW/m² | −164 |
| Kandlikar 1991 | 4.62 K | 3.86 K | −0.438 | 2829 kW/m² | −164 |
| Basu 2002 | 4.90 K | 4.11 K | −0.621 | 3469 kW/m² | −247 |

**v7 per-fluid RMSE_ΔT:**

| fluid | n_test | PINN | Hsu | Bergles |
|---|---|---|---|---|
| water | 35 | 1.97 K | 4.52 K | 4.00 K |
| water_DIW | 18 | 1.32 K | 4.96 K | 3.12 K |

---

### 주요 분석

**저온 ΔT 과소예측 원인 분석 (2026-05-29)**

저온 구간(ΔT<5K)에서 세 가지 패턴 확인:

| 패턴 | 논문 | 원인 | 오차 |
|---|---|---|---|
| A | basu2002 (G=-1) | 풀비등 데이터 잔류 → v7에서 제거 | +3.05K 과대예측 |
| B | cheng2022 (저G, P=145kPa) | Hsu coupling tension: Hsu≈0.06K vs 실측 2~5K | −0.16K (미세 과소예측) |
| C | kuang2025 (P=500kPa, 희소 조건) | 훈련 외삽 영역 | +1.70K 과대예측 |

패턴 B 원인: Hsu self-consistency coupling(`loss_hsu_coupling`, w=0.05)이 등식
`ΔT_pred = C_hsu_nd·√q_star`(순수 포화 pool Hsu)을 강제 → 저q(15~44 kW/m²) 고과냉도
(ΔT_sub=20~40K)에서 Hsu≈0.06K로 하향 당김. 고과냉도 flow boiling에서 Hsu는 하한.
→ **v9에서 one-sided hinge로 해소 (ΔT_pred ≥ ΔT_Hsu만 페널티). cheng2022 RMSE 0.62K, 무편향.**

---

### 체크포인트 위치

| 버전 | 경로 |
|---|---|
| v3 (Phase 1 transfer) | `experiments/checkpoints/phase2_v3_phase1_transfer/best_model.pt` |
| v7 (ΔT-only best) | `experiments/checkpoints/phase2_v7_no_pool_boiling/best_model.pt` |
| v8 (microchannel) | `experiments/checkpoints/phase2_v8_microchannel_qu/best_model.pt` |
| v9 (ΔT 최저, 압력 물리 없음) | `experiments/checkpoints/phase2_v9_hsu_onesided/best_model.pt` |
| v10 (압력 물리 학습) | `experiments/checkpoints/phase2_v10_pressure_feature/best_model.pt` |
| **v11 (현재 best)** | `experiments/checkpoints/phase2_v11_highP_wang/best_model.pt` |

---

### 다음 단계

- [x] ~~Qu 2002 데이터 수집~~ → v8 완료 (20행, q R²_q 0.544→0.780)
- [x] ~~v9 Hsu coupling 보정~~ → 완료 (one-sided hinge, ΔT 1.91K/R²0.740, Pattern B 해소)
- [x] ~~Pattern C 검토~~ → v10 환산압력 입력으로 부분 해소 (corr 부호 전환, 경향 #4 학습)
- [x] ~~고압 데이터 보강~~ → v11 Wang2024 7행 (P=10~16MPa). corr(P,예측) −0.688, ΔT 1.84K. Pattern C 경향 학습 확정
- [ ] M7-M9: NS/Energy PDE residual 활성화 (plan Stage 3)
- [ ] manuscript M5 단계 초안 작성

---

### Git 커밋 이력 (이번 세션)

| 커밋 | 내용 |
|---|---|
| `3414310` | Add Kuang 2025 data (66 rows) |
| `b1ecb6f` | Add Hong/Al-Yahia/Cheng data (67 rows) |
| `cde1dfa` | Add v5 config + fix Ra_um in dataset loader |
| `a153f78` | v5 results: RMSE_ΔT 5.56K |
| `243589d` | Update parity plots to log scale |
| `f262400` | Remove pool boiling/P-unknown rows; add v6 config (422 rows) |
| `0b93e1a` | v6 results: RMSE_ΔT 4.02K, RMSE_q 151 kW/m² |
| `8516b89` | Remove basu2002 G=-1 rows; add v7 config (324 rows) |
| `d427e41` | v7 results: RMSE_ΔT 1.85K, R²_ΔT 0.769 |
| `8da5f1a` | Add PROGRESS_LOG.md |
| `b670234` | Add Qu & Mudawar 2002 microchannel data (20 rows) |
| `e01cb1e` | Add v8 config (344 rows) |
| `1fd758b` | v8 results: RMSE_q 135kW/m², R²_q 0.780 |
| `76b7373` | Add one-sided Hsu coupling (v9) |
| `67ef0ab` | v9 results: RMSE_ΔT 1.91K, Pattern B resolved |
| `8619236` | Add reduced pressure feature (v10): fix Pattern C |
| `1768a46` | v10 results: Pattern C partially resolved |
| `7e947e4` | Add Wang 2024 high-P data (7 rows); v11 config |
