"""Tefsirlerin ön metni (`books/tefsir_openiti.FRONT`): kısımların sınırları baskının satırlarından bulunur."""

import pytest

from risale_mcp import openiti
from risale_mcp.auth import AuthStore
from risale_mcp.books.tefsir_openiti import FRONT, Front, _front_segments, _title_line


def _p(text):
    return openiti.Paragraph(text, text, None, [], [], None, None, None)


LINES = [_p(t) for t in ("بسم الله الرحمن الرحيم", "الحمد لله", "بسم الله الرحمن الرحيم", "فاتحة الكتاب", "2 -",
                         "2 - قوله")]


def test_segments_in_order_exact_and_nth():
    plan = [Front("mukaddime", None, "مقدمة المؤلف", printed=False),
            Front("sura", "=بسم الله الرحمن الرحيم", nth=1), Front("unit", "=2 -", verses=(1, 2, 7))]
    assert [i for _, i in _front_segments(LINES, plan)] == [0, 2, 4]
    # nth sayar, aramanın önceki kısımdan sonra başladığını unutmadan
    assert _front_segments(LINES, [Front("sura", "=بسم الله الرحمن الرحيم", nth=2)])[0][1] == 2


def test_missing_part_stops_the_build():
    with pytest.raises(ValueError):
        _front_segments(LINES, [Front("mukaddime", "مقدمة المصنف", "مقدمة المصنف")])


def test_title_line_ignores_star_and_footnote_mark():
    assert _title_line(_p("* مقدمة التحقيق"), "مقدمة التحقيق")
    assert _title_line(_p("مقدمة ابن كثير (1)"), "مقدمة ابن كثير")


def test_every_layer_says_whose_it_is():
    for slug, plan in FRONT.items():
        for f in plan:
            if f.kind in ("mukaddime", "tahkik"):
                assert f.title, slug
            if f.kind == "tahkik":
                assert f.local and f.local != "mukaddime", slug
            if f.kind == "unit":
                assert f.verses, slug


def test_usage_is_tagged_with_server(tmp_path):
    db = tmp_path / "auth.db"
    genel, hadis = AuthStore(db), AuthStore(db, server="hadis")
    genel.log(None, None, "tools/call", "semantic_search", 5, None)
    hadis.log(None, None, "tools/call", "semantic_search", 5, None)
    hadis.log(None, None, "tools/call", "semantic_search", 5, None)
    assert genel.anonymous_calls("semantic_search", 0) == 1
    assert hadis.anonymous_calls("semantic_search", 0) == 2


def test_hadis_units_enter_the_manifest():
    import sqlite3

    from risale_mcp.manifest import Manifest, diff

    def db(text):
        conn = sqlite3.connect(":memory:")
        conn.executescript("CREATE TABLE lib_units (seq INTEGER PRIMARY KEY, id TEXT, node_id TEXT, text TEXT);"
                           "CREATE TABLE lib_nodes (seq INTEGER PRIMARY KEY, id TEXT, title TEXT);"
                           "INSERT INTO lib_nodes VALUES (1, 'bukhari/k01', 'كتاب');")
        conn.execute("INSERT INTO lib_units VALUES (1, 'bukhari/1', 'bukhari/k01', ?)", (text,))
        return Manifest.from_db(conn)

    assert [s[0] for s in db("إنما الأعمال").sentences] == ["bukhari/1"]
    assert diff(db("إنما الأعمال"), db("إنما الأعمال بالنيات")).breaking      # metni değişen hadis durdurur


def test_default_scope_only_where_the_corpus_is():
    from risale_mcp.library import Library
    from risale_mcp.profiles import TEFSIR

    if not TEFSIR.db.exists():
        pytest.skip("tefsir veritabanı yok")
    assert Library(TEFSIR.db, TEFSIR.vectors).search("الختم", limit=1)["total"] > 0
