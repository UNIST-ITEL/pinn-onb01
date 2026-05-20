# Phase 2 Host — 컴퓨터 B 설치 가이드

> 본 문서는 **Phase 2 (forced-convection flow boiling) 담당 컴퓨터 (이하 B)** 의
> 초기 설치 절차입니다. macmini (Phase 1 + 1.5 host, root maintainer) 와 OneDrive 로
> 동기화되며, Phase 2 폴더 격리 작업을 수행하기 위한 환경을 구축합니다.

작성일: 2026-05-20
대상: Phase 2 host 사용자 (Jaeseon Lee 또는 협업자)
완료 소요: 약 30-60 분 (네트워크 속도에 따라 OneDrive 첫 sync 가 가장 길어짐)

---

## 0. 사전 체크리스트

설치 시작 전 다음을 확인하세요:

- [ ] **OS**: macOS, Linux, 또는 Windows (모두 지원)
- [ ] **인터넷 연결**: OneDrive sync + Anthropic auth + GitHub access
- [ ] **OneDrive 계정**: macmini 와 **동일 계정** (UNIST 또는 개인). 다른 계정이면 PINN-ONB01 폴더 sync 불가
- [ ] **GitHub 계정**: `UNIST-ITEL/pinn-onb01` 또는 본인 fork 에 push/pull 권한
- [ ] **Anthropic 계정**: Claude Code 사용 가능 (이미 Claude Pro/Team 가입자라면 동일 계정)
- [ ] (Phase 2 학습 단계 진입 시) **Python 3.10+ 설치 가능 환경**, 가급적 NVIDIA GPU + CUDA

체크 안 된 항목이 있으면 먼저 해결 후 본 가이드 진행.

---

## 1. OneDrive 동기화 확인

### 1.1 OneDrive 클라이언트 설치 + 로그인

| OS | 설치 / 로그인 |
|---|---|
| **macOS** | App Store 에서 "Microsoft OneDrive" 설치 → 실행 → macmini 와 동일 계정 로그인 |
| **Windows** | `winget install Microsoft.OneDrive` 또는 OneDrive 공식 페이지에서 다운로드 → 동일 계정 로그인 |
| **Linux** | `abraunegg/onedrive` (https://abraunegg.github.io/) 등 third-party 클라이언트 사용. 본 가이드는 macOS/Windows 기본 클라이언트 가정 |

### 1.2 PINN-ONB01 폴더 동기화 확인

OneDrive 가 로그인되면 자동으로 모든 폴더가 sync 됩니다. 다음 경로가 보이면 성공:

| OS | 경로 |
|---|---|
| macOS | `~/Library/CloudStorage/OneDrive-개인/Projects/PINN-ONB01/` (또는 계정명에 따라 `OneDrive-UNIST` 등) |
| Windows | `%USERPROFILE%\OneDrive\Projects\PINN-ONB01\` |
| Linux | OneDrive 클라이언트의 sync 경로 |

```bash
# 경로 확인 (macOS/Linux)
ls "<OneDrive-경로>/PINN-ONB01/phase2_flow_boiling/"
# CLAUDE.md, README.md, plan.md, data/, experiments/, ... 가 보여야 함

# Windows PowerShell
ls "$env:USERPROFILE\OneDrive\Projects\PINN-ONB01\phase2_flow_boiling\"
```

### 1.3 selective sync (선택, 권장)

OneDrive 의 "Choose folders" 기능으로 **PINN-ONB01 전체** 또는 최소 **phase2_flow_boiling/ + shared/ + root 의 .md 파일들** 만 sync 가능. 디스크 용량 절약 시 선택적 sync 사용.

⚠️ **주의**: `phase1_pool_boiling/` 와 `phase1p5_inhouse_augmentation/` 데이터 디렉토리는 macmini 의 작업 영역이므로 sync 불필요. 단 root `CLAUDE.md`, `HOSTS.md` 등은 반드시 sync 필요 (Claude Code 가 CLAUDE.md 계층 상속 시 root 까지 walk-up).

---

## 2. Claude Code CLI 설치

### 2.1 설치

| OS | 명령 |
|---|---|
| macOS (Homebrew) | `brew install --cask claude-code` 또는 공식 installer |
| macOS / Linux (curl) | `curl -fsSL https://claude.ai/install.sh \| bash` |
| Windows | 공식 페이지 (https://claude.com/claude-code) 의 Windows installer |

### 2.2 설치 확인

```bash
claude --version
# 출력 예: claude version 1.x.x
```

### 2.3 Anthropic 계정 로그인

```bash
claude
# 첫 실행 시 브라우저 OAuth flow 자동 시작
# Claude Pro/Team/API 계정으로 로그인
```

로그인 완료 후 `~/.claude/` 폴더가 생성됩니다.

---

## 3. Git 설정 + repo 인증

### 3.1 Git 설치 확인

```bash
git --version
# 없으면: macOS는 `xcode-select --install`, Windows는 https://git-scm.com/
```

### 3.2 사용자 정보 설정 (전역)

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

### 3.3 GitHub 인증 — SSH 키 (권장)

```bash
# SSH 키 생성 (이미 있으면 건너뜀)
ssh-keygen -t ed25519 -C "your-email@example.com"

# 공개키를 GitHub Settings → SSH and GPG keys 에 등록
cat ~/.ssh/id_ed25519.pub
# (출력 복사 → GitHub 웹에서 "New SSH key" → paste)

# 연결 테스트
ssh -T git@github.com
# "Hi <username>! You've successfully authenticated" 보이면 성공
```

또는 PAT (Personal Access Token):
- GitHub Settings → Developer settings → Personal access tokens → Fine-grained → `UNIST-ITEL/pinn-onb01` repo 에 `Contents: Read/Write`, `Pull requests: Read/Write` 권한
- `git clone https://...` 시 password 자리에 PAT 입력

### 3.4 repo 인증 확인

```bash
cd <OneDrive-경로>/PINN-ONB01
git fetch origin
# 에러 없이 fetch 되면 성공
git pull
# 최신 상태로 동기화 (이미 OneDrive 로 받았더라도 git history 가져옴)
```

⚠️ **OneDrive 와 git 의 관계**: OneDrive 는 파일을 sync 하지만 git history (`.git/`) 는 작은 binary 들이라 sync 가 느릴 수 있음. `git pull` 로 명시적으로 git state 를 최신화.

---

## 4. Hostname / username 확인 → macmini 에 통보

이 단계는 **B 의 정체성을 워크스페이스 문서에 박는 단계** 입니다.

### 4.1 본인 컴퓨터 정보 수집

```bash
# macOS / Linux
hostname           # 예: dell-workstation.local
whoami             # 예: jslee
scutil --get LocalHostName  # macOS only
```

```powershell
# Windows PowerShell
hostname            # 예: DESKTOP-ABC123
whoami              # 예: DESKTOP-ABC123\jslee
```

### 4.2 macmini 에 4 가지 정보 통보

다음을 macmini 사용자 (Jaeseon Lee, `leejs92@gmail.com`) 에게 전달:

| 항목 | 예시 |
|---|---|
| Hostname | `dell-workstation.local` 또는 `DESKTOP-ABC123` |
| Username | `jslee` |
| 담당자 이름 | "Jaeseon Lee (Phase 2 host 겸 root maintainer 보조)" 등 |
| OneDrive 경로 (B 측) | `/home/jslee/OneDrive/Projects/PINN-ONB01` 등 |

### 4.3 macmini 가 수행할 갱신 (B 는 대기)

macmini 가 다음 파일 갱신 + commit + push:

| 파일 | 갱신 내용 |
|---|---|
| `HOSTS.md` | "Phase 2 host" 행의 TBD → 실제 hostname/username/담당자 |
| `phase2_flow_boiling/CLAUDE.md` | 최상단 host warning 의 TBD → B 의 정체성 |
| `CLAUDE.md` (root) | 활성 트랙 표 + 다중 컴퓨터 운영 표 갱신 |
| (필요 시) | `.gitignore` — B 의 OS 별 파일 (`.DS_Store`, `Thumbs.db` 등) |

### 4.4 B 측 동기화

```bash
cd <OneDrive-경로>/PINN-ONB01
git pull
# macmini 의 갱신 받음
# phase2_flow_boiling/CLAUDE.md 의 host 경고가 B 의 정체성을 명시한 상태가 됨
```

---

## 5. Python 환경 (선택 — 학습 시점에)

Phase 2 의 M2-M3 (데이터 수집 / 전처리) 단계까지는 Python 환경이 필수가 아닙니다. M4 (학습) 진입 직전에 설정해도 됩니다.

### 5.1 Conda / mamba 설치

```bash
# Miniforge3 (mamba 포함, 권장)
# macOS / Linux
curl -L https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh -o miniforge.sh
bash miniforge.sh

# Windows: https://github.com/conda-forge/miniforge/releases
```

### 5.2 환경 생성

```bash
cd <OneDrive-경로>/PINN-ONB01
mamba env create -f environment.yml
mamba activate pinn-onb
# 또는 pip
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 5.3 GPU 확인 (선택)

```python
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.device_count())"
```

`True` 출력 시 GPU 학습 가능. `False` 라도 CPU 로 작업 시작은 가능 (학습 속도만 느림).

---

## 6. 첫 Claude Code 실행

### 6.1 정확한 경로로 진입

```bash
cd <OneDrive-경로>/PINN-ONB01/phase2_flow_boiling
pwd
# 출력 끝이 .../phase2_flow_boiling 임을 반드시 확인
```

🚫 **`cd PINN-ONB01 && claude` 절대 금지** — root 진입 시 root CLAUDE.md 의 prominent warning 이 B 를 거부합니다.

### 6.2 첫 실행 (`--resume` 아님)

```bash
claude
```

`claude --resume` 은 **B 의 로컬 과거 세션** 을 picker 로 띄우는데, 첫 진입에는 그 폴더가 비어 있어서 작동하지 않습니다. **반드시 첫 호출은 `claude`** (no flag).

### 6.3 Claude 의 자동 로드 확인

세션 시작 시 Claude 가 다음 CLAUDE.md 들을 자동 병합:

```
~/.claude/CLAUDE.md                    (B 의 전역 — 비어있을 수 있음)
+ PINN-ONB01/CLAUDE.md                  (root — Phase 2 host 가 root 진입 금지 경고)
+ PINN-ONB01/phase2_flow_boiling/CLAUDE.md  (phase — B 의 정체성 명시)
```

Claude 에게 다음 prompt 로 환경 점검 권장:

```
/memory
```

→ 로드된 CLAUDE.md 목록과 핵심 내용 표시. host 경고 표시가 B 의 hostname 과 일치하는지 확인.

### 6.4 첫 작업

Phase 2 plan 의 M1 (서베이) 부터 시작:

```
Read phase2_flow_boiling/plan.md
```

Claude 가 plan.md 를 읽고 M1 단계의 구체적 액션 (서베이 키워드, 후보 paper, 데이터 수집 시작 등) 을 제안합니다.

### 6.5 이후 호출

| 명령 | 용도 |
|---|---|
| `claude` | 새 세션 시작 |
| `claude --resume` | 같은 phase2 폴더의 과거 B 세션 picker |
| `claude` 안에서 `/resume` | session picker (동일) |
| `claude` 안에서 `/exit` | 종료 |

---

## 7. 작업 종료 시 절차

매 작업 종료 시 (또는 하루 끝):

```bash
# Claude Code 안에서 또는 별도 터미널에서:
git status                         # 변경 사항 확인
git add <변경 파일>
git commit -m "Phase 2: <작업 요약>"
git push                           # macmini 가 받을 수 있도록

# 그리고 Claude Code 종료
/exit
```

⚠️ **commit 없이 종료하면 다음 날 macmini 의 OneDrive 동기화로 인한 충돌 위험 증가**. 매일 commit/push 가 안전합니다.

OneDrive 가 따로 sync 하더라도 git 으로 명시적 push 가 신뢰할 수 있는 동기화 채널입니다 (가이드 § 9 참조).

---

## 8. 트러블슈팅

### 8.1 OneDrive 충돌 파일 발생

```
phase2_flow_boiling/main.py
phase2_flow_boiling/main (다른 컴퓨터에서 충돌 복사본).py    ← OneDrive 자동 생성
```

대처:
1. 즉시 Claude Code 종료 (양쪽 컴퓨터)
2. 두 버전을 `diff` 로 비교
3. 올바른 버전 보존, 충돌본 삭제
4. 양쪽에서 `git pull` 동기화
5. **B 가 root 진입했는지 확인** — 다시 발생 안 하도록 phase2_flow_boiling/ 안에서만 작업

### 8.2 `claude` 명령이 root 진입을 거부

```
🚫 Phase 2 담당 컴퓨터는 본 root 에서 작업하지 마세요.
```

→ 정상 동작. `cd phase2_flow_boiling` 으로 이동 후 재실행.

### 8.3 Git push 거부 (non-fast-forward)

```
! [rejected]   main -> main (non-fast-forward)
```

대처:
```bash
git pull --rebase    # macmini 의 변경을 먼저 받고 본인 commit 위에 rebase
# 또는 merge
git pull
# conflict 가 있으면 해결 후
git commit
git push
```

### 8.4 Anthropic auth 만료

```
Error: authentication required
```

```bash
claude logout
claude login
```

### 8.5 Python `ModuleNotFoundError: pinn_onb`

```bash
# shared 가 editable install 되어야 함 (Stage 2 후)
pip install -e shared/src/
# 또는 PYTHONPATH 직접 추가
export PYTHONPATH="<OneDrive-경로>/PINN-ONB01/03_model/src:$PYTHONPATH"
```

### 8.6 CLAUDE.md 가 로드 안 됨 (host 경고 안 보임)

```bash
# 세션 안에서:
/memory
```

→ 로드된 파일 목록 확인. `phase2_flow_boiling/CLAUDE.md` 가 빠져 있으면:
- `pwd` 로 cwd 가 phase2_flow_boiling 인지 확인
- `git pull` 로 파일이 동기화됐는지 확인
- 같은 경로 다시 `claude`

---

## 9. FAQ

### Q1. macmini 가 진행한 Phase 2 plan 작성 대화를 B 에서 볼 수 있나?

A. **불가**. Claude Code 세션 이력은 컴퓨터 로컬에 저장되며 OneDrive sync 대상이 아님 (가이드 § 8). macmini 의 사고 과정 중 B 에 필요한 내용은 `plan.md` 또는 phase2_flow_boiling 의 다른 markdown 파일에 명시적으로 기록되어 있어야 함.

### Q2. B 에서 root 의 다른 파일을 읽고 싶을 때 (예: Phase 1 결과)

A. **읽기는 허용**. `Read 01_survey/paper_database.md` 같은 명령은 Claude 안에서 가능. 단, **편집 / 쓰기는 금지** (root CLAUDE.md 의 host warning 으로 Claude 가 거부할 것).

### Q3. macmini 가 휴가 중인데 macmini 만 할 수 있는 root 작업이 필요하다

A. **임시 root maintainer 이양 절차** 가능 (HOSTS.md "Root maintainer 이양" 참조). 단순 임시 작업이면 macmini 가 사전에 PR 권한 위임 후 B 가 별도 branch 에서 작업 → macmini 가 복귀 시 merge. 추천하지 않음. 가능한 macmini 복귀 대기.

### Q4. 다른 컴퓨터를 추가해서 Phase 3 시작하려면?

A. HOSTS.md 의 "새 phase launch 표준 워크플로" 참조. 요약: **macmini 가 root setup → 새 phase host 가 본 가이드와 유사한 자기 setup 진행**. 본 가이드 (`SETUP_PHASE2_HOST.md`) 를 템플릿 삼아 `SETUP_PHASE3_HOST.md` 작성 권장.

### Q5. B 의 컴퓨터가 바뀌면?

A. 위 6 의 step 4 (정체성 통보) 부터 재실행. macmini 가 HOSTS.md + phase2_flow_boiling/CLAUDE.md 갱신, B 는 신컴퓨터에서 본 가이드 1-6 재진행.

### Q6. macOS 와 Windows 의 OneDrive 경로가 다른데 git 이 헷갈리지 않나?

A. Git 은 OS 와 무관 — `.git/` 내부 history 가 동일하면 어디서든 push/pull 가능. CLAUDE.md 의 host warning 도 hostname 으로 분기하므로 OS 와 무관.

⚠️ 단, **OneDrive 의 인코딩 경로** (Claude Code 세션 폴더명) 는 OS/username 별로 다름. 따라서 B 의 세션 이력이 macmini 로 자동 동기화되지는 않음 (그래야 정상).

---

## 10. 체크리스트 요약

본 가이드를 따라 진행한 결과:

- [ ] OneDrive sync — `phase2_flow_boiling/` 폴더 visible
- [ ] Claude Code CLI — `claude --version` 작동
- [ ] Anthropic 로그인 — 첫 `claude` 실행 시 prompt 진입 가능
- [ ] Git 인증 — `git fetch origin` 에러 없음
- [ ] Hostname / username — macmini 에 통보됨, HOSTS.md 갱신 완료, B 가 git pull 받음
- [ ] (선택) Python 환경 — `mamba env create -f environment.yml` 완료
- [ ] 첫 `claude` 실행 — `phase2_flow_boiling/` 안에서 진입, /memory 로 CLAUDE.md 로드 확인
- [ ] phase2_flow_boiling/CLAUDE.md 의 host warning 이 본인 hostname 명시 확인

위 8개 모두 ✅ 면 Phase 2 작업 시작 준비 완료.

---

## 11. 관련 문서

| 문서 | 위치 | 용도 |
|---|---|---|
| 다중 프로젝트 운영 원리 | root `claude-code-multi-project-guide.md` | Claude Code CLI 의 세션 / 동기화 메커니즘 전반 |
| 컴퓨터 ↔ phase 매핑 | root `HOSTS.md` | 본 워크스페이스의 host 배정 + 운영 규칙 |
| Phase 2 plan | `plan.md` (본 폴더) | Phase 2 12개월 계획 (M1-M5) |
| Phase 2 CLAUDE.md | `CLAUDE.md` (본 폴더) | Claude 가 자동 로드하는 phase 컨텍스트 + host 경고 |
| Workspace 메인 가이드 | root `CLAUDE.md` | 워크스페이스 전체 구조 + 코딩 규칙 |
| Workspace 구조 결정 배경 | root `WORKSPACE_RESTRUCTURE_PROPOSAL.md` | Stage 1-3 마이그레이션 의사결정 기록 |

## 12. 문의

- **Maintainer**: Jaeseon Lee (`leejs92@gmail.com`, ORCID 0000-0003-1996-6086)
- 본 가이드 개선 제안: Phase 2 host 가 PR 또는 macmini 에 직접 통보
- 긴급 (OneDrive 충돌 등): 즉시 양쪽 컴퓨터의 Claude Code 종료 후 macmini 사용자에게 통보
