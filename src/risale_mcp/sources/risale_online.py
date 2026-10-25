"""risale.online: Hayrat baskısı, JSON API.

    /risale-api/eserler                                   kitap listesi (id, slug, sayfa_sayisi)
    /risale-api/fihrist?eserid=N                          üst düzey fihrist
    /risale-api/paragraf?eserid=N&ilksayfa=A&sonsayfa=B&yazi=latince
                                                          paragraflar (sitenin kendisi 8'er sayfa ister)

Ham arşiv (`data/raw/risale_online/`):
    eserler.json
    <kitap>/manifest.json, fihrist.json, paragraf/<ilk>-<son>.json

robots.txt `/risale-api` yolunu yasaklamaz.
"""

import json
from pathlib import Path
from typing import Callable

from risale_mcp.sources.archive import fetch_cached, read_raw, write_manifest
from risale_mcp.sources.http import PoliteClient

API_URL = "https://risale.online/risale-api"
PAGES_PER_REQUEST = 8


def _chunks(page_count: int) -> list[tuple[int, int]]:
    return [(first, min(first + PAGES_PER_REQUEST - 1, page_count))
            for first in range(1, page_count + 1, PAGES_PER_REQUEST)]


def _chunk_path(root: Path, book: str, first: int, last: int) -> Path:
    return root / book / "paragraf" / f"{first:04d}-{last:04d}.json"


def book_meta(root: Path, client: PoliteClient, book: str, refresh: bool = False) -> dict:
    books = json.loads(fetch_cached(root / "eserler.json", f"{API_URL}/eserler", client, refresh))
    meta = next((b for b in books if b["slug"] == book), None)
    if meta is None:
        raise ValueError(f"risale.online'da '{book}' adlı kitap yok")
    if not meta["metin_var_mi"]:
        raise ValueError(f"risale.online'da '{book}' kitabının metni yok")
    return meta


def fetch_book(book: str, root: Path, client: PoliteClient, *,
               refresh: bool = False, log: Callable[[str], None] = print) -> None:
    meta = book_meta(root, client, book, refresh)
    book_id, page_count = meta["id"], meta["sayfa_sayisi"]
    fetch_cached(root / book / "fihrist.json", f"{API_URL}/fihrist?eserid={book_id}", client, refresh)

    chunks = _chunks(page_count)
    log(f"{book}: {page_count} sayfa, {len(chunks)} istek")
    for n, (first, last) in enumerate(chunks, 1):
        url = f"{API_URL}/paragraf?eserid={book_id}&ilksayfa={first}&sonsayfa={last}&yazi=latince"
        fetch_cached(_chunk_path(root, book, first, last), url, client, refresh)
        log(f"  [{n}/{len(chunks)}] sayfa {first}-{last}")
    write_manifest(root / book / "manifest.json", site="risale_online", book=book,
                   book_id=book_id, page_count=page_count)


def read_fihrist(book: str, root: Path) -> list[dict]:
    return json.loads(read_raw(root / book / "fihrist.json"))


def load_paragraphs(book: str, root: Path) -> list[dict]:
    manifest = json.loads((root / book / "manifest.json").read_text(encoding="utf-8"))
    paragraphs = []
    for first, last in _chunks(manifest["page_count"]):
        paragraphs.extend(json.loads(read_raw(_chunk_path(root, book, first, last))))
    return paragraphs


def check_book(book: str, root: Path) -> tuple[list[str], bool]:
    """Her sayfada en az bir paragraf olmalı. (rapor satırları, sorunsuz mu)"""
    manifest = json.loads((root / book / "manifest.json").read_text(encoding="utf-8"))
    paragraphs = load_paragraphs(book, root)
    pages = {int(p["sayfa"]) for p in paragraphs}
    empty = sorted(set(range(1, manifest["page_count"] + 1)) - pages)
    fihrist = json.loads(read_raw(root / book / "fihrist.json"))
    lines = [
        f"risale_online/{book}: {manifest['page_count']} sayfa, {len(paragraphs)} paragraf, "
        f"{len(fihrist)} fihrist girdisi",
        f"  paragrafsız sayfa: {len(empty)} {empty[:20]}",
    ]
    return lines, not empty
