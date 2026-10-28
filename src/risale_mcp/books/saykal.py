"""Saykalü'l-İslâm (İhsan Kasım es-Sâlihî tahkiki) Word dosyaları ve Ta'likat'ın Türkçesi -> eser modeli.

Saykal dosyaları İşârâtü'l-İ'câz'ınki gibi basılı kitabın düz dökümüdür ("صيقل الإسلام/قزل إيجاز - ص: 163"
sayfa satırları, "_____" çizgisinden sonra sayfa dipnotları); sayfa ve dipnot işleri `books/rasaelalnour.py`
ile ortaktır. Muhakkikin ön sözleri her eserde alınmaz (kökte bir notla belirtilir).

Kızıl İcaz (Arapça): Ahdarî'nin manzum mantık metni Süllem'e hâşiyedir. Üç katman vardır:
- Kalın satırlar Süllem'in beyitleridir; kelimelerinde "[1]" numaraları durur. Müellifin değildir: `quote`.
- "[1] …" satırları ve "اعلم!" ile başlayan uzun bahisler müellifin hâşiyesidir; eserin asıl metni.
- Sayfa dipnotları müellifin kardeşi Molla Abdülmecid'in şerhidir: hâşiye gibi bağlı olduğu cümleye bağlanır
  ve okunur, ama `commentator` taşır (kimlik `…/s1`, atıf "› Şerh ›"); müellife mal edilmez (kullanıcının
  isteği). Abdülmecid'in mukaddimesi ve sondaki i'tizârı alınmaz.
"[n]" numaraları hâşiye ile beytin kelimesini eşleştirir; metinde kalır. Bölümler Süllem'in "فصل …"
başlıklarıdır (`fasl-01`…); ilk fasıldan önceki beyitler "ديباجة" düğümüdür: başlığı kaynakta yoktur, alt
başlığında `OUR_TITLE` yazar.

Ta'likat (Arapça ve Türkçe): Gelenbevî'nin Burhân'ına hâşiye; molla Habib'in derste tuttuğu notlar.
- Bölümler Burhân'ın bölüm başlarıdır: müellif onları "[فصل في الكليّ والجزئي]" gibi köşeli ayraçla
  alıntılar (Türkçede "﴾Mutlak olarak yüklem faslı…vs.﴿" ya da ortalı başlık). İki dilde aynı kimlik
  (`TALIKAT_SECTIONS`); sırayla aranır, Burhân'dan alıntı yalnız başına bir satırsa başlıktır, değilse
  paragraf başındaki satır içi başlıktır.
- Arapçada dipnotlar müellifin satır arası ve "(تقرير)" hâşiyeleridir; Badıllı'nın Burhân sayfa
  göndermeleri ("كلنبوي ص/3 س/22") ve "ع. ب" notları nottur.
- Türkçe (Protranslate tercümesi, Keşif Yolculukları programı): Word dipnotları hâşiyelerin tercümesidir;
  köşeli ayraçlı açıklamalar ve Badıllı/Gelenbevî kaynak notları nottur. "[Sayfa: 34]" satırları atılır
  (sayfa sonunda bölünen paragraf birleşir); "-A. B.-" Badıllı'nın tercümesini işaretler, not olur.

Hutbe-i Şamiye (Arapça): İhsan Kasım'ın Türkçe metinden tercümesi (1911'deki Arapça aslı değil; kullanıcı
"İhsan Kasım tercümesi" diye işaretlenerek alınmasını istedi). Bölümler Türkçe eserin bölümleriyle aynı
kimliği taşır (`HUTBE_SECTIONS`, Türkçe başlıktan bulunur). Dipnotta "المؤلف" müellifin hâşiyesi,
"المترجم" ve öbürleri not.
"""

import json
import re
from dataclasses import dataclass
from pathlib import Path

from risale_mcp.books import mesnevi_arabi
from risale_mcp.books.model import Book, Node, Text
from risale_mcp.books.rasaelalnour import ORDINALS, Line, Report, Row, _key, join_pages, pages, read_rows
from risale_mcp.catalog import Work

_MASKED = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
_UNMASKED = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")


def _book(work: Work) -> Book:
    return Book(work.slug, work.title, {
        "group": str(work.group), "language": work.language,
        "source": {"site": str(work.source.site), "book": work.source.book},
    })


def lines(rows: list[Row], report: Report, mask: bool = False) -> list[Line]:
    """Sayfa satırları atılmış, dipnotları bağlanmış satırlar. `mask`: "[1]" numaraları dipnot işareti sanılmasın
    diye geçici olarak Arapça rakamla yazılır."""
    if mask:
        rows = [Row(re.sub(r"\[(\d+)\]", lambda m: f"[{m[1].translate(_MASKED)}]", r.text), r.align, r.bold)
                for r in rows]
    out = join_pages(pages(rows, report), report, weight=True)
    if mask:
        unmask = lambda t: re.sub(r"\[([٠-٩]+)\]", lambda m: f"[{m[1].translate(_UNMASKED)}]", t)   # noqa: E731
        for line in out:
            line.text = unmask(line.text)
            line.marks = [(o, unmask(n)) for o, n in line.marks]
    return out


OUR_TITLE = "Bu başlık kaynakta yoktur; bölümü ayırmak için konuldu."


def _attach(book: Book, node: Node, record: dict | None, marks, classify) -> None:
    """Dipnotlar: `classify(not)` -> ("hasiye", metin), ("serh", metin) ya da ("note", metin)."""
    for offset, note in marks:
        kind, text = classify(note)
        if kind in ("hasiye", "serh"):
            parent = record["id"] if record else node.id
            book.add_hasiye(parent, node, offset if record else 0, Text(text),
                            commentator=SHARH_BY if kind == "serh" else None)
        else:
            book.notes.append({"node_id": node.id, "after": record["id"] if record else None, "text": text})


def _emit(book: Book, node: Node, line: Line, classify, kind: str = "paragraph", **extra) -> dict:
    record = book.add_paragraph(node, kind, Text(line.text), **extra)
    _attach(book, node, record, line.marks, classify)
    return record


def _ordinal(word: str) -> int | None:
    return ORDINALS.get(_key(word).rstrip(":"))


# ---------------------------------------------------------------- Kızıl İcaz

KIZIL_EXCLUDED = ("Muhakkikin notu (\"ملاحظة\"), Molla Abdülmecid'in mukaddimesi ve i'tizârı esere dahil edilmedi. "
                  "Sayfa dipnotları Abdülmecid Nursî'nin şerhidir; bağlı oldukları cümlenin şerhi olarak durur. "
                  "Süllem'in beyitleri (kalın) Ahdarî'nindir, müellifin değildir.")
SHARH_BY = "Abdülmecid Nursî"
_HASIYE_HEAD = re.compile(r"^\[\d+\]\s*")
_KIZIL_SUBSECTIONS = {"انواع الدلالات الوضعية": "delalet", "مقدمة في المحرفات": "muharrefat"}


def parse_kizil_icaz(work: Work, rows: list[Row]) -> tuple[Book, Report]:
    book, report = _book(work), Report()
    book.notes.append({"node_id": book.root.id, "after": None, "text": KIZIL_EXCLUDED})
    keys = [_key(r.text) for r in rows]
    start = keys.index("ايضاح")
    sharh = lambda note: ("serh", note)   # noqa: E731
    node = izah = book.add_node(book.root, "izah", rows[start].text)
    fasl, phase = 0, "izah"
    for line in lines(rows[start + 1:], report, mask=True):
        key = _key(line.text).strip()
        if phase == "izah":
            _emit(book, izah, line, sharh, "signature" if key == "سعيد" else "paragraph")
            if key == "سعيد":
                phase = "skip"
            continue
        if phase == "skip":                    # muhakkikin notu ve Abdülmecid'in mukaddimesi
            if not (line.bold and "[1]" in line.text):
                continue
            phase = "matn"
            node = book.add_node(book.root, "dibace", "ديباجة", subtitle=OUR_TITLE)
        if line.bold and key == "اعتذار":       # Abdülmecid'in i'tizârı: eser burada biter
            break
        if line.bold and key.startswith("فصل"):
            fasl += 1
            fasl_node = node = book.add_node(book.root, f"fasl-{fasl:02d}", line.text.strip(), type="Fasıl",
                                             number=fasl)
            _attach(book, node, None, line.marks, sharh)
            continue
        if line.bold and (local := _KIZIL_SUBSECTIONS.get(re.sub(r"[ًٌٍَُِّْ]", "", key))):
            node = book.add_node(fasl_node, local, line.text.strip())
            _attach(book, node, None, line.marks, sharh)
            continue
        hasiye = _HASIYE_HEAD.match(line.text) or re.match(r"^[وثم\s]*[اأ]علم", key)
        kind = "quote" if line.bold and not hasiye else "paragraph"
        _emit(book, node, line, sharh, kind)
    return book, report


# ---------------------------------------------------------------- Ta'likat

@dataclass(frozen=True)
class Section:
    local: str
    arabic: str           # Arapça satırın başı (harekesiz, köşeli ayraçsız)
    arabic_title: str
    turkish: str          # Türkçe satırın başı
    turkish_title: str
    turkish_ours: bool = False   # Türkçe başlık kaynakta yok (alt başlıkta `OUR_TITLE`)


TALIKAT_SECTIONS = (
    Section("kulli-ve-cuzi", "فصل في الكلي والجزئي", "فصل في الكليّ والجزئي",
            "KÜLLÎ VE CÜZÎ HAKKINDA", "Küllî ve Cüzî Hakkında Bir Fasıl"),
    Section("mukaddime", "مقدمة", "مقدمة", "ÖNSÖZ", "Önsöz"),
    Section("zati-ve-arizi", "فصل في الذاتي والعرضي", "فصل في الذّاتيّ والعرضي",
            "ZÂTÎ VE ÂRIZÎ HAKKINDA", "Zâtî ve Ârızî Hakkında Fasıl"),
    Section("hadd", "باب الحد", "باب الحدّ", "[Tariften kastedilen şey", "Hadd Bâbı", turkish_ours=True),
    Section("kaziyye", "باب القضايا", "باب القضايا", "ÖNERMELER BÖLÜMÜ", "Önermeler Bölümü… Kaziye"),
    Section("hamliyye", "فصل الحملية مطلقا", "فصل الحملية مطلقاً", "Mutlak olarak yüklem faslı",
            "Mutlak Olarak Yüklem Faslı"),
    Section("udul-ve-tahsil", "فصل في العدول والتحصيل", "فصل في العدول والتّحصيل",
            "Vazgeçme (değilleme) ve tahsil etme hakkında fasıl", "Vazgeçme ve Tahsil Etme Hakkında Fasıl"),
    Section("sartiyye", "فصل الشرطية", "فصل الشرطيّة", "Şartlı önerme bölümü", "Şartlı Önerme Bölümü"),
    Section("aks", "فصل في العكس", "فصل في العكس", "Akiste fasıl", "Akiste Fasıl"),
    Section("aks-i-nakiz", "فصل في عكس النقيض", "فصل في عكس النقيض", "Ters Döndürme hakkında bölüm",
            "Ters Döndürme Hakkında Bölüm"),
    Section("edille", "الباب الرابع", "الباب الرابع: في الادلة والحجج", "Dördüncü Bâb", "Dördüncü Bâb: Deliller",
            turkish_ours=True),
)
HEADING_WORDS = 8          # Burhân'dan alıntı bundan kısaysa ve ardından metin gelmiyorsa başlıktır
TALIKAT_EXCLUDED = ("Muhakkikin ön sözü ve Abdülmecid Nursî'nin yazmadaki notları (İhsan Kasım'ın tercümesiyle) "
                    "esere dahil edilmedi.")
_EDITOR = re.compile(r"كلنبو|ع\s*\.\s*ب\b")


def _talikat_note(note: str) -> tuple[str, str]:
    return ("note", note) if _EDITOR.search(note) else ("hasiye", note)


def _strip_lemma(text: str) -> str:
    return " ".join(re.sub(r"[\[\]﴾﴿:.…]|الخ|vs\.?", " ", text).split())


def parse_talikat_arabic(work: Work, rows: list[Row]) -> tuple[Book, Report]:
    book, report = _book(work), Report()
    book.notes.append({"node_id": book.root.id, "after": None, "text": TALIKAT_EXCLUDED})
    keys = [_key(r.text) for r in rows]
    start = keys.index("بسم الله الرحمن الرحيم")
    node, pending = book.root, list(TALIKAT_SECTIONS)
    for line in lines(rows[start:], report):
        key = _key(line.text).lstrip("[ ").strip()
        if pending and key.startswith(_key(pending[0].arabic)) and (pending[0].local != "mukaddime" or line.bold):
            section = pending.pop(0)
            after = line.text.rsplit("]", 1)[1] if "]" in line.text else ""
            standalone = not after.strip(" :.") and len(_strip_lemma(line.text).split()) <= HEADING_WORDS
            node = book.add_node(book.root, section.local, section.arabic_title,
                                 **({} if standalone else {"heading": "inline"}))
            if standalone:
                _attach(book, node, None, line.marks, _talikat_note)
                continue
        _emit(book, node, line, _talikat_note)
    if pending:
        raise ValueError(f"Ta'likat (Arapça): bulunamayan bölümler {[s.local for s in pending]}")
    return book, report


TURKISH_START = "Rahmân ve Rahîm Olan Allah’ın Adıyla"
TURKISH_END = "(Allah’ın inayetiyle) -Bitti-"
_PAGE = re.compile(r"^\[Sayfa:\s*\d+\]$")
_AB = re.compile(r"\s*[-–]\s*A\.\s*B\.\s*[-–]\s*(?:\(Abdülkadir Badıllı\))?\s*$")
AB_NOTE = "Bu kısım Abdülkadir Badıllı'nın tercümesidir (-A. B.-)."
TURKISH_EXCLUDED = ("Türkçe metin Protranslate'in tercümesidir (Keşif Yolculukları Risale-i Nur Eğitim Programı, "
                    "Ediz Sözüer); \"-A. B.-\" işaretli kısımlar Abdülkadir Badıllı'nın tercümesi. Kitabın tanıtım "
                    "yazıları, Gelenbevî'nin biyografisi ve ek bölümler esere dahil edilmedi.")
_TRANSLATOR = re.compile(r"Badıllı|Gelenbevî|kaynak adresi|^\[.*\]\.?$", re.S)


def _talikat_turkish_note(note: str) -> tuple[str, str]:
    return ("note", note) if _TRANSLATOR.search(note.strip()) else ("hasiye", note)


def parse_talikat_turkish(work: Work, docx: Path) -> tuple[Book, Report]:
    book, report = _book(work), Report()
    book.notes.append({"node_id": book.root.id, "after": None, "text": TURKISH_EXCLUDED})
    paras, footnotes = mesnevi_arabi.read(docx, Path("/nonexistent"), mesnevi_arabi.Report())
    texts = [p.text for p in paras]
    start = texts.index(TURKISH_START)
    end = next(i for i in range(start, len(texts)) if texts[i].startswith(TURKISH_END))
    body: list[Line] = []
    page_break = False
    for p in paras[start:end + 1]:
        if _PAGE.match(p.text):
            page_break = True
            continue
        marks = [(o, footnotes[i]) for o, i in p.marks if i in footnotes]
        report.footnotes += len(marks)
        if _AB.fullmatch(p.text) or p.text.strip() in ("-A. B.-", "- A. B. -"):
            if body:
                body[-1].marks.append((len(body[-1].text), AB_NOTE))
            continue
        text = p.text
        if m := _AB.search(text):              # paragraf sonundaki "-A. B.-"
            text = text[:m.start()]
            marks = [(min(o, len(text)), n) for o, n in marks] + [(len(text), AB_NOTE)]
        align = {"center": "center", "right": "end"}.get(p.align, "start")
        prev = body[-1] if body else None
        if page_break and prev and align == "start" and prev.align == "start" and text[:1].islower():
            shift = len(prev.text) + 1         # sayfa sonunda bölünen paragraf
            prev.text = f"{prev.text} {text}"
            prev.marks += [(o + shift, n) for o, n in marks]
            report.joined += 1
        else:
            body.append(Line(text, align, p.bold, marks=marks))
        page_break = False
    node, pending = book.root, list(TALIKAT_SECTIONS)
    for line in body:
        if pending and _strip_lemma(line.text).startswith(_strip_lemma(pending[0].turkish)):
            section = pending.pop(0)
            standalone = line.align == "center"
            node = book.add_node(book.root, section.local, section.turkish_title,
                                 **({} if standalone else {"heading": "inline"}),
                                 **({"subtitle": OUR_TITLE} if section.turkish_ours else {}))
            if standalone:
                _attach(book, node, None, line.marks, _talikat_turkish_note)
                continue
        _emit(book, node, line, _talikat_turkish_note, **({"center": True} if line.align == "center" else {}))
    if pending:
        raise ValueError(f"Ta'likat (Türkçe): bulunamayan bölümler {[s.local for s in pending]}")
    return book, report


# ---------------------------------------------------------------- Hutbe-i Şamiye (Arapça)

HUTBE_TRANSLATED = "İhsan Kasım es-Sâlihî'nin tercümesi (Türkçe metinden; 1911'de okunan Arapça aslı değil)"
HUTBE_EXCLUDED = "Muhakkikin (İhsan Kasım) \"بين يدي هذه الرسالة\" ön sözü esere dahil edilmedi."
_AUTHOR = re.compile(r"[\s.\-–]*المؤلف\s*\.?\s*$")


@dataclass(frozen=True)
class HutbeSection:
    arabic: str                     # basılı başlık (harekesiz)
    turkish: str | None             # Türkçe eserdeki bölümün başlığının başı; yoksa `local`
    parent: str | None = None       # Türkçe başlık (üst bölüm); yoksa kök
    subtitle: bool = False          # sonraki kalın satır alt başlıktır
    local: str | None = None
    bold: bool = True


HUTBE_SECTIONS = (
    HutbeSection("مقدمة", "Arabî Hutbe‑i Şâmiye’nin Mukaddimesidir", subtitle=True),
    HutbeSection("نهج رسائل النور", "Gayet Mühim Bir Suâle", subtitle=True),
    HutbeSection("اولاها:", "Birincisi", "Gayet Mühim Bir Suâle"),
    HutbeSection("الحالة الرهيبة الثانية لعصرنا الحالي:", "Bu Asırda İkinci Dehşetli Hâl", "Gayet Mühim Bir Suâle"),
    HutbeSection("الخطبة الشامية", "Arabî Hutbe‑i Şâmiye Eserinin Tercümesi"),
    HutbeSection("اما انه مستعد للرقي المعنوي:", "Birinci Cihet", "Birinci Kelime"),
    HutbeSection("الجهة الثانية: ان الاسلام مستعد للرقي المادي:", "İkinci Cihet", "Birinci Kelime"),
    HutbeSection("الذيل الاول", "Arabî Hutbe‑i Şâmiye’nin Zeyli’nin", subtitle=True),
    HutbeSection("ذيل الذيل", "Hutbe‑i Şâmiye’nin Zeylinin Zeyli"),
    HutbeSection("لتحيا الشريعة الغراء", "Yaşasın Şerîat‑ı Garrâ", "Hutbe‑i Şâmiye’nin Zeylinin Zeyli"),
    HutbeSection("حقيقة", "Hakikat", "Hutbe‑i Şâmiye’nin Zeylinin Zeyli"),
    HutbeSection("صدى الحقيقة", "Sadâ‑yı Hakikat", "Hutbe‑i Şâmiye’nin Zeylinin Zeyli"),
    HutbeSection("\"فقرة تركتها من \"فهرس المقاصد\" المنشور\"", None, "Hutbe‑i Şâmiye’nin Zeylinin Zeyli",
                 local="fihristul-makasid-fikrasi"),
    HutbeSection("لتحيا الشريعة الاحمدية", "Yaşasın Şerîat‑ı Ahmedî", "Hutbe‑i Şâmiye’nin Zeylinin Zeyli"),
    HutbeSection("رد الاوهام", "Reddü'l‑Evhâm", "Hutbe‑i Şâmiye’nin Zeylinin Zeyli"),
    HutbeSection("اخي رئيس التحرير!", "Biraderim Başmuharrir", "Hutbe‑i Şâmiye’nin Zeylinin Zeyli"),
    HutbeSection("القطعة الاخيرة", "Hutbe‑i Şâmiye’nin Birinci Zeylinin Zeylinden", "Hutbe‑i Şâmiye’nin Zeylinin Zeyli",
                 subtitle=True, bold=False),
    HutbeSection("الى جنودنا الاشاوس", "Kahraman Askerlerimize", "Hutbe‑i Şâmiye’nin Zeylinin Zeyli"),
    HutbeSection("خطاب الى الجنود", "Asâkire Hitâb", "Hutbe‑i Şâmiye’nin Zeylinin Zeyli"),
)
_KELIME = re.compile(r"^الكلمة\s+(\S+)$")
_VEHIM = re.compile(r"^الوهم\s+(\S+?)\s*:$")


def _hutbe_note(note: str) -> tuple[str, str]:
    return ("hasiye", _AUTHOR.sub("", note)) if _AUTHOR.search(note) else ("note", note)


def _turkish_ids(path: Path) -> dict[str, str]:
    """Türkçe Hutbe'nin başlıkları -> yerel kimlik yolu ("zeyl/reddul-evham")."""
    data = json.loads(path.read_text(encoding="utf-8"))
    root = data["outline"][0]["id"]
    return {n["title"]: n["id"].removeprefix(root + "/") for n in data["outline"][1:]}


def parse_hutbe(work: Work, rows: list[Row], turkish: Path) -> tuple[Book, Report]:
    book, report = _book(work), Report()
    book.root.subtitle = HUTBE_TRANSLATED
    book.notes.append({"node_id": book.root.id, "after": None, "text": HUTBE_EXCLUDED})
    ids = _turkish_ids(turkish)

    def turkish_id(prefix: str) -> str:
        found = [i for t, i in ids.items() if t == prefix] or [i for t, i in ids.items() if t.startswith(prefix)]
        if len(found) != 1:
            raise ValueError(f"Hutbe-i Şamiye: Türkçe başlık {prefix!r} {len(found)} bölümde")
        return found[0]

    nodes: dict[str, Node] = {}

    def open_path(path: str, title: str, **fields) -> Node:
        parent_path, _, local = path.rpartition("/")
        parent = nodes[parent_path] if parent_path else book.root
        nodes[path] = book.add_node(parent, local, title, **fields)
        return nodes[path]

    keys = [_key(r.text) for r in rows]
    start = keys.index("مقدمة")
    node, title_block, want_subtitle = book.root, 0, False
    for line in lines(rows[start:], report):
        key = _key(line.text).strip()
        if title_block:                         # ikinci kapak: "تأليف … إحسان قاسم الصالحى"
            title_block -= 1
            continue
        if want_subtitle and line.bold or want_subtitle and key == "من ذيل الذيل":
            node.subtitle = line.text.strip()
            want_subtitle = False
            _attach(book, node, None, line.marks, _hutbe_note)
            continue
        want_subtitle = False
        section = next((s for s in HUTBE_SECTIONS if key == _key(s.arabic) and line.bold == s.bold), None)
        if section:
            path = turkish_id(section.turkish) if section.turkish else \
                f"{turkish_id(section.parent)}/{section.local}"
            node = open_path(path, line.text.strip())
            want_subtitle = section.subtitle
            if key == "الخطبة الشامية":
                title_block = 4
            _attach(book, node, None, line.marks, _hutbe_note)
            continue
        if line.bold and (m := _KELIME.match(key)) and (n := _ordinal(m[1])):
            node = open_path(f"{turkish_id('Arabî Hutbe‑i Şâmiye Eserinin Tercümesi')}/kelime-{n:02d}",
                             line.text.strip(), type="Kelime", number=n)
            want_subtitle = True
            continue
        if line.bold and (m := _VEHIM.match(key)) and (n := _ordinal(m[1])):
            node = open_path(f"{turkish_id('Reddü')}/vehim-{n:02d}", line.text.strip().rstrip(":"),
                             type="Vehim", number=n)
            _attach(book, node, None, line.marks, _hutbe_note)
            continue
        kind = "signature" if key in ("سعيد النورسي", "بديع الزمان") else "paragraph"
        if key in ("* * *", "***"):
            continue
        _emit(book, node, line, _hutbe_note, kind)
    return book, report


def parse(work: Work, docx: Path, turkish: Path | None = None) -> tuple[Book, Report]:
    if work.slug == "kizil-icaz-arabi":
        return parse_kizil_icaz(work, read_rows(docx))
    if work.slug == "talikat-arabi":
        return parse_talikat_arabic(work, read_rows(docx))
    if work.slug == "talikat":
        return parse_talikat_turkish(work, docx)
    if work.slug == "hutbe-i-samiye-arabi":
        return parse_hutbe(work, read_rows(docx), turkish)
    raise ValueError(f"{work.slug} için Saykal ayrıştırıcısı yok")
