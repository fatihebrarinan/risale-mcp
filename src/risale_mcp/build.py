"""Aşama 2: ham kaynak verisinden eser JSON'ları.

Kullanım:
    uv run python -m risale_mcp.build sozler lemeat   # seçilen eserler
    uv run python -m risale_mcp.build --all           # ayrıştırıcısı olan bütün eserler (şimdilik erisale)

Çıktılar:
    data/books/<eser>.json            eserin başlık ağacı, paragrafları, hâşiyeleri
    data/interim/outline/<eser>.txt   elle kontrol için girintili başlık ağacı
Sonunda `ESERLER.md` kontrol listesi yenilenir.
"""

import argparse
import json
import sys
from collections import Counter
from functools import cache

from risale_mcp import checklist
from risale_mcp.books import erisale as erisale_parser
from risale_mcp.books.model import Book
from risale_mcp.catalog import WORKS, Site, Status, Work, get_work
from risale_mcp.paths import BOOKS_DIR, INTERIM_DIR, RAW_DIR, ROOT
from risale_mcp.sources import erisale

OUTLINE_DIR = INTERIM_DIR / "outline"
PARSEABLE_SITES = {Site.ERISALE}


@cache
def _erisale_book(book_id: str) -> erisale.BookBlocks:
    return erisale.load_book(book_id, erisale.Archive(RAW_DIR / Site.ERISALE))


def outline_text(book: Book) -> str:
    counts = Counter(p["node_id"] for p in book.paragraphs if p["kind"] != "hasiye")
    lines = []

    def walk(node, depth: int) -> None:
        subtitle = f" — {node.subtitle}" if node.subtitle else ""
        lines.append(f"{'  ' * depth}{node.title}{subtitle}  [{node.id}] ¶{counts[node.id]}")
        for child in node.children:
            walk(child, depth + 1)
    walk(book.root, 0)
    return "\n".join(lines) + "\n"


def report(book: Book, parse: erisale_parser.ParseReport) -> list[str]:
    nodes = book.nodes()
    kinds = Counter(p["kind"] for p in book.paragraphs)
    arabic = sum(len(p.get("arabic", [])) for p in book.paragraphs)
    has_text = {p["node_id"] for p in book.paragraphs}
    empty = [n.id for n in nodes if not n.children and n.id not in has_text]
    lines = [
        f"{book.slug}: {len(nodes)} düğüm (satır içi {parse.inline_nodes}), "
        f"{len(book.paragraphs) - kinds['hasiye']} paragraf, {kinds['hasiye']} hâşiye, {arabic} Arapça parça",
        f"  paragraf türleri     : {dict(kinds.most_common())}",
        f"  metinsiz yaprak düğüm: {len(empty)} {empty[:5]}",
        f"  aynı adlı kardeş     : {len(book.renamed)} {book.renamed[:5]}",
        f"  eşsiz BookOnly       : {len(parse.unmatched_book_only)} {parse.unmatched_book_only[:5]}",
        f"  başlıksız açıklama   : {parse.stray_descriptions}",
        f"  editör notu          : {len(book.notes)}",
        f"  kaynakta eksik       : {sum(g['missing_blocks'] for g in book.gaps)} blok {book.gaps[:3]}",
    ]
    if parse.unknown_blocks:
        lines.append(f"  BİLİNMEYEN BLOK      : {dict(parse.unknown_blocks)}")
    return lines


def build_work(work: Work) -> None:
    book, parse = erisale_parser.parse_work(work, _erisale_book(work.source.book))
    BOOKS_DIR.mkdir(parents=True, exist_ok=True)
    OUTLINE_DIR.mkdir(parents=True, exist_ok=True)
    out = BOOKS_DIR / f"{work.slug}.json"
    out.write_text(json.dumps(book.to_json(), ensure_ascii=False, indent=1), encoding="utf-8")
    (OUTLINE_DIR / f"{work.slug}.txt").write_text(outline_text(book), encoding="utf-8")
    print("\n" + "\n".join(report(book, parse)))
    print(f"  yazıldı: {out.relative_to(ROOT)}", flush=True)


def _parseable(work: Work) -> bool:
    return work.source is not None and work.status is not Status.DEFERRED and work.source.site in PARSEABLE_SITES


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("works", nargs="*", help="katalogdaki eser slug'ları")
    parser.add_argument("--all", action="store_true", help="ayrıştırıcısı olan bütün eserler")
    args = parser.parse_args()
    if not (args.all or args.works):
        sys.exit("Eser slug'ı ya da --all verin.")

    works = [w for w in WORKS if _parseable(w)] if args.all else [get_work(s) for s in args.works]
    for work in works:
        if not _parseable(work):
            reason = "ertelendi" if work.status is Status.DEFERRED else "bu kaynağın ayrıştırıcısı Aşama 4'te yazılacak"
            print(f"atlandı: {work.title} — {reason}.")
            continue
        build_work(work)
    checklist.main()


if __name__ == "__main__":
    main()
