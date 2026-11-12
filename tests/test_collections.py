"""Katalog, koleksiyonlar ve profiller: külliyat dışı metin müellife mal edilmez, asıl metnin önüne geçmez."""

import shutil
import sqlite3

import pytest

from risale_mcp.catalog import WORKS, Authority, Collection, Group, get_work
from risale_mcp.catalog.ilgili import ILGILI_WORKS, ilgili
from risale_mcp.library import Library
from risale_mcp.paths import KULLIYAT_DIR, LIBRARY_DIR
from risale_mcp.profiles import GENEL, KISISEL


def test_collection_gives_the_folder():
    assert get_work("sozler").book_path == KULLIYAT_DIR / "sozler.json"
    work = ilgili("sorular", "Sorular", Group.ANA_CILT, None, Authority.MODERN)
    assert work.book_path == LIBRARY_DIR / "risale" / "ilgili" / "sorular.json"


def test_related_works_are_never_the_authors_and_stay_private_by_default():
    assert all(w.authority is not Authority.MUELLIF for w in ILGILI_WORKS)
    work = ilgili("hatira", "Hatıra", Group.ANA_CILT, None, Authority.NAKIL)
    assert work.private and work.collection is Collection.ILGILI


def test_works_not_by_the_author_are_marked():
    assert get_work("esasat-i-nuriye").authority is Authority.DERLEME
    assert get_work("tesbihat").authority is Authority.BASKASI
    assert get_work("sozler").authority is Authority.MUELLIF


def test_translations_are_marked_and_keep_their_author():
    marked = {w.slug for w in WORKS if w.translation}
    assert marked == {"isaratul-icaz", "mesnevi-i-nuriye", "talikat", "teshisul-illet-zeyli", "hutbe-i-samiye",
                      "hutbe-i-samiye-arabi"}
    assert all(get_work(slug).authority is Authority.MUELLIF for slug in marked)


def test_profiles_choose_works():
    private, public = get_work("esasat-i-nuriye"), get_work("sozler")
    assert KISISEL.includes(private) and KISISEL.includes(public)
    assert GENEL.includes(public) and not GENEL.includes(private)
    assert KISISEL.db != GENEL.db and KISISEL.vectors != GENEL.vectors


@pytest.fixture
def related_db(small_db, tmp_path):
    """Örnek veritabanının kopyası: Asâ-yı Mûsâ külliyat dışı, günümüz yazarının metni sayılır."""
    path = tmp_path / "related.db"
    shutil.copy(small_db[0], path)
    conn = sqlite3.connect(path)
    with conn:
        conn.execute("UPDATE works SET collection = ?, authority = ? WHERE slug = 'asa-yi-musa'",
                     (Collection.ILGILI, Authority.MODERN))
        conn.execute("UPDATE works SET translation = 1 WHERE slug = 'sozler'")
    conn.close()
    library = Library(path)
    yield library
    library.close()


def test_search_stays_in_the_kulliyat_by_default(related_db):
    result = related_db.search("mecmua")
    assert result["total"] == 0 and not result["results"] and "matching_sections" not in result


def test_related_sources_come_only_when_asked_and_are_marked(related_db):
    for result in (related_db.search("mecmua", include_related=True), related_db.search("mecmua", work="asa-yi-musa"),
                   related_db.search("mecmua", group="mecmua")):
        assert result["total"] == 1
        assert result["results"][0]["authority"] == Authority.MODERN


def test_tools_say_whose_text_it_is(related_db):
    assert related_db.read_section("asa-yi-musa/haşir")["authority"] == Authority.MODERN
    own = related_db.read_section("sozler/10")
    assert own["translation"] is True and "authority" not in own
    assert "translation" not in related_db.read_section("asa-yi-musa/haşir")
    assert related_db.search("hasr*")["results"][0]["translation"] is True
    record = next(w for w in related_db.works() if w["id"] == "asa-yi-musa")
    assert record["authority"] == Authority.MODERN and record["collection"] == Collection.ILGILI
