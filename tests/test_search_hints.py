"""S13.11: aramanın az ve sıfır sonuçtaki ipuçları (genel veritabanıyla)."""

import pytest

from risale_mcp.profiles import GENEL

pytestmark = pytest.mark.skipif(not GENEL.db.exists(), reason="genel veritabanı yok")


@pytest.fixture(scope="module")
def library():
    from risale_mcp.library import Library
    return Library(GENEL.db, GENEL.vectors)


def test_few_hits_report_word_starts(library):
    # "tezekkür" yalnız tam kelime: 2; "tezekkürde" gibi ekli biçimlerle daha çok (model "iki yerde geçer" diyordu)
    result = library.search("tezekkür")
    assert result["total"] == 2
    assert result["word_starts"]["total"] > 2 and "*" in result["word_starts"]["note"]
    assert "word_starts" not in library.search("tefekkür")                  # çok sonuçta yok
    assert "word_starts" not in library.search("tezekkür*")                 # zaten kelime başı


def test_latin_arabic_gets_hint(library):
    result = library.search("lealleküm tetefekkerûn")
    assert result["total"] == 0 and "Arabic letters" in result["hint"]
    assert "hint" not in library.search("لعلكم تتفكرون")
