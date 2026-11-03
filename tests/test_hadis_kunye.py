"""Künye ayrıştırma: kitap, bölüm, cilt, sayfa, numara ve ham metin. Örnekler eserlerin künyelerindendir."""

import pytest

from risale_mcp.hadis_kitaplar import BY_ID, normalize_name, section
from risale_mcp.hadis_kunye import parse


def books(raw):
    return [c.book for c in parse(raw).citations]


def test_chapters_continue_across_semicolons_within_a_collection():
    parts = parse("Buharî, Rikak: 1; Cihad: 33, 110; Müslim, Cihad: 126, 129; Müsned, 2:381; 3:172, 180; 5:332.").citations
    assert [c.book for c in parts] == ["bukhari", "muslim", "musned-ahmed"]
    assert [(l.chapter, l.section, l.number) for l in parts[0].locators] == [("rikak", 81, "1"), ("cihad", 56, "33,110")]
    assert parts[1].locators[0].section == 32
    assert [(l.volume, l.page) for l in parts[2].locators] == [(2, "381"), (3, "172"), (3, "180"), (5, "332")]


@pytest.mark.parametrize("raw, book", [
    ("el-Heysemî, Mecmeu'z-Zevâid, 9:203", "mecmauz-zevaid"), ("Mecmau’z-Zevaid 9:203", "mecmauz-zevaid"),
    ("Kadı Iyâz, eş-Şifâ, 1:328", "sifa"), ("Hafâcî, Şerhu’ş-Şifâ, 3:134", "serhus-sifa-hafaci"),
    ("Ali el-Kari, Şerhu'ş-Şifâ, 1:747", "serhus-sifa-kari"), ("el-Hâkim, el-Müstedrek, 3:499", "mustedrek"),
    ("Ebû Nuaym, Hilyetü'l-Evliyâ, 1:93", "hilye"), ("Ebû Nuaym, Delâilü'n-Nübüvve, 3:206", "delail-ebu-nuaym"),
    ("Beyhakî, Delâilü'n-Nübüvve: 2:255", "delail-beyhaki"), ("el-Hakîm et-Tirmizî, Nevâdiru'l-Usûl 1:149", "nevadir"),
    ("Ebû Hanîfe, el-Müsned 1:151", "musned-ebu-hanife"), ("Keşf-ül Hafa, 1:127", "keşfu"), ("Ed-Deylemî, 3:12", "musned-firdevs"),
    ("Müsnedü'l-Firdevs, 4:198", "musned-firdevs"), ("et-Taberânî, el-Mu'cemü'l-Evsat: 7:84", "mucemul-evsat"),
    ("İbn-i Hibbân, Sahih, no. 12215", "sahih-ibn-hibban"), ("Ebû Hanîfe, el-Müsned 1:151", "musned-ebu-hanife"),
])
def test_author_and_title_spellings(raw, book):
    assert books(raw) == [book]


def test_ranges_and_numbers_keep_their_kind():
    c = parse("Süyûtî, el-Hasâisü'l-Kübrâ, 1:252-271").citations[0]
    assert (c.book, c.locators[0].page) == ("hasais", "252-271")
    assert parse("Kenzü'l-Ummal, 3:326/6180").citations[0].locators[0].number == "6180"
    c = parse("Tirmizî, Menâkıb: 27, no. 3751").citations[0]
    assert [l.kind for l in c.locators] == ["chapter", "no"] and c.locators[1].section == 49
    assert parse("Müslim, c.4 s.2199").citations[0].locators[0].page == "2199"
    assert parse("el-Münâvî, Künûzü'l-Hakâik, s. 78.").citations[0].locators[0].kind == "page"
    assert parse("Tirmizî, 58. Sûrenin tefsiri: 1").citations[0].locators[0].section == 47


def test_qualifiers_come_from_the_text():
    assert parse("Hadis-i bilma’na. Sahih-i İbn-i Hibban, 1:2").citations[0].qualifier == "by_meaning"
    assert parse("İktibâsen: Müslim, Zikir: 79").citations[0].qualifier == "iktibas"
    first, second = parse("Müsned, 1:2. Ayrıca bk.: Tirmizî, Fiten: 48").citations
    assert first.qualifier is None and second.qualifier == "see"


def test_prose_around_a_citation_is_not_lost_or_taken_for_a_book():
    p = parse("Bu hadis-i şerifin Buharî, Rikak: 1")
    assert p.citations[0].book == "bukhari" and p.leftover
    assert "buyuran" not in parse("(Müslim, Zikir: 79.) buyuran zâta salât").citations[0].locators[0].chapter


def test_an_unknown_book_keeps_its_raw_text():
    c = parse("Mektûbat sh: 137").citations[0]
    assert c.book is None and c.raw == "Mektûbat sh: 137"


def test_book_ids_are_unique_and_collections_have_sections():
    assert len(BY_ID) == len({b.id for b in BY_ID.values()})
    assert section("bukhari", "Fedâilü's-Sahâbe") == 62 and section("muslim", "Salâtü'l-Müsâfirîn") == 6
    assert section("bukhari", "el-Amel Fi's-Salât") == 21 and section("tirmidhi", "yok") is None
    assert normalize_name("Keşfü’l-Hafâ") == "kesfulhafa"


def test_raw_ends_where_the_citation_ends():
    """Kaynakçaya giden ham künye: meal ayracının kapanışı, sondaki "bk." ve açıklama künyeye girmez."""
    assert [c.raw for c in parse("Müsned, 4:405, 409.) buyuran zâta ve âl ve ashabına salât ve selâm et").citations] \
        == ["Müsned, 4:405, 409"]
    assert parse("el-Aclûnî, Keşfü’l-Hafâ, 1:132, Hadis No: 381) 2: (").citations[0].raw \
        == "el-Aclûnî, Keşfü’l-Hafâ, 1:132, Hadis No: 381"
    assert parse("el-Münâvî, Feyzü'l-Kadîr, 6:108, hadis no: 8605; Aynı manada diğer rivayetler için bk.").citations[0].raw \
        == "el-Münâvî, Feyzü'l-Kadîr, 6:108, hadis no: 8605"
    assert parse("İbnu Abdilber, et-Temhîd: c. 8 s. 61. Ayrıca bk.:").citations[0].raw == "İbnu Abdilber, et-Temhîd: c. 8 s. 61"


def test_raw_keeps_names_after_semicolons_and_initials():
    """Kayıtta olmayan yazar ve kitap da nâşirin künyesidir; tek harfli kısaltma cümle sonu değildir."""
    assert parse("El-Münâvî, Feyzu'l-Kadîr 2:410; Mer'î b. Yûsuf; Ekâvîlü's-Sikât s. 45").citations[0].raw \
        == "El-Münâvî, Feyzu'l-Kadîr 2:410; Mer'î b. Yûsuf; Ekâvîlü's-Sikât s. 45"
    assert parse("Müsned (thk. Arnaut), 4:12; Buharî, Îman: 1").citations[0].raw == "Müsned (thk. Arnaut), 4:12"
    assert parse("Feyzü'l-Kadîr, 3:262-263. İmam-ı Ali'ye (r.a.) ait olduğu rivayet edilmektedir.").citations[0].raw.count("(") == 0
