# Phase 2 문헌 서베이 후보 논문

생성일: 2026-05-21
담당: Phase 2 서베이 에이전트 (`survey-search`)
목적: 강제대류 비등(Flow Boiling) ONB PINN 연구를 위한 핵심 문헌 목록

---

## 요약 표

| # | 제목 (축약) | 저자 | 연도 | 저널 | 그룹 | Phase 1 중복 | 우선순위 |
|---|------------|------|------|------|------|------------|---------|
| 1 | Development of a Flow Boiling Map for Subcooled/Saturated Flow Boiling | Kandlikar | 1991 | ASME J. Heat Transfer | G1 고전 상관식 | 없음 | ⭐⭐⭐ |
| 2 | Onset of Nucleate Boiling and Active Nucleation Site Density During Subcooled Flow Boiling | Basu, Warrier, Dhir | 2002 | ASME J. Heat Transfer | G1 고전 상관식 | 기존 카드 있음 (Phase 1) | ⭐⭐⭐ |
| 3 | Wall Heat Flux Partitioning During Subcooled Flow Boiling: Part 1 | Basu, Warrier, Dhir | 2005 | ASME J. Heat Transfer | G1 고전 상관식 | 없음 | ⭐⭐⭐ |
| 4 | Wall Heat Flux Partitioning During Subcooled Flow Boiling: Part 2 | Basu, Warrier, Dhir | 2005 | ASME J. Heat Transfer | G1 고전 상관식 | 없음 | ⭐⭐ |
| 5 | The Determination of Forced-Convection Surface-Boiling Heat Transfer | Bergles, Rohsenow | 1964 | ASME J. Heat Transfer | G1 고전 상관식 | 기존 카드 있음 (Phase 1) | ⭐⭐⭐ |
| 6 | The Incipience of Nucleate Boiling in Forced Convection Flow | Davis, Anderson | 1966 | AIChE Journal | G1 고전 상관식 | 기존 카드 있음 (Phase 1) | ⭐⭐⭐ |
| 7 | Transport Processes in Boiling and Two-Phase Systems (Book) | Hsu, Graham | 1976 | Hemisphere/McGraw-Hill | G1 고전 상관식 | 없음 | ⭐⭐⭐ |
| 8 | Heat Transfer Mechanisms During Flow Boiling in Microchannels | Kandlikar | 2004 | ASME J. Heat Transfer | G1/G2 | 없음 | ⭐⭐ |
| 9 | Prediction of the Onset of Nucleate Boiling in Microchannel Flow | Liu, Lee, Garimella | 2005 | IJHMT | G2 마이크로채널 | 없음 | ⭐⭐⭐ |
| 10 | Fluid Flow and Heat Transfer in Low-Temperature Two-Phase Micro-Channel Heat Sinks Part 2 | Lee, Mudawar | 2008 | IJHMT | G2 마이크로채널 | 없음 | ⭐⭐ |
| 11 | Correlation for Boiling Heat Transfer of R-134a Including Effect of Tube Diameter | Saitoh, Daiguji, Hihara | 2007 | IJHMT | G2 마이크로채널 | 없음 | ⭐⭐ |
| 12 | Effect of Surface Oxidation on the Onset of Nucleate Boiling in a MTR Coolant Channel | Forrest et al. | 2016 | J. Nuclear Eng. Rad. Sci. | G1 상관식 + 표면 | 없음 | ⭐⭐⭐ |
| 13 | Physics-Informed Neural Networks for Heat Transfer Problems | Cai et al. | 2021 | ASME J. Heat Transfer | G4 PINN 방법론 | 기존 카드 있음 (Phase 1) | ⭐⭐⭐ |
| 14 | NSFnets: Physics-Informed Neural Networks for Incompressible Navier-Stokes | Jin, Cai, Li, Karniadakis | 2021 | J. Comput. Phys. | G4 PINN 방법론 | 없음 | ⭐⭐⭐ |
| 15 | Physics-Informed Neural Networks for Heat Transfer in Two-Phase Flows | Jalili et al. | 2024 | IJHMT | G3 최신 PINN/ML | 없음 | ⭐⭐⭐ |
| 16 | Transfer Learning via PINNs for Bubble Growth in Superheated Liquid | Jalili et al. | 2024 | IJHMT | G3 최신 PINN/ML | 없음 | ⭐⭐⭐ |
| 17 | Physics-Informed Neural Networks for Two-Phase Film Boiling Heat Transfer | Jalili, Mahmoudi Larimi | 2025 | IJHMT | G3 최신 PINN/ML | 없음 | ⭐⭐ |
| 18 | PINN-Based Modelling of HTC and Pressure Drop in R513A Flow Boiling (Micro-Fin) | 저자 미확인 | 2025 | Applied Thermal Engineering | G3 최신 PINN/ML | 없음 | ⭐⭐ |
| 19 | Onset of Nucleate Boiling for Subcooled Flow through Narrow Rectangular Channel | 저자 미확인 (Cheng group) | 2017 | Nuclear Engineering & Design | G1 상관식 채널 | 없음 | ⭐⭐ |
| 20 | Experimental Study of ONB in Vertical Rectangular Channels (Flow Path Heights) | Cheng et al. | 2022 | Sci. Technol. Nuclear Inst. | G1 상관식 채널 | 없음 | ⭐ |
| 21 | TL-PINN for Prediction of Nuclear Reactor Transients | Schiassi et al. (추정) | 2023 | Scientific Reports / PMC | G3 최신 PINN/ML | 없음 | ⭐⭐ |

---

## 그룹별 상세 카드

### G1 — Flow Boiling ONB 고전 상관식

---

### [Kandlikar (1991)] Development of a Flow Boiling Map for Subcooled and Saturated Flow Boiling of Different Fluids Inside Circular Tubes

- **DOI**: 10.1115/1.2910524
- **저널**: ASME Journal of Heat Transfer, 113(1), pp. 190–200, February 1991
- **핵심 내용**: subcooled 및 포화 유동비등 영역에서 열전달계수, 건도, 열유속, 질량유속 간의 관계를 유동비등 맵(flow boiling map)으로 표현. 물 및 냉매 10,000점 이상의 데이터로 개발된 범용 상관식 제안. 이 맵은 핵비등 영역(nucleate boiling dominant), 대류증발 영역(convective boiling dominant), 과도 영역의 3구역으로 구분됨.
- **Phase 2 활용 포인트**: subcooled 영역 ONB 기준선(baseline) 역할. G와 q_flux, x를 동시에 입력으로 사용하는 Phase 2 PINN 입력 변수 설계의 직접 근거. 유체별 Froude 수 보정 인자(F_fluid) 개념 활용 가능.
- **디지타이즈 대상 Figure**: Fig. 4 (Flow boiling map, subcooled region ONB 경계선)

---

### [Basu, Warrier & Dhir (2002)] Onset of Nucleate Boiling and Active Nucleation Site Density During Subcooled Flow Boiling

- **DOI**: 10.1115/1.1471522
- **저널**: ASME Journal of Heat Transfer, 124(4), pp. 717–728, August 2002
- **핵심 내용**: 접촉각 θ와 공동 밀도 N_s, 유속, 과냉도를 통합한 ONB 모델 제안. 기존 상관식들이 ΔT_ONB를 과소예측함을 실험으로 확인하고 새 상관식을 ±30% 이내 정확도로 제안. 고속카메라 시각 관찰 + 열전대 break point를 ONB 기준으로 사용.
- **Phase 2 활용 포인트**: **Phase 1에서 이미 카드화됨 (paper_database.md)**. Phase 2에서는 유속(Re, G) + 과냉도(ΔT_sub) 의존성 공식으로 PINN 물리 손실항 L_ONB 확장 근거로 활용.
- **디지타이즈 대상 Figure**: Fig. 7 (ONB 실험값 vs 예측값), Fig. 9 (active site density)

**[Phase 1 인용됨 — 상세 카드는 `01_survey/paper_database.md` 참조]**

---

### [Basu, Warrier & Dhir (2005a)] Wall Heat Flux Partitioning During Subcooled Flow Boiling: Part 1 — Model Development

- **DOI**: 10.1115/1.1842784
- **저널**: ASME Journal of Heat Transfer, 127(2), pp. 131–140, February 2005
- **핵심 내용**: subcooled flow boiling에서 벽면 열유속을 강제대류분과 증발분으로 분리(partition)하는 기계론적 모델 제안. 핵비등 사이트 밀도, 기포 이탈/리프트오프 직경, 기포 주파수, 유동 파라미터, 유체·표면 물성의 함수로 각 성분을 정량화. 압력 1.03–3.2 bar, 다양한 질량유속 조건에서 실험 검증.
- **Phase 2 활용 포인트**: Phase 2 PINN의 physics loss 설계 시 열유속 분배 모델(heat flux partitioning)을 soft constraint로 구현하는 직접 근거. ONB 이후 부분비등(partial boiling) 영역 모델링에 필수.
- **디지타이즈 대상 Figure**: Fig. 4–5 (heat flux partitioning vs 실험 비교), Fig. 8 (site density)

---

### [Basu, Warrier & Dhir (2005b)] Wall Heat Flux Partitioning During Subcooled Flow Boiling: Part 2 — Model Validation

- **DOI**: 10.1115/1.1842785
- **저널**: ASME Journal of Heat Transfer, 127(2), pp. 141–148, February 2005
- **핵심 내용**: Part 1 모델을 다양한 실험 데이터셋(압력, 질량유속, 과냉도 범위 확장)으로 검증. 광범위한 운전 조건에서 heat flux partitioning 예측 오차가 ±15–20% 수준임을 제시.
- **Phase 2 활용 포인트**: Phase 2 검증 데이터로 활용 가능. Part 1 모델의 적용 범위와 한계 파악용.
- **디지타이즈 대상 Figure**: Fig. 3–5 (모델 vs 실험 비교 플롯)

---

### [Bergles & Rohsenow (1964)] The Determination of Forced-Convection Surface-Boiling Heat Transfer

- **DOI**: 10.1115/1.3688697
- **저널**: ASME Journal of Heat Transfer, 86(3), pp. 365–372, August 1964
- **핵심 내용**: 강제대류 비등 커브의 ONB 영역 분석. q″_ONB = f(P, ΔT_ONB) 형태의 실험 상관식 제안. 물·대기압 기준으로 가장 널리 쓰이는 ONB 상관식.
- **Phase 2 활용 포인트**: **Phase 1에서 이미 카드화됨 (paper_database.md)**. Phase 2에서는 적용 압력 범위 확장(reactor 조건)과 질량유속 의존성 추가 시 비교 baseline으로 사용.
- **디지타이즈 대상 Figure**: Fig. 3 (boiling curve incipience)

**[Phase 1 인용됨 — 상세 카드는 `01_survey/paper_database.md` 참조]**

---

### [Davis & Anderson (1966)] The Incipience of Nucleate Boiling in Forced Convection Flow

- **DOI**: 10.1002/aic.690120426
- **저널**: AIChE Journal, 12(4), pp. 774–780, July 1966
- **핵심 내용**: 강제대류 조건에서 공동 크기(cavity size)를 기반으로 ONB를 예측. linear temperature profile + truncated spherical bubble 가정. 매끄러운 표면에서 large cavity 부재로 ONB가 지연되는 현상을 정량화.
- **Phase 2 활용 포인트**: **Phase 1에서 이미 카드화됨 (paper_database.md)**. Phase 2에서 r_c 역추정 문제(inverse problem)의 baseline 상관식으로 활용.
- **디지타이즈 대상 Figure**: Fig. 1 (ONB correlation vs 실험)

**[Phase 1 인용됨 — 상세 카드는 `01_survey/paper_database.md` 참조]**

---

### [Hsu & Graham (1976)] Transport Processes in Boiling and Two-Phase Systems (Book)

- **DOI / URL**: 미확인 (Hemisphere Publishing / McGraw-Hill, ISBN 미확인 — DOI 미확인)
- **저널**: Book — Hemisphere Publishing Corporation (Washington, D.C.) / McGraw-Hill Book Company, 1976
- **핵심 내용**: 비등 및 이상유동의 수송 현상을 체계화한 교재. Hsu (1962) 이론을 강제대류로 확장한 분석을 포함. cavity size range 기준을 강제대류 온도 경계층에 적용하여 ΔT_ONB 예측. "Hsu-Graham 기준"으로 유동비등 ONB 분야에서 표준 참조문헌으로 인용됨.
- **Phase 2 활용 포인트**: Phase 1 Hsu (1962) 풀비등 기준의 강제대류 확장판. 강제대류 경계층 두께 δ의 유속 의존성 식을 PINN의 PDE residual 구성에 직접 활용 가능. Phase 2 L_ONB_flow 손실항 설계의 핵심 이론적 근거.
- **디지타이즈 대상 Figure**: 해당 챕터 ONB 경계 그래프 (전문 도서, 접근 후 확인 필요)

---

### [Forrest, Don, Hu, Buongiorno & McKrell (2016)] Effect of Surface Oxidation on the Onset of Nucleate Boiling in a Materials Test Reactor Coolant Channel

- **DOI**: 10.1115/1.4031503
- **저널**: Journal of Nuclear Engineering and Radiation Science, 2(2), 021001, February 2016
- **핵심 내용**: 재료시험로(MTR) 냉각채널 모사 수직 채널(갭 1.96 mm, 종횡비 29:1)에서 산화 표면과 clean 표면의 ONB 비교. 산화 표면에서 ONB가 더 높은 열유속·과열도에서 발생함을 확인. 질량유속 750–3000 kg/m²s, 과냉도 10–45°C 범위 실험.
- **Phase 2 활용 포인트**: 표면 상태(산화/청결)가 강제대류 ONB에 미치는 영향의 실험 데이터. Phase 2 표면 카드 설계 시 산화 계수(표면 오염 factor)를 추가 변수로 고려하는 근거 제공. 좁은 채널 형상 데이터로 confined channel 효과 포함.
- **디지타이즈 대상 Figure**: Fig. 6–7 (ONB locus: 산화 vs 청결 표면 비교)

---

### [Bergles (2000)] The Imperative to Enhance Boiling Heat Transfer (Review)

> **주의**: 검색 범위 내에서 메타데이터 미확인. 추가 확인 필요. 아래는 알려진 정보만 기재.

- **DOI**: DOI 미확인
- **저널**: Enhanced Heat Transfer 관련 review 논문 (추후 bibtex-curator 확인 필요)
- **핵심 내용**: (메타데이터 불충분 — 본 항목 생략, 추후 확인 후 보완)

---

## G2 — Microchannel / Minichannel 유동비등 ONB

---

### [Liu, Lee & Garimella (2005)] Prediction of the Onset of Nucleate Boiling in Microchannel Flow

- **DOI**: 10.1016/j.ijheatmasstransfer.2005.07.021
- **저널**: International Journal of Heat and Mass Transfer, 48(25–26), pp. 5052–5064, 2005
- **핵심 내용**: 275 μm × 636 μm 마이크로채널 내 물의 ONB를 고속촬영으로 관찰하고 analytical model로 예측. 닫힌 형태(closed-form)의 incipient heat flux 및 기포 크기 식을 도출하여 중요 파라미터의 영향을 분석. 모델 예측이 실험과 양호한 일치를 보임.
- **Phase 2 활용 포인트**: 마이크로채널 형상(좁은 간격, 작은 수력직경)에서의 ONB 물리 — 채널 폭, 수력직경 D_h를 Phase 2 형상 변수로 추가할 근거. 채널 confinement number 도입 가능성.
- **디지타이즈 대상 Figure**: Fig. 8–9 (incipient heat flux vs 유속, 예측 vs 실험)

---

### [Lee & Mudawar (2008)] Fluid Flow and Heat Transfer Characteristics of Low-Temperature Two-Phase Micro-Channel Heat Sinks — Part 2: Subcooled Boiling Pressure Drop and Heat Transfer

- **DOI**: 10.1016/j.ijheatmasstransfer.2008.02.013
- **저널**: International Journal of Heat and Mass Transfer, 51(17–18), pp. 4327–4341, 2008
- **핵심 내용**: 극저온 냉각 대상(−100°C 수준) 마이크로채널 열침의 subcooled boiling 특성 규명. 압력강하 및 열전달계수 측정·예측. ONB, 기포 이탈, slug/churn 전이를 식별. 낮은 유속에서의 boiling instability 서술.
- **Phase 2 활용 포인트**: Phase 2에서 Lee 그룹의 microchanel flow boiling 체계에 따른 ONB 기준 적용. 질량유속 G와 채널 크기 D_h 복합 영향 데이터.
- **디지타이즈 대상 Figure**: Fig. 5–6 (boiling curve, ONB 표시점)

---

### [Saitoh, Daiguji & Hihara (2007)] Correlation for Boiling Heat Transfer of R-134a in Horizontal Tubes Including Effect of Tube Diameter

- **DOI**: 10.1016/j.ijheatmasstransfer.2007.06.019
- **저널**: International Journal of Heat and Mass Transfer, 50(25–26), pp. 5215–5225, 2007
- **핵심 내용**: R-134a의 수평관 유동비등 열전달 상관식 — Chen형 수정식에 기체상 Weber 수로 관 직경 효과를 정량화. 직경 0.5–11 mm ID 범위에서 적용 가능한 confinement 고려 상관식.
- **Phase 2 활용 포인트**: 관 직경 D_h가 유동비등 열전달에 미치는 영향의 물리적 파라미터화(Weber 수 기반). Phase 2 PINN에서 채널 형상 변수를 무차원화하는 방법론적 참고.
- **디지타이즈 대상 Figure**: Fig. 4–5 (HTC vs quality, diameter 비교)

---

## G3 — 최신 PINN / ML for Flow Boiling (2023–2026)

---

### [Jalili, Jadidi, Keshmiri, Chakraborty, Georgoulas & Mahmoudi (2024)] Physics-Informed Neural Networks for Heat Transfer Prediction in Two-Phase Flows

- **DOI**: 10.1016/j.ijheatmasstransfer.2023.125089
- **저널**: International Journal of Heat and Mass Transfer, 221, Article 125089, 2024
- **핵심 내용**: PINN을 이상유동 열전달에 적용하여 기포 상승(rising bubble) 및 관련 열전달을 CFD 데이터로 학습·예측. 상(phase) 경계면 위치 최대 오차 5.2%, 질량 중심 위치 오차 2.8% 달성. 계면 포착 CFD를 training data source로 활용.
- **Phase 2 활용 포인트**: Phase 2에서 이상유동 PINN 구현의 선행 방법론적 근거. CFD → PINN 학습 파이프라인과 계면 추적 loss 설계 참고.
- **디지타이즈 대상 Figure**: Fig. 7–8 (bubble interface PINN vs CFD 비교)

---

### [Jalili, Jadidi, Keshmiri, Chakraborty, Georgoulas & Mahmoudi (2024)] Transfer Learning Through Physics-Informed Neural Networks for Bubble Growth in Superheated Liquid Domains

- **DOI**: 10.1016/j.ijheatmasstransfer.2024.007701 (추정 — DOI 미확인, URL 패턴 기반)
- **저널**: International Journal of Heat and Mass Transfer, 232, 2024
- **핵심 내용**: 과열 액체 내 기포 성장의 열·질량 전달을 PINN으로 모델링하고 transfer learning을 적용. 물, R-134a, FC-72 3종 유체에서 테스트. 표면장력 효과가 지배적인 phase change 시나리오에 대한 PINN 첫 검증. 물 기포 예측 오차 감소, FC-72에서 최대 오차 1.3% 달성.
- **Phase 2 활용 포인트**: Phase 1 → Phase 2 transfer learning 전략의 직접 선행 사례. frozen encoder 기반 transfer learning 설계 시 참고.
- **디지타이즈 대상 Figure**: Fig. 5–6 (bubble growth PINN vs CFD)

---

### [Jalili & Mahmoudi Larimi (2025)] Physics-Informed Neural Networks for Two-Phase Film Boiling Heat Transfer

- **DOI**: 10.1016/j.ijheatmasstransfer.2025.126680
- **저널**: International Journal of Heat and Mass Transfer, 241, Article 126680, 2025
- **핵심 내용**: 막비등(film boiling) 이상유동 열전달에 PINN을 적용. CFD로 생성한 데이터로 학습하고 Stefan 상변화 문제로 검증. 계면 위치 오차 최대 7.1%. 앞선 2024 bubble growth 논문의 후속 심화 연구.
- **Phase 2 활용 포인트**: PINN의 boiling regime 별 확장 가능성 확인. 막비등 → 핵비등 ONB 전이 구간 모델링의 잠재적 near-term 과제.
- **디지타이즈 대상 Figure**: Fig. 4 (film boiling interface prediction)

---

### [저자 미확인 (2025)] Experimental Investigation and Physics-Informed Neural Network Based Modelling of HTC and Pressure Drop in R513A Flow Boiling Through Micro-Fin Tube

- **DOI**: DOI 미확인 (Applied Thermal Engineering, 2025; ScienceDirect URL: https://www.sciencedirect.com/science/article/abs/pii/S014070072500026X)
- **저널**: Applied Thermal Engineering, 2025
- **핵심 내용**: 마이크로핀 튜브에서 R513A(저GWP 냉매)의 유동비등 HTC 및 압력강하를 실험으로 측정하고 PINN으로 예측. 열유속, 건도, 질량유속, 포화온도를 PINN 입력으로 사용하며 물리 제약 통합. 하이퍼파라미터 튜닝으로 예측 정확도 향상.
- **Phase 2 활용 포인트**: 유동비등 HTC 예측에 PINN을 적용한 최근 응용 사례. 운전 파라미터(열유속, 건도, 질량유속) 입력 구조가 Phase 2 PINN 아키텍처 설계에 참고 가능.
- **디지타이즈 대상 Figure**: Fig. 6–7 (PINN vs 실험 HTC 비교)

---

### [Schiassi et al. (2023)] Physics-Informed Neural Network with Transfer Learning Based on Domain Similarity Measure for Prediction of Nuclear Reactor Transients

- **DOI**: DOI 미확인 (PMC10558465; Scientific Reports, October 2023)
- **저널**: Scientific Reports, 2023
- **핵심 내용**: TL-PINN(전이학습 PINN)을 원자로 과도 상태 예측에 적용. 도메인 유사도 측정으로 transfer learning의 효과를 정량화. 복잡한 열수력 현상에 대한 PINN + 전이학습 융합의 방법론적 선례.
- **Phase 2 활용 포인트**: Phase 1 (풀비등) → Phase 2 (유동비등) transfer learning 구현의 방법론적 참고. frozen encoder weight 이식 시 domain similarity 평가 방법 참고.
- **디지타이즈 대상 Figure**: Fig. 3–4 (transfer learning 효과 비교)

---

## G4 — Computational PINN for Flow / Multiphase

---

### [Jin, Cai, Li & Karniadakis (2021)] NSFnets: Physics-Informed Neural Networks for the Incompressible Navier-Stokes Equations

- **DOI**: 10.1016/j.jcp.2020.109951
- **저널**: Journal of Computational Physics, 426, Article 109951, 2021
- **핵심 내용**: 비압축성 Navier-Stokes 방정식에 PINN(NSFnet)을 적용. velocity-pressure 공식과 vorticity-velocity 공식 두 가지를 비교. 층류 및 난류 채널 유동에서 검증. 대규모 병렬화 가능성 및 sparse data 조건에서의 우수한 성능 시연.
- **Phase 2 활용 포인트**: Phase 2 PINN에서 강제대류 유동장(속도, 압력) 동시 모델링이 필요할 때의 핵심 방법론 참고. subcooled flow boiling의 단상 liquid region에 NSFnet 아이디어 직접 적용 가능.
- **디지타이즈 대상 Figure**: 없음 (방법론 논문)

---

### [Cai, Wang, Wang, Perdikaris & Karniadakis (2021)] Physics-Informed Neural Networks for Heat Transfer Problems

- **DOI**: 10.1115/1.4050542
- **저널**: ASME Journal of Heat Transfer, 143(6), Article 060801, 2021
- **핵심 내용**: 다양한 열전달 문제(열전도, 대류, 복합 열전달 등)에 PINN을 적용한 포괄적 연구. 역문제(BC 및 열원 회복)도 포함. NVIDIA DGX-A100 히트싱크의 conjugate heat transfer 문제 포함.
- **Phase 2 활용 포인트**: **Phase 1에서 이미 카드화됨 (paper_database.md)**. Phase 2에서는 conjugate heat transfer 공식화를 강제대류 채널 벽면 열전달에 적용하는 직접 근거.
- **디지타이즈 대상 Figure**: 없음 (방법론 논문)

**[Phase 1 인용됨 — 상세 카드는 `01_survey/paper_database.md` 참조]**

---

## 추가 검색 필요 항목 (미확인 또는 미발굴 논문)

아래 논문들은 타깃 키워드에 포함되었으나 검색 결과에서 메타데이터 미확인 상태. 추가 확인 권고.

| 항목 | 현황 | 권장 조치 |
|------|------|---------|
| Kandlikar (2006) — "bubble nucleation and force balance" in flow boiling | 2004 논문(Heat Transfer Mechanisms in Microchannels, 10.1115/1.4004769)으로 추정되나 연도 불일치 확인 필요 | ASME Digital Collection 직접 조회 |
| Bertsch, Groll & Garimella (2009) — composite correlation for saturated flow boiling in small channels | IJHMT 2009, Vol. 52, pp. 2110–2118로 확인. ONB 직접 연구는 아님 | ONB-specific figure 유무 확인 후 포함 여부 결정 |
| Ren et al. (2022) — PINN for conjugate heat transfer | 검색 결과에서 특정 저자·연도 매칭 실패 | Google Scholar에서 "Ren 2022 PINN conjugate heat transfer flow" 재검색 필요 |
| Sato & Matsumura (1964) — 풀비등 incipience 상관식 | Phase 1 상관식 baseline으로 이미 활용 중. 강제대류 ONB 직접 연구 아님 | Phase 1 baseline 유지, Phase 2 비교군에서는 Basu(2002)로 대체 |
| Kosar, Mishra & Peles (2005) — micropin-fin 내 subcooled boiling | DOI 10.1016/J.IJHEATMASSTRANSFER.2005.07.021 — Liu et al. (2005)와 동일 DOI 의심. 별도 논문 확인 필요 | ScienceDirect 직접 조회로 저자 재확인 |

---

## Top 3 추천 (full text 확보 우선순위)

1. **Liu, Lee & Garimella (2005)** — DOI: 10.1016/j.ijheatmasstransfer.2005.07.021
   - 마이크로채널 ONB를 closed-form으로 예측하는 유일한 전용 논문. Phase 2 채널 형상 입력 변수 설계에 필수.

2. **Jalili et al. (2024) — Transfer Learning via PINN for Bubble Growth**
   - Phase 1 → Phase 2 transfer learning 설계의 가장 직접적인 방법론 선례. PINN + TL 조합의 첫 검증 사례.

3. **Forrest et al. (2016)** — DOI: 10.1115/1.4031503
   - 강제대류 ONB에서 표면 상태(산화) 효과를 정량화한 희소한 실험 논문. Phase 2 표면 조건화 입력 설계의 근거 데이터.

---

## 검색 이력

| 날짜 | 검색어 | 결과 |
|------|--------|------|
| 2026-05-21 | Kandlikar 1991 flow boiling map subcooled ASME | 확인: DOI 10.1115/1.2910524 |
| 2026-05-21 | Basu Warrier Dhir 2002 2005 ONB wettability | 확인: DOI 10.1115/1.1471522, 10.1115/1.1842784/785 |
| 2026-05-21 | Bergles Rohsenow 1964 forced convection boiling | 확인: DOI 10.1115/1.3688697 |
| 2026-05-21 | Liu Lee Garimella 2005 microchannel ONB | 확인: DOI 10.1016/j.ijheatmasstransfer.2005.07.021 |
| 2026-05-21 | Saitoh Daiguji Hihara 2007 R134a tube diameter | 확인: DOI 10.1016/j.ijheatmasstransfer.2007.06.019 |
| 2026-05-21 | Forrest 2016 surface oxidation ONB reactor channel | 확인: DOI 10.1115/1.4031503 |
| 2026-05-21 | Jin Cai 2021 NSFnet PINN Navier-Stokes | 확인: DOI 10.1016/j.jcp.2020.109951 |
| 2026-05-21 | Jalili 2024 PINN two-phase flow heat transfer | 확인: DOI 10.1016/j.ijheatmasstransfer.2023.125089 |
| 2026-05-21 | Jalili 2024 transfer learning bubble growth PINN | 확인: IJHMT 232 (2024) |
| 2026-05-21 | Jalili 2025 film boiling PINN | 확인: DOI 10.1016/j.ijheatmasstransfer.2025.126680 |
| 2026-05-21 | PINN R513A flow boiling micro-fin 2025 | 확인: Applied Thermal Engineering 2025 |
| 2026-05-21 | Hsu Graham 1976 book forced convection boiling | 확인: Hemisphere/McGraw-Hill 1976 (DOI 없음) |
