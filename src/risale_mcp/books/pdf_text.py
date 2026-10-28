"""Kullanıcının PDF'inden (LibreOffice çıktısı) satırlar: Türkçe metin ve glif kimliklerinden çözülen Arapça.

PDF'in Arapçası metin olarak okunamaz: yazı tipinin karakter eşlemesi (ToUnicode) harekeleri ve noktaları
harf diye verir ("بسم" yerine "سم م"). Ama her glif tektir: gömülü DejaVu Sans glifleri sistemdeki DejaVu
Sans'ın glifleriyle birebir aynıdır. Bu eşleme bir kez çıkarıldı (`rumuzat_glyphs.tsv`; Arial'ın 38 glifi
gözle okundu): her glif bir harf (`L`, sunum biçimi temel harfe indirilmiş), noktasız bir gövde (`S`: ب ت ث ن ي
gövdesi "beh", ف ق gövdesi, sondaki ى ve ں), nokta (`D1`..`D3`) ya da harekedir (`M`, ince "۪" dahil).

Satır kurma:
- Taban glifler (harf, gövde, Latin) taban çizgilerine göre satırlara toplanır.
- Hareke ve nokta akışta ardından geldiği harfe bağlanır; akışta önünde harf yoksa mürekkebinin merkezi hangi
  Arapça taban glifin genişliğindeyse ona (yoksa en yakınına). Noktalar gövdeyi harfe çevirir: gövdenin altında bir nokta ب, üstünde iki nokta ت…
- Glifler görsel sırayla (soldan sağa) gelir. Arapça parçalar (Arapça harfler ve aralarındaki her şey,
  Latin harf hariç) mantıksal sıraya çevrilir: ters çevrilir, içindeki rakam dizileri ve ayraçlar düzeltilir.
  Latin harfi olmayan satır baştan sona Arapçadır.
"""

import re
from collections import defaultdict
from dataclasses import dataclass, field
from importlib.resources import files

import pymupdf

_DOTTED = {("beh", "b1"): "ب", ("beh", "a2"): "ت", ("beh", "a3"): "ث", ("beh", "a1"): "ن", ("beh", "b2"): "ي",
           ("beh", "b3"): "پ", ("beh", ""): "ى", ("noon", "a1"): "ن", ("noon", ""): "ں",
           ("yeh", "b2"): "ي", ("yeh", ""): "ى", ("feh", "a1"): "ف", ("feh", "a2"): "ق", ("qaf", "a1"): "ف",
           ("qaf", "a2"): "ق", ("feh", ""): "ڡ", ("qaf", ""): "ٯ", ("feh1", ""): "ف", ("feh1", "a1"): "ق"}
_MIRROR = str.maketrans("()[]{}«»", ")(][}{»«")
_ARABIC_DIGITS = "٠١٢٣٤٥٦٧٨٩"
_LATIN = re.compile(r"[A-Za-zÀ-ɏ]")


def _table() -> dict[str, dict[int, tuple[str, float, float]]]:
    out: dict[str, dict] = defaultdict(dict)
    for line in files("risale_mcp.books").joinpath("rumuzat_glyphs.tsv").read_text(encoding="utf-8").splitlines():
        if line.startswith("#") or not line.strip():
            continue
        font, gid, token, cx, cy = line.split("\t")
        out[font][int(gid)] = (token, float(cx or 0), float(cy or 0))
    return out


@dataclass
class Glyph:
    kind: str           # L (Arapça harf), S (noktasız gövde), M (hareke), D (nokta), T (PDF'in verdiği karakter)
    value: str
    x: float            # başlangıç (origin)
    y: float            # taban çizgisi
    width: float
    size: float
    bold: bool
    color: int
    order: int          # sayfadaki akış sırası
    ink: tuple[float, float] = (0.0, 0.0)
    marks: list["Glyph"] = field(default_factory=list)
    rotated: bool = False

    @property
    def arabic(self) -> bool:
        return self.kind in "LS" or (self.kind == "T" and self.value in _ARABIC_DIGITS)


@dataclass
class PdfLine:
    page: int
    y: float
    x0: float
    x1: float
    text: str
    size: float
    bold: bool          # Latin harflerinin çoğu kalın
    color: int          # en çok kullanılan renk
    rtl: bool
    arabic: list[tuple[int, int]] = field(default_factory=list)   # Arapça parçalar (başlangıç, bitiş)


@dataclass
class PdfTable:
    page: int
    y: float
    rows: list[list[str]]                                  # hücreler soldan sağa


@dataclass
class Report:
    unresolved: list[str] = field(default_factory=list)   # harfe çevrilemeyen gövde + nokta birleşimleri
    stray_marks: int = 0                                  # bağlanacak taban glif bulunamayan hareke


def _glyphs(page: pymupdf.Page, table) -> list[Glyph]:
    out = []
    for trace in page.get_texttrace():
        font = trace["font"]
        glyph_table = table.get(font, {})
        bold = "Bold" in font
        color = trace.get("color") or (0, 0, 0)
        rgb = (int(color[0] * 255) << 16) | (int(color[1] * 255) << 8) | int(color[2] * 255) if len(color) == 3 else 0
        known, owner = False, None
        rotated = tuple(round(v) for v in trace["dir"]) != (1, 0)
        for char, gid, origin, bbox in trace["chars"]:
            if gid < 0 and known:
                continue                   # tablodaki glifin karakter eşlemesindeki fazla karakter ("ْف")
            known = gid in glyph_table
            token, cx, cy = glyph_table.get(gid, ("T" + chr(char), 0.0, 0.0))
            if token == "Lا" and chr(char) == "l":
                token = "Tl"               # DejaVu'da "l" ile elif aynı glif
            size = trace["size"]
            glyph = Glyph(token[0], token[1:], origin[0], origin[1], bbox[2] - bbox[0], size, bold, rgb,
                          len(out), (origin[0] + cx * size, origin[1] - cy * size), rotated=rotated)
            if glyph.kind in "MD" and owner is not None:
                owner.marks.append(glyph)          # akışta harfin ardından gelen hareke ve nokta onundur
                continue
            owner = glyph if glyph.kind in "LS" else None
            out.append(glyph)
    return out


def _attach(bases: list[Glyph], marks: list[Glyph], report: Report) -> None:
    arabic = [b for b in bases if b.kind in "LS"]
    for mark in marks:
        mx = mark.ink[0]
        near = ([b for b in arabic if abs(b.y - mark.y) < b.size * 0.5]
                or [b for b in arabic if abs(b.y - mark.y) < b.size * 1.2])
        inside = [b for b in near if b.x - 0.3 <= mx <= b.x + b.width + 0.3]
        pool = inside or near
        if not pool:
            report.stray_marks += 1
            continue
        best = min(pool, key=lambda b: (abs(b.x + b.width / 2 - mx), abs(b.y - mark.y)))
        if mark.value == "۪" and (best.value in "يى" or best.value == "yeh"):
            # "۪" uzun "i"nin (ي) önündeki harfin altındadır; görsel olarak sağdaki komşu
            right = [b for b in near if b.y == best.y and b.x > best.x]
            best = min(right, key=lambda b: b.x) if right else best
        best.marks.append(mark)


def _letter(base: Glyph, report: Report) -> str:
    marks = sorted(base.marks, key=lambda m: m.order)
    dots = "".join(("a" if m.ink[1] < base.y - base.size * 0.2 else "b") + m.value for m in marks if m.kind == "D")
    if base.kind == "S":
        letter = _DOTTED.get((base.value, dots))
        if letter is None:
            report.unresolved.append(f"{base.value}+{dots}")
            letter = _DOTTED.get((base.value, ""), "?")
    else:
        letter = base.value
        if dots:
            report.unresolved.append(f"{letter}+{dots}")
    return letter + "".join(m.value for m in marks if m.kind == "M")


def _logical(cells: list[tuple[str, bool]], rtl: bool) -> tuple[str, list[tuple[int, int]]]:
    """Görsel sıradaki hücreler (metin, Arapça mı) -> mantıksal metin ve Arapça parçaların konumları."""
    def is_latin(cell):
        return bool(_LATIN.search(cell[0]))

    def flip(run: list[tuple[str, bool]]) -> list[tuple[str, bool]]:
        out, i = [], len(run) - 1
        while i >= 0:                                  # rakam dizileri soldan sağa kalır
            if run[i][0] in _ARABIC_DIGITS or run[i][0].isdigit():
                j = i
                while j - 1 >= 0 and (run[j - 1][0] in _ARABIC_DIGITS or run[j - 1][0].isdigit()):
                    j -= 1
                out += run[j:i + 1]
                i = j - 1
            else:
                text, ar = run[i]
                out.append((text.translate(_MIRROR), ar))
                i -= 1
        return out

    if rtl:
        # Satır Arapçadır: hepsi ters çevrilir, içindeki Latin parçalar (varsa) yeniden düzeltilir.
        flipped, out, i = flip(cells), [], 0
        while i < len(flipped):
            if is_latin(flipped[i]):
                j = i
                while j < len(flipped) and not flipped[j][1]:
                    j += 1
                out += [(c.translate(_MIRROR), a) for c, a in reversed(flipped[i:j])]
                i = j
            else:
                out.append(flipped[i])
                i += 1
        cells = out
    else:
        out, i = [], 0
        while i < len(cells):
            if cells[i][1] and cells[i][0] not in _ARABIC_DIGITS:
                j, last = i, i                         # parça: ilk Arapça harften Latin harfe kadar
                while j < len(cells) and not is_latin(cells[j]):
                    if cells[j][1]:
                        last = j
                    j += 1
                out += flip(cells[i:last + 1])
                i = last + 1
            else:
                out.append(cells[i])
                i += 1
        cells = out
    text, spans = "", []
    for chunk, ar in cells:
        if ar and chunk.strip():
            if spans and spans[-1][1] >= len(text.rstrip()) and not _LATIN.search(text[spans[-1][1]:]):
                spans[-1] = (spans[-1][0], len(text) + len(chunk))
            else:
                spans.append((len(text), len(text) + len(chunk)))
        text += chunk
    return text, spans


def _line(page_no: int, row: list[Glyph], report: Report) -> PdfLine:
    row.sort(key=lambda g: g.x)
    cells: list[tuple[str, bool]] = []
    prev = None
    for g in row:
        if prev is not None and g.x - (prev.x + prev.width) > g.size * 0.2 and not cells[-1][0].endswith(" ") \
                and g.value != " ":
            cells.append((" ", False))                # boşluk glifi olmayan aralık
        text = _letter(g, report) if g.kind in "LS" else g.value
        cells.append((text, g.arabic))
        prev = g
    latin = [g for g in row if g.kind == "T" and _LATIN.match(g.value)]
    rtl = len(latin) == 0 and any(g.kind in "LS" for g in row)
    text, spans = _logical(cells, rtl)
    lead = len(text) - len(text.lstrip())
    text = text.strip()
    spans = [(max(s - lead, 0), min(e - lead, len(text))) for s, e in spans]
    colors = defaultdict(int)
    for g in row:
        colors[g.color] += 1
    return PdfLine(page_no, row[0].y, row[0].x, row[-1].x + row[-1].width, text, max(g.size for g in row),
                   bool(latin) and sum(g.bold for g in latin) > len(latin) / 2,
                   max(colors, key=colors.get), rtl, spans)


def _rows(glyphs: list[Glyph], superscripts: bool = True) -> list[list[Glyph]]:
    """Taban glifleri satırlara toplar. Küçük puntolu üst simgeler ("(A.S.M.)", "(Hâşiye)" işareti) hemen
    altındaki satırın içine, kendi yatay konumlarına girer: "Ahmediye (A.S.M.) Risalesinde"."""
    rows: list[list[Glyph]] = []
    for g in sorted(glyphs, key=lambda g: (g.y, g.x)):
        if rows and abs(rows[-1][0].y - g.y) < 2.5:
            rows[-1].append(g)
        else:
            rows.append([g])
    rows = [r for r in rows if any(g.value.strip() for g in r)]
    out: list[list[Glyph]] = []
    for i, row in enumerate(rows):
        small = max(g.size for g in row) < 10 and not any(g.kind in "LS" for g in row)
        below = rows[i + 1] if i + 1 < len(rows) else None
        if superscripts and small and below and 0 < below[0].y - row[0].y < 15 and max(g.size for g in below) >= 10:
            below.extend(row)
            continue
        out.append(row)
    return out


def _cell(glyphs: list[Glyph], page_no: int, report: Report) -> str:
    """Hücre metni. Dar hücrede alt alta yazılmış harfler ("a/d/e/d") ve döndürülmüş yazı birleşir."""
    if glyphs and all(g.rotated for g in glyphs):
        return "".join(g.value for g in sorted(glyphs, key=lambda g: g.order)).strip()
    out, previous_letter = "", False
    for row in _rows(glyphs, superscripts=False):
        text = _line(page_no, row, report).text
        letter = len(text) == 1 and text.isalpha()
        out += text if letter and previous_letter else (" " if out else "") + text
        previous_letter = letter
    return out


def read_blocks(pdf_path, report: Report) -> list[PdfLine | PdfTable]:
    """Sayfa sırasıyla satırlar ve tablolar. Tablolar PyMuPDF'in çizgilerden bulduğu hücrelerdir; her hücrenin
    metni içine düşen gliflerden kurulur."""
    table = _table()
    doc = pymupdf.open(pdf_path)
    out: list[PdfLine | PdfTable] = []
    for page_no, page in enumerate(doc, 1):
        glyphs = _glyphs(page, table)
        bases = [g for g in glyphs if g.kind not in "MD"]
        _attach(bases, [g for g in glyphs if g.kind in "MD"], report)
        items: list[PdfLine | PdfTable] = []
        for found in page.find_tables().tables:
            box = pymupdf.Rect(found.bbox)
            inside = [g for g in bases if box.contains(pymupdf.Point(g.x + g.width / 2, g.y - g.size * 0.3))]
            bases = [g for g in bases if g not in inside]
            rows = []
            for row in found.rows:
                cells = []
                for cell in row.cells:
                    if cell is None:
                        continue
                    r = pymupdf.Rect(cell)
                    cells.append(_cell([g for g in inside
                                        if r.contains(pymupdf.Point(g.x + g.width / 2, g.y - g.size * 0.3))],
                                       page_no, report))
                if any(cells):
                    rows.append(cells)
            items.append(PdfTable(page_no, box.y0, rows))
        items += [_line(page_no, row, report) for row in _rows(bases)]
        out += sorted(items, key=lambda item: item.y)
    return out
