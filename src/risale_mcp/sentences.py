"""Aşama 3: cümleler. Atıf birimi cümledir.

Bölme kuralları (CLAUDE.md "Cümle kuralları"):
- Cümle `.` `!` `?` `؟` `…` `‥` (ve ardından gelebilecek kapanış tırnağı/parantezi) ile biter;
  ancak ardından boşluk ve şunlardan biri gelirse: büyük harf, açılış tırnağı ya da
  parantezi, Arapça bir parça ya da harf ("…gördüm. اَيُحِبُّ…"; Arapça nesirde her cümle
  böyle başlar) ya da madde numarası ("2. Yâhut").
- `;` ve `:` cümleyi bitirmez ("Hiç mümkün müdür ki;", "Elcevab:").
- Kısaltma ve baş harflerden sonra bölünmez: "Hz.", "Dr.", "M. Kemâl", "(İ.G.Z.)";
  madde numarasından ("1.") sonra da bölünmez.
- Arapça parçanın içinde bölünmez. Tamamen Arapça paragraf ve imza tek cümledir,
  tablonun her satırı bir cümledir. Şiir de düz metin gibi bölünür.
- Eser `stops: "*"` taşıyorsa (Badıllı'nın el-Mesnevî el-Arabî baskısı cümleleri klasik baskılardaki gibi
  " * " ile ayırır) iki yanı boşluklu "*" de, ardından Arapça harf gelirse cümleyi bitirir.

Numaralar her düğümün kendi metninde 1'den başlar. Hâşiye cümleleri, hâşiyenin bağlı
olduğu cümlenin altında kendi içinde numaralanır:
    sozler/10/on-iki-hakikat/hakikat-09/c032            … › Dokuzuncu Hakikat › 32. cümle
    sozler/10/on-iki-hakikat/hakikat-09/c032/h1/c002    … › 32. cümle › Hâşiye › 2. cümle
Bir cümlede birden çok hâşiye varsa "Hâşiye 1", "Hâşiye 2" olur. Başlıktaki hâşiye
düğüme bağlanır: `<düğüm>/h1/c001`. Başkasının şerhi (`commentator`) hâşiye gibi bağlanır, ama
ayrı sayılır: `…/c032/s1/c002`, `… › 32. cümle › Şerh › 2. cümle`.
"""

import argparse
import hashlib
import json
import re
from collections import defaultdict

from risale_mcp.books.model import REF_SEPARATOR
from risale_mcp.normalize import fold
from risale_mcp.paths import BOOKS_DIR, ROOT

_END = re.compile(r"[.!?؟…‥]+[”’\"»)\]']*(?=\s)")
_STAR_END = re.compile(r"[.!?؟…‥]+[”’\"»)\]']*(?=\s)|(?<=\s)[*٭](?=\s|$)")
_ARABIC_LETTER = re.compile(r"[\u0600-\u06FF]")
_OPENERS = "“\"‘'«("
_LIST_MARKER = re.compile(r"\d{1,2}\.\s+\S")
_INITIALS = re.compile(r"(?:[A-ZÇĞİÖŞÜÂÎÛ]\.)*[A-ZÇĞİÖŞÜÂÎÛ]")
ABBREVIATIONS = {"Hz", "Hzr", "Dr", "Prof", "No", "vs", "vb", "Sh", "Av"}
MIN_INCIPIT_WORDS = 4

# Altın örnekler: bu Sözler düğümlerinin cümleleri tests/golden/ altında kilitlidir.
GOLDEN_PATH = ROOT / "tests" / "golden" / "sentences_sozler.json"
GOLDEN_NODES = (
    "sozler/1",                                   # Bismillah, temsiller, "Öyle mi?"
    "sozler/6",                                   # Kâr ve Hasaret serileri
    "sozler/10/on-iki-hakikat/hakikat-09",        # uzun hakikat, tırnaklı konuşmalar, hâşiye
    "sozler/26/zeyl",                             # iki "Hatve" serisi
)


def _arabic_mask(text: str, arabic: list[dict]) -> list[bool]:
    mask = [False] * len(text)
    for span in arabic:
        for i in range(span["start"], min(span["end"], len(text))):
            mask[i] = True
    return mask


def _no_break_before(text: str, dot: int) -> bool:
    """Noktadan önceki kelime kısaltma, baş harf ya da madde numarası mı?"""
    start = dot
    while start > 0 and not text[start - 1].isspace():
        start -= 1
    word = text[start:dot].lstrip(_OPENERS)
    return (word in ABBREVIATIONS or bool(_INITIALS.fullmatch(word))
            or (word.isdigit() and len(word) <= 3))


def _starts_sentence(text: str, i: int, arabic: list[bool]) -> bool:
    ch = text[i]
    return (ch.isupper() or ch in _OPENERS or arabic[i] or bool(_ARABIC_LETTER.match(ch))
            or bool(_LIST_MARKER.match(text, i)))


def split(text: str, arabic: list[dict] | None = None, star: bool = False) -> list[tuple[int, int]]:
    """Düz metni cümlelere böler: (başlangıç, bitiş) karakter konumları, boşluksuz."""
    mask = _arabic_mask(text, arabic or [])
    bounds, start = [], 0
    for match in (_STAR_END if star else _END).finditer(text):
        if mask[match.start()]:
            continue
        nxt = match.end()
        while nxt < len(text) and text[nxt].isspace():
            nxt += 1
        if nxt == len(text) or not _starts_sentence(text, nxt, mask):
            continue
        if match.group() == "*" and not _ARABIC_LETTER.match(text[nxt]):
            continue
        if text[match.start()] == "." and match.group().count(".") == 1 and _no_break_before(text, match.start()):
            continue
        bounds.append((start, match.end()))
        start = nxt
    bounds.append((start, len(text.rstrip())))
    return [(s, e) for s, e in bounds if e > s]


def split_paragraph(paragraph: dict, star: bool = False) -> list[tuple[int, int]]:
    text = paragraph["text"]
    if paragraph["kind"] in ("arabic", "signature"):
        return [(0, len(text))] if text else []
    if paragraph["kind"] == "table":
        out, pos = [], 0
        for line in text.split("\n"):
            if line.strip():
                out.append((pos, pos + len(line)))
            pos += len(line) + 1
        return out
    return split(text, paragraph.get("arabic"), star)


# ---------------------------------------------------------------- eserin cümleleri

def _containing(spans: list[tuple[int, int, str]], offset: int) -> str | None:
    """Hâşiye işaretinin düştüğü cümle: işaret cümlenin sonundaki noktadan hemen sonra da olabilir."""
    for start, end, sid in spans:
        if offset <= end:
            return sid
    return spans[-1][2] if spans else None


def incipits(texts: list[str]) -> list[str]:
    """Her cümle için, aynı gruptaki başka bir cümlenin başıyla karışmayan en kısa baş
    (en az MIN_INCIPIT_WORDS kelime). Tamamen aynı iki cümlede cümlenin tamamı döner."""
    words = [t.split() for t in texts]
    folded = [[fold(w) for w in ws] for ws in words]
    out = []
    for i, ws in enumerate(folded):
        length = min(MIN_INCIPIT_WORDS, len(ws))
        others = [f for j, f in enumerate(folded) if j != i]
        while length < len(ws) and any(o[:length] == ws[:length] for o in others):
            length += 1
        out.append(" ".join(words[i][:length]))
    return out


def segment(book: dict) -> list[dict]:
    """Eser JSON'undan cümle kayıtları üretir; hâşiye paragraflarına `anchor` (bağlı oldukları
    cümle ya da başlıktaysa düğüm) yazar."""
    node_refs = {n["id"]: n["ref"] for n in book["outline"]}
    sentences: list[dict] = []
    spans_of: dict[str, list[tuple[int, int, str]]] = {}   # paragraf -> cümleleri
    count_in_node: dict[str, int] = defaultdict(int)
    hasiye_count: dict[tuple, int] = defaultdict(int)        # (bağlantı, h|s) -> hâşiye ya da şerh sayısı
    hasiye_prefix: dict[str, tuple[str, tuple, int]] = {}    # hâşiye paragrafı -> (önek, (bağlantı, h|s), k)

    for p in book["paragraphs"]:
        if "text" not in p:                     # mecmuada ana cilde eşlenmiş: cümleleri orada
            spans_of[p["id"]] = []
            continue
        if p["kind"] == "hasiye":
            parent = p["parent_id"]
            anchor = parent if parent in node_refs else (_containing(spans_of[parent], p["offset"]) or p["node_id"])
            p["anchor"] = anchor
            letter = "s" if p.get("commentator") else "h"
            hasiye_count[anchor, letter] += 1
            k = hasiye_count[anchor, letter]
            hasiye_prefix[p["id"]] = (f"{anchor}/{letter}{k}", (anchor, letter), k)
        spans = []
        for m, (start, end) in enumerate(split_paragraph(p, book.get("stops") == "*"), 1):
            if p["kind"] == "hasiye":
                prefix, anchor, k = hasiye_prefix[p["id"]]
                sid, n = f"{prefix}/c{m:03d}", m
            else:
                count_in_node[p["node_id"]] += 1
                n = count_in_node[p["node_id"]]
                sid, anchor, k = f"{p['node_id']}/c{n:03d}", None, None
            text = p["text"][start:end]
            sentences.append({"id": sid, "node_id": p["node_id"], "paragraph_id": p["id"], "n": n,
                              "start": start, "end": end, "text": text,
                              "hash": hashlib.sha1(text.encode("utf-8")).hexdigest()[:12],
                              "_anchor": anchor, "_k": k})
            spans.append((start, end, sid))
        spans_of[p["id"]] = spans

    refs = dict(node_refs)
    for s in sentences:
        anchor, k = s.pop("_anchor"), s.pop("_k")
        if anchor is None:
            base = refs[s["node_id"]]
        else:
            name = "Şerh" if anchor[1] == "s" else "Hâşiye"
            label = name if hasiye_count[anchor] == 1 else f"{name} {k}"
            base = f"{refs[anchor[0]]}{REF_SEPARATOR}{label}"
        s["ref"] = f"{base}{REF_SEPARATOR}{s['n']}. cümle"
        refs[s["id"]] = s["ref"]

    by_node = defaultdict(list)
    for s in sentences:
        by_node[s["node_id"]].append(s)
    for group in by_node.values():
        for s, incipit in zip(group, incipits([s["text"] for s in group])):
            s["incipit"] = incipit
    return sentences


def golden_snapshot(book: dict) -> dict[str, list[list[str]]]:
    """Altın düğümlerin cümleleri: [kimlik, incipit, metin özeti]."""
    return {node: [[x["id"], x["incipit"], x["hash"]] for x in book["sentences"] if x["node_id"] == node]
            for node in GOLDEN_NODES}


def main() -> None:
    parser = argparse.ArgumentParser(description="Cümle bölücü yardımcıları.")
    parser.add_argument("--golden", action="store_true", help="altın örnekleri data/books/sozler.json'dan yenile")
    args = parser.parse_args()
    if args.golden:
        book = json.loads((BOOKS_DIR / "sozler.json").read_text(encoding="utf-8"))
        GOLDEN_PATH.parent.mkdir(parents=True, exist_ok=True)
        GOLDEN_PATH.write_text(json.dumps(golden_snapshot(book), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"yazıldı: {GOLDEN_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
