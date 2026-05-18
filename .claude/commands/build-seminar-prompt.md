---
description: seminar-prompt-builder 호출 — Phase manuscript/figures → Claude Design prompt.md 자동 생성
argument-hint: <event_name> [--phase 1|1.5|2] [--audience lab_seminar|conference|thesis_defense|industry] [--duration <min>]
---

# /build-seminar-prompt — 발표 자료 prompt 생성

본 명령은 **seminar-prompt-builder** 서브에이전트를 호출하여 Phase 별
manuscript / figures / 핵심 결과를 분석하고 **Claude Design**
(https://claude.ai/design) 또는 다른 슬라이드 생성 도구에 paste할 수
있는 4개 markdown 파일을 자동 생성합니다.

## 입력 (`$ARGUMENTS`)

```
<event_name>             폴더 식별자 (snake_case, 예: "2026_lab_seminar_phase1")
--phase <1|1.5|2>         (기본: 1)
--audience <type>         lab_seminar (기본) / conference_KSME / conference_IHMTC / thesis_defense / industry
--duration <minutes>      (기본: 25; 학회 보통 15, defense 보통 45)
--slide-count <N>         (선택, 기본 duration×0.6 자동)
--focus <topic>           (선택) 강조 주제 (예: "ablation", "OOD", "future_work")
```

## 처리 흐름

1. **출력 폴더 생성**:
   - Phase 1 → `phase1_pool_boiling/presentations/slides/<event_name>/`
   - Phase 1.5 → `phase1p5_inhouse_augmentation/presentations/slides/<event_name>/`
   - Phase 2 → `phase2_flow_boiling/presentations/slides/<event_name>/` (folder 신설)

2. **자산 분석**:
   - Phase 별 manuscript sections → narrative 추출
   - figures 디렉토리 → file 목록
   - references.bib → 핵심 인용
   - PHASE_STATUS.md → 진행 단계 / 결과 요약
   - reviewer_rebuttal.md (있다면) → 예상 Q&A 후보

3. **4개 파일 생성**:
   - `prompt.md` — Claude Design 에 paste할 메인 prompt
   - `figure_list.md` — 별도 업로드할 figure 경로 목록
   - `speaker_notes.md` — 슬라이드별 narrative + 시간 분배
   - `README.md` — 발표 메타데이터 + workflow 체크리스트

## 청중별 자동 분기

| Audience | 톤 | 시간 분배 (motivation / method / results / future) |
|---|---|---|
| lab_seminar | 친밀, 진척 보고 | 20 / 30 / 35 / 15 % |
| conference_KSME / IHMTC | 격식, headline | 15 / 25 / 45 / 15 % |
| thesis_defense | 방어, 완전 정당화 | 15 / 35 / 35 / 15 % |
| industry | 응용 가치 중심 | 30 / 15 / 40 / 15 % |

## 사용 예

```bash
# 가장 기본 — Phase 1 lab seminar 25분
/build-seminar-prompt 2026_lab_seminar_phase1

# KSME 학회 15분 발표 (Phase 1)
/build-seminar-prompt 2026_KSME_phase1 --audience conference_KSME --duration 15

# Phase 1.5 KSME 발표
/build-seminar-prompt 2026_KSME_phase1p5 --phase 1.5 --audience conference_KSME

# 학위논문 발표 45분
/build-seminar-prompt defense_kim_2027 --audience thesis_defense --duration 45

# Phase 1 발표에 OOD 결과 강조
/build-seminar-prompt 2026_lab_phase1_ood_focus --focus OOD
```

## 출력 보고

```
✓ Folder: phase1_pool_boiling/presentations/slides/2026_lab_seminar_phase1/
✓ prompt.md: 16 슬라이드 구조 + 9 figure references
✓ figure_list.md: 9 files (모두 경로 존재 확인 완료)
✓ speaker_notes.md: 25 min 시간 분배 + Q&A 5 min
✓ README.md: 발표 metadata + workflow checklist (7 단계)

다음 단계:
  1. prompt.md 검토 / 수정
  2. https://claude.ai/design 접속
  3. prompt.md 내용 paste + figure_list.md 의 9 files 업로드
  4. 생성된 slide deck 검토 → PPTX/PDF 다운로드
  5. 본 폴더에 저장 → README.md 갱신
```

## 후속 발표 시 — 동일 event 재호출

`event_name` 동일하게 호출하면 **prompt.md 갱신** + 기존 speaker_notes / README
보존 (덮어쓰기 전 확인 prompt).

## 관련 슬래시 명령

- `/draft-phase1p5-section <n>` — Phase 1.5 paper section 작성 (slide 가 아닌 paper용)
- `/add-paper` — 새 인용 추가 (paper 본문 + 발표 references)

## 인자

$ARGUMENTS
