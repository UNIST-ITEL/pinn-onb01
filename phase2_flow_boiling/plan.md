# PINN 기반 핵비등 개시점(ONB) 예측 연구 계획서
# 2단계: 강제대류 비등(Flow Boiling) — 표면 + 유동 복합 효과

**작성일**: 2026-05-18
**선행 단계**: 풀비등 ONB PINN (Phase 1, 2026-05 IJHMT 투고 완료)
**예상 기간**: 12-15개월
**대응 후속 주제**: future_research_roadmap.md A1

---

## 1. 연구 개요

### 1.1 Phase 1 결과 요약 (출발점)

| 항목 | Phase 1 달성치 |
|------|---|
| 본문 길이 | 35페이지, 7,371 단어 (IJHMT 적정 범위) |
| 데이터셋 | 1,361 boiling 포인트 + 82 ONB 라벨 (49 surfaces, 7 sources, 4 fluids) |
| 모델 | FiLM-conditioned PINN, **24,005 parameters** |
| 학습 시간 | ~17-20분 (Apple M1 CPU) |
| 메인 성능 | **RMSE 3.42 K, R² +0.44** (n=77) — Basu 대비 −53% |
| 냉매 성능 | RMSE **1.18 K** (R-134a) / **2.35 K** (R-123) — 65~67% 개선 |
| 검증 | Level 1 4/4, Level 3 8/9 PASS, ensemble coverage 98.7% |
| 신규 발견 | Simpson-type reversal in R_a–r_c (열역학적 스케일링 효과) |
| Open-source | Dataset + 모델 + 스크립트 GitHub 공개 약속 |

### 1.2 Phase 1 → Phase 2 전이 로드맵

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│  1단계 (완료)                          2단계 (본 계획서)             │
│  ──────────────                       ────────────────               │
│  풀비등 ONB                            강제대류 비등 ONB             │
│  ├─ 평판 / 원형관                      ├─ 미니/마이크로채널          │
│  ├─ 정지 유체                          ├─ 강제 유속 G                │
│  ├─ 자연대류 BC                        ├─ Reynolds, Bo, We           │
│  ├─ 표면 개질 효과 + Hsu               ├─ 표면 + 유동 복합 효과      │
│  └─ 1D 정상 상태 열전도                └─ NS + 에너지 연성 (2D)      │
│                                                                      │
│  물리: 열전도 + h_nc(Ra, Pr)           물리: NS + 에너지 완전 연성   │
│  콜로케이션: 2,000 LHS                 콜로케이션: 50,000-200,000    │
│  손실 5항                              손실 6-8항 (NS / energy 추가) │
│  난이도: ★★☆                          난이도: ★★★                  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 1.3 본 연구의 핵심 동기

```
산업·학술적 필요성:
  ├─ 전자장비 양상 냉각 (microchannel cooling) — 강제대류 ONB 정밀 예측 필요
  ├─ 원자력 reactor safety — 강제대류 subcooled boiling 영역의 DNB margin
  ├─ HVAC evaporator design — multi-tube refrigerant boiling
  └─ 기존 강제대류 ONB 상관식 (Hsu-Graham, Kandlikar, Sato-Matsumura) 모두
     surface-specific calibration 의존 — PINN으로 보편화

Phase 1 자산을 활용한 이점:
  ├─ Surface Encoder 모듈 재사용 (49 surface cards)
  ├─ Hsu nucleation 항 그대로 유지 (boundary layer thickness 정의만 변경)
  ├─ Monotonicity regularizers 그대로 (R_a↓, θ↓ 트렌드)
  ├─ Deep ensemble UQ 인프라 재사용
  └─ Open-source dataset의 cross-fluid manifold 활용 → cold-start 회피
```

### 1.4 연구 목표

| 구분 | 목표 | 정량 기준 |
|------|------|----------|
| 1차 | Flow boiling ONB 벽면 과열도 예측 PINN 개발 | RMSE ≤ 5 K on 다중 유체/유속 |
| 2차 | 표면 × 유동 복합 효과 분리 (Reynolds, Bo, 표면 개질) | Spearman ρ 5-trend |Pr≥|0.7| |
| 3차 | Phase 1 모델 전이학습 효과 정량화 | from-scratch 대비 학습 시간 −50%, RMSE −20% |
| 4차 | 유동 instability 영역 (vapor confinement) ONB localization | Multi-channel/single-channel 비교 |

### 1.5 연구 범위

```
포함하는 범위:
  ├─ 강제대류 subcooled boiling ONB
  ├─ 채널 형상
  │    ├─ 원형관 내부 (D > 1 mm)
  │    ├─ 사각/직사각 미니채널 (D_h: 0.5-3 mm)
  │    └─ 마이크로채널 (D_h: 50-500 μm)
  ├─ 유동 방향
  │    ├─ 수직 상향
  │    ├─ 수평
  │    └─ 수직 하향 (제한)
  ├─ 표면 개질 (Phase 1 49 cards 일부 재활용 + 신규 추가)
  ├─ 작동 유체: 물, R-134a, R-1234yf, FC-72, HFE-7100
  ├─ 압력: 0.1~5 MPa
  ├─ 유속(질량 유속 G): 50-3000 kg/m²s
  └─ 과냉도 ΔT_sub: 0-50 K

제외하는 범위:
  ├─ Saturated/superheated flow boiling (ONB 후 영역)
  ├─ CHF/DNB 임계열유속
  ├─ Two-phase pressure drop (별도 주제)
  ├─ 다성분 혼합물 (oil-refrigerant 등)
  └─ Cryogenic flow boiling (→ 3단계 후보)
```

---

## 2. 문헌 서베이

### 2.1 Phase 1 대비 신규 서베이 필요 영역

```
신규 추가:
  ├─ Flow boiling ONB classical correlations
  │    ├─ Sato-Matsumura (1964) — Phase 1과 동일 식, 단 다른 BC
  │    ├─ Kandlikar (1991, 2006) — flow boiling 범용 식
  │    ├─ Hsu-Graham (1976) — 강제대류 확장
  │    └─ Basu et al. (2002, 2005) — wettability + 유속 결합
  ├─ Microchannel-specific
  │    ├─ Bertsch et al. (2009) — laminar microchannel
  │    ├─ Lee-Mudawar 시리즈 (2005-2018) — micro/mini channel
  │    └─ Saitoh et al. (2007) — confinement effect
  ├─ Recent PINN/ML for flow boiling
  │    ├─ Jalili & Mahmoudi (2025, IJHMT) — film boiling [Phase 1 cited]
  │    ├─ Li & Kharangate (2025, ASME J HMT) — cryogenic CHF [Phase 1 cited]
  │    ├─ Huang et al. (2024, IJMF) — ML bubble visualization [Phase 1 cited]
  │    └─ 신규 대상: Sato et al., Yang et al., Park et al. 2024-2026
  └─ Computational
       ├─ Multiphase NS PINN — Jin et al. (2021), Hennigh et al. (2021)
       └─ Conjugate heat-transfer PINN — Cai et al. (2021), Ren et al. (2022)
```

### 2.2 갭 분석 매트릭스 (예상)

```
              ┌──────────┬───────────┬──────────────┬──────────────┐
              │ 단일유체 │ 다유체    │ 표면개질     │ 표면×유속    │
              │          │           │              │ 복합         │
┌─────────────┼──────────┼───────────┼──────────────┼──────────────┤
│ 경험식      │   ★★★   │    ★      │      ★       │      -       │
│ CFD/DNS     │   ★★    │    ★      │      ★       │      -       │
│ Pure ML     │   ★★    │    -      │      -       │      -       │
│ PINN        │   ★      │    -      │      -       │      -       │
│ 본 연구     │          │           │              │   ★★★        │
└─────────────┴──────────┴───────────┴──────────────┴──────────────┘
★★★: 충분  ★★: 보통  ★: 부족  -: 결여
```

Phase 1과 동일하게 **표면×유속 복합 영역이 비어있음**을 입증할 예정.

---

## 3. 데이터 확보 전략

### 3.1 데이터 소스 계층

```
A. 문헌 데이터 (즉시 확보, 6-12개월)
   ├─ 1st-tier: Kandlikar group 데이터 (1990-2010)
   │           ~300 ONB 포인트, 다중 유체
   ├─ 2nd-tier: Mudawar group (mini/microchannel)
   │           ~200 ONB 포인트, R-134a/HFE
   ├─ 3rd-tier: Jacobi, Thome, Cheng 등
   │           ~150 ONB 포인트
   └─ 목표: 600+ flow boiling ONB 포인트

B. Phase 1 데이터 재활용
   ├─ Surface cards 49장 → 50% 정도 재활용 (유사 가공법/재질)
   └─ Hsu 기반 r_c 라벨 → 동일 사용

C. 합성 데이터 (CFD/PINN bootstrap)
   ├─ ANSYS Fluent 또는 OpenFOAM 단순 case
   │    ├─ 균일 유속 + 균일 가열 채널
   │    ├─ Reynolds 범위 100-10000
   │    └─ 1000-2000 synthetic ONB 포인트
   └─ Phase 1 PINN으로 자연대류 case 보강 (cross-validation)

D. 실험 데이터 (외부 협력, 12-18개월)
   ├─ UNIST ITE Lab 내부 실험 가능성
   ├─ 외부 협력 (대학/연구소) — Phase 1 SEM/AFM 협력과 연계
   └─ ~50-100 in-house ONB 포인트 추가
```

### 3.2 Flow boiling ONB에 필요한 신규 측정 변수

| 변수 | 단위 | 측정/추정 방법 |
|------|------|--------------|
| G (mass flux) | kg/m²s | 직접 측정 |
| 유속 u | m/s | G/(ρL × Acs) |
| Re | — | ρL u D_h / μL |
| Bo (boiling) | — | q'' / (G hfg) |
| Bo_conf (confinement) | — | Lc / D_h |
| We (Weber) | — | ρL u² Lc / σ |
| ΔT_sub_inlet | K | T_sat − T_inlet |
| ΔT_sub_local | K | T_sat − T_local (ONB 위치) |
| L/D 비 | — | 채널 길이/직경 |
| 유동 방향 | — | 수직 상향/수평/수직 하향 |

위 변수 + Phase 1의 표면 변수 ({R_a, θ, r_c, N_s, paper category}) = 13-15 입력 차원

### 3.3 데이터 전처리 파이프라인 확장

```
Phase 1 단계 (재사용):
  ① WPD digitization
  ② SI 단위 변환
  ③ CoolProp 물성치 산출
  ④ Outlier 제거 (Hsu 범위 [2, 30] K)
  ⑤ 무차원화

Phase 2 추가:
  ⑥ Re/Bo/We 계산 (CoolProp 기반)
  ⑦ Channel geometry parsing (D_h 추출)
  ⑧ Flow direction encoding (categorical)
  ⑨ Inlet/local subcooling 분리
  ⑩ Onset location parameterization (x/L 위치 정규화)
```

---

## 4. PINN 모델링

### 4.1 강제대류 비등의 물리 — 지배방정식 단순화

```
완전한 2-phase 유동 비등 지배방정식:
  ┌─ Mass:      ∂ρ/∂t + ∇·(ρu) = 0
  ├─ Momentum:  ∂(ρu)/∂t + ∇·(ρuu) = -∇p + ∇·τ + ρg + σκδ
  ├─ Energy:    ∂(ρcpT)/∂t + ∇·(ρcpTu) = ∇·(k∇T) + Φ_dis + h_evap
  └─ Phase:     ∂α/∂t + u·∇α = Γ/ρ

Phase 2 단순화 가정:
  ├─ 정상 상태 (∂/∂t = 0)
  ├─ ONB 직전 단상 (single-phase 가정, α≈0)
  ├─ 비압축성 (ρ = const within liquid)
  ├─ 축대칭/2D 단면 (3D 무시 가능 채널)
  └─ Newton 점성 + Fourier 전도

→ Simplified PDEs:
  ⓐ Continuity: ∇·u = 0
  ⓑ Momentum:   ρ(u·∇)u = -∇p + μ∇²u
  ⓒ Energy:     ρcp(u·∇)T = k∇²T + Φ_dis
  ⓓ Hsu nucleation criterion: D_Hsu(δt, ΔTw, q'') ≥ 0
```

### 4.2 모델 아키텍처

```
                  ┌──────────────────────────┐
                  │  Surface descriptor      │
                  │  (Phase 1과 동일)         │
                  └────────────┬─────────────┘
                               ▼
                       ┌──────────────┐
                       │ Surface Enc  │  (Phase 1 가중치 초기화)
                       │   → z_s ∈ ℝ⁸ │
                       └──────┬───────┘
                              │
        Flow descriptor       │
        ┌──────────────────┐  │
        │ Re, G, Bo, We,   │  │
        │ ΔT_sub, D_h, dir │  │
        └────────┬─────────┘  │
                 ▼            ▼
            ┌────────────────────┐
            │ Conditioning fusion │
            │ (FiLM × 2 stages)  │  ← Surface + Flow 각각 별도 FiLM
            └────────┬───────────┘
                     ▼
        ┌─────────────────────────┐
        │  Main Backbone          │
        │  (Phase 1 transfer)     │
        │  6-7 hidden layers      │
        │  width 96-128           │
        │  tanh + GELU mix        │
        └───┬─────────────┬───────┘
            │             │
       ┌────▼─────┐  ┌────▼──────┐
       │ u, v, p  │  │ T, ΔT_ONB │
       │ velocity │  │ q''_ONB   │
       │ heads    │  │ heads     │
       └──────────┘  └───────────┘

총 파라미터: 약 60,000-80,000 (Phase 1의 24,005 대비 ~3x)
```

### 4.3 손실 함수 구성 (Phase 1의 5항 → Phase 2의 7-8항)

```
Phase 1 (5 terms):
  L = w_cond·L_cond + w_BC·L_BC + w_data·L_data
    + w_ONB·L_Hsu + w_mono·(L_mono,Ra + L_mono,θ)

Phase 2 (확장 7-8 terms):
  L = w_cont·L_continuity    (∇·u = 0)
    + w_mom·L_momentum       (NS residual)
    + w_eng·L_energy         (∇·(ρcpTu) - ∇·(k∇T) = Φ)
    + w_BC·L_BC              (inlet/outlet/wall BC)
    + w_data·L_data          (ONB labels + boiling curves)
    + w_ONB·L_Hsu_flow       (modified Hsu for boundary layer in flow)
    + w_mono·L_mono          (R_a, θ, Re-trend)
    + w_phys·L_consist       (energy balance closure)
```

### 4.4 Phase 1 → Phase 2 전이학습 (Critical 전략)

```
1. Pre-training (Phase 1 자산 활용):
   ├─ Surface Encoder 가중치 → Phase 2 초기값으로 freeze 후 fine-tune
   ├─ Hsu loss term 그대로 (boundary layer δt만 flow-aware로 변경)
   └─ Monotonicity regularizer 그대로

2. Warm-start training (Phase 2 stage 1):
   ├─ Phase 1 model의 boiling-curve regression 능력 활용
   ├─ Flow descriptor만 처음에 학습 (Surface frozen)
   └─ Adam 1000 epochs, lr=1e-3

3. Full fine-tuning (Phase 2 stage 2):
   ├─ 모든 가중치 unfreeze
   ├─ L_continuity, L_momentum, L_energy 활성화
   └─ Adam 5000 + LBFGS 2000

4. Inverse problem (Phase 2 stage 3):
   ├─ ONB 위치 (x_ONB/L) 역추정
   └─ Phase 1과 동일한 r_c 역추정 (재검증)

예상 효과:
  ├─ from-scratch 대비 학습 시간 50-60% 감소
  ├─ RMSE 20-30% 개선
  └─ Cross-fluid generalization 자동 상속
```

---

## 5. 분석 및 검증

### 5.1 검증 계층 (Phase 1과 동일 구조 + 추가)

```
Level 1: 코드 검증 (Phase 1 4개 + 신규 4개)
  ├─ V1-V4: Phase 1 그대로
  ├─ V5: Poiseuille flow (해석해)
  ├─ V6: Thermally developing pipe flow (Graetz 해)
  ├─ V7: Conjugate heat transfer (fin) 해석해
  └─ V8: Inlet/outlet BC consistency

Level 2: 합성 데이터 검증 (DNS or CFD 비교)
  ├─ ANSYS Fluent single-phase channel
  └─ OpenFOAM laminar/turbulent benchmark

Level 3: 물리적 일관성 (Phase 1 5 trend + 4 신규)
  ├─ Phase 1: q''↑→ΔT↑, R_a↑→ΔT↓, θ↑→ΔT↓, P↑→ΔT↓, ΔT_sub↑→ΔT↑
  ├─ Re↑ → ΔT_ONB↓ (강제대류 강화 → 단상 영역 확대)
  ├─ G↑ → ΔT_ONB↓ (유속 효과)
  ├─ ΔT_sub_inlet↑ → ΔT_ONB↑
  └─ D_h↓ (microchannel) → ΔT_ONB↑ (confinement)

Level 4: 비교 분석 (Phase 1과 동일 구조)
  ├─ Kandlikar (1991, 2006)
  ├─ Hsu-Graham (1976)
  ├─ Basu (2002, 2005)
  ├─ Bertsch (2009) microchannel
  └─ Lee-Mudawar (2018)
```

### 5.2 불확실도 정량화 (Phase 1과 동일 + Heteroscedastic 추가)

```
Phase 1: Deep Ensemble K=10
  └─ Coverage 98.7% achieved

Phase 2 확장:
  ├─ Deep Ensemble K=20 (parameter increase 대응)
  ├─ Heteroscedastic aleatoric head (입력 의존 σ_ale)
  ├─ Sub-grid sampling for high-Re region (covariance shift)
  └─ Out-of-distribution detection (Mahalanobis-style)
```

---

## 6. 문서화 및 투고

### 6.1 산출물 체계

| 산출물 | 시기 | 비고 |
|---|---|---|
| Phase 2 main paper (IJHMT) | M12 | Phase 1 인용 + flow 확장 |
| Phase 1+2 hybrid review (선택) | M15 | Annual Review of Heat Transfer 후보 |
| Open-source data v2 (Zenodo) | M9 | Phase 1 dataset + flow 데이터 |
| Pretrained model checkpoint | M10 | Transfer-learning starter kit |
| Benchmark publication (NeurIPS DB&B) | M15+ | E1 (community) 와 연계 |

### 6.2 논문 구성 전략

```
Phase 2 메인 논문 구성 (제안):

Section 1 Introduction
  ├─ Phase 1 결과 인용 + flow boiling 확장 필요성
  └─ Research gap: 표면 × 유동 복합 PINN 부재

Section 2 Mathematical Formulation
  ├─ NS + Energy 단순화
  ├─ Flow-aware Hsu criterion
  └─ Non-dim (Phase 1 + flow 추가)

Section 3 Data
  ├─ Phase 1 데이터 재활용 명시
  ├─ 신규 600 flow ONB 포인트
  └─ Synthetic CFD data 보강

Section 4 Architecture
  ├─ Phase 1 Surface Encoder 전이
  ├─ Flow Encoder 신규
  ├─ Dual-FiLM conditioning
  └─ Loss 7-8 terms

Section 5 Results
  ├─ Forward accuracy (flow boiling)
  ├─ Transfer learning benefit (quantified)
  ├─ Physics consistency (9 trends)
  ├─ Inverse + Simpson-effect under flow
  └─ UQ + heteroscedastic

Section 6 Conclusions
  ├─ Phase 1 + 2 통합 성과
  └─ Phase 3 (transient, CHF) 방향
```

### 6.3 저널 전략

| 저널 | 강점 | 약점 | 추천도 |
|---|---|---|---|
| **IJHMT** | Phase 1 인용 연속, scope 완벽 | 심사 6-12주 | 🥇 |
| Applied Thermal Eng | IF 6.9, 산업 응용 강조 가능 | 일부 ML scope 제한 | 🎯 |
| Int. J. Multiphase Flow | flow boiling 전문 | IF 3.8 | 🎯 |
| Int. J. Thermal Sciences | 기초 물리 강조 | scope overlap | 🛡 |
| ASME J Heat Mass Transfer | Li-Kharangate 2025 trace | IF 1.8 | 🛡 |

---

## 7. 전체 일정 및 마일스톤

```
M1-M3: 서베이 + 데이터 수집 (Stage 1)
  ├─ 신규 PINN-flow-boiling 문헌 50편 정리
  ├─ Kandlikar/Mudawar/Thome 데이터 디지타이즈
  ├─ Phase 1 surface card 재사용 매핑
  └─ Go/No-Go: Flow ONB 라벨 300+ 확보 필요

M4-M6: PINN 1단계 — Surface 재사용 + Flow encoder (Stage 2)
  ├─ Surface Encoder transfer
  ├─ Flow Encoder 구현 (Re, G, Bo, We, ΔT_sub, D_h)
  ├─ Dual-FiLM conditioning 구현
  ├─ Loss 7-8항 구성 + HPO
  └─ Go/No-Go: RMSE ≤ 8 K on 검증셋

M7-M9: PINN 2단계 — NS + Energy 통합 (Stage 3)
  ├─ Continuity / Momentum / Energy PDE residual 활성화
  ├─ Collocation 50,000-200,000 LHS
  ├─ Multi-stage training (Adam → LBFGS)
  ├─ Synthetic CFD case 비교 (Level 2)
  └─ Go/No-Go: 5 신규 trend 모두 단조성 회복

M10-M11: 검증 + UQ + Inverse (Stage 4)
  ├─ Level 1 V1-V8 검증
  ├─ Level 3 9 trends
  ├─ Deep ensemble K=20
  ├─ Heteroscedastic head
  └─ Inverse: ONB 위치 + r_c 재추정

M12: 논문 작성 (Stage 5)
  ├─ IJHMT 투고 (Phase 1과 동일 저널)
  ├─ Open-source v2 release (Zenodo DOI)
  └─ Pretrained model checkpoint 공개

M13-M15: 응답 / 부가 산출물 (Stage 6)
  ├─ 리뷰 응답
  ├─ Phase 1+2 hybrid review paper (선택)
  └─ Benchmark publication 준비 (선택)
```

---

## 8. 리스크 관리

| 리스크 | 영향 | 확률 | 대응 |
|---|---|---|---|
| Flow ONB 데이터 부족 | 상 | 중 | Synthetic CFD bootstrap 강화 + 외부 협력 |
| NS PDE residual 수렴 어려움 | 상 | 중 | Phase 1 처럼 "physics-regularized regressor" 철학 명시 |
| Transfer learning 효과 미미 | 중 | 저 | from-scratch와 ablation 공개 (정직한 비교) |
| Multi-fluid coverage 불균등 | 중 | 중 | Phase 1과 동일하게 무차원화로 universal manifold |
| Microchannel confinement 효과 미반영 | 중 | 저 | Bo_conf 별도 입력 + dimensional analysis 강화 |
| 산업 검증 어려움 | 저 | 중 | Phase 1 산업 응용 단락에서 미리 hook 배치 |
| 학습 시간 폭증 | 중 | 중 | GPU 사용 권장 + minibatch 콜로케이션 |

---

## 9. Phase 3 전이 계획

```
2단계 → 3단계 연결 후보:

후보 A — Transient boiling (시간 의존 동역학)
  ├─ ∂/∂t 항 활성화 → unsteady PINN
  ├─ Pulsed heating, transient startup, quench
  └─ 응용: laser ablation cooling, transient thermal control

후보 B — Two-phase coupled (ONB 이후 영역)
  ├─ Volume of Fluid (VOF) 결합
  ├─ ONB → bubble growth → coalescence → CHF
  └─ End-to-end boiling platform (F1 mega-project)

후보 C — Cryogenic flow boiling
  ├─ Li-Kharangate (2025) 후속
  ├─ LN₂, LHe 대상
  └─ 응용: superconducting magnet cooling

후보 D — Foundation model
  ├─ Phase 1+2 통합 weights → 다중 fluid + geometry pretrained
  ├─ Few-shot fine-tuning on new fluids
  └─ NeurIPS or ML-physics venue
```

---

## 10. 산업 응용 hook (Phase 2 paper에 명시)

```
Section 1 Introduction에 강조 권장:
  ├─ Server immersion cooling — Re 100-500, R-1234yf
  ├─ Microchannel heat exchanger — D_h < 1 mm, ΔT_sub 가변
  ├─ Nuclear DNB margin — Re 10⁴-10⁵, water at 7-15 MPa
  └─ HVAC evaporator — R-410A, R-32 boiling onset

Section 5 Discussion에 정량 예시:
  ├─ Industry-relevant range: G=100-2000 kg/m²s, q''=50-500 kW/m²
  ├─ Reduced thermal margin uncertainty: 5K → 2.5K
  └─ Design map (Surface × Flow → ΔT_ONB) 예시 그림
```

---

## 11. Claude Code 에이전트 활용 (Phase 1 자산 재사용)

```
재사용 에이전트:
  ├─ paper-card-extractor — 새 문헌 통합
  ├─ figure-digitizer — Kandlikar/Mudawar 데이터
  ├─ surface-card-builder — Phase 1 49장 + 신규
  ├─ coolprop-integrator — Re/Bo/We 계산 추가
  ├─ preprocess-pipeline — Stage 6 신규 (Re/Bo/We)
  ├─ pinn-architect — dual-FiLM 확장
  ├─ surface-encoder-dev — 전이학습 wrapper
  ├─ loss-function-builder — 7-8 terms
  ├─ training-orchestrator — 4-stage pipeline
  ├─ level1-verifier — V5-V8 신규
  ├─ physics-consistency-check — 9 trends
  ├─ correlation-comparator — Kandlikar/Mudawar/Bertsch
  ├─ inverse-solver — ONB 위치 + r_c
  ├─ ensemble-uq — K=20 + heteroscedastic
  ├─ figure-composer / figure-digitizer — Figure
  ├─ section-drafter — 본문 작성 (Phase 1 style 상속)
  ├─ latex-formatter — IJHMT format
  ├─ bibtex-curator — references.bib v2
  └─ reviewer-anticipator — Phase 1 rebuttal 자산 활용

신규 에이전트 (필요 시):
  ├─ flow-pde-builder (NS + 에너지 residual)
  ├─ confinement-handler (Bo_conf, D_h categorical)
  └─ transfer-learning-helper (Phase 1 → Phase 2 weight mapping)
```

---

## 12. 예상 산출물 정리

| 시기 | 산출물 | 매체 |
|---|---|---|
| M3 | Flow ONB 갭 매트릭스 | `01_survey/gap_matrix_phase2.md` |
| M6 | Flow ONB 데이터셋 v1 (~400 ONB pts) | `02_data/processed/onb_dataset_phase2.csv` |
| M9 | Phase 2 PINN trained model | `03_model/checkpoints/phase2_baseline/` |
| M9 | Synthetic CFD validation data | `02_data/synthetic/` |
| M11 | Phase 2 full results (figures + tables) | `04_analysis/` |
| M12 | Phase 2 manuscript draft | `05_manuscript_phase2/main.tex` |
| M12 | Open-source v2 release | Zenodo DOI + GitHub release |
| M15 | Phase 2 published paper | IJHMT or ATE |

---

## 부록 A: Phase 1 자산 매핑 (재활용 목록)

| Phase 1 자산 | Phase 2 활용 | 수정 정도 |
|---|---|---|
| Surface cards (49) | 직접 재활용 + 신규 추가 | 없음 |
| Hsu nucleation loss | δ_t 정의만 flow-aware로 변경 | 작음 |
| Monotonicity regularizers | 직접 재활용 (R_a, θ) | 없음 |
| Surface Encoder weights | 전이학습 초기값 | 일부 fine-tune |
| FiLM conditioning | Dual-FiLM으로 확장 | 보통 |
| Deep ensemble UQ | K=10 → K=20 + heteroscedastic | 보통 |
| CoolProp integration | Re/Bo/We 계산 추가 | 작음 |
| BibTeX entries (31) | 직접 재활용 + flow 문헌 추가 | 없음 |
| Reviewer rebuttal logic | Q1-Q5 그대로 + flow 특화 Q 추가 | 일부 추가 |

## 부록 B: Phase 1 평가지표 → Phase 2 목표지표

| 지표 | Phase 1 결과 | Phase 2 목표 |
|---|---|---|
| RMSE | 3.42 K (n=77) | ≤ 5 K (n=300+, flow) |
| R² | +0.44 | +0.40 (분산 증가 감안) |
| Coverage | 98.7% | ≥ 90% |
| Physics tests | 8/9 | 12/13 (4 신규 포함) |
| Transfer benefit | — | 학습 시간 -50%, RMSE -20% (from-scratch 대비) |
| Open-source impact | dataset v1 | dataset v2 + pretrained checkpoint |
