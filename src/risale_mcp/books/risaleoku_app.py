"""risaleoku.com'un yeni uygulamasının kitap dosyaları -> eser modeli.

Metin dosyası satır satırdır; işaret satırın başındadır, başlık ve imza satırları `>` ile kapanır:
    #5                sayfa (yalnızca sayfa sonunda bölünen paragrafı birleştirmek ve fihrist için; saklanmaz)
    <…>  &…>  €…>  ∑…>   ortalı başlıklar (`&` kitap ya da büyük bölüm, `€`, `∑` üst başlık)
    ` …>              iç başlık ("` Birinci Esas:>")
    ,…>               ortalı küçük satır; yalnızca süs olanlar ("* * *", "- - -") atılır
    ÷…>  §…>          imza
    {…}               hâşiye (birkaç satır sürebilir); eski baskılarda metnin içinde, işareti "(*)", "(Haşiye)"
    ~…|n@             Arapça satır; `n` meal kaydının numarası (boş olabilir) ya da mealin kendisi (Gençlik Rehberi)
    "   metin"        yeni paragraf (üç boşlukla ya da "  \\" ile başlar); bu baskılarda cümle ortasındaki satır da
                      girintili, kalın, küçük satır ya da boş satırdan sonra gelebilir (bkz. `_continues`)
    düz satır         önceki paragrafın devamı (sayfa sonundan ya da araya giren Arapçadan sonra)
    \\…>  ∫…>  £…>     satır içi kalın yazı: paragraf başındaysa etikettir ("\\Birinci Esas:>")
    ∫                 kapanışı yoksa paragrafın ilk harfi süsü; atılır
    ﹛…|﹜             metnin içinde alıntı (âyet); işaretler atılır

`footnotes` dosyası `sayfa|işaret|metin`: işaret o sayfadaki blokta aranır, metinden silinir, hâşiye oraya bağlanır.
Fihrist sekmeyle girintili `başlık[@ikinci ad]|sayfa`; sayfası olmayan girdi grup başlığıdır. Kökü kitabın adıdır.
Arapça türü (âyet/hadis) kaynakta işaretli değildir: `arabi`; âyetler `build_db`'de Kur'ân metninde bulunur.
"""

import gzip
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

from risale_mcp.books.model import ARABIC_SCRIPT, ArabicSpan, Book, FootnoteMark, Text
from risale_mcp.books.risaleoku import Block, TocEntry, _Heading, assemble
from risale_mcp.catalog import Group, Work
from risale_mcp.headings import parse_heading, parse_inline_label
from risale_mcp.normalize import match_words, slugify
from risale_mcp.sources import risaleoku_app as source

SOURCE_FIXES = (("âÚ§îkat", "Hakîkat"),)     # kaynaktaki bozuk kodlama (Âsâr-ı Bediiyye, Nutuk 7); metnin tek istisnası
WRONG_MEALS = {"فَلْيَشْهَدِ الثَّقَلَانِ اَنّ۪ى مُرْتَجِعٌ"}     # kaynakta başka bir mealin numarası yazılı (6509: "Gerçek hile…"); meal verilmez
_PAGE = re.compile(r"^#(\d+)\s*$")
_PRESENTATION = re.compile(r"[ﭐ-﷯ﹰ-ﻼ]+")   # Arapça harf biçimleri (Zülfikâr'ın Hizb'i): standart harfe çevrilir
_STRAY = str.maketrans("", "", "∫£~\\")
_ARABIC_LINE = re.compile(r"^~(.*)\|([^|]*)@\s*$", re.S)
_BOLD = re.compile(r"[\\∫£]([^>\n]*)>")
_INLINE_QUOTE = re.compile(r"﹛|\|?﹜")
_ORNAMENT = re.compile(r"^[\s*∗٭❋.\-–—_]*$")
_ARABIC_RUN = re.compile(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFC]"
                         r"(?:[\s\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFC]*"
                         r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFC])?")
_TERMINAL = tuple(".!?؟…:»”\"")
_FULL_STOP = tuple(".!?؟…")
_LOWER_START = re.compile(r"\s*[a-zçğıöşüâîû]")
HASIYE_REACH = 5        # hâşiye metni, işaretini taşıyan paragraftan en çok bu kadar sonra gelir (sayfa sonu)
_HASIYE_MARK = re.compile(r"^\s*(?:﴿\s*)?(\(\*+\)|\(H[âa]ş[iy]+e\)|\(حاشيه\))\s*:?\s*")
_ARTICLE = re.compile(r"^(NUTUK|MAKALE)\s*-\s*(\d+)$")
_PERIODICAL = re.compile(r"^(VOLKAN|İKDAM|SEBİL-ÜR REŞAD|MİZAN|SERBESTÎ)$")
_FRONT = re.compile(r"^(Risale-i Nur|Müellifi|Bed[iî]üzzaman Said|\(?Ve\)?$|Yahud$)")
_VERSE_END = re.compile(r"(?<=﴾)\s+(?=\S)")          # Hizblerde âyet numarası: her âyet ayrı paragraf
_MARKERS = {"<": "title", "&": "title", "€": "title", "∑": "title", "`": "label", ",": "small", "÷": "sign", "§": "sign"}


@dataclass
class AppBlock(Block):
    marker: str = ""       # başlık türü: title, label, small; düz paragrafta boş
    head: str = ""         # başlık satırının işareti (`&`, `<`, `€`, `∑`)
    last_page: int = 0     # paragraf sayfa sonunda sürüyorsa bittiği sayfa
    label: str = ""        # paragraf başındaki kalın etiket


def _plain(line: str) -> tuple[str, str]:
    """Satır içi işaretleri atar: (metin, paragraf başındaki kalın etiket)."""
    label = m[1].strip() if (m := _BOLD.match(line.strip())) else ""
    return re.sub(r"\s+", " ", _BOLD.sub(r" \1 ", line).translate(_STRAY).replace(">", " ")).strip(), label


def _text(line: str, language: str) -> Text:
    """Satırı metne çevirir; Türkçe metnin içindeki Arapça parçalar işaretlenir."""
    if language != "tr":
        return Text(line)
    return Text(line, [ArabicSpan(m.start(), m.end(), "arabi") for m in _ARABIC_RUN.finditer(line)])


def _append(block: Block, line: str, language: str) -> None:
    separator = "" if line[:1] in "-'’" else " "
    block.text = Text.join([block.text, _text(line, language)], separator)


def _attach(block: Block, mark: str, content: Text) -> bool:
    """Hâşiyeyi bloktaki işaretin yerine bağlar, işareti metinden siler. İşaret yoksa False."""
    start = block.text.text.find(mark) if mark else -1
    if start < 0:
        return False
    text = block.text
    while start > 0 and text.text[start - 1] == " ":
        start -= 1
    end = text.text.find(mark, start) + len(mark)
    shift = end - start

    def moved(i: int) -> int:
        return i - shift if i >= end else min(i, start)
    arabic = [ArabicSpan(moved(a.start), moved(a.end), a.kind, a.meal, a.source) for a in text.arabic]
    block.text = Text(text.text[:start] + text.text[end:], arabic,
                      [FootnoteMark(moved(f.offset), f.content) for f in text.footnotes] + [FootnoteMark(start, content)])
    return True


def _hasiye(blocks: list[Block], raw: str) -> None:
    """Hâşiye metni işaretin yerine bağlanır; sayfa sonunda geldiği için işaret birkaç paragraf önce olabilir."""
    body, _ = _plain(raw.strip("{} \n"))
    recent = [b for b in reversed(blocks) if not getattr(b, "marker", "")][:HASIYE_REACH]
    if not recent:
        return
    m = _HASIYE_MARK.match(body)
    mark = m[1] if m else ""
    text = Text(body[m.end():].strip(" ﴾") if m else body)
    if not any(_attach(b, mark, text) for b in recent):
        recent[0].text.footnotes.append(FootnoteMark(len(recent[0].text.text), text))


def _continues(tail: Block | None, text: str, line: str, language: str, after_page: bool) -> bool:
    """Yeni paragraf gibi yazılmış satır önceki cümleyi mi sürdürüyor? Türkçede küçük harf yeter (etiketin devamı
    da olur: "İkinci Bürhan'ın / beş noktası var:"); sayfa başında "," ya da ";" sonrası büyük harf de.
    Arapça ve Osmanlıcada harf büyüklüğü yok: sayfa başında, önceki satır bitmemişse."""
    if tail is None:
        return False
    marker, end = getattr(tail, "marker", ""), tail.text.text.rstrip()
    if end.endswith(_FULL_STOP) or end[-1:].isdigit():
        return False
    if language == "tr":
        if _LOWER_START.match(text):
            return not marker or marker == "label" and not end.endswith(":")
        return not marker and after_page and end.endswith((",", ";"))
    return (not marker and after_page and line.lstrip()[:1] not in ("[", "\\")
            and not end.endswith(_TERMINAL) and not end.endswith(")") and not tail.text.is_arabic())


def read_blocks(body: str, meals: dict[str, str], language: str, split_verses: bool = False) -> list[Block]:
    blocks: list[Block] = []
    page, open_paragraph, after_page = 0, False, False
    hasiye: str | None = None

    for wrong, right in SOURCE_FIXES:
        body = body.replace(wrong, right)
    body = _PRESENTATION.sub(lambda m: unicodedata.normalize("NFKC", m[0]), body)
    lines = _INLINE_QUOTE.sub("", body).split("\n")
    while lines:
        line = lines.pop(0).rstrip()
        if hasiye is not None:
            hasiye += " " + line.strip()
            if line.endswith("}"):
                _hasiye(blocks, hasiye)
                hasiye = None
            continue
        if not line.strip():
            open_paragraph = False             # boş satır paragrafı kapatır (Zülfikâr'ın Hizb'i)
            continue
        if m := _PAGE.match(line):
            page, after_page = int(m[1]), True
            continue
        if line.startswith("{"):
            if line.endswith("}"):
                _hasiye(blocks, line)
            else:
                hasiye = line
            continue
        if line.startswith("~") and lines and lines[0].strip() == "|@":       # kapanışı alt satıra düşmüş
            line += lines.pop(0).strip()
        if m := _ARABIC_LINE.match(line):
            arabic = re.sub(r"\s+", " ", m[1]).strip()
            meal = meals.get(m[2]) if m[2].isdigit() else _plain(m[2])[0] or None
            span = ArabicSpan(0, len(arabic), "arabi", None if arabic in WRONG_MEALS else meal)
            tail = blocks[-1] if blocks else None
            after_page = False
            if open_paragraph and tail and not tail.text.is_arabic() and not tail.text.text.endswith(_TERMINAL):
                tail.text = Text.join([tail.text, Text(arabic, [span])], " ")
            elif split_verses:
                for verse in _VERSE_END.split(arabic):
                    blocks.append(AppBlock(Text(verse, [ArabicSpan(0, len(verse), "arabi")]), page))
                open_paragraph = False
            else:
                blocks.append(AppBlock(Text(arabic, [span]), page))
                open_paragraph = True
            continue
        if line.lstrip()[0] in _MARKERS and ">" in line:   # girintili başlık ya da süs satırı
            line = line.lstrip()
        marker = _MARKERS.get(line[0])
        if marker and ">" in line:
            head, _, tail = line.partition(">")
            if tail.strip():                   # kapanıştan sonra metin süren satır
                lines.insert(0, "   " + tail.strip())
            plain, _ = _plain(head[1:])
            if marker == "small" and language == "tr" and blocks and _LOWER_START.match(plain) \
                    and _continues(blocks[-1], plain, line, language, after_page):
                _append(blocks[-1], plain, language)
                blocks[-1].last_page = page
                open_paragraph, after_page = True, False
                continue
            open_paragraph = after_page = False
            if not _ORNAMENT.match(plain):
                blocks.append(AppBlock(_text(plain, language), page, centered=marker != "sign",
                                       signature=marker == "sign", marker=marker, head=line[0]))
            continue
        if line.startswith((" ", "  \\")) or not open_paragraph:
            plain, label = _plain(line)
            if not plain:
                continue
            lower = language == "tr" and bool(_LOWER_START.match(plain))
            if _HASIYE_MARK.match(plain):                 # ayraçsız hâşiye: paragraf gibi yazılmış
                _hasiye(blocks, plain)
            elif (open_paragraph or lower) and blocks and (lower or not label) \
                    and _continues(blocks[-1], plain, line, language, after_page):
                _append(blocks[-1], plain, language)
                blocks[-1].last_page = page
                open_paragraph = True
            else:
                blocks.append(AppBlock(_text(plain, language), page, label=label))
                open_paragraph = True
            after_page = False
            continue
        _append(blocks[-1], _plain(line)[0], language)
        blocks[-1].last_page = page
        after_page = False
    return blocks


def add_footnotes(blocks: list[Block], lines: str, classify=None) -> list[str]:
    """`sayfa|işaret|metin` satırlarını bağlar; işareti bulunamayanları döndürür."""
    by_page: dict[int, list[Block]] = {}
    for block in blocks:
        for page in range(block.page, max(block.page, getattr(block, "last_page", 0)) + 1):
            by_page.setdefault(page, []).append(block)
    lost = []
    for line in lines.splitlines():
        page, mark, text = (line.split("|", 2) + ["", ""])[:3]
        if not page.isdigit() or not text:
            continue
        note = Text(_plain(text)[0])
        if not any(_attach(b, mark, note) for b in by_page.get(int(page), [])):
            lost.append(line[:60])
            if on_page := by_page.get(int(page)):
                on_page[-1].text.footnotes.append(FootnoteMark(len(on_page[-1].text.text), note))
    return lost


def read_toc(body: str) -> list[TocEntry]:
    """Fihrist; sayfası olmayan grup girdisi ilk alt girdisinin sayfasını alır. Kök (kitabın adı) atılır."""
    rows = []
    for line in body.splitlines():
        if not line.strip():
            continue
        depth = len(line) - len(line.lstrip("\t"))
        name, _, page = line.strip().rpartition("|") if "|" in line else (line.strip(), "", "")
        title, _, alt = name.partition("@")
        rows.append([depth, title.strip(), int(page) if page.isdigit() else None, "" if alt == "—" else alt.strip()])
    for i, row in enumerate(rows):
        if row[2] is None:
            row[2] = next((r[2] for r in rows[i + 1:] if r[2] is not None), 0)
    entries = [TocEntry(d, t, p, a) for d, t, p, a in rows]
    if entries and entries[0].depth == 0 and all(e.depth > 0 for e in entries[1:]):
        entries = entries[1:]
    return entries


def inline_starts(starts: dict[int, list[_Heading]], blocks: list[Block]) -> None:
    """Fihristin altındaki numaralı iç başlıklar ("` Birinci Nükte:>", "\\Birinci Esas:>" etiketi) düğüm açar.
    Aynı tür yeniden gelince kardeş olur. Yeni tür, açık seri aynı bölümde sürüyorsa onun içine, sürmüyorsa
    yanına girer (erisale'deki kural): "Birinci Hakikat"in "Esas"ları içeride, beş "Kâr"dan sonra "Hasaret" yanda."""
    def label_of(block: Block):
        marker = getattr(block, "marker", "")
        if marker == "label":
            return block.text.text, parse_inline_label(block.text.text)
        if marker == "title":
            info = parse_heading(block.text.text)
            return block.text.text, info if info.number else None
        return (block.label, parse_inline_label(block.label)) if getattr(block, "label", "") else (None, None)

    fixed = set(starts)
    labels = {}
    for i, block in enumerate(blocks):
        title, info = label_of(block)
        if i not in fixed and info and info.type:
            labels[i] = (title, info)

    def series_continues(at: int, info) -> bool:
        for k in range(at + 1, len(blocks)):
            if k in fixed:
                return False
            if k in labels and labels[k][1].type == info.type and info.number and (labels[k][1].number or 0) > info.number:
                return True
        return False

    base, section, opened = 1, None, []
    for i in range(len(blocks)):
        if i in fixed:
            base, section, opened = max(h.depth for h in starts[i]) + 1, parse_heading(starts[i][-1].title), []
            continue
        if i not in labels:
            continue
        title, info = labels[i]
        if section and (section.type, section.number) == (info.type, info.number):
            continue                                       # bölümün kendi başlığını tekrarlıyor
        same = next((k for k in range(len(opened) - 1, -1, -1) if opened[k].type == info.type), None)
        if same is not None:
            del opened[same:]
        else:
            while opened and not series_continues(i, opened[-1]):
                opened.pop()
        opened.append(info)
        starts[i] = [_Heading(base + len(opened) - 1, title.rstrip(":").strip())]


def title_entries(blocks: list[Block]) -> dict[int, list[_Heading]]:
    """Fihristi olmayan kitap (Zülfikâr): `&` birinci, öbür başlıklar ikinci seviye; künye satırları başlık değildir."""
    starts: dict[int, list[_Heading]] = {}
    for i, block in enumerate(blocks):
        if getattr(block, "marker", "") == "title" and not _FRONT.match(block.text.text):
            starts[i] = [_Heading(1 if block.head == "&" else 2, block.text.text)]
    return starts


def _slice(blocks: list[Block], first: str, stop: str | None) -> list[Block]:
    """Kitabın, başlığı `first` ile başlayan bloktan `stop` ile başlayan bloğa kadarki kısmı (başlıklar hariç)."""
    def at(title: str, after: int, top: bool) -> int:
        head = match_words(title)
        hits = [i for i in range(after, len(blocks)) if blocks[i].marker == "title"
                and match_words(blocks[i].text.text)[:len(head)] == head]
        if not hits:
            raise ValueError(f"başlık bulunamadı: {title}")
        return next((i for i in hits if top and blocks[i].head in "&€∑"), hits[0])
    start = at(first, 0, True)
    return blocks[start + 1:at(stop, start + 1, False) if stop else None]


def article_starts(blocks: list[Block]) -> tuple[list[Block], dict[int, list[_Heading]]]:
    """Nutuk ve Makalat: "<MAKALE - 5>" bölüm açar; ardından gelen ilk başlık satırı basılı adıdır, öbürleri
    (gazete, tarih) alt başlık. Metindeki öbür başlıklar alt bölümdür."""
    out: list[Block] = []
    starts: dict[int, list[_Heading]] = {}
    i = 0
    while i < len(blocks):
        block = blocks[i]
        title = getattr(block, "marker", "") == "title"
        m = _ARTICLE.match(block.text.text) if title else None
        if m:
            kind, number = m[1].capitalize(), int(m[2])
            rows, notes = [], []
            while i + 1 < len(blocks) and getattr(blocks[i + 1], "marker", "") in ("title", "small") \
                    and blocks[i + 1].page == block.page and not _ARTICLE.match(blocks[i + 1].text.text):
                i += 1
                line = blocks[i].text.text
                (rows if blocks[i].marker == "title" and not _PERIODICAL.match(line) else notes).append(line)
            name = rows[0] if rows else f"{kind} – {number}"
            out.append(AppBlock(Text(name), block.page, centered=True, marker="title"))
            starts[len(out) - 1] = [_Heading(1, name, subtitle=" · ".join(rows[1:] + notes),
                                             local=f"{slugify(kind)}-{number:02d}")]
        else:
            if title and not out:                                  # bölümün kendi adı ("Nutuklar")
                i += 1
                continue
            if title and not parse_heading(block.text.text).number:
                starts[len(out)] = [_Heading(2, block.text.text)]
            out.append(block)
        i += 1
    return out, starts


SHARH_BY = "Abdülmecid Nursî"
OUTLINES = Path(__file__).parent / "outlines"
MAX_CANDIDATES = 12
MAX_ALONE = 3
_AUTHOR_NOTE = re.compile(r"\s*(?:[(（]\s*المؤلف\s*[)）]|[-–ـ]\s*المؤلف\s*[-–ـ]?)\s*\.?\s*$")


ENDS_AT = {"isaratul-icaz-arabi": "باسمه سبحانه", "kizil-icaz-arabi": "اعتذار"}


def _ancestors(node_id: str) -> list[str]:
    parts = node_id.split("/")
    return ["/".join(parts[:k]) for k in range(1, len(parts) + 1)]


def _clean(words: list[str]) -> list[str]:
    return [w for w in words if not w.isdigit()]


def _anchor_words(text: str) -> list[str]:
    return _clean(match_words(text.replace("ـ", "")))


def _classify_author(note: str) -> tuple[str, str]:
    """"(المؤلف)" müellifin hâşiyesi, öbürleri muhakkik ve naşirin notu."""
    return ("hasiye", _AUTHOR_NOTE.sub("", note)) if _AUTHOR_NOTE.search(note) else ("note", note)


def _anchored(blocks: list[Block], outline: list[dict]) -> tuple[dict[int, list[dict]], list[str]]:
    """Şablondaki her düğümün metindeki yeri: kelime çapalarından biri, öncekinin ardında. (blok -> düğümler, bulunamayanlar)"""
    words, owner = [], []
    for i, block in enumerate(blocks):
        w = _anchor_words(block.text.text)
        words += w
        owner += [i] * len(w)
    index: dict[str, list[int]] = {}
    for at, word in enumerate(words):
        index.setdefault(word, []).append(at)

    def finds(anchor: list[str]) -> list[int]:
        return [at for at in index.get(anchor[0], ()) if words[at:at + len(anchor)] == anchor] if anchor else []

    def candidates(node: dict) -> list[int]:
        title = _anchor_words(node["title"])
        if start := _anchor_words(node.get("start", "")):        # şablonda bu baskının ilk kelimeleri verilmişse
            return finds(start)[:MAX_CANDIDATES]
        if printed := _anchor_words(node.get("printed", "")):    # şablonda bu baskının başlık satırı verilmişse
            return [at for at in finds(printed) if blocks[owner[at]].marker
                    and _anchor_words(blocks[owner[at]].text.text) == printed]
        headed = [at for at in finds(title) if len(title) >= 2 and blocks[owner[at]].marker
                  and _anchor_words(blocks[owner[at]].text.text)[:len(title)] == title]
        if headed:                              # başlık satırı en güvenilir yerdir
            return headed[:MAX_CANDIDATES]
        tries = [_clean(a) for a in node["anchors"]]
        found = [at for a in tries for at in finds(a)]
        if not found:                           # baskı farkı: çapanın dört kelimelik parçaları
            found = [at for a in tries for k in range(len(a) - 3) for at in finds(a[k:k + 4])]
        if not found and len(title) >= 2:
            found = finds(title)
        if not found and len(title) == 1:       # tek kelimelik risale adı ("حباب"); çok geçiyorsa alt başlıktır ("نكتة")
            alone = [at for at in finds(title) if blocks[owner[at]].marker
                     and _anchor_words(blocks[owner[at]].text.text) == title]
            found = alone if len(alone) <= MAX_ALONE else []
        return sorted(set(found))[:MAX_CANDIDATES]

    # Yanlış bir ileri eşleşme sonrakileri kaybettirmesin: en çok düğümü sıralı yerleştiren zincir seçilir.
    nodes = outline if outline[0]["anchors"] else outline[1:]
    best: list[tuple[int, int, tuple | None]] = []        # (zincir boyu, konum, önceki halka)
    for k, node in enumerate(nodes):
        for at in candidates(node):
            prior = max((c for c in best if c[1] <= at and c[3] < k), key=lambda c: c[0], default=None)
            best.append(((prior[0] if prior else 0) + 1, at, prior, k))
    chain = {}
    link = max(best, key=lambda c: c[0], default=None)
    while link:
        chain[link[3]] = link[1]
        link = link[2]
    # Yeri bulunamayan düğüm (kendi metni olmayan grup başlığı da) kendinden sonra yerleşen düğümle açılır.
    starts: dict[int, list[dict]] = {}
    lost, waiting = [], []
    for k, node in enumerate(nodes):
        waiting.append(node)
        if node["anchors"] and k not in chain:
            lost.append(node["id"])
        if k in chain:
            at = chain[k]
            starts.setdefault(owner[at] if at < len(owner) else len(blocks) - 1, []).extend(waiting)
            waiting = []
    if waiting:
        starts.setdefault(len(blocks) - 1, []).extend(waiting)
    return starts, lost


def parse_with_outline(work: Work, root: Path, classify=_classify_author, verses: bool = False) -> tuple[Book, list[str]]:
    """Aslı Arapça eserler: başlık ağacı ve kimlikler şablondan (`outlines/<eser>.json`; Türkçe eserle paralel),
    metin ve dipnotlar bu kaynaktan. Şablon ağacın ilk çapasından önceki kısım (muhakkikin ön sözü) alınmaz.
    `verses`: `<…>` satırları şerh edilen manzum metindir (Kızıl İcaz'da Süllem), `quote`."""
    key = work.source.book
    template = json.loads((OUTLINES / f"{work.slug}.json").read_text(encoding="utf-8"))
    book = Book(work.slug, work.title, {
        "group": str(work.group), "language": work.language,
        "source": {"site": str(work.source.site), "book": key},
    })
    book.notes += template["notes"]
    book.root.subtitle = template["outline"][0].get("subtitle", "")
    blocks = read_blocks(_read(root, key, "text").replace("|\n", "\n"), source.load_meals(root), work.language)
    report = add_footnotes(blocks, _read(root, key, "footnotes"))
    if work.source.sections:
        first, stop = work.source.sections
        blocks = _slice(blocks, first, stop or None)
    starts, lost = _anchored(blocks, template["outline"])
    if stop := ENDS_AT.get(work.slug):                  # sondaki eklemeler (talebelerin sözü, takriz…) alınmaz
        head = match_words(stop)
        last = max(starts)
        blocks = blocks[:next((i for i in range(last, len(blocks))
                               if match_words(blocks[i].text.text)[:len(head)] == head), len(blocks))]
    kept = {p for row in template["outline"] if row["id"] not in lost for p in _ancestors(row["id"])}
    nodes = {book.root.id: book.root}
    node, begun = book.root, False
    for i, block in enumerate(blocks):
        title_words = None
        for row in starts.get(i, ()):
            begun = True
            if row["parent_id"] is None or row["id"] not in kept:   # kökün kendi metni; bu baskıda bulunmayan bölüm
                continue
            fields = {k: row[k] for k in ("subtitle", "toc_title", "type", "number", "heading") if k in row}
            parent = nodes[row["parent_id"]]
            local = row["id"].removeprefix(parent.id + "/")
            node = nodes[row["id"]] = book.add_node(parent, local, row["title"], **fields)
            title_words = match_words(row["title"])
        if not begun or match_words(block.text.text) == title_words:
            continue
        kind = "signature" if block.signature else "quote" if verses and block.head == "<" else "paragraph"
        extra = {"center": True} if block.centered and kind == "paragraph" else {}
        record = book.add_paragraph(node, kind, block.text, **extra)
        for mark in block.text.footnotes:
            what, text = classify(mark.content.text)
            if what == "note":
                book.notes.append({"node_id": node.id, "after": record["id"], "text": text})
            else:
                book.add_hasiye(record["id"], node, mark.offset, Text(text),
                                commentator=SHARH_BY if what == "serh" else None)
    return book, [f"  işareti bulunamayan dipnot: {len(report)} {report[:2]}",
                  f"  çapası bulunamayan bölüm : {len(lost)} {lost[:6]}"]


def _read(root: Path, key: str, name: str) -> str:
    path = root / key / f"{name}.txt.gz"
    return gzip.open(path, "rt", encoding="utf-8").read() if path.exists() else ""


def parse_work(work: Work, root: Path) -> Book:
    key = work.source.book
    book = Book(work.slug, work.title, {
        "group": str(work.group), "language": work.language,
        "source": {"site": str(work.source.site), "book": key},
        **({"stops": "*"} if work.slug == "hizb-i-nuri" else {}),     # Hizb'in cümleleri "٭" ile ayrılır
    })
    if work.private:
        book.root.subtitle = work.note                     # sonradan derleme: kimin olduğu görünsün
    blocks = read_blocks(_read(root, key, "text"), source.load_meals(root), work.language,
                         split_verses=work.group is Group.HIZB)
    add_footnotes(blocks, _read(root, key, "footnotes"))
    entries = read_toc(_read(root, key, "toc"))
    if work.source.sections:
        first, stop = work.source.sections
        blocks = _slice(blocks, first, stop or None)
        blocks, articles = article_starts(blocks)
        return assemble(book, blocks, [], lambda starts, b: (starts.clear(), starts.update(articles), inline_starts(starts, b)))
    if not entries or len(entries) == 1:
        heads = title_entries(blocks)
        return assemble(book, blocks, [], lambda starts, b: (starts.clear(), starts.update(heads), inline_starts(starts, b)))
    return assemble(book, blocks, entries, inline_starts)
