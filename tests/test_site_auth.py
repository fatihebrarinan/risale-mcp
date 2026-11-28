"""S5, S13.15.5: lab.ayinedar.org ve read.ayinedar.org girişi (site_auth.py)."""

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
    return TestClient(build_app(store, MasaStore(tmp_path / "masa.db")), base_url="https://lab.ayinedar.org",
                      follow_redirects=False, headers={"X-Bolum": "lab"})


@pytest.fixture
def read(store, tmp_path):
    from risale_mcp.masa import MasaStore
    return TestClient(build_app(store, MasaStore(tmp_path / "masa.db")), base_url="https://read.ayinedar.org",
                      follow_redirects=False, headers={"X-Bolum": "read"})


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
    assert safe_next("/") == "/"
    assert safe_next("/index.html?x=1") == "/index.html?x=1"
    for bad in ("https://kotu.example/", "//kotu.example/", "/giris", "/giris?next=/", None, "/\\..\\x", "x"):
        assert safe_next(bad) == "/"


def test_gate_flow(client):
    r = client.get("/_auth", headers={"X-Forwarded-Uri": "/ayet.html"})
    assert r.status_code == 302 and r.headers["location"] == "/giris?next=/ayet.html"
    r = client.post("/giris?next=/", data={"email": "okur@example.org", "password": "yanlis"})
    assert r.status_code == 401 and "yanlış" in r.text and COOKIE not in r.cookies
    r = client.post("/giris?next=https://kotu.example/",
                    data={"email": "okur@example.org", "password": "dogru-parola-123"})
    assert r.status_code == 303 and r.headers["location"] == "/"
    cookie = next(c for c in r.headers.get_list("set-cookie") if "Max-Age=0" not in c and 'Max-Age="0"' not in c
                  and "max-age=0" not in c.lower())
    assert "HttpOnly" in cookie and "Secure" in cookie and "Path=/;" in cookie and "samesite=lax" in cookie.lower()
    assert "domain" not in cookie.lower()                    # alan adına bağlı: öbür alt alan adlarına gitmez
    token = r.cookies[COOKIE]
    # Caddy, tarayıcının isteğindeki çerezi olduğu gibi /_auth'a iletir
    assert client.get("/_auth", headers={"Cookie": f"{COOKIE}={token}"}).status_code == 200
    r = client.get("/ben", headers={"Cookie": f"{COOKIE}={token}"})
    assert r.json() == {"email": "okur@example.org", "name": "okur@example.org", "scope": "masa", "welcomed": False,
                        "toured": False, "place": None}
    client.cookies.clear()
    assert client.get("/ben").status_code == 401
    r = client.get("/cikis", headers={"Cookie": f"{COOKIE}={token}"})
    assert r.status_code == 303 and r.headers["location"] == "/giris?cikis=1"
    assert client.get("/_auth", headers={"Cookie": f"{COOKIE}={token}"}).status_code == 302


def test_login_page_names_ayinedar(client):
    r = client.get("/giris")
    assert r.status_code == 200 and "Âyinedâr" in r.text and "/favicon.ico" in r.text


def test_scopes(store, client, read):
    store.add_user("okuyucu@example.org", "okuyucu-parola-1", scope="oku")
    r = client.post("/giris?next=/", data={"email": "okuyucu@example.org", "password": "okuyucu-parola-1"})
    assert r.status_code == 403 and "read.ayinedar.org" in r.text and COOKIE not in r.cookies   # masada oturum açılmaz
    r = read.post("/giris?next=/", data={"email": "okuyucu@example.org", "password": "okuyucu-parola-1"})
    assert r.status_code == 303 and r.headers["location"] == "/"
    tok = read.cookies.get(COOKIE)
    assert read.get("/_auth", headers={"x-forwarded-uri": "/"}, cookies={COOKIE: tok}).status_code == 200
    r = client.get("/_auth", headers={"x-forwarded-uri": "/"}, cookies={COOKIE: tok})       # çerez taşınsa bile
    assert r.status_code == 302 and r.headers["location"] == "https://read.ayinedar.org/"
    assert client.get("/giris", cookies={COOKIE: tok}).status_code == 403
    assert read.get("/api/okumalar", cookies={COOKIE: tok}).status_code == 401
    assert read.get("/ben", cookies={COOKIE: tok}).json()["scope"] == "oku"


def test_masa_scope_reaches_both(store, client, read):
    tok = store.open_session("okur@example.org")
    for c in (client, read):
        assert c.get("/_auth", headers={"x-forwarded-uri": "/"}, cookies={COOKIE: tok}).status_code == 200
    assert read.get("/giris?next=/30", cookies={COOKIE: tok}).headers["location"] == "/30"


def test_missing_area_header_is_lab(store, tmp_path):
    from risale_mcp.masa import MasaStore
    bare = TestClient(build_app(store, MasaStore(tmp_path / "m.db")), base_url="https://x", follow_redirects=False)
    store.add_user("okuyucu@example.org", "okuyucu-parola-1", scope="oku")
    tok = store.open_session("okuyucu@example.org")
    assert bare.get("/_auth", cookies={COOKIE: tok}).status_code == 302


def test_everyone_sees_only_own_notes(store, client, read):
    """S10 (g1): kişisel defter: yönetici (masa) de yalnız kendi notunu görür; defter notunun durumu yoktur."""
    store.add_user("okuyucu@example.org", "okuyucu-parola-1", scope="oku")
    masa_tok = store.open_session("okur@example.org")
    oku_tok = store.open_session("okuyucu@example.org")
    for tok, text in ((masa_tok, "masadan"), (oku_tok, "okuyucudan")):
        read.cookies.set(COOKIE, tok)
        assert read.post("/api/notlar/30", json={"birim": "30", "metin": text}).status_code == 200
        read.cookies.clear()
    read.cookies.set(COOKIE, oku_tok)
    mine = read.get("/api/notlar/30").json()["notlar"]
    assert [n["metin"] for n in mine] == ["okuyucudan"]
    nid = mine[0]["id"]
    assert read.put(f"/api/not/{nid}/durum", json={"durum": "kapandi"}).status_code == 404
    assert read.put(f"/api/not/{nid}/durum", json={"durum": "geri_cekildi"}).status_code == 404
    client.cookies.set(COOKIE, masa_tok)
    assert [n["metin"] for n in client.get("/api/notlar/30").json()["notlar"]] == ["masadan"]
    assert client.get("/api/notlar/30?arge=1").json()["notlar"] == []      # defter notları ar-ge değildir
    assert client.put(f"/api/not/{nid}", json={"metin": "x"}).status_code == 404      # başkasınınki
    assert client.delete(f"/api/not/{nid}").status_code == 404
    assert read.get("/api/notlar/30?arge=1").status_code == 401           # ar-ge kaydı masanındır


def test_allowed():
    from risale_mcp.site_auth import allowed
    assert allowed("oku", "read") and allowed("masa", "read") and allowed("masa", "lab")
    assert not allowed("oku", "lab")


def test_default_scope_is_oku(tmp_path):
    s = Store(tmp_path / "site.db")
    s.add_user("yeni@example.org", "dogru-parola-123")
    assert s.scope("yeni@example.org") == "oku"


def test_invite_flow(store, read):
    """S10 (b): tek kullanımlık bağlantı, 7 gün; okuyucu parolasını koyar, girmiş olur; yenisi eskisini bozar."""
    old = store.invite("davetli@example.org")
    token = store.invite("Davetli@Example.org ")
    assert store.invite_email(old) is None and store.invite_email(token) == "davetli@example.org"
    assert [d["email"] for d in store.invites()] == ["davetli@example.org"]
    r = read.get(f"/davet/{token}")
    assert r.status_code == 200 and "davetli@example.org" in r.text and r.headers["referrer-policy"] == "no-referrer"
    assert read.get(f"/davet/{old}").status_code == 410
    r = read.post(f"/davet/{token}", data={"password": "kisa", "password2": "kisa"})
    assert r.status_code == 400 and "en az" in r.text
    r = read.post(f"/davet/{token}", data={"password": "uzun-parola-1", "password2": "uzun-parola-2"})
    assert r.status_code == 400 and "aynı değil" in r.text
    r = read.post(f"/davet/{token}", data={"password": "uzun-parola-1", "password2": "uzun-parola-1"})
    assert r.status_code == 303 and r.headers["location"] == "/"
    tok = r.cookies[COOKIE]
    assert store.check(tok) == "davetli@example.org" and store.scope("davetli@example.org") == "oku"
    assert read.get(f"/davet/{token}").status_code == 410                      # tek kullanımlık
    assert store.login("davetli@example.org", "uzun-parola-1")[0]
    # süresi dolan bağlantı
    late = store.invite("baska@example.org", now=time.time() - site_auth.INVITE_DAYS * 86400 - 1)
    assert store.invite_email(late) is None


def test_invite_resets_password_and_keeps_scope(store, read):
    tok = store.open_session("okur@example.org")
    link = store.invite("okur@example.org", scope="oku")           # hesap var: kapsam değişmez
    r = read.post(f"/davet/{link}", data={"password": "yepyeni-parola", "password2": "yepyeni-parola"})
    assert r.status_code == 303 and r.headers["location"] == "/"
    assert store.scope("okur@example.org") == "masa" and store.check(tok) is None     # eski oturumlar kapandı
    assert store.login("okur@example.org", "yepyeni-parola")[0]


def test_invite_masa_scope(tmp_path):
    s = Store(tmp_path / "site.db")
    s.accept(s.invite("m@example.org", scope="masa", name="M"), "dogru-parola-123")
    assert s.scope("m@example.org") == "masa" and s.display_name("m@example.org") == "M"


def test_welcome_and_place(store, read):
    tok = store.open_session("okur@example.org")
    read.cookies.set(COOKIE, tok)
    assert read.get("/ben").json()["welcomed"] is False
    assert read.post("/api/karsilandi").json() == {"ok": True}
    assert read.get("/ben").json()["welcomed"] is True
    assert read.get("/ben").json()["toured"] is False             # S13.23.8: rehber ayrı tutulur
    assert read.post("/api/rehber").json() == {"ok": True}
    assert read.get("/ben").json()["toured"] is True
    assert read.get("/api/yer").json() == {"place": None}
    read.put("/api/yer", json={"birim": "40-46", "paragraf": "p-abc"})
    place = read.get("/ben").json()["place"]
    assert (place["birim"], place["paragraf"]) == ("40-46", "p-abc")
    read.cookies.clear()
    assert read.put("/api/yer", json={"birim": "1"}).status_code == 401
    assert read.post("/api/karsilandi").status_code == 401
    assert read.post("/api/rehber").status_code == 401


def test_remove_user_drops_invites(store):
    store.invite("okur@example.org")
    store.remove_user("okur@example.org")
    assert store.invites() == []


def test_invite_link_points_to_read():
    assert site_auth.READ + site_auth.INVITE == "https://read.ayinedar.org/davet/"


def test_open_invite(store, read):
    """Açık davet: okuyucu e-postasını kendisi yazar; yalnız yeni hesap açar; not hesaba geçer."""
    token = store.invite(None, label="Ahmet Hoca")
    assert store.invite_email(token) == "" and store.invites()[0]["label"] == "Ahmet Hoca"
    r = read.get(f"/davet/{token}")
    assert r.status_code == 200 and "Hesabınızı açın" in r.text and " readonly " not in r.text
    pw = {"password": "uzun-parola-1", "password2": "uzun-parola-1"}
    r = read.post(f"/davet/{token}", data={"email": "okur@example.org"} | pw)     # var olan hesap: ele geçirilemez
    assert r.status_code == 400 and "zaten var" in r.text and store.login("okur@example.org", "dogru-parola-123")[0]
    r = read.post(f"/davet/{token}", data={"email": "adres-degil"} | pw)
    assert r.status_code == 400 and "Geçerli" in r.text and "adres-degil" in r.text        # yazdığı kalır
    r = read.post(f"/davet/{token}", data={"email": " Yeni@Example.org "} | pw)
    assert r.status_code == 303 and r.headers["location"] == "/"
    assert store.check(r.cookies[COOKIE]) == "yeni@example.org" and store.scope("yeni@example.org") == "oku"
    assert {u["email"]: u["label"] for u in store.users()}["yeni@example.org"] == "Ahmet Hoca"
    assert read.get(f"/davet/{token}").status_code == 410                         # tek kullanımlık
    other = store.invite(None)
    with pytest.raises(ValueError):
        store.accept(other, "uzun-parola-1", email="yeni@example.org")                 # ikinci kez aynı adres


def test_labels(store):
    store.set_label("okur@example.org", "kendi hesabım")
    assert store.users()[0]["label"] == "kendi hesabım"
    store.accept(store.invite("okur@example.org", label="yeni not"), "yepyeni-parola")   # yenilemede not güncellenir
    assert store.users()[0]["label"] == "yeni not"
