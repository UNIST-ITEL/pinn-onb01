---
description: Phase 1.5 V0-V5 ablation sweep 자동 실행 (training-orchestrator)
argument-hint: [--variants V0,V1,...] [--seeds <N>] [--config <path>]
---

# /ablate-phase1p5 — V0-V5 Ablation Sweep

본 명령은 **training-orchestrator** 에이전트를 호출하여 Phase 1.5 의
ablation 변형 V0-V5 를 자동 sweep합니다.

## Ablation 변형 (본 plan § 5.4)

| Variant | 학습 데이터 | 목적 |
|---|---|---|
| V0 | 외부 49 surface (Phase 1 baseline 재현) | 비교 baseline |
| V1 | 외부 + Lee2023/2024 laser | Laser family 단독 효과 |
| V2 | 외부 + inhouse_corrosion | Corrosion 단독 효과 |
| V3 | 외부 + inhouse_biphilic | Biphilic family 효과 |
| V4 | 외부 + lab 전체 (full) | **Phase 1.5 main result** |
| V5 | Lab data만 (역방향) | Lab 자체 일관성 |

## 입력 (`$ARGUMENTS`)

```
--variants V0,V1,...    (선택) 실행할 variant 부분집합 (기본: 전체 V0-V5)
--seeds <N>              (선택) Seed 수 (기본: 1, ensemble 시 10)
--config <path>          (선택) 기준 YAML (기본: baseline_phaseDbal.yaml)
```

## 처리 흐름

1. 각 variant 별로 데이터 분할 (data partitioning):
   - V0: `onb_dataset.csv` (Phase 1 외부 82 rows)
   - V1-V3: filter by source_paper
   - V4: 전체 v1p5
   - V5: Lab only
2. `training-orchestrator` 호출 (variant 당):
   - Phase 1 4-stage 학습 파이프라인 그대로 적용
   - MLflow run name: `phaseDbal_<variant>_seed<N>`
3. 결과 저장:
   - `phase1p5_inhouse_augmentation/experiments/checkpoints/<variant>/`
   - `phase1p5_inhouse_augmentation/experiments/logs/<variant>.log`
4. 자동 평가:
   - 각 variant 의 test_RMSE, MAE, R², coverage 95%
   - `phase1p5_inhouse_augmentation/analysis/tables/ablation_results.md`

## 사용 예

```
/ablate-phase1p5                          # 전체 V0-V5, K=1
/ablate-phase1p5 --variants V4,V5         # 일부만
/ablate-phase1p5 --seeds 10               # V4 main 에 ensemble K=10
```

## 출력 보고

```
✓ V0 (Phase 1 baseline 재현): test_RMSE = 3.45 K [sanity check vs 3.42]
✓ V1 (+laser): test_RMSE = 3.20 K (lab subset 4.5 K)
✓ V2 (+corrosion): test_RMSE = 3.18 K
✓ V3 (+biphilic): test_RMSE = 3.10 K
✓ V4 (full): test_RMSE = 2.85 K ⭐ main
⚠ V5 (lab only): test_RMSE on external = 7.5 K (학습 데이터 부족)
✓ Table: phase1p5_.../analysis/tables/ablation_results.md
```

## 학습 비용 예상

| Variant 수 | Seed 수 | 예상 시간 (M1 CPU) |
|---|---|---|
| 6 (V0-V5) | 1 | ~3시간 |
| 6 (V0-V5) | 10 (V4만 ensemble) | ~5시간 |

GPU 사용 시 1/5 수준.

## 주의사항

- V0 결과는 Phase 1 baseline 과 거의 일치해야 함 (sanity check).
- V5 (lab only) 는 학습 데이터 부족으로 RMSE 클 수 있음 — 정상.
- 결과 표는 ICHMT paper Table 2 후보.

## 인자

$ARGUMENTS
