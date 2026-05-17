# PINN-ONB01 — Pool Boiling ONB Prediction (Phase 1)

PINN을 이용한 풀비등 핵비등 개시점(ONB, Onset of Nucleate Boiling) 예측 연구.
1단계: 풀비등(표면 개질 효과 중심), 2단계(후속): 강제대류 비등.

## 연구 컨텍스트

- **분야**: 비등 열전달, 표면 공학, Physics-Informed Neural Networks
- **핵심 물리**: 풀비등 핵생성, Hsu 기준, 자연대류 경계조건
- **프레임워크**: PyTorch + DeepXDE
- **데이터**: 문헌 실험 + 합성(2D 열전도 해석)
- **유체**: 물(대기압 기본), FC-72/HFE-7100(비교)
- **가열 형상**: 수평 평판(상면), 수평 원형관 외면

## 폴더 구조

```
01_survey/        문헌 서베이 — 논문 카드, 갭 매트릭스
02_data/          데이터 — raw(literature/experiment/synthetic), processed, surface_cards
03_model/         PINN 소스 — src, configs, checkpoints, experiments
04_analysis/      분석 — figures, tables, scripts, validation_report.md
05_manuscript/    논문 원고 — main.tex, references.bib, supplementary
.claude/          서브에이전트, 슬래시 명령
```

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

무차원 변수는 접미 `_star` (예: `delta_T_star`, `q_star`, `r_star`).
무차원화 함수는 `utils/nondim.py`에 집중한다.

## 코딩 규칙

- Python 3.10+, **type hints 필수** (`from __future__ import annotations`).
- SI 단위 기본, 입력 단위가 다르면 즉시 변환.
- 물성치는 **CoolProp**으로 계산 (REFPROP 대체 가능).
- PyTorch dtype은 `torch.float32` 기본, 정밀 검증 시 `float64`.
- 콜로케이션 포인트 샘플링은 LHS(Latin Hypercube Sampling) 사용.
- 모든 손실 항목은 `loss_functions.py`에 1:1 함수로 분리 (디버깅 용이).
- 학습 로그는 MLflow(`03_model/experiments/`)에 기록.

## 도메인 지식 — 기억해 둘 사실

- **ΔT_ONB 물리적 범위** (물, 대기압): 2~30 °C. 이 범위를 벗어나면 데이터/예측 오류 의심.
- **r_c 활성 공동 크기**: 1 < r_c < 100 μm. SEM/AFM 측정과 비교.
- **물리적 경향성** (검증 시 필수 확인 5개):
  1. **q'' ↑ → ΔT_ONB ↑** — Hsu/Sato-Matsumura 공식 `ΔT_ONB ∝ √q''`. 단일 표면 boiling curve의 ΔT_wall 도 q와 함께 단조 증가. (이전 spec은 ↓로 기재됐으나 ↑가 정답.)
  2. Ra ↑ → ΔT_ONB ↓ — 거친 표면일수록 더 작은 r_c 활성 cavity 존재 → 더 낮은 wall 과열도에서 ONB. **단, water 데이터셋은 표면개질(BETZ 매끈+코팅 vs JONES 거친+비처리)이 confounding으로 작용해 +상관도 보임. 깨끗한 Ra 효과는 R-134a/R-123 (JABARDO Cu) 데이터에서 관찰 (-0.7 ~ -0.5).**
  3. θ ↑ (소수성) → ΔT_ONB ↓ — Basu et al. F(θ) 의존성.
  4. P ↑ → ΔT_ONB ↓ — Bergles-Rohsenow 경험식. 압력↑ → 기포 직경↓.
  5. ΔT_sub ↑ → ΔT_ONB ↑
- **기존 상관식 비교 대상** (필수): Hsu(1962), Davis-Anderson(1966), Bergles-Rohsenow(1964), Basu et al.(2002).

## 단계별 산출물 책임

| 단계 | 기간 | 폴더 | Go/No-Go 기준 |
|-----|------|------|---------------|
| ① 서베이 | M1-2 | `01_survey/` | 갭 존재 확인 |
| ② 데이터 | M3-4 | `02_data/` | ONB 포인트 100개 + 표면 유형 10종 |
| ③ 모델링 | M5-7 | `03_model/` | 합성 데이터에서 상관식 동등 이상 |
| ④ 검증 | M8-9 | `04_analysis/` | 통계적으로 유의한 개선 |
| ⑤ 문서화 | M10-12 | `05_manuscript/` | IJHMT 투고 |

## 서브에이전트 / 슬래시 명령

`.claude/agents/`에 단계별 서브에이전트 정의가 있다.
호출 예: "paper-card-extractor 에이전트로 이 PDF 카드 만들어줘"

`.claude/commands/`의 슬래시 명령은 위 에이전트들을 묶어서 호출한다.

## 작업 시 참고

- 새 논문이 들어오면 먼저 `01_survey/paper_database.md`에 카드 추가.
- 새 데이터셋은 `02_data/raw/`에 출처별 분리, 전처리 후 `02_data/processed/`로.
- 모델 변경 시 반드시 `03_model/configs/`에 새 YAML 추가 (재현성).
- Figure는 `04_analysis/figures/`에 PNG, `05_manuscript/figures/`에 EPS/PDF.

## 참조 문서

- 연구 계획서 원본: `ONB_PINN_Phase1_Pool_Boiling_Plan.md`
