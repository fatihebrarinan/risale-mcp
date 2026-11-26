"""S13.17 (3): âyet çalışmasının dosyası: Risale önce, tefsirler kelimeyle ölçülen paylarına göre, sayfanın eki."""

import asyncio

import pytest

from risale_mcp import ayet_dosyasi, kipler
from risale_mcp.profiles import GENEL, PROFILES

needs_dbs = pytest.mark.skipif(not (GENEL.db.exists() and PROFILES["tefsir"].db.exists()),
                               reason="genel ya da tefsir veritabanı yok")


def test_verse_count():
    assert ayet_dosyasi._verse_count("Bakara Sûresi, 2:255") == 1
    assert ayet_dosyasi._verse_count("Bakara Sûresi, 2:252-257") == 6
    assert ayet_dosyasi._verse_count("") == 1


def test_verse_mode_opens_tafsir_and_has_its_tool():
    kip = kipler.get("ayet")
    assert kip.libraries == ("tefsir",) and kip.tools == ("verse_file",) and kip.post == ("verse_places",)
    assert "verse_file" in kipler.LOCAL_TOOLS and "read_first" in kip.instructions
    assert "Hadis" not in kip.libraries


def test_verse_places_lists_only_what_was_not_read():
    page = {"tefsir": [{"work": "razi", "unit": "razi/2/255", "author": "Râzî", "title": "Mefâtîh", "words": 4920},
                       {"work": "taberi", "unit": "taberi/2/255", "author": "Taberî", "title": "Câmi'", "words": 3175}],
            "risale": [{"section": "lemalar/30/nukte-05", "ref": "Lem'alar › Otuzuncu Lem'a", "sentences": 3},
                       {"section": "sozler/25", "ref": "Sözler › Yirmibeşinci Söz", "sentences": 2}]}
    text = ayet_dosyasi.verse_places(page, [{"id": "tefsir:razi/2/255/c003"}], {"sozler/25/sule-01"})
    assert "Taberî" in text and "Râzî" not in text
    assert "Otuzuncu Lem'a" in text and "Yirmibeşinci" not in text
    assert ayet_dosyasi.verse_places(None, [], set()) == ""


@needs_dbs
def test_verse_file_ranks_by_words_per_verse():
    from risale_mcp.kutuphaneler import KUTUPHANELER, InProcess, Kutuphaneler
    from risale_mcp.library import Library
    library = Library(GENEL.db, GENEL.vectors)
    libs = Kutuphaneler({"tefsir": InProcess(KUTUPHANELER["tefsir"])})
    out = asyncio.run(ayet_dosyasi.verse_file(library, libs, "Bakara", 255, hadis_open=False))
    page = out.pop("_page")
    assert out["verse"]["ref"] == "Bakara Sûresi, 2:255" and "Diyanet Vakfı" in out["verse"]["translation_by"]
    assert out["risale"]["ties"][0]["strength"] == "strong"
    works = out["tefsir"]["works"]
    assert [w["work"] for w in works][:2] == ["taberi", "maturidi"]              # vefat sırasıyla
    shares = {w["unit"]: w["share"] for w in works if w.get("unit")}
    assert out["tefsir"]["read_first"] == sorted(shares, key=lambda u: -shares[u])[:4]
    nesefi = next(w for w in works if w["work"] == "nesefi")                     # 2:252-257: altı âyete bölünür
    assert nesefi["share"] == round(nesefi["words"] / 6)
    assert "closed" in out["hadis"] and page["tefsir"] and page["risale"]
