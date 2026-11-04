"""Rumuzat-ı Semaniye'nin nurpedia kaynağı: HTML okuyucu ve (ham veri diskteyse) gerçek eser."""

import json

import pytest

from risale_mcp.books.nurpedia_html import Block, Heading, Image, parse_page
from risale_mcp.catalog import get_work
from risale_mcp.paths import KULLIYAT_DIR, RAW_DIR

PAGE = """<html><script>"wgRevisionId":123</script><div class="mw-parser-output">
<div class="hf-nsheader"><a href="/wiki/x">Sözler</a></div>
<p><i><a href="/wiki/a">Rumuzat</a> → <a href="/wiki/b">4. Kısım</a>: Sonraki Risale</i></p>
<h2 id="x"><span></span>BİRİNCİ MESELE<span class="mw-editsection">[düzenle]</span></h2>
<p>Kur'an'daki <span dir="rtl">قُرْاٰنْ</span> kelimesi<sup class="reference"><a href="#cite_note-1">[1]</a></sup> ve ت harfi.</p>
<ul><li>Birinci madde</li></ul>
<h4>Birinci Cüz</h4><p><img src="/images/a.jpg" class="mw-file-element"/></p>
<ol class="references"><li id="cite_note-1"><span class="mw-cite-backlink">↑</span> <span class="reference-text">Hâşiye metni.</span></li></ol>
</div><div class="printfooter">x</div></html>"""


def test_page_blocks_notes_and_navigation():
    page = parse_page(PAGE, "t")
    assert page.revision == 123
    kinds = [type(b).__name__ for b in page.blocks]
    assert kinds == ["Heading", "Block", "Block", "Heading", "Image"]          # gezinti satırı ve liste atıldı
    assert page.blocks[0].text == "BİRİNCİ MESELE"
    para = page.blocks[1]
    assert para.text == "Kur'an'daki قُرْاٰنْ kelimesi ve ت harfi."
    assert any(r.rtl for r in para.runs) and para.notes == [(3, "cite_note-1")]          # işaret 3. parçadan önce: "kelimesi"nin ardı
    assert page.blocks[2].kind == "li"
    assert page.notes["cite_note-1"].text == "Hâşiye metni."


BOOK = KULLIYAT_DIR / "rumuzat-i-semaniye.json"
OLD = RAW_DIR.parent / "archive" / "rumuzat-pdf" / "rumuzat-i-semaniye.json"
needs_book = pytest.mark.skipif(not (BOOK.exists() and OLD.exists()), reason="eser JSON'u ya da eski kopyası yok")


@needs_book
def test_real_book_keeps_old_ids_and_tables():
    book = json.loads(BOOK.read_text(encoding="utf-8"))
    assert get_work("rumuzat-i-semaniye").source.site == "nurpedia"
    ids = {n["id"] for n in book["outline"]}
    aliases = {a["old"]: a["new"] for a in book["aliases"]}
    old = [n["id"] for n in json.loads(OLD.read_text(encoding="utf-8"))["outline"]]
    assert all(i in ids or aliases.get(i) in ids for i in old)                # eski bölüm kimlikleri kaybolmaz
    tables = [p for p in book["paragraphs"] if p["kind"] == "table"]
    assert len(tables) == 20 and all(p["source_edition"] == "pdf" for p in tables)
    assert len({p["source_id"] for p in book["paragraphs"] if "source_id" in p}) == \
        sum("source_id" in p for p in book["paragraphs"])                      # her PDF paragrafı bir kez
    assert "mektub-28-mesele-07" in {i.split("/")[1] for i in ids if "/" in i}
    assert not any("{{" in p.get("text", "") for p in book["paragraphs"])
    hasiye = [p for p in book["paragraphs"] if p["kind"] == "hasiye"]
    assert hasiye and all(p["text"] for p in hasiye)
