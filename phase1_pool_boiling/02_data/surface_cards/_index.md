# Surface Cards Index

**작성일:** 2026-05-10
**최종 갱신:** 2026-05-18 (JABARDO 20면 추가 반영, FC-77 출처 정정)
**총 표면 수:** 49 (SFC-001 ~ SFC-029, SFC-031 ~ SFC-050)
**연관 데이터:** `02_data/processed/boiling_curves.csv` (1361 points), `onb_dataset.csv` (82 labels)

> **SFC-030 결번 안내.** SFC-030은 원래 BETZ Fig.7b의 외부 비교 데이터
> (Chen 2009, Jones 10μm/Polished, Li 2008)를 위해 예약된 ID이지만,
> 최종 학습 데이터셋에는 포함되지 않아 결번으로 유지한다.

---

## 표면 카드 정의

각 카드는 디지타이즈 데이터 기반 raw 표면 정보 + 표면 처리/코팅 메타데이터.
본 인덱스는 모든 49개 카드를 통합 관리한다.

### 1. BETZ_2013 — Patterned wettability surfaces (Si)

| ID | Label | Ra (nm/μm) | θ_static (°) | Treatment | 디지타이즈 시리즈 |
|----|-------|-----------|--------------|-----------|------------------|
| SFC-001 | BETZ_Hydrophilic | nano | ~20 (7-30) | Oxidized Si, plain | figure_4_Hydrophilic, figure_6b_hydrophilic |
| SFC-002 | BETZ_Hydrophobic | nano | ~115 (110-120) | Si + Teflon coating | figure_4_Hydrophobic |
| SFC-003 | BETZ_SHPi | nano | ~0 | Si + SiO₂ nanopillar + O₂ plasma | figure_4_SHPi, figure_6b_Superhydrophilic |
| SFC-004 | BETZ_SHPo | nano | ~158 (150-165) | Si + Teflon + nanostructure | figure_4_SHPo |
| SFC-005 | BETZ_Biphilic | nano | mixed | SHPi background + SHPo dots (50μm) | figure_6b_Biphilic, figure_7b_Biphilic |
| SFC-006 | BETZ_SBPi_circle | nano | mixed | Superbiphilic, circular pattern (50μm, d/p=0.5) | figure_6b_Superbiphiliccircle |
| SFC-007 | BETZ_SBPi_hex | nano | mixed | Superbiphilic, hexagonal pattern | figure_6b_Superbiphilichexagon |

### 2. JO_2011 — SiO₂/Teflon dot patterns

| ID | Label | Ra (μm) | θ_static (°) | Treatment | 디지타이즈 시리즈 |
|----|-------|---------|--------------|-----------|------------------|
| SFC-008 | JO_Hydrophilic | 0.00175 | 54  | SiO₂ pure   | figure_3_Hydrophilic |
| SFC-009 | JO_Hydrophobic | 0.00175 | 123 | Teflon pure | figure_3_Hydrophobic |

### 3. PHAN_2009 — Nano-coated stainless ribbon (subcooled, ΔT_sub = 15 K)

| ID | Label | Ra (nm) | θ_static (°) | Coating / Method | 디지타이즈 시리즈 |
|----|-------|---------|--------------|------------------|------------------|
| SFC-010 | PHAN_SiOx   | ~30 | 22 | SiOx, PECVD          | figure_12a_theta22 |
| SFC-011 | PHAN_TiO2   | ~30 | 31 | TiO₂, NNBD           | figure_12a_theta31 |
| SFC-012 | PHAN_Pt     | ~30 | 67 | Pt, MOCVD            | figure_12a_theta67 |
| SFC-013 | PHAN_Fe2O3  | ~30 | 80 | Fe₂O₃, MOCVD         | figure_12a_theta80 |
| SFC-014 | PHAN_ref    | ~30 | 85 | Stainless, no coating | figure_12a_theta85 |

### 4. JONES_2009 — EDM-roughened aluminum, water + FC-77

| ID | Label | Ra (μm) | θ_static (°) | Treatment | 디지타이즈 시리즈 | Fluid |
|----|-------|---------|--------------|-----------|------------------|-------|
| SFC-015 | JONES_Polished_w   | 0.038 | (water-specific)  | Polished Al | figure_3a_Polished (water) | water |
| SFC-016 | JONES_Polished_F   | 0.027 | (FC-77-specific)  | Polished Al | figure_4a_Polished (FC-77) | FC-77 |
| SFC-017 | JONES_EDM1p08      | 1.08  | (Al, no coating) | EDM         | figure_3a_EDM1p08, figure_4a_EDM1p08   | water + FC-77 |
| SFC-018 | JONES_EDM2p22      | 2.22  | (Al, no coating) | EDM         | figure_3a_EDM2p22, figure_4a_EDM2p22   | water + FC-77 |
| SFC-019 | JONES_EDM5p89      | 5.89  | (Al, no coating) | EDM         | figure_3a_EDM5p89, figure_4a_EDM5p89   | water + FC-77 |
| SFC-020 | JONES_EDM10p0      | 10.0  | (Al, no coating) | EDM         | figure_3a_EDM10p0, figure_4a_EDM10p0   | water + FC-77 |

> JONES_2009는 본 데이터셋에서 **FC-77 데이터의 유일한 출처**이다 (5 ONB 라벨).
> CoolProp이 FC-77의 검증된 EOS를 제공하지 않으므로 학습에서는 제외되지만,
> CSV에는 투명성 확보를 위해 유지된다.

### 5. BOURDON_2012 — Bronze plate + Au + alkanethiol grafting

| ID | Label | Sa (nm) | θ_advancing (°) | Treatment | 디지타이즈 시리즈 |
|----|-------|---------|------------------|-----------|------------------|
| SFC-021 | BOURDON12_S1               | ~9.7 | 0   | Bronze + 24.8nm Au, polished (rougher) | figure_4_S1, figure_6_ungrafted |
| SFC-022 | BOURDON12_S2               | ~8.6 | 0   | Bronze + Au, intermediate              | figure_4_S2 |
| SFC-023 | BOURDON12_S3               | ~7.6 | 0   | Bronze + Au, smoothest                 | figure_4_S3 |
| SFC-024 | BOURDON12_S1_grafted       | ~9.7 | 108 | S1 + alkanethiol SAM (whole plate)     | figure_6_grafted_whole |
| SFC-025 | BOURDON12_S1_grafted_C     | ~9.7 | 108 (center) | S1 + alkanethiol SAM (15mm center) | figure_6_grafted_center |

### 6. BOURDON_2015 — Float glass + silane SAM (ultra-smooth)

| ID | Label | Sa (nm) | θ_static (°) | Treatment | 디지타이즈 시리즈 |
|----|-------|---------|--------------|-----------|------------------|
| SFC-026 | BOURDON15_NotGrafted | 0.43 | 11.1  | Float glass, no grafting   | figure_3 (θ=11.1°), figure_7_NotGrafted |
| SFC-027 | BOURDON15_MPEGPTMS   | 0.43 | 33.5  | Silane SAM (MPEGPTMS)      | figure_3 (θ=33.5°), figure_7_MPEGPTMS   |
| SFC-028 | BOURDON15_AcOUTES    | 0.43 | 70.8  | Silane SAM (AcOUTES)       | figure_3 (θ=70.8°), figure_7_AcOUTES    |
| SFC-029 | BOURDON15_OTS        | 0.43 | 101.6 | Silane SAM (OTS)           | figure_3 (θ=101.6°), figure_7_OTS       |

### 7. _Reserved (외부 비교 데이터, 미사용)_

| ID | Label | 출처 | Notes |
|----|-------|------|-------|
| ~~SFC-030~~ | _EXT_REFs_Fig7b_ | Chen 2009, Jones 10μm/Polished, Li 2008 | BETZ Fig.7b 비교 인용 데이터 — 학습 데이터셋 미포함 |

### 8. JABARDO_2009 — Roughness ladders on Cu/Brass/Stainless (R-123, R-134a)

JABARDO et al. (Exp. Therm. Fluid Sci., 2009)은 세 종류 금속 기재(Cu, Brass, Stainless)
위에 polished(P) / semi-polished(SP) / coarsest(SPI) 의 거칠기 사다리를 만든 후
R-123 및 R-134a 비등 실험을 수행했다. 본 데이터셋에서 단일 출처 중 가장 큰 규모
(20 surface × 589 curve points × 44 ONB labels)를 차지한다.
JABARDO 표면 카드는 **접촉각(θ)을 보고하지 않으므로 `theta_deg`는 비어 있다**;
표면 인코더는 surface-card 기본값으로 imputation 한다.

#### 8.1 Copper substrate (8 surfaces, R-123 + R-134a)

| ID | Label | Ra (μm) | Finish | 디지타이즈 시리즈 (대표) | Fluid |
|----|-------|---------|--------|------------------------|-------|
| SFC-031 | JABARDO_Cu_Ra0p07P    | 0.07  | Polished      | figure_9_Cu_Ra0p07P    | R-134a |
| SFC-032 | JABARDO_Cu_Ra0p16SP   | 0.16  | Semi-Polished | figure_9_Cu_Ra0p16SP   | R-123  |
| SFC-033 | JABARDO_Cu_Ra0p47SP   | 0.47  | Semi-Polished | figure_9_Cu_Ra0p47SP   | R-123  |
| SFC-034 | JABARDO_Cu_Ra0p5SP    | 0.5   | Semi-Polished | figure_9_Cu_Ra0p5SP    | R-134a |
| SFC-035 | JABARDO_Cu_Ra2p5SPI   | 2.5   | Coarse        | figure_9_Cu_Ra2p5SPI   | R-134a |
| SFC-036 | JABARDO_Cu_Ra3p3SPI   | 3.3   | Coarse        | figure_9_Cu_Ra3p3SPI   | R-123  |
| SFC-037 | JABARDO_Cu_Ra4p6SPI   | 4.6   | Coarse        | figure_9_Cu_Ra4p6SPI   | R-123 + R-134a |
| SFC-038 | JABARDO_Cu_Ra10p5SPI  | 10.5  | Coarse        | figure_9_Cu_Ra10p5SPI  | R-123 + R-134a |

#### 8.2 Brass substrate (5 surfaces, R-134a)

| ID | Label | Ra (μm) | Finish | 디지타이즈 시리즈 (대표) |
|----|-------|---------|--------|------------------------|
| SFC-039 | JABARDO_Br_Ra0p08P    | 0.08 | Polished      | figure_10a_Br_Ra0p08P |
| SFC-040 | JABARDO_Br_Ra0p90SP   | 0.9  | Semi-Polished | figure_10a_Br_Ra0p90SP |
| SFC-041 | JABARDO_Br_Ra1p2SPI   | 1.2  | Coarse        | figure_10a_Br_Ra1p2SPI |
| SFC-042 | JABARDO_Br_Ra1p8SPI   | 1.8  | Coarse        | figure_10a_Br_Ra1p8SPI |
| SFC-043 | JABARDO_Br_Ra3p5SPI   | 3.5  | Coarse        | figure_10a_Br_Ra3p5SPI |

#### 8.3 Stainless steel substrate (7 surfaces, R-134a)

| ID | Label | Ra (μm) | Finish | 디지타이즈 시리즈 (대표) |
|----|-------|---------|--------|------------------------|
| SFC-044 | JABARDO_SS_Ra0p03P    | 0.03 | Polished      | figure_10b_SS_Ra0p03P |
| SFC-045 | JABARDO_SS_Ra0p07SP   | 0.07 | Semi-Polished | figure_10b_SS_Ra0p07SP |
| SFC-046 | JABARDO_SS_Ra0p45SP   | 0.45 | Semi-Polished | figure_10b_SS_Ra0p45SP |
| SFC-047 | JABARDO_SS_Ra0p90SPI  | 0.9  | Coarse        | figure_10b_SS_Ra0p90SPI |
| SFC-048 | JABARDO_SS_Ra1p45SPI  | 1.45 | Coarse        | figure_10b_SS_Ra1p45SPI |
| SFC-049 | JABARDO_SS_Ra2p50SPI  | 2.5  | Coarse        | figure_10b_SS_Ra2p50SPI |
| SFC-050 | JABARDO_SS_Ra3p20SPI  | 3.2  | Coarse        | figure_10b_SS_Ra3p20SPI |

> Finish 명명 규칙: `P` = polished, `SP` = semi-polished (sandblasted then polished),
> `SPI` = coarsest sandblasted finish. 정확한 표면 가공 절차는 JABARDO et al. (2009)
> §2 (Test surfaces) 참조.

---

## 출처별 통계 (재집계)

| Source | Surfaces | Curve pts | ONB labels | Fluids |
|--------|----------|-----------|------------|--------|
| BETZ_2013     |  7 | 168  | 10 | water |
| JO_2011       |  2 |  14  |  2 | water |
| PHAN_2009     |  5 |  51  |  5 | water |
| JONES_2009    |  6 | 320  | 10 | water + **FC-77** |
| BOURDON_2012  |  5 | 144  |  6 | water |
| BOURDON_2015  |  4 |  75  |  5 | water |
| JABARDO_2009  | 20 | 589  | 44 | R-123, R-134a |
| **Total**     | **49** | **1361** | **82** | 4 fluids |

> **정정 (2026-05-18):** 이전 버전에서 JABARDO_2009의 fluid에 FC-77이 포함되어
> 있었으나, 실제 CSV에서 JABARDO는 R-123/R-134a만이며 FC-77의 유일한 출처는
> JONES_2009 (5 라벨)이다. 본문 §3 tab:dataset 도 이에 맞춰 수정 필요.

---

## 표면 분포 통계 (49면 기준 재집계)

### 거칠기 별 (Ra 또는 Sa)

| 범주 | 개수 | 대표 카드 |
|----|----|---------|
| Sub-nm (Sa < 1 nm)         | 4 | SFC-026~029 (BOURDON15) |
| Nano (1-100 nm)            | 9 | BETZ 7면 + JO 2면 |
| ~30 nm (PHAN)              | 5 | SFC-010~014 |
| Polished (Ra < 0.1 μm)     | 7 | JONES Polished 2면 + JABARDO P 4면 + JABARDO_SS_Ra0p07SP |
| 0.1-1 μm                   | 7 | JABARDO SP 5면 + BOURDON12 nano 3면 (등가) |
| 1-3 μm                     | 6 | JONES_EDM1p08/2p22 + JABARDO Br_Ra1p2/1p8 + Cu_Ra2p5 + SS_Ra1p45/2p50 |
| 3-10 μm                    | 7 | JONES_EDM5p89 + JABARDO Cu_Ra3p3/4p6 + Br_Ra3p5 + SS_Ra3p20 |
| > 10 μm                    | 2 | JONES_EDM10p0, JABARDO_Cu_Ra10p5SPI |

### 접촉각 별

| 범주 | 개수 | 비고 |
|----|----|------|
| Super-hydrophilic (θ < 20°)        | 6 | BETZ_SHPi, BOURDON12 ungrafted×3, BOURDON15_NotGrafted, etc. |
| Hydrophilic (20° ≤ θ < 60°)         | 5 | PHAN SiOx/TiO2, JO_Hydrophilic, BOURDON15_MPEGPTMS |
| Intermediate (60° ≤ θ < 90°)        | 4 | PHAN Pt/Fe2O3/ref, BOURDON15_AcOUTES |
| Hydrophobic (90° ≤ θ < 130°)        | 5 | BETZ_Hydrophobic, JO_Hydrophobic, BOURDON12 grafted×2, BOURDON15_OTS |
| Super-hydrophobic (θ ≥ 130°)        | 1 | BETZ_SHPo |
| Mixed (biphilic)                    | 3 | BETZ Biphilic, SBPi-circle, SBPi-hex |
| **Unreported (θ 데이터 없음)**       | **25** | JABARDO 20면 + JONES 5면 (EDM 시리즈 + Polished) |

> JABARDO 20면과 JONES EDM/Polished 5면은 원 논문에서 접촉각을 보고하지 않으므로
> CSV 의 `theta_deg`는 빈 값이고, 표면 인코더에서 기본값으로 imputation 된다.

### 재료 별

| 재료 | 개수 | 카드 ID 범위 |
|------|------|-------------|
| Silicon (BETZ + JO)                  |  9 | SFC-001~009 |
| Stainless ribbon (PHAN)              |  5 | SFC-010~014 |
| Aluminum (JONES)                     |  6 | SFC-015~020 |
| Bronze + Au (BOURDON12)              |  5 | SFC-021~025 |
| Float glass (BOURDON15)              |  4 | SFC-026~029 |
| Copper (JABARDO_Cu)                  |  8 | SFC-031~038 |
| Brass (JABARDO_Br)                   |  5 | SFC-039~043 |
| Stainless steel plate (JABARDO_SS)   |  7 | SFC-044~050 |

---

## 향후 보강 항목

- BOURDON_2012 S2의 Sa 정확값 (논문 Fig.X 또는 Table X 확인 필요)
- BETZ Hydrophilic/Hydrophobic의 정확 접촉각 측정값
- JONES Polished의 접촉각 측정값 (논문 supplementary 확인)
- 모든 표면의 공동 밀도 N_s (역문제 분석용)
- 모든 표면의 활성 공동 반경 r_c 분포 (역문제 분석용)
- JABARDO 20면 표면의 접촉각 추정값 (SEM/AFM 보강 시)
