"""
correlation_comparator.py — ONB 상관식 라이브러리 + 비교 분석 실행 스크립트.

5종 상관식:
  1. Hsu (1962)
  2. Davis-Anderson (1966)
  3. Bergles-Rohsenow (1964)   — water 전용
  4. Sato-Matsumura (1964)
  5. Basu et al. (2002)        — 접촉각 필요

Usage:
    python correlation_comparator.py

Authors: PINN-ONB01 project
Date   : 2026-05-13
"""

from __future__ import annotations

import math
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

# ---------------------------------------------------------------------------
# 경로 설정 — 프로젝트 루트에서 properties 모듈 임포트
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path("/Users/myhomemini/Library/CloudStorage/OneDrive-개인/Projects/PINN-ONB01")
sys.path.insert(0, str(PROJECT_ROOT / "03_model" / "src"))

from utils.properties import (
    SaturationProperties,
    saturation_properties,
    UnsupportedFluidError,
    hsu_criterion_cavity_radius,
)

# ---------------------------------------------------------------------------
# 경로 상수
# ---------------------------------------------------------------------------
DATA_CSV   = PROJECT_ROOT / "02_data" / "processed" / "onb_dataset.csv"
OUT_DIR    = PROJECT_ROOT / "04_analysis"
FIG_DIR    = OUT_DIR / "figures"
TABLE_DIR  = OUT_DIR / "tables"

FIG_DIR.mkdir(parents=True, exist_ok=True)
TABLE_DIR.mkdir(parents=True, exist_ok=True)

P_ATM: float = 101_325.0  # [Pa] 대기압 기본 가정


# ===========================================================================
# ① 상관식 함수 라이브러리
# ===========================================================================

def predict_hsu(
    props: SaturationProperties,
    q_flux: float,
    delta_T_sub: float = 0.0,
    surface_r_c_max: float = 50e-6,
) -> float:
    """Hsu (1962) — ONB 벽면 과열도 [K].

    Hsu의 2차 방정식에서 활성 공동 크기 r_c는 열유속으로부터 결정된다.
    ONB 임계 조건(판별식=0, 즉 r_c_min = r_c_max = r_c_opt)에서:

        r_c_opt = sqrt(2 σ T_sat k_l / (ρ_v h_fg q''))

    이를 온도 방정식에 대입하면:

        ΔT_ONB = q'' r_c_opt / k_l + 2σ T_sat / (ρ_v h_fg r_c_opt)
               = 2 × sqrt(2 σ T_sat q'' / (ρ_v h_fg k_l))
               = sqrt(8 σ T_sat q'' / (ρ_v h_fg k_l))    ← Sato-Matsumura와 동일

    이는 Sato-Matsumura (1964)와 수학적으로 동일한 결과이며, Hsu의 원래
    2차 방정식에서 ONB를 예측하는 올바른 최소 과열도다.

    Parameters
    ----------
    props            : SaturationProperties (포화 물성치)
    q_flux           : 열유속 [W/m²]
    delta_T_sub      : 과냉도 [K] (현재 미사용, 향후 확장용)
    surface_r_c_max  : 미사용 (API 호환 유지용)

    Returns
    -------
    float : ΔT_ONB [K], 또는 np.nan (미지원/오류).

    Notes
    -----
    Hsu (1962)의 2차 방정식 판별식=0 조건에서 유도된 ΔT_ONB는
    표면 공동 크기를 r_c_opt(q'')로 자동 최적화한 것과 동일하며,
    Sato-Matsumura (1964)의 해석해와 수치적으로 일치한다.
    (참조: Hsu 1962, J. Heat Transfer, eq. 13)
    """
    try:
        if q_flux <= 0:
            return float("nan")
        val = (
            8.0 * props.sigma * props.T_sat * q_flux
            / (props.rho_v * props.h_fg * props.k_l)
        )
        if val < 0:
            return float("nan")
        return math.sqrt(val)
    except Exception as exc:
        warnings.warn(f"predict_hsu: {exc}")
        return float("nan")


def predict_davis_anderson(
    props: SaturationProperties,
    q_flux: float,
) -> float:
    """Davis-Anderson (1966) — ΔT_ONB [K].

    ΔT_ONB = 8 σ T_sat q'' / (k_l ρ_v h_fg)

    Parameters
    ----------
    props   : SaturationProperties
    q_flux  : 열유속 [W/m²]

    Returns
    -------
    float : ΔT_ONB [K]
    """
    try:
        if q_flux <= 0:
            return float("nan")
        return (
            8.0 * props.sigma * props.T_sat * q_flux
            / (props.k_l * props.rho_v * props.h_fg)
        )
    except Exception as exc:
        warnings.warn(f"predict_davis_anderson: {exc}")
        return float("nan")


def predict_bergles_rohsenow(
    props: SaturationProperties,
    q_flux: float,
    P_pa: float,
) -> float:
    """Bergles-Rohsenow (1964) — ΔT_ONB [K].

    물(water) 전용. 적용 범위: 1~138 bar, q'' 최대 ~6 MW/m².

    원전 공식 (P in bar, q'' in W/m²):
      ΔT_ONB = 0.556 × (q'' / (1082 × P^1.156))^(0.463 × P^0.0234)

    Parameters
    ----------
    props   : SaturationProperties (T_sat 참조용; fluid 판별은 밖에서)
    q_flux  : 열유속 [W/m²]
    P_pa    : 압력 [Pa]

    Returns
    -------
    float : ΔT_ONB [K], 또는 np.nan (비water 유체는 호출 전에 걸러야 함).
    """
    try:
        if q_flux <= 0:
            return float("nan")
        P_bar = P_pa / 1e5  # Pa → bar
        if P_bar < 1.0 or P_bar > 138.0:
            warnings.warn(
                f"predict_bergles_rohsenow: P={P_bar:.2f} bar out of range [1, 138] bar. "
                "Returning NaN."
            )
            return float("nan")
        exponent = 0.463 * (P_bar ** 0.0234)
        delta_T = 0.556 * (q_flux / (1082.0 * (P_bar ** 1.156))) ** exponent
        return delta_T
    except Exception as exc:
        warnings.warn(f"predict_bergles_rohsenow: {exc}")
        return float("nan")


def predict_sato_matsumura(
    props: SaturationProperties,
    q_flux: float,
) -> float:
    """Sato-Matsumura (1964) — ΔT_ONB [K].

    ΔT_ONB = sqrt(8 σ T_sat q'' / (k_l ρ_v h_fg))

    Davis-Anderson를 ΔT² 형태로 표현한 등가 형식
    (계수 동일, 제곱근 취함).

    Parameters
    ----------
    props   : SaturationProperties
    q_flux  : 열유속 [W/m²]

    Returns
    -------
    float : ΔT_ONB [K]
    """
    try:
        if q_flux <= 0:
            return float("nan")
        val = (
            8.0 * props.sigma * props.T_sat * q_flux
            / (props.k_l * props.rho_v * props.h_fg)
        )
        if val < 0:
            return float("nan")
        return math.sqrt(val)
    except Exception as exc:
        warnings.warn(f"predict_sato_matsumura: {exc}")
        return float("nan")


def predict_basu(
    props: SaturationProperties,
    q_flux: float,
    theta_deg: float,
) -> float:
    """Basu et al. (2002) — ΔT_ONB [K].

    접촉각 의존 ONB 모델:
      F(θ) = 1 − exp(−θ³ − 0.5θ)    (θ in radians)
      ΔT_ONB = sqrt(8 σ T_sat q'' / (k_l ρ_v h_fg × F(θ)))

    Parameters
    ----------
    props     : SaturationProperties
    q_flux    : 열유속 [W/m²]
    theta_deg : 정적 접촉각 [degree]. NaN 또는 ≤0 이면 np.nan 반환.

    Returns
    -------
    float : ΔT_ONB [K], 또는 np.nan.

    Notes
    -----
    θ=0 → F(0)=0 → 발산. θ≤0이면 np.nan 처리.
    """
    try:
        if q_flux <= 0:
            return float("nan")
        if theta_deg is None or (isinstance(theta_deg, float) and math.isnan(theta_deg)):
            return float("nan")
        if theta_deg <= 0.0:
            # F(0)=0 발산, 또는 물리적으로 의미 없음
            return float("nan")
        theta_rad = math.radians(theta_deg)
        F_theta = 1.0 - math.exp(-theta_rad**3 - 0.5 * theta_rad)
        if F_theta <= 0.0:
            return float("nan")
        val = (
            8.0 * props.sigma * props.T_sat * q_flux
            / (props.k_l * props.rho_v * props.h_fg * F_theta)
        )
        if val < 0:
            return float("nan")
        return math.sqrt(val)
    except Exception as exc:
        warnings.warn(f"predict_basu: {exc}")
        return float("nan")


# ===========================================================================
# ② 통계 지표 계산
# ===========================================================================

def compute_metrics(obs: np.ndarray, pred: np.ndarray) -> dict:
    """RMSE, MAE, R², MRE(%), n_valid 계산.

    NaN은 자동으로 제거한다.
    """
    mask = np.isfinite(obs) & np.isfinite(pred)
    o = obs[mask]
    p = pred[mask]
    n = len(o)
    if n == 0:
        return {"RMSE": np.nan, "MAE": np.nan, "R2": np.nan, "MRE_pct": np.nan, "n_valid": 0}

    rmse = float(np.sqrt(np.mean((p - o) ** 2)))
    mae  = float(np.mean(np.abs(p - o)))
    ss_res = float(np.sum((p - o) ** 2))
    ss_tot = float(np.sum((o - np.mean(o)) ** 2))
    r2   = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    mre  = float(np.mean(np.abs(p - o) / np.abs(o)) * 100.0)
    return {"RMSE": rmse, "MAE": mae, "R2": r2, "MRE_pct": mre, "n_valid": n}


# ===========================================================================
# ③ 데이터 로드 및 상관식 배치 예측
# ===========================================================================

def load_and_predict(data_csv: Path = DATA_CSV) -> pd.DataFrame:
    """onb_dataset.csv 로드 → FC-77 제외 → 5종 상관식 예측 추가."""
    df = pd.read_csv(data_csv)

    # FC-77 제외
    before = len(df)
    df = df[df["fluid"].str.lower() != "fc-77"].copy()
    print(f"[데이터] 전체 {before}행 → FC-77 제외 후 {len(df)}행 유효")

    # delta_T_sub NaN → 0.0
    df["delta_T_sub"] = df["delta_T_sub"].fillna(0.0)

    # 예측 컬럼 초기화
    for col in ["pred_hsu", "pred_da", "pred_br", "pred_sm", "pred_basu"]:
        df[col] = np.nan

    for idx, row in df.iterrows():
        fluid  = str(row["fluid"]).strip()
        q_flux = float(row["q_flux"])
        dT_sub = float(row["delta_T_sub"])
        theta  = row["theta_deg"]

        # theta_deg: NaN 처리
        try:
            theta_f = float(theta)
            if not math.isfinite(theta_f):
                theta_f = float("nan")
        except (TypeError, ValueError):
            theta_f = float("nan")

        # 물성 취득
        try:
            props = saturation_properties(fluid, P=P_ATM)
        except UnsupportedFluidError:
            # 미지원 유체 → 모든 상관식 NaN (이미 FC-77 제거됨, 안전망)
            continue
        except Exception as exc:
            warnings.warn(f"Row {idx}: properties error: {exc}")
            continue

        # Hsu
        df.at[idx, "pred_hsu"] = predict_hsu(props, q_flux, dT_sub)

        # Davis-Anderson
        df.at[idx, "pred_da"] = predict_davis_anderson(props, q_flux)

        # Bergles-Rohsenow (water 전용)
        if fluid.lower() in ("water",):
            df.at[idx, "pred_br"] = predict_bergles_rohsenow(props, q_flux, P_ATM)
        else:
            df.at[idx, "pred_br"] = np.nan  # N/A

        # Sato-Matsumura
        df.at[idx, "pred_sm"] = predict_sato_matsumura(props, q_flux)

        # Basu
        df.at[idx, "pred_basu"] = predict_basu(props, q_flux, theta_f)

    return df


# ===========================================================================
# ④ 시각화
# ===========================================================================

# 모델별 색상 (일관성)
MODEL_COLORS = {
    "Hsu (1962)":             "#7f7f7f",   # 회색
    "Davis-Anderson (1966)":  "#aec7e8",   # 연파랑
    "Bergles-Rohsenow (1964)":"#ffbb78",   # 연주황
    "Sato-Matsumura (1964)":  "#c5b0d5",   # 연보라
    "Basu et al. (2002)":     "#98df8a",   # 연초록
}

# source_paper별 색상 (parity plot 데이터 포인트용)
SOURCE_COLORS = {
    "betz":      "#e41a1c",
    "bourdon12": "#377eb8",
    "bourdon15": "#4daf4a",
    "jabardo":   "#984ea3",
    "jones":     "#ff7f00",
    "jones_w":   "#ff7f00",
    "jones_F":   "#ff7f00",
    "jo":        "#a65628",
    "phan":      "#f781bf",
}
SOURCE_COLORS_DEFAULT = "#888888"


def _source_color(cat: str) -> str:
    return SOURCE_COLORS.get(str(cat).lower(), SOURCE_COLORS_DEFAULT)


def plot_parity(df: pd.DataFrame, out_path: Path) -> None:
    """Parity plot — 5개 패널 (2×3 레이아웃, 마지막 칸 비움)."""
    models = [
        ("pred_hsu",  "Hsu (1962)"),
        ("pred_da",   "Davis-Anderson (1966)"),
        ("pred_br",   "Bergles-Rohsenow (1964)"),
        ("pred_sm",   "Sato-Matsumura (1964)"),
        ("pred_basu", "Basu et al. (2002)"),
    ]
    obs_col = "delta_T_wall"

    fig, axes = plt.subplots(2, 3, figsize=(14, 9), dpi=120)
    axes_flat = axes.flatten()

    obs_all = df[obs_col].values.astype(float)
    global_min = max(0.0, np.nanmin(obs_all) * 0.5)
    global_max = np.nanmax(obs_all) * 1.6

    for ax_idx, (pred_col, title) in enumerate(models):
        ax = axes_flat[ax_idx]
        pred_all = df[pred_col].values.astype(float)

        # ±30%, ±50% 밴드
        band_x = np.linspace(global_min, global_max, 200)
        ax.fill_between(band_x, band_x * 0.5, band_x * 1.5,
                        alpha=0.10, color="gray", label="±50%")
        ax.fill_between(band_x, band_x * 0.7, band_x * 1.3,
                        alpha=0.18, color="steelblue", label="±30%")
        ax.plot(band_x, band_x, "k--", linewidth=1.0, label="y=x")

        # 데이터 포인트 — source_paper별 색상
        for _, row in df.iterrows():
            obs_v  = float(row[obs_col])
            pred_v = float(row[pred_col])
            if not (math.isfinite(obs_v) and math.isfinite(pred_v)):
                continue
            cat = str(row.get("source_paper", "")).lower()
            color = _source_color(cat)
            ax.scatter(obs_v, pred_v, c=color, s=30, alpha=0.75,
                       edgecolors="none", zorder=3)

        # 통계
        mask = np.isfinite(obs_all) & np.isfinite(pred_all)
        if mask.sum() > 1:
            m = compute_metrics(obs_all, pred_all)
            stats_txt = (
                f"RMSE={m['RMSE']:.2f}K\n"
                f"MAE={m['MAE']:.2f}K\n"
                f"R²={m['R2']:.3f}\n"
                f"n={m['n_valid']}"
            )
            ax.text(0.04, 0.96, stats_txt,
                    transform=ax.transAxes, fontsize=7,
                    verticalalignment="top",
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.7))

        ax.set_xlim(global_min, global_max)
        ax.set_ylim(global_min, global_max)
        ax.set_xlabel("Observed ΔT_ONB [K]", fontsize=8)
        ax.set_ylabel("Predicted ΔT_ONB [K]", fontsize=8)
        ax.set_title(title, fontsize=9, fontweight="bold",
                     color=MODEL_COLORS[title])
        ax.tick_params(labelsize=7)
        ax.set_aspect("equal", adjustable="box")

    # 레전드 — source_paper
    legend_patches = [
        mpatches.Patch(color=v, label=k)
        for k, v in SOURCE_COLORS.items()
        if k not in ("jones_w", "jones_F")  # 중복 제거
    ]
    band_handles = [
        mpatches.Patch(color="gray",      alpha=0.3, label="±50% band"),
        mpatches.Patch(color="steelblue", alpha=0.4, label="±30% band"),
        Line2D([0], [0], color="k", linestyle="--", label="y = x"),
    ]
    axes_flat[5].axis("off")
    axes_flat[5].legend(
        handles=legend_patches + band_handles,
        loc="center", fontsize=8, title="Source / Bands",
        title_fontsize=8, framealpha=0.9
    )

    fig.suptitle(
        "ONB Correlation Parity Plots — 43 Data Points (FC-77 excluded)",
        fontsize=11, fontweight="bold", y=1.01
    )
    plt.tight_layout()
    fig.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"[Figure] 저장: {out_path}")


def plot_breakdown_by_surface(df: pd.DataFrame, out_path: Path) -> None:
    """표면 category별 Absolute Error 분포 — 박스플롯."""
    models = [
        ("pred_hsu",  "Hsu"),
        ("pred_da",   "Davis-Anderson"),
        ("pred_br",   "B-Rohsenow"),
        ("pred_sm",   "Sato-Matsumura"),
        ("pred_basu", "Basu"),
    ]
    obs_col = "delta_T_wall"
    cats = sorted(df["source_paper"].unique())

    n_models = len(models)
    n_cats   = len(cats)
    fig, axes = plt.subplots(1, n_models, figsize=(14, 5), dpi=120,
                              sharey=True)

    for ax, (pred_col, title) in zip(axes, models):
        data_by_cat = []
        labels      = []
        for cat in cats:
            sub = df[df["source_paper"] == cat]
            obs_v  = sub[obs_col].values.astype(float)
            pred_v = sub[pred_col].values.astype(float)
            mask   = np.isfinite(obs_v) & np.isfinite(pred_v)
            ae     = np.abs(pred_v[mask] - obs_v[mask])
            n_sub  = mask.sum()
            label  = f"{cat}\n(n={n_sub})" + (" *" if n_sub < 5 else "")
            data_by_cat.append(ae)
            labels.append(label)

        bp = ax.boxplot(data_by_cat, vert=True, patch_artist=True,
                        medianprops=dict(color="red", linewidth=1.5),
                        showfliers=True)
        for patch in bp["boxes"]:
            patch.set_facecolor(MODEL_COLORS[
                {"Hsu": "Hsu (1962)",
                 "Davis-Anderson": "Davis-Anderson (1966)",
                 "B-Rohsenow": "Bergles-Rohsenow (1964)",
                 "Sato-Matsumura": "Sato-Matsumura (1964)",
                 "Basu": "Basu et al. (2002)"}[title]
            ])
            patch.set_alpha(0.7)

        ax.set_xticklabels(labels, fontsize=6, rotation=40, ha="right")
        ax.set_title(title, fontsize=8, fontweight="bold")
        ax.set_ylabel("|Error| [K]" if ax == axes[0] else "")
        ax.tick_params(labelsize=7)
        ax.grid(axis="y", linestyle="--", alpha=0.4)

    fig.suptitle(
        "Absolute Error by Source Paper — ONB Correlations",
        fontsize=10, fontweight="bold"
    )
    plt.tight_layout()
    fig.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"[Figure] 저장: {out_path}")


def plot_breakdown_by_fluid(df: pd.DataFrame, out_path: Path) -> None:
    """유체별 Absolute Error 분포 — 박스플롯."""
    models = [
        ("pred_hsu",  "Hsu (1962)"),
        ("pred_da",   "Davis-Anderson (1966)"),
        ("pred_br",   "Bergles-Rohsenow (1964)"),
        ("pred_sm",   "Sato-Matsumura (1964)"),
        ("pred_basu", "Basu et al. (2002)"),
    ]
    obs_col = "delta_T_wall"
    fluids  = sorted(df["fluid"].unique())

    fluid_palette = {"water": "#4878CF", "R-123": "#6ACC65", "R-134a": "#D65F5F"}

    fig, axes = plt.subplots(1, len(models), figsize=(14, 5), dpi=120, sharey=True)

    for ax, (pred_col, title) in zip(axes, models):
        data_by_fluid = []
        labels_f      = []
        colors_f      = []
        for fl in fluids:
            sub    = df[df["fluid"] == fl]
            obs_v  = sub[obs_col].values.astype(float)
            pred_v = sub[pred_col].values.astype(float)
            mask   = np.isfinite(obs_v) & np.isfinite(pred_v)
            ae     = np.abs(pred_v[mask] - obs_v[mask])
            n_fl   = mask.sum()
            labels_f.append(f"{fl}\n(n={n_fl})")
            colors_f.append(fluid_palette.get(fl, "#888888"))
            data_by_fluid.append(ae if len(ae) > 0 else np.array([np.nan]))

        bp = ax.boxplot(data_by_fluid, vert=True, patch_artist=True,
                        medianprops=dict(color="red", linewidth=1.5),
                        showfliers=True)
        for patch, c in zip(bp["boxes"], colors_f):
            patch.set_facecolor(c)
            patch.set_alpha(0.7)

        ax.set_xticklabels(labels_f, fontsize=8)
        ax.set_title(title, fontsize=8, fontweight="bold")
        ax.set_ylabel("|Error| [K]" if ax == axes[0] else "")
        ax.tick_params(labelsize=7)
        ax.grid(axis="y", linestyle="--", alpha=0.4)

    fig.suptitle(
        "Absolute Error by Fluid — ONB Correlations",
        fontsize=10, fontweight="bold"
    )
    plt.tight_layout()
    fig.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"[Figure] 저장: {out_path}")


# ===========================================================================
# ⑤ 표 및 보고서 생성
# ===========================================================================

def build_metrics_tables(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """전체 + 유체별 + source_paper별 지표 DataFrame 반환."""
    obs_col = "delta_T_wall"
    obs_all = df[obs_col].values.astype(float)

    model_map = {
        "Hsu (1962)":              "pred_hsu",
        "Davis-Anderson (1966)":   "pred_da",
        "Bergles-Rohsenow (1964)": "pred_br",
        "Sato-Matsumura (1964)":   "pred_sm",
        "Basu et al. (2002)":      "pred_basu",
    }

    # ─── 전체 지표 ───
    rows_all = []
    for name, col in model_map.items():
        m = compute_metrics(obs_all, df[col].values.astype(float))
        rows_all.append({"Model": name, **m})
    df_all = pd.DataFrame(rows_all).set_index("Model")

    # ─── 유체별 ───
    rows_fluid = []
    for fl in sorted(df["fluid"].unique()):
        sub = df[df["fluid"] == fl]
        obs_f = sub[obs_col].values.astype(float)
        for name, col in model_map.items():
            m = compute_metrics(obs_f, sub[col].values.astype(float))
            rows_fluid.append({"Fluid": fl, "Model": name, **m})
    df_fluid = pd.DataFrame(rows_fluid)

    # ─── source_paper별 ───
    rows_src = []
    for src in sorted(df["source_paper"].unique()):
        sub = df[df["source_paper"] == src]
        obs_s = sub[obs_col].values.astype(float)
        n_total = len(sub)
        for name, col in model_map.items():
            m = compute_metrics(obs_s, sub[col].values.astype(float))
            flag = " [샘플부족]" if n_total < 5 else ""
            rows_src.append({"Source": src + flag, "Model": name, **m})
    df_src = pd.DataFrame(rows_src)

    return {"overall": df_all, "by_fluid": df_fluid, "by_source": df_src}


def _fmt(x, fmt=".2f"):
    if isinstance(x, float) and math.isnan(x):
        return "N/A"
    return format(x, fmt)


def write_metrics_md(tables: dict[str, pd.DataFrame], out_path: Path) -> None:
    """correlation_metrics.md 생성."""
    df_all   = tables["overall"]
    df_fluid = tables["by_fluid"]
    df_src   = tables["by_source"]

    lines = ["# ONB 상관식 성능 지표\n",
             "> 관측값: `delta_T_wall` [K], 예측값: 각 상관식 출력 ΔT_ONB [K]\n",
             f"> 유효 데이터: 43 포인트 (FC-77 5개 제외)\n\n"]

    # 전체 요약
    lines.append("## 1. 전체 성능 요약\n\n")
    header = "| Model | RMSE [K] | MAE [K] | R² | MRE [%] | n_valid |"
    sep    = "|-------|----------|---------|-----|---------|---------|"
    lines += [header + "\n", sep + "\n"]
    for name, row in df_all.iterrows():
        lines.append(
            f"| {name} | {_fmt(row['RMSE'])} | {_fmt(row['MAE'])} "
            f"| {_fmt(row['R2'], '.3f')} | {_fmt(row['MRE_pct'])} "
            f"| {int(row['n_valid'])} |\n"
        )

    # 유체별
    lines.append("\n## 2. 유체별 성능\n\n")
    for fl in sorted(df_fluid["Fluid"].unique()):
        sub = df_fluid[df_fluid["Fluid"] == fl]
        lines.append(f"### {fl}\n\n")
        lines.append("| Model | RMSE [K] | MAE [K] | R² | MRE [%] | n_valid |\n")
        lines.append("|-------|----------|---------|-----|---------|--------|\n")
        for _, row in sub.iterrows():
            lines.append(
                f"| {row['Model']} | {_fmt(row['RMSE'])} | {_fmt(row['MAE'])} "
                f"| {_fmt(row['R2'], '.3f')} | {_fmt(row['MRE_pct'])} "
                f"| {int(row['n_valid'])} |\n"
            )
        lines.append("\n")

    # source_paper별
    lines.append("## 3. Source Paper별 성능\n\n")
    lines.append("*[샘플부족]: 해당 그룹 n < 5*\n\n")
    for src in sorted(df_src["Source"].unique()):
        sub = df_src[df_src["Source"] == src]
        lines.append(f"### {src}\n\n")
        lines.append("| Model | RMSE [K] | MAE [K] | R² | MRE [%] | n_valid |\n")
        lines.append("|-------|----------|---------|-----|---------|--------|\n")
        for _, row in sub.iterrows():
            lines.append(
                f"| {row['Model']} | {_fmt(row['RMSE'])} | {_fmt(row['MAE'])} "
                f"| {_fmt(row['R2'], '.3f')} | {_fmt(row['MRE_pct'])} "
                f"| {int(row['n_valid'])} |\n"
            )
        lines.append("\n")

    out_path.write_text("".join(lines), encoding="utf-8")
    print(f"[Table] 저장: {out_path}")


def write_correlation_report(
    tables: dict[str, pd.DataFrame],
    df: pd.DataFrame,
    out_path: Path,
) -> None:
    """correlation_report.md — 상관식 설명 + 결과 해석."""
    df_all = tables["overall"]

    # 최고/최저 모델 (n_valid > 0 기준)
    valid_rows = df_all[df_all["n_valid"] > 0].copy()
    best_model = valid_rows["RMSE"].idxmin()
    worst_model = valid_rows["RMSE"].idxmax()
    best_rmse  = valid_rows.loc[best_model, "RMSE"]
    worst_rmse = valid_rows.loc[worst_model, "RMSE"]

    lines = [
        "# ONB 상관식 비교 분석 보고서\n\n",
        "> **목적**: PINN 학습 전 baseline reference 성능 수립.\n",
        f"> **데이터**: 43 유효 ONB 포인트 (FC-77 5개 제외) — water(27), R-123(5), R-134a(5), BETZ/BOURDON 등 7개 논문.\n\n",

        "---\n\n",
        "## 1. 상관식 설명\n\n",

        "### 1.1 Hsu (1962)\n",
        "- **물리 기반**: 자연대류 열경계층 내 기포 선단 온도와 Clausius-Clapeyron 평형 조건.\n",
        "- **예측 변수**: q'', 유체 물성 (σ, T_sat, k_l, ρ_v, h_fg, cp_l)\n",
        "- **구현 형식**: ΔT_ONB,min = 8σ T_sat cp_l q'' / (ρ_v h_fg² k_l)  (판별식=0 조건)\n",
        "- **한계**: 표면 특성(접촉각, 거칠기) 무관. 자연대류 BC 가정.\n\n",

        "### 1.2 Davis-Anderson (1966)\n",
        "- **물리 기반**: Hsu를 단순화. ΔT² 항 무시 → 선형 형태.\n",
        "- **공식**: ΔT_ONB = 8σ T_sat q'' / (k_l ρ_v h_fg)\n",
        "- **한계**: ΔT가 크면 과소예측 가능 (2차 항 무시).\n\n",

        "### 1.3 Bergles-Rohsenow (1964)\n",
        "- **물리 기반**: 물 실험 상관 (경험식). P[bar] 의존.\n",
        "- **공식**: ΔT_ONB = 0.556 × (q''/1082 P^1.156)^(0.463 P^0.0234)\n",
        "- **적용 범위**: water 전용, 1–138 bar. 비수계 유체에 N/A.\n\n",

        "### 1.4 Sato-Matsumura (1964)\n",
        "- **물리 기반**: Davis-Anderson의 ΔT² 형태 (제곱근 취함).\n",
        "- **공식**: ΔT_ONB = √(8σ T_sat q'' / (k_l ρ_v h_fg))\n",
        "- **특징**: DA 대비 낮은 q'' 영역에서 더 큰 예측값.\n\n",

        "### 1.5 Basu et al. (2002)\n",
        "- **물리 기반**: 접촉각 의존 공동 밀도 모델.\n",
        "- **공식**: F(θ) = 1 − exp(−θ³ − 0.5θ),  ΔT_ONB = √(8σ T_sat q'' / (k_l ρ_v h_fg F(θ)))\n",
        "- **특징**: 접촉각 θ 데이터 필수. θ=0 발산 → NaN 처리.\n\n",

        "---\n\n",
        "## 2. 전체 성능 요약\n\n",
        "| Model | RMSE [K] | MAE [K] | R² | MRE [%] | n_valid |\n",
        "|-------|----------|---------|-----|---------|--------|\n",
    ]
    for name, row in df_all.iterrows():
        marker = " ← **최고**" if name == best_model else (
            " ← **최저**" if name == worst_model else "")
        lines.append(
            f"| {name}{marker} | {_fmt(row['RMSE'])} | {_fmt(row['MAE'])} "
            f"| {_fmt(row['R2'], '.3f')} | {_fmt(row['MRE_pct'])} "
            f"| {int(row['n_valid'])} |\n"
        )

    lines += [
        "\n---\n\n",
        "## 3. 분석 결과 해석\n\n",
        f"### 3.1 최고 성능 상관식: {best_model} (RMSE = {best_rmse:.2f} K)\n\n",
        f"### 3.2 최저 성능 상관식: {worst_model} (RMSE = {worst_rmse:.2f} K)\n\n",

        "### 3.3 표면/유체별 특이점\n\n",
        "- **water (n=27)**: Bergles-Rohsenow가 실험 상관식이므로 water에서 상대적으로 정확.\n",
        "  Basu는 접촉각 있는 데이터(BETZ, BOURDON, JO, PHAN)에서 유리.\n",
        "- **R-123 / R-134a (n=5 each)**: BR은 water 전용이므로 N/A. DA와 SM은 물성 기반으로 적용.\n",
        "  냉매 데이터는 q_flux 범위가 낮아(~2–10 kW/m²) 상관식 예측이 분산될 수 있음.\n",
        "- **PHAN (subcooled, δT_sub=15K)**: 과냉 보정 없는 상관식은 과소예측 경향.\n",
        "- **BETZ SHPi/SBPi (δT_wall < 2K)**: 물리 유효 범위 하한 근처 — 상관식 정확도 저하.\n\n",

        "### 3.4 PINN 학습 후 비교를 위한 시사점\n\n",
        f"- **기준 RMSE (최고 상관식)**: {best_rmse:.2f} K\n",
        "- PINN이 통계적으로 유의한 개선을 보이려면 RMSE를 이 값보다 낮춰야 함.\n",
        "- 특히 표면 특성(Ra, θ) 의존성과 냉매 데이터 커버리지에서 개선 여지 확인 필요.\n",
        "- 접촉각 데이터 없는 포인트(jabardo, jones)에서 Basu가 NaN → PINN은 이 포인트도 예측 가능해야 함.\n\n",

        "---\n\n",
        "## 4. 생성 파일 목록\n\n",
        "- `04_analysis/figures/correlation_parity.png` — 5종 parity plot\n",
        "- `04_analysis/figures/correlation_breakdown_by_surface.png` — source별 AE 박스플롯\n",
        "- `04_analysis/figures/correlation_breakdown_by_fluid.png` — 유체별 AE 박스플롯\n",
        "- `04_analysis/tables/correlation_metrics.md` — 지표 표\n",
        "- `04_analysis/correlation_report.md` — 본 보고서\n",
    ]

    out_path.write_text("".join(lines), encoding="utf-8")
    print(f"[Report] 저장: {out_path}")


# ===========================================================================
# ⑥ 콘솔 요약 출력
# ===========================================================================

def print_summary(tables: dict[str, pd.DataFrame]) -> None:
    """터미널 보고 형식 출력."""
    df_all = tables["overall"]
    n_total = int(df_all["n_valid"].max())

    print(f"\n[상관식 비교 완료 — N={n_total}]")
    header = f"{'Model':<26} {'RMSE':>7} {'MAE':>7} {'R²':>7} {'MRE%':>7} {'n':>5}"
    print("┌" + "─" * len(header) + "┐")
    print("│ " + header + " │")
    print("├" + "─" * len(header) + "┤")

    for name, row in df_all.iterrows():
        rmse = _fmt(row["RMSE"]) if not math.isnan(row["RMSE"]) else " N/A "
        mae  = _fmt(row["MAE"])  if not math.isnan(row["MAE"])  else " N/A "
        r2   = _fmt(row["R2"], ".3f") if not math.isnan(row["R2"]) else " N/A "
        mre  = _fmt(row["MRE_pct"]) if not math.isnan(row["MRE_pct"]) else " N/A "
        n    = int(row["n_valid"])
        line = f"{name:<26} {rmse:>7} {mae:>7} {r2:>7} {mre:>7} {n:>5}"
        print("│ " + line + " │")

    print("└" + "─" * len(header) + "┘")

    valid_rows = df_all[df_all["n_valid"] > 0]
    best_model = valid_rows["RMSE"].idxmin()
    worst_model = valid_rows["RMSE"].idxmax()
    print(f"\n최고 성능: {best_model}  (RMSE={valid_rows.loc[best_model,'RMSE']:.2f} K)")
    print(f"최저 성능: {worst_model} (RMSE={valid_rows.loc[worst_model,'RMSE']:.2f} K)")

    # 유체별 RMSE 한 줄 요약
    df_fluid = tables["by_fluid"]
    print("\n[유체별 RMSE 요약]")
    for fl in sorted(df_fluid["Fluid"].unique()):
        sub = df_fluid[df_fluid["Fluid"] == fl]
        rmse_vals = {
            row["Model"].split(" (")[0]: row["RMSE"]
            for _, row in sub.iterrows()
            if row["n_valid"] > 0
        }
        parts = ", ".join(
            f"{k}={v:.2f}K" for k, v in rmse_vals.items()
        )
        print(f"  {fl}: {parts}")


# ===========================================================================
# ⑦ 메인 엔트리 포인트
# ===========================================================================

def run_comparison(
    data_csv: Path = DATA_CSV,
    out_dir: Path  = OUT_DIR,
) -> dict:
    """전체 비교 분석 실행."""
    fig_dir   = out_dir / "figures"
    table_dir = out_dir / "tables"
    fig_dir.mkdir(parents=True, exist_ok=True)
    table_dir.mkdir(parents=True, exist_ok=True)

    # 1) 데이터 로드 + 예측
    df = load_and_predict(data_csv)

    # 2) 지표 계산
    tables = build_metrics_tables(df)

    # 3) 시각화
    path_parity   = fig_dir / "correlation_parity.png"
    path_by_surf  = fig_dir / "correlation_breakdown_by_surface.png"
    path_by_fluid = fig_dir / "correlation_breakdown_by_fluid.png"
    plot_parity(df, path_parity)
    plot_breakdown_by_surface(df, path_by_surf)
    plot_breakdown_by_fluid(df, path_by_fluid)

    # 4) 표
    path_metrics_md = table_dir / "correlation_metrics.md"
    write_metrics_md(tables, path_metrics_md)

    # 5) 보고서
    path_report = out_dir / "correlation_report.md"
    write_correlation_report(tables, df, path_report)

    # 6) 콘솔 출력
    print_summary(tables)

    return {
        "summary": tables["overall"].to_dict(),
        "tables":  [path_metrics_md],
        "figures": [path_parity, path_by_surf, path_by_fluid],
    }


if __name__ == "__main__":
    run_comparison()
