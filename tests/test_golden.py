"""Aşama 7: altın soru düzeneğinin döküm okuma ve atıf denetimi (Claude çağrılmaz)."""

import json

import pytest

from risale_mcp.golden import Checker, Transcript, ToolCall, evaluate, load_questions, read_transcript, sandbox
from risale_mcp.library import Library
from risale_mcp.paths import ROOT


@pytest.fixture
def checker(small_db):
    lib = Library(small_db[0])
    yield Checker(lib)
    lib.close()


def test_questions_file_is_well_formed():
    questions = load_questions()
    assert len({q["id"] for q in questions}) == len(questions) == 25
    assert all({"id", "category", "question", "expected", "sections"} <= set(q) for q in questions)


def test_read_transcript_collects_calls_answer_and_cost(tmp_path):
    events = [
        {"type": "system", "subtype": "init", "mcp_servers": [{"name": "risale", "status": "connected"}]},
        {"type": "assistant", "message": {"content": [
            {"type": "tool_use", "id": "t1", "name": "mcp__risale__search", "input": {"query": "haşir"}}]}},
        {"type": "user", "message": {"content": [
            {"type": "tool_result", "tool_use_id": "t1", "content": [{"type": "text", "text": "{\"total\":1}"}]}]}},
        {"type": "result", "subtype": "success", "is_error": False, "result": "Cevap.", "total_cost_usd": 0.12,
         "num_turns": 3, "duration_ms": 4200},
    ]
    path = tmp_path / "A1.jsonl"
    path.write_text("\n".join(json.dumps(e) for e in events), encoding="utf-8")
    t = read_transcript(path)
    assert (t.answer, t.turns, t.seconds, t.failure) == ("Cevap.", 3, 4.2, None)
    assert [(c.name, c.arguments, c.result) for c in t.calls] == [("search", {"query": "haşir"}, "{\"total\":1}")]


@pytest.mark.parametrize("line,status", [
    ("Bkz. Sözler › Onuncu Söz › “Elbette haşr-i cismânî…”", "ok"),
    ("**Onuncu Söz › Birinci Hakikat** › \"Kıyâmet ve mîzan\"", "ok"),          # eser adı yazılmadan
    ("Sözler › Onuncu Söz › 2. cümle", "ok"),
    ("Sözler › Onuncu Söz › 1. cümle › Hâşiye › 1. cümle", "ok"),
    ("Sözler › Onuncu Söz", "section"),
    ("Sözler › Onuncu Söz › On Beşinci Hakikat", "unresolved"),                  # uydurma bölüm
    ("Sözler › Onuncu Söz › “Böyle bir cümle yok…”", "unresolved"),
    ("Giriş: Sözler › Onuncu Söz › \"Elbette 'haşr-i' cismânî\" ve \"başka\"", "ok"),     # iki alıntı, iç tırnak
    ("Sözler › Onuncu Söz › 9. cümle", "unresolved"),
    ("**Sözler › Onuncu Söz** bölümünde yer alıyor; \"Kıyâmet\" der.", "section"),        # başlıktan sonra düz yazı
    ("(Sözler › Onuncu Söz › \"haşr-i cismânî olacak\")", "inside"),                    # cümle başı değil
])
def test_citations_are_checked_against_database(checker, line, status):
    (citation,) = checker.citations(f"Metin şöyle der.\n{line}\n")
    assert citation.status == status


def test_evaluate_reports_read_and_named_sections(checker):
    question = {"id": "A1", "sections": ["sozler/10", "sozler/11"]}
    transcript = Transcript(answer="Onuncu Söz’de anlatılır: Sözler › Onuncu Söz › “Elbette haşr-i…”",
                            calls=[ToolCall("read_section", {"section": "sozler/10/hakikat-01"}),
                                   ToolCall("get_outline", {"section": "sozler/11"})])
    result = evaluate(question, transcript, checker)
    assert result["sections"] == [{"id": "sozler/10", "read": True, "named": True},
                                  {"id": "sozler/11", "read": False, "named": False}]   # ağaca bakmak okumak değil
    assert result["unresolved"] == []


def test_sandbox_must_be_outside_project(tmp_path):
    sandbox(tmp_path / "deneme")
    settings = json.loads((tmp_path / "deneme" / ".claude" / "settings.json").read_text())
    assert "Read" in settings["permissions"]["deny"] and settings["permissions"]["allow"] == ["mcp__risale"]
    assert json.loads((tmp_path / "deneme" / ".mcp.json").read_text())["mcpServers"]["risale"]["args"][-1] == "risale-mcp"
    with pytest.raises(SystemExit):
        sandbox(ROOT / "deneme")
