---
description: ood-evaluator 호출 — Phase 1.5 Level 4 cross-lab generalization 검증
argument-hint: [--mode loo|lab-as-ood|lab-only|all] [--k-seeds <N>]
---

# /ood-eval — Cross-lab Generalization 검증

본 명령은 **ood-evaluator** 서브에이전트를 호출하여 Phase 1.5 의 Level 4
(cross-lab generalization) 검증을 수행합니다.

## 모드 (3가지 + all)

| Mode | 의미 | 학습 횟수 |
|---|---|---|
| `loo` (Leave-one-lab-out) | 11 출처 중 하나씩 제외 후 학습 | 11회 |
| `lab-as-ood` | Phase 1 외부 학습 → lab 4 출처 평가 | 0회 (사전 학습 활용) |
| `lab-only` | Lab 4 출처만 학습 → 외부 평가 | 1회 |
| `all` (기본) | 위 3가지 모두 | 12회 |

## 입력 (`$ARGUMENTS`)

```
--mode <loo|lab-as-ood|lab-only|all>    실행 모드 (기본: all)
--k-seeds <N>                            Seed 수 (기본: 1, robust: 3)
```

## 처리 흐름

1. `ood-evaluator` 에이전트가 모드별 학습/평가 수행
2. 결과 figures + tables 생성:
   - `phase1p5_inhouse_augmentation/analysis/figures/ood_matrix.png`
   - `phase1p5_inhouse_augmentation/analysis/figures/calibration_plot.png`
   - `phase1p5_inhouse_augmentation/analysis/figures/leave_one_lab_out_bar.png`
   - `phase1p5_inhouse_augmentation/analysis/tables/ood_metrics.md`
3. LOO 체크포인트 (선택):
   - `phase1p5_inhouse_augmentation/experiments/checkpoints/loo_<source>/`

## 사용 예

```
/ood-eval                              # 전체 (loo + lab-as-ood + lab-only), K=1
/ood-eval --mode lab-as-ood            # 빠른 baseline (학습 X)
/ood-eval --mode loo --k-seeds 3       # Robust LOO (33회 학습)
```

## 출력 보고

```
✓ Lab-as-OOD (사전 학습 Phase 1 baseline):
    Lee2023_ICHMT  : n=?, RMSE=? K, Cov95%=?
    Lee2024_ICHMT  : n=?, RMSE=? K, Cov95%=?
    inhouse_corr   : n=?, RMSE=? K, Cov95%=?
    inhouse_biphi  : n=?, RMSE=? K, Cov95%=?
✓ Leave-one-lab-out (K=1):
    11 출처 평균 test_RMSE: ? K
    최악 case: <source> = ? K
✓ Lab-only → external: RMSE=? K
✓ OOD matrix figure 생성
✓ Calibration plot 생성
```

## 학습 비용 예상

| Mode | K-seeds | 시간 (M1 CPU) |
|---|---|---|
| lab-as-ood | 0 | 5분 (학습 X) |
| lab-only | 1 | 30분 |
| loo | 1 | 6시간 |
| all | 1 | 7시간 |
| all | 3 (robust) | 21시간 |

GPU 사용 시 1/5.

## 주의사항

- LOO 학습은 비용 큼 — 첫 시도는 `--mode lab-as-ood` 로 빠른 baseline 권장.
- 데이터 부족 출처 (JO_2011 = 2 labels) 의 LOO 결과는 신뢰도 낮음 — 보고서에 명시.
- `lab-as-ood` 결과는 Phase 1 baseline_phaseDbal 의 lab data 일반화 baseline.
- Calibration plot 은 ICHMT paper 의 핵심 figure (F5 후보).

## 인자

$ARGUMENTS
