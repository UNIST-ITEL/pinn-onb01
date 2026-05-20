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
| `merged` 매칭 후 PINN 결과만 있고 상관식 컬럼이 비어 있음 | (df22132에서 해결됨) — 구버전 사용 시 fix commit으로 업데이트 |
| **동일 표면의 다른 q'' trial이 같은 PINN 예측을 받음** | **정상 동작** — 모델은 surface features만 입력으로 사용. Q6 참조 |
| **PINN 평균이 관측보다 크지만 CI는 관측을 cover** | **OOD 신호** — wide σ는 모델이 미학습 표면임을 인지한 것. Q7 참조 |

---

## 7. 자주 묻는 질문

**Q1.** R-134a를 5 bar 외 압력에서 실험했는데 사용 가능한가?
> 모델 내부 ($\rho_v, \sigma, h_{fg}$ 등) 는 5 bar로 hard-coded. 다른 압력이면 정확도 저하 가능. `notes`에 명시 후 신중히 해석.

**Q2.** 본 모델이 학습되지 않은 fluid (FC-72, ethanol 등)에 사용 가능한가?
> 비추천. CoolProp이 fluid 물성을 모르면 inference 시 row drop. 그래도 시도하려면 fluid명을 변경 (예: water로 위장)할 수 있지만 결과는 의미 없음. 본격 적용은 Phase 2 multi-fluid 모델 (`phase2_flow_boiling/plan.md`) 완성 후.

**Q3.** 시각화 없이 boiling curve slope 만으로 ONB 식별해도 되나?
> 가능. 본 모델 학습 데이터의 58/82 라벨이 그렇게 식별됨. 단, slope threshold (대략 자연대류의 1.5배) 일관 적용. `notes`에 "slope-change heuristic" 명시.

**Q4.** ONB 후의 nucleate boiling 데이터도 학습 모델에 도움이 되나?
> 본 모델은 **ONB 시점**만 예측. nucleate boiling 후의 ($q'', \Delta T_{wall}$)는 ONB 라벨이 아님 (`ONB_flag=False`). 단, **boiling curve 전체**를 CSV로 제공하면 slope 분석 시 유용 (별도 분석).

**Q5.** 새 실험으로 모델을 fine-tune 하고 싶다.
> Phase 1 학습 파이프라인의 transfer learning 코드 (`03_model/src/training/train.py`)를 재사용해 새 데이터 + 기존 ensemble checkpoint로 재학습 가능. Phase 1 plan 4.5절 Phase 3 (실험 미세조정) 참조. 자세한 방법은 별도 요청 시 작성.

**Q6.** 동일 표면에서 q'' 만 다른 여러 trial을 입력했는데 PINN 예측이 모두 동일하다. 왜?
> 정상 동작. 본 PINN은 (Ra, θ, category) 등 **표면 특성만을 입력**으로 받는다.
> $q''$는 학습 중 PDE residual + 경계조건에 들어가서 ΔT_ONB 라벨과의 잠재 관계를 학습할 뿐, 추론 시 직접 입력이 아니다. 따라서 같은 표면이면 단일 ΔT_ONB 예측값이 나오고, 같은 표면의 multiple trials는 ensemble σ 범위 안에서 sampling variance로 해석한다.
> 만약 q''에 따라 명시적으로 변하는 예측이 필요하다면 고전 상관식 5종 (`Hsu`, `Davis-Anderson`, `Bergles-Rohsenow`, `Sato-Matsumura`, `Basu`)이 모두 $\sqrt{q''}$ 형태로 q-의존성을 가지므로 별도 panel에서 직접 확인 가능.

**Q7.** 예측 평균이 관측과 크게 다른데(예: PINN 17 K vs 관측 5 K), 모델이 틀린 건가?
> **σ_total 과 95% CI를 확인하라**. Smoke test 결과(2026-05-18):
> - 학습 분포 외 표면(`in_house` category 미학습) 입력 시 PINN 평균 17.7 K, σ_total 7.0 K, 95% CI [3.94, 31.45] K.
> - 관측 4.8-5.2 K는 CI 안에 들어옴 → ensemble UQ는 **모르는 표면임을 정확히 인지**.
> - 동일 입력에 대해 고전식 Bergles-Rohsenow RMSE 1.82 K로 더 정확.
> 해석: **wide CI** (σ > 5 K) 시 모델이 OOD 신호를 emit하는 것이므로 (1) Bergles-Rohsenow / Basu 등 동시 출력을 우선 참고, (2) 가능하면 fine-tune (Q5), (3) 더 많은 유사 표면 SEM/AFM 보강으로 학습 분포 확장.
> Narrow CI (σ < 2 K) 인데 mean이 어긋날 때만 모델 오류로 의심.

**Q8.** 새 표면 카드를 만들었지만 `category` 를 무엇으로 할지 모름.
> `category` 는 stratified-sampling tag일 뿐 모델 입력은 아니다. 다만 `category_id` (학습 시 만든 임베딩) 가 PINN에 주입되므로 영향은 있다.
> 권장:
> 1. 기존 카테고리에 매칭되면 그것 사용 (`betz`, `bourdon12`, `bourdon15`, `jabardo`, `jabardo_br`, `jabardo_ss`, `jones`, `jones_F`, `jones_w`, `jo`, `phan`)
> 2. 새 카테고리라면 `in_house` 또는 `external` 등 자유 명칭 사용 — 모델은 "unknown" embedding으로 fallback (neutral default)
> 3. category_id 영향이 크면 (CI가 매우 wide) 표면 metadata가 부족하다는 신호

---

## 8. 책임 / 연락처

- **Maintainer**: Jaeseon Lee `<JaeseonLee@unist.ac.kr>`
- **본 가이드**: `02_data/raw/experiment/MEASUREMENT_GUIDE.md`
- **관련 문서**:
  - `02_data/processed/README.md` — dataset schema (12 columns)
  - `02_data/surface_cards/_index.md` — 기존 surface card 목록
  - `RELEASE_CHECKLIST.md` — 공개 release 절차
  - `phase2_flow_boiling/plan.md` — flow boiling 확장 계획
- **이슈**: GitHub Issues (수락 후 `UNIST-ITEL/pinn-onb01`)
