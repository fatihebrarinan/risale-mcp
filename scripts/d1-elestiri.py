"""D9 yapay zekâ eleştirmeni ve mekanik denetimler (PLANLAR.md D9).

    uv run python scripts/d1-elestiri.py mekanik 11-12 [--taslak 1 2 …]   # D9.1: model gerekmez
    uv run python scripts/d1-elestiri.py elestir 11-12 [--taslak 1 …] [--model opus] [--paralel 3] [--yeniden]  # D9.2
    uv run python scripts/d1-elestiri.py rapor 11-12                      # D9.2 notlarının denetimi ve raporu
    uv run python scripts/d1-elestiri.py bilirkisi 11-12 [--kisim A|B]    # D6.2 örneklemi (A sabit, B süzgeçten)
    uv run python scripts/d1-elestiri.py orneklem 11-12 [--yeniden]       # D9.3 süzgeç örneklemi (10 not, sabit)

D9.1 mekanik denetimleri hüküm vermez, aday ve sayı verir; eleştirmen (D9.2) ve kullanıcı (D9.3) bakar. Girdiler:
taslak (`provalar/<birim>/taslak-<n>.md`), yazarın dökümü (`.jsonl`: araçlardan dönen her metin), yazarın istemi (Ek 1–3:
usul özeti, birim çizelgesi, İşârât'ın görünen kısmı), D7'nin eşleştirmesi (`yz/sonuc.json`). "Okunan" yazarın o
oturumda gördüğü metindir: istem ve araç sonuçları (cite hariç). Denetimler:

1. **Kaynak numaraları:** metindeki [n] kaynakçada ve son `cite` çağrılarında var mı; kaynakçadaki numara metinde
   kullanılmış mı.
2. **Tırnak içindeki söz:** blok alıntılar, satır içi «…» “…” "…" (iki kelime ve fazlası) ve ﴾…﴿ âyet parçaları
   okunan metinde aranır (hareke ve noktalama yok sayılır; âyette harf iskeleti ikinci basamak). Sonuç: `kaynakta`
   (aynı paragraf çiftinin andığı kaynakta), `okunan` (okunan başka bir yerde), `ayet` (Kur'ân'da), `bulunmadi`.
   Bulunmayan Arapça söz kendi sözüdür (dinleyenin sorusu, takdir edilen cümle: usule uygun olabilir); ardından
   kaynak numarası geliyorsa "kaynağa nisbet edilen söz kaynakta yok" diye ayrıca sayılır. Bulunmayan Türkçe söz
   yazarın kendi tercümesidir (kullanıcının sohbetteki istem önerisi: tırnağa yalnız araçların döndürdüğü metin).
   Damgasız Türkçe blok alıntı ayrıca sayılır.
3. **Okunan kaynaklarla ortak söz:** taslağın her Arapça cümlesi okunan cümlelerle anahtar üçlüleri (hafif kökle:
   baştaki و ف ve harf-i tarif atılır) üzerinden karşılaştırılır; Kur'ân'daki ve okunanların çoğunda geçen kalıp
   üçlüler sayılmaz. En az `MIN_SHARED` ortak üçlü bir benzerliktir. Benzerlik paragraf çiftinin andığı kaynaktaysa
   sorun yok; değilse ve paragraf çiftinin tercümesinde "kendi tespiti" varsa `kendi_tespiti` adayı (cümlenin
   paragraftaki yeri oranıyla tercümedeki işaretin yerine yakınsa), yoksa `atifsiz` adayı. Aday hükmü değildir:
   İşârât'ın kalıplarını almak usuldür, ortak kelimeler gösterilir.
4. **Kaçırılan nüktelerin ipucu:** D7'de iki okuyucunun da bulunamadı dediği (`yok` ya da `farkli_gerekce`) her
   envanter kalemi için kalemin İşârât alıntısının ve lafzının ayırt edici kelimeleri (âyetin kelimeleri ve sık
   kelimeler hariç) okunan cümlelerde ve okunmayan ama kolay erişilen yerlerde (müfessirlerin 11–12 birimleri,
   İşârât'ın görünen kısmı) aranır. En yüksek puanlı üç yer, okundu mu diye. "Okunan yerde güçlü aday" dikkat
   sorununa, "yalnız okunmayan yerde" arama sorununa işarettir; karar eleştirmenin ve kullanıcınındır.

Çıktılar: `provalar/<birim>/yz/mekanik-taslak-<n>.json`, rapor `provalar/<birim>/d9-mekanik.md`.

D9.2 eleştirmen (tek model, kullanıcının kararı; varsayılan Opus 5.5, taslakları yazan Fable değil): istem
`docs/d1/elestiri-istemi.md` (sürümlü), `claude -p` proje dışında, yerleşik araçlar ve web kapalı, Risale, Tefsir,
Klasik ve Hadis eklentileri yayındaki veritabanlarıyla açık (İşârât gizlenmez). Taslağın tamamını, D7'nin
eşleştirmesini ve D9.1'in bulgularını istemde görür. Notlar okuma notlarının türleriyle, çapayla ve dayandığı cümle
kimlikleriyle gelir; program her notun taslak alıntısını çapasında, her dayanağı veritabanında ve eleştirmenin o
oturumda okuduklarında arar (bulunmayan not silinmez, işaretlenir). Çıktı `yz/elestiri-taslak-<n>.{json,jsonl,meta.json}`,
rapor `provalar/<birim>/d9-elestiri.md`.
"""

import argparse
import importlib.util
import json
import math
import re
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from collections import Counter, defaultdict
from pathlib import Path

from risale_mcp.normalize import search_words
from risale_mcp.paths import ROOT
from risale_mcp.quran import skeleton

_spec = importlib.util.spec_from_file_location("d1_prova", ROOT / "scripts" / "d1-prova.py")
P = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P)
_spec = importlib.util.spec_from_file_location("d1_yz", ROOT / "scripts" / "d1-yz.py")
Y = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(Y)

ISTEM_FILES = {None: "istem.md", "tam": "istem.md", "ince": "istem-ince.md", "ince-klasik": "istem-ince-klasik.md"}
STAMP = "Yapay zekâ tercümesi:"
MIN_SHARED = 2               # ortak anahtar üçlüsü: 2 üçlü ≈ 4 ardışık kelime
COMMON_SHARE = 0.02          # okunan cümlelerin bu oranından fazlasında geçen üçlü kalıptır
TOP_HINTS = 3
AR = re.compile(r"[؀-ۿ]")
MARK = re.compile(r"\[([^\[\]\n]{1,80})\]")
INLINE = re.compile(r"«([^«»\n]+)»|“([^“”\n]+)”|\"([^\"\n]+)\"")
AYAH = re.compile(r"﴿([^﴾\n]+)﴾")


# ---------------------------------------------------------------- yardımcılar

def is_ar(text: str) -> bool:
    return P._arabic_ratio(text) > 0.5


def akey(w: str) -> str:
    """Arapça kelimenin hafif kökü (iki taraf aynı işlemden geçer): و/ف ve harf-i tarif atılır."""
    if not AR.search(w):
        return w
    w = w.translate(str.maketrans("ةىأإآؤئ", "هيااااي"))
    if len(w) > 3 and w[0] in "وف":
        w = w[1:]
    for pre in ("بال", "كال", "فال", "لل", "ال"):
        if w.startswith(pre) and len(w) - len(pre) >= 2:
            return w[len(pre):]
    return w


def keys(text: str) -> list[str]:
    return [akey(w) for w in search_words(text)]


def grams(text: str, n: int = 3) -> set[tuple[str, ...]]:
    k = keys(text)
    return {tuple(k[i:i + n]) for i in range(len(k) - n + 1)}


def split_ar(text: str) -> list[str]:
    """Taslağın Arapça paragrafını cümlelere: . ؟ ! ؛ ve İşârât'ın ".." ayracı."""
    parts = re.split(r"(?<=[.؟!؛])\s+|\.\.\s+", re.sub(MARK, "", text))
    return [p.strip() for p in parts if len(search_words(p)) >= 3]


def marks_of(text: str) -> tuple[set[str], list[tuple[int, str]]]:
    """Paragraftaki kaynak numaraları ve işaretler (konum, içerik)."""
    nums, out = set(), []
    for m in MARK.finditer(text):
        body = m.group(1)
        nums |= set(re.findall(r"\d+", body.split("burada")[0]))
        out.append((m.start(), body))
    return nums, out


# ---------------------------------------------------------------- okunanlar

FULL_ID = re.compile(r"\[([a-z][\w-]*/[^\]\s]*?c\d+)\] ")
_WORKS: dict[str, str] = {}


def _server_of(sid: str) -> str:
    """Tam kimliğin eklentisi: eserin hangi veritabanında olduğuna göre (tefsir, klasik, yoksa risale)."""
    if not _WORKS:
        for server in ("tefsir", "klasik"):
            db = sqlite3.connect(f"file:{CRITIC_DBS[server]}?mode=ro", uri=True)
            for (w,) in db.execute("SELECT DISTINCT work FROM nodes"):
                _WORKS[w] = server
    return _WORKS.get(sid.split("/", 1)[0], "risale")


class Read:
    """Yazarın oturumda gördüğü metin: [(sunucu, kimlik, dil, metin)] ve kimlikten metin."""

    def __init__(self, unit: str | None = None, n: int | None = None, log: Path | None = None):
        self.items: dict[tuple[str, str], str] = {}
        if log is not None:                     # yalnız bir dökümün okudukları (eleştirmen)
            self._log(log)
            return
        meta = json.loads((P.DRAFTS / unit / f"taslak-{n}.json").read_text(encoding="utf-8"))
        name = ISTEM_FILES.get(meta.get("istem"), "")
        if meta.get("istem") in P.ISTEM:            # sürümlü istem (D8: v1 ve v2 aynı birimde)
            name = P.istem_files(meta["istem"], meta.get("surum", "v1"))[0]
        prompt = P.OUT / unit / name
        raw = prompt.read_text(encoding="utf-8")
        if P._sha(raw) != meta["prompt_sha"]:
            print(f"  uyarı: taslak {n}'in istemi değişmiş ({prompt.name}); okunanlar bugünkü istemden")
        self._prompt(raw)
        self._log(P.DRAFTS / unit / f"taslak-{n}.jsonl")

    def add(self, server: str, sid: str, text: str) -> None:
        if text and len(search_words(text)) >= 2:
            self.items.setdefault((server, sid), text)

    def _prompt(self, raw: str) -> None:
        node, ek = None, "istem"
        for i, line in enumerate(raw.split("\n")):
            if line.startswith("# Ek "):
                ek = "ek" + line[5]
            if m := re.match(r"#{3,4} .*\(`([^`]+)`\)", line):
                node = m.group(1)
            elif FULL_ID.match(line):          # D11 kaynak dosyası: "[eser/…/c033] metin" (bir satırda birkaç cümle)
                parts = FULL_ID.split(line)
                for sid, text in zip(parts[1::2], parts[2::2]):
                    self.add(_server_of(sid), sid, text.strip())
            elif m := re.match(r"\[(c\d+(?:/[\w/-]+)?)\] (.+)", line):
                self.add("risale", f"{node}/{m.group(1)}" if node else m.group(1), m.group(2))
            elif line.strip() and not line.startswith("#"):
                self.add("istem", f"{ek}:{i + 1}", line.lstrip("> ").strip())

    def _walk(self, server: str, obj, ayah_ctx: str | None = None) -> None:
        if isinstance(obj, dict):
            text = obj.get("text")
            if isinstance(text, str):
                if "id" in obj:
                    self.add(server, str(obj["id"]), text)
                elif "ayah" in obj:
                    self.add("kuran", f"{obj.get('sura', ayah_ctx or '?')}:{obj['ayah']}", text)
                elif "translator" in obj and ayah_ctx:
                    self.add("meal", f"{ayah_ctx}:{obj['translator']}", text)
            for key in ("matn", "arabic"):
                if isinstance(obj.get(key), str) and "id" in obj:
                    self.add(server, f"{obj['id']}#{key}", obj[key])
            ctx = f"{obj.get('sura', '')}:{obj['ayah']}" if "ayah" in obj and "text" in obj else ayah_ctx
            for v in obj.values():
                self._walk(server, v, ctx)
        elif isinstance(obj, list):
            for v in obj:
                self._walk(server, v, ayah_ctx)

    def _log(self, log: Path) -> None:
        names = {}
        for line in log.read_text(encoding="utf-8").splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            for block in (event.get("message") or {}).get("content", []) if isinstance(event.get("message"), dict) else []:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "tool_use":
                    names[block["id"]] = block["name"].removeprefix("mcp__")
                elif block.get("type") == "tool_result":
                    name = names.get(block.get("tool_use_id"), "?")
                    if name.endswith("__cite"):
                        continue
                    content = block.get("content")
                    texts = [c.get("text", "") for c in content] if isinstance(content, list) else [content or ""]
                    for t in texts:
                        try:
                            self._walk(name.split("__")[0], json.loads(t))
                        except (json.JSONDecodeError, TypeError):
                            self.add(name.split("__")[0], f"{name}:metin", t)

    def nodes(self, only: set[tuple[str, str]] | None = None) -> dict[tuple[str, str], str]:
        """Okunan cümleler bölüm bölüm birleşik (alıntı birden çok cümleyi aşabilir); `only` verilirse yalnız onlar."""
        if only is None and hasattr(self, "_nodes"):
            return self._nodes
        groups: dict[tuple[str, str], list] = defaultdict(list)
        for key, text in self.items.items():
            if only is not None and key not in only:
                continue
            node = key[1].rsplit("/", 1)[0] if re.search(r"/c\d+$", key[1]) else key[1]
            groups[(key[0], node)].append((key[1], text))
        out = {k: " ".join(t for _, t in sorted(v)) for k, v in groups.items()}
        if only is None:
            self._nodes = out
        return out

    def find(self, quote: str, only: set[tuple[str, str]] | None = None) -> list[tuple[str, str]]:
        return [key for key, text in self.nodes(only).items() if Y.quote_found(quote, text)]


# ---------------------------------------------------------------- taslak

def draft(unit: str, n: int) -> dict:
    """Paragraf çiftleri: [{ar, tr, ar_text, tr_text, quote, stamped}] okuma sayfasının çapalarıyla."""
    raw = (P.DRAFTS / unit / f"taslak-{n}.md").read_text(encoding="utf-8")
    blocks, sources = Y.draft_blocks(unit, n)
    flat = re.sub(r"\s+", " ", raw)
    pairs, last_ar, last_para = [], None, None
    for anchor, lang, quote, text in blocks:
        stamped = lang == "tr" and (STAMP + " " + re.sub(r"\s+", " ", text)[:60]) in flat
        if lang == "ar":
            pairs.append({"ar": anchor, "ar_text": text, "quote": quote, "tr": None, "tr_text": "", "stamped": None})
            last_ar = pairs[-1]
            if not quote:
                last_para = pairs[-1]
        elif not quote and last_ar is not None and last_ar["quote"] and last_para is not None \
                and last_para["tr"] is None and anchor.split("/")[0] == last_para["ar"].split("/")[0]:
            # paragrafın tercümesi alıntılardan sonra (D12.5 T1): alıntıya değil paragrafa bağlanır
            last_para.update(tr=anchor, tr_text=text, stamped=stamped, tr_quote=quote)
        elif last_ar is not None and last_ar["tr"] is None and anchor.split("/")[0] == last_ar["ar"].split("/")[0]:
            last_ar.update(tr=anchor, tr_text=text, stamped=stamped, tr_quote=quote)
        else:
            pairs.append({"ar": None, "ar_text": "", "quote": quote, "tr": anchor, "tr_text": text, "stamped": stamped,
                          "tr_quote": quote})
    return {"pairs": pairs, "sources": sources, "raw": raw}


def expand(sid: str) -> list[str]:
    """Kaynak aralığı (`…/c005..c007`) cümle kimliklerine; cite aralığı tek bölümde tutar."""
    first, _, last = sid.partition("..")
    m = re.match(r"(.*/c)(\d+)$", first)
    if not last or not m or not last.lstrip("c").isdigit():
        return [first]
    width = len(m[2])
    return [f"{m[1]}{i:0{width}d}" for i in range(int(m[2]), int(last.lstrip("c")) + 1)]


def source_keys(ids: dict) -> dict[str, set[tuple[str, str]]]:
    """Kaynak numarası -> okunan anahtarları {(sunucu, cümle kimliği)}."""
    return {n: {(srv, x) for x in expand(sid)} for n, (srv, sid) in ids.items()}


def pair_nums(p: dict) -> set[str]:
    return marks_of(p["ar_text"])[0] | marks_of(p["tr_text"])[0]


# ---------------------------------------------------------------- 1. kaynak numaraları

def check_numbers(d: dict, ids: dict) -> dict:
    used = set()
    for p in d["pairs"]:
        used |= pair_nums(p)
    listed = set(d["sources"])
    ayah = {k for k, v in d["sources"].items() if re.match(r"[^›]*Sûresi, \d+:\d+", v)}   # âyet atfı cite'tan geçmez
    return {"metinde_kaynakcada_yok": sorted(used - listed, key=int),
            "metinde_cite_yok": sorted(used - set(ids) - ayah, key=int),
            "kaynakcada_kullanilmayan": sorted(listed - used, key=int),
            "kullanilan": len(used), "kaynakca": len(listed)}


# ---------------------------------------------------------------- 2. tırnak içindeki söz

def _status(quote: str, nums: set[str], ids: dict, read: Read) -> tuple[str, list[str]]:
    cited = set().union(*(ids[k] for k in nums if k in ids))
    hit = read.find(quote, cited)
    if hit:
        return "kaynakta", [f"{s}:{i}" for s, i in hit[:3]]
    hit = read.find(quote)
    if hit:
        kur = [h for h in hit if h[0] in ("kuran", "meal")]
        return ("ayet" if kur and len(kur) == len(hit) else "okunan"), [f"{s}:{i}" for s, i in hit[:3]]
    return "bulunmadi", []


def _followed_by_num(text: str, end: int) -> bool:
    """Tırnağın ardından, cümle bitmeden bir kaynak numarası geliyor mu."""
    rest = text[end:end + 160]
    stop = re.search(r"[.؟!?;؛]\s", rest)
    seg = rest[:stop.start()] if stop else rest
    return any(re.search(r"\d", m.group(1)) for m in MARK.finditer(seg))


def ayah_status(frag: str, read: Read, quran_sk: list[str]) -> str:
    if read.find(frag, {k for k in read.items if k[0] in ("kuran",)}) or read.find(frag):
        return "aynen"
    sk = skeleton(frag)
    if len(sk) >= 4 and any(sk in a for a in quran_sk):
        return "iskelet"
    return "bulunmadi"


# D12.5 Tur 0 (kullanıcının kararı, 2026-11-16): h2'den beri taslağın Türkçesinde «…» takdir ve beklenen sözdür,
# "…" kaynağın sözü. O taslaklarda Türkçe «…» tırnak sayılmaz, `takdir` diye ayrıca sayılır (aranmaz).
NO_TAKDIR = {"v1", "v2", "h1"}


def takdir_mark(meta: dict) -> bool:
    return (meta.get("surum") or "v1") not in NO_TAKDIR


def check_quotes(d: dict, ids: dict, read: Read, quran_sk: list[str], takdir: bool = False) -> list[dict]:
    out = []
    for p in d["pairs"]:
        nums = pair_nums(p)
        for lang, anchor, text, is_block in (("ar", p["ar"], p["ar_text"], p["quote"]),
                                             ("tr", p["tr"], p["tr_text"], p.get("tr_quote"))):
            if not anchor:
                continue
            body = MARK.sub("", text)
            if is_block and not anchor.startswith("Âyet"):
                if lang == "ar":
                    st, where = _status(body, nums, ids, read)
                    out.append({"tur": "blok", "dil": lang, "capa": anchor, "soz": body, "durum": st, "yer": where})
                elif not p.get("stamped"):
                    st, where = _status(body, nums, ids, read)
                    out.append({"tur": "blok_damgasiz", "dil": lang, "capa": anchor, "soz": body, "durum": st,
                                "yer": where})
                continue
            for m in AYAH.finditer(text):
                st = ayah_status(m.group(1), read, quran_sk)
                out.append({"tur": "ayet", "dil": lang, "capa": anchor, "soz": m.group(1).strip(), "durum": st})
            for m in INLINE.finditer(text):
                q = next(g for g in m.groups() if g is not None).strip()
                if takdir and m.group(1) is not None and not is_ar(q):
                    out.append({"tur": "takdir", "dil": "tr", "capa": anchor, "soz": q, "durum": "takdir", "yer": []})
                    continue
                if len(search_words(AYAH.sub(" ", q))) < 2:
                    continue
                st, where = _status(q, nums, ids, read)
                qlang = "ar" if is_ar(q) else "tr"
                out.append({"tur": "satir_ici", "dil": qlang, "capa": anchor, "soz": q, "durum": st, "yer": where,
                            "nisbet": _followed_by_num(text, m.end())})
    return out


# ---------------------------------------------------------------- 3. okunanlarla ortak söz

FORMULA_WORDS = "رمز خفي ايماء اشاره تلويح نظم هييه هييات جمله جمل اعلم لما فيه هذه تعميم مفعول حذف قيل اي ذلك كلام"


def content_gram(g: tuple, stop: set) -> bool:
    """Kalıp olmayan üçlü: en az iki kelimesi ne edat ne İşârât'ın kalıp terimi."""
    return sum(w not in stop for w in g) >= 2


class GramIndex:
    def __init__(self, read: Read, stop: set):
        self.by: dict[tuple, set] = defaultdict(set)
        self.grams: dict[tuple[str, str], set] = {}
        for key, text in read.items.items():
            if key[0] in ("kuran", "meal") or not is_ar(text):
                continue
            g = {x for x in grams(text) - stop if content_gram(x, FORMULA)}
            self.grams[key] = g
            for x in g:
                self.by[x].add(key)
        limit = max(3, int(COMMON_SHARE * len(self.grams)))
        self.common = {x for x, ks in self.by.items() if len(ks) > limit}

    def best(self, text: str, k: int = 2) -> list[tuple[tuple[str, str], list[tuple]]]:
        g = {x for x in grams(text) - self.common if content_gram(x, FORMULA)}
        hits = Counter()
        for x in g:
            for key in self.by.get(x, ()):
                hits[key] += 1
        out = []
        for key, c in sorted(hits.items(), key=lambda kv: (-kv[1], kv[0]))[:k]:
            if c >= MIN_SHARED:
                out.append((key, sorted(g & self.grams[key])))
        return out


def check_overlap(d: dict, ids: dict, index: GramIndex) -> list[dict]:
    rev = {key: n for n, keys_ in ids.items() for key in keys_}
    out = []
    for p in d["pairs"]:
        if not p["ar"] or p["quote"] or p["ar"].startswith("Âyet"):
            continue
        nums = pair_nums(p)
        cited = set().union(*(ids[k] for k in nums if k in ids))
        sents = split_ar(p["ar_text"])
        tr = p["tr_text"]
        own = [pos / max(1, len(tr)) for pos, body in marks_of(tr)[1] if "kendi tespiti" in body or "istinbat" in body]
        plain = MARK.sub("", p["ar_text"])
        for s in sents:
            found = index.best(s)
            if not found:
                continue
            key, shared = found[0]
            if key in cited or any(k in cited for k, _ in found):
                continue
            pos = plain.find(s[:30]) / max(1, len(plain))
            near_own = any(abs(pos - o) <= 0.35 or (o >= pos and o - pos <= 0.5) for o in own)
            num = rev.get(key)
            out.append({"capa": p["ar"], "cumle": s, "kaynak": f"{key[0]}:{key[1]}", "kaynak_no": num,
                        "ortak": [" ".join(x) for x in shared][:6], "ortak_sayi": len(shared),
                        "tur": "kendi_tespiti" if near_own else "atifsiz",
                        "kaynakcada": num is not None})
    return out


# ---------------------------------------------------------------- 4. kaçırılan nüktelerin ipucu

STOP_AR = set(map(akey, search_words(
    "في من على إلى عن أن إن ما لا لم لن هو هي هم هذا هذه ذلك تلك الذي التي الذين كما مع ثم بل قد كل بعض أي إذ إذا "
    "لما أو أم حتى كان يكون له لها لهم به بها بهم فيه فيها منه منها عليه عليهم إليه وهو وهي ولا فلا كذلك أيضا "
    "اعلم أنه أنها إنه إنما ليس غير بين عند قال يقول تعالى الله قوله لأن لكن وجه أما لابد جملة الآية")))


FORMULA = STOP_AR | set(FORMULA_WORDS.split())


def unread_places(unit: str) -> dict[tuple[str, str], str]:
    """Kolay erişilen ama okunmamış olabilecek yerler: müfessirlerin âyet birimleri ve İşârât'ın görünen kısmı."""
    cfg = P.UNITS[unit]
    out = {}
    t = sqlite3.connect(P.OUT / unit / "tefsir.db")
    a0, a1 = cfg["ayahs"]
    for nid, in t.execute("SELECT DISTINCT node_id FROM sentences WHERE node_id LIKE ?", (f"%/{cfg['sura']}/%",)):
        rng = nid.split("/")[2] if nid.count("/") >= 2 else ""
        m = re.match(r"(\d+)(?:-(\d+))?$", rng)
        if m and int(m[1]) <= a1 and int(m[2] or m[1]) >= a0:
            for sid, text in t.execute("SELECT id, text FROM sentences WHERE node_id = ?", (nid,)):
                out[("tefsir", sid)] = text
    r = sqlite3.connect(P.OUT / unit / "risale.db")
    for sid, text in r.execute("SELECT id, text FROM sentences WHERE id LIKE 'isaratul-icaz-arabi/sure-i-bakara/%'"):
        out[("risale", sid)] = text
    return out


def check_hints(unit: str, n: int, read: Read, extra: dict, ayah_words: set) -> list[dict]:
    res = json.loads((Y.out_dir(unit) / "sonuc.json").read_text(encoding="utf-8"))
    rows = {r["id"]: r for r in res["taslaklar"].get(f"taslak-{n}", {}).get("satirlar", [])}
    items = {i["id"]: i for i in res["envanter"]["kalemler"]}
    pool = {k: v for k, v in read.items.items() if is_ar(v) and k[0] not in ("kuran", "meal")}
    pool_all = dict(pool)
    for k, v in extra.items():
        pool_all.setdefault(k, v)
    docs = {k: set(keys(v)) for k, v in pool_all.items()}
    df = Counter(w for ws in docs.values() for w in ws)
    total = len(docs)
    out = []
    for iid, row in rows.items():
        st = set(row["durum"].values())
        if st & set(Y.FOUND) or None in st:
            continue
        it = items[iid]
        words = {w for w in keys(it.get("alinti", "") + " " + it.get("lafiz", ""))
                 if len(w) >= 3 and w not in STOP_AR and w not in ayah_words and AR.search(w)}
        if not words:
            continue
        scored = []
        for k, ws in docs.items():
            common = words & ws
            if len(common) < 2:
                continue
            score = sum(math.log(total / df[w]) for w in common)
            scored.append((score, k, sorted(common)))
        scored.sort(reverse=True)
        out.append({"kalem": iid, "durum": row["durum"], "nukte": it.get("nukte", ""), "anahtar": sorted(words),
                    "adaylar": [{"yer": f"{k[0]}:{k[1]}", "okundu": k in pool, "puan": round(s, 1),
                                 "ortak": c, "metin": pool_all[k][:400]} for s, k, c in scored[:TOP_HINTS]]})
    return out


# ---------------------------------------------------------------- çalıştırma ve rapor

def quran_data(unit: str) -> tuple[list[str], set]:
    conn = sqlite3.connect(P.GENEL_DB)
    sk = [skeleton(t) for (t,) in conn.execute("SELECT text FROM quran_ayahs")]
    cfg = P.UNITS[unit]
    words = set()
    for (t,) in conn.execute("SELECT text_simple FROM quran_ayahs WHERE sura = ? AND ayah BETWEEN ? AND ?",
                             (cfg["sura"], cfg["ayahs"][0], cfg["ayahs"][1])):
        words |= set(keys(t))
    return sk, words


def quran_grams(unit: str) -> set:
    conn = sqlite3.connect(P.GENEL_DB)
    out = set()
    for (t,) in conn.execute("SELECT text_simple FROM quran_ayahs"):
        out |= grams(t)
    return out


# D6'nın dersi (2026-11-14): taslağın kendi tespitinde inhisar ve mutlaklık kalıbı, kapsam ve derece adayı. A10
# ("nifâkın tabiatıyla ifsad olduğuna işârettir") ve A09 ("reddi nâsihin şahsına değil, nasihatin kendisinedir")
# bu süzgeçten geçer; hüküm eleştirmenin (istem v1.2, 4. soru) ve okuyucunundur.
SCOPE = re.compile(r"(?<![\w])(tabiatıyla|zâtında|zatında|dâima|daima|asla|hiç|ancak|yalnız|sadece|"
                   r"değil(?:dir)?(?![\w])[^.;]{0,40}?(?:dır|dir|dur|dür|tır|tir|tur|tür)(?![\w]))", re.I)


def check_scope(d: dict) -> list[dict]:
    out = []
    for p in d["pairs"]:
        if not p.get("tr"):
            continue
        for sent in re.split(r"(?<=[.!?])\s+", p["tr_text"]):
            m = SCOPE.search(sent)
            if m and ("kendi tespiti" in sent or "istinbat" in sent):
                out.append({"capa": p["tr"], "kalip": m.group(1)[:40], "cumle": sent.strip()})
    return out


def mekanik(unit: str, drafts: list[int]) -> None:
    d_out = Y.out_dir(unit)
    quran_sk, ayah_words = quran_data(unit)
    qgrams = quran_grams(unit)
    extra = unread_places(unit)
    results = {}
    for n in drafts:
        read = Read(unit, n)
        raw_ids = P.draft_sources(P.DRAFTS / unit / f"taslak-{n}.jsonl")
        ids = source_keys(raw_ids)
        d = draft(unit, n)
        index = GramIndex(read, qgrams)
        r = {"taslak": n, "okunan": len(read.items),
             "okunan_sunucu": dict(Counter(k[0] for k in read.items)),
             "numaralar": check_numbers(d, raw_ids),
             "tirnak": check_quotes(d, ids, read, quran_sk,
                                    takdir_mark(json.loads((P.DRAFTS / unit / f"taslak-{n}.json").read_text()))),
             "ortak": check_overlap(d, ids, index),
             "ipucu": check_hints(unit, n, read, extra, ayah_words),
             "kapsam": check_scope(d)}
        (d_out / f"mekanik-taslak-{n}.json").write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
        results[n] = r
        q = Counter((x["tur"], x["dil"], x["durum"]) for x in r["tirnak"])
        print(f"taslak {n}: okunan {r['okunan']} · tırnak {len(r['tirnak'])} · ortak {len(r['ortak'])} · "
              f"ipucu {len(r['ipucu'])} · kapsam {len(r['kapsam'])}")
    report(unit, results)


def _s(text: str, k: int = 160) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= k else text[:k - 1] + "…"


def report(unit: str, results: dict) -> None:
    L = [f"# Prova {unit}: D9.1 mekanik denetimler", "",
         f"`uv run python scripts/d1-elestiri.py mekanik {unit}` üretir. Hüküm değil aday ve sayıdır; ayrıntı "
         "`yz/mekanik-taslak-<n>.json`. \"Okunan\": yazarın o oturumda gördüğü metin (istem ve araç sonuçları).", ""]
    L += ["## Özet", "", "| Taslak | Okunan | Numara sorunu | Ar. tırnak: kaynakta / okunan / bulunmadı (nisbetli) | "
          "Tr. tırnak bulunmadı (nisbetli) | Damgasız Tr. blok | Âyet: aynen / iskelet / yok | Kendi tespiti adayı | "
          "Atıfsız benzerlik | Kaçırılan: okunan yerde aday / yalnız okunmayanda | Kapsam adayı |",
          "|---|---:|---:|---|---|---:|---|---:|---:|---|---:|"]
    for n, r in results.items():
        nm = r["numaralar"]
        bad = len(nm["metinde_kaynakcada_yok"]) + len(nm["metinde_cite_yok"])
        t = r["tirnak"]
        ar = [x for x in t if x["tur"] in ("satir_ici", "blok") and x["dil"] == "ar"]
        tr = [x for x in t if x["tur"] == "satir_ici" and x["dil"] == "tr"]
        c = Counter(x["durum"] for x in ar)
        ar_nis = sum(1 for x in ar if x["durum"] == "bulunmadi" and x.get("nisbet"))
        tr_no = [x for x in tr if x["durum"] == "bulunmadi"]
        ay = Counter(x["durum"] for x in t if x["tur"] == "ayet")
        ov = Counter(x["tur"] for x in r["ortak"])
        hints = r["ipucu"]
        strong_read = sum(1 for h in hints if h["adaylar"] and h["adaylar"][0]["okundu"])
        only_unread = sum(1 for h in hints if h["adaylar"] and not any(a["okundu"] for a in h["adaylar"]))
        L.append(f"| {n} | {r['okunan']} | {bad} | {c['kaynakta']} / {c['okunan'] + c['ayet']} / {c['bulunmadi']} "
                 f"({ar_nis}) | {len(tr_no)} ({sum(1 for x in tr_no if x.get('nisbet'))}) | "
                 f"{sum(1 for x in t if x['tur'] == 'blok_damgasiz')} | {ay['aynen']} / {ay['iskelet']} / "
                 f"{ay['bulunmadi']} | {ov['kendi_tespiti']} | {ov['atifsiz']} | {strong_read} / {only_unread} "
                 f"(toplam {len(hints)}) | {len(r.get('kapsam', []))} |")
    L += ["", "Nisbetli: tırnağın ardından aynı cümlede kaynak numarası geliyor (söz o kaynağa mal ediliyor). Kapsam "
          "adayı: \"kendi tespiti\" işaretli cümlede inhisar ya da mutlaklık kalıbı (tabiatıyla, ancak, hiç, \"X değil Y'dir\"…; "
          "D6'nın dersi), hüküm değil.", ""]
    for n, r in results.items():
        L += [f"## Taslak {n}", ""]
        if r.get("kapsam"):
            L += ["### Kapsam adayları", ""] + [f"- `{x['capa']}` ({x['kalip']}): {_s(x['cumle'], 200)}" for x in r["kapsam"]] + [""]
        nm = r["numaralar"]
        if nm["metinde_kaynakcada_yok"] or nm["metinde_cite_yok"] or nm["kaynakcada_kullanilmayan"]:
            L.append(f"- Numaralar: metinde olup kaynakçada olmayan {nm['metinde_kaynakcada_yok'] or '—'}, cite'ta "
                     f"olmayan {nm['metinde_cite_yok'] or '—'}, kaynakçada olup kullanılmayan "
                     f"{nm['kaynakcada_kullanilmayan'] or '—'}")
            L.append("")
        tk = [x for x in r["tirnak"] if x["tur"] == "takdir"]
        if tk:
            L += [f"### Takdir işareti «…» ({len(tk)})", ""] + [f"- `{x['capa']}` «{_s(x['soz'], 120)}»" for x in tk] + [""]
        bad = [x for x in r["tirnak"] if x["durum"] == "bulunmadi" and x["tur"] != "ayet"]
        nis = [x for x in bad if x["dil"] == "ar" and (x.get("nisbet") or x["tur"] == "blok")]
        if nis:
            L += ["### Kaynağa nisbet edilip okunan metinde bulunmayan Arapça söz", ""]
            L += [f"- `{x['capa']}` «{_s(x['soz'])}»" for x in nis] + [""]
        ar_own = [x for x in bad if x["dil"] == "ar" and x not in nis]
        if ar_own:
            L += [f"### Tırnak içinde kendi Arapça sözü ({len(ar_own)}; usule uygun olabilir: soru, takdir)", ""]
            L += [f"- `{x['capa']}` «{_s(x['soz'], 120)}»" for x in ar_own] + [""]
        tr_own = [x for x in bad if x["dil"] == "tr"]
        if tr_own:
            L += [f"### Tırnak içinde kendi Türkçesi ({len(tr_own)}; ✱ ardından kaynak numarası)", ""]
            L += [f"- `{x['capa']}`{' ✱' if x.get('nisbet') else ''} «{_s(x['soz'], 120)}»" for x in tr_own] + [""]
        ay = [x for x in r["tirnak"] if x["tur"] == "ayet" and x["durum"] != "aynen"]
        if ay:
            L += ["### Âyet lafzı araçlardan dönen metinle harf harf aynı değil", ""]
            L += [f"- `{x['capa']}` ﴿{_s(x['soz'], 100)}﴾ ({x['durum']})" for x in ay] + [""]
        own = [x for x in r["ortak"] if x["tur"] == "kendi_tespiti"]
        if own:
            L += ["### \"Kendi tespiti\" denen paragrafta okunan kaynakla ortak söz (aday)", ""]
            for x in own:
                L.append(f"- `{x['capa']}` {_s(x['cumle'], 140)}  \n  ↔ `{x['kaynak']}`"
                         f"{' [' + x['kaynak_no'] + ']' if x['kaynak_no'] else ' (kaynakçada yok)'} · ortak: "
                         + "; ".join(x["ortak"][:4]))
            L.append("")
        atf = [x for x in r["ortak"] if x["tur"] == "atifsiz"]
        if atf:
            L += [f"### Paragrafın anmadığı okunan kaynakla ortak söz (aday, {len(atf)})", ""]
            for x in atf:
                L.append(f"- `{x['capa']}` {_s(x['cumle'], 140)}  \n  ↔ `{x['kaynak']}`"
                         f"{' [' + x['kaynak_no'] + ']' if x['kaynak_no'] else ' (kaynakçada yok)'} · ortak: "
                         + "; ".join(x["ortak"][:4]))
            L.append("")
        if r["ipucu"]:
            L += ["### Kaçırılan nüktelerin ipucu adayları", "",
                  "Kalemin ayırt edici kelimeleri okunan (●) ve okunmayan (○) yerlerde; puan kelimelerin nadirliğidir.", ""]
            for h in r["ipucu"]:
                L.append(f"- **{h['kalem']}** {_s(h['nukte'], 130)}  \n  anahtar: {' '.join(h['anahtar'])}")
                for a in h["adaylar"]:
                    L.append(f"  - {'●' if a['okundu'] else '○'} `{a['yer']}` ({a['puan']}; {' '.join(a['ortak'])}): "
                             f"{_s(a['metin'], 150)}")
            L.append("")
    path = P.DRAFTS / unit / "d9-mekanik.md"
    path.write_text("\n".join(L).rstrip() + "\n", encoding="utf-8")
    print(path.relative_to(ROOT))


# ---------------------------------------------------------------- D9.2 eleştirmen

ELESTIRI_PROMPT = ROOT / "docs" / "d1" / "elestiri-istemi.md"
CRITIC_SERVERS = {"risale": "genel", "tefsir": "tefsir", "klasik": "klasik", "hadis": "hadis"}
CRITIC_DBS = {"risale": P.GENEL_DB, "tefsir": P.TEFSIR_DB, "klasik": P.DIST_DIR / "klasik" / "risale.db",
              "hadis": P.HADIS_DB}


def critic_mcp(unit: str) -> Path:
    """Eleştirmenin eklentileri: yayındaki profiller, prova veritabanları değil (İşârât gizlenmez)."""
    uv = Path.home() / ".local" / "bin" / "uv"
    servers = {name: {"type": "stdio", "command": str(uv),
                      "args": ["--directory", str(ROOT), "run", "risale-mcp", "--profile", profile]}
               for name, profile in CRITIC_SERVERS.items()}
    path = P.OUT / unit / "mcp-elestiri.json"
    path.write_text(json.dumps({"mcpServers": servers}, indent=2), encoding="utf-8")
    return path


def d7_text(unit: str, n: int) -> str:
    res = json.loads((Y.out_dir(unit) / "sonuc.json").read_text(encoding="utf-8"))
    h = Y.hidden(unit)
    items = {i["id"]: i for i in res["envanter"]["kalemler"]}
    tr = res["taslaklar"].get(f"taslak-{n}")
    if tr is None:
        return "(Bu taslak için D7 eşleştirmesi yok.)"
    L = ["Envanter ve durumlar (İşârât kimlikleri veritabanındaki cümle numaralarıdır):", ""]
    for r in tr["satirlar"]:
        it = items[r["id"]]
        cells = []
        for m, pm in tr["modeller"].items():
            x = pm["nukteler"].get(r["id"]) or {}
            cells.append(f"{m}: {x.get('durum')}" + (f" [{', '.join(x.get('taslak') or [])}]" if x.get("taslak") else ""))
        ids = Y._ids_db(h, (it.get("ar") or []) + (it.get("tr") or []))
        L.append(f"- {r['id']} ({it.get('vecih')}) {it.get('nukte')} · İşârât: {ids} · " + "; ".join(cells))
    L += ["", f"Fazla (envantere bağlanmayan iddialar, {len(tr['fazla'])}):", ""]
    for f in tr["fazla"]:
        L.append(f"- [{', '.join(f.get('taslak') or [])}] {f.get('iddia', '')} (işaret: {f.get('isaret', '')}; "
                 f"okuyucular: {', '.join(f['okuyucular'])}" + (f"; çelişki: {f['celiski']}" if f.get("celiski") else "") + ")")
    return "\n".join(L)


def mekanik_text(unit: str, n: int) -> str:
    path = Y.out_dir(unit) / f"mekanik-taslak-{n}.json"
    if not path.exists():
        return "(D9.1 bu taslak için çalıştırılmadı.)"
    r = json.loads(path.read_text(encoding="utf-8"))
    L = []
    nm = r["numaralar"]
    if nm["metinde_kaynakcada_yok"] or nm["metinde_cite_yok"]:
        L.append(f"- Kaynak numarası sorunu: kaynakçada yok {nm['metinde_kaynakcada_yok']}, cite'ta yok {nm['metinde_cite_yok']}")
    for x in r["tirnak"]:
        if x["durum"] == "bulunmadi" and x["tur"] != "ayet":
            what = ("kaynağa nisbet edilmiş, okunan metinde yok" if x["dil"] == "ar" and (x.get("nisbet") or x["tur"] == "blok")
                    else "kendi Arapça sözü tırnakta" if x["dil"] == "ar" else
                    "kendi Türkçesi tırnakta" + (", ardından kaynak numarası" if x.get("nisbet") else ""))
            L.append(f"- [{x['capa']}] «{_s(x['soz'], 140)}»: {what}")
        elif x["tur"] == "ayet" and x["durum"] != "aynen":
            L.append(f"- [{x['capa']}] âyet lafzı ﴿{_s(x['soz'], 80)}﴾: {x['durum']}")
    for x in r["ortak"]:
        what = "\"kendi tespiti\" denen yerde" if x["tur"] == "kendi_tespiti" else "paragrafın anmadığı"
        L.append(f"- [{x['capa']}] {what} okunan kaynakla ortak söz: `{x['kaynak'].split(':', 1)[1]}` "
                 f"({'; '.join(x['ortak'][:3])}): {_s(x['cumle'], 120)}")
    for x in r.get("kapsam", []):
        L.append(f"- [{x['capa']}] kapsam adayı ({x['kalip']}): {_s(x['cumle'], 160)}")
    for h in r["ipucu"]:
        cands = "; ".join(f"{'●' if a['okundu'] else '○'} `{a['yer'].split(':', 1)[1]}` ({' '.join(a['ortak'])})"
                          for a in h["adaylar"]) or "aday yok"
        L.append(f"- İpucu adayı {h['kalem']}: {cands}")
    return "\n".join(L) or "(Bulgu yok.)"


def critic_prompt(unit: str, n: int) -> tuple[str, str]:
    raw = ELESTIRI_PROMPT.read_text(encoding="utf-8")
    body = re.split(r"^---- ELESTIRI ----$", raw, maxsplit=1, flags=re.M)[1].strip()
    cfg = P.UNITS[unit]
    meta = json.loads((P.DRAFTS / unit / f"taslak-{n}.json").read_text(encoding="utf-8"))
    ar = next(x for x in cfg["nodes"] if x.startswith("isaratul-icaz-arabi/"))
    tr = next(x for x in cfg["nodes"] if x.startswith("isaratul-icaz/"))
    blocks, sources = Y.draft_blocks(unit, n)
    stamped = {x["tr"] for x in draft(unit, n)["pairs"] if x.get("stamped")}
    # damga taslakta tercüme paragrafının başındadır; `draft_blocks` onu atar, eleştirmen görmeli (v1'in hatası)
    blocks = [(a, lang, q, (STAMP + " " + t) if a in stamped else t) for a, lang, q, t in blocks]
    text = body.format(sura_name=cfg["sura_name"], ayahs="–".join(map(str, cfg["ayahs"])), gizli_ar=ar, gizli_tr=tr,
                       klasik_not=", belâgat ve terim eserlerini" if P.uses_klasik(meta.get("istem")) else "",
                       d7=d7_text(unit, n), mekanik=mekanik_text(unit, n))
    text += "\n\n# Taslak\n\nHer paragrafın başında okuma sayfasındaki çapası var (`V3/ar/5`: üçüncü vecih, Arapça, " \
            "6. paragraf; `V3/tr/5` onun tercümesi).\n\n" + Y.render_draft(blocks, sources)
    return text, P._sha(raw)


def run_critic(unit: str, n: int, model: str, again: bool) -> None:
    import os, subprocess, tempfile, time
    from datetime import datetime
    stem = Y.out_dir(unit) / f"elestiri-taslak-{n}"
    if stem.with_suffix(".json").exists() and not again:
        print(f"{stem.name}: var (--yeniden ile yeniden)")
        return
    prompt, sha = critic_prompt(unit, n)
    mcp = critic_mcp(unit)
    env = {k: v for k, v in os.environ.items() if k not in P.PARENT_ENV}
    command = ["claude", "-p", "--model", Y.MODELS[model], "--effort", Y.EFFORT, "--output-format", "stream-json",
               "--verbose", "--mcp-config", str(mcp), "--strict-mcp-config", "--tools", "",
               "--allowedTools", ",".join(f"mcp__{s}" for s in CRITIC_SERVERS), "--no-session-persistence"]
    started = time.monotonic()
    print(f"{stem.name}: {Y.MODELS[model]} ({datetime.now():%H:%M})", flush=True)
    with tempfile.TemporaryDirectory(prefix="d1-elestiri-") as tmp, stem.with_suffix(".jsonl").open("w") as log:
        done = subprocess.run(command, input=prompt, cwd=tmp, env=env, stdout=log, stderr=subprocess.PIPE, text=True,
                              timeout=Y.TIMEOUT, check=False)
    answer, calls, cost = P.transcript(stem.with_suffix(".jsonl"))
    data = Y.extract_json(answer)
    meta = {"model": Y.MODELS[model], "effort": Y.EFFORT, "istem_sha": sha, "taslak": n,
            "seconds": round(time.monotonic() - started), "returncode": done.returncode, "calls": calls,
            "cost_usd": cost, "at": datetime.now().isoformat(), "prompt_chars": len(prompt), "parsed": data is not None}
    if done.stderr.strip():
        meta["stderr"] = done.stderr.strip()[-2000:]
    stem.with_suffix(".meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    if data is None:
        stem.with_suffix(".cevap.txt").write_text(answer, encoding="utf-8")
        print(f"  {stem.name}: JSON ayrıştırılamadı ({meta['seconds']} sn)", flush=True)
        return
    stem.with_suffix(".json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  {stem.name}: {meta['seconds']} sn, {sum(calls.values())} araç çağrısı, {len(data.get('notlar', []))} not"
          + (f", ≈{cost:.2f} $" if cost else ""), flush=True)


def elestir(unit: str, drafts: list[int], model: str, parallel: int, again: bool) -> None:
    critic_mcp(unit)
    with ThreadPoolExecutor(max_workers=parallel) as pool:
        list(pool.map(lambda n: run_critic(unit, n, model, again), drafts))
    rapor(unit)


def _exists(server: str, sid: str, conns: dict) -> bool:
    db = CRITIC_DBS.get(server)
    if db is None or not db.exists():
        return False
    if db not in conns:
        conns[db] = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    conn = conns[db]
    first = sid.partition("..")[0]
    for table in ("sentences", "nodes", "lib_units"):
        try:
            if conn.execute(f"SELECT 1 FROM {table} WHERE id = ?", (first,)).fetchone():
                return True
        except sqlite3.Error:
            continue
    return False


def check_critic(unit: str, n: int, data: dict) -> dict:
    """Her not: taslak alıntısı çapasında mı, dayanaklar veritabanında ve eleştirmenin okuduklarında mı."""
    blocks, _ = Y.draft_blocks(unit, n)
    by_anchor = {a: t for a, _, _, t in blocks}
    pr = Y.pairs(blocks)
    whole = " ".join(by_anchor.values())
    read = Read(log=Y.out_dir(unit) / f"elestiri-taslak-{n}.jsonl")
    read_ids = {k[1] for k in read.items}
    conns: dict = {}
    for note in data.get("notlar", []):
        q, capa = note.get("taslak_alinti"), note.get("capa") or "genel"
        d = {}
        if q:
            pair = [by_anchor.get(capa, ""), by_anchor.get(pr.get(capa, ""), "")]
            d["alinti"] = Y.quote_found(q, " ".join(pair)) or ("baska_capada" if Y.quote_found(q, whole) else False)
        if capa != "genel":
            d["capa"] = capa in by_anchor
        bad, unread = [], []
        for sid in note.get("dayanak") or []:
            server = next((s for s, db in (("risale", "isaratul"), ) if sid.startswith(db)), None)
            found = any(_exists(s, sid, conns) for s in ([server] if server else CRITIC_DBS))
            if not found:
                bad.append(sid)
            elif not any(x == sid.partition("..")[0] or x.startswith(sid.partition("..")[0] + "#") for x in read_ids):
                unread.append(sid)
        d["dayanak_yok"] = bad
        d["dayanak_okunmamis"] = unread
        note["denetim"] = d
    return data


# ---------------------------------------------------------------- D6.2 bilirkişi örneklemi

BK_SIZE = 24
BK_PER_DRAFT = 4
# kullanıcının kararı (2026-11-14): 24 iddia, taslak başına 4; riskli olana ağırlık; itiraz edilen paragraftan 4
# (eleştirmenin itirazına ters yoklama); B kısmı (D9.3'te "ehline sor" denen notlar) ayrı sayılır
BK_STRATA = [("itiraz", 4), ("dil", 4), ("belagat_kaynakli", 6), ("belagat_kendi", 10)]
BK_OBJECT = {"yanlis", "belagat", "irab", "kaynak", "uydurma", "fazla"}
BK_VERDICT = {"dogru": "doğru", "yanlis": "yanlış", "emin_degilim": "emin değilim"}
BK_BASIS = {"kaynak": "kaynak", "kisi": "kişi", "kanaat": "kendi kanaati", "yz": "yapay zekâ"}


def _claim(text: str, start: int, prev_end: int) -> str:
    """İşaretin önündeki iddia: işaretin cümlesinin başından işarete kadar (aynı cümledeki önceki işaretler atılır)."""
    head = text[:start]
    cut = max(head.rfind(". "), head.rfind("? "), head.rfind("! "))
    return MARK.sub("", head[cut + 2 if cut >= 0 else 0:]).strip(" `;,")


def claims(unit: str, n: int) -> list[dict]:
    """Taslağın `[dil]` ve `[belâgat]` iddiaları: tercüme paragrafındaki her işaret bir iddia."""
    blocks, sources = Y.draft_blocks(unit, n)
    by = {a: t for a, _, _, t in blocks}
    pr = Y.pairs(blocks)
    ids = P.draft_sources(P.DRAFTS / unit / f"taslak-{n}.jsonl")
    crit_path = Y.out_dir(unit) / f"elestiri-taslak-{n}.denetim.json"
    crit = json.loads(crit_path.read_text(encoding="utf-8"))["notlar"] if crit_path.exists() else []
    objected: dict[str, list[str]] = defaultdict(list)
    for x in crit:
        if x.get("tur") in BK_OBJECT or x.get("ehline_sor"):
            objected[Y.tr_of(pr, x.get("capa") or "") or (x.get("capa") or "")].append(Y.critic_key(n, x))
    out = []
    for anchor, lang, quote, text in blocks:
        if lang != "tr" or quote:
            continue
        prev = 0
        for m in MARK.finditer(text):
            body = m.group(1)
            kind = "dil" if body.startswith("dil") else "belagat" if body.startswith("belâgat") else None
            if kind:
                nums = re.findall(r"\d+", body.split("burada")[0])
                out.append({"taslak": f"taslak-{n}", "capa": anchor, "ar_capa": Y.ar_of(pr, anchor),
                            "tur": kind, "kaynak": "kendi" if "kendi tespiti" in body or "istinbat" in body else "kaynakli",
                            "isaret": body, "iddia": _claim(text, m.start(), prev), "tercume": MARK.sub("", text),
                            "arapca": MARK.sub("", by.get(pr.get(anchor, ""), "")),
                            "kaynaklar": [{"no": k, "atif": sources.get(k, ""), "id": (ids.get(k) or (None, None))[1],
                                           "sunucu": (ids.get(k) or (None, None))[0]} for k in nums],
                            "itiraz": objected.get(anchor, [])})
            prev = m.end()
    return out


def _stratum(c: dict) -> str:
    if c["itiraz"]:
        return "itiraz"
    if c["tur"] == "dil":
        return "dil"
    return "belagat_kendi" if c["kaynak"] == "kendi" else "belagat_kaynakli"


def bilirkisi(unit: str, again: bool = False) -> None:
    """D6.2 A kısmı: sabit örneklem `yz/bilirkisi-A.json` (var olan, --yeniden verilmedikçe korunur)."""
    import random
    path = Y.out_dir(unit) / "bilirkisi-A.json"
    if path.exists() and not again:
        print(f"{path.relative_to(ROOT)} var; korunuyor (--yeniden ile yeniden çekilir)")
        return
    pool: dict[str, list[dict]] = defaultdict(list)
    for n in Y.drafts_of(unit):
        for c in claims(unit, n):
            pool[_stratum(c)].append(c)
    rng = random.Random(f"d6-{unit}-A")
    for name, items in pool.items():
        rng.shuffle(items)
        if name == "dil":                       # dil ve kendi tespiti az: önce onlardan iki tane
            items.sort(key=lambda c: c["kaynak"] != "kendi")
    per_draft, used, picked = Counter(), set(), []
    for name, target in BK_STRATA:
        got, kendi_dil = 0, 0
        while got < target:
            cands = [c for c in pool[name] if per_draft[c["taslak"]] < BK_PER_DRAFT
                     and (c["taslak"], c["capa"]) not in used
                     and not (name == "dil" and c["kaynak"] == "kendi" and kendi_dil >= 2)]
            if not cands:
                break
            low = min(per_draft[c["taslak"]] for c in cands)
            c = next(c for c in cands if per_draft[c["taslak"]] == low)
            pool[name].remove(c)
            per_draft[c["taslak"]] += 1
            used.add((c["taslak"], c["capa"]))
            kendi_dil += name == "dil" and c["kaynak"] == "kendi"
            picked.append({**c, "tabaka": name})
            got += 1
    texts = P.SourceTexts(unit)
    picked.sort(key=lambda c: (int(c["taslak"].split("-")[1]), Y._anchor_order([c["capa"]])))
    for i, c in enumerate(picked, 1):
        c["id"] = f"A{i:02d}"
        for k in c["kaynaklar"]:
            k["metin"] = texts.text(k["sunucu"], k["id"], k["atif"])
    data = {"birim": unit, "kisim": "A", "at": datetime.now().isoformat(timespec="seconds"),
            "tabakalar": dict(BK_STRATA), "havuz": {k: len(v) + sum(1 for c in picked if c["tabaka"] == k)
                                                    for k, v in pool.items()}, "maddeler": picked}
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{path.relative_to(ROOT)}: {len(picked)} madde · " +
          ", ".join(f"{k} {sum(1 for c in picked if c['tabaka'] == k)}" for k, _ in BK_STRATA) + " · taslak başına " +
          ", ".join(f"{t.split('-')[1]}:{v}" for t, v in sorted(per_draft.items(), key=lambda kv: int(kv[0].split('-')[1]))))


def bilirkisi_b(unit: str) -> None:
    """D6.2 B kısmı: D9.3'te "ehline sor" denen eleştirmen notları (ayrı sayılır). Süzgeç değiştikçe yeniden kurulur."""
    decisions = suzgec(unit)
    items = []
    for n in Y.drafts_of(unit):
        path = Y.out_dir(unit) / f"elestiri-taslak-{n}.denetim.json"
        if not path.exists():
            continue
        blocks, _ = Y.draft_blocks(unit, n)
        by = {a: t for a, _, _, t in blocks}
        pr = Y.pairs(blocks)
        for x in json.loads(path.read_text(encoding="utf-8"))["notlar"]:
            key = Y.critic_key(n, x)
            if (decisions.get(f"{unit}|taslak-{n}|{key}") or {}).get("v") != "ehline":
                continue
            capa = x.get("capa") or "genel"
            items.append({"id": f"B{len(items) + 1:02d}", "taslak": f"taslak-{n}", "capa": capa, "not_anahtari": key,
                          "tur": x.get("tur"), "elestiri": x.get("metin", ""), "soru": x.get("soru"),
                          "dayanak": x.get("dayanak") or [],
                          "arapca": MARK.sub("", by.get(Y.ar_of(pr, capa), "")),
                          "tercume": MARK.sub("", by.get(Y.tr_of(pr, capa) or "", ""))})
    path = Y.out_dir(unit) / "bilirkisi-B.json"
    path.write_text(json.dumps({"birim": unit, "kisim": "B", "at": datetime.now().isoformat(timespec="seconds"),
                                "maddeler": items}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{path.relative_to(ROOT)}: {len(items)} madde (D9.3'te \"ehline sor\" denenler)")


def exported(unit: str, field: str) -> dict[str, dict]:
    """Dışa aktarımlardaki bir alan (`yz_suzgec`, `bilirkisi`): anahtar başına en yenisi."""
    out: dict[str, dict] = {}
    for f in sorted(P.NOTES_DIR.glob("*.json")) if P.NOTES_DIR.exists() else []:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        for k, v in (data.get(field) or {}).items():
            if k.startswith(unit + "|") and (k not in out or v.get("at", "") > out[k].get("at", "")):
                out[k] = v
    return out


def bilirkisi_rapor(unit: str) -> list[str]:
    marks = exported(unit, "bilirkisi")
    L = ["# D6.2 bilirkişi okuması", "",
         "Hüküm kullanıcınındır; dayanağı yapay zekâ olan hüküm \"emin değilim\" sayılır (PLANLAR.md D6.2). A: "
         "eleştirmenin itiraz etmediği dil ve belâgat iddiaları (ve ters yoklama için itiraz edilen paragraftan 4); "
         "B: D9.3'te \"ehline sor\" denen notlar. İki kısım ayrı sayılır.", ""]
    for part in ("A", "B"):
        path = Y.out_dir(unit) / f"bilirkisi-{part}.json"
        if not path.exists():
            continue
        items = json.loads(path.read_text(encoding="utf-8"))["maddeler"]
        qpath = path.with_name(f"bilirkisi-{part}-sorular.json")
        questions = json.loads(qpath.read_text(encoding="utf-8"))["sorular"] if qpath.exists() else {}
        got = {i["id"]: marks.get(f"{unit}|{part}|{i['id']}") for i in items}
        verdict = Counter((("emin_degilim" if (m or {}).get("dt") == "yz" else (m or {}).get("v")) or "—")
                          for m in got.values())
        basis = Counter(((m or {}).get("dt") or "—") for m in got.values() if m)
        L += [f"## {part} kısmı ({len(items)} madde)", "",
              "Hüküm: " + ", ".join(f"{BK_VERDICT.get(k, 'işaretsiz')} {v}" for k, v in verdict.most_common()),
              "Dayanak: " + (", ".join(f"{BK_BASIS.get(k, k)} {v}" for k, v in basis.most_common()) or "—"), ""]
        if part == "A":
            by = defaultdict(Counter)
            for i in items:
                m = got[i["id"]] or {}
                by[i["tabaka"]][("emin_degilim" if m.get("dt") == "yz" else m.get("v")) or "—"] += 1
            L += ["| Tabaka | " + " | ".join(BK_VERDICT.values()) + " | işaretsiz |", "|---|---:|---:|---:|---:|"]
            for name, _ in BK_STRATA:
                c = by[name]
                L.append(f"| {name} | " + " | ".join(str(c[k]) for k in BK_VERDICT) + f" | {c['—']} |")
            L.append("")
        for i in items:
            m = got[i["id"]]
            if not m:
                continue
            v = "emin_degilim" if m.get("dt") == "yz" else m.get("v")
            L.append(f"- **{i['id']}** {i['taslak']} `{i['capa']}` · {BK_VERDICT.get(v, '?')} · dayanak "
                     f"{BK_BASIS.get(m.get('dt'), '—')}{': ' + m['d'] if m.get('d') else ''}  \n  "
                     + (f"_Soru:_ {questions[i['id']]}  \n  " if questions.get(i["id"]) else "")
                     + f"{_s(i.get('iddia') or i.get('elestiri') or '', 200)}" + (f"  \n  _Not:_ {m['n']}" if m.get("n") else ""))
        L.append("")
    return L


# D9.3 süzgeç örneklemi (kullanıcının kararı, 2026-11-14): notların hepsi değil, eleştirmenin en çok zarar verebileceği
# türlerden 10 not; övgü ("dogru") ve "ehline sor" notları girmez (övgünün kör noktası D6'nın işiydi, "ehline sor"
# doğrudan heyete gider). Yanında eleştirmenin `sistemli` listelerinden toplanan başlıklar (`elestiri-sistemli.json`,
# elle) süzülür: D8'in istemi onlardan yazılır.
CRITIC_STRATA = [("itiraz", ("yanlis", "fazla"), 3), ("kaynak", ("kaynak",), 2), ("belagat", ("belagat", "irab"), 2),
                 ("eksik", ("eksik",), 2), ("usul", ("usul",), 1)]
CRITIC_PER_DRAFT = 2


def orneklem(unit: str, again: bool = False) -> None:
    import random
    path = Y.out_dir(unit) / "elestiri-orneklem.json"
    if path.exists() and not again:
        print(f"{path.relative_to(ROOT)} var; korunuyor (--yeniden ile yeniden çekilir)")
        return
    pool: dict[str, list[dict]] = defaultdict(list)
    for n in Y.drafts_of(unit):
        dpath = Y.out_dir(unit) / f"elestiri-taslak-{n}.denetim.json"
        if not dpath.exists():
            continue
        for i, x in enumerate(json.loads(dpath.read_text(encoding="utf-8"))["notlar"]):
            if x.get("ehline_sor") or x.get("denetim", {}).get("alinti") is False:
                continue
            for name, types, _ in CRITIC_STRATA:
                if x.get("tur") in types:
                    pool[name].append({"taslak": f"taslak-{n}", "k": Y.critic_key(n, x), "sira": i, "tur": x.get("tur"),
                                       "capa": x.get("capa"), "metin": x.get("metin", "")})
    rng = random.Random(f"d9-{unit}-suzgec")
    for xs in pool.values():
        rng.shuffle(xs)
    per_draft, picked = Counter(), []
    for name, _, target in CRITIC_STRATA:
        got = 0
        while got < target:
            cands = [c for c in pool[name] if per_draft[c["taslak"]] < CRITIC_PER_DRAFT]
            if not cands:
                break
            low = min(per_draft[c["taslak"]] for c in cands)   # taslaklara yay: en az not alan taslaktan
            c = next(c for c in cands if per_draft[c["taslak"]] == low)
            pool[name].remove(c)
            per_draft[c["taslak"]] += 1
            picked.append({**c, "tabaka": name})
            got += 1
    picked.sort(key=lambda c: (int(c["taslak"].split("-")[1]), c["sira"]))
    data = {"birim": unit, "at": datetime.now().isoformat(timespec="seconds"),
            "tabakalar": {n: t for n, _, t in CRITIC_STRATA}, "havuz": {k: len(v) for k, v in pool.items()},
            "notlar": picked}
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{path.relative_to(ROOT)}: {len(picked)} not · " + ", ".join(f"{c['taslak']} {c['tur']}" for c in picked))


def suzgec_lines(unit: str, decisions: dict) -> list[str]:
    """D9.3 örneklemi ve sistemli başlıklar: kullanıcının kararları."""
    d = Y.out_dir(unit)
    L: list[str] = []
    sp = d / "elestiri-orneklem.json"
    if sp.exists():
        xs = json.loads(sp.read_text(encoding="utf-8"))["notlar"]
        got = {x["k"]: (decisions.get(f"{unit}|{x['taslak']}|{x['k']}") or {}).get("v") for x in xs}
        c = Counter(v or "—" for v in got.values())
        judged = c["kalsin"] + c["atilsin"]
        L += ["## Süzgeç örneklemi (D9.3)", "",
              f"{len(xs)} not (övgü ve \"ehline sor\" dışında, türlere göre katmanlı, sabit tohum). Karar: kalsın {c['kalsin']}, "
              f"atılsın {c['atilsin']}, ehline sor {c['ehline']}, işaretsiz {c['—']}"
              + (f"; kabul {c['kalsin']}/{judged} (%{c['kalsin'] / judged * 100:.0f})" if judged else "") + ".", ""]
        for x in xs:
            v = got[x["k"]]
            L.append(f"- {x['taslak']} `{x['capa']}` **{x['tur']}** → {SUZ_TR.get(v, 'işaretsiz')}: {_s(x['metin'], 220)}")
        L.append("")
    zp = d / "elestiri-sistemli.json"
    if zp.exists():
        z = json.loads(zp.read_text(encoding="utf-8"))
        L += ["## Sistemli başlıklar (D9.3)", "",
              "Eleştirmenin altı taslaktaki `sistemli` listelerinden en az iki taslakta geçenler (`yz/elestiri-sistemli.json`). "
              "D8'in istemi \"kalsın\" denenlerden yazılır.", ""]
        for b in z["basliklar"]:
            v = (decisions.get(f"{unit}|sistemli|{b['id']}") or {}).get("v")
            L.append(f"- **{b['id']} {b['baslik']}** ({b['tur']}; {len(b['dayanak'])} taslak) → {SUZ_TR.get(v, 'işaretsiz')}")
        L.append("")
    return L


SUZ_TR = {"kalsin": "kalsın", "atilsin": "atılsın", "ehline": "ehline sor"}


def suzgec(unit: str) -> dict[str, dict]:
    """D9.3 kararları: `data/d1/notlar/` altındaki dışa aktarımlardan (`yz_suzgec`), anahtar başına en yenisi."""
    return exported(unit, "yz_suzgec")


def rapor(unit: str) -> None:
    d = Y.out_dir(unit)
    decisions = suzgec(unit)
    L = [f"# Prova {unit}: D9.2 yapay zekâ eleştirmeni", "",
         f"`uv run python scripts/d1-elestiri.py elestir {unit}` üretir (istem `docs/d1/elestiri-istemi.md`). Notlar "
         "eleştirmenindir, hüküm değil: süzgeç kullanıcıdadır (D9.3). Denetim: ✓ taslak alıntısı çapasında, "
         "↷ başka çapada, ✗ taslakta yok; dayanak ✗ veritabanında yok, ◌ eleştirmen o oturumda okumamış. Süzgeç "
         "kararları `data/d1/notlar/` altındaki dışa aktarımlardan (`scripts/d1-prova.py notlar <dosya>`); kabul "
         "oranı kalsın / (kalsın + atılsın), eleştirmenin isabet ölçüsüdür.", ""]
    rows, bodies = [], []
    for path in sorted(d.glob("elestiri-taslak-*.json"), key=lambda p: int(re.search(r"(\d+)", p.stem).group(1))):
        if not re.fullmatch(r"elestiri-taslak-\d+\.json", path.name):
            continue
        n = int(re.search(r"taslak-(\d+)", path.stem).group(1))
        data = check_critic(unit, n, json.loads(path.read_text(encoding="utf-8")))
        path.with_name(f"elestiri-taslak-{n}.denetim.json").write_text(json.dumps(data, ensure_ascii=False, indent=1),
                                                                       encoding="utf-8")
        meta = json.loads(path.with_suffix(".meta.json").read_text(encoding="utf-8"))
        notes = data.get("notlar", [])
        types = Counter(x.get("tur") for x in notes)
        bad_q = sum(1 for x in notes if x["denetim"].get("alinti") is False)
        bad_id = sum(len(x["denetim"]["dayanak_yok"]) for x in notes)
        unread = sum(len(x["denetim"]["dayanak_okunmamis"]) for x in notes)
        dec = Counter((decisions.get(f"{unit}|taslak-{n}|{Y.critic_key(n, x)}") or {}).get("v") for x in notes)
        judged = dec["kalsin"] + dec["atilsin"]
        rate = f"{dec['kalsin']}/{judged} (%{dec['kalsin'] / judged * 100:.0f})" if judged else "—"
        rows.append(f"| {n} | {len(notes)} | " + ", ".join(f"{k} {v}" for k, v in types.most_common()) +
                    f" | {sum(1 for x in notes if x.get('ehline_sor'))} | {bad_q} | {bad_id} / {unread} | "
                    f"{sum(meta['calls'].values())} | {meta['seconds'] // 60} dk | {rate} · ehline {dec['ehline']} |")
        B = [f"## Taslak {n}", "", f"**Özet:** {data.get('ozet', '')}", ""]
        for x in notes:
            dn = x["denetim"]
            mark = {True: "✓", False: "✗", "baska_capada": "↷"}.get(dn.get("alinti"), "")
            ids = ", ".join(("✗ " if s in dn["dayanak_yok"] else "◌ " if s in dn["dayanak_okunmamis"] else "") + f"`{s}`"
                            for s in x.get("dayanak") or [])
            v = (decisions.get(f"{unit}|taslak-{n}|{Y.critic_key(n, x)}") or {}).get("v")
            B.append(f"- **{x.get('tur')}** `{x.get('capa')}`" + (f" [{ {'kalsin': 'kalsın', 'atilsin': 'atılsın', 'ehline': 'ehline sor'}.get(v, v)}]" if v else "") + (f" {x['nukte']}" if x.get("nukte") else "") +
                     (" · ehline sor" if x.get("ehline_sor") else "") + f" {mark}  \n  {x.get('metin', '')}")
            if x.get("nasil"):
                B.append(f"  _Nasıl:_ {x['nasil']}")
            if x.get("soru"):
                B.append(f"  _Soru:_ {x['soru']}")
            if ids:
                B.append(f"  Dayanak: {ids}")
        if data.get("sistemli"):
            B += ["", "**Sistemli zaaflar:**", ""] + [f"- ({s.get('tur')}) {s.get('metin')} "
                                                       f"[{', '.join(s.get('capalar') or [])}]" for s in data["sistemli"]]
        if data.get("oneriler"):
            B += ["", "**Öneriler:**", ""] + [f"- {o}" for o in data["oneriler"]]
        bodies += B + [""]
    L += ["| Taslak | Not | Türler | Ehline sor | Alıntı bulunmadı | Dayanak yok / okunmamış | Araç çağrısı | Süre | "
          "Süzgeç: kalsın / karar (kabul) |",
          "|---|---:|---|---:|---:|---|---:|---:|---|"] + rows + [""] + suzgec_lines(unit, decisions) + bodies
    out = P.DRAFTS / unit / "d9-elestiri.md"
    out.write_text("\n".join(L).rstrip() + "\n", encoding="utf-8")
    print(out.relative_to(ROOT))
    if (d / "bilirkisi-A.json").exists():
        out = P.DRAFTS / unit / "d6-bilirkisi.md"
        out.write_text("\n".join(bilirkisi_rapor(unit)).rstrip() + "\n", encoding="utf-8")
        print(out.relative_to(ROOT))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("mekanik")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--taslak", type=int, nargs="*")
    p = sub.add_parser("elestir")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--taslak", type=int, nargs="*")
    p.add_argument("--model", choices=Y.MODELS, default="opus")
    p.add_argument("--paralel", type=int, default=3)
    p.add_argument("--yeniden", action="store_true")
    p = sub.add_parser("istem", help="eleştirmenin istemini dosyaya yaz (model çağırmadan)")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--taslak", type=int, default=1)
    p = sub.add_parser("rapor")
    p.add_argument("unit", choices=P.UNITS)
    p = sub.add_parser("bilirkisi", help="D6.2 örneklemi: A (sabit) ya da B (D9.3'ün \"ehline sor\" notları)")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--kisim", choices=["A", "B"], default="A")
    p.add_argument("--yeniden", action="store_true", help="A'yı yeniden çek (işaretler kimliğe bağlıdır)")
    p = sub.add_parser("orneklem", help="D9.3 süzgeç örneklemi (10 not, sabit tohum)")
    p.add_argument("unit", choices=P.UNITS)
    p.add_argument("--yeniden", action="store_true")
    args = parser.parse_args()
    if args.command == "mekanik":
        mekanik(args.unit, args.taslak or Y.drafts_of(args.unit))
    elif args.command == "elestir":
        elestir(args.unit, args.taslak or Y.drafts_of(args.unit), args.model, args.paralel, args.yeniden)
    elif args.command == "istem":
        text, _ = critic_prompt(args.unit, args.taslak)
        path = P.OUT / args.unit / f"elestiri-istem-taslak-{args.taslak}.md"
        path.write_text(text, encoding="utf-8")
        print(f"{path.relative_to(ROOT)}: {len(text):,} karakter")
    elif args.command == "bilirkisi":
        bilirkisi(args.unit, args.yeniden) if args.kisim == "A" else bilirkisi_b(args.unit)
    elif args.command == "orneklem":
        orneklem(args.unit, args.yeniden)
    else:
        rapor(args.unit)


if __name__ == "__main__":
    main()
