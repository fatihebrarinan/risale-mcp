"""S5: risalemcp.com/taslak/ girişi (site_auth.py)."""

import time

import pytest
from starlette.testclient import TestClient

from risale_mcp import site_auth
from risale_mcp.site_auth import COOKIE, Store, build_app, safe_next


@pytest.fixture
def store(tmp_path):
    s = Store(tmp_path / "site.db")
    s.add_user("Okur@Example.org ", "dogru-parola-123")
    return s


@pytest.fixture
def client(store):
    return TestClient(build_app(store), base_url="https://risalemcp.com", follow_redirects=False)


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
    cookie = r.headers["set-cookie"]
    assert "HttpOnly" in cookie and "Secure" in cookie and "Path=/taslak/" in cookie and "samesite=lax" in cookie.lower()
    token = r.cookies[COOKIE]
    # Caddy, tarayıcının /taslak/… isteğindeki çerezi olduğu gibi /_auth'a iletir
    assert client.get("/_auth", headers={"Cookie": f"{COOKIE}={token}"}).status_code == 200
    client.cookies.clear()
    assert client.get("/taslak/cikis", headers={"Cookie": f"{COOKIE}={token}"}).status_code == 303
    assert client.get("/_auth", headers={"Cookie": f"{COOKIE}={token}"}).status_code == 302
