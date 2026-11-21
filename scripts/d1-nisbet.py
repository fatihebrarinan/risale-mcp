"""D14.5b nisbet denetçisi (PLANLAR.md D14.5b; kullanıcının kararı, 2026-11-18).

    uv run python scripts/d1-nisbet.py denetle 9-10 --taslak 1 8     # her taslak için tek model çağrısı (araçsız)
    uv run python scripts/d1-nisbet.py rapor 9-10 13                   # data/d1/nisbet-raporu.md

Taslakta bir kaynağa atıf veren her Türkçe tercüme cümlesi, o kaynağın atıf verilen cümleleri ve iki yanındaki dörder
cümleyle birlikte modele gider; model her cümlenin nisbetini tartar (istem `docs/d1/nisbet-istemi.md` n1): doğru,
nakil, itiraz, reddedilen, kaynakta yok, aşıyor, nisbet yok. Âyet atıfları denetlenmez. Kaynağın metni prova
veritabanlarından (sınanan birimin İşârât'ı zaten yoktur). Denetçi yalnız nisbeti sorar; taslağın değerini değil.
Güvenilirse D5.0'da üretim hattının kalite kapısıdır; cümle düzeyinde düzeltme sonra.
"""

import argparse
import importlib.util
import json
import re
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from risale_mcp.paths import ROOT


def _load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


Y = _load("d1_yz", "d1-yz.py")
P = Y.P

PROMPT = ROOT / "docs" / "d1" / "nisbet-istemi.md"
SURUM = "n1"
BAGLAM = 4             # atıf verilen cümlelerin iki yanından alınan cümle
HUKUM = ("dogru", "nakil", "itiraz", "reddedilen", "kaynakta_yok", "asiyor", "nisbet_yok")
HATA = ("nakil", "itiraz", "reddedilen", "kaynakta_yok", "asiyor")


def _ids(unit: str, n: int) -> dict[str, tuple[str, str]]:
    ids = dict(P.draft_sources(P.DRAFTS / unit / f"taslak-{n}.jsonl"))
    kp = P.DRAFTS / unit / f"taslak-{n}.kaynak.json"
    if kp.exists():
        ids.update({k: tuple(v) for k, v in json.loads(kp.read_text(encoding="utf-8")).items()})
    return ids


def context(texts, server: str, sid: str) -> str | None:
    """Atıf verilen cümleler »…« arasında, iki yanında BAGLAM cümle (aynı bölümde)."""
    for path in texts.dbs.get(server, []):
        conn = texts._conn(path)
        if conn is None or not P._has(conn, "sentences"):
            continue
        first, _, last = sid.partition("..")
        row = conn.execute("SELECT seq, node_id FROM sentences WHERE id = ?", (first,)).fetchone()
        if not row:
            continue
        end_id = (first.rsplit("/", 1)[0] + "/" + last) if last and "/" not in last else (last or first)
        end = conn.execute("SELECT seq FROM sentences WHERE id = ?", (end_id,)).fetchone()
        a, b = row[0], end[0] if end else row[0]
        rows = conn.execute("SELECT seq, text FROM sentences WHERE node_id = ? AND seq BETWEEN ? AND ? ORDER BY seq",
                            (row[1], a - BAGLAM, b + BAGLAM)).fetchall()
        return " ".join(f"»{t}«" if a <= s <= b else t for s, t in rows)
    return None


def clip(ctx: str, n: int = 4000) -> str:
    """Bağlamı `n` harfe indirir ama atfedilen kısmı (»…«) içeride tutar (2026-11-21, Bakara 34: baştan kesilince
    Ebüssuûd'un uzun önceki cümleleri atfedilen cümleyi dışarıda bırakıyordu; denetçi "kaynakta yok" diyordu)."""
    if len(ctx) <= n:
        return ctx
    i = ctx.find("»")
    if i < 0:
        return ctx[:n]
    j = ctx.find("«", i) + 1 or len(ctx)
    if j - i >= n:
        return ctx[i:i + n] + "…"
    start = max(0, i - (n - (j - i)) // 2)
    return ("…" if start else "") + ctx[start:start + n] + ("…" if start + n < len(ctx) else "")


def items(unit: str, n: int) -> list[dict]:
    blocks, cites = Y.draft_blocks(unit, n)
    ids = _ids(unit, n)
    texts = P.SourceTexts(unit)
    by_src: dict[str, list[str]] = {}
    for a, lang, q, t in blocks:
        if lang != "tr" or q:
            continue
        sents = re.split(r"(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜÂÎÛ«\"“(﴿])", t)
        for i, sent in enumerate(sents):
            for m in re.finditer(r"\[([^\[\]\n]{1,80})\]", sent):
                for k in re.findall(r"\d+", m.group(1)):
                    if k in ids:
                        prev = sents[i - 1] if i else ""
                        by_src.setdefault(k, [])
                        line = (prev + " " if prev and len(sent) < 120 else "") + sent
                        if line not in by_src[k]:
                            by_src[k].append(line)
    out = []
    for k, lines in sorted(by_src.items(), key=lambda kv: int(kv[0])):
        server, sid = ids[k]
        if not sid:
            continue
        ctx = context(texts, server, sid) if server != "hadis" else texts.hadith(texts._conn(P.HADIS_DB), sid)
        if not ctx:
            continue
        out.append({"kaynak": k, "atif": cites.get(k, ""), "id": sid, "sunucu": server, "baglam": clip(ctx),
                    "cumleler": lines})
    return out


def prompt_for(unit: str, its: list[dict]) -> str:
    cfg = P.UNITS[unit]
    raw = PROMPT.read_text(encoding="utf-8")
    body = re.split(r"^---- NISBET ----$", raw, maxsplit=1, flags=re.M)[1].strip()
    L = []
    for it in its:
        L += [f"## Kaynak [{it['kaynak']}]: {it['atif']}", "", f"Bağlam: {it['baglam']}", "", "Taslak cümleleri:"]
        L += [f"{j}. {c}" for j, c in enumerate(it["cumleler"], 1)] + [""]
    a, b = cfg["ayahs"]
    return body.format(sura_name=cfg["sura_name"], ayahs=f"{a}" if a == b else f"{a}–{b}", kalemler="\n".join(L))


def denetle(unit: str, ns: list[int]) -> None:
    def one(n: int):
        its = items(unit, n)
        stem = Y.out_dir(unit) / f"nisbet-taslak-{n}"
        if stem.with_suffix(".json").exists():
            print(f"{stem.name}: var")
            return
        data = Y.run_model(prompt_for(unit, its), "opus", stem, {"gorev": "nisbet", "surum": SURUM, "taslak": n,
                                                                  "kaynak": len(its)})
        if data is None:
            return
        data["kalemler"] = its
        stem.with_suffix(".json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        hs = [h.get("hukum") for h in data.get("hukumler", [])]
        print(f"{unit} taslak {n}: {len(its)} kaynak, {len(hs)} hüküm; hata {sum(h in HATA for h in hs)} "
              f"({', '.join(f'{x} {hs.count(x)}' for x in HUKUM if hs.count(x))})")

    with ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(one, ns))


def rapor(units: list[str]) -> None:
    L = ["# Nisbet denetçisinin bulguları (D14.5b, n1)", ""]
    for unit in units:
        for path in sorted(Y.out_dir(unit).glob("nisbet-taslak-*.json")):
            if path.name.endswith(".meta.json"):
                continue
            d = json.loads(path.read_text(encoding="utf-8"))
            meta = json.loads(path.with_name(path.stem + ".meta.json").read_text(encoding="utf-8"))
            hs = d.get("hukumler", [])
            src = {it["kaynak"]: it for it in d.get("kalemler", [])}
            n = path.stem.rsplit("-", 1)[1]
            L += [f"## {unit}, taslak {n} ({len(src)} kaynak, {len(hs)} hüküm, ≈{meta.get('cost_usd') or 0:.2f} $)", "",
                  "| Hüküm | Sayı |", "|---|---:|"] + [f"| {x} | {sum(h.get('hukum') == x for h in hs)} |" for x in HUKUM] + [""]
            L += ["Hata hükümleri:", ""]
            for h in hs:
                if h.get("hukum") in HATA:
                    it = src.get(str(h.get("kaynak")), {})
                    L.append(f"- **{h['hukum']}** [{h.get('kaynak')}] `{it.get('id', '')}`: "
                             f"\"{h.get('taslak_alinti', '')}\" — {h.get('gerekce', '')}")
            L.append("")
    out = P.KEEP / "nisbet-raporu.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(out.relative_to(ROOT))


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("denetle")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--taslak", type=int, nargs="+", required=True)
    p = sub.add_parser("rapor")
    p.add_argument("units", nargs="+")
    a = ap.parse_args()
    if a.cmd == "denetle":
        denetle(a.unit, a.taslak)
    else:
        rapor(a.units)


if __name__ == "__main__":
    main()
