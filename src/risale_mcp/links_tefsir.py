"""Müfessirlerin eserlerinin bağları (T5, `docs/tefsir-altyapi-plani.md`): pilot Beyzâvî.

    uv run python -m risale_mcp.links_tefsir            # yerel veritabanından -> data/links/tefsir/*.jsonl, rapor
    uv run python -m risale_mcp.links_tefsir --measure  # yalnız Kur'ân alıntısı ölçümü (JK'nın işaretleriyle)

Bütün dosyalar `private`'tır (pilot): yalnız yerel profil okur; genel profile bağın hedefi de girmez (T4).

    tefsir/structure.jsonl   âyet birimi -> âyetleri (`relation`, `verse_unit`, yöntem `structure`: birimin başlığı
                             söylüyor; okuma değil). Kaynak birimin düğümü (`scope: section`)
    tefsir/quran_text.jsonl  şerhteki işaretsiz Kur'ân alıntıları (`quote`, yöntem `quran_text`). İlişki: `lemma`
                             (birimin kendi âyetinin sözü cümlenin başında: şerh edilen lafız, aday), `verbatim` (öbürleri).
                             Güç: kendi âyetinin cümle ortasındaki sözü zayıf, öbürleri güçlü.
                             Bulunan söz, konumu ve harf sayısı `evidence`'ta. Cümlede birden çok alıntı olabilir:
                             parça anahtarı yoktur (Arapça parça işaretli değil), konum `evidence`'tadır
    tefsir/corpus.jsonl      «» içindeki hadis adaylarının rivayetleri (`quote`, `corpus`; Risale'nin hadis eşlemesiyle
                             aynı eşleyici ve aynı ilişki adları). Parça anahtarı yoktur: Risale'nin hadis tabloları
                             yalnız parçalı bağlardan kurulur, bu bağlar onlara karışmaz. Rivayet metinleri
                             `data/library/hadis/tefsir-beyzavi.json`'da

Kur'ân alıntısı (işaretsiz metin): cümlenin kelimeleri harf iskeletine indirilir (`quran.skeleton`, kelime başına);
her kelimeden başlayarak Kur'ân'ın kelime iskeletinde (Osmanî ve imlâî iki yazım, kelime sınırıyla) bulunan en uzun
dizi alınır, en az `MIN_WORDS` kelime ve `MIN_LETTERS` harf; birimin kendi âyetinde geçiyorsa bağlam doğruladığı için
`OWN_MIN_WORDS` ve `OWN_MIN_LETTERS` yeter. Yer: birimin kendi âyetlerinde geçiyorsa orası; değilse
Kur'ân'da tek bir yerde geçiyorsa orası; birden çok yerde geçiyorsa numara verilmez, bağ kurulmaz (sayılır). Eşikler
JK sürümünün `@QB@` işaretleriyle ölçülerek seçildi (`--measure`, rapor `data/interim/tefsir/t5-kuran.md`).

İşârât ile aynı âyetteki yerler bağ değildir, okuma adayıdır (`data/interim/tefsir/t5-isarat.md`): aynı âyet
aralığı ve ortak kelime dizileri (Kur'ân sözü sayılmaz). İlişkinin türü okumayla belirlenir.
"""

import argparse
import json
import re
import sqlite3
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

from risale_mcp import openiti
from risale_mcp.links import Link, cite_as, write
from risale_mcp.paths import DB_PATH, INTERIM_DIR, LIBRARY_DIR, LINKS_DIR
from risale_mcp.quran import Quran, skeleton

WORK = "beyzavi"
OUT = LINKS_DIR / "tefsir"
REPORT_DIR = INTERIM_DIR / "tefsir"
HADITH_STORE = LIBRARY_DIR / "hadis" / "tefsir-beyzavi.json"   # eser klasörüne konmaz: oradaki her JSON eserdir
MIN_WORDS = 3           # ölçümle seçildi (`--measure`)
MIN_LETTERS = 9         # 7'de sık kalıplar ("ما تقدم من", "كل واحد منهما") başka sûreye bağlanıyordu
OWN_MIN_WORDS = 2       # birimin kendi âyetinde: bağlam doğruluyor ("إياك نعبد")
OWN_MIN_LETTERS = 4
JK_KEY = "beyzavi-jk"
JK_STOP = "اسجدوا لآدم"  # JK'da pilotun sonu (Bakara 34)
HADITH_CUES = re.compile(r"(?:عليه (?:الصلاة و)?السلام|صلى الله عليه وسلم|رسول الله|النبي|روي|روى)[^«]{0,40}$")
META = {"producer": "links_tefsir.py", "private": True, "note": "Tefsir pilotu: yalnız yerel profil"}


# ---------------------------------------------------------------- Kur'ân'ın kelime iskeleti

class QuranWords:
    """Kur'ân'ın iki yazımda kelime iskeleti: sûre başına " k1 k2 … " dizisi ve her âyetin dizideki başı."""

    def __init__(self, quran: Quran) -> None:
        self.fields: list[dict[int, tuple[str, list[int]]]] = []
        for field in ("text", "text_clean"):
            suras = {}
            for number, count in quran.counts.items():
                buf, starts = " ", []
                for ayah in range(1, count + 1):
                    starts.append(len(buf) - 1)
                    words = [w for w in map(skeleton, quran.ayahs[(number, ayah)][field].split()) if w]
                    buf += " ".join(words) + " "
                suras[number] = (buf, starts)
            self.fields.append(suras)
        self.all = "|".join(buf for suras in self.fields for buf, _ in suras.values())

    def contains(self, words: list[str]) -> bool:
        return f" {' '.join(words)} " in self.all

    def places(self, words: list[str]) -> set[tuple[int, int, int]]:
        """(sûre, ilk âyet, son âyet): dizinin geçtiği bütün yerler."""
        import bisect
        needle, out = f" {' '.join(words)} ", set()
        for suras in self.fields:
            for number, (buf, starts) in suras.items():
                at = buf.find(needle)
                while at >= 0:
                    out.add((number, bisect.bisect_right(starts, at), bisect.bisect_right(starts, at + len(needle) - 2)))
                    at = buf.find(needle, at + 1)
        return out


@dataclass
class Quote:
    sentence: str
    start: int                     # cümle metnindeki konum
    end: int
    text: str
    place: tuple[int, int, int] | None
    own: bool                      # birimin kendi âyetinde
    lemma: bool                    # cümlenin başında ve kendi âyeti
    places: int                    # Kur'ân'da kaç yerde


def _tokens(text: str) -> list[tuple[int, int, str]]:
    """(başlangıç, bitiş, iskelet) — iskeleti boş kalan kelime ("و", "يا") atlanır."""
    return [(m.start(), m.end(), sk) for m in re.finditer(r"\S+", text) if (sk := skeleton(m.group()))]


def find_quotes(qw: QuranWords, sid: str, text: str, own: tuple[int, int, int] | None,
                min_words: int = MIN_WORDS, min_letters: int = MIN_LETTERS) -> tuple[list[Quote], int]:
    """Cümledeki işaretsiz Kur'ân alıntıları ve numarası verilemeyen (birden çok yerde geçen) dizilerin sayısı."""
    tokens = _tokens(text)
    out, ambiguous, i = [], 0, 0
    while i < len(tokens):
        j = i
        while j < len(tokens) and qw.contains([t[2] for t in tokens[i:j + 1]]):
            j += 1
        words = [t[2] for t in tokens[i:j]]
        places = qw.places(words) if len(words) >= OWN_MIN_WORDS and sum(map(len, words)) >= OWN_MIN_LETTERS else set()
        mine = {p for p in places if own and p[0] == own[0] and p[1] <= own[2] and own[1] <= p[2]}
        if mine or (len(words) >= min_words and sum(map(len, words)) >= min_letters):
            place = min(mine) if mine else (next(iter(places)) if len(places) == 1 else None)
            if place is None:
                ambiguous += 1
            else:
                start, end = tokens[i][0], tokens[j - 1][1]
                out.append(Quote(sid, start, end, text[start:end], place, bool(mine), bool(mine) and i == 0, len(places)))
            i = j
        else:
            i += 1
    return out, ambiguous


# ---------------------------------------------------------------- eser

def _book() -> dict:
    from risale_mcp.catalog import get_work
    return json.loads(get_work(WORK).book_path.read_text(encoding="utf-8"))


def _units(book: dict) -> dict[str, tuple[int, int, int]]:
    return {n["id"]: (n["verses"]["sura"], n["verses"]["start"], n["verses"]["end"]) for n in book["outline"] if n.get("verses")}


def _unit_of(node: str, units: dict) -> tuple[int, int, int] | None:
    while node:
        if node in units:
            return units[node]
        node = node.rpartition("/")[0]
    return None


def _verse(place: tuple[int, int, int]) -> str:
    sura, a, b = place
    return f"quran:{sura}:{a}" + (f"-{b}" if b != a else "")


def structure_links(conn: sqlite3.Connection, book: dict) -> list[Link]:
    return [Link(node, _verse(place), "relation", "structure", "strong", "verse_unit", scope="section",
                 display=cite_as(conn, node, "section")) for node, place in _units(book).items()]


def quote_links(conn: sqlite3.Connection, book: dict, quotes: list[Quote]) -> list[Link]:
    out = []
    for q in quotes:
        # Kendi âyetinin cümle ortasındaki sözü zayıf: kısa olabilir (eşik bağlamla gevşek), kalıp ifade de olabilir.
        strength = "weak" if q.own and not q.lemma else "strong"
        out.append(Link(q.sentence, _verse(q.place), "quote", "quran_text", strength, "lemma" if q.lemma else "verbatim",
                        evidence={"text": q.text, "start": q.start, "end": q.end, "letters": len(skeleton(q.text)),
                                  **({"own_verse": True} if q.own else {}), **({"candidate": True} if q.lemma else {})},
                        display=cite_as(conn, q.sentence)))
    return out


def all_quotes(conn: sqlite3.Connection, book: dict, qw: QuranWords, muellif_only: bool = False,
               **thresholds) -> tuple[list[Quote], int]:
    """`muellif_only`: muhakkikin girişi atlanır (ölçüm: JK'da giriş yok)."""
    units = _units(book)
    quotes, ambiguous = [], 0
    for sid, node, text in conn.execute("SELECT id, node_id, text FROM sentences WHERE work = ? ORDER BY seq", (WORK,)):
        if muellif_only and node.startswith(f"{WORK}/mukaddime-tahkik"):
            continue
        found, amb = find_quotes(qw, sid, text, _unit_of(node, units), **thresholds)
        quotes += found
        ambiguous += amb
    return quotes, ambiguous


# ---------------------------------------------------------------- ölçüm (JK'nın işaretleri)

def jk_quotes() -> list[str]:
    """JK sürümünün pilot aralığındaki `@QB@` alıntıları (iskelet kelimeleri boşlukla)."""
    out = []
    for p in openiti.load(JK_KEY).paragraphs:
        out += [" ".join(t[2] for t in _tokens(p.text[a:b])) for a, b in p.quran]
        if JK_STOP in p.text:
            break
    return [q for q in out if q]


def measure(quotes: list[Quote], marked: list[str]) -> dict:
    """Bulunanların JK işaretleriyle örtüşmesi: isabet (bulunanın bir JK işaretiyle iç içe olması) ve kapsama
    (en az 2 kelimelik JK işaretinin bulunanlardan biriyle iç içe olması). İki baskı aynı değil: ölçü kabadır."""
    found = [" ".join(t[2] for t in _tokens(q.text)) for q in quotes]
    pad = lambda s: f" {s} "
    marked_long = [m for m in marked if len(m.split()) >= 2]           # sabit tanım: eşikten bağımsız
    hit = sum(any(pad(f) in pad(m) or pad(m) in pad(f) for m in marked) for f in found)
    covered = sum(any(pad(m) in pad(f) or pad(f) in pad(m) for f in found) for m in marked_long)
    return {"bulunan": len(found), "isabet": hit, "isabet_orani": hit / max(1, len(found)),
            "jk_isaretli": len(marked_long), "kapsanan": covered, "kapsama": covered / max(1, len(marked_long))}


# ---------------------------------------------------------------- hadis

def hadith_candidates(conn: sqlite3.Connection) -> list[tuple[str, str]]:
    """(cümle, söz): «» içindeki, önünde hadis işareti ("عليه الصلاة والسلام", "روي"…) bulunan sözler."""
    out = []
    for sid, text in conn.execute("SELECT id, text FROM sentences WHERE work = ? ORDER BY seq", (WORK,)):
        for m in re.finditer(r"«([^«»]{8,})»", text):
            if HADITH_CUES.search(text[max(0, m.start() - 80):m.start()]):
                out.append((sid, m.group(1).strip()))
    return out


def hadith_links(conn: sqlite3.Connection, candidates: list[tuple[str, str]], qw: QuranWords) -> tuple[list[Link], list[dict], dict]:
    from risale_mcp.hadis import Corpus, read_reports
    from risale_mcp.links_hadis import MATCH_RELATION, target
    corpus = Corpus(list(read_reports()))
    links, rows, used = [], [], {}
    for sid, text in candidates:
        words = [t[2] for t in _tokens(text)]
        if qw.contains(words):                                 # Kur'ân sözü (kırâat, âyet): hadis değil
            rows.append({"sentence": sid, "text": text, "match": "quran"})
            continue
        match, found, total = corpus.match(text)
        rows.append({"sentence": sid, "text": text, "match": match, "total": total,
                     "reports": [corpus.reports[i].id for i in found]})
        if (relation := MATCH_RELATION.get(match)) is None:
            continue
        for rank, i in enumerate(found):
            r = corpus.reports[i]
            used[r.id] = {"title": r.title, "number": r.number, "text": r.text, "source": r.source, "grades": r.grades}
            links.append(Link(sid, target(r.id), "quote", "corpus", "weak" if relation == "phrase" else "strong", relation,
                              evidence={"match": match, "rank": rank, "total": total, "text": text},
                              display=cite_as(conn, sid)))
    return links, rows, used


# ---------------------------------------------------------------- İşârât adayları

ISARAT = ("isaratul-icaz-arabi", "isaratul-icaz")


def isarat_candidates(conn: sqlite3.Connection, book: dict, qw: QuranWords, size: int = 4) -> list[dict]:
    """Her Beyzâvî birimi için İşârât'ın aynı âyetle açılan bölümleri (`ayah_links`, `acilis`) ve Arapça İşârât ile
    ortak `size` kelimelik diziler (Kur'ân sözü olanlar sayılmaz). Bağ değil, okuma adayı."""
    def grams(text: str) -> set[str]:
        w = [t[2] for t in _tokens(text)]
        return {" ".join(w[i:i + size]) for i in range(len(w) - size + 1) if not qw.contains(w[i:i + size])}

    out = []
    for node, (sura, a, b) in _units(book).items():
        sections = [r[0] for r in conn.execute(
            "SELECT DISTINCT node_id FROM ayah_links WHERE kind = 'acilis' AND sura = ? AND ayah_start <= ? AND ? <= ayah_end"
            " AND (node_id LIKE 'isaratul-icaz/%' OR node_id LIKE 'isaratul-icaz-arabi/%') ORDER BY node_id", (sura, b, a))]
        mine = {s: grams(t) for s, t in conn.execute("SELECT id, text FROM sentences WHERE node_id = ?", (node,))}
        shared = []
        for section in (s for s in sections if s.startswith("isaratul-icaz-arabi/")):
            for sid, text in conn.execute("SELECT id, text FROM sentences WHERE node_id = ? OR node_id LIKE ?",
                                          (section, section + "/%")):
                g = grams(text)
                for bid, bg in mine.items():
                    if common := g & bg:
                        shared.append({"isarat": sid, "beyzavi": bid, "grams": sorted(common)[:3], "count": len(common)})
        out.append({"unit": node, "verses": _verse((sura, a, b)), "sections": sections,
                    "shared": sorted(shared, key=lambda x: -x["count"])})
    return out


# ---------------------------------------------------------------- rapor

def _write_reports(stats: dict, quotes: list[Quote], hadith_rows: list[dict], isarat: list[dict]) -> None:
    import random
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    lines = ["# T5: Beyzâvî'nin Kur'ân alıntıları", "", "`uv run python -m risale_mcp.links_tefsir --measure`.",
             "Ölçü JK sürümünün `@QB@` işaretleridir; iki baskı aynı değildir, sayılar kabadır.", "",
             "| en az kelime | en az harf | bulunan | isabet | kapsanan JK işareti | kapsama |", "|---|---|---|---|---|---|"]
    for (w, l), m in stats["grid"].items():
        mark = " **(seçilen)**" if (w, l) == (MIN_WORDS, MIN_LETTERS) else ""
        lines.append(f"| {w}{mark} | {l} | {m['bulunan']} | %{100 * m['isabet_orani']:.0f} | {m['kapsanan']}/{m['jk_isaretli']} | %{100 * m['kapsama']:.0f} |")
    lines += ["", f"Seçilen eşikte: {len(quotes)} alıntı (lemma adayı {sum(q.lemma for q in quotes)}, birimin kendi âyeti "
              f"{sum(q.own for q in quotes)}), numarası verilemeyen (birden çok yerde) {stats['ambiguous']}.", "",
              "## 30'luk örneklem (seçilen eşik)", "", "| # | Cümle | Söz | Âyet | Tür |", "|---|---|---|---|---|"]
    for k, q in enumerate(sorted(random.Random(5).sample(quotes, min(30, len(quotes))), key=lambda q: q.sentence), 1):
        kind = "lemma" if q.lemma else "kendi âyeti" if q.own else f"{q.places} yerde"
        lines.append(f"| {k} | `{q.sentence}` | {q.text} | {_verse(q.place)} | {kind} |")
    (REPORT_DIR / "t5-kuran.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    counts = Counter(r["match"] for r in hadith_rows)
    lines = ["# T5: Beyzâvî'nin hadis adayları", "", f"«» içinde, önünde hadis işareti olan {len(hadith_rows)} söz: "
             + ", ".join(f"{k} {v}" for k, v in counts.most_common()) + ".", "",
             "| Cümle | Söz | Sonuç | Rivayet |", "|---|---|---|---|"]
    lines += [f"| `{r['sentence']}` | {r['text'][:80]} | {r['match']} | {', '.join(r.get('reports', [])[:2])} |" for r in hadith_rows]
    (REPORT_DIR / "t5-hadis.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    lines = ["# T5: İşârât ile Beyzâvî, aynı âyette (okuma adayları, bağ değil)", "",
             "Bölümler: İşârât'ın o âyetle açılan bölümleri (`ayah_links`, `acilis`). Ortak diziler: Arapça İşârât ile "
             "Beyzâvî biriminin ortak 4 kelimelik dizileri (Kur'ân sözü sayılmaz). İlişkinin türü okumayla belirlenir.", "",
             "| Birim | Âyet | İşârât bölümleri | Ortak dizili cümle çifti | En çok ortak |", "|---|---|---|---|---|"]
    for c in isarat:
        top = c["shared"][0] if c["shared"] else None
        lines.append(f"| `{c['unit']}` | {c['verses']} | {len(c['sections'])} | {len(c['shared'])} | "
                     + (f"`{top['isarat']}` ↔ `{top['beyzavi']}` ({top['count']}): {' / '.join(top['grams'])}" if top else "") + " |")
    (REPORT_DIR / "t5-isarat.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- T7: kullanıcı örneklemi

SAMPLE_SEED = 7
LONG_WORDS = 100


def review_sample(conn: sqlite3.Connection, quran: Quran) -> tuple[list[str], dict]:
    """Numaralı örneklem (Markdown) ve numaraların anahtarları (JSON): A Kur'ân alıntıları (15 lemma, 10 kendi âyetinin
    cümle ortası, 15 başka âyet), B bağ kurulan hadis sözleri, C 100 kelimeyi aşan cümleler. Daha önce karara
    bağlanmış bağ örnekleme girmez."""
    import random
    from risale_mcp import link_reviews
    reviewed = {r.key for r in link_reviews.current(link_reviews.read()) if r.key}
    rows = conn.execute("SELECT l.source, l.target, l.type, l.relation, l.strength, l.evidence, s.text FROM links l"
                        " JOIN sentences s ON s.id = l.source WHERE l.file = 'tefsir/quran_text.jsonl'").fetchall()
    rows = [r for r in rows if (r[0], r[1], r[2], "") not in reviewed]
    rng = random.Random(SAMPLE_SEED)
    groups = (("lemma", 15, lambda r: r[3] == "lemma"), ("kendi âyeti, cümle ortası", 10, lambda r: r[4] == "weak"),
              ("başka âyet", 15, lambda r: r[3] == "verbatim" and r[4] == "strong"))
    keys: dict = {"A": {}, "B": {}, "C": {}}
    lines = ["# T7: Beyzâvî örneklemi", "",
             "Her satır için ✓ (doğru) ya da ✗ (yanlış; isterseniz kısa not). Numarasıyla bildirin: \"A3 ✗ âyet değil\".",
             "Kararlar isminizle denetim kaydına yazılır (`data/links/reviews/tefsir/`).", "",
             "## A. Kur'ân alıntıları", "",
             "Soru: **bulunan söz gerçekten bu âyetten bir alıntı mı?** Lemma için ayrıca: cümle âyetin bu lafzını şerh "
             "ederek mi başlıyor? Âyetin Tanzil metni karşılaştırma içindir.", ""]
    n = 0
    for title, size, pick in groups:
        chosen = sorted(rng.sample([r for r in rows if pick(r)], min(size, sum(map(pick, rows)))), key=lambda r: r[0])
        lines += [f"### {title} ({len(chosen)})", "", "| # | Cümle | Bulunan söz (cümlede) | Âyet | Âyetin metni |",
                  "|---|---|---|---|---|"]
        for r in chosen:
            n += 1
            ev = json.loads(r[5])
            text = r[6]
            shown = text[:ev["start"]] + "**" + text[ev["start"]:ev["end"]] + "**" + text[ev["end"]:]
            if len(shown) > 260:
                shown = "… " + shown[max(0, ev["start"] - 80):ev["end"] + 84] + " …"
            sura_s, _, ayahs = r[1].removeprefix("quran:").partition(":")
            a_s, _, b_s = ayahs.partition("-")
            sura, a, b = int(sura_s), int(a_s), int(b_s or a_s)
            verse = " ".join(quran.ayahs[(sura, k)]["text"] for k in range(a, b + 1))
            lines.append(f"| A{n} | `{r[0]}` | {shown.replace('|', '/')} | {sura}:{ayahs} | {verse[:160]} |")
            keys["A"][f"A{n}"] = {"source": r[0], "target": r[1], "type": r[2]}
        lines.append("")
    store = json.loads(HADITH_STORE.read_text("utf-8"))["reports"] if HADITH_STORE.exists() else {}
    from risale_mcp.links_hadis import report_id
    lines += ["## B. Hadis sözleri", "", "Soru: **Beyzâvî'nin sözü ile rivayet aynı hadis mi?** (Derece sorulmuyor; "
              "hüküm verilmez.) Her sözün ilk bulunan rivayeti, metninin sonuyla (senet başta kalır).", "",
              "| # | Cümle | Beyzâvî'nin sözü | Eşleşme | Rivayet (kitap, no) | Rivayetin metni |", "|---|---|---|---|---|---|"]
    k = 0
    for source, target, type_, ev in conn.execute(
            "SELECT source, target, type, evidence FROM links WHERE file = 'tefsir/corpus.jsonl'"
            " AND json_extract(evidence, '$.rank') = 0 ORDER BY source"):
        k += 1
        ev = json.loads(ev)
        r = store.get(report_id(target), {})
        lines.append(f"| B{k} | `{source}` | {ev['text']} | {ev['match']} | {r.get('title', '?')}, {r.get('number', '?')} | "
                     f"… {(r.get('text') or '')[-260:].replace('|', '/')} |")         # metin senetten sonra: sonu gösterilir
        keys["B"][f"B{k}"] = {"source": source, "target": target, "type": type_}
    lines += ["", "## C. Uzun cümleler", "",
              f"{LONG_WORDS} kelimeyi aşan cümleler. Bölücü yalnız . ؟ ! işaretinden böler; \"؛\" ve \":\" bölmez (Risale'nin "
              "kuralı). Soru: **olduğu gibi kalsın mı?** Toplu cevap yeter (\"C hepsi kalsın\"); bölünmesi gerekeni "
              "numarasıyla ve nereden bölüneceğiyle yazın.", "", "| # | Cümle | Kelime | Baş ve son |", "|---|---|---|---|"]
    long = [(sid, text) for sid, text in conn.execute(
        "SELECT id, text FROM sentences WHERE work = ? ORDER BY seq", (WORK,)) if len(text.split()) > LONG_WORDS]
    for k, (sid, text) in enumerate(long, 1):
        words = text.split()
        lines.append(f"| C{k} | `{sid}` | {len(words)} | {' '.join(words[:12])} … {' '.join(words[-8:])} |")
        keys["C"][f"C{k}"] = {"sentence": sid, "words": len(words)}
    return lines, keys


# Örneklemin HTML'i: bütün Arapça tek yazı tipiyle ve büyük (kullanıcının isteği, 2026-11-04: âyet sütunu ile bulunan söz
# farklı görünüyordu, Arapça küçüktü). Markdown görüntüleyiciye bağlıdır; HTML'de yazı tipi sayfanındır. Dışarıdan
# bir şey yüklenmez: yazı tipi bilgisayardakidir (Amiri ya da Scheherazade yoksa Noto Naskh Arabic).
SAMPLE_CSS = """
:root { --bg: #fdfcf9; --fg: #1d1d1b; --muted: #6b6b66; --line: #ddd8cc; --mark: #fbe7a6; --head: #f2eee4; }
@media (prefers-color-scheme: dark) { :root { --bg: #1b1b19; --fg: #ecebe6; --muted: #a3a29b; --line: #3a3934;
  --mark: #6b5a1c; --head: #26251f; } }
body { background: var(--bg); color: var(--fg); font: 16px/1.6 system-ui, sans-serif; margin: 0 auto;
  max-width: 1400px; padding: 16px; }
h1, h2, h3 { line-height: 1.25; } h3 { color: var(--muted); }
table { border-collapse: collapse; width: 100%; margin: 12px 0 28px; }
th, td { border: 1px solid var(--line); padding: 8px 10px; vertical-align: top; text-align: start; }
th { background: var(--head); font-weight: 600; }
td.ar { font-family: "Amiri", "Scheherazade New", "Noto Naskh Arabic", serif; font-size: 1.55em; line-height: 2.1;
  direction: rtl; text-align: right; }
td.ar b { background: var(--mark); font-weight: 700; border-radius: 3px; padding: 0 2px; }
td.no { font-weight: 700; white-space: nowrap; } code { font-size: .85em; color: var(--muted); }
"""
_ARABIC = re.compile(r"[\u0600-\u06FF]")


def sample_html(lines: list[str]) -> str:
    """Örneklemin Markdown satırlarından sayfa: başlıklar, paragraflar, tablolar (**kalın**, `kod`)."""
    import html

    def inline(text: str) -> str:
        text = html.escape(text)
        text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
        return re.sub(r"`(.+?)`", r"<code>\1</code>", text)

    out, table = [], None
    for line in lines:
        if line.startswith("|"):
            cells = line.strip()[1:-1].split(" | ")
            if set(line.replace("|", "").strip()) <= {"-"}:
                continue
            if table is None:
                table = True
                out.append("<table><tr>" + "".join(f"<th>{inline(c.strip())}</th>" for c in cells) + "</tr>")
                continue
            row = []
            for i, c in enumerate(cells):
                c = c.strip()
                cls = "no" if i == 0 else "ar" if _ARABIC.search(c) and not c.startswith("`") else ""
                row.append(f"<td class=\"{cls}\">{inline(c)}</td>" if cls else f"<td>{inline(c)}</td>")
            out.append("<tr>" + "".join(row) + "</tr>")
            continue
        if table:
            out.append("</table>")
            table = None
        for prefix, tag in (("### ", "h3"), ("## ", "h2"), ("# ", "h1")):
            if line.startswith(prefix):
                out.append(f"<{tag}>{inline(line[len(prefix):])}</{tag}>")
                break
        else:
            if line.strip():
                out.append(f"<p>{inline(line)}</p>")
    if table:
        out.append("</table>")
    return ("<!doctype html><html lang=\"tr\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>Beyzâvî örneklemi</title>"
            f"<style>{SAMPLE_CSS}</style></head><body>" + "\n".join(out) + "</body></html>\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--measure", action="store_true", help="yalnız Kur'ân alıntısı ölçümü")
    parser.add_argument("--sample", action="store_true", help="T7 örneklemi: data/interim/tefsir/t7-orneklem.{html,md,json}")
    parser.add_argument("--db", type=Path, default=DB_PATH)
    args = parser.parse_args()
    conn = sqlite3.connect(args.db)
    if args.sample:
        lines, keys = review_sample(conn, Quran.load())
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        (REPORT_DIR / "t7-orneklem.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        (REPORT_DIR / "t7-orneklem.html").write_text(sample_html(lines), encoding="utf-8")
        (REPORT_DIR / "t7-orneklem.json").write_text(json.dumps(keys, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  örneklem: A {len(keys['A'])}, B {len(keys['B'])}, C {len(keys['C'])}; {REPORT_DIR / 't7-orneklem.html'} (ve .md)")
        return
    book = _book()
    qw = QuranWords(Quran.load())
    marked = jk_quotes()
    grid = {}
    for w, l in ((2, 7), (2, 9), (3, 7), (3, 9), (4, 10)):
        grid[(w, l)] = measure(all_quotes(conn, book, qw, True, min_words=w, min_letters=l)[0], marked)
        print(f"  en az {w} kelime, {l} harf: {grid[(w, l)]}")
    quotes, ambiguous = all_quotes(conn, book, qw)
    if args.measure:
        _write_reports({"grid": grid, "ambiguous": ambiguous}, quotes, [], [])
        return
    hadith, rows, used = hadith_links(conn, hadith_candidates(conn), qw)
    isarat = isarat_candidates(conn, book, qw)
    counts = {"structure": write(OUT / "structure.jsonl", structure_links(conn, book), **META),
              "quran_text": write(OUT / "quran_text.jsonl", quote_links(conn, book, quotes), **META),
              "corpus": write(OUT / "corpus.jsonl", hadith, **META)}
    HADITH_STORE.write_text(json.dumps({"reports": used}, ensure_ascii=False), encoding="utf-8")
    _write_reports({"grid": grid, "ambiguous": ambiguous}, quotes, rows, isarat)
    print(f"  bağlar: {counts}; rapor: {REPORT_DIR}")


if __name__ == "__main__":
    main()
