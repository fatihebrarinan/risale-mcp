"""Eserlerin kontrol listesi: her eserin hangi aşamada olduğu, koleksiyon başına ayrı dosyada.

Liste `docs/eserler/<alan>-<koleksiyon>.md` dosyalarındadır (`data/` git'e girmediği için orada durmaz);
kökteki `ESERLER.md` yalnızca dizindir.

Kullanım:
    uv run python -m risale_mcp.checklist

Durum diskten okunur, elle tutulmaz: ham veri `data/raw/<site>/<kitap>/manifest.json`,
erisale eksikleri `data/interim/erisale/<kitap>.blocks.json`, ayrıştırılmış eser
`Work.book_path`. Her aşamadan sonra yeniden üretilir.
"""

import json
from dataclasses import dataclass

from risale_mcp.catalog import WORKS, Collection, Group, Site, Status, Work
from risale_mcp.paths import INTERIM_DIR, QURAN_PATH, RAW_DIR, ROOT

INDEX_PATH = ROOT / "ESERLER.md"
OUT_DIR = ROOT / "docs" / "eserler"

COLLECTION_TITLES = {
    Collection.KULLIYAT: "Risale-i Nur Külliyatı",
    Collection.ILGILI: "Risale-i Nur ile ilgili kaynaklar",
}

GROUP_TITLES = {
    Group.ESKI_SAID: "Eski Said dönemi eserleri",
    Group.ANA_CILT: "Risale-i Nur ana ciltleri",
    Group.MECMUA: "Mecmualar",
    Group.HIZB: "Hizbler ve dualar",
    Group.OSMANLICA: "Osmanlıca eserler",
}

DONE, PARTIAL, TODO, NONE, PAUSED = "✅", "⚠️", "⬜", "❌", "⏸️"


@dataclass(frozen=True)
class Row:
    work: Work
    raw: str     # ham verinin durumu
    parsed: str  # Aşama 2: eser JSON'u


def _raw_status(work: Work) -> str:
    if work.source is None:
        return f"{NONE} kaynak bulunamadı"
    if work.status is Status.DEFERRED:
        return f"{PAUSED} ertelendi"
    if not (RAW_DIR / work.source.site / work.source.book / "manifest.json").exists():
        return f"{TODO} indirilmedi"
    if work.source.site is Site.ERISALE and not work.source.sections:
        blocks = INTERIM_DIR / "erisale" / f"{work.source.book}.blocks.json"
        missing = json.loads(blocks.read_text(encoding="utf-8"))["missing"] if blocks.exists() else []
        if missing:
            path = work.book_path
            gaps = json.loads(path.read_text(encoding="utf-8"))["gaps"] if path.exists() else True
            if not gaps:                       # ayrıştırıcı tamamladı (Sikke'de başlık yol bilgisinden, metin risaleoku'dan)
                return f"{DONE} indirildi ({len(missing)} blok tamamlandı)"
            return f"{PARTIAL} {len(missing)} blok sitede yok"
    return f"{DONE} indirildi"


def _parsed_status(work: Work) -> str:
    path = work.book_path
    if not path.exists():
        return TODO
    book = json.loads(path.read_text(encoding="utf-8"))
    mains = [p for p in book["paragraphs"] if p["kind"] != "hasiye"]
    status = f"{DONE} {len(book['outline'])} düğüm, {len(mains)} paragraf, {len(book.get('sentences', []))} cümle"
    mapped = sum("source" in p for p in mains)
    if mapped:
        status += f"; %{100 * mapped // len(mains)} ana cilde eşlendi"
    return status


def rows() -> list[Row]:
    return [Row(w, _raw_status(w), _parsed_status(w)) for w in WORKS]


def list_path(collection: Collection):
    return OUT_DIR / f"{collection.value.replace('/', '-')}.md"


def render(table: list[Row], title: str = COLLECTION_TITLES[Collection.KULLIYAT]) -> str:
    raw_done = sum(r.raw.startswith((DONE, PARTIAL)) for r in table)
    parsed = sum(r.parsed.startswith(DONE) for r in table)
    missing = [r.work.title for r in table if r.work.source is None]
    lines = [
        f"# {title}: kontrol listesi",
        "",
        "> Bu dosya `uv run python -m risale_mcp.checklist` ile üretilir; elle düzenlemeyin.",
        "> Eserlerin listesi ve kaynakları: `src/risale_mcp/catalog/`.",
        "",
        f"- **Ham veri:** {raw_done}/{len(table)} eser indirildi.",
        f"- **Ayrıştırma:** {parsed}/{len(table)} eser.",
        f"- **Kaynağı bulunamayan:** {', '.join(missing) or 'yok'}.",
        "",
        f"İşaretler: {DONE} tamam · {PARTIAL} kısmen · {TODO} yapılmadı · {NONE} kaynak yok · {PAUSED} ertelendi",
    ]
    n = 0
    for group, heading in GROUP_TITLES.items():
        if not any(r.work.group is group for r in table):
            continue
        lines += ["", f"## {heading}", "",
                  "| # | Eser | Kaynak | Ham veri | Ayrıştırma | Not |",
                  "|---:|---|---|---|---|---|"]
        for r in (r for r in table if r.work.group is group):
            n += 1
            w = r.work
            source = f"{w.source.site}/{w.source.book}" if w.source else "—"
            note = " ".join(filter(None, ["**Doğrulanacak.**" if w.status is Status.VERIFY else "", w.note]))
            lines.append(f"| {n} | {w.title} | `{source}` | {r.raw} | {r.parsed} | {note} |")
    return "\n".join(lines) + "\n"


def render_index(table: list[Row]) -> str:
    lines = [
        "# Eserler",
        "",
        "> Bu dosya `uv run python -m risale_mcp.checklist` ile üretilir; elle düzenlemeyin.",
        "",
        "| Alan | Eser | Ayrıştırılan | Liste |",
        "|---|---:|---:|---|",
    ]
    for collection, title in COLLECTION_TITLES.items():
        chosen = [r for r in table if r.work.collection is collection]
        parsed = sum(r.parsed.startswith(DONE) for r in chosen)
        link = f"[liste]({list_path(collection).relative_to(ROOT)})" if chosen else "henüz eser yok"
        lines.append(f"| {title} | {len(chosen)} | {parsed} | {link} |")
    if QURAN_PATH.exists():
        lines.append("| Kur'ân-ı Kerîm | 114 sûre | ✅ | `data/library/kuran/` |")
    return "\n".join(lines) + "\n"


def main() -> None:
    table = rows()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for collection, title in COLLECTION_TITLES.items():
        if chosen := [r for r in table if r.work.collection is collection]:
            path = list_path(collection)
            path.write_text(render(chosen, title), encoding="utf-8")
            print(f"yazıldı: {path.relative_to(ROOT)}")
    INDEX_PATH.write_text(render_index(table), encoding="utf-8")
    print(f"yazıldı: {INDEX_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
