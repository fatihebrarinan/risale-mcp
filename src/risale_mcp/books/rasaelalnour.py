"""rasaelalnour.com Word dosyaları -> eser modeli: İşârâtü'l-İ'câz'ın Arapça aslı (İhsan Kasım tahkiki).

Word dosyası basılı kitabın düz dökümüdür; biçim stili yoktur. Satırlar (`Row`) yalnızca hizasını
(ortalı, sağa/sola yaslı) ve kalınlığını taşır.

Sayfa düzeni:
- Her sayfa "إشارات الإعجاز - ص: 38" satırıyla başlar; bu satır atılır (sayfa bilgisi tutulmaz).
- Sayfanın dipnotları "_____" çizgisinden sonra gelir: "1 metin", devam satırları numarasızdır.
  Numaralar her sayfada 1'den başlar. Metindeki işaret ("كان 1", "الْكَوْثَرَ )4") sıradaki numaradır;
  işaret metinden silinir, yeri hâşiyenin konumudur.
- Sayfa sonunda bölünen paragraf (noktalamasız biten, sonraki sayfa düz metinle süren) birleştirilir.

Dipnotun kimin olduğu sonundaki işaretten anlaşılır:
- "(المؤلف)": müellifin hâşiyesi; eserin parçasıdır.
- "(ت: 13)": Türkçe tercümeden (Abdülmecid Nursî) aktarılan açıklama; not (`notes`), sayfa işareti atılır.
- İşaretsiz: muhakkikin (İhsan Kasım) notu (âyet kaynağı, lügat, biyografi); not.

Yapı (kullanıcının kararları):
- Muhakkikin ön sözleri ve sondaki eklemeler (talebelerin sözü, takriz, "قالوا عن القرآن") alınmaz;
  eser "مقدمة الترجمة التركية" satırıyla başlar, "باسمه سبحانه" (talebelerin sözü) ile biter.
- Müellifin Türkçe yazıp İhsan Kasım'ın Arapçaya çevirdiği ön kısım ("مقدمة الترجمة التركية":
  Tenbih ve üç Nükte) alınır ama alt başlıkta "İhsan Kasım es-Sâlihî'nin tercümesi" diye işaretlenir.
- Sûreler ve Bakara'nın âyet bölümleri Türkçe eserle aynı adı ve kimliği taşır ("Sûre-i Bakara",
  "2. Âyetin Tefsiri", `…/sure-i-bakara/2`); basılı âyet satırı alt başlıktır. Numara basılı satırdan gelir.
  Türkçe eserde aynı âyetleri kapsayan bölüm varsa kimliği ondan alınır (`23-24-ayetlerin-tefsiri-nubuvvet-
  hakkinda`); böylece iki dilin bölümleri kimlikleriyle eşlenir.
- Bakara'da bir bölüm "***" ayıracından sonraki ortalı âyet satırlarıyla açılır. Satırlar zaten açılmış
  âyetleri tekrar ediyorsa (17-20'de 19-20 yeniden) bölüm açmaz, ortalı paragraf olur.
- Fâtiha'nın bölümleri paragraf başındaki parantezli âyet parçasıyla açılır ("(الحَمْدُ)"); hangi
  parçanın bölüm olduğu ve kimliği Türkçe eserin bölümlerinden gelir (`FATIHA_SECTIONS`).
- Ortalı "مقدمة", "فصل …" satırları ve tek başına duran "المبحث الاول:" gibi etiketler alt bölüm açar.
"""

import html
import json
import re
import unicodedata
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

from risale_mcp.books.model import Book, Node, Text
from risale_mcp.catalog import Work

_PAGE_MARK = re.compile(r"^[^\d]{2,40}-\s*ص\s*:\s*\d+\s*$")
_SEPARATOR = re.compile(r"^_{5,}$")
_SECTION_BREAK = re.compile(r"^\*(\s*\*)*$")
_FOOTNOTE = re.compile(r"^\(?\s*(\d{1,2})\s*\)?\s*[-–]?\s*(?=\S)(.*)$")   # "1 metin", "(1) metin", "( 2)metin"
_AUTHOR_TAG = re.compile(r"\s*(?:[(（]\s*المؤلف\s*[)）]|[-–]\s*المؤلف)\s*\.?\s*$")   # "(المؤلف)" ya da "- المؤلف."
_TRANSLATION_TAG = re.compile(r"\s*\(\s*ت\s*:\s*[\d\s,،-]+\)\s*\.?\s*$")
_TERMINAL = tuple(".!?؟:»”\")…")
_TATWEEL = re.compile(r"ـ+")
_VERSE_NUMBER = re.compile(r"(?<![\d])(\d{1,3})(?![\d])")
NEXT_VERSES = 4                 # bölüm açan âyet satırı açılmış son âyetten en çok bu kadar ileride olur

START_LINE = "مقدمة الترجمة التركية"
END_LINE = "باسمه سبحانه"
TRANSLATED = "İhsan Kasım es-Sâlihî'nin tercümesi (aslı Türkçe)"
SUBSECTION = re.compile(r"^(مقدمة|فصل|خاتمة|تتمة|تذييل)")
SUBSECTION_WORDS = 6
SIGNATURES = ("سعيد النورسي", "سعيد النورسى", "سعيد")

ORDINALS = {"الاول": 1, "الأول": 1, "الاولى": 1, "الأولى": 1, "الثاني": 2, "الثانية": 2, "الثالث": 3,
            "الثالثة": 3, "الرابع": 4, "الرابعة": 4, "الخامس": 5, "الخامسة": 5, "السادس": 6, "السادسة": 6,
            "السابع": 7, "السابعة": 7, "الثامن": 8, "الثامنة": 8, "التاسع": 9, "التاسعة": 9, "العاشر": 10,
            "العاشرة": 10}
# Tek başına duran etiket ("المبحث الاول:") -> Türkçe eserdeki kimlik öneki.
LABEL_TYPES = {"المبحث": ("Mebhas", "mebhas"), "المسألة": ("Mes'ele", "mesele"), "النكتة": ("Nükte", "nukte"),
               "المأخذ": ("Me'haz", "mehaz"), "الوجه": ("Vecih", "vecih"), "النقطة": ("Nokta", "nokta")}
_LABEL = re.compile(r"^(" + "|".join(LABEL_TYPES) + r")\s+(\S+)\s*:?\s*$")

def _key(text: str) -> str:
    """Harekesiz, elif çeşitleri birleşmiş metin ("اِيَّاكَ نَعْبُدُ" -> "اياك نعبد"). Elif kalır: "الله" ≠ "لله"."""
    text = "".join(ch for ch in unicodedata.normalize("NFD", text) if not unicodedata.category(ch).startswith("M"))
    return re.sub(r"\s+", " ", re.sub(r"[ٱأإآ]", "ا", text.replace("ـ", ""))).strip()


# Fâtiha'nın bölümleri: paragraf başındaki parantezli parça -> Türkçe eserdeki kimlik.
FATIHA_SECTIONS = {
    _key(k): v for k, v in {
        "بسم الله": "bismillahi", "الرحمن الرحيم": "er-rahmanir-rahim", "الحمد": "el-hamdu", "لله": "lillahi",
        "رب": "rabbi", "العالمين": "el-alemin", "مالك يوم الدين": "maliki-yevmid-din",
        "اياك نعبد": "iyyake-nabudu", "واياك نستعين": "ve-iyyake-nestein", "اهدنا": "ihdina",
        "الصراط المستقيم": "es-siratal-mustekim", "صراط الذين انعمت عليهم": "siratallezine-enamte-aleyhim",
        "غير المغضوب عليهم": "gayril-magdubi-aleyhim", "ولا الضالين": "ve-led-dallin"}.items()}
_FATIHA_HEAD = re.compile(r"^(?:أمّا|أما|اما)?\s*\(([^()]{2,40})\)")


@dataclass
class Row:
    text: str
    align: str = "start"           # start | center | end
    bold: bool = False


@dataclass
class Line:
    """Sayfa satırı; dipnot işaretleri silinmiş, yerleri `marks`'ta (konum, dipnot metni)."""
    text: str
    align: str = "start"
    bold: bool = False
    verse: str | None = None       # Bakara'nın âyet satırı: "new" (bölüm açar) ya da "repeat"
    marks: list[tuple[int, str]] = field(default_factory=list)


@dataclass
class Report:
    pages: int = 0
    footnotes: int = 0
    unanchored: list[str] = field(default_factory=list)
    joined: int = 0


# ---------------------------------------------------------------- Word dosyası

def read_rows(path: Path) -> list[Row]:
    xml = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8")
    rows = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", xml, re.S):
        text = html.unescape("".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p))).strip()
        if not text:
            continue
        align = re.search(r'<w:jc w:val="(\w+)"', p)
        rows.append(Row(re.sub(r"\s+", " ", text), align[1] if align else "start",
                        bool(re.search(r"<w:b/>|<w:bCs/>", p))))
    return rows


# ---------------------------------------------------------------- sayfalar ve dipnotlar

def _plain(text: str) -> str:
    return _TATWEEL.sub("", re.sub(r"\s+", " ", text)).strip()


def _mark_verse_lines(rows: list[Row]) -> list[str | None]:
    """Bakara'nın âyet satırları; numaraları âyet numarasıdır, dipnot işareti değil.
    Ardışık ortalı satırlar (sayfa sonundaki dipnotlar ve sayfa satırı araya girebilir) bir bloktur:
    - "new": blok, açılmış son âyetten sonraki birkaç âyetin numarasını taşır; bölüm açar. Önünde "***"
      olabilir ya da yeni sayfanın başında olabilir. Numara blokun yalnızca son satırında olabilir
      ("…غِشَاوَةٌ / وَلَهُمْ عَذابٌ عَظِيمٌ 7") ya da eksik basılmış olabilir ("…مُصْلِحُونَ 1 / …12").
    - "repeat": "***"tan sonra açılmış âyetleri tekrar eden blok (17-20'de 19-20 yeniden)."""
    kinds: list[str | None] = [None] * len(rows)
    covered, after_break, in_bakara, in_notes = 0, False, False, False
    block: list[int] = []

    def close() -> None:
        nonlocal covered, block
        numbers = [int(n) for i in block for n in _VERSE_NUMBER.findall(rows[i].text)]
        ahead = [n for n in numbers if covered < n <= covered + NEXT_VERSES]
        kind = "new" if ahead else "repeat" if after_break else None
        for i in block:
            kinds[i] = kind
        if ahead:
            covered = max(ahead)
        block = []

    for i, row in enumerate(rows):
        if _PAGE_MARK.match(row.text):
            in_notes = False
            continue
        if _SEPARATOR.match(row.text):
            in_notes = True
        if in_notes:
            continue
        if "الزهراوين" in _key(row.text):      # sûrenin başlığı; numarası dipnot işaretidir
            in_bakara = True
            continue
        if in_bakara and row.align == "center" and not SUBSECTION.match(_plain(row.text)) \
                and not _SECTION_BREAK.match(row.text):
            block.append(i)
            continue
        if block:
            close()
        after_break = bool(_SECTION_BREAK.match(row.text))
    if block:
        close()
    return kinds


def pages(rows: list[Row], report: Report) -> list[list[Line]]:
    """Satırları sayfalara böler, dipnotları işaretlerine bağlar (işaret metinden silinir)."""
    verse = _mark_verse_lines(rows)
    out: list[list[Line]] = []
    body: list[Line] = []
    notes: list[list] = []          # [numara, metin]
    in_notes = False

    def close() -> None:
        if not in_notes:                       # çizgisiz sayfa: dipnotlar sonda "(1) …" diye sıralanır
            notes.extend(_trailing_notes(body))
        if body or notes:
            _anchor(body, notes, report)
            out.append(body)

    for row, is_verse in zip(rows, verse):
        if _PAGE_MARK.match(row.text):
            close()
            body, notes, in_notes = [], [], False
            report.pages += 1
            continue
        if _SEPARATOR.match(row.text):
            in_notes = True
            continue
        if in_notes:
            if m := _FOOTNOTE.match(row.text):
                notes.append([int(m[1]), m[2]])
            elif notes:
                notes[-1][1] += " " + row.text
            continue
        body.append(Line(row.text, row.align, row.bold, is_verse))
    close()
    return out


_PAREN_NOTE = re.compile(r"^\(\s*(\d{1,2})\s*\)\s*(.*)$")


def _trailing_notes(body: list[Line]) -> list[list]:
    """Çizgisiz sayfanın sonundaki dipnotlar: son "(1)" satırından itibaren numaralar 1, 2, 3… diye sürüyorsa
    (araya numarasız devam satırları girebilir) bunlar dipnottur; satırlar metinden çıkarılır."""
    for start in range(len(body) - 1, -1, -1):
        m = _PAREN_NOTE.match(body[start].text)
        if not (m and m[1] == "1" and body[start].align != "center"):
            continue
        notes, expected = [], 1
        for line in body[start:]:
            if (m := _PAREN_NOTE.match(line.text)) and int(m[1]) == expected:
                notes.append([expected, m[2]])
                expected += 1
            elif notes and not _PAREN_NOTE.match(line.text) and line.align != "center":
                notes[-1][1] += " " + line.text
            else:
                break
        else:
            del body[start:]
            return notes
    return []


def _anchor(body: list[Line], notes: list[list], report: Report) -> None:
    """Dipnotları sırasıyla metindeki numaralarına bağlar; bulunamayanı sayfanın son satırına koyar."""
    line_at, pos = 0, 0
    for number, text in notes:
        report.footnotes += 1
        pattern = re.compile(rf"\s?\(\s*{number}\s*\)|(?<=[^\d\s-])\s?{number}(?![\d])|(?<=\s){number}(?![\d.])")
        found = None
        for i in range(line_at, len(body)):
            if body[i].verse:
                continue
            m = pattern.search(body[i].text, pos if i == line_at else 0)
            if m and m.start() > 0:
                found = (i, m)
                break
        if found is None:
            report.unanchored.append(text[:60])
            if body:
                body[-1].marks.append((len(body[-1].text), text))
            continue
        i, m = found
        line = body[i]
        line.text = line.text[:m.start()] + line.text[m.end():]
        line.marks = [(o - (m.end() - m.start()) if o > m.start() else o, t) for o, t in line.marks]
        line.marks.append((m.start(), text))
        line_at, pos = i, m.start()


def join_pages(page_list: list[list[Line]], report: Report) -> list[Line]:
    """Sayfa sonunda bölünen paragrafı sonraki sayfanın ilk satırıyla birleştirir."""
    lines: list[Line] = []
    for page in page_list:
        for k, line in enumerate(page):
            prev = lines[-1] if lines else None
            if (k == 0 and prev is not None and prev.align == "start" and line.align == "start"
                    and not prev.text.rstrip().endswith(_TERMINAL) and not _is_heading(line.text)):
                shift = len(prev.text) + 1
                prev.text = f"{prev.text} {line.text}"
                prev.marks += [(o + shift, t) for o, t in line.marks]
                report.joined += 1
            else:
                lines.append(line)
    return lines


def _is_heading(text: str) -> bool:
    return bool(_LABEL.match(_plain(text)) or _FATIHA_HEAD.match(text))


# ---------------------------------------------------------------- yapı

def _number(word: str) -> int | None:
    return ORDINALS.get(word.rstrip(":").replace("أ", "ا").replace("إ", "ا")) or ORDINALS.get(word.rstrip(":"))


def turkish_sections(path: Path) -> dict[tuple[int, int], str]:
    """Türkçe İşaratü'l-İ'caz'ın Bakara bölümleri: (ilk âyet, son âyet) -> yerel kimlik."""
    if not path.exists():
        return {}
    out = {}
    for node in json.loads(path.read_text(encoding="utf-8"))["outline"]:
        if node["parent_id"] and node["parent_id"].endswith("/sure-i-bakara") and \
                (m := re.match(r"^(\d+)(?:[‑-](\d+))?\. Âyet", node["title"])):
            out[(int(m[1]), int(m[2] or m[1]))] = node["id"].rsplit("/", 1)[1]
    return out


def parse_rows(work: Work, rows: list[Row], section_ids: dict[tuple[int, int], str] | None = None
               ) -> tuple[Book, Report]:
    book = Book(work.slug, work.title, {
        "group": str(work.group), "language": work.language,
        "source": {"site": str(work.source.site), "book": work.source.book},
    })
    report = Report()
    plain = [_plain(r.text) for r in rows]
    start = next(i for i, t in enumerate(plain) if t == START_LINE)
    end = next(i for i, t in enumerate(plain) if i > start and t.startswith(END_LINE))
    book.notes.append({"node_id": book.root.id, "after": None,
                       "text": "Muhakkikin ön sözleri ve sondaki eklemeler (talebelerin sözü, takriz, "
                               "\"قالوا عن القرآن\") esere dahil edilmedi."})
    lines = join_pages(pages(rows[start:end], report), report)
    _Builder(book, section_ids or {}).run(lines)
    return book, report


class _Builder:
    def __init__(self, book: Book, section_ids: dict[tuple[int, int], str]) -> None:
        self.book = book
        self.section_ids = section_ids
        self.node: Node = book.root
        self.top: Node = book.root             # en üst bölüm (ön kısım, sûre)
        self.section: Node = book.root         # âyet bölümü (alt başlıkların ebeveyni)
        self.sura: str | None = None
        self.covered = 0                       # Bakara'da açılmış son âyet
        self.last: dict | None = None
        self.pending_verse: list[Line] = []

    def open(self, parent: Node, local: str, title: str, **fields) -> Node:
        self.node = self.book.add_node(parent, local, title, **fields)
        return self.node

    def run(self, lines: list[Line]) -> None:
        for line in lines:
            if line.verse and self.pending_verse and line.verse != self.pending_verse[-1].verse:
                self.flush_verse()
            if line.verse:
                self.pending_verse.append(line)
                continue
            self.flush_verse()
            self.line(line)
        self.flush_verse()

    def line(self, line: Line) -> None:
        text = _plain(line.text)
        root = self.book.root
        if text == START_LINE:
            self.top = self.section = self.open(root, "mukaddime-tercume", line.text, subtitle=TRANSLATED)
            return
        if text == "تنبيه" and self.top.id.endswith("mukaddime-tercume"):
            self.section = self.open(self.top, "tenbih", line.text)
            return
        if text == "افادة المرام":
            self.top = self.section = self.open(root, "ifadetul-meram", line.text)
            return
        if text == "لمعة من تعريف القرآن":
            self.top = self.section = self.open(root, "kuran-nedir-tarifi-nasildir", line.text)
            return
        if line.align == "center" and "بسم" in _key(text) and self.top.id.endswith("tarifi-nasildir"):
            self.sura = "fatiha"
            self.top = self.section = self.open(root, "sure-i-fatiha", "Sûre‑i Fâtiha")
        elif "الزهراوين" in _key(text):
            self.sura, self.covered = "bakara", 0
            besmele = self.last if self.last and self.last["node_id"] == self.node.id \
                and "بسم" in _key(self.last["text"]) and self.last.get("center") else None
            if besmele:                        # sûrenin Besmelesi başlığından önce basılmış
                self.book.paragraphs.remove(besmele)
                self.node.paragraph_count -= 1
            self.top = self.section = self.open(root, "sure-i-bakara", "Sûre‑i Bakara", subtitle=line.text)
            if besmele:
                self.last = self.book.add_paragraph(self.node, "paragraph", Text(besmele["text"]), center=True)
            self.hasiye(line, None)
            return
        if self.sura == "fatiha" and (m := _FATIHA_HEAD.match(line.text)):
            local = FATIHA_SECTIONS.get(_key(m[1]))
            if local:
                self.section = self.open(self.top, local, m[1].strip())
        if line.align == "center" and SUBSECTION.match(text) and len(text.split()) <= SUBSECTION_WORDS:
            local = "mukaddime" if text.startswith("مقدمة") else "fasil"
            self.open(self.section, local, text)
            self.hasiye(line, None)
            return
        if m := _LABEL.match(text):
            type_, prefix = LABEL_TYPES[m[1]]
            number = _number(m[2])
            if number:
                parent = self.node.parent if self.node.type == type_ else self.section
                self.open(parent, f"{prefix}-{number:02d}", line.text.rstrip(), type=type_, number=number)
                return
        self.paragraph(line)

    def flush_verse(self) -> None:
        """Bakara'da "***"tan sonraki ortalı âyet satırları: yeni âyet bölümü ya da tekrar edilen âyet."""
        if not self.pending_verse:
            return
        block, self.pending_verse = self.pending_verse, []
        if block[0].verse == "repeat":
            for line in block:                 # 17-20 içinde 19-20 yeniden: bölüm açmaz
                self.paragraph(line)
            return
        numbers = [int(n) for line in block for n in _VERSE_NUMBER.findall(line.text)]
        first = self.covered + 1               # âyetler sırayla işlenir; eksik basılmış numara da sayılır
        last = max([first] + [n for n in numbers if self.covered < n <= self.covered + NEXT_VERSES])
        title = f"{first}. Âyetin Tefsiri" if first == last else f"{first}‑{last}. Âyetlerin Tefsiri"
        local = self.section_ids.get((first, last)) or (str(first) if first == last else f"{first}-{last}-ayetlerin-tefsiri")
        printed = " ".join(_VERSE_NUMBER.sub("", line.text).strip() for line in block)
        self.section = self.open(self.top, local, title, subtitle=re.sub(r"\s+", " ", printed))
        self.covered = last
        for line in block:
            self.hasiye(line, None)

    def paragraph(self, line: Line) -> None:
        text = _plain(line.text)
        if line.align == "end" and text in SIGNATURES:
            kind, extra = "signature", {}
        else:
            kind, extra = "paragraph", ({"center": True} if line.align == "center" else {})
        self.last = self.book.add_paragraph(self.node, kind, Text(line.text), **extra)
        self.hasiye(line, self.last)

    def hasiye(self, line: Line, paragraph: dict | None) -> None:
        """Satırın dipnotları: müellifinki hâşiye, öbürleri not."""
        for offset, note in line.marks:
            if _AUTHOR_TAG.search(note):
                body = _AUTHOR_TAG.sub("", note)
                parent = paragraph["id"] if paragraph else self.node.id
                self.book.add_hasiye(parent, self.node, offset if paragraph else 0, Text(body))
            else:
                if _TRANSLATION_TAG.search(note):
                    note = "(Türkçe tercümeden) " + _TRANSLATION_TAG.sub("", note)
                self.book.notes.append({"node_id": self.node.id,
                                        "after": paragraph["id"] if paragraph else None, "text": note})


def parse_work(work: Work, docx_path: Path, turkish: Path | None = None) -> tuple[Book, Report]:
    """`turkish`: Türkçe eserin JSON'u; bölüm kimlikleri ondan alınır (yoksa kural)."""
    return parse_rows(work, read_rows(docx_path), turkish_sections(turkish) if turkish else {})
