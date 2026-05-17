# 새 비등 실험 측정 가이드 (PINN-ONB01 검증 / 비교용)

**작성일**: 2026-05-18
**대상 모델**: `03_model/checkpoints/ensemble_phaseDbal/` (K=10 deep ensemble)
**비교 baseline**: Hsu (1962), Davis-Anderson (1966), Bergles-Rohsenow (1964), Sato-Matsumura (1964), Basu et al. (2002)
**관련 스크립트**: `04_analysis/scripts/predict_new_experiment.py`
**관련 템플릿**: `new_experiment_template.csv` (동일 폴더)

---

## 0. 본 가이드의 사용법

1. 본 문서에 따라 실험 + 측정 수행
2. 결과를 **`new_experiment_template.csv`** 형식으로 CSV 작성
3. `predict_new_experiment.py --csv <your_csv> --run-name <label>` 실행
4. `04_analysis/experiments/<label>/` 에서 결과 확인 (`predictions.csv`, `metrics.md`, `parity_combined.png`, `applicability_report.md`)

> **검증 모드** (실험값으로 모델 평가): `delta_T_wall` 컬럼에 관측된 ONB 과열도 입력
> **순수 예측 모드** (ONB 시점을 모르는 새 조건): `delta_T_wall` 비워둠 → metrics 생략, 예측만 출력

---

## 1. 실험 전 1회 측정 항목 (표면 특성)

| 측정 | 장비 | 정확도 권장 | CSV 컬럼 |
|---|---|---|---|
| **Ra** (산술 평균 거칠기) | AFM (서브-μm용) / Stylus profilometer (≥0.1 μm) | ±10% | `Ra_um` (μm 단위) |
| **θ_static** (정적 접촉각) | Goniometer + sessile drop | ±2° | `theta_deg` |
| (선택) Sa | AFM (서브-nm용) | — | `notes`에 기록 |
| (선택) θ_adv / θ_rec | Dynamic goniometer | ±3° | `notes`에 기록 |
| (선택) SEM 표면 형상 | SEM ≥ 1000x | — | `notes`에 image filename |
| (선택) 활성 공동 밀도 N_s | 고속카메라 / SEM 정량 | — | (학습 미사용; 향후 보강) |

### 측정 시 주의

- **여러 위치 평균**: 최소 3-5 spot 측정 후 평균. 표면 균일성 확인.
- **세척 후 측정**: 비등 실험 전 세척 절차와 동일한 상태에서 측정.
- **단위 변환**:
  - AFM이 nm로 출력하면 **÷1000** → μm
  - 예: $R_a = 30$ nm → `Ra_um = 0.030`
- **Ra vs Sa**: 본 모델은 Ra(line) 단일 스칼라로 학습됨. Sa(area) 사용 시 `notes`에 명시. 일반적으로 같은 표면에서 $S_a \approx R_a$ 정도로 비슷하지만 정확하지 않음.

---

## 2. 비등 실험 측정 항목

### 2.1 실험 환경 사전 결정

| 항목 | 모델 학습 범위 (1단계) | 권장 |
|---|---|---|
| Fluid | water, R-123, R-134a (FC-77 비지원) | water 1 atm 권장 |
| Pressure | water 1 atm, R-123 1 atm, **R-134a 5 bar** | 모델 학습 압력 일치 시 가장 정확 |
| Subcooling | 0 – 15 K | 0 K (saturated) 또는 명시 |
| Heater 형상 | 수평 평판 (상면 가열), 대구경 수평 원형관 | 1D 가정 만족 형상 |
| Heater 크기 | $L_c \approx 2.5$ mm 이상 권장 (Bo $\ge 1$) | — |
| Heater 재질 | 금속 (Cu, Al, SS, brass 등) | 표면 카드 카테고리와 일치 시 좋음 |

> **Bond 수 점검**: $\mathrm{Bo} = (\rho_l - \rho_v) g L^2 / \sigma$. $\mathrm{Bo} \ge 1$ 인 크기 (1 atm water 기준 $L \ge 2.5$ mm) 권장. 작은 wire / small cylinder 데이터는 본 모델 학습 분포 외.

### 2.2 boiling curve 측정 절차

| Step | 작업 | 도구 |
|---|---|---|
| 1 | 표면 세척 (acetone → DI water → drying) | — |
| 2 | 셀에 fluid 충전, degassing 1시간 이상 | hotplate + reflux |
| 3 | 가열 전력 매우 낮은 값에서 시작 ($q'' \le 1$ kW/m² for water) | DC power supply |
| 4 | 안정 상태 도달 후 **$q'', T_{wall}, T_{bulk}, P$** 동시 기록 | DAQ |
| 5 | 가열 전력 ~10-20% 단계로 증가, 각 단계 안정 후 기록 | — |
| 6 | 자연대류 → ONB 전환 구간을 **밀하게 sampling** (단계 ~5% 권장) | — |
| 7 | ONB 시점 명확히 확인 (시각화 권장, 없으면 boiling curve slope change) | 고속 카메라 또는 육안 |
| 8 | nucleate boiling 구간 추가 측정 후 CHF 직전에서 종료 | — |

### 2.3 ONB 시점 식별 기준 (3가지 중 1개라도 만족 시)

1. **시각적 (gold standard)**: 표면 어디서든 첫 기포 발생 시점의 $(q'', \Delta T_{wall})$
2. **Boiling-curve slope change**: $\log q''$ – $\log \Delta T_{wall}$ 그래프에서 자연대류 기울기보다 1.5배 가파른 첫 점 (본 모델 학습에 사용된 휴리스틱)
3. **Wall 온도 강하**: ONB 후 표면 온도가 떨어지면서 step 발생 — 첫 강하 시점

> **권장**: 1번 (시각화) + 2번 (boiling curve) 교차 검증. `notes`에 어느 기준 사용 명시.

### 2.4 측정 변수와 정확도

| 변수 | 단위 | 권장 정확도 | CSV 컬럼 |
|---|---|---|---|
| $T_{wall}$ (표면 온도) | K | ±0.5 K (calibrated TC/RTD) | 계산에 사용 |
| $T_{sat}$ (포화 온도) | K | 0.1 K | (CoolProp 자동 계산) |
| $T_{bulk}$ (벌크 유체 온도) | K | ±0.5 K | $\Delta T_{sub}$ 계산 |
| $\Delta T_{wall} = T_{wall} - T_{sat}$ | K | ±1 K | `delta_T_wall` |
| $\Delta T_{sub} = T_{sat} - T_{bulk}$ | K | ±0.5 K | `delta_T_sub` |
| $q''$ (heat flux) | **W/m²** | ±5% | `q_flux` |
| Pressure | Pa | ±1% | (CSV 미수록; 모델 hard-coded) |
| Heater 면적 | m² | ±2% (calorimetry용) | 별도 기록 |

### 2.5 CSV 변환 시 흔한 단위 실수

| 잘못 | 정정 |
|---|---|
| $q'' = 50$ (kW/m²) | $q'' = 50000$ (W/m²) **— 반드시 W/m² 단위** |
| $R_a = 30$ (nm) | $R_a = 0.030$ (μm) |
| $\theta = 1.48$ (rad) | $\theta = 85$ (deg) |
| $T_{wall} = 105$ (°C) | $\Delta T_{wall} = 5$ (K) — **wall 온도 그대로 X, 과열도로 변환** |
| $\Delta T_{wall} = T_{wall} - T_{bulk}$ | 정의는 $T_{wall} - T_{sat}$ — bulk 아님 |

---

## 3. CSV 작성 예시

`new_experiment_template.csv` 의 예시 행:

```csv
source_paper,figure_ref,surface_id,surface_label,fluid,delta_T_wall,delta_T_sub,q_flux,Ra_um,theta_deg,category,notes
in_house_2026,run01,MY-001,Cu_polished_Ra0p5,water,5.2,0.0,50000,0.5,85.0,in_house,trial 1 - visible ONB
in_house_2026,run02,MY-001,Cu_polished_Ra0p5,water,4.8,0.0,45000,0.5,85.0,in_house,trial 2 - repeat
in_house_2026,run03,MY-001,Cu_polished_Ra0p5,water,,0.0,60000,0.5,85.0,in_house,prediction-only mode
```

### 동일 표면 여러 trial

| 권장 | 의미 |
|---|---|
| 같은 `surface_id`, 다른 `figure_ref` | 동일 표면의 여러 ONB 관측 |
| 같은 `surface_label` 유지 | 모델은 surface_id가 같으면 같은 표면 카드로 인식 |
| `notes`에 trial 번호 기록 | 통계/평균 계산 시 유용 |

### 다른 표면

- `surface_id` 와 `surface_label` 둘 다 변경
- 동일 실험 batch면 `category`는 동일 유지 (예: `in_house`)

---

## 4. 추론 실행 (예시)

```bash
cd "/Users/myhomemini/Library/CloudStorage/OneDrive-개인/Projects/PINN-ONB01"

# 본인 데이터로 실행
python 04_analysis/scripts/predict_new_experiment.py \
    --csv 02_data/raw/experiment/my_data.csv \
    --run-name my_water_test_2026

# 출력 위치
ls 04_analysis/experiments/my_water_test_2026/
#   predictions.csv          # 각 row + PINN ±σ + 5 상관식 예측
#   metrics.md               # RMSE/MAE/R²/coverage (delta_T_wall 있을 때만)
#   parity_combined.png      # 6-panel parity plot
#   applicability_report.md  # 학습 분포 외 row 경고
```

---

## 5. 결과 해석 가이드

### 5.1 `predictions.csv` 주요 컬럼

| 컬럼 | 의미 |
|---|---|
| `pred_mean_K` | PINN 10개 ensemble 평균 ΔT_ONB [K] |
| `pred_std_epi_K` | Epistemic (모델 불확실성) σ [K] |
| `pred_std_ale_K` | Aleatoric (데이터 노이즈) σ [K] |
| `pred_std_total_K` | $\sqrt{\sigma_{epi}^2 + \sigma_{ale}^2}$ |
| `lower_95_K`, `upper_95_K` | 95% credible interval |
| `covered_95` | 실험값이 [lower, upper] 안에 들어왔는지 (검증 모드 시) |
| `Hsu_dT_K`, `Davis_dT_K`, `BR_dT_K`, `SM_dT_K`, `Basu_dT_K` | 5종 상관식 예측 |
| `extrapolation_flags` | 학습 분포 외 변수 list (있다면) |

### 5.2 `metrics.md` 해석

- **RMSE**: 작을수록 좋음. 학습 set test 기준 PINN 3.42 K, Basu 7.21 K.
  - 새 실험 RMSE가 비슷하면 좋은 신호.
  - 5 K 이내면 산업적으로 충분한 정확도.
- **R²**: 1에 가까울수록 좋음. 음수는 평균선만 못함.
  - 학습 set PINN R² = +0.44.
- **95% coverage**:
  - 95%에 가까울수록 ensemble uncertainty가 잘 calibrate됨.
  - 학습 set 기준 PINN 98.7% (overconfident하지 않음).
  - 새 실험에서 50% 이하면 ensemble undercoverage → 학습 분포 외 가능성.
- **MRE**: $\le 30\%$ 이면 산업 표준 acceptable.

### 5.3 `parity_combined.png` 해석

6 panel (PINN + 5 상관식):
- 점이 대각선($y=x$) 가까이 = 정확한 예측
- PINN panel이 다른 5개보다 흩어짐 작으면 → PINN 우위 확인
- 점이 한쪽으로 치우치면 → 계통적 bias

### 5.4 `applicability_report.md` 해석

- "All rows lie within the training distribution" = 신뢰성 높음
- Row별 변수 outside 표기 시 → extrapolation, 결과 해석 주의

---

## 6. Troubleshooting

| 증상 | 원인 / 조치 |
|---|---|
| 스크립트가 `Unsupported fluid` 경고 | fluid명 오타 또는 비지원 fluid. `water`, `R-123`, `R-134a` 만 가능 |
| 모든 PINN 예측이 NaN | CSV 컬럼 순서/명칭 어긋남. 헤더 정확히 copy |
| `q_flux` 값이 100 이하라고 경고 | kW/m² → W/m² 변환 누락. ×1000 |
| RMSE가 매우 큼 (>10 K) | 1) 실험 압력이 학습 압력과 다름 / 2) Fluid가 학습 분포 외 (FC-77 등) / 3) ONB 시점 식별 오류 |
| Coverage가 0% | ensemble undercoverage. 학습 분포 외 가능성 — applicability report 확인 |
| `extrapolation_flags` 행이 많음 | 학습 분포 밖. 결과 해석은 정성적으로만 사용 |
| `merged` 매칭 후 PINN 결과만 있고 상관식 컬럼이 비어 있음 | join key 불일치. surface_id, fluid, q_flux 정확히 일치하는지 확인 |

---

## 7. 자주 묻는 질문

**Q1.** R-134a를 5 bar 외 압력에서 실험했는데 사용 가능한가?
> 모델 내부 ($\rho_v, \sigma, h_{fg}$ 등) 는 5 bar로 hard-coded. 다른 압력이면 정확도 저하 가능. `notes`에 명시 후 신중히 해석.

**Q2.** 본 모델이 학습되지 않은 fluid (FC-72, ethanol 등)에 사용 가능한가?
> 비추천. CoolProp이 fluid 물성을 모르면 inference 시 row drop. 그래도 시도하려면 fluid명을 변경 (예: water로 위장)할 수 있지만 결과는 의미 없음. 본격 적용은 Phase 2 multi-fluid 모델 (`ONB_PINN_Phase2_Flow_Boiling_Plan.md`) 완성 후.

**Q3.** 시각화 없이 boiling curve slope 만으로 ONB 식별해도 되나?
> 가능. 본 모델 학습 데이터의 58/82 라벨이 그렇게 식별됨. 단, slope threshold (대략 자연대류의 1.5배) 일관 적용. `notes`에 "slope-change heuristic" 명시.

**Q4.** ONB 후의 nucleate boiling 데이터도 학습 모델에 도움이 되나?
> 본 모델은 **ONB 시점**만 예측. nucleate boiling 후의 ($q'', \Delta T_{wall}$)는 ONB 라벨이 아님 (`ONB_flag=False`). 단, **boiling curve 전체**를 CSV로 제공하면 slope 분석 시 유용 (별도 분석).

**Q5.** 새 실험으로 모델을 fine-tune 하고 싶다.
> Phase 1 학습 파이프라인의 transfer learning 코드 (`03_model/src/training/train.py`)를 재사용해 새 데이터 + 기존 ensemble checkpoint로 재학습 가능. Phase 1 plan 4.5절 Phase 3 (실험 미세조정) 참조. 자세한 방법은 별도 요청 시 작성.

---

## 8. 책임 / 연락처

- **Maintainer**: Jaeseon Lee `<JaeseonLee@unist.ac.kr>`
- **본 가이드**: `02_data/raw/experiment/MEASUREMENT_GUIDE.md`
- **관련 문서**:
  - `02_data/processed/README.md` — dataset schema (12 columns)
  - `02_data/surface_cards/_index.md` — 기존 surface card 목록
  - `RELEASE_CHECKLIST.md` — 공개 release 절차
  - `ONB_PINN_Phase2_Flow_Boiling_Plan.md` — flow boiling 확장 계획
- **이슈**: GitHub Issues (수락 후 `UNIST-ITEL/pinn-onb01`)
