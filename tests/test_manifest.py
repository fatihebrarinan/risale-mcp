"""Kimlik manifestosu (H1): kayan, silinen ve değişen kimlik kurulumu durdurur; eklenen kabul edilir; sürüm."""

import shutil
import sqlite3

import pytest

from risale_mcp import manifest
from risale_mcp.library import Library
from risale_mcp.manifest import Changes, IdChangesError, Manifest, diff


def m(sentences, nodes=None):
    nodes = nodes or [(n, n.upper()) for n in dict.fromkeys(node for _, node, _ in sentences)]
    return Manifest(list(sentences), list(nodes))


BASE = [("w/1/c001", "w/1", "a"), ("w/1/c002", "w/1", "b"), ("w/1/c003", "w/1", "c"), ("w/2/c001", "w/2", "d")]


def test_additions_are_not_breaking():
    new = m(BASE + [("w/2/c002", "w/2", "e"), ("w/3/c001", "w/3", "f")])
    changes = diff(m(BASE), new)
    assert not changes.breaking
    assert changes.added_sentences == ["w/2/c002", "w/3/c001"] and changes.added_nodes == ["w/3"]


def test_inserted_sentence_is_reported_as_a_shift():
    # w/1'in başına yeni bir cümle girdi: eski c001..c003 bir kaydı
    new = m([("w/1/c001", "w/1", "x"), ("w/1/c002", "w/1", "a"), ("w/1/c003", "w/1", "b"),
             ("w/1/c004", "w/1", "c"), ("w/2/c001", "w/2", "d")])
    changes = diff(m(BASE), new)
    assert changes.breaking
    assert changes.changed_sentences == ["w/1/c001", "w/1/c002", "w/1/c003"]
    assert changes.shifts == {"w/1": "c001"}
    assert "kayma c001'den başlıyor" in changes.report("t")


def test_removed_node_and_renamed_node():
    old = m(BASE)
    new = Manifest([s for s in BASE if s[1] != "w/2"], [("w/1", "Yeni Ad")])
    changes = diff(old, new)
    assert changes.removed_nodes == ["w/2"] and changes.removed_sentences == ["w/2/c001"]
    assert changes.renamed_nodes == [("w/1", "W/1", "Yeni Ad")]
    assert not diff(old, Manifest(BASE, [("w/1", "Yeni Ad"), ("w/2", "W/2")])).breaking   # yalnız yol değişti


def test_hash_depends_on_ids_text_and_refs():
    assert m(BASE).corpus_hash == m(list(BASE)).corpus_hash
    assert m(BASE).corpus_hash != m(BASE[:-1] + [("w/2/c001", "w/2", "z")]).corpus_hash
    assert m(BASE).corpus_hash != Manifest(BASE, [("w/1", "W/1"), ("w/2", "başka")]).corpus_hash


def test_node_of_handles_hasiye_ids():
    assert manifest._node_of("sozler/10/c038/h1/c001") == "sozler/10"
    assert manifest._node_of("sozler/10/on-iki-hakikat/hakikat-09/c032") == "sozler/10/on-iki-hakikat/hakikat-09"


@pytest.fixture
def db_copy(small_db, tmp_path, monkeypatch):
    monkeypatch.setattr(manifest, "MANIFEST_DIR", tmp_path / "manifest")
    path = tmp_path / "risale.db"
    shutil.copy(small_db[0], path)
    return path


def test_check_build_accepts_first_then_blocks_changes(db_copy):
    conn = sqlite3.connect(db_copy)
    assert manifest.check_build(conn, "genel").empty                    # ilk manifesto kabul edilir
    first = sentence = conn.execute("SELECT id FROM sentences ORDER BY seq LIMIT 1").fetchone()[0]
    with conn:
        conn.execute("UPDATE sentences SET hash = 'deadbeef0000' WHERE id = ?", (sentence,))
    with pytest.raises(IdChangesError, match="1 cümlenin metni değişti"):
        manifest.check_build(conn, "genel")
    reports = list((manifest.MANIFEST_DIR / "genel" / "changes").glob("*.md"))
    assert reports and "REDDEDİLDİ" in reports[0].read_text()
    changes = manifest.check_build(conn, "genel", accept=True)       # kasıtlıysa kabul edilir
    assert changes.changed_sentences == [first]
    assert manifest.check_build(conn, "genel").empty                    # artık kabul edilmiş hâl budur


def test_release_labels_the_database_and_cite_shows_it(db_copy):
    conn = sqlite3.connect(db_copy)
    manifest.check_build(conn, "genel")
    conn.commit()
    corpus_hash = dict(conn.execute("SELECT key, value FROM meta"))["corpus_hash"]
    conn.close()
    library = Library(db_copy)
    assert library.corpus_version() == f"unreleased:{corpus_hash}"
    label = manifest.release(db_copy, "genel", "2026-11-04")
    assert label == "2026-11-04" and library.corpus_version() == "2026-11-04"
    assert manifest.release(db_copy, "genel", "başka") == "2026-11-04"           # aynı metin aynı sürüm
    assert manifest.releases("genel")[0]["corpus_hash"] == corpus_hash
    conn = sqlite3.connect(db_copy)                                            # yeniden kurulum sürümü bulur
    with conn:
        conn.execute("DELETE FROM meta WHERE key = 'corpus_version'")
        manifest.check_build(conn, "genel")
    assert library.corpus_version() == "2026-11-04"
