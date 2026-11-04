"""Rumuzat-ı Semaniye: nurpedia.org'un sayfaları -> eser modeli (kullanıcının kararı, 2026-11-04).

Kaynak: `Risale:Rumuzat-ı_Semaniye` dizin sayfasının bağlantı verdiği dört metin sayfası, nurpedia'nın sırasıyla
(`PAGES`): Yirmi Dokuzuncu Mektub'un Üçüncü, Dördüncü ve Sekizinci Kısmı ve Yirmi Sekizinci Mektub'un Yedinci
Mes'elesinden bir parça. Fihrist sayfası alınmaz (içindekiler). Sayfanın baskısı belirtilmemiştir; bu metin
kullanıcının PDF'inden (eski kaynak, `books/rumuzat.py`) daha geniş, ayrı bir baskıdır. HTML okuyucu
`books/nurpedia_html.py`.

Kurallar:
- Her sayfa kökün bir bölümüdür; Yirmi Dokuzuncu Mektub'un kısımları Mektubat'la aynı kimlikleri taşır
  (`kisim-03`, `kisim-04`, `kisim-08`), Yirmi Sekizinci Mektub'un parçası `mektub-28-mesele-07`. Sekizinci Kısım'ın
  sayfa başlığı "RUMUZAT-I SEMANİYE"dir; bölümün adı metindeki "Yirmi Dokuzuncu Mektub'un Sekizinci Kısmı"
  satırıdır, o satır metne girmez.
- Başlıklar (`<h1>`…`<h6>`) bölüm açar, ağaç seviyelerden kurulur. Kaynağın seviyesi yer yer kardeşleriyle
  tutmaz; düzeltmeler `LEVEL_FIXES`'tedir. Başlıktan hemen sonra gelen açıklayıcı başlık (`SUBTITLES`) alt
  başlıktır. Kimlik türden ve numaradan (`mesele-01`, `silsile-04`), numarasız başlıkta adından gelir.
- **Bölüm kimlikleri eski kaynakla aynı kalır** (kullanıcının kararı): eski kimlik adla tutmuyorsa `ID_FIXES`
  verir; eskiden olmayan bölümler yeni kimlik alır. Eski kaynakta başlığı olmayan iki toplayıcı bölüm korunur:
  Sekizinci Kısım'ın Birinci Remzi nurpedia'da başlıklıdır; İkinci Nükte'nin tetimmesi (Lafz-ı Resul
  silsilelerinin sahife listesi) nurpedia'da başlıksızdır, `tetimme` adı eski kaynaktandır (alt başlıkta yazılı).
  Yeni baskıda yeri değişen eski bölümler `ALIASES`'tadır: eser JSON'unda `aliases`, veritabanında `node_aliases`;
  araçlar eski kimliği yenisine çözer.
- Paragraf: `<p>` ve her madde (`<li>`). Tamamı Arapça olan blok `arabic`. Arapça satırdan sonra küçük harfle
  süren blok ("Sahife iki yüz seksen beşte (285)" / Arapça / "âyeti, sahife…") `continued` taşır.
- Hâşiye: metindeki dipnot işareti ve sayfa sonundaki notun metni; işaretin konumuna bağlanır. "(Hâşiyenin
  Hâşiyesi)" notun içinde kalır.
- Kaynağın düzeltilmemiş şablon artığı ("{{Arabi|") metinden atılır, `notes`'a yazılır.
- **Tablolar** (kullanıcının kararı ve sorumluluğuyla): nurpedia Yedinci Remz'in tablolarını resim olarak verir
  (sûre listesi, cüz cüz İsm-i Celal cetvelleri, ekleri). Her resim dizisinin yerine, eski kaynakta (kullanıcının
  PDF'i) o dizinin önündeki ve ardındaki paragrafların arasında kalan ve nurpedia'da karşılığı olmayan
  paragraflar (tablolar ve PDF'in tablo satırı parçaları) konur; `source_edition: "pdf"` taşır. Cüz başlıkları
  ("Birinci Cüz") resmin yazısıdır, bölüm açmaz: PDF'in tabloları birkaç cüzü birlikte verir.
- Arapçanın türü kaynakta işaretli değildir: `arabi`. Âyet ve hadisler `arabic_kinds` ile bulunur.
"""

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from risale_mcp.books.model import ArabicSpan, Book, Node, Text, TextBuilder
from risale_mcp.books.nurpedia_html import Block, Heading, Image, Page, arabic_pieces, parse_page
from risale_mcp.books.rumuzat import label_info
from risale_mcp.catalog import Work
from risale_mcp.headings import HeadingInfo, local_id, parse_heading, parse_inline_label
from risale_mcp.normalize import fold, match_words, parse_ordinal, slugify

PAGES = (                    # (sayfa, bölümün yerel kimliği, bölümün adı); sıra `sources.nurpedia.TEXTS`'deki
    ("Risale:29._Mektubun_3._Kısmı", "kisim-03", None),
    ("Risale:29._Mektubun_4._Kısmı", "kisim-04", None),
    ("Risale:29._Mektubun_8._Kısmı_(Rumuzat-ı_Semaniye)", "kisim-08", "Yirmi Dokuzuncu Mektub'un Sekizinci Kısmı"),
    ("Risale:28._Mektubun_7._Meselesinden", "mektub-28-mesele-07", None),
)
_K8 = "rumuzat-i-semaniye/kisim-08"
# (sayfanın bölümü, başlık, kaynaktaki seviye) -> doğru seviye. Üçüncü Remiz'de "Birinci Kısım" ve letafetleri
# bir seviye derindedir (kardeşi "İkinci Kısmı" H4), "Mühim Bir İhtar" İkinci Kısım'ın içindedir (eski kaynak).
LEVEL_FIXES: dict[tuple[str, str, int], int] = {
    (_K8, "Birinci Kısım", 5): 4,
    **{(_K8, f"{n} Letafet", 6): 5 for n in ("Birinci", "İkinci", "Üçüncü", "Dördüncü")},
    (_K8, "Mühim Bir İhtar", 4): 5,
}
SUBTITLES = {"Kenzü'l-Arş Duası'nın Feyzinden Gelen Bir Nükte-i Kur'aniye",
             "Kenzü'l-Arş Duası'nın Feyzinden Gelen Üçüncü Nükte-i İ'caziye"}
# (ebeveynin kimliği, başlık) -> yerel kimlik: eski kaynağın kimliği
ID_FIXES: dict[tuple[str, str], str] = {
    ("rumuzat-i-semaniye/kisim-04/nukte-01", "Silsile Harici Küçük Tevafukat"): "silsileden-baska-kucuk-tevafukat",
    (f"{_K8}/remiz-07/parca-03", "Yedinci Remzin Üçüncü Parçasının İkinci Küçük Kısmı"): "kisim-02",
}
# Kaynakta başlığı olmayan, eski kaynaktan gelen bölüm: (sayfanın bölümü, önüne girdiği başlık) ->
# (seviye, yerel kimlik, başlık, alt başlık)
INSERTED = {
    ("rumuzat-i-semaniye/kisim-04", "Birinci Silsile-i Lafz-ı Resul"): (
        3, "tetimme", "İkinci Nüktenin Tetimmesi",
        "Bu başlık nurpedia'da yoktur; eski kaynaktaki (kullanıcının PDF'i) adıdır."),
}
# Paragraf başındaki etiket yalnız bu türlerde bölüm açar ("Birinci Esas: …"; eski kaynağın bölümleri)
INLINE_TYPES = {"Esas"}
_SUBTITLES = {fold(t) for t in SUBTITLES}
# Yeni baskıda yeri değişen eski bölümler: eski kimlik -> yeni kimlik (`aliases`; araçlar eskisini yenisine çözer)
ALIASES = {
    f"{_K8}/remiz-01/zeyl": (f"{_K8}/remiz-02/zeyl",
                             "Eski kaynakta Birinci Remiz'in altındaydı; nurpedia'da İkinci Remz'in zeylidir."),
    **{f"{_K8}/remiz-05/makam-01/mesele-{n:02d}": (
        f"{_K8}/remiz-05/makam-01/maksat/bab-01/mesele-{n:02d}",
        "Eski kaynakta Birinci Makam'ın altındaydı; nurpedia'da Maksat › Birinci Bab'ın altındadır.")
       for n in (1, 2, 3)},
}
_INLINE = re.compile(r"^([^:]{3,40}):")
CAPTION = re.compile(r"^[\wÇĞİÖŞÜçğıöşüâîû ]+ Cüz$")
TEMPLATE = re.compile(r"\{\{\s*\w+\s*\|")
CHAIN = 8                         # çapa için en çok bu kadar paragraf geriye ya da ileriye bakılır
MIN_SHARED = 0.5                  # nurpedia'da karşılığı var sayılan PDF paragrafının ortak 5'li oranı


@dataclass
class Report:
    pages: list[tuple[str, int | None]] = field(default_factory=list)
    hasiye: int = 0
    unmatched_notes: list[str] = field(default_factory=list)
    tables: int = 0
    table_runs: list[str] = field(default_factory=list)
    templates: int = 0
    used: set = field(default_factory=set)            # yeri bulunan eski kaynak paragrafları


def _text(block: Block) -> tuple[Text, list[int]]:
    """Blok metni ve dipnot işaretlerinin metindeki konumları."""
    builder = TextBuilder()
    marks = dict.fromkeys(i for i, _ in block.notes)
    offsets = {}
    for i, run in enumerate(block.runs):
        if i in marks:
            offsets[i] = builder._length
        for piece, arabic in arabic_pieces(run):
            builder.add(TEMPLATE.sub("", piece), ArabicSpan(0, 0, "arabi") if arabic else None)
    end = builder._length
    text = Text.from_builder(builder)
    positions = [min(offsets.get(i, end), len(text.text)) for i, _ in block.notes]
    return text, positions


def _grams(text: str) -> set:
    words = match_words(text)
    return {tuple(words[i:i + 5]) for i in range(max(len(words) - 4, 0))} or ({tuple(words)} if words else set())


class Tree:
    def __init__(self, book: Book) -> None:
        self.book = book
        self.stack: list[tuple[int, Node]] = []

    def section(self, node: Node) -> None:
        self.stack = [(1, node)]

    @property
    def node(self) -> Node:
        return self.stack[-1][1]

    def heading(self, level: int, title: str, page_node: Node, local: str | None = None, **fields) -> Node:
        level = LEVEL_FIXES.get((page_node.id, title, level), level)
        while len(self.stack) > 1 and self.stack[-1][0] >= level:
            self.stack.pop()
        parent = self.node
        info = parse_heading(title)
        if info.type is None and (found := label_info(title, strict=False)):
            info = found
        local = local or ID_FIXES.get((parent.id, title)) or local_id(info, title, False)
        node = self.book.add_node(parent, local, title, type=info.type, number=info.number,
                                  heading=fields.pop("heading", f"H{level}"), **fields)
        self.stack.append((level, node))
        return node


def parse(work: Work, root: Path, pdf_book: dict | None = None) -> tuple[Book, Report]:
    """`root`: nurpedia ham verisi (`data/raw/nurpedia/metin/<eser>/`). `pdf_book`: eski kaynağın JSON'u
    (tabloların yeri için)."""
    report = Report()
    book = Book(work.slug, work.title, {"group": work.group, "language": work.language,
                                        "source": {"site": "nurpedia", "pages": [p for p, _, _ in PAGES]}})
    tree = Tree(book)
    pdf_items = _pdf_items(pdf_book) if pdf_book else []
    for title, local, name in PAGES:
        page = parse_page((root / f"{title}.html").read_text(encoding="utf-8"), title)
        report.pages.append((title, page.revision))
        blocks = page.blocks
        h1 = next(b for b in blocks if isinstance(b, Heading))
        section_title = name or h1.text
        section = book.add_node(book.root, local, section_title, heading="H1",
                                url=f"https://www.nurpedia.org/wiki/{title}",
                                **({"toc_title": h1.text} if name and fold(name) != fold(h1.text) else {}))
        tree.section(section)
        _fill(book, tree, section, blocks[blocks.index(h1) + 1:], page, name, pdf_items, report)
    known = {n.id for n in book.nodes()}
    for old, (new, note) in ALIASES.items():
        if new not in known or old in known:
            raise ValueError(f"takma ad tutmuyor: {old} -> {new}")
    book.meta["aliases"] = [{"old": old, "new": new, "note": note} for old, (new, note) in ALIASES.items()]
    return book, report


def _fill(book: Book, tree: Tree, section: Node, blocks: list, page: Page, name: str | None,
          pdf_items: list[dict], report: Report) -> None:
    previous_arabic = False
    pending_subtitle = False
    nurpedia_grams = set().union(*(_grams(b.text) for b in blocks if isinstance(b, Block)))
    i = 0
    while i < len(blocks):
        block = blocks[i]
        if isinstance(block, Heading):
            if CAPTION.match(block.text) and i + 1 < len(blocks) and isinstance(blocks[i + 1], Image):
                i += 1                                      # resmin yazısı: bölüm açmaz
                continue
            if fold(block.text) in _SUBTITLES:          # kaynakta Besmele araya girebilir
                tree.node.subtitle = block.text
                i += 1
                continue
            if inserted := INSERTED.get((section.id, block.text)):
                level, local, title, subtitle = inserted
                tree.heading(level, title, section, local, subtitle=subtitle, heading="none")
            tree.heading(block.level, block.text, section)
            pending_subtitle = True
            previous_arabic = False
            i += 1
            continue
        pending_subtitle = False
        if isinstance(block, Image):
            run_end = i
            while run_end < len(blocks) and (isinstance(blocks[run_end], Image) or (
                    isinstance(blocks[run_end], Heading) and CAPTION.match(blocks[run_end].text))):
                run_end += 1
            before = [b for b in reversed(blocks[:i]) if isinstance(b, Block)]
            after = [b for b in blocks[run_end:] if isinstance(b, Block)]
            start = i - 1 if i and isinstance(blocks[i - 1], Heading) and CAPTION.match(blocks[i - 1].text) else i
            captions = {n for b in blocks[start:run_end] if isinstance(b, Heading) and (n := _cuz(b.text))}
            _tables(book, tree.node, before, after, nurpedia_grams, pdf_items, report,
                    [b.src for b in blocks[i:run_end] if isinstance(b, Image)], captions)
            i = run_end
            previous_arabic = False
            continue
        if name and fold(block.text) == fold(name):          # Sekizinci Kısım'ın adı: başlık oldu
            i += 1
            continue
        if TEMPLATE.search(block.text):
            report.templates += 1
            book.notes.append({"node_id": tree.node.id, "text": "Kaynaktaki şablon artığı atıldı: "
                               + TEMPLATE.search(block.text).group()})
        text, positions = _text(block)
        if not text.text:
            i += 1
            continue
        if (label := _INLINE.match(text.text)) and (info := parse_inline_label(label[1])) and info.type in INLINE_TYPES:
            sibling = next((n for lvl, n in reversed(tree.stack) if n.type == info.type and n.heading == "inline"), None)
            if sibling is not None:
                while tree.node is not sibling:
                    tree.stack.pop()
                tree.stack.pop()
            parent_level = tree.stack[-1][0]
            tree.heading(parent_level + 1, label[1], section, local_id(info, label[1], False), heading="inline")
            tree.node.type, tree.node.number = info.type, info.number
        kind = "arabic" if text.is_arabic() else "paragraph"
        extra = {"continued": True} if previous_arabic and kind == "paragraph" and text.text[:1].islower() else {}
        record = book.add_paragraph(tree.node, kind, text, **extra)
        for (_, note_id), offset in zip(block.notes, positions):
            note = page.notes.get(note_id)
            if note is None:
                report.unmatched_notes.append(note_id)
                continue
            note_text, _ = _text(note)
            book.add_hasiye(record["id"], tree.node, offset, note_text)
            report.hasiye += 1
        previous_arabic = kind == "arabic"
        i += 1


def _pdf_items(pdf_book: dict) -> list[dict]:
    return [p for p in pdf_book["paragraphs"] if p["kind"] != "hasiye"]


def _best(items: list[dict], block: Block, start: int = 0) -> int | None:
    grams = _grams(block.text)
    best, score = None, 0.0
    for k in range(start, len(items)):
        text = items[k].get("text")
        if not text:
            continue
        shared = len(grams & _grams(text)) / max(len(grams), 1)
        if shared > score:
            best, score = k, shared
    return best if score >= 0.3 else None


def _cuz(text: str) -> int | None:
    """"On Beşinci Cüz" -> 15 (resim yazısı ya da tablonun ilk hücresi)."""
    m = re.match(r"^\s*(.+?)\s+Cüz\b", text)
    return parse_ordinal(m[1].replace(" ", "")) if m else None


def _tables(book: Book, node: Node, before: list[Block], after: list[Block], nurpedia_grams: set,
            items: list[dict], report: Report, images: list[str], captions: set[int]) -> None:
    """Resim dizisinin yerine eski kaynağın aynı aralıktaki tabloları. Çapa: resimlerden önceki ve sonraki,
    eski kaynakta da bulunan en yakın paragraf (nurpedia'da olup PDF'te olmayan paragraflar atlanır)."""
    first = next((k for b in before[:CHAIN] if (k := _best(items, b)) is not None), None)
    last = next((k for b in after[:CHAIN] if (k := _best(items, b, (first or 0) + 1)) is not None), None)
    if first is None or last is None or last <= first:
        raise ValueError(f"{node.id}: tabloların yeri eski kaynakta bulunamadı ({images[0]})")
    taken = []
    for k in range(first + 1, last):
        item = items[k]
        text = item.get("text") or ""
        grams = _grams(text)
        if not text or k in report.used:
            continue
        if item["kind"] == "table":
            # Cüz cetvelleri: tablo, ilk cüzünün resmi bu dizideyse buraya girer (iki dizi aynı aralığı paylaşabilir)
            if captions and (n := _cuz(text.split("\n", 1)[0])) is not None and n not in captions:
                continue
        elif captions or grams and len(grams & nurpedia_grams) / len(grams) >= MIN_SHARED:
            continue                                         # nurpedia'da da olan metin; cetvel dizisinde yalnız tablo
        report.used.add(k)
        taken.append(item["id"])
        arabic = [ArabicSpan(a["start"], a["end"], a["kind"]) for a in item.get("arabic", [])]
        book.add_paragraph(node, item["kind"], Text(text, arabic), source_edition="pdf", source_id=item["id"])
        report.tables += item["kind"] == "table"
    if not taken:
        raise ValueError(f"{node.id}: {images[0]} resminin yerine eski kaynakta tablo bulunamadı")
    report.table_runs.append(f"{node.id} [{items[first]['id'].split('remiz-07/')[-1]} .. {items[last]['id'].split('remiz-07/')[-1]}]: {len(images)} resim -> " + ", ".join(t.rsplit("/", 2)[-2] + "/" + t.rsplit("/", 1)[-1] for t in taken))


def load_pdf_book(path: Path) -> dict | None:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None
