"""S12.1: aynı altın sorulara farklı modellerin cevapları, yan yana okuma sayfası.

    uv run python scripts/s12-karsilastir.py <çalıştırma> [<çalıştırma> …] [--gonder]

Her çalıştırma `data/interim/golden/<ad>/` klasörüdür (`golden run … --model …`). Sütunun adı klasördeki
`model.json`'dan (yoksa dökümün modelinden) gelir; `--etiket "ad=Açıklama"` ile değiştirilir. Ölçüler `golden.py`'nin
raporundakiyle aynıdır (doğrulanan atıf, beklenen bölüm okundu mu, araç, süre, eşdeğer maliyet). Sayfa
`data/interim/sohbet/s12-modeller.html`; `--gonder` girişli taslak bölümüne koyar (`scripts/taslak-gonder.sh`).

Okuyucu için: "adları gizle" kipinde sütunlar her soruda karışık sırayla A, B, C diye görünür; tercih tarayıcıda
saklanır, sayfanın başında sayılır ve dışa aktarılır.
"""

import argparse
import html
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

from risale_mcp import golden
from risale_mcp.paths import INTERIM_DIR, ROOT

OUT = INTERIM_DIR / "sohbet" / "s12-modeller.html"
NAMES = {"claude-haiku-5-5": "Haiku 5.5", "claude-sonnet-5-5": "Sonnet 5.5", "claude-opus-5-5": "Opus 5.5"}


def _site():
    spec = importlib.util.spec_from_file_location("site_uret", ROOT / "scripts" / "site-uret.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # Yazılar için yazılmış Markdown; model cevaplarında liste girintili satırla başlayabiliyor
    def items(lines: list[str], marker: str) -> list[str]:
        out: list[str] = []
        for line in lines:
            if re.match(marker, line) or not out:
                out.append(re.sub(marker, "", line.strip(), count=1))
            else:
                out[-1] += " " + line.strip()
        return out
    mod._items = items
    return mod


def run_model(run_dir: Path) -> str:
    meta = run_dir / "model.json"
    if meta.exists():
        return json.loads(meta.read_text(encoding="utf-8"))["model"]
    for path in run_dir.glob("*.jsonl"):
        for line in path.read_text(encoding="utf-8").splitlines():
            if '"model":"' in line:
                event = json.loads(line)
                model = event.get("model") or event.get("message", {}).get("model")
                if model:
                    return model
    return run_dir.name


def collect(run_dir: Path, questions: dict, checkers: dict) -> dict:
    multi = (run_dir / "servers.json").exists()
    out = {}
    for path in run_dir.glob("*.jsonl"):
        q = questions.get(path.stem)
        if q is None:
            continue
        if multi:
            checker = checkers.setdefault("multi", golden.MultiChecker())
        else:
            checker = checkers.setdefault(q.get("profile"), golden.Checker(golden.library_for(q.get("profile"))))
        t = golden.read_transcript(path)
        e = golden.evaluate(q, t, checker)
        out[q["id"]] = {
            "answer": t.answer.strip(), "failure": t.failure,
            "tools": e["tools"], "errors": e["tool_errors"], "cite": e["verify_calls"],
            "ok": sum(c.verified for c in e["citations"]), "citations": len(e["citations"]),
            "read": [s["read"] for s in e["sections"]],
            "seconds": t.seconds or 0, "cost": t.cost_usd or 0, "tokens": t.output_tokens or 0,
            "calls": [f"{c.name}({golden._call_line(c).split('` ', 1)[1][:160]})" + (" ✗" if c.error else "")
                      for c in t.calls],
        }
    return out


def summary(rows: list[dict]) -> dict:
    n = len(rows) or 1
    cites = sum(r["citations"] for r in rows)
    reads = [x for r in rows for x in r["read"]]
    return {"n": len(rows), "ok": sum(r["ok"] for r in rows), "citations": cites,
            "read": sum(reads), "expected": len(reads),
            "tools": sum(r["tools"] for r in rows) / n, "errors": sum(r["errors"] for r in rows),
            "nocite": sum(not r["cite"] for r in rows),
            "seconds": sum(r["seconds"] for r in rows) / n, "cost": sum(r["cost"] for r in rows) / n,
            "failures": sum(bool(r["failure"]) for r in rows)}


CSS = """
@font-face{font-family:Naskh;src:url(/fonts/naskh.woff2) format("woff2");font-display:swap}
:root{--bg:#fbfaf7;--fg:#1f2328;--mut:#5c6370;--line:#e3e0d8;--card:#fff;--acc:#2f6f4f;--bad:#a33;--warn:#9a6b00}
@media (prefers-color-scheme:dark){:root{--bg:#16181b;--fg:#e6e6e6;--mut:#a0a6ad;--line:#33373c;--card:#1d2024;
--acc:#6cc394;--bad:#e27b7b;--warn:#e0b450}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 system-ui,sans-serif}
header.top{padding:24px 20px 8px;max-width:1500px;margin:auto}h1{font-size:1.5rem;margin:0 0 6px}
.lead{color:var(--mut);max-width:900px;margin:0}
main{max-width:1500px;margin:auto;padding:0 20px 80px}
table.sum{border-collapse:collapse;margin:16px 0;font-size:.92rem}
table.sum th,table.sum td{border-bottom:1px solid var(--line);padding:6px 12px;text-align:left}
table.sum td.n{text-align:right;font-variant-numeric:tabular-nums}
.bar{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);padding:8px 0;
display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.bar label{font-size:.9rem;color:var(--mut)}.bar select,.bar button{font:inherit;font-size:.9rem;padding:4px 10px;
border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:6px;cursor:pointer}
.qnav{display:flex;flex-wrap:wrap;gap:4px;margin:12px 0}.qnav a{font-size:.8rem;padding:2px 7px;border:1px solid var(--line);
border-radius:5px;text-decoration:none;color:var(--fg)}.qnav a.done{background:var(--acc);color:#fff;border-color:var(--acc)}
section.q{border-top:2px solid var(--line);padding-top:18px;margin-top:28px}
section.q h2{font-size:1.15rem;margin:0 0 4px}.qtext{font-size:1.05rem;margin:0 0 6px}
details.exp{color:var(--mut);font-size:.9rem;margin-bottom:10px}
.cols{display:grid;grid-template-columns:repeat(var(--n),minmax(0,1fr));gap:14px;align-items:start}
@media (max-width:900px){.cols{grid-template-columns:1fr}}
.col{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;min-width:0}
.col h3{margin:0 0 6px;font-size:1rem;display:flex;justify-content:space-between;gap:8px}
.metrics{font-size:.8rem;color:var(--mut);margin-bottom:10px;display:flex;flex-wrap:wrap;gap:4px 10px}
.metrics .bad{color:var(--bad)}.metrics .warn{color:var(--warn)}
.ans{font-size:.95rem;overflow-wrap:anywhere}.ans h2,.ans h3{font-size:1rem;margin:16px 0 6px}
.ans blockquote{margin:8px 0;padding:4px 12px;border-left:3px solid var(--acc);background:rgba(47,111,79,.06)}
.ans blockquote[dir=rtl]{border-left:0;border-right:3px solid var(--acc)}
[lang=ar]{font-family:Naskh,"Amiri","Scheherazade New",serif;font-size:1.15em;line-height:1.9}
.ans table{border-collapse:collapse;font-size:.88rem}.ans td,.ans th{border:1px solid var(--line);padding:3px 6px}
.table-wrap{overflow-x:auto}
details.calls{font-size:.78rem;color:var(--mut);margin-top:10px}details.calls li{overflow-wrap:anywhere}
.vote{margin-top:12px;display:flex;flex-wrap:wrap;gap:6px;align-items:center;font-size:.9rem}
.vote button{font:inherit;font-size:.85rem;padding:3px 10px;border:1px solid var(--line);background:var(--card);
color:var(--fg);border-radius:6px;cursor:pointer}.vote button.on{background:var(--acc);color:#fff;border-color:var(--acc)}
.vote textarea{width:100%;min-height:2.4em;font:inherit;font-size:.88rem;padding:6px;border:1px solid var(--line);
border-radius:6px;background:var(--card);color:var(--fg)}
body.blind .real,body.blind .metrics,body.blind details.calls{display:none}body:not(.blind) .alias{display:none}
"""

JS = r"""
const KEY = 'risale-s12-oylar:' + DATA.id;
let votes = JSON.parse(localStorage.getItem(KEY) || '{}');
const save = () => { localStorage.setItem(KEY, JSON.stringify(votes)); tally(); };
function seeded(s){let h=2166136261;for(const c of s)h=Math.imul(h^c.charCodeAt(0),16777619);
  return ()=>{h^=h<<13;h^=h>>>17;h^=h<<5;return ((h>>>0)%1e6)/1e6}}
function arrange(){
  const blind = document.body.classList.contains('blind');
  document.querySelectorAll('.cols').forEach(cols=>{
    const items=[...cols.children]; const r=seeded(cols.dataset.q+DATA.id);
    const order = blind ? items.map(i=>[r(),i]).sort((a,b)=>a[0]-b[0]).map(x=>x[1])
                        : items.sort((a,b)=>a.dataset.i-b.dataset.i);
    order.forEach((el,k)=>{cols.appendChild(el); el.querySelector('.alias').textContent='Cevap '+'ABCDEF'[k];});
  });
}
function tally(){
  const c={}; let n=0;
  for(const [q,v] of Object.entries(votes)){ if(!v.best) continue; n++; c[v.best]=(c[v.best]||0)+1;
    const a=document.querySelector(`.qnav a[href="#${q}"]`); if(a) a.classList.add('done'); }
  document.getElementById('tally').textContent = n ? `Tercihleriniz (${n} soru): ` +
    Object.entries(c).map(([k,v])=>`${k==='esit'?'eşit':(k==='hicbiri'?'hiçbiri iyi değil':DATA.names[k])} ${v}`).join(' · ') : 'Henüz tercih yok.';
}
document.querySelectorAll('.vote').forEach(box=>{
  const q=box.dataset.q, v=votes[q]||{};
  box.querySelectorAll('button').forEach(b=>{ if(v.best===b.dataset.v) b.classList.add('on');
    b.onclick=()=>{ votes[q]={...(votes[q]||{}),best:b.dataset.v};
      box.querySelectorAll('button').forEach(x=>x.classList.toggle('on',x===b)); save(); }; });
  const t=box.querySelector('textarea'); t.value=v.note||'';
  t.oninput=()=>{ votes[q]={...(votes[q]||{}),note:t.value}; save(); };
});
document.getElementById('blind').onchange=e=>{document.body.classList.toggle('blind',e.target.checked);arrange();
  document.querySelectorAll('.vote button[data-v^="m"]').forEach(b=>b.textContent=e.target.checked?'bu':DATA.names[b.dataset.v]);};
document.getElementById('export').onclick=()=>{
  const blob=new Blob([JSON.stringify({page:DATA.id,names:DATA.names,votes},null,1)],{type:'application/json'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='s12-tercihler.json';a.click();};
arrange(); tally();
"""


def page(runs: list[tuple[str, Path, dict]], questions: dict) -> str:
    site = _site()
    ids = [q for q in questions if all(q in data for _, _, data in runs)]   # her modelin cevapladığı sorular
    keys = {f"m{i}": label for i, (label, _, _) in enumerate(runs)}
    sums = [(label, summary([data[q] for q in ids if q in data])) for label, _, data in runs]
    head_rows = []
    for label, s in sums:
        pct = f"{100 * s['ok'] / s['citations']:.0f}%" if s["citations"] else "—"
        head_rows.append(
            f"<tr><td>{html.escape(label)}</td><td class=n>{s['n']}</td>"
            f"<td class=n>{s['ok']}/{s['citations']} ({pct})</td>"
            f"<td class=n>{s['read']}/{s['expected']}</td><td class=n>{s['tools']:.1f}</td>"
            f"<td class=n>{s['errors']}</td><td class=n>{s['nocite']}</td>"
            f"<td class=n>{s['seconds']:.0f} sn</td><td class=n>{s['cost']:.3f} $</td></tr>")
    sections = []
    for qid in ids:
        q = questions[qid]
        cols = []
        for i, (label, _, data) in enumerate(runs):
            r = data.get(qid)
            if r is None:
                body, metrics, calls = "<p><em>Bu soru bu çalıştırmada yok.</em></p>", "", ""
            else:
                body = site.markdown(r["answer"]) if r["answer"] else f"<p><em>Cevap yok: {html.escape(str(r['failure']))}</em></p>"
                read = "".join("✓" if x else "✗" for x in r["read"]) or "—"
                cls = lambda bad, warn=False: ' class="bad"' if bad else (' class="warn"' if warn else "")
                errors = f" ({r['errors']} hata)" if r["errors"] else ""
                metrics = (f"<span{cls(r['ok'] < r['citations'])}>atıf {r['ok']}/{r['citations']}</span>"
                           f"<span{cls('✗' in read)}>beklenen bölüm {read}</span>"
                           f"<span{cls(r['errors'] > 0, True)}>araç {r['tools']}{errors}</span>"
                           f"<span{cls(not r['cite'])}>cite {r['cite']}</span>"
                           f"<span>{r['seconds']:.0f} sn</span><span>{r['cost']:.3f} $</span>")
                calls = ("<details class=calls><summary>Araç çağrıları</summary><ol>"
                         + "".join(f"<li>{html.escape(c)}</li>" for c in r["calls"]) + "</ol></details>")
            cols.append(f'<div class=col data-i="{i}"><h3><span class=real>{html.escape(label)}</span>'
                        f'<span class=alias></span></h3><div class=metrics>{metrics}</div>'
                        f'<div class=ans>{body}</div>{calls}</div>')
        buttons = "".join(f'<button data-v="m{i}">{html.escape(label)}</button>' for i, (label, _, _) in enumerate(runs))
        expected = html.escape(q.get("expected", ""))
        trap = f"<br><strong>Tuzak:</strong> “{html.escape(q['absent'])}” yoktur." if q.get("absent") else ""
        sections.append(
            f'<section class=q id="{qid}"><h2>{qid} · {html.escape(q["category"])}</h2>'
            f'<p class=qtext><strong>Soru:</strong> {html.escape(q["question"])}</p>'
            f'<details class=exp><summary>Beklenen</summary>{expected}{trap}</details>'
            f'<div class=cols data-q="{qid}" style="--n:{len(runs)}">{"".join(cols)}</div>'
            f'<div class=vote data-q="{qid}"><span>Hangisi daha iyi?</span>{buttons}'
            f'<button data-v="esit">eşit</button><button data-v="hicbiri">hiçbiri iyi değil</button>'
            f'<textarea placeholder="Notunuz (isteğe bağlı)"></textarea></div></section>')
    nav = "".join(f'<a href="#{q}">{q}</a>' for q in ids)
    data = {"id": "-".join(p.name for _, p, _ in runs), "names": keys}
    return f"""<!doctype html><html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>S12.1 · Modeller yan yana</title><style>{CSS}</style></head><body>
<header class=top><h1>Aynı soru, farklı modeller</h1>
<p class=lead>Sohbet sayfası (S12) için model seçimi. Her model aynı altın soruları yalnız Risale eklentisiyle
(yayındaki veri) cevapladı. Ölçüler otomatiktir: <strong>atıf</strong> cevaptaki atıfların kaçının veritabanında
doğrulandığı, <strong>beklenen bölüm</strong> sorunun asıl yerini okuyup okumadığı, <strong>cite</strong> atıf aracını
çağırıp çağırmadığı; maliyet abonelikteki eşdeğer API fiyatıdır. Asıl ölçü sizin okumanız: her sorunun altında
hangisini daha iyi bulduğunuzu işaretleyin; tercihleriniz bu tarayıcıda saklanır.</p></header>
<main>
<table class=sum><thead><tr><th>Model</th><th>Soru</th><th>Doğrulanan atıf</th><th>Beklenen bölüm okundu</th>
<th>Araç (ort.)</th><th>Araç hatası</th><th>cite'sız cevap</th><th>Süre (ort.)</th><th>Maliyet (ort.)</th></tr></thead>
<tbody>{"".join(head_rows)}</tbody></table>
<div class=bar><label><input type=checkbox id=blind> Adları gizle (sütunlar karışık sırayla A, B…)</label>
<span id=tally></span><button id=export>Tercihleri indir</button></div>
<nav class=qnav>{nav}</nav>
{"".join(sections)}
</main><script>const DATA={json.dumps(data, ensure_ascii=False)};{JS}</script></body></html>"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs", nargs="+", type=Path)
    ap.add_argument("--etiket", action="append", default=[], help='"<klasör adı>=Sütun adı"')
    ap.add_argument("--gonder", action="store_true")
    args = ap.parse_args()
    labels = dict(e.split("=", 1) for e in args.etiket)
    questions = {q["id"]: q for q in golden.load_questions()}
    checkers: dict = {}
    runs = []
    for run_dir in args.runs:
        run_dir = run_dir if run_dir.is_absolute() else (golden.RUNS_DIR / run_dir if not run_dir.exists() else run_dir)
        if not run_dir.is_dir():
            sys.exit(f"yok: {run_dir}")
        model = run_model(run_dir)
        label = labels.get(run_dir.name, NAMES.get(model, model))
        runs.append((label, run_dir.resolve(), collect(run_dir, questions, checkers)))
        print(f"{label}: {len(runs[-1][2])} soru ({run_dir.name})")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page(runs, questions), encoding="utf-8")
    print(f"sayfa: {OUT.relative_to(ROOT)}")
    if args.gonder:
        subprocess.run([str(ROOT / "scripts" / "taslak-gonder.sh"), str(OUT)], check=True)


if __name__ == "__main__":
    main()
