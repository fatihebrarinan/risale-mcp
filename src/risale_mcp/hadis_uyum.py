"""Künye uyumu: künyesiz bulunan eşleşme, künyenin gösterdiği yerde mi (`docs/hadis-plani.md`, Adım 6).

    uv run python -m risale_mcp.hadis_uyum        # data/interim/hadis/uyum.{md,json}

Döngüsel değildir: yalnız `Corpus.match`'in künyeye bakmadan bulduğu rivayetler sınanır (künye orada yalnız seçimi
sıralar, bulunan küme aynıdır); seçilmiş 8 değil bütün rivayetler. `located_chapter` sınanmaz, künyeyle bulunmuştur.
Geçiş başınadır: aynı parça yerine göre başka künye taşır. Kısa parçalar (`phrase_found`) rivayeti ayırt etmez, girmez.

    chapter   bir rivayet künyedeki kitabın anılan bölümünde
    book      kitapta, başka bölümde ya da künyede bölüm yok
    absent    künyedeki kitap derlemde var, söz o kitapta bu lafızla yok: lafız farkı, başka baskı ya da yanlış künye
    no_corpus künyedeki kitapların hiçbiri derlemde yok: sınanamaz

`absent` künye yanlıştır demek değildir: müellifin lafzı rivayetten ayrılabilir, tek künye birçok rivayeti gösterir.
Karışık künye (`ROUNDS` tur) tesadüfi uyumun tabanıdır. Sonuç hüküm değildir, `hadith_support`'u değiştirmez.
"""

import json
import random
from collections import Counter
from pathlib import Path

from risale_mcp.db import connect
from risale_mcp.hadis import Corpus, read_reports
from risale_mcp.hadis_adaylar import cited_places
from risale_mcp.hadis_eval import is_holdout
from risale_mcp.hadis_kitaplar import BY_ID
from risale_mcp.hadis_kunye import parse as parse_citation
from risale_mcp.paths import DB_PATH, HADIS_PATH, INTERIM_DIR, RAW_DIR

ROUNDS = 100
LEVELS = ("chapter", "book", "absent", "no_corpus")


def level(found: list[tuple[str, int | None]], chapters: set, titles: set) -> str:
    """`found`: bulunan rivayetlerin (kitap, bölüm) çiftleri."""
    if not titles:
        return "no_corpus"
    if any(pair in chapters for pair in found):
        return "chapter"
    return "book" if any(title in titles for title, _ in found) else "absent"


def passages(db: Path, parts: dict) -> list[dict]:
    """Eşleşmeli parçaların künyeli geçişleri; aynı (parça, künye) bir kez sayılır."""
    seen = {}
    for r in connect(db).execute(
            "SELECT a.hadith_key AS key, a.source, a.paragraph_id AS place, a.kind_source,"
            " substr(p.text, a.span_start + 1, a.span_end - a.span_start) AS text FROM arabic a"
            " JOIN paragraphs p ON p.id = a.paragraph_id JOIN works w ON w.slug = p.work"
            " WHERE a.hadith_key IS NOT NULL AND a.source IS NOT NULL AND p.text IS NOT NULL AND w.language != 'os'"):
        if parts.get(r["key"], {}).get("match") in ("found", "partly_found"):
            citations = parse_citation(r["source"]).citations
            if any(c.book for c in citations):
                seen.setdefault((r["key"], r["source"]), {
                    "key": r["key"], "text": r["text"], "source": r["source"], "place": r["place"],
                    "match": parts[r["key"]]["match"], "qualifiers": sorted({c.qualifier for c in citations if c.qualifier})})
    return list(seen.values())


def numbers(corpus: Corpus, chosen: dict[str, list[int]], items: list[dict]) -> Counter:
    """Künyedeki "no." sayısı bulunan rivayetin numarasıyla tutuyor mu (Hadith API kitapları)."""
    counts = Counter()
    for item in items:
        for c in parse_citation(item["source"]).citations:
            known = BY_ID.get(c.book)
            for loc in c.locators:
                if known and known.api and loc.kind == "no":
                    hits = [corpus.reports[i] for i in chosen[item["key"]] if corpus.reports[i].section is not None]
                    in_book = [r for r in hits if r.id.startswith(f"{known.api}:")]
                    if in_book:
                        counts["no denenen"] += 1
                        counts["no tutan"] += any(r.number == loc.number for r in in_book)
    return counts


def book_rate(corpus: Corpus, chosen: dict[str, list[int]], items: list[dict]) -> Counter:
    """Bölüm taşıyan kitap künyeleri: metin o kitapta varsa künyedeki bölümde mi."""
    counts = Counter()
    for item in items:
        for c in parse_citation(item["source"]).citations:
            chapters, titles = cited_places([c])
            found = [(corpus.reports[i].title, corpus.reports[i].section) for i in chosen[item["key"]]]
            if chapters and any(t in titles for t, _ in found):
                counts["bölüm denenen"] += 1
                counts["bölüm tutan"] += any(p in chapters for p in found)
    return counts


def origins(db: Path, keys: list[str]) -> dict[str, Counter]:
    """Parçaların hadis işaretinin dayanağı, geçiş başına (`arabic.kind_source`)."""
    out: dict[str, Counter] = {}
    conn = connect(db)
    for key in keys:
        out[key] = Counter(r[0] for r in conn.execute("SELECT kind_source FROM arabic WHERE hadith_key = ?", (key,)))
    return out


def build(db: Path = DB_PATH, raw: Path = RAW_DIR, out_dir: Path = INTERIM_DIR / "hadis") -> dict:
    parts = json.loads(HADIS_PATH.read_text("utf-8"))["parts"]
    items = passages(db, parts)
    corpus = Corpus(list(read_reports(raw)))
    chosen = {i["key"]: corpus.match(i["text"], limit=None)[1] for i in items}
    found = {k: [(corpus.reports[r].title, corpus.reports[r].section) for r in v] for k, v in chosen.items()}
    places = [cited_places(parse_citation(i["source"]).citations) for i in items]
    for item, (chapters, titles) in zip(items, places):
        item["level"] = level(found[item["key"]], chapters, titles)
        item["holdout"] = is_holdout(item["key"])
        item["reports"] = len(chosen[item["key"]])
    shuffled = {False: Counter(), True: Counter()}
    rng, order = random.Random(14), list(places)
    for _ in range(ROUNDS):
        rng.shuffle(order)
        for item, (chapters, titles) in zip(items, order):
            shuffled[item["holdout"]][level(found[item["key"]], chapters, titles)] += 1
    audited = out_dir / "rivayet.json"
    queue = [p for p in json.loads(audited.read_text("utf-8"))["parts"] if "no_prophet" in p["queues"]]
    table = origins(db, [p["key"] for p in queue])
    result = {"items": items, "numbers": numbers(corpus, chosen, items) + book_rate(corpus, chosen, items),
              "shuffled": {("sınama" if h else "ayar"): {k: v / ROUNDS for k, v in c.items()} for h, c in shuffled.items()},
              "origins": [{"part": p["part"], "set": p["set"], "origins": table[p["key"]]} for p in queue]}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "uyum.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), "utf-8")
    (out_dir / "uyum.md").write_text(render(result), "utf-8")
    return result


def summary(result: dict) -> list[str]:
    items = result["items"]
    lines = ["\n## Künye uyumu (Adım 6, geçiş ve künye başına)\n", "| küme | geçiş | chapter | book | absent | no_corpus |", "|---|---|---|---|---|---|"]
    for name, holdout in (("ayar", False), ("sınama", True)):
        chosen = [i for i in items if i["holdout"] == holdout]
        real, fake = Counter(i["level"] for i in chosen), result["shuffled"][name]
        lines.append(f"| {name} gerçek | {len(chosen)} | " + " | ".join(str(real[l]) for l in LEVELS) + " |")
        lines.append(f"| {name} karışık | {len(chosen)} | " + " | ".join(f"{fake.get(l, 0):.1f}" for l in LEVELS) + " |")
    weak = [i for i in items if i["qualifiers"] and i["level"] == "absent"]
    n = result["numbers"]
    lines.append(f"\nBölüm: {n.get('bölüm tutan', 0)}/{n.get('bölüm denenen', 0)} künye. \"no.\": {n.get('no tutan', 0)}/{n.get('no denenen', 0)}. "
                 f"`absent` içinde see/iktibas/by_meaning: {len(weak)}.")
    return lines


def render(result: dict) -> str:
    lines = ["# Künye uyumu", *summary(result), "\n# absent: söz künyedeki kitapta bu lafızla yok\n"]
    for i in sorted((i for i in result["items"] if i["level"] == "absent"), key=lambda i: -i["reports"]):
        marks = "".join(f" `{q}`" for q in i["qualifiers"])
        lines.append(f"- {i['text']}{marks} ({i['match']}, {i['reports']} rivayet) | {i['source']} | {i['place']}")
    lines.append("\n# Peygamber'e bağlı görünmeyenlerin hadis işareti nereden\n")
    lines += [f"- {o['part']} ({o['set']}): {dict(o['origins'])}" for o in result["origins"]]
    return "\n".join(lines) + "\n"


def main() -> None:
    print("\n".join(summary(build())))


if __name__ == "__main__":
    main()
