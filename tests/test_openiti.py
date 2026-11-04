"""Ortak OpenITI okuyucu (`openiti.py`, H6): üst bilgi, paragraflar, âyet ve sayfa işaretleri.

Örnekler ham dosyaların gerçek satırlarındandır (Buhârî'nin başı), kısaltılmıştır.
"""

import pytest

from risale_mcp import openiti
from risale_mcp.openiti import Page, clean, read, version_info
from risale_mcp.sources.openiti import Text

RAW = """######OpenITI#
#META# 040.EdEDITOR	:: د. مصطفى ديب البغا
#META# 043.EdPUBLISHER	:: دار ابن كثير , اليمامة
#META# 045.EdYEAR	:: 1407 - 1987
#META# 049.EdISBN	:: NODATA
#META#Header#End#

# صحيح البخاري PageV01P001 بسم الله الرحمن الرحيم
### | ( باب بدء الوحي )
### || ( 1 باب كيف كان بدء الوحي وقول الله جل ذكره @QB@ إنا أوحينا إليك @QE@ )
# 1 حدثنا الحميدي قال حدثنا سفيان
~~يقول * إنما الأعمال بالنيات
~~هاجر إليه PageV01P003
# 2 حدثنا عبد الله بن يوسف * أن الحارث PageV01P004 سأل رسول الله \\ 1 ms0007 \\
# PageV02P005
# 3 حدثنا يحيى
# 4 حدثنا بعد آخر سيفة
"""


def test_header_gives_the_edition_of_the_page_numbers():
    doc = read(RAW)
    assert doc.edition == {"editor": "د. مصطفى ديب البغا", "publisher": "دار ابن كثير , اليمامة", "year": "1407 - 1987"}
    with pytest.raises(ValueError):
        read("# metin\n")                                            # üst bilgisiz dosya


def test_paragraphs_headings_and_continuations():
    paras = read(RAW).paragraphs
    assert [p.level for p in paras] == [None, 1, 2, None, None, None, None, None]
    assert paras[5].text == "" and paras[5].page is None          # yalnız sayfa işareti (Buhârî'de 235 satır)
    assert paras[1].text == "( باب بدء الوحي )"
    assert paras[3].text == "1 حدثنا الحميدي قال حدثنا سفيان يقول * إنما الأعمال بالنيات هاجر إليه"


def test_quran_marks_become_brackets_with_their_span():
    p = read(RAW).paragraphs[2]
    assert "﴿ إنا أوحينا إليك ﴾" in p.text
    (start, end), = p.quran
    assert p.text[start:end] == "إنا أوحينا إليك"


def test_page_marker_ends_its_page():
    """OpenITI'nin kuralı: işaretten önceki metin o sayfada, sonraki metin bir sonraki işaretin sayfasındadır."""
    paras = read(RAW).paragraphs
    assert paras[0].page == Page(1, 1) and paras[0].end_page == Page(1, 3)       # başlık sayfası, sonra 3. sayfa
    assert (paras[3].page, paras[3].end_page) == (Page(1, 3), Page(1, 3))        # 1. hadis 3. sayfada biter
    assert paras[4].printed() == {"volume": 1, "page": 4, "end": "2/5"}           # 2. hadis 4'te başlar, 5'e taşar
    assert paras[6].page is None and paras[7].page is None                       # son işaretten sonrası: bilinmez


def test_marks_are_dropped_without_touching_the_letters():
    text, quran, breaks = clean("أن الحارث PageV01P004 سأل رسول الله \\ 1 ms0007 \\ قال ms0008")
    assert text == "أن الحارث سأل رسول الله قال" and quran == []
    assert breaks == [(len("أن الحارث"), Page(1, 4))]


def test_version_info_reads_the_yml():
    yml = ("00#VERS#URI######: 0256Bukhari.Sahih.JK000110-ara1\n80#VERS#COLLATED#: http://x (2002 reprint)\n"
           "90#VERS#COMMENT##: 1- The version I used\n    has other page numbers.\n80#VERS#LINKS####:\n")
    assert version_info(yml) == {"URI": "0256Bukhari.Sahih.JK000110-ara1", "COLLATED": "http://x (2002 reprint)",
                                 "COMMENT": "1- The version I used has other page numbers."}


def test_text_urls_are_pinned_to_a_commit():
    t = Text("0275AH", "44e1c3", "0256Bukhari/0256Bukhari.Sahih/0256Bukhari.Sahih.JK000110-ara1.completed")
    assert t.url() == ("https://raw.githubusercontent.com/OpenITI/0275AH/44e1c3/data/0256Bukhari/0256Bukhari.Sahih/"
                       "0256Bukhari.Sahih.JK000110-ara1.completed")
    assert t.yml_url().endswith("/0256Bukhari.Sahih/0256Bukhari.Sahih.JK000110-ara1.yml")
    assert t.file == "0275AH/data/" + t.path


def test_hadith_books_get_their_printed_page():
    from risale_mcp.hadis_kutub import parse, to_json
    nodes, hadiths, stats = parse("bukhari", RAW)
    data = to_json("bukhari", nodes, hadiths, read(RAW).edition)
    printed = {h["id"]: h.get("printed") for h in data["hadiths"]}
    assert printed == {"bukhari/1": {"volume": 1, "page": 3}, "bukhari/2": {"volume": 1, "page": 4, "end": "2/5"},
                       "bukhari/3": None, "bukhari/4": None}
    assert data["source"]["edition"]["editor"] == "د. مصطفى ديب البغا" and stats["sayfasiz"] == 2
    assert openiti.RAW_ROOT.name == "openiti"
