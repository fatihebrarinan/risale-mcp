"""Klasik eserler, E5 (kelâm, usûl, siyer): başlık ağacı kurulan büyük eserlerin ayrıştırıcısı.

    uv run python -m risale_mcp.build serhul-mevakif serhul-makasid telvih mevahib

Paragraf kurma 1. dilimdeki gibidir (`books/klasik_openiti.py`: kaynağın satırı baskının paragrafı, yalnız sayfa
sınırında birleşir; tek beyit kendi paragrafı; muhakkikin dipnot işaretleri ayrılır). Fark başlık ağacındadır: bu
eserlerin bölümleri iç içe ve aynı adlıdır ("المقصد الأول" Mevâkıf'ta 30'dan çok yerde), düz bir liste atıfı
belirsizleştirir. Kurallar ham verinin incelemesinden (2026-11-25):

**Seri kuralı** (`Tree.place`): sıra sayılı bir başlık ("المرصد الثاني", "الفصل الأول"; tür kelimesi `KINDS`, sayı
`ordinal`) ancak kendi serisinin sıradaki numarasıysa bölüm açar: yığında aynı türden bir bölüm varsa ve numarası bir
eksikse onun kardeşi olur; aynı türden açık bölüm yoksa ve numara 1 ise en içteki bölümün çocuğu olur (yeni seri).
Tutmayan "başlık" bölüm açmaz, metin olarak kalır, kelime düşmez. Ham veride bunlar Şâmile'nin içindekilerden
türettiği başlıklardır: bölümün başındaki içindekiler satırları ("1 - المرصد الأول…", "المرصد الثاني في الكم المزصد
الثالث…"), aynı başlığın iki kez yazılması (Mevâkıf'ta "الموقف السادس"), metin cümlesi ("قدم مباحث الوجود…").
Sırasız başlıklar (`UNRANKED`: مقدمة, خاتمة, تنبيه, تذييل…) en içteki bölümün çocuğudur; sıralı bir başlık gelince önce
onlar kapanır. Türlerin sabit bir seviyesi yoktur (Mevâkıf'ta "القسم الرابع" "الفصل الأول"i içerir, başka yerde tersi):
seviye seriden çıkar. Bedeli: eksik bir başlık serisinin devamını metne düşürür (Mevâkıf'ta "القسم الثاني في النفس
الحيوانية", öncesi kaynakta başlık değil); bölüm kaba kalır (`Report.rejected`).

**Şerhu'l-Mevâkıf** (ShamAY0033881, Umeyre baskısı; OpenITI'de Îcî'nin adı altında "المواقف" diye durur, içi Seyyid
Şerîf'in şerhidir): baskı Îcî'nin metnini "المتن" satırıyla, şerhi "الشرح" satırıyla ayırır. Bu satırlar bölümün
içinde alt bölüm açar (`m1` "المتن", `s1` "الشرح"); metin bölümü katmandır (`authority: metin`, `by: Îcî`),
şârihin sözü değildir. Baskı metni her yerde ayırmamıştır (145 "المتن", 179 "الشرح"): ayrılmayan yerde metin şerhin
içinde kalır ve şârihin bölümünde görünür. Başlıklar Şâmile'nin "AUTO" başlıklarıdır, `[جزء n]` satırları atılır.
İlk başlıktan önceki metin (şârihin mukaddimesi, Îcî'nin hutbesinin şerhi) başlıksız bir bölümdür.

**Şerhu'l-Makāsıd** (JK001157; ShamAY sürümü aynı düzende): başlık satırı yoktur. Teftâzânî kendi metnini "قال"
ile aktarır, bölümler bu aktarmanın başındadır ("قال المبحث الأول …", "( قال المبحث الأول )"). Paragraf bu
işaretten bölünür, işaret yeni bölümün ilk sözüdür. Serinin ilk bölümü çoğu yerde "قال"sız başlar ("الفصل الأول"
metnin içinde): bu yüzden seri kuralı gevşektir: aynı türden açık bölümden büyük numara kardeş, açık bölüm yoksa
çocuk olur; küçük ya da eşit numara (aktarmanın tekrarı) bölüm açmaz. Bölüm başlığı yalnız tür ve sayıdır.

**et-Telvîh** (JK007110, Umeyrât baskısı): JK sürümü yalnız Teftâzânî'nin şerhidir, başlıksızdır. Aynı baskının
ShamAY sürümü (ShamAY0034200) başlıklıdır ama sayfa düzeni bozuktur: her sayfada Tavzîh (üstte) ile Telvîh
("....." çizgisinin altında) iç içedir. Metin JK'dan alınır; her JK paragrafının ilk sekiz kelimesi ShamAY'de
(son yerin yakınında) aranır, paragraf orada önündeki son başlığın bölümüne girer. Bulunamayan paragraf önceki bölümde
kalır (`Report.unmatched`). Başlıklar Şâmile'nin içindekilerindendir ("مدخل" gibi baskıda olmayanlar dahil);
seviyeleri ShamAY'nin işaretinden. Paragrafı olmayan başlık (yalnız Tavzîh'in metni olan yer) bölüm açmaz.

**el-Mevâhibü'l-Ledünniyye** (Shamela0023685, Tevfîkıyye): başlıklar tek seviyedir, seri kuralı on Maksadı ve
içindeki fasıl, nev', kısım serilerini kurar; sırasız başlıklar (köşeli parantezliler baskının eklediği) en içteki
bölüme girer. "* …" ve "ومنها" ile başlayan başlıklar sayımın maddeleridir, metin kalır. Muhakkikin dipnot işaretleri
(«1») metinden ayrılır, dipnotların kendisi kaynakta yok.
"""

import re
from dataclasses import dataclass, field

from risale_mcp import openiti
from risale_mcp.books import klasik_openiti as K
from risale_mcp.books.model import Book, Node, Text
from risale_mcp.books.openiti_writer import Para, Writer
from risale_mcp.catalog import Work
from risale_mcp.paths import RAW_DIR

SHAMELA_HEADING = "Başlık Şâmile sürümünün içindekilerinden (baskıda böyle olmayabilir)"
TEXT_HEADING = "Başlık metinden: kaynakta başlık satırı yok, bölüm müellifin \"قال\" ile aktardığı metnin başında"
MATN_SUBTITLE = "Metin (المتن): Îcî'nin el-Mevâkıf'ı; şârihin sözü değil"


def fold(text: str) -> str:
    """Sıra kelimesi karşılaştırması için: hemze, elif-maksûre, tâ-i merbûta ve hareke farkı yok sayılır."""
    text = re.sub(r"[ً-ْـٰ]", "", text)
    return text.translate(str.maketrans("أإآٱىة", "اااايه"))


_UNITS = {"الاول": 1, "الاولي": 1, "الحادي": 1, "الحاديه": 1, "الثاني": 2, "الثانيه": 2, "الثالث": 3, "الثالثه": 3,
          "الرابع": 4, "الرابعه": 4, "الخامس": 5, "الخامسه": 5, "السادس": 6, "السادسه": 6, "السابع": 7,
          "السابعه": 7, "الثامن": 8, "الثامنه": 8, "التاسع": 9, "التاسعه": 9, "العاشر": 10, "العاشره": 10}
_TENS = {"العشرون": 20, "الثلاثون": 30, "الاربعون": 40}


def ordinal(words: list[str]) -> int | None:
    """Arapça sıra sayısı ("الثاني", "الحادي عشر", "الثالث والعشرون"); katlanmış kelimelerle."""
    if not words:
        return None
    w = words[0].rstrip(":،.")
    if w in _TENS:
        return _TENS[w]
    if w not in _UNITS:
        return None
    n = _UNITS[w]
    nxt = words[1].rstrip(":،.") if len(words) > 1 else ""
    if nxt in ("عشر", "عشره", "العشر"):                # "الرابع العشر": Mevâkıf'ın dizgisi
        return n + 10 if n < 10 else None
    if nxt.startswith("و") and nxt[1:] in _TENS:
        return n + _TENS[nxt[1:]]
    return n


KINDS = {"الموقف", "المرصد", "المقصد", "الفصل", "النوع", "القسم", "المبحث", "الباب", "الركن", "المقاله", "الطبقه",
         "الفرع", "التقسيم", "المسلك", "المطلب", "الفرقه"}
TYPOS = {"المقصر": "المقصد", "المزصد": "المرصد"}     # Mevâkıf'ın Şâmile başlıklarındaki dizgi hataları
UNRANKED = ("المقدمه", "مقدمه", "خاتمه", "الخاتمه", "تنبيه", "تذييل", "تذنيب", "تتمه", "تكمله", "فائده", "الكلام")


def heading_kind(title: str) -> tuple[str | None, int | None]:
    words = fold(title).split()
    if not words:
        return None, None
    first = TYPOS.get(words[0], words[0])
    if first in KINDS and (n := ordinal(words[1:])) is not None:
        return first, n
    return None, None


@dataclass
class Report(K.Report):
    rejected: list[str] = field(default_factory=list)       # bölüm açmayan başlıklar (metin kaldı)
    layers: int = 0                                          # metin (المتن) bölümleri
    unmatched: int = 0                                       # Telvîh: başlığı bulunamayan paragraflar
    shamela_headings: int = 0
    lost: int = 0                                            # İhyâ: bağlanacak paragrafı olmayan şerh parçası


@dataclass
class _Open:
    node: Node
    kind: str | None
    n: int | None


class Tree:
    """Seri kuralıyla başlık ağacı (modülün açıklaması). `relaxed`: Makāsıd'ın metin içi işaretleri."""

    def __init__(self, book: Book, report: Report, relaxed: bool = False, ranks: dict[str, int] | None = None) -> None:
        self.book, self.report, self.relaxed, self.ranks = book, report, relaxed, ranks or {}
        self.stack = [_Open(book.root, "root", None)]
        self.counts: dict[str, int] = {}

    def _child(self, title: str, kind: str | None, n: int | None, subtitle: str | None, prefix: str = "",
               **extra) -> Node:
        parent = self.stack[-1].node
        key = f"{parent.id}|{prefix}"
        self.counts[key] = k = self.counts.get(key, 0) + 1
        node = self.book.add_node(parent, f"{prefix}{k}", title, **({"subtitle": subtitle} if subtitle else {}))
        node.extra.update(extra)
        self.stack.append(_Open(node, kind, n))
        self.report.sections += 1
        return node

    def _pop_unranked(self) -> None:
        while len(self.stack) > 1 and self.stack[-1].kind is None:
            self.stack.pop()

    def place(self, title: str, subtitle: str | None, unranked_ok: bool = False) -> Node | None:
        kind, n = heading_kind(title)
        if kind is None:
            if unranked_ok or fold(title).split()[0] in UNRANKED:
                self._pop_unranked()
                return self._child(title, None, None, subtitle)
            return None
        if self.ranks:                                   # sabit seviyeli eser (Makāsıd): üst seviyeler kapanmaz
            rank = self.ranks[kind]
            for i in range(len(self.stack) - 1, 0, -1):
                if self.stack[i].kind == kind and n <= self.stack[i].n:
                    return None                          # aktarmanın tekrarı
                if self.stack[i].kind in self.ranks and self.ranks[self.stack[i].kind] < rank:
                    break
            while len(self.stack) > 1 and (self.stack[-1].kind is None
                                           or self.ranks.get(self.stack[-1].kind, 0) >= rank):
                self.stack.pop()
            return self._child(title, kind, n, subtitle)
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].kind == kind:
                prev = self.stack[i].n
                if n == prev + 1 or (self.relaxed and n > prev):
                    del self.stack[i:]
                    return self._child(title, kind, n, subtitle)
                if n == 1 and i < len(self.stack) - 1 and self.stack[-1].kind is not None:
                    return self._child(title, kind, n, subtitle)      # iç içe yeni seri (dışta aynı tür açık)
                return None
        if n == 1 or self.relaxed:
            self._pop_unranked()
            return self._child(title, kind, n, subtitle)
        return None

    def layer(self, title: str, matn: bool, by: str | None) -> Node:
        """Mevâkıf'ın "المتن" / "الشرح" satırı: en içteki bölümün içinde alt bölüm."""
        self._pop_unranked()
        if matn:
            self.report.layers += 1
            return self._child(title, None, None, MATN_SUBTITLE, "m", authority="metin", by=by)
        return self._child(title, None, None, None, "s")


TITLE_FIXES = {        # Şâmile başlığında tür kelimesi yanlış; seri ve konu bunu gösterir (Mevâkıf › الموقف الثاني)
    "المقصد الرابع في الوحدة والكثرة": "المرصد الرابع في الوحدة والكثرة",
}
FIXED_SUBTITLE = "Başlık Şâmile sürümünde \"{}\"; seriye göre düzeltildi"


def _title(p: openiti.Paragraph) -> str:
    """Şâmile başlığı: "AUTO"/"CHECK" etiketi, iç içe yazılmış işaret ("### |||| AUTO") ve boşluklar atılır."""
    text = K._clean(p.text)
    text = re.sub(r"#+\s*\|+\s*", " ", text)
    text = re.sub(r"\b(?:AUTO|CHECK)\b", " ", text)
    return " ".join(text.split())


def _start(book: Book, w: Writer, report: Report, title: str) -> Node:
    node = book.add_node(book.root, "mukaddime", title, subtitle=K.NO_TITLE)
    w.start(node)
    return node


def _finish(book: Book, notes: tuple[str, ...]) -> None:
    for note in notes:
        book.notes.append({"node_id": book.root.id, "after": None, "text": note})
    if K.MARKS["removed"]:
        book.notes.append({"node_id": book.root.id, "after": None,
                           "text": f"Muhakkikin dipnot işaretleri ({K.MARKS['removed']}) metinden ayrıldı; dipnotların "
                                   "kendisi kaynakta yok (OpenITI)."})
    K._printed_on_nodes(book)


# ---------------------------------------------------------------- Şerhu'l-Mevâkıf

MEVAKIF_NOTES = (
    "Başlıklar Şâmile sürümünün (ShamAY0033881) içindekilerinden; bölüm başlarındaki içindekiler satırları ve "
    "tekrarlar bölüm açmaz, metinde kalır.",
    "Îcî'nin metni baskının \"المتن\" satırıyla ayrıldığı yerde ayrı bölümdür (katman: metin, Îcî); baskının ayırmadığı "
    "yerde şerhin içindedir.",
)


def parse_mevakif(work: Work, raw_root=RAW_DIR / "openiti") -> tuple[Book, Report]:
    P = openiti.load(work.source.book, raw_root).paragraphs
    report, book = Report(), K._book(work)
    K.MARKS["removed"] = 0
    w = Writer(book, report)
    tree = Tree(book, report)
    pre = _start(book, w, report, "مقدمة الشارح")
    tree.stack.append(_Open(pre, None, None))
    asm = K.Assembler(w, report)
    for p in P[K.Mark("=" + K.BESMELE, 1).find(P):]:
        text = K._clean(p.text)
        if p.level:
            title = _title(p)
            if not title or title.startswith("[") or title.startswith("#"):
                report.dropped += 1
                if p.breaks:
                    asm.page(p)
                continue
            report.shamela_headings += 1
            label = None
            if (m := re.match(r"^(.*\S)\s+(المتن|الشرح)$", title)) and heading_kind(m[1])[0]:
                title, label = m[1], m[2]                # başlığa yapışmış baskı etiketi
            toc = re.match(r"^(\d+)\s*-\s*(.*)$", title)
            if toc:                                      # içindekiler satırı: yalnız serinin ilki bölüm açar
                node = tree.place(toc[2], SHAMELA_HEADING) if heading_kind(toc[2])[1] == 1 else None
                title = toc[2] if node is not None else title
            elif title in TITLE_FIXES:
                node = tree.place(TITLE_FIXES[title], FIXED_SUBTITLE.format(title))
            else:
                node = tree.place(title, SHAMELA_HEADING)
            if node is not None:
                w.start(node)
                asm.page_gap = False
                if label:
                    w.start(tree.layer(label, label == "المتن", "Adudüddîn el-Îcî"))
            else:
                report.rejected.append(title)
                asm.add(K._line(p, title), new=True)
            continue
        if not text or K._JUNK.match(text):
            if p.breaks:
                asm.page(p)
            continue
        if text in ("المتن", "الشرح"):
            w.start(tree.layer(text, text == "المتن", "Adudüddîn el-Îcî"))
            asm.page_gap = False
            continue
        asm.add(K._line(p, text))
    w.flush()
    _finish(book, MEVAKIF_NOTES)
    return book, report


# ---------------------------------------------------------------- Şerhu'l-Makāsıd

_MAKASID_MARK = re.compile(r"(?:\(\s*)?قال\s*\)?\s*(المقصد|الفصل|المبحث)\s+(\S+(?:\s+\S+)?)")
MAKASID_NOTES = (
    "Cilt başlarındaki kitap adı ve besmele satırları (\"شرح المقاصد في علم الكلام | 1 |\") alınmadı.",
    "Kaynakta başlık satırı yok: bölümler Teftâzânî'nin kendi metnini \"قال\" ile aktardığı yerlerden (\"قال "
    "المبحث الأول\"); paragraf orada bölünür. Serinin ilk bölümü \"قال\"sız başladığı yerde metin üst bölümde kalır.",
)


def _split(p: openiti.Paragraph, at: int) -> tuple[openiti.Paragraph, openiti.Paragraph]:
    """Satırı `at`'tan böler; sayfa sonları iki yana dağılır."""
    left, right = p.text[:at].rstrip(), p.text[at:].lstrip()
    skip = len(p.text) - len(p.text[at:].lstrip())
    lb = [(a, pg) for a, pg in p.breaks if a <= len(left)]
    rb = [(max(0, a - skip), pg) for a, pg in p.breaks if a > len(left)]
    return (openiti.Paragraph(p.raw, left, None, [], lb, p.page, p.end_page),
            openiti.Paragraph(p.raw, right, None, [], rb, p.page, p.end_page))


def parse_makasid(work: Work, raw_root=RAW_DIR / "openiti") -> tuple[Book, Report]:
    P = openiti.load(work.source.book, raw_root).paragraphs
    report, book = Report(), K._book(work)
    K.MARKS["removed"] = 0
    w = Writer(book, report)
    tree = Tree(book, report, relaxed=True, ranks={"المقصد": 1, "الفصل": 2, "المبحث": 3})
    pre = _start(book, w, report, "مقدمة المؤلف")
    tree.stack.append(_Open(pre, None, None))
    asm = K.Assembler(w, report)
    for p in P[K.Mark("نحمدك يا من").find(P):]:
        text = K._clean(p.text)
        if not text or K._JUNK.match(text) or re.match(r"^\|?\s*(?:شرح المقاصد في علم الكلام|بسم الله الرحمن الرحيم)\s*(?:\|.*)?$", text):
            if p.breaks:
                asm.page(p)
            continue
        line = K._line(p, text)
        while True:
            for m in _MAKASID_MARK.finditer(line.text):
                words = m[2].split()
                two = len(words) > 1 and (fold(words[1]) in ("عشر", "عشره") or fold(words[1])[1:] in _TENS)
                title = f"{m[1]} {' '.join(words[:2] if two else words[:1])}".rstrip(" :،.)")
                node = tree.place(title, TEXT_HEADING)
                if node is None:
                    continue
                before, after = _split(line, m.start())
                if before.text:
                    asm.add(before)
                w.start(node)
                asm.page_gap = False
                line = after
                break
            else:
                break
        if line.text:
            asm.add(line, new=not w.open)
    w.flush()
    _finish(book, MAKASID_NOTES)
    return book, report


# ---------------------------------------------------------------- et-Telvîh

TELVIH_NOTES = (
    "Metin JK007110'dan (yalnız Telvîh); başlıklar aynı baskının ShamAY0034200 sürümünün içindekilerinden, "
    "paragraflar ilk kelimeleriyle o sürümde bulunarak yerleştirildi. Tavzîh'in metni (Sadrüşşerîa) bu eserde yok; "
    "Teftâzânî onu \"قوله\" ile anar.",
)
_WORD = re.compile(r"[ء-ي]+")


def _words(text: str) -> list[str]:
    return [fold(x) for x in _WORD.findall(re.sub(r"[ً-ْٰ]", "", text))]


WINDOW = 30_000          # eşleşme son yerden en çok bu kadar kelime ileride aranır (uzak, yanlış eşleşme imleci atmasın)
BACK = 5_000             # ... ve bu kadar geride (önceki bir yanlış eşleşme imleci ileri attıysa geri döner)
KEY = 8                  # paragrafın ilk kaç kelimesi: 6 kelimelik kalıplar ("وقال صلى الله عليه وسلم") çok yerde geçiyor


def _aligned(work: Work, raw_root, head_key: str, notes: tuple[str, ...], preface: str,
             tahric: str | None = None, intro: tuple[str, str] | None = None, key_len: int = KEY,
             window: int | None = WINDOW, back: int = BACK) -> tuple[Book, Report]:
    """Metin `work.source.book`'tan, başlıklar `head_key` sürümünden: her paragrafın ilk sekiz kelimesi başlıklı
    sürümde (sıra korunarak) aranır, paragraf orada önündeki son başlığın bölümüne girer (Telvîh, İhyâ).
    `tahric` verilirse paragrafın içindeki "+ حديث … +" parçaları metinden ayrılır, o kişinin şerhi olarak
    yerlerine bağlanır (hâşiye gibi, `commentator`); paragraf kaynağın satırıdır, sayfa sınırında birleşmez.
    `intro` (ilk ve son sözleri): kaynağın metne kattığı şârih mukaddimesi; tek şerh parçası olarak önceki
    paragrafa bağlanır (İhyâ'da Irâkî'nin mukaddimesi, Gazâlî'nin hutbesinin ortasında)."""
    import bisect
    P = openiti.load(work.source.book, raw_root).paragraphs
    Q = openiti.load(head_key, raw_root).paragraphs
    report, book = Report(), K._book(work)
    K.MARKS["removed"] = 0
    stream: list[str] = []
    heads: list[tuple[int, int, str]] = []          # (akıştaki yer, seviye, başlık)
    for q in Q:
        if q.level:
            title = _title(q)
            if title and re.search(r"[\u0621-\u064A]", title):
                heads.append((len(stream), q.level, title))
            continue
        stream += _words(q.text)
    report.shamela_headings = len(heads)
    index: dict[tuple[str, ...], list[int]] = {}
    for i in range(len(stream) - key_len + 1):
        index.setdefault(tuple(stream[i:i + key_len]), []).append(i)
    starts = [h[0] for h in heads]
    parents: list[int | None] = []                   # her başlığın üst başlığı (seviyeden)
    for k, (_, level, _) in enumerate(heads):
        j = k - 1
        while j >= 0 and heads[j][1] >= level:
            j = parents[j] if parents[j] is not None else -1
        parents.append(j if j >= 0 else None)

    w = Writer(book, report)
    asm = K.Assembler(w, report)
    made: dict[int, Node] = {}
    counts: dict[str, int] = {}
    pre = _start(book, w, report, preface)
    current = None
    pos = 0
    open_tahric: list[str] = []                       # paragraf sınırını aşan tahric

    def node_of(k: int) -> Node:
        if k in made:
            return made[k]
        parent = node_of(parents[k]) if parents[k] is not None else book.root
        counts[parent.id] = c = counts.get(parent.id, 0) + 1
        made[k] = book.add_node(parent, str(c), heads[k][2], subtitle=SHAMELA_HEADING)
        report.sections += 1
        return made[k]

    def continues(nxt: str | None) -> bool:
        """Açık kalan tahric sonraki paragrafa sürer mi: oradaki ilk "+" bir kapanışsa (ardından "حديث" gelmiyor ya da
        paragraf onunla bitiyor). İlk "+" yeni bir tahric açıyorsa öncesi müellifin metnidir."""
        if not nxt or "+" not in nxt:
            return False
        after = re.split(r"\s*\+\s*", nxt, maxsplit=1)[1]
        return not after.startswith("حديث")

    def split_tahric(text: str, nxt: str | None) -> tuple[str, list[tuple[int, str]]]:
        """Metin ve şerh parçaları: "+ حديث …" ile açılan parça bir sonraki "+"ya kadar şerhtir; açık kalırsa
        sonraki paragrafa yalnız `continues` öyle derse sürer."""
        out, notes_, parts = "", [], re.split(r"\s*\+\s*", text)
        for n, part in enumerate(parts):
            last = n == len(parts) - 1
            if open_tahric or (n > 0 and part.startswith("حديث")):
                if part:
                    open_tahric.append(part)
                if not last or not continues(nxt):
                    if open_tahric:
                        notes_.append((len(out.rstrip()), " ".join(open_tahric)))
                    open_tahric.clear()
                continue
            if part:
                out = f"{out} {part}" if out else part
        return out.strip(), notes_

    def bar(text: str) -> str:
        """İhyâ'nın JK sürümünde satır başındaki "| " işareti metin değildir; Telvîh'in yayımlanan kimlikleri onu
        metinde tutar (4 satır), dokunulmaz."""
        return text.lstrip("| ").strip() if tahric else text

    first = next((n for n, x in enumerate(P) if bar(K._clean(x.text)) == K.BESMELE), 0)
    collecting: list[str] | None = None
    last_para: tuple[dict, Node] | None = None
    for idx in range(first, len(P)):
        p = P[idx]
        text = bar(K._clean(p.text))
        if intro and collecting is None and text.startswith(intro[0]):
            collecting = []
        if collecting is not None:
            head, sep, rest = text.partition(" + ") if intro[1] in text else (text, "", "")
            collecting.append(head.strip())
            if not sep and intro[1] not in text:
                continue
            last, node = last_para
            book.add_hasiye(last["id"], node, len(last["text"]), Text(" ".join(collecting)), commentator=tahric)
            report.layers += 1
            intro, collecting = None, None
            text = rest.strip()
            if not text:
                continue
        if not text or K._JUNK.match(text):
            if p.breaks:
                asm.page(p)
            continue
        key = tuple(_words(text)[:key_len])
        hit = next((i for i in index.get(key, []) if pos - back <= i and (window is None or i <= pos + window)),
                   None) if len(key) == key_len else None
        if hit is None:
            report.unmatched += 1
        else:
            pos = hit
            k = bisect.bisect_right(starts, hit) - 1
            if k >= 0 and k != current:
                current = k
                w.start(node_of(k))
                asm.page_gap = False
        if tahric is None:
            asm.add(K._line(p, text), new=hit is not None and w.open is None)
            continue
        nxt = bar(K._clean(P[idx + 1].text)) if idx + 1 < len(P) else None
        body, parts = split_tahric(text, nxt)
        if not body:
            if parts and last_para is not None:     # yalnız şerhten oluşan satır: önceki paragrafa (bölümü ne olursa)
                for _, note in parts:
                    book.add_hasiye(last_para[0]["id"], last_para[1], len(last_para[0]["text"]), Text(note),
                                    commentator=tahric)
                    report.layers += 1
            elif parts:
                report.lost += len(parts)
            continue
        w.flush()
        line = K._line(p, body)
        record = w._emit("paragraph", Para(line))
        last_para = (record, w.node)
        for at, note in parts:
            book.add_hasiye(record["id"], w.node, min(at, len(record["text"])), Text(note), commentator=tahric)
            report.layers += 1
    w.flush()
    if not pre.paragraph_count:
        book.root.children.remove(pre)
    _finish(book, notes)
    return book, report


def parse_telvih(work: Work, raw_root=RAW_DIR / "openiti") -> tuple[Book, Report]:
    # Yayımlanan kimlikler (2026-11-25) bu ayarlarla kuruldu: altı kelime, pencere yok (değişirse cümleler kayar)
    return _aligned(work, raw_root, f"{work.source.book}-shamay", TELVIH_NOTES, "مقدمة الشارح", key_len=6,
                    window=None, back=0)


# ---------------------------------------------------------------- İhyâu Ulûmi'd-Dîn

IHYA_COMMENTATOR = "Zeynüddîn el-Irâkî"
IHYA_NOTES = (
    "Metin JK000001'den (Dâru'l-Ma'rife); başlıklar aynı baskının Shamela0009472 sürümünün içindekilerinden, "
    "paragraflar ilk kelimeleriyle o sürümde bulunarak yerleştirildi.",
    "Irâkî'nin hadis tahrici (el-Muğnî an Hamli'l-Esfâr) bu baskıda metnin içinde \"+ حديث … +\" arasında durur: "
    "metinden ayrıldı, geçtiği cümleye şerh olarak bağlandı (commentator: Irâkî); Gazâlî'nin sözü değildir. "
    "Irâkî'nin kendi mukaddimesi (\"الحمد لله الذي أحيا علوم الدين…\") kaynakta Gazâlî'nin hutbesinin ortasındadır: "
    "o da şerh olarak önceki paragrafa bağlandı.",
)


def parse_ihya(work: Work, raw_root=RAW_DIR / "openiti") -> tuple[Book, Report]:
    return _aligned(work, raw_root, f"{work.source.book}-shamela", IHYA_NOTES, "مقدمة المؤلف", tahric=IHYA_COMMENTATOR,
                    intro=("الحمد لله الذي أحيا علوم الدين", "جعله الله خالصا لوجهه الكريم"))


# ---------------------------------------------------------------- el-Mevâhibü'l-Ledünniyye

_MAWAHIB_NOTE = re.compile(r"\s?«\d+»")
MEVAHIB_NOTES = (
    "Başlıklar baskının (Tevfîkıyye); köşeli parantezliler baskının eklediği. \"* …\" ve \"ومنها\" başlıkları "
    "sayımın maddeleridir, metinde kaldı.",
)


def parse_mevahib(work: Work, raw_root=RAW_DIR / "openiti") -> tuple[Book, Report]:
    P = openiti.load(work.source.book, raw_root).paragraphs
    report, book = Report(), K._book(work)
    K.MARKS["removed"] = 0
    w = Writer(book, report)
    tree = Tree(book, report)
    asm = K.Assembler(w, report)
    marks = 0

    def clean(text: str) -> str:
        nonlocal marks
        marks += len(_MAWAHIB_NOTE.findall(text))
        return _MAWAHIB_NOTE.sub("", text).strip()

    for p in P[K.Mark("=مقدمة المؤلف").find(P):]:
        text = clean(K._clean(p.text))
        if p.level:
            title = clean(_title(p))
            if not title:
                continue
            if not re.search(r"[\u0621-\u064A]", title):
                report.dropped += 1
                continue
            if title.startswith("*") or fold(title).startswith("ومنها"):
                report.rejected.append(title)
                asm.add(K._line(p, title), new=True)
                continue
            node = tree.place(title, K.EDITION_HEADING, unranked_ok=True)
            if node is None:                         # seriyi tutmayan sıralı başlık: sırasız bölüm
                tree._pop_unranked()
                node = tree._child(title, None, None, K.EDITION_HEADING)
            w.start(node)
            asm.page_gap = False
            continue
        if not text or K._JUNK.match(text):
            if p.breaks:
                asm.page(p)
            continue
        asm.add(K._line(p, text))
    w.flush()
    notes = MEVAHIB_NOTES + ((f"Muhakkikin dipnot işaretleri («1», {marks}) metinden ayrıldı; dipnotların kendisi "
                              "kaynakta yok (OpenITI).",) if marks else ())
    _finish(book, notes)
    return book, report


PARSERS = {"serhul-mevakif": parse_mevakif, "serhul-makasid": parse_makasid, "telvih": parse_telvih,
           "mevahib": parse_mevahib, "ihya": parse_ihya}
