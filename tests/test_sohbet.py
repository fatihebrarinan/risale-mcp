"""S12.3: sohbet servisi. Gerçek API çağrılmaz: sahte istemci akışı taklit eder; araçlar ve atıf denetimi gerçek genel
veritabanıyla (yoksa atlanır)."""

import asyncio
from types import SimpleNamespace as NS

import pytest

from risale_mcp import sohbet
from risale_mcp.profiles import GENEL
from risale_mcp.server import INSTRUCTIONS

pytest.importorskip("starlette")
needs_db = pytest.mark.skipif(not GENEL.db.exists(), reason="genel veritabanı yok")

C32 = "sozler/10/on-iki-hakikat/hakikat-09/c032"
TEXT_32 = "Teşkilce, sûretçe birbirinden ayrı, hiç şaşırtmaz."


def test_instructions_replace_cite():
    text = sohbet.instructions(INSTRUCTIONS, "Risale MCP")
    assert "call cite" not in text and "cite returns" not in text
    assert "[[sozler/10/on-iki-hakikat/hakikat-09/c032]]" in text
    assert "Use the web only" not in text
    assert text.startswith("You answer readers' questions on the Risale-i Nur chat page of Risale MCP")
    assert "5. Keep what the text says apart" in text and "\nAnswering:" in text


def test_instructions_stop_when_server_text_changes():
    with pytest.raises(RuntimeError):
        sohbet.instructions(INSTRUCTIONS.replace("3. Before writing the answer, call cite once", "3. X"), "R")


def test_marks_quotes():
    text = ('Giriş [[a/c001]] cümlesi.\n\n> "Birinci satır\n> ikinci satır" [[b/c002..c004]]\n\n'
            '> "Ayrı blok"\n[[c/c009]]\n\nSatır içi "sekiz harften uzun söz" [[d/c001]] ve "kısa" [[e/c001]].')
    got = [(i, q) for i, q, _ in sohbet.marks(text)]
    assert got == [("a/c001", None), ("b/c002..c004", "Birinci satır\nikinci satır"), ("c/c009", "Ayrı blok"),
                   ("d/c001", "sekiz harften uzun söz"), ("e/c001", None)]
    for ident, _, (start, end) in sohbet.marks(text):
        assert text[start:end].strip("[]").strip() == ident


def test_strip_own_sources():
    text = "Cevap [[a/c001]].\n\n**Kaynaklar**\n[1] Sözler › …"
    assert sohbet.strip_own_sources(text) == "Cevap [[a/c001]]."
    assert sohbet.strip_own_sources("Kaynaklar demek") == "Kaynaklar demek"


class FakeChecker:
    def sources(self, items):
        out = []
        for n, item in enumerate(items, 1):
            record = {"n": n, "id": item["id"], "cite_as": f"Yol {item['id']}"}
            if "yanlis" in item.get("quote", ""):
                record["problem"] = "The quoted words are not in these sentences."
            out.append(record)
        return {"sources": out}


def test_check_numbers_and_problems():
    text = '> "doğru söz" [[x/c001]]\n\nBir daha [[x/c001]], başka [[y/c002]].\n\n> "yanlis söz" [[z/c003]]'
    checked = sohbet.check(FakeChecker(), text)
    assert checked.markdown == '> "doğru söz" [1]\n\nBir daha [1], başka [2].\n\n> "yanlis söz" [3]'
    assert [s["n"] for s in checked.sources] == [1, 2, 3]
    assert [p["id"] for p in checked.problems] == ["z/c003"]


def test_cost():
    usage = NS(input_tokens=1000, output_tokens=500, cache_creation_input_tokens=8000, cache_read_input_tokens=20000)
    expected = (1000 * 0.10 + 8000 * 0.10 * 1.25 + 20000 * 0.10 * 0.10 + 500 * 0.50) / 1e6
    assert sohbet.cost("claude-haiku-5-5", usage) == pytest.approx(expected)


# ------------------------------------------------------------ sahte istemciyle döngü

def text_block(text):
    return NS(type="text", text=text)


def tool_block(ident, name, args):
    return NS(type="tool_use", id=ident, name=name, input=args)


class FakeStream:
    def __init__(self, message):
        self.message = message

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False

    def __aiter__(self):
        async def gen():
            for block in self.message.content:
                if block.type == "text":
                    yield NS(type="text", text=block.text)
        return gen()

    async def get_final_message(self):
        return self.message


class FakeClient:
    def __init__(self, replies):
        self.replies = list(replies)
        self.calls = []
        self.messages = self

    def stream(self, **params):
        self.calls.append({**params, "messages": list(params["messages"])})    # o anki hâli
        return FakeStream(self.replies.pop(0))


def reply(*blocks, stop="end_turn"):
    usage = NS(input_tokens=100, output_tokens=50, cache_creation_input_tokens=0, cache_read_input_tokens=0)
    return NS(content=list(blocks), stop_reason=stop, usage=usage)


def run(chat, question, history=()):
    async def go():
        return [event async for event in chat.ask(list(history), question)]
    return asyncio.run(go())


@pytest.fixture(scope="module")
def library():
    from risale_mcp.library import Library
    return Library(GENEL.db, GENEL.vectors)


@needs_db
def test_loop_with_tool_and_correction(library):
    client = FakeClient([
        reply(tool_block("t1", "get_passage", {"id": C32}), stop="tool_use"),
        reply(text_block(f'Metinde:\n\n> "Teşkilce, sûretçe birbirinden ayrı, hiç yanılmaz." [[{C32}]]')),
        reply(text_block(f'Metinde:\n\n> "{TEXT_32}" [[{C32}]]\n\nKaynaklar\n[1] uydurma')),
    ])
    chat = sohbet.Chat(library, client)
    events = run(chat, "Dokuzuncu Hakikat ne der?")
    kinds = [e for e, _ in events]
    assert kinds[-1] == "done" and "restart" in kinds and "clear" in kinds
    assert any(e == "status" and d["text"].startswith("Cümleler okunuyor: Sözler › Onuncu Söz") for e, d in events)
    done = events[-1][1]
    assert done["corrected"] is True and done["problems"] == 0
    assert done["markdown"] == f'Metinde:\n\n> "{TEXT_32}" [1]'
    assert done["sources"][0]["cite_as"].startswith("Sözler › Onuncu Söz")
    assert f"[[{C32}]]" in done["raw"] and "uydurma" not in done["raw"]
    # araç tanımları sunucudan, `cite` yok; talimat ve araçlar önbellekte
    params = client.calls[0]
    names = {t["name"] for t in params["tools"]}
    assert "cite" not in names and {"semantic_search", "read_section", "get_passage"} <= names
    assert params["system"][0]["cache_control"] == {"type": "ephemeral"}
    assert params["model"] == "claude-haiku-5-5"
    # aracın sonucu modele gitti; düzeltme isteği okuyucunun sözü değil
    tool_result = client.calls[1]["messages"][2]["content"][0]
    assert tool_result["tool_use_id"] == "t1" and TEXT_32 in tool_result["content"]
    assert client.calls[2]["messages"][-1]["content"].startswith("[Automatic check")


@needs_db
def test_problem_after_correction_is_flagged(library):
    wrong = f'> "hiç yanılmaz ve uydurma" [[{C32}]]'
    chat = sohbet.Chat(library, FakeClient([reply(text_block(wrong)), reply(text_block(wrong))]))
    done = run(chat, "soru")[-1][1]
    assert done["problems"] == 1 and "problem" in done["sources"][0]


@needs_db
def test_tool_error_reaches_model(library):
    client = FakeClient([reply(tool_block("t1", "get_passage", {"id": "yok/c001"}), stop="tool_use"),
                         reply(text_block("Bulamadım."))])
    done = run(sohbet.Chat(library, client), "soru")[-1]
    assert done[0] == "done" and done[1]["sources"] == []
    result = client.calls[1]["messages"][-1]["content"][0]
    assert result["is_error"] is True and "No sentence" in result["content"]


@needs_db
def test_limits(library):
    chat = sohbet.Chat(library, FakeClient([]))
    with pytest.raises(sohbet.Refusal):
        run(chat, "")
    with pytest.raises(sohbet.Refusal):
        run(chat, "soru", [{"q": "a", "a": "b"}] * sohbet.MAX_TURNS)
    calls = [reply(tool_block(f"t{i}", "list_works", {}), stop="tool_use") for i in range(sohbet.MAX_ROUNDS)]
    events = run(sohbet.Chat(library, FakeClient(calls)), "soru")
    assert events[-1][0] == "error"


@needs_db
def test_web_routes(library, tmp_path):
    from starlette.testclient import TestClient
    from risale_mcp.sohbet_hesap import Config, LogMailer, Store
    store = Store(tmp_path / "s.db")
    code, _ = store.new_code("a@b.co", 10)
    store.redeem("a@b.co", code, "uzun-bir-parola")
    config = Config()
    client = FakeClient([reply(text_block(f'> "{TEXT_32}" [[{C32}]]'))])
    app = sohbet.build(sohbet.Chat(library, client, config), store, LogMailer(tmp_path / "e.log"), config)
    web = TestClient(app, base_url="https://testserver")
    assert web.post("/sohbet/api/sor", json={"question": "x"}).status_code == 401
    web.cookies.set("sohbet_oturum", store.open_session("a@b.co"))
    page = web.get("/sohbet/")
    assert page.status_code == 200 and "soru-formu" in page.text and "script-src 'self'" in page.headers["content-security-policy"]
    assert web.get("/sohbet/static/sohbet.js").status_code == 200
    assert web.get("/sohbet/static/../sohbet.py").status_code == 404
    r = web.post("/sohbet/api/sor", json={"question": "Dokuzuncu Hakikat?", "history": []})
    assert "event: done" in r.text and '"[1]' not in r.text
    row = store._run("SELECT * FROM usage")[0]
    assert row["email"] == "a@b.co" and row["outcome"] == "done" and row["sources"] == 1
    passage = web.get("/sohbet/api/metin", params={"id": C32}).json()
    assert any(s["target"] for s in passage["sentences"])
    store.remove_user("a@b.co")
    assert store._run("SELECT email FROM usage")[0]["email"] is None


class FlakyClient(FakeClient):
    """İlk akış ortada kopar."""
    def __init__(self, replies):
        super().__init__(replies)
        self.failed = False

    def stream(self, **params):
        if not self.failed:
            import anthropic
            import httpx2
            self.failed = True
            self.calls.append(params)
            raise anthropic.APIConnectionError(request=httpx2.Request("POST", "https://api.anthropic.com"))
        return super().stream(**params)


@needs_db
def test_stream_retry_after_dropped_connection(library):
    pytest.importorskip("anthropic")
    client = FlakyClient([reply(text_block("Cevap."))])
    events = run(sohbet.Chat(library, client), "soru")
    assert events[-1][0] == "done" and ("status", {"text": "Bağlantı yenileniyor…"}) in events


def test_bare_ids_are_problems_and_dropped():
    text = ('Temsil başta verilir (sozler/1/c016). Nefse hitap eder (c033), çöl (c034–c036) diye.\n\n'
            '> "söz" [[sozler/1/c040]]')
    checked = sohbet.check(FakeChecker(), text)
    assert [p["id"] for p in checked.problems] == ["(sozler/1/c016)", "(c033)", "(c034–c036)"]
    assert checked.markdown == 'Temsil başta verilir. Nefse hitap eder, çöl diye.\n\n> "söz" [1]'
    assert sohbet.check(FakeChecker(), "Hiç kimlik yok, 2:255 ve c-vitamini.").problems == []
