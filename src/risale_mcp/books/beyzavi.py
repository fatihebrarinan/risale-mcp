"""Beyzâvî, Envârü't-Tenzîl: OpenITI Shamela0023588 (Maraşlî tahkiki) ayrıştırıcısı (T3, `docs/tefsir-altyapi-plani.md`).

    uv run python -m risale_mcp.fetch tefsir        # data/raw/openiti/beyzavi-shamela.txt
    uv run python -m risale_mcp.build beyzavi       # data/library/tefsir/beyzavi.json

Kararlar T2'dedir (kullanıcı onayladı); ham verinin incelemesi T1 (`data/interim/tefsir/beyzavi-t1.md`). Okuma ortak
OpenITI okuyucusuyla (`openiti.py`): işaretler atılır, harflere dokunulmaz, her satırın basılı sayfası bilinir.

Başlık ağacı:

    beyzavi                          Envârü't-Tenzîl
    beyzavi/mukaddime-tahkik         Maraşlî'nin girişi ("مقدمة التحقيق"): muhakkik katmanı (`authority`, `by`),
                                     müellifin metni değil. Alt düğümleri yalnız girişin kendi içindekiler listesinin
                                     iki ana kısmıdır ("أولا: …" -> `/1`, "ثانيا: …" -> `/2`); öbür başlık satırları
                                     tutarsız seviyelidir (liste maddeleri, tam cümleler), kendi paragraflarını açar
    beyzavi/hutbe                    müellifin hutbesi; başlığı ("خطبة الكتاب") baskının
    beyzavi/1, beyzavi/2             sûre ("(1) سورة الفاتحة" -> "سورة الفاتحة", numarası `number`'da); ilk âyet
                                     biriminden önceki metni ("مكية وآيها سبع آيات…") müellifindir
    beyzavi/2/6, beyzavi/1/3-4       âyet birimi: "[سورة البقرة (2) : آية 6]" başlığından ("آية 6", "الآيات 3 الى 4");
                                     `verses: {sura, start, end}`. Başlık çoğu yerde satırlara bölünmüştür
                                     ("### |" boş, "# 1]</span>"): "]" görülene kadar birleştirilir

Birimin başı: baskının âyet satırı (ya da satırları) "… (6)" `kind: "ayah"` paragrafıdır (kullanıcının kararı), âyet
aralığıyla (`verses: "quran:2:6"`); cümle sayılmaz (`sentences.split_paragraph`). Satırdaki numaralar birimin
aralığını tam karşılamazsa ayrıştırma durur (tahmin yok). Bakara'nın başındaki besmele satırı numarasız `ayah`'tır.

Paragraflar: kaynağın satırları yazarın paragrafı değildir (Shamela biçim kalıntısı, T1): paragraf yalnız cümle
sonunda (. ؟ !, ardından kapanış işaretleri olabilir) biter; öbür satırlar bir boşlukla eklenir, noktalamayla başlayan
satır boşluksuz. Girişte başlık satırı yeni paragraf açar. Her paragraf `printed` ve `page_breaks` taşır
(`books/printed.py` cümlelere dağıtır).

Kapsam: Bakara 34'ün başlığında durulur (pilot); kaynakta öncesinde "[الجزء الاول]" cilt etiketi `notes`'tadır.
Muhakkikin dipnot işaretleri («1») metinde kalır, dipnotlar kaynakta yoktur (`notes`).
"""

import re
from dataclasses import dataclass, field

from risale_mcp import openiti
from risale_mcp.books.model import Book, Node, Text
from risale_mcp.catalog import Work
from risale_mcp.paths import RAW_DIR

STOP = (2, 34)                                   # pilotun sonu: bu birimin başlığında durulur
INTRO = "مقدمة التحقيق"
KHUTBA = "خطبة الكتاب"
VOLUME_LABEL = "[الجزء الاول]"
EDITION_HEADING = "Başlık baskının (Maraşlî)"
INTRO_SUBTITLE = "Muhakkikin girişi (Muhammed Abdurrahman el-Maraşlî, 1418): müellifin metni değil"
INTRO_PARTS = {"أولا": "1", "ثانيا": "2"}         # girişin kendi içindekiler listesindeki iki ana kısım
FOOTNOTES_NOTE = "Muhakkikin dipnot işaretleri («1») metinde kalır; dipnotların kendisi kaynakta yok (OpenITI temizliği)."
SCOPE_NOTE = ("Pilot aralığı (T3): muhakkikin girişi, hutbe, Fâtiha ve Bakara 1–33. Bakara 34'ten sonrası "
              "ayrıştırılmadı.")
BESMELE = "بسم الله الرحمن الرحيم"

_UNIT = re.compile(r"\[سورة (.+?) \((\d+)\) : (آية|الآيات)\s*#?\s*(\d+)(?:\s*(?:الى|إلى)\s*(\d+))?\s*\]")
_SURA = re.compile(r"^\((\d+)\)\s*(سورة .+?)\s*$")
_VERSE_NO = re.compile(r"\((\d+)\)")
_VERSE_LINE = re.compile(r"\(\d+\)\s*$")
_ENDS = ".؟!"
_CLOSERS = "»”\")]' "
_LEADING_PUNCT = ".،:؛"


@dataclass
class Report:
    units: int = 0
    lines: int = 0                               # kaynağın metin satırları
    paragraphs: int = 0                          # birleştirilmiş paragraflar
    ayah_lines: int = 0
    pages: list[str] = field(default_factory=list)
    unknown_pages: int = 0


class _Para:
    """Açık paragraf: satırlar birleştikçe sayfa sonları kaydırılır."""

    def __init__(self, line: openiti.Paragraph) -> None:
        self.text = line.text
        self.page, self.end_page = line.page, line.end_page
        self.breaks = [(at, str(page)) for at, page in line.breaks]

    def ends_sentence(self) -> bool:
        tail = self.text.rstrip(_CLOSERS)
        return bool(tail) and tail[-1] in _ENDS

    def add(self, line: openiti.Paragraph) -> None:
        sep = "" if line.text[:1] in _LEADING_PUNCT else " "
        shift = len(self.text) + len(sep)
        self.text += sep + line.text
        self.breaks += [(shift + at, str(page)) for at, page in line.breaks]
        self.end_page = line.end_page or self.end_page

    def add_break(self, line: openiti.Paragraph) -> None:
        """Yalnız sayfa işaretinden oluşan satır: sayfa açık paragrafın şu anki sonunda biter."""
        self.breaks += [(len(self.text), str(page)) for _, page in line.breaks]


def _printed(page: openiti.Page | None, end: openiti.Page | None) -> dict | None:
    if page is None:
        return None
    return {"volume": page.volume, "page": page.page, **({"end": str(end)} if end and end != page else {})}


class _Writer:
    def __init__(self, book: Book, report: Report) -> None:
        self.book, self.report = book, report
        self.node: Node | None = None
        self.open: _Para | None = None

    def flush(self) -> None:
        if self.open is not None:
            self._emit("paragraph", self.open)
            self.open = None

    def _emit(self, kind: str, para: _Para, **extra) -> dict:
        printed = _printed(para.page, para.end_page)
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
        self.open = _Para(line)

    def ayah(self, lines: list[openiti.Paragraph], verses: str | None, note: str | None = None) -> None:
        self.flush()
        para = _Para(lines[0])
        for line in lines[1:]:
            para.add(line)
        self._emit("ayah", para, **({"verses": verses} if verses else {}), **({"note": note} if note else {}))
        self.report.ayah_lines += len(lines)


def _heading_text(paragraphs: list[openiti.Paragraph], i: int) -> tuple[str, int]:
    """Başlık metni ve son satırının sırası: "[سورة" açılıp "]" kapanmadıysa sonraki satırlar eklenir."""
    text, j = paragraphs[i].text, i
    if "[سورة" in text:
        while "]" not in text:
            j += 1
            text += " " + paragraphs[j].text
        text = text.replace("</span>", "")
        if text.split("]", 1)[1].strip():
            raise ValueError(f"âyet başlığından sonra metin var: {text!r}")
    return text.strip(), j


def _verse_range(sura: int, start: int, end: int) -> str:
    return f"quran:{sura}:{start}" + (f"-{end}" if end != start else "")


def parse(work: Work, key: str | None = None, raw_root=RAW_DIR / "openiti") -> tuple[Book, Report]:
    doc = openiti.load(key or work.source.book, raw_root)
    P = doc.paragraphs
    report = Report()
    book = Book(work.slug, work.title, {"group": str(work.group), "language": work.language,
                                        "source": {"site": str(work.source.site), "book": work.source.book}})
    w = _Writer(book, report)
    intro = book.add_node(book.root, "mukaddime-tahkik", INTRO, subtitle=INTRO_SUBTITLE)
    intro.extra.update({"authority": "muhakkik", "by": work.editor})
    book.notes.append({"node_id": book.root.id, "after": None, "text": SCOPE_NOTE})
    book.notes.append({"node_id": intro.id, "after": None, "text": FOOTNOTES_NOTE})
    w.start(intro)
    region, sura_node = "front", None
    i = 0
    while i < len(P):
        p = P[i]
        if p.level or p.entity:
            text, j = _heading_text(P, i)
            i = j + 1
            if not text:
                continue
            if m := _UNIT.search(text):
                sura, start, end = int(m[2]), int(m[4]), int(m[5] or m[4])
                if (sura, start) >= STOP:
                    break
                if sura_node is None or sura_node.number != sura:
                    raise ValueError(f"âyet birimi {sura}:{start} sûre başlığından önce")
                local = f"{start}" + (f"-{end}" if end != start else "")
                title = f"{m[3]} {start}" + (f" الى {end}" if end != start else "")
                unit = book.add_node(sura_node, local, title, subtitle=EDITION_HEADING)
                unit.extra["verses"] = {"sura": sura, "start": start, "end": end}
                w.start(unit)
                i = _verse_lines(P, i, w, sura, start, end)
                report.units += 1
                continue
            if m := _SURA.match(text):
                sura_node = book.add_node(book.root, m[1], m[2], subtitle=EDITION_HEADING, number=int(m[1]))
                w.start(sura_node)
                region = "text"
                continue
            if text == KHUTBA:
                w.start(book.add_node(book.root, "hutbe", KHUTBA, subtitle=EDITION_HEADING))
                region = "text"
                continue
            if text == INTRO:
                region = "intro"
                continue
            if region == "intro" and (part := INTRO_PARTS.get(text.split(":", 1)[0].strip())):
                w.start(book.add_node(intro, part, text))
                continue
            if region == "intro":                     # tutarsız seviyeli başlık satırı: kendi paragrafını açar
                w.line(openiti.Paragraph(p.raw, text, None, [], p.breaks, p.page, p.end_page), force_new=True)
                continue
            raise ValueError(f"tanınmayan başlık: {text!r}")
        if region == "front" and p.text == VOLUME_LABEL:
            book.notes.append({"node_id": intro.id, "after": None, "text": f"Kaynakta girişin önünde cilt etiketi: {VOLUME_LABEL}"})
        else:
            w.line(p)
        i += 1
    w.flush()
    pages = sorted({(r["printed"]["volume"], r["printed"]["page"]) for r in book.paragraphs if r.get("printed")})
    report.pages = [f"{v}/{n}" for v, n in (pages[0], pages[-1])] if pages else []
    for node in book.nodes():
        first = next((r for r in book.paragraphs if r["node_id"] == node.id and r.get("printed")), None)
        if node.extra.get("verses") and first:
            node.extra["printed"] = {k: first["printed"][k] for k in ("volume", "page")}
    return book, report


def _verse_lines(P: list[openiti.Paragraph], i: int, w: _Writer, sura: int, start: int, end: int) -> int:
    """Birimin başındaki âyet satırları; aralığın bütün numaraları görülünce biter. Sıradaki satırın sırasını döndürür."""
    want, seen = set(range(start, end + 1)), set()
    while seen != want:
        if i >= len(P) or P[i].level:
            raise ValueError(f"{sura}:{start}-{end}: âyet satırı eksik (görülen {sorted(seen)})")
        line = P[i]
        i += 1
        if not line.text:                              # yalnız sayfa işareti
            continue
        if line.text == BESMELE and not seen:
            w.ayah([line], None, note="sûre başı besmele")
            continue
        numbers = {int(n) for n in _VERSE_NO.findall(line.text)}
        if not _VERSE_LINE.search(line.text) or not numbers or not numbers <= want - seen:
            raise ValueError(f"{sura}:{start}-{end}: beklenmeyen âyet satırı {line.text[:80]!r}")
        seen |= numbers
        w.ayah([line], _verse_range(sura, min(numbers), max(numbers)))
    return i
