"""Rumuzat-ı Semaniye: PDF'in Arapçasını glif kimliklerinden çözme, satırların mantıksal sırası, etiketler,
ve (kullanıcının PDF'i diskteyse) gerçek eser."""

import json
import unicodedata

import pytest

from risale_mcp.books.pdf_text import Glyph, Report, _letter, _logical
from risale_mcp.books.rumuzat import label_info
from risale_mcp.catalog import get_work
from risale_mcp.headings import HeadingInfo
from risale_mcp.paths import BOOKS_DIR, RAW_DIR
from risale_mcp.sources.kullanici import pdf_path

PDF = pdf_path(RAW_DIR / "kullanici", "rumuzat-i-semaniye")


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)        # şedde ile harekenin sırası yazana göre değişir


def glyph(kind: str, value: str, y: float = 100.0, ink_y: float = 100.0) -> Glyph:
    return Glyph(kind, value, 0, y, 8, 16, False, 0, 0, (0, ink_y))


@pytest.mark.parametrize("dots, letter", [
    ([("1", 104)], "ب"), ([("2", 88)], "ت"), ([("3", 88)], "ث"), ([("1", 88)], "ن"), ([("2", 104)], "ي"), ([], "ى"),
])
def test_dotless_body_and_dots_make_a_letter(dots, letter):
    base = glyph("S", "beh")
    base.marks = [glyph("D", n, ink_y=y) for n, y in dots] + [glyph("M", "َ")]
    assert _letter(base, Report()) == letter + "َ"


def test_qaf_and_feh_share_a_body():
    base = glyph("S", "qaf")
    base.marks = [glyph("D", "2", ink_y=88)]
    assert _letter(base, Report()) == "ق"


def test_unknown_combination_is_reported():
    report = Report()
    base = glyph("S", "noon")
    base.marks = [glyph("D", "2", ink_y=104)]
    assert _letter(base, report) == "ں" and report.unresolved == ["noon+b2"]


def test_arabic_run_inside_turkish_line_is_reversed():
    # Görsel sıra (soldan sağa): "akıl anlasa " + "اللّٰه" + " " + "سبحان" + " kalb"
    cells = [(c, False) for c in "anlasa "] + [("ه", True), ("ل", True), ("ل", True), ("ا", True), (" ", False),
                                                ("ن", True), ("ا", True), ("ح", True), ("ب", True), ("س", True)]
    cells += [(c, False) for c in " kalb"]
    text, spans = _logical(cells, rtl=False)
    assert text == "anlasa سبحان الله kalb"
    assert [text[s:e] for s, e in spans] == ["سبحان الله"]


def test_digits_and_brackets_in_arabic_line():
    # "٢٥٥ (الم)": görselde rakam sağda; ayraçların glifi aynalanmıştır (soldaki kapanış "(" görünür)
    cells = [("(", False), ("م", True), ("ل", True), ("ا", True), (")", False), (" ", False),
             ("٢", True), ("٥", True), ("٥", True)]
    text, _ = _logical(cells, rtl=True)
    assert text == "٢٥٥ (الم)"


@pytest.mark.parametrize("label, strict, info", [
    ("Birinci Mes'ele", True, HeadingInfo("Mes'ele", 1)),
    ("Altıncı mesele", True, HeadingInfo("Mes'ele", 6)),
    ("Dördüncü Silsile-i", False, HeadingInfo("Silsile", 4)),
    ("İkinci Letafet", False, HeadingInfo("Letafet", 2)),
    ("Lafzullah’ın Üçüncü Nüktesi", False, HeadingInfo("Nükte", 3)),
    ("Sekizinci Kısmın Üçüncü Remzi", False, HeadingInfo("Remiz", 3)),
    ("Birinci sebeb", False, HeadingInfo("Sebeb", 1)),            # tür açmaz; OPENING_TYPES dışında
    ("Mühim bir mes’ele-i Kur’âniye", False, None),
    ("Tenbih", False, None),
])
def test_label_info(label, strict, info):
    assert label_info(label, strict) == info


needs_pdf = pytest.mark.skipif(not (PDF.exists() and (BOOKS_DIR / "rumuzat-i-semaniye.json").exists()),
                               reason="kullanıcının PDF'i ya da eser JSON'u yok")


@needs_pdf
def test_real_book():
    book = json.loads((BOOKS_DIR / "rumuzat-i-semaniye.json").read_text(encoding="utf-8"))
    ids = {n["id"].removeprefix("rumuzat-i-semaniye/") for n in book["outline"]}
    assert {"kisim-03/mesele-09", "kisim-04/nukte-02/silsile-08", "kisim-04/nukte-03/nukte-04",
            "kisim-08/remiz-01/remiz-05", "kisim-08/remiz-07/parca-03", "kisim-08/remiz-08"} <= ids
    first = book["paragraphs"][0]
    assert nfc(first["text"]) == nfc("بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّح۪يمِ") and first["kind"] == "arabic"
    hasiye = [p for p in book["paragraphs"] if p["kind"] == "hasiye"]
    assert len(hasiye) == 20
    assert hasiye[0]["text"].startswith("Tevafukat ise ittifaka işarettir.")
    assert "(Hâşiye" not in " ".join(p.get("text", "") for p in book["paragraphs"])
    # Üçüncü Kısım'ın Birinci Mes'elesi Mektubat'tadır: metni orada durur.
    assert book["paragraphs"][2]["source"][0] == "mektubat/29/kisim-03/mesele-01/p001"
    assert get_work("rumuzat-i-semaniye").source.site == "kullanici"
