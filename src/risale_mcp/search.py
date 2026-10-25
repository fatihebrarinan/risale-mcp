"""Cümle ve başlık araması (FTS5, BM25 sıralaması).

Sorgu dili (kullanıcının ya da modelin yazdığı):
    haşir kıyamet          iki kelime de geçmeli
    "haşr-i cismanî"       tam ifade
    haşr*                  kelime başı: haşr, haşre, haşrin…
    haşir OR kıyamet       ikisinden biri
    haşir -kıyamet         kıyamet geçmeyenler
    NEAR(haşir mizan, 5)   en çok 5 kelime arayla

Kelimeler dizindeki biçime (`normalize.search_words`) çevrilir: şapka, çengel, Arapça hareke ve
kesme yok sayılır, ı = i. "hasir" yazmak "Haşr’i"yi de bulur. Bir kelime birden çok parçaya
bölünürse ("Risâle-i") tam ifade olarak aranır.

Sonuçlar `Hit` biçimindedir; ileride anlamsal arama da aynı biçimde sonuç verecek, puanlar
yalnızca kendi aramaları içinde karşılaştırılabilir (büyük = daha iyi).
"""

import re
import sqlite3
from dataclasses import dataclass

from risale_mcp.normalize import search_words

_TOKEN = re.compile(r'"[^"]*"?\*?|NEAR\(|[(),]|[^\s"(),]+')
DEFAULT_NEAR = 10


class QueryError(ValueError):
    pass


@dataclass(frozen=True)
class Hit:
    sentence_id: str
    work: str
    node_id: str
    ref: str
    incipit: str
    text: str
    score: float


@dataclass(frozen=True)
class NodeHit:
    node_id: str
    work: str
    ref: str
    title: str
    subtitle: str | None
    score: float


def _term(raw: str) -> str | None:
    """Bir kelime ya da tırnaklı ifade -> FTS5 ifadesi; aranacak harf yoksa None."""
    prefix = raw.endswith("*")
    words = search_words(raw.rstrip("*").strip('"'))
    if not words:
        return None
    return f'"{" ".join(words)}"' + ("*" if prefix else "")


def _near(tokens: list[str], i: int) -> tuple[str | None, int]:
    """`NEAR(` sonrasını okur: (ifade, kapanıştan sonraki konum)."""
    terms, distance = [], DEFAULT_NEAR
    while i < len(tokens) and tokens[i] != ")":
        token = tokens[i]
        if token == ",":
            if i + 1 >= len(tokens) or not tokens[i + 1].isdigit():
                raise QueryError("NEAR(…, n) içinde virgülden sonra bir sayı olmalı.")
            distance = int(tokens[i + 1])
            i += 2
            continue
        if term := _term(token):
            terms.append(term)
        i += 1
    if i >= len(tokens):
        raise QueryError("NEAR( kapanmamış.")
    if len(terms) < 2:
        return (terms[0] if terms else None), i + 1
    return f"NEAR({' '.join(terms)}, {distance})", i + 1


def to_fts(query: str) -> str:
    """Sorgu dilini FTS5 MATCH ifadesine çevirir. Geçersiz ya da boş sorguda `QueryError`."""
    tokens = _TOKEN.findall(query)
    clauses: list[list[str]] = [[]]
    excluded: list[str] = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        i += 1
        if token == "OR":
            clauses.append([])
            continue
        if token in ("AND", "(", ")", ","):
            continue
        if token == "NEAR(":
            term, i = _near(tokens, i)
        elif token == "NOT" or token == "-":
            if i < len(tokens) and (term := _term(tokens[i])):
                excluded.append(term)
            i += 1
            continue
        elif token.startswith("-") and len(token) > 1:
            if term := _term(token[1:]):
                excluded.append(term)
            continue
        else:
            term = _term(token)
        if term:
            clauses[-1].append(term)

    clauses = [c for c in clauses if c]
    if not clauses:
        raise QueryError("Sorguda aranacak bir kelime yok." if not excluded else
                         "Yalnızca dışlanan kelime var; aranacak bir kelime de yazın.")
    expr = " OR ".join(f"({' AND '.join(c)})" for c in clauses)
    if excluded:
        expr = f"({expr})" + "".join(f" NOT {term}" for term in excluded)
    return expr


def _filters(work: str | None, group: str | None) -> tuple[str, list]:
    sql, params = "", []
    if work:
        sql += " AND s.work = ?"
        params.append(work)
    if group:
        sql += " AND s.work IN (SELECT slug FROM works WHERE group_name = ?)"
        params.append(group)
    return sql, params


def search(conn: sqlite3.Connection, query: str, work: str | None = None, group: str | None = None,
           limit: int = 20, offset: int = 0) -> list[Hit]:
    """Cümle araması, en uygun önce."""
    where, params = _filters(work, group)
    rows = conn.execute(
        "SELECT s.id, s.work, s.node_id, s.ref, s.incipit, s.text, -bm25(sentences_fts) AS score"
        " FROM sentences_fts JOIN sentences s ON s.seq = sentences_fts.rowid"
        f" WHERE sentences_fts MATCH ?{where} ORDER BY bm25(sentences_fts) LIMIT ? OFFSET ?",
        [to_fts(query), *params, limit, offset])
    return [Hit(*row) for row in rows]


def count_by_work(conn: sqlite3.Connection, query: str, group: str | None = None) -> dict[str, int]:
    """Sorguya uyan cümle sayısı, eser başına (katalog sırasıyla)."""
    where, params = _filters(None, group)
    rows = conn.execute(
        "SELECT s.work, count(*) FROM sentences_fts JOIN sentences s ON s.seq = sentences_fts.rowid"
        " JOIN works w ON w.slug = s.work"
        f" WHERE sentences_fts MATCH ?{where} GROUP BY s.work ORDER BY w.ord",
        [to_fts(query), *params])
    return dict(rows.fetchall())


def search_nodes(conn: sqlite3.Connection, query: str, work: str | None = None, limit: int = 20) -> list[NodeHit]:
    """Başlık araması (basılı başlık, alt başlık, içindekiler adı)."""
    where, params = (" AND n.work = ?", [work]) if work else ("", [])
    rows = conn.execute(
        "SELECT n.id, n.work, n.ref, n.title, n.subtitle, -bm25(nodes_fts) AS score"
        " FROM nodes_fts JOIN nodes n ON n.seq = nodes_fts.rowid"
        f" WHERE nodes_fts MATCH ?{where} ORDER BY bm25(nodes_fts), n.seq LIMIT ?",
        [to_fts(query), *params, limit])
    return [NodeHit(*row) for row in rows]
