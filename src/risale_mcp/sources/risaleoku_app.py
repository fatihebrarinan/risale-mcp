"""risaleoku.com'un yeni uygulaması (2026-10): katalog ve kitap dosyaları.

Site WebAssembly uygulamasına döndü; eski `/oku` ve `/ajax` adresleri kapandı (eski ham veri `risaleoku`
klasöründe, karşılaştırma için durur). Uygulama iki şey ister:

    /api/v1/content/changes?after=<seq>&limit=500   bütün katalog: raflar, kitaplar, dosyalarının adresi ve SHA-256'sı
    /f/<sha256>.<uzantı>.gz                         kitabın `text`, `toc`, `footnotes` dosyası

Silinen kayıtların `data` alanı boştur. Katalogdaki `sha256` dosyanın açılmış hâlinindir, `size` sıkıştırılmışının.

Ham arşiv (`data/raw/risaleoku_app/`):
    catalog.json, meal/<parça>.json.gz, <kitap>/text.txt.gz, toc.txt.gz, footnotes.txt.gz, manifest.json

Metindeki `~…|n@` satırlarının `n`'i Türkçe meal kaydının numarasıdır: meal dosyaları `[{"id": "300", "meal": "…"}]`.
"""

import hashlib
import json
from pathlib import Path
from typing import Callable

from risale_mcp.sources.archive import fetch_cached, read_raw, write_atomic, write_manifest
from risale_mcp.sources.http import PoliteClient

BASE_URL = "https://risaleoku.com"
PAGE_SIZE = 500


def fetch_catalog(root: Path, client: PoliteClient, *, refresh: bool = False) -> list[dict]:
    """Katalog akışını baştan sona indirip `catalog.json`'a yazar (kayıtlar, akış sırasıyla)."""
    path = root / "catalog.json"
    if path.exists() and not refresh:
        return json.loads(path.read_text(encoding="utf-8"))
    records, after = [], 0
    while True:
        body = client.get(f"{BASE_URL}/api/v1/content/changes?after={after}&limit={PAGE_SIZE}")
        page = json.loads(body)
        records += page["records"]
        if not page.get("has_more"):
            break
        after = page["next_cursor"]
    write_atomic(path, json.dumps(records, ensure_ascii=False).encode("utf-8"))
    return records


def books_by_key(records: list[dict]) -> dict[str, dict]:
    return {r["data"]["key"]: r["data"] for r in records if r["kind"] == "book" and r["data"]}


def shelf_books(records: list[dict], shelf_id: int) -> list[str]:
    books = [b for b in books_by_key(records).values() if b["shelf_id"] == shelf_id]
    return [b["key"] for b in sorted(books, key=lambda b: b["sort"])]


def fetch_meals(root: Path, client: PoliteClient, *, refresh: bool = False) -> None:
    records = fetch_catalog(root, client)
    meal = next(r["data"] for r in records if r["kind"] == "meal" and r["data"])
    for name, file in meal["files"].items():
        fetch_cached(root / "meal" / f"{name}.gz", file["url"], client, refresh)


def load_meals(root: Path) -> dict[str, str]:
    """Meal numarası -> meal metni (bütün parçalar)."""
    meals: dict[str, str] = {}
    for path in (root / "meal").glob("*.json.gz"):
        meals |= {str(m["id"]): m["meal"] for m in json.loads(read_raw(path))}
    return meals


def _file_path(root: Path, key: str, name: str) -> Path:
    return root / key / f"{name}.txt.gz"


def fetch_book(key: str, root: Path, client: PoliteClient, *,
               refresh: bool = False, log: Callable[[str], None] = print) -> None:
    book = books_by_key(fetch_catalog(root, client))[key]
    for name, file in book["files"].items():
        if file:
            fetch_cached(_file_path(root, key, name), file["url"], client, refresh)
    write_manifest(root / key / "manifest.json", site="risaleoku_app", book=key, version=book["version"],
                   files={name: file["sha256"] for name, file in book["files"].items() if file})
    log(f"{key}: {book['title']} (v{book['version']})")


def check_book(key: str, root: Path) -> tuple[list[str], bool]:
    """Her dosya diskte ve özeti katalogla aynı olmalı. (rapor satırları, sorunsuz mu)"""
    manifest = json.loads((root / key / "manifest.json").read_text(encoding="utf-8"))
    bad, chars = [], 0
    for name, sha256 in manifest["files"].items():
        path = _file_path(root, key, name)
        data = read_raw(path) if path.exists() else b""
        chars += len(data)
        if hashlib.sha256(data).hexdigest() != sha256:
            bad.append(name)
    return [f"risaleoku_app/{key}: {len(manifest['files'])} dosya, {chars:,} bayt, bozuk: {bad}"], not bad
