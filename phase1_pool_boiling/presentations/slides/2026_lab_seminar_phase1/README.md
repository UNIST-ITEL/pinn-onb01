# 2026 Lab Seminar — Phase 1 PINN-ONB 발표 자료

## 발표 메타데이터

| 항목 | 값 |
|---|---|
| Date | TBD (사용자 지정) |
| Location | UNIST ITEL (실내 lab seminar room) |
| Audience | Lab 내부 (boiling / heat transfer 전공 동료 + 지도교수) |
| Duration | 25 min talk + 10 min Q&A |
| Phase | 1 (IJHMT 제출 완료, review 대기) |
| Speaker | Jaeseon Lee (Gyuchang Kim 도 발표 가능) |
| Status | prompt drafted (2026-05-19) → Claude Design 에서 렌더링 예정 |

## 본 폴더의 4개 파일

| 파일 | 용도 |
|---|---|
| `prompt.md` | Claude Design (https://claude.ai/design) 에 paste할 메인 prompt — 15 슬라이드 구조 |
| `figure_list.md` | Claude Design 에 별도 업로드할 figure 목록 (필수 5 + 선택 3) |
| `speaker_notes.md` | 슬라이드별 narrative + 25분 시간 분배 + Q&A 예상 6건 |
| `README.md` | 본 파일 — metadata + workflow checklist |

## Workflow Checklist

- [x] **Step 1**: prompt.md, figure_list.md, speaker_notes.md 작성 완료 (seminar-prompt-builder, 2026-05-19)
- [ ] **Step 2**: Claude Design (https://claude.ai/design) 접속
- [ ] **Step 3**: `prompt.md` 내용 paste
- [ ] **Step 4**: `figure_list.md` 의 figures 업로드 (5 필수 + 3 선택)
- [ ] **Step 5**: Claude Design 생성 슬라이드 검토 (15 슬라이드 ± 1)
- [ ] **Step 6**: Speaker notes (`speaker_notes.md`) 를 PPTX 의 notes 영역에 통합
- [ ] **Step 7**: PPTX/PDF 다운로드 → 본 폴더에 저장 (`final.pptx` 또는 `final.pdf`)
- [ ] **Step 8**: Rehearsal — speaker_notes.md 시간 표 따라 실제 시간 측정
- [ ] **Step 9**: 발표 전 점검 — backup slides, equipment, 발표 본인 자료

## 청중별 발표 강조점

본 lab seminar (audience: lab_seminar) 특성:

- **친밀 톤** — 진척 보고 형식. 격식 발표 아님.
- **수식 OK** — 청중이 전공자이므로 Hsu criterion 등 수식 fully render
- **Q&A 길게** — 10 min Q&A 시간 충분 활용. 6개 예상 질문 (speaker_notes § Q&A)
- **Future work 강조** — Phase 1.5 / Phase 2 진행 방향 공유

## 변경 history

| 일자 | 작업 |
|---|---|
| 2026-05-19 | Initial drafting via seminar-prompt-builder agent (4 files generated) |
| TBD | Claude Design 렌더링 + PPTX 다운로드 |
| TBD | Speaker rehearsal + 시간 보정 |
| TBD | 발표 실시 |

## 재사용

본 prompt 는 향후 다음 용도 재활용 가능:

| 변형 발표 | 수정 사항 |
|---|---|
| **KSME 추계 학회** (15 min) | `/build-seminar-prompt 2026_KSME_phase1 --audience conference_KSME --duration 15` 로 새 prompt 생성. 슬라이드 9-10개로 축소. |
| **IHMTC 2026** (20 min) | conference_IHMTC audience, 12 슬라이드 |
| **Industry briefing** (30 min, 응용 청중) | audience=industry, value 강조 |
| **Thesis defense** (45 min, Gyuchang Kim 가능) | audience=thesis_defense, 25 슬라이드, 모든 design decision 정당화 |

## 책임자

- **Maintainer**: Jaeseon Lee `<JaeseonLee@unist.ac.kr>` (ORCID 0000-0003-1996-6086)
- **Co-presenters (선택)**: Gyuchang Kim (PINN 구현 chap 6-8), Eunjeong Ko (데이터 chap 9), Yujin Kim (figure)
- **Phase 1 paper status**: IJHMT submitted 2026-05-18, review 대기
