"""Denetim kaydı (`link_reviews.py`, H5): kayıt, geçerli karar, kurulum ve araç."""

import json
import shutil
import sqlite3

import pytest

from risale_mcp import link_reviews
from risale_mcp.build_db import build
from risale_mcp.library import Library
from risale_mcp.link_reviews import Review, current, validate

PEOPLE = {"a": {"name": "Denetçi A"}, "b": {"name": "Denetçi B"}}
KEY = {"source": "lemalar/1", "target": "quran:2:255", "type": "relation"}


def review(**kw) -> Review:
    return Review(**{"status": "reviewed", "reviewer": "a", "date": "2026-11-04", "link": KEY, "strength": "strong",
                     "file": "kuran/relation.jsonl", **kw})


@pytest.mark.parametrize("kw,problem", [
    ({"reviewer": "x"}, "denetçi"),                                  # listede olmayan denetçi
    ({"status": "accepted"}, "status"),
    ({"date": "dün"}, "date"),
    ({"status": "disputed"}, "gerekçe"),                             # itiraz gerekçesiz olmaz
    ({"match": {"node_prefix": "lemalar", "verse": "quran:2:255"}}, "link ya da match"),
    ({"link": {**KEY, "strength": "strong"}}, "link"),               # güç anahtarda değil
    ({"strength": "maybe"}, "strength"),
])
def test_record_problems(kw, problem):
    assert any(problem in p for p in review(**kw).problems(PEOPLE))


def test_current_keeps_the_last_word_of_each_reviewer_and_never_merges_reviewers():
    rows = [review(), review(strength="weak", date="2026-11-05"),                 # a fikrini değiştirdi
            review(reviewer="b", status="disputed", reason="bağ yok"),          # b itiraz etti: a'nınkini silmez
            review(link={**KEY, "source": "lemalar/2"}),
            review(link={**KEY, "source": "lemalar/2"}, status="withdrawn", date="2026-11-06")]
    live = current(rows)
    assert sorted((r.reviewer, r.status, r.strength) for r in live) == [("a", "reviewed", "weak"),
                                                                        ("b", "disputed", "strong")]
    assert validate(rows, PEOPLE) == []
    lonely = review(status="withdrawn")
    assert [p for _, p in validate([lonely], PEOPLE)] == ["geri çekilecek önceki karar yok"]


def test_append_only_adds_valid_lines(tmp_path, monkeypatch):
    (tmp_path / "reviewers.json").write_text(json.dumps({"reviewers": PEOPLE}), "utf-8")
    path = tmp_path / "kuran" / "relation.jsonl"
    link_reviews.append(path, review(), tmp_path)
    link_reviews.append(path, review(reviewer="b", status="disputed", reason="x"), tmp_path)
    with pytest.raises(ValueError):
        link_reviews.append(path, review(reviewer="z"), tmp_path)
    assert [r.reviewer for r in link_reviews.read(tmp_path)] == ["a", "b"]
    assert all(r.file == "kuran/relation.jsonl" for r in link_reviews.read(tmp_path))


@pytest.fixture(scope="module")
def reviewed_db(tmp_path_factory):
    """`test_ayah_links`'in küçük eserleri, kendi bağ klasörüyle: lemalar/1'in 2:255 ilişkisine iki karar."""
    from test_ayah_links import LETTERS, SECTIONS, WINDOWS, _book

    from conftest import mini_quran
    folder = tmp_path_factory.mktemp("reviewed")
    books = folder / "books"
    books.mkdir()
    for work, sections in (("lemalar", SECTIONS), ("mektubat", LETTERS), ("sozler", WINDOWS)):
        (books / f"{work}.json").write_text(json.dumps(_book(work, sections), ensure_ascii=False), "utf-8")
    quran = folder / "quran.json"
    quran.write_text(json.dumps(mini_quran(), ensure_ascii=False), "utf-8")
    reviews = folder / "links" / "reviews"
    (reviews / "kuran").mkdir(parents=True)
    (reviews / "reviewers.json").write_text(json.dumps({"reviewers": PEOPLE}), "utf-8")
    rows = [review(reason="metin söylüyor"), review(reviewer="b", status="disputed", reason="yalnız bir cümle"),
            review(link={**KEY, "source": "lemalar/99"})]                              # bağı yok: yüklenmez
    (reviews / "kuran" / "relation.jsonl").write_text(
        "".join(json.dumps(r.to_json(), ensure_ascii=False) + "\n" for r in rows), "utf-8")
    out = folder / "test.db"
    report = build(books, out, quran, links_dir=folder / "links")
    yield out, report, folder
    shutil.rmtree(folder)


def test_build_loads_current_reviews_that_meet_a_link(reviewed_db):
    out, report, _ = reviewed_db
    assert report.counts["link_reviews"] == 2 and report.counts["reviews_unmatched"] == 1
    rows = sqlite3.connect(out).execute("SELECT source, status, name FROM link_reviews ORDER BY name").fetchall()
    assert rows == [("lemalar/1", "reviewed", "Denetçi A"), ("lemalar/1", "disputed", "Denetçi B")]


def test_find_ayah_shows_who_checked_a_link(reviewed_db):
    lib = Library(reviewed_db[0])
    links = {l["section"]: l for l in lib.find_ayah("2", 255)["links"]}
    assert links["lemalar/1"]["reviews"] == [
        {"status": "reviewed", "strength": "strong", "by": "Denetçi A", "date": "2026-11-04", "reason": "metin söylüyor"},
        {"status": "disputed", "strength": "strong", "by": "Denetçi B", "date": "2026-11-04", "reason": "yalnız bir cümle"}]
    assert "reviews" not in links["lemalar/2"]                          # kimse bakmadı: alan yok
    lib.close()


def test_an_invalid_review_stops_the_build(reviewed_db, tmp_path):
    _, _, folder = reviewed_db
    links = tmp_path / "links"
    shutil.copytree(folder / "links" / "reviews", links / "reviews")
    with open(links / "reviews" / "kuran" / "relation.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(review(reviewer="kimse").to_json()) + "\n")
    with pytest.raises(ValueError, match="denetçi"):
        build(folder / "books", tmp_path / "x.db", folder / "quran.json", links_dir=links)
    assert not (tmp_path / "x.db").exists()


def test_the_real_reviews_are_valid():
    """data/links/reviews/ git'tedir: kayıtlar her zaman geçerli olmalı (veritabanı gerekmez)."""
    people, reviews = link_reviews.reviewers(), link_reviews.read()
    if not reviews:
        pytest.skip("karar yok")
    assert validate(reviews, people) == []
