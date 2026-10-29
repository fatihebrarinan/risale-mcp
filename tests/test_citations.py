"""Atıf denetimi (`citations.py`): `cite` aracı ve altın soru raporu bunu kullanır.

Kurallar `conftest.py`'deki küçük veritabanıyla sınanır. Son testler gerçek veritabanında, altın
soru cevaplarında görülen yazılışlarla denenir; veritabanı yoksa atlanır.
"""

import pytest

from risale_mcp.citations import CitationChecker, summary
from risale_mcp.library import Library
from risale_mcp.paths import DB_PATH


@pytest.fixture
def checker(small_db):
    lib = Library(small_db[0])
    yield CitationChecker(lib)
    lib.close()


@pytest.mark.parametrize("line,status,exact", [
    ("Bkz. Sözler › Onuncu Söz › “Elbette haşr-i cismânî…”", "ok", True),
    ("**Onuncu Söz › Birinci Hakikat** › \"Kıyâmet ve mîzan\"", "ok", False),          # eser adı yazılmadan
    ("Sözler › Onuncu Söz › 2. cümle", "ok", True),
    ("Sözler › Onuncu Söz › 1. cümle › Hâşiye › 1. cümle", "ok", True),
    ("Sözler › Onuncu Söz › 1. cümle › Hâşiye › “Işık geldi.”", "ok", True),        # `cite`'ın hâşiye atfı
    ("Sözler › Onuncu Söz", "section", True),
    ("Bu konu Sözler › Onuncu Söz'de geçer.", "section", True),                       # ekli yazılış
    ("**Sözler › Onuncu Söz** bölümünde yer alıyor; \"Kıyâmet\" der.", "section", True),   # başlıktan sonra düz yazı
    ("Sözler › “Onuncu Söz”", "section", True),                                         # tırnak içinde başlık
    ("Sözler › Onuncu Söz'ün Birinci Hakikati", "section", False),                      # tür ve numarayla
    ("Sözler › Birinci Hakikat › “Kıyâmet ve mîzan”", "ok", False),                     # ara başlık atlanmış
    ("Giriş: Sözler › Onuncu Söz › \"Elbette 'haşr-i' cismânî\" ve \"başka\"", "ok", True),   # iki alıntı, iç tırnak
    ("(Sözler › Onuncu Söz › \"haşr-i cismânî olacak\")", "mid_sentence", True),        # cümle başı değil
    ("Sözler › Onuncu Söz › “Işık geldi.”", "ok", True),                                # hâşiye cümlesi
    ("Sözler › Onuncu Söz › “Elbette haşr-i … olacak.”", "ok", True),                   # "…" ile atlanan yer
    ("Sözler › Onuncu Söz › “Elbette haşr-i … uydurma söz.”", "quote_not_found", True),
    ("Asâ-yı Mûsâ › Haşir › “Bu mecmûa haşre”", "ok", True),
    ("Sözler › Onuncu Söz › On Beşinci Hakikat", "unknown_section", True),              # uydurma bölüm
    ("Sözler › Onuncu Söz › “Böyle bir cümle yok…”", "quote_not_found", True),
    ("Sözler › Onuncu Söz › 9. cümle", "no_such_sentence", True),
    ("Risâle-i Yok › Birinci Bab › “Elbette haşr-i”", "unknown_section", True),         # uydurma eser
])
def test_citation_status(checker, line, status, exact):
    (citation,) = checker.check(f"Metin şöyle der.\n{line}\n")
    assert (citation.status, citation.exact) == (status, exact)


def test_full_reference_is_offered_for_shortened_paths(checker):
    (citation,) = checker.check("Birinci Hakikat › “Kıyâmet ve mîzan”")
    assert citation.sentence == "sozler/10/hakikat-01/c001"
    assert citation.cite_as == "Sözler › Onuncu Söz › Birinci Hakikat › “Kıyâmet ve mîzan gün…”"   # incipit: ilk 20 harf
    assert "write the full path" in citation.problem()


def test_several_citations_on_one_line_and_prose_arrows(checker):
    found = checker.check("Önce Sözler › Onuncu Söz › “Elbette haşr-i” der, sonra Sözler › Onbirinci Söz gelir.\n"
                          "Sıra şöyle: giriş › gelişme › sonuç.")
    assert [(c.node, c.status) for c in found] == [("sozler/10", "ok"), ("sozler/11", "section")]


def test_relative_citations_follow_the_previous_one(checker):
    _, same, parent = checker.check("Sözler › Onuncu Söz › Birinci Hakikat › “Kıyâmet”\n"
                                    "> (… › “Kıyâmet ve mîzan günü”)\n"
                                    "aynı yer › Onuncu Söz › “Elbette haşr-i”")
    assert same.sentence == "sozler/10/hakikat-01/c001" and not same.exact
    assert parent.sentence == "sozler/10/c002"


def test_misplaced_quote_points_to_where_it_occurs(checker):
    (citation,) = checker.check("Sözler › Onbirinci Söz › “Elbette haşr-i cismânî”")
    assert citation.status == "quote_not_found"
    assert citation.elsewhere == [{"id": "sozler/10/c002", "cite_as": "Sözler › Onuncu Söz › “Elbette haşr-i cismâ…”"}]
    assert "occur at: Sözler › Onuncu Söz" in citation.problem()


def test_summary_counts_problems(checker):
    result = summary(checker.check("Sözler › Onuncu Söz › “Elbette haşr-i”\nSözler › Onuncu Söz › On Beşinci Hakikat"))
    assert (result["checked"], result["problems"]) == (2, 1)
    assert result["citations"][0] == {"citation": "Sözler › Onuncu Söz › “Elbette haşr-i”", "status": "ok",
                                      "sentence": "sozler/10/c002"}
    assert result["citations"][1]["problem"].startswith("No section “On Beşinci Hakikat” under Sözler › Onuncu Söz")


# ---------------------------------------------------------------- ardışık cümleler ve alıntı blokları

@pytest.mark.parametrize("line,status,covered", [
    ("Sözler › Onuncu Söz › “Bakara’da…” ile başlayan 2 cümle", "ok", 2),
    ("Sözler › Onuncu Söz › 1.–2. cümle", "ok", 2),
    ("Sözler › Onuncu Söz › “Bakara’da…” ile başlayan 3 cümle", "range_past_section", 2),   # bölümde iki cümle var
    ("Sözler › Onuncu Söz › “Bakara’da…” ile başlayan 9 cümle", "range_too_long", 2),
])
def test_ranges_of_consecutive_sentences(checker, line, status, covered):
    (citation,) = checker.check(line)
    assert (citation.status, citation.count > 1, len(citation.covered)) == (status, True, covered)


def test_range_reference_names_the_number_of_sentences(checker):
    (citation,) = checker.check("Sözler › Onuncu Söz › 1.–2. cümle")
    assert citation.cite_as.endswith("” ile başlayan 2 cümle") and citation.problem() is None
    (past,) = checker.check("Sözler › Onuncu Söz › “Bakara’da…” ile başlayan 3 cümle")
    assert "only 2 sentence(s)" in past.problem() and past.cite_as.endswith("ile başlayan 2 cümle")


@pytest.mark.parametrize("text,block_ok", [
    ("Sözler › Onuncu Söz › “Bakara’da…” ile başlayan 2 cümle\n\n> \"Bakara’da … denildi. Elbette haşr-i cismânî olacak.\"", True),
    ("> \"Elbette haşr-i cismânî olacak.\"\n\n(Sözler › Onuncu Söz › “Elbette haşr-i…”)", True),        # atıf altta
    ("Sözler › Onuncu Söz › “Elbette haşr-i…”\n\n> \"Elbette rûh bâkîdir.\"", False),                  # metinde yok
    ("Sözler › Onuncu Söz › “Elbette haşr-i…”\n\n> \"Bakara’da denildi.\"", False),                    # başka cümle
])
def test_block_quote_must_be_in_the_cited_sentences(checker, text, block_ok):
    (citation,) = checker.check(text)
    assert citation.block_ok is block_ok and citation.verified is block_ok
    assert (citation.problem() is None) is block_ok


def test_block_between_two_references_belongs_to_the_one_it_matches(checker):
    first, second = checker.check("Sözler › Onuncu Söz › “Elbette haşr-i…”\n\n> \"Elbette haşr-i cismânî olacak.\"\n\n"
                                  "Sözler › Onuncu Söz › Birinci Hakikat › “Kıyâmet…”\n\n> \"Kıyâmet ve mîzan günü gelecek.\"")
    assert (first.block_ok, second.block_ok) == (True, True)


def test_bibliography_entries_check_the_blocks_that_point_to_them(checker):
    """Kaynakçalı cevap: "[n]" ile biten alıntı bloğu kaynakçadaki n numaralı atfın cümlelerinde aranır."""
    found = checker.check("Haşir olacaktır.\n\n> \"Elbette haşr-i cismânî olacak.\" [2]\n\nAyrıca:\n\n"
                          "> \"Kıyâmet ve mîzan günü\" [1]\n\n> \"Uydurma söz.\" [1, 2]\n\n**Kaynaklar**\n"
                          "[1] Sözler › Onuncu Söz › Birinci Hakikat › “Kıyâmet ve mîzan”\n"
                          "[2] Sözler › Onuncu Söz › “Elbette haşr-i”\n")
    assert [(c.node, c.status, c.exact) for c in found] == [("sozler/10/hakikat-01", "ok", True), ("sozler/10", "ok", True)]
    assert [c.block_ok for c in found] == [False, False]           # son blok ikisinde de yok
    found = checker.check("> \"Kıyâmet ve mîzan günü\" [1]\n\n[1] Sözler › Onuncu Söz › Birinci Hakikat › “Kıyâmet”")
    assert found[0].block_ok is True


def test_real_bibliography_lines(real_checker):
    """Kaynakça numarası başlığa karışmaz ("[1] Lem'alar" Mesnevî'nin "1‑ Lem'alar" fihrist başlığı değildir);
    iç içe tırnaklı ilk kelimeler aralıkla birlikte okunur; aynı kelimelerle başlayan iki cümleden blok
    hangisindeyse atıf odur."""
    found = real_checker.check(
        "> \"İşte, “kadere ve kazâya îmân” rüknü dahi, geniş bir vecihte sırr‑ı hayatla anlaşılıyor\" [1]\n\n"
        "> \"Şimdi hiç mümkün müdür ki; böyle en küçük bir mahlûkun\" [2]\n\n"
        "[1] Lem'alar › Otuzuncu Lem'a › Otuzuncu Lem'anın Beşinci Nüktesi › Dördüncü Remiz › "
        "\"İşte, \"kadere ve kazâya…\" ile başlayan 2 cümle\n"
        "[2] Sözler › Onuncu Söz › On iki Hakikat › Üçüncü Hakikat › “Şimdi hiç mümkün müdür…”\n")
    assert [(c.status, c.exact, c.count, c.block_ok) for c in found] == [("ok", True, 2, True), ("ok", True, 1, True)]


def test_cite_returns_references_and_flags_problems(checker):
    result = checker.sources([
        {"id": "sozler/10/c001..c002", "quote": "Elbette haşr-i … olacak."},
        {"id": "sozler/10/c001/h1/c001"},
        {"id": "sozler/10/c002", "quote": "Kıyâmet ve mîzan"},
        {"id": "sozler/10/c001..sozler/10/hakikat-01/c001"},
        {"id": "sozler/10/c009"},
    ])
    ok, hasiye, misplaced, past, unknown = result["sources"]
    assert ok["status"] == "ok" and ok["cite_as"].endswith("ile başlayan 2 cümle")
    assert hasiye["status"] == "ok"
    assert "occur at: Sözler › Onuncu Söz › Birinci Hakikat" in misplaced["problem"]
    assert "stays inside one section" in past["problem"] and past["cite_as"].endswith("ile başlayan 2 cümle")
    assert unknown["status"] == "unknown_id"
    assert result["problems"] == 3
    assert result["bibliography"].splitlines()[1].startswith("[2] ")


# ---------------------------------------------------------------- gerçek veritabanı

@pytest.fixture
def real_checker():
    if not DB_PATH.exists():
        pytest.skip("risale.db yok; önce `uv run python -m risale_mcp.build_db` çalıştırın")
    lib = Library()
    yield CitationChecker(lib)
    lib.close()


@pytest.mark.parametrize("line,status,node", [
    # Toc adı: basılı başlık "Yirminci Söz’ün İkinci Makamı".
    ("Sözler › Yirminci Söz › İkinci Makam › Bir Nükte‑i Mühimme ve Bir Sırr-ı Ehemm", "section",
     "sozler/20/makam-02/bir-nukte-i-muhimme-ve-bir"),
    # Başlıktaki "(asm)" yazılmamış; ara başlık "…" ile atlanmış.
    ("Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye › Onyedinci İşâret", "section",
     "mektubat/19/mucizat-i-ahmediye-asm/isaret-17"),
    ("Mektubat › Ondokuzuncu Mektûb › … Onsekizinci İşâret", "section", "mektubat/19/mucizat-i-ahmediye-asm/isaret-18"),
    # "…" ile kısaltılmış uzun başlık.
    ("Şualar › Onüçüncü Şuâ › Ekser Beşer; Maddî ve Manevî… › \"Birden Hastalar Risalesi hâtıra geldi, tesellî verdi.\"",
     "ok", None),
    # Atıftan önce düz yazı, başlıkta ek.
    ("Bu temsil Sözler › Dördüncü Söz'de geçer.", "section", "sozler/4"),
    ("Bu kısım Mektubat › Yedinci Mektûb'dadır.", "section", "mektubat/7"),
    # Eser adı yazılmadan; tür ve numarayla.
    ("Lem'alar › Otuzuncu Lem'a › Beşinci Nükte › Dördüncü Remiz", "section", "lemalar/30/nukte-05/remiz-04"),
])
def test_real_spellings_from_golden_answers(real_checker, line, status, node):
    (citation,) = real_checker.check(line)
    assert citation.status == status
    assert node is None or citation.node == node


def test_real_relative_citations_resolve_in_context(real_checker):
    found = real_checker.check("Sözler › Yirmialtıncı Söz › Birinci Mebhas › \"Kader ve cüz'‑i ihtiyarî,…\"\n"
                               "> (Birinci Mebhas › \"Kader, nefsi gururdan…\")\n"
                               "> (İkinci Mebhas › \"Masdar kisbimizdir…\")")
    assert [c.sentence.rsplit("/", 1)[0] for c in found] == ["sozler/26/mebhas-01"] * 2 + ["sozler/26/mebhas-02"]
    assert all(c.status == "ok" for c in found)
