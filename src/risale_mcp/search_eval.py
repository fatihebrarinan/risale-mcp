"""Aşama 8: aramanın değerlendirilmesi.

Kullanım:
    uv run python -m risale_mcp.search_eval check          # seti denetle, gözden geçirme sayfasını üret
    uv run python -m risale_mcp.search_eval run words      # bir aramayı ölç (words, words-or, …)

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

from risale_mcp import search as fts
from risale_mcp.db import connect
from risale_mcp.normalize import search_words
from risale_mcp.paths import DB_PATH, INTERIM_DIR, ROOT

QUERIES = ROOT / "tests" / "golden" / "semantic_queries.json"
OUT_DIR = INTERIM_DIR / "search_eval"
DEPTH = 20                 # her aramadan alınan sonuç sayısı
CUTOFFS = (5, 10, 20)

# Arama: (bağlantı, soru, sonuç sayısı) -> cümlelerin düğüm kimlikleri, en uygun önce.
Retriever = Callable[[sqlite3.Connection, str, int], list[str]]


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

def _words(conn: sqlite3.Connection, query: str, k: int) -> list[str]:
    """Bugünkü kelime araması, sorunun kelimeleriyle (hepsi geçmeli)."""
    words = search_words(query)
    return [h.node_id for h in fts.search(conn, " ".join(words), limit=k)] if words else []


def _words_or(conn: sqlite3.Connection, query: str, k: int) -> list[str]:
    """Kelimelerden herhangi biri (BM25 sıralaması): kelime aramasının en iyimser hâli."""
    words = search_words(query)
    return [h.node_id for h in fts.search(conn, " OR ".join(words), limit=k)] if words else []


RETRIEVERS: dict[str, Retriever] = {"words": _words, "words-or": _words_or}


# ---------------------------------------------------------------- ölçüm

def evaluate(conn: sqlite3.Connection, retriever: Retriever, queries: list[Query]) -> list[dict]:
    rows = []
    for q in queries:
        nodes = retriever(conn, q.query, DEPTH)
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


def run(name: str, conn: sqlite3.Connection) -> Path:
    rows = evaluate(conn, RETRIEVERS[name], load_queries())
    summary = summarize(rows)
    lines = [f"# Arama değerlendirmesi: `{name}`", "", f"{datetime.now():%Y-%m-%d %H:%M}, {len(rows)} soru", "",
             " · ".join(f"**{k}** {v:.2f}" for k, v in summary.items()), "",
             "| Soru | | Beklenen bölümün sırası | Beklenen ya da yan |", "|---|---|---|---|",
             *(f"| {r['id']} | {r['query']} | {_rank(r['rank'])} | {_rank(r['any_rank'])} |" for r in rows), ""]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{name}.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(" · ".join(f"{k} {v:.2f}" for k, v in summary.items()))
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
    run_parser = commands.add_parser("run", help="bir aramayı ölç")
    run_parser.add_argument("retriever", choices=sorted(RETRIEVERS))
    parser.add_argument("--db", type=Path, default=DB_PATH)
    args = parser.parse_args()
    conn = connect(args.db)
    if args.command == "check":
        check(conn)
    else:
        run(args.retriever, conn)


if __name__ == "__main__":
    main()
