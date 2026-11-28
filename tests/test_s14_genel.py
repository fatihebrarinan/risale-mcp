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
    assert next(t for t in tools if t["name"] == "risale_search")["description"].startswith("[Risale-i Nur Library]")
    assert "search_all first" in sohbet.instructions("X", general=True)
    assert "search_all" not in sohbet.instructions("X")


def test_risale_mode_is_todays_page():
    """"Risale-i Nur'dan" kipi: genel sayfa açıkken de bugünkü talimat, bugünkü araçlar, kütüphanesiz."""
    import asyncio
    general = sohbet.Chat(sohbet._library(), None, settings=sohbet.Settings(general=True))
    today = sohbet.Chat(sohbet._library(), None)
    assert kipler.get("risale").risale_only
    assert general.system_for((), (), False) == today.system_for((), ())
    assert asyncio.run(general.tools("risale", (), False)) == asyncio.run(today.tools("serbest", ()))
    assert sohbet.wrong_library_hint("get_hadith", {"id": "bukhari/1"}, ()) == ""      # kapalı kütüphane önerilmez


def test_prefixed_names():
    import asyncio
    chat = sohbet.Chat(sohbet._library(), None, settings=sohbet.Settings(general=True))
    names = [t["name"] for t in asyncio.run(chat.tools("serbest", ("tefsir",), True))[0]]
    assert "risale_get_passage" in names and "get_ayah" in names and "get_passage" not in names
    assert sohbet.internal_name("risale_get_passage") == "get_passage"
    assert sohbet.internal_name("tefsir_get_passage") == "tefsir_get_passage"
    assert sohbet.internal_name("get_ayah") == "get_ayah"
    text = chat.system_for(("tefsir",), (), True)
    assert "risale_get_passage" in text and "tefsir_get_passage" in text and "tefsir_risale_" not in text


def test_survey_is_risale_scope_in_general():
    today = {k["id"]: k for k in kipler.public()}
    general = {k["id"]: k for k in kipler.public(general=True)}
    assert today["tarama"]["title"] == "Konu taraması" and "risale_only" not in today["tarama"]
    assert general["tarama"]["title"] == "Risale-i Nur'da konu taraması" and general["tarama"]["risale_only"]
    assert general["risale"]["risale_only"] and "risale_only" not in general["serbest"]
    assert kipler.risale_only(kipler.get("tarama"), True) and not kipler.risale_only(kipler.get("tarama"), False)


def test_s14_8_general_instructions_do_not_push_the_risale():
    new = sohbet.instructions("X", general=True)
    assert "fullest Turkish voice" not in new and "never leave it out" not in new
    assert "no library has to be quoted" in new and "rests on one library" in new
    assert "answer it from the Risale first" in new             # soru Risale'yi soruyorsa
    general = kutuphaneler.instructions(("klasik",), general=True)
    assert "only what the question needs" not in general
    assert "only what the question needs" in kutuphaneler.instructions(("klasik",))     # Risale sayfası aynı


def test_s14_8_one_rule_for_both_translations():
    for text in (sohbet.instructions("X"), sohbet.instructions("X", general=True)):
        assert "never join the two names in one label" in text and "never inside a block quote" in text


def test_s14_8_search_all_order_and_equal_counts():
    import asyncio
    import json
    asked = {}

    class Server:
        async def call_tool(self, name, args):
            asked["risale"] = args["limit"]
            return SimpleNamespace(content=[SimpleNamespace(text='{"results":[{"id":"sozler/1/c001"}]}')], is_error=False)

    class Libraries:
        async def call(self, k, name, args):
            asked[k] = args["limit"]
            return '{"results":[{"id":"x/1"}]}', False
    fake = SimpleNamespace(server=Server(), libraries=Libraries())
    out = json.loads(asyncio.run(sohbet.Chat._search_all(fake, "kader", ("tefsir", "hadis", "klasik"))))
    assert list(out)[:4] == ["Tafsir Library", "Risale-i Nur Library", "Hadith Library", "Classical Islamic Library"]
    assert len(set(asked.values())) == 1
