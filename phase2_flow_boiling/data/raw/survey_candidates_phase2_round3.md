# Phase 2 Survey Candidates — Round 3
**작성일**: 2026-05-22
**검색자**: survey-search agent (Claude Sonnet 4.6)
**검색 목적**: 44편 보유 → 50편 목표, 4개 갭(A/B/C/D) 보강

---

## 검색 전략 요약

| 갭 | 설명 | 검색 쿼리 |
|----|------|----------|
| A | 냉매별 ONB (R-32, R-1234ze, R-1234yf, 저GWP) | R-32/R-1234ze "onset of nucleate boiling" flow boiling subcooled experiment |
| B | 표면 개질 + 강제대류 ONB (거칠기·젖음성·코팅) | surface roughness/wettability flow boiling ONB forced convection channel |
| C | 채널 기하 효과 (Dh 범위, 종횡비) | hydraulic diameter aspect ratio onset nucleate boiling comparison multiple |
| D | 최근(2020–2025) 강력 논문 (ML/실험) | flow boiling ONB prediction machine learning PINN 2022–2025 |

**중복 제거 기준**: 기존 44편 DB (`paper_database_phase2.md`) + Round 1·2 후보 목록(`survey_candidates_phase2.md`, `survey_candidates_phase2_round2.md`) 대조 완료.

---

## 후보 논문 목록

| # | 제목 | 저자 | 연도 | 저널 | 갭 셀 | DOI 상태 | 우선순위 |
|---|------|------|------|------|-------|----------|---------|
| 1 | Experimental data review for boiling incipience at subcooled flow boiling and new dimensionless correlation | Conde-Fontenla, Paz, Cabarcos, Concheiro | 2024 | Int J Heat Mass Transfer | D (다중유체 ONB 리뷰+상관식) | 10.1016/j.ijheatmasstransfer.2024.126007 ✅ | ⭐⭐⭐ |
| 2 | Experimental study of the effect of surface roughness on the heat transfer characteristics of subcooled flow boiling in a narrow rectangular channel | Zou, Li, Li, Sui, Qiao, Tan, Tian | 2025 (공개 2024) | Annals of Nuclear Energy | B (거칠기×강제대류 ONB) | 10.1016/j.anucene.2024.110842 ✅ | ⭐⭐⭐ |
| 3 | ONB, OSV, and OFI for subcooled flow boiling through a narrow rectangular channel heated on one-side | Al-Yahia, Jo | 2018 | Int J Heat Mass Transfer | C+D (채널기하+ONB전이경계) | DOI 미확인 (pii: S0017931017316502) | ⭐⭐ |
| 4 | The effect of surface wettability on flow boiling characteristics within microchannels | Vontas et al. | 2021 | Int J Heat Mass Transfer | B (젖음성×강제대류 ONB) | DOI 미확인 (pii: S0017931021002362) | ⭐⭐ |
| 5 | Experimental investigation on flow boiling characteristics of R1233zd(E) in a parallel mini-channel heat sink for battery thermal management | (저자 미확인) | 2021 | Int J Heat Mass Transfer | A (저GWP 냉매 ONB) | DOI 미확인 (pii: S0017931021006943) | ⭐⭐ |
| 6 | Experimental Study of Onset of Nucleate Boiling in Vertical Rectangular Channels with Different Flow Path Heights | Cheng, Yu, Xiao, Peng | 2022 | Science and Technology of Nuclear Installations | C (채널 높이별 ONB 비교) | 10.1155/2022/7760569 ✅ | ⭐ |
| 7 | Experimental study on onset of nucleate boiling in wide-ranged parameters for narrow rectangular channels | (저자 미확인) | 2024 | Annals of Nuclear Energy | C+D (광범위 파라미터 ONB) | DOI 미확인 (pii: S030645492400598X) | ⭐⭐ |
| 8 | Addressing the synergistic effect of hydraulic diameter and aspect ratio on experimental flow boiling in microchannels | Qin, Widyatama, Zhang, Passos, Sefiane, Li, Orejon | 2025 | Applied Thermal Engineering | C (Dh+AR 시너지 효과) | 10.1016/j.applthermaleng.2025.126566 ✅ | ⭐ |
| 9 | Enhanced subcooled flow boiling in microchannels integrated with nanoporous graphene coatings of distinctive wettability | (저자 미확인) | 2025 | Int J Heat Mass Transfer | B (코팅 젖음성×ONB) | DOI 미확인 (pii: S0017931025004065) | ⭐⭐ |

---

## 개별 논문 상세

---

### 후보 1 — CONDEFONTENLA2024

- **제목**: Experimental data review for boiling incipience at subcooled flow boiling and new dimensionless correlation
- **저자**: Marcos Conde-Fontenla, Concepción Paz, Adrián Cabarcos, Miguel Concheiro
- **저널**: International Journal of Heat and Mass Transfer
- **연도**: 2024 (11월 출판)
- **권/호/페이지**: Vol. 233, Article 126007
- **DOI**: 10.1016/j.ijheatmasstransfer.2024.126007 ✅ CrossRef 검증됨
- **갭 셀**: D (최근 강력 논문 — 다중 유체 ONB 데이터 리뷰 + 새 무차원 상관식)

**Abstract 요약 (검색 결과 기반)**:
- 강제대류 subcooled 비등의 핵비등 개시(ONB) 데이터를 체계적으로 재검토하고 새 무차원 상관식 제안.
- 자체 실험(50% vol 에틸렌글리콜-물 혼합물, 수평 직사각형 채널)에서 신규 ONB 데이터 생성.
- 기존 문헌 12편에서 추출한 데이터 포함, **총 6종 유체** 데이터 통합.
- 기존 상관식(Bergles-Rohsenow, Davis-Anderson 등)의 오차 분석과 함께 새 무차원 상관식의 정확도 검증.

**예상 ONB 데이터 포인트**: 다중 유체·다중 조건 합산으로 50+ 포인트 추정 (원문 확인 필요).

**Phase 2 활용 포인트**:
- 다중 유체(물, 에틸렌글리콜 혼합물, 냉매 등) ONB 데이터 → Phase 2 학습셋 다양성 보강.
- 새 무차원 상관식 → Phase 2 baseline 비교 상관식 후보.
- 6종 유체 커버리지 → PINN 무차원화 설계 검증에 활용.

**중복 확인**: 기존 DB에 없음. Round 1·2 후보에 없음. ✅ 신규.

**Top 3 추천 이유**: Gap D를 직접 충족하는 2024년 최신 실험·리뷰 논문. CrossRef DOI 검증 완료. 다중 유체 데이터셋으로 Phase 2 PINN 학습셋 강화 가능.

---

### 후보 2 — ZOUETAL2025

- **제목**: Experimental study of the effect of surface roughness on the heat transfer characteristics of subcooled flow boiling in a narrow rectangular channel
- **저자**: Yu Zou, Jinyang Li, Tangyu Li, Xinru Sui, Shouxu Qiao, Sichao Tan, Ruifeng Tian
- **저널**: Annals of Nuclear Energy
- **연도**: 2025 출판 (공개일 2024년)
- **권/페이지**: Vol. 210, Article 110842
- **DOI**: 10.1016/j.anucene.2024.110842 ✅ CrossRef 검증됨
- **갭 셀**: B (표면 거칠기 × 강제대류 ONB — 협소 직사각형 채널)

**Abstract 요약 (검색 결과 기반)**:
- 협소 직사각형 채널에서 표면 거칠기(Ra = 0.34 μm, 1.2 μm, 2.5 μm) 3가지 조건에 따른 subcooled 유동비등 ONB 위치 및 열전달 특성 시각화 실험.
- 거칠기 증가 → ONB 위치가 유동 상류 방향으로 이동(ONB 조기 발생).
- 열전달계수(HTC)는 거칠기와 비선형 관계.
- Hsu 핵생성 기준을 거칠기 조건에 맞게 수정한 경험 상관식 제안.

**예상 ONB 데이터 포인트**: Ra 3개 조건 × 다수 열유속/유속 조건 → 20–40 포인트 추정.

**Phase 2 활용 포인트**:
- 표면 거칠기(Ra) → 강제대류 ONB 직접 연결 데이터 (Phase 1 풀비등과의 연속성 확인).
- Phase 2 Surface Encoder에 Ra 입력 변수 정당화.
- 수정 Hsu 기준 → Phase 2 `L_ONB_flow` 손실함수 참조.

**주의**: Round 2 후보 B06에 이미 placeholder로 등록(DOI 미확인 상태). 본 Round 3에서 DOI 검증 완료. **B06 항목을 이 DOI로 갱신 요망**.

**중복 확인**: 기존 DB에 없음. Round 2에 B06 placeholder 존재 → DOI 확인 신규 정보 제공. ✅

**Top 3 추천 이유**: Gap B의 핵심 논문. DOI CrossRef 검증 완료. 물+협소채널 조건에서 Ra별 ONB 위치 이동 정량 데이터 — Phase 2 학습셋에 고가치.

---

### 후보 3 — ALYAHIA2018

- **제목**: ONB, OSV, and OFI for subcooled flow boiling through a narrow rectangular channel heated on one-side
- **저자**: Omar S. Al-Yahia, Daeseong Jo
- **저널**: International Journal of Heat and Mass Transfer
- **연도**: 2018
- **권/페이지**: Vol. 116, pp. 136–151
- **DOI**: DOI 미확인 (pii: S0017931017316502). CrossRef 조회 실패 — **DOI 미확인**으로 표기.
- **갭 셀**: C+D (협소 채널 기하 + ONB/OSV/OFI 경계 동시 측정)

**Abstract 요약 (검색 결과 기반)**:
- 편면 가열 협소 직사각형 채널(gap 2.35 mm × 54 mm, 가열길이 300 mm)에서 수직 상향류(물) 조건으로 ONB, 현저한 공극 개시(OSV), 유동 불안정 개시(OFI) 세 임계 열수력 경계를 동시 실험.
- 입구 온도 35–65°C, 질량유속 118–1,400 kg/(m²s), 열유속 50–650 kW/m² 광범위 조건.
- ONB→OSV→OFI 순서로 발생. OFI 예측 새 상관식 개발.

**예상 ONB 데이터 포인트**: 광범위 조건 → 30–50 ONB 포인트 추정.

**Phase 2 활용 포인트**:
- ONB 이후 OSV·OFI 연속 데이터 → Phase 2 부분 비등 영역 물리 경계 설계 참조.
- 편면 가열 협소 채널 → 원자로 냉각 채널과의 비교 기준.
- 기존 ALYAHIA2017(Annals Nuclear Energy)과 다른 논문임 — 저자 동일, 저널 다름 확인.

**주의**: Round 2 후보 E02에 이미 placeholder로 등록(DOI 미확인 상태). 본 Round 3에서 저자, 권, 페이지 확인. DOI는 CrossRef 미검증.

---

### 후보 4 — VONTAS2021

- **제목**: The effect of surface wettability on flow boiling characteristics within microchannels
- **저자**: Vontas et al. (저자 성명 미확인, 그리스계 연구그룹 추정)
- **저널**: International Journal of Heat and Mass Transfer
- **연도**: 2021 (3월 출판)
- **DOI**: DOI 미확인 (pii: S0017931021002362). **DOI 미확인**.
- **갭 셀**: B (젖음성 × 강제대류 ONB — 마이크로채널)

**Abstract 요약 (검색 결과 기반)**:
- 직사각형 마이크로채널에서 4가지 접촉각 조건(SiOx 26°, Ti 49°, DLC 63°, SiOC 104°) 표면의 유동비등 특성 비교 실험.
- 접촉각 증가 → ONB 발생 과열도 감소(소수성 → ONB 조기 발생).
- 친수성 채널: 핵비등 종료 후 Nu 43.9% 향상. 소수성: 17.8% 향상.
- 버블 핵생성·성장·이탈에 대한 젖음성 영향 메커니즘 분석.

**예상 ONB 데이터 포인트**: 4가지 표면 × 다수 열유속/유속 → 15–30 ONB 포인트 추정.

**Phase 2 활용 포인트**:
- 접촉각(θ) → 강제대류 ONB 직접 연결 — Phase 2 Surface Encoder θ 입력 정당화.
- 마이크로채널 강제대류 ONB θ 의존성 데이터 (Phase 1 풀비등 θ 데이터와의 연속성).
- Basu et al. (2002) F(θ) 의존성 Phase 2 확장 검증에 활용.

**중복 확인**: 기존 DB에 없음. Round 1·2 후보에 없음. ✅ 신규.

---

### 후보 5 — R1233ZD2021

- **제목**: Experimental investigation on flow boiling characteristics of R1233zd(E) in a parallel mini-channel heat sink for the application in battery thermal management
- **저자**: 미확인 (저자 성명 원문 확인 필요)
- **저널**: International Journal of Heat and Mass Transfer
- **연도**: 2021 (6월 출판)
- **DOI**: DOI 미확인 (pii: S0017931021006943). **DOI 미확인**.
- **갭 셀**: A (저GWP HFO 냉매 ONB — R-32/R-1234ze 직접은 아니지만 동계열 HFO)

**Abstract 요약 (검색 결과 기반)**:
- R1233zd(E) (저GWP HFO 냉매, GWP≈1) 평행 미니채널(21채널, 단면 1.5 × 1.5 mm², 길이 140 mm) 배터리 냉각 응용 실험.
- 포화압력 125 kPa, 열유속 5–100 kW/m², 질량유속 150–600 kg/(m²s), 과냉도 2.5–8 K.
- **ONB 지연 현상 정량 확인**: 질량유속 및 과냉도 증가 → ONB 지연. 유동 패턴 시각화로 전이 검증.

**예상 ONB 데이터 포인트**: 질량유속 × 과냉도 매트릭스 → 15–25 ONB 포인트 추정.

**Phase 2 활용 포인트**:
- 저GWP HFO 냉매 ONB 실험 → Gap A (R-32/R-1234ze 대안으로 동계열 HFO 확보).
- 배터리 냉각 마이크로채널 조건 → Phase 2 응용 확장.
- CoolProp R1233zd(E) 지원 여부 확인 필요.

**중복 확인**: 기존 DB에 없음. Round 1·2 후보에 없음. ✅ 신규.

---

### 후보 6 — CHENG2022 (이미 DB 등록, DOI 검증 완료)

- **제목**: Experimental Study of Onset of Nucleate Boiling in Vertical Rectangular Channels with Different Flow Path Heights
- **저자**: Ning Cheng, Shuwen Yu, Jun Xiao, Chang-Hong Peng
- **저널**: Science and Technology of Nuclear Installations
- **연도**: 2022
- **DOI**: 10.1155/2022/7760569 ✅ CrossRef 검증됨
- **갭 셀**: C (채널 높이 비교 ONB)

**주의**: 기존 DB(`paper_database_phase2.md`, CHENG2022)에 이미 등록됨. Round 3 에서는 DOI 검증 완료 보고만 수행.

---

### 후보 7 — ONBWIDEPARAMS2024

- **제목**: Experimental study on onset of nucleate boiling in wide-ranged parameters for narrow rectangular channels
- **저자**: 미확인 (원문 확인 필요)
- **저널**: Annals of Nuclear Energy
- **연도**: 2024 (9월 출판)
- **DOI**: DOI 미확인 (pii: S030645492400598X). **DOI 미확인**.
- **갭 셀**: C+D (광범위 조건 ONB 실험 + 새 상관식)

**Abstract 요약 (검색 결과 기반)**:
- 압력 0.1–5.5 MPa, 질량유속 200–2,000 kg/(m²s), 과냉도 10–150 K 광범위 파라미터 범위에서 협소 직사각형 채널 ONB 실험.
- 열수력 파라미터·채널 치수가 ONB에 미치는 영향 분석.
- 새 ONB 상관식 개발.

**예상 ONB 데이터 포인트**: 광범위 파라미터 → 50+ 포인트 추정.

**Phase 2 활용 포인트**:
- 매우 넓은 압력·유속 조건 → Phase 2 학습셋 압력 의존성 커버리지 보강.
- 새 상관식 → Phase 2 baseline 비교 대상 추가.

**주의**: Round 2 후보 C05에 이미 placeholder로 등록. DOI 아직 미확인.

---

### 후보 8 — QINETAL2025

- **제목**: Addressing the synergistic effect of hydraulic diameter and aspect ratio on experimental flow boiling in microchannels
- **저자**: Luwen Qin, Arif Widyatama, Ningxi Zhang, Júlio Cesar Passos, Khellil Sefiane, Shuhong Li, Daniel Orejon
- **저널**: Applied Thermal Engineering
- **연도**: 2025 (9월 출판)
- **권/호**: Vol. 274, Article 126566
- **DOI**: 10.1016/j.applthermaleng.2025.126566 ✅ CrossRef 검증됨
- **갭 셀**: C (Dh × 종횡비 시너지 효과)

**Abstract 요약 (검색 결과 기반)**:
- Dh = 727, 762, 909 μm, 종횡비(AR) 10 및 20 직사각형 마이크로채널에서 유동비등 특성 실험.
- 작동 유체: HFE-7000 (T_sat = 34°C).
- ONB는 Dh 및 유속에 더 민감하고 AR에는 덜 민감.
- ONB 측정 포함 확인됨.

**예상 ONB 데이터 포인트**: 3채널 × 다수 조건 → 10–20 ONB 포인트 추정.

**Phase 2 활용 포인트**:
- Dh × AR 동시 변화 ONB 데이터 → Phase 2 채널 기하 입력(Dh, AR) 변수 정당화.
- HFE-7000 냉매: CoolProp 지원 여부 확인 필요.
- Gap C 직접 충족.

**중복 확인**: 기존 DB에 없음. Round 1·2 후보에 없음. ✅ 신규.

---

### 후보 9 — GNPWET2025

- **제목**: Enhanced subcooled flow boiling in microchannels integrated with nanoporous graphene coatings of distinctive wettability
- **저자**: 미확인 (저자 성명 원문 확인 필요)
- **저널**: International Journal of Heat and Mass Transfer
- **연도**: 2025 (4월 출판)
- **DOI**: DOI 미확인 (pii: S0017931025004065). **DOI 미확인**.
- **갭 셀**: B (나노 코팅 젖음성 × ONB — 마이크로채널)

**Abstract 요약 (검색 결과 기반)**:
- 그래핀 나노플레이트(GNP) 코팅으로 마이크로채널 표면 젖음성 제어: 초친수성(SHi), 초소수성(SHo), 이중 젖음성(U-GNP) 비교.
- 기준(U-GNP) 코팅이 Nu 143% 향상, 표면 온도 최대 25°C 감소.
- ONB 발생 조건 및 코팅 종류에 따른 ONB 거동 차이 보고.

**예상 ONB 데이터 포인트**: 3–4 코팅 조건 × 다수 열유속 → 10–20 ONB 포인트 추정.

**Phase 2 활용 포인트**:
- 나노 코팅 젖음성 → ONB 이동 정량 데이터 (Gap B 직접 보강).
- 초소수성·초친수성 극단값 포함 → Phase 2 θ 입력 범위 확장.

**중복 확인**: 기존 DB에 없음. Round 1·2 후보에 없음. ✅ 신규.

---

## 갭별 충족 현황 요약

| 갭 | 목표 | 이번 Round 3 후보 | 상태 |
|----|------|-------------------|------|
| A — 냉매별 ONB (R-32, R-1234ze, 저GWP) | 2편 | 후보 5 (R1233zd 2021) | 부분 충족 — R-32·R-1234ze 직접 ONB 데이터는 문헌에 극히 희소. R1233zd(E)가 현실적 대안. |
| B — 표면 개질 + 강제대류 ONB | 2편 | 후보 2 (Zou 2024), 후보 4 (Vontas 2021), 후보 9 (GNP 2025) | 3편 발굴 → 충분 |
| C — 채널 기하 효과 | 1편 | 후보 3 (Al-Yahia 2018), 후보 7 (Wide-params 2024), 후보 8 (Qin 2025) | 3편 발굴 → 충분 |
| D — 최근 ONB 예측 강력 논문 | 1편 | 후보 1 (Conde-Fontenla 2024) | 충족 |

---

## Top 3 추천 (full text 확보 우선순위)

**1순위: 후보 1 — CONDEFONTENLA2024**
DOI 검증 완료. 2024년 IJHMT. 6종 유체 ONB incipience 데이터 통합 리뷰 + 새 무차원 상관식. Phase 2 Gap D를 직접 충족하며 다중 유체 데이터셋 확보 가능. PINN 손실함수 설계 참조에도 활용 가능.

**2순위: 후보 2 — ZOUETAL2025**
DOI 검증 완료. 2025년 Annals of Nuclear Energy. 표면 거칠기(Ra) → 강제대류 ONB 위치 이동 정량 데이터. Round 2 B06 placeholder DOI 갱신 가능. Gap B 핵심.

**3순위: 후보 4 — VONTAS2021**
DOI 미확인이나 pii 확인됨. 2021년 IJHMT. 접촉각 θ(26°–104°) 4단계에 따른 마이크로채널 유동비등 ONB 데이터. Phase 2 Surface Encoder θ 입력 정당화 및 Basu(2002) θ 의존성 Phase 2 확장 검증에 핵심.

---

## 후속 조치 사항

| 항목 | 설명 |
|------|------|
| DOI 확인 필요 | 후보 3 (Al-Yahia 2018), 후보 4 (Vontas 2021), 후보 5 (R1233zd 2021), 후보 7 (Wide-params 2024), 후보 9 (GNP 2025) |
| 기존 DB 갱신 | Round 2 B06 → 후보 2 DOI 갱신 (`10.1016/j.anucene.2024.110842`); C05 → 후보 7 DOI 갱신 필요; E02 → 후보 3 저자·권·페이지 갱신; CHENG2022 → DOI 검증 완료 표시 |
| Gap A 미충족 | R-32 및 R-1234ze(E) 직접 ONB 데이터는 문헌 공백이 실재. R1233zd(E)(후보 5)로 부분 대체 또는 갭을 Phase 2 논문의 연구 동기로 활용 권장. |
| CoolProp 지원 확인 | HFE-7000 (후보 8), R1233zd(E) (후보 5) — CoolProp 지원 여부 검토 필요. |

---

## 검색 이력

| 날짜 | 검색 쿼리 | 결과 |
|------|----------|------|
| 2026-05-22 | R-32 onset nucleate boiling flow boiling subcooled ONB experiment | R-32 직접 ONB 데이터 미발견 |
| 2026-05-22 | R-1234ze R-1234yf HFO refrigerant onset nucleate boiling flow boiling | HFO ONB 데이터 희소 확인 |
| 2026-05-22 | surface roughness wettability hydrophobic flow boiling ONB onset nucleate boiling channel | 후보 2, 4, 9 발굴 |
| 2026-05-22 | hydraulic diameter aspect ratio channel geometry onset nucleate boiling comparison | 후보 3, 7, 8 발굴 |
| 2026-05-22 | flow boiling onset nucleate boiling prediction machine learning neural network 2022–2025 | 후보 1 발굴 |
| 2026-05-22 | "experimental data review" boiling incipience subcooled flow boiling 2024 | 후보 1 DOI 확인 |
| 2026-05-22 | R1233zd flow boiling mini-channel onset nucleate boiling 2021 | 후보 5 발굴 |
| 2026-05-22 | subcooled flow boiling wettability contact angle microchannel ONB experiment 2020–2024 | 후보 4 발굴 |
| 2026-05-22 | graphene nanoporous subcooled flow boiling wettability ONB 2025 | 후보 9 발굴 |
