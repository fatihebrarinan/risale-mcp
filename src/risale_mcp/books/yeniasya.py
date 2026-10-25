"""Yeni Asya "Eski Saîd Dönemi Eserleri" cildi -> Makâlât ve Nutuk. Son çare kaynak.

Sayfa çevirmeli kitabın `basic-html` katmanında her satır konumu ve yazı tipiyle ayrı durur.
- Gövde: `font1` satırları; tek sayfada solda (x≈48), çift sayfada sağda (x≈170) bir sütun.
  Paragraf, sütunun 12 px içerisinden başlayan satırla ya da süslü baş harfle açılır.
- Atılır: lügat ve editör notları (`font7`), sayfa üst/alt bilgisi, tahkik dipnotu işaretleri ("(2)").
- Müellifin hâşiyesi `font10` ("HaşİYe: …"); metindeki işareti `(HaşİYe)`.
- Arapça özel bir yazı tipiyle kodlanmış ve okunamaz; yerine "[Arapça]" yazılır ve not düşülür.
- Başlıklar içindekiler listesinden (`toc.html`, sayfa numaralı, düz liste) gelir. Bir eser,
  kendi adı ile ardından gelen "Bu Esere Ait Takdim" girdisinden başlar (yayıncının takdimi alınmaz)
  ve bir sonraki eserin adına kadar sürer. "Birinci Madde" gibi numaralı seriler önceki numarasız
  başlığın altına girer. Makalenin tarihi (`font28`) ve gazetesi (`font29`) alt başlıktır.

Onarımlar (yazı tipi kusurları):
- Satır sonu tiresi kaldırılır ("kav-" + "miyeyi").
- Gövde yazı tipi D, E, G, K, L, N, O, Ö, P, R, S, T, Ü, Z büyük harflerini küçük basar; bu harfler
  cümle başında büyütülür ("alınız. pencerenin" -> "alınız. Pencerenin"). Cümle içindeki özel
  isimler ("kürd") düzeltilemez.
- Etiket yazı tiplerindeki karışık harf ve aralıklı harfler ("BirinCi CinaYET", "i r i n c i s i :")
  düzene sokulur.
"""

import gzip
import html as html_lib
import re
from dataclasses import dataclass, field
from pathlib import Path

from risale_mcp.books.model import Book, Node, Text
from risale_mcp.catalog import Work
from risale_mcp.headings import local_id, parse_heading
from risale_mcp.normalize import fold, match_words, parse_ordinal, tr_capitalize, tr_lower
from risale_mcp.sources.yeniasya import ENCODING

_LINE = re.compile(r'style="top : (\d+)px; left : (\d+)px; width : (\d+)px; height : (\d+)px;[^"]*">\s*'
                   r'<span class="(font\d+) fontPosition"[^>]*>(.*?)</span>', re.S)
BODY = "font1"
SMALL_CAPS = "font11"                     # paragrafın ilk kelimesi: "üRkÇe"
HASIYE = "font10"
DATE, SOURCE = "font28", "font29"
SKIPPED = {"font7", "font5", "font6", "font21", "font24", "font27", "font2", "font40"}   # font8: işaretler
LOST_CAPITALS = set("degklnoöprstüz")
LABEL_WORDS = 4                           # bundan uzun satırlar etiket değil, başka yazı tipindeki gövde metnidir
WORK_TITLE = "font25"                     # cildin içindeki eserin büyük başlığı ("Nutuk", "Münazarat")
_TURKISH = re.compile(r"[A-Za-zÇĞİÖŞÜçğıöşüÂÎÛâîûàìùÀ0-9\s.,;:!?'’‘“”\"()\[\]\-–—…/*]")
_SENTENCE_START = re.compile(r"(^|[.!?…]\s+|^[“\"(]|[.!?…]\s+[“\"(])([a-zçğıöşü])")
TAKDIM = fold("Bu Esere Ait Takdim")


@dataclass
class Line:
    top: int
    left: int
    width: int
    height: int
    font: str
    text: str

    @property
    def readable(self) -> bool:
        """Türkçe harflerle yazılmış mı (değilse okunamayan Arapça yazı tipidir)?"""
        letters = [c for c in self.text if not c.isspace()]
        return bool(letters) and sum(bool(_TURKISH.match(c)) for c in letters) / len(letters) >= 0.8


def page_lines(page_html: str) -> list[Line]:
    out = []
    for m in _LINE.finditer(page_html):
        text = html_lib.unescape(re.sub(r"<[^>]+>", "", m[6])).strip()
        if text:
            out.append(Line(int(m[1]), int(m[2]), int(m[3]), int(m[4]), m[5], text))
    return out


def clean_label(text: str) -> str:
    """Etiket yazı tiplerinin bozukluğu: 'BirinCi CinaYET' -> 'Birinci Cinayet', 'i r i n c i s i :' -> 'irincisi:'."""
    tokens = text.split()
    if len(tokens) >= 3 and sum(len(t) == 1 for t in tokens) / len(tokens) >= 0.6:   # aralıklı harfler
        text = "".join(tokens)
    return " ".join(tr_capitalize(tr_lower(w)) if w.isalpha() or w[:-1].isalpha() else w for w in text.split())


def repair_capitals(text: str) -> str:
    """Kayıp büyük harfleri cümle başında geri koyar."""
    def fix(m: re.Match) -> str:
        letter = m[2]
        return m[1] + (tr_capitalize(letter) if letter in LOST_CAPITALS else letter)
    return _SENTENCE_START.sub(fix, text)


@dataclass
class Paragraph:
    parts: list[str] = field(default_factory=list)
    hasiyeler: list[str] = field(default_factory=list)
    hasiye_marks: int = 0
    arabic_missing: bool = False
    continued: bool = False          # önceki sayfadaki paragrafın devamı

    def add(self, piece: str) -> None:
        if self.parts and self.parts[-1].endswith("-") and piece[:1].islower():
            self.parts[-1] = self.parts[-1][:-1] + piece          # satır sonu tiresi
        elif self.parts and self.parts[-1].endswith(("“", "(", "[")):
            self.parts[-1] += piece
        else:
            self.parts.append(piece)

    def extend(self, other: "Paragraph") -> None:
        for piece in other.parts:
            self.add(piece)
        self.hasiyeler += other.hasiyeler
        self.arabic_missing = self.arabic_missing or other.arabic_missing

    @property
    def text(self) -> str:
        return repair_capitals(re.sub(r"\s+", " ", " ".join(self.parts)).strip())


@dataclass
class Heading:
    entry: "TocEntry"
    subtitle: str


def _hasiye_texts(lines: list[Line]) -> list[str]:
    texts: list[list[str]] = []
    for ln in sorted((ln for ln in lines if ln.font == HASIYE), key=lambda x: (x.top, x.left)):
        if re.match(r"(?i)haşiye\s*:", ln.text):
            texts.append([re.sub(r"(?i)^haşiye\s*:\s*", "", ln.text)])
        elif texts:
            texts[-1].append(ln.text)
    return [repair_capitals(re.sub(r"-\s+(?=[a-zçğıöşü])", "", " ".join(t))) for t in texts]


def _rows(lines: list[Line], column: int, width: int) -> list[list[Line]]:
    """Gövde sütunundaki satırlar (lügat sütunu, alt bilgi, hâşiye hariç), okuma sırasıyla."""
    in_column = sorted((ln for ln in lines if column - 30 <= ln.left <= column + width and ln.top < 610
                        and ln.font not in SKIPPED | {DATE, SOURCE, HASIYE}), key=lambda x: (x.top, x.left))
    rows: list[list[Line]] = []
    for ln in in_column:
        if rows and abs(rows[-1][0].top - ln.top) <= 6:
            rows[-1].append(ln)
        else:
            rows.append([ln])
    return [sorted(row, key=lambda x: x.left) for row in rows]


def _piece(ln: Line, para: Paragraph) -> str | None:
    """Satır parçasının metni; hâşiye işareti ya da okunamayan Arapça için None."""
    if ln.font == BODY:
        return ln.text
    if re.fullmatch(r"\(\d+\)", ln.text):
        return None                                                # tahkik dipnotu işareti
    if ln.font in (SMALL_CAPS, "font9", "font96", "font42"):
        return tr_lower(ln.text)                                   # küçük büyük harf, (asm)
    if "haşiye" in tr_lower(ln.text):
        para.hasiye_marks += 1
        return None
    if ln.readable:
        return clean_label(ln.text) if len(ln.text.split()) <= LABEL_WORDS else ln.text
    if not (para.parts and para.parts[-1] == "[Arapça]"):
        para.parts.append("[Arapça]")
    para.arabic_missing = True
    return None


def _attach_article_info(lines: list[Line], heading_tops: list[tuple[int, Heading]]) -> None:
    """Makalenin tarihi ve gazetesi, dikey olarak en yakın başlığın alt başlığı olur."""
    if not heading_tops:
        return
    for ln in sorted((ln for ln in lines if ln.font in (DATE, SOURCE)), key=lambda x: (x.top, x.left)):
        _, heading = min(heading_tops, key=lambda th: abs(th[0] - ln.top))
        heading.subtitle = re.sub(r"-\s+(?=[a-zçğıöşü])", "", " · ".join(filter(None, [heading.subtitle, ln.text])))


def read_page(lines: list[Line], heads: list["TocEntry"]) -> list[Paragraph | Heading]:
    """Sayfanın okuma sırasıyla başlıkları ve paragrafları; hâşiyeler işaretli paragraflara dağıtılır."""
    body = [ln for ln in lines if ln.font == BODY]
    column = min((ln.left for ln in body), default=48)
    width = max((ln.left + ln.width for ln in body), default=column + 264) - column
    pending = list(heads)
    items: list[Paragraph | Heading] = []
    heading_tops: list[tuple[int, Heading]] = []
    for row in _rows(lines, column, width):
        words = match_words(" ".join(x.text for x in row))
        head = next((h for h in pending if match_words(h.title)[:4] == words[:len(match_words(h.title)[:4])]), None)
        if head is not None:
            pending.remove(head)
            items.append(Heading(head, ""))
            heading_tops.append((row[0].top, items[-1]))
            continue
        first = row[0]
        drop_cap = first.font != BODY and len(first.text) == 1 and first.text.isupper() and first.height >= 18
        indented = first.font == BODY and first.left >= column + 8
        if drop_cap or indented or not items or isinstance(items[-1], Heading):
            items.append(Paragraph(continued=not items and not (drop_cap or indented)))
        para = items[-1]
        cap = ""
        for ln in row:
            if ln is first and drop_cap:
                cap = ln.text
                continue
            piece = _piece(ln, para)
            if piece is not None:
                para.add(cap + piece)
                cap = ""
    # Sayfada satırı bulunamayan başlıklar (ör. sayfanın en üstündeki numaralı başlık) sayfanın başında açılır.
    unplaced = [Heading(h, "") for h in pending]
    items = unplaced + items
    heading_tops += [(0, h) for h in unplaced]
    _attach_article_info(lines, heading_tops)
    hasiyeler = _hasiye_texts(lines)
    for para in (i for i in items if isinstance(i, Paragraph)):
        para.hasiyeler, hasiyeler = hasiyeler[:para.hasiye_marks], hasiyeler[para.hasiye_marks:]
    if hasiyeler and any(isinstance(i, Paragraph) for i in items):
        [i for i in items if isinstance(i, Paragraph)][-1].hasiyeler += hasiyeler
    return [i for i in items if isinstance(i, Heading) or i.parts]


# ---------------------------------------------------------------- içindekiler

@dataclass
class TocEntry:
    title: str
    page: int


def read_toc(toc_html: str) -> list[TocEntry]:
    entries = []
    for href, label in re.findall(r'<a[^>]*href="page(\d+)\.html"[^>]*>(.*?)</a>', toc_html, re.S):
        title = " ".join(html_lib.unescape(re.sub(r"<[^>]+>", "", label)).split())
        if title and not title.isdigit():
            entries.append(TocEntry(title, int(href)))
    return entries


def work_entries(entries: list[TocEntry], name: str, title_pages: set[int]) -> tuple[list[TocEntry], int]:
    """Eserin içindekiler girdileri (takdim hariç) ve eserin bittiği sayfa. Bir girdi, ardından
    "Bu Esere Ait Takdim" geliyorsa ya da sayfasında büyük eser başlığı (`font25`) varsa eser başlığıdır."""
    starts = [i for i in range(len(entries)) if (i + 1 < len(entries) and fold(entries[i + 1].title) == TAKDIM)
              or (entries[i].page in title_pages and fold(entries[i].title) != TAKDIM)]
    own = next(i for i in starts if fold(entries[i].title).startswith(fold(name)))
    end_index = next((i for i in starts if i > own and entries[i].page > entries[own].page), len(entries))
    end_page = entries[end_index].page if end_index < len(entries) else 10_000
    first = own + 2 if own + 1 < len(entries) and fold(entries[own + 1].title) == TAKDIM else own + 1
    return entries[first:end_index], end_page


def parse_work(work: Work, root: Path) -> Book:
    book = Book(work.slug, work.title, {
        "group": str(work.group), "language": work.language,
        "source": {"site": str(work.source.site), "book": work.source.book, "sections": list(work.source.sections)},
    })
    book_dir = root / work.source.book
    toc = read_toc(gzip.decompress((book_dir / "toc.html.gz").read_bytes()).decode(ENCODING))
    title_pages = {e.page for e in toc if any(ln.font == WORK_TITLE for ln in page_lines(
        gzip.decompress((book_dir / "pages" / f"{e.page:04d}.html.gz").read_bytes()).decode(ENCODING)))}
    entries, end_page = work_entries(toc, work.source.sections[0], title_pages)
    by_page: dict[int, list[TocEntry]] = {}
    for e in entries:
        by_page.setdefault(e.page, []).append(e)

    # 1) Sayfaları okuma sırasıyla başlık ve paragraf akışına çevir; sayfa sonunda bölüneni birleştir.
    stream: list[Paragraph | Heading] = []
    for page in range(entries[0].page if entries else end_page, end_page):
        lines = page_lines(gzip.decompress((book_dir / "pages" / f"{page:04d}.html.gz").read_bytes()).decode(ENCODING))
        for item in read_page(lines, by_page.get(page, [])):
            if isinstance(item, Paragraph) and item.continued and stream and isinstance(stream[-1], Paragraph):
                stream[-1].extend(item)
            else:
                stream.append(item)

    # 2) Akıştan eser: numaralı seriler ("Birinci Madde") önceki numarasız başlığın altına girer.
    top: Node = book.root
    current: Node = book.root
    for item in stream:
        if isinstance(item, Heading):
            info = parse_heading(item.entry.title)
            numbered = info.number is not None or parse_ordinal(item.entry.title.split()[0]) is not None
            current = book.add_node(top if numbered else book.root, local_id(info, item.entry.title, top_level=False),
                                    item.entry.title, type=info.type, number=info.number,
                                    subtitle="" if numbered else item.subtitle)
            if not numbered:
                top = current
            continue
        record = book.add_paragraph(current, "paragraph", Text(item.text))
        for hasiye in item.hasiyeler:
            book.add_hasiye(record["id"], current, len(record["text"]), Text(hasiye))
        if item.arabic_missing:
            book.notes.append({"node_id": current.id, "after": record["id"],
                               "text": "Bu paragraftaki Arapça kaynakta okunamıyor; yerine [Arapça] yazıldı."})
    return book
