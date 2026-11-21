"""S7c.4 sınaması: İşârâtü'l-İ'câz'ın Arapça aslıyla Abdülmecid Nursî tercümesini cümle düzeyinde eşlemek mümkün mü
(kullanıcının şartı, 2026-11-21: "mümkün olmayabilir"; önce sınama, karar sonra). Model çağırmaz.

Yöntem (program): iki metin aynı bölümde, aynı sırayla gider; tercüme Arapça alıntıları (âyet, lafız) olduğu gibi taşır.
1. Her cümlenin Arapça kelimeleri harekesiz, eliflenmiş biçime indirilir (tercümede yalnız içindeki Arapça parçalar).
2. Benzerlik: ortak ikili kelime dizileri (nadir olanlar ağır) ve ortak nadir kelimeler.
3. Hizalama: sıra korunarak dinamik programlama (Gale–Church gibi): 1–1, 1–2, 2–1, 2–2, 1–3, 3–1, 1–0, 0–1;
   uzunluk oranı cezası (birimin kendi tercüme oranıyla), benzerlik ödülü.

Ölçü: envanterin kalemleri (D7; modelin her nükteye bağladığı Arapça ve Türkçe cümleler) yarı-altın veridir:
kalemin Arapça cümlelerinin eşlendiği Türkçe cümlelerden biri kalemin Türkçe cümlelerindense "tutar".
Kalemler nükte düzeyindedir, cümle düzeyinde birebir değildir: ölçü bir alt sınırdır, örneklem kullanıcıya.

    uv run python scripts/isarat-esleme.py 13 28 30          # rapor + data/d1/masa/isarat-esleme.html (örneklem)
    uv run python scripts/isarat-esleme.py --hepsi
    uv run python scripts/isarat-esleme.py --model 13 28 30   # model ile (Opus, araçsız); d1-arka.sh ile başlatılır
    uv run python scripts/isarat-esleme.py --butun            # Fâtiha ve Bakara'nın bütün bölümleri, model ile
                                                              # (kullanıcının kararı, 2026-11-21) → esleme.json

`esleme.json`: {Arapça cümle kimliği: [Türkçe cümle kimlikleri]} (karşılığı olmayan cümle listede yok). Masa ve platform
Türkçe kipte İşârât'a atıfların kaynak kutusunda Abdülmecid Nursî tercümesini bundan gösterir; eşlemenin yapay zekânın
olduğu yazılır.
"""
from __future__ import annotations

import argparse
import html
import importlib.util
import json
import math
import random
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, file: str):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / file)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


Y = _load("d1_yz", "d1-yz.py")
P = Y.P
OUT = P.KEEP / "isarat-esleme"
HAR = re.compile(r"[ً-ٰٟۖ-ۭـ]")
ARW = re.compile(r"[ء-ي٠-٩ٱ-ۓ]+")


def norm(t: str) -> str:
    t = HAR.sub("", t)
    t = re.sub("[أإآٱ]", "ا", t).replace("ى", "ي").replace("ة", "ه")
    return re.sub(r"[^ء-ي]", "", t)


def words(text: str) -> list[str]:
    out = []
    for w in ARW.findall(text):
        n = norm(w)
        if len(n) >= 2:
            out.append(n[1:] if n[:1] in "وف" and len(n) > 3 else n)       # baştaki و/ف atılır
    return out


def feats(ws: list[str]) -> set:
    return set(ws) | {a + " " + b for a, b in zip(ws, ws[1:])}


LENW = 2.0                                          # uzunluk cezasının ağırlığı
# geçişler ve maliyetleri; envanterle küçük bir taramada en iyisi (2026-11-21: tam %77, ±1 cümle %88; 666 kalem)
MOVES = [(1, 1, 0), (1, 2, .6), (2, 1, .6), (2, 2, 1.2), (1, 3, 1.4), (3, 1, 1.4), (1, 4, 2.1), (1, 0, 4.0), (0, 1, 3.0)]


def align(ar: list[str], tr: list[str]) -> list[tuple[list[int], list[int]]]:
    A = [feats(words(t)) for t in ar]
    T = [feats(words(t)) for t in tr]
    df = Counter(f for s in A + T for f in s)
    def idf(f): return math.log(1 + (len(A) + len(T)) / df[f]) * (1.6 if " " in f else 1.0)
    la = [max(len(t), 1) for t in ar]
    lt = [max(len(t), 1) for t in tr]
    ratio = sum(lt) / sum(la)
    def sim(ii, jj):
        a = set().union(*(A[i] for i in ii)) if ii else set()
        t = set().union(*(T[j] for j in jj)) if jj else set()
        return sum(idf(f) for f in a & t)
    def lenpen(ii, jj):
        x, y = sum(la[i] for i in ii) * ratio, sum(lt[j] for j in jj)
        return LENW * abs(math.log(y / x))
    moves = MOVES
    n, m = len(ar), len(tr)
    best = [[-1e18] * (m + 1) for _ in range(n + 1)]
    back = [[None] * (m + 1) for _ in range(n + 1)]
    best[0][0] = 0.0
    for i in range(n + 1):
        for j in range(m + 1):
            if best[i][j] <= -1e17:
                continue
            for di, dj, cost in moves:
                ni, nj = i + di, j + dj
                if ni > n or nj > m:
                    continue
                ii, jj = list(range(i, ni)), list(range(j, nj))
                sc = best[i][j] - cost + (sim(ii, jj) - lenpen(ii, jj) if di and dj else 0)
                if sc > best[ni][nj]:
                    best[ni][nj], back[ni][nj] = sc, (i, j)
    out, i, j = [], n, m
    while (i, j) != (0, 0):
        pi, pj = back[i][j]
        out.append((list(range(pi, i)), list(range(pj, j))))
        i, j = pi, pj
    return out[::-1]


MODEL_ISTEM = """Aşağıda İşârâtü'l-İ'câz'ın bir bölümü iki dilde var: Bediüzzaman'ın Arapça aslı (A1, A2…) ve Abdülmecid
Nursî'nin Türkçe tercümesi (T1, T2…), ikisi de cümle cümle ve sırasıyla. Görev: cümleleri eşle. Tercüme serbesttir: bir
Arapça cümle birkaç Türkçe cümleye bölünebilir, iki Arapça cümle tek Türkçe cümlede birleşebilir; tercüme Arapçada
olmayan başlıklar, soru-cevaplar ("S –", "C –") ve açıklamalar ekleyebilir; nadiren Arapçanın bir cümlesi tercümede
olmayabilir.

Kurallar: sıra korunur (gruplar art arda gelir, geri dönmez); her A ve her T tam bir gruba girer; karşılığı olmayan
Türkçe cümle `{{"a": [], "t": [n]}}`, Türkçesi olmayan Arapça cümle `{{"a": [n], "t": []}}`. Grubu olabildiğince
küçük tut (cümle düzeyi); yalnız anlam gerçekten bölünmüşse birleştir. Emin olmadığın grupta "emin": false.

Yalnız JSON döndür: {{"gruplar": [{{"a": [1], "t": [1, 2], "emin": true}}, ...]}}

---- ARAPÇA ----
{ar}

---- TÜRKÇE ----
{tr}
"""


def model_align(unit: str) -> list[tuple[list[int], list[int]]] | None:
    h = Y.hidden(unit)
    ar, tr = h["ar"], h["tr"]
    stem = OUT / f"{unit}-model"
    prompt = MODEL_ISTEM.format(ar="\n".join(f"A{i + 1}. {r[2]}" for i, r in enumerate(ar)),
                                tr="\n".join(f"T{j + 1}. {r[2]}" for j, r in enumerate(tr)))
    data = json.loads(stem.with_suffix(".json").read_text(encoding="utf-8")) if stem.with_suffix(".json").exists() \
        else Y.run_model(prompt, "opus", stem, {"gorev": "isarat-esleme", "birim": unit})
    if not data:
        return None
    groups, ia, it, bad = [], 0, 0, 0
    for g in data.get("gruplar", []):
        a = [x - 1 for x in g.get("a", [])]
        t = [x - 1 for x in g.get("t", [])]
        if a != list(range(ia, ia + len(a))) or t != list(range(it, it + len(t))):
            bad += 1                                     # sırayı bozan grup: kalan kısım sırayla eklenir
            continue
        groups.append((a, t))
        ia, it = ia + len(a), it + len(t)
    if ia < len(ar) or it < len(tr):
        groups.append((list(range(ia, len(ar))), list(range(it, len(tr)))))
    if bad:
        print(f"  {unit}: modelin {bad} grubu sırayı bozuyordu, atıldı")
    return groups


# ---------------------------------------------------------------- bütün İşârât (Fâtiha ve Bakara)

GENEL_DB = P.GENEL_DB
TR_W, AR_W = "isaratul-icaz", "isaratul-icaz-arabi"
SURELER = ("sure-i-fatiha", "sure-i-bakara")


def section_pairs() -> list[tuple[str, list[str], list[str]]]:
    """(ad, Arapça bölümler, Türkçe bölümler): aynı kimlikle; Türkçede 21 ve 22 ayrı, Arapçada tek bölüm."""
    import sqlite3
    c = sqlite3.connect(f"file:{GENEL_DB}?mode=ro", uri=True)
    out = []
    for sure in SURELER:
        kids = {w: [r[0] for r in c.execute("SELECT id FROM nodes WHERE parent_id = ? ORDER BY ord", (f"{w}/{sure}",))]
                for w in (AR_W, TR_W)}
        tr_tail = {k.rsplit("/", 1)[1]: k for k in kids[TR_W]}
        for a in kids[AR_W]:
            tail = a.rsplit("/", 1)[1]
            if tail in tr_tail:
                out.append((f"{sure}/{tail}", [a], [tr_tail[tail]]))
            elif tail.startswith("21-22"):
                out.append((f"{sure}/{tail}", [a], [tr_tail["21"], tr_tail["22"]]))
    return out


def section_sentences(nodes: list[str]) -> list[tuple[str, str]]:
    import sqlite3
    c = sqlite3.connect(f"file:{GENEL_DB}?mode=ro", uri=True)
    out = []
    for nid in nodes:
        work = nid.split("/")[0]
        o, lo = c.execute("SELECT ord, last_ord FROM nodes WHERE id = ?", (nid,)).fetchone()
        out += c.execute("""SELECT s.id, s.text FROM sentences s JOIN nodes n ON n.id = s.node_id
                            WHERE n.work = ? AND n.ord BETWEEN ? AND ? ORDER BY s.seq""", (work, o, lo)).fetchall()
    return out


def butun() -> None:
    from concurrent.futures import ThreadPoolExecutor
    base = OUT / "butun"
    base.mkdir(parents=True, exist_ok=True)
    pairs = section_pairs()
    def one(item):
        name, an, tn = item
        ar, tr = section_sentences(an), section_sentences(tn)
        stem = base / name.replace("/", "_")
        if stem.with_suffix(".json").exists():
            data = json.loads(stem.with_suffix(".json").read_text(encoding="utf-8"))
        else:
            prompt = MODEL_ISTEM.format(ar="\n".join(f"A{i + 1}. {t}" for i, (_, t) in enumerate(ar)),
                                        tr="\n".join(f"T{j + 1}. {t}" for j, (_, t) in enumerate(tr)))
            data = Y.run_model(prompt, "opus", stem, {"gorev": "isarat-esleme", "bolum": name})
        return name, ar, tr, data
    mapping, report = {}, []
    with ThreadPoolExecutor(3) as ex:
        for name, ar, tr, data in ex.map(one, pairs):
            if not data:
                report.append(f"{name}: model cevabı yok")
                continue
            ia = it = bad = 0
            for g in data.get("gruplar", []):
                a = [x - 1 for x in g.get("a", [])]
                t = [x - 1 for x in g.get("t", [])]
                if a != list(range(ia, ia + len(a))) or t != list(range(it, it + len(t))) or ia + len(a) > len(ar) \
                        or it + len(t) > len(tr):
                    bad += 1
                    continue
                for i in a:
                    if t:
                        mapping[ar[i][0]] = [tr[j][0] for j in t]
                ia, it = ia + len(a), it + len(t)
            report.append(f"{name}: {len(ar)} Arapça, {len(tr)} Türkçe cümle; eşlenen Arapça {sum(1 for x, _ in ar if x in mapping)}"
                          + (f"; sırayı bozan {bad} grup atıldı" if bad else "") + (f"; sonda eşlenmemiş A{ia + 1}…" if ia < len(ar) else ""))
    (OUT / "esleme.json").write_text(json.dumps(mapping, ensure_ascii=False, indent=0), encoding="utf-8")
    (OUT / "esleme-rapor.md").write_text("# İşârât: Arapça → Türkçe cümle eşlemesi (model)\n\n" + "\n".join(f"- {x}" for x in report) + "\n",
                                         encoding="utf-8")
    print("\n".join(report))
    print(f"{len(mapping)} Arapça cümle eşlendi → {(OUT / 'esleme.json').relative_to(ROOT)}")


def unit_result(unit: str, model: bool = False) -> dict:
    h = Y.hidden(unit)
    ar, tr = h["ar"], h["tr"]                           # [(istem kimliği a016, db kimliği, metin, paragraf)]
    groups = model_align(unit) if model else align([r[2] for r in ar], [r[2] for r in tr])
    if groups is None:
        raise SystemExit(f"{unit}: model eşlemesi yok")
    a2t: dict[str, set] = {}
    for ii, jj in groups:
        for i in ii:
            a2t[ar[i][0]] = {tr[j][0] for j in jj}
    env = json.loads((Y.out_dir(unit) / "envanter.json").read_text(encoding="utf-8"))
    ok = tot = 0
    for k in env["kalemler"]:
        if not k.get("ar") or not k.get("tr") or k.get("yalniz_tercume"):
            continue
        tot += 1
        got = set().union(*(a2t.get(a, set()) for a in k["ar"]))
        ok += bool(got & set(k["tr"]))
    shapes = Counter(f"{len(ii)}-{len(jj)}" for ii, jj in groups)
    return {"birim": unit, "model": model, "ar": len(ar), "tr": len(tr), "gruplar": len(groups), "bicim": dict(shapes),
            "envanter": [ok, tot],
            "ciftler": [{"ar": [ar[i][1] for i in ii], "tr": [tr[j][1] for j in jj],
                         "ar_t": " ".join(ar[i][2] for i in ii), "tr_t": " ".join(tr[j][2] for j in jj)}
                        for ii, jj in groups]}


def page(results: list[dict], n: int = 40) -> str:
    rnd = random.Random(2026_11_21)
    pool = [(r["birim"], c) for r in results for c in r["ciftler"] if c["ar"] and c["tr"]]
    sample = rnd.sample(pool, min(n, len(pool)))
    sample.sort(key=lambda x: [int(p) for p in x[0].split("-")])
    rows = []
    for k, (u, c) in enumerate(sample, 1):
        rows.append(f'<div class="pair"><div class="no">{k}. Bakara {html.escape(u)} · {len(c["ar"])} Arapça ↔ '
                    f'{len(c["tr"])} Türkçe cümle</div><div class="cols"><p class="ar">{html.escape(c["ar_t"])}</p>'
                    f'<p class="tr">{html.escape(c["tr_t"])}</p></div></div>')
    stats = "".join(f'<tr><td>Bakara {html.escape(r["birim"])}</td><td>{r["ar"]}</td><td>{r["tr"]}</td>'
                    f'<td>{r["envanter"][0]}/{r["envanter"][1]}</td><td>{html.escape(str(r["bicim"]))}</td></tr>'
                    for r in results)
    return f"""<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,
initial-scale=1"><meta name="robots" content="noindex, nofollow"><title>İşârât Eşleme Sınaması</title><style>
:root {{ --bg:#fbfaf7; --fg:#1d1d1b; --muted:#6b6a66; --line:#dcd8cf; --card:#fff; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#161614; --fg:#e8e6e1; --muted:#9c9a94; --line:#34332f; --card:#1f1e1b; }} }}
body {{ margin:0; background:var(--bg); color:var(--fg); font:15px/1.6 system-ui,sans-serif; }}
main {{ padding: 12px 16px 60px; }} .muted {{ color:var(--muted); }} table {{ border-collapse: collapse; font-size:.85rem; }}
td, th {{ border-top:1px solid var(--line); padding:3px 8px; text-align:left; }}
.pair {{ background:var(--card); border:1px solid var(--line); border-radius:8px; padding:6px 10px; margin:10px 0; }}
.no {{ font-size:.78rem; color:var(--muted); }} .cols {{ display:grid; grid-template-columns:1fr 1fr; gap:14px; }}
@media (max-width:760px) {{ .cols {{ grid-template-columns:1fr; }} }}
.ar {{ direction:rtl; text-align:right; font-family:"Noto Naskh Arabic","Amiri",serif; font-size:1.15rem; line-height:1.9; margin:0; }}
.tr {{ font-family:"Noto Serif",Georgia,serif; margin:0; }}
</style></head><body><main><p class="small"><a href="./">← masa</a></p>
<h1>İşârât: Arapça aslı ile Abdülmecid Nursî tercümesi, cümle düzeyinde eşleme sınaması</h1>
<p class="muted">S7c.4. {"Eşleme modelle (Opus, araçsız)" if any(r.get("model") for r in results) else "Eşleme programla (model yok): iki metnin ortak Arapça sözleri çapa, aradakiler sıra ve uzunlukla"}. Öbür sayfa: <a href="isarat-esleme.html">program</a> · <a href="isarat-esleme-model.html">model</a>.
Envanter sütunu: modelin nükteye bağladığı Arapça ve Türkçe cümlelerle uyuşan kalem sayısı (alt sınır; kalemler nükte
düzeyinde). Aşağıda rastgele {len(sample)} eşleme: sol Arapça, sağ tercüme. Soru: eşlemeler cümle düzeyinde doğru mu?</p>
<table><tr><th>Birim</th><th>Arapça cümle</th><th>Türkçe cümle</th><th>Envanter</th><th>Eşleme biçimleri</th></tr>{stats}</table>
{''.join(rows)}</main></body></html>
"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("units", nargs="*")
    ap.add_argument("--hepsi", action="store_true")
    ap.add_argument("--model", action="store_true", help="model ile eşle (Opus); program eşlemesiyle karşılaştırılır")
    ap.add_argument("--butun", action="store_true", help="Fâtiha ve Bakara'nın bütün bölümleri, model ile → esleme.json")
    a = ap.parse_args()
    if a.butun:
        butun()
        return
    units = a.units or []
    if a.hepsi:
        units = [u for u in P.UNITS if not P.UNITS[u].get("d5") and (Y.out_dir(u) / "envanter.json").exists()]
    OUT.mkdir(parents=True, exist_ok=True)
    results = []
    for u in units:
        r = unit_result(u, a.model)
        results.append(r)
        (OUT / f"{u}{'-model-sonuc' if a.model else ''}.json").write_text(json.dumps(r, ensure_ascii=False, indent=1),
                                                                          encoding="utf-8")
        ok, tot = r["envanter"]
        print(f"{u}{' (model)' if a.model else ''}: {r['ar']} Arapça, {r['tr']} Türkçe cümle; {r['gruplar']} grup "
              f"{r['bicim']}; envanter {ok}/{tot} (%{100 * ok / max(tot, 1):.0f})")
    out = P.KEEP / "masa" / ("isarat-esleme-model.html" if a.model else "isarat-esleme.html")
    out.write_text(page(results), encoding="utf-8")
    print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
