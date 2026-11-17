"""D12.5 turları (PLANLAR.md D12.5; plan `docs/d1/d12-rapor-ve-plan.md` 4.3–4.10): yeni kolların hattı, ölçüm, okuma.

    uv run python scripts/d1-tur.py hazirla 9-10          # T1 kolunun okuma istemi ve sızıntı testi (c1)
    uv run python scripts/d1-tur.py yaz 9-10              # T1 kolu: okuma (araçlı) → denetim → tamamla → yazım (yalnız cite)
    uv run python scripts/d1-tur.py kapsam 9-10 --taslak 1 2   # âyetin kelime ve harflerinin taslakta ele alınma oranı
    uv run python scripts/d1-tur.py olc 9-10 --tur T1 --taban 1 --yeni 2   # eşleştirme (tek okuyucu), D9.1, kör A/B, sayılar
    uv run python scripts/d1-tur.py okuma 9-10 --tur T1 --taban 1 --yeni 2 --yerler yerler.json   # okuma sayfası (standart)
    uv run python scripts/d1-tur.py sonuc 9-10 --tur T1 ~/İndirilenler/d1-notlar-*.json   # kullanıcının A/B'si

Taban kol `d1-hat.py yazdir` (o anki en iyi hat; T1'de h2). Yeni kol bu betikte. Kararlar:
- **T1, okuma ve yazım ayrı** (`docs/d1/cizelge-istemi.md` c1): iki kol arasındaki tek fark işin bölünmesi ve kelime
  çizelgesidir; görev, usul, uzunluk, şablon ve tırnak kuralları h2'den aynen alınır, me'haz (kaynak dosyası, Ek 1–2)
  aynıdır. Okuma çizelgesini program denetler (boş satır reddedilir): eksik ya da boş satırlar ve kimliğinin metninde
  bulunmayan alıntılar bir kez geri gönderilir (aynı sunucularla), kalan kusurlar sayılır. Yazım oturumunda okuma
  araçları kapalıdır, yalnız `cite` açık.
- Yeni kolun taslağı da `taslak-<n>.md` olur; `.jsonl` okuma, tamamlama ve yazım dökümlerinin art arda eklenmişidir
  (D9.1 okunanları ondan çıkarır), istem kaydı `istem-cizelge-c1.md` iki istemin birleşiğidir.
- Ölçü (4.3, 4.4): tek okuyuculu eşleştirme (Opus), D9.1, kör A/B (açık kitap, o2), kapsam, uzunluk, maliyet.
"""

import argparse
import importlib.util
import json
import os
import random
import re
import sqlite3
import subprocess
import tempfile
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

from risale_mcp.paths import ROOT
from risale_mcp.quran import skeleton


def _load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


D = _load("d1_duzelt", "d1-duzelt.py")
H, M, Y, P, E = D.H, D.M, D.Y, D.P, D.E

CIZELGE_PROMPT = ROOT / "docs" / "d1" / "cizelge-istemi.md"
SURUM = "c1"
OPUS = "claude-opus-5-5"
SERVERS = ("risale", "tefsir", "hadis", "klasik")
# yazım oturumunda kapalı okuma araçları (yalnız `cite` açık; listede olmayan araç modelin önüne gelmez)
READ_TOOLS = {
    "risale": ("list_works", "get_outline", "read_section", "get_passage", "search", "find_sentence", "find_ayah",
               "get_ayah", "find_hadith", "get_hadith", "semantic_search"),
    "tefsir": ("find_ayah", "find_sentence", "get_ayah", "get_outline", "get_passage", "list_works", "read_section",
               "search", "semantic_search", "text_links"),
    "klasik": ("find_ayah", "find_sentence", "get_ayah", "get_outline", "get_passage", "list_works", "read_section",
               "search", "semantic_search"),
    "hadis": ("find_by_citation", "get_ayah", "get_hadith", "get_outline", "list_books", "read_chapter",
              "search_hadith", "semantic_search"),
}


# ---------------------------------------------------------------- istemler

def parts() -> tuple[dict[str, str], str]:
    raw = CIZELGE_PROMPT.read_text(encoding="utf-8")
    found = dict(re.findall(r"^---- (\w+) ----\n(.*?)(?=^---- \w+ ----|\Z)", raw, flags=re.M | re.S))
    return {k: v.strip() for k, v in found.items()}, P._sha(raw)


def h2_body(unit: str) -> dict[str, str]:
    """Taban hattın (h2) istem gövdesi, doldurulmuş, `## ` başlıklarına göre: {'giris', 'Taslağın adı…', …}."""
    cfg = P.UNITS[unit]
    h = H.hedef(unit)
    body = H.HAT_PROMPT.read_text(encoding="utf-8").split("---- İSTEM ----", 1)[1].strip()
    fmt = lambda x: f"{x:,}".replace(",", ".")
    body = body.format(sura_name=cfg["sura_name"], ayahs="–".join(map(str, cfg["ayahs"])), en_az=fmt(h["en_az"]),
                       en_cok=fmt(h["en_cok"]), kelime_az=fmt(h["kelime_az"]), kelime_cok=fmt(h["kelime_cok"]))
    chunks = re.split(r"(?m)^(?=## )", body)
    out = {"giris": chunks[0].strip()}
    for c in chunks[1:]:
        out[c.split("\n", 1)[0][3:].strip()] = c.strip()
    return out


def _sec(b: dict, prefix: str) -> str:
    return next(v for k, v in b.items() if k.startswith(prefix))


def ekler(unit: str) -> tuple[str, str]:
    cfg = P.UNITS[unit]
    ozet = P.apply_edits(P.OZET.read_text(encoding="utf-8"), cfg["ozet"], "özet")
    cizelge = P.apply_edits(P.CIZELGE.read_text(encoding="utf-8"), cfg["cizelge"], "çizelge")
    ek1 = H._section(ozet, H.OZET_BOLUM[0], "## 6. Anlatım biçimi")
    ek2 = H._section(cizelge, "## Çizelge: Bakara", "## Çizelge: Fâtiha")
    return (f"# Ek 1: Usul özeti, 4. ve 5. bölüm (prova kopyası)\n\n{ek1}\n\n---\n\n"
            f"# Ek 2: Birim çizelgesi, Bakara (prova kopyası)\n\n{ek2}")


def okuma_prompt(unit: str) -> str:
    b = h2_body(unit)
    pp, _ = parts()
    dosya = (P.OUT / unit / "dosya.md").read_text(encoding="utf-8")
    body = "\n\n".join([b["giris"], _sec(b, "Taslağın adı"), _sec(b, "Me'haz"), _sec(b, "Usul"), pp["OKUMA"]])
    return f"{body}\n\n---\n\n{ekler(unit)}\n\n---\n\n# Ek 3: " + dosya.removeprefix("# ")


def yazim_prompt(unit: str, cizelge_md: str) -> str:
    b = h2_body(unit)
    pp, _ = parts()
    body = "\n\n".join([b["giris"], _sec(b, "Taslağın adı"), _sec(b, "Usul"), _sec(b, "Şablon"), pp["YAZIM"]])
    return f"{body}\n\n---\n\n{ekler(unit)}\n\n---\n\n# Ek 3: Okuma çizelgesi\n\n{cizelge_md}"


def hazirla(unit: str) -> str:
    cfg = P.UNITS[unit]
    if not (P.OUT / unit / "dosya.md").exists():
        raise SystemExit(f"önce: uv run python scripts/d1-hat.py hazirla {unit}")
    prompt = okuma_prompt(unit)
    path = P.OUT / unit / f"istem-cizelge-okuma-{SURUM}.md"
    path.write_text(prompt, encoding="utf-8")
    ok = P.leak_report(unit, cfg, P.OUT / unit, prompt, f"sizinti-cizelge-okuma-{SURUM}.md")
    print(f"{path.relative_to(ROOT)}: {len(prompt):,} harf; sızıntı testi {'temiz' if ok else 'SORUN'}")
    if not ok:
        raise SystemExit(1)
    return prompt


# ---------------------------------------------------------------- model

def call(unit: str, prompt: str, log: Path, only_cite: bool = False) -> tuple[str, dict, float | None, int, int]:
    env = {k: v for k, v in os.environ.items() if k not in P.PARENT_ENV}
    cmd = ["claude", "-p", "--model", OPUS, "--effort", "high", "--output-format", "stream-json", "--verbose",
           "--mcp-config", str(P.OUT / unit / "mcp-klasik.json"), "--strict-mcp-config", "--tools", "",
           "--no-session-persistence"]
    if only_cite:
        cmd += ["--allowedTools", ",".join(f"mcp__{s}__cite" for s in SERVERS),
                "--disallowedTools", ",".join(f"mcp__{s}__{t}" for s, ts in READ_TOOLS.items() for t in ts)]
    else:
        cmd += ["--allowedTools", ",".join(f"mcp__{s}" for s in SERVERS)]
    started = time.monotonic()
    print(f"{log.name}: {OPUS} ({datetime.now():%H:%M})", flush=True)
    with tempfile.TemporaryDirectory(prefix="d1-tur-") as tmp, log.open("w", encoding="utf-8") as out:
        done = subprocess.run(cmd, input=prompt, cwd=tmp, env=env, stdout=out, stderr=subprocess.PIPE, text=True,
                              timeout=P.TIMEOUT, check=False)
    answer, calls, cost = P.transcript(log)
    secs = round(time.monotonic() - started)
    print(f"  {secs} sn, {sum(calls.values())} araç çağrısı, ≈{cost or 0:.2f} $, çıkış {done.returncode}", flush=True)
    if done.stderr.strip():
        log.with_suffix(".stderr.txt").write_text(done.stderr, encoding="utf-8")
    return answer, calls, cost, secs, done.returncode


# ---------------------------------------------------------------- çizelgenin denetimi

ATTACHED = "وفبلكس"


def ayah_words(unit: str) -> list[dict]:
    a = M.Ayah(unit)
    return [{"ayet": v, "lafiz": w, "norm": n, "sk": sk(w)} for v, w, n in a.words]


def sk(word: str) -> str:
    """Harf iskeleti (Osmanî ve imlâî yazım bir: يخدعون = يخادعون); boş kalırsa normal biçim."""
    return skeleton(word) or M.norm(word)


def same(tok: str, word: str) -> bool:
    """İki kelime aynı mı: iskeletleri bir ya da biri öbürünün başındaki و/ف/ب/ل'siz hâli."""
    na, nb = M.norm(tok), M.norm(word)
    if len(na) <= 3 or len(nb) <= 3:         # edat ve kısa kelime: iskelet çok şeyi bir eder ("لا" = "إلا")
        return M.eq(na, nb) or M.eq(nb, na)
    a, b = sk(tok), sk(word)
    return bool(a) and bool(b) and (a == b or (len(b) > 2 and b[1:] == a and b[0] in "فبلك")
                                    or (len(a) > 2 and a[1:] == b and a[0] in "فبلك"))


def _match(row_toks: list[str], word: dict) -> bool:
    return any(same(t, word["lafiz"]) for t in row_toks)


class Sentences:
    """Kimlikten metin (prova veritabanları; aralık `…/c004..c006`)."""

    def __init__(self, unit: str):
        self.t = P.SourceTexts(unit)

    def text(self, sid: str) -> str | None:
        for server in ("tefsir", "risale", "klasik", "hadis"):
            if (x := self.t.text(server, sid, "")):
                return x
        return None

    def server(self, sid: str) -> str | None:
        for server in ("tefsir", "risale", "klasik", "hadis"):
            if self.t.text(server, sid, ""):
                return server
        return None


def _quotes(data: dict):
    """Çizelgedeki bütün (yer, müfessir kaydı) çiftleri."""
    for r in data.get("kelimeler", []):
        for m in r.get("mufessirler") or []:
            yield f"kelime {r.get('no')}", m
    for c in data.get("cumleler", []):
        for m in c.get("mufessirler") or []:
            yield f"cümle {c.get('no')}", m
    for i, o in enumerate(data.get("onceki", []), 1):
        for m in o.get("mufessirler") or []:
            yield f"öncesiyle bağ {i}", m
    for i, a in enumerate(data.get("ayrilik", []), 1):
        for m in a.get("gorusler") or []:
            yield f"ayrılık {i}", m
    for m in data.get("isarat_nazir", []):
        yield "İşârât nazîri", m


def denetle(unit: str, data: dict, texts: Sentences) -> dict:
    words = ayah_words(unit)
    rows = data.get("kelimeler", [])
    toks = [[x for x in M.SEP.split(r.get("lafiz", "")) if M.norm(x)] for r in rows]
    missing = [w for w in words if not any(_match(ts, w) for ts in toks)]
    empty = []
    for r in rows:
        has = bool((r.get("irab") or "").strip()) and any(
            (r.get(k) or "") if not isinstance(r.get(k), list) else r.get(k)
            for k in ("mufessirler", "tercih", "nukte_adayi"))
        if not has and not (r.get("bos_gerekce") or "").strip():
            empty.append(r.get("no"))
    bad_quotes = []
    n_quotes = 0
    for where, m in _quotes(data):
        n_quotes += 1
        sid, soz = (m.get("kimlik") or "").strip("` "), m.get("soz") or ""
        text = texts.text(sid) if sid else None
        if text is None:
            bad_quotes.append({"yer": where, "kimlik": sid, "sorun": "kimlik yok"})
        elif soz and not Y.quote_found(soz, text):
            bad_quotes.append({"yer": where, "kimlik": sid, "sorun": "alıntı bu kimliğin metninde yok", "soz": soz[:200]})
    harf_rows = sum(1 for r in rows if r.get("harfler"))
    attached = [w for w in words if w["norm"][:1] in ATTACHED and len(w["norm"]) > 3]
    return {"kelime": len(words), "satir": len(rows), "eksik": [w["lafiz"] for w in missing], "bos": empty,
            "alinti": n_quotes, "alinti_sorunlu": bad_quotes, "harfli_satir": harf_rows,
            "bitisik_harf_adayi": len(attached), "bos_gerekceli": sum(1 for r in rows if (r.get("bos_gerekce") or "").strip())}


def eksik_text(d: dict) -> str:
    L = []
    if d["eksik"]:
        L += ["## Satırı olmayan kelimeler", ""] + [f"- {w}" for w in d["eksik"]] + [""]
    if d["bos"]:
        L += ["## Boş satırlar (i'râbı yok ya da müfessir, tercih ve nükte alanlarının üçü de boş, gerekçesiz)", ""]
        L += [f"- {n}" for n in d["bos"]] + [""]
    if d["alinti_sorunlu"]:
        L += ["## Kimliğinin metninde bulunamayan alıntılar (yalnız kelime satırlarındakiler buradan düzeltilir; "
              "öbürleri için ilgili kelime satırına doğru kimlik ve sözle ekle)", ""]
        L += [f"- {x['yer']} · `{x['kimlik']}` · {x['sorun']}" + (f": {x.get('soz', '')}" if x.get("soz") else "")
              for x in d["alinti_sorunlu"]] + [""]
    return "\n".join(L)


def merge_rows(data: dict, fix: dict) -> dict:
    by_no = {r.get("no"): i for i, r in enumerate(data.get("kelimeler", []))}
    for r in fix.get("kelimeler", []):
        if r.get("no") in by_no:
            data["kelimeler"][by_no[r["no"]]] = r
        else:
            data.setdefault("kelimeler", []).append(r)
    return data


# ---------------------------------------------------------------- çizelgenin Markdown'ı (yazım istemine)

def _m(ms: list) -> list[str]:
    out = []
    for m in ms or []:
        out.append(f"  - `{m.get('kimlik', '')}`: \"{m.get('soz', '')}\""
                   + (f" ({m['ozet']})" if m.get("ozet") else ""))
    return out


def render(unit: str, data: dict) -> str:
    a = M.Ayah(unit)
    L = ["## Âyetler", ""]
    for v in a.verses:
        L += [f"> {v['text']} ({v['ref']})", f"> Meâl ({v['meal_by']}): {v['meal']}", ""]
    L += [f"## Maksat (okuyanın sözü)", "", data.get("maksat", ""), "",
          f"## Mukaddime (okuyanın sözü)", "", data.get("mukaddime", ""), "", "## Öncesiyle bağ", ""]
    for o in data.get("onceki", []):
        L += [f"- {o.get('bag', '')}"] + _m(o.get("mufessirler"))
    L += ["", "## Cümleler", ""]
    for c in data.get("cumleler", []):
        L += [f"### {c.get('no')}: {c.get('lafiz', '')}", f"- Hey'et: {c.get('heyet', '')}"]
        if c.get("mukadder"):
            L.append(f"- Mukadder (okuyanın takdiri): {c['mukadder']}")
        L += _m(c.get("mufessirler")) + [""]
    L += ["## Kelimeler", ""]
    for r in data.get("kelimeler", []):
        L.append(f"### {r.get('no')} · {r.get('cumle', '')} · {r.get('lafiz', '')}")
        for k, lab in (("irab", "İ'râb"), ("siga", "Sîga"), ("tarif_tenkir", "Ta'rif-tenkir"),
                       ("takdim_tehir", "Takdim-te'hir"), ("tercih", "Tercih")):
            if (r.get(k) or "").strip():
                L.append(f"- {lab}: {r[k]}")
        for hf in r.get("harfler") or []:
            L.append(f"- Harf {hf.get('harf', '')}: {hf.get('islev', '')}")
        if r.get("mufessirler"):
            L.append("- Müfessirler:")
            L += _m(r["mufessirler"])
        if (r.get("nukte_adayi") or "").strip():
            L.append(f"- Nükte adayı (okuyanın sözü): {r['nukte_adayi']}")
        if (r.get("bos_gerekce") or "").strip():
            L.append(f"- Boş: {r['bos_gerekce']}")
        L.append("")
    if data.get("ayrilik"):
        L += ["## Müfessirlerin ayrıldığı yerler", ""]
        for x in data["ayrilik"]:
            L += [f"- {x.get('yer', '')}" + (f": {x['not']}" if x.get("not") else "")] + _m(x.get("gorusler"))
        L.append("")
    if data.get("isarat_nazir"):
        L += ["## İşârât'ın öbür birimlerinde nazîrler", ""] + _m(data["isarat_nazir"]) + [""]
    return "\n".join(L)


# ---------------------------------------------------------------- yeni kol

def yaz(unit: str, n: int | None = None) -> int:
    keep = P.DRAFTS / unit
    keep.mkdir(parents=True, exist_ok=True)
    taken = {int(m.group(1)) for p in keep.glob("taslak-*") if (m := re.match(r"taslak-(\d+)", p.name))}
    n = n or max(taken, default=0) + 1
    if (keep / f"taslak-{n}.md").exists() or (keep / f"taslak-{n}.jsonl").exists():
        raise SystemExit(f"taslak {n} var (ya da yazılıyor)")
    stem = keep / f"taslak-{n}"
    pp, sha = parts()
    texts = Sentences(unit)
    # 1. okuma
    p1 = hazirla(unit)
    a1, c1, cost1, s1, rc1 = call(unit, p1, Path(str(stem) + ".okuma.jsonl"))
    data = Y.extract_json(a1) or D.repair_json(a1)
    if data is None:
        Path(str(stem) + ".okuma.cevap.txt").write_text(a1, encoding="utf-8")
        raise SystemExit("okuma: JSON ayrıştırılamadı")
    d1 = denetle(unit, data, texts)
    print(f"  çizelge: {d1['satir']} satır / {d1['kelime']} kelime; eksik {len(d1['eksik'])}, boş {len(d1['bos'])}, "
          f"sorunlu alıntı {len(d1['alinti_sorunlu'])}/{d1['alinti']}")
    steps = {"okuma": {"cost": cost1, "seconds": s1, "calls": c1, "denetim": d1}}
    logs = [Path(str(stem) + ".okuma.jsonl")]
    prompts = [p1]
    # 2. tamamla (bir kez)
    if d1["eksik"] or d1["bos"] or d1["alinti_sorunlu"]:
        p2 = (p1 + "\n\n---\n\n# Senin çizelgen\n\n```json\n" + json.dumps(data, ensure_ascii=False, indent=1)
              + "\n```\n\n---\n\n" + pp["TAMAMLA"].format(eksikler=eksik_text(d1)))
        a2, c2, cost2, s2, _ = call(unit, p2, Path(str(stem) + ".tamamla.jsonl"))
        fix = Y.extract_json(a2) or D.repair_json(a2)
        if fix:
            data = merge_rows(data, fix)
        d2 = denetle(unit, data, texts)
        print(f"  tamamlandıktan sonra: eksik {len(d2['eksik'])}, boş {len(d2['bos'])}, "
              f"sorunlu alıntı {len(d2['alinti_sorunlu'])}/{d2['alinti']}")
        steps["tamamla"] = {"cost": cost2, "seconds": s2, "calls": c2, "denetim": d2, "parsed": fix is not None}
        logs.append(Path(str(stem) + ".tamamla.jsonl"))
        prompts.append(p2)
    Path(str(stem) + ".cizelge.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    # 3. yazım
    md = render(unit, data)
    Path(str(stem) + ".cizelge.md").write_text(md, encoding="utf-8")
    p3 = yazim_prompt(unit, md)
    leak_ok = P.leak_report(unit, P.UNITS[unit], P.OUT / unit, p3, f"sizinti-cizelge-yazim-taslak-{n}.md")
    print(f"  yazım istemi {len(p3):,} harf; sızıntı testi {'temiz' if leak_ok else 'UYARI (okuma ezber getirmiş olabilir)'}")
    a3, c3, cost3, s3, rc3 = call(unit, p3, Path(str(stem) + ".yazim.jsonl"), only_cite=True)
    steps["yazim"] = {"cost": cost3, "seconds": s3, "calls": c3, "sizinti_temiz": leak_ok}
    logs.append(Path(str(stem) + ".yazim.jsonl"))
    prompts.append(p3)
    # taslak ve kayıtlar (D9.1 ve eşleştirme bunları okur)
    (keep / f"taslak-{n}.md").write_text(a3, encoding="utf-8")
    (keep / f"taslak-{n}.jsonl").write_text("".join(x.read_text(encoding="utf-8") for x in logs), encoding="utf-8")
    joined = "\n\n=====\n\n".join(prompts)
    (P.OUT / unit / P.istem_files("cizelge", SURUM)[0]).write_text(joined, encoding="utf-8")
    calls = Counter()
    for s in steps.values():
        calls.update(s["calls"])
    meta = {"model": OPUS, "effort": "high", "istem": "cizelge", "surum": SURUM, "taban_surum": H.SURUM,
            "istem_sha": sha, "prompt_sha": P._sha(joined), "seconds": sum(s["seconds"] for s in steps.values()),
            "returncode": rc3, "calls": dict(calls), "cost_usd": round(sum(s["cost"] or 0 for s in steps.values()), 4),
            "adimlar": steps, "at": datetime.now().isoformat()}
    (keep / f"taslak-{n}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"taslak {n}: {meta['seconds']} sn, ≈{meta['cost_usd']:.2f} $; Arapça {D.ar_chars(unit, n):,} harf")
    return n


# ---------------------------------------------------------------- ölçüler

PARTICLES = set(map(M.norm, "و ف ب ل ك س ان إن أن إنما انما إذا اذا ما لا في من إلا الا ثم أو بل قد لن لم ألا الا هم هو "
                    "على الى إلى عن مع كما لكن ولكن".split()))
HARF_NAMES = {"و": ("الواو", "واو"), "ف": ("الفاء", "فاء"), "ب": ("الباء", "باء"), "ل": ("اللام", "لام"),
              "ك": ("الكاف", "كاف"), "س": ("السين", "سين")}


def kapsam(unit: str, n: int) -> dict:
    """Âyetin kelimelerinden ve harflerinden kaçı taslağın V2/V3 Arapça paragraflarında **tek başına** ele alınıyor:
    en çok iki kelimelik bir ayraç (﴿…﴾, «…», "…") içinde ya da harfin adıyla ("الواو", "الفاء"). Cümlenin
    tamamını alıntılamak sayılmaz (T1'in ek ölçüsü, Z11: harfler ve küçük lafızlar)."""
    blocks, _ = Y.draft_blocks(unit, n)
    body = " ".join(t for a, lang, q, t in blocks if lang == "ar" and not q and a.split("/")[0] in ("V2", "V3"))
    spans = [next(g for g in s if g) for s in re.findall(r"﴿([^﴾]+)﴾|«([^»]+)»|\"([^\"]+)\"|“([^”]+)”", body)]
    focused = [[x for x in M.SEP.split(s) if M.norm(x)] for s in spans]
    focused = [f for f in focused if 1 <= len(f) <= 2]
    words = ayah_words(unit)
    seen = [w for w in words if any(same(x, w["lafiz"]) for f in focused for x in f)]
    parts_ = [w for w in words if w["norm"] in PARTICLES or (w["norm"][:1] in "وف" and w["norm"][1:] in PARTICLES)]
    att = [w for w in words if w["norm"][:1] in HARF_NAMES and len(w["norm"]) > 3 and w["norm"] not in PARTICLES]
    att_seen = [w for w in att if any(nm in body for nm in HARF_NAMES[w["norm"][0]])
                or any(len(f) == 1 and M.norm(f[0]) == w["norm"][0] for f in focused)]
    letters = sorted({w["norm"][0] for w in att})
    return {"kelime": len(words), "kelime_tek_basina": len(seen), "edat": len(parts_),
            "edat_tek_basina": sum(1 for w in parts_ if w in seen), "bitisik_harf": len(att),
            "bitisik_harf_anilan": len(att_seen), "harf_adlari": {h: any(nm in body for nm in HARF_NAMES[h]) for h in letters},
            "tek_basina_anilmayan": [w["lafiz"] for w in words if w not in seen]}


def run_cmd(args: list[str]) -> None:
    print("$", " ".join(args), flush=True)
    subprocess.run(["uv", "run", "python", *args], cwd=ROOT, check=True)


def olc(unit: str, tur: str, taban: int, yeni: int) -> None:
    run_cmd(["scripts/d1-yz.py", "eslestir", unit, "--taslak", str(taban), str(yeni), "--modeller", "opus"])
    run_cmd(["scripts/d1-yz.py", "rapor", unit])
    run_cmd(["scripts/d1-elestiri.py", "mekanik", unit, "--taslak", str(taban), str(yeni)])
    run_cmd(["scripts/d1-duzelt.py", "olc", unit, "--cift", f"{taban}-{yeni}"])
    sayilar(unit, tur, taban, yeni)


# D13: me'haz dağılımı (kullanıcının kararı, 2026-11-17: taslak İşârât ve Risale-i Nur'dan mı, müfessirlerden mi konuşuyor)
MUFESSIR_ADLARI = ("أبو السعود", "أبي السعود", "الآلوسي", "الألوسي", "الرازي", "الزمخشري", "الكشاف", "البيضاوي",
                   "الطبري", "القرطبي", "ابن كثير", "الماتريدي", "النسفي", "البروسوي", "حقي", "الجلالين", "السيوطي")


def _kind(server: str | None, work: str) -> str:
    if server == "risale":
        return "isarat" if work.startswith("isaratul-icaz") else "risale"
    if server == "tefsir":
        return "kessaf" if work == "kessaf" else "tefsir"
    return {"klasik": "belagat", "hadis": "hadis"}.get(server or "", "bilinmeyen")


def mehaz(unit: str, n: int) -> dict:
    """Taslağın me'haz dağılımı: atıfların kaynak türüne göre sayısı (metindeki her [n] geçişi), Arapça metinde
    (alıntılar hariç) müfessir adı ve İşârât adı, Risale-i Nur'a (İşârât dışı) dayanan paragraf çifti, blok alıntılar."""
    blocks, _ = Y.draft_blocks(unit, n)
    ids = dict(P.draft_sources(P.DRAFTS / unit / f"taslak-{n}.jsonl"))
    kp = P.DRAFTS / unit / f"taslak-{n}.kaynak.json"
    if kp.exists():
        ids.update({k: tuple(v) for k, v in json.loads(kp.read_text(encoding="utf-8")).items()})
    kind_of = {k: _kind(sv, (sid or "").split("/")[0]) for k, (sv, sid) in ids.items()}
    pr = Y.pairs(blocks)

    def nums(t: str) -> list[str]:
        return [x for m in re.finditer(r"\[([^\[\]\n]{1,80})\]", t) for x in re.findall(r"\d+", m.group(1))]

    atif, alinti = Counter(), Counter()
    for a, lang, q, t in blocks:
        for k in nums(t):
            atif[kind_of.get(k, "bilinmeyen")] += 1
        if q and lang == "ar":
            alinti[next((kind_of.get(k, "bilinmeyen") for k in nums(t)), "numarasiz")] += 1
    own_ar = " ".join(t for a, lang, q, t in blocks if lang == "ar" and not q)
    by = {a: t for a, _, _, t in blocks}
    risale_par = sum(1 for a, lang, q, t in blocks if lang == "ar" and not q
                     and any(kind_of.get(k) == "risale" for k in nums(t + " " + by.get(pr.get(a, ""), ""))))
    ar_par = sum(1 for a, lang, q, t in blocks if lang == "ar" and not q)
    return {"atif": dict(atif), "blok_alinti": dict(alinti),
            "mufessir_adi_ar": sum(own_ar.count(x) for x in MUFESSIR_ADLARI),
            "isarat_adi_ar": own_ar.count("الإشارات") + own_ar.count("إشارات الإعجاز"),
            "risale_paragraf": risale_par, "arapca_paragraf": ar_par}


def sayilar(unit: str, tur: str, taban: int, yeni: int) -> dict:
    out = {"birim": unit, "tur": tur, "taban": taban, "yeni": yeni, "taslaklar": {}}
    h = H.hedef(unit)
    for n in (taban, yeni):
        meta = json.loads((P.DRAFTS / unit / f"taslak-{n}.json").read_text(encoding="utf-8"))
        mek = json.loads((Y.out_dir(unit) / f"mekanik-taslak-{n}.json").read_text(encoding="utf-8"))
        t = mek["tirnak"]
        out["taslaklar"][n] = {
            "istem": f"{meta.get('istem')} {meta.get('surum')}", "maliyet": meta.get("cost_usd"),
            "sure": meta.get("seconds"), "arac": sum((meta.get("calls") or {}).values()),
            "ar_harf": D.ar_chars(unit, n), "hedef": [h["en_az"], h["en_cok"]],
            "kapsama": D.coverage(unit, n), "kelime_kapsami": kapsam(unit, n),
            "tirnak_tr_bulunmadi": sum(1 for x in t if x["tur"] == "satir_ici" and x["dil"] == "tr" and x["durum"] == "bulunmadi"),
            "tirnak_ar_nisbetli_yok": sum(1 for x in t if x["dil"] == "ar" and x["durum"] == "bulunmadi"
                                          and (x.get("nisbet") or x["tur"] == "blok")),
            "takdir": sum(1 for x in t if x["tur"] == "takdir"),
            "kendi_tespiti_adayi": sum(1 for x in mek["ortak"] if x["tur"] == "kendi_tespiti"),
            "kapsam_adayi": len(mek.get("kapsam", [])),
            "numara_sorunu": len(mek["numaralar"]["metinde_kaynakcada_yok"]) + len(mek["numaralar"]["metinde_cite_yok"]),
            "mehaz": mehaz(unit, n),
        }
        if meta.get("adimlar"):
            out["taslaklar"][n]["adimlar"] = {k: {"cost": v["cost"], "seconds": v["seconds"],
                                                  "denetim": {kk: (len(vv) if isinstance(vv, list) else vv)
                                                              for kk, vv in (v.get("denetim") or {}).items()}}
                                              for k, v in meta["adimlar"].items()}
    kor = Y.out_dir(unit) / f"kor-olcu-{taban}-{yeni}"
    if Path(str(kor) + ".json").exists():
        km = json.loads(Path(str(kor) + ".meta.json").read_text(encoding="utf-8"))
        kd = json.loads(Path(str(kor) + ".json").read_text(encoding="utf-8"))
        who = {"A": km["A"], "B": km["B"], "esit": "esit"}
        out["kor"] = {"A": km["A"], "B": km["B"], "maliyet": km.get("cost_usd"), "surum": km.get("surum"),
                      "butun": dict(kd.get("butun", {}), taslak=who.get(kd.get("butun", {}).get("tercih"))),
                      **({"mehaz": dict(kd["mehaz"], taslak=who.get(kd["mehaz"].get("tercih")))} if kd.get("mehaz") else {}),
                      "bolumler": [dict(b, taslak=who.get(b.get("tercih"))) for b in kd.get("bolumler", [])],
                      "yalniz_A": kd.get("yalniz_A_kusurlari", []), "yalniz_B": kd.get("yalniz_B_kusurlari", [])}
    path = P.DRAFTS / unit / f"d12-5-{tur}-sayilar.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1)[:6000])
    return out


# ---------------------------------------------------------------- tur okuması (masa)

# ---------------------------------------------------------------- tur okuması (standart, 2026-11-17)
# Plan belgesi 4.10 "Okuma standardı" (kullanıcının kararları): turda tek sayfa `masa/tur-<birim>-<tur>.html`; bir yer
# envanterin tek bir nüktesidir; yan başına en çok 2 paragraf ve ≈250 kelime (Türkçe; Türkçesi yoksa Arapça); Türkçe
# önde, Arapça açılır kutuda; sarı fark yalnız düzeltme turunda (D); İşârât'ın sözü "Aç"tan sonra.

READ_MAX_PARAS, READ_MAX_WORDS = 2, 250
READ_KINDS = {"hipotez": "değişikliğin sınandığı yer", "ayrilik": "iki ölçünün ayrıldığı yer",
              "elestirmen": "kör eleştirmenin açık hüküm verdiği yer"}
TUR_GIRIS = ("<b>Ne okuyorsunuz:</b> aynı âyetler için iki yapay zekâ taslağı, <b>A</b> ve <b>B</b>; hangisinin nasıl "
             "yazıldığı gizli. Her kart İşârât'ın tek bir nüktesinin yeridir: her taslaktan o nükteyi işleyen paragraflar "
             "(en çok iki), Türkçesiyle; Arapçası altında açılır. Her kartta <b>hangisi daha iyi</b> (doğruluk, "
             "İşârât'a yakınlık, kaynak disiplini, îcâz) ve bir iki cümle gerekçe; sonra <b>Aç</b>: hangisi hangisi, "
             "ölçülerin dediği ve İşârât'ın o yerdeki sözü. Bitince <b>Dışa aktar</b>.")
TUR_GIRIS_D = ("<b>Ne okuyorsunuz:</b> aynı taslağın iki düzeltilmiş hâli, <b>A</b> ve <b>B</b>; hangisinin nasıl "
               "düzeltildiği gizli. Her kart İşârât'ın tek bir nüktesinin yeridir: her hâlden o nükteyi işleyen "
               "paragraflar (en çok iki), Türkçesiyle; Arapçası altında açılır. <b>Sarı</b>: öbür hâlde karşılığı "
               "olmayan kelimeler (değişen yer). Her kartta <b>hangisi daha iyi</b> (doğruluk, İşârât'a yakınlık, "
               "kaynak disiplini, îcâz, kendi sözü) ve bir iki cümle gerekçe; sonra <b>Aç</b>. Bitince <b>Dışa aktar</b>.")


def read_side(unit: str, n: int, nid: str, rows: dict, sources: dict) -> dict:
    """Bir taslağın o nükteyi işleyen paragrafları (eşleştiricinin çapaları), eşleriyle; sınır `READ_MAX_*`."""
    blocks, _ = Y.draft_blocks(unit, n)
    pr, by = Y.pairs(blocks), {a: (lang, q, t) for a, lang, q, t in blocks}
    order = {a: i for i, (a, *_) in enumerate(blocks)}
    row = {m: x for m, x in (rows.get(nid) or {}).items() if isinstance(x, dict)}   # okuyucu başına {d, a}
    durum = {m: (x or {}).get("d") for m, x in row.items()}
    anchors = sorted({Y.ar_of(pr, a) for x in row.values() if x for a in x.get("a") or [] if a in by},
                     key=lambda a: order[a])
    paras, words = [], 0
    for a in anchors:
        lang, q, t = by[a]
        tr = by[pr[a]][2] if a in pr and lang == "ar" else (t if lang == "tr" else "")
        ar = t if lang == "ar" else ""
        paras.append({"a": a, "q": q, "ar": ar, "tr": tr})
        words += len((tr or ar).split())
    nums = sorted({x for p in paras for m in re.finditer(r"\[([^\[\]\n]{1,80})\]", p["ar"] + " " + p["tr"])
                   for x in re.findall(r"\d+", m.group(1))}, key=int)
    srcs = {k: {"c": sources[k]["c"], "t": (sources[k]["t"] or "")[:1500]} for k in nums if k in sources}
    return {"paras": paras, "words": words, "durum": durum, "sources": srcs}


def okuma(unit: str, tur: str, taban: int, yeni: int, yerler: list[dict], sari: bool = False) -> Path:
    """Turun okuma sayfası (standart): `provalar/<birim>/tur-<tur>.json` ve `masa/tur-<birim>-<tur>.html`.

    `yerler`: [{id: envanter kalemi, tur: hipotez|ayrilik|elestirmen, baslik, soru, acik}]; soru nükteyi söylemez
    (İşârât'ın sözü "Aç"tan sonra). Sınırı aşan yer kabul edilmez: başka nükte seçilir.
    """
    order = [taban, yeni]
    random.Random(f"d12-5-{unit}-{tur}").shuffle(order)
    env = json.loads((Y.out_dir(unit) / "envanter.json").read_text(encoding="utf-8"))
    items = {i["id"]: i for i in env["kalemler"]}
    h = Y.hidden(unit)
    pd = Y.page_data(unit)
    ayah = M.Ayah(unit)
    dr = M.drafts(unit, ayah)
    cards, bad = [], []
    for y in yerler:
        it = items[y["id"]]
        sides = {}
        for lab, n in zip("AB", order):
            dk = f"taslak-{n}"
            sides[lab] = read_side(unit, n, y["id"], pd["drafts"][dk]["rows"], dr[dk]["sources"])
            sd = sides[lab]
            if len(sd["paras"]) > READ_MAX_PARAS or sd["words"] > READ_MAX_WORDS:
                bad.append(f"{y['id']} {lab}: {len(sd['paras'])} paragraf, {sd['words']} kelime")
        cards.append(dict(y, tur_ad=READ_KINDS[y["tur"]], nukte=it["nukte"], lafiz=it.get("lafiz", ""),
                          isarat_ar=Y.hidden_text(h, it.get("ar") or []), isarat_tr=Y.hidden_text(h, it.get("tr") or []),
                          A=sides["A"], B=sides["B"]))
    if bad:
        raise SystemExit("okuma sınırını aşan yer (yan başına 2 paragraf, 250 kelime): " + "; ".join(bad))
    words = sum(c[s]["words"] for c in cards for s in "AB")
    page = f"tur-{unit}-{tur}.html"
    data = {"ad": tur, "a": f"taslak-{order[0]}", "b": f"taslak-{order[1]}", "taban": f"taslak-{taban}",
            "yeni": f"taslak-{yeni}", "giris": TUR_GIRIS_D if sari else TUR_GIRIS, "sayfa": page, "kelime": words,
            "sari": sari,
            "dakika": round(words / 100 + 2 * len(cards)),
            "yerler": [{k: c[k] for k in ("id", "tur", "baslik", "soru", "acik")} for c in cards],
            "at": datetime.now().isoformat()}
    path = P.DRAFTS / unit / f"tur-{tur}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    page_data = dict(data, unit=unit, title=M.title(unit), masa=f"{unit}.html", cards=cards,
                     about={k: dr[k]["about"] for k in (data["a"], data["b"])})
    blob = json.dumps(page_data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    out = M.OUT_DIR / page
    out.write_text(READ_TEMPLATE.read_text(encoding="utf-8").replace("{data}", blob), encoding="utf-8")
    print(f"{path.relative_to(ROOT)}: A = {data['a']}, B = {data['b']}")
    print(f"{out.relative_to(ROOT)}: {len(cards)} yer, ≈{words} kelime, ≈{data['dakika']} dk; " + "; ".join(
        f"{c['id']} A {len(c['A']['paras'])}/{c['A']['words']}, B {len(c['B']['paras'])}/{c['B']['words']}" for c in cards))
    return out


READ_TEMPLATE = Path(__file__).with_name("d1-tur-okuma-sablon.html")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("hazirla", "yaz"):
        p = sub.add_parser(name)
        p.add_argument("unit", choices=P.UNITS)
        if name == "yaz":
            p.add_argument("--n", type=int, help="taslak numarası (taban aynı anda yazılıyorsa)")
    p = sub.add_parser("kapsam")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--taslak", type=int, nargs="+", required=True)
    for name in ("olc", "sayilar"):
        p = sub.add_parser(name)
        p.add_argument("unit", choices=P.UNITS)
        p.add_argument("--tur", required=True)
        p.add_argument("--taban", type=int, required=True)
        p.add_argument("--yeni", type=int, required=True)
    p = sub.add_parser("okuma")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--tur", required=True)
    p.add_argument("--taban", type=int, required=True)
    p.add_argument("--yeni", type=int, required=True)
    p.add_argument("--yerler", required=True, help="JSON: [{id: envanter kalemi, tur, baslik, soru, acik}]")
    p.add_argument("--sari", action="store_true", help="sarı fark (yalnız D turu: aynı taslağın iki düzeltmesi)")
    a = ap.parse_args()
    if a.cmd == "hazirla":
        hazirla(a.unit)
    elif a.cmd == "yaz":
        yaz(a.unit, a.n)
    elif a.cmd == "kapsam":
        for n in a.taslak:
            print(n, json.dumps(kapsam(a.unit, n), ensure_ascii=False))
    elif a.cmd == "olc":
        olc(a.unit, a.tur, a.taban, a.yeni)
    elif a.cmd == "okuma":
        okuma(a.unit, a.tur, a.taban, a.yeni, json.loads(Path(a.yerler).read_text(encoding="utf-8")), a.sari)
        run_cmd(["scripts/d1-masa.py", a.unit])
    elif a.cmd == "sayilar":
        sayilar(a.unit, a.tur, a.taban, a.yeni)


if __name__ == "__main__":
    main()
