"""MVP hadis kitapları: OpenITI Shamela (ve Keşfü'l-Hafâ'nın JK) sürümlerinden kitap ağacı ve hadisler (M2,
`docs/mvp-kitaplar.md`).

    uv run python -m risale_mcp.fetch hadis          # data/raw/openiti/<kitap>.txt (sabit commit, `sources/hadis.MVP_BOOKS`)
    uv run python -m risale_mcp.hadis_openiti        # data/library/hadis/kutub/<kitap>.json, rapor data/interim/hadis/mvp-kutub.md

Çıktı Kütüb-i Sitte'ninkiyle (`hadis_kutub.py`) aynı biçimdedir: `outline` (kitap, bâb, sahâbî müsnedi; başlığın
seviyesine göre) ve `hadiths` (`id` `musned/14870`: baskının numarası, `node_id`, `text`, `printed`). Kütüb-i Sitte
yükleyicisi (`hadis_kutub.load`) bu dosyaları okumaz.

Biçim (ham veri incelendi, 2026-11-06):

    ### | 14870 -              hadis 14870 (Müsned, Müstedrek, Mecmaü'z-Zevâid, Kenz, Feyzü'l-Kadîr, Dârimî, Mu'cem)
    ### | [ص: 156]             basılı sayfa (sayfa işareti boş olan sürümlerde tek kaynak): sayfanın BAŞI
    ### | [التعليق - من تلخيص الذهبي]   Müstedrek: Zehebî'nin Telhîs'i, hadisin ardında ayrı katman
    ### | كتاب … / باب … / مسند …   başlık: seviyesine göre ağaç
    # 47 - أخبرنا …             el-İhsân: numara paragrafın başında (bazen satırın ortasında "…# 48 - …")
    # __________L               el-İhsân: ayraç; ardından Elbânî'nin hükmü ve nâşirin notları (ayrı katman)
    # 1461 ( … )                Keşfü'l-Hafâ (JK): numara ve parantezli söz
    # 143 – …                   Kenz: numaranın bir kısmı başlıkta değil paragrafın başında, uzun tireyle
    ### | [تعليق المحقق]        Dârimî: muhakkik Hüseyin Selîm Esed'in senet hükmü, ayrı katman

Katmanlar müellife mal edilmez (`layers`: `by`, metin). Feyzü'l-Kadîr Münâvî'nin iç içe şerhidir: parantez içindeki
sözler Câmiu's-Sağîr'in (Suyûtî) metnidir; ayrılmaz, kitabın notunda yazılıdır. Sayfa: sürümün sayfa işareti
gerçekse (`PageV00P000` değilse) o; değilse "[ص: n]" işaretinden (cilt bilinmez).
"""

import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from risale_mcp import openiti
from risale_mcp.paths import INTERIM_DIR, LIBRARY_DIR, RAW_DIR
from risale_mcp.sources.hadis import MVP_BOOKS, MVP_COMMITS

KUTUB_DIR = LIBRARY_DIR / "hadis" / "kutub"
LICENCE = "CC BY-NC-SA 4.0"


@dataclass(frozen=True)
class Spec:
    title: str
    author: str
    inline: re.Pattern | None = None            # numara başlıkta değil paragrafın başında
    layer_head: str | None = None              # bu başlıktan sonraki paragraflar ayrı katman
    layer_sep: str | None = None               # bu satırdan sonraki paragraflar ayrı katman
    layer_by: str | None = None
    note: str | None = None
    unit: str = "number"                       # number: baskının numarası; isnad: "أخبرنا/حدثنا" ile açılan rivayet;
                                               # paragraph: kaynağın paragrafı (ikisinde kimlik bizim sıramız: s00001)
    editor_head: str | None = None             # bu başlığın altı muhakkikin metnidir (sonraki başlığa kadar)


SPECS = {
    "musned": Spec("Müsned", "Ahmed b. Hanbel"),
    "darimi": Spec("Sünen-i Dârimî", "Abdullah b. Abdurrahman ed-Dârimî", layer_head="[تعليق المحقق]",
                   layer_by="Muhakkik Hüseyin Selîm Esed'in hükmü"),
    "mucem-sagir": Spec("el-Mu'cemü's-Sağîr", "Ebü'l-Kāsım et-Taberânî"),
    "mustedrek": Spec("el-Müstedrek ale's-Sahîhayn", "Hâkim en-Nîsâbûrî",
                      layer_head="[التعليق - من تلخيص الذهبي]", layer_by="Zehebî, Telhîsü'l-Müstedrek"),
    "ihsan": Spec("el-İhsân fî Takrîbi Sahîhi İbn Hibbân", "İbn Hibbân (tertip: İbn Balbân)",
                  inline=re.compile(r"(?:^|#\s*)(\d{1,5})\s*-\s+"), layer_sep="__________",
                  layer_by="Elbânî'nin hükmü ve nâşirin notları (baskının ta'lîkı)"),
    "mecma": Spec("Mecmaü'z-Zevâid", "Nûreddîn el-Heysemî"),
    "kenz": Spec("Kenzü'l-Ummâl", "Alî el-Müttakī el-Hindî", inline=re.compile(r"(?:^|#\s*)(\d{1,5})\s*[-–]\s+"),
                 note="Her hadisin sonundaki parantez içi remizler (\"(هب عن …)\") müellifin kaynak işaretleridir."),
    "feyz": Spec("Feyzü'l-Kadîr", "Abdürraûf el-Münâvî",
                 note="Münâvî'nin el-Câmiu's-Sağîr şerhi (iç içe): parantez içindeki sözler Suyûtî'nin metnidir, "
                      "gerisi Münâvî'nin; ayrılmadı."),
    "sifa": Spec("eş-Şifâ bi-Ta'rîfi Hukūki'l-Mustafâ", "Kādî İyâz", unit="paragraph", editor_head="EDITOR",
                 note="Hadis numarası yok: birim kaynağın paragrafıdır, kimlik bizim sıramızdır (sifa/s00001). "
                      "«1» gibi işaretler muhakkikin dipnot işaretleridir; dipnotlar kaynakta yok."),
    "delail": Spec("Delâilü'n-Nübüvve", "Ebû Bekr el-Beyhakī", unit="isnad",
                   note="Hadis numarası yok: birim \"أخبرنا/حدثنا\" ile açılan rivayettir, kimlik bizim sıramızdır "
                        "(delail/s00001). Bâb başlıkları ağaçtadır."),
    "kesfulhafa": Spec("Keşfü'l-Hafâ", "İsmâil b. Muhammed el-Aclûnî", inline=re.compile(r"^(\d{1,5})\s*\(")),
}

_NUMBER = re.compile(r"^(\d{1,5})\s*[-–]?\s*$")
_PAGE = re.compile(r"^\[ص:\s*(\d+)\]$")
_KITAB = re.compile(r"^(?:كتاب|أبواب|ابواب|كتب)\b")
_ISNAD_START = re.compile(r"^(?:و|ف)?(?:أخبرنا|حدثنا|أخبرني|حدثني|أنبأنا|وأنبأنا)\b")


@dataclass
class Report:
    hadiths: int = 0
    nodes: int = 0
    layered: int = 0
    gaps: list[str] = field(default_factory=list)
    repeats: int = 0
    unpaged: int = 0
    before_first: int = 0                       # ilk hadisten önceki paragraf (mukaddime, başlıklar)


def _real_pages(doc: openiti.Document) -> bool:
    return any(p.page and (p.page.volume, p.page.page) != (0, 0) for p in doc.paragraphs[:5000])


def parse(key: str, raw_root: Path = RAW_DIR / "openiti") -> tuple[dict, Report]:
    spec = SPECS[key]
    doc = openiti.load(key, raw_root)
    real = _real_pages(doc)
    report = Report()
    outline = [{"id": key, "parent_id": None, "level": "book", "number": None, "title": spec.title}]
    stack: list[tuple[int, str]] = []          # (seviye, düğüm kimliği)
    counters: Counter = Counter()
    hadiths: list[dict] = []
    current: dict | None = None
    layer = False
    inline_page: int | None = None
    seen: set[int] = set()
    occurrences: Counter = Counter()

    def node_id() -> str:
        return stack[-1][1] if stack else key

    def start(number: int, text: str, p: openiti.Paragraph) -> None:
        nonlocal current, layer
        if number in seen:
            report.repeats += 1
        seen.add(number)
        occurrences[number] += 1                 # kaynakta tekrar eden numara (yazım hatası): ikinci geçiş "-2" alır
        suffix = f"-{occurrences[number]}" if occurrences[number] > 1 else ""
        current = {"id": f"{key}/{number}{suffix}", "number": number, "node_id": node_id(), "paragraphs": [],
                   "printed": _printed(p, real, inline_page)}
        if current["printed"] is None:
            report.unpaged += 1
        hadiths.append(current)
        layer = False
        if text:
            current["paragraphs"].append(text)

    seq = 0
    editor = False

    def start_seq(text: str, p: openiti.Paragraph) -> None:
        nonlocal seq, current, layer
        seq += 1
        current = {"id": f"{key}/s{seq:05d}", "number": None, "seq": seq, "node_id": node_id(), "paragraphs": [],
                   "printed": _printed(p, real, inline_page)}
        if current["printed"] is None:
            report.unpaged += 1
        hadiths.append(current)
        layer = False
        if text:
            current["paragraphs"].append(text)

    def add(text: str) -> None:
        if editor:
            report.before_first += 1             # muhakkikin metni: alınmaz, sayılır
            return
        if current is None:
            report.before_first += 1
            return
        if layer:
            current.setdefault("layers", [{"by": spec.layer_by, "text": []}])[0]["text"].append(text)
        else:
            current["paragraphs"].append(text)

    for p in doc.paragraphs:
        text = p.text.strip()
        if p.level:
            if not text:
                continue
            if m := _NUMBER.match(text):
                start(int(m[1]), "", p)
                continue
            if m := _PAGE.match(text):
                inline_page = int(m[1])
                continue
            if spec.layer_head and text == spec.layer_head:
                layer = True
                continue
            if spec.editor_head and text.strip("| ") == spec.editor_head:
                editor = True
                continue
            editor = False
            title = re.sub(r"^AUTO\s+", "", text).strip("[] ")
            while stack and stack[-1][0] >= p.level:
                stack.pop()
            counters[node_id()] += 1
            nid = f"{node_id()}/n{counters[node_id()]:03d}"
            kind = "kitab" if _KITAB.match(title) else "bab"
            outline.append({"id": nid, "parent_id": node_id(), "level": kind, "number": None, "title": title})
            stack.append((p.level, nid))
            current, layer = None, False
            report.nodes += 1
            continue
        if not text:
            continue
        if spec.layer_sep and text.startswith(spec.layer_sep):
            layer = True
            continue
        if spec.unit == "paragraph" and not editor:
            start_seq(text, p)
            continue
        if spec.unit == "isnad" and _ISNAD_START.match(text):
            start_seq(text, p)
            continue
        if spec.inline and (m := _inline(spec.inline, text)):
            pos, number, rest = m
            if pos:
                add(text[:pos].rstrip("# ").strip())
            start(number, rest, p)
            continue
        add(text)

    numbers = [h["number"] for h in hadiths if h["number"] is not None]
    report.hadiths = len(hadiths)
    report.layered = sum(1 for h in hadiths if h.get("layers"))
    report.gaps = [f"{a}→{b}" for a, b in zip(numbers, numbers[1:]) if b - a > 50 or b < a][:20]
    for h in hadiths:
        h["text"] = " ".join(h.pop("paragraphs"))
        for layer_ in h.get("layers", []):
            layer_["text"] = " ".join(layer_["text"])
    repo, path = MVP_BOOKS[key]
    source = {"site": "openiti", "repo": repo, "commit": MVP_COMMITS[repo], "path": path, "licence": LICENCE,
              "edition": doc.edition, "author": spec.author,
              **({"pages": "inline [ص: n] işaretinden; cilt bilinmez"} if not real else {}),
              **({"note": spec.note} if spec.note else {})}
    return {"book": key, "title": spec.title, "source": source, "outline": outline, "hadiths": hadiths}, report


def _inline(pattern: re.Pattern, text: str) -> tuple[int, int, str] | None:
    """Paragraf içindeki numara: başta ya da "#" ardından (satır birleşmesi); yer, numara, numaradan sonrası."""
    m = pattern.match(text) or (pattern.search(text) if "#" in text else None)
    if not m:
        return None
    body = m.group(0).rstrip()
    return m.start(), int(m[1]), (text[m.end():] if body.endswith(("-", "–")) else text[m.end() - 1:]).strip()


def _printed(p: openiti.Paragraph, real: bool, inline_page: int | None) -> dict | None:
    if real and p.page and (p.page.volume, p.page.page) != (0, 0):
        return {"volume": p.page.volume, "page": p.page.page}
    if inline_page is not None:
        return {"page": inline_page}
    return None


def main() -> None:
    import sys
    keys = sys.argv[1:] or list(SPECS)
    KUTUB_DIR.mkdir(parents=True, exist_ok=True)
    lines = ["# MVP hadis kitapları (M2)", "", "| Kitap | Hadis | Düğüm | Katmanlı | Tekrar numara | Sayfasız | İlk hadisten önce | Atlama |",
             "|---|---|---|---|---|---|---|---|"]
    for key in keys:
        book, r = parse(key)
        (KUTUB_DIR / f"{key}.json").write_text(json.dumps(book, ensure_ascii=False), encoding="utf-8")
        lines.append(f"| {book['title']} | {r.hadiths} | {r.nodes} | {r.layered} | {r.repeats} | {r.unpaged} | "
                     f"{r.before_first} | {', '.join(r.gaps[:6])} |")
        print(f"{key}: hadis {r.hadiths}, düğüm {r.nodes}, katmanlı {r.layered}, tekrar {r.repeats}, sayfasız {r.unpaged},"
              f" ilk hadisten önce {r.before_first}, atlama {r.gaps[:5]}")
    out = INTERIM_DIR / "hadis" / "mvp-kutub.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
