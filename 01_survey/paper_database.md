# 논문 카드 데이터베이스

`paper-card-extractor` 서브에이전트가 새 논문을 추가할 때 이 파일 끝에 카드를 append한다.

원문 PDF는 `01_survey/pdfs/` 폴더에 보관하며, 카드의 `PDF:` 줄에 상대 경로 표기.

## 카드 형식 (2.2절)

```
────────────────────────────────────
제목:
저자 / 저널 / 연도:
DOI:
────────────────────────────────────
분류: [상관식 / 표면개질 / CFD / ML / PINN]
비등 유형: [풀비등 / 강제대류 / 기타]
가열 형상: [평판 / 원형관 / 마이크로채널 / 기타]
표면 특성:
  ├─ 재질:
  ├─ 거칠기 Ra:
  ├─ 접촉각 θ:
  └─ 개질 방법:
작동 유체:
ONB 기준: [과열도 / 열유속 / 기포관찰 / 기타]
핵심 기여:
한계점:
본 연구 활용도: [직접 비교 / 방법론 참조 / 데이터 참조]
────────────────────────────────────
```

---

## 누적 카드

────────────────────────────────────
**제목:** On the Size Range of Active Nucleation Cavities on a Heating Surface
**저자 / 저널 / 연도:** Hsu, Y. Y. / Journal of Heat Transfer (ASME), 84(3), pp. 207–216 / 1962년 8월
**DOI:** 미확인 (ASME Paper No. 61-WA-177; 추후 `bibtex-curator`로 CrossRef 조회 권장)
**PDF:** `pdfs/HSU_JHT_1962_NucleationCavity.pdf`
────────────────────────────────────
**분류:** 상관식 (이론 기반 핵생성 기준)
**비등 유형:** 풀비등 (강제 유동 없음, 과열층 가정)
**가열 형상:** 평판 (가열면 일반화 — heating surface)
**표면 특성:**
  ├─ 재질: 명시 없음 (이론 모델, 일반 표면)
  ├─ 거칠기 Ra: 명시 없음
  ├─ 접촉각 θ: 명시 없음 (식에 β 포함되나 수치 비교 없음)
  └─ 개질 방법: 명시 없음
**작동 유체:** 물 (과냉 0~∞), 에테르(ether), 펜탄(pentane)
**ONB 기준:** 활성 공동 크기 범위 + 벽면 과열도 (effective cavity의 finite waiting period 조건; 식 (15)에서 r_c,max, r_c,min을 ΔT_sub, P, 물성, 과열층 두께 δ의 함수로 도출)
**핵심 기여:** 핵생성 cavity의 max/min 크기를 transient conduction(과열층 내) + 표면장력 기반 superheat 조건의 교점으로 정의 — 풀비등 ONB 예측의 가장 기본적인 이론적 골격을 제공. 후속 ONB 상관식(Davis-Anderson, Bergles-Rohsenow, Basu et al.)이 모두 이 모델을 출발점으로 삼음.
**한계점:**
  - 표면 거칠기/접촉각의 효과가 정량적으로 반영되지 않음 (β는 등장하나 표면 카드 매핑 불가)
  - 과열층 두께 δ가 외생 입력 — 자연대류 BC에서 어떻게 결정할지 별도 모델 필요
  - 단일 공동·정상 상태 가정, 다공질·biphilic·나노구조 표면에 직접 적용 곤란
  - 검증 데이터가 1960년대 ether/pentane/water 중심 — 현대 작동 유체(FC-72, HFE-7100) 미포함
**본 연구 활용도:** **직접 비교 + 방법론 참조**
  - 직접 비교: `correlation-comparator`의 5종 비교 baseline 중 1번 (필수). PINN 예측 ΔT_ONB와 parity plot 동일 축에 표시.
  - 방법론 참조: `loss-function-builder`의 `loss_onb_hsu` 함수가 본 논문 식 (15)의 r_c,max/min 조건을 soft constraint로 사용. 4.3절 L_ONB 항목 (a)(b)(c)는 모두 본 논문에서 유도.
────────────────────────────────────

────────────────────────────────────
**제목:** The Incipience of Nucleate Boiling in Forced Convection Flow
**저자 / 저널 / 연도:** Davis, E. J. & Anderson, G. H. / AIChE Journal, 12(4), pp. 774–780 / 1966년 7월
**DOI:** 10.1002/aic.690120426 (PDF 메타데이터에서 직접 확인)
**저자 소속:** 본문 발표 시점 — Imperial College, London, England (두 저자 모두). 본문 각주에 "E. J. Davis is at Gonzaga University, Spokane, Washington" 명시(투고 후 이직).
**PDF:** `pdfs/DAVIS_AIChE_1966_IncipienceForcedConv.pdf` (Acrobat OCR 스캔본, 7 pages, 988 KB)
**원문 상태:** **풀텍스트 확보 완료** (스캔 OCR 품질 양호; Wiley AIChE J. 1966 vol.12, pp.774–780).
────────────────────────────────────
**분류:** 상관식 (Hsu/Bergles-Rohsenow 분석의 cavity-size-range 확장)
**비등 유형:** 강제대류 (subcooled water, vertical tube). ONB 기준 자체는 풀비등에도 응용 가능.
**가열 형상:** 평판형 (관내 flow), 구리 가열관 표면 캐릭터라이즈 측정 포함
**표면 특성:**
  ├─ 재질: 구리(주 실험) + 302 stainless steel(매끄러운 비교군), Pyrex(Gouse-Coumou 인용 사례)
  ├─ 거칠기 Ra: 측정 (수치는 Surface Characteristics 섹션 — full-text에서 추출 가능, 추후 figure-digitizer로 수치화 권장)
  ├─ 접촉각 θ: 식에 명시(hemispherical bubble 가정 — bubble contact angle = 90°에서 hemispherical로 환원)
  └─ 개질 방법: 명시 없음 (as-machined / smooth-finish 비교)
**작동 유체:** 물 (subcooled forced convection), Steam-water two-phase 비교(Davis 1965 데이터)
**ONB 기준:** 벽면 과열도 + cavity size 범위 (linear temperature profile + truncated spherical bubble 가정)
**핵심 기여:**
  1. Bergles-Rohsenow(1964) 및 Sato-Matsumura(1964) 분석을 **확장** — 매끄러운 표면(예: 302 stainless steel, Pyrex)에서 large cavity 부재로 인해 ONB가 예상보다 늦게 발생하는 현상을 정량 설명.
  2. **Critical cavity size r_c 명시적 도출** — 첫 활성화되는 공동 크기를 ΔT_w, ΔT_sub, q″의 폐형 함수로 제공 (본 논문 Eq. 1과 그래프). 본 연구 4.5절 Phase 4 (역문제로 r_c 회복)의 직접 baseline.
  3. 평활 표면 가정에 한정된 단순 식: ΔT_ONB ∝ √(8σT_sat q″ / (k_l ρ_v h_fg)) (계획서 부록 A 식 [2]).
  4. 1960년대 ONB 분석 문헌(Hsu, Han-Griffith, Bergles-Rohsenow, Sato-Matsumura, Kenning)을 종합하여 **첫 cavity-size-aware 모델**의 출발점이 됨.
**한계점:**
  - **단일 공동 크기** 분석 (population density 효과 명시적으로 작다고 가정 — "low density" 명문화) — 실제 표면의 분포 무시
  - **Hemispherical bubble 가정** — Cassie-Baxter / Wenzel 등 modern wetting state 미고려
  - **Linear temperature profile** + Bergles-Rohsenow의 isothermal streamline 선택을 그대로 채택 — Sato-Matsumura, Kenning은 더 낮은 ΔT_ONB 예측
  - 강제대류 데이터로 검증 — 풀비등 자연대류 BC와 직접 매칭 필요
  - 1960년대 OCR 스캔: 일부 식 우변·아래첨자 OCR 오류 가능성 존재 (figure-digitizer로 식 재확인 권장)
**본 연구 활용도:** **직접 비교 + 방법론 참조**
  - `correlation-comparator`의 baseline 식 [2] (`davis_anderson_1966` 함수). 가장 단순한 closed-form ONB 식 → PINN 개선폭 측정의 lower bound.
  - **방법론 참조 (강화됨)**: 본 연구 4.5절 Phase 4 inverse-solver의 r_c 회복 baseline — Davis-Anderson Eq. (1)이 r_c(ΔT, q″)의 일차 근사. PINN 회복 결과와 parity plot 동일 축에 표시.
  - **데이터 참조**: Figure 1(steam-water, 100" tube), Surface Characteristics 절 측정값을 figure-digitizer로 추출 → 02_data/raw/literature/DAVIS_1966/ (cavity size 분포 + ONB 포인트).
  - Section 1.2 (ONB correlations history) 인용 시 이 카드의 "1960년대 종합" 정리를 활용.
────────────────────────────────────

────────────────────────────────────
**제목:** The Determination of Forced-Convection Surface-Boiling Heat Transfer
**저자 / 저널 / 연도:** Bergles, A. E. & Rohsenow, W. M. / ASME Journal of Heat Transfer, 86(3), pp. 365–372 / 1964
**DOI:** 미확인 (ASME 카탈로그에서 조회 권장; bibtex-curator로 추후 보강)
**PDF:** _아직 미확보. 1962년 선행 MIT TR(open access)이 dspace.mit.edu/handle/1721.1/61458 에서 조회 가능_
**원문 상태:** abstract-only
────────────────────────────────────
**분류:** 상관식 (실험 기반 — 본 그룹의 가장 영향력 있는 ONB 상관식)
**비등 유형:** 강제대류 (관내 유동), 그러나 ONB 임계 조건은 풀비등에서도 사용
**가열 형상:** 평판형 가열 면 (관내)
**표면 특성:**
  ├─ 재질: 명시 없음 (다양한 시편)
  ├─ 거칠기 Ra: 명시 없음
  ├─ 접촉각 θ: 명시적 변수 아님 (Davis-Anderson이 추가)
  └─ 개질 방법: 명시 없음
**작동 유체:** 물 (대기압 근처)
**ONB 기준:** 열유속–과열도 관계 (q''_ONB = f(P, ΔT_ONB))
**핵심 기여:** 가장 널리 쓰이는 ONB 실험 상관식 — `q''_ONB = 1082·P^1.156 · ΔT_ONB^(2.16/P^0.0234)` (계획서 부록 A 식 [3]). 기포 직경 << 마이크로레이어 가정으로 액체 온도장을 열전도로 단순화. 정확도와 사용 편의성으로 평가가 높음.
**한계점:**
  - 물·대기압 근처에 한정 — 작동 유체 일반화 제한
  - 표면 특성이 식에 명시 안 됨 (P와 ΔT만)
  - 개정 강제대류 ONB만 — 풀비등 적용 시 단일상 단열 가정 위반 가능
**본 연구 활용도:** **직접 비교**
  - `correlation-comparator`의 baseline 식 [3] (`bergles_rohsenow_1964` 함수). 물·대기압 데이터에서 가장 강한 baseline.
  - 적용 범위 외 데이터는 NaN 처리 (계획서 5.2절 규칙 따름).
────────────────────────────────────

────────────────────────────────────
**제목:** Onset of Nucleate Boiling and Active Nucleation Site Density During Subcooled Flow Boiling
**저자 / 저널 / 연도:** Basu, N., Warrier, G. R., & Dhir, V. K. / **ASME Journal of Heat Transfer, 124(4), pp. 717–728** / August 2002
**DOI:** 미확인 (ASME 카탈로그; bibtex-curator로 추후 보강)
**PDF:** _아직 미확보 — ASME 구독 필요_
**원문 상태:** abstract-only
**계획서 정정 사항:** 계획서 부록 B의 Basu 2002 인용 ("IJHMT, 45(19), 3947-3962")은 다른 논문과 혼동된 것으로 보임. 본 카드의 J. Heat Transfer 124(4) 정보가 정확.
────────────────────────────────────
**분류:** 상관식 + 표면개질 (접촉각 + 공동 밀도 통합 모델)
**비등 유형:** 강제대류 (subcooled flow boiling)
**가열 형상:** 평판 (구리) + 9-rod 봉다발 (zircaloy-4)
**표면 특성:**
  ├─ 재질: 구리 (flat plate), zircaloy-4 (rod bundle)
  ├─ 거칠기 Ra: 명시 (full-text 확인 필요)
  ├─ 접촉각 θ: **본 모델의 핵심 변수** (정량적으로 ONB에 영향)
  └─ 개질 방법: 별도 modification 없음 (mill-finish surfaces)
**작동 유체:** 물 (subcooled)
**ONB 기준:** 시각 관찰(고속 카메라) + 열전대 신호 break point의 일치
**핵심 기여:** **접촉각 + 공동 밀도 + 유속 + 과냉도**를 통합한 ONB 모델. 기존 상관식들이 ΔT_ONB를 underpredict함을 보이고, 새 상관식 제안 (실험 데이터 ±30% 이내). 풀비등 ONB에서 본 연구가 가장 직접 비교할 baseline.
**한계점:**
  - Forced convection 데이터로 도출 — 풀비등 자연대류 BC와 차이
  - 단일 표면 유형(mill-finish), 표면 개질 효과는 다루지 않음
  - r_c 분포가 아닌 평균값 기반
**본 연구 활용도:** **직접 비교 + 방법론 참조**
  - 직접 비교: `correlation-comparator`의 baseline 식 [5] (`basu_2002` 함수). 본 연구가 가장 적극적으로 능가해야 할 대상.
  - 방법론 참조: Surface Encoder의 입력에 **접촉각**을 포함시키는 직접 근거 (4.4절). 공동 밀도 N_s를 입력 변수로 채택한 것도 본 논문의 영향.
────────────────────────────────────

────────────────────────────────────
**제목:** Physics-Informed Neural Networks: A Deep Learning Framework for Solving Forward and Inverse Problems Involving Nonlinear Partial Differential Equations
**저자 / 저널 / 연도:** Raissi, M., Perdikaris, P., & Karniadakis, G. E. / Journal of Computational Physics, 378, pp. 686–707 / 2019년 2월
**DOI:** 10.1016/j.jcp.2018.10.045 (JCP 합본), arXiv:1711.10561 (Part I — Data-driven Solutions, 2017-11-30), arXiv:1711.10566 (Part II — Data-driven Discovery, 2017-11-30)
**PDF:**
  - Part I: `pdfs/RAISSI_JCP_2019_PINN.pdf` (22 pages, 580 KB)
  - Part II: `pdfs/RAISSI_arXiv_2017_PINN_PartII.pdf` (19 pages, 4.0 MB)
**저자 소속:** Brown University (Division of Applied Mathematics) + UPenn (Mech. Engr. & Applied Mech.)
**소스 코드:** https://github.com/maziarraissi/PINNs (Part I + Part II 데모 모두 공개)
**원문 상태:** **arXiv full-text 확보 완료 (Part I + Part II)**. JCP 2019 합본은 Elsevier 구독 필요하지만 arXiv preprint와 내용 동등.
────────────────────────────────────
**분류:** PINN (방법론 — 본 연구의 토대 논문)
**비등 유형:** 해당 없음 (도메인 unrelated, 프레임워크 정의)
**가열 형상:** 해당 없음
**표면 특성:** 해당 없음
**작동 유체:** 해당 없음 (Burgers, Schrödinger, Allen-Cahn, Korteweg-de Vries, Navier-Stokes 등 표준 PDE 데모)
**ONB 기준:** 해당 없음
**핵심 기여:** **PINN 프레임워크의 정식 정의**. 신경망이 PDE 잔차를 자동미분으로 평가하고 supervised data fitting과 동시에 손실항으로 받아 학습.
  - **Part I (본 PDF, 1711.10561)**: forward problem — 적은 데이터로 PDE 해 추론.
    - **Continuous time model** — 시공간 콜로케이션 포인트에서 잔차 평가, 임의 시각 평가 가능.
    - **Discrete time model** — Runge-Kutta 시간 적분(임의 차수, 최대 ~500단계) 내장 → long-horizon 안정성. 본 연구 Phase 1 해석해 학습 단계와 연관.
  - **Part II (1711.10566, 동일 저널 합본)**: inverse problem — sparse 데이터에서 PDE 매개변수(예: Reynolds 수, 비선형 계수) 동시 회복. 본 연구 4.5절 Phase 4 (ΔT_ONB 데이터 → r_c, h_nc 회복)의 직접 출처.
    - 정식화: $u_t + \mathcal{N}[u; \lambda] = 0$에서 $\lambda$를 NN의 학습 파라미터로 동시 최적화. **Burgers (λ₁, λ₂ 동시 회복)**, **Navier-Stokes (Reynolds 수)**, **KdV/shallow-water** 데모.
    - Continuous time vs Discrete time 두 알고리즘 — 데이터 분포(전역 산포 vs 두 시점 스냅샷)에 따라 선택. 본 연구의 ΔT_ONB 측정은 “산포 데이터”에 해당하므로 **Continuous time inverse model**이 1차 기본형.
    - 노이즈 강건성 데모 — 1%, 5% 가우시안 노이즈에서도 λ 회복 정확도 유지 (본 연구 실험 ΔT_ONB의 ±10% 측정 노이즈 대응 baseline).
  - 자동 미분 기반 잔차 계산 → 메쉬프리, discretization error 없음.
**한계점:**
  - 표준 PDE만 데모 (현실 응용 미적용 — Cai 2021, Zobeiry 2021이 후속으로 보완)
  - **다중 손실항 가중치 균형 문제** — 후속 연구의 주제 (GradNorm, NTK-based, adaptive normalization 등). Zobeiry 2021의 adaptive normalizing scheme이 본 연구가 채택할 보완책.
  - 고차/강비선형/multi-scale PDE에서 수렴 곤란 — 풀비등 nucleation의 강비선형성에 직접 적용 시 수렴 위험 (계획서 8절 리스크).
  - 표면 conditioning 구조 없음 — 본 연구의 Surface Encoder가 차별점.
**본 연구 활용도:** **방법론 참조** (최상위 필수 인용)
  - `pinn-architect` + `loss-function-builder`의 직접적 출처. 4.2~4.3절의 모든 구조가 본 논문의 일반화.
  - 4.5절 Phase 1 — Discrete time model의 RK 통합 아이디어가 자연대류 정상상태 사전학습에 응용 가능.
  - 4.5절 Phase 4 inverse-solver 에이전트 spec — Part II Continuous time model 정식화 채택. λ ↔ (r_c, h_nc, δ) 매핑.
  - 5.1절 Level 1 검증 — 본 논문 Burgers/Allen-Cahn 케이스의 재현 정확도와 동등 또는 그 이상 달성을 목표로 설정.
  - GitHub 레퍼런스 코드 (maziarraissi/PINNs) — Phase 1 Burgers 재현은 Level 1 검증 시 비교 baseline.
  - 논문 작성 시 Section 1.4 (Promise of PINN)의 첫 인용.
  - 후속: Lu et al. 2021 DeepXDE는 본 논문의 구현 라이브러리 — 별도 카드 작성 권장.
────────────────────────────────────

────────────────────────────────────
**제목:** A Study of Nucleate Boiling Heat Transfer on Hydrophilic, Hydrophobic and Heterogeneous Wetting Surfaces
**저자 / 저널 / 연도:** Jo, H., Ahn, H. S., Kang, S., & Kim, M. H. / International Journal of Heat and Mass Transfer, 54(25–26), pp. 5643–5652 / 2011
**DOI:** 10.1016/j.ijheatmasstransfer.2011.06.001
**PDF:** `pdfs/JO_IJHMT_2011_HydrophobicDots.pdf` (1.2 MB) — 다운로드 완료 (2026-05-09, UNIST 기관 접속)
**원문 상태:** abstract + full-text 확보
────────────────────────────────────
**분류:** 표면개질 (이종 wettability — 본 연구 차별점의 직접 baseline)
**비등 유형:** 풀비등 (대기압)
**가열 형상:** 평판 (실리콘 웨이퍼 위 패턴)
**표면 특성:**
  ├─ 재질: 실리콘(Si) 기반 — SiO₂/Teflon 코팅으로 wettability 조절
  ├─ 거칠기 Ra: full-text 확인 필요 (코팅 두께 수십 nm 수준 추정)
  ├─ 접촉각 θ: hydrophilic (≈ 36°) / hydrophobic (≈ 123°) / heterogeneous (패턴 영역 따라)
  └─ 개질 방법: 포토리소그래피 + Teflon 코팅으로 hydrophilic / hydrophobic / 두 영역 패턴된 heterogeneous 표면 3종 제작
**작동 유체:** 물 (포화, 1 atm)
**ONB 기준:** 시각 관찰(고속 카메라) + 비등 곡선 변곡점
**핵심 기여:** 동일 재질 위에 wettability만 다른 3종 표면(hydrophilic / hydrophobic / 패턴된 heterogeneous)에서 비등 거동을 직접 비교. **hydrophobic 표면이 ONB 과열도를 가장 낮추지만 CHF는 hydrophilic에서 최대**임을 보임. heterogeneous 패턴은 ONB 저감 + CHF 보존을 동시 달성 — 본 연구의 surface conditioning 가설(접촉각 → r_c 활성 분포 변화)의 직접 실험적 근거.
**한계점:**
  - r_c, N_s가 직접 측정되지 않음 (접촉각만 보고)
  - 단일 작동 유체(물), 단일 압력(대기압)
  - heterogeneous 패턴의 기하학적 매개변수(line spacing, area fraction) 변화는 제한적
**본 연구 활용도:** **데이터 참조 + 직접 비교**
  - 데이터 참조: figure-digitizer로 비등 곡선 3종 디지타이즈 → 02_data/raw/literature/JO_2011/. ONB 포인트와 ΔT_ONB 추출.
  - 직접 비교: 표면 카드 SFC-Jo-Hydrophilic, SFC-Jo-Hydrophobic, SFC-Jo-Heterogeneous 3종 등록. PINN의 ΔT_ONB 예측이 hydrophobic ↓ 경향(계획서 검증 경향성 #3)을 재현하는지 확인.
  - 방법론 참조: 본 연구 4.4절 Surface Encoder 입력에 접촉각을 포함시키는 핵심 근거 (Basu 2002와 함께 인용).
────────────────────────────────────

────────────────────────────────────
**제목:** Boiling Heat Transfer on Superhydrophilic, Superhydrophobic, and Superbiphilic Surfaces
**저자 / 저널 / 연도:** Betz, A. R., Jenkins, J., Kim, C.-J. "CJ", & Attinger, D. / International Journal of Heat and Mass Transfer, 57(2), pp. 733–741 / 2013년 2월
**DOI:** 10.1016/j.ijheatmasstransfer.2012.10.080
**PDF:** `pdfs/BETZ_IJHMT_2013_Superbiphilic.pdf` (4.9 MB, 19 pages) — 다운로드 완료 (2026-05-07, arXiv:1211.1602)
**원문 상태:** abstract + 주요 결과 확보. arXiv 본문 read 가능 (full-text 처리는 후속 카드 보강 시).
────────────────────────────────────
**분류:** 표면개질 (superbiphilic — 극단적 wettability contrast)
**비등 유형:** 풀비등 (포화, 대기압)
**가열 형상:** 평판 (실리콘 웨이퍼 위 마이크로/나노 구조)
**표면 특성:**
  ├─ 재질: Si 기반, SiO₂ 나노필러(superhydrophilic) + Teflon 코팅(superhydrophobic) 조합
  ├─ 거칠기 Ra: 마이크로/나노 구조 (Cassie-Baxter / Wenzel 영역 전환), 수치 full-text 확인 필요
  ├─ 접촉각 θ: superhydrophilic (≈ 0°) / superhydrophobic (> 150°) / superbiphilic (영역별)
  └─ 개질 방법: 마이크로 컬럼 어레이 + 표면 화학 (실리카 나노입자 + 자기조립 단분자막) — 4종 표면 제작
**작동 유체:** 물 (포화, 1 atm)
**ONB 기준:** 시각 관찰(고속 카메라) + 비등 곡선 시작점
**핵심 기여:** **첫 superbiphilic 표면 제작·시험**. (1) superhydrophobic은 ΔT_ONB가 거의 0에 가까울 정도로 ONB 조기 발생 — 본 연구 검증 경향성 #3의 극한 사례. (2) superbiphilic은 CHF > 100 W/cm² + HTC > 100 kW/(m²·K) 동시 달성. (3) hydrophobic 영역이 nucleation을 trigger하고 hydrophilic 영역이 dryout을 막는 dual-role 메커니즘 제안.
**한계점:**
  - 패턴 기하 파라미터(영역 크기, 배치) 최적화는 제한적
  - 압력·과냉도 영향 미평가
  - 패턴 spatial 정보를 1D PINN(본 연구)에 어떻게 반영할지가 도전 — Surface Encoder가 평균값으로 처리하면 정보 손실 발생
**본 연구 활용도:** **데이터 참조 + 직접 비교**
  - 데이터 참조: figure-digitizer로 4종 표면(SHL/SHB/SBP × 1 plain) 비등 곡선 디지타이즈 → 02_data/raw/literature/BETZ_2013/. 특히 superhydrophobic의 극저 ΔT_ONB 데이터는 PINN extrapolation 검증의 stress test.
  - 직접 비교: PINN이 θ → 0° 및 θ → 150° 극단에서 물리적으로 타당한 ΔT_ONB를 출력하는지 확인 (계획서 5.1절 Level 3 — 극한 조건 거동).
  - 한계 인지: heterogeneous 패턴은 본 연구의 1D 모델에서 정확 재현 곤란 — 한계점 섹션에 명시 (계획서 8절 리스크 관리).
────────────────────────────────────

────────────────────────────────────
**제목:** Controlling Bubble Motion over Heated Surface through Evaporation Momentum Force to Enhance Pool Boiling Heat Transfer
**저자 / 저널 / 연도:** Kandlikar, S. G. / Applied Physics Letters, 102(5), 051611 / 2013
**DOI:** 10.1063/1.4791682
**PDF:** _아직 미확보 — AIP 구독 필요 (UNIST 기관 접속 권장). RIT 저자 프로필에서 사후 공개판 확인 가능_
**원문 상태:** abstract + 주요 결과 확보
────────────────────────────────────
**분류:** 표면개질 (마이크로 구조 — feeder 채널 + 증발 모멘텀 메커니즘)
**비등 유형:** 풀비등 (포화, 대기압)
**가열 형상:** 평판 (구리, 마이크로채널 가공)
**표면 특성:**
  ├─ 재질: 구리 (plain copper baseline + microstructured)
  ├─ 거칠기 Ra: 마이크로채널 깊이/폭 (수십~수백 μm, full-text 확인 필요)
  ├─ 접촉각 θ: 명시 없음 (메커니즘은 wettability 아닌 evaporation momentum)
  └─ 개질 방법: 가열면에 V-groove / 직사각형 마이크로채널 가공 — bubble trajectory를 강제 분리하여 vapor와 liquid feeder path 형성
**작동 유체:** 물 (포화, 1 atm)
**ONB 기준:** 비등 곡선 (HTC, CHF 중심 — ONB 자체는 부수적)
**핵심 기여:** Wettability가 아닌 **마이크로구조 → 기포 운동 제어 → 증발 모멘텀 활용**이라는 별도 enhancement 경로 제시. 결과: 평판 구리 대비 **HTC 8배(629 kW/m²·K)**, **CHF 2.5배 (~3 MW/m²)**. ONB는 부수 결과지만, 마이크로채널이 활성 공동을 추가 공급하여 ΔT_ONB 저감에도 기여.
**한계점:**
  - ONB 자체에 초점이 아님 — ΔT_ONB 데이터는 비등 곡선에서 파생 추출 필요
  - 단일 fluid (물), 단일 압력
  - 마이크로채널 기하가 1D 평균 거칠기 Ra로 표현 불가 — Surface Encoder의 표현력 한계 stress test
  - 메커니즘이 evaporation momentum 기반 → Hsu 기준의 표면장력 가정과 부분 충돌
**본 연구 활용도:** **데이터 참조 + 한계 인지 (방법론 참조 부수)**
  - 데이터 참조: 본 연구가 다루는 평탄/약한 거칠기 영역과 다른 “구조화” 영역의 boundary 표시. Surface Encoder의 입력 특성에 microchannel 기하(width, depth, aspect ratio)를 추가할지 검토 (Phase 2 surface card 정의 시).
  - 한계 인지: Hsu 기준만으로 본 표면을 설명할 수 없음 → 본 연구는 명시적으로 “마이크로채널·structured surface는 scope-out” 선언 (계획서 1.1절 scope).
  - 방법론 참조 (부수): "표면이 단순 wettability/Ra 변수만으로 환원되지 않는다"는 한계 논의의 인용근거.
────────────────────────────────────

────────────────────────────────────
**제목:** DeepXDE: A Deep Learning Library for Solving Differential Equations
**저자 / 저널 / 연도:** Lu, L., Meng, X., Mao, Z., & Karniadakis, G. E. / SIAM Review, 63(1), pp. 208–228 / 2021
**DOI:** 10.1137/19M1274067
**arXiv:** 1907.04502 (2019, open access — preprint와 출판본 내용 동등)
**PDF:** `pdfs/LU_SIAM_2021_DeepXDE.pdf` (arXiv preprint, 1.1 MB) — 다운로드 완료
**소스 코드:** https://github.com/lululxvi/deepxde (PyPI: `pip install deepxde`)
**원문 상태:** **arXiv full-text 확보 완료**
────────────────────────────────────
**분류:** PINN (방법론 + 구현 프레임워크 — 본 연구의 직접 구현 라이브러리)
**비등 유형:** 해당 없음 (PDE 일반 — Burgers, Poisson, Lorenz inverse 등 5종 데모)
**가열 형상:** 해당 없음 (CSG 기반 임의 형상 지원)
**표면 특성:** 해당 없음
**작동 유체:** 해당 없음
**ONB 기준:** 해당 없음
**핵심 기여:**
  1. **DeepXDE 라이브러리 (Python)** — Raissi 2019 정식화를 production-ready 라이브러리로 구현. 본 연구의 `requirements.txt`가 이 라이브러리를 직접 채택 (CLAUDE.md "프레임워크: PyTorch + DeepXDE").
  2. **RAR (Residual-based Adaptive Refinement)** — 잔차가 큰 위치에 콜로케이션 포인트를 동적 추가. 풀비등 ONB의 강비선형 구간(transition zone)에서 특히 유용 — `pinn-architect` + `training-orchestrator`가 채택할 핵심 기법.
  3. **CSG (Constructive Solid Geometry)** — 복잡 형상 도메인을 unions/intersections으로 표현. 본 연구 1D 도메인에서는 직접 사용 안 하나, Phase 2 (강제대류) 확장 시 활용 가능.
  4. **Forward + Inverse 통일 인터페이스** — 동일 코드 베이스에서 방향 전환. 본 연구 4.5절 Phase 1 (forward) → Phase 4 (inverse) 전환 코드 단순화.
  5. **integro-differential, fractional, stochastic PDE** 지원 — 본 연구 scope에는 직접 해당 없으나 확장성 인용 근거.
  6. **FEM 대비 분석** — pedagogical 비교로 PINN의 mesh-free + auto-diff 장점 명확화. 논문 작성 시 Section 1.4 인용.
**한계점:**
  - 1.x 시리즈는 TensorFlow 1.x 기반이었으나 현재(2.0+) PyTorch backend 지원 — 본 연구는 PyTorch backend 사용 (CLAUDE.md 기준).
  - 다중 손실항 가중치 자동 균형은 미내장 (Zobeiry 2021 또는 Wang et al. NTK 등 별도 구현 필요).
  - GPU 분산 학습 미직접 지원 (단일 GPU 기준).
**본 연구 활용도:** **방법론 참조 + 구현 프레임워크 (필수 인용)**
  - `pinn-architect` + `training-orchestrator`의 직접적 구현 토대. 4.2절 네트워크 + 4.3절 손실 + 4.5절 Phase 학습 모두 DeepXDE API 활용.
  - **RAR 채택**: ONB transition zone (ΔT 5~10K)의 잔차 집중 영역에서 콜로케이션 동적 보강 — `training-orchestrator`의 핵심 옵션.
  - Phase 1 해석해 사전학습 — DeepXDE의 1D 열전도 예제(Burgers/diffusion)를 baseline으로 코드 구조 차용.
  - 5.1절 Level 1 검증 — DeepXDE 공식 예제(diffusion equation, Poisson) 재현 정확도와 비교.
  - 논문 Section 2 (Methods) 인용: "PINN 구현은 DeepXDE 라이브러리(Lu et al. 2021)에 기반".
────────────────────────────────────

────────────────────────────────────
**제목:** Physics-Informed Neural Networks for Heat Transfer Problems
**저자 / 저널 / 연도:** Cai, S., Wang, Z., Wang, S., Perdikaris, P., & Karniadakis, G. E. / ASME Journal of Heat Transfer, 143(6), Article 060801 / 2021년 6월
**DOI:** 10.1115/1.4050542
**PDF:** _아직 미확보 — ASME 구독 필요. arXiv preprint 미확인 (Karniadakis 그룹은 자주 OSTI/researchgate에 공개판 제공)_
**원문 상태:** abstract + 핵심 문제군 확보
────────────────────────────────────
**분류:** PINN (방법론 — 본 연구의 가장 가까운 직접 선례)
**비등 유형:** 해당 없음 (단상 forced/mixed convection 중심) — Stefan 문제 케이스에서 상변화 다룸
**가열 형상:** 다양한 prototype (cavity 내 mixed convection, two-phase Stefan 등)
**표면 특성:** 표면 미세구조 미고려 (이상 BC 가정)
**작동 유체:** 케이스별 (단상 유체 일반 — 비등 ONB 데이터 없음)
**ONB 기준:** 해당 없음
**핵심 기여:** Raissi 2019의 일반 PINN을 **열전달 문제 전용**으로 구체화. 핵심 시나리오: (1) **알 수 없는 열적 BC**가 있는 forced/mixed convection — sparse 온도 측정만으로 T, u 전 영역 + 경계 회복(역문제). (2) Stefan 문제 (two-phase, moving boundary). 본 연구의 4.5절 Phase 4 (역문제 — ΔT_ONB 데이터로 r_c 분포 추정)와 직접 일치하는 패러다임.
**한계점:**
  - 단상 / Stefan만 — 풀비등의 다공동 핵생성 메커니즘 미적용
  - 표면 특성을 입력 변수로 받는 conditioning 구조 없음 → 본 연구의 Surface Encoder가 차별점
  - 실험 데이터 미사용 (모두 합성/FEM 데이터)
**본 연구 활용도:** **방법론 참조 (필수 인용)**
  - 4.5절 Phase 4 inverse-solver의 직접 출처. ΔT_ONB 측정값에서 r_c, h_nc, δ 등 미지 파라미터 회복.
  - 4.2절 PINN 메인 구조에서 sparse data + PDE residual 가중 전략의 인용 근거.
  - 비교 정량 baseline은 아님 (도메인이 다름) — Section 1.4 (PINN promise)에서 "PINN이 열전달에 적용된 대표 사례" 목록에 포함.
  - Note: 동일 그룹 Cai et al. (2021), Acta Mechanica Sinica 37(12) 1727–1738 (PINN for fluid mechanics review, DOI: 10.1007/s10409-021-01148-1)는 별도 카드로 추가할지 검토 — 유체 mechanics 중심이라 우선순위 낮음.
────────────────────────────────────

────────────────────────────────────
**제목:** A Physics-Informed Machine Learning Approach for Solving Heat Transfer Equation in Advanced Manufacturing and Engineering Applications
**저자 / 저널 / 연도:** Zobeiry, N. & Humfeld, K. D. / Engineering Applications of Artificial Intelligence, 101, Article 104232 / 2021
**DOI:** 10.1016/j.engappai.2021.104232
**PDF:** `pdfs/ZOBEIRY_EAAI_2021_PINNHeatTransfer.pdf` (1.98 MB) — 다운로드 완료 (2026-05-09, UNIST 기관 접속)
**원문 상태:** abstract + 핵심 기법 + full-text 확보
────────────────────────────────────
**분류:** PINN (방법론 — 손실 정규화 + 외삽 안정화)
**비등 유형:** 해당 없음 (단상 conduction + convective BC, 오븐 가열 응용)
**가열 형상:** 1D, 2D 평판 (advanced manufacturing — 복합재 경화 등)
**표면 특성:** 표면 미세구조 미고려 (대류 BC h가 미지)
**작동 유체:** 해당 없음 (오븐 내 가열 — 공기 BC)
**ONB 기준:** 해당 없음
**핵심 기여:**
  1. **Adaptive normalizing scheme** — 다중 손실항(잔차, BC, 데이터)의 수치 스케일을 자동 균형화하여 동시 감소 보장. 본 연구 4.3절 4-항 손실 가중치 튜닝(λ_PDE, λ_BC, λ_data, λ_ONB)의 직접 모티브.
  2. **Physics-informed activation function** — 열전달 이론(예: 지수 감쇠 $e^{-\alpha t}$ 형태)을 활성함수에 내장 → 학습 영역 외부에서도 정확 외삽. 본 연구 4.2절 네트워크 설계 옵션 검토.
  3. **Unknown convective coefficient** 회복 — h를 NN 출력으로 동시 학습. 본 연구 자연대류 BC의 h_nc 추정과 직접 유사.
**한계점:**
  - 단순 1D/2D 케이스만 검증 — 풀비등 nucleation처럼 강한 비선형성 미시험
  - 표면 conditioning 미고려
  - 다중 표면 유형 일반화 미시도
**본 연구 활용도:** **방법론 참조**
  - debug-diagnoser + hpo-tuner: adaptive normalizing scheme을 손실 가중치 자동 조정의 baseline으로 채택 검토 (계획서 4.3절 보완).
  - pinn-architect: physics-informed activation 옵션을 Phase 1 (해석해 사전학습) 단계의 활성함수 후보로 검토 — 자연대류 점근 거동 내장.
  - inverse-solver: h_nc(자연대류 계수) 회복 방식의 직접 선례.
  - Section 1.4 인용: PINN을 열전달 + 외삽 안정성 측면에서 발전시킨 대표 사례.
────────────────────────────────────

────────────────────────────────────
**제목:** The Influence of Surface Roughness on Nucleate Pool Boiling Heat Transfer
**저자 / 저널 / 연도:** Jones, B. J., McHale, J. P., & Garimella, S. V. / ASME Journal of Heat Transfer, 131(12), Article 121009 / 2009년 12월
**DOI:** 10.1115/1.3220144
**저자 소속:** Cooling Technologies Research Center, School of Mechanical Engineering, Purdue University
**PDF:** `pdfs/JONES_JHT_2009_RoughnessPoolBoiling.pdf` (1.93 MB) — 다운로드 완료 (2026-05-09, 사용자 수동 — Purdue 리포지토리)
**원문 상태:** abstract + 핵심 수치 결과 확보
────────────────────────────────────
**분류:** 상관식 + 표면개질 (거칠기 효과의 정량 측정)
**비등 유형:** **풀비등** (saturated, 1 atm)
**가열 형상:** 평판 (구리 추정 — full-text 확인 필요)
**표면 특성:**
  ├─ 재질: full-text 확인 필요 (Garimella 그룹 표준은 보통 구리)
  ├─ 거칠기 Ra: **체계 변수 — 0.027~0.038 μm (polished) ↔ 1.08~10.0 μm (EDM 가공)** → 본 연구 Surface Encoder Ra 입력 범위와 직접 매핑
  ├─ 접촉각 θ: 측정값 명시 없음 (거칠기 변수에 집중)
  └─ 개질 방법: 기계 polishing + EDM (electric discharge machining) 가공으로 Ra 단계적 변화
**작동 유체:** **물 + Fluorinert FC-77** (두 유체 비교 — 본 연구 작동 유체 범위와 직접 매핑)
**ONB 기준:** 비등 곡선 (HTC, ΔT 측정 — ONB 자체는 곡선에서 파생)
**핵심 기여:**
  1. 거칠기 Ra가 풀비등 HTC에 미치는 영향을 두 유체에서 정량 측정. 가장 거친 표면(EDM)에서 polished 대비 **FC-77 +210%, 물 +100%** HTC 향상.
  2. **"Ra alone is inadequate"** — 거칠기 효과를 단일 Ra로 표현하는 것이 부적절함을 명시. h ∝ Ra^m 형태의 power-law 상관식 제안 (m은 유체 의존). 본 연구 Surface Encoder가 Ra 단독이 아닌 추가 표면 특성(N_s, θ)을 함께 받아야 한다는 직접 근거.
  3. 두 유체에서 거칠기 민감도가 다름 — FC-77이 물보다 거칠기에 훨씬 민감 (작동 유체 의존성). 본 연구 conditioning 입력에 유체 식별자(또는 σ, h_fg 등 물성)가 필요한 이유.
**한계점:**
  - ONB 자체의 ΔT 직접 측정값은 abstract에 미명시 — 비등 곡선에서 ΔT_ONB 추출 필요 (figure-digitizer)
  - 단일 압력(대기압), 단일 형상(평판)
  - 접촉각·공동 밀도 미측정 → 거칠기 변화의 메커니즘이 r_c, N_s 중 어느 것을 통한 것인지 불분명
**본 연구 활용도:** **직접 비교 + 데이터 참조 + 방법론 참조**
  - **직접 비교**: `correlation-comparator`에 h ∝ Ra^m 형태 baseline 식 추가 검토 (`jones_2009` 함수, 유체별 m 분리).
  - **데이터 참조 (핵심)**: figure-digitizer로 두 유체 × 다섯 거칠기 비등 곡선 디지타이즈 → 02_data/raw/literature/JONES_2009/ → ΔT_ONB 추출 후 Surface Encoder 학습 데이터로 직접 활용.
  - **방법론 참조**: "Ra alone is inadequate" — 본 연구 4.4절 Surface Encoder 입력 변수 설계의 직접 근거. 단순 Ra가 아닌 다차원 표면 특성 인코딩 정당화.
  - 갭 매트릭스: **거칠기 × 상관식 셀 +1** (현재 0편 → 1편). 갭 매트릭스 1번째 갱신.
────────────────────────────────────

────────────────────────────────────
**제목:** A Theoretical Model to Predict Pool Boiling CHF Incorporating Effects of Contact Angle and Orientation
**저자 / 저널 / 연도:** Kandlikar, S. G. / ASME Journal of Heat Transfer, 123(6), pp. 1071–1079 / 2001년 12월
**DOI:** 10.1115/1.1409265
**저자 소속:** Mechanical Engineering Department, Rochester Institute of Technology (RIT)
**PDF:** `pdfs/KANDLIKAR_JHT_2001_CHFContactAngle.pdf` (174 KB) — 다운로드 완료 (2026-05-09, UNIST 기관 접속)
**원문 상태:** abstract + full-text 확보
────────────────────────────────────
**분류:** 상관식 (CHF 이론 모델 — 접촉각 효과의 정식 정량화)
**비등 유형:** **풀비등** (saturated)
**가열 형상:** 평판 (수평~수직, orientation 0°~90° 범위)
**표면 특성:**
  ├─ 재질: 모델 자체는 재질 무관 (이론). 검증 데이터: 다양한 (R-113, 물 등)
  ├─ 거칠기 Ra: 명시 없음 (모델 변수 아님)
  ├─ 접촉각 θ: **dynamic receding contact angle** — 모델의 핵심 입력 변수. 본 연구의 정적 θ보다 정확한 표현 (실제 비등 시 receding이 더 물리적)
  └─ 개질 방법: 모델 적용 가능 영역 — 표면 conditioning을 통한 θ 변경
**작동 유체:** R-113 (주 검증), 물, 다양한 (CHF correlation 호환)
**ONB 기준:** 해당 없음 — **CHF (Critical Heat Flux)** 예측 모델. ONB와는 다른 비등 곡선 영역이지만, 접촉각의 비등 거동 영향을 정량화한 점에서 본 연구와 메커니즘 공유.
**핵심 기여:**
  1. **CHF 예측에 접촉각을 명시적 변수로 도입한 첫 이론 모델** — Zuber(1959) hydrodynamic 모델의 확장. 가장 인용되는 CHF correlation 중 하나.
  2. **Force balance**: bubble 기저부의 evaporation momentum vs. 표면장력 + 관성 + 점성 — Hsu(1962)의 thermal balance와 다른 mechanical balance 관점.
  3. **Orientation 효과**: 0° (수평 가열, 위쪽 향함) ~ 90° (수직) 범위에서 CHF 변화를 예측. 본 연구는 수평 평판 0°에 한정되나, 향후 확장 시 참조.
  4. CHF formula: $q''_{CHF} = h_{fg} \rho_v^{1/2} \left[\frac{\sigma g (\rho_l - \rho_v)}{\rho_v^2}\right]^{1/4} K(\beta_{rec}, \phi)$ — K(β_rec, φ)에 dynamic receding 접촉각과 orientation 의존성 함수.
**한계점:**
  - **CHF 모델이지 ONB 모델 아님** — 본 연구의 Section 1.2 (ONB correlations)에는 직접 baseline 아님. 단, Section 1.3 (surface modification effects)에서 인용.
  - Dynamic receding contact angle은 정적 θ보다 측정 어려움 — 본 연구는 정적 θ만 사용 (한계로 명시 필요).
  - 표면 거칠기 효과 미포함 → Jones 2009와 상보적.
  - 단일 유체 검증(주로 R-113, 물) → 일반화 한계.
**본 연구 활용도:** **방법론 참조 (간접 비교)**
  - **방법론 참조 (강함)**: 본 연구 4.4절 Surface Encoder가 접촉각을 입력으로 받는 정당화 — Basu(2002), Jo(2011)와 함께 가장 강한 인용 근거. "접촉각 → CHF 영향이 정량화된 가장 인용되는 모델 (Kandlikar 2001)".
  - **간접 비교 (CHF 영역)**: 본 연구의 메인 출력은 ΔT_ONB이지만, 학습된 Surface Encoder가 동일 표면에서 CHF에도 일관된 경향을 보이는지 부수 검증.
  - **한계 인지**: 본 연구가 사용하는 정적 접촉각의 한계점을 reviewer에게 설명할 때 인용 ("dynamic receding이 더 물리적이지만 실험 데이터 한계로 정적 사용").
  - 갭 매트릭스: **젖음성 × 상관식 셀 +1** (현재 0편 → 1편).
────────────────────────────────────

────────────────────────────────────
**제목:** Surface Wettability Control by Nanocoating: The Effects on Pool Boiling Heat Transfer and Nucleation Mechanism
**저자 / 저널 / 연도:** Phan, H. T., Caney, N., Marty, P., Colasson, S., & Gavillet, J. / International Journal of Heat and Mass Transfer, 52(23–24), pp. 5459–5471 / 2009년 11월
**DOI:** 10.1016/j.ijheatmasstransfer.2009.06.032
**저자 소속:** CEA Grenoble + LEGI (Univ. Joseph Fourier, France)
**PDF:** `pdfs/PHAN_IJHMT_2009_NanocoatingWettability.pdf` (1.27 MB) — 다운로드 완료 (2026-05-09, UNIST 기관 접속)
**원문 상태:** abstract + full-text 확보
────────────────────────────────────
**분류:** 표면개질 + 상관식 (nanocoating으로 접촉각 단독 제어 + ONB 메커니즘 분석)
**비등 유형:** **풀비등** (saturated, 1 atm)
**가열 형상:** 평판 (스테인리스 추정 — full-text 확인 필요)
**표면 특성:**
  ├─ 재질: 금속 substrate + 나노코팅 (구체 재질 full-text 확인 필요)
  ├─ 거칠기 Ra: 코팅으로 거의 동일하게 유지 → **거칠기 변수 제어로 접촉각 단독 효과 분리** (Jo 2011보다 더 엄격한 분리)
  ├─ 접touchangle θ: **체계 변수 — 약 20° (친수) ~ 110° (소수) 범위 단독 제어**
  └─ 개질 방법: SiO₂ / 다양한 나노입자 코팅 — 표면 화학만 변경, 거칠기 보존
**작동 유체:** 물 (포화, 1 atm)
**ONB 기준:** 비등 곡선 + 핵생성 메커니즘 분석 (고속 카메라 관찰 추정)
**핵심 기여:**
  1. **거칠기 영향을 제거한 상태에서 접촉각만의 효과 정량화** — Jo(2011) hydrophilic/hydrophobic 두 점이 아닌 **연속적 접촉각 변화** 측정 (20°~110° 범위).
  2. ONB 과열도 ΔT_ONB가 접촉각에 따라 어떻게 변하는지 정량 그래프 제공 — 본 연구의 검증 경향성 #3 (θ ↑ → ΔT_ONB ↓)의 직접 데이터 출처.
  3. Hsu(1962) cavity activation 메커니즘과 nanocoating 결과를 연결하여 **접촉각이 r_c 활성 분포를 어떻게 변화시키는지** 메커니즘 차원 분석.
  4. 단순 wettability classification이 아닌 정량적 접촉각 변수 — Surface Encoder의 θ 입력 차원 학습 데이터로 가장 적합.
**한계점:**
  - 단일 유체(물), 단일 압력(대기압)
  - 코팅 두께·내구성 정보 — full-text 확인 필요
  - ONB 자체의 직접 측정 그래프는 abstract에 명시 없음 — figure-digitizer로 확인 필요
  - 동적 receding 접촉각 측정은 미보고 (정적 θ만)
**본 연구 활용도:** **데이터 참조 + 직접 비교 + 방법론 참조**
  - **데이터 참조 (최우선)**: figure-digitizer로 ΔT_ONB(θ) 그래프 추출 → 02_data/raw/literature/PHAN_2009/. **연속적 θ 변화 데이터**가 Surface Encoder의 θ 차원 학습에 가장 가치 있음.
  - **직접 비교**: 본 연구 PINN의 ΔT_ONB(θ) 예측 곡선이 Phan의 실험 곡선과 일치하는지 비교 (`physics-consistency-check` 경향성 #3 검증).
  - **방법론 참조**: 거칠기·접촉각 효과를 분리하는 실험 설계 — 본 연구 데이터셋 구성 시 입력 변수 직교성 확보의 모범.
  - 갭 매트릭스: **젖음성 × 상관식 셀 +1** (Kandlikar 2001과 함께 카운트 → 0편 → 2편).
────────────────────────────────────

────────────────────────────────────
**제목:** Nucleate Pool-Boiling Heat Transfer. I: Review of Parametric Effects of Boiling Surface
**저자 / 저널 / 연도:** Pioro, I. L., Rohsenow, W., & Doerffer, S. S. / International Journal of Heat and Mass Transfer, 47(23), pp. 5033–5044 / 2004
**DOI:** 10.1016/j.ijheatmasstransfer.2004.06.019
**저자 소속:** McMaster University (Pioro), MIT (Rohsenow), AECL (Doerffer)
**PDF:** `pdfs/PIORO_IJHMT_2004_PartI_ParametricReview.pdf` (429 KB) — 다운로드 완료 (2026-05-09, UNIST 기관 접속)
**원문 상태:** abstract + full-text 확보
────────────────────────────────────
**분류:** 상관식 (서베이 + 표면 파라미터 리뷰)
**비등 유형:** **풀비등** (saturated/subcooled 포괄)
**가열 형상:** 평판 + 원형관 외면 (포괄적)
**표면 특성:**
  ├─ 재질: 다양 (구리/알루미늄/황동/스테인리스 등 — 리뷰 범위)
  ├─ 거칠기 Ra: 핵심 변수 — 레이저 프로파일로미터 측정의 **14종 거칠기 지수** (Ra, Rq, Rz 등) 비교 분석
  ├─ 접촉각 θ: 명시 변수 (재질 + 표면 처리 함수)
  └─ 개질 방법: 다양 (mechanical polishing, sandblasting, EDM, coatings — 문헌 종합)
**작동 유체:** 다양 (물, 에탄올, R-113, n-헵탄, 냉매 — 리뷰)
**ONB 기준:** HTC 곡선 기반 (직접 ΔT_ONB 측정은 부수)
**핵심 기여:**
  1. **표면 파라미터의 종합 리뷰** — Ra만으로 거칠기 효과를 설명하는 것의 한계를 명시. Jones et al.(2009)의 "Ra alone is inadequate" 논지의 직접 선례.
  2. **14종 거칠기 지수 비교** — Surface Encoder 입력 변수 후보군의 학술적 근거 (Ra, Rq, Rz, Sk, Sm 등).
  3. Gorenflo, Rohsenow, Cooper 등 주요 풀비등 HTC 상관식의 표면 파라미터 의존성을 한 자리에서 비교.
  4. Part II와 짝을 이루는 시리즈 — Part I은 데이터 + 파라미터, Part II는 예측 상관식 평가.
**한계점:**
  - ONB 자체보다 HTC + CHF 중심 — ΔT_ONB 직접 측정 데이터는 종합 그래프에 포함됨
  - 2004년 시점 — 최근 nano/micro structured 표면 미포함
  - 정량 모델보다 정성 정리 위주
**본 연구 활용도:** **방법론 참조 + 데이터 참조**
  - **방법론 참조 (강함)**: 본 연구 4.4절 Surface Encoder 입력 변수 설계의 학술적 근거 — "다중 거칠기 지수가 필요하다"는 본 논문의 결론을 직접 인용.
  - **데이터 참조**: 종합 비등 곡선 그래프(figure-digitizer 후보)에서 ΔT_ONB 후보 추출 가능.
  - 갭 매트릭스: **거칠기 × 상관식 +1**, **평판 × 상관식 +1** (다중 셀).
────────────────────────────────────

────────────────────────────────────
**제목:** Nucleate Pool-Boiling Heat Transfer. II: Assessment of Prediction Methods
**저자 / 저널 / 연도:** Pioro, I. L., Rohsenow, W., & Doerffer, S. S. / International Journal of Heat and Mass Transfer, 47(23), pp. 5045–5057 / 2004
**DOI:** 10.1016/j.ijheatmasstransfer.2004.06.020
**저자 소속:** Part I과 동일 (McMaster, MIT, AECL)
**PDF:** `pdfs/PIORO_IJHMT_2004_PartII_PredictionAssessment.pdf` (1.55 MB) — 다운로드 완료 (2026-05-09, UNIST 기관 접속)
**원문 상태:** abstract + full-text 확보
────────────────────────────────────
**분류:** 상관식 (예측 방법 정량 평가)
**비등 유형:** **풀비등**
**가열 형상:** 평판 + 원형관 외면 (포괄)
**표면 특성:** Part I 참조 — 본 논문은 예측 모델 평가에 집중
**작동 유체:** 물, 에탄올, R-113, n-헵탄 (구리/알루미늄/황동/스테인리스 표면)
**ONB 기준:** HTC 곡선 + 평가 메트릭
**핵심 기여:**
  1. **6종 풀비등 HTC 예측 상관식 정량 평가** — Rohsenow, Stephan-Abdelsalam, Cooper, Gorenflo, Pioro 등.
  2. 각 상관식의 데이터 적합도(MAE, MAPE 등)를 유체·재질 조합별로 정량화.
  3. **Rohsenow + Pioro 상관식이 최우수** 결론 — 본 연구 `correlation-comparator`의 baseline 식 선정 근거.
  4. Part I + Part II 합본은 풀비등 HTC 분야의 표준 reference.
**한계점:**
  - HTC 상관식 평가 — ONB 상관식은 부수적
  - 2004년 데이터 한정 — 최근 nano coating 미포함
  - 평가 메트릭에 표면 conditioning 효과 제한적
**본 연구 활용도:** **직접 비교 + 방법론 참조**
  - **직접 비교**: `correlation-comparator`의 baseline 식 선정 시 본 논문 평가 결과 인용. 특히 ONB 데이터는 부족하지만 HTC 부근의 ΔT 예측 정확도 baseline으로 사용.
  - **방법론 참조**: 5.2절 비교 분석 — 평가 메트릭(MAE, MAPE, R²) 채택의 직접 선례.
  - 갭 매트릭스: **거칠기 × 상관식 +1**, **평판 × 상관식 +1**.
────────────────────────────────────

────────────────────────────────────
**제목:** Influence of the Wettability on the Boiling Onset
**저자 / 저널 / 연도:** Bourdon, B., Rioboo, R., Marengo, M., Gosselin, E., & De Coninck, J. / Langmuir, 28(2), pp. 1618–1624 / 2012년 1월
**DOI:** 10.1021/la203636a
**저자 소속:** Université de Mons (Bourdon, Rioboo, De Coninck) + Univ. Bergamo (Marengo)
**PDF:** `pdfs/BOURDON_Langmuir_2012_BoilingOnset.pdf` (2.44 MB) — 다운로드 완료 (2026-05-09, UNIST 기관 접속)
**원문 상태:** abstract + full-text 확보
────────────────────────────────────
**분류:** 표면개질 + 상관식 (젖음성 단독 효과의 가장 엄격한 실험)
**비등 유형:** **풀비등**
**가열 형상:** 평판 (극평활 청동)
**표면 특성:**
  ├─ 재질: 청동 (bronze)
  ├─ 거칠기 Ra: **10 nm 이하 고정** (ultra-smooth — 거칠기 효과 완전 배제)
  ├─ 접촉각 θ: **체계 변수 — 화학적 그라프팅으로 단독 제어** (silane 등 SAM)
  └─ 개질 방법: 표면 화학 그라프팅 (자기조립 단분자막) — 거칠기 보존 + 화학 변경
**작동 유체:** 물 (포화)
**ONB 기준:** Boiling onset temperature (직접 측정)
**핵심 기여:**
  1. **거칠기를 10 nm 이하로 고정**한 상태에서 화학적 처리만으로 접촉각 변화 — Phan(2009)보다 더 엄격한 변수 분리.
  2. 젖음성 단독으로 ONB 개시 온도가 결정됨을 실험적 증명 — Hsu(1962) cavity activation 메커니즘이 거칠기 부재에서도 작동함을 의미.
  3. 본 연구 검증 경향성 #3 (θ ↑ → ΔT_ONB ↓)의 가장 깨끗한 실험 데이터.
**한계점:**
  - 단일 유체(물), 단일 압력
  - Ultra-smooth 표면은 실제 응용 표면(거칠기 있음)과 다름 — 일반화 제약
  - ONB 데이터 포인트 수 — full text 확인 필요
**본 연구 활용도:** **데이터 참조 + 방법론 참조**
  - **데이터 참조 (최우선급)**: figure-digitizer로 ΔT_onset(θ) 그래프 추출 → 02_data/raw/literature/BOURDON_2012/. **거칠기를 통제 변수로 만든 데이터셋** — Surface Encoder의 θ 차원만 학습할 때 가장 깨끗한 데이터.
  - **방법론 참조**: 본 연구 데이터셋 구성 시 거칠기-젖음성 직교성 확보의 모범. Phan(2009)와 함께 인용.
  - 갭 매트릭스: **젖음성 × 상관식 +1**, **평판 × 상관식 +1**.
────────────────────────────────────

────────────────────────────────────
**제목:** Wettability Influence on the Onset Temperature of Pool Boiling: Experimental Evidence onto Ultra-Smooth Surfaces
**저자 / 저널 / 연도:** Bourdon, B., Bertrand, E., Di Marco, P., Marengo, M., Rioboo, R., & De Coninck, J. / Advances in Colloid and Interface Science, 221, pp. 34–40 / 2015년 7월
**DOI:** 10.1016/j.cis.2015.04.004
**저자 소속:** Université de Mons + Univ. Pisa (Di Marco) + Univ. Bergamo (Marengo)
**PDF:** `pdfs/BOURDON_ACIS_2015_UltraSmoothONB.pdf` (1.19 MB, 7 pages) — 다운로드 완료 (2026-05-09, UNIST 기관 접속)
**원문 상태:** abstract + full-text 확보
────────────────────────────────────
**분류:** 표면개질 + 상관식 (Bourdon 2012의 확장 — 비단조 거동 + 분자 모델)
**비등 유형:** **풀비등**
**가열 형상:** 평판 (극평활)
**표면 특성:**
  ├─ 재질: 명시 (full-text 확인 필요 — 청동 추정)
  ├─ 거칠기 Ra: **10 nm 이하 고정** (ultra-smooth)
  ├─ 접촉각 θ: **0°~110° 범위** — Bourdon 2012(20°~110°) 대비 더 친수까지 확장
  └─ 개질 방법: 분자 코팅 (다양한 silane chemistry)
**작동 유체:** 물 (포화)
**ONB 기준:** ONB 개시 온도 (T_w)
**핵심 기여:**
  1. **비단조적 접촉각-ONB 관계** 발견 — θ가 매우 작을 때(<20°)와 크을 때(>90°)에서 ONB 거동이 단조적이지 않음을 보고. **본 연구 검증 경향성 #3 (θ↑ → ΔT_ONB↓)의 한계** — 극저 θ에서는 다른 메커니즘 작용.
  2. 분자 확산 기반 이론 모델 제안 — 표면 화학과 ONB의 분자 수준 연결.
  3. Bourdon 2012의 후속 — 더 넓은 θ 범위와 분자 메커니즘 추가.
**한계점:**
  - 단일 유체, 단일 압력
  - Ultra-smooth 한정
  - 비단조 거동의 이론 모델은 검증 데이터가 제한적
**본 연구 활용도:** **데이터 참조 + 한계 인지**
  - **데이터 참조**: ONB(θ) 곡선 figure-digitizer로 추출 → 본 연구 검증 경향성의 **edge case** 데이터로 사용. 매우 친수(θ < 20°) 영역의 비단조성은 PINN 학습 시 outlier로 둘지 학습 데이터에 포함할지 결정 필요.
  - **한계 인지**: 본 연구가 단조 monotonic 경향(검증 #3)만 검증한다는 점을 reviewer 대응 시 명시. "θ < 20° 영역은 본 연구 scope-out, Bourdon(2015) 보고된 비단조 거동은 향후 연구로".
  - 갭 매트릭스: **젖음성 × 상관식 +1**, **평판 × 상관식 +1**.
────────────────────────────────────

────────────────────────────────────
**제목:** Roughness and Surface Material Effects on Nucleate Boiling Heat Transfer from Cylindrical Surfaces to Refrigerants R-134a and R-123
**저자 / 저널 / 연도:** Jabardo, J. M. S., Ribatski, G., & Stelute, E. / Experimental Thermal and Fluid Science, 33(4), pp. 579–590 / 2009년 4월
**DOI:** 10.1016/j.expthermflusci.2008.12.006 (Elsevier DOI redirect resolve 확인됨)
**저자 소속:** University of São Paulo, São Carlos
**PDF:** `pdfs/JABARDO_ETFS_2009_CylindricalRoughness.pdf` (983 KB) — 다운로드 완료 (2026-05-09, UNIST 기관 접속)
**원문 상태:** abstract + full-text 확보
────────────────────────────────────
**분류:** 상관식 + 표면개질 (원형관 + 거칠기 복합 — 가열 형상 갭 보충)
**비등 유형:** **풀비등** (saturated)
**가열 형상:** **원형관 외면** (수평 cylindrical, OD = 19 mm) — 본 매트릭스 가열 형상 갭(원형관 0편)을 메우는 핵심 논문
**표면 특성:**
  ├─ 재질: **3종 — 구리, 황동, 스테인리스** (재질 효과 비교)
  ├─ 거칠기 Ra: **체계 변수 0.03~10.5 μm** (Jones 2009와 유사 범위)
  ├─ 접촉각 θ: 명시 없음 (재질·거칠기에 집중)
  └─ 개질 방법: 기계 가공 (연마 + sandblasting)
**작동 유체:** **냉매 R-134a, R-123** (본 연구 작동 유체 후보 확장)
**ONB 기준:** HTC 곡선 (ΔT_ONB는 곡선에서 파생)
**핵심 기여:**
  1. **원형관 외면 풀비등** — 본 연구 가열 형상 #2 (원형관)의 직접 baseline.
  2. **재질 × 거칠기 상호작용** 정량화 — 동일 Ra라도 재질에 따라 HTC가 다름. 본 연구 Surface Encoder 입력에 재질 인덱스(또는 열물성 k_substrate)를 포함시킬지 결정의 근거.
  3. R-134a/R-123 — 물·FC-72 외 냉매 confirm 데이터셋. Phase 2 확장 시 활용 가능.
**한계점:**
  - 직접 ΔT_ONB 측정값보다 HTC 데이터 중심
  - 단일 압력
  - 접촉각 미측정
**본 연구 활용도:** **직접 비교 + 데이터 참조**
  - **직접 비교**: `correlation-comparator`의 원형관 형상 baseline. 매트릭스 가열 형상 #2 (원형관 외면) 셀의 핵심 카운트.
  - **데이터 참조**: 3종 재질 × 다양 Ra 데이터셋 → 02_data/raw/literature/JABARDO_2009/. 재질 효과를 학습 데이터에 포함시키면 Surface Encoder 차원 확장 가능.
  - 갭 매트릭스: **원형관 × 상관식 +1**, **거칠기 × 상관식 +1** (다중 셀).
────────────────────────────────────

────────────────────────────────────
**제목:** Nucleate Pool Boiling on Horizontal Tubes: A Convection-Based Correlation
**저자 / 저널 / 연도:** Cornwell, K. & Houston, S. D. / International Journal of Heat and Mass Transfer, 37(Suppl. 1), pp. 303–309 / 1994
**DOI:** 10.1016/0017-9310(94)90031-0
**저자 소속:** Heriot-Watt University, Edinburgh
**PDF:** `pdfs/CORNWELL_IJHMT_1994_TubePoolBoiling.pdf` (698 KB) — 다운로드 완료 (2026-05-09, UNIST 기관 접속)
**원문 상태:** abstract + full-text 확보
────────────────────────────────────
**분류:** 상관식 (원형관 외면 풀비등 — convection-based)
**비등 유형:** **풀비등**
**가열 형상:** **원형관 외면** (수평, 직경 8~50 mm)
**표면 특성:**
  ├─ 재질: 다양 (다양한 관 재료)
  ├─ 거칠기 Ra: 명시 변수 아님 (slidong bubble convection 메커니즘 중심)
  ├─ 접촉각 θ: 명시 없음
  └─ 개질 방법: 표준 가공 표면
**작동 유체:** 물, 냉매, 유기물 (광범위 — 일반화 의도)
**ONB 기준:** HTC 상관식 (Nu 형태)
**핵심 기여:**
  1. **수평 원형관 풀비등의 가장 인용되는 상관식 중 하나** — Nu = A·F(p)·Re_b^0.67·Pr^0.4 (sliding bubble convection 메커니즘).
  2. 직경 8~50 mm 범위 적용 가능 — 본 연구 원형관 형상 default 사이즈와 매핑.
  3. Hsu/Bergles-Rohsenow 같은 stationary bubble 가정과 다른 관점 — sliding bubble 메커니즘 도입.
**한계점:**
  - HTC 중심 — ONB 자체 예측은 부수
  - 표면 특성(거칠기·접촉각) 미명시 — Surface Encoder의 직접 입력 매핑 곤란
  - 1994년 데이터 — 현대 nano/micro 표면 미적용
**본 연구 활용도:** **직접 비교**
  - `correlation-comparator`의 원형관 baseline (`cornwell_houston_1994` 함수). Jabardo 2009와 짝을 이루는 원형관 baseline 한 쌍.
  - 본 연구가 평판에서 시작하지만 향후 원형관 확장 시 가장 먼저 비교할 식.
  - 갭 매트릭스: **원형관 × 상관식 +1**.
────────────────────────────────────

────────────────────────────────────
**제목:** Lattice Boltzmann Modeling of Boiling Heat Transfer: The Boiling Curve and the Effects of Wettability
**저자 / 저널 / 연도:** Li, Q., Kang, Q. J., Francois, M. M., He, Y. L., & Luo, K. H. / International Journal of Heat and Mass Transfer, 85, pp. 787–796 / 2015년 6월
**DOI:** 10.1016/j.ijheatmasstransfer.2015.01.136
**저자 소속:** LANL (Kang, Francois) + Xi'an Jiaotong (Li, He) + UCL (Luo)
**arXiv:** 1501.03857 (open access — preprint와 출판본 동등)
**PDF:** `pdfs/LI_IJHMT_2015_LBM_Boiling.pdf` (arXiv preprint, 299 KB) — 다운로드 완료
**원문 상태:** **arXiv full-text 확보 완료** (preprint와 출판본 내용 동등)
────────────────────────────────────
**분류:** **CFD** (Lattice Boltzmann 위상변화 모델 — 매트릭스 CFD 열 첫 카운트)
**비등 유형:** **풀비등**
**가열 형상:** 평판 (수치 시뮬레이션)
**표면 특성:**
  ├─ 재질: 시뮬레이션 — 재질 무관 (열물성 입력)
  ├─ 거칠기 Ra: 명시 변수 아님 (smooth wall 가정)
  ├─ 접촉각 θ: **체계 변수** — LBM에서 접촉각 의존성 직접 구현
  └─ 개질 방법: 시뮬레이션상 θ 변화
**작동 유체:** 모델 유체 (van der Waals 형태 EOS — 일반화)
**ONB 기준:** 비등 곡선 — ONB, CHF, 막비등 임계 모두 시뮬레이션
**핵심 기여:**
  1. **LBM 위상변화 모델로 핵비등~막비등 전체 비등 곡선을 최초 재현** — 본 연구의 PINN 결과를 검증할 수 있는 CFD reference.
  2. 접촉각 → ONB, CHF, 막비등 임계 과열도 의존성을 정량 그래프로 제공 — 본 연구 PINN 예측의 trend 검증 기준.
  3. ONB 단독이 아닌 **boiling curve 전체** 재현 — 본 연구 scope-out인 후행 영역(post-ONB)의 거동 참조.
**한계점:**
  - LBM 모델 유체 — 실제 물·FC-72 등 정확 물성 매핑 어려움
  - 표면 거칠기 미고려 (smooth wall)
  - 단일 가열 형상 (평판)
**본 연구 활용도:** **직접 비교 + 방법론 참조**
  - **직접 비교**: 본 연구 PINN의 ΔT_ONB(θ) 예측 곡선이 Li 2015 LBM 결과와 정성 일치하는지 비교 (`physics-consistency-check` Level 3).
  - **방법론 참조**: 5.2절 비교 분석 — 본 연구가 PINN으로 single-phase conduction + ONB만 예측하는 이유 (LBM은 비싸지만 정확 / PINN은 빠르지만 ONB만)의 trade-off 인용.
  - 갭 매트릭스: **젖음성 × CFD +1**, **평판 × CFD +1**.
────────────────────────────────────

────────────────────────────────────
**제목:** Lattice Boltzmann Simulations for Surface Wettability Effects in Saturated Pool Boiling Heat Transfer
**저자 / 저널 / 연도:** Gong, S. & Cheng, P. / International Journal of Heat and Mass Transfer, 85, pp. 635–646 / 2015년 6월
**DOI:** 10.1016/j.ijheatmasstransfer.2015.02.008 (DOI redirect resolve 확인됨)
**저자 소속:** Shanghai Jiao Tong University
**PDF:** `pdfs/GONG_IJHMT_2015_LBM_Wettability.pdf` (2.56 MB) — 다운로드 완료 (2026-05-09, UNIST 기관 접속)
**원문 상태:** abstract + full-text 확보
────────────────────────────────────
**분류:** **CFD** (위상변화 LBM)
**비등 유형:** **풀비등** (saturated)
**가열 형상:** 평판 (균질 + 이종 wettability 패턴 — biphilic 시뮬레이션)
**표면 특성:**
  ├─ 재질: 시뮬레이션 (열물성 입력)
  ├─ 거칠기 Ra: smooth wall
  ├─ 접촉각 θ: **체계 변수** — 균질 + 패턴된 biphilic 둘 다
  └─ 개질 방법: 시뮬레이션상 θ 분포
**작동 유체:** 모델 유체
**ONB 기준:** 비등 곡선 (ONB, CHF 시뮬레이션)
**핵심 기여:**
  1. **균질 + 이종(biphilic) 젖음성 표면 풀비등을 LBM으로 시뮬레이션** — Betz(2013) superbiphilic 실험의 수치 대응판.
  2. **이종 젖음성 배열이 ONB 저감 + CHF 유지를 동시 달성**함을 수치 검증 — Betz(2013) 실험 결론을 first-principles 시뮬레이션으로 confirm.
  3. Li 2015와 함께 LBM-based 풀비등 연구의 한 축.
**한계점:**
  - LBM 모델 유체
  - 평판 한정
  - 거칠기 미고려
**본 연구 활용도:** **직접 비교 + 방법론 참조**
  - **직접 비교**: 본 연구가 1D 평판 PINN으로 Betz superbiphilic을 직접 표현 못 한다는 한계 — Gong 2015 LBM이 본 연구 한계의 보완 도구라는 점을 명시 (계획서 8절 리스크 관리).
  - **방법론 참조**: 5.2절 PINN vs CFD trade-off — Gong/Li 2015가 CFD 비교 baseline.
  - 갭 매트릭스: **젖음성 × CFD +1**, **평판 × CFD +1** (Li 2015와 합쳐 ❌→⚠️로 승급 예상).
────────────────────────────────────

────────────────────────────────────
**제목:** Laser-Engineered Microcavity Surfaces with a Nanoscale Superhydrophobic Coating for Extreme Boiling Performance
**저자 / 저널 / 연도:** Može, M., Senegačnik, M., Gregorčič, P., Hočevar, M., Zupančič, M., Golobič, I. / ACS Applied Materials & Interfaces, 12(22), pp. 24917–24926 / 2020
**DOI:** 10.1021/acsami.0c01594
**PDF:** PMC Open Access — https://pmc.ncbi.nlm.nih.gov/articles/PMC7304832/ — 사용자 수동 다운로드 후 `pdfs/MOZE_ACSAMI_2020_LaserMicrocavity.pdf`로 보관 권장
**원문 상태:** abstract 확보; PMC 오픈 액세스이나 bot 차단으로 직접 수집 불가 — 사용자 수동 다운로드 필요
────────────────────────────────────
**분류:** 표면개질 (마이크로구조 + 나노코팅) (부수: 상관식)
**비등 유형:** 풀비등 (saturated)
**가열 형상:** 평판 (수평, ITO 가열면)
**표면 특성:**
  ├─ 재질: ITO(Indium Tin Oxide) 코팅 유리 기판
  ├─ 거칠기 Ra: 명시 없음 (마이크로캐비티 직경 2.8 μm 및 4.2 μm, 깊이 명시 — Ra 환산 불가)
  ├─ 접촉각 θ: 초소수성(superhydrophobic) 나노코팅 적용면 ~150°, 비처리 친수성 기준면 ~30° (약 추정; 정확 수치는 full-text 확인 필요)
  └─ 개질 방법: 펨토초 레이저 마이크로캐비티 가공 + 나노스케일 소수성 코팅 (SFCS — silane-based fluorocarbon)
**작동 유체:** 물 (탈이온수, 대기압)
**ONB 기준:** 벽면 과열도 ΔT_ONB (고속 카메라 기포 초생 관찰 + 비등 곡선 급변점 교차 확인)
**핵심 기여:**
  1. 레이저 가공 마이크로캐비티(d = 2.8 / 4.2 μm) + 나노소수성 코팅 조합으로 **ΔT_ONB = 0.2 K** 극저 과열도 달성 — 풀비등 ONB 데이터베이스의 최저값 수준.
  2. 캐비티 직경(2.8 μm vs. 4.2 μm), 접촉각(친수 vs. 초소수성), ΔT_ONB 3-변수 조합 데이터 제공 — Surface Encoder 학습 데이터로 직접 활용 가능.
  3. 나노코팅 단독(초소수성, 캐비티 無) 대비 캐비티+코팅 시너지 정량 비교 — 표면 인자 상호작용 데이터.
  4. 고속 카메라(100,000 fps) 기포 핵생성 시각화로 ONB 기준 직접 검증 — 기포관찰 ONB 기준의 신뢰성 높음.
**한계점:**
  - 단일 유체(물, 대기압) — 압력·유체 일반화 불가
  - ITO 가열면 한정 — 금속 기판과의 비교 없음
  - 마이크로캐비티 직경 2종만 — 더 넓은 파라메트릭 스터디 없음
  - 접촉각 정확 수치는 full-text 확인 후 카드 갱신 필요
**본 연구 활용도:** **데이터 참조 + 직접 비교**
  - **데이터 참조 (최우선)**: 마이크로캐비티 직경(d_cavity)·접촉각(θ)·ONB 과열도(ΔT_ONB) 3변수 쌍이 `02_data/raw/literature/MOZE_2020/`의 Surface Encoder 학습 데이터로 직접 입력 가능. figure-digitizer로 ONB(d_cavity) 그래프 추출 권장.
  - **직접 비교**: ΔT_ONB = 0.2 K 극저값 — PINN 외삽 성능의 stress test. `physics-consistency-check` Level 4 대상.
  - 갭 매트릭스: **마이크로구조 × 상관식 셀의 첫 카드 (❌→⚠️ 승급)**.
────────────────────────────────────

────────────────────────────────────
**제목:** Wall superheat at the incipient nucleate boiling condition for natural and forced convection: A CFD approach
**저자 / 저널 / 연도:** Saleem, A., Farooq, S., Karimi, I. A., Banerjee, R. / Computers & Chemical Engineering, 134, 106718 / 2020
**DOI:** 10.1016/j.compchemeng.2019.106718
**PDF:** Elsevier 구독 필요. Academia.edu에 PDF 확인됨 — https://www.academia.edu/94156306/Wall_superheat_at_the_incipient_nucleate_boiling_condition_for_natural_and_forced_convection_A_CFD_approach — 사용자 수동 확보 권장; 확보 후 `pdfs/SALEEM_CCE_2020_CFD_ONB.pdf`로 보관
**원문 상태:** abstract 확보; full-text 미확보 (Elsevier 구독 필요)
────────────────────────────────────
**분류:** CFD (부수: 상관식)
**비등 유형:** 풀비등 (자연대류) + 강제대류 (둘 다 포함)
**가열 형상:** 평판 (수직 가열면 — 수치 시뮬레이션)
**표면 특성:**
  ├─ 재질: 명시 없음 (CFD 수치 모델 — 열유속 경계조건)
  ├─ 거칠기 Ra: CFD 명시 변수 (공동 반경 r_c를 Ra의 함수로 직접 설정 — 정량 관계 핵심)
  ├─ 접촉각 θ: 명시 없음
  └─ 개질 방법: 해당 없음 (시뮬레이션)
**작동 유체:** 물 (과냉, 대기압 기준) — 유체 독립 일반 상관식 도출 의도
**ONB 기준:** 벽면 과열도 ΔT_ONB (CFD 온도장 해석 + Hsu/Davis-Anderson 기준 적용 교점)
**핵심 기여:**
  1. **CFD로 ΔT_ONB ↔ Ra(표면 거칠기) 직접 정량 관계 도출** — 갭 매트릭스 거칠기 × CFD 셀의 첫 카드 (❌→⚠️ 승급).
  2. 자연대류 + 강제대류 비등 ONB를 동일 CFD 프레임워크로 비교 — 본 연구 1단계(자연대류 풀비등) 경계조건(BC) 설정의 직접 reference.
  3. 유체 독립 일반 상관식 제안 — 본 연구 PINN generalization 검증의 비교 baseline 후보.
  4. Hsu/Davis-Anderson 대비 CFD 기반 접근의 개선점(비선형 온도장 반영) 정량 제시.
**한계점:**
  - 단일 유체(물) 위주 — 냉매 등으로의 일반화 검증 없음
  - 접촉각 θ를 변수로 포함하지 않음 — 젖음성 효과 미반영
  - 수직 평판 형상 — 수평 평판(본 연구 1차 표적 형상)과 차이
**본 연구 활용도:** **직접 비교 + 방법론 참조**
  - **직접 비교**: ΔT_ONB ↔ Ra 정량 관계 — `correlation-comparator`의 거칠기 dependent baseline. `saleem_2020_cfd_onb` 함수로 등록 가능.
  - **방법론 참조**: 자연대류 풀비등 BC 설정 방법 — `loss-function-builder` h_nc(자연대류 열전달계수) 항목의 CFD 근거 참조.
  - 갭 매트릭스: **거칠기 × CFD 셀의 첫 카드 (❌→⚠️ 승급)**, **평판 × CFD +1**.
────────────────────────────────────

────────────────────────────────────
**제목:** Lattice Boltzmann simulation of nucleate boiling in micro-pillar structured surface
**저자 / 저널 / 연도:** Dong, Z., Li, W., Song, Y. / International Journal of Heat and Mass Transfer, 132, pp. 1176–1186 / 2019
**DOI:** 10.1016/j.ijheatmasstransfer.2018.12.005
**PDF:** Elsevier 구독 필요. ResearchGate 저자 요청 가능; 확보 후 `pdfs/DONG_IJHMT_2019_LBM_MicroPillar.pdf`로 보관
**원문 상태:** abstract 확보; full-text 미확보 (Elsevier 구독 필요)
────────────────────────────────────
**분류:** CFD (Lattice Boltzmann — 마이크로필러 표면 핵비등)
**비등 유형:** 풀비등 (saturated)
**가열 형상:** 평판 (마이크로필러 구조 표면 — 2D/3D 수치 시뮬레이션)
**표면 특성:**
  ├─ 재질: 시뮬레이션 (재질 무관)
  ├─ 거칠기 Ra: 명시 없음 (마이크로필러 높이 H, 간격 W, 직경 D가 체계 변수 — Ra 환산 불가)
  ├─ 접촉각 θ: 명시 변수 (LBM 내 θ 설정 — 수치 범위는 full-text 확인 필요)
  └─ 개질 방법: 시뮬레이션상 마이크로필러 기하 변수(H, W, D) 파라메트릭 스터디
**작동 유체:** 모델 유체 (LBM van der Waals EOS — 물·냉매 직접 매핑 어려움)
**ONB 기준:** 비등 곡선 + 기포 핵생성 시작 과열도 (LBM 시뮬레이션에서 직접 관찰)
**핵심 기여:**
  1. **마이크로필러 높이(H)·간격(W)이 ONB 과열도에 미치는 정량 영향을 LBM으로 규명** — 표면 파라미터 민감도 분석의 CFD reference.
  2. 필러 간격 감소 시 ONB 촉진(ΔT_ONB 저감) 메커니즘 규명 — 공동 포획 유리한 기하 조건 도출.
  3. **Li 2015 / Gong 2015와 함께 LBM 비등 시뮬레이션 카드 그룹(3편) 구성** — CFD 행을 일관성 있게 보강.
  4. 마이크로구조 파라미터 → ONB 민감도 지도 제공 — Surface Encoder 입력 차원 설계의 선험 정보.
**한계점:**
  - LBM 모델 유체 — 실제 유체 물성 매핑 한계
  - 2D 시뮬레이션 위주 — 3D 효과 미반영 가능
  - Ra 단일 수치 매핑 불가 (필러 기하 변수 → Ra 환산식 별도 필요)
  - 접촉각·필러 기하의 교호작용 분석 미흡 (full-text 확인 필요)
**본 연구 활용도:** **방법론 참조 + 데이터 참조**
  - **방법론 참조**: 마이크로필러 표면 파라미터(H, W, D)를 Surface Encoder 입력에 추가할지 결정 시 이 논문의 민감도 분석 결과를 선험 근거로 활용.
  - **데이터 참조**: figure-digitizer로 ΔT_ONB(H, W) 그래프 수치화 → `02_data/raw/literature/DONG_2019/`에 저장하여 LBM 합성 데이터 보완 가능.
  - 갭 매트릭스: **거칠기(마이크로구조) × CFD +1**, **마이크로구조 × CFD +1** (Li/Gong 2015와 함께 CFD 행 강화).
────────────────────────────────────

