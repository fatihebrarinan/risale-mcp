"""D5.0 (4) birim bölümlemesi: İşârât âyetleri neden birleştiriyor, neden ayırıyor (PLANLAR.md D5; kullanıcının
kararı, 2026-11-19: önce İşârât'ın mantığı, sonra bütün Kur'ân).

    uv run python scripts/d1-bolme.py tablo     # Bakara 1–33'ün 32 geçişi, mekanik özellikler: data/d1/bolme/gecisler.json
    uv run python scripts/d1-bolme.py oku       # her geçişte müellifin sözü (tek model çağrısı): okuma.json
    uv run python scripts/d1-bolme.py rapor     # gecisler.md: tablo, müellifin sözü, alıntı denetimi
    uv run python scripts/d1-bolme.py sina      # kuralın işlenebilirlik sınaması (Bakara 1–33, İşârât görülmeden)
    uv run python scripts/d1-bolme.py bol       # b4 ile Bakara 34–286: bakara/bolme.md (üç koşu, çoğunluk, inceleme listesi)

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


# ---------------------------------------------------------------- işlenebilirlik sınaması (b1)

KURAL_DOC = ROOT / "docs" / "d1" / "bolme-kurali.md"
SINA_ISTEM = """Kur'ân âyetlerini tahlil birimlerine böleceksin: her birim, nazmı birlikte tahlil edilecek âyet ya da
âyetlerdir (bir tefsirde tek başlık altında işlenecek kısım). {talimat}

Bölünecek kısım: {sura_name} {a}–{b}. Her âyet ya kendinden önceki birime katılır ya da yeni birim başlatır. Her
geçiş (k|k+1) için kararını ve bir cümle gerekçeni yaz{kural_no}.

Cevabın yalnız şu JSON:
```json
{{"birimler": [[1, 1], [2, 3]], "gecisler": [{{"gecis": "1|2", "karar": "sinir|birlikte", {kural_alan}"gerekce": "..."}}]}}
```

# Âyetler

{ayetler}
{kural}"""
TALIMAT = {
    "kural": "Aşağıdaki kurala göre böl; kural bir müfessirin (Bediüzzaman, İşârâtü'l-İ'câz) usulünden çıkarıldı.",
    "yalin": "Bediüzzaman'ın İşârâtü'l-İ'câz'daki usulüyle böl: o eserde âyetler bazen tek tek, bazen gruplar hâlinde "
             "tahlil edilir.",
}


def kural_text() -> str:
    raw = KURAL_DOC.read_text(encoding="utf-8")
    return raw.split("\n---- KURAL ----\n", 1)[1].split("\n---- DAYANAK ----\n", 1)[0].strip()


def sina_prompt(kol: str, a: int = 1, b: int = LAST) -> str:
    q = json.loads(QURAN.read_text(encoding="utf-8"))
    rows = [x for x in q["suras"][1]["ayahs"] if a <= x["ayah"] <= b]
    vakif = next(k for k in rows[0]["translations"] if "vakf" in k.lower() or "tdv" in k.lower())
    ayetler = "\n\n".join(f"{x['ayah']}. {x['text']}\nMeâl (Diyanet Vakfı): {x['translations'][vakif]}" for x in rows)
    kural = kol == "kural"
    return SINA_ISTEM.format(talimat=TALIMAT[kol], sura_name="Bakara", a=a, b=b, ayetler=ayetler,
                             kural_no=" (hangi kurala dayandığıyla: asıl ölçüt ya da 1–6)" if kural else "",
                             kural_alan='"kural": "…", ' if kural else "",
                             kural=f"\n# Kural\n\n{kural_text()}\n" if kural else "")


def sina(kollar: list[str], kez: int, again: bool = False) -> None:
    from concurrent.futures import ThreadPoolExecutor
    jobs = []
    for kol in kollar:
        prompt = sina_prompt(kol)
        (OUT / f"sina-{kol}-istem.md").write_text(prompt, encoding="utf-8")
        for i in range(1, kez + 1):
            stem = OUT / f"sina-{kol}-{i}"
            if stem.with_suffix(".json").exists() and not again:
                continue
            jobs.append((prompt, stem, {"gorev": "bolme-sina", "kol": kol, "istem_sha": Y.P._sha(prompt),
                                        "kural_sha": Y.P._sha(kural_text())}))
    with ThreadPoolExecutor(4) as ex:
        list(ex.map(lambda j: Y.run_model(j[0], "opus", j[1], j[2]), jobs))
    sina_rapor()


def sina_rapor() -> None:
    data = json.loads((OUT / "gecisler.json").read_text(encoding="utf-8"))
    truth = {r["gecis"]: r["isarat"] for r in data["gecisler"]}
    L = ["# Bölme kuralının işlenebilirlik sınaması (b1)", "",
         "İşârât'ın bölmesini görmeyen model Bakara 1–33'ü böler. `kural`: `docs/d1/bolme-kurali.md`'nin Kural kısmıyla; "
         "`yalin`: yalnız \"İşârât'ın usulüyle böl\". Ölçü İşârât'ın 21 sınırı (18|19 İşârât'ta birlikte sayılır). "
         "Kural Bakara 1–33'ten çıktığı için bu genelleme değil, kuralın yazıldığı gibi uygulanabilirliği sınamasıdır.", "",
         "| Koşu | Tutan sınır | Fazla sınır (İşârât birleştiriyor) | Kaçan sınır (İşârât ayırıyor) | Birim |", "|---|---|---|---|---|"]
    runs = sorted(OUT.glob("sina-*-[0-9].json"))
    detail = []
    for f in runs:
        d = json.loads(f.read_text(encoding="utf-8"))
        got = {}
        for a, b in d.get("birimler", []):
            for k in range(a, b):
                got[f"{k}|{k + 1}"] = "birlikte"
            if b < LAST:
                got[f"{b}|{b + 1}"] = "sinir"
        fazla = [g for g, v in truth.items() if v == "birlikte" and got.get(g) == "sinir"]
        kacan = [g for g, v in truth.items() if v == "sinir" and got.get(g) == "birlikte"]
        n_sinir = sum(v == "sinir" for v in truth.values())
        L.append(f"| {f.stem} | {n_sinir - len(kacan)}/{n_sinir} | {', '.join(fazla) or '—'} | {', '.join(kacan) or '—'} | "
                 f"{len(d.get('birimler', []))} |")
        gerekce = {g.get("gecis"): g for g in d.get("gecisler", [])}
        for g in fazla + kacan:
            x = gerekce.get(g, {})
            detail.append(f"- **{f.stem} {g}** (İşârât: {truth[g]}; model: {x.get('karar', '?')}"
                          + (f", kural {x['kural']}" if x.get("kural") else "") + f"): {x.get('gerekce', '')}")
    L += ["", "## Ayrılan geçişlerde modelin gerekçesi", ""] + detail
    (OUT / "sina.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"{(OUT / 'sina.md').relative_to(ROOT)}")
    print("\n".join(L[5:5 + len(runs) + 1]))


# ---------------------------------------------------------------- uygulama: Bakara 34–286 (b4)

BOL_ISTEM = """Kur'ân âyetlerini tahlil birimlerine böleceksin: her birim, nazmı birlikte tahlil edilecek âyet ya da
âyetlerdir (bir tefsirde tek başlık altında işlenecek kısım). Aşağıdaki kurala göre böl; kural Bediüzzaman'ın
İşârâtü'l-İ'câz'ından (Bakara 1–33) çıkarıldı ve orada İşârât'ın bölmesini aynen verir. Dayanak ve İşârât'ın Bakara
1–33 bölmesi örnek içindir.

Bölünecek kısım: {sura_name} {a}–{b}. {baglam_notu}Her geçiş (k|k+1) için kararını, dayandığın kuralı (asıl ölçüt ya da
1–6), bir cümle gerekçeni ve ne kadar emin olduğunu yaz. Geçişler {ilk}'den {son}'a kadar, hepsi.

Cevabın yalnız şu JSON:
```json
{{"gecisler": [{{"gecis": "{ilk}", "karar": "sinir|birlikte", "kural": "…", "emin": "yuksek|orta|dusuk", "gerekce": "..."}}]}}
```

# Âyetler

{ayetler}

# Kural

{kural}

# Dayanak (İşârât'tan, Bakara 1–33)

{dayanak}

İşârât'ın Bakara 1–33 birimleri: {isarat_birimler}
"""
BOL_PARCA = 50
BOL_BAGLAM = 3


def dayanak_text() -> str:
    raw = KURAL_DOC.read_text(encoding="utf-8")
    return raw.split("\n---- DAYANAK ----\n", 1)[1].split("\n## Bilinen sınırlar", 1)[0].strip()


def parcalar(a: int, b: int) -> list[tuple[int, int]]:
    out, x = [], a
    while x <= b:
        y = min(x + BOL_PARCA - 1, b)
        if b - y < 15:                     # kısa artığı son parçaya kat
            y = b
        out.append((x, y))
        x = y + 1
    return out


def bol_prompt(a: int, b: int) -> str:
    q = json.loads(QURAN.read_text(encoding="utf-8"))
    rows = {x["ayah"]: x for x in q["suras"][1]["ayahs"]}
    ctx = range(max(1, a - BOL_BAGLAM), a)
    L = []
    for k in list(ctx) + list(range(a, b + 1)):
        x = rows[k]
        tag = " (bağlam: önceki kısım)" if k < a else ""
        L.append(f"{k}.{tag} {x['text']}\nMeâl (Diyanet Vakfı): {x['translations']['diyanet-vakfi']}")
    data = json.loads((OUT / "gecisler.json").read_text(encoding="utf-8"))
    birim = " | ".join(f"{u['ayahs'][0]}" + (f"–{u['ayahs'][1]}" if u['ayahs'][1] != u['ayahs'][0] else "")
                       for u in data["birimler"])
    return BOL_ISTEM.format(sura_name="Bakara", a=a, b=b, ilk=f"{a - 1}|{a}", son=f"{b - 1}|{b}",
                            baglam_notu=(f"{ctx.start}–{a - 1}. âyetler yalnız bağlamdır; {a - 1}|{a} geçişine de karar ver. "
                                         if a > 1 else ""),
                            ayetler="\n\n".join(L), kural=kural_text(), dayanak=dayanak_text(),
                            isarat_birimler=birim.replace("17–18 | 19–20", "17–20 (içinde 17–18 ve 19–20)"))


def bol(a: int, b: int, kez: int, again: bool = False) -> None:
    from concurrent.futures import ThreadPoolExecutor
    d = OUT / "bakara"
    d.mkdir(parents=True, exist_ok=True)
    jobs = []
    for x, y in parcalar(a, b):
        prompt = bol_prompt(x, y)
        (d / f"istem-{x}-{y}.md").write_text(prompt, encoding="utf-8")
        for i in range(1, kez + 1):
            stem = d / f"bol-{x}-{y}-{i}"
            if stem.with_suffix(".json").exists() and not again:
                continue
            jobs.append((prompt, stem, {"gorev": "bolme", "aralik": [x, y], "kez": i, "kural_sha": Y.P._sha(kural_text())}))
    print(f"{len(jobs)} çağrı")
    with ThreadPoolExecutor(4) as ex:
        list(ex.map(lambda j: Y.run_model(j[0], "opus", j[1], j[2]), jobs))
    bol_rapor(a, b)


def bol_rapor(a: int, b: int) -> None:
    from collections import Counter
    d = OUT / "bakara"
    votes: dict[str, list[dict]] = {}
    for f in sorted(d.glob("bol-*-[0-9].json")):
        for g in json.loads(f.read_text(encoding="utf-8")).get("gecisler", []):
            votes.setdefault(g.get("gecis"), []).append(g)
    mf = {w: boundaries(w) for w in ("razi", "durr", "ibnkesir")}
    rows, sinir = [], set()
    for k in range(a - 1, b):
        key = f"{k}|{k + 1}"
        vs = votes.get(key, [])
        c = Counter(v.get("karar") for v in vs)
        karar = c.most_common(1)[0][0] if vs else "?"
        if karar == "sinir":
            sinir.add(k)
        oy = f"{c.get('sinir', 0)}/{len(vs)}"
        dusuk = sum(v.get("emin") == "dusuk" for v in vs)
        muf = [w for w in mf if k in mf[w]]
        rows.append({"gecis": key, "karar": karar, "oy": oy, "oybirligi": len(c) == 1, "dusuk": dusuk,
                     "razi": k in mf["razi"], "mufessir": muf,
                     "kural": Counter(v.get("kural", "") for v in vs).most_common(1)[0][0] if vs else "",
                     "gerekce": [v.get("gerekce", "") for v in vs]})
    units, x = [], a
    for k in range(a, b + 1):
        if k in sinir or k == b:
            units.append((x, k))
            x = k + 1
    sizes = [y - x + 1 for x, y in units]
    ayri = [r for r in rows if not r["oybirligi"]]
    razi_fark = [r for r in rows if (r["karar"] == "sinir") != r["razi"]]
    out = {"aralik": [a, b], "birimler": units, "gecisler": rows}
    (d / "bolme.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    L = [f"# Bakara {a}–{b}: b4 ile bölme", "",
         f"Her geçiş üç koşunun çoğunluğuyla. Birim {len(units)}; tek âyetli {sum(s == 1 for s in sizes)}; en büyük "
         f"{max(sizes)} âyet. Oybirliği olmayan geçiş {len(ayri)}; Râzî'nin bölmesiyle ayrılan {len(razi_fark)}.", "",
         "## Birimler", "", ", ".join(f"{x}" + (f"–{y}" if y != x else "") for x, y in units), "",
         "## İnceleme listesi: koşuların ayrıldığı geçişler", "",
         "| Geçiş | Karar | Sınır oyu | Râzî sınır | Müfessir sınırı | Kural | Gerekçeler |", "|---|---|---|---|---|---|---|"]
    for r in ayri:
        L.append(f"| {r['gecis']} | {r['karar']} | {r['oy']} | {'✓' if r['razi'] else ''} | {', '.join(r['mufessir'])} | "
                 f"{r['kural']} | {' / '.join(r['gerekce'])} |")
    L += ["", "## Râzî'den ayrılan oybirlikli kararlar", "",
          "| Geçiş | Karar | Râzî | Müfessir sınırı | Kural | Gerekçe |", "|---|---|---|---|---|---|"]
    for r in razi_fark:
        if r["oybirligi"]:
            L.append(f"| {r['gecis']} | {r['karar']} | {'sınır' if r['razi'] else 'birlikte'} | {', '.join(r['mufessir'])} | "
                     f"{r['kural']} | {r['gerekce'][0] if r['gerekce'] else ''} |")
    (d / "bolme.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"{(d / 'bolme.md').relative_to(ROOT)}: birim {len(units)}, tek âyetli {sum(s == 1 for s in sizes)}, "
          f"oybirliği olmayan {len(ayri)}, Râzî'den ayrılan {len(razi_fark)}")


# ---------------------------------------------------------------- inceleme sayfası (kullanıcının kararları için)

INCELEME_HTML = """<!doctype html><html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Bakara bölmesi: inceleme</title>
<style>
:root { --bg:#fbfaf7; --fg:#222; --muted:#666; --line:#ddd; --card:#fff; --accent:#2f6f4f; }
@media (prefers-color-scheme: dark) { :root { --bg:#161616; --fg:#e8e6e1; --muted:#9a968e; --line:#333; --card:#1e1e1e; --accent:#7fc4a0; } }
body { background:var(--bg); color:var(--fg); font:16px/1.55 system-ui, sans-serif; margin:0; }
header { position:sticky; top:0; background:var(--bg); border-bottom:1px solid var(--line); padding:8px 16px; display:flex; gap:12px; align-items:center; flex-wrap:wrap; }
main { max-width:980px; margin:0 auto; padding:16px; }
.card { background:var(--card); border:1px solid var(--line); border-radius:8px; padding:14px 16px; margin:14px 0; }
.card.done { border-color:var(--accent); }
.ayet { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
@media (max-width:760px) { .ayet { grid-template-columns:1fr; } }
.ar { font-family:'Amiri','Scheherazade New',serif; font-size:1.3rem; direction:rtl; line-height:2; }
.small { font-size:.88rem; } .muted { color:var(--muted); }
.box { border-left:3px solid var(--line); padding:4px 10px; margin:8px 0; }
label { margin-right:14px; white-space:nowrap; } textarea { width:100%; min-height:44px; box-sizing:border-box; }
button { padding:6px 12px; }
</style></head><body>
<header><b>Bakara 34–286: koşuların ayrıldığı geçişler</b><span class="small muted" id="sub"></span>
<span style="flex:1"></span><span class="small" id="progress"></span><button id="export">Dışa aktar</button></header>
<main><p class="small">Kural b5 (<code>docs/d1/bolme-kurali.md</code>). Her geçişte soru: <b>iki âyet aynı birimde mi
(birlikte), ayrı birimde mi (sınır)?</b> Ölçüt: iki âyet tek bir maksadın parçalarıysa (cevap, red, açıklama, aynı
sahne, aynı fiilin devamı) birlikte; ayrı maksatlar ve yalnız garazda münasebet varsa sınır. Kararınız kuralın bir
eksiğini gösteriyorsa notta yazın.</p><div id="cards"></div></main>
<script>
const DATA = {data};
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const KEY = 'd1-bolme-bakara';
const load = () => { try { return JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { return {}; } };
let marks = load();
const save = () => { try { localStorage.setItem(KEY, JSON.stringify(marks)); } catch (e) {} progress(); };
const KARAR = [['birlikte','Birlikte (aynı birim)'],['sinir','Sınır (ayrı birim)'],['emin_degilim','Emin değilim']];
function card(g, i) {
  const m = marks[g.gecis] || {};
  const radios = KARAR.map(([v,l]) => `<label><input type="radio" name="k${i}" value="${v}" data-g="${g.gecis}"${m.karar===v?' checked':''}> ${l}</label>`).join('');
  const ay = a => `<div><div class="small muted">${a.n}. âyet</div><div class="ar">${esc(a.ar)}</div><div class="small">${esc(a.meal)}</div></div>`;
  return `<div class="card${m.karar?' done':''}"><h3>${i+1}. ${esc(g.gecis)}</h3>
    <div class="ayet">${ay(g.a)}${ay(g.b)}</div>
    <div class="box small"><b>Bugünkü bölme:</b> ${esc(g.birimler)} · <b>Koşuların oyu:</b> ${esc(g.oy)} sınır (çoğunluk: ${g.karar==='sinir'?'sınır':'birlikte'})
      · <b>Râzî:</b> ${g.razi?'sınır':'birlikte'} · <b>Sınır koyan müfessirler:</b> ${esc(g.mufessir.join(', ')||'yok')}</div>
    <details class="small"><summary>Modelin gerekçeleri (${g.gerekce.length})</summary>${g.gerekce.map(x=>`<div class="box">${esc(x)}</div>`).join('')}</details>
    <div style="margin-top:8px">${radios}</div>
    <textarea data-n="${g.gecis}" placeholder="Not (isteğe bağlı)">${esc(m.not||'')}</textarea></div>`;
}
function render() { document.getElementById('cards').innerHTML = DATA.gecisler.map(card).join(''); progress(); }
function progress() { const n = DATA.gecisler.filter(g => (marks[g.gecis]||{}).karar).length;
  document.getElementById('progress').textContent = `İşaretlenen: ${n}/${DATA.gecisler.length}`; }
document.addEventListener('change', e => { const t = e.target;
  if (t.dataset.g) { marks[t.dataset.g] = Object.assign({}, marks[t.dataset.g], {karar: t.value, at: new Date().toISOString()}); save(); t.closest('.card').classList.add('done'); }
  if (t.dataset.n) { marks[t.dataset.n] = Object.assign({}, marks[t.dataset.n], {not: t.value}); save(); } });
document.getElementById('export').onclick = () => {
  const blob = new Blob([JSON.stringify({kind:'d1-bolme-inceleme', kural: DATA.kural, exported: new Date().toISOString(), kararlar: marks}, null, 1)], {type:'application/json'});
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'd1-bolme-bakara.json'; a.click(); };
document.getElementById('sub').textContent = `${DATA.gecisler.length} geçiş`;
render();
</script></body></html>"""


def inceleme() -> Path:
    """Koşuların ayrıldığı geçişler için kullanıcının karar sayfası: `data/d1/masa/bolme-bakara.html`."""
    d = json.loads((OUT / "bakara" / "bolme.json").read_text(encoding="utf-8"))
    q = json.loads(QURAN.read_text(encoding="utf-8"))
    ay = {x["ayah"]: x for x in q["suras"][1]["ayahs"]}
    units = [tuple(u) for u in d["birimler"]]
    def unit_of(k):
        return next(u for u in units if u[0] <= k <= u[1])
    fmt = lambda u: f"{u[0]}" + (f"–{u[1]}" if u[1] != u[0] else "")
    rows = []
    for g in d["gecisler"]:
        if g["oybirligi"]:
            continue
        k = int(g["gecis"].split("|")[0])
        ua, ub = unit_of(k), unit_of(k + 1)
        rows.append({"gecis": g["gecis"], "karar": g["karar"], "oy": g["oy"], "razi": g["razi"], "mufessir": g["mufessir"],
                     "gerekce": g["gerekce"], "birimler": fmt(ua) if ua == ub else f"{fmt(ua)} | {fmt(ub)}",
                     "a": {"n": k, "ar": ay[k]["text"], "meal": ay[k]["translations"]["diyanet-vakfi"]},
                     "b": {"n": k + 1, "ar": ay[k + 1]["text"], "meal": ay[k + 1]["translations"]["diyanet-vakfi"]}})
    blob = json.dumps({"gecisler": rows, "kural": "b5"}, ensure_ascii=False).replace("</", "<\\/")
    out = ROOT / "data" / "d1" / "masa" / "bolme-bakara.html"
    out.write_text(INCELEME_HTML.replace("{data}", blob), encoding="utf-8")
    print(f"{out.relative_to(ROOT)}: {len(rows)} geçiş")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("tablo")
    p = sub.add_parser("oku")
    p.add_argument("--yeniden", action="store_true")
    sub.add_parser("rapor")
    p = sub.add_parser("sina", help="işlenebilirlik sınaması: Bakara 1–33'ü İşârât'ı görmeden böl")
    p.add_argument("--kollar", nargs="+", default=["kural", "yalin"], choices=list(TALIMAT))
    p.add_argument("--kez", type=int, default=2)
    p.add_argument("--yeniden", action="store_true")
    sub.add_parser("sina-rapor")
    p = sub.add_parser("bol", help="b4 ile Bakara'yı böl (parça parça, üç koşu, çoğunluk)")
    p.add_argument("--aralik", nargs=2, type=int, default=[34, 286])
    p.add_argument("--kez", type=int, default=3)
    p.add_argument("--yeniden", action="store_true")
    sub.add_parser("inceleme", help="koşuların ayrıldığı geçişler için karar sayfası (data/d1/masa/bolme-bakara.html)")
    p = sub.add_parser("bol-rapor")
    p.add_argument("--aralik", nargs=2, type=int, default=[34, 286])
    a = ap.parse_args()
    if a.cmd == "tablo":
        tablo()
    elif a.cmd == "oku":
        oku(a.yeniden)
    elif a.cmd == "sina":
        sina(a.kollar, a.kez, a.yeniden)
    elif a.cmd == "sina-rapor":
        sina_rapor()
    elif a.cmd == "bol":
        bol(*a.aralik, a.kez, a.yeniden)
    elif a.cmd == "inceleme":
        inceleme()
    elif a.cmd == "bol-rapor":
        bol_rapor(*a.aralik)
    else:
        rapor()


if __name__ == "__main__":
    main()
