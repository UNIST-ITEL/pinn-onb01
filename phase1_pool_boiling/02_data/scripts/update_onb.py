"""
ONB 인덱스 수동 보정 헬퍼.

특정 표준 CSV의 ONB_flag 행을 변경하고 sidecar meta.yaml의 onb_index도 동기화.

사용:
  python3 02_data/scripts/update_onb.py BETZ_2013 6b_hydrophilic 7
  python3 02_data/scripts/update_onb.py BETZ_2013 6b_Superbiphiliccircle --clear
  python3 02_data/scripts/update_onb.py BETZ_2013 4_SHPi --show
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LIT_ROOT = PROJECT_ROOT / "02_data" / "raw" / "literature"


def find_csv(paper_id: str, series_key: str) -> Path:
    """series_key 예: '6b_hydrophilic', '4_SHPi'"""
    paper_dir = LIT_ROOT / paper_id
    target = paper_dir / f"figure_{series_key}.csv"
    if not target.is_file():
        # 부분 매칭 fallback
        candidates = list(paper_dir.glob(f"figure_*{series_key}*.csv"))
        if len(candidates) == 1:
            return candidates[0]
        if not candidates:
            raise SystemExit(f"no CSV matches: {target}")
        raise SystemExit(f"ambiguous match for {series_key}: {[c.name for c in candidates]}")
    return target


def show_csv(csv_path: Path) -> None:
    print(f"=== {csv_path.name} ===")
    with csv_path.open() as f:
        reader = csv.reader(f)
        header = next(reader)
        print(f"  {'idx':>3} | {'ΔT [K]':>8} | {'q [W/m²]':>12} | {'HTC [W/m²K]':>12} | ONB | notes")
        print(f"  {'-'*3:>3} + {'-'*8:>8} + {'-'*12:>12} + {'-'*12:>12} + {'-'*3} + ----")
        for i, row in enumerate(reader):
            q = float(row[0])
            dT = float(row[1])
            onb = row[7] == "True"
            htc = q / dT if dT > 0 else 0.0
            mark = "★" if onb else " "
            notes_short = row[8][:50]
            print(f"  {i:>3} | {dT:>8.3f} | {q:>12.1f} | {htc:>12.1f} | {mark:>3} | {notes_short}")


def apply_onb_change(csv_path: Path, new_idx: int | None) -> int | None:
    """ONB_flag 컬럼을 new_idx 행에만 True로 설정. None이면 전부 False."""
    with csv_path.open() as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    n = len(rows)
    if new_idx is not None and not (0 <= new_idx < n):
        raise SystemExit(f"index {new_idx} out of range [0, {n - 1}]")

    old_idx: int | None = None
    for i, row in enumerate(rows):
        was_onb = row[7] == "True"
        is_onb = (new_idx is not None and i == new_idx)
        if was_onb:
            old_idx = i
        row[7] = "True" if is_onb else "False"
        # notes의 ONB_auto/ONB_manual 표시 정리
        notes = row[8].strip('"').strip()
        notes_parts = [p for p in notes.split("; ") if p and not p.startswith("ONB_")]
        if is_onb:
            notes_parts.append(f"ONB_manual (was idx={old_idx})" if old_idx != i else "ONB_manual")
        row[8] = "; ".join(notes_parts)

    with csv_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)

    return old_idx


def update_meta_yaml(meta_path: Path, new_idx: int | None) -> None:
    if not meta_path.is_file():
        return
    txt = meta_path.read_text()
    new_val = str(new_idx) if new_idx is not None else "null"
    txt2 = re.sub(r"^onb_index:.*$", f"onb_index: {new_val}", txt, count=1, flags=re.MULTILINE)
    meta_path.write_text(txt2)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paper_id")
    parser.add_argument("series_key", help="예: 6b_hydrophilic, 4_SHPi")
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("new_idx", nargs="?", type=int, help="새 ONB 행 인덱스 (0-based)")
    g.add_argument("--clear", action="store_true", help="ONB_flag 모두 False로")
    g.add_argument("--show", action="store_true", help="현재 CSV 내용 표시만")
    args = parser.parse_args()

    csv_path = find_csv(args.paper_id, args.series_key)

    if args.show:
        show_csv(csv_path)
        return

    new_idx = None if args.clear else args.new_idx
    old_idx = apply_onb_change(csv_path, new_idx)
    meta_path = csv_path.with_suffix(".meta.yaml")
    update_meta_yaml(meta_path, new_idx)
    print(f"[ok] {csv_path.name}: ONB idx {old_idx} → {new_idx}")
    print(f"     meta.yaml synced: {meta_path.name}")


if __name__ == "__main__":
    main()
