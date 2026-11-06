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

Kapsam: eserin tamamı (MVP; pilotta Bakara 34'te durulurdu). Muhakkikin cilt sonu içindekiler listeleri ("محتوى
الجزء …") atlanır; kaynakta girişin önündeki "[الجزء الاول]" cilt etiketi `notes`'tadır.
Muhakkikin dipnot işaretleri («1») metinde kalır, dipnotlar kaynakta yoktur (`notes`).
"""

import re

from risale_mcp import openiti
from risale_mcp.books.model import Book
from risale_mcp.books.openiti_writer import Report, Writer as _Writer
from risale_mcp.catalog import Work
from risale_mcp.paths import RAW_DIR

TOC = "محتوى الجزء"                               # muhakkikin cilt sonu içindekiler listesi: metin değil, atlanır
INTRO = "مقدمة التحقيق"
KHUTBA = "خطبة الكتاب"
VOLUME_LABEL = "[الجزء الاول]"
EDITION_HEADING = "Başlık baskının (Maraşlî)"
INTRO_SUBTITLE = "Muhakkikin girişi (Muhammed Abdurrahman el-Maraşlî, 1418): müellifin metni değil"
INTRO_PARTS = {"أولا": "1", "ثانيا": "2"}         # girişin kendi içindekiler listesindeki iki ana kısım
FOOTNOTES_NOTE = "Muhakkikin dipnot işaretleri («1») metinde kalır; dipnotların kendisi kaynakta yok (OpenITI temizliği)."
SCOPE_NOTE = ("Eserin tamamı (MVP, 2026-11-06; pilot T3'te Bakara 33'e kadardı). Muhakkikin cilt sonlarındaki "
              "içindekiler listeleri (\"محتوى الجزء …\") metin değildir, alınmadı.")
BESMELE = "بسم الله الرحمن الرحيم"

_UNIT = re.compile(r"\[سورة (.+?) \((\d+)\) : (آية|الآيات)\s*#?\s*(\d+)(?:\s*(?:الى|إلى|إلي)\s*(\d+))?\s*\]")
_SURA = re.compile(r"^\((\d+)\)\s*(سورة .+?)\s*$")
_VERSE_NO = re.compile(r"\((\d+)\)")
_VERSE_LINE = re.compile(r"\(\d+\)\s*$")


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
                if sura_node is None or sura_node.number != sura:
                    raise ValueError(f"âyet birimi {sura}:{start} sûre başlığından önce")
                local = f"{start}" + (f"-{end}" if end != start else "")
                title = f"{m[3]} {start}" + (f" الى {end}" if end != start else "")
                unit = book.add_node(sura_node, local, title, subtitle=EDITION_HEADING)
                unit.extra["verses"] = {"sura": sura, "start": start, "end": end}
                w.start(unit)
                region = "text"
                i = _verse_lines(P, i, w, sura, start, end)
                report.units += 1
                continue
            if m := _SURA.match(text):
                sura_node = book.add_node(book.root, m[1], m[2], subtitle=EDITION_HEADING, number=int(m[1]))
                w.start(sura_node)
                region = "text"
                continue
            if text.startswith(TOC):                  # içindekiler: sonraki sûre ya da birim başlığına kadar atlanır
                region = "toc"
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
        if region == "toc":
            i += 1
            continue
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
