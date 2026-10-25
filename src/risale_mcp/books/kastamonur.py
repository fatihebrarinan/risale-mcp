"""kastamonur.com (Âsâr-ı Bedîiyye baskısı) -> eser modeli: Nutuk ve Makalat.

"Nutuklar ve Makaleler" tek sayfadır, iki bölümü vardır: "Nutuklar" (`h1`) ve "Makaleler
Kısmı" (ortalı satır). Katalogdaki bölüm seçici `nutuklar` ya da `makaleler`dir.

- Her `h2` ("Nutuk – 2", "Makale – 5") bir nutuk ya da makaledir; kimliği numarasıdır
  (`makalat/makale-05`). Basılı adı, hemen altındaki tamamı kalın paragraftır ("Mebusana
  Hitabı"); öncesindeki ve ardındaki yayın satırları (gazete, tarih, sayı) alt başlıktır. Kalın
  ad yoksa `h2`'nin kendisi başlıktır. `h3` alt bölümdür. İlk `h2`'den önceki tamamı kalın
  paragraf ("İfade-i Meram") de bir düğümdür.
- Arapça `dir="rtl"` ile işaretlidir ve Unicode sunum biçimleriyle yazılmıştır ("ﻳَٓﺎ"); harf
  biçimleri standart harflere çevrilir (NFKC). "ﷺ", "﷽" gibi kelime bitişikleri korunur.
  Meali verilmediği için türü "arabi"dir. Bölüm başlarındaki Osmanlıca başlık ("ﻧﻄﻘﻠﺮ") atılır.
- Dipnotlar `<sup class="reference">` ile işaretlidir, metni bölümün sonundaki listededir;
  numaralar her bölümde baştan başlar. İşaret "[*[12]]", "[Haşiye[12]]" ya da baskının kendi
  numarasıyla "[2[12]]" biçimindedir. Metinde "[Haşiye]" diye işaretli ya da "(Müellif)" ile
  biten dipnot müellifin hâşiyesidir. Diğerleri nâşirin notudur (Misbah nüshasıyla farklar,
  kaynak bilgisi) ve `notes`'a gider. İşaretin ayraçları ("[*]", "(*)") metne girmez.
- "***" ayraçları ve sayfa başındaki nâşir girişi atılır. Birkaç kelimelik "Said…" ya da
  "Bediüzzaman" satırı imzadır.
"""

import re
import unicodedata
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

from risale_mcp.books.model import ARABIC_SCRIPT, ArabicSpan, Book, Node, Text, TextBuilder
from risale_mcp.catalog import Work
from risale_mcp.headings import local_id, parse_heading
from risale_mcp.sources import kastamonur as source

BLOCK_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "div"}
VOID_TAGS = {"br", "img", "input", "hr", "meta", "link"}
SECTIONS = {"nutuklar": "Nutuklar", "makaleler": "Makaleler Kısmı"}
# Harf biçimleri ve lam-elif bitişikleri; U+FDF0–FDFF kelime bitişikleri (ﷺ, ﷽) dışarıda.
_PRESENTATION = re.compile(r"[ﭐ-﷯ﹰ-ﻼ]+")
_ARTICLE = re.compile(r"(Nutuk|Makale)\s*[–-]\s*(\d+)")
# Nutkun/makalenin başındaki yayın bilgisi: "Volkan", "No: 83 – 11 Mart 1325", "Kürd Teavün ve Terakki Gazetesi…".
# Gazetenin adı tek başına satır olmalı ("İkdam Ceride-i Muteberesine!" mektubun hitabıdır, metindir).
_PUBLICATION = re.compile(r"\bGazete(si)?\b|\bSayı\b|\bNo:|\b1[23]\d\d\b|\b19\d\d\b|Bu makale|Âsâr-ı Bediiyye|"
                          r"^(Volkan|İkdam|Mizân|Serbestî|Sebil-ür Reşad)$")
_PUBLICATION_WORDS = 20
_MARK_BEFORE = re.compile(r"\s*(?:\(\*\)\s*)?\[\s*(\*+|Haşiye|\d+)\s*$")   # "[*", "[**", "[Haşiye", "[2" (baskının numarası)
_MARK_AFTER = re.compile(r"^\s*\]")
_AUTHOR = re.compile(r"\s*\(Müellif\)\s*$")
_SIGNATURE = re.compile(r"^(?:Molla |Bediüzzaman |)Said\b|^Bediüzzaman$")
_SEPARATOR = re.compile(r"[\s*]+")


def unpresent(text: str) -> str:
    """'ﻳَٓﺎ ﺍَﻳُّﻬَﺎ' -> 'يَٓا اَيُّهَا': Arapça sunum biçimlerini standart harflere çevirir."""
    return _PRESENTATION.sub(lambda m: unicodedata.normalize("NFKC", m[0]), text)


# ---------------------------------------------------------------- HTML -> bloklar

@dataclass
class Piece:
    text: str = ""
    bold: bool = False
    rtl: int | None = None       # içinde bulunduğu RTL öğesinin sırası: aynı öğenin parçaları birleşir
    ref: int | None = None       # dipnot işaretiyse dipnotun numarası
    ref_list: int = 0            # işaretin ait olduğu dipnot listesi (bölüm sırası)


@dataclass
class Block:
    tag: str
    align: str = ""
    note: int | None = None      # dipnot listesindeki <li id="cite_note-N">
    note_list: int = 0
    pieces: list[Piece] = field(default_factory=list)

    @property
    def plain(self) -> str:
        return re.sub(r"\s+", " ", "".join(p.text for p in self.pieces)).strip()

    @property
    def bold(self) -> bool:
        """Tamamı kalın mı? (dipnot işaretleri ve ayraçları sayılmaz)"""
        signs = [p for p in self.pieces if p.ref is None and p.text.strip(" []*()“”\"")]
        return bool(signs) and all(p.bold for p in signs)

    @property
    def arabic(self) -> bool:
        signs = [p for p in self.pieces if p.ref is None and p.text.strip()]
        return bool(signs) and all(p.rtl is not None or not re.search(r"\w", p.text) for p in signs)


class _Blocks(HTMLParser):
    """Eserin HTML'ini okuma sırasıyla bloklara ayırır; iç içe bloklarda metin en içtekine gider."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[Block] = []
        self._tags: list[str] = []
        self._open: list[tuple[int, Block]] = []    # (derinlik, blok)
        self._bold: list[int] = []                  # açık kalın öğelerin derinlikleri
        self._rtl: list[tuple[int, int]] = []       # (derinlik, RTL öğesinin sırası)
        self._rtl_count = 0
        self._sup: tuple[int, str] | None = None    # açık dipnot işareti: (derinlik, metni)
        self._lists = 0                             # kapanmış dipnot listesi sayısı

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag in VOID_TAGS:
            if tag == "br":
                self.handle_data(" ")
            return
        a = {k: v or "" for k, v in attrs}
        self._tags.append(tag)
        depth = len(self._tags)
        if tag in BLOCK_TAGS:
            align = re.search(r"text-align:\s*(\w+)", a.get("style", ""))
            note = re.fullmatch(r"cite_note-(\d+)", a.get("id", ""))
            self._open.append((depth, Block(tag, align[1] if align else "", int(note[1]) if note else None,
                                            self._lists)))
        if tag in ("strong", "b"):
            self._bold.append(depth)
        if a.get("dir") == "rtl":
            self._rtl_count += 1
            self._rtl.append((depth, self._rtl_count))
        if tag == "sup" and "reference" in a.get("class", ""):
            self._sup = (depth, "")

    def handle_endtag(self, tag: str) -> None:
        if tag not in self._tags:
            return
        while self._tags:                           # kapanmamış iç etiketler de burada kapanır
            depth = len(self._tags)
            closed = self._tags.pop()
            self._close(closed, depth)
            if closed == tag:
                break

    def _close(self, tag: str, depth: int) -> None:
        if self._sup and self._sup[0] == depth:
            number = re.sub(r"\D", "", self._sup[1])
            if number and self._open:
                self._open[-1][1].pieces.append(Piece(ref=int(number), ref_list=self._lists))
            self._sup = None
        if self._bold and self._bold[-1] == depth:
            self._bold.pop()
        if self._rtl and self._rtl[-1][0] == depth:
            self._rtl.pop()
        if self._open and self._open[-1][0] == depth:
            block = self._open.pop()[1]
            if block.plain:
                self.blocks.append(block)
        if tag == "ol":
            self._lists += 1

    def handle_data(self, data: str) -> None:
        if self._sup:
            self._sup = (self._sup[0], self._sup[1] + data)
        elif self._open:
            self._open[-1][1].pieces.append(
                Piece(unpresent(data), bool(self._bold), self._rtl[-1][1] if self._rtl else None))


def read_blocks(html: str) -> list[Block]:
    parser = _Blocks()
    parser.feed(html)
    parser.close()
    return parser.blocks


# ---------------------------------------------------------------- bloklar -> metin

@dataclass(frozen=True)
class Mark:
    """Metindeki dipnot işareti; `hasiye`: metinde "[Haşiye]" diye işaretli."""
    note: int
    note_list: int
    hasiye: bool


def _strip_marks(pieces: list[Piece]) -> list[Piece]:
    """Dipnot işaretlerinin ayraçlarını ("[*", "]", "(*)") metinden çıkarır; "[Haşiye" işareti
    `Piece.text`'e "Haşiye" olarak yazılır (`block_text` onu `Mark.hasiye` yapar)."""
    out = [Piece(p.text, p.bold, p.rtl, p.ref, p.ref_list) for p in pieces]
    for i, piece in enumerate(out):
        if piece.ref is None:
            continue
        before = next((p for p in reversed(out[:i]) if p.ref is None and p.text), None)
        if before and (m := _MARK_BEFORE.search(before.text)):
            before.text = before.text[:m.start()]
            piece.text = m[1]
        after = next((p for p in out[i + 1:] if p.ref is None and p.text), None)
        if after:
            after.text = _MARK_AFTER.sub("", after.text)
    return out


def block_text(pieces: list[Piece]) -> Text:
    builder = TextBuilder()
    for piece in _strip_marks(pieces):
        if piece.ref is not None:
            builder.mark_footnote(Mark(piece.ref, piece.ref_list, piece.text == "Haşiye"))
        elif piece.rtl is not None and ARABIC_SCRIPT.search(piece.text):
            builder.add(piece.text, ArabicSpan(0, 0, "arabi"), key=piece.rtl)
        else:
            builder.add(piece.text)
    return Text.from_builder(builder)


@dataclass
class Footnote:
    text: Text
    author: bool                  # "(Müellif)": müellifin hâşiyesi


def _footnote(block: Block) -> Footnote:
    pieces = [Piece(p.text, p.bold, p.rtl, p.ref, p.ref_list) for p in block.pieces]
    last = next((p for p in reversed(pieces) if p.text.strip()), None)
    author = bool(last and _AUTHOR.search(last.text))
    if author:
        last.text = _AUTHOR.sub("", last.text)
    return Footnote(block_text(pieces), author)


# ---------------------------------------------------------------- eser

def _section(blocks: list[Block], name: str) -> list[Block]:
    """Seçilen bölümün blokları (başlığı hariç); bir sonraki bölümün başlığına kadar."""
    starts: dict[str, int] = {}
    for i, b in enumerate(blocks):
        for title in SECTIONS.values():
            if b.tag != "li" and b.plain.startswith(title) and len(b.plain) < len(title) + 6:
                starts.setdefault(title, i)
    start = starts[SECTIONS[name]]
    later = [i for i in starts.values() if i > start]
    return blocks[start + 1:min(later, default=len(blocks))]


def _is_publication(block: Block) -> bool:
    return bool(_PUBLICATION.search(block.plain)) and len(block.plain.split()) <= _PUBLICATION_WORDS


def _article_head(blocks: list[Block], i: int) -> tuple[Block | None, list[Block], int]:
    """`h2`'nin ardından: (basılı ad, yayın satırları, metnin başladığı sıra)."""
    title, publication = None, []
    j = i + 1
    while j < len(blocks) and blocks[j].tag == "p":
        block = blocks[j]
        if title is None and block.bold:
            title = block
        elif _is_publication(block):
            publication.append(block)
        else:
            break
        j += 1
    return title, publication, j


class _Writer:
    """Blokları sırayla esere yazar; hâşiye ve nâşir notlarını dipnot listelerinden çözer."""

    def __init__(self, book: Book, footnotes: dict[tuple[int, int], Footnote]) -> None:
        self.book = book
        self.footnotes = footnotes

    def heading(self, parent: Node, title: Text, local: str, **fields) -> Node:
        node = self.book.add_node(parent, local, title.text, **fields)
        self._resolve(title, node, None)
        return node

    def paragraph(self, node: Node, block: Block) -> None:
        text = block_text(block.pieces)
        extra = {"center": True} if block.align == "center" else {}
        if text.is_arabic():
            kind = "arabic"
        elif len(text.text.split()) <= 5 and _SIGNATURE.search(text.text):
            kind, extra = "signature", {}
        else:
            kind = "paragraph"
        record = self.book.add_paragraph(node, kind, text, **extra)
        self._resolve(text, node, record["id"])

    def _resolve(self, text: Text, node: Node, paragraph_id: str | None) -> None:
        for mark in text.footnotes:
            note = self.footnotes.get((mark.content.note_list, mark.content.note))
            if note is None:
                self.book.notes.append({"node_id": node.id, "after": paragraph_id,
                                        "text": f"Dipnot {mark.content.note} sitede bulunamadı."})
            elif mark.content.hasiye or note.author:
                self.book.add_hasiye(paragraph_id or node.id, node, mark.offset, note.text)
            else:
                self.book.notes.append({"node_id": node.id, "after": paragraph_id, "text": note.text.text})


def parse_work(work: Work, root: Path) -> Book:
    book = Book(work.slug, work.title, {
        "group": str(work.group), "language": work.language,
        "source": {"site": str(work.source.site), "book": work.source.book, "sections": list(work.source.sections)},
    })
    blocks = read_blocks(source.article_html(source.read_page(work.source.book, root)))
    footnotes = {(b.note_list, b.note): _footnote(b) for b in blocks if b.tag == "li" and b.note is not None}
    writer = _Writer(book, footnotes)
    body = [b for b in _section(blocks, work.source.sections[0]) if b.tag != "li"]

    article: Node | None = None
    current: Node = book.root
    i = 0
    while i < len(body):
        block = body[i]
        if not _SEPARATOR.sub("", block.plain) or (block.arabic and block.bold and (block.tag == "h1" or block.align == "center")):
            i += 1                                  # "***" ayracı, Osmanlıca bölüm başlığı
            continue
        if block.tag == "h2" and (m := _ARTICLE.search(block.plain)):
            title, publication, i = _article_head(body, i)
            label = block_text(block.pieces)
            name = block_text(title.pieces) if title else label
            article = current = writer.heading(
                book.root, name, f"{m[1].lower()}-{int(m[2]):02d}", type=m[1], number=int(m[2]), heading="H2",
                subtitle=" · ".join(b.plain for b in publication), toc_title=label.text if title else None)
            continue
        if block.tag == "h3" and article is not None:
            title = block_text(block.pieces)
            info = parse_heading(title.text)
            current = writer.heading(article, title, local_id(info, title.text, top_level=False),
                                     type=info.type, number=info.number, heading="H3")
        elif article is None and block.tag == "p" and block.bold:
            title = block_text(block.pieces)          # ilk nutuktan önceki "İfade-i Meram"
            info = parse_heading(title.text)
            current = writer.heading(book.root, title, local_id(info, title.text, top_level=False), heading="inline")
        else:
            writer.paragraph(current, block)
        i += 1
    return book
