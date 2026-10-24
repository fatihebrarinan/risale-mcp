"""Aşama 2 testleri: yardımcı fonksiyonlar ve üretilmiş JSON üzerinde yapı kontrolleri.

Yapı testleri data/interim/sozler.json dosyasını kullanır; dosya yoksa atlanır
(önce `uv run python -m risale_mcp.parse` çalıştırın).
"""

import json
from pathlib import Path

import pytest

from risale_mcp.normalize import fold, ordinal_word, parse_ordinal, slugify, tr_lower, tr_title
from risale_mcp.parse import _parse_number_and_type, canonical_type, fix_letter_spacing

JSON_PATH = Path(__file__).resolve().parents[1] / "data" / "interim" / "sozler.json"


# ---------------------------------------------------------------- normalize

@pytest.mark.parametrize("word,n", [
    ("Birinci", 1), ("İKİNCİ", 2), ("Onuncu", 10), ("Onbirinci", 11), ("Yirminci", 20),
    ("YİRMİBEŞİNCİ", 25), ("Otuzüçüncü", 33), ("Onbesinci", 15), ("Kitab", None),
])
def test_parse_ordinal(word, n):
    assert parse_ordinal(word) == n


def test_ordinal_word_roundtrip():
    for n in range(1, 50):
        assert parse_ordinal(ordinal_word(n)) == n
    assert ordinal_word(2) == "İkinci"


def test_turkish_case():
    assert tr_lower("IŞIK İSLÂM") == "ışık islâm"
    assert tr_title("BİRİNCİ SIR") == "Birinci Sır"
    assert tr_title("ONDOKUZUNCU VE OTUZBİRİNCİ") == "Ondokuzuncu ve Otuzbirinci"


def test_fold_removes_only_circumflex():
    assert fold("Hâtime İSLÂM") == "hatime islam"
    assert fold("çğöşü") == "çğöşü"
    assert fold("Lem'a") == "lema"


def test_slugify():
    assert slugify("Hâtime") == "hatime"
    assert slugify("Mes'ele") == "mesele"


# ---------------------------------------------------------------- parse yardımcıları

def test_canonical_type_strips_suffixes():
    assert canonical_type("Makamı") == "Makam"
    assert canonical_type("REŞHASI") == "Reşha"
    assert canonical_type("Hatveye") == "Hatve"
    assert canonical_type("Haşiyesidir") == "Haşiye"


@pytest.mark.parametrize("text,expected", [
    ("Zeylin İkinci Parçası", (2, "Parça")),
    ("Onüçüncü Sözün İkinci Makamı", (2, "Makam")),
    ("Risale-i Nur Mizanlarından Onüçüncü Söz'ün İkinci Makamının Haşiyesidir", (None, "Haşiye")),
    ("Ondördüncü Sözün Zeyli", (None, "Zeyl")),
    ("Otuzüç Penceredir", (None, "")),
    ("Şeytanın İkinci Küçük Bir İtirazı", (None, "")),
    ("Do kuzuncu Şua", (9, "Şua")),
])
def test_parse_number_and_type(text, expected):
    assert _parse_number_and_type(text) == expected


def test_fix_letter_spacing():
    assert fix_letter_spacing("Do kuzuncu Şua") == "Dokuzuncu Şua"
    assert fix_letter_spacing("Birinci Söz") == "Birinci Söz"


# ---------------------------------------------------------------- üretilmiş JSON

@pytest.fixture(scope="module")
def data():
    if not JSON_PATH.exists():
        pytest.skip("sozler.json yok; önce parse çalıştırın")
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))


def _children(data, parent_id):
    return [o for o in data["outline"] if o["parent_id"] == parent_id]


def test_all_33_soz_present_in_order(data):
    soz = [o for o in data["outline"] if o["depth"] == 1 and o["type"] == "Söz"]
    assert [o["number"] for o in soz] == list(range(1, 34))


def test_onuncu_soz_has_twelve_hakikat(data):
    titles = [o["title"] for o in _children(data, "sozler/10")]
    hakikat = [t for t in titles if t.endswith("Hakikat")]
    assert hakikat == [f"{ordinal_word(n)} Hakikat" for n in range(1, 13)]
    assert "Mukaddime" in titles


def test_nested_series(data):
    # Altıncı Hakikat dokuz Esas içerir; Yedinci Hakikat yine Söz'ün çocuğudur.
    esas = _children(data, "sozler/10/hakikat-06")
    assert [o["number"] for o in esas] == list(range(1, 10))
    # Kâr ve Hasaret serileri art arda, kardeş.
    six = [o["id"] for o in _children(data, "sozler/6")]
    assert "sozler/6/kar-05" in six and "sozler/6/hasaret-01" in six


def test_ids_unique_and_refs_present(data):
    ids = [p["id"] for p in data["passages"]]
    assert len(ids) == len(set(ids))
    assert all(p["ref"].startswith("Sözler › ") for p in data["passages"])
    assert len({o["id"] for o in data["outline"]}) == len(data["outline"])


def test_example_address_from_claude_md(data):
    p = next(p for p in data["passages"] if p["id"] == "sozler/10/hakikat-09/p003")
    assert p["ref"] == "Sözler › Onuncu Söz › Dokuzuncu Hakikat › ¶3"


def test_no_markers_or_glyph_garbage(data):
    for p in data["passages"]:
        assert "sh:»" not in p["text"]
        assert not any(c in p["text"] for c in "\x01\x8d\x8e«×²¾ð"), p["id"]


def test_hasiye_linked(data):
    ids = {p["id"] for p in data["passages"]}
    hasiye = [p for p in data["passages"] if p["kind"] == "hasiye"]
    assert len(hasiye) >= 135
    assert all(h["parent_id"] in ids for h in hasiye)
    assert not any(h["parent_uncertain"] for h in hasiye)


def test_page_split_paragraph_joined(data):
    p = next(p for p in data["passages"] if "kereme lâyık ve o rahmete şayeste" in p["text"])
    assert (p["page_start"], p["page_end"]) == (64, 65)
