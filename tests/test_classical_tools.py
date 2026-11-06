"""Araçlarda müfessirin eseri (T6): yalnız veritabanında müfessir eseri varsa görünür.

Gerçek profillerin veritabanlarıyla çalışır; yoksa atlanır. Genel profilin araç çıktısının değişmediğini ayrıca
`tool_snapshot` denetler (H0).
"""

import asyncio
import json

import pytest

from risale_mcp.library import Library
from risale_mcp.profiles import GENEL, KISISEL
from risale_mcp.server import CLASSICAL_INSTRUCTIONS, create_server


def _library(profile) -> Library:
    if not profile.db.exists():
        pytest.skip(f"{profile.name} veritabanı yok")
    return Library(profile.db)


def _tools(server) -> list[str]:
    from mcp import Client

    async def go():
        async with Client(server) as client:
            return [t.name for t in (await client.list_tools()).tools]
    return asyncio.run(go())


def test_public_server_shows_nothing_of_the_pilot():
    lib = _library(GENEL)
    assert not lib.has_classical()
    server = create_server(lib)
    assert CLASSICAL_INSTRUCTIONS.strip() not in server.instructions and "text_links" not in _tools(server)
    assert "classical_works" not in lib.find_ayah("2", 6)


@pytest.fixture(scope="module")
def local():
    lib = _library(KISISEL)
    if not lib.has_classical():
        pytest.skip("yerel veritabanında müfessir eseri yok")
    return lib


def test_local_server_adds_the_instructions_and_the_tool(local):
    server = create_server(local)
    assert server.instructions.endswith(CLASSICAL_INSTRUCTIONS) and "text_links" in _tools(server)


def test_find_ayah_lists_the_risale_first_then_the_classical_work(local):
    result = local.find_ayah("2", 6)
    assert list(result).index("results") < list(result).index("classical_works")
    works = {w["work"]: w for w in result["classical_works"]}                 # MVP: 13 müfessirin hepsi
    assert {"beyzavi", "kessaf", "razi", "taberi"} <= set(works)
    work = works["beyzavi"]
    assert work["author"] == "Nâsırüddîn el-Beyzâvî"
    assert [u["section"] for u in work["units"]] == ["beyzavi/2/6"] and work["units"][0]["method"] == "structure"
    ids = [q["id"] for q in work["quotations"]]
    assert len(ids) == len(set(ids)) == work["quotations_total"]               # cümle başına tek kayıt


def test_read_section_shows_the_printed_verse_and_the_unit(local):
    items = local.read_section("beyzavi/2/6", max_words=200)["items"]
    head, verse = items[0], items[1]
    assert head["verses"] == "Bakara Sûresi, 2:6" and head["printed"] == {"volume": 1, "page": 40}
    assert verse["kind"] == "ayah" and verse["text"].endswith("(6)") and verse["sentences"] == []
    assert verse["verses"] == "Bakara Sûresi, 2:6" and "get_ayah" in verse["note"]
    assert all("printed" in s for item in items[2:] for s in item.get("sentences", []))


def test_the_editors_introduction_is_marked_as_his(local):
    result = local.passage("beyzavi/mukaddime-tahkik/c003")
    assert result["author"] == "Nâsırüddîn el-Beyzâvî"                          # eserin yazarı
    assert result["layer"]["authority"] == "muhakkik" and "not the work's author's" in result["layer"]["note"]
    hit = local.search("الكوفيون", work="beyzavi")["results"][0]
    assert hit["author"] == "Nâsırüddîn el-Beyzâvî" and "layer" not in hit
    assert json.dumps(local.works("tefsir"), ensure_ascii=False).count("Nâsırüddîn el-Beyzâvî") == 1
