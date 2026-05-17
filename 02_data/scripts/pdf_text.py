"""PDF 텍스트 추출 헬퍼.

논문 PDF에서 표제·본문·참고문헌 영역의 텍스트를 추출하여
paper-card-extractor 에이전트가 사용 가능한 형태로 반환.

사용 예:
    from pdf_text import extract_text, extract_metadata, summarize

    text = extract_text("01_survey/pdfs/HSU_JHT_1962_NucleationCavity.pdf")
    meta = extract_metadata("01_survey/pdfs/HSU_JHT_1962_NucleationCavity.pdf")
    print(summarize(text, max_chars=2000))

CLI 사용:
    python 02_data/scripts/pdf_text.py 01_survey/pdfs/HSU_JHT_1962_NucleationCavity.pdf
    python 02_data/scripts/pdf_text.py path/to.pdf --pages 1-3
    python 02_data/scripts/pdf_text.py path/to.pdf --by-font  # 폰트 크기별 분리(제목 추출용)
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

try:
    import pdfplumber
except ImportError:
    sys.stderr.write(
        "pdfplumber 미설치. `pip install -r requirements.txt` 또는 "
        "`pip install pdfplumber` 실행 후 재시도.\n"
    )
    sys.exit(1)


class PDFMetadata(NamedTuple):
    n_pages: int
    title_candidates: list[str]
    largest_font_text: str
    info: dict


def _parse_page_range(spec: str | None, n_pages: int) -> list[int]:
    """'1-3', '1,3,5', None → 0-based 페이지 인덱스 리스트."""
    if spec is None:
        return list(range(n_pages))
    pages: set[int] = set()
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-")
            pages.update(range(int(a) - 1, int(b)))
        else:
            pages.add(int(part) - 1)
    return sorted(p for p in pages if 0 <= p < n_pages)


def extract_text(pdf_path: str | Path, pages: str | None = None) -> str:
    """PDF에서 텍스트 추출. pages 미지정 시 전체."""
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(path)
    with pdfplumber.open(path) as pdf:
        idx = _parse_page_range(pages, len(pdf.pages))
        return "\n".join((pdf.pages[i].extract_text() or "") for i in idx)


def extract_by_font_size(pdf_path: str | Path, page: int = 0) -> dict[float, str]:
    """페이지의 폰트 크기별로 텍스트 분리. 제목 추출 시 유용."""
    path = Path(pdf_path)
    with pdfplumber.open(path) as pdf:
        p = pdf.pages[page]
        buckets: dict[float, list[str]] = defaultdict(list)
        for c in p.chars:
            buckets[round(c["size"], 1)].append(c["text"])
    return {size: "".join(chars) for size, chars in buckets.items()}


_TITLE_NEGATIVES = re.compile(
    r"^(introduction|abstract|nomenclature|references|figure|table|"
    r"copyright|journal|received|paper no|received)",
    re.IGNORECASE,
)


def extract_metadata(pdf_path: str | Path) -> PDFMetadata:
    """페이지 수 + 제목 후보 + PDF info dict 반환.

    제목은 (1) 폰트 크기 상위 → 후보, (2) PDF info의 /Title 필드 백업.
    """
    path = Path(pdf_path)
    with pdfplumber.open(path) as pdf:
        info = pdf.metadata or {}
        n_pages = len(pdf.pages)
        font_buckets = extract_by_font_size(path, page=0)

    sizes_desc = sorted(font_buckets.keys(), reverse=True)
    candidates: list[str] = []
    if info.get("Title"):
        candidates.append(info["Title"])
    for size in sizes_desc[:5]:
        text = font_buckets[size].strip()
        if not text or len(text) < 8:
            continue
        if _TITLE_NEGATIVES.match(text):
            continue
        candidates.append(text[:200])

    largest_font_text = font_buckets[sizes_desc[0]] if sizes_desc else ""
    return PDFMetadata(
        n_pages=n_pages,
        title_candidates=candidates,
        largest_font_text=largest_font_text,
        info=dict(info),
    )


def summarize(text: str, max_chars: int = 2000) -> str:
    """긴 본문에서 abstract 영역만 빠르게 발췌."""
    abst_match = re.search(
        r"\b(abstract|summary)\b(.*?)(?:\bintroduction\b|\bnomenclature\b)",
        text,
        re.IGNORECASE | re.DOTALL,
    )
    if abst_match:
        snippet = abst_match.group(2).strip()
        return snippet[:max_chars]
    return text[:max_chars]


def main() -> int:
    parser = argparse.ArgumentParser(description="PDF 텍스트 추출 헬퍼")
    parser.add_argument("pdf_path", type=Path)
    parser.add_argument("--pages", default=None, help="'1-3' 또는 '1,3,5'")
    parser.add_argument("--by-font", action="store_true", help="폰트 크기별 분리")
    parser.add_argument("--meta", action="store_true", help="메타데이터만 출력")
    parser.add_argument("--abstract", action="store_true", help="abstract만 발췌")
    args = parser.parse_args()

    if args.meta:
        meta = extract_metadata(args.pdf_path)
        print(f"Pages: {meta.n_pages}")
        print(f"PDF info: {meta.info}")
        print("Title candidates:")
        for c in meta.title_candidates:
            print(f"  - {c}")
        return 0

    if args.by_font:
        buckets = extract_by_font_size(args.pdf_path)
        for size in sorted(buckets.keys(), reverse=True):
            text = buckets[size].strip()
            if text:
                print(f"\n=== Font {size} ({len(text)} chars) ===")
                print(text[:300])
        return 0

    text = extract_text(args.pdf_path, args.pages)
    if args.abstract:
        print(summarize(text))
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
