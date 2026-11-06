"""OpenITI metninden paragraf kurmak: müfessirlerin eserlerinin ortak yazıcısı (T3'ten; `books/beyzavi.py`,
`books/tefsir_openiti.py`).

Kaynağın satırları yazarın paragrafı değildir (Shamela biçim kalıntısı): paragraf yalnız cümle sonunda (. ؟ !,
ardından kapanış işaretleri olabilir) biter; öbür satırlar bir boşlukla eklenir, noktalamayla başlayan satır
boşluksuz. Her paragraf `printed` ve `page_breaks` taşır (`books/printed.py` cümlelere dağıtır).
"""

from dataclasses import dataclass, field

from risale_mcp import openiti
from risale_mcp.books.model import Book, Node, Text

ENDS = ".؟!"
CLOSERS = "»”\")]' "
LEADING_PUNCT = ".،:؛"


@dataclass
class Report:
    units: int = 0
    lines: int = 0                               # kaynağın metin satırları
    paragraphs: int = 0                          # birleştirilmiş paragraflar
    ayah_lines: int = 0
    pages: list[str] = field(default_factory=list)
    unknown_pages: int = 0


class Para:
    """Açık paragraf: satırlar birleştikçe sayfa sonları kaydırılır."""

    def __init__(self, line: openiti.Paragraph) -> None:
        self.text = line.text
        self.page, self.end_page = line.page, line.end_page
        self.breaks = [(at, str(page)) for at, page in line.breaks]

    def ends_sentence(self) -> bool:
        tail = self.text.rstrip(CLOSERS)
        return bool(tail) and tail[-1] in ENDS

    def add(self, line: openiti.Paragraph) -> None:
        sep = "" if line.text[:1] in LEADING_PUNCT else " "
        shift = len(self.text) + len(sep)
        self.text += sep + line.text
        self.breaks += [(shift + at, str(page)) for at, page in line.breaks]
        self.end_page = line.end_page or self.end_page

    def add_break(self, line: openiti.Paragraph) -> None:
        """Yalnız sayfa işaretinden oluşan satır: sayfa açık paragrafın şu anki sonunda biter."""
        self.breaks += [(len(self.text), str(page)) for _, page in line.breaks]


def printed_of(page: openiti.Page | None, end: openiti.Page | None) -> dict | None:
    if page is None:
        return None
    return {"volume": page.volume, "page": page.page, **({"end": str(end)} if end and end != page else {})}


class Writer:
    def __init__(self, book: Book, report: Report) -> None:
        self.book, self.report = book, report
        self.node: Node | None = None
        self.open: Para | None = None

    def flush(self) -> None:
        if self.open is not None:
            self._emit("paragraph", self.open)
            self.open = None

    def _emit(self, kind: str, para: Para, **extra) -> dict:
        printed = printed_of(para.page, para.end_page)
        if printed is None:
            self.report.unknown_pages += 1
        record = self.book.add_paragraph(self.node, kind, Text(para.text), **extra,
                                         **({"printed": printed} if printed else {}),
                                         **({"page_breaks": [list(b) for b in para.breaks]} if para.breaks else {}))
        self.report.paragraphs += 1
        return record

    def start(self, node: Node) -> None:
        self.flush()
        self.node = node

    def line(self, line: openiti.Paragraph, force_new: bool = False) -> None:
        if not line.text:
            if self.open is not None:
                self.open.add_break(line)
            return
        self.report.lines += 1
        if self.open is not None and not force_new and not self.open.ends_sentence():
            self.open.add(line)
            return
        self.flush()
        self.open = Para(line)

    def ayah(self, lines: list[openiti.Paragraph], verses: str | None, note: str | None = None) -> None:
        self.flush()
        para = Para(lines[0])
        for line in lines[1:]:
            para.add(line)
        self._emit("ayah", para, **({"verses": verses} if verses else {}), **({"note": note} if note else {}))
        self.report.ayah_lines += len(lines)
