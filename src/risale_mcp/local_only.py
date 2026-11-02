"""Yerelde olup sunucuda olmayan veriler: `HUSUSI-VERILER.md` listesini üretir.

Kullanım:
    uv run python -m risale_mcp.local_only

İki veritabanını karşılaştırır: `kisisel` profili (hepsi) ve `genel` profili (sunucuya giden kopya).
Durum veriden okunur, elle tutulmaz; `build` sonunda yeniden üretilir. Sunucuda `genel` profilinin veritabanı ve
vektörleri ile `quran.json` durur (bkz. `scripts/deploy.sh`); ham veri, kitap JSON'ları ve ara çıktılar sunucuya gitmez.
"""

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path

from risale_mcp.catalog import WORKS
from risale_mcp.db import connect
from risale_mcp.embeddings import SEARCH_MODEL, units
from risale_mcp.paths import DB_PATH, PUBLIC_DB_PATH, RAW_DIR, ROOT, VECTORS_DIR

OUT_PATH = ROOT / "HUSUSI-VERILER.md"

# data/raw/<klasör> -> ham verinin şimdiki işi. Yeni kaynak klasörü buraya da eklenir (test bunu denetler).
RAW_ROLES = {
    "erisale": "Kullanımda: genel sunucunun birincil kaynağı",
    "risaleoku_app": "Kullanımda: genel sunucu",
    "kesif": "Kullanımda: Ta'likat'ın Türkçesi",
    "tanzil": "Kullanımda: Kur'ân katmanı",
    "risale_online": "Yalnız yerel Siracü'n-Nur (Hayrat)",
    "kullanici": "Rumuzat-ı Semaniye sunucuda; Kızıl İcaz'ın Türkçe PDF'i yalnız yerelde, ayrıştırılmadı (Aşama 17)",
    "rasaelalnour": "Yalnız yerel harekeli Mesnevî; izin vermedi, sunucuya çıkmaz",
    "qurancom": "Yalnız yerel harekeli Mesnevî'deki âyetlerin çözümü",
    "kastamonur": "Telif tarihi sayfaları kullanımda; Nutuk ve Makalat artık risaleoku'dan; izin var (`docs/izinler.md`)",
    "nurpedia": "Ham sayfalar yerelde: hadis işaretleri ve künyeleri (Aşama 14); sunucuya yalnız sonuçları çıkar",
    "sanadset": "Hadis katmanı (Aşama 14): CC BY 4.0, eşleşen rivayetler sunucuya gider",
    "hadith_api": "Hadis katmanı (Aşama 14): Unlicense; âlimlerin dereceleri",
    "risaleoku": "Kullanılmıyor: sitenin kapanan eski sayfaları, karşılaştırma için",
    "yeniasya": "Kullanılmıyor: bozuk kodlu PDF metni, karşılaştırma için",
}


@dataclass(frozen=True)
class Count:
    nodes: int = 0
    paragraphs: int = 0
    sentences: int = 0
    arabic: int = 0

    def __sub__(self, other: "Count") -> "Count":
        return Count(self.nodes - other.nodes, self.paragraphs - other.paragraphs,
                     self.sentences - other.sentences, self.arabic - other.arabic)


def _scalar(conn: sqlite3.Connection, sql: str, *args: object) -> int:
    return conn.execute(sql, args).fetchone()[0]


def count(conn: sqlite3.Connection, work: str | None = None) -> Count:
    """Bütün veritabanının ya da tek eserin sayıları."""
    where, args = (" WHERE work = ?", (work,)) if work else ("", ())
    arabic = ("SELECT count(*) FROM arabic a JOIN paragraphs p ON p.id = a.paragraph_id WHERE p.work = ?", (work,)) \
        if work else ("SELECT count(*) FROM arabic", ())
    return Count(_scalar(conn, f"SELECT count(*) FROM nodes{where}", *args),
                 _scalar(conn, f"SELECT count(*) FROM paragraphs{where}", *args),
                 _scalar(conn, f"SELECT count(*) FROM sentences{where}", *args),
                 _scalar(conn, *arabic[:1], *arabic[1]))


def compare(full: sqlite3.Connection, public: sqlite3.Connection) -> tuple[list[str], list[str]]:
    """(yalnız yereldeki eserler, iki veritabanında metni farklı olan eserler)."""
    local = dict(full.execute("SELECT slug, json_sha1 FROM works"))
    remote = dict(public.execute("SELECT slug, json_sha1 FROM works"))
    return [s for s in local if s not in remote], [s for s, sha1 in remote.items() if local.get(s) != sha1]


def extra_vectors(public: sqlite3.Connection) -> int:
    """Yerel vektörlerden sunucu veritabanında karşılığı olmayanların sayısı."""
    path = VECTORS_DIR / f"{SEARCH_MODEL}.context.keys.json"
    keys = set(json.loads(path.read_text(encoding="utf-8"))) if path.exists() else set()
    return len(keys - {u.key for u in units(public, "context")})


def _size(path: Path) -> str:
    size = sum(p.stat().st_size for p in path.rglob("*") if p.is_file())
    return f"{size / 1e6:,.0f} MB".replace(",", ".")


def _n(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def render(full: sqlite3.Connection, public: sqlite3.Connection, vectors: int) -> str:
    only_local, changed = compare(full, public)
    titles = {w.slug: w for w in WORKS}
    a, b = count(full), count(public)
    d = a - b
    lines = [
        "# Yerelde olup sunucuda olmayan veriler",
        "",
        "> Bu dosya `uv run python -m risale_mcp.local_only` ile üretilir (`build` sonunda da); elle düzenlemeyin.",
        "> Bir eseri yerelde tutan `Work.private` işaretidir: `src/risale_mcp/catalog/`. İzinler: `docs/izinler.md`.",
        "",
        "| Veritabanı | Eser | Bölüm | Paragraf | Cümle | Arapça parça |",
        "|---|---:|---:|---:|---:|---:|",
        f"| Yerel (`data/dist/kisisel/`) | {_scalar(full, 'SELECT count(*) FROM works WHERE built = 1')} | "
        f"{_n(a.nodes)} | {_n(a.paragraphs)} | {_n(a.sentences)} | {_n(a.arabic)} |",
        f"| Sunucu (`data/dist/genel/`) | {_scalar(public, 'SELECT count(*) FROM works WHERE built = 1')} | "
        f"{_n(b.nodes)} | {_n(b.paragraphs)} | {_n(b.sentences)} | {_n(b.arabic)} |",
        f"| **Fark** | **{len(only_local)}** | **{_n(d.nodes)}** | **{_n(d.paragraphs)}** | "
        f"**{_n(d.sentences)}** | **{_n(d.arabic)}** |",
        "",
        "Ortak eserlerde metin " + ("aynıdır (JSON özetleri tutuyor)." if not changed else
                                    f"**farklı**: {', '.join(f'`{s}`' for s in changed)}. Sunucu kopyası eski olabilir."),
        "",
        "## Yalnız yerelde olan eserler",
        "",
        "| # | Eser | Kaynak | Bölüm | Paragraf | Cümle | Neden yerelde |",
        "|---:|---|---|---:|---:|---:|---|",
    ]
    for i, slug in enumerate(only_local, 1):
        w, c = titles[slug], count(full, slug)
        source = f"{w.source.site}/{w.source.book}" if w.source else "—"
        lines.append(f"| {i} | {w.title} | `{source}` | {_n(c.nodes)} | {_n(c.paragraphs)} | {_n(c.sentences)} | {w.note} |")
    lines += [
        "",
        "## Eser olmayan yerel veriler",
        "",
        "Ham kaynak verisi hiçbir zaman sunucuya gitmez.",
        "",
        "| `data/raw/` | Boyut | Durum |",
        "|---|---:|---|",
    ]
    for folder, role in RAW_ROLES.items():
        lines.append(f"| `{folder}` | {_size(RAW_DIR / folder)} | {role} |")
    lines += ["", f"Anlamsal aramanın {_n(vectors)} vektörü de yalnız yereldedir: `scripts/deploy.sh` sunucuya "
                  "süzülmüş kopyayı gönderir (`embeddings export-public`)."]
    return "\n".join(lines) + "\n"


def main() -> None:
    full, public = connect(DB_PATH), connect(PUBLIC_DB_PATH)
    OUT_PATH.write_text(render(full, public, extra_vectors(public)), encoding="utf-8")
    print(f"yazıldı: {OUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
