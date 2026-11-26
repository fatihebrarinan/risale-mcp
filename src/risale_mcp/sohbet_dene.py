"""S13.11: sohbetin hata ayıklama turları (kullanıcının kararı, 2026-11-26).

Konuşmaları yerelde, sohbet servisinin kendi koduyla (`sohbet.Chat`: aynı talimat, araçlar, model, düzeltme) sorar;
canlı sohbete gitmez, denemenin sayılarına karışmaz. `sor`dan farkı: bir konuşmanın soruları sırayla aynı geçmişle
sorulur (takip soruları sayfadaki gibi: geçmişe modelin düzeltilmiş ham cevabı ve sayfa notu girer) ve her turun
bütün araç çağrıları sonuçlarıyla birlikte yazılır, yani modelin gördüğü her şey.

Soru dosyası düz metindir: `## ad` bir konuşma açar (`## ad [kip: tarama]`: konuşmanın ilk sorusunun kipi, S13.12;
sayfadaki gibi takip soruları serbesttir, S13.13; yoksa serbest soru; `[kütüphane: tefsir,hadis]`: konuşmanın her
sorusunda açık öbür kütüphaneler, S13.17, sayfadaki seçim gibi), altındaki her dolu satır bir sorudur, `#` ile başlayan öbür satırlar açıklamadır (sorulmaz). Konuşmalar aynı
anda sorulur (`--paralel`).

    uv run --extra sohbet python -m risale_mcp.sohbet dene tests/golden/sohbet_konusmalar/tur-01.txt [ad …]
    SOHBET_MODEL=claude-sonnet-5-5 uv run --extra sohbet python -m risale_mcp.sohbet dene …   # model karşılaştırması

Döküm `data/interim/sohbet/dene/<zaman>-<model>-<dosya>/`: `<ad>.json` (her tur: soru, çağrılar ve sonuçları,
modelin ham cevabı, okuyucunun gördüğü cevap, Kaynaklar, denetim sayıları, maliyet) ve okumak için `ozet.md`.
"""

import asyncio
import json
import re
import time
from datetime import datetime
from pathlib import Path

from risale_mcp.paths import DATA_DIR

OUT_DIR = DATA_DIR / "interim" / "sohbet" / "dene"
RESULT_PREVIEW = 400          # özetteki araç sonucunun uzunluğu (tamamı JSON'da)


def load(path: Path) -> list[dict]:
    """Soru dosyası -> [{ad, sorular}]."""
    out: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("## "):
            head = line[3:].strip()
            tags = dict(re.findall(r"\[(kip|kütüphane):\s*([\w,-]+)\]", head))
            name = re.sub(r"\s*\[(?:kip|kütüphane):[^\]]*\]", "", head).strip()
            out.append({"ad": name, "kip": tags.get("kip"),
                        "kutuphaneler": [k for k in tags.get("kütüphane", "").split(",") if k], "sorular": []})
        elif not line or line.startswith("#"):
            continue
        elif not out:
            raise SystemExit(f"{path}: ilk sorudan önce '## ad' satırı yok")
        else:
            out[-1]["sorular"].append(line)
    names = [c["ad"] for c in out]
    if len(set(names)) != len(names):
        raise SystemExit(f"{path}: aynı adlı konuşmalar var")
    return [c for c in out if c["sorular"]]


async def converse(chat, conversation: dict) -> dict:
    from risale_mcp.sohbet import Tally
    history, turns = [], []
    for i, question in enumerate(conversation["sorular"]):
        tally, start, done, error = Tally(), time.time(), None, None
        mode = conversation.get("kip") if i == 0 else None        # S13.13: sayfa tarama cevabından sonra serbeste döner
        try:
            async for event, data in chat.ask(history, question, tally, mode, conversation.get("kutuphaneler") or ()):
                if event == "done":
                    done = data
                elif event == "error":
                    error = data["message"]
        except Exception as e:          # Refusal ya da API hatası: konuşma burada biter
            error = f"{type(e).__name__}: {e}"
        turns.append({
            "question": question, "seconds": round(time.time() - start, 1), "error": error,
            "calls": [{"tool": name, "input": args, "result": result, "is_error": is_error}
                      for name, args, result, is_error in tally.calls],
            "model_text": tally.model_text,
            "markdown": done and done["markdown"], "raw": done and done["raw"], "sources": done and done["sources"],
            "checks": done and done["checks"],
            "usage": {"cost": round(tally.cost, 5), "rounds": tally.rounds, "tools": tally.tools,
                      "input": tally.input, "output": tally.output}})
        if done is None:
            break
        history.append({"q": question, "a": done["raw"], "r": done["reads"]})
    return {"ad": conversation["ad"], "kip": conversation.get("kip"),
            "kutuphaneler": conversation.get("kutuphaneler") or [], "turns": turns}


def summary(results: list[dict], model: str, source: Path) -> str:
    lines = [f"# Sohbet denemesi: {source.name}", "", f"Model `{model}`, {datetime.now():%Y-%m-%d %H.%M}.", ""]
    total = sum(t["usage"]["cost"] for r in results for t in r["turns"])
    lines += [f"Toplam ≈{total:.3f} $, {sum(len(r['turns']) for r in results)} cevap.", ""]
    for r in results:
        lines += [f"## {r['ad']}" + (f" [kip: {r['kip']}]" if r.get("kip") else ""), ""]
        for i, t in enumerate(r["turns"], 1):
            u = t["usage"]
            lines += [f"### {i}. {t['question']}", "",
                      f"{u['tools']} araç, {u['rounds']} tur, ≈{u['cost']:.4f} $, {t['seconds']} sn; "
                      f"denetim {json.dumps(t['checks'], ensure_ascii=False)}", ""]
            if t["error"]:
                lines += [f"**HATA:** {t['error']}", ""]
            for c in t["calls"]:
                shown = ", ".join(f"{k}={v!r}" for k, v in (c["input"] or {}).items())
                preview = re.sub(r"\s+", " ", c["result"] or "")[:RESULT_PREVIEW]
                lines.append(f"- `{c['tool']}({shown})`{' **hata**' if c['is_error'] else ''} → {preview}")
            lines += ["", "**Cevap (okuyucunun gördüğü):**", "", t["markdown"] or "—", "", "**Kaynaklar:**", ""]
            for s in t["sources"] or []:
                flag = "  ⚠ " + s["problem"] if s.get("problem") else ""
                lines.append(f"- [{s['n']}] `{s['id']}` {s.get('cite_as') or ''}{flag}")
                lines += [f"  - {e['line']}" for e in s.get("embedded", ())]
            if t["model_text"] and t["raw"] and t["model_text"].strip() != t["raw"].strip():
                lines += ["", "<details><summary>Modelin düzeltilmemiş cevabı</summary>", "", t["model_text"], "",
                          "</details>"]
            lines.append("")
    return "\n".join(lines)


async def run(chat, source: Path, names: list[str], parallel: int = 4) -> Path:
    conversations = load(source)
    if names:
        unknown = set(names) - {c["ad"] for c in conversations}
        if unknown:
            raise SystemExit(f"bilinmeyen konuşma: {', '.join(sorted(unknown))}")
        conversations = [c for c in conversations if c["ad"] in names]
    out = OUT_DIR / f"{datetime.now():%Y%m%d-%H%M%S}-{chat.settings.model}-{source.stem}"
    out.mkdir(parents=True)
    gate = asyncio.Semaphore(parallel)

    async def one(conversation):
        async with gate:
            result = await converse(chat, conversation)
        (out / f"{result['ad']}.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
        cost = sum(t["usage"]["cost"] for t in result["turns"])
        print(f"  {result['ad']}: {len(result['turns'])} cevap, ≈{cost:.4f} $", flush=True)
        return result

    results = await asyncio.gather(*(one(c) for c in conversations))
    (out / "ozet.md").write_text(summary(list(results), chat.settings.model, source), encoding="utf-8")
    print(out)
    return out
