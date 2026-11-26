"""S13.14: yanlış okuma setinin kanıtları veritabanında var; puanlama ve okuma denetimi."""
import sqlite3

import pytest

from risale_mcp import okuma_olc
from risale_mcp.profiles import GENEL

needs_db = pytest.mark.skipif(not GENEL.db.exists(), reason="genel veritabanı yok")


def test_set_shape():
    items = okuma_olc.load_set()
    assert len({i["id"] for i in items}) == len(items) >= 10
    for item in items:
        assert item["questions"] and item["facts"] and item["wrong"] and item["source"]
        assert all(f["evidence"] for f in item["facts"])


@needs_db
def test_evidence_and_must_read_exist():
    conn = sqlite3.connect(GENEL.db)
    for item in okuma_olc.load_set():
        for f in item["facts"]:
            for e in f["evidence"]:
                assert conn.execute("SELECT 1 FROM sentences WHERE id = ?", (e,)).fetchone(), (item["id"], e)
        for m in item["must_read"]:
            assert conn.execute("SELECT 1 FROM nodes WHERE id = ?", (m,)).fetchone(), (item["id"], m)


def test_scoring_and_reads():
    item = {"facts": [{"id": "f1"}, {"id": "f2"}], "wrong": [{"id": "w1"}], "must_read": ["sozler/29/maksad-02"]}
    calls = [{"tool": "read_section", "input": {"section": "sozler/29/maksad-02/esas-02"}},
             {"tool": "search", "input": {"query": "x"}}]
    hits = okuma_olc.must_read_hits(item, okuma_olc.read_places(calls))
    assert hits == {"sozler/29/maksad-02": True}
    verdicts = {"facts": [{"id": "f1", "verdict": "partly"}, {"id": "f2", "verdict": "contradicted"}],
                "wrong": [{"id": "w1", "verdict": "present"}]}
    assert okuma_olc.score(item, verdicts, hits) == {"facts": 0.5, "facts_total": 2, "wrong": 2, "must_read": 1,
                                                     "must_read_total": 1}
    text = "Cevap.\n\n**Konunun geçtiği öbür yerler** (…)\n\n- A\n\n:::ek X\n- B\n:::"
    assert okuma_olc.model_answer(text) == "Cevap."
