"""D14.7 İşârât'ın soru kalıpları (PLANLAR.md D14.7; kullanıcının kararı, 2026-11-18).

    uv run python scripts/d1-kalip.py liste            # geliştirme birimlerinden kalıp listesi (tek model çağrısı)
    uv run python scripts/d1-kalip.py sizinti          # listeyi yasak birimlere karşı dener
    uv run python scripts/d1-kalip.py yaz              # docs/d1/soru-kaliplari.md (kullanıcının okuması, istemin eki)
    uv run python scripts/d1-kalip.py tablo 14-15      # birimin tarama tablosu (h10; âyetin metninden, İşârât'sız)
    uv run python scripts/d1-kalip.py kontrol 14-15 7  # taslağın Tarama'sı: cevapsız satırlar, taşıyor/taşımıyor

Kaynak yalnız geliştirme birimleri: Fâtiha, Bakara 1–8, 9–10, 11–12, 13, 17–20, 23–24, 31–33 (Arapça metin, kişisel
veritabanından) ve envanteri olanların (9–10, 11–12, 13, 31–33) okumayla çıkarılmış nükteleri. 14–15 (D14.7'de sınanan),
16 (yedek temiz birim) ve saklı birimler (21–22, 25, 26–27, 28, 29, 30; D15) verilmez. Sızıntı testi listenin Arapça ve
Türkçe metnini yasak birimlerin İşârât'ıyla (iki dilde) 5 kelimelik dizilerle karşılaştırır; örnek yerlerinin birimini
denetler. Model İşârât'ı ezberinden de bilebilir: bu yüzden test listenin bütün metnine bakar, yalnız kaynağa değil.
"""

import argparse
import importlib.util
import json
import re
import sqlite3
from pathlib import Path

from risale_mcp.normalize import match_words
from risale_mcp.paths import DATA_DIR, ROOT


def _load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


Y = _load("d1_yz", "d1-yz.py")
P = Y.P

PROMPT = ROOT / "docs" / "d1" / "kalip-istemi.md"
SURUM = "k1"
DB = DATA_DIR / "dist" / "kisisel" / "risale.db"
OUT = P.KEEP / "kaliplar"
DOC = ROOT / "docs" / "d1" / "soru-kaliplari.md"
B = "sure-i-bakara/"
KAYNAK = [("sure-i-fatiha", "Fâtiha")] + [(f"{B}{i}", f"Bakara {i}") for i in range(1, 9)] + [
    (f"{B}9-10-ayetlerin-tefsiri", "Bakara 9–10"), (f"{B}11-12-ayetlerin-tefsiri", "Bakara 11–12"),
    (f"{B}13", "Bakara 13"), (f"{B}17-20-ayetlerin-tefsiri", "Bakara 17–20"),
    (f"{B}23-24-ayetlerin-tefsiri-nubuvvet-hakkinda", "Bakara 23–24"), (f"{B}31-33-ayetlerin-tefsiri", "Bakara 31–33")]
ENVANTER = {"9-10": "Bakara 9–10", "11-12": "Bakara 11–12", "13": "Bakara 13", "31-33": "Bakara 31–33"}
YASAK = [(f"{B}14-15-ayetlerin-tefsiri", "Bakara 14–15"), (f"{B}16", "Bakara 16"),
         (f"{B}21-22-ayetlerin-tefsiri", "Bakara 21–22"), (f"{B}25", "Bakara 25"),
         (f"{B}26-27-ayetlerin-tefsiri", "Bakara 26–27"), (f"{B}28", "Bakara 28"), (f"{B}29", "Bakara 29"),
         (f"{B}30", "Bakara 30")]
N = 5


TR_NODES = {f"{B}21-22-ayetlerin-tefsiri": (f"{B}21", f"{B}22")}   # Türkçede 21 ve 22 ayrı bölüm


def text_of(conn, work: str, node: str) -> str:
    if work == "isaratul-icaz" and node in TR_NODES:
        return "\n\n".join(text_of(conn, work, n) for n in TR_NODES[node])
    o, l = conn.execute("SELECT ord, last_ord FROM nodes WHERE id = ?", (f"{work}/{node}",)).fetchone()
    rows = conn.execute("""SELECT p.text FROM paragraphs p JOIN nodes n ON p.node_id = n.id
                           WHERE n.work = ? AND n.ord BETWEEN ? AND ? AND p.text IS NOT NULL ORDER BY p.ord""",
                        (work, o, l)).fetchall()
    return "\n\n".join(r[0] for r in rows)


def _bolum(ad: str) -> str:
    raw = PROMPT.read_text(encoding="utf-8")
    body = raw.split(f"---- {ad} ----", 1)[1]
    return body.split("\n---- ", 1)[0].strip()


def kaynaklar() -> str:
    conn = sqlite3.connect(DB)
    L = []
    for node, ad in KAYNAK:
        L += [f"## {ad}", "", text_of(conn, "isaratul-icaz-arabi", node), ""]
        unit = next((u for u, a in ENVANTER.items() if a == ad), None)
        if unit:
            items = Y.page_data(unit)["items"]
            L += [f"### {ad}: envanter (okumayla çıkarılmış nükteler; lafız ← nükte)", ""]
            L += [f"- [{it.get('v', '')}] {it.get('l', '')}: {it.get('n', '')}" for it in items.values()] + [""]
    return "\n".join(L)


def liste() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    raw = _bolum("KALIP")
    prompt = raw.format(kaynaklar=kaynaklar())
    stem = OUT / f"liste-{SURUM}"
    (OUT / f"istem-{SURUM}.md").write_text(prompt, encoding="utf-8")
    print(f"istem: {len(prompt):,} harf")
    data = Y.run_model(prompt, "opus", stem, {"gorev": "kalip", "surum": SURUM})
    if data:
        print(f"{len(data.get('kaliplar', []))} kalıp")


def _grams(text: str) -> set[tuple]:
    w = match_words(text)
    return {tuple(w[i:i + N]) for i in range(len(w) - N + 1)}


def sizinti() -> bool:
    data = json.loads((OUT / f"liste-{SURUM}.json").read_text(encoding="utf-8"))
    conn = sqlite3.connect(DB)
    ok, L = True, [f"# Sızıntı testi: soru kalıpları {SURUM}", ""]
    yasak_ad = {ad for _, ad in YASAK}
    for k in data["kaliplar"]:
        for o in k.get("ornekler", []):
            if o.get("birim") in yasak_ad or o.get("birim") not in {ad for _, ad in KAYNAK}:
                ok = False
                L.append(f"- **örnek yeri kaynakta değil:** {k['ad']}: {o.get('birim')}")
    liste_g = _grams(json.dumps(data, ensure_ascii=False))
    kaynak_g = set().union(*(_grams(text_of(conn, w, n)) for n, _ in KAYNAK for w in ("isaratul-icaz-arabi", "isaratul-icaz")))
    for node, ad in YASAK:
        for work in ("isaratul-icaz-arabi", "isaratul-icaz"):
            ortak = (liste_g & _grams(text_of(conn, work, node))) - kaynak_g   # kaynakta da geçen ortak kalıp sayılmaz
            if ortak:
                ok = False
                L.append(f"- **{ad} ({work}):** {len(ortak)} ortak dizi: " + "; ".join(" ".join(g) for g in list(ortak)[:5]))
    L.append("" if not ok else "Temiz: örnek yerleri kaynak birimlerde; yasak birimlerle ortak 5'li dizi yok.")
    (OUT / f"sizinti-{SURUM}.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L[2:]) or "temiz")
    return ok


DUZEY = {"kelime": "Kelime", "cumle": "Cümle", "cumleler": "Cümleler arası", "ayet": "Âyetin bütünü"}


def markdown(data: dict) -> str:
    L = []
    for d, ad in DUZEY.items():
        ks = [k for k in data["kaliplar"] if k.get("duzey") == d]
        if not ks:
            continue
        L += [f"## {ad}", ""]
        for k in ks:
            L += [f"### {k['ad']}", "", f"**Soru:** {k['soru']}", "", "İşârât'ın cevapları:"]
            L += [f"- {c}" for c in k.get("cevaplar", [])]
            L += ["", "Örnekler: " + "; ".join(f"{o['birim']} «{o['lafiz']}»: {o['nukte']}" for o in k.get("ornekler", [])),
                  "", f"Dikkat: {k.get('dikkat', '')}", ""]
    return "\n".join(L)


def yaz() -> None:
    data = json.loads((OUT / f"liste-{SURUM}.json").read_text(encoding="utf-8"))
    head = (f"# İşârât'ın soru kalıpları ({SURUM})\n\nD14.7 (PLANLAR.md). `scripts/d1-kalip.py`, istem "
            "`docs/d1/kalip-istemi.md`. Kaynak yalnız geliştirme birimleri; 14–15, 16 ve saklı birimler girmez. "
            "Tanıma (kural ya da model) ve sıklık listenin JSON'undadır (`data/d1/kaliplar/`).\n\n")
    DOC.write_text(head + markdown(data), encoding="utf-8")
    print(DOC.relative_to(ROOT), len(data["kaliplar"]), "kalıp")


# ---------------------------------------------------------------- tarama tablosu (D14.7, h10)

YALNIZ_LISTE = ("Vecihlerin çokluğu (ihtimal)", "Kayıtların tek garaza akması", "Dört esas maksadın remzi")   # kullanıcı


def kaliplar() -> list[dict]:
    data = json.loads((OUT / f"liste-{SURUM}.json").read_text(encoding="utf-8"))
    return [k for k in data["kaliplar"] if k["ad"] not in YALNIZ_LISTE]


def tablo_path(unit: str) -> Path:
    return P.OUT / unit / "tarama-tablosu.json"


def tablo(unit: str, again: bool = False) -> list[dict]:
    path = tablo_path(unit)
    if path.exists() and not again:
        return json.loads(path.read_text(encoding="utf-8"))["satirlar"]
    cfg = P.UNITS[unit]
    a, b = cfg["ayahs"]
    conn = sqlite3.connect(P.OUT / unit / "risale.db")
    ayat = conn.execute("SELECT ayah, text FROM quran_ayahs WHERE sura = ? AND ayah BETWEEN ? AND ? ORDER BY ayah",
                        (cfg["sura"], a, b)).fetchall()
    ks = kaliplar()
    klist = "\n".join(f"- **{k['ad']}** ({DUZEY[k['duzey']]}; tanıma: {k['tanima']}"
                       + (f", kural `{k['kural']}`" if k.get("kural") else "") + f"): {k['soru']} Dikkat: {k.get('dikkat', '')}"
                       for k in ks)
    prompt = _bolum("TABLO").format(sura_name=cfg["sura_name"], ayahs=f"{a}" if a == b else f"{a}–{b}",
                                    ayetler="\n".join(f"({n}) {t}" for n, t in ayat), kaliplar=klist)
    data = Y.run_model(prompt, "opus", P.OUT / unit / "tarama-tablosu-model", {"gorev": "tarama-tablosu", "surum": SURUM})
    if not data:
        raise SystemExit("tablo kurulamadı")
    adlar = {k["ad"] for k in ks}
    rows, seen = [], set()
    for r in data.get("satirlar", []):
        key = (r.get("ayet"), r.get("lafiz", "").strip(), r.get("kalip"))
        if r.get("kalip") not in adlar or key in seen:
            print(f"  atıldı: {r}")
            continue
        seen.add(key)
        rows.append({"ayet": r.get("ayet"), "lafiz": key[1], "kalip": r["kalip"]})
    # kural: her âyetin fâsılası tabloda (son kelime)
    for n, t in ayat:
        if not any(r["ayet"] == n and r["kalip"] == "Fâsıla" for r in rows):
            last = t.split()[-1]
            rows.append({"ayet": n, "lafiz": last, "kalip": "Fâsıla", "program": True})
    rows.sort(key=lambda r: (r["ayet"] or 0,))   # âyet sırası; âyet içinde modelin sırası korunur (sort kararlı)
    for i, r in enumerate(rows, 1):
        r["id"] = f"T{i:02d}"
    path.write_text(json.dumps({"surum": SURUM, "satirlar": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{path.relative_to(ROOT)}: {len(rows)} satır")
    return rows


def tablo_md(unit: str) -> str:
    L = ["| # | Âyet | Lafız | Kalıp |", "|---|---:|---|---|"]
    L += [f"| {r['id']} | {r['ayet']} | {r['lafiz']} | {r['kalip']} |" for r in tablo(unit)]
    return "\n".join(L)


TARAMA_RE = re.compile(r"^\s*-\s*(T\d+)\b(.*)$", re.M)


def kontrol(unit: str, n: int) -> dict:
    """Taslağın Tarama'sı: her satırın cevabı (taşıyor / taşımıyor / yok)."""
    tp = P.DRAFTS / unit / f"taslak-{n}.tarama.md"
    text = tp.read_text(encoding="utf-8") if tp.exists() else ""
    rows = tablo(unit)
    ans = {m.group(1): m.group(2) for m in TARAMA_RE.finditer(text)}
    out = {"satir": len(rows), "tasiyor": 0, "tasimiyor": 0, "cevapsiz": []}
    for r in rows:
        t = ans.get(r["id"], "")
        if re.search(r"taşımıyor", t, re.I):
            out["tasimiyor"] += 1
        elif re.search(r"taşıyor", t, re.I):
            out["tasiyor"] += 1
        else:
            out["cevapsiz"].append(r["id"])
    print(f"{unit} taslak {n}: {out['satir']} satır; taşıyor {out['tasiyor']}, taşımıyor {out['tasimiyor']}, "
          f"cevapsız {len(out['cevapsiz'])} {out['cevapsiz'][:10]}")
    return out


def _iskelet(t: str) -> set[str]:
    from risale_mcp.quran import skeleton
    return {skeleton(w) for w in re.findall(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+", t) if len(skeleton(w)) >= 2}


def kayip(unit: str, n: int) -> dict:
    """Envanterin nükteleri (vecih 2 ve 3) için: taslakta var mı (eşleştirme), lafzı tabloda mı, yazar ne dedi.
    Kaçırılan nükte üç türe ayrılır: tabloda yok / yazar taşımıyor dedi / taşıyor deyip yazmadı (ya da cevapsız)."""
    pd = Y.page_data(unit)
    rows = pd["drafts"][f"taslak-{n}"]["rows"]
    tp = P.DRAFTS / unit / f"taslak-{n}.tarama.md"
    ans = {m.group(1): m.group(2) for m in TARAMA_RE.finditer(tp.read_text(encoding="utf-8"))} if tp.exists() else {}
    tab = tablo(unit)
    out, L = {"tabloda_yok": [], "tasimiyor": [], "yazmadi": [], "var": []}, []
    for nid, it in pd["items"].items():
        if it.get("v") not in ("V2", "V3"):
            continue
        d = ((rows.get(nid) or {}).get("opus") or {}).get("d")
        sk = _iskelet(it.get("l", ""))
        hits = [r for r in tab if sk & _iskelet(r["lafiz"])]
        if d in ("aynen", "kismen"):
            out["var"].append(nid)
            continue
        if not hits:
            kind = "tabloda_yok"
        elif any(re.search("taşıyor", ans.get(r["id"], ""), re.I) and not re.search("taşımıyor", ans.get(r["id"], ""), re.I)
                 for r in hits):
            kind = "yazmadi"
        else:
            kind = "tasimiyor"
        out[kind].append(nid)
        L.append(f"- {nid} [{kind}] {it.get('l', '')}: {it.get('n', '')[:90]} | satırlar: "
                 + ", ".join(f"{r['id']} {r['kalip']} → {ans.get(r['id'], '—')[:60]}" for r in hits[:4]))
    print(f"{unit} taslak {n}: var {len(out['var'])}; kaçırılan: tabloda yok {len(out['tabloda_yok'])}, "
          f"taşımıyor {len(out['tasimiyor'])}, taşıyor deyip yazmadı {len(out['yazmadi'])}")
    (P.DRAFTS / unit / f"taslak-{n}.kayip.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["liste", "sizinti", "yaz", "tablo", "kontrol", "kayip"])
    ap.add_argument("unit", nargs="?")
    ap.add_argument("taslak", nargs="?", type=int)
    ap.add_argument("--yeniden", action="store_true")
    a = ap.parse_args()
    if a.cmd == "tablo":
        tablo(a.unit, a.yeniden)
    elif a.cmd == "kontrol":
        kontrol(a.unit, a.taslak)
    elif a.cmd == "kayip":
        kayip(a.unit, a.taslak)
    else:
        {"liste": liste, "sizinti": sizinti, "yaz": yaz}[a.cmd]()


if __name__ == "__main__":
    main()
