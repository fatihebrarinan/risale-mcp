"""Arapça parçaların türü: Kur'ân metni, meal kaydı, işaretler ve bağlam."""

import pytest

from risale_mcp.arabic_kinds import Classifier, _citation, _context
from risale_mcp.quran import Quran


@pytest.fixture
def classifier():
    data = {"suras": [{"number": 2, "name": "x", "ayahs": [
        {"ayah": 1, "text": "وَالَّذِينَ يُؤْمِنُونَ بِالْغَيْبِ", "text_clean": "والذين يؤمنون بالغيب"},
        {"ayah": 2, "text": "فَانْكِحُوا مَا طَابَ لَكُمْ", "text_clean": "فانكحوا ما طاب لكم"},
        {"ayah": 3, "text": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ", "text_clean": "الحمد لله رب العالمين"},
    ]}]}
    meal = {}
    books = {"e": {"paragraphs": [{"text": "خير الناس انفعهم للناس", "arabic": [{"start": 0, "end": 22, "kind": "hadis", "source": "Beyhakî"}]}]}}
    return Classifier(Quran(data), meal, books)


def decide(classifier, text, before="", after="", kind="arabi", source=None, language="tr"):
    part = {"kind": kind, "start": 0, "end": len(text), "source": source}
    return classifier.decide(part, text, before, after, language)


def test_source_marks_are_never_changed(classifier):
    assert decide(classifier, "فانكحوا ما طاب لكم", kind="hadis").kind == "hadis"


def test_text_found_in_the_quran_is_a_verse_with_its_address(classifier):
    d = decide(classifier, "وَالَّذِينَ يُؤْمِنُونَ بِالْغَيْبِ")
    assert (d.kind, d.kind_source) == ("ayet", "kuran") and d.source.endswith("2:1")


def test_formula_stays_arabic_even_if_in_the_quran(classifier):
    assert decide(classifier, "الْحَمْدُ لِلَّهِ").kind == "arabi"


def test_hadith_mark_carries_to_the_same_arabic(classifier):
    d = decide(classifier, "خَيْرُ النَّاسِ اَنْفَعُهُمْ لِلنَّاسِ")
    assert (d.kind, d.kind_source, d.source) == ("hadis", "erisale", "Beyhakî")


def test_bibliography_of_a_hadith_book(classifier):
    d = decide(classifier, "لكل اية ظهر وبطن", source="Hadisten iktibas: Ebû Yâ'lâ, el-Müsned 9:287")
    assert (d.kind, d.kind_source) == ("hadis", "kaynakca")


def test_context_gives_only_a_candidate_and_hadise_is_not_hadith(classifier):
    assert decide(classifier, "من لم يشكر الناس لم يشكر الله", after=" hadîs-i şerifinin sırrıyla").kind_source == "baglam"
    assert decide(classifier, "من لم يشكر الناس لم يشكر الله", before="EMİRDAĞI'NDAKİ BİR HADİSE)").kind == "arabi"


def test_context_words_in_each_language():
    assert _context("", " âyeti imdada geldi", "tr") == (True, False)
    assert _context("Peygamber (asm) ferman etmiş ki: ", "", "tr") == (False, True)
    assert _context("", " حديثنڭ حقيقتى", "os") == (False, True)


def test_citation_part_of_a_meal_record():
    assert _citation('"Ümmetimin helâki." Buharî, Fiten: 3.') == "Buharî, Fiten: 3."
