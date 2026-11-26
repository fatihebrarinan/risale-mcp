"""S13.14: metin içi göndermeler (pointers.py) ve bölüm notları (books/bolum_notlari.json)."""
import json
import sqlite3
from pathlib import Path

import pytest

from risale_mcp import pointers
from risale_mcp.profiles import GENEL

needs_db = pytest.mark.skipif(not GENEL.db.exists(), reason="genel veritabanı yok")
NODES = {"sozler/10", "sozler/10/hatime", "sozler/22", "sozler/29", "mektubat/20", "nokta", "isaratul-icaz",
         "sualar/9", "sualar/11", "lemeat", "muhakemat"}


def find(text, here="x"):
    found = pointers.find([{"id": "s1", "text": text}], here, NODES.__contains__, lambda i: i)
    return [t["id"] for p in found for t in p["to"]]


def test_numbered_named_and_suffixed_targets():
    assert find("Şu âyetin hakikatini Onuncu Söz’ün Hâtimesi’nde icmâlen ve Nokta Risalesi’nde ve Yirminci Mektûb’da "
                "izâhen beyân etmişiz.") == ["sozler/10/hatime", "mektubat/20", "nokta"]
    assert find("Şu mes'eleye dair bir mikdarını Arabî olarak İşârâtü'l‑İ'câz’da yazmıştım.") == ["isaratul-icaz"]
    assert find("Zâten Yirmi Dokuzuncu Söz’de bürhânlar zikredilmiştir.") == ["sozler/29"]
    # eski ad asıl yerine: Otuz İkinci Mektub = Lemeât
    assert find("Otuzikinci Mektûbları te'lif ile ve Dokuzuncu Şuâ’nın dokuz makamını tekmîl ile devam edecek, "
                "izâhla yazılacak.") == ["lemeat", "sualar/9"]


def test_no_pointer_without_verb_or_target_or_capital():
    assert find("Onuncu Söz ile Yirmidokuzuncu Söz’ü in'âm etti.") == []          # gönderme fiili yok
    assert find("Bu mes'ele tafsilen beyân edilmiştir.") == []                     # hedef yok
    assert find("Şecere‑i kâinâtın meyvesi olan insan izâh edilmiştir.") == []     # "meyvesi" ad değil
    assert find("Lem'alar’da beyân edilmiştir.") == []                              # cildin adı, bir Lem'a değil
    assert find("Onuncu Söz’de beyân edilmiş.", here="sozler/10/hatime") == []      # okunan bölümün üstü


@needs_db
def test_section_notes_have_evidence():
    data = json.loads((Path(pointers.__file__).parent / "books" / "bolum_notlari.json").read_text(encoding="utf-8"))
    conn = sqlite3.connect(GENEL.db)
    for note in data["notes"]:
        assert conn.execute("SELECT 1 FROM nodes WHERE id = ?", (note["id"],)).fetchone(), note["id"]
        assert note["evidence"] and note["note"] and note["kind"]
        for ident in note["evidence"]:
            assert conn.execute("SELECT 1 FROM sentences WHERE id = ?", (ident,)).fetchone(), ident


@needs_db
def test_library_gives_coverage_pointers_and_notes():
    from risale_mcp.library import Library
    library = Library(GENEL.db, GENEL.vectors)
    page = library.read_section("nokta/kisim-02/hasir", max_words=900)
    assert page["coverage"]["sentences"].startswith("1–") and page["coverage"]["note"]
    assert {"sentence": "nokta/kisim-02/hasir/c003", "to": [{"id": "isaratul-icaz", "ref": "İşaratü'l-İ'caz"}]} \
        in page["points_to"]
    assert library.read_section("sualar/9/mukaddime")["profile"]["notes"][0]["kind"] == "unwritten"
    whole = library.read_section("sozler/29/maksad-02/esas-02/medar-02", max_words=100000)
    assert "coverage" not in whole
    one = library.passage("sozler/29/maksad-02/esas-03/c010")
    assert one["of_section"]["sentences"] == 1 and one["of_section"]["of"] > 1
    assert "mektubat/20" in [t["id"] for p in one["points_to"] for t in p["to"]]
