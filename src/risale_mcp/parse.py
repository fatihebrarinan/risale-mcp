"""Aşama 2: Sözler PDF'i -> hiyerarşik JSON.

Kullanım:
    uv run python -m risale_mcp.parse

Çıktılar (data/interim/):
    sozler.json         başlık ağacı (outline) ve pasajlar
    outline.txt         elle kontrol için girintili başlık ağacı
    fihrist_check.txt   başlık ağacı ile PDF fihristinin karşılaştırması
"""

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

import pymupdf

from risale_mcp.normalize import fold, ordinal_word, parse_ordinal, slugify, tr_capitalize, tr_lower, tr_title

ROOT = Path(__file__).resolve().parents[2]
PDF_PATH = ROOT / "data" / "raw" / "Sozler.pdf"
OUT_DIR = ROOT / "data" / "interim"

BOOK = "sozler"
BOOK_TITLE = "Sözler"
FIRST_PAGE, LAST_PAGE = 5, 774          # 1-4 kapak/künye, 775+ fihrist
FIHRIST_PAGES = (775, 792)

ARABIC_FONTS = {"TTE27E7E00t00", "TTE2735E60t00", "TTE27C1CB8t00"}
TR_GLYPH_BOLD = "TTE2734BB8t00"
TITLE_FONTS = {"TTE27DA560t00", "TTE27C4F88t00"}
ARABIC_PLACEHOLDER = "[Arapça]"
ARABIC_BLOCK_TEXT = "[Arapça metin]"

PAGE_CENTER = 306.0
BODY_LEFT = 128.8
INDENT_MIN, INDENT_MAX = 158.0, 175.0   # ilk satır girintisi x≈161-164

PAGE_MARKER = re.compile(r"-*\s*sh:»?\([SŞ]:\s*\d+\)\s*↓?\s*-*")
HASIYE_START = re.compile(r"^\s*\((Haşiye(?:-\s*\d+)?|\*+)\)\s*:")
HASIYE_START_LOOSE = re.compile(r"^\s*\((Haşiye(?:-\s*\d+)?|\*+)\)")
HASIYE_REF = re.compile(r"\((Haşiye(?:-\s*\d+)?|\*+)\)(?!\s*:)")
SEPARATOR_ROW = re.compile(r"^[\s*]+$")
WORD = r"[A-Za-zÇĞİÖŞÜçğıöşüÂâÎîÛû'’]+"
INLINE_HEADING = re.compile(rf"^\s*({WORD})\s+({WORD})(\s+{WORD})?\s*:")
GENITIVE_END = re.compile(r"(?:ün|un|in|ın|ÜN|UN|İN|IN)\s*$")

# Fihrist'te kitap düzeyinde (Söz ile aynı seviyede) listelenen, Söz olmayan bölümler.
TOP_LEVEL_EXTRA = {fold(t) for t in [
    "Ondördüncü Lem'anın İkinci Makamı", "Lemaat", "Anglikan Kilisesine Cevab", "Konferans",
]}

# Bölüm türlerinin kanonik adları. Ekli biçimler ("Makamı", "Reşhası", "Hatveye") bunlara indirgenir.
KNOWN_TYPES = {fold(t): t for t in [
    "Söz", "Makam", "Mebhas", "Maksad", "Mevkıf", "Mukaddime", "Mukaddeme", "Hâtime", "Zeyl",
    "Esas", "Hakikat", "Nükte", "Sır", "Suret", "İşaret", "Remiz", "Lem'a", "Nokta", "Mes'ele",
    "Pencere", "Bürhan", "Levha", "Kâr", "Hasaret", "Asıl", "Vecih", "Temsil", "Sual", "Meyve",
    "Medar", "Menba'", "Basamak", "Şua", "Şu'le", "Ziya", "Işık", "Misal", "Fıkra", "Hüccet",
    "Dal", "Hatve", "Cilve", "Şavk", "Sebeb", "Kısım", "Cüz'", "Nur", "Hikmet", "Müşkil",
    "Reşha", "Parça", "Mertebe", "Mukayese", "Ders", "Kelime", "Cihet", "Hikâye", "Haşiye",
]}
UNNUMBERED_STRUCTURAL = {fold(t) for t in ["Mukaddime", "Mukaddeme", "Hâtime", "Zeyl", "Haşiye"]}
SUFFIXES = ["sidir", "sıdır", "sudur", "südür", "dir", "dır", "sı", "si", "su", "sü",
            "nın", "nin", "nun", "nün", "ye", "ya", "de", "da", "ı", "i", "u", "ü"]
UNNUMBERED_STRUCTURAL_INTRO = {fold("Mukaddime"), fold("Mukaddeme")}

# Puntosu yapısal konumuyla uyuşmayan başlıklar (görsel seviye elle düzeltilir).
# Dokuzuncu Şua (s.94) 14pt basılmış ama Onuncu Söz Hâtimesi'nin değil, Söz'ün zeylidir
# ("Zeylin İkinci Parçası" vb. ile kardeş).
LEVEL_OVERRIDES = {fold("Dokuzuncu Şua"): 2}


# ---------------------------------------------------------------- satırlar

@dataclass
class Row:
    page: int
    y0: float
    y1: float
    x0: float
    x1: float
    text: str                 # Arapça kısımlar yer tutucuyla değiştirilmiş metin
    size: float
    bold: bool
    title_font: bool
    arabic_only: bool
    glyphs: str = ""          # Arapça fontun ham kodları (ileride çözmek için)

    @property
    def centered(self) -> bool:
        # Girintili tam satırlar (x0≈164, x1≈486) da merkeze yakın düşer; sağ kenara uzananlar ortalı değildir.
        return abs((self.x0 + self.x1) / 2 - PAGE_CENTER) < 12 and self.x0 > 134 and self.x1 < 482


def _is_bold(span: dict) -> bool:
    return "Bold" in span["font"] or span["font"] == TR_GLYPH_BOLD or span["font"] in TITLE_FONTS


def _build_row(page_no: int, lines: list[dict]) -> Row | None:
    lines.sort(key=lambda l: l["bbox"][0])
    parts: list[str] = []
    glyphs: list[str] = []
    latin_spans: list[dict] = []
    arabic_sizes: list[float] = []
    prev_x1 = None
    for line in lines:
        if prev_x1 is not None and line["bbox"][0] - prev_x1 > 1.5:
            parts.append(" ")
        prev_x1 = line["bbox"][2]
        for span in line["spans"]:
            text = span["text"]
            if span["font"] in ARABIC_FONTS:
                if text.strip(" ×\x01"):
                    glyphs.append(text)
                    arabic_sizes.append(span["size"])
                    if not (parts and parts[-1] == ARABIC_PLACEHOLDER):
                        if parts and not parts[-1].endswith(" "):
                            parts.append(" ")
                        parts.append(ARABIC_PLACEHOLDER)
                else:
                    parts.append(" ")
                continue
            if parts and parts[-1] == ARABIC_PLACEHOLDER and text[:1].isalnum():
                parts.append(" ")
            parts.append(text)
            if text.strip():
                latin_spans.append(span)

    text = re.sub(r"\s+", " ", "".join(parts)).strip()
    text = PAGE_MARKER.sub("", text).strip() if PAGE_MARKER.search(text) else text
    has_latin = bool(re.search(r"[^\W_]", text.replace(ARABIC_PLACEHOLDER, "")))
    if not text or (not has_latin and not glyphs):
        return None
    sizes = [s["size"] for s in latin_spans] or arabic_sizes
    # Başlıktaki "(Haşiye)" atfı düz yazılır; kalınlık kararında yok sayılır (s.678).
    non_bold = "".join(s["text"] for s in latin_spans if not _is_bold(s))
    non_bold = re.sub(r"\s+", "", HASIYE_REF.sub("", re.sub(r"\s+", "", non_bold)))
    x0 = min(l["bbox"][0] for l in lines)
    x1 = max(l["bbox"][2] for l in lines)
    return Row(
        page=page_no,
        y0=min(l["bbox"][1] for l in lines),
        y1=max(l["bbox"][3] for l in lines),
        x0=x0, x1=x1,
        # Tamamen Arapça satırda yalnızca hâşiye atıfları korunur: "[Arapça metin] (*)" (s.727).
        text=text if has_latin else " ".join([ARABIC_BLOCK_TEXT] + [m.group(0) for m in HASIYE_REF.finditer(text)]),
        size=max(sizes),
        bold=bool(latin_spans) and not non_bold,
        title_font=any(s["font"] in TITLE_FONTS and s["size"] >= 30 for s in latin_spans),
        arabic_only=not has_latin,
        glyphs=" ".join(glyphs),
    )


def page_rows(page: pymupdf.Page, page_no: int) -> list[Row]:
    """Satırları y'ye göre sıralar; aynı görsel satırdaki parçaları birleştirir."""
    lines = [l for b in page.get_text("dict")["blocks"] for l in b.get("lines", [])
             if any(s["text"].strip() for s in l["spans"])]
    lines.sort(key=lambda l: (l["bbox"][1] + l["bbox"][3]) / 2)
    groups: list[list[dict]] = []
    for line in lines:
        yc = (line["bbox"][1] + line["bbox"][3]) / 2
        h = line["bbox"][3] - line["bbox"][1]
        if groups:
            last = groups[-1][-1]
            lyc = (last["bbox"][1] + last["bbox"][3]) / 2
            lh = last["bbox"][3] - last["bbox"][1]
            if abs(yc - lyc) < 0.4 * min(h, lh):
                groups[-1].append(line)
                continue
        groups.append([line])
    return [r for g in groups if (r := _build_row(page_no, g))]


def split_hasiye_zone(page: pymupdf.Page, rows: list[Row]) -> tuple[list[Row], list[Row]]:
    """Ana metin ve hâşiye satırlarını ayırır. Hâşiye bölgesi, sayfa genişliğindeki ayırıcı
    çizginin altındaki ilk '(Haşiye…):' satırından sayfa sonuna kadar sürer."""
    seps = sorted(r.y0 for r in (d["rect"] for d in page.get_drawings())
                  if r.height < 2 and r.width > 300)
    start_idx = None
    for sep in seps:
        below = [i for i, r in enumerate(rows) if r.y0 >= sep - 3]
        strict = [i for i in below if HASIYE_START.match(rows[i].text)]
        if strict:
            start_idx = strict[0]
        elif below and HASIYE_START_LOOSE.match(rows[below[0]].text):
            start_idx = below[0]                       # "(*) Nur'un birinci kâtibidir." (s.553)
        if start_idx is not None:
            break
    if start_idx is None:
        # Ayırıcısız sayfalar (267, 670, 723): ilk kesin hâşiye başlangıcından itibaren.
        start_idx = next((i for i, r in enumerate(rows) if HASIYE_START.match(r.text)), None)
    if start_idx is None:
        return rows, []
    return rows[:start_idx], rows[start_idx:]


# ---------------------------------------------------------------- bloklar

@dataclass
class Block:
    kind: str                       # heading | paragraph | arabic | hasiye | break
    rows: list[Row]
    level: int = 0                  # başlıklar için görsel seviye (1 = Söz)
    title: str = ""
    subtitle: str = ""
    htype: str = ""                 # kanonik bölüm türü ("Hakikat")
    number: int | None = None
    inline: bool = False            # paragraf başındaki kalın önekten gelen başlık
    upper: bool = False             # önek TAMAMI BÜYÜK harf mi
    label: str = ""                 # hâşiye etiketi ("Haşiye-2")
    node: "Node | None" = None

    @property
    def text(self) -> str:
        out = ""
        for r in self.rows:
            t = r.text
            if not out:
                out = t
            elif out.endswith("-") and not out.endswith(" -"):
                out += t                     # birleşik kelime tiresi: "daire-" + "i a'zamında"
            else:
                out += " " + t
        return out

    @property
    def page_start(self) -> int:
        return self.rows[0].page

    @property
    def page_end(self) -> int:
        return self.rows[-1].page


def canonical_type(word: str) -> str:
    f = fold(word)
    if f in KNOWN_TYPES:
        return KNOWN_TYPES[f]
    for suf in SUFFIXES:
        if f.endswith(suf) and f[: -len(suf)] in KNOWN_TYPES:
            return KNOWN_TYPES[f[: -len(suf)]]
    return tr_capitalize(word)


def fix_letter_spacing(text: str) -> str:
    """Harf aralıklı başlıklarda bölünen sıra sayılarını birleştirir: 'Do kuzuncu' -> 'Dokuzuncu'."""
    tokens = text.split(" ")
    out: list[str] = []
    for tok in tokens:
        if out and parse_ordinal(out[-1]) is None and parse_ordinal(out[-1] + tok) is not None:
            out[-1] += tok
        else:
            out.append(tok)
    return " ".join(out)


def heading_level(row: Row) -> int:
    if row.title_font:
        return 1
    key = fold(fix_letter_spacing(row.text))
    if key in TOP_LEVEL_EXTRA:
        return 1
    if key in LEVEL_OVERRIDES:
        return LEVEL_OVERRIDES[key]
    if row.size >= 18:
        return 2
    if row.size >= 13.5:
        return 3
    return 4


def _title_like(text: str) -> bool:
    """Başlıklar büyük harfle başlayan kelimelerden oluşur; cümle gibi satırlar başlık değildir
    ("Tevekkül eden ve etmeyenin misalleri, şu hikâyeye benzer:")."""
    words = [w for w in re.findall(WORD, fix_letter_spacing(text)) if len(w) >= 3 and tr_lower(w) not in {"ve", "ile", "bir"}]
    if not words:
        return True
    return sum(w[0].isupper() for w in words) / len(words) >= 0.6


def is_heading_row(row: Row) -> bool:
    if row.arabic_only or ARABIC_PLACEHOLDER in row.text or len(row.text) > 110:
        return False
    if row.title_font or (row.bold and row.size >= 30):
        return True                                   # Söz başlığı; 36pt alt başlık (s.691)
    if row.text.count("]") > row.text.count("[") or row.text.count(")") > row.text.count("("):
        return False                                  # önceki satırda açılan notun kapanışı
    return row.bold and row.centered and (_title_like(row.text) or row.text[:1] in "([")


def _unbalanced(text: str) -> bool:
    return text.count("(") > text.count(")") or text.count("[") > text.count("]")


def _is_structural(text: str) -> bool:
    number, _ = _parse_number_and_type(text)
    return number is not None or fold(text) in UNNUMBERED_STRUCTURAL


def _merge_heading(prev: Block, row: Row) -> bool:
    """Ardışık ortalı başlık satırlarını tek başlıkta birleştirme kararı."""
    last = prev.rows[-1]
    if row.page != last.page or row.y0 - last.y1 > 2.2 * row.size:
        return False
    joined = " ".join(r.text for r in prev.rows)
    if _unbalanced(joined):
        return True                                   # parantez/köşeli parantez içi devam
    if last.title_font and row.title_font:
        return True
    if heading_level(row) != prev.level or row.text[:1] in "([":
        return False
    if GENITIVE_END.search(last.text) or fold(row.text) == "söz":
        return True
    return not _is_structural(row.text) and not last.text.rstrip().endswith((".", ":"))


def _known_type(word: str) -> str | None:
    t = canonical_type(word)
    return t if fold(t) in KNOWN_TYPES else None


def _parse_number_and_type(text: str) -> tuple[int | None, str]:
    """Başlığın son kelimesine göre tür ve numara: 'Zeylin İkinci Parçası' -> (2, 'Parça');
    '... İkinci Makamının Haşiyesidir' -> (None, 'Haşiye')."""
    tokens = re.findall(WORD, fix_letter_spacing(text))
    if not tokens:
        return None, ""
    last_type = _known_type(tokens[-1])
    if len(tokens) >= 2 and last_type and parse_ordinal(tokens[-2]) is not None:
        return parse_ordinal(tokens[-2]), last_type
    if last_type and fold(last_type) in UNNUMBERED_STRUCTURAL:
        return None, last_type                        # "...Makamının Haşiyesidir", "...Sözün Zeyli"
    return None, ""                                   # "Otuzüç Penceredir" yapısal değil


def build_blocks(doc: pymupdf.Document) -> tuple[list[Block], list[Block]]:
    """Ana akış bloklarını ve hâşiye bloklarını döndürür."""
    flow: list[Block] = []
    hasiyeler: list[Block] = []

    for pno in range(FIRST_PAGE, LAST_PAGE + 1):
        page = doc[pno - 1]
        rows = page_rows(page, pno)
        main, notes = split_hasiye_zone(page, rows)

        for k, row in enumerate(main):
            prev = flow[-1] if flow else None
            if SEPARATOR_ROW.match(row.text):
                flow.append(Block("break", [row]))
                continue
            if row.arabic_only:
                if prev and prev.kind == "arabic" and prev.page_end == pno:
                    prev.rows.append(row)
                else:
                    flow.append(Block("arabic", [row]))
                continue
            in_open_heading = (prev is not None and prev.kind == "heading" and prev.page_end == pno
                               and _unbalanced(" ".join(r.text for r in prev.rows)) and row.centered)
            if is_heading_row(row) or in_open_heading:
                if prev and prev.kind == "heading" and _merge_heading(prev, row):
                    prev.rows.append(row)
                else:
                    flow.append(Block("heading", [row], level=heading_level(row)))
                continue
            # Paragraf satırı
            starts_new = (
                INDENT_MIN <= row.x0 <= INDENT_MAX      # ilk satır girintisi
                or _inline_heading(row.text) is not None  # girintisiz "Yedinci Esas:" (s.76)
                or row.x0 > INDENT_MAX                  # ortalı / şiir satırı
                or prev is None or prev.kind != "paragraph"
            )
            if (starts_new and prev is not None and prev.kind == "paragraph" and prev.page_end == pno
                    and _unbalanced(prev.text) and not INDENT_MIN <= row.x0 <= INDENT_MAX):
                starts_new = False                      # köşeli parantezli notun devam satırı
            elif not starts_new and prev.page_end == pno:
                gap = row.y0 - prev.rows[-1].y1
                starts_new = gap > 1.4 * row.size
            if not starts_new and prev.page_end != pno and k > 0:
                starts_new = True                       # sayfada önce başka öğe var
            if starts_new:
                flow.append(Block("paragraph", [row]))
            else:
                prev.rows.append(row)                   # aynı sayfada ya da sayfa aşan devam

        for row in notes:
            m = HASIYE_START_LOOSE.match(row.text)
            if m or not hasiyeler or hasiyeler[-1].page_end != pno:
                label = re.sub(r"\s+", "", m.group(1)) if m else "?"
                hasiyeler.append(Block("hasiye", [row], label=label))
            else:
                hasiyeler[-1].rows.append(row)
    return flow, hasiyeler


def _inline_heading(text: str) -> tuple[int, str, bool] | None:
    """Paragraf başındaki numaralı önek: 'BİRİNCİ SIR: …' -> (1, 'Sır', True)."""
    m = INLINE_HEADING.match(text)
    if not m or not m.group(2)[:1].isupper():
        return None
    n = parse_ordinal(m.group(1))
    if n is None:
        return None
    noun = m.group(2)
    letters = [c for c in noun if c.isalpha()]
    return n, noun, all(c.isupper() for c in letters)


def annotate_headings(flow: list[Block]) -> list[Block]:
    """Başlık metinlerini, türlerini, numaralarını ve alt başlıkları belirler;
    paragraf başındaki numaralı önekleri (Birinci Hakikat: …) başlık olarak işaretler."""
    out: list[Block] = []
    for b in flow:
        if b.kind == "heading":
            raw = fix_letter_spacing(" ".join(r.text for r in b.rows))
            raw = re.sub(r"\s+", " ", HASIYE_REF.sub("", raw)).strip()    # atıf pasaja bağlanır
            # Arada yalnızca Arapça blok ya da köşeli parantezli not varsa önceki başlık "hemen önce" sayılır.
            prev_heading = next((x for x in reversed(out)
                                 if not (x.kind == "arabic" or (x.kind == "paragraph" and x.text[:1] in "(["))),
                                None)
            number, htype = _parse_number_and_type(raw)
            structural = number is not None or bool(htype)
            if (out and out[-1] is prev_heading and prev_heading is not None
                    and prev_heading.kind == "heading" and not prev_heading.inline
                    and prev_heading.level == b.level and structural and not prev_heading.htype
                    and prev_heading.number is None and prev_heading.level > 1):
                # Yapısal başlıktan hemen önce gelen açıklayıcı satır -> ön başlık (s.154)
                out.pop()
                b.subtitle = (prev_heading.title + " " + prev_heading.subtitle).strip()
                b.rows = prev_heading.rows + b.rows
            if (b.level > 1 and prev_heading is not None and prev_heading.kind == "heading"
                    and not prev_heading.inline and not structural and not raw.endswith(":")):
                # Başlığın hemen ardından gelen açıklama satırı -> alt başlık
                prev_heading.subtitle = (prev_heading.subtitle + " " + raw).strip()
                prev_heading.rows = prev_heading.rows + b.rows
                continue
            if raw[:1] in "([" or (raw.endswith(":") and not structural):
                b.kind = "paragraph"         # ortalı açıklama notu ya da "…Şudur Ki:" cümlesi
                out.append(b)
                continue
            if b.level == 1 and b.rows[0].title_font:
                n = parse_ordinal(raw.split()[0]) if raw.split() else None
                if n is not None and "söz" in tr_lower(raw):
                    b.title, b.number, b.htype = f"{ordinal_word(n)} Söz", n, "Söz"
                else:
                    b.title = tr_title(raw)
            else:
                b.title = tr_title(raw).rstrip(" :")
                b.number, b.htype = number, htype
            out.append(b)
            continue

        if b.kind == "paragraph" and (ih := _inline_heading(b.rows[0].text)):
            n, noun, upper = ih
            # Başlıkta metindeki kelime korunur ("Birinci Hatveye" / "Birinci Hatvede"); tür kanoniktir.
            title = f"{ordinal_word(n)} {tr_capitalize(noun) if upper else noun}"
            out.append(Block("heading", b.rows[:1], level=5 if upper else 6, inline=True,
                             upper=upper, htype=canonical_type(noun), number=n, title=title))
        out.append(b)
    return out


# ---------------------------------------------------------------- hiyerarşi

@dataclass
class Node:
    id: str
    title: str
    level: int                       # görsel seviye
    htype: str
    number: int | None
    parent: "Node | None"
    page_start: int
    subtitle: str = ""
    children: list["Node"] = field(default_factory=list)
    paragraphs: int = 0
    first_seq: int | None = None
    last_seq: int | None = None

    @property
    def depth(self) -> int:
        return 0 if self.parent is None else self.parent.depth + 1

    def path(self) -> list[str]:
        return [] if self.parent is None else self.parent.path() + [self.title]


def _continues(headings: list[Block], idx: int, top: Block) -> bool:
    """`top` başlığının bir sonraki numaralı kardeşi, kapsayıcısı kapanmadan geliyor mu?"""
    for h in headings[idx + 1:]:
        if h.level < top.level:
            return False
        if h.level == top.level and h.htype == top.htype:
            # +1 beklenir; ama bazı maddeler başlık olarak yakalanamıyor ("Üçüncü Dal" gibi).
            return top.number is not None and h.number is not None and h.number > top.number
    return False


def build_tree(blocks: list[Block]) -> Node:
    root = Node(BOOK, BOOK_TITLE, 0, "", None, None, FIRST_PAGE)
    headings = [b for b in blocks if b.kind == "heading"]
    hindex = {id(h): i for i, h in enumerate(headings)}
    stack: list[tuple[Block | None, Node]] = [(None, root)]

    def make_node(h: Block, parent: Node) -> Node:
        if h.htype == "Söz" and h.level == 1:
            local = str(h.number)
        elif h.number is not None and h.htype:
            local = f"{slugify(h.htype)}-{h.number:02d}"
        elif h.htype:
            local = slugify(h.htype)                    # hatime, zeyl, mukaddime, hasiye
        else:
            local = slugify(" ".join(h.title.split()[:4])) or "bolum"
        base = f"{parent.id}/{local}"
        nid, k = base, 2
        while any(c.id == nid for c in parent.children):
            nid, k = f"{base}-{k}", k + 1
        node = Node(nid, h.title, h.level, h.htype, h.number, parent, h.page_start, h.subtitle)
        parent.children.append(node)
        return node

    # Birinci Söz'den önceki giriş metni için yapay düğüm (başlığı PDF'te yok).
    intro = Node(f"{BOOK}/giris", "Giriş", 1, "", None, root, FIRST_PAGE)
    root.children.append(intro)
    stack.append((None, intro))

    for b in blocks:
        if b.kind != "heading":
            b.node = stack[-1][1]
            continue
        if b.level == 1:
            del stack[1:]
        else:
            same = None
            if b.number is not None and b.htype:
                for i in range(len(stack) - 1, 0, -1):
                    top = stack[i][0]
                    if top is None or top.level == 1:
                        break
                    if top.htype == b.htype and top.number is not None:
                        same = i
                        break
            if same is None and fold(b.htype) in UNNUMBERED_STRUCTURAL_INTRO:
                # Mukaddime, henüz alt bölümü olmayan en yakın bölümün girişidir (Dokuzuncu Şua › Mukaddeme).
                while len(stack) > 2 and stack[-1][0] is not None and stack[-1][0].inline:
                    stack.pop()
                if not stack[-1][1].children and stack[-1][0] is not None:
                    node = make_node(b, stack[-1][1])
                    stack.append((b, node))
                    b.node = node
                    continue
            if same is None and b.inline and b.number == 1:
                # Mukaddime'nin kapsamı: hemen ardından gelen BÜYÜK HARFLİ seri (Onuncu Söz › Mukaddime ›
                # BİRİNCİ İŞARET) Mukaddime'ye aittir. Küçük harfli bir seri ya da Mukaddime'nin kendi serisi
                # bittikten sonra başlayan yeni bir seri, Mukaddime'den çıkar (Onuncu Söz › Birinci Hakikat).
                mi = next((i for i in range(len(stack) - 1, 0, -1) if stack[i][0] is not None
                           and fold(stack[i][0].htype) in UNNUMBERED_STRUCTURAL_INTRO), None)
                if mi is not None:
                    muk_node = stack[mi][1]
                    if not muk_node.children:
                        leave = not b.upper
                    else:
                        series_top = stack[mi + 1][0] if mi + 1 < len(stack) else None
                        leave = (series_top is not None and series_top.htype != b.htype
                                 and not _continues(headings, hindex[id(b)], series_top))
                    if leave:
                        del stack[mi:]
            if same is not None:
                del stack[same:]
            else:
                while len(stack) > 1:
                    top = stack[-1][0]
                    if top is None or top.level == 1 and b.level > 1:
                        break
                    if top.level > b.level:
                        stack.pop()
                        continue
                    if top.level < b.level:
                        break
                    if not b.inline or top.htype == b.htype:
                        stack.pop()
                        continue
                    if _continues(headings, hindex[id(b)], top):
                        break                       # iç içe: üstteki seri devam edecek
                    stack.pop()                     # art arda: kardeş seri
        node = make_node(b, stack[-1][1])
        stack.append((b, node))
        b.node = node
    return root


# ---------------------------------------------------------------- pasajlar

def ref_for(node: Node, suffix: str) -> str:
    return " › ".join([BOOK_TITLE] + node.path() + [suffix])


def build_passages(blocks: list[Block], hasiyeler: list[Block]) -> list[dict]:
    passages: list[dict] = []
    refs_on_page: dict[tuple[int, str], dict] = {}
    pending_heading_refs: list[tuple[int, str]] = []
    seq = 0

    for b in blocks:
        if b.kind == "heading":
            for m in HASIYE_REF.finditer(b.text):
                pending_heading_refs.append((b.page_start, re.sub(r"\s+", "", m.group(1))))
            continue
        if b.kind not in ("paragraph", "arabic"):
            continue
        node = b.node
        node.paragraphs += 1
        seq += 1
        n = node.paragraphs
        p = {
            "id": f"{node.id}/p{n:03d}",
            "book": BOOK,
            "path": node.path(),
            "ref": ref_for(node, f"¶{n}"),
            "seq": seq,
            "kind": b.kind,
            "text": (b.text if b.kind == "paragraph" else " ".join(
                [ARABIC_BLOCK_TEXT] + [m.group(0) for m in HASIYE_REF.finditer(b.text)])),
            "parent_id": None,
            "node_id": node.id,
            "page_start": b.page_start,
            "page_end": b.page_end,
        }
        if b.kind == "arabic":
            p["arabic_glyphs"] = " / ".join(r.glyphs for r in b.rows)
        elif any(r.glyphs for r in b.rows):
            p["arabic_glyphs"] = " / ".join(r.glyphs for r in b.rows if r.glyphs)
        passages.append(p)
        node.first_seq = node.first_seq or seq
        anc = node
        while anc is not None:
            anc.first_seq = anc.first_seq or seq
            anc.last_seq = seq
            anc = anc.parent
        for page, label in pending_heading_refs:
            refs_on_page.setdefault((page, label), p)
        pending_heading_refs.clear()
        # Atıf satır sonunda bölünebilir: "(Haşiye-" + "19)" (s.288); birleşik metinde aranır.
        for m in HASIYE_REF.finditer(b.text):
            label = re.sub(r"\s+", "", m.group(1))
            for page in range(b.page_start, b.page_end + 1):
                refs_on_page[(page, label)] = p

    by_parent: dict[str, int] = {}
    unresolved = []
    for h in hasiyeler:
        parent = refs_on_page.get((h.page_start, h.label))
        uncertain = parent is None
        if parent is None:
            # Atıf bulunamadı: aynı sayfadaki son ana pasaja bağla, belirsiz olarak işaretle.
            parent = next(p for p in reversed(passages)
                          if p["kind"] != "hasiye" and p["page_start"] <= h.page_start)
            unresolved.append(h)
        k = by_parent[parent["id"]] = by_parent.get(parent["id"], 0) + 1
        text = HASIYE_START_LOOSE.sub("", h.text, count=1).lstrip(" :")
        passages.append({
            "id": f"{parent['id']}/h{k}",
            "book": BOOK,
            "path": parent["path"],
            "ref": f"{parent['ref']} › Hâşiye {k}",
            "seq": None,
            "kind": "hasiye",
            "text": text,
            "label": h.label,
            "parent_id": parent["id"],
            "node_id": parent["node_id"],
            "page_start": h.page_start,
            "page_end": h.page_end,
            "parent_uncertain": uncertain,
        })
    # Tek hâşiyeli pasajlarda numara verilmez: "… › ¶3 › Hâşiye".
    for p in passages:
        if p["kind"] == "hasiye" and by_parent[p["parent_id"]] == 1:
            p["ref"] = p["ref"].rsplit(" ", 1)[0]
    return passages


# ---------------------------------------------------------------- çıktılar

def outline_records(root: Node) -> list[dict]:
    out = []

    def walk(n: Node):
        if n.parent is not None:
            out.append({
                "id": n.id, "title": n.title, "subtitle": n.subtitle or None,
                "type": n.htype or None, "number": n.number,
                "depth": n.depth, "parent_id": n.parent.id if n.parent.parent else None,
                "ref": " › ".join([BOOK_TITLE] + n.path()),
                "page_start": n.page_start, "first_seq": n.first_seq, "last_seq": n.last_seq,
                "paragraphs": n.paragraphs,
            })
        for c in n.children:
            walk(c)
    walk(root)
    return out


def outline_text(root: Node) -> str:
    lines = []

    def walk(n: Node):
        if n.parent is not None:
            sub = f"  — {n.subtitle}" if n.subtitle else ""
            lines.append(f"{'  ' * (n.depth - 1)}{n.title}{sub}  [s.{n.page_start}, ¶{n.paragraphs}]  ({n.id})")
        for c in n.children:
            walk(c)
    walk(root)
    return "\n".join(lines) + "\n"


def fihrist_check(doc: pymupdf.Document, outline: list[dict]) -> str:
    text = "".join(doc[i].get_text() for i in range(FIHRIST_PAGES[0] - 1, FIHRIST_PAGES[1]))
    entries = [(m.group(1).strip(), int(m.group(2)))
               for m in re.finditer(r"^(.{3,80}?):\s*(\d+)\s*$", text, re.M)]
    candidates = [o for o in outline if o["depth"] <= 3]

    def key(s: str) -> str:
        return re.sub(r"[^\wçğıöşü ]", " ", fold(s)).split()

    def tokens_match(want: list[str], have: list[str]) -> bool:
        """Fihrist kelimeleri sırayla, ek farkına toleranslı (önek eşleşmesi) olarak bulunmalı."""
        i = 0
        for w in want:
            while i < len(have) and not (have[i].startswith(w[:max(4, len(w) - 3)])
                                         or w.startswith(have[i][:max(4, len(have[i]) - 3)])):
                i += 1
            if i == len(have):
                return False
            i += 1
        return True

    rows = ["Fihrist girişi | Fihrist s. | Ağaçta bulunan düğüm | Ağaç s. | Durum", "-" * 100]
    ok = 0
    for title, page in entries:
        if fold(title) == "fihrist":
            continue
        k = key(title)
        best = None
        # Fihrist'te iki satıra bölünen girişlerin yalnızca ikinci satırı yakalanır
        # ("… EDEN BİRİNCİ LEVHA"); eşleşme yoksa son iki kelimeyle yeniden denenir.
        for attempt in (k, k[-2:]):
            if best is not None:
                break
            k = attempt
            for o in candidates:
                have = key(o["ref"] + " " + (o["subtitle"] or ""))
                if tokens_match(k, have) and tokens_match(key(o["title"])[-1:], k + key(o["subtitle"] or "")):
                    if best is None or abs(o["page_start"] - page) < abs(best["page_start"] - page):
                        best = o
        if best is None:
            status = "BULUNAMADI"
        elif abs(best["page_start"] - page) <= 1:
            status = "OK"
            ok += 1
        else:
            status = f"SAYFA FARKI ({best['page_start'] - page:+d})"
        rows.append(f"{title} | {page} | {best['ref'] if best else '-'} | "
                    f"{best['page_start'] if best else '-'} | {status}")
    rows.append(f"\nEşleşen: {ok} / {len(entries) - 1}")
    return "\n".join(rows) + "\n"


def main() -> None:
    doc = pymupdf.open(PDF_PATH)
    flow, hasiyeler = build_blocks(doc)
    blocks = annotate_headings(flow)
    root = build_tree(blocks)
    passages = build_passages(blocks, hasiyeler)
    outline = outline_records(root)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "sozler.json").write_text(
        json.dumps({"book": BOOK, "title": BOOK_TITLE, "source": PDF_PATH.name,
                    "outline": outline, "passages": passages}, ensure_ascii=False, indent=1),
        encoding="utf-8")
    (OUT_DIR / "outline.txt").write_text(outline_text(root), encoding="utf-8")
    (OUT_DIR / "fihrist_check.txt").write_text(fihrist_check(doc, outline), encoding="utf-8")

    kinds: dict[str, int] = {}
    for p in passages:
        kinds[p["kind"]] = kinds.get(p["kind"], 0) + 1
    print(f"Düğüm: {len(outline)}  Pasaj: {len(passages)}  Türler: {kinds}")
    print(f"Belirsiz hâşiye bağlantısı: {sum(1 for p in passages if p.get('parent_uncertain'))}")
    print(f"Çıktılar: {OUT_DIR}")


if __name__ == "__main__":
    main()
