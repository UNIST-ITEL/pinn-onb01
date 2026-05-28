# Phase 2 서베이 후보 논문 — Round 2
**작성일**: 2026-05-21
**작성자**: survey-search 에이전트
**목적**: 유형 A–E (냉매 ONB, 표면 개질, 채널 기하, 수평 유동, 고압 조건) 신규 발굴
**기준 DB**: `paper_database_phase2.md` 등록 21편 중복 제외
**신규 후보**: 28편 (유형별 할당 A:8, B:7, C:6, D:3, E:4)

---

## 유형 A — 냉매(R-1234yf / R-32 / R-410A) 유동비등 ONB 실험

### [A01 — Chen et al. 2021]
- **제목**: Experimental study on R-410A subcooled flow boiling heat transfer and bubble behavior inside horizontal annuli
- **저자**: Chen, C. A.; Li, K. W.; Lin, T. F.; Li, W.-K.; Yan, W.-M.
- **저널**: International Communications in Heat and Mass Transfer
- **연도**: 2021
- **DOI**: 10.1016/j.icheatmasstransfer.2021.105274 (미확인 — pii S0735193321001779 기반 추정)
- **키워드**: R-410A, subcooled flow boiling, horizontal annuli, onset of nucleate boiling, bubble behavior, temperature undershoot, annular gap
- **핵심 내용**: R-410A를 냉매로 사용하여 수평 환형 채널(horizontal annuli)에서 subcooled 유동비등 실험 수행. ONB 시 뚜렷한 온도 강하(temperature undershoot) 관찰 및 열유속, 질량유속, 과냉도, 포화온도, 환형 갭이 ONB와 기포 거동에 미치는 영향 정량화. 질량유속·과냉도 증가 시 온도 강하 확대; 열유속 증가 시 기포 크기·형성·이탈 향상 확인.
- **실험 조건**: 유체: R-410A; 기하: 수평 환형 채널; G, ΔT_sub, T_sat, 환형 갭 다중 조건; 압력: R-410A 포화 조건
- **ONB 데이터 수 (추정)**: 20–35 ONB 포인트 (G×ΔT_sub 조합별)
- **디지타이즈 대상 Figure**: boiling curve (q'' vs ΔT_w) + ONB locus (q''_ONB vs G)
- **Phase 2 활용 포인트**: 유형 A 냉매(C2) + 수평 유동 방향(C5) 동시 커버. R-410A CoolProp 지원 여부 확인 필요. ONB temperature undershoot 현상 → Phase 2 불확실도 입력으로 활용 가능.
- **유형**: A + D

---

### [A02 — Comparative Multi-Refrigerant 2021]
- **제목**: Study on heat transfer and bubble behavior inside horizontal annuli: Experimental comparison of R-134a, R-407C, and R-410A subcooled flow boiling
- **저자**: (저자 미확인 — ScienceDirect pii S2214157X21000381)
- **저널**: Case Studies in Thermal Engineering
- **연도**: 2021
- **DOI**: 미확인 (pii S2214157X21000381 기반)
- **키워드**: R-134a, R-407C, R-410A, subcooled flow boiling, horizontal annuli, comparison, ONB, bubble characteristics
- **핵심 내용**: 동일 수평 환형 채널에서 R-134a, R-407C, R-410A 3종 냉매의 subcooled 유동비등 열전달 및 기포 거동 비교 실험. 냉매 종류에 따른 ONB 조건 차이 및 기포 이탈 직경 비교 제공. 단일 기하에서 3개 유체 ONB 데이터 동시 확보 가능.
- **실험 조건**: 유체: R-134a, R-407C, R-410A; 기하: 수평 환형 채널; G, q'', ΔT_sub 다중 조건
- **ONB 데이터 수 (추정)**: 30–50 ONB 포인트 (3유체 × 조건 조합)
- **디지타이즈 대상 Figure**: 냉매별 boiling curve + ONB 비교 그래프
- **Phase 2 활용 포인트**: 다중 냉매 ONB 데이터 — Phase 2 무차원 매니폴드 설계 검증. R-134a (CoolProp 지원) 데이터 즉시 활용 가능. 유체 물성 차이에 따른 ONB 변화 경향 확인.
- **유형**: A

---

### [A03 — Jafari et al. 2016]
- **제목**: Experimental investigation of surface roughness effects on the flow boiling of R134a in microchannels
- **저자**: Jafari, R.; Okutucu-Özyurt, T.; Ünver, H.; Bayer, O.
- **저널**: Experimental Thermal and Fluid Science
- **연도**: 2016
- **DOI**: 10.1016/j.expthermflusci.2016.06.009 (미확인 — Vol. 79, pp. 222–230 기반 추정)
- **키워드**: R-134a, surface roughness, microchannel, flow boiling, heat transfer coefficient, μ-WEDM, two-phase, enhancement
- **핵심 내용**: 마이크로WEDM으로 제작한 3종 표면 거칠기의 마이크로채널(40채널, 700 μm 높이 × 250 μm 폭)에서 R-134a 유동비등 실험. 거칠기 증가 시 두상 열전달계수 최대 45% 향상. 채널 거칠기(Ra)가 ONB 및 HTC에 미치는 영향을 R-134a 냉매로 정량화.
- **실험 조건**: 유체: R-134a; 기하: 직사각형 마이크로채널 40개 병렬 (D_h 추정 400 μm); 표면 거칠기 3수준; G, q'' 다중 조건
- **ONB 데이터 수 (추정)**: 15–25 ONB 포인트 (거칠기 3수준 × G 조건)
- **디지타이즈 대상 Figure**: HTC vs q'' (거칠기별 비교) + boiling curve — ONB 라벨 추출 필요
- **Phase 2 활용 포인트**: 유형 A (냉매 R-134a) + 유형 B (표면 거칠기) 동시. Ra × 냉매 상호작용 데이터 — Phase 2 Surface Encoder + 냉매 입력 결합 검증에 핵심.
- **유형**: A + B

---

### [A04 — Sato Matsumura 1964]
- **제목**: On the Conditions of Incipient Subcooled-Boiling with Forced Convection
- **저자**: Sato, T.; Matsumura, H.
- **저널**: Bulletin of the Japan Society of Mechanical Engineers (JSME)
- **연도**: 1964
- **DOI**: 미확인 (JSME Bulletin Vol. 7, No. 26, pp. 392–398)
- **키워드**: subcooled boiling, forced convection, incipient boiling, ONB correlation, high pressure, analytical, incipience superheat
- **핵심 내용**: 강제대류 subcooled boiling의 핵생성 개시 조건을 해석적으로 유도한 고전 상관식. 가열 표면 온도가 포화 온도와 같다고 가정하고 기포 생성 조건 분석. 고압 조건에서 실험 데이터와 잘 일치하나 과냉 상태에서는 편차 존재. Phase 1 PINN 비교 기준 중 하나인 Sato-Matsumura 상관식 원문.
- **실험 조건**: 물; 수직관; 고압 조건; 강제대류; 다양한 질량유속
- **ONB 데이터 수 (추정)**: 상관식 논문 — 실험 검증점 20–30개
- **디지타이즈 대상 Figure**: q''_ONB vs ΔT_w (상관식 곡선 + 실험 데이터 비교)
- **Phase 2 활용 포인트**: Phase 2 Level 4 비교 기준 상관식 (plan.md §5.1). Bergles-Rohsenow와 함께 강제대류 ONB의 기본 baseline. CoolProp과 결합하여 다중 압력 조건 비교 구현.
- **유형**: A + E

---

### [A05 — Tibiriça et al. 2012]
- **제목**: Flow boiling of R1234yf in a 1 mm diameter channel
- **저자**: Tibiriça, C. B.; Ribatski, G.; Thome, J. R.
- **저널**: International Journal of Refrigeration
- **연도**: 2012
- **DOI**: 10.1016/j.ijrefrig.2012.03.017 (pii S0140700712002861 기반)
- **키워드**: R-1234yf, flow boiling, 1 mm channel, small diameter, HTC, flow pattern, low GWP, refrigerant comparison
- **핵심 내용**: 저GWP 냉매 R-1234yf의 1 mm 직경 수평 원형관 유동비등 실험. R-134a와 비교하여 R-1234yf의 HTC와 유동 패턴 유사성 확인. 소직경 채널에서 핵비등 지배 구간 및 ONB 인근 거동 분석. Thome (EPFL) 그룹의 R-1234yf 마이크로채널 초기 연구.
- **실험 조건**: 유체: R-1234yf (비교: R-134a); 기하: 수평 원형관 D=1 mm; G=100–400 kg/m²s; T_sat=31°C; q''=5–40 kW/m²
- **ONB 데이터 수 (추정)**: ONB 라벨 직접 없음 — boiling curve에서 추출 (10–20포인트)
- **디지타이즈 대상 Figure**: HTC vs 건도 (핵비등 구간), boiling curve (ONB 추출)
- **Phase 2 활용 포인트**: R-1234yf 냉매 데이터 (C2) — CoolProp R-1234yf 지원 확인 필요. Thome/Ribatski 그룹의 검증된 실험 데이터. 1 mm 채널: 마이크로채널 confinement 경계 조건 데이터.
- **유형**: A

---

### [A06 — Comprehensive Review Low-GWP 2023]
- **제목**: A Comprehensive Review on the Nucleate/Convective Boiling of Low-GWP Refrigerants: Alternatives to HFC Refrigerants
- **저자**: (저자 미확인 — MDPI Processes Vol. 11, No. 2, Article 468)
- **저널**: Processes (MDPI)
- **연도**: 2023
- **DOI**: 10.3390/pr11020468 (미확인)
- **키워드**: low-GWP refrigerants, R-1234yf, R-32, R-290, nucleate boiling, convective boiling, review, HFC alternatives
- **핵심 내용**: R-1234yf, R-32, R-290 등 저GWP 냉매의 핵비등/대류비등 열전달 종합 리뷰. 기존 HFC 냉매(R-134a, R-22) 대비 성능 비교 및 ONB 관련 연구 현황 정리. Phase 2에서 냉매 선택 및 데이터 갭 확인에 활용 가능한 리뷰 논문.
- **실험 조건**: 리뷰 논문 — 복수 유체, 채널, 조건 포함
- **ONB 데이터 수 (추정)**: 리뷰 — 개별 실험 데이터 미포함, 문헌 정리용
- **디지타이즈 대상 Figure**: 해당 없음 (리뷰용)
- **Phase 2 활용 포인트**: 냉매 선택 근거 제공 (C2) — R-1234yf, R-32 유동비등 연구 현황 파악. Phase 2 M1 서베이 Reference 구성에 활용.
- **유형**: A

---

### [A07 — Wang et al. 2022 Rod Bundle]
- **제목**: Experimental investigation on onset of nucleate boiling and flow boiling heat transfer in a 5 × 5 rod bundle
- **저자**: Wang et al. (저자 전체 미확인)
- **저널**: Applied Thermal Engineering
- **연도**: 2022
- **DOI**: 10.1016/j.applthermaleng.2022.118263 (검색 기반, 미확인)
- **키워드**: onset of nucleate boiling, rod bundle, 5×5, flow boiling, heat transfer, subcooled, nuclear, high pressure
- **핵심 내용**: 정사각 배열 5×5 수직 핵연료봉 다발에서 subcooled 유동비등 실험 및 ONB 측정. 입구 압력 3.5–7 MPa, 질량유속 250–500 kg/m²s 조건에서 ONB 벽면 과열도 데이터 획득. 질량유속·압력 증가 시 ONB ΔT_w 감소 확인. 신규 ONB 상관식 및 포화 비등 상관식 제안.
- **실험 조건**: 유체: 물; 기하: 5×5 수직 핵연료봉 다발; P=3.5–7 MPa; G=250–500 kg/m²s; q''=180–200 kW/m²; x<0.25
- **ONB 데이터 수 (추정)**: 20–40 ONB 포인트 (P×G 조합별)
- **디지타이즈 대상 Figure**: ONB ΔT_w vs G (압력별), boiling curve — 고압 ONB 포인트
- **Phase 2 활용 포인트**: 고압 ONB (E) + 복잡 기하(봉 다발) 데이터. 핵연료봉 형상: D_h 계산 후 상관식 비교 가능. Phase 2 고압 조건 검증 데이터 확보.
- **유형**: A + E

---

### [A08 — Li et al. 2019 Rod Bundle Low Flow]
- **제목**: Experimental study on onset of nucleate boiling and flow boiling heat transfer in a 5 × 5 rod bundle at low flow rate
- **저자**: Li et al. (저자 전체 미확인)
- **저널**: International Journal of Heat and Mass Transfer
- **연도**: 2019
- **DOI**: 미확인 (pii S0017931018364044 기반)
- **키워드**: ONB, 5×5 rod bundle, flow boiling, low flow rate, subcooled, nuclear, vertical, high pressure
- **핵심 내용**: 저유량(저질량유속) 조건에서 5×5 핵연료봉 다발 유동비등 ONB 실험. A07(Wang 2022)의 선행 연구로 저유량 확장. P=6 MPa, 질량유속 25–200 kg/m²s 조건에서 ONB 측정.
- **실험 조건**: 유체: 물; 기하: 5×5 수직 핵연료봉 다발; P=6 MPa; G=25–200 kg/m²s (저유량); q''=25–75 kW/m²
- **ONB 데이터 수 (추정)**: 15–25 ONB 포인트
- **디지타이즈 대상 Figure**: ONB locus + 저유량 boiling curve
- **Phase 2 활용 포인트**: 저질량유속 ONB 데이터 — 상관식 extrapolation 한계 검증에 활용. Wang 2022와 합산 시 G=25–500 kg/m²s 광범위 커버. 유형 E (고압) 병행.
- **유형**: A + E

---

## 유형 B — 표면 개질 + 강제대류 ONB 실험

### [B01 — Aboubakri et al. 2021]
- **제목**: Effect of Surface Biphilicity on FC-72 Flow Boiling in a Rectangular Minichannel
- **저자**: Aboubakri, A.; Ahmadi, V. E.; Celik, S.; Sadaghiani, A. K.; Sefiane, K.; Kosar, A.
- **저널**: Frontiers in Mechanical Engineering
- **연도**: 2021
- **DOI**: 10.3389/fmech.2021.755580 (확인)
- **키워드**: biphilic surface, FC-72, flow boiling, rectangular minichannel, mixed wettability, hydrophobic island, nucleation enhancement, ONB, bubble fragmentation
- **핵심 내용**: C4F8 소수성 섬(θ=110°)이 실리콘 친수성 기판(θ=55°)에 배열된 biphilic 표면으로 FC-72 직사각형 미니채널 유동비등 실험. 비필릭 표면이 균일 소수성 표면 대비 열전달 50% 향상. 소수성 부위가 핵생성 사이트 밀도 증가 및 slug 흐름 내 기포 파쇄를 유도하여 ONB 개시 저하.
- **실험 조건**: 유체: FC-72; 기하: 직사각형 미니채널 51×15×1 mm; G=90, 130 kg/m²s; q''=2–16 W/cm²; T_in=28°C
- **ONB 데이터 수 (추정)**: 15–25 ONB 포인트 (3표면 × 2질량유속)
- **디지타이즈 대상 Figure**: boiling curve (q'' vs ΔT_w) 표면별 비교 — ONB 포인트 추출
- **Phase 2 활용 포인트**: 비필릭 표면 + 강제대류 ONB 핵심 실험 논문 (갭 매트릭스 복합 개질×유동비등). Phase 2 Surface Encoder의 biphilic 표면 카테고리 직접 근거. FC-72: CoolProp 미지원 확인 필요 (물성 직접 입력 필요).
- **유형**: B

---

### [B02 — Ammerman You 2001]
- **제목**: Enhancing Small-Channel Convective Boiling Performance Using a Microporous Surface Coating
- **저자**: Ammerman, C. N.; You, S. M.
- **저널**: ASME Journal of Heat Transfer
- **연도**: 2001
- **DOI**: 10.1115/1.1388300 (확인)
- **키워드**: microporous coating, small channel, convective boiling, FC-87, boiling incipience, ONB suppression, nucleation site density, CHF enhancement
- **핵심 내용**: FC-87을 유체로 하는 2 mm 정사각 단면 소형 수평 채널에서 마이크로다공성 코팅(microporous coating) 유무에 따른 강제대류 비등 성능 비교. 코팅 적용 시 더 낮은 벽면 과열도에서 비등 개시(ONB 저하) 및 HTC와 CHF 동시 향상. 핵생성 사이트 밀도 증가 메커니즘 규명.
- **실험 조건**: 유체: FC-87; 기하: 수평 2 mm 정사각 채널 (L=8 cm); 코팅 유/무 비교; G, q'' 다중 조건
- **ONB 데이터 수 (추정)**: 10–20 ONB 포인트 (코팅 유무 × 유속 조건)
- **디지타이즈 대상 Figure**: boiling curve (ΔT_w vs q'') 코팅 유무 비교 — ONB 포인트 추출
- **Phase 2 활용 포인트**: 표면 코팅 + 강제대류 ONB (유형 B) — Surface Encoder에 coating_type 범주 입력 근거. 소수성 코팅이 ONB 저하시키는 메커니즘 정량 데이터. FC-87 물성 확인 필요.
- **유형**: B

---

### [B03 — Mixed Wettability Flow Boiling Subatmospheric 2023]
- **제목**: Effect of mixed wettability surfaces on flow boiling heat transfer at subatmospheric pressures
- **저자**: (저자 미확인 — pii S1359431123015053 기반, Sabanci University 그룹 추정)
- **저널**: Applied Thermal Engineering
- **연도**: 2023
- **DOI**: 미확인 (pii S1359431123015053)
- **키워드**: mixed wettability, biphilic surface, flow boiling, subatmospheric pressure, onset of nucleate boiling, heat transfer enhancement, nucleation site density
- **핵심 내용**: 초친수, 초소수, 혼합 젖음성(biphilic) 표면에서 대기압·저압(48, 68, 101 kPa) 유동비등 실험. biphilic 표면이 초친수 대비 최대 28% HTC 향상. ONB가 3.1 K 선행(더 낮은 ΔT_w에서 개시). 저압 조건에서 biphilic 표면의 slug 유동 확장 효과 확인.
- **실험 조건**: 유체: 물(추정); 표면: 초친수/초소수/혼합 젖음성 3종; P=48, 68, 101 kPa; q'' 다중 조건
- **ONB 데이터 수 (추정)**: 20–30 ONB 포인트 (3표면 × 3압력)
- **디지타이즈 대상 Figure**: boiling curve 표면별 비교 + ONB 조건 표 — ONB ΔT_w 값 직접 추출 가능
- **Phase 2 활용 포인트**: 표면 젖음성 + 유동비등 ONB 직접 측정 — Phase 2 Surface Encoder 젖음성 입력 핵심 데이터. 저압 조건: CoolProp 증기압 곡선 검증에 활용. ONB 3.1 K 선행 정량값 → PINN 예측 검증 기준.
- **유형**: B

---

### [B04 — Forrest et al. 2016] (이미 등록됨 — 상세 카드 확인)
- 등록 ID: [FORREST2016] — 중복 제외

---

### [B05 — Jung et al. 2024]
- **제목**: Unveiling the fundamentals of flow boiling heat transfer enhancement on structured surfaces
- **저자**: (저자 미확인 — Science Advances, DOI 10.1126/sciadv.adp8632)
- **저널**: Science Advances
- **연도**: 2024
- **DOI**: 10.1126/sciadv.adp8632 (확인 — PMC11546817)
- **키워드**: structured surface, flow boiling, heat transfer enhancement, boroscopy, bubble dynamics, pore size distribution, aluminum tube, copper tube, nucleation onset
- **핵심 내용**: in situ 보어스코프(boroscopy)로 화학 에칭된 Al/Cu 튜브의 미세 기포 역학을 유동비등 핵생성 시 직접 관찰. Al 구조(나노~마이크로 다중 스케일 기공)에서 최대 391%, Cu에서 41% HTC 향상. 기공 크기 분포(mercury porosimetry)와 열성능 상관관계 최초 규명. ONB 온도가 계층적 표면에서 현저히 감소.
- **실험 조건**: 유체: 물 또는 냉매 (원문 확인 필요); 기하: Al/Cu 에칭 튜브; G, q'' 다중 조건
- **ONB 데이터 수 (추정)**: 10–20 ONB 포인트 (Al/Cu × 조건)
- **디지타이즈 대상 Figure**: ONB 비교 그래프 + HTC vs q'' 표면별 비교
- **Phase 2 활용 포인트**: 나노~마이크로 계층적 구조 표면 + 유동비등 ONB — Phase 2 마이크로구조 표면 카테고리 직접 근거. 기공 크기 분포 → r_c 분포와의 연결 (역문제 설계 참고).
- **유형**: B

---

### [B06 — Subcooled Flow Boiling Roughness Narrow Channel 2024]
- **제목**: Experimental study of the effect of surface roughness on the heat transfer characteristics of subcooled flow boiling in a narrow rectangular channel
- **저자**: (저자 미확인 — pii S030645492400505X, Annals of Nuclear Energy)
- **저널**: Annals of Nuclear Energy
- **연도**: 2024
- **DOI**: 미확인 (pii S030645492400505X)
- **키워드**: surface roughness, subcooled flow boiling, narrow rectangular channel, heat transfer coefficient, ONB, axial ONB location, Hsu criterion modification
- **핵심 내용**: 직사각형 협소 채널에서 Ra=0.34, 1.2, 2.5 μm 3수준으로 표면 거칠기 변화에 따른 subcooled 유동비등 ONB 거동 실험. 거칠기 증가 시 HTC 비선형 증가 및 ONB 위치 상류 이동(더 낮은 열유속에서 개시). Hsu 핵생성 기준 수정 상관식 제안.
- **실험 조건**: 유체: 물; 기하: 협소 직사각형 채널; Ra=0.34/1.2/2.5 μm 3수준; G, q'' 다중 조건; 원자력 냉각 조건
- **ONB 데이터 수 (추정)**: 20–40 ONB 포인트 (3거칠기 × G×q'' 조건)
- **디지타이즈 대상 Figure**: q''_ONB vs G (거칠기별 비교) + ONB axial location vs q''
- **Phase 2 활용 포인트**: 표면 거칠기 × 강제대류 ONB 직접 실험 (갭 매트릭스 거칠기×유동비등 핵심). Phase 2 Surface Encoder Ra 입력 훈련 데이터. Ra=0.34–2.5 μm: Phase 1 Jones 데이터 범위와 중첩 확인 필요.
- **유형**: B

---

### [B07 — ONB Roughness Effect Flow Boiling Subcooled 2015]
- **제목**: On the effect of surface roughness and material on the subcooled flow boiling of water: Experimental study and global correlation
- **저자**: (저자 미확인 — ResearchGate 확인 필요)
- **저널**: Experimental Thermal and Fluid Science (추정)
- **연도**: 2015 (추정)
- **DOI**: 미확인
- **키워드**: surface roughness, material, subcooled flow boiling, water, global correlation, ONB
- **핵심 내용**: 표면 거칠기와 재질(material)이 subcooled 유동비등 ONB 및 열전달에 미치는 영향을 실험적으로 규명하고 전역 상관식 제안. 거칠기+재질 복합 효과의 정량적 분리 시도.
- **실험 조건**: 유체: 물; 거칠기 다수준; 재질 비교; G, q'' 다중 조건
- **ONB 데이터 수 (추정)**: 20–35 ONB 포인트
- **디지타이즈 대상 Figure**: ONB 상관식 vs 실험 비교 + 거칠기별 boiling curve
- **Phase 2 활용 포인트**: 거칠기×재질 복합 효과 분리 — Phase 2 Surface Encoder에 재질(material) 범주 입력 정당화. 원문 접근 후 저자·DOI 확인 필수.
- **유형**: B

---

## 유형 C — 복합 채널 기하 / D_h 연속 변수 ONB

### [C01 — Bertsch Groll Garimella 2009]
- **제목**: A composite heat transfer correlation for saturated flow boiling in small channels
- **저자**: Bertsch, S. S.; Groll, E. A.; Garimella, S. V.
- **저널**: International Journal of Heat and Mass Transfer
- **연도**: 2009
- **DOI**: 10.1016/j.ijheatmasstransfer.2008.10.022 (확인)
- **키워드**: composite correlation, saturated flow boiling, small channels, confinement number, nucleate boiling, convective evaporation, multi-fluid, hydraulic diameter, confinement
- **핵심 내용**: 소형 채널(D_h=0.16–2.92 mm) 포화 유동비등 열전달계수 복합 상관식 개발. 핵비등 + 대류증발 두 항의 복합(superposition) 형태로 구성. 12종 유체·14개 연구의 3899 데이터 포인트 기반. Confinement number(Co=0.3–4.0) 보정 포함. 평균 절대 오차 30% 미만.
- **실험 조건**: 복합 — D_h=0.16–2.92 mm; G=20–3000 kg/m²s; q''=0.4–115 W/cm²; T_sat=−194–97°C; 12종 유체
- **ONB 데이터 수 (추정)**: 상관식 논문 — 개별 ONB 데이터 직접 없음 (HTC 기반)
- **디지타이즈 대상 Figure**: 해당 없음 (상관식 활용)
- **Phase 2 활용 포인트**: Phase 2 Level 4 비교 상관식 중 채널 기하(D_h) + Confinement number 포함 유일 종합 상관식. 복합 구조의 nucleate boiling + convective evaporation 분리 개념 → Phase 2 PINN 손실항 설계 참고. plan.md §5.1 Level 4 필수 구현 대상.
- **유형**: C

---

### [C02 — Harirchian Garimella 2009]
- **제목**: Effects of channel dimension, heat flux, and mass flux on flow boiling regimes in microchannels
- **저자**: Harirchian, T.; Garimella, S. V.
- **저널**: International Journal of Multiphase Flow
- **연도**: 2009
- **DOI**: 10.1016/j.ijmultiphaseflow.2009.01.003 (pii S030193220900007X 기반, 미확인)
- **키워드**: microchannel, flow boiling regimes, channel dimension, nucleate boiling, confinement, bubble confinement, FC-77, flow visualization, regime map
- **핵심 내용**: FC-77을 유체로 7종 채널 폭(100–5850 μm, 깊이 400 μm 고정)에서 고속 촬영으로 유동비등 체제 분류. 채널 폭 400 μm 이상은 핵비등 지배; 250 μm 이하는 기포 핵생성 억제. 채널 치수 감소 → 기포 구속(confinement) 효과 증가 → 핵비등 억제 임계값 결정.
- **실험 조건**: 유체: FC-77; 기하: Si 마이크로채널, 폭 100–5850 μm (7종); G=225–1420 kg/m²s; q'' 다중 조건
- **ONB 데이터 수 (추정)**: ONB 억제 임계 D_h 데이터 (7채널 × G 조건 = 20–30 점)
- **디지타이즈 대상 Figure**: flow regime map (채널 폭 × G) + ONB 억제 경계
- **Phase 2 활용 포인트**: D_h 연속 변수로 ONB/confinement 경계 체계화 — Phase 2 Bo_conf 입력 변수 설계의 실험적 근거. 채널 폭 100–5850 μm 연속 범위 커버. plan.md §3.2 채널 기하 입력 설계 참고.
- **유형**: C

---

### [C03 — Qu Mudawar 2002]
- **제목**: Prediction and measurement of incipient boiling heat flux in micro-channel heat sinks
- **저자**: Qu, W.; Mudawar, I.
- **저널**: International Journal of Heat and Mass Transfer
- **연도**: 2002
- **DOI**: 10.1016/S0017-9310(02)00034-8 (Vol. 45, pp. 3933–3945, 미확인)
- **키워드**: incipient boiling, microchannel heat sink, onset of nucleate boiling, bubble departure diameter, force balance, mechanistic model, water, deionized water
- **핵심 내용**: 마이크로채널 열침(231×713 μm 직사각형)에서 탈이온수 유동비등 ONB 측정 및 기계론적 예측 모델 개발. 기포 이탈 직경을 항력·표면장력 힘 평형으로 산출 후 ONB 열유속 예측. 과냉도 감소 시 ONB 열유속 감소 실험 검증. 고속 촬영으로 ONB 위치 시각 확인.
- **실험 조건**: 유체: 탈이온수; 기하: 직사각형 마이크로채널 231×713 μm; u=0.13–1.44 m/s; ΔT_sub=10, 40, 70 K
- **ONB 데이터 수 (추정)**: 15–25 ONB 포인트 (유속 × 과냉도 조합)
- **디지타이즈 대상 Figure**: q''_ONB vs u (과냉도별) + 기포 이탈 직경 vs q''
- **Phase 2 활용 포인트**: 마이크로채널 ONB 기계론적 모델 — Phase 2 L_ONB_flow 손실항의 기포 이탈 기준 설계 참고. Qu-Mudawar 모델 vs Hsu 모델 비교 → Phase 2 PINN 물리 제약 선택 근거.
- **유형**: C

---

### [C04 — Kandlikar Balasubramanian 2004]
- **제목**: An Extension of the Flow Boiling Correlation to Transition, Laminar, and Deep Laminar Flows in Minichannels and Microchannels
- **저자**: Kandlikar, S. G.; Balasubramanian, P.
- **저널**: Heat Transfer Engineering
- **연도**: 2004
- **DOI**: 10.1080/01457630490280425 (확인)
- **키워드**: flow boiling correlation, minichannels, microchannels, laminar flow, transition flow, deep laminar, nucleate boiling dominant, convective boiling
- **핵심 내용**: 기존 Kandlikar(1990) 유동비등 상관식을 층류(Re<1000) 및 심층류(Re<100) 마이크로/미니채널로 확장. 소형 채널에서 층류 단상 유동 → 핵비등 지배 전환 조건 분석. 저유량 마이크로채널에서 ONB 경계 결정에 Re 의존성 명시.
- **실험 조건**: 물, 냉매 다종; D_h=0.2–2 mm; Re<2300 (층류 조건)
- **ONB 데이터 수 (추정)**: 상관식 + 검증 — 층류 유동비등 데이터 20–40점
- **디지타이즈 대상 Figure**: 유동비등 상관식 vs 실험 비교 (층류 구간)
- **Phase 2 활용 포인트**: 층류 Re 조건 ONB 상관식 — Phase 2 저유량(층류) 영역 baseline 비교 대상. Kandlikar 2004 (마이크로채널 메커니즘, 기등록) + 이 논문 = Kandlikar 1991+2004+2004b 3편 세트로 종합 비교.
- **유형**: C

---

### [C05 — ONB Narrow Rectangular High Pressure 2024]
- **제목**: Experimental study on onset of nucleate boiling in wide-ranged parameters for narrow rectangular channels
- **저자**: (저자 미확인 — pii S030645492400598X, Annals of Nuclear Energy)
- **저널**: Annals of Nuclear Energy
- **연도**: 2024
- **DOI**: 미확인 (pii S030645492400598X)
- **키워드**: onset of nucleate boiling, narrow rectangular channel, wide range, high pressure, ONB correlation, wall superheat, mass flux, heat flux
- **핵심 내용**: 협소 직사각형 채널(60×2.0 mm, w/e=30)에서 고압(10–16 MPa) 광범위 조건의 ONB 실험. ΔT_w_ONB가 열유속과 강한 양의 상관관계, 입구온도·질량유속의 영향은 미미. 평균 오차 −2.71%의 신규 ONB 상관식 제안. 기존 상관식 비교 검증 포함.
- **실험 조건**: 유체: 물; 기하: 협소 직사각형 60×2.0 mm; P=10–16 MPa; G, ΔT_sub, q'' 광범위 조건
- **ONB 데이터 수 (추정)**: 30–50 ONB 포인트 (압력×질량유속×열유속 조합)
- **디지타이즈 대상 Figure**: ΔT_w_ONB vs q'' (압력별), 신규 상관식 vs 실험 비교
- **Phase 2 활용 포인트**: 고압(10–16 MPa) ONB 데이터 — Phase 2 고압 조건(유형 E) 핵심. 채널 종횡비(aspect ratio) = 30 → Phase 2 D_h 입력 설계 검증. 기존 상관식 비교 결과 → Level 4 비교 분석 직접 활용.
- **유형**: C + E

---

### [C06 — ONB Model Rectangular Upward Narrow CFD 2021]
- **제목**: Onset of Nucleate Boiling Model for Rectangular Upward Narrow Channel: CFD Based Approach
- **저자**: (저자 미확인 — pii S0017931020336516, IJHMT)
- **저널**: International Journal of Heat and Mass Transfer
- **연도**: 2021
- **DOI**: 미확인 (pii S0017931020336516)
- **키워드**: onset of nucleate boiling, rectangular narrow channel, CFD, wall superheat, incipience model, upward flow
- **핵심 내용**: 수직 상향 협소 직사각형 채널 ONB 예측에 CFD 기반 접근법 적용. 벽면 온도 분포에서 ONB 조건 수치 결정. 기존 Hsu, Bergles-Rohsenow 상관식 대비 CFD 개선 효과 정량화. 채널 종횡비 효과 포함.
- **실험 조건**: 물; 수직 협소 직사각형 채널; CFD 시뮬레이션 + 실험 검증; G, q'', ΔT_sub 다중 조건
- **ONB 데이터 수 (추정)**: CFD 결과 20–30점 + 실험 검증 10–20점
- **디지타이즈 대상 Figure**: CFD vs 실험 ONB 비교 + 기존 상관식 비교
- **Phase 2 활용 포인트**: CFD × 협소 채널 ONB — 갭 매트릭스 CFD × 채널 기하 셀 보완. Phase 2 합성 데이터 생성(NS+Energy CFD) 방법론 선례. 원문 확인 후 저자·DOI 보완 필요.
- **유형**: C

---

## 유형 D — 수평 유동 방향 ONB

### [D01 — Chen et al. 2021] (A01과 동일 논문, 수평 유동)
- A01 참조 (R-410A 수평 환형 채널 ONB — 유형 A+D 동시 해당)

---

### [D02 — Statistical Method ONB Natural Forced Convection 2021]
- **제목**: Statistical method for determining the onset of nucleate boiling under forced and natural convections in a rectangular channel
- **저자**: (저자 미확인 — pii S0306454920305612, Annals of Nuclear Energy)
- **저널**: Annals of Nuclear Energy
- **연도**: 2021
- **DOI**: 미확인 (pii S0306454920305612)
- **키워드**: onset of nucleate boiling, statistical method, forced convection, natural convection, rectangular channel, ONB detection, temperature-based identification
- **핵심 내용**: 단상 유동에서의 온도-열유속 관계 통계 분석으로 ONB 개시점을 정밀 결정하는 신규 방법론 제안. 강제/자연 대류 양 조건에서 실험 검증. 강제대류에서는 기존 교차점법과 결과 일치; 자연대류에서는 차이 발생 — 방법론 비교 정보 제공.
- **실험 조건**: 유체: 물; 기하: 직사각형 채널; 강제/자연 대류 조건; 입구 온도 다수준
- **ONB 데이터 수 (추정)**: 15–30 ONB 포인트 (유동 조건 × 입구 온도 조합)
- **디지타이즈 대상 Figure**: 통계 방법 vs 기존 방법 ONB 비교 + 보일링 곡선
- **Phase 2 활용 포인트**: ONB 탐지 방법론 — Phase 2 실험 데이터 품질 검증 및 라벨링 방법 표준화에 활용. 강제/자연 대류 ONB 경계 비교 → Phase 1↔Phase 2 연속성 검토.
- **유형**: D

---

### [D03 — Subcooled Flow Boiling Horizontal Circular Pipe 2024]
- **제목**: Subcooled flow boiling in a horizontal circular pipe under high heat flux and high mass flux conditions
- **저자**: (저자 미확인 — pii S0306454924006935, Annals of Nuclear Energy)
- **저널**: Annals of Nuclear Energy
- **연도**: 2024
- **DOI**: 미확인 (pii S0306454924006935)
- **키워드**: subcooled flow boiling, horizontal circular pipe, high heat flux, high mass flux, tube diameter, infrared thermography, local heat transfer coefficient, ONB
- **핵심 내용**: 수평 원형관(D=5.5/7.5/9.5/12 mm 4종)에서 고열유속·고질량유속 조건의 subcooled 유동비등 실험. 적외선 열화상으로 국부 벽면 온도 측정. G=248–2000 kg/m²s, q''=0–1837 kW/m²의 광범위 조건. 수평 유동에서 직경 효과와 ONB 위치 규명.
- **실험 조건**: 유체: 물; 기하: 수평 원형관 D=5.5/7.5/9.5/12 mm; G=248–2000 kg/m²s; q''=0–1837 kW/m²; 저압~중압
- **ONB 데이터 수 (추정)**: 30–50 ONB 포인트 (D×G×q'' 조합)
- **디지타이즈 대상 Figure**: ONB locus (q''_ONB vs G, 직경별) + 국부 HTC 분포 (수평 주변 비대칭)
- **Phase 2 활용 포인트**: 수평 유동 방향(D) + D_h 연속 변수(C) 동시. 수평관 ONB 비대칭 열경계층 → Phase 2 PINN에서 방향성 BC 처리 설계. 적외선 열화상 데이터: 공간 분해 ONB 위치 정보 활용 가능.
- **유형**: D + C

---

## 유형 E — 고압 조건 ONB (원자력 응용)

### [E01 — Sato Matsumura 1964] (A04와 동일 논문, 고압 분류 병행)
- A04 참조 (유형 A + E 동시 해당)

---

### [E02 — ONB OSV OFI Narrow Rectangular 2017]
- **제목**: ONB, OSV, and OFI for subcooled flow boiling through a narrow rectangular channel heated on one-side
- **저자**: (저자 미확인 — pii S0017931017316502, IJHMT)
- **저널**: International Journal of Heat and Mass Transfer
- **연도**: 2017
- **DOI**: 미확인 (pii S0017931017316502)
- **키워드**: ONB, OSV (onset of significant void), OFI (onset of flow instability), subcooled flow boiling, narrow rectangular channel, one-side heating, nuclear
- **핵심 내용**: 편면 가열 협소 직사각형 채널에서 ONB, 현저한 공극 개시(OSV), 유동 불안정 개시(OFI) 세 임계값을 동시 실험 측정. ONB→OSV→OFI 연속 전이 조건 정량화. 원자력 열수력 설계 목적.
- **실험 조건**: 유체: 물; 기하: 협소 직사각형 채널(편면 가열); G, q'', ΔT_sub 다중 조건; 원자력 압력 범위
- **ONB 데이터 수 (추정)**: 20–40 ONB 포인트 (G×q''×ΔT_sub 조합)
- **디지타이즈 대상 Figure**: ONB, OSV, OFI locus 비교 그래프 + 기존 상관식 비교
- **Phase 2 활용 포인트**: ONB 이후 전이 연속 데이터 — Phase 2 부분비등 영역 모델링 한계 설정에 활용. OFI 조건 → Phase 2 불안정성 경계 설계. 기등록 ALYAHIA2017 (Al-Yahia & Jo)와 같은 저널 동일 그룹 가능성 확인 필요.
- **유형**: E

---

### [E03 — Subcooled Boiling High Pressure Vertical Tube 2015]
- **제목**: Subcooled flow boiling heat transfer of water in a circular tube under high heat fluxes and high mass fluxes
- **저자**: (저자 미확인 — pii S0920379615302313, Fusion Engineering and Design)
- **저널**: Fusion Engineering and Design
- **연도**: 2015
- **DOI**: 미확인 (pii S0920379615302313)
- **키워드**: subcooled flow boiling, high heat flux, high mass flux, circular tube, nuclear, fusion, HHHM, ONB, high pressure, vertical
- **핵심 내용**: ITER 다이버터 냉각 조건(고열유속·고질량유속, HHHM)에서 수직 원형관 subcooled 유동비등 실험. P=3, 4.2, 5 MPa; G=6000–10,000 kg/m²s; q''=5–12.5 MW/m²의 극한 조건. ONB 위치를 초기 기포 발생 위치로 정의하여 측정.
- **실험 조건**: 유체: 물; 기하: 수직 원형관 (D=9.0 mm); P=3–5 MPa; G=6000–10,000 kg/m²s; q''=5–12.5 MW/m²; xth=−0.5~−0.03
- **ONB 데이터 수 (추정)**: 20–30 ONB 포인트 (P×G×q'' 조합)
- **디지타이즈 대상 Figure**: ONB 조건 표 + q''_ONB vs G (압력별)
- **Phase 2 활용 포인트**: 극한 고압·고질량유속 ONB 데이터 — Phase 2 적용 범위 한계 설정. 원자력/핵융합 응용 → Phase 2 논문의 산업 응용 절에 인용. 기존 Bergles-Rohsenow 상관식 하한 이탈 조건 확인.
- **유형**: E

---

### [E04 — Frost Dzakowic 1967]
- **제목**: An extension of the method for predicting incipient boiling on commercially finished surfaces
- **저자**: Frost, W.; Dzakowic, G. S.
- **저널**: ASME Paper (비학술지, ASME 콘퍼런스 논문)
- **연도**: 1967
- **DOI**: 미확인 (ASME Paper 67-HT-61)
- **키워드**: incipient boiling, commercially finished surfaces, high pressure, forced convection, ONB prediction, surface roughness, cavity size
- **핵심 내용**: Bergles-Rohsenow(1964)와 Davis-Anderson(1966)의 ONB 예측 방법을 상업적으로 마감된 표면(commercially finished surfaces)으로 확장. 표면 거칠기가 ONB에 미치는 영향을 상업 표면 기준으로 정량화. 고압 강제대류 조건에서 검증.
- **실험 조건**: 물; 강제대류; 고압 조건; 상업 표면 마감 다종 (Ra 암묵적)
- **ONB 데이터 수 (추정)**: 15–25 ONB 포인트 (압력 × 표면 조합)
- **디지타이즈 대상 Figure**: ONB 예측 vs 실험 비교 (연장 상관식)
- **Phase 2 활용 포인트**: 고압 ONB 고전 상관식 (유형 E). Bergles-Rohsenow의 상업 표면 확장 — Phase 2에서 표면 처리 범주를 상관식과 연결하는 역사적 근거. plan.md §5.1 Level 4 비교 대상 후보.
- **유형**: E

---

### [E05 — Thom et al. 1965]
- **제목**: Boiling in subcooled water during flow in tubes and annuli
- **저자**: Thom, J. R. S.; Walker, W. M.; Fallon, T. A.; Reising, G. F. S.
- **저널**: Proceedings of the Institution of Mechanical Engineers
- **연도**: 1965
- **DOI**: 미확인 (IMechE Proceedings)
- **키워드**: subcooled boiling, forced convection, high pressure, ONB correlation, wall superheat, Thom correlation, water, nuclear, tubes, annuli
- **핵심 내용**: 고압(51.7–138 bar) 수직 관·환형관에서 subcooled 유동비등 실험 및 ONB 상관식 제안. Thom 상관식(q''_ONB = f(ΔT_w, P))은 이후 원자력 설계 표준 상관식으로 광범위 인용. Jens-Lottes, Bergles-Rohsenow와 함께 3대 고압 ONB 상관식.
- **실험 조건**: 유체: 물; 기하: 수직 관·환형관; P=51.7–138 bar; 강제대류
- **ONB 데이터 수 (추정)**: 30–50 ONB 포인트
- **디지타이즈 대상 Figure**: q''_ONB vs ΔT_w (압력별 곡선) — Thom 상관식 검증 플롯
- **Phase 2 활용 포인트**: 고압 ONB baseline (유형 E). Bergles-Rohsenow + Davis-Anderson + Sato-Matsumura + Thom = 4개 고전 상관식 완성. Phase 2 논문 §4 "Classical Correlations Comparison"에서 필수 인용.
- **유형**: E

---

## 추가 후보 — Phase 2 방법론 참고

### [M01 — Kim Mudawar 2013]
- **제목**: Universal approach to predicting saturated flow boiling heat transfer in mini/micro-channels — Part I & Part II
- **저자**: Kim, S.-M.; Mudawar, I.
- **저널**: International Journal of Heat and Mass Transfer
- **연도**: 2013
- **DOI**: Part I: 10.1016/j.ijheatmasstransfer.2013.04.016; Part II: 10.1016/j.ijheatmasstransfer.2013.04.017 (미확인)
- **키워드**: universal correlation, saturated flow boiling, mini-channel, micro-channel, multi-fluid, nucleate boiling, convective evaporation, heat transfer
- **핵심 내용**: 다중 유체·다중 채널 크기에 적용 가능한 보편 유동비등 HTC 상관식 개발. 핵비등 + 대류증발의 superposition 형태. 광범위한 데이터베이스(다중 유체·기하·조건)로 검증. 평균 절대 오차 20.3%.
- **실험 조건**: 복합 — 다중 유체; D_h=0.19–6.5 mm; G=19–2000 kg/m²s
- **ONB 데이터 수 (추정)**: 상관식 논문 — HTC 데이터 위주, ONB 직접 라벨 없음
- **디지타이즈 대상 Figure**: 해당 없음 (상관식 활용)
- **Phase 2 활용 포인트**: Bertsch(2009)와 함께 Phase 2 Level 4 비교 상관식. 보편 접근법 → Phase 2 PINN의 다중 유체 일반화 주장 근거. plan.md §5.1.
- **유형**: C (방법론)

---

### [M02 — Cheng et al. 2022 Vertical Channels]
- **제목**: Experimental Study of Onset of Nucleate Boiling in Vertical Rectangular Channels with Different Flow Path Heights
- **저자**: Cheng et al. (기등록 CHENG2022와 동일 — 확인 필요)
- **저널**: Science and Technology of Nuclear Installations
- **연도**: 2022
- **DOI**: 10.1155/2022/7760569 (Hindawi/Wiley, 기등록 CHENG2022)
- **참고**: 기등록 논문 CHENG2022와 동일 가능성 높음 — 중복 확인 후 처리

---

## 요약 표

| # | 후보 ID | 제목 (약칭) | 저자 | 연도 | 저널 | 유형 | DOI 확인 | 우선순위 |
|---|---------|-----------|------|------|------|------|----------|---------|
| 1 | A01 | R-410A subcooled flow boiling horizontal annuli | Chen et al. | 2021 | Int Commun HMT | A+D | 미확인 | ⭐⭐⭐ |
| 2 | A02 | R-134a/R-407C/R-410A comparison horizontal annuli | 미확인 | 2021 | Case Stud Thermal Eng | A | 미확인 | ⭐⭐ |
| 3 | A03 | Surface roughness R134a microchannels flow boiling | Jafari et al. | 2016 | Exp Therm Fluid Sci | A+B | 미확인 | ⭐⭐⭐ |
| 4 | A04 | Incipient subcooled boiling forced convection (Sato-Matsumura) | Sato, Matsumura | 1964 | Bulletin JSME | A+E | 미확인 | ⭐⭐⭐ |
| 5 | A05 | R1234yf flow boiling 1 mm channel | Tibiriça et al. | 2012 | Int J Refrigeration | A | 미확인 | ⭐⭐ |
| 6 | A06 | Review: Nucleate/convective boiling low-GWP refrigerants | 미확인 | 2023 | Processes (MDPI) | A | 미확인 | ⭐ |
| 7 | A07 | ONB and flow boiling 5×5 rod bundle | Wang et al. | 2022 | Appl Thermal Eng | A+E | 미확인 | ⭐⭐ |
| 8 | A08 | ONB rod bundle 5×5 low flow rate | Li et al. | 2019 | Int J HMT | A+E | 미확인 | ⭐⭐ |
| 9 | B01 | Biphilic surface FC-72 flow boiling minichannel | Aboubakri et al. | 2021 | Front Mech Eng | B | 10.3389/fmech.2021.755580 ✅ | ⭐⭐⭐ |
| 10 | B02 | Microporous coating small channel FC-87 | Ammerman, You | 2001 | ASME J Heat Transfer | B | 10.1115/1.1388300 ✅ | ⭐⭐⭐ |
| 11 | B03 | Mixed wettability flow boiling subatmospheric | 미확인 | 2023 | Appl Thermal Eng | B | 미확인 | ⭐⭐⭐ |
| 12 | B05 | Structured surface flow boiling enhancement boroscopy | 미확인 | 2024 | Science Advances | B | 10.1126/sciadv.adp8632 ✅ | ⭐⭐⭐ |
| 13 | B06 | Surface roughness subcooled flow boiling narrow channel | 미확인 | 2024 | Ann Nucl Energy | B | 미확인 | ⭐⭐⭐ |
| 14 | B07 | Roughness+material subcooled flow boiling global correlation | 미확인 | 2015 | 미확인 | B | 미확인 | ⭐⭐ |
| 15 | C01 | Composite correlation small channels (Bertsch) | Bertsch et al. | 2009 | Int J HMT | C | 10.1016/j.ijheatmasstransfer.2008.10.022 ✅ | ⭐⭐⭐ |
| 16 | C02 | Channel dimension effects microchannel flow boiling | Harirchian, Garimella | 2009 | Int J Multiphase Flow | C | 미확인 | ⭐⭐⭐ |
| 17 | C03 | Incipient boiling microchannel heat sinks (Qu-Mudawar) | Qu, Mudawar | 2002 | Int J HMT | C | 미확인 | ⭐⭐⭐ |
| 18 | C04 | Flow boiling correlation laminar deep laminar microchannels | Kandlikar, Balasubramanian | 2004 | Heat Transfer Eng | C | 10.1080/01457630490280425 ✅ | ⭐⭐ |
| 19 | C05 | ONB wide-ranged parameters narrow rectangular channels | 미확인 | 2024 | Ann Nucl Energy | C+E | 미확인 | ⭐⭐⭐ |
| 20 | C06 | ONB model rectangular narrow channel CFD | 미확인 | 2021 | Int J HMT | C | 미확인 | ⭐⭐ |
| 21 | D02 | Statistical method ONB forced natural convection | 미확인 | 2021 | Ann Nucl Energy | D | 미확인 | ⭐⭐ |
| 22 | D03 | Subcooled flow boiling horizontal circular pipe | 미확인 | 2024 | Ann Nucl Energy | D+C | 미확인 | ⭐⭐⭐ |
| 23 | E02 | ONB OSV OFI narrow rectangular one-side heated | 미확인 | 2017 | Int J HMT | E | 미확인 | ⭐⭐ |
| 24 | E03 | Subcooled boiling high heat flux ITER conditions | 미확인 | 2015 | Fusion Eng Design | E | 미확인 | ⭐⭐ |
| 25 | E04 | Frost-Dzakowic 1967 incipient boiling commercial surfaces | Frost, Dzakowic | 1967 | ASME Paper | E | 미확인 | ⭐⭐ |
| 26 | E05 | Thom et al. 1965 subcooled boiling high pressure | Thom et al. | 1965 | IMechE Proc | E | 미확인 | ⭐⭐ |
| 27 | M01 | Universal correlation mini/micro-channel Kim-Mudawar | Kim, Mudawar | 2013 | Int J HMT | C | 미확인 | ⭐⭐ |

**총 신규 후보**: 27편 (기등록 21편 제외, A01/A04 유형 복수 해당 제외 시 순수 신규)
**DOI 확인 완료**: B01, B02, B05, C01, C04 — 5편
**DOI 미확인**: 22편 (원문 접근 후 CrossRef/Semantic Scholar 검증 필요)

---

## Top 3 추천 (Full Text 확보 우선순위)

### 1위: B01 — Aboubakri et al. 2021 (DOI 확인 ✅)
- **이유**: biphilic 표면 + FC-72 강제대류 ONB 직접 측정 — 갭 매트릭스 복합 개질×유동비등 공백을 가장 직접 채우는 논문. DOI 확인 완료. 오픈 액세스(Frontiers) 논문으로 전문 접근 용이.

### 2위: B06 — 표면 거칠기 × 협소 직사각형 채널 ONB 2024 (DOI 미확인)
- **이유**: 표면 거칠기(Ra=0.34/1.2/2.5 μm) × 강제대류 ONB 직접 실험 — Phase 2 Surface Encoder Ra 입력 훈련 데이터 확보에 필수. 2024년 신규 논문으로 최근성 높음.

### 3위: C01 — Bertsch Groll Garimella 2009 (DOI 확인 ✅)
- **이유**: D_h 연속 변수 + Confinement number 포함 다중 유체 composite 상관식 — Phase 2 Level 4 비교 상관식 중 채널 기하 커버의 유일한 종합 논문. DOI 확인 완료.

---

## 다음 단계

이 중 어떤 논문을 카드화할까요?

1. **즉시 카드화 가능** (DOI 확인 완료 5편): B01, B02, B05, C01, C04
2. **DOI 확인 후 카드화** (22편): 원문 접근 → CrossRef/Semantic Scholar 검증 → paper-card-extractor 위임
3. **저자 확인 필요** (A02, A06, B03, B07, C05, C06, D02, D03, E02, E03): ScienceDirect pii 기반 접근 또는 ResearchGate 확인

**유형별 확보 현황**:
- 유형 A (냉매): 8편 후보 (목표 10편 — 2편 추가 탐색 권장)
- 유형 B (표면 개질): 6편 후보 (목표 8편 — 2편 추가 탐색 권장)
- 유형 C (채널 기하): 6편 후보 (목표 7편 — 1편 추가 탐색 권장)
- 유형 D (수평 유동): 3편 후보 (목표 4편 — A01 중복 포함 시 달성)
- 유형 E (고압): 5편 후보 (목표 4편 — 초과 달성)

---

## 갱신 이력

| 날짜 | 변경 내용 |
|------|---------|
| 2026-05-21 | 초기 작성 — Round 2 신규 후보 27편 등록 |
