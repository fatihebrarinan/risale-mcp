"""Ar-ge masasının giriş sayfası (S7.2; kullanıcının onayı, 2026-11-21: "Pano · Okumalar · Birimler", D5.1'den önce).

`/taslak/` açılınca gelen sayfadır. İki parça:
- `masa/index.html`: değişmeyen kabuk (üç sekme, telefona göre). Sekmeler adreste durur (`#pano`, `#okumalar`,
  `#birimler`).
- `masa/pano.json`: sayfanın verisi (D5'in ilerlemesi, kota, alarmlar; birimler ve sayfaları). Taslak deposundan
  (`data/d1`) üretilir; D5 kuyruğu her birimden sonra sunucudan yeniler (`d1-birim.durum_sayfasi`), yerelde bu betik.
- Okumalar sekmesi canlıdır: masa servisinden (`/taslak/api/okumalar`, girişli kişinin görevleri) gelir.

Eski "âyet masası"nın son birim kopyası (`d1-masa.py`'nin `index.html`'i) artık yazılmaz; birimlerin masa sayfaları
(`<birim>.html`) Birimler sekmesinden açılır.

    uv run python scripts/masa-giris.py              # data/d1/masa/index.html ve pano.json
    uv run python scripts/masa-giris.py --gonder     # ve siteye (scripts/taslak-gonder.sh)
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
import time
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
MASA = P.KEEP / "masa"                      # okunan sayfalar (tur, D5 okuma sayfaları; git'te)
OUT = ROOT / "data" / "interim" / "oku-masa"  # yazılanlar: yeniden üretilir, git'e girmez (iki makine yazıyordu, S7d)
STOP = Path.home() / ".d5-dur"


def _num_key(uid: str) -> list[int]:
    return [int(x) for x in uid.split("-")]


def _pages() -> list[str]:
    return sorted(p.name for p in MASA.glob("*.html") if p.name not in ("index.html", "deneyler.html"))


def _unit_pages(uid: str, pages: list[str]) -> list[dict]:
    """Bir birimin masa sayfaları: masa sayfası, D5 okuma sayfası, okuma turları, fark kartları."""
    out = [{"ad": "âyet masası", "href": f"ayet.html#/{uid}", "tur": "masa"}]
    for name in pages:
        stem = name[:-5]
        if stem == uid:
            continue
        elif stem == f"d5-{uid}" or stem.startswith(f"d5-{uid}-t"):
            out.append({"ad": "okuma sayfası" + (f" (taslak {stem.rsplit('-t', 1)[1]})" if "-t" in stem[3 + len(uid):]
                                                 else ""), "href": name, "tur": "d5"})
        elif stem.startswith(f"tur-{uid}-"):
            out.append({"ad": "okuma turu " + stem.removeprefix(f"tur-{uid}-"), "href": name, "tur": "tur"})
        elif stem.startswith("fark-") and stem.removeprefix("fark-").startswith(uid + "-"):
            out.append({"ad": "fark kartları", "href": name, "tur": "fark"})
    return out


def _queue_state() -> str | None:
    """Kuyruk hizmetinin durumu (yalnız sunucuda: `d1-kuyruk` kullanıcı hizmeti kuruluysa; yerelde None)."""
    try:
        p = subprocess.run(["systemctl", "--user", "show", "-p", "LoadState,ActiveState", "d1-kuyruk"],
                           capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.TimeoutExpired):
        return None
    kv = dict(line.split("=", 1) for line in p.stdout.splitlines() if "=" in line)
    if kv.get("LoadState") != "loaded":
        return None
    st = {"active": "çalışıyor", "activating": "başlıyor"}.get(kv.get("ActiveState"), "durdu")
    return st + (" · dur işareti var (birim bitince durur)" if STOP.exists() else "")


GENEL = {"bolme-bakara.html": "Bakara'nın birim bölmesi", "d5.html": "D5 durum tablosu"}


def veri() -> dict:
    units = P.d5_units()
    st = P.d5_state()["birimler"]
    d5 = [u for u in units if u["kaynak"] != "isarat"]
    done = [u["id"] for u in d5 if (st.get(u["id"]) or {}).get("bitti")]
    running = [u["id"] for u in d5 if (st.get(u["id"]) or {}).get("basladi") and not (st.get(u["id"]) or {}).get("bitti")]
    nxt = next((u["id"] for u in d5 if not (st.get(u["id"]) or {}).get("bitti")), None)
    shares = [st[u]["hafta_sonra"] - st[u]["hafta_once"] for u in done
              if st[u].get("hafta_once") is not None and st[u].get("hafta_sonra") is not None
              and st[u]["hafta_sonra"] >= st[u]["hafta_once"]]
    lim = json.loads(P.LIMIT_STATE.read_text(encoding="utf-8")) if P.LIMIT_STATE.exists() else {}
    avg = sum(shares) / len(shares) if shares else None
    pages = _pages()
    alarmed = [{"id": u["id"], "alarmlar": st[u["id"]]["alarmlar"]} for u in d5 if (st.get(u["id"]) or {}).get("alarmlar")]
    recent = sorted(done, key=lambda u: st[u]["bitti"], reverse=True)[:5]
    out_d5 = {
        "toplam": len(d5), "bitti": len(done), "suruyor": running, "siradaki": nxt,
        "maliyet": round(sum(st[u].get("maliyet") or 0 for u in done), 2),
        "hafta": lim.get("week"), "hafta_reset": lim.get("week_reset"), "bes_saat": lim.get("five"),
        "bes_saat_reset": lim.get("five_reset"), "yoklama": lim.get("at"),
        "birim_payi": avg, "kalan_hafta": (len(d5) - len(done)) * avg / 0.9 if avg else None,
        "kuyruk": _queue_state(),
        "son": [{"id": u, "bitti": st[u]["bitti"], "maliyet": st[u].get("maliyet"), "sure_dk": st[u].get("sure_dk"),
                 "alarm": len(st[u].get("alarmlar") or [])} for u in recent],
        "alarmli": alarmed,
    }
    # Birimler: ar-ge birimleri (taslak deposunda klasörü olanlar) ve D5'in başlamış birimleri; sırayla
    arge = {p.name for p in P.DRAFTS.iterdir() if p.is_dir() and p.name.replace("-", "").isdigit()}
    rows = []
    for u in units:
        uid = u["id"]
        x = st.get(uid) or {}
        if uid not in arge and not x and u["kaynak"] == "isarat":
            continue
        row = {"id": uid, "ayet": u["ayet"], "tur": "d5" if u["kaynak"] != "isarat" else "arge",
               "sayfalar": _unit_pages(uid, pages)}
        if uid in arge:
            s = DUR.state(uid)
            total, _ = DUR.cost_of(uid)
            row |= {"taslaklar": [{"n": t["n"], "surum": t["surum"]} for t in s["taslaklar"]],
                    "okuma": len(s["okumalar"]), "maliyet": round(total, 1), "envanter": s["envanter"]}
        if u["kaynak"] != "isarat":
            if not x:
                continue
            row |= {"durum": "bitti" if x.get("bitti") else "sürüyor", "maliyet": x.get("maliyet"),
                    "sure_dk": x.get("sure_dk"), "alarmlar": x.get("alarmlar") or []}
        rows.append(row)
    known = {p["href"] for r in rows for p in r["sayfalar"]}
    genel = [{"ad": GENEL.get(n, n[:-5]), "href": n} for n in pages
             if n not in known and not n.startswith(("d5-", "tur-", "fark-")) and n[:-5] not in arge]
    return {"sema": "pano/1", "uretildi": time.time(),
            "makine": "sunucu" if (Path.home() / ".ssh" / "site_gonder").exists() else "yerel",
            "d5": out_d5, "birimler": rows, "genel": genel,
            "kalan_d5": len(d5) - len([r for r in rows if r["tur"] == "d5"])}


SHELL = r"""<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>Ar-ge Masası</title><style>__CSS__
nav.tabs { display: flex; gap: 4px; border-bottom: 1px solid var(--line); margin: 8px 0 14px; overflow-x: auto; }
nav.tabs a { padding: 8px 12px; color: var(--muted); text-decoration: none; border-bottom: 2px solid transparent;
             white-space: nowrap; }
nav.tabs a.on { color: var(--fg); border-bottom-color: var(--accent); font-weight: 600; }
.badge { display: inline-block; min-width: 1.4em; padding: 0 6px; border-radius: 10px; background: var(--accent);
         color: var(--bg); font-size: .75rem; text-align: center; margin-left: 4px; }
.bar { height: 8px; background: var(--soft); border-radius: 4px; overflow: hidden; margin: 6px 0; }
.bar > i { display: block; height: 100%; background: var(--accent); }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 8px; }
.stat { background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 8px 12px; }
.stat b { display: block; font-size: 1.25rem; } .stat span { font-size: .8rem; color: var(--muted); }
.row { background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 8px 12px; margin: 8px 0; }
.row .t { display: flex; justify-content: space-between; gap: 8px; flex-wrap: wrap; }
.row a { color: var(--src); }
.chips a { display: inline-block; margin: 4px 6px 0 0; padding: 1px 8px; border: 1px solid var(--line);
           border-radius: 12px; font-size: .82rem; text-decoration: none; }
.st-bitti { color: var(--accent); } .st-suruyor, .st-bekliyor { color: var(--ai); } .alarm { color: var(--bad); }
nav.big { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 10px; margin: 10px 0 6px; }
nav.big a { display: block; text-align: center; padding: 14px 10px; border: 1px solid var(--line); border-radius: 10px;
            background: var(--card); color: var(--fg); text-decoration: none; font-weight: 600; font-size: 1.02rem; }
nav.big a:first-child { border-color: var(--accent); }
nav.big a:hover { background: var(--soft); }
header.top { display: flex; justify-content: space-between; align-items: baseline; gap: 8px; flex-wrap: wrap; }
header.top a { font-size: .85rem; color: var(--muted); }
</style></head><body><main>
<header class="top"><h1>Ar-ge Masası</h1><span class="small muted"><span id="ben"></span> · <a href="cikis">çıkış</a></span></header>
<nav class="big"><a href="ayet.html">Âyet masası</a><a href="/oku/">Okuma platformu</a><a href="deneyler.html">Deneyler defteri</a><a href="d5.html">D5 durumu</a></nav>
<p class="small muted">Yapay zekâ taslaklarının iç çalışma masası. Buradaki hiçbir taslak tefsir değildir.</p>
<nav class="tabs"><a href="#pano" data-t="pano">Pano</a><a href="#okumalar" data-t="okumalar">Okumalar<span id="nok"></span></a><a href="#birimler" data-t="birimler">Birimler</a></nav>
<section id="pano"></section><section id="okumalar" hidden></section><section id="birimler" hidden></section>
<p class="small muted" id="alt"></p>
</main><script>
const API = '/taslak/api/';
const $ = id => document.getElementById(id);
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
const pct = x => x == null ? '—' : '%' + Math.round(x * 100);
const when = t => t ? new Date(t * 1000).toLocaleString('tr-TR', {day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit'}) : '';
const ayet = a => a[0] === a[1] ? String(a[0]) : a[0] + '–' + a[1];
function show(t) {
  t = ['pano', 'okumalar', 'birimler'].includes(t) ? t : 'pano';
  for (const s of document.querySelectorAll('main > section')) s.hidden = s.id !== t;
  for (const a of document.querySelectorAll('nav.tabs a')) a.classList.toggle('on', a.dataset.t === t);
}
addEventListener('hashchange', () => show(location.hash.slice(1)));
show(location.hash.slice(1));

function pano(d, oks) {
  const x = d.d5, L = [];
  L.push('<h2>D5 · Bakara 34–286</h2>');
  L.push(`<div class="bar"><i style="width:${x.toplam ? 100 * x.bitti / x.toplam : 0}%"></i></div>`);
  L.push('<div class="grid">'
    + `<div class="stat"><b>${x.bitti}/${x.toplam}</b><span>birim bitti</span></div>`
    + `<div class="stat"><b>${x.suruyor.length ? esc(x.suruyor.join(', ')) : (x.siradaki ? esc(x.siradaki) : '—')}</b><span>${x.suruyor.length ? 'yazılıyor' : 'sıradaki'}</span></div>`
    + `<div class="stat"><b>≈${Math.round(x.maliyet)} $</b><span>kullanım değeri</span></div>`
    + `<div class="stat"><b>${pct(x.hafta)}</b><span>haftalık kota${x.hafta_reset ? ' · ' + when(x.hafta_reset) + "'de sıfırlanır" : ''}</span></div>`
    + `<div class="stat"><b>${x.birim_payi == null ? '—' : '%' + (100 * x.birim_payi).toFixed(1)}</b><span>birim başına haftalık kota</span></div>`
    + `<div class="stat"><b>${x.kalan_hafta == null ? '—' : x.kalan_hafta.toFixed(1)}</b><span>kalanın haftalık kotası (eşik %90)</span></div>`
    + '</div>');
  L.push(`<p class="small muted">Kuyruk: ${esc(x.kuyruk || 'bilinmiyor (sayfa yerelde üretildi)')}`
    + (x.yoklama ? ` · kota yoklaması ${when(x.yoklama)}` : '') + ' · <a href="d5.html">bütün tablo</a></p>');
  const bek = oks.filter(o => o.durum !== 'bitti');
  L.push('<h2>Açık okumalar (deneyler)</h2>');
  L.push(bek.length ? bek.map(okuma).join('') : '<p class="muted">Bekleyen okuma yok.</p>');
  L.push('<h2>Alarmlar</h2><p class="small muted">Programın gördüğü (birim yine yayımlandı); ar-ge bilgisidir, okuma görevi açmaz.</p>');
  L.push(x.alarmli.length ? x.alarmli.map(a => `<div class="row"><a href="d5-${esc(a.id)}.html">${esc(a.id)}</a> <span class="alarm">⚠ ${esc(a.alarmlar.join('; '))}</span></div>`).join('')
    : '<p class="muted">Alarm yok.</p>');
  if (x.son.length) {
    L.push('<h2>Son biten birimler</h2>');
    L.push(x.son.map(s => `<div class="row t"><span><a href="d5-${esc(s.id)}.html">Bakara ${esc(s.id)}</a>${s.alarm ? ' <span class="alarm">⚠</span>' : ''}</span>`
      + `<span class="small muted">${esc(s.bitti.slice(0, 16).replace('T', ' '))} · ${s.maliyet ?? '?'} $ · ${s.sure_dk ?? '?'} dk</span></div>`).join(''));
  }
  $('pano').innerHTML = L.join('\n');
}
function okuma(o) {
  const st = {bekliyor: 'bekliyor', suruyor: 'sürüyor', bitti: 'bitti'}[o.durum] || o.durum;
  return `<div class="row"><div class="t"><a href="${esc(o.sayfa || '#')}"><b>${esc(o.baslik)}</b></a>`
    + `<span class="small st-${esc(o.durum)}">${esc(st)}</span></div>`
    + (o.aciklama ? `<div class="small muted">${esc(o.aciklama)}</div>` : '')
    + `<div class="small muted">${o.birim ? 'Bakara ' + esc(o.birim) + ' · ' : ''}${o.karar}/${o.yer} yer${o.dakika ? ' · ≈' + o.dakika + ' dk' : ''}`
    + ` · ${when(o.olusturuldu)}${o.bitti ? ' · bitti ' + when(o.bitti) : ''}</div></div>`;
}
function okumalar(oks) {
  const bek = oks.filter(o => o.durum !== 'bitti'), bit = oks.filter(o => o.durum === 'bitti');
  $('nok').innerHTML = bek.length ? `<span class="badge">${bek.length}</span>` : '';
  $('okumalar').innerHTML = '<h2>Bekleyen</h2>' + (bek.length ? bek.map(okuma).join('') : '<p class="muted">Bekleyen okuma yok.</p>')
    + '<h2>Biten</h2>' + (bit.length ? bit.map(okuma).join('') : '<p class="muted">Henüz yok.</p>')
    + '<p class="small muted">Görevli okumalar burada; daha eskileri (görevsiz okuma turları) Birimler sekmesinde, birimin altında.</p>';
}
function birimler(d) {
  const row = r => {
    const ts = (r.taslaklar || []).map(t => t.n + ':' + (t.surum || '?')).join(', ');
    const bits = [];
    if (r.durum) bits.push(`<span class="st-${r.durum === 'bitti' ? 'bitti' : 'suruyor'}">${esc(r.durum)}</span>`);
    if (r.envanter != null) bits.push(r.envanter + ' kalem envanter');
    if (ts) bits.push('taslaklar ' + esc(ts));
    if (r.okuma) bits.push(r.okuma + ' okuma');
    if (r.maliyet != null) bits.push('≈' + Math.round(r.maliyet) + ' $');
    if (r.sure_dk) bits.push(r.sure_dk + ' dk');
    return `<div class="row"><div class="t"><b>Bakara ${esc(ayet(r.ayet))}</b>`
      + (r.alarmlar && r.alarmlar.length ? `<span class="small alarm">⚠ ${esc(r.alarmlar.join('; '))}</span>` : '') + '</div>'
      + `<div class="small muted">${bits.join(' · ')}</div>`
      + `<div class="chips">${r.sayfalar.map(p => `<a href="${esc(p.href)}">${esc(p.ad)}</a>`).join('')}</div></div>`;
  };
  const ar = d.birimler.filter(r => r.tur === 'arge'), d5 = d.birimler.filter(r => r.tur === 'd5');
  $('birimler').innerHTML = '<h2>Ar-ge birimleri (Bakara 1–33, İşârât\'ın âyetleri)</h2>' + ar.map(row).join('')
    + '<h2>D5 (Bakara 34–286)</h2>' + (d5.length ? d5.map(row).join('') : '<p class="muted">Henüz başlamadı.</p>')
    + (d.kalan_d5 ? `<p class="small muted">Başlamamış ${d.kalan_d5} birim.</p>` : '')
    + (d.genel.length ? '<h2>Öbür sayfalar</h2><div class="chips">' + d.genel.map(p => `<a href="${esc(p.href)}">${esc(p.ad)}</a>`).join('') + '</div>' : '');
}
async function load() {
  let d = null, oks = [];
  try { d = await (await fetch('pano.json', {cache: 'no-store'})).json(); } catch (e) { $('pano').textContent = 'pano.json okunamadı.'; }
  try {
    const r = await fetch(API + 'okumalar', {cache: 'no-store'});
    if (r.ok) oks = (await r.json()).okumalar;
  } catch (e) {}
  okumalar(oks);
  if (d) { pano(d, oks); birimler(d); $('alt').textContent = 'Pano ' + when(d.uretildi) + ' (' + d.makine + ')'; }
  try { const b = await (await fetch('ben', {cache: 'no-store'})).json(); $('ben').textContent = b.name || b.email || ''; } catch (e) {}
}
load();
</script></body></html>
"""


def yaz() -> list[Path]:
    S = _load("d1_d5_sayfa", "d1-d5-sayfa.py")
    MASA.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    index, data = OUT / "index.html", OUT / "pano.json"
    index.write_text(SHELL.replace("__CSS__", S.CSS), encoding="utf-8")
    data.write_text(json.dumps(veri(), ensure_ascii=False, indent=1), encoding="utf-8")
    D = _load("deneyler", "deneyler.py")          # deneyler defteri, alet ayarı, kayma, arama (her birimden sonra)
    return [index, data, *D.yaz()]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gonder", action="store_true", help="siteye gönder (scripts/taslak-gonder.sh)")
    a = ap.parse_args()
    out = yaz()
    for p in out:
        print(f"{p.relative_to(ROOT)} ({p.stat().st_size // 1024} KB)")
    if a.gonder:
        subprocess.run([str(ROOT / "scripts" / "taslak-gonder.sh"), *map(str, out)], check=True, cwd=ROOT)


if __name__ == "__main__":
    main()
