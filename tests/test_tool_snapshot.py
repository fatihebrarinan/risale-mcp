"""Araç çıktısı karşılaştırması (H0): çağrı seti geçerli, fark yolu doğru, beklenen farklar ayrılıyor."""

import asyncio
import json

from risale_mcp import tool_snapshot
from risale_mcp.library import Library
from risale_mcp.server import create_server


def test_call_set_names_are_unique_and_tools_exist():
    calls = tool_snapshot.load_calls()
    assert len(calls) >= 90

    async def names():
        from mcp import Client
        server = create_server(Library(":memory:"))
        async with Client(server) as client:
            tools = {t.name for t in (await client.list_tools()).tools}
            prompts = {p.name for p in (await client.list_prompts()).prompts}
        return tools, prompts

    tools, prompts = asyncio.run(names())
    for call in calls:
        kind = call.get("kind", "tool")
        if kind == "tool":
            assert call["tool"] in tools, call["name"]
        elif kind == "prompt":
            assert call["prompt"] in prompts, call["name"]
        else:
            assert kind == "resource" and call["uri"].startswith("risale://"), call["name"]
    assert tools - {"sign_in"} <= {c["tool"] for c in calls if c.get("kind", "tool") == "tool"}, "her araç sette olmalı"


def test_json_diff_gives_field_paths():
    old = {"results": [{"id": "a", "ref": "X"}], "total": 3}
    new = {"results": [{"id": "a", "ref": "Y"}, {"id": "b"}], "total": 3, "version": "1"}
    diff = tool_snapshot.json_diff(old, new)
    assert "results[0].ref: X → Y" in diff
    assert "results: 1 öğe → 2 öğe" in diff
    assert any(line.startswith("version: eklendi") for line in diff)
    assert tool_snapshot.json_diff(old, json.loads(json.dumps(old))) == []


def test_compare_separates_expected_tools(tmp_path, monkeypatch):
    monkeypatch.setattr(tool_snapshot, "SNAPSHOT_DIR", tmp_path)
    calls = tmp_path / "calls.json"
    calls.write_text(json.dumps({"calls": [{"name": "c", "tool": "cite"}, {"name": "s", "tool": "search"},
                                           {"name": "m", "tool": "semantic_search", "semantic": True}]}))
    monkeypatch.setattr(tool_snapshot, "CALLS_PATH", calls)
    monkeypatch.setattr(tool_snapshot, "load_calls", lambda path=calls: json.loads(calls.read_text())["calls"])

    def write(name, cite, search, semantic):
        (tmp_path / name).mkdir()
        (tmp_path / name / "calls.json").write_text(json.dumps({
            "instructions": "i", "tools": {}, "resources": [], "prompts": {},
            "calls": {"c": {"error": False, "text": json.dumps(cite)}, "s": {"error": False, "text": json.dumps(search)},
                      "m": semantic}}))

    write("a", {"cite_as": "X"}, {"total": 1}, {"skipped": True})
    write("b", {"cite_as": "X", "version": "2026.1"}, {"total": 1}, {"error": False, "text": "{}"})
    assert tool_snapshot.compare("a", "b", ("cite",)) == 0           # yalnız beklenen fark; atlanan çağrı sayılmaz
    assert tool_snapshot.compare("a", "b") == 1
    write("c", {"cite_as": "X"}, {"total": 2}, {"skipped": True})
    assert tool_snapshot.compare("a", "c", ("cite",)) == 1
    assert "total: 1 → 2" in (tmp_path / "c" / "diff-a.md").read_text()
