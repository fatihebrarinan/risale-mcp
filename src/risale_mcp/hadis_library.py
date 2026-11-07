"""Hadis sunucusunun veritabanı katmanı (MVP M5): `hadis_db.py`'nin kurduğu `data/dist/hadis/hadis.db`.

Atıf birimi hadistir (`musned/14870`; numarasız kitapta bizim sıramız `sifa/s00007`). Kur'ân araçları ortak
`Library`'den gelir (aynı şema). Hüküm verilmez: dereceler yalnız kaynağın verdiği (Hadith API'de âlimin adıyla,
Kütüb-i Sitte için) ve başkasının katmanı (`layers`: Zehebî, Elbânî, muhakkik) kimin olduğuyla.
"""

import json
from pathlib import Path

import numpy as np

from risale_mcp import search as fts
from risale_mcp.hadis_kunye import parse as parse_citation
from risale_mcp.library import Library, LibraryError

# künye kitap kimliği (`hadis_kitaplar`) -> kütüphanedeki kitap
CITED_BOOK = {"bukhari": "bukhari", "muslim": "muslim", "abudawud": "abudawud", "tirmidhi": "tirmidhi",
              "nasai": "nasai", "ibnmajah": "ibnmajah", "muvatta": "malik", "musned-ahmed": "musned",
              "sunen-darimi": "darimi", "mucemus-sagir": "mucem-sagir", "mustedrek": "mustedrek",
              "sahih-ibn-hibban": "ihsan", "mecmauz-zevaid": "mecma", "kenzul-ummal": "kenz", "feyzul-kadir": "feyz",
              "keşfu": "kesfulhafa", "sifa": "sifa", "delail-beyhaki": "delail"}
CAUTION = {"kesfulhafa": "This book collects sayings current among people, many weak or baseless: a match here means "
                          "the saying is discussed there, not that it is sound."}
MAX_UNITS = 20
PREVIEW = 300
UNIT_NOTE = ("A report is evidence, not a verdict: never rule on its soundness yourself. layers are other scholars' "
             "notes (by), not the book author's. Grades are given only as the source holds them.")
PAGE_NOTE = ("The citation's volume:page belongs to the edition the citing author used; this library's edition may "
             "differ, so these are the reports printed on that page of this edition, not necessarily the cited one.")


class HadisLibrary(Library):
    """Hadis kitapları üzerine okuma araçları; Kur'ân için `Library`'nin araçları aynen."""

    def books(self) -> dict:
        rows = self.conn.execute("SELECT key, title, author, units, source FROM lib_books ORDER BY ord").fetchall()
        return {"books": [{"id": r["key"], "title": r["title"], "author": r["author"], "reports": r["units"],
                           "edition": _edition(json.loads(r["source"]))} for r in rows],
                "note": "Ids of reports are the edition's numbers (musned/14870) or, in books without numbers, this "
                        "library's sequence (sifa/s00007)."}

    def tree(self, node: str, depth: int = 2) -> dict:
        row = self._lib_node(node)
        return self._tree(row, depth)

    def _tree(self, row, depth: int) -> dict:
        out = {"id": row["id"], "title": row["title"], "level": row["level"], "reports": row["units"]}
        children = self.conn.execute("SELECT * FROM lib_nodes WHERE parent_id = ? ORDER BY seq", (row["id"],)).fetchall()
        if children and depth > 0:
            out["children"] = [self._tree(c, depth - 1) for c in children]
        elif children:
            out["subsections"] = len(children)
        return out

    def chapter(self, node: str, cursor: int = 0, limit: int = MAX_UNITS) -> dict:
        row = self._lib_node(node)
        units = self.conn.execute("SELECT * FROM lib_units WHERE node_id = ? ORDER BY seq LIMIT ? OFFSET ?",
                                  (row["id"], limit + 1, max(cursor, 0))).fetchall()
        out = {"id": row["id"], "title": row["title"], "book": row["book"],
               "reports": [self._unit(u, full=True) for u in units[:limit]]}
        if len(units) > limit:
            out["next_cursor"] = cursor + limit
        if not units:
            out["subsections"] = [{"id": c["id"], "title": c["title"], "reports": c["units"]} for c in
                                  self.conn.execute("SELECT * FROM lib_nodes WHERE parent_id = ? ORDER BY seq",
                                                    (row["id"],)).fetchall()]
        return out

    def report(self, unit_id: str) -> dict:
        row = self.conn.execute("SELECT * FROM lib_units WHERE id = ?", (unit_id,)).fetchone()
        if row is None:
            raise LibraryError(f"No report with id {unit_id!r}; use list_books, read_chapter or search_hadith.")
        out = self._unit(row, full=True)
        places = self.conn.execute("SELECT sentence, display, method, relation FROM lib_risale WHERE unit_id = ?",
                                   (unit_id,)).fetchall()
        if places:
            # Türkçe metin önce, Osmanlıca ciltler (Türkçeyle eşlenmemiş ayrı baskı) sonra.
            places = sorted(places, key=lambda p: "-osmanlica/" in p["sentence"])
            out["in_risale"] = [{"id": p["sentence"], "cite_as": p["display"], "method": p["method"],
                                 "relation": p["relation"]} for p in places]
            out["in_risale_note"] = ("Places in the Risale-i Nur linked to this report (id and citation only; the text "
                                     "is on the Risale-i Nur server). method: corpus = the words occur in the report, "
                                     "cited_chapter = a short part in the cited chapter, reading = two blind readers.")
        out["note"] = UNIT_NOTE
        return out

    def search_reports(self, query: str, book: str | None = None, limit: int = 20, offset: int = 0) -> dict:
        try:
            expr = fts.to_fts(query)
        except fts.QueryError as error:
            raise LibraryError(str(error)) from None
        where, params = (" AND u.book = ?", [book]) if book else ("", [])
        total = self.conn.execute(f"SELECT count(*) FROM lib_fts JOIN lib_units u ON u.seq = lib_fts.rowid"
                                  f" WHERE lib_fts MATCH ?{where}", [expr, *params]).fetchone()[0]
        rows = self.conn.execute(f"SELECT u.* FROM lib_fts JOIN lib_units u ON u.seq = lib_fts.rowid WHERE lib_fts MATCH ?"
                                 f"{where} ORDER BY bm25(lib_fts) LIMIT ? OFFSET ?",
                                 [expr, *params, min(max(limit, 1), 50), max(offset, 0)]).fetchall()
        return {"total": total, "results": [self._unit(r, full=False) for r in rows],
                "note": "Matches the report's text (the matn where the edition separates it). Read a report with "
                        "get_hadith before relying on it."}

    def semantic(self, query: str, book: str | None = None, limit: int = 10, offset: int = 0) -> dict:
        """Anlamca en yakın hadisler (`hadis_vectors.py`: hadis başına, yalnız metin)."""
        from risale_mcp import semantic
        from risale_mcp.embeddings import SEARCH_MODEL, EmbeddingError
        from risale_mcp.hadis_vectors import store
        if not query.strip():
            raise LibraryError("Give a question or a concept to search for.")
        if not hasattr(self, "_vectors"):
            self._vectors = store()
        vectors = self._vectors
        if not vectors.keys:
            raise LibraryError("Semantic search is not available on this server yet (no vectors); use search_hadith.")
        try:
            q = semantic._query_vector(SEARCH_MODEL, query.strip())
        except EmbeddingError as error:
            raise LibraryError(f"Semantic search failed ({error}); use search_hadith with Arabic words.") from None
        scores = vectors.scores(q)
        order = np.argsort(-scores)
        out, skipped = [], 0
        for i in order:
            unit_id = vectors.keys[i].split("|", 1)[0]
            if book and not unit_id.startswith(book + "/"):
                continue
            if skipped < offset:
                skipped += 1
                continue
            row = self.conn.execute("SELECT * FROM lib_units WHERE id = ?", (unit_id,)).fetchone()
            if row is None:
                continue
            out.append({**self._unit(row, full=False), "similarity": round(float(scores[i]), 3)})
            if len(out) >= min(max(limit, 1), 30):
                break
        return {"results": out, "unindexed": max(0, self.conn.execute("SELECT count(*) FROM lib_units").fetchone()[0]
                                                    - len(vectors.keys)),
                "note": "Nearest reports by meaning (the text of each report, not its chain). Candidates: read with "
                        "get_hadith before relying on one."}

    def by_citation(self, citation: str, limit: int = 20) -> dict:
        """Künyeden ("Buharî, Ezân: 148", "Müsned 14870", "Müstedrek, 4:123") kütüphanedeki yer."""
        from risale_mcp.hadis_kutub import Index, load
        parsed = parse_citation(citation).citations
        out = []
        for c in parsed:
            key = CITED_BOOK.get(c.book or "")
            if key is None:
                out.append({"citation": c.raw, "found": False, "note": "This book is not in the library."})
                continue
            for loc in c.locators or []:
                found, note = [], None
                if loc.kind == "chapter" and key in ("bukhari", "muslim", "abudawud", "tirmidhi", "nasai", "ibnmajah", "malik"):
                    index = self._kutub_index(Index, load)
                    found = [self.conn.execute("SELECT * FROM lib_units WHERE id = ?", (h["id"],)).fetchone()
                             for h in _region(index, key, loc.section, loc.number)]
                    note = "The reports in the cited chapter's region (book, chapter number ± a small window)."
                elif loc.kind in ("no", "number", "bare") and (loc.number or "").isdigit():
                    found = self.conn.execute("SELECT * FROM lib_units WHERE book = ? AND number = ? ORDER BY seq",
                                              (key, int(loc.number))).fetchall()
                elif loc.kind in ("volume", "page") and loc.page and str(loc.page).isdigit():
                    found = [r for r in self.conn.execute("SELECT * FROM lib_units WHERE book = ? ORDER BY seq", (key,))
                             if (p := json.loads(r["printed"] or "null")) and p.get("page") == int(loc.page)
                             and (loc.volume is None or p.get("volume") in (None, loc.volume))]
                    note = PAGE_NOTE
                    if loc.volume is not None and any(json.loads(r["printed"]).get("volume") is None for r in found):
                        note += (" This edition's source gives pages without volumes: the reports listed are on that "
                                 "page number in any volume.")
                out.append({"citation": c.raw, "book": key, "found": bool(found), **({"note": note} if note else {}),
                            "reports": [self._unit(r, full=False) for r in found[:limit] if r is not None]})
        if not out:
            raise LibraryError("No book recognised in the citation; give it as e.g. 'Buharî, Ezân: 148' or 'Müsned 14870'.")
        return {"citations": out}

    def cite_reports(self, ids: list[str], first: int = 1) -> dict:
        lines, problems = [], []
        for n, unit_id in enumerate(ids, first):
            row = self.conn.execute("SELECT u.*, b.title AS book_title, b.author, b.source FROM lib_units u"
                                    " JOIN lib_books b ON b.key = u.book WHERE u.id = ?", (unit_id,)).fetchone()
            if row is None:
                problems.append({"id": unit_id, "problem": "unknown report id"})
                continue
            lines.append(f"[{n}] {_cite(row)}")
        return {"problems": len(problems), "issues": problems, "bibliography": "\n".join(lines),
                "note": "Copy the bibliography unchanged under the heading Kaynaklar; sources outside the books go in "
                        "a separate list."}

    # ------------------------------------------------------------ yardımcılar

    def _lib_node(self, node: str):
        row = self.conn.execute("SELECT * FROM lib_nodes WHERE id = ?", (node,)).fetchone()
        if row is None:
            raise LibraryError(f"No book or chapter {node!r}; list_books gives the ids.")
        return row

    def _kutub_index(self, Index, load):
        if not hasattr(self, "_index"):
            self._index = Index(load())
        return self._index

    def _unit(self, row, full: bool) -> dict:
        text = row["text"] if full else (row["text"][:PREVIEW] + ("…" if len(row["text"]) > PREVIEW else ""))
        out = {"id": row["id"], "book": row["book"], "number": row["number"], "text": text}
        if full and row["isnad"] and row["matn"]:
            out["isnad"], out["matn"] = row["isnad"], row["matn"]
        if row["printed"]:
            out["printed"] = json.loads(row["printed"])
        if full and row["layers"]:
            out["layers"] = json.loads(row["layers"])
        if row["book"] in CAUTION:
            out["book_note"] = CAUTION[row["book"]]
        out["cite_as"] = _cite(self.conn.execute("SELECT u.*, b.title AS book_title, b.author, b.source FROM lib_units u"
                                                 " JOIN lib_books b ON b.key = u.book WHERE u.id = ?", (row["id"],)).fetchone())
        return out


def _region(index, book: str, section: int | None, numbers: str | None) -> list[dict]:
    """Künyenin bölgesi. Baskı künyenin kitabını birden çok kitaba bölmüşse (JK'da Buhârî'nin Ezân'ı üç kitap, bâb
    numarası her birinde yeniden başlar) bâblar kitap sırasıyla kesintisiz numaralanır: künyedeki numara (Ezân: 148)
    o kesintisiz sayıdır. Tek kitapta `Index.cited` aynen."""
    from risale_mcp.hadis_kutub import BAB_WINDOW, numbers_of
    kitabs = sorted(index.kitabs.get((book, section), ()), key=lambda k: int(k.rsplit("k", 1)[1]) if k.rsplit("k", 1)[1].isdigit() else 0)
    if len(kitabs) < 2 or book not in BAB_WINDOW or not (wanted := numbers_of(numbers)):
        return index.cited(book, section, numbers)
    out, offset = [], 0
    for kitab in kitabs:
        top = 0
        for h in index.in_kitab.get(kitab, ()):
            bab = index.place[h["id"]][1]
            if bab is None:
                continue
            top = max(top, bab)
            if any(abs(offset + bab - n) <= BAB_WINDOW[book] for n in wanted):
                out.append(h)
        offset += top
    return out


def _edition(source: dict) -> str | None:
    ed = source.get("edition") or {}
    parts = [ed.get(k) for k in ("editor", "publisher", "edition") if ed.get(k)]
    return ", ".join(parts) or None


def _cite(row) -> str:
    number = f"no. {row['number']}" if row["number"] is not None else f"sıra {row['id'].split('/', 1)[1]} (baskıda numara yok)"
    printed = json.loads(row["printed"] or "null")
    page = (f", {printed['volume']}/{printed['page']}" if printed and printed.get("volume")
            else f", s. {printed['page']} (cilt bilinmiyor)" if printed else "")   # kaynak yalnız [ص: n] veriyor
    return f"{row['book_title']} ({row['author']}), {number}{page}"
