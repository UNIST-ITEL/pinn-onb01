# Workspace Restructure Proposal — Multi-Phase Research Layout

**작성일**: 2026-05-19
**상태**: 제안 — 사용자 승인 후 단계별 마이그레이션
**작성 배경**: Phase 1 (IJHMT 제출 완료) + Phase 1.5 (in-house augmentation) + Phase 2 (flow boiling) 등 다중 단계 연구의 독립성 확보와 동시에 공통 코드의 효율적 운영 필요

---

## 1. 현재 구조 (As-Is)

```
PINN-ONB01/                          # 단일 평면 구조 (Phase 1만 가정)
├── 01_survey/
├── 02_data/
├── 03_model/                        # PINN 소스 + 체크포인트 혼재
├── 04_analysis/
├── 05_manuscript/
├── .claude/                         # 24 agents + 1 command
├── ONB_PINN_Phase1_Pool_Boiling_Plan.md
├── ONB_PINN_Phase1p5_InHouse_Augmentation_Plan.md
├── ONB_PINN_Phase2_Flow_Boiling_Plan.md
├── PHASE_STATUS.md
├── RELEASE_CHECKLIST.md
└── (기타 release artifacts)
```

### 한계점

| # | 한계 | 영향 |
|---|---|---|
| 1 | Phase 간 데이터/결과 분리 부재 | Phase 1.5에서 03_model에 새 체크포인트 추가 시 Phase 1 결과와 섞임 |
| 2 | 공유 코드 vs Phase 별 결과의 경계 모호 | "어디까지가 framework, 어디까지가 phase artifact인가" |
| 3 | Phase 1 paper 게재 후 코드 변경이 Phase 1 결과 재현성을 깰 수 있음 | Reproducibility 위험 |
| 4 | Phase 2 시작 시 또 동일 구조 (01~05) 반복 → 중복/혼선 | 확장성 한계 |
| 5 | Manuscript 폴더 (05_manuscript/) 하나만 있어 미래 paper 다수 관리 불편 | 향후 multi-paper 운영 어려움 |

---

## 2. 핵심 의사결정 — 공유 코드 운영 방식

세 가지 패턴 비교:

### 옵션 A — **각 Phase가 코드를 자체 복사**

```
phase1/
├── src/                  ← 자체 복사본 v1.0
└── data/

phase1p5/
├── src/                  ← 자체 복사본 v1.5 (Phase 1 src 복사 후 수정)
└── data/
```

| 평가 항목 | 점수 |
|---|---|
| Paper reproducibility | ★★★★★ |
| 버그 수정 전파 | ★ (각 phase 일일이 fix) |
| 코드 중복 | ★ (DRY 위배) |
| 리뷰어 검증 편의 | ★★★★ (`phase1/src` 만 보면 됨) |
| 향후 phase 추가 | ★★★ (반복 작업) |

**적합 사례**: Phase 1 paper가 freeze 되어 reproduce 가능성이 최우선일 때.

### 옵션 B — **`shared/` 단일 공유 폴더 + Phase 별 결과 폴더**

```
shared/
└── src/                  ← 모든 phase가 동일 소스 import

phase1/                   ← shared/src import, 자체 data + experiments
phase1p5/                 ← 동일
```

| 평가 항목 | 점수 |
|---|---|
| Paper reproducibility | ★★ (shared 변경 시 옛 phase 결과 깨질 수 있음) |
| 버그 수정 전파 | ★★★★★ |
| 코드 중복 | ★★★★★ (없음) |
| 리뷰어 검증 편의 | ★★★ (shared/src 모두 봐야) |
| 향후 phase 추가 | ★★★★★ (단순) |

**적합 사례**: 활발한 개발 중인 단일 프레임워크.

### 옵션 C — **하이브리드: `shared/` + Git tag로 phase별 freeze** ⭐ 권장

```
shared/
├── src/                  ← 활발 개발, 최신 소스
└── pyproject.toml        ← installable pkg "pinn_onb"

phase1/                   ← shared @ phase1-v1.0 tag 사용 (paper 명시)
phase1p5/                 ← shared @ phase1p5-v1.0 tag 사용
phase2/                   ← shared @ phase2-v1.0 tag (future)

git tags:
  phase1-v1.0-submitted   2026-05-18 (제출 시점 freeze)
  phase1-v1.0-published   (수락 후 발급)
  shared-v1.0             phase1-v1.0와 동일 시점 shared/ 스냅샷
  phase1p5-v1.0           Phase 1.5 게재 시점
  shared-v1.5             phase1p5-v1.0와 동일 시점 shared/ 스냅샷
  ...
```

| 평가 항목 | 점수 |
|---|---|
| Paper reproducibility | ★★★★ (`git checkout phase1-v1.0` 으로 완전 복원) |
| 버그 수정 전파 | ★★★★ (활발 개발 중에는 자유, 게재 후 tag로 freeze) |
| 코드 중복 | ★★★★★ (없음) |
| 리뷰어 검증 편의 | ★★★★ (git tag 한 줄 안내) |
| 향후 phase 추가 | ★★★★★ |

**적합 사례**: 본 프로젝트. Phase 1 게재 후에도 framework가 Phase 1.5, Phase 2로 진화하지만, 각 phase paper의 결과는 git tag로 영구 reproducible.

---

## 3. 제안 To-Be 구조 (옵션 C 기반)

```
PINN-ONB01/  (workspace root, github.com/UNIST-ITEL/pinn-onb01)
│
├── shared/                                  # 공유 자산 (모든 phase 사용)
│   ├── src/                                 # Installable Python package
│   │   ├── pinn_onb/
│   │   │   ├── __init__.py
│   │   │   ├── model/                       # PINN architecture
│   │   │   │   ├── pinn.py
│   │   │   │   ├── surface_encoder.py
│   │   │   │   ├── film_layers.py
│   │   │   │   └── __init__.py
│   │   │   ├── loss/                        # composite loss
│   │   │   ├── training/                    # train, ensemble, hpo
│   │   │   ├── correlations/                # 5 classical (Hsu...Basu)
│   │   │   ├── utils/                       # CoolProp, nondim, properties
│   │   │   └── inference/                   # predict_new_experiment.py
│   │   ├── tests/
│   │   │   ├── test_correlations.py
│   │   │   ├── test_model_io.py
│   │   │   └── test_inference.py
│   │   ├── pyproject.toml                   # `pip install -e ./shared/src/`
│   │   └── README.md
│   │
│   ├── docs/                                # 모든 phase가 공유하는 기술 문서
│   │   ├── ARCHITECTURE.md
│   │   ├── DATA_SCHEMA.md                   # 12-column CSV schema
│   │   ├── MEASUREMENT_GUIDE.md             # 실험 측정 가이드
│   │   ├── SETUP_GITHUB_ZENODO_GUIDE.md
│   │   └── RELEASE_CHECKLIST.md
│   │
│   └── templates/                           # 빈 양식
│       ├── new_experiment_template.csv
│       ├── surface_card_template.yaml
│       └── paper_card_template.md
│
├── phase1_pool_boiling/                     # Phase 1 (IJHMT 제출, 수락 대기)
│   ├── README.md                            # 본 phase의 진입점
│   ├── plan.md → ONB_PINN_Phase1_Pool_Boiling_Plan.md (symlink 또는 이름변경)
│   ├── data/
│   │   ├── raw/literature/                  # 7 외부 출처
│   │   ├── processed/
│   │   │   ├── boiling_curves.csv           # 1361 rows
│   │   │   ├── onb_dataset.csv              # 82 rows
│   │   │   └── README.md
│   │   └── surface_cards/                   # SFC-001 ~ SFC-049
│   ├── experiments/
│   │   ├── checkpoints/
│   │   │   └── baseline_phaseDbal/          # 최종 모델
│   │   ├── ensemble/                        # K=10 seeds
│   │   ├── configs/                         # YAML configs
│   │   ├── logs/
│   │   └── mlflow_runs/
│   ├── analysis/
│   │   ├── figures/                         # 9 main + 10 supp
│   │   ├── tables/
│   │   └── scripts/                         # phase1 전용 분석 스크립트
│   ├── manuscript/
│   │   ├── main.tex
│   │   ├── supplementary/
│   │   ├── sections/
│   │   ├── references.bib
│   │   └── figures/                         # EPS/PDF for journal
│   └── presentations/                       # Phase 1 발표·보고 자료
│       ├── slides/                          # 학회·세미나·archive
│       ├── posters/
│       ├── reports/                         # 진척 보고
│       ├── outreach/
│       └── conference_abstracts/
│
├── phase1p5_inhouse_augmentation/           # Phase 1.5 (계획 단계)
│   ├── README.md
│   ├── plan.md → ONB_PINN_Phase1p5_InHouse_Augmentation_Plan.md
│   ├── data/
│   │   ├── raw/lab/
│   │   │   ├── lee_2023_ichmt/              # 출처 1
│   │   │   ├── lee_2024_ichmt/              # 출처 2
│   │   │   ├── inhouse_corrosion/           # 출처 3
│   │   │   └── inhouse_biphilic/            # 출처 4
│   │   ├── processed/
│   │   │   ├── boiling_curves_v1p5.csv      # phase1 + lab 통합 (or 분리 유지)
│   │   │   └── onb_dataset_v1p5.csv
│   │   ├── surface_cards/                   # SFC-051 ~ SFC-070+ (신규)
│   │   └── lab_data_inventory.md            # 별도 inventory
│   ├── experiments/
│   │   ├── checkpoints/
│   │   │   ├── V0_phase1_baseline/          # ablation V0
│   │   │   ├── V1_laser_only/
│   │   │   ├── V2_corrosion_only/
│   │   │   ├── V3_biphilic_only/
│   │   │   ├── V4_full/                     # main result
│   │   │   └── V5_lab_only/
│   │   └── configs/
│   ├── analysis/
│   │   ├── figures/                         # ablation, OOD, calibration
│   │   ├── tables/
│   │   └── scripts/                         # phase1.5 전용
│   ├── manuscript/                          # ICHMT 1순위
│   │   ├── main.tex
│   │   └── (similar to phase1)
│   └── presentations/                       # Phase 1.5 발표·보고 자료
│       ├── slides/                          # 학회·세미나
│       ├── posters/
│       ├── reports/                         # 진척 보고
│       ├── outreach/
│       └── conference_abstracts/
│
├── phase2_flow_boiling/                     # Phase 2 (future)
│   └── (similar structure including presentations/)
│
├── presentations/                           # Cross-phase 발표 자료 (workspace-level)
│   ├── workspace_overview/                  # PINN-BOILING 전체 소개
│   ├── grant_reports/                       # NRF/KETEP 통합 보고
│   ├── lab_meetings/                        # 워크스페이스 lab meeting
│   └── thesis_defense/                      # 학위논문 발표
│
├── .claude/                                 # workspace-wide agents/commands
│   ├── agents/                              # 24 + 2 agents (Phase 1 + 1.5 신규)
│   └── commands/                            # 1 + 5 commands
│
├── CLAUDE.md                                # workspace-level project rules
├── PHASE_STATUS.md                          # cross-phase 진척 표
├── RELEASE_CHECKLIST.md                     # release procedures (or 옮김 → shared/docs/)
├── future_research_roadmap.md
├── README.md                                # workspace 개요 (Phase 안내)
├── README_PUBLIC.md                         # 공개 github repo의 README
├── CITATION.cff
├── LICENSE-CODE                             # MIT
├── LICENSE-DATA                             # CC-BY-4.0
├── requirements.txt                         # workspace deps (또는 shared/에 위임)
├── environment.yml
├── .gitignore
└── (workspace-level admin files)
```

### 폴더 명명 규칙

| 패턴 | 이유 |
|---|---|
| `phase1_pool_boiling/` | Phase 번호 + 핵심 주제. 디렉토리 정렬 시 자연 순서 (`phase1`, `phase1p5`, `phase2`) |
| `shared/src/pinn_onb/` | Python package 이름과 import 경로 일치 (`from pinn_onb.model import ...`) |
| Phase 내 폴더 | 1단계 자리 숫자 prefix 제거 (`01_survey` → `survey` 등) — 이미 phase 안이라 redundant |

---

## 4. 코드 import 변경 예시

### 현재 (Phase 1, 평면 구조)

```python
# 04_analysis/scripts/correlation_comparator.py
sys.path.insert(0, str(PROJECT_ROOT / "03_model" / "src"))
from utils.properties import SaturationProperties
from model.pinn import PoolBoilingPINN
```

### 변경 후 (옵션 C, package import)

```python
# phase1_pool_boiling/analysis/scripts/correlation_comparator.py
# shared/ 가 'pip install -e' 로 설치된 후
from pinn_onb.correlations.classical import Hsu, DavisAnderson, Basu
from pinn_onb.utils.properties import SaturationProperties
from pinn_onb.model.pinn import PoolBoilingPINN
```

→ Path hack (`sys.path.insert`) 제거. Standard Python packaging.

---

## 5. Phase별 git tag 전략

### 5.1 Tag 명명 규칙

```
phaseN-v<major.minor>-<state>

phase1-v1.0-submitted        2026-05-18 (제출 시점)
phase1-v1.0-revision1        Reviewer 1차 revision 후
phase1-v1.0-published        IJHMT 게재 확정
phase1p5-v1.0-submitted      Phase 1.5 ICHMT 제출
phase1p5-v1.0-published      Phase 1.5 게재
phase2-v1.0-submitted        ...
```

### 5.2 Shared/ snapshot tag

```
shared-v1.0   phase1-v1.0-submitted 시점의 shared/ 스냅샷
shared-v1.5   phase1p5-v1.0-submitted 시점
shared-v2.0   phase2 시점
```

### 5.3 Paper에 명시할 reproducibility 안내

```markdown
## Reproducing the published results

To reproduce the results in this paper exactly:

  git clone https://github.com/UNIST-ITEL/pinn-onb01.git
  cd pinn-onb01
  git checkout phase1-v1.0-published
  pip install -e ./shared/src/
  cd phase1_pool_boiling
  make figures
```

→ Reviewer / 후속 연구자에게 명확한 경로 제공.

---

## 6. 마이그레이션 전략

전체 한꺼번에 옮기지 말고 **3단계 점진 마이그레이션** 권장:

### Stage 1 — `shared/` 신설 + 새 phase 1.5는 새 구조에서 시작 (1주, 위험 ★)

```
[유지]                         [추가]
01_survey/                     phase1p5_inhouse/
02_data/                       shared/src/pinn_onb/  (03_model/src 심볼릭 링크 또는 카피)
03_model/                      shared/docs/
04_analysis/
05_manuscript/
```

- Phase 1 폴더 구조 그대로 유지 (제출 후 review 대기 중이라 변경 위험 회피)
- Phase 1.5 는 새 구조 사용
- `shared/src/pinn_onb/` 는 03_model/src/ 의 심볼릭 링크 또는 동일 복사본

**장점**: Phase 1 review 진행 중에는 영향 없음.
**단점**: 임시로 두 경로 공존 (03_model/src/ + shared/src/pinn_onb/).

### Stage 2 — Phase 1 게재 수락 후 정식 마이그레이션 (1-2주, 위험 ★★)

```
[Phase 1 수락 시점에 한 번에]
01_survey/        →  phase1_pool_boiling/survey/
02_data/          →  phase1_pool_boiling/data/
03_model/         →  phase1_pool_boiling/experiments/
                  +  shared/src/pinn_onb/ (정식 분리)
04_analysis/      →  phase1_pool_boiling/analysis/
05_manuscript/    →  phase1_pool_boiling/manuscript/
```

- `git tag phase1-v1.0-published` 발급 시점에 freeze
- `git mv` 로 history 보존
- README_PUBLIC.md 갱신, paper 내 repo URL 안내 보강

### Stage 3 — Phase 2 추가 (Phase 1.5 완료 후, 자연스럽게)

```
phase2_flow_boiling/ 디렉토리 신설
```

이 시점에는 패턴이 확립되어 있어 마찰 없음.

---

## 7. 위험 및 완화

| 위험 | 가능성 | 완화 |
|---|---|---|
| Stage 1 도중 import 경로 충돌 (03_model + shared 동시 존재) | Medium | `shared/` 를 sys.path 후순위로, 또는 임시로 03_model/src 만 사용 |
| Stage 2 마이그레이션 후 Phase 1 결과 재현 실패 | Low (코드 변경 없으므로) | Smoke test (parity plot 재생성)로 검증 |
| 외부 reviewer가 게재 후 repo 방문 시 구조 변경에 혼란 | Low | README_PUBLIC.md 상단에 변경 history + tag 안내 |
| GitHub `phase1-v1.0-published` tag 와 Zenodo archive 일치 | Critical | Zenodo는 Release tag 시점 stamp — 마이그레이션 전에 Release 발행 권장 |
| .claude/agents/ 가 phase별 분리 안 됨 | Low | agents는 workspace-level 자산이라 의도된 공유. Phase 별 customization 필요 시 `.claude/agents/phase1/` 서브폴더 가능 |
| pyproject.toml 의존성 lock 깨짐 | Low | `requirements-lock.txt` Phase별로 freeze |

---

## 8. 미실시 시 (Stay As-Is) 옵션

만약 마이그레이션 자체를 보류한다면:

| 부분 채택 | 효과 |
|---|---|
| Phase 1.5 만 `phase1p5_inhouse/` 별도 폴더로 격리 (Phase 1은 평면 구조 유지) | 즉시 격리, 마이그레이션 위험 회피 |
| 단, shared/ 미신설 → Phase 1.5 가 `../03_model/src/` 를 import 하는 형태 | Path 의존 (덜 깔끔하지만 작동) |
| Phase 2 시작 시 다시 결정 | 결정 유보 |

→ "Stage 1만 부분 적용" 옵션. 권장하지 않지만 가능.

---

## 9. 결정 요청 사항

다음 4개 항목 결정 후 마이그레이션 착수:

| # | 결정 | 추천 |
|---|---|---|
| 1 | 옵션 A (복사) / B (공유) / **C (하이브리드)** 중 선택 | **C** ⭐ |
| 2 | Stage 1 즉시 시작 / Phase 1 수락 후 일괄 / 보류 | **Stage 1 즉시** |
| 3 | `shared/` 와 phase 폴더 명명 (제안: `phase1_pool_boiling/`, `phase1p5_inhouse_augmentation/`) | 짧게 → `phase1/`, `phase1p5/` 도 가능 |
| 4 | Python package 이름 (제안: `pinn_onb`) | 사용자 의견 |

---

## 10. 본 제안의 위치

- **본 문서**: `WORKSPACE_RESTRUCTURE_PROPOSAL.md` (workspace root)
- 본 제안이 승인되면:
  - 마이그레이션 작업은 별도 commit/branch에서 진행
  - CLAUDE.md, README_PUBLIC.md 등 후속 갱신
  - 본 제안 문서는 archive 폴더 (예: `docs/decisions/`) 또는 의사결정 record 로 보존
