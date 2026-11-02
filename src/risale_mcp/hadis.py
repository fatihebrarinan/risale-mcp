"""Hadis katmanı: Risale'deki hadislerin rivayetlerle eşlenmesi ve dayanağı.

    uv run python -m risale_mcp.fetch hadis     # data/raw/{sanadset,hadith_api,nurpedia}
    uv run python -m risale_mcp.hadis           # veritabanındaki parçalar -> data/library/hadis/matches.json
    uv run python -m risale_mcp.build_db        # eşlemeler veritabanına (her profil)

Hüküm verilmez: bir parçanın hadis olup olmadığına kimse karar vermez, kanıtı gösterilir (kullanıcı hadis âlimi
değildir, örneklemi elle denetlemek yerine kanıtlar üst üste konur). Kaynağın işareti değişmez (`arabic_kinds`).
Dayanak (`arabic.hadith_support`), en güçlüden:

    found         Arapçası bir rivayette kelime sınırlarıyla tam geçiyor ve rivayeti ayırt edecek kadar uzun
    partly_found  bir rivayet parçanın yarısından çoğunu ya da aynı harfleri kelime sınırı tutmadan taşıyor:
                  kısaltılmış, değiştirilmiş ya da mânen nakil olabilir
    located_chapter  kısa parça, bu geçişin künyesindeki kitabın anılan bölümünde kelime sınırıyla geçiyor
    cited         tam metni ayırt edilemedi, ama hadis kitabı künyesi var (kaynakça, risaleoku meali, nurpedia)
    phrase_found  sözler bir rivayette geçiyor, ama rivayeti ayırt etmeye kısa ve künyesi yok
    marked        yalnız kaynak hadis diye işaretlemiş
    unsupported   yalnız yanındaki söz ya da hiçbir şey

`MIN_MATCH` harften kısa parça derlemde aranmaz: kalıp sözler rastgele tutar. `MIN_IDENTIFY` kelimeden kısa eşleşme
rivayeti kanıtlamaz: müellifin hadis işaretsiz Arapçasından 4 ve daha az kelimelilerin %20'si derlemde tutuyor, 5 ve
üstü %0,6 (`hadis_eval`; harf sayısı ayırt etmiyor, iskelet kısadır). Künye kısa parçada anahtara yayılmaz: aynı kısa ifade başka yerde başka hadisin parçası olabilir.
Künyeli arama (`Corpus.locate`) geçiş başınadır ve yalnız kısa parçaya uygulanır. Karşı sınama (`hadis_eval`): künyeler
karıştırılınca kitap düzeyinde tutma gerçek künyeyle aynıdır (2–4 kelime, ayar kümesi: gerçek %31–35, karışık %27–36),
kitapta geçmek kanıt değildir ve saklanmaz. Bölüm düzeyinde gerçek %10–25, karışık %1–4: yalnız o kanıttır. "…" ve "الخ" ile atlanan parçanın her kesimi aynı rivayette aranır. "Bulunamadı" hadis olmadığı anlamına gelmez;
müellif hadisi çoğu yerde kendi ifadesiyle yazar (`docs/hadis-plani.md`). Sanadset'in kitapları arasında tefsir ve tabakât da var: eşleşme rivayettir, her zaman hadis kitabı değil.
Derece yalnız Hadith API'dendir, âlimin adıyla; Buhârî ve Müslim'de hadis başına derece yoktur, verilmez.

Tam derlem ham veride durur; `matches.json` yalnız eşleşenleri taşır (ileride `hadis` profili bütününü kuracak).
"""

import csv
import html
import json
import re
from bisect import bisect_right
from collections import Counter, defaultdict
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path

from risale_mcp.arabic_kinds import HADITH_BOOKS
from risale_mcp.db import connect
from risale_mcp.hadis_kitaplar import BY_ID
from risale_mcp.hadis_kunye import Citation, parse as parse_citation
from risale_mcp.paths import DB_PATH, HADIS_PATH, RAW_DIR, ROOT
from risale_mcp.quran import pieces, skeleton
from risale_mcp.sources.hadis import COLLECTIONS

MIN_MATCH = 10          # derlemde aranan en kısa iskelet (harf)
MIN_IDENTIFY = 5        # rivayeti ayırt eden en az kelime
MIN_LOCATE = 2          # künyeli aramada en az kelime
MIN_WINDOW = 12         # kısmi eşlemede pencere
PARTIAL = 0.5           # kısmi eşleme için aynı rivayette geçmesi gereken pencere oranı
MAX_REPORTS = 8         # bir parça için saklanan en çok rivayet
MAX_HITS = 3000         # bir dizinin izlendiği en çok geçiş (kalıp sözler)

TITLES = {"bukhari": "Sahîh-i Buhârî", "muslim": "Sahîh-i Müslim", "abudawud": "Sünen-i Ebû Dâvûd",
          "tirmidhi": "Sünen-i Tirmizî", "nasai": "Sünen-i Nesâî", "ibnmajah": "Sünen-i İbn Mâce",
          "malik": "Muvatta", "nawawi": "Nevevî'nin Kırk Hadisi", "qudsi": "Kudsî Hadisler",
          "dehlawi": "Dihlevî'nin Kırk Hadisi"}
# Hadith API'de bulunanlar Sanadset'ten alınmaz: aynı rivayet iki kez çıkmasın, dereceli olan kalsın.
IN_HADITH_API = {"صحيح البخاري", "صحيح مسلم", "سنن أبي داود", "جامع الترمذي", "سنن النسائى الصغرى",
                 "سنن ابن ماجه", "موطأ مالك رواية يحيى الليثي"}
# Önce gelen büyük hadis kitapları; adı zayıf ya da mevzu rivayet derlediğini söyleyenler en sonda (`CAUTION_BOOKS`).
MAIN_BOOKS = ("مسند أحمد بن حنبل", "صحيح ابن حبان", "المستدرك على الصحيحين", "صحيح ابن خزيمة", "السنن الكبرى للبيهقي",
              "السنن الكبرى للنسائي", "المعجم الكبير للطبراني", "المعجم الأوسط للطبراني", "مصنف ابن أبي شيبة",
              "مصنف عبد الرزاق", "شعب الإيمان للبيهقي", "مسند أبي يعلى الموصلي")
CAUTION_BOOKS = re.compile(r"موضوع|الضعفاء|الضعيف|المجروحين|الأباطيل|تنزيه الشريعة|اللآلئ")
_ETC = skeleton("الخ")
ATTRIBUTION = {"hadith_api": "Hadith API (github.com/fawazahmed0/hadith-api), Unlicense",
               "sanadset": "Sanadset 650K (Mghari, Bouras, El Hibaoui, Data in Brief 2022), CC BY 4.0"}


@dataclass(frozen=True)
class Report:
    id: str
    title: str
    number: str
    text: str
    source: str
    grades: tuple[tuple[str, str], ...] = ()
    section: int | None = None      # Hadith API bölümü


def read_reports(raw: Path = RAW_DIR) -> Iterator[Report]:
    """Önce dereceli derlemler; eşleşmeler bu sırayla seçilir."""
    for name in COLLECTIONS:
        for h in json.loads((raw / "hadith_api" / f"ara-{name}.json").read_text(encoding="utf-8"))["hadiths"]:
            if (text := (h.get("text") or "").strip()):
                yield Report(f"{name}:{h['hadithnumber']}", TITLES[name], str(h["hadithnumber"]), text, "hadith_api",
                             tuple((g["name"], g["grade"]) for g in h.get("grades") or ()),
                             (h.get("reference") or {}).get("book"))
    csv.field_size_limit(10 ** 9)
    with open(raw / "sanadset" / "sanadset.csv", encoding="utf-8", errors="replace", newline="") as f:
        for i, row in enumerate(csv.DictReader(f)):
            if row["Book"] not in IN_HADITH_API and (text := (row["Matn"] or "").strip()):
                yield Report(f"sanadset:{i}", row["Book"], row["Num_hadith"], text, "sanadset")


def rank(report: Report) -> int:
    if report.source == "hadith_api":
        return 0
    if CAUTION_BOOKS.search(report.title):
        return 3
    return 1 if report.title in MAIN_BOOKS else 2


class Corpus:
    """Rivayetlerin iskeletleri tek metinde; aranan dizinin geçtiği rivayetler konumdan bulunur."""

    def __init__(self, reports: list[Report]) -> None:
        reports = sorted(reports, key=rank)         # sıralama kararlıdır: seçim bu sırayla yapılır
        self.reports = reports
        keys = [skeleton(r.text) for r in reports]
        self.text = "\n".join(keys)
        self.spaced_text: dict[int, str] = {}
        self.books: dict[str, list[int]] = defaultdict(list)
        for i, r in enumerate(reports):
            self.books[r.title].append(i)
        self.starts, at = [], 0
        for key in keys:
            self.starts.append(at)
            at += len(key) + 1

    def containing(self, key: str) -> set[int]:
        found, at = set(), self.text.find(key)
        for _ in range(MAX_HITS):
            if at < 0:
                break
            found.add(bisect_right(self.starts, at) - 1)
            at = self.text.find(key, at + 1)
        return found

    def locate(self, text: str, citations: list[Citation]) -> tuple[str | None, list[int]]:
        """Parçayı yalnız künyedeki kitaplarda arar: (chapter | book | boş, o düzeyin rivayetleri)."""
        needle = f" {' '.join(words(text))} "
        chapter, book = [], []
        for c in citations:
            known = BY_ID.get(c.book)
            for title in ([TITLES[known.api]] if known.api else known.sanadset) if known else ():
                sections = {l.section for l in c.locators if l.section is not None}
                for r in self.books[title]:
                    if needle in self._spaced(r):
                        (chapter if self.reports[r].section in sections else book).append(r)
        if chapter:
            return "chapter", self.select(dict.fromkeys(chapter))
        return ("book", self.select(dict.fromkeys(book))) if book else (None, [])

    def _spaced(self, report: int) -> str:
        if report not in self.spaced_text:
            self.spaced_text[report] = f" {' '.join(words(self.reports[report].text))} "
        return self.spaced_text[report]

    def match(self, text: str, prefer: Iterable[str] = (), limit: int | None = MAX_REPORTS) -> tuple[str, list[int], int]:
        """(found | partly_found | phrase_found | none | short, seçilen rivayetler, bulunan rivayet sayısı)."""
        key = skeleton(text)
        if len(key) < MIN_MATCH:
            return "short", [], 0
        cuts = [p for p in pieces(text) if len(p) >= MIN_MATCH] or [key]    # kesimlerin hepsi kısaysa bütünü aranır
        hits = set.intersection(*(self.containing(c) for c in cuts))
        if hits:
            exact = {r for r in hits if self._has_words(text, r)} if cuts == [key] else hits
            if not exact:
                return "partly_found", self.select(hits, prefer, limit), len(hits)
            return ("found" if identifies(text) else "phrase_found"), self.select(exact, prefer, limit), len(exact)
        windows = [c[i:i + size] for c in cuts for size in [min(len(c), max(MIN_WINDOW, len(c) // 3))]
                   for i in range(0, len(c) - size + 1, max(1, size // 2))]
        counts = Counter(r for w in windows for r in self.containing(w))
        best = [r for r, n in counts.items() if n >= max(2, len(windows) * PARTIAL)]
        best.sort(key=lambda r: (-counts[r], r))
        return ("partly_found", self.select(best, prefer, limit), len(best)) if best else ("none", [], 0)

    def _has_words(self, text: str, report: int) -> bool:
        return f" {' '.join(words(text))} " in self._spaced(report)

    def select(self, found: Iterable[int], prefer: Iterable[str] = (), limit: int | None = MAX_REPORTS) -> list[int]:
        """Saklanacak rivayetler: künyedeki kitaplar, sonra her kitaptan biri, sonra sırayla. Küme sıraya dizilir."""
        ordered = sorted(found) if isinstance(found, (set, frozenset)) else list(found)
        wanted, seen, cited, first, rest = set(prefer), set(), [], [], []
        for r in ordered:
            title = self.reports[r].title
            (rest if title in seen else cited if title in wanted else first).append(r)
            seen.add(title)
        return (cited + first + rest)[:limit]


def words(text: str) -> list[str]:
    """Kelimelerin iskeleti; iskeleti boş kalan kelime ("يا", "و") atılır."""
    return [w for w in map(skeleton, text.split()) if w]


def identifies(text: str) -> bool:
    return len([w for w in words(text) if w != _ETC]) >= MIN_IDENTIFY


def nurpedia_citations(root: Path) -> dict[str, set[str]]:
    """nurpedia meal sayfalarında hadis kitabı künyesi taşıyan Arapça satırlar: iskelet -> künyeler."""
    found: dict[str, set[str]] = {}
    for path in root.glob("*.html"):
        page = path.read_text(encoding="utf-8")
        text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", page[page.find("mw-parser-output"):])))
        for m in re.finditer(r"[؀-ۿ][؀-ۿ\s،؛:]{6,}", text):
            after = text[m.end():m.end() + 420]
            if (next_arabic := re.search(r"[؀-ۿ]{3}", after)):
                after = after[:next_arabic.start()]
            refs = {ref.strip() for ref in re.findall(r"\(([^()]{4,240})\)", after) if HADITH_BOOKS.search(ref)}
            if refs:
                found.setdefault(skeleton(m.group()), set()).update(refs)
    return {k: v for k, v in found.items() if len(k) >= 6}


def _refs_for(key: str, citations: dict[str, set[str]]) -> list[str]:
    refs = set(citations.get(key, ()))
    if len(key) >= MIN_MATCH:
        refs.update(r for c, v in citations.items() if len(c) >= MIN_MATCH and (key in c or c in key) for r in v)
    return sorted(refs)


def row_cited(source: str | None, meal: str | None) -> bool:
    return bool(HADITH_BOOKS.search(f"{source or ''} {meal or ''}"))


def book_titles(citations: Iterable[Citation]) -> set[str]:
    """Künyelerin derlemdeki kitap adları."""
    known = (BY_ID[c.book] for c in citations if c.book)
    return {t for b in known for t in ([TITLES[b.api]] if b.api else b.sanadset)}


def build(db: Path = DB_PATH, raw: Path = RAW_DIR, out: Path = HADIS_PATH) -> Counter:
    """Veritabanındaki hadis parçalarını rivayetlerle eşler; anahtar parçanın harf iskeletidir."""
    conn = connect(db)
    parts: dict[str, list] = {}
    sources: dict[str, set[str]] = defaultdict(set)
    for row in conn.execute("SELECT a.source, a.meal, substr(p.text, a.span_start + 1, a.span_end - a.span_start) AS text"
                            " FROM arabic a JOIN paragraphs p ON p.id = a.paragraph_id"
                            " WHERE a.kind = 'hadis' AND p.text IS NOT NULL"):
        part = parts.setdefault(skeleton(row["text"]), [row["text"], False])
        part[1] = part[1] or row_cited(row["source"], row["meal"])
        if row["source"] and row["source"] != "REF-TODO":
            sources[skeleton(row["text"])].add(row["source"])
    corpus = Corpus(list(read_reports(raw)))
    reports = corpus.reports
    citations = nurpedia_citations(raw / "nurpedia")
    entries, used, counts = {}, {}, Counter()
    for key, (text, cited) in parts.items():
        parsed = {raw: parse_citation(raw).citations for raw in sources[key]}
        match, found, total = corpus.match(text, book_titles(c for cs in parsed.values() for c in cs))
        refs = _refs_for(key, citations)
        entries[key] = {"match": match, "cited": cited or bool(refs), "total": total, "identifies": identifies(text),
                        "nurpedia": refs, "located": (located := _located(corpus, text, match, parsed)),
                        "reports": [reports[i].id for i in found]}
        counts[match] += 1
        used.update((reports[i].id, reports[i]) for i in found)
        used.update((reports[i].id, reports[i]) for place in located.values() for i in place.pop("found"))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"parts": entries, "reports": {
        r.id: {"title": r.title, "number": r.number, "text": r.text, "source": r.source, "grades": r.grades}
        for r in used.values()}}, ensure_ascii=False), encoding="utf-8")
    counts["reports"] = len(used)
    return counts


SUPPORT_ORDER = ("found", "partly_found", "located_chapter", "cited", "phrase_found", "marked", "unsupported")


def support(entry: dict | None, kind_source: str, cited: bool | None = None, source: str | None = None) -> str | None:
    """Parçanın bu geçişteki dayanağı (`arabic.hadith_support`); eşlemesi yoksa boş. `cited` verilmezse parçanınkidir,
    `source` geçişin künye metnidir."""
    if entry is None:
        return None
    if place := entry.get("located", {}).get(source):
        return f"located_{place['level']}"
    cited = entry["cited"] if cited is None else cited
    if entry["match"] in ("found", "partly_found"):
        return entry["match"]
    if cited:
        return "cited"
    if entry["match"] == "phrase_found":
        return "phrase_found"
    return "marked" if kind_source in ("kaynak", "erisale") else "unsupported"


def _located(corpus: Corpus, text: str, match: str, parsed: dict[str, list[Citation]]) -> dict[str, dict]:
    """Kısa parçanın künyeli araması, künye metni başına: geçişler aynı künyeyi taşıyorsa aynı sonucu alır."""
    if match not in ("short", "phrase_found") or len(words(text)) < MIN_LOCATE:
        return {}
    places = {}
    for raw, citations in parsed.items():
        level, found = corpus.locate(text, citations)
        if level == "chapter":
            places[raw] = {"level": level, "found": found, "reports": [corpus.reports[i].id for i in found]}
    return places


def main() -> None:
    counts = build()
    print(dict(counts))
    print(f"yazıldı: {HADIS_PATH.relative_to(ROOT)}; şimdi `uv run python -m risale_mcp.build_db`")


if __name__ == "__main__":
    main()
