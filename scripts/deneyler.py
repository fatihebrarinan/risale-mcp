"""Ar-ge masasının deneyler defteri, alet ayarı ve araması (S7.2 ekleri (b), (c), (e); kullanıcının kararları,
2026-11-21). Model çağırmaz; taslak deposundan ve istem belgelerinden kendiliğinden üretilir, böylece bundan sonraki
denemeler de kendiliğinden girer.

- **Sürümler:** her istemin (taslak `hat` h1–h12, `duzeltme` d1–d3, eleştirmenler, nisbet, ölçüler, izah…) bütün
  sürümleri, `docs/d1/*-istemi.md`'lerin "Sürümler" kısmından, tarihiyle ve gerekçesiyle.
- **Deneyler:** her okuma turu (`data/d1/provalar/<birim>/tur-*.json`) bir kayıt: ne sınandı (kollar ve sürümleri),
  makinelerin ölçüleri (kör A/B, İşârât karşılaştırması), okuyucunun kararları (`data/d1/notlar/`, sabit numara; ad
  yok), birimin maliyeti ve KAYIT.md'deki kaydı (verilen karar). Aşamaların (D11–D15, D5) kendi kayıtları da.
- **Alet ayarı:** okuyucunun kararıyla makinelerin hükmü aynı mı (birim ve tur düzeyinde; okuma biriktikçe dolar).
- **Arama:** bütün taslaklarda (her birimin her taslağı) ve okuma notlarında kelime araması; aynı nükte iki birimde
  çelişiyor mu diye bakmak için (tarayıcıda, `deneyler-ara.json`).

    uv run python scripts/deneyler.py        # data/d1/masa/deneyler.html (+ deneyler.json, deneyler-ara.json)
"""
from __future__ import annotations

import html
import importlib.util
import json
import re
import sys
import time
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


P = _load("d1_prova", "d1-prova.py")
DUR = _load("d1_durum", "d1-durum.py")
MASA = P.KEEP / "masa"
DOCS = ROOT / "docs" / "d1"
KAYIT = ROOT / "KAYIT.md"
esc = html.escape


def jload(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


# ---------------------------------------------------------------- sürümler

def surumler() -> list[dict]:
    out = []
    for doc in sorted(DOCS.glob("*-istemi.md")):
        lines = doc.read_text(encoding="utf-8").splitlines()
        try:
            i = next(k for k, l in enumerate(lines) if l.strip() == "Sürümler:")
        except StopIteration:
            continue
        items, cur = [], None
        for l in lines[i + 1:]:
            if l.startswith("- "):
                cur = [l[2:]]
                items.append(cur)
            elif l.startswith("  ") and cur is not None:
                cur.append(l.strip())
            elif not l.strip():
                if items:
                    break
            else:
                break
        for it in items:
            text = " ".join(it)
            m = re.match(r"([^\s(]+(?:,\s*[^\s(]+)*)\s*(?:\(([^)]*)\))?:?\s*(.*)", text)
            ver, paren = (m.group(1), m.group(2) or "") if m else (text[:10], "")
            date = re.search(r"\d{4}-\d{2}-\d{2}", paren or text)
            out.append({"istem": doc.stem.removesuffix("-istemi"), "surum": ver.rstrip(":"),
                        "tarih": date.group(0) if date else None, "metin": text})
    return out


# ---------------------------------------------------------------- deneyler

def kayit_index() -> dict[str, str]:
    """KAYIT.md'de "- **D14.4 …**" ya da "**D15. …**" ile başlayan kayıtlar: kimlik → metin (madde sonuna kadar)."""
    lines = KAYIT.read_text(encoding="utf-8").splitlines()
    out, cur, buf = {}, None, []
    for l in lines:
        m = re.match(r"^(?:- )?\*\*((?:D|T|S|A|E|B)\d+(?:\.\d+)*[a-z]?)[ .*:]", l)
        if m or (cur and (l.startswith("- ") or l.startswith("**") or l.startswith("#"))):
            if cur and cur not in out:
                out[cur] = " ".join(x.strip() for x in buf)
            cur, buf = (m.group(1), [l]) if m else (None, [])
        elif cur:
            buf.append(l)
    if cur and cur not in out:
        out[cur] = " ".join(x.strip() for x in buf)
    return out


_READERS: dict[str, str] = {}


def reader_no(name: str | None) -> str:
    """Okuyucunun sabit numarası (ad yayımlanmaz): masadan gelenler zaten "okuyucu<n>"; eski dışa aktarmalardaki adlar
    ilk görülme sırasıyla numaralanır (dosya adları tarihli olduğu için sıra sabittir)."""
    name = name or "?"
    if re.fullmatch(r"okuyucu\d+", name):
        return name
    if name not in _READERS:
        _READERS[name] = f"okuyucu{len(_READERS) + 1}"
    return _READERS[name]


def readings(unit: str, tur: str) -> list[dict]:
    out = []
    for f in sorted((P.KEEP / "notlar").glob(f"d1-tur-{unit}-{tur}-*.json")):
        d = jload(f) or {}
        votes = [v.get("secim") for v in (d.get("ab") or {}).values() if v.get("secim")]
        out.append({"okuyucu": reader_no(d.get("reader")), "kararlar": dict(Counter(votes)), "yer": len(d.get("ab") or {}),
                    "tarih": (time.strftime("%Y-%m-%d", time.localtime(d["exported"])) if isinstance(d.get("exported"), (int, float))
                              else (d.get("exported") or "")[:10]),
                    "gerekceler": [{"yer": k.split("|")[-1], "secim": v.get("secim"), "gerekce": v.get("gerekce")}
                                   for k, v in (d.get("ab") or {}).items() if v.get("gerekce")]})
    return out


def machine(unit: str, drafts: dict[int, str]) -> dict:
    yz = P.KEEP / "provalar" / unit / "yz"
    kor = []
    for f in sorted(yz.glob("kor-olcu-*.json")):
        if f.name.endswith(".meta.json"):
            continue
        k, meta = jload(f) or {}, jload(f.with_name(f.stem + ".meta.json")) or {}
        b = k.get("butun") or {}
        win = {"A": meta.get("A"), "B": meta.get("B")}.get(b.get("tercih"), b.get("tercih"))
        kor.append({"dosya": f.stem, "A": meta.get("A"), "B": meta.get("B"), "tercih": win, "guc": b.get("guc"),
                    "surum": meta.get("surum"), "bolumler": {x.get("bolum"): x.get("tercih") for x in k.get("bolumler", [])}})
    isr = {}
    for n in drafts:
        x = jload(yz / f"isarat-karsilastirma-taslak-{n}.json")
        if x:
            isr[n] = {"butun": (x.get("butun") or {}).get("hukum"),
                      "bolumler": {b.get("bolum"): b.get("hukum") for b in x.get("bolumler", [])}}
    return {"kor": kor, "isarat": isr}


def deneyler() -> list[dict]:
    kay = kayit_index()
    out = []
    for f in sorted(P.DRAFTS.glob("*/tur-*.json"), key=lambda p: p.stat().st_mtime):
        unit, t = f.parent.name, jload(f) or {}
        tur = t.get("ad") or f.stem.removeprefix("tur-")
        drafts = {d["n"]: d["surum"] for d in DUR.drafts(unit)}
        arms = [x for x in (t.get("a"), t.get("b")) if x]
        arm_n = [int(x.split("-")[1]) for x in arms if x.split("-")[-1].isdigit()]
        total, by = DUR.cost_of(unit)
        key = tur if tur in kay else (tur.split("-")[0] if tur.split("-")[0] in kay else None)
        out.append({"birim": unit, "tur": tur, "tek": bool(t.get("tek")), "sayfa": t.get("sayfa"),
                    "kollar": [{"taslak": n, "surum": drafts.get(n)} for n in arm_n],
                    "yerler": [y.get("baslik") or y.get("ad") or y.get("id") for y in t.get("yerler", [])],
                    "dakika": t.get("dakika"), "makine": machine(unit, {n: drafts.get(n) for n in arm_n}),
                    "okumalar": readings(unit, tur), "birim_maliyeti": round(total, 1),
                    "kayit": kay.get(key, "")[:1600] if key else ""})
    return out


def asamalar() -> list[dict]:
    kay = kayit_index()
    return [{"kimlik": k, "metin": v[:2400]} for k, v in kay.items() if re.fullmatch(r"D1[1-5]|D5|D5\.0(\.\d+)?", k)]


def ayar(exps: list[dict]) -> list[dict]:
    """Okuyucu ile makineler: A/B turlarında okuyucunun çoğunluğu kör ölçünün tercihiyle aynı mı; tek turlarda
    okuyucunun hükümleri ile İşârât karşılaştırmasının bütün hükmü."""
    rows = []
    for e in exps:
        votes = Counter()
        for r in e["okumalar"]:
            votes.update(r["kararlar"])
        if not votes:
            continue
        row = {"birim": e["birim"], "tur": e["tur"], "okuyucu": dict(votes)}
        if len(e["kollar"]) == 2:
            names = {f"taslak-{k['taslak']}": k["taslak"] for k in e["kollar"]}
            arm_votes = Counter({names[k]: v for k, v in votes.items() if k in names}).most_common()
            tie = len(arm_votes) > 1 and arm_votes[0][1] == arm_votes[1][1]
            top = arm_votes[0][0] if arm_votes and not tie else None
            kor = next((k for k in e["makine"]["kor"] if {k["A"], k["B"]} == set(names.values())), None)
            row |= {"okuyucu_secti": top, "kor_secti": kor and kor["tercih"],
                    "ayni": None if not kor or top is None else kor["tercih"] == top}
        else:
            n = e["kollar"][0]["taslak"] if e["kollar"] else None
            isr = e["makine"]["isarat"].get(n, {})
            row |= {"isarat_hukmu": isr.get("butun")}
        rows.append(row)
    return rows


# ---------------------------------------------------------------- kayma görünümü

def kayma() -> list[dict]:
    """Ardışık birimlerin garaz özetleri (1–33 İşârât'tan, D5'te taslaktan; ikisi de yapay zekâ özeti) ve yayımlanan
    taslağın birinci vechinin (öncesiyle nazım) ilk Türkçe paragrafı: zincir kayıyor mu, bağlar tutuyor mu."""
    isr = {x["birim"]: x["ozet"] for x in (jload(P.KEEP / "garaz" / "isarat-bakara.json") or {}).get("ozetler", [])}
    d5 = (jload(P.KEEP / "garaz" / "d5-bakara.json") or {}).get("ozetler", {})
    idx = (jload(P.KEEP / "yayin" / "index.json") or {}).get("birimler", {})
    out = []
    for u in P.d5_units():
        uid = u["id"]
        v1 = None
        if uid in idx:
            y = jload(P.KEEP / "yayin" / idx[uid]["yol"]) or {}
            v1 = next((b["metin"] for b in y.get("bloklar", []) if b["bolum"] == "V1" and b["tur"] in ("tercume", "tr")), None)
        if uid in isr or uid in d5 or v1:
            out.append({"birim": uid, "ayet": u["ayet"], "isarat_ozeti": isr.get(uid), "taslak_ozeti": d5.get(uid),
                        "birinci_vecih": v1})
    return out


# ---------------------------------------------------------------- arama dizini

def search_index() -> list[dict]:
    """Bütün taslakların Türkçe paragrafları ve okuma gerekçeleri: [{b, n, s, c, t}] (birim, taslak, sürüm, çapa, metin)."""
    Y = _load("d1_yz", "d1-yz.py")
    out = []
    for d in sorted(p for p in P.DRAFTS.iterdir() if p.is_dir() and p.name.replace("-", "").isdigit()):
        for t in DUR.drafts(d.name):
            try:
                blocks, _ = Y.draft_blocks(d.name, t["n"])
            except Exception:                 # noqa: BLE001 (eski biçim)
                continue
            for a, lang, _, text in blocks:
                if lang == "tr":
                    out.append({"b": d.name, "n": t["n"], "s": t["surum"], "c": a, "t": text})
    for f in sorted((P.KEEP / "notlar").glob("d1-tur-*.json")):
        d = jload(f) or {}
        for k, v in (d.get("ab") or {}).items():
            if v.get("gerekce"):
                out.append({"b": d.get("unit"), "n": None, "s": "okuma " + str(d.get("tur")), "c": k.split("|")[-1],
                            "t": v["gerekce"]})
    return out


# ---------------------------------------------------------------- sayfa

PAGE = """<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,
initial-scale=1"><meta name="robots" content="noindex, nofollow"><title>Deneyler Defteri</title><style>__CSS__
nav.tabs { display: flex; gap: 4px; border-bottom: 1px solid var(--line); margin: 8px 0 14px; overflow-x: auto; }
nav.tabs a { padding: 8px 12px; color: var(--muted); text-decoration: none; border-bottom: 2px solid transparent; }
nav.tabs a.on { color: var(--fg); border-bottom-color: var(--accent); font-weight: 600; }
.row { background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 8px 12px; margin: 8px 0; }
table.t { width: 100%; border-collapse: collapse; font-size: .85rem; } table.t td, table.t th { border-top: 1px solid
var(--line); padding: 4px 6px; text-align: left; vertical-align: top; }
input.q { width: 100%; padding: 6px 9px; font: inherit; border: 1px solid var(--line); border-radius: 6px;
background: var(--card); color: var(--fg); } mark { background: var(--warn-soft); color: inherit; }
</style></head><body><main>
<p class="small"><a href="./">← masa</a></p><h1>Deneyler defteri</h1>
<p class="small muted">Taslak deposundan ve istem belgelerinden kendiliğinden üretilir (`scripts/deneyler.py`); yeni
denemeler kendiliğinden girer. Okuyucular sabit numarayla.</p>
<nav class="tabs"><a href="#deneyler" data-t="deneyler">Deneyler</a><a href="#surumler" data-t="surumler">Sürümler</a>
<a href="#asamalar" data-t="asamalar">Aşamalar</a><a href="#ayar" data-t="ayar">Alet ayarı</a><a href="#kayma" data-t="kayma">Kayma</a><a href="#ara" data-t="ara">Arama</a></nav>
__BODY__
<section id="ara" hidden><input class="q" id="q" placeholder="Bütün taslaklarda ve okuma gerekçelerinde ara (en az 3 harf)">
<p class="small muted" id="qn"></p><div id="qr"></div></section>
<p class="small muted">Üretildi __WHEN__</p>
</main><script>
function show(t) { t = t || 'deneyler'; for (const s of document.querySelectorAll('main > section')) s.hidden = s.id !== t;
  for (const a of document.querySelectorAll('nav.tabs a')) a.classList.toggle('on', a.dataset.t === t); }
addEventListener('hashchange', () => show(location.hash.slice(1))); show(location.hash.slice(1));
let IDX = null;
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
const fold = s => s.toLocaleLowerCase('tr').normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').replace(/ı/g, 'i');
document.getElementById('q').addEventListener('input', async e => {
  const q = fold(e.target.value.trim());
  if (q.length < 3) { document.getElementById('qr').innerHTML = ''; return; }
  if (!IDX) { IDX = await (await fetch('deneyler-ara.json', {cache: 'no-cache'})).json(); IDX.forEach(x => x.f = fold(x.t)); }
  const hits = IDX.filter(x => x.f.includes(q));
  document.getElementById('qn').textContent = hits.length + ' sonuç' + (hits.length > 200 ? ' (ilk 200)' : '');
  document.getElementById('qr').innerHTML = hits.slice(0, 200).map(x => {
    const i = x.f.indexOf(q), s = Math.max(0, i - 120);
    const snip = esc(x.t.slice(s, i)) + '<mark>' + esc(x.t.slice(i, i + q.length)) + '</mark>' + esc(x.t.slice(i + q.length, i + q.length + 160));
    return `<div class="row small"><b>Bakara ${esc(x.b)}</b> · ${x.n ? 'taslak ' + x.n + ' (' + esc(x.s) + ')' : esc(x.s)} · ${esc(x.c)}${x.n ? ` · <a href="birim.html#/${esc(x.b)}/~hepsi">aç</a>` : ''}<br>${s ? '…' : ''}${snip}…</div>`;
  }).join('');
});
</script></body></html>
"""


def render(data: dict) -> str:
    L = ['<section id="deneyler">']
    for e in reversed(data["deneyler"]):
        arms = ", ".join(f"taslak {k['taslak']} ({esc(str(k['surum']))})" for k in e["kollar"])
        m = e["makine"]
        L.append(f'<div class="row"><b>{esc(e["tur"])}</b> · Bakara {esc(e["birim"])} · '
                 f'{"tek taslak" if e["tek"] else "A/B"}: {arms or "—"}'
                 + (f' · <a href="{esc(e["sayfa"])}">okuma sayfası</a>' if e.get("sayfa") else "")
                 + f'<div class="small muted">{len(e["yerler"])} yer: {esc("; ".join(map(str, e["yerler"]))[:300])} · '
                 f'birimin bütün harcaması ≈{e["birim_maliyeti"]} $</div>')
        mm = [f'kör A/B ({esc(str(k["surum"]))}): taslak {k["A"]} – {k["B"]} → <b>{esc(str(k["tercih"]))}</b> ({esc(str(k["guc"]))})'
              for k in m["kor"]]
        mm += [f'İşârât karşılaştırması, taslak {n}: <b>{esc(str(v["butun"]))}</b>' for n, v in m["isarat"].items()]
        if mm:
            L.append('<div class="small">Makineler: ' + " · ".join(mm) + "</div>")
        for r in e["okumalar"]:
            L.append(f'<div class="small">Okuma ({esc(str(r["okuyucu"]))}, {esc(r["tarih"])}): '
                     + ", ".join(f"{esc(str(k))} {v}" for k, v in r["kararlar"].items()) + "</div>")
            if r["gerekceler"]:
                L.append("<details><summary class=\"small\">gerekçeler</summary>" + "".join(
                    f'<div class="small"><b>{esc(g["yer"])}</b> ({esc(str(g["secim"]))}): {esc(g["gerekce"])}</div>'
                    for g in r["gerekceler"]) + "</details>")
        if e["kayit"]:
            L.append(f'<details><summary class="small">kayıt (KAYIT.md)</summary><div class="small">{esc(e["kayit"])}</div></details>')
        L.append("</div>")
    L.append("</section>")
    L.append('<section id="surumler" hidden>')
    by = {}
    for s in data["surumler"]:
        by.setdefault(s["istem"], []).append(s)
    for ist, rows in by.items():
        L.append(f"<h2>{esc(ist)}</h2>")
        L += [f'<div class="row small"><b>{esc(r["surum"])}</b> {esc(r["tarih"] or "")}<br>{esc(r["metin"])}</div>' for r in rows]
    L.append("</section>")
    L.append('<section id="asamalar" hidden>')
    L += [f'<div class="row small"><b>{esc(a["kimlik"])}</b><br>{esc(a["metin"])}</div>' for a in data["asamalar"]]
    L.append("</section>")
    L.append('<section id="ayar" hidden><p class="small muted">Okuyucunun kararıyla makinelerin hükmü (okuma '
             'biriktikçe dolar). A/B: okuyucunun çoğunlukla seçtiği taslak ile kör ölçünün seçtiği; tek taslak: '
             'okuyucunun hükümleri ile İşârât karşılaştırmasının bütün hükmü.</p><table class="t">'
             "<tr><th>Tur</th><th>Okuyucu</th><th>Makine</th><th>Aynı mı</th></tr>")
    known = [r["ayni"] for r in data["ayar"] if r.get("ayni") is not None]
    if known:
        L[-1] = L[-1].replace('<table class="t">', f'<p class="small">Kör A/B ile okuyucu: {sum(known)}/{len(known)} '
                              'turda aynı taslağı seçti.</p><table class="t">')
    for r in data["ayar"]:
        mach = (f'kör: {r.get("kor_secti")}' if "kor_secti" in r else f'İşârât: {r.get("isarat_hukmu")}')
        same = {True: "✓", False: "✗", None: "—"}[r.get("ayni")] if "ayni" in r else "—"
        L.append(f'<tr><td>{esc(r["tur"])} · {esc(r["birim"])}</td><td>'
                 + esc(", ".join(f"{k} {v}" for k, v in r["okuyucu"].items()))
                 + (f' → {esc(str(r.get("okuyucu_secti") or "berabere"))}' if "okuyucu_secti" in r else "")
                 + f"</td><td>{esc(mach)}</td><td>{same}</td></tr>")
    L.append("</table></section>")
    L.append('<section id="kayma" hidden><p class="small muted">Ardışık birimler: garaz özeti (1–33 İşârât\'tan, D5\'te '
             'taslaktan; ikisi de yapay zekâ özeti, iki cümle) ve yayımlanan taslağın birinci vechinin (öncesiyle nazım) ilk '
             'paragrafı. Zincir kayıyor mu, önceki birime bağ tutuyor mu.</p>')
    for k in data["kayma"]:
        a, b = k["ayet"]
        L.append(f'<div class="row small"><b><a href="birim.html#/{esc(k["birim"])}">Bakara {a}{"–" + str(b) if b != a else ""}</a></b>'
                 + (f'<br><span class="muted">İşârât\'ın garazı:</span> {esc(k["isarat_ozeti"])}' if k["isarat_ozeti"] else "")
                 + (f'<br><span class="muted">Taslağın garazı:</span> {esc(k["taslak_ozeti"])}' if k["taslak_ozeti"] else "")
                 + (f'<br><span class="muted">Birinci vecih:</span> {esc(k["birinci_vecih"][:600])}' if k["birinci_vecih"] else "")
                 + "</div>")
    L.append("</section>")
    return "\n".join(L)


def yaz() -> list[Path]:
    exps = deneyler()
    data = {"sema": "deneyler/1", "uretildi": time.time(), "surumler": surumler(), "deneyler": exps,
            "asamalar": asamalar(), "ayar": ayar(exps), "kayma": kayma()}
    S = _load("d1_d5_sayfa", "d1-d5-sayfa.py")
    MASA.mkdir(parents=True, exist_ok=True)
    out = [MASA / "deneyler.json", MASA / "deneyler-ara.json", MASA / "deneyler.html"]
    out[0].write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    out[1].write_text(json.dumps(search_index(), ensure_ascii=False), encoding="utf-8")
    out[2].write_text(PAGE.replace("__CSS__", S.CSS).replace("__BODY__", render(data))
                      .replace("__WHEN__", time.strftime("%Y-%m-%d %H:%M")), encoding="utf-8")
    return out


if __name__ == "__main__":
    for p in yaz():
        print(f"{p.relative_to(ROOT)} ({p.stat().st_size // 1024} KB)")
