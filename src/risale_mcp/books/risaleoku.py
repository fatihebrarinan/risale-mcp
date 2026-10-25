"""risaleoku.com -> eser modeli: Küçük Sözler, Hizbü'l-Kur'ân, Hizbü Envâri'l-Hakāik, el-Mesnevî el-Arabî.

Sayfanın metin bölgesi (`#okucerceve`) iki `<br>` ile paragraflara ayrılır.
- `<span class='arapca' data-content='meal'>`: Arapça parça ve meali.
- `ortali`, `barla`, `h1ortali`, `<center>`: ortalı satır (başlık adayı); `sagayasli`: imza.
- `<span class='hasiye'>{(Haşiye): …}</span>`: önceki paragrafın hâşiyesi.
- `<font style='background-color…'>`: sitenin "tefekkür" boyaması; anlamı yoktur, atılır.
- `* * *`: bölüm ayıracı, atılır.

Yapı:
- Okuyucu sayfasındaki fihrist ağacı (`#treemenu1`) varsa ondan gelir: her girdinin sayfası
  bellidir; düğüm o sayfada başlığıyla başlayan paragrafta (yoksa sayfanın ilk paragrafında) açılır.
- Ağaç boşsa (el-Mesnevî el-Arabî) ortalı başlıklardan çıkarılır: "الرسالة …" birinci,
  "الباب …", "ذيل …", "القطعة …", "المقدمة", "تقريظ" ikinci seviyedir; başlığın hemen
  ardından gelen en çok iki kısa ortalı satır alt başlıktır. İlk başlıktan önceki sayfalar
  tahkik edenin girişidir; esere alınmaz, `notes`'a yazılır.

Sayfa sonunda bölünen paragraf birleştirilir: sayfa noktalamasız biter ve sonraki sayfa düz
metinle sürerse. Tahkik dipnotlarının işaretleri ("(25)") metinden atılır; notların kendisi bu
kaynakta yoktur.
"""

import gzip
import re
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path

from risale_mcp.books.model import ArabicSpan, Book, Node, Text, TextBuilder
from risale_mcp.catalog import Work
from risale_mcp.headings import local_id, parse_heading
from risale_mcp.normalize import match_words

_PARAGRAPH_BREAK = re.compile(r"(?:<br\s*/?>\s*){2,}")
_SEPARATOR = re.compile(r"^[*∗\s]+$")
_FOOTNOTE_MARK = re.compile(r"\s?\((\d{1,3})\)")
_HASIYE = re.compile(r"^\{\s*\(Haşiye\)\s*:\s*(.*)\}$", re.S)
_TERMINAL = tuple(".!?؟…:»”)﴾﴿")
CENTERED = {"ortali", "barla", "h1ortali"}
ARABIC_TOP = re.compile(r"^(الرسالة|مقدمة المؤلف)")
ARABIC_SUB = re.compile(r"^(الباب|ذيل|القطعة|المقدمة|تقريظ|الخاتمة)")
SUBTITLE_LINES, SUBTITLE_WORDS = 2, 8


def page_region(page_html: str) -> str:
    """Sayfanın yalnızca metin bölgesi (okuyucu araçları ve gezinme menüsü hariç)."""
    start = page_html.find("</div>", page_html.find('<div id="dim-bottom"'))
    start = page_html.find("</div>", start + 6) + 6           # #crop-ui kapanışı
    end = page_html.find('<input type="hidden" id="baslangic"')
    return page_html[start:end]


@dataclass
class Block:
    text: Text
    page: int
    centered: bool = False
    signature: bool = False


class _BlockHTML(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.builder = TextBuilder()
        self.classes: set[str] = set()
        self._stack: list[dict] = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        a = {k: v or "" for k, v in attrs}
        if tag == "center":
            self.classes.add("center")
        if tag == "span":
            self.classes.update(a.get("class", "").split())
            self._stack.append(a)

    def handle_endtag(self, tag: str) -> None:
        if tag == "span" and self._stack:
            self._stack.pop()

    def handle_data(self, data: str) -> None:
        arabic = next((a for a in reversed(self._stack) if "arapca" in a.get("class", "").split()), None)
        if arabic is None:
            self.builder.add(data)
        else:
            self.builder.add(data, ArabicSpan(0, 0, "arabi", arabic.get("data-content") or None), key=id(arabic))


def page_blocks(page_html: str, page: int, strip_footnote_marks: bool) -> list[Block | str]:
    """Sayfanın paragrafları. Hâşiye, metni (str) olarak döner; önceki paragrafa bağlanır."""
    out: list[Block | str] = []
    for chunk in _PARAGRAPH_BREAK.split(page_region(page_html)):
        parser = _BlockHTML()
        parser.feed(chunk)
        text = Text.from_builder(parser.builder)
        if strip_footnote_marks and not text.arabic:
            text = Text(_FOOTNOTE_MARK.sub("", text.text).strip())
        if not text.text or _SEPARATOR.match(text.text):
            continue
        if "hasiye" in parser.classes and (m := _HASIYE.match(text.text)):
            out.append(m[1].strip())
            continue
        out.append(Block(text, page, centered=bool(parser.classes & (CENTERED | {"center"})),
                         signature="sagayasli" in parser.classes))
    return out


# ---------------------------------------------------------------- fihrist

@dataclass
class TocEntry:
    depth: int
    title: str
    page: int
    arabic_title: str = ""


class _TocHTML(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.entries: list[TocEntry] = []
        self._depth = 0
        self._href: str | None = None
        self._text = ""

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag == "ul":
            self._depth += 1
        elif tag == "a":
            self._href, self._text = dict(attrs).get("href", ""), ""

    def handle_endtag(self, tag: str) -> None:
        if tag == "ul":
            self._depth -= 1
        elif tag == "a" and self._href is not None:
            if m := re.search(r"/(\d+)$", self._href):
                turkish, _, arabic = " ".join(self._text.split()).partition("@")
                self.entries.append(TocEntry(self._depth, turkish.strip(), int(m[1]), arabic.strip()))
            self._href = None

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._text += data


def read_toc(index_html: str) -> list[TocEntry]:
    start = index_html.find('<ul id="treemenu1"')
    if start < 0:
        return []
    parser = _TocHTML()
    parser.feed(index_html[start:])
    entries = parser.entries
    # Ağacın kökü kitabın adıdır (sayfa = kitabın başı): eser düğümüdür, ayrı düğüm açmaz.
    if entries and entries[0].depth == 1 and all(e.depth > 1 for e in entries[1:]):
        entries = [TocEntry(e.depth - 1, e.title, e.page, e.arabic_title) for e in entries[1:]]
    return entries


# ---------------------------------------------------------------- eser

def _joins(previous: Block, block: Block) -> bool:
    """Sayfa sonunda bölünmüş paragraf mı?"""
    return (block.page == previous.page + 1 and not (block.centered or previous.centered or block.signature)
            and not previous.text.text.rstrip().endswith(_TERMINAL) and not block.text.is_arabic())


@dataclass
class _Heading:
    depth: int
    title: str
    subtitle: str = ""
    arabic_title: str = ""


def load_blocks(book: str, root: Path, first_page: int, strip_footnote_marks: bool) -> list[Block | str]:
    """Bütün sayfaların paragrafları, sayfa sonunda bölünenler birleştirilmiş olarak."""
    blocks: list[Block | str] = []
    for path in sorted((root / book / "pages").glob("*.html.gz")):
        page = int(path.name[:4])
        if page < first_page:
            continue
        for item in page_blocks(gzip.decompress(path.read_bytes()).decode("utf-8"), page, strip_footnote_marks):
            last = blocks[-1] if blocks else None
            if isinstance(item, Block) and isinstance(last, Block) and _joins(last, item):
                blocks[-1] = Block(Text.join([last.text, item.text], " "), item.page)
            else:
                blocks.append(item)
    return blocks


def _toc_starts(entries: list[TocEntry], blocks: list[Block | str]) -> dict[int, list[_Heading]]:
    starts: dict[int, list[_Heading]] = {}
    floor = 0
    for entry in entries:
        on_page = [i for i in range(floor, len(blocks)) if isinstance(blocks[i], Block) and blocks[i].page >= entry.page]
        if not on_page:
            continue
        candidates = [i for i in on_page if blocks[i].page == entry.page] or on_page[:1]
        heads = [match_words(t)[:3] for t in (entry.title, entry.arabic_title) if t]
        titled = [i for i in candidates if any(h and match_words(blocks[i].text.text)[:len(h)] == h for h in heads)]
        start = titled[0] if titled else candidates[0]
        starts.setdefault(start, []).append(_Heading(entry.depth, entry.title, arabic_title=entry.arabic_title))
        floor = start
    return starts


def _arabic_heading_starts(blocks: list[Block | str]) -> tuple[dict[int, list[_Heading]], set[int]]:
    """el-Mesnevî el-Arabî: ortalı "الرسالة …" ve alt başlıklar. (başlangıçlar, başlık olarak tüketilen bloklar)
    Başlığın hemen ardından gelen en çok iki kısa ortalı satır alt başlıktır ("الرسالة الثانية عشرة"
    + "الرسالة القيمة"); daha uzun ortalı satırlar (beyit, özlü söz) metne aittir."""
    starts: dict[int, list[_Heading]] = {}
    consumed: set[int] = set()
    current: _Heading | None = None
    subtitle_lines = 0
    for i, block in enumerate(blocks):
        if not isinstance(block, Block) or not block.centered:
            current = None
            continue
        title = block.text.text
        depth = 1 if ARABIC_TOP.match(title) else 2 if ARABIC_SUB.match(title) else 0
        short = len(title.split()) <= SUBTITLE_WORDS
        if current is not None and subtitle_lines < SUBTITLE_LINES and short and depth in (0, current.depth):
            current.subtitle = " ".join(filter(None, [current.subtitle, title]))
            subtitle_lines += 1
            consumed.add(i)
        elif depth:
            current, subtitle_lines = _Heading(depth, title), 0
            starts.setdefault(i, []).append(current)
            consumed.add(i)
        else:
            current = None
    return starts, consumed


def parse_work(work: Work, root: Path) -> Book:
    book = Book(work.slug, work.title, {
        "group": str(work.group), "language": work.language,
        "source": {"site": str(work.source.site), "book": work.source.book},
    })
    index_html = gzip.decompress((root / work.source.book / "index.html.gz").read_bytes()).decode("utf-8")
    first = int(m[1]) if (m := re.search(r'id="baslangic" value="(\d+)"', index_html)) else 1
    arabic_prose = work.language == "ar"
    blocks = load_blocks(work.source.book, root, first, strip_footnote_marks=arabic_prose)

    entries = read_toc(index_html)
    if entries:
        starts, consumed = _toc_starts(entries, blocks), set()
    else:
        starts, consumed = _arabic_heading_starts(blocks)

    stack: list[tuple[int, Node]] = [(0, book.root)]
    last: dict | None = None
    if not entries and starts:
        # Başlıklar metinden çıkarıldıysa ilk başlıktan önceki sayfalar tahkik edenin girişidir, eserin değil.
        first_heading = min(starts)
        skipped = sum(isinstance(b, Block) for b in blocks[:first_heading])
        book.notes.append({"node_id": book.root.id, "after": None,
                           "text": f"Tahkik edenin girişi ({skipped} paragraf) esere dahil edilmedi."})
        blocks = blocks[first_heading:]
        starts = {i - first_heading: v for i, v in starts.items()}
        consumed = {i - first_heading for i in consumed}
    for i, block in enumerate(blocks):
        heading_words = []
        for head in starts.get(i, []):
            while stack[-1][0] >= head.depth:
                stack.pop()
            info = parse_heading(head.title)
            slug_source = head.title if re.search(r"[A-Za-z]", head.title) else f"{len(stack[-1][1].children) + 1:03d}"
            node = book.add_node(stack[-1][1], local_id(info, slug_source, top_level=False), head.title,
                                 type=info.type, number=info.number, subtitle=head.subtitle)
            stack.append((head.depth, node))
            heading_words += [match_words(head.title), match_words(head.arabic_title)]
        if isinstance(block, str):                               # hâşiye: önceki paragrafa
            if last is not None:
                book.add_hasiye(last["id"], stack[-1][1], len(last["text"]), Text(block))
            continue
        if i in consumed or match_words(block.text.text) in heading_words:
            continue                                             # başlığın kendisi
        kind = "arabic" if block.text.is_arabic() else "signature" if block.signature else "paragraph"
        extra = {"center": True} if block.centered and kind == "paragraph" else {}
        last = book.add_paragraph(stack[-1][1], kind, block.text, **extra)
    return book
