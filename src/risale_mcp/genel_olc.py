"""S14.3: genel soru setinin raporu (`sohbet olc --set tests/golden/genel_sorular.json`).

Altın soruların raporu (`golden.report`) Risale'nin atıflarını denetler; genel setin cevapları tefsir, hadis ve klasik
kütüphanelerden de alıntı yapar. Alıntıların doğruluğunu sohbet zaten denetler (her kütüphanenin `cite`'ı; tutmayan
"doğrulanamadı" olur). Bu rapor yalnız şunları sayar, gerisi elle okunur:

- açık kütüphaneler, kütüphane başına araç çağrısı ve kaynak, doğrulanamayan kaynak;
- beklenen yerler (`core`, set dondurulurken araçlarla okunarak doğrulandı): okundu mu (bir okuma çağrısının
  girdisinde ya da sonucunda geçti mi), kaynakçaya girdi mi;
- kaynakların kütüphane sırası (K2: varsa âyet ve hadis önce, sonra açıklayanlar; sıranın doğruluğu elle okunur);
- maliyet, süre, tur.

Dökümler `measure`'ın yazdığı `<soru>.jsonl`'dır (golden biçimi; sonuç kaydında `sohbet.sources`, `sohbet.libraries`).
"""

import json
import re
from pathlib import Path

PREFIXES = ("tefsir", "hadis", "klasik")
READ_TOOLS = ("read_section", "get_passage", "get_hadith", "read_chapter", "get_ayah", "find_ayah")


def tool_library(name: str) -> str:
    head = name.split("_", 1)[0]
    return head if head in PREFIXES else "risale"


def tool_name(name: str) -> str:
    """`tefsir_read_section` -> `read_section`; Risale'nin araçları öneksizdir (`read_section`)."""
    return name.split("_", 1)[1] if tool_library(name) != "risale" else name


def bare(ident: str) -> str:
    """`tefsir:ibnkesir/2/255/c001..c004` -> `ibnkesir/2/255/c001`"""
    ident = ident.split(":", 1)[1] if ident.split(":", 1)[0] in PREFIXES else ident
    return ident.split("..", 1)[0]


def _related(a: str, b: str) -> bool:
    """Aynı yer mi: biri öbürünün öneki (bölüm ve içindeki cümle)."""
    a, b = bare(a), bare(b)
    return a == b or a.startswith(b + "/") or b.startswith(a + "/")


def _ayah(core_id: str) -> tuple[int, int, int] | None:
    m = re.fullmatch(r"(\d+):(\d+)(?:[-–](\d+))?", core_id)
    return (int(m[1]), int(m[2]), int(m[3] or m[2])) if m else None


def load(path: Path) -> dict:
    calls, results, final = [], {}, {}
    for line in path.read_text(encoding="utf-8").splitlines():
        x = json.loads(line)
        if x["type"] == "assistant":
            for c in x["message"]["content"]:
                if c.get("type") == "tool_use":
                    calls.append({"id": c["id"], "name": c["name"], "input": c["input"]})
        elif x["type"] == "user":
            for c in x["message"]["content"]:
                if c.get("type") == "tool_result":
                    results[c["tool_use_id"]] = str(c.get("content", ""))
        elif x["type"] == "result":
            final = x
    for c in calls:
        c["result"] = results.get(c["id"], "")
    return {"calls": calls, "final": final}


def core_status(place: dict, calls: list[dict], sources: list[dict]) -> tuple[bool, bool]:
    """(okundu mu, kaynakçada mı)"""
    lib, ident = place["library"], place["id"]
    if lib == "kuran":
        span = _ayah(ident)
        if not span:
            return False, False
        read = False
        for c in calls:
            a = c["input"]
            try:
                sura, ayah = int(a.get("sura")), int(a.get("ayah") or 0)
            except (TypeError, ValueError):
                continue
            end = int(a.get("end") or ayah)
            if sura == span[0] and (ayah == 0 or (ayah <= span[2] and end >= span[1])):
                read = True
        return read, False
    read = any(tool_name(c["name"]) in READ_TOOLS and tool_library(c["name"]) == lib
               and any(_related(ident, v) for v in _ids_in(c)) for c in calls)
    cited = any((s.get("library") or "risale") == lib and _related(ident, s["id"]) for s in sources)
    return read, cited


def _ids_in(call: dict) -> list[str]:
    vals = [v for v in call["input"].values() if isinstance(v, str)]
    vals += re.findall(r'"(?:id|section)":\s*"([^"]+)"', call["result"])[:200]
    return vals


def order(sources: list[dict]) -> str:
    seq = []
    for s in sources:
        lib = s.get("library") or "risale"
        if not seq or seq[-1] != lib:
            seq.append(lib)
    return " → ".join(seq) or "—"


def report(run_dir: Path, question_set: Path) -> Path:
    questions = {q["id"]: q for q in json.loads(question_set.read_text(encoding="utf-8"))["questions"]}
    rows, details, total = [], [], {"cost": 0.0, "sec": 0.0, "core": 0, "read": 0, "cited": 0, "unv": 0, "n": 0}
    for qid, q in questions.items():
        path = run_dir / f"{qid}.jsonl"
        if not path.exists():
            continue
        d = load(path)
        fin, so = d["final"], d["final"].get("sohbet", {})
        sources = so.get("sources") or []
        per_lib: dict[str, int] = {}
        for c in d["calls"]:
            per_lib[tool_library(c["name"])] = per_lib.get(tool_library(c["name"]), 0) + 1
        src_lib: dict[str, int] = {}
        for s in sources:
            src_lib[s.get("library") or "risale"] = src_lib.get(s.get("library") or "risale", 0) + 1
        core = (q.get("places") or {}).get("core", [])
        st = [core_status(p, d["calls"], sources) for p in core]
        nread, ncited = sum(r for r, _ in st), sum(c for _, c in st)
        unv = sum(1 for s in sources if s.get("unverified"))
        cost, sec = fin.get("total_cost_usd", 0.0), fin.get("duration_ms", 0) / 1000
        total["cost"] += cost; total["sec"] += sec; total["n"] += 1
        total["core"] += len(core); total["read"] += nread; total["cited"] += ncited; total["unv"] += unv
        fmt = lambda m: ", ".join(f"{k} {v}" for k, v in sorted(m.items())) or "—"
        rows.append(f"| {qid} | {q['category']} | {fmt(per_lib)} | {fmt(src_lib)} | {unv} | {nread}/{len(core)} | "
                    f"{ncited}/{len(core)} | {order(sources)} | {cost:.3f} | {sec:.0f} |"
                    + (" HATA" if so.get("failure") else ""))
        lines = [f"## {qid}. {q['question']}", "", f"*Tür:* {q['category']} · *Beklenen davranış:* {q.get('behaviour', '')}",
                 f"*Açık kütüphaneler:* {', '.join(so.get('libraries') or []) or 'yalnız Risale'}", "",
                 "Beklenen yerler:"]
        for p, (r, c) in zip(core, st):
            lines.append(f"- {'✓' if r else '·'} okundu {'✓' if c else '·'} kaynakçada — {p['library']} `{p['id']}` "
                         f"{p.get('ref', '')}")
        if so.get("failure"):
            lines += ["", f"**HATA:** {so['failure']}"]
        lines += ["", "Cevap:", "", fin.get("result", "").strip() or "(cevap yok)", ""]
        details.append("\n".join(lines))
    n = max(total["n"], 1)
    head = [f"# Genel set ölçümü: {run_dir.name}", "",
            f"Set: `{question_set}` · {total['n']} soru · toplam {total['cost']:.2f} $ (soru başı "
            f"{total['cost'] / n:.3f} $) · ortalama {total['sec'] / n:.0f} sn · beklenen yerlerin "
            f"{total['read']}/{total['core']}'i okundu, {total['cited']}/{total['core']}'i kaynakçada · "
            f"doğrulanamayan kaynak {total['unv']}", "",
            "Sütunlar: araç çağrısı ve kaynak kütüphane başına; *okundu* ve *kaynakçada* beklenen yerlerden (Kur'ân "
            "yerleri yalnız okunur, kaynakçaya girmez); *sıra* kaynakların kütüphane sırası.", "",
            "| Soru | Tür | Araç | Kaynak | Doğrulanamayan | Okundu | Kaynakçada | Sıra | $ | sn |",
            "|---|---|---|---|---:|---:|---:|---|---:|---:|"]
    out = run_dir / "genel-rapor.md"
    out.write_text("\n".join(head + rows) + "\n\n" + "\n\n".join(details) + "\n", encoding="utf-8")
    return out
