"""Eserlerin kontrol listesi: her eserin hangi aşamada olduğu, koleksiyon başına ayrı dosyada.

Liste `docs/eserler/<alan>-<koleksiyon>.md` dosyalarındadır (`data/` git'e girmediği için orada durmaz);
kökteki `ESERLER.md` yalnızca dizindir.

Tefsir, hadis ve klasik eserlerin dosyaları üç bölümlüdür (PLANLAR.md E1, 2026-11-09): (a) eklenenler buradan
üretilir; (b) eklenmesi çok iyi olacaklar ve (c) aklımızda bulunsun elle tutulur. Elle tutulan kısım `MANUAL_MARK`
satırının altıdır, yeniden üretimde korunur. Hadis kitapları katalogda değil, `data/library/hadis/kutub/`
dosyalarından okunur.

Kullanım:
    uv run python -m risale_mcp.checklist

Durum diskten okunur, elle tutulmaz: ham veri `data/raw/<site>/<kitap>/manifest.json`,
erisale eksikleri `data/interim/erisale/<kitap>.blocks.json`, ayrıştırılmış eser
`Work.book_path`. Her aşamadan sonra yeniden üretilir.
"""

import json
from dataclasses import dataclass

from pathlib import Path

from risale_mcp.catalog import WORKS, Collection, Group, Site, Status, Work
from risale_mcp.catalog import excluded
from risale_mcp.paths import INTERIM_DIR, LIBRARY_DIR, QURAN_PATH, RAW_DIR, ROOT

INDEX_PATH = ROOT / "ESERLER.md"
OUT_DIR = ROOT / "docs" / "eserler"

COLLECTION_TITLES = {
    Collection.KULLIYAT: "Risale-i Nur Külliyatı",
    Collection.ILGILI: "Risale-i Nur ile ilgili kaynaklar",
    Collection.TEFSIR: "Müfessirlerin eserleri",
}

GROUP_TITLES = {
    Group.ESKI_SAID: "Eski Said dönemi eserleri",
    Group.ANA_CILT: "Risale-i Nur ana ciltleri",
    Group.MECMUA: "Mecmualar",
    Group.HIZB: "Hizbler ve dualar",
    Group.OSMANLICA: "Osmanlıca eserler",
    Group.TEFSIR: "Müfessirlerin eserleri",
}

DONE, PARTIAL, TODO, NONE, PAUSED = "✅", "⚠️", "⬜", "❌", "⏸️"

# Üç bölümlü dosyalar: (a) üretilir, (b) ve (c) elle
MANUAL_MARK = "<!-- Bu satırın altı elle tutulur; checklist yeniden üretirken korur. -->"
MANUAL_DEFAULT = """
## (b) Eklenmesi çok iyi olacaklar

Her eser için: nüsha (OpenITI sürümü, muhakkik), E2 ölçütünün üç şartı (Risale'de anılma ya da künye, açık izin ve
nüsha, gerçekçi soru), gerekçe.

## (c) Aklımızda bulunsun

Şimdilik eklenmese de olur; neden beklediği yazılır.
"""
KUTUB_DIR = LIBRARY_DIR / "hadis" / "kutub"
HADIS_PATH = OUT_DIR / "hadis.md"
KLASIK_PATH = OUT_DIR / "klasik.md"
PARTED = {Collection.TEFSIR}
# Kütüb-i Sitte ve Muvatta (`hadis_kutub.py`), sonra öbürleri (`hadis_openiti.SPECS`) bu sırayla
KUTUB_AUTHORS = {"bukhari": "Buhârî", "muslim": "Müslim", "abudawud": "Ebû Dâvûd", "tirmidhi": "Tirmizî",
                 "nasai": "Nesâî", "ibnmajah": "İbn Mâce", "malik": "İmam Mâlik"}
SIYER = ("sifa", "delail")


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
    if work.source.site is Site.OPENITI:          # OpenITI dosyaları düzdür: data/raw/openiti/<anahtar>.txt
        return f"{DONE} indirildi" if (RAW_DIR / "openiti" / f"{work.source.book}.txt").exists() else f"{TODO} indirilmedi"
    folder = RAW_DIR / "nurpedia" / "metin" if work.source.site is Site.NURPEDIA else RAW_DIR / work.source.site
    if not (folder / work.source.book / "manifest.json").exists():
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


def render(table: list[Row], title: str = COLLECTION_TITLES[Collection.KULLIYAT], parted: bool = False) -> str:
    raw_done = sum(r.raw.startswith((DONE, PARTIAL)) for r in table)
    parsed = sum(r.parsed.startswith(DONE) for r in table)
    missing = [r.work.title for r in table if r.work.source is None]
    lines = [
        f"# {title}: kontrol listesi",
        "",
        *_header(parted, "> Eserlerin listesi ve kaynakları: `src/risale_mcp/catalog/`."),
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
        lines += ["", f"{'###' if parted else '##'} {heading}", "",
                  "| # | Eser | Kaynak | Ham veri | Ayrıştırma | Not |",
                  "|---:|---|---|---|---|---|"]
        for r in (r for r in table if r.work.group is group):
            n += 1
            w = r.work
            source = f"{w.source.site}/{w.source.book}" if w.source else "—"
            note = " ".join(filter(None, ["**Doğrulanacak.**" if w.status is Status.VERIFY else "", w.note]))
            lines.append(f"| {n} | {w.title} | `{source}` | {r.raw} | {r.parsed} | {note} |")
    if parted:
        lines += _excluded()
    return "\n".join(lines) + "\n"


def _header(parted: bool, *extra: str) -> list[str]:
    command = "`uv run python -m risale_mcp.checklist`"
    if not parted:
        return [f"> Bu dosya {command} ile üretilir; elle düzenlemeyin.", *extra, ""]
    return [f"> (a) {command} ile üretilir, elle düzenlemeyin; (b) ve (c) elle tutulur, yeniden üretimde korunur.",
            *extra, "> Eser ekleme ölçütü ve sıra: `PLANLAR.md` E2.", "", "## (a) Eklenenler", ""]


def _excluded() -> list[str]:
    reasons = sorted(set(excluded.OPENITI.values()))
    return ["", "Kaynak alınmaz (`catalog/excluded.py`, kullanıcının kararı): " + "; ".join(reasons) + "."]


def _edition(source: dict) -> str:
    ed = source.get("edition") or {}
    return "، ".join(v for k in ("editor", "publisher", "place", "edition", "year") if (v := (ed.get(k) or "").strip(" -")))


def render_hadis() -> str:
    """Hadis kitapları: katalogda değil, kütüphanedeki kitap dosyalarından."""
    from risale_mcp.hadis_openiti import SPECS

    order = [*KUTUB_AUTHORS, *SPECS]
    books = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in KUTUB_DIR.glob("*.json")}
    groups = (("Kütüb-i Sitte ve Muvatta", [b for b in KUTUB_AUTHORS if b in books]),
              ("Öbür hadis kitapları", [b for b in SPECS if b in books and b not in SIYER]),
              ("Siyer ve delâil", [b for b in SIYER if b in books]))
    lines = ["# Hadis kitapları: kontrol listesi", "",
             *_header(True, "> Kitaplar: `data/library/hadis/kutub/` (`hadis_kutub.py`, `hadis_openiti.py`); "
                            "sunucusu `hadis` profili."),
             f"- **Kütüphanede:** {len(books)} kitap, "
             + f"{sum(len(b.get('hadiths', [])) for b in books.values()):,}".replace(",", ".") + " birim.", ""]
    n = 0
    for heading, keys in groups:
        if not keys:
            continue
        lines += [f"### {heading}", "", "| # | Kitap | Müellif | Nüsha | Baskı | Birim | Ayrı katman |",
                  "|---:|---|---|---|---|---:|---|"]
        for key in keys:
            n += 1
            book, src = books[key], books[key]["source"]
            spec = SPECS.get(key)
            author = KUTUB_AUTHORS.get(key) or src.get("author") or (spec.author if spec else "")
            parts = (src.get("path") or src.get("file") or "").rsplit("/", 1)[-1].split(".")
            version = parts[2] if len(parts) > 2 else parts[-1]     # yazar.eser.SÜRÜM[.completed|.mARkdown]
            unit = "paragraf" if spec and spec.unit == "paragraph" else "rivayet" if spec and spec.unit == "isnad" else "hadis"
            count = f"{len(book.get('hadiths', [])):,}".replace(",", ".")
            layer = spec.layer_by if spec and spec.layer_by else ""
            lines.append(f"| {n} | {book['title']} | {author} | `{version}` | {_edition(src)} | {count} {unit} | {layer} |")
        lines.append("")
    unknown = sorted(set(books) - set(order))
    if unknown:
        lines += [f"Sırası tanımsız kitap: {', '.join(unknown)}.", ""]
    return "\n".join(lines).rstrip("\n") + "\n"


def render_klasik() -> str:
    """Klasik eserler (belâgat, kelâm, tasavvuf, siyer): henüz koleksiyonu yok (PLANLAR.md E2)."""
    return "\n".join(["# Klasik eserler: kontrol listesi", "",
                      *_header(True, "> Koleksiyonu henüz yok; ilk eser eklenince katalogdan üretilir."),
                      "Henüz eklenen eser yok.", *_excluded()]) + "\n"


def write_parted(path: Path, generated: str) -> None:
    """Üretilen (a) kısmını yazar, işaretin altındaki elle tutulan kısmı korur (yoksa boş iskelet)."""
    manual = MANUAL_DEFAULT
    if path.exists() and MANUAL_MARK in (old := path.read_text(encoding="utf-8")):
        manual = old.split(MANUAL_MARK, 1)[1]
    path.write_text(f"{generated}\n{MANUAL_MARK}\n{manual}", encoding="utf-8")


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
    hadis = len(list(KUTUB_DIR.glob("*.json")))
    lines.append(f"| Hadis kitapları | {hadis} | {hadis} | [liste]({HADIS_PATH.relative_to(ROOT)}) |")
    lines.append(f"| Klasik eserler | 0 | 0 | [liste]({KLASIK_PATH.relative_to(ROOT)}) |")
    if QURAN_PATH.exists():
        lines.append("| Kur'ân-ı Kerîm | 114 sûre | ✅ | `data/library/kuran/` |")
    return "\n".join(lines) + "\n"


def main() -> None:
    table = rows()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for collection, title in COLLECTION_TITLES.items():
        if chosen := [r for r in table if r.work.collection is collection]:
            path = list_path(collection)
            if collection in PARTED:
                write_parted(path, render(chosen, title, parted=True))
            else:
                path.write_text(render(chosen, title), encoding="utf-8")
            print(f"yazıldı: {path.relative_to(ROOT)}")
    for path, text in ((HADIS_PATH, render_hadis()), (KLASIK_PATH, render_klasik())):
        write_parted(path, text)
        print(f"yazıldı: {path.relative_to(ROOT)}")
    INDEX_PATH.write_text(render_index(table), encoding="utf-8")
    print(f"yazıldı: {INDEX_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
