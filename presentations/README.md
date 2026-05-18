# `presentations/` — Workspace-level Presentations & Reports

본 폴더는 **PINN-BOILING workspace의 cross-phase 발표/보고 자료**를 보관한다.
특정 phase에만 해당하는 자료는 각 phase 폴더의 `presentations/` 에 보관.

## 보관 대상

| 폴더 | 내용 |
|---|---|
| `workspace_overview/` | PINN-BOILING 전체 소개 슬라이드, one-pager, vision statement |
| `grant_reports/` | NRF / KETEP 등 기금 통합 보고서 (여러 phase 망라) |
| `lab_meetings/` | 주간/월간 lab meeting 자료 (workspace 전체) |
| `thesis_defense/` | 학위논문 발표 자료 (예: Gyuchang Kim, Eunjeong Ko 학위 발표) |

## Phase 별 자료는 phase 폴더로

| 종류 | 위치 |
|---|---|
| Phase 1 학회 발표 | `phase1_pool_boiling/presentations/slides/<YYYY>_<conf>/` |
| Phase 1.5 학회 발표 | `phase1p5_inhouse_augmentation/presentations/slides/...` |
| Phase 별 진척 보고 | `phase*/presentations/reports/` |
| Phase 별 포스터 | `phase*/presentations/posters/` |

## 파일 명명 규칙

```
slides/<YYYY>_<event>_<topic>/main.pptx
slides/<YYYY>_<event>_<topic>/main.pdf       (compiled, final)

reports/<YYYY>_<MM>_<source>_<type>.<ext>
  예: 2026_06_NRF_annual.docx
      2026_07_KETEP_progress.pdf
```

## Git 관리 (`.gitignore` 적용됨)

| 파일 | git |
|---|---|
| Final PDF (`*.pdf`) | ✅ commit |
| Markdown 보고서 (`*.md`) | ✅ commit |
| Editable source (`*.pptx`, `*.key`, `*.docx`) | ⚠️ 선택 (워크스페이스 정책: commit 안 함 — 외부 백업) |
| Working drafts (`*.tmp`, `~$*`) | ❌ ignore |

policy: 외부 발표 후 **공식 final PDF만** commit 권장. Source 파일은 작성자의
OneDrive / Dropbox 등 외부 보관.

## IP 주의

- Phase 1 review 중 (현재) : 미공개 결과 슬라이드는 **internal only**
- Phase 1 수락 후 ~ 게재 전: 결과 발표 OK, paper DOI placeholder
- 게재 후: 모든 자료에 paper + dataset DOI 명시

## 책임자

- Maintainer: Jaeseon Lee `<JaeseonLee@unist.ac.kr>`
