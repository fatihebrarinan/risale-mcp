"""Bağ kaydı (`links.py`): biçim, dosya, veritabanına karşı doğrulama. Küçük veritabanı `conftest.py`'dedir."""

import sqlite3

import pytest

from risale_mcp.links import Link, check, files, part_key, read, read_meta, write

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
                                    "hadis-derlem:sanadset:220501", "risale:lemalar/30"])
def test_valid_targets(target):
    assert link(target=target).problems() == []


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
        link(target="risale:sozler/99", type="reference", method="curated"),   # hedef bölüm yok
    ])
    assert {k: len(v) for k, v in problems.items()} == {"no_source": 1, "no_part": 1, "moved": 1, "no_target": 1}
    assert check(conn, [good]) == {}
