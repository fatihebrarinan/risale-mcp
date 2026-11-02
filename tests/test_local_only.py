"""Yerel ve sunucu verisinin farkı (`HUSUSI-VERILER.md`)."""

import sqlite3

from risale_mcp import local_only
from risale_mcp.catalog import Site
from risale_mcp.paths import RAW_DIR

TABLES = """
CREATE TABLE works (slug TEXT, json_sha1 TEXT, built INTEGER);
CREATE TABLE nodes (id TEXT, work TEXT);
CREATE TABLE paragraphs (id TEXT, work TEXT);
CREATE TABLE sentences (id TEXT, work TEXT);
CREATE TABLE arabic (paragraph_id TEXT);
"""


def _db(works: dict[str, str], *paragraphs: tuple[str, str]) -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.executescript(TABLES)
    conn.executemany("INSERT INTO works VALUES (?, ?, 1)", works.items())
    conn.executemany("INSERT INTO paragraphs VALUES (?, ?)", paragraphs)
    conn.executemany("INSERT INTO sentences VALUES (?, ?)", paragraphs)
    conn.executemany("INSERT INTO arabic VALUES (?)", [(paragraphs[0][0],)] if paragraphs else [])
    return conn


def test_compare_finds_local_works_and_stale_text():
    full = _db({"sozler": "a", "esasat-i-nuriye": "b", "lemalar": "c"})
    public = _db({"sozler": "a", "lemalar": "eski"})
    assert local_only.compare(full, public) == (["esasat-i-nuriye"], ["lemalar"])


def test_count_of_a_work_and_difference():
    full = _db({"a": "1", "b": "2"}, ("p1", "a"), ("p2", "b"))
    public = _db({"a": "1"}, ("p1", "a"))
    assert local_only.count(full, "a") == local_only.Count(0, 1, 1, 1)
    assert local_only.count(full, "b") == local_only.Count(0, 1, 1, 0)
    assert local_only.count(full) - local_only.count(public) == local_only.Count(0, 1, 1, 0)


def test_every_raw_folder_has_a_role():
    assert {s.value for s in Site} <= set(local_only.RAW_ROLES)
    if RAW_DIR.exists():
        assert {p.name for p in RAW_DIR.iterdir()} == set(local_only.RAW_ROLES)
