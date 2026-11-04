"""Beyzâvî ayrıştırıcısı (`books/beyzavi.py`, T3): kurallar, gerçek satırlardan kısaltılmış bir dosyayla.

Gerçek eser üzerindeki denetim (`test_real_book_*`) yerel ham veri ya da JSON yoksa atlanır.
"""

import json

import pytest

from risale_mcp.books import beyzavi, printed
from risale_mcp.catalog import get_work
from risale_mcp.sentences import segment

RAW = """######OpenITI#
#META# 040.EdEDITOR	:: محمد عبد الرحمن المرعشلي
#META#Header#End#

# PageV00P000
# [الجزء الاول]
# بسم الله الرحمن الرحيم
### | مقدمة التحقيق
# إن الحمد لله، نحمده ونستعينه.
# مقدمة
# أولا: ترجمة صاحب التفسير
# PageV01P007
### | أولا: ترجمة صاحب التفسير
### $ 1- اسمه ونسبه:
# هو العلامة المفسر «1» .
### | 2-
# وكتاب «الطوالع» مطبوع.
### | ثانيا: التعريف بأنوار التنزيل
# تفسير متوسط الحجم. PageV01P011
### | خطبة الكتاب
# الحمد لله الذي نزل الفرقان على عبده.
# PageV01P023
### | (1) سورة الفاتحة
# مكية وآيها سبع آيات
### |
### | [سورة الفاتحة (1) : آية
# 1]</span>
# بسم الله الرحمن الرحيم (1)
# بسم الله الرحمن الرحيم من الفاتحة، ومن كل سورة، وعليه قراءة مكة
~~والكوفة.
# وسئل محمد بن الحسن عنها فقال: ما بين الدفتين كلام الله تعالى
# . ولنا أحاديث كثيرة: منها
# ما روى أبو هريرة قال: «فاتحة الكتاب سبع آيات» . PageV01P026
### | [سورة الفاتحة (1) : الآيات 3 الى 4]
# الرحمن الرحيم (3) مالك يوم الدين (4)
# الرحمن الرحيم كرره للتعليل. PageV01P028
### | (2) سورة البقرة
# مدنية وآيها مائتان وسبع وثمانون آية
### |
### | [سورة البقرة (2) : آية
# 1]</span>
# بسم الله الرحمن الرحيم
# الم (1)
# الم وسائر الألفاظ التي يتهجى بها. وقيل إنها أسماء السور. PageV01P033
### | [سورة البقرة (2) : آية 34]
# وإذ قلنا للملائكة اسجدوا لآدم (34)
# بعد الحد.
"""


@pytest.fixture(scope="module")
def parsed(tmp_path_factory):
    root = tmp_path_factory.mktemp("openiti")
    (root / "beyzavi-shamela.txt").write_text(RAW, encoding="utf-8")
    book, report = beyzavi.parse(get_work("beyzavi"), raw_root=root)
    data = book.to_json()
    data["sentences"] = segment(data)
    printed.apply(data)
    return book, report, data


def _paras(data, node):
    return [p for p in data["paragraphs"] if p["node_id"] == node]


def test_outline_ids_titles_and_layers(parsed):
    _, report, data = parsed
    nodes = {n["id"]: n for n in data["outline"]}
    assert list(nodes) == ["beyzavi", "beyzavi/mukaddime-tahkik", "beyzavi/mukaddime-tahkik/1",
                           "beyzavi/mukaddime-tahkik/2", "beyzavi/hutbe", "beyzavi/1", "beyzavi/1/1", "beyzavi/1/3-4",
                           "beyzavi/2", "beyzavi/2/1"]                     # Bakara 34'te durur
    intro = nodes["beyzavi/mukaddime-tahkik"]
    assert intro["authority"] == "muhakkik" and intro["by"] == "Muhammed Abdurrahman el-Maraşlî"
    assert nodes["beyzavi/1"]["title"] == "سورة الفاتحة" and nodes["beyzavi/1"]["number"] == 1
    assert nodes["beyzavi/1/3-4"]["title"] == "الآيات 3 الى 4"
    assert nodes["beyzavi/1/3-4"]["verses"] == {"sura": 1, "start": 3, "end": 4}
    assert nodes["beyzavi/2/1"]["ref"] == "Envârü't-Tenzîl › سورة البقرة › آية 1"
    assert nodes["beyzavi/hutbe"]["subtitle"] == beyzavi.EDITION_HEADING
    assert report.units == 3 and report.unknown_pages == 0


def test_verse_lines_head_each_unit_and_are_not_sentences(parsed):
    _, report, data = parsed
    first = _paras(data, "beyzavi/1/3-4")[0]
    assert (first["kind"], first["verses"], first["text"]) == ("ayah", "quran:1:3-4", "الرحمن الرحيم (3) مالك يوم الدين (4)")
    besmele, alif = _paras(data, "beyzavi/2/1")[:2]
    assert besmele["kind"] == "ayah" and "verses" not in besmele and besmele["note"] == "sûre başı besmele"
    assert alif["verses"] == "quran:2:1"
    ayah_ids = {p["id"] for p in data["paragraphs"] if p["kind"] == "ayah"}
    assert not any(s["paragraph_id"] in ayah_ids for s in data["sentences"])
    assert data["sentences"][0]["id"].startswith("beyzavi/mukaddime-tahkik/c")


def test_lines_join_until_a_sentence_ends(parsed):
    _, _, data = parsed
    texts = [p["text"] for p in _paras(data, "beyzavi/1/1")[1:]]
    assert texts == [
        "بسم الله الرحمن الرحيم من الفاتحة، ومن كل سورة، وعليه قراءة مكة والكوفة.",
        "وسئل محمد بن الحسن عنها فقال: ما بين الدفتين كلام الله تعالى. ولنا أحاديث كثيرة: منها ما روى أبو هريرة قال:"
        " «فاتحة الكتاب سبع آيات» ."]                     # ". ولنا" boşluksuz; ":" ve cümle ortası birleşir


def test_intro_heading_lines_open_paragraphs_and_sura_text_is_the_authors(parsed):
    _, _, data = parsed
    assert [p["text"] for p in _paras(data, "beyzavi/mukaddime-tahkik/1")] == [
        "1- اسمه ونسبه: هو العلامة المفسر «1» .", "2- وكتاب «الطوالع» مطبوع."]
    assert _paras(data, "beyzavi/mukaddime-tahkik")[0]["text"].startswith("بسم الله الرحمن الرحيم إن الحمد لله")
    assert [p["text"] for p in _paras(data, "beyzavi/1")] == ["مكية وآيها سبع آيات"]
    assert any("[الجزء الاول]" in n["text"] for n in data["notes"])
    assert not any("[الجزء الاول]" in p["text"] for p in data["paragraphs"])


def test_printed_pages_reach_sentences(parsed):
    _, _, data = parsed
    by_id = {s["id"]: s for s in data["sentences"]}
    assert _paras(data, "beyzavi/mukaddime-tahkik/1")[0]["printed"] == {"volume": 1, "page": 11}
    assert by_id["beyzavi/2/1/c001"]["printed"] == {"volume": 1, "page": 33}
    hutbe = _paras(data, "beyzavi/hutbe")[0]
    assert hutbe["printed"] == {"volume": 1, "page": 23}


def test_printed_apply_splits_a_paragraph_at_its_page_break():
    data = {"paragraphs": [{"id": "x/p001", "text": "أ. ب.", "printed": {"volume": 1, "page": 5, "end": "1/6"},
                            "page_breaks": [[2, "1/5"]]}],
            "sentences": [{"id": "x/c001", "paragraph_id": "x/p001", "start": 0, "end": 2},
                          {"id": "x/c002", "paragraph_id": "x/p001", "start": 3, "end": 5}]}
    assert printed.apply(data) == 2
    assert [s["printed"] for s in data["sentences"]] == [{"volume": 1, "page": 5}, {"volume": 1, "page": 6}]


def test_a_verse_line_that_does_not_match_its_heading_stops_the_parse(tmp_path):
    (tmp_path / "beyzavi-shamela.txt").write_text(RAW.replace("مالك يوم الدين (4)", "مالك يوم الدين (5)"), encoding="utf-8")
    with pytest.raises(ValueError, match="1:3-4"):
        beyzavi.parse(get_work("beyzavi"), raw_root=tmp_path)


def test_real_book_covers_the_pilot_range():
    path = get_work("beyzavi").book_path
    if not path.exists():
        pytest.skip("beyzavi.json yok")
    data = json.loads(path.read_text("utf-8"))
    units = [n["verses"] for n in data["outline"] if n.get("verses")]
    covered = [(u["sura"], a) for u in units for a in range(u["start"], u["end"] + 1)]
    assert covered == [(1, a) for a in range(1, 8)] + [(2, a) for a in range(1, 34)]
    assert all(s.get("printed") for s in data["sentences"])
    assert sum(p["kind"] == "ayah" for p in data["paragraphs"]) == 40


def test_users_long_sentence_decision_holds():
    """T7: 100 kelimeyi aşan 28 cümle olduğu gibi kalır (kullanıcının kararı); bölme kuralı onları değiştirmemeli."""
    from risale_mcp.paths import ROOT
    path = get_work("beyzavi").book_path
    if not path.exists():
        pytest.skip("beyzavi.json yok")
    by_id = {s["id"]: s for s in json.loads(path.read_text("utf-8"))["sentences"]}
    locked = json.loads((ROOT / "tests" / "golden" / "beyzavi_long_sentences.json").read_text("utf-8"))["sentences"]
    assert len(locked) == 28
    assert [(sid, by_id[sid]["hash"]) for sid, _, _ in locked if sid in by_id] == [(sid, h) for sid, h, _ in locked]
