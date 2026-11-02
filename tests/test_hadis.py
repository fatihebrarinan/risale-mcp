"""Hadis katmanı: eşleme, dayanak ve araçlar. Küçük derlem elle kurulur; ağa çıkılmaz."""

import json

import pytest

from risale_mcp import hadis
from risale_mcp.build_db import build
from risale_mcp.arabic_kinds import HADITH_BOOKS, _mukattaat
from risale_mcp.hadis import Corpus, Report, support
from risale_mcp.library import Library, LibraryError
from risale_mcp.quran import skeleton


def report(id_, title, text, source="sanadset", grades=()):
    return Report(id_, title, "1", text, source, grades)


@pytest.fixture
def corpus():
    return Corpus([report("bukhari:1", "Sahîh-i Buhârî", "حدثنا مالك قال إنما الأعمال بالنيات وإنما لكل امرئ ما نوى", "hadith_api"),
                   report("sanadset:5", "مسند أحمد بن حنبل", "اطلبوا العلم ولو بالصين فإن طلب العلم فريضة"),
                   report("sanadset:9", "تذكرة الموضوعات للفتني", "إنما الأعمال بالنيات")])


def test_full_match_lists_every_report(corpus):
    match, found = corpus.match(skeleton("إِنَّمَا الْأَعْمَالُ بِالنِّيَّاتِ"))
    assert match == "found" and found == [0, 2]


def test_short_parts_are_not_searched(corpus):
    assert corpus.match(skeleton("العلم")) == ("short", [])


def test_partial_needs_most_of_it_in_one_report(corpus):
    assert corpus.match(skeleton("اطلبوا العلم ولو بالصين فإن طلب العلم فريضة على كل مسلم"))[0] == "partly_found"
    assert corpus.match(skeleton("قال رجل من اهل البادية كلاما طويلا لا يوجد في شيء"))[0] == "none"


def test_books_of_forged_reports_come_last():
    assert hadis.rank(report("sanadset:1", "تذكرة الموضوعات للفتني", "x")) > hadis.rank(report("sanadset:2", "مسند أحمد بن حنبل", "x"))
    assert hadis.rank(report("muslim:1", "Sahîh-i Müslim", "x", "hadith_api")) < hadis.rank(report("sanadset:2", "مسند أحمد بن حنبل", "x"))


@pytest.mark.parametrize("entry, source, expected", [
    ({"match": "found", "cited": False}, "kaynak", "found"),
    ({"match": "partly_found", "cited": True}, "meal", "partly_found"),
    ({"match": "none", "cited": True}, "kaynak", "cited"),
    ({"match": "short", "cited": False}, "kaynak", "marked"),
    ({"match": "none", "cited": False}, "baglam", "unsupported"),
    (None, "kaynak", None),
])
def test_support(entry, source, expected):
    assert support(entry, source) == expected


def test_classifier_rules():
    assert _mukattaat("كٓهٰیٰعٓصٓ حٰمٓ عٓسٓقٓ") and not _mukattaat("اِنَّمَا الْاَعْمَالُ بِالنِّيَّاتِ")
    assert not HADITH_BOOKS.search("el-Gazâlî, İhyâu Ulûmi'd-Dîn: 3:36")
    assert HADITH_BOOKS.search("Buharî, Rikak: 1")


def test_nurpedia_keeps_only_lines_with_a_hadith_book(tmp_path):
    (tmp_path / "a.html").write_text('<div class="mw-parser-output"><p>لَا عَيْشَ اِلَّا عَيْشُ الْاٰخِرَةِ</p><p>Gerçek hayat. (Buharî, Rikak: 1)</p>'
                                     '<p>اِنَّ اللّٰهَ مَعَ الصَّابِر۪ينَ</p><p>Allah sabredenlerle. (Bakara Sûresi, 2:153)</p></div>', "utf-8")
    assert hadis.nurpedia_citations(tmp_path) == {skeleton("لَا عَيْشَ اِلَّا عَيْشُ الْاٰخِرَةِ")}


@pytest.fixture(scope="module")
def library(tmp_path_factory):
    from conftest import ASA, SOZLER, _complete, mini_quran
    folder = tmp_path_factory.mktemp("hadis")
    books = tmp_path_factory.mktemp("books")
    hadith = "إِنَّمَا الْأَعْمَالُ بِالنِّيَّاتِ"
    text = f"Şöyle buyurdu: {hadith} dedi."
    start = text.index(hadith)
    book = json.loads(json.dumps(SOZLER))
    book["paragraphs"].append({"id": "sozler/11/p009", "node_id": "sozler/11", "kind": "paragraph", "text": text,
                               "arabic": [{"start": start, "end": start + len(hadith), "kind": "hadis"}]})
    book["sentences"].append({"id": "sozler/11/c009", "node_id": "sozler/11", "paragraph_id": "sozler/11/p009", "n": 9})
    data = _complete(book, {"sozler/11/p009": [text]} | _sentences())
    (books / "sozler.json").write_text(json.dumps(data, ensure_ascii=False), "utf-8")
    (books / "asa-yi-musa.json").write_text(json.dumps(_complete(ASA, _sentences()), ensure_ascii=False), "utf-8")
    key = skeleton(hadith)
    matches = folder / "matches.json"
    matches.write_text(json.dumps({"parts": {key: {"match": "found", "cited": False, "reports": ["abudawud:7", "bukhari:1", "sanadset:9"]}},
                                   "reports": {"abudawud:7": {"title": "Sünen-i Ebû Dâvûd", "number": "7", "text": "إنما", "source": "hadith_api", "grades": [["Al-Albani", "Sahih"]]},
                                               "bukhari:1": {"title": "Sahîh-i Buhârî", "number": "1", "text": "إنما", "source": "hadith_api", "grades": []},
                                               "sanadset:9": {"title": "تذكرة الموضوعات للفتني", "number": "3", "text": "إنما", "source": "sanadset", "grades": []},
                                               "sanadset:77": {"title": "unused", "number": "1", "text": "x", "source": "sanadset", "grades": []}}},
                                  ensure_ascii=False), "utf-8")
    out = folder / "test.db"
    quran = folder / "quran.json"
    quran.write_text(json.dumps(mini_quran(), ensure_ascii=False), "utf-8")
    build(books, out, quran, hadis_path=matches)
    lib = Library(out)
    yield lib
    lib.close()


def _sentences():
    from conftest import FIRST, HASR
    return {"sozler/10/p001": [FIRST, HASR], "sozler/10/p001/h1": ["Işık geldi."],
            "sozler/10/hakikat-01/p001": ["Kıyâmet ve mîzan günü gelecek."],
            "sozler/11/p001": ["قُلْ هُوَ اللّٰهُ اَحَدٌ"], "asa-yi-musa/haşir/p002": ["Bu mecmûa haşre dâirdir."]}


def test_find_hadith_gives_places_evidence_and_reports(library):
    part = library.find_hadith("انما الاعمال بالنيات")["parts"][0]
    assert part["hadith_support"] == "found" and part["places"][0]["id"].startswith("sozler/11/")
    ids = {r["id"]: r for r in part["reports"]}
    assert ids["abudawud:7"]["grades"] == [{"scholar": "Al-Albani", "grade": "Sahih"}]
    assert "grades" not in ids["bukhari:1"] and "no per-hadith grade" in ids["bukhari:1"]["collection_note"]
    assert "forged" in ids["sanadset:9"]["book_note"]


def test_only_used_reports_enter_and_attribution_is_given(library):
    assert library.conn.execute("SELECT count(*) FROM hadith_reports").fetchone()[0] == 3
    assert "CC BY 4.0" in library.hadith("sanadset:9")["source"]
    with pytest.raises(LibraryError):
        library.hadith("yok:1")


def test_reading_shows_the_support(library):
    items = library.read_section("sozler/11")["items"]
    parts = [a for i in items for a in i.get("arabic", [])]
    assert any(a.get("hadith_support") == "found" for a in parts)


def test_find_hadith_needs_arabic(library):
    with pytest.raises(LibraryError):
        library.find_hadith("haşir")
    assert library.find_hadith("لا يوجد هذا الكلام ابدا في شيء")["parts"] == []
