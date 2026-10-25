"""Aşama 6: okuma işleri (`library.py`) ve MCP sunucusu (`server.py`).

Okuma işleri `conftest.py`'deki küçük veritabanıyla sınanır. Sunucu, SDK'nın süreç içi istemcisiyle
gerçek protokol üzerinden çağrılır. Son testler gerçek veritabanını kullanır; yoksa atlanır.
"""

import json
import os
import shutil

import pytest
from mcp import Client

from risale_mcp.library import Library, LibraryError
from risale_mcp.paths import DB_PATH
from risale_mcp.server import create_server

pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def library(small_db):
    lib = Library(small_db[0])
    yield lib
    lib.close()


# ---------------------------------------------------------------- okuma işleri

def test_works_lists_catalog_with_availability(library):
    works = {w["id"]: w for w in library.works()}
    assert works["sozler"]["sentences"] == 5 and works["sozler"]["sections"] == 4
    assert works["kizil-icaz"] == {"id": "kizil-icaz", "title": "Kızıl İcaz", "group": "eski-said", "language": "ar",
                                   "available": False, "status": "missing", "note": "Arapça mantık eseri."}
    assert [w["id"] for w in library.works("mecmua")][0] == "asa-yi-musa"
    with pytest.raises(LibraryError, match="Unknown group"):
        library.works("roman")


def test_outline_counts_and_depth(library):
    outline = library.outline("sozler", depth=1)
    assert outline["ref"] == "Sözler" and outline["sentences"] == 4            # hâşiye cümlesi sayılmaz
    onuncu = outline["children"][0]
    assert (onuncu["id"], onuncu["subtitle"], onuncu["sentences"], onuncu["subsections"]) == ("sozler/10", "Haşre dâir", 3, 1)
    assert "children" not in onuncu
    assert library.outline("sozler", depth=2)["children"][0]["children"][0]["id"] == "sozler/10/hakikat-01"
    with pytest.raises(LibraryError, match="get_outline"):
        library.outline("sozler/99")


def test_read_section_in_book_order_with_hasiye_and_ayah(library):
    section = library.read_section("sozler/10")
    kinds = [item.get("section") or item.get("kind") for item in section["items"]]
    assert kinds == ["sozler/10", "paragraph", "hasiye", "sozler/10/hakikat-01", "paragraph"]
    paragraph, hasiye = section["items"][1:3]
    assert [s["id"] for s in paragraph["sentences"]] == ["sozler/10/c001", "sozler/10/c002"]
    assert paragraph["arabic"][0]["source"] == "Bakara Sûresi, 2:255"
    assert hasiye["hasiye_of"] == "sozler/10/c001"
    assert section["next_cursor"] is None


def test_read_section_pages_continue_from_cursor(library):
    first = library.read_section("sozler/10", max_words=8)
    assert first["next_cursor"] == "sozler/10/p001/h1"
    rest = library.read_section("sozler/10", cursor=first["next_cursor"], max_words=8)
    assert rest["items"][0] == {"section": "sozler/10", "title": "Onuncu Söz", "ref": "Sözler › Onuncu Söz",
                                "subtitle": "Haşre dâir", "continued": True}
    assert rest["items"][1]["kind"] == "hasiye"
    with pytest.raises(LibraryError, match="Cursor"):
        library.read_section("sozler/11", cursor=first["next_cursor"])


def test_read_section_of_mecmua_brings_canonical_sentences(library):
    items = library.read_section("asa-yi-musa/haşir")["items"]
    mapped, own = items[1], items[2]
    assert mapped["canonical"] == {"paragraphs": ["sozler/10/p001"], "ref": "Sözler › Onuncu Söz"}
    assert [s["id"] for s in mapped["sentences"]] == ["sozler/10/c001", "sozler/10/c002"]   # atıf ana cilde
    assert own["sentences"][0]["id"] == "asa-yi-musa/haşir/c001"


def test_passage_with_context_range_and_hasiye(library):
    passage = library.passage("sozler/10/c001", context=1)
    first, second = passage["sentences"]
    assert first["target"] and not second["target"]
    assert first["hasiye"] == [{"id": "sozler/10/c001/h1/c001", "ref": "sozler/10/c001/h1/c001", "text": "Işık geldi."}]
    assert first["arabic"][0]["meal"].startswith("Allah")
    assert [s["id"] for s in library.passage("sozler/10/c001..c002")["sentences"]] == ["sozler/10/c001", "sozler/10/c002"]
    with pytest.raises(LibraryError, match="forward"):
        library.passage("sozler/10/c002..c001")
    with pytest.raises(LibraryError, match="No sentence"):
        library.passage("sozler/10/c099")


def test_find_sentence_by_opening_words(library):
    assert [m["id"] for m in library.find_sentence("elbette hasr-i cism")["matches"]] == ["sozler/10/c002"]
    assert library.find_sentence("Elbette haşr", scope="sozler/11")["matches"] == []
    with pytest.raises(LibraryError):
        library.find_sentence("…")


def test_find_ayah_by_number_or_name(library):
    by_name = library.find_ayah("Bakara", 255)
    assert (by_name["sura"], by_name["name"], by_name["total"]) == (2, "Bakara", 1)
    assert by_name["results"][0]["id"] == "sozler/10/c001"
    assert library.find_ayah("2")["total"] == 2                               # 2:255 ve "Sûre-i Bakara, 1"
    with pytest.raises(LibraryError, match="Unknown sura"):
        library.find_ayah("Yok")


def test_search_reports_totals_and_bad_queries(library):
    result = library.search("hasr*")
    assert result["total"] == 2 and result["by_work"] == {"sozler": 1, "asa-yi-musa": 1}
    assert result["matching_sections"] == [{"id": "sozler/10", "ref": "Sözler › Onuncu Söz"}]
    assert library.search("hasr*", work="sozler")["by_work"] == {"sozler": 1}
    with pytest.raises(LibraryError, match="aranacak"):
        library.search("-hasir")


def test_rebuilt_database_is_reopened(small_db, tmp_path):
    path = tmp_path / "copy.db"
    shutil.copy(small_db[0], path)
    lib = Library(path)
    old = lib.conn
    os.utime(path, ns=(0, 0))                                                 # build_db dosyayı değiştirdi
    assert lib.conn is not old
    lib.close()


# ---------------------------------------------------------------- MCP protokolü

async def test_server_lists_tools_prompts_and_resources(library):
    async with Client(create_server(library)) as client:
        tools = {t.name: t for t in (await client.list_tools()).tools}
        assert set(tools) == {"list_works", "get_outline", "read_section", "get_passage", "search",
                              "find_sentence", "find_ayah"}
        assert all(t.annotations.read_only_hint for t in tools.values())
        prompts = {p.name for p in (await client.list_prompts()).prompts}
        assert prompts == {"topic_survey", "text_and_commentary", "discuss", "self_test", "lesson_plan"}
        templates = {t.uri_template for t in (await client.list_resource_templates()).resource_templates}
        assert templates == {"risale://outline/{work}", "risale://text/{+section}"}


async def test_server_tool_returns_compact_json_and_readable_errors(library):
    async with Client(create_server(library)) as client:
        result = await client.call_tool("search", {"query": "hasr*", "work": "sozler"})
        assert not result.is_error
        assert json.loads(result.content[0].text)["by_work"] == {"sozler": 1}
        assert ", " not in result.content[0].text.split('"text"')[0]           # girintisiz JSON
        error = await client.call_tool("get_outline", {"section": "sozler/99"})
        assert error.is_error and "get_outline to see section ids" in error.content[0].text


async def test_server_resources_and_prompts(library):
    async with Client(create_server(library)) as client:
        text = (await client.read_resource("risale://text/sozler/10")).contents[0].text
        assert "## Sözler › Onuncu Söz" in text and "[2] Elbette haşr-i cismânî olacak." in text
        assert "> Hâşiye: [1] Işık geldi." in text
        outline = (await client.read_resource("risale://outline/sozler")).contents[0].text
        assert "- Birinci Hakikat `sozler/10/hakikat-01`" in outline
        prompt = await client.get_prompt("topic_survey", {"topic": "haşir"})
        assert "“haşir”" in prompt.messages[0].content.text


# ---------------------------------------------------------------- gerçek veritabanı

@pytest.fixture
def real_library():
    if not DB_PATH.exists():
        pytest.skip("risale.db yok; önce `uv run python -m risale_mcp.build_db` çalıştırın")
    lib = Library()
    yield lib
    lib.close()


def test_real_reading_of_dokuzuncu_hakikat(real_library):
    section = real_library.read_section("sozler/10/on-iki-hakikat/hakikat-09", max_words=400)
    assert section["ref"] == "Sözler › Onuncu Söz › On iki Hakikat › Dokuzuncu Hakikat"
    first = section["items"][1]["sentences"][0]
    assert first["id"] == "sozler/10/on-iki-hakikat/hakikat-09/c001" and first["text"].startswith("Hiç mümkün müdür ki;")
    assert section["next_cursor"]
    found = real_library.find_sentence("Hiç mümkün müdür ki; ölmüş", scope="sozler/10")["matches"]
    assert [m["id"] for m in found] == [first["id"]]


def test_real_ayat_al_kursi_and_mecmua(real_library):
    assert real_library.find_ayah("Bakara", 255)["total"] > 10
    items = real_library.read_section("tilsimlar/hasan-feyzinin-bir-kasidesi", max_words=300)["items"]
    canonical = [i for i in items if "canonical" in i]
    assert canonical and canonical[0]["canonical"]["paragraphs"][0].startswith("tarihce-i-hayat/")
