"""S14.3: genel setin raporu (`genel_olc`)."""
import json

from risale_mcp import genel_olc


def _dump(path, calls, sources, libraries=("tefsir",)):
    lines = []
    for i, (name, args, result) in enumerate(calls):
        lines.append({"type": "assistant", "message": {"content": [{"type": "tool_use", "id": f"t{i}", "name": name, "input": args}]}})
        lines.append({"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": f"t{i}", "content": result}]}})
    lines.append({"type": "result", "result": "Cevap [1]\n\nKaynaklar\n[1] x", "total_cost_usd": 0.05, "duration_ms": 30000,
                  "sohbet": {"libraries": list(libraries), "sources": sources, "failure": None}})
    path.write_text("\n".join(json.dumps(x) for x in lines) + "\n")


def test_report(tmp_path):
    qs = tmp_path / "set.json"
    qs.write_text(json.dumps({"questions": [{"id": "G1", "category": "ayet", "question": "Kürsî?", "behaviour": "b",
        "places": {"core": [{"library": "kuran", "id": "2:255"}, {"library": "tefsir", "id": "ibnkesir/2/255"},
                            {"library": "risale", "id": "sozler/10"}]}}]}))
    _dump(tmp_path / "G1.jsonl",
          [("get_ayah", {"sura": 2, "ayah": 255}, "{}"),
           ("tefsir_read_section", {"section": "ibnkesir/2/255"}, '{"id": "ibnkesir/2/255/c003"}'),
           ("search", {"query": "x"}, '{"id": "sozler/10/c001"}')],
          [{"n": 1, "id": "tefsir:ibnkesir/2/255/c003..c004", "library": "tefsir"},
           {"n": 2, "id": "lemalar/26/c001", "unverified": True}])
    out = genel_olc.report(tmp_path, qs).read_text()
    assert "| G1 | ayet | risale 2, tefsir 1 | risale 1, tefsir 1 | 1 | 2/3 | 1/3 | tefsir → risale |" in out
    assert "✓ okundu ✓ kaynakçada — tefsir `ibnkesir/2/255`" in out
    assert "· okundu · kaynakçada — risale `sozler/10`" in out


def test_unprefixed_risale_read(tmp_path):
    qs = tmp_path / "set.json"
    qs.write_text(json.dumps({"questions": [{"id": "G2", "category": "x", "question": "?",
        "places": {"core": [{"library": "risale", "id": "sozler/10"}]}}]}))
    _dump(tmp_path / "G2.jsonl", [("read_section", {"section": "sozler/10/on-iki-hakikat"}, "{}")], [])
    assert "| 1/1 | 0/1 |" in genel_olc.report(tmp_path, qs).read_text()
