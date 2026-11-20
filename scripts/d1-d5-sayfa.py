"""D5'in okuma sayfası (PLANLAR D5; kullanıcının kararı, 2026-11-21: D5.1 üretimin aynısı): bir birimin son taslağı,
tercümesi ve izahı; kalite kapısının yaptıkları (karşılanan ve reddedilen notlar); eleştirmenin eksik notları
(düzeltmeye girmedi). İşârât yok (D5 birimlerinde İşârât'ın bu âyetleri yok). S7'nin okuma platformunun ilk hâli.

    uv run python scripts/d1-d5-sayfa.py 34 [--taslak 4]     # data/d1/masa/d5-<birim>.html
"""
from __future__ import annotations

import argparse
import html
import importlib.util
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / file)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


P = _load("d1_prova", "d1-prova.py")
Y = _load("d1_yz", "d1-yz.py")
MASA = P.KEEP / "masa"
STAMP_RE = re.compile(r"Yapay zekâ tercümesi(?: \(alıntının\))?: ?$")

CSS = """
:root { --bg: #fbfaf7; --fg: #1d1d1b; --muted: #6b6a66; --line: #dcd8cf; --card: #ffffff; --soft: #f3f1ec;
        --accent: #1f5c3f; --ai: #5a4a8a; --ai-soft: #eeebf7; --bad: #a3271f; --src: #1f4f7a; --src-soft: #e3eef8;
        --warn-soft: #fdf0dc; --q: #f6f2e8; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #161614; --fg: #e8e6e1; --muted: #9c9a94; --line: #34332f; --card: #1f1e1b; --soft: #26251f;
  --accent: #7cc49d; --ai: #b9a8ee; --ai-soft: #2a2540; --bad: #f08a80; --src: #8cc0ef; --src-soft: #18293a;
  --warn-soft: #3a2a14; --q: #24221c; } }
:root[data-theme="dark"] { --bg: #161614; --fg: #e8e6e1; --muted: #9c9a94; --line: #34332f; --card: #1f1e1b;
  --soft: #26251f; --accent: #7cc49d; --ai: #b9a8ee; --ai-soft: #2a2540; --bad: #f08a80; --src: #8cc0ef;
  --src-soft: #18293a; --warn-soft: #3a2a14; --q: #24221c; }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--fg); font: 15px/1.65 system-ui, "Noto Sans", sans-serif; }
main { max-width: 860px; margin: 0 auto; padding: 12px 16px 80px; }
h1 { font-size: 1.15rem; margin: 10px 0 4px; } h2 { font-size: 1.05rem; margin: 26px 0 8px; color: var(--accent); }
h3 { font-size: .95rem; margin: 18px 0 6px; }
.muted { color: var(--muted); } .small { font-size: .82rem; }
.ar { font-family: "Noto Naskh Arabic", "Amiri", "Scheherazade New", serif; direction: rtl; text-align: right;
      font-size: 1.22rem; line-height: 2.05; margin: 10px 0 2px; }
.tr { font-family: "Noto Serif", "DejaVu Serif", Georgia, serif; margin: 2px 0 6px; }
.lab { font-size: .72rem; color: var(--ai); letter-spacing: .02em; }
.quote { background: var(--q); border-left: 3px solid var(--line); padding: 4px 10px; border-radius: 4px; margin: 6px 0; }
.izah { background: var(--ai-soft); border-radius: 8px; padding: 6px 10px; margin: 4px 0 12px; font-size: .93rem; }
.box { background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 8px 14px; margin: 10px 0; }
.warn { background: var(--warn-soft); }
sup.n { color: var(--src); cursor: help; font-size: .72em; }
details > summary { cursor: pointer; } details { margin: 6px 0; }
.note { border-top: 1px dashed var(--line); padding: 6px 0; font-size: .9rem; }
.note:first-of-type { border-top: 0; }
ol.src { padding-left: 1.6em; font-size: .88rem; } ol.src li { margin: 3px 0; }
.tag { display: inline-block; font-size: .72rem; border: 1px solid var(--line); border-radius: 10px; padding: 0 7px;
       color: var(--muted); margin-right: 4px; }
"""


def esc(t: str) -> str:
    return html.escape(t or "")


def marks(t: str, sources: dict) -> str:
    """[n] kaynak işaretleri: üstüne gelince kaynakça satırı."""
    out = esc(t)
    return re.sub(r"\[(\d+)\]", lambda m: f'<sup class="n" title="{esc(sources.get(m.group(1), ""))}">[{m.group(1)}]</sup>',
                  out).replace("\n", "<br>")


def chain(unit: str, son: int) -> list[tuple[int, int, str]]:
    """Son taslağa giden düzeltmeler [(kaynak, yeni, not türü)], baştan sona."""
    reg_path = P.DRAFTS / unit / "duzeltmeler.json"
    reg = json.loads(reg_path.read_text(encoding="utf-8")) if reg_path.exists() else {}
    out, cur = [], str(son)
    while cur in reg:
        r = reg[cur]
        out.append((r["kaynak"], int(cur), r["notlar"]))
        cur = str(r["kaynak"])
    return out[::-1]


def kapi_html(unit: str, steps: list[tuple[int, int, str]]) -> list[str]:
    files = {"kapi": "kapi-notlar-taslak-{n}.json", "kapi2": "kapi2-notlar-taslak-{n}.json"}
    L = []
    for src, new, kind in steps:
        nf = Y.out_dir(unit) / files.get(kind, "kapi-notlar-taslak-{n}.json").format(n=src)
        dz = P.DRAFTS / unit / f"taslak-{new}.duzeltme.json"
        if not nf.exists() or not dz.exists():
            continue
        notes = json.loads(nf.read_text(encoding="utf-8"))["notlar"]
        prefix = {"kapi": "Q", "kapi2": "R"}.get(kind, "Q")
        by_no = {f"{prefix}{i}": x for i, x in enumerate(notes, 1)}
        data = json.loads(dz.read_text(encoding="utf-8"))
        handled = {}
        for ch in data.get("degisiklikler", []):
            for no in ch.get("notlar", []):
                handled.setdefault(no, []).append(f"{ch.get('islem')} {ch.get('capa') or ch.get('sonra')}")
        rejected = {r.get("not"): r.get("gerekce", "") for r in data.get("reddedilen", [])}
        meta = json.loads((P.DRAFTS / unit / f"taslak-{new}.json").read_text(encoding="utf-8")).get("duzeltme", {})
        title = "Kalite kapısı" if kind == "kapi" else "İkinci tur (düzeltmenin yazdıklarında nisbet hataları)"
        L += [f"<h3>{title}: taslak {src} → {new}</h3>",
              f'<p class="small muted">{len(notes)} not; {meta.get("karsilanan", "?")} karşılandı, '
              f'{len(rejected)} gerekçesiyle reddedildi; Arapça {meta.get("ar_harf", {}).get("once", "?")} → '
              f'{meta.get("ar_harf", {}).get("sonra", "?")} harf.</p>']
        for no, x in by_no.items():
            if x.get("tur") == "dogru":
                continue
            state = ("karşılandı: " + ", ".join(handled[no])) if no in handled else (
                "reddedildi: " + rejected[no] if no in rejected else "anılmadı")
            L.append(f'<div class="note"><span class="tag">{esc(x.get("kaynak") or "")}</span>'
                     f'<span class="tag">{esc(x.get("tur") or "")}</span> <b>{no}</b> · {esc(x.get("capa") or "")}<br>'
                     f'{esc(x.get("metin") or "")}<br><span class="small muted">{esc(state)}</span></div>')
    return L


def sayfa(unit: str, n: int | None = None) -> Path:
    cfg = P.UNITS[unit]
    st = P.d5_state()["birimler"].get(unit, {})
    son = n or st.get("son_taslak")
    if not son:
        raise SystemExit(f"{unit}: son taslak yok")
    steps = chain(unit, son)
    first = steps[0][0] if steps else son
    blocks, sources = Y.draft_blocks(unit, son)
    raw_flat = re.sub(r"\s+", " ", (P.DRAFTS / unit / f"taslak-{son}.md").read_text(encoding="utf-8"))
    meta = json.loads((P.DRAFTS / unit / f"taslak-{first}.json").read_text(encoding="utf-8"))
    izf = Y.out_dir(unit) / f"izah-taslak-{son}.json"
    izah = {x.get("capa"): x.get("metin", "") for x in json.loads(izf.read_text(encoding="utf-8")).get("izah", [])} \
        if izf.exists() else {}
    q = json.loads((ROOT / "data" / "library" / "kuran" / "quran.json").read_text(encoding="utf-8"))
    ay = {v["ayah"]: v for v in q["suras"][cfg["sura"] - 1]["ayahs"]}
    a, b = cfg["ayahs"]
    rng = P.ayah_range(cfg)
    L = [f"<h1>{cfg['sura_name']} {rng}: yapay zekâ taslağı</h1>",
         f'<p class="small muted">İşârâtü\'l-İ\'câz usulüyle · istem {esc(meta.get("surum"))} · taslak {son}'
         + (f' · ≈{st["maliyet"]} $' if st.get("maliyet") else "") + (f' · {st["sure_dk"]} dk' if st.get("sure_dk") else "")
         + "</p>",
         '<div class="box warn small">Bu bir <b>yapay zekâ taslağıdır</b>; tefsir değildir, müellife ya da İşârât\'a mal '
         'edilmez. Kaynak işaretinin üstüne gelince kaynakça satırı görünür. Türkçe paragraflar yapay zekâ tercümesidir; '
         'izah günümüz Türkçesiyle, yine yapay zekânındır. Taslak bir kalite kapısından geçti (aşağıda): kaynağın '
         'sözünü aşan atıflar düzeltildi; eleştirmenin "eksik" notları taslağa eklenmedi, en sonda duruyor.</div>']
    L += ["<h2>Âyet</h2>"]
    for k in range(a, b + 1):
        L += [f'<p class="ar">{esc(ay[k]["text"])} ﴿{k}﴾</p>',
              f'<p class="tr small">Meâl (Diyanet Vakfı): {esc(ay[k]["translations"]["diyanet-vakfi"])}</p>']
    sec, prev = None, None
    for anchor, lang, quote, text in blocks:
        key = anchor.split("/")[0]
        if key == "Âyet":
            continue
        if key != sec:
            L.append(f"<h2>{esc(P.SECTION_TITLES.get(key, key))}</h2>")
            sec, prev = key, None
        if lang == "ar":
            L.append(f'<div class="{"quote" if quote else ""}"><p class="ar">{marks(text, sources)}</p></div>')
        else:
            # damga taslağın kendisinde: tercüme paragrafı "Yapay zekâ tercümesi:" ile başlar (`draft_blocks` atar)
            stamped = STAMP_RE.search(raw_flat.split(re.sub(r"\s+", " ", text)[:60], 1)[0][-60:]) is not None \
                if re.sub(r"\s+", " ", text)[:60] in raw_flat else False
            label = ("Yapay zekâ tercümesi (alıntının)" if quote else "Yapay zekâ tercümesi") if stamped else (
                "Alıntı" if quote else "Türkçe (taslağın kendi sözü)")
            L.append(f'<div class="{"quote" if label == "Alıntı" else ""}"><div class="lab">{label}</div>'
                     f'<p class="tr">{marks(text, sources)}</p></div>')
            if izah.get(anchor):
                L.append(f'<div class="izah"><div class="lab">İzah (günümüz Türkçesiyle, yapay zekâ)</div>'
                         f'{marks(izah[anchor], sources)}</div>')
        prev = (lang, quote)
    L += ["<h2>Kaynaklar</h2>", '<ol class="src">']
    L += [f'<li value="{k}">{esc(v)}</li>' for k, v in sorted(sources.items(), key=lambda kv: int(kv[0]))]
    L += ["</ol>"]
    L += ["<h2>Kalite kapısı</h2>",
          '<p class="small muted">Kapalı eleştirmen (İşârât\'ı görmeden), nisbet denetçisi (atıf kaynakta var mı) ve biçim '
          'denetiminin notları; yazar her notu ya karşıladı ya gerekçesiyle reddetti. Düzeltme yeni kaynak getirmez.</p>']
    L += kapi_html(unit, steps) or ['<p class="muted">Kapı çalışmadı.</p>']
    acik = Y.out_dir(unit) / f"kapi-acik-notlar-taslak-{first}.json"
    eksik = json.loads(acik.read_text(encoding="utf-8"))["notlar"] if acik.exists() else []
    L += ["<h2>Eleştirmenin eksik notları</h2>",
          '<p class="small muted">Kapalı eleştirmenin "bu nükte eksik" dediği yerler; taslağa eklenmedi (eklemek yeni '
          'hata getiriyordu, 2026-11-20 sınaması). Okuyucuya yol göstermek için.</p>']
    L += [f'<div class="note"><b>{esc(x.get("capa") or "")}</b> · {esc(x.get("metin") or "")}'
          + (f'<br><span class="small muted">Öneri: {esc(x["oneri"])}</span>' if x.get("oneri") else "") + "</div>"
          for x in eksik] or ['<p class="muted">Yok.</p>']
    L += [f'<p class="small muted">Sayfa {datetime.now():%Y-%m-%d %H:%M}</p>']
    page = (f'<!doctype html>\n<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" '
            f'content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow">'
            f"<title>{esc(cfg['sura_name'])} {rng} Taslağı</title><style>{CSS}</style></head><body><main>"
            + "\n".join(L) + "</main></body></html>\n")
    MASA.mkdir(parents=True, exist_ok=True)
    out = MASA / (f"d5-{unit}-t{son}.html" if n else f"d5-{unit}.html")   # --taslak: kabul biriminde iki kol
    out.write_text(page, encoding="utf-8")
    print(f"{out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB)")
    return out


def durum_sayfasi() -> Path:
    """D5'in durum sayfası (`masa/d5.html`): birimler, okuma sayfaları, alarmlar, maliyet, haftalık kota ve tahmin.
    Okuma listesi yok (kullanıcının kararı, 2026-11-21: D5'te okuma onay değildir; alarmlar ar-ge bilgisidir)."""
    st = P.d5_state()
    b = st["birimler"]
    units = [u for u in P.d5_units() if u["kaynak"] != "isarat"]
    done = [u["id"] for u in units if (b.get(u["id"]) or {}).get("bitti")]
    cost = sum(b[u].get("maliyet") or 0 for u in done)
    shares = [b[u]["hafta_sonra"] - b[u]["hafta_once"] for u in done
              if b[u].get("hafta_once") is not None and b[u].get("hafta_sonra") is not None
              and b[u]["hafta_sonra"] >= b[u]["hafta_once"]]
    lim = json.loads(P.LIMIT_STATE.read_text(encoding="utf-8")) if P.LIMIT_STATE.exists() else {}
    left = len(units) - len(done)
    L = ["<h1>D5 · Bakara 34–286</h1>",
         f'<p><b>{len(done)}/{len(units)}</b> birim bitti · ≈{cost:.0f} $ (kullanım değeri) · haftalık kota '
         f'%{(lim.get("week") or 0) * 100:.0f}'
         + (f' (sıfırlanma {datetime.fromtimestamp(lim["week_reset"]):%d.%m %H:%M})' if lim.get("week_reset") else "")
         + "</p>"]
    if shares:
        avg = sum(shares) / len(shares)
        L.append(f'<p class="small muted">Birim başına haftalık kotanın ≈%{avg * 100:.1f}\'i; kalan {left} birim ≈'
                 f'{left * avg / 0.9:.1f} haftalık kota (eşik %90).</p>')
    L.append('<p class="small muted">⚠ alarm: program bir şey gördü (birim yine yayımlandı); ar-ge bilgisidir, okuma görevi açmaz.</p>')
    L.append('<table style="width:100%;border-collapse:collapse;font-size:.88rem">'
             '<tr style="text-align:left"><th>Birim</th><th>Durum</th><th>$</th><th>dk</th><th>Not</th></tr>')
    for u in units:
        x = b.get(u["id"]) or {}
        al = x.get("alarmlar") or []
        name = (f'<a href="d5-{u["id"]}.html">{u["id"]}</a>' if x.get("bitti") else u["id"])
        state = "bitti" if x.get("bitti") else ("sürüyor" if x.get("basladi") else "")
        L.append(f'<tr style="border-top:1px solid var(--line)"><td>{name}</td><td>{state}</td>'
                 f'<td>{x.get("maliyet") or ""}</td><td>{x.get("sure_dk") or ""}</td>'
                 f'<td>{"⚠ " + esc("; ".join(al)) if al else ""}</td></tr>')
    L.append("</table>")
    L.append(f'<p class="small muted">Sayfa {datetime.now():%Y-%m-%d %H:%M}</p>')
    page = (f'<!doctype html>\n<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" '
            f'content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow">'
            f"<title>D5 Durumu</title><style>{CSS}</style></head><body><main>" + "\n".join(L) + "</main></body></html>\n")
    out = MASA / "d5.html"
    MASA.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("unit", choices=P.UNITS)
    ap.add_argument("--taslak", type=int)
    a = ap.parse_args()
    sayfa(a.unit, a.taslak)


if __name__ == "__main__":
    main()
