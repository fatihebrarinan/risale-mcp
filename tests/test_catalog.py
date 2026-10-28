"""Eser kataloğunun tutarlılık testleri."""

import re

import pytest

from risale_mcp.catalog import WORKS, Site, SourceRef, Status, get_work, works_from


def test_slugs_are_unique_and_url_safe():
    slugs = [w.slug for w in WORKS]
    assert len(slugs) == len(set(slugs))
    assert all(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", s) for s in slugs)


def test_every_listed_work_is_present():
    # Kullanıcının listesindeki 42 madde; aslı Arapça eserlerin (Mesnevî, İşaratü'l-İ'caz, Kızıl İcaz, Ta'likat)
    # Arapçası ve Türkçesi ayrı eser; Hutbe-i Şamiye'nin Arapçası da (İhsan Kasım tercümesi) ayrı eser.
    assert len(WORKS) == 47


def test_missing_works_have_no_source_and_others_do():
    for work in WORKS:
        assert (work.source is None) == (work.status is Status.MISSING), work.slug


def test_section_selectors():
    whole = SourceRef(Site.ERISALE, "sozler", exclude=("lemeat",))
    assert whole.includes("onuncu-soz-hasir-bahsi")
    assert not whole.includes("lemeat")
    assert not whole.includes("lemeat-tenbih")

    part = SourceRef(Site.ERISALE, "ilk-donem-eserleri", ("isarat",))
    assert part.includes("isarat")
    assert part.includes("isarat-aşura")
    assert not part.includes("isaratul-icaz")  # önek kelime sınırında eşleşir


def test_shared_source_books_do_not_overlap():
    """Aynı kaynak kitabını paylaşan eserler aynı bölümü iki kez sahiplenmemeli."""
    sozler, lemeat = get_work("sozler"), get_work("lemeat")
    assert {w.slug for w in works_from(Site.ERISALE, "sozler")} == {"sozler", "lemeat"}
    for section in ("lemeat", "lemeat-tenbih", "birinci-soz", "fihrist"):
        assert sozler.source.includes(section) != lemeat.source.includes(section)


def test_unknown_work_raises():
    with pytest.raises(KeyError):
        get_work("yok-boyle-eser")
