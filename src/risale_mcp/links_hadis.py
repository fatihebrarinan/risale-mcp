"""Hadis bağları: Risale'deki hadis parçalarının rivayetlere bağları, `links` biçiminde (`docs/bag-altyapisi-plani.md`, B2).

    uv run python -m risale_mcp.links_hadis      # data/library/hadis/{matches,region,readings}.json -> data/links/hadis/*.jsonl

Bağı üreten işler (`hadis.py`, `hadis_bolge.py score`, `hadis_okumalar.py`) bitince bunu çağırır. Kaynak cümledir,
parça `arabic.hadith_key`'dir; bugünkü tablolar parça anahtarına bağlı olsa da bağ parçanın geçtiği her cümle için
yazılır. Rivayetin metni bağda değil, üreten işin dosyasındadır (`matches.json` vb.).

    corpus.jsonl         derlemde bulunan (`found` verbatim, `partly_found` partial, `phrase_found` phrase)
    cited_chapter.jsonl  kısa parça, geçişin künyesindeki kitabın anılan bölümünde (künye `evidence.citation`)
    reading.jsonl        künyenin bölgesinde iki kör okuyucu aynı söz dedi (kullanıcının kararıyla bulundu sayılır)
    reading_lead.jsonl   model okumalarının hepsi, hüküm değil (Adım 3–7, 9); private: yalnız yerel profil

Hedef kimliği: kütüphanede kitabı olan JK metni `hadis:<kitap>/<no>`, öbürleri bugünkü derlem kimliğiyle
`hadis-derlem:<derlem>:<no>`. Kütüphane kimliğine geçiş ve gösterilecek numara hadis sunucusunun kararıdır (HA5):
Buhârî'de JK numarası okuyucunun bildiği Fethu'l-Bârî numarası değildir.
"""

import json
import sqlite3
from pathlib import Path

from risale_mcp.links import Link, write
from risale_mcp.paths import DB_PATH, HADIS_PATH, LIBRARY_DIR, LINKS_DIR

OUT = LINKS_DIR / "hadis"
REGION_PATH = LIBRARY_DIR / "hadis" / "region.json"
READINGS_PATH = LIBRARY_DIR / "hadis" / "readings.json"
MATCH_RELATION = {"found": "verbatim", "partly_found": "partial", "phrase_found": "phrase"}
SAME = ("verbatim", "abridged", "by_meaning")


def target(report_id: str) -> str:
    return "hadis:" + report_id.removeprefix("jk:") if report_id.startswith("jk:") else "hadis-derlem:" + report_id


def report_id(target_id: str) -> str:
    """Bağın hedefinden bugünkü rivayet kimliği (`hadith_reports.id`)."""
    if target_id.startswith("hadis-derlem:"):
        return target_id.removeprefix("hadis-derlem:")
    return "jk:" + target_id.removeprefix("hadis:")


def passages(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    """Hadis parçalarının geçişleri: cümlesi, künye metni ve gösterilecek atfı."""
    from risale_mcp.library import hit_cite
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT a.paragraph_id, a.ord, a.hadith_key, a.source, s.id AS sentence_id, s.ref, s.incipit, s.text"
        " FROM arabic a JOIN sentences s ON s.id = a.sentence_id WHERE a.hadith_key IS NOT NULL").fetchall()
    return [{**dict(r), "display": hit_cite(r["ref"], r["incipit"], r["text"])} for r in rows]


def corpus_links(rows: list[dict], parts: dict) -> list[Link]:
    out = []
    for r in rows:
        entry = parts.get(r["hadith_key"]) or {}
        if (relation := MATCH_RELATION.get(entry.get("match"))) is None:
            continue
        for rank, rid in enumerate(entry["reports"]):
            out.append(Link(r["sentence_id"], target(rid), "quote", "corpus", "weak" if relation == "phrase" else "strong",
                            relation, r["hadith_key"], evidence={"match": entry["match"], "rank": rank, "total": entry["total"]},
                            display=r["display"]))
    return out


def located_links(rows: list[dict], parts: dict) -> list[Link]:
    out = []
    for r in rows:
        place = ((parts.get(r["hadith_key"]) or {}).get("located") or {}).get(r["source"])
        for rank, rid in enumerate((place or {}).get("reports", ())):
            out.append(Link(r["sentence_id"], target(rid), "quote", "cited_chapter", "weak", "phrase", r["hadith_key"],
                            evidence={"citation": r["source"], "rank": rank, "level": place["level"]}, display=r["display"]))
    return out


def reading_links(conn: sqlite3.Connection, rows: list[dict], region: dict) -> list[Link]:
    """Okumayla bulunan: geçişin kendi künyesi (yoksa nurpedia'nınki) o kitabı aynı yazılışla gösteriyorsa."""
    wanted = {(e["key"], e["book"], e["citation"]): e for e in region["entries"]}
    out = []
    for r in rows:
        own = conn.execute("SELECT book, raw FROM hadith_citations WHERE paragraph_id = ? AND ord = ?",
                           (r["paragraph_id"], r["ord"])).fetchall()
        own = own or conn.execute("SELECT book, raw FROM hadith_citations WHERE hadith_key = ? AND origin = 'nurpedia'",
                                  (r["hadith_key"],)).fetchall()
        for book, raw in own:
            if e := wanted.get((r["hadith_key"], book, raw)):
                out.append(Link(r["sentence_id"], target(e["report"]), "quote", "reading", "strong", ",".join(e["relation"]),
                                r["hadith_key"], evidence={"citation": raw, "book": book}, display=r["display"]))
    return out


def lead_links(rows: list[dict], readings: dict) -> list[Link]:
    by_key: dict[str, list[dict]] = {}
    for r in rows:
        by_key.setdefault(r["hadith_key"], []).append(r)
    out = []
    for key, part in readings["parts"].items():
        for kind, items in (("candidate", part["candidates"]), ("match", part["readings"])):
            for c in items:
                relation = c["relation"][0] if len(set(c["relation"])) == 1 else "disputed"
                for r in by_key.get(key, ()):
                    out.append(Link(r["sentence_id"], target(c["report"]), "quote", "reading",
                                    "strong" if c["same"] else "weak", relation, key,
                                    evidence={"kind": kind, "tier": c.get("tier"), "in_cited_chapter": c.get("in_cited_chapter"),
                                              "readers": c["relation"], "speaker": c["speaker"], "denied": c["denied"],
                                              "same": c["same"]},
                                    display=r["display"]))
    return out


def export(db: Path = DB_PATH, out: Path = OUT, matches: Path = HADIS_PATH, region: Path = REGION_PATH,
           readings: Path = READINGS_PATH) -> dict[str, int]:
    conn = sqlite3.connect(db)
    rows = passages(conn)
    parts = json.loads(matches.read_text("utf-8"))["parts"] if matches.exists() else {}
    counts = {
        "corpus": write(out / "corpus.jsonl", corpus_links(rows, parts), producer="hadis.py", source="matches.json"),
        "cited_chapter": write(out / "cited_chapter.jsonl", located_links(rows, parts), producer="hadis.py",
                               source="matches.json"),
    }
    if region.exists():
        counts["reading"] = write(out / "reading.jsonl", reading_links(conn, rows, json.loads(region.read_text("utf-8"))),
                                  producer="hadis_bolge.py", source="region.json")
    if readings.exists():
        counts["reading_lead"] = write(out / "reading_lead.jsonl", lead_links(rows, json.loads(readings.read_text("utf-8"))),
                                       producer="hadis_okumalar.py", source="readings.json", private=True,
                                       note="Model okumaları, hüküm değil: hadisçi görmeden genel sunucuya çıkmaz")
    return counts


def main() -> None:
    print(export())


if __name__ == "__main__":
    main()
