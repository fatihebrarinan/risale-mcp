"""S13.17: sohbetin öbür kütüphaneleri: seçim, araçlar, işaret denetimi, uzak MCP istemcisi."""

import asyncio
import dataclasses
import json
import socket
import threading
import time

import pytest

from risale_mcp import kutuphaneler as k
from risale_mcp import sohbet


class FakeChecker:
    """Risale tarafı (test_sohbet'teki gibi): her kimlik bulunur, "yanlis" geçen alıntı tutmaz."""

    nodes: dict = {}

    def sources(self, items):
        out = []
        for n, item in enumerate(items, 1):
            record = {"n": n, "id": item["id"], "cite_as": f"Yol {item['id']}"}
            if "yanlis" in item.get("quote", ""):
                record["problem"] = "The quoted words are not in these sentences."
            out.append(record)
        return {"sources": out}

    def _quote_sentences(self, quote, node, limit):
        return []

    def refresh(self):
        from types import SimpleNamespace as NS
        return NS(execute=lambda *a: NS(fetchone=lambda: None, fetchall=lambda: []))


def test_split_id_and_selection():
    assert k.split_id("tefsir:ibnkesir/2/255/c001") == ("tefsir", "ibnkesir/2/255/c001")
    assert k.split_id("hadis:bukhari/1") == ("hadis", "bukhari/1")
    assert k.split_id("risale:sozler/10/c001") == (None, "sozler/10/c001")
    assert k.split_id("sozler/10/c001") == (None, "sozler/10/c001")
    assert k.selected(["klasik", "yok", "tefsir", "tefsir"]) == ("tefsir", "klasik")      # sabit sıra
    assert k.selected("tefsir") == () and k.selected(None) == ()


class FakeClient:
    """Öbür kütüphanenin sunucusu: araç listesi, cite ve okuma."""

    def __init__(self, texts: dict[str, str], tools=("search", "find_ayah", "get_ayah", "cite", "get_passage")):
        self.texts, self.names, self.calls = texts, tools, []

    async def list_tools(self):
        return [{"name": n, "description": f"{n} açıklaması", "input_schema": {"type": "object"}} for n in self.names]

    async def call(self, name, args):
        self.calls.append((name, args))
        if name == "cite":
            out = []
            for i, item in enumerate(args["sources"], 1):
                if item["id"] not in self.texts:
                    out.append({"n": i, "id": item["id"], "status": "unknown_id", "problem": "No sentence"})
                elif item.get("quote") and item["quote"] not in self.texts[item["id"]]:
                    out.append({"n": i, "id": item["id"], "status": "problem", "cite_as": f"Eser › {item['id']}",
                                "problem": "The quoted words are not in these sentences.", "source_name": "OpenITI"})
                else:
                    out.append({"n": i, "id": item["id"], "status": "ok", "cite_as": f"Eser › {item['id']}",
                                "source_name": "OpenITI"})
            return json.dumps({"sources": out}), False
        if name == "get_outline":
            if args["section"] == "ibnkesir/2/255":
                return json.dumps({"id": args["section"], "ref": "Tefsîr › آية 255"}), False
            return "Unknown section", True
        if name == "search":
            return "x" * (k.MAX_RESULT + 10), False
        return "{}", False


def test_tools_are_prefixed_without_cite_and_get_ayah():
    libs = k.Kutuphaneler({"tefsir": FakeClient({})})
    tools = asyncio.run(libs.tools("tefsir"))
    assert [t["name"] for t in tools] == ["tefsir_search", "tefsir_find_ayah", "tefsir_get_passage"]
    assert tools[0]["description"].startswith("[Tafsir Library] ")
    assert libs.owner("tefsir_find_ayah", ("tefsir",)) == ("tefsir", "find_ayah")
    assert libs.owner("tefsir_find_ayah", ()) is None                 # seçilmemiş kütüphanenin aracı çalışmaz
    assert libs.owner("find_ayah", ("tefsir",)) is None and libs.owner("hadis_get_hadith", ("hadis",)) is None
    assert libs.available() == ("tefsir",) and [p["id"] for p in libs.public()] == ["tefsir"]


def test_long_results_are_cut():
    libs = k.Kutuphaneler({"tefsir": FakeClient({})})
    text, error = asyncio.run(libs.call("tefsir", "search", {"query": "x"}))
    assert not error and len(text) < k.MAX_RESULT + 200 and "Result cut" in text


def test_unreachable_library_is_an_error_the_model_reads():
    class Down(FakeClient):
        async def call(self, name, args):
            raise k.Unavailable("tefsir: ConnectError")
    text, error = asyncio.run(k.Kutuphaneler({"tefsir": Down({})}).call("tefsir", "search", {}))
    assert error and "cannot be reached" in text


def test_instructions_only_for_chosen():
    assert k.instructions(()) == ""
    text = k.instructions(("tefsir", "hadis"), ("klasik",))
    assert "Tafsir Library (tools tefsir_" in text and "Hadith Library (tools hadis_" in text
    assert "Classical Islamic Library (tools" not in text and "Not reachable now: Classical Islamic Library" in text
    assert "[[tefsir:ibnkesir/2/255/c001]]" in text and "Yapay zekâ tercümesi:" in text
    assert "Never give a legal ruling" in text                       # hassas alan (S13.14)


def test_status_lines():
    assert k.status_line("tefsir", "find_ayah", {"sura": "Bakara", "ayah": 255}) == \
        "Tefsirlerde Bakara 255 âyetinin birimleri aranıyor"
    assert k.status_line("hadis", "get_hadith", {"id": "bukhari/1"}) == "Hadis kitabında bukhari/1 okunuyor"
    assert k.status_line("klasik", "get_outline", {}) == "Klasik eserler kütüphanesine bakılıyor"


TEXTS = {"ibnkesir/2/255/c001": "هذه آية الكرسي ولها شأن عظيم", "bukhari/1": "إنما الأعمال بالنيات"}


def _check(text, clients):
    libs = k.Kutuphaneler(clients)
    loop = asyncio.new_event_loop()
    foreign = lambda lib, items: loop.run_until_complete(libs.verify(lib, items))    # noqa: E731
    try:
        return sohbet.check(FakeChecker(), text, foreign=foreign)
    finally:
        loop.close()


def test_foreign_marks_are_checked_and_numbered_with_risale():
    tefsir, hadis = FakeClient(TEXTS), FakeClient(TEXTS)
    text = ('Risale [[a/c001]].\n\n> "هذه آية الكرسي" [[tefsir:ibnkesir/2/255/c001]]\n\n'
            'Rivayet "إنما الأعمال بالنيات" [[hadis:bukhari/1]] ve yine [[tefsir:ibnkesir/2/255/c001]].\n\n'
            '> "لم يقله أحد" [[tefsir:ibnkesir/2/255/c001]]\n\nBölüm [[tefsir:ibnkesir/2/255]]. Yok [[tefsir:yok/c009]].'
            ' Kapalı [[klasik:tarifat/2/c001]].')
    checked = _check(text, {"tefsir": tefsir, "hadis": hadis})
    by_id = {}
    for s in checked.sources:
        by_id.setdefault(s["id"], []).append(s)
    assert [s["n"] for s in checked.sources] == [1, 2, 3, 4, 5]
    ok = by_id["tefsir:ibnkesir/2/255/c001"]
    assert ok[0]["library"] == "tefsir" and ok[0]["library_title"] == "Tefsir" and not ok[0].get("unverified")
    assert ok[0]["cite_as"] == "Eser › ibnkesir/2/255/c001" and ok[0]["source_name"] == "OpenITI"
    assert ok[1]["unverified"] and "not in these sentences" in ok[1]["problem"]       # tutmayan alıntı ayrı numara
    assert by_id["hadis:bukhari/1"][0]["library"] == "hadis"
    assert by_id["tefsir:ibnkesir/2/255"][0]["section"] and by_id["tefsir:ibnkesir/2/255"][0]["cite_as"] == "Tefsîr › آية 255"
    assert "tefsir:yok/c009" not in by_id and "klasik:tarifat/2/c001" not in by_id    # bilinmeyen ve açık olmayan
    assert checked.counts["unverified"] == 1 and checked.counts["dropped"] == 2
    assert "[[tefsir:ibnkesir/2/255/c001]]" in checked.raw and "[[tefsir:yok/c009]]" not in checked.raw
    assert "[2]" in checked.markdown and "[[" not in checked.markdown
    cites = [c for c in tefsir.calls if c[0] == "cite"]
    assert len(cites) == 1                                                        # kütüphane başına tek denetim
    assert {"id": "ibnkesir/2/255/c001", "quote": "هذه آية الكرسي"} in cites[0][1]["sources"]


def test_without_libraries_foreign_marks_are_dropped():
    checked = sohbet.check(FakeChecker(), 'Söz [[tefsir:ibnkesir/2/255/c001]] ve [[risale:a/c001]].')
    assert [s["id"] for s in checked.sources] == ["a/c001"] and checked.counts["dropped"] == 1


def test_hadith_text_for_the_panel():
    class Hadis(FakeClient):
        async def call(self, name, args):
            assert name == "get_hadith"
            return json.dumps({"id": args["id"], "isnad": "حدثنا", "matn": "إنما الأعمال", "cite_as": "Buhârî, no. 1"}), False
    text = asyncio.run(k.Kutuphaneler({"hadis": Hadis({})}).text("hadis", "bukhari/1"))
    assert text["section_ref"] == "Buhârî, no. 1"
    assert [(s["text"], s["target"]) for s in text["sentences"]] == [("حدثنا", False), ("إنما الأعمال", True)]


# ---------------------------------------------------------------- uzak istemci: gerçek bir HTTP sunucusuna

def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture
def remote_server(small_db, tmp_path):
    uvicorn = pytest.importorskip("uvicorn")
    from risale_mcp.auth import AuthStore
    from risale_mcp.library import Library
    from risale_mcp.server import create_server, http_app
    public = "https://tefsir.example"
    store = AuthStore(tmp_path / "auth.db", server="tefsir")
    key = store.new_internal_key("sohbet")
    server = create_server(Library(small_db[0]), public, store, open_access=True, profile="genel")
    port = _free_port()
    config = uvicorn.Config(http_app(server, public, open_store=store), host="127.0.0.1", port=port, log_level="error")
    running = uvicorn.Server(config)
    thread = threading.Thread(target=running.run, daemon=True)
    thread.start()
    for _ in range(100):
        if running.started:
            break
        time.sleep(0.05)
    yield f"http://127.0.0.1:{port}/mcp/{key}", store
    running.should_exit = True
    thread.join(5)


def test_remote_client_lists_and_calls_tools(remote_server):
    url, store = remote_server
    lib = dataclasses.replace(k.KUTUPHANELER["tefsir"], host="tefsir.example")
    remote = k.Remote(lib, url)

    async def go():
        tools = await remote.list_tools()
        text, error = await remote.call("search", {"query": "kiyamet"})
        remote.session = "eskimis-oturum"                       # oturum düşmüşse bir kez yeniden açılır
        again, _ = await remote.call("search", {"query": "kiyamet"})
        return tools, text, error, again
    tools, text, error, again = asyncio.run(go())
    assert "search" in [t["name"] for t in tools] and not error
    assert "sozler/10/hakikat-01" in text and "sozler/10/hakikat-01" in again
    logged = [r for r in store.usage() if r["name"] == "search"]
    assert logged and all(r["user"] == "(iç:sohbet)" and r["params"] is None for r in logged)


def test_remote_client_with_a_wrong_key_is_unavailable(remote_server):
    url, _ = remote_server
    lib = dataclasses.replace(k.KUTUPHANELER["tefsir"], host="tefsir.example")
    remote = k.Remote(lib, url.rsplit("/", 1)[0] + "/yanlis-anahtar")
    with pytest.raises(k.Unavailable):
        asyncio.run(remote.list_tools())


def test_mark_after_the_translation_goes_back_to_the_quotation():
    """Haiku işareti tercüme satırının altına yazıyordu: alıntı denetlenmiyordu (2026-11-26 denemesi)."""
    tefsir = FakeClient(TEXTS)
    text = ('> هذه آية الكرسي\n\nYapay zekâ tercümesi: "Bu, Kürsî âyetidir ve şanı büyüktür."\n\n'
            '[[tefsir:ibnkesir/2/255/c001]]\n\n> لم يقله أحد\n\nYapay zekâ tercümesi: "Kimse söylemedi." '
            '[[tefsir:ibnkesir/2/255/c001]]')
    checked = _check(text, {"tefsir": tefsir})
    sent = [c[1]["sources"] for c in tefsir.calls if c[0] == "cite"][0]
    assert {"id": "ibnkesir/2/255/c001", "quote": "هذه آية الكرسي"} in sent
    assert {"id": "ibnkesir/2/255/c001", "quote": "لم يقله أحد"} in sent
    assert "⚠" not in checked.markdown                     # tercüme işaretsiz alıntı sayılmaz
    assert checked.markdown.index("[1]") < checked.markdown.index("Yapay zekâ tercümesi")
    assert checked.counts["unverified"] == 1


def test_foreign_reads_count_as_read():
    calls = [("tefsir_read_section", {"section": "ibnkesir/2/255"},
              '{"section":"ibnkesir/2/255","items":[{"sentences":[{"id":"ibnkesir/2/255/c001"}]}]}', False),
             ("hadis_get_hadith", {"id": "bukhari/1"}, '{"id":"bukhari/1"}', False),
             ("tefsir_search", {"query": "x"}, '{"id":"kessaf/2/7/c001"}', False)]
    got = sohbet.foreign_read_ids(calls)
    assert {"tefsir:ibnkesir/2/255", "tefsir:ibnkesir/2/255/c001", "hadis:bukhari/1"} <= got
    assert "tefsir:kessaf/2/7/c001" not in got              # arama okuma değildir


def test_translation_inside_the_block_is_taken_out():
    """Haiku tercümeyi alıntı bloğuna koyuyordu: alıntı tutmuyor, tercüme "⚠ bulunamadı" alıyordu (tur 7)."""
    tefsir = FakeClient(TEXTS)
    text = ('> هذه آية الكرسي\n> Yapay zekâ tercümesi: "Bu, Kürsî âyetidir ve şanı büyüktür." '
            '[[tefsir:ibnkesir/2/255/c001]]')
    checked = _check(text, {"tefsir": tefsir})
    sent = [c[1]["sources"] for c in tefsir.calls if c[0] == "cite"][0]
    assert sent == [{"id": "ibnkesir/2/255/c001", "quote": "هذه آية الكرسي"}]
    assert "> Yapay" not in checked.markdown and "\nYapay zekâ tercümesi:" in checked.markdown
    assert "⚠" not in checked.markdown and not checked.counts["unverified"]


def test_quoted_rendering_next_to_foreign_marks_is_not_searched_in_the_risale(monkeypatch):
    monkeypatch.setattr(sohbet, "_place_unmarked", lambda checker, quote, read: "")     # Risale'de yok
    text = ('Taberî halifeyi "yeryüzünde birbirinin yerine geçen nesil" diye anlar. Şöyle der:\n\n'
            '> هذه آية الكرسي [[tefsir:ibnkesir/2/255/c001]]\n\n'
            'Risale ise "hiç kimsenin söylemediği bir söz burada" der. Bakınız [[a/c001]].')
    checked = _check(text, {"tefsir": FakeClient(TEXTS)})
    first, _, second = checked.markdown.split("\n\n")[:3]
    assert "⚠" not in first and "⚠" in second
    assert checked.counts["unmarked_foreign"] == 1 and checked.counts["unmarked_missing"] == 1


def test_translation_label_variants(monkeypatch):
    monkeypatch.setattr(sohbet, "_place_unmarked", lambda checker, quote, read: "")
    tefsir = FakeClient(TEXTS)
    text = ('> هذه آية الكرسي\n> Yapay zekâ tercümesi (AI translation): "This is the Throne Verse, it is great." '
            '[[tefsir:ibnkesir/2/255/c001]]\n\nRisale der ki (Yapay zekâ tercümesi: "bu satır modelin kendi '
            'tercümesidir") ve geçer.')
    checked = _check(text, {"tefsir": tefsir})
    assert "⚠" not in checked.markdown and "> Yapay" not in checked.markdown
    assert [c[1]["sources"] for c in tefsir.calls if c[0] == "cite"][0] == [
        {"id": "ibnkesir/2/255/c001", "quote": "هذه آية الكرسي"}]
