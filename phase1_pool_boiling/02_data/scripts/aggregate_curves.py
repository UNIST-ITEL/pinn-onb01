"""
모든 표준화 CSV에서 전체 boiling curve 포인트를 모아 통합 데이터셋 생성.

출력:
  02_data/processed/boiling_curves.csv   — 전체 (q, ΔT) 포인트 (~1,145 행)
                                            ONB_flag 컬럼 보존

aggregate_onb.py와의 차이: ONB_flag 필터 없음. 모든 행 수집.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LIT_ROOT = PROJECT_ROOT / "02_data" / "raw" / "literature"
PROCESSED = PROJECT_ROOT / "02_data" / "processed"
PROCESSED.mkdir(parents=True, exist_ok=True)

# Re-import SFC_META from aggregate_onb (single source of truth)
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from aggregate_onb import SFC_META  # noqa: E402

# Hsu inverse for r_c weak labels
sys.path.insert(0, str(PROJECT_ROOT / "03_model"))
from src.utils.properties import (  # noqa: E402
    saturation_properties,
    hsu_criterion_cavity_radius,
    UnsupportedFluidError,
)


def hsu_r_c_geomean_um(fluid: str, delta_T_wall: float, q_flux: float,
                       P: float = 101_325.0) -> float | None:
    """Compute Hsu-derived geometric mean cavity radius [μm] for one ONB obs.

    Returns None if fluid unsupported or solution invalid.
    """
    try:
        props = saturation_properties(fluid, P=P)
        r_min, r_max = hsu_criterion_cavity_radius(props, delta_T_wall, q_flux)
        if r_min is None or r_max is None or r_min <= 0 or r_max <= 0:
            return None
        return math.sqrt(r_min * r_max) * 1e6  # m → μm
    except (UnsupportedFluidError, ValueError, ZeroDivisionError):
        return None


def collect_all_rows() -> list[dict]:
    """모든 figure_*.csv의 모든 행 수집. ONB_flag 포함."""
    rows: list[dict] = []
    for paper_dir in sorted(LIT_ROOT.glob("*/")):
        if not paper_dir.name[0].isupper():
            continue
        for csv_path in sorted(paper_dir.glob("figure_*.csv")):
            if ".meta." in csv_path.name:
                continue
            with csv_path.open() as f:
                reader = csv.DictReader(f)
                for r in reader:
                    sid = r["surface_id"]
                    if sid not in SFC_META:
                        continue
                    try:
                        q_flux = float(r["q_flux"])
                        delta_T_wall = float(r["delta_T_wall"])
                    except (ValueError, KeyError):
                        continue
                    if q_flux <= 0 or delta_T_wall <= 0:
                        continue
                    # ONB regime filter: drop post-CHF / film-boiling outliers.
                    if delta_T_wall > 30.0 or q_flux > 1.5e6:
                        continue
                    meta = SFC_META[sid]
                    onb_flag_str = str(r.get("ONB_flag", "")).strip()
                    rows.append({
                        "source_paper": r["source_paper"],
                        "figure_ref": r["figure_ref"],
                        "surface_id": sid,
                        "surface_label": meta["label"],
                        "fluid": r["fluid"],
                        "delta_T_wall": delta_T_wall,
                        "delta_T_sub": float(r.get("delta_T_sub", 0.0) or 0.0),
                        "q_flux": q_flux,
                        "Ra_um": meta["Ra_um"],
                        "theta_deg": meta["theta_deg"],
                        "category": meta["category"],
                        "ONB_flag": onb_flag_str == "True",
                        "notes": r.get("notes", ""),
                    })

    # ---- Surface-level weak label: r_c from Hsu inverse on ONB-labeled rows ----
    # Compute per-surface r_c_geomean (μm) from ONB observations and apply to all
    # rows of that surface. Surfaces with no valid ONB → r_c_um = None.
    from collections import defaultdict
    per_surface_r_c: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        if not row["ONB_flag"]:
            continue
        r_c = hsu_r_c_geomean_um(row["fluid"], row["delta_T_wall"], row["q_flux"])
        if r_c is not None and 1e-3 < r_c < 1e3:   # physical sanity band
            per_surface_r_c[row["surface_id"]].append(r_c)
    surface_r_c_mean: dict[str, float | None] = {
        sid: (sum(vs) / len(vs)) if vs else None
        for sid, vs in per_surface_r_c.items()
    }
    for row in rows:
        row["r_c_um"] = surface_r_c_mean.get(row["surface_id"])

    return rows


def write_dataset(rows: list[dict], out: Path) -> None:
    fields = [
        "source_paper", "figure_ref", "surface_id", "surface_label",
        "fluid", "delta_T_wall", "delta_T_sub", "q_flux",
        "Ra_um", "theta_deg", "category", "ONB_flag", "r_c_um", "notes",
    ]
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main() -> None:
    rows = collect_all_rows()
    print(f"[aggregate_curves] collected {len(rows)} boiling-curve points")

    out_csv = PROCESSED / "boiling_curves.csv"
    write_dataset(rows, out_csv)
    print(f"[ok] dataset → {out_csv}")

    # 통계 요약
    n_onb = sum(1 for r in rows if r["ONB_flag"])
    n_curve = len(rows) - n_onb
    n_surfaces = len(set(r["surface_id"] for r in rows))
    fluids = sorted(set(r["fluid"] for r in rows))
    papers = sorted(set(r["source_paper"] for r in rows))

    print()
    print("=== summary ===")
    print(f"  total points:     {len(rows)}")
    print(f"  ONB-labeled:      {n_onb}")
    print(f"  pre/post-ONB:     {n_curve}")
    print(f"  unique surfaces:  {n_surfaces}")
    print(f"  fluids:           {fluids}")
    print(f"  papers:           {papers}")
    print(f"  ΔT range:         {min(r['delta_T_wall'] for r in rows):.2f}–{max(r['delta_T_wall'] for r in rows):.2f} K")
    print(f"  q range:          {min(r['q_flux'] for r in rows)/1000:.2f}–{max(r['q_flux'] for r in rows)/1000:.1f} kW/m²")
    # By paper breakdown
    print()
    print("  by paper:")
    for p in papers:
        sub = [r for r in rows if r["source_paper"] == p]
        n_p = len(sub)
        n_p_onb = sum(1 for r in sub if r["ONB_flag"])
        print(f"    {p}: {n_p} pts ({n_p_onb} ONB)")


if __name__ == "__main__":
    main()
