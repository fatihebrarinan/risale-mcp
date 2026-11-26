"""S13.12: konu taramasının dosyası. Kapsamı (bir konunun bütün yerlerini bulmak) sunucu yapar, model önüne konan
sınırlı adaylar üzerinde okur ve yazar (`docs/kipler-plani.md`). Şimdilik yalnız Risale (genel veritabanı).

Bir dosya, risale düzeyindeki bölümlerden (`unit_of`) oluşan aday listesidir. Her aday dört aramanın birinden ya da
birkaçından gelir, neden geldiği (`why`) yanında yazar:

- **named**: konunun sözlerinde adıyla anılan risale (`books/risale_adlari.json`: "İhlâs Risalesi" → Lem'alar 20, 21);
- **heading**: başlıkta ya da alt başlıkta konunun bir kelimesi ("İhlâs Hakkında");
- **words**: konunun kelimelerinin (ekli biçimleriyle, `kelime*`) geçtiği cümle sayısı;
- **meaning**: anlamsal aramanın en yakın `semantic.POOL` cümlesinden bölüme düşenlerin puanı.

Puan bunların ağırlıklı toplamıdır (`_points`); sıra yalnız okunacak yeri seçmeye yardımdır, hüküm değildir: kelimesi
geçen yer konuyu işliyor demek değildir. Her adayda okunacak yer (`focus`: kelimelerin ya da anlamın en çok düştüğü alt
bölümler) ve en yakın cümleler (`closest`) vardır; mektupsa imzası (`signed`).

**Risale düzeyi** (`unit_of`): eserin birinci kat bölümü (Sözler › Onuncu Söz); o bölüm bir kapsa (Lâhikalar,
Tarihçe, Sikke: `CONTAINER_WORKS`; ya da `BIG_UNIT`'ten çok cümle) bir alt kat (mektup). Fihrist bölümleri özettir,
aday olmaz; Hizbler Kur'ân ve dua metnidir. Mecmualar ve ilgili kaynaklar varsayılan
kapsamın dışındadır (aynı metin ana ciltte; ilgili kaynaklar aramaya varsayılan olarak girmez).

    uv run python -m risale_mcp.dosya kur "ihlas" ihlâs* ihlas* samimiyet    # elle bakmak
    uv run python -m risale_mcp.dosya olc                                     # kapsam ölçümü (anlamsal soru seti)
"""

import json
import math
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from risale_mcp import search as fts
from risale_mcp.catalog import Collection

BIG_UNIT = 2500          # bundan çok cümlesi olan birinci kat bölüm bir kaptır; aday onun alt bölümüdür
CANDIDATES = 25          # modele ayrıntısıyla giden aday
OTHERS = 40              # sondaki "öbür yerler" listesine girebilecek en çok aday
CLOSEST = 2              # adayın en yakın cümleleri
FOCUS = 2                # adayın okunacak alt bölümleri
TEXT = 220               # cümle önizlemesi
EXCLUDED_GROUPS = ("mecmua", "osmanlica", "hizb")    # hizbler Kur'ân'ın ve duaların metnidir
# Birinci katı mektup ve parça kapları olan eserler: aday bir alt kattır (Lâhikalarda mektup, Tarihçe'de bölüm)
CONTAINER_WORKS = {"barla-lahikasi", "kastamonu-lahikasi", "emirdag-lahikasi", "tarihce-i-hayat",
                   "sikke-i-tasdik-i-gaybi"}


@dataclass
class Candidate:
    unit: str
    named: bool = False
    headings: list = field(default_factory=list)       # başlığı eşleşen alt bölümler
    words: int = 0
    word_nodes: dict = field(default_factory=lambda: defaultdict(int))
    meaning: float = 0.0
    meaning_hits: list = field(default_factory=list)   # (puan, cümle kimliği, düğüm)
    points: float = 0.0


class Dossier:
    def __init__(self, library) -> None:
        self.library = library
        self.conn = library.conn
        self._unit: dict[str, str] = {}
        self._size: dict[str, int] = {}
        works = self.conn.execute(
            "SELECT slug FROM works WHERE collection = ? AND built = 1 AND group_name NOT IN (%s)"
            % ",".join("?" * len(EXCLUDED_GROUPS)), (Collection.KULLIYAT, *EXCLUDED_GROUPS))
        self.works = {r[0] for r in works}

    # ------------------------------------------------------------ risale düzeyi

    def size(self, node_id: str) -> int:
        if node_id not in self._size:
            node = self.library._node(node_id)
            self._size[node_id] = self.conn.execute(
                "SELECT count(*) FROM sentences s JOIN nodes n ON n.id = s.node_id WHERE n.work = ? AND n.ord BETWEEN ? "
                "AND ? AND s.hasiye = 0", (node["work"], node["ord"], node["last_ord"])).fetchone()[0]
        return self._size[node_id]

    def unit_of(self, node_id: str) -> str | None:
        if node_id in self._unit:
            return self._unit[node_id]
        chain, node = [], node_id
        while node:
            chain.append(node)
            row = self.conn.execute("SELECT parent_id FROM nodes WHERE id = ?", (node,)).fetchone()
            node = row[0] if row else None
        chain.reverse()                       # kök, birinci kat, ikinci kat, …
        unit = None
        if len(chain) >= 2 and not any(part == "fihrist" for part in chain[1].split("/")):   # özet, metin değil
            unit = chain[1]
            container = chain[0] in CONTAINER_WORKS or self.size(unit) > BIG_UNIT
            if container and len(chain) >= 3:
                unit = chain[2]
        self._unit[node_id] = unit
        return unit

    # ------------------------------------------------------------ aramalar

    def build(self, topic: str, terms: list[str] | None = None) -> dict:
        terms = [t.strip() for t in (terms or []) if t and t.strip()]
        cands: dict[str, Candidate] = {}

        def cand(node_id: str) -> Candidate | None:
            unit = self.unit_of(node_id)
            if unit is None or unit.split("/")[0] not in self.works:
                return None
            return cands.setdefault(unit, Candidate(unit))

        for entry in self.library.named(" ".join([topic, *terms])):
            for place in entry["sections"]:
                if (c := cand(place["id"])) is not None:
                    c.named = True
        lexical = " OR ".join(terms) if terms else topic
        try:
            where, params = fts._filters(None, None, Collection.KULLIYAT)
            for (node_id,) in self.conn.execute(
                    "SELECT s.node_id FROM sentences_fts JOIN sentences s ON s.seq = sentences_fts.rowid"
                    f" WHERE sentences_fts MATCH ?{where}", [fts.to_fts(lexical, prefix_all=True), *params]):
                if (c := cand(node_id)) is not None:
                    c.words += 1
                    c.word_nodes[node_id] += 1
            for hit in fts.search_nodes(self.conn, lexical, limit=40, collection=Collection.KULLIYAT, prefix_all=True):
                if (c := cand(hit.node_id)) is not None:
                    c.headings.append(hit.node_id)
        except fts.QueryError:
            pass
        semantic_ok = True
        try:
            index = self.library._semantic_index()
            from risale_mcp.semantic import POOL
            hits, _ = index.search(topic if not terms else f"{topic} ({', '.join(terms)})", self.works, POOL)
            per_unit = defaultdict(int)
            for h in hits:
                if (c := cand(h.node_id)) is not None and per_unit[c.unit] < 5:
                    per_unit[c.unit] += 1
                    c.meaning += h.score
                    c.meaning_hits.append((h.score, h.sentence_id, h.node_id))
        except Exception:                      # vektör ya da anahtar yoksa dosya yine kelimeyle kurulur
            semantic_ok = False
        ranked = self._rank(list(cands.values()))
        out = {"topic": topic, "terms": terms, "candidates": [self._record(c) for c in ranked[:CANDIDATES]],
               "others": [self._brief(c) for c in ranked[CANDIDATES:CANDIDATES + OTHERS]],
               "total_places": len(ranked), "note": NOTE}
        if not semantic_ok:
            out["meaning_search"] = "unavailable: candidates come from words, headings and names only"
        return out

    def _rank(self, cands: list[Candidate]) -> list[Candidate]:
        top_meaning = max((c.meaning for c in cands), default=0) or 1
        top_words = max((c.words for c in cands), default=0) or 1
        for c in cands:
            c.points = (10 * c.named + 3 * bool(c.headings) + 4 * c.meaning / top_meaning
                        + 3 * math.log1p(c.words) / math.log1p(top_words))
        return sorted(cands, key=lambda c: -c.points)

    # ------------------------------------------------------------ kayıtlar

    def _brief(self, c: Candidate) -> dict:
        return {"id": c.unit, "ref": self.library._node(c.unit)["ref"]}

    def _record(self, c: Candidate) -> dict:
        why = []
        if c.named:
            why.append("named")
        if c.headings:
            why.append("heading")
        if c.words:
            why.append(f"words in {c.words} sentences")
        if c.meaning_hits:
            why.append("meaning")
        rec = {**self._brief(c), "why": why, "sentences": self.size(c.unit)}
        focus = []
        for node in [*c.headings, *sorted(c.word_nodes, key=lambda n: -c.word_nodes[n]),
                     *[n for _, _, n in sorted(c.meaning_hits, reverse=True)]]:
            if node not in focus and node != c.unit:
                focus.append(node)
        if focus:
            rec["focus"] = [{"id": n, "ref": self.library._node(n)["ref"]} for n in focus[:FOCUS]]
        closest = []
        for _, sid, _ in sorted(c.meaning_hits, reverse=True)[:CLOSEST]:
            text = self.conn.execute("SELECT text FROM sentences WHERE id = ?", (sid,)).fetchone()[0]
            closest.append({"id": sid, "text": text if len(text) <= TEXT else text[:TEXT - 1] + "…"})
        if closest:
            rec["closest"] = closest
        # imza yalnız mektup düzeyinde (kaptaki aday) ya da adayın kendi metninde: büyük risalenin sonuna eklenmiş bir
        # mektubun imzası bütün risaleye mal edilmesin
        signatures = self.library.profile(self.library._node(c.unit)).get("signatures", [])
        own = [x for x in signatures if x["section"] == c.unit or c.unit.split("/")[0] in CONTAINER_WORKS]
        if own:
            rec["signed"] = own[0]["signed"]
        return rec


NOTE = ("Candidates the page gathered from every search: names of treatises (named), headings, the topic's words "
        "with their suffixed forms, and meaning. why says how each came; a word match alone is not a treatment. "
        "Read the central ones (focus) before relying on them. The page lists the candidates you do not cite at the "
        "end of your answer itself.")


def survey(library, topic: str, terms: list[str] | None = None) -> dict:
    return Dossier(library).build(topic, terms)


# ------------------------------------------------------------ kapsam ölçümü

QUERIES = Path(__file__).resolve().parents[2] / "tests" / "golden" / "semantic_queries.json"


def measure(library) -> dict:
    """Anlamsal soru setinin beklenen bölümlerinden biri (ya da onu içeren/onun içindeki bölüm) dosyanın ilk
    `CANDIDATES` adayında mı; karşılaştırma için anlamsal aramanın beş bölümü. Modelsizdir."""
    data = json.loads(QUERIES.read_text(encoding="utf-8"))
    questions = data["queries"] if isinstance(data, dict) else data
    dossier = Dossier(library)
    hits = {5: 0, 10: 0, CANDIDATES: 0}
    hit_semantic = total = 0
    misses = []
    for q in questions:
        expected = q.get("expected") or q.get("sections") or []
        if not expected:
            continue
        total += 1
        result = dossier.build(q["query"])
        ids = [c["id"] for c in result["candidates"]]
        for k in hits:
            hits[k] += _covers(ids[:k], expected)
        if not _covers(ids, expected):
            misses.append(q["query"])
        sem = [s["id"] for s in library.semantic_search(q["query"], limit=1).get("sections", [])]
        if _covers(sem, expected):
            hit_semantic += 1
    return {"questions": total, **{f"dossier_top{k}": v for k, v in hits.items()}, "semantic_sections_top5": hit_semantic,
            "misses": misses}


def _covers(ids: list[str], expected: list[str]) -> bool:
    return any(e == i or e.startswith(i + "/") or i.startswith(e + "/") for e in expected for i in ids)


def main(argv: list[str] | None = None) -> None:
    from risale_mcp.env import load_env
    from risale_mcp.sohbet import _library
    load_env()
    argv = sys.argv[1:] if argv is None else argv
    library = _library()
    if argv and argv[0] == "kur":
        print(json.dumps(survey(library, argv[1], argv[2:]), ensure_ascii=False, indent=1))
    elif argv and argv[0] == "olc":
        print(json.dumps(measure(library), ensure_ascii=False, indent=1))
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
