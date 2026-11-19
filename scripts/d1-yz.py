"""D7 yapay zekâ karşılaştırıcısı (PLANLAR.md D7): taslakları İşârât'ın gizlenen metniyle eşleştiren iki kör okuyucu.

    uv run python scripts/d1-yz.py envanter 11-12 [--model fable] [--denetci opus]   # D7.2 cevap anahtarı
    uv run python scripts/d1-yz.py eslestir 11-12 [--taslak 1 2 3] [--modeller fable opus] [--paralel 3]   # D7.3
    uv run python scripts/d1-yz.py rapor 11-12       # D7.4 denetim ve birleştirme, D7.5 rapor
    uv run python scripts/d1-prova.py okuma          # D7.6: sonuç varsa data/d1/okuma-yz.html de yazılır

İstem `docs/d1/karsilastirma-istemi.md` (sürümlü). Model istemi `claude -p` ile proje dışında, yerleşik araçlar, web ve
eklentiler kapalı alır: girdilerin hepsi istemdedir. Gizlenen metnin cümleleri istemde `a001` (Arapça asıl, veritabanında
`c001`) ve `t001` (tercüme) diye anılır; taslağın paragrafları okuma sayfasının çapalarıyla (`V3/ar/5`).

Çıktılar kapalı depoda (`data/d1/provalar/<birim>/yz/`): her çağrının dökümü (`.jsonl`), meta kaydı (`.meta.json`),
ayrıştırılmış cevabı (`.json`); `envanter.json` birleşmiş cevap anahtarı, `envanter.md` okunur hâli, `sonuc.json`
denetlenmiş ve birleşmiş eşleştirme (okuma sayfası onu okur). Rapor `provalar/<birim>/yz-karsilastirma.md`.

Kurallar (kullanıcı onayladı, 2026-11-13): karşılaştırıcı eşleştirir, hüküm vermez; envanteri bir model çıkarır,
öbürü metne bakarak denetler (`eksik` önerileri eklenir, öbür öneriler kullanıcıya listelenir); eşleştirmede iki model
birbirini görmez; alıntılar kendi metninde aranır (hareke ve noktalama yok sayılarak), bulunmayan satır silinmez,
`denetimsiz` işaretlenir.
"""

import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

from risale_mcp.normalize import search_words
from risale_mcp.paths import ROOT

_spec = importlib.util.spec_from_file_location("d1_prova", ROOT / "scripts" / "d1-prova.py")
P = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P)

PROMPT = ROOT / "docs" / "d1" / "karsilastirma-istemi.md"
MODELS = {"fable": "claude-fable-5-2", "opus": "claude-opus-5-5", "sonnet": "claude-sonnet-5-5"}
EFFORT = "high"
TIMEOUT = 60 * 60
DURUM = ("aynen", "kismen", "farkli_gerekce", "yok")
DURUM_TR = {"aynen": "aynen", "kismen": "kısmen", "farkli_gerekce": "farklı gerekçe", "yok": "yok"}
SIMGE = {"aynen": "✓", "kismen": "◐", "farkli_gerekce": "↔", "yok": "·", None: "?"}
FOUND = ("aynen", "kismen")


def out_dir(unit: str) -> Path:
    d = P.DRAFTS / unit / "yz"
    d.mkdir(parents=True, exist_ok=True)
    return d


# ---------------------------------------------------------------- istem

def prompt_parts() -> tuple[dict[str, str], str]:
    raw = PROMPT.read_text(encoding="utf-8")
    parts = dict(re.findall(r"^---- (\w+) ----\n(.*?)(?=^---- \w+ ----|\Z)", raw, flags=re.M | re.S))
    return parts, P._sha(raw)


def hidden(unit: str) -> dict[str, list[tuple[str, str, str]]]:
    """Gizlenen metin: {'ar'|'tr': [(istem kimliği, veritabanı kimliği, metin, paragraf)]}; `son`dan öncesi."""
    cfg = P.UNITS[unit]
    out = {}
    for work, lang in (("isaratul-icaz-arabi", "ar"), ("isaratul-icaz", "tr")):
        stop = cfg["sections"][work].get("son")
        rows = []
        for sid, pid, text, local in P.unit_sentences(cfg, work):
            if local == stop:
                break
            rows.append((local, sid, text, pid))
        p = "a" if lang == "ar" else "t"
        if any("/" in r[0] for r in rows):    # alt bölümlü birim (31–33): istem kimliği sırayla
            out[lang] = [(f"{p}{k:03d}", sid, text, pid) for k, (_, sid, text, pid) in enumerate(rows, 1)]
        else:                                  # tek bölüm (11–12): c004 -> a004, eski kimlikler korunur
            out[lang] = [(f"{p}{local[1:]}", sid, text, pid) for local, sid, text, pid in rows]
    return out


def render_hidden(rows: list) -> str:
    paras, last = [], None
    for pid_short, _, text, pid in rows:
        if pid != last:
            paras.append([])
            last = pid
        paras[-1].append(f"[{pid_short}] {text}")
    return "\n\n".join(" ".join(p) for p in paras)


def draft_blocks(unit: str, n: int) -> tuple[list[tuple[str, str, bool, str]], dict]:
    """Taslağın paragrafları [(çapa, dil, alıntı mı, metin)] okuma sayfasının sırasıyla ve kaynakçası."""
    raw = (P.DRAFTS / unit / f"taslak-{n}.md").read_text(encoding="utf-8")
    sections, sources = P.parse_draft(raw)
    blocks = []
    for key, items in sections.items():
        if key not in P.SECTION_TITLES:
            continue
        count = Counter()
        for lang, kind, text in items:
            blocks.append((f"{key}/{lang}/{count[lang]}", lang, kind == "quote", text))
            count[lang] += 1
    return blocks, sources


def pairs(blocks: list) -> dict[str, str]:
    """Paragrafın eşi, iki yönde: Arapça paragraf ↔ Türkçesi, Arapça alıntı ↔ tercümesi.

    Çapalar dil başına ayrı sayılır; `/ar/k` ile `/tr/k` her zaman eş değildir: Türkçesi olmayan Arapça alıntı ya da
    Arapçası olmayan Türkçe alıntı (Risale'den) sırayı kaydırır (9–10 taslak 2'de hemen her paragraf; 2026-11-17'ye
    kadar masa ve denetimler sıra numarasıyla eşliyordu). Eş paragraf sırasından bulunur: tercüme alıntısının eşi hemen
    önündeki Arapça alıntı; paragraf tercümesi aradaki alıntılardan sonra da gelebilir (`quote_tr_is_paragraph`), eşi
    bölümdeki eşsiz son Arapça paragraftır. Eşi olmayan çapa sözlükte yoktur.
    """
    out: dict[str, str] = {}
    sec, open_ar, prev = None, [], None
    for a, lang, quote, _ in blocks:
        s = a.split("/")[0]
        if s != sec:
            sec, open_ar, prev = s, [], None
        if lang == "ar":
            if not quote:
                open_ar.append(a)
        elif quote:
            if prev and prev[1] == "ar" and prev[2] and prev[0] not in out:
                out[a], out[prev[0]] = prev[0], a
        elif open_ar:
            x = open_ar.pop()
            out[a], out[x] = x, a
        prev = (a, lang, quote)
    return out


def ar_of(pr: dict[str, str], a: str) -> str:
    """Çapanın Arapça tarafı (Türkçe çapa eşsizse kendisi)."""
    return a if "/tr/" not in a else pr.get(a, a)


def tr_of(pr: dict[str, str], a: str) -> str | None:
    """Çapanın Türkçe tarafı (yoksa None)."""
    return a if "/tr/" in a else pr.get(a)


def render_draft(blocks: list, sources: dict) -> str:
    lines, current = [], None
    for anchor, _, quote, text in blocks:
        key = anchor.split("/")[0]
        if key != current:
            lines += [f"## {P.SECTION_TITLES[key]}", ""]
            current = key
        lines += [f"[{anchor}]{' (alıntı)' if quote else ''} {text}", ""]
    lines += ["## Kaynaklar", ""] + [f"[{k}] {v}" for k, v in sources.items()]
    return "\n".join(lines)


def build_prompt(task: str, unit: str, **extra) -> tuple[str, str]:
    parts, sha = prompt_parts()
    cfg = P.UNITS[unit]
    h = hidden(unit)
    values = {"sura_name": cfg["sura_name"], "ayahs": "–".join(map(str, cfg["ayahs"])),
              "arapca": render_hidden(h["ar"]), "turkce": render_hidden(h["tr"]), **extra}
    return parts["ORTAK"].format(**values) + "\n" + parts[task].format(**values), sha


# ---------------------------------------------------------------- model çağrısı

def run_model(prompt: str, model: str, stem: Path, meta_extra: dict) -> dict | None:
    """`claude -p`, araçsız; döküm `<stem>.jsonl`, meta `<stem>.meta.json`, JSON cevap `<stem>.json`."""
    env = {k: v for k, v in os.environ.items() if k not in P.PARENT_ENV}
    command = ["claude", "-p", "--model", MODELS[model], "--effort", EFFORT, "--output-format", "stream-json",
               "--verbose", "--strict-mcp-config", "--tools", "", "--no-session-persistence"]
    started = time.monotonic()
    print(f"{stem.name}: {MODELS[model]} ({datetime.now():%H:%M})", flush=True)
    done = P.claude_p(command, prompt, stem.with_suffix(".jsonl"), env, TIMEOUT, esik=0.85, prefix="d1-yz-")
    answer, calls, cost = P.transcript(stem.with_suffix(".jsonl"))
    data = extract_json(answer)
    meta = {"model": MODELS[model], "effort": EFFORT, "seconds": round(time.monotonic() - started),
            "returncode": done.returncode, "cost_usd": cost, "at": datetime.now().isoformat(),
            "prompt_chars": len(prompt), "parsed": data is not None, **meta_extra}
    if done.stderr.strip():
        meta["stderr"] = done.stderr.strip()[-2000:]
    stem.with_suffix(".meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    if data is None:
        stem.with_suffix(".cevap.txt").write_text(answer, encoding="utf-8")
        print(f"  {stem.name}: JSON ayrıştırılamadı ({meta['seconds']} sn, çıkış {done.returncode})", flush=True)
        return None
    stem.with_suffix(".json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  {stem.name}: {meta['seconds']} sn" + (f", ≈{cost:.2f} $" if cost else ""), flush=True)
    return data


def extract_json(answer: str) -> dict | None:
    m = re.search(r"```(?:json)?\s*\n(.*?)\n```", answer, flags=re.S)
    for candidate in ([m.group(1)] if m else []) + [answer[answer.find("{"):answer.rfind("}") + 1]]:
        try:
            return json.loads(candidate)
        except (json.JSONDecodeError, ValueError):
            continue
    return None


# ---------------------------------------------------------------- alıntı denetimi

def quote_found(quote: str, text: str) -> bool:
    """Alıntı metinde mi: "…" ile bölünen her parça sırayla, kelime dizisi olarak (hareke, noktalama yok sayılır)."""
    target = search_words(text)
    pos = 0
    parts = [search_words(p) for p in re.split(r"…|\.\.\.", quote or "")]
    parts = [p for p in parts if p]
    if not parts:
        return False
    joined = " " + " ".join(target) + " "
    for part in parts:
        needle = " " + " ".join(part) + " "
        i = joined.find(needle, pos)
        if i < 0:
            return False
        pos = i + len(needle) - 1
    return True


def hidden_text(h: dict, ids: list[str]) -> str:
    index = {r[0]: r[2] for lang in h for r in h[lang]}
    return " ".join(index.get(i, "") for i in ids)


def check_item(item: dict, h: dict) -> dict:
    ids = item.get("tr") if item.get("yalniz_tercume") else item.get("ar")
    known = {r[0] for lang in h for r in h[lang]}
    bad = [i for i in (item.get("ar") or []) + (item.get("tr") or []) if i not in known]
    item["denetim"] = {"kimlik": not bad, "alinti": quote_found(item.get("alinti", ""), hidden_text(h, ids or []))}
    if bad:
        item["denetim"]["bilinmeyen"] = bad
    return item


# ---------------------------------------------------------------- D7.2 envanter

def envanter(unit: str, model: str, denetci: str) -> None:
    d = out_dir(unit)
    prompt, sha = build_prompt("ENVANTER", unit)
    raw = run_model(prompt, model, d / "envanter-ham", {"gorev": "envanter", "istem_sha": sha})
    if raw is None:
        sys.exit("envanter çıkarılamadı")
    review_prompt, _ = build_prompt("DENETIM", unit, envanter=json.dumps(raw, ensure_ascii=False, indent=1))
    review = run_model(review_prompt, denetci, d / "envanter-denetim", {"gorev": "denetim", "istem_sha": sha})
    merge_envanter(unit, raw, review or {"oneriler": []}, {"cikaran": MODELS[model], "denetci": MODELS[denetci],
                                                          "istem_sha": sha, "denetim_basarili": review is not None})


def _first_ar(item: dict, h: dict) -> int:
    order = {r[0]: i for lang in ("ar", "tr") for i, r in enumerate(h[lang])}
    keys = [order[i] for i in (item.get("ar") or []) if i in order]
    if keys:
        return min(keys)
    tr = [order[i] for i in (item.get("tr") or []) if i in order]
    # tercümede kalan kalem: Arapçadaki yerine yaklaşık (tercüme cümlesinin oranı)
    return int(min(tr) * len(h["ar"]) / max(1, len(h["tr"]))) if tr else 10 ** 6


def merge_envanter(unit: str, raw: dict, review: dict, meta: dict) -> None:
    """Çıkaranın kalemleri + denetçinin `eksik` önerileri, metin sırasıyla yeniden numaralanır; öbür öneriler açık."""
    h = hidden(unit)
    items = [dict(i, kaynak="cikaran", eski_id=i.get("id")) for i in raw.get("kalemler", [])]
    open_items = []
    # Kullanıcının kabul ettiği öbür öneriler (`envanter-kararlar.json`: [{tur, ilgili}], ilgili çıkaranın kimlikleri):
    # `bol` kalemi önerinin kalemleriyle değiştirir, `sil` kalemi çıkarır. Eşleştirmeden önce verilir (2026-11-15).
    kp = out_dir(unit) / "envanter-kararlar.json"
    accepted = json.loads(kp.read_text(encoding="utf-8"))["kabul"] if kp.exists() else []
    is_accepted = lambda o: any(k["tur"] == o.get("tur") and k["ilgili"] == o.get("ilgili") for k in accepted)
    applied = []
    for o in review.get("oneriler", []):
        if o.get("tur") == "eksik" and isinstance(o.get("oneri"), dict):
            items.append(dict(o["oneri"], kaynak="denetci", gerekce_denetci=o.get("gerekce", "")))
        elif o.get("tur") in ("bol", "sil") and is_accepted(o):
            gone = set(o.get("ilgili") or [])
            items = [i for i in items if i.get("eski_id") not in gone]
            if o["tur"] == "bol":
                items += [dict(x, kaynak="denetci", eski_id=None, bolunen=sorted(gone), gerekce_denetci=o.get("gerekce", ""))
                          for x in o.get("oneri") or []]
            applied.append(o)
        else:
            open_items.append(o)
    items.sort(key=lambda i: (_first_ar(i, h), 0 if i["kaynak"] == "cikaran" else 1))
    renum = {}
    for n, item in enumerate(items, 1):
        new = f"N{n:02d}"
        if item.get("eski_id"):
            renum[item["eski_id"]] = new
        item["id"] = new
        check_item(item, h)
    for o in open_items:
        o["ilgili"] = [renum.get(i, i) for i in o.get("ilgili") or []]
    out = {"birim": unit, "surum": 1, "at": datetime.now().isoformat(), **meta, "kalemler": items,
           "acik_oneriler": open_items, "uygulanan_oneriler": applied}
    d = out_dir(unit)
    (d / "envanter.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    (d / "envanter.md").write_text(envanter_md(unit, out, h), encoding="utf-8")
    bad = sum(1 for i in items if not all(i["denetim"].values()))
    print(f"envanter: {len(items)} kalem ({sum(i['kaynak'] == 'denetci' for i in items)} denetçiden), "
          f"{len(open_items)} açık öneri, {bad} denetimsiz → {(d / 'envanter.md').relative_to(ROOT)}")


def _ids_db(h: dict, ids: list[str]) -> str:
    index = {r[0]: r[1] for lang in h for r in h[lang]}
    return ", ".join(f"`{index[i].rsplit('/', 1)[-1]}`{' (tr)' if i.startswith('t') else ''}" for i in ids if i in index)


def envanter_md(unit: str, env: dict, h: dict) -> str:
    cfg = P.UNITS[unit]
    lines = [f"# Prova {unit}: İşârât'ın nükte envanteri (D7.2)", "",
             "Yapay zekâ çıkarımıdır; cevap anahtarı olarak kullanılır, İşârât'ın kendisi değildir. "
             f"`uv run python scripts/d1-yz.py envanter {unit}` üretir; düzeltme `envanter.json`'da yapılır.", "",
             f"Çıkaran {env['cikaran']}, denetleyen {env['denetci']}; istem `{env['istem_sha']}`; "
             f"{len(env['kalemler'])} kalem. Kimlikler: Arapça asılda `c…`, tercümede `c… (tr)` "
             f"({cfg['nodes'][1]}, {cfg['nodes'][0]}).", ""]
    counts = Counter(i.get("vecih") for i in env["kalemler"])
    lines += ["| Vecih | Kalem |", "|---|---:|"] + [f"| {k} | {v} |" for k, v in sorted(counts.items(), key=str)] + [""]
    for item in env["kalemler"]:
        flags = []
        if item["kaynak"] == "denetci":
            flags.append("denetçinin eklediği")
        if item.get("yalniz_tercume"):
            flags.append("yalnız tercümede")
        if not all(item["denetim"].values()):
            flags.append("**denetimsiz**: " + ", ".join(k for k, v in item["denetim"].items() if v is False))
        lines += [f"**{item['id']}** · {item.get('vecih', '?')} · {item.get('lafiz', '')}"
                  + (f" · _{'; '.join(flags)}_" if flags else ""), "",
                  f"{item.get('nukte', '')}", "", f"> {item.get('alinti', '')}", "",
                  f"Yeri: {_ids_db(h, (item.get('ar') or []) + (item.get('tr') or []))}"
                  + (f"  \nDenetçi: {item['gerekce_denetci']}" if item.get("gerekce_denetci") else ""), ""]
    if env["acik_oneriler"]:
        lines += ["## Denetçinin açık önerileri", "",
                  "Uygulanmadı; kullanıcının kararını bekler. Uygulanırsa eşleştirme yeniden çalıştırılır.", ""]
        for o in env["acik_oneriler"]:
            prop = o.get("oneri")
            if isinstance(prop, list):
                prop = " / ".join(p.get("nukte", "") for p in prop if isinstance(p, dict))
            elif isinstance(prop, dict):
                prop = prop.get("nukte", "")
            lines += [f"- **{o.get('tur')}** {', '.join(o.get('ilgili') or [])}: {o.get('gerekce', '')}"
                      + (f"  \n  Öneri: {prop}" if prop else "")]
    return "\n".join(lines).rstrip() + "\n"


# ---------------------------------------------------------------- D7.3 eşleştirme

def drafts_of(unit: str) -> list[int]:
    return sorted(int(m.group(1)) for p in (P.DRAFTS / unit).glob("taslak-*.md")
                  if (m := re.fullmatch(r"taslak-(\d+)", p.stem)))


def env_for_prompt(env: dict) -> str:
    keep = ("id", "vecih", "lafiz", "nukte", "ar", "tr", "alinti")
    return json.dumps({"kalemler": [{k: i.get(k) for k in keep} for i in env["kalemler"]]}, ensure_ascii=False,
                      indent=1)


def eslestir(unit: str, drafts: list[int], models: list[str], parallel: int, again: bool) -> None:
    d = out_dir(unit)
    env = json.loads((d / "envanter.json").read_text(encoding="utf-8"))
    jobs = []
    for n in drafts:
        blocks, sources = draft_blocks(unit, n)
        prompt, sha = build_prompt("ESLESTIRME", unit, envanter=env_for_prompt(env),
                                   taslak=render_draft(blocks, sources))
        for m in models:
            stem = d / f"eslestirme-taslak-{n}-{m}"
            if stem.with_suffix(".json").exists() and not again:
                print(f"{stem.name}: var (yeniden için --yeniden)")
                continue
            jobs.append((prompt, m, stem, {"gorev": "eslestirme", "taslak": n, "istem_sha": sha,
                                           "envanter_at": env["at"]}))
    with ThreadPoolExecutor(max_workers=parallel) as pool:
        list(pool.map(lambda j: run_model(*j), jobs))


# ---------------------------------------------------------------- D7.4 denetim ve birleştirme

def check_match(result: dict, env: dict, blocks: list) -> dict:
    texts = {a: t for a, _, _, t in blocks}
    known = {i["id"] for i in env["kalemler"]}
    by_id = {}
    for r in result.get("nukteler", []):
        if r.get("id") in known and r.get("id") not in by_id:
            r["durum"] = r.get("durum") if r.get("durum") in DURUM else None
            anchors = r.get("taslak") or []
            r["denetim"] = {"capa": all(a in texts for a in anchors),
                            "alinti": r["durum"] == "yok" or quote_found(r.get("alinti", ""),
                                                                        " ".join(texts.get(a, "") for a in anchors))}
            by_id[r["id"]] = r
    extras = []
    for f in result.get("fazla", []):
        anchors = f.get("taslak") or []
        f["denetim"] = {"capa": bool(anchors) and all(a in texts for a in anchors),
                        "alinti": quote_found(f.get("alinti", ""), " ".join(texts.get(a, "") for a in anchors))}
        if f.get("celiski") and f["celiski"] not in known:
            f["celiski_bilinmeyen"] = f["celiski"]
            f["celiski"] = None
        extras.append(f)
    return {"nukteler": by_id, "fazla": extras, "eksik_kalem": sorted(known - set(by_id))}


def merge_extras(per_model: dict[str, list], pr: dict[str, str] | None = None) -> list[dict]:
    """İki modelin fazlaları: Arapça çapası örtüşenler bir kayıtta (`okuyucular` ikisi), öbürleri tek okuyuculu."""
    models = list(per_model)
    merged = [dict(f, okuyucular=[models[0]], es={}) for f in per_model.get(models[0], [])]
    for m in models[1:]:
        for f in per_model[m]:
            mine = {ar_of(pr or {}, a) for a in f.get("taslak") or []}
            hit = next((g for g in merged if m not in g["okuyucular"]
                        and mine & {ar_of(pr or {}, a) for a in g.get("taslak") or []}), None)
            if hit:
                hit["okuyucular"].append(m)
                hit["es"][m] = {k: f.get(k) for k in ("iddia", "isaret", "celiski", "gerekce", "alinti", "taslak")}
            else:
                merged.append(dict(f, okuyucular=[m], es={}))
    merged.sort(key=lambda g: _anchor_order(g.get("taslak") or []))
    return merged


SECTION_ORDER = list(P.SECTION_TITLES)


def _anchor_order(anchors: list[str]) -> tuple:
    keys = []
    for a in anchors:
        parts = a.split("/")
        if len(parts) == 3 and parts[0] in SECTION_ORDER and parts[2].isdigit():
            keys.append((SECTION_ORDER.index(parts[0]), int(parts[2])))
    return min(keys) if keys else (99, 0)


def sonuc(unit: str) -> dict:
    d = out_dir(unit)
    env = json.loads((d / "envanter.json").read_text(encoding="utf-8"))
    out = {"birim": unit, "at": datetime.now().isoformat(), "envanter": env, "taslaklar": {}}
    for n in drafts_of(unit):
        blocks, _ = draft_blocks(unit, n)
        per = {}
        for path in sorted(d.glob(f"eslestirme-taslak-{n}-*.json")):
            if path.name.endswith(".meta.json"):
                continue
            model = path.stem.removeprefix(f"eslestirme-taslak-{n}-")
            meta = json.loads(path.with_name(path.stem + ".meta.json").read_text())
            per[model] = dict(check_match(json.loads(path.read_text(encoding="utf-8")), env, blocks),
                              meta={k: meta.get(k) for k in ("model", "seconds", "cost_usd", "istem_sha", "at")})
        if not per:
            continue
        rows = []
        for item in env["kalemler"]:
            states = {m: per[m]["nukteler"].get(item["id"], {}).get("durum") for m in per}
            vals = set(states.values())
            uyum = ("tek" if len(per) < 2 else "ayni" if len(vals) == 1 else
                    "yakin" if vals <= set(FOUND) else "ayrilik")
            rows.append({"id": item["id"], "durum": states, "uyum": uyum})
        extras = merge_extras({m: per[m]["fazla"] for m in per}, pairs(blocks))
        for f in extras:   # sınama işaretlerinin anahtarı: taslak, çapa ve iddiadan (yeniden üretimde sabit)
            f["k"] = hashlib.sha1(f"{n}|{','.join(f.get('taslak') or [])}|{f.get('iddia', '')}".encode()).hexdigest()[:10]
        out["taslaklar"][f"taslak-{n}"] = {"modeller": per, "satirlar": rows, "fazla": extras}
    out["orneklem"] = sample_keys(out)
    (d / "sonuc.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    return out


# ---------------------------------------------------------------- D7.5 rapor

def _short(text: str, n: int = 140) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text if len(text) <= n else text[:n - 1].rstrip() + "…"


def _tr_of(blocks: dict, anchors: list[str]) -> str:
    """Çapanın Türkçe karşılığı (eşi, `pairs`), rapor için."""
    pr = blocks.get("__pairs__") or {}
    for a in anchors:
        t = blocks.get(tr_of(pr, a) or "")
        if t:
            return t
    return ""


def rapor(unit: str) -> None:
    res = sonuc(unit)
    env = res["envanter"]
    items = {i["id"]: i for i in env["kalemler"]}
    drafts = list(res["taslaklar"])
    models = sorted({m for t in res["taslaklar"].values() for m in t["modeller"]}, key=list(MODELS).index)
    N = len(items)
    L = [f"# Prova {unit}: yapay zekâ karşılaştırması (D7)", "",
         "> Yapay zekâ karşılaştırmasıdır, hüküm değildir: bir nüktenin taslakta bulunup bulunmadığını ve İşârât'la "
         "çelişip çelişmediğini söyler; fazladan söylenenin doğruluğu ehlinindir. Okuyuculara gösterilmez (D6 "
         "okumaları ondan bağımsız kalsın).", "",
         f"`uv run python scripts/d1-yz.py rapor {unit}` üretir; elle düzenlenmez. Envanter (cevap anahtarı) "
         f"`yz/envanter.md`: {N} kalem; çıkaran {env['cikaran']}, denetleyen {env['denetci']}. Okuyucular: "
         + ", ".join(f"{m} ({MODELS[m]})" for m in models) + ", birbirini görmeden. İstem `docs/d1/karsilastirma-istemi.md` "
         f"(`{env['istem_sha']}`).", "",
         "Simgeler: ✓ aynen, ◐ kısmen, ↔ farklı gerekçe (aynı lafza bakıp başka nükte), · yok; hücrede okuyucular "
         "sırasıyla (" + " / ".join(models) + ").", ""]
    # sayılar; mukaddimesi olan birimde (31–33) vecihlerin kapsaması ayrıca: taslağın mukaddime yazıp yazmaması
    # kalemlerin büyük kısmını tek başına oynatmasın (2026-11-15)
    muk = {i for i, it in items.items() if it.get("vecih") == "Mukaddime"}
    nv = N - len(muk)
    vcol = muk and nv > 0
    surum = {t: json.loads((P.DRAFTS / unit / f"{t}.json").read_text()).get("surum", "v1")
             for t in drafts if (P.DRAFTS / unit / f"{t}.json").exists()}
    L += ["## Sayılar", "", "Kapsama: envanter kalemlerinden aynen ya da kısmen bulunanların oranı. \"İkisi de\": iki "
          "okuyucunun da bulduğu dediği." + (f" \"Vecihler\": mukaddimenin {len(muk)} kalemi dışında, {nv} kalem üzerinden."
                                             if vcol else ""), "",
          "| Taslak | Okuyucu | ✓ | ◐ | ↔ | · | Kapsama |" + (" Vecihler |" if vcol else "")
          + " Fazla (kaynaklı / kendi / işaretsiz) | Çelişki | Denetimsiz |",
          "|---|---|---:|---:|---:|---:|---:|" + ("---:|" if vcol else "") + "---|---:|---:|"]
    vc = lambda hits: f" %{hits / nv * 100:.0f} |" if vcol else ""
    for t in drafts:
        tl = f"{t} ({surum[t]})" if len(set(surum.values())) > 1 else t
        tr = res["taslaklar"][t]
        for m in models:
            if m not in tr["modeller"]:
                continue
            pm = tr["modeller"][m]
            c = Counter(r.get("durum") for r in pm["nukteler"].values())
            fz = pm["fazla"]
            fc = Counter(f.get("isaret") for f in fz)
            cel = sum(1 for f in fz if f.get("celiski"))
            bad = (sum(1 for r in pm["nukteler"].values() if not all(r["denetim"].values()))
                   + sum(1 for f in fz if not all(f["denetim"].values())))
            cov = (c["aynen"] + c["kismen"]) / max(1, N)
            vhits = sum(1 for i, r in pm["nukteler"].items() if i not in muk and r.get("durum") in FOUND)
            L.append(f"| {tl} | {m} | {c['aynen']} | {c['kismen']} | {c['farkli_gerekce']} | {c['yok']} | %{cov * 100:.0f} |"
                     + vc(vhits) + f" {len(fz)} ({fc['kaynakli']} / {fc['kendi_tespiti']} / {fc['isaretsiz']}) | {cel} | {bad} |")
        if len(tr["modeller"]) < 2:      # D11: tek okuyucu (kalibrasyon); "ikisi de" satırı anlamsız
            continue
        both = sum(1 for r in tr["satirlar"] if all(r["durum"].get(m) in FOUND for m in models))
        vboth = sum(1 for r in tr["satirlar"] if r["id"] not in muk and all(r["durum"].get(m) in FOUND for m in models))
        u = Counter(r["uyum"] for r in tr["satirlar"])
        L.append(f"| {tl} | ikisi de | | | | | %{both / max(1, N) * 100:.0f} |" + vc(vboth)
                 + f" {sum(len(f['okuyucular']) > 1 for f in tr['fazla'])} ortak | | |")
        if not u.get("tek"):
            L.append(f"| | uyum | {u['ayni']} aynı, {u['yakin']} yakın (✓/◐), {u['ayrilik']} ayrılık | | | | | |"
                     + (" |" if vcol else "") + " | |")
    # nükte × taslak
    L += ["", "## Nükte × taslak", "", "| Kalem | Vecih | Lafız | Nükte | " + " | ".join(drafts) + " |",
          "|---|---|---|---|" + ":---:|" * len(drafts)]
    for iid, item in items.items():
        cells = []
        for t in drafts:
            row = next(r for r in res["taslaklar"][t]["satirlar"] if r["id"] == iid)
            cells.append(" ".join(SIMGE[row["durum"].get(m)] for m in models) + (" ⚠" if row["uyum"] == "ayrilik" else ""))
        L.append(f"| {iid} | {item.get('vecih', '')} | {_short(item.get('lafiz', ''), 40)} | {_short(item.get('nukte', ''), 110)} | "
                 + " | ".join(cells) + " |")
    none = [i for i in items if all(all(r["durum"].get(m) not in FOUND for m in models)
                                    for t in drafts for r in res["taslaklar"][t]["satirlar"] if r["id"] == i)]
    every = [i for i in items if all(all(r["durum"].get(m) in FOUND for m in models)
                                     for t in drafts for r in res["taslaklar"][t]["satirlar"] if r["id"] == i)]
    L += ["", f"⚠: iki okuyucu ayrıldı (biri buldu, öbürü bulmadı).", "",
          f"**Hiçbir taslağın yakalamadığı** (iki okuyucuya göre de): {', '.join(none) or '—'}  ",
          f"**Üç taslağın da yakaladığı** (iki okuyucuya göre de): {', '.join(every) or '—'}", ""]
    for iid in none:
        L.append(f"- **{iid}** ({items[iid].get('vecih')}, {items[iid].get('lafiz', '')}): {items[iid].get('nukte', '')}")
    # taslak başına
    for t in drafts:
        tr = res["taslaklar"][t]
        n = int(t.split("-")[1])
        bl = draft_blocks(unit, n)[0]
        blocks = {a: txt for a, _, _, txt in bl}
        blocks["__pairs__"] = pairs(bl)                 # _tr_of eşi buradan alır
        ms = [m for m in models if m in tr["modeller"]]
        L += ["", f"## {t.replace('taslak-', 'Taslak ')}", ""]
        if len(ms) < len(models):
            L += [f"_Yalnız {', '.join(ms)} okudu; öbür okuyucunun sonucu yok._", ""]
        split = [r for r in tr["satirlar"] if r["uyum"] == "ayrilik"]
        if split:
            L += ["### Okuyucuların ayrıldığı kalemler", ""]
            for r in split:
                L.append(f"- **{r['id']}** {_short(items[r['id']].get('nukte', ''), 120)}")
                for m in ms:
                    x = tr["modeller"][m]["nukteler"].get(r["id"], {})
                    L.append(f"  - {m}: {DURUM_TR.get(x.get('durum'), '?')}"
                             + (f" ({', '.join(x.get('taslak') or [])})" if x.get("taslak") else "")
                             + f": {x.get('gerekce', '')}")
            L.append("")
        conflicts = [f for f in tr["fazla"] if f.get("celiski") or any(e.get("celiski") for e in f["es"].values())]
        if conflicts:
            L += ["### İşârât'la çelişki", ""]
            for f in conflicts:
                L += _extra_lines(f, blocks, items)
            L.append("")
        L += ["### Fazla (ehline sor)", "", "Envanterde karşılığı olmayan iddialar. Doğru ya da yanlış oldukları "
              "söylenmez; \"iki okuyucu\" ikisinin de aynı paragrafta fazla bulduğu yerdir.", ""]
        for f in tr["fazla"]:
            if f in conflicts:
                continue
            L += _extra_lines(f, blocks, items)
        bad = [(m, r) for m in ms for r in list(tr["modeller"][m]["nukteler"].values()) + tr["modeller"][m]["fazla"]
               if not all(r["denetim"].values())]
        if bad:
            L += ["", "### Denetimsiz satırlar", "", "Alıntısı taslakta bulunmayan ya da çapası olmayan satırlar "
                  "(silinmedi; yukarıdaki sayılara dahil).", ""]
            for m, r in bad:
                L.append(f"- {m} · {r.get('id', 'fazla')} · {', '.join(r.get('taslak') or [])} · "
                         f"{', '.join(k for k, v in r['denetim'].items() if not v)}: «{_short(r.get('alinti', ''), 100)}»")
    L += sinama_lines(unit, res, items)
    path = P.DRAFTS / unit / "yz-karsilastirma.md"
    path.write_text("\n".join(L).rstrip() + "\n", encoding="utf-8")
    print(path.relative_to(ROOT))


def _stratum(res: dict, key: str) -> str:
    """Örneklem anahtarının katmanı (`sample_keys` ile aynı): ayrılık, çelişki, fazla ya da okuyucunun durumu."""
    draft, who, ident = key.split("|", 2)
    t = res["taslaklar"].get(draft, {})
    if who == "fazla":
        f = next((x for x in t.get("fazla", []) if x["k"] == ident), None)
        return "celiski" if f and f.get("celiski") else "fazla"
    row = next((r for r in t.get("satirlar", []) if r["id"] == ident), None)
    if not row:
        return "?"
    return "ayrilik" if row["uyum"] == "ayrilik" else row["durum"].get(who) or "?"


STRATUM_TR = {"ayrilik": "ayrılık (iki okuyucu ayrıldı)", "celiski": "çelişki", "fazla": "fazla",
              **{k: v for k, v in DURUM_TR.items()}}
MARK_TR = {"tutuyor": "tutuyor", "kismen": "kısmen", "tutmuyor": "tutmuyor"}


def _trust_table(groups: dict[str, Counter], order: list[str]) -> list[str]:
    L = ["| Satır türü | Tutuyor | Kısmen | Tutmuyor | Güven |", "|---|---:|---:|---:|---:|"]
    total = Counter()
    for kind in [k for k in order if k in groups] + sorted(k for k in groups if k not in order):
        c = groups[kind]
        total += c
        n = sum(c.values())
        L.append(f"| {STRATUM_TR.get(kind, kind)} | {c['tutuyor']} | {c['kismen']} | {c['tutmuyor']} | "
                 f"%{(c['tutuyor'] + c['kismen'] / 2) / n * 100:.0f} |")
    n = sum(total.values())
    L.append(f"| **Toplam** | {total['tutuyor']} | {total['kismen']} | {total['tutmuyor']} | "
             f"**%{(total['tutuyor'] + total['kismen'] / 2) / n * 100:.0f}** |")
    return L


def sinama_lines(unit: str, res: dict, items: dict) -> list[str]:
    """D7.7: masada (önce okuma-yz sayfasında) "metinde tutuyor / kısmen / tutmuyor" işaretleri
    (`data/d1/notlar/*.json`, `yz_sinama`; aynı anahtarda en yeni işaret). Ölçü insanla uyuşmak değil, metne bakınca
    tutmaktır (kullanıcının düzeltmesi, 2026-11-13). Güven oranı yalnız örneklemden; örneklem dışı ayrıca sayılır."""
    marks: dict[str, dict] = {}
    for f in sorted(P.NOTES_DIR.glob("*.json")) if P.NOTES_DIR.exists() else []:
        for k, v in (json.loads(f.read_text(encoding="utf-8")).get("yz_sinama") or {}).items():
            if k.startswith(unit + "|") and (k not in marks or v["at"] > marks[k]["at"]):
                marks[k] = v
    marks = {k.split("|", 1)[1]: v for k, v in marks.items()}
    sample = res.get("orneklem", [])
    inside = [k for k in sample if k in marks]
    outside = [k for k in marks if k not in set(sample)]
    L = ["", "## Sınama (D7.7)", "",
         f"Örneklem {len(sample)} satır (katmanlı, sabit tohumla; âyet masası › İşârât'la karşılaştırma › "
         f"\"Örneklem\"). İşaretli: {len(inside)}/{len(sample)} örneklemden, {len(outside)} örneklem dışından. "
         "Okuyucu satırında \"tutuyor\" okuyucunun hükmünün (aynen, kısmen, farklı gerekçe, yok) metne bakınca "
         "doğru olduğudur; fazla satırında iddianın İşârât'ın gizlenen metninde gerçekten karşılığı olmadığı, çelişki "
         "satırında çelişkinin metinde bulunduğudur. Fazlanın kendisinin doğruluğu ölçülmez (ehline sor).", ""]
    if not marks:
        return L + ["Henüz işaret yok."]
    order = ["ayrilik", "celiski", "fazla", "aynen", "kismen", "farkli_gerekce", "yok"]
    groups: dict[str, Counter] = {}
    for k in inside:
        groups.setdefault(_stratum(res, k), Counter())[marks[k]["v"]] += 1
    L += ["### Örneklem", ""] + _trust_table(groups, order)
    L += ["", "Güven: (tutuyor + kısmen/2) / işaretli satır."]
    if outside:
        out_groups: dict[str, Counter] = {}
        for k in outside:
            out_groups.setdefault(_stratum(res, k), Counter())[marks[k]["v"]] += 1
        L += ["", "### Örneklem dışı işaretler", "",
              "Kullanıcının kendiliğinden işaretledikleri (çoğu bir ayrılığın öbür okuyucusu); güven oranına girmez.",
              ""] + _trust_table(out_groups, order)
    # Ayrılıklar: iki okuyucunun ayrıldığı satırlarda kullanıcı hangisini tuttu
    rows = sorted({(k.split("|")[0], k.split("|")[2]) for k in marks
                   if k.split("|")[1] != "fazla" and _stratum(res, k) == "ayrilik"},
                  key=lambda x: (int(x[0].split("-")[1]), x[1]))
    if rows:
        models = sorted({m for t in res["taslaklar"].values() for m in t["modeller"]}, key=list(MODELS).index)
        L += ["", "### Ayrılıklar", "",
              "İki okuyucunun ayrıldığı satırlar: her okuyucunun hükmü ve kullanıcının işareti (işaretsizse —).", "",
              "| Taslak | Nükte | " + " | ".join(models) + " |", "|---|---|" + "---|" * len(models)]
        for draft, ident in rows:
            row = next(r for r in res["taslaklar"][draft]["satirlar"] if r["id"] == ident)
            cells = []
            for m in models:
                mk = marks.get(f"{draft}|{m}|{ident}")
                cells.append(f"{DURUM_TR.get(row['durum'].get(m), '?')} → {MARK_TR[mk['v']] if mk else '—'}")
            L.append(f"| {draft} | {ident} {_short(items.get(ident, {}).get('nukte', ''), 70)} | " + " | ".join(cells) + " |")
    weak = [k for k in inside + outside if marks[k]["v"] != "tutuyor"]
    if weak:
        L += ["", "### Tam tutmayanlar", ""]
        for k in weak:
            draft, who, ident = k.split("|", 2)
            what = (f"fazla {ident}" if who == "fazla" else
                    f"{ident} {_short(items.get(ident, {}).get('nukte', ''), 70)} · {who}: "
                    f"{DURUM_TR.get(next(r for r in res['taslaklar'][draft]['satirlar'] if r['id'] == ident)['durum'].get(who), '?')}")
            L.append(f"- {draft} · {what} → {MARK_TR[marks[k]['v']]}{'' if k in set(sample) else ' (örneklem dışı)'}")
    return L


def _extra_lines(f: dict, blocks: dict, items: dict) -> list[str]:
    readers = f["okuyucular"]
    head = (f"- **{', '.join(f.get('taslak') or [])}** · {'iki okuyucu' if len(readers) > 1 else readers[0]} · "
            f"{ {'kaynakli': 'kaynaklı', 'kendi_tespiti': 'kendi tespiti', 'isaretsiz': 'işaretsiz'}.get(f.get('isaret'), f.get('isaret') or '?')}"
            + (f" [{', '.join(f.get('kaynak') or [])}]" if f.get("kaynak") else "")
            + f": {f.get('iddia', '')}")
    out = [head]
    for m, e in f["es"].items():
        out.append(f"  - {m}: {e.get('iddia', '')}")
    for who, c, g in [(readers[0], f.get("celiski"), f.get("gerekce"))] + [(m, e.get("celiski"), e.get("gerekce"))
                                                                         for m, e in f["es"].items()]:
        if c:
            out.append(f"  - çelişki ({who}) {c} ({_short(items.get(c, {}).get('nukte', ''), 90)}): {g}")
    tr = _tr_of(blocks, f.get("taslak") or [])
    out.append(f"  > {_short(f.get('alinti', ''), 220)}")
    if tr:
        out.append(f"  > _Tercümesi:_ {_short(tr, 260)}")
    return out


# ---------------------------------------------------------------- D2: klasik eserlerin kullanımı

_MARK = re.compile(r"\[(?:[^\[\]]*?;\s*)?([\d][\d\s,،]*)\]")


def source_items(unit: str, n: int, server: str = "klasik") -> list[dict]:
    """Taslağın `server` eklentisinden bir kaynağa dayanan paragrafları: her (paragraf, kaynak) bir kalem. Paragraf
    çifti (Arapça ve tercümesi) birlikte verilir; işaret hangisindeyse (tercümede `[belâgat; 3]`, alıntıda `[3]`)."""
    blocks, sources = draft_blocks(unit, n)
    log = P.DRAFTS / unit / f"taslak-{n}.jsonl"
    ids = P.draft_sources(log) if log.exists() else {}
    texts = P.SourceTexts(unit)
    by_anchor = {a: t for a, _, _, t in blocks}
    items, seen = [], set()
    for anchor, lang, _, text in blocks:
        nums = {x for m in _MARK.finditer(text) for x in re.findall(r"\d+", m[1])}
        for num in sorted(nums, key=int):
            srv, sid = ids.get(num, (None, None))
            if srv != server:
                continue
            ar = anchor.replace("/tr/", "/ar/")
            key = (ar, num)
            if key in seen:
                continue
            seen.add(key)
            items.append({"id": f"K{len(items) + 1:02d}", "anchor": ar, "kaynak": num, "kaynak_id": sid,
                          "kaynak_atif": sources.get(num, ""), "kaynak_metin": texts.text(srv, sid, sources.get(num, "")),
                          "ar": by_anchor.get(ar, ""), "tr": by_anchor.get(ar.replace("/ar/", "/tr/"), "")})
    return items


def render_items(items: list[dict]) -> str:
    out = []
    for it in items:
        out += [f"## {it['id']} · taslağın paragrafı {it['anchor']} · kaynak [{it['kaynak']}]", "",
                f"Taslağın Arapçası: {it['ar']}", "", f"Taslağın Türkçesi: {it['tr']}", "",
                f"Kaynak [{it['kaynak']}] ({it['kaynak_atif']}): {it['kaynak_metin'] or '(metni bulunamadı)'}", ""]
    return "\n".join(out)


def kaynak(unit: str, drafts: list[int], models: list[str], parallel: int, again: bool) -> None:
    d = out_dir(unit)
    jobs = []
    for n in drafts:
        items = source_items(unit, n)
        (d / f"kaynak-taslak-{n}-kalemler.json").write_text(json.dumps(items, ensure_ascii=False, indent=1),
                                                            encoding="utf-8")
        print(f"taslak {n}: {len(items)} kalem (klasik esere dayanan paragraf × kaynak)")
        if not items:
            continue
        prompt, sha = build_prompt("KAYNAK", unit, kalemler=render_items(items))
        for m in models:
            stem = d / f"kaynak-taslak-{n}-{m}"
            if stem.with_suffix(".json").exists() and not again:
                continue
            jobs.append((prompt, m, stem, {"gorev": "kaynak", "taslak": n, "istem_sha": sha}))
    with ThreadPoolExecutor(max_workers=parallel) as pool:
        list(pool.map(lambda j: run_model(*j), jobs))


def d2_veri(unit: str, d1: list[int], d2: list[int], info: list[int] = ()) -> None:
    """D1 ile D2'nin karşılaştırma verisi (`provalar/<birim>/d2-veri.md`): kapsama, nükte nükte fark, klasik
    eserlerin kullanımı ve kaynak denetimi. Değerlendirme raporu bunun üstüne yazılır."""
    d = out_dir(unit)
    res = json.loads((d / "sonuc.json").read_text(encoding="utf-8"))
    env = res["envanter"]
    items = {i["id"]: i for i in env["kalemler"]}
    models = sorted({m for t in res["taslaklar"].values() for m in t["modeller"]}, key=list(MODELS).index)
    N = len(items)

    def found(t: str, iid: str, m: str | None = None) -> bool:
        row = next(r for r in res["taslaklar"][t]["satirlar"] if r["id"] == iid)
        ms = [m] if m else models
        return all(row["durum"].get(x) in FOUND for x in ms)

    L = [f"# Prova {unit}: D2'nin verisi (D1 ile karşılaştırma)", "",
         f"`uv run python scripts/d1-yz.py d2-veri {unit}` üretir. Taban D1: taslak {', '.join(map(str, d1))} (istem "
         f"v1-ince); D2: taslak {', '.join(map(str, d2))} (v1-ince-klasik: aynı istem, me'hazda klasik eserler); "
         f"yalnız bilgi için: taslak {', '.join(map(str, info)) or '—'} (tam istem, tabana girmez). "
         f"Envanter {N} kalem; \"ikisi de\": iki okuyucunun ({' ve '.join(models)}) da bulduğu dediği.", ""]
    L += ["## Kapsama", "", "| Taslak | Grup | " + " | ".join(f"Kapsama {m}" for m in models) + " | İkisi de | ✓ ikisi de |",
          "|---|---|" + "---:|" * (len(models) + 2)]
    for t in [f"taslak-{n}" for n in list(info) + d1 + d2]:
        if t not in res["taslaklar"]:
            continue
        g = "D1" if int(t.split("-")[1]) in d1 else "D2" if int(t.split("-")[1]) in d2 else "D1 (tam, bilgi)"
        covs = [sum(found(t, i, m) for i in items) / N for m in models]
        both = sum(found(t, i) for i in items)
        exact = sum(all(next(r for r in res["taslaklar"][t]["satirlar"] if r["id"] == i)["durum"].get(m) == "aynen"
                        for m in models) for i in items)
        L.append(f"| {t} | {g} | " + " | ".join(f"%{c * 100:.0f}" for c in covs) + f" | {both} (%{both / N * 100:.0f}) | {exact} |")

    def count(group, iid):
        return sum(found(f"taslak-{n}", iid) for n in group if f"taslak-{n}" in res["taslaklar"])
    # grup büyüklükleri farklı olabilir: oranla karşılaştırılır (D2'de en az 2/3, D1'de en çok 1/2 gibi)
    gained = [i for i in items if count(d2, i) / len(d2) - count(d1, i) / len(d1) >= 0.5]
    lost = [i for i in items if count(d1, i) / len(d1) - count(d2, i) / len(d2) >= 0.5]
    L += ["", "## Nükte nükte", "", f"Sayılar: o grubun kaç taslağında iki okuyucunun da bulduğu (D1 {len(d1)}, D2 "
          f"{len(d2)} taslak; oranlar bu yüzden grup büyüklüğüne göre okunur).", "",
          "| Kalem | Vecih | Nükte | D1 | D2 |", "|---|---|---|---:|---:|"]
    for iid, it in items.items():
        a, b = count(d1, iid), count(d2, iid)
        mark = " ▲" if iid in gained else " ▼" if iid in lost else ""
        L.append(f"| {iid} | {it.get('vecih')} | {_short(it.get('nukte', ''), 90)} | {a} | {b}{mark} |")
    L += ["", f"▲ D2'de oran en az yarım fazla: {', '.join(gained) or '—'} · ▼ D2'de oran en az yarım eksik: "
          f"{', '.join(lost) or '—'}", ""]
    # kaynakların eklentilere dağılımı (kaynakçadaki numaralar, son `cite` çağrılarından)
    L += ["## Kaynakların eklentilere dağılımı", "", "| Taslak | Grup | risale | tefsir | hadis | klasik | Toplam | "
          "İşaret: kaynaklı / kendi tespiti |", "|---|---|---:|---:|---:|---:|---:|---|"]
    for n in list(info) + d1 + d2:
        log = P.DRAFTS / unit / f"taslak-{n}.jsonl"
        if not log.exists():
            continue
        by = Counter(srv for srv, _ in P.draft_sources(log).values())
        text = "\n".join(t for _, lang, _, t in draft_blocks(unit, n)[0] if lang == "tr")
        own = len(re.findall(r"(?:kendi tespiti|istinbat)\]", text))   # h3'ten beri etiket "istinbat"
        sourced = len(re.findall(r"\[(?:dil|belâgat);\s*\d", text))
        L.append(f"| taslak-{n} | {'D1' if n in d1 else 'D2' if n in d2 else 'D1 (tam, bilgi)'} | {by['risale']} | {by['tefsir']} | {by['hadis']} | "
                 f"{by['klasik']} | {sum(by.values())} | {sourced} / {own} |")
    L.append("")
    # klasik eserlerin kullanımı
    L += ["## Klasik eserlerin kullanımı", "",
          "| Taslak | Klasik araç çağrısı | Kaynakçada klasik kaynak | Klasik esere dayanan paragraf × kaynak | Eserler |",
          "|---|---:|---:|---:|---|"]
    all_items = {}
    for n in d2:
        meta = json.loads((P.DRAFTS / unit / f"taslak-{n}.json").read_text())
        calls = sum(v for k, v in meta["calls"].items() if k.startswith("klasik__"))
        path = d / f"kaynak-taslak-{n}-kalemler.json"
        its = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
        all_items[n] = its
        srcs = {it["kaynak"] for it in its}
        works = Counter((it["kaynak_id"] or "?").split("/", 1)[0] for it in {it["kaynak"]: it for it in its}.values())
        L.append(f"| taslak-{n} | {calls} | {len(srcs)} | {len(its)} | {', '.join(f'{w} {c}' for w, c in works.most_common())} |")
    # kalemler: İşârât'ta karşılığı var mı (D7 eşleştirmesi), kaynak denetimi
    L += ["", "## Klasik esere dayanan paragraflar: İşârât'ta karşılığı ve kaynak denetimi", "",
          "Karşılık: D7 eşleştirmesinde bu paragraf bir envanter kalemine (aynen/kısmen) bağlanmış mı (iki okuyucudan "
          "biri yeter), yoksa \"fazla\" mı. Kaynak denetimi iki kör okuyucunun (`KAYNAK` görevi) sonucudur.", ""]
    tot_support = {m: Counter() for m in models}
    tot_role = Counter()
    linked = Counter()
    for n, its in all_items.items():
        t = f"taslak-{n}"
        tr = res["taslaklar"].get(t)
        if tr is None or not its:
            continue
        audit = {}
        for m in models:
            path = d / f"kaynak-taslak-{n}-{m}.json"
            if path.exists():
                audit[m] = {k["id"]: k for k in json.loads(path.read_text(encoding="utf-8")).get("kalemler", [])}
        L += [f"### {t}", "", "| Kalem | Paragraf | Kaynak | İşârât'ta | " + " | ".join(models) + " | Rol |",
              "|---|---|---|---|" + "---|" * len(models) + "---|"]
        for it in its:
            matches = sorted({iid for m in tr["modeller"].values() for iid, r in m["nukteler"].items()
                              if r.get("durum") in FOUND and it["anchor"] in [x.replace("/tr/", "/ar/") for x in r.get("taslak") or []]})
            extra = any(it["anchor"] in [x.replace("/tr/", "/ar/") for x in f.get("taslak") or []] for f in tr["fazla"])
            where = ", ".join(matches) if matches else ("fazla" if extra else "—")
            linked["nükte" if matches else "fazla" if extra else "yok"] += 1
            cells = []
            for m in models:
                a = audit.get(m, {}).get(it["id"], {})
                cells.append(a.get("durum", "?"))
                tot_support[m][a.get("durum", "?")] += 1
            role = Counter(audit.get(m, {}).get(it["id"], {}).get("rol") for m in models).most_common(1)[0][0]
            tot_role[role] += 1
            L.append(f"| {it['id']} | {it['anchor']} | [{it['kaynak']}] {_short(it['kaynak_atif'], 60)} | {where} | "
                     + " | ".join(cells) + f" | {role} |")
        notes = [(m, k) for m in models for k in audit.get(m, {}).values() if k.get("uygulama")]
        if notes:
            L += ["", "Ehline sorulacak uygulamalar:", ""] + [f"- {k['id']} ({m}): {k['uygulama']}" for m, k in notes]
        L.append("")
    L += ["## Toplam", "",
          f"- Klasik esere dayanan paragraf × kaynak: {sum(len(v) for v in all_items.values())}; İşârât'ın bir nüktesine "
          f"karşılık gelen {linked['nükte']}, fazla {linked['fazla']}, eşleştirmede geçmeyen {linked['yok']}.",
          *[f"- Kaynak denetimi ({m}): " + ", ".join(f"{k} {v}" for k, v in tot_support[m].most_common()) for m in models],
          "- Rol: " + ", ".join(f"{k} {v}" for k, v in tot_role.most_common())]
    path = P.DRAFTS / unit / "d2-veri.md"
    path.write_text("\n".join(L).rstrip() + "\n", encoding="utf-8")
    print(path.relative_to(ROOT))


# ---------------------------------------------------------------- D7.6 okuma sayfasının katmanı

def hidden_para_anchors(unit: str) -> dict[str, str]:
    """İstem kimliği (a003, t006) -> okuma sayfasındaki gizlenen paragrafın çapası (V1/ar/h1); `hidden_sections` gibi."""
    cfg = P.UNITS[unit]
    out = {}
    for lang, rows in hidden(unit).items():
        work = "isaratul-icaz-arabi" if lang == "ar" else "isaratul-icaz"
        bounds = {v: k for k, v in cfg["sections"][work].items() if k != "son"}
        node = P.unit_node(cfg, work)
        current, para, count = None, None, Counter()
        for short, sid, _, pid in rows:
            local = P.local_id(cfg, work, sid)
            if local in bounds:
                current, para = bounds[local], None
            if current is None:
                continue
            if pid != para:
                count[current] += 1
                para = pid
            out[short] = f"{current}/{lang}/h{count[current] - 1}"
    return out


SAMPLE_SIZE = 30


def sample_keys(res: dict, size: int = SAMPLE_SIZE) -> list[str]:
    """D7.7 örneklemi: katmanlı, sabit tohumla; önce ayrılıklar ve fazlalar, sonra durumlara göre eşit."""
    import random
    rng = random.Random(f"d7-{res['birim']}-{res['envanter']['at']}")
    strata: dict[str, list[str]] = {}
    for t, tr in res["taslaklar"].items():
        for r in tr["satirlar"]:
            for m, d in r["durum"].items():
                if d is None:
                    continue
                stratum = "ayrilik" if r["uyum"] == "ayrilik" else d
                strata.setdefault(stratum, []).append(f"{t}|{m}|{r['id']}")
        for f in tr["fazla"]:
            strata.setdefault("celiski" if f.get("celiski") else "fazla", []).append(f"{t}|fazla|{f['k']}")
    for keys in strata.values():
        rng.shuffle(keys)
    out: list[str] = []
    while len(out) < size and any(strata.values()):
        for name in ("ayrilik", "celiski", "fazla", "aynen", "kismen", "farkli_gerekce", "yok"):
            if strata.get(name) and len(out) < size:
                out.append(strata[name].pop())
    return out


def page_data(unit: str) -> dict | None:
    path = out_dir(unit) / "sonuc.json"
    if not path.exists():
        return None
    res = json.loads(path.read_text(encoding="utf-8"))
    anchors = hidden_para_anchors(unit)
    h = hidden(unit)
    tr_text = {r[0]: r[2] for r in h["tr"]}
    items = {}
    for i in res["envanter"]["kalemler"]:
        places = sorted({anchors[x] for x in (i.get("ar") or []) + (i.get("tr") or []) if x in anchors})
        # İşârât'ın sözü sayfada Abdülmecid Nursî tercümesinden (kullanıcının isteği, 2026-11-14); Arapça alıntı ayrıca
        tr = i.get("alinti", "") if i.get("yalniz_tercume") else " ".join(tr_text.get(x, "") for x in i.get("tr") or [])
        items[i["id"]] = {"v": i.get("vecih", ""), "l": i.get("lafiz", ""), "n": i.get("nukte", ""),
                          "q": "" if i.get("yalniz_tercume") else i.get("alinti", ""), "qt": tr.strip(), "h": places}
    drafts = {}
    for t, tr in res["taslaklar"].items():
        rows = {}
        for r in tr["satirlar"]:
            row = {"u": r["uyum"]}
            for m, pm in tr["modeller"].items():
                x = pm["nukteler"].get(r["id"])
                if x:
                    row[m] = {"d": x.get("durum"), "a": x.get("taslak") or [], "q": x.get("alinti", ""),
                              "g": x.get("gerekce", ""), "ok": all(x["denetim"].values())}
            rows[r["id"]] = row
        extras = [{"k": f["k"], "a": f.get("taslak") or [], "q": f.get("alinti", ""), "i": f.get("iddia", ""),
                   "s": f.get("isaret", ""), "src": f.get("kaynak") or [], "c": f.get("celiski"),
                   "g": f.get("gerekce", ""), "r": f["okuyucular"], "es": f["es"], "ok": all(f["denetim"].values())}
                  for f in tr["fazla"]]
        drafts[t] = {"rows": rows, "extras": extras}
    return {"models": sorted({m for t in res["taslaklar"].values() for m in t["modeller"]}, key=list(MODELS).index),
            "items": items, "drafts": drafts, "sample": res.get("orneklem", []), "critic": critic_page(unit),
            "bilirkisi": bilirkisi_page(unit), **critic_review_page(unit)}


def critic_review_page(unit: str) -> dict:
    """D9.3 süzgeci: örneklemin 10 notu (`elestiri-orneklem.json`) ve sistemli başlıklar (`elestiri-sistemli.json`),
    başlığın dayandığı maddelerin metniyle (eleştirmenin `sistemli` listesinden, taslak ve sırasıyla)."""
    d = out_dir(unit)
    sp, zp = d / "elestiri-orneklem.json", d / "elestiri-sistemli.json"
    sample = [{"t": x["taslak"], "k": x["k"]} for x in json.loads(sp.read_text(encoding="utf-8"))["notlar"]] if sp.exists() else []
    note = ""
    d11 = d / "d11-orneklem.json"        # D11.3: iki eleştiri biçiminin eşit örneklemi (D8'in süzgecinin yerine)
    if d11.exists():
        dd = json.loads(d11.read_text(encoding="utf-8"))
        sample = [{"t": x["taslak"], "k": x["k"]} for x in dd["notlar"]]
        note = ("Bu notlar iki eleştiri biçiminin karşılaştırması için seçildi (D11): aynı iki taslak (eski taslak 3 ve "
                "yeni hattın pilotu taslak 7) bir kez bütün olarak, bir kez bölüm bölüm eleştirildi; her taslağın her "
                "biçiminden 5 not, türlere yayılarak. Övgü notları, eleştirmenin \"ehline sorulmalı\" dedikleri ve "
                "alıntısı denetimde tutmayanlar girmedi. Sıra karışıktır; notun biçimi kartındaki etiketten görünür.")
    systemic = []
    if zp.exists():
        lists = {}
        for path in d.glob("elestiri-taslak-*.denetim.json"):
            n = int(re.search(r"taslak-(\d+)", path.name).group(1))
            lists[n] = json.loads(path.read_text(encoding="utf-8")).get("sistemli", [])
        ref = lambda pairs: [{"t": f"taslak-{n}", "m": lists[n][i - 1]["metin"]} for n, i in pairs]
        for b in json.loads(zp.read_text(encoding="utf-8"))["basliklar"]:
            systemic.append({"id": b["id"], "tur": b["tur"], "b": b["baslik"], "x": b["aciklama"],
                             "d": ref(b["dayanak"]), "karsi": ref(b.get("karsi", []))})
    return {"critic_sample": sample, "systemic": systemic, "critic_sample_note": note}


def bilirkisi_page(unit: str) -> dict:
    """D6.2 örneklemi (A sabit, B süzgeçten): sayfada tabaka ve eleştirmenin itirazı gösterilmez (kör okuma)."""
    out = {}
    for part in ("A", "B"):
        path = out_dir(unit) / f"bilirkisi-{part}.json"
        if not path.exists():
            continue
        qpath = path.with_name(f"bilirkisi-{part}-sorular.json")   # dar sorular (S5; iddiadan sadeleştirilmiş)
        questions = json.loads(qpath.read_text(encoding="utf-8"))["sorular"] if qpath.exists() else {}
        items = []
        for i in json.loads(path.read_text(encoding="utf-8"))["maddeler"]:
            items.append({"id": i["id"], "t": i["taslak"], "a": i["capa"], "c": i.get("iddia") or "",
                          "q": questions.get(i["id"], ""),
                          "m": i.get("isaret") or "", "ar": i.get("arapca") or "", "tr": i.get("tercume") or "",
                          "e": i.get("elestiri") or "", "s": i.get("soru") or "",
                          "src": [{"n": k["no"], "c": k.get("atif", ""), "x": k.get("metin") or ""}
                                  for k in i.get("kaynaklar") or []]})
        out[part] = items
    return out


def critic_key(n: int, note: dict) -> str:
    """D9.3 süzgecinin kararı bu anahtara bağlanır (taslak, çapa, metin)."""
    return hashlib.sha1(f"{n}|{note.get('capa')}|{note.get('metin')}".encode()).hexdigest()[:10]


def critic_page(unit: str) -> dict:
    """D9.2 eleştirmeninin notları (denetlenmiş hâli), taslak başına: okuma sayfasının ayrı katmanı (D9.3)."""
    out = {}
    for path in out_dir(unit).glob("elestiri-taslak-*.denetim.json"):
        n = int(re.search(r"taslak-(\d+)", path.name).group(1))
        data = json.loads(path.read_text(encoding="utf-8"))
        notes = []
        for x in data.get("notlar", []):
            dn = x.get("denetim", {})
            notes.append({"k": critic_key(n, x), "t": x.get("tur"), "a": x.get("capa") or "genel", "n": x.get("nukte"),
                          "m": x.get("metin", ""), "h": x.get("nasil"), "s": x.get("soru"), "e": bool(x.get("ehline_sor")),
                          "q": x.get("taslak_alinti"), "d": x.get("dayanak") or [],
                          "ok": dn.get("alinti") is not False and not dn.get("dayanak_yok")})
        out[f"taslak-{n}"] = {"notes": notes, "ozet": data.get("ozet", ""), "sistemli": data.get("sistemli", []),
                              "oneriler": data.get("oneriler", [])}
    # D11: bölüm bölüm eleştiri (`d1-hat.py bolum`): aynı taslağın notlarına eklenir, kendi anahtarıyla ve işaretiyle
    for path in out_dir(unit).glob("bolum-elestiri-taslak-*.json"):
        if not (m := re.fullmatch(r"bolum-elestiri-taslak-(\d+)\.json", path.name)):   # bölüm başına dosyalar değil
            continue
        n = int(m.group(1))
        data = json.loads(path.read_text(encoding="utf-8"))
        entry = out.setdefault(f"taslak-{n}", {"notes": [], "ozet": "", "sistemli": [], "oneriler": []})
        for x in data.get("notlar", []):
            dn = x.get("denetim", {})
            entry["notes"].append({"k": "b" + critic_key(n, x), "b": x.get("bolum"), "t": x.get("tur"),
                                   "a": x.get("capa") or "genel", "n": x.get("nukte"), "m": x.get("metin", ""),
                                   "h": x.get("nasil"), "s": x.get("soru"), "e": bool(x.get("ehline_sor")),
                                   "q": x.get("taslak_alinti"), "d": x.get("dayanak") or [],
                                   "ok": dn.get("alinti") is not False and not dn.get("dayanak_yok")})
    # D12: kapalı kitap eleştirmen (`d1-duzelt.py kapali`; İşârât'ın bu birimi gizliydi): ayrı katman ("c": "kapali"),
    # numarası düzeltmedeki gibi K1, K2… (taslak 8'in düzeltmesi bu numaralarla karşıladı ya da reddetti)
    for path in out_dir(unit).glob("kapali-elestiri-taslak-*.json"):
        if not (m := re.fullmatch(r"kapali-elestiri-taslak-(\d+)\.json", path.name)):
            continue
        n = int(m.group(1))
        data = json.loads(path.read_text(encoding="utf-8"))
        entry = out.setdefault(f"taslak-{n}", {"notes": [], "ozet": "", "sistemli": [], "oneriler": []})
        entry["kapali"] = {"ozet": data.get("ozet", {}), "sistemli": data.get("sistemli", [])}
        handled = {}
        for rev in P.DRAFTS.joinpath(unit).glob("taslak-*.duzeltme.json"):      # düzeltmede karşılandı mı, reddedildi mi
            meta = json.loads(rev.with_name(rev.name.replace(".duzeltme.json", ".json")).read_text(encoding="utf-8"))
            d = meta.get("duzeltme") or {}
            if d.get("kaynak") != n or d.get("notlar") != "kapali":
                continue
            r = json.loads(rev.read_text(encoding="utf-8"))
            m2 = int(re.search(r"taslak-(\d+)", rev.name).group(1))
            for ch in r.get("degisiklikler", []):
                for no in ch.get("notlar", []):
                    handled[no] = f"taslak {m2}: karşılandı"
            for x in r.get("reddedilen", []):
                handled[x.get("not")] = f"taslak {m2}: reddedildi ({x.get('gerekce', '')})"
        for i, x in enumerate(data.get("notlar", []), 1):
            dn = x.get("denetim", {})
            entry["notes"].append({"k": "k" + critic_key(n, x), "c": "kapali", "no": f"K{i}", "b": x.get("bolum"),
                                   "t": x.get("tur"), "a": x.get("capa") or "genel", "n": None, "m": x.get("metin", ""),
                                   "h": x.get("nasil"), "s": x.get("soru"), "e": bool(x.get("ehline_sor")),
                                   "o": x.get("oneri"), "p": x.get("oncelik"), "r": handled.get(f"K{i}"),
                                   "q": x.get("taslak_alinti"), "d": x.get("dayanak") or [],
                                   "ok": dn.get("alinti") is not False and not dn.get("dayanak_yok")})
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("envanter")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--model", choices=MODELS, default="fable")
    p.add_argument("--denetci", choices=MODELS, default="opus")
    p = sub.add_parser("envanter-birlestir", help="ham envanter ve denetimden yeniden birleştir (model çağırmadan)")
    p.add_argument("unit", choices=P.UNITS)
    p = sub.add_parser("eslestir")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--taslak", type=int, nargs="*")
    p.add_argument("--modeller", nargs="*", choices=MODELS, default=["fable", "opus"])
    p.add_argument("--paralel", type=int, default=3)
    p.add_argument("--yeniden", action="store_true")
    p = sub.add_parser("rapor")
    p.add_argument("unit", choices=P.UNITS)
    p = sub.add_parser("kaynak", help="D2: taslağın klasik eserlere dayanışını iki kör okuyucuya denetlet")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--taslak", type=int, nargs="+", required=True)
    p.add_argument("--modeller", nargs="*", choices=MODELS, default=["fable", "opus"])
    p.add_argument("--paralel", type=int, default=3)
    p.add_argument("--yeniden", action="store_true")
    p = sub.add_parser("d2-veri", help="D1 ile D2'nin karşılaştırma verisi")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--d1", type=int, nargs="+", default=[2, 3], help="taban: D1'in ince istemli taslakları")
    p.add_argument("--bilgi", type=int, nargs="*", default=[1], help="yalnız bilgi için gösterilen taslaklar")
    p.add_argument("--d2", type=int, nargs="+", default=[4, 5, 6])
    p = sub.add_parser("istem", help="istemi dosyaya yaz (denetim için, model çağırmadan)")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("gorev", choices=["ENVANTER", "ESLESTIRME"])
    p.add_argument("--taslak", type=int, default=1)
    args = parser.parse_args()
    if args.command == "envanter":
        envanter(args.unit, args.model, args.denetci)
    elif args.command == "envanter-birlestir":
        d = out_dir(args.unit)
        raw = json.loads((d / "envanter-ham.json").read_text(encoding="utf-8"))
        rev_path = d / "envanter-denetim.json"
        review = json.loads(rev_path.read_text(encoding="utf-8")) if rev_path.exists() else {"oneriler": []}
        m1 = json.loads((d / "envanter-ham.meta.json").read_text())
        m2 = json.loads((d / "envanter-denetim.meta.json").read_text()) if rev_path.exists() else {}
        merge_envanter(args.unit, raw, review, {"cikaran": m1["model"], "denetci": m2.get("model", ""),
                                                "istem_sha": m1["istem_sha"], "denetim_basarili": rev_path.exists()})
    elif args.command == "eslestir":
        eslestir(args.unit, args.taslak or drafts_of(args.unit), args.modeller, args.paralel, args.yeniden)
    elif args.command == "rapor":
        rapor(args.unit)
    elif args.command == "kaynak":
        kaynak(args.unit, args.taslak, args.modeller, args.paralel, args.yeniden)
    elif args.command == "d2-veri":
        d2_veri(args.unit, args.d1, args.d2, args.bilgi)
    else:
        if args.gorev == "ENVANTER":
            text, _ = build_prompt("ENVANTER", args.unit)
        else:
            env = json.loads((out_dir(args.unit) / "envanter.json").read_text(encoding="utf-8"))
            blocks, sources = draft_blocks(args.unit, args.taslak)
            text, _ = build_prompt("ESLESTIRME", args.unit, envanter=env_for_prompt(env),
                                   taslak=render_draft(blocks, sources))
        path = P.OUT / args.unit / f"yz-istem-{args.gorev.lower()}.md"
        path.write_text(text, encoding="utf-8")
        print(f"{path.relative_to(ROOT)}: {len(text):,} karakter")


if __name__ == "__main__":
    main()
