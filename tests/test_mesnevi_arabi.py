"""el-Mesnevî el-Arabî: Badıllı baskısının Word dosyası (QCF âyetleri, Word dipnotları, Türkçeyle paralel yapı).

Küçük bir Word dosyası ve bir mushaf sayfasının kelime verisi elle kurulur. Son test gerçek dosyayı kullanır.
"""

import gzip
import json
import zipfile

import pytest

from risale_mcp.books.mesnevi_arabi import _ordinal, parse
from risale_mcp.catalog import get_work
from risale_mcp.paths import BOOKS_DIR
from risale_mcp.sentences import split

WORK = get_work("el-mesnevi-el-arabi")


def p(text: str = "", align: str = "both", runs: str = "") -> str:
    body = runs or f"<w:r><w:t>{text}</w:t></w:r>"
    return f'<w:p><w:pPr><w:jc w:val="{align}"/></w:pPr>{body}</w:p>'


def qcf(chars: str, page: int = 1) -> str:
    return f'<w:r><w:rPr><w:rFonts w:cs="QCF_P{page:03d}"/></w:rPr><w:t>{chars}</w:t></w:r>'


def text(t: str) -> str:
    return f'<w:r><w:t xml:space="preserve">{t}</w:t></w:r>'


def note_ref(i: int) -> str:
    return f'<w:r><w:footnoteReference w:id="{i}"/></w:r>'


DOCUMENT = "".join([
    p("مقدمة الناشر لا تؤخذ", "center"),
    p("تَرْجَمَةُ المُقَدِّمَةِ التُّرْكِيَّةِ بِالْعَرَبِيَّةِ", "center"), p("النُّقْطَةُ الْأُولَى: كلام."),
    p("******", "center"),
    p("لَـمَـعَــاتٌ", "center"), p("مِنْ شَمْسِ التَّوْحِيدِ", "center"),
    p("اَللَّمْعَةُ الْأُولَى: فِيهِ * وَفِيهِ اَيْضًا."),
    p(runs=text("كما قال {") + qcf("ﭑ ﭒ ﭓ") + text("} وهذا (") + note_ref(2) + text(") صحيح.")),
    p("اَللَّمْعَةُ الْحَادِيَةُ عَشَرَ: كلام."),
    p("الفهرس", "center"), p("لا يؤخذ."),
])
FOOTNOTES = ('<w:footnotes><w:footnote w:id="2"><w:p><w:r><w:t>(?) هذا من الأصل ـ المؤلف ـ</w:t></w:r></w:p>'
             '</w:footnote></w:footnotes>')
PAGE = {"pagination": {"total_pages": 1}, "verses": [{"verse_key": "1:1", "words": [
    {"code_v1": c, "char_type_name": t, "position": i, "text_uthmani": w}
    for i, (c, t, w) in enumerate([("ﭑ", "word", "بِسْمِ"), ("ﭒ", "word", "ٱللَّهِ"), ("ﭓ", "word", "ٱلرَّحْمَـٰنِ"),
                                    ("ﭔ", "word", "ٱلرَّحِيمِ"), ("ﭕ", "end", "١")], 1)]}]}


@pytest.fixture(scope="module")
def book(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("mesnevi")
    path = tmp / "m.docx"
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("word/document.xml", f"<w:document><w:body>{DOCUMENT}</w:body></w:document>")
        z.writestr("word/footnotes.xml", FOOTNOTES)
    (tmp / "glyphs" / "pages").mkdir(parents=True)
    (tmp / "glyphs" / "pages" / "001.json.gz").write_bytes(gzip.compress(json.dumps(PAGE).encode()))
    book, report = parse(WORK, path, tmp / "glyphs")
    return book.to_json(), report


def test_structure_parallel_to_the_turkish_work(book):
    data, _ = book
    ids = [n["id"].removeprefix("el-mesnevi-el-arabi/") for n in data["outline"][1:]]
    assert ids == ["mukaddime", "mukaddime/nokta-01", "lemalar", "lemalar/lema-01", "lemalar/lema-11"]
    lemalar = next(n for n in data["outline"] if n["id"].endswith("/lemalar"))
    assert lemalar["subtitle"] == "مِنْ شَمْسِ التَّوْحِيدِ"
    assert not any("لا تؤخذ" in x["text"] or "لا يؤخذ" in x["text"] for x in data["paragraphs"])


def test_qcf_glyphs_become_the_verse_and_footnotes_are_attributed(book):
    data, report = book
    para = next(x for x in data["paragraphs"] if x["text"].startswith("كما قال"))
    assert para["text"] == "كما قال {بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ} وهذا صحيح."
    span = para["arabic"][0]
    assert (para["text"][span["start"]:span["end"]], span["source"]) == ("بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ", "Fâtiha Sûresi, 1:1")
    hasiye = [x for x in data["paragraphs"] if x["kind"] == "hasiye"]
    assert [h["text"] for h in hasiye] == ["هذا من الأصل"] and report.hasiye == 1


def test_star_ends_a_sentence_only_when_asked():
    text = "فِيهِ * وَفِيهِ اَيْضًا."
    assert len(split(text)) == 1 and len(split(text, star=True)) == 2


def test_ordinals():
    assert (_ordinal(["الرابعة"]), _ordinal(["الحادية", "عشرة"]), _ordinal(["الرابع", "عشر"])) == (4, 11, 14)


def test_real_mesnevi():
    path = BOOKS_DIR / "el-mesnevi-el-arabi.json"
    if not path.exists():
        pytest.skip("el-mesnevi-el-arabi.json yok")
    data = json.loads(path.read_text(encoding="utf-8"))
    ids = {n["id"].removeprefix("el-mesnevi-el-arabi/") for n in data["outline"]}
    assert {f"lemalar/lema-{n:02d}" for n in range(1, 15)} <= ids
    assert {f"reshalar/resha-{n:02d}" for n in range(1, 13)} <= ids
    assert {"katre/bab-01", "katre/hatime", "katre/zeyl", "habbe/zeylul-habbe", "sule/zeyl"} <= ids
