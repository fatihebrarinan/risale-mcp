"""D5.0 (4) birim bölümlemesi: İşârât âyetleri neden birleştiriyor, neden ayırıyor (PLANLAR.md D5; kullanıcının
kararı, 2026-11-19: önce İşârât'ın mantığı, sonra bütün Kur'ân).

    uv run python scripts/d1-bolme.py tablo     # Bakara 1–33'ün 32 geçişi, mekanik özellikler: data/d1/bolme/gecisler.json
    uv run python scripts/d1-bolme.py oku       # her geçişte müellifin sözü (tek model çağrısı): okuma.json
    uv run python scripts/d1-bolme.py rapor     # gecisler.md: tablo, müellifin sözü, alıntı denetimi

Geçiş `k|k+1`: İşârât k ile k+1'i ayrı birimde (`sinir`) ya da aynı birimde (`birlikte`) tahlil eder. Müellifin bağ
hakkındaki sözü iki yerde aranır: sınırda sonraki birimin birinci vechi (mâkabliyle irtibat), birlikte olanda birimin
ikinci vechi (cümleler arası nazım). Vecih başları birim çizelgesinden (`docs/d1/birim-cizelgesi.md`, Bakara tablosu).
17–20 çizelgede iki satırdır (17–18, 19–20); İşârât onları tek birimde ama iki temsil olarak işler, 18|19 ayrıca
işaretlenir (`ic_sinir`). Okuma yalnız bölme kuralı içindir; D15'in yazar istemine hiçbir şey girmez. 30 D5.0'ın
kabul birimidir: yalnız sınırı (29|30, 30|31) tabloda durur, metni okumaya gitmez.
"""

import argparse
import importlib.util
import json
import re
import sqlite3
import sys
from pathlib import Path

from risale_mcp.normalize import search_words
from risale_mcp.paths import ROOT


def _load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


Y = _load("d1_yz", "d1-yz.py")
GENEL_DB = ROOT / "data" / "dist" / "genel" / "risale.db"
CIZELGE = ROOT / "docs" / "d1" / "birim-cizelgesi.md"
QURAN = ROOT / "data" / "library" / "kuran" / "quran.json"
TEFSIR = ROOT / "data" / "library" / "tefsir"
OUT = ROOT / "data" / "d1" / "bolme"
B = "isaratul-icaz-arabi/sure-i-bakara/"
LAST = 33
YEDEK = {30}                      # D5.0'ın kabul birimi: metni okunmaz
MUFESSIR = ("razi", "durr", "ibnkesir", "kessaf", "ebussuud", "bursevi")
MAX_SENT = 70                     # bir vecih parçasından en çok bu kadar cümle
CONT = re.compile(r"^(الذين|الذي|التي|اللذين|فإن|فإذا|فلما|فأ|فت|فق|فل|فم|فس|فا|ثم|أو|بل|ولكن|لكن|إلا)")


def units() -> list[dict]:
    """Bakara tablosu: [{ayahs: (a, b), V1, V2, V3}] (vecih başı: ilk kimlik ya da None)."""
    text = CIZELGE.read_text(encoding="utf-8").split("## Çizelge: Bakara", 1)[1].split("\n## ", 1)[0]
    out = []
    for line in text.split("\n"):
        m = re.match(r"\| (\d+)(?:–(\d+))? \|(.*)", line)
        if not m:
            continue
        cells = [c.strip() for c in m.group(3).split("|")]
        ids = []
        for c in cells[:3]:
            first = re.search(r"`(B/[^`]+)`", c)
            ids.append(first.group(1).replace("B/", B) if first else None)
        a = int(m.group(1))
        out.append({"ayahs": (a, int(m.group(2) or a)), "V1": ids[0], "V2": ids[1], "V3": ids[2]})
    return out


def node_of(sid: str) -> str:
    """Birimin kök düğümü: `B/<birim>`."""
    return B + sid[len(B):].split("/", 1)[0]


def unit_rows(conn, root: str) -> list[tuple[str, str]]:
    return conn.execute("SELECT id, text FROM sentences WHERE (node_id = ? OR node_id LIKE ?) AND id NOT LIKE '%/h_/%' "
                        "ORDER BY seq", (root, root + "/%")).fetchall()


def piece(conn, u: dict, key: str) -> list[tuple[str, str]]:
    """Vechin cümleleri: başından bir sonraki vecih başına (ya da MAX_SENT'e) kadar."""
    start = u[key]
    if not start:
        return []
    rows = unit_rows(conn, node_of(start))
    ids = [r[0] for r in rows]
    if start not in ids:
        sys.exit(f"çizelgedeki kimlik bulunamadı: {start}")
    i = ids.index(start)
    stops = [ids.index(u[k]) for k in ("V1", "V2", "V3") if u[k] and u[k] in ids and ids.index(u[k]) > i]
    j = min(stops + [i + MAX_SENT])
    return rows[i:j]


def boundaries(work: str) -> set[int]:
    d = json.loads((TEFSIR / f"{work}.json").read_text(encoding="utf-8"))
    out = set()
    for n in d["outline"]:
        if m := re.fullmatch(rf"{work}/2/(\d+)(?:-(\d+))?", n["id"]):
            out.add(int(m.group(2) or m.group(1)))
    return out


def tablo() -> dict:
    q = json.loads(QURAN.read_text(encoding="utf-8"))
    ayah = {a["ayah"]: a for a in q["suras"][1]["ayahs"]}
    us = units()
    unit_of = {k: (u["ayahs"][0] if u["ayahs"] != (17, 18) and u["ayahs"] != (19, 20) else 17)
               for u in us for k in range(u["ayahs"][0], u["ayahs"][1] + 1)}
    sub_of = {k: u["ayahs"] for u in us for k in range(u["ayahs"][0], u["ayahs"][1] + 1)}
    mf = {w: boundaries(w) for w in MUFESSIR}
    rows = []
    for k in range(1, LAST):
        nxt = ayah[k + 1]["text_clean"]
        rows.append({
            "gecis": f"{k}|{k + 1}",
            "isarat": "sinir" if unit_of[k] != unit_of[k + 1] else "birlikte",
            "ic_sinir": unit_of[k] == unit_of[k + 1] and sub_of[k] != sub_of[k + 1],
            "birim_once": "–".join(map(str, sub_of[k])), "birim_sonra": "–".join(map(str, sub_of[k + 1])),
            "ilk_kelimeler": " ".join(nxt.split()[:3]),
            "bag_kalibi": bool(CONT.match(nxt)),
            "kelime": [len(ayah[k]["text_clean"].split()), len(ayah[k + 1]["text_clean"].split())],
            "mufessir_sinir": sorted(w for w in MUFESSIR if k in mf[w]),
        })
    data = {"aciklama": __doc__.split("\n\n")[0], "gecisler": rows, "birimler": [u | {"ayahs": list(u["ayahs"])} for u in us]}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "gecisler.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    n = sum(r["isarat"] == "sinir" for r in rows)
    print(f"{len(rows)} geçiş: {n} sınır, {len(rows) - n} birlikte → {(OUT / 'gecisler.json').relative_to(ROOT)}")
    return data


ISTEM = """Sen İşârâtü'l-İ'câz'ın usulünü inceleyen bir araştırmacısın. Soru: Bediüzzaman Bakara 1–33'te âyetleri neden bazen
tek tek, bazen gruplar hâlinde tahlil ediyor? Aşağıda Bakara 1–33'ün âyetleri ve 32 âyet geçişi (k|k+1) var; her
geçişte İşârât'ın iki âyeti ayrı birimde mi ("sinir") yoksa aynı birimde mi ("birlikte") tahlil ettiği belli. Her
birimin İşârât'taki iki parçası da var (Arapça asıl, cümle kimlikleriyle): birinci vecih (âyetin öncekiyle bağı,
"nazm-ı mecmû' bi-mâkablihi") ve ikinci vecih (âyetin cümlelerinin birbiriyle nazmı).

Görevin, her geçiş için:
1. **Müellifin sözü:** İşârât'ın o iki âyet arasındaki bağ hakkında söylediği yer. Sınırda bunu sonraki birimin
   birinci vechinde, birlikte olanda birimin ikinci vechinde ara. Cümle kimliğini ve Arapçadan kelimesi kelimesine
   kısa bir alıntı ver (en çok ≈25 kelime; alıntı o cümlede aynen geçmeli, kısaltma için "…"). Söz yoksa boş bırak,
   uydurma.
2. **Bağın adı:** müellifin kendi terimiyle (ör. "سؤال وجواب", "دلالة"، "عطف"، "صفة"، "تمثيل", "قصة"); terim yoksa senin
   kısa tarifin, "(benim tarifim)" diye.
3. **İkinci âyet tek başına tahlil edilebilir mi:** "evet", "hayır" ya da "kısmen", bir cümle gerekçe (dil bilgisi:
   sıfat, ism-i mevsûl, şart–cevap, makûl-ül kavl; ya da mânâ: cevap, red, temsilin devamı, kıssanın sahnesi).
4. **Garaz:** iki âyetin garazı (asıl maksadı) bir mi, ayrı mı; kısa.

Sonra **aday kurallar**: bütün geçişleri açıklamaya çalışan en çok beş kural. Her kural için hangi geçişleri
açıkladığı ve hangilerinin istisna kaldığı. Kuralları müellifin kavramlarıyla kur (nazm, garaz, mâkabl, cümleler arası
nazım). Özellikle şunu açıkla: 3, 4, 5 dil bilgisine göre 2'deki «المتقين»ın sıfatlarıdır, yine de ayrı birimdir;
21–22 ve 26–27'de sıfat ve ism-i mevsûl birleştirir. Kesin bilgi yoksa "tahmin" de. 30. âyetin metni verilmedi
(saklı); 29|30 ve 30|31 geçişlerinde yalnız tabloyu kullan.

Cevabın yalnız şu JSON (Türkçe; alıntılar Arapça):
```json
{{"gecisler": [{{"gecis": "1|2", "soz": [{{"id": "...", "alinti": "..."}}], "bag": "...", "ikinci_tek_basina": "evet|hayır|kısmen", "gerekce": "...", "garaz": "..."}}],
 "aday_kurallar": [{{"kural": "...", "aciklar": ["9|10", "..."], "istisna": ["..."], "not": "..."}}],
 "genel_not": "..."}}
```

# Âyetler (Bakara 1–33)

{ayetler}

# Geçişler

{gecisler}

# İşârât: birimlerin birinci ve ikinci vecihleri (Arapça asıl)

{metin}
"""


def oku(again: bool = False) -> dict | None:
    data = json.loads((OUT / "gecisler.json").read_text(encoding="utf-8"))
    stem = OUT / "okuma"
    if stem.with_suffix(".json").exists() and not again:
        return json.loads(stem.with_suffix(".json").read_text(encoding="utf-8"))
    q = json.loads(QURAN.read_text(encoding="utf-8"))
    tr = q["suras"][1]["ayahs"]
    ayetler = "\n".join(f"{a['ayah']}. {a['text']}" for a in tr if a["ayah"] <= LAST)
    gecisler = "\n".join(f"- {r['gecis']}: {r['isarat']}" + (" (İşârât'ın kendi alt bölmesi: iki temsil)" if r["ic_sinir"] else "")
                         for r in data["gecisler"])
    conn = sqlite3.connect(f"file:{GENEL_DB}?mode=ro", uri=True)
    L = []
    for u in data["birimler"]:
        a, b = u["ayahs"]
        if set(range(a, b + 1)) & YEDEK:
            L.append(f"\n## Birim {a}" + (f"–{b}" if b != a else "") + "\n\n(saklı: metin verilmedi)")
            continue
        L.append(f"\n## Birim {a}" + (f"–{b}" if b != a else ""))
        for key, name in (("V1", "Birinci vecih"), ("V2", "İkinci vecih")):
            rows = piece(conn, u, key)
            L.append(f"\n### {name}" + ("" if rows else ": çizelgede yok"))
            L += [f"[{sid}] {text}" for sid, text in rows]
    prompt = ISTEM.format(ayetler=ayetler, gecisler=gecisler, metin="\n".join(L))
    (OUT / "okuma-istem.md").write_text(prompt, encoding="utf-8")
    print(f"istem {len(prompt):,} harf")
    return Y.run_model(prompt, "opus", stem, {"gorev": "bolme-okuma", "istem_sha": Y.P._sha(ISTEM)})


def rapor() -> None:
    data = json.loads((OUT / "gecisler.json").read_text(encoding="utf-8"))
    oku_ = json.loads((OUT / "okuma.json").read_text(encoding="utf-8"))
    conn = sqlite3.connect(f"file:{GENEL_DB}?mode=ro", uri=True)
    by = {g["gecis"]: g for g in oku_["gecisler"]}
    bad = 0

    def check(sid: str, quote: str) -> str:
        nonlocal bad
        row = conn.execute("SELECT text FROM sentences WHERE id = ?", (sid,)).fetchone()
        if not row:
            bad += 1
            return " ✗ kimlik yok"
        hay = " ".join(search_words(row[0]))
        parts = [" ".join(search_words(p)) for p in quote.split("…") if search_words(p)]
        if all(p in hay for p in parts):
            return ""
        bad += 1
        return " ✗ alıntı cümlede yok"

    L = ["# Bakara 1–33: İşârât'ın âyet geçişleri", "",
         "`sinir`: ayrı birim; `birlikte`: aynı birim. Bağ kalıbı: sonraki âyet الذين، الذي، ف…، ثم… ile başlıyor. "
         "Müfessir: o geçişte sınır koyanlar (Râzî, Suyûtî ed-Dürr, İbn Kesîr, Zemahşerî, Ebüssuûd, Bursevî). "
         "Müellifin sözü ve bağın adı model okumasıdır (Opus), alıntılar programla denetlendi.", "",
         "| Geçiş | İşârât | İlk kelimeler | Bağ kalıbı | Kelime | Müfessir sınırı | Bağ | 2. âyet tek başına |",
         "|---|---|---|---|---|---|---|---|"]
    for r in data["gecisler"]:
        g = by.get(r["gecis"], {})
        isarat = r["isarat"] + (" (iç)" if r["ic_sinir"] else "")
        L.append(f"| {r['gecis']} | {isarat} | {r['ilk_kelimeler']} | {'✓' if r['bag_kalibi'] else ''} | "
                 f"{r['kelime'][0]}/{r['kelime'][1]} | {len(r['mufessir_sinir'])}/{len(MUFESSIR)} | "
                 f"{g.get('bag', '')} | {g.get('ikinci_tek_basina', '')} |")
    L += ["", "## Geçiş geçiş müellifin sözü", ""]
    for r in data["gecisler"]:
        g = by.get(r["gecis"], {})
        L.append(f"### {r['gecis']} ({r['isarat']}; {r['birim_once']} → {r['birim_sonra']})")
        for s in g.get("soz", []):
            L.append(f"> {s.get('alinti', '')}  \n`{s.get('id', '')}`{check(s.get('id', ''), s.get('alinti', ''))}")
        L += [f"- Bağ: {g.get('bag', '')}", f"- İkinci âyet tek başına: {g.get('ikinci_tek_basina', '')}: {g.get('gerekce', '')}",
              f"- Garaz: {g.get('garaz', '')}", ""]
    L += ["## Aday kurallar (model önerisi, onay bekliyor)", ""]
    for i, k in enumerate(oku_.get("aday_kurallar", []), 1):
        L += [f"{i}. **{k.get('kural', '')}**", f"   - Açıkladığı: {', '.join(k.get('aciklar', []))}",
              f"   - İstisna: {', '.join(k.get('istisna', [])) or 'yok'}"] + ([f"   - Not: {k['not']}"] if k.get("not") else [])
    L += ["", "## Genel not", "", oku_.get("genel_not", ""), "", f"Alıntı denetimi: {bad} sorun."]
    (OUT / "gecisler.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"{(OUT / 'gecisler.md').relative_to(ROOT)}; alıntı sorunu {bad}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("tablo")
    p = sub.add_parser("oku")
    p.add_argument("--yeniden", action="store_true")
    sub.add_parser("rapor")
    a = ap.parse_args()
    if a.cmd == "tablo":
        tablo()
    elif a.cmd == "oku":
        oku(a.yeniden)
    else:
        rapor()


if __name__ == "__main__":
    main()
