# Phase 2 Flow Boiling ONB — 디지타이즈 작업 가이드

**작성일**: 2026-05-21
**담당**: Jaeseon Lee (leejs92@gmail.com)
**목표**: 300+ ONB 라벨 확보 (M1 Go/No-Go 기준)
**저장 경로**: `phase2_flow_boiling/data/raw/literature/`
**최종 통합 파일**: `phase2_flow_boiling/data/raw/onb_dataset_phase2.csv`

---

## 목차

1. 도구 선택 및 설치
2. 논문별 타겟 Figure 목록
3. 디지타이즈 절차 (단계별)
4. 데이터 저장 형식 (CSV 스키마)
5. 물리적 타당성 검증 체크리스트
6. 파일 저장 위치 및 네이밍 규칙
7. 단계별 진척 추적

---

## 1. 도구 선택 및 설치

### 1.1 WebPlotDigitizer 접근 방법

**웹 버전 (권장)**: https://automeris.io/wpd/
- 설치 불필요. Chrome/Edge/Firefox 최신 버전에서 동작.
- 세션 저장: `.tar` 파일로 내보내기 가능 (작업 중단 후 재개 지원).
- 단점: 인터넷 연결 필요.

**데스크탑 버전**: https://github.com/ankitrohatgi/WebPlotDigitizer/releases
- macOS: `.dmg` 파일 다운로드 후 설치.
- 오프라인 작업 가능. PDF에서 Figure 페이지 직접 스크린샷 권장.

### 1.2 초기 설정

**Figure 이미지 준비**:
- PDF에서 대상 Figure를 고해상도(300 dpi 이상)로 crop 또는 전체 페이지 스크린샷.
- 도구: macOS Preview (cmd+shift+4 영역 선택), Adobe Acrobat "스냅샷" 기능.
- 저장 형식: PNG (JPEG는 압축 아티팩트가 좌표 정밀도에 영향).

**WebPlotDigitizer 기본 설정**:
1. 웹 접속 후 "Load Image" → PNG 파일 업로드.
2. Plot type: "2D (X-Y) Plot" 선택 (log scale의 경우도 동일 선택).
3. 축 보정(Axis Calibration) 수행 (2.2절 참조).

---

## 2. 논문별 타겟 Figure 목록

우선순위 P1~P6 순으로 정렬. 각 Figure의 축 변수, 단위, 스케일, 예상 포인트 수를 명시.

---

### P1 — Basu, Warrier, Dhir (2002) [BASU2002]
**DOI**: 10.1115/1.1471522 | **예상 ONB 포인트**: ~50개

> **⚠️ PDF 확인 결과 (2026-05-21)**: 이전 가이드의 Fig.3/5/7은 모두 실험장치 도면·사진으로 ONB 데이터 없음.
> - Fig.3 = 평판 시험부 단면도 (schematic cross section)
> - Fig.5 = 시험부 조립 사진 (photograph of test chamber)
> - Fig.7 = 열전대 배치 단면도 (thermocouple arrangement)
> 실제 ONB 데이터는 아래 Fig.9/10/11/12에 있음.

| Figure | 설명 | x축 (단위) | y축 (단위) | 스케일 | 시리즈 수 | 우선도 |
|--------|------|-----------|-----------|--------|---------|--------|
| Fig. 9 | ONB 위치 (ΔT_ONB) — 다양한 유동 조건 (G, θ) | ΔT_wall (°C) 또는 q'' | ΔT_ONB (°C) 또는 ONB locus | linear/log | 3~5 (G·θ 조합) | ★★★ |
| Fig. 10 | 예측 vs 실험 ΔT_ONB parity plot | ΔT_ONB,pred (°C) | ΔT_ONB,exp (°C) | linear | 1 | ★★★ |
| Fig. 11 | 예측 vs 실험 q''_ONB parity plot | q''_ONB,pred (W/m²) | q''_ONB,exp (W/m²) | linear | 1 | ★★★ |
| Fig. 12 | 접촉각 θ에 따른 inception superheat 변화 | θ/π (무차원) | ΔT_ONB (정규화) | linear | 1 | ★★ |

**접촉각 θ 처리 방법**: Fig.9의 각 시리즈별 범례에서 θ값을 읽어 `theta_deg` 열에 기입. θ별로 별도 CSV 파일 또는 동일 CSV에 시리즈 구분 열 추가.

**단위 확인 완료 (2026-05-27)**:
- **Fig.9**: ONB locus — 원문 축 단위 확인 후 기입
- **Fig.10 (parity ΔT_ONB)**: x, y 단위 = **°C** (예측 vs 실험 ΔT_ONB)
- **Fig.11 (parity q''_ONB)**: x, y 단위 = **W/cm²** → 전처리 시 `q_onb_W_m2 = col × 10,000` 적용
- **Fig.12**: x축 = **θ/π** (무차원) → `theta_deg = x_raw × 180`; y축은 정규화 inception superheat

**추출 전략**: Fig.10/11의 parity plot에서 실험값(y축)을 추출하는 것이 가장 직접적. Fig.9에서 ONB locus 선 위의 포인트를 균등 간격으로 추출.

---

### P2 — Kandlikar (1991) [KANDLIKAR1991]
**DOI**: 10.1115/1.2910524 | **현재 확보**: 41 포인트 (fig5 완료)

> **⚠️ PDF 확인 결과 (2026-05-28) — 스캔 이미지 PDF, 텍스트 추출 불가. PNG 직접 확인.**

---

#### Fig.2 — 유동비등 레짐 맵 (상세 가이드)

**실제 내용**: *"Flow boiling map — h_TP/h_lo versus Quality x"*

| 축 | 변수 | 범위 | 스케일 |
|----|------|------|--------|
| x축 | 증기 건도 Quality, x | −0.4 ~ 0.8 | linear |
| y축 | 무차원 열전달계수 h_TP/h_lo | 1 ~ 20 | linear |

**그림에 표시된 경계선**:

| 레이블 | 의미 | ONB 관련도 |
|--------|------|-----------|
| **SPL** | Single Phase Liquid 영역 | ONB **이전** |
| **PB** | Partial Boiling 영역 | ONB **이후** ← SPL/PB 경계 = ONB locus |
| **FDB** | Fully Developed Boiling | ONB 이후 |
| **NVG,1 / NVG,2** | Net Vapor Generation (= OSV) 경계 | |
| **x_ONB1, x_ONB2** | x축 위의 ONB 발생 위치 마커 | |

**ONB 경계 위치**: 서브쿨 영역(x < 0)에서 h_TP/h_lo = 1 선 근처에서 PB 영역으로 분기하는 곡선.

**⚠️ 디지타이즈 제약 — 왜 어려운가**:

```
이 그림은 이론적 레짐 맵 (실험 데이터 산점이 아님).
좌표계: (x_quality, h_TP/h_lo) — 모두 무차원.

물리량(q''_ONB, ΔT_ONB) 역산에 필요한 정보:
  - G (질량유속) → 그림에 없음
  - h_lo (단상 액체 열전달계수) → 계산 필요
  - 유체 물성치 (ρ, μ, k, cp) → 별도 지정
  → 역산 불가 (그림 단독으로)
```

**결론: Fig.2 디지타이즈 생략**. 레짐 경계 이해·논문 기술 참고용으로만 사용.

---

#### Fig.5 — 비등 곡선 (상세 가이드)

**실제 내용**: *"Experimental results of Bergles & Rohsenow (1964), reproduced from Collier (1981)"*

> **⚠️ 데이터 출처 주의**: Fig.5는 Kandlikar 고유 데이터가 아닌 **Bergles & Rohsenow (1964) 원본 데이터** 재수록.
> → **P3 (bergles1964)와 동일 실험 데이터**. 처리 시 중복 계산 방지.

| 축 | 변수 | 단위 | 스케일 |
|----|------|------|--------|
| x축 | T_w − T_SAT = ΔT_wall | **°C** (상단에 °F 병기) | log |
| y축 | Surface heat flux q'' | **MW/m²** ✅ 확인 완료 | log |

**실험 조건** (전 시리즈 공통):
- 시험부: Stainless steel rod in Pyrex tube
- 압력: **p = 2.2 bar (32 psia)**
- 위치: z/D_e = 48

**시리즈별 조건**:

| 파일명 | 유속 | ΔT_sub 범위 | G 추정 (kg/m²s) |
|--------|------|-----------|----------------|
| `pbSS_Tsub2p2` | Pool boiling (u=0) | 2.2°C | 0 (참조용) |
| `u1p37_Tsub103-40` | **u = 1.37 m/s** | 103→40°C (축방향 변화) | 계산 필요 |
| `u2p65_Tsub101-68` | **u = 2.65 m/s** | 101→68°C | 계산 필요 |
| `u4p60_Tsub109-72` | **u = 4.60 m/s** | 109→72°C | 계산 필요 |

> ΔT_sub 범위 해석: z/D_e=20 기준 위치에서 z/D_e=48까지 이동하며 변하는 과냉도 폭. 단일 운전 조건에서 위치에 따라 다름.

**ONB 포인트 식별 — 단계별 방법**:

비등 곡선에서 ONB는 단상 대류선(점선)과 비등 곡선이 분리되는 지점입니다.

```
Step 1. WebPlotDigitizer에서 해당 시리즈 PNG 로드.
Step 2. 점선(dashed line, = 단상 강제대류 Dittus-Boelter 선) 위의
        두 점을 클릭 → 점선의 기울기/위치를 파악.
Step 3. 각 시리즈 데이터 포인트 중 점선보다 위쪽(q'' 초과)으로
        처음 벗어나는 포인트 = ONB 포인트.
Step 4. 해당 포인트의 (ΔT_wall [°C], q'' [MW/m²]) 좌표 추출.
        → delta_T_onb_K = x값, q_onb_W_m2 = y값 × 1,000,000
Step 5. 굴곡이 불명확하면: 점선과의 q'' 차이가 처음으로
        +10% 초과하는 포인트 선택. notes에 "ONB by 10% deviation" 기재.
```

**시리즈별 ONB 예상 위치** (그림 시각적 확인 기준):

| 시리즈 | 예상 ΔT_ONB (°C) | 예상 q''_ONB (MW/m²) |
|--------|-----------------|---------------------|
| pbSS (pool) | ~10~12 | ~0.15~0.3 |
| u=1.37 m/s | ~10~13 | ~1~2 |
| u=2.65 m/s | ~8~11 | ~2~3 |
| u=4.60 m/s | ~8~10 | ~3~5 |

**현재 상태**: ✅ 전체 비등 곡선 디지타이즈 완료 (41 포인트).
**다음 작업**: 각 시리즈에서 ONB 굴곡점 1개씩 식별 → 별도 `kandlikar1991_fig5_ONB.csv` 작성.

**단위 변환 (전처리 시 적용)**:
- `q_onb_W_m2 = y_raw × 1,000,000` (MW/m² → W/m²)
- `delta_T_onb_K = x_raw` (이미 °C = K 차이값)

**CSV 메타데이터**:
- `fluid`: `water`
- `channel_type`: `tube_circular`
- `P_kPa`: `220.0` (2.2 bar)
- `surface_cat`: `ss_rod` (stainless steel rod)
- `Ra_um`: `-1` (미기재)
- `theta_deg`: `-1` (미기재)

---

### P3 — Bergles & Rohsenow (1964) [BERGLES1964]
**DOI**: 10.1115/1.3688697 | **예상 ONB 포인트**: ~25개

> **⚠️ PDF 직접 확인 결과 (2026-05-28)**:
> - Fig.3 = 시험부 단면도 (schematic) — ONB 데이터 없음
> - Fig.4 = 단상 강제대류 상관식 — ONB 데이터 없음
> - **Fig.5** = 비등 곡선 (ONB 이탈점 포함) ← **Kandlikar1991_fig5와 동일 데이터** (중복)
> - **Fig.6** = 이론 모델 버블 기하학 다이어그램 — ONB 실험 데이터 **없음** (사용자 확인)
> - **Fig.7** = 고압 조건 incipient boiling 실험 데이터 ✅
> - **Fig.9** = 종합 강제대류 비등 데이터셋 ✅ (추가 조건 다수)

| Figure | 설명 | x축 (단위) | y축 (단위) | 스케일 | 시리즈 수 | 우선도 |
|--------|------|-----------|-----------|--------|---------|--------|
| ~~Fig. 5~~ | ~~비등 곡선~~ | — | — | — | — | **생략** — Kandlikar1991_fig5와 동일 데이터 (S.S. rod, p=32 psia, u=1.37/2.65/4.60 m/s) |
| ~~Fig. 6~~ | ~~이론 모델 다이어그램~~ | — | — | — | — | **생략** — 버블 기하 스케치, 실험 데이터 없음 |
| Fig. 7 | 고압 조건 incipient boiling — 실험 데이터 | ΔT_wall (°F) | q'' (Btu/h·ft²) | log-log | 2-3 (압력별) | ★★★ |
| Fig. 9 | 종합 강제대류 비등 + 풀비등 데이터 (stainless steel tube) | ΔT_wall (°F) | q'' (Btu/h·ft²) | log-log | 4-6 (유속·과냉도 조합) | ★★★ |

**Fig.7 상세**:
- 고압 시스템의 incipient boiling (Hewitt & Hall-Taylor 등 데이터 포함)
- x축: T_w − T_sat (°F), y축: q'' (Btu/h·ft²), log-log
- 압력 조건이 Fig.5/9와 다름 → 압력 효과 포착에 필수

**Fig.9 상세**:
- 강제대류 비등 + 풀비등 데이터를 하나의 그래프에 통합
- 시리즈: 유속(U) × 과냉도(ΔT_sub) 조합 다수
- x축: T_w − T_sat (°F), y축: q'' (Btu/h·ft²), log-log
- ONB 포인트: 각 시리즈에서 단상 강제대류 선 이탈점 (Fig.5와 동일 방법)

**✅ 디지타이즈 완료 (2026-05-28)**:

| 파일 | 시리즈 | 행 수 | x 범위 (°F) | y 범위 (W/m²) |
|------|--------|------|------------|--------------|
| bergles1964_fig7_v10ftsec_wpd.csv | v=10 ft/s (3.05 m/s) | 5 | 4.67~7.76 | 1.08~1.82 MW/m² |
| bergles1964_fig7_v20ftsec_wpd.csv | v=20 ft/s (6.10 m/s) | 11 | 3.71~9.88 | 1.37~2.52 MW/m² |
| bergles1964_fig7_v30ftsec_wpd.csv | v=30 ft/s (9.14 m/s) | 10 | 4.18~9.74 | 1.85~2.98 MW/m² |
| bergles1964_fig9_v4p5ftsec_wpd.csv | v=4.5 ft/s (1.37 m/s) | 7 | 10.77~55.38 | 0.99~2.54 MW/m² |
| bergles1964_fig9_v8p7ftsec_wpd.csv | v=8.7 ft/s (2.65 m/s) | 15 | 11.31~70.63 | 1.52~3.93 MW/m² |
| bergles1964_fig9_v15p1ftsec_wpd.csv | v=15.1 ft/s (4.60 m/s) | 12 | 25.15~77.72 | 2.16~5.03 MW/m² |

**단위 확인 (2026-05-28, 사용자 직접 확인)**:
- **x축**: ΔT_wall = **°F** → `delta_T_onb_K = x_raw × 5/9`
  - (차이값 변환: 32 빼기 없이 × 5/9만 적용)
- **y축**: **Btu/h·ft²** → `q_onb_W_m2 = y_raw × 3.15459`

변환 후 범위 확인:
| 시리즈 | ΔT_wall (°C) | q'' (MW/m²) |
|--------|-------------|------------|
| fig7 v=10 ft/s | 2.6~4.3 | 3.4~5.7 |
| fig7 v=20 ft/s | 2.1~5.5 | 4.3~8.0 |
| fig7 v=30 ft/s | 2.3~5.4 | 5.8~9.4 |
| fig9 v=4.5 ft/s | 6.0~30.8 | 3.1~8.0 |
| fig9 v=8.7 ft/s | 6.3~39.2 | 4.8~12.4 |
| fig9 v=15.1 ft/s | 14.0~43.2 | 6.8~15.9 |

**제외 확정**:
- **Fig.5**: Kandlikar1991_fig5와 동일 데이터 (중복)
- **Fig.6**: 이론 버블 기하 다이어그램 (실험 데이터 없음, 사용자 확인)
- **Fig.8**: "Tripping of flow by surface boiling" — 유동 전이 현상, ONB 열유속 데이터 없음
- **Fig.10**: "Influence of subcooling on pool boiling" — 풀비등 과냉도 효과, 유동비등 ONB 아님

**ONB 굴곡점 식별** (fig9 시리즈 — 비등 곡선 전체 추출됨):
```
전처리 시 각 시리즈에서 단상 강제대류 선 이탈점 1개 식별:
  x_min (ΔT_wall 최솟값) 근처 포인트 = ONB 후보
  또는 log-log 직선 기울기 변화점 (3.2절 방법 적용)
```

**CSV 메타데이터**:
- `fluid`: `water`
- `channel_type`: `tube_circular`
- `P_kPa`: fig7=고압(원문 확인 필요), fig9=`220.0` (2.2 bar=32 psia)
- `surface_cat`: `ss_tube`
- `Ra_um`: `-1`, `theta_deg`: `-1`

---

### P4 — Forrest et al. (2016) [FORREST2016]
**DOI**: 10.1115/1.4031503 | **예상 ONB 포인트**: ~40개

> **⚠️ PDF 확인 결과 (2026-05-21)**: 이전 가이드의 Fig.5/6은 ONB 데이터 아님.
> - Fig.5 = 단일 G=3000 조건의 부분 비등 곡선 (partial forced convection boiling curve, 단일 조건)
> - Fig.6 = TC13 열전대 단독 분할 열유속 그래프 (partitioned boiling heat flux for TC13)
> 실제 ONB 측정 데이터는 아래 Fig.7/8/10/17/18/19에 있음.

| Figure | 설명 | x축 (단위) | y축 (단위) | 스케일 | 시리즈 수 | 우선도 |
|--------|------|-----------|-----------|--------|---------|--------|
| Fig. 7 | ONB에서 측정된 열유속 (온도 기반 판별) | G (kg/m²s) 또는 ΔT_sub | q''_ONB (MW/m² 또는 W/m²) | linear | 2 (clean / oxidized) | ★★★ |
| Fig. 8 | clean vs 산화 표면 측정 ONB 열유속 비교 | G (kg/m²s) | q''_ONB (W/m²) | linear | 2 (clean / oxidized) | ★★★ |
| Fig. 10 | 채널 출구에서의 ONB 열유속 (전체 조건 요약) | G (kg/m²s) 또는 ΔT_sub | q''_ONB (W/m²) | linear | 다중 조건 | ★★★ |
| Fig. 17 | ONB 열유속 vs 벽면 포화 과열도 (모델 비교 포함) | ΔT_ONB (°C) | q''_ONB (W/m²) | linear/log | 2+ | ★★ |
| Fig. 18 | 측정 vs 예측 ONB 열유속 parity plot | q''_ONB,pred | q''_ONB,exp | linear | 1 | ★★ |
| Fig. 19 | 압력 측정 기반 ONB 열유속 parity plot (독립 검증) | q''_ONB,pred (kW/m²) | q''_ONB,exp (**kW/m²** ✅) | linear | 1 | ★ (참고용) |
| Fig. 4 | 비등 곡선 판별 비교 (참고용) | q'' (W/m²) | 지역 온도 | linear | 다중 TC | ★ (참고용) |

**표면 상태 처리**: `surface_cat` 열에 `ss_clean` / `ss_oxidized` 구분 기입. θ와 Ra는 Fig.13~16 (접촉각 사진)에서 수치 확인 필요.

**단위 주의**: q''가 MW/m²로 표기되면 × 1,000,000하여 W/m² 변환.

**단위 확인 완료 (2026-05-28)**:
- **Fig.19 y축**: **kW/m²** → 전처리 시 `q_onb_W_m2 = y_raw × 1,000` 적용 (x축 동일)
- Fig.19 값 범위: 110~845 kW/m² — MTR 조건에서 물리적으로 타당

**추출 전략**: Fig.7 또는 Fig.8에서 clean/oxidized 시리즈별 q''_ONB vs G 데이터 추출이 핵심. Fig.10으로 전체 조건 보완.

---

### P5 — Basu, Warrier, Dhir (2005a/b) [BASU2005a/b]
**Part I DOI**: 10.1115/1.1842784 | **Part II DOI**: 10.1115/1.1842785

> **⚠️ PDF 확인 결과 (2026-05-22) — 두 파일 모두 확인 완료**
> 
> | 파일 | 실제 내용 | ONB 데이터 여부 |
> |------|---------|--------------|
> | `basu2005part1.pdf` | "Wall Heat Flux Partitioning — **Part I: Model Development**" | ❌ 없음 — 열유속 분배 모델 개발 |
> | `basu2005part2.pdf` | "Wall Heat Flux Partitioning — **Part II: Model Validation**" | ❌ 없음 — 열유속 분배 모델 검증 |
> 
> **결론**: 두 논문 모두 **ONB 발생 조건 실험 데이터를 직접 제공하지 않음**.
> 내용: 버블 슬라이딩, 버블 이탈 직경, 대기 시간, 열유속 분배 모델 — ONB incipience 상관식 아님.
> 
> **Basu 그룹의 ONB 실험 데이터 원본**: → **P1 (BASU2002, fig9/10/11/12)** 에서 추출.
> 2005 논문들은 ONB 이후 핵비등 열전달 메커니즘에 관한 후속 연구임.

**디지타이즈 대상 아님** — P5 우선순위 제외. 아래 활용 용도로만 보관:
- Part I: 열유속 분배 출발점이 ONB임을 서술 → PINN 모델 물리 기반 참고
- Part II: 다양한 조건의 비등 곡선 (Fig.9~12) → 모델 검증 참고 (데이터 포인트 추출 불필요)

**디지타이즈 예상 포인트**: 0 (제외)

---

### P6 — Liu, Lee, Garimella (2005) [LIU2005]
**DOI**: 10.1016/j.ijheatmasstransfer.2005.07.021 | **예상 ONB 포인트**: ~20개

> **⚠️ PDF 확인 결과 (2026-05-21)**: 이전 가이드의 Fig.6/7/8은 모두 ONB 데이터 아님.
> - Fig.6 = 핵생성 공동 크기 분포 (nucleation cavity size for Case 4 + incipient bubble geometry)
> - Fig.7 = 마이크로채널 핵비등 과정 버블 시각화 사진 (visualization of nucleate boiling)
> - Fig.8 = 버블 반경 성장 및 접촉각 계산 (bubble radius evolution)
> 실제 ONB 데이터는 아래 Fig.4/5/9에 있음.

| Figure | 설명 | x축 (단위) | y축 (단위) | 스케일 | 시리즈 수 | 우선도 |
|--------|------|-----------|-----------|--------|---------|--------|
| Fig. 4 | 모델 예측 vs 측정 incipient heat flux 비교 | q''_ONB,pred (W/cm²) | q''_ONB,exp (W/cm²) | linear | 1~2 (채널 조건별) | ★★★ |
| Fig. 5 | 벽면 과열도 vs incipient heat flux — **5개 모델 곡선 + 실험 산점** | q''_inc (W/cm²) | ΔT_w (°C) | linear | 모델 5개(곡선) + 실험점(산점) | ★★ |
| Fig. 9 | 매개변수 효과 — (a)유량, (b)입구온도, (c)출구압력, (d)채널폭 | 조건별 변수 | q''_ONB (W/m²) | linear | 각 subplot당 1~2 | ★★ |

**마이크로채널 특이사항**: D_h < 1 mm 영역. `channel_type` 열에 `microchannel` 기입. 유체는 탈이온수(DIW) — `fluid` 열에 `water_DIW` 기입.

---

#### Fig.5 — 상세 가이드 (PDF 직접 확인 2026-05-28)

**실제 내용**: *"Comparison of predictions of wall superheat as a function of incipient heat flux from the present model as well as those from [4 other models]"*

> ⚠️ **디지타이즈 주의**: Fig.5는 **모델 검증 비교 도식** — 5개 이론 곡선(선)과 실험 데이터(산점)가 함께 표시됨.
> - **모델 곡선**: Present model, Hsu & Graham [7], Bergles & Rohsenow [2], Kandlikar et al. [25], Celata et al. [26]
> - **실험 산점**: 범례에 별도 항목 없이 그래프 내 scatter 심볼로만 표시

| 축 | 변수 | 단위 | 스케일 |
|----|------|------|--------|
| x축 | Incipient heat flux q''_inc | **W/cm²** | linear |
| y축 | Wall superheat at incipience ΔT_w | **°C** | linear |

**디지타이즈 방침**:

```
추출 대상: 실험 데이터 산점(scatter symbol)만
추출 금지: 5개 모델 예측 곡선 (이론 산출값, 측정값 아님)

실험점 식별 방법:
  1. 모든 곡선(선)은 제외 → 선이 아닌 독립 점(도형 심볼)만 클릭
  2. 범례에 없어도 scatter 심볼 = 실험 측정값
  3. 곡선 위에 놓인 점처럼 보이는 경우 → 곡선과 일치 여부 확인;
     곡선과 정확히 겹치면 모델 계산점일 수 있음 → notes에 "model or exp uncertain" 기재

주의: 5개 곡선이 촘촘히 겹쳐 있어 배경 산점 식별이 어려움.
      불확실한 점은 추출하지 말고 Fig.4 데이터로 대체.
```

**단위 변환 (전처리 시)**:
- `q_onb_W_m2 = x_raw × 10,000` (W/cm² → W/m²)
- `delta_T_onb_K = y_raw` (이미 °C = K 차이값)

**Fig.4와의 관계**: Fig.4("Comparison of incipient heat flux")가 동일 실험 데이터를 더 직접적으로 보여줌. Fig.4 완료 후 Fig.5의 산점을 대조 확인하는 방식 권장. Fig.4와 중복되는 포인트는 추출 불필요.

---

**추출 전략**: Fig.4의 데이터 포인트(실험값)를 추출하는 것이 최우선. Fig.5는 Fig.4 완료 후 보완 목적으로만 실험 산점 추출 (모델 곡선 추출 금지). Fig.9는 (a)~(d) subplot 4개 각각 별도 CSV 처리.

**Fig.9 subplot 파일 명명**: `liu2005_fig9a_flowrate.csv`, `liu2005_fig9b_inlet_temp.csv`, `liu2005_fig9c_pressure.csv`, `liu2005_fig9d_width.csv`

---

## 3. 디지타이즈 절차 (단계별)

### 3.1 축 보정 (Axis Calibration)

**목적**: 픽셀 좌표를 물리 단위로 변환하는 선형(또는 log) 매핑 수립.

**절차**:

1. WebPlotDigitizer에서 Figure 이미지 로드 후 "Calibration" 탭 선택.
2. **X축 보정**:
   - 그래프에서 x축 상의 두 점 (알려진 값) 클릭: 예) x=100, x=1000.
   - "X1", "X2" 입력창에 실제 값 입력.
   - log scale 여부: log인 경우 "Log Scale" 체크박스 활성화.
3. **Y축 보정**:
   - y축 상의 두 점 클릭: 예) y=1×10⁴, y=1×10⁶.
   - "Y1", "Y2" 입력창에 실제 값 입력.
4. "Complete!" 클릭.

**오차 최소화 팁**:
- 눈금선(grid line)이 있는 점을 보정 기준점으로 사용 (격자 교차점이 가장 정밀).
- 보정 범위를 가능한 넓게 설정 (양 끝 눈금 사용 권장).
- 동일 점을 400% 확대(브라우저 zoom) 후 클릭하면 픽셀 정밀도 향상.
- log scale에서 10의 거듭제곱 눈금(10¹, 10², 10³)을 보정점으로 사용.

### 3.2 데이터 포인트 추출

**수동 추출 (Manual mode, 권장)**:

1. "Add Dataset" 클릭 → 시리즈 이름 입력 (예: "theta30", "G=500_clean").
2. 마우스로 그래프 위 데이터 포인트 클릭. 포인트는 빨간 점으로 표시됨.
3. 클릭 실수 시: Ctrl+Z (Undo).
4. 다음 시리즈: "Add Dataset" 재클릭 후 새 이름 입력, 다른 색상으로 표시됨.

**자동 추출 (Auto mode)**:
- 배경색과 데이터 색상 대비가 뚜렷한 경우에만 사용.
- "Auto Extraction" 탭 → 색상 마스킹 → "Run Extraction".
- 자동 추출 후 반드시 수동 검토: 오인식 포인트 삭제, 누락 포인트 수동 추가.

**다중 시리즈 처리**:
- 범례(legend)의 시리즈별 색상을 기록해 두고 추출 순서와 매칭.
- 시리즈별로 별도 Dataset 생성 → CSV 내보내기 시 Dataset별로 분리 가능.
- 예: Basu(2002) Fig. 9에서 θ=30°/50°/80°의 세 곡선을 각각 별도 Dataset으로 추출.

### 3.3 ONB 포인트 식별

ONB(Onset of Nucleate Boiling) 포인트는 그래프 유형에 따라 다르게 식별:

**유형 A — 비등 곡선 (q'' vs ΔT_wall)**:
- 단상 대류 영역(직선)에서 핵비등 영역(급격한 기울기 변화)으로 전환되는 굴곡점.
- 해당 굴곡점 1개만 추출. 전체 비등 곡선이 아닌 ONB 포인트만 기입.

**유형 B — ONB locus 선**:
- 논문에서 "ONB line" 또는 "incipient boiling line"으로 명시된 선.
- 선 위의 포인트를 균등 간격으로 10~20개 추출.

**유형 C — 실험 데이터 포인트 (scatter plot)**:
- 각 포인트가 하나의 실험 조건에서 측정된 ONB 값.
- 모든 포인트 추출.

**유형 D — Parity plot (예측 vs 실험)**:
- x축 또는 y축이 ONB 실험값인 경우, y축 값만 추출하여 `delta_T_onb_K` 또는 `q_onb_W_m2`에 기입.

**ONB 식별이 불명확한 경우**:
- 원문 본문에서 ONB 판별 기준 설명 확인 (온도 급등, 압력강하 변화, 시각 관찰 등).
- 불명확 시 `notes` 열에 "ONB identification ambiguous — see paper §X.X" 기재.
- 굴곡점이 복수로 보이면 후보를 모두 추출하고 `notes`에 "ONB candidate — row X or Y" 표시.

### 3.4 CSV 내보내기

1. "View Data" 탭 클릭 → 추출된 포인트 확인.
2. "Download" → CSV 형식 선택.
3. 내려받은 CSV 파일: 열 구성은 `x, y` (또는 Dataset 이름이 앞에 추가됨).
4. 내보낸 CSV를 §4의 표준 스키마로 변환 (수동 또는 Python 스크립트 활용).

**세션 저장**: "Save" → `.tar` 파일 저장. 논문별로 `<paper_id>_fig<n>.tar` 저장 권장 (재현 가능성).

---

## 4. 데이터 저장 형식 (CSV 스키마)

### 4.1 표준 헤더

```
paper_id, fluid, channel_type, D_h_mm, G_kg_m2s, P_kPa, delta_T_sub_K, Ra_um, theta_deg, surface_cat, q_onb_W_m2, delta_T_onb_K, source_fig, digitize_date, notes
```

### 4.2 열 정의 및 허용값

| 열 이름 | 타입 | 단위 | 설명 | 허용값 / 예시 |
|---------|------|------|------|-------------|
| `paper_id` | str | — | 논문 DB 카드 ID | `basu2002`, `kandlikar1991`, `bergles1964`, `forrest2016`, `basu2005a`, `liu2005` |
| `fluid` | str | — | 작동 유체 | `water`, `water_DIW`, `R-12`, `R-22`, `R-113`, `R-114`, `R-134a`, `R-152a` |
| `channel_type` | str | — | 채널 형상 분류 | `tube_circular`, `rect_channel`, `narrow_channel`, `microchannel`, `annulus` |
| `D_h_mm` | float | mm | 수력직경. 미지/해당없음: -1 | 0.3, 1.96, 5.0 |
| `G_kg_m2s` | float | kg/m²s | 질량유속. 풀비등: 0 | 500, 1000, 3000 |
| `P_kPa` | float | kPa | 절대압력. 대기압: 101.325 | 101.325, 200, 500 |
| `delta_T_sub_K` | float | K | 과냉도 (T_sat - T_bulk). 포화: 0 | 5.0, 20.0, 45.0 |
| `Ra_um` | float | μm | 표면 거칠기 (산술 평균). 미지: -1 | 0.5, 1.2, -1 |
| `theta_deg` | float | degree | 정적 접촉각. 미지: -1 | 30, 50, 80, -1 |
| `surface_cat` | str | — | 표면 카테고리 | `stainless_clean`, `ss_oxidized`, `silicon_DIW`, `copper_polished`, `unknown` |
| `q_onb_W_m2` | float | W/m² | ONB 열유속 | 12000, 150000 |
| `delta_T_onb_K` | float | K | ONB 벽면 과열도. 미지: -1 | 3.5, 8.2, -1 |
| `source_fig` | str | — | 원 논문 Figure 번호 | `fig3`, `fig9`, `fig4_series2` |
| `digitize_date` | str | — | 추출일 (YYYY-MM-DD) | `2026-05-21` |
| `notes` | str | — | 특이사항 | 단위 변환, 시리즈 구분, ONB 식별 방법 등 |

**결측값 처리**:
- 숫자형: `-1` (센서 미측정, 논문에 미기재)
- 문자형: `unknown`

### 4.3 예시 행

```csv
paper_id, fluid, channel_type, D_h_mm, G_kg_m2s, P_kPa, delta_T_sub_K, Ra_um, theta_deg, surface_cat, q_onb_W_m2, delta_T_onb_K, source_fig, digitize_date, notes
basu2002, water, tube_circular, 9.5, 450, 101.325, 10.0, -1, 30.0, copper_polished, 85000, 4.2, fig9, 2026-05-21, theta=30deg series; q_onb unit originally W/cm2 converted x10000
basu2002, water, tube_circular, 9.5, 450, 101.325, 10.0, -1, 80.0, copper_polished, 42000, 7.8, fig9, 2026-05-21, theta=80deg series; higher contact angle lower ONB flux
forrest2016, water, narrow_channel, 3.92, 1500, 200.0, 25.0, -1, -1, ss_oxidized, 1800000, 12.5, fig7, 2026-05-21, oxidized surface; D_h=2*gap=3.92mm; P from MTR conditions; fig7=measured ONB heat flux
liu2005, water_DIW, microchannel, 0.318, 341, 113.0, 3.0, -1, -1, silicon_DIW, 450000, 2.8, fig4, 2026-05-21, Case10; D_h=318um; data point from incipient heat flux comparison plot
```

### 4.4 Sidecar YAML 형식

각 CSV와 동일 폴더에 `<paper_id>_fig<n>.meta.yaml` 저장:

```yaml
paper_id: basu2002
doi: 10.1115/1.1471522
figure: 9
curve_label: "theta=30deg, G=450 kg/m2s"
fluid: water
pressure_kPa: 101.325
subcooling_K: 10.0
channel_type: tube_circular
D_h_mm: 9.5
original_units:
  q_flux: "W/cm2"
  temperature: "degC"
onb_identification: "incipient point on boiling curve — inflection from single-phase"
digitizer_user: leejs92
digitized_date: "2026-05-21"
wpd_session_file: "basu2002_fig9.tar"
notes: ""
```

---

## 5. 물리적 타당성 검증 체크리스트

추출 완료 후 아래 항목을 순서대로 점검. 이상값은 삭제하지 말고 `notes`에 플래그.

### 5.1 ΔT_ONB 허용 범위

| 유체 | ΔT_ONB 물리적 범위 | 이상값 기준 |
|------|-----------------|-----------|
| 물 (대기압) | 2 ~ 30 °C | < 1 °C 또는 > 40 °C |
| 물 (가압, P > 500 kPa) | 1 ~ 15 °C | < 0.5 °C 또는 > 20 °C |
| R-12, R-22, R-113 | 0.5 ~ 10 °C | < 0.3 °C 또는 > 15 °C |
| R-134a | 0.5 ~ 8 °C | < 0.3 °C 또는 > 12 °C |

이 범위를 벗어나는 행: `notes`에 `[FLAG: delta_T_onb out of physical range]` 추가.

### 5.2 q''_ONB 허용 범위

| 유체 / 채널 유형 | q''_ONB 전형적 범위 | 이상값 기준 |
|---------------|----------------|-----------|
| 물, 일반관 (D_h > 1 mm) | 10 kW/m² ~ 3 MW/m² | < 1 kW/m² 또는 > 10 MW/m² |
| 물, 마이크로채널 (D_h < 1 mm) | 100 kW/m² ~ 5 MW/m² | < 10 kW/m² 또는 > 20 MW/m² |
| 냉매류 (R-12, R-113 등) | 5 kW/m² ~ 1 MW/m² | < 1 kW/m² 또는 > 5 MW/m² |

이 범위를 벗어나는 행: `notes`에 `[FLAG: q_onb out of physical range — check unit conversion]` 추가.

### 5.3 단조성 체크

**동일 표면, 동일 G, 동일 P 조건에서**:
- q''_ONB 증가 시 ΔT_ONB도 증가해야 함 (Hsu/Sato-Matsumura: ΔT_ONB ∝ √q'').
- 위반 행: `notes`에 `[FLAG: non-monotonic — check digitize order]` 추가.

**G 증가 시** (동일 표면, 동일 P, 동일 ΔT_sub):
- q''_ONB 증가 (강한 대류 → 더 높은 열유속에서 비등 시작).
- 이 경향 위반: `notes`에 `[FLAG: G trend violation]`.

**θ 증가 시** (소수성화, 동일 조건):
- ΔT_ONB 감소 경향 (Basu et al. 상관식).
- 이 경향 위반: `notes`에 `[FLAG: theta trend check needed]`.

### 5.4 Bergles-Rohsenow 상관식 비교

**목적**: 디지타이즈된 q''_ONB 포인트가 고전 상관식과 ±50% 이내인지 확인.

**Bergles-Rohsenow (1964) 상관식** (물, SI 단위 변환 버전):

```
q''_ONB [W/m²] = 1,082 × P^1.156 × (ΔT_ONB / (0.556 × (P/6.895)^0.0234 × 1.8))^(2.16 / (P/6.895)^0.0234)
```

여기서 P는 kPa. 또는 더 간단한 형태:

```
ΔT_ONB [°C] = 0.556 × (q'' / (1082 × P^1.156))^(1 / (2.16/(P/6.895)^0.0234))
```

**실용적 점검 방법** (Python 코드 스니펫):
```python
# Bergles & Rohsenow (1964) — water, approximate SI form
# P in kPa, q in W/m2, dT in degC
def dT_onb_bergles(q_flux_W_m2, P_kPa):
    P_psia = P_kPa / 6.8948
    exponent = 2.16 / (P_psia ** 0.0234)
    dT = 0.556 * (q_flux_W_m2 / (1082.0 * P_kPa**1.156)) ** (1.0 / exponent)
    return dT  # degC
```

**비교 기준**:
- 추출값이 B-R 예측의 0.5배~2배 이내: 정상.
- 0.5배 미만 또는 2배 초과: `notes`에 `[FLAG: BR ratio = X.X — verify]`.

### 5.5 교차 확인

- 동일 논문의 다른 Figure에서 중복으로 나타나는 포인트는 일치 여부 확인.
- Parity plot (예측 vs 실험) 에서 추출한 값은 실험값 기준 ±5% 이내 일치해야 함.

---

## 6. 파일 저장 위치 및 네이밍 규칙

### 6.1 디렉토리 구조

```
phase2_flow_boiling/data/raw/
├── literature/                          ← 논문별 원본 추출 파일
│   ├── basu2002_fig3.csv
│   ├── basu2002_fig3.meta.yaml
│   ├── basu2002_fig9.csv
│   ├── basu2002_fig9.meta.yaml
│   ├── basu2002_fig9.tar                ← WPD 세션 (optional, .gitignore 처리)
│   ├── kandlikar1991_fig4_water.csv
│   ├── kandlikar1991_fig4_water.meta.yaml
│   ├── kandlikar1991_fig4_r12.csv
│   ├── ...
│   └── _index.md                        ← 디지타이즈 진척 인덱스
├── onb_dataset_phase2.csv               ← 전체 통합 파일 (literature/ 병합 결과)
├── onb_dataset_phase2_template.csv      ← 빈 헤더 템플릿
├── digitize_guide_phase2.md             ← 본 파일
└── paper_database_phase2.md
```

### 6.2 파일 네이밍 규칙

**CSV 파일**: `<paper_id>_fig<n>[_<series>].csv`
- `paper_id`: 소문자, 저자+연도 (예: `basu2002`, `bergles1964`, `forrest2016`)
- `fig<n>`: Figure 번호 (예: `fig3`, `fig9`, `fig4b`)
- `_<series>`: 같은 Figure 내 시리즈 구분 (예: `_water`, `_r12`, `_theta30`, `_clean`)
- 예: `basu2002_fig9_theta30.csv`, `kandlikar1991_fig4_r113.csv`

**Sidecar YAML**: CSV와 동일 이름, 확장자만 `.meta.yaml`
- 예: `basu2002_fig9_theta30.meta.yaml`

**WPD 세션**: CSV와 동일 이름, 확장자 `.tar`
- `.gitignore`에 `*.tar` 추가 권장 (용량 과다 방지). OneDrive에만 보관.

**통합 파일**: `onb_dataset_phase2.csv` (자동 병합 스크립트 사용 권장)

### 6.3 `_index.md` 인덱스 형식

`literature/_index.md`에 한 줄씩 추가:

```markdown
| paper_id_fig | 논문 | 표면/조건 | 유체 | G [kg/m²s] | ONB 대표값 | 포인트 수 |
|---|---|---|---|---|---|---|
| basu2002_fig9 | Basu et al. 2002 | Cu polished, θ=30° | water | 450 | q''=85 kW/m², ΔT=4.2°C | 15 |
| bergles1964_fig3 | Bergles & Rohsenow 1964 | steel tube | water | 500 | q''=200 kW/m², ΔT=6.1°C | 8 |
```

---

## 7. 단계별 진척 추적

### 7.1 논문별 진척 추적 템플릿

`literature/_index.md` 상단에 아래 테이블을 유지:

```markdown
## 디지타이즈 진척 현황

최종 갱신: YYYY-MM-DD
전체 목표: 300+ ONB 포인트
현재 확보: N 포인트

| 우선순위 | paper_id | 논문 | 상태 | Figure | 추출 포인트 | 완료일 | 비고 |
|---------|---------|------|------|--------|-----------|-------|------|
| P1 ⭐⭐⭐ | basu2002 | Basu et al. 2002 | 미시작 | fig9, fig10, fig11, fig12 | 0/50 | — | θ별 시리즈 구분; fig10/11 parity 우선 |
| P2 ⭐⭐⭐ | kandlikar1991 | Kandlikar 1991 | 미시작 | fig4, fig2 | 0/100 | — | 유체별 파일 분리 |
| P3 ⭐⭐⭐ | bergles1964 | Bergles & Rohsenow 1964 | 미시작 | **fig7, fig9** | 0/25 | — | 영국 단위 변환 필수; fig5=Kandlikar중복, fig6=이론다이어그램(생략) |
| P4 ⭐⭐⭐ | forrest2016 | Forrest et al. 2016 | 미시작 | fig7, fig8, fig10, fig17, fig18 | 0/40 | — | 산화/비산화 시리즈; fig7/8 우선 |
| ~~P5~~ | ~~basu2005a/b~~ | ~~Basu et al. 2005 Part I/II~~ | ✅ 제외 확정 | — | 0 | — | **ONB 데이터 없음** — 열유속 분배 모델 논문. ONB 데이터는 BASU2002에서 추출 |
| P6 ⭐⭐ | liu2005 | Liu et al. 2005 | 미시작 | fig4, fig5, fig9(a-d) | 0/20 | — | 마이크로채널, DIW; fig4/5 우선 |
| — | kandlikar1991 (냉매) | Kandlikar 1991 추가 | 미시작 | fig4 (R-12 등) | 0/50 | — | P2 이후 단계 |
```

**상태 코드**: `미시작` / `진행중` / `검증중` / `완료`

### 7.2 Go/No-Go 점검 기준

| 마일스톤 | 기준 | 점검 방법 |
|---------|------|---------|
| M1 중간 점검 | P1+P2+P3 완료, 150+ 포인트 | `_index.md` 누적 포인트 합산 |
| M1 Go/No-Go | 300+ 포인트, 물리 검증 통과율 > 90% | §5 체크리스트 실행 |
| 품질 기준 | 단위 변환 오류 0, BR 비율 0.5~2배 이내 90% 이상 | CSV 자동 검증 스크립트 |

### 7.3 통합 병합 스크립트 (참고)

`literature/` 내 개별 CSV를 `onb_dataset_phase2.csv`로 병합하는 Python 원라이너:

```python
import glob, pandas as pd
files = glob.glob("phase2_flow_boiling/data/raw/literature/*.csv")
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
df.to_csv("phase2_flow_boiling/data/raw/onb_dataset_phase2.csv", index=False)
print(f"Total ONB points: {len(df)}")
```

실행 전 각 CSV의 헤더가 표준 스키마와 일치하는지 확인.

---

## 부록 A. 단위 변환 참조표

| 원 단위 | SI 단위 | 변환 계수 | 적용 논문 |
|--------|--------|---------|---------|
| W/cm² | W/m² | × 10,000 | Basu 2002, 일부 일본 논문 |
| kW/m² | W/m² | × 1,000 | 일반 |
| MW/m² | W/m² | × 1,000,000 | Forrest 2016, 원자로 조건 |
| Btu/h·ft² | W/m² | × 3.15459 | Bergles 1964 |
| °F | °C | (F-32)×5/9 | Bergles 1964 |
| psia | kPa | × 6.8948 | Bergles 1964, 미국 논문 |
| bar | kPa | × 100 | 유럽 논문 |
| atm | kPa | × 101.325 | 일반 |
| sites/cm² | sites/m² | × 10,000 | Basu N_s 데이터 (직접 변환, 단 CSV에는 cm² 단위 유지 후 notes에 기재) |

---

## 부록 B. WebPlotDigitizer 주요 단축키

| 동작 | 단축키 |
|------|--------|
| 포인트 추가 (Add mode) | 마우스 클릭 |
| 포인트 삭제 | Delete 키 (선택 후) |
| 실행 취소 | Ctrl+Z |
| 포인트 이동 | Alt + 드래그 |
| 이미지 줌인 | 마우스 휠 업 / 브라우저 Ctrl++ |
| 데이터 보기 | View Data 탭 |
| 세션 저장 | Save (상단 메뉴) |
| CSV 내보내기 | View Data → Download |

---

*본 가이드 버전: v1.6 (2026-05-28)*
*v1.1: P1/P4/P6 Figure 번호 수정*
*v1.2: P5 (Basu2005) 제외 확정*
*v1.3: P3 (Bergles1964) Figure 번호 수정 — fig5/6/7*
*v1.4: P2 (Kandlikar1991) 대폭 보강 — Fig.2 생략 근거 + Fig.5 ONB 굴곡점 식별 방법 + 데이터 출처(Bergles&Rohsenow) 명기*
*v1.5: P3 (Bergles1964) 재정리 — Fig.5(중복)/Fig.6(이론) 생략, Fig.7+Fig.9로 대상 확정 (PDF 직접 확인)*
*v1.6: P6 (Liu2005) Fig.5 상세 가이드 — 모델 비교 도식 경고, 실험 산점만 추출 지침, 단위(W/cm²) 명기, Fig.4 우선 전략 확정 (PDF 직접 확인)*
*다음 갱신 예정: Liu2005 디지타이즈 완료 후 (M1 Go/No-Go 전)*
