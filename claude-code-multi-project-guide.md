# Claude Code CLI — 다층 프로젝트 · 다중 컴퓨터 구성 참조 가이드

> 작성 기준: Claude Code CLI (2026년 5월 기준)  
> 대상: OneDrive 등 공유 스토리지를 활용해 여러 컴퓨터에서 하위 프로젝트를 분담 진행하는 팀

---

## 목차

1. [핵심 개념: 세션 이력의 저장 위치](#1-핵심-개념-세션-이력의-저장-위치)
2. [다중 컴퓨터 동기화 현황](#2-다중-컴퓨터-동기화-현황)
3. [권장 폴더 구조](#3-권장-폴더-구조)
4. [CLAUDE.md 계층 상속 원리](#4-claudemd-계층-상속-원리)
5. [CLAUDE.md 작성 가이드](#5-claudemd-작성-가이드)
6. [각 컴퓨터의 실행 방법](#6-각-컴퓨터의-실행-방법)
7. [OS별 절대 경로 확인 방법](#7-os별-절대-경로-확인-방법)
8. [세션 이력 공유 가능 조건](#8-세션-이력-공유-가능-조건)
9. [실수 시나리오와 위험 분석](#9-실수-시나리오와-위험-분석)
10. [실수 예방 체크리스트](#10-실수-예방-체크리스트)
11. [동기화 항목 요약표](#11-동기화-항목-요약표)
12. [고급 설정: CLAUDE_CONFIG_DIR](#12-고급-설정-claude_config_dir)

---

## 1. 핵심 개념: 세션 이력의 저장 위치

Claude Code CLI는 대화 세션 이력을 **프로젝트 폴더 안이 아닌** 각 컴퓨터의 로컬 홈 디렉토리에 저장합니다.

```
~/.claude/
├── projects/
│   └── [인코딩된-경로명]/         ← 절대 경로를 '-'로 인코딩한 폴더명
│       ├── session-abc123.jsonl   ← 대화 이력 (로컬 전용)
│       └── session-def456.jsonl
├── settings.json                  ← 개인 설정 (로컬 전용)
├── CLAUDE.md                      ← 전역 지시문 (로컬 전용)
└── history.jsonl                  ← 명령 히스토리 (로컬 전용)
```

### 경로 인코딩 규칙

Claude Code는 프로젝트 폴더의 **절대 경로**를 그대로 인코딩해서 세션 저장 폴더명을 결정합니다.

| 절대 경로 | 인코딩 결과 |
|-----------|-------------|
| `/Users/me/OneDrive/root-project/project-a` | `-Users-me-OneDrive-root-project-project-a` |
| `C:\Users\me\OneDrive\root-project\project-a` | `C--Users-me-OneDrive-root-project-project-a` |

> **중요**: `/`(Mac/Linux)와 `\`(Windows), 드라이브 문자(`C:`) 등이 모두 다르게 인코딩되므로, Mac ↔ Windows 사이에는 경로가 절대 일치하지 않습니다.

---

## 2. 다중 컴퓨터 동기화 현황

Claude Code CLI는 현재 **공식 자동 동기화 기능을 제공하지 않습니다.**

| 항목 | OneDrive 공유 | 동기화 여부 |
|------|:---:|:---:|
| 소스 코드, 프로젝트 파일 | ✅ | ✅ 자동 |
| 루트 `CLAUDE.md` (공통 지시문) | ✅ | ✅ 자동 |
| 각 서브 프로젝트 `CLAUDE.md` | ✅ | ✅ 자동 |
| `.mcp.json` (MCP 서버 설정) | ✅ | ✅ 자동 |
| **세션 대화 이력** | ❌ | ❌ 각 컴퓨터 로컬 |
| `~/.claude/settings.json` | ❌ | ❌ 각 컴퓨터 로컬 |
| `~/.claude/CLAUDE.md` (전역) | ❌ | ❌ 각 컴퓨터 로컬 |

**결론**: 코드와 `CLAUDE.md` 지시문은 공유되지만, 세션 이력은 공유되지 않습니다.

---

## 3. 권장 폴더 구조

```
OneDrive/root-project/              ← 공유 스토리지 (전체 동기화됨)
│
├── CLAUDE.md                       ← 공통 지시문 (모든 하위 프로젝트에 자동 상속)
│
├── project-a/
│   ├── CLAUDE.md                   ← a 전용 지시문
│   ├── .mcp.json                   ← a 전용 MCP 설정 (필요 시)
│   └── (소스 코드 ...)
│
├── project-b/
│   ├── CLAUDE.md                   ← b 전용 지시문
│   ├── .mcp.json                   ← b 전용 MCP 설정 (필요 시)
│   └── (소스 코드 ...)
│
└── project-c/
    ├── CLAUDE.md                   ← c 전용 지시문
    ├── .mcp.json                   ← c 전용 MCP 설정 (필요 시)
    └── (소스 코드 ...)
```

각 컴퓨터 로컬 (공유 안 됨):

```
컴퓨터 A — ~/.claude/projects/
└── ...-root-project-project-a/    ← project-a 세션 이력만 쌓임

컴퓨터 B — ~/.claude/projects/
└── ...-root-project-project-b/    ← project-b 세션 이력만 쌓임

컴퓨터 C — ~/.claude/projects/
└── ...-root-project-project-c/    ← project-c 세션 이력만 쌓임
```

---

## 4. CLAUDE.md 계층 상속 원리

Claude Code는 현재 작업 디렉토리부터 파일시스템 루트까지 **모든 상위 경로의 CLAUDE.md를 자동으로 읽어 병합**합니다.

### 로드 순서 (컴퓨터 A에서 project-a를 열었을 때)

```
1. ~/.claude/CLAUDE.md               ← 전역 (개인 설정, 로컬 전용)
2. ~/OneDrive/root-project/CLAUDE.md ← 공통 (팀 전체 공유)
3. ~/OneDrive/root-project/project-a/CLAUDE.md  ← a 전용
```

아래로 내려올수록 더 구체적인 지시문이 우선 적용됩니다.

### 형제 프로젝트 간 격리

```
컴퓨터 A에서 project-a를 열었을 때:
  ✅ root-project/CLAUDE.md     → 로드됨 (부모)
  ✅ project-a/CLAUDE.md        → 로드됨 (현재)
  ❌ project-b/CLAUDE.md        → 로드 안 됨 (형제)
  ❌ project-c/CLAUDE.md        → 로드 안 됨 (형제)
```

형제 프로젝트의 내용은 서로 완전히 격리됩니다.

---

## 5. CLAUDE.md 작성 가이드

### 루트 공통 CLAUDE.md (root-project/CLAUDE.md)

모든 하위 프로젝트에 공통으로 적용할 내용을 작성합니다.

```markdown
# [프로젝트명] 공통 규칙

## 프로젝트 개요
- 전체 목적 및 구성 설명
- 하위 프로젝트 목록: project-a, project-b, project-c

## 공통 코딩 규칙
- 언어: Python 3.11+
- 코드 스타일: PEP8
- 커밋 메시지 형식: [type]: description

## 공통 아키텍처
- 공유 API 엔드포인트, 데이터베이스 구조 등

## 보안 규칙
- 비밀키, API 키는 절대 코드에 포함하지 말 것
- .env 파일 사용 필수
```

### 서브 프로젝트 CLAUDE.md (project-a/CLAUDE.md)

담당 컴퓨터 명시와 a 전용 지시문을 작성합니다.

```markdown
# Project A

> ⚠️ 이 프로젝트는 컴퓨터 A 전용입니다.
> 다른 컴퓨터에서 이 폴더를 열었다면 즉시 닫고 담당자에게 알리세요.
> 담당 컴퓨터 경로: /Users/[사용자명]/OneDrive/root-project/project-a

## 담당
- 컴퓨터: 컴퓨터 A
- 담당자: [이름]

## Project A 개요
- 역할 및 기능 설명

## 기술 스택
- 사용 프레임워크, 라이브러리 등

## 현재 진행 상황
- (세션이 바뀔 때마다 여기에 상태를 기록해두면 맥락 유지에 도움)
- 마지막 업데이트: YYYY-MM-DD

## 주의사항
- A 프로젝트 특유의 패턴, 하지 말아야 할 것
```

---

## 6. 각 컴퓨터의 실행 방법

**반드시 담당 서브 프로젝트 폴더로 이동한 후** Claude Code를 실행합니다.

### Mac / Linux

```bash
# 컴퓨터 A — project-a 담당
cd ~/OneDrive/root-project/project-a
claude

# 컴퓨터 B — project-b 담당
cd ~/OneDrive/root-project/project-b
claude

# 컴퓨터 C — project-c 담당
cd ~/OneDrive/root-project/project-c
claude
```

### Windows (PowerShell)

```powershell
# 컴퓨터 A — project-a 담당
cd "$env:USERPROFILE\OneDrive\root-project\project-a"
claude

# 컴퓨터 B — project-b 담당
cd "$env:USERPROFILE\OneDrive\root-project\project-b"
claude
```

> **주의**: 루트 폴더(`root-project/`)에서 `claude`를 실행하면 하위 프로젝트들이 모두 작업 범위에 포함되어 의도치 않은 파일 수정이 발생할 수 있습니다.

---

## 7. OS별 절대 경로 확인 방법

세션 이력 공유 여부를 확인하려면 두 컴퓨터의 절대 경로가 동일한지 먼저 확인합니다.

### Mac / Linux

```bash
# 현재 폴더의 절대 경로 확인
cd ~/OneDrive/root-project/project-a
pwd
# 출력 예: /Users/me/OneDrive/root-project/project-a

# 실제 세션 저장 폴더명 확인
ls ~/.claude/projects/
```

### Windows

```cmd
:: 명령 프롬프트
cd %USERPROFILE%\OneDrive\root-project\project-a
cd
:: 출력 예: C:\Users\me\OneDrive\root-project\project-a
```

```powershell
# PowerShell
cd "$env:USERPROFILE\OneDrive\root-project\project-a"
(Get-Item .).FullName

# 세션 저장 폴더 확인
ls "$env:USERPROFILE\.claude\projects\"
```

---

## 8. 세션 이력 공유 가능 조건

같은 프로젝트 세션 이력을 다른 컴퓨터에서도 보려면 아래 **두 조건을 동시에 만족**해야 합니다.

| 조건 | 설명 |
|------|------|
| ① 절대 경로 동일 | 두 컴퓨터의 프로젝트 폴더 절대 경로가 완전히 일치 |
| ② 세션 파일 공유 | `~/.claude/projects/<인코딩된 경로>/` 폴더가 두 컴퓨터에 모두 존재 |

### OS 조합별 가능 여부

| 조합 | 경로 일치 | 이력 공유 |
|------|:---:|:---:|
| Mac ↔ Mac (동일 사용자명, 동일 경로) | ✅ | ✅ 가능 |
| Windows ↔ Windows (동일 사용자명, 동일 경로) | ✅ | ✅ 가능 |
| Mac ↔ Windows | ❌ 불가 | ❌ 불가 |
| Mac ↔ Mac (사용자명 다름) | ❌ 불가 | ❌ 불가 |

### 세션 이력 수동 동기화 방법 (Mac ↔ Mac, 경로 동일한 경우)

```bash
# 컴퓨터 A에서 세션 파일을 OneDrive에 복사 (작업 종료 후)
cp -r ~/.claude/projects/-Users-me-OneDrive-root-project-project-a/ \
      ~/OneDrive/.claude-sessions/project-a/

# 컴퓨터 A2에서 세션 파일 복원 (작업 시작 전)
cp -r ~/OneDrive/.claude-sessions/project-a/ \
      ~/.claude/projects/-Users-me-OneDrive-root-project-project-a/
```

> **경고**: Claude Code 실행 중에는 세션 파일을 복사하지 마세요. 종료 후 복사해야 최신 내용이 반영됩니다.

---

## 9. 실수 시나리오와 위험 분석

### 시나리오: 컴퓨터 A에서 실수로 project-b를 열었을 때

```
정상:  컴퓨터 A → project-a,  컴퓨터 B → project-b
실수:  컴퓨터 A → project-b,  컴퓨터 B → project-b  ← 동시 접근!
```

#### 문제 ① 파일 충돌 (심각도: 높음)

A와 B가 동시에 같은 파일을 편집하면 OneDrive가 충돌 파일을 자동 생성합니다.

```
project-b/
├── main.py                                    ← B가 저장한 버전
└── main (컴퓨터 A의 충돌 복사본).py           ← OneDrive 자동 생성
```

Claude Code는 이 충돌을 감지하지 못하므로 **코드 손상 위험**이 있습니다.

#### 문제 ② 세션 이력 분산 (심각도: 중간)

```
컴퓨터 A 로컬: project-b 세션 → A만 알고 있음
컴퓨터 B 로컬: project-b 세션 → B만 알고 있음
```

B에서 `claude --resume` 해도 A에서 진행한 작업 내용이 전혀 보이지 않습니다.
같은 작업이 중복으로 진행되거나, 서로 모순된 방향으로 개발될 수 있습니다.

#### 문제 ③ 환경 설정 불일치 (심각도: 낮음)

CLAUDE.md는 정상 로드되지만, 컴퓨터 A에 설정된 MCP 서버, 환경변수, 로컬 경로 등이 project-b 환경과 맞지 않을 수 있어 예상치 못한 동작이 발생할 수 있습니다.

---

## 10. 실수 예방 체크리스트

### CLAUDE.md에 담당 컴퓨터 경고 삽입

각 서브 프로젝트의 `CLAUDE.md` 맨 위에 아래 내용을 추가합니다.
Claude Code 세션 시작 시 Claude가 즉시 읽으므로, 잘못된 컴퓨터에서 열었을 때 경고를 인지할 수 있습니다.

```markdown
> ⚠️ **담당 컴퓨터 확인**
> 이 프로젝트는 **컴퓨터 B** 전용입니다.
> 세션 시작 전 현재 컴퓨터가 컴퓨터 B인지 확인하세요.
> 다른 컴퓨터라면 즉시 Claude Code를 종료하고 담당자에게 알리세요.
```

### 작업 시작 전 확인 루틴

```bash
# 1. 현재 경로 확인
pwd

# 2. 의도한 프로젝트 폴더인지 확인
# (project-a 담당이라면 경로에 'project-a'가 있어야 함)

# 3. Claude Code 실행
claude
```

### 터미널 프롬프트 커스터마이징 (Mac/Linux)

`~/.zshrc` 또는 `~/.bashrc`에 추가하면 항상 현재 경로가 보여 실수를 줄일 수 있습니다.

```bash
# 프롬프트에 현재 경로 표시
export PS1="\u@\h [\w] $ "
```

---

## 11. 동기화 항목 요약표

| 항목 | 저장 위치 | 공유 방법 | 비고 |
|------|-----------|-----------|------|
| 소스 코드 | 공유 폴더 | OneDrive 자동 | ✅ 항상 동기화 |
| `CLAUDE.md` (루트) | 공유 폴더 | OneDrive 자동 | ✅ 모든 서브에 상속 |
| `CLAUDE.md` (서브) | 공유 폴더 | OneDrive 자동 | ✅ 해당 프로젝트 전용 |
| `.mcp.json` | 공유 폴더 | OneDrive 자동 | ✅ MCP 서버 설정 |
| 세션 대화 이력 | `~/.claude/projects/` | 수동 복사 필요 | ❌ 기본 비공유 |
| `~/.claude/settings.json` | 로컬 홈 | 수동 동기화 | ❌ 개인 설정 |
| `~/.claude/CLAUDE.md` (전역) | 로컬 홈 | 수동 동기화 | ❌ 개인 전역 설정 |

---

## 12. 고급 설정: CLAUDE_CONFIG_DIR

`CLAUDE_CONFIG_DIR` 환경변수를 설정하면 `~/.claude` 전체를 다른 경로로 변경할 수 있습니다.
이를 OneDrive 내부 경로로 지정하면 세션 이력을 포함한 모든 설정이 동기화됩니다.

### 설정 방법 (Mac/Linux)

```bash
# ~/.zshrc 또는 ~/.bashrc에 추가
export CLAUDE_CONFIG_DIR="$HOME/OneDrive/.claude-config"
```

### 설정 방법 (Windows PowerShell)

```powershell
# PowerShell 프로파일에 추가
$env:CLAUDE_CONFIG_DIR = "$env:USERPROFILE\OneDrive\.claude-config"
```

### 주의사항

| 주의사항 | 설명 |
|----------|------|
| 동시 실행 금지 | 두 컴퓨터에서 동시에 Claude Code 실행 시 파일 충돌 발생 가능 |
| 경로 일치 필수 | 두 컴퓨터의 `CLAUDE_CONFIG_DIR` 값이 동일해야 세션 이력이 연결됨 |
| OS 혼용 불가 | Mac ↔ Windows는 경로 체계가 달라 이력 연결 불가 |
| 개인 설정 공유 | 이 방식은 개인 설정까지 모두 공유되므로 팀 공유보다 개인 멀티컴퓨터 환경에 적합 |

---

## 부록: 트러블슈팅

### 세션 이력이 보이지 않을 때

```bash
# 현재 프로젝트에 해당하는 세션 폴더 확인
ls ~/.claude/projects/ | grep $(pwd | sed 's/\//-/g')
```

### CLAUDE.md가 로드되었는지 확인

Claude Code 세션 안에서:

```
/memory
```

실행하면 현재 세션에 로드된 모든 CLAUDE.md 목록을 확인할 수 있습니다.

### OneDrive 충돌 파일 발생 시

1. Claude Code를 즉시 종료합니다.
2. 두 버전의 파일 내용을 비교합니다.
3. 올바른 버전을 선택하고 충돌 복사본을 삭제합니다.
4. 이후 한 번에 한 컴퓨터만 해당 프로젝트에서 작업합니다.

---

*이 가이드는 Claude Code CLI의 동작 방식에 따라 작성되었으며, 버전 업데이트에 따라 일부 내용이 변경될 수 있습니다.*  
*최신 정보: https://docs.claude.com/en/docs/claude-code/overview*
