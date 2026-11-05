"""Metinden metne bağlar (T4): hedefin atfı, iki yönlü okuma, yalnız yerelde duran esere sızma koruması, kararı ekleme.

Küçük veritabanının eserleri (`conftest.small_db`) kendi bağ klasörüyle yeniden kurulur; gerçek `data/links`'e dokunulmaz.
"""

import json
import sqlite3

import pytest

from risale_mcp import link_reviews
from risale_mcp.build_db import build
from risale_mcp.library import Library
from risale_mcp.links import Link, check, cite_as, write
from risale_mcp.profiles import GENEL, KISISEL

BEYZAVI_SHOWN = "Envârü't-Tenzîl › سورة البقرة › آية 6 › “إن الذين كفروا…” ile başlayan 2 cümle"
LEMALAR_SHOWN = "Lem'alar › Birinci Lem'a › “Bir…”"


def _links(conn) -> list[Link]:
    def shown(value):
        return cite_as(conn, value)
    scholar = {"method": "scholar", "strength": "strong"}
    return [
        Link("sozler/10/c001", "risale:sozler/10/hakikat-01/c001", "quote", relation="same_words",
             display=shown("sozler/10/c001"), target_display=shown("sozler/10/hakikat-01/c001"), **scholar),
        Link("risale:sozler/11/c001", "tefsir:beyzavi/2/6/c001..c002", "relation", relation="same_view",
             display=shown("sozler/11/c001"), target_display=BEYZAVI_SHOWN, **scholar),       # yalnız yerelde duran eser
        Link("sozler/10/c001..c002", "risale:sozler/11", "relation", relation="different_view", **scholar),
        Link("sozler/10/c002", "risale:lemalar/1/c001", "relation", relation="same_view", **scholar),   # atıf yok
        Link("sozler/10/c002", "risale:lemalar/1/c002", "relation", relation="same_view",
             target_display=LEMALAR_SHOWN, **scholar),
    ]


@pytest.fixture(scope="module")
def built(small_db, tmp_path_factory):
    books = small_db[0].parent
    folder = tmp_path_factory.mktemp("text_links")
    links = folder / "links"
    conn = sqlite3.connect(small_db[0])
    write(links / "risale" / "scholar.jsonl", _links(conn), producer="test")
    (links / "reviews").mkdir()
    (links / "reviews" / "reviewers.json").write_text(json.dumps({"reviewers": {"a": {"name": "Denetçi A", "number": 1}}}), "utf-8")
    out = {}
    for profile in (KISISEL, GENEL):
        db = folder / f"{profile.name}.db"
        out[profile.name] = (db, build(books, db, profile=profile, links_dir=links))
    return out, links


def test_cite_as_comes_from_the_data(small_db):
    conn = sqlite3.connect(small_db[0])
    ref, incipit = conn.execute("SELECT ref, incipit FROM sentences WHERE id = 'sozler/10/c001'").fetchone()
    assert cite_as(conn, "sozler/10/c001") == f"{ref.rsplit(' › ', 1)[0]} › “{incipit}…”"
    assert cite_as(conn, "sozler/10/c001..c002").endswith("ile başlayan 2 cümle")    # hâşiye cümlesi sayılmaz
    assert cite_as(conn, "risale:sozler/10") == conn.execute("SELECT ref FROM nodes WHERE id = 'sozler/10'").fetchone()[0]
    assert cite_as(conn, "sozler/99/c001") is None


def test_private_targets_stay_out_of_the_public_profile(built):
    out, _ = built
    kisisel, genel = out["kisisel"][1].counts, out["genel"][1].counts
    assert kisisel["links"] == 4 and kisisel["links_target_no_display"] == 1         # metni yok, atfı yok: girmez
    assert genel["links"] == 3 and genel["links_target_private"] == 1                # Beyzâvî genel profilde yok
    rows = sqlite3.connect(out["genel"][0]).execute("SELECT target FROM links WHERE target LIKE 'tefsir:%'").fetchall()
    assert rows == []


def test_text_links_read_both_directions(built):
    out, _ = built
    lib = Library(out["kisisel"][0])
    first = lib.text_links("sozler/10/c001")["links"]
    assert {(l["direction"], l["other"], l["relation"]) for l in first} == {
        ("out", "sozler/10/hakikat-01/c001", "same_words"), ("out", "sozler/11", "different_view")}   # aralık da dokunur
    back = lib.text_links("sozler/10/hakikat-01")["links"]
    assert [(l["direction"], l["other"]) for l in back] == [("in", "sozler/10/c001")]
    eleven = {l["other"]: l for l in lib.text_links("sozler/11")["links"]}
    beyzavi = eleven["beyzavi/2/6/c001..c002"]
    assert beyzavi["available"] is False and beyzavi["cite_as"] == BEYZAVI_SHOWN     # metni burada yok: kayıtlı atıf
    assert eleven["sozler/10/c001..c002"]["direction"] == "in" and eleven["sozler/10/c001..c002"]["available"]
    elsewhere = lib.text_links("sozler/10/c002")["links"]
    assert [(l["other"], l["available"], l["cite_as"]) for l in elsewhere if l["other"].startswith("lemalar")] == [
        ("lemalar/1/c002", False, LEMALAR_SHOWN)]
    lib.close()


def test_check_catches_a_moved_target(small_db):
    conn = sqlite3.connect(small_db[0])
    good = Link("sozler/10/c001", "risale:sozler/10/hakikat-01/c001", "quote", "scholar", relation="same_words",
                target_display=cite_as(conn, "sozler/10/hakikat-01/c001"))
    moved = Link("sozler/10/c001", "risale:sozler/10/hakikat-01/c001", "quote", "scholar", relation="same_words",
                 target_display="Sözler › “Başka bir cümle…”")
    assert check(conn, [good]) == {}
    assert list(check(conn, [moved])) == ["target_moved"]


def test_add_appends_a_review_of_an_existing_link(built):
    out, links = built
    conn = sqlite3.connect(out["kisisel"][0])
    root = links / "reviews"
    key = {"source": "risale:sozler/10/c001", "target": "risale:sozler/10/hakikat-01/c001", "type": "quote"}
    with pytest.raises(ValueError, match="gerekçe"):                                 # metinden metne: gerekçe zorunlu
        link_reviews.add(conn, "risale/scholar.jsonl", key, "reviewed", "a", "2026-11-04", "strong", root=root)
    review = link_reviews.add(conn, "risale/scholar.jsonl", key, "reviewed", "a", "2026-11-04", "strong",
                              reason="aynı söz", root=root)
    assert review.link["source"] == "sozler/10/c001"                                 # anahtar öneksiz
    assert review.seen == {"relation": "same_words", "strength": "strong", "scope": "sentence"}
    with pytest.raises(ValueError, match="bağ yok"):
        link_reviews.add(conn, "risale/scholar.jsonl", {**key, "type": "relation"}, "reviewed", "a", "2026-11-04", root=root)
    with pytest.raises(ValueError, match="gerekçe"):
        link_reviews.add(conn, "risale/scholar.jsonl", key, "disputed", "a", "2026-11-04", root=root)
    with pytest.raises(ValueError, match="denetçi"):
        link_reviews.add(conn, "risale/scholar.jsonl", key, "reviewed", "model", "2026-11-04", root=root)
    assert len(link_reviews.read(root)) == 1
