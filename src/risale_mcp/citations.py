"""Atıf denetimi: metindeki "Eser › Bölüm › “ilk kelimeler…”" atıflarını veritabanında bulur.

`verify_citations` aracı (model cevabını vermeden önce atıflarını denetletir) ve altın soru raporu
(`golden.py`) bunu kullanır.

Bir satırda birden çok atıf, atıflardan önce ve sonra düz yazı olabilir. Satır `›` işaretlerinden
parçalara bölünür ve soldan sağa yürünür:
- Atfın başı bir parçanın son kelimeleridir ("Bu temsil Sözler" → "Sözler"); en uzun uyan son
  kelimeler alınır. Eser adı yazılmamış olabilir ("Onuncu Söz › …"). "…" ya da "aynı yer" bir
  önceki atfın bölümüdür.
- Sonraki her parça bir alt bölümdür. Parça başlıktan sonra düz yazıyla sürebilir
  ("Dördüncü Söz'de geçer."); atıf o başlıkta biter, sonraki atıf aynı parçanın sonunda başlayabilir.
- Atıf bir alıntıyla (“…”, "…") ya da cümle numarasıyla ("32. cümle", ardından "› Hâşiye › 2. cümle")
  biter. Tırnak içinde bir başlık ya da alt başlık yazılmışsa atıf o bölümdür.

Başlıklar basılı adla, içindekiler adıyla ya da tür ve numarayla eşleşir ("İkinci Makam" =
"Yirminci Söz’ün İkinci Makamı"); ekli yazılış da olur ("Dördüncü Söz'de"). Ara başlıklar atlanmış
olabilir ("Onuncu Söz › Dokuzuncu Hakikat"). Böyle bulunan atıf geçerlidir ama tam yolu yazılmamıştır
(`exact` yanlış); araç modele tam yolu verir.

Aynı yol birden çok bölüme uyabilir ("Birinci Mebhas"). Alıntı varsa geçtiği bölüm seçilir. Yoksa
sırasıyla bir önceki atfa yakın olan, ana ciltteki ve başlık ağacında daha üstteki bölüm; yine
ayrılamazsa atıf belirsizdir.
"""

import re
import sqlite3
from bisect import bisect_left, bisect_right
from dataclasses import dataclass, field

from risale_mcp.catalog import Group
from risale_mcp.headings import parse_heading
from risale_mcp.library import Library
from risale_mcp.normalize import parse_ordinal, search_words

MAX_TITLE_WORDS = 12        # bir başlık en çok bu kadar kelime sayılır
MAX_HEADING_WORDS = 7       # bulunamayan bölüm adı sayılacak parçanın üst sınırı
NUMBERED_WORDS = 5          # tür ve numarayla eşleşen başlığın üst sınırı ("Otuzuncu Lem'anın Beşinci Nüktesi")
SKIPPED_LEVELS = 3          # yolda atlanabilecek ara başlık sayısı
PHRASE_WORDS = 6            # alıntının aramada kullanılan ilk kelimeleri
ELSEWHERE = 3               # bölümde bulunamayan alıntının başka yerde gösterilen en çok geçişi
GROUP_RANK = {Group.ANA_CILT: 0, Group.ESKI_SAID: 1, Group.MECMUA: 2, Group.HIZB: 3}

_QUOTED = (re.compile(r'^"\s*(.+?)\s*(?:…|\.\.\.)?\s*"'), re.compile(r"^[“«]\s*(.+?)\s*(?:…|\.\.\.)?\s*[”»]"))
_SENTENCE_NO = re.compile(r"^(\d+)\.\s*cümle\b", re.IGNORECASE)
_HASIYE = re.compile(r"^Hâşiye(?:\s+(\d+))?$", re.IGNORECASE)
_SUFFIX = re.compile(r"['’][^\W\d_]+$")                 # "Söz'de" -> "Söz"
_MARKUP = re.compile(r"[*_`#>]+")
_EDGE = " \t-–—:;,.…()[]"
_ELLIPSIS = ("…", "...")
_SAME_PLACE = ("aynı yer", "aynı bölüm")                # ve boş baş ("(› …", "… › …"): bir önceki atfın bölümü
_PARENTHETICAL = re.compile(r"\s*\([^)]*\)$")            # "Mu'cizât‑ı Ahmediye (asm)"


def _key(text: str) -> str:
    return " ".join(search_words(text))


def _clean(text: str) -> str:
    return _MARKUP.sub("", text).strip(_EDGE)


def _opening(sentence: sqlite3.Row) -> str:
    """Cümlenin ilk kelimeleri; cümle daha uzunsa "…" ile."""
    incipit = sentence["incipit"]
    return incipit if len(incipit) >= len(sentence["text"].rstrip()) else incipit + "…"


def _quote(segment: str) -> str | None:
    """Parçanın başındaki alıntı."""
    text = _MARKUP.sub("", segment).strip(" :–—(")
    for pattern in _QUOTED:
        if m := pattern.match(text):
            return m[1]
    return None


@dataclass(frozen=True)
class _Title:
    """Yazılmış bir başlık: karşılaştırma anahtarları, (sıra sayısıyla başlıyorsa) tür ve numarası,
    "…" ile kısaltılmışsa başlığın başı olduğu."""
    keys: frozenset[str]
    heading: tuple[str, int] | None
    truncated: bool = False

    @classmethod
    def of(cls, text: str, truncated: bool = False) -> "_Title":
        text = _clean(text)
        bare = _SUFFIX.sub("", text)
        keys = frozenset(k for k in (_key(text), _key(bare)) if k)
        words = bare.split()
        heading = None
        if words and len(words) <= NUMBERED_WORDS and not re.search(r"[.!?;]", bare) and (
                parse_ordinal(words[0]) is not None or len(words) > 1 and parse_ordinal(words[0] + words[1]) is not None):
            info = parse_heading(bare)
            if info.type and info.number is not None:
                heading = (info.type, info.number)
        return cls(keys, heading, truncated and any(len(k.split()) > 1 for k in keys))


@dataclass(frozen=True)
class _Node:
    id: str
    work: str
    parent: str | None
    ord: int
    last_ord: int
    depth: int
    ref: str
    keys: frozenset[str]            # basılı başlık ve içindekiler adı
    subtitle: str | None
    heading: tuple[str, int] | None
    rank: int                       # eserin grubu: ana ciltler önce

    def matches(self, title: _Title) -> bool:
        if title.truncated:
            return any(k.startswith(t) for k in self.keys for t in title.keys)
        return bool(self.keys & title.keys) or title.heading is not None and title.heading == self.heading


@dataclass
class Citation:
    """Bir atfın sonucu. `status`:
    - ok: cümle bulundu (alıntı cümlenin başı ya da numarası doğru)
    - section: bölüm var, denetlenecek alıntı yok
    - mid_sentence: alıntı bölümde var ama bir cümlenin başı değil
    - quote_not_found: bölüm var, alıntı yok (`elsewhere`: alıntının geçtiği yerler)
    - no_such_sentence: bölümde o numarada cümle yok
    - unknown_section: yola uyan bölüm yok (`missing`; `node` varsa ondan sonrası bulunamadı)
    - ambiguous: yol birden çok bölüme uyuyor (`candidates`)"""
    written: str                         # atfın metindeki hâli
    status: str
    node: str | None = None
    ref: str | None = None               # bölümün tam yolu
    exact: bool = True                   # yol tam olarak yazılmış mı
    quote: str | None = None
    number: int | None = None
    sentence: str | None = None          # bulunan cümle
    opening: str | None = None           # cümlenin ilk kelimeleri ("…" ile)
    elsewhere: list[dict] = field(default_factory=list)   # bölümde olmayan alıntının bulunduğu cümleler
    candidates: list[str] = field(default_factory=list)   # belirsiz yolun uyduğu bölümler
    missing: str | None = None           # bulunamayan bölüm adı

    @property
    def cite_as(self) -> str | None:
        """Kullanıcıya gösterilecek tam atıf: yol ve cümlenin ilk kelimeleri."""
        if self.sentence and self.opening:
            return f"{self.ref} › “{self.opening}”"
        return self.ref

    def problem(self) -> str | None:
        """Modelin düzeltmesi gereken şey (İngilizce); sorun yoksa None."""
        if self.status in ("ok", "section"):
            return None if self.exact else f"Valid, but write the full path: {self.cite_as}"
        if self.status == "mid_sentence":
            begins = f"; the sentence begins “{self.opening}”, cite it as {self.cite_as}" if self.opening else ""
            return f"The quoted words are in {self.ref} but do not start a sentence{begins}."
        if self.status == "no_such_sentence":
            return f"{self.ref} has no sentence {self.number}."
        if self.status == "ambiguous":
            return "The path matches several sections: " + "; ".join(self.candidates) + ". Write the full path."
        where = f"These words are not in {self.ref}." if self.status == "quote_not_found" else (
            f"No section “{self.missing}” under {self.ref}; check it with get_outline('{self.node}')."
            if self.node else f"No section matches “{self.missing or self.written}”; check the path with get_outline.")
        if self.elsewhere:
            return where + " The quoted words occur at: " + "; ".join(f"{e['cite_as']} ({e['id']})" for e in self.elsewhere)
        return where + (" Quote only text returned by the tools." if self.quote else "")

    def to_dict(self) -> dict:
        record = {"citation": self.written if len(self.written) <= 200 else self.written[:200] + "…",
                  "status": self.status}
        if self.sentence:
            record["sentence"] = self.sentence
        elif self.node:
            record["section"] = self.node
        if problem := self.problem():
            record["problem"] = problem
        return record


class CitationChecker:
    """Başlık ağacının dizini; veritabanı yeniden kurulunca (yeni bağlantı) dizin de yenilenir."""

    def __init__(self, library: Library) -> None:
        self.library = library
        self._conn: sqlite3.Connection | None = None

    @property
    def conn(self) -> sqlite3.Connection:
        return self.refresh()

    def refresh(self) -> sqlite3.Connection:
        """Güncel bağlantı; veritabanı yeniden kurulduysa önce dizin yenilenir."""
        conn = self.library.conn
        if conn is not self._conn:
            self._conn = conn
            self._index(conn)
        return conn

    def _index(self, conn: sqlite3.Connection) -> None:
        ranks = {w: GROUP_RANK.get(g, len(GROUP_RANK)) for w, g in conn.execute("SELECT slug, group_name FROM works")}
        self.nodes: dict[str, _Node] = {}
        self.by_key: dict[str, list[_Node]] = {}
        self.by_heading: dict[tuple[str, int], list[_Node]] = {}
        self.children: dict[str, list[_Node]] = {}
        self.in_order: dict[str, list[_Node]] = {}         # eser -> düğümler kitap sırasıyla
        for row in conn.execute("SELECT id, work, parent_id, ord, last_ord, depth, title, toc_title, subtitle, type,"
                                " number, ref FROM nodes ORDER BY work, ord"):
            heading = (row["type"], row["number"]) if row["type"] and row["number"] is not None else None
            titles = [t for t in (row["title"], row["toc_title"]) if t]
            keys = frozenset(_key(v) for t in titles for v in (t, _PARENTHETICAL.sub("", t)))
            node = _Node(row["id"], row["work"], row["parent_id"], row["ord"], row["last_ord"], row["depth"],
                         row["ref"], keys, row["subtitle"], heading, ranks.get(row["work"], len(GROUP_RANK)))
            self.nodes[node.id] = node
            for k in keys:
                self.by_key.setdefault(k, []).append(node)
            if heading:
                self.by_heading.setdefault(heading, []).append(node)
            if node.parent:
                self.children.setdefault(node.parent, []).append(node)
            self.in_order.setdefault(node.work, []).append(node)
        self.ords = {work: [n.ord for n in nodes] for work, nodes in self.in_order.items()}

    # ------------------------------------------------------------ metindeki atıflar

    def check(self, text: str) -> list[Citation]:
        """Metindeki atıflar, yazıldıkları sırayla."""
        self.refresh()
        out: list[Citation] = []
        context: _Node | None = None
        for line in text.splitlines():
            segments = line.split("›")
            i = 0
            while i < len(segments) - 1:
                citation, i = self._chain(segments, i, context)
                if citation:
                    out.append(citation)
                    context = self.nodes.get(citation.node) if citation.node else context
        return out

    def _chain(self, segments: list[str], i: int, context: _Node | None) -> tuple[Citation | None, int]:
        """`segments[i]`in sonunda başlayan atıf ve sonraki atfın aranacağı parça."""
        starts, head = self._start(segments[i], context)
        if not starts:
            return self._unknown_head(segments, i)
        path, j = [head], i + 1
        quote = number = None
        while j < len(segments):
            segment = segments[j]
            if (quote := _quote(segment)) is not None:
                break
            if m := _SENTENCE_NO.match(_clean(segment)):
                number = int(m[1])
                while j + 1 < len(segments) and (_HASIYE.match(_clean(segments[j + 1]))
                                                 or _SENTENCE_NO.match(_clean(segments[j + 1]))):
                    j += 1                               # "› Hâşiye › 2. cümle": ana cümlenin atfıdır
                break
            if _HASIYE.match(_clean(segment)):
                path.append(_clean(segment))             # "› Hâşiye ›": alıntı bölümün hâşiyesindedir
                j += 1
                continue
            found = self._step(starts, segment)
            if found is None:
                if self._looks_like_heading(segment):
                    return self._unknown_step(segments, j, starts, context), j + 1
                break
            starts, title, rest = found
            path.append(title)
            if rest:
                break
            j += 1
        written = " › ".join([*path, *([f"“{quote}”"] if quote else []), *([f"{number}. cümle"] if number else [])])
        return self._resolve(written, path, starts, context, quote, number), j

    def _start(self, segment: str, context: _Node | None) -> tuple[list[_Node], str]:
        """Parçanın en uzun uyan son kelimeleri ve uydukları düğümler. Boş baş ("… ›", "(› …") bir önceki
        atfın bölümü ve onun üst bölümleridir; ardından gelen başlık bunların herhangi birinde olabilir."""
        text = _clean(segment)
        if context and (not text or segment.rstrip().endswith("(") or text in _SAME_PLACE
                        or text.endswith(tuple(f" {p}" for p in _SAME_PLACE))):
            return self._ancestors(context), "…"
        words = text.split()
        for k in range(min(len(words), MAX_TITLE_WORDS), 0, -1):
            title = _clean(" ".join(words[-k:]))
            if nodes := self._lookup(_Title.of(title)):
                return nodes, title
        return [], ""

    def _ancestors(self, node: _Node) -> list[_Node]:
        """Düğüm ve üst bölümleri, en yakını önce."""
        out = [node]
        while out[-1].parent:
            out.append(self.nodes[out[-1].parent])
        return out

    def _lookup(self, title: _Title) -> list[_Node]:
        found = {n.id: n for k in title.keys for n in self.by_key.get(k, ())}
        if title.heading:
            found |= {n.id: n for n in self.by_heading.get(title.heading, ())}
        return list(found.values())

    def _step(self, parents: list[_Node], segment: str, whole: bool = False) -> tuple | None:
        """Parçanın en uzun uyan ilk kelimeleri (`whole` ise bütünü): (alt düğümler, başlık, kalan metin
        var mı). Önce doğrudan alt bölümlerde, yoksa birkaç seviye aşağıda, en son bölümün kendisinde
        aranır ("… › Dördüncü Remiz": bir önceki atfın bölümü yeniden yazılmış)."""
        words = _clean(segment).split()
        truncated = _MARKUP.sub("", segment).rstrip(" :").endswith(_ELLIPSIS)
        lengths = [len(words)] if whole else range(min(len(words), MAX_TITLE_WORDS), 0, -1)
        for k in lengths:
            title_text = _clean(" ".join(words[:k]))
            title = _Title.of(title_text, truncated=truncated and k == len(words))
            if not title.keys:
                continue
            found = [c for p in parents for c in self.children.get(p.id, ()) if c.matches(title)]
            if not found:
                found = [d for p in parents for d in self._descendants(p) if d.matches(title)]
            if not found:
                found = [p for p in parents if p.matches(title)]
            if found:
                return found, title_text, k < len(words)
        return None

    def _descendants(self, node: _Node) -> list[_Node]:
        ords = self.ords[node.work]
        nodes = self.in_order[node.work][bisect_right(ords, node.ord):bisect_left(ords, node.last_ord + 1)]
        return [n for n in nodes if n.depth <= node.depth + SKIPPED_LEVELS + 1]

    @staticmethod
    def _looks_like_heading(segment: str) -> bool:
        text = _clean(segment)
        return (bool(text) and len(text.split()) <= MAX_HEADING_WORDS and (text[0].isupper() or text[0].isdigit())
                and not re.search(r"[.!?;\"“”]", text))

    # ------------------------------------------------------------ çözüm

    def _resolve(self, written: str, path: list[str], nodes: list[_Node], context: _Node | None,
                 quote: str | None, number: int | None) -> Citation:
        nodes = sorted(nodes, key=lambda n: self._preference(n, context))
        if quote is not None:
            inside = None                                # cümlenin başı olmayan ilk geçiş
            for node in nodes:
                status, sentence = self._find_quote(quote, node)
                if status == "ok":
                    return self._citation(written, path, node, status, quote=quote, sentence=sentence)
                if status == "mid_sentence" and inside is None:
                    inside = node, sentence
            if inside:
                return self._citation(written, path, inside[0], "mid_sentence", quote=quote, sentence=inside[1])
            if titled := self._quoted_title(nodes, quote, path):
                return self._resolve(written, *titled, context, None, None)
        elif number is not None:
            for node in nodes:
                if row := self.conn.execute("SELECT * FROM sentences WHERE node_id = ? AND n = ? AND hasiye = 0",
                                            (node.id, number)).fetchone():
                    return self._citation(written, path, node, "ok", number=number, sentence=row)
        if len(nodes) > 1 and self._preference(nodes[0], context) == self._preference(nodes[1], context):
            return Citation(written, "ambiguous", quote=quote, number=number,
                            candidates=[n.ref for n in nodes[:5]],
                            elsewhere=self._elsewhere(quote) if quote else [])
        node = nodes[0]
        if quote is not None:
            return self._citation(written, path, node, "quote_not_found", quote=quote, elsewhere=self._elsewhere(quote))
        if number is not None:
            return self._citation(written, path, node, "no_such_sentence", number=number)
        return self._citation(written, path, node, "section")

    def _quoted_title(self, nodes: list[_Node], quote: str, path: list[str]) -> tuple | None:
        """Metinde bulunmayan alıntı bir başlık ya da alt başlıksa atıf o bölümdür: (yol, düğümler)."""
        if found := self._step(nodes, quote, whole=True):
            sections, title, _ = found
            return ([*path, title] if not set(sections) <= set(nodes) else path), sections
        if subtitled := [n for n in nodes if n.subtitle and _key(n.subtitle) == _key(quote)]:
            return path, subtitled
        return None

    @staticmethod
    def _preference(node: _Node, context: _Node | None) -> tuple:
        """Küçük olan önce: bir önceki atfa yakınlık, eserin grubu, başlık ağacındaki derinlik."""
        closeness = 0
        if context and context.work == node.work:
            a, b = context.id.split("/"), node.id.split("/")
            closeness = next((k for k, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b))) + 1
        return -closeness, node.rank, node.depth

    def _citation(self, written: str, path: list[str], node: _Node, status: str,
                  sentence: sqlite3.Row | None = None, **fields) -> Citation:
        typed = [_Title.of(p).keys for p in path if not _HASIYE.match(p)]       # ekli yazılış da tamdır
        printed = [_key(p) for p in node.ref.split("›")]
        exact = len(typed) == len(printed) and all(k in keys for k, keys in zip(printed, typed))
        citation = Citation(written, status, node.id, node.ref, exact, **fields)
        if sentence is not None:
            citation.sentence, citation.opening = sentence["id"], _opening(sentence)
            # Alt bölümdeki cümlenin atfı kendi bölümünün yoludur.
            if sentence["node_id"] != node.id:
                citation.ref = self.nodes[sentence["node_id"]].ref
                citation.exact = False
        return citation

    def _unknown_head(self, segments: list[str], i: int) -> tuple[Citation | None, int]:
        """Başı hiçbir bölüme uymayan atıf. Başlığın düz yazının neresinde başladığı bilinemez; son
        kelimeler ve ardından gelen başlığa benzer parçalar bulunamayan yol sayılır. Ardından başlık
        ya da alıntı gelmiyorsa `›` düz yazıdadır, atlanır."""
        head = " ".join(_clean(segments[i]).split()[-3:])
        following = segments[i + 1]
        if not (self._looks_like_heading(head) and (self._looks_like_heading(following) or _quote(following))):
            return None, i + 1
        j = i + 1
        while j < len(segments) and self._looks_like_heading(segments[j]):
            j += 1
        missing = " › ".join([head, *(_clean(s) for s in segments[i + 1:j])])
        quote = _quote(segments[j]) if j < len(segments) else None
        written = missing + (f" › “{quote}”" if quote else "")
        return Citation(written, "unknown_section", quote=quote, missing=missing,
                        elsewhere=self._elsewhere(quote) if quote else []), j

    def _unknown_step(self, segments: list[str], j: int, parents: list[_Node], context: _Node | None) -> Citation:
        """Yolun `segments[j]` parçası bulunamadı; atıf bulunan son bölümle birlikte bildirilir."""
        parent = min(parents, key=lambda n: self._preference(n, context))
        quote = _quote(segments[j + 1]) if j + 1 < len(segments) else None
        missing = _clean(segments[j])
        written = " › ".join([parent.ref, missing, *([f"“{quote}”"] if quote else [])])
        return Citation(written, "unknown_section", parent.id, parent.ref, quote=quote, missing=missing,
                        elsewhere=self._elsewhere(quote) if quote else [])

    # ------------------------------------------------------------ alıntılar

    def _find_quote(self, quote: str, node: _Node) -> tuple[str, sqlite3.Row | None]:
        """Alıntının bölümde geçtiği ilk cümle: ("ok" | "mid_sentence" | "quote_not_found", cümle).
        Son kelime eksik yazılmış olabilir; alıntı sonraki cümleye taşabilir. Alıntının içinde "…" ile
        atlanan yer varsa cümle ilk parçadan bulunur, diğer parçalar bölümün metninde aranır."""
        first, *rest = [part for part in re.split(r"…|\.\.\.", quote) if _key(part)] or [quote]
        found = self._quote_sentences(first, node, limit=1)
        if found and not rest:
            return found[0]
        texts = [_key(p[0]) for p in self.conn.execute(
            "SELECT p.text FROM paragraphs p JOIN nodes n ON n.id = p.node_id"
            " WHERE n.work = ? AND n.ord BETWEEN ? AND ? AND p.text IS NOT NULL", (node.work, node.ord, node.last_ord))]
        if not all(any(_key(part) in t for t in texts) for part in rest):
            return "quote_not_found", None
        if found:
            return found[0]
        if any(_key(first) in t for t in texts):
            return "mid_sentence", None            # cümle sınırını aşan parça
        return "quote_not_found", None

    def _quote_sentences(self, quote: str, node: _Node | None, limit: int) -> list[tuple[str, sqlite3.Row]]:
        words = search_words(quote)
        if not words:
            return []
        phrase = words[:PHRASE_WORDS]
        match = '"' + " ".join(phrase) + '"' + ("*" if len(phrase) == len(words) else "")
        sql = ("SELECT s.* FROM sentences_fts JOIN sentences s ON s.seq = sentences_fts.rowid"
               " WHERE sentences_fts MATCH ?")
        params: list = [match]
        if node:
            sql += " AND s.work = ? AND s.node_id IN (SELECT id FROM nodes WHERE work = ? AND ord BETWEEN ? AND ?)"
            params += [node.work, node.work, node.ord, node.last_ord]
        found = []
        for row in self.conn.execute(sql + " ORDER BY s.seq", params):
            if (at := self._quote_at(words, row)) is not None:
                found.append(("ok" if at == 0 else "mid_sentence", row))
                if len(found) >= limit:
                    break
        return found

    def _quote_at(self, words: list[str], row: sqlite3.Row) -> int | None:
        """Alıntının cümlede başladığı kelime. Alıntı paragrafın sonraki cümlelerine taşabilir; son
        kelimesi eksik yazılmış olabilir."""
        stream = search_words(row["text"])
        starts = [at for at, word in enumerate(stream) if word == words[0] or len(words) == 1 and word.startswith(words[0])]
        if starts and len(stream) - starts[-1] < len(words):
            stream = stream + [w for (text,) in self.conn.execute(
                "SELECT text FROM sentences WHERE paragraph_id = ? AND seq > ? ORDER BY seq",
                (row["paragraph_id"], row["seq"])) for w in search_words(text)]
        for at in starts:
            found = stream[at:at + len(words)]
            if len(found) == len(words) and found[:-1] == words[:-1] and found[-1].startswith(words[-1]):
                return at
        return None

    def _elsewhere(self, quote: str) -> list[dict]:
        out = []
        for _, row in self._quote_sentences(quote, None, ELSEWHERE):
            ref = self.nodes[row["node_id"]].ref
            out.append({"id": row["id"], "cite_as": f"{ref} › “{_opening(row)}”"})
        return out


def summary(citations: list[Citation]) -> dict:
    """Aracın sonucu: atıflar ve sorunlu olanların sayısı."""
    return {"checked": len(citations),
            "problems": sum(c.problem() is not None for c in citations),
            "citations": [c.to_dict() for c in citations]}
