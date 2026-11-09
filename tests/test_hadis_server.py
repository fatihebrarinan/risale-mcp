"""Hadis sunucusu (MVP M5): `hadis_db.py`'nin kurduğu veritabanı varsa gerçek veriyle; yoksa atlanır."""

import pytest

from risale_mcp.library import LibraryError
from risale_mcp.profiles import PROFILES


@pytest.fixture(scope="module")
def lib():
    from risale_mcp.hadis_library import HadisLibrary
    p = PROFILES["hadis"]
    if not p.db.exists():
        pytest.skip("hadis.db yok (uv run python -m risale_mcp.hadis_db)")
    return HadisLibrary(p.db, p.vectors)


def test_the_unit_is_the_report_with_the_editions_number(lib):
    r = lib.report("musned/7422")
    assert r["number"] == 7422 and r["cite_as"].startswith("Müsned (Ahmed b. Hanbel), no. 7422")


def test_other_scholars_layers_are_kept_apart(lib):
    r = lib.report("mustedrek/51")
    assert r["layers"][0]["by"].startswith("Zehebî") and r["layers"][0]["text"] not in r["text"]


def test_books_without_numbers_use_the_librarys_sequence(lib):
    assert "sıra s00007 (baskıda numara yok)" in lib.cite_reports(["sifa/s00007"])["bibliography"]


def test_a_split_chapter_is_numbered_continuously(lib):
    found = lib.by_citation("Buharî, Ezân: 148")["citations"][0]
    assert found["found"] and all(r["id"].startswith("bukhari/") for r in found["reports"])


def test_kashf_al_khafa_carries_its_note(lib):
    hits = lib.search_reports('"ستفتح عليكم الشام"', book="kesfulhafa")["results"]
    assert hits and all("book_note" in h for h in hits)


def test_the_server_has_its_own_tools(lib):
    import asyncio

    from mcp import Client

    from risale_mcp.server import HADIS_INSTRUCTIONS, create_server
    server = create_server(lib, profile="hadis")

    async def names():
        async with Client(server) as client:
            return [t.name for t in (await client.list_tools()).tools]
    tools = asyncio.run(names())
    assert server.name == "hadis" and server.instructions == HADIS_INSTRUCTIONS
    assert {"get_hadith", "search_hadith", "find_by_citation", "cite", "get_ayah"} <= set(tools)
    assert "find_ayah" not in tools and "read_section" not in tools


def test_every_book_id_opens_its_outline(lib):
    for book in lib.books()["books"]:
        tree = lib.tree(book["id"], 1)
        assert tree["id"] == book["id"] and (tree.get("children") or tree.get("subsections") or tree["reports"])


def test_narrator_search_finds_the_report_in_its_chain(lib):
    # Nevvâs b. Sem'ân'ın Deccal hadisi: senet ayrı (Müslim) ve ayrı değil (Müsned) baskılarda (2026-11-09)
    ids = [r["id"] for r in lib.search_reports("الدجال", narrator="النواس بن سمعان", limit=20)["results"]]
    assert "muslim/2937" in ids and "musned/17629" in ids
    only = lib.search_reports(narrator="النواس بن سمعان", book="muslim")
    assert only["total"] and all(r["id"].startswith("muslim/") for r in only["results"])
    with pytest.raises(LibraryError):
        lib.search_reports("")


def test_ibn_and_bin_are_the_same_word(lib):
    # metin "المسيح بن مريم", sorgu "ابن مريم"
    assert "muslim/2937" in [r["id"] for r in lib.search_reports('"المسيح ابن مريم فينزل عند المنارة البيضاء"')["results"]]
    missed = lib.search_reports('"فبينما هو على ذلك إذ بعث الله المسيح ابن مريم"')
    assert missed["total"] == 0 and "narrator" in missed["note"]


def test_cite_checks_quotes_against_the_report(lib):
    # ChatGPT'nin 2026-11-07 cevabından: harekeli alıntı tutar, hafızadan lafız tutmaz ve asıl yeri gösterilir
    out = lib.cite_reports([
        {"id": "musned/17629", "quote": "فَبَيْنَا هُوَ عَلَى ذَلِكَ إِذْ بَعَثَ اللَّهُ الْمَسِيحَ ابْنَ مَرْيَمَ … فَيَقْتُلُهُ عِنْدَ بَابِ لُدٍّ الشَّرْقِيِّ"},
        {"id": "muslim/2937", "quote": "فبينا هو على ذلك إذ بعث الله المسيح ابن مريم"},
        {"id": "tirmidhi/2233"},
        {"id": "bukhari/99999999"}], first=3)
    status = {s["id"]: s["status"] for s in out["sources"]}
    assert status == {"musned/17629": "ok", "muslim/2937": "problem", "tirmidhi/2233": "ok", "bukhari/99999999": "problem"}
    assert "musned/17629" in out["sources"][1]["problem"]
    assert out["bibliography"].startswith("[3] Müsned") and "[5] Sünen-i Tirmizî" in out["bibliography"]


def test_cite_names_a_scholars_note(lib):
    row = lib.conn.execute("SELECT id, layers FROM lib_units WHERE book = 'mustedrek' AND layers IS NOT NULL LIMIT 1").fetchone()
    import json
    layer = json.loads(row["layers"])[0]
    words = " ".join(layer["text"].split()[:6])
    out = lib.cite_reports([{"id": row["id"], "quote": words}])
    if out["sources"][0]["status"] == "problem":           # söz rivayetin metninde de geçebilir
        assert "note on this report" in out["sources"][0]["problem"]


def test_the_older_ids_form_says_nothing_was_checked(lib):
    assert "no quotation was checked" in lib.cite_reports(["muslim/2937"], legacy=True)["note"]
    assert "no quotation was checked" not in lib.cite_reports([{"id": "muslim/2937", "quote": "ذات غداة"}])["note"]


def test_narrator_only_search_lists_the_six_books_first(lib):
    r = lib.search_reports(narrator="النواس بن سمعان", limit=20)
    ids = [x["id"] for x in r["results"]]
    assert "muslim/2937" in ids[:10] and not ids[0].startswith(("kenz/", "kesfulhafa/", "mecma/"))


def test_notes_remind_the_label_the_chain_and_unquoted_sources(lib):
    assert "Yapay zekâ tercümesi" in lib.report("muslim/2937")["note"]
    note = lib.cite_reports([{"id": "muslim/2937"}, {"id": "tirmidhi/2244", "quote": "بباب لد"}])["note"]
    assert "Sent without a quotation: muslim/2937." in note
