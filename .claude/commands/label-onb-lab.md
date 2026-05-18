---
description: lab-onb-labeler 호출 — Phase 1.5 lab boiling curve에서 ONB 라벨 자동 식별
argument-hint: <source_name>
---

# /label-onb-lab — Lab ONB 라벨링

본 명령은 **lab-onb-labeler** 서브에이전트를 호출하여 지정 lab 출처의
boiling curve 데이터에서 ONB 라벨을 자동 식별합니다.

## 입력 (`$ARGUMENTS`)

```
<source_name>    lab 출처 폴더명 (예: "lee_2023_ichmt")
```

해당 폴더에 `boiling_curves.csv` (또는 동등) 가 존재해야 함.

## 처리 흐름

1. `phase1p5_inhouse_augmentation/data/raw/lab/<source_name>/boiling_curves.csv`
   로드
2. `lab-onb-labeler` 에이전트 호출:
   - 자연대류 slope 계산 + 1.5x slope-change 탐지
   - Hsu envelope 검증
   - Admissible band (ΔT_ONB ∈ [0.7, 30] K) 검사
   - Quality tier A/B/C/D 부여
3. 결과 저장:
   - `phase1p5_inhouse_augmentation/data/processed/onb_labels_<source_name>.csv`
   - `phase1p5_inhouse_augmentation/data/lab_onb_labeling_report_<source_name>.md`

## 사용 예

```
/label-onb-lab lee_2023_ichmt
/label-onb-lab inhouse_corrosion
```

## 출력 보고

```
✓ <source>: N_curves 곡선 분석
✓ Auto-labeled: N_auto (Tier B)
⚠ Override: N_override (Hsu_violated / admissible_band)
⚠ Pending review: N_pending (Tier D)
✓ Output: onb_labels_<source>.csv (N_total rows)
✓ Report: lab_onb_labeling_report_<source>.md
```

## 주의사항

- Tier D (검토 필요) 가 있다면 사용자 검토 후 manual override 권장.
- 결과 CSV 는 Phase 1 `onb_dataset.csv` 12-column schema 동일.
- 통합 v1p5 dataset 작성 시: `preprocess-pipeline` 에이전트로 합치기.

## 인자

$ARGUMENTS
