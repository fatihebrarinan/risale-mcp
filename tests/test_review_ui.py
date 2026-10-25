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
}


def test_view_places_hasiye_markers_and_refs():
    view = to_view(SAMPLE)
    main, hasiye = view["passages"]
    assert main["text"].startswith("Metin (Haşiye-1) </script>")
    assert main["ref"] == "Sözler › Birinci Söz › ¶1"
    assert hasiye["ref"] == "Sözler › Birinci Söz › ¶1 › Hâşiye"
    assert hasiye["label"] == "Haşiye-1"


def test_embedded_json_cannot_close_script_tag():
    embedded = embed_json(to_view(SAMPLE))
    assert "</script>" not in embedded
    assert json.loads(embedded)["passages"][0]["text"].startswith("Metin (Haşiye-1) </script>")


def test_render_is_self_contained():
    html = render(SAMPLE)
    for marker in ("/*__STYLE__*/", "/*__SCRIPT__*/", "__DATA__", "__TITLE__"):
        assert marker not in html
    assert "<h1>Sözler</h1>" in html
