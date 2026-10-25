"""kastamonur.com: Âsâr-ı Bedîiyye baskısından "Nutuklar ve Makaleler" (Makalat ve Nutuk).

Eser tek bir WordPress yazısıdır; metni MediaWiki'den aktarılmıştır (başlıklar `h1`–`h3`,
dipnotlar `<sup class="reference">` ve bölüm sonundaki `<ol class="references">`).
Sitenin "TELİF UYARISI": içerik izinsiz ve kaynak gösterilmeden kullanılamaz. Kullanım kişiseldir;
yayımlanırsa izin alınacak.

Ham arşiv (`data/raw/kastamonur/`):
    <yazı>/manifest.json, page.html.gz
"""

import json
from pathlib import Path
from typing import Callable

from risale_mcp.sources.archive import fetch_cached, read_raw, write_manifest
from risale_mcp.sources.http import PoliteClient

BASE_URL = "https://www.kastamonur.com"
# Yazının başı ve sonu; arasındaki her şey eserdir.
START_MARKER = "<b>Nutuklar ve Makaleler</b>"
END_MARKER = 'class="wpautbox-below"'


def page_path(root: Path, book: str) -> Path:
    return root / book / "page.html.gz"


def read_page(book: str, root: Path) -> str:
    return read_raw(page_path(root, book)).decode("utf-8")


def article_html(page: str) -> str:
    """Sayfadan yalnızca eserin kendisi (paylaşım düğmeleri, yorumlar, menüler hariç)."""
    start, end = page.find(START_MARKER), page.find(END_MARKER)
    if start < 0 or end < start:
        raise ValueError("Sayfada eserin başı ya da sonu bulunamadı; site düzeni değişmiş olabilir.")
    return page[page.rfind("<", 0, start):end]


def fetch_book(book: str, root: Path, client: PoliteClient, *,
               refresh: bool = False, log: Callable[[str], None] = print) -> None:
    url = f"{BASE_URL}/{book}/"
    fetch_cached(page_path(root, book), url, client, refresh)
    write_manifest(root / book / "manifest.json", site="kastamonur", book=book, url=url)
    log(f"{book}: 1 sayfa")


def check_book(book: str, root: Path) -> tuple[list[str], bool]:
    """Eser sayfada bulunmalı; her dipnot işaretinin listede karşılığı olmalı."""
    manifest = root / book / "manifest.json"
    if not manifest.exists() or not page_path(root, book).exists():
        return [f"kastamonur/{book}: indirilmemiş"], False
    url = json.loads(manifest.read_text(encoding="utf-8"))["url"]
    try:
        html = article_html(read_page(book, root))
    except ValueError as error:
        return [f"kastamonur/{book}: {error}"], False
    refs, notes = html.count('class="reference"'), html.count('id="cite_note-')
    lines = [
        f"kastamonur/{book}: {url}",
        f"  eser metni        : {len(html) / 1000:.0f} KB",
        f"  dipnot işareti    : {refs}, dipnot: {notes}",
    ]
    return lines, refs > 0 and notes >= refs
