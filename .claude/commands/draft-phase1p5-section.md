---
description: Phase 1.5 ICHMT short paper 섹션 초안 작성 (section-drafter, 4-5K words constraint)
argument-hint: <section_number_or_name>
---

# /draft-phase1p5-section — ICHMT 섹션 초안

본 명령은 **section-drafter** 서브에이전트를 호출하여 Phase 1.5 ICHMT
short paper 의 특정 섹션 초안을 작성합니다.

## ICHMT Short Paper 구조 (target ≤ 5000 words)

| # | 섹션 | 권장 단어 수 |
|---|---|---|
| 1 | Introduction | 600-800 |
| 2 | Dataset and methodology (Phase 1 framework 요약 + Phase 1.5 보강) | 800-1000 |
| 3 | Cross-lab generalization analysis | 1500-2000 |
| 4 | Discussion (laser, corrosion, biphilic family 결과 + limitations) | 800-1000 |
| 5 | Conclusions | 300-400 |

## 입력 (`$ARGUMENTS`)

다음 중 하나:
- 섹션 번호: `1`, `2`, ..., `5`
- 섹션 이름: `intro`, `methods`, `results`, `discussion`, `conclusions`
- 또는 `abstract`, `highlights`, `nomenclature`

## 처리 흐름

1. 입력 섹션 식별
2. `section-drafter` 호출:
   - **Phase 1 paper와의 차별점 명확화** — salami slicing 우려 회피
   - 4:6 long:short sentence mix 유지 (Phase 1 동일)
   - Native English tone (Phase 1 동일 style)
   - 본 Phase 의 핵심 claim:
     - Cross-lab generalization 정량 검증
     - Laser/corrosion/biphilic family 추가의 marginal contribution
     - OOD ensemble UQ calibration
3. 결과 저장:
   - `phase1p5_inhouse_augmentation/manuscript/sections/<n>_<name>.tex`

## 사용 예

```
/draft-phase1p5-section 1
/draft-phase1p5-section intro
/draft-phase1p5-section abstract
```

## 출력 보고

```
✓ Section <n> (<name>) 초안 작성
  - 단어 수: N (target: <target>)
  - 4:6 mix 비율: actual ratio
  - Phase 1과 중복 표현 검출: N건 (확인 권장)
✓ 저장: phase1p5_.../manuscript/sections/<n>_<name>.tex
```

## Phase 1과의 차별 framing 가이드

ICHMT reviewer 가 salami slicing 우려를 제기할 수 있으므로 다음 framing 적용:

| Phase 1 paper 주장 | Phase 1.5 paper 주장 |
|---|---|
| "Curated literature corpus 학습 PINN으로 ONB 예측 framework 제시" | "동일 framework가 cross-lab 일반화하며 laser/corrosion 신규 family 에서도 성립" |
| 49 surface, 82 ONB, 외부만 | 60-70 surface, 100-130 ONB, 외부 + lab |
| Level 1-3 검증 | **Level 4 (NEW)** cross-lab generalization |
| Ensemble UQ calibration 미보고 | **Calibration plot 정식 보고** |
| Per-fluid/per-source breakdown | **Per-surface-family marginal contribution analysis** |

## 주의사항

- ICHMT 는 short format — 단어 수 엄격히 관리.
- Phase 1 본문에서 표현/문장 직접 인용 시 self-plagiarism 위험 — 표현 다듬기 필수.
- Hsu 기준식, PDE 등 수식은 Phase 1과 동일하므로 짧게 referencing (Lee et al. 2026).

## 인자

$ARGUMENTS
