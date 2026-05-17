# ONB 상관식 비교 분석 보고서

> **목적**: PINN 학습 전 baseline reference 성능 수립.
> **데이터**: 43 유효 ONB 포인트 (FC-77 5개 제외) — water(27), R-123(5), R-134a(5), BETZ/BOURDON 등 7개 논문.

---

## 1. 상관식 설명

### 1.1 Hsu (1962)
- **물리 기반**: 자연대류 열경계층 내 기포 선단 온도와 Clausius-Clapeyron 평형 조건.
- **예측 변수**: q'', 유체 물성 (σ, T_sat, k_l, ρ_v, h_fg, cp_l)
- **구현 형식**: ΔT_ONB,min = 8σ T_sat cp_l q'' / (ρ_v h_fg² k_l)  (판별식=0 조건)
- **한계**: 표면 특성(접촉각, 거칠기) 무관. 자연대류 BC 가정.

### 1.2 Davis-Anderson (1966)
- **물리 기반**: Hsu를 단순화. ΔT² 항 무시 → 선형 형태.
- **공식**: ΔT_ONB = 8σ T_sat q'' / (k_l ρ_v h_fg)
- **한계**: ΔT가 크면 과소예측 가능 (2차 항 무시).

### 1.3 Bergles-Rohsenow (1964)
- **물리 기반**: 물 실험 상관 (경험식). P[bar] 의존.
- **공식**: ΔT_ONB = 0.556 × (q''/1082 P^1.156)^(0.463 P^0.0234)
- **적용 범위**: water 전용, 1–138 bar. 비수계 유체에 N/A.

### 1.4 Sato-Matsumura (1964)
- **물리 기반**: Davis-Anderson의 ΔT² 형태 (제곱근 취함).
- **공식**: ΔT_ONB = √(8σ T_sat q'' / (k_l ρ_v h_fg))
- **특징**: DA 대비 낮은 q'' 영역에서 더 큰 예측값.

### 1.5 Basu et al. (2002)
- **물리 기반**: 접촉각 의존 공동 밀도 모델.
- **공식**: F(θ) = 1 − exp(−θ³ − 0.5θ),  ΔT_ONB = √(8σ T_sat q'' / (k_l ρ_v h_fg F(θ)))
- **특징**: 접촉각 θ 데이터 필수. θ=0 발산 → NaN 처리.

---

## 2. 전체 성능 요약

| Model | RMSE [K] | MAE [K] | R² | MRE [%] | n_valid |
|-------|----------|---------|-----|---------|--------|
| Hsu (1962) | 7.43 | 6.07 | -0.978 | 95.03 | 43 |
| Davis-Anderson (1966) ← **최저** | 16.47 | 10.26 | -8.721 | 334.25 | 43 |
| Bergles-Rohsenow (1964) | 7.87 | 6.37 | -0.874 | 98.41 | 33 |
| Sato-Matsumura (1964) | 7.43 | 6.07 | -0.978 | 95.03 | 43 |
| Basu et al. (2002) ← **최고** | 7.21 | 5.85 | -0.208 | 106.71 | 22 |

---

## 3. 분석 결과 해석

### 3.1 최고 성능 상관식: Basu et al. (2002) (RMSE = 7.21 K)

### 3.2 최저 성능 상관식: Davis-Anderson (1966) (RMSE = 16.47 K)

### 3.3 표면/유체별 특이점

- **water (n=27)**: Bergles-Rohsenow가 실험 상관식이므로 water에서 상대적으로 정확.
  Basu는 접촉각 있는 데이터(BETZ, BOURDON, JO, PHAN)에서 유리.
- **R-123 / R-134a (n=5 each)**: BR은 water 전용이므로 N/A. DA와 SM은 물성 기반으로 적용.
  냉매 데이터는 q_flux 범위가 낮아(~2–10 kW/m²) 상관식 예측이 분산될 수 있음.
- **PHAN (subcooled, δT_sub=15K)**: 과냉 보정 없는 상관식은 과소예측 경향.
- **BETZ SHPi/SBPi (δT_wall < 2K)**: 물리 유효 범위 하한 근처 — 상관식 정확도 저하.

### 3.4 PINN 학습 후 비교를 위한 시사점

- **기준 RMSE (최고 상관식)**: 7.21 K
- PINN이 통계적으로 유의한 개선을 보이려면 RMSE를 이 값보다 낮춰야 함.
- 특히 표면 특성(Ra, θ) 의존성과 냉매 데이터 커버리지에서 개선 여지 확인 필요.
- 접촉각 데이터 없는 포인트(jabardo, jones)에서 Basu가 NaN → PINN은 이 포인트도 예측 가능해야 함.

---

## 4. 생성 파일 목록

- `04_analysis/figures/correlation_parity.png` — 5종 parity plot
- `04_analysis/figures/correlation_breakdown_by_surface.png` — source별 AE 박스플롯
- `04_analysis/figures/correlation_breakdown_by_fluid.png` — 유체별 AE 박스플롯
- `04_analysis/tables/correlation_metrics.md` — 지표 표
- `04_analysis/correlation_report.md` — 본 보고서
