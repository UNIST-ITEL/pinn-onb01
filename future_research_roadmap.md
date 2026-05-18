# PINN-ONB01 후속 연구 주제 로드맵

**작성일**: 2026-05-18
**근거 자료**:
- 본문 §6 Conclusions and Future Work
- `04_analysis/reviewer_rebuttal.md` Appendix B
- 분야 트렌드 (Jalili 2025, Li-Kharangate 2025, Huang 2024 등)

---

## 🎯 A. 직접 확장 (Phase 1 → Phase 2/3 자연 흐름)

| # | 주제 | 기간 | 난이도 | 임팩트 |
|---|---|---|---|---|
| A1 | **Forced-convection subcooled boiling ONB** (기존 Phase 2 계획) | 6-12개월 | 중상 | 매우 큼 |
| A2 | **1D → 2D conduction kernel** (biphilic patterns, lateral spreading) | 3-6개월 | 중 | 큼 |
| A3 | **SEM/AFM 직접 측정 통합** (3-5 실험 파트너, 5-10 surfaces, +50 ONB) | 9-18개월 | 외부 협력 | 큼 (Q1 reviewer 정면 대응) |
| A4 | **Heteroscedastic aleatoric head** (deep ensemble 상위 layer) | 2-3개월 | 중 | 중 |

## 📊 B. 데이터 / 모델 확장

| # | 주제 | 기간 | 난이도 | 임팩트 |
|---|---|---|---|---|
| B1 | **다중 유체 확장** (FC-72, Novec-7100/7200, methanol, cryogenic LN₂/LHe) | 6-12개월 | 중 | 큼 |
| B2 | **고압 비등 데이터** (p_r > 0.5, supercritical 인접 영역) | 12개월 | 중 | 중 |
| B3 | **고-q'' 영역 보강** (>200 kW/m², electronics cooling 대역) | 6개월 | 중 | 중 |
| B4 | **단일 표면 q'' sweep 통제 실험** (√q'' 단조성 직접 검증) | 6-9개월 | 외부 | 중 |
| B5 | **Model-class ensemble** (FiLM vs concat vs cross-attention, d_z 변화 ablation) | 2-3개월 | 저 | 중 |
| B6 | **Foundation model 방향** (cross-fluid + cross-geometry pretraining) | 12-24개월 | 상 | 매우 큼 |

## 🔬 C. 메소드 / 이론 확장

| # | 주제 | 기간 | 난이도 | 임팩트 |
|---|---|---|---|---|
| C1 | **Transient PINN** (pulsed heating, transient boiling startup) | 6-9개월 | 중상 | 큼 |
| C2 | **3D conjugate heat transfer** (heater-fluid 결합, lateral conduction) | 9-15개월 | 상 | 중 |
| C3 | **Hsu inverse → cavity distribution recovery** (단일 r_c → 분포 P(r_c)) | 6개월 | 중 | 중 |
| C4 | **Bayesian PINN** (variational ensemble, BNN 대체) | 6-9개월 | 중상 | 중 |
| C5 | **PINN ↔ DNS coarse-grain hybrid** (DNS sub-grid 정보 통합) | 12-18개월 | 상 | 큼 |
| C6 | **Multi-modal data fusion** (thermal + high-speed visualization + IR) | 9-12개월 | 상 | 큼 |
| C7 | **Active learning loop** (실험 디자인 → 모델 → 다음 실험 추천) | 6-9개월 | 중상 | 큼 |

## 🏭 D. 응용 / 산업 번역 (Translational)

| # | 주제 | 기간 | 난이도 | 임팩트 |
|---|---|---|---|---|
| D1 | **Immersion cooling 적용** (server thermal margin 설계) | 6-12개월 | 산업 협력 | 큼 |
| D2 | **원자력 안전 평가** (DNB margin estimation, regulatory) | 12-18개월 | 외부 검증 | 큼 |
| D3 | **냉동 evaporator 설계 자동화** (multi-objective optimization 통합) | 9-12개월 | 중 | 중 |
| D4 | **표면 개질 design map** (Ra/θ/coating → ONB 역설계) | 6개월 | 중 | 큼 |
| D5 | **반도체 발열 thermal margin 예측** (high-flux electronics) | 12개월 | 산업 | 큼 |

## 🌐 E. 커뮤니티 / 인프라

| # | 주제 | 기간 | 난이도 | 임팩트 |
|---|---|---|---|---|
| E1 | **ONB benchmark dataset 표준화** (CHF community의 LUT 같은 표준) | 12개월 | 커뮤니티 | 매우 큼 |
| E2 | **Zenodo/OSF dataset DOI 발급 + paper data citation** | 1개월 | 저 | 중 (인용 증가) |
| E3 | **Reproducibility 인증** (Papers with Code, ML4Sci benchmark 등록) | 1-2개월 | 저 | 중 |
| E4 | **PINN-for-boiling tutorial / workshop paper** (review 형식) | 6개월 | 중 | 중 |
| E5 | **Open-source dashboard** (interactive prediction tool) | 3개월 | 중 | 중 |

## 🧪 F. 통합 메가-프로젝트

| # | 주제 | 기간 | 난이도 | 임팩트 |
|---|---|---|---|---|
| F1 | **End-to-end boiling design platform** (ONB → bubble growth → CHF 통합 PINN) | 2-3년 | 매우 상 | 매우 큼 |
| F2 | **Multi-physics digital twin** (열전달 + 표면 진동 + 유동 분포) | 3년+ | 매우 상 | 매우 큼 |
| F3 | **Self-supervised boiling foundation model** (large-scale unlabeled video) | 2-3년 | 매우 상 | 매우 큼 |

---

## 추천 우선 순서 (실용적 관점)

### 즉시 후속 (Phase 2, ≤12개월)
1. **A1** Flow boiling ONB — 기존 plan, 같은 framework 직접 확장 가능, 논문 1편 도출
2. **A4 + B5** Heteroscedastic head + model-class ablation — 빠른 ablation paper (3-6개월)
3. **A3** 외부 실험 파트너 SEM/AFM 협력 시작 — 다소 시간 걸리니 일찍 시작

### 중기 (Phase 3, 12-24개월)
4. **A2** 2D kernel for biphilic patterns
5. **C1** Transient PINN — 시간 의존 비등 동역학
6. **B1 + B2** 다중 유체/고압 데이터 확장
7. **D4** Surface design map — 산업 활용도 높음

### 장기 (Phase 4+, 24개월+)
8. **B6/F1/F3** Foundation model 방향
9. **D1/D2** 산업 검증 + 규제 활용
10. **E1** Community benchmark 주도

---

## 본문 §6에 명시된 4가지 future direction (출처 일치)

> "Future work will address these gaps along four directions."

1. **Surface-card corpus 확장** + 5-10 SEM/AFM 측정 surfaces + 3-5 추가 sources에서 +50 ONB 라벨 → 본 로드맵 **A3**
2. **Forced-convection subcooled boiling** 확장 (Re, inlet subcooling 추가 conditioning) → 본 로드맵 **A1**
3. **1D → 2D kernel** (biphilic patterns의 hydrophobic island ONB localization) → 본 로드맵 **A2**
4. **Heteroscedastic aleatoric head** (ensemble 상위) → 본 로드맵 **A4**

본 로드맵의 A-시리즈는 본문 합의 사항. B~F는 본문 직접 명시는 없으나 reviewer rebuttal과 분야 트렌드에서 자연스럽게 도출되는 확장.

---

## 산출물 예상

| 단기 (1-12개월) | 산출물 |
|---|---|
| A4 + B5 ablation paper | IJHMT 또는 ATE short paper |
| A1 Phase 2 main paper | IJHMT full paper (12개월) |
| E2-E3 reproducibility | Zenodo DOI + Papers with Code 등록 |

| 중기 (12-24개월) | 산출물 |
|---|---|
| A2 biphilic ONB | 2D PINN paper (IJHMT) |
| C1 transient | IJHMT 또는 IJMF paper |
| B1 multi-fluid | Dataset paper + benchmark |

| 장기 (24개월+) | 산출물 |
|---|---|
| F1 end-to-end platform | Top journal review / framework paper |
| E1 benchmark | NeurIPS Datasets & Benchmarks 또는 ML4Sci |
| D1/D2 industrial | Application papers + technical reports |
