"""Adım 3–7'nin yerel kaydı: lafız farkı adayları, model okuması ve rivayet denetiminin uyarıları (`docs/kaynakca-plani.md`, K3).

    uv run python -m risale_mcp.hadis_okumalar     # data/interim/hadis/{adaylar,okuma,rivayet}.json -> data/library/hadis/readings.json

Yalnız `kisisel` profil okur (`build_db`): hadisçi görmeden genel sunucuya çıkmaz (kullanıcının kararı, 2026-11-03).
Hiçbiri hüküm değildir ve `hadith_support`'u değiştirmez:

- `candidates`: derlemde lafzı tutmayan parçanın, iki model okuyucunun okuduğu adayı (Adım 3 ve 7). `relation` iki
  okuyucunun cevabı (verbatim, abridged, by_meaning, related, different), `same` ikisi de aynı söz dedi mi.
- `readings`: bulunan (`found`, `partly_found`) eşleşmenin okunan rivayeti; ilişki ve söz sahibi.
- `flags`: rivayet denetiminin kuyrukları (reddeden ifade, başkasının sözü, yalnız mevzu kitaplarında, Peygamber'e
  bağlı görünmüyor, senet yok, zayıflatan ifade); `verdicts` ifadenin kendisi, kitabıyla.

Rivayet metinleri ham derlemden bir kez alınır; `matches.json`'da olmayan aday rivayetler `reports`'a girer.
"""

import json
from pathlib import Path

from risale_mcp.hadis import read_reports
from risale_mcp.paths import INTERIM_DIR, LIBRARY_DIR, RAW_DIR

READINGS_PATH = LIBRARY_DIR / "hadis" / "readings.json"
CANDIDATE_SETS = ("aday_chapter", "aday_close")


def build(interim: Path = INTERIM_DIR / "hadis", raw: Path = RAW_DIR, out: Path = READINGS_PATH) -> dict:
    okuma = json.loads((interim / "okuma.json").read_text("utf-8"))["rows"]
    rivayet = json.loads((interim / "rivayet.json").read_text("utf-8"))
    adaylar = {p["key"]: p for p in json.loads((interim / "adaylar.json").read_text("utf-8"))["parts"]}
    parts: dict[str, dict] = {}

    def part(key: str) -> dict:
        return parts.setdefault(key, {"candidates": [], "readings": [], "flags": [], "verdicts": []})

    for row in okuma:
        if row["decoy"]:
            continue
        a, b = row["answers"]
        reading = {"report": row["report"], "relation": [a["relation"], b["relation"]],
                   "speaker": [a["speaker"], b["speaker"]], "denied": bool(a["denied"] and b["denied"]),
                   "same": bool(row["agree_same"] and a["relation"] in ("verbatim", "abridged", "by_meaning"))}
        if row["set"] in CANDIDATE_SETS:
            cand = next((c for c in adaylar[row["key"]]["candidates"] if c["report"] == row["report"]), {})
            part(row["key"])["candidates"].append({**reading, "tier": adaylar[row["key"]]["tier"],
                                                   "in_cited_chapter": bool(cand.get("in_cited_chapter"))})
        else:
            part(row["key"])["readings"].append(reading)
    for p in rivayet["parts"]:
        if p["queues"]:
            part(p["key"])["flags"] = sorted(set(part(p["key"])["flags"]) | set(p["queues"]))
    for row in rivayet["rows"]:
        if row["verdict"] and row["verdict_text"]:
            part(row["key"])["verdicts"].append({"report": row["report"], "verdict": row["verdict"], "text": row["verdict_text"]})
    wanted = {c["report"] for p in parts.values() for c in p["candidates"] + p["readings"]} | \
             {v["report"] for p in parts.values() for v in p["verdicts"]}
    reports = {r.id: {"title": r.title, "number": r.number, "text": r.text, "source": r.source, "grades": list(r.grades)}
               for r in read_reports(raw) if r.id in wanted}
    result = {"parts": parts, "reports": reports}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False), "utf-8")
    return result


def main() -> None:
    result = build()
    parts = result["parts"].values()
    print(f"yazıldı: {READINGS_PATH}; parça {len(result['parts'])}, aday {sum(len(p['candidates']) for p in parts)}"
          f" (ikisi de aynı söz {sum(c['same'] for p in parts for c in p['candidates'])}), okuma "
          f"{sum(len(p['readings']) for p in parts)}, uyarılı parça {sum(bool(p['flags']) for p in parts)},"
          f" rivayet {len(result['reports'])}")


if __name__ == "__main__":
    main()
