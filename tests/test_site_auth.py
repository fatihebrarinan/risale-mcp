"""S5: risalemcp.com/taslak/ girişi (site_auth.py)."""

import time

import pytest
from starlette.testclient import TestClient

from risale_mcp import site_auth
from risale_mcp.site_auth import COOKIE, Store, build_app, safe_next


@pytest.fixture
def store(tmp_path):
    s = Store(tmp_path / "site.db")
    s.add_user("Okur@Example.org ", "dogru-parola-123", scope="masa")
    return s


@pytest.fixture
def client(store, tmp_path):
    from risale_mcp.masa import MasaStore
    return TestClient(build_app(store, MasaStore(tmp_path / "masa.db")), base_url="https://risalemcp.com",
                      follow_redirects=False)


def test_db_private(store):
    assert store.path.stat().st_mode & 0o077 == 0


def test_add_user_normalizes_and_rejects(store):
    assert [u["email"] for u in store.users()] == ["okur@example.org"]
    with pytest.raises(ValueError):
        store.add_user("okur@example.org", "baska-parola-1")
    with pytest.raises(ValueError):
        store.add_user("e-posta-degil", "baska-parola-1")


def test_login_and_lock(store):
    assert store.login("OKUR@example.org", "dogru-parola-123") == (True, None)
    assert store.login("yok@example.org", "x")[0] is False
    now = time.time()
    for _ in range(site_auth.MAX_FAILURES):
        assert store.login("okur@example.org", "yanlis", now=now)[0] is False
    ok, msg = store.login("okur@example.org", "dogru-parola-123", now=now + 1)
    assert not ok and "saniye" in msg


def test_sessions(store):
    token = store.open_session("okur@example.org")
    assert store.check(token) == "okur@example.org"
    assert store.check("baska") is None
    assert store.check(token, now=time.time() + site_auth.SESSION_DAYS * 86400 + 1) is None
    store.set_password("okur@example.org", "yeni-parola-456")      # parola değişince oturumlar kapanır
    assert store.check(token) is None


def test_names(store, tmp_path):
    assert store.display_name("okur@example.org") == "okur@example.org"
    store.set_name("okur@example.org", "Fatih")
    assert store.display_name("OKUR@example.org") == "Fatih"
    store.add_user("iki@example.org", "dogru-parola-123", name="Ahmet")
    assert store.display_name("iki@example.org") == "Ahmet"
    # ad sütunu olmayan eski dosya açılınca sütun eklenir
    import sqlite3
    old = tmp_path / "eski.db"
    sqlite3.connect(old).executescript("CREATE TABLE users (email TEXT PRIMARY KEY, password TEXT NOT NULL, created REAL NOT NULL,"
                                       " failures INTEGER NOT NULL DEFAULT 0, locked_until REAL NOT NULL DEFAULT 0, last_login REAL);")
    Store(old).add_user("x@example.org", "dogru-parola-123")


def test_safe_next():
    assert safe_next("/taslak/") == "/taslak/"
    assert safe_next("/taslak/index.html?x=1") == "/taslak/index.html?x=1"
    for bad in ("https://kotu.example/", "//kotu.example/", "/gizlilik.html", "/taslak/giris", None, "/taslak\\..\\x"):
        assert safe_next(bad) == "/taslak/"


def test_gate_flow(client):
    r = client.get("/_auth", headers={"X-Forwarded-Uri": "/taslak/"})
    assert r.status_code == 302 and r.headers["location"] == "/taslak/giris?next=/taslak/"
    r = client.post("/taslak/giris?next=/taslak/", data={"email": "okur@example.org", "password": "yanlis"})
    assert r.status_code == 401 and "yanlış" in r.text and COOKIE not in r.cookies
    r = client.post("/taslak/giris?next=https://kotu.example/",
                    data={"email": "okur@example.org", "password": "dogru-parola-123"})
    assert r.status_code == 303 and r.headers["location"] == "/taslak/"
    cookie = next(c for c in r.headers.get_list("set-cookie") if "Max-Age=0" not in c and 'Max-Age="0"' not in c
                  and "max-age=0" not in c.lower())
    assert "HttpOnly" in cookie and "Secure" in cookie and "Path=/;" in cookie and "samesite=lax" in cookie.lower()
    token = r.cookies[COOKIE]
    # Caddy, tarayıcının /taslak/… isteğindeki çerezi olduğu gibi /_auth'a iletir
    assert client.get("/_auth", headers={"Cookie": f"{COOKIE}={token}"}).status_code == 200
    r = client.get("/taslak/ben", headers={"Cookie": f"{COOKIE}={token}"})
    assert r.json() == {"email": "okur@example.org", "name": "okur@example.org", "scope": "masa", "welcomed": False,
                        "place": None}
    client.cookies.clear()
    assert client.get("/taslak/ben").status_code == 401
    assert client.get("/taslak/cikis", headers={"Cookie": f"{COOKIE}={token}"}).status_code == 303
    assert client.get("/_auth", headers={"Cookie": f"{COOKIE}={token}"}).status_code == 302


def test_scopes_and_shared_cookie(store, client):
    store.add_user("okuyucu@example.org", "okuyucu-parola-1", scope="oku")
    r = client.post("/taslak/giris?next=/taslak/", data={"email": "okuyucu@example.org", "password": "okuyucu-parola-1"})
    assert r.status_code == 303 and r.headers["location"] == "/oku/"          # masaya değil platforma
    tok = client.cookies.get(COOKIE)
    assert client.get("/_auth", headers={"x-forwarded-uri": "/oku/2/30"}, cookies={COOKIE: tok}).status_code == 200
    assert client.get("/_auth", headers={"x-forwarded-uri": "/taslak/"}, cookies={COOKIE: tok}).headers["location"] == "/oku/"
    assert client.get("/taslak/api/okumalar", cookies={COOKIE: tok}).status_code == 401
    assert client.get("/taslak/ben", cookies={COOKIE: tok}).json()["scope"] == "oku"


def test_masa_scope_reaches_both(store, client):
    r = client.post("/taslak/giris", data={"email": "okur@example.org", "password": "dogru-parola-123"})
    assert r.headers["location"] == "/taslak/"
    tok = client.cookies.get(COOKIE)
    for uri in ("/taslak/", "/oku/"):
        assert client.get("/_auth", headers={"x-forwarded-uri": uri}, cookies={COOKIE: tok}).status_code == 200
    assert safe_next("/oku/x") == "/oku/" + "x" and safe_next("//evil") == "/taslak/"


def test_everyone_sees_only_own_notes(store, client):
    """S10 (g1): kişisel defter: yönetici (masa) de yalnız kendi notunu görür; defter notunun durumu yoktur."""
    store.add_user("okuyucu@example.org", "okuyucu-parola-1", scope="oku")
    client.post("/taslak/giris", data={"email": "okur@example.org", "password": "dogru-parola-123"})
    masa_tok = client.cookies.get(COOKIE)
    client.cookies.clear()
    client.post("/taslak/giris", data={"email": "okuyucu@example.org", "password": "okuyucu-parola-1"})
    oku_tok = client.cookies.get(COOKIE)
    client.cookies.clear()
    for tok, text in ((masa_tok, "masadan"), (oku_tok, "okuyucudan")):
        client.cookies.set(COOKIE, tok)
        assert client.post("/taslak/api/notlar/30", json={"birim": "30", "metin": text}).status_code == 200
        client.cookies.clear()
    client.cookies.set(COOKIE, oku_tok)
    mine = client.get("/taslak/api/notlar/30").json()["notlar"]
    assert [n["metin"] for n in mine] == ["okuyucudan"]
    nid = mine[0]["id"]
    assert client.put(f"/taslak/api/not/{nid}/durum", json={"durum": "kapandi"}).status_code == 404
    assert client.put(f"/taslak/api/not/{nid}/durum", json={"durum": "geri_cekildi"}).status_code == 404
    client.cookies.clear()
    client.cookies.set(COOKIE, masa_tok)
    assert [n["metin"] for n in client.get("/taslak/api/notlar/30").json()["notlar"]] == ["masadan"]
    assert client.get("/taslak/api/notlar/30?arge=1").json()["notlar"] == []      # defter notları ar-ge değildir
    assert client.put(f"/taslak/api/not/{nid}", json={"metin": "x"}).status_code == 404      # başkasınınki
    assert client.delete(f"/taslak/api/not/{nid}").status_code == 404
    client.cookies.clear()
    client.cookies.set(COOKIE, oku_tok)
    assert client.get("/taslak/api/notlar/30?arge=1").status_code == 401           # ar-ge kaydı masanındır


def test_platform_path_behind_rewrite():
    from risale_mcp.site_auth import allowed
    assert allowed("oku", "/taslak/oku/veri/30.json") and allowed("oku", "/oku/")
    assert not allowed("oku", "/taslak/") and not allowed("oku", "/taslak/birim/30.json")
    assert allowed("masa", "/taslak/birim/30.json")


def test_default_scope_is_oku(tmp_path):
    s = Store(tmp_path / "site.db")
    s.add_user("yeni@example.org", "dogru-parola-123")
    assert s.scope("yeni@example.org") == "oku"


def test_invite_flow(store, client):
    """S10 (b): tek kullanımlık bağlantı, 7 gün; okuyucu parolasını koyar, girmiş olur; yenisi eskisini bozar."""
    old = store.invite("davetli@example.org")
    token = store.invite("Davetli@Example.org ")
    assert store.invite_email(old) is None and store.invite_email(token) == "davetli@example.org"
    assert [d["email"] for d in store.invites()] == ["davetli@example.org"]
    r = client.get(f"/oku/davet/{token}")
    assert r.status_code == 200 and "davetli@example.org" in r.text and r.headers["referrer-policy"] == "no-referrer"
    assert client.get(f"/oku/davet/{old}").status_code == 410
    r = client.post(f"/oku/davet/{token}", data={"password": "kisa", "password2": "kisa"})
    assert r.status_code == 400 and "en az" in r.text
    r = client.post(f"/oku/davet/{token}", data={"password": "uzun-parola-1", "password2": "uzun-parola-2"})
    assert r.status_code == 400 and "aynı değil" in r.text
    r = client.post(f"/oku/davet/{token}", data={"password": "uzun-parola-1", "password2": "uzun-parola-1"})
    assert r.status_code == 303 and r.headers["location"] == "/oku/"
    tok = r.cookies[COOKIE]
    assert store.check(tok) == "davetli@example.org" and store.scope("davetli@example.org") == "oku"
    assert client.get(f"/oku/davet/{token}").status_code == 410                      # tek kullanımlık
    assert store.login("davetli@example.org", "uzun-parola-1")[0]
    # süresi dolan bağlantı
    late = store.invite("baska@example.org", now=time.time() - site_auth.INVITE_DAYS * 86400 - 1)
    assert store.invite_email(late) is None


def test_invite_resets_password_and_keeps_scope(store, client):
    tok = store.open_session("okur@example.org")
    link = store.invite("okur@example.org", scope="oku")           # hesap var: kapsam değişmez
    r = client.post(f"/oku/davet/{link}", data={"password": "yepyeni-parola", "password2": "yepyeni-parola"})
    assert r.status_code == 303 and r.headers["location"] == "/taslak/"
    assert store.scope("okur@example.org") == "masa" and store.check(tok) is None     # eski oturumlar kapandı
    assert store.login("okur@example.org", "yepyeni-parola")[0]


def test_invite_masa_scope(tmp_path):
    s = Store(tmp_path / "site.db")
    s.accept(s.invite("m@example.org", scope="masa", name="M"), "dogru-parola-123")
    assert s.scope("m@example.org") == "masa" and s.display_name("m@example.org") == "M"


def test_welcome_and_place(store, client):
    tok = store.open_session("okur@example.org")
    client.cookies.set(COOKIE, tok)
    assert client.get("/taslak/ben").json()["welcomed"] is False
    assert client.post("/taslak/api/karsilandi").json() == {"ok": True}
    assert client.get("/taslak/ben").json()["welcomed"] is True
    assert client.get("/taslak/api/yer").json() == {"place": None}
    client.put("/taslak/api/yer", json={"birim": "40-46", "paragraf": "p-abc"})
    place = client.get("/taslak/ben").json()["place"]
    assert (place["birim"], place["paragraf"]) == ("40-46", "p-abc")
    client.cookies.clear()
    assert client.put("/taslak/api/yer", json={"birim": "1"}).status_code == 401
    assert client.post("/taslak/api/karsilandi").status_code == 401


def test_remove_user_drops_invites(store):
    store.invite("okur@example.org")
    store.remove_user("okur@example.org")
    assert store.invites() == []
