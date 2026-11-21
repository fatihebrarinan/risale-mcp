"""Küçük açıkların kilitleri (2026-11-21): B4 mecmua eşlemesi, B8 Delâil'in dipnot işaretleri."""
import json

import pytest

from risale_mcp.books.klasik_openiti import _FOOTNOTE_MARK
from risale_mcp.paths import DATA_DIR


def test_footnote_marks_b8():
    assert _FOOTNOTE_MARK.sub("", "في المسئلة الأولى2، لأن") == "في المسئلة الأولى، لأن"
    assert _FOOTNOTE_MARK.sub("", 'دون أن يقال: "ابلعي ماءك"1، ثم') == 'دون أن يقال: "ابلعي ماءك"، ثم'
    for kept in ("[الأنبياء100 - 101]", "توفى سنة 471 ه", "[ص: 394، 395]"):
        assert _FOOTNOTE_MARK.sub("", kept) == kept


NUTUK = DATA_DIR / "library" / "risale" / "kulliyat" / "nutuk.json"


@pytest.mark.skipif(not NUTUK.exists(), reason="eser JSON'u yok")
def test_short_line_not_mapped_into_long_paragraph_b4():
    """Nutuk'ta "Birincisi"nin altındaki iki kelimelik satır Divan-ı Harb'in uzun "Yaşasın…" paragrafına bağlanmamalı."""
    paragraphs = {p["id"]: p for p in json.loads(NUTUK.read_text(encoding="utf-8"))["paragraphs"]}
    assert paragraphs["nutuk/nutuk-03/p020"].get("text") == "İttihad-ı millî..."
