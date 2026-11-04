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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--measure", action="store_true", help="yalnız Kur'ân alıntısı ölçümü")
    parser.add_argument("--db", type=Path, default=DB_PATH)
    args = parser.parse_args()
    conn = sqlite3.connect(args.db)
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
