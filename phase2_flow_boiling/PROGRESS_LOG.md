# Phase 2 Progress Log

_Last updated: 2026-06-02_

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

**최종 dataset (351행) paper별:**

| paper_id | 행 수 |
|---|---|
| liu2005 | 112 |
| forrest2016 | 72 |
| kuang2025 | 66 |
| cheng2022 | 54 |
| qu2002 | 20 |
| alyahia2017 | 7 |
| wang2024 | 7 |
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
> **FINAL best = v11** (ΔT 최저 1.84K + 압력 물리 + 고압 커버리지 16MPa).

| v12 | 351행 | 236/50/56 | 3.94 K | — | **−0.06** | — | — | M7-M9: +energy(.05)+P-mono+one-sided → **실패** |
| v13 | 351행 | 236/50/56 | 3.88 K | — | **−0.03** | — | — | energy .05→.002 → **여전히 실패** |
| v14 | 351행 | 236/50/56 | — | — | — | — | — | equality+P-mono+energy → Stage1 정체(조기중단) |

> v12/13/14 모두 **데이터 fit 붕괴(R² 음수)**. M7-M9 negative result (아래 분석). v11 유지.

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

**M7-M9 PDE residual 탐색 — Negative Result (2026-05-31)**

목표: NS+Energy PDE residual 활성화 (plan Stage 3). **결론: 현 스칼라-ONB regressor
아키텍처에 부적합. v11 유지.**

1. **완전 NS 불가능**: 모델은 (surface, flow, x*) → (ΔT_onb*, q_onb*, T*) 스칼라 출력기.
   속도(u,v)·압력 필드가 없어 continuity/momentum residual 정의 불가. → 미구현(weight 0).

2. **1D 에너지 residual (`loss_energy_1d`) 구현·검증**: head_T에 고-Pe 이류지배 balance
   (dT*/dx*>0, d²T*/dx*²≈0, autograd 1·2차). **불안정**: 2차 autograd 그래디언트가
   grad_clip(1.0) 예산 독점 → 데이터 손실 굶음. w_energy=0.05(v12)·0.002(v13) 모두
   test R² 음수. 게다가 head_T는 **데이터 supervision 없는 보조 필드**라 가치 한계적.

3. **trend-hardening 소프트 제약 (P-mono 등)**: 모델이 단조성을 **"평탄화"로 trivially
   만족**(v11 Re/G sweep이 ΔT 거의 무변화인 이유 — flat이 mono loss 최소화). 강제력 약함.
   P-mono+energy를 v11에 쌓으면 데이터 fit 붕괴 (v12/13/14 R² 음수).

4. **근본 원인**: v11은 이미 물리-정합 해 근처에 잘 튜닝됨. 추가 PDE/제약은 데이터를
   **과구속**해 fit을 해침. 물리 경향은 이미 **아키텍처(압력 피처)+데이터+Hsu coupling**으로
   확보 (ΔT_sub✓, q✓, P부분✓; Re/G는 평탄·무해).

**조치**: 코드(`loss_energy_1d`, w_mono_P, one-sided coupling)는 옵션으로 보존(기본 비활성).
완전 field-resolving PINN은 future work (plan 리스크노트의 "physics-regularized regressor
철학" 그대로). v9 one-sided coupling은 OneDrive가 되돌렸던 것을 156a39b에서 복원(기본 false).

---

### 체크포인트 위치

| 버전 | 경로 |
|---|---|
| v3 (Phase 1 transfer) | `experiments/checkpoints/phase2_v3_phase1_transfer/best_model.pt` |
| v7 (ΔT-only best) | `experiments/checkpoints/phase2_v7_no_pool_boiling/best_model.pt` |
| v8 (microchannel) | `experiments/checkpoints/phase2_v8_microchannel_qu/best_model.pt` |
| v9 (ΔT 최저, 압력 물리 없음) | `experiments/checkpoints/phase2_v9_hsu_onesided/best_model.pt` |
| v10 (압력 물리 학습) | `experiments/checkpoints/phase2_v10_pressure_feature/best_model.pt` |
| **v11 (FINAL best ⭐)** | `experiments/checkpoints/phase2_v11_highP_wang/best_model.pt` |
| v12-v14 (실패, 미커밋) | M7-M9 PDE/제약 실험, R² 음수 — 디스크에만, git 미포함 |

---

### 다음 단계

- [x] ~~Qu 2002 데이터 수집~~ → v8 완료 (20행, q R²_q 0.544→0.780)
- [x] ~~v9 Hsu coupling 보정~~ → 완료 (one-sided hinge, ΔT 1.91K/R²0.740, Pattern B 해소)
- [x] ~~Pattern C 검토~~ → v10 환산압력 입력으로 부분 해소 (corr 부호 전환, 경향 #4 학습)
- [x] ~~고압 데이터 보강~~ → v11 Wang2024 7행 (P=10~16MPa). corr(P,예측) −0.688, ΔT 1.84K. Pattern C 경향 학습 확정
- [x] ~~M7-M9 PDE residual~~ → **Negative result**: 완전 NS 불가(스칼라 regressor), 1D 에너지·소프트 제약은
      과구속/2차-그래디언트 불안정으로 fit 붕괴. v11이 이미 경향 만족. 코드는 옵션 보존. (위 분석 참조)
- [x] ~~M10 Deep Ensemble UQ (K=5)~~ → 완료. Ensemble mean ΔT 1.72K/R²0.796 (단일 v11 1.84/0.768 개선).
      Epistemic std 평균 0.51K, 1σ coverage 28%(과소) → 재보정 ×4.7 필요, aleatoric(heteroscedastic) 미모델 한계.
      `analysis/tables/ensemble_uq_metrics.md`, `analysis/figures/ensemble_uq.png`.
- [x] ~~manuscript M5 초안~~ → 완료. 6섹션+abstract (~5,250단어), 11 figures, 2 tables, 57 refs. polish 완료.
      `manuscript/main.tex` + `sections/` + `figures/`(자체완결).
- [ ] **(재개 지점) 개별 그림 수정** ⭐ — 휴식 후 figure별 다듬기. 인벤토리는 아래 § Figure 인벤토리.
- [ ] LaTeX 컴파일 (이 머신 toolchain 없음 → Phase 1 머신/Overleaf)
- [ ] co-author·funding·acknowledgements 기입 (현재 TBD)
- [ ] (선택) heteroscedastic head로 aleatoric 추가 → full calibration
- [ ] (선택) inverse problem (측정 ΔT_ONB → r_c 분포)

---

### Figure 인벤토리 (재개용 — 개별 그림 수정 작업)

manuscript는 **11 figure 환경**(파일 12개; parity는 2-panel). 모든 figure는 **재현 가능**.
논문용 사본: `manuscript/figures/` (png+pdf), 원본/재생성: `analysis/figures/`.
graphicspath = `{figures/}` 단일.

> **Fig # = 원고 컴파일 순서** (`\input` §1→6 안에서 `\begin{figure}` 등장 순서). 파일/스크립트명은 미변경(참조표만). 개별 그림 수정은 이 순서대로 진행. (검토 상태: ☐ 미검토 / ✅ 완료)

| Fig # | 검토 | label | 파일 | 섹션 | 생성 방법 | 비고 |
|---|---|---|---|---|---|---|
| **1** | ✅ | fig:arch | architecture.png | Methods 2.2 | inline matplotlib 블록도 | (2026-06-02) in-figure 제목·중복 FiLM 라벨 제거 + 행 중심선(6.7/4.3/2.1) 정렬 + 내부 phase ID('Phase-1','new') → 독자용 표현(transfer-learned/frozen, trained from scratch, 박스 내부) + Training objective 박스 3줄·우측 정렬(heads 오른쪽 끝 x=14.8) + predictions/backprop 화살표로 학습루프 명시 |
| **2** | ✅ | fig:concept | fig_onb_concept.png | Methods 2.3 | (a) schematic + (b) 실제 v11 데이터 | (2026-06-02) (a) 곡선이 ONB에서 연결되도록 수정(연속 T_w, 기울기 꺾임 + single-phase 점선 연장) + (b) 무작위 합성점 → 실제 193점 측정 ΔT_ONB vs per-point 포화 Hsu ΔT_Hsu,sat 산점도(대각선 하한, 96% 위, forbidden 음영). caption·\dThsu 매크로 갱신 |
| **3** | ✅ | fig:coverage | fig_coverage_map.png | Data 3.1 | CSV scatter (P vs D_h, size=G) | (2026-06-02) in-figure 제목 제거 + G 크기 범례 추가(200/600/1000) → 마커 크기 정량화. G 범례+source 범례 둘 다 좌상단 적층(우하단 데이터 가림 해소) |
| **4** | ✅ | fig:dist | fig_data_distributions.png | Data 3.1 | CSV 6-panel 히스토그램 | (2026-06-02) suptitle 제거 + subcooling 라벨 "Inlet/local subcooling"으로 정확화(스크립트↔PNG drift 해소) + caption에 n-varies 주석 |
| **5** | ✅ | fig:persource | fig_per_source_rmse.png | Results 4.1 | v11 전체추론 per-source RMSE bar | (2026-06-02) in-figure 제목 제거 + y라벨 정돈("Kuang 2024" 등). ⚠️ 본문(4_results)도 재서술: stale("~0.6–2.5K,Kuang최대,균일")→실제(대형sweep≤1.2K 잘맞음, 소수-n 문헌셋 Qu/Forrest/Bergles/Kandlikar 3–5.7K가 잔차 carry) |
| **6** | ✅ | fig:parity | parity_dT_onb_test.png + parity_q_onb_test.png | Results 4.1 | `fig_parity.py` (v11 test) | (2026-06-02) in-figure 제목 제거→(a)/(b) 라벨 + ±0%→1:1 + 단위 SI통일(kW m⁻²) + caption (a)/(b) |
| **7** | ☐ | fig:ablation | fig_ablation_progression.png | Results 4.2 | 하드코딩 v3→v11 값 막대+선 | 값은 위 실험표 |
| **8** | ☐ | fig:ptrend | fig_pressure_trend.png | Results 4.3.2 | v11 추론, kuang/wang P-sweep | 고압 잔여 uptick 정직 표시 |
| **9** | ☐ | fig:trends | fig_physics_trends.png | Results 4.3.3 | v11 ΔT_sub sweep + q-data scatter | 2-panel (P패널 제거함) |
| **10** | ☐ | fig:uq | ensemble_uq.png | Results 4.4 | 5-멤버 추론 (parity±2σ/calib/std-vs-P) | math.erf 사용 (scipy 없음) |
| **11** | ☐ | fig:designmap | fig_design_map.png | Discussion 5.1 | v11 (G,P) 격자 추론 contour | q=None(Bo=0) |

**그림 수정 작업 방법 (영구화 완료, 2026-06-02)**: 생성 스크립트가 `analysis/scripts/fig_*.py`로 저장됨 (그림 1개=스크립트 1개, `figlib.py` 공유 헬퍼). phase2 root에서 `python analysis/scripts/<fig>.py` 실행하면 **analysis/figures/ + manuscript/figures/ 양쪽에 png+pdf 자동 저장**(복사 누락 없음). 목록·매핑은 `analysis/scripts/README.md`.
> 주의: ① scipy 미설치(math.erf 우회). ② v9 체크포인트는 9-ch라 현재 11-ch 코드로 로드 불가. ③ `fig_ablation_progression.py` 값은 위 실험표에서 하드코딩 — 변경 시 동기화. ④ OneDrive 되돌림 이력 → 편집 후 즉시 커밋.

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
| `155fdd1` | v11 results: RMSE_ΔT 1.84K (FINAL best) |
| `156a39b` | M7-M9 energy+P-mono; RESTORE v9 one-sided (OneDrive fix) |
| `7921b74` | M7-M9 negative result documented; v11=best |
| `8472c01`/`5bedacf` | M10 Deep Ensemble K=5 + UQ analysis |
| `8e348e9` | M5 manuscript first draft (IJHMT) + bib |
| `ffd3841`/`9f4c8c8`/`e76e57f` | manuscript figures (→11) |
| `e373b51` | manuscript English polish |
| `ef8185d` | consolidate figures → manuscript/figures/ |
