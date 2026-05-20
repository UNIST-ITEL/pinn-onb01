# 컴퓨터 ↔ Phase 담당 매핑 (Multi-Computer Workspace)

> 본 워크스페이스는 OneDrive 동기화 기반으로 **여러 컴퓨터에서 phase 를 분담**하는 구조입니다.
> 자세한 원리·운영 규칙은 `claude-code-multi-project-guide.md` 참조.

## 현재 매핑 (2026-05-20 기준)

| Phase | 담당 컴퓨터 | 호스트명 (예시) | 담당자 | 작업 디렉토리 | 상태 |
|---|---|---|---|---|---|
| **Phase 1** (풀비등 ONB) | `macmini` | `MyHomeMiniui-Macmini.local` | Jaeseon Lee (`myhomemini`) | workspace root + `phase1_pool_boiling/` | ✅ IJHMT 제출 (review 대기) |
| **Phase 1.5** (in-house augmentation) | `macmini` | `MyHomeMiniui-Macmini.local` | Jaeseon Lee (`myhomemini`) | `phase1p5_inhouse_augmentation/` | 진행 중 |
| **Phase 2** (forced-convection flow boiling) | **TBD — 별도 컴퓨터** | TBD (사용자 채움) | TBD | `phase2_flow_boiling/` ONLY | 계획 단계 |
| Phase 3+ | TBD | TBD | TBD | TBD | Roadmap |

## 운영 규칙

### Rule 1 — phase 폴더 isolation

| 컴퓨터 | 허용되는 작업 디렉토리 |
|---|---|
| **macmini** | workspace root, `01_survey/~05_manuscript/`, `phase1_pool_boiling/`, `phase1p5_inhouse_augmentation/`, `shared/`, `presentations/` |
| **Phase 2 컴퓨터** | `phase2_flow_boiling/` **만** (root, 다른 phase 폴더 진입 금지) |

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
# Phase 2 컴퓨터 — 반드시 phase2 폴더에서 진입
cd <OneDrive-경로>/PINN-ONB01/phase2_flow_boiling
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

1. 사용자가 Phase 2 컴퓨터 hostname / username 확정
2. 본 파일 갱신 (TBD → 실제 값)
3. `phase2_flow_boiling/CLAUDE.md` 의 담당 컴퓨터 헤더 갱신
4. 해당 컴퓨터에서 OneDrive 동기화 확인 후 `cd phase2_flow_boiling && claude`
5. Git auth (SSH 키 또는 PAT) Phase 2 컴퓨터에 설치

## 갱신 history

| 일자 | 변경 |
|---|---|
| 2026-05-20 | 본 파일 작성. Phase 2 host TBD 상태. Phase 2 폴더 skeleton 신설 |

## 관련 문서

- 다중 프로젝트 운영 원리: `claude-code-multi-project-guide.md`
- 워크스페이스 구조 결정 배경: `WORKSPACE_RESTRUCTURE_PROPOSAL.md`
- 진척 현황: `PHASE_STATUS.md`
