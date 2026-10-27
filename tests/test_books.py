"""Aşama 2: eser modeli ve erisale ayrıştırıcısı.

Ayrıştırıcı testleri elle kurulmuş küçük blok listeleriyle çalışır. En sondaki yapı
testleri `data/books/sozler.json` dosyasını kullanır; dosya yoksa atlanır
(önce `uv run python -m risale_mcp.build sozler` çalıştırın).
"""

import json

import pytest

from risale_mcp.books.erisale import parse_work
from risale_mcp.books.model import ArabicSpan, Text, TextBuilder
from risale_mcp.catalog import Group, Site, SourceRef, Work
from risale_mcp.paths import BOOKS_DIR
from risale_mcp.sources.erisale import BookBlocks, PageSummary

WORK = Work("kitap", "Kitap", Group.ANA_CILT, SourceRef(Site.ERISALE, "kitap"))


# ---------------------------------------------------------------- blok kurucular

def text(value: str, **extra) -> dict:
    return {"type": "Text", "value": value, **extra}


def regular(value: str) -> dict:
    return {"type": "Regular", "children": [text(value)]}


def meta(value: str) -> dict:
    return {"type": "Meta", "children": [text(value)]}


def heading(value: str) -> dict:
    return {"type": "Heading", "children": [text(value)]}


def arabic(value: str, id_: int = 1, kind: str = "ayet") -> dict:
    return {"type": "RTL", "children": [text(value, rtl={"id": id_, "type": kind, "txn": "meal", "ref": "Fâtiha Sûresi, 1:1"})]}


def footnote(*blocks: dict) -> dict:
    return {"type": "FootnoteRef", "children": [text("Hâşiye")],
            "footnote": {"type": "Footnote", "blocks": list(blocks)}}


def parse(*contents: tuple[str, list], missing: tuple[int, ...] = (), first: int = 1):
    blocks, index = [], first
    for kind, children in contents:
        while index in missing:
            index += 1
        blocks.append({"index": index, "section": 0, "page": "bolum", "content": {"type": kind, "children": children}})
        index += 1
    source = BookBlocks("kitap", pages=[PageSummary("bolum", "https://x/bolum", [], first, index)],
                        blocks=blocks, first_index=first, missing=list(missing))
    return parse_work(WORK, source)


def outline(book) -> dict:
    return {n["id"]: n for n in book.to_json()["outline"]}


# ---------------------------------------------------------------- metin modeli

def test_text_builder_collapses_spaces_and_tracks_positions():
    b = TextBuilder()
    b.add("Bu dünya ")
    b.add(" بسم", ArabicSpan(0, 0, "ayet"), key=1)
    b.add(" الله", ArabicSpan(0, 0, "ayet"), key=1)   # aynı parçanın devamı
    b.add(" fânîdir. ")
    b.mark_footnote("içerik")
    b.add(" Son. ")
    t = Text.from_builder(b)
    assert t.text == "Bu dünya بسم الله fânîdir. Son."
    assert [t.text[a.start:a.end] for a in t.arabic] == ["بسم الله"]
    assert t.text[: t.footnotes[0].offset].endswith("fânîdir.")


def test_is_arabic_counts_symbols():
    t = Text("﷽", [ArabicSpan(0, 1, "ayet")])
    assert t.is_arabic()
    assert not Text("Bismillah", []).is_arabic()


def test_join_shifts_positions():
    joined = Text.join([Text("ab", [ArabicSpan(0, 2, "arabi")]), Text("cd", [ArabicSpan(1, 2, "arabi")])], "\n")
    assert joined.text == "ab\ncd"
    assert [(a.start, a.end) for a in joined.arabic] == [(0, 2), (4, 5)]


# ---------------------------------------------------------------- ayrıştırıcı

def test_tree_from_heading_levels_and_directives():
    book, report = parse(
        ("H1", [regular("Birinci Söz"), meta("TocOnly=")]),
        ("Paragraph", [regular("Giriş.")]),
        ("H1", [regular("Birinci Söz"), meta("BookOnly=")]),      # aynı düğümün basılı başlığı
        ("Paragraph", [regular("Metin.")]),
        ("H2", [regular("On iki Hakikat"), meta("TocOnly=")]),
        ("H3", [regular("Birinci Hakikat")]),
        ("HeadingDescription", [regular("Bâb-ı Rubûbiyet.")]),
        ("Paragraph", [heading("Birinci Esas:"), regular(" Anlarsın ki.")]),
        ("Paragraph", [heading("İkinci Esas:"), regular(" Hem anlarsın.")]),
        ("Paragraph", [regular("Esasın devamı.")]),
        ("H3", [regular("İkinci Hakikat")]),
        ("Paragraph", [regular("Hiç mümkün müdür ki?")]),
        ("H1", [regular("Onuncu Söz"), heading("Haşir Bahsi"), meta("TocTitle=Onuncu Söz (Haşir Bahsi)")]),
    )
    nodes = outline(book)
    assert list(nodes) == [
        "kitap", "kitap/1", "kitap/1/on-iki-hakikat", "kitap/1/on-iki-hakikat/hakikat-01",
        "kitap/1/on-iki-hakikat/hakikat-01/esas-01", "kitap/1/on-iki-hakikat/hakikat-01/esas-02",
        "kitap/1/on-iki-hakikat/hakikat-02", "kitap/10",
    ]
    hakikat = nodes["kitap/1/on-iki-hakikat/hakikat-01"]
    assert hakikat["ref"] == "Kitap › Birinci Söz › On iki Hakikat › Birinci Hakikat"
    assert (hakikat["type"], hakikat["number"], hakikat["subtitle"]) == ("Hakikat", 1, "Bâb-ı Rubûbiyet.")
    assert nodes["kitap/10"]["subtitle"] == "Haşir Bahsi"
    assert nodes["kitap/10"]["toc_title"] == "Onuncu Söz (Haşir Bahsi)"
    assert nodes["kitap/1/on-iki-hakikat/hakikat-01/esas-01"]["heading"] == "inline"

    by_node = {}
    for p in book.paragraphs:
        by_node.setdefault(p["node_id"], []).append(p["text"])
    assert by_node["kitap/1"] == ["Giriş.", "Metin."]          # BookOnly yeni düğüm açmadı
    assert by_node["kitap/1/on-iki-hakikat/hakikat-01/esas-02"] == ["İkinci Esas: Hem anlarsın.", "Esasın devamı."]
    assert not report.unmatched_book_only


def test_leading_number_is_dropped_unless_it_numbers_the_verse():
    """Lâhika mektuplarının sıra numarası başlıktan atılır; "6. Âyetin Tefsiri"nde numara başlığın kendisidir."""
    book = parse(("H1", [regular("1. Zaman cemaat zamanıdır")]), ("Paragraph", [regular("Metin.")]),
                 ("H1", [regular("6. Âyetin Tefsiri")]), ("Paragraph", [regular("Metin.")]),
                 ("H1", [regular("9‑10. Âyetlerin Tefsiri")]), ("Paragraph", [regular("Metin.")]))
    titles = [n["title"] for n in book[0].to_json()["outline"][1:]]
    assert titles == ["Zaman cemaat zamanıdır", "6. Âyetin Tefsiri", "9‑10. Âyetlerin Tefsiri"]


def test_single_top_heading_is_the_work_itself():
    book, _ = parse(
        ("H1", [regular("Münâzarât"), meta("TocOnly=")]),
        ("H1", [regular("Münâzarât"), meta("BookOnly=")]),
        ("Paragraph", [regular("Önsöz.")]),
        ("H2", [regular("Mukaddime")]),
        ("Paragraph", [regular("Metin.")]),
    )
    nodes = outline(book)
    assert list(nodes) == ["kitap", "kitap/mukaddime"]
    assert nodes["kitap"]["title"] == "Kitap"                   # kök katalogdaki adıyla anılır
    assert book.paragraphs[0]["node_id"] == "kitap"


def test_inline_arabic_and_hasiye():
    book, _ = parse(
        ("H1", [regular("Birinci Söz")]),
        ("Paragraph", [regular("Bu dünya "), arabic("بسم"), regular(" fânîdir."),
                       footnote({"type": "Paragraph", "children": [
                           {"type": "FootnoteRef", "children": [text("Hâşiye")]}, regular(" Hâşiye metni.")]}),
                       regular(" Son.")]),
        ("CenteredParagraph", [arabic("﷽", id_=2)]),
        ("H1", [regular("İkinci Söz")]),
    )
    main, hasiye, besmele = book.paragraphs
    assert main["text"] == "Bu dünya بسم fânîdir. Son."
    assert main["arabic"] == [{"start": 9, "end": 12, "kind": "ayet", "meal": "meal", "source": "Fâtiha Sûresi, 1:1"}]
    assert hasiye["kind"] == "hasiye" and hasiye["parent_id"] == main["id"] and hasiye["id"] == f"{main['id']}/h1"
    assert hasiye["text"] == "Hâşiye metni."
    assert main["text"][: hasiye["offset"]].endswith("fânîdir.")
    assert besmele["kind"] == "arabic"


def test_arabic_without_meal_and_adjacent_arabic():
    plain = {"type": "RTL", "children": [text("بِاسْمِهِ")]}                  # erisale meal vermemiş
    book, _ = parse(
        ("H1", [regular("Birinci Söz")]),
        ("CenteredParagraph", [plain]),
        ("Paragraph", [{"type": "Mark", "children": [text("[4]")]}, arabic("فَهَذَا", id_=3),
                       arabic("حَسْبُنَا", id_=4), regular(" son.")]),
    )
    bismihi, paragraph = book.paragraphs
    assert bismihi["kind"] == "arabic" and bismihi["arabic"] == [{"start": 0, "end": 9, "kind": "arabi"}]
    assert paragraph["text"] == "[4]فَهَذَا حَسْبُنَا son."                     # art arda iki parça: araya boşluk
    assert [paragraph["text"][a["start"]:a["end"]] for a in paragraph["arabic"]] == ["فَهَذَا", "حَسْبُنَا"]


def test_text_builder_drops_bom_and_spans_without_arabic():
    builder = TextBuilder()
    builder.add("\ufeffSaîdü’n-Nûrsî", ArabicSpan(0, 0, "arabi"), key=1)       # kaynakta yanlış işaretli imza
    builder.add(" ", None)
    builder.add("بِسْمِ", ArabicSpan(0, 0, "ayet"), key=2)
    text = Text.from_builder(builder)
    assert text.text == "Saîdü’n-Nûrsî بِسْمِ"
    assert [(a.start, a.kind) for a in text.arabic] == [(14, "ayet")]


def test_poem_lines_until_break_form_one_paragraph():
    book, _ = parse(
        ("H1", [regular("Birinci Söz")]),
        ("Poem", [regular("Bırak bîçâre feryâdı,")]),
        ("Poem", [regular("belâdan gel tevekkül kıl.")]),
        ("PoemBreak", [regular(".")]),
        ("Poem", [regular("Tevekkül kıl.")]),
        ("H1", [regular("İkinci Söz")]),
    )
    assert [(p["kind"], p["text"]) for p in book.paragraphs] == [
        ("poem", "Bırak bîçâre feryâdı,\nbelâdan gel tevekkül kıl."), ("poem", "Tevekkül kıl.")]


def test_missing_blocks_and_editor_notes_are_recorded_not_invented():
    book, _ = parse(
        ("H1", [regular("Birinci Söz")]),
        ("Paragraph", [regular("Önce.")]),
        ("Comment", [regular("işittiğim anlar > işittiğim ânlar")]),
        ("Paragraph", [regular("Sonra.")]),
        ("H1", [regular("İkinci Söz")]),
        missing=(4, 5),
    )
    assert [p["text"] for p in book.paragraphs] == ["Önce.", "Sonra."]
    assert book.notes == [{"node_id": "kitap/1", "text": "işittiğim anlar > işittiğim ânlar", "after": "kitap/1/p001"}]
    assert book.gaps == [{"node_id": "kitap/1", "missing_blocks": 2, "after": "kitap/1/p001"}]


# ---------------------------------------------------------------- üretilmiş Sözler

@pytest.fixture(scope="module")
def sozler():
    path = BOOKS_DIR / "sozler.json"
    if not path.exists():
        pytest.skip("sozler.json yok; önce `uv run python -m risale_mcp.build sozler` çalıştırın")
    return json.loads(path.read_text(encoding="utf-8"))


def _children(book, parent_id):
    return [n for n in book["outline"] if n["parent_id"] == parent_id]


def test_all_33_soz_in_order(sozler):
    soz = [n for n in _children(sozler, "sozler") if n.get("type") == "Söz"]
    assert [n["number"] for n in soz] == list(range(1, 34))


def test_onuncu_soz_structure(sozler):
    hakikat = _children(sozler, "sozler/10/on-iki-hakikat")
    assert [n["number"] for n in hakikat] == list(range(1, 13))
    assert hakikat[8]["ref"] == "Sözler › Onuncu Söz › On iki Hakikat › Dokuzuncu Hakikat"
    esas = _children(sozler, "sozler/10/on-iki-hakikat/hakikat-06")
    assert [n["number"] for n in esas] == list(range(1, 10))
    six = {n["id"] for n in _children(sozler, "sozler/6")}
    assert {"sozler/6/kar-05", "sozler/6/hasaret-01"} <= six   # Kâr ve Hasaret serileri kardeş


def test_ids_unique_and_links_resolve(sozler):
    nodes = {n["id"] for n in sozler["outline"]}
    paragraphs = [p["id"] for p in sozler["paragraphs"]]
    assert len(nodes) == len(sozler["outline"]) and len(paragraphs) == len(set(paragraphs))
    targets = nodes | set(paragraphs)
    assert all(p["node_id"] in nodes for p in sozler["paragraphs"])
    assert all(p["parent_id"] in targets for p in sozler["paragraphs"] if p["kind"] == "hasiye")
    assert all(n["ref"].startswith("Sözler") for n in sozler["outline"])


def test_no_page_numbers_and_lemeat_separate(sozler):
    raw = json.dumps(sozler, ensure_ascii=False)
    assert "pageNumber" not in raw and "page_start" not in raw
    assert not any(n["id"].startswith("sozler/lemeat") for n in sozler["outline"])


def test_signature_parts_are_lines():
    book, _ = parse(
        ("H1", [regular("Birinci Söz")]),
        ("Signature", [regular("Umum Risale‑i Nur Şâkirdleri nâmına"), {"type": "Bold", "children": [text("Said Nursî")]}]),
        ("H1", [regular("İkinci Söz")]),
    )
    assert book.paragraphs[0]["text"] == "Umum Risale‑i Nur Şâkirdleri nâmına\nSaid Nursî"
