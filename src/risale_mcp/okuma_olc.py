"""S13.14: Türkçe yanlış okuma ölçümü. Sohbetin elle bulunmuş okuma hatalarından kurulan set
(`tests/golden/okuma_seti.json`) sohbetin kendi koduyla sorulur (`sohbet_dene.converse`: aynı talimat, araçlar,
model, düzeltme), son turun cevabı bir hakeme (varsayılan Sonnet; `OKUMA_HAKEM`) verilir.

Her madde için:
- **olgular** (facts): cevapta bulunması gerekenler; hakem `stated` (1), `partly` (½), `absent` (0) ya da
  `contradicted` (0, yanlış sayılır) der. Hakeme olgunun kanıt cümleleri de verilir (veritabanından).
- **yanlışlar** (wrong): bilinen yanlış iddialar; hakem `present` ya da `absent` der.
- **okunması beklenen yerler** (must_read): mekanik: `read_section` ya da `get_passage` o bölümü ya da içini okudu mu.

Hakem de yanılabilir: rapor her kararın gerekçesini ve cevabın ilgili sözünü yazar, elle gözden geçirilir. Sayılar
yalnız aynı set ve aynı hakemle karşılaştırılır. Cevaba sayfanın eklediği listeler (öbür yerler, bütün yerler, kapsam
notu) hakeme gitmez: model ne yazdıysa o ölçülür.

    uv run --extra sohbet python -m risale_mcp.okuma_olc run [madde …] [--paralel 4]
    uv run --extra sohbet python -m risale_mcp.okuma_olc hakem <klasör>      # var olan koşuyu yeniden değerlendir
    uv run --extra sohbet python -m risale_mcp.okuma_olc karsilastir <klasör> <klasör>

Döküm `data/interim/sohbet/okuma/<zaman>-<model>/`: `<madde>.json` (konuşma, çağrılar, hakemin kararları), `rapor.md`.
"""

import argparse
import asyncio
import json
import os
import re
from datetime import datetime
from pathlib import Path

from risale_mcp.paths import DATA_DIR

SET = Path(__file__).resolve().parents[2] / "tests" / "golden" / "okuma_seti.json"
OUT_DIR = DATA_DIR / "interim" / "sohbet" / "okuma"
JUDGE_MODEL = os.environ.get("OKUMA_HAKEM", "claude-sonnet-5-5")
READ_TOOLS = ("read_section", "get_passage")
# sayfanın cevaba eklediği bölümler: hakem yalnız modelin yazdığını görür
PAGE_PARTS = (re.compile(r"\n\*\*Konunun geçtiği öbür yerler\*\*.*", re.S), re.compile(r"\n:::ek .*", re.S))

JUDGE_PROMPT = """\
You are checking one answer of a source-grounded chat about the works of Bediüzzaman Said Nursî (Risale-i Nur). The \
answer is in Turkish. You are given the reader's question(s), the answer, a list of FACTS (each with the source \
sentences that establish it) and a list of WRONG claims (misreadings found earlier).

For each fact decide:
- "stated": the answer conveys the fact (in any words, any part of the answer, quotation or prose);
- "partly": it conveys only part of it, or only vaguely;
- "absent": it does not say it;
- "contradicted": it says the opposite or something incompatible.
For each wrong claim decide:
- "present": the answer asserts it or something equivalent (in the text section or in its interpretation section);
- "absent": it does not (saying the opposite is "absent").
Judge only against these lists; do not grade style, length or other content. Give exactly one verdict for each \
listed id and no other ids. Quote the answer's own words that decide each verdict (at most 25 words; empty if \
absent). Write "why" in Turkish, one short sentence.

Reply with JSON only:
{"facts": [{"id": "f1", "verdict": "...", "answer_words": "...", "why": "..."}],
 "wrong": [{"id": "w1", "verdict": "...", "answer_words": "...", "why": "..."}]}"""

FACT_POINTS = {"stated": 1.0, "partly": 0.5, "absent": 0.0, "contradicted": 0.0}


def load_set(path: Path = SET) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["items"]


def model_answer(markdown: str) -> str:
    for pattern in PAGE_PARTS:
        markdown = pattern.sub("", markdown)
    return markdown.strip()


def read_places(calls: list[dict]) -> set[str]:
    """Bu konuşmada okunan bölüm ve cümle kimlikleri (aralıkların ilk ucu, cümle eki atılmadan)."""
    out = set()
    for call in calls:
        if call["tool"] in READ_TOOLS and not call.get("is_error"):
            args = call.get("input") or {}
            place = str(args.get("section") or args.get("id") or "").split("..")[0]
            if place:
                out.add(place)
    return out


def must_read_hits(item: dict, places: set[str]) -> dict[str, bool]:
    """Beklenen yerin kendisi, içi ya da (cümle okunduysa) cümlesi; ya da beklenen yeri içine alan bir bölüm."""
    return {m: any(p == m or p.startswith(m + "/") or m.startswith(p + "/") for p in places)
            for m in item.get("must_read", [])}


def evidence_texts(library, item: dict) -> dict[str, str]:
    ids = {e for f in item["facts"] for e in f.get("evidence", [])}
    return {i: (library.conn.execute("SELECT text FROM sentences WHERE id = ?", (i,)).fetchone() or ["?"])[0]
            for i in sorted(ids)}


def judge_input(item: dict, answer: str, evidence: dict[str, str]) -> str:
    lines = ["QUESTION(S):", *[f"- {q}" for q in item["questions"]], "", "ANSWER (last turn):", answer, "", "FACTS:"]
    for f in item["facts"]:
        lines.append(f"- {f['id']}: {f['text']}")
        lines += [f"    source {e}: {evidence.get(e, '?')}" for e in f.get("evidence", [])]
    lines += ["", "WRONG CLAIMS:", *[f"- {w['id']}: {w['text']}" for w in item["wrong"]]]
    return "\n".join(lines)


def _json(text: str) -> dict:
    start = text.find("{")
    if start < 0:
        raise ValueError("hakem JSON vermedi")
    return json.JSONDecoder().raw_decode(text[start:])[0]        # ardından gelen metin atılır


async def judge(client, item: dict, answer: str, evidence: dict[str, str]) -> dict:
    message = await client.messages.create(
        model=JUDGE_MODEL, max_tokens=2000, system=JUDGE_PROMPT,
        messages=[{"role": "user", "content": judge_input(item, answer, evidence)}])
    text = "".join(b.text for b in message.content if b.type == "text")
    verdicts = _json(text)
    known = {"facts": {f["id"] for f in item["facts"]}, "wrong": {w["id"] for w in item["wrong"]}}
    for kind, ids in known.items():          # hakemin uydurduğu kimlikler atılır
        verdicts[kind] = [v for v in verdicts.get(kind, []) if v.get("id") in ids]
    from risale_mcp.sohbet import cost
    return {**verdicts, "model": JUDGE_MODEL, "cost": round(cost(JUDGE_MODEL, message.usage), 5)}


def score(item: dict, verdicts: dict, hits: dict[str, bool]) -> dict:
    facts = {v["id"]: v["verdict"] for v in verdicts.get("facts", [])}
    wrong = {v["id"]: v["verdict"] for v in verdicts.get("wrong", [])}
    return {"facts": sum(FACT_POINTS.get(facts.get(f["id"], "absent"), 0) for f in item["facts"]),
            "facts_total": len(item["facts"]),
            "wrong": sum(wrong.get(w["id"]) == "present" for w in item["wrong"])
            + sum(facts.get(f["id"]) == "contradicted" for f in item["facts"]),
            "must_read": sum(hits.values()), "must_read_total": len(hits)}


async def evaluate(client, library, item: dict, result: dict) -> dict:
    last = result["turns"][-1] if result["turns"] else None
    if not last or not last.get("markdown"):
        return {"error": (last or {}).get("error") or "cevap yok"}
    calls = [c for t in result["turns"] for c in t["calls"]]
    hits = must_read_hits(item, read_places(calls))
    verdicts = await judge(client, item, model_answer(last["markdown"]), evidence_texts(library, item))
    return {"verdicts": verdicts, "must_read": hits, "score": score(item, verdicts, hits)}


# ------------------------------------------------------------ rapor

def report(rows: list[dict], items: dict[str, dict], title: str) -> str:
    tot = {k: 0.0 for k in ("facts", "facts_total", "wrong", "must_read", "must_read_total")}
    cost = judge_cost = 0.0
    lines = [f"# Okuma ölçümü: {title}", "", f"{datetime.now():%Y-%m-%d %H.%M}, hakem `{JUDGE_MODEL}`.", "",
             "| Madde | Olgu | Yanlış | Okuma |", "|---|---|---|---|"]
    details = []
    for row in rows:
        item, ev = items[row["id"]], row.get("evaluation") or {}
        cost += sum(t["usage"]["cost"] for t in row["result"]["turns"])
        if "score" not in ev:
            lines.append(f"| {row['id']} | hata: {ev.get('error', '?')} | | |")
            continue
        s = ev["score"]
        judge_cost += ev["verdicts"].get("cost", 0)
        for k in tot:
            tot[k] += s[k]
        lines.append(f"| {row['id']} | {s['facts']:g}/{s['facts_total']} | {s['wrong']} | "
                     f"{s['must_read']}/{s['must_read_total']} |")
        details += ["", f"## {row['id']}", "", *[f"> {q}" for q in item["questions"]], ""]
        texts = {**{f["id"]: f["text"] for f in item["facts"]}, **{w["id"]: w["text"] for w in item["wrong"]}}
        for v in ev["verdicts"].get("facts", []) + ev["verdicts"].get("wrong", []):
            mark = {"stated": "✓", "partly": "◑", "absent": "·", "contradicted": "✗", "present": "✗"}.get(v["verdict"], "?")
            details.append(f"- {mark} **{v['id']}** {v['verdict']}: {texts.get(v['id'], '')}")
            if v.get("answer_words"):
                details.append(f"  - cevap: “{v['answer_words']}”")
            if v.get("why"):
                details.append(f"  - gerekçe: {v['why']}")
        missed = [m for m, ok in ev["must_read"].items() if not ok]
        if missed:
            details.append(f"- okunmadı: {', '.join(missed)}")
    lines += [f"| **toplam** | **{tot['facts']:g}/{tot['facts_total']:g}** | **{tot['wrong']:g}** | "
              f"**{tot['must_read']:g}/{tot['must_read_total']:g}** |", "",
              f"Sohbet ≈{cost:.3f} $, hakem ≈{judge_cost:.3f} $.", *details]
    return "\n".join(lines) + "\n"


def totals(folder: Path) -> dict:
    data = json.loads((folder / "sonuc.json").read_text(encoding="utf-8"))
    return {row["id"]: (row.get("evaluation") or {}).get("score") for row in data["rows"]}


# ------------------------------------------------------------ çalıştırma

async def run(chat, client, names: list[str], parallel: int) -> Path:
    from risale_mcp.sohbet_dene import converse
    items = {i["id"]: i for i in load_set()}
    chosen = [items[n] for n in names] if names else list(items.values())
    out = OUT_DIR / f"{datetime.now():%Y%m%d-%H%M%S}-{chat.settings.model}"
    out.mkdir(parents=True)
    gate = asyncio.Semaphore(parallel)

    async def one(item):
        async with gate:
            result = await converse(chat, {"ad": item["id"], "kip": item.get("kip"), "sorular": item["questions"]})
            try:
                evaluation = await evaluate(client, chat.library, item, result)
            except Exception as e:                 # hakemin hatası ölçümü durdurmaz, raporda görünür
                evaluation = {"error": f"{type(e).__name__}: {e}"}
        row = {"id": item["id"], "result": result, "evaluation": evaluation}
        (out / f"{item['id']}.json").write_text(json.dumps(row, ensure_ascii=False, indent=1), encoding="utf-8")
        s = evaluation.get("score")
        print(f"  {item['id']}: " + (f"olgu {s['facts']:g}/{s['facts_total']}, yanlış {s['wrong']}" if s
                                      else evaluation.get("error", "?")), flush=True)
        return row

    rows = await asyncio.gather(*(one(i) for i in chosen))
    _write(out, list(rows), items, chat.settings.model)
    return out


async def rejudge(client, library, folder: Path) -> None:
    items = {i["id"]: i for i in load_set()}
    rows = []
    for path in sorted(folder.glob("*.json")):
        if path.name == "sonuc.json":
            continue
        row = json.loads(path.read_text(encoding="utf-8"))
        if row["id"] in items:
            row["evaluation"] = await evaluate(client, library, items[row["id"]], row["result"])
            path.write_text(json.dumps(row, ensure_ascii=False, indent=1), encoding="utf-8")
            rows.append(row)
    _write(folder, rows, items, folder.name)


def _write(out: Path, rows: list[dict], items: dict, title: str) -> None:
    rows.sort(key=lambda r: list(items).index(r["id"]))
    (out / "sonuc.json").write_text(json.dumps({"rows": [{"id": r["id"], "evaluation": r["evaluation"]} for r in rows]},
                                               ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "rapor.md").write_text(report(rows, items, title), encoding="utf-8")
    print(out / "rapor.md")


def compare(a: Path, b: Path) -> str:
    ta, tb = totals(a), totals(b)
    lines = [f"| Madde | {a.name} | {b.name} |", "|---|---|---|"]
    for key in [k for k in ta if k in tb]:
        fmt = lambda s: f"olgu {s['facts']:g}/{s['facts_total']}, yanlış {s['wrong']}, okuma {s['must_read']}/{s['must_read_total']}" if s else "—"
        lines.append(f"| {key} | {fmt(ta[key])} | {fmt(tb[key])} |")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> None:
    from risale_mcp.env import load_env
    load_env()
    parser = argparse.ArgumentParser(prog="okuma_olc")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("run")
    p.add_argument("names", nargs="*")
    p.add_argument("--paralel", type=int, default=4)
    p = sub.add_parser("hakem")
    p.add_argument("folder", type=Path)
    p = sub.add_parser("karsilastir")
    p.add_argument("a", type=Path)
    p.add_argument("b", type=Path)
    args = parser.parse_args(argv)
    from risale_mcp.sohbet import Chat, Config, Settings, _client, _library
    if args.command == "run":
        asyncio.run(run(Chat(_library(), _client(), Config.from_env(), Settings.from_env()), _client(), args.names,
                        args.paralel))
    elif args.command == "hakem":
        asyncio.run(rejudge(_client(), _library(), args.folder))
    else:
        print(compare(args.a, args.b))


if __name__ == "__main__":
    main()
