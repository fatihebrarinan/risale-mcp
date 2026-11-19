"""D11 üretim hattı (PLANLAR.md D11): birim başına tek, kısa, ucuz taslak; Arapça, tercüme ve izah.

    uv run python scripts/d1-hat.py dosya 31-33            # kaynak dosyası: data/interim/d1-prova/<birim>/dosya.md
    uv run python scripts/d1-hat.py hazirla 31-33          # kısa istem + dosya, sızıntı testi (istem-hat-h1.md)
    uv run python scripts/d1-hat.py yazdir 31-33 [--model claude-opus-5-5]   # taslak (d1-prova.yazdir, istem "hat")
    uv run python scripts/d1-hat.py izah 31-33 --taslak 7  # günümüz Türkçesiyle izah, paragraf paragraf
    uv run python scripts/d1-hat.py bolum 31-33 --taslak 7 3   # bölüm bölüm eleştiri (eleştirmen v1.2'nin soruları)
    uv run python scripts/d1-hat.py orneklem 31-33 --taslak 3 7  # D11.3 süzgeci: iki biçimden eşit, sabit tohumlu
    uv run python scripts/d1-hat.py oran                   # İşârât'ın Bakara birimlerinde âyet kelimesi başına harf
(pilotun raporu elle yazıldı: provalar/<birim>/d11-rapor.md)

Kararlar (kullanıcıyla, 2026-11-15):
- **Kaynak dosyası** programla toplanır (âyet masasının fonksiyonlarıyla): altı taslağın hepsinin okuduğu müfessirlerin
  birimleri tam (`DOSYA_TEFSIR`), İşârât'ın önceki birimi (D5'te İşârât'ın kendisi ya da önceki taslak), Risale'de
  âyetin geçtiği yerler bir cümle bağlamla (yalnız âyetten ibaret dua ve hatime cümleleri sayıyla), klasik eserlerde
  âyetten üç kelimelik dizinin geçtiği yerler. Araçla arama kısıtlanmaz; model eksik gördüğünü okur.
- **Uzunluk:** Arapçada İşârât'ın 1–2 katı. Hedef birimde İşârât'ın Arapça uzunluğundan; D5'te İşârât olmadığı için
  `uzunluk_orani` (Bakara 8–33'te âyetin kelimesi başına İşârât'ın harfi) raporda karşılaştırılır.
- **İzah** ayrı adımda: yalnız paragrafın Arapçası ve tercümesi; taslağın söylemediğini söylemez, [n] ve tırnak eklemez.
- **Bölüm eleştirisi:** eleştirmen v1.2'nin istemi aynen, yalnız "# Taslak" kısmında bir bölüm ve D7 ile D9.1'in o
  bölüme düşen bulguları; bölümler ayrı çağrı, sonuçlar tek dosyada birleşir.
"""

import argparse
import importlib.util
import json
import re
import sqlite3
import statistics
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

from risale_mcp.normalize import match_words
from risale_mcp.paths import ROOT


def _load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M = _load("d1_masa", "d1-masa.py")          # Y (d1-yz) ve P (d1-prova) onun içinde
Y = M.Y
P = Y.P
E = _load("d1_elestiri", "d1-elestiri.py")

HAT_PROMPT = ROOT / "docs" / "d1" / "hat-istemi.md"
IZAH_PROMPT = ROOT / "docs" / "d1" / "izah-istemi.md"
SURUM = "h9"          # (sürüm karşılaştırmaları dizedir: "h10" < "h3"; h10 yalnız `hazirla --tarama` ile) istem dosyası yalnız son sürümü taşır; eski sürümlerin kopyası data/interim/d1-prova/<birim>/istem-hat-<sürüm>.md
# D13 (me'haz): dosyada tam metniyle yalnız Zemahşerî (nazmın i'câzı); öbür müfessirler yalnız araçla (kullanıcının kararı)
DOSYA_TEFSIR_H3 = ("kessaf",)
# D14.1 (h4; kullanıcının kararı, 2026-11-17): Zemahşerî de dosyadan çıkar, tefsirlerin başında araçla
DOSYA_TEFSIR_H4: tuple[str, ...] = ()
# D13: Risale-i Nur'un konuya dair yerleri (kullanıcı: "sonuçların yarısı falan"): konu başına ilk 100, üst yarısı
KONU_ILK, KONU_AL = 100, 50
PARA_PENCERE = 6       # uzun paragrafta bulunan cümlelerin iki yanından alınan cümle sayısı
RISALE_DISI_GRUP = ("osmanlica", "hizb")   # Osmanlıca Türkçeyi tekrar eder; Hizbler dua metnidir
# D14.2 (h5): ders adayı: bir konunun iki sorgusunun ilk 100 sonucunda en az bu kadar isabet alan bölüm (ilk eşik)
ADAY_ESIK = 12
ADAY_KOPYA = 0.5       # bu orandan çok cümlesi daha güçlü bir adayla aynı olan bölüm onun kopyasıdır (Tarihçe'deki Hutbe)
# D14.3 (h6): ders adayının isabeti en az bu kadar olan lafızlar için program üçüncü vecihte ders başlığı açar
ZORUNLU_ESIK = 25
RISALE_ILK: int | None = 10        # dosyada konu başına gösterilen Risale paragrafı (h9, D14.6b; None: ilk 100'ün üst yarısı)
# h2'ye kadar: altı taslağın hepsinin okuduğu müfessirler (D8, 31–33); öbürleri araçla
DOSYA_TEFSIR = ("kessaf", "beyzavi", "ebussuud", "alusi")
# usul özetinden kısa isteme giren bölümler: "Bir âyette izlenen sıra" ve "Mukaddime ne zaman gelir"
OZET_BOLUM = ("## 4. Bir âyette izlenen sıra", "## 5. Mukaddime ve meseleler ne zaman gelir")
# D13 (h3): Muhâkemât (usul 2.7) yazara da gider
OZET_MUHAKEMAT = ("### 2.7 Aslı: Muhâkemât'ın \"Unsur-u Belâğat\"ı", "## 3. İlkeler")


def out_dir(unit: str) -> Path:
    return P.OUT / unit


# ---------------------------------------------------------------- uzunluk

def uzunluk_orani() -> dict:
    """İşârât'ın Bakara birimlerinde âyetin kelimesi başına Arapça harf (8. âyetten sonra: sabit düzen)."""
    conn = sqlite3.connect(f"file:{P.GENEL_DB}?mode=ro", uri=True)
    rows = []
    for (nid,) in conn.execute("SELECT id FROM nodes WHERE parent_id = 'isaratul-icaz-arabi/sure-i-bakara' ORDER BY ord"):
        m = re.match(r"(\d+)(?:-(\d+))?", nid.rsplit("/", 1)[1])
        a, b = int(m.group(1)), int(m.group(2) or m.group(1))
        chars = conn.execute("SELECT sum(length(text)) FROM sentences WHERE node_id = ? OR node_id LIKE ?",
                             (nid, nid + "/%")).fetchone()[0] or 0
        words = sum(len(t.split()) for (t,) in conn.execute(
            "SELECT text FROM quran_ayahs WHERE sura = 2 AND ayah BETWEEN ? AND ?", (a, b)))
        rows.append({"birim": f"{a}" if a == b else f"{a}-{b}", "harf": chars, "ayet_kelime": words,
                     "oran": round(chars / words)})
    ratios = [r["oran"] for r in rows if int(r["birim"].split("-")[0]) >= 8]
    return {"birimler": rows, "medyan": round(statistics.median(ratios)), "en_az": min(ratios), "en_cok": max(ratios)}


def hedef(unit: str) -> dict:
    cfg = P.UNITS[unit]
    rows = [t for sid, t in P.hidden_sentences(cfg) if sid.startswith("isaratul-icaz-arabi/")]
    chars = sum(len(t) for t in rows)
    return {"isarat_harf": chars, "en_az": chars, "en_cok": 2 * chars,
            "kelime_az": round(chars / 5.5 / 10) * 10, "kelime_cok": round(2 * chars / 5.5 / 10) * 10}


# ---------------------------------------------------------------- kaynak dosyası

def _isarat_prev(unit: str) -> str:
    """İşârât'ın sınanan birimden önceki birimi, Arapça asıl, cümle kimlikleriyle (prova veritabanından)."""
    cfg = P.UNITS[unit]
    conn = sqlite3.connect(out_dir(unit) / "risale.db")
    # önceki birim programla (D12.5 Tur 0): Bakara'nın Arapça birimlerinden, gizlenen birimden hemen önceki kardeş
    me = P.unit_node(cfg, "isaratul-icaz-arabi")
    g = sqlite3.connect(f"file:{P.GENEL_DB}?mode=ro", uri=True)
    sibs = [r[0] for r in g.execute("SELECT id FROM nodes WHERE parent_id = 'isaratul-icaz-arabi/sure-i-bakara' "
                                    "ORDER BY ord")]
    prev = sibs[sibs.index(me) - 1]
    nodes = [r for r in conn.execute("SELECT id, ref FROM nodes WHERE id = ? OR id LIKE ? ORDER BY ord", (prev, prev + "/%"))]
    L = []
    for nid, ref in nodes:
        L.append(f"\n#### {ref}  (`{nid}`)")
        para = None
        for sid, pid, text in conn.execute("SELECT id, paragraph_id, text FROM sentences WHERE node_id = ? ORDER BY seq",
                                           (nid,)):
            if pid != para:
                L.append("")
                para = pid
            L.append(f"[{sid[len(nid) + 1:]}] {text}")
    return "\n".join(L).strip()


def _is_formula(text: str) -> bool:
    """Âyetten ibaret cümle (risalelerin sonundaki "سبحانك لا علم لنا…" gibi): Türkçe kelimesi yok denecek kadar az."""
    letters = [c for c in text if c.isalpha()]
    latin = sum(c.isascii() or c in "çğıöşüâîûÇĞİÖŞÜÂÎÛ" for c in letters)
    return latin < 25


KONU_PROMPT = """Aşağıda {sura_name} Sûresi {ayahs}. âyetler, Arapça metni ve Türkiye Diyanet Vakfı mealiyle.

Bu âyetlerin **mânâ ve ders** bakımından işlediği konuları çıkar: Risale-i Nur'da bu konuların işlendiği yerler
anlamsal aramayla bulunacak ve bu âyetler üzerine yazacak birine me'haz olarak verilecek. Kelime, harf ve i'râb
tahlili değil; imanî, ahlâkî ve ruhî ders (âyet neyi anlatıyor, neyi kötülüyor, neye çağırıyor, insanın içinde neyi
gösteriyor).

- 6–8 konu; her biri âyetin bir sözüne ya da cümlesine dayansın: `lafiz` o söz, **Arapça, âyetteki yazılışıyla
  harfi harfine** (âyetin bütününe dair konuda null); `neden` onun Türkçe açıklaması.
- Her konu için iki arama ifadesi (`sorgular`): biri günümüz Türkçesiyle, bir iki cümlelik tarif ya da soru; biri
  Risale-i Nur'un kullandığı kelimelerle (Osmanlı Türkçesi terimleriyle), yine bir iki cümle.
- Konular birbirini tekrar etmesin; geniş bir konuyu (ör. "iman") değil, bu âyetlerin söylediği yönü yaz.
- Her konunun kapsamı (`kapsam`): bir lafızdan doğuyorsa `lafiz`; âyetin bütün meâlinden ya da bir iman rükününden
  (tevhid, nübüvvet, haşir, adalet, melâike…) doğuyorsa `ayet`. Âyetin bütününe dair konu yoksa yazma.

Cevabın yalnız tek bir ```json kod bloğudur:

```json
{{"konular": [{{"konu": "kısa ad", "kapsam": "lafiz | ayet", "lafiz": "Arapça söz ya da null", "neden": "Türkçe: bu sözden neden", "sorgular": ["…", "…"]}}]}}
```

# Âyetler

{ayetler}
"""


def konular(unit: str, again: bool = False) -> list[dict]:
    """D13.2: âyetlerin mânâ ve ders konuları (yalnız âyetler ve meal; İşârât'ı ve müfessirleri görmez)."""
    cfg = P.UNITS[unit]
    stem = out_dir(unit) / "konular"
    if stem.with_suffix(".json").exists() and not again:
        return json.loads(stem.with_suffix(".json").read_text(encoding="utf-8"))["konular"]
    ayah = M.Ayah(unit)
    text = "\n\n".join(f"{v['text']} ({v['ref']})\nMeâl ({v['meal_by']}): {v['meal']}" for v in ayah.verses)
    prompt = KONU_PROMPT.format(sura_name=cfg["sura_name"], ayahs="–".join(map(str, cfg["ayahs"])), ayetler=text)
    data = Y.run_model(prompt, "opus", stem, {"gorev": "konular", "istem_sha": P._sha(KONU_PROMPT)})
    if not data or not data.get("konular"):
        sys.exit("konular çıkarılamadı")
    return data["konular"]


def risale_works(conn: sqlite3.Connection) -> set[str]:
    """D13: konuya göre aranan eserler: külliyat (Muhâkemât dahil), İşârât, Osmanlıca ve Hizbler hariç."""
    return {w for w, g, c in conn.execute("SELECT slug, group_name, collection FROM works WHERE built = 1")
            if c == "risale/kulliyat" and g not in RISALE_DISI_GRUP and not w.startswith("isaratul-icaz")}


def risale_konu(unit: str, topics: list[dict]) -> tuple[list[dict], dict]:
    """Konu başına anlamsal aramanın ilk `KONU_ILK` sonucu (iki sorgunun en iyisi), benzerliğe göre üst `KONU_AL`
    cümlesi; ve âyetin geçtiği yerler. Paragraflarıyla, kitap sırasıyla: [{node, ref, paras: [{konu, s: [(id, t)]}]}]."""
    from risale_mcp.env import load_env
    from risale_mcp.semantic import SemanticIndex
    load_env()                                     # VOYAGE_API_KEY (.env)
    conn = sqlite3.connect(f"file:{P.GENEL_DB}?mode=ro", uri=True)
    index = SemanticIndex(conn)
    works = risale_works(conn)
    hit_topics: dict[str, set] = defaultdict(set)
    hit_score: dict[tuple[str, str], float] = {}       # (cümle, konu) → benzerlik (h4: konu altında sıralama)
    stats = {}
    density: dict[str, dict[str, list]] = {}           # h5: konu → bölüm → [isabet, puan] (iki sorgunun ilk 100'ü)
    for t in topics:
        best: dict[str, float] = {}
        dens = density.setdefault(t["konu"], {})
        for q in t["sorgular"]:
            hits, _ = index.search(q, works, limit=KONU_ILK)
            for h in hits:
                best[h.sentence_id] = max(best.get(h.sentence_id, 0.0), h.score)
                d = dens.setdefault(h.node_id, [0, 0.0])
                d[0] += 1
                d[1] += h.score
        top = sorted(best, key=lambda k: -best[k])[:KONU_ILK][:KONU_AL]
        stats[t["konu"]] = {"cumle": len(top), "benzerlik": [round(best[top[0]], 3), round(best[top[-1]], 3)] if top else []}
        for sid in top:
            hit_topics[sid].add(t["konu"])
            hit_score[(sid, t["konu"])] = best[sid]
    for r in M.risale(unit):                       # âyetin geçtiği yerler (dua ve hatime cümleleri hariç)
        if not all(_is_formula(x["t"]) for x in r.get("s", []) if x["id"] == r["id"]):
            hit_topics[r["id"]].add(f"âyet {r['ayah']}")
    paras: dict[str, dict] = {}
    for sid, tops in hit_topics.items():
        row = conn.execute("SELECT paragraph_id, node_id, seq FROM sentences WHERE id = ?", (sid,)).fetchone()
        if not row:
            continue
        pid, node, seq = row
        p = paras.setdefault(pid, {"pid": pid, "node": node, "hits": set(), "konu": set(), "skor": {}})
        p["hits"].add(seq)
        p["konu"] |= tops
        for k in tops:
            p["skor"][k] = max(p["skor"].get(k, 0.0), hit_score.get((sid, k), 0.0))
    out_nodes: dict[str, dict] = {}
    for p in paras.values():
        sents = conn.execute("SELECT id, text, seq FROM sentences WHERE paragraph_id = ? ORDER BY seq", (p["pid"],)).fetchall()
        if len(sents) > 2 * PARA_PENCERE + 1:           # uzun paragraf: bulunan cümlelerin iki yanı, aralar "…"
            keep = {s for _, _, s in sents if any(abs(s - h) <= PARA_PENCERE for h in p["hits"])}
            sents = [x for x in sents if x[2] in keep]
        p["s"] = sents
        p["ord"] = sents[0][2] if sents else 0
        out_nodes.setdefault(p["node"], {"node": p["node"], "paras": []})["paras"].append(p)
    for p in paras.values():
        p["ref"] = conn.execute("SELECT ref FROM nodes WHERE id = ?", (p["node"],)).fetchone()[0]
    for n in out_nodes.values():
        n["ref"] = conn.execute("SELECT ref FROM nodes WHERE id = ?", (n["node"],)).fetchone()[0]
        n["paras"].sort(key=lambda p: p["ord"])
        n["ord"] = n["paras"][0]["ord"]
    nodes = sorted(out_nodes.values(), key=lambda n: n["ord"])
    stats["toplam"] = {"cumle_isabet": len(hit_topics), "paragraf": len(paras), "bolum": len(nodes),
                       "eser": len({n["node"].split("/")[0] for n in nodes})}
    stats["_paras"] = list(paras.values())               # h4: konu konu dizmek için (dosyaya yazılmaz)
    stats["_adaylar"] = ders_adaylari(conn, topics, density, unit)
    return nodes, stats


def ders_adaylari(conn: sqlite3.Connection, topics: list[dict], density: dict, unit: str) -> dict[str, list[dict]]:
    """D14.2 (h5): konu başına ders adayları. Birinci tetikleyici isabetlerin yoğunlaştığı bölüm (iki sorgunun ilk 100
    sonucundan en az `ADAY_ESIK` isabet), ikinci âyeti anan bölüm (dua ve hatime cümleleri hariç; `ayet` anahtarında).
    Daha güçlü bir adayla cümlelerinin `ADAY_KOPYA`'dan çoğu aynı olan bölüm kopyadır, ayrı aday sayılmaz."""
    def grams(node: str) -> set[tuple]:                # baskıdan bağımsız: normalize kelimelerin 5'li dizileri
        words = [w for (t,) in conn.execute("SELECT text FROM sentences WHERE node_id = ?", (node,))
                 for w in match_words(t)]
        return {tuple(words[i:i + 5]) for i in range(max(0, len(words) - 4))}

    def head(node: str) -> dict:
        ref, sub_ = conn.execute("SELECT ref, subtitle FROM nodes WHERE id = ?", (node,)).fetchone()
        first = conn.execute("SELECT id, text FROM sentences WHERE node_id = ? ORDER BY seq LIMIT 3", (node,)).fetchall()
        return {"ref": ref, "alt": sub_, "bas": first}

    raw = [(t["konu"], node, n, sc) for t in topics for node, (n, sc) in density.get(t["konu"], {}).items() if n >= ADAY_ESIK]
    raw.sort(key=lambda x: -x[2])
    kept: dict[str, set] = {}                          # aday bölüm → 5'li diziler (aynı bölüm iki konuda aday olabilir)
    twin_of: dict[str, str] = {}
    out: dict[str, list[dict]] = defaultdict(list)
    for konu, node, n, sc in raw:
        if node not in kept and node not in twin_of:
            g = grams(node)
            twin = next((o for o, og in kept.items() if g and len(g & og) / len(g) > ADAY_KOPYA), None)
            if twin:
                twin_of[node] = twin
            else:
                kept[node] = g
        if node in twin_of:
            continue
        out[konu].append({"node": node, "isabet": n, "puan": round(sc, 2), "tur": "yogunluk", **head(node)})
    seen = [(o, None) for o in kept]
    anan = {}
    for r in M.risale(unit):                       # ikinci tetikleyici: âyeti anan bölüm
        if all(_is_formula(x["t"]) for x in r.get("s", []) if x["id"] == r["id"]):
            continue
        node = conn.execute("SELECT node_id FROM sentences WHERE id = ?", (r["id"],)).fetchone()
        if node and not any(node[0] == o for o, _ in seen) and node[0] not in anan:
            anan[node[0]] = {"node": node[0], "isabet": None, "tur": "ayeti_anan", "ayet": r["ayah"], **head(node[0])}
    if anan:
        out["ayet"] = list(anan.values())
    return dict(out)


def _aday_lines(adaylar: list[dict]) -> list[str]:
    L = ["**Ders adayları** (Risale-i Nur'da bu konunun yoğunlaştığı bölümler; program seçti):", ""]
    for a in adaylar:
        why = f"{a['isabet']} isabet" if a["isabet"] else f"âyeti anıyor (âyet {a.get('ayet')})"
        L.append(f"- `{a['node']}`: {a['ref']}" + (f" ({a['alt']})" if a.get("alt") else "") + f"; {why}. Başı: "
                 + " ".join(f"[{i}] {t}" for i, t in a["bas"]))
    return L + [""]


def _para_text(p: dict) -> str:
    parts, prev = [], None
    for sid, text, seq in p["s"]:
        if prev is not None and seq != prev + 1:
            parts.append("…")
        parts.append(f"[{sid}] {text}")
        prev = seq
    return " ".join(parts)


def risale_by_word(topics: list[dict], paras: list[dict], adaylar: dict | None = None) -> list[str]:
    """h4 (D14.1): Risale-i Nur'un yerleri âyetin sözüne göre: söz → konu → paragraflar benzerlik sırasıyla. Bir paragraf
    en yüksek benzerlikle bulunduğu konunun altında bir kez durur; öbür konuları yanında yazılır. Âyetin kendisinin geçtiği
    yerler ayrı alt bölümde."""
    L = []
    home: dict[str, list] = defaultdict(list)
    ayet = []
    for p in paras:
        if p["skor"]:
            k = max(p["skor"], key=p["skor"].get)
            home[k].append(p)
        else:
            ayet.append(p)
    for t in topics:
        ps = sorted(home.get(t["konu"], []), key=lambda p: -p["skor"][t["konu"]])
        if RISALE_ILK:
            ps = ps[:RISALE_ILK]
        L += [f"### {(t['lafiz'] + ' — ') if t.get('lafiz') else ''}{t.get('neden', '')}", "", f"Konu: **{t['konu']}**"
              + (" (âyetin bütününden)" if t.get("kapsam") == "ayet" else "") + f" ({len(ps)} yer, benzerlik sırasıyla)", ""]
        if adaylar and adaylar.get(t["konu"]):
            L += _aday_lines(adaylar[t["konu"]])
        for p in ps:
            also = sorted(k for k in p["konu"] if k != t["konu"])
            L.append(f"_{p['ref']}_ (`{p['node']}`)" + (f"; ayrıca: {', '.join(also)}" if also else ""))
            L += [_para_text(p), ""]
    if ayet or (adaylar and adaylar.get("ayet")):
        L += ["### Âyetin kendisinin geçtiği yerler", ""]
        if adaylar and adaylar.get("ayet"):
            L += _aday_lines(adaylar["ayet"])
        for p in sorted(ayet, key=lambda p: p["ord"]):
            L += [f"_{p['ref']}_ (`{p['node']}`; {', '.join(sorted(p['konu']))})", _para_text(p), ""]
    return L


def dosya(unit: str) -> Path:
    """Kaynak dosyası, h3 (D13, me'haz hiyerarşisi; kullanıcının kararları 2026-11-17): (1) İşârât'ın önceki birimi,
    (2) Risale-i Nur'un bu âyetlerin konularına dair yerleri, çok sayıda, (3) nazmın i'câzı: Zemahşerî tam ve belâgat
    eserleri, (4) klasik tefsirler dosyada yok, yalnız araçla. h2'nin dosyası (dört müfessir tam önde, Risale yalnız
    âyetin geçtiği yerler) 9–10 için `dosya-h2.md`'de durur."""
    cfg = P.UNITS[unit]
    ayah = M.Ayah(unit)
    topics = konular(unit)
    L = [f"# Kaynak dosyası: {cfg['sura_name']} {'–'.join(map(str, cfg['ayahs']))}", "",
         "Program topladı (bu birim için; senin araştırman değil). Sıra me'hazın sırasıdır: önce İşârât, sonra "
         "Risale-i Nur, sonra nazmın i'câzını gösteren eserler (" + ("belâgat eserleri; Zemahşerî tefsirlerin başında, "
         "eklentide" if SURUM >= "h4" else "Zemahşerî ve belâgat eserleri") + "); klasik tefsirler dosyada "
         "yok, eklentiyle açılır. Her cümlenin başında kimliği: `cite` ve `get_passage` bu kimliklerle çalışır, "
         "`read_section` bölümün tamamını verir.", ""]
    L += ["## Âyetler", ""]
    for v in ayah.verses:
        L += [f"> {v['text']} ({v['ref']})", f"> Meâl ({v['meal_by']}): {v['meal']}", ""]
    L += ["## 1. İşârâtü'l-İ'câz: önceki birim (Arapça asıl)", "",
          "Aynı türden öbür birimler `risale` eklentisinde (`work: \"isaratul-icaz-arabi\"`; kimlikleri Ek 2'de).", "",
          _isarat_prev(unit), ""]
    nodes, stats = risale_konu(unit, topics)
    paras = stats.pop("_paras")
    adaylar = stats.pop("_adaylar")
    (out_dir(unit) / "ders-adaylari.json").write_text(json.dumps(adaylar, ensure_ascii=False, indent=1), encoding="utf-8")
    stats["ders_adayi"] = {k: len(v) for k, v in adaylar.items()}
    try:
        pconn = sqlite3.connect(out_dir(unit) / "risale.db")
        a, b = cfg["ayahs"]
        links = pconn.execute("SELECT kind, strength, node_id, evidence_id, ayah_start, ayah_end FROM ayah_links "
                              "WHERE sura = ? AND ayah_start <= ? AND ayah_end >= ?", (cfg["sura"], b, a)).fetchall()
    except sqlite3.Error:
        links = []
    link_lines = (["Âyetle bağ kuran yerler (kural çıkardı; tür ve güç):", ""]
                  + [f"- `{n}` ({k}, {s}; kanıt `{e}`; âyet {x}–{y})" for k, s, n, e, x, y in links] + [""]) if links else []
    if SURUM >= "h4":            # D14.1: âyetin sözüne göre, benzerlik sırasıyla; Zemahşerî dosyada yok
        L += ["## 2. Risale-i Nur: âyetin sözlerine göre dersi", "",
              "Program bu âyetlerin konularını âyetin sözlerinden çıkardı ve her konu için Risale-i Nur'da anlamsal arama "
              f"yaptı (konu başına ilk {KONU_ILK} sonucun benzerliğe göre üst yarısı). Burada âyetin her sözünün altında "
              "o sözün konusu ve Risale-i Nur'da o konunun işlendiği yerler var, **en yakından başlayarak**. Âyetin bir "
              "sözünü işlerken onun dersini buradan al ve Arapça metinde kendi sözünle aç. Bir yerin devamını "
              "`read_section` ile oku."
              + (" Bir sözün altında **ders adayı** varsa: Risale-i Nur o konuyu orada yoğun işliyor; o sözü işlerken "
                 "dur ve dersi aç (usulün 3. maddesi)." if SURUM >= "h5" else ""), ""] + link_lines
        L += risale_by_word(topics, paras, adaylar if SURUM >= "h5" else None)
        L += ["## 3. Nazmın i'câzı: belâgat ve lügat eserleri", ""]
        tefsir_tam = DOSYA_TEFSIR_H4
    else:                        # h3 (D13): kitap sırasıyla; Zemahşerî dosyada tam
        L += ["## 2. Risale-i Nur: bu âyetlerin konularına dair yerler", "",
              "Program bu âyetlerin konularını çıkardı ve her konu için Risale-i Nur'da anlamsal arama yaptı (konu başına "
              f"ilk {KONU_ILK} sonucun benzerliğe göre üst yarısı); bulunan cümleler paragraflarıyla, kitap sırasıyla. "
              "Âyetin kendisinin geçtiği yerler de burada. Her paragrafın üstünde hangi konudan geldiği yazılı. Bir yerin "
              "devamını `read_section` ile oku.", "", "Konular:", ""]
        L += [f"- **{t['konu']}** ({t.get('neden', '')})" for t in topics] + [""] + link_lines
        for n in nodes:
            L += [f"### {n['ref']}  (`{n['node']}`)", ""]
            for p in n["paras"]:
                L += [f"_Konu: {', '.join(sorted(p['konu']))}_", _para_text(p), ""]
        L += ["## 3. Nazmın i'câzı: Zemahşerî ve belâgat eserleri", ""]
        tefsir_tam = DOSYA_TEFSIR_H3
    for w in M.tefsir(unit):
        if w["work"] not in tefsir_tam:
            continue
        for u in w["units"]:
            L += [f"### {w['author']}, {w['title']}: {u['ref']}  (`{u['id']}`)", ""]
            for r in u["rows"]:
                L.append(" ".join(f"[{s['id']}] {s['t']}" for s in r.get("s", [])) if r.get("s") else r.get("t", ""))
                L.append("")
    L += ["### Belâgat ve lügat eserleri: âyetten üç kelimelik bir dizinin geçtiği yerler", ""]
    for k in M.klasik(ayah):
        L += [f"#### {k['author']}, {k['title']}: {k['ref']}", ""] + [f"[{s['id']}] {s['t']}" for s in k["s"]] + [""]
    if SURUM >= "h4":
        L += ["## 4. Klasik tefsirler", "",
              "Dosyada yok; `tefsir` eklentisinde (`find_ayah` bu âyetlerdeki birimleri verir). Bakacaksan **önce "
              "Zemahşerî'nin Keşşâf'ı** (`kessaf`; nazmın i'câzında müellif onun yolunu izler), sonra gerekirse öbürleri "
              "(Beyzâvî, Ebüssuûd, Âlûsî, Râzî, Taberî, Mâtürîdî, Kurtubî, Nesefî, İbn Kesîr, Celâleyn, Süyûtî, Bursevî): "
              "ihtilafı ve yoklamayı görmek için. Akıl yürütmeyi onlara bırakma; nükteyi lafızdan ve usulden kendin kur.", ""]
    else:
        L += ["## 4. Klasik tefsirler", "",
              "Dosyada yok. Beyzâvî, Ebüssuûd, Âlûsî, Râzî, Taberî, Mâtürîdî, Kurtubî, Nesefî, İbn Kesîr, Celâleyn, Süyûtî ve "
              "Bursevî `tefsir` eklentisinde (`find_ayah` ile bu âyetlerdeki birimleri); ihtilafı ve yoklamayı görmek için "
              "gerektikçe oku.", ""]
    path = out_dir(unit) / "dosya.md"
    path.write_text("\n".join(L), encoding="utf-8")
    (out_dir(unit) / "dosya-sayilar.json").write_text(json.dumps(stats, ensure_ascii=False, indent=1), encoding="utf-8")
    sizes, cur = {}, None
    for line in L:
        if line.startswith("## "):
            cur = line[3:]
        sizes[cur] = sizes.get(cur, 0) + len(line) + 1
    print(f"{path.relative_to(ROOT)}: {path.stat().st_size // 1024} KB, {len(' '.join(L).split()):,} kelime")
    for k, v in sizes.items():
        print(f"  {v:9,} harf  {k}")
    print(json.dumps(stats, ensure_ascii=False, indent=1))
    return path


# ---------------------------------------------------------------- istem

def _section(text: str, start: str, end: str | None) -> str:
    i = text.index(start)
    j = text.index(end, i) if end else len(text)
    return text[i:j].strip()


# D14.2 (h5): usulün 3. maddesinin örnekleri: İşârât'ta bir lafızdan kalkan dersler (`data/d1/isarat-yapi`, D14.2'nin
# hazırlığı); sınanan birimden olanı alınmaz (prova kuralı)
DERS_ORNEKLERI = [("11-12-ayetlerin-tefsiri", "c024", "c028", "soru–cevap"),
                  ("13", "c027", "c030", "إشارة إلى"),
                  ("16", "c012", "c014", "إشارة إلى ve hitap"),
                  ("9-10-ayetlerin-tefsiri", "c080", "c086", "hitapla ders ve içinde soru–cevap"),
                  # D14.3: geniş ders (mesele) örneği; genişi Yirminci Söz'ün İkinci Makamı
                  ("31-33-ayetlerin-tefsiri", "mukaddime/c001", "mukaddime/c011", "mukaddime: geniş ders, taksimle")]


def zorunlu_dersler(unit: str) -> list[dict]:
    """D14.3 (h6): en güçlü adayının isabeti `ZORUNLU_ESIK`'i aşan konular: lafız ve aday bölümler (dosyanın adaylarından)."""
    adaylar = json.loads((out_dir(unit) / "ders-adaylari.json").read_text(encoding="utf-8"))
    topics = {t["konu"]: t for t in konular(unit)}
    out = []
    for konu, xs in adaylar.items():
        strong = [x for x in xs if (x.get("isabet") or 0) >= ZORUNLU_ESIK]
        if konu in topics and strong:
            t = topics[konu]
            lafiz = t.get("lafiz") or re.split(r"\s+[—–-]\s+", t.get("neden", ""), maxsplit=1)[0].strip()
            out.append({"konu": konu, "lafiz": lafiz, "kapsam": t.get("kapsam", "lafiz"), "adaylar": strong})
    return out


def ders_basliklari(unit: str) -> str:
    rows = zorunlu_dersler(unit) if SURUM >= "h6" else []
    if not rows:
        return "(Bu birim için program ders başlığı açmadı.)"
    L = []
    for r in rows:
        refs = "; ".join(f"{x['ref']} (`{x['node']}`, {x['isabet']} isabet)" for x in r["adaylar"])
        if r["kapsam"] == "ayet":                      # tek kaide: âyetin bütününden doğan ders mukaddimededir
            L.append(f"- `### Ders: {r['konu']}`: **vecihlerden önce, mukaddime olarak** (`## Mukaddime` başlığının altında); "
                     f"Risale-i Nur'da {refs}")
        else:
            L.append(f"- `### Ders: «{r['lafiz']}»`: üçüncü vecihte, o lafız işlenirken; Risale-i Nur'da {refs}")
    return "\n".join(L)


def ders_ornekleri(unit: str) -> str:
    cfg = P.UNITS[unit]
    hidden = P.unit_node(cfg, "isaratul-icaz-arabi")
    conn = sqlite3.connect(f"file:{P.GENEL_DB}?mode=ro", uri=True)
    L = ["Müellif bir lafzı işlerken nazmın nüktesinden öte bir derse ya da hakikate geçer; ders o lafzın yerinde, kısa ve "
         "lafza bağlıdır. Aşağıdakiler İşârât'ın başka birimlerinden (Arapça asıl, cümle kimlikleriyle).", ""]
    for u, a, b, how in DERS_ORNEKLERI:
        node = f"isaratul-icaz-arabi/sure-i-bakara/{u}"
        if node == hidden or hidden.startswith(node) or node.startswith(hidden):
            continue
        rows = conn.execute("SELECT id, text FROM sentences WHERE node_id = ? OR node_id LIKE ? ORDER BY seq",
                            (node, node + "/%")).fetchall()
        ids = [r[0] for r in rows]
        i, j = ids.index(f"{node}/{a}"), ids.index(f"{node}/{b}")
        ref = conn.execute("SELECT ref FROM nodes WHERE id = ?", (node,)).fetchone()[0]
        L += [f"### {ref} ({how})", ""] + [f"[{sid}] {t}" for sid, t in rows[i:j + 1]] + [""]
    return "\n".join(L).strip()


KALIP_DOC = ROOT / "docs" / "d1" / "soru-kaliplari.md"
TARAMA_PROMPT = ROOT / "docs" / "d1" / "tarama-istemi.md"   # D14.7 (h10)
TARAMA_ALANLAR = ("tarama_usul", "tarama_bolum", "tarama_adim", "tarama_denetim", "cevap", "tarama_baslik")
CEVAP_H9 = "Cevabın yalnız taslaktır; önüne ve ardına açıklama yazma."


def tarama_parcalari(unit: str | None) -> dict:
    """h10: tarama-istemi.md'nin bölümleri ve birimin tablosu; h9 (unit None): boş, cevap cümlesi h9'unki."""
    if unit is None:
        return {k: "" for k in TARAMA_ALANLAR} | {"cevap": CEVAP_H9}
    K = _load("d1_kalip", "d1-kalip.py")
    raw = TARAMA_PROMPT.read_text(encoding="utf-8")
    out = {}
    for k in TARAMA_ALANLAR:
        part = raw.split(f"---- {k} ----\n", 1)[1]
        part = part.split("\n---- ", 1)[0]
        out[k] = part.rstrip("\n") if k not in ("tarama_bolum", "tarama_baslik") else part.rstrip("\n") + "\n\n"
    out["tarama_bolum"] = out["tarama_bolum"].replace("{tablo}", K.tablo_md(unit))
    return out


def hazirla(unit: str, surum: str | None = None, tarama: bool = False) -> Path:
    surum = surum or ("h10" if tarama else SURUM)
    cfg = P.UNITS[unit]
    out = out_dir(unit)
    if not (out / "risale.db").exists():
        sys.exit("önce: uv run python scripts/d1-prova.py hazirla <birim> (prova veritabanları)")
    dosya_path = dosya(unit)
    ozet = P.apply_edits(P.OZET.read_text(encoding="utf-8"), cfg["ozet"], "özet")
    cizelge = P.apply_edits(P.CIZELGE.read_text(encoding="utf-8"), cfg["cizelge"], "çizelge")
    ek1 = _section(ozet, OZET_BOLUM[0], "## 6. Anlatım biçimi")
    if SURUM >= "h3":                                  # D13: Muhâkemât (usul 2.7) yazara da gider
        ek1 = _section(ozet, *OZET_MUHAKEMAT) + "\n\n" + ek1
    ek2 = _section(cizelge, "## Çizelge: Bakara", "## Çizelge: Fâtiha")
    h = hedef(unit)
    body = HAT_PROMPT.read_text(encoding="utf-8").split("---- İSTEM ----", 1)[1].strip()
    body = body.format(**tarama_parcalari(unit if tarama else None),sura_name=cfg["sura_name"], ayahs="–".join(map(str, cfg["ayahs"])),
                       ders_basliklari=ders_basliklari(unit),
                       en_az=f"{h['en_az']:,}".replace(",", "."), en_cok=f"{h['en_cok']:,}".replace(",", "."),
                       kelime_az=f"{h['kelime_az']:,}".replace(",", "."), kelime_cok=f"{h['kelime_cok']:,}".replace(",", "."))
    ek4 = ders_ornekleri(unit) if SURUM >= "h5" else ""
    prompt = (f"{body}\n\n---\n\n# Ek 1: Usul özeti, {'2.7 (Muhâkemât), ' if SURUM >= 'h3' else ''}4. ve 5. bölüm (prova kopyası)\n\n{ek1}\n\n---\n\n"
              f"# Ek 2: Birim çizelgesi, Bakara (prova kopyası)\n\n{ek2}\n\n---\n\n# Ek 3: "
              + dosya_path.read_text(encoding="utf-8").removeprefix("# ")
              + (f"\n\n---\n\n# Ek 4: İşârât'tan ders örnekleri\n\n{ek4}" if ek4 else "")
              + (f"\n\n---\n\n# Ek 5: İşârât'ın soru kalıpları\n\n{'## ' + KALIP_DOC.read_text(encoding='utf-8').split(chr(10) + '## ', 1)[1]}"
                 if tarama else ""))
    name, report = P.istem_files("hat", surum)
    (out / name).write_text(prompt, encoding="utf-8")
    print(f"istem: {len(prompt):,} harf (gövde {len(body):,}, Ek 1 {len(ek1):,}, Ek 2 {len(ek2):,}); hedef {h}")
    ok = P.leak_report(unit, cfg, out, prompt, report)
    print(f"sızıntı testi: {'temiz' if ok else 'SORUN'} → {(out / report).relative_to(ROOT)}")
    if not ok:
        sys.exit(1)
    return out / name


# ---------------------------------------------------------------- izah

QUOTE_RE = re.compile(r"«([^»]+)»|“([^”]+)”|\"([^\"]+)\"")


def izah(unit: str, n: int, again: bool = False) -> dict | None:
    cfg = P.UNITS[unit]
    stem = Y.out_dir(unit) / f"izah-taslak-{n}"
    if stem.with_suffix(".json").exists() and not again:
        print(f"{stem.name}: var (--yeniden)")
        return json.loads(stem.with_suffix(".json").read_text(encoding="utf-8"))
    blocks, sources = Y.draft_blocks(unit, n)
    raw = IZAH_PROMPT.read_text(encoding="utf-8").split("---- İZAH ----", 1)[1].strip()
    text = raw.format(sura_name=cfg["sura_name"], ayahs="–".join(map(str, cfg["ayahs"])),
                      taslak=Y.render_draft(blocks, {}))
    data = Y.run_model(text, "opus", stem, {"gorev": "izah", "taslak": n, "istem_sha": P._sha(raw)})
    if data is None:
        return None
    data["denetim"] = izah_check(blocks, data)
    stem.with_suffix(".json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    d = data["denetim"]
    print(f"  izah: {d['kayit']} kayıt, eksik {len(d['eksik'])}, fazla {len(d['fazla'])}, numara {len(d['numara'])}, "
          f"tırnak {len(d['tirnak'])}")
    return data


def izah_check(blocks: list, data: dict) -> dict:
    """İzahta taslakta olmayan [n] ve tırnak (paragraf çiftinde geçmeyen söz); eksik ve fazla çapalar."""
    text = {a: t for a, _, _, t in blocks}
    pr = Y.pairs(blocks)
    tr = [a for a, lang, q, _ in blocks if lang == "tr" and not q]
    got = {x.get("capa"): x.get("metin", "") for x in data.get("izah", [])}
    out = {"kayit": len(got), "eksik": [a for a in tr if a not in got], "fazla": [a for a in got if a not in text],
           "numara": [], "tirnak": []}
    for a, m in got.items():
        pair = text.get(a, "") + " " + text.get(Y.ar_of(pr, a), "")
        nums = set(re.findall(r"\[(\d+)", m)) - set(re.findall(r"\[(\d+)", pair))
        if nums:
            out["numara"].append({"capa": a, "n": sorted(nums)})
        for g in QUOTE_RE.finditer(m):
            q = next(x for x in g.groups() if x)
            if len(q.split()) >= 2 and not Y.quote_found(q, pair):
                out["tirnak"].append({"capa": a, "soz": q[:120]})
    return out


# ---------------------------------------------------------------- bölüm eleştirisi

BOLUM_NOT = """

# Bu çağrıda bakacağın bölüm: {baslik}

Taslağın tamamı yukarıda bağlam için duruyor; bu çağrıda **yalnız "{baslik}" bölümünü** eleştiriyorsun (çapaları
`{key}/…`). Aynı taslağın öbür bölümlerine ayrı çağrılar bakıyor. Bu bölümün paragraflarını **tek tek, yakından**
oku: her paragraf için yukarıdaki soruları sor; İşârât'ın bu bölüme düşen kısmıyla ve paragrafın dayandığı
kaynaklarla karşılaştır. Notlarını yalnız bu bölümün çapalarına yaz. Bir nükte bu bölümde yoksa ama taslağın başka bir
bölümünde varsa onu eksik sayma. `sistemli` ve `oneriler` alanlarına yalnız bu bölümden çıkanları yaz; `ozet` bu
bölümün özetidir. Çıktı biçimi yukarıdakinin aynısıdır."""


def _sections(unit: str, n: int) -> list[str]:
    blocks, _ = Y.draft_blocks(unit, n)
    keys = []
    for a, *_ in blocks:
        k = a.split("/")[0]
        if k != "Âyet" and k not in keys:
            keys.append(k)
    return keys


def bolum_run(unit: str, n: int, key: str, again: bool) -> dict | None:
    import os, subprocess, tempfile, time
    stem = Y.out_dir(unit) / f"bolum-elestiri-taslak-{n}-{key}"
    if stem.with_suffix(".json").exists() and not again:
        return json.loads(stem.with_suffix(".json").read_text(encoding="utf-8"))
    prompt, sha = E.critic_prompt(unit, n)
    prompt += BOLUM_NOT.format(baslik=P.SECTION_TITLES[key], key=key)
    mcp = E.critic_mcp(unit)
    env = {k: v for k, v in os.environ.items() if k not in P.PARENT_ENV}
    command = ["claude", "-p", "--model", Y.MODELS["opus"], "--effort", Y.EFFORT, "--output-format", "stream-json",
               "--verbose", "--mcp-config", str(mcp), "--strict-mcp-config", "--tools", "",
               "--allowedTools", ",".join(f"mcp__{s}" for s in E.CRITIC_SERVERS), "--no-session-persistence"]
    started = time.monotonic()
    print(f"{stem.name}: ({datetime.now():%H:%M})", flush=True)
    done = P.claude_p(command, prompt, stem.with_suffix(".jsonl"), env, Y.TIMEOUT, esik=0.85, prefix="d1-bolum-")
    answer, calls, cost = P.transcript(stem.with_suffix(".jsonl"))
    data = Y.extract_json(answer)
    meta = {"model": Y.MODELS["opus"], "effort": Y.EFFORT, "istem_sha": sha, "taslak": n, "bolum": key,
            "seconds": round(time.monotonic() - started), "returncode": done.returncode, "calls": calls,
            "cost_usd": cost, "at": datetime.now().isoformat(), "parsed": data is not None}
    stem.with_suffix(".meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    if data is None:
        stem.with_suffix(".cevap.txt").write_text(answer, encoding="utf-8")
        print(f"  {stem.name}: JSON ayrıştırılamadı (çıkış {done.returncode})", flush=True)
        return None
    stem.with_suffix(".json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  {stem.name}: {meta['seconds']} sn, {len(data.get('notlar', []))} not" + (f", ≈{cost:.2f} $" if cost else ""),
          flush=True)
    return data


def check_notes(unit: str, n: int, notes: list, log: Path) -> None:
    """`d1-elestiri.check_critic`in aynısı, döküm dosyası verilerek (bölüm çağrısının okudukları)."""
    blocks, _ = Y.draft_blocks(unit, n)
    by_anchor = {a: t for a, _, _, t in blocks}
    pr = Y.pairs(blocks)
    whole = " ".join(by_anchor.values())
    read_ids = {k[1] for k in E.Read(log=log).items}
    conns: dict = {}
    for note in notes:
        q, capa = note.get("taslak_alinti"), note.get("capa") or "genel"
        d = {}
        if q:
            pair = [by_anchor.get(capa, ""), by_anchor.get(pr.get(capa, ""), "")]
            d["alinti"] = Y.quote_found(q, " ".join(pair)) or ("baska_capada" if Y.quote_found(q, whole) else False)
        if capa != "genel":
            d["capa"] = capa in by_anchor
        bad, unread = [], []
        for sid in note.get("dayanak") or []:
            server = "risale" if sid.startswith("isaratul") else None
            if not any(E._exists(s, sid, conns) for s in ([server] if server else E.CRITIC_DBS)):
                bad.append(sid)
            elif not any(x == sid.partition("..")[0] or x.startswith(sid.partition("..")[0] + "#") for x in read_ids):
                unread.append(sid)
        d["dayanak_yok"], d["dayanak_okunmamis"] = bad, unread
        note["denetim"] = d


def bolum(unit: str, drafts: list[int], again: bool = False, parallel: int = 4) -> None:
    jobs = [(n, k) for n in drafts for k in _sections(unit, n)]
    with ThreadPoolExecutor(max_workers=parallel) as pool:
        results = list(pool.map(lambda j: (j, bolum_run(unit, j[0], j[1], again)), jobs))
    for n in drafts:
        merged = {"taslak": n, "bolumler": {}, "notlar": [], "sistemli": [], "oneriler": [], "ozet": {}}
        for (m, k), data in results:
            if m != n:
                continue
            if data is None:
                merged["bolumler"][k] = "basarisiz"
                continue
            notes = data.get("notlar", [])
            for x in notes:
                x["bolum"] = k
            check_notes(unit, n, notes, Y.out_dir(unit) / f"bolum-elestiri-taslak-{n}-{k}.jsonl")
            merged["bolumler"][k] = len(notes)
            merged["notlar"] += notes
            merged["sistemli"] += [dict(x, bolum=k) for x in data.get("sistemli", [])]
            merged["oneriler"] += [x if isinstance(x, dict) else {"metin": x, "bolum": k} for x in data.get("oneriler", [])]
            merged["ozet"][k] = data.get("ozet", "")
        (Y.out_dir(unit) / f"bolum-elestiri-taslak-{n}.json").write_text(
            json.dumps(merged, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"taslak {n}: bölüm eleştirisi {merged['bolumler']}, toplam {len(merged['notlar'])} not")


# ---------------------------------------------------------------- D11.3 süzgeç örneklemi

ORNEK_PER = 5          # taslak ve biçim başına (kullanıcının yükü: iki taslak × iki biçim × 5 = 20 not)


def orneklem(unit: str, drafts: list[int], again: bool = False) -> None:
    """Bütün ve bölüm eleştirisinden eşit, sabit tohumlu örneklem: övgü, "ehline sor" ve denetimde tutmayan hariç;
    türlere yayılarak. Kabul oranı × not sayısı, hangi biçimin daha çok geçerli not bulduğunu verir."""
    import random
    path = Y.out_dir(unit) / "d11-orneklem.json"
    if path.exists() and not again:
        print(f"{path.relative_to(ROOT)} var; korunuyor (--yeniden)")
        return
    rng = random.Random(f"d11-{unit}-orneklem")
    picked, havuz = [], {}
    for n in drafts:
        for mod, file, prefix in (("butun", f"elestiri-taslak-{n}.denetim.json", ""),
                                  ("bolum", f"bolum-elestiri-taslak-{n}.json", "b")):
            notes = json.loads((Y.out_dir(unit) / file).read_text(encoding="utf-8"))["notlar"]
            pool = [(i, x) for i, x in enumerate(notes) if x.get("tur") != "dogru" and not x.get("ehline_sor")
                    and (x.get("denetim") or {}).get("alinti") is not False and not (x.get("denetim") or {}).get("dayanak_yok")]
            havuz[f"taslak-{n}/{mod}"] = len(pool)
            by_type = defaultdict(list)
            for i, x in pool:
                by_type[x.get("tur")].append((i, x))
            for xs in by_type.values():
                rng.shuffle(xs)
            got = []
            while len(got) < ORNEK_PER and any(by_type.values()):     # türlere sırayla: en kalabalıktan başla
                for t in sorted(by_type, key=lambda t: -len(by_type[t])):
                    if by_type[t] and len(got) < ORNEK_PER:
                        got.append(by_type[t].pop())
            for i, x in got:
                picked.append({"taslak": f"taslak-{n}", "k": prefix + Y.critic_key(n, x), "mod": mod, "sira": i,
                               "tur": x.get("tur"), "capa": x.get("capa"), "metin": x.get("metin", "")})
    rng.shuffle(picked)            # okuyan biçimi sıradan tahmin etmesin (masada etiket yine görünür)
    data = {"birim": unit, "at": datetime.now().isoformat(timespec="seconds"), "havuz": havuz, "notlar": picked,
            "aciklama": "D11.3: aynı iki taslağın (eski 3, pilot 7) bütün olarak ve bölüm bölüm eleştirisinden eşit örneklem"}
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{path.relative_to(ROOT)}: {len(picked)} not; havuz {havuz}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("dosya")
    p.add_argument("unit", choices=P.UNITS)
    p = sub.add_parser("oran")
    p = sub.add_parser("hazirla")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--surum", help="istem sürümünün adı (varsayılan SURUM, --tarama ile h10)")
    p.add_argument("--tarama", action="store_true", help="D14.7 (h10): soru kalıpları (Ek 5) ve tarama tablosu")
    p = sub.add_parser("yazdir")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--surum")
    p.add_argument("--model", default="claude-opus-5-5")
    p.add_argument("--effort", default="high")
    p.add_argument("--yoksa", action="store_true",
                   help="birimde bu sürümün taslağı varsa yazdırma (iş yeniden başlatılınca aynı taslak iki kez yazılmasın)")
    p = sub.add_parser("izah")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--taslak", type=int, required=True)
    p.add_argument("--yeniden", action="store_true")
    p = sub.add_parser("bolum")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--taslak", type=int, nargs="+", required=True)
    p.add_argument("--yeniden", action="store_true")
    p = sub.add_parser("orneklem")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--taslak", type=int, nargs="+", required=True)
    p.add_argument("--yeniden", action="store_true")
    a = ap.parse_args()
    if a.cmd == "dosya":
        dosya(a.unit)
    elif a.cmd == "hazirla":
        hazirla(a.unit, a.surum, a.tarama)
    elif a.cmd == "yazdir":
        surum = a.surum or SURUM
        have = [q.stem for q in sorted((P.DRAFTS / a.unit).glob("taslak-*.json"))
                if q.stem.split("-")[1].isdigit()
                and json.loads(q.read_text(encoding="utf-8")).get("surum") == surum]
        if a.yoksa and have:
            print(f"{a.unit}: {surum} taslağı var ({', '.join(have)}); yazdırılmadı (--yoksa)")
        else:
            P.yazdir(a.unit, 1, a.model, a.effort, "hat", surum)
    elif a.cmd == "izah":
        izah(a.unit, a.taslak, a.yeniden)
    elif a.cmd == "bolum":
        bolum(a.unit, a.taslak, a.yeniden)
    elif a.cmd == "orneklem":
        orneklem(a.unit, a.taslak, a.yeniden)
    elif a.cmd == "oran":
        print(json.dumps(uzunluk_orani(), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
