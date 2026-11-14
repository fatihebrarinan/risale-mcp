"""Âyet masası (kullanıcının tasarımı, 2026-11-14): âyet üstte, lafızları tıklanır; sol yan kaynaklar, sağ yan yapay zekâ.

    uv run python scripts/d1-masa.py [11-12]      # data/d1/masa.html (kapalı depo; okuyuculara gönderilmez)

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
OUT = P.KEEP / "masa.html"
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
        for a, lang, _, text in blocks:
            sec = a.split("/")[0]
            if lang != "ar":
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
        for a, lang, _, _ in blocks:
            if lang == "tr":
                out[a] = out.get(a.replace("/tr/", "/ar/"), ["L:genel"])
        return out


# ---------------------------------------------------------------- kaynaklar

def isarat(unit: str) -> dict:
    """Gizlenen metin vecih vecih, paragraflarıyla; cümlelerin istem kimliği (a016) ve veritabanı kimliği."""
    cfg = P.UNITS[unit]
    out = {}
    for lang, rows in Y.hidden(unit).items():
        work = "isaratul-icaz-arabi" if lang == "ar" else "isaratul-icaz"
        bounds = {v: k for k, v in cfg["sections"][work].items() if k != "son"}
        cur, paras, last = None, [], None
        for short, sid, text, pid in rows:
            local = sid.rsplit("/", 1)[-1]
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
    cfg = P.UNITS[unit]
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

def drafts(unit: str, ayah: Ayah) -> dict:
    keep = P.DRAFTS / unit
    texts = P.SourceTexts(unit)
    out = {}
    for n in Y.drafts_of(unit):
        meta = json.loads((keep / f"taslak-{n}.json").read_text())
        blocks, cites = Y.draft_blocks(unit, n)
        log = keep / f"taslak-{n}.jsonl"
        ids = P.draft_sources(log) if log.exists() else {}
        sources = {}
        for k, cite in cites.items():
            server, sid = ids.get(k, (None, None))
            sources[k] = {"c": cite, "i": sid, "t": texts.text(server, sid, cite.split(" · ")[0])}
        istem = meta.get("istem", "tam")
        out[f"taslak-{n}"] = {
            "label": f"Taslak {n}",
            "about": {"tam": "tam istem", "ince": "ince istem", "ince-klasik": "ince istem, klasik eserler açık"}.get(istem, istem),
            "blocks": [{"a": a, "l": lang, "q": quote, "t": text} for a, lang, quote, text in blocks],
            "heads": ayah.heads(blocks), "sources": sources}
    return out


def layer(unit: str, ayah: Ayah, places: dict[str, list[str]], dr: dict) -> dict:
    """Eşleştirme, eleştiri ve bilirkişi maddeleri, her biri yeriyle (`loc`)."""
    y = Y.page_data(unit)
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
            "sample": sample, "critic_sample": critic_sample, "systemic": y["systemic"]}


def main() -> None:
    unit = sys.argv[1] if len(sys.argv) > 1 else "11-12"
    cfg = P.UNITS[unit]
    env = json.loads((Y.out_dir(unit) / "envanter.json").read_text(encoding="utf-8"))
    ayah = Ayah(unit)
    places = ayah.build_chips(env["kalemler"])
    dr = drafts(unit, ayah)
    data = {"unit": unit, "title": f"{cfg['sura_name']} {'–'.join(map(str, cfg['ayahs']))}",
            "verses": ayah.verses,
            "chips": [{k: c[k] for k in ("id", "ayah", "text", "norm")} for c in ayah.chips],
            "isarat": isarat(unit), "tefsir": tefsir(unit), "klasik": klasik(ayah), "risale": risale(unit),
            "drafts": dr, "yz": layer(unit, ayah, places, dr)}
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    OUT.write_text(TEMPLATE.read_text(encoding="utf-8").replace("{data}", blob), encoding="utf-8")
    counts = {}
    for i in data["yz"]["items"].values():
        for l in i["loc"]:
            counts[l] = counts.get(l, 0) + 1
    names = {c["id"]: c["text"] for c in ayah.chips}
    print(f"{OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KB)")
    print("nükteler:", ", ".join(f"{names.get(k, k)} {v}" for k, v in counts.items()))


if __name__ == "__main__":
    main()
