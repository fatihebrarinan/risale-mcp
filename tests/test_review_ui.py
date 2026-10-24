"""Kontrol arayüzü üreticisinin testleri."""

import json

from risale_mcp.review_ui import embed_json, render, slim

SAMPLE = {
    "book": "sozler",
    "title": "Sözler",
    "outline": [{"id": "sozler/1", "title": "Birinci Söz", "subtitle": None, "parent_id": None,
                 "ref": "Sözler › Birinci Söz", "page_start": 5, "depth": 1}],
    "passages": [
        {"id": "sozler/1/p001", "node_id": "sozler/1", "kind": "paragraph", "seq": 1,
         "text": "Metin </script><b>x</b> (Haşiye)", "parent_id": None,
         "ref": "Sözler › Birinci Söz › ¶1", "page_start": 5, "page_end": 6},
        {"id": "sozler/1/p001/h1", "node_id": "sozler/1", "kind": "hasiye", "seq": None,
         "text": "Hâşiye metni", "parent_id": "sozler/1/p001", "label": "Haşiye",
         "ref": "Sözler › Birinci Söz › ¶1 › Hâşiye", "page_start": 6, "page_end": 6},
    ],
}


def test_slim_drops_page_fields():
    data = slim(SAMPLE)
    for record in data["outline"] + data["passages"]:
        assert not any(key.startswith("page") for key in record)
    assert data["passages"][1]["label"] == "Haşiye"


def test_embedded_json_cannot_close_script_tag():
    embedded = embed_json(slim(SAMPLE))
    assert "</script>" not in embedded
    assert json.loads(embedded)["passages"][0]["text"].startswith("Metin </script>")


def test_render_is_self_contained():
    html = render(SAMPLE)
    for marker in ("/*__STYLE__*/", "/*__SCRIPT__*/", "__DATA__"):
        assert marker not in html
    assert "page_start" not in html and "page_end" not in html
    assert '<script id="data" type="application/json">' in html
