"""Klasik eserlerin ayrıştırma kuralları (E2.3, `books/klasik_openiti.py`): ham veri diskteyse gerçek metinle."""

import pytest

from risale_mcp.books import klasik_openiti
from risale_mcp.catalog import get_work
from risale_mcp.paths import RAW_DIR
from risale_mcp.sentences import split_paragraph

RAW = RAW_DIR / "openiti"


def _book(slug):
    if not (RAW / f"{slug}.txt").exists():
        pytest.skip("ham veri yok (uv run python -m risale_mcp.fetch klasik)")
    book, report = klasik_openiti.parse(get_work(slug))
    return book.to_json(), report


def test_verse_is_one_sentence():
    # mısraları ayıran "..." cümle sonu değildir
    para = {"kind": "poem", "verse": True, "text": "يا شبيه البدر في الحس ... ن وفي بعد المنال"}
    assert split_paragraph(para) == [(0, len(para["text"]))]
    assert klasik_openiti._is_verse(para["text"])
    assert not klasik_openiti._is_verse("هذا كلام طويل ... ثم يتم الكلام ويستمر حتى ينتهي.")


def test_heading_inside_text_goes_back_into_the_text():
    # Esrâr: metindeki "فصلا" kelimesinin "فصل"i başlık diye işaretlenmiş; kelime bölünmeden geri katılır
    book, report = _book("esrarul-belaga")
    texts = " ".join(p["text"] for p in book["paragraphs"])
    assert "لا تجد فصلا بين" in texts
    assert "</span>" not in texts
    assert any(n["title"] == "مقدمة المصنف" for n in book["outline"])


def test_miftah_preface_list_stays_text():
    # Miftâh: mukaddimedeki "القسم الأول في علم الصرف، القسم الثاني…" sayımı başlık değil, metin
    book, _ = _book("miftahul-ulum")
    assert any("القسم الأول في علم الصرف، القسم الثاني في علم النحو" in p["text"] for p in book["paragraphs"])


def test_delail_layers_and_fikra():
    book, report = _book("delailul-icaz")
    intro = next(n for n in book["outline"] if n["id"] == "delailul-icaz/mukaddime-tahkik")
    assert intro.get("authority") == "muhakkik" and intro.get("by") == "Mahmûd Muhammed Şâkir"
    assert next(n for n in book["outline"] if n["id"] == "delailul-icaz/1/f1")["title"] == "1"
    assert not any("الفهارس" == n["title"] for n in book["outline"])        # fihrist alınmaz
    assert report.fikra > 600


def test_mufredat_entries_from_roots():
    book, report = _book("mufredat")
    kitab = [n for n in book["outline"] if n.get("parent_id") == "mufredat" and n["id"] != "mufredat/mukaddime"]
    assert [n["title"] for n in kitab][-3:] == ["كتاب الواو", "كتاب الهاء", "كتاب الياء"]    # bu baskının sırası
    assert len(kitab) == 28 and report.entries == 1600
    first = next(n for n in book["outline"] if n["id"] == "mufredat/01/001")
    assert first["title"] == "أبا"
    texts = " ".join(p["text"] for p in book["paragraphs"])
    assert "= كتاب" not in texts and " | " not in texts


def test_no_unpaged_front_matter_page():
    book, _ = _book("delailul-icaz")
    assert not any(p.get("printed", {}).get("volume") == 0 for p in book["paragraphs"])
