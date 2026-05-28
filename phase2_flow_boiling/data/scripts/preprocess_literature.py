#!/usr/bin/env python3
"""
Phase 2 Flow Boiling ONB — Literature Data Preprocessing
Raw WPD CSV → standard schema (SI units)

Run:
    python3 data/scripts/preprocess_literature.py

Output:
    data/raw/onb_dataset_phase2_raw.csv   (전체 병합, 단위 변환 완료)
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

# ── Paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
DATA_DIR   = SCRIPT_DIR.parent          # phase2_flow_boiling/data/
LIT_DIR    = DATA_DIR / "raw" / "literature"
OUT_FILE   = DATA_DIR / "raw" / "onb_dataset_phase2_raw.csv"

# ── Unit conversion constants ──────────────────────────────────────────────────
BTU_H_FT2_TO_W_M2 = 3.15459   # Btu/h·ft² → W/m²
W_CM2_TO_W_M2     = 1e4       # W/cm² → W/m²
MW_M2_TO_W_M2     = 1e6       # MW/m² → W/m²
KW_M2_TO_W_M2     = 1e3       # kW/m² → W/m²
DF_DIFF_TO_DK     = 5 / 9     # ΔT °F → ΔK  (온도 차이; 32 빼기 불필요)

# ── Standard schema ────────────────────────────────────────────────────────────
COLS = [
    "paper_id", "fluid", "channel_type", "D_h_mm",
    "G_kg_m2s", "P_kPa", "delta_T_sub_K",
    "Ra_um", "theta_deg", "surface_cat",
    "q_onb_W_m2", "delta_T_onb_K",
    "source_fig", "digitize_date", "notes",
]

DIGITIZE_DATE = "2026-05-28"


def base_row(**kw) -> dict:
    """빈 스키마 행 반환."""
    row = {
        "paper_id": "unknown", "fluid": "water",
        "channel_type": "tube_circular", "D_h_mm": -1,
        "G_kg_m2s": -1, "P_kPa": -1, "delta_T_sub_K": -1,
        "Ra_um": -1, "theta_deg": -1, "surface_cat": "unknown",
        "q_onb_W_m2": -1, "delta_T_onb_K": -1,
        "source_fig": "unknown", "digitize_date": DIGITIZE_DATE, "notes": "",
    }
    row.update(kw)
    return row


# ══════════════════════════════════════════════════════════════════════════════
# ONB 굴곡점 추출 (비등 곡선 전체 데이터 → ONB 1점)
# ══════════════════════════════════════════════════════════════════════════════

def extract_onb_inflection(
    x_raw: np.ndarray,
    y_raw: np.ndarray,
    n_fit_frac: float = 0.35,
    threshold: float = 1.20,
) -> tuple[float, float] | None:
    """
    비등 곡선에서 ONB 굴곡점 추출.

    Parameters
    ----------
    x_raw : ΔT_wall (K) — 이미 변환된 값
    y_raw : q'' (W/m²) — 이미 변환된 값
    n_fit_frac : 단상 선형 영역에 사용할 데이터 비율
    threshold  : 단상 예측 대비 실제값 초과 배율 기준

    Returns
    -------
    (x_onb, y_onb) or None
    """
    if len(x_raw) < 4:
        return None

    # x 오름차순 정렬
    idx = np.argsort(x_raw)
    x = x_raw[idx]
    y = y_raw[idx]

    # 양수 데이터만으로 log-log 선형 피팅 (단상 강제대류 영역)
    mask = (x > 0) & (y > 0)
    if mask.sum() < 3:
        return None

    n_fit = max(2, int(mask.sum() * n_fit_frac))
    xf = np.log(x[mask][:n_fit])
    yf = np.log(y[mask][:n_fit])
    coeffs = np.polyfit(xf, yf, 1)  # log(y) = a*log(x) + b

    # 굴곡점 탐색: 단상 예측보다 threshold 배 초과하는 첫 번째 점
    for xi, yi in zip(x[mask][n_fit:], y[mask][n_fit:]):
        y_pred = np.exp(np.polyval(coeffs, np.log(xi)))
        if yi >= y_pred * threshold:
            return (float(xi), float(yi))

    # 굴곡점 미발견: 비등 곡선이 측정 범위 내에 ONB를 포함하지 않음
    return None


# ══════════════════════════════════════════════════════════════════════════════
# P1 — Basu, Warrier, Dhir (2002) [basu2002]
# ══════════════════════════════════════════════════════════════════════════════

# fig9: EXCLUDED — z_ONB(cm) 데이터, q'' 정보 없음 → fig10/11로 대체

_BASU2002_SERIES = {
    "Past_theta01_FC72-NICr":      {"fluid": "FC-72",  "theta_deg": 1.0,  "surface_cat": "nicr_rod"},
    "Past_theta04_R11-Haynes":     {"fluid": "R-11",   "theta_deg": 4.0,  "surface_cat": "haynes_rod"},
    "Past_theta04_R11-SS":         {"fluid": "R-11",   "theta_deg": 4.0,  "surface_cat": "ss_rod"},
    "Past_theta05_R113-CrPt":      {"fluid": "R-113",  "theta_deg": 5.0,  "surface_cat": "crpt_rod"},
    "Past_theta05_R113-SS":        {"fluid": "R-113",  "theta_deg": 5.0,  "surface_cat": "ss_rod"},
    "Past_theta06_R12-Cu":         {"fluid": "R-12",   "theta_deg": 6.0,  "surface_cat": "copper_rod"},
    "Past_theta38_water-Ni":       {"fluid": "water",  "theta_deg": 38.0, "surface_cat": "nickel_rod"},
    "Past_theta38_water-SS":       {"fluid": "water",  "theta_deg": 38.0, "surface_cat": "ss_rod"},
    "Pres_theta30_water-Cu_flat":  {"fluid": "water",  "theta_deg": 30.0, "surface_cat": "copper_flat"},
    "Pres_theta57_water-Zr_rod":   {"fluid": "water",  "theta_deg": 57.0, "surface_cat": "zr_rod"},
    "Pres_theta80to85_water-Cu_flat": {"fluid": "water", "theta_deg": 82.5, "surface_cat": "copper_flat"},
}


def _basu2002_series_key(filename: str) -> str | None:
    """파일명에서 시리즈 키 추출."""
    stem = Path(filename).stem  # e.g. basu2002_fig10_Past_theta04_R11-Haynes_wpd
    m = re.search(r"fig1[012]_(.+?)_wpd", stem)
    return m.group(1).strip() if m else None


def process_basu2002(lit_dir: Path) -> list[dict]:
    rows: list[dict] = []
    common = {
        "paper_id": "basu2002",
        "channel_type": "tube_circular",
        "D_h_mm": 9.5,      # 3/8-inch tube ID (Basu2002 § Experimental)
        "P_kPa": 101.325,
        "G_kg_m2s": -1,     # parity plot — 조건 다수 혼합
        "delta_T_sub_K": -1,
        "Ra_um": -1,
        "digitize_date": DIGITIZE_DATE,
    }

    # 물리적으로 불가능한 시리즈 제외 (재디지타이즈 후에도 동일값 확인)
    # FC-72/NiCr: ΔT_ONB=82-84K → T_wall=138°C (FC-72 T_sat=56°C, CHF 초과 3×)
    # 인용된 타 연구 데이터 — 측정 조건 오류 또는 원 논문 이상값 추정
    _BASU_FIG10_EXCLUDE = {"Past_theta01_FC72-NICr"}

    # fig10: parity ΔT_ONB  (y_raw = 실험 ΔT_ONB, 단위 °C)
    for f in sorted(lit_dir.glob("basu2002_fig10_*_wpd.csv")):
        key = _basu2002_series_key(f.name)
        if key in _BASU_FIG10_EXCLUDE:
            print(f"  [EXCL] basu2002 fig10 {key}: 물리적으로 불가능한 ΔT — 제외")
            continue
        meta = _BASU2002_SERIES.get(key, {})
        df = pd.read_csv(f, header=None, names=["x", "y"])
        for _, r in df.iterrows():
            row = base_row(**common)
            row.update(meta)
            row["delta_T_onb_K"] = float(r["y"])   # measured ΔT_ONB (°C → K 차이값)
            row["q_onb_W_m2"]    = -1               # q'' 미제공 (parity 한 축)
            row["source_fig"]    = "fig10"
            row["notes"] = f"parity ΔT_ONB; x=predicted({r['x']:.2f}°C); series={key}"
            rows.append(row)

    # fig11: parity q''_ONB  (y_raw = 실험 q''_ONB, 단위 W/cm²)
    for f in sorted(lit_dir.glob("basu2002_fig11_*_wpd.csv")):
        key = _basu2002_series_key(f.name)
        meta = _BASU2002_SERIES.get(key, {})
        df = pd.read_csv(f, header=None, names=["x", "y"])
        for _, r in df.iterrows():
            row = base_row(**common)
            row.update(meta)
            row["q_onb_W_m2"]    = float(r["y"]) * W_CM2_TO_W_M2
            row["delta_T_onb_K"] = -1
            row["source_fig"]    = "fig11"
            row["notes"] = f"parity q''_ONB; y_raw={r['y']:.3f} W/cm²→×10000; series={key}"
            rows.append(row)

    # fig12: theta/pi vs normalized ΔT — 물리 단위 미제공 → SKIP
    #   (theta 상관관계 참고용, 학습 데이터로 사용 불가)

    return rows


# ══════════════════════════════════════════════════════════════════════════════
# P2 — Kandlikar (1991) [kandlikar1991]  — Bergles&Rohsenow 재수록
# ══════════════════════════════════════════════════════════════════════════════

_KANDLIKAR_VEL = {
    "pbSS_Tsub2p2":     {"G_kg_m2s": 0,    "delta_T_sub_K": 2.2,  "notes": "pool boiling"},
    "u1p37_Tsub103-40": {"G_kg_m2s": 1315, "delta_T_sub_K": 71.5, "notes": "u=1.37m/s; ΔT_sub=103→40°C 축방향 변화 (평균 71.5K)"},
    "u2p65_Tsub101-68": {"G_kg_m2s": 2541, "delta_T_sub_K": 84.5, "notes": "u=2.65m/s; ΔT_sub=101→68°C 평균"},
    "u4p60_Tsub109-72": {"G_kg_m2s": 4409, "delta_T_sub_K": 90.5, "notes": "u=4.60m/s; ΔT_sub=109→72°C 평균"},
}
# 비등 곡선이 측정 범위 내에 ONB를 포함하지 않는 시리즈 (ONB below x_min)
_KANDLIKAR_ONB_BELOW_RANGE = {"u4p60_Tsub109-72"}


def process_kandlikar1991(lit_dir: Path) -> list[dict]:
    """
    fig5: 비등 곡선 전체 → ONB 굴곡점 1개 추출.
    단위: x=°C(ΔT_wall), y=MW/m²  →  y × 1e6 = W/m²
    """
    rows: list[dict] = []
    common = {
        "paper_id": "kandlikar1991",
        "fluid": "water",
        "channel_type": "tube_circular",
        "D_h_mm": 12.1,    # 0.476-inch ID (Bergles&Rohsenow 1964 SS tube)
        "P_kPa": 220.0,    # 32 psia
        "Ra_um": -1,
        "theta_deg": -1,
        "surface_cat": "ss_rod",
        "digitize_date": DIGITIZE_DATE,
    }

    for f in sorted(lit_dir.glob("Kandlikar1991_fig5_*_wpd.csv")):
        stem = f.stem   # e.g. Kandlikar1991_fig5_u1p37_Tsub103-40_wpd
        m = re.search(r"fig5_(.+?)_wpd", stem)
        key = m.group(1) if m else stem
        vel_meta = _KANDLIKAR_VEL.get(key, {})

        df = pd.read_csv(f, header=None, names=["x", "y"])
        x_K   = df["x"].values.astype(float)          # °C (ΔT_wall) → K 차이값 동일
        y_Wm2 = df["y"].values.astype(float) * MW_M2_TO_W_M2

        row = base_row(**common)
        row.update(vel_meta)
        row["source_fig"] = "fig5"
        if key in _KANDLIKAR_ONB_BELOW_RANGE:
            # 측정 범위 하한이 이미 핵비등 영역 — ONB는 x_min 아래에 존재
            print(f"  [INFO] kandlikar1991 {key}: ONB below measurement range "
                  f"(x_min={x_K.min():.1f}K; high G/ΔT_sub)")
            row["q_onb_W_m2"]    = -1
            row["delta_T_onb_K"] = -1
            row["notes"] = (
                f"ONB_NOT_FOUND: ONB below x_min={x_K.min():.1f}K; "
                f"curve fully in nucleate regime; n_pts={len(df)}; "
                + vel_meta.get("notes", "")
            )
        else:
            result = extract_onb_inflection(x_K, y_Wm2)
            if result is None:
                print(f"  [INFO] kandlikar1991 {key}: ONB not in measured range "
                      f"(curve starts at ΔT={x_K.min():.1f}K, already nucleate boiling)")
                row["q_onb_W_m2"]    = -1
                row["delta_T_onb_K"] = -1
                row["notes"] = (
                    f"ONB_NOT_FOUND: boiling curve starts at ΔT={x_K.min():.1f}K "
                    f"already in nucleate regime; n_pts={len(df)}; "
                    + vel_meta.get("notes", "")
                )
            else:
                x_onb, y_onb = result
                row["q_onb_W_m2"]    = y_onb
                row["delta_T_onb_K"] = x_onb
                row["notes"] = (
                    f"ONB extracted from boiling curve (threshold=1.20); "
                    f"series={key}; n_pts={len(df)}; "
                    + vel_meta.get("notes", "")
                )
        rows.append(row)

    return rows


# ══════════════════════════════════════════════════════════════════════════════
# P3 — Bergles & Rohsenow (1964) [bergles1964]
# ══════════════════════════════════════════════════════════════════════════════

_BERGLES_VEL = {
    # fig7 — 고압 (P 미확인 → -1)
    "fig7_v10ftsec": {"G_kg_m2s": 2920, "P_kPa": -1, "delta_T_sub_K": -1,
                      "notes": "v=10ft/s=3.05m/s; high-pressure; P unknown"},
    "fig7_v20ftsec": {"G_kg_m2s": 5840, "P_kPa": -1, "delta_T_sub_K": -1,
                      "notes": "v=20ft/s=6.10m/s; high-pressure; P unknown"},
    "fig7_v30ftsec": {"G_kg_m2s": 8760, "P_kPa": -1, "delta_T_sub_K": -1,
                      "notes": "v=30ft/s=9.14m/s; high-pressure; P unknown"},
    # fig9 — P=32 psia=220 kPa
    "fig9_v4p5ftsec":  {"G_kg_m2s": 1315, "P_kPa": 220.0, "delta_T_sub_K": -1,
                        "notes": "v=4.5ft/s=1.37m/s; P=32psia=220kPa"},
    "fig9_v8p7ftsec":  {"G_kg_m2s": 2541, "P_kPa": 220.0, "delta_T_sub_K": -1,
                        "notes": "v=8.7ft/s=2.65m/s; P=32psia=220kPa"},
    "fig9_v15p1ftsec": {"G_kg_m2s": 4409, "P_kPa": 220.0, "delta_T_sub_K": -1,
                        "notes": "v=15.1ft/s=4.60m/s; P=32psia=220kPa"},
}
# ONB below measurement range (boiling curve starts already in nucleate regime)
_BERGLES_ONB_BELOW_RANGE = {"fig9_v15p1ftsec"}


def process_bergles1964(lit_dir: Path) -> list[dict]:
    """
    fig7: 고압 incipient boiling — 각 행이 하나의 ONB 측정치 (비등 곡선 아님)
    fig9: 비등 곡선 → ONB 굴곡점 1개 추출

    단위: x=°F(ΔT_wall), y=Btu/h·ft²
    → delta_T_onb_K = x × 5/9,  q_onb_W_m2 = y × 3.15459
    """
    rows: list[dict] = []
    common = {
        "paper_id": "bergles1964",
        "fluid": "water",
        "channel_type": "tube_circular",
        "D_h_mm": 12.1,
        "Ra_um": -1,
        "theta_deg": -1,
        "surface_cat": "ss_tube",
        "digitize_date": DIGITIZE_DATE,
    }

    for f in sorted(lit_dir.glob("bergles1964_fig*_wpd.csv")):
        stem = f.stem   # e.g. bergles1964_fig7_v10ftsec_wpd
        m = re.search(r"bergles1964_(fig\d+_.+?)_wpd", stem)
        key = m.group(1) if m else stem
        vel_meta = _BERGLES_VEL.get(key, {})

        df = pd.read_csv(f, header=None, names=["x", "y"])
        x_K   = df["x"].values.astype(float) * DF_DIFF_TO_DK
        y_Wm2 = df["y"].values.astype(float) * BTU_H_FT2_TO_W_M2

        fig_num = key.split("_")[0]  # "fig7" or "fig9"

        if fig_num == "fig7":
            # 각 행 = 개별 ONB 측정치
            for xi, yi in zip(x_K, y_Wm2):
                row = base_row(**common)
                row.update(vel_meta)
                row["q_onb_W_m2"]    = yi
                row["delta_T_onb_K"] = xi
                row["source_fig"] = key
                row["notes"] = vel_meta.get("notes", "") + "; direct ONB measurement"
                rows.append(row)
        else:
            # fig9: 비등 곡선 → 굴곡점 추출
            row = base_row(**common)
            row.update(vel_meta)
            row["source_fig"] = key
            if key in _BERGLES_ONB_BELOW_RANGE:
                print(f"  [INFO] bergles1964 {key}: ONB below measurement range "
                      f"(x_min={x_K.min():.1f}K; high v/ΔT_sub)")
                row["q_onb_W_m2"]    = -1
                row["delta_T_onb_K"] = -1
                row["notes"] = (
                    f"ONB_NOT_FOUND: ONB below x_min={x_K.min():.1f}K; "
                    f"curve fully in nucleate regime; n_pts={len(df)}; "
                    + vel_meta.get("notes", "")
                )
            else:
                result = extract_onb_inflection(x_K, y_Wm2)
                if result is None:
                    print(f"  [INFO] bergles1964 {key}: ONB not in measured range "
                          f"(curve starts at ΔT={x_K.min():.1f}K, already nucleate boiling)")
                    row["q_onb_W_m2"]    = -1
                    row["delta_T_onb_K"] = -1
                    row["notes"] = (
                        f"ONB_NOT_FOUND: boiling curve starts at ΔT={x_K.min():.1f}K "
                        f"already in nucleate regime; n_pts={len(df)}; "
                        + vel_meta.get("notes", "")
                    )
                else:
                    x_onb, y_onb = result
                    row["q_onb_W_m2"]    = y_onb
                    row["delta_T_onb_K"] = x_onb
                    row["notes"] = (
                        f"ONB from boiling curve (threshold=1.20); n_pts={len(df)}; "
                        + vel_meta.get("notes", "")
                    )
            rows.append(row)

    return rows


# ══════════════════════════════════════════════════════════════════════════════
# P4 — Forrest et al. (2016) [forrest2016]
# ══════════════════════════════════════════════════════════════════════════════

def _forrest_surface(fname: str) -> str:
    if "Oxi" in fname:
        return "ss_oxidized"
    if "Norm" in fname:
        return "ss_clean"
    return "unknown"


def _forrest_dtsub(fname: str) -> float:
    m = re.search(r"Tsub(\d+)", fname)
    return float(m.group(1)) if m else -1


def process_forrest2016(lit_dir: Path) -> list[dict]:
    """
    fig4:  비등 곡선 → ONB 굴곡점 추출
           x=ΔT_sat(°C), y=q''(kW/m²) → y × 1000 = W/m²
    fig7/8/10: 직접 ONB 측정 — x=G(kg/m²s), y=q''_ONB(kW/m²)
    fig17: x=ΔT_sat(°C), y=q''_ONB(kW/m²)
    fig18/19: parity — y=q''_ONB,exp(kW/m²)
    """
    rows: list[dict] = []
    common = {
        "paper_id": "forrest2016",
        "fluid": "water",
        "channel_type": "narrow_channel",
        "D_h_mm": 3.92,     # 2×gap = 2×1.96 mm
        "P_kPa": -1,        # MTR 조건, 논문에서 확인 필요
        "Ra_um": -1,
        "theta_deg": -1,
        "digitize_date": DIGITIZE_DATE,
    }

    # ── fig4: 비등 곡선 (G=750, T_in=80°C)
    for f in sorted(lit_dir.glob("Forrest2016_fig04_*_wpd.csv")):
        df = pd.read_csv(f, header=None, names=["x", "y"])
        x_K   = df["x"].values.astype(float)            # ΔT_sat (°C → K 차이값)
        y_Wm2 = df["y"].values.astype(float) * KW_M2_TO_W_M2

        result = extract_onb_inflection(x_K, y_Wm2)
        if result is None:
            print(f"  [WARN] forrest2016 {f.name}: ONB 굴곡점 미발견")
            continue
        x_onb, y_onb = result
        row = base_row(**common)
        row["G_kg_m2s"]      = 750
        row["delta_T_sub_K"] = -1    # T_in=80°C; ΔT_sub 위치 의존
        row["surface_cat"]   = "ss_clean"
        row["q_onb_W_m2"]    = y_onb
        row["delta_T_onb_K"] = x_onb
        row["source_fig"]    = "fig4"
        row["notes"] = (
            f"ONB from boiling curve; G=750 kg/m²s; T_in=80°C; "
            f"TC={f.stem.split('_')[-2]}; n_pts={len(df)}"
        )
        rows.append(row)

    # ── fig7/8/10: 직접 ONB 데이터 — x=G, y=q''_ONB (kW/m²)
    for fig_pat, note_pfx in [("fig07", "fig7"), ("fig08", "fig8"), ("fig10", "fig10")]:
        for f in sorted(lit_dir.glob(f"Forrest2016_{fig_pat}_*_wpd.csv")):
            df = pd.read_csv(f, header=None, names=["x", "y"])
            surface = _forrest_surface(f.name)
            dtsub   = _forrest_dtsub(f.name)
            for _, r in df.iterrows():
                row = base_row(**common)
                row["G_kg_m2s"]      = float(r["x"])
                row["delta_T_sub_K"] = dtsub
                row["surface_cat"]   = surface
                row["q_onb_W_m2"]    = float(r["y"]) * KW_M2_TO_W_M2
                row["delta_T_onb_K"] = -1
                row["source_fig"]    = note_pfx
                row["notes"] = f"direct ONB; G from x-axis; {f.stem}"
                rows.append(row)

    # ── fig17: x=ΔT_sat(°C), y=q''_ONB(kW/m²)
    for f in sorted(lit_dir.glob("Forrest2016_fig17_*_wpd.csv")):
        df = pd.read_csv(f, header=None, names=["x", "y"])
        surface = _forrest_surface(f.name)
        for _, r in df.iterrows():
            row = base_row(**common)
            row["surface_cat"]   = surface
            row["delta_T_onb_K"] = float(r["x"])
            row["q_onb_W_m2"]    = float(r["y"]) * KW_M2_TO_W_M2
            row["source_fig"]    = "fig17"
            row["notes"] = f"{f.stem}"
            rows.append(row)

    # ── fig18/19: parity — y=q''_ONB,exp(kW/m²)
    for fig_pat, fig_lbl in [("fig18", "fig18"), ("fig19", "fig19")]:
        for f in sorted(lit_dir.glob(f"Forrest2016_{fig_pat}_*_wpd.csv")):
            df = pd.read_csv(f, header=None, names=["x", "y"])
            surface = _forrest_surface(f.name)
            for _, r in df.iterrows():
                row = base_row(**common)
                row["surface_cat"]   = surface
                row["q_onb_W_m2"]    = float(r["y"]) * KW_M2_TO_W_M2
                row["delta_T_onb_K"] = -1
                row["source_fig"]    = fig_lbl
                row["notes"] = (
                    f"parity q''_ONB; x=predicted({r['x']:.1f} kW/m²); {f.stem}"
                )
                rows.append(row)

    return rows


# ══════════════════════════════════════════════════════════════════════════════
# P6 — Liu, Lee, Garimella (2005) [liu2005]
# ══════════════════════════════════════════════════════════════════════════════

# 공통 실험 조건 (Liu2005 Table 1 / paper 본문)
_LIU_COMMON = {
    "paper_id": "liu2005",
    "fluid": "water_DIW",
    "channel_type": "microchannel",
    "D_h_mm": 0.318,    # 318 μm 수력직경 (Case 10 기준 대표값)
    "G_kg_m2s": -1,     # 조건별 상이 → 파일별 처리
    "P_kPa": -1,        # 출구압력 1.0~1.5 bar → 파일별 처리
    "delta_T_sub_K": -1,
    "Ra_um": -1,
    "theta_deg": -1,
    "surface_cat": "silicon_DIW",
    "digitize_date": DIGITIZE_DATE,
}


def process_liu2005(lit_dir: Path) -> list[dict]:
    """
    fig4a/4b: parity q''_ONB — y_raw = 실험 q''_ONB (W/cm²) → × 10000
    fig9a-e : 매개변수 효과 — y_raw = q''_ONB (W/cm²) → × 10000
              x_raw = 조건값 (velocity/Tin/Pout/width/height)
    """
    rows: list[dict] = []

    # ── fig4a: 전체 parity
    f4a = lit_dir / "liu2005_fig4a_wpd.csv"
    if f4a.exists():
        df = pd.read_csv(f4a, header=None, names=["x", "y"])
        for _, r in df.iterrows():
            row = base_row(**_LIU_COMMON)
            row["q_onb_W_m2"]    = float(r["y"]) * W_CM2_TO_W_M2
            row["delta_T_onb_K"] = -1
            row["source_fig"]    = "fig4a"
            row["notes"] = f"parity q''_ONB all cases; x_pred={r['x']:.2f} W/cm²"
            rows.append(row)

    # ── fig4b: Tin별 parity (Tin=30/60/90°C)
    for tin in [30, 60, 90]:
        f = lit_dir / f"liu2005_fig4b_Tin{tin}_wpd.csv"
        if not f.exists():
            continue
        df = pd.read_csv(f, header=None, names=["x", "y"])
        # T_sat at ~1 bar ≈ 100°C → delta_T_sub = T_sat - T_in = 100 - Tin
        dtsub = 100.0 - tin
        for _, r in df.iterrows():
            row = base_row(**_LIU_COMMON)
            row["delta_T_sub_K"] = dtsub
            row["q_onb_W_m2"]    = float(r["y"]) * W_CM2_TO_W_M2
            row["delta_T_onb_K"] = -1
            row["source_fig"]    = f"fig4b_Tin{tin}"
            row["notes"] = f"parity q''_ONB; T_in={tin}°C; ΔT_sub≈{dtsub}K; x_pred={r['x']:.2f} W/cm²"
            rows.append(row)

    # ── fig9a: 유속 효과 — x=velocity(m/s), y=q''_ONB(W/cm²)
    f9a = lit_dir / "liu2005_fig9a_flowvel_wpd.csv"
    if f9a.exists():
        df = pd.read_csv(f9a, header=None, names=["x", "y"])
        for _, r in df.iterrows():
            row = base_row(**_LIU_COMMON)
            row["G_kg_m2s"]   = float(r["x"]) * 997.0  # ρ_water ≈ 997 kg/m³
            row["q_onb_W_m2"] = float(r["y"]) * W_CM2_TO_W_M2
            row["source_fig"] = "fig9a"
            row["notes"] = f"flow velocity effect; u={r['x']:.3f} m/s"
            rows.append(row)

    # ── fig9b: 입구온도 효과 — x=T_in(°C), y=q''_ONB(W/cm²)
    f9b = lit_dir / "liu2005_fig9b_Tin_wpd.csv"
    if f9b.exists():
        df = pd.read_csv(f9b, header=None, names=["x", "y"])
        for _, r in df.iterrows():
            dtsub = max(0.0, 100.0 - float(r["x"]))  # T_sat≈100°C at ~1 bar
            row = base_row(**_LIU_COMMON)
            row["delta_T_sub_K"] = dtsub
            row["q_onb_W_m2"]    = float(r["y"]) * W_CM2_TO_W_M2
            row["source_fig"]    = "fig9b"
            row["notes"] = f"inlet temp effect; T_in={r['x']:.1f}°C; ΔT_sub≈{dtsub:.1f}K"
            rows.append(row)

    # ── fig9c: 출구압력 효과 — x=P_out(bar), y=q''_ONB(W/cm²)
    f9c = lit_dir / "liu2005_fig9c_Pout_wpd.csv"
    if f9c.exists():
        df = pd.read_csv(f9c, header=None, names=["x", "y"])
        for _, r in df.iterrows():
            row = base_row(**_LIU_COMMON)
            row["P_kPa"]      = float(r["x"]) * 100.0  # bar → kPa
            row["q_onb_W_m2"] = float(r["y"]) * W_CM2_TO_W_M2
            row["source_fig"] = "fig9c"
            row["notes"] = f"outlet pressure effect; P_out={r['x']:.3f} bar"
            rows.append(row)

    # ── fig9d: 채널폭 효과 — x=w_c(μm), y=q''_ONB(W/cm²)
    f9d = lit_dir / "liu2005_fig9d_wc_wpd.csv"
    if f9d.exists():
        df = pd.read_csv(f9d, header=None, names=["x", "y"])
        for _, r in df.iterrows():
            wc_mm = float(r["x"]) * 1e-3   # μm → mm
            row = base_row(**_LIU_COMMON)
            row["D_h_mm"]     = wc_mm      # 채널폭 변화 → D_h 근사
            row["q_onb_W_m2"] = float(r["y"]) * W_CM2_TO_W_M2
            row["source_fig"] = "fig9d"
            row["notes"] = f"channel width effect; w_c={r['x']:.0f}μm; D_h≈w_c(mm)"
            rows.append(row)

    # ── fig9e: 채널높이 효과 — x=H_c(μm), y=q''_ONB(W/cm²)
    f9e = lit_dir / "liu2005_fig9e_Hc_wpd.csv"
    if f9e.exists():
        df = pd.read_csv(f9e, header=None, names=["x", "y"])
        for _, r in df.iterrows():
            row = base_row(**_LIU_COMMON)
            row["q_onb_W_m2"] = float(r["y"]) * W_CM2_TO_W_M2
            row["source_fig"] = "fig9e"
            row["notes"] = f"channel height effect; H_c={r['x']:.0f}μm"
            rows.append(row)

    return rows


# ══════════════════════════════════════════════════════════════════════════════
# 물리적 타당성 검증
# ══════════════════════════════════════════════════════════════════════════════

_DT_LIMITS = {
    "water":      (0.5, 40.0),
    "water_DIW":  (0.5, 40.0),
    "R-11":       (0.3, 40.0),   # 고과냉도 유동비등 시 최대 40K (Basu2002 36K 관측)
    "R-12":       (0.3, 40.0),
    "R-113":      (0.3, 40.0),
    "FC-72":      (0.3, 30.0),
}
_Q_LIMITS_W_M2 = (1e3, 2e7)   # 1 kW/m² ~ 20 MW/m²


def validate(df: pd.DataFrame) -> pd.DataFrame:
    """이상값 플래그 추가 (삭제 안 함)."""
    df = df.copy()

    # ΔT 범위 체크
    def flag_dt(row: pd.Series) -> str:
        note = str(row["notes"])
        if row["delta_T_onb_K"] <= 0:
            return note
        lo, hi = _DT_LIMITS.get(row["fluid"], (0.3, 50.0))
        if row["delta_T_onb_K"] < lo:
            note += f" [FLAG: delta_T_onb={row['delta_T_onb_K']:.2f}K < {lo}]"
        elif row["delta_T_onb_K"] > hi:
            note += f" [FLAG: delta_T_onb={row['delta_T_onb_K']:.2f}K > {hi}]"
        return note

    # q'' 범위 체크
    def flag_q(row: pd.Series) -> str:
        note = str(row["notes"])
        if row["q_onb_W_m2"] <= 0:
            return note
        qlo, qhi = _Q_LIMITS_W_M2
        if row["q_onb_W_m2"] < qlo:
            note += f" [FLAG: q_onb={row['q_onb_W_m2']:.0f} W/m² < {qlo:.0f}]"
        elif row["q_onb_W_m2"] > qhi:
            note += f" [FLAG: q_onb={row['q_onb_W_m2']:.0f} W/m² > {qhi:.0f}]"
        return note

    df["notes"] = df.apply(flag_dt, axis=1)
    df["notes"] = df.apply(flag_q, axis=1)
    return df


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    print("Phase 2 Literature Preprocessing")
    print(f"  입력 디렉토리: {LIT_DIR}")
    print(f"  출력 파일:     {OUT_FILE}\n")

    all_rows: list[dict] = []

    processors = [
        ("basu2002",      process_basu2002),
        ("kandlikar1991", process_kandlikar1991),
        ("bergles1964",   process_bergles1964),
        ("forrest2016",   process_forrest2016),
        ("liu2005",       process_liu2005),
    ]

    for name, fn in processors:
        rows = fn(LIT_DIR)
        all_rows.extend(rows)
        print(f"  {name:15s}: {len(rows):4d} 행")

    df = pd.DataFrame(all_rows, columns=COLS)

    # 물리 검증 플래그
    df = validate(df)

    # 저장
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_FILE, index=False)

    # 요약 출력
    print(f"\n총 {len(df)} 행 → {OUT_FILE.name}")
    print("\n논문별 행 수:")
    print(df.groupby("paper_id").size().to_string())
    print("\nq_onb 보유 행:", (df["q_onb_W_m2"] > 0).sum())
    print("delta_T_onb 보유 행:", (df["delta_T_onb_K"] > 0).sum())
    print("양쪽 모두 보유:", ((df["q_onb_W_m2"] > 0) & (df["delta_T_onb_K"] > 0)).sum())

    flag_rows = df["notes"].str.contains(r"\[FLAG", na=False).sum()
    if flag_rows:
        print(f"\n⚠️  FLAG 행 수: {flag_rows} — 검토 필요")
        print(df[df["notes"].str.contains(r"\[FLAG", na=False)][
            ["paper_id", "fluid", "q_onb_W_m2", "delta_T_onb_K", "notes"]
        ].to_string())


if __name__ == "__main__":
    main()
