"""S11: site yazılarının taslaklarını web'de düzenlemek (yazilar.py)."""

import pytest
from starlette.testclient import TestClient

from risale_mcp.masa import MasaStore
from risale_mcp.site_auth import COOKIE, Store, build_app
from risale_mcp.yazilar import YaziStore, sha

DRAFT = """---
baslik: Deneme yazısı
tarih: 2026-11-23
ozet: Kısa özet.
durum: taslak
whatsapp: |
  Paylaşım metni.
---

İlk paragraf **kalın**.
"""
AD = "yenilikler/2026-11-23-deneme"


@pytest.fixture
def setup(tmp_path):
    root = tmp_path / "repo"
    (root / "docs" / "yenilikler").mkdir(parents=True)
    (root / "docs" / "yenilikler" / "2026-11-23-deneme.md").write_text(DRAFT, encoding="utf-8")
    (root / "docs" / "yenilikler" / "2026-11-01-eski.md").write_text(DRAFT.replace("durum: taslak", "durum: yayinda"),
                                                                     encoding="utf-8")
    auth = Store(tmp_path / "site.db")
    auth.add_user("yazar@example.org", "dogru-parola-123", scope="masa")
    auth.add_user("masa@example.org", "dogru-parola-123", scope="masa")
    yz = YaziStore(tmp_path / "yazilar.db", root)
    yz.allow("Yazar@example.org")
    client = TestClient(build_app(auth, MasaStore(tmp_path / "masa.db"), yz), base_url="https://lab.ayinedar.org")

    def login(email):
        client.cookies.set(COOKIE, auth.open_session(email))
    return client, yz, root, login


def test_only_editors(setup):
    client, _, _, login = setup
    assert client.get("/api/yazi", params={"ad": AD}).status_code == 403
    login("masa@example.org")
    assert client.get("/api/yazi/yetki").json() == {"duzenleyebilir": False}
    assert client.put("/api/yazi", json={"ad": AD, "metin": "x"}).status_code == 403
    login("yazar@example.org")
    assert client.get("/api/yazi/yetki").json() == {"duzenleyebilir": True}


def test_versions_and_state(setup):
    client, yz, root, login = setup
    login("yazar@example.org")
    s = client.get("/api/yazi", params={"ad": AD}).json()
    assert s["kaynak"] == "depo" and s["metin"] == DRAFT and s["surum"] == 0 and s["taslak"]
    assert client.put("/api/yazi", json={"ad": AD, "metin": DRAFT}).json()["degismedi"]
    v1 = DRAFT.replace("İlk", "Birinci")
    assert client.put("/api/yazi", json={"ad": AD, "metin": v1}).json()["surum"] == 1
    v2 = v1.replace("kalın", "koyu")
    assert client.put("/api/yazi", json={"ad": AD, "metin": v2}).json()["surum"] == 2
    s = client.get("/api/yazi", params={"ad": AD}).json()
    assert s["kaynak"] == "web" and s["metin"] == v2 and [g["n"] for g in s["gecmis"]] == [2, 1] and "cakisma" not in s
    assert client.get("/api/yazi", params={"ad": AD, "surum": 1}).json()["metin"] == v1
    exp = yz.export()[AD]
    assert exp["sha"] == sha(v2) and exp["taban"] == sha(DRAFT) and sha(DRAFT) in exp["bilinen"]
    # depo web sürümüne yetişti (geri çekildi, deploy edildi): düzenleyici depoyu açar, yeni sürümün tabanı bugünkü depo
    (root / "docs" / "yenilikler" / "2026-11-23-deneme.md").write_text(v2, encoding="utf-8")
    assert client.get("/api/yazi", params={"ad": AD}).json()["kaynak"] == "depo"
    v3 = v2 + "\nEk.\n"
    client.put("/api/yazi", json={"ad": AD, "metin": v3})
    assert yz.export()[AD]["taban"] == sha(v2)


def test_conflict(setup):
    client, _, root, login = setup
    login("yazar@example.org")
    client.put("/api/yazi", json={"ad": AD, "metin": DRAFT + "\nweb\n"})
    other = DRAFT + "\nyerel\n"
    (root / "docs" / "yenilikler" / "2026-11-23-deneme.md").write_text(other, encoding="utf-8")
    s = client.get("/api/yazi", params={"ad": AD}).json()
    assert s["cakisma"] and s["depo_metin"] == other and s["metin"].endswith("web\n")
    client.put("/api/yazi", json={"ad": AD, "metin": DRAFT + "\nweb\nyerel\n", "taban": s["depo_sha"]})
    assert "cakisma" not in client.get("/api/yazi", params={"ad": AD}).json()


def test_published_and_bad_names(setup):
    client, _, _, login = setup
    login("yazar@example.org")
    r = client.put("/api/yazi", json={"ad": "yenilikler/2026-11-01-eski", "metin": "x"})
    assert r.status_code == 403
    for bad in ["../../etc/passwd", "yenilikler/../x", "baska/2026-x", "yenilikler/yok"]:
        assert client.get("/api/yazi", params={"ad": bad}).status_code == 404


def test_preview_uses_site_program(setup):
    client, _, _, login = setup
    login("yazar@example.org")
    d = client.post("/api/yazi/onizle", json={"ad": AD, "metin": DRAFT}).json()
    assert "<strong>kalın</strong>" in d["html"] and "Deneme yazısı" in d["html"]
    d = client.post("/api/yazi/onizle", json={"ad": AD, "metin": "üst bilgi yok"}).json()
    assert "üst bilgi" in d["hata"]
