"""Eserin yazarı (H2), baskı kaydı ve izin kapısı (H3)."""

import json

import pytest

from risale_mcp.build_db import check_permissions
from risale_mcp.catalog import WORKS, Authority, Collection, Site, SourceRef, Work, get_work
from risale_mcp.catalog.editions import _risaleoku_catalog, edition
from risale_mcp.catalog.model import AUTHOR, Group
from risale_mcp.catalog.permissions import PERMISSIONS
from risale_mcp.profiles import GENEL, KISISEL


def test_every_sourced_work_has_a_known_permission():
    for work in WORKS:
        if work.source is not None:
            assert work.permission_key in PERMISSIONS, work.slug


def test_public_profile_holds_only_permitted_works_and_known_exceptions():
    exceptions = [w.slug for w in WORKS if GENEL.includes(w) and w.source
                  and not PERMISSIONS[w.permission_key].public]
    assert exceptions == []                     # Rumuzat 2026-11-04'te izinli kaynağa (nurpedia) geçti
    assert get_work("rumuzat-i-semaniye").permission_key == "nurpedia"
    assert not any(GENEL.includes(w) for w in WORKS if w.permission_key == "rasaelalnour")


def test_gate_stops_the_public_build_but_not_the_personal_one():
    work = Work("deneme", "Deneme", Group.MECMUA, SourceRef(Site.RISALE_ONLINE, "x"))
    with pytest.raises(RuntimeError, match="deneme: risale.online"):
        check_permissions([work], {"deneme"}, GENEL)
    assert check_permissions([work], {"deneme"}, KISISEL) == []
    assert check_permissions([work], set(), GENEL) == []          # kurulmayan eser denetlenmez
    allowed = Work("deneme", "Deneme", Group.MECMUA, SourceRef(Site.KULLANICI, "x"), public_without_record="karar bekleniyor")
    assert check_permissions([allowed], {"deneme"}, GENEL) == ["deneme: Kullanıcının dosyası (kayit-yok); karar bekleniyor"]


def test_authors_are_only_what_the_catalog_knows():
    for work in WORKS:
        if work.authority is Authority.BASKASI:
            assert work.author is None, work.slug                # bilinmeyen yazar tahmin edilmez
        elif work.collection is Collection.TEFSIR:               # müfessirin eseri kendi yazarının
            assert work.author and work.author != AUTHOR, work.slug
        else:
            assert work.author == AUTHOR, work.slug
    assert get_work("isaratul-icaz").translator == "Abdülmecid Nursî"
    assert get_work("isaratul-icaz-arabi").editor == "İhsan Kasım es-Sâlihî"
    assert get_work("hutbe-i-samiye").translator == AUTHOR


def test_edition_comes_from_the_raw_data(tmp_path):
    raw = tmp_path / "raw"
    (raw / "risaleoku_app" / "kitap").mkdir(parents=True)
    (raw / "risaleoku_app" / "catalog.json").write_text(json.dumps([
        {"kind": "shelf_group", "id": 1, "data": {"name": "Other Languages"}},
        {"kind": "shelf", "id": 2, "data": {"group_id": 1, "name": "Osmanlıca Kitaplar", "subtitle": "Envar Neşriyat"}},
        {"kind": "book", "id": 3, "data": {"key": "kitap", "shelf_id": 2, "title": "Kitap"}},
        {"kind": "book", "id": 4, "deleted": True, "data": {"key": "silinen", "shelf_id": 2}}]))
    (raw / "risaleoku_app" / "kitap" / "manifest.json").write_text(json.dumps(
        {"files": {"text": "abc"}, "fetched_at": "2026-10-30T13:39:15+00:00"}))
    _risaleoku_catalog.cache_clear()
    record = edition(Work("x", "X", Group.MECMUA, SourceRef(Site.RISALEOKU_APP, "kitap")), raw)
    assert record == {"site": "risaleoku_app", "book": "kitap", "site_url": "https://risaleoku.com",
                      "files": {"text": "abc"}, "fetched_at": "2026-10-30T13:39:15+00:00",
                      "shelf_group": "Other Languages", "shelf": "Osmanlıca Kitaplar", "shelf_note": "Envar Neşriyat",
                      "title": "Kitap"}
    assert edition(Work("y", "Y", Group.MECMUA, SourceRef(Site.ERISALE, "yok")), raw) == {
        "site": "erisale", "book": "yok", "site_url": "https://www.erisale.com"}   # ham veri yoksa yalnız kaynak
    assert edition(Work("z", "Z", Group.MECMUA, None), raw) is None
    _risaleoku_catalog.cache_clear()
