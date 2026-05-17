# PINN-ONB01

PINN 기반 풀비등 ONB 예측 연구 — 1단계 (표면 개질 효과 중심).

## 빠른 시작

```bash
# 환경 설정 (예시 — 실제 환경은 03_model/ 정착 후 갱신)
python -m venv .venv && source .venv/bin/activate
pip install torch deepxde coolprop mlflow optuna numpy pandas matplotlib scikit-learn
```

## 폴더

| 경로 | 내용 |
|------|------|
| `01_survey/` | 문헌 서베이 — 논문 카드, 갭 매트릭스 |
| `02_data/` | 데이터 — raw, processed, surface_cards |
| `03_model/` | PINN 소스 — src, configs, checkpoints |
| `04_analysis/` | 분석 — figures, tables, scripts |
| `05_manuscript/` | 논문 원고 |
| `.claude/` | Claude Code 서브에이전트 + 슬래시 명령 |

## 연구 계획

자세한 계획은 [`ONB_PINN_Phase1_Pool_Boiling_Plan.md`](./ONB_PINN_Phase1_Pool_Boiling_Plan.md) 참조.

## 단계별 진행

1. **M1-2 서베이** — 풀비등 ONB + 표면 개질 논문 50편 카드화, 갭 분석
2. **M3-4 데이터** — 문헌 디지타이징, 합성 데이터 생성, 전처리 파이프라인
3. **M5-7 모델링** — Surface Encoder + PINN 구현, Phase 1-3 학습
4. **M8-9 검증** — 3계층 검증, 불확실도 정량화, 역문제
5. **M10-12 논문** — 초안, 수정, IJHMT 투고

## Claude Code 활용

```bash
# 서브에이전트 직접 호출 예시
"paper-card-extractor로 이 PDF 카드 만들어줘"
"loss-function-builder로 Hsu 기준 손실함수 구현해줘"
"figure-composer로 parity plot 만들어줘"
```
