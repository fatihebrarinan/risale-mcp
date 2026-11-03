"""Âyet bağları ve eski adlar, `links` biçiminde (`docs/bag-altyapisi-plani.md`, B4).

Âyet alıntısı ve âyet ilişkileri metinden kurallarla çıkar, `build_db` her profilde yeniden hesaplar: bu bağlar
dosyadan okunmaz (döngü olmasın), `build_db` onları `links` tablosuna doğrudan yazar ve yerel profilde dosyaya döker
(`computed: build_db`). Dosya, Risale veritabanı olmadan okuyanlar içindir (hadis sunucusu, ileride tefsir).

    kuran/quote.jsonl       cümledeki âyet: kaynağın işareti (`source_mark`) ya da Kur'ân metninde bulunan
                            (`quran_text`); `ayah_check` iktibas ise `abridged`. Bir duanın içindeki âyet (`ayah_quotes`)
                            parçanın tamamının anahtarıyla, `evidence.inside`
    kuran/relation.jsonl    âyet ilişkileri (`ayah_links.py`): isaret, acilis, izah, dayanak, risale; bölüm kapsamlıda
                            kaynak düğümdür, kanıt cümlesi `evidence.sentence`
    risale/reference.jsonl  eski adlar (`books/old_names.json`): metni başka yerde duran bölüm -> asıl yeri
"""

import json
import sqlite3
from pathlib import Path

from risale_mcp.links import Link, part_key

OLD_NAMES = Path(__file__).parent / "books" / "old_names.json"
COMPUTED = "build_db"
QUOTE_RELATION = {"iktibas": "abridged"}           # öbürleri (exact, near, dizgi şüphesi, numarasız) verbatim


def _verse(sura: int, start: int, end: int | None) -> str:
    return f"quran:{sura}:{start}" + (f"-{end}" if end and end != start else "")


def quote_links(conn: sqlite3.Connection) -> list[Link]:
    conn.row_factory = sqlite3.Row
    out = []
    for r in conn.execute(
            "SELECT a.sentence_id, a.sura, a.ayah_start, a.ayah_end, a.ayah_check, a.kind_source,"
            " substr(p.text, a.span_start + 1, a.span_end - a.span_start) AS text FROM arabic a"
            " JOIN paragraphs p ON p.id = a.paragraph_id WHERE a.sura IS NOT NULL AND a.sentence_id IS NOT NULL"):
        evidence = {k: v for k, v in (("check", r["ayah_check"]), ("kind_source", r["kind_source"])) if v}
        out.append(Link(r["sentence_id"], _verse(r["sura"], r["ayah_start"], r["ayah_end"]), "quote",
                        "quran_text" if r["kind_source"] == "kuran" else "source_mark", "strong",
                        QUOTE_RELATION.get(r["ayah_check"], "verbatim"), part_key(r["text"]), evidence=evidence))
    for r in conn.execute(
            "SELECT q.sentence_id, q.sura, q.ayah_start, q.ayah_end,"
            " substr(p.text, a.span_start + 1, a.span_end - a.span_start) AS text FROM ayah_quotes q"
            " JOIN arabic a ON a.paragraph_id = q.paragraph_id AND a.ord = q.ord"
            " JOIN paragraphs p ON p.id = q.paragraph_id WHERE q.sentence_id IS NOT NULL"):
        out.append(Link(r["sentence_id"], _verse(r["sura"], r["ayah_start"], r["ayah_end"]), "quote", "quran_text",
                        "strong", "verbatim", part_key(r["text"]), evidence={"inside": True}))
    return out


def relation_links(conn: sqlite3.Connection) -> list[Link]:
    out = []
    for sura, start, end, kind, strength, node, scope, evidence in conn.execute(
            "SELECT sura, ayah_start, ayah_end, kind, strength, node_id, scope, evidence_id FROM ayah_links"):
        source = node if scope == "section" else evidence
        out.append(Link(source, _verse(sura, start, end), "relation", "rule", strength, kind, scope=scope,
                        evidence={"sentence": evidence}))
    return out


def reference_links(path: Path = OLD_NAMES) -> list[Link]:
    out = []
    for node, entry in json.loads(path.read_text("utf-8"))["sections"].items():
        for target in entry["elsewhere"]:
            out.append(Link(node, f"risale:{target}", "reference", "curated", "strong", "old_name", scope="section",
                            evidence={k: entry[k] for k in ("name", "evidence", "rule") if entry.get(k)}))
    return out


def computed(conn: sqlite3.Connection) -> dict[str, list[Link]]:
    """Dosya adı -> bağlar: `build_db`'nin bu profil için hesapladıkları."""
    return {"kuran/quote.jsonl": quote_links(conn), "kuran/relation.jsonl": relation_links(conn),
            "risale/reference.jsonl": reference_links()}
