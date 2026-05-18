# Phase 1.5 — In-house Pool-Boiling Data Augmentation

**Workspace**: PINN-BOILING
**상태**: 계획 단계 (Phase 1 IJHMT review 대기 중 병행 진행)
**기간**: 3.5-5개월 (Phase 1 review 시기와 중첩)
**목표 저널**: International Communications in Heat and Mass Transfer (ICHMT, 1순위) → Applied Thermal Engineering (2순위) → IJHMT short paper (3순위)

## 위치

본 폴더는 `PINN-BOILING` workspace 의 Phase 1.5 트랙 디렉토리이다.
Workspace 상위 `WORKSPACE_RESTRUCTURE_PROPOSAL.md` 의 옵션 C
(shared/ + tag-based freeze) 에 따라 구성됨.

## 핵심 목표

| 지표 | Phase 1 → 1.5 |
|---|---|
| Surface cards | 49 → **60-70** |
| ONB labels | 82 → **100-130** |
| Surface categories | 10 → **13+** (laser, corrosion, biphilic-extended 추가) |
| Test RMSE | 3.42 K → **≤ 3.0 K** |
| OOD RMSE | (Phase 1 미측정) → **≤ 5.0 K + 명시 평가** |
| Coverage | 98.7% → 유지 |

자세한 사양: `plan.md` (본 폴더 내)

## 데이터 소스 (4종)

| 출처 | 상태 | 표면 종류 | 폴더 |
|---|---|---|---|
| Lee2023_ICHMT (DOI 10.1016/j.icheatmasstransfer.2023.107072) | 공개 | Femtosecond laser periodic ripple | `data/raw/lab/lee_2023_ichmt/` |
| Lee2024_ICHMT (DOI 10.1016/j.icheatmasstransfer.2024.107270) | 공개 | Laser + Cu sintering | `data/raw/lab/lee_2024_ichmt/` |
| In-house corrosion | 미공개 | Cu 부식 친수화 | `data/raw/lab/inhouse_corrosion/` |
| In-house biphilic | 미공개 | Biphilic 패턴 | `data/raw/lab/inhouse_biphilic/` |

IP: 본 lab 전적 보유 (Jaeseon Lee 2026-05-18 확인).

## 폴더 구조

```
phase1p5_inhouse_augmentation/
├── README.md                       # 본 파일
├── data/
│   ├── raw/lab/                    # 4 출처별 raw + WPD project files
│   │   ├── lee_2023_ichmt/
│   │   ├── lee_2024_ichmt/
│   │   ├── inhouse_corrosion/
│   │   └── inhouse_biphilic/
│   ├── processed/                  # 통합 v1p5 데이터셋 (boiling_curves, onb_dataset)
│   └── surface_cards/              # SFC-051 ~ SFC-070+ (신규)
├── experiments/
│   ├── checkpoints/                # V0-V5 ablation 체크포인트 + ensemble
│   ├── configs/                    # YAML configs (Phase 1 baseline + 변형)
│   └── logs/                       # MLflow runs, training logs
├── analysis/
│   ├── figures/                    # 6-8 main figures (ablation, OOD, calibration)
│   ├── tables/
│   └── scripts/                    # Phase 1.5 전용 분석 스크립트
└── manuscript/                     # ICHMT main.tex + supplementary
```

## 진행 단계 (M1-M5)

| Stage | 기간 | 산출물 | 핵심 에이전트 |
|---|---|---|---|
| M1 인벤토리 + bib + baseline | 1개월 | `data/lab_data_inventory.md` + 갱신된 references.bib + OOD baseline | `paper-card-extractor`, `bibtex-curator`, `survey-search` |
| M2-M3 데이터 디지타이즈 + 라벨링 | 2개월 | SFC-051~070 카드, `data/processed/boiling_curves_v1p5.csv`, `onb_dataset_v1p5.csv` | `figure-digitizer`, `surface-card-builder`, `preprocess-pipeline`, **`lab-onb-labeler`** (신규) |
| M4 재학습 + ablation + OOD | 1개월 | V0-V5 결과, OOD matrix, calibration plot | `training-orchestrator`, `ensemble-uq`, `correlation-comparator`, `physics-consistency-check`, **`ood-evaluator`** (신규) |
| M5 Paper draft + figures | 1개월 | ICHMT submission package | `section-drafter`, `figure-composer`, `latex-formatter`, `bibtex-curator`, `reviewer-anticipator` |

자세한 단계별 에이전트 활용: 본 plan § 10.

## 신규 에이전트 (2개)

| Agent | 정의 위치 | 용도 |
|---|---|---|
| **lab-onb-labeler** | `../.claude/agents/lab-onb-labeler.md` | Lab boiling curve → ONB 라벨 자동 식별 + Hsu envelope 검증 |
| **ood-evaluator** | `../.claude/agents/ood-evaluator.md` | Level 4 cross-lab generalization 자동 평가 |

## 신규 슬래시 명령 (5개)

```
/add-lab-source <name>       새 lab data 출처 등록
/label-onb-lab <source>      lab-onb-labeler 호출
/ablate-phase1p5             V0-V5 sweep 자동 실행
/ood-eval                    ood-evaluator 호출
/draft-phase1p5-section <n>  ICHMT short format section 작성
```

## Phase 1 자산 재사용

| 자산 | 재사용 위치 |
|---|---|
| PINN architecture (`shared/src/pinn_onb/`) | `import pinn_onb` |
| 5 classical correlations | `predict_new_experiment.py` 그대로 (Phase 1 작성) |
| Deep ensemble (K=10, seeds 42-51) | 동일 seeds 사용 |
| 24 기존 에이전트 중 **19개** (79%) | `.claude/agents/` |

## 빠른 시작 (Phase 1.5 작업 시)

```bash
# 1. shared 패키지 editable 설치 (workspace root에서)
cd ../
pip install -e ./shared/src/

# 2. Phase 1.5 폴더로 이동
cd phase1p5_inhouse_augmentation/

# 3. 데이터 인벤토리 작성 (M1)
# lab_data_inventory.md 채우기

# 4. 현 Phase 1 모델로 lab data baseline 측정
python ../04_analysis/scripts/predict_new_experiment.py \
    --csv data/processed/lab_baseline_test.csv \
    --run-name lab_baseline_M1

# 5. (M4) Ablation 실행
# (Phase 1.5 전용 training script 추후 작성)
```

## 책임자

- **Maintainer**: Jaeseon Lee `<JaeseonLee@unist.ac.kr>` (ORCID 0000-0003-1996-6086)
- **데이터 측정 (laser)**: Seunghwan Lee, Yeonsu Kim, Hyungson Ki (Lee2023/2024 ICHMT 공저)
- **PINN ML**: Gyuchang Kim (1st-tier), Eunjeong Ko, Yujin Kim
