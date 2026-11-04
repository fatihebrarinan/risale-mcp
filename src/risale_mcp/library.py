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

import json
import re
import sqlite3
from collections import defaultdict
from itertools import accumulate
from pathlib import Path

from risale_mcp import search as fts
from risale_mcp.catalog import Authority, Collection
from risale_mcp.db import connect
from risale_mcp.hadis import ATTRIBUTION, CAUTION_BOOKS, SUPPORT_ORDER, TITLES
from risale_mcp.hadis_kitaplar import BY_ID
from risale_mcp.quran import skeleton
from risale_mcp.embeddings import EmbeddingError
from risale_mcp.normalize import search_words
from risale_mcp.paths import DB_PATH
from risale_mcp.semantic import SemanticIndex, SemanticUnavailable

MAX_RANGE = 100          # get_passage'ın bir seferde döndürdüğü en çok cümle
MAX_CITED = 8            # tek atıfla verilebilecek en çok ardışık cümle (aynı bölümde)
MAX_RESULTS = 50
PREVIEW_CHARS = 400      # arama sonucunda gösterilen en uzun cümle metni
ANNOTATED_ARABIC = ("ayet", "hadis")   # okurken meali ve kaynağı gösterilen Arapça türleri
# Eski adla anılan, metni başka yerde duran bölümler: bölüm kimliği -> {name, elsewhere, rule?, evidence}
OLD_NAMES = json.loads((Path(__file__).parent / "books" / "old_names.json").read_text(encoding="utf-8"))["sections"]


HADITH_NOTE = ("hadith_support is evidence, not a verdict: found = the Arabic occurs word for word in a report and is long "
               "enough to identify it; partly_found = a report carries most of it (it may be abridged, altered or quoted by "
               "meaning); located_chapter = a short part that occurs in the cited chapter of the cited book at this place; "
               "read_chapter = two blind model readers found the same saying (often in other words or abridged) in the "
               "region of the cited book the citation points to (read_reports); "
               "cited = a hadith book is cited for it, its report was not identified from the text, any reports "
               "listed only share its words; phrase_found = the words occur in a report but are too short to identify it, "
               "and no book is cited: do not present that report as its source; marked = only the source marks it as a "
               "hadith; unsupported = nothing beyond the words around it. Not found never means it is not a hadith: the "
               "author often gives a hadith in his own words. reports is a selection, reports_total counts them. "
               "cited_in lists the printed references as they stand (qualifier: see, iktibas, by_meaning); they are the "
               "publishers', not the author's, and were not checked against the books. "
               "A report may come from a tafsir or history "
               "book, or from a book that lists forged reports (book_note): name the book. Give grades only as listed, with each scholar's name.")


# Model okuması ve rivayet denetimi (`hadis_okumalar.py`): yalnız yerel profilde dolu. Hüküm değildir.
READING_NOTE = ("model_readings and report_flags come from two model readers and rule-based checks, not from a hadith "
                "scholar: they are leads, never a verdict. A candidate the readers called the same saying (same: true) "
                "is a likely variant wording or the author's rendering by meaning (relation), not a verified source; "
                "say so and keep hadith_support as the evidence. verdicts are the book's own words after a report, "
                "one scholar's view: give them with the book's name.")
FLAG_TEXT = {"denied": "a report is followed by words denying it is a hadith",
             "other_saying": "a report attributes it to someone else",
             "only_caution": "found only in books that collect weak or forged reports",
             "no_prophet": "no report attributes it to the Prophet",
             "no_chain": "no report carries a chain of narrators",
             "weakened": "a report is followed by words weakening it"}


def _report_summary(row) -> dict:
    """Derece yalnız âlimin adıyla; Buhârî ve Müslim'de hadis başına derece yoktur, uydurulmaz."""
    record = {"id": row["id"], "book": row["title"], "number": row["number"]}
    if row["grades"]:
        record["grades"] = [{"scholar": s, "grade": g} for s, g in json.loads(row["grades"])]
    elif row["id"].split(":")[0] in ("bukhari", "muslim"):
        record["collection_note"] = "In this Sahih; no per-hadith grade is held."
    if CAUTION_BOOKS.search(row["title"]):
        record["book_note"] = "This book collects weak or forged reports: a match here means the saying is discussed there, not that it is sound, and it may be listed as forged."
    return record


def _arabic_record(row) -> dict:
    """Bağlamdan çıkarılan hadis adaydır, doğrulanmamıştır: model bunu bilmeli."""
    record = {k: row[k] for k in ("text", "kind", "publisher_translation", "source") if row[k]}
    if row["kind_source"] == "baglam":
        record["kind_unverified"] = True
    if row["hadith_support"]:
        record["hadith_support"] = row["hadith_support"]
    if "model_reading" in row.keys() and row["model_reading"]:
        record["model_reading"] = "find_hadith lists two model readers' leads for it (not a verdict)"
    return record
MAX_CITATIONS = 12       # find_hadith'in bir parça için döndürdüğü en çok künye
MAX_LINKS = 30           # find_ayah'ın bir âyet için döndürdüğü en çok ilişki
MAX_AYAHS = 30           # get_ayah'ın bir seferde döndürdüğü en çok âyet (bağlam hariç)
QURAN_ATTRIBUTION = ("Arabic text: Tanzil Project (tanzil.net), Medina Mushaf script. Translations: Diyanet İşleri "
                     "Başkanlığı and Türkiye Diyanet Vakfı, via Tanzil (non-commercial use).")
# Kaynağın âyet numarası Kur'ân metniyle tutmuyorsa modele giden uyarı (build_db, `ayah_check`).
AYAH_CHECK_NOTES = {
    "near": "the quoted text is in a neighbouring verse, not exactly the one the source names",
    "dizgi_suphesi": "possible misprint: the text differs from the named verse and may be a printing error, not the "
                     "author's wording. Quote the work as it stands, say so, and take the verse's own text from get_ayah",
    "iktibas": "the quoted text does not match the named verse word for word: the author's adapted quotation or "
               "abridgement. Quote the work as it stands; take the verse's own text from get_ayah",
}


def old_names_note() -> str:
    """Sunucu talimatı için eski adlar listesi: "Otuz Birinci Mektub = lemalar (its Nth Lem'a is lemalar/N)"."""
    return "; ".join(f"{e['name']} = {', '.join(e['elsewhere'])}" + (f" ({e['rule']})" if "rule" in e else "")
                     for e in OLD_NAMES.values())


def _elsewhere(node_id: str) -> dict:
    """Bölümün metni başka yerdeyse sonuca eklenecek alan; değilse boş."""
    entry = OLD_NAMES.get(node_id)
    if entry is None:
        return {}
    return {"text_elsewhere": {k: entry[k] for k in ("elsewhere", "rule", "evidence") if k in entry}}


def _default_scope(work: str | None, group: str | None, include_related: bool) -> str | None:
    """Süzgeçsiz arama yalnız külliyata bakar: günümüz Türkçesiyle yazılmış ilgili kaynaklar asıl metnin önüne geçmesin."""
    return None if work or group or include_related else Collection.KULLIYAT


class LibraryError(ValueError):
    """Modelin düzeltebileceği hata: bilinmeyen kimlik, geçersiz sorgu…"""


def _preview(text: str) -> str:
    return text if len(text) <= PREVIEW_CHARS else text[:PREVIEW_CHARS].rsplit(" ", 1)[0] + " …"


REF_SEP = " › "


def opening(incipit: str, text: str) -> str:
    """Kullanıcıya gösterilen ilk kelimeler; cümle daha uzunsa "…" ile."""
    return incipit if len(incipit) >= len(text.rstrip()) else incipit + "…"


def cite(section_ref: str, opening_words: str, count: int = 1) -> str:
    """Kullanıcıya gösterilen atıf: yol › “ilk kelimeler…”; ardışık cümlelerde “…” ile başlayan N cümle."""
    quoted = f"{section_ref} › “{opening_words}”"
    return quoted if count == 1 else f"{quoted} ile başlayan {count} cümle"


# Arama sonuçlarına eklenen hatırlatma: claude.ai gibi genel istemcilerde model aramadan doğrudan cevaba geçiyordu
# (2026-10-28, kullanım kaydı: iki arama, hiç okuma ve denetim yok).
SEARCH_NOTE = ("These are candidates, not evidence. Before relying on one, read it in context with get_passage(id, "
               "context=2) or read_section. Quote the text itself in a > block and get the answer's Kaynaklar list "
               "from cite; never give sentence numbers.")


def hit_cite(sentence_ref: str, incipit: str, text: str) -> str:
    """Arama sonucundaki cümlenin kullanıcıya gösterilecek atfı (yol › “ilk kelimeler”)."""
    return cite(sentence_ref.rsplit(REF_SEP, 1)[0], opening(incipit, text))


def _ayah_span(start: int, end: int) -> str:
    return f"{start}" if start == end else f"{start}-{end}"


def _placeholders(items) -> str:
    return ",".join("?" * len(items))


# Kaynakçanın alt satırları (`docs/kaynakca-plani.md`): alıntılanan cümledeki âyetin ve hadisin adresi. Meal girmez.
# Âyet: Kur'ân metniyle tutan numara notsuz; numarası olmayan âyet satıra girmez (adres uydurulmaz).
AYAH_LINE_NOTES = {"iktibas": "iktibas", "dizgi_suphesi": "numara metinle tutmuyor", "near": "komşu âyette"}
# Hadis: gösterilen künye nâşirindir. Derlemde künyedeki kitapta bulunmadıkça "doğrulanmadı" der.
HADITH_PARTLY = "lafız farkıyla bulundu"
HADITH_READ = "okumayla bulundu"          # künyenin bölgesinde iki kör okuyucu aynı söz dedi (kullanıcının kararı)
HADITH_UNVERIFIED = "doğrulanmadı"
_QUALIFIER_SUFFIX = {"iktibas": "iktibas", "by_meaning": "mânen"}


def _citation_text(raw: str, qualifier: str | None) -> str:
    """Künye kaynaktaki gibi (`hadis_kunye` artığını atmıştır); "bk." de kaynağındır, kalır."""
    return ("bk. " if qualifier == "see" else "") + raw


def _in_books(report_ids: list[tuple[str, str]], books: set[str]) -> bool:
    """Bulunan rivayetlerden biri künyedeki kitaplardan birinde mi (Hadith API derlemi ya da Sanadset adı)."""
    titles = set()
    for b in filter(None, (BY_ID.get(book) for book in books)):
        titles |= {TITLES[b.api]} if b.api else set(b.sanadset)
    return any(title in titles for _, title in report_ids)


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

    def corpus_version(self) -> str | None:
        """Metnin sürümü (`manifest.py`): yayın etiketi, yayınlanmamışsa "unreleased:<özet>"; eski veritabanında yok."""
        meta = dict(self.conn.execute("SELECT key, value FROM meta WHERE key IN ('corpus_version', 'corpus_hash')").fetchall())
        if "corpus_version" in meta:
            return meta["corpus_version"]
        return f"unreleased:{meta['corpus_hash']}" if "corpus_hash" in meta else None

    def works(self, group: str | None = None) -> list[dict]:
        sentences = dict(self.conn.execute("SELECT work, count(*) FROM sentences GROUP BY work").fetchall())
        sections = dict(self.conn.execute("SELECT work, count(*) FROM nodes GROUP BY work").fetchall())
        written = dict(self.conn.execute("SELECT id, written FROM nodes WHERE parent_id IS NULL AND written IS NOT NULL"))
        rows = self.conn.execute(
            "SELECT slug, title, group_name, collection, authority, translation, language, status, note, built FROM works"
            + (" WHERE group_name = ?" if group else "") + " ORDER BY ord", [group] if group else []).fetchall()
        if group and not rows:
            groups = [r[0] for r in self.conn.execute("SELECT DISTINCT group_name FROM works ORDER BY ord")]
            raise LibraryError(f"Unknown group {group!r}; groups are: {', '.join(groups)}.")
        out = []
        for w in rows:
            record = {"id": w["slug"], "title": w["title"], "group": w["group_name"], "language": w["language"]}
            if w["collection"] != Collection.KULLIYAT:
                record["collection"] = w["collection"]
            if w["authority"] != Authority.MUELLIF:
                record["authority"] = w["authority"]
            if w["translation"]:
                record["translation"] = True
            if w["built"]:
                record |= {"sections": sections[w["slug"]], "sentences": sentences.get(w["slug"], 0)}
            else:
                record |= {"available": False, "status": w["status"]}
            if w["note"]:
                record["note"] = w["note"]
            if w["slug"] in written:
                record["written"] = json.loads(written[w["slug"]])
            out.append(record)
        return out

    def _node(self, node_id: str) -> sqlite3.Row:
        row = self.conn.execute("SELECT * FROM nodes WHERE id = ?", (node_id,)).fetchone()
        if row is None:                          # yeni kaynakta yeri değişen eski bölüm (node_aliases)
            row = self.conn.execute("SELECT n.* FROM node_aliases a JOIN nodes n ON n.id = a.new_id "
                                    "WHERE a.old_id = ?", (node_id,)).fetchone()
        if row is None:
            hint = "use get_outline to see section ids" if "/" in node_id else "use list_works for work ids"
            raise LibraryError(f"No section with id {node_id!r}; {hint}.")
        return row

    def _written(self, node: sqlite3.Row) -> dict | None:
        """Bölümün ya da içinde bulunduğu en yakın üst bölümün telif bilgisi; üst bölümdense `section` onu gösterir."""
        own = node["id"]
        while node["written"] is None and node["parent_id"]:
            node = self._node(node["parent_id"])
        if node["written"] is None:
            return None
        return json.loads(node["written"]) | ({"section": node["id"]} if node["id"] != own else {})

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
            if n["written"]:
                record["written"] = json.loads(n["written"])
            record["sentences"] = prefix[n["last_ord"] - first + 1] - prefix[n["ord"] - first]
            if n["id"] != root["id"]:
                records[n["parent_id"]].setdefault("children", []).append(record)
            records[n["id"]] = record
        for node_id_, record in records.items():
            if "children" not in record and child_count[node_id_]:
                record["subsections"] = child_count[node_id_]
        return {"work": root["work"], "ref": root["ref"], **records[root["id"]], **_elsewhere(root["id"])}

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
                if n["written"] and n["id"] != root["id"]:
                    item["written"] = json.loads(n["written"])
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
        result = {"section": root["id"], "ref": root["ref"], "items": items, "next_cursor": next_cursor}
        if written := self._written(root):
            result["written"] = written
        return result | _elsewhere(root["id"]) | self._work_status(root["work"])

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
                " a.kind, a.kind_source, a.hadith_support, a.meal AS publisher_translation, a.source,"
                " EXISTS (SELECT 1 FROM hadith_readings h WHERE h.hadith_key = a.hadith_key AND h.same = 1) AS model_reading"
                " FROM arabic a JOIN paragraphs p ON p.id = a.paragraph_id"
                f" WHERE a.paragraph_id IN ({_placeholders(wanted)}) AND a.kind IN ({_placeholders(ANNOTATED_ARABIC)})"
                " ORDER BY a.paragraph_id, a.ord", [*wanted, *ANNOTATED_ARABIC]):
            arabic[a["paragraph_id"]].append(_arabic_record(a))
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
                if p["commentator"]:
                    record["commentary_by"] = p["commentator"]
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
        result = {"section": node["id"], "section_ref": node["ref"], "sentences": out} | self._work_status(node["work"])
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
                "SELECT p.anchor, p.commentator, s.id, s.ref, s.text FROM paragraphs p JOIN sentences s ON s.paragraph_id = p.id"
                f" WHERE p.kind = 'hasiye' AND p.anchor IN ({_placeholders(sentence_ids)}) ORDER BY s.seq", sentence_ids):
            out[s["anchor"]].append({"id": s["id"], "ref": s["ref"], "text": s["text"],
                                     **({"commentary_by": s["commentator"]} if s["commentator"] else {})})
        return out

    def _arabic_of(self, sentence_ids: list[str]) -> dict[str, list[dict]]:
        out = defaultdict(list)
        for a in self.conn.execute(
                "SELECT a.sentence_id, substr(p.text, a.span_start + 1, a.span_end - a.span_start) AS text,"
                " a.kind, a.kind_source, a.hadith_support, a.meal AS publisher_translation, a.source,"
                " EXISTS (SELECT 1 FROM hadith_readings h WHERE h.hadith_key = a.hadith_key AND h.same = 1) AS model_reading"
                " FROM arabic a JOIN paragraphs p ON p.id = a.paragraph_id"
                f" WHERE a.sentence_id IN ({_placeholders(sentence_ids)}) ORDER BY a.paragraph_id, a.ord", sentence_ids):
            if a["publisher_translation"] or a["source"]:
                out[a["sentence_id"]].append(_arabic_record(a))
        return out

    def embedded(self, sentence_ids: list[str]) -> list[dict]:
        """Cümlelerdeki âyet ve hadis parçaları, metindeki sırayla: kaynakçanın alt satırları (`line`) ve dayanağı.
        Adresi olmayan âyet girmez; künyesi olmayan hadis "künye yok" der. Meal girmez."""
        if not sentence_ids:
            return []
        rows = self.conn.execute(
            "SELECT a.paragraph_id, a.ord, a.sentence_id, substr(p.text, a.span_start + 1, a.span_end - a.span_start) AS text,"
            " a.kind, a.kind_source, a.sura, a.ayah_start, a.ayah_end, a.ayah_check, a.hadith_key, a.hadith_support"
            " FROM arabic a JOIN paragraphs p ON p.id = a.paragraph_id JOIN sentences s ON s.id = a.sentence_id"
            f" WHERE a.sentence_id IN ({_placeholders(sentence_ids)}) AND (a.kind IN ('ayet', 'hadis') OR a.sura IS NOT NULL)"
            " ORDER BY s.seq, a.span_start", sentence_ids).fetchall()
        quotes = self.conn.execute(
            "SELECT q.sentence_id, substr(p.text, q.span_start + 1, q.span_end - q.span_start) AS text, q.sura,"
            " q.ayah_start, q.ayah_end, q.span_start FROM ayah_quotes q JOIN paragraphs p ON p.id = q.paragraph_id"
            f" WHERE q.sentence_id IN ({_placeholders(sentence_ids)})", sentence_ids).fetchall()
        out = []
        for r in rows:
            if r["sura"] is not None:
                note = AYAH_LINE_NOTES.get(r["ayah_check"])
                ref = self._verse_ref(r["sura"], r["ayah_start"], r["ayah_end"])
                out.append({"kind": "ayet", "sentence_id": r["sentence_id"], "text": r["text"], "ref": ref,
                            "line": f"Âyet: {ref}" + (f" ({note})" if note else "")})
            elif r["kind"] == "hadis":
                out.append({"sentence_id": r["sentence_id"], "text": r["text"], **self._hadith_line(r)})
        for q in quotes:      # bir duanın içinde geçen âyet: parça `arabi`, âyet ayrıca bulunmuş
            ref = self._verse_ref(q["sura"], q["ayah_start"], q["ayah_end"])
            out.append({"kind": "ayet", "sentence_id": q["sentence_id"], "text": q["text"], "ref": ref, "line": f"Âyet: {ref}"})
        order = {sid: i for i, sid in enumerate(sentence_ids)}
        return sorted(out, key=lambda e: order.get(e["sentence_id"], 0))

    def _hadith_line(self, r: sqlite3.Row) -> dict:
        """Geçişin kendi künyesi, yoksa nurpedia'nınki (parçaya bağlı); notu derlemdeki kanıttan."""
        citations = self.conn.execute(
            "SELECT raw, qualifier, book FROM hadith_citations WHERE paragraph_id = ? AND ord = ? ORDER BY id",
            (r["paragraph_id"], r["ord"])).fetchall() or self.conn.execute(
            "SELECT raw, qualifier, book FROM hadith_citations WHERE hadith_key = ? AND origin = 'nurpedia' ORDER BY id",
            (r["hadith_key"],)).fetchall()
        support = r["hadith_support"]
        record = {"kind": "hadis", "hadith_support": support}
        if not citations:
            label = "Hadis olarak sunulmuş (künye yok)" if r["kind_source"] == "baglam" else "Hadis (kaynakta künye yok)"
            return {**record, "citations": [], "line": label}
        # "iktibas", "mânen" künyenin değil sözündür: bütün künyelerde aynıysa bir kez, değilse künyenin yanında.
        marks = {_QUALIFIER_SUFFIX.get(c["qualifier"]) for c in citations}
        shared = marks.pop() if len(marks) == 1 else None
        texts = list(dict.fromkeys(
            _citation_text(c["raw"], c["qualifier"]) + ("" if shared or c["qualifier"] not in _QUALIFIER_SUFFIX
                                                         else f" ({_QUALIFIER_SUFFIX[c['qualifier']]})")
            for c in citations))
        texts = [t for t in texts if t and t != "bk."]
        books = {c["book"] for c in citations if c["book"]}
        reports = self.conn.execute("SELECT r.id, r.title FROM hadith_matches m JOIN hadith_reports r ON r.id = m.report_id"
                                    " WHERE m.hadith_key = ?", (r["hadith_key"],)).fetchall()
        read = self.conn.execute("SELECT 1 FROM hadith_region WHERE paragraph_id = ? AND ord = ?",
                                 (r["paragraph_id"], r["ord"])).fetchone()
        if support == "located_chapter" or (support == "found" and _in_books(reports, books)):
            note = None
        elif support == "partly_found" and _in_books(reports, books):
            note = HADITH_PARTLY
        elif read:
            note = HADITH_READ
        else:
            note = HADITH_UNVERIFIED
        notes = ", ".join(filter(None, (shared, note)))
        return {**record, "citations": texts, "verified": note != HADITH_UNVERIFIED,
                "line": "Hadis: " + "; ".join(texts) + (f" ({notes})" if notes else "")}

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

    def _status(self) -> dict[str, dict]:
        """Sonuçlarda söylenecek eser statüsü: eser -> {authority?, translation?}; müellifin kendi metninde boş."""
        rows = self.conn.execute("SELECT slug, authority, translation FROM works WHERE authority != ? OR translation = 1",
                                 (Authority.MUELLIF,))
        return {r["slug"]: ({"authority": r["authority"]} if r["authority"] != Authority.MUELLIF else {})
                | ({"translation": True} if r["translation"] else {}) for r in rows}

    def _work_status(self, work: str) -> dict:
        return self._status().get(work, {})

    def search(self, query: str, work: str | None = None, group: str | None = None,
               limit: int = 20, offset: int = 0, include_related: bool = False) -> dict:
        if work:
            self._node(work)
        collection = _default_scope(work, group, include_related)
        limit = min(max(limit, 1), MAX_RESULTS)
        try:
            hits = fts.search(self.conn, query, work=work, group=group, limit=limit, offset=max(offset, 0),
                              collection=collection)
            by_work = fts.count_by_work(self.conn, query, group=group, collection=collection)
            sections = fts.search_nodes(self.conn, query, work=work, limit=5, collection=collection)
        except fts.QueryError as error:
            raise LibraryError(str(error)) from None
        if work:
            by_work = {work: by_work.get(work, 0)}
        status = self._status()
        result = {
            "total": sum(by_work.values()),
            "by_work": by_work,
            "results": [{"id": h.sentence_id, "cite_as": hit_cite(h.ref, h.incipit, h.text), "text": _preview(h.text),
                         **status.get(h.work, {})} for h in hits],
            "note": SEARCH_NOTE,
        }
        if sections:
            result["matching_sections"] = [{"id": s.node_id, "ref": s.ref} for s in sections]
        return result

    def semantic_search(self, query: str, work: str | None = None, group: str | None = None,
                        limit: int = 10, offset: int = 0, include_related: bool = False) -> dict:
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
                raise LibraryError(f"Unknown group {group!r}; groups are: eski-said, ana-cilt, mecmua, hizb, osmanlica.")
        elif collection := _default_scope(work, group, include_related):
            works = {r[0] for r in self.conn.execute("SELECT slug FROM works WHERE collection = ?", (collection,))}
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
        status = self._status()
        result = {
            "results": [{"id": h.sentence_id,
                         "cite_as": hit_cite(rows[h.sentence_id]["ref"], rows[h.sentence_id]["incipit"],
                                             rows[h.sentence_id]["text"]),
                         "text": _preview(rows[h.sentence_id]["text"]), "similarity": round(h.score, 3),
                         **status.get(h.work, {})} for h in hits],
            "note": SEARCH_NOTE,
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
            "SELECT CASE a.kind_source WHEN 'kaynak' THEN 'source' ELSE 'text' END AS via, a.sentence_id, a.paragraph_id, a.span_start, a.span_end, a.meal, a.source,"
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
            "SELECT l.kind, l.strength, l.scope, l.ayah_start, l.ayah_end, n.id AS node_id, n.ref AS node_ref,"
            " s.id AS sid, s.ref AS sref, s.incipit, s.text FROM ayah_links l JOIN nodes n ON n.id = l.node_id"
            " JOIN sentences s ON s.id = l.evidence_id WHERE l.sura = ? AND ? BETWEEN l.ayah_start AND l.ayah_end"
            " ORDER BY l.strength = 'weak', s.seq LIMIT ?", (sura, ayah, MAX_LINKS)).fetchall()
        out = []
        for r in rows:
            item = {"kind": r["kind"], "strength": r["strength"], "scope": r["scope"], "section": r["node_id"],
                    "ref": r["node_ref"], "evidence": {"id": r["sid"], "ref": r["sref"],
                                                       "opening": opening(r["incipit"], r["text"])}}
            verse = f"quran:{sura}:{r['ayah_start']}" + (f"-{r['ayah_end']}" if r["ayah_end"] != r["ayah_start"] else "")
            source = r["node_id"] if r["scope"] == "section" else r["sid"]
            if reviews := self._reviews(source, verse, "relation"):
                item["reviews"] = reviews
            out.append(item)
        return out

    def _reviews(self, source: str, target: str, type_: str, part: str = "") -> list[dict]:
        """Bağ üzerine isimli denetçilerin geçerli kararları (`link_reviews.py`); yoksa boş: bağı kural kurdu,
        kimse bakmadı."""
        return [{k: v for k, v in (("status", r["status"]), ("strength", r["strength"]), ("by", r["name"]),
                                   ("date", r["date"]), ("reason", r["reason"])) if v}
                for r in self.conn.execute(
                    "SELECT status, strength, name, date, reason FROM link_reviews WHERE source = ? AND target = ?"
                    " AND type = ? AND part = ? ORDER BY date, reviewer", (source, target, type_, part))]

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

    def find_hadith(self, text: str, limit: int = 20) -> dict:
        """Arapça metinden Risale'deki hadis parçaları, dayanakları ve eşleşen rivayetler (`hadis.py`)."""
        key = skeleton(text)
        if len(key) < 4:
            raise LibraryError("Give the Arabic words of the hadith; use search for Turkish words.")
        keys = [r[0] for r in self.conn.execute(
            "SELECT hadith_key FROM arabic WHERE hadith_key = ? OR hadith_key LIKE ? OR (length(hadith_key) >= 8 AND ? LIKE '%' || hadith_key || '%')"
            " GROUP BY hadith_key ORDER BY hadith_key != ?, count(*) DESC LIMIT 5", (key, f"%{key}%", key, key))]
        if not keys:
            return {"parts": [], "note": "No part marked as a hadith in the works has these words. Try search."}
        parts = []
        for k in keys:
            found = {r[0] for r in self.conn.execute("SELECT DISTINCT hadith_support FROM arabic WHERE hadith_key = ?", (k,))}
            support = next((s for s in SUPPORT_ORDER if s in found), None)     # kısa ifadede geçişler ayrılabilir
            part = self.conn.execute("SELECT total FROM hadith_parts WHERE hadith_key = ?", (k,)).fetchone()
            places = self.conn.execute(
                "SELECT s.id, s.ref FROM arabic a JOIN sentences s ON s.id = a.sentence_id"
                " WHERE a.hadith_key = ? ORDER BY s.seq", (k,)).fetchall()
            parts.append({
                "hadith_support": support, "occurrences": len(places), "reports_total": part[0] if part else 0,
                "cited_in": self._hadith_citations(k),
                "read_reports": [{**_report_summary(r), "relation": r["relation"]} for r in self.conn.execute(
                    "SELECT DISTINCT r.*, g.relation FROM arabic a JOIN hadith_region g ON g.paragraph_id = a.paragraph_id"
                    " AND g.ord = a.ord JOIN hadith_reports r ON r.id = g.report_id WHERE a.hadith_key = ? LIMIT ?", (k, MAX_CITATIONS))],
                "located_reports": [_report_summary(r) for r in self.conn.execute(
                    "SELECT DISTINCT r.* FROM arabic a JOIN hadith_located l ON l.paragraph_id = a.paragraph_id AND l.ord = a.ord"
                    " JOIN hadith_reports r ON r.id = l.report_id WHERE a.hadith_key = ? LIMIT ?", (k, MAX_CITATIONS))],
                **self._readings(k),
                "places": [{"id": p["id"], "ref": p["ref"]} for p in places[:limit]],
                "reports": [_report_summary(r) for r in self.conn.execute(
                    "SELECT r.* FROM hadith_matches m JOIN hadith_reports r ON r.id = m.report_id"
                    " WHERE m.hadith_key = ? ORDER BY m.rank", (k,))]})
        note = HADITH_NOTE + (" " + READING_NOTE if any("model_readings" in p or "report_flags" in p for p in parts) else "")
        return {"parts": parts, "note": note}

    def _readings(self, key: str) -> dict:
        """Model okuması, rivayet denetiminin uyarıları ve kitapların ifadeleri; yoksa boş (genel profil)."""
        out: dict = {}
        readings = self.conn.execute(
            "SELECT h.*, r.title, r.number, r.text, r.grades, r.id FROM hadith_readings h JOIN hadith_reports r ON r.id = h.report_id"
            " WHERE h.hadith_key = ? ORDER BY h.kind = 'match', h.same DESC, h.in_cited_chapter IS NOT 1, h.report_id", (key,)).fetchall()
        if readings:
            out["model_readings"] = [{
                **_report_summary(r), "text": r["text"],
                "kind": "candidate (its words do not match; read by two models)" if r["kind"] == "candidate" else "matched report",
                "same": bool(r["same"]), "relation": sorted({r["relation_a"], r["relation_b"]}),
                **({"speaker": r["speaker_a"]} if r["speaker_a"] == r["speaker_b"] and r["speaker_a"] else {}),
                **({"in_cited_chapter": True} if r["in_cited_chapter"] else {})} for r in readings]
        if flags := [FLAG_TEXT[f[0]] for f in self.conn.execute("SELECT flag FROM hadith_flags WHERE hadith_key = ?", (key,))
                     if f[0] in FLAG_TEXT]:
            out["report_flags"] = flags
        if verdicts := self.conn.execute(
                "SELECT v.verdict, v.text, r.title FROM hadith_verdicts v JOIN hadith_reports r ON r.id = v.report_id"
                " WHERE v.hadith_key = ?", (key,)).fetchall():
            out["verdicts"] = [{"book": v["title"], "kind": v["verdict"], "words": v["text"]} for v in verdicts]
        return out

    def _hadith_citations(self, key: str) -> list[dict]:
        """Künyeler: kaynağın ve nurpedia'nın, kitap başına bir kez; `number` bâb ya da baskı numarası olabilir."""
        seen, out = set(), []
        for row in self.conn.execute(
                "SELECT c.raw, c.qualifier, c.origin, b.title, b.kind FROM hadith_citations c LEFT JOIN hadith_books b ON b.id = c.book"
                " WHERE c.hadith_key = ? ORDER BY c.origin = 'nurpedia', c.id", (key,)):
            if (mark := (row["title"] or row["raw"], row["raw"])) in seen or len(out) >= MAX_CITATIONS:
                continue
            seen.add(mark)
            out.append({k: v for k, v in {"book": row["title"], "kind": row["kind"], "citation": row["raw"],
                                          "qualifier": row["qualifier"], "from": row["origin"]}.items() if v})
        return out

    def hadith(self, report_id: str) -> dict:
        """Bir rivayetin metni, kitabı, âlimlerin dereceleri ve kaynağı."""
        row = self.conn.execute("SELECT * FROM hadith_reports WHERE id = ?", (report_id,)).fetchone()
        if row is None:
            raise LibraryError(f"No report with id {report_id!r}; use the ids find_hadith returns.")
        return _report_summary(row) | {"text": row["text"], "source": ATTRIBUTION[row["source"]],
                                       **({"linked_in_works": places} if (places := self._report_places(report_id)) else {}),
                                       "note": HADITH_NOTE}

    def _report_places(self, report_id: str, limit: int = MAX_CITATIONS) -> list[dict]:
        """Ters yön: rivayete bağlı Risale cümleleri, bağ tablosundan (`links`). Model okumalarının adayları
        (yerel `reading_lead`) girmez, onlar `find_hadith`'in `model_readings`'indedir."""
        from risale_mcp.links_hadis import target
        rows = self.conn.execute(
            "SELECT l.source, l.method, l.relation, s.ref, s.incipit, s.text FROM links l JOIN sentences s ON s.id = l.source"
            " WHERE l.target = ? AND l.file != 'hadis/reading_lead.jsonl' ORDER BY l.strength = 'weak', s.seq",
            (target(report_id),)).fetchall()
        out: dict[str, dict] = {}
        for r in rows:
            out.setdefault(r["source"], {"id": r["source"], "cite_as": hit_cite(r["ref"], r["incipit"], r["text"]),
                                         "method": r["method"], "relation": r["relation"]})
        return list(out.values())[:limit]

    def text_links(self, text_id: str, limit: int = 100) -> dict:
        """Metinden metne bağlar, iki yönde (T4; araca T6'da bağlanır): verilen cümleye, aralığa ya da bölüme (alt
        bölümleriyle) dokunan bağlar. Her bağda öbür uç: kimliği, atfı (bu veritabanındaysa veriden, değilse bağın
        kayıtlı atfından), bu sunucuda olup olmadığı; tür, ilişki, yöntem, güç, kanıt ve denetim kararları."""
        from risale_mcp.links import TEXT_NAMESPACES, cite_as, local_id, resolve, text_endpoint
        here = resolve(self.conn, text_id)
        if here is None:
            raise LibraryError(f"No sentence, range or section {text_id!r}.")
        node, ns = here["node"], here["namespace"]

        def seqs(end: dict) -> tuple[int, int] | None:
            """Ucun cümle sırası aralığı; bölüm ucu için None."""
            if end["kind"] == "section":
                return None
            first, _, last = end["id"].partition("..")
            a = self.conn.execute("SELECT seq FROM sentences WHERE id = ?", (first,)).fetchone()[0]
            if last:
                last = last if "/" in last else f"{first.rsplit('/', 1)[0]}/{last}"
                return a, self.conn.execute("SELECT seq FROM sentences WHERE id = ?", (last,)).fetchone()[0]
            return a, a

        span = seqs(here)

        def touches(value: str, scope: str | None) -> bool:
            end = resolve(self.conn, value, scope)
            if end is None:
                return False
            if span is None:                                   # bölüm: kendisi ve altındaki her şey
                return end["id"] == text_id or end["id"].startswith(text_id + "/")
            other = seqs(end)
            return other is not None and other[0] <= span[1] and span[0] <= other[1]

        text_targets = " OR ".join("target LIKE ?" for _ in TEXT_NAMESPACES)     # ad alanları koleksiyonlardan (H4)
        rows = self.conn.execute(
            f"SELECT * FROM links WHERE ({text_targets}) AND (source = ? OR source LIKE ? OR target = ? OR target LIKE ?)",
            (*(f"{n}:%" for n in TEXT_NAMESPACES), node, node + "/%", f"{ns}:{node}", f"{ns}:{node}/%")).fetchall()
        out = []
        for r in rows:
            if not text_endpoint(r["target"]):
                continue
            outgoing = touches(r["source"], r["scope"])
            incoming = touches(r["target"], None)
            if not (outgoing or incoming):
                continue
            other, other_scope, stored = ((r["target"], None, r["target_display"]) if outgoing
                                          else (r["source"], r["scope"], r["display"]))
            shown = cite_as(self.conn, other, other_scope)
            item = {"direction": "out" if outgoing else "in", "other": local_id(other),
                    "cite_as": shown or stored, "available": shown is not None,
                    "type": r["type"], "relation": r["relation"], "method": r["method"], "strength": r["strength"]}
            if r["evidence"]:
                item["evidence"] = json.loads(r["evidence"])
            if reviews := self._reviews(r["source"], r["target"], r["type"], r["part"] or ""):
                item["reviews"] = reviews
            out.append(item)
        out.sort(key=lambda x: (x["strength"] == "weak", x["direction"], x["other"]))
        return {"text": text_id, "total": len(out), "links": out[:limit]}

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
