"""Bağ kaydı (`links.py`): biçim, dosya, veritabanına karşı doğrulama. Küçük veritabanı `conftest.py`'dedir."""

import sqlite3

import pytest

from risale_mcp.links import TEXT_NAMESPACES, Link, check, files, local_id, part_key, read, read_meta, resolve, write

QUL = "قُلْ هُوَ اللّٰهُ اَحَدٌ"


def link(**kw) -> Link:
    base = {"source": "sozler/11/c001", "target": "quran:112:1", "type": "quote", "method": "source_mark"}
    return Link(**{**base, **kw})


@pytest.mark.parametrize("kw,problem", [
    ({"target": "quran:115:1"}, "target"),            # 114 sûre
    ({"target": "quran:2:7-5"}, "target"),            # aralık geriye
    ({"target": "hadis:Bukhari 52"}, "target"),
    ({"type": "tafsir"}, "type"),                     # "tefsir" bir bağ türü değildir (kullanıcının kararı)
    ({"method": "guess"}, "method"),
    ({"strength": "maybe"}, "strength"),
])
def test_record_problems(kw, problem):
    assert any(p.startswith(problem) for p in link(**kw).problems())


@pytest.mark.parametrize("target", ["quran:2:255", "quran:2:255-257", "hadis:bukhari/52", "hadis:muslim/8-2",
                                    "hadis-derlem:sanadset:220501", "hadis-derlem:tirmidhi:2780.2", "risale:lemalar/30"])
def test_valid_targets(target):
    kw = {"type": "reference", "relation": "old_name"} if target.startswith("risale:") else {}   # metne giden bağın türü
    assert link(target=target, **kw).problems() == []


@pytest.mark.parametrize("kw,ok", [
    ({"source": "risale:sozler/10/c001"}, True),                                # önekli kaynak (H4)
    ({"source": "sozler/10/c001..c004"}, True),                                 # aralık
    ({"source": "quran:2:255"}, False),                                         # Kur'ân bağın metin ucu olamaz
    ({"target": "risale:sozler/1/c004..c007", "relation": "same_words"}, True),  # metinden metne
    ({"target": "risale:sozler/1", "type": "relation", "relation": "objection"}, True),
    ({"target": "risale:sozler/1", "relation": "verbatim"}, False),             # metne giden alıntının türü
    ({"target": "risale:sozler/1", "type": "relation", "relation": "isaret"}, False),
    ({"target": "tefsir:beyzavi/1"}, False),                                    # koleksiyonu yok: ad alanı yok
])
def test_text_endpoints(kw, ok):
    assert (link(**kw).problems() == []) is ok


def test_namespaces_come_from_collections():
    assert TEXT_NAMESPACES == ("risale",)
    assert local_id("risale:sozler/10/c001") == "sozler/10/c001" == local_id("sozler/10/c001")
    assert local_id("quran:2:255") == "quran:2:255"
    assert link(source="risale:sozler/10/c001").key == link(source="sozler/10/c001").key


def test_write_and_read_keep_meta_order_and_drop_defaults(tmp_path):
    path = tmp_path / "kuran" / "quote.jsonl"
    rows = [link(source="sozler/11/c001"), link(source="sozler/10/c001", evidence={"check": "exact"}), link()]
    assert write(path, rows, producer="test", private=True) == 2               # aynı bağ bir kez
    meta, back = read(path)
    assert meta == {"producer": "test", "private": True, "count": 2} and read_meta(path) == meta
    assert [l.source for l in back] == ["sozler/10/c001", "sozler/11/c001"] and back[0].evidence == {"check": "exact"}
    assert "scope" not in path.read_text("utf-8").splitlines()[1]               # varsayılan yazılmaz
    assert files(tmp_path) == [path] and files(tmp_path, private=False) == []    # genel profil yerel dosyayı atlar


def test_write_refuses_an_invalid_link(tmp_path):
    with pytest.raises(ValueError):
        write(tmp_path / "x.jsonl", [link(target="quran:0:1")])


def test_check_against_the_database(small_db):
    conn = sqlite3.connect(small_db[0])
    good = link(part=part_key(QUL), display="Sözler › Onbirinci Söz › “قُلْ هُوَ اللّٰهُ…”")
    problems = check(conn, [
        good,
        link(source="sozler/99/c001"),                                         # cümle yok
        link(part="يوجد"),                                                      # parça o cümlede yok
        link(display="Sözler › Onbirinci Söz › “Başka bir cümle…”"),           # kimlik kaymış
        link(source="sozler/10", scope="section", type="relation", relation="acilis", method="rule"),
        link(target="risale:sozler/99", type="reference", relation="old_name", method="curated"),   # hedef yok
    ])
    assert {k: len(v) for k, v in problems.items()} == {"no_source": 1, "no_part": 1, "moved": 1, "no_target": 1}
    assert check(conn, [good]) == {}
    titled = link(display="Hutbe › İkinci Kelime: “Ye's” › “قُلْ هُوَ اللّٰهُ…”")       # başlıkta tırnak
    assert check(conn, [titled]) == {}


def test_text_to_text_links_against_the_database(small_db):
    """H4: iki uç da bir eserin cümlesi, aralığı ya da bölümü; önek eserin koleksiyonuyla tutmalı."""
    conn = sqlite3.connect(small_db[0])
    first, second = (r[0] for r in conn.execute("SELECT id FROM sentences WHERE node_id = 'sozler/10' ORDER BY seq LIMIT 2"))
    assert resolve(conn, f"risale:{first}..{second.rsplit('/', 1)[1]}")["kind"] == "range"
    assert resolve(conn, "risale:sozler/10")["kind"] == "section"
    assert resolve(conn, f"{second}..{first.rsplit('/', 1)[1]}") is None                  # geriye giden aralık
    assert resolve(conn, f"{first}..sozler/10/hakikat-01/c001") is None                    # bölümü aşan aralık
    text = {"type": "quote", "method": "scholar", "relation": "same_words"}
    problems = check(conn, [
        link(source=f"risale:{first}", target=f"risale:{second}", **text),
        link(source="sozler/11/c001", target=f"risale:{first}..{second}", **text),
        link(source="sozler/11/c001", target="risale:sozler/10/c999", **text),              # hedef cümle yok
        link(source="risale:sozler/10", scope="section", target="risale:sozler/11", type="relation",
             method="scholar", relation="same_view"),
    ])
    assert {k: len(v) for k, v in problems.items()} == {"no_target": 1}


def test_hadith_link_targets_round_trip_and_corpus_links():
    from risale_mcp.links_hadis import corpus_links, located_links, report_id, target
    for rid in ("tirmidhi:3839", "sanadset:220501", "tirmidhi:2780.2", "jk:bukhari/5764"):
        assert report_id(target(rid)) == rid
    assert target("jk:bukhari/5764") == "hadis:bukhari/5764"
    rows = [{"sentence_id": "a/c001", "hadith_key": "k1", "source": "Buharî, Ezân: 148", "display": "A › “x…”"}]
    parts = {"k1": {"match": "phrase_found", "reports": ["bukhari:1", "muslim:4927"], "total": 137,
                    "located": {"Buharî, Ezân: 148": {"level": "chapter", "reports": ["bukhari:6689"]}}}}
    corpus = corpus_links(rows, parts)
    assert [(l.target, l.relation, l.strength, l.evidence["rank"]) for l in corpus] == [
        ("hadis-derlem:bukhari:1", "phrase", "weak", 0), ("hadis-derlem:muslim:4927", "phrase", "weak", 1)]
    assert [(l.method, l.target) for l in located_links(rows, parts)] == [("cited_chapter", "hadis-derlem:bukhari:6689")]


def test_verse_links_and_old_names_are_computed_into_the_database(small_db):
    """Âyet bağları her kurulumda hesaplanır ve `links` tablosuna girer; eski adlar `old_names.json`'dan."""
    from risale_mcp.links_kuran import reference_links
    conn = sqlite3.connect(small_db[0])
    files = dict(conn.execute("SELECT file, count(*) FROM links GROUP BY file").fetchall())
    assert files.get("kuran/quote.jsonl", 0) >= 1
    row = conn.execute("SELECT source, target, method FROM links WHERE file = 'kuran/quote.jsonl' AND source = 'sozler/11/c001'").fetchone()
    assert row[1].startswith("quran:") and row[2] in ("source_mark", "quran_text")
    refs = {(l.source, l.target) for l in reference_links()}
    assert ("mektubat/31", "risale:lemalar") in refs and all(l.scope == "section" for l in reference_links())
