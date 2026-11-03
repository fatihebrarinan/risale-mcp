"""Künye ayrıştırıcı: kaynakça metninden kitap, bölüm, cilt, sayfa, numara.

    uv run python -m risale_mcp.hadis_kunye      # rapor: data/interim/hadis/kunye.md

Risale'ye bağlı değildir: serbest metin alır, `hadis_kitaplar` kaydına bağlar; ileride `hadis` profili de kullanır.
Ham metin asla atılmaz, tanınmayan kısım `leftover`'da durur ve ölçülür. Sayılar yorumlanmaz, türüyle saklanır:

    chapter   "Edeb: 96": kitap adı + sayı. Ölçüldü (bulunan rivayetlerin Hadith API numaralarıyla): metin o kitapta
              varsa kitap adı bölümle %85 tutar (149'da 127; bir hadise birçok kitap gösterilir, aynı lafız hepsinde
              geçmez); sayı hadis sırasıyla tutmaz, çoğunlukla bâbdır: `number` ile rivayete gidilmez
    no        "no. 3012", "hadis no: 8270": kitabın genel numarası; baskıya bağlıdır, ölçümde 15'te 3 tuttu: rivayete
              doğrudan götürmez, ancak metinle birlikte kanıttır
    volume    "3:326": cilt ve sayfa, "c. 3 s. 509" de aynı; baskıya bağlıdır, rivayete götürmez
    page      "s. 78", "sh: 12"

`qualifier` künyenin gücünü söyler, metinden gelir: `see` ("bk."), `iktibas` ("iktibâsen"), `by_meaning` ("bilmânâ",
"aynı mânâyı ifade eden"). `by_meaning` ve `iktibas` künyenin bütününe, `see` geçtiği yerden sonrasına uygulanır.
"""

import re
from collections import Counter
from dataclasses import dataclass, field

from risale_mcp.hadis_kitaplar import BOOKS, BY_ID, MENTION, _fold, section

_QUALIFIERS = (("by_meaning", re.compile(r"bilmana|bil mana|mana ?ile|ayni manay?[ia]|manen|manaca|benzer ifade")),
               ("iktibas", re.compile(r"iktibas")))
_SEE = re.compile(r"\b(ayrica )?(bk|bkz|bakiniz)\b\.?:?")
_NOISE = re.compile(r"^[\s,.;:()\[\]/\"“”'’-]*$")
_EDITION = re.compile(r"\((?:tahkik|thk|tah|baski|nesir|dipnot|haz|ter)[^()]*\)")
_CHAPTER_START = re.compile(r"\s*[^\W\d][^\d:;,()]{1,38}?\s*[:,]?\s*\d")
_NUMBERS = r"\d+(?:\s*[-–]\s*\d+)?(?:\s*,\s*\d+(?:\s*[-–]\s*\d+)?(?!\s*[:/]))*"
_ITEM = re.compile(
    rf"(?P<cv>c\.?\s*(?P<v>\d+)[,\s]*(?:s|sh|sf)\.?\s*(?P<vp>\d+))"
    rf"|(?P<vol>(?P<vn>\d+)\s*[:/]\s*(?P<pn>\d+(?:\s*[-–]\s*\d+)?)(?:\s*/\s*(?P<vno>\d+))?(?P<more>(?:\s*,\s*\d+(?:\s*[-–]\s*\d+)?(?![\d\s]*[:/]))*))"
    rf"|(?:(?:hadis(?:\s*no|\s*numara\w*)?|hadis-i\s*serif\s*no|no|numara)[.:]*\s*(?P<no>\d+))"
    rf"|(?:(?:s|sh|sf|sayfa)[.:]*\s*(?P<page>\d+))"
    rf"|(?P<chapter>[^\W\d][^\d:;,()]{{1,38}}?)\s*[:,]?\s*(?P<ns>{_NUMBERS})"
    rf"|(?P<sure>\d+)\.\s*(?:sure|suren)\w*\s*tefsiri\s*:?\s*(?P<sn>\d+)"
    rf"|(?P<bare>{_NUMBERS})")


@dataclass
class Locator:
    kind: str                       # chapter, no, volume, page, number (türü belirsiz sayı), bare (konum yok)
    chapter: str | None = None
    section: int | None = None      # Hadith API bölümü
    volume: int | None = None
    page: str | None = None
    number: str | None = None


@dataclass
class Citation:
    book: str | None                # kayıtta olmayan kitapta boş, `raw` durur
    qualifier: str | None
    raw: str
    locators: list[Locator] = field(default_factory=list)
    leftover: str = ""


@dataclass
class Parsed:
    raw: str
    citations: list[Citation]
    leftover: str                   # hiçbir kitaba bağlanamayan metin


def _mentions(folded: str) -> list[tuple[int, int, str]]:
    return [(m.start(), m.end(), BOOKS[int(m.lastgroup[1:])].id) for m in MENTION.finditer(folded)]


def _locators(book: str, segment: str) -> tuple[list[Locator], str]:
    api, found, rest, at, chapter = BY_ID[book].api, [], [], 0, None
    folded = segment
    for m in _ITEM.finditer(folded):
        rest.append(folded[at:m.start()])
        at = m.end()
        if m["cv"]:
            found.append(Locator("volume", volume=int(m["v"]), page=m["vp"]))
        elif m["vol"]:
            found.append(Locator("volume", volume=int(m["vn"]), page=m["pn"], number=m["vno"]))
            found += [Locator("volume", volume=int(m["vn"]), page=p.strip()) for p in (m["more"] or "").split(",") if p.strip()]
        elif m["no"]:
            found.append(Locator("no", chapter=chapter, section=section(api, chapter) if chapter and api else None, number=m["no"]))
        elif m["page"]:
            found.append(Locator("page", page=m["page"]))
        elif m["bare"]:
            found.append(Locator("number", number=re.sub(r"\s+", "", m["bare"])))
        elif m["sure"]:
            chapter = "tefsir"
            found.append(Locator("chapter", chapter=f"tefsir {m['sure']}", section=section(api, "tefsir") if api else None, number=m["sn"]))
        else:
            chapter = m["chapter"].strip(" .,:-")
            if chapter == "bab":                        # "Tirmizi bab: 12": kitap adı yok
                chapter = None
                found.append(Locator("number", number=re.sub(r"\s+", "", m["ns"])))
                continue
            found.append(Locator("chapter", chapter=chapter, section=section(api, chapter) if api else None, number=re.sub(r"\s+", "", m["ns"])))
    rest.append(folded[at:])
    return found, "".join(rest)


_RAW_EDGE = " ;,.(:"
_SEE_TAIL = re.compile(r"(?:;[^;]*?)?\b(?:ayrica\s+)?(?:bk|bkz|bakiniz)\b[.:\s]*$")


def _unmatched_close(segment: str) -> int:
    """Eşi olmayan ilk ")" (künye bir meal ya da açıklama ayracının içindeyse orada biter); yoksa sonu."""
    depth = 0
    for i, ch in enumerate(segment):
        depth += (ch == "(") - (ch == ")")
        if depth < 0:
            return i
    return len(segment)


def _own_part(book: str, segment: str) -> tuple[str, str]:
    """Kitabın kendi kısmı ve artığı: ";" kitabı bitirir; Kütüb-i Sitte'de sonraki parça başka bölümse sürer."""
    head, *rest = segment.split(";")
    for i, piece in enumerate(rest):
        if not (piece.strip()[:1].isdigit() or BY_ID[book].api and _CHAPTER_START.match(piece)):
            return ";".join([head, *rest[:i]]), ";".join(rest[i:])
    return segment, ""


def parse(raw: str) -> Parsed:
    folded, where = _fold(raw)
    marks = _mentions(folded)
    qualifier = next((q for q, p in _QUALIFIERS if p.search(folded)), None)
    see_from = (m.start() if (m := _SEE.search(folded)) else None)
    citations = []
    for i, (start, end, book) in enumerate(marks):
        stop = marks[i + 1][0] if i + 1 < len(marks) else len(folded)
        # Baskı ayracı aynı uzunlukta boşluk olur: konumlar `raw`'la hizalı kalır, kesilen yer künyeden de kesilir.
        segment = _EDITION.sub(lambda m: " " * len(m[0]), folded[end:stop])
        # Künyeden sonra süren cümle; tek harfli kısaltmadan ("b. Yûsuf", "M. Bahaeddin") sonra değil.
        cut = re.search(r"\)\s*[^\W\d]|(?<!\d)(?<!\b[^\W\d])[.]\s+[^\W\d]{3}", segment)
        segment = segment[:cut.start()] if cut else segment
        segment = segment[:_unmatched_close(segment)]                    # meal ayracının kapanışı: künye biter
        # Künye ";"den sonra da sürer (kayıtta olmayan yazar ya da kitap); yalnız sondaki "… için bk" açıklaması atılır.
        own = _SEE_TAIL.sub("", segment).rstrip(_RAW_EDGE)
        if own.count("(") > own.count(")"):                            # kesilen ayraç künyede açık kalmasın
            own = own[:own.rindex("(")]
        segment, left_over = _own_part(book, segment)
        locators, left = _locators(book, segment)
        left += left_over
        left = re.sub(_SEE, "", left)
        kind = qualifier or ("see" if see_from is not None and start >= see_from else None)
        own_end = min(end + len(own.rstrip(_RAW_EDGE)), len(where))
        last = where[own_end - 1] + 1 if where and own_end else 0
        citations.append(Citation(book, kind, raw[where[start]:last].strip(_RAW_EDGE), locators or [Locator("bare")],
                                  "" if _NOISE.match(left) else left.strip(" ,.;:()")))
    head = folded[:marks[0][0]] if marks else folded
    head = "" if _NOISE.match(re.sub(_SEE, "", head)) else head.strip(" ,.;:()")
    if not citations:
        citations.append(Citation(None, qualifier, raw.strip(), [Locator("bare")], head))
    return Parsed(raw, citations, head)


def report() -> str:
    from risale_mcp.db import connect
    from risale_mcp.paths import DB_PATH, INTERIM_DIR
    conn = connect(DB_PATH)
    sources = Counter(r[0] for r in conn.execute("SELECT source FROM arabic WHERE kind = 'hadis' AND source IS NOT NULL"))
    books, kinds, chapters, left, heads, nobook = Counter(), Counter(), Counter(), Counter(), Counter(), Counter()
    for raw, n in sources.items():
        p = parse(raw)
        if p.citations[0].book is None:
            nobook[raw] += n
            continue
        if p.leftover:
            heads[p.leftover[:70]] += n
        for c in p.citations:
            books[c.book] += n
            if c.leftover:
                left[f"{c.book}: {c.leftover[:60]}"] += n
            for loc in c.locators:
                kinds[loc.kind] += n
                if BY_ID[c.book].api and loc.chapter and loc.section is None:
                    chapters[f"{c.book}: {loc.chapter}"] += n
    lines = [f"# Künye ayrıştırma\n\nFarklı künye metni: {len(sources)}, geçiş: {sum(sources.values())}.",
             f"Kitabı bulunamayan metin: {len(nobook)} ({sum(nobook.values())} geçiş). Künye içi artık: {len(left)}. "
             f"Bölümü eşlenmeyen kitap adı: {len(chapters)}. Baştaki metin: {len(heads)}.",
             f"\nKonum türü: {dict(kinds)}\n", "## Kitaplar", *(f"- {BY_ID[b].title}: {n}" for b, n in books.most_common()),
             "\n## Kitabı bulunamayan", *(f"- ({n}) {r[:120]}" for r, n in nobook.most_common(80)),
             "\n## Bölümü eşlenmeyen", *(f"- ({n}) {r}" for r, n in chapters.most_common(120)),
             "\n## Künye içi artık", *(f"- ({n}) {r}" for r, n in left.most_common(120)),
             "\n## Baştaki metin", *(f"- ({n}) {r}" for r, n in heads.most_common(60))]
    path = INTERIM_DIR / "hadis" / "kunye.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", "utf-8")
    return str(path)


if __name__ == "__main__":
    print(report())
