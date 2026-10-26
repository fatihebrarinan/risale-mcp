"""Aşama 8: arama değerlendirmesinin ölçüleri ve değerlendirme seti."""

import pytest

from risale_mcp.db import connect
from risale_mcp.paths import DB_PATH
from risale_mcp.search_eval import first_rank, load_queries, summarize, within


def test_hits_count_inside_the_expected_subtree():
    assert within("sozler/10/hakikat-01", ["sozler/10"]) and within("sozler/10", ["sozler/10"])
    assert not within("sozler/100", ["sozler/10"]) and not within("sozler/1", ["sozler/10"])
    assert first_rank(["lemalar/2", "sozler/10/hakikat-01", "sozler/10"], ["sozler/10"]) == 2
    assert first_rank(["lemalar/2"], ["sozler/10"]) is None


def test_summary_metrics():
    rows = [{"rank": 1, "any_rank": 1}, {"rank": 8, "any_rank": 3}, {"rank": None, "any_rank": 15}, {"rank": None, "any_rank": None}]
    summary = summarize(rows)
    assert (summary["hit@5"], summary["hit@10"], summary["any@10"]) == (0.25, 0.5, 0.5)
    assert summary["MRR"] == pytest.approx((1 + 1 / 8) / 4)


def test_query_set_is_well_formed():
    queries = load_queries()
    assert len({q.id for q in queries}) == len(queries) >= 40
    assert all(q.query and q.expected and q.evidence for q in queries)


def test_query_set_points_to_existing_sections():
    if not DB_PATH.exists():
        pytest.skip("risale.db yok")
    conn = connect(DB_PATH)
    known = {r[0] for r in conn.execute("SELECT id FROM nodes")}
    assert [s for q in load_queries() for s in q.expected + q.related if s not in known] == []
