# 컴퓨터 ↔ Phase 담당 매핑 (Multi-Computer Workspace)

> 본 워크스페이스는 OneDrive 동기화 기반으로 **여러 컴퓨터에서 phase 를 분담**하는 구조입니다.
> 자세한 원리·운영 규칙은 `claude-code-multi-project-guide.md` 참조.

## 현재 매핑 (2026-05-20 기준)

### Phase ↔ 실행 host

| Phase | 담당 컴퓨터 | 호스트명 (예시) | 담당자 | 작업 디렉토리 | 상태 |
|---|---|---|---|---|---|
| **Phase 1** (풀비등 ONB) | `macmini` | `MyHomeMiniui-Macmini.local` | Jaeseon Lee (`myhomemini`) | workspace root + `phase1_pool_boiling/` | ✅ IJHMT 제출 (review 대기) |
| **Phase 1.5** (in-house augmentation) | `macmini` | `MyHomeMiniui-Macmini.local` | Jaeseon Lee (`myhomemini`) | `phase1p5_inhouse_augmentation/` | 진행 중 |
| **Phase 2** (forced-convection flow boiling) | `macbook-air-6` | `MacBook-Air-6.local` | Jaeseon Lee (`mymachome`) | `phase2_flow_boiling/` ONLY | host setup 완료 (2026-05-21), M1 진입 대기 |
| Phase 3+ | TBD | TBD | TBD | TBD | Roadmap |

### Workspace root maintainer

| 역할 | 담당 컴퓨터 | 책임 |
|---|---|---|
| **Root maintainer** | `macmini` (Jaeseon Lee) | 워크스페이스 root 의 모든 변경 — 새 phase 신설, root CLAUDE.md / HOSTS.md / PHASE_STATUS.md 갱신, `.claude/agents/` & `commands/` 추가, `shared/` 공통 모듈, roadmap 통합 결정 |

→ macmini 는 동시에 **두 역할**: Phase 1 + 1.5 실행자 + 전체 워크스페이스 root maintainer.
   Phase 1 + 1.5 완료 후에도 root maintainer 역할은 macmini 가 유지 (이양 시 본 표 갱신).

## 역할 분리 — Setup vs Execution

새 phase 신설·기존 phase 변경 작업은 **항상 root maintainer (macmini)** 가 수행하고,
**실제 연구 실행** 은 해당 phase 담당 host 에서 진행합니다. 이 분리가 OneDrive 충돌 / git divergence / CLAUDE.md 비일관성 방지의 핵심 메커니즘입니다.

| 단계 | 작업 내용 | 필요 권한 | 담당 컴퓨터 |
|---|---|---|---|
| **Setup** | root 파일 다수 동시 수정 (CLAUDE.md, HOSTS.md, phase skeleton 생성, shared/, agents/commands 추가, commit) | **root write** | **macmini** (root maintainer) |
| **Execution** | 지정 phase 폴더 내에서만 실험·분석·작성 | phase folder write | 담당 host (B = Phase 2, C = Phase 3, …) |

### 왜 Setup 은 macmini 에서만?

새 phase 신설 시 단일 commit 으로 묶여야 일관성 유지되는 5-8개 파일 + 폴더 + agents 가 동시 변경됩니다:

| 파일 / 폴더 | 변경 내용 |
|---|---|
| `HOSTS.md` | 새 phase 행 + 새 컴퓨터 행 추가 |
| `CLAUDE.md` (root) | (1) 최상단 host warning 에 새 host 추가, (2) 활성 트랙 표, (3) 다중 컴퓨터 운영 섹션, (4) 폴더 트리, (5) 참조 문서 |
| `phase<N>_*/` 신설 | skeleton (data, experiments, analysis, manuscript, presentations) + `.gitkeep` |
| `phase<N>_*/plan.md` | phase plan |
| `phase<N>_*/README.md` | entry point |
| `phase<N>_*/CLAUDE.md` | 담당 host 경고 헤더 |
| `PHASE_STATUS.md` | 새 phase 진척 섹션 |
| `.claude/agents/` & `commands/` | phase 특화 sub-agents & slash commands (모든 host 공유) |
| `shared/src/pinn_onb/` (Stage 2 후) | 공통 모듈 추가 (필요 시) |
| `future_research_roadmap.md` | roadmap → active 이동 |

이 변경을 phase 담당 host (B/C/…) 에서 시도하면:
- root 파일 동시 편집 → macmini 의 작업과 OneDrive 충돌 위험
- 일부만 수정한 채 commit/push → repo state 불일치 → 나머지 host pull 시 혼란

→ **반드시 macmini 가 일괄 처리 후 commit/push** 해서 다른 host 들은 단순 `git pull` 로 동기화.

### 새 phase launch 표준 워크플로

```bash
# Step 1: macmini 에서 setup
cd ~/Library/CloudStorage/OneDrive-개인/Projects/PINN-ONB01
claude
# → Claude 에 지시: "Phase 3 launch — 주제: <X>, 담당 host: C (<hostname/username>)"
# → Claude 가 위 표의 모든 파일·폴더 일괄 생성/수정
# → 검토 후 git commit + push

# Step 2: phase 담당 host (예: C) 에서 sync
git pull
cd phase3_<topic>
claude
# → phase3_<topic>/CLAUDE.md 의 host 경고 + plan.md 자동 로드
# → 실제 연구 작업 시작 (해당 폴더 안에서만)
```

### Root maintainer 이양 (향후 시나리오)

macmini 가 은퇴 / 사용자 변경 / 역할 재배정될 때:

1. 새 root maintainer 컴퓨터 (예: D) 합의·지정
2. 본 파일의 "Workspace root maintainer" 표 갱신
3. root `CLAUDE.md` 최상단 host warning 의 macmini → D
4. 모든 phase `CLAUDE.md` 의 host warning 검토 (macmini 가 실행자로 명시된 phase 가 있다면 이양 절차 동반)
5. 새 root maintainer 가 첫 commit 으로 위 변경 일괄 push

현재는 미발생 시나리오 — 대비 차원의 절차만 기록.

## 운영 규칙

### Rule 1 — phase 폴더 isolation

| 컴퓨터 | 허용되는 작업 디렉토리 |
|---|---|
| **macmini** | workspace root, `01_survey/~05_manuscript/`, `phase1_pool_boiling/`, `phase1p5_inhouse_augmentation/`, `shared/`, `presentations/` |
| **macbook-air-6** (`MacBook-Air-6.local`, `mymachome`) — Phase 2 host | `phase2_flow_boiling/` **만** (root, 다른 phase 폴더 진입 금지) |

각 컴퓨터는 본 표의 **허용 디렉토리 안에서만 쓰기**해야 OneDrive 충돌을 회피합니다.
다른 phase 폴더는 OneDrive 동기화로 보이지만 **참조 전용 (read-only)** 으로 취급합니다.

### Rule 2 — Claude Code 실행 위치

각 컴퓨터의 Claude Code 호출 시 `cd` 경로 :

```bash
# macmini (Phase 1 또는 1.5)
cd ~/Library/CloudStorage/OneDrive-개인/Projects/PINN-ONB01
claude   # Phase 1 작업 (root 컨텍스트)

# 또는
cd ~/Library/CloudStorage/OneDrive-개인/Projects/PINN-ONB01/phase1p5_inhouse_augmentation
claude   # Phase 1.5 격리 컨텍스트
```

```bash
# macbook-air-6 (Phase 2 host) — 반드시 phase2 폴더에서 진입
cd ~/PINN-ONB01/phase2_flow_boiling   # symlink → /Users/mymachome/Library/CloudStorage/OneDrive-개인/Projects/PINN-ONB01
claude   # Phase 2 격리 컨텍스트 (root 안 들어감)
```

### Rule 3 — 충돌 방지

`claude-code-multi-project-guide.md` § 9 의 충돌 시나리오 참고. 핵심:

- 한 phase 폴더는 동시에 **한 컴퓨터만** 쓰기 (OneDrive 충돌 파일 자동 생성 방지)
- 세션 종료 후 commit (다른 컴퓨터가 동기화로 받기 전 안정 상태로 두기)
- 의도치 않은 컴퓨터에서 phase 폴더 열었을 경우 각 phase 의 `CLAUDE.md` 가 **즉시 경고**

### Rule 4 — `shared/` 폴더 변경

`shared/src/pinn_onb/` 등 공유 모듈을 변경할 때는:

- 단순 변경: macmini 에서 수행, commit + push, 다른 컴퓨터에서 pull
- 양쪽 동시 변경 필요 시: PR + branch 분리

### Rule 5 — Phase 2 시작 시 추가 단계

Phase 2 host 의 첫 설치 절차는 **`phase2_flow_boiling/SETUP_PHASE2_HOST.md`** 의 12 단계 가이드 참조. 요약:

1. 사용자가 Phase 2 컴퓨터 hostname / username 확정 (사용자가 macmini 에 통보)
2. **macmini (root maintainer)** 가 본 파일 갱신 (TBD → 실제 값) + `phase2_flow_boiling/CLAUDE.md` 헤더 갱신 + commit/push
3. Phase 2 host 에서 OneDrive 동기화 + git pull
4. Phase 2 host: Claude Code 설치 + Anthropic auth + Git auth (SSH 키 또는 PAT)
5. Phase 2 host: `cd phase2_flow_boiling && claude` (first time — `--resume` 금지)
6. 이후 모든 Phase 2 작업은 해당 폴더 안에서만 (root 진입 금지) + 매일 `git commit && git push` 로 macmini 와 동기화

### Rule 6 — 새 Phase (3+) 신설 시 절차

위 "역할 분리 — Setup vs Execution" 섹션의 **새 phase launch 표준 워크플로** 참조.
요약: **macmini 가 root 에서 일괄 setup → commit/push → 담당 host 가 pull → 해당 폴더에서 execution 시작**.

## 갱신 history

| 일자 | 변경 |
|---|---|
| 2026-05-20 | 본 파일 작성. Phase 2 host TBD 상태. Phase 2 폴더 skeleton 신설 |
| 2026-05-20 | Setup vs Execution 역할 분리 섹션 추가. macmini 의 root maintainer 역할 명시. Phase 3+ 신설 절차 (Rule 6) 추가. |
| 2026-05-20 | `phase2_flow_boiling/SETUP_PHASE2_HOST.md` (12 단계 host 설치 가이드) 작성 + Rule 5 에서 참조 |
| 2026-05-21 | Phase 2 host 확정: `macbook-air-6` (`MacBook-Air-6.local`, `mymachome`, Jaeseon Lee). SETUP_PHASE2_HOST.md § 4 따라 본 파일 + `phase2_flow_boiling/CLAUDE.md` + root `CLAUDE.md` 일괄 갱신. B 측은 OneDrive 한글경로 우회 위해 `ln -s "/Users/mymachome/Library/CloudStorage/OneDrive-개인/Projects/PINN-ONB01" ~/PINN-ONB01` symlink 설치 완료 |

## 관련 문서

- 다중 프로젝트 운영 원리: `claude-code-multi-project-guide.md`
- 워크스페이스 구조 결정 배경: `WORKSPACE_RESTRUCTURE_PROPOSAL.md`
- 진척 현황: `PHASE_STATUS.md`
