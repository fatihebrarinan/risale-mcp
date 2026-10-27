"""Veritabanı üzerindeki okuma işleri: MCP araçlarının asıl işi (Aşama 6).

`server.py` yalnızca bunları çağırır; burada MCP yoktur, böylece sorgular protokolden bağımsız
sınanır. Sonuçlar JSON'a çevrilebilir sözlüklerdir. Modelin okuyacağı hata iletileri İngilizcedir
(`LibraryError`); araç katmanı onları olduğu gibi modele iletir.

Okuma birimleri:
- Düğüm (`sozler/10`) başlık ağacının bir öğesidir; kendi metni ve alt bölümleri vardır.
- `read_section` bir düğümü alt bölümleriyle birlikte, kitap sırasıyla ve parça parça okur.
  Parçalar paragraf sınırında kesilir; `next_cursor` sonraki parçanın ilk paragrafıdır.
- Mecmuada ana cilde eşlenmiş paragrafın metni ana ciltteki cümlelerle gelir; atıf oraya yapılır.
- Cümle ve hâşiye kimlikleri eser verisindeki gibi kalıcıdır (`sozler/10/c032/h1/c002`).
"""

import re
import sqlite3
from collections import defaultdict
from itertools import accumulate
from pathlib import Path

from risale_mcp import search as fts
from risale_mcp.db import connect
from risale_mcp.embeddings import EmbeddingError
from risale_mcp.normalize import search_words
from risale_mcp.paths import DB_PATH
from risale_mcp.semantic import SemanticIndex, SemanticUnavailable

MAX_RANGE = 100          # get_passage'ın bir seferde döndürdüğü en çok cümle
MAX_CITED = 8            # tek atıfla verilebilecek en çok ardışık cümle (aynı bölümde)
MAX_RESULTS = 50
PREVIEW_CHARS = 400      # arama sonucunda gösterilen en uzun cümle metni
ANNOTATED_ARABIC = ("ayet", "hadis")   # okurken meali ve kaynağı gösterilen Arapça türleri
MAX_LINKS = 30           # find_ayah'ın bir âyet için döndürdüğü en çok ilişki
MAX_AYAHS = 30           # get_ayah'ın bir seferde döndürdüğü en çok âyet (bağlam hariç)
QURAN_ATTRIBUTION = ("Arabic text: Tanzil Project (tanzil.net), Medina Mushaf script. Translations: Diyanet İşleri "
                     "Başkanlığı and Türkiye Diyanet Vakfı, via Tanzil (non-commercial use).")
# Kaynağın âyet numarası Kur'ân metniyle tutmuyorsa modele giden uyarı (build_db, `ayah_check`).
AYAH_CHECK_NOTES = {
    "near": "the quoted text is in a neighbouring verse, not exactly the one the source names",
    "differs": "the quoted text does not match the named verse word for word (adapted quotation, abridgement "
               "or a wrong number in the source)",
}


class LibraryError(ValueError):
    """Modelin düzeltebileceği hata: bilinmeyen kimlik, geçersiz sorgu…"""


def _preview(text: str) -> str:
    return text if len(text) <= PREVIEW_CHARS else text[:PREVIEW_CHARS].rsplit(" ", 1)[0] + " …"


def opening(incipit: str, text: str) -> str:
    """Kullanıcıya gösterilen ilk kelimeler; cümle daha uzunsa "…" ile."""
    return incipit if len(incipit) >= len(text.rstrip()) else incipit + "…"


def cite(section_ref: str, opening_words: str, count: int = 1) -> str:
    """Kullanıcıya gösterilen atıf: yol › “ilk kelimeler…”; ardışık cümlelerde “…” ile başlayan N cümle."""
    quoted = f"{section_ref} › “{opening_words}”"
    return quoted if count == 1 else f"{quoted} ile başlayan {count} cümle"


def _ayah_span(start: int, end: int) -> str:
    return f"{start}" if start == end else f"{start}-{end}"


def _placeholders(items) -> str:
    return ",".join("?" * len(items))


class Library:
    def __init__(self, path: Path = DB_PATH, vectors_dir: Path | None = None) -> None:
        self.path = path
        self.vectors_dir = vectors_dir
        self._conn: sqlite3.Connection | None = None
        self._version: int | None = None
        self._semantic: tuple[sqlite3.Connection, SemanticIndex] | None = None

    @property
    def conn(self) -> sqlite3.Connection:
        """Veritabanı yeniden kurulunca (`build_db` dosyayı değiştirir) bağlantı yenilenir."""
        version = self.path.stat().st_mtime_ns if self.path.exists() else None
        if self._conn is None or version != self._version:
            self.close()
            self._conn, self._version = connect(self.path), version
        return self._conn

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    # ------------------------------------------------------------ eserler ve başlık ağacı

    def works(self, group: str | None = None) -> list[dict]:
        sentences = dict(self.conn.execute("SELECT work, count(*) FROM sentences GROUP BY work").fetchall())
        sections = dict(self.conn.execute("SELECT work, count(*) FROM nodes GROUP BY work").fetchall())
        rows = self.conn.execute(
            "SELECT slug, title, group_name, language, status, note, built FROM works"
            + (" WHERE group_name = ?" if group else "") + " ORDER BY ord", [group] if group else []).fetchall()
        if group and not rows:
            groups = [r[0] for r in self.conn.execute("SELECT DISTINCT group_name FROM works ORDER BY ord")]
            raise LibraryError(f"Unknown group {group!r}; groups are: {', '.join(groups)}.")
        out = []
        for w in rows:
            record = {"id": w["slug"], "title": w["title"], "group": w["group_name"], "language": w["language"]}
            if w["built"]:
                record |= {"sections": sections[w["slug"]], "sentences": sentences.get(w["slug"], 0)}
            else:
                record |= {"available": False, "status": w["status"]}
            if w["note"]:
                record["note"] = w["note"]
            out.append(record)
        return out

    def _node(self, node_id: str) -> sqlite3.Row:
        row = self.conn.execute("SELECT * FROM nodes WHERE id = ?", (node_id,)).fetchone()
        if row is None:
            hint = "use get_outline to see section ids" if "/" in node_id else "use list_works for work ids"
            raise LibraryError(f"No section with id {node_id!r}; {hint}.")
        return row

    def _subtree(self, node: sqlite3.Row, max_depth: int | None = None) -> list[sqlite3.Row]:
        sql = "SELECT * FROM nodes WHERE work = ? AND ord BETWEEN ? AND ?"
        params: list = [node["work"], node["ord"], node["last_ord"]]
        if max_depth is not None:
            sql += " AND depth <= ?"
            params.append(max_depth)
        return self.conn.execute(sql + " ORDER BY ord", params).fetchall()

    def outline(self, node_id: str, depth: int = 2) -> dict:
        """Düğüm ve `depth` kat alt bölümü; her düğümde alt ağacının ana metin cümle sayısı.
        Derinlik sınırında gizlenen alt bölümlerin sayısı `subsections`'dadır."""
        root = self._node(node_id)
        subtree = self._subtree(root)
        own = dict(self.conn.execute(
            "SELECT node_id, count(*) FROM sentences WHERE work = ? AND hasiye = 0 GROUP BY node_id",
            (root["work"],)).fetchall())
        # Alt ağaç kitap sırasında ord..last_ord aralığıdır; sayımlar önek toplamlarından bulunur.
        prefix = [0, *accumulate(own.get(n["id"], 0) for n in subtree)]
        first = root["ord"]
        child_count = defaultdict(int)
        for n in subtree:
            child_count[n["parent_id"]] += 1

        records: dict[str, dict] = {}
        for n in subtree:
            if n["depth"] > root["depth"] + max(depth, 0):
                continue
            record = {"id": n["id"], "title": n["title"]}
            if n["subtitle"]:
                record["subtitle"] = n["subtitle"]
            record["sentences"] = prefix[n["last_ord"] - first + 1] - prefix[n["ord"] - first]
            if n["id"] != root["id"]:
                records[n["parent_id"]].setdefault("children", []).append(record)
            records[n["id"]] = record
        for node_id_, record in records.items():
            if "children" not in record and child_count[node_id_]:
                record["subsections"] = child_count[node_id_]
        return {"work": root["work"], "ref": root["ref"], **records[root["id"]]}

    # ------------------------------------------------------------ okuma

    def read_section(self, node_id: str, cursor: str | None = None, max_words: int = 1500) -> dict:
        """Bölümü alt bölümleriyle birlikte kitap sırasıyla okur: başlıklar, paragraflar (cümleleriyle),
        hâşiyeler ve kaynaktaki eksikler. `max_words`'ü aşmadan paragraf sınırında keser."""
        root = self._node(node_id)
        nodes = self._subtree(root)
        node_ord = {n["id"]: n["ord"] for n in nodes}
        paragraphs = self.conn.execute(
            "SELECT p.* FROM paragraphs p JOIN nodes n ON n.id = p.node_id"
            " WHERE n.work = ? AND n.ord BETWEEN ? AND ? ORDER BY p.ord",
            (root["work"], root["ord"], root["last_ord"])).fetchall()

        start = 0
        if cursor is not None:
            start = next((i for i, p in enumerate(paragraphs) if p["id"] == cursor), None)
            if start is None:
                raise LibraryError(f"Cursor {cursor!r} is not in section {node_id!r}; pass the next_cursor value as is.")
        # Önce sayfanın paragraflarını seç; cümleleri yalnızca onlar için oku.
        page, words = [], 0
        for p in paragraphs[start:]:
            cost = len((p["text"] or "").split()) or 50      # eşlenmiş paragrafın metni ana ciltte
            if page and words + cost > max_words:
                break
            page.append(p)
            words += cost
        next_cursor = paragraphs[start + len(page)]["id"] if start + len(page) < len(paragraphs) else None

        texts = self._paragraph_texts(page)
        gaps = defaultdict(list)
        for g in self.conn.execute("SELECT node_id, after, missing_blocks, note FROM gaps WHERE work = ?",
                                   (root["work"],)):
            gaps[g["after"] or g["node_id"]].append(
                {"gap": g["note"] or f"{g['missing_blocks']} block(s) missing at the source; text not invented."})

        verses = defaultdict(list)
        for v in self.conn.execute(
                "SELECT l.node_id, l.kind, l.sura, l.ayah_start, l.ayah_end, l.evidence_id FROM ayah_links l"
                " JOIN nodes n ON n.id = l.node_id WHERE l.scope = 'section' AND n.work = ? AND n.ord BETWEEN ? AND ?"
                " ORDER BY l.rowid", (root["work"], root["ord"], root["last_ord"])):
            verses[v["node_id"]].append({"verse": self._verse_ref(v["sura"], v["ayah_start"], v["ayah_end"]),
                                         "kind": v["kind"], "evidence": v["evidence_id"]})
        items: list[dict] = []
        heading_at = 0
        first_ord = node_ord[page[0]["node_id"]] if page else root["ord"]
        while heading_at < len(nodes) and nodes[heading_at]["ord"] < first_ord:
            heading_at += 1                  # devam eden okumada önceki başlıklar zaten verildi

        def headings_until(ord_: int, continued: bool = False) -> None:
            nonlocal heading_at
            while heading_at < len(nodes) and nodes[heading_at]["ord"] <= ord_:
                n = nodes[heading_at]
                item = {"section": n["id"], "title": n["title"], "ref": n["ref"]}
                if n["subtitle"]:
                    item["subtitle"] = n["subtitle"]
                if n["id"] in verses:
                    item["linked_verses"] = verses[n["id"]]
                if continued and n["ord"] == ord_:
                    item["continued"] = True
                items.append(item)
                items.extend(gaps.get(n["id"], []))
                heading_at += 1

        for i, p in enumerate(page):
            headings_until(node_ord[p["node_id"]], continued=cursor is not None and i == 0)
            items.append(texts[p["id"]])
            items.extend(gaps.get(p["id"], []))
        if next_cursor is None:
            headings_until(root["last_ord"])           # metinsiz son alt bölümler
        return {"section": root["id"], "ref": root["ref"], "items": items, "next_cursor": next_cursor}

    def _paragraph_texts(self, paragraphs: list[sqlite3.Row]) -> dict[str, dict]:
        """Paragraf -> {id, kind, sentences, arabic?, hasiye_of?, canonical?}."""
        if not paragraphs:
            return {}
        ids = [p["id"] for p in paragraphs]
        canonical = defaultdict(list)
        for row in self.conn.execute(
                f"SELECT paragraph_id, source_paragraph_id FROM paragraph_sources WHERE paragraph_id IN ({_placeholders(ids)})"
                " ORDER BY paragraph_id, ord", ids):
            canonical[row[0]].append(row[1])
        sources = [s for group in canonical.values() for s in group]
        wanted = ids + sources
        sentences = defaultdict(list)
        for s in self.conn.execute(
                f"SELECT id, paragraph_id, text FROM sentences WHERE paragraph_id IN ({_placeholders(wanted)}) ORDER BY seq",
                wanted):
            sentences[s["paragraph_id"]].append({"id": s["id"], "text": s["text"]})
        arabic = defaultdict(list)
        for a in self.conn.execute(
                "SELECT a.paragraph_id, substr(p.text, a.span_start + 1, a.span_end - a.span_start) AS text,"
                " a.kind, a.meal AS publisher_translation, a.source FROM arabic a JOIN paragraphs p ON p.id = a.paragraph_id"
                f" WHERE a.paragraph_id IN ({_placeholders(wanted)}) AND a.kind IN ({_placeholders(ANNOTATED_ARABIC)})"
                " ORDER BY a.paragraph_id, a.ord", [*wanted, *ANNOTATED_ARABIC]):
            arabic[a["paragraph_id"]].append({k: a[k] for k in ("text", "kind", "publisher_translation", "source") if a[k]})
        source_refs = {}
        if sources:
            source_refs = dict(self.conn.execute(
                f"SELECT p.id, n.ref FROM paragraphs p JOIN nodes n ON n.id = p.node_id WHERE p.id IN ({_placeholders(sources)})",
                sources).fetchall())

        out = {}
        for p in paragraphs:
            record = {"id": p["id"], "kind": p["kind"]}
            if p["kind"] == "hasiye":
                record["hasiye_of"] = p["anchor"] or p["parent_id"]
            if p["id"] in canonical:
                # Mecmuada eşlenmiş paragraf: metin ve atıf ana cilttedir.
                group = canonical[p["id"]]
                record["canonical"] = {"paragraphs": group, "ref": source_refs.get(group[0])}
                record["sentences"] = [s for pid in group for s in sentences[pid]]
                record_arabic = [a for pid in group for a in arabic[pid]]
            else:
                record["sentences"] = sentences[p["id"]]
                record_arabic = arabic[p["id"]]
            if record_arabic:
                record["arabic"] = record_arabic
            out[p["id"]] = record
        return out

    # ------------------------------------------------------------ cümleler

    def _sentence(self, sentence_id: str) -> sqlite3.Row:
        row = self.conn.execute("SELECT * FROM sentences WHERE id = ?", (sentence_id,)).fetchone()
        if row is None:
            raise LibraryError(f"No sentence with id {sentence_id!r}; ids come from search, read_section or find_sentence.")
        return row

    def passage(self, passage_id: str, context: int = 0) -> dict:
        """Bir cümle ya da aralık ("…/c010..c015" veya iki tam kimlik), istenirse komşu cümlelerle.
        Ana metin cümlelerine bağlı hâşiyeler cümlenin altında gelir."""
        first_id, _, last_id = passage_id.partition("..")
        first = self._sentence(first_id.strip())
        notes: list[str] = []
        if last_id:
            last_id = last_id.strip()
            if "/" not in last_id:                     # kısa biçim: aynı düğümde "c015"
                last_id = f"{first['id'].rsplit('/', 1)[0]}/{last_id}"
            last, note = self._range_end(last_id)
            notes += [note] if note else []
            if last["work"] != first["work"] or last["seq"] < first["seq"]:
                raise LibraryError("A range must run forward inside one work: first..last.")
            if last["seq"] - first["seq"] >= MAX_RANGE:
                raise LibraryError(f"Ranges are limited to {MAX_RANGE} sentences; use read_section for longer text.")
        else:
            last = first

        hasiye_only = first["hasiye"] and last["hasiye"]
        main_filter = "" if hasiye_only else " AND hasiye = 0"
        rows = self.conn.execute(f"SELECT * FROM sentences WHERE work = ? AND seq BETWEEN ? AND ?{main_filter}"
                                 " ORDER BY seq", (first["work"], first["seq"], last["seq"])).fetchall()
        before = after = []
        if context > 0:
            context = min(context, MAX_RANGE // 2)
            before = self.conn.execute(
                f"SELECT * FROM sentences WHERE node_id = ? AND seq < ?{main_filter} ORDER BY seq DESC LIMIT ?",
                (first["node_id"], first["seq"], context)).fetchall()[::-1]
            after = self.conn.execute(
                f"SELECT * FROM sentences WHERE node_id = ? AND seq > ?{main_filter} ORDER BY seq LIMIT ?",
                (last["node_id"], last["seq"], context)).fetchall()

        shown = [*before, *rows, *after]
        targets = {r["id"] for r in rows}
        hasiye = self._hasiye_of([r["id"] for r in shown]) if not hasiye_only else {}
        arabic = self._arabic_of([r["id"] for r in shown])
        out = []
        for r in shown:
            record = {"id": r["id"], "ref": r["ref"], "incipit": r["incipit"], "text": r["text"]}
            if context > 0:
                record["target"] = r["id"] in targets
            if arabic.get(r["id"]):
                record["arabic"] = arabic[r["id"]]
            if hasiye.get(r["id"]):
                record["hasiye"] = hasiye[r["id"]]
            out.append(record)
        node = self._node(first["node_id"])
        result = {"section": node["id"], "section_ref": node["ref"], "sentences": out}
        if len(rows) > 1 and not hasiye_only:
            if len({r["node_id"] for r in rows}) > 1:
                notes.append("The range spans several sections; cite each section's sentences separately.")
            elif len(rows) > MAX_CITED:
                notes.append(f"Cite at most {MAX_CITED} consecutive sentences at once; quote the key part.")
            else:
                result["cite_as"] = cite(node["ref"], opening(rows[0]["incipit"], rows[0]["text"]), len(rows))
        if notes:
            result["note"] = " ".join(notes)
        return result

    def _range_end(self, sentence_id: str) -> tuple[sqlite3.Row, str | None]:
        """Aralığın son cümlesi. Bölümün son cümlesini aşan numara ("c029", bölümde 24 cümle varken)
        bölümün sonuna çekilir; model aralığın ucunu çoğu zaman tahmin eder."""
        try:
            return self._sentence(sentence_id), None
        except LibraryError:
            node_id, _, local = sentence_id.rpartition("/")
            number = re.fullmatch(r"c(\d+)", local)
            last = self.conn.execute("SELECT * FROM sentences WHERE node_id = ? AND hasiye = 0 ORDER BY n DESC LIMIT 1",
                                     (node_id,)).fetchone()
            if number is None or last is None or int(number[1]) <= last["n"]:
                raise
        return last, f"Section {node_id!r} has {last['n']} sentences; the range ends at {last['id']}."

    def _hasiye_of(self, sentence_ids: list[str]) -> dict[str, list[dict]]:
        """Cümle -> ona bağlı hâşiyelerin cümleleri."""
        out = defaultdict(list)
        for s in self.conn.execute(
                "SELECT p.anchor, s.id, s.ref, s.text FROM paragraphs p JOIN sentences s ON s.paragraph_id = p.id"
                f" WHERE p.kind = 'hasiye' AND p.anchor IN ({_placeholders(sentence_ids)}) ORDER BY s.seq", sentence_ids):
            out[s["anchor"]].append({"id": s["id"], "ref": s["ref"], "text": s["text"]})
        return out

    def _arabic_of(self, sentence_ids: list[str]) -> dict[str, list[dict]]:
        out = defaultdict(list)
        for a in self.conn.execute(
                "SELECT a.sentence_id, substr(p.text, a.span_start + 1, a.span_end - a.span_start) AS text,"
                " a.kind, a.meal AS publisher_translation, a.source FROM arabic a JOIN paragraphs p ON p.id = a.paragraph_id"
                f" WHERE a.sentence_id IN ({_placeholders(sentence_ids)}) ORDER BY a.paragraph_id, a.ord", sentence_ids):
            if a["publisher_translation"] or a["source"]:
                out[a["sentence_id"]].append({k: a[k] for k in ("text", "kind", "publisher_translation", "source") if a[k]})
        return out

    def find_sentence(self, incipit: str, scope: str | None = None, limit: int = 10) -> dict:
        """İlk kelimelerinden cümleyi bulur (işaretsiz; son kelime eksik yazılabilir)."""
        words = search_words(incipit)
        if not words:
            raise LibraryError("Give the first words of the sentence.")
        params: list = [f'"{" ".join(words)}"*']
        where = ""
        if scope:
            node = self._node(scope)
            where = " AND s.work = ? AND s.node_id IN (SELECT id FROM nodes WHERE work = ? AND ord BETWEEN ? AND ?)"
            params += [node["work"], node["work"], node["ord"], node["last_ord"]]
        rows = self.conn.execute(
            "SELECT s.id, s.ref, s.incipit, s.text FROM sentences_fts JOIN sentences s ON s.seq = sentences_fts.rowid"
            f" WHERE sentences_fts MATCH ?{where} ORDER BY s.seq", params)
        matches = []
        for r in rows:
            head = search_words(r["text"])[:len(words)]
            if head[:-1] == words[:-1] and head and head[-1].startswith(words[-1]):
                matches.append({"id": r["id"], "ref": r["ref"], "incipit": r["incipit"], "text": _preview(r["text"])})
                if len(matches) >= limit:
                    break
        return {"matches": matches}

    # ------------------------------------------------------------ arama ve âyetler

    def search(self, query: str, work: str | None = None, group: str | None = None,
               limit: int = 20, offset: int = 0) -> dict:
        if work:
            self._node(work)
        limit = min(max(limit, 1), MAX_RESULTS)
        try:
            hits = fts.search(self.conn, query, work=work, group=group, limit=limit, offset=max(offset, 0))
            by_work = fts.count_by_work(self.conn, query, group=group)
            sections = fts.search_nodes(self.conn, query, work=work, limit=5)
        except fts.QueryError as error:
            raise LibraryError(str(error)) from None
        if work:
            by_work = {work: by_work.get(work, 0)}
        result = {
            "total": sum(by_work.values()),
            "by_work": by_work,
            "results": [{"id": h.sentence_id, "ref": h.ref, "incipit": h.incipit, "text": _preview(h.text)}
                        for h in hits],
        }
        if sections:
            result["matching_sections"] = [{"id": s.node_id, "ref": s.ref} for s in sections]
        return result

    def semantic_search(self, query: str, work: str | None = None, group: str | None = None,
                        limit: int = 10, offset: int = 0) -> dict:
        """Anlamca en yakın cümleler ve konunun yoğunlaştığı bölümler (`semantic.py`)."""
        if not query.strip():
            raise LibraryError("Give a question or a concept to search for.")
        works = None
        if work:
            self._node(work)
            works = {work}
        elif group:
            works = {r[0] for r in self.conn.execute("SELECT slug FROM works WHERE group_name = ?", (group,))}
            if not works:
                raise LibraryError(f"Unknown group {group!r}; groups are: eski-said, ana-cilt, mecmua, hizb.")
        try:
            hits, sections = self._semantic_index().search(query, works, min(max(limit, 1), MAX_RESULTS), max(offset, 0))
        except SemanticUnavailable:
            raise LibraryError("Semantic search is not available on this server (no sentence vectors); "
                               "use search with the text's own words.") from None
        except EmbeddingError as error:
            raise LibraryError(f"Semantic search failed ({error}); use search with the text's own words.") from None
        ids = [h.sentence_id for h in hits]
        rows = {r["id"]: r for r in self.conn.execute(
            f"SELECT id, ref, incipit, text FROM sentences WHERE id IN ({_placeholders(ids)})", ids)}
        refs = {}
        if sections and offset == 0:
            ids_ = [s.node_id for s in sections]
            refs = dict(self.conn.execute(f"SELECT id, ref FROM nodes WHERE id IN ({_placeholders(ids_)})", ids_).fetchall())
        result = {
            "results": [{"id": h.sentence_id, "ref": rows[h.sentence_id]["ref"], "incipit": rows[h.sentence_id]["incipit"],
                         "text": _preview(rows[h.sentence_id]["text"]), "similarity": round(h.score, 3)} for h in hits],
        }
        if refs:
            result["sections"] = [{"id": s.node_id, "ref": refs[s.node_id], "matches": s.matches} for s in sections]
        if unindexed := self._semantic_index().unindexed:
            result["unindexed_sentences"] = unindexed
        return result

    def _semantic_index(self) -> SemanticIndex:
        """Veritabanı yeniden kurulunca (yeni bağlantı) eşleme de yenilenir."""
        conn = self.conn
        if self._semantic is None or self._semantic[0] is not conn:
            self._semantic = (conn, SemanticIndex(conn, directory=self.vectors_dir))
        return self._semantic[1]

    def find_ayah(self, sura: str, ayah: int | None = None, limit: int = 30, offset: int = 0) -> dict:
        """Bir sûrenin (ya da âyetin) eserlerde geçtiği yerler. `sura` numara ya da ad ("Bakara").

        İki kaynaktan: kaynağın âyet diye işaretlediği Arapça (`via: source`, numarası kaynağın) ve kaynağın
        işaretlemediği, Kur'ân metninde bulunan alıntılar (`via: text`; Hizbler, el-Mesnevî el-Arabî).
        Kaynağın numarası Kur'ân metniyle tutmuyorsa `check` uyarır (iktibas, kısaltma ya da yanlış numara).
        """
        number = self._sura_number(sura)
        where, params = "q.sura = ?", [number]
        if ayah is not None:
            where += " AND ? BETWEEN q.ayah_start AND q.ayah_end"
            params.append(ayah)
        quotes = (
            "SELECT 'source' AS via, a.sentence_id, a.paragraph_id, a.span_start, a.span_end, a.meal, a.source,"
            " a.ayah_check, a.sura, a.ayah_start, a.ayah_end FROM arabic a WHERE a.sura IS NOT NULL"
            " UNION ALL SELECT 'text', q.sentence_id, q.paragraph_id, q.span_start, q.span_end, NULL, NULL, NULL,"
            " q.sura, q.ayah_start, q.ayah_end FROM ayah_quotes q")
        total = self.conn.execute(f"SELECT count(*) FROM ({quotes}) q WHERE {where} AND q.sentence_id IS NOT NULL",
                                  params).fetchone()[0]
        rows = self.conn.execute(
            "SELECT s.id, s.ref, s.incipit, substr(p.text, q.span_start + 1, q.span_end - q.span_start) AS arabic,"
            " q.meal AS publisher_translation, q.source, q.via, q.ayah_check, q.ayah_start, q.ayah_end"
            f" FROM ({quotes}) q JOIN sentences s ON s.id = q.sentence_id JOIN paragraphs p ON p.id = q.paragraph_id"
            f" WHERE {where} ORDER BY s.seq LIMIT ? OFFSET ?",
            [*params, min(max(limit, 1), MAX_RESULTS), max(offset, 0)])
        results = []
        for r in rows:
            item = {k: r[k] for k in ("id", "ref", "incipit", "arabic", "publisher_translation", "source") if r[k]}
            item["ayahs"] = _ayah_span(r["ayah_start"], r["ayah_end"])
            item["via"] = r["via"]
            if r["ayah_check"] in AYAH_CHECK_NOTES:
                item["check"] = AYAH_CHECK_NOTES[r["ayah_check"]]
            results.append(item)
        result = {"sura": number, "name": self._sura_name(number), "ayah": ayah, "total": total, "results": results}
        if ayah is not None and self._has_quran():
            result["quran"] = self.ayahs(number, ayah)["ayahs"][0]
            result["links"] = self._links(number, ayah)
        return result

    def _links(self, sura: int, ayah: int) -> list[dict]:
        """Âyetle bağ kuran yerler (güçlüler önce, kitap sırasıyla), kanıt cümleleriyle."""
        rows = self.conn.execute(
            "SELECT l.kind, l.strength, l.scope, n.id AS node_id, n.ref AS node_ref, s.id AS sid, s.ref AS sref,"
            " s.incipit, s.text FROM ayah_links l JOIN nodes n ON n.id = l.node_id JOIN sentences s ON s.id = l.evidence_id"
            " WHERE l.sura = ? AND ? BETWEEN l.ayah_start AND l.ayah_end"
            " ORDER BY l.strength = 'weak', s.seq LIMIT ?", (sura, ayah, MAX_LINKS)).fetchall()
        return [{"kind": r["kind"], "strength": r["strength"], "scope": r["scope"], "section": r["node_id"],
                 "ref": r["node_ref"], "evidence": {"id": r["sid"], "ref": r["sref"],
                                                    "opening": opening(r["incipit"], r["text"])}} for r in rows]

    def ayahs(self, sura: str | int, ayah: int, end: int | None = None, context: int = 0) -> dict:
        """Kur'ân'dan âyet ya da âyet aralığı: harekeli metin (Medine Mushafı hattı) ve Diyanet mealleri."""
        if not self._has_quran():
            raise LibraryError("The Qur'an layer is not installed in this database.")
        number = self._sura_number(str(sura))
        count = self.conn.execute("SELECT ayahs FROM quran_suras WHERE number = ?", (number,)).fetchone()[0]
        end = ayah if end is None else end
        if not 1 <= ayah <= end <= count:
            raise LibraryError(f"{self._sura_name(number)} has verses 1–{count}; got {ayah}–{end}.")
        if end - ayah + 1 > MAX_AYAHS:
            raise LibraryError(f"At most {MAX_AYAHS} verses at a time.")
        first, last = max(1, ayah - context), min(count, end + context)
        translators = dict(self.conn.execute("SELECT id, name FROM quran_translators ORDER BY ord").fetchall())
        meals = defaultdict(list)
        for r in self.conn.execute(
                "SELECT t.ayah, t.translator, t.text, t.first_ayah, t.last_ayah FROM quran_translations t"
                " JOIN quran_translators q ON q.id = t.translator WHERE t.sura = ? AND t.ayah BETWEEN ? AND ?"
                " ORDER BY q.ord", (number, first, last)):
            meal = {"translator": translators[r["translator"]], "text": r["text"]}
            if r["first_ayah"] != r["last_ayah"]:
                meal["covers_verses"] = f"{number}:{r['first_ayah']}-{r['last_ayah']}"
            meals[r["ayah"]].append(meal)
        quoted = dict(self.conn.execute(
            "SELECT a.ayah, count(*) FROM quran_ayahs a JOIN (SELECT sura, ayah_start, ayah_end FROM arabic"
            " WHERE sura = :s UNION ALL SELECT sura, ayah_start, ayah_end FROM ayah_quotes WHERE sura = :s) q"
            " ON a.ayah BETWEEN q.ayah_start AND q.ayah_end WHERE a.sura = :s AND a.ayah BETWEEN :f AND :l"
            " GROUP BY a.ayah", {"s": number, "f": first, "l": last}).fetchall())
        links = defaultdict(lambda: {"strong": 0, "weak": 0})
        for r in self.conn.execute(
                "SELECT a.ayah, l.strength, count(*) AS n FROM quran_ayahs a JOIN ayah_links l ON l.sura = a.sura"
                " AND a.ayah BETWEEN l.ayah_start AND l.ayah_end WHERE a.sura = ? AND a.ayah BETWEEN ? AND ?"
                " GROUP BY a.ayah, l.strength", (number, first, last)):
            links[r["ayah"]][r["strength"]] = r["n"]
        out = []
        for r in self.conn.execute("SELECT ayah, text FROM quran_ayahs WHERE sura = ? AND ayah BETWEEN ? AND ?"
                                   " ORDER BY ayah", (number, first, last)):
            item = {"ayah": r["ayah"], "ref": f"{self._sura_name(number)} Sûresi, {number}:{r['ayah']}",
                    "text": r["text"], "translations": meals[r["ayah"]],
                    "quoted_in_works": quoted.get(r["ayah"], 0)}
            if r["ayah"] in links:
                item["linked_in_works"] = links[r["ayah"]]
            if not ayah <= r["ayah"] <= end:
                item["context"] = True
            out.append(item)
        return {"sura": number, "name": self._sura_name(number), "ayahs": out, "attribution": QURAN_ATTRIBUTION}

    def _verse_ref(self, sura: int, start: int, end: int) -> str:
        return f"{self._sura_name(sura)} Sûresi, {sura}:{_ayah_span(start, end)}"

    def _has_quran(self) -> bool:
        return self.conn.execute("SELECT EXISTS (SELECT 1 FROM quran_ayahs)").fetchone()[0] == 1

    def _sura_name(self, number: int) -> str | None:
        row = self.conn.execute("SELECT name FROM quran_suras WHERE number = ?", (number,)).fetchone()
        row = row or self.conn.execute("SELECT name FROM sura_names WHERE number = ? LIMIT 1", (number,)).fetchone()
        return row[0] if row else None

    def _sura_number(self, sura: str) -> int:
        sura = str(sura).strip()
        if sura.isdigit():
            number = int(sura)
            if not 1 <= number <= 114:
                raise LibraryError("Sura numbers run from 1 to 114.")
            return number
        row = self.conn.execute("SELECT number FROM sura_names WHERE key = ?", ("".join(search_words(sura)),)).fetchone()
        if row is None:
            raise LibraryError(f"Unknown sura name {sura!r}; give its number (e.g. 2 for Bakara).")
        return row[0]
