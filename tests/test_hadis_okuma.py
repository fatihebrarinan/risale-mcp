import json

from risale_mcp.hadis_okuma import pick, same, score, summary, window


def row(title, kind="hadis", speaker="prophet", verdict=None):
    return {"title": title, "book_kind": kind, "speaker": speaker, "verdict": verdict}


def test_pick_prefers_a_hadith_book_and_adds_another_book_when_queued():
    rows = [row("A", "mevzu"), row("B"), row("B"), row("C", speaker="none")]
    assert [r["title"] for r in pick(rows, False)] == ["B"]
    assert [r["title"] for r in pick(rows, True)] == ["B", "C"]


def test_window_keeps_context_around_the_match():
    filler = " ".join(f"كلمة{i}" for i in range(100))
    text = window("الضرورات تبيح المحظورات", f"{filler} الضرورات تبيح المحظورات {filler}")
    assert "الضرورات تبيح المحظورات" in text
    assert len(text.split()) == 73


def test_score_joins_readers_and_counts_decoys(tmp_path):
    (tmp_path / "key.json").write_text(json.dumps([
        {"id": "x0", "set": "found", "decoy": False, "part": "a", "title": "t", "report": "r", "queues": []},
        {"id": "x1", "set": "found", "decoy": True, "part": "b", "title": "t", "report": "r", "queues": []},
        {"id": "x2", "set": "found", "decoy": False, "part": "c", "title": "t", "report": "r", "queues": []}]))
    answer = lambda i, rel: {"id": i, "relation": rel, "speaker": "unclear", "denied": False, "confidence": "high", "note": ""}
    (tmp_path / "A-0-answers.json").write_text(json.dumps([answer("x0", "verbatim"), answer("x1", "different")]))
    (tmp_path / "B-0-answers.json").write_text(json.dumps([answer("x0", "abridged"), answer("x1", "different")]))
    result = score(tmp_path)
    assert result["missing"] == 1
    first = next(r for r in result["rows"] if r["id"] == "x0")
    assert first["agree_same"] and not first["agree"]
    assert same(first["answers"][0])
    assert any("| decoy | 1 | 0 | 1 | 0 |" in line for line in summary(result))
