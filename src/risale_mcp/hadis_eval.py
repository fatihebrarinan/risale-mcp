"""Hadis eşlemesinin ölçümü: her adımın katkısı ve hatası (`docs/hadis-plani.md`).

    uv run python -m risale_mcp.hadis_eval freeze    # negatif kontrol havuzunu dondurur (bir kez)
    uv run python -m risale_mcp.hadis_eval run [ad]  # rapor: data/interim/hadis/<ad>.md

Negatif kontrol: müellifin hadis işaretsiz, mealsiz Arapçası. Kur'ân'da geçenler ve işaretli hadisler çıkarılır.
Derlemde tutması üst sınırdır, kesin hata payı değil: havuzda işaretsiz gerçek hadis de vardır. Havuz dondurulmuştur,
sonraki adımların bulduğu adaylar onu değiştirmez.

Sınama kümesi (`is_holdout`): parçaların üçte biri anahtarın özetiyle ayrılır; eşik ayarında bakılmaz, yalnız sonda.
Karşı sınama (`shuffled`): kısa parçalara başka parçaların künyesi verilir. Yanlış künyeyle tutma oranı yöntemin taban
gürültüsüdür; gerçek künyeyle aradaki fark gücüdür. Sınama kümesi burada da ayrı sayılır.

Ana metin: Osmanlıca ciltler sayıya girmez (aynı metnin Envar baskısı), yalnız onlarda duranlar ayrı gösterilir.
"""

import hashlib
import json
import random
import sys
from collections import Counter
from pathlib import Path

from risale_mcp.db import connect
from risale_mcp.hadis import MIN_MATCH, Corpus, identifies, read_reports, words
from risale_mcp.hadis_kunye import parse as parse_citation
from risale_mcp.paths import DB_PATH, HADIS_PATH, INTERIM_DIR, RAW_DIR, ROOT
from risale_mcp.quran import Quran, pieces, skeleton

CONTROL_PATH = ROOT / "tests" / "golden" / "hadis_control.json"


def is_holdout(key: str) -> bool:
    return hashlib.sha1(key.encode()).digest()[0] % 3 == 0


def freeze(db: Path = DB_PATH, out: Path = CONTROL_PATH) -> int:
    conn, quran = connect(db), Quran.load()
    hadiths = {r[0] for r in conn.execute("SELECT DISTINCT hadith_key FROM arabic WHERE hadith_key IS NOT NULL")}
    pool = {}
    for row in conn.execute(
            "SELECT substr(p.text, a.span_start + 1, a.span_end - a.span_start) AS text FROM arabic a"
            " JOIN paragraphs p ON p.id = a.paragraph_id JOIN works w ON w.slug = p.work"
            " WHERE a.kind = 'arabi' AND a.meal IS NULL AND p.text IS NOT NULL AND w.language = 'tr'"):
        key = skeleton(row["text"])
        if len(key) >= MIN_MATCH and key not in hadiths and not any(quran.find(p) for p in pieces(row["text"])):
            pool.setdefault(key, row["text"])
    out.write_text(json.dumps({"note": __doc__.split("\n\n")[2], "pool": sorted(pool.values())}, ensure_ascii=False, indent=0), "utf-8")
    return len(pool)


def rows(db: Path) -> list:
    return connect(db).execute(
        "SELECT a.hadith_key AS key, a.hadith_support AS support, w.language AS language FROM arabic a"
        " JOIN paragraphs p ON p.id = a.paragraph_id JOIN works w ON w.slug = p.work"
        " WHERE a.hadith_key IS NOT NULL AND p.text IS NOT NULL").fetchall()


def _table(title: str, counts: Counter) -> list[str]:
    return [f"\n## {title}\n", "| | sayı |", "|---|---|", *(f"| {k} | {v} |" for k, v in sorted(counts.items(), key=str))]


def control(corpus: Corpus) -> Counter:
    pool = json.loads(CONTROL_PATH.read_text("utf-8"))["pool"]
    counts = Counter()
    for text in pool:
        band = "5+ kelime" if identifies(text) else "4 ve daha az kelime"
        counts[f"{band} denenen"] += 1
        counts[f"{band} {corpus.match(text)[0]}"] += 1
    return counts


def located_rates(corpus: Corpus, db: Path, parts: dict, rounds: int = 5) -> list[str]:
    """Kısa parçalar: kelime sayısına göre gerçek künye ve karıştırılmış künyeyle tutma oranı."""
    seen: dict[str, tuple[str, str]] = {}
    for row in connect(db).execute(
            "SELECT a.hadith_key AS key, a.source, substr(p.text, a.span_start + 1, a.span_end - a.span_start) AS text"
            " FROM arabic a JOIN paragraphs p ON p.id = a.paragraph_id JOIN works w ON w.slug = p.work"
            " WHERE a.hadith_key IS NOT NULL AND a.source IS NOT NULL AND p.text IS NOT NULL AND w.language != 'os'"):
        if parts.get(row["key"], {}).get("match") in ("short", "phrase_found"):
            seen.setdefault(row["key"], (row["text"], row["source"]))
    items = [(k, *v) for k, v in seen.items() if parse_citation(v[1]).citations[0].book]
    def tally(pairs) -> Counter:
        counts = Counter()
        for key, text, source in pairs:
            n = min(len(words(text)), 5)
            group = f"{'sınama' if is_holdout(key) else 'ayar'} {n} kelime"
            counts[group, "n"] += 1
            counts[group, corpus.locate(text, parse_citation(source).citations)[0]] += 1
        return counts
    real, fake = tally(items), Counter()
    rng = random.Random(14)
    for _ in range(rounds):
        sources = [s for *_, s in items]
        rng.shuffle(sources)
        fake.update(tally((k, t, s) for (k, t, _), s in zip(items, sources)))
    out = ["\n## Künyeli arama: gerçek künye / karıştırılmış künye\n",
           "| grup | parça | bölümde | kitapta | karışık bölümde | karışık kitapta |", "|---|---|---|---|---|---|"]
    for group in sorted({g for g, _ in real}):
        n = real[group, "n"]
        out.append(f"| {group} | {n} | {real[group, 'chapter']} | {real[group, 'book']} "
                   f"| %{100 * fake[group, 'chapter'] / (n * rounds):.1f} | %{100 * fake[group, 'book'] / (n * rounds):.1f} |")
    return out


def run(name: str, db: Path = DB_PATH, out_dir: Path = INTERIM_DIR / "hadis") -> Path:
    data = rows(db)
    parts = json.loads(HADIS_PATH.read_text("utf-8"))["parts"]
    main = [r for r in data if r["language"] != "os"]
    main_keys = {r["key"] for r in main}
    best = {}
    for r in main:
        best.setdefault(r["key"], set()).add(r["support"])
    lines = [f"# Hadis ölçümü: {name}\n", f"Tekil parça: bütün {len(parts)}, ana metin {len(main_keys)}, "
             f"yalnız Osmanlıca {len(set(parts) - main_keys)}. Geçiş (ana metin): {len(main)}. "
             f"Sınama kümesi: {sum(map(is_holdout, main_keys))} parça."]
    lines += _table("Derlem sonucu (ana metin, tekil)", Counter(parts[k]["match"] for k in main_keys if k in parts))
    lines += _table("Dayanak (ana metin, geçiş)", Counter(r["support"] for r in main))
    lines += _table("Dayanağı geçişe göre ayrılan parça", Counter(len(v) for v in best.values() if len(v) > 1))
    lines += _table("Rivayet sayısı sınıra dayanan parça", Counter(len(parts[k]["reports"]) >= 8 for k in main_keys if k in parts))
    corpus = Corpus(list(read_reports(RAW_DIR)))
    lines += _table("Negatif kontrol (donmuş havuz)", control(corpus))
    lines += located_rates(corpus, db, parts)
    if (candidates := out_dir / "adaylar.json").exists():
        from risale_mcp.hadis_adaylar import summary
        lines += summary(json.loads(candidates.read_text("utf-8")))
    if (turkish := out_dir / "turkce.json").exists():
        lines += _table("Yalnız Türkçe aktarılan hadis adayları (cümle)", Counter(json.loads(turkish.read_text("utf-8"))["counts"]))
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{name}.md"
    path.write_text("\n".join(lines) + "\n", "utf-8")
    return path


def main() -> None:
    args = sys.argv[1:] or ["run"]
    if args[0] == "freeze":
        print(f"donmuş havuz: {freeze()} parça -> {CONTROL_PATH.relative_to(ROOT)}")
    else:
        print(run(args[1] if len(args) > 1 else "son").read_text("utf-8"))


if __name__ == "__main__":
    main()
