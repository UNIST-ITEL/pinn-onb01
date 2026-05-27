"""
표준화된 boiling curve CSV들의 surface_id 컬럼을 SFC-XXX로 일괄 업데이트.

매핑 정의 (paper_id, figure, series) → SFC-ID
"""

from __future__ import annotations

import csv
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LIT_ROOT = PROJECT_ROOT / "02_data" / "raw" / "literature"


# (paper_id, figure, series) → SFC-XXX
SURFACE_MAPPING: dict[tuple[str, str, str], str] = {
    # BETZ_2013
    ("BETZ_2013", "4", "Hydrophilic"): "SFC-001",
    ("BETZ_2013", "4", "Hydrophobic"): "SFC-002",
    ("BETZ_2013", "4", "SHPi"): "SFC-003",
    ("BETZ_2013", "4", "SHPo"): "SFC-004",
    ("BETZ_2013", "6b", "hydrophilic"): "SFC-001",
    ("BETZ_2013", "6b", "Superhydrophilic"): "SFC-003",
    ("BETZ_2013", "6b", "Biphilic"): "SFC-005",
    ("BETZ_2013", "6b", "Superbiphiliccircle"): "SFC-006",
    ("BETZ_2013", "6b", "Superbiphilichexagon"): "SFC-007",
    ("BETZ_2013", "7b", "Biphilic"): "SFC-005",
    ("BETZ_2013", "7b", "Superbiphilic"): "SFC-006",  # Fig.7b의 SBPi (CHF/film, ONB 보류)
    ("BETZ_2013", "7b", "Chen2009"): "SFC-030",
    ("BETZ_2013", "7b", "Li2008"): "SFC-030",
    ("BETZ_2013", "7b", "Jones10um"): "SFC-030",
    ("BETZ_2013", "7b", "JonesPolished"): "SFC-030",
    # JO_2011
    ("JO_2011", "3", "Hydrophilic"): "SFC-008",
    ("JO_2011", "3", "Hydrophobic"): "SFC-009",
    # PHAN_2009
    ("PHAN_2009", "12a", "theta22"): "SFC-010",
    ("PHAN_2009", "12a", "theta31"): "SFC-011",
    ("PHAN_2009", "12a", "theta67"): "SFC-012",
    ("PHAN_2009", "12a", "theta80"): "SFC-013",
    ("PHAN_2009", "12a", "theta85"): "SFC-014",
    # JONES_2009
    ("JONES_2009", "3a", "Polished"): "SFC-015",
    ("JONES_2009", "3a", "EDM1p08"): "SFC-017",
    ("JONES_2009", "3a", "EDM2p22"): "SFC-018",
    ("JONES_2009", "3a", "EDM5p89"): "SFC-019",
    ("JONES_2009", "3a", "EDM10p0"): "SFC-020",
    ("JONES_2009", "4a", "Polished"): "SFC-016",
    ("JONES_2009", "4a", "EDM1p08"): "SFC-017",
    ("JONES_2009", "4a", "EDM2p22"): "SFC-018",
    ("JONES_2009", "4a", "EDM5p89"): "SFC-019",
    ("JONES_2009", "4a", "EDM10p0"): "SFC-020",
    # BOURDON_2012
    ("BOURDON_2012", "4", "S1"): "SFC-021",
    ("BOURDON_2012", "4", "S2"): "SFC-022",
    ("BOURDON_2012", "4", "S3"): "SFC-023",
    ("BOURDON_2012", "6", "ungrafted"): "SFC-021",   # same as S1
    ("BOURDON_2012", "6", "grafted_whole"): "SFC-024",
    ("BOURDON_2012", "6", "grafted_center"): "SFC-025",
    # BOURDON_2015
    ("BOURDON_2015", "3", "ONB_vs_theta"): "SFC-MULTI",  # 행별로 다른 SFC 매핑 (theta별)
    ("BOURDON_2015", "7", "NotGrafted"): "SFC-026",
    ("BOURDON_2015", "7", "MPEGPTMS"): "SFC-027",
    ("BOURDON_2015", "7", "AcOUTES"): "SFC-028",
    ("BOURDON_2015", "7", "OTS"): "SFC-029",
    # JABARDO_2009 (Cu surfaces, 같은 표면이 두 fluid에 사용)
    ("JABARDO_2009", "9a", "Cu_Ra0p07P"): "SFC-031",
    ("JABARDO_2009", "9a", "Cu_Ra0p16SP"): "SFC-032",
    ("JABARDO_2009", "9a", "Cu_Ra0p47SP"): "SFC-033",
    ("JABARDO_2009", "9a", "Cu_Ra0p5SP"): "SFC-034",
    ("JABARDO_2009", "9a", "Cu_Ra2p5SPI"): "SFC-035",
    ("JABARDO_2009", "9a", "Cu_Ra3p3SPI"): "SFC-036",
    ("JABARDO_2009", "9a", "Cu_Ra4p6SPI"): "SFC-037",
    ("JABARDO_2009", "9a", "Cu_Ra10p5SPI"): "SFC-038",
    ("JABARDO_2009", "9c", "Cu_Ra0p07P"): "SFC-031",
    ("JABARDO_2009", "9c", "Cu_Ra0p16SP"): "SFC-032",
    ("JABARDO_2009", "9c", "Cu_Ra0p47SP"): "SFC-033",
    ("JABARDO_2009", "9c", "Cu_Ra0p5SP"): "SFC-034",
    ("JABARDO_2009", "9c", "Cu_Ra2p5SPI"): "SFC-035",
    ("JABARDO_2009", "9c", "Cu_Ra3p3SPI"): "SFC-036",
    ("JABARDO_2009", "9c", "Cu_Ra4p6SPI"): "SFC-037",
    ("JABARDO_2009", "9c", "Cu_Ra10p5SPI"): "SFC-038",
    # JABARDO_2009 Fig.9b (R-123, p_r=0.092) — Cu, 동일 표면 SFC 재사용
    ("JABARDO_2009", "9b", "Cu_Ra0p16SP"): "SFC-032",
    ("JABARDO_2009", "9b", "Cu_Ra0p47SP"): "SFC-033",
    ("JABARDO_2009", "9b", "Cu_Ra3p3SPI"): "SFC-036",
    ("JABARDO_2009", "9b", "Cu_Ra4p6SPI"): "SFC-037",
    ("JABARDO_2009", "9b", "Cu_Ra10p5SPI"): "SFC-038",
    # JABARDO_2009 Fig.9d (R-134a, p_r=0.260) — Cu, 동일 표면 SFC 재사용
    ("JABARDO_2009", "9d", "Cu_Ra0p07P"): "SFC-031",
    ("JABARDO_2009", "9d", "Cu_Ra0p5SP"): "SFC-034",
    ("JABARDO_2009", "9d", "Cu_Ra2p5SPI"): "SFC-035",
    ("JABARDO_2009", "9d", "Cu_Ra4p6SPI"): "SFC-037",
    ("JABARDO_2009", "9d", "Cu_Ra10p5SPI"): "SFC-038",
    # JABARDO_2009 Fig.10a (Brass, R-134a, p_r=0.063)
    ("JABARDO_2009", "10a", "Br_Ra0p08P"): "SFC-039",
    ("JABARDO_2009", "10a", "Br_Ra0p90SP"): "SFC-040",
    ("JABARDO_2009", "10a", "Br_Ra1p2SPI"): "SFC-041",
    ("JABARDO_2009", "10a", "Br_Ra1p8SPI"): "SFC-042",
    ("JABARDO_2009", "10a", "Br_Ra3p5SPI"): "SFC-043",
    # JABARDO_2009 Fig.10b (Brass, R-134a, p_r=0.260)
    ("JABARDO_2009", "10b", "Br_Ra0p08P"): "SFC-039",
    ("JABARDO_2009", "10b", "Br_Ra0p90SP"): "SFC-040",
    ("JABARDO_2009", "10b", "Br_Ra1p2SPI"): "SFC-041",
    ("JABARDO_2009", "10b", "Br_Ra1p8SPI"): "SFC-042",
    ("JABARDO_2009", "10b", "Br_Ra3p5SPI"): "SFC-043",
    # JABARDO_2009 Fig.10c (Stainless Steel, R-134a, p_r=0.063)
    ("JABARDO_2009", "10c", "SS_Ra0p03P"): "SFC-044",
    ("JABARDO_2009", "10c", "SS_Ra0p07SP"): "SFC-045",
    ("JABARDO_2009", "10c", "SS_Ra0p45SP"): "SFC-046",
    ("JABARDO_2009", "10c", "SS_Ra0p90SPI"): "SFC-047",
    ("JABARDO_2009", "10c", "SS_Ra1p45SPI"): "SFC-048",
    ("JABARDO_2009", "10c", "SS_Ra2p50SPI"): "SFC-049",
    ("JABARDO_2009", "10c", "SS_Ra3p20SPI"): "SFC-050",
    # JABARDO_2009 Fig.10d (Stainless Steel, R-134a, p_r=0.260)
    ("JABARDO_2009", "10d", "SS_Ra0p03P"): "SFC-044",
    ("JABARDO_2009", "10d", "SS_Ra0p07SP"): "SFC-045",
    ("JABARDO_2009", "10d", "SS_Ra0p45SP"): "SFC-046",
    ("JABARDO_2009", "10d", "SS_Ra0p90SPI"): "SFC-047",
    ("JABARDO_2009", "10d", "SS_Ra1p45SPI"): "SFC-048",
    ("JABARDO_2009", "10d", "SS_Ra2p50SPI"): "SFC-049",
    ("JABARDO_2009", "10d", "SS_Ra3p20SPI"): "SFC-050",
}

# Fig.3 ONB diagram의 row별 매핑 (theta_contact 값 → SFC)
THETA_TO_SFC: dict[float, str] = {
    11.1: "SFC-026",   # NotGrafted
    33.5: "SFC-027",   # MPEGPTMS
    70.8: "SFC-028",   # AcOUTES
    101.6: "SFC-029",  # OTS
}


def parse_csv_filename(name: str) -> tuple[str, str, str] | None:
    """figure_{fig}_{series}.csv → (fig, series). paper는 폴더에서."""
    if not name.startswith("figure_") or not name.endswith(".csv") or ".meta." in name:
        return None
    body = name[len("figure_"):-len(".csv")]
    parts = body.split("_", 1)
    if len(parts) != 2:
        return None
    return parts[0], parts[1]


def update_csv_surface_id(csv_path: Path, paper_id: str) -> tuple[int, str | None]:
    """CSV의 surface_id 컬럼을 매핑에 따라 업데이트. (변경 행수, 적용된 SFC) 반환."""
    parsed = parse_csv_filename(csv_path.name)
    if not parsed:
        return 0, None
    fig_id, series = parsed

    sfc_id = SURFACE_MAPPING.get((paper_id, fig_id, series))
    if sfc_id is None:
        return 0, None

    with csv_path.open() as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    # surface_id 인덱스 (4th column, idx 3)
    sid_col = header.index("surface_id")
    notes_col = header.index("notes")

    n_changed = 0
    for row in rows:
        if sfc_id == "SFC-MULTI":
            # BOURDON_2015 Fig.3: theta별 매핑
            theta_match = re.search(r"theta_contact=([\d.]+)deg", row[notes_col])
            if theta_match:
                theta = float(theta_match.group(1))
                # 가장 가까운 theta 찾기
                closest = min(THETA_TO_SFC.keys(), key=lambda t: abs(t - theta))
                row[sid_col] = THETA_TO_SFC[closest]
                n_changed += 1
        else:
            if row[sid_col] != sfc_id:
                row[sid_col] = sfc_id
                n_changed += 1

    if n_changed > 0:
        with csv_path.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(rows)

    return n_changed, sfc_id


def main() -> None:
    print("[update_surface_id] applying SFC-XXX to all standardized CSVs")
    total_files = 0
    total_rows = 0

    for paper_dir in sorted(LIT_ROOT.glob("*/")):
        paper_id = paper_dir.name
        if not paper_id[0].isupper():
            continue
        for csv_path in sorted(paper_dir.glob("figure_*.csv")):
            if ".meta." in csv_path.name:
                continue
            n, sfc = update_csv_surface_id(csv_path, paper_id)
            if sfc:
                print(f"  {paper_id}/{csv_path.name} → {sfc} ({n} rows updated)")
                total_files += 1
                total_rows += n
            elif n == 0:
                # Mapping 없는 파일
                print(f"  [skip] {paper_id}/{csv_path.name}: no mapping")

    print()
    print(f"=== summary ===")
    print(f"  files updated: {total_files}")
    print(f"  rows updated:  {total_rows}")


if __name__ == "__main__":
    main()
