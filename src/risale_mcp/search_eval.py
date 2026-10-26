"""Aşama 8: aramanın değerlendirilmesi.

Kullanım:
    uv run python -m risale_mcp.search_eval check          # seti denetle, gözden geçirme sayfasını üret
    uv run python -m risale_mcp.search_eval run words      # bir aramayı ölç
    uv run --env-file .env python -m risale_mcp.search_eval run words-or semantic:voyage-4-large hybrid:voyage-4-large

Aramalar: `words` (bugünkü kelime araması, bütün kelimeler geçmeli), `words-or` (kelimelerden biri),
`semantic:<model>[:<seçenek>]` (vektör araması; `embeddings.py`), `hybrid:<model>[:<seçenek>]`
(vektör ve `words-or` sonuçları RRF ile birleşir). Birden çok arama verilirse karşılaştırma tablosu yazılır.

Değerlendirme seti `tests/golden/semantic_queries.json`'dadır: günümüz Türkçesiyle sorulmuş
kavramlar ve her birinin asıl işlendiği bölümler (`expected`), kabul edilen yan bölümler
(`related`). Bir arama sonucu, cümlesi bu bölümlerden birinin altındaysa isabettir.

Ölçüler (her soru için ilk isabetin sırasından):
- hit@k: beklenen bölümden bir cümle ilk k sonuçta mı (k = 5, 10, 20)
- MRR: ilk isabetin sırasının tersi, sorular üzerinden ortalama (isabet yoksa 0)
- any@10: beklenen ya da yan bölümden bir cümle ilk 10 sonuçta mı

`evidence` alanı yalnızca seti kurarken beklenen yeri doğrulamak içindir; ölçümde kullanılmaz.
Gözden geçirme sayfası `data/interim/search_eval/review.md`, ölçüm raporları aynı klasördedir.
"""

import argparse
import json
import sqlite3
import sys
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from risale_mcp import embeddings
from risale_mcp import search as fts
from risale_mcp.db import connect
from risale_mcp.normalize import search_words
from risale_mcp.paths import DB_PATH, INTERIM_DIR, ROOT

QUERIES = ROOT / "tests" / "golden" / "semantic_queries.json"
OUT_DIR = INTERIM_DIR / "search_eval"
DEPTH = 20                 # her aramadan alınan sonuç sayısı
CUTOFFS = (5, 10, 20)
RRF_K = 60                 # karma aramada sıraların birleştirilmesi: puan = Σ 1 / (RRF_K + sıra)
POOL = 100                 # karma aramada her aramadan alınan sonuç

# Arama: (bağlantı, soru, sonuç sayısı) -> (cümle, düğüm) listesi, en uygun önce.
Retriever = Callable[[sqlite3.Connection, str, int], list[tuple[str, str]]]


@dataclass(frozen=True)
class Query:
    id: str
    query: str
    expected: list[str]
    related: list[str]
    evidence: str


def load_queries(path: Path = QUERIES) -> list[Query]:
    return [Query(**q) for q in json.loads(path.read_text(encoding="utf-8"))["queries"]]


def within(node: str, sections: list[str]) -> bool:
    return any(node == s or node.startswith(s + "/") for s in sections)


def first_rank(nodes: list[str], sections: list[str]) -> int | None:
    """İlk isabetin sırası (1'den başlar)."""
    return next((i for i, node in enumerate(nodes, 1) if within(node, sections)), None)


# ---------------------------------------------------------------- aramalar

def _words(conn: sqlite3.Connection, query: str, k: int) -> list[tuple[str, str]]:
    """Bugünkü kelime araması, sorunun kelimeleriyle (hepsi geçmeli)."""
    words = search_words(query)
    return [(h.sentence_id, h.node_id) for h in fts.search(conn, " ".join(words), limit=k)] if words else []


def _words_or(conn: sqlite3.Connection, query: str, k: int) -> list[tuple[str, str]]:
    """Kelimelerden herhangi biri (BM25 sıralaması): kelime aramasının en iyimser hâli."""
    words = search_words(query)
    return [(h.sentence_id, h.node_id) for h in fts.search(conn, " OR ".join(words), limit=k)] if words else []


def _semantic(spec: str) -> Retriever:
    """`<model>[:<seçenek>]` için vektör araması. Birimler ilk çağrıda bir kez okunur."""
    name, _, variant = spec.partition(":")
    model = embeddings.MODELS[name]
    variant = variant or ("context" if model.contextual else "sentence")
    store = embeddings.VectorStore(model.name, variant)
    if not store.keys:
        sys.exit(f"{name}.{variant} için vektör yok; önce `python -m risale_mcp.embeddings build {name}`.")
    sentences: dict[str, list[tuple[str, str]]] = {}

    def retrieve(conn: sqlite3.Connection, query: str, k: int) -> list[tuple[str, str]]:
        if not sentences:
            sentences.update((u.key, u.sentences) for u in embeddings.units(conn, variant))
        out = []
        for key, _ in store.nearest(embeddings.query_vector(model, query), list(sentences), k):
            out += sentences[key]
        return out[:k]
    return retrieve


def _hybrid(spec: str) -> Retriever:
    semantic = _semantic(spec)

    def retrieve(conn: sqlite3.Connection, query: str, k: int) -> list[tuple[str, str]]:
        return rrf([semantic(conn, query, POOL), _words_or(conn, query, POOL)])[:k]
    return retrieve


def rrf(rankings: list[list[tuple[str, str]]]) -> list[tuple[str, str]]:
    """Sıralamaların birleşimi (Reciprocal Rank Fusion): puanlar değil sıralar toplanır."""
    scores: dict[tuple[str, str], float] = {}
    for ranking in rankings:
        for rank, hit in enumerate(ranking, 1):
            scores[hit] = scores.get(hit, 0) + 1 / (RRF_K + rank)
    return sorted(scores, key=lambda hit: -scores[hit])


def retriever(name: str) -> Retriever:
    if name in ("words", "words-or"):
        return {"words": _words, "words-or": _words_or}[name]
    kind, _, spec = name.partition(":")
    if kind not in ("semantic", "hybrid") or spec.split(":")[0] not in embeddings.MODELS:
        sys.exit(f"Bilinmeyen arama {name!r}; modeller: {', '.join(embeddings.MODELS)}.")
    return _semantic(spec) if kind == "semantic" else _hybrid(spec)


# ---------------------------------------------------------------- ölçüm

def evaluate(conn: sqlite3.Connection, retriever: Retriever, queries: list[Query]) -> list[dict]:
    rows = []
    for q in queries:
        nodes = [node for _, node in retriever(conn, q.query, DEPTH)]
        rows.append({"id": q.id, "query": q.query, "rank": first_rank(nodes, q.expected),
                     "any_rank": first_rank(nodes, q.expected + q.related)})
    return rows


def summarize(rows: list[dict]) -> dict:
    n = len(rows)
    out = {f"hit@{k}": sum(r["rank"] is not None and r["rank"] <= k for r in rows) / n for k in CUTOFFS}
    out["MRR"] = sum(1 / r["rank"] for r in rows if r["rank"]) / n
    out["any@10"] = sum(r["any_rank"] is not None and r["any_rank"] <= 10 for r in rows) / n
    return out


def _rank(rank: int | None) -> str:
    return str(rank) if rank else "—"


def run(names: list[str], conn: sqlite3.Connection) -> Path:
    """Aramaları ölçer; özet tablo ve soru başına beklenen bölümün sırası (yan bölümler parantez içinde)."""
    queries = load_queries()
    results = {name: evaluate(conn, retriever(name), queries) for name in names}
    summaries = {name: summarize(rows) for name, rows in results.items()}
    metrics = list(next(iter(summaries.values())))
    lines = ["# Arama değerlendirmesi", "", f"{datetime.now():%Y-%m-%d %H:%M}, {len(queries)} soru", "",
             "| Arama | " + " | ".join(metrics) + " |", "|---|" + "---|" * len(metrics),
             *(f"| `{name}` | " + " | ".join(f"{v:.2f}" for v in summary.values()) + " |"
               for name, summary in summaries.items()),
             "", "Soru başına beklenen bölümün sırası (— = ilk 20'de yok; parantez içinde yan bölümler dahil):", "",
             "| Soru | | " + " | ".join(f"`{n}`" for n in names) + " |", "|---|---|" + "---|" * len(names)]
    for i, q in enumerate(queries):
        cells = [f"{_rank(results[n][i]['rank'])} ({_rank(results[n][i]['any_rank'])})" for n in names]
        lines.append(f"| {q.id} | {q.query} | " + " | ".join(cells) + " |")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / ("compare.md" if len(names) > 1 else f"{names[0].replace(':', '_')}.md")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    width = max(map(len, names))
    for name, summary in summaries.items():
        print(f"{name:{width}}  " + " · ".join(f"{k} {v:.2f}" for k, v in summary.items()))
    print(f"rapor: {out.relative_to(ROOT)}")
    return out


# ---------------------------------------------------------------- setin denetimi

def _evidence(conn: sqlite3.Connection, section: str, evidence: str) -> tuple[int, str | None]:
    """Kanıt terimlerinin bölümde kaç cümlede geçtiği ve en uygun cümle."""
    node = conn.execute("SELECT work, ord, last_ord FROM nodes WHERE id = ?", (section,)).fetchone()
    params = [fts.to_fts(evidence), node["work"], node["work"], node["ord"], node["last_ord"]]
    where = (" WHERE sentences_fts MATCH ? AND s.work = ?"
             " AND s.node_id IN (SELECT id FROM nodes WHERE work = ? AND ord BETWEEN ? AND ?)")
    base = " FROM sentences_fts JOIN sentences s ON s.seq = sentences_fts.rowid" + where
    count = conn.execute("SELECT count(*)" + base, params).fetchone()[0]
    best = conn.execute("SELECT s.text" + base + " ORDER BY bm25(sentences_fts) LIMIT 1", params).fetchone()
    return count, best[0] if best else None


def check(conn: sqlite3.Connection) -> Path:
    """Kimlikleri doğrular; her soru için beklenen bölümleri, kanıtları ve kelime aramasının sonucunu yazar."""
    queries = load_queries()
    problems = []
    if len({q.id for q in queries}) != len(queries):
        problems.append("soru kimlikleri tekil değil")
    nodes = {r["id"]: r for r in conn.execute("SELECT id, ref, subtitle FROM nodes")}
    for q in queries:
        problems += [f"{q.id}: bilinmeyen bölüm {s}" for s in q.expected + q.related if s not in nodes]
        if not q.expected:
            problems.append(f"{q.id}: beklenen bölüm yok")
    if problems:
        sys.exit("\n".join(problems))

    words = {r["id"]: r for r in evaluate(conn, _words, queries)}
    words_or = {r["id"]: r for r in evaluate(conn, _words_or, queries)}
    intro = ("Her soru için: beklenen bölümler (asıl işlendiği yer), yan bölümler ve bugünkü kelime aramasının "
             "beklenen bölümü kaçıncı sırada bulduğu (— = ilk 20'de yok). Kanıt: metindeki terimlerin o bölümde "
             "geçtiği cümle sayısı ve en uygun cümle.")
    lines = ["# Anlamsal arama değerlendirme seti", "", intro, ""]
    for q in queries:
        baseline = (f"Kelime araması: hepsi geçmeli {_rank(words[q.id]['rank'])}, herhangi biri "
                    f"{_rank(words_or[q.id]['rank'])} · kanıt terimleri: `{q.evidence}`")
        lines += [f"## {q.id} · {q.query}", "", baseline, "", "Beklenen:"]
        for s in q.expected:
            count, best = _evidence(conn, s, q.evidence)
            subtitle = f" — *{nodes[s]['subtitle']}*" if nodes[s]["subtitle"] else ""
            lines.append(f"- `{s}` {nodes[s]['ref']}{subtitle} · kanıt: {count} cümle")
            if best:
                lines.append(f"  > {best[:300]}")
        if q.related:
            lines += ["", "Yan: " + "; ".join(nodes[s]["ref"] for s in q.related)]
        lines += ["", "⬜ uygun ⬜ değiştir — not:", ""]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / "review.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    for name, rows in (("words", words), ("words-or", words_or)):
        print(f"{name}: " + " · ".join(f"{k} {v:.2f}" for k, v in summarize(list(rows.values())).items()))
    print(f"{len(queries)} soru; gözden geçirme: {out.relative_to(ROOT)}")
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check", help="seti denetle, gözden geçirme sayfasını üret")
    run_parser = commands.add_parser("run", help="aramaları ölç ve karşılaştır")
    run_parser.add_argument("retrievers", nargs="+", help="words, words-or, semantic:<model>, hybrid:<model>")
    parser.add_argument("--db", type=Path, default=DB_PATH)
    args = parser.parse_args()
    conn = connect(args.db)
    if args.command == "check":
        check(conn)
    else:
        run(args.retrievers, conn)


if __name__ == "__main__":
    main()
