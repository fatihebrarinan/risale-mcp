"""Eski adlar sözlüğü (`books/old_names.json`): gerçek veritabanında her kayıt kanıtıyla tutmalı."""

import pytest

from risale_mcp.library import OLD_NAMES, Library, old_names_note
from risale_mcp.paths import DB_PATH


@pytest.fixture(scope="module")
def lib():
    if not DB_PATH.exists():
        pytest.skip("risale.db yok")
    library = Library(DB_PATH)
    yield library
    library.close()


@pytest.mark.parametrize("section", OLD_NAMES)
def test_entry_is_backed_by_the_data(lib, section):
    entry = OLD_NAMES[section]
    lib._node(section)
    for target in entry["elsewhere"]:
        assert lib.outline(target, depth=0)["sentences"] > 0, target
    evidence = entry["evidence"]
    sentence = lib.conn.execute("SELECT 1 FROM sentences WHERE id = ?", (evidence,)).fetchone()
    assert sentence or lib._node(evidence)["subtitle"]


def test_tools_point_to_the_real_text(lib):
    for result in (lib.read_section("mektubat/31"), lib.outline("mektubat/31")):
        assert result["text_elsewhere"]["elsewhere"] == ["lemalar"]
    assert "text_elsewhere" not in lib.read_section("sozler/1")


def test_note_lists_every_name():
    note = old_names_note()
    assert all(e["name"] in note for e in OLD_NAMES.values())
