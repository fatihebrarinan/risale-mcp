"""S7.2: ar-ge masasının sunucu tarafı (masa.py): görevler, kararlar, kör eşlemenin saklanması, notlar, dışa aktarma."""

import pytest
from starlette.testclient import TestClient

from risale_mcp.masa import MasaStore
from risale_mcp.site_auth import COOKIE, Store, build_app


@pytest.fixture
def env(tmp_path):
    auth = Store(tmp_path / "site.db")
    auth.add_user("okur@example.org", "dogru-parola-123")
    auth.add_user("iki@example.org", "dogru-parola-123")
    masa = MasaStore(tmp_path / "masa.db")
    token = masa.new_token("taslak-sunucusu")
    client = TestClient(build_app(auth, masa), base_url="https://risalemcp.com", follow_redirects=False)
    return auth, masa, token, client


def login(client, auth, email):
    client.cookies.set(COOKIE, auth.open_session(email), path="/taslak/")


TASK = {"id": "tur-30-D5-kabul", "tur": "ab", "birim": "30", "baslik": "30: h9 ve h12", "sayfa": "/taslak/tur-30.html",
        "atanan": "okur@example.org", "veri": {"yerler": [{"ad": "v1"}, {"ad": "ders"}], "dakika": 20},
        "gizli": {"A": "taslak-5", "B": "taslak-2"}}


def test_task_needs_token(env):
    auth, masa, token, client = env
    assert client.post("/taslak/api/gorev", json=TASK).status_code == 401
    r = client.post("/taslak/api/gorev", json=TASK, headers={"Authorization": f"Bearer {token}"})
    assert r.json() == {"acildi": True}
    assert client.post("/taslak/api/gorev", json=TASK, headers={"Authorization": f"Bearer {token}"}).json() == {"acildi": False}


def test_reading_flow_and_blind_mapping(env):
    auth, masa, token, client = env
    masa.add_task(TASK)
    assert client.get("/taslak/api/okumalar").status_code == 401
    login(client, auth, "okur@example.org")
    [t] = client.get("/taslak/api/okumalar").json()["okumalar"]
    assert (t["durum"], t["yer"], t["karar"]) == ("bekliyor", 2, 0)
    got = client.get("/taslak/api/okuma/tur-30-D5-kabul").json()
    assert "gizli" not in got                                  # kör: taraflar bitene kadar verilmez
    assert client.put("/taslak/api/okuma/tur-30-D5-kabul/karar/v1", json={"secim": "A"}).json() == {"ok": True}
    assert client.put("/taslak/api/okuma/tur-30-D5-kabul/karar/v1", json={"secim": "B", "gerekce": "x"}).json()["ok"]
    got = client.get("/taslak/api/okuma/tur-30-D5-kabul").json()
    assert got["durum"] == "suruyor" and got["kararlar"]["v1"]["secim"] == "B"     # sonuncusu geçerli
    done = client.post("/taslak/api/okuma/tur-30-D5-kabul/bitir").json()
    assert done["durum"] == "bitti" and done["gizli"] == {"A": "taslak-5", "B": "taslak-2"}


def test_assignment_hides_task(env):
    auth, masa, token, client = env
    masa.add_task(TASK)
    login(client, auth, "iki@example.org")
    assert client.get("/taslak/api/okumalar").json()["okumalar"] == []
    assert client.get("/taslak/api/okuma/tur-30-D5-kabul").status_code == 404
    assert client.put("/taslak/api/okuma/tur-30-D5-kabul/karar/v1", json={"secim": "A"}).status_code == 404


def test_notes_lifecycle_and_export_without_names(env):
    auth, masa, token, client = env
    masa.add_task(TASK)
    login(client, auth, "okur@example.org")
    client.put("/taslak/api/okuma/tur-30-D5-kabul/karar/v1", json={"secim": "A"})
    nid = client.post("/taslak/api/notlar/30", json={"birim": "30", "surum": 1, "paragraf": "p-abc", "tur": "hata",
                                                     "metin": "Keşşâf bunu demiyor",
                                                     "secici": {"exact": "كما قال"}}).json()["id"]
    [n] = client.get("/taslak/api/notlar/30").json()["notlar"]
    assert n["benim"] and n["durum"] == "acik" and n["okuyucu_no"] == 1
    assert client.put(f"/taslak/api/not/{nid}/durum", json={"durum": "islendi", "surum": 2}).json()["ok"]
    login(client, auth, "iki@example.org")
    assert client.put(f"/taslak/api/not/{nid}/durum", json={"durum": "geri_cekildi"}).status_code == 404  # yalnız yazan
    assert client.get("/taslak/api/disa").status_code == 401
    out = client.get("/taslak/api/disa", headers={"Authorization": f"Bearer {token}"}).json()
    text = str(out)
    assert "okur@example.org" not in text and "iki@example.org" not in text     # ad yok, numara var
    assert out["notlar"][0]["isleyen_surum"] == 2 and out["okumalar"][0]["kararlar"][0]["okuyucu_no"] == 1
    assert [h["olay"] for h in out["not_gecmisi"]] == ["yazildi", "durum"]


def test_db_private(env):
    assert env[1].path.stat().st_mode & 0o077 == 0


def test_machine_marks_note_processed(tmp_path):
    from starlette.testclient import TestClient
    from risale_mcp.masa import MasaStore
    from risale_mcp.site_auth import Store, build_app
    s = Store(tmp_path / "site.db")
    m = MasaStore(tmp_path / "masa.db")
    tok = m.new_token("taslak-sunucusu")
    nid = m.add_note("okur@example.org", {"birim": "34", "metin": "hata var", "surum": 1, "paragraf": "p-x"})
    c = TestClient(build_app(s, m), base_url="https://risalemcp.com")
    assert c.post("/taslak/api/not-durum", json={"id": nid, "durum": "islendi", "surum": 2}).status_code == 401
    r = c.post("/taslak/api/not-durum", json={"id": nid, "durum": "islendi", "surum": 2},
               headers={"Authorization": f"Bearer {tok}"})
    assert r.status_code == 200
    n = m.export()["notlar"][0]
    assert n["durum"] == "islendi" and n["isleyen_surum"] == 2
