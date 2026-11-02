"""Aşama 13.2: risalelerin yazıldığı tarih, yer ve dil.

Kullanım:
    uv run python -m risale_mcp.books.telif     # docs/telif-tablosu.md inceleme tablosunu üretir

Asıl liste `telif.json`'dur ve elle düzenlenir: eser JSON'ları her `build`'de yeniden üretildiği için orada duramaz.
`sources` kaynak anahtarını adına ve adresine bağlar; `written` bölüm kimliğini kayda:
    date, place, language   tarih serbest metindir ("1936", "1943–1944", "1938 veya 1942")
    estimated               kaynak "tahminen" diyor
    status                  tarih yerine: "telif edilmedi", "tarih verilmedi"
    source, note            kaynağın anahtarı; ayrılan kaynaklar ve karar notu
Tarih kuralı ve karşılaştırmalar: `docs/telif-tarihleri-plani.md`. Liste yalnız bu bilgiyi taşır, metne dokunmaz:
cümle kimlikleri ve vektörler değişmez. Dosyada olup eserde bulunmayan kimlik kurulumu durdurur.
"""

import json
from functools import cache
from pathlib import Path

PATH = Path(__file__).with_name("telif.json")


@cache
def load() -> dict:
    return json.loads(PATH.read_text(encoding="utf-8"))


def apply(book: dict, listing: dict | None = None) -> int:
    """Eserin düğümlerine `written` yazar; kaç düğüme yazıldığını döndürür."""
    listing = listing or load()
    work = book["work"]
    entries = {key: entry for key, entry in listing["written"].items() if key == work or key.startswith(f"{work}/")}
    nodes = {node["id"]: node for node in book["outline"]}
    if unknown := sorted(set(entries) - set(nodes)):
        raise ValueError(f"telif.json: {work} eserinde olmayan bölüm: {unknown}")
    for key, entry in entries.items():
        nodes[key]["written"] = entry | {"source": listing["sources"][entry["source"]]["name"]}
    return len(entries)


def table(listing: dict, refs: dict[str, str]) -> str:
    """Kimlik sırası `refs` sırasıdır (kitap sırası); kitapta olmayan kimlik burada da hata verir."""
    lines = ["# Telif tarihleri", "",
             "> `uv run python -m risale_mcp.books.telif` ile `src/risale_mcp/books/telif.json` listesinden üretilir; "
             "elle düzenlemeyin. \"~\" tahmindir.", "",
             "| Bölüm | Tarih | Yer | Dil | Kaynak | Not |", "|---|---|---|---|---|---|"]
    written = listing["written"]
    for key in [k for k in refs if k in written]:
        entry = written[key]
        date = entry.get("status") or ("~" if entry.get("estimated") else "") + entry["date"]
        lines.append(f"| {refs[key]} | {date} | {entry.get('place', '')} | {entry.get('language', '')} "
                     f"| {listing['sources'][entry['source']]['name']} | {entry.get('note', '')} |")
    return "\n".join(lines) + "\n"


def main() -> None:
    from risale_mcp.db import connect
    from risale_mcp.paths import ROOT
    rows = connect().execute("SELECT n.id, n.ref FROM nodes n JOIN works w ON w.slug = n.work ORDER BY w.ord, n.ord")
    (ROOT / "docs" / "telif-tablosu.md").write_text(table(load(), dict(tuple(r) for r in rows)), encoding="utf-8")
    print("yazıldı: docs/telif-tablosu.md")


if __name__ == "__main__":
    main()
