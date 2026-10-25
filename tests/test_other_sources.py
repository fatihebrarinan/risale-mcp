"""Aşama 4 ayrıştırıcıları: risale.online, risaleoku, Yeni Asya, kastamonur (ağ gerektirmez)."""

import gzip

from risale_mcp.books import kastamonur, risale_online, risaleoku, yeniasya
from risale_mcp.books.model import Text
from risale_mcp.catalog import Group, Site, SourceRef, Work


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


KASTAMONUR_PAGE = """<html><body><div class="a2a">paylaş</div>
<h3><span><b>Nutuklar ve Makaleler</b></span></h3>
<p>Not: Bu kısım iki bölümdür.</p>
<h1><span dir="rtl">ﻧﻄﻘﻠﺮ</span></h1>
<h1><strong>Nutuklar</strong></h1>
<p><strong>İfade-i Meram</strong></p>
<p>Kader bana Türkçeyi az vermiş.</p>
<h2><strong><span class="mw-headline">Nutuk &#8211; 2</span></strong></h2>
<p><strong>Prens Sabahaddin Beyin Fikrine Cevap</strong> (*)[*<sup class="reference">[1]</sup>]</p>
<p>Hayat ittihaddadır.[**<sup class="reference">[2]</sup>] Zira <span dir="rtl">ﻣَﻦْ ﻛَﺎﻥَ ﻟِﻠَّﻪِ</span> hürriyet var.</p>
<h3><strong>Birinci Hakikat</strong></h3>
<p>Timarhaneyi kabul ettim.[Haşiye<sup class="reference">[3]</sup>] Rezil olur.[2<sup class="reference">[1]</sup>]</p>
<p>Bediüzzaman</p>
<ol class="references">
<li id="cite_note-1"><span>Misbah’da başka türlü yazılmış.</span></li>
<li id="cite_note-2"><span>Kadınlaşmış erkek… (Müellif)</span></li>
<li id="cite_note-3"><span>İhsan-ı şahâneyi kabul etmedim.</span></li>
</ol>
<div style="text-align: center;"><strong>Makaleler Kısmı (2)</strong></div>
<h2><strong>Makale &#8211; 1</strong></h2>
<p><strong>Kürdler Neye Muhtaçtır?</strong>[*<sup class="reference">[1]</sup>]</p>
<p>Şark ve Kürdistan Gazetesi Sayı: 1 19 Teşrin-i Sani 1324</p>
<p>Gazeteler iki vazife deruhte etmiştir.</p>
<ol class="references"><li id="cite_note-1"><span>Makalenin nâşir notu.</span></li></ol>
<div class="wpautbox-below">yazar</div></body></html>"""


def kastamonur_book(tmp_path, section: str):
    book = "nutuklar-ve-makaleler"
    (tmp_path / book).mkdir()
    (tmp_path / book / "page.html.gz").write_bytes(gzip.compress(KASTAMONUR_PAGE.encode("utf-8")))
    work = Work("nutuk", "Nutuk", Group.ESKI_SAID, SourceRef(Site.KASTAMONUR, book, (section,)))
    return kastamonur.parse_work(work, tmp_path).to_json()


def test_kastamonur_nutuk(tmp_path):
    book = kastamonur_book(tmp_path, "nutuklar")
    nodes = {n["id"]: n for n in book["outline"]}
    assert list(nodes) == ["nutuk", "nutuk/ifade-i-meram", "nutuk/nutuk-02", "nutuk/nutuk-02/hakikat-01"]
    article = nodes["nutuk/nutuk-02"]
    assert (article["title"], article["toc_title"], article["number"]) == ("Prens Sabahaddin Beyin Fikrine Cevap", "Nutuk – 2", 2)
    texts = {p["id"]: p for p in book["paragraphs"]}
    main = texts["nutuk/nutuk-02/p001"]
    assert main["text"] == "Hayat ittihaddadır. Zira مَنْ كَانَ لِلَّهِ hürriyet var."   # ayraçsız, standart harfler
    assert main["text"][main["arabic"][0]["start"]:main["arabic"][0]["end"]] == "مَنْ كَانَ لِلَّهِ"
    hasiye = [p for p in book["paragraphs"] if p["kind"] == "hasiye"]
    assert [h["text"] for h in hasiye] == ["Kadınlaşmış erkek…", "İhsan-ı şahâneyi kabul etmedim."]   # (Müellif), [Haşiye]
    assert [n["text"] for n in book["notes"]] == ["Misbah’da başka türlü yazılmış."] * 2      # nâşir notu, metne girmez
    assert texts["nutuk/nutuk-02/hakikat-01/p001"]["text"] == "Timarhaneyi kabul ettim. Rezil olur."   # "[2[1]]" de işarettir
    assert texts["nutuk/nutuk-02/hakikat-01/p002"]["kind"] == "signature"


def test_kastamonur_makaleler_has_own_footnotes_and_publication_line(tmp_path):
    book = kastamonur_book(tmp_path, "makaleler")
    article = book["outline"][1]
    assert (article["id"], article["title"]) == ("nutuk/makale-01", "Kürdler Neye Muhtaçtır?")
    assert article["subtitle"] == "Şark ve Kürdistan Gazetesi Sayı: 1 19 Teşrin-i Sani 1324"
    assert [p["text"] for p in book["paragraphs"]] == ["Gazeteler iki vazife deruhte etmiştir."]
    assert [n["text"] for n in book["notes"]] == ["Makalenin nâşir notu."]                 # bölümün kendi listesi


def test_kastamonur_edition_gap_is_anchored_to_paragraph(tmp_path):
    from risale_mcp.books.model import Book
    book = Book("makalat", "Makalat", {})
    node = book.add_node(book.root, "makale-11", "Yaşasın Şeriat-ı Ahmedî")
    book.add_paragraph(node, "paragraph", Text("İstanbul’u Avrupa’ya kıyas etmişler."))
    book.add_paragraph(node, "paragraph", Text("Yaşasın Şeriat-ı Garrâ!.."))
    gap = kastamonur.EditionGap("makale-11", 1, "Hâtime yok.", after="İstanbul’u Avrupa’ya")
    assert kastamonur._gap_record(book, gap) == {"node_id": "makalat/makale-11", "missing_blocks": 1,
                                                 "after": "makalat/makale-11/p001", "note": "Hâtime yok."}
    end = kastamonur._gap_record(book, kastamonur.EditionGap("makale-11", 3, "Makale yok."))
    assert end["after"] == "makalat/makale-11/p002"                                      # düğümün sonu
