"""Aşama 5: JSON -> SQLite kurulumu ve arama.

Testler `conftest.py`'deki küçük, elle yazılmış eserlerden kurulan veritabanını kullanır. Son test
gerçek veritabanını kullanır; yoksa atlanır.
"""

import sqlite3

import pytest

from risale_mcp import search
from risale_mcp.build_db import SuraNames, parse_ayah_source
from risale_mcp.catalog import WORKS
from risale_mcp.db import DatabaseError, connect
from risale_mcp.paths import DB_PATH
from risale_mcp.search import QueryError, to_fts

@pytest.fixture(scope="module")
def db(small_db):
    path, report = small_db
    conn = connect(path)
    yield conn, report
    conn.close()


def test_counts_and_catalog(db):
    conn, report = db
    assert report.works == 2 and report.counts["sentences"] == 6
    works = conn.execute("SELECT slug, built FROM works ORDER BY ord").fetchall()
    assert [w["slug"] for w in works] == [w.slug for w in WORKS]           # bütün katalog, katalog sırasıyla
    assert {w["slug"] for w in works if w["built"]} == {"sozler", "asa-yi-musa"}
    assert conn.execute("SELECT count(*) FROM notes").fetchone()[0] == 1


def test_outline_order_and_subtree(db):
    conn, _ = db
    rows = {r["id"]: r for r in conn.execute("SELECT id, ord, last_ord, depth FROM nodes WHERE work = 'sozler'")}
    assert (rows["sozler"]["ord"], rows["sozler"]["last_ord"]) == (0, 3)
    assert (rows["sozler/10"]["ord"], rows["sozler/10"]["last_ord"], rows["sozler/10"]["depth"]) == (1, 2, 1)
    assert rows["sozler/11"]["last_ord"] == 3


def test_mecmua_mapped_paragraph_has_source_not_text(db):
    conn, _ = db
    p = conn.execute("SELECT text FROM paragraphs WHERE id = 'asa-yi-musa/haşir/p001'").fetchone()
    assert p["text"] is None
    assert conn.execute("SELECT source_paragraph_id FROM paragraph_sources WHERE paragraph_id = ?",
                        ("asa-yi-musa/haşir/p001",)).fetchone()[0] == "sozler/10/p001"
    assert conn.execute("SELECT node_id FROM node_sources WHERE source_node_id = 'sozler/10'").fetchone()[0] \
        == "asa-yi-musa/haşir"


def test_hasiye_sentence_is_flagged(db):
    conn, _ = db
    flags = dict(conn.execute("SELECT id, hasiye FROM sentences WHERE node_id = 'sozler/10'").fetchall())
    assert flags == {"sozler/10/c001": 0, "sozler/10/c002": 0, "sozler/10/c001/h1/c001": 1}


def test_arabic_linked_to_sentence_and_ayah_resolved(db):
    conn, _ = db
    rows = conn.execute("SELECT sentence_id, kind, source, sura, ayah_start, ayah_end FROM arabic"
                        " ORDER BY paragraph_id, ord").fetchall()
    assert [tuple(r) for r in rows] == [
        ("sozler/10/c001", "ayet", "Bakara Sûresi, 2:255", 2, 255, 255),
        # Hayrat biçimi: sûre numarası, numaralı kaynakta öğrenilen addan gelir.
        ("sozler/11/c001", "ayet", "Sûre-i Bakara, 1’den", 2, 1, 1),
        ("sozler/11/c001", "arabi", None, None, None, None),                 # REF-YOK -> kaynak yok
    ]
    # Kaynağın numarası Kur'ân metniyle denetlenir: 2:255 tutuyor; "قل هو الله احد" 2:1 değil.
    checks = [r[0] for r in conn.execute("SELECT ayah_check FROM arabic ORDER BY paragraph_id, ord")]
    assert checks == ["exact", "differs", None]


def test_quran_layer(db):
    conn, report = db
    assert report.counts["quran_ayahs"] == 256
    assert conn.execute("SELECT name FROM quran_suras WHERE number = 112").fetchone()[0] == "İhlâs"
    assert conn.execute("SELECT count(*) FROM quran_translations").fetchone()[0] == 512
    # Veride hiç geçmeyen sûre de Türkçe adıyla bulunur.
    assert conn.execute("SELECT number FROM sura_names WHERE key = 'kadr'").fetchone()[0] == 97


@pytest.mark.parametrize("source,expected", [
    ("Bakara Sûresi, 2:255", (2, 255, 255)),
    ("Zilzal Sûresi, 99:7-8", (99, 7, 8)),
    ("Âyet: Sûre-i Âl-i İmrân, 18", (3, 18, 18)),
    ("Sûre-i Âl-i Imran, 173", (3, 173, 173)),
    ("Kalem Sûresi: 1", (68, 1, 1)),
    ("Mâide, Sûresi, 5:1", (5, 1, 1)),
    ("Sûre-i Kadr, 1", None),                                                # öğrenilmemiş yazılış
    ("hadis", None),
])
def test_parse_ayah_source(source, expected):
    suras = SuraNames()
    for known in ("Âl-i İmrân Sûresi, 3:7", "Kalem Sûresi, 68:4"):
        suras.learn(known)
    ref = parse_ayah_source(source, suras)
    assert (ref and (ref.sura, ref.start, ref.end)) == expected


def test_search_ignores_marks_and_dotless_i(db):
    conn, _ = db
    assert [h.sentence_id for h in search.search(conn, "hasr-i cismani")] == ["sozler/10/c002"]
    assert [h.sentence_id for h in search.search(conn, "isik")] == ["sozler/10/c001/h1/c001"]
    assert [h.sentence_id for h in search.search(conn, "KIYAMET")] == ["sozler/10/hakikat-01/c001"]
    assert {h.sentence_id for h in search.search(conn, "الله")} == {"sozler/10/c001", "sozler/11/c001"}  # harekesiz
    assert [h.sentence_id for h in search.search(conn, "احد")] == ["sozler/11/c001"]


def test_search_operators_and_filters(db):
    conn, _ = db
    ids = lambda q, **kw: {h.sentence_id for h in search.search(conn, q, **kw)}
    assert ids("hasr*") == {"sozler/10/c002", "asa-yi-musa/haşir/c001"}
    assert ids("hasr*", work="sozler") == {"sozler/10/c002"}
    assert ids("hasr*", group="mecmua") == {"asa-yi-musa/haşir/c001"}
    assert ids('"cismani olacak"') == {"sozler/10/c002"}
    assert ids('"olacak cismani"') == set()
    assert ids("hasr* -mecmua") == {"sozler/10/c002"}
    assert ids("isik OR mizan") == {"sozler/10/c001/h1/c001", "sozler/10/hakikat-01/c001"}
    assert ids("NEAR(kiyamet gunu, 2)") == {"sozler/10/hakikat-01/c001"}
    assert ids("NEAR(kiyamet gelecek, 1)") == set()
    assert search.count_by_work(conn, "hasr*") == {"sozler": 1, "asa-yi-musa": 1}


def test_search_nodes(db):
    conn, _ = db
    assert [h.node_id for h in search.search_nodes(conn, "hasre")] == ["sozler/10"]    # alt başlıkta
    assert [h.node_id for h in search.search_nodes(conn, "hakikat", work="sozler")] == ["sozler/10/hakikat-01"]


@pytest.mark.parametrize("query,expected", [
    ("Haşir", '("hasir")'),
    ("haşir kıyâmet", '("hasir" AND "kiyamet")'),
    ('"Risâle-i Nûr"', '("risale i nur")'),
    ("Risâle-i", '("risale i")'),
    ("haşr*", '("hasr"*)'),
    ("haşir OR mizan", '("hasir") OR ("mizan")'),
    ("haşir -kıyamet", '(("hasir")) NOT "kiyamet"'),
    ("haşir NOT kıyamet", '(("hasir")) NOT "kiyamet"'),
    ("NEAR(haşir mizan)", '(NEAR("hasir" "mizan", 10))'),
    ("NEAR(haşir mizan, 3)", '(NEAR("hasir" "mizan", 3))'),
    ('haşir "', '("hasir")'),                                                # yarım tırnak yok sayılır
])
def test_to_fts(query, expected):
    assert to_fts(query) == expected


@pytest.mark.parametrize("query", ["", "  ", "!!", "-haşir", "NEAR(haşir mizan", "NEAR(haşir, x)"])
def test_to_fts_rejects(query):
    with pytest.raises(QueryError):
        to_fts(query)


def test_connect_checks_schema(tmp_path):
    with pytest.raises(DatabaseError):
        connect(tmp_path / "yok.db")
    old = tmp_path / "old.db"
    sqlite3.connect(old).executescript("CREATE TABLE meta (key, value); INSERT INTO meta VALUES ('schema_version', '0');")
    with pytest.raises(DatabaseError):
        connect(old)


def test_real_database():
    if not DB_PATH.exists():
        pytest.skip("risale.db yok; önce `uv run python -m risale_mcp.build_db` çalıştırın")
    conn = connect()
    nodes = {h.node_id for h in search.search(conn, '"hasr-i cismani"', work="sozler", limit=50)}
    assert any(n.startswith("sozler/28") for n in nodes)                     # Yirmisekizinci Söz
    ayetel_kursi = conn.execute("SELECT count(*) FROM arabic WHERE sura = 2 AND ayah_start = 255").fetchone()[0]
    assert ayetel_kursi > 0
    # Mecmuada ana cilde eşlenen paragrafın cümlesi yoktur: aynı cümle iki kez aranmaz.
    assert conn.execute("SELECT count(*) FROM sentences s JOIN paragraphs p ON p.id = s.paragraph_id"
                        " WHERE p.text IS NULL").fetchone()[0] == 0
