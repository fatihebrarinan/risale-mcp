"""Cümle ve başlık araması (FTS5, BM25 sıralaması).

Sorgu dili (kullanıcının ya da modelin yazdığı):
    haşir kıyamet          iki kelime de geçmeli
    "haşr-i cismanî"       tam ifade
    haşr*                  kelime başı: haşr, haşre, haşrin…
    الكتاب                 Arapça kelime önekli biçimleriyle de: والكتاب، بالكتاب، للكتاب، كتاب…
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


_ARABIC = re.compile(r"[\u0600-\u06FF]")
# Arapça kelimenin başına bitişen bağlaç ve harf-i cerler (و ف ب ل ك ve birleşimleri) ve harf-i tarif: dizinde
# "والكتاب" tek kelimedir; "الكتاب" ya da "كتاب" arayan onu da bulmalı (MVP M4). Sorgu tarafında açılır, dizin değişmez.
_PROCLITICS = ("", "و", "ف", "ب", "ل", "ك", "وب", "ول", "فب", "فل", "وك", "فك")


def arabic_forms(word: str) -> list[str]:
    """Arapça kelimenin önekli biçimleri: harf-i tarifli ve tarifsiz, bağlaç ve harf-i cerli ("لل…" dahil)."""
    core = word[2:] if word.startswith("ال") and len(word) > 3 else word
    forms = {p + core for p in _PROCLITICS} | {p + "ال" + core for p in _PROCLITICS}
    forms |= {"لل" + core, "ولل" + core, "فلل" + core}
    forms.discard("")
    return sorted(forms, key=lambda f: (f != word, len(f), f))


# Hadis metinlerinde "ابن" ile "بن" aynı yerde ikisi de yazılır ("المسيح بن مريم" / "ابن مريم"): hadis dizini ve
# sorgusu ikisini "بن"e indirir (2026-11-09; Risale'nin dizini değişmez). Yalnız yalın ve و/ف'li biçim: "لابن",
# "بابن" "لبن" (süt) gibi başka kelimelere düşmesin diye olduğu gibi kalır.
_IBN = re.compile(r"([وف]?)ابن")
_BIN_FORMS = ("بن", "وبن", "فبن", "لابن", "بابن", "كابن", "ولابن", "وبابن")


def hadith_word(word: str) -> str:
    """Hadis dizininin kelimesi: "ابن"/"وابن"/"فابن" -> "بن"/"وبن"/"فبن"."""
    m = _IBN.fullmatch(word)
    return m[1] + "بن" if m else word


def _term(raw: str, prefix_all: bool = False, canon=None) -> str | None:
    """Bir kelime ya da tırnaklı ifade -> FTS5 ifadesi; aranacak harf yoksa None. Tırnaksız tek Arapça kelime
    önekli biçimleriyle aranır; `prefix_all`: tırnaksız tek kelime kelime başı olarak aranır (Türkçe ek). `canon`:
    dizinin kelime biçimi (hadis dizini: `hadith_word`)."""
    prefix = raw.endswith("*")
    quoted = raw.startswith('"')
    words = search_words(raw.rstrip("*").strip('"'))
    if canon:
        words = [canon(w) for w in words]
    if not words:
        return None
    if len(words) == 1 and not quoted and _ARABIC.search(words[0]):
        forms = _BIN_FORMS if canon and words[0] in _BIN_FORMS[:3] else arabic_forms(words[0])
        return "(" + " OR ".join(f'"{f}"' + ("*" if prefix else "") for f in forms) + ")"
    if prefix_all and len(words) == 1 and not quoted:
        prefix = True
    return f'"{" ".join(words)}"' + ("*" if prefix else "")


def _near(tokens: list[str], i: int, canon=None) -> tuple[str | None, int]:
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
        if term := _term(token, canon=canon):
            terms.append(term)
        i += 1
    if i >= len(tokens):
        raise QueryError("NEAR( kapanmamış.")
    if len(terms) < 2:
        return (terms[0] if terms else None), i + 1
    return f"NEAR({' '.join(terms)}, {distance})", i + 1


def to_fts(query: str, prefix_all: bool = False, canon=None) -> str:
    """Sorgu dilini FTS5 MATCH ifadesine çevirir. Geçersiz ya da boş sorguda `QueryError`. `prefix_all`: dışlanmayan
    tırnaksız kelimeler kelime başı olarak aranır (sonuçsuz sorguda Türkçe ek için ikinci deneme). `canon`: dizinin
    kelime biçimi (`_term`)."""
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
            term, i = _near(tokens, i, canon)
        elif token == "NOT" or token == "-":
            if i < len(tokens) and (term := _term(tokens[i], canon=canon)):
                excluded.append(term)
            i += 1
            continue
        elif token.startswith("-") and len(token) > 1:
            if term := _term(token[1:], canon=canon):
                excluded.append(term)
            continue
        else:
            term = _term(token, prefix_all, canon)
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


def _filters(work: str | None, group: str | None, collection: str | None = None) -> tuple[str, list]:
    sql, params = "", []
    if work:
        sql += " AND s.work = ?"
        params.append(work)
    if group:
        sql += " AND s.work IN (SELECT slug FROM works WHERE group_name = ?)"
        params.append(group)
    if collection:
        sql += " AND s.work IN (SELECT slug FROM works WHERE collection = ?)"
        params.append(collection)
    return sql, params


def search(conn: sqlite3.Connection, query: str, work: str | None = None, group: str | None = None,
           limit: int = 20, offset: int = 0, collection: str | None = None, prefix_all: bool = False) -> list[Hit]:
    """Cümle araması, en uygun önce."""
    where, params = _filters(work, group, collection)
    rows = conn.execute(
        "SELECT s.id, s.work, s.node_id, s.ref, s.incipit, s.text, -bm25(sentences_fts) AS score"
        " FROM sentences_fts JOIN sentences s ON s.seq = sentences_fts.rowid"
        f" WHERE sentences_fts MATCH ?{where} ORDER BY bm25(sentences_fts) LIMIT ? OFFSET ?",
        [to_fts(query, prefix_all), *params, limit, offset])
    return [Hit(*row) for row in rows]


def count_by_work(conn: sqlite3.Connection, query: str, group: str | None = None,
                  collection: str | None = None, prefix_all: bool = False) -> dict[str, int]:
    """Sorguya uyan cümle sayısı, eser başına (katalog sırasıyla)."""
    where, params = _filters(None, group, collection)
    rows = conn.execute(
        "SELECT s.work, count(*) FROM sentences_fts JOIN sentences s ON s.seq = sentences_fts.rowid"
        " JOIN works w ON w.slug = s.work"
        f" WHERE sentences_fts MATCH ?{where} GROUP BY s.work ORDER BY w.ord",
        [to_fts(query, prefix_all), *params])
    return dict(rows.fetchall())


def search_nodes(conn: sqlite3.Connection, query: str, work: str | None = None, limit: int = 20,
                 collection: str | None = None, prefix_all: bool = False) -> list[NodeHit]:
    """Başlık araması (basılı başlık, alt başlık, içindekiler adı)."""
    where, params = (" AND n.work = ?", [work]) if work else ("", [])
    if collection:
        where += " AND n.work IN (SELECT slug FROM works WHERE collection = ?)"
        params.append(collection)
    rows = conn.execute(
        "SELECT n.id, n.work, n.ref, n.title, n.subtitle, -bm25(nodes_fts) AS score"
        " FROM nodes_fts JOIN nodes n ON n.seq = nodes_fts.rowid"
        f" WHERE nodes_fts MATCH ?{where} ORDER BY bm25(nodes_fts), n.seq LIMIT ?",
        [to_fts(query, prefix_all), *params, limit])
    return [NodeHit(*row) for row in rows]
