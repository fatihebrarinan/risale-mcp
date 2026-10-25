"""Aşama 4 ayrıştırıcıları: risale.online, risaleoku, Yeni Asya (ağ gerektirmez)."""

from risale_mcp.books import risale_online, risaleoku, yeniasya
from risale_mcp.books.model import Text


def test_risale_online_paragraph_html():
    html = (
        '<div class="paragraf-icerik"><p class="paragraf hizalama-iki-yana">'
        '<span class="kelime-grup OsmanlicaStandart">şimendifer</span> '
        '<span class="kelime-grup OsmanlicaStandartKirmiziUstSimge" data-hasiye-no="1">Hâşiye</span> '
        '<span class="kelime-grup OsmanlicaStandart">gāibden gelir</span><span class="kelime-grup">,</span> '
        '<span class="kelime-grup ArabiKirmizi" data-mehaz-id="7" data-mehaz-latince-meal="Allah’ın adıyla" '
        'data-mehaz-latince-kaynak="(Sûre-i Fâtiha, 1:1)"><span class="kelime-grup">بِسْمِ اللّٰهِ</span></span>'
        '</p><section><aside class="paragraf-hasiye" data-hasiye-no="1">'
        '<span class="kelime-grup">Hâşiye</span> <span class="kelime-grup">Seneye işârettir</span></aside></section></div>'
    )
    parsed = risale_online._ParagraphHTML()
    parsed.feed(html)
    text = Text.from_builder(parsed.main)
    assert text.text == "şimendifer gāibden gelir, بِسْمِ اللّٰهِ"
    assert text.text[: text.footnotes[0].offset].endswith("şimendifer")
    assert (text.arabic[0].kind, text.arabic[0].meal, text.arabic[0].source) == ("ayet", "Allah’ın adıyla", "Sûre-i Fâtiha, 1:1")
    assert Text.from_builder(parsed.hasiyeler["1"]).text == "Seneye işârettir"


def test_risale_online_mehaz_without_arabic_class_is_arabic():
    html = ('<p class="paragraf"><span class="kelime-grup OsmanlicaStandartKirmizi" data-mehaz-id="352" '
            'data-mehaz-latince-meal="Bâkî olan, O’dur" data-mehaz-latince-kaynak="(Arabî ibâre)">'
            'اَلْبَاق۪ي هُوَ الْبَاق۪ي</span></p>')
    parsed = risale_online._ParagraphHTML()
    parsed.feed(html)
    text = Text.from_builder(parsed.main)
    assert text.is_arabic() and text.arabic[0].meal == "Bâkî olan, O’dur"


def test_risale_online_stanza_numbers_are_not_text():
    assert risale_online._STANZA_NUMBER.fullmatch("12")
    assert not risale_online._STANZA_NUMBER.fullmatch("1339 Hicrî")


def test_risaleoku_page_blocks_and_toc():
    page = (
        '<div id="dim-bottom" class="dim-overlay"></div>\n  </div>\n'
        "<span class='barla'>KÜÇÜK SÖZLER</span> <br /><br />"
        "<span class='arapca' data-content='Rahmân ve Rahîm olan Allah’ın adıyla.'><span class='arapca_ic'>بِسْمِ اللّٰهِ</span></span><br /><br />"
        "<font style='background-color: rgba(1,2,3,0.3);'>Ey kardeş! Benden birkaç nasihat istedin.</font><br /><br />"
        "<center>* * *</center><br /><br />"
        "<span class='hasiye'>{(Haşiye): Bu makam bir derstir.}</span><br /><br />"
        '</div>\n<div><input type="hidden" id="baslangic" value="4">'
    )
    blocks = risaleoku.page_blocks(page, 4, strip_footnote_marks=False)
    assert [b.text.text if not isinstance(b, str) else b for b in blocks] == [
        "KÜÇÜK SÖZLER", "بِسْمِ اللّٰهِ", "Ey kardeş! Benden birkaç nasihat istedin.", "Bu makam bir derstir."]
    assert blocks[0].centered and blocks[1].text.is_arabic() and blocks[1].text.arabic[0].meal.startswith("Rahmân")

    toc = risaleoku.read_toc(
        "<ul id=\"treemenu1\" class=\"treeview\"><li><a href='/oku/ksozler/4'>KÜÇÜK SÖZLER</a><ul>"
        "<li><a href='/oku/ksozler/5'>Birinci Söz</a></li>"
        "<li><a href='/oku/ksozler/40'>Dokuzuncu Söz</a><ul><li><a href='/oku/ksozler/41'>Birinci Nükte</a></li></ul></li>"
        "</ul></li></ul>")
    assert [(e.depth, e.title, e.page) for e in toc] == [(1, "Birinci Söz", 5), (1, "Dokuzuncu Söz", 40), (2, "Birinci Nükte", 41)]


def test_yeniasya_repairs():
    assert yeniasya.repair_capitals("Bundan ibret alınız. pencerenin kapatılması. zira hürriyet var.") == \
        "Bundan ibret alınız. Pencerenin kapatılması. Zira hürriyet var."
    assert yeniasya.clean_label("BirinCi CinaYET") == "Birinci Cinayet"
    assert yeniasya.clean_label("İk i n c i s i :") == "İkincisi:"
    para = yeniasya.Paragraph()
    for piece in ["zira mevcudiyet-i kav-", "miyeyi gösterir."]:
        para.add(piece)
    assert para.text == "Zira mevcudiyet-i kavmiyeyi gösterir."            # tire kalktı, baş harf büyüdü


def test_yeniasya_work_boundaries():
    toc = [yeniasya.TocEntry(t, p) for t, p in [
        ("Makalât", 17), ("Bu Esere Ait Takdim", 18), ("Hamidiye Alaylarına Dair", 19),
        ("Divan-ı Harb-i Örfî ve Said Nursî", 111), ("Bu Esere Ait Takdim", 112), ("Mukaddime", 117),
        ("Nutuk", 167), ("Bu Esere Ait Takdim", 168), ("İfade-i Meram", 169), ("Münazarat", 199), ("İfade-i Meram", 201)]]
    entries, end = yeniasya.work_entries(toc, "makalat", title_pages={17, 167, 199})
    assert [e.title for e in entries] == ["Hamidiye Alaylarına Dair"] and end == 111
    entries, end = yeniasya.work_entries(toc, "nutuk", title_pages={17, 167, 199})
    assert [e.title for e in entries] == ["İfade-i Meram"] and end == 199       # Münazarat'ta takdim yok
