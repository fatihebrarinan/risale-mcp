"""Aşama 1: Sözler PDF'inin yapısını inceleme.

Kullanım:
    uv run python -m risale_mcp.inspect_pdf summary
    uv run python -m risale_mcp.inspect_pdf headings [--from N] [--to M]
    uv run python -m risale_mcp.inspect_pdf page N [--spans]
"""

import argparse
import collections
import re
from pathlib import Path

import pymupdf

DEFAULT_PDF = Path(__file__).resolve().parents[2] / "data" / "raw" / "Sozler.pdf"

# Unicode eşlemesi olmayan Arapça fontlar (çıkan metin anlamsız baytlar).
ARABIC_FONTS = {"TTE27E7E00t00", "TTE2735E60t00", "TTE27C1CB8t00"}
# Türkçe özel harfler (ş, ğ, İ) için ayrı gömülü fontlar; metinleri doğru çıkar.
TR_GLYPH_REGULAR = "TTE2733628t00"
TR_GLYPH_BOLD = "TTE2734BB8t00"
# Söz başlıklarında kullanılan süslü font (ş harfi yok: "Onbesinci").
TITLE_FONTS = {"TTE27DA560t00", "TTE27C4F88t00"}

PAGE_MARKER = re.compile(r"-*\s*sh:»?\([SŞ]:(\d+)\)\s*↓?\s*-*")
HASIYE_REF = re.compile(r"\(Haşiye(?:-\s*\d+)?\)|\(\*+\)")
HASIYE_BODY = re.compile(r"^\s*(\(Haşiye(?:-\s*\d+)?\)|\(\*+\))\s*:")


def is_bold(span: dict) -> bool:
    return "Bold" in span["font"] or span["font"] == TR_GLYPH_BOLD or span["font"] in TITLE_FONTS


def iter_lines(page: pymupdf.Page):
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            spans = [s for s in line["spans"] if s["text"].strip()]
            if spans:
                yield line, spans


def summary(doc: pymupdf.Document) -> None:
    print(f"Sayfa: {doc.page_count}  Yer imi (TOC): {len(doc.get_toc())}")
    print(f"Metadata: {doc.metadata}\n")

    fonts = collections.Counter()
    arabic_pages = set()
    total = arabic = 0
    markers_missing, marker_offsets = [], collections.Counter()
    hasiye_refs = hasiye_bodies = 0

    for i, page in enumerate(doc):
        for line, spans in iter_lines(page):
            for s in spans:
                n = len(s["text"].strip())
                fonts[(s["font"], round(s["size"], 1))] += n
                total += n
                if s["font"] in ARABIC_FONTS:
                    arabic += n
                    arabic_pages.add(i + 1)
            text = "".join(s["text"] for s in line["spans"])
            if HASIYE_BODY.match(text):
                hasiye_bodies += 1
        text = page.get_text()
        hasiye_refs += len(HASIYE_REF.findall(text))
        m = PAGE_MARKER.search(text)
        if m:
            marker_offsets[int(m.group(1)) - (i + 1)] += 1
        else:
            markers_missing.append(i + 1)

    print("Font kullanımı (karakter sayısı, font, punto):")
    for (font, size), n in fonts.most_common(25):
        print(f"  {n:>9}  {font:<16} {size}")
    print(f"\nArapça (eşlemesiz) karakter: {arabic} / {total} ({arabic / total:.1%}), "
          f"{len(arabic_pages)} sayfada")
    print(f"Sayfa işaretçisi olmayan sayfalar ({len(markers_missing)}): {markers_missing}")
    print(f"İşaretçi no − PDF sayfa no dağılımı: {dict(marker_offsets)}")
    print(f"Hâşiye işareti (toplam) / gövde satırı: {hasiye_refs} / {hasiye_bodies}")


def headings(doc: pymupdf.Document, first: int, last: int) -> None:
    """Başlık adayları: tamamı kalın ya da >12.5pt satırlar ve kalın önekli paragraflar."""
    for i in range(first - 1, min(last, doc.page_count)):
        for line, spans in iter_lines(doc[i]):
            text = "".join(s["text"] for s in line["spans"]).strip()
            if PAGE_MARKER.search(text) or any(s["font"] in ARABIC_FONTS for s in spans):
                continue
            size = max(s["size"] for s in spans)
            x0, _, x1, _ = line["bbox"]
            centered = abs((x0 + x1) / 2 - 306) < 15 and x0 > 140
            if all(is_bold(s) for s in spans) or size > 12.5:
                tag = "C" if centered else " "
                print(f"p{i + 1:<4} {size:4.1f} {tag} BAŞLIK | {text[:90]}")
            elif is_bold(spans[0]):
                prefix = ""
                for s in line["spans"]:
                    if is_bold(s) or not s["text"].strip():
                        prefix += s["text"]
                    else:
                        break
                print(f"p{i + 1:<4} {size:4.1f}   ÖNEK   | [{prefix.strip()}] {text[len(prefix.strip()):][:60]}")


def page_dump(doc: pymupdf.Document, number: int, spans_mode: bool) -> None:
    page = doc[number - 1]
    if not spans_mode:
        print(page.get_text())
        return
    for line, spans in iter_lines(page):
        for s in spans:
            print(f"y={s['bbox'][1]:5.0f} x={s['bbox'][0]:4.0f} {s['font']:<14} "
                  f"{s['size']:4.1f} | {s['text']!r}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("summary")
    h = sub.add_parser("headings")
    h.add_argument("--from", dest="first", type=int, default=1)
    h.add_argument("--to", dest="last", type=int, default=10_000)
    p = sub.add_parser("page")
    p.add_argument("number", type=int)
    p.add_argument("--spans", action="store_true")
    args = parser.parse_args()

    doc = pymupdf.open(args.pdf)
    if args.cmd == "summary":
        summary(doc)
    elif args.cmd == "headings":
        headings(doc, args.first, args.last)
    else:
        page_dump(doc, args.number, args.spans)


if __name__ == "__main__":
    main()
