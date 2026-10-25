"""Türkçe metin yardımcıları."""

import pytest

from risale_mcp.normalize import fold, ordinal_word, parse_ordinal, slugify, tr_lower, tr_title


@pytest.mark.parametrize("word,n", [
    ("Birinci", 1), ("İKİNCİ", 2), ("Onuncu", 10), ("Onbirinci", 11), ("Yirminci", 20),
    ("YİRMİBEŞİNCİ", 25), ("Otuzüçüncü", 33), ("Onbesinci", 15), ("Kitab", None),
])
def test_parse_ordinal(word, n):
    assert parse_ordinal(word) == n


def test_ordinal_word_roundtrip():
    for n in range(1, 50):
        assert parse_ordinal(ordinal_word(n)) == n
    assert ordinal_word(2) == "İkinci"


def test_turkish_case():
    assert tr_lower("IŞIK İSLÂM") == "ışık islâm"
    assert tr_title("BİRİNCİ SIR") == "Birinci Sır"
    assert tr_title("ONDOKUZUNCU VE OTUZBİRİNCİ") == "Ondokuzuncu ve Otuzbirinci"


def test_fold_removes_only_circumflex_and_apostrophes():
    assert fold("Hâtime İSLÂM") == "hatime islam"
    assert fold("çğöşü") == "çğöşü"
    assert fold("Lem'a") == fold("Lem’a") == fold("Lem‘a") == "lema"


def test_slugify():
    assert slugify("Hâtime") == "hatime"
    assert slugify("Mes'ele") == slugify("Mes‘ele") == "mesele"
