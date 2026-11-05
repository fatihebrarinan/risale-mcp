"""Denetim kaydı (`link_reviews.py`, H5): kayıt, geçerli karar, kurulum ve araç."""

import json
import shutil
import sqlite3

import pytest

from risale_mcp import link_reviews
from risale_mcp.build_db import build
from risale_mcp.library import Library
from risale_mcp.link_reviews import Review, current, validate

TERMS = {"version": 1, "date": "2026-11-01"}
PEOPLE = {"a": {"name": "Denetçi A", "number": 1, "terms": TERMS,
                "fields": {"kuran": {"since": "2026-11-01"}, "risale": {"since": "2026-11-01"}}},
          "b": {"name": "Denetçi B", "number": 2, "terms": TERMS, "fields": {"risale": {"since": "2026-11-01"}}}}
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
    ({"link": {"source": "beyzavi/1/1/c004", "target": "tefsir:kessaf/1/1/c002", "type": "quote"}}, "gerekçe"),
    ({"link": {"source": "isaratul-icaz/1/c003", "target": "tefsir:beyzavi/1/1", "type": "relation"}}, "gerekçe"),
])
def test_record_problems(kw, problem):
    assert any(problem in p for p in review(**kw).problems(PEOPLE))


def test_reason_is_required_only_between_texts():
    """Metinden metne lafız ve ilişki bağında gerekçe her kararda zorunlu; Kur'ân hedefinde ve göndermede değil."""
    text = {"source": "beyzavi/1/1/c004", "target": "tefsir:kessaf/1/1/c002", "type": "quote"}
    assert review(link=text, reason="aynı söz, Keşşâf'tan").problems(PEOPLE) == []
    assert review().problems(PEOPLE) == []                                          # âyet ilişkisi: gerekçesiz olur
    old_name = {"source": "lemalar/18", "target": "risale:sikke-i-tasdik-i-gaybi/lema-18", "type": "reference"}
    assert review(link=old_name).problems(PEOPLE) == []
    assert review(link=text, status="withdrawn").problems(PEOPLE) == []


def test_every_reviewer_has_a_fixed_number_of_their_own(tmp_path):
    (tmp_path / "reviewers.json").write_text(json.dumps({"reviewers": PEOPLE}), "utf-8")
    assert link_reviews.reviewers(tmp_path) == PEOPLE
    for people, problem in [({"a": {"name": "A"}}, "numarası yok"),
                            ({"a": {"number": 1}, "b": {"number": 1}}, "aynı numara")]:
        (tmp_path / "reviewers.json").write_text(json.dumps({"reviewers": people}), "utf-8")
        with pytest.raises(ValueError, match=problem):
            link_reviews.reviewers(tmp_path)


@pytest.mark.parametrize("type_,source,target,needs", [
    ("quote", "sozler/10/c001", "quran:2:255", ("kuran",)),                   # Kur'ân – Risale lafız
    ("relation", "sozler/10", "quran:2:255", ("kuran", "risale")),            # Kur'ân – Risale ilişki
    ("quote", "beyzavi/1/1/c001", "quran:1:1", ("kuran",)),                   # Kur'ân – tefsir lafız
    ("relation", "beyzavi/1/1", "quran:1:1", ("tefsir",)),                     # müfessirin âyet birimi
    ("quote", "sozler/10/c001", "hadis-derlem:bukhari:1", ("hadis",)),        # hadis – Risale
    ("quote", "beyzavi/1/1/c004", "hadis-derlem:sanadset:1", ("hadis",)),     # hadis – tefsir
    ("quote", "beyzavi/1/1/c004", "tefsir:kessaf/1/1/c002", ("tefsir",)),     # tefsir – tefsir lafız
    ("relation", "isaratul-icaz/1/c003", "tefsir:beyzavi/1/1", ("risale", "tefsir")),   # Risale – tefsir ilişki
    ("reference", "lemalar/18", "risale:sikke-i-tasdik-i-gaybi/lema-18", ("risale",)),  # Risale – Risale gönderme
    ("reference", "isaratul-icaz/1/c003", "tefsir:kessaf/1", ("risale", "tefsir")),     # müfessiri adıyla anma
])
def test_the_fields_a_link_needs_follow_its_kind_and_ends(type_, source, target, needs):
    namespace = "tefsir" if source.startswith(("beyzavi", "kessaf")) else "risale"
    got = link_reviews.needed_fields(type_, link_reviews.end_field(source, namespace), link_reviews.end_field(target))
    assert got == needs


def test_a_decision_counts_only_in_the_fields_held_on_its_date():
    person = {"fields": {"kuran": {"since": "2026-11-01"}, "hadis": {"since": "2026-11-10", "until": "2026-12-01"}}}
    assert link_reviews.fields_on(person, "2026-10-30") == set()
    assert link_reviews.fields_on(person, "2026-11-15") == {"kuran", "hadis"}
    assert link_reviews.fields_on(person, "2026-12-02") == {"kuran"}
    assert link_reviews.fields_on({**person, "until": "2026-11-05"}, "2026-11-06") == set()
    assert link_reviews.competence(review(date="2026-11-15"), person, ("kuran", "risale")) == ("kuran",)
    assert link_reviews.competence(review(date="2026-11-15"), {}, ("kuran",)) == ()      # alansız: competent false


def test_a_decision_needs_the_terms_accepted_before_it():
    """Katılım şartlarını kabul etmemiş denetçinin ya da kabulden önceki kararı geçersiz; proje sahibi hariç."""
    no_terms = {"a": {**PEOPLE["a"], "terms": None}}
    assert any("şartlarını kabul etmemiş" in p for p in review().problems(no_terms))
    assert any("kabulünden önce" in p for p in review(date="2026-10-30").problems(PEOPLE))
    owner = {"a": {**PEOPLE["a"], "terms": None, "owner": True}}
    assert review(date="2026-10-30").problems(owner) == []


def test_reviewer_fields_are_checked(tmp_path):
    for people, problem in [({"a": {"number": 1, "fields": {"arapca": {"since": "2026-11-01"}}}}, "bilinmeyen alan"),
                            ({"a": {"number": 1, "fields": {"kuran": {}}}}, "tarihi yok"),
                            ({"a": {"number": 1, "fields": {"kuran": {"since": "2026-11-01", "trial": "dün"}}}}, "geçersiz"),
                            ({"a": {"number": 1, "terms": {"version": 2, "date": "2026-11-01"}}}, "şartların kaydı")]:
        (tmp_path / "reviewers.json").write_text(json.dumps({"reviewers": people}), "utf-8")
        with pytest.raises(ValueError, match=problem):
            link_reviews.reviewers(tmp_path)


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
    rows = sqlite3.connect(out).execute("SELECT source, status, reviewer FROM link_reviews ORDER BY reviewer").fetchall()
    assert rows == [("lemalar/1", "reviewed", 1), ("lemalar/1", "disputed", 2)]       # ad veritabanına girmez
    assert not any("Denetçi" in str(v) for row in sqlite3.connect(out).execute("SELECT * FROM link_reviews") for v in row)


def test_find_ayah_shows_who_checked_a_link(reviewed_db):
    lib = Library(reviewed_db[0])
    links = {l["section"]: l for l in lib.find_ayah("2", 255)["links"]}
    assert links["lemalar/1"]["reviews"] == [
        {"status": "reviewed", "strength": "strong", "reviewer": 1, "fields": ["kuran", "risale"], "date": "2026-11-04",
         "reason": "metin söylüyor"},
        {"status": "disputed", "strength": "strong", "reviewer": 2, "fields": ["risale"], "date": "2026-11-04",
         "reason": "yalnız bir cümle"}]
    assert links["lemalar/1"]["review_fields"] == {"needs": ["kuran", "risale"], "covered": ["kuran", "risale"]}
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
