# PINN-BOILING — Multi-Phase Boiling ONB Research Workspace

> ⚠️ **담당 컴퓨터 확인 — Workspace Root**
>
> 본 root 디렉토리는 **`macmini` (호스트: `MyHomeMiniui-Macmini.local`, 사용자: `myhomemini`)** 전용 작업 영역입니다.
> Phase 1 (`01_survey/~05_manuscript/`, `phase1_pool_boiling/`) 과 Phase 1.5 (`phase1p5_inhouse_augmentation/`) 가 본 root 에서 진행됩니다.
>
> **🚫 Phase 2 담당 컴퓨터 (또는 macmini 가 아닌 모든 host) 는 본 root 에서 작업하지 마세요.**
> - root 에서 파일 편집 시 OneDrive 충돌 (`xxx (Computer B의 충돌 복사본).md`) 발생 가능 → 코드 손상 위험
> - root commit 은 Phase 1 history 를 fork 시킬 수 있음
> - 세션 이력이 macmini 의 진행과 분리되어 중복/모순 작업 유발
>
> **Phase 2 host 는 반드시:**
> ```bash
> cd <OneDrive-path>/PINN-ONB01/phase2_flow_boiling
> claude   # 이 폴더 안에서만 작업
> ```
>
> 자신의 컴퓨터가 어느 phase 담당인지 확인: root `HOSTS.md` 참조.
> 잘못된 컴퓨터에서 열었다면 즉시 Claude Code 종료 → 담당자(Jaeseon Lee, `leejs92@gmail.com`)에게 통보.
> 운영 원리 전체: `claude-code-multi-project-guide.md`.

---

PINN(Physics-Informed Neural Network)을 이용한 풀비등 / 강제대류 비등 핵비등
개시점(ONB, Onset of Nucleate Boiling) 예측 연구 워크스페이스.

워크스페이스 명칭: **PINN-BOILING** (이전 PINN-ONB01 에서 일반화, 2026-05-19).
OneDrive 폴더명 / GitHub repo 명 (`UNIST-ITEL/pinn-onb01`)은 Phase 1 paper 인용
일관성을 위해 현 이름 유지.

## 활성 트랙

| Phase | 주제 | 상태 (2026-05-20) | 폴더 | 담당 컴퓨터 |
|---|---|---|---|---|
| **Phase 1** | 풀비등 ONB (외부 corpus, 표면 개질 중심) | ✅ IJHMT 제출, review 대기 | `01_survey/`, `02_data/`, `03_model/`, `04_analysis/`, `05_manuscript/` (Stage 2 시 `phase1_pool_boiling/`로 이동) | **macmini** |
| **Phase 1.5** | In-house lab data augmentation (laser/corrosion/biphilic) | 진행 중 (계획 단계) ⭐ | `phase1p5_inhouse_augmentation/` | **macmini** |
| **Phase 2** | Forced-convection subcooled flow boiling ONB | Future (Phase 1.5 후) | `phase2_flow_boiling/` (skeleton 신설 2026-05-20) | **`macbook-air-6`** (`MacBook-Air-6.local`, `mymachome`) — host setup 완료 2026-05-21 |
| **Phase 3+** | Transient / multi-fluid / industrial 응용 | Roadmap | TBD | TBD |

세부 컴퓨터 매핑 + 운영 규칙: `HOSTS.md` 참조. Multi-computer 운영 원리: `claude-code-multi-project-guide.md`.

## 워크스페이스 구조 (현재, Stage 1)

```
PINN-BOILING/  (OS 상 OneDrive 폴더는 PINN-ONB01 유지)
│
├── shared/                      공유 자산 (모든 phase 사용)
│   ├── src/pinn_onb/            Python package (skeleton; Stage 2에서 실 코드)
│   ├── docs/                    공통 기술 문서 (Stage 2 시 채워짐)
│   └── templates/               빈 양식 (Stage 2 시 이동)
│
├── 01_survey/ ~ 05_manuscript/  Phase 1 (현 평면 구조, Stage 2 후 phase1_pool_boiling/ 로 이동)
│
├── phase1_pool_boiling/         Phase 1 (Stage 2 대비 placeholder)
│   └── presentations/           Phase 1 발표·보고 자료 (slides, posters, reports, outreach, abstracts)
│
├── phase1p5_inhouse_augmentation/  Phase 1.5 (신규)
│   ├── CLAUDE.md                담당 컴퓨터 = macmini 경고
│   ├── plan.md                  Phase 1.5 plan
│   ├── data/                    raw lab + processed + surface_cards
│   ├── experiments/             V0-V5 ablation 체크포인트
│   ├── analysis/                figures + tables + scripts
│   ├── manuscript/              ICHMT main.tex
│   └── presentations/           Phase 1.5 발표·보고 자료
│
├── phase2_flow_boiling/         Phase 2 (skeleton, 2026-05-20 신설)
│   ├── CLAUDE.md                담당 컴퓨터 = macbook-air-6 (MacBook-Air-6.local, mymachome) 경고
│   ├── plan.md                  Phase 2 plan (이전: root ONB_PINN_Phase2_Flow_Boiling_Plan.md)
│   ├── data/, experiments/, analysis/, manuscript/, presentations/
│
├── presentations/               Cross-phase 발표 자료 (workspace overview, grant reports, lab meetings, thesis defense)
│
├── .claude/                     모든 phase 공유 (24+2 agents, 1+5 commands)
│
├── CLAUDE.md                    본 파일 (workspace-level)
├── HOSTS.md                     컴퓨터 ↔ phase 매핑 (multi-computer 운영) ⭐ 신규
├── claude-code-multi-project-guide.md  다중 프로젝트 · 다중 컴퓨터 운영 가이드
├── PHASE_STATUS.md              cross-phase 진척
├── RELEASE_CHECKLIST.md         release 절차
├── future_research_roadmap.md   30 후속 주제
├── ONB_PINN_Phase1_Pool_Boiling_Plan.md         Phase 1 plan
├── phase1p5_inhouse_augmentation/plan.md         Phase 1.5 plan (이동: 2026-05-19)
├── phase2_flow_boiling/plan.md                   Phase 2 plan (이동: 2026-05-20)
├── WORKSPACE_RESTRUCTURE_PROPOSAL.md            구조 변경 의사결정
├── SETUP_GITHUB_ZENODO_GUIDE.md
├── README_PUBLIC.md
└── (LICENSE, CITATION, requirements, env, 등)
```

## 다중 컴퓨터 운영 (2026-05-20)

본 워크스페이스는 OneDrive 동기화 기반으로 **phase 별 컴퓨터 분담**을 지원합니다.

| 컴퓨터 | 호스트명 | 담당 phase | 허용 작업 디렉토리 |
|---|---|---|---|
| **macmini** | `MyHomeMiniui-Macmini.local` (`myhomemini`) | Phase 1, Phase 1.5 | workspace root, `01_~05_`, `phase1_pool_boiling/`, `phase1p5_inhouse_augmentation/`, `shared/`, `presentations/` |
| **macbook-air-6** | `MacBook-Air-6.local` (`mymachome`) — Phase 2 host | Phase 2 | `phase2_flow_boiling/` **만** (root, 다른 phase 폴더 진입 금지) |

각 phase 폴더의 `CLAUDE.md` 첫 줄에 **담당 컴퓨터 경고** 가 있어, 잘못된 컴퓨터에서 열었을 때 Claude 가 즉시 인지합니다.
운영 규칙·실수 시나리오·예방 체크리스트: `claude-code-multi-project-guide.md`, 매핑 표: `HOSTS.md`.

## 마이그레이션 단계 (2026-05-20 현재 Stage 1)

| Stage | 시점 | 작업 |
|---|---|---|
| **Stage 1 (현재)** | 2026-05-19 | `shared/` skeleton + `phase1p5_inhouse_augmentation/` 신설. Phase 1 평면 구조 유지 |
| Stage 2 | Phase 1 수락 후 | Phase 1 코드를 `phase1_pool_boiling/` + `shared/src/pinn_onb/` 로 분리 |
| Stage 3 | Phase 2 시작 | `phase2_flow_boiling/` 추가 |

세부 사항: `WORKSPACE_RESTRUCTURE_PROPOSAL.md`.

## 연구 컨텍스트

- **분야**: 비등 열전달, 표면 공학, Physics-Informed Neural Networks
- **핵심 물리**: 풀비등 핵생성, Hsu 기준, 자연대류 경계조건
- **프레임워크**: PyTorch (DeepXDE는 방법론 reference 인용만; 런타임 비의존)
- **데이터**: 문헌 실험 + lab in-house + 합성(2D 열전도 해석)
- **유체**: 물(대기압 기본), R-123, R-134a (FC-77/FC-72/HFE-7100은 CoolProp 미지원)
- **가열 형상**: 수평 평판(상면), 수평 원형관 외면

## 주요 변수 명명 규칙

물리량은 다음 표기를 따른다 (LaTeX 수식과 일관성 유지):

| 코드 변수명 | 물리량 | 단위 |
|-----------|--------|------|
| `T_wall` | 벽면 온도 | K |
| `T_sat` | 포화 온도 | K |
| `T_bulk` | 벌크 유체 온도 | K |
| `delta_T_onb` | ONB 벽면 과열도 (T_wall − T_sat) | K |
| `delta_T_sub` | 과냉도 (T_sat − T_bulk) | K |
| `q_flux` | 열유속 | W/m² |
| `q_onb` | ONB 열유속 | W/m² |
| `Ra_surface` | 표면 거칠기 (산술 평균) | μm |
| `theta_contact` | 정적 접촉각 | ° (degree) |
| `r_c` | 활성 공동 반경 | μm |
| `N_s` | 공동 밀도 | sites/cm² |
| `Ja` | Jacob 수 | — |
| `h_nc` | 자연대류 열전달계수 | W/(m²·K) |
| `Bi` | Biot 수 (heater) | — |

무차원 변수는 접미 `_star` (예: `delta_T_star`, `q_star`, `r_star`).
무차원화 함수는 `utils/nondim.py` (Stage 2 후 `shared/src/pinn_onb/utils/nondim.py`).

## 코딩 규칙

- Python 3.10+ (3.13 검증됨), **type hints 필수** (`from __future__ import annotations`).
- SI 단위 기본, 입력 단위가 다르면 즉시 변환.
- 물성치는 **CoolProp**으로 계산 (REFPROP 대체 가능).
- PyTorch dtype은 `torch.float32` 기본, 정밀 검증 시 `float64`.
- 콜로케이션 포인트 샘플링은 LHS(Latin Hypercube Sampling) 사용.
- 모든 손실 항목은 `loss_functions.py`에 1:1 함수로 분리 (디버깅 용이).
- 학습 로그는 MLflow (Phase 1: `03_model/experiments/`, Phase 1.5: `phase1p5_inhouse_augmentation/experiments/logs/`).

## 도메인 지식 — 기억해 둘 사실

- **ΔT_ONB 물리적 범위** (물, 대기압): 2~30 °C. 이 범위를 벗어나면 데이터/예측 오류 의심.
- **r_c 활성 공동 크기**: 1 < r_c < 100 μm. SEM/AFM 측정과 비교.
- **물리적 경향성** (검증 시 필수 확인 5개):
  1. **q'' ↑ → ΔT_ONB ↑** — Hsu/Sato-Matsumura 공식 `ΔT_ONB ∝ √q''`. 단일 표면 boiling curve의 ΔT_wall 도 q와 함께 단조 증가.
  2. Ra ↑ → ΔT_ONB ↓ — 거친 표면일수록 더 작은 r_c 활성 cavity 존재 → 더 낮은 wall 과열도에서 ONB. **단, water 데이터셋은 표면개질(BETZ 매끈+코팅 vs JONES 거친+비처리)이 confounding으로 작용해 +상관도 보임. 깨끗한 Ra 효과는 R-134a/R-123 (JABARDO Cu) 데이터에서 관찰 (-0.7 ~ -0.5).**
  3. θ ↑ (소수성) → ΔT_ONB ↓ — Basu et al. F(θ) 의존성.
  4. P ↑ → ΔT_ONB ↓ — Bergles-Rohsenow 경험식. 압력↑ → 기포 직경↓.
  5. ΔT_sub ↑ → ΔT_ONB ↑
- **기존 상관식 비교 대상** (필수): Hsu(1962), Davis-Anderson(1966), Bergles-Rohsenow(1964), Sato-Matsumura(1964), Basu et al.(2002).
- **PINN 모델 특성**: 현 모델은 surface features (Ra, θ, category) → ΔT_ONB 직접 매핑. q_flux는 학습 시 PDE residual로만 사용되며 추론 시 직접 입력 아님. 동일 surface 의 여러 q'' 입력은 동일 예측 (정상 동작).
- **Phase 1.5 신규 surface category**: `unist_laser`, `unist_corrosion`, `unist_biphilic` (Phase 1 외부 10 카테고리에 추가).

## 단계별 산출물 책임

### Phase 1 (완료)

| 단계 | 기간 | 폴더 | Go/No-Go |
|-----|------|------|---------------|
| ① 서베이 | M1-2 | `01_survey/` | 갭 존재 확인 ✅ |
| ② 데이터 | M3-4 | `02_data/` | ONB 100+ ✅ (82 + 합성) |
| ③ 모델링 | M5-7 | `03_model/` | 상관식 동등 이상 ✅ (RMSE 3.42K vs 7.21K) |
| ④ 검증 | M8-9 | `04_analysis/` | 통계 개선 ✅ |
| ⑤ 문서화 | M10-12 | `05_manuscript/` | IJHMT 제출 ✅ (2026-05-18) |

### Phase 1.5 (진행 중)

| 단계 | 기간 | 산출물 |
|---|---|---|
| M1 인벤토리 | 1개월 | `lab_data_inventory.md` + 갱신 bib + OOD baseline |
| M2-M3 데이터 | 2개월 | SFC-051~070+ + boiling_curves_v1p5.csv + onb_dataset_v1p5.csv |
| M4 학습/검증 | 1개월 | V0-V5 ablation + OOD matrix + calibration plot |
| M5 작성 | 1개월 | ICHMT submission package |

자세한 계획: `phase1p5_inhouse_augmentation/plan.md`.

## 서브에이전트 / 슬래시 명령

`.claude/agents/` (현재 27 agents):

| Phase 1 (24개) | Phase 1.5 신규 (2개) | Cross-phase (1개) |
|---|---|---|
| paper-card-extractor, bibtex-curator, coolprop-integrator, correlation-comparator, debug-diagnoser, ensemble-uq, figure-composer, figure-digitizer, gap-matrix-mapper, hpo-tuner, inverse-solver, latex-formatter, level1-verifier, loss-function-builder, physics-consistency-check, pinn-architect, preprocess-pipeline, reviewer-anticipator, section-drafter, surface-card-builder, surface-encoder-dev, survey-search, synthetic-data-gen, training-orchestrator | **lab-onb-labeler** (lab boiling curve → ONB labels), **ood-evaluator** (Level 4 cross-lab generalization) | **seminar-prompt-builder** (Phase manuscript → Claude Design prompt.md, 슬라이드 발표 자료) |

`.claude/commands/` (현재 7 commands):

| Phase 1 (1개) | Phase 1.5 신규 (5개) | Cross-phase (1개) |
|---|---|---|
| /add-paper | /add-lab-source, /label-onb-lab, /ablate-phase1p5, /ood-eval, /draft-phase1p5-section | **/build-seminar-prompt** (Claude Design 용 발표 prompt) |

호출 예: "paper-card-extractor 에이전트로 이 PDF 카드 만들어줘", "/ood-eval --mode lab-as-ood".

## 작업 시 참고

- 새 논문이 들어오면 먼저 `01_survey/paper_database.md`에 카드 추가 (Phase 1) 또는 `phase1p5_inhouse_augmentation/manuscript/references.bib` (Phase 1.5).
- 새 외부 데이터셋은 `02_data/raw/`에 출처별 분리.
- 새 lab 데이터는 `phase1p5_inhouse_augmentation/data/raw/lab/<source>/` (Phase 1.5).
- 모델 변경 시 반드시 새 YAML config 추가 (재현성). Phase 1: `03_model/configs/`, Phase 1.5: `phase1p5_inhouse_augmentation/experiments/configs/`.
- Figure는 phase 별 `analysis/figures/`. 논문 EPS/PDF는 phase 별 `manuscript/figures/`.
- **발표 자료**:
  - Phase 별 자료 (학회·세미나·포스터·보고서·outreach·abstract) → `phase*/presentations/`
  - Cross-phase 자료 (워크스페이스 overview, 기금 통합 보고, lab meeting, 학위논문 발표) → root `presentations/`
  - **Final PDF (`.pdf`) + Markdown 만 git commit**, editable source (`.pptx`, `.docx` 등)는 외부 보관 (`.gitignore` 적용됨).
- Stage 2 마이그레이션 후에는 `shared/src/pinn_onb/` 와 phase별 `experiments/`, `analysis/`, `manuscript/` 구조로 통일.

## 참조 문서

- Phase 1 계획서: `ONB_PINN_Phase1_Pool_Boiling_Plan.md`
- Phase 1.5 계획서: `phase1p5_inhouse_augmentation/plan.md`
- Phase 2 계획서: `phase2_flow_boiling/plan.md`
- 컴퓨터 매핑: `HOSTS.md`
- 다중 컴퓨터 운영 가이드: `claude-code-multi-project-guide.md`
- 워크스페이스 구조 변경 결정: `WORKSPACE_RESTRUCTURE_PROPOSAL.md`
- 후속 연구 로드맵: `future_research_roadmap.md`
- 진척 상태: `PHASE_STATUS.md`
- Release 절차: `RELEASE_CHECKLIST.md`, `SETUP_GITHUB_ZENODO_GUIDE.md`
