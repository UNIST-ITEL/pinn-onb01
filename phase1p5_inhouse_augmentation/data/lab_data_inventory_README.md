# `lab_data_inventory.xlsx` — 사용 가이드 (대학원생 입력자용)

**대상**: Phase 1.5 in-house data 수집 담당 학생
**파일**: `lab_data_inventory.xlsx` (본 폴더)
**작성일**: 2026-05-19
**문의**: Jaeseon Lee `<JaeseonLee@unist.ac.kr>`

---

## 1. 본 파일의 역할

`lab_data_inventory.xlsx`는 **Phase 1.5 lab 데이터 수집을 추적하는 master
spreadsheet** 입니다. 4개 출처 (Lee 2023 / 2024 ICHMT 공개 논문 + 미공개
부식 + 미공개 biphilic) 의 모든 표면별 metadata를 담습니다.

이 파일을 채워야 다음 단계가 진행됩니다:

```
[학생 작업] lab_data_inventory.xlsx 작성
       ↓
       (CSV export — Claude/script 가능)
       ↓
[Claude/script] surface-card-builder → SFC-051..yaml 자동 생성
       ↓
[Claude/script] preprocess-pipeline → boiling_curves_v1p5.csv 통합
       ↓
[Claude] PINN 학습 (V0-V5 ablation)
```

---

## 2. 7개 시트 구성

| # | 시트 이름 | 내용 |
|---|---|---|
| 1 | **Overview** | 4 출처 요약 (status, # surfaces, # curves, # ONB 등) |
| 2 | **Lee_2023_ICHMT** | 표면별 metadata (Cu 레이저 ripple) |
| 3 | **Lee_2024_ICHMT** | 표면별 metadata (Cu sinter + laser) |
| 4 | **Inhouse_corrosion** | 표면별 metadata (Cu 부식 친수화) |
| 5 | **Inhouse_biphilic** | 표면별 metadata (biphilic 패턴) |
| 6 | **Boiling_curves** | 모든 boiling curve 측정점 (long format) |
| 7 | **ONB_labels** | ONB 시점만 모은 부분집합 |

각 시트의 **헤더 행 (1행)** 에 셀 코멘트 (마우스 호버 시 표시) 가 있어
각 컬럼이 무엇을 의미하는지 설명합니다.

각 source 시트 (2-5번)에는 **연두색 italic 예시 행** 이 있습니다. 실제
데이터 입력 시 이 행을 **지우거나 위에 덮어쓰기** 하시면 됩니다.

---

## 3. 입력 절차 — 단계별

### Step 1: Overview 시트 채우기

| 컬럼 | 입력값 |
|---|---|
| `source` | 이미 4개 row 채워져 있음 |
| `doi` | 공개 논문은 채워져 있음 |
| `status` | drop-down: TBD / in_progress / complete / blocked |
| `raw_data_format` | drop-down: CSV / Excel / paper_figure_only / mixed / no_data |
| `sem_available` | drop-down: Yes / No / partial |
| `n_surfaces_target` | 예상 surface 수 (예: 5) |
| `responsible_student` | 입력자 이름 |
| `deadline_M1_M3` | 본인 데드라인 (예: "2026-07-15") |

→ Step 1 완료 시 4 출처의 데이터 가용성이 한눈에 보임.

### Step 2: 각 source 시트 (Lee_2023_ICHMT 등) 채우기

표면 한 개당 한 행. 컬럼 의미는 헤더 셀 코멘트 참조.

**필수 컬럼** (반드시 채우기):
- `surface_id` — `SFC-051` 부터 차례로 (다음 가용 ID는 _index.md 확인 후 결정)
- `surface_label` — 사람이 이해 가능한 이름 (예: `Cu_laser_F20`)
- `material` — drop-down (Cu / Al / SS / ...)
- `treatment_primary` — 자유 텍스트 (예: `laser_ripple`, `Cu_sinter+laser`)
- `fluid` — drop-down (water / R-123 / R-134a)
- `Ra_um` — μm 단위. **nm 값은 ÷1000 변환** 필수
- `n_boiling_curves` — 이 표면에서 측정된 boiling curve 수
- `n_onb_labels_extractable` — ONB 식별 가능한 라벨 수 (보통 1-3)
- `data_quality_tier` — drop-down (A / B / C / D)

**선택 컬럼** (가능하면 채우기, 빈칸 OK):
- `treatment_parameters` — 자유 텍스트로 가공 조건 (laser fluence, etch time 등)
- `theta_static_deg` — 측정값 있다면
- `pressure_kPa` — water at 1 atm = 101.325; R-134a 5 bar = 500
- `subcooling_K` — saturated test면 0
- `heater_geometry` / `heater_size_mm` — 실험 형상
- `sem_*` — SEM 이미지 파일명 (실파일은 `data/raw/lab/<source>/sem/` 에 보관)
- `N_s_per_cm2`, `r_c_distribution_um` — SEM 정량 분석 결과 (있을 때만)
- `experiment_date`, `experimenter`, `thesis_used_in`, `notes` — provenance

### Step 3: Boiling_curves 시트 채우기

각 측정점 한 행. 한 surface에서 여러 측정점 (q'' 변화에 따른 측정).

**최소 입력**:
- `source_paper` — drop-down
- `figure_ref` — 원본 figure 또는 run 식별자
- `surface_id` — Step 2의 SFC-NNN 와 일치
- `fluid` — drop-down
- `delta_T_wall` — K
- `q_flux` — **W/m²** (kW/m²면 ×1000)
- `ONB_flag` — TRUE (ONB 점) / FALSE (일반 점)
- `notes` — `ONB_manual` 또는 `ONB_auto` 또는 자유 텍스트

> **참고**: Raw boiling curve가 CSV/Excel 로 별도 있다면, 본 시트에 모두 옮길
> 필요 없이 그 파일을 `data/raw/lab/<source>/boiling_curves.csv`에 그대로 두고
> 본 시트에는 **ONB 시점만** 입력해도 됩니다.

### Step 4: ONB_labels 시트 채우기 (자동 또는 수동)

ONB 시점만 모은 부분집합 (Boiling_curves 시트에서 `ONB_flag=TRUE` 만).

선택지 A: **Boiling_curves 시트만 채우고 ONB_labels 시트는 비워둠**
  → 후속 Claude가 자동 추출.

선택지 B: **두 시트 모두 직접 채움** (검증 용이)

---

## 4. 단위 / 명명 규칙 (필수 준수)

| 변수 | 단위 | 예시 | 흔한 실수 |
|---|---|---|---|
| `Ra_um` | μm | `0.5` | nm 그대로 입력 (`500` 잘못 → `0.5` 맞음) |
| `theta_deg` | ° (degree) | `85` | radian (`1.48` 잘못) |
| `delta_T_wall` | K | `5.2` | °C 표기 (값은 같음) — `T_wall - T_sat` 이라는 점 명심 |
| `delta_T_sub` | K | `0.0` (saturated) | 음수 (`-` 부호 빼야) |
| `q_flux` | **W/m²** | `50000` | kW/m² (`50`) — ×1000 변환 필요 |
| `pressure_kPa` | kPa | `101.325` | Pa (`101325`) 또는 bar (`1.013`) |

---

## 5. Data Quality Tier 결정 가이드

본 plan § 4.4 (Phase 1.5) 기반:

| Tier | 조건 |
|---|---|
| **A** | Raw CSV 보존 + **시각화로 ONB 확인** + 측정 불확실도 명시 |
| **B** | Raw CSV + **slope-change** 기준 ONB (시각화 없음) |
| **C** | 보고서/논문 figure 만 → **WebPlotDigitizer 디지타이즈** + slope-change |
| **D** | **모호** — Hsu envelope 위반, admissible band 벗어남, 검토 필요 |

Tier D는 manual review 후 사용 또는 제외 결정.

---

## 6. 자주 묻는 질문

### Q1. 같은 표면에서 여러 실험 (날짜 / 조건 다름)이 있다면?

A: `surface_id` 는 동일 (예: `SFC-051`), `figure_ref` 또는 `notes` 에 trial
구분 표기. 예: `figure_ref=run01_2023-05-15`, `figure_ref=run02_2023-06-10`.

### Q2. SEM 이미지 r_c 추출이 어려운데 빈칸 OK?

A: 빈칸 OK. 본 column 은 supplementary용이며, 모델 학습에는 미사용.
SEM 이미지 파일명만 채워두면 가치 있음 (paper supplementary에 첨부 가능).

### Q3. ONB 시점 식별이 모호하다면?

A: 셋 중 하나:
1. **시각화 자료 있음** → 그 시점 manual label, notes에 "ONB_visual" 명시
2. **시각화 없음, boiling curve slope change 가능** → slope×1.5 기준,
   notes에 "ONB_slope_change" 명시
3. **모두 모호** → row 입력하지 말고 Boiling_curves 시트에 그냥 측정점만 추가
   (`ONB_flag=FALSE`). 후속 Claude `lab-onb-labeler` 가 처리.

### Q4. 미공개 데이터 (corrosion, biphilic) 의 IP 우려?

A: Lab 전적 보유로 협의 불필요 (2026-05-18 PI 확인). Phase 1.5 paper에서
첫 publication. `notes` 에 측정자 / 학위논문 사용 여부만 기록.

### Q5. 실험 압력이 atm 외 다른 값이면?

A: `pressure_kPa` 에 정확히 입력. 단, **본 PINN 모델은 R-134a 5 bar /
water 1 atm으로 hard-coded** — 다른 압력은 정확도 저하. notes 에 명시 권장.

### Q6. 일부 컬럼만 채워도 되나?

A: § 3 의 "필수 컬럼" 만 채우면 시작 가능. 선택 컬럼은 데이터 가용성에 따라.
"unknown" 또는 빈칸으로 둬도 후속 처리 가능 (단, 정확도 저하 risk).

### Q7. Excel 외 다른 도구 (Google Sheets) 사용 가능?

A: 가능. 단, drop-down 검증 / 셀 코멘트가 Google Sheets에서 100% 호환되지
않을 수 있음. 최종은 **xlsx 형식으로 저장** 권장.

---

## 7. 입력 완료 후 절차

### M1 (월 1) 완료 기준 ☐

- [ ] Overview 시트의 4개 출처 모두 status ≠ `TBD`
- [ ] 각 출처별 `raw_data_format` 식별
- [ ] 데이터 가용성 부족 (no_data, blocked) 출처는 별도 보고

### M2-M3 (월 2-3) 완료 기준 ☐

- [ ] 각 source 시트의 surface row 모두 입력
- [ ] Boiling_curves 시트에 최소 모든 ONB row 입력
- [ ] ONB_labels 시트 — 자동 추출 또는 수동 채움
- [ ] Data quality tier A/B/C/D 모든 row 부여

### CSV export (M3 종료 시점)

xlsx → csv 자동 export:

```bash
cd "/Users/myhomemini/Library/CloudStorage/OneDrive-개인/Projects/PINN-ONB01"
# (export script 추후 작성 예정)
python3 02_data/scripts/export_inventory_to_csv.py \
    --xlsx phase1p5_inhouse_augmentation/data/lab_data_inventory.xlsx \
    --out-dir phase1p5_inhouse_augmentation/data/processed/
```

생성될 파일:
- `boiling_curves_v1p5_partial.csv` (Boiling_curves 시트)
- `onb_dataset_v1p5_partial.csv` (ONB_labels 시트)
- `surface_metadata.csv` (4 source 시트 통합)

이후 Claude `preprocess-pipeline` 에이전트가 Phase 1 데이터와 합쳐
최종 `boiling_curves_v1p5.csv`, `onb_dataset_v1p5.csv` 생성.

---

## 8. Git 관리

- **xlsx 자체** : commit 권장 (workspace 상 크기 작음, 30KB 수준)
- 학생들이 채워나가며 git push 하면 PI 가 진척 확인 가능
- 파일 충돌 방지: **한 번에 한 학생만 편집** 또는 OneDrive sync 활용
- xlsx 충돌 시: backup branch에서 manual merge

권장 commit 빈도: **각 source 시트 완료 시** (4번 commit)

---

## 9. 책임자

- **Inventory maintainer**: Jaeseon Lee
- **데이터 제공 (Lee 2023/2024 laser)**: Seunghwan Lee, Yeonsu Kim
- **데이터 제공 (Inhouse corrosion/biphilic)**: 측정자 (TBD)
- **Phase 1.5 PINN ML**: Gyuchang Kim, Eunjeong Ko, Yujin Kim

문의 / 데이터 추가 / 컬럼 확장 요청: Jaeseon Lee `<JaeseonLee@unist.ac.kr>`
