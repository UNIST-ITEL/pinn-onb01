# Phase 1 — Pool-Boiling ONB (풀비등 ONB)

> ⚠️ **담당 컴퓨터 확인 — Phase 1**
>
> 본 phase 는 **`macmini` (호스트: `MyHomeMiniui-Macmini.local`, 사용자: `myhomemini`)** 전용입니다.
> Phase 1 작업은 워크스페이스 root 또는 본 폴더에서 수행하며, **다른 컴퓨터 (Phase 2 host 등)** 에서는
> 본 phase 의 파일을 **쓰지 마세요** (read-only 참조만 허용).
>
> 잘못된 컴퓨터에서 열었다면 즉시 Claude Code 를 종료하고 담당자(Jaeseon Lee)에게 알려주세요.
> 자세한 매핑은 root `HOSTS.md`, 운영 원리는 `claude-code-multi-project-guide.md` 참조.

## Phase 1 상태 (2026-05-20)

- **결과**: IJHMT 제출 완료 (2026-05-18), peer-review 대기
- **모델**: Surface-conditioned PINN + FiLM encoder + deep ensemble UQ (K=10)
- **성능**: RMSE 3.42 K (vs Basu 7.21 K, **53% 개선**), coverage 98.7%
- **데이터**: 7 papers / 49 surfaces / 82 ONB labels / 4 fluids (water, R-134a, R-123, FC-77 제외)

## 작업 위치 (2026-05-27 이동 완료)

Phase 1 의 실제 산출물은 **본 폴더 (`phase1_pool_boiling/`) 아래**로 이동했습니다 (2026-05-27,
구조 혼동 해소 목적, **폴더명 유지** — root 평면 구조에서 `git mv`):

| 단계 | 위치 |
|---|---|
| ① 서베이 | `phase1_pool_boiling/01_survey/` |
| ② 데이터 | `phase1_pool_boiling/02_data/` |
| ③ 모델링 | `phase1_pool_boiling/03_model/` |
| ④ 분석/검증 | `phase1_pool_boiling/04_analysis/` |
| ⑤ 원고 | `phase1_pool_boiling/05_manuscript/` |
| 발표 자료 | `phase1_pool_boiling/presentations/` |

폴더명을 유지했으므로 코드의 동적 root 탐색(`02_data/` 를 찾아 올라감)과 config 상대경로가 그대로
동작합니다 (코드 무수정). 잔여 정식 Stage 2 (폴더명 변경 + `shared/src/pinn_onb/` 코드 분리 +
`git tag phase1-v1.0-published`) 는 **IJHMT acceptance 후** 진행.

## 본 폴더 (현재)

```
phase1_pool_boiling/
├── CLAUDE.md            ← 본 파일 (Phase 1 컴퓨터 경고 + 컨텍스트)
├── 01_survey/           ← 서베이 (paper_database, gap_matrix)
├── 02_data/             ← 데이터 (raw, processed, surface_cards, scripts)
├── 03_model/            ← 모델 (src, configs, experiments[mlruns])
├── 04_analysis/         ← 분석/검증 (figures, tables, scripts, reports)
├── 05_manuscript/       ← 원고 (tex, bib, sections, SUBMISSION)
└── presentations/       ← 발표 자료 (slides, posters, reports, outreach, abstracts)
    └── slides/2026_lab_seminar_phase1/   ← 첫 lab seminar deliverable
```

## Phase 1 작업 시 우선순위

1. **Reviewer 회신 대비** — `05_manuscript/reviewer_rebuttal.md` 점진 작성
2. **추가 발표 자료** — `presentations/slides/` 에 학회·세미나용 prompt 작성 (`/build-seminar-prompt`)
3. **잔여 Stage 2 마이그레이션** — IJHMT acceptance 직후 폴더명 변경 + `shared/src` 코드 분리
   (`WORKSPACE_RESTRUCTURE_PROPOSAL.md` § Stage 2). 폴더 이동 자체는 2026-05-27 선행 완료.

## 참고

- Phase 1 plan: `../ONB_PINN_Phase1_Pool_Boiling_Plan.md`
- 본 phase 관련 28 agents + 7 commands: root `.claude/`
- 문체 review: **academic-writing-reviewer** (native-English, tone/voice/sentence-variety) — `05_manuscript/sections/*.tex` 에 적용 가능. Reviewer 회신용 rebuttal 문체 다듬기에도 활용.
- Phase 1 ↔ 1.5 ↔ 2 관계: root `PHASE_STATUS.md`, `HOSTS.md`
