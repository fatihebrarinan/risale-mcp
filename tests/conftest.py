"""Testlerin ortak verisi: elle yazılmış iki küçük eserden kurulan veritabanı.

Sözler'den bir parça (Arapça, âyet, hâşiye, alt bölüm) ve onu ana cilde eşlenmiş bir paragrafla
gösteren bir mecmua (Asâ-yı Mûsâ). Aşama 5 (veritabanı) ve Aşama 6 (sunucu) testleri kullanır.
"""

import json

import pytest

from risale_mcp.build_db import BuildReport, build

AYAH = "اَللّٰهُ لَٓا اِلٰهَ اِلَّا هُوَ"
FIRST = f"Bakara’da {AYAH} denildi."
HASR = "Elbette haşr-i cismânî olacak."
SOZLER = {
    "work": "sozler", "title": "Sözler", "group": "ana-cilt", "source": {},
    "outline": [
        {"id": "sozler", "parent_id": None, "title": "Sözler", "ref": "Sözler"},
        {"id": "sozler/10", "parent_id": "sozler", "title": "Onuncu Söz", "subtitle": "Haşre dâir",
         "ref": "Sözler › Onuncu Söz"},
        {"id": "sozler/10/hakikat-01", "parent_id": "sozler/10", "title": "Birinci Hakikat", "type": "Hakikat", "number": 1,
         "ref": "Sözler › Onuncu Söz › Birinci Hakikat"},
        {"id": "sozler/11", "parent_id": "sozler", "title": "Onbirinci Söz", "ref": "Sözler › Onbirinci Söz"},
    ],
    "paragraphs": [
        {"id": "sozler/10/p001", "node_id": "sozler/10", "kind": "paragraph",
         "text": f"{FIRST} {HASR}",
         "arabic": [{"start": 10, "end": 10 + len(AYAH), "kind": "ayet", "meal": "Allah’tan başka ilâh yoktur",
                     "source": "Bakara Sûresi, 2:255"}]},
        {"id": "sozler/10/p001/h1", "node_id": "sozler/10", "kind": "hasiye", "parent_id": "sozler/10/p001",
         "offset": len(FIRST), "anchor": "sozler/10/c001", "text": "Işık geldi."},
        {"id": "sozler/10/hakikat-01/p001", "node_id": "sozler/10/hakikat-01", "kind": "paragraph",
         "text": "Kıyâmet ve mîzan günü gelecek."},
        {"id": "sozler/11/p001", "node_id": "sozler/11", "kind": "arabic", "text": "قُلْ هُوَ اللّٰهُ اَحَدٌ",
         "arabic": [{"start": 0, "end": 24, "kind": "ayet", "meal": "", "source": "Sûre-i Bakara, 1’den"},
                    {"start": 0, "end": 3, "kind": "arabi", "meal": "", "source": "REF-YOK"}]},
    ],
    "notes": [{"node_id": "sozler/10", "after": "sozler/10/p001", "text": "kontrol"}],
    "gaps": [],
}
SOZLER["sentences"] = [
    {"id": "sozler/10/c001", "node_id": "sozler/10", "paragraph_id": "sozler/10/p001", "n": 1},
    {"id": "sozler/10/c002", "node_id": "sozler/10", "paragraph_id": "sozler/10/p001", "n": 2},
    {"id": "sozler/10/c001/h1/c001", "node_id": "sozler/10", "paragraph_id": "sozler/10/p001/h1", "n": 1},
    {"id": "sozler/10/hakikat-01/c001", "node_id": "sozler/10/hakikat-01",
     "paragraph_id": "sozler/10/hakikat-01/p001", "n": 1},
    {"id": "sozler/11/c001", "node_id": "sozler/11", "paragraph_id": "sozler/11/p001", "n": 1},
]
ASA = {
    "work": "asa-yi-musa", "title": "Asâ-yı Mûsâ", "group": "mecmua", "source": {},
    "outline": [
        {"id": "asa-yi-musa", "parent_id": None, "title": "Asâ-yı Mûsâ", "ref": "Asâ-yı Mûsâ"},
        {"id": "asa-yi-musa/haşir", "parent_id": "asa-yi-musa", "title": "Haşir", "ref": "Asâ-yı Mûsâ › Haşir",
         "sources": ["sozler/10"]},
    ],
    "paragraphs": [
        {"id": "asa-yi-musa/haşir/p001", "node_id": "asa-yi-musa/haşir", "kind": "paragraph",
         "source": ["sozler/10/p001"]},
        {"id": "asa-yi-musa/haşir/p002", "node_id": "asa-yi-musa/haşir", "kind": "paragraph",
         "text": "Bu mecmûa haşre dâirdir."},
    ],
    "sentences": [
        {"id": "asa-yi-musa/haşir/c001", "node_id": "asa-yi-musa/haşir", "paragraph_id": "asa-yi-musa/haşir/p002",
         "n": 1},
    ],
    "notes": [], "gaps": [],
}


def _complete(book: dict, texts: dict[str, list[str]]) -> dict:
    """Cümleleri paragraf metninden sırayla keser; konumları elle yazmak gerekmez."""
    paragraphs = {p["id"]: p.get("text") for p in book["paragraphs"]}
    pieces = {pid: iter(t) for pid, t in texts.items()}
    for s in book["sentences"]:
        text = next(pieces[s["paragraph_id"]])
        start = paragraphs[s["paragraph_id"]].index(text)
        s.update(start=start, end=start + len(text), text=text, incipit=text[:20], hash="0" * 12, ref=s["id"])
    return book


@pytest.fixture(scope="session")
def small_db(tmp_path_factory) -> tuple:
    """(veritabanı yolu, kurulum raporu)"""
    books = tmp_path_factory.mktemp("books")
    sentences = {"sozler/10/p001": [FIRST, HASR], "sozler/10/p001/h1": ["Işık geldi."],
                 "sozler/10/hakikat-01/p001": ["Kıyâmet ve mîzan günü gelecek."],
                 "sozler/11/p001": ["قُلْ هُوَ اللّٰهُ اَحَدٌ"], "asa-yi-musa/haşir/p002": ["Bu mecmûa haşre dâirdir."]}
    for book in (SOZLER, ASA):
        data = _complete(book, sentences)
        (books / f"{book['work']}.json").write_text(json.dumps(data, ensure_ascii=False), "utf-8")
    out = books / "test.db"
    report: BuildReport = build(books, out)
    return out, report
