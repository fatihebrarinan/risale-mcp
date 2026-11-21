"""Âyet masası (kullanıcının tasarımı, 2026-11-14): âyet üstte, lafızları tıklanır; altında yanlar.

    uv run python scripts/d1-masa.py [11-12 …]    # data/d1/masa/<birim>.html (kapalı depo)

**İkinci hâli (S6, 2026-11-16, kullanıcının tasarımı):** yan sayısı dinamik ("+ yan ekle", en çok 4; bir yan tam,
iki yan ikiye, üç yan üçe; telefonda alt alta); her yan kendi seçicisiyle Kaynaklar, İşârât'ın metni ya da bir
taslaktır; seçilen yer bütün yanları süzer. Yapay zekâ kısmının odağı taslaktır: karşılaştırma, eleştirmen ve
bilirkişi taslağın üzerinde **katmandır** (sekme değil): karşılaştırma paragrafın sol kenarını boyar (bulunan, çelişki
adayı, fazla) ve sonda kaçırılan nükteleri sayar; eleştirmen ve bilirkişi paragrafın üstüne işaret koyar, tıklanınca
kartlar paragrafın altında açılır. "Metinlerin tamamı" bir yer düğmesidir (eski "bütün taslağı göster" ve "İşârât'ın
tamamı" kutuları kalktı). Kör kip taslakları "Taslak A, B…" diye sabit tohumla karışık adlandırır. Yanların düzeni
tarayıcıda birim başına saklanır (`d1-masa-yanlar-<birim>`); işaretlerin anahtarları ve dışa aktarma biçimi aynıdır.

Her birim kendi sayfasıdır (2026-11-16: tek sayfa vardı, 31–33 kurulunca 11–12'ninkinin üzerine yazılmıştı); birim
verilmezse envanteri olan bütün birimler kurulur. "Âyet" seçicisi öbürlerine gider; giriş sayfası (`index.html`)
`scripts/masa-giris.py`'dedir.

`okuma-yz.html`'in yerine geçmek için kuruldu: o sayfa iş akışımıza göre dizilmişti (D7, D9, D6 ayrı katman ve kod),
okur neyi neyle karşılaştıracağını bulamadı. Burada her şey âyetin bir yerine bağlıdır:

- **Yerler.** Üç düzey (kullanıcının kararı): "Önceki âyetlerle münasebet" (İşârât'ın ve taslağın birinci vechi),
  "Cümlelerin nazmı" (ikinci vecih) ve üçüncü vechin kelimeleri. Kelime düğmeleri âyetin kelimelerinden, envanterin
  lafız alanındaki harekeli Kur'ân sözlerinden kurulur: birden çok kelimelik söz, kelimelerinden biri tek başına
  geçmiyorsa tek düğmedir ("لا تفسدوا", "في الأرض"). Üçten çok kelimeyi kapsayan ya da kelimesi bulunamayan üçüncü vecih
  maddesi "Cümleler ve kelimesi belirsizler"dedir; yer uydurulmaz.
- **Taslak tarafı:** önce eşleştirmenin ya da eleştirinin nükte kimliği; yoksa taslak paragrafının vechi, üçüncü
  vecihte paragrafın başlığı: taslaklar İşârât gibi "وأما ﴿…﴾" diye başlar; paragrafın ilk 80 harfindeki ilk ayraçlı
  söz bir ya da iki düğmeye uyuyorsa paragraf onundur, "أما" ile başlayıp uymuyorsa ("وأما الغيبة") belirsizdir,
  ikisi de yoksa önceki paragrafın başlığı sürer (alıntı ve devam paragrafları). Tercüme paragrafı Arapçasınındır.
- **Kaynaklar** veritabanlarından: İşârât (gizlenen metin, Arapça asıl ve Abdülmecid Nursî tercümesi), 13 müfessirin
  bu âyetlerdeki birimleri (vefat sırasıyla), klasik eserlerde âyetten üç kelimelik bir dizinin geçtiği cümleler,
  Risale'de âyetin geçtiği öbür yerler. Müfessirlerin Türkçesi yok (kullanıcının kararı: sonraya).
- **İşaretler** eski sayfanın anahtarlarıyla saklanır ve aynı biçimde dışa aktarılır (`d1-yz-sinama`, `d1-yz-suzgec`,
  `d1-bilirkisi`; `d1-prova.py notlar` okur). Kör okuma yok (kullanıcının kararı): bilirkişi maddesinde eleştiri görünür.
"""

import importlib.util
import json
import re
import sqlite3
import sys
from pathlib import Path

from risale_mcp.library import Library
from risale_mcp.paths import ROOT

_spec = importlib.util.spec_from_file_location("d1_yz", ROOT / "scripts" / "d1-yz.py")
Y = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(Y)
P = Y.P

TEMPLATE = Path(__file__).with_name("d1-masa-sablon.html")
OUT_DIR = P.KEEP / "masa"
D5_DIR = ROOT / "data" / "interim" / "oku-masa"   # D5 birimlerinin masası: yeniden üretilir, git'e girmez (S7b)
KLASIK_DB = P.DIST_DIR / "klasik" / "risale.db"
LEVELS = {"V1": "L:munasebet", "V2": "L:nazim"}
OTHER = "L:belirsiz"

HAR = re.compile(r"[ً-ٰٟۖ-ۭـ]")
SEP = re.compile(r"[\s()«»←:،,{}\[\]﴿﴾.؛]+")


def norm(t: str) -> str:
    t = HAR.sub("", t)
    t = re.sub("[أإآٱ]", "ا", t).replace("ى", "ي").replace("ة", "ه")
    return re.sub(r"[^ء-ي]", "", t)


def tokens(text: str) -> list[str]:
    return [n for t in SEP.split(text) if (n := norm(t))]


def eq(tok: str, word: str) -> bool:
    """Metnin kelimesi âyetin kelimesi mi: aynı ya da başındaki و/ف'siz ("إذا" = "وإذا")."""
    return tok == word or (word[:1] in "وف" and len(word) > 3 and tok == word[1:])


# ---------------------------------------------------------------- âyet ve kelime düğmeleri

class Ayah:
    def __init__(self, unit: str):
        cfg = P.UNITS[unit]
        lib = Library(P.TEFSIR_DB)
        self.verses = []
        self.words = []                       # (âyet, metin, norm)
        for a in range(cfg["ayahs"][0], cfg["ayahs"][1] + 1):
            q = lib.find_ayah(str(cfg["sura"]), a)["quran"]
            self.verses.append({"n": a, "text": q["text"], "meal": q["translations"][0]["text"],
                                "meal_by": q["translations"][0]["translator"], "ref": q["ref"]})
            for w in q["text"].split():
                if norm(w):
                    self.words.append((a, w, norm(w)))
        self.wn = [w[2] for w in self.words]
        self.chips: list[dict] = []
        self.chip_of: dict[int, str] = {}

    def find(self, ph: list[str]) -> list[int] | None:
        for s in range(len(self.wn) - len(ph) + 1):
            if all(eq(ph[k], self.wn[s + k]) for k in range(len(ph))):
                return list(range(s, s + len(ph)))
        return None

    def spans(self, lafiz: str) -> list[list[int]]:
        """Envanterin lafız alanındaki harekeli sözler (Kur'ân'dan) âyette nerede; bulunmayan söz parçalanarak aranır."""
        phrases, cur = [], []
        for tok in re.findall(r"[^\s()«»←:،,]+|[()«»←:،,]", lafiz):
            if re.search(r"[ً-ْ]", tok) and norm(tok):
                cur.append(norm(tok))
            elif cur:
                phrases.append(cur)
                cur = []
        if cur:
            phrases.append(cur)
        out = []
        for ph in phrases:
            i = 0
            while i < len(ph):                 # en uzun bulunan alt diziyi al, kalanına devam et
                for j in range(len(ph), i, -1):
                    if (hit := self.find(ph[i:j])) is not None:
                        out.append(hit)
                        i = j
                        break
                else:
                    i += 1
        return out

    def build_chips(self, items: list[dict]) -> dict[str, list[str]]:
        """Kelime düğmeleri ve her üçüncü vecih maddesinin yeri {nükte: [yer]}."""
        spans = {i["id"]: self.spans(i["lafiz"]) for i in items if i["vecih"] == "V3"}
        singles = {s[0] for ss in spans.values() for s in ss if len(s) == 1}
        groups = sorted({tuple(s) for ss in spans.values() for s in ss
                         if 1 < len(s) <= 3 and not singles & set(s)}, key=len, reverse=True)
        taken: dict[int, tuple] = {}
        for g in groups:
            if not any(k in taken for k in g):
                for k in g:
                    taken[k] = g
        i = 0
        while i < len(self.words):
            g = taken.get(i, (i,))
            cid = f"W{len(self.chips) + 1}"
            self.chips.append({"id": cid, "ayah": self.words[i][0], "text": " ".join(self.words[k][1] for k in g),
                               "norm": [self.wn[k] for k in g]})
            for k in g:
                self.chip_of[k] = cid
            i = g[-1] + 1
        out = {}
        for i in items:
            if i["vecih"] in LEVELS:
                out[i["id"]] = [LEVELS[i["vecih"]]]
                continue
            covered = sorted({self.chip_of[k] for s in spans.get(i["id"], []) for k in s},
                             key=lambda c: int(c[1:]))
            out[i["id"]] = covered if 0 < len(covered) <= 3 else [OTHER]
        return out

    def chips_in(self, text: str) -> list[str]:
        toks = tokens(text)
        found = []
        for c in self.chips:
            n = c["norm"]
            if any(all(eq(toks[s + k], n[k]) for k in range(len(n))) for s in range(len(toks) - len(n) + 1)):
                found.append(c["id"])
        return found

    def heads(self, blocks: list) -> dict[str, list[str]]:
        """Taslak paragrafının yeri {çapa: [yer]}: birinci ve ikinci vecih düzeyleri, üçüncüde paragrafın başlığı."""
        out, head = {}, [OTHER]
        for a, lang, quote, text in blocks:
            sec = a.split("/")[0]
            if lang != "ar":
                continue
            if quote and sec == "V3":                    # kaynaktan alıntı yeni başlık açmaz, paragrafının yerindedir
                out[a] = head
                continue
            if sec in LEVELS:
                out[a] = [LEVELS[sec]]
                continue
            if sec != "V3":
                out[a] = ["L:genel"]
                continue
            start = text.lstrip(" \"'.…")[:80]
            found = next((c for br in re.findall(r"﴿([^﴾]+)﴾|«([^»]+)»", start)
                          if (c := self.chips_in("".join(br)))), None)
            if found:
                head = found if len(found) <= 2 else [OTHER]
            elif re.match(r"و?أما\b", start):
                head = [OTHER]
            out[a] = head
        pr, last = Y.pairs(blocks), ["L:genel"]
        for a, lang, _, _ in blocks:                     # Türkçe eşinin yerinde; eşsiz Türkçe önündeki paragrafın
            if lang == "tr":
                out[a] = out.get(pr.get(a, ""), last)
            last = out.get(a, last)
        return out


# ---------------------------------------------------------------- kaynaklar

def isarat(unit: str) -> dict:
    """Gizlenen metin vecih vecih, paragraflarıyla; cümlelerin istem kimliği (a016) ve veritabanı kimliği."""
    cfg = P.UNITS[unit]
    out = {}
    for lang, rows in Y.hidden(unit).items():
        work = "isaratul-icaz-arabi" if lang == "ar" else "isaratul-icaz"
        bounds = {v: k for k, v in cfg["sections"][work].items() if k != "son"}
        node = P.unit_node(cfg, work)
        cur, paras, last = None, [], None
        for short, sid, text, pid in rows:
            local = P.local_id(cfg, work, sid)
            cur = bounds.get(local, cur)
            if cur is None or cur == "Âyet":
                continue
            if pid != last:
                paras.append({"v": cur, "s": []})
                last = pid
            paras[-1]["s"].append({"k": short, "id": sid, "t": text})
        out[lang] = paras
    return out


def _unit_rows(conn: sqlite3.Connection, section: str) -> list[dict]:
    ords = conn.execute("SELECT ord, last_ord FROM nodes WHERE id = ?", (section,)).fetchone()
    work = section.split("/")[0]
    paras = conn.execute("""SELECT p.id, p.kind, p.text FROM paragraphs p JOIN nodes n ON n.id = p.node_id
                            WHERE n.work = ? AND n.ord BETWEEN ? AND ? ORDER BY n.ord, p.ord""",
                         (work, *ords)).fetchall()
    sents: dict[str, list] = {}
    for sid, pid, text in conn.execute("""SELECT s.id, s.paragraph_id, s.text FROM sentences s
                                          JOIN nodes n ON n.id = s.node_id WHERE n.work = ? AND n.ord BETWEEN ? AND ?
                                          ORDER BY s.seq""", (work, *ords)):
        sents.setdefault(pid, []).append({"id": sid, "t": text})
    out = []
    for pid, kind, text in paras:
        if kind == "ayah":
            out.append({"ayah": text})
        elif pid in sents:
            out.append({"s": sents[pid], "k": kind})
    return out


def tefsir(unit: str) -> list[dict]:
    cfg = P.UNITS[unit]
    lib = Library(P.TEFSIR_DB)
    conn = sqlite3.connect(f"file:{P.TEFSIR_DB}?mode=ro", uri=True)
    works: dict[str, dict] = {}
    for a in range(cfg["ayahs"][0], cfg["ayahs"][1] + 1):
        for w in lib.find_ayah(str(cfg["sura"]), a)["classical_works"]:
            entry = works.setdefault(w["work"], {"work": w["work"], "title": w["title"], "author": w["author"],
                                                 "units": []})
            for u in w["units"]:
                if u["section"] not in [x["id"] for x in entry["units"]]:
                    entry["units"].append({"id": u["section"], "ref": u["ref"], "verses": u["verses"],
                                           "printed": u.get("printed"), "rows": _unit_rows(conn, u["section"])})
    return list(works.values())


def klasik(ayah: Ayah, window: int = 3, context: int = 2) -> list[dict]:
    """Klasik eserlerde âyetten en az üç kelimelik bir dizinin geçtiği cümleler, önceki ve sonraki ikişer cümleyle."""
    grams = {tuple(ayah.wn[i:i + window]) for i in range(len(ayah.wn) - window + 1)
             if ayah.words[i][0] == ayah.words[i + window - 1][0]}
    conn = sqlite3.connect(f"file:{KLASIK_DB}?mode=ro", uri=True)
    titles = {s: (t, a) for s, t, a in conn.execute("SELECT slug, title, author FROM works")}
    out = []
    for seq, sid, node, work, text in conn.execute("SELECT seq, id, node_id, work, text FROM sentences ORDER BY seq"):
        toks = tokens(text)
        if not any(all(eq(toks[s + k], g[k]) for k in range(window)) for g in grams
                   for s in range(len(toks) - window + 1)):
            continue
        ctx = conn.execute("""SELECT s.id, s.text, n.ref FROM sentences s JOIN nodes n ON n.id = s.node_id
                              WHERE s.node_id = ? AND s.seq BETWEEN ? AND ? ORDER BY s.seq""",
                           (node, seq - context, seq + context)).fetchall()
        if out and out[-1]["node"] == node and any(c[0] == sid for c in out[-1]["s"]):
            out[-1]["hit"].append(sid)
            continue
        out.append({"node": node, "work": work, "title": titles[work][0], "author": titles[work][1] or "",
                    "ref": ctx[0][2], "hit": [sid], "s": [(i, t) for i, t, _ in ctx]})
    return [dict(x, s=[{"id": i, "t": t} for i, t in x["s"]]) for x in out]


def risale(unit: str) -> list[dict]:
    """Âyetin Risale'de geçtiği öbür yerler (İşârât'ın bu birimi ve Osmanlıca hariç), birer cümle bağlamla."""
    cfg = dict(P.UNITS[unit])
    cfg.setdefault("nodes", ())
    lib = Library(P.GENEL_DB)
    conn = sqlite3.connect(f"file:{P.GENEL_DB}?mode=ro", uri=True)
    seen, out = set(), []
    for a in range(cfg["ayahs"][0], cfg["ayahs"][1] + 1):
        for r in lib.find_ayah(str(cfg["sura"]), a)["results"]:
            sid = r["id"]
            if sid in seen or "osmanlica" in sid or any(sid.startswith(n + "/") for n in cfg["nodes"]):
                continue
            seen.add(sid)
            seq, node = conn.execute("SELECT seq, node_id FROM sentences WHERE id = ?", (sid,)).fetchone()
            ctx = conn.execute("SELECT id, text FROM sentences WHERE node_id = ? AND seq BETWEEN ? AND ? ORDER BY seq",
                               (node, seq - 1, seq + 1)).fetchall()
            out.append({"id": sid, "ref": r["ref"], "ayah": a, "s": [{"id": i, "t": t} for i, t in ctx]})
    return out


# ---------------------------------------------------------------- taslaklar ve yapay zekâ katmanı

TERCUME = P.KEEP / "tercume" / "kaynaklar.json"     # S7c.5: andığı tefsir ve klasik yerlerin Türkçesi (yapay zekâ)


def drafts(unit: str, ayah: Ayah) -> dict:
    keep = P.DRAFTS / unit
    texts = P.SourceTexts(unit)
    tercume = json.loads(TERCUME.read_text(encoding="utf-8")) if TERCUME.exists() else {}
    out = {}
    for n in Y.drafts_of(unit):
        meta = json.loads((keep / f"taslak-{n}.json").read_text())
        blocks, cites = Y.draft_blocks(unit, n)
        pr = Y.pairs(blocks)                                   # paragrafın eşi (çapanın sıra numarası değil)
        log = keep / f"taslak-{n}.jsonl"
        ids = P.draft_sources(log) if log.exists() else {}
        sources = {}
        for k, cite in cites.items():
            server, sid = ids.get(k, (None, None))
            sources[k] = {"c": cite, "i": sid, "t": texts.text(server, sid, cite.split(" · ")[0]),
                          **({"tr": tercume[sid]["tr"]} if sid in tercume else {})}
        istem = meta.get("istem", "tam")
        about = {"tam": "tam istem", "ince": "ince istem", "ince-klasik": "ince istem, klasik eserler açık",
                 "hat": "üretim hattı (D11): kısa istem, kaynak dosyası, uzunluk sınırı",
                 "cizelge": "D12.5 T1: önce okuma ve kelime çizelgesi (araçlı), sonra çizelgeden yazım (yalnız cite)"}.get(istem, istem)
        if meta.get("surum") and meta["surum"] != "v1":
            about += f" · istem {meta['surum']}"
        if meta.get("model") and meta["model"] != "claude-fable-5-2":
            about += f" · {meta['model']}"
        if d := meta.get("duzeltme"):                          # D12: düzeltilmiş taslak
            how = {"kapali": "kapalı kitap notlarıyla", "acik": "açık kitap notlarıyla",
                   "ikinci": "ikinci kapalı eleştirinin notlarıyla (D turu, d2)"}.get(d["notlar"], d["notlar"])
            about += f" · taslak {d['kaynak']}'in düzeltmesi, {how}"
        izah = Y.out_dir(unit) / f"izah-taslak-{n}.json"       # D11: günümüz Türkçesiyle izah, paragraf başına
        iz = {x["capa"]: x["metin"] for x in json.loads(izah.read_text(encoding="utf-8")).get("izah", [])} if izah.exists() else {}
        out[f"taslak-{n}"] = {
            "label": f"Taslak {n}", "about": about,
            "blocks": [{"a": a, "l": lang, "q": quote, "t": text, **({"p": pr[a]} if a in pr else {}),
                        **({"iz": iz[a]} if a in iz else {})}
                       for a, lang, quote, text in blocks],
            "heads": ayah.heads(blocks), "sources": sources}
    return out


def layer(unit: str, ayah: Ayah, places: dict[str, list[str]], dr: dict) -> dict:
    """Eşleştirme, eleştiri ve bilirkişi maddeleri, her biri yeriyle (`loc`). Envanteri ve eşleştirmesi olmayan
    birimde (D5, kabul birimi) yalnız eleştirmen katmanı (kapalı eleştirmen, kapının dosyalarından)."""
    y = Y.page_data(unit)
    if y is None:
        head = {dk: d["heads"] for dk, d in dr.items()}
        critic = {}
        for dk, c in Y.critic_page(unit).items():
            if dk in head:
                critic[dk] = dict(c, notes=[dict(x, loc=next((head[dk][a] for a in [x["a"]] if a in head[dk]),
                                                            ["L:genel"])) for x in c["notes"]])
        return {"models": [], "items": {}, "drafts": {}, "critic": critic, "bilirkisi": {}, "sample": [],
                "critic_sample": [], "systemic": [], "critic_sample_note": ""}
    env = json.loads((Y.out_dir(unit) / "envanter.json").read_text(encoding="utf-8"))
    hidden = {r[0]: r[1] for rows in Y.hidden(unit).values() for r in rows}
    items = {}
    for i in env["kalemler"]:
        page = y["items"][i["id"]]
        items[i["id"]] = {"v": i["vecih"], "l": i["lafiz"], "n": i["nukte"], "loc": places[i["id"]],
                          "sids": [hidden[x] for x in (i.get("ar") or []) + (i.get("tr") or []) if x in hidden],
                          "qt": page["qt"], "q": page["q"]}
    head = {dk: d["heads"] for dk, d in dr.items()}

    def where(dk: str, anchors: list[str], nukte: str | None = None) -> list[str]:
        if nukte and nukte in items:
            return items[nukte]["loc"]
        return next((head[dk][a] for a in anchors if a in head[dk]), ["L:genel"])

    out_drafts = {}
    for dk, d in y["drafts"].items():
        out_drafts[dk] = {"rows": d["rows"], "extras": [dict(f, loc=where(dk, f["a"])) for f in d["extras"]]}
    critic = {}
    for dk, c in y["critic"].items():
        critic[dk] = dict(c, notes=[dict(x, loc=where(dk, [x["a"]], x["n"])) for x in c["notes"]])
    bk = {part: [dict(x, loc=where(x["t"], [x["a"]])) for x in xs] for part, xs in y["bilirkisi"].items()}
    # D7.7 örneklemi (`d1-yz.sample_keys`): 30 satır, katmanlı; her biri yeriyle
    sample = []
    for key in y["sample"]:
        t, m, i = key.split("|")
        if m == "fazla":
            f = next((f for f in out_drafts.get(t, {}).get("extras", []) if f["k"] == i), None)
            loc = f["loc"] if f else ["L:genel"]
        else:
            loc = items[i]["loc"] if i in items else ["L:genel"]
        sample.append({"key": key, "t": t, "m": m, "id": i, "loc": loc})
    # D9.3 süzgeç örneklemi: her not yeriyle
    notes = {(dk, x["k"]): x for dk, c in critic.items() for x in c["notes"]}
    critic_sample = [dict(x, loc=notes[(x["t"], x["k"])]["loc"]) for x in y["critic_sample"] if (x["t"], x["k"]) in notes]
    return {"models": y["models"], "items": items, "drafts": out_drafts, "critic": critic, "bilirkisi": bk,
            "sample": sample, "critic_sample": critic_sample, "systemic": y["systemic"],
            "critic_sample_note": y.get("critic_sample_note", "")}


def ready_units() -> list[str]:
    """Masası kurulabilen birimler: taslağı olan her birim (ar-ge birimleri ve D5), Bakara sırasıyla."""
    order = {u["id"]: i for i, u in enumerate(P.d5_units())}
    units = [u for u in P.UNITS if (P.DRAFTS / u).is_dir() and Y.drafts_of(u)]
    return sorted(units, key=lambda u: order.get(u, 10 ** 6))


def out_dir(unit: str) -> Path:
    return D5_DIR if P.UNITS[unit].get("d5") else OUT_DIR


def extras(unit: str, dr: dict) -> dict:
    """S7b: kapının notları (her düzeltme ayrı, yazarın cevabıyla), nisbet hükümleri ve yayın sürümü; her not yeriyle
    (taslağın çapasından, `heads`). Ham hâliyle, ar-ge masası için (`oku-veri.masa_data`)."""
    spec = importlib.util.spec_from_file_location("oku_veri", ROOT / "scripts" / "oku-veri.py")
    if "oku_veri" not in sys.modules:
        mod = importlib.util.module_from_spec(spec)
        sys.modules["oku_veri"] = mod
        spec.loader.exec_module(mod)
    OV = sys.modules["oku_veri"]
    m = OV.masa_data(unit, {})
    def loc(dk: str, capa: str | None, quote: str | None = None) -> list[str]:
        h = (dr.get(dk) or {}).get("heads", {})
        if capa and capa in h:
            return h[capa]
        if quote:                                       # nisbet: alıntının geçtiği paragraf
            q = re.sub(r"\s+", " ", quote)[:40]
            for b in (dr.get(dk) or {}).get("blocks", []):
                if q and q in re.sub(r"\s+", " ", b["t"]):
                    return h.get(b["a"], ["L:genel"])
        return ["L:genel"]
    for k in m["kapi"]:
        for x in k["notlar"]:
            x["loc"] = loc(f"taslak-{k['taslak']}", x.get("capa"))
    for k in m["nisbet"]:
        for x in k["hukumler"]:
            x["loc"] = loc(f"taslak-{k['taslak']}", None, x.get("taslak_alinti"))
    YAY = OV.YAY
    idx = json.loads((YAY.YAYIN / "index.json").read_text(encoding="utf-8")) if (YAY.YAYIN / "index.json").exists() else {}
    cur = (idx.get("birimler") or {}).get(unit)
    yayin = None
    if cur:
        pub = json.loads((YAY.YAYIN / cur["yol"]).read_text(encoding="utf-8"))
        dk = f"taslak-{pub['kunye']['son_taslak']}"
        yayin = {"surum": pub["surum"], "taslak": dk,
                 "capa": {b["id"]: b["taslak_capa"] for b in pub["bloklar"]}}
    return {"kapi": m["kapi"], "nisbet": m["nisbet"], "alarmlar": m["alarmlar"], "yayin": yayin}


def build(unit: str, units: list[dict]) -> Path:
    cfg = P.UNITS[unit]
    envf = Y.out_dir(unit) / "envanter.json"
    env = json.loads(envf.read_text(encoding="utf-8")) if envf.exists() else {"kalemler": []}
    ayah = Ayah(unit)
    places = ayah.build_chips(env["kalemler"])
    dr = drafts(unit, ayah)
    d5 = bool(cfg.get("d5"))
    data = {"unit": unit, "title": title(unit), "units": units, "d5": d5,
            "verses": ayah.verses,
            "chips": [{k: c[k] for k in ("id", "ayah", "text", "norm")} for c in ayah.chips],
            "isarat": {} if d5 else isarat(unit), "tefsir": tefsir(unit), "klasik": klasik(ayah),
            "risale": risale(unit), "drafts": dr, "yz": layer(unit, ayah, places, dr), "masa": extras(unit, dr),
            "fark": sorted(p.name for p in OUT_DIR.glob(f"fark-{unit}-*.html")),   # D12.2 fark kartları
            "turlar": tur_pages(),                                                  # bütün birimlerin tur okumaları
            "tur": tur_data(unit),                                                  # D12.5 tur okuması (kör A/B)
            "tur_acik": tur_open(unit)}                                             # S7c: kör okuması sürüyor mu
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    out = out_dir(unit) / f"{unit}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(TEMPLATE.read_text(encoding="utf-8").replace("{data}", blob), encoding="utf-8")
    counts = {}
    for i in data["yz"]["items"].values():
        for l in i["loc"]:
            counts[l] = counts.get(l, 0) + 1
    names = {c["id"]: c["text"] for c in ayah.chips}
    print(f"{out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB)")
    print("  nükteler:", ", ".join(f"{names.get(k, k)} {v}" for k, v in counts.items()))
    return out


def tur_pages() -> list[dict]:
    """Bütün birimlerin tur okuma sayfaları (`masa/tur-<birim>-<tur>.html`), en yenisi başta: her masada üstte bağlantı
    (2026-11-18: D14.4 13'ün masasındaydı, 9–10'un masasında görünmüyordu)."""
    out = []
    for path in (P.DRAFTS).glob("*/tur-*.json"):
        t = json.loads(path.read_text(encoding="utf-8"))
        if t.get("sayfa") and (OUT_DIR / t["sayfa"]).exists():
            out.append({"sayfa": t["sayfa"], "birim": title(path.parent.name), "ad": t.get("ad"), "at": t.get("at", "")})
    return sorted(out, key=lambda x: x["at"], reverse=True)


def tur_data(unit: str) -> dict | None:
    """Birimin son tur okuması (`provalar/<birim>/tur-<tur>.json`, `d1-tur.py okuma` yazar; en son kaydedilen):
    {ad, a, b, giris, yerler, sayfa}."""
    turs = [json.loads(p.read_text(encoding="utf-8")) for p in (P.DRAFTS / unit).glob("tur-*.json")]  # T1…, D
    return max(turs, key=lambda t: t.get("at", "")) if turs else None


def tur_open(unit: str) -> dict | None:
    """Birimin son turu kör A/B ise ve okuyucunun sonucu henüz alınmadıysa (`data/d1/notlar/d1-tur-<b>-<tur>-*.json`
    yok) {ad, sayfa}: masada üstte uyarı (S7c.1, kullanıcının kararı: kör kip kalktı)."""
    t = tur_data(unit)
    if not t or not t.get("b") or list((P.KEEP / "notlar").glob(f"d1-tur-{unit}-{t.get('ad')}-*.json")):
        return None
    return {"ad": t.get("ad"), "sayfa": t.get("sayfa")}


def title(unit: str) -> str:
    cfg = P.UNITS[unit]
    a, b = cfg["ayahs"]
    return f"{cfg['sura_name']} {a}" if a == b else f"{cfg['sura_name']} {a}–{b}"      # tek âyet: "Bakara 13"


def main() -> None:
    every = ready_units()
    todo = sys.argv[1:] or every
    OUT_DIR.mkdir(exist_ok=True)
    units = [{"unit": u, "title": title(u), "ayah": list(P.UNITS[u]["ayahs"]), "d5": bool(P.UNITS[u].get("d5"))}
             for u in every]
    # Kur'ân panelinin listesi bütün masa sayfalarında ortak (eski sayfalar yeni D5 birimlerini de görsün)
    for d in {OUT_DIR, D5_DIR}:
        d.mkdir(parents=True, exist_ok=True)
        (d / "masa-birimler.json").write_text(json.dumps(units, ensure_ascii=False), encoding="utf-8")
    for unit in todo:
        build(unit, units)
    # index.html artık ar-ge masasının giriş sayfasıdır (scripts/masa-giris.py; S7.2, 2026-11-21)


if __name__ == "__main__":
    main()
