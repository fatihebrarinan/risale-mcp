"""Kaynak sitelerden ham metni indirir ve bütünlüğünü doğrular.

Kullanım:
    uv run python -m risale_mcp.fetch list              # eserler ve kaynak durumu
    uv run python -m risale_mcp.fetch get sozler        # indir (kaldığı yerden devam eder) ve doğrula
    uv run python -m risale_mcp.fetch get --all         # bütün eserler; --site ile tek site
    uv run python -m risale_mcp.fetch check sozler      # yalnızca diskteki ham veriyi doğrula
    uv run python -m risale_mcp.fetch quran             # Kur'ân metni ve mealleri (tanzil.net)

Ham sayfalar `data/raw/<site>/<kitap>/`, doğrulanmış blok listesi
`data/interim/<site>/<kitap>.blocks.json` altına yazılır.
"""

import argparse
import json
import sys
from collections import Counter
from dataclasses import dataclass
from typing import Callable

from risale_mcp.catalog import WORKS, Site, Status, Work, get_work, works_from
from risale_mcp.paths import INTERIM_DIR, RAW_DIR, ROOT
from risale_mcp.sources import erisale, kastamonur, risale_online, risaleoku, tanzil, yeniasya
from risale_mcp.sources.http import PoliteClient

DEFAULT_DELAY = 5.0                                 # saniye; siteleri yormamak için
MIN_DELAY = {Site.RISALEOKU: risaleoku.CRAWL_DELAY}  # robots.txt Crawl-delay


def count_node_types(node, counter: Counter | None = None) -> Counter:
    """Blok ağacındaki bütün düğüm türlerini sayar (Paragraph, FootnoteRef, RTL…)."""
    counter = Counter() if counter is None else counter
    if isinstance(node, dict):
        if "type" in node:
            counter[node["type"]] += 1
        for value in node.values():
            count_node_types(value, counter)
    elif isinstance(node, list):
        for value in node:
            count_node_types(value, counter)
    return counter


def _fetchable_books(works: list[Work]) -> list[tuple[Site, str]]:
    """Eserlerin beslendiği kaynak kitapları, tekrarsız ve katalog sırasıyla."""
    books = {}
    for work in works:
        if work.source is None:
            print(f"atlandı: {work.title} — henüz kaynak bulunamadı.")
        elif work.status is Status.DEFERRED:
            print(f"atlandı: {work.title} — ertelendi ({work.note}).")
        else:
            books.setdefault((work.source.site, work.source.book), None)
    return list(books)


def _selected_works(args: argparse.Namespace) -> list[Work]:
    if args.all:
        works = list(WORKS)
    elif args.works:
        works = [get_work(slug) for slug in args.works]
    else:
        sys.exit("Eser slug'ı ya da --all verin.")
    if args.site:
        works = [w for w in works if w.source and w.source.site == args.site]
    return works


def check_erisale(book_id: str) -> bool:
    """Diskteki ham sayfaları birleştirir, ara dosyayı yazar, raporlar. Sorun yoksa True."""
    book = erisale.load_book(book_id, erisale.Archive(RAW_DIR / Site.ERISALE))
    out = INTERIM_DIR / "erisale" / f"{book_id}.blocks.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(book.to_json(), ensure_ascii=False), encoding="utf-8")

    types = count_node_types([b["content"] for b in book.blocks])
    top_level = Counter(b["content"]["type"] for b in book.blocks)
    print(f"\nerisale/{book_id}: {len(book.pages)} sayfa, {len(book.blocks)} blok")
    print(f"  ilk blockIndex   : {book.first_index} (1 beklenir; 0 kitap başlığıdır)")
    print(f"  eksik blockIndex : {len(book.missing)} {book.missing[:20]}")
    print(f"  çelişen blok     : {len(book.conflicts)} {book.conflicts[:20]}")
    print(f"  çözülemeyen başvuru: {len(book.unresolved)} {book.unresolved[:20]}")
    print(f"  boş sayfa        : {[p.slug for p in book.pages if p.first_block is None]}")
    print(f"  blok türleri     : {dict(top_level.most_common())}")
    print(f"  bütün düğümler   : {dict(types.most_common())}")
    for work in works_from(Site.ERISALE, book_id):
        n = sum(work.source.includes(p.slug) for p in book.pages)
        print(f"  -> {work.slug}: {n} sayfa")
    print(f"  yazıldı: {out.relative_to(ROOT)}")
    return not (book.missing or book.conflicts or book.unresolved)


@dataclass(frozen=True)
class Handler:
    fetch: Callable[[str, PoliteClient, bool], None]  # (kitap, istemci, yeniden indir)
    check: Callable[[str], bool]                      # kitap -> sorunsuz mu


def _fetch_erisale(book: str, client: PoliteClient, refresh: bool) -> None:
    erisale.fetch_book(book, erisale.Archive(RAW_DIR / Site.ERISALE), client, refresh=refresh)


def _plain_handler(site: Site, module) -> Handler:
    """Yalnızca ham veriyi kaydeden kaynaklar: `fetch_book` ve `check_book` arayüzü."""
    root = RAW_DIR / site

    def fetch(book: str, client: PoliteClient, refresh: bool) -> None:
        module.fetch_book(book, root, client, refresh=refresh)

    def check(book: str) -> bool:
        lines, ok = module.check_book(book, root)
        print("\n" + "\n".join(lines))
        return ok

    return Handler(fetch, check)


HANDLERS: dict[Site, Handler] = {
    Site.ERISALE: Handler(_fetch_erisale, check_erisale),
    Site.RISALE_ONLINE: _plain_handler(Site.RISALE_ONLINE, risale_online),
    Site.RISALEOKU: _plain_handler(Site.RISALEOKU, risaleoku),
    Site.YENIASYA: _plain_handler(Site.YENIASYA, yeniasya),
    Site.KASTAMONUR: _plain_handler(Site.KASTAMONUR, kastamonur),
}


def cmd_list(_: argparse.Namespace) -> None:
    for group in dict.fromkeys(w.group for w in WORKS):
        print(f"\n[{group}]")
        for w in (w for w in WORKS if w.group == group):
            source = f"{w.source.site}/{w.source.book}" if w.source else "—"
            print(f"  {w.slug:28} {w.status:9} {source:42} {w.note}")


def cmd_get(args: argparse.Namespace) -> None:
    clients: dict[Site, PoliteClient] = {}
    failed = []
    for site, book in _fetchable_books(_selected_works(args)):
        delay = max(args.delay, MIN_DELAY.get(site, 0.0))
        client = clients.setdefault(site, PoliteClient(delay))
        print(f"\n=== {site}/{book} (istekler arası {delay:g} sn) ===", flush=True)
        try:
            HANDLERS[site].fetch(book, client, args.refresh)
            ok = HANDLERS[site].check(book)
        except Exception as error:  # bir kitabın hatası gece boyu süren toplu indirmeyi durdurmasın
            print(f"HATA {site}/{book}: {error!r}")
            ok = False
        if not ok:
            failed.append(f"{site}/{book}")
    print(f"\nBitti. Sorunlu kitaplar: {failed or 'yok'}")
    if failed:
        sys.exit(1)


def cmd_check(args: argparse.Namespace) -> None:
    results = [HANDLERS[site].check(book) for site, book in _fetchable_books(_selected_works(args))]
    if not all(results):
        sys.exit(1)


def cmd_quran(args: argparse.Namespace) -> None:
    # Kur'ân katalogdaki eserlerden değildir; tek bir arşiv olarak indirilir.
    root = RAW_DIR / "tanzil"
    tanzil.fetch_book("quran", root, PoliteClient(args.delay), refresh=args.refresh)
    lines, ok = tanzil.check_book("quran", root)
    print("\n".join(lines))
    if not ok:
        sys.exit(1)


def _add_selection(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("works", nargs="*", help="katalogdaki eser slug'ları, ör. sozler lemeat")
    parser.add_argument("--all", action="store_true", help="katalogdaki bütün eserler")
    parser.add_argument("--site", type=Site, choices=list(Site), help="yalnızca bu siteden beslenenler")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(required=True)
    sub.add_parser("list", help="eserler ve kaynak durumu").set_defaults(func=cmd_list)
    get = sub.add_parser("get", help="indir ve doğrula")
    _add_selection(get)
    get.add_argument("--refresh", action="store_true", help="diskte olsa da yeniden indir")
    get.add_argument("--delay", type=float, default=DEFAULT_DELAY, help="istekler arası saniye")
    get.set_defaults(func=cmd_get)
    check = sub.add_parser("check", help="diskteki ham veriyi doğrula")
    _add_selection(check)
    check.set_defaults(func=cmd_check)
    quran = sub.add_parser("quran", help="Kur'ân metni ve mealleri (tanzil.net)")
    quran.add_argument("--refresh", action="store_true", help="diskte olsa da yeniden indir")
    quran.add_argument("--delay", type=float, default=DEFAULT_DELAY, help="istekler arası saniye")
    quran.set_defaults(func=cmd_quran)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
