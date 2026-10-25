"""risaleoku.com: sayfa sayfa HTML.

    /oku/<kitap>          okuyucu sayfası: içindekiler ve toplam sayfa sayısı
    /ajax/<kitap>/<n>     n. sayfanın yalnızca metni (sitenin okuyucusu da bunu ister)

Ham arşiv (`data/raw/risaleoku/`):
    <kitap>/manifest.json, index.html.gz, pages/<n>.html.gz

robots.txt `Crawl-delay: 10` ister; istemci en az bu kadar bekler.
"""

import html as html_lib
import json
import re
from pathlib import Path
from typing import Callable

from risale_mcp.sources.archive import fetch_cached, read_raw, write_manifest
from risale_mcp.sources.http import PoliteClient

BASE_URL = "https://risaleoku.com"
CRAWL_DELAY = 10.0

_PAGE_COUNT = re.compile(r'<div class="sh_label">\s*<div>&nbsp;/&nbsp;&nbsp;</div>\s*<div>(\d+)</div>')
_TAG = re.compile(r"<[^>]+>")


def page_count(index_html: str) -> int:
    match = _PAGE_COUNT.search(index_html)
    if not match:
        raise ValueError("risaleoku okuyucu sayfasında toplam sayfa sayısı bulunamadı")
    return int(match[1])


def page_text(page_html: str) -> str:
    """Sayfanın yalnızca metin bölgesindeki düz metin (okuyucu araçları ve menü hariç)."""
    start = page_html.find('<div id="dim-bottom"')
    if start >= 0:
        start = page_html.find("</div>", page_html.find("</div>", start) + 6) + 6
        end = page_html.find('<input type="hidden" id="baslangic"')
        page_html = page_html[start:end if end >= 0 else None]
    return " ".join(html_lib.unescape(_TAG.sub(" ", page_html)).split())


def _page_path(root: Path, book: str, n: int) -> Path:
    return root / book / "pages" / f"{n:04d}.html.gz"


def fetch_book(book: str, root: Path, client: PoliteClient, *,
               refresh: bool = False, log: Callable[[str], None] = print) -> None:
    index = fetch_cached(root / book / "index.html.gz", f"{BASE_URL}/oku/{book}", client, refresh)
    total = page_count(index.decode("utf-8"))
    log(f"{book}: {total} sayfa")
    for n in range(1, total + 1):
        path = _page_path(root, book, n)
        if path.exists() and not refresh:
            continue
        fetch_cached(path, f"{BASE_URL}/ajax/{book}/{n}", client, refresh)
        log(f"  [{n}/{total}]")
    write_manifest(root / book / "manifest.json", site="risaleoku", book=book, page_count=total)


def check_book(book: str, root: Path) -> tuple[list[str], bool]:
    """Bütün sayfalar diskte ve metinli olmalı. (rapor satırları, sorunsuz mu)"""
    total = json.loads((root / book / "manifest.json").read_text(encoding="utf-8"))["page_count"]
    missing, empty, chars = [], [], 0
    for n in range(1, total + 1):
        path = _page_path(root, book, n)
        if not path.exists():
            missing.append(n)
            continue
        text = page_text(read_raw(path).decode("utf-8"))
        chars += len(text)
        if not text:
            empty.append(n)
    lines = [
        f"risaleoku/{book}: {total} sayfa, {chars:,} karakter",
        f"  eksik sayfa: {len(missing)} {missing[:20]}",
        f"  boş sayfa  : {len(empty)} {empty[:20]} (baskıdaki boş arka yüzler; hata sayılmaz)",
    ]
    return lines, not missing
