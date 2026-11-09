"""Hadis sunucusunun veritabanı (MVP M5, `hadis` profili): kitaplar, bâb ağacı, hadisler, Kur'ân, Risale'den bağlar.

    uv run python -m risale_mcp.hadis_db          # data/dist/hadis/hadis.db (≈1 dk)

Şema (kullanıcı onayladı, 2026-11-06): atıf birimi hadistir. Kimlik `musned/14870` (baskının numarası) ya da
numarasız kitapta bizim sıramız `sifa/s00007`; kitap, bâb ve sahâbî müsnedi ağacı adrestir. Başkasının katmanı
(Zehebî, Elbânî, muhakkik) `layers`'ta, kimin olduğu yazılı; birimin metnine girmez.

Kaynaklar: `data/library/hadis/kutub/*.json` (Kütüb-i Sitte ve Muvatta: `hadis_kutub.py`; MVP kitapları:
`hadis_openiti.py`). Kur'ân tabloları genel profilin veritabanından kopyalanır (Kur'ân her sunucudadır); şema ortak
şemadır (`db.SCHEMA`), Risale tabloları boş kalır. Risale'den bağlar (`data/links/hadis/`; corpus, cited_chapter,
reading; model okumaları değil) Risale'nin metnini değil kimliğini ve atfını (`display`) taşır.

Bağın hedefi (`links_hadis.target`): Hadith API kimliği `hadis-derlem:tirmidhi:2670` kitabın API numarasıyla
(`api`) birime, kütüphane kimliği `hadis-derlem:musned:7422` / `…:sifa:s00007` doğrudan birime çözülür.
"""

import json
import sqlite3
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from risale_mcp import manifest
from risale_mcp.db import NORMALIZATION, SCHEMA, SCHEMA_VERSION
from risale_mcp.normalize import search_words
from risale_mcp.search import hadith_word
from risale_mcp.paths import DIST_DIR, LIBRARY_DIR, LINKS_DIR, PUBLIC_DB_PATH

KUTUB_DIR = LIBRARY_DIR / "hadis" / "kutub"
HADIS_DB = DIST_DIR / "hadis" / "hadis.db"
# Kitapların sırası: Kütüb-i Sitte ve Muvatta, sonra müellifin vefatına göre (hicrî)
ORDER = ("bukhari", "muslim", "abudawud", "tirmidhi", "nasai", "ibnmajah", "malik", "musned", "darimi", "mucem-sagir",
         "mustedrek", "delail", "sifa", "ihsan", "mecma", "kenz", "feyz", "kesfulhafa")
AUTHORS = {"bukhari": "Muhammed b. İsmâil el-Buhârî", "muslim": "Müslim b. Haccâc", "abudawud": "Ebû Dâvûd es-Sicistânî",
           "tirmidhi": "Ebû Îsâ et-Tirmizî", "nasai": "Ahmed b. Şuayb en-Nesâî", "ibnmajah": "İbn Mâce",
           "malik": "Mâlik b. Enes"}

HADIS_SCHEMA = """
CREATE TABLE lib_books (
    key     TEXT PRIMARY KEY,
    ord     INTEGER NOT NULL,
    title   TEXT NOT NULL,
    author  TEXT,
    source  TEXT NOT NULL,                       -- JSON: depo, commit, yol, lisans, baskı, not
    units   INTEGER NOT NULL
);
CREATE TABLE lib_nodes (
    seq       INTEGER PRIMARY KEY,
    id        TEXT NOT NULL UNIQUE,
    book      TEXT NOT NULL,
    parent_id TEXT,
    level     TEXT NOT NULL,                     -- book | kitab | bab
    number    INTEGER,
    title     TEXT NOT NULL,
    units     INTEGER NOT NULL DEFAULT 0          -- doğrudan altındaki birim
);
CREATE TABLE lib_units (
    seq      INTEGER PRIMARY KEY,                -- okuma sırası (bu veritabanında)
    id       TEXT NOT NULL UNIQUE,               -- musned/14870, sifa/s00007
    book     TEXT NOT NULL,
    node_id  TEXT NOT NULL,
    number   INTEGER,                            -- baskının numarası (numarasız kitapta NULL)
    api      INTEGER,                            -- Hadith API numarası (Kütüb-i Sitte)
    text     TEXT NOT NULL,
    isnad    TEXT,
    matn     TEXT,
    printed  TEXT,                               -- JSON {volume?, page}
    layers   TEXT                                -- JSON [{by, text}]: başkasının katmanı
);
CREATE INDEX lib_units_node ON lib_units(node_id);
CREATE INDEX lib_units_api ON lib_units(book, api);
CREATE VIRTUAL TABLE lib_fts USING fts5(words, tokenize = "unicode61 remove_diacritics 0");
-- râvi araması: baskı senedi ayırdıysa senet, ayırmadıysa bütün metin (senet orada metnin içindedir)
CREATE VIRTUAL TABLE lib_isnad_fts USING fts5(words, tokenize = "unicode61 remove_diacritics 0");
CREATE TABLE lib_risale (                     -- Risale'den bağlar: Risale'nin metni değil, kimliği ve atfı
    unit_id   TEXT NOT NULL,
    sentence  TEXT NOT NULL,
    display   TEXT,
    method    TEXT NOT NULL,
    relation  TEXT,
    strength  TEXT
);
CREATE INDEX lib_risale_unit ON lib_risale(unit_id);
"""

COPIED = ("quran_suras", "quran_ayahs", "quran_translators", "quran_translations", "sura_names")


def _words(text: str) -> str:
    """Dizinin kelimeleri: aramanın biçimi, "ابن" -> "بن" (`search.hadith_word`)."""
    return " ".join(hadith_word(w) for w in search_words(text))


def _books() -> list[dict]:
    out = []
    for key in ORDER:
        path = KUTUB_DIR / f"{key}.json"
        if path.exists():
            out.append(json.loads(path.read_text(encoding="utf-8")))
    return out


def build(out: Path = HADIS_DB, source_db: Path = PUBLIC_DB_PATH, manifest_check: bool = True,
          accept_id_changes: bool = False) -> Counter:
    counts: Counter = Counter()
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".tmp")
    tmp.unlink(missing_ok=True)
    conn = sqlite3.connect(tmp)
    conn.executescript("PRAGMA journal_mode = OFF; PRAGMA synchronous = OFF; PRAGMA temp_store = MEMORY;"
                       " PRAGMA cache_size = -200000;")             # geçici dosya: yarıda kalırsa silinir
    conn.executescript(SCHEMA)
    conn.executescript(HADIS_SCHEMA)
    conn.execute("ATTACH DATABASE ? AS src", (str(source_db),))
    for table in COPIED:
        conn.execute(f"INSERT INTO {table} SELECT * FROM src.{table}")
        counts[table] = conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
    conn.commit()
    conn.execute("DETACH DATABASE src")
    api_index: dict[tuple[str, int], str] = {}
    for ord_, book in enumerate(_books()):
        key = book["book"]
        source = dict(book.get("source") or {})
        author = source.get("author") or AUTHORS.get(key)
        node_units: Counter = Counter()
        for h in book["hadiths"]:
            node_units[h["node_id"]] += 1
        # Kütüb-i Sitte ve Muvatta'nın ağacında kitabın kendi düğümü yok: kök eklenir, en üst düğümler ona bağlanır
        # (`get_outline("bukhari")` kitap kimliğiyle çalışsın).
        rooted = any(n["id"] == key for n in book["outline"])
        if not rooted:
            conn.execute("INSERT INTO lib_nodes (id, book, parent_id, level, number, title, units) VALUES (?, ?, NULL, 'book', NULL, ?, 0)",
                         (key, key, book["title"]))
        for n in book["outline"]:
            parent = n.get("parent_id") or (None if rooted else key)
            conn.execute("INSERT INTO lib_nodes (id, book, parent_id, level, number, title, units) VALUES (?, ?, ?, ?, ?, ?, ?)",
                         (n["id"], key, parent, n.get("level") or "bab", n.get("number"), n["title"],
                          node_units.get(n["id"], 0)))
        for h in book["hadiths"]:
            if not (h.get("text") or "").strip():
                continue
            cur = conn.execute(
                "INSERT INTO lib_units (id, book, node_id, number, api, text, isnad, matn, printed, layers)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (h["id"], key, h["node_id"], h.get("number"), h.get("api"), h["text"], h.get("isnad"), h.get("matn"),
                 json.dumps(h["printed"]) if h.get("printed") else None,
                 json.dumps(h["layers"], ensure_ascii=False) if h.get("layers") else None))
            conn.execute("INSERT INTO lib_fts (rowid, words) VALUES (?, ?)", (cur.lastrowid, _words(h.get("matn") or h["text"])))
            separated = bool(h.get("isnad") and h.get("matn"))
            conn.execute("INSERT INTO lib_isnad_fts (rowid, words) VALUES (?, ?)",
                         (cur.lastrowid, _words(h["isnad"] if separated else h["text"])))
            if h.get("api") is not None:
                api_index[(key, int(h["api"]))] = h["id"]
            counts["units"] += 1
        conn.execute("INSERT INTO lib_books VALUES (?, ?, ?, ?, ?, ?)",
                     (key, ord_, book["title"], author, json.dumps(source, ensure_ascii=False), len(book["hadiths"])))
        counts["books"] += 1
    seen: set[tuple[str, str]] = set()     # aynı yer iki yoldan (Hadith API numarası, kütüphane kimliği) gelebilir
    for name in ("corpus", "cited_chapter", "reading"):
        path = LINKS_DIR / "hadis" / f"{name}.jsonl"
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            rec = json.loads(line)
            if "meta" in rec:
                continue
            unit = resolve_target(rec["target"], api_index)
            if unit is None:
                counts["risale_unresolved"] += 1
                continue
            if (unit, rec["source"]) in seen:
                counts["risale_duplicate"] += 1
                continue
            seen.add((unit, rec["source"]))
            conn.execute("INSERT INTO lib_risale VALUES (?, ?, ?, ?, ?, ?)",
                         (unit, rec["source"], rec.get("display"), rec["method"], rec.get("relation"), rec.get("strength")))
            counts["risale_links"] += 1
    conn.executemany("INSERT INTO meta VALUES (?, ?)", [
        ("schema_version", str(SCHEMA_VERSION)), ("normalization", NORMALIZATION),
        ("built_at", datetime.now(timezone.utc).isoformat(timespec="seconds")), ("profile", "hadis")])
    conn.commit()
    if manifest_check:                  # H1: hadis kimlikleri de kabul edilmiş manifestoyla karşılaştırılır
        try:
            changes = manifest.check_build(conn, "hadis", accept_id_changes)
        except manifest.IdChangesError:
            conn.close()
            tmp.unlink(missing_ok=True)
            raise
        counts["id_changes"] = 0 if changes.empty else 1
        conn.commit()
    conn.close()
    tmp.replace(out)
    return counts


def resolve_target(target: str, api_index: dict[tuple[str, int], str]) -> str | None:
    """Bağın hedefinden birim kimliği: Hadith API numarası kitabın `api` alanıyla, kütüphane kimliği doğrudan."""
    if not target.startswith("hadis-derlem:"):
        return None
    book, _, number = target.removeprefix("hadis-derlem:").partition(":")
    if number.isdigit() and (book, int(number)) in api_index:
        return api_index[(book, int(number))]
    if (KUTUB_DIR / f"{book}.json").exists() and book not in AUTHORS:
        return f"{book}/{number}"
    return None


def main() -> None:
    counts = build(accept_id_changes="--accept-id-changes" in sys.argv)
    print(dict(counts), HADIS_DB, f"{HADIS_DB.stat().st_size // 1_000_000} MB", file=sys.stdout)


if __name__ == "__main__":
    main()
