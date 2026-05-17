# Surface Cards Index

**작성일:** 2026-05-10
**총 표면 수:** 30 (SFC-001 ~ SFC-030)
**기준 데이터:** 1군 6편 디지타이즈 결과 (38 ONB 포인트)

---

## 표면 카드 정의

각 카드는 디지타이즈 데이터 기반 raw 표면 정보 + 표면 처리/코팅 메타데이터. 본 인덱스 파일에서 모든 카드를 통합 관리.

### 1. BETZ_2013 — Boiling enhancement on patterned wettability surfaces

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
| SFC-008 | JO_Hydrophilic | 0.00175 | 54 | SiO₂ pure | figure_3_Hydrophilic |
| SFC-009 | JO_Hydrophobic | 0.00175 | 123 | Teflon pure | figure_3_Hydrophobic |

### 3. PHAN_2009 — Nano-coated stainless ribbon (subcooled, ΔT_sub=15K)

| ID | Label | Ra (nm) | θ_static (°) | Coating / Method | 디지타이즈 시리즈 |
|----|-------|---------|--------------|------------------|------------------|
| SFC-010 | PHAN_SiOx | ~30 | 22 | SiOx, PECVD | figure_12a_theta22 |
| SFC-011 | PHAN_TiO2 | ~30 | 31 | TiO₂, NNBD | figure_12a_theta31 |
| SFC-012 | PHAN_Pt | ~30 | 67 | Pt, MOCVD | figure_12a_theta67 |
| SFC-013 | PHAN_Fe2O3 | ~30 | 80 | Fe₂O₃, MOCVD | figure_12a_theta80 |
| SFC-014 | PHAN_ref | ~30 | 85 | Stainless, no coating | figure_12a_theta85 |

### 4. JONES_2009 — EDM-roughened Al, water + FC-77

| ID | Label | Ra (μm) | θ_static (°) | Treatment | 디지타이즈 시리즈 |
|----|-------|---------|--------------|-----------|------------------|
| SFC-015 | JONES_Polished_water | 0.038 | (water-specific) | Polished Al | figure_3a_Polished (water) |
| SFC-016 | JONES_Polished_FC77 | 0.027 | (FC-77-specific) | Polished Al | figure_4a_Polished (FC-77) |
| SFC-017 | JONES_EDM1p08 | 1.08 | (Al, no coating) | EDM | figure_3a_EDM1p08, figure_4a_EDM1p08 |
| SFC-018 | JONES_EDM2p22 | 2.22 | (Al, no coating) | EDM | figure_3a_EDM2p22, figure_4a_EDM2p22 |
| SFC-019 | JONES_EDM5p89 | 5.89 | (Al, no coating) | EDM | figure_3a_EDM5p89, figure_4a_EDM5p89 |
| SFC-020 | JONES_EDM10p0 | 10.0 | (Al, no coating) | EDM | figure_3a_EDM10p0, figure_4a_EDM10p0 |

### 5. BOURDON_2012 — Bronze plate + Au + alkanethiol grafting

| ID | Label | Sa (nm) | θ_advancing (°) | Treatment | 디지타이즈 시리즈 |
|----|-------|---------|------------------|-----------|------------------|
| SFC-021 | BOURDON12_S1 | ~9.7 | 0 | Bronze + 24.8nm Au, polished (rougher) | figure_4_S1, figure_6_ungrafted |
| SFC-022 | BOURDON12_S2 | ~8.6 | 0 | Bronze + Au, intermediate | figure_4_S2 |
| SFC-023 | BOURDON12_S3 | ~7.6 | 0 | Bronze + Au, smoothest | figure_4_S3 |
| SFC-024 | BOURDON12_S1_grafted_whole | ~9.7 | 108 | S1 + alkanethiol SAM (whole plate) | figure_6_grafted_whole |
| SFC-025 | BOURDON12_S1_grafted_center | ~9.7 | 108 (center) | S1 + alkanethiol SAM (15mm center only) | figure_6_grafted_center |

### 6. BOURDON_2015 — Float glass + silane SAM (ultra-smooth)

| ID | Label | Sa (nm) | θ_static (°) | Treatment | 디지타이즈 시리즈 |
|----|-------|---------|--------------|-----------|------------------|
| SFC-026 | BOURDON15_NotGrafted | 0.43 | 11.1 | Float glass, no grafting (super-hydrophilic) | figure_3 (theta11.1deg row), figure_7_NotGrafted |
| SFC-027 | BOURDON15_MPEGPTMS | 0.43 | 33.5 | Silane SAM (MPEGPTMS) | figure_3 (theta33.5deg row), figure_7_MPEGPTMS |
| SFC-028 | BOURDON15_AcOUTES | 0.43 | 70.8 | Silane SAM (AcOUTES) | figure_3 (theta70.8deg row), figure_7_AcOUTES |
| SFC-029 | BOURDON15_OTS | 0.43 | 101.6 | Silane SAM (OTS) | figure_3 (theta101.6deg row), figure_7_OTS |

### 7. External References (BETZ Fig.7b 비교 데이터)

| ID | Label | 출처 | Notes |
|----|-------|------|-------|
| SFC-030 | EXT_REFs_Fig7b | Chen 2009, Jones 10μm/Polished, Li 2008 | BETZ가 Fig.7b에 비교용으로 인용 |

---

## 표면 분포 통계

| 분류 | 개수 |
|----|----|
| **거칠기 별** | |
| Sub-nm (Sa < 1 nm) | 5 (SFC-026~029) + BETZ nano = 8 |
| Nano (1-100 nm) | 8 (BETZ nano-pattern + JO nano + PHAN ~30nm + BOURDON12 nano) |
| Polished (Ra < 0.1 μm) | 2 (JONES Polished water + FC-77) |
| EDM (1-10 μm) | 4 (JONES EDM 1.08~10.0) |
| **접촉각 별** | |
| Super-hydrophilic (θ < 20°) | 6 (BETZ_SHPi, BOURDON12 ungrafted×3, BOURDON15 NotGrafted, BOURDON12 SAM 0°) |
| Hydrophilic (20° ≤ θ < 60°) | 5 (PHAN SiOx/TiO2, JO Hydrophilic, BOURDON15 MPEGPTMS) |
| Intermediate (60° ≤ θ < 90°) | 4 (PHAN Pt/Fe2O3/ref, BOURDON15 AcOUTES) |
| Hydrophobic (90° ≤ θ < 130°) | 5 (BETZ Hydrophobic, JO Hydrophobic, BOURDON12 grafted×2, BOURDON15 OTS) |
| Super-hydrophobic (θ ≥ 130°) | 1 (BETZ_SHPo) |
| Mixed (biphilic) | 3 (BETZ Biphilic, SBPi-circle, SBPi-hexagon) |

---

## 향후 보강 항목

- BOURDON_2012 S2의 Sa 정확값 (논문 Fig.X 또는 Table X 확인 필요)
- BETZ Hydrophilic/Hydrophobic의 정확 접촉각 측정값
- JONES Polished의 접촉각 측정값 (논문 supplementary 확인)
- 모든 표면의 공동 밀도 N_s (역문제 분석용)
- 모든 표면의 활성 공동 반경 r_c 분포 (역문제 분석용)
