# Phase 1 Surface Card → Phase 2 재사용 매핑

**작성일**: 2026-05-21
**기준**: Phase 1 `02_data/surface_cards/_index.md` (49면, SFC-001~050, SFC-030 결번)
**목적**: Phase 2 강제대류 비등 ONB PINN에서 Phase 1 표면 카드를 어떻게 재활용할지 판단

---

## 재사용 등급 기준

| 등급 | 기준 |
|------|------|
| ⭐⭐⭐ **직접 재활용** | 유체·재질·실험 조건이 flow boiling에 그대로 적용 가능. Surface Encoder 초기화 + 데이터 병합 모두 허용 |
| ⭐⭐ **부분 재활용** | 표면 기하(Ra, θ) 정보는 유효하나 유체·가열 형상이 Pool boiling 전용. Surface Encoder 초기화에만 활용 |
| ⭐ **참조만** | 표면 처리가 Flow boiling 실험 조건과 거리가 멀거나 CoolProp 미지원 유체. Reference 목적으로만 유지 |

---

## 그룹별 재사용 판단

### 1. BETZ_2013 — Patterned wettability surfaces (Si wafer, water)

| ID | Label | Ra | θ | 재사용 등급 | 판단 근거 |
|----|-------|----|---|------------|----------|
| SFC-001 | BETZ_Hydrophilic | nano | ~20° | ⭐⭐ | θ 효과 학습에 유효. Si 기판은 flow channel 소재로 희소하나 wettability manifold 커버리지 기여 |
| SFC-002 | BETZ_Hydrophobic | nano | ~115° | ⭐⭐ | 동일 |
| SFC-003 | BETZ_SHPi | nano | ~0° | ⭐⭐ | 초친수 극단값 — Surface Encoder의 θ 범위 확보 |
| SFC-004 | BETZ_SHPo | nano | ~158° | ⭐⭐ | 초소수 극단값 — 동일 |
| SFC-005 | BETZ_Biphilic | nano | mixed | ⭐ | 이종혼합 패턴 → 단일 θ 로 인코딩 어려움. Phase 2 입력 변수 설계 단순화 단계에서는 참조만 |
| SFC-006 | BETZ_SBPi_circle | nano | mixed | ⭐ | 동일 |
| SFC-007 | BETZ_SBPi_hex | nano | mixed | ⭐ | 동일 |

**그룹 요약**: SFC-001~004 부분 재활용, SFC-005~007 참조만.

---

### 2. JO_2011 — SiO₂/Teflon dot patterns (Si wafer, water)

| ID | Label | Ra | θ | 재사용 등급 | 판단 근거 |
|----|-------|----|---|------------|----------|
| SFC-008 | JO_Hydrophilic | ~1.75 nm | 54° | ⭐⭐ | θ=54° 중간값 — Surface Encoder 보간 데이터로 유효 |
| SFC-009 | JO_Hydrophobic | ~1.75 nm | 123° | ⭐⭐ | 동일 |

**그룹 요약**: 2면 모두 부분 재활용.

---

### 3. PHAN_2009 — Nano-coated stainless ribbon, **subcooled boiling (ΔT_sub=15 K)**

| ID | Label | Ra | θ | 재사용 등급 | 판단 근거 |
|----|-------|----|---|------------|----------|
| SFC-010 | PHAN_SiOx | ~30 nm | 22° | ⭐⭐⭐ | **유일하게 subcooled 조건(ΔT_sub=15 K) 실험**. Stainless ribbon → flow channel 재질 직결. 코팅 효과(θ 제어) 정보 포함 |
| SFC-011 | PHAN_TiO2 | ~30 nm | 31° | ⭐⭐⭐ | 동일 |
| SFC-012 | PHAN_Pt | ~30 nm | 67° | ⭐⭐⭐ | 동일 |
| SFC-013 | PHAN_Fe2O3 | ~30 nm | 80° | ⭐⭐⭐ | 동일 |
| SFC-014 | PHAN_ref | ~30 nm | 85° | ⭐⭐⭐ | uncoated reference — baseline 역할 |

**그룹 요약**: 5면 전체 직접 재활용. Phase 2에서 subcooled 효과 학습의 핵심 anchor 데이터셋.
⚠️ 주의: PHAN은 flow가 아닌 natural convection + subcooled 조건이므로 유속(G, Re) 변수는 0으로 처리 또는 별도 stratification 필요.

---

### 4. JONES_2009 — EDM-roughened aluminum (water + FC-77)

| ID | Label | Ra | Fluid | 재사용 등급 | 판단 근거 |
|----|-------|----|-------|------------|----------|
| SFC-015 | JONES_Polished_w | 0.038 μm | water | ⭐⭐ | Ra 거칠기 ladder 데이터로 Surface Encoder 초기화 유효 |
| SFC-016 | JONES_Polished_F | 0.027 μm | FC-77 | ⭐ | FC-77 → CoolProp 미지원. 참조만 |
| SFC-017 | JONES_EDM1p08 | 1.08 μm | water+FC-77 | ⭐⭐ / ⭐ | water 데이터만 재활용, FC-77 제외 |
| SFC-018 | JONES_EDM2p22 | 2.22 μm | water+FC-77 | ⭐⭐ / ⭐ | 동일 |
| SFC-019 | JONES_EDM5p89 | 5.89 μm | water+FC-77 | ⭐⭐ / ⭐ | 동일 |
| SFC-020 | JONES_EDM10p0 | 10.0 μm | water+FC-77 | ⭐⭐ / ⭐ | 동일 |

**그룹 요약**: water 데이터(4면) 부분 재활용, FC-77 전용(SFC-016)은 참조만.

---

### 5. BOURDON_2012 — Bronze + Au + alkanethiol SAM (water)

| ID | Label | Ra | θ | 재사용 등급 | 판단 근거 |
|----|-------|----|---|------------|----------|
| SFC-021 | BOURDON12_S1 | ~9.7 nm | 0° | ⭐⭐ | θ≈0° 초친수 극단값, Bronze 소재는 flow channel 비표준이나 wettability 효과 학습에 기여 |
| SFC-022 | BOURDON12_S2 | ~8.6 nm | 0° | ⭐⭐ | 동일 |
| SFC-023 | BOURDON12_S3 | ~7.6 nm | 0° | ⭐⭐ | 동일 |
| SFC-024 | BOURDON12_S1_grafted | ~9.7 nm | 108° | ⭐⭐ | θ 변화 효과 (코팅 전후 쌍 구성) 학습에 유용 |
| SFC-025 | BOURDON12_S1_grafted_C | ~9.7 nm | 108° (center) | ⭐ | 부분 코팅 패턴 → 단일 θ 표현 어려움. 참조만 |

**그룹 요약**: SFC-021~024 부분 재활용, SFC-025 참조만.

---

### 6. BOURDON_2015 — Float glass + silane SAM (ultra-smooth, water)

| ID | Label | Sa | θ | 재사용 등급 | 판단 근거 |
|----|-------|----|---|------------|----------|
| SFC-026 | BOURDON15_NotGrafted | 0.43 nm | 11.1° | ⭐⭐ | Ultra-smooth 기준점 — Ra 하단 극단값 확보 |
| SFC-027 | BOURDON15_MPEGPTMS | 0.43 nm | 33.5° | ⭐⭐ | θ gradient 학습에 유효 |
| SFC-028 | BOURDON15_AcOUTES | 0.43 nm | 70.8° | ⭐⭐ | 동일 |
| SFC-029 | BOURDON15_OTS | 0.43 nm | 101.6° | ⭐⭐ | 동일 |

**그룹 요약**: 4면 전체 부분 재활용.

---

### 7. JABARDO_2009 — Roughness ladders on Cu/Brass/SS (R-123, R-134a)

> Phase 1 최대 데이터셋 (20면, 589 curve pts, 44 ONB labels).
> **R-134a는 flow boiling 에서 가장 많이 사용되는 냉매 중 하나** → 직접 재활용 가치 높음.
> R-123도 CoolProp 지원 → 재활용 가능.

#### 7.1 Copper substrate (SFC-031~038)

| ID | Label | Ra | Fluid | 재사용 등급 | 판단 근거 |
|----|-------|----|-------|------------|----------|
| SFC-031 | JABARDO_Cu_Ra0p07P | 0.07 μm | R-134a | ⭐⭐⭐ | Cu heat sink는 flow boiling 실험 표준 재질. R-134a 직접 적용 가능 |
| SFC-032 | JABARDO_Cu_Ra0p16SP | 0.16 μm | R-123 | ⭐⭐⭐ | 동일 (R-123 CoolProp 지원) |
| SFC-033 | JABARDO_Cu_Ra0p47SP | 0.47 μm | R-123 | ⭐⭐⭐ | 동일 |
| SFC-034 | JABARDO_Cu_Ra0p5SP | 0.5 μm | R-134a | ⭐⭐⭐ | 동일 |
| SFC-035 | JABARDO_Cu_Ra2p5SPI | 2.5 μm | R-134a | ⭐⭐⭐ | 동일 |
| SFC-036 | JABARDO_Cu_Ra3p3SPI | 3.3 μm | R-123 | ⭐⭐⭐ | 동일 |
| SFC-037 | JABARDO_Cu_Ra4p6SPI | 4.6 μm | R-123+R-134a | ⭐⭐⭐ | 동일 |
| SFC-038 | JABARDO_Cu_Ra10p5SPI | 10.5 μm | R-123+R-134a | ⭐⭐⭐ | 동일 |

#### 7.2 Brass substrate (SFC-039~043)

| ID | Label | Ra | Fluid | 재사용 등급 | 판단 근거 |
|----|-------|----|-------|------------|----------|
| SFC-039 | JABARDO_Br_Ra0p08P | 0.08 μm | R-134a | ⭐⭐ | Brass는 flow channel 비표준이나 R-134a 데이터로 Surface Encoder 초기화 기여 |
| SFC-040 | JABARDO_Br_Ra0p90SP | 0.9 μm | R-134a | ⭐⭐ | 동일 |
| SFC-041 | JABARDO_Br_Ra1p2SPI | 1.2 μm | R-134a | ⭐⭐ | 동일 |
| SFC-042 | JABARDO_Br_Ra1p8SPI | 1.8 μm | R-134a | ⭐⭐ | 동일 |
| SFC-043 | JABARDO_Br_Ra3p5SPI | 3.5 μm | R-134a | ⭐⭐ | 동일 |

#### 7.3 Stainless steel plate (SFC-044~050)

| ID | Label | Ra | Fluid | 재사용 등급 | 판단 근거 |
|----|-------|----|-------|------------|----------|
| SFC-044 | JABARDO_SS_Ra0p03P | 0.03 μm | R-134a | ⭐⭐⭐ | **SS는 flow channel 가장 일반적인 재질**. R-134a 직접 적용 |
| SFC-045 | JABARDO_SS_Ra0p07SP | 0.07 μm | R-134a | ⭐⭐⭐ | 동일 |
| SFC-046 | JABARDO_SS_Ra0p45SP | 0.45 μm | R-134a | ⭐⭐⭐ | 동일 |
| SFC-047 | JABARDO_SS_Ra0p90SPI | 0.9 μm | R-134a | ⭐⭐⭐ | 동일 |
| SFC-048 | JABARDO_SS_Ra1p45SPI | 1.45 μm | R-134a | ⭐⭐⭐ | 동일 |
| SFC-049 | JABARDO_SS_Ra2p50SPI | 2.5 μm | R-134a | ⭐⭐⭐ | 동일 |
| SFC-050 | JABARDO_SS_Ra3p20SPI | 3.2 μm | R-134a | ⭐⭐⭐ | 동일 |

**그룹 요약**: Cu(8면) + SS(7면) 직접 재활용, Brass(5면) 부분 재활용.

---

## 집계 요약

| 등급 | 면 수 | 카드 ID | 비고 |
|------|-------|---------|------|
| ⭐⭐⭐ 직접 재활용 | **20** | SFC-010~014 (PHAN), SFC-031~038 (JABARDO_Cu), SFC-044~050 (JABARDO_SS) | Surface Encoder 초기화 + Phase 2 데이터 병합 모두 허용 |
| ⭐⭐ 부분 재활용 | **22** | SFC-001~004, 008~009, 015/017~020(water), 021~024, 026~029, 039~043 | θ/Ra 정보는 유효 → Surface Encoder 초기화에 활용 |
| ⭐ 참조만 | **7** | SFC-005~007 (biphilic complex), SFC-016 (FC-77), SFC-025 (partial coating) | Pool boiling 전용 또는 CoolProp 미지원 유체 |
| 결번 | 1 | SFC-030 | — |
| **합계** | **49** | | |

---

## Phase 2 신규 추가 필요 표면 (목표)

Phase 1 재활용 20면으로 flow boiling 표면 특성은 어느 정도 커버되나,
다음 영역은 Phase 2 전용 신규 카드 필요:

| 우선순위 | 재질 / 조건 | 이유 |
|---------|-----------|------|
| 1순위 | **유로 채널 내벽 (microchannel, D_h < 1 mm)** | JABARDO/JONES는 평판 기반 — 채널 기하 정보 없음 |
| 2순위 | **수정/산화 SS (Forrest 2016 계열)** | 원자로 안전 응용 — 표면 산화 효과 |
| 3순위 | **Cu microchannel (Mudawar group)** | 전자냉각 응용의 핵심 소재 |
| 4순위 | **R-1234yf 대응 표면** | R-134a 대체 냉매 — 유사 소재에서 유체만 교체 |

---

## Phase 2 Surface Encoder 전이학습 전략

```
Phase 1 Surface Encoder (Ra, θ, r_c, N_s, category → z_s ∈ ℝ⁸)
  ↓ freeze 후 fine-tune
Phase 2 Surface Encoder (동일 입력 → z_s ∈ ℝ⁸)

재활용 우선순위:
  ① JABARDO_SS (7면, R-134a) — Phase 2 핵심 유체·재질 일치
  ② PHAN (5면, subcooled) — subcooled 효과 anchor
  ③ JABARDO_Cu (8면, R-123/R-134a) — Ra ladder 커버리지
```

---

## 파일 참조

- Phase 1 원본: `../../02_data/surface_cards/_index.md`
- Phase 1 처리 데이터: `../../02_data/processed/onb_dataset.csv`
- Phase 2 신규 카드 저장 위치: `phase2_flow_boiling/data/surface_cards/` (SFC-051+)
