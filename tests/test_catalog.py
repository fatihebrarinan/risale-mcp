"""Eser kataloğunun tutarlılık testleri."""

import re

import pytest

from risale_mcp.catalog import Collection, WORKS, Site, SourceRef, Status, get_work, works_from


def test_slugs_are_unique_and_url_safe():
    slugs = [w.slug for w in WORKS]
    assert len(slugs) == len(set(slugs))
    assert all(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", s) for s in slugs)


def test_every_listed_work_is_present():
    # Kullanıcının listesindeki 42 madde; aslı Arapça eserlerin (Mesnevî, İşaratü'l-İ'caz, Kızıl İcaz, Ta'likat)
    # Arapçası ve Türkçesi ayrı eser; Hutbe-i Şamiye'nin Arapçası da (İhsan Kasım tercümesi) ayrı eser.
    # 2026-10-30'da risaleoku.com'dan 11 eser, 16 Osmanlıca cilt ve harekeli Mesnevî eklendi. Kızıl İcaz'ın Türkçesi
    # 2026-11-12'de katalogdan çıktı (kullanıcının kararı: model tercümesi damgalı yeter).
    risale = [w for w in WORKS if w.collection not in (Collection.TEFSIR, Collection.KLASIK)]
    assert len(risale) == 73
    # Klasik eserlerin 1. dilimi (E2.2, 2026-11-13): beş belâgat ve terim eseri
    assert [w.slug for w in WORKS if w.collection is Collection.KLASIK] == [
        "delailul-icaz", "esrarul-belaga", "mufredat", "miftahul-ulum", "tarifat"]
    assert sum(w.group == "osmanlica" for w in WORKS) == 16
    # Müfessirlerin eserleri ayrı sayılır: MVP'nin 13 tefsiri (`docs/mvp-kitaplar.md`); genel çıkış kararına (M7)
    # kadar hepsi yalnız yerelde.
    assert {w.slug for w in WORKS if w.collection is Collection.TEFSIR} == {
        "beyzavi", "taberi", "maturidi", "kessaf", "razi", "kurtubi", "nesefi", "ibnkesir", "celaleyn", "durr",
        "ebussuud", "bursevi", "alusi"}
    assert all(w.private for w in WORKS if w.collection is Collection.TEFSIR)
    assert {w.slug for w in risale if w.private} == {"el-mesnevi-el-arabi-harekeli", "esasat-i-nuriye", "siracun-nur-hayrat",
                                                    "hizmet-rehberi-ve-dusturlari"}


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
