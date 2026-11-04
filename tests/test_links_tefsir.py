"""Müfessirin bağları (`links_tefsir.py`, T5): işaretsiz Kur'ân alıntısı, lemma, hadis adayı, ölçüm."""

import sqlite3

from risale_mcp import links_tefsir as lt
from risale_mcp.quran import Quran

FATIHA = ["بسم الله الرحمن الرحيم", "الحمد لله رب العالمين", "الرحمن الرحيم", "مالك يوم الدين",
          "إياك نعبد وإياك نستعين", "اهدنا الصراط المستقيم",
          "صراط الذين أنعمت عليهم غير المغضوب عليهم ولا الضالين"]
OTHER = ["الذين يؤمنون بالغيب ويقيمون الصلاة", "وآخر دعواهم أن الحمد لله رب العالمين"]


def _quran() -> lt.QuranWords:
    def sura(number, texts):
        return {"number": number, "name": str(number), "ayahs": [
            {"ayah": k, "text": t, "text_simple": t, "text_clean": t, "translations": {}} for k, t in enumerate(texts, 1)]}
    return lt.QuranWords(Quran({"suras": [sura(1, FATIHA), sura(2, OTHER)]}))


QW = _quran()


def test_lemma_is_the_units_own_verse_at_the_sentence_start():
    quotes, ambiguous = lt.find_quotes(QW, "b/1/5/c001", "إياك نعبد وإياك نستعين ثم إنه لما ذكر الحقيق", (1, 5, 5))
    assert [(q.text, q.place, q.lemma, q.own) for q in quotes] == [("إياك نعبد وإياك نستعين", (1, 5, 5), True, True)]
    assert ambiguous == 0


def test_own_verse_is_found_with_fewer_words_only_at_the_sentence_start():
    text = "اهدنا الصراط يعني البيان"
    assert [(q.text, q.lemma) for q in lt.find_quotes(QW, "s", text, (1, 6, 6))[0]] == [("اهدنا الصراط", True)]
    assert lt.find_quotes(QW, "s", text, (2, 1, 1))[0] == []          # başka birimde iki kelime yetmez
    assert lt.find_quotes(QW, "s", "ثم اهدنا الصراط يعني", (1, 6, 6))[0] == []   # cümle ortasında da (T7, A25)


def test_other_verses_need_a_unique_place():
    quotes, ambiguous = lt.find_quotes(QW, "s", "كما قال الذين يؤمنون بالغيب ويقيمون الصلاة فهذا", (1, 2, 2))
    assert [(q.text, q.place, q.own) for q in quotes] == [("الذين يؤمنون بالغيب ويقيمون الصلاة", (2, 1, 1), False)]
    quotes, ambiguous = lt.find_quotes(QW, "s", "ثم قال الحمد لله رب العالمين وهذا", None)     # iki yerde: numara yok
    assert quotes == [] and ambiguous == 1
    own, _ = lt.find_quotes(QW, "s", "ثم قال الحمد لله رب العالمين وهذا", (1, 2, 2))   # kendi âyeti seçilir
    assert own[0].place == (1, 2, 2)


def test_words_keep_their_boundaries():
    assert lt.find_quotes(QW, "s", "المالكين يوم الدينار", (1, 4, 4))[0] == []     # kelimenin parçası alıntı değil


def test_hadith_candidates_need_a_cue_before_the_guillemets():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE sentences (id TEXT, work TEXT, text TEXT, seq INTEGER)")
    conn.executemany("INSERT INTO sentences VALUES (?, 'beyzavi', ?, ?)", [
        ("a", "لقوله عليه الصلاة والسلام «كل أمر ذي بال لا يبدأ فيه»", 1),
        ("b", "وقرئ «صراط من أنعمت عليهم» وهو شاذ", 2)])
    assert lt.hadith_candidates(conn) == [("a", "كل أمر ذي بال لا يبدأ فيه")]


def test_measure_counts_overlaps_both_ways():
    quotes = [lt.Quote("s", 0, 0, "اهدنا الصراط المستقيم", (1, 6, 6), True, True, 1),
              lt.Quote("s", 0, 0, "ما تقدم من ذنبك", (48, 2, 2), False, False, 1)]
    m = lt.measure(quotes, [" ".join(t[2] for t in lt._tokens("الصراط المستقيم")), "نستعين"])
    assert (m["bulunan"], m["isabet"], m["jk_isaretli"], m["kapsanan"]) == (2, 1, 1, 1)


def test_review_rules_formula_words_and_mid_sentence_own_verse():
    """T7: "قائل" alıntının başı olmaz (A24); kendi âyetinin iki kelimesi cümle ortasında alıntı sayılmaz (A25)."""
    quotes, _ = lt.find_quotes(QW, "s", "بقوله عز من قائل الذين يؤمنون بالغيب ويقيمون الصلاة", (2, 1, 1))
    assert [q.text for q in quotes] == ["الذين يؤمنون بالغيب ويقيمون الصلاة"]
    assert lt.find_quotes(QW, "s", "فإنه لما اهدنا الصراط خفي", (1, 6, 6))[0] == []
    assert [q.lemma for q in lt.find_quotes(QW, "s", "اهدنا الصراط بيان", (1, 6, 6))[0]] == [True]
