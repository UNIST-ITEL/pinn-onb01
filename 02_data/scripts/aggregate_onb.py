"""
모든 표준화 CSV에서 ONB_flag=True 행을 모아 통합 ONB 데이터셋 + 시각화 생성.

출력:
  02_data/processed/onb_dataset.csv     — 모든 ONB 포인트 통합 (38행)
  04_analysis/figures/onb_overview.png  — 4-panel 시각화
"""

from __future__ import annotations

import csv
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LIT_ROOT = PROJECT_ROOT / "02_data" / "raw" / "literature"
PROCESSED = PROJECT_ROOT / "02_data" / "processed"
FIG_DIR = PROJECT_ROOT / "04_analysis" / "figures"
PROCESSED.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)


# 표면 메타데이터 (Ra in μm, theta in deg, fluid)
SFC_META: dict[str, dict] = {
    "SFC-001": {"label": "BETZ_Hydrophilic", "Ra_um": 0.001, "theta_deg": 20.0, "category": "betz"},
    "SFC-002": {"label": "BETZ_Hydrophobic", "Ra_um": 0.001, "theta_deg": 115.0, "category": "betz"},
    "SFC-003": {"label": "BETZ_SHPi", "Ra_um": 0.001, "theta_deg": 0.0, "category": "betz"},
    "SFC-004": {"label": "BETZ_SHPo", "Ra_um": 0.001, "theta_deg": 158.0, "category": "betz"},
    "SFC-005": {"label": "BETZ_Biphilic", "Ra_um": 0.001, "theta_deg": 70.0, "category": "betz"},   # mixed → effective
    "SFC-006": {"label": "BETZ_SBPi_circle", "Ra_um": 0.001, "theta_deg": 75.0, "category": "betz"},
    "SFC-007": {"label": "BETZ_SBPi_hex", "Ra_um": 0.001, "theta_deg": 75.0, "category": "betz"},
    "SFC-008": {"label": "JO_Hydrophilic", "Ra_um": 0.00175, "theta_deg": 54.0, "category": "jo"},
    "SFC-009": {"label": "JO_Hydrophobic", "Ra_um": 0.00175, "theta_deg": 123.0, "category": "jo"},
    "SFC-010": {"label": "PHAN_SiOx", "Ra_um": 0.030, "theta_deg": 22.0, "category": "phan"},
    "SFC-011": {"label": "PHAN_TiO2", "Ra_um": 0.030, "theta_deg": 31.0, "category": "phan"},
    "SFC-012": {"label": "PHAN_Pt", "Ra_um": 0.030, "theta_deg": 67.0, "category": "phan"},
    "SFC-013": {"label": "PHAN_Fe2O3", "Ra_um": 0.030, "theta_deg": 80.0, "category": "phan"},
    "SFC-014": {"label": "PHAN_ref", "Ra_um": 0.030, "theta_deg": 85.0, "category": "phan"},
    "SFC-015": {"label": "JONES_Polished_w", "Ra_um": 0.038, "theta_deg": None, "category": "jones_w"},
    "SFC-016": {"label": "JONES_Polished_F", "Ra_um": 0.027, "theta_deg": None, "category": "jones_F"},
    "SFC-017": {"label": "JONES_EDM1p08", "Ra_um": 1.08, "theta_deg": None, "category": "jones"},
    "SFC-018": {"label": "JONES_EDM2p22", "Ra_um": 2.22, "theta_deg": None, "category": "jones"},
    "SFC-019": {"label": "JONES_EDM5p89", "Ra_um": 5.89, "theta_deg": None, "category": "jones"},
    "SFC-020": {"label": "JONES_EDM10p0", "Ra_um": 10.0, "theta_deg": None, "category": "jones"},
    "SFC-021": {"label": "BOURDON12_S1", "Ra_um": 0.0097, "theta_deg": 0.0, "category": "bourdon12"},
    "SFC-022": {"label": "BOURDON12_S2", "Ra_um": 0.0086, "theta_deg": 0.0, "category": "bourdon12"},
    "SFC-023": {"label": "BOURDON12_S3", "Ra_um": 0.0076, "theta_deg": 0.0, "category": "bourdon12"},
    "SFC-024": {"label": "BOURDON12_S1_grafted", "Ra_um": 0.0097, "theta_deg": 108.0, "category": "bourdon12"},
    "SFC-025": {"label": "BOURDON12_S1_grafted_C", "Ra_um": 0.0097, "theta_deg": 108.0, "category": "bourdon12"},
    "SFC-026": {"label": "BOURDON15_NotGrafted", "Ra_um": 0.00043, "theta_deg": 11.1, "category": "bourdon15"},
    "SFC-027": {"label": "BOURDON15_MPEGPTMS", "Ra_um": 0.00043, "theta_deg": 33.5, "category": "bourdon15"},
    "SFC-028": {"label": "BOURDON15_AcOUTES", "Ra_um": 0.00043, "theta_deg": 70.8, "category": "bourdon15"},
    "SFC-029": {"label": "BOURDON15_OTS", "Ra_um": 0.00043, "theta_deg": 101.6, "category": "bourdon15"},
    # JABARDO_2009 Cu surfaces (다양한 표면처리)
    "SFC-031": {"label": "JABARDO_Cu_Ra0p07P", "Ra_um": 0.07, "theta_deg": None, "category": "jabardo"},
    "SFC-032": {"label": "JABARDO_Cu_Ra0p16SP", "Ra_um": 0.16, "theta_deg": None, "category": "jabardo"},
    "SFC-033": {"label": "JABARDO_Cu_Ra0p47SP", "Ra_um": 0.47, "theta_deg": None, "category": "jabardo"},
    "SFC-034": {"label": "JABARDO_Cu_Ra0p5SP", "Ra_um": 0.50, "theta_deg": None, "category": "jabardo"},
    "SFC-035": {"label": "JABARDO_Cu_Ra2p5SPI", "Ra_um": 2.5, "theta_deg": None, "category": "jabardo"},
    "SFC-036": {"label": "JABARDO_Cu_Ra3p3SPI", "Ra_um": 3.3, "theta_deg": None, "category": "jabardo"},
    "SFC-037": {"label": "JABARDO_Cu_Ra4p6SPI", "Ra_um": 4.6, "theta_deg": None, "category": "jabardo"},
    "SFC-038": {"label": "JABARDO_Cu_Ra10p5SPI", "Ra_um": 10.5, "theta_deg": None, "category": "jabardo"},
    # JABARDO_2009 Fig.10 — Brass surfaces (R-134a, 2 pressures × 5 Ra)
    "SFC-039": {"label": "JABARDO_Br_Ra0p08P",   "Ra_um": 0.08, "theta_deg": None, "category": "jabardo_br"},
    "SFC-040": {"label": "JABARDO_Br_Ra0p90SP",  "Ra_um": 0.90, "theta_deg": None, "category": "jabardo_br"},
    "SFC-041": {"label": "JABARDO_Br_Ra1p2SPI",  "Ra_um": 1.20, "theta_deg": None, "category": "jabardo_br"},
    "SFC-042": {"label": "JABARDO_Br_Ra1p8SPI",  "Ra_um": 1.80, "theta_deg": None, "category": "jabardo_br"},
    "SFC-043": {"label": "JABARDO_Br_Ra3p5SPI",  "Ra_um": 3.50, "theta_deg": None, "category": "jabardo_br"},
    # JABARDO_2009 Fig.10 — Stainless Steel surfaces (R-134a, 2 pressures × 7 Ra)
    "SFC-044": {"label": "JABARDO_SS_Ra0p03P",   "Ra_um": 0.03, "theta_deg": None, "category": "jabardo_ss"},
    "SFC-045": {"label": "JABARDO_SS_Ra0p07SP",  "Ra_um": 0.07, "theta_deg": None, "category": "jabardo_ss"},
    "SFC-046": {"label": "JABARDO_SS_Ra0p45SP",  "Ra_um": 0.45, "theta_deg": None, "category": "jabardo_ss"},
    "SFC-047": {"label": "JABARDO_SS_Ra0p90SPI", "Ra_um": 0.90, "theta_deg": None, "category": "jabardo_ss"},
    "SFC-048": {"label": "JABARDO_SS_Ra1p45SPI", "Ra_um": 1.45, "theta_deg": None, "category": "jabardo_ss"},
    "SFC-049": {"label": "JABARDO_SS_Ra2p50SPI", "Ra_um": 2.50, "theta_deg": None, "category": "jabardo_ss"},
    "SFC-050": {"label": "JABARDO_SS_Ra3p20SPI", "Ra_um": 3.20, "theta_deg": None, "category": "jabardo_ss"},
}


def collect_onb_rows() -> list[dict]:
    """모든 figure_*.csv에서 ONB_flag=True 행 수집."""
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
                    if r["ONB_flag"] == "True":
                        # surface_id가 SFC-XXX이고 SFC_META에 있는 경우만
                        sid = r["surface_id"]
                        if sid not in SFC_META:
                            continue
                        meta = SFC_META[sid]
                        rows.append({
                            "source_paper": r["source_paper"],
                            "figure_ref": r["figure_ref"],
                            "surface_id": sid,
                            "surface_label": meta["label"],
                            "fluid": r["fluid"],
                            "delta_T_wall": float(r["delta_T_wall"]),
                            "delta_T_sub": float(r["delta_T_sub"]),
                            "q_flux": float(r["q_flux"]),
                            "Ra_um": meta["Ra_um"],
                            "theta_deg": meta["theta_deg"],
                            "category": meta["category"],
                            "notes": r["notes"],
                        })
    return rows


def write_dataset(rows: list[dict], out: Path) -> None:
    fields = [
        "source_paper", "figure_ref", "surface_id", "surface_label",
        "fluid", "delta_T_wall", "delta_T_sub", "q_flux",
        "Ra_um", "theta_deg", "category", "notes",
    ]
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def make_overview_figure(rows: list[dict], out: Path) -> None:
    """4-panel overview: (a) ΔT vs θ, (b) ΔT vs Ra, (c) ΔT vs q (boiling curve), (d) source별 분포."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # 색상: 논문별
    paper_colors = {
        "BETZ_2013": "#1f77b4",
        "JO_2011": "#ff7f0e",
        "PHAN_2009": "#2ca02c",
        "JONES_2009": "#d62728",
        "BOURDON_2012": "#9467bd",
        "BOURDON_2015": "#8c564b",
        "JABARDO_2009": "#e377c2",
    }
    fluid_marker = {"water": "o", "FC-77": "s", "R-123": "^", "R-134a": "D"}

    # (a) ΔT vs θ
    ax = axes[0, 0]
    for r in rows:
        if r["theta_deg"] is None:
            continue
        c = paper_colors.get(r["source_paper"], "gray")
        m = fluid_marker.get(r["fluid"], "o")
        ax.scatter(r["theta_deg"], r["delta_T_wall"], c=c, marker=m, s=70, alpha=0.85, edgecolors="black", linewidths=0.6)
    ax.set_xlabel("Static contact angle θ [°]", fontsize=11)
    ax.set_ylabel(r"$\Delta T_{ONB}$ [K]", fontsize=11)
    ax.set_title("(a) ONB superheat vs. contact angle", fontsize=12)
    ax.grid(alpha=0.3)
    ax.set_xlim(-5, 175)
    ax.set_ylim(0, 22)

    # (b) ΔT vs Ra (log scale)
    ax = axes[0, 1]
    for r in rows:
        if r["Ra_um"] is None or r["Ra_um"] <= 0:
            continue
        c = paper_colors.get(r["source_paper"], "gray")
        m = fluid_marker.get(r["fluid"], "o")
        ax.scatter(r["Ra_um"], r["delta_T_wall"], c=c, marker=m, s=70, alpha=0.85, edgecolors="black", linewidths=0.6)
    ax.set_xscale("log")
    ax.set_xlabel(r"Surface roughness $R_a$ [μm]", fontsize=11)
    ax.set_ylabel(r"$\Delta T_{ONB}$ [K]", fontsize=11)
    ax.set_title("(b) ONB superheat vs. roughness (log scale)", fontsize=12)
    ax.grid(alpha=0.3, which="both")
    ax.set_ylim(0, 22)

    # (c) ΔT vs q'' (ONB points only)
    ax = axes[1, 0]
    for r in rows:
        if r["q_flux"] <= 0:
            continue
        c = paper_colors.get(r["source_paper"], "gray")
        m = fluid_marker.get(r["fluid"], "o")
        ax.scatter(r["delta_T_wall"], r["q_flux"] / 1000.0, c=c, marker=m, s=70, alpha=0.85, edgecolors="black", linewidths=0.6)
    ax.set_xlabel(r"$\Delta T_{ONB}$ [K]", fontsize=11)
    ax.set_ylabel(r"$q''_{ONB}$ [kW/m²]", fontsize=11)
    ax.set_title("(c) ONB heat flux vs. superheat", fontsize=12)
    ax.grid(alpha=0.3)
    ax.set_xlim(0, 22)

    # (d) 논문별 ONB 개수 + ΔT 범위 (box plot)
    ax = axes[1, 1]
    by_paper: dict[str, list[float]] = {}
    for r in rows:
        by_paper.setdefault(r["source_paper"], []).append(r["delta_T_wall"])
    paper_order = sorted(by_paper.keys())
    data = [by_paper[p] for p in paper_order]
    labels = [f"{p}\n(n={len(by_paper[p])})" for p in paper_order]
    bp = ax.boxplot(data, labels=labels, patch_artist=True)
    for patch, p in zip(bp["boxes"], paper_order):
        patch.set_facecolor(paper_colors.get(p, "gray"))
        patch.set_alpha(0.6)
    ax.set_ylabel(r"$\Delta T_{ONB}$ [K]", fontsize=11)
    ax.set_title("(d) ΔT_ONB distribution by source paper", fontsize=12)
    ax.tick_params(axis="x", labelrotation=25, labelsize=9)
    ax.grid(alpha=0.3, axis="y")

    # 범례 (figure 단위)
    handles = [plt.Line2D([], [], marker="o", linestyle="", color=c, label=p, markersize=9, markeredgecolor="black", markeredgewidth=0.5)
               for p, c in paper_colors.items()]
    handles += [plt.Line2D([], [], marker=m, linestyle="", color="gray", label=f"fluid={fl}", markersize=9, markeredgecolor="black", markeredgewidth=0.5)
                for fl, m in fluid_marker.items()]
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, 0.02), ncol=4, fontsize=9, frameon=False)

    fig.suptitle("Phase 1 ONB Database Overview — 38 points × 6 papers × 30 surfaces", fontsize=13, y=0.99)
    fig.tight_layout(rect=[0, 0.05, 1, 0.97])
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    rows = collect_onb_rows()
    print(f"[aggregate] collected {len(rows)} ONB points")

    out_csv = PROCESSED / "onb_dataset.csv"
    write_dataset(rows, out_csv)
    print(f"[ok] dataset → {out_csv}")

    out_png = FIG_DIR / "onb_overview.png"
    make_overview_figure(rows, out_png)
    print(f"[ok] figure  → {out_png}")

    # 통계 요약
    print()
    print("=== summary ===")
    print(f"  total ONB points: {len(rows)}")
    print(f"  unique surfaces:  {len(set(r['surface_id'] for r in rows))}")
    print(f"  unique fluids:    {sorted(set(r['fluid'] for r in rows))}")
    print(f"  ΔT range:         {min(r['delta_T_wall'] for r in rows):.2f} – {max(r['delta_T_wall'] for r in rows):.2f} K")
    print(f"  q range:          {min(r['q_flux'] for r in rows)/1000:.1f} – {max(r['q_flux'] for r in rows)/1000:.1f} kW/m²")


if __name__ == "__main__":
    main()
