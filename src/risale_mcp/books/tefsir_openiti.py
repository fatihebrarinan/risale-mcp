"""Müfessirlerin eserleri, OpenITI: metin Shamela sürümünden, âyet birimleri altafsir sürümünden (MVP M2,
`docs/mvp-kitaplar.md`).

    uv run python -m risale_mcp.fetch tefsir        # data/raw/openiti/<eser>-shamela.txt ve <eser>-altafsir.txt
    uv run python -m risale_mcp.build kessaf        # data/library/tefsir/kessaf.json

Neden iki sürüm: seçilen Shamela sürümü metnin tamamını, basılı sayfasını ve muhakkikini verir ama âyet birimi
işareti eserden esere farklıdır, altısında hiç yoktur. altafsir.com'dan alınmış sürüm (`Tafsir…`) her birimin
başında `### || [2.6]` (ya da `[13.5-6]`) taşır ve âyetlerin hemen hepsini kapsar (M1 ölçümü), ama sayfasızdır ve
"eksik metin" diye işaretlidir. Bu yüzden metin hiçbir zaman altafsir'den alınmaz; ondan yalnız sınırlar alınır.

Çapalama: iki metin de harf iskeletine (`quran.skeleton`, kelime kelime) indirilir. Her birimin metninin ilk
kelimelerinden 5'li (kısa birimde 3'lü) diziler Shamela'nın kelime dizisinde aranır, adaylar dizilerin sıklığıyla
tartılır (seyrek söz yeri belirler, sık geçen âyet sözü belirleyemez); bütün birimler için kitap sırasıyla tutarlı
en güçlü aday zinciri seçilir (`anchor`, `_chain`). Birim satırın ortasında başlıyorsa satır çapanın kelimesinden
bölünür (`_split_lines`). Bulunamayan birim (altafsir'de metni eksik ya da baskı farkı) öncekine
katılır: o zaman öncekinin aralığı genişler, adres yine doğru kalır (birim "6–7. âyetler" olur, tahmin edilmez).
Birimin aralığı altafsir başlığının başından bir sonraki birimin başına kadardır; sûrenin son birimi sûrenin son
âyetine kadar uzar.

Sınırın satırı: çapanın düştüğü kaynak satırı; hemen önündeki satırlar birimin başıdır, eğer âyet satırıysa (sonu
"(6)", numarası birimin aralığında: `kind: "ayah"`, cümle sayılmaz), yalnız sayfa işaretiyse ya da başlıksa (Shamela'nın
"قوله تعالى" gibi başlıkları birimin ilk paragrafı olur).

Paragraf: Beyzâvî'deki kural (`books/openiti_writer.py`: paragraf cümle sonunda biter). Ama noktalaması seyrek
eserde (100 kelimede birden az . ؟ !; Nesefî gibi) kaynağın kendi paragrafları korunur: orada her lemma yeni
paragraf açar ve cümle sonuna kadar birleştirmek bütün bir sûreyi tek paragraf yapardı. İki birimin başı aynı
kaynak satırına düşerse satır bölünmez, birimler tek aralıkta birleşir.

Sûre: altafsir'in sûre başlıkları (`### | [2 - سورة البقرة]`) sûre düğümünü açar; Shamela'da ilk birimden önce
"سورة" geçen bir başlık varsa sûrenin kendi metni (mekkî/medenî, fazîleti) oradan başlar, yoksa önceki birime
kalır (ayıran işaret yoksa ayrılmaz).

Ön metin (ilk birimden önceki kısım; envanter `docs/tefsir-on-metinler.md`, kullanıcının kararı 2026-11-07): sınırlar
eser başına gözle doğrulandı ve `FRONT`'ta baskının kendi satırlarıyla yazılıdır, tahmin edilmez. Müellifin mukaddimesi
`<eser>/mukaddime` düğümüdür; muhakkikin ve baskının girişleri ayrı katmandır (`authority: muhakkik`, `by`; Beyzâvî'deki
gibi), müellife mal edilmez. Fâtiha'nın kendi metni (mekkî/medenî, fazîleti) sûre düğümüne gider; ön metne düşmüş
âyet tefsiri birimine döner: Râzî'nin ve ed-Dürrü'l-Mensûr'un besmelesi yeni 1:1 birimi, Mâtürîdî'ninki 1:1'in,
Kurtubî'ninki 1–7 biriminin başı. ed-Dürrü'l-Mensûr'da altafsir Fâtiha'yı besmelesiz sayıyor (etiketleri bir âyet kayık): o sûrenin altafsir
birimleri atılır, besmeleden sonrası baskının "2 -" numarasından tek 2–7 birimi olur (adres geniş ama doğru). İlk
satırlardaki Shamela künyesi (yazar, muhakkik, yayınevi) ve baskının harfli sayfa satırları ("- ط -") alınmaz.
"""

import bisect
import re
from dataclasses import dataclass, field

from risale_mcp import openiti
from risale_mcp.books.model import Book
from risale_mcp.books.openiti_writer import Report, Writer
from risale_mcp.catalog import Work
from risale_mcp.paths import RAW_DIR
from risale_mcp.quran import Quran, skeleton

GRAM = 5                      # çapa dizisinin uzunluğu (kelime)
ANCHOR_WORDS = 60             # birimin ilk kaç kelimesinde dizi aranır
MIN_SCORE = 1.0               # bir yerin kabulü: onu gösteren dizilerin 1/sıklık toplamı
SHORT_GRAM = 3                # kısa birimde (az kelime) ek dizi uzunluğu
MAX_PLACES = 200              # bundan sık geçen dizi aday üretmez (puanı zaten çok küçük)
UNIT_SUBTITLE = "Birim sınırı OpenITI'nin altafsir.com sürümünden; metin ve sayfa {edition}"
FRONT_NOTE = ("İlk âyet biriminden önceki metin (muhakkikin girişi ve müellifin mukaddimesi bu sürümde ayrı işaretli "
              "değil) alınmadı.")
FRONT_TAKEN_NOTE = ("İlk âyet biriminden önceki metnin sınırları gözle doğrulandı (`FRONT`): müellifin mukaddimesi "
                    "`mukaddime`, muhakkikin ve baskının girişleri ayrı katman. Baştaki Shamela künyesi alınmadı.")
NO_TITLE = "Başlık kaynakta yok: müellifin ilk âyet biriminden önceki metni"
FRONT_UNIT_SUBTITLE = "Birim sınırı baskının kendi satırından (\"{line}\"); metin ve sayfa {edition}"


@dataclass(frozen=True)
class Front:
    """Ön metnin bir kısmı. `at`: kısmın başladığı satır (önceki kısımdan sonra ilk eşleşen; "=" ile başlıyorsa tam
    eşit, değilse satır onunla başlar; None: ön metnin ilk satırı). `kind`: `mukaddime` (müellifin), `tahkik`
    (muhakkikin ya da baskının katmanı, `local` ve `by` ile), `sura` (sûrenin kendi metni), `unit` (yeni âyet birimi,
    `verses`), `prepend` (ilk birim buradan başlar)."""
    kind: str
    at: str | None = None
    title: str | None = None
    printed: bool = True
    local: str | None = None
    by: str | None = None
    subtitle: str | None = None
    verses: tuple[int, int, int] | None = None
    nth: int = 1                     # `at`'in kaçıncı eşleşmesi


_TABI = "Baskının mukaddimesi (Ahmed Abdülalîm el-Berdûnî, 1372/1952): müellifin metni değil"
FRONT: dict[str, list[Front]] = {
    "taberi": [Front("mukaddime", None, "مقدمة المصنف"), Front("sura", "سورة الفاتحة")],
    "maturidi": [Front("tahkik", "* مقدمة التحقيق", "مقدمة التحقيق", local="mukaddime-tahkik"),
                 Front("mukaddime", "مقدمة المصنف", "مقدمة المصنف"), Front("prepend", "=بسم الله الرحمن الرحيم (1)")],
    "kessaf": [Front("mukaddime", "مقدمة التفسير للعلامة الزمخشري", "مقدمة التفسير للعلامة الزمخشري"),
               Front("sura", "سورة فاتحة الكتاب")],
    "razi": [Front("mukaddime", None, "مقدمة المؤلف", printed=False), Front("sura", "سورة الفاتحة"),
             Front("unit", "تفسير البسملة", verses=(1, 1, 1))],
    "kurtubi": [Front("tahkik", "مقدمة الطبعة الثانية", "مقدمة الطبعة الثانية", local="mukaddime-tabi",
                      by="Ahmed Abdülalîm el-Berdûnî", subtitle=_TABI),
                Front("tahkik", "ترجمة أبي عبد الله القرطبي", "ترجمة أبي عبد الله القرطبي مؤلف هذا التفسير",
                      local="tercume", subtitle="Baskının müellif biyografisi: müellifin metni değil"),
                Front("mukaddime", "=المدخل", "المدخل"), Front("prepend", "[الكلام في] البسملة")],
    "nesefi": [Front("mukaddime", None, "مقدمة المؤلف", printed=False),
               Front("sura", "=بسم الله الرحمن الرحيم", nth=2)],
    "ibnkesir": [Front("mukaddime", None, "مقدمة ابن كثير")],
    "celaleyn": [Front("sura", None)],
    "durr": [Front("mukaddime", "مقدمة المؤلف", "مقدمة المؤلف"), Front("sura", "مقدمة سورة الفاتحة"),
             Front("unit", "قوله تعالى: بسم الله الرحمن الرحيم", verses=(1, 1, 1)),
             Front("unit", "=2 -", verses=(1, 2, 7))],
    "ebussuud": [Front("mukaddime", "=مقدمة", "مقدمة"), Front("sura", "سورة الفاتحة")],
    "bursevi": [Front("mukaddime", None, "مقدمة المؤلف", printed=False), Front("sura", "سورة فاتحة الكتاب")],
    "alusi": [Front("mukaddime", None, "خطبة المفسر"), Front("sura", "سورة الفاتحة")],
}
DROP_UNITS = {"durr": {1}}          # altafsir birimleri güvenilmeyen sûreler (yerine `FRONT`'taki birimler)
_FRONT_JUNK = re.compile(r"^(?:-\s*\S{1,3}\s*-|\.{3,}|الجزء ال\S+|EDITOR\|?)$")


def _front_segments(P: list[openiti.Paragraph], plan: list[Front]) -> list[tuple[Front, int]]:
    """`FRONT` kısımlarının ön metindeki başlangıç satırları; bulunamayan kısım kurulumu durdurur (sınır tahmin
    edilmez)."""
    out, at = [], 0
    for f in plan:
        if f.at is None:
            idx = 0 if not out else None
        else:
            exact, want = f.at.startswith("="), f.at.lstrip("=")
            hits = (i for i in range(at, len(P)) if P[i].text and
                    (P[i].text.strip() == want if exact else P[i].text.strip().startswith(want)))
            idx = next((i for k, i in enumerate(hits, 1) if k == f.nth), None)
        if idx is None:
            raise ValueError(f"ön metinde kısım bulunamadı: {f.kind} {f.at!r}")
        out.append((f, idx))
        at = idx + 1
    return out


def _title_line(p: openiti.Paragraph, title: str) -> bool:
    text = re.sub(r"\s*\(\d+\)\s*$", "", (p.text or "").strip().lstrip("* ").strip())
    return text == title

_UNIT_HEAD = re.compile(r"^### \|+ \[(\d+)\.(\d+)(?:-(\d+))?\]\s*$")
_SURA_HEAD = re.compile(r"^### \|+ \[(\d+) - (سورة .+?)\]\s*$")
_VERSE_NO = re.compile(r"\((\d{1,3})\)")
_VERSE_LINE = re.compile(r"\(\d{1,3}\)\s*$")
_MARKUP = re.compile(r"ms\d+|PageV\d+P\d+|[{}~#|]")
# baskının kendi birim başlığı ("[سورة النمل (27) : الآيات 59 الى 60]"), satırlara bölünmüş parçalarıyla
_UNIT_REF = re.compile(r"\(\d+\)\s*:")
_EDITION_HEAD = re.compile(r"\[?سورة [^\]\[]{1,40}\(\d+\)\s*:\s*(?:آية|الآيات)(?:\s*\d+)?(?:\s*(?:الى|إلى)(?:\s*\d+)?)?\s*\]?"
                           r"|^\s*\d{1,3}\]|</span>")
_HEAD_START = re.compile(r"\[سورة [^\]\[]{1,40}\(\d+\)\s*:")
_HEAD_REF = re.compile(r"\[سورة [^\]\[]{1,40}\((\d+)\)\s*:\s*(?:آية|الآيات)\s*(\d+)")


@dataclass
class Unit:
    sura: int
    start: int
    end: int
    words: list[str]                       # birimin ilk kelimelerinin iskeleti (çapa)
    at: int | None = None                  # Shamela kelime dizisindeki yeri
    line: int | None = None                # çapanın satırı (satırlar çapalardan bölündükten sonra)


@dataclass
class Alignment:
    units: int = 0
    anchored: int = 0
    merged: list[str] = field(default_factory=list)      # çapası bulunamayıp öncekine katılanlar


def skeleton_words(text: str) -> list[str]:
    return [w for w in (skeleton(t) for t in text.split()) if w]


def altafsir_units(raw: str) -> tuple[list[Unit], dict[int, str]]:
    """altafsir sürümünün birimleri (kitap sırasıyla) ve sûre adları."""
    units, names, current = [], {}, None
    for line in raw.splitlines():
        if m := _SURA_HEAD.match(line):
            names[int(m[1])] = m[2].strip()
            continue
        if m := _UNIT_HEAD.match(line):
            current = Unit(int(m[1]), int(m[2]), int(m[3] or m[2]), [])
            units.append(current)
            continue
        if current is not None and len(current.words) < ANCHOR_WORDS + 40 and not line.startswith("### "):
            current.words += skeleton_words(_MARKUP.sub(" ", line))
    for unit in units:                  # sûrenin ilk birimi: besmeleye kadarki kalıp künye ("مكية وهي…") çapa olmaz
        if unit.start == 1 and (k := _find(unit.words, _BESMELE)) is not None:
            unit.words = unit.words[k + len(_BESMELE):]
        unit.words = unit.words[:ANCHOR_WORDS]
    return units, names


_BESMELE = skeleton_words("بسم الله الرحمن الرحيم")


def _find(words: list[str], seq: list[str]) -> int | None:
    return next((i for i in range(len(words) - len(seq) + 1) if words[i:i + len(seq)] == seq), None)


def anchor(units: list[Unit], words: list[str]) -> Alignment:
    """Her birimin Shamela kelime dizisindeki başı; bulunamayan `at = None`.

    1. Adaylar: birimin ilk kelimelerindeki her 5'li dizi (birim kısaysa 3'lü de) kitabın her yerinde aranır; dizinin
       yeri eksi birim içindeki konumu bir aday yerdir. Adayın puanı, onu (±3 kelime) gösteren dizilerin 1/sıklık
       toplamıdır: kitapta tek geçen dizi 1, on kez geçen 0,1 sayar (Kur'ân'da ve tefsirde defalarca geçen söz yeri
       belirleyemez). Puanı en az 1 olan en güçlü beş aday tutulur.
    2. Sıra: bütün birimler için, yerleri kitap sırasıyla artan ve puan toplamı en büyük aday zinciri seçilir
       (en uzun artan dizi, eşitlikte puan). Tek bir yanlış aday (başka bir sûrede aynı söz) sıraya uymadığı için seçilmez,
       sonraki birimleri de sürükleyemez. Zincire girmeyen birim çapasızdır."""
    index: dict[str, list[int]] = {}
    for n in (GRAM, SHORT_GRAM):
        for i in range(len(words) - n + 1):
            index.setdefault(" ".join(words[i:i + n]), []).append(i)
    cands: list[list[tuple[int, float]]] = []
    for unit in units:
        weight: dict[int, float] = {}
        for n in ((GRAM, SHORT_GRAM) if len(unit.words) < 2 * GRAM + 2 else (GRAM,)):
            for off in range(0, max(0, min(len(unit.words), ANCHOR_WORDS) - n + 1)):
                places = index.get(" ".join(unit.words[off:off + n]))
                if not places or len(places) > MAX_PLACES:
                    continue
                for place in places:
                    if place - off >= 0:
                        weight[place - off] = weight.get(place - off, 0.0) + 1.0 / len(places)
        scored = []
        for c in weight:
            score = sum(v for d, v in weight.items() if abs(d - c) <= 3)
            if score >= MIN_SCORE:
                scored.append((c, min(score, 3.0)))
        scored.sort(key=lambda x: -x[1])
        kept, used = [], []
        for c, sc in scored:                       # yakın adaylar tek sayılır
            if all(abs(c - u) > 3 for u in used):
                kept.append((c, sc))
                used.append(c)
            if len(kept) == 5:
                break
        cands.append(kept)
    chosen = _chain(cands)
    report = Alignment(units=len(units))
    for unit, at in zip(units, chosen):
        unit.at = at
        if at is None:
            report.merged.append(f"{unit.sura}:{unit.start}" + (f"-{unit.end}" if unit.end != unit.start else ""))
        else:
            report.anchored += 1
    return report


def _chain(cands: list[list[tuple[int, float]]]) -> list[int | None]:
    """Birim sırasıyla, yerleri kesin artan seçim (her birimden en çok bir aday): önce zincire giren birim sayısı en
    büyük, eşitlikte puan toplamı (her birim 1 + puan/10; puan en çok 3 olduğu için bir birim kaybı puanla telafi edilemez).
    Fenwick ağacıyla: yerler sıkıştırılır, her aday kendinden küçük yerlerdeki en iyi zincire eklenir."""
    positions = sorted({c for row in cands for c, _ in row})
    rank = {p: i + 1 for i, p in enumerate(positions)}
    size = len(positions)
    tree_val = [0.0] * (size + 1)
    tree_at: list[tuple[int, int] | None] = [None] * (size + 1)
    back: dict[tuple[int, int], tuple[int, int] | None] = {}

    def query(i: int) -> tuple[float, tuple[int, int] | None]:
        best, at = 0.0, None
        while i > 0:
            if tree_val[i] > best:
                best, at = tree_val[i], tree_at[i]
            i -= i & -i
        return best, at

    def update(i: int, val: float, at: tuple[int, int]) -> None:
        while i <= size:
            if val > tree_val[i]:
                tree_val[i], tree_at[i] = val, at
            i += i & -i

    best_total, best_end = 0.0, None
    for u, row in enumerate(cands):
        found = []
        for k, (c, sc) in enumerate(row):
            prev_val, prev_at = query(rank[c] - 1)
            found.append((rank[c], prev_val + 1.0 + sc / 10.0, (u, k), prev_at))   # önce birim sayısı, sonra puan
        for r, val, key, prev_at in found:       # aynı birimin adayları birbirine zincirlenmez
            back[key] = prev_at
            update(r, val, key)
            if val > best_total:
                best_total, best_end = val, key
    chosen: list[int | None] = [None] * len(cands)
    key = best_end
    while key is not None:
        u, k = key
        chosen[u] = cands[u][k][0]
        key = back[key]
    return chosen


def _ranges(units: list[Unit], counts: dict[int, int]) -> list[Unit]:
    """Çapalı birimler, aralıkları sonrakinin başına (ya da sûrenin sonuna) kadar genişlemiş hâlde."""
    kept = [u for u in units if u.at is not None]
    out = []
    for i, u in enumerate(kept):
        nxt = kept[i + 1] if i + 1 < len(kept) else None
        end = (nxt.start - 1) if nxt and nxt.sura == u.sura else counts[u.sura]
        out.append(Unit(u.sura, u.start, max(u.end, end), u.words, u.at, u.line))
    return out


def parse(work: Work, key: str | None = None, raw_root=RAW_DIR / "openiti") -> tuple[Book, Report]:
    key = key or work.source.book
    base = key.removesuffix("-shamela")
    doc = openiti.load(key, raw_root)
    units, names = altafsir_units((raw_root / f"{base}-altafsir.txt").read_text(encoding="utf-8"))
    P = _split_at_headings(doc.paragraphs)
    words, word_pos = [], []                       # kelime iskeleti ve (satır, satırdaki karakter yeri)
    for i, p in enumerate(P):
        for m in re.finditer(r"\S+", p.text or ""):
            if w := skeleton(m.group(0)):
                words.append(w)
                word_pos.append((i, m.start()))
    report = Report()
    align = anchor(units, words)
    quran = Quran.load()
    for u in units:                    # âyetin sözü çapanın hemen önündeyse (aynı satırda) birimin başıdır
        if u.at is None:
            continue
        verse, k = _verse_words(quran, u), 0
        while k < 60 and u.at - k - 1 >= 0 and word_pos[u.at - k - 1][0] == word_pos[u.at][0] \
                and words[u.at - k - 1] in verse:
            k += 1
        if k >= 2:
            u.at -= k
            report.verse_backed = getattr(report, "verse_backed", 0) + 1
    P, unit_line = _split_lines(P, [word_pos[u.at] if u.at is not None else None for u in units])
    for u, line in zip(units, unit_line):
        u.line = line
    counts = quran.counts
    spans = _ranges(units, counts)
    report.alignment = align
    book = Book(work.slug, work.title, {"group": str(work.group), "language": work.language,
                                        "source": {"site": str(work.source.site), "book": work.source.book}})
    book.notes.append({"node_id": book.root.id, "after": None,
                       "text": FRONT_TAKEN_NOTE if work.slug in FRONT else FRONT_NOTE})
    if align.merged:
        book.notes.append({"node_id": book.root.id, "after": None,
                           "text": f"altafsir sürümünde olup Shamela metninde başı bulunamayan {len(align.merged)} birim "
                                   f"öncekine katıldı (aralığı genişledi): {', '.join(align.merged[:50])}"
                                   + (" …" if len(align.merged) > 50 else "")})
    edition = doc.edition.get("editor") or doc.edition.get("publisher") or "Shamela sürümünden"
    subtitle = UNIT_SUBTITLE.format(edition=f"{edition}" if edition.startswith("Shamela") else f"baskıdan ({edition})")
    starts = [_start_line(P, u.line, u, _verse_words(quran, u)) for u in spans]
    # baskının numaralı birim başlığı ("[سورة الفجر (89) : الآيات 15 …") çapadan güçlü kanıttır: birimin kendi
    # başlığı başından sonra ve sonraki birimden önce duruyorsa birim oradan başlar
    for n, u in enumerate(spans):
        limit = starts[n + 1] if n + 1 < len(spans) else len(P)
        own = next((i for i in range(starts[n] + 1, min(limit, starts[n] + 80))
                    if (m := _HEAD_REF.search(P[i].text or "")) and (int(m[1]), int(m[2])) == (u.sura, u.start)), None)
        if own is not None:
            starts[n] = own
            report.moved_units = getattr(report, "moved_units", 0) + 1
    # birim kendi aralığından önceki bir âyet satırıyla başlıyorsa (çapa erken düştü) kendi âyet satırına ilerler
    for n, u in enumerate(spans):
        limit = starts[n + 1] if n + 1 < len(spans) else len(P)
        first_verse = next((i for i in range(starts[n], min(limit, starts[n] + 400)) if _verse_numbers(P[i])), None)
        if first_verse is not None and max(_verse_numbers(P[first_verse])) < u.start:
            own = next((i for i in range(first_verse, min(limit, starts[n] + 400))
                        if _verse_numbers(P[i]) and min(_verse_numbers(P[i])) >= u.start), None)
            if own is not None:
                starts[n] = own
                report.moved_units = getattr(report, "moved_units", 0) + 1
    # ön metin (`FRONT`): kısımlar, yeni birimler, ilk birimin erken başı
    front_end = starts[0] if starts else 0
    segs = _front_segments(P[:front_end], FRONT.get(work.slug, []))
    if drop := DROP_UNITS.get(work.slug):
        kept = [k for k, u in enumerate(spans) if u.sura not in drop]
        spans, starts = [spans[k] for k in kept], [starts[k] for k in kept]
    front_units = {}
    for f, idx in reversed([(f, i) for f, i in segs if f.kind == "unit"]):
        u = Unit(*f.verses, [])
        spans.insert(0, u)
        starts.insert(0, idx)
        front_units[id(u)] = P[idx].text.strip()
    for f, idx in segs:
        if f.kind == "prepend":
            starts[0] = idx
    # iki birimin başı aynı satıra düştüyse satır bölünmez: birimler tek aralıkta birleşir
    merged_spans, merged_starts = [], []
    for u, st in zip(spans, starts):
        if merged_starts and merged_starts[-1] >= st and merged_spans[-1].sura == u.sura:
            prev = merged_spans[-1]
            merged_spans[-1] = Unit(prev.sura, prev.start, max(prev.end, u.end), prev.words, prev.at, prev.line)
            report.joined_units = getattr(report, "joined_units", 0) + 1
            continue
        merged_spans.append(u)
        merged_starts.append(st)
    spans, starts = merged_spans, merged_starts
    # noktalaması seyrek eserde kaynağın paragrafları korunur (cümle sonuna kadar birleştirilmez)
    marks = sum(sum(p.text.count(c) for c in ".؟!") for p in P)
    keep_source = marks < len(words) / 100
    report.keep_source_paragraphs = keep_source
    # sûre başı: Shamela'da sûrenin adıyla başlayan kısa satır (başlık ya da düz satır), sırayla aranır. Sûrenin ilk
    # birimi bu satırdan önceye düşemez; düşmüşse sûrenin kendi âyet satırına (yoksa satırın ardına) ilerler.
    heads = {}
    sura_lines = _sura_lines(P, names)
    for n in range(1, len(spans)):
        if spans[n].sura == spans[n - 1].sura or (head := sura_lines.get(spans[n].sura)) is None:
            continue
        if not starts[n - 1] < head < (starts[n + 1] if n + 1 < len(spans) else len(P)):
            continue                                     # sıraya uymuyor: güvenilmez, kullanılmaz
        heads[n] = head
        if starts[n] <= head:
            limit = starts[n + 1] if n + 1 < len(spans) else len(P)
            own = next((i for i in range(head + 1, min(limit, head + 60))
                        if _verse_numbers(P[i]) and spans[n].start in range(min(_verse_numbers(P[i])),
                                                                            max(_verse_numbers(P[i])) + 1)), None)
            starts[n] = own if own is not None else head + 1
            report.moved_units = getattr(report, "moved_units", 0) + 1
    first_seg = segs[0][1] if segs else (starts[0] if starts else 0)
    report.front_words = sum(len(p.text.split()) for p in P[:first_seg] if p.text)
    report.front = P[:starts[0]] if starts else []
    report.front_parts = [(f.kind, f.local or f.kind, i) for f, i in segs]
    report.heading_words = sum(len(" ".join(m.group(0) for m in _EDITION_HEAD.finditer(p.text)).split())
                               for p in P if p.text)
    w = Writer(book, report)
    bounds = [i for _, i in segs] + [starts[0] if starts else len(P)]
    sura_text = None
    for k, (f, idx) in enumerate(segs):
        end = min(bounds[k + 1], starts[0]) if starts else bounds[k + 1]
        if f.kind == "sura":
            sura_text = (idx, end)
        if f.kind not in ("mukaddime", "tahkik"):
            continue
        node = book.add_node(book.root, f.local or "mukaddime", f.title,
                             **({"subtitle": f.subtitle} if f.subtitle else
                                {"subtitle": f"Muhakkikin girişi ({f.by or work.editor}): müellifin metni değil"}
                                if f.kind == "tahkik" else {"subtitle": NO_TITLE} if not f.printed else {}))
        if f.kind == "tahkik":
            node.extra.update({"authority": "muhakkik", "by": f.by or work.editor})
        w.start(node)
        for i in range(idx, end):
            text = (P[i].text or "").strip()
            if (i - idx < 3 and _title_line(P[i], f.title) or _FRONT_JUNK.match(text)
                    or text.startswith("سورة") and len(text.split()) <= 3):
                continue
            _write(w, P[i], keep_source)
    sura_node = None
    for n, unit in enumerate(spans):
        last = len(P) if n + 1 == len(spans) else (heads.get(n + 1) or starts[n + 1])
        if sura_node is None or sura_node.number != unit.sura:
            sura_node = book.add_node(book.root, str(unit.sura), names.get(unit.sura, f"سورة {unit.sura}"),
                                      number=unit.sura)
            w.start(sura_node)
            if heads.get(n) is not None:                 # sûrenin kendi metni: başlıktan ilk birime
                for i in range(heads[n] + 1, starts[n]):
                    _write(w, P[i], keep_source)
            elif n == 0 and sura_text:                   # Fâtiha'nın ön metindeki kendi metni
                a, b = sura_text
                fatiha = _verse_words(quran, Unit(unit.sura, 1, counts[unit.sura], []))
                for i in range(a, b):
                    p, text = P[i], (P[i].text or "").strip()
                    if (i == a and text.startswith("سورة") and len(text.split()) <= 6
                            or text.startswith("سورة") and len(text.split()) <= 3 or _FRONT_JUNK.match(text)):
                        continue
                    if _verse_numbers(p) and not p.level and _is_own_verse_text(p, fatiha):
                        w.ayah([p], _verse_range(unit.sura, p))
                    else:
                        _write(w, p, keep_source)
        local = f"{unit.start}" + (f"-{unit.end}" if unit.end != unit.start else "")
        title = f"آية {unit.start}" if unit.end == unit.start else f"الآيات {unit.start} الى {unit.end}"
        own = front_units.get(id(unit))
        node = book.add_node(sura_node, local, title, subtitle=FRONT_UNIT_SUBTITLE.format(
            line=own, edition=subtitle.split("metin ve sayfa ", 1)[1]) if own else subtitle)
        node.extra["verses"] = {"sura": unit.sura, "start": unit.start, "end": unit.end}
        w.start(node)
        opening = True                                   # âyet satırı yalnız birimin başında `ayah` olur
        for i in range(starts[n], last):
            p = P[i]
            if opening and _is_verse_line(p, unit):
                w.ayah([p], _verse_range(unit.sura, p))
                continue
            if p.text:
                opening = False
            _write(w, p, keep_source)
        report.units += 1
    w.flush()
    for node in book.nodes():
        first = next((r for r in book.paragraphs if r["node_id"] == node.id and r.get("printed")), None)
        if node.extra.get("verses") and first:
            node.extra["printed"] = {k: first["printed"][k] for k in ("volume", "page")}
    return book, report


def _cut(p: openiti.Paragraph, cut: int) -> tuple[openiti.Paragraph, openiti.Paragraph]:
    """Satırı karakter yerinden ikiye böler; sayfa sonları paylaşılır, ikinci parçanın sayfası kestiği yerden önceki son
    sayfa sonundan sonraki sayfadır (OpenITI'nin işareti sayfanın sonudur)."""
    before = [(at, pg) for at, pg in p.breaks if at <= cut]
    after = [(at - cut, pg) for at, pg in p.breaks if at > cut]
    page2 = openiti.Page(before[-1][1].volume, before[-1][1].page + 1) if before else p.page
    return (openiti.Paragraph(p.raw, p.text[:cut].rstrip(), None, [], before, p.page,
                              before[-1][1] if before else p.page, p.entity),
            openiti.Paragraph(p.raw, p.text[cut:], None, [], after, page2, p.end_page, p.entity))


def _split_lines(P: list[openiti.Paragraph], at: list[tuple[int, int] | None]) -> tuple[list, list]:
    """Birimlerin çapası satırın ortasındaysa satır oradan bölünür (önceki birimin şerhi öncekinde kalır). Yeni satır
    listesi ve her birimin çapa satırı döner."""
    cuts: dict[int, set[int]] = {}
    for pos in at:
        if pos and pos[1] > 0 and P[pos[0]].text[:pos[1]].strip() and not P[pos[0]].level:
            cuts.setdefault(pos[0], set()).add(pos[1])
    out, where = [], {}
    for i, p in enumerate(P):
        offsets = sorted(cuts.get(i, ()))
        if not offsets:
            where[(i, 0)] = len(out)
            out.append(p)
            continue
        where[(i, 0)] = len(out)
        rest, base = p, 0
        for off in offsets:
            head, rest = _cut(rest, off - base)
            out.append(head)
            where[(i, off)] = len(out)
            base = off
        out.append(rest)
    lines = []
    for pos in at:
        if pos is None:
            lines.append(None)
        else:
            lines.append(where.get(pos, where[(pos[0], 0)]))
    return out, lines


def _split_at_headings(P: list[openiti.Paragraph]) -> list[openiti.Paragraph]:
    """Satırın ortasında baskının birim başlığı ("[سورة الفجر (89) : الآيات 15 …") varsa satır oradan bölünür:
    öncesi önceki âyetin şerhidir, sonrası yeni birimin başı. Sayfa: başlıktan önceki son sayfa sonundan sonraki
    sayfa (OpenITI'nin işareti sayfanın sonudur)."""
    out = []
    for p in P:
        m = _HEAD_START.search(p.text) if p.text and not p.level else None
        if not m or m.start() == 0 or not p.text[:m.start()].strip():
            out.append(p)
            continue
        out.extend(_cut(p, m.start()))
    return out


def _sura_lines(P: list[openiti.Paragraph], names: dict[int, str]) -> dict[int, int]:
    """Her sûrenin Shamela'daki baş satırı: adıyla (iskelet) başlayan, en çok 20 kelimelik satır; sûreler sırayla,
    her biri öncekinden sonra aranır. Bulunamayan sûre yoktur sayılır."""
    out, at = {}, 0
    keys = {n: skeleton_words(name) for n, name in names.items()}
    for n in sorted(keys):
        want = keys[n]
        if len(want) < 2:
            continue
        for i in range(at, len(P)):
            if not P[i].text or _UNIT_REF.search(P[i].text):      # baskının birim başlığı sûre başı değildir
                continue
            ws = skeleton_words(P[i].text)
            if ws[:len(want)] == want and len(ws) <= 20:
                out[n], at = i, i + 1
                break
    return out


def _clean(p: openiti.Paragraph) -> openiti.Paragraph:
    """Baskının birim başlığı parçaları metinden atılır (başlık bilgisi düğümdedir); satırın geri kalanı kalır.
    Atılan yerden sonraki sayfa sonu konumları kaydırılır."""
    if not _EDITION_HEAD.search(p.text):
        return p
    text, breaks, shift, last = "", [], 0, 0
    for m in _EDITION_HEAD.finditer(p.text):
        text += p.text[last:m.start()]
        last = m.end()
    text += p.text[last:]
    removed = len(p.text) - len(text)
    breaks = [(max(0, at - removed), page) for at, page in p.breaks]
    return openiti.Paragraph(p.raw, " ".join(text.split()), p.level, p.quran, breaks, p.page, p.end_page, p.entity)


def _write(w: Writer, p: openiti.Paragraph, keep_source: bool = False) -> None:
    """Satır: başlık kendi paragrafını açar (birimin ilk paragrafı olabilir), metin satırı açık paragrafa eklenir;
    noktalaması seyrek eserde her kaynak paragrafı yeni paragraf açar."""
    p = _clean(p)
    if not p.text:
        if p.breaks and w.open is not None:
            w.open.add_break(p)
        return
    if p.level or p.entity:
        if p.text:
            w.line(openiti.Paragraph(p.raw, p.text, None, [], p.breaks, p.page, p.end_page), force_new=True)
    else:
        w.line(p, force_new=keep_source)


def _verse_numbers(p: openiti.Paragraph) -> list[int]:
    text = _EDITION_HEAD.sub(" ", p.text)
    return [int(x) for x in _VERSE_NO.findall(text)] if p.text and _VERSE_LINE.search(text) else []


def _is_verse_line(p: openiti.Paragraph, unit: Unit) -> bool:
    """Birimin âyet satırı: sonu "(n)", ilk numarası birimin aralığında (satır sonraki âyetlere taşabilir: baskının
    birimi altafsir'inkinden geniş olabilir)."""
    numbers = _verse_numbers(p)
    return bool(numbers) and unit.start <= min(numbers) <= unit.end and not p.level


def _verse_range(sura: int, p: openiti.Paragraph) -> str:
    numbers = sorted(set(_verse_numbers(p)))
    return f"quran:{sura}:{numbers[0]}" + (f"-{numbers[-1]}" if numbers[-1] != numbers[0] else "")


def _verse_words(quran: Quran, unit: Unit) -> set[str]:
    """Birimin âyetlerinin kelimeleri (iskelet)."""
    out = set()
    for a in range(unit.start, unit.end + 1):
        if (unit.sura, a) in quran.ayahs:
            out |= set(skeleton_words(quran.ayahs[(unit.sura, a)]["text_clean"]))
    return out


def _is_own_verse_text(p: openiti.Paragraph, verse: set[str]) -> bool:
    """Numarasız âyet satırı: kelimelerinin en az %80'i birimin âyetlerinden (en az 2 kelime)."""
    ws = skeleton_words(_VERSE_NO.sub(" ", p.text or ""))
    return len(ws) >= 2 and sum(w in verse for w in ws) >= 0.8 * len(ws)


def _start_line(P: list[openiti.Paragraph], line: int, unit: Unit, verse: set[str] = frozenset()) -> int:
    """Çapanın satırından geri: önündeki âyet satırları (numaralı ya da kelimeleri birimin âyetinden), yalnız sayfa
    işareti olan satırlar ve başlıklar birimindir."""
    i = line
    while i > 0:
        p = P[i - 1]
        if not p.text or (p.level and "سورة" not in p.text) or _is_verse_line(p, unit) \
                or (verse and not p.level and _is_own_verse_text(p, verse)):
            i -= 1
            continue
        break
    return i


def verify(book_json: dict, quran: Quran, words: int = 300) -> tuple[int, list[str]]:
    """Denetim: her birimin ilk 60 kelimesinde kendi âyetlerinin (iskelet, en az iki harfli) kelimelerinden en az ikisi
    geçiyor mu. Çapa doğruysa geçer (müfessir âyeti ya da lemmasını birimin başında anar; Celâleyn gibi âyeti kelime
    kelime bölen şerhte de). Geçmeyenler listelenir; hüküm değil, bakılacak yer."""
    by_node: dict[str, list[str]] = {}
    for p in book_json["paragraphs"]:
        if (t := p.get("text")) and len(by_node.setdefault(p["node_id"], [])) < words:
            by_node[p["node_id"]] += skeleton_words(_MARKUP.sub(" ", t))
    checked, failed = 0, []
    for node in book_json["outline"]:
        v = node.get("verses")
        if not v:
            continue
        checked += 1
        verse = set()
        for a in range(v["start"], v["end"] + 1):
            verse |= {w for w in skeleton_words(quran.ayahs[(v["sura"], a)]["text_clean"]) if len(w) >= 2}
        head = set(by_node.get(node["id"], [])[:60])
        need = min(2, len(verse)) or 1
        if len(head & verse) < need:
            failed.append(node["id"])
    return checked, failed
