# `shared/` — Cross-phase shared assets

본 폴더는 **PINN-BOILING workspace**의 모든 phase (Phase 1, 1.5, 2, ...) 가
공통으로 사용하는 자산을 보관한다.

## 구성

```
shared/
├── src/pinn_onb/    Python package — PINN architecture, loss, training,
│                    correlations, utils, inference. `pip install -e ./src/`
│                    로 각 phase 환경에 editable 설치.
├── docs/            모든 phase 공유 기술 문서 — ARCHITECTURE, DATA_SCHEMA,
│                    MEASUREMENT_GUIDE 등.
└── templates/       빈 양식 — new_experiment_template.csv,
                     surface_card_template.yaml, paper_card_template.md.
```

## 현재 상태 (Stage 1 — 2026-05-19)

`shared/src/pinn_onb/` 는 **빈 패키지 skeleton 상태**. Phase 1 실제 코드는
여전히 `phase1_pool_boiling/03_model/src/` (Stage 2 마이그레이션 시 이동
예정) 또는 workspace root의 `03_model/src/` (현재 위치)에 있다.

Phase 1.5 작업 시 임시로 다음 두 가지 import 전략 중 선택:

### Option A: sys.path 임시 주입 (Stage 1 동안)

```python
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[N]  # workspace root까지
sys.path.insert(0, str(ROOT / "03_model" / "src"))
from model.pinn import PoolBoilingPINN
```

### Option B: shared/src/pinn_onb/__init__.py 가 re-export (Stage 1 후반)

```python
# shared/src/pinn_onb/__init__.py 에서 root/03_model/src 를 import path 추가
import pinn_onb
from pinn_onb.model import PoolBoilingPINN  # cleaner
```

→ Stage 2 (Phase 1 수락 후) 에서 실제 코드를 shared/src/ 로 이동하면
   Option B 자동 정상화.

## Stage 2 마이그레이션 시점 작업

1. `mv 03_model/src/{model,loss,training,utils}/* shared/src/pinn_onb/`
2. `04_analysis/scripts/correlation_comparator.py` 의 함수들 →
   `shared/src/pinn_onb/correlations/`
3. `04_analysis/scripts/predict_new_experiment.py` →
   `shared/src/pinn_onb/inference/`
4. `02_data/raw/experiment/MEASUREMENT_GUIDE.md` → `shared/docs/`
5. `02_data/raw/experiment/new_experiment_template.csv` → `shared/templates/`
6. import 문 일괄 갱신 (`sed -i`)
7. Smoke test (Phase 1 figures 재생성)
8. `git tag shared-v1.0` + `git tag phase1-v1.0-published`

자세한 절차: `WORKSPACE_RESTRUCTURE_PROPOSAL.md` § 6.

## 라이선스

- 본 폴더의 코드: workspace root `LICENSE-CODE` (MIT)
- 본 폴더의 데이터/템플릿: workspace root `LICENSE-DATA` (CC-BY-4.0)

## 책임자

- Maintainer: Jaeseon Lee `<JaeseonLee@unist.ac.kr>`
- ORCID: 0000-0003-1996-6086
