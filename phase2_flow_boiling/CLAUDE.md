# Phase 2 — Forced-Convection Subcooled Flow Boiling ONB

> ⚠️ **담당 컴퓨터 확인 — Phase 2**
>
> 본 phase 는 **별도 컴퓨터 (TBD — Phase 2 host)** 전용입니다.
> **`macmini` (Phase 1 / 1.5 host)** 에서는 본 폴더의 파일을 **쓰지 마세요** (read-only 참조만 허용).
>
> 다른 컴퓨터에서 (예: macmini, Phase 2 가 아닌 host) 본 폴더를 열었다면 즉시 Claude Code 를 종료하세요.
> Phase 2 작업 시작 시 root `HOSTS.md` 에서 본인의 hostname / username 을 확인 후 채워주세요.
>
> 운영 원리: root `claude-code-multi-project-guide.md` 참조.

## Phase 2 상태 (2026-05-20)

- **단계**: 계획 (Future, Phase 1.5 완료 후 진입)
- **목표**: Subcooled flow boiling ONB — Re, x, ΔT_sub, mass flux 등 추가 변수
- **전략**: Phase 1 모델에서 **transfer learning** (frozen encoder + new flow head)
- **데이터**: 외부 corpus (Bergles, Sato, Bowring, Frost-Dzakowic 등) + 가능 시 lab forced-convection

## 본 폴더 구조 (skeleton)

```
phase2_flow_boiling/
├── CLAUDE.md            ← 본 파일 (Phase 2 컴퓨터 경고)
├── README.md            ← Phase 2 entry point
├── plan.md              ← Phase 2 12개월 plan (이전: root ONB_PINN_Phase2_Flow_Boiling_Plan.md)
├── data/
│   ├── raw/             ← 문헌 + (선택) lab forced-convection
│   ├── processed/
│   └── surface_cards/   ← Phase 2 표면 카드 (Phase 1.5 와 별도 또는 공유)
├── experiments/
│   ├── checkpoints/
│   ├── configs/
│   └── logs/            ← MLflow runs
├── analysis/
│   ├── figures/
│   ├── scripts/
│   └── tables/
├── manuscript/
│   └── figures/         ← Phase 2 paper EPS/PDF
└── presentations/       ← slides, posters, reports, outreach, conference_abstracts
```

## Phase 2 시작 단계 (체크리스트)

Phase 2 host 컴퓨터의 첫 설치는 **`SETUP_PHASE2_HOST.md`** (본 폴더, 12 단계) 참조. 본 phase 작업 시작 시:

- [ ] **Step 1** — 담당자/hostname 확정 후 본 파일 § 컴퓨터 경고 헤더 + root `HOSTS.md` 갱신 (`SETUP_PHASE2_HOST.md` § 4)
- [ ] **Step 2** — 해당 컴퓨터에 OneDrive sync 확인 + Claude Code 설치 + Git 인증 (`SETUP_PHASE2_HOST.md` § 1-3)
- [ ] **Step 3** — `cd phase2_flow_boiling && claude` 진입 (root 진입 금지) (`SETUP_PHASE2_HOST.md` § 6)
- [ ] **Step 4** — `plan.md` 의 M1 (서베이) 실행
- [ ] **Step 5** — `shared/src/pinn_onb/` 의 Phase 1 모델 import 확인 (Stage 2 후) — 의존성 import path 검증

## Phase 1 ↔ Phase 2 공유

| 항목 | 공유 방식 |
|---|---|
| Network skeleton (FiLM, ensemble) | `shared/src/pinn_onb/` (Stage 2 후) |
| Surface descriptor encoder | 동일 모듈 사용 |
| 5 classical correlations | `shared/src/pinn_onb/correlations.py` |
| CoolProp wrapper | `shared/src/pinn_onb/properties.py` |
| Phase 1 학습된 weights | `phase1_pool_boiling/experiments/checkpoints/` (frozen) |
| Loss functions | Phase 2 는 추가 항목 (convection, subcooling) — 본 phase 내 구현 |

## 관련 slash commands

Phase 2 시작 시 추가 예정:

- `/start-phase2` (TBD) — Phase 2 환경 점검
- `/transfer-phase1-to-phase2` (TBD) — frozen encoder 이식

기존 phase-agnostic commands 사용 가능: `/add-paper`, `/build-seminar-prompt --phase 2`

## 참고

- Phase 2 plan (12개월): `plan.md`
- 향후 후속 주제 30 건: root `future_research_roadmap.md`
- 컴퓨터 매핑: root `HOSTS.md`
- 운영 원리: root `claude-code-multi-project-guide.md`
