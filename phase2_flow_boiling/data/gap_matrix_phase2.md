# Phase 2 갭 분석 매트릭스 — Flow Boiling ONB

**작성일**: 2026-05-21
**작성자**: gap-matrix-mapper (Phase 2 메타분석 에이전트)
**최종 갱신**: 2026-05-21 (Round 3 반영, 49편 기준)
**기반 자료**:
- `data/raw/paper_database_phase2.md` — 등록 카드 49편 (Round 1: 21편 + Round 2: 23편 + Round 3: 5편)
- `data/raw/survey_candidates_phase2.md` — Round 1 후보 21편
- `data/raw/survey_candidates_phase2_round2.md` — Round 2 후보 27편
- `data/raw/survey_candidates_phase2_round3.md` — Round 3 후보 9편
- `plan.md` §2.2 — 예비 갭 매트릭스 참조

---

## 매트릭스 설계

**행 (접근 방법)**: 경험식 | CFD/DNS | Pure ML | PINN | 본 연구(Phase 2)
**열 (커버리지 차원)**: 단일 유체 | 다중 유체 | 단일 채널 기하 | 복합 채널 기하 | 표면 개질 효과 | 표면 × 유속 복합

**범례**:
- ★★★ 충분 — 해당 셀을 다루는 문헌 5편 이상, 서로 다른 유체·기하 조건에서 교차 검증됨
- ★★  보통 — 2~4편, 단일 조건 또는 한정된 범위에서만 검증됨
- ★   부족 — 1편, 개념 증명 수준 또는 간접 증거만 존재
- -   결여 — 해당 조건을 직접 다룬 문헌 없음

*셀 표기 형식*: 기호 (대표 문헌 ID 또는 그룹명)

---

## 갭 분석 매트릭스

|  | C1. 단일 유체 | C2. 다중 유체 | C3. 단일 채널 기하 | C4. 복합 채널 기하 | C5. 표면 개질 효과 | C6. 표면 × 유속 복합 |
|---|---|---|---|---|---|---|
| **R1. 경험식** | ★★★ (Bergles&Rohsenow 1964, Davis&Anderson 1966, Hsu&Graham 1976, Basu 2002, LIU2005, FORREST2016) | ★★ (Kandlikar 1991 — 물+냉매 10종; CONDEFONTENLA2024 — 6종 유체 통합 상관식) | ★★★ (Bergles 1964, Davis 1966, Basu 2002, Hsu&Graham 1976, FORREST2016, LIU2005) | ★★ (Basu 2005b, Saitoh 2007 D=0.5–11 mm, QINETAL2025 D_h+종횡비) | ★★ (Basu 2002 θ, FORREST2016 산화, VONTAS2021 θ×유동, ROUGHNARROW2024 Ra) | - |
| **R2. CFD/DNS** | ★ (Jin 2021 NSFnet 비압축 NS) | - | ★★ (Jin 2021 채널, Cai 2021 공역 열전달) | - | - | - |
| **R3. Pure ML** | ★ (Anonymous 2025 R513A — HTC 예측) | - | ★ (Anonymous 2025 마이크로핀 튜브 단일 형상) | - | - | - |
| **R4. PINN** | ★★ (Jalili 2024a 이상유동, Jalili 2025 막비등, Schiassi 2023 원자로) | ★ (Jalili 2024b = JALILI2024b — 물·R-134a·FC-72 전이학습) | ★★ (Jalili 2024a, JALILI2024b, Jalili 2025, Anonymous 2025) | - | - | - |
| **R5. 본 연구 (Phase 2)** | ★★★ (계획: 물·R-134a·R-1234yf, 단일 유체 각각 검증) | ★★★ (계획: 물+R-134a+R-1234yf 통합 무차원 manifold) | ★★★ (계획: 원형관·직사각 채널 단일 형상 baseline) | ★★★ (계획: D_h 50 μm–3 mm, 마이크로/미니/일반 채널) | ★★★ (계획: Ra·θ·산화 상태 Surface Encoder 통합) | ★★★ (계획: Dual-FiLM — 표면 z_s × 유동 Re/G/Bo 동시 조건화) |

---

## 셀별 근거 상세 (카운트 및 문헌 목록)

### R1. 경험식 행

| 열 | 카운트 | 해당 문헌 |
|---|---|---|
| C1 단일 유체 | 9 | Bergles&Rohsenow(1964), Davis&Anderson(1966), Hsu&Graham(1976), Basu(2002), Basu(2005a), Basu(2005b), LIU2005(물), FORREST2016(물), Kandlikar(1991) 포함 시 단일 유체 각각 |
| C2 다중 유체 | 2 | Kandlikar(1991) — 유동비등 맵에서 물·냉매 10종 이상 통합; CONDEFONTENLA2024 — 물·R-113·R-12·R-22·R-134a·FC-72 6종 ONB incipience 통합 리뷰 + 무차원 상관식 |
| C3 단일 채널 기하 | 6+ | Bergles(1964) 원형관, Davis(1966) 일반관, Basu(2002) 수직관, Hsu&Graham(1976) 기본 채널, FORREST2016 협소채널, LIU2005 마이크로채널 |
| C4 복합 채널 기하 | 4 | Basu(2005b) 다조건 검증, Saitoh(2007) 0.5–11 mm, Kandlikar(1991) 다관경, QINETAL2025 D_h+종횡비 복합 |
| C5 표면 개질 | 4 | Basu(2002) 접촉각 θ, FORREST2016 산화 처리, VONTAS2021 θ=26°~104° 마이크로채널 유동비등, ROUGHNARROW2024 Ra=0.34–2.5 μm 좁은 채널 |
| C6 표면×유속 | 0 | 없음 (VONTAS2021이 θ+유동 결합에 가장 근접하나, 표면 형상(Ra, 마이크로구조)과 Re/G 동시 입력 모델 없음) |

### R2. CFD/DNS 행

| 열 | 카운트 | 해당 문헌 |
|---|---|---|
| C1 단일 유체 | 1 | Jin(2021) NSFnet 비압축 NS(물 가정) |
| C2 다중 유체 | 0 | 없음 |
| C3 단일 채널 기하 | 2 | Jin(2021) 채널 유동, Cai(2021) 공역 열전달 단일 형상 |
| C4 복합 채널 기하 | 0 | 없음 |
| C5 표면 개질 | 0 | 없음 |
| C6 표면×유속 | 0 | 없음 |

### R3. Pure ML 행

| 열 | 카운트 | 해당 문헌 |
|---|---|---|
| C1 단일 유체 | 1 | Anonymous(2025) R513A 마이크로핀 튜브 HTC/압력강하 ML |
| C2 다중 유체 | 0 | 없음 |
| C3 단일 채널 기하 | 1 | Anonymous(2025) 마이크로핀 튜브 단일 형상 |
| C4 복합 채널 기하 | 0 | 없음 |
| C5 표면 개질 | 0 | 없음 |
| C6 표면×유속 | 0 | 없음 |

### R4. PINN 행

| 열 | 카운트 | 해당 문헌 |
|---|---|---|
| C1 단일 유체 | 3 | Jalili(2024a) 이상유동, Jalili(2025) 막비등, Schiassi(2023) 원자로(물) |
| C2 다중 유체 | 1 | JALILI2024b (물·R-134a·FC-72 전이학습) |
| C3 단일 채널 기하 | 4 | Jalili(2024a), JALILI2024b, Jalili(2025), Anonymous(2025) — 각 논문 단일 형상 |
| C4 복합 채널 기하 | 0 | 없음 |
| C5 표면 개질 | 0 | 없음 |
| C6 표면×유속 | 0 | 없음 |

---

## 주요 갭 서술

### 1. 다중 유체 + 경험식 조합 — 기존 제한적 커버 (C2 × R1: ★★)

49편 서베이 기준, CONDEFONTENLA2024(물·R-113·R-12·R-22·R-134a·FC-72 6종 통합 리뷰)와 Kandlikar(1991)(유동비등 맵)로 ★ → ★★로 갱신됐다. 그러나 R-1234yf·R-32 같은 최신 HFO 냉매의 직접 ONB incipience 데이터(강제대류 조건)는 여전히 없음 — 본 연구의 refrigerant 확장성이 차별화 포인트다. 물·R-134a·R-1234yf를 동시에 커버하면서 ONB 벽면 과열도를 직접 예측하는 PINN은 현재 없다.

### 2. 복합 채널 기하 차원의 전면적 공백 (C4: 경험식 ★★ 이상인 열 없음)

C4(복합 채널 기하)는 경험식 행에서만 ★★를 보이고, CFD/DNS·Pure ML·PINN 행은 모두 결여(-)다. 직경 범위를 D_h 50 μm~수 mm로 연속 변수화하여 하나의 모델로 커버하는 연구가 전무하다. 본 연구는 D_h와 Bo_conf를 명시적 입력으로 삼아 이 공백을 채운다.

### 3. 표면 개질 × 강제대류 ONB 연구 — 경험식 수준에서 증거 확보 (C5 × R1: ★★, 나머지 행 모두 -)

49편 서베이 기준, C5(표면 개질 효과)는 4편으로 확장: Basu 2002(θ), FORREST2016(산화), VONTAS2021(θ=26°~104° 마이크로채널), ROUGHNARROW2024(Ra=0.34~2.5 μm 좁은 채널). 경험식 행은 ★★ 유지. CFD·ML·PINN 행은 여전히 모두 결여. 이 4편의 실험 데이터가 Phase 2 Surface Encoder(Ra, θ 입력)의 학습 근거를 제공하며, 강제대류 ONB에 Surface Encoder를 결합하는 본 연구가 ML/PINN 행에서 최초 기여가 된다.

### 4. 표면 × 유속 복합(C6)은 모든 기존 접근법에서 완전 결여 (전체 행 -)

C6(표면 개질과 유동 파라미터의 동시 영향)를 정량화한 연구는 survey 21편 전체에서 한 편도 없다. Basu(2002)가 θ + Re를 일부 결합했으나 표면 형상(Ra, 마이크로구조)과 Re/G/Bo를 동시에 입력으로 사용하는 데이터 기반 모델은 존재하지 않는다. 본 연구의 Dual-FiLM conditioning이 이 셀의 유일한 기여자가 된다.

### 5. PINN의 유동비등 ONB 직접 예측 부재 (C1~C6 × R4에서 ONB-specific 0편)

PINN 행의 4편(Jalili 2024a/b, Jalili 2025, Anonymous 2025)은 모두 열전달계수나 기포 성장을 예측하며, ONB 벽면 과열도(ΔT_ONB)를 직접 출력으로 삼는 PINN은 현재 없다. 본 연구는 flow-aware Hsu 손실항(L_Hsu_flow)을 명시적으로 구현하는 첫 번째 유동비등 ONB PINN이 된다.

---

## Phase 1 갭 매트릭스와의 비교

| 비교 항목 | Phase 1 (풀비등 ONB) | Phase 2 (유동비등 ONB) | 이동 시 드러나는 신규 갭 |
|---|---|---|---|
| 데이터 풍부도 | 외부 corpus 82 ONB 포인트 확보 | survey 21편 기준 가용 포인트 수백~수천 추정 (디지타이즈 미완료) | 데이터 디지타이즈 규모가 Phase 2 진전의 병목 |
| 경험식 커버리지 | 단일/다중 유체 ⚠️(Phase 1 매트릭스 기준) | 단일 유체 풍부(★★★), 다중 유체 희박(★) | 다중 유체 경험식 전무 — Phase 1보다 심각한 공백 |
| CFD/DNS | 공동 특성 역추정 CFD 일부 존재 | 단일 유체 단일 형상만 존재(★) | 강제대류 조건 CFD 연구 수가 풀비등보다 적음 |
| ML/Pure ML | Phase 1에서 거칠기·젖음성 ML ⚠️ | 유동비등 ML 1편(Anonymous 2025) | 강제대류 ONB 전용 Pure ML 연구 사실상 없음 |
| PINN | Phase 1 본 연구가 첫 사례 | PINN 4편 존재하나 ONB-specific 없음 | 유동비등 ONB에 PINN을 적용한 선행 연구 없음 |
| 표면 개질 × 방법론 | Phase 1 전 행에서 공백 확인 | 동일한 공백 + 유속 차원 추가 → 더 깊은 공백 | C6(표면×유속)가 Phase 2 고유의 신규 갭 차원 |
| 복합 채널 기하 | Phase 1에서 원형관/평판 두 형상만 고려 | D_h 연속 변수화 필요 | 채널 기하를 연속 변수로 처리하는 연구 부재 |

**핵심 전환**: Phase 1에서 "표면 × 방법론" 갭이 존재했다면, Phase 2에서는 "표면 × 유속 × 방법론" 3차원 갭으로 확장된다. 이는 연구의 새로운 기여 차원(C6)이 Phase 1에서는 정의조차 되지 않았던 차원임을 의미한다.

---

## 데이터 갭 분석

survey_candidates_phase2.md 21편 기준으로 각 조건별 ONB 데이터 가용성을 평가한다.

### 풍부한 데이터 조건
- **물, 원형관, 대기압 근처**: Bergles(1964), Davis(1966), Basu(2002), Kandlikar(1991) 등 다수 — 수백 포인트 추정, 디지타이즈 가능
- **물, 마이크로채널 (실리콘 기판)**: LIU2005 — 약 15~30 ONB 포인트 (단, 단일 기하)
- **물, 협소 채널, 고질량유속**: FORREST2016 — G=750~3000 kg/m²s, ΔT_sub=10~45°C (포인트 수 원문 확인 필요)

### 부족한 데이터 조건
- **R-134a / R-1234yf 유동비등 ONB 포인트**: Saitoh(2007)는 HTC 데이터 위주, ONB 직접 라벨 불명확. 냉매 유동비등 ONB 데이터는 탐색 필요
- **마이크로채널 + 표면 개질 동시 조건**: LIU2005는 실리콘 native surface만, 표면 처리 변수 없음. FORREST2016은 협소채널이나 표면 산화만 다룸
- **수평 유동 방향 ONB**: survey 21편 대부분 수직 상향 또는 유동 방향 미명시. 수평 채널 ONB 데이터 부재
- **D_h < 300 μm 마이크로채널 ONB**: LIU2005가 유일하며 단일 기판(실리콘) 에 국한
- **고압 조건 (P > 1 MPa) ONB**: FORREST2016이 MTR 조건이나 정확한 압력 미명시. P ↑ → ΔT_ONB ↓ 트렌드 검증용 다중 압력 데이터 없음
- **표면 Ra + θ + 유동 동시 측정 데이터**: survey 전체에서 한 편도 없음 (FORREST2016은 θ만 변화, LIU2005는 표면 정보 없음)

### 데이터 확보 우선순위 (정량 목표: 총 300+ ONB 포인트)

| 우선순위 | 논문 | 예상 ONB 포인트 | 조건 |
|---|---|---|---|
| 1 | Basu et al. (2002) 디지타이즈 | ~30–50 | 물, 수직관, θ 포함 |
| 2 | Kandlikar (1991) 맵 경계선 | ~50–100 | 물+냉매, 다중 유속 |
| 3 | Bergles & Rohsenow (1964) | ~20–30 | 물, 원형관, 대기압 |
| 4 | FORREST2016 디지타이즈 | ~20–40 | 물, 협소채널, G=750–3000 |
| 5 | Basu (2005a) 열유속 분배 | ~20–30 | 물, 수직관, 과냉도 가변 |
| 6 | Lee & Mudawar (2008) | ~15–25 | 냉매, 마이크로채널 |

---

## 다음 서베이 우선순위

### Phase 2 M1 기간 중 추가 탐색 필요 논문 유형

**유형 A — 다중 냉매 유동비등 ONB 실험 (최우선)**

탐색 키워드: `"onset of nucleate boiling" "R-134a" OR "R-1234yf" "flow boiling" "correlation"`
이유: C2(다중 유체) 열이 경험식 ★, PINN ★에 불과. 냉매 기반 유동비등 ONB 실험 데이터가 절대적으로 부족.
추천 저자 그룹: Thome (EPFL), Dario (Kandlikar의 미니채널 냉매 확장), Kim & Mudawar

**유형 B — 표면 개질 + 강제대류 ONB 실험 (2순위)**

탐색 키워드: `"surface modification" OR "roughness" OR "wettability" "flow boiling" "onset" "nucleate boiling"`
이유: C5(표면 개질) × 모든 방법론 행에서 ★★ 이상인 셀이 경험식 행 하나뿐.
추천 저자 그룹: Jo et al. (친수/소수 복합 표면), Surt & Calame (roughness + flow), UNIST ITE Lab 내부 실험

**유형 C — 복합 채널 기하 / D_h 연속 변수 ONB 실험 (3순위)**

탐색 키워드: `"hydraulic diameter" "onset nucleate boiling" "mini-channel" OR "microchannel" "confinement"`
이유: C4(복합 채널 기하) × CFD/PINN 행 전체 결여(-). D_h를 연속 파라미터로 처리한 ONB 데이터셋 부재.
추천 논문: Bertsch et al. (2009) IJHMT 52, 2110–2118, Harirchian & Garimella (2012)

**유형 D — 수평 유동 방향 ONB 실험 (4순위)**

탐색 키워드: `"horizontal flow boiling" "onset of nucleate boiling" "subcooled"`
이유: 유동 방향이 ONB에 미치는 영향 데이터 전무. plan.md §1.5에서 수평·수직 상향·수직 하향을 포함 범위로 명시했으나 현재 survey는 수직 상향 위주.
추천 저자 그룹: Kandlikar (horizontal flow nucleation), Bowring (NATO reactor 수평관)

**유형 E — 고압 조건 ONB 실험 (5순위, 원자력 응용 대비)**

탐색 키워드: `"subcooled flow boiling" "onset nucleate boiling" "high pressure" "PWR" OR "BWR"`
이유: P > 1 MPa 영역 ΔT_ONB 트렌드 검증 데이터 부재. plan.md §5.1 Level 3 검증 항목(P↑→ΔT_ONB↓) 확인 필요.
추천 논문: Sato & Matsumura (1964), Frost & Dzakowic (1967), 원자력 분야 Griffith & Wallis

---

## 갱신 이력

| 날짜 | 분석 논문 수 | 변경 내용 | 담당 |
|---|---|---|---|
| 2026-05-21 | 24편 (등록 3 + 후보 21) | 초기 매트릭스 생성 (5 × 6 셀, 전체 셀 값 최초 부여) | gap-matrix-mapper (Phase 2) |
