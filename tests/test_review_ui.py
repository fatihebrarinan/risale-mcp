"""Kontrol arayüzü üreticisinin testleri."""

import json

from risale_mcp.review_ui import embed_json, render, to_view

SAMPLE = {
    "work": "sozler",
    "title": "Sözler",
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
BOOKS = [{"slug": "sozler", "title": "Sözler"}, {"slug": "mektubat", "title": "Mektubat"}]


def test_view_keeps_text_and_carries_positions():
    view = to_view(SAMPLE, BOOKS)
    main, hasiye = view["passages"]
    assert main["text"] == SAMPLE["paragraphs"][0]["text"]          # metin değiştirilmez
    assert main["ref"] == "Sözler › Birinci Söz › ¶1"
    assert (hasiye["ref"], hasiye["label"], hasiye["offset"]) == ("Sözler › Birinci Söz › ¶1 › Hâşiye", "Haşiye-1", 5)
    assert view["sentences"] == [{"id": "sozler/1/c001", "p": "sozler/1/p001", "s": 0, "e": 29, "n": 1,
                                  "incipit": "Metin </script><b>x</b> son.", "ref": "Sözler › Birinci Söz › 1. cümle"}]
    assert view["books"] == BOOKS


def test_embedded_json_cannot_close_script_tag():
    embedded = embed_json(to_view(SAMPLE, BOOKS))
    assert "</script>" not in embedded
    assert json.loads(embedded)["passages"][0]["text"].startswith("Metin </script>")


def test_render_is_self_contained():
    html = render(SAMPLE, BOOKS)
    for marker in ("/*__STYLE__*/", "/*__SCRIPT__*/", "__DATA__", "__TITLE__"):
        assert marker not in html
    assert "<h1>Sözler</h1>" in html
