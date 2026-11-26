"""Lügat (A4): risaleoku.com'un Osmanlıca–Türkçe lügatı ve metindeki kelimenin maddesini bulma.

Kaynak (`uv run python -m risale_mcp.fetch lugat`, ham veri `data/raw/risaleoku_app/lugat-tr/`): risaleoku
kataloğunda `kind: dictionary`, `lang: tr` kaydı; dosyalar harf başınadır (`a.txt`, `c1.txt` = ç, `ط.txt`…).

- `x.txt`: her madde "madde=anlam" satırıyla başlar; "2. …" gibi numaralı ya da "=" taşımayan satırlar bir önceki
  maddenin anlamının devamıdır (satır sonuyla birleşir). Aynı madde iki kez yazılmış olabilir: anlamları sırayla
  birleşir.
- `x_f.txt`: "madde=çeşit1,çeşit2:bayrak|…": maddenin başka yazılışları (şapkalı, şapkasız, kesmeli) ve bayrak.
  Bayrak 1 kısa ya da başka kelimelerin başında sıkça geçen maddelerdedir ("âl", "as", "âtıl", "âyâ"): bunlar ek
  atılarak eşlenmez, yalnız kelimenin kendisi olarak (bizim yorumumuz; uygulama belgelenmemiş).

Lügat nâşirindir (sitenin hazırladığı ya da derlediği), müellifin sözü değildir; mealler gibi araçlarda kaynağıyla
gider. Asıl veri `data/library/lugat/risaleoku-tr.json` (`uv run python -m risale_mcp.lugat build`), `build_db`
Risale profillerinde `lugat` tablosuna yükler.

Eşleme (`Lexicon.lookup`), kelime ya da tamlama, metinde yazıldığı gibi:
1. Anahtar `normalize.search_words` biçimidir (şapka, çengel, kesme yok; ı = i), kelimeler boşlukla: "Âb-ı hayat"
   ile "ab-i hayat" aynı anahtara iner. Önce maddenin kendisi ve çeşitleri tam aranır.
2. Bulunmazsa son kelimenin sonundan Türkçe ekler atılır ve en uzun madde alınır ("kâinatın" → "kâinat",
   "hakikatlerini" → "hakikat"). Atılan kısım yalnız bilinen eklerden oluşmalı (`SUFFIX`), kök en az 3 harf.
   Kökün sonu yumuşamış olabilir (b/p, d/t, g/k: "kalbi" → "kalp") ve iki ünsüzle bitiyorsa düşen ünlü geri konur
   ("ilmi" → "ilim", "aklı" → "akıl").
3. Metnin harf biçimi (`Form`) adayları süzer: ş ç ğ ö ü, kesmenin yeri ve ünlüden sonraki ı/i ("sâika" sevk eden,
   "sâıka" yıldırım; S13.16) tutmalı.
Bulunan her şey aday olarak döner (`how`: `exact`, `variant`, `stem`); hüküm vermez.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from risale_mcp.normalize import search_words, tr_lower
from risale_mcp.paths import LIBRARY_DIR, RAW_DIR

LANG = "tr"
LUGAT_PATH = LIBRARY_DIR / "lugat" / f"risaleoku-{LANG}.json"
SOURCE_NAME = "risaleoku.com lügatı"
SOURCE_URL = "https://risaleoku.com"
NOTE = ("A dictionary by the publisher (risaleoku.com), not the author's words. Use it to understand a word; name it "
        "when you give a meaning from it, and never quote it as the text.")

MIN_STEM = 3            # ek atılınca kalan kökün en az harfi
MAX_PHRASE = 6          # tamlama en çok kaç kelime

# Türkçe çekim ekleri ve sık yapım ekleri, `search_words` biçiminde (ı = i, ö = o, ü = u, ş = s, ç = c, ğ = g).
# Atılan kısım bunların art arda gelmesinden oluşmalı.
_SUFFIXES = sorted(set("""
lar ler
m im um n in un i u si su miz imiz umuz niz iniz unuz lari leri
yi yu ni nu a e ya ye na ne da de ta te nda nde dan den tan ten ndan nden nin nun la le yla yle ile
ki dir dur tir tur ca ce siz suz li lu lik luk lig lug se sa yse ysa ken yken cesine casina
""".split()), key=len, reverse=True)
SUFFIX = re.compile(f"(?:{'|'.join(_SUFFIXES)}){{1,5}}")

_SOFT = {"b": "p", "p": "b", "d": "t", "t": "d", "g": "k", "k": "g"}
_VOWELS = set("aeiou")
_LITE_VOWELS = set("aeıioöuü")


def key(text: str) -> str:
    return " ".join(search_words(text))


# Anahtar ş/s, ç/c, ğ/g, ö/o, ü/u ve ı/i farkını, kesmeyi yok sayar: "esrar" ile "eşrar", "şu" ile "şu'", "bir" ile
# "bi'r" aynı anahtara iner. Harflerin metindeki biçimi (`Form`: ş, ç, ğ, ö, ü korunur, ı = i; kesmelerin yeri ayrı)
# adayları ayırır: metinle harfi ya da kesmesi tutmayan madde eşlenmez.
_KEEP_MARKS = {"\u0327", "\u0306", "\u0308", "\u0302"}   # çengel (ş, ç), ğ'nin işareti, ö ve ü'nün noktaları, şapka
_APOS = "'’‘ʼ`"
# Ünlüden sonraki ı ile i (S13.16 (b)): "sâika" (سائقه, sevk eden; hemze) ile "sâıka", "saîka" (صاعقه, yıldırım;
# ayın) Latin harfle aynı anahtara iner. Maddenin yazılışlarında o yerde yalnız ı varsa metindeki i (ya da tersi)
# onunla eşlenmez; "î" iki yana da sayılmaz. Anahtarda ve öbür yerlerde ı = i kalır. Şapkanın yeri ayırıcı değildir:
# lügat şapkaları tutarsız yazar ("ilahî", "İlâhiye").
_HATS = {"â": "a", "î": "i", "û": "u", "ê": "e", "ô": "o"}


@dataclass(frozen=True)
class Form:
    letters: str                 # anahtarla aynı uzunlukta
    apos: frozenset[int]         # kesmelerin yeri (ardından gelen harfin sırası)
    gap_i: frozenset[int] = frozenset()  # ünlüden sonra gelen i ("sâika")
    gap_ı: frozenset[int] = frozenset()  # ünlüden sonra gelen ı ("sâıka")


def form(text: str) -> Form | None:
    """Metnin ya da maddenin harf biçimi; anahtarla harf harf hizalanamazsa None."""
    s = unicodedata.normalize("NFD", tr_lower(text))
    s = "".join(ch for ch in s if not unicodedata.category(ch).startswith("M") or ch in _KEEP_MARKS)
    s = unicodedata.normalize("NFC", s).replace("ـ", "")
    letters, apos, gap_i, gap_ı = [], set(), set(), set()
    for word in re.findall(rf"[\w{_APOS}]+", s):
        if letters:
            letters.append(" ")
        n = len("".join(letters))
        for ch in word:
            if ch in _APOS:
                apos.add(n)
            else:
                if ch in _HATS:
                    ch = _HATS[ch]
                elif ch in "iı":
                    if letters and letters[-1] in "aeiou":
                        (gap_i if ch == "i" else gap_ı).add(n)
                    ch = "i"
                letters.append(ch)
                n += 1
    out = "".join(letters)
    out = " ".join(w for w in out.split(" ") if w)
    return (Form(out, frozenset(apos), frozenset(gap_i), frozenset(gap_ı))
            if len(out) == len(key(text)) else None)


def _gaps_agree(forms: list[Form], text: Form, upto: int) -> bool:
    """Ünlüden sonraki ı/i (ilk `upto` harfte): maddenin yazılışları o yerde yalnız öbür harfi taşıyorsa çatışır."""
    has_i = set().union(*(f.gap_i for f in forms))
    has_ı = set().union(*(f.gap_ı for f in forms))
    return not any(p < upto and ((p in text.gap_i and p in has_ı - has_i) or (p in text.gap_ı and p in has_i - has_ı))
                   for p in text.gap_i | text.gap_ı)


# ------------------------------------------------------------------ ham veriden

_CONTINUATION = re.compile(r"^\s*(\d+\s*[.)-]|[-–•*])")


def parse(texts: dict[str, str]) -> tuple[list[dict], dict]:
    """Ham dosyalardan maddeler (lügat sırasıyla) ve rapor. `texts`: dosya adı -> metin."""
    words: dict[str, dict] = {}
    report = {"lines": 0, "continuations": 0, "duplicates": [], "orphans": [], "without_f": 0, "f_unknown": []}
    for name in sorted(n for n in texts if not n.endswith("_f.txt")):
        last = None
        for line in texts[name].splitlines():
            line = line.strip()
            if not line:
                continue
            report["lines"] += 1
            word, sep, meaning = line.partition("=")
            if not sep or _CONTINUATION.match(line) or not word.strip():
                if last is None:
                    report["orphans"].append(f"{name}: {line[:80]}")
                    continue
                last["meanings"][-1] += "\n" + line
                report["continuations"] += 1
                continue
            word = word.strip()
            if word in words:
                report["duplicates"].append(word)
                if meaning.strip() not in words[word]["meanings"]:      # aynısı birkaç kez yazılmış olabilir
                    words[word]["meanings"].append(meaning.strip())
            else:
                words[word] = {"word": word, "meanings": [meaning.strip()], "variants": [], "exact": False}
            last = words[word]
    for name in sorted(n for n in texts if n.endswith("_f.txt")):
        for item in texts[name].split("|"):
            item = item.strip()
            if not item:
                continue
            head, _, rest = item.partition("=")
            variants, _, flag = rest.rpartition(":")
            entry = words.get(head.strip())
            if entry is None:
                report["f_unknown"].append(head)
                continue
            entry["variants"] = [v.strip() for v in variants.split(",") if v.strip() and v.strip() != entry["word"]]
            entry["exact"] = flag.strip() == "1"
    entries = []
    for i, entry in enumerate(words.values()):
        meaning = "\n".join(m for m in entry["meanings"] if m)
        if not meaning:
            report["orphans"].append(f"anlamsız madde: {entry['word']}")
            continue
        entries.append({"id": i + 1, "word": entry["word"], "meaning": meaning,
                        **({"variants": entry["variants"]} if entry["variants"] else {}),
                        **({"exact": True} if entry["exact"] else {})})
    return entries, report


# ------------------------------------------------------------------ eşleme


@dataclass(frozen=True)
class Match:
    entry: dict
    how: str             # exact | variant | stem
    matched: str         # metinden eşlenen kısım (anahtar biçiminde)
    stem: str | None = None
    form: str | None = None   # ek atılınca aranan biçim: kök, yumuşamışı (kalb -> kalp) ya da ünlüsü geri konmuşu (ilm -> ilim)


# Lügatta sesteşi olan, metinde çok geçen Türkçe kelimeler: maddeye bağlanmaz ("dahi" dâhî değildir, "olan" ola'dan
# değildir, "hasta" has'tan değildir). Anahtar biçiminde; ölçümle bulundu (`lugat olc`).
STOP = frozenset("""
dahi beni benim belki halde birden biri birisi birer birlikte birdir yedi hata geri deki haydi yarim yarin olsa olsun
olan olanlar eden edenler alan kalan bazen bazi bazisi bazilari vardi vardir
""".split())
# Bu Türkçe köklerle başlayan kelime ek atılarak eşlenmez ("güzele" güz'den, "hastalık" has'tan değildir).
STOP_PREFIXES = ("guzel", "hasta", "karanlik", "sevgi", "arkasi", "arasi", "aralari")


class Lexicon:
    def __init__(self, entries: list[dict], source: dict | None = None) -> None:
        self.entries = {e["id"]: e for e in entries}
        self.source = source or {}
        self.heads: dict[str, list[int]] = defaultdict(list)       # anahtar -> madde (kendi yazılışı)
        self.variants: dict[str, list[int]] = defaultdict(list)    # anahtar -> madde (çeşit yazılış)
        self.stems: dict[str, list[int]] = defaultdict(list)       # ek atılarak eşlenebilenler
        self.prefixes: set[str] = set()                            # çok kelimeli maddelerin kelime önekleri
        self.forms: dict[int, list[Form]] = {}
        for e in entries:
            self.forms[e["id"]] = [f for x in [e["word"], *e.get("variants", [])] if (f := form(x))]
            for k, table in [(key(e["word"]), self.heads)] + [(key(v), self.variants) for v in e.get("variants", [])]:
                if not k or e["id"] in table[k]:
                    continue
                table[k].append(e["id"])
                if not e.get("exact") and e["id"] not in self.stems[k]:
                    self.stems[k].append(e["id"])
                parts = k.split(" ")
                for n in range(1, len(parts)):
                    self.prefixes.add(" ".join(parts[:n]))

    @classmethod
    def load(cls, path: Path = LUGAT_PATH) -> "Lexicon":
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(data["entries"], data.get("source"))

    # ---------------------------------------------------------- adaylar (anahtarla)

    def _exact(self, k: str) -> list[Match]:
        out = [Match(self.entries[i], "exact", k) for i in self.heads.get(k, [])]
        seen = {m.entry["id"] for m in out}
        return out + [Match(self.entries[i], "variant", k) for i in self.variants.get(k, []) if i not in seen]

    def _stemmed(self, head: str, last: str, levels_max: int = 2) -> list[Match]:
        """Son kelimeden ek atarak maddeler, en uzun kökten. İlk kök "i" ya da "u" ile bitiyorsa iki ünsüzle biten
        kısası da alınır: o harf ek de olabilir ("sırrıyla": sırrî mi, sırr mı?). `head`: önceki kelimeler (anahtar biçiminde,
        boş olabilir). Yalnız "n" ya da "m" eki atılmaz ("olan" ola'dan, "benim" benî'den değildir)."""
        pre = head + " " if head else ""
        out: list[Match] = []
        levels = 0
        for cut in range(len(last) - 1, MIN_STEM - 1, -1):
            stem, suffix = last[:cut], last[cut:]
            if suffix in ("n", "m") or suffix.startswith("nl") or not SUFFIX.fullmatch(suffix):
                continue
            candidates = [stem]
            if len(stem) > MIN_STEM and stem[-1] in _SOFT and suffix[0] in _VOWELS:     # kalbi -> kalp
                candidates.append(stem[:-1] + _SOFT[stem[-1]])
            if stem[-1] not in _VOWELS and stem[-2] not in _VOWELS and suffix[0] in "iu":   # ilmi -> ilim, ömrü -> ömür
                candidates.append(stem[:-1] + suffix[0] + stem[-1])
            found = [(i, c) for c in candidates for i in self.stems.get(pre + c, [])]
            found = [(i, c) for n, (i, c) in enumerate(found)
                     if all(i != j for j, _ in found[:n]) and all(m.entry["id"] != i for m in out)]
            if found and levels and not (stem[-1] not in _VOWELS and stem[-2] not in _VOWELS):
                continue                  # ikinci kök yalnız iki ünsüzle biterse (sırr-ıyla, haşr-ine; "câr-idir" değil)
            if found:
                out += [Match(self.entries[i], "stem", pre + last, pre + stem, pre + c) for i, c in found]
                levels += 1
                if levels == levels_max or stem[-1] not in "iu":
                    break
        return out

    # ---------------------------------------------------------- metnin harfleriyle süzme

    def _fits(self, m: Match, text: Form) -> bool:
        """Maddenin yazılışlarından biri metnin harfleriyle tutuyor mu. Tam eşlemede bütün harfler ve maddedeki her
        kesme; ek atılarak eşlemede kök (yumuşayan son harf serbest: kalb-i kalp, ihtiyac-ı ihtiyaç; ünlüsü geri konan
        kökte metnin ünlüsüyle: sabr-ı sabır), atılan ek ş ya da ö taşımaz ("kurtuluşu" kurt değildir)."""
        t = text.letters
        if m.how != "stem":
            want, free = t, None
        else:
            n = len(m.stem)
            if set(t[n:]) & {"ş", "ö"}:
                return False
            if len(m.form) == n + 1:
                want, free = t[:n - 1] + t[n] + t[n - 1], None
            else:
                soft = m.form != m.stem or (t[n - 1] in "cbdgğ" and t[n:n + 1] in _LITE_VOWELS)
                want, free = t[:n], (n - 1 if soft else None)
        forms = [f for f in self.forms[m.entry["id"]] if len(f.letters) == len(want)]
        if not _gaps_agree(forms, text, len(want)):
            return False
        for f in forms:
            if all(a == b or i == free for i, (a, b) in enumerate(zip(f.letters, want))) \
                    and all(p in text.apos or p > len(want) for p in f.apos):
                return True
        return False

    @lru_cache(maxsize=300_000)
    def lookup_key(self, k: str, text: Form | None = None) -> tuple[Match, ...]:
        """Anahtarın maddeleri. `text`: metindeki harf biçimi; verilirse harfi ya da kesmesi tutmayanlar atılır ve
        son kelimedeki kesmeden sonrası ek sayılır ("Kur’ân’ın": önce Kur'ân)."""
        if not k or k in STOP:
            return ()
        keep = (lambda ms: [m for m in ms if self._fits(m, text)]) if text else (lambda ms: ms)
        head, _, last = k.rpartition(" ")
        exact = keep(self._exact(k))
        if exact and head:
            return tuple(exact)
        if head and head not in self.prefixes:
            return tuple(exact)
        stems: list[Match] = []
        start = len(head) + 1 if head else 0
        cuts = sorted((p - start for p in (text.apos if text else ()) if p > start), reverse=True)
        if cuts and MIN_STEM - 1 <= cuts[0] < len(last) and SUFFIX.fullmatch(last[cuts[0]:]):
            pre = head + " " if head else ""
            stem = last[:cuts[0]]
            stems = keep([Match(m.entry, "stem", k, pre + stem, pre + stem) for m in self._exact(pre + stem)])
        if not stems and not last.startswith(STOP_PREFIXES):
            stems = keep(self._stemmed(head, last, 1 if exact else 2))
        ids = {m.entry["id"] for m in exact}
        return tuple(exact + [m for m in stems if m.entry["id"] not in ids])

    def lookup(self, text: str) -> list[Match]:
        return list(self.lookup_key(key(text), form(text)))

    def spans(self, text: str) -> list[tuple[int, int, tuple[Match, ...]]]:
        """Metinde lügatta karşılığı olan bütün kelime ve tamlamalar: (baş, uzunluk, eşleşmeler); baş ve uzunluk
        `tokens_of(text)` dizisindedir (`search_words(text)` ile aynı kelimeler). Tamlamada önceki kelimeler maddeyle aynı yazılmalı, yalnız sonuncusu ek
        alabilir."""
        tokens = tokens_of(text)
        words = [w for w, _ in tokens]
        out = []
        for i in range(len(words)):
            for n in range(1, MAX_PHRASE + 1):
                if i + n > len(words):
                    break
                head = " ".join(words[i:i + n - 1])
                if n > 1 and head not in self.prefixes:
                    break
                forms = [f for _, f in tokens[i:i + n]]
                if found := self.lookup_key(" ".join(words[i:i + n]), _join(forms)):
                    out.append((i, n, found))
        return out


# Kelime: harfler, birleşen işaretler (şapka, Arapça hareke) ve kesmeler; okuma platformundaki `lugatWords` aynı böler
_TOKEN = re.compile(rf"(?:[\w{_APOS}]|[\u0300-\u036f\u0610-\u061a\u064b-\u065f\u0670\u06d6-\u06ed])+")


def tokens_of(text: str) -> list[tuple[str, Form | None]]:
    """Metnin anahtar kelimeleri (`search_words` ile aynı) ve harf biçimleri."""
    return [(w, f) for m in _TOKEN.finditer(text) for w, f in _token_forms(m[0])]


def _token_forms(token: str) -> list[tuple[str, Form | None]]:
    words = search_words(token)
    if len(words) == 1:
        return [(words[0], form(token))]
    return [(w, None) for w in words]


def _join(forms: list[Form | None]) -> Form | None:
    if any(f is None for f in forms):
        return None
    letters, apos, gap_i, gap_ı, n = [], set(), set(), set(), 0
    for f in forms:
        apos |= {p + n for p in f.apos}
        gap_i |= {p + n for p in f.gap_i}
        gap_ı |= {p + n for p in f.gap_ı}
        letters.append(f.letters)
        n += len(f.letters) + 1
    return Form(" ".join(letters), frozenset(apos), frozenset(gap_i), frozenset(gap_ı))


def record(m: Match) -> dict:
    """Araçların gösterdiği madde."""
    return {"word": m.entry["word"], "meaning": m.entry["meaning"], "how": m.how}


def surface(text: str, start: int, length: int) -> str:
    """`spans`'ın verdiği kelime aralığının metindeki yazılışı."""
    raw = [m for m in _TOKEN.finditer(text) for _ in _token_forms(m[0])]
    if start + length > len(raw):
        return " ".join(w for w, _ in tokens_of(text)[start:start + length])
    return text[raw[start].start():raw[start + length - 1].end()]


# ------------------------------------------------------------------ komut satırı


def build(root: Path = RAW_DIR / "risaleoku_app") -> dict:
    from risale_mcp.sources.risaleoku_app import load_dictionary
    manifest, texts = load_dictionary(LANG, root)
    entries, report = parse(texts)
    data = {"source": {"name": SOURCE_NAME, "url": SOURCE_URL, "site": "risaleoku_app", "title": manifest["title"],
                       "version": manifest["version"], "fetched_at": manifest["fetched_at"]},
            "entries": entries}
    LUGAT_PATH.parent.mkdir(parents=True, exist_ok=True)
    LUGAT_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=0), encoding="utf-8")
    return {"entries": len(entries), **{k: (len(v) if isinstance(v, list) else v) for k, v in report.items()},
            "examples": {k: v[:15] for k, v in report.items() if isinstance(v, list)}}


def measure(sample: int = 3000, seed: int = 7) -> Path:
    """Risale'nin Türkçe cümlelerinden örneklemde kapsam ve örnekler: `data/interim/lugat/olcum.md` (elle bakmak için)."""
    import random
    import sqlite3
    from collections import Counter
    from risale_mcp.paths import DIST_DIR, INTERIM_DIR
    lex = Lexicon.load()
    conn = sqlite3.connect(DIST_DIR / "genel" / "risale.db")
    rows = [r[0] for r in conn.execute(
        "SELECT s.text FROM sentences s JOIN nodes n ON n.id = s.node_id JOIN works w ON w.slug = n.work"
        " WHERE w.language = 'tr' AND w.collection = 'risale/kulliyat'")]
    rng = random.Random(seed)
    rows = rng.sample(rows, min(sample, len(rows)))
    how, missing, stems, phrases, tokens = Counter(), Counter(), Counter(), Counter(), 0
    for text in rows:
        for token in _TOKEN.finditer(text):
            for w, f in _token_forms(token[0]):
                if not w.isalpha() or not w.isascii():
                    continue
                tokens += 1
                found = lex.lookup_key(w, f)
                how[found[0].how if found else "yok"] += 1
                if not found:
                    missing[w] += 1
                elif found[0].how == "stem":
                    stems[(token[0], found[0].entry["word"])] += 1
        words = [w for w, _ in tokens_of(text)]
        assert words == search_words(text), text
        for i, n, found in lex.spans(text):
            if n > 1:
                phrases[(" ".join(words[i:i + n]), found[0].entry["word"])] += 1
    out = INTERIM_DIR / "lugat" / "olcum.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# Lügat ölçümü ({len(rows)} cümle, {tokens} kelime; Arapça ve sayılar hariç)", "",
             "| eşleme | oran |", "|---|---|"]
    lines += [f"| {k} | {v / tokens:.1%} |" for k, v in how.most_common()]
    lines += ["", "## En sık bulunamayanlar", "", ", ".join(f"{w} ({n})" for w, n in missing.most_common(150)),
              "", "## Ek atılarak bulunanlardan 80 örnek (metindeki kelime → madde)", ""]
    lines += [f"- {w} → {e}" for w, e in rng.sample(sorted(stems), min(80, len(stems)))]
    lines += ["", "## Tamlamalardan 60 örnek (metin → madde)", ""]
    lines += [f"- {w} → {e}" for w, e in rng.sample(sorted(phrases), min(60, len(phrases)))]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build", help="ham veriden data/library/lugat/")
    look = sub.add_parser("bak", help="kelime ya da tamlamaların maddesi")
    look.add_argument("words", nargs="+")
    sub.add_parser("olc", help="Risale'nin cümlelerinde kapsam ve örnekler (data/interim/lugat/olcum.md)")
    args = ap.parse_args()
    if args.cmd == "olc":
        print(f"yazıldı: {measure()}")
    elif args.cmd == "build":
        print(json.dumps(build(), ensure_ascii=False, indent=1))
        print(f"yazıldı: {LUGAT_PATH}")
    else:
        lex = Lexicon.load()
        for w in args.words:
            found = lex.lookup(w)
            print(f"{w}: " + ("; ".join(f"{m.entry['word']} ({m.how}{', ' + m.stem if m.stem else ''}) = "
                                        f"{m.entry['meaning'][:90]!r}" for m in found) or "—"))


if __name__ == "__main__":
    main()
