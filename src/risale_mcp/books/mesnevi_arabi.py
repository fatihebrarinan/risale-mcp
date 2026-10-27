"""el-Mesnevî el-Arabî en-Nûrî: Abdülkadir Badıllı'nın "el-Kâmil" baskısı (rasaelalnour.com Word dosyası).

Kullanıcının kararıyla Arapça Mesnevî bu baskıdandır: tamamen harekelidir, müellifin hâşiyeleri işaretlidir,
Lem'alar ve Reşhalar Türkçe Mesnevî-i Nuriye'nin numaralarıyla bölünmüştür.

Word dosyasının özellikleri:
- Dipnotlar gerçek Word dipnotudur (`word/footnotes.xml`); metindeki işaret "()" içindedir, ikisi de silinir.
  Dipnotun sonunda "ـ المؤلف ـ" ya da "(المؤلف)" varsa müellifin hâşiyesidir; öbürleri (nüsha farkları,
  "ـ الناشر ـ" notları, tercüme açıklamaları) naşirin notudur.
- Âyetlerin bir kısmı Kur'ân Kompleksi'nin sayfa yazı tipleriyle yazılmıştır ("QCF_P286": mushafın 286.
  sayfası; her karakter o sayfadaki bir kelimenin glifi). Glifler `sources/qurancom` verisiyle âyetin adresine
  ve Osmanî harekeli metnine çevrilir; parça âyet olarak işaretlenir (kaynağı glifin kendisi). Âyet numarası
  glifi ("end") metne yazılmaz.
- "******" ayıraçları atılır; sayfa satırı yoktur.

Yapı Türkçe eserle paraleldir: risaleler ve bölümler Türkçe eserin kimliklerini taşır (`lemalar/lema-04`,
`katre/bab-01`), başlıklar Arapça basılı hâlleridir. Badıllı'nın ön sözü ve sondaki fihrist alınmaz.
Müellifin Türkçe yazdığı Mukaddime'nin Arapçası tercümedir; alt başlıkta işaretlenir.
"""

import html
import re
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

from risale_mcp.books.model import ArabicSpan, Book, Node, Text
from risale_mcp.books.rasaelalnour import ORDINALS, _key
from risale_mcp.catalog import Work
from risale_mcp.quran import SURA_NAMES
from risale_mcp.sources import qurancom

_QCF = re.compile(r'w:(?:ascii|hAnsi|cs)="QCF_P(\d{3})')
_RUN = re.compile(r"<w:r[ >].*?</w:r>", re.S)
_TEXT = re.compile(r"<w:t(?: [^>]*)?>([^<]*)</w:t>")
_FOOTNOTE_REF = re.compile(r'<w:footnoteReference w:id="(\d+)"')
# "ـ المؤلف ـ", "ــ المؤلّف ــ.", "(المؤلف)" (harekeli de); "(بتصحيح المؤلف)" nüsha notudur, hâşiye değil.
_MARKS = "[\u064B-\u0652\u0670]*"
_AUTHOR = re.compile(r"\s*(?:ـ+|\()\s*" + "".join(ch + _MARKS for ch in "المؤلف") + r"\s*(?:ـ+|\))?\s*\.?\s*$")
_NOTE_PREFIX = re.compile(r"^\(\s*\??\s*\)\s*")       # dipnotun başında düz metin "(?)"


@dataclass
class Para:
    text: str
    align: str = "both"
    bold: bool = False
    spans: list[ArabicSpan] = field(default_factory=list)
    marks: list[tuple[int, str]] = field(default_factory=list)   # (konum, dipnotun kimliği)


@dataclass
class Report:
    verses: int = 0
    unknown_glyphs: int = 0
    footnotes: int = 0
    hasiye: int = 0


_GLYPH = re.compile(r"[\uFB50-\uFEFF]")   # QCF yazı tipinde kelime glifi; öbür karakterler (parantez, harf) metindir


class _Decoder:
    """QCF glifleri -> âyet metni ve adresi. Tanınmayan glif, aynı sayfada tanınan kelimelerin arasındaysa
    sayfa verisinden tamamlanır (kelimeler sayfa sırasıyladır)."""

    def __init__(self, root: Path, report: Report) -> None:
        self.root, self.report = root, report
        self.pages: dict[int, tuple[list[dict], dict[str, int]]] = {}

    def index(self, page: int, ch: str) -> int | None:
        if page not in self.pages:
            words = list(qurancom.glyphs(self.root, page).values())
            self.pages[page] = (words, {w["code"]: i for i, w in enumerate(words)})
        found = self.pages[page][1].get(ch)
        if found is None:
            self.report.unknown_glyphs += 1
        return found

    def words(self, glyphs: list[tuple[int, int]]) -> list[dict]:
        out: list[dict] = []
        for page in dict.fromkeys(p for p, _ in glyphs):
            idx = [i for p, i in glyphs if p == page]
            out += self.pages[page][0][min(idx):max(idx) + 1]
        return [w for w in out if w["type"] == "word"]


def _paragraph(xml: str, decoder: _Decoder) -> Para:
    align = re.search(r'<w:jc w:val="(\w+)"', xml)
    bold = bool(re.search(r"<w:b/>|<w:bCs/>", xml))
    text, spans, marks = "", [], []
    glyphs: list[tuple[int, int]] = []

    def flush() -> None:
        nonlocal text, glyphs
        if words := decoder.words(glyphs) if glyphs else []:
            if text and not text.endswith((" ", "{", "(", "[")):
                text += " "
            start = len(text)
            text += " ".join(w["text"] for w in words)
            keys = [tuple(map(int, w["verse_key"].split(":"))) for w in words]
            sura, first, last = keys[0][0], keys[0][1], keys[-1][1]
            ayahs = f"{first}" if first == last or keys[-1][0] != sura else f"{first}-{last}"
            spans.append(ArabicSpan(start, len(text), "ayet", source=f"{SURA_NAMES[sura - 1]} Sûresi, {sura}:{ayahs}"))
            decoder.report.verses += 1
        glyphs = []

    for run in _RUN.findall(xml):
        chars = html.unescape("".join(_TEXT.findall(run)))
        if ref := _FOOTNOTE_REF.search(run):
            flush()
            if text.endswith("("):                    # "مقدمة()": işaret parantezin içindedir
                text = text[:-1]
            marks.append((len(text), ref[1]))
            continue
        page = _QCF.search(run)
        for ch in chars:
            if page and _GLYPH.match(ch):
                if (i := decoder.index(int(page[1]), ch)) is not None:
                    glyphs.append((int(page[1]), i))
            elif page and ch.isspace() and glyphs:
                continue
            else:
                flush()
                if ch == ")" and marks and marks[-1][0] == len(text):
                    continue                          # işaretin kapanış parantezi
                if ch.isspace() and text.endswith(" "):
                    continue                          # silinen işaretin yerinde iki boşluk kalmasın
                text += " " if ch.isspace() else ch
    flush()
    lead = len(text) - len(text.lstrip())
    text = text.strip()
    shift = lambda o: max(0, min(o - lead, len(text)))          # noqa: E731
    return Para(text, align[1] if align else "both", bold,
                [ArabicSpan(shift(a.start), shift(a.end), a.kind, a.meal, a.source) for a in spans],
                [(shift(o), i) for o, i in marks])


def read(path: Path, glyph_root: Path, report: Report) -> tuple[list[Para], dict[str, str]]:
    """Word dosyasının paragrafları ve dipnotları (kimlik -> metin)."""
    z = zipfile.ZipFile(path)
    decoder = _Decoder(glyph_root, report)
    paras = [p for p in (_paragraph(x, decoder) for x in re.findall(r"<w:p[ >].*?</w:p>", z.read("word/document.xml").decode(), re.S))
             if p.text]
    notes = {}
    xml = z.read("word/footnotes.xml").decode()
    for fid, body in re.findall(r'<w:footnote [^>]*w:id="(\d+)"[^>]*>(.*?)</w:footnote>', xml, re.S):
        parts = [_paragraph(x, decoder).text for x in re.findall(r"<w:p[ >].*?</w:p>", body, re.S)]
        text = _NOTE_PREFIX.sub("", " ".join(p for p in parts if p).strip())
        if text:
            notes[fid] = text
    return paras, notes


def qcf_pages(path: Path) -> set[int]:
    """Dosyada kullanılan mushaf sayfaları (kelime verisi indirilecek)."""
    z = zipfile.ZipFile(path)
    return {int(p) for part in ("word/document.xml", "word/footnotes.xml") for p in _QCF.findall(z.read(part).decode())}


# ---------------------------------------------------------------- yapı

def _clean(text: str) -> str:
    """Başlık karşılaştırması: harekesiz, süs işaretleri ("**", "ـ", köşeli ayraç) atılmış."""
    return " ".join(re.sub(r"[*\[\]{}()<>ـ]", " ", _key(text)).split())


# Risaleler: basılı adının başı -> Türkçe eserdeki kimlik. Türkçe Mesnevî'de olmayan "نور" kendi adıyla.
RISALES = (("ترجمة المقدمة التركية", "mukaddime"), ("تنبيه اخطار اعتذار", "itizar"), ("لمعات", "lemalar"),
           ("رشحات", "reshalar"), ("لا سيمات", "lasiyyemalar"), ("قطرة", "katre"), ("حباب", "hubab"),
           ("حبة", "habbe"), ("زهرة", "zuhre"), ("ذرة", "zerre"), ("شمة", "semme"), ("الرسالة العاشرة", "onuncu-risale"),
           ("شعلة", "sule"), ("نور", "nur"))
# Risale içindeki ortalı başlıklar -> kimlik (Türkçe eserdekiyle aynı; yoksa Arapça adından).
SECTIONS = (("افادة المرام", "ifade-i-meram"), ("المقدمة", "mukaddime"), ("تقريظ", "takriz"), ("هذا تقريظ", "takriz"),
            ("خاتمة", "hatime"), ("ذيل للقطرة", "zeyl"), ("ذيل الحباب", "zeylul-hubab"), ("ذيل للحبة", "zeylul-habbe"),
            ("ذيل الذيل", "zeyl"), ("تضرع ونياز", "tazarru-ve-niyaz"), ("تذييل للزهرة", "tezyil"),
            ("ذيل للشعلة", "zeyl"), ("تتمة لمبحث العندليب", "tetimme"), ("مبحث عظيم", "mebhas"),
            ("هذه الخطابة الارشادية", "meclis-i-mebusana-hitaben-yazdigim-bir"))
REPEATED = {"نكتة": "nukte", "نقطة": "nokta", "رمز": "remz"}   # "** نكتة **" dizileri (Katre'nin Hâtime ve Zeyli)
BABS = re.compile(r"^(الباب|القسم)\s+(\S+)(?:\s+من الباب\s+(\S+))?$")
NUMBERED = {"اللمعة": ("Lem'a", "lema"), "الرشحة": ("Reşha", "resha"), "النقطة": ("Nokta", "nokta"),
            "القطرة": ("Katre", "katre"), "الدرس": ("Ders", "ders")}
END = "الفهرس"
TRANSLATED = "Türkçe aslından Arapça tercüme"
SUBTITLE_LINES = 2


def _ordinal(words: list[str]) -> int | None:
    """"الرابعة" -> 4, "الحادية عشرة" -> 11, "الرابع عشر" -> 14."""
    if not words:
        return None
    unit = {"الحادي": 1, "الحادية": 1}.get(words[0]) or ORDINALS.get(words[0].replace("أ", "ا"))
    if unit is None:
        return None
    return unit + 10 if len(words) > 1 and words[1].startswith("عشر") else unit


def parse(work: Work, docx_path: Path, glyph_root: Path) -> tuple[Book, Report]:
    report = Report()
    paras, notes = read(docx_path, glyph_root, report)
    book = Book(work.slug, work.title, {
        "group": str(work.group), "language": work.language, "stops": "*",      # cümle " * " ile de biter
        "source": {"site": str(work.source.site), "book": work.source.book},
    })
    keys = [_clean(p.text) for p in paras]
    start = next(i for i, k in enumerate(keys) if k.startswith(RISALES[0][0]))
    end = next(i for i, k in enumerate(keys) if i > start and k == END)
    book.notes.append({"node_id": book.root.id, "after": None,
                       "text": "Naşirin (Abdülkadir Badıllı) ön sözü ve sondaki fihrist esere dahil edilmedi."})
    _Builder(book, notes, report).run(paras[start:end])
    return book, report


class _Builder:
    def __init__(self, book: Book, notes: dict[str, str], report: Report) -> None:
        self.book, self.notes, self.report = book, notes, report
        self.risale: Node = book.root
        self.node: Node = book.root
        self.titling = False                  # risalenin adından sonraki ortalı satırlar alt başlıktır
        self.subtitle_lines = 0

    def open(self, parent: Node, local: str, title: str, **fields) -> Node:
        self.node = self.book.add_node(parent, local, title, **fields)
        return self.node

    def run(self, paras: list[Para]) -> None:
        for p in paras:
            key = _clean(p.text)
            if not key or set(key) <= {"*", " "} or re.fullmatch(r"\*+", p.text.strip()):
                continue                      # "******" ayıracı
            if self.heading(p, key):
                continue
            self.titling = False
            self.paragraph(p)

    def heading(self, p: Para, key: str) -> bool:
        centered = p.align == "center"
        words = key.split()
        for prefix, local in RISALES:
            if centered and (key == prefix or key.startswith(prefix + " ")) and len(words) <= 8 \
                    and not any(n.id.endswith("/" + local) for n in self.book.root.children):
                self.risale = self.open(self.book.root, local, p.text.strip("* "),
                                        subtitle=TRANSLATED if local == "mukaddime" else "")
                self.titling, self.subtitle_lines = local != "mukaddime", 0
                return True
        if centered and key.startswith("بسم الله") and self.node.id.endswith("/ifade-i-meram"):
            self.node = self.node.parent      # İfâde-i Merâm biter, risalenin (ya da Zeyl'in) metni Besmele ile başlar
        if self.titling and centered and len(words) <= 12 and "بسم" not in key and "{" not in p.text \
                and not any(key.startswith(prefix) for prefix, _ in SECTIONS) and self.subtitle_lines < SUBTITLE_LINES:
            self.risale.subtitle = " ".join(filter(None, [self.risale.subtitle, p.text.strip()]))
            self.subtitle_lines += 1
            return True
        if not centered and not p.bold:
            return self.label(p, key)
        if (m := BABS.match(key)) and (n := _ordinal(m[2].split())):
            if m[1] == "القسم" and m[3]:
                parent = next((c for c in self.risale.children if c.id.endswith(f"bab-{_ordinal(m[3].split()):02d}")),
                              self.risale)
                self.open(parent, f"kisim-{n:02d}", p.text.strip(), type="Kısım", number=n)
            else:
                self.open(self.risale, f"bab-{n:02d}", p.text.strip(), type="Bâb", number=n)
            return True
        if len(words) == 1 and words[0] in REPEATED:
            parent = self.node if self.node.id.endswith("/zeyl") else self.node.parent \
                if self.node.parent and REPEATED.get(_clean(self.node.title)) else self.risale
            if words[0] == "رمز" and not self.node.id.split("/")[-1].startswith(("zeyl", "remz")):
                parent = self.risale
            self.open(parent, REPEATED[words[0]], words[0])
            return True
        for prefix, local in SECTIONS:
            if key.startswith(prefix) and len(words) <= 10:
                if self.node.id.endswith("/" + local):
                    return True               # aynı başlığın tekrarı
                if self.node.parent and self.node.parent.id.endswith("/" + local):
                    self.node = self.node.parent  # Zeyl'in adı İfâde-i Merâm'dan sonra yeniden: asıl metin başlar
                    return True
                self.open(self.section_parent(local, key), local, p.text.strip("* "))
                return True
        return self.label(p, key)

    def section_parent(self, local: str, key: str) -> Node:
        """Zeyl'in İfâde-i Merâm'ı ve Mukaddime'si Zeyl'in, Bâb'ın hâtimesi Bâb'ın altındadır."""
        top = self.node
        while top.parent is not None and top.parent is not self.risale:
            top = top.parent
        if local in ("ifade-i-meram", "mukaddime") and top is not self.risale and top.id.split("/")[-1].startswith("zeyl"):
            return top
        if key.startswith("خاتمة هذا المبحث"):           # Birinci Bâb'ın hâtimesi; Katre'nin Hâtime'si ayrıdır
            babs = [c for c in self.risale.children if c.id.split("/")[-1].startswith("bab-")]
            return babs[-1] if babs else self.risale
        if self.risale.id.endswith("/reshalar") and top.type == "Reşha":
            return top                        # Ondördüncü Reşha'nın "مبحث عظيم"i
        return self.risale

    def label(self, p: Para, key: str) -> bool:
        """Paragraf başındaki numaralı etiket ("اَللَّمْعَةُ الرَّابِعَةُ: …") bölüm açar; etiket metinde kalır.
        Tek başına duran etiket ("اَلرَّشْحَةُ الرَّابِعَةَ عَشْرَةَ") paragraf olmaz."""
        m = re.match(r"^([^\s:]+)\s+([^\s:]+)(?:\s+(عشرة?))?\s*(:)?", key)
        if not (m and m[1] in NUMBERED and (m[4] or len(key.split()) <= 3)):
            return False
        n = _ordinal([w for w in (m[2], m[3]) if w])
        if n is None:
            return False
        type_, prefix = NUMBERED[m[1]]
        if self.node.type == type_ and self.node.number == n:
            return not m[4]                   # aynı etiketin tekrarı
        top = self.node
        while top.parent is not None and top.parent is not self.risale:
            top = top.parent
        if self.node.type == type_:
            parent = self.node.parent
        elif type_ in ("Katre", "Nokta") and top.type == "Reşha":
            parent = top                      # Ondördüncü Reşha'nın Katreleri ve Noktaları
        else:
            parent = self.risale
        self.open(parent, f"{prefix}-{n:02d}", " ".join(p.text.split(":")[0].split()[:3]), type=type_, number=n,
                  heading="inline" if m[4] else None)
        return not m[4]                       # tek başına başlıksa paragraf değildir

    def paragraph(self, p: Para) -> None:
        extra = {"center": True} if p.align == "center" else {}
        record = self.book.add_paragraph(self.node, "paragraph", Text(p.text, p.spans), **extra)
        for offset, fid in p.marks:
            note = self.notes.get(fid)
            if note is None:
                continue
            self.report.footnotes += 1
            if _AUTHOR.search(note):
                self.report.hasiye += 1
                self.book.add_hasiye(record["id"], self.node, offset, Text(_AUTHOR.sub("", note).strip()))
            else:
                self.book.notes.append({"node_id": self.node.id, "after": record["id"], "text": note})
