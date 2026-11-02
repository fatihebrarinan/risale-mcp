"""Bağımsız model okuması: künyeyi ve önceki kararı görmeden (`docs/hadis-plani.md`, Adım 7).

    uv run python -m risale_mcp.hadis_okuma prepare   # data/interim/hadis/okuma/batch-N.json, key.json
    uv run python -m risale_mcp.hadis_okuma score     # okuma/*-answers.json -> okuma.{md,json}

Okuyucu yalnız iki Arapça metni görür: parça ve rivayetin eşleşen yeri. Kitap adı, künye, seviye, dayanak gizlidir
(`key.json`, okuyucuya verilmez). Kontrol: parçaya rastgele başka parçanın rivayeti verilen çiftler (`decoy`) araya
karışır; okuyucunun "aynı söz" deme eğilimini ölçer. Her parti iki okuyucuya gider, ayrılan çift kuyrukta kalır.
Okuma hüküm değildir, `hadith_support`'u değiştirmez; hadisçi örneklemi (Adım 8) bunun üstüne kurulur.
"""

import json
import random
import sys
from collections import Counter
from pathlib import Path

from risale_mcp.hadis import read_reports
from risale_mcp.hadis_adaylar import kept_words, measure, stems
from risale_mcp.paths import INTERIM_DIR, RAW_DIR

BATCHES = 3
DECOYS = 30
CONTEXT = 35            # eşleşmenin iki yanında gösterilen kelime
SAME = ("verbatim", "abridged", "by_meaning")
OUT = INTERIM_DIR / "hadis" / "okuma"


def window(part: str, report: str) -> str:
    query, body = stems(part), stems(report)
    score = measure(query, body, dict.fromkeys(query, 1.0))
    kept = kept_words(report)
    return " ".join(kept[max(0, score.start - CONTEXT):score.end + CONTEXT + 1])


def pick(rows: list[dict], queued: bool) -> list[dict]:
    """En güçlü görünen rivayet; kuyruktaki parçada bir ikincisi, başka kitaptan."""
    ordered = sorted(rows, key=lambda r: (r["book_kind"] != "hadis", r["speaker"] != "prophet", r["verdict"] is not None))
    chosen = ordered[:1]
    if queued:
        chosen += next(([r] for r in ordered[1:] if r["title"] != ordered[0]["title"]), [])
    return chosen


def prepare(raw: Path = RAW_DIR, out: Path = OUT, seed: int = 14) -> Counter:
    audited = json.loads((INTERIM_DIR / "hadis" / "rivayet.json").read_text("utf-8"))
    groups: dict[tuple[str, str], list[dict]] = {}
    for row in audited["rows"]:
        groups.setdefault((row["set"], row["key"]), []).append(row)
    pairs = []
    for p in audited["parts"]:
        pairs += [{"set": p["set"], "key": p["key"], "part": p["part"], "report": r["report"], "title": r["title"],
                   "holdout": p["holdout"], "queues": p["queues"], "decoy": False} for r in pick(groups[p["set"], p["key"]], bool(p["queues"]))]
    rng = random.Random(seed)
    donors = rng.sample(pairs, DECOYS)
    for donor in donors:
        other = rng.choice([p for p in pairs if p["key"] != donor["key"]])
        pairs.append({**other, "report": donor["report"], "title": donor["title"], "decoy": True, "queues": []})
    wanted = {p["report"] for p in pairs}
    texts = {r.id: r.text for r in read_reports(raw) if r.id in wanted}
    rng.shuffle(pairs)
    out.mkdir(parents=True, exist_ok=True)
    for i, p in enumerate(pairs):
        p["id"] = f"x{i:03d}"
    for b in range(BATCHES):
        items = [{"id": p["id"], "a": p["part"], "b": window(p["part"], texts[p["report"]])} for p in pairs[b::BATCHES]]
        (out / f"batch-{b}.json").write_text(json.dumps(items, ensure_ascii=False, indent=0), "utf-8")
    (out / "key.json").write_text(json.dumps(pairs, ensure_ascii=False, indent=0), "utf-8")
    return Counter(("decoy" if p["decoy"] else p["set"]) for p in pairs)


def same(answer: dict) -> bool:
    return answer["relation"] in SAME


def score(out: Path = OUT) -> dict:
    key = {p["id"]: p for p in json.loads((out / "key.json").read_text("utf-8"))}
    readers: dict[str, dict] = {}
    for path in sorted(out.glob("*-answers.json")):
        reader = path.name.split("-")[0]
        readers.setdefault(reader, {}).update({a["id"]: a for a in json.loads(path.read_text("utf-8"))})
    names = sorted(readers)
    rows = []
    for pid, pair in key.items():
        answers = [readers[n].get(pid) for n in names]
        if all(answers):
            agree = len({a["relation"] for a in answers}) == 1
            rows.append({**pair, "answers": answers, "agree": agree, "agree_same": len({same(a) for a in answers}) == 1})
    return {"rows": rows, "readers": names, "missing": len(key) - len(rows)}


def summary(result: dict) -> list[str]:
    rows = result["rows"]
    lines = ["\n## Bağımsız okuma (Adım 7; model okuması, hüküm değil)\n", f"Okunan çift: {len(rows)}, eksik: {result['missing']}.\n",
             "| küme | çift | ikisi de aynı söz | ikisi de değil | ayrılan |", "|---|---|---|---|---|"]
    for name in ("decoy", "found", "partly_found", "aday_chapter", "aday_close"):
        chosen = [r for r in rows if (r["decoy"] if name == "decoy" else not r["decoy"] and r["set"] == name)]
        both = sum(all(same(a) for a in r["answers"]) for r in chosen)
        none = sum(not any(same(a) for a in r["answers"]) for r in chosen)
        lines.append(f"| {name} | {len(chosen)} | {both} | {none} | {len(chosen) - both - none} |")
    real = [r for r in rows if not r["decoy"]]
    lines.append(f"\nİlişki türünde tam uyum: {sum(r['agree'] for r in real)}/{len(real)}. "
                 f"Aynı söz mü sorusunda uyum: {sum(r['agree_same'] for r in real)}/{len(real)}.")
    lines.append(f"\nİlişki (ilk okuyucu): {dict(Counter(r['answers'][0]['relation'] for r in real).most_common())}")
    lines.append(f"\nSöz sahibi (ikisi de aynı): {dict(Counter(r['answers'][0]['speaker'] for r in real if len({a['speaker'] for a in r['answers']}) == 1).most_common())}")
    return lines


def render(result: dict) -> str:
    lines = ["# Bağımsız okuma", *summary(result)]
    def block(title, chosen):
        lines.append(f"\n# {title} ({len(chosen)})\n")
        for r in chosen:
            notes = " / ".join(f"{a['relation']} {a['speaker']} {a['confidence']}: {a['note']}" for a in r["answers"])
            lines.append(f"- `{r['id']}` {r['part']} ({r['set']}, {r['title']}, {r['report']}, {r['queues']}): {notes}")
    rows = result["rows"]
    block("Kontrol çiftinde aynı söz denilen", [r for r in rows if r["decoy"] and any(same(a) for a in r["answers"])])
    block("Okuyucular ayrıldı", [r for r in rows if not r["decoy"] and not r["agree_same"]])
    block("İkisi de aynı söz değil dedi", [r for r in rows if not r["decoy"] and not any(same(a) for a in r["answers"])])
    block("Reddi ikisi de gördü", [r for r in rows if not r["decoy"] and all(a["denied"] for a in r["answers"])])
    block("Söz başkasının", [r for r in rows if not r["decoy"] and all(same(a) and a["speaker"] == "other" for a in r["answers"])])
    return "\n".join(lines) + "\n"


def main() -> None:
    if sys.argv[1:] == ["prepare"]:
        print(prepare())
    else:
        result = score()
        (OUT.parent / "okuma.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), "utf-8")
        (OUT.parent / "okuma.md").write_text(render(result), "utf-8")
        print("\n".join(summary(result)))


if __name__ == "__main__":
    main()
