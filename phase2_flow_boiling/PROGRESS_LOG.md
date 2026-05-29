# Phase 2 Progress Log

_Last updated: 2026-05-29_

---

## 세션 요약 (2026-05-29)

### 데이터 수집

| 논문 | 추출 행 수 | 주요 조건 | 비고 |
|---|---|---|---|
| Kuang 2025 | 66 | SUS304, P=0.3~5.0 MPa, G=400~1000, D_h=3.85~7.41mm | Fig 6b/7b/8b/9b/10a/10b |
| Hong 2012 | 6 | Stainless, P=180~195 kPa, G=507~840 | Fig 6/7 |
| Al-Yahia 2017 | 7 | Aluminum, P=101.3 kPa, G=118~473 | Fig 7/8 |
| Cheng 2022 | 54 | Stainless, P=145 kPa, G=100~300, 2채널(D_h=3.50/5.35mm) | Fig 10~13 |

---

### 데이터 정제 이력

원시 데이터: **536행** → 최종: **324행**

| 단계 | 제거 대상 | 사유 | 행 수 |
|---|---|---|---|
| v5→v6 | basu2002 fig11 | 풀비등 parity 데이터 (G=-1, ΔT_sub=-1 전량, series=Past/Pres_theta*) | −88 |
| v5→v6 | bergles1964 fig7 | P_kPa=-1 (압력 미기록, 유체물성 계산 불가) | −26 |
| v6→v7 | basu2002 fig10 | G=-1, ΔT_sub=-1 전량 — 풀비등 데이터, q=-1 전부 | −98 |
| **합계** | | | **−212행** |

**최종 dataset (324행) paper별:**

| paper_id | 행 수 |
|---|---|
| liu2005 | 112 |
| forrest2016 | 72 |
| kuang2025 | 66 |
| cheng2022 | 54 |
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
| **v7** | **324행 (−fig10)** | **222/47/53** | **1.85 K** | **1.30 K** | **0.769** | **187 kW/m²** | **0.544** | **basu2002 완전 제거** |

**v7 vs 기존 상관식 (test n_dT=32):**

| 방법 | RMSE_ΔT | MAE_ΔT | R²_ΔT | RMSE_q | R²_q |
|---|---|---|---|---|---|
| **PINN v7** | **1.85 K** | **1.30 K** | **0.769** | **187 kW/m²** | **0.544** |
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

패턴 B 원인: `w_hsu=0.5` loss가 저q(15~44 kW/m²) 고과냉도(ΔT_sub=20~40K) 조건에서
Hsu 예측(0.06K)으로 당기는 tension 발생. 고과냉도 flow boiling에서 Hsu 공식 부적합.

---

### 체크포인트 위치

| 버전 | 경로 |
|---|---|
| v3 (Phase 1 transfer) | `experiments/checkpoints/phase2_v3_phase1_transfer/best_model.pt` |
| v7 (현재 best) | `experiments/checkpoints/phase2_v7_no_pool_boiling/best_model.pt` |

---

### 다음 단계

- [ ] **v8**: Hsu coupling 수정 — 고과냉도 조건(ΔT_sub > 15K)에서 `w_hsu` 가중치 감소
      또는 subcooled-flow 보정항 추가 (패턴 B 해소 목표)
- [ ] 추가 논문 데이터 수집 (Qu 2002 미처리)
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
