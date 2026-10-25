"""Kontrol arayüzü üreticisinin testleri."""

import json

from risale_mcp.review_ui import book_view, embed_json, index_view, render_book, render_index

SAMPLE = {
    "work": "sozler",
    "title": "Sözler",
    "group": "ana-cilt",
    "outline": [
        {"id": "sozler", "parent_id": None, "title": "Sözler", "ref": "Sözler"},
        {"id": "sozler/1", "parent_id": "sozler", "title": "Birinci Söz", "ref": "Sözler › Birinci Söz"},
    ],
    "paragraphs": [
        {"id": "sozler/1/p001", "node_id": "sozler/1", "kind": "paragraph", "text": "Metin </script><b>x</b> son."},
        {"id": "sozler/1/p001/h1", "node_id": "sozler/1", "kind": "hasiye", "parent_id": "sozler/1/p001",
         "offset": 5, "text": "Hâşiye metni"},
    ],
    "sentences": [
        {"id": "sozler/1/c001", "node_id": "sozler/1", "paragraph_id": "sozler/1/p001", "n": 1, "start": 0,
         "end": 29, "text": "Metin </script><b>x</b> son.", "incipit": "Metin </script><b>x</b> son.",
         "ref": "Sözler › Birinci Söz › 1. cümle", "hash": "x"},
    ],
}
MECMUA = {
    "work": "asa-yi-musa", "title": "Asâ-yı Mûsâ", "group": "mecmua",
    "outline": [{"id": "asa-yi-musa", "parent_id": None, "title": "Asâ-yı Mûsâ", "ref": "Asâ-yı Mûsâ",
                 "sources": ["sozler/1"]}],
    "paragraphs": [{"id": "asa-yi-musa/p001", "node_id": "asa-yi-musa", "kind": "paragraph",
                    "source": ["sozler/1/p001"]}],
    "sentences": [],
}


def test_book_view_keeps_text_and_carries_positions():
    view = book_view(SAMPLE)
    main, hasiye = view["passages"]
    assert main["text"] == SAMPLE["paragraphs"][0]["text"]          # metin değiştirilmez
    assert main["ref"] == "Sözler › Birinci Söz › ¶1"
    assert (hasiye["ref"], hasiye["label"], hasiye["offset"]) == ("Sözler › Birinci Söz › ¶1 › Hâşiye", "Haşiye-1", 5)
    assert view["sentences"] == [{"id": "sozler/1/c001", "p": "sozler/1/p001", "s": 0, "e": 29, "n": 1,
                                  "incipit": "Metin </script><b>x</b> son.", "ref": "Sözler › Birinci Söz › 1. cümle"}]


def test_index_holds_every_outline_grouped():
    index = index_view([SAMPLE, MECMUA])
    assert [g["id"] for g in index["groups"]] == ["ana-cilt", "mecmua"]      # yalnızca eseri olan gruplar
    assert [w["slug"] for w in index["works"]] == ["sozler", "asa-yi-musa"]
    assert index["works"][0]["counts"] == {"nodes": 2, "passages": 1, "sentences": 1}
    nodes = {n["id"]: n for n in index["outline"]}
    assert nodes["sozler/1"]["p"] == 1 and nodes["sozler"]["p"] == 0        # kendi paragraf sayısı
    assert nodes["asa-yi-musa"]["sources"] == ["sozler/1"]
    assert "passages" not in index                                         # metin eser dosyasında


def test_embedded_json_cannot_close_script_tag():
    embedded = embed_json(book_view(SAMPLE))
    assert "</script>" not in embedded
    assert json.loads(embedded)["passages"][0]["text"].startswith("Metin </script>")


def test_render_index_and_book_file():
    html = render_index([SAMPLE])
    for marker in ("/*__STYLE__*/", "/*__SCRIPT__*/", "__DATA__", "__TITLE__"):
        assert marker not in html
    assert 'id="book"' not in html                                         # eser seçici yok
    script = render_book(SAMPLE)
    assert script.startswith("RisaleReview.register(") and script.rstrip().endswith(");")
    assert json.loads(script[len("RisaleReview.register("):script.rindex(")")])["book"] == "sozler"
