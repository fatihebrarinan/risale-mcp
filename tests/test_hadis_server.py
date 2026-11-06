"""Hadis sunucusu (MVP M5): `hadis_db.py`'nin kurduğu veritabanı varsa gerçek veriyle; yoksa atlanır."""

import pytest

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
