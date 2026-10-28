"""Rumuzat-ı Semaniye: kullanıcının PDF'i (LibreOffice çıktısı) -> eser modeli.

PDF Yirmi Dokuzuncu Mektub'un üç kısmını taşır: Üçüncü Kısım (Dokuz Mes'ele), Dördüncü Kısım (üç Nükte; lafz-ı
Kur'ân ve lafz-ı Resul silsileleri ve tabloları) ve Rumuzat-ı Semaniye adıyla bilinen Sekizinci Kısım (Remizler).
erisale'nin Mektubat'ında bunlardan yalnız Üçüncü Kısım'ın Birinci Mes'elesi ve Dördüncü Kısım'ın Üçüncü Nüktesi
vardır; o paragraflar mecmua eşlemesiyle Mektubat'a bağlanır, kalanı bu eserde durur. Bölüm kimlikleri
Mektubat'ınkilerle aynıdır (`kisim-03/mesele-01`, `kisim-04/nukte-03/nukte-01`).

Satırlar `books/pdf_text.py`'den gelir (Arapça glif kimliklerinden çözülür). Kurallar:
- İlk sayfanın kapak satırları ("Risale-i Nur Külliyatından … Said Nursî") ve sayfa numaraları alınmaz.
- Başlık: kalın ve en az 14 punto satır (ya da köşeli ayraçla açılıp sonraki satırda kapanan iki satır).
  Kısım başlıkları kökün, "Sekizinci Kısmın … Remzi" Sekizinci Kısım'ın, "… Silsile: … Satırda" o andaki
  Nükte'nin, "Parça" o andaki Remz'in altına; öbürleri ("Mülahazat", "Mühim Bir İhtar") o andaki başlıklı
  bölümün altına girer.
- Paragraf başındaki numaralı etiket bölüm açar: köşeli ayraçlı ("[Birinci Silsile]", "[Lafzullah'ın Üçüncü
  Nüktesi]") ya da iki noktalı ("Birinci Mes'ele:"), türü `OPENING_TYPES`'ta ise. Etiket metinde kalır. Aynı
  türden açık bir bölüm (en yakın başlıklı bölümün içinde) varsa yeni bölüm onun kardeşidir, yoksa çocuğu.
  Sekizinci Kısım'ın "Birinci remiz altı remizdir" dediği alt remizler (`[Birinci Remiz]`…) kaynakta başlığı
  olmayan `remiz-01` ("Birinci Remiz", alt başlıkta işaretli) bölümünde toplanır.
- Paragraf: önceki satırdan en az 20 nokta içeride başlayan satır (ilk satır girintisi; girintili blokların
  satırları birbirinin hizasındadır) ya da kısa biten satırdan sonra küçük harfle başlamayan satır yeni
  paragraftır; tire ile biten satır ("Tevafukat-" / "ı lafzîye") boşluksuz birleşir. Cümlenin
  ortasına giren Arapça satırdan ("imam Busayrî'nin / قد ينكر المرء… / düsturuyla") sonra küçük harfle süren
  paragraf `continued` taşır. Arapça satırlar (Latin
  harfi yok) Arapça paragraftır; numarayla başlayan ("٢٥٥ …") ya da "*" ile biten satırdan sonra yenisi başlar.
- Hâşiye: metindeki küçük mavi "(Hâşiye)", "(Hâşiye-1)" işaretleri; hâşiyenin metni sol kenarda aynı etiketle
  başlayan satırdır (dipnot çizgisinden, kısa biten satırdan ya da boşluktan sonra; yoksa satır başına düşmüş
  işarettir) ve kısa biten satırda biter. Dipnot çizgileri ("_____") atılır. İşaretler sırayla, etiketiyle eşleşir; işaret metinden silinir.
- Tablolar (çizgili hücreler) `table` paragrafıdır: satırlar "\n", hücreler " | " ile. Sayfa sonunda bölünen
  tablo (aynı sütun sayısı, arada metin yok) tek tablodur.
- Arapçanın türü (âyet/hadis) PDF'te işaretli değildir: `arabi`.
- Ana ciltlere (çoğu Mektubat ve Barla Lâhikası) yalnızca düz paragraflar eşlenir (`MAPPED_KINDS`): âyet
  listelerinin maddeleri ("٢٥٥ …") bu eserin kendi metnidir, başka bir yerde alıntılanan âyete bağlanmaz.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path

from risale_mcp.books.model import ArabicSpan, Book, Node, Text, TextBuilder
from risale_mcp.books.pdf_text import PdfLine, PdfTable, read_blocks
from risale_mcp.books.pdf_text import Report as PdfReport
from risale_mcp.catalog import Work
from risale_mcp.headings import HeadingInfo, canonical_type, local_id, parse_heading
from risale_mcp.normalize import fold, parse_ordinal, slugify

MAPPED_KINDS = frozenset({"paragraph"})
OPENING_TYPES = {"Mes'ele", "Nükte", "Silsile", "Remiz", "Parça", "Kısım", "Letafet", "Misal", "Esas", "Makam"}
OUR_TITLE = "Bu başlık kaynakta yoktur; Sekizinci Kısım'ın alt remizlerini toplamak için konuldu."
TITLE_PAGE = ("Kapak satırları (\"Risale-i Nur Külliyatından Rumuzat-ı Semaniye Mecmuası, Müellifi Bediüzzaman "
              "Said Nursî\") ve sayfa numaraları alınmadı. Kaynak kullanıcının PDF'idir; âyet ve hadislerin türü "
              "PDF'te işaretli olmadığından Arapça parçalar `arabi` türündedir.")
_START = "Üçüncü Risale Olan Üçüncü Kısım"
_INDENT = 85
_SHORT = 480                               # bundan önce biten satır paragrafı bitirebilir
_MARK = re.compile(r" ?\((Hâşiye(?:-\d+)?)\)")
_LABEL = re.compile(r"^\[\s*([^\]]+?)\s*\]|^([^:\[\]]{3,40}):")
_ARABIC_NUMBER = re.compile(r"^[٠-٩]+\s")


@dataclass
class Report:
    pdf: PdfReport = field(default_factory=PdfReport)
    hasiye: int = 0
    unmatched_marks: list[str] = field(default_factory=list)   # metni bulunamayan hâşiye işaretleri
    unmatched_texts: list[str] = field(default_factory=list)   # işareti bulunamayan hâşiye metinleri
    tables: int = 0


# ---------------------------------------------------------------- satırlardan paragraflar

@dataclass
class Para:
    """Kurulmakta olan paragraf: satırlar ve türü."""
    lines: list[PdfLine]
    hasiye: str | None = None                 # hâşiye metniyse etiketi ("Hâşiye-1")
    heading: bool = False
    continued: bool = False                   # araya giren Arapça satırdan sonra süren cümle

    @property
    def rtl(self) -> bool:
        return all(line.rtl for line in self.lines)


def _is_heading(line: PdfLine) -> bool:
    bracketed = line.text.startswith("[") and line.text.endswith("]")
    return line.bold and (line.size >= 14 or bracketed) and not line.rtl


def _short(line: PdfLine) -> bool:
    return line.x1 < _SHORT


def _starts_lower(line: PdfLine) -> bool:
    return line.text[:1].islower()


def paragraphs(blocks: list[PdfLine | PdfTable]) -> list[Para | PdfTable]:
    """Satırları paragraflara, başlıklara, hâşiye metinlerine ve tablolara toplar (belge sırasıyla)."""
    out: list[Para | PdfTable] = []
    main: Para | None = None                   # sürmekte olan ana metin paragrafı
    note: Para | None = None                   # sürmekte olan hâşiye metni
    started = separator = False
    previous: PdfLine | None = None
    for block in blocks:
        if isinstance(block, PdfTable):
            prev = out[-1] if out else None
            if isinstance(prev, PdfTable) and prev.page + 1 == block.page \
                    and len(prev.rows[0]) == max(len(r) for r in block.rows):
                prev.rows += block.rows                     # sayfa sonunda bölünen tablo
            else:
                out.append(block)
            main = note = None
            continue
        line = block
        if not started:
            started = line.text == _START
            if not started:
                continue
        if line.y < 60 and re.fullmatch(r"\d+", line.text):
            continue                                        # sayfa numarası
        if _is_heading(line):
            prev = out[-1] if out else None
            if isinstance(prev, Para) and prev.heading and prev.lines[-1].text.startswith("[") \
                    and "]" not in prev.lines[-1].text:
                prev.lines.append(line)                     # iki satıra bölünmüş başlık
            else:
                out.append(Para([line], heading=True))
            main = note = None
            continue
        if re.fullmatch(r"_+", line.text):
            separator = True                                # dipnot çizgisi
            continue
        # Satır başındaki "(Hâşiye)" ya hâşiye metninin etiketidir (çizgiden, kısa biten satırdan ya da boşluktan
        # sonra) ya da satırın başına düşmüş işaret ("(Hâşiye) gâyet manidar…").
        m = re.match(r"\((Hâşiye(?:-\d+)?)\)", line.text) if line.x0 < _INDENT else None
        if m and not (separator or previous is None or _short(previous) or line.page != previous.page
                      or line.y - previous.y > 20):
            m = None
        separator, previous = False, line
        if m:
            line.text = line.text[m.end():].lstrip()
            line.arabic = [(s - (len(m[0]) + 1), e - (len(m[0]) + 1)) for s, e in line.arabic]
            note = Para([line], hasiye=m[1])
            out.append(note)
            if _short(line):
                note = None
            continue
        if note is not None:
            note.lines.append(line)
            if _short(line):
                note = None
            continue
        if main is not None and _continues(main, line):
            main.lines.append(line)
        else:
            continued = main is not None and main.rtl and not line.rtl and _starts_lower(line)
            main = Para([line], continued=continued)
            out.append(main)
    return out


def _continues(para: Para, line: PdfLine) -> bool:
    last = para.lines[-1]
    if para.rtl != line.rtl:
        return False
    if line.rtl:
        return not _ARABIC_NUMBER.match(line.text) and not last.text.endswith("*")
    if line.x0 - last.x0 >= 20:
        return False                                        # ilk satır girintisi (girintili blokta da)
    return not _short(last) or _starts_lower(line)


def _text(lines: list[PdfLine]) -> Text:
    """Satırları tek metne çevirir: Arapça parçalar `arabi`, art arda gelenler birleşir."""
    builder = TextBuilder()
    for i, line in enumerate(lines):
        if i:
            prev = lines[i - 1].text
            if not (prev.endswith("-") and line.text[:1].islower()):
                builder.add(" ")
        pos = 0
        for start, end in line.arabic:
            builder.add(line.text[pos:start])
            builder.add(line.text[start:end], ArabicSpan(0, 0, "arabi"), key="pdf")
            pos = end
        builder.add(line.text[pos:])
    return Text.from_builder(builder)


# ---------------------------------------------------------------- başlık ağacı

_LOCAL_TYPES = {"silsile": "Silsile", "letafet": "Letafet"}     # headings.KNOWN_TYPES'ta yok (orada eklemek
                                                                # öbür eserlerin bölümlerini değiştirirdi)


def _type(word: str) -> str | None:
    word = word.split("-")[0]
    if found := canonical_type(word):
        return found
    folded = fold(word)
    return next((t for stem, t in _LOCAL_TYPES.items() if folded in (stem, stem + "si", stem + "in")), None)


def label_info(label: str, strict: bool) -> HeadingInfo | None:
    """Etiketin türü ve numarası: "Birinci Mes'ele", "Dördüncü Silsile-i", "Lafzullah'ın Üçüncü Nüktesi",
    "Sekizinci Kısmın Üçüncü Remzi". `strict`: iki noktalı etiket, sıra sayısı ve türden ibaret olmalı."""
    words = re.findall(r"[^\W\d_]+(?:['’][^\W\d_]+)*(?:-[^\W\d_]+)?", label)
    if not strict and len(words) >= 3 and (t := _type(words[-1])) and (n := parse_ordinal(words[-2])):
        return HeadingInfo(t, n)                 # "Sekizinci Kısmın Üçüncü Remzi": tür sondadır
    for used in (2, 1):
        if len(words) > used and (n := parse_ordinal("".join(words[:used]))) and (t := _type(words[used])):
            rest = words[used + 1:]
            if not rest or not strict and len(rest[0]) <= 2:
                return HeadingInfo(t, n)
            return None if strict else HeadingInfo(t, n)
    if not strict and len(words) >= 2 and (t := _type(words[-1])) and (n := parse_ordinal(words[-2])):
        return HeadingInfo(t, n)
    return None


class Tree:
    def __init__(self, book: Book) -> None:
        self.book = book
        self.node = book.root            # metnin girdiği düğüm
        self.info: dict[str, HeadingInfo] = {}
        self.inline: set[str] = set()

    def add(self, parent: Node, local: str, title: str, info: HeadingInfo | None = None, **fields) -> Node:
        info = info or HeadingInfo()
        node = self.book.add_node(parent, local, title, type=info.type, number=info.number, **fields)
        self.info[node.id] = info
        if fields.get("heading") == "inline":
            self.inline.add(node.id)
        self.node = node
        return node

    def ancestor(self, type_: str, inline_only: bool = False) -> Node | None:
        node = self.node
        while node is not None:
            if self.info.get(node.id, HeadingInfo()).type == type_ and (not inline_only or node.id in self.inline):
                return node
            node = node.parent
        return None

    def kisim(self, number: int) -> Node:
        return next(c for c in self.book.root.children if c.id.endswith(f"/kisim-{number:02d}"))

    def heading(self, title: str) -> None:
        """Bağımsız başlık satırı."""
        bare = title.strip("[]() ").strip()
        info = parse_heading(bare)
        if info.type is None and (found := label_info(bare, strict=False)):
            info = found                                        # "Birinci Silsile: Birinci Satırda"
        if info.type == "Kısım":
            self.add(self.book.root, f"kisim-{info.number:02d}", bare, info)
        elif info.type == "Remiz":
            self.add(self.kisim(8), f"remiz-{info.number:02d}", bare, info)
        elif info.type == "Parça" or fold(bare).startswith(fold("Üçüncü Parça")):
            info = info if info.type else HeadingInfo("Parça", 3)
            self.add(self.ancestor("Remiz"), f"parca-{info.number:02d}", bare, info)
        elif info.type == "Silsile":
            self.add(self.ancestor("Nükte"), f"silsile-{info.number:02d}", bare, info)
        elif "tetimme" in fold(bare):
            self.add(self.ancestor("Nükte"), "tetimme", bare)
        elif info.type == "Nükte":
            self.add(self.kisim(4), f"nukte-{info.number:02d}", bare, info)
        elif "zeyl" in fold(bare):
            self.add(self.kisim(8).children[0], "zeyl", bare, HeadingInfo("Zeyl"))
        else:
            # "Mülahazat", "Mühim Bir İhtar": numaralı bir etiketin bölümündeyse onun kardeşi, aynı başlığın
            # tekrarıysa (ikinci "Mülahazat") onun kardeşi, değilse o anki bölümün çocuğu.
            parent = self.node
            if parent.id in self.inline or parent.id.rsplit("/", 1)[1].split("-")[0] == slugify(bare):
                parent = parent.parent
            self.add(parent, slugify(bare), bare)

    def label(self, text: str) -> None:
        """Paragraf başındaki numaralı etiket bölüm açar: "[Birinci Silsile] …", "Birinci Mes'ele: …"."""
        m = _LABEL.match(text)
        if not m:
            return
        label = m[1] or m[2]
        info = label_info(label, strict=not m[1])
        if info is None or info.type not in OPENING_TYPES:
            return
        sibling = self.ancestor(info.type, inline_only=True)
        if sibling is not None:
            parent = sibling.parent
        elif info.type == "Remiz" and self.ancestor("Remiz") is None:
            # Sekizinci Kısım'ın birinci remzinin alt remizleri: kaynakta başlığı olmayan remiz-01'de toplanır.
            parent = self.add(self.kisim(8), "remiz-01", "Birinci Remiz", HeadingInfo("Remiz", 1), subtitle=OUR_TITLE)
        else:
            parent = self.node
        self.add(parent, local_id(info, label, False), label.rstrip(":").strip(), info, heading="inline")


# ---------------------------------------------------------------- eser

def parse(work: Work, pdf: Path) -> tuple[Book, Report]:
    report = Report()
    book = Book(work.slug, work.title, {
        "group": str(work.group), "language": work.language,
        "source": {"site": str(work.source.site), "book": work.source.book},
    })
    book.notes.append({"node_id": book.root.id, "after": None, "text": TITLE_PAGE})
    tree = Tree(book)
    marks: list[Mark] = []                                    # metindeki işaretler, belge sırasıyla
    texts: list[Mark] = []                                    # hâşiye metinleri
    last: dict | None = None                                  # son ana metin paragrafı
    previous_heading = False
    for item in paragraphs(read_blocks(pdf, report.pdf)):
        if isinstance(item, PdfTable):
            previous_heading = False
            rows = [Text(" | ".join(_trim(row))) for row in item.rows]
            book.add_paragraph(tree.node, "table", Text.join(rows, "\n"))
            report.tables += 1
            continue
        if item.heading:
            title = " ".join(line.text for line in item.lines)
            if previous_heading and not title.startswith("["):
                tree.node.subtitle = title                  # "Kenzül Arş duasının feyzinden gelen…"
            else:
                tree.heading(title)
            previous_heading = True
            continue
        text = _text(item.lines)
        if previous_heading and re.fullmatch(r"\[[^\]]+\]", text.text) and not tree.node.subtitle:
            tree.node.subtitle = text.text.strip("[]")      # "[Latif ve Yüksek ve Şüphesiz bir Tevafuk]"
            previous_heading = False
            continue
        previous_heading = False
        page = item.lines[0].page
        where = (page, item.lines[0].y)
        if item.hasiye:
            texts.append(Mark(item.hasiye, where, last, len(last["text"]) if last else 0, text))
            continue
        tree.label(text.text)
        text, found = _strip_marks(text)
        kind = "arabic" if text.is_arabic() else "paragraph"
        extra = {"center": True} if item.rtl and all(l.x0 > 100 for l in item.lines) else {}
        if item.continued:
            extra["continued"] = True
        record = last = book.add_paragraph(tree.node, kind, text, **extra)
        positions = [(line.page, line.y) for line in item.lines for _ in _MARK.finditer(line.text)]
        marks += [Mark(label, where, record, offset) for (label, offset), where in zip(found, positions)]
    _attach_hasiye(book, marks, texts, report)
    return book, report


@dataclass
class Mark:
    """Hâşiye işareti (metindeki konumu) ya da hâşiye metni (`text`; `record`/`offset` önündeki paragrafın sonu)."""
    label: str
    where: tuple[int, float]      # sayfa ve satırın yüksekliği
    record: dict | None
    offset: int
    text: Text | None = None


def _attach_hasiye(book: Book, marks: list[Mark], texts: list[Mark], report: Report) -> None:
    """Her hâşiye metni, aynı etiketli, kullanılmamış, kendinden önceki en yakın işarete bağlanır (en çok iki
    sayfa geriye). İşareti PDF'te bulunmayan metin önündeki paragrafın sonuna bağlanır ve raporlanır."""
    used: set[int] = set()
    nodes = {node.id: node for node in book.nodes()}
    for text in texts:
        candidates = [i for i, m in enumerate(marks) if m.label == text.label and i not in used
                      and m.where < text.where and text.where[0] - m.where[0] <= 2]
        if candidates:
            mark = marks[candidates[-1]]
            used.add(candidates[-1])
        else:
            report.unmatched_texts.append(f"{text.label} {text.text.text[:40]}")
            mark = text
        if mark.record is None:
            continue
        book.add_hasiye(mark.record["id"], nodes[mark.record["node_id"]], mark.offset, text.text)
        report.hasiye += 1
    report.unmatched_marks = [f"{m.label} {m.record['id']}" for i, m in enumerate(marks) if i not in used]
    # hâşiye bağlı olduğu paragrafın hemen ardından gelir
    children: dict[str, list[dict]] = {}
    for p in book.paragraphs:
        if p["kind"] == "hasiye":
            children.setdefault(p["parent_id"], []).append(p)
    ordered = []
    for p in book.paragraphs:
        if p["kind"] != "hasiye":
            ordered += [p, *sorted(children.get(p["id"], []), key=lambda h: h["offset"])]
    book.paragraphs[:] = ordered


def _trim(row: list[str]) -> list[str]:
    while row and not row[-1]:
        row = row[:-1]
    return row


def _strip_marks(text: Text) -> tuple[Text, list[tuple[str, int]]]:
    """Hâşiye işaretlerini metinden siler: (yeni metin, [(etiket, konum)])."""
    found, out, removed = [], text.text, 0
    spans = [ArabicSpan(a.start, a.end, a.kind, a.meal, a.source) for a in text.arabic]
    for m in list(_MARK.finditer(text.text)):
        start = m.start() - removed
        out = out[:start] + out[start + len(m[0]):]
        found.append((m[1], start))
        for span in spans:
            if span.start >= start + len(m[0]):
                span.start -= len(m[0])
            if span.end >= start + len(m[0]):
                span.end -= len(m[0])
        removed += len(m[0])
    return Text(out, spans), found
