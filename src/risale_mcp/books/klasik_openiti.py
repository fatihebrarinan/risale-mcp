"""Klasik eserler, OpenITI (E2.3, `docs/e2-adaylar.md`): belâgat ve terim eserlerinin ayrıştırıcısı.

    uv run python -m risale_mcp.fetch klasik                  # data/raw/openiti/<eser>.txt
    uv run python -m risale_mcp.build delailul-icaz           # data/library/klasik/delailul-icaz.json

Okuma ortak OpenITI okuyucusuyla (`openiti.py`), paragraflar müfessirlerin eserlerindeki kuralla
(`books/openiti_writer.py`: kaynağın satırı yazarın paragrafı değildir, paragraf cümle sonunda biter). Kurallar ham
verinin incelemesinden (2026-11-13); her eserin sınırları `PLANS`'ta baskının kendi satırlarıyla yazılıdır, tahmin
edilmez, bulunamayan sınır kurulumu durdurur.

Başlıklar (Shamela sürümlerinde hepsi `### |`, tek seviye): baskının başlıklarıdır (muhakkikin koyduğu kenar
başlıkları dahil), alt başlıkta öyle işaretlidir. Ağaç düzdür: her başlık kökün altında bir bölüm açar, kimliği
sırasıdır (`delailul-icaz/12`). Ardışık başlık satırları ve başlıktan hemen önceki kısa, cümlesi bitmemiş satır
("فصل في") tek başlıktır.

**Metnin içine düşmüş başlık** (ham veride sık: Esrâr'da metindeki "الفصل" kelimesinin "فصل"i, Miftâh'ta mukaddimenin
"القسم الأول في علم الصرف، القسم الثاني…" sayımı başlık diye işaretlenmiş): başlık açık paragrafın cümlesi bitmeden
gelirse (son harf . ؟ ! : değil) ya da başlıktan sonraki satır noktalamayla sürüyorsa ("، …") başlık değil metindir:
paragrafa geri katılır, düğüm açmaz. Böylece hiçbir kelime düşmez; bedeli, böyle bir yerde gerçek bir başlık varsa
bölümün kaba kalmasıdır (`Report.inline`).

Numaralı başlık ("412 -"): muhakkikin fıkra numarası (Delâil'de Şâkir'in): `numbered` eserde o bölümün altında
düğümdür (`delailul-icaz/12/f412`, başlığı numara), öbürlerinde atılır (Müfredât'ın Shamela sürümündeki beyit
numaraları gibi).

Ön metin: muhakkikin girişi ayrı katmandır (`mukaddime-tahkik`, `authority: muhakkik`, `by`), müellife mal edilmez;
ilk satırlardaki Shamela künyesi (kitap, yazar, muhakkik, yayınevi) alınmaz. Arka metin (fihristler, baskının
kapanış satırı) alınmaz, `notes`'ta yazılıdır. Baskının harfli sayfa satırları ("- أ -"), "....." satırları,
Shamela'nın `</span>` artığı atılır.

Müfredât (JK sürümü, `parse_mufredat`): her madde "kök : …" diye başlayan paragraftır (madde başlığı ayrı satır
değil), harf kitapları "= كتاب الألف =" işaretiyle paragrafın sonuna düşmüştür ve biri (الخاء) yoktur. Bu yüzden harf
kitabı işaretten değil kökün ilk harfinden çıkar: bir paragraf ancak kökünün ilk harfi o anki harf kitabının harfi ya
da sıradaki harfse madde açar ("الخامس :", "قيل :", "وقوله :" gibi madde içi satırlar bu yüzden açmaz). Düğümler
`mufredat/<harf sırası>/<madde sırası>`, başlıkları kök ve harf kitabının adı. JK'nın satır işareti " | " ve
harf kitabı işaretleri metinden atılır; beyit yarımlarını ayıran "%" kaynağın yazdığı gibi kalır.
"""

import re
from dataclasses import dataclass, field

from risale_mcp import openiti
from risale_mcp.books.model import Book, Node
from risale_mcp.books.openiti_writer import Para, Report as _Report, Writer
from risale_mcp.catalog import Work
from risale_mcp.paths import RAW_DIR

BESMELE = "بسم الله الرحمن الرحيم"
EDITION_HEADING = "Başlık baskının"
NO_TITLE = "Başlık kaynakta yok: müellifin ilk bölümden önceki metni"
BOUNDARY = ".؟!:"
CLOSERS = " »”\")]'*"
CONTINUES = ("،", ",", ".", "؛", ":", ")", "»", "]", '"')
_NUMBERED = re.compile(r"^(\d+)\s*-\s*(\d*)$")
_JUNK = re.compile(r"^(?:-\s*\S{1,3}\s*-|\.{3,}|\|?\s*\+?\s*\*?)$")


@dataclass(frozen=True)
class Mark:
    """Ham verideki bir satır: `text` ile başlayan (`=` ile başlarsa tam eşit) `nth` eşleşme."""
    text: str
    nth: int = 1

    def find(self, P: list[openiti.Paragraph], start: int = 0) -> int:
        exact, want = self.text.startswith("="), self.text.lstrip("=")
        seen = 0
        for i in range(start, len(P)):
            t = _clean(P[i].text)
            if (t == want) if exact else t.startswith(want):
                seen += 1
                if seen == self.nth:
                    return i
        raise ValueError(f"sınır satırı bulunamadı: {self.text!r} ({self.nth}.)")


@dataclass(frozen=True)
class Plan:
    start: Mark                          # müellifin metninin ilk satırı
    intro: Mark | None = None            # muhakkikin girişinin ilk satırı (yoksa giriş yok)
    intro_title: str = "مقدمة التحقيق"
    end: Mark | None = None              # arka metnin ilk satırı (alınmaz)
    numbered: bool = False               # numaralı başlıklar fıkra düğümü
    preface: str | None = None           # ilk başlıktan önceki müellif metninin düğüm başlığı
    end_gap: str | None = None           # kaynağın son paragrafı eksikse açıklaması (`gaps`)
    notes: tuple[str, ...] = ()


PLANS: dict[str, Plan] = {
    "delailul-icaz": Plan(
        start=Mark("=" + BESMELE, 2), intro=Mark("=" + BESMELE, 1), intro_title="مقدمة",
        end=Mark("=الفهارس"), numbered=True,
        notes=("Muhakkikin (Şâkir) fıkra numaraları düğümdür (`f412`); Risâletü'ş-Şâfiye'de numaralar yeniden "
               "başlar. Muhakkikin dipnot işaretleri (\"منها1.\") metinde kalır; dipnotlar kaynakta yok (OpenITI "
               "temizliği).", "Baskının fihristleri (\"الفهارس\" ve sonrası) alınmadı.")),
    "esrarul-belaga": Plan(
        start=Mark("=" + BESMELE, 1),
        end_gap=("Bu sürüm son paragrafın ortasında biter (\"… فكنحو\"); başka baskıda (ShamAY0032338) devamı var, "
                 "o baskı farklı olduğu için alınmadı."),
        notes=("Başlıklar baskının (Medenî); muhakkik satırı sürümde boş.",)),
    "miftahul-ulum": Plan(
        start=Mark("=" + BESMELE, 1), end=Mark("بحمد الله وتوفيقه تم طبع كتاب"), preface="مقدمة المؤلف",
        notes=("Baştaki başlık satırı (\"كذلك نصرف الآيات لقوم يشكرون\", kapak) ve sondaki baskı kapanışı "
               "(\"بحمد الله وتوفيقه تم طبع كتاب…\") alınmadı.",)),
    "tarifat": Plan(
        start=Mark("=مقدمة"), end=Mark("=باب: الفهارس"),
        notes=("Baştaki \"المجلد الأول\" satırı ve sondaki fihrist (\"باب: الفهارس\") alınmadı.",)),
}


@dataclass
class Report(_Report):
    sections: int = 0
    fikra: int = 0
    inline: list[str] = field(default_factory=list)       # metne geri katılan "başlıklar"
    dropped: int = 0                                      # atılan numaralı ya da artık başlık satırları
    entries: int = 0                                      # Müfredât: madde düğümleri
    verses: int = 0                                       # tek beyit paragrafları


def _clean(text: str) -> str:
    return text.replace("</span>", "").strip()


def _ends(para: Para | None) -> bool:
    if para is None:
        return True
    tail = para.text.rstrip(CLOSERS)
    return not tail or tail[-1] in BOUNDARY


def _line(p: openiti.Paragraph, text: str) -> openiti.Paragraph:
    """Temizlenmiş metinli satır; sayfa sonları metnin boyuna kırpılır (artık atılınca konum kısalır)."""
    return openiti.Paragraph(p.raw, text, None, [], [(min(at, len(text)), page) for at, page in p.breaks],
                             p.page, p.end_page)


def _book(work: Work) -> Book:
    return Book(work.slug, work.title, {"group": str(work.group), "language": work.language,
                                        "source": {"site": str(work.source.site), "book": work.source.book}})


def parse(work: Work, raw_root=RAW_DIR / "openiti") -> tuple[Book, Report]:
    if work.slug == "mufredat":
        return parse_mufredat(work, raw_root)
    plan = PLANS[work.slug]
    doc = openiti.load(work.source.book, raw_root)
    P = doc.paragraphs
    report = Report()
    book = _book(work)
    w = Writer(book, report)
    start = plan.start.find(P)
    end = plan.end.find(P, start) if plan.end else len(P)
    for note in plan.notes:
        book.notes.append({"node_id": book.root.id, "after": None, "text": note})
    if plan.intro:
        intro = book.add_node(book.root, "mukaddime-tahkik", plan.intro_title,
                              subtitle=f"Muhakkikin girişi ({work.editor}): müellifin metni değil")
        intro.extra.update({"authority": "muhakkik", "by": work.editor})
        w.start(intro)
        asm = Assembler(w, report)
        for p in P[plan.intro.find(P):start]:
            text = _clean(p.text)
            if not text or _JUNK.match(text):
                if p.breaks:
                    asm.page(p)
                continue
            asm.add(_line(p, text), new=bool(p.level))       # girişin başlıkları kendi paragrafını açar
        w.flush()
    _body(book, w, report, P[start:end], plan, work)
    w.flush()
    if plan.end_gap:
        last = book.nodes()[-1]
        book.gaps.append({"node_id": last.id, "missing_blocks": 1, "after": None, "note": plan.end_gap})
    _printed_on_nodes(book)
    return book, report


class Assembler:
    """Paragraf kurma: kaynağın satırı baskının paragrafıdır; yalnız sayfa sınırında bölünmüşse (arada sayfa işareti
    var ve önceki satırın cümlesi bitmemiş) öncekine katılır. Metne geri katılan başlıkta boşluk kaynağa göredir."""

    def __init__(self, w: Writer, report: Report) -> None:
        self.w, self.report = w, report
        self.page_gap = False

    def page(self, p: openiti.Paragraph) -> None:
        if self.w.open is not None:
            self.w.open.add_break(p)
        self.page_gap = True

    def _append(self, line: openiti.Paragraph, sep: str) -> None:
        para = self.w.open
        shift = len(para.text) + len(sep)
        para.text += sep + line.text
        para.breaks += [(shift + at, str(page)) for at, page in line.breaks]
        para.end_page = line.end_page or para.end_page

    def add(self, line: openiti.Paragraph, sep: str | None = None, new: bool = False) -> None:
        """`sep` verilirse açık paragrafa o ayraçla eklenir (metne geri katılan başlık); `new` yeni paragraf açar.
        Tek beyit satırı kendi paragrafıdır (`poem`, `verse`): mısraları ayıran "..." cümleyi bölmez."""
        self.report.lines += 1
        if sep is None and _is_verse(line.text):
            self.w.flush()
            self.w._emit("poem", Para(line), verse=True)
            self.report.verses += 1
            self.page_gap = False
            return
        para = self.w.open
        if para is not None and not new and (sep is not None or (self.page_gap and not _ends(para))):
            self._append(line, sep if sep is not None else ("" if line.text[:1] in ".،:؛" else " "))
        else:
            self.w.flush()
            self.w.open = Para(line)
        self.page_gap = any(at >= len(line.text) - 1 for at, _ in line.breaks)


_VERSE = re.compile(r"\s(?:\.\.\.|…)(?:\s|$)")


def _is_verse(text: str) -> bool:
    """Tek beyit: iki mısra " ... " ile ayrılmış (ya da mısra "..." ile bitiyor), kısa satır."""
    return len(text.split()) <= 24 and len(_VERSE.findall(text)) == 1 and not text.rstrip().endswith((".", "؟", "!"))


def _glue_before(prev: Para | None) -> str:
    """Metne geri katılan başlığın önündeki ayraç: kelimenin parçası ("هذا ال" + "فصل") ya da açılış işaretinden
    sonra boşluksuz."""
    if prev is None:
        return " "
    tail = prev.text.rstrip()
    return "" if tail.endswith(("\"", "«", "(", "[")) or tail.split()[-1:] == ["ال"] else " "


def _body(book: Book, w: Writer, report: Report, P: list[openiti.Paragraph], plan: Plan, work: Work) -> None:
    asm = Assembler(w, report)
    title: list[tuple[openiti.Paragraph, str]] = []     # bekleyen başlık satırları
    carry: list[openiti.Paragraph] = []                 # yeni bölüme taşınacak satır (başlıktan önceki besmele)
    section: Node | None = None
    if plan.preface:
        section = book.add_node(book.root, "mukaddime", plan.preface, subtitle=NO_TITLE)
        w.start(section)
    else:
        w.start(book.root)

    def real(q: openiti.Paragraph) -> bool:
        return bool(_clean(q.text)) and not _JUNK.match(_clean(q.text))

    def is_heading(q: openiti.Paragraph) -> bool:
        return bool(q.level or q.entity) and real(q)

    def next_real(i: int) -> openiti.Paragraph | None:
        return next((q for q in P[i + 1:] if real(q)), None)

    def continues(q: openiti.Paragraph) -> bool:
        """Başlıktan sonraki satır metni sürdürüyor mu: Shamela'nın `</span>` artığıyla ya da noktalamayla başlıyor."""
        return q.text.lstrip().startswith("</span>") or _clean(q.text).startswith(CONTINUES)

    def open_section() -> None:
        nonlocal section
        report.sections += 1
        section = book.add_node(book.root, str(report.sections), " ".join(t for _, t in title).rstrip(" :"),
                                subtitle=EDITION_HEADING)
        title.clear()
        w.start(section)
        for c in carry:
            asm.add(c, new=True)
        carry.clear()

    def title_as_text(nxt: openiti.Paragraph | None) -> None:
        """Bekleyen "başlık" metnin parçasıydı: açık paragrafa geri katılır, ardından sonraki satır boşluksuz ya da
        boşlukla (kaynakta `</span>` harfe bitişikse boşluksuz)."""
        report.inline.append(" ".join(t for _, t in title))
        for k, (q, t) in enumerate(title):
            asm.add(_line(q, t), sep=_glue_before(w.open) if k == 0 else " ")
        title.clear()
        if nxt is not None:
            raw = nxt.text.lstrip()
            glued = raw.startswith("</span>") and raw[len("</span>"):][:1] not in ("", " ")
            text = _clean(nxt.text)
            asm.add(_line(nxt, text), sep="" if glued or text.startswith(CONTINUES) else " ")

    i = 0
    while i < len(P):
        p = P[i]
        i += 1
        text = _clean(p.text)
        if not real(p):
            if p.breaks:
                asm.page(p)
            if text and p.level:
                report.dropped += 1
            continue
        if title and p.text.lstrip().startswith("</span> ") and len(text.split()) <= 2 and text[-1] not in BOUNDARY:
            title.append((p, text))                   # Shamela'nın böldüğü başlık ("مقدمة" + "</span> المصنف")
            continue
        if title and continues(p):                    # başlık metnin parçasıydı
            title_as_text(p)
            continue
        if text == BESMELE and not title:
            if (n := next_real(i - 1)) is not None and is_heading(n):
                carry.append(_line(p, text))          # bölümün başındaki besmele o bölüme girer
            else:
                asm.add(_line(p, text), new=True)
            continue
        if is_heading(p):
            if m := _NUMBERED.match(text):
                if title:
                    open_section()
                if not plan.numbered:
                    report.dropped += 1
                    continue
                report.fikra += 1
                w.start(book.add_node(section or book.root, f"f{m[1]}", m[1], type="fikra", number=int(m[1])))
                asm.page_gap = False
                continue
            title.append((p, text))
            continue
        if len(text.split()) <= 3 and text[-1] not in BOUNDARY and (n := next_real(i - 1)) is not None \
                and is_heading(n) and not _NUMBERED.match(_clean(n.text)):
            title.append((p, text))                   # başlığın parçası ("فصل في", "في")
            continue
        if title:
            open_section()
        asm.add(_line(p, text))
    if title:                                         # sonda kalan başlık satırları metindir
        title_as_text(None)


def _printed_on_nodes(book: Book) -> None:
    """Düğümlere ilk paragrafının basılı sayfası. OpenITI'nin `PageV00P000` işareti sayfasız ön metindir (kapak,
    muhakkikin harfli sayfaları): sayfa değildir, atılır."""
    for r in book.paragraphs:
        if r.get("printed", {}).get("volume") == 0:
            del r["printed"]
        if r.get("page_breaks"):
            r["page_breaks"] = [b for b in r["page_breaks"] if not str(b[1]).startswith("0/")] or None
            if r["page_breaks"] is None:
                del r["page_breaks"]
    first: dict[str, dict] = {}
    for r in book.paragraphs:
        if r.get("printed") and r["node_id"] not in first:
            first[r["node_id"]] = r["printed"]
    for node in book.nodes():
        if node.id in first and node is not book.root:
            node.extra["printed"] = {k: first[node.id][k] for k in ("volume", "page")}


# ---------------------------------------------------------------- Müfredât

LETTERS = ("الألف", "الباء", "التاء", "الثاء", "الجيم", "الحاء", "الخاء", "الدال", "الذال", "الراء", "الزاي",
           "السين", "الشين", "الصاد", "الضاد", "الطاء", "الظاء", "العين", "الغين", "الفاء", "القاف", "الكاف",
           "اللام", "الميم", "النون", "الواو", "الهاء", "الياء")     # bu baskının sırası: و, ه'den önce
_FIRST = {"ا": 0, "أ": 0, "إ": 0, "آ": 0, "ء": 0, "ب": 1, "ت": 2, "ث": 3, "ج": 4, "ح": 5, "خ": 6, "د": 7, "ذ": 8,
          "ر": 9, "ز": 10, "س": 11, "ش": 12, "ص": 13, "ض": 14, "ط": 15, "ظ": 16, "ع": 17, "غ": 18, "ف": 19, "ق": 20,
          "ك": 21, "ل": 22, "م": 23, "ن": 24, "و": 25, "ه": 26, "ي": 27, "ى": 27}
_ENTRY = re.compile(r"^([ء-ي]{1,6})\s*:\s")
_KITAB = re.compile(r"\s*=\s*كتاب\s+\S+\s*=\s*")
_JK_LINE = re.compile(r"\s*\|\s*")
MUFREDAT_TITLE = "المفردات في غريب القرآن"
MUFREDAT_NOTES = (
    "Madde (kök) düğümü, paragrafın \"kök : …\" başlangıcından; harf kitabı kökün ilk harfinden (JK sürümünde harf "
    "kitabı işaretleri paragraf sonuna düşmüş, الخاء işareti yok). Kökün ilk harfi o anki harf kitabının harfi ya da "
    "sıradaki harf değilse paragraf madde açmaz, önceki maddede kalır.",
    "JK'nın satır işareti (\" | \") ve harf kitabı işaretleri (\"= كتاب الألف =\") metinden atıldı; beyit "
    "yarımlarını ayıran \"%\" kaynağın yazdığı gibidir. Muhakkikin girişi bu sürümde yok.",
)


def _letter(word: str) -> int | None:
    return _FIRST.get(word[0])


def parse_mufredat(work: Work, raw_root=RAW_DIR / "openiti") -> tuple[Book, Report]:
    P = openiti.load(work.source.book, raw_root).paragraphs
    report = Report()
    book = _book(work)
    w = Writer(book, report)
    for note in MUFREDAT_NOTES:
        book.notes.append({"node_id": book.root.id, "after": None, "text": note})
    w.start(book.add_node(book.root, "mukaddime", "مقدمة المؤلف", subtitle=NO_TITLE))
    asm = Assembler(w, report)
    current, kitab, count = -1, None, 0
    for p in P:
        text = _JK_LINE.sub(" ", _KITAB.sub(" ", p.text)).strip()
        if text.endswith(MUFREDAT_TITLE) and _KITAB.search(p.text):
            text = text[:-len(MUFREDAT_TITLE)].strip()       # harf kitabının başındaki kitap adı (sayfa başlığı)
        if not text:
            if p.breaks:
                asm.page(p)
            continue
        m = _ENTRY.match(text)
        letter = _letter(m[1]) if m else None
        if m and letter is not None and (letter == current or letter == current + 1) and current >= 0 or \
                (m and current == -1 and letter == 0):
            if letter != current:
                current, count = letter, 0
                kitab = book.add_node(book.root, f"{letter + 1:02d}", f"كتاب {LETTERS[letter]}",
                                      subtitle=EDITION_HEADING)
            count += 1
            report.entries += 1
            w.start(book.add_node(kitab, f"{count:03d}", m[1], type="madde"))
            asm.add(_line(p, text), new=True)
            continue
        asm.add(_line(p, text))
    w.flush()
    report.sections = current + 1
    _printed_on_nodes(book)
    return book, report
