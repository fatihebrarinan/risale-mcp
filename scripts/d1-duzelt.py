"""D12.1 düzeltme deneyi (PLANLAR.md D12): kapalı kitap eleştiri, düzeltme, kör ölçü, iki eleştirmenin karşılaştırması.

    uv run python scripts/d1-duzelt.py kapali 31-33 --taslak 7          # kapalı kitap bölüm eleştirisi (prova sunucuları)
    uv run python scripts/d1-duzelt.py duzelt 31-33 --taslak 7 --notlar kapali   # yeni taslak (8): düzeltilmiş 7
    uv run python scripts/d1-duzelt.py duzelt 31-33 --taslak 7 --notlar acik     # yeni taslak (9): D11'in açık notlarıyla
    uv run python scripts/d1-duzelt.py olc 31-33 --cift 7-8 7-9 8-9     # kör A/B, açık kitap, bütün
    uv run python scripts/d1-duzelt.py notlar 31-33 --taslak 7          # iki eleştirmenin notları (araçsız)
    uv run python scripts/d1-duzelt.py rapor 31-33                      # provalar/<birim>/d12-1-sayilar.md
    uv run python scripts/d1-duzelt.py fark 31-33 --eski 7 --yeni 8     # D12.2 fark kartları (masa klasöründe)
    uv run python scripts/d1-duzelt.py ikinci 9-10 --taslak 3           # D turu (d2): düzeltmenin değiştirdiği yerlere ikinci eleştiri
    uv run python scripts/d1-duzelt.py duzelt 9-10 --taslak 3 --notlar ikinci   # d2'nin ikinci geçişi

Kararlar (kullanıcı, 2026-11-16; PLANLAR.md D12):
- **Kapalı kitap eleştirmen** (`docs/d1/elestiri-kapali-istemi.md`) D5'in şartıyla çalışır: prova sunucuları
  (İşârât'ın sınanan birimi gizli, öbür her şey açık), D7 ve D9.1'in ipucu adayları yok (envanterden çıkar), ölçü
  usul özetinin 2–5. bölümleri, dil, belâgat ve kaynaklar. Bölüm bölüm (Mukaddime, V1, V2, V3; her çağrı taslağın
  tamamını görür, notu kendi bölümüne yazar). Her not bir yapılacak iş (`oneri`) ve öncelik taşır. İstem, eleştirmene
  gitmeden sızıntı testinden geçer.
- **Düzeltme** (`docs/d1/duzeltme-istemi.md`): aynı yazar (Opus 5.5, yüksek), yazarın isteminin aynısı (Ek 1–3 dahil)
  ve aynı prova sunucuları; taslak çapalarıyla, notlar numaralı. Yalnız değişen paragraflar (`degistir`, `sil`,
  `ekle`); her not ya bir değişiklikte ya gerekçeli retlerde. Program değişiklikleri asıl taslağın Markdown'una
  uygular: başlıklar, damga ve alıntı biçimi korunur; tercüme paragrafına damgayı program koyar. Yeni taslak bir
  sonraki numarayı alır; `taslak-<m>.json` asıl taslağın meta kaydıdır (istem ve özeti aynı: D9.1 aynı okunanlarla
  çalışsın) ve `duzeltme` alanı; `taslak-<m>.jsonl` asıl dökümle düzeltme dökümünün art arda eklenmişidir (okunanlar
  ikisinin birleşimi); kaynak numaralarının eşlemesi `taslak-<m>.kaynak.json` (asıl eşleme + düzeltmenin `cite`ları).
  Açık kitap notlarıyla düzeltme üst sınır koludur: notlar İşârât'ın gizli metnini taşır, bu taslağı envanter ve
  kullanıcı ölçer, açık eleştirmenin kör ölçüsü ona karşı taraflıdır.
- **Kör ölçü** (`docs/d1/kor-olcu-istemi.md`): yayındaki sunucularla (açık kitap), bütün olarak, iki taslak "A" ve
  "B" (sıra sabit tohumla karışık, kaydedilir); istem, model ve düzeltme bilgisi verilmez.
- **İki eleştirmenin karşılaştırması** (`docs/d1/not-karsilastirma-istemi.md`): açığın her notu kapalıyla eşleşiyor
  mu, eşleşmiyorsa "yalnız gizli metinden" mi "görülebilirdi" mi; kapalının tek kalan notları yerinde mi.
"""

import argparse
import difflib
import importlib.util
import json
import os
import random
import re
import subprocess
import tempfile
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

from risale_mcp.paths import ROOT


def _load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load("d1_hat", "d1-hat.py")
M, Y, P, E = H.M, H.Y, H.P, H.E

KAPALI_PROMPT = ROOT / "docs" / "d1" / "elestiri-kapali-istemi.md"
DUZELTME_PROMPT = ROOT / "docs" / "d1" / "duzeltme-istemi.md"
OLCU_PROMPT = ROOT / "docs" / "d1" / "kor-olcu-istemi.md"
NOT_PROMPT = ROOT / "docs" / "d1" / "not-karsilastirma-istemi.md"
IKINCI_PROMPT = ROOT / "docs" / "d1" / "elestiri-ikinci-istemi.md"
ISARAT_PROMPT = ROOT / "docs" / "d1" / "isarat-karsilastirma-istemi.md"
SURUM = {"kapali": "k2", "duzeltme": "d1", "olcu": "o3", "notlar": "n1", "ikinci": "i1", "isarat": "i1"}
PROVA_SERVERS = ("risale", "tefsir", "hadis", "klasik")
OPUS = "claude-opus-5-5"
STAMP = E.STAMP

KAPALI_BOLUM = """

# Bu çağrıda bakacağın bölüm: {baslik}

Taslağın tamamı yukarıda bağlam için duruyor; bu çağrıda **yalnız "{baslik}" bölümünü** eleştiriyorsun (çapaları
`{key}/…`). Aynı taslağın öbür bölümlerine ayrı çağrılar bakıyor. Bu bölümün paragraflarını **tek tek, yakından**
oku: her paragraf için yukarıdaki soruları sor; paragrafın dayandığı kaynakları aç. Notlarını yalnız bu bölümün
çapalarına yaz. Bir nükte bu bölümde yoksa ama taslağın başka bir bölümünde varsa onu eksik sayma. `sistemli`
alanına yalnız bu bölümden çıkanları yaz; `ozet` bu bölümün özetidir. Çıktı biçimi yukarıdakinin aynısıdır."""
# D15 (kullanıcının kararı, 2026-11-19): kör aletlerin ayarında kapalı eleştirmen bütün taslağa tek çağrıyla (ucuz;
# D5'te birim başına bu çalışacak). Notların bölümü çapadan.
KAPALI_BUTUN = """

# Bu çağrıda bakacağın yer: taslağın tamamı

Taslağın bütün bölümlerini (Mukaddime varsa, üç vecih ve dersler) bu tek çağrıda eleştiriyorsun. Paragrafları sırayla
oku, her biri için yukarıdaki soruları sor; dayandığı kaynakları aç. Önceliği yanlışlara, çelişkilere, yanlış
nisbetlere ve kaçan önemli nüktelere ver. Çıktı biçimi yukarıdakinin aynısıdır."""


def body(path: Path, marker: str) -> tuple[str, str]:
    raw = path.read_text(encoding="utf-8")
    return re.split(rf"^---- {marker} ----$", raw, maxsplit=1, flags=re.M)[1].strip(), P._sha(raw)


def ayahs(cfg: dict) -> str:
    return "–".join(map(str, cfg["ayahs"]))


def draft_text(unit: str, n: int, with_ids: bool = False) -> str:
    """Taslak çapalarıyla; tercüme paragraflarında damga (eleştirmen görsün); kaynakçada istenirse kimlikler."""
    blocks, sources = Y.draft_blocks(unit, n)
    stamped = {x["tr"] for x in E.draft(unit, n)["pairs"] if x.get("stamped")}
    blocks = [(a, lang, q, (STAMP + " " + t) if a in stamped else t) for a, lang, q, t in blocks]
    if with_ids:
        ids = P.draft_sources(P.DRAFTS / unit / f"taslak-{n}.jsonl")
        sources = {k: v + (f"  ⟨{ids[k][0]}: {ids[k][1]}⟩" if k in ids else "") for k, v in sources.items()}
    return Y.render_draft(blocks, sources)


def repair_json(answer: str) -> dict | None:
    """Modelin JSON'unda kaçırılmamış iç tırnaklar ("soruya cevap"): hata yerinden önceki tırnak kaçırılır, yeniden
    denenir. Yalnız tırnak onarılır; metin değişmez."""
    m = re.search(r"```(?:json)?\s*\n(.*?)\n```", answer, flags=re.S)
    s = m.group(1) if m else answer[answer.find("{"):answer.rfind("}") + 1]
    for _ in range(200):
        try:
            return json.loads(s)
        except json.JSONDecodeError as e:
            if "delimiter" not in e.msg:
                return None
            i = s.rfind('"', 0, e.pos)
            if i <= 0:
                return None
            s = s[:i] + '\\"' + s[i + 1:]
    return None


def run_claude(prompt: str, stem: Path, mcp: Path | None, allowed: tuple[str, ...], meta_extra: dict,
               model: str = OPUS, effort: str = "high") -> dict | None:
    """`claude -p` (yerleşik araçlar ve web kapalı); döküm `<stem>.jsonl`, meta `<stem>.meta.json`, cevap `<stem>.json`."""
    env = {k: v for k, v in os.environ.items() if k not in P.PARENT_ENV}
    command = ["claude", "-p", "--model", model, "--effort", effort, "--output-format", "stream-json", "--verbose",
               "--strict-mcp-config", "--tools", "", "--no-session-persistence"]
    if mcp:
        command += ["--mcp-config", str(mcp), "--allowedTools", ",".join(f"mcp__{s}" for s in allowed)]
    started = time.monotonic()
    print(f"{stem.name}: {model} ({datetime.now():%H:%M})", flush=True)
    log_path = Path(str(stem) + ".jsonl")
    with tempfile.TemporaryDirectory(prefix="d1-duzelt-") as tmp, log_path.open("w") as log:
        done = subprocess.run(command, input=prompt, cwd=tmp, env=env, stdout=log, stderr=subprocess.PIPE, text=True,
                              timeout=Y.TIMEOUT, check=False)
    answer, calls, cost = P.transcript(log_path)
    data = Y.extract_json(answer) or repair_json(answer)
    meta = {"model": model, "effort": effort, "seconds": round(time.monotonic() - started),
            "returncode": done.returncode, "calls": calls, "cost_usd": cost, "at": datetime.now().isoformat(),
            "prompt_chars": len(prompt), "parsed": data is not None, **meta_extra}
    if done.stderr.strip():
        meta["stderr"] = done.stderr.strip()[-2000:]
    Path(str(stem) + ".meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    if data is None:
        Path(str(stem) + ".cevap.txt").write_text(answer, encoding="utf-8")
        print(f"  {stem.name}: JSON ayrıştırılamadı ({meta['seconds']} sn, çıkış {done.returncode})", flush=True)
        return None
    Path(str(stem) + ".json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  {stem.name}: {meta['seconds']} sn, {sum(calls.values())} araç çağrısı"
          + (f", ≈{cost:.2f} $" if cost else ""), flush=True)
    return data


# ---------------------------------------------------------------- kapalı kitap eleştiri

def _bolum_of(capa: str | None) -> str:
    head = (capa or "").split("/", 1)[0]
    return head if head in P.SECTION_TITLES else "genel"


def mekanik_kapali(unit: str, n: int) -> str:
    """D9.1'in bulguları, ipucu adayları hariç (onlar envanterden, yani gizli metinden çıkar)."""
    lines = [x for x in E.mekanik_text(unit, n).split("\n") if not x.startswith("- İpucu adayı")]
    return "\n".join(lines) or "(Bulgu yok.)"


def kapali_prompt(unit: str, n: int) -> tuple[str, str]:
    cfg = P.UNITS[unit]
    text, sha = body(KAPALI_PROMPT, "ELESTIRI")
    text = text.format(sura_name=cfg["sura_name"], ayahs=ayahs(cfg), mekanik=mekanik_kapali(unit, n))
    ozet = (P.OUT / unit / "ek-ozet.md").read_text(encoding="utf-8")
    usul = H._section(ozet, "## 2. Usulün nazarî temeli", "## 6. Anlatım biçimi")
    text += ("\n\n# Usul özeti, 2–5. bölüm (İşârât'ın kendi metninden döküm; prova kopyası)\n\n" + usul
             + "\n\n# Taslak\n\nHer paragrafın başında çapası var (`V3/ar/5`: üçüncü vecih, Arapça, 6. paragraf; "
             "`V3/tr/5` onun tercümesi).\n\n" + draft_text(unit, n))
    return text, sha


def kapali(unit: str, n: int, again: bool = False, kabul: str | None = None, butun: bool = False) -> None:
    cfg = P.UNITS[unit]
    out = P.OUT / unit
    prompt, sha = kapali_prompt(unit, n)
    ok = P.leak_report(unit, cfg, out, prompt, f"sizinti-kapali-taslak-{n}.md")
    print(f"sızıntı testi: {'temiz' if ok else 'SORUN'} → {(out / f'sizinti-kapali-taslak-{n}.md').relative_to(ROOT)}")
    if not ok and not kabul:
        raise SystemExit("sızıntı raporunu oku; kalıp ibareyse --sizinti-kabul '<gerekçe>' ile sür")
    if not ok:
        print(f"  sızıntı uyarısı kabul edildi: {kabul}")
    keys = ["butun"] if butun else H._sections(unit, n)

    def one(key: str):
        stem = Y.out_dir(unit) / f"kapali-elestiri-taslak-{n}-{key}"
        if Path(str(stem) + ".json").exists() and not again:
            return key, json.loads(Path(str(stem) + ".json").read_text(encoding="utf-8"))
        p = prompt + (KAPALI_BUTUN if key == "butun" else KAPALI_BOLUM.format(baslik=P.SECTION_TITLES[key], key=key))
        return key, run_claude(p, stem, out / "mcp-klasik.json", PROVA_SERVERS,
                               {"gorev": "kapali-elestiri", "surum": SURUM["kapali"], "istem_sha": sha, "taslak": n,
                                "bolum": key})

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(one, keys))
    merged = {"taslak": n, "surum": SURUM["kapali"], "bolumler": {}, "notlar": [], "sistemli": [], "ozet": {}}
    for key, data in results:
        if data is None:
            merged["bolumler"][key] = "basarisiz"
            continue
        notes = data.get("notlar", [])
        for x in notes:
            x["bolum"] = key if key != "butun" else _bolum_of(x.get("capa"))
        H.check_notes(unit, n, notes, Y.out_dir(unit) / f"kapali-elestiri-taslak-{n}-{key}.jsonl")
        merged["bolumler"][key] = len(notes)
        merged["notlar"] += notes
        merged["sistemli"] += [dict(x, bolum=key) for x in data.get("sistemli", [])]
        merged["ozet"][key] = data.get("ozet", "")
    (Y.out_dir(unit) / f"kapali-elestiri-taslak-{n}.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"taslak {n}: kapalı kitap eleştirisi {merged['bolumler']}, toplam {len(merged['notlar'])} not")


# ---------------------------------------------------------------- düzeltme

NOTE_FILES = {"kapali": ("kapali-elestiri-taslak-{n}.json", "K", "kapalı kitap: İşârât'ın bu âyetlerdeki kısmını o da görmedi"),
              "acik": ("bolum-elestiri-taslak-{n}.json", "A", "açık kitap: İşârât'ın bu âyetlerdeki kısmını okuyarak"),
              # D15: İşârât karşılaştırması (`isarat`), kör aletlerin ayarında açık taraf
              "isarat": ("isarat-karsilastirma-taslak-{n}.json", "A", "açık kitap: İşârât'ın bu âyetlerdeki kısmını okuyarak"),
              # D turu (d2): yalnız düzeltmenin değiştirdiği paragraflara, yan etkileri için (`ikinci`)
              "ikinci": ("ikinci-elestiri-taslak-{n}.json", "Y", "ikinci kapalı kitap eleştiri: yalnız bir önceki "
                         "düzeltmenin değiştirdiği paragraflara, yan etkileri için (düşen fikir, belirsiz gönderme, "
                         "kendi sözün yerine nakil, îcâz); İşârât'ın bu âyetlerdeki kısmını o da görmedi")}


def notes_of(unit: str, n: int, kind: str) -> tuple[list[dict], str]:
    """Notlar numarasıyla (`K1`…/`A1`…, dosyadaki sırayla) ve önek."""
    file, prefix, _ = NOTE_FILES[kind]
    notes = json.loads((Y.out_dir(unit) / file.format(n=n)).read_text(encoding="utf-8"))["notlar"]
    for i, x in enumerate(notes, 1):
        x["no"] = f"{prefix}{i}"
    return notes, prefix


def required(notes: list[dict]) -> list[str]:
    return [x["no"] for x in notes if x.get("tur") != "dogru" and not x.get("ehline_sor")]


def render_notes(notes: list[dict]) -> str:
    L = []
    for x in notes:
        head = f"**{x['no']}** · {P.SECTION_TITLES.get(x.get('bolum'), x.get('bolum') or '')} · çapa `{x.get('capa')}` · " \
               f"tür {x.get('tur')}" + (f" · öncelik {x['oncelik']}" if x.get("oncelik") else "") \
               + (" · **ehline sor**" if x.get("ehline_sor") else "")
        L.append(head)
        if x.get("taslak_alinti"):
            L.append(f"  - Alıntı: {x['taslak_alinti']}")
        L.append(f"  - Not: {x.get('metin', '')}")
        for k, label in (("nasil", "Nasıl"), ("oneri", "Öneri"), ("soru", "Ehline soru")):
            if x.get(k):
                L.append(f"  - {label}: {x[k]}")
        if x.get("dayanak"):
            L.append(f"  - Dayanak: {', '.join(x['dayanak'])}")
        L.append("")
    return "\n".join(L)


def ar_chars(unit: str, n: int) -> int:
    blocks, _ = Y.draft_blocks(unit, n)
    return sum(len(t) for _, lang, q, t in blocks if lang == "ar" and not q)


def registry(unit: str) -> Path:
    return P.DRAFTS / unit / "duzeltmeler.json"


def duzelt(unit: str, n: int, kind: str) -> int | None:
    cfg = P.UNITS[unit]
    reg_path = registry(unit)
    reg = json.loads(reg_path.read_text(encoding="utf-8")) if reg_path.exists() else {}
    done = next((m for m, r in reg.items() if r["kaynak"] == n and r["notlar"] == kind), None)
    if done and (P.DRAFTS / unit / f"taslak-{done}.md").exists():
        print(f"taslak {n}, {kind} notlarla: taslak {done} olarak var")
        return int(done)
    m = int(done) if done else max(Y.drafts_of(unit)) + 1
    meta0 = json.loads((P.DRAFTS / unit / f"taslak-{n}.json").read_text(encoding="utf-8"))
    istem = (P.OUT / unit / P.istem_files(meta0["istem"], meta0.get("surum", "v1"))[0]).read_text(encoding="utf-8")
    if P._sha(istem) != meta0["prompt_sha"]:
        print(f"  uyarı: taslak {n}'in istemi değişmiş; düzeltme bugünkü istemle")
    notes, prefix = notes_of(unit, n, kind)
    _, sources = Y.draft_blocks(unit, n)
    h = H.hedef(unit)
    text, sha = body(DUZELTME_PROMPT, "DUZELTME")
    text = text.format(sura_name=cfg["sura_name"], ayahs=ayahs(cfg), not_kaynagi=NOTE_FILES[kind][2], onek=prefix,
                       en_az=f"{h['en_az']:,}".replace(",", "."), en_cok=f"{h['en_cok']:,}".replace(",", "."),
                       simdi=f"{ar_chars(unit, n):,}".replace(",", "."), sonraki=max(map(int, sources)) + 1,
                       taslak=draft_text(unit, n, with_ids=True), notlar=render_notes(notes))
    prompt = istem + "\n\n---\n\n" + text
    reg[str(m)] = {"kaynak": n, "notlar": kind, "surum": SURUM["duzeltme"], "at": datetime.now().isoformat()}
    reg_path.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
    stem = P.DRAFTS / unit / f"taslak-{m}.duzeltme"
    data = run_claude(prompt, stem, P.OUT / unit / "mcp-klasik.json", PROVA_SERVERS,
                      {"gorev": "duzeltme", "surum": SURUM["duzeltme"], "istem_sha": sha, "taslak": n, "notlar": kind})
    if data is None:
        return None
    build_revised(unit, n, m, kind, data, notes)
    return m


def _blocks(raw: str) -> list[dict]:
    """Taslağın Markdown'ı `parse_draft` gibi bloklara: [{raw, anchor, section}], çapa `draft_blocks`'unkiyle aynı."""
    out, current, count = [], None, {}
    for block in re.split(r"\n\s*\n", raw):
        block = block.strip()
        if not block:
            continue
        lines = block.split("\n")
        if lines[0].startswith("## "):
            current = P.heading_key(lines[0][3:])
            count = {}
            out.append({"raw": lines[0], "anchor": None, "section": current})
            block = "\n".join(lines[1:]).strip()
            if not block:
                continue
        if current is None or current not in P.SECTION_TITLES:
            out.append({"raw": block, "anchor": None, "section": current})
            continue
        quote = block.startswith(">")
        b = re.sub(r"^>\s?", "", block, flags=re.M) if quote else block
        lang = "tr" if b.startswith(STAMP) else ("ar" if P._arabic_ratio(b) > 0.5 else "tr")
        anchor = f"{current}/{lang}/{count.get(lang, 0)}"
        count[lang] = count.get(lang, 0) + 1
        out.append({"raw": block, "anchor": anchor, "section": current, "lang": lang, "quote": quote,
                    "stamped": b.startswith(STAMP)})
    return out


def _raw(text: str, lang: str, quote: bool, stamped: bool) -> str:
    text = text.strip()
    q = quote or text.startswith(">")
    text = re.sub(r"^>\s?", "", text, flags=re.M).strip()
    text = text.removeprefix(STAMP).strip()
    if lang == "tr" and (stamped or not q):
        text = f"{STAMP} {text}"
    return "\n".join("> " + line for line in text.split("\n")) if q else text


def apply_changes(raw: str, data: dict) -> tuple[str, list[str]]:
    blocks = _blocks(raw)
    by_anchor = {b["anchor"]: b for b in blocks if b["anchor"]}
    problems = []
    for ch in data.get("degisiklikler", []):
        op = ch.get("islem")
        if op in ("degistir", "sil"):
            b = by_anchor.get(ch.get("capa"))
            if b is None:
                problems.append(f"bilinmeyen çapa: {ch.get('capa')} ({op})")
                continue
            if op == "sil":
                b["deleted"] = True
            else:
                b["new"] = _raw(ch.get("metin", ""), b["lang"], b["quote"], b["stamped"])
        elif op == "ekle":
            b = by_anchor.get(ch.get("sonra"))
            if b is None:
                problems.append(f"bilinmeyen çapa: {ch.get('sonra')} (ekle)")
                continue
            b.setdefault("after", []).extend(_raw(x.get("metin", ""), x.get("dil", "ar"), False, x.get("dil") == "tr")
                                             for x in ch.get("bloklar", []))
        else:
            problems.append(f"bilinmeyen işlem: {op}")
    parts = []
    for b in blocks:
        if not b.get("deleted"):
            parts.append(b.get("new", b["raw"]))
        parts += b.get("after", [])
    extra = [x.strip() for x in data.get("kaynaklar_ek", []) if x.strip()]
    if extra:
        if any(b["section"] == "Kaynaklar" for b in blocks):
            parts[-1] = parts[-1] + "\n" + "\n".join(extra)
        else:
            parts += ["## Kaynaklar", "\n".join(extra)]
    return "\n\n".join(parts) + "\n", problems


def cite_calls(log: Path) -> dict[str, tuple[str, str]]:
    """Bir dökümdeki bütün `cite` çağrıları: numara -> (sunucu, kimlik); sonraki çağrı aynı numarayı ezer."""
    out = {}
    for line in log.read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") != "assistant":
            continue
        for block in event["message"].get("content", []):
            if block.get("type") == "tool_use" and block["name"].endswith("__cite"):
                inp = block.get("input") or {}
                first = int(inp.get("first") or 1)
                for i, item in enumerate(inp.get("sources") or inp.get("ids") or []):
                    out[str(first + i)] = (block["name"].split("__")[1], item["id"] if isinstance(item, dict) else item)
    return out


def build_revised(unit: str, n: int, m: int, kind: str, data: dict, notes: list[dict]) -> None:
    keep = P.DRAFTS / unit
    raw = (keep / f"taslak-{n}.md").read_text(encoding="utf-8")
    text, problems = apply_changes(raw, data)
    (keep / f"taslak-{m}.md").write_text(text, encoding="utf-8")
    rev_log = keep / f"taslak-{m}.duzeltme.jsonl"
    (keep / f"taslak-{m}.jsonl").write_text((keep / f"taslak-{n}.jsonl").read_text(encoding="utf-8")
                                            + rev_log.read_text(encoding="utf-8"), encoding="utf-8")
    ids = dict(P.draft_sources(keep / f"taslak-{n}.jsonl"))
    new_ids = cite_calls(rev_log)
    ids.update(new_ids)
    (keep / f"taslak-{m}.kaynak.json").write_text(json.dumps(ids, ensure_ascii=False, indent=1), encoding="utf-8")
    meta0 = json.loads((keep / f"taslak-{n}.json").read_text(encoding="utf-8"))
    rmeta = json.loads((keep / f"taslak-{m}.duzeltme.meta.json").read_text(encoding="utf-8"))
    req = set(required(notes))
    handled = {x for ch in data.get("degisiklikler", []) for x in ch.get("notlar", [])}
    rejected = {r.get("not") for r in data.get("reddedilen", [])}
    report = {"kaynak": n, "notlar": kind, "surum": SURUM["duzeltme"], "not_sayisi": len(notes),
              "karsilanmasi_gereken": len(req), "karsilanan": len(req & handled), "reddedilen": len(req & rejected),
              "anilmayan": sorted(req - handled - rejected, key=lambda s: int(s[1:])),
              "degisiklik": {op: sum(ch.get("islem") == op for ch in data.get("degisiklikler", []))
                             for op in ("degistir", "sil", "ekle")},
              "yeni_kaynak": sorted(new_ids, key=int), "sorunlar": problems,
              "ar_harf": {"once": ar_chars(unit, n), "sonra": ar_chars(unit, m)},
              "cost_usd": rmeta.get("cost_usd"), "seconds": rmeta.get("seconds"), "calls": rmeta.get("calls")}
    meta = dict(meta0, duzeltme=report)
    if meta0.get("duzeltme"):                          # D turu: düzeltilmiş taslağın düzeltmesi, önceki halkalar
        meta["duzeltme_zinciri"] = meta0.get("duzeltme_zinciri", []) + [meta0["duzeltme"]]
    meta["cost_usd_asil"] = meta0.get("cost_usd")
    (keep / f"taslak-{m}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"taslak {m} (taslak {n}, {kind} notlarla): {report['karsilanan']}/{report['karsilanmasi_gereken']} "
          f"karşılandı, {report['reddedilen']} reddedildi, anılmayan {len(report['anilmayan'])}; değişiklik "
          f"{report['degisiklik']}; Arapça {report['ar_harf']['once']} → {report['ar_harf']['sonra']} harf; "
          f"sorun {len(problems)}")
    for p in problems:
        print("  ", p)


# ---------------------------------------------------------------- D turu: ikinci kapalı eleştiri (d2)

def changed_places(unit: str, n: int, m: int) -> list[dict]:
    """Düzeltmenin değiştirdiği yerler: bölüm bölüm paragraf dizilerinin farkı; her yerde önceki ve düzeltilmiş
    bloklar (kendi çapalarıyla) ve düzeltmenin o yerde andığı notlar (çapası ya da `sonra`sı yerdeki eski çapa)."""
    old, _ = Y.draft_blocks(unit, n)
    new, _ = Y.draft_blocks(unit, m)
    data = json.loads((P.DRAFTS / unit / f"taslak-{m}.duzeltme.json").read_text(encoding="utf-8"))
    by_anchor: dict[str, set] = {}
    for ch in data.get("degisiklikler", []):
        a = ch.get("capa") or ch.get("sonra")
        if a:
            by_anchor.setdefault(a, set()).update(ch.get("notlar") or [])
    places = []
    for sec in P.SECTION_TITLES:
        o = [b for b in old if b[0].split("/")[0] == sec]
        w = [b for b in new if b[0].split("/")[0] == sec]
        sm = difflib.SequenceMatcher(a=[b[3] for b in o], b=[b[3] for b in w], autojunk=False)
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == "equal":
                continue
            olds, news = o[i1:i2], w[j1:j2]
            near = [b[0] for b in olds] + ([o[i1 - 1][0]] if i1 > 0 else [])   # ekle: önceki paragrafın ardına
            notes = sorted({x for a in near for x in by_anchor.get(a, ())}, key=lambda s: int(s[1:]))
            places.append({"bolum": sec, "onceki": olds, "duzeltilmis": news, "notlar": notes})
    return places


def ikinci(unit: str, m: int, again: bool = False, kabul: str | None = None) -> Path | None:
    """D turu (d2): taslak m (bir düzeltme) için yalnız değişen yerlere ikinci kapalı eleştiri (`elestiri-ikinci-istemi`)."""
    cfg = P.UNITS[unit]
    reg = json.loads(registry(unit).read_text(encoding="utf-8"))[str(m)]
    n = reg["kaynak"]
    out_path = Y.out_dir(unit) / f"ikinci-elestiri-taslak-{m}.json"
    if out_path.exists() and not again:
        print(f"{out_path.name}: var (--yeniden)")
        return out_path
    notes = {x["no"]: x for x in notes_of(unit, n, reg["notlar"])[0]}
    places = changed_places(unit, n, m)
    L = []
    for i, pl in enumerate(places, 1):
        L += [f"## Yer {i} · {P.SECTION_TITLES[pl['bolum']]}", ""]
        if pl["notlar"]:
            L.append("Düzeltmenin burada karşıladığı notlar:")
            for k in pl["notlar"]:
                x = notes.get(k, {})
                L.append(f"- {k} ({x.get('tur', '')}): {x.get('metin', '')}" + (f" Öneri: {x['oneri']}" if x.get("oneri") else ""))
            L.append("")
        L += ["### Önceki hâl", ""] + ([f"[{a}]{' (alıntı)' if q else ''} {t}" for a, _, q, t in pl["onceki"]] or ["(yok: yeni eklendi)"])
        L += ["", "### Düzeltilmiş hâl", ""] + ([f"[{a}]{' (alıntı)' if q else ''} {t}" for a, _, q, t in pl["duzeltilmis"]] or ["(silindi)"])
        L.append("")
    text, sha = body(IKINCI_PROMPT, "IKINCI")
    text = text.format(sura_name=cfg["sura_name"], ayahs=ayahs(cfg), yerler="\n".join(L))
    ozet = (P.OUT / unit / "ek-ozet.md").read_text(encoding="utf-8")
    text += ("\n\n# Usul özeti, 2–5. bölüm (İşârât'ın kendi metninden döküm; prova kopyası)\n\n"
             + H._section(ozet, "## 2. Usulün nazarî temeli", "## 6. Anlatım biçimi"))
    out = P.OUT / unit
    ok = P.leak_report(unit, cfg, out, text, f"sizinti-ikinci-taslak-{m}.md")
    print(f"{len(places)} yer; sızıntı testi: {'temiz' if ok else 'SORUN'}")
    if not ok and not kabul:
        raise SystemExit("sızıntı raporunu oku; kalıp ibareyse --sizinti-kabul '<gerekçe>' ile sür")
    stem = Y.out_dir(unit) / f"ikinci-elestiri-taslak-{m}"
    data = run_claude(text, stem, out / "mcp-klasik.json", PROVA_SERVERS,
                      {"gorev": "ikinci-elestiri", "surum": SURUM["ikinci"], "istem_sha": sha, "taslak": m,
                       "kaynak": n, "yer": len(places), **({"sizinti_kabul": kabul} if kabul else {})})
    if data is None:
        return None
    for x in data.get("notlar", []):
        x["bolum"] = (x.get("capa") or "genel").split("/")[0]
    H.check_notes(unit, m, data.get("notlar", []), Path(str(stem) + ".jsonl"))
    merged = {"taslak": m, "kaynak": n, "surum": SURUM["ikinci"], "yer": len(places), "notlar": data.get("notlar", []),
              "ozet": data.get("ozet", "")}
    out_path.write_text(json.dumps(merged, ensure_ascii=False, indent=1), encoding="utf-8")
    kinds = Counter(x.get("tur") for x in merged["notlar"])
    print(f"taslak {m}: ikinci eleştiri {len(merged['notlar'])} not {dict(kinds)}")
    return out_path


# ---------------------------------------------------------------- kör ölçü

def olc(unit: str, pairs: list[tuple[int, int]], again: bool = False) -> None:
    cfg = P.UNITS[unit]
    text, sha = body(OLCU_PROMPT, "OLCU")
    ar = next(x for x in cfg["nodes"] if x.startswith("isaratul-icaz-arabi/"))
    tr = next(x for x in cfg["nodes"] if x.startswith("isaratul-icaz/"))
    mcp = E.critic_mcp(unit)
    jobs = []
    for a, b in pairs:
        stem = Y.out_dir(unit) / f"kor-olcu-{a}-{b}"
        if Path(str(stem) + ".json").exists() and not again:
            print(f"{stem.name}: var")
            continue
        order = [a, b]
        random.Random(f"d12-{unit}-{a}-{b}").shuffle(order)
        prompt = text.format(sura_name=cfg["sura_name"], ayahs=ayahs(cfg), gizli_ar=ar, gizli_tr=tr,
                             taslak_a=draft_text(unit, order[0]), taslak_b=draft_text(unit, order[1]))
        jobs.append((prompt, stem, {"gorev": "kor-olcu", "surum": SURUM["olcu"], "istem_sha": sha,
                                    "A": order[0], "B": order[1]}))
    with ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(lambda j: run_claude(j[0], j[1], mcp, tuple(E.CRITIC_SERVERS), j[2]), jobs))


# ---------------------------------------------------------------- iki eleştirmenin notları

def notlar(unit: str, n: int, acik: str = "acik") -> None:
    cfg = P.UNITS[unit]
    k_notes, _ = notes_of(unit, n, "kapali")
    a_notes, _ = notes_of(unit, n, acik)
    k_notes = [x for x in k_notes if x.get("tur") != "dogru"]
    a_notes = [x for x in a_notes if x.get("tur") != "dogru"]
    h = Y.hidden(unit)
    text, sha = body(NOT_PROMPT, "KARSILASTIRMA")
    text = text.format(sura_name=cfg["sura_name"], ayahs=ayahs(cfg), arapca=Y.render_hidden(h["ar"]),
                       turkce=Y.render_hidden(h["tr"]), acik=render_notes(a_notes), kapali=render_notes(k_notes))
    stem = Y.out_dir(unit) / (f"not-karsilastirma-taslak-{n}" + ("" if acik == "acik" else f"-{acik}"))
    run_claude(text, stem, None, (), {"gorev": "not-karsilastirma", "surum": SURUM["notlar"], "istem_sha": sha,
                                      "taslak": n, "acik": acik})


# ---------------------------------------------------------------- İşârât karşılaştırması (D15)

def isarat(unit: str, n: int, again: bool = False) -> dict | None:
    """Tek taslak İşârât'ın kendisiyle: mutlak hüküm ve notlar (`docs/d1/isarat-karsilastirma-istemi.md`)."""
    cfg = P.UNITS[unit]
    stem = Y.out_dir(unit) / f"isarat-karsilastirma-taslak-{n}"
    if Path(str(stem) + ".json").exists() and not again:
        print(f"{stem.name}: var")
        return json.loads(Path(str(stem) + ".json").read_text(encoding="utf-8"))
    text, sha = body(ISARAT_PROMPT, "KARSILASTIRMA")
    ar = next(x for x in cfg["nodes"] if x.startswith("isaratul-icaz-arabi/"))
    trs = [x for x in cfg["nodes"] if x.startswith("isaratul-icaz/")]
    tr_read = " ve ".join(f'`read_section("{x}")`' for x in trs)
    prompt = text.format(sura_name=cfg["sura_name"], ayahs=ayahs(cfg), gizli_ar=ar, gizli_tr_okuma=tr_read,
                         taslak=draft_text(unit, n))
    data = run_claude(prompt, stem, E.critic_mcp(unit), tuple(E.CRITIC_SERVERS),
                      {"gorev": "isarat-karsilastirma", "surum": SURUM["isarat"], "istem_sha": sha, "taslak": n})
    if data:
        for x in data.get("notlar", []):
            x["bolum"] = _bolum_of(x.get("capa"))
        H.check_notes(unit, n, data.get("notlar", []), Path(str(stem) + ".jsonl"))
        Path(str(stem) + ".json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        b = data.get("butun", {})
        print(f"taslak {n}: İşârât karşılaştırması bütün: {b.get('hukum')}; bölümler "
              f"{[(x.get('bolum'), x.get('hukum')) for x in data.get('bolumler', [])]}; {len(data.get('notlar', []))} not")
    return data


# ---------------------------------------------------------------- sayılar

def coverage(unit: str, n: int, model: str = "opus") -> dict | None:
    path = Y.out_dir(unit) / f"eslestirme-taslak-{n}-{model}.json"
    if not path.exists():
        return None
    env = json.loads((Y.out_dir(unit) / "envanter.json").read_text(encoding="utf-8"))
    blocks, _ = Y.draft_blocks(unit, n)
    res = Y.check_match(json.loads(path.read_text(encoding="utf-8")), env, blocks)
    items = env["kalemler"]
    found = [i for i in items if (res["nukteler"].get(i["id"]) or {}).get("durum") in Y.FOUND]
    aynen = [i for i in items if (res["nukteler"].get(i["id"]) or {}).get("durum") == "aynen"]
    nomuk = [i for i in items if i.get("vecih") != "Mukaddime"]
    found_nm = [i for i in found if i.get("vecih") != "Mukaddime"]
    celiski = sum(1 for f in res["fazla"] if f.get("celiski"))
    return {"kapsama": round(100 * len(found) / len(items)), "mukaddimesiz": round(100 * len(found_nm) / len(nomuk)),
            "aynen": len(aynen), "fazla": len(res["fazla"]), "celiski": celiski}


def rapor(unit: str) -> None:
    reg = json.loads(registry(unit).read_text(encoding="utf-8")) if registry(unit).exists() else {}
    L = [f"# D12.1 sayıları: {unit}", "", "`uv run python scripts/d1-duzelt.py rapor` üretir; yorum `d12-1-rapor.md`'de.", ""]
    L += ["## Taslaklar", "", "| Taslak | Ne | Arapça harf | Kapsama (opus) | Mukaddimesiz | Aynen | Fazla | Çelişki | "
          "Not karşılandı / reddedildi / anılmadı | Değişiklik | Maliyet |", "|---|---|---:|---:|---:|---:|---:|---:|---|---|---:|"]
    for n in Y.drafts_of(unit):
        if n != 7 and str(n) not in reg:
            continue
        meta = json.loads((P.DRAFTS / unit / f"taslak-{n}.json").read_text(encoding="utf-8"))
        d = meta.get("duzeltme")
        c = coverage(unit, n) or {}
        what = "pilot (D11)" if not d else f"{d['kaynak']}'in düzeltmesi, {d['notlar']} notlarla"
        nt = f"{d['karsilanan']} / {d['reddedilen']} / {len(d['anilmayan'])} (gereken {d['karsilanmasi_gereken']})" if d else ""
        ch = ", ".join(f"{k} {v}" for k, v in d["degisiklik"].items()) if d else ""
        cost = d["cost_usd"] if d else meta.get("cost_usd")
        L.append(f"| {n} | {what} | {ar_chars(unit, n):,} | {c.get('kapsama', '–')} | {c.get('mukaddimesiz', '–')} | "
                 f"{c.get('aynen', '–')} | {c.get('fazla', '–')} | {c.get('celiski', '–')} | {nt} | {ch} | "
                 + (f"{cost:.2f} $" if cost else "–") + " |")
    L += ["", "## Kör ölçü (açık kitap, bütün)", "", "| Çift | A | B | Bütün | Bölümler | Maliyet |", "|---|---|---|---|---|---:|"]
    for path in sorted(Y.out_dir(unit).glob("kor-olcu-*.json")):
        if path.name.endswith(".meta.json"):
            continue
        meta = json.loads(path.with_name(path.stem + ".meta.json").read_text(encoding="utf-8"))
        data = json.loads(path.read_text(encoding="utf-8"))
        who = {"A": meta["A"], "B": meta["B"], "esit": "eşit"}
        b = data.get("butun", {})
        secs = "; ".join(f"{x.get('bolum')}: {who.get(x.get('tercih'), x.get('tercih'))} ({x.get('guc')})"
                         for x in data.get("bolumler", []))
        L.append(f"| {path.stem.removeprefix('kor-olcu-')} | {meta['A']} | {meta['B']} | "
                 f"{who.get(b.get('tercih'), b.get('tercih'))} ({b.get('guc')}) | {secs} | {meta.get('cost_usd') or 0:.2f} $ |")
    path = Y.out_dir(unit) / "not-karsilastirma-taslak-7.json"
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        from collections import Counter
        t = Counter(x.get("tur") for x in data.get("acik", []))
        d = Counter(x.get("deger") for x in data.get("kapali_tek", []))
        L += ["", "## İki eleştirmen (taslak 7, övgü dışı notlar)", "",
              f"Açık kitabın notları: {sum(t.values())}; kapalıyla eşleşen {t['eslesti']}, yalnız gizli metinden "
              f"{t['yalniz_gizli']}, görülebilirdi {t['gorulebilirdi']}, karışık {t['karisik']}.",
              f"Kapalının eşleşmeyen notları: {sum(d.values())}; yerinde {d['yerinde']}, şüpheli {d['supheli']}, "
              f"yanlış {d['yanlis']}."]
    out = P.DRAFTS / unit / "d12-1-sayilar.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))

# ---------------------------------------------------------------- D12.2 fark kartları

FARK_TEMPLATE = Path(__file__).with_name("d1-fark-sablon.html")
FARK_INTRO = """<p><b>Ne okuyorsunuz:</b> aynı taslağın iki hâli; biri bir eleştirmenin notlarıyla düzeltildi. Yalnız
değişen paragraflar, A ve B diye; hangisinin düzeltilmiş olduğu karışık sırayla gizli. Sarı işaretli kelimeler öbür
yanda olmayanlardır.</p><ul><li>Her kartta <b>hangisi daha iyi</b> (doğruluk, İşârât'a yakınlık, kaynak disiplini,
îcâz) ve bir iki cümle gerekçe.</li><li>Sonra <b>Aç</b>: hangisinin düzeltilmiş olduğu ve iki ölçünün (İşârât'tan
çıkarılan envanter ve kör eleştirmen) o yer için dediği. Envanter bir çelişki gösteriyorsa onun gerçek olup
olmadığını sorar.</li><li>Bitince <b>Dışa aktar</b>; dosyayı bana gönderin.</li></ul><p class="small muted">Kartların
yarısı iki ölçünün ayrıldığı yerlerdir (envanter düzeltmede yeni çelişki görüyor, eleştirmen düzeltilmişi tercih
ediyor); öbürleri eleştirmenin açık hüküm verdiği yerler. Hangisi hangisi, açınca görünür.</p>"""
# D12.3'ün yerleri (PLANLAR.md D12.3): ölçülerin ayrıldığı yerler ve eleştirmenin açık hüküm verdiği yerler
FARK_YERLER = {("31-33", 7, 8): {"ayrilik": ["Mukaddime/0", "Mukaddime/1", "V1/0", "V2/0", "V3/0"],
                                 "elestirmen": ["V2/3", "V3/3", "V3/6", "V3/4", "V1/4"]}}


def fark(unit: str, old: int, new: int) -> Path:
    cfg = P.UNITS[unit]
    yerler = FARK_YERLER[(unit, old, new)]
    bo = {a: t for a, _, _, t in Y.draft_blocks(unit, old)[0]}
    bn = {a: t for a, _, _, t in Y.draft_blocks(unit, new)[0]}
    env = json.loads((Y.out_dir(unit) / "envanter.json").read_text(encoding="utf-8"))
    items = {i["id"]: i for i in env["kalemler"]}
    h = Y.hidden(unit)
    res = {}
    for n in (old, new):
        blocks, _ = Y.draft_blocks(unit, n)
        res[n] = Y.check_match(json.loads((Y.out_dir(unit) / f"eslestirme-taslak-{n}-opus.json").read_text(
            encoding="utf-8")), env, blocks)
    old_conf = {(f.get("celiski"), a) for f in res[old]["fazla"] if f.get("celiski") for a in f.get("taslak") or []}
    kor = Y.out_dir(unit) / f"kor-olcu-{old}-{new}"
    kmeta = json.loads(Path(str(kor) + ".meta.json").read_text(encoding="utf-8"))
    kdata = json.loads(Path(str(kor) + ".json").read_text(encoding="utf-8"))
    who = {"A": kmeta["A"], "B": kmeta["B"]}
    remarks = list(kdata.get("yalniz_A_kusurlari", [])) + list(kdata.get("yalniz_B_kusurlari", []))
    for b in kdata.get("bolumler", []):
        remarks += re.split(r"(?<=[.;])\s+", b.get("gerekce", ""))

    def relabel(t: str) -> str:
        return re.sub(r"\b([AB]):(?=[A-ZÂÎÛ])", lambda m: f"taslak {who[m.group(1)]}:", t)

    # D12.5 Tur 0 (D12.3'te eksikti): kartın iki hâlinin andığı kaynakların metni, karar verirken açılabilir
    texts = P.SourceTexts(unit)
    srcs = {n: (Y.draft_blocks(unit, n)[1], P.draft_sources(P.DRAFTS / unit / f"taslak-{n}.jsonl")) for n in (old, new)}

    def card_sources(anchors: list[str]) -> list[dict]:
        out, seen = [], set()
        for n in (old, new):
            cites, ids = srcs[n]
            body = " ".join({a: t for a, _, _, t in Y.draft_blocks(unit, n)[0]}.get(a, "") for a in anchors)
            for num in sorted({x for m in re.finditer(r"\[([^\[\]\n]{1,80})\]", body) for x in re.findall(r"\d+", m.group(1))}, key=int):
                server, sid = ids.get(num, (None, None))
                key = (sid or cites.get(num, ""))
                if not key or key in seen:
                    continue
                seen.add(key)
                out.append({"n": num, "cite": cites.get(num, ""), "id": sid,
                            "text": (texts.text(server, sid, cites.get(num, "")) or "")[:1500]})
        return out

    cards = []
    for tur, ids in yerler.items():
        for pid in ids:
            sec, k = pid.split("/")
            ar, tr = f"{sec}/ar/{k}", f"{sec}/tr/{k}"
            envs = []
            for f in res[new]["fazla"]:
                nid = f.get("celiski")
                if nid and set(f.get("taslak") or []) & {ar, tr} and not any((nid, a) in old_conf for a in (ar, tr)):
                    it = items.get(nid, {})
                    envs.append({"id": nid, "iddia": f.get("iddia", ""), "nukte": it.get("nukte", ""),
                                 "isarat_ar": Y.hidden_text(h, it.get("ar") or []),
                                 "isarat_tr": Y.hidden_text(h, it.get("tr") or [])})
            pat = re.compile(rf"\b[AB]:{re.escape(sec)}/(?:ar|tr)/{k}\b")
            crit = [relabel(r) for r in remarks if pat.search(r)]
            cards.append({"id": pid, "tur": tur, "sec_title": P.SECTION_TITLES[sec],
                          "ar": [bo.get(ar, ""), bn.get(ar, "")], "tr": [bo.get(tr, ""), bn.get(tr, "")],
                          "left": None,
                          "envanter": envs, "elestirmen": crit, "kaynak": card_sources([ar, tr])})
    rng = random.Random(f"d12-fark-{unit}-{old}-{new}")
    rng.shuffle(cards)
    sides = (["eski", "yeni"] * len(cards))[:len(cards)]       # sol ve sağ yarı yarıya (sıradan tahmin edilmesin)
    rng.shuffle(sides)
    for c, side in zip(cards, sides):
        c["left"] = side
    data = {"unit": unit, "title": f"{cfg['sura_name']} {ayahs(cfg)}", "eski": old, "yeni": new, "cards": cards,
            "intro": FARK_INTRO}
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    out = M.OUT_DIR / f"fark-{unit}-{old}-{new}.html"
    out.write_text(FARK_TEMPLATE.read_text(encoding="utf-8").replace("{data}", blob), encoding="utf-8")
    print(f"{out.relative_to(ROOT)}: {len(cards)} kart; envanter çelişkisi olan {sum(bool(c['envanter']) for c in cards)}, "
          f"eleştirmen sözü olan {sum(bool(c['elestirmen']) for c in cards)}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("kapali")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--taslak", type=int, required=True)
    p.add_argument("--yeniden", action="store_true")
    p.add_argument("--sizinti-kabul", help="sızıntı uyarısı elle incelendi: gerekçe")
    p.add_argument("--butun", action="store_true", help="D15: bütün taslağa tek çağrı (bölüm bölüm değil)")
    p = sub.add_parser("isarat")                      # D15: tek taslak İşârât'la, mutlak hüküm ve notlar
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--taslak", type=int, required=True)
    p.add_argument("--yeniden", action="store_true")
    p = sub.add_parser("ikinci")                      # D turu (d2): düzeltilmiş taslağın değişen yerlerine ikinci eleştiri
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--taslak", type=int, required=True, help="düzeltilmiş taslak (registry'de kaynağı olan)")
    p.add_argument("--yeniden", action="store_true")
    p.add_argument("--sizinti-kabul", help="sızıntı uyarısı elle incelendi: gerekçe")
    p = sub.add_parser("istem")                       # yalnız istemleri yaz ve sızıntı testi (model yok)
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--taslak", type=int, required=True)
    p = sub.add_parser("duzelt")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--taslak", type=int, required=True)
    p.add_argument("--notlar", choices=NOTE_FILES, required=True)
    p = sub.add_parser("uygula")                      # düzeltme cevabını yeniden uygula (model yok)
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--yeni", type=int, required=True)
    p = sub.add_parser("olc")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--cift", nargs="+", required=True)
    p.add_argument("--yeniden", action="store_true")
    p = sub.add_parser("notlar")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--taslak", type=int, required=True)
    p.add_argument("--acik", choices=("acik", "isarat"), default="acik")
    p = sub.add_parser("rapor")
    p.add_argument("unit", choices=P.UNITS)
    p = sub.add_parser("fark")                        # D12.2 fark kartları: data/d1/masa/fark-<birim>-<eski>-<yeni>.html
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--eski", type=int, required=True)
    p.add_argument("--yeni", type=int, required=True)
    a = ap.parse_args()
    if a.cmd == "kapali":
        kapali(a.unit, a.taslak, a.yeniden, a.sizinti_kabul, a.butun)
    elif a.cmd == "isarat":
        isarat(a.unit, a.taslak, a.yeniden)
    elif a.cmd == "ikinci":
        ikinci(a.unit, a.taslak, a.yeniden, a.sizinti_kabul)
    elif a.cmd == "istem":
        prompt, _ = kapali_prompt(a.unit, a.taslak)
        out = P.OUT / a.unit
        (out / f"istem-kapali-taslak-{a.taslak}.md").write_text(prompt, encoding="utf-8")
        ok = P.leak_report(a.unit, P.UNITS[a.unit], out, prompt, f"sizinti-kapali-taslak-{a.taslak}.md")
        print(f"kapalı eleştirmen istemi {len(prompt):,} harf; sızıntı testi: {'temiz' if ok else 'SORUN'}")
    elif a.cmd == "duzelt":
        duzelt(a.unit, a.taslak, a.notlar)
    elif a.cmd == "uygula":
        reg = json.loads(registry(a.unit).read_text(encoding="utf-8"))[str(a.yeni)]
        data = json.loads((P.DRAFTS / a.unit / f"taslak-{a.yeni}.duzeltme.json").read_text(encoding="utf-8"))
        notes, _ = notes_of(a.unit, reg["kaynak"], reg["notlar"])
        build_revised(a.unit, reg["kaynak"], a.yeni, reg["notlar"], data, notes)
    elif a.cmd == "olc":
        olc(a.unit, [tuple(map(int, c.split("-"))) for c in a.cift], a.yeniden)
    elif a.cmd == "notlar":
        notlar(a.unit, a.taslak, a.acik)
    elif a.cmd == "rapor":
        rapor(a.unit)
    elif a.cmd == "fark":
        fark(a.unit, a.eski, a.yeni)


if __name__ == "__main__":
    main()
