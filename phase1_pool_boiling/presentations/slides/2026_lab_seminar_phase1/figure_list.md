# Figures for 2026 Lab Seminar (Phase 1) — Upload to Claude Design separately

Claude Design 웹 UI 에서 prompt.md paste 후, **다음 figure 파일들을 별도 업로드** 해주세요.

| Slide | File path (workspace root 기준 상대 경로) | 설명 | 우선순위 |
|---|---|---|---|
| 10 | `05_manuscript/figures/fig03_pinn_parity.png` | **PINN headline parity** (RMSE 3.42 K) | ⭐⭐⭐ 필수 |
| 11 | `05_manuscript/figures/fig02_correlation_parity.png` | PINN + 5 classical correlations 6-panel | ⭐⭐⭐ 필수 |
| 12 | `05_manuscript/figures/fig07_physics_trends_composite.png` | 5 trends + 1 Simpson | ⭐⭐⭐ 필수 |
| 13 | `05_manuscript/figures/fig04_ensemble_errorbars.png` | Coverage 98.7% UQ | ⭐⭐⭐ 필수 |
| 13 (opt) | `05_manuscript/figures/fig05_std_by_category.png` | σ by surface category | ⭐⭐ 선택 |
| 14 | `05_manuscript/figures/fig08_inverse_rc_vs_Ra.png` | Hsu inverse — Simpson's paradox | ⭐⭐⭐ 필수 |
| 14 (opt) | `05_manuscript/figures/fig09_inverse_rc_by_category.png` | Per-category r_c | ⭐⭐ 선택 |
| 1 (옵션) | `05_manuscript/figures/graphical_abstract.png` | Title 슬라이드 또는 outline 배경 | ⭐ 선택 |

## Total

- **필수 5개** (slide 10, 11, 12, 13, 14)
- **선택 3개** (slide 13 보조, slide 14 보조, title 배경)

## 파일 형식

- 모든 PNG 가 300 DPI 로 저장됨 — slide 사용 충분
- PDF / EPS 도 동일 폴더 존재 (필요 시 사용)
- Claude Design 은 PNG 권장

## 업로드 후 확인 사항

- [ ] Slide 10 (parity plot): 좌측 x축 label "observed ΔT_ONB [K]", 우측 RMSE annotation 보임
- [ ] Slide 11 (6-panel): 모든 6 panel 가독 (PINN + 5 classical)
- [ ] Slide 12 (trends): 5 subpanels 라벨 보임 (q, Ra, θ, P, sub)
- [ ] Slide 13 (UQ): error bar + parity line 가독
- [ ] Slide 14 (inverse): scatter + trend line 보임

## 잘 안 보이는 경우

- 폰트가 작거나 안 보이면 — 원본 matplotlib 스크립트
  (`04_analysis/scripts/compose_figures.py` 등) 의 `font.size` 키워드 조정 후
  재생성
- Color 가 흐릿하면 — `--dpi 600` 옵션으로 재생성
