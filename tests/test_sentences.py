"""Aşama 3: cümle bölücü ve altın örnekler.

Bölme kuralları değişirse numaralar kayar ve eski atıflar bozulur. Bu yüzden kurallar
burada örneklerle, Sözler'den seçilmiş düğümlerin cümleleri de `tests/golden/` altındaki
anlık görüntüyle kilitlenir. Kurallar bilerek değiştirildiyse görüntü şöyle yenilenir:
    uv run python -m risale_mcp.sentences --golden
"""

import json

import pytest

from risale_mcp.paths import BOOKS_DIR
from risale_mcp.sentences import GOLDEN_PATH, golden_snapshot, incipits, segment, split


def parts(text: str, arabic: list[dict] | None = None) -> list[str]:
    return [text[s:e] for s, e in split(text, arabic)]


@pytest.mark.parametrize("text,expected", [
    # Soru ve ünlemden sonra büyük harf: yeni cümle.
    ("Öyle mi? Evet, nasıl ki görsen; bir tek adam geldi.",
     ["Öyle mi?", "Evet, nasıl ki görsen; bir tek adam geldi."]),
    # ";" ve ":" bölmez.
    ("Hiç mümkün müdür ki; şu kâinât kendi kendine olsun. Elcevab: Evet, olamaz.",
     ["Hiç mümkün müdür ki; şu kâinât kendi kendine olsun.", "Elcevab: Evet, olamaz."]),
    # Kapanış tırnağı cümleye dahildir; tırnak içindeki ünlem küçük harfle sürerse bölmez.
    ("Başta demiştik: “Bütün mevcûdât ‘Bismillâh’ der.” Öyle mi?",
     ["Başta demiştik: “Bütün mevcûdât ‘Bismillâh’ der.”", "Öyle mi?"]),
    ("“Ey insan!” dediğim vakit, nefsimi murad ediyorum.", ["“Ey insan!” dediğim vakit, nefsimi murad ediyorum."]),
    # Açılış tırnağı yeni cümle başlatır.
    ("Biri sana dese. “Kaldırmaz” desen.", ["Biri sana dese.", "“Kaldırmaz” desen."]),
    # Kısaltma ve baş harf.
    ("Ankara’ya dâvet ederler. M. Kemâl Paşa çağırır. Hz. Üstadımız gördü. Dr. Rehber geldi.",
     ["Ankara’ya dâvet ederler.", "M. Kemâl Paşa çağırır.", "Hz. Üstadımız gördü.", "Dr. Rehber geldi."]),
    ("Bu (İ.G.Z.) milletinin ihtirasıdır. Talebeniz H. S. Bey geldi.",
     ["Bu (İ.G.Z.) milletinin ihtirasıdır.", "Talebeniz H. S. Bey geldi."]),
    # Madde numarası: önceki cümle biter, numaradan sonra bölünmez.
    ("Şunlardır: 1. Ya müellifînin hatâsı. 2. Yâhut tedrîcî bir değişiklik.",
     ["Şunlardır: 1. Ya müellifînin hatâsı.", "2. Yâhut tedrîcî bir değişiklik."]),
    # "‥" ve "…": küçük harf gelirse sürer, büyük harf gelirse biter.
    ("Dünya kendi için değil‥ kendi kendine de olmaz. Hâşâ!‥ Sonra bak… Ve hâkezâ…",
     ["Dünya kendi için değil‥ kendi kendine de olmaz.", "Hâşâ!‥", "Sonra bak…", "Ve hâkezâ…"]),
])
def test_split(text, expected):
    assert parts(text) == expected


def test_arabic_after_full_stop_starts_a_sentence_and_is_never_split():
    text = "Bir ihtarla gördüm. اَيُحِبُّ. اَحَدُكُمْ âyeti der ki: Gıybet etme."
    start = text.index("ا")
    arabic = [{"start": start, "end": text.index(" âyeti")}]
    assert parts(text, arabic) == ["Bir ihtarla gördüm.", "اَيُحِبُّ. اَحَدُكُمْ âyeti der ki: Gıybet etme."]


def test_incipit_is_shortest_unique_prefix_of_at_least_four_words():
    texts = ["Ey insan! Eğer insan isen, de.", "Ey insan! Eğer insan isen, bil.", "Bak!", "Evet, bu kelime ile hareket eden adam."]
    assert incipits(texts) == ["Ey insan! Eğer insan isen, de.", "Ey insan! Eğer insan isen, bil.",
                               "Bak!", "Evet, bu kelime ile"]


def test_segment_numbers_per_node_and_anchors_hasiye():
    book = {
        "outline": [{"id": "k", "ref": "Kitap"}, {"id": "k/1", "ref": "Kitap › Birinci Söz"}],
        "paragraphs": [
            {"id": "k/1/p001", "node_id": "k/1", "kind": "paragraph", "text": "Bir cümle. İkinci cümle bitti."},
            {"id": "k/1/p001/h1", "node_id": "k/1", "kind": "hasiye", "parent_id": "k/1/p001",
             "offset": 29, "text": "Hâşiye bir. Hâşiye iki."},
            {"id": "k/1/p002", "node_id": "k/1", "kind": "arabic", "text": "بسم الله. الرحمن"},
        ],
    }
    by_id = {s["id"]: s for s in segment(book)}
    assert list(by_id) == ["k/1/c001", "k/1/c002", "k/1/c002/h1/c001", "k/1/c002/h1/c002", "k/1/c003"]
    assert by_id["k/1/c002/h1/c002"]["ref"] == "Kitap › Birinci Söz › 2. cümle › Hâşiye › 2. cümle"
    assert book["paragraphs"][1]["anchor"] == "k/1/c002"
    assert by_id["k/1/c003"]["text"] == "بسم الله. الرحمن"            # tamamen Arapça: tek cümle


@pytest.fixture(scope="module")
def sozler():
    path = BOOKS_DIR / "sozler.json"
    if not path.exists():
        pytest.skip("sozler.json yok; önce `uv run python -m risale_mcp.build sozler` çalıştırın")
    return json.loads(path.read_text(encoding="utf-8"))


def test_golden_sentences_of_sozler(sozler):
    expected = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    assert golden_snapshot(sozler) == expected


def test_every_sentence_is_an_exact_slice_of_its_paragraph(sozler):
    paragraphs = {p["id"]: p for p in sozler["paragraphs"]}
    for s in sozler["sentences"]:
        assert paragraphs[s["paragraph_id"]]["text"][s["start"]:s["end"]] == s["text"]
    assert len({s["id"] for s in sozler["sentences"]}) == len(sozler["sentences"])


def test_numbered_translation_line_starts_a_sentence():
    text = "Devam eder.\n[6]O Sâni' ki, Fâtır-ı Bâkî'dir."
    assert [text[s:e] for s, e in split(text)] == ["Devam eder.", "[6]O Sâni' ki, Fâtır-ı Bâkî'dir."]
