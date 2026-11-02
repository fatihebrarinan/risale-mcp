"""nurpedia.org: Risale'deki hadislerin listesi ve bölüm bölüm âyet-hadis mealleri.

Metin değil, hadis işaretlerinin dayanağıdır: `Risale:Hadisler` sayfası elle hazırlanmış listedir (kaynağı
Abdülkadir Badıllı'nın "Risale-i Nur'un Kudsi Kaynakları"), `Risale:<bölüm> (Ayet-Hadis Mealleri)` sayfaları
Arapçayı meali ve tahriciyle verir. Sunucuya metni çıkmaz. İzin: `docs/izinler.md`. robots.txt yalnızca özel
sayfaları ve `api.php`'yi kapatır; okuma sayfaları indirilir.

Ham arşiv (`data/raw/nurpedia/`): <sayfa adı>.html, manifest.json
"""

import re
from html import unescape
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote, unquote

from risale_mcp.sources.archive import fetch_cached, write_manifest
from risale_mcp.sources.http import PoliteClient

BASE_URL = "https://www.nurpedia.org/wiki/"
INDEX = "Risale:Hadisler"
LISTS = (INDEX, "Risale:Kudsi_Hadisler", "Risale:33_Hadis")
SUFFIX = "_(Ayet-Hadis_Mealleri)"
SERIES = (("Söz", 33), ("Mektup", 33), ("Lem'a", 33), ("Şua", 15))    # sitenin kullandığı sayfa adları


def page_path(root: Path, title: str) -> Path:
    return root / f"{title.replace('/', '_')}.html"


def linked_pages(html: str) -> list[str]:
    links = {unescape(unquote(link)) for link in re.findall(r'href="/wiki/([^"#?]+)', html)}
    return sorted(link for link in links if link.endswith(SUFFIX))


def candidates(html: str) -> list[str]:
    """Listenin bağlantı verdiği meal sayfaları ve numaralı bölümlerin aynı kalıptaki sayfaları."""
    numbered = [f"Risale:{n}._{name}{SUFFIX}" for name, last in SERIES for n in range(1, last + 1)]
    return sorted({*linked_pages(html), *numbered})


def fetch(root: Path, client: PoliteClient, *, refresh: bool = False) -> tuple[int, list[str]]:
    """Listeleri ve var olan meal sayfalarını indirir: (dosya sayısı, bulunamayan sayfalar)."""
    def get(title: str) -> bytes | None:
        try:
            return fetch_cached(page_path(root, title), BASE_URL + quote(title, safe=":'()_."), client, refresh)
        except HTTPError as error:
            if error.code == 404:
                return None
            raise

    index = get(INDEX)
    missing, pages = [], [INDEX]
    for title in [*LISTS[1:], *candidates(index.decode("utf-8"))]:
        if get(title) is None:
            missing.append(title)
        else:
            pages.append(title)
    write_manifest(root / "manifest.json", pages=pages, missing=missing)
    return len(pages), missing
