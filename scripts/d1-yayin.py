"""S7.1 veri katmanı: bir birimin yayın dosyası (kullanıcının kararı, 2026-11-21; PLANLAR S7). Ar-ge masası da okuma
platformu da bu dosyadan çizilir; ileride okuyucu ve ehil notları bunun kimliklerine bağlanır.

    uv run python scripts/d1-yayin.py yayinla 34 [--taslak 4]   # data/d1/yayin/bakara/<birim>/v<k>.json (değişmez)
    uv run python scripts/d1-yayin.py goster 34                  # son sürümün özeti

Kurallar:
- **Sürümler değişmez.** Bir sürüm yazıldıktan sonra dokunulmaz, silinmez. İçerik (blokların metni, kaynaklar, izah,
  işaretler) öncekiyle aynıysa yeni sürüm açılmaz; değiştiyse `v<k+1>`. `index.json` her birimin sürümlerini tutar.
- **Paragraf kimliği içerikten:** `p-` + bölüm anahtarı ve normalleştirilmiş metnin SHA-1'inin ilk 10 hanesi (aynı
  birimde aynı metin iki kez geçerse `-2`). Sıra numarası değildir: düzeltme bir paragrafı değiştirmezse kimliği
  sürümden sürüme aynı kalır, notlar taşınır; değiştirirse yeni kimlik, eski sürümdeki not eski sürüme bağlı kalır.
  Bir not ayrıca işaretlediği sözü (önü ve ardıyla) taşır (W3C Web Annotation'ın TextQuoteSelector'ı gibi; S7.4).
- **Sahiplik her kayıtta:** blokların `sahip`i `yapay_zeka` (taslağın Arapçası, tercüme, izah) ya da alıntının kaynağı
  (`kaynak`: Risale, müfessir…); eleştirmen notları `yapay_zeka_elestirmen`, denetlenmedi.
- **Okuyucuya giden sonuçlar:** kapının düzeltemediği kuşkulu atıflar bloğun `isaretler`inde (nisbet denetçisinin
  hükmü ve gerekçesi; yapay zekânın hükmüdür), kapının özeti `kunye.kapi`'da, eksik notları `eksik`te. Ham notlar ar-ge
  masasında, birim klasöründen okunur (bu dosyada yok).
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d1-yayin/1"


def _load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / file)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


P = _load("d1_prova", "d1-prova.py")
Y = _load("d1_yz", "d1-yz.py")
YAYIN = P.KEEP / "yayin"
STAMP_RE = re.compile(r"Yapay zekâ tercümesi(?: \(alıntının\))?: ?$")


def flat(t: str) -> str:
    return re.sub(r"\s+", " ", t or "").strip()


def chain(unit: str, son: int) -> list[dict]:
    """Son taslağa giden düzeltmeler, baştan sona: [{kaynak, yeni, notlar, surum}]."""
    reg_path = P.DRAFTS / unit / "duzeltmeler.json"
    reg = json.loads(reg_path.read_text(encoding="utf-8")) if reg_path.exists() else {}
    out, cur = [], str(son)
    while cur in reg:
        r = reg[cur]
        out.append({"kaynak": r["kaynak"], "yeni": int(cur), "notlar": r["notlar"], "surum": r.get("surum")})
        cur = str(r["kaynak"])
    return out[::-1]


def residual_flags(unit: str, steps: list[dict], final_text: str) -> list[dict]:
    """Kapıdan sonra kalan kuşkulu atıflar: kapının ilk düzeltmesinin nisbet denetiminde hata çıkıp son taslakta hâlâ
    duran (ikinci turda karşılanmamış) sözler."""
    first = next((s["yeni"] for s in steps if s["notlar"] == "kapi"), None)
    d = Y.out_dir(unit)
    if not first or not (d / f"nisbet-taslak-{first}.json").exists():
        return []
    errs = [h for h in json.loads((d / f"nisbet-taslak-{first}.json").read_text(encoding="utf-8"))["hukumler"]
            if h["hukum"] in ("asiyor", "kaynakta_yok")]
    fixed: set[str] = set()
    k2 = next((s for s in steps if s["notlar"] == "kapi2"), None)
    if k2 and (d / f"kapi2-notlar-taslak-{k2['kaynak']}.json").exists():
        notes = json.loads((d / f"kapi2-notlar-taslak-{k2['kaynak']}.json").read_text(encoding="utf-8"))["notlar"]
        data = json.loads((P.DRAFTS / unit / f"taslak-{k2['yeni']}.duzeltme.json").read_text(encoding="utf-8"))
        handled = {no for ch in data.get("degisiklikler", []) for no in ch.get("notlar", [])}
        fixed = {flat(x.get("taslak_alinti"))[:40] for i, x in enumerate(notes, 1) if f"R{i}" in handled}
    out = []
    for h in errs:
        q = flat(h.get("taslak_alinti"))[:40]
        if q and q in final_text and q not in fixed:
            out.append({"alinti": h.get("taslak_alinti"), "kaynak": str(h.get("kaynak")), "hukum": h["hukum"],
                        "gerekce": h.get("gerekce"), "sahip": "yapay_zeka_denetci"})
    return out


def build(unit: str, n: int | None = None) -> dict:
    cfg = P.UNITS[unit]
    st = P.d5_state()["birimler"].get(unit, {})
    son = n or st.get("son_taslak")
    if not son:
        raise SystemExit(f"{unit}: son taslak yok")
    keep = P.DRAFTS / unit
    steps = chain(unit, son)
    first = steps[0]["kaynak"] if steps else son
    meta0 = json.loads((keep / f"taslak-{first}.json").read_text(encoding="utf-8"))
    blocks, sources = Y.draft_blocks(unit, son)
    raw_flat = flat((keep / f"taslak-{son}.md").read_text(encoding="utf-8"))
    izf = Y.out_dir(unit) / f"izah-taslak-{son}.json"
    izah = {x.get("capa"): x.get("metin", "") for x in json.loads(izf.read_text(encoding="utf-8")).get("izah", [])} \
        if izf.exists() else {}
    ids = P.draft_sources(keep / f"taslak-{son}.jsonl") if (keep / f"taslak-{son}.jsonl").exists() else {}
    texts = P.SourceTexts(unit)
    q = json.loads((ROOT / "data" / "library" / "kuran" / "quran.json").read_text(encoding="utf-8"))
    ay = {v["ayah"]: v for v in q["suras"][cfg["sura"] - 1]["ayahs"]}
    a, b = cfg["ayahs"]

    out_blocks, seen, pid_of = [], {}, {}
    pr = Y.pairs(blocks)          # Arapça paragraf ↔ Türkçesi (sıra numarasıyla değil; `d1-yz.pairs`)
    for anchor, lang, quote, text in blocks:
        key = anchor.split("/")[0]
        if key == "Âyet":
            continue
        h = hashlib.sha1(f"{key}\n{flat(text)}".encode("utf-8")).hexdigest()[:10]
        pid = f"p-{h}"
        seen[pid] = seen.get(pid, 0) + 1
        if seen[pid] > 1:
            pid = f"{pid}-{seen[pid]}"
        if lang == "ar":
            kind = "alinti_ar" if quote else "ar"
            owner = "kaynak" if quote else "yapay_zeka"
        else:
            head = flat(text)[:60]
            stamped = head in raw_flat and STAMP_RE.search(raw_flat.split(head, 1)[0][-60:]) is not None
            kind = ("alinti_tercume" if quote else "tercume") if stamped else ("alinti" if quote else "tr")
            owner = "yapay_zeka" if kind != "alinti" else "kaynak"
        blk = {"id": pid, "bolum": key, "tur": kind, "sahip": owner, "metin": text,
               "kaynaklar": sorted(set(re.findall(r"\[(\d+)\]", text)), key=int), "taslak_capa": anchor}
        if izah.get(anchor):
            blk["izah"] = {"metin": izah[anchor], "sahip": "yapay_zeka"}
        pid_of[anchor] = pid
        out_blocks.append(blk)
    # bölüm içi alt başlıklar ("### Ders: …", "### Dersin sonu"): ardından gelen paragrafın `ust_baslik`'ı
    DZ = sys.modules.get("d1_duzelt") or _load("d1_duzelt", "d1-duzelt.py")
    pending = None
    for raw_blk in DZ._blocks((keep / f"taslak-{son}.md").read_text(encoding="utf-8")):
        if raw_blk["anchor"] is None and raw_blk["raw"].startswith("### "):
            pending = raw_blk["raw"][4:].strip()
        elif raw_blk["anchor"] and pending:
            if raw_blk["anchor"] in pid_of:
                next(x for x in out_blocks if x["taslak_capa"] == raw_blk["anchor"])["ust_baslik"] = pending
            pending = None
    for blk in out_blocks:        # Türkçe paragrafın Arapçası (tercüme ya da alıntının tercümesi)
        capa = blk["taslak_capa"]
        if "/tr/" in capa and pr.get(capa) in pid_of:
            blk["tercumesi"] = pid_of[pr[capa]]

    for f in residual_flags(unit, steps, raw_flat):
        q40 = flat(f["alinti"])[:40]
        target = next((blk for blk in out_blocks if q40 and q40 in flat(blk["metin"])), None)
        if target is not None:
            target.setdefault("isaretler", []).append({k: v for k, v in f.items() if k != "alinti"} | {"soz": f["alinti"]})

    src = {}
    for k, line in sorted(sources.items(), key=lambda kv: int(kv[0])):
        server, sid = ids.get(k, (None, None))
        src[k] = {"satir": line, "sunucu": server, "kimlik": sid, "metin": texts.text(server, sid, line)}

    # kapının özeti (okuyucuya künye): her halkada not, karşılanan, reddedilen
    kapi = []
    for s in steps:
        m = json.loads((keep / f"taslak-{s['yeni']}.json").read_text(encoding="utf-8")).get("duzeltme", {})
        kapi.append({"tur": s["notlar"], "surum": s["surum"], "taslak": [s["kaynak"], s["yeni"]],
                     "not": m.get("not_sayisi"), "karsilanan": m.get("karsilanan"), "reddedilen": m.get("reddedilen"),
                     "ar_harf": m.get("ar_harf")})
    acik = Y.out_dir(unit) / f"kapi-acik-notlar-taslak-{first}.json"
    first_blocks = {a: t for a, _, _, t in Y.draft_blocks(unit, first)[0]}
    by_text = {flat(blk["metin"]): blk["id"] for blk in out_blocks}
    eksik = []
    for x in (json.loads(acik.read_text(encoding="utf-8"))["notlar"] if acik.exists() else []):
        old = flat(first_blocks.get(x.get("capa"), ""))
        pid = by_text.get(old)
        if pid is None and old:          # düzeltme paragrafı değiştirdiyse aynı bölümde en benzeri (≥ 0,6)
            import difflib
            sec = (x.get("capa") or "").split("/")[0]
            cands = [(difflib.SequenceMatcher(None, old[:400], flat(blk["metin"])[:400]).ratio(), blk["id"])
                     for blk in out_blocks if blk["bolum"] == sec]
            best = max(cands, default=(0, None))
            pid = best[1] if best[0] >= 0.6 else None
        eksik.append({"metin": x.get("metin"), "oneri": x.get("oneri"), "bolum": (x.get("capa") or "").split("/")[0],
                      "paragraf": pid, "sahip": "yapay_zeka_elestirmen", "denetlendi": False})

    content = {"bloklar": out_blocks, "kaynaklar": src, "eksik": eksik}
    return {
        "sema": SCHEMA, "birim": unit, "sure": cfg["sura"], "sure_adi": cfg["sura_name"], "ayet": [a, b],
        "ayetler": [{"n": k, "metin": ay[k]["text"], "meal": ay[k]["translations"]["diyanet-vakfi"],
                     "meal_sahibi": "Türkiye Diyanet Vakfı"} for k in range(a, b + 1)],
        "kunye": {"istem": meta0.get("surum"), "model": meta0.get("model"), "effort": meta0.get("effort"),
                  "yazildi": meta0.get("at"), "istem_sha": meta0.get("prompt_sha"), "taslak": first, "son_taslak": son,
                  "kapi": kapi, "maliyet": st.get("maliyet"), "sure_dk": st.get("sure_dk"),
                  "alarmlar": st.get("alarmlar") or [], "saklı": not cfg.get("d5"),
                  "damga": "Yapay zekâ taslağıdır; tefsir değildir, müellife ya da İşârât'a mal edilmez."},
        **content,
        "icerik_sha": hashlib.sha1(json.dumps(content, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:12],
    }


def unit_dir(unit: str) -> Path:
    return YAYIN / P.UNITS[unit]["sura_name"].lower() / unit


def yayinla(unit: str, n: int | None = None) -> Path:
    data = build(unit, n)
    d = unit_dir(unit)
    d.mkdir(parents=True, exist_ok=True)
    versions = sorted((int(p.stem[1:]), p) for p in d.glob("v*.json") if p.stem[1:].isdigit())
    if versions:
        last = json.loads(versions[-1][1].read_text(encoding="utf-8"))
        if last.get("icerik_sha") == data["icerik_sha"]:
            print(f"{unit}: içerik değişmedi, sürüm {versions[-1][0]} kalır")
            return versions[-1][1]
    k = (versions[-1][0] if versions else 0) + 1
    data["surum"] = k
    data["yayimlandi"] = datetime.now().isoformat(timespec="seconds")
    if versions:
        prev = json.loads(versions[-1][1].read_text(encoding="utf-8"))
        old = {blk["id"] for blk in prev["bloklar"]}
        data["onceki_surum"] = {"surum": versions[-1][0], "ayni_paragraf": sum(blk["id"] in old for blk in data["bloklar"])}
    path = d / f"v{k}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    idx_path = YAYIN / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8")) if idx_path.exists() else {"sema": SCHEMA, "birimler": {}}
    idx["birimler"][unit] = {"son": k, "yol": str(path.relative_to(YAYIN)), "ayet": data["ayet"],
                             "yayimlandi": data["yayimlandi"], "saklı": data["kunye"]["saklı"]}
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{path.relative_to(ROOT)}: {len(data['bloklar'])} paragraf, {len(data['kaynaklar'])} kaynak, "
          f"{sum(len(blk.get('isaretler', [])) for blk in data['bloklar'])} işaret, {len(data['eksik'])} eksik notu")
    return path


def goster(unit: str) -> None:
    idx = json.loads((YAYIN / "index.json").read_text(encoding="utf-8"))
    x = idx["birimler"][unit]
    data = json.loads((YAYIN / x["yol"]).read_text(encoding="utf-8"))
    from collections import Counter
    print(f"{unit} v{data['surum']} ({data['yayimlandi']}): {Counter(blk['tur'] for blk in data['bloklar'])}; "
          f"izahlı {sum('izah' in blk for blk in data['bloklar'])}; kaynak metni olan "
          f"{sum(bool(v['metin']) for v in data['kaynaklar'].values())}/{len(data['kaynaklar'])}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("yayinla")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--taslak", type=int)
    p = sub.add_parser("goster")
    p.add_argument("unit")
    a = ap.parse_args()
    if a.cmd == "yayinla":
        yayinla(a.unit, a.taslak)
    else:
        goster(a.unit)


if __name__ == "__main__":
    main()
