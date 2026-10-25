"""erisale blokları -> eser modeli (Aşama 2).

Kurallar:
- Her H1–H6 başlığı bir düğümdür; ağaç başlık seviyelerinden kurulur.
- `TocOnly` başlık yalnızca sitenin içindekiler listesinde görünür ama yine düğümdür:
  "On iki Hakikat" gibi grup başlıkları kendi giriş metnini taşıyabilir.
- `BookOnly` başlık yeni düğüm açmaz; aynı seviyedeki açık `TocOnly` düğümün basılı
  başlığıdır. İçindekilerdeki ad `toc_title` alanına geçer.
- Başlığın içindeki satır içi başlık ("Onuncu Söz" + "Haşir Bahsi") ve başlıktan hemen
  sonraki `HeadingDescription` blokları alt başlıktır.
- Paragraf başındaki biçimli numaralı etiket ("Birinci Esas:", "Birinci Kâr:") düğüm
  açar; düğüm aynı türden bir sonraki etikete ya da bir sonraki blok başlığına kadar
  sürer. Diğer etiketler ("Birincisi:", "Onuncu Söz'den") metinde kalır. Etiket metinde
  de kalır, çünkü basılı metnin parçasıdır.
- Seçilen bölümlerde tek bir en üst başlık varsa (ör. İlk Dönem Eserleri içindeki
  "Münâzarât") o başlık eserin kendisidir, ayrı düğüm açmaz.
- Paragraf türleri: paragraph, arabic, poem, quote, signature, table, hasiye. Art arda gelen
  şiir satırları `PoemBreak`'e kadar tek paragraftır. `ContinuedParagraph` araya giren
  bir bloktan sonra süren paragraftır (`continued: true`).
- Editör notları (`Comment`) metne girmez, `notes` alanına yazılır. Bölüm ayıraçları
  (`ThematicBreak`, `GroupStart`, `GroupEnd`) atılır.
- Kaynakta bulunmayan bloklar `gaps` alanında işaretlenir; metin uydurulmaz.
"""

import re
from collections import Counter
from dataclasses import dataclass, field

from risale_mcp.books.model import ArabicSpan, Book, Node, Text, TextBuilder
from risale_mcp.catalog import Work
from risale_mcp.headings import HeadingInfo, clean_label, local_id, parse_heading, parse_inline_label
from risale_mcp.normalize import fold, slugify
from risale_mcp.sources.erisale import BookBlocks

_HEADING = re.compile(r"H([1-6])")
_LEADING_NUMBER = re.compile(r"^\d+\.\s+")
_SEGMENT_NUMBER = re.compile(r"\[\d+\]\s*")   # erisale'nin Arapça metindeki bölüm numarası: "[1]"
PARAGRAPH_KINDS = {
    "Paragraph": "paragraph",
    "CenteredParagraph": "paragraph",
    "ContinuedParagraph": "paragraph",
    "Blockquote": "quote",
    "Signature": "signature",
    "PrefatoryNote": "paragraph",   # mektubun başındaki tarih: "(5 Şubat 1934)"
}
SKIPPED = {"ThematicBreak", "GroupStart", "GroupEnd"}
# Paragraf başındaki numaralı etiket bunlardan biriyle işaretlenir: "Birinci Esas:" (Heading),
# "Birinci Kâr:" (Mark), "İkinci temsîl:" (Bold), "Birinci Kelime:" (BoldItalic).
LABEL_TYPES = {"Heading", "Mark", "Bold", "BoldItalic"}


# ---------------------------------------------------------------- satır içi metin

def _render(node: dict, builder: TextBuilder, skip_headings: bool) -> None:
    kind = node.get("type")
    if kind == "Meta" or (kind == "Heading" and skip_headings):
        return
    if kind == "FootnoteRef":                     # "Hâşiye" etiketi metne girmez
        if "footnote" in node:
            builder.mark_footnote(node["footnote"]["blocks"])
        return
    if "value" in node:
        rtl = node.get("rtl")
        if rtl:
            span = ArabicSpan(0, 0, rtl.get("type") or "arabi", rtl.get("txn") or None, rtl.get("ref") or None)
            builder.add(node["value"], span, key=rtl.get("id"))
        else:
            builder.add(node["value"])
        return
    for child in node.get("children", []):
        _render(child, builder, skip_headings)


def inline_text(content: dict, skip_headings: bool = False) -> Text:
    builder = TextBuilder()
    for child in content.get("children", []):
        _render(child, builder, skip_headings)
    return Text.from_builder(builder)


def metas(content: dict) -> list[str]:
    """Bloğun yönergeleri: 'Section=', 'TocOnly=', 'TocTitle=Onuncu Söz (Haşir Bahsi)'…"""
    return [inline_text(c).text for c in content.get("children", []) if c.get("type") == "Meta"]


def _directive(content: dict, name: str) -> str | None:
    for meta in metas(content):
        if meta == name or meta.startswith(name + "="):
            return meta[len(name) + 1:]
    return None


def _subtitle(content: dict) -> str:
    return " ".join(inline_text(c).text for c in content.get("children", []) if c.get("type") == "Heading")


def _table(content: dict) -> Text:
    """Tablo: her satır bir satıra, hücreler " | " ile ayrılır."""
    rows = [Text.join([inline_text(cell) for cell in row.get("children", [])], " | ")
            for row in content.get("children", [])]
    return Text.join(rows, "\n")


def _inline_label(content: dict) -> str | None:
    """Paragrafın biçimli ilk parçası (satır içi başlık ya da vurgulu etiket)."""
    children = content.get("children", [])
    if children and children[0].get("type") in LABEL_TYPES:
        return inline_text({"children": children[:1]}).text
    return None


# ---------------------------------------------------------------- ayrıştırıcı

@dataclass
class ParseReport:
    unknown_blocks: Counter = field(default_factory=Counter)
    unmatched_book_only: list[str] = field(default_factory=list)   # eşi bulunmayan BookOnly başlıklar
    stray_descriptions: int = 0                                    # başlıktan uzak HeadingDescription
    inline_nodes: int = 0


class _Parser:
    def __init__(self, work: Work, source: BookBlocks):
        self.book = Book(work.slug, work.title, {
            "group": str(work.group),
            "source": {"site": str(work.source.site), "book": work.source.book,
                       "sections": list(work.source.sections), "exclude": list(work.source.exclude)},
        })
        self.report = ParseReport()
        self.urls = {p.slug: p.url for p in source.pages}
        self.missing = set(source.missing)
        self.blocks = [b for b in source.blocks if work.source.includes(b["page"])]
        self.stack: list[tuple[int, Node]] = [(0, self.book.root)]   # (başlık seviyesi, düğüm)
        self.inline: list[Node] = []                                 # açık satır içi düğümler
        self.toc_only: dict[int, Node] = {}                          # basılı başlığını bekleyenler
        self.subtitle_target: Node | None = None
        self.poem: list[Text] = []
        self.last_paragraph: dict | None = None
        self.position = 0                                            # işlenen bloğun sırası
        self.labels = self._inline_labels()                          # sıra -> numaralı etiket

    @property
    def current(self) -> Node:
        return self.inline[-1] if self.inline else self.stack[-1][1]

    def run(self) -> Book:
        root_block = self._root_heading_block()
        previous = None
        for self.position, block in enumerate(self.blocks):
            if previous is not None:
                self._mark_gap(previous, block["index"])
            previous = block["index"]
            content = block["content"]
            kind = content["type"]
            if kind != "Poem":
                self._flush_poem()
            if kind != "HeadingDescription" and not _HEADING.fullmatch(kind):
                self.subtitle_target = None

            if heading := _HEADING.fullmatch(kind):
                self._heading(block, int(heading[1]), is_root=block is root_block)
            elif kind == "HeadingDescription":
                self._description(content)
            elif kind == "Poem":
                self.poem.append(inline_text(content))
            elif kind in PARAGRAPH_KINDS:
                self._paragraph(content)
            elif kind == "Table":
                self._add("table", _table(content), {})
            elif kind == "Comment":
                self.book.notes.append({"node_id": self.current.id, "text": inline_text(content).text,
                                        "after": self.last_paragraph["id"] if self.last_paragraph else None})
            elif kind not in SKIPPED and kind != "PoemBreak":
                self.report.unknown_blocks[kind] += 1
                self._paragraph(content)          # bilinmeyen türün metni kaybolmasın
        self._flush_poem()
        return self.book

    # --- yapı

    def _root_heading_block(self) -> dict | None:
        """Seçilen bölümler tek bir en üst başlıkla açılıyorsa o başlık eserin kendisidir."""
        levels = [(b, int(m[1])) for b in self.blocks
                  if (m := _HEADING.fullmatch(b["content"]["type"])) and _directive(b["content"], "BookOnly") is None]
        if not levels:
            return None
        top = min(level for _, level in levels)
        tops = [b for b, level in levels if level == top]
        return tops[0] if len(tops) == 1 and tops[0] is self.blocks[0] else None

    def _heading(self, block: dict, level: int, is_root: bool) -> None:
        content = block["content"]
        title_text = inline_text(content, skip_headings=True)
        raw_title, subtitle = title_text.text, _SEGMENT_NUMBER.sub("", _subtitle(content))
        if not raw_title:                     # başlığın tamamı satır içi başlık: "Tenbih"
            raw_title, subtitle = subtitle, ""
        title = _LEADING_NUMBER.sub("", _SEGMENT_NUMBER.sub("", raw_title)).strip()
        self.inline.clear()

        if is_root:
            node = self.book.root
            self.stack = [(level, node)]
            node.subtitle, node.toc_title = subtitle, title if title != node.title else None
            node.url = self.urls.get(block["page"])
            if _directive(content, "TocOnly") is not None:
                self.toc_only[level] = node
        elif _directive(content, "BookOnly") is not None:
            node = self.toc_only.pop(level, None) or self._printed_heading_of(level, title)
            if node is None:
                self.report.unmatched_book_only.append(f"{block['index']}: {title}")
                node = self._open_node(block, level, raw_title, title, subtitle)
            else:
                if node.title != title and node is not self.book.root:   # kök, katalogdaki adıyla anılır
                    node.toc_title = node.toc_title or node.title
                    node.title = title
                node.subtitle = " ".join(filter(None, [node.subtitle, subtitle]))
        else:
            node = self._open_node(block, level, raw_title, title, subtitle)
            if _directive(content, "TocOnly") is not None:
                self.toc_only[level] = node

        self.subtitle_target = node
        self._hasiyeler(node.id, node, title_text)

    def _printed_heading_of(self, level: int, title: str) -> Node | None:
        """`TocOnly` eşi olmayan BookOnly başlık şu düğümlerin basılı başlığı olabilir:
        aynı seviyedeki açık düğüm, içindekiler adı bu başlığı içeriyorsa
        ("İkinci Makale (Unsuru'l-Belâğat)" -> "İkinci Makale"); ya da eserin kendisi."""
        if level == self.stack[0][0]:
            return self.book.root
        open_node = next((n for lvl, n in self.stack if lvl == level), None)
        if open_node and open_node.toc_title and fold(title) in fold(open_node.toc_title):
            return open_node
        return None

    def _open_node(self, block: dict, level: int, raw_title: str, title: str, subtitle: str) -> Node:
        while len(self.stack) > 1 and self.stack[-1][0] >= level:
            self.stack.pop()
        for pending_level in [lvl for lvl in self.toc_only if lvl >= level]:
            del self.toc_only[pending_level]
        parent = self.stack[-1][1]
        toc_title = _directive(block["content"], "TocTitle") or None
        info = parse_heading(raw_title)
        if info == HeadingInfo() and toc_title:      # Arapça başlık: "Birinci Bâb (اَلْبَابُ الْأَوَّلُ)"
            info = parse_heading(toc_title)
        slug_source = title if re.search(r"[a-z]", slugify(title)) else (toc_title or title)
        node = self.book.add_node(
            parent, local_id(info, slug_source, top_level=parent is self.book.root), title,
            type=info.type, number=info.number, heading=f"H{level}", subtitle=subtitle,
            toc_title=toc_title, url=self.urls.get(block["page"]))
        self.stack.append((level, node))
        return node

    def _inline_labels(self) -> dict[int, HeadingInfo]:
        labels = {}
        for position, block in enumerate(self.blocks):
            content = block["content"]
            if content["type"] in PARAGRAPH_KINDS and (label := _inline_label(content)):
                if info := parse_inline_label(label):
                    labels[position] = info
        return labels

    def _series_continues(self, node: Node) -> bool:
        """Açık satır içi serinin bir sonraki halkası, bir sonraki blok başlığından önce geliyor mu?"""
        for position in range(self.position + 1, len(self.blocks)):
            if _HEADING.fullmatch(self.blocks[position]["content"]["type"]):
                return False
            info = self.labels.get(position)
            if info and info.type == node.type and info.number and node.number and info.number > node.number:
                return True
        return False

    def _open_inline_node(self, label: str) -> None:
        info = parse_inline_label(label)
        if info is None:
            return
        same = next((i for i in range(len(self.inline) - 1, -1, -1) if self.inline[i].type == info.type), None)
        if same is not None:
            del self.inline[same:]                    # aynı serinin sonraki halkası: kardeş
        else:
            # Yeni seri: açık seri sonra sürüyorsa onun içindedir ("Birinci Hakikat"in "Esas"ları),
            # sürmüyorsa onun kardeşidir (beş "Kâr"dan sonra beş "Hasaret").
            while self.inline and not self._series_continues(self.inline[-1]):
                self.inline.pop()
        title = clean_label(label)
        self.inline.append(self.book.add_node(
            self.current, local_id(info, title, top_level=False), title,
            type=info.type, number=info.number, heading="inline"))
        self.report.inline_nodes += 1

    # --- metin

    def _description(self, content: dict) -> None:
        if self.subtitle_target is None:
            self.report.stray_descriptions += 1
            self._paragraph(content)
            return
        node = self.subtitle_target
        node.subtitle = " ".join(filter(None, [node.subtitle, inline_text(content).text]))

    def _paragraph(self, content: dict) -> None:
        label = _inline_label(content)
        if label:
            self._open_inline_node(label)
        text = inline_text(content)
        if not text.text and not text.footnotes:
            return
        kind = PARAGRAPH_KINDS.get(content["type"], "paragraph")
        extra = {}
        if text.is_arabic():
            kind = "arabic"
        elif content["type"] == "CenteredParagraph":
            extra["center"] = True
        if content["type"] == "ContinuedParagraph":
            extra["continued"] = True
        self._add(kind, text, extra)

    def _flush_poem(self) -> None:
        if self.poem:
            self._add("poem", Text.join(self.poem, "\n"), {})
            self.poem = []

    def _add(self, kind: str, text: Text, extra: dict) -> None:
        node = self.current
        record = self.book.add_paragraph(node, kind, text, **extra)
        self.last_paragraph = record
        self._hasiyeler(record["id"], node, text)

    def _hasiyeler(self, parent_id: str, node: Node, text: Text) -> None:
        for mark in text.footnotes:
            body = Text.join([inline_text(block) for block in mark.content], "\n")
            record = self.book.add_hasiye(parent_id, node, mark.offset, body)
            self._hasiyeler(record["id"], node, body)    # hâşiyenin hâşiyesi

    def _mark_gap(self, previous: int, index: int) -> None:
        lost = self.missing.intersection(range(previous + 1, index))
        if lost:
            self.book.gaps.append({
                "node_id": self.current.id, "missing_blocks": len(lost),
                "after": self.last_paragraph["id"] if self.last_paragraph else None,
            })


def parse_work(work: Work, source: BookBlocks) -> tuple[Book, ParseReport]:
    parser = _Parser(work, source)
    return parser.run(), parser.report
