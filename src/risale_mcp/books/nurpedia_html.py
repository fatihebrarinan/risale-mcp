"""nurpedia.org'un MediaWiki sayfalarını sıralı bloklara çevirir (Rumuzat-ı Semaniye, `books/nurpedia.py`).

Sayfanın gövdesi `mw-parser-output`tur. Atılanlar: üstteki eser listesi (`hf-nsheader`), "Önceki/Sonraki Risale"
gezinti satırı (bağlantılı tek `<p><i>`), içindekiler, düzenleme bağlantıları, dipnot listesinin "↑" işaretleri.
Bloklar:

- `Heading(level, text)`: `<h1>`…`<h6>`;
- `Block(kind, text)`: `<p>` ve her `<li>` (madde) ayrı blok; `<br>` satır sonudur;
- `Image(src)`: gövdedeki resim (Rumuzat'ta tablolar resimdir);
- dipnotlar: metindeki `<sup class="reference">` işareti (`Block.notes`: metindeki konum ve not kimliği) ve
  sayfa sonundaki `<li id="cite_note-…">` metni (`Page.notes`).

Arapça: `dir="rtl"` taşıyan her öğe ve metnin içinde işaretsiz geçen Arapça harf dizisi Arapça parçadır.
"""

import re
from dataclasses import dataclass, field
from html import unescape
from html.parser import HTMLParser

from risale_mcp.books.model import ARABIC_SCRIPT

# Arapça harf dizisi: Arapça harfler, aralarındaki boşluk ve noktalama (bir sonraki Arapça harfe kadar)
ARABIC_RUN = re.compile(r"[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-ﻼ]"
                        r"(?:[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-ﻼ\s.,:;!؟?()«»\"'﴾﴿۝\d٠-٩-]*"
                        r"[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-ﻼ﴾﴿])?")
_SKIP_CLASSES = ("hf-nsheader", "mw-editsection", "toc", "printfooter", "mw-cite-backlink", "catlinks")


@dataclass
class Run:
    text: str
    rtl: bool = False


@dataclass
class Block:
    kind: str                                   # "p" | "li"
    runs: list[Run] = field(default_factory=list)
    notes: list[tuple[int, str]] = field(default_factory=list)   # (run sırası, not kimliği): işaret bu run'dan sonra

    @property
    def text(self) -> str:
        return re.sub(r"\s+", " ", "".join(r.text for r in self.runs)).strip()


@dataclass
class Heading:
    level: int
    text: str


@dataclass
class Image:
    src: str


@dataclass
class Page:
    title: str
    revision: int | None
    blocks: list = field(default_factory=list)
    notes: dict[str, Block] = field(default_factory=dict)        # not kimliği -> metni


class _Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.page_blocks: list = []
        self.notes: dict[str, Block] = {}
        self.inside = 0                 # mw-parser-output içinde mi (derinlik)
        self.depth = 0
        self.skip_until: int | None = None
        self.rtl_until: list[int] = []
        self.block: Block | None = None
        self.heading: tuple[int, list[str], int] | None = None
        self.note_id: str | None = None
        self.note_depth: int | None = None
        self.ref_depth: int | None = None
        self.nav_p = False

    # --- yardımcılar
    def _open_block(self, kind: str) -> None:
        self.block = Block(kind)

    def _close_block(self) -> None:
        if self.block is None:
            return
        if self.note_id is not None:
            target = self.notes.setdefault(self.note_id, Block("note"))
            target.runs += self.block.runs
            target.notes += self.block.notes
        elif self.block.text:
            self.page_blocks.append(self.block)
        self.block = None

    def handle_starttag(self, tag: str, attrs) -> None:
        attrs = dict(attrs)
        if tag in ("br", "img", "meta", "hr", "link", "input", "wbr"):   # boş öğeler derinliği değiştirmez
            if self.inside and self.skip_until is None:
                if tag == "br" and self.block is not None:
                    self.block.runs.append(Run("\n"))
                elif tag == "img" and "mw-file-element" in attrs.get("class", ""):
                    self._close_block()
                    self.page_blocks.append(Image(attrs.get("src", "")))
            return
        self.depth += 1
        cls = attrs.get("class", "") or ""
        if not self.inside:
            if "mw-parser-output" in cls:
                self.inside = self.depth
            return
        if self.skip_until is not None:
            return
        if any(c in cls.split() for c in _SKIP_CLASSES) or tag in ("style", "script"):
            self.skip_until = self.depth
            return
        if tag == "sup" and "reference" in cls:
            self.ref_depth = self.depth
            return
        if self.ref_depth is not None:
            if tag == "a" and attrs.get("href", "").startswith("#cite_note-") and self.block is not None:
                self.block.notes.append((len(self.block.runs), attrs["href"][1:]))
            return
        if tag == "li" and attrs.get("id", "").startswith("cite_note-"):
            self._close_block()
            self.note_id, self.note_depth = attrs["id"], self.depth
            self._open_block("note")
            return
        if attrs.get("dir") == "rtl":
            self.rtl_until.append(self.depth)
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._close_block()
            self.heading = (int(tag[1]), [], self.depth)
        elif tag == "p":
            self._close_block()
            self._open_block("p")
        elif tag == "li" and self.note_id is None:
            self._close_block()
            self._open_block("li")
        elif tag == "p" or (tag == "div" and self.note_id is not None and self.block is None):
            self._open_block("note")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("br", "img", "meta", "hr", "link", "input", "wbr"):
            return
        depth = self.depth
        self.depth -= 1
        if not self.inside:
            return
        if depth == self.inside:
            self._close_block()
            self.inside = 0
            return
        if self.skip_until is not None:
            if depth == self.skip_until:
                self.skip_until = None
            return
        if self.ref_depth is not None:
            if depth == self.ref_depth:
                self.ref_depth = None
            return
        if self.rtl_until and depth == self.rtl_until[-1]:
            self.rtl_until.pop()
        if self.heading and depth == self.heading[2]:
            level, parts, _ = self.heading
            text = re.sub(r"\s+", " ", "".join(parts)).strip()
            if text:
                self.page_blocks.append(Heading(level, text))
            self.heading = None
        elif tag in ("p", "li") and self.block is not None and self.note_id is None:
            self._close_block()
        elif self.note_id is not None and depth == self.note_depth:
            self._close_block()
            self.note_id = self.note_depth = None
        elif self.note_id is not None and tag == "p":
            if self.block is not None:
                self.block.runs.append(Run("\n"))

    def handle_data(self, data: str) -> None:
        if not self.inside or self.skip_until is not None or self.ref_depth is not None:
            return
        if self.heading is not None:
            self.heading[1].append(data)
            return
        if self.block is None:
            if not data.strip():
                return
            self._open_block("note" if self.note_id is not None else "p")
        self.block.runs.append(Run(data, rtl=bool(self.rtl_until)))


def parse_page(html: str, title: str) -> Page:
    match = re.search(r'"wgRevisionId":(\d+)', html)
    parser = _Parser()
    parser.feed(html)
    parser.close()
    blocks = parser.page_blocks
    # Gezinti satırı: "Rumuzat-ı Semaniye → 29. Mektubun 4. Kısmı: Sonraki Risale"
    blocks = [b for b in blocks if not (isinstance(b, Block) and re.search(r"(Sonraki|Önceki) Risale", b.text))]
    for note in parser.notes.values():
        note.runs = [Run(unescape(r.text.lstrip("↑")) if i == 0 else r.text, r.rtl) for i, r in enumerate(note.runs)]
    return Page(title, int(match[1]) if match else None, blocks, parser.notes)


def arabic_pieces(run: Run) -> list[tuple[str, bool]]:
    """Run'ı Arapça ve Arapça olmayan parçalara böler (rtl run'ın tamamı Arapçadır)."""
    if run.rtl and ARABIC_SCRIPT.search(run.text):
        return [(run.text, True)]
    out, last = [], 0
    for m in ARABIC_RUN.finditer(run.text):
        if m.start() > last:
            out.append((run.text[last:m.start()], False))
        out.append((m.group(), True))
        last = m.end()
    if last < len(run.text):
        out.append((run.text[last:], False))
    return out
