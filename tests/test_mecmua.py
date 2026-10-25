"""Mecmuaların ana ciltlere eşlenmesi."""

from risale_mcp.books.mecmua import CanonicalIndex, map_to_canonical
from risale_mcp.normalize import match_words

ONUNCU = "Hiç mümkün müdür ki şe'n-i Rubûbiyet ve saltanat-ı Ulûhiyet böyle bir kâinâtı kemâlâtını göstermek için yapsın"
DOKUZUNCU = "Evet şu âlemin Mutasarrıf-ı Hakîmi her mevsimde yeryüzünde otuz bin haşir ve kıyâmet nümûnelerini icâd ediyor"
ONUNCU_DEVAMI = "Ve hiç mümkün müdür ki o Zât-ı Kerîm ve Rahîm böyle bir misâfirhâneyi yapsın da dâimî bir saray yapmasın"


def canonical() -> CanonicalIndex:
    index = CanonicalIndex()
    index.add("sozler", {"paragraphs": [
        {"id": "sozler/10/p001", "node_id": "sozler/10", "kind": "paragraph", "text": ONUNCU},
        {"id": "sozler/10/p002", "node_id": "sozler/10", "kind": "arabic", "text": "﷽"},
        {"id": "sozler/10/p003", "node_id": "sozler/10", "kind": "paragraph", "text": DOKUZUNCU},
        {"id": "sozler/10/p004", "node_id": "sozler/10", "kind": "paragraph", "text": ONUNCU_DEVAMI},
    ]})
    return index


def test_match_words_ignores_edition_spelling():
    assert match_words("Risâle-i Nûr’un i‘tirâzlara gāib") == match_words("Risale-i Nur’un itirazlara gàib")
    assert match_words("عَلٰی") == match_words("عَلٰى")                      # Farsça ye / elif maksure


def test_mapping_replaces_text_with_source_and_keeps_unique():
    book = {
        "outline": [{"id": "m", "parent_id": None}, {"id": "m/soz-10", "parent_id": "m"}],
        "paragraphs": [
            {"id": "m/p001", "node_id": "m", "kind": "paragraph", "text": "Bu mecmûa Üç Makam ve Bir Hâtimedir."},
            {"id": "m/soz-10/p001", "node_id": "m/soz-10", "kind": "arabic", "text": "﷽"},
            # Hayrat baskısı iki paragrafı birleştirmiş ve yazımı farklı:
            {"id": "m/soz-10/p002", "node_id": "m/soz-10", "kind": "paragraph",
             "text": DOKUZUNCU.replace("âlem", "ālem") + " " + ONUNCU_DEVAMI.replace("Kerîm", "Kerim")},
        ],
    }
    report = map_to_canonical(book, canonical())
    by_id = {p["id"]: p for p in book["paragraphs"]}
    assert "text" in by_id["m/p001"] and report.unique == 1                 # mecmuaya özgü: metniyle kalır
    assert by_id["m/soz-10/p002"]["source"] == ["sozler/10/p003", "sozler/10/p004"]
    assert by_id["m/soz-10/p001"]["source"] == ["sozler/10/p002"]           # kısa: sonrakinden geriye bağlandı
    assert "text" not in by_id["m/soz-10/p002"]
    assert book["outline"][1]["sources"] == ["sozler/10"]
