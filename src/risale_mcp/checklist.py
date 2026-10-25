"""Eserlerin kontrol listesi: katalogdaki her eserin hangi aşamada olduğunu `ESERLER.md`'ye yazar.

Kullanım:
    uv run python -m risale_mcp.checklist

Durum diskten okunur, elle tutulmaz: ham veri `data/raw/<site>/<kitap>/manifest.json`,
erisale eksikleri `data/interim/erisale/<kitap>.blocks.json`, ayrıştırılmış eser
`data/books/<eser>.json`. Her aşamadan sonra yeniden üretilir.
"""

import json
from dataclasses import dataclass

from risale_mcp.catalog import WORKS, Group, Site, Status, Work
from risale_mcp.paths import BOOKS_DIR, INTERIM_DIR, RAW_DIR, ROOT

OUT_PATH = ROOT / "ESERLER.md"

GROUP_TITLES = {
    Group.ESKI_SAID: "Eski Said dönemi eserleri",
    Group.ANA_CILT: "Risale-i Nur ana ciltleri",
    Group.MECMUA: "Mecmualar",
    Group.HIZB: "Hizbler",
}

DONE, PARTIAL, TODO, NONE, PAUSED = "✅", "⚠️", "⬜", "❌", "⏸️"


@dataclass(frozen=True)
class Row:
    work: Work
    raw: str     # ham verinin durumu
    parsed: str  # Aşama 2: data/books/<eser>.json


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
            return f"{PARTIAL} {len(missing)} blok sitede yok"
    return f"{DONE} indirildi"


def _parsed_status(work: Work) -> str:
    path = BOOKS_DIR / f"{work.slug}.json"
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


def render(table: list[Row]) -> str:
    raw_done = sum(r.raw.startswith((DONE, PARTIAL)) for r in table)
    parsed = sum(r.parsed.startswith(DONE) for r in table)
    missing = [r.work.title for r in table if r.work.source is None]
    lines = [
        "# Eserler kontrol listesi",
        "",
        "> Bu dosya `uv run python -m risale_mcp.checklist` ile üretilir; elle düzenlemeyin.",
        "> Eserlerin listesi ve kaynakları: `src/risale_mcp/catalog.py`.",
        "",
        f"- **Ham veri:** {raw_done}/{len(table)} eser indirildi.",
        f"- **Ayrıştırma:** {parsed}/{len(table)} eser.",
        f"- **Kaynağı bulunamayan:** {', '.join(missing) or 'yok'}.",
        "",
        f"İşaretler: {DONE} tamam · {PARTIAL} kısmen · {TODO} yapılmadı · {NONE} kaynak yok · {PAUSED} ertelendi",
    ]
    n = 0
    for group, title in GROUP_TITLES.items():
        lines += ["", f"## {title}", "",
                  "| # | Eser | Kaynak | Ham veri | Ayrıştırma | Not |",
                  "|---:|---|---|---|---|---|"]
        for r in (r for r in table if r.work.group is group):
            n += 1
            w = r.work
            source = f"{w.source.site}/{w.source.book}" if w.source else "—"
            note = " ".join(filter(None, ["**Doğrulanacak.**" if w.status is Status.VERIFY else "", w.note]))
            lines.append(f"| {n} | {w.title} | `{source}` | {r.raw} | {r.parsed} | {note} |")
    return "\n".join(lines) + "\n"


def main() -> None:
    OUT_PATH.write_text(render(rows()), encoding="utf-8")
    print(f"yazıldı: {OUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
