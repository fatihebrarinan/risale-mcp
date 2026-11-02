"""Hadis katmanı: eşleme, dayanak ve araçlar. Küçük derlem elle kurulur; ağa çıkılmaz."""

import json

import pytest

from risale_mcp import hadis
from risale_mcp.build_db import build
from risale_mcp.arabic_kinds import HADITH_BOOKS, _mukattaat
from risale_mcp.hadis import Corpus, Report, support
from risale_mcp.hadis_kunye import parse as parse_citation
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
    assert corpus.match("إِنَّمَا الْأَعْمَالُ بِالنِّيَّاتِ وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى")[:2] == ("found", [0])
    assert corpus.match("إِنَّمَا الْأَعْمَالُ بِالنِّيَّاتِ")[0] == "phrase_found"


def test_short_parts_are_not_searched(corpus):
    assert corpus.match("العلم") == ("short", [], 0)


def test_partial_needs_most_of_it_in_one_report(corpus):
    assert corpus.match("اطلبوا العلم ولو بالصين فإن طلب العلم فريضة على كل مسلم")[0] == "partly_found"
    assert corpus.match("قال رجل من اهل البادية كلاما طويلا لا يوجد في شيء")[0] == "none"


def test_a_match_must_keep_word_boundaries():
    corpus = Corpus([report("sanadset:1", "x", "انا معاشر الانبياء امرنا ان نكلم الناس على قدر عقولهم")])
    assert corpus.match("كلم الناس على قدر عقولهم")[0] == "partly_found"
    assert corpus.match("نكلم الناس على قدر عقولهم")[0] == "found"


def test_every_cut_of_an_elided_part_is_searched():
    corpus = Corpus([report("sanadset:1", "x", "اطلبوا العلم ولو بالصين ثم كلام اخر طويل فإن طلب العلم فريضة")])
    assert corpus.match("اطلبوا العلم ولو بالصين … فإن طلب العلم فريضة")[0] == "found"
    assert corpus.match("اطلبوا العلم ولو بالصين الخ")[0] == "phrase_found"     # dört kelime rivayeti ayırt etmez
    assert corpus.match("اطلبوا العلم ولو بالصين ثم الخ")[0] == "found"


def test_a_part_of_short_cuts_is_searched_whole():
    corpus = Corpus([report("sanadset:1", "x", "علم كثير ثم عمل قليل ثم صبر جميل")])
    assert corpus.match("علم كثير … عمل قليل")[0] == "none"
    assert corpus.match("علم كثير ثم عمل قليل")[0] != "short"


def test_locate_searches_only_the_cited_book():
    corpus = Corpus([Report("bukhari:1", "Sahîh-i Buhârî", "1", "قال المرء مع من احب", "hadith_api", (), 78),
                     Report("bukhari:2", "Sahîh-i Buhârî", "2", "قال كلام مع غيره", "hadith_api", (), 2),
                     Report("muslim:1", "Sahîh-i Müslim", "1", "المرء مع من احب", "hadith_api", (), 45)])
    cite = lambda raw: parse_citation(raw).citations
    level, found = corpus.locate("اَلْمَرْءُ مَعَ مَنْ اَحَبَّ", cite("Buhari, Edeb: 96"))
    assert level == "chapter" and found == [0]
    assert corpus.locate("اَلْمَرْءُ مَعَ مَنْ اَحَبَّ", cite("Buhari, Rikak: 1"))[0] == "book"
    assert corpus.locate("اَلْمَرْءُ مَعَ مَنْ اَحَبَّ", cite("Tirmizî, Zühd: 50")) == (None, [])
    assert corpus.locate("المرء مع", cite("Müsned, 1:2")) == (None, [])
    assert corpus.locate("رء مع من", cite("Buhari, Edeb: 96")) == (None, [])     # kelime sınırı


def test_a_book_level_hit_is_not_stored():
    corpus = Corpus([Report("bukhari:1", "Sahîh-i Buhârî", "1", "قال المرء مع من احب", "hadith_api", (), 78)])
    parsed = {"Buhari, Rikak: 1": parse_citation("Buhari, Rikak: 1").citations, "Buhari, Edeb: 96": parse_citation("Buhari, Edeb: 96").citations}
    assert set(hadis._located(corpus, "المرء مع من احب", "short", parsed)) == {"Buhari, Edeb: 96"}


def test_a_chapter_hit_lists_only_chapter_reports():
    corpus = Corpus([Report("bukhari:1", "Sahîh-i Buhârî", "1", "المرء مع من احب", "hadith_api", (), 78),
                     Report("bukhari:2", "Sahîh-i Buhârî", "2", "المرء مع من احب", "hadith_api", (), 2)])
    assert corpus.locate("المرء مع من احب", parse_citation("Buhari, Edeb: 96").citations) == ("chapter", [0])


def test_cited_books_are_chosen_first():
    corpus = Corpus([report(f"sanadset:{i}", f"k{i}", "x") for i in range(9)] + [report("sanadset:9", "aranan", "x")])
    assert corpus.select(set(range(10)), {"aranan"})[0] == 9


def test_a_location_belongs_to_its_citation():
    entry = {"match": "phrase_found", "cited": True, "located": {"Buhari, Edeb: 96": {"level": "chapter"}}}
    assert support(entry, "kaynak", True, "Buhari, Edeb: 96") == "located_chapter"
    assert support(entry, "kaynak", True, "Müslim, Birr: 1") == "cited"


def test_selection_prefers_different_books():
    corpus = Corpus([report(f"sanadset:{i}", "a", "x") for i in range(9)] + [report("sanadset:9", "b", "x")])
    chosen = corpus.select(set(range(10)))
    assert len(chosen) == hadis.MAX_REPORTS and 9 in chosen


def test_books_of_forged_reports_come_last():
    assert hadis.rank(report("sanadset:1", "تذكرة الموضوعات للفتني", "x")) > hadis.rank(report("sanadset:2", "مسند أحمد بن حنبل", "x"))
    assert hadis.rank(report("muslim:1", "Sahîh-i Müslim", "x", "hadith_api")) < hadis.rank(report("sanadset:2", "مسند أحمد بن حنبل", "x"))


@pytest.mark.parametrize("entry, source, expected", [
    ({"match": "found", "cited": False}, "kaynak", "found"),
    ({"match": "partly_found", "cited": True}, "meal", "partly_found"),
    ({"match": "none", "cited": True}, "kaynak", "cited"),
    ({"match": "short", "cited": False}, "kaynak", "marked"),
    ({"match": "phrase_found", "cited": False}, "kaynak", "phrase_found"),
    ({"match": "phrase_found", "cited": True}, "kaynak", "cited"),
    ({"match": "none", "cited": False}, "baglam", "unsupported"),
    (None, "kaynak", None),
])
def test_support(entry, source, expected):
    assert support(entry, source) == expected


def test_a_short_part_takes_only_its_own_citation():
    entry = {"match": "phrase_found", "cited": True}
    assert support(entry, "kaynak", True) == "cited" and support(entry, "kaynak", False) == "phrase_found"


def test_classifier_rules():
    assert _mukattaat("كٓهٰیٰعٓصٓ حٰمٓ عٓسٓقٓ") and not _mukattaat("اِنَّمَا الْاَعْمَالُ بِالنِّيَّاتِ")
    assert not HADITH_BOOKS.search("el-Gazâlî, İhyâu Ulûmi'd-Dîn: 3:36")
    assert HADITH_BOOKS.search("Buharî, Rikak: 1")


def test_nurpedia_keeps_only_lines_with_a_hadith_book(tmp_path):
    (tmp_path / "a.html").write_text('<div class="mw-parser-output"><p>لَا عَيْشَ اِلَّا عَيْشُ الْاٰخِرَةِ</p><p>Gerçek hayat. (Buharî, Rikak: 1)</p>'
                                     '<p>اِنَّ اللّٰهَ مَعَ الصَّابِر۪ينَ</p><p>Allah sabredenlerle. (Bakara Sûresi, 2:153)</p></div>', "utf-8")
    assert hadis.nurpedia_citations(tmp_path) == {skeleton("لَا عَيْشَ اِلَّا عَيْشُ الْاٰخِرَةِ"): {"Buharî, Rikak: 1"}}


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
    matches.write_text(json.dumps({"parts": {key: {"match": "found", "cited": False, "total": 3, "nurpedia": ["Buharî, Bed'ü'l-Vahy: 1"], "reports": ["abudawud:7", "bukhari:1", "sanadset:9"]}},
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
    assert part["hadith_support"] == "found" and part["reports_total"] == 3 and part["places"][0]["id"].startswith("sozler/11/")
    ids = {r["id"]: r for r in part["reports"]}
    assert ids["abudawud:7"]["grades"] == [{"scholar": "Al-Albani", "grade": "Sahih"}]
    assert "grades" not in ids["bukhari:1"] and "no per-hadith grade" in ids["bukhari:1"]["collection_note"]
    assert "forged" in ids["sanadset:9"]["book_note"]


def test_find_hadith_lists_the_citations(library):
    cited = library.find_hadith("انما الاعمال بالنيات")["parts"][0]["cited_in"]
    assert cited == [{"book": "Sahîh-i Buhârî", "kind": "hadis", "citation": "Buharî, Bed'ü'l-Vahy: 1", "from": "nurpedia"}]
    row = library.conn.execute("SELECT section, number FROM hadith_locators").fetchone()
    assert (row["section"], row["number"]) == (1, "1")


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
