"""S12.3: sohbet servisi. Gerçek API çağrılmaz: sahte istemci akışı taklit eder; araçlar ve atıf denetimi gerçek genel
veritabanıyla (yoksa atlanır)."""

import asyncio
from types import SimpleNamespace as NS

import pytest

from risale_mcp import sohbet
from risale_mcp.profiles import GENEL

pytest.importorskip("starlette")
needs_db = pytest.mark.skipif(not GENEL.db.exists(), reason="genel veritabanı yok")

C32 = "sozler/10/on-iki-hakikat/hakikat-09/c032"
TEXT_32 = "Teşkilce, sûretçe birbirinden ayrı, hiç şaşırtmaz."


def test_instructions_are_the_chats_own():
    from risale_mcp import server
    text = sohbet.instructions("Risale MCP")
    assert text.startswith("You answer readers' questions on the Risale-i Nur chat page of Risale MCP")
    assert "[[sozler/10/on-iki-hakikat/hakikat-09/c032]]" in text and "never put a section id after a quotation" in text
    # MCP'ye özgü kısımlar yok
    for phrase in ("cite once", "cite returns", "call each server", "another connector", "Use the web",
                   "model_readings", "permission of their sources"):
        assert phrase not in text, phrase
    # kaynağa bağlılığın blokları ortak: iki talimatta da aynen, kopya değil
    for block in (server.FIND, server.READ, server.GROUNDED, server.NEVER_INVENT, server.TEXT_APART):
        assert block in text and block in server.INSTRUCTIONS
    # alıntı kuralı sohbetin kendisinin: satır içi kısa alıntı işaretiyle serbest (sayfa onu da denetler)
    assert sohbet.QUOTE_EXACTLY in text and server.QUOTE_EXACTLY not in text
    assert server.QUOTE_EXACTLY in server.INSTRUCTIONS
    assert server.risale_layers(connectors=False).split("\n")[0] == "Layers that are not the author's words:"
    assert "Dictionary (lookup_word)" in text and "Dictionary" not in sohbet.instructions("R", lugat=False)


def test_mcp_instructions_keep_their_blocks():
    """Bloklara bölünme MCP'nin metnini değiştirmedi (ayrıntılı denetim araç çıktısı kaydında)."""
    from risale_mcp import server
    assert server.INSTRUCTIONS.startswith(server.RISALE_INTRO + "\nWorkflow:\n1. Find:")
    assert server.INSTRUCTIONS.endswith(server.risale_layers())
    assert "another connector's text" in server.INSTRUCTIONS and "model_readings" in server.INSTRUCTIONS
    assert "{old_names}" not in server.INSTRUCTIONS


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

    def _quote_sentences(self, quote, node, limit):     # başka yerde de bulunmaz
        return []

    def refresh(self):                                   # kaynak adı yok
        return NS(execute=lambda *a: NS(fetchone=lambda: None))


def test_check_numbers_and_problems():
    text = '> "doğru söz" [[x/c001]]\n\nBir daha [[x/c001]], başka [[y/c002]].\n\n> "yanlis söz" [[z/c003]]'
    checked = sohbet.check(FakeChecker(), text)
    assert checked.markdown == '> "doğru söz" [1]\n\nBir daha [1], başka [2].\n\n> "yanlis söz" [3]'
    assert [s["n"] for s in checked.sources] == [1, 2, 3]
    assert [p["id"] for p in checked.problems] == ["z/c003"]
    assert checked.sources[2]["unverified"] and "unverified" not in checked.sources[0]
    assert checked.counts == {"fixed": 0, "unverified": 1, "dropped": 0, "leaks": 0, "paragraphs": 1, "unmarked": 0}
    assert checked.raw == text


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
    chat = sohbet.Chat(library, client, settings=sohbet.Settings(model_fix=True))     # yol (a), varsayılan kapalı
    events = run(chat, "Dokuzuncu Hakikat ne der?")
    kinds = [e for e, _ in events]
    assert kinds[-1] == "done" and "restart" in kinds and "clear" in kinds
    assert any(e == "status" and d.get("step") and d["text"].startswith("Sözler › Onuncu Söz") and d["text"].endswith(" okunuyor") for e, d in events)
    assert ("status", {"text": sohbet.CHECKING}) in events and ("status", {"text": sohbet.THINKING_FIRST}) in events
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
    chat = sohbet.Chat(library, FakeClient([reply(text_block(wrong)), reply(text_block(wrong))]),
                       settings=sohbet.Settings(model_fix=True))
    done = run(chat, "soru")[-1][1]
    assert done["problems"] == 1 and "problem" in done["sources"][0] and done["corrected"]


# ------------------------------------------------------------ S12.9: düzeltmeyi sunucu yapar

C31 = "sozler/10/on-iki-hakikat/hakikat-09/c031"
SINEK = "Bütün hayvanatı icâd etmek, bir sinek icâdı kadar kudretine kolay gelir bir Zât’tır."
SINEK_A, SINEK_B = "sozler/10/parca-04/c025", "sozler/25/sule-02/nur-02/nukte-06/sir-07/c041"


@pytest.fixture(scope="module")
def checker(library):
    from risale_mcp.citations import CitationChecker
    return CitationChecker(library)


@needs_db
def test_server_moves_quote_to_its_sentence(checker):
    checked = sohbet.check(checker, f'> "{TEXT_32}" [[{C31}]]')
    assert checked.problems and checked.counts["fixed"] == 1 and checked.counts["unverified"] == 0
    assert checked.sources[0]["id"] == C32 and "problem" not in checked.sources[0]
    assert checked.sources[0]["source_name"] == "e-Risale"
    assert checked.raw == f'> "{TEXT_32}" [[{C32}]]' and checked.markdown == f'> "{TEXT_32}" [1]'


@needs_db
def test_server_prefers_read_section(checker):
    other = "sozler/1/c001"
    assert sohbet.check(checker, f'> "{SINEK}" [[{other}]]').sources[0]["id"] == SINEK_A    # okunan yok: kitap sırası
    assert sohbet.check(checker, f'> "{SINEK}" [[{other}]]', {SINEK_B}).sources[0]["id"] == SINEK_B
    # işaretin bölümündeki yer okunmuş yerden sonra gelir
    assert sohbet.check(checker, f'> "{SINEK}" [[{SINEK_B[:-4]}c001]]').sources[0]["id"] == SINEK_B


@needs_db
def test_server_trims_and_drops_marks_without_quote(checker):
    section = C32.rsplit("/", 1)[0]
    checked = sohbet.check(checker, f"Uzun aralık [[{section}/c001..c020]]. Uydurma [[{section}/c999]] yer.")
    assert checked.sources[0]["id"] == f"{section}/c001..c008" and "problem" not in checked.sources[0]
    assert checked.counts["fixed"] == 1 and checked.counts["dropped"] == 1
    assert checked.markdown == "Uzun aralık [1]. Uydurma yer."
    assert "c999" not in checked.raw


@needs_db
def test_unverified_quote_gets_its_own_number(checker):
    text = f'> "{TEXT_32}" [[{C32}]]\n\n> "Bu söz eserlerde hiç geçmez, uydurmadır efendim." [[{C32}]]'
    checked = sohbet.check(checker, text)
    assert checked.markdown.endswith("[1]\n\n> \"Bu söz eserlerde hiç geçmez, uydurmadır efendim.\" [2]")
    assert [s["id"] for s in checked.sources] == [C32, C32]
    assert "problem" not in checked.sources[0] and checked.sources[1]["unverified"]
    assert checked.counts["unverified"] == 1 and checked.counts["fixed"] == 0


def test_read_ids_only_from_reading_tools():
    calls = [("read_section", {}, '{"id":"a/b/c001","x":[{"id":"a/b/c002/h1/c001"}]}', False),
             ("search", {}, '{"id":"z/c001"}', False), ("get_passage", {}, '{"id":"y/c001"}', True)]
    assert sohbet.read_ids(calls) == {"a/b/c001", "a/b/c002/h1/c001"}


def test_paragraph_counts():
    text = "## Başlık\n\nGiriş paragrafı.\n\n> alıntı [[a/c001]]\n\nYorum [[a/c001]] burada.\n\nSon söz.\n\n---"
    assert sohbet._paragraphs(text) == {"paragraphs": 3, "unmarked": 2}


@needs_db
def test_tool_error_reaches_model(library):
    client = FakeClient([reply(tool_block("t1", "get_passage", {"id": "yok/c001"}), stop="tool_use"),
                         reply(text_block("Bulamadım."))])
    done = run(sohbet.Chat(library, client), "soru")[-1]
    assert done[0] == "done" and done[1]["sources"] == []
    result = client.calls[1]["messages"][-1]["content"][0]
    assert result["is_error"] is True and "No sentence" in result["content"]


@needs_db
def test_earlier_reads_note(library):
    """S13.4 (c): önceki cevabın çağırdığı araçlar sonraki soruda sayfa notu olarak gider."""
    client = FakeClient([reply(tool_block("t1", "get_passage", {"id": "yok/c001", "context": 0}), stop="tool_use"),
                         reply(text_block("Bulamadım."))])
    done = run(sohbet.Chat(library, client), "soru")[-1][1]
    assert done["reads"] == ["get_passage(id=yok/c001, context=0) -> error"]
    chat = sohbet.Chat(library, FakeClient([]))
    sent = chat.messages([{"q": "bir", "a": "cevap", "r": done["reads"]}, {"q": "iki", "a": "cevap"},
                          {"q": "üç", "a": "cevap", "r": []}], "dört")
    last = sent[-1]["content"]
    assert last.startswith("[Page note") and last.endswith("]\n\ndört")
    assert "Answer 1: get_passage(id=yok/c001, context=0) -> error" in last
    assert "Answer 2: not recorded." in last and "Answer 3: no tools called." in last
    assert chat.messages([], "tek")[-1]["content"] == "tek"
    assert "Never call an earlier statement unchecked" in chat.system and "only from get_ayah" in chat.system
    # S13.7 (3): okuma çağrısının ardına okunan yerin başlığı; eski turlarda da (not kurulurken bulunur)
    sent = chat.messages([{"q": "bir", "a": "cevap", "r": [
        "get_passage(id=lemalar/2/nukte-05/mesele-02/c008..c013)", "read_section(section=sozler/10, max_words=1500)",
        "get_outline(section=sozler/23, depth=2)", "search(query=tevekkül, limit=40)"]}], "iki")
    last = sent[-1]["content"]
    assert ("get_passage(id=lemalar/2/nukte-05/mesele-02/c008..c013) = read: Lem'alar › İkinci Lem'a › Beşinci Nükte"
            in last)
    assert "read_section(section=sozler/10, max_words=1500) = read: Sözler › Onuncu Söz;" in last
    assert "get_outline(section=sozler/23, depth=2) = outline of: Sözler › " in last
    assert last.count(" = ") == 3
    assert "never say you have not read a place" in chat.system and "not even to say" in chat.system
    assert chat.system.index("6. Verses quoted in the works") > chat.system.index("5. Earlier answers")
    assert "Writing dates: say when or where" in chat.system


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
    font = web.get("/sohbet/static/naskh.woff2")     # S13.8: Arapçanın yazı tipi (kesre işareti U+06EA)
    assert font.status_code == 200 and font.headers["content-type"] == "font/woff2"
    assert web.get("/sohbet/static/../sohbet.py").status_code == 404
    # servis yeni açılmış, henüz soru yok: atıf dizini kurulmadan da kaynağın metni açılır (2026-11-25 hatası)
    assert web.get("/sohbet/api/metin", params={"id": C32}).status_code == 200
    assert web.get("/sohbet/api/metin", params={"id": "sozler/31"}).status_code == 200
    r = web.post("/sohbet/api/sor", json={"question": "Dokuzuncu Hakikat?", "history": []})
    assert "event: done" in r.text and '"[1]' not in r.text
    row = store._run("SELECT * FROM usage")[0]
    assert row["email"] == "a@b.co" and row["outcome"] == "done" and row["sources"] == 1
    assert row["fixed"] == 0 and row["unmarked"] == 0 and row["paragraphs"] == 0
    passage = web.get("/sohbet/api/metin", params={"id": C32}).json()
    assert any(s["target"] for s in passage["sentences"])
    assert web.get("/sohbet/api/metin", params={"id": "sozler/31"}).json()["section_ref"] == "Sözler › Otuzbirinci Söz"
    # S12.12: geri bildirim; soru ve cevap yalnız kutu işaretliyse
    assert web.post("/sohbet/api/geri-bildirim", json={"vote": 1, "note": "iyi", "question": "q", "answer": "a"}).json()["ok"]
    assert web.post("/sohbet/api/geri-bildirim", json={"vote": -1, "share": True, "question": "q", "answer": "a"}).json()["ok"]
    assert web.post("/sohbet/api/geri-bildirim", json={"vote": 5}).status_code == 400
    rows = store._run("SELECT vote, note, question, answer FROM feedback ORDER BY ts")
    assert [tuple(r) for r in rows] == [(1, "iyi", None, None), (-1, None, "q", "a")]
    # S13.4: oy tıklanınca gider, not ve onay kutusu aynı satırı günceller; kutu kalkınca soru ve cevap silinir
    fid = web.post("/sohbet/api/geri-bildirim", json={"vote": 1}).json()["id"]
    assert web.post("/sohbet/api/geri-bildirim", json={"id": fid, "vote": -1, "note": "eksik", "share": True,
                                                       "question": "q2", "answer": "a2"}).json()["id"] == fid
    assert tuple(store._run("SELECT vote, note, question FROM feedback WHERE rowid = ?", (fid,))[0]) == (-1, "eksik", "q2")
    web.post("/sohbet/api/geri-bildirim", json={"id": fid, "vote": -1, "note": "eksik", "share": False})
    assert tuple(store._run("SELECT question, answer FROM feedback WHERE rowid = ?", (fid,))[0]) == (None, None)
    assert store._run("SELECT COUNT(*) FROM feedback")[0][0] == 3
    assert web.post("/sohbet/api/geri-bildirim", json={"id": 9999, "vote": 1}).status_code == 404
    assert web.post("/sohbet/api/geri-bildirim", json={"id": "1", "vote": 1}).status_code == 400
    rows = store._run("SELECT vote FROM feedback ORDER BY ts")
    store.remove_user("a@b.co")
    assert store._run("SELECT email FROM usage")[0]["email"] is None
    assert [tuple(r) for r in store._run("SELECT email, vote, note, question, answer FROM feedback ORDER BY ts")] == [
        (None, 1, None, None, None), (None, -1, None, None, None), (None, -1, None, None, None)]


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


@needs_db
def test_section_marks_are_section_references(checker):
    subtitle = "Otuz üç Penceredir Bir cihette Otuzüçüncü Mektûb ve bir cihette Otuzüçüncü Söz"
    checked = sohbet.check(checker, f'Otuz Birinci Söz\'de [[sozler/31]]. Alt başlık: "{subtitle}" [[sozler/33]].')
    assert [(s["id"], s["cite_as"], s.get("section")) for s in checked.sources] == [
        ("sozler/31", "Sözler › Otuzbirinci Söz", True), ("sozler/33", "Sözler › Otuzüçüncü Söz", True)]
    assert checked.counts["dropped"] == 0 and checked.markdown.startswith("Otuz Birinci Söz'de [1].")
    # bölüm kimliğinin ardındaki gerçek alıntı bölümün içindeki cümlesine taşınır
    moved = sohbet.check(checker, f'> "{TEXT_32}" [[sozler/10]]')
    assert moved.sources[0]["id"] == C32 and moved.counts["fixed"] == 1
    opening = sohbet.section_opening(checker, "sozler/31")
    assert opening["section_ref"] == "Sözler › Otuzbirinci Söz" and not any(s["target"] for s in opening["sentences"])


# ------------------------------------------------------------ S12.4: kota ve bütçe

def _usage(store, email, cost, ts):
    store._run("INSERT INTO usage (ts, email, model, rounds, tools, input, output, cache_write, cache_read, cost, "
               "seconds, outcome) VALUES (?, ?, 'm', 1, 0, 0, 0, 0, 0, ?, 1, 'done')", (ts, email, cost))


def test_quota_and_budget(tmp_path, monkeypatch):
    from risale_mcp.sohbet_hesap import Store
    store = Store(tmp_path / "s.db")
    limits = sohbet.Limits(questions=3, daily=1.0, monthly=2.0, alert=0.5)
    now = 1_795_000_000.0                                   # 2026-11-17 civarı
    day, month = sohbet._starts(now)
    assert day <= now < day + 86400 and month <= day
    _usage(store, "a@b.co", 0.1, day - 10)                  # dün: sayılmaz
    for _ in range(2):
        _usage(store, "a@b.co", 0.1, now)
    assert sohbet.refusal(store, "a@b.co", limits, now) is None
    _usage(store, "a@b.co", 0.1, now)
    assert "soru hakkınız (3)" in sohbet.refusal(store, "a@b.co", limits, now)
    assert sohbet.refusal(store, "c@d.co", limits, now) is None
    # sınırsız hesap: soru sınırı yok, bütçe tavanı var
    import dataclasses
    free = dataclasses.replace(limits, unlimited=frozenset({"a@b.co"}))
    assert sohbet.refusal(store, "a@b.co", free, now) is None
    monkeypatch.setenv("SOHBET_SINIRSIZ", " A@B.co , x@y.co")
    assert sohbet.Limits.from_env().unlimited == {"a@b.co", "x@y.co"}
    _usage(store, "c@d.co", 0.7, now)                       # bugün 1,0 $
    assert "Bugünlük sohbet bütçesi" in sohbet.refusal(store, "a@b.co", free, now)
    assert "Bugünlük sohbet bütçesi" in sohbet.refusal(store, "c@d.co", limits, now)
    assert sohbet.spent(store, now) == pytest.approx((1.0, 1.1))
    # eşikler bir kez, aşıldığı soruda
    assert sohbet.alerts((0.4, 1.4), (0.6, 1.6), limits) == ["Günlük harcama 0.60 $ oldu (uyarı eşiği 0.5 $)",
                                                             "Aylık harcama 1.60 $ (tavanın %80'i: 1.6 $)"]
    assert sohbet.alerts((0.6, 0.6), (0.7, 0.7), limits) == []
    assert len(sohbet.alerts((0.9, 1.9), (1.1, 2.1), limits)) == 2


@needs_db
def test_quota_refuses_at_route(library, tmp_path):
    from starlette.testclient import TestClient
    from risale_mcp.sohbet_hesap import Config, LogMailer, Store
    store = Store(tmp_path / "s.db")
    code, _ = store.new_code("a@b.co", 10)
    store.redeem("a@b.co", code, "uzun-bir-parola")
    client = FakeClient([reply(text_block("Cevap."))])
    app = sohbet.build(sohbet.Chat(library, client, Config()), store, LogMailer(tmp_path / "e.log"), Config(),
                       sohbet.Limits(questions=1))
    web = TestClient(app, base_url="https://testserver")
    web.cookies.set("sohbet_oturum", store.open_session("a@b.co"))
    first = web.post("/sohbet/api/sor", json={"question": "soru", "history": []})
    assert '"remaining": 0' in first.text
    second = web.post("/sohbet/api/sor", json={"question": "soru", "history": []})
    assert second.status_code == 429 and "soru hakkınız (1)" in second.json()["error"]


def test_title_of():
    assert sohbet.title_of("  Haşrin   aklî\ndelilleri? ") == "Haşrin aklî delilleri?"
    long = "kelime " * 30
    title = sohbet.title_of(long)
    assert title.endswith("…") and len(title) <= sohbet.MAX_TITLE + 1 and not title[:-1].endswith(" ")


@needs_db
def test_conversations_stored(library, tmp_path):
    """S13.1: konuşma hesapta saklanır; geçmiş sunucudan okunur; başkasının konuşması görünmez; silme ve ayar."""
    from starlette.testclient import TestClient
    from risale_mcp.sohbet_hesap import Config, LogMailer, Store
    store = Store(tmp_path / "s.db")
    for email in ("a@b.co", "c@d.co"):
        code, _ = store.new_code(email, 10)
        store.redeem(email, code, "uzun-bir-parola")
    client = FakeClient([reply(text_block(f'> "{TEXT_32}" [[{C32}]]')), reply(text_block("İkinci cevap.")),
                         reply(text_block("Geçici cevap."))])
    app = sohbet.build(sohbet.Chat(library, client, Config()), store, LogMailer(tmp_path / "e.log"), Config())
    web = TestClient(app, base_url="https://testserver")
    web.cookies.set("sohbet_oturum", store.open_session("a@b.co"))
    status = web.get("/sohbet/api/durum").json()
    assert status == {"email": "a@b.co", "keep": True, "questions": 10, "remaining": 10}

    first = web.post("/sohbet/api/sor", json={"question": "Dokuzuncu Hakikat ne der?"})
    assert '"conversation": "' in first.text and '"n": 0' in first.text
    listed = web.get("/sohbet/api/konusmalar").json()["conversations"]
    assert len(listed) == 1 and listed[0]["title"] == "Dokuzuncu Hakikat ne der?"
    ident = listed[0]["id"]
    # ikinci soru: tarayıcının geçmişi yok sayılır, sunucu kendi kaydını gönderir
    web.post("/sohbet/api/sor", json={"question": "Devamı?", "conversation": ident, "history": [{"q": "x", "a": "y"}]})
    sent = client.calls[1]["messages"]
    assert [m["role"] for m in sent] == ["user", "assistant", "user"] and sent[0]["content"] == "Dokuzuncu Hakikat ne der?"
    assert sent[2]["content"].startswith("[Page note") and "Answer 1: no tools called." in sent[2]["content"]
    got = web.get("/sohbet/api/konusma", params={"id": ident}).json()
    assert [t["q"] for t in got["turns"]] == ["Dokuzuncu Hakikat ne der?", "Devamı?"]
    assert got["turns"][0]["sources"][0]["id"] == C32 and "a" not in got["turns"][0]
    # oy saklanan tura da yazılır
    web.post("/sohbet/api/geri-bildirim", json={"vote": 1, "conversation": ident, "n": 1})
    assert web.get("/sohbet/api/konusma", params={"id": ident}).json()["turns"][1]["feedback"] == 1
    assert web.post("/sohbet/api/konusma/ad", json={"id": ident, "title": "  Yeni   ad "}).json()["ok"]
    assert web.get("/sohbet/api/konusmalar").json()["conversations"][0]["title"] == "Yeni ad"
    assert web.get("/sohbet/api/durum").json()["remaining"] == 8

    # başkası göremez, değiştiremez, silemez, devam edemez
    other = TestClient(app, base_url="https://testserver")
    other.cookies.set("sohbet_oturum", store.open_session("c@d.co"))
    assert other.get("/sohbet/api/konusma", params={"id": ident}).status_code == 404
    assert other.get("/sohbet/api/konusmalar").json()["conversations"] == []
    assert other.post("/sohbet/api/konusma/ad", json={"id": ident, "title": "x"}).status_code == 400
    assert other.post("/sohbet/api/konusma/sil", json={"id": ident}).json()["deleted"] == 0
    assert other.post("/sohbet/api/sor", json={"question": "q", "conversation": ident}).status_code == 404

    # saklama kapalı: konuşma açılmaz, geçmiş tarayıcıdan gelir
    assert web.post("/sohbet/api/ayarlar", json={"keep": False}).json()["keep"] is False
    temp = web.post("/sohbet/api/sor", json={"question": "Geçici?", "history": [{"q": "önce", "a": "cevap"}]})
    assert '"conversation"' not in temp.text and client.calls[2]["messages"][0]["content"] == "önce"
    assert len(web.get("/sohbet/api/konusmalar").json()["conversations"]) == 1
    assert web.post("/sohbet/api/ayarlar", json={"keep": "evet"}).status_code == 400

    # silme: tek tek ve hepsi; hesap silinince konuşmalar da gider
    assert web.post("/sohbet/api/konusma/sil", json={"id": ident}).json()["deleted"] == 1
    assert store._run("SELECT COUNT(*) FROM turns")[0][0] == 0
    store._run("UPDATE users SET keep_history = 1 WHERE email = 'a@b.co'")
    client.replies += [reply(text_block("Bir.")), reply(text_block("İki."))]
    web.post("/sohbet/api/sor", json={"question": "Bir"})
    web.post("/sohbet/api/sor", json={"question": "İki"})
    assert web.post("/sohbet/api/konusma/sil", json={"all": True}).json()["deleted"] == 2
    client.replies.append(reply(text_block("Üç.")))
    web.post("/sohbet/api/sor", json={"question": "Üç"})
    assert store._run("SELECT COUNT(*) FROM turns")[0][0] == 1
    store.remove_user("a@b.co")
    assert store._run("SELECT COUNT(*) FROM conversations")[0][0] == 0
    assert store._run("SELECT COUNT(*) FROM turns")[0][0] == 0


def test_old_database_gets_keep_history(tmp_path):
    import sqlite3
    from risale_mcp.sohbet_hesap import Store
    path = tmp_path / "eski.db"
    with sqlite3.connect(path) as c:
        c.execute("CREATE TABLE users (email TEXT PRIMARY KEY, password TEXT NOT NULL, created REAL NOT NULL, "
                  "failures INTEGER NOT NULL DEFAULT 0, locked_until REAL NOT NULL DEFAULT 0, last_login REAL)")
        c.execute("INSERT INTO users (email, password, created) VALUES ('a@b.co', 'x', 0)")
    store = Store(path)
    assert sohbet.Conversations(store).keeps("a@b.co") is True


@needs_db
def test_source_text_arabic_refs(library):
    """S13.7 (1): metin panelinde âyet ve hadis satırı, hadisin notu ve nâşirin meali (Kaynaklar listesinde değil)."""
    chat = sohbet.Chat(library, FakeClient([]))
    base = "sualar/13/talebe-i-ulumun-hatta-uykusu-dahi"
    data = sohbet.source_text(chat, f"{base}/c004..c010")
    by_id = {s["id"]: s for s in data["sentences"]}
    hadis = by_id[f"{base}/c004"]["refs"]
    assert hadis == [{"line": "Hadis: el-Aclûnî, Keşfü'l-Hafâ: 1:55 (doğrulanmadı)",
                      "meal": "İşlerin en hayırlısı zorlu olanıdır."}]
    assert by_id[f"{base}/c010"]["refs"] == [{"line": "Âyet: Âl-i İmrân Sûresi, 3:173",
                                              "meal": "Bize Allah yeter. O ne güzel vekildir."}]
    assert "refs" not in by_id[f"{base}/c005"]


@needs_db
def test_inline_quote_is_checked_like_a_block(checker):
    """Sohbette cümleye örülmüş kısa alıntı serbest (2026-11-26): sayfa onu da denetler ve asıl yerine taşır."""
    checked = sohbet.check(checker, f'Müellif şöyle der: "{TEXT_32}" [[{C31}]] ve devam eder.')
    assert checked.counts["fixed"] == 1 and checked.sources[0]["id"] == C32
    assert checked.markdown == f'Müellif şöyle der: "{TEXT_32}" [1] ve devam eder.'
