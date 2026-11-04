"""Ortak OpenITI okuyucu (H6, `docs/tefsir-altyapi-plani.md`): mARkdown metni, üst bilgi, âyet ve sayfa işaretleri.

    uv run python -m risale_mcp.openiti <anahtar>…     # data/raw/openiti/<anahtar>.txt özeti: baskı, başlıklar, sayfa, âyet

İndirme `sources/openiti.py`'dedir. Bu modül alana bağlı değildir: hadis kitapları (`hadis_kutub.py`) ve ileride
müfessirlerin eserleri aynı okuyucuyu kullanır; eserin bölümlerini, hadis numarasını ya da âyet aralığını çıkarmak
kullananın işidir.

Biçim (OpenITI mARkdown):

    #META# 040.EdEDITOR :: …        üst bilgi; `#META#Header#End#` satırında biter. `NODATA` boş sayılır
    # metin                         paragraf başı; `~~` ile başlayan satırlar paragrafın devamıdır
    ### | başlık, ### || alt başlık  başlık; çizgi sayısı seviyedir (`Paragraph.level`)
    PageV01P003                     sayfa işareti: 1. cildin 3. sayfasının SONU. İşaretten önceki metin o sayfadadır,
                                    sonraki metin bir sonraki işaretin sayfasındadır (OpenITI'nin kuralı)
    @QB@ … @QE@                     âyet alıntısı: metinde "﴿ … ﴾" olur, yeri `quran` aralıklarındadır
    ms0001                          kilometre taşı (OpenITI'nin bölme işareti), atılır
    \\ 1 \\                         dipnot işareti (dipnotlar OpenITI temizliğinde atılmıştır), atılır; içine düşmüş
                                    kilometre taşıyla birlikte (`\\ 1 ms0007 \\`)

Metin yalnız işaretlerden arındırılır, harfine dokunulmaz; boşluklar teke iner.

Basılı sayfa (`printed`, kullanıcının kararı, 2026-11-04): Risale'de sayfa yoktur; klasik eserlerde asıl adres
yapısaldır, kaynak verdiyse basılı cilt ve sayfa ikincil bilgidir, kimliğe girmez, tahmin edilmez. Sayfa
numaraları üst bilgide adı geçen baskınındır (`edition`: muhakkik, yayınevi, yer, yıl, baskı sayısı). OpenITI'nin
`.yml`'si sürümün başka bir baskıyla karşılaştırıldığını söyleyebilir (`version`: `COLLATED`, `COMMENT`); o baskının
sayfaları farklıdır, `printed` onu göstermez. Son işaretten sonra kalan metnin sayfası bilinmez (`None`).
"""

import bisect
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from risale_mcp.paths import RAW_DIR

RAW_ROOT = RAW_DIR / "openiti"
HEADER_END = "#META#Header#End#"

_MARK = re.compile(r"(?P<page>PageV(?P<vol>\d+)P(?P<num>\d+))|(?P<ms>\bms\d+\b)|(?P<note>\\\s*\d+\s*(?:ms\d+\s*)?\\)"
                   r"|(?P<qb>@QB@)|(?P<qe>@QE@)")
_META = re.compile(r"^#META#\s*\d+\.(\w+)\s*::\s*(.*)$")
_YML = re.compile(r"^\d+#(\w+)#(\w+)#*:\s?(.*)$")
_LEVEL = re.compile(r"^###\s*(\|+)\s*")
# Doldurulmamış `.yml` şablonunun değerleri: bilgi değildir (Beyzâvî'nin dört sürümünde öyle kalmış).
YML_TEMPLATE = ("permalink, permalink", "all@id, vol1@id", "the name of the annotator", "a free running comment here",
                "YYYY-MM-DD", "formalized issues, separated with commas")
EDITION_FIELDS = {"EdEDITOR": "editor", "EdPUBLISHER": "publisher", "EdPLACE": "place", "EdYEAR": "year",
                  "EdNUMBER": "edition", "BookVOLS": "volumes"}


@dataclass(frozen=True, order=True)
class Page:
    volume: int
    page: int

    def __str__(self) -> str:
        return f"{self.volume}/{self.page}"


@dataclass
class Paragraph:
    raw: str                                        # satırın kendisi, `~~` devamları bir boşlukla eklenmiş
    text: str                                       # işaretlerden arınmış metin (baştaki "#", "### |" dahil değil)
    level: int | None = None                        # başlıksa seviye (### | -> 1)
    quran: list[tuple[int, int]] = field(default_factory=list)    # `text` içinde âyet alıntıları (﴿ ﴾ hariç)
    breaks: list[tuple[int, Page]] = field(default_factory=list)  # `text` içinde sayfa sonları: (konum, biten sayfa)
    page: Page | None = None                        # metnin başladığı sayfa
    end_page: Page | None = None                    # metnin bittiği sayfa

    def printed(self) -> dict | None:
        """Araçlara ve JSON'a giden biçim: {"volume", "page"} ve sayfa aşıyorsa "end"."""
        if self.page is None:
            return None
        out = {"volume": self.page.volume, "page": self.page.page}
        if self.end_page and self.end_page != self.page:
            out["end"] = str(self.end_page)
        return out


@dataclass
class Document:
    meta: dict[str, str]
    paragraphs: list[Paragraph]

    @property
    def edition(self) -> dict:
        """Sayfa numaralarının ait olduğu baskı: üst bilginin söylediği kadar."""
        return {name: self.meta[key] for key, name in EDITION_FIELDS.items() if self.meta.get(key)}


def clean(text: str) -> tuple[str, list[tuple[int, int]], list[tuple[int, Page]]]:
    """İşaretleri atar, boşlukları teke indirir: (metin, âyet aralıkları, sayfa sonları). Sayfa sonunun konumu, o
    sayfanın son harfinden sonraki yerdir (metin sonunu aşmaz)."""
    out: list[str] = []
    quran, breaks = [], []
    opened: int | None = None

    def put(chunk: str) -> None:
        for ch in chunk:
            if ch.isspace():
                if out and out[-1] != " ":
                    out.append(" ")
            else:
                out.append(ch)

    def end() -> int:                               # sondaki boşluk sayılmaz
        return len(out) - (1 if out and out[-1] == " " else 0)

    pos = 0
    for m in _MARK.finditer(text):
        put(text[pos:m.start()])
        pos = m.end()
        if m["page"]:
            breaks.append((end(), Page(int(m["vol"]), int(m["num"]))))
            put(" ")
        elif m["qb"]:
            put("﴿")
            opened = len(out)
        elif m["qe"]:
            if opened is not None:
                start = opened + (1 if opened < len(out) and out[opened] == " " else 0)
                if end() > start:
                    quran.append((start, end()))
                opened = None
            put("﴾")
        else:                                       # ms, dipnot işareti
            put(" ")
    put(text[pos:])
    while out and out[-1] == " ":
        out.pop()
    result = "".join(out)
    return result, quran, [(min(at, len(result)), page) for at, page in breaks]


def split_header(raw: str) -> tuple[dict[str, str], str]:
    head, sep, body = raw.partition(HEADER_END)
    if not sep:
        raise ValueError(f"OpenITI üst bilgisinin sonu ({HEADER_END}) yok")
    meta = {}
    for line in head.splitlines():
        if (m := _META.match(line.strip())) and m[2].strip() and m[2].strip() != "NODATA":
            meta[m[1]] = m[2].strip()
    return meta, body


def raw_paragraphs(body: str) -> list[str]:
    """Paragraflar (`#` ile başlayan satırlar); `~~` satırları öncekine bir boşlukla eklenir."""
    out: list[str] = []
    for line in body.splitlines():
        if line.startswith("~~"):
            if out:
                out[-1] += " " + line[2:]
        elif line.startswith("#"):
            out.append(line)
    return out


def read(raw: str) -> Document:
    meta, body = split_header(raw)
    paragraphs = []
    for line in raw_paragraphs(body):
        level = len(m[1]) if (m := _LEVEL.match(line)) else None
        text, quran, breaks = clean(line[m.end():] if m else line.lstrip("#"))
        paragraphs.append(Paragraph(line, text, level, quran, breaks))
    _pages(paragraphs)
    return Document(meta, paragraphs)


def _pages(paragraphs: list[Paragraph]) -> None:
    """Her paragrafın başladığı ve bittiği sayfa: harfin sayfası, ondan sonra gelen ilk sayfa işaretidir."""
    offsets, stops, pages = [], [], []              # paragrafların ortak eksendeki başı; işaretlerin yeri ve sayfası
    total = 0
    for p in paragraphs:
        offsets.append(total)
        for at, page in p.breaks:
            stops.append(total + at)
            pages.append(page)
        total += len(p.text) + 1

    def page_of(position: int) -> Page | None:
        i = bisect.bisect_right(stops, position)
        return pages[i] if i < len(pages) else None

    for p, start in zip(paragraphs, offsets):
        if p.text:
            p.page, p.end_page = page_of(start), page_of(start + len(p.text) - 1)


def version_info(yml: str) -> dict[str, str]:
    """Sürümün `.yml` açıklaması (`80#VERS#BASED####: …`): alan -> değer; girintili satırlar değere eklenir."""
    out: dict[str, str] = {}
    key = None
    for line in yml.splitlines():
        if m := _YML.match(line):
            key = m[2]
            out[key] = m[3].strip()
        elif key and line.startswith((" ", "\t")):
            out[key] = (out[key] + " " + line.strip()).strip()
    return {k: v for k, v in out.items() if v and not v.startswith(("NODATA", *YML_TEMPLATE))}


def load(key: str, root: Path = RAW_ROOT) -> Document:
    return read((root / f"{key}.txt").read_text(encoding="utf-8"))


def summary(key: str, root: Path = RAW_ROOT) -> list[str]:
    doc = load(key, root)
    yml = root / f"{key}.yml"
    version = version_info(yml.read_text(encoding="utf-8")) if yml.exists() else {}
    paged = [p for p in doc.paragraphs if p.text]
    unknown = sum(p.page is None for p in paged)
    pages = sorted({page for p in doc.paragraphs for _, page in p.breaks})
    levels: dict[int, int] = {}
    for p in doc.paragraphs:
        if p.level:
            levels[p.level] = levels.get(p.level, 0) + 1
    return [f"## {key}", "", f"- baskı: {doc.edition}",
            *([f"- karşılaştırılan: {version['COLLATED']}"] if version.get("COLLATED") else []),
            f"- paragraf {len(doc.paragraphs)}, başlık {levels}",
            f"- sayfa işareti {len(pages)} ({pages[0]}–{pages[-1]})" if pages else "- sayfa işareti yok",
            f"- sayfası bilinmeyen paragraf {unknown}",
            f"- âyet alıntısı {sum(len(p.quran) for p in doc.paragraphs)}", ""]


def main() -> None:
    keys = sys.argv[1:] or sorted(p.stem for p in RAW_ROOT.glob("*.txt"))
    for key in keys:
        print("\n".join(summary(key)))


if __name__ == "__main__":
    main()
