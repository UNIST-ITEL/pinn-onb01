# `phase1_pool_boiling/presentations/` — Phase 1 발표·보고 자료

본 폴더는 **Phase 1 (pool boiling ONB, 외부 corpus)** 의 발표·보고 자료
전용이다. Cross-phase 자료는 workspace 루트 `presentations/`.

## 폴더 구성

| 폴더 | 내용 | 형식 |
|---|---|---|
| `slides/` | 구두 발표 (학회, 세미나) | .pptx + final .pdf |
| `slides/archive/` | 옛 버전, 작업 중 draft | (commit 안 함) |
| `posters/` | 학회 포스터 | .pdf (A0 final) + source |
| `reports/` | 서면 보고서 (지도교수, 기금, 학내) | .docx, .pdf, .md |
| `outreach/` | 보도자료, SNS, 블로그 | .md, .png |
| `conference_abstracts/` | 학회 abstract submission | .txt, .pdf |

## 명명 규칙

```
slides/<YYYY>_<event_or_conf>_<topic>/
  예: 2026_KSME_spring_phase1_main_results/
      2026_lab_seminar_phase1_overview/

posters/<YYYY>_<conf>_A0.pdf
  예: 2026_KSME_A0.pdf

reports/<YYYY>_<MM>_<source>_<type>.<ext>
  예: 2026_06_NRF_phase1_progress.docx
      2026_07_advisor_phase1_review.md
```

## Stage 2 마이그레이션 대비

본 폴더는 **Stage 2 마이그레이션 대비 forward-looking placeholder** 이다.
현재 Phase 1 의 본 코드/데이터는 워크스페이스 root 의 `01_survey/`, `02_data/`,
`03_model/`, `04_analysis/`, `05_manuscript/` 에 있다.

Phase 1 게재 수락 후 Stage 2 마이그레이션 시 위 5개 폴더가 본 폴더로 이동.

## IP 주의 (Phase 1)

- 현재 (2026-05-19) Phase 1 paper IJHMT review 중.
- **미공개 결과 슬라이드는 외부 노출 제한** (소수 internal 청중만).
- 슬라이드에 IJHMT 제출 paper DOI는 게재 확정 후 삽입.
- Reviewer 정보 / pre-print 내용 슬라이드 작성 시 신중.

## 권장 발표 일정 (Phase 1)

| 시점 | 종류 | 청중 |
|---|---|---|
| Review 중 | 연구실 internal seminar (lab_seminar) | UNIST ITEL 내부 |
| 수락 후 | KSME 추계/IHMTC 학회 발표 | 국내외 비등 커뮤니티 |
| 게재 후 | 보도자료 + SNS | 일반 학술 community |
