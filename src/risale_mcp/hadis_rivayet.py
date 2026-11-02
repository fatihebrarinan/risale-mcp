"""Rivayet denetimi: eşleşmenin yanındaki işaretler (`docs/hadis-plani.md`, Adım 5).

    uv run python -m risale_mcp.hadis_rivayet     # data/interim/hadis/rivayet.{md,json}

Hüküm verilmez, hiçbir eşleşme silinmez, `hadith_support` değişmez. Kurallar metne bakar ve yalnız okunacak yeri gösterir:
"sözün sahibi" dil kuralıdır, senet tenkidi değildir. Yöntem Risale'ye bağlı değildir: metin, kitap adı, senet alır.

    book_kind  kitabın türü, adından: hadis, siyer, tefsir, tabakat, zuhd, mevzu, diger. Eşleşme her zaman hadis kitabı
               değildir; `mevzu` sözü çürütmek için de anar
    chain      senet: Sanadset zincir uzunluğu (0 = "No SANAD"), Hadith API'de bilinmez (None)
    speaker    eşleşmeden önceki son anılan kişi. prophet: en son Peygamber anılmış, araya başkası girmemiş; other: sonra
               başkası ("قال ابن عباس", "رضي الله عنه"), addressed: "يا رسول الله" diyen başkası; none: Peygamber anılmıyor;
               start: söz metnin başında, öncesi yok. Örneklemde `none` çoğu kez örtük "قال"dır ve `other`da Peygamber
               sonradan konuşabilir: tek rivayet için hüküm olmaz, parça düzeyinde okunacak kuyruk verir
    verdict    eşleşmeden sonraki kısa pencerede: denied ("ليس بحديث", "لا أصل له", "موضوع", "باطل"), weakened ("ضعيف",
               "منكر"), other_saying ("من كلام", "من قول"). Ravi hakkındaki söz de tutabilir, okunmadan hüküm sayılmaz
"""

import csv
import json
import re
import unicodedata
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

from risale_mcp.hadis import CAUTION_BOOKS, TITLES, read_reports
from risale_mcp.hadis_adaylar import kept_words, measure, stems
from risale_mcp.hadis_eval import is_holdout
from risale_mcp.paths import HADIS_PATH, INTERIM_DIR, RAW_DIR

AFTER = 30      # eşleşmeden sonra bakılan kelime
BOOK_KINDS = (
    ("mevzu", re.compile(CAUTION_BOOKS.pattern + r"|الأسرار المرفوعة|الفوائد المجموعة|المصنوع|كشف الخفاء|المقاصد الحسنة|الموضوعات")),
    ("tefsir", re.compile(r"تفسير|تأويل|معالم التنزيل|أحكام القرآن|الدر المنثور|زاد المسير|الكشف والبيان|أسباب النزول|فضائل القرآن")),
    ("tabakat", re.compile(r"طبقات|الطبقات|الجرح|الكامل في|الكنى|تهذيب|سير أعلام|تذكرة الحفاظ|الإصابة|أسد الغابة|ميزان|لسان الميزان|الثقات|معرفة الصحابة")),
    ("siyer", re.compile(r"تاريخ|البداية والنهاية|سيرة|السيرة|المغازي|دلائل النبوة|الشمائل|أخبار|فتوح")),
    ("zuhd", re.compile(r"زهد|الرقائق|الرقة|ذم |حلية الأولياء|مكارم|الورع|الصمت|المجالسة|عيون")),
    ("hadis", re.compile(r"صحيح|سنن|السنن|مسند|مصنف|معجم|المعجم|مستدرك|المستدرك|موطأ|مستخرج|جامع|الأربعين|أربعون|جزء|أمالي|مشيخة|فوائد|شعب الإيمان|إتحاف|مجمع|الأدب المفرد|صفوة")),
)
_PLAIN = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ى": "ي", "ة": "ه", "ـ": None})
_PROPHET = re.compile(r"(يا )?(?:رسول الله|نبي الله|رسول الل|النبي|رسول)")
_OTHER = re.compile(r"رضي الله عن|(?:قال|قالت|فقال|وقال|يقول|سمعت)\s+(?:ابن|ابو|ابي|عمر|علي|عثمان|عائشه|انس|جابر|معاذ|عبد الله|سفيان|مجاهد|الحسن|قتاده|عكرمه|كعب|وهب)")
_DENIED = re.compile(r"(?<!ليس ب)(?<!ليس )(?:ليس بحديث|ليس حديثا|لا اصل له|ليس له اصل|لا اصل لهذا|موضوع\b|الموضوعات|باطل\b|مكذوب|لم يثبت|لا يصح|لا يثبت)")
_WEAK = re.compile(r"(?<!ليس ب)(?:ضعيف\b|منكر\b|فيه نظر)")
_OTHER_SAYING = re.compile(r"من كلام|من قول|من الاسرائيليات")


def plain(text: str) -> str:
    """Harekesiz, elif ve yaları birleşmiş metin; işaret aramak için."""
    return "".join(c for c in unicodedata.normalize("NFKC", text) if not unicodedata.category(c).startswith("M")).translate(_PLAIN)


def book_kind(title: str) -> str:
    if title in TITLES.values():
        return "hadis"
    return next((kind for kind, pattern in BOOK_KINDS if pattern.search(title)), "diger")


def speaker(before: str) -> str:
    if not before.strip():
        return "start"
    mentions = list(_PROPHET.finditer(before))
    if not mentions:
        return "none"
    last = mentions[-1]
    if last.group(1):
        return "addressed"
    return "other" if _OTHER.search(before, last.end()) else "prophet"


def verdict(after: str) -> str | None:
    for name, pattern in (("denied", _DENIED), ("other_saying", _OTHER_SAYING), ("weakened", _WEAK)):
        if pattern.search(after):
            return name
    return None


@dataclass(frozen=True)
class Audit:
    book_kind: str
    chain: int | None
    speaker: str
    verdict: str | None
    verdict_text: str | None = None


def audit(part: str, report: str, title: str, chain: int | None) -> Audit:
    """Eşleşen pencerenin önü ve ardı; pencere kelime kelime, ağırlıksız bulunur."""
    query = stems(part)
    body = stems(report)
    score = measure(query, body, dict.fromkeys(query, 1.0))
    kept = kept_words(report)
    before, after = plain(" ".join(kept[:score.start])), plain(" ".join(kept[score.end + 1:score.end + 1 + AFTER]))
    found = verdict(after)
    return Audit(book_kind(title), chain, speaker(before), found, after if found else None)


def chains(ids: set[int], raw: Path = RAW_DIR) -> dict[int, int]:
    csv.field_size_limit(10 ** 9)
    with open(raw / "sanadset" / "sanadset.csv", encoding="utf-8", errors="replace", newline="") as f:
        return {i: int(r["Sanad_Length"] or 0) for i, r in enumerate(csv.DictReader(f)) if i in ids}


def _chain(report_id: str, known: dict[int, int]) -> int | None:
    return known.get(int(report_id.split(":")[1])) if report_id.startswith("sanadset:") else None


QUEUES = {"denied": "Sözün yanında reddeden ifade", "other_saying": "Başkasının sözü denilmiş",
          "only_caution": "Rivayetleri yalnız mevzu ve zayıf kitaplarında", "no_prophet": "Hiçbir rivayette Peygamber'e bağlı görünmüyor",
          "no_chain": "Hiçbir rivayette senet yok", "weakened": "Sözün yanında zayıflatan ifade"}


def queues(rows: list[dict]) -> dict[str, str]:
    """Bir parçanın düştüğü kuyruklar: tek rivayetten çıkmaz, parçanın bütün rivayetlerine bakılır."""
    out = []
    if any(r["verdict"] == "denied" for r in rows):
        out.append("denied")
    if any(r["verdict"] == "other_saying" for r in rows):
        out.append("other_saying")
    if all(r["book_kind"] == "mevzu" for r in rows):
        out.append("only_caution")
    if not any(r["speaker"] == "prophet" for r in rows):
        out.append("no_prophet")
    if all(r["chain"] == 0 for r in rows):
        out.append("no_chain")
    if any(r["verdict"] == "weakened" for r in rows):
        out.append("weakened")
    return out


def _texts_of(ids: set[str], raw: Path) -> dict[str, tuple[str, str]]:
    return {r.id: (r.title, r.text) for r in read_reports(raw) if r.id in ids}


def build(raw: Path = RAW_DIR, out_dir: Path = INTERIM_DIR / "hadis") -> dict:
    data = json.loads(HADIS_PATH.read_text("utf-8"))
    candidates = json.loads((out_dir / "adaylar.json").read_text("utf-8"))["parts"]
    texts = _part_texts()
    pairs: list[tuple[str, str, str, str]] = []     # küme, anahtar, metin, rivayet
    for key, entry in data["parts"].items():
        if entry["match"] in ("found", "partly_found") and key in texts:
            pairs += [(entry["match"], key, texts[key], r) for r in entry["reports"]]
    for part in candidates:
        if part["tier"] != "review":
            chosen = [c for c in part["candidates"] if c["in_cited_chapter"]] or part["candidates"][:1]
            pairs += [(f"aday_{part['tier']}", part["key"], part["text"], c["report"]) for c in chosen]
    ids = {p[3] for p in pairs}
    known = chains({int(r.split(":")[1]) for r in ids if r.startswith("sanadset:")}, raw)
    reports = _texts_of(ids, raw)
    rows = [{"set": kind, "key": key, "part": part, "report": rid, "title": reports[rid][0], "holdout": is_holdout(key),
             **asdict(audit(part, reports[rid][1], reports[rid][0], _chain(rid, known)))}
            for kind, key, part, rid in pairs]
    grouped: dict[tuple[str, str], list[dict]] = {}
    for row in rows:
        grouped.setdefault((row["set"], row["key"]), []).append(row)
    parts = [{"set": s, "key": k, "part": v[0]["part"], "holdout": v[0]["holdout"], "reports": len(v), "queues": queues(v)}
             for (s, k), v in grouped.items()]
    result = {"rows": rows, "parts": parts}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "rivayet.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), "utf-8")
    (out_dir / "rivayet.md").write_text(render(result), "utf-8")
    return result


def summary(result: dict) -> list[str]:
    rows, parts = result["rows"], result["parts"]
    sets = sorted({p["set"] for p in parts})
    lines = ["\n## Rivayet denetimi (Adım 5, okunacak kuyruklar, hüküm değil)\n", f"| kuyruk | {' | '.join(sets)} |", f"|---|{'---|' * len(sets)}",
             f"| parça | {' | '.join(str(sum(p['set'] == s for p in parts)) for s in sets)} |"]
    for queue, title in QUEUES.items():
        lines.append(f"| {title} | {' | '.join(str(sum(p['set'] == s and queue in p['queues'] for p in parts)) for s in sets)} |")
    lines.append(f"| hiçbiri | {' | '.join(str(sum(p['set'] == s and not p['queues'] for p in parts)) for s in sets)} |")
    sahih = [r for r in rows if r["title"] in (TITLES["bukhari"], TITLES["muslim"])]
    lines.append(f"\nYanlış alarm ölçüsü: Buhârî ve Müslim'den {len(sahih)} kayıtta `denied` {sum(r['verdict'] == 'denied' for r in sahih)}, "
                 f"`weakened` {sum(r['verdict'] == 'weakened' for r in sahih)}.")
    lines.append(f"\nKitap türü (rivayet): {dict(Counter(r['book_kind'] for r in rows).most_common())}")
    lines.append(f"\nSöz sahibi (rivayet): {dict(Counter(r['speaker'] for r in rows).most_common())}")
    return lines


def render(result: dict) -> str:
    lines = ["# Rivayet denetimi", *summary(result)]
    by_key = {}
    for r in result["rows"]:
        by_key.setdefault((r["set"], r["key"]), []).append(r)
    for queue, title in QUEUES.items():
        chosen = [p for p in result["parts"] if queue in p["queues"]]
        lines.append(f"\n# {title} ({len(chosen)})")
        for p in chosen:
            lines.append(f"\n## {p['part']} ({p['set']})\n")
            for r in by_key[p["set"], p["key"]]:
                note = f" {r['verdict']}: {r['verdict_text'][:160]}" if r["verdict"] else ""
                lines.append(f"- {r['title']} ({r['report']}), {r['book_kind']}, senet {r['chain']}, {r['speaker']}{note}")
    return "\n".join(lines) + "\n"


def _part_texts() -> dict[str, str]:
    from risale_mcp.db import connect
    from risale_mcp.paths import DB_PATH
    return {r["key"]: r["text"] for r in connect(DB_PATH).execute(
        "SELECT a.hadith_key AS key, substr(p.text, a.span_start + 1, a.span_end - a.span_start) AS text FROM arabic a"
        " JOIN paragraphs p ON p.id = a.paragraph_id JOIN works w ON w.slug = p.work"
        " WHERE a.hadith_key IS NOT NULL AND p.text IS NOT NULL AND w.language != 'os'")}


def main() -> None:
    print("\n".join(summary(build())))


if __name__ == "__main__":
    main()
