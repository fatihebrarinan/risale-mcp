"""risale.online (Hayrat baskısı) -> eser modeli.

Bu sitedeki eserler (Zülfikâr, Tılsımlar, Sirâcü'n-Nûr, Gençlik ve Hanımlar Rehberi) mecmuadır;
metinleri sonra ana ciltlere eşlenir (`books/mecmua.py`). Bu yüzden ayrıştırıcının asıl işi
yapıyı ve eşlemeye yetecek temiz metni çıkarmaktır.

- Yapı sitenin fihristinden gelir (`fihrist.json`, iç içe `alt_basliklar`). Her girdinin sayfası
  bellidir; düğüm, o sayfada başlığıyla başlayan ilk paragrafta açılır (bulunamazsa sayfanın
  ilk paragrafında). Başlığın kendisi olan paragraf metne girmez.
- Paragraf metni HTML'deki kelime gruplarından kurulur. Arapça parçalar (`Arabi*` sınıfı) meal
  ve kaynağıyla (`data-mehaz-*`) işaretlenir; hâşiye işareti (`data-hasiye-no`) konumuyla,
  hâşiye metni (`<aside>`) ayrı kayıt olarak gelir.
- Ortalı paragraf `center`, sağa yaslı kısa paragraf imzadır.
- Yalnızca bir sayıdan oluşan paragraf, Hayrat baskısının şiirlerde kıtalara verdiği sıra
  numarasıdır ("1", "2"…); ana ciltlerde yoktur, metne girmez.
"""

import re
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path

from risale_mcp.books.model import ArabicSpan, Book, Node, Text, TextBuilder
from risale_mcp.catalog import Work
from risale_mcp.headings import local_id, parse_heading
from risale_mcp.normalize import match_words
from risale_mcp.sources import risale_online as source

_ALIGN = re.compile(r"hizalama-([\w-]*)")
_STANZA_NUMBER = re.compile(r"\d{1,3}")


def arabic_kind(source_label: str) -> str:
    """'(Sûre-i Bakara, 2:255)' -> ayet; '(Hadîs-i Şerîf’den)' -> hadis; '(Fârisî ibâre)' -> farsi."""
    if "Sûre" in source_label:
        return "ayet"
    if "Hadîs" in source_label or "Hadis" in source_label:
        return "hadis"
    if "Fârisî" in source_label or "Farisi" in source_label:
        return "farsi"
    return "arabi"


class _ParagraphHTML(HTMLParser):
    """Bir paragrafın HTML'i: ana metin ve hâşiyeler (numara -> metin)."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.main = TextBuilder()
        self.hasiyeler: dict[str, TextBuilder] = {}
        self.align = ""
        self._target = self.main
        self._stack: list[tuple[str, dict]] = []    # açık span'ler: (rol, özellikler)

    def handle_starttag(self, tag: str, attrs: list) -> None:
        a = {k: v or "" for k, v in attrs}
        if tag == "p" and (m := _ALIGN.search(a.get("class", ""))):
            self.align = m[1]
        if tag == "aside":
            self._target = self.hasiyeler.setdefault(a.get("data-hasiye-no", str(len(self.hasiyeler) + 1)), TextBuilder())
            self._stack.append(("aside-label", {}))       # hâşiyenin ilk kelimesi "Hâşiye" etiketidir
            return
        if tag != "span":
            return
        if "data-hasiye-no" in a and self._target is self.main:
            self.main.mark_footnote(a["data-hasiye-no"])
            self._stack.append(("skip", a))
        elif "Arabi" in a.get("class", "") or "data-mehaz-id" in a:      # meal ve kaynağı olan her parça Arapçadır
            self._stack.append(("arabic", a))
        else:
            self._stack.append(("text", a))

    def handle_endtag(self, tag: str) -> None:
        if tag == "aside":
            self._target = self.main
            self._stack = [s for s in self._stack if s[0] != "aside-label"]
        elif tag == "span" and self._stack:
            self._stack.pop()

    def handle_data(self, data: str) -> None:
        roles = [role for role, _ in self._stack]
        if "skip" in roles:
            return
        if roles and roles[0] == "aside-label" and data.strip() == "Hâşiye" and self._target.is_empty():
            return
        arabic = next((a for role, a in reversed(self._stack) if role == "arabic"), None)
        if arabic is None:
            self._target.add(data)
            return
        label = arabic.get("data-mehaz-latince-kaynak", "")
        span = ArabicSpan(0, 0, arabic_kind(label), arabic.get("data-mehaz-latince-meal") or None, label.strip("() ") or None)
        self._target.add(data, span, key=arabic.get("data-mehaz-id") or id(arabic))


@dataclass
class _Entry:
    depth: int
    title: str
    subtitle: str
    page: int


def _entries(items: list[dict], depth: int = 1) -> list[_Entry]:
    out = []
    for item in items:
        title = (item.get("latince_baslik") or item.get("latince_metin") or "").strip()
        subtitle = (item.get("latince_metin") or "").strip() if item.get("latince_baslik") else ""
        out.append(_Entry(depth, title, subtitle, int(item["sayfa"])))
        out += _entries(item.get("alt_basliklar") or [], depth + 1)
    return out


def _sira(paragraph: dict) -> int:
    m = re.search(r'data-sira="(\d+)"', paragraph["latince_html"])
    return int(m[1]) if m else 0


def _starts(entries: list[_Entry], paragraphs: list[dict]) -> dict[int, list[_Entry]]:
    """Her fihrist girdisinin açıldığı paragraf sırası."""
    starts: dict[int, list[_Entry]] = {}
    floor = 0
    for entry in entries:
        head = match_words(entry.title)[:3]
        on_page = [i for i in range(floor, len(paragraphs)) if int(paragraphs[i]["sayfa"]) == entry.page]
        if not on_page:
            on_page = [i for i in range(floor, len(paragraphs)) if int(paragraphs[i]["sayfa"]) > entry.page][:1]
        if not on_page:
            continue
        titled = [i for i in on_page if match_words(re.sub(r"<[^>]+>", " ", paragraphs[i]["latince_html"]))[:len(head)] == head]
        start = titled[0] if titled else on_page[0]
        starts.setdefault(start, []).append(entry)
        floor = start
    return starts


def parse_work(work: Work, root: Path) -> Book:
    book = Book(work.slug, work.title, {
        "group": str(work.group),
        "source": {"site": str(work.source.site), "book": work.source.book},
    })
    paragraphs = sorted(source.load_paragraphs(work.source.book, root), key=lambda p: (int(p["sayfa"]), _sira(p)))
    fihrist = source.read_fihrist(work.source.book, root)
    starts = _starts(_entries(fihrist), paragraphs)

    stack: list[tuple[int, Node]] = [(0, book.root)]
    for i, raw in enumerate(paragraphs):
        heading_titles = []
        for entry in starts.get(i, []):
            while stack[-1][0] >= entry.depth:
                stack.pop()
            parent = stack[-1][1]
            info = parse_heading(entry.title)
            node = book.add_node(parent, local_id(info, entry.title, top_level=False), entry.title,
                                 type=info.type, number=info.number, subtitle=entry.subtitle)
            stack.append((entry.depth, node))
            heading_titles.append(match_words(entry.title))

        parsed = _ParagraphHTML()
        parsed.feed(raw["latince_html"])
        text = Text.from_builder(parsed.main)
        if not text.text or match_words(text.text) in heading_titles:
            continue                                # başlığın kendisi: düğüm başlığında duruyor
        if _STANZA_NUMBER.fullmatch(text.text):
            continue                                # kıta numarası
        node = stack[-1][1]
        extra = {}
        kind = "paragraph"
        if text.is_arabic():
            kind = "arabic"
        elif parsed.align == "sag" and len(text.text.split()) <= 8:
            kind = "signature"
        elif parsed.align == "ortali":
            extra["center"] = True
        record = book.add_paragraph(node, kind, text, **extra)
        hasiye_texts = {no: Text.from_builder(b) for no, b in parsed.hasiyeler.items()}
        for mark in text.footnotes:
            body = hasiye_texts.pop(str(mark.content), None)
            if body and body.text:
                book.add_hasiye(record["id"], node, mark.offset, body)
        for body in hasiye_texts.values():          # işareti bulunamayan hâşiye: paragrafın sonuna
            if body.text:
                book.add_hasiye(record["id"], node, len(text.text), body)
    return book
