"""Hadis kitapları: OpenITI JK baskılarından kitap, bâb ve hadis (`docs/hadis-kitaplari-plani.md`, 2b ilk dilim).

    uv run python -m risale_mcp.fetch hadis          # data/raw/openiti/<kitap>.txt (sabit commit)
    uv run python -m risale_mcp.hadis_kutub          # data/library/hadis/kutub/<kitap>.json, rapor data/interim/hadis/kutub.md

Risale'ye bağlı değildir; `hadis` profilinin temelidir. Lisans CC BY-NC-SA 4.0 (OpenITI): kaynak dosyada yazılıdır.

OpenITI biçimi (mARkdown): üst bilgi `#META#Header#End#` satırında biter; paragraf `# ` ile başlar, `~~` ile süren
satırlar paragrafın devamıdır. Baskılara göre başlık yazılışı:

    ### | ( 2 كتاب الإيمان )            kitap (Buhârî, Tirmizî, Nesâî)
    ### || ( 3 باب … )                  bâb
    ### ||| 5                          Tirmizî: hadis numarası, metni sonraki paragraf
    # | 1 ( 2 كتاب الطهارة )            kitap (Müslim, İbn Mâce, Ebû Dâvûd, Muvatta)
    # | 1 ( 4 باب … )  # | 1 ( 2 النداء في السفر )   bâb; numaralı başlıksız "باب" da bâbdır
    # 1 كتاب الطهارة                    Ebû Dâvûd'un ilk kitabı (kısa satır)
    # 12 حدثنا …                        hadis 12; numarasız paragraf önceki hadisin devamıdır (Müslim'de öbür tarikler)

Okuma ortak OpenITI okuyucusuyla (`openiti.py`, H6): işaretler atılır (metin değişmez), âyet işareti
`@QB@ … @QE@` "﴿ … ﴾" olur. Sayfa işaretinden hadisin basılı cildi ve sayfası (`printed`: {volume, page}, birden çok
sayfaya yayılıyorsa `end` "1/4"); sayfalar üst bilgideki baskınındır (`source.edition`), ikincil bilgidir, kimliğe
girmez. HA3'te sayfayla verilen künyeler (Müsned'de cilt:sayfa) bunu kullanır. Senet ile metin ilk " * " işaretinden
ayrılır; işaret yoksa `isnad` boştur. "# | 1 ( قال … )" gibi numarasız ve "باب/كتاب" taşımayan ayraçlı satır başlık
değildir (Müslim'de metnin parçası): önceki hadise eklenir.

Kimlik: hadis `bukhari/52` (baskının numarası), düğüm `bukhari/k02` ve `bukhari/k02/b003` (sıra; basılı numara
`number`'da). Bâb numarası künyelerdeki ("Ezân: 148") bâb numarasıdır; kitabın içinde yeniden başlar.
"""

import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from risale_mcp import openiti
from risale_mcp.paths import INTERIM_DIR, LIBRARY_DIR, RAW_DIR
from risale_mcp.sources.hadis import OPENITI_BOOKS, OPENITI_COMMITS

KUTUB_DIR = LIBRARY_DIR / "hadis" / "kutub"
TITLES = {"bukhari": "Sahîh-i Buhârî", "muslim": "Sahîh-i Müslim", "abudawud": "Sünen-i Ebû Dâvûd",
          "tirmidhi": "Sünen-i Tirmizî", "nasai": "Sünen-i Nesâî", "ibnmajah": "Sünen-i İbn Mâce", "malik": "Muvatta"}
LICENCE = "CC BY-NC-SA 4.0"
MAX_DIGITS = 6               # daha uzun "numara" birleşmiş dizgi hatasıdır
MAX_GAP = 50                 # bundan büyük numara boşluğu yanlış okunmuş numaradır, rapora ayrı yazılır

_LEVEL = re.compile(r"^###\s*(\|+)\s*(.*)$")
_PIPE = re.compile(r"^#\s*\|\s*\d*\s*(.*)$")               # "# | 1 ( … )" ya da "# | 1 - كتاب …"
_NUMBERED = re.compile(r"^#\s+(\d+)\s+(.*)$")
_HEAD = re.compile(r"^[(\s-]*(\d+)?\s*-?\s*(.*?)[\s)]*$")
_KITAB = re.compile(r"^(?:كتاب|أبواب|ابواب|كتب)\b")
_BAB = re.compile(r"^(?:باب|أبواب|ابواب|جماع أبواب|فضل)\b")


@dataclass
class Node:
    id: str
    parent_id: str | None
    level: str                   # kitab | bab
    number: int | None
    title: str


@dataclass
class Hadith:
    id: str
    number: int
    node_id: str
    paragraphs: list[str] = field(default_factory=list)
    page: openiti.Page | None = None                  # basılı sayfa: başladığı ve bittiği
    end_page: openiti.Page | None = None


def clean(text: str) -> str:
    return openiti.clean(text)[0]


def paragraphs(raw: str) -> list[str]:
    """Üst bilgiden sonraki paragraflar; `~~` satırları öncekine eklenir."""
    return openiti.raw_paragraphs(openiti.split_header(raw)[1])


def heading(text: str) -> tuple[str, int | None, str] | None:
    """Ayraçlı başlık metni -> (kitab | bab, basılı numara, başlık); başlık değilse None."""
    text = clean(text)
    m = _HEAD.match(text)
    number, title = (int(m[1]) if m[1] else None), clean(m[2]).strip("() ")
    if _KITAB.match(title):
        return "kitab", number, title
    if _BAB.match(title) or (number is not None and title):
        return "bab", number, title
    return None


def parse(book: str, raw: str) -> tuple[list[Node], list[Hadith], Counter]:
    nodes: list[Node] = []
    hadiths: list[Hadith] = []
    stats = Counter()
    kitab: Node | None = None
    current: Node | None = None
    pending_number: int | None = None          # Tirmizî: "### ||| N", metin sonraki paragraf
    seen_numbers: Counter = Counter()

    def open_kitab(number: int | None, title: str) -> None:
        nonlocal kitab, current
        kitab = Node(f"{book}/k{sum(n.level == 'kitab' for n in nodes) + 1:02d}", None, "kitab", number, title)
        nodes.append(kitab)
        current = kitab

    def open_bab(number: int | None, title: str) -> None:
        nonlocal current
        if kitab is None:
            open_kitab(None, "")
        count = sum(n.level == "bab" and n.parent_id == kitab.id for n in nodes) + 1
        current = Node(f"{kitab.id}/b{count:03d}", kitab.id, "bab", number, title)
        nodes.append(current)

    def add_text(text: str) -> None:
        if hadiths and (text := clean(text)):
            hadiths[-1].paragraphs.append(text)
            hadiths[-1].end_page = para.end_page or hadiths[-1].end_page
            stats["devam"] += 1
        elif text:
            stats["hadis_oncesi"] += 1

    def start_hadith(number: int, text: str) -> None:
        if current is None:
            open_kitab(None, "")
        # Aynı numaranın sonraki tarikleri (Müslim'de Abdülbaki'nin ana numarası tekrarlanır) "-2", "-3" eki alır.
        seen_numbers[number] += 1
        suffix = f"-{seen_numbers[number]}" if seen_numbers[number] > 1 else ""
        hadiths.append(Hadith(f"{book}/{number}{suffix}", number, current.id, [clean(text)] if clean(text) else [],
                              para.page, para.end_page))

    doc = openiti.read(raw)
    for para in doc.paragraphs:
        p = para.raw
        if m := _LEVEL.match(p):
            depth, text = len(m[1]), m[2]
            if depth == 3 and (n := re.match(r"\s*(\d+)\s*$", clean(text))):
                pending_number = int(n[1])
                continue
            head = heading(text)
            kind = head[0] if head else None
            if depth == 1 and head and (kind == "kitab" or book != "malik"):
                open_kitab(head[1], head[2])
            elif head and depth >= 2:
                open_bab(head[1], head[2])
            elif depth == 1 and not hadiths:
                stats["baslik_disi"] += 1         # eser adı, mukaddime başlığı
            else:
                add_text(text)
            continue
        if m := _PIPE.match(p):
            head = heading(m[1])
            if head and head[0] == "kitab":
                open_kitab(head[1], head[2])
            elif head:
                open_bab(head[1], head[2])
            else:
                add_text(m[1])
            continue
        body = p.lstrip("#").strip()
        if pending_number is not None:
            start_hadith(pending_number, body)
            pending_number = None
            continue
        if m := _NUMBERED.match(p):
            number, rest = int(m[1]), m[2]
            # Kaynağın dizgi hatası: "# 291429132913 2913 …" (Müslim'de 2 satır); asıl numara ardındaki sayıdır.
            if len(m[1]) > MAX_DIGITS and (n := re.match(r"(\d+)\s+(.*)$", rest)):
                number, rest = int(n[1]), n[2]
                stats["birlesik_numara"] += 1
            if _KITAB.match(clean(rest)) and len(clean(rest)) < 60:   # Ebû Dâvûd: "# 1 كتاب الطهارة"
                open_kitab(number, clean(rest))
                continue
            start_hadith(number, rest)
            continue
        add_text(body)
    stats["sayfasiz"] = sum(h.page is None for h in hadiths)
    return nodes, hadiths, stats


# Muvatta'nın JK baskısı hadisin sonuna muhakkikin tahric kodlarını koyar ("س 1 - 16 ت 8 - 10"): metin değildir.
_REFS = re.compile(r"(?:\s+[\u0621-\u064A]{1,2}(?:\s+\d+(?:\s*-\s*\d+)*)+)+\s*$")


def split_refs(text: str) -> tuple[str, str]:
    m = _REFS.search(text)
    return (text[:m.start()].rstrip(), m.group().strip()) if m else (text, "")


def split(text: str) -> tuple[str, str]:
    """Senet ve metin: ilk " * " işareti; yoksa senet boş."""
    if " * " in f" {text} ":
        isnad, _, matn = text.partition("*")
        return isnad.strip(), matn.strip().replace(" * ", " ")
    return "", text


def to_json(book: str, nodes: list[Node], hadiths: list[Hadith], edition: dict | None = None) -> dict:
    """`edition`: sayfa numaralarının ait olduğu baskı (`openiti.Document.edition`)."""
    repo, path = OPENITI_BOOKS[book]
    records = []
    for h in hadiths:
        parts = [split_refs(p) for p in h.paragraphs]
        text = " ".join(t for t, _ in parts)
        isnad, matn = split(parts[0][0] if parts else "")
        record = {"id": h.id, "number": h.number, "node_id": h.node_id, "isnad": isnad, "matn": matn, "text": text}
        if refs := [r for _, r in parts if r]:
            record["refs"] = " ".join(refs)
        if h.page:
            record["printed"] = {"volume": h.page.volume, "page": h.page.page,
                                 **({"end": str(h.end_page)} if h.end_page and h.end_page != h.page else {})}
        records.append(record)
    return {"book": book, "title": TITLES[book],
            "source": {"name": "OpenITI (KITAB project)", "file": f"{repo}/data/{path}", "commit": OPENITI_COMMITS[repo],
                       "licence": LICENCE, **({"edition": edition} if edition else {})},
            "outline": [{"id": n.id, "parent_id": n.parent_id, "level": n.level, "number": n.number, "title": n.title}
                        for n in nodes],
            "hadiths": records}


TAIL = 20                    # karşılıkta karşılaştırılan metin sonu (iskelet harfi)


def align(data: dict, api_hadiths: list[dict]) -> Counter:
    """Her hadise Hadith API numarası (`api`) ve her kitaba API bölümü (`api_section`), metinden.

    Anahtar metnin son `TAIL` iskelet harfidir (`quran.skeleton`: hareke ve zayıf harfler atılır; JK harekesiz, API
    harekelidir); hem bütün metnin hem ilk paragrafın sonu denenir. Birden çok aday varsa (aynı sözle biten tekrarlar)
    kitap sırasıyla ilerlenir: bir önceki karşılığa en yakın numara seçilir. Kitap bölümü, kitabın hadislerinin
    karşılıklarından çoğunlukla seçilir."""
    from risale_mcp.quran import skeleton
    tails: dict[str, list[dict]] = {}
    for h in api_hadiths:
        if len(s := skeleton(h.get("text") or "")) >= TAIL:
            tails.setdefault(s[-TAIL:], []).append(h)
    stats, last = Counter(), 0
    votes: dict[str, Counter] = {}
    parent = {n["id"]: n["parent_id"] or n["id"] for n in data["outline"]}
    for r in data["hadiths"]:
        keys = {skeleton(r["text"])[-TAIL:], skeleton(r["matn"] or r["text"])[-TAIL:]}
        cands = {h["hadithnumber"]: h for k in keys for h in tails.get(k, ())}
        if not cands:
            stats["eslesmeyen"] += 1
            continue
        number = min(cands, key=lambda n: (abs(n - (last + 1)), n))
        stats["belirsiz" if len(cands) > 1 else "tek"] += 1
        stats["ayni_numara"] += number == r["number"]
        r["api"] = number
        last = number
        if section := (cands[number].get("reference") or {}).get("book"):
            votes.setdefault(parent[r["node_id"]], Counter())[section] += 1
    for n in data["outline"]:
        if n["level"] == "kitab" and (v := votes.get(n["id"])):
            n["api_section"], top = v.most_common(1)[0]
            # JK bazı kitapları birleştirir (Ebû Dâvûd'un Salât'ı API'de birkaç bölüm): kapsanan bölümlerin hepsi.
            n["api_sections"] = sorted(sec for sec, c in v.items() if c >= max(3, sum(v.values()) // 20))
            stats["bolum_oyu_azinlik"] += sum(v.values()) - top
    return stats


def check(hadiths: list[Hadith]) -> dict:
    numbers = [h.number for h in hadiths]
    seen = Counter(numbers)
    top = max(numbers, default=0)
    return {"hadis": len(numbers), "en_buyuk": top, "tekrar": sorted(n for n, c in seen.items() if c > 1)[:20],
            "tekrar_sayisi": sum(c - 1 for c in seen.values() if c > 1),
            # Eksikler ardışık numaralar arasındaki boşluklardan sayılır: yanlış okunmuş büyük bir sayı belleği doldurmasın.
            "eksik_sayisi": sum(max(0, b - a - 1) for a, b in zip(sorted(seen), sorted(seen)[1:]) if b - a <= MAX_GAP),
            "buyuk_bosluk": [(a, b) for a, b in zip(sorted(seen), sorted(seen)[1:]) if b - a > MAX_GAP][:10],
            "geri_giden": sum(1 for a, b in zip(numbers, numbers[1:]) if b < a)}


def build(raw_dir: Path = RAW_DIR / "openiti", out_dir: Path = KUTUB_DIR) -> dict[str, dict]:
    out_dir.mkdir(parents=True, exist_ok=True)
    report = {}
    for book in OPENITI_BOOKS:
        raw = (raw_dir / f"{book}.txt").read_text(encoding="utf-8")
        nodes, hadiths, stats = parse(book, raw)
        data = to_json(book, nodes, hadiths, openiti.read(raw).edition)
        api_path = RAW_DIR / "hadith_api" / f"ara-{book}.json"
        aligned = align(data, json.loads(api_path.read_text(encoding="utf-8"))["hadiths"]) if api_path.exists() else Counter()
        (out_dir / f"{book}.json").write_text(json.dumps(data, ensure_ascii=False, indent=0), encoding="utf-8")
        report[book] = {"kitap": sum(n.level == "kitab" for n in nodes), "bab": sum(n.level == "bab" for n in nodes),
                        "numarasiz_bab": sum(n.level == "bab" and n.number is None for n in nodes),
                        **check(hadiths), "senetli": sum(bool(r["isnad"]) for r in data["hadiths"]), **stats,
                        "api_karsiligi": sum("api" in r for r in data["hadiths"]), **{f"api_{k}": v for k, v in aligned.items()}}
    return report


def render(report: dict[str, dict]) -> str:
    keys = ("kitap", "bab", "numarasiz_bab", "hadis", "en_buyuk", "eksik_sayisi", "tekrar_sayisi", "geri_giden", "senetli",
            "devam", "hadis_oncesi", "baslik_disi", "birlesik_numara", "api_karsiligi", "api_ayni_numara", "api_belirsiz",
            "api_bolum_oyu_azinlik")
    lines = ["# Hadis kitapları (OpenITI JK)\n", "`docs/hadis-kitaplari-plani.md`. Kaynak: OpenITI, CC BY-NC-SA 4.0.\n",
             "| kitap | " + " | ".join(keys) + " |", "|---" * (len(keys) + 1) + "|"]
    lines += [f"| {b} | " + " | ".join(str(r.get(k, 0)) for k in keys) + " |" for b, r in report.items()]
    lines += ["", "Tekrar eden numaralar (ilk 20):", ""] + [f"- {b}: {r['tekrar']}" for b, r in report.items() if r["tekrar"]]
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------ künye -> bâb

ROUNDS = 50                  # karıştırılmış künye turu


def numbers_of(text: str | None) -> set[int]:
    """Künye numaraları "15,35", "3-5" -> {15, 35}, {3, 4, 5} (aralık en çok 20)."""
    out: set[int] = set()
    for piece in (text or "").replace(" ", "").split(","):
        if m := re.fullmatch(r"(\d+)(?:[-–](\d+))?", piece):
            a, b = int(m[1]), int(m[2] or m[1])
            out |= set(range(a, min(b, a + 20) + 1)) if b >= a else {a}
    return out


def load(out_dir: Path = KUTUB_DIR) -> dict[str, dict]:
    return {b: json.loads((out_dir / f"{b}.json").read_text("utf-8")) for b in OPENITI_BOOKS if (out_dir / f"{b}.json").exists()}


# Künyenin numarası kitaba göre başka şeydir (Wensinck sistemi): Kütüb-i Sitte'nin sünenlerinde ve Buhârî'de bâb,
# Müslim ve Muvatta'da kitabın içindeki hadis sırası. Baskılar bâb ve tarik sayımında ayrıldığı için künye kesin yeri
# değil yakın bir bölgeyi gösterir. Pencereler 2026-11-03 ölçümünden (tekil künye, karıştırılmış künyeye karşı;
# `docs/hadis-kitaplari-plani.md`): küçük kümelerle ve aynı veride seçildi, yön gösterir.
BAB_WINDOW = {"nasai": 0, "ibnmajah": 0, "tirmidhi": 1, "bukhari": 3, "abudawud": 5}
ORDER_WINDOW = {"muslim": 10, "malik": 10}              # Muvatta ölçülemedi (bulunmuş parçası yok)


class Index:
    """Kitapların künyeyle aranması: künye (kitap, API bölümü, numaralar) -> künyenin bölgesindeki hadisler."""

    def __init__(self, books: dict[str, dict]) -> None:
        self.books = books
        self.kitabs: dict[tuple[str, int], set[str]] = {}
        self.by_api: dict[tuple[str, int], dict] = {}
        self.place: dict[str, tuple[str, int | None, int]] = {}     # hadis -> (kitap, bâb no, kitap içi sıra)
        self.in_kitab: dict[str, list[dict]] = {}
        for book, data in books.items():
            nodes = {n["id"]: n for n in data["outline"]}
            for n in data["outline"]:
                if n["level"] == "kitab":
                    for sec in n.get("api_sections", ()):
                        self.kitabs.setdefault((book, sec), set()).add(n["id"])
            for h in data["hadiths"]:
                node = nodes[h["node_id"]]
                kitab = node["parent_id"] or node["id"]
                self.in_kitab.setdefault(kitab, []).append(h)
                self.place[h["id"]] = (kitab, node["number"] if node["level"] == "bab" else None, len(self.in_kitab[kitab]))
                if "api" in h:
                    self.by_api[book, h["api"]] = h

    def cited(self, book: str, section: int | None, numbers: str | None) -> list[dict]:
        """Künyenin bölgesindeki hadisler ("Ezân: 148" -> Ezân'ı kapsayan kitapta 148±pencere numaralı bâblar)."""
        if section is None or not (wanted := numbers_of(numbers)):
            return []
        out = []
        for kitab in self.kitabs.get((book, section), ()):
            for h in self.in_kitab.get(kitab, ()):
                _, bab, order = self.place[h["id"]]
                if book in BAB_WINDOW and bab is not None and any(abs(bab - n) <= BAB_WINDOW[book] for n in wanted):
                    out.append(h)
                elif book in ORDER_WINDOW and any(abs(order - n) <= ORDER_WINDOW[book] for n in wanted):
                    out.append(h)
        return out


def citations(db: Path, supports: tuple[str, ...]) -> dict[tuple[str, str, str], set]:
    """Tekil (parça, kitap, künye) -> konumlar {(API bölümü, numaralar)}; bu yedi kitabı gösteren künyeler."""
    import sqlite3
    conn = sqlite3.connect(db)
    out: dict[tuple[str, str, str], set] = {}
    for key, book, raw, section, number in conn.execute(
            "SELECT a.hadith_key, c.book, c.raw, l.section, l.number FROM arabic a"
            " JOIN hadith_citations c ON (c.paragraph_id = a.paragraph_id AND c.ord = a.ord)"
            " OR (c.paragraph_id IS NULL AND c.hadith_key = a.hadith_key)"
            " JOIN hadith_locators l ON l.citation_id = c.id"
            f" WHERE a.hadith_support IN ({','.join('?' * len(supports))}) AND l.kind = 'chapter'"
            " AND l.section IS NOT NULL", supports):
        if book in OPENITI_BOOKS:
            out.setdefault((key, book, raw), set()).add((section, number))
    return out


def measure(db: Path, books: dict[str, dict] | None = None, seed: int = 3) -> dict[str, tuple[int, float, int]]:
    """Künye–bölge ölçümü: metni derlemde bulunmuş (`found`, `partly_found`) parçada, bulunan rivayet künyenin
    bölgesinde mi. Birim tekil (parça, künye); karşılaştırma: künyeler aynı kitabın künyeleri arasında karıştırılır.
    Kitap başına (isabet, karışık ortalama, künye)."""
    import random
    import sqlite3
    index = Index(books or load())
    conn = sqlite3.connect(db)
    matched: dict[str, set[str]] = {}
    for key, report in conn.execute("SELECT hadith_key, report_id FROM hadith_matches"):
        book, _, number = report.partition(":")
        if number.isdigit() and (h := index.by_api.get((book, int(number)))):
            matched.setdefault(key, set()).add(h["id"])
    items = [(book, locs, found) for (key, book, _), locs in citations(db, ("found", "partly_found")).items()
             if (found := {h for h in matched.get(key, ()) if h.startswith(book + "/")})]

    def hit(book: str, locs, found: set[str]) -> bool:
        return any(h["id"] in found for sec, num in locs for h in index.cited(book, sec, num))
    rng, out = random.Random(seed), {}
    for book in sorted({b for b, *_ in items}):
        group = [i for i in items if i[0] == book]
        shuffled = 0
        for _ in range(ROUNDS):
            locs = [g[1] for g in group]
            rng.shuffle(locs)
            shuffled += sum(hit(g[0], l, g[2]) for g, l in zip(group, locs))
        out[book] = (sum(hit(*g) for g in group), shuffled / ROUNDS, len(group))
    return out


def main() -> None:
    from risale_mcp.paths import DB_PATH
    report = build()
    text = render(report)
    if DB_PATH.exists():
        rows = measure(DB_PATH)
        text += ("\n## Künye–bölge ölçümü\n\nMetni derlemde bulunmuş parçalarda bulunan rivayet künyenin bölgesinde mi "
                 f"(tekil parça ve künye; karışık: {ROUNDS} tur ortalaması). Pencereler: bâb {BAB_WINDOW}, sıra {ORDER_WINDOW}.\n\n"
                 "| kitap | künye | bölgede | karışık |\n|---|---|---|---|\n")
        text += "".join(f"| {b} | {n} | {h} | {s:.1f} |\n" for b, (h, s, n) in rows.items())
    (INTERIM_DIR / "hadis" / "kutub.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
