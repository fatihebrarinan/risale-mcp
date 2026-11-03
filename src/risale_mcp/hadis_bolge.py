"""Künyenin bölgesinde okuma: doğrulanmamış hadis künyesi bâblı kitaplara gidiyorsa oradaki hadisleri okumak
(`docs/hadis-plani.md`, Adım 9; genel sıranın 2a-2'si).

    uv run python -m risale_mcp.hadis_bolge prepare    # data/interim/hadis/bolge/batch-N.json, key.json, yonerge.md
    (iki okuyucu: bolge/<A|B>-<N>-answers.json; yönerge yonerge.md'de)
    uv run python -m risale_mcp.hadis_bolge score      # bolge.{md,json}, data/library/hadis/region.json

Kaynakçada "doğrulanmadı" ya da "lafız farkıyla bulundu" yazan geçişlerin künyesi Kütüb-i Sitte ya da Muvatta'yı
bölüm ve numarayla gösteriyorsa künyenin bölgesi (`hadis_kutub.Index.cited`: bâb ya da kitap içi sıra, kitaba göre
pencere) okunur. Bölgedeki hadisler parçaya benzerliğe göre sıralanır (`hadis_adaylar.measure`), en yakın ikisi
okuyucuya gider.

Okuyucu yalnız iki Arapça metni görür (kitap, künye, puan gizli). Kontroller araya karışır ve okuyucu bilmez:
- `same_region`: aynı bölgenin parçaya en az benzeyen hadisi (aynı bâb, aynı konu; zor kontrol),
- `other_part`: aynı kitaptan başka bir parçanın en yakın adayı (Adım 7'nin kolay kontrolü).
Adım 7'nin kontrolü kolaydı (rastgele çift başka konudur); `same_region` o eksiği kapatmak içindir.

Kullanıcının kararı (2026-11-03): iki okuyucunun da aynı söz dediği rivayet künyenin bölgesindeyse geçiş "okumayla
bulundu" sayılır. `score` bunları `data/library/hadis/region.json`'a yazar (rivayetin metniyle: Hadith API karşılığı
varsa harekeli metin ve dereceler, yoksa JK metni); `build_db` iki profilde de yükler, künyesi yalnız anılmış
(`cited`, `phrase_found`, `marked`, `unsupported`) geçişin dayanağı `read_chapter` olur, kaynakçanın notu
"okumayla bulundu"dur. Bütün okumalar (bulunmayanlar dahil) `readings.json`'a `region` türüyle de girer (yalnız yerel).
"""

import json
import random
import sys
from collections import Counter
from pathlib import Path

from risale_mcp.hadis_adaylar import kept_words, measure, stems
from risale_mcp.hadis_kutub import Index, citations, load
from risale_mcp.hadis_okuma import score as score_pairs, same
from risale_mcp.paths import DB_PATH, INTERIM_DIR, LIBRARY_DIR, RAW_DIR

OUT = INTERIM_DIR / "hadis" / "bolge"
BATCHES = 3
TOP = 2                 # parça başına okunan en yakın aday
SECOND = 0.5            # ikinci aday, birincinin puanının en az bu kadarıysa
SAME_REGION = 0.25      # zor kontrol eklenen künye oranı (bölgede en az 4 hadis varsa)
OTHER_PART = 0.10
CONTEXT = 35            # adayda gösterilen pencere: eşleşen yerin iki yanı (kelime)
MIN_WORDS = 2
INSTRUCTIONS = """# Okuma yönergesi

Her çiftte iki Arapça metin var: `a` bir kitapta hadis diye anılan söz, `b` bir hadis kitabından bir rivayet (çoğu
zaman harekesiz, bazen bir parçası). Yalnız bu iki metne bakarak karar ver; hangi kitaptan geldiklerini, künyeyi ya
da başka bir bilgiyi bilmiyorsun ve ezberinden yargılama.

Her çift için şu alanlarla bir JSON nesnesi yaz:

- `id`: çiftin kimliği
- `relation`: `verbatim` (a, b'de kelimesi kelimesine ya da çok küçük farkla geçiyor), `abridged` (a, b'deki sözün
  kısaltılmışı ya da bir parçası), `by_meaning` (aynı söz, başka kelimelerle; anlam ve söyleyen aynı), `related` (aynı
  konu, başka söz), `different` (ilgisiz)
- `speaker`: b'de sözü kim söylüyor: `prophet`, `other` (sahâbî, tâbiî ya da başkası), `unclear`
- `denied`: b'de sözün hadis olmadığını söyleyen bir ifade var mı (true/false)
- `confidence`: `high`, `medium`, `low`
- `note`: kısa gerekçe (İngilizce ya da Türkçe, bir cümle)

Bütün cevapları tek bir JSON dizisi olarak `<okuyucu>-<parti>-answers.json` dosyasına yaz.
"""


def eligible(db: Path, index: Index) -> list[dict]:
    """Doğrulanmamış ya da lafız farkıyla bulunmuş geçişlerin, bu kitapları gösteren tekil künyeleri ve bölgeleri."""
    from risale_mcp.library import Library
    lib = Library(db)
    rows = lib.conn.execute(
        "SELECT a.paragraph_id, a.ord, a.hadith_key, a.hadith_support, a.kind, a.kind_source,"
        " substr(p.text, a.span_start + 1, a.span_end - a.span_start) AS text FROM arabic a"
        " JOIN paragraphs p ON p.id = a.paragraph_id JOIN works w ON w.slug = p.work"
        " WHERE a.kind = 'hadis' AND p.text IS NOT NULL AND w.language = 'tr'").fetchall()
    unverified = {}
    for r in rows:
        if not lib._hadith_line(r).get("verified"):
            unverified.setdefault(r["hadith_key"], r["text"])
    lib.close()
    supports = ("cited", "phrase_found", "marked", "unsupported", "found", "partly_found", "located_chapter")
    items = []
    for (key, book, raw), locs in citations(db, supports).items():
        if key not in unverified or len(unverified[key].split()) < MIN_WORDS:
            continue
        region = list({h["id"]: h for sec, num in locs for h in index.cited(book, sec, num)}.values())
        if region:
            items.append({"key": key, "part": unverified[key], "book": book, "citation": raw, "region": region})
    return items


def rank(part: str, region: list[dict], idf: dict[str, float]) -> list[tuple[float, dict, object]]:
    query = stems(part)
    scored = [(s.value, h, s) for h in region if (s := measure(query, stems(h["matn"] or h["text"]), idf))]
    return sorted(scored, key=lambda x: -x[0])


def window(text: str, start: int, end: int) -> str:
    kept = kept_words(text)
    if len(kept) <= 2 * CONTEXT + (end - start):
        return text
    return " ".join(kept[max(0, start - CONTEXT):end + CONTEXT + 1])


def prepare(db: Path = DB_PATH, out: Path = OUT, seed: int = 9) -> Counter:
    books = load()
    index = Index(books)
    idf = _idf(books)
    items = eligible(db, index)
    rng = random.Random(seed)
    pairs, tops = [], {}
    for it in items:
        ranked = rank(it["part"], it["region"], idf)
        if not ranked or ranked[0][0] <= 0:
            continue
        chosen = [ranked[0]] + [r for r in ranked[1:TOP] if r[0] >= SECOND * ranked[0][0]]
        tops[it["key"], it["book"], it["citation"]] = ranked[0][1]
        for value, h, s in chosen:
            pairs.append(_pair(it, h, s, value, "real"))
        if len(ranked) >= 4 and rng.random() < SAME_REGION:
            value, h, s = ranked[-1]
            pairs.append(_pair(it, h, s, value, "same_region"))
    for it in items:
        if rng.random() < OTHER_PART:
            others = [h for (k, b, _), h in tops.items() if b == it["book"] and k != it["key"]]
            if others:
                h = rng.choice(others)
                s = measure(stems(it["part"]), stems(h["matn"] or h["text"]), idf)
                pairs.append(_pair(it, h, s, s.value, "other_part"))
    unique = list({(p["key"], p["report"]): p for p in pairs}.values())      # aynı çift bir kez okunur
    rng.shuffle(unique)
    out.mkdir(parents=True, exist_ok=True)
    for i, p in enumerate(unique):
        p["id"] = f"r{i:03d}"
    for b in range(BATCHES):
        batch = [{"id": p["id"], "a": p["part"], "b": p["shown"]} for p in unique[b::BATCHES]]
        (out / f"batch-{b}.json").write_text(json.dumps(batch, ensure_ascii=False, indent=0), "utf-8")
    (out / "key.json").write_text(json.dumps(unique, ensure_ascii=False, indent=0), "utf-8")
    (out / "yonerge.md").write_text(INSTRUCTIONS, "utf-8")
    return Counter(p["set"] for p in unique) + Counter({"künye": len(items), "parça": len({i["key"] for i in items})})


def _pair(item: dict, hadith: dict, score, value: float, kind: str) -> dict:
    text = hadith["matn"] or hadith["text"]
    return {"key": item["key"], "part": item["part"], "book": item["book"], "citation": item["citation"],
            "report": hadith["id"], "api": hadith.get("api"), "score": round(value, 3), "set": kind,
            "decoy": kind != "real", "shown": window(text, score.start, score.end), "queues": [], "title": item["book"]}


def _idf(books: dict[str, dict]) -> dict[str, float]:
    import math
    df, n = Counter(), 0
    for data in books.values():
        for h in data["hadiths"]:
            df.update(set(stems(h["matn"] or h["text"])))
            n += 1
    return {w: math.log(n / (1 + c)) for w, c in df.items()}


def summary(result: dict) -> list[str]:
    rows = result["rows"]
    lines = ["# Künyenin bölgesinde okuma (Adım 9; model okuması, hüküm değil)\n",
             f"Okunan çift: {len(rows)}, eksik: {result['missing']}.\n",
             "| küme | çift | ikisi de aynı söz | ikisi de değil | ayrılan |", "|---|---|---|---|---|"]
    for name in ("real", "same_region", "other_part"):
        chosen = [r for r in rows if r["set"] == name]
        both = sum(all(same(a) for a in r["answers"]) for r in chosen)
        none = sum(not any(same(a) for a in r["answers"]) for r in chosen)
        lines.append(f"| {name} | {len(chosen)} | {both} | {none} | {len(chosen) - both - none} |")
    real = [r for r in rows if r["set"] == "real"]
    found = {(r["key"], r["citation"]) for r in real if all(same(a) for a in r["answers"])}
    cited = {(r["key"], r["citation"]) for r in real}
    keys = {r["key"] for r in real}
    lines.append(f"\nKünye: {len(cited)}, bölgesinde iki okuyucunun da aynı söz dediği bir rivayet bulunan: {len(found)}."
                 f" Parça: {len(keys)}, bulunan: {len({k for k, _ in found})}.")
    per_book = Counter(r["book"] for r in real if (r["key"], r["citation"]) in found and all(same(a) for a in r["answers"]))
    lines.append(f"\nİlişki (ikisi de aynı söz, ilk okuyucu): "
                 f"{dict(Counter(r['answers'][0]['relation'] for r in real if all(same(a) for a in r['answers'])).most_common())}")
    lines.append(f"\nKitap başına aynı söz denilen çift: {dict(per_book.most_common())}")
    return lines


def render(result: dict) -> str:
    lines = summary(result)

    def block(title: str, chosen: list[dict]) -> None:
        lines.append(f"\n## {title} ({len(chosen)})\n")
        for r in chosen:
            notes = " / ".join(f"{a['relation']} {a['speaker']} {a['confidence']}: {a['note']}" for a in r["answers"])
            lines.append(f"- `{r['id']}` {r['part']} ↔ `{r['report']}` ({r['citation']}; puan {r['score']}): {notes}")
    rows = result["rows"]
    block("Kontrolde aynı söz denilen", [r for r in rows if r["decoy"] and any(same(a) for a in r["answers"])])
    block("Okuyucular ayrıldı", [r for r in rows if not r["decoy"] and not r["agree_same"]])
    block("İkisi de aynı söz dedi", [r for r in rows if not r["decoy"] and all(same(a) for a in r["answers"])])
    return "\n".join(lines) + "\n"


REGION_PATH = LIBRARY_DIR / "hadis" / "region.json"


def export(result: dict, raw: Path = RAW_DIR, out: Path = REGION_PATH) -> int:
    """İki okuyucunun da aynı söz dediği gerçek çiftler: (parça, kitap, künye) -> rivayet, metniyle."""
    from risale_mcp.hadis import TITLES as API_TITLES
    from risale_mcp.hadis_kutub import TITLES as BOOK_TITLES
    found = [r for r in result["rows"] if not r["decoy"] and all(same(a) for a in r["answers"])]
    api: dict[str, dict] = {}
    for book in {r["book"] for r in found if r.get("api")}:
        for h in json.loads((raw / "hadith_api" / f"ara-{book}.json").read_text("utf-8"))["hadiths"]:
            api[f"{book}:{h['hadithnumber']}"] = h
    entries, reports = [], {}
    for r in found:
        rid = f"{r['book']}:{r['api']}" if r.get("api") and f"{r['book']}:{r['api']}" in api else f"jk:{r['report']}"
        if rid.startswith("jk:"):
            reports[rid] = {"title": BOOK_TITLES[r["book"]], "number": r["report"].split("/")[-1], "text": r["shown"],
                            "source": "openiti", "grades": []}
        else:
            h = api[rid]
            reports[rid] = {"title": API_TITLES[r["book"]], "number": str(h["hadithnumber"]), "text": h["text"],
                            "source": "hadith_api", "grades": [[g["name"], g["grade"]] for g in h.get("grades") or ()]}
        entries.append({"key": r["key"], "book": r["book"], "citation": r["citation"], "report": rid,
                        "relation": sorted({a["relation"] for a in r["answers"]})})
    out.write_text(json.dumps({"entries": entries, "reports": reports}, ensure_ascii=False, indent=0), "utf-8")
    return len(entries)


def main() -> None:
    if sys.argv[1:] == ["prepare"]:
        print(prepare())
        return
    result = score_pairs(OUT)
    (OUT.parent / "bolge.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), "utf-8")
    (OUT.parent / "bolge.md").write_text(render(result), "utf-8")
    print("\n".join(summary(result)))
    print(f"yazıldı: {REGION_PATH} ({export(result)} çift); şimdi `uv run python -m risale_mcp.build_db` (her profil)")


if __name__ == "__main__":
    main()
