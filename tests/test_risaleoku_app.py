"""risaleoku.com uygulamasının metin biçimi: işaretler, hâşiye, Arapça, fihrist, şablonla yerleştirme."""

from risale_mcp.books.risaleoku import TocEntry
from risale_mcp.books.risaleoku_app import _anchored, _slice, add_footnotes, article_starts, read_blocks, read_toc

BODY = """#3
<Başlık>
,* * *>
   Bu bir paragraf ve
#4
sayfada sürüyor (*) burada
~اَللّٰهُ|7@
sırrı tahakkuk eder.
{(*) Bir hâşiye. -Müellif-}
  \\Birinci Esas:>Etiketli paragraf.
÷Said Nursî>
"""


def test_markers_paragraphs_and_inline_arabic():
    blocks = read_blocks(BODY, {"7": "Allah"}, "tr")
    assert [b.marker for b in blocks] == ["title", "", "", "sign"]
    assert blocks[1].text.text == "Bu bir paragraf ve sayfada sürüyor burada اَللّٰهُ sırrı tahakkuk eder."
    assert blocks[1].text.arabic[0].meal == "Allah"
    assert blocks[2].label == "Birinci Esas:" and blocks[2].text.text == "Birinci Esas: Etiketli paragraf."
    assert blocks[3].signature


def test_hasiye_binds_to_its_mark_and_the_mark_leaves_the_text():
    paragraph = read_blocks(BODY, {}, "tr")[1]
    mark = paragraph.text.footnotes[0]
    assert "(*)" not in paragraph.text.text
    assert paragraph.text.text[:mark.offset].endswith("sürüyor")
    assert mark.content.text == "Bir hâşiye. -Müellif-"


def test_footnote_file_finds_mark_on_a_continued_paragraph():
    blocks = read_blocks("#1\n   Metin başı\n#2\nsonu (3) devam.\n", {}, "ar")
    assert add_footnotes(blocks, "2|(3)|Not metni") == []
    assert "(3)" not in blocks[0].text.text and blocks[0].text.footnotes[0].content.text == "Not metni"


def test_hizb_verses_become_separate_paragraphs():
    blocks = read_blocks("#1\n~اَلْحَمْدُ ﴿١﴾ اَلرَّحْمٰنِ ﴿٢﴾|@\n", {}, "ar", split_verses=True)
    assert [b.text.text for b in blocks] == ["اَلْحَمْدُ ﴿١﴾", "اَلرَّحْمٰنِ ﴿٢﴾"]


def test_presentation_forms_become_standard_letters():
    assert read_blocks("   ﺣِﺰْﺏُ\n", {}, "ar")[0].text.text == "حِزْبُ"


def test_toc_groups_take_the_page_of_their_first_child():
    toc = read_toc("Kitap|1\n\tGrup\n\t\tAlt@ikinci|5\n\tDiğer@—|9\n")
    assert toc == [TocEntry(1, "Grup", 5), TocEntry(2, "Alt", 5, "ikinci"), TocEntry(1, "Diğer", 9)]


def test_articles_take_printed_name_and_publication_subtitle():
    body = "#1\n&Nutuklar>\n<MAKALE - 5>\n<VOLKAN>\n<HAKİKAT>\n,Sayı: 70>\n   Metin.\n<İHTAR>\n   Devam.\n"
    blocks, starts = article_starts(read_blocks(body, {}, "tr")[1:])
    head = starts[0][0]
    assert (head.title, head.subtitle, head.local) == ("HAKİKAT", "VOLKAN · Sayı: 70", "makale-05")
    assert starts[2][0].title == "İHTAR"


def test_slice_prefers_top_level_heading():
    blocks = read_blocks("#1\n<Nutuklar ve Makaleler>\n&Nutuklar>\n   Bir.\n&Lemeât>\n   İki.\n", {}, "tr")
    assert [b.text.text for b in _slice(blocks, "Nutuklar", "Lemeât")] == ["Bir."]


def test_anchor_chain_ignores_a_false_later_match():
    blocks = read_blocks("#1\n   bir iki üç dört\n   beş altı yedi sekiz\n   dokuz on bir iki üç dört\n", {}, "tr")
    outline = [{"id": "e", "title": "E", "anchors": []},
               {"id": "e/a", "title": "A", "anchors": [["bir", "iki", "uc", "dort"]]},
               {"id": "e/b", "title": "B", "anchors": [["bes", "altı", "yedi", "sekiz"]]}]
    starts, lost = _anchored(blocks, outline)
    assert not lost and [n["id"] for n in starts[0]] == ["e/a"] and [n["id"] for n in starts[1]] == ["e/b"]
