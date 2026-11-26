"""S13.12: risale adları dizini ve bölüm künyesi (genel veritabanıyla)."""

import pytest

from risale_mcp.library import RISALE_NAMES
from risale_mcp.profiles import GENEL

pytestmark = pytest.mark.skipif(not GENEL.db.exists(), reason="genel veritabanı yok")


@pytest.fixture(scope="module")
def library():
    from risale_mcp.library import Library
    return Library(GENEL.db, GENEL.vectors)


def test_every_name_points_to_existing_places_with_evidence(library):
    for entry in RISALE_NAMES:
        assert entry["ids"] and entry["evidence"], entry["name"]
        for ident in entry["ids"]:
            library._node(ident)
        for ev in entry["evidence"]:
            if "/c" in ev.rsplit("/", 1)[-1] or ev.rsplit("/", 1)[-1].startswith("c"):
                library._sentence(ev)
            else:
                library._node(ev)


def test_named_in_search(library):
    named = library.search("İhlâs Risalesi")["named_sections"]
    assert named[0]["name"] == "İhlâs Risalesi"
    assert [s["id"] for s in named[0]["sections"]] == ["lemalar/20", "lemalar/21"]
    assert "named_sections" not in library.search("ihlâs")            # tek kelime ad değildir
    assert library.search("ihtiyarlar lem'ası")["named_sections"][0]["sections"][0]["id"] == "lemalar/26"


def test_profile_counts_hasiye_and_signatures(library):
    profile = library.outline("isaratul-icaz", 0)["profile"]
    assert profile["hasiye"] >= 15                                        # "tek hâşiye" değil
    letter = library.read_section("kastamonu-lahikasi/1-105-mektuplar/31", max_words=50)["profile"]
    assert any("Ahmed Nazîf" in s["signed"] for s in letter["signatures"])
    assert "profile" not in library.read_section("kastamonu-lahikasi/1-105-mektuplar/31", max_words=50,
                                                 cursor="kastamonu-lahikasi/1-105-mektuplar/31/p002")
