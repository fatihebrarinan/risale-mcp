"""Aşama 2: ham kaynak verisinden eser JSON'ları.

Kullanım:
    uv run python -m risale_mcp.build sozler lemeat   # seçilen eserler
    uv run python -m risale_mcp.build --all           # ayrıştırıcısı olan bütün eserler (şimdilik erisale)

Çıktılar:
    data/books/<eser>.json            eserin başlık ağacı, paragrafları, hâşiyeleri, cümleleri
    data/interim/outline/<eser>.txt   elle kontrol için girintili başlık ağacı
Sonunda `ESERLER.md` kontrol listesi yenilenir ve veritabanı (`data/risale.db`) bütün
JSON'lardan yeniden kurulur (`--no-db` ile atlanır). Metni değişen cümlelerin anlamsal arama
vektörü yoksa bildirilir; `python -m risale_mcp.embeddings build voyage-context-4` tamamlar.
"""

import argparse
import json
import re
import sys
from collections import Counter
from functools import cache

from risale_mcp import build_db, checklist, embeddings, sentences
from risale_mcp.books import erisale as erisale_parser
from risale_mcp.books import kastamonur as kastamonur_parser
from risale_mcp.books import risale_online as risale_online_parser
from risale_mcp.books import risaleoku as risaleoku_parser
from risale_mcp.books import yeniasya as yeniasya_parser
from risale_mcp.books.mecmua import CanonicalIndex, MappingReport, map_to_canonical
from risale_mcp.books.model import Book
from risale_mcp.catalog import SECONDARY_SITES, WORKS, Group, Site, Status, Work, get_work
from risale_mcp.db import connect
from risale_mcp.paths import BOOKS_DIR, DB_PATH, INTERIM_DIR, RAW_DIR, ROOT
from risale_mcp.sources import erisale

OUTLINE_DIR = INTERIM_DIR / "outline"
HASIYE_ID = re.compile(r"/h\d+/")
PARSEABLE_SITES = set(Site)


@cache
def _canonical_index() -> CanonicalIndex:
    """Ana ciltlerin eşleme dizini; ana ciltler mecmualardan önce üretildiği için diskten okunur."""
    return CanonicalIndex.load(BOOKS_DIR)


def mapping_report(report: MappingReport) -> list[str]:
    total = report.mapped + report.unique
    return [
        f"  ana cilde eşlenen   : {report.mapped}/{total} paragraf ({report.mapped / max(total, 1):.0%}) "
        f"{dict(report.sources.most_common(6))}",
        f"  mecmuaya özgü       : {report.unique} paragraf, {report.unique_hasiye} hâşiye",
        f"  birleşen eşleme     : {report.merged} paragraf (ana cilt paragrafı bölünmüş)",
        *(f"      {s}" for s in report.unique_samples[:6]),
    ]


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


def report(book: Book, sentence_list: list[dict]) -> list[str]:
    nodes = book.nodes()
    kinds = Counter(p["kind"] for p in book.paragraphs)
    arabic = sum(len(p.get("arabic", [])) for p in book.paragraphs)
    has_text = {p["node_id"] for p in book.paragraphs}
    empty = [n.id for n in nodes if not n.children and n.id not in has_text]
    return [
        f"{book.slug}: {len(nodes)} düğüm, {len(book.paragraphs) - kinds['hasiye']} paragraf, "
        f"{kinds['hasiye']} hâşiye, {arabic} Arapça parça",
        f"  paragraf türleri     : {dict(kinds.most_common())}",
        f"  cümle                : {len(sentence_list)} (hâşiyelerde {sum(bool(HASIYE_ID.search(s['id'])) for s in sentence_list)})",
        f"  metinsiz yaprak düğüm: {len(empty)} {empty[:5]}",
        f"  aynı adlı kardeş     : {len(book.renamed)} {book.renamed[:5]}",
    ]


def erisale_report(book: Book, parse: erisale_parser.ParseReport) -> list[str]:
    lines = [
        f"  satır içi düğüm      : {parse.inline_nodes}",
        f"  eşsiz BookOnly       : {len(parse.unmatched_book_only)} {parse.unmatched_book_only[:5]}",
        f"  başlıksız açıklama   : {parse.stray_descriptions}",
        f"  editör notu          : {len(book.notes)}",
        f"  kaynakta eksik       : {sum(g['missing_blocks'] for g in book.gaps)} blok {book.gaps[:3]}",
    ]
    if parse.unknown_blocks:
        lines.append(f"  BİLİNMEYEN BLOK      : {dict(parse.unknown_blocks)}")
    return lines


def parse(work: Work) -> tuple[Book, list[str]]:
    """Eserin kaynağına göre ayrıştırıcıyı seçer: (eser, ayrıştırıcıya özgü rapor satırları)."""
    if work.source.site is Site.ERISALE:
        book, parse_report = erisale_parser.parse_work(work, _erisale_book(work.source.book))
        return book, erisale_report(book, parse_report)
    if work.source.site is Site.RISALE_ONLINE:
        return risale_online_parser.parse_work(work, RAW_DIR / Site.RISALE_ONLINE), []
    if work.source.site is Site.RISALEOKU:
        return risaleoku_parser.parse_work(work, RAW_DIR / Site.RISALEOKU), []
    if work.source.site is Site.YENIASYA:
        return yeniasya_parser.parse_work(work, RAW_DIR / Site.YENIASYA), []
    if work.source.site is Site.KASTAMONUR:
        return kastamonur_parser.parse_work(work, RAW_DIR / Site.KASTAMONUR), []
    raise ValueError(f"{work.source.site} için ayrıştırıcı yok")


def needs_mapping(work: Work) -> bool:
    """Mecmualar ve son çare kaynaktaki eserler: metni ana ciltlerde olan paragraflar oraya işaret eder."""
    return work.group is Group.MECMUA or work.source.site in SECONDARY_SITES


def build_work(work: Work) -> None:
    book, extra = parse(work)
    BOOKS_DIR.mkdir(parents=True, exist_ok=True)
    OUTLINE_DIR.mkdir(parents=True, exist_ok=True)
    data = book.to_json()
    if needs_mapping(work):
        extra += mapping_report(map_to_canonical(data, _canonical_index()))
    data["sentences"] = sentences.segment(data)
    out = BOOKS_DIR / f"{work.slug}.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUTLINE_DIR / f"{work.slug}.txt").write_text(outline_text(book), encoding="utf-8")
    print("\n" + "\n".join(report(book, data["sentences"]) + extra))
    print(f"  yazıldı: {out.relative_to(ROOT)}", flush=True)


def _parseable(work: Work) -> bool:
    return work.source is not None and work.status is not Status.DEFERRED and work.source.site in PARSEABLE_SITES


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("works", nargs="*", help="katalogdaki eser slug'ları")
    parser.add_argument("--all", action="store_true", help="ayrıştırıcısı olan bütün eserler")
    parser.add_argument("--no-db", action="store_true", help="veritabanını yeniden kurma")
    args = parser.parse_args()
    if not (args.all or args.works):
        sys.exit("Eser slug'ı ya da --all verin.")

    works = [w for w in WORKS if _parseable(w)] if args.all else [get_work(s) for s in args.works]
    # Eşleme dizini ana ciltlerden kurulur: onlar önce üretilmeli.
    works = [w for w in works if not needs_mapping(w)] + [w for w in works if needs_mapping(w)]
    for work in works:
        if not _parseable(work):
            reason = "ertelendi" if work.status is Status.DEFERRED else "bu kaynağın ayrıştırıcısı Aşama 4'te yazılacak"
            print(f"atlandı: {work.title} — {reason}.")
            continue
        build_work(work)
    checklist.main()
    if not args.no_db:
        print("\nveritabanı:\n" + "\n".join(build_db.build().lines()))
        if count := embeddings.missing(connect(DB_PATH)):
            print(f"\nanlamsal arama: {count} cümlenin vektörü yok; tamamlamak için "
                  f"`uv run python -m risale_mcp.embeddings build {embeddings.SEARCH_MODEL}`")


if __name__ == "__main__":
    main()
