"""Eserin baskı kaydı (H3): metnin hangi dijital nüshadan, hangi baskıdan, ne zaman alındığı.

Kayıt ham verinin kendi bilgisinden kurulur, tahmin edilmez: indirme manifestosu (`data/raw/<kaynak>/<kitap>/
manifest.json`: adres, indirme zamanı, dosya özeti) ve risaleoku kataloğunun raf kayıtları
(`catalog.json`: kitap → raf → raf grubu). Kaynak bir bilgiyi vermiyorsa alan yoktur. Raf grubu her zaman yayınevi
değildir ("Envar Neşriyat - Türkçe" ama "Other Languages", "Evrad ve Muhtelif Kitaplar"): kaynağın adıyla
`shelf_group` olarak durur, yayınevi diye yorumlanmaz; rafın alt başlığı çoğu yerde baskıyı söyler (`shelf_note`).
Kişiler (muhakkik, mütercim, derleyen) katalogdadır (`Work`), burada tekrarlanmaz.

`build_db` her eserin kaydını `works.edition`'a (JSON) yazar; ham veri yalnız yerelde olduğu için sunucuya
veritabanıyla gider.

    {"site": "risaleoku_app", "book": "abed", "shelf_group": "…", "shelf": "Muhtelif Eserler", "shelf_note": "…",
     "files": {"text": "<sha256>"}, "fetched_at": "2026-10-30T13:39:15+00:00",
     "supplements": [{"book": "soz_stg", "shelf_group": "Sözler Neşriyat - Türkçe", "sections": 1}]}
"""

import json
from functools import cache
from pathlib import Path

from risale_mcp.catalog.model import Site, Work
from risale_mcp.paths import RAW_DIR

# Ham verinin klasörü sitenin adından farklı olan kaynaklar
_RAW_NAME = {Site.KESIF: "kesif", Site.KULLANICI: "kullanici"}
_SITE_URL = {Site.ERISALE: "https://www.erisale.com", Site.RISALEOKU_APP: "https://risaleoku.com",
             Site.RISALE_ONLINE: "https://risale.online"}


def _read(path: Path) -> dict | None:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


@cache
def _risaleoku_catalog(raw_dir: Path) -> dict[str, dict]:
    """Kitap anahtarı → raf grubu ve raf (risaleoku kataloğundan)."""
    records = json.loads((raw_dir / "catalog.json").read_text(encoding="utf-8")) if (raw_dir / "catalog.json").exists() else []
    live = [r for r in records if not r.get("deleted")]
    groups = {r["id"]: r["data"] for r in live if r["kind"] == "shelf_group"}
    shelves = {r["id"]: r["data"] for r in live if r["kind"] == "shelf"}
    out = {}
    for r in live:
        if r["kind"] != "book":
            continue
        shelf = shelves.get(r["data"].get("shelf_id"), {})
        group = groups.get(shelf.get("group_id"), {})
        out[r["data"]["key"]] = {k: v for k, v in {
            "shelf_group": group.get("name"), "shelf": shelf.get("name"),
            "shelf_note": " · ".join(x for x in (shelf.get("subtitle"), shelf.get("short_description")) if x) or None,
            "title": r["data"].get("title"), "version": r["data"].get("version")}.items() if v}
    return out


def edition(work: Work, raw_root: Path = RAW_DIR) -> dict | None:
    if work.source is None:
        return None
    site, book = work.source.site, work.source.book
    record: dict = {"site": str(site), "book": book}
    if url := _SITE_URL.get(site):
        record["site_url"] = url
    raw_dir = raw_root / _RAW_NAME.get(site, str(site))
    manifest = _read(raw_dir / book / "manifest.json") or {}
    for key in ("url", "file", "sha1", "files", "fetched_at"):
        if manifest.get(key):
            record[key] = manifest[key]
    if site is Site.RISALEOKU_APP:
        record.update(_risaleoku_catalog(raw_dir).get(book, {}))
    from risale_mcp.books.erisale import SUPPLEMENTS
    if site is Site.ERISALE and work.slug in SUPPLEMENTS:
        app = _risaleoku_catalog(raw_root / str(Site.RISALEOKU_APP))
        books = [s.book for s in SUPPLEMENTS[work.slug]]
        record["supplements"] = [{"site": str(Site.RISALEOKU_APP), "book": b, "sections": books.count(b),
                                  **{k: v for k, v in app.get(b, {}).items() if k in ("shelf_group", "shelf")}}
                                 for b in dict.fromkeys(books)]
    return record
