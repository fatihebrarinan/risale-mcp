"""HA2 ölçümü (MVP M3): Risale'nin hadislerini yalnız kütüphanedeki kitaplarla eşlemek ne bulur, ne kaybettirir.

    uv run python -m risale_mcp.hadis_kutuphane      # rapor data/interim/hadis/ha2-olcum.md (+ .json)

Bugünkü eşleme (`hadis.py`) Sanadset'in 954 kitabından ve Hadith API'den yapılır; Sanadset'te tefsir, tarih,
tabakât ve mevzu derleyen kitaplar da var, kitap baskısı belirsiz. HA2'nin hedefi eşleşmenin yalnız kütüphanedeki
(`data/library/hadis/kutub/`: Kütüb-i Sitte, Muvatta ve MVP'nin dokuz kitabı; baskısı ve sayfası belli) kitaplardan
gelmesidir. Bu modül yalnız ölçer: aynı eşleyiciyle (`hadis.Corpus.match`) iki derlemi karşılaştırır, parça başına
sonucu yazar. `matches.json`'a ve veritabanına dokunmaz; geçiş kararı kullanıcınındır.
"""

import json
from collections import Counter
from pathlib import Path

from risale_mcp.db import connect
from risale_mcp.hadis import Corpus, Report, identifies, read_reports
from risale_mcp.paths import DB_PATH, INTERIM_DIR, LIBRARY_DIR, RAW_DIR
from risale_mcp.quran import skeleton

KUTUB_DIR = LIBRARY_DIR / "hadis" / "kutub"
ORDER = ("found", "partly_found", "phrase_found", "none", "short")


def library_reports(root: Path = KUTUB_DIR) -> list[Report]:
    """Kütüphanedeki her kitabın hadisleri (metin: senet ve metin birlikte; katmanlar hariç)."""
    out = []
    for path in sorted(root.glob("*.json")):
        book = json.loads(path.read_text(encoding="utf-8"))
        for h in book["hadiths"]:
            if text := (h.get("text") or "").strip():
                out.append(Report(f"{book['book']}:{h['number']}", book["title"], str(h["number"]), text, "kutuphane"))
    return out


def parts(db: Path = DB_PATH) -> dict[str, str]:
    """Risale'deki hadis parçaları (iskelet anahtarıyla), `hadis.build`'deki gibi."""
    conn = connect(db)
    out = {}
    for row in conn.execute("SELECT substr(p.text, a.span_start + 1, a.span_end - a.span_start) AS text"
                            " FROM arabic a JOIN paragraphs p ON p.id = a.paragraph_id"
                            " WHERE a.kind = 'hadis' AND p.text IS NOT NULL"):
        out.setdefault(skeleton(row["text"]), row["text"])
    return out


def compare(db: Path = DB_PATH, raw: Path = RAW_DIR) -> dict:
    texts = parts(db)
    library = Corpus(library_reports())
    current = Corpus(list(read_reports(raw)))
    rows, table = [], Counter()
    for key, text in texts.items():
        a, found_a, _ = current.match(text)
        b, found_b, _ = library.match(text)
        table[(a, b)] += 1
        rows.append({"text": text[:120], "identifies": identifies(text), "current": a, "library": b,
                     "current_books": sorted({current.reports[i].title for i in found_a})[:4],
                     "library_books": sorted({library.reports[i].title for i in found_b})[:4]})
    return {"parts": len(texts), "table": {f"{a} → {b}": n for (a, b), n in sorted(table.items())}, "rows": rows,
            "library_size": len(library.reports)}


def report(result: dict) -> str:
    rows, table = result["rows"], Counter()
    for r in rows:
        table[(r["current"], r["library"])] += 1
    by = lambda side: Counter(r[side] for r in rows)
    cur, lib = by("current"), by("library")
    lines = ["# HA2 ölçümü: Risale'nin hadisleri yalnız kütüphanedeki kitaplarla", "",
             f"Parça: {result['parts']} (tekil iskelet). Kütüphane: {result['library_size']} hadis (Kütüb-i Sitte, Muvatta, "
             "MVP'nin dokuz kitabı). Bugünkü derlem: Sanadset ve Hadith API. Eşleyici aynı (`hadis.Corpus.match`).", "",
             "| Sonuç | Bugün | Yalnız kütüphane |", "|---|---|---|"]
    lines += [f"| {k} | {cur.get(k, 0)} | {lib.get(k, 0)} |" for k in ORDER]
    lines += ["", "## Geçişler (bugün → kütüphane)", "", "| Bugün | Kütüphane | Parça |", "|---|---|---|"]
    lines += [f"| {a} | {b} | {n} |" for (a, b), n in sorted(table.items(), key=lambda x: -x[1])]
    lost = [r for r in rows if ORDER.index(r["library"]) > ORDER.index(r["current"])]
    gained = [r for r in rows if ORDER.index(r["library"]) < ORDER.index(r["current"])]
    for title, group in (("Kaybedilenler (kütüphanede daha zayıf)", lost), ("Kazanılanlar (kütüphanede daha güçlü)", gained)):
        lines += ["", f"## {title}: {len(group)}", "", "| Parça | Bugün (kitaplar) | Kütüphane (kitaplar) |", "|---|---|---|"]
        lines += [f"| {r['text'][:70]} | {r['current']} ({', '.join(r['current_books'])}) | "
                  f"{r['library']} ({', '.join(r['library_books'])}) |" for r in group[:80]]
    return "\n".join(lines) + "\n"


def main() -> None:
    result = compare()
    out = INTERIM_DIR / "hadis" / "ha2-olcum.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report(result), encoding="utf-8")
    out.with_suffix(".json").write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result["table"], ensure_ascii=False))
    print(out)


if __name__ == "__main__":
    main()
