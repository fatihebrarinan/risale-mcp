"""Arapça parçaların türü: âyet, hadis ya da düz Arapça, ve bu türün neye dayandığı.

risaleoku kaynağı âyet ve hadisi ayırmaz, erisale de bazı alıntıları `arabi` bırakır. `build_db` her parçayı
buradan geçirir; JSON'lar değişmez. Karar sırası (`kind_source` sütununda durur):

    kaynak   kaynağın kendi işareti (erisale, Hayrat); değiştirilmez, yalnız denetlenir
    kuran    metin Kur'ân'da bulundu: en az `MIN_QURAN` harflik iskelet, Kur'ân'da tek yerde geçen `MIN_UNIQUE`
             harflik alıntı ya da bağlamı "âyet" diyen kısa alıntı. "٭" ile sıralanmış parçaların her biri bulunmalı.
    kaynakca kaynak parçayı Arapça bırakmış, ama kaynakçası hadis kitabı gösteriyor
    meal     aynı Arapçanın risaleoku meal kaydı âyet numarası ya da hadis kaynağı veriyor
    erisale  aynı Arapçayı erisale hadis diye işaretlemiş
    baglam   yalnız yanındaki söz ("hadîs-i şerîf", "ferman etmiş", "âyeti") söylüyor; hadiste kesin değil, adaydır:
             derlemle doğrulaması Aşama 14'ündür

Kalıp sözler (`FORMULAS`: Besmele, hamdele, "Mâşâallâh"…) Kur'ân'da geçse de âyet sayılmaz; yanında "âyet" denirse
sayılır. Bir parçanın yalnız bir kısmı âyetse parça `arabi` kalır, âyet `ayah_quotes`'tadır.
"""

import gzip
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from functools import cache
from pathlib import Path

from risale_mcp.normalize import fold
from risale_mcp.quran import Match, Quran, pieces, skeleton, sura_ref
from risale_mcp.sources import risaleoku_app as app_source

MIN_QURAN = 12            # kendi başına âyet sayılan en kısa iskelet (harf)
MIN_UNIQUE = 8            # Kur'ân'da tek yerde geçiyorsa yeten iskelet
MIN_CONTEXT = 4           # bağlamı "âyet" diyorsa yeten iskelet
MIN_EVIDENCE = 8          # meal ya da erisale kaydının kanıt sayıldığı en kısa iskelet
# Kaynağın âyet numarası metne oturmuyor, metin başka âyete tam oturuyor (bkz. `docs/ayet-duzeltmeleri.md`):
# (paragraf, parça sırası) -> (sûre, ilk, son). Metin değişmez, yalnız adres. Aralıklarda kaynak birkaç âyet sayar.
AYAH_FIXES = {
    ("sozler/33/pencere-19/p008", 0): (59, 1, 1),
    ("sozler/fihrist/soz-33/pencere-19/p002", 0): (59, 1, 1),
    ("sualar/1/sual-02/ayet-05/sabrinin-sadakatinin-bir-kerametidir/p002", 3): (61, 8, 8),
    ("isaratul-icaz/sure-i-bakara/26-27-ayetlerin-tefsiri/p009", 0): (2, 17, 17),
    ("mektubat/26/mebhas-03/mesele-04/p003", 0): (5, 54, 54),
    ("el-mesnevi-el-arabi-harekeli/habbe/zeylul-habbe/p012", 0): (39, 67, 67),
    ("el-mesnevi-el-arabi-harekeli/hubab/meclis-i-mebusana-hitaben-yazdigim-bir/p042", 1): (31, 28, 28),
    ("el-mesnevi-el-arabi-harekeli/sule/p116", 0): (72, 28, 28),
    ("el-mesnevi-el-arabi-harekeli/hubab/p080", 0): (17, 88, 88),
    ("isaratul-icaz/sure-i-bakara/17-20-ayetlerin-tefsiri/p068", 0): (2, 19, 20),
    ("isaratul-icaz/sure-i-bakara/31-33-ayetlerin-tefsiri/p001", 0): (2, 31, 33),
    ("sualar/7/ayetul-kubra/bab-02/menzil-03/hakikat-01/p001", 1): (3, 5, 6),
    ("sualar/15/makam-01/kisim-02/p003", 0): (1, 1, 2),
}
# Dizgi hatası olabilecek âyetler (kullanıcının kararı: potansiyel hatalı işaretlenir, metin değişmez).
AYAH_SUSPECTS = {
    ("muhakemat/makale-01/mukaddeme-08/p015", 0),
    ("lemalar/28/nukte-26/p003", 0),
    ("sozler/fihrist/soz-33/pencere-20/p002", 2),
}
_FORMULA_TEXTS = (
    "بسم الله الرحمن الرحيم", "الحمد لله", "الحمد لله رب العالمين", "سبحان الله", "لا اله الا الله", "الله اكبر",
    "ان شاء الله", "ما شاء الله", "لا قوة الا بالله", "والله اعلم", "حسبنا الله", "حسبي الله", "استغفر الله",
    "رب العالمين", "الرحمن الرحيم", "صدق الله العظيم", "اعوذ بالله من الشيطان الرجيم", "لا اله الا هو", "الله", "لله", "والله", "يا الله", "يا رب",
    "ان الله", "سبحانه", "سبحانه وتعالى", "الباقي هو الباقي", "لا اله الا انت", "سبحانك", "ربنا", "بالله", "اللهم",
)
FORMULAS = {skeleton(t) for t in _FORMULA_TEXTS}
_REF = re.compile(r"S[ûu]resi,?\s*(\d+)\s*[:/]\s*(\d+)")
_SEPARATE = re.compile(r"[٭﴿﴾]")
_HADITH_BOOKS = re.compile(
    r"Buh[âa]r[iî]|Müslim|Tirmiz[iî]|Eb[ûu] ?D[âa]v[ûu]d|Nes[âa][iî]|[İI]bn[-‑ i]+M[âa]ce|Müsned|Musned|Taber[âa]n[iî]|"
    r"Müstedrek|Beyhak[iî]|Acl[ûu]n[iî]|Keşfü|Münâv[iî]+|Feyzü|Kenzü|Deylem[iî]|Suy[ûu]t[iî]|Muvatta|D[âa]rim[iî]|"
    r"Bezz[âa]r|Heysem[iî]|Mecmau|Mecmaü|İbn[-‑ ]Hibb[âa]n|\(Hadis|Hadis\.|hadis no|İhy[âa]")
_GAP = r"[\s,.;:()\"“”’'«»…\-‑]*(?:\S+\s+){0,3}?"
_TR_AYAH_AFTER = re.compile(_GAP + r"(?:ayet|sure)", re.I)
_TR_AYAH_BEFORE = re.compile(r"(?:ayet|sure-i|kuran(?:da|ın)?\b|furkan|ferman-ı ilahi)[^.!?]{0,50}$", re.I)
_TR_HADITH_AFTER = re.compile(_GAP + r"(?:hadis(?!e)|ferman-ı nebevi|ferman-ı peygamber)", re.I)
_TR_HADITH_BEFORE = re.compile(
    r"(?:hadis(?!e)|ferman-ı nebevi|(?:peygamber|resul|aleyhissalatu|nebi|\(asm\)|\(a\.s\.m\.\)|muhbir-i sadik)"
    r"[^.!?]{0,60}(?:ferman|buyur|demis|dedi|ihbar|tebsir|emretmis)[^.!?]{0,14})[^.!?]{0,20}$", re.I)
_AR_AYAH = re.compile(r"قوله تعالى|قال تعالى|قال الله|الآية|آية|سورة|﴿")
_AR_HADITH = re.compile(r"حديث|عليه السلام|عليه الصلاة|صلى الله عليه|ﷺ|\(ص\)|قال النبي|قال رسول")
_OS_AYAH = re.compile(r"آيت|آية|سوره")
_OS_HADITH = re.compile(r"حديث|فرمان نبوى")


@dataclass
class Decision:
    kind: str
    source: str | None
    kind_source: str


@dataclass
class Report:
    decided: Counter = field(default_factory=Counter)           # (eski tür, yeni tür, dayanak) -> sayı
    by_work: Counter = field(default_factory=Counter)           # (eser, tür, dayanak) -> sayı
    conflicts: list[tuple[str, str, str, str]] = field(default_factory=list)    # (paragraf, tür, sorun, metin)
    samples: dict = field(default_factory=lambda: defaultdict(list))


@cache
def read_meal_evidence(root: Path) -> dict[str, tuple[str, str]]:
    """risaleoku'nun Arapça satırı -> (ayet|hadis, kaynak): iskelet anahtarıyla, bütün indirilmiş kitaplardan."""
    meals = app_source.load_meals(root)
    seen: dict[str, Counter] = defaultdict(Counter)
    for path in root.glob("*/text.txt.gz"):
        with gzip.open(path, "rt", encoding="utf-8") as f:
            for line in f:
                if (m := re.match(r"^~(.*)\|(\d+)@", line.rstrip())) and m[2] in meals and (key := skeleton(m[1])):
                    seen[key][meals[m[2]]] += 1
    out = {}
    for key, texts in seen.items():
        for text, _ in texts.most_common():
            if ref := _REF.search(text):
                if 1 <= int(ref[1]) <= 114:
                    out[key] = ("ayet", sura_ref(int(ref[1]), int(ref[2])))
                break
            if _HADITH_BOOKS.search(text):
                out[key] = ("hadis", _citation(text))
                break
    return out


def _citation(meal: str) -> str:
    """Meal kaydının kaynak kısmı: tırnak kapandıktan sonrası, yoksa kaydın tamamı."""
    tail = re.split(r"[\"”]\s*", meal)[-1].strip()
    return tail if _HADITH_BOOKS.search(tail) else meal


class Classifier:
    def __init__(self, quran: Quran, meal: dict[str, tuple[str, str]], books: dict[str, dict]) -> None:
        self.quran, self.meal, self.report = quran, meal, Report()
        self.marked: dict[str, tuple[str, str | None]] = {}
        for book in books.values():
            for p in book["paragraphs"]:
                for part in p.get("arabic") or []:
                    if part["kind"] == "hadis" and p.get("text"):
                        self.marked.setdefault(skeleton(p["text"][part["start"]:part["end"]]), ("hadis", part.get("source")))

    def _in_quran(self, text: str) -> tuple[int, set[Match]]:
        parts = pieces(text)
        if not parts:
            return 0, set()
        longest = max(parts, key=len)
        if len(longest) < 3:
            return len(longest), set()
        return len(longest), {h for h in self.quran.find(longest) if self.quran.contains(parts, h.sura, h.start, h.end)}

    def decide(self, part: dict, text: str, before: str, after: str, language: str) -> Decision:
        kind, source = part["kind"], part.get("source")
        if kind in ("ayet", "hadis", "farsi", "kurdi", "osmani"):
            return Decision(kind, source, "kaynak")
        key = skeleton(text)
        if key in FORMULAS or len(key) < 2:
            return Decision(kind, source, "kaynak")
        ayah_ctx, hadith_ctx = _context(before, after, language)
        size, hits = self._in_quran(text)
        evidence = self.meal.get(key) if len(key) >= MIN_EVIDENCE else None
        if evidence and evidence[0] == "hadis" and size < MIN_QURAN:     # kısa alıntıda hadis kaydı Kur'ân'daki benzerinden önce
            return Decision("hadis", evidence[1], "meal")
        if hits and (size >= MIN_QURAN or (len(hits) == 1 and size >= MIN_UNIQUE) or (ayah_ctx and size >= MIN_CONTEXT)):
            return Decision("ayet", _ref(hits), "kuran")
        if self._all_in_quran(text):
            return Decision("ayet", None, "kuran")
        if source and source != "REF-TODO" and _HADITH_BOOKS.search(source):
            return Decision("hadis", source, "kaynakca")
        if evidence:
            if evidence[0] == "hadis":
                return Decision("hadis", evidence[1], "meal")
            if self.quran.contains(pieces(text), *_numbers(evidence[1])):
                return Decision("ayet", evidence[1], "meal")
        if key in self.marked and len(key) >= MIN_EVIDENCE:
            return Decision("hadis", self.marked[key][1], "erisale")
        if hadith_ctx and len(key) >= MIN_EVIDENCE and not ayah_ctx:
            return Decision("hadis", source if source != "REF-TODO" else None, "baglam")
        return Decision(kind, source, "kaynak")

    def _all_in_quran(self, text: str) -> bool:
        """"٭" ile ayrılmış birkaç âyet parçası: her biri Kur'ân'da olmalı."""
        chunks = [c for c in (skeleton(x) for x in _SEPARATE.split(text)) if c]
        return len(chunks) >= 2 and all(len(c) >= MIN_CONTEXT and self.quran.find(c) for c in chunks) \
            and sum(map(len, chunks)) >= MIN_QURAN

    def note(self, work: str, paragraph: str, part: dict, text: str, before: str, after: str, decision: Decision) -> None:
        if decision.kind != part["kind"]:
            self.report.decided[(part["kind"], decision.kind, decision.kind_source)] += 1
            self.report.by_work[(work, decision.kind, decision.kind_source)] += 1
            self.report.samples[f"{decision.kind}-{decision.kind_source}"].append(
                (paragraph, before[-50:], text[:200], after[:50], decision.source))
        else:
            self.report.decided[(part["kind"], part["kind"], decision.kind_source)] += 1
        self.review(paragraph, part, text)

    def review(self, paragraph: str, part: dict, text: str) -> None:
        """Kaynağın kendi işaretini denetler; değiştirmez, rapora yazar."""
        if part["kind"] == "hadis":
            size, hits = self._in_quran(text)
            if hits and size >= MIN_QURAN:
                self.report.conflicts.append((paragraph, "hadis", "metin Kur'ân'da geçiyor: " + _ref(hits, many=True), text))


def _numbers(ref: str) -> tuple[int, int, int]:
    sura, ayah = ref.rsplit(" ", 1)[1].split(":")
    return int(sura), int(ayah), int(ayah)


def _ref(hits: set[Match], many: bool = False) -> str | None:
    """Tek yerde geçen alıntının adresi; birden çok yerdeyse numara verilmez (uydurulmaz)."""
    if len(hits) == 1 or many:
        first = min(hits, key=lambda h: (h.sura, h.start))
        return sura_ref(first.sura, first.start, first.end)
    return None


def _context(before: str, after: str, language: str) -> tuple[bool, bool]:
    if language == "tr":
        b, a = fold(before).replace("‑", "-"), fold(after).replace("‑", "-")
        return (bool(_TR_AYAH_AFTER.match(a) or _TR_AYAH_BEFORE.search(b)),
                bool(_TR_HADITH_AFTER.match(a) or _TR_HADITH_BEFORE.search(b)))
    ayah, hadith = (_AR_AYAH, _AR_HADITH) if language == "ar" else (_OS_AYAH, _OS_HADITH)
    near = before[-40:] + " " + after[:30]
    return bool(ayah.search(near)), bool(hadith.search(near))


def write_report(report: Report, folder: Path, sample: int = 40) -> None:
    """Sayımlar, kaynağın işaretiyle çatışanlar ve gözden geçirme örneklemleri."""
    import random
    folder.mkdir(parents=True, exist_ok=True)
    lines = ["# Arapça parçaların türü", "", "`build_db` üretir.", "", "| eski | yeni | dayanak | sayı |", "|---|---|---|---:|"]
    lines += [f"| {o} | {n} | {s} | {c} |" for (o, n, s), c in sorted(report.decided.items())]
    lines += ["", "## Eser başına (yalnız değişenler)", "", "| eser | tür | dayanak | sayı |", "|---|---|---|---:|"]
    lines += [f"| {w} | {k} | {s} | {c} |" for (w, k, s), c in sorted(report.by_work.items())]
    lines += ["", f"## Kaynağın işaretiyle çatışan ({len(report.conflicts)})", ""]
    lines += [f"- `{p}` {k}: {why} — {t[:80]}" for p, k, why, t in report.conflicts]
    (folder / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    rng = random.Random(14)
    for name, rows in report.samples.items():
        chosen = rng.sample(rows, min(sample, len(rows)))
        (folder / f"sample-{name}.md").write_text(
            f"# {name} ({len(rows)} parçadan {len(chosen)})\n\n" + "\n".join(
                f"{i}. `{p}`\n   - {b} **{t}** {a}\n   - {src or '—'}\n" for i, (p, b, t, a, src) in enumerate(chosen, 1)),
            encoding="utf-8")


