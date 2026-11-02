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
    cited         tam metni ayırt edilemedi, ama hadis kitabı künyesi var (kaynakça, risaleoku meali, nurpedia)
    phrase_found  sözler bir rivayette geçiyor, ama rivayeti ayırt etmeye kısa ve künyesi yok
    marked        yalnız kaynak hadis diye işaretlemiş
    unsupported   yalnız yanındaki söz ya da hiçbir şey

`MIN_MATCH` harften kısa parça derlemde aranmaz: kalıp sözler rastgele tutar. `MIN_IDENTIFY` kelimeden kısa eşleşme
rivayeti kanıtlamaz: müellifin hadis işaretsiz Arapçasından 4 ve daha az kelimelilerin %20'si derlemde tutuyor, 5 ve
üstü %0,6 (`hadis_eval`; harf sayısı ayırt etmiyor, iskelet kısadır). Künye kısa parçada anahtara yayılmaz: aynı kısa ifade başka yerde başka hadisin parçası olabilir.
"…" ve "الخ" ile atlanan parçanın her kesimi aynı rivayette aranır. "Bulunamadı" hadis olmadığı anlamına gelmez;
müellif hadisi çoğu yerde kendi ifadesiyle yazar (`docs/hadis-plani.md`). Sanadset'in kitapları arasında tefsir ve tabakât da var: eşleşme rivayettir, her zaman hadis kitabı değil.
Derece yalnız Hadith API'dendir, âlimin adıyla; Buhârî ve Müslim'de hadis başına derece yoktur, verilmez.

Tam derlem ham veride durur; `matches.json` yalnız eşleşenleri taşır (ileride `hadis` profili bütününü kuracak).
"""

import csv
import html
import json
import re
from bisect import bisect_right
from collections import Counter
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path

from risale_mcp.arabic_kinds import HADITH_BOOKS
from risale_mcp.db import connect
from risale_mcp.paths import DB_PATH, HADIS_PATH, RAW_DIR, ROOT
from risale_mcp.quran import pieces, skeleton
from risale_mcp.sources.hadis import COLLECTIONS

MIN_MATCH = 10          # derlemde aranan en kısa iskelet (harf)
MIN_IDENTIFY = 5        # rivayeti ayırt eden en az kelime
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


def read_reports(raw: Path = RAW_DIR) -> Iterator[Report]:
    """Önce dereceli derlemler; eşleşmeler bu sırayla seçilir."""
    for name in COLLECTIONS:
        for h in json.loads((raw / "hadith_api" / f"ara-{name}.json").read_text(encoding="utf-8"))["hadiths"]:
            if (text := (h.get("text") or "").strip()):
                yield Report(f"{name}:{h['hadithnumber']}", TITLES[name], str(h["hadithnumber"]), text, "hadith_api",
                             tuple((g["name"], g["grade"]) for g in h.get("grades") or ()))
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

    def match(self, text: str) -> tuple[str, list[int], int]:
        """(found | partly_found | phrase_found | none | short, seçilen rivayetler, bulunan rivayet sayısı)."""
        key = skeleton(text)
        if len(key) < MIN_MATCH:
            return "short", [], 0
        cuts = [p for p in pieces(text) if len(p) >= MIN_MATCH] or [key]    # kesimlerin hepsi kısaysa bütünü aranır
        hits = set.intersection(*(self.containing(c) for c in cuts))
        if hits:
            exact = {r for r in hits if self._has_words(text, r)} if cuts == [key] else hits
            if not exact:
                return "partly_found", self.select(hits), len(hits)
            return ("found" if identifies(text) else "phrase_found"), self.select(exact), len(exact)
        windows = [c[i:i + size] for c in cuts for size in [min(len(c), max(MIN_WINDOW, len(c) // 3))]
                   for i in range(0, len(c) - size + 1, max(1, size // 2))]
        counts = Counter(r for w in windows for r in self.containing(w))
        best = [r for r, n in counts.items() if n >= max(2, len(windows) * PARTIAL)]
        best.sort(key=lambda r: (-counts[r], r))
        return ("partly_found", self.select(best), len(best)) if best else ("none", [], 0)

    def _has_words(self, text: str, report: int) -> bool:
        return f" {' '.join(words(text))} " in f" {' '.join(words(self.reports[report].text))} "

    def select(self, found: Iterable[int]) -> list[int]:
        """Saklanacak rivayetler: önce her kitaptan biri, sonra sırayla; `found` sıralı değilse sıraya dizilir."""
        ordered = found if isinstance(found, list) else sorted(found)
        seen, first, rest = set(), [], []
        for r in ordered:
            title = self.reports[r].title
            (rest if title in seen else first).append(r)
            seen.add(title)
        return (first + rest)[:MAX_REPORTS]


def words(text: str) -> list[str]:
    """Kelimelerin iskeleti; iskeleti boş kalan kelime ("يا", "و") atılır."""
    return [w for w in map(skeleton, text.split()) if w]


def identifies(text: str) -> bool:
    return len([w for w in words(text) if w != _ETC]) >= MIN_IDENTIFY


def nurpedia_citations(root: Path) -> set[str]:
    """nurpedia meal sayfalarında hadis kitabı künyesi taşıyan Arapça satırlar (iskelet). Künye saklanmaz: izin
    kapsamı netleşene kadar yalnız "künyesi var" bilgisi kullanılır."""
    keys = set()
    for path in root.glob("*.html"):
        page = path.read_text(encoding="utf-8")
        text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", page[page.find("mw-parser-output"):])))
        for m in re.finditer(r"[؀-ۿ][؀-ۿ\s،؛:]{6,}", text):
            after = text[m.end():m.end() + 420]
            if (next_arabic := re.search(r"[؀-ۿ]{3}", after)):
                after = after[:next_arabic.start()]
            if any(HADITH_BOOKS.search(ref) for ref in re.findall(r"\(([^()]{4,240})\)", after)):
                keys.add(skeleton(m.group()))
    return {k for k in keys if len(k) >= 6}


def _cited_in(key: str, citations: set[str]) -> bool:
    return key in citations or (len(key) >= MIN_MATCH and any(len(c) >= MIN_MATCH and (key in c or c in key) for c in citations))


def row_cited(source: str | None, meal: str | None) -> bool:
    return bool(HADITH_BOOKS.search(f"{source or ''} {meal or ''}"))


def build(db: Path = DB_PATH, raw: Path = RAW_DIR, out: Path = HADIS_PATH) -> Counter:
    """Veritabanındaki hadis parçalarını rivayetlerle eşler; anahtar parçanın harf iskeletidir."""
    conn = connect(db)
    parts: dict[str, list] = {}
    for row in conn.execute("SELECT a.source, a.meal, substr(p.text, a.span_start + 1, a.span_end - a.span_start) AS text"
                            " FROM arabic a JOIN paragraphs p ON p.id = a.paragraph_id"
                            " WHERE a.kind = 'hadis' AND p.text IS NOT NULL"):
        part = parts.setdefault(skeleton(row["text"]), [row["text"], False])
        part[1] = part[1] or row_cited(row["source"], row["meal"])
    corpus = Corpus(list(read_reports(raw)))
    reports = corpus.reports
    citations = nurpedia_citations(raw / "nurpedia")
    entries, used, counts = {}, {}, Counter()
    for key, (text, cited) in parts.items():
        match, found, total = corpus.match(text)
        entries[key] = {"match": match, "cited": cited or _cited_in(key, citations), "total": total,
                        "identifies": identifies(text),
                        "reports": [reports[i].id for i in found]}
        counts[match] += 1
        used.update((reports[i].id, reports[i]) for i in found)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"parts": entries, "reports": {
        r.id: {"title": r.title, "number": r.number, "text": r.text, "source": r.source, "grades": r.grades}
        for r in used.values()}}, ensure_ascii=False), encoding="utf-8")
    counts["reports"] = len(used)
    return counts


SUPPORT_ORDER = ("found", "partly_found", "cited", "phrase_found", "marked", "unsupported")


def support(entry: dict | None, kind_source: str, cited: bool | None = None) -> str | None:
    """Parçanın bu geçişteki dayanağı (`arabic.hadith_support`); eşlemesi yoksa boş. `cited` verilmezse parçanınkidir."""
    if entry is None:
        return None
    cited = entry["cited"] if cited is None else cited
    if entry["match"] in ("found", "partly_found"):
        return entry["match"]
    if cited:
        return "cited"
    if entry["match"] == "phrase_found":
        return "phrase_found"
    return "marked" if kind_source in ("kaynak", "erisale") else "unsupported"


def main() -> None:
    counts = build()
    print(dict(counts))
    print(f"yazıldı: {HADIS_PATH.relative_to(ROOT)}; şimdi `uv run python -m risale_mcp.build_db`")


if __name__ == "__main__":
    main()
