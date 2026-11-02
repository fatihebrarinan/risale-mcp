"""Hadis adayları: derlemde lafzen bulunamayan parçaya en yakın rivayetler (`docs/hadis-plani.md`, Adım 3).

    uv run python -m risale_mcp.hadis_adaylar     # data/interim/hadis/adaylar.{md,json}

Çıktı eşleme değil, gözden geçirilecek listedir: `arabic`, `hadith_support` ve araçlar değişmez. Benzerlik başka hadise
gidebilir; adayı kabul etmek okuyanın işidir (Adım 7, 8). Yöntem Risale'ye bağlı değildir, metin alır.

Kelimeler iskelete indirilir, başındaki harf-i cer ve "ال", sonundaki zamir atılır (`stem`). Nadir kelimeler rivayetleri
seçer (`Index.search`), seçilenlerde parçanın kelimelerini en dar yerde toplayan pencere ölçülür:

    coverage  parçanın ağırlıklı kelimelerinin penceredeki oranı
    order     aynı sırayla gelenlerin oranı (en uzun ortak dizi)
    adjacency parçada yan yana duran ikililerin rivayette de yan yana durma oranı

Yalnız kelime ortaklığı rastgele tutar, bitişiklik ayırır. Kısaltma ve lafız farkı ipucu `hint`'tir, hüküm değildir:
    abridged    parçanın nerdeyse bütün kelimeleri aynı sırayla, araları açık
    variant     kelimeleri çoğunlukla ortak, sırası ya da birkaç kelimesi farklı
Künyedeki `by_meaning` ("bilmânâ") ayrı kanıttır, yanında gösterilir; "ilişki mânen nakildir" diyen tek şey odur.

Seviye (`tier`), ikisi birbirinden bağımsız kanıttır:
    chapter  ilk 10 adaydan biri künyenin anılan bölümünde. Arama künyeyi görmez, bu yüzden döngüsel değildir
    close    en yakın aday `CLOSE` eşiğini geçiyor: negatif kontrolde ayar kümesinde en çok %3 geçen eşik
    review   ikisi de yok, en yakın adaylar yalnız okumak için
4 ve daha az kelimede eşik yoktur: kısa parçada benzerlik negatif kontrolden ayrılmıyor.
Eşikler yalnız ayar kümesinden seçildi (`hadis_eval.is_holdout`); sınama kümesi raporda ayrı sayılır.
"""

import json
import math
import random
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from risale_mcp.db import connect
from risale_mcp.hadis import TITLES, Corpus, Report, book_titles, rank, read_reports, words
from risale_mcp.hadis_eval import CONTROL_PATH, is_holdout
from risale_mcp.hadis_kitaplar import BY_ID
from risale_mcp.hadis_kunye import parse as parse_citation
from risale_mcp.paths import DB_PATH, HADIS_PATH, INTERIM_DIR, RAW_DIR
from risale_mcp.quran import skeleton

MAX_SHARE = 0.2         # bu orandan çok rivayette geçen kelime seçmede kullanılmaz
POOL = 3000             # ince ölçüme giren rivayet
LIMIT = 10              # parça başına aday
CLOSE = ((12, 0.5), (8, 0.7), (5, 0.9))     # en az kelime, en az puan
ROUNDS = 200            # karışık künye turu
_PREFIXES = ("فل", "بل", "كل", "ل", "ب", "ف", "ك")
_SUFFIXES = ("هم", "كم", "ه", "ك", "ن")
_ETC = skeleton("الخ")


def stem(word: str) -> str:
    for p in _PREFIXES:
        if word.startswith(p) and len(word) - len(p) >= 2:
            word = word[len(p):]
            break
    for s in _SUFFIXES:
        if word.endswith(s) and len(word) - len(s) >= 2:
            return word[:-len(s)]
    return word


def stems(text: str) -> list[str]:
    return [stem(w) for w in words(text) if w != _ETC]


def common_subsequence(a: list[str], b: list[str]) -> int:
    row = [0] * (len(b) + 1)
    for x in a:
        new = [0]
        for j, y in enumerate(b):
            new.append(row[j] + 1 if x == y else max(row[j + 1], new[j]))
        row = new
    return row[-1]


@dataclass(frozen=True)
class Score:
    report: int
    coverage: float
    order: float
    adjacency: float
    start: int
    end: int

    @property
    def value(self) -> float:
        return self.coverage * (0.4 + 0.2 * self.order + 0.4 * self.adjacency)


def measure(query: list[str], body: list[str], idf: dict[str, float], report: int = 0) -> Score:
    """Parçanın kelimelerini en çok toplayan pencere; pencere parçanın bir buçuk katıdır."""
    unique = list(dict.fromkeys(query))
    total = sum(idf.get(w, 0.0) for w in unique) or 1.0
    wanted, width = set(unique), len(query) * 3 // 2 + 2
    hits = [i for i, w in enumerate(body) if w in wanted]
    best, span, low = 0.0, (0, -1), 0
    for high, at in enumerate(hits):
        while at - hits[low] >= width:
            low += 1
        weight = sum(idf.get(w, 0.0) for w in {body[i] for i in hits[low:high + 1]})
        if weight > best:
            best, span = weight, (hits[low], at)
    window = body[span[0]:span[1] + 1]
    pairs = list(dict.fromkeys(zip(query, query[1:])))
    present = set(zip(window, window[1:]))
    weigh = lambda p: idf.get(p[0], 0.0) + idf.get(p[1], 0.0)
    adjacency = sum(map(weigh, set(pairs) & present)) / (sum(map(weigh, pairs)) or 1.0)
    return Score(report, best / total, common_subsequence(query, window) / len(query), adjacency, *span)


def hint(score: Score) -> str:
    return "abridged" if score.coverage >= 0.85 and score.order >= 0.8 and score.adjacency < 0.8 else "variant"


class Index:
    def __init__(self, reports: list[Report]) -> None:
        self.reports = reports
        self.bodies = [stems(r.text) for r in reports]
        df = Counter(w for body in self.bodies for w in set(body))
        n = len(reports)
        self.idf = {w: math.log(n / (1 + c)) for w, c in df.items()}
        self.absent = math.log(n)
        postings: dict[str, list[int]] = defaultdict(list)
        for i, body in enumerate(self.bodies):
            for w in set(body):
                if df[w] < n * MAX_SHARE:
                    postings[w].append(i)
        self.postings = {w: np.array(v, dtype=np.int32) for w, v in postings.items()}

    def search(self, text: str, limit: int = 5) -> list[Score]:
        """En yakın rivayetler; aynı metnin kopyaları ayrı sayılmaz (ilki kalır, `rank` sırasıyla)."""
        query = stems(text)
        if len(query) < 2:
            return []
        idf = {w: self.idf.get(w, self.absent) for w in query}
        votes = np.zeros(len(self.reports), dtype=np.float32)
        for w in set(query):
            if w in self.postings:
                votes[self.postings[w]] += idf[w]
        pool = np.argpartition(-votes, min(POOL, len(votes) - 1))[:POOL]
        scored = [measure(query, self.bodies[i], idf, int(i)) for i in pool if votes[i] > 0]
        scored.sort(key=lambda s: (-s.value, s.report))
        out, seen = [], set()
        for s in scored:
            passage = tuple(self.bodies[s.report][s.start:s.end + 1])
            if passage not in seen:
                seen.add(passage)
                out.append(s)
            if len(out) == limit:
                break
        return out


def close(query_length: int, value: float) -> bool:
    return any(query_length >= n and value >= t for n, t in CLOSE)


def kept_words(text: str) -> list[str]:
    """Metnin kendi yazılışıyla, `stems` ile aynı sırada aynı kelimeler."""
    return [w for w in text.split() if (k := skeleton(w)) and k != _ETC]


def excerpt(text: str, start: int, end: int) -> str:
    return " ".join(kept_words(text)[start:end + 1])


def cited_places(citations: list) -> tuple[set[tuple[str, int]], set[str]]:
    """Künyelerin (kitap, bölüm) çiftleri ve derlemdeki kitap adları."""
    chapters = set()
    for c in citations:
        known = BY_ID.get(c.book)
        if known and known.api:
            chapters |= {(TITLES[known.api], l.section) for l in c.locators if l.section is not None}
    return chapters, book_titles(citations)


def _agrees(reports: list[Report], scores: list[Score], chapters: set) -> bool:
    return any((reports[s.report].title, reports[s.report].section) in chapters for s in scores)


def _shuffled(reports: list[Report], items: list[tuple[list[Score], set]]) -> float:
    places, rng, total = [c for _, c in items], random.Random(14), 0
    for _ in range(ROUNDS):
        rng.shuffle(places)
        total += sum(_agrees(reports, s, c) for (s, _), c in zip(items, places))
    return total / ROUNDS


def parts_without_match(db: Path) -> dict[str, dict]:
    """Ana metinde derlem sonucu `none` olan parçalar, geçişleriyle."""
    matches = json.loads(HADIS_PATH.read_text("utf-8"))["parts"]
    parts: dict[str, dict] = {}
    for row in connect(db).execute(
            "SELECT a.hadith_key AS key, a.source, a.paragraph_id AS place,"
            " substr(p.text, a.span_start + 1, a.span_end - a.span_start) AS text FROM arabic a"
            " JOIN paragraphs p ON p.id = a.paragraph_id JOIN works w ON w.slug = p.work"
            " WHERE a.hadith_key IS NOT NULL AND p.text IS NOT NULL AND w.language != 'os'"):
        if matches.get(row["key"], {}).get("match") == "none":
            part = parts.setdefault(row["key"], {"text": row["text"], "sources": set(), "places": []})
            part["places"].append(row["place"])
            part["sources"].update([row["source"]] if row["source"] else [])
    return parts


def build(db: Path = DB_PATH, raw: Path = RAW_DIR, out_dir: Path = INTERIM_DIR / "hadis") -> dict:
    reports = sorted(read_reports(raw), key=rank)
    index = Index(reports)
    corpus = Corpus(reports)
    entries, agreement = [], {False: [], True: []}
    for key, part in parts_without_match(db).items():
        citations = [c for raw_ in sorted(part["sources"]) for c in parse_citation(raw_).citations]
        chapters, titles = cited_places(citations)
        scores = index.search(part["text"], LIMIT)
        n = len(stems(part["text"]))
        holdout = is_holdout(key)
        if chapters:
            agreement[holdout].append((scores, chapters))
        in_chapter = _agrees(reports, scores, chapters)
        tier = "chapter" if in_chapter else "close" if scores and close(n, scores[0].value) else "review"
        entries.append({
            "key": key, "text": part["text"], "words": n, "holdout": holdout, "tier": tier, "places": part["places"],
            "sources": sorted(part["sources"]), "by_meaning": any(c.qualifier == "by_meaning" for c in citations),
            "iktibas": any(c.qualifier == "iktibas" for c in citations),
            "candidates": [{
                "report": reports[s.report].id, "title": reports[s.report].title, "score": round(s.value, 2),
                "coverage": round(s.coverage, 2), "order": round(s.order, 2), "adjacency": round(s.adjacency, 2),
                "hint": hint(s), "in_cited_chapter": _agrees(reports, [s], chapters),
                "in_cited_book": reports[s.report].title in titles,
                "excerpt": excerpt(reports[s.report].text, s.start, s.end)} for s in scores]})
    pool = json.loads(CONTROL_PATH.read_text("utf-8"))["pool"]
    control = Counter()
    for text in pool:
        if corpus.match(text)[0] == "none":
            n, top = len(stems(text)), index.search(text, 1)
            band = f"{'sınama' if is_holdout(skeleton(text)) else 'ayar'} {_band(n)}"
            control[f"{band}|n"] += 1
            control[f"{band}|close"] += bool(top and close(n, top[0].value))
    result = {
        "parts": entries, "control": control,
        "agreement": {name: {"parts": len(agreement[h]), "real": sum(_agrees(reports, s, c) for s, c in agreement[h]),
                             "shuffled": _shuffled(reports, agreement[h])}
                      for name, h in (("ayar", False), ("sınama", True))}}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "adaylar.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), "utf-8")
    (out_dir / "adaylar.md").write_text(render(result), "utf-8")
    return result


def _band(n: int) -> str:
    return "4 ve daha az" if n < 5 else "5–7" if n < 8 else "8–11" if n < 12 else "12+"


def summary(result: dict) -> list[str]:
    parts = result["parts"]
    lines = ["\n## Adaylar (Adım 3, gözden geçirilecek liste, eşleme değil)\n", "| grup | parça | chapter | close | review |",
             "|---|---|---|---|---|"]
    for name, holdout in (("ayar", False), ("sınama", True)):
        for band in ("4 ve daha az", "5–7", "8–11", "12+"):
            tiers = Counter(p["tier"] for p in parts if p["holdout"] == holdout and _band(p["words"]) == band)
            lines.append(f"| {name} {band} | {sum(tiers.values())} | {tiers['chapter']} | {tiers['close']} | {tiers['review']} |")
    lines += ["\nNegatif kontrol, `close` eşiğini geçen:\n", "| grup | geçen / denenen |", "|---|---|"]
    for key in sorted(k[:-2] for k in result["control"] if k.endswith("|n")):
        lines.append(f"| {key} | {result['control'][f'{key}|close']} / {result['control'][f'{key}|n']} |")
    lines += ["\nİlk 10 aday künyenin anılan bölümünde:\n", "| küme | künyesi bölüm gösteren | gerçek künye | karışık künye |", "|---|---|---|---|"]
    lines += [f"| {k} | {a['parts']} | {a['real']} | {a['shuffled']:.1f} |" for k, a in result["agreement"].items()]
    lines.append(f"\nKünyesi `by_meaning` diyen parça: {sum(p['by_meaning'] for p in parts)}; "
                 f"`iktibas`: {sum(p['iktibas'] for p in parts)}.")
    return lines


def render(result: dict) -> str:
    lines = ["# Hadis adayları", *summary(result)]
    for tier in ("chapter", "close", "review"):
        chosen = [p for p in result["parts"] if p["tier"] == tier]
        lines.append(f"\n# {tier} ({len(chosen)})")
        for p in chosen:
            marks = "".join(f" `{m}`" for m in ("by_meaning", "iktibas") if p[m])
            lines += [f"\n## {p['text']}{marks}\n", f"Künye: {' / '.join(p['sources']) or 'yok'}", f"Yer: {p['places'][0]} ({len(p['places'])} geçiş)\n"]
            shown = p["candidates"] if tier == "chapter" else p["candidates"][:3]
            for c in shown:
                if tier != "chapter" or c["in_cited_chapter"] or c is shown[0]:
                    flag = " **künye bölümü**" if c["in_cited_chapter"] else " künye kitabı" if c["in_cited_book"] else ""
                    lines.append(f"- {c['score']} `{c['hint']}` {c['title']} ({c['report']}){flag}: {c['excerpt']}")
    return "\n".join(lines) + "\n"


def main() -> None:
    print("\n".join(summary(build())))


if __name__ == "__main__":
    main()
