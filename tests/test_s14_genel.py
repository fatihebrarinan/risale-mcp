"""S14.4: genel sayfanın talimatı, "Risale-i Nur'dan" kipi ve iki düzeltme (öneksiz yabancı kimlik, başlık gibi söz)."""
import sqlite3
from types import SimpleNamespace

from risale_mcp import kipler, kutuphaneler, sohbet


def test_legacy_instructions_untouched_and_general_differs():
    old, new = sohbet.instructions("X"), sohbet.instructions("X", general=True)
    assert "Risale-i Nur chat page" in old and "only from the Risale-i Nur" in old
    assert "Qur'an and the Sunna come first" in new and "Risale-i Nur chat page" not in new
    assert "There is no fiqh library" in new and "only from the Risale-i Nur." not in new
    assert old.split("Rules:")[1] == new.split("Rules:")[1]          # kaynağa bağlılık kuralları aynı


def test_risale_mode_hidden_unless_general():
    assert "risale" not in [k["id"] for k in kipler.public()]
    assert "risale" in [k["id"] for k in kipler.public(general=True)]
    assert kipler.get("risale").risale_only


def test_library_block_general():
    old = kutuphaneler.instructions(("klasik",))
    new = kutuphaneler.instructions(("klasik",), general=True)
    assert "Keep the Risale-i Nur first" in old and "Keep each library apart" in new
    assert "refers its reader to and relies" in old and "classical works of the Islamic sciences" in new
    assert kutuphaneler.instructions((), general=True).startswith("Only the Risale-i Nur and the Qur'an are open")
    assert kutuphaneler.instructions(()) == ""


def test_title_like():
    assert sohbet._title_like("Kitâbu Esrâri's-Salât ve Mühimmâtihâ")
    assert not sohbet._title_like("Namaz kalplerin anahtarıdır; onda sırlar açılır")
    assert not sohbet._title_like("Bu dünya bir misafirhanedir.")


def test_prefix_foreign():
    conn = sqlite3.connect(":memory:")
    conn.executescript("CREATE TABLE sentences (id TEXT); CREATE TABLE nodes (id TEXT);"
                       "INSERT INTO sentences VALUES ('sozler/10/c001');")
    checker = SimpleNamespace(library=SimpleNamespace(conn=conn))
    read = {"klasik:ihya/4/3/4/c041", "klasik:ihya/4/3/4", "hadis:bukhari/1"}
    assert sohbet._prefix_foreign(checker, "ihya/4/3/4/c041", read) == "klasik:ihya/4/3/4/c041"
    assert sohbet._prefix_foreign(checker, "ihya/4/3/4/c040..c041", read) == "klasik:ihya/4/3/4/c040..c041"
    assert sohbet._prefix_foreign(checker, "sozler/10/c001", read) == "sozler/10/c001"        # Risale'de var
    assert sohbet._prefix_foreign(checker, "yok/1", read) == "yok/1"                          # hiçbir yerde okunmadı


def test_wrong_library_hint():
    assert "hadis_get_hadith with id='bukhari/1'" in sohbet.wrong_library_hint("get_hadith", {"id": "bukhari/1"})
    assert "klasik_get_passage" in sohbet.wrong_library_hint("get_passage", {"id": "serhul-mevakif/5/2/6/c210"})
    assert "hadis_get_hadith with id='malik/342'" in sohbet.wrong_library_hint("get_passage", {"id": "malik/342"})
    assert sohbet.wrong_library_hint("get_passage", {"id": "sozler/10/c001"}) == ""


def test_search_all_only_in_general():
    import asyncio
    chat = sohbet.Chat(sohbet._library(), None)
    names = lambda general: [t["name"] for t in asyncio.run(chat.tools("serbest", (), general))[0]]
    assert "search_all" in names(True) and "search_all" not in names(False)
    tools = asyncio.run(chat.tools("serbest", (), True))[0]
    assert next(t for t in tools if t["name"] == "search")["description"].startswith("[Risale-i Nur Library]")
    assert "search_all first" in sohbet.instructions("X", general=True)
    assert "search_all" not in sohbet.instructions("X")
