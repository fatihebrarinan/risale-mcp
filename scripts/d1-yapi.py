"""D14.2'nin hazırlığı: İşârât'ın Bakara 9'dan 31–33'e kadarki birimlerinde üç vecihten başka neler var (PLANLAR.md D14).

    uv run python scripts/d1-yapi.py oku [birim…]     # birim başına model okuması (araçsız): data/d1/isarat-yapi/<birim>.json
    uv run python scripts/d1-yapi.py rapor            # tablo ve özet: data/d1/isarat-yapi/rapor.md

Kararlar (kullanıcı, 2026-11-17): mukaddime ve mesele, ders ve irşad, soru–cevap, tenbih ve tezyîl, müellifin Türkçe
hâşiyeleri; her birinin yeri, dayandığı lafız, hitap, uzunluğu; ders ne zaman geliyor. Model kısımları ve cümle
aralıklarını yazar (istem `docs/d1/yapi-istemi.md`); kimlikleri ve uzunlukları program denetler ve hesaplar. Saklı
birimler de içindedir: sonuçtan taslağa yalnız genel kural gider.
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

PROMPT = ROOT / "docs" / "d1" / "yapi-istemi.md"
OUT = P.KEEP / "isarat-yapi"
ROOT_NODE = "isaratul-icaz-arabi/sure-i-bakara"
FIRST, LAST = "9-10-ayetlerin-tefsiri", "31-33-ayetlerin-tefsiri"


def conn() -> sqlite3.Connection:
    return sqlite3.connect(f"file:{P.GENEL_DB}?mode=ro", uri=True)


def units(c: sqlite3.Connection) -> list[str]:
    sibs = [r[0].rsplit("/", 1)[1] for r in c.execute("SELECT id FROM nodes WHERE parent_id = ? ORDER BY ord", (ROOT_NODE,))]
    return sibs[sibs.index(FIRST):sibs.index(LAST) + 1]


def sentences(c: sqlite3.Connection, unit: str) -> list[tuple[str, str, str, str]]:
    """Birimin Arapça cümleleri kitap sırasıyla: (yerel kimlik, düğüm, paragraf, metin)."""
    node = f"{ROOT_NODE}/{unit}"
    rows = c.execute("SELECT s.id, s.node_id, s.paragraph_id, s.text FROM sentences s JOIN nodes n ON n.id = s.node_id "
                     "WHERE n.id = ? OR n.id LIKE ? ORDER BY s.seq", (node, node + "/%")).fetchall()
    return [(sid[len(node) + 1:], nid, pid, text) for sid, nid, pid, text in rows]


def hasiyeler(c: sqlite3.Connection, unit: str) -> list[str]:
    node = f"isaratul-icaz/sure-i-bakara/{unit}"
    return [t for (t,) in c.execute("SELECT p.text FROM paragraphs p JOIN nodes n ON n.id = p.node_id WHERE (n.id = ? OR "
                                    "n.id LIKE ?) AND p.kind = 'hasiye' ORDER BY n.ord, p.ord", (node, node + "/%"))]


def render(c: sqlite3.Connection, unit: str) -> str:
    L, node, para = [], None, None
    for sid, nid, pid, text in sentences(c, unit):
        if nid != node:
            ref = c.execute("SELECT ref FROM nodes WHERE id = ?", (nid,)).fetchone()[0]
            L += ["", f"### {ref}", ""]
            node, para = nid, None
        if pid != para:
            L.append("")
            para = pid
        L.append(f"[{sid}] {text}")
    hs = hasiyeler(c, unit)
    if hs:
        L += ["", "# Müellifin Türkçe hâşiyeleri", ""] + [f"{i}. {t}" for i, t in enumerate(hs, 1)]
    return "\n".join(L).strip()


def words(text: str) -> int:
    return len(re.findall(r"\S+", text))


def check(c: sqlite3.Connection, unit: str, data: dict) -> dict:
    """Kimlikleri denetler, her kısmın cümle ve kelime sayısını ve birimdeki payını hesaplar."""
    rows = sentences(c, unit)
    index = {sid: i for i, (sid, *_) in enumerate(rows)}
    total = sum(words(t) for *_, t in rows)
    bad = []
    for k in data.get("kisimlar", []):
        a, b = index.get(k.get("ilk")), index.get(k.get("son"))
        if a is None or b is None or b < a:
            bad.append(k.get("ilk"))
            k["denetim"] = "kimlik"
            continue
        w = sum(words(rows[i][3]) for i in range(a, b + 1))
        k.update(cumle=b - a + 1, kelime=w, pay=round(100 * w / total, 1), sira=round(100 * a / len(rows)))
    for v, sid in (data.get("vecihler") or {}).items():
        if sid and sid not in index:
            bad.append(sid)
    data["birim"] = unit
    data["toplam"] = {"cumle": len(rows), "kelime": total}
    data["hasiye_kelime"] = [words(t) for t in hasiyeler(c, unit)]
    data["denetim"] = {"bilinmeyen_kimlik": bad}
    return data


def oku(only: list[str]) -> None:
    c = conn()
    OUT.mkdir(parents=True, exist_ok=True)
    raw = PROMPT.read_text(encoding="utf-8")
    body = re.split(r"^---- YAPI ----$", raw, maxsplit=1, flags=re.M)[1].strip()
    todo = [u for u in units(c) if not only or u in only or any(u.startswith(o) for o in only)]

    def one(unit: str):
        stem = OUT / unit
        if stem.with_suffix(".json").exists():
            return unit, json.loads(stem.with_suffix(".json").read_text(encoding="utf-8"))
        prompt = body.format(birim=unit, metin=render(conn(), unit))     # iş parçacığı başına bağlantı
        data = Y.run_model(prompt, "opus", stem, {"gorev": "isarat-yapi", "surum": "y1", "istem_sha": P._sha(raw),
                                                  "birim": unit})
        if data is None:
            return unit, None
        data = check(sqlite3.connect(f"file:{P.GENEL_DB}?mode=ro", uri=True), unit, data)
        stem.with_suffix(".json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        return unit, data

    with ThreadPoolExecutor(max_workers=4) as pool:
        for unit, data in pool.map(one, todo):
            if data is None:
                print(f"{unit}: okunamadı")
                continue
            ks = data.get("kisimlar", [])
            print(f"{unit}: {len(ks)} kısım ({', '.join(k['tur'] for k in ks)}); bilinmeyen kimlik "
                  f"{len(data['denetim']['bilinmeyen_kimlik'])}")


def rapor() -> None:
    c = conn()
    L = ["# İşârât'ta üç vecih dışındaki kısımlar (Bakara 9 – 31–33)", "",
         "D14.2'nin hazırlığı (PLANLAR.md D14). Kısımları birim başına bir model okuması (Opus, araçsız; istem "
         "`docs/d1/yapi-istemi.md` y1) buldu; cümle aralıklarını ve uzunlukları program denetledi ve hesapladı. Pay: "
         "kısmın Arapça kelimesi / birimin Arapça kelimesi. Sıra: kısmın başladığı yer, birimin yüzde kaçında.", "",
         "| Birim | Kelime | Tür | Ad | Yer | Lafız | Hitap | Cümle | Pay % | Sıra % |",
         "|---|---:|---|---|---|---|---|---:|---:|---:|"]
    by_type: dict[str, list] = {}
    notes = []
    for unit in units(c):
        path = OUT / f"{unit}.json"
        if not path.exists():
            L.append(f"| {unit} | | (okunmadı) | | | | | | | |")
            continue
        d = json.loads(path.read_text(encoding="utf-8"))
        ks = d.get("kisimlar", [])
        if not ks:
            L.append(f"| {unit} | {d['toplam']['kelime']} | — | | | | | | | |")
        for k in ks:
            by_type.setdefault(k["tur"], []).append((unit, k))
            L.append(f"| {unit} | {d['toplam']['kelime']} | {k['tur']} | {k.get('ad', '')} | {k.get('yer', '')} | "
                     f"{k.get('lafiz') or ''} | {'evet' if k.get('hitap') else ''} | {k.get('cumle', '?')} | "
                     f"{k.get('pay', '?')} | {k.get('sira', '?')} |")
        if d.get("hasiyeler"):
            notes.append(f"- {unit}: hâşiyeler " + "; ".join(f"{h.get('tur')} ({h.get('ozet', '')})" for h in d["hasiyeler"]))
        notes.append(f"- {unit}: {d.get('genel', '')}" + (f" Vecihler: {d.get('vecih_notu')}" if d.get("vecih_notu") else ""))
    L += ["", "## Türlere göre", ""]
    for t, xs in sorted(by_type.items()):
        pays = [k.get("pay", 0) for _, k in xs if isinstance(k.get("pay"), (int, float))]
        units_ = sorted({u for u, _ in xs})
        L.append(f"- **{t}**: {len(xs)} kısım, {len(units_)} birimde ({', '.join(units_)}); pay "
                 + (f"ortalama %{sum(pays) / len(pays):.1f}, en çok %{max(pays):.1f}" if pays else "?")
                 + "; yerler: " + ", ".join(sorted({k.get('yer', '') for _, k in xs})))
    L += ["", "## Birim notları (modelin özeti)", ""] + notes
    (OUT / "rapor.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("oku")
    p.add_argument("birim", nargs="*")
    sub.add_parser("rapor")
    a = ap.parse_args()
    if a.cmd == "oku":
        oku(a.birim)
    else:
        rapor()


if __name__ == "__main__":
    main()
