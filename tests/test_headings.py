"""Başlıkların türü, numarası ve kimlikteki yerel adı."""

import pytest

from risale_mcp.headings import HeadingInfo, canonical_type, local_id, parse_heading, parse_inline_label


def test_canonical_type_strips_suffixes():
    assert canonical_type("Makamı") == "Makam"
    assert canonical_type("REŞHASI") == "Reşha"
    assert canonical_type("Hatveye") == "Hatve"
    assert canonical_type("Haşiyesidir") == "Hâşiye"
    assert canonical_type("Remzi") == "Remiz"       # ses düşmesi
    assert canonical_type("Suâliniz") == "Sual"
    assert canonical_type("Kitab") is None


@pytest.mark.parametrize("title,expected", [
    ("Dokuzuncu Hakikat", HeadingInfo("Hakikat", 9)),
    ("Zeylin İkinci Parçası", HeadingInfo("Parça", 2)),
    ("Ondördüncü Lem'a’nın İkinci Makamı", HeadingInfo("Makam", 2)),
    ("Otuzuncu Lem‘anın Beşinci Nüktesinin Dördüncü Remzi", HeadingInfo("Remiz", 4)),
    ("Yirmi Sekizinci Lem'a", HeadingInfo("Lem'a", 28)),
    ("Birinci Kelime: “El‑Emel”", HeadingInfo("Kelime", 1)),
    ("Ondördüncü Sözün Zeyli", HeadingInfo("Zeyl")),
    ("Hâtime", HeadingInfo("Hâtime")),
    ("297. Emirdağı’nın manidar bir hatırası", HeadingInfo(number=297)),
    # Tür yok: grup başlığı, sayısız başlık, cümle biçiminde mektup başlığı.
    ("On iki Hakikat", HeadingInfo()),
    ("Otuzüç Penceredir", HeadingInfo()),
    ("Yirmi Beşinci Söz, Kur’ân’ı çok güzel tarif eder", HeadingInfo()),
])
def test_parse_heading(title, expected):
    assert parse_heading(title) == expected


@pytest.mark.parametrize("label,expected", [
    ("Birinci Esâs:", HeadingInfo("Esas", 1)),
    ("Birinci Kâr:", HeadingInfo("Kâr", 1)),
    ("Üçüncü Mes'ele Ki:", HeadingInfo("Mes'ele", 3)),
    ("Birinci Hatvede:", HeadingInfo("Hatve", 1)),
    ("Birinci kısım", HeadingInfo("Kısım", 1)),
    ("On Birinci Esas:", HeadingInfo("Esas", 11)),
    ("Birincisi:", None),                          # sayı sıfatı
    ("Onuncu Söz’den", None),                      # kaynak etiketi
    ("İkinci kısmın", None),                       # ilgi hâli: cümlenin başı
    ("Birinci Vecih Âyinedârlık İse", None),       # etiket değil, cümle
])
def test_parse_inline_label(label, expected):
    assert parse_inline_label(label) == expected


def test_local_id():
    assert local_id(HeadingInfo("Söz", 10), "Onuncu Söz", top_level=True) == "10"
    assert local_id(HeadingInfo("Söz", 10), "Onuncu Söz", top_level=False) == "soz-10"
    assert local_id(HeadingInfo("Hakikat", 9), "Dokuzuncu Hakikat", top_level=False) == "hakikat-09"
    assert local_id(HeadingInfo("Hâtime"), "Hâtime", top_level=False) == "hatime"
    assert local_id(HeadingInfo(number=297), "Bir mektup", top_level=True) == "297"
    assert local_id(HeadingInfo(), "On iki Hakikat", top_level=False) == "on-iki-hakikat"
