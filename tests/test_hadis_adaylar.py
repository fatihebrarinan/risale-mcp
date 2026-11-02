import math

from risale_mcp.hadis import Report
from risale_mcp.hadis_adaylar import Index, close, excerpt, hint, measure, stem, stems


def report(i: int, text: str) -> Report:
    return Report(f"t:{i}", "Kitap", str(i), text, "sanadset")


def idf(*words_: str) -> dict[str, float]:
    return {w: 1.0 for w in words_}


def test_stem_removes_article_and_pronoun():
    assert stem("لجنت") == "جنت"
    assert stem("علمه") == "علم"
    assert stem("كتب") == "تب"      # bilinen sınır: kökün ilk harfi de ön ek sanılır, "بكتب" ile ayrı düşer
    assert stem("به") == "به"       # iki harf kalmazsa dokunulmaz


def test_adjacency_separates_a_phrase_from_scattered_words():
    query = stems("الضرورات تبيح المحظورات")
    weights = dict.fromkeys(query, 1.0)
    phrase = measure(query, stems("قال الضرورات تبيح المحظورات وهو كلام"), weights)
    scattered = measure(query, stems("الضرورات شيء تبيح امر اخر المحظورات"), weights)
    assert phrase.adjacency == 1 and phrase.value == 1
    assert scattered.coverage == 1 and scattered.adjacency == 0 and scattered.value < phrase.value


def test_window_stays_near_the_part():
    query = ["ا1", "ب1"]
    score = measure(query, ["ا1", *["س"] * 20, "ب1"], {"ا1": 1.0, "ب1": 1.0})
    assert score.coverage == 0.5


def test_hint_abridged_needs_order_and_gaps():
    query = ["ا1", "ب1", "ج1", "د1"]
    weights = dict.fromkeys(query, 1.0)
    assert hint(measure(query, ["ا1", "س", "ب1", "ص", "ج1", "ط", "د1"], weights)) == "abridged"


def test_close_has_no_threshold_under_five_words():
    assert not close(4, 1.0)
    assert not close(6, 0.89) and close(6, 0.9)
    assert close(12, 0.5)


def test_excerpt_counts_the_same_words_as_stems():
    text = "قَالَ : يَا اَلْجَنَّةُ تَحْتَ الْخ اَقْدَامِ"
    assert len(stems(text)) == len(excerpt(text, 0, 99).split())
    assert "تَحْتَ" in excerpt(text, 1, 2)


def test_search_finds_the_variant_and_drops_copies():
    filler = [report(i, f"حدثنا رجل{i} عن ابيه") for i in range(20)]
    near = report(100, "قال الضرورات تبيح المحظورات كلام صحيح")
    copy = report(101, "قال الضرورات تبيح المحظورات كلام صحيح")
    other = report(102, "الضرورات في الكلام")
    index = Index([*filler, near, copy, other])
    found = index.search("ان الضرورات تبيح المحظورات", 5)
    assert found[0].report == 20
    assert 21 not in [s.report for s in found]
    assert math.isclose(found[0].adjacency, 1.0) or found[0].adjacency > 0.5


def test_single_word_is_not_searched():
    assert Index([report(1, "الضرورات")]).search("الضرورات") == []
