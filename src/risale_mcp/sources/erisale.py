"""erisale.com: standart baskı, birincil kaynak.

Site her bölüm için ayrı bir sayfa sunar (`/tr/<kitap>/<bölüm-slug>`); sayfa listesi
sitemap'ten, kitap sırasıyla alınır. Metin, sayfanın içine gömülü React Server Components
verisinde yapısal bir ağaç olarak durur:

    {"bookId": "sozler", "blockIndex": 537, "sectionIndex": 18, "pageNumber": 0,
     "content": {"type": "Paragraph", "children": [...]}}

`blockIndex` kitap içinde sürekli bir sıra numarasıdır; bütün sayfaların blokları
birleştirilince boşluk kalmamalıdır. Bu, eksik bölüm olup olmadığının kanıtıdır.

robots.txt yalnızca `/api/` yolunu yasaklar; biz yalnızca okuma sayfalarını indiririz.
"""

import gzip
import html as html_lib
import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable
from xml.etree import ElementTree

from risale_mcp.sources.archive import write_atomic
from risale_mcp.sources.http import PoliteClient

BASE_URL = "https://www.erisale.com"
SITEMAP_URL = f"{BASE_URL}/sitemap-tr.xml"
REQUEST_DELAY = 5.0  # saniye

_SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
_PAGE_URL = re.compile(rf"^{re.escape(BASE_URL)}/tr/([^/]+)/([^/]+)$")
_RSC_PUSH = re.compile(r'self\.__next_f\.push\(\[1,"((?:[^"\\]|\\.)*)"\]\)')
_BLOCK_START = re.compile(r'\{"bookId":')
_TITLE = re.compile(r"<title>(.*?)</title>", re.S)
_TITLE_SEP = " — "

# Basılı sayfa bilgisi veri setine girmez.
_PAGE_BLOCK = "PageNumber"


@dataclass(frozen=True)
class Page:
    book: str
    slug: str
    url: str


# ---------------------------------------------------------------- ayrıştırma

def parse_sitemap(xml: str) -> list[Page]:
    """Sitemap'teki bölüm sayfalarını kitap sırasıyla döndürür."""
    pages = []
    for loc in ElementTree.fromstring(xml).iterfind("sm:url/sm:loc", _SITEMAP_NS):
        match = _PAGE_URL.match((loc.text or "").strip())
        if match:
            pages.append(Page(book=match[1], slug=match[2], url=match[0]))
    return pages


def rsc_payload(html: str) -> str:
    """Sayfaya parça parça gömülmüş RSC akışını tek metin olarak birleştirir."""
    return "".join(json.loads(f'"{chunk}"') for chunk in _RSC_PUSH.findall(html))


def extract_blocks(html: str) -> list[dict]:
    """Sayfadaki metin bloklarını `blockIndex` sırasıyla döndürür."""
    payload = rsc_payload(html)
    decoder = json.JSONDecoder()
    blocks: dict[int, dict] = {}
    for match in _BLOCK_START.finditer(payload):
        try:
            obj, _ = decoder.raw_decode(payload, match.start())
        except json.JSONDecodeError:
            continue
        if "blockIndex" in obj and "content" in obj:
            blocks.setdefault(obj["blockIndex"], obj)
    return [blocks[i] for i in sorted(blocks)]


def extract_breadcrumb(html: str) -> list[str]:
    """Sayfa başlığındaki bölüm yolu: "Onuncu Söz — On iki Hakikat — Beşinci Hakikat — Sözler | eRisale"."""
    match = _TITLE.search(html)
    if not match:
        return []
    title = html_lib.unescape(match[1]).rsplit(" | ", 1)[0]
    return title.split(_TITLE_SEP)[:-1]  # son öğe kitap adıdır


# ---------------------------------------------------------------- ham arşiv

class Archive:
    """`data/raw/erisale/` altındaki ham dosyalar.

    sitemap-tr.xml
    <kitap>/manifest.json         sayfa sırası ve indirme zamanı
    <kitap>/pages/<slug>.html.gz  sayfanın kendisi, değiştirilmeden
    """

    def __init__(self, root: Path):
        self.root = root

    @property
    def sitemap_path(self) -> Path:
        return self.root / "sitemap-tr.xml"

    def manifest_path(self, book: str) -> Path:
        return self.root / book / "manifest.json"

    def page_path(self, page: Page) -> Path:
        return self.root / page.book / "pages" / f"{page.slug}.html.gz"

    def read_page(self, page: Page) -> str:
        return gzip.decompress(self.page_path(page).read_bytes()).decode("utf-8")

    def write_page(self, page: Page, body: bytes) -> None:
        write_atomic(self.page_path(page), gzip.compress(body))

    def read_manifest(self, book: str) -> list[Page]:
        data = json.loads(self.manifest_path(book).read_text(encoding="utf-8"))
        return [Page(book, p["slug"], p["url"]) for p in data["pages"]]

    def write_manifest(self, book: str, pages: list[Page]) -> None:
        data = {
            "site": "erisale",
            "book": book,
            "sitemap": SITEMAP_URL,
            "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "pages": [{"slug": p.slug, "url": p.url} for p in pages],
        }
        write_atomic(self.manifest_path(book),
                      json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8"))


# ---------------------------------------------------------------- indirme

def fetch_book(book: str, archive: Archive, client: PoliteClient | None = None, *,
               refresh: bool = False, log: Callable[[str], None] = print) -> list[Page]:
    """Kitabın bütün bölüm sayfalarını indirir. Diskte olanları atlar, böylece kaldığı yerden devam eder."""
    client = client or PoliteClient(REQUEST_DELAY)
    if refresh or not archive.sitemap_path.exists():
        log(f"sitemap indiriliyor: {SITEMAP_URL}")
        write_atomic(archive.sitemap_path, client.get(SITEMAP_URL))
    pages = [p for p in parse_sitemap(archive.sitemap_path.read_text(encoding="utf-8")) if p.book == book]
    if not pages:
        raise ValueError(f"erisale sitemap'inde '{book}' kitabına ait sayfa yok")

    todo = [p for p in pages if refresh or not archive.page_path(p).exists()]
    log(f"{book}: {len(pages)} sayfa, indirilecek {len(todo)}")
    for n, page in enumerate(todo, 1):
        archive.write_page(page, client.get(page.url))
        log(f"  [{n}/{len(todo)}] {page.slug}")
    archive.write_manifest(book, pages)
    return pages


# ---------------------------------------------------------------- birleştirme ve doğrulama

@dataclass
class PageSummary:
    slug: str
    url: str
    breadcrumb: list[str]
    first_block: int | None
    last_block: int | None


@dataclass
class BookBlocks:
    """Bir kitabın bütün sayfalarından birleştirilmiş, sayfa bilgisi ayıklanmış bloklar."""
    book: str
    pages: list[PageSummary] = field(default_factory=list)
    blocks: list[dict] = field(default_factory=list)
    # Kitabın ilk bloğu. Kitap başlığı (blockIndex 0) hiçbir bölüm sayfasında sunulmaz, bu yüzden 1 beklenir.
    first_index: int | None = None
    missing: list[int] = field(default_factory=list)    # ilk ve son blok arasında hiçbir sayfada bulunmayanlar
    conflicts: list[int] = field(default_factory=list)  # iki sayfada farklı içerikle geçenler

    def to_json(self) -> dict:
        return {
            "site": "erisale",
            "book": self.book,
            "pages": [vars(p) for p in self.pages],
            "first_index": self.first_index,
            "missing": self.missing,
            "conflicts": self.conflicts,
            "blocks": self.blocks,
        }


def merge_pages(book: str, pages: list[tuple[Page, str]]) -> BookBlocks:
    """(sayfa, html) çiftlerini kitap sırasındaki tek blok listesine çevirir."""
    result = BookBlocks(book)
    merged: dict[int, dict] = {}
    for page, html in pages:
        blocks = extract_blocks(html)
        result.pages.append(PageSummary(
            slug=page.slug, url=page.url, breadcrumb=extract_breadcrumb(html),
            first_block=blocks[0]["blockIndex"] if blocks else None,
            last_block=blocks[-1]["blockIndex"] if blocks else None,
        ))
        for block in blocks:
            index = block["blockIndex"]
            if index not in merged:
                merged[index] = {"index": index, "section": block["sectionIndex"],
                                 "page": page.slug, "content": block["content"]}
            elif merged[index]["content"] != block["content"]:
                result.conflicts.append(index)

    if merged:
        result.first_index = min(merged)
        result.missing = sorted(set(range(min(merged), max(merged) + 1)) - merged.keys())
    result.blocks = [merged[i] for i in sorted(merged) if merged[i]["content"]["type"] != _PAGE_BLOCK]
    return result


def load_book(book: str, archive: Archive) -> BookBlocks:
    pages = archive.read_manifest(book)
    return merge_pages(book, [(page, archive.read_page(page)) for page in pages])
