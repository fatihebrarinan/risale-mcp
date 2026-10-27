"""Aşama 13: Kur'ân katmanı ve Risale'deki âyetlerin Kur'ân metniyle eşlenmesi.

Eşleme `conftest.py`'deki küçük Kur'ân'la (ve buna eklenen, Bakara ile aynı başlayan bir sûreyle) sınanır.
"""

import json
import sqlite3

import pytest

from conftest import mini_quran
from risale_mcp.build_db import build
from risale_mcp.quran import Match, Quran, _mark_spans, pieces, skeleton, sura_ref


@pytest.fixture(scope="module")
def quran() -> Quran:
    data = mini_quran()
    data["suras"].insert(1, {"number": 3, "name": "Âl-i İmrân", "name_ar": "آل عمران", "ayahs": [
        {"ayah": 1, "text": "الٓمٓ", "text_simple": "الٓمٓ", "text_clean": "الم", "translations": {}}]})
    return Quran(data)


@pytest.mark.parametrize("risale,tanzil", [
    ("اَللّٰهُ لَٓا اِلٰهَ اِلَّا هُوَ", "ٱللَّهُ لَآ إِلَـٰهَ إِلَّا هُوَ"),        # Türk mushafı imlâsı / Medine hattı
    ("﷽", "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ"),                               # bağlama
    ("رَحْمَةِ اللّٰهِ", "رَحْمَتِ ٱللَّهِ"),                                         # tâ-i merbûta = açık tâ
    ("الصَّلٰوةَ", "ٱلصَّلَوٰةَ"),
])
def test_skeleton_ignores_spelling_differences(risale, tanzil):
    assert skeleton(risale) == skeleton(tanzil)


def test_pieces_split_at_ellipsis_and_etc():
    assert pieces("اَللّٰهُ لَٓا اِلٰهَ اِلَّا هُوَ… اَلْقَيُّومُ اَلْخ") == [skeleton("اَللّٰهُ لَٓا اِلٰهَ اِلَّا هُوَ"),
                                                                       skeleton("اَلْقَيُّومُ")]


def test_check_against_the_named_verse(quran):
    kursi = "اَللّٰهُ لَٓا اِلٰهَ اِلَّا هُوَ الْحَيُّ الْقَيُّومُ"
    assert quran.check(kursi, 2, 255, 255) == "exact"
    assert quran.check(kursi, 2, 254, 254) == "near"                        # metin komşu âyette
    assert quran.check(kursi, 2, 100, 100) == "differs"
    assert quran.check("…", 2, 1, 1) == "empty"


def test_locate_numbered_and_bracketed(quran):
    numbered = quran.locate("قُلْ هُوَ اللّٰهُ اَحَدٌ﴿١﴾")
    assert [(q.match, q.number) for q in numbered] == [(Match(112, 1, 1), 1)]
    bracketed = quran.locate("وكما قال: ﴿ اَللّٰهُ لَٓا اِلٰهَ اِلَّا هُوَ ﴾ فافهم")
    assert bracketed[0].match == Match(2, 255, 255) and bracketed[0].number is None
    assert quran.locate("﴿ الٓمٓ ﴾") == []                                  # numarasız ve kısa: aranmaz
    ambiguous = quran.locate("الٓمٓ﴿١﴾")[0]                                  # Bakara 1 de Âl-i İmrân 1 de
    assert ambiguous.match is None
    assert quran.in_sura(ambiguous, 3) == Match(3, 1, 1)


def test_grouped_translation_spans():
    ayahs = [{"ayah": n, "translations": {"diyanet-isleri": t, "diyanet-vakfi": str(n)}}
             for n, t in enumerate(["a", "b", "b", "b", "c"], 1)]
    _mark_spans(ayahs)
    assert [a.get("spans") for a in ayahs] == [None, {"diyanet-isleri": [2, 4]}, {"diyanet-isleri": [2, 4]},
                                               {"diyanet-isleri": [2, 4]}, None]


def test_sura_ref():
    assert sura_ref(2, 255) == "Bakara Sûresi, 2:255"
    assert sura_ref(99, 7, 8) == "Zilzâl Sûresi, 99:7-8"


def test_build_links_unmarked_verses_and_uses_the_section_sura(tmp_path, quran):
    """Hizb paragrafı: numaralı âyetler; kısa ve iki sûrede geçen âyet bölümün öbür âyetlerinin sûresinde."""
    texts = ["اَللّٰهُ لَٓا اِلٰهَ اِلَّا هُوَ الْحَيُّ الْقَيُّومُ﴿٢٥٥﴾", "الٓمٓ﴿١﴾"]
    paragraphs, sentences = [], []
    for i, text in enumerate(texts, 1):
        pid = f"hizbul-kuranil-muazzam/2-bakara/p{i:03}"
        paragraphs.append({"id": pid, "node_id": "hizbul-kuranil-muazzam/2-bakara", "kind": "arabic", "text": text,
                           "arabic": [{"start": 0, "end": len(text), "kind": "arabi", "meal": "", "source": "REF-YOK"}]})
        sentences.append({"id": f"hizbul-kuranil-muazzam/2-bakara/c{i:03}", "node_id": "hizbul-kuranil-muazzam/2-bakara",
                          "paragraph_id": pid, "n": i, "start": 0, "end": len(text), "text": text, "incipit": text,
                          "hash": "0" * 12, "ref": "x"})
    book = {"work": "hizbul-kuranil-muazzam", "title": "Hizb", "group": "hizb", "source": {},
            "outline": [{"id": "hizbul-kuranil-muazzam", "parent_id": None, "title": "Hizb", "ref": "Hizb"},
                        {"id": "hizbul-kuranil-muazzam/2-bakara", "parent_id": "hizbul-kuranil-muazzam",
                         "title": "2-Bakara", "ref": "Hizb › 2-Bakara"}],
            "paragraphs": paragraphs, "sentences": sentences, "notes": [], "gaps": []}
    books, out = tmp_path / "books", tmp_path / "test.db"
    books.mkdir()
    (books / "hizbul-kuranil-muazzam.json").write_text(json.dumps(book, ensure_ascii=False), "utf-8")
    quran_path = tmp_path / "quran.json"
    quran_path.write_text(json.dumps(quran.data, ensure_ascii=False), "utf-8")
    report = build(books, out, quran_path)
    rows = sqlite3.connect(out).execute(
        "SELECT sentence_id, sura, ayah_start, ayah_end FROM ayah_quotes ORDER BY paragraph_id").fetchall()
    assert rows == [("hizbul-kuranil-muazzam/2-bakara/c001", 2, 255, 255),
                    ("hizbul-kuranil-muazzam/2-bakara/c002", 2, 1, 1)]
    assert report.located["bulundu"] == 2
