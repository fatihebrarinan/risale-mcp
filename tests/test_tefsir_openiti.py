"""Ortak tefsir ayrıştırıcısı (`books/tefsir_openiti.py`, MVP M2): çapa zinciri, satır bölme, altafsir birimleri."""

from risale_mcp import openiti
from risale_mcp.books import tefsir_openiti as t


def test_chain_keeps_order_and_ignores_a_wrong_far_candidate():
    # ikincinin en güçlü adayı yanlış ve çok ileride (900): seçilirse üçüncü (300) kaybolurdu; birim sayısı önce gelir
    cands = [[(100, 1.0)], [(900, 3.0), (200, 1.0)], [(300, 1.0)]]
    assert t._chain(cands) == [100, 200, 300]


def test_chain_leaves_out_a_unit_that_does_not_fit():
    cands = [[(100, 1.0)], [(50, 1.0)], [(300, 1.0)]]        # ikinci birimin tek adayı sıraya uymuyor
    assert t._chain(cands) == [100, None, 300]


def test_altafsir_units_and_sura_names():
    raw = ("### | [2 - سورة البقرة]\n### || [2.6]\n# { إن الذين كفروا } لما ذكر خاصة عباده\n"
           "### || [2.7-8]\n# ختم الله على قلوبهم\n")
    units, names = t.altafsir_units(raw)
    assert names == {2: "سورة البقرة"}
    assert [(u.sura, u.start, u.end) for u in units] == [(2, 6, 6), (2, 7, 8)]
    assert units[0].words[:3] == t.skeleton_words("إن الذين كفروا")


def test_a_line_is_cut_where_the_unit_starts():
    page = openiti.Page(1, 10)
    p = openiti.Paragraph("raw", "آخر شرح الآية السابقة ختم الله على قلوبهم", None, [], [(5, page)], page, page)
    lines, where = t._split_lines([p], [(0, 22)])
    assert [l.text for l in lines] == ["آخر شرح الآية السابقة", "ختم الله على قلوبهم"]
    assert where == [1]
    assert lines[0].breaks == [(5, page)] and lines[1].page == openiti.Page(1, 11)
