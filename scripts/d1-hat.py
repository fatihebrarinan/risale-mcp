"""D11 üretim hattı (PLANLAR.md D11): birim başına tek, kısa, ucuz taslak; Arapça, tercüme ve izah.

    uv run python scripts/d1-hat.py dosya 31-33            # kaynak dosyası: data/interim/d1-prova/<birim>/dosya.md
    uv run python scripts/d1-hat.py hazirla 31-33          # kısa istem + dosya, sızıntı testi (istem-hat-h1.md)
    uv run python scripts/d1-hat.py yazdir 31-33 [--model claude-opus-5-5]   # taslak (d1-prova.yazdir, istem "hat")
    uv run python scripts/d1-hat.py izah 31-33 --taslak 7  # günümüz Türkçesiyle izah, paragraf paragraf
    uv run python scripts/d1-hat.py bolum 31-33 --taslak 7 3   # bölüm bölüm eleştiri (eleştirmen v1.2'nin soruları)
    uv run python scripts/d1-hat.py rapor 31-33 --taslak 7      # pilotun raporu: provalar/<birim>/d11-rapor.md

Kararlar (kullanıcıyla, 2026-11-15):
- **Kaynak dosyası** programla toplanır (âyet masasının fonksiyonlarıyla): altı taslağın hepsinin okuduğu müfessirlerin
  birimleri tam (`DOSYA_TEFSIR`), İşârât'ın önceki birimi (D5'te İşârât'ın kendisi ya da önceki taslak), Risale'de
  âyetin geçtiği yerler bir cümle bağlamla (yalnız âyetten ibaret dua ve hatime cümleleri sayıyla), klasik eserlerde
  âyetten üç kelimelik dizinin geçtiği yerler. Araçla arama kısıtlanmaz; model eksik gördüğünü okur.
- **Uzunluk:** Arapçada İşârât'ın 1–2 katı. Hedef birimde İşârât'ın Arapça uzunluğundan; D5'te İşârât olmadığı için
  `uzunluk_orani` (Bakara 8–33'te âyetin kelimesi başına İşârât'ın harfi) raporda karşılaştırılır.
- **İzah** ayrı adımda: yalnız paragrafın Arapçası ve tercümesi; taslağın söylemediğini söylemez, [n] ve tırnak eklemez.
- **Bölüm eleştirisi:** eleştirmen v1.2'nin istemi aynen, yalnız "# Taslak" kısmında bir bölüm ve D7 ile D9.1'in o
  bölüme düşen bulguları; bölümler ayrı çağrı, sonuçlar tek dosyada birleşir.
"""

import argparse
import importlib.util
import json
import re
import sqlite3
import statistics
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

from risale_mcp.paths import ROOT


def _load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M = _load("d1_masa", "d1-masa.py")          # Y (d1-yz) ve P (d1-prova) onun içinde
Y = M.Y
P = Y.P
E = _load("d1_elestiri", "d1-elestiri.py")

HAT_PROMPT = ROOT / "docs" / "d1" / "hat-istemi.md"
IZAH_PROMPT = ROOT / "docs" / "d1" / "izah-istemi.md"
SURUM = "h1"
# altı taslağın hepsinin okuduğu müfessirler (D8, 31–33); öbürleri araçla
DOSYA_TEFSIR = ("kessaf", "beyzavi", "ebussuud", "alusi")
# usul özetinden kısa isteme giren bölümler: "Bir âyette izlenen sıra" ve "Mukaddime ne zaman gelir"
OZET_BOLUM = ("## 4. Bir âyette izlenen sıra", "## 5. Mukaddime ve meseleler ne zaman gelir")


def out_dir(unit: str) -> Path:
    return P.OUT / unit


# ---------------------------------------------------------------- uzunluk

def uzunluk_orani() -> dict:
    """İşârât'ın Bakara birimlerinde âyetin kelimesi başına Arapça harf (8. âyetten sonra: sabit düzen)."""
    conn = sqlite3.connect(f"file:{P.GENEL_DB}?mode=ro", uri=True)
    rows = []
    for (nid,) in conn.execute("SELECT id FROM nodes WHERE parent_id = 'isaratul-icaz-arabi/sure-i-bakara' ORDER BY ord"):
        m = re.match(r"(\d+)(?:-(\d+))?", nid.rsplit("/", 1)[1])
        a, b = int(m.group(1)), int(m.group(2) or m.group(1))
        chars = conn.execute("SELECT sum(length(text)) FROM sentences WHERE node_id = ? OR node_id LIKE ?",
                             (nid, nid + "/%")).fetchone()[0] or 0
        words = sum(len(t.split()) for (t,) in conn.execute(
            "SELECT text FROM quran_ayahs WHERE sura = 2 AND ayah BETWEEN ? AND ?", (a, b)))
        rows.append({"birim": f"{a}" if a == b else f"{a}-{b}", "harf": chars, "ayet_kelime": words,
                     "oran": round(chars / words)})
    ratios = [r["oran"] for r in rows if int(r["birim"].split("-")[0]) >= 8]
    return {"birimler": rows, "medyan": round(statistics.median(ratios)), "en_az": min(ratios), "en_cok": max(ratios)}


def hedef(unit: str) -> dict:
    cfg = P.UNITS[unit]
    rows = [t for sid, t in P.hidden_sentences(cfg) if sid.startswith("isaratul-icaz-arabi/")]
    chars = sum(len(t) for t in rows)
    return {"isarat_harf": chars, "en_az": chars, "en_cok": 2 * chars,
            "kelime_az": round(chars / 5.5 / 10) * 10, "kelime_cok": round(2 * chars / 5.5 / 10) * 10}


# ---------------------------------------------------------------- kaynak dosyası

def _isarat_prev(unit: str) -> str:
    """İşârât'ın sınanan birimden önceki birimi, Arapça asıl, cümle kimlikleriyle (prova veritabanından)."""
    cfg = P.UNITS[unit]
    prev = {"31-33": "isaratul-icaz-arabi/sure-i-bakara/30", "11-12": "isaratul-icaz-arabi/sure-i-bakara/9-10-ayetlerin-tefsiri"}[unit]
    conn = sqlite3.connect(out_dir(unit) / "risale.db")
    nodes = [r for r in conn.execute("SELECT id, ref FROM nodes WHERE id = ? OR id LIKE ? ORDER BY ord", (prev, prev + "/%"))]
    L = []
    for nid, ref in nodes:
        L.append(f"\n#### {ref}  (`{nid}`)")
        para = None
        for sid, pid, text in conn.execute("SELECT id, paragraph_id, text FROM sentences WHERE node_id = ? ORDER BY seq",
                                           (nid,)):
            if pid != para:
                L.append("")
                para = pid
            L.append(f"[{sid[len(nid) + 1:]}] {text}")
    return "\n".join(L).strip()


def _is_formula(text: str) -> bool:
    """Âyetten ibaret cümle (risalelerin sonundaki "سبحانك لا علم لنا…" gibi): Türkçe kelimesi yok denecek kadar az."""
    letters = [c for c in text if c.isalpha()]
    latin = sum(c.isascii() or c in "çğıöşüâîûÇĞİÖŞÜÂÎÛ" for c in letters)
    return latin < 25


def dosya(unit: str) -> Path:
    cfg = P.UNITS[unit]
    ayah = M.Ayah(unit)
    L = [f"# Kaynak dosyası: {cfg['sura_name']} {'–'.join(map(str, cfg['ayahs']))}", "",
         "Program topladı (bu birim için; senin araştırman değil). Her cümlenin başında kimliği: `cite` ve `get_passage` "
         "bu kimliklerle çalışır. Burada olmayanı eklentilerde oku: öbür müfessirler (Taberî, Mâtürîdî, Râzî, Kurtubî, "
         "Nesefî, İbn Kesîr, Celâleyn, Süyûtî, Bursevî), İşârât'ın öbür birimleri, Risale'nin bölümlerinin tamamı, "
         "hadis kitapları, klasik eserlerin öbür yerleri.", ""]
    L += ["## Âyetler", ""]
    for v in ayah.verses:
        L += [f"> {v['text']} ({v['ref']})", f"> Meâl ({v['meal_by']}): {v['meal']}", ""]
    L += ["## Müfessirler: bu âyetlerdeki birimleri (tam)", ""]
    for w in M.tefsir(unit):
        if w["work"] not in DOSYA_TEFSIR:
            continue
        for u in w["units"]:
            L += [f"### {w['author']}, {w['title']}: {u['ref']}  (`{u['id']}`)", ""]
            for r in u["rows"]:
                L.append(" ".join(f"[{s['id']}] {s['t']}" for s in r.get("s", [])) if r.get("s") else r.get("t", ""))
                L.append("")
    L += ["## İşârâtü'l-İ'câz: önceki birim (Arapça asıl)", "", _isarat_prev(unit), ""]
    rs = M.risale(unit)
    formula = [r for r in rs if all(_is_formula(s["t"]) for s in r["s"] if s["id"] == r["id"])]
    L += ["## Risale-i Nur: âyetin geçtiği yerler (bir cümle bağlamla)", ""]
    try:
        links = []
        conn = sqlite3.connect(out_dir(unit) / "risale.db")
        a, b = cfg["ayahs"]
        links = conn.execute("SELECT kind, strength, node_id, evidence_id, ayah_start, ayah_end FROM ayah_links "
                             "WHERE sura = ? AND ayah_start <= ? AND ayah_end >= ?", (cfg["sura"], b, a)).fetchall()
    except sqlite3.Error:
        pass
    if links:
        L += ["Âyetle bağ kuran yerler (kural çıkardı; tür ve güç):", ""]
        L += [f"- `{n}` ({k}, {s}; kanıt `{e}`; âyet {x}–{y})" for k, s, n, e, x, y in links] + [""]
    gconn = sqlite3.connect(f"file:{P.GENEL_DB}?mode=ro", uri=True)
    heads_done = set()
    for r in rs:
        if r in formula:
            continue
        seq, node = gconn.execute("SELECT seq, node_id FROM sentences WHERE id = ?", (r["id"],)).fetchone()
        L += [f"### {r['ref']} (âyet {r['ayah']})", ""]
        if node not in heads_done:          # bölümün ana tezi: başlığı, alt başlığı ve ilk üç cümlesi
            heads_done.add(node)
            ref, sub = gconn.execute("SELECT ref, subtitle FROM nodes WHERE id = ?", (node,)).fetchone()
            first = gconn.execute("SELECT id, text, seq FROM sentences WHERE node_id = ? ORDER BY seq LIMIT 3",
                                  (node,)).fetchall()
            head = [f"[{i}] {t}" for i, t, s in first if s < seq - 2]   # bağlamla örtüşmeyenler
            L += [f"Bölüm: {ref}" + (f" ({sub})" if sub else "") + f"; baştan sona `read_section {node}`.", ""]
            if head:
                L += ["Bölümün başı:"] + head + ["", "Âyetin geçtiği yer:"]
        ctx = gconn.execute("SELECT id, text FROM sentences WHERE node_id = ? AND seq BETWEEN ? AND ? ORDER BY seq",
                            (node, seq - 2, seq + 2)).fetchall()
        L += [f"[{i}] {t}" for i, t in ctx] + [""]
    if formula:
        L += [f"Âyet ayrıca {len(formula)} yerde yalnız kendisi olarak geçer (risale sonlarında dua ve hatime): "
              + ", ".join(f"`{r['id']}`" for r in formula), ""]
    L += ["## Klasik eserler: âyetten üç kelimelik bir dizinin geçtiği yerler", ""]
    for k in M.klasik(ayah):
        L += [f"### {k['author']}, {k['title']}: {k['ref']}", ""] + [f"[{s['id']}] {s['t']}" for s in k["s"]] + [""]
    path = out_dir(unit) / "dosya.md"
    path.write_text("\n".join(L), encoding="utf-8")
    sizes = {}
    cur = None
    for line in L:
        if line.startswith("## "):
            cur = line[3:]
        sizes[cur] = sizes.get(cur, 0) + len(line) + 1
    print(f"{path.relative_to(ROOT)}: {path.stat().st_size // 1024} KB, {len(''.join(L)):,} harf")
    for k, v in sizes.items():
        print(f"  {v:7,}  {k}")
    return path


# ---------------------------------------------------------------- istem

def _section(text: str, start: str, end: str | None) -> str:
    i = text.index(start)
    j = text.index(end, i) if end else len(text)
    return text[i:j].strip()


def hazirla(unit: str) -> Path:
    cfg = P.UNITS[unit]
    out = out_dir(unit)
    if not (out / "risale.db").exists():
        sys.exit("önce: uv run python scripts/d1-prova.py hazirla <birim> (prova veritabanları)")
    dosya_path = dosya(unit)
    ozet = P.apply_edits(P.OZET.read_text(encoding="utf-8"), cfg["ozet"], "özet")
    cizelge = P.apply_edits(P.CIZELGE.read_text(encoding="utf-8"), cfg["cizelge"], "çizelge")
    ek1 = _section(ozet, OZET_BOLUM[0], "## 6. Anlatım biçimi")
    ek2 = _section(cizelge, "## Çizelge: Bakara", "## Çizelge: Fâtiha")
    h = hedef(unit)
    body = HAT_PROMPT.read_text(encoding="utf-8").split("---- İSTEM ----", 1)[1].strip()
    body = body.format(sura_name=cfg["sura_name"], ayahs="–".join(map(str, cfg["ayahs"])),
                       en_az=f"{h['en_az']:,}".replace(",", "."), en_cok=f"{h['en_cok']:,}".replace(",", "."),
                       kelime_az=f"{h['kelime_az']:,}".replace(",", "."), kelime_cok=f"{h['kelime_cok']:,}".replace(",", "."))
    prompt = (f"{body}\n\n---\n\n# Ek 1: Usul özeti, 4. ve 5. bölüm (prova kopyası)\n\n{ek1}\n\n---\n\n"
              f"# Ek 2: Birim çizelgesi, Bakara (prova kopyası)\n\n{ek2}\n\n---\n\n# Ek 3: "
              + dosya_path.read_text(encoding="utf-8").removeprefix("# "))
    name, report = P.istem_files("hat", SURUM)
    (out / name).write_text(prompt, encoding="utf-8")
    print(f"istem: {len(prompt):,} harf (gövde {len(body):,}, Ek 1 {len(ek1):,}, Ek 2 {len(ek2):,}); hedef {h}")
    ok = P.leak_report(unit, cfg, out, prompt, report)
    print(f"sızıntı testi: {'temiz' if ok else 'SORUN'} → {(out / report).relative_to(ROOT)}")
    if not ok:
        sys.exit(1)
    return out / name


# ---------------------------------------------------------------- izah

QUOTE_RE = re.compile(r"«([^»]+)»|“([^”]+)”|\"([^\"]+)\"")


def izah(unit: str, n: int, again: bool = False) -> dict | None:
    cfg = P.UNITS[unit]
    stem = Y.out_dir(unit) / f"izah-taslak-{n}"
    if stem.with_suffix(".json").exists() and not again:
        print(f"{stem.name}: var (--yeniden)")
        return json.loads(stem.with_suffix(".json").read_text(encoding="utf-8"))
    blocks, sources = Y.draft_blocks(unit, n)
    raw = IZAH_PROMPT.read_text(encoding="utf-8").split("---- İZAH ----", 1)[1].strip()
    text = raw.format(sura_name=cfg["sura_name"], ayahs="–".join(map(str, cfg["ayahs"])),
                      taslak=Y.render_draft(blocks, {}))
    data = Y.run_model(text, "opus", stem, {"gorev": "izah", "taslak": n, "istem_sha": P._sha(raw)})
    if data is None:
        return None
    data["denetim"] = izah_check(blocks, data)
    stem.with_suffix(".json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    d = data["denetim"]
    print(f"  izah: {d['kayit']} kayıt, eksik {len(d['eksik'])}, fazla {len(d['fazla'])}, numara {len(d['numara'])}, "
          f"tırnak {len(d['tirnak'])}")
    return data


def izah_check(blocks: list, data: dict) -> dict:
    """İzahta taslakta olmayan [n] ve tırnak (paragraf çiftinde geçmeyen söz); eksik ve fazla çapalar."""
    text = {a: t for a, _, _, t in blocks}
    tr = [a for a, lang, q, _ in blocks if lang == "tr" and not q]
    got = {x.get("capa"): x.get("metin", "") for x in data.get("izah", [])}
    out = {"kayit": len(got), "eksik": [a for a in tr if a not in got], "fazla": [a for a in got if a not in text],
           "numara": [], "tirnak": []}
    for a, m in got.items():
        pair = text.get(a, "") + " " + text.get(a.replace("/tr/", "/ar/"), "")
        nums = set(re.findall(r"\[(\d+)", m)) - set(re.findall(r"\[(\d+)", pair))
        if nums:
            out["numara"].append({"capa": a, "n": sorted(nums)})
        for g in QUOTE_RE.finditer(m):
            q = next(x for x in g.groups() if x)
            if len(q.split()) >= 2 and not Y.quote_found(q, pair):
                out["tirnak"].append({"capa": a, "soz": q[:120]})
    return out


# ---------------------------------------------------------------- bölüm eleştirisi

BOLUM_NOT = """

# Bu çağrıda bakacağın bölüm: {baslik}

Taslağın tamamı yukarıda bağlam için duruyor; bu çağrıda **yalnız "{baslik}" bölümünü** eleştiriyorsun (çapaları
`{key}/…`). Aynı taslağın öbür bölümlerine ayrı çağrılar bakıyor. Bu bölümün paragraflarını **tek tek, yakından**
oku: her paragraf için yukarıdaki soruları sor; İşârât'ın bu bölüme düşen kısmıyla ve paragrafın dayandığı
kaynaklarla karşılaştır. Notlarını yalnız bu bölümün çapalarına yaz. Bir nükte bu bölümde yoksa ama taslağın başka bir
bölümünde varsa onu eksik sayma. `sistemli` ve `oneriler` alanlarına yalnız bu bölümden çıkanları yaz; `ozet` bu
bölümün özetidir. Çıktı biçimi yukarıdakinin aynısıdır."""


def _sections(unit: str, n: int) -> list[str]:
    blocks, _ = Y.draft_blocks(unit, n)
    keys = []
    for a, *_ in blocks:
        k = a.split("/")[0]
        if k != "Âyet" and k not in keys:
            keys.append(k)
    return keys


def bolum_run(unit: str, n: int, key: str, again: bool) -> dict | None:
    import os, subprocess, tempfile, time
    stem = Y.out_dir(unit) / f"bolum-elestiri-taslak-{n}-{key}"
    if stem.with_suffix(".json").exists() and not again:
        return json.loads(stem.with_suffix(".json").read_text(encoding="utf-8"))
    prompt, sha = E.critic_prompt(unit, n)
    prompt += BOLUM_NOT.format(baslik=P.SECTION_TITLES[key], key=key)
    mcp = E.critic_mcp(unit)
    env = {k: v for k, v in os.environ.items() if k not in P.PARENT_ENV}
    command = ["claude", "-p", "--model", Y.MODELS["opus"], "--effort", Y.EFFORT, "--output-format", "stream-json",
               "--verbose", "--mcp-config", str(mcp), "--strict-mcp-config", "--tools", "",
               "--allowedTools", ",".join(f"mcp__{s}" for s in E.CRITIC_SERVERS), "--no-session-persistence"]
    started = time.monotonic()
    print(f"{stem.name}: ({datetime.now():%H:%M})", flush=True)
    with tempfile.TemporaryDirectory(prefix="d1-bolum-") as tmp, stem.with_suffix(".jsonl").open("w") as log:
        done = subprocess.run(command, input=prompt, cwd=tmp, env=env, stdout=log, stderr=subprocess.PIPE, text=True,
                              timeout=Y.TIMEOUT, check=False)
    answer, calls, cost = P.transcript(stem.with_suffix(".jsonl"))
    data = Y.extract_json(answer)
    meta = {"model": Y.MODELS["opus"], "effort": Y.EFFORT, "istem_sha": sha, "taslak": n, "bolum": key,
            "seconds": round(time.monotonic() - started), "returncode": done.returncode, "calls": calls,
            "cost_usd": cost, "at": datetime.now().isoformat(), "parsed": data is not None}
    stem.with_suffix(".meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    if data is None:
        stem.with_suffix(".cevap.txt").write_text(answer, encoding="utf-8")
        print(f"  {stem.name}: JSON ayrıştırılamadı (çıkış {done.returncode})", flush=True)
        return None
    stem.with_suffix(".json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  {stem.name}: {meta['seconds']} sn, {len(data.get('notlar', []))} not" + (f", ≈{cost:.2f} $" if cost else ""),
          flush=True)
    return data


def check_notes(unit: str, n: int, notes: list, log: Path) -> None:
    """`d1-elestiri.check_critic`in aynısı, döküm dosyası verilerek (bölüm çağrısının okudukları)."""
    blocks, _ = Y.draft_blocks(unit, n)
    by_anchor = {a: t for a, _, _, t in blocks}
    whole = " ".join(by_anchor.values())
    read_ids = {k[1] for k in E.Read(log=log).items}
    conns: dict = {}
    for note in notes:
        q, capa = note.get("taslak_alinti"), note.get("capa") or "genel"
        d = {}
        if q:
            pair = [by_anchor.get(capa, ""), by_anchor.get(capa.replace("/tr/", "/ar/"), ""),
                    by_anchor.get(capa.replace("/ar/", "/tr/"), "")]
            d["alinti"] = Y.quote_found(q, " ".join(pair)) or ("baska_capada" if Y.quote_found(q, whole) else False)
        if capa != "genel":
            d["capa"] = capa in by_anchor
        bad, unread = [], []
        for sid in note.get("dayanak") or []:
            server = "risale" if sid.startswith("isaratul") else None
            if not any(E._exists(s, sid, conns) for s in ([server] if server else E.CRITIC_DBS)):
                bad.append(sid)
            elif not any(x == sid.partition("..")[0] or x.startswith(sid.partition("..")[0] + "#") for x in read_ids):
                unread.append(sid)
        d["dayanak_yok"], d["dayanak_okunmamis"] = bad, unread
        note["denetim"] = d


def bolum(unit: str, drafts: list[int], again: bool = False, parallel: int = 4) -> None:
    jobs = [(n, k) for n in drafts for k in _sections(unit, n)]
    with ThreadPoolExecutor(max_workers=parallel) as pool:
        results = list(pool.map(lambda j: (j, bolum_run(unit, j[0], j[1], again)), jobs))
    for n in drafts:
        merged = {"taslak": n, "bolumler": {}, "notlar": [], "sistemli": [], "oneriler": [], "ozet": {}}
        for (m, k), data in results:
            if m != n:
                continue
            if data is None:
                merged["bolumler"][k] = "basarisiz"
                continue
            notes = data.get("notlar", [])
            for x in notes:
                x["bolum"] = k
            check_notes(unit, n, notes, Y.out_dir(unit) / f"bolum-elestiri-taslak-{n}-{k}.jsonl")
            merged["bolumler"][k] = len(notes)
            merged["notlar"] += notes
            merged["sistemli"] += [dict(x, bolum=k) for x in data.get("sistemli", [])]
            merged["oneriler"] += [x if isinstance(x, dict) else {"metin": x, "bolum": k} for x in data.get("oneriler", [])]
            merged["ozet"][k] = data.get("ozet", "")
        (Y.out_dir(unit) / f"bolum-elestiri-taslak-{n}.json").write_text(
            json.dumps(merged, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"taslak {n}: bölüm eleştirisi {merged['bolumler']}, toplam {len(merged['notlar'])} not")


# ---------------------------------------------------------------- D11.3 süzgeç örneklemi

ORNEK_PER = 5          # taslak ve biçim başına (kullanıcının yükü: iki taslak × iki biçim × 5 = 20 not)


def orneklem(unit: str, drafts: list[int], again: bool = False) -> None:
    """Bütün ve bölüm eleştirisinden eşit, sabit tohumlu örneklem: övgü, "ehline sor" ve denetimde tutmayan hariç;
    türlere yayılarak. Kabul oranı × not sayısı, hangi biçimin daha çok geçerli not bulduğunu verir."""
    import random
    path = Y.out_dir(unit) / "d11-orneklem.json"
    if path.exists() and not again:
        print(f"{path.relative_to(ROOT)} var; korunuyor (--yeniden)")
        return
    rng = random.Random(f"d11-{unit}-orneklem")
    picked, havuz = [], {}
    for n in drafts:
        for mod, file, prefix in (("butun", f"elestiri-taslak-{n}.denetim.json", ""),
                                  ("bolum", f"bolum-elestiri-taslak-{n}.json", "b")):
            notes = json.loads((Y.out_dir(unit) / file).read_text(encoding="utf-8"))["notlar"]
            pool = [(i, x) for i, x in enumerate(notes) if x.get("tur") != "dogru" and not x.get("ehline_sor")
                    and (x.get("denetim") or {}).get("alinti") is not False and not (x.get("denetim") or {}).get("dayanak_yok")]
            havuz[f"taslak-{n}/{mod}"] = len(pool)
            by_type = defaultdict(list)
            for i, x in pool:
                by_type[x.get("tur")].append((i, x))
            for xs in by_type.values():
                rng.shuffle(xs)
            got = []
            while len(got) < ORNEK_PER and any(by_type.values()):     # türlere sırayla: en kalabalıktan başla
                for t in sorted(by_type, key=lambda t: -len(by_type[t])):
                    if by_type[t] and len(got) < ORNEK_PER:
                        got.append(by_type[t].pop())
            for i, x in got:
                picked.append({"taslak": f"taslak-{n}", "k": prefix + Y.critic_key(n, x), "mod": mod, "sira": i,
                               "tur": x.get("tur"), "capa": x.get("capa"), "metin": x.get("metin", "")})
    rng.shuffle(picked)            # okuyan biçimi sıradan tahmin etmesin (masada etiket yine görünür)
    data = {"birim": unit, "at": datetime.now().isoformat(timespec="seconds"), "havuz": havuz, "notlar": picked,
            "aciklama": "D11.3: aynı iki taslağın (eski 3, pilot 7) bütün olarak ve bölüm bölüm eleştirisinden eşit örneklem"}
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{path.relative_to(ROOT)}: {len(picked)} not; havuz {havuz}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("dosya")
    p.add_argument("unit", choices=P.UNITS)
    p = sub.add_parser("oran")
    p = sub.add_parser("hazirla")
    p.add_argument("unit", choices=P.UNITS)
    p = sub.add_parser("yazdir")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--model", default="claude-opus-5-5")
    p.add_argument("--effort", default="high")
    p = sub.add_parser("izah")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--taslak", type=int, required=True)
    p.add_argument("--yeniden", action="store_true")
    p = sub.add_parser("bolum")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--taslak", type=int, nargs="+", required=True)
    p.add_argument("--yeniden", action="store_true")
    p = sub.add_parser("orneklem")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--taslak", type=int, nargs="+", required=True)
    p.add_argument("--yeniden", action="store_true")
    a = ap.parse_args()
    if a.cmd == "dosya":
        dosya(a.unit)
    elif a.cmd == "hazirla":
        hazirla(a.unit)
    elif a.cmd == "yazdir":
        P.yazdir(a.unit, 1, a.model, a.effort, "hat", SURUM)
    elif a.cmd == "izah":
        izah(a.unit, a.taslak, a.yeniden)
    elif a.cmd == "bolum":
        bolum(a.unit, a.taslak, a.yeniden)
    elif a.cmd == "orneklem":
        orneklem(a.unit, a.taslak, a.yeniden)
    elif a.cmd == "oran":
        print(json.dumps(uzunluk_orani(), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
