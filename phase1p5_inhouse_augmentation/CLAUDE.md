# Phase 1.5 — In-House Lab Data Augmentation

> ⚠️ **담당 컴퓨터 확인 — Phase 1.5**
>
> 본 phase 는 **`macmini` (호스트: `MyHomeMiniui-Macmini.local`, 사용자: `myhomemini`)** 전용입니다.
> Phase 1 (root) 과 같은 컴퓨터에서 진행되며, **Phase 2 컴퓨터에서는 본 폴더에 쓰기 금지** (read-only 참조만).
>
> 잘못된 컴퓨터에서 열었다면 즉시 Claude Code 를 종료하고 담당자(Jaeseon Lee)에게 알려주세요.
> 자세한 매핑은 root `HOSTS.md`, 운영 원리는 root `claude-code-multi-project-guide.md` 참조.

## Phase 1.5 상태 (2026-05-20)

- **단계**: M1 (인벤토리) — 진행 중. 학생들 lab data 회신 대기.
- **목표 산출물**: ICHMT short paper + V0-V5 ablation + OOD matrix
- **신규 surface category**: `unist_laser`, `unist_corrosion`, `unist_biphilic`
- **참조 데이터**: Lee 2023 ICHMT (laser), Lee 2024 ICHMT (laser/biphilic), unpublished Cu corrosion + biphilic

## 본 폴더 구조

```
phase1p5_inhouse_augmentation/
├── CLAUDE.md            ← 본 파일
├── README.md            ← Phase 1.5 entry point
├── plan.md              ← 상세 계획 (M1-M5)
├── data/
│   ├── lab_data_inventory.xlsx        ← 학생 입력용 워크북 (7 sheets)
│   ├── lab_data_inventory_README.md   ← 학생 가이드 (9 sections + FAQ)
│   ├── raw/lab/{lee_2023_ichmt, lee_2024_ichmt, inhouse_corrosion, inhouse_biphilic}/
│   ├── processed/       ← boiling_curves_v1p5.csv + onb_dataset_v1p5.csv
│   └── surface_cards/   ← SFC-051~070+ (laser/corrosion/biphilic)
├── experiments/
│   ├── checkpoints/     ← V0-V5 모델
│   ├── configs/         ← YAML configs (per V*)
│   └── logs/            ← MLflow runs
├── analysis/
│   ├── figures/         ← OOD matrix, calibration plot, ablation
│   ├── scripts/         ← ablation runner, OOD eval
│   └── tables/
├── manuscript/          ← ICHMT main.tex (M5)
└── presentations/       ← slides, posters, reports
```

## Phase 1.5 작업 시 우선순위

1. **학생 데이터 회신 대기** — `data/lab_data_inventory.xlsx` 회수 후 `02_data/scripts/export_inventory_to_csv.py` 실행
2. **Lab boiling curve 라벨링** — `/label-onb-lab` 호출, `lab-onb-labeler` 에이전트 사용
3. **V0-V5 ablation** — `/ablate-phase1p5` 호출
4. **OOD 검증** — `/ood-eval --mode leave-one-lab-out` 등 3 mode

## 관련 slash commands

| Command | 용도 |
|---|---|
| `/add-lab-source` | 새 lab boiling curve 등록 |
| `/label-onb-lab` | ONB labeling (slope-change + Hsu envelope) |
| `/ablate-phase1p5` | V0-V5 ablation 실행 |
| `/ood-eval` | Level 4 cross-lab generalization |
| `/draft-phase1p5-section <n>` | manuscript section 작성 |

## 참고

- Phase 1.5 plan: `plan.md` (831 lines)
- Phase 1 결과: root `01_survey/~05_manuscript/`, `phase1_pool_boiling/`
- 컴퓨터 매핑: root `HOSTS.md`
