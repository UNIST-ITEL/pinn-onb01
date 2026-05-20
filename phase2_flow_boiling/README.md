# Phase 2 — Forced-Convection Subcooled Flow Boiling ONB

> 📍 **담당 컴퓨터**: TBD — Phase 2 전용 host (root `HOSTS.md` 참조)
> 본 폴더는 Phase 2 전용 — 다른 컴퓨터에서 쓰기 금지.

## 빠른 시작

처음 설치하는 컴퓨터라면 먼저 **`SETUP_PHASE2_HOST.md` 의 12 단계 가이드** 를 따라 환경을 구성하세요 (약 30-60 분).

설치 완료된 컴퓨터의 일상 작업:

1. **본인의 컴퓨터가 Phase 2 host 인지 확인** — root `HOSTS.md`
2. **CLAUDE.md 읽기** — 본 폴더 `CLAUDE.md`
3. **Plan 검토** — `plan.md` (12개월 plan, M1-M5)
4. **진입** — `cd phase2_flow_boiling && claude` (root 진입 금지)
5. **종료 시** — `git commit && git push` 로 macmini 와 동기화

## 폴더 구조

```
phase2_flow_boiling/
├── CLAUDE.md            컴퓨터 경고 + Phase 2 컨텍스트
├── README.md            본 파일
├── SETUP_PHASE2_HOST.md Phase 2 host 컴퓨터 첫 설치 가이드 (12 단계)
├── plan.md              Phase 2 plan (이전: root ONB_PINN_Phase2_Flow_Boiling_Plan.md)
├── data/                raw/, processed/, surface_cards/
├── experiments/         checkpoints/, configs/, logs/
├── analysis/            figures/, scripts/, tables/
├── manuscript/          figures/, main.tex (M5)
└── presentations/       slides/, posters/, reports/, outreach/, conference_abstracts/
```

## Phase 2 현재 상태

- **단계**: 계획 (Phase 1.5 완료 후 진입)
- **데이터**: 미수집 (M1 단계에서 외부 corpus 수집 예정)
- **모델**: Phase 1 transfer learning (frozen encoder + new flow head)

## Phase 1 ↔ Phase 2 공유 자산

Stage 2 (Phase 1 IJHMT acceptance 후) 마이그레이션 완료 시:

- `shared/src/pinn_onb/` — network skeleton, surface encoder, 5 classical correlations, CoolProp wrapper
- `phase1_pool_boiling/experiments/checkpoints/` — Phase 1 학습된 weights (frozen 으로 사용)

Stage 1 (현재): Phase 1 코드가 `03_model/src/` 에 있음. Phase 2 시작 시 직접 import 또는 `shared/src/pyproject.toml` 의 shim 사용.

## 관련 문서

| 문서 | 위치 |
|---|---|
| Phase 2 plan | `plan.md` |
| 컴퓨터 매핑 | root `HOSTS.md` |
| 운영 원리 | root `claude-code-multi-project-guide.md` |
| Workspace 구조 | root `CLAUDE.md` |
| Phase 1 결과 | root `01_survey/~05_manuscript/`, `phase1_pool_boiling/` |
| Phase 1.5 진행 | root `phase1p5_inhouse_augmentation/` |
