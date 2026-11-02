from risale_mcp.hadis import Corpus, Report
from risale_mcp.hadis_uyum import level


def test_level_order():
    found = [("Buhârî", 3), ("Müsned", None)]
    assert level(found, {("Buhârî", 3)}, {"Buhârî"}) == "chapter"
    assert level(found, {("Buhârî", 9)}, {"Buhârî"}) == "book"
    assert level(found, set(), {"Müsned"}) == "book"
    assert level(found, set(), {"Tirmizî"}) == "absent"
    assert level(found, set(), set()) == "no_corpus"


def test_match_limit_does_not_change_the_found_set():
    reports = [Report(f"t:{i}", f"K{i}", str(i), "الضرورات تبيح المحظورات عند الحاجة", "sanadset") for i in range(12)]
    corpus = Corpus(reports)
    text = "الضرورات تبيح المحظورات عند الحاجة"
    kind, chosen, total = corpus.match(text)
    assert (kind, len(chosen), total) == ("found", 8, 12)
    assert len(corpus.match(text, limit=None)[1]) == 12
