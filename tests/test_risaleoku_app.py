"""risaleoku.com uygulamasının metin biçimi: işaretler, hâşiye, Arapça, fihrist, şablonla yerleştirme."""

from risale_mcp.books.risaleoku import TocEntry
from risale_mcp.books.risaleoku_app import (_anchored, _slice, add_footnotes, article_starts, inline_starts, read_blocks,
                                            read_toc, title_entries)

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
    blocks = read_blocks("#1\n   Bir iki üç dört\n   Beş altı yedi sekiz\n   Dokuz on bir iki üç dört\n", {}, "tr")
    outline = [{"id": "e", "title": "E", "anchors": []},
               {"id": "e/a", "title": "A", "anchors": [["bir", "iki", "uc", "dort"]]},
               {"id": "e/b", "title": "B", "anchors": [["bes", "altı", "yedi", "sekiz"]]}]
    starts, lost = _anchored(blocks, outline)
    assert not lost and [n["id"] for n in starts[0]] == ["e/a"] and [n["id"] for n in starts[1]] == ["e/b"]


def test_indented_line_after_a_page_continues_a_broken_sentence():
    blocks = read_blocks("   tahammül\n#2\n   ettiniz, yılmadınız.\n#3\n   Yeni paragraf.\n", {}, "tr")
    assert [b.text.text for b in blocks] == ["tahammül ettiniz, yılmadınız.", "Yeni paragraf."]


def test_indented_line_after_arabic_continues_the_sentence():
    blocks = read_blocks("   gelince\n~اَللّٰهُ|@\n   âyeti imdadıma geldi.\n", {}, "tr")
    assert [b.text.text for b in blocks] == ["gelince اَللّٰهُ âyeti imdadıma geldi."]


def test_index_lines_stay_apart_across_a_page():
    blocks = read_blocks("   akıl , 22\n#2\n   aklı nakle tercih , 23\n", {}, "tr")
    assert len(blocks) == 2


def test_arabic_text_continues_across_a_page_only_without_a_full_stop():
    blocks = read_blocks("   قال إن\n#2\n   الله واحد.\n#3\n   ثم قال\n", {}, "ar")
    assert [b.text.text for b in blocks] == ["قال إن الله واحد.", "ثم قال"]


def test_meal_written_in_the_line_and_a_closing_on_the_next_line():
    blocks = read_blocks("~هُوَ|O.@\n~اَللّٰهُ\n|@\n", {}, "tr")
    assert [b.text.text for b in blocks] == ["هُوَ", "اَللّٰهُ"] and blocks[0].text.arabic[0].meal == "O."


def test_inline_marks_leave_no_trace():
    text = read_blocks("   إن ﹛﴿ اِنَّمَا ﴾|﹜ وفي ∫Evvelâ:>Çünkü bu\n", {}, "ar")[0].text.text
    assert text == "إن ﴿ اِنَّمَا ﴾ وفي Evvelâ: Çünkü bu"


def test_hasiye_at_the_end_of_a_page_finds_its_mark_in_an_earlier_paragraph():
    blocks = read_blocks("   Birinci (*) metin.\n   İkinci metin.\n{(*) Hâşiye.}\n", {}, "tr")
    assert "(*)" not in blocks[0].text.text and blocks[0].text.footnotes[0].content.text == "Hâşiye."
    assert not blocks[1].text.footnotes


def test_hasiye_written_as_a_paragraph_is_a_hasiye():
    blocks = read_blocks("   Birinci (حاشيه) metin.\n   (حاشيه): بو نكته\n", {}, "os")
    assert len(blocks) == 1 and blocks[0].text.footnotes[0].content.text == "بو نكته"


def _titles(body: str) -> dict[str, int]:
    blocks = read_blocks(body, {}, "tr")
    starts = title_entries(blocks)
    inline_starts(starts, blocks)
    return {h.title: h.depth for heads in starts.values() for h in heads}


def test_new_series_nests_only_while_the_open_series_goes_on():
    depths = _titles("<Bölüm>\n` Birinci Hakikat:>\n   a\n` Birinci Esas:>\n   b\n` İkinci Hakikat:>\n   c\n")
    assert (depths["Birinci Hakikat"], depths["Birinci Esas"], depths["İkinci Hakikat"]) == (3, 4, 3)
    depths = _titles("<Bölüm>\n` Birinci Kâr:>\n   a\n` İkinci Kâr:>\n   b\n` Birinci Hasaret:>\n   c\n")
    assert depths["Birinci Hasaret"] == depths["İkinci Kâr"]


def test_printed_heading_line_places_a_section_the_anchors_miss():
    blocks = read_blocks("#1\n<حبة>\n   نص\n<زَهْــرَةٌ>\n   نص آخر\n", {}, "ar")
    outline = [{"id": "e", "title": "E", "anchors": []},
               {"id": "e/a", "title": "حبة", "anchors": [["لا", "يوجد", "هذا", "ابدا"]], "printed": "حبة"},
               {"id": "e/b", "title": "زَهْــرَةٌ", "anchors": [["لا", "يوجد", "ذلك", "ابدا"]]}]
    starts, lost = _anchored(blocks, outline)
    assert not lost and [n["id"] for n in starts[0]] == ["e/a"] and [n["id"] for n in starts[2]] == ["e/b"]


def test_lowercase_line_continues_after_a_bold_start_a_small_line_or_a_blank_line():
    blocks = read_blocks("   tahammül\n  \\ettiniz.>\n", {}, "tr")
    assert [b.text.text for b in blocks] == ["tahammül ettiniz."]
    blocks = read_blocks("~عَلَيْكُمْ|@\n,hadîsinin sırrı>\n", {}, "tr")
    assert [b.text.text for b in blocks] == ["عَلَيْكُمْ hadîsinin sırrı"]
    blocks = read_blocks("   Müddeti azdır ki\n\nişâret ediyor.\n", {}, "tr")
    assert [b.text.text for b in blocks] == ["Müddeti azdır ki işâret ediyor."]


def test_lowercase_line_continues_a_label_only_without_a_colon():
    blocks = read_blocks("` İkinci Bürhan'ın>\nbeş noktası var:\n", {}, "tr")
    assert [b.text.text for b in blocks] == ["İkinci Bürhan'ın beş noktası var:"]
    blocks = read_blocks("` Birinci Esas:>\n   kâinatın sahibi.\n", {}, "tr")
    assert len(blocks) == 2


def test_start_words_place_a_section_inside_a_paragraph_run():
    blocks = read_blocks("#1\n   Bir iki üç dört.\n   Beş altı yedi sekiz.\n", {}, "ar")
    outline = [{"id": "e", "title": "E", "anchors": []},
               {"id": "e/a", "title": "Yok olan başlık", "anchors": [["yok"]], "start": "Beş altı yedi"}]
    starts, lost = _anchored(blocks, outline)
    assert not lost and [n["id"] for n in starts[1]] == ["e/a"]
