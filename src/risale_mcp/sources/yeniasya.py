"""Yeni Asya: sayfa çevirmeli kitapların `basic-html` metin katmanı. Son çare kaynak.

    /risaleinur/<kitap>/files/assets/basic-html/toc.html        içindekiler
    /risaleinur/<kitap>/files/assets/basic-html/page<n>.html    n. sayfa (windows-1254)

Metin bozuk kodlanmıştır (ş→fl, ı→›, İ→‹), satır sonu tireli, lügat karışıktır ve
Arapça yoktur; onarım ayrıştırma aşamasında yapılır. Toplam sayfa sayısı bilinmediği
için sayfalar ilk 404 yanıtına kadar indirilir.

Ham arşiv (`data/raw/yeniasya/`):
    <kitap>/manifest.json, toc.html.gz, pages/<n>.html.gz
"""

import json
import urllib.error
from pathlib import Path
from typing import Callable

from risale_mcp.sources.archive import fetch_cached, read_raw, write_manifest
from risale_mcp.sources.http import PoliteClient

BASE_URL = "https://www.yeniasya.com.tr/risaleinur"
ENCODING = "windows-1254"


def _base(book: str) -> str:
    return f"{BASE_URL}/{book}/files/assets/basic-html"


def _page_path(root: Path, book: str, n: int) -> Path:
    return root / book / "pages" / f"{n:04d}.html.gz"


def fetch_book(book: str, root: Path, client: PoliteClient, *,
               refresh: bool = False, log: Callable[[str], None] = print) -> None:
    fetch_cached(root / book / "toc.html.gz", f"{_base(book)}/toc.html", client, refresh)
    n = 1
    while True:
        path = _page_path(root, book, n)
        if not path.exists() or refresh:
            try:
                fetch_cached(path, f"{_base(book)}/page{n}.html", client, refresh=True)
            except urllib.error.HTTPError as error:
                if error.code != 404:
                    raise
                break
            log(f"  [{n}]")
        n += 1
    write_manifest(root / book / "manifest.json", site="yeniasya", book=book,
                   encoding=ENCODING, page_count=n - 1)
    log(f"{book}: {n - 1} sayfa")


def check_book(book: str, root: Path) -> tuple[list[str], bool]:
    """Bütün sayfalar diskte ve windows-1254 olarak çözülebilir olmalı. (rapor satırları, sorunsuz mu)"""
    total = json.loads((root / book / "manifest.json").read_text(encoding="utf-8"))["page_count"]
    missing, undecodable = [], []
    for n in range(1, total + 1):
        path = _page_path(root, book, n)
        if not path.exists():
            missing.append(n)
            continue
        try:
            read_raw(path).decode(ENCODING)
        except UnicodeDecodeError:
            undecodable.append(n)
    lines = [
        f"yeniasya/{book}: {total} sayfa",
        f"  eksik sayfa       : {len(missing)} {missing[:20]}",
        f"  çözülemeyen sayfa : {len(undecodable)} {undecodable[:20]}",
    ]
    return lines, total > 0 and not (missing or undecodable)
