# PINN-ONB01 Phase 1.5 — In-house Data Augmentation Plan

**작성일**: 2026-05-18
**상태**: 초안 (인벤토리 미완성 상태에서 placeholder 다수)
**의존**: Phase 1 IJHMT review 결과 (수락/revision 시점에 따라 시나리오 분기)
**관련 문서**:
- `future_research_roadmap.md` (A3-internal 신규 트랙)
- `ONB_PINN_Phase1_Pool_Boiling_Plan.md` (원 1단계 계획)
- `ONB_PINN_Phase2_Flow_Boiling_Plan.md` (2단계 계획, 본 1.5 이후)
- `02_data/raw/experiment/MEASUREMENT_GUIDE.md` (데이터 입력 양식)
- `04_analysis/reviewer_rebuttal.md` (예상 reviewer 질문 — 본 Phase가 직접 응답)

---

## 1. 개요 (Executive Summary)

**Phase 1.5는 본 연구실 자체 보유 풀비등 실험 데이터를 Phase 1 PINN 프레임워크에
통합·재학습하여 외부 corpus의 한계를 보강하는 단기 트랙이다.** Phase 1이
IJHMT review 중인 동안 (보통 2-5개월) 병행 진행하며, 데이터 인벤토리/디지타이즈
및 surface-card 작성, 모델 재학습, 별도 paper draft 작성까지 **3.5-5개월**에
완료를 목표로 한다. Phase 1의 OOD 한계 + reviewer 예상 질문 (Q1/Q3/Q4)을
정면 해소하는 fast-follow 또는 revision 보강 자료가 된다.

| 항목 | 내용 |
|---|---|
| 코드명 | Phase 1.5 — In-house Augmentation |
| 기간 | 3.5-5개월 (Phase 1 review 기간과 중첩) |
| 대상 저널 | (1순위) International Communications in Heat and Mass Transfer (ICHMT) — 실험실 publication track; (2순위) Applied Thermal Engineering; (3순위) IJHMT short paper (Phase 1 게재 후 fast-follow) |
| 핵심 산출물 | (a) 보강된 dataset (60-70 surfaces, 100-130 ONB labels), (b) 재학습 PINN, (c) ICHMT short paper, (d) 공개 dataset v1.5 |
| Phase 1과의 관계 | **보완형 (augmentation)** — 동일 framework, 확장 데이터. Salami slicing 아님 (새 surface family + 새 검증 축) |
| Phase 2와의 관계 | Phase 2 (flow boiling)의 Phase 0 사전 단계 — Phase 1.5에서 framework 강화 후 Phase 2 진입 |

---

## 2. 동기 (Motivation)

### 2.1 Phase 1의 발견된 한계

| 한계 | 근거 | Phase 1.5에서의 해소 |
|---|---|---|
| n=82 ONB labels (통계적 소규모) | reviewer rebuttal Q1 | +20-50 신규 labels |
| 7개 외부 출처만 — 단일 lab cross-validation 부재 | reviewer rebuttal Q3-Q4 | 자체 lab 측정 추가 (cross-source) |
| Biphilic 표면 3면 (BETZ만), 레이저 표면 0면 | surface_cards/_index.md | 신규 표면 카테고리 2종 (laser, corrosion) + biphilic 확장 |
| 학습 분포 외 surface에 wide CI | smoke test (2026-05-18) | OOD set 명시 평가로 ensemble UQ calibration 검증 |
| FC-77 학습 미포함, water dominant | §3 Table 2 | 본 Phase는 water 중심이므로 보강 효과 강함 |

### 2.2 사용 가능 데이터 소스

| 출처 | 출간 상태 | 표면 종류 | 예상 규모 |
|---|---|---|---|
| **Lee2023_ICHMT** (icheatmasstransfer.2023.107072) | 공개 | Femtosecond laser periodic micro/nano ripple | _TBD (3-5면)_ |
| **Lee2024_ICHMT** (icheatmasstransfer.2024.107270) | 공개 | Laser + Cu sintering 복합 | _TBD (3-5면)_ |
| **In-house corrosion** | 미공개 | Cu 부식 친수화 | _TBD_ |
| **In-house biphilic** | 미공개 | Biphilic 패턴 (구체적 패턴 미정) | _TBD_ |

→ 합계 **추정 10-20 새 surfaces, 20-50 ONB labels** 보강.

### 2.3 학술적 위치

- **Laser-treated 표면**: 2020-2025 hot topic (Kruse, Suss, AlShehhi, ITEL 자체 publication 2편). Phase 1.5는 PINN으로 laser surface ONB를 학습한 **최초 시도** (Jalili 2025, Huang 2024 등 최신 PINN ONB 논문에서 laser 표면 미다룸).
- **부식 친수화**: 산업 양산 공정에 가까움 (저비용). Industrial relevance↑.
- **Biphilic 확장**: BETZ 패러다임을 cross-lab 검증.

### 2.4 IP 상태

- **저자의 lab이 4개 출처 모두 전적 저작권 보유** → 협의 단계 불필요 (2026-05-18 확인됨).
- 학술 인용 (self-citation) 정상 절차로 처리.
- Phase 1.5 paper 저자 구성은 사용자 재량 (Phase 1 4명 + laser 데이터 측정자 옵션).

---

## 3. 목표 및 기여 (Objectives & Contributions)

### 3.1 정량 목표

| 지표 | Phase 1 baseline | Phase 1.5 목표 |
|---|---|---|
| Surface cards 수 | 49 | **60-70** |
| ONB labels 수 | 82 | **100-130** |
| Surface 카테고리 수 | 10 (외부) | **13+ (laser, corrosion, biphilic-extended 추가)** |
| Test set RMSE (전체) | 3.42 K | **≤ 3.0 K** |
| OOD set (lab data held-out) RMSE | _측정 안 함_ | **report + ≤ 5.0 K 목표** |
| 95% Coverage (ensemble) | 98.7% | **유지 또는 개선** |
| Spearman ρ (per-fluid Ra trend) | 0.5-0.7 | **유지** |

### 3.2 학술적 기여 (paper claim 후보)

1. **첫 cross-lab 검증** PINN-ONB framework — 외부 7개 lab 학습, 자체 lab 4개 데이터셋 보강
2. **신규 surface family 통합**: laser-engineered, corrosion-treated 표면을 PINN ONB에 처음 적용
3. **OOD 일반화 분석**: deep ensemble UQ가 미지 surface 카테고리를 wide CI로 표시함을 정량 검증 (calibration plot)
4. **표면 family ablation**: biphilic / laser / corrosion / 기존 외부 → 각 family 추가가 모델 RMSE에 미치는 marginal contribution
5. **Inverse Hsu와 SEM r_c 비교** (선택, SEM 가용성 의존)

### 3.3 비기여 (스코프 밖)

- 새 PINN 아키텍처 변경 — Phase 1 architecture 그대로
- 새 fluid 추가 — water dominant 유지 (R-134a 일부 가능)
- Forced convection / flow boiling — Phase 2에서 다룸
- High pressure 영역 — Phase 3 후속

---

## 4. 데이터 소스 및 인벤토리 (Data Sources & Inventory)

### 4.1 인벤토리 작성 필요 — 각 출처별

다음 표는 **현재 빈 상태**. 별도 `lab_data_inventory.md` 생성하여 채워넣기.

#### 4.1.1 Lee2023_ICHMT (Periodic ripple, laser-only)

| 항목 | 값 |
|---|---|
| Total surfaces | _TBD_ |
| Surface IDs (예상 SFC-051 ~ SFC-???) | _TBD_ |
| 각 surface별 laser fluence / pattern parameter | _TBD_ |
| Ra (μm), θ_static (°) | _TBD_ |
| Boiling curve 수 | _TBD_ |
| 추출 가능 ONB labels | _TBD_ |
| Fluid / pressure | 추정: water at 1 atm |
| Heater 형상 / 크기 | _TBD_ |
| ΔT_sub 범위 | _TBD_ |
| SEM 가용 (top-view / cross-section) | _TBD_ |
| Raw data 형태 (CSV / Excel / 보고서 figure only) | _TBD_ |
| 측정 불확실도 | _TBD_ |

#### 4.1.2 Lee2024_ICHMT (Laser + Cu sintering)

(동일 양식)

#### 4.1.3 In-house corrosion (미공개)

(동일 양식 + 추가)

| 추가 항목 | 값 |
|---|---|
| 첫 publication 시점 | Phase 1.5 paper 또는 별도? |
| Thesis 사용 여부 | _TBD_ |
| 데이터 staleness | _TBD_ |

#### 4.1.4 In-house biphilic (미공개)

(동일)

### 4.2 데이터 통합 절차

```
출처별 raw 데이터
    ↓
WebPlotDigitizer (필요 시) 또는 CSV import
    ↓
02_data/raw/experiment/<source>/ 폴더 (per-paper digitization metadata 형식)
    ↓
Surface card YAML 작성 (SFC-051+)
    ↓
02_data/processed/boiling_curves.csv 행 추가 (기존 schema 동일)
    ↓
ONB label 식별 (시각화 / slope change / Hsu envelope 검증)
    ↓
02_data/processed/onb_dataset.csv 행 추가
    ↓
02_data/surface_cards/_index.md 갱신 (현 49 → 60-70 surfaces)
```

### 4.3 라벨링 프로토콜 (Phase 1과 동일)

- 가능하면 **시각화 자료 (고속카메라/육안) 기반 manual label**
- 없으면 **boiling-curve slope-change heuristic** (자연대류 slope의 1.5배 초과 시점)
- 라벨 후 **Hsu envelope + 2≤ΔT≤30 K admissible band** 검증
- 위반 시 override + notes에 명시

### 4.4 데이터 품질 등급

각 row에 quality tier 부여 (paper 본문 transparency용):

| Tier | 기준 |
|---|---|
| A | Raw CSV 보존 + 시각화 ONB + 측정 불확실도 명시 |
| B | Raw CSV + slope-change ONB |
| C | 보고서 figure만 → 디지타이즈 + slope-change ONB |
| D | 미확실 (보류) |

---

## 5. 방법론 (Methodology)

### 5.1 모델 아키텍처

**변경 없음** — Phase 1 PINN architecture (`baseline_phaseDbal` config) 그대로 사용.

- Surface encoder (Ra, θ, category embedding)
- 1D conduction PINN (z=0 query)
- Composite loss (L_conduction + L_BC + L_data + L_ONB)
- Deep ensemble K=10

이는 의도적 결정:
- 같은 framework가 lab data로 cross-validate 됨을 입증 → **generalization claim 강화**
- 아키텍처 변경 paper는 별도 트랙 (B5 ablation)으로 분리

### 5.2 학습 전략 (3가지 시나리오 평가)

| 시나리오 | 학습 방법 | 목적 |
|---|---|---|
| **S1: Joint full retrain** | 외부 + lab 데이터 모두 합쳐서 처음부터 학습 | Default; 가장 단순 |
| **S2: Phase 1 model + fine-tune** | Phase 1 baseline_phaseDbal 체크포인트에서 lab data로 fine-tune (낮은 lr) | Catastrophic forgetting 방지 |
| **S3: Two-head model** | Phase 1 backbone freeze + lab-specific head | OOD vs ID separation 명시 |

→ **S1을 primary**, S2/S3는 ablation으로 비교. 어느 게 가장 잘 generalize 하는지 paper 핵심 결과.

### 5.3 학습 분할 (Train/Val/Test)

새 데이터 통합 시:

| Split | 비율 | 구성 |
|---|---|---|
| Train | 70% | Stratified by surface category (외부 + lab) |
| Val | 15% | 하이퍼파라미터 선택 |
| Test | 15% | 최종 평가 |
| **OOD set (별도)** | _Phase 1 보유 데이터 중 일부 (예: PHAN 5면) hold-out 으로 lab data만 학습 시 평가_ | OOD 일반화 명시 검증 |

### 5.4 Ablation 설계 (paper 핵심)

| Variant | 학습 데이터 | 목적 |
|---|---|---|
| V0 (Phase 1 baseline) | 외부 49 surface | 비교 baseline |
| V1 (Lee-laser only) | 외부 + Lee2023/2024 laser | Laser family 단독 효과 |
| V2 (Corrosion only) | 외부 + corrosion | Corrosion 단독 효과 |
| V3 (Biphilic only) | 외부 + biphilic | Biphilic family 효과 |
| **V4 (Full)** | 외부 + lab 전체 | **Phase 1.5 main result** |
| V5 (Lab only) | Lab data만 | Lab 자체 일관성 |

→ V1-V3는 family별 marginal contribution을 isolate. V5는 lab data 내적 일관성 검증.

### 5.5 평가 지표

Phase 1과 동일 + 추가:

| 추가 지표 | 의미 |
|---|---|
| OOD RMSE | Held-out lab category에 대한 RMSE |
| Per-family RMSE | Laser / Corrosion / Biphilic / Existing 별 |
| Ensemble σ vs error correlation | Wide CI ↔ Large error 인지능력 검증 |
| Calibration plot (predicted CI width vs empirical coverage) | UQ calibration |
| Marginal RMSE contribution | V0→V1 변화량 등 |

---

## 6. 검증 전략 (Verification)

### 6.1 Level 1 — 코드 검증

Phase 1 `level1_verifier.py` 동일 적용. 새 데이터 추가 후 1D analytical solution 재현 변동 없는지 확인.

### 6.2 Level 2 — 데이터 검증

| 검증 항목 | 기준 |
|---|---|
| Ra, θ unit 일관성 | μm, deg |
| q_flux W/m² 일관성 | 100 < q < 2e6 |
| ΔT_ONB 범위 | 0.7 - 30 K |
| Fluid 지원 | water / R-123 / R-134a (FC-77 제외) |
| Hsu envelope | 모든 ONB label discriminant ≥ 0 |
| Slope-change ONB threshold | NC slope × 1.5 일관 적용 |

### 6.3 Level 3 — 물리적 타당성

Phase 1의 5가지 경향성 모두 유지:

| 경향성 | Phase 1 결과 | Phase 1.5 점검 |
|---|---|---|
| q'' ↑ → ΔT_ONB ↑ | PASS (Hsu √q) | 재확인 |
| Ra ↑ → ΔT_ONB ↓ | Mixed (water confounded) | Laser/corrosion family 추가로 신호 강화? |
| θ ↑ → ΔT_ONB ↓ | PASS | 재확인 |
| P ↑ → ΔT_ONB ↓ | Limited (refrigerant only) | water 추가는 무영향 |
| ΔT_sub ↑ → ΔT_ONB ↑ | PASS | 재확인 |

### 6.4 Level 4 (NEW) — Cross-lab generalization

| 시나리오 | 학습 | 평가 | 의미 |
|---|---|---|---|
| Leave-one-lab-out | 7 외부 + 4 lab 출처 중 하나 제외 | 제외된 출처 RMSE | Cross-lab transfer |
| Lab-as-OOD | 외부만 학습 | Lab 데이터 RMSE | Pre-trained model의 OOD 일반화 |
| Lab-only | Lab만 학습 | 외부 데이터 RMSE | 역방향 OOD |

---

## 7. 일정 및 마일스톤 (Timeline)

```
       M1                M2                M3                M4                M5
       ────────────────  ────────────────  ────────────────  ────────────────  ────────────────
M1.1   인벤토리 작성       
M1.2   2 ICHMT bib 추가    
M1.3   현 모델 baseline 측정
                          ────────
M2.1                       Raw 데이터 정리/디지타이즈 (출처 1, 2)
M2.2                       Surface card 작성 (출처 1, 2)
                                            ────────
M3.1                                         Raw 데이터 정리 (출처 3, 4)
M3.2                                         Surface card 작성 (출처 3, 4)
M3.3                                         ONB labels 확정 (전체)
                                                              ────────
M4.1                                                           재학습 (V0-V5 ablation)
M4.2                                                           OOD 검증
M4.3                                                           Figure / Table 작성
                                                                                ────────
M5.1                                                                             Paper draft
M5.2                                                                             Internal review
M5.3                                                                             제출 준비
```

| Milestone | 시점 | Go/No-Go |
|---|---|---|
| MS1 | M1 end | 인벤토리 완료, 데이터 규모 확정 |
| MS2 | M2 end | 출처 1,2 surface card + curve CSV 완성 |
| MS3 | M3 end | 전체 데이터 학습 가능 상태 |
| MS4 | M4 end | V0-V5 ablation 결과 + OOD report |
| MS5 | M5 end | Paper draft + figures |

### 7.1 Phase 1 review 결과에 따른 분기

| Phase 1 결과 | Phase 1.5 사용처 |
|---|---|
| **Accept as-is (M2-M3 시점)** | Phase 1.5는 **fast-follow paper**. ICHMT 단독 제출. |
| **Minor revision (M2-M3)** | 일부 데이터를 supplementary로 추가. Phase 1.5 독립 paper는 계속 진행. |
| **Major revision (M2-M3)** | "more data" 요청 시 일부 통합. Phase 1.5 scope 축소 가능 (남은 데이터로 후속 paper) |
| **Reject (M2-M3)** | Phase 1 + Phase 1.5 데이터 통합한 **강화 paper** 재제출 (IJHMT 또는 IJHMT 외 venue) |
| **Phase 1 review 미정 (M4 도달)** | Phase 1.5 paper draft까지 진행, 제출은 Phase 1 결과 후 |

---

## 8. 위험 관리 (Risk Management)

| Risk | 가능성 | 영향 | 대응 |
|---|---|---|---|
| 미공개 데이터 raw 보존 부재 (보고서 figure만 있음) | Medium | High | Tier C 라벨링 + tolerance 명시. SEM이라도 있으면 보강 |
| ONB 식별 모호 (시각화 부족) | High | Medium | Slope-change heuristic + Hsu envelope cross-check. 모호 시 보류 |
| Surface 측정값 (Ra, θ) 불일치 / 측정 시점 변동 | Medium | Medium | notes에 측정 method 명시. 가능하면 재측정 |
| Phase 1 paper "more data" major revision 요구 | Medium | (혼합) | 시나리오 분기 7.1 활용. 큰 손해 없음 |
| Salami slicing 비판 (Phase 1과 너무 유사) | Low-Medium | Medium | Paper claim을 framework-validation으로 명확히 분리 (단순 데이터 추가가 아닌 cross-lab generalization analysis가 핵심) |
| ICHMT가 self-citation 과다로 desk reject | Low | Medium | Phase 1 main paper 게재 후 Phase 1.5 제출 (timing 조정) |
| SEM 이미지에서 r_c 추출 실패 | Medium | Low | r_c는 inverse Hsu 출력으로만 사용 — 학습 영향 없음. Supplementary로 강등 |
| Lab data 학습 시 외부 데이터 성능 저하 (catastrophic forgetting) | Medium | High | S2 fine-tune 전략 또는 S1에서 lab data oversampling 균형 |

---

## 9. Phase 1 자산 재사용 매핑

다음 자산 100% 재사용:

| 자산 | 위치 | 변경 여부 |
|---|---|---|
| PINN architecture | `03_model/src/model/pinn.py` | 무변경 |
| Surface encoder | `03_model/src/model/surface_encoder.py` | 무변경 (category 임베딩만 확장) |
| Composite loss | `03_model/src/loss/` | 무변경 |
| Deep ensemble K=10 | `03_model/src/training/ensemble.py` | 무변경 (seeds 그대로) |
| CoolProp wrapper | `03_model/src/utils/properties.py` | 무변경 (R-134a 압력 hard-coded 인지) |
| Optuna HPO | `03_model/src/training/hpo.py` | 재사용 시 lab data 포함 |
| Dataset class | `03_model/src/training/dataset.py` | 무변경 (CSV schema 동일) |
| Surface card format | `02_data/surface_cards/*.yaml` | 무변경 |
| 5 classical correlations | `04_analysis/scripts/correlation_comparator.py` | 무변경 |
| Inference wrapper | `04_analysis/scripts/predict_new_experiment.py` | 무변경 — lab data로 즉시 사용 가능 |
| Measurement guide | `02_data/raw/experiment/MEASUREMENT_GUIDE.md` | 무변경 |
| Reviewer rebuttal | `04_analysis/reviewer_rebuttal.md` | Phase 1.5 결과로 Appendix B 보강 |

→ **순수 신규 작업은 데이터 + paper draft만**. 코드 작업 거의 없음.

---

## 10. Claude Code 에이전트 / 스킬 활용 전략

Phase 1에서 구축된 24개 에이전트 (`.claude/agents/`) 와 1개 슬래시 명령
(`/add-paper`) 을 최대한 재사용한다. Phase 1.5 특성상 **신규 에이전트는
최소 2개** 만 추가 필요. 단계별 매핑:

### 10.1 단계별 에이전트 활용 매핑

#### Stage M1 — 인벤토리 + bib 추가 + 현 모델 baseline (1개월)

```
[기존 에이전트 재사용]
paper-card-extractor
  ├─ Lee2023_ICHMT (icheatmasstransfer.2023.107072) 카드 생성
  ├─ Lee2024_ICHMT (icheatmasstransfer.2024.107270) 카드 생성
  └─ 결과 → phase1p5_inhouse/data/lab_data_inventory.md 통합

bibtex-curator
  ├─ 2 ICHMT 논문 references.bib 등록 (formatting 일관성)
  └─ Phase 1 bib와 별도 또는 통합 — phase1.5/manuscript/references.bib 구성

survey-search
  ├─ 추가 laser-treated / corrosion / biphilic 최신 논문 보강 (2025-2026)
  └─ Phase 1 survey에 없는 신규 trend 반영 (예: Suss 2025, AlShehhi 2024 등)

[직접 실행 — 새 에이전트 불필요]
predict_new_experiment.py wrapper (이미 구축됨)
  ├─ 4개 lab 출처 데이터에 Phase 1 baseline_phaseDbal 모델 적용
  └─ Out-of-distribution baseline metric 산출 → MS1 Go/No-Go 근거
```

**Stage M1 산출물**: 인벤토리 markdown + 갱신된 bib + OOD baseline 보고서.

---

#### Stage M2-M3 — 데이터 디지타이즈 + surface card + ONB labels (2개월)

```
[기존 에이전트 재사용]
figure-digitizer
  ├─ Lee2023/2024 ICHMT 논문 boiling curve figure 디지타이즈 가이드
  ├─ 미공개 corrosion / biphilic 데이터의 보고서 그림 → CSV
  └─ WPD 프로젝트 파일을 phase1p5/data/raw/lab/<source>/ 에 보존
     (Phase 1 의 raw/literature 와 동일 구조)

surface-card-builder
  ├─ 출처별 신규 SFC 카드 작성 (SFC-051 ~ SFC-070+)
  ├─ 새 category 추가: 'unist_laser', 'unist_corrosion', 'unist_biphilic'
  └─ phase1p5/data/surface_cards/_index.md 갱신

preprocess-pipeline
  ├─ 통합 boiling_curves_v1p5.csv 생성 (Phase 1 1361 + lab N rows)
  ├─ 통합 onb_dataset_v1p5.csv 생성 (Phase 1 82 + lab M labels)
  ├─ 단위 변환·이상값·split·결측 6단계 (Phase 1 파이프라인 그대로)
  └─ data quality tier 컬럼 추가 (A/B/C/D — § 4.4)

[신규 에이전트 1: lab-onb-labeler] ⭐
  목적: lab boiling curve에서 ONB 라벨 자동 식별
  입력: phase1p5/data/raw/lab/<source>/boiling_curves.csv
  로직:
    1. 자연대류 slope 계산 (low-q 영역, q < 1 kW/m^2)
    2. slope-change point detection (NC slope × 1.5)
    3. Hsu envelope 검증 (eq:hsu_discriminant ≥ 0)
    4. 2 ≤ ΔT_ONB ≤ 30 K admissible band 검사
    5. 위반 시 manual override 권장 + notes 자동 기재
  파생: Phase 1 ONB labeling protocol (24 manual + 58 slope) 자동화
  위치: .claude/agents/lab-onb-labeler.md
```

**Stage M2-M3 산출물**: SFC-051~SFC-070+ 카드, v1p5 데이터셋 CSV, ONB 라벨 82+M.

---

#### Stage M4 — 재학습 + ablation V0-V5 + OOD 검증 (1개월)

```
[기존 에이전트 재사용]
training-orchestrator
  ├─ Phase 1 학습 파이프라인 그대로 (Adam → L-BFGS)
  ├─ V0-V5 6개 variant 자동 sweep
  └─ MLflow에 각 variant 기록 (phase1p5/experiments/mlflow_runs/)

ensemble-uq
  ├─ V4 (full) 에 대해 K=10 ensemble 학습 (Phase 1과 동일 seeds 42-51)
  ├─ Coverage / epistemic-aleatoric 분리
  └─ Calibration plot 생성 — Phase 1.5의 핵심 기여 (§ 3.2 항목 3)

hpo-tuner (선택)
  ├─ V4 main variant 에 대해 lr / w_data / d_z 재탐색 (5-10 trials)
  └─ Phase 1 best HPO 결과 ≈ 그대로 사용 시 skip

correlation-comparator
  ├─ lab data 에 대해 5 classical correlations 동시 평가
  ├─ predict_new_experiment.py wrapper 그대로 활용
  └─ Per-family parity plot (laser / corrosion / biphilic / external)

physics-consistency-check
  ├─ Level 3 (5 trends) Phase 1 동일 재실행
  └─ 신규: laser family 에서 q-dependency 단조성 재확인

level1-verifier
  ├─ Level 1 analytical solution 재현 (regression test)
  └─ shared/src 변경 시 trigger

[신규 에이전트 2: ood-evaluator] ⭐
  목적: Phase 1.5 Level 4 (cross-lab generalization) 검증 자동화
  3가지 split 수행:
    1. Leave-one-lab-out:
        - 외부 7 + lab 4 = 11 출처 중 하나 제외하고 학습
        - 제외 출처에서 RMSE 측정
        - 총 11번 학습 (subset 가능)
    2. Lab-as-OOD:
        - 외부 7만 학습 (= Phase 1 모델)
        - Lab 4 데이터로 RMSE
    3. Lab-only:
        - Lab 4만 학습
        - 외부 7에 RMSE (역방향)
  출력:
    - phase1p5/analysis/figures/ood_matrix.png (heatmap)
    - phase1p5/analysis/tables/ood_metrics.md
  위치: .claude/agents/ood-evaluator.md
```

**Stage M4 산출물**: V0-V5 결과 표, OOD matrix, calibration plot, 5 classical 비교.

---

#### Stage M5 — Paper draft + figures + 제출 준비 (1개월)

```
[기존 에이전트 재사용]
section-drafter
  ├─ ICHMT short paper 6-7 섹션 초안 작성
  ├─ Phase 1과 차별화된 framing (cross-lab generalization 강조)
  ├─ 본문 4000-5000 단어 (ICHMT short format)
  └─ Style: 4:6 long:short mix (Phase 1 동일)

figure-composer
  ├─ Phase 1.5 핵심 figures 6-8개:
  │    F1. Dataset summary (49 + lab 추가 visualisation)
  │    F2. Ablation V0-V5 결과 (RMSE 막대)
  │    F3. Per-family parity (4-panel)
  │    F4. OOD matrix (Level 4 핵심)
  │    F5. Calibration plot (epistemic vs predicted CI)
  │    F6. Cross-lab generalization 시연 (Leave-one-lab-out heatmap)
  │    F7. (선택) SEM r_c vs inverse Hsu 비교 — SEM 가용성 의존
  └─ EPS/PDF 300dpi (ICHMT 요건 일치)

latex-formatter
  ├─ ICHMT 저널 클래스 적용 (필요 시)
  ├─ Figure caption, equation numbering 일관화
  └─ Phase 1의 elsarticle 설정 재활용 가능 — ICHMT 도 Elsevier

bibtex-curator
  ├─ Phase 1.5 references.bib (Phase 1 + 신규)
  ├─ Lee2023/2024 ICHMT 자기 인용 포함
  └─ Cross-validation 관련 reference 보강 (cross-lab ML papers)

reviewer-anticipator
  ├─ Phase 1.5 예상 reviewer 질문 사전 정리:
  │    Q1: "Phase 1 paper와 본 paper의 차별점은?"
  │    Q2: "Self-citation (Lee2023, Lee2024) bias 우려"
  │    Q3: "Lab data raw 형태 검증 가능?"
  │    Q4: "Cross-lab generalization 인과 vs 상관?"
  │    Q5: "OOD set 구성의 정당성"
  └─ phase1p5/manuscript/reviewer_rebuttal.md 생성
```

**Stage M5 산출물**: ICHMT main.tex + figures + bib + cover letter + rebuttal.

---

### 10.2 신규 에이전트 정의 — 2개

#### 10.2.1 `lab-onb-labeler` (M2-M3)

```yaml
description: |
  Lab boiling curve CSV 에서 ONB 라벨을 자동 식별하고
  Hsu envelope + admissible band 검증을 수행.
  Phase 1 ONB labeling protocol (24 manual + 58 slope) 의 자동화 버전.

tools: Read, Write, Edit, Bash

inputs:
  - phase1p5/data/raw/lab/<source>/boiling_curves.csv

outputs:
  - phase1p5/data/processed/onb_labels_<source>.csv
  - phase1p5/data/lab_onb_labeling_report.md (per-curve QA notes)

trigger:
  - "lab ONB 라벨링"
  - "/label-onb-lab <source>"
```

#### 10.2.2 `ood-evaluator` (M4)

```yaml
description: |
  Phase 1.5 의 Level 4 cross-lab generalization 검증을 자동화.
  Leave-one-lab-out / Lab-as-OOD / Lab-only 3가지 split 수행
  + heatmap, calibration plot, OOD metrics 표 생성.

tools: Read, Write, Edit, Bash

inputs:
  - phase1p5/data/processed/onb_dataset_v1p5.csv
  - phase1p5/experiments/checkpoints/V0_phase1_baseline/ (참조용)

outputs:
  - phase1p5/analysis/figures/ood_matrix.png
  - phase1p5/analysis/figures/calibration_plot.png
  - phase1p5/analysis/tables/ood_metrics.md
  - phase1p5/experiments/checkpoints/loo_*/ (Leave-one-out 체크포인트)

trigger:
  - "OOD 검증"
  - "Level 4 generalization"
  - "/ood-eval"
```

---

### 10.3 슬래시 명령 확장

Phase 1.5 전용 슬래시 명령 추가:

```
[기존 — Phase 1 정의됨]
/add-paper [pdf]                paper card 생성 + DB 추가

[신규 — Phase 1.5 추가]
/add-lab-source <name>          새 lab data 출처 등록
                                 (data/raw/lab/ 폴더 생성 + inventory entry)

/label-onb-lab <source>         lab-onb-labeler 호출

/ablate-phase1p5                training-orchestrator + V0-V5 자동 sweep

/ood-eval                       ood-evaluator 호출

/draft-phase1p5-section <n>     section-drafter — ICHMT 4-5K words constraint 적용
```

각 슬래시 명령 정의: `.claude/commands/<name>.md` 에 추가.

---

### 10.4 스킬 활용

Phase 1과 동일 패턴 + Phase 1.5 특화:

```
[데이터 / 인벤토리]
xlsx 스킬
  ├─ lab_data_inventory.md → inventory.xlsx 변환 (공동저자 검토용)
  ├─ V0-V5 ablation 결과 표 → Excel
  └─ Per-family metrics → Excel sheets

docx 스킬
  ├─ Phase 1.5 plan 진척 보고서 (지도교수/연구실 공유)
  ├─ 데이터 사용 권한 확인서 (필요 시 — 본 프로젝트는 IP 자체 보유로 불요)
  └─ ICHMT cover letter Word 초안

pptx 스킬
  ├─ 연구실 세미나 (Phase 1 vs 1.5 차별점 발표)
  ├─ 학회 발표 자료 (KSME 추계 / IHMTC 등)
  └─ Phase 1.5 final review 발표 (제출 직전)

pdf 스킬
  ├─ ICHMT main.pdf 최종 compile
  ├─ Supplementary.pdf
  └─ ICHMT cover_letter.pdf
```

---

### 10.5 CLAUDE.md 변경 사항

Phase 1.5 진입 시 `CLAUDE.md` 에 다음 추가/수정 필요:

```markdown
# CLAUDE.md (Phase 1.5 추가분)

## 활성 트랙
1단계: 풀비등 외부 corpus 학습 (✅ IJHMT 제출 완료, review 대기)
1.5단계: lab 데이터 augmentation (진행 중) ⭐ 현재 작업 중
2단계: 강제대류 비등 (future)

## Phase 1.5 폴더 (workspace restructure 후)
phase1p5_inhouse_augmentation/
  ├─ data/          → lab raw + processed
  ├─ experiments/   → V0-V5 + OOD checkpoints
  ├─ analysis/      → ablation, OOD figures
  └─ manuscript/    → ICHMT main.tex

## Phase 1.5 신규 카테고리
'unist_laser', 'unist_corrosion', 'unist_biphilic' (lab 출처)

## Phase 1.5 신규 에이전트
lab-onb-labeler         lab boiling curve → ONB labels
ood-evaluator           Level 4 cross-lab generalization

## Phase 1.5 목표 저널
1순위: ICHMT (lab home venue, 2023/2024 paper 게재처)
2순위: Applied Thermal Engineering
```

---

### 10.6 단계별 에이전트 활용 흐름도

```
[M1 인벤토리]
  paper-card-extractor → bibtex-curator → survey-search
        ↓
  predict_new_experiment.py (baseline 측정)

[M2-M3 데이터]
  figure-digitizer → surface-card-builder → preprocess-pipeline
        ↓
  lab-onb-labeler ⭐ (신규)
        ↓
  boiling_curves_v1p5.csv + onb_dataset_v1p5.csv

[M4 학습/검증]
  training-orchestrator → ensemble-uq → hpo-tuner (선택)
        ↓
  correlation-comparator + physics-consistency-check + level1-verifier
        ↓
  ood-evaluator ⭐ (신규)
        ↓
  V0-V5 결과 + OOD matrix + calibration plot

[M5 작성]
  section-drafter → figure-composer → latex-formatter → bibtex-curator
        ↓
  reviewer-anticipator
        ↓
  ICHMT submission package
```

---

### 10.7 Phase 1 에이전트 24개 재사용 현황

| 에이전트 | Phase 1.5 재사용 | 비고 |
|---|---|---|
| paper-card-extractor | ✅ | Lab 2 ICHMT 논문 카드 |
| bibtex-curator | ✅ | references.bib 통합 |
| coolprop-integrator | ✅ | water/refrigerant 변동 없음 |
| correlation-comparator | ✅ | lab data 비교 |
| debug-diagnoser | ✅ | 학습 발산 시 동일 |
| ensemble-uq | ✅ | K=10 그대로 |
| figure-composer | ✅ | 6-8 figures |
| figure-digitizer | ✅ | lab 보고서 그림 |
| gap-matrix-mapper | ⚠️ 선택 | 새 trend 반영 필요 시만 |
| hpo-tuner | ⚠️ 선택 | Phase 1 HPO 결과 재사용 가능 |
| inverse-solver | ⚠️ 선택 | SEM r_c 비교 시 |
| latex-formatter | ✅ | ICHMT 클래스 적용 |
| level1-verifier | ✅ | regression test |
| loss-function-builder | ❌ | 손실 변경 없음 |
| paper-card-extractor | ✅ | 위 동일 |
| physics-consistency-check | ✅ | 5 trends 재확인 |
| pinn-architect | ❌ | 아키텍처 변경 없음 |
| preprocess-pipeline | ✅ | v1p5 데이터 생성 |
| reviewer-anticipator | ✅ | Phase 1.5 예상 질문 |
| section-drafter | ✅ | ICHMT short 작성 |
| surface-card-builder | ✅ | SFC-051+ |
| surface-encoder-dev | ❌ | encoder 변경 없음 |
| survey-search | ✅ | 신규 trend 보강 |
| synthetic-data-gen | ❌ | 합성 데이터 사용 안 함 (lab 실측만) |
| training-orchestrator | ✅ | V0-V5 sweep |

**재사용 19 / 24 = 79%**. 5개는 Phase 1.5 에서 미사용.
**신규 2개** (lab-onb-labeler, ood-evaluator) 추가.

---

## 11. 목표 저널 및 출간 전략

### 11.1 후보 저널 비교

| 저널 | 적합도 | 장점 | 단점 |
|---|---|---|---|
| **ICHMT** ⭐ (1순위) | 매우 높음 | Lab의 home venue (2023/2024 paper 게재처). Short paper 형식. Phase 1과 차별화 분명 | Short format (4000 단어 제한 가능) |
| Applied Thermal Engineering | 높음 | Volume 큼, broad audience | Boiling-specific 아님 |
| IJHMT short paper | 중간 | Phase 1과 동일 venue 일관성 | Phase 1 결과 후 timing 주의 (salami 인식) |
| Experimental Thermal Fluid Science | 중간 | Experimental focus + data validation | Computational 측면 약함 |

### 11.2 권장 출간 시퀀스

```
Phase 1 (IJHMT) → 게재 확정
  ↓ (1-2개월 gap)
Phase 1.5 (ICHMT short paper) — "Cross-lab validation of surface-conditioned PINN ONB prediction"
  ↓ (3-6개월 gap)
Phase 2 (IJHMT full paper) — "Extension to forced-convection flow boiling"
```

### 11.3 Paper title 후보

1. "Cross-lab validation of a surface-conditioned PINN for nucleate boiling onset using laser-engineered and biphilic surfaces" — Generalization 강조
2. "Extending physics-informed ONB prediction to laser-treated and corrosion-modified pool boiling surfaces" — 응용 강조
3. "Out-of-distribution generalization of ensemble PINN predictions for pool-boiling nucleation onset" — UQ 강조

→ M3 시점에 결과 보면서 결정.

---

## 12. 예상 산출물 (Expected Outputs)

| 산출물 | Phase 1.5 release |
|---|---|
| Paper (ICHMT) | 1편, 약 4-5K words |
| Dataset v1.5 (Zenodo, 새 DOI 또는 v1.0 update) | 60-70 surfaces, 100-130 ONB labels |
| Public model checkpoints (GitHub Release v1.5) | 새 ensemble (V4 best) |
| Surface cards | SFC-051 ~ SFC-070+ |
| Per-paper digitization metadata | Lee2023/2024 WPD project files (raw 보존 시 unnecessary) |
| Figure 산출 | 6-8 main figures (parity, ablation V0-V5, OOD, calibration, family marginal) |

---

## 13. 사전 검토 필요 사항 (Open Questions)

다음은 인벤토리 / 정책 결정이 필요한 항목:

| # | 질문 | 결정 시점 |
|---|---|---|
| 1 | 미공개 corrosion / biphilic 데이터의 첫 publication 권리는 Phase 1.5에 부여 OK? | M1 |
| 2 | Lab data 측정자 (Seunghwan Lee, Yeonsu Kim 등) Phase 1.5 공저 여부 | M1 |
| 3 | Hyungson Ki 교수 acknowledgement vs co-author | M1 |
| 4 | Phase 1 게재 확정 전 ICHMT 제출 시점 | Phase 1 결과 후 |
| 5 | 학습 전략 S1 vs S2 vs S3 중 primary 선택 | M4 (결과 보면서) |
| 6 | SEM 이미지에서 r_c 추출 시도 vs supplementary 강등 | M3 |
| 7 | OOD set 구성: held-out lab data vs 외부 PHAN/JONES 일부 | M3 |
| 8 | Salami slicing 우려에 대한 paper framing 전략 | M5 (draft) |
| 9 | 신규 dataset DOI를 별도 발급 vs Phase 1 dataset에 v1.5 update | M5 |
| 10 | Phase 1 IJHMT reviewer가 lab data 사용 요구 시 → Phase 1.5 통합 vs 분리 | Phase 1 review 후 |

---

## 14. 즉시 액션 (Phase 0 — 1주 내)

| # | 작업 | 담당 |
|---|---|---|
| 0-1 | `lab_data_inventory.md` 빈 템플릿 생성 (4 출처 × 인벤토리 항목) | Claude (요청 시) |
| 0-2 | 2개 공개 논문 (Lee2023_ICHMT, Lee2024_ICHMT) `05_manuscript/references.bib` 추가 | Claude (요청 시) |
| 0-3 | Lee2023_ICHMT 보유 raw 데이터 형태 확인 (CSV / Excel / figure-only) | 저자 |
| 0-4 | Lee2024_ICHMT raw 데이터 형태 확인 | 저자 |
| 0-5 | In-house corrosion 데이터 위치 / 형태 확인 | 저자 |
| 0-6 | In-house biphilic 데이터 위치 / 형태 확인 | 저자 |
| 0-7 | 본 plan 검토 + 수정 사항 피드백 | 저자 |
| 0-8 | Open Questions § 12 의 #1-#3 lab 내부 결정 | 저자 |

---

## 15. 본 계획서의 위치

- **본 문서**: `phase1p5_inhouse_augmentation/plan.md` (Phase 1.5 폴더 내, 2026-05-19 이동)
- **이전 위치**: `ONB_PINN_Phase1p5_InHouse_Augmentation_Plan.md` (workspace root, deprecated)
- **로드맵 갱신 필요**: `future_research_roadmap.md` 에 A3-internal 트랙으로 정식 반영 (Phase 1.5 = A3-internal 매핑)
- **PHASE_STATUS.md 갱신**: Phase 1.5 트랙 추가됨 (2026-05-19)
