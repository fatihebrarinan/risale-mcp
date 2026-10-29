"""Aşama 12: OAuth ile korunan HTTP sunucusu. Claude'un gereksinimleri uçtan uca, süreç içinde denenir:
401 + üst veri, kayıt, PKCE'li yetkilendirme, giriş sayfası, jeton, MCP çağrısı, yenileme, iptal, kullanım kaydı."""

import base64
import hashlib
import secrets
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest
from starlette.testclient import TestClient

from risale_mcp.auth import MAX_FAILURES, AuthStore, check_password, hash_password
from risale_mcp.library import Library
from risale_mcp.server import create_server, http_app, http_security

PUBLIC = "https://mcp.example"
CALLBACK = "https://claude.ai/api/mcp/auth_callback"
PASSWORD = "doğru-parola-123"


@pytest.fixture
def store(tmp_path):
    store = AuthStore(tmp_path / "auth.db")
    store.add_user("fatih", PASSWORD)
    store.add_user("abi", "abinin-parolasi-1")
    return store


@pytest.fixture
def client(small_db, store):
    server = create_server(Library(small_db[0]), PUBLIC, store)
    app = server.streamable_http_app(transport_security=http_security(PUBLIC))
    with TestClient(app, base_url=PUBLIC, follow_redirects=False) as client:
        yield client


def pkce() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(48)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    return verifier, challenge


def register(client, redirect=CALLBACK) -> dict:
    response = client.post("/register", json={"redirect_uris": [redirect], "client_name": "Claude",
                                              "token_endpoint_auth_method": "none",
                                              "grant_types": ["authorization_code", "refresh_token"]})
    assert response.status_code == 201, response.text
    return response.json()


def authorize(client, reg: dict, challenge: str, redirect=CALLBACK) -> str:
    response = client.get("/authorize", params={
        "response_type": "code", "client_id": reg["client_id"], "redirect_uri": redirect,
        "code_challenge": challenge, "code_challenge_method": "S256", "state": "durum", "scope": "risale:read",
        "resource": f"{PUBLIC}/mcp"})
    assert response.status_code == 302, response.text
    login = urlparse(response.headers["location"])
    assert f"{login.scheme}://{login.netloc}{login.path}" == f"{PUBLIC}/login"
    return parse_qs(login.query)["request"][0]


def sign_in(client, request_id: str, user="fatih", password=PASSWORD):
    return client.post("/login", data={"request": request_id, "username": user, "password": password,
                                       "action": "allow"})


def tokens(client, user="fatih", password=PASSWORD, redirect=CALLBACK) -> tuple[dict, dict]:
    reg = register(client, redirect)
    verifier, challenge = pkce()
    response = sign_in(client, authorize(client, reg, challenge, redirect), user, password)
    assert response.status_code == 302
    back = parse_qs(urlparse(response.headers["location"]).query)
    assert back["state"] == ["durum"]
    response = client.post("/token", data={"grant_type": "authorization_code", "code": back["code"][0],
                                           "redirect_uri": redirect, "client_id": reg["client_id"],
                                           "code_verifier": verifier, "resource": f"{PUBLIC}/mcp"})
    assert response.status_code == 200, response.text
    return reg, response.json()


MCP_HEADERS = {"Accept": "application/json, text/event-stream", "Content-Type": "application/json"}


def mcp_call(client, token: str, method: str, params: dict, session: str | None = None):
    headers = {**MCP_HEADERS, "Authorization": f"Bearer {token}"}
    if session:
        headers["Mcp-Session-Id"] = session
    return client.post("/mcp", headers=headers, json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params})


def test_password_hash_roundtrip():
    stored = hash_password("parola")
    assert check_password("parola", stored) and not check_password("Parola", stored)


def test_unauthenticated_request_points_to_resource_metadata(client):
    response = client.post("/mcp", headers=MCP_HEADERS, json={"jsonrpc": "2.0", "id": 1, "method": "ping"})
    assert response.status_code == 401
    assert 'resource_metadata="https://mcp.example/.well-known/oauth-protected-resource/mcp"' in \
        response.headers["www-authenticate"]
    meta = client.get("/.well-known/oauth-protected-resource/mcp").json()
    assert meta["resource"] == f"{PUBLIC}/mcp" and meta["authorization_servers"][0].rstrip("/") == PUBLIC
    assert meta["scopes_supported"] == ["risale:read"]
    server = client.get("/.well-known/oauth-authorization-server").json()
    assert server["code_challenge_methods_supported"] == ["S256"]
    assert server["registration_endpoint"] == f"{PUBLIC}/register"


def test_registration_accepts_only_claude_and_loopback(client):
    register(client, CALLBACK)
    register(client, "http://127.0.0.1:43123/callback")
    response = client.post("/register", json={"redirect_uris": ["https://evil.example/cb"],
                                              "token_endpoint_auth_method": "none"})
    assert response.status_code == 400 and response.json()["error"] == "invalid_redirect_uri"


def test_full_flow_and_tool_call_is_logged(client, store):
    _, token = tokens(client)
    assert token["token_type"] == "Bearer" and token["refresh_token"]
    response = mcp_call(client, token["access_token"], "initialize", {
        "protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}})
    assert response.status_code == 200, response.text
    session = response.headers.get("mcp-session-id")
    client.post("/mcp", headers={**MCP_HEADERS, "Authorization": f"Bearer {token['access_token']}",
                                 **({"Mcp-Session-Id": session} if session else {})},
                json={"jsonrpc": "2.0", "method": "notifications/initialized"})
    response = mcp_call(client, token["access_token"], "tools/call",
                        {"name": "search", "arguments": {"query": "kiyamet"}}, session)
    assert response.status_code == 200 and "sozler/10/hakikat-01" in response.text
    logged = [row for row in store.usage() if row["method"] == "tools/call"]
    assert logged and logged[0]["user"] == "fatih" and logged[0]["name"] == "search"
    assert logged[0]["params"] is None                     # konuşma içeriği kaydedilmez (dizin politikası 1E)


def test_wrong_password_and_lockout(client, store):
    reg = register(client)
    request_id = authorize(client, reg, pkce()[1])
    for _ in range(MAX_FAILURES):
        response = sign_in(client, request_id, password="yanlış")
        assert response.status_code == 401
    response = sign_in(client, request_id)                  # doğru parola da kilit süresince geçmez
    assert response.status_code == 401 and "saniye sonra" in response.text
    assert store.users()[1]["failures"] == MAX_FAILURES     # sıralama: abi, fatih


def test_deny_returns_access_denied(client):
    reg = register(client)
    request_id = authorize(client, reg, pkce()[1])
    response = client.post("/login", data={"request": request_id, "action": "deny"})
    assert parse_qs(urlparse(response.headers["location"]).query)["error"] == ["access_denied"]


def test_wrong_pkce_verifier_is_rejected(client):
    reg = register(client)
    _, challenge = pkce()
    response = sign_in(client, authorize(client, reg, challenge))
    code = parse_qs(urlparse(response.headers["location"]).query)["code"][0]
    response = client.post("/token", data={"grant_type": "authorization_code", "code": code, "redirect_uri": CALLBACK,
                                           "client_id": reg["client_id"], "code_verifier": pkce()[0]})
    assert response.status_code == 400 and response.json()["error"] == "invalid_grant"


def test_refresh_rotates_and_old_tokens_die(client):
    reg, token = tokens(client)
    form = {"grant_type": "refresh_token", "refresh_token": token["refresh_token"], "client_id": reg["client_id"]}
    response = client.post("/token", data=form)
    assert response.status_code == 200
    fresh = response.json()
    assert fresh["refresh_token"] != token["refresh_token"]
    again = client.post("/token", data=form)                 # kullanılmış yenileme jetonu
    assert again.status_code == 400 and again.json()["error"] == "invalid_grant"
    assert mcp_call(client, token["access_token"], "ping", {}).status_code == 401
    assert mcp_call(client, fresh["access_token"], "initialize", {
        "protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "t", "version": "1"}}
    ).status_code == 200


def test_loopback_redirect_ignores_port(client):
    reg = register(client, "http://127.0.0.1:5000/callback")
    authorize(client, reg, pkce()[1], redirect="http://127.0.0.1:6123/callback")
    response = client.get("/authorize", params={
        "response_type": "code", "client_id": reg["client_id"], "redirect_uri": "http://127.0.0.1:6123/other",
        "code_challenge": pkce()[1], "code_challenge_method": "S256"})
    assert response.status_code == 400                       # yol farklıysa kabul edilmez


def test_revoking_a_user_closes_their_sessions_only(client, store):
    _, mine = tokens(client)
    _, his = tokens(client, "abi", "abinin-parolasi-1")
    assert {s["user"] for s in store.sessions()} == {"fatih", "abi"}
    store.revoke(user="abi")
    assert mcp_call(client, his["access_token"], "ping", {}).status_code == 401
    assert [s["user"] for s in store.sessions()] == ["fatih"]
    store.remove_user("fatih")
    assert mcp_call(client, mine["access_token"], "ping", {}).status_code == 401


def test_stdio_server_has_no_auth(small_db):
    server = create_server(Library(small_db[0]))
    assert server.settings.auth is None


# ---------------------------------------------------------------- hesapsız erişim (lazy authentication)

@pytest.fixture
def anon(small_db, store):
    server = create_server(Library(small_db[0]), PUBLIC, store, anonymous=True, anonymous_semantic=0)
    with TestClient(http_app(server, PUBLIC, anonymous=True), base_url=PUBLIC, follow_redirects=False) as client:
        yield client


def open_session(client, token: str | None = None) -> dict:
    headers = {**MCP_HEADERS, **({"Authorization": f"Bearer {token}"} if token else {})}
    response = client.post("/mcp", headers=headers, json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
        "protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "t", "version": "1"}}})
    assert response.status_code == 200, response.text
    if session := response.headers.get("mcp-session-id"):
        headers["Mcp-Session-Id"] = session
    client.post("/mcp", headers=headers, json={"jsonrpc": "2.0", "method": "notifications/initialized"})
    return headers


def call(client, headers: dict, tool: str, arguments: dict | None = None):
    return client.post("/mcp", headers=headers, json={"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                                                      "params": {"name": tool, "arguments": arguments or {}}})


def test_anonymous_can_search_and_is_logged_without_a_user(anon, store):
    headers = open_session(anon)
    response = call(anon, headers, "search", {"query": "kiyamet"})
    assert response.status_code == 200 and "sozler/10/hakikat-01" in response.text
    logged = [r for r in store.usage() if r["name"] == "search"]
    assert logged and logged[0]["user"] is None


def test_anonymous_sign_in_gets_a_401_challenge(anon):
    headers = open_session(anon)
    response = call(anon, headers, "sign_in")
    assert response.status_code == 401
    challenge = response.headers["www-authenticate"]
    assert 'resource_metadata="https://mcp.example/.well-known/oauth-protected-resource/mcp"' in challenge
    assert 'scope="risale:read"' in challenge


def test_signed_in_user_is_named_and_semantic_search_is_not_limited(anon):
    _, token = tokens(anon)
    headers = open_session(anon, token["access_token"])
    assert '\\"signed_in_as\\":\\"fatih\\"' in call(anon, headers, "sign_in").text
    response = call(anon, headers, "semantic_search", {"query": "kıyamet"})
    assert "daily limit" not in response.text                     # sınır hesapsızlar için


def test_anonymous_semantic_search_has_a_daily_limit(anon):
    headers = open_session(anon)
    response = call(anon, headers, "semantic_search", {"query": "kıyamet"})
    assert response.status_code == 200 and "daily limit" in response.text and "use search" in response.text.lower()


def test_invalid_token_is_still_rejected(anon):
    response = anon.post("/mcp", headers={**MCP_HEADERS, "Authorization": "Bearer yanlis"},
                         json={"jsonrpc": "2.0", "id": 1, "method": "ping"})
    assert response.status_code == 401                            # hesapsız yola düşmez: Claude jetonu yeniler


def test_anonymous_requests_are_rate_limited(anon):
    gate = next(r.app for r in anon.app.router.routes if getattr(r, "path", None) == "/mcp")
    gate.per_minute = 3
    codes = [anon.post("/mcp", headers=MCP_HEADERS, json={"jsonrpc": "2.0", "id": 1, "method": "ping"}).status_code
             for _ in range(5)]
    assert codes[-1] == 429


def test_without_anonymous_mode_there_is_no_sign_in_tool(client):
    _, token = tokens(client)
    headers = open_session(client, token["access_token"])
    assert "sign_in" not in client.post("/mcp", headers=headers, json={
        "jsonrpc": "2.0", "id": 3, "method": "tools/list"}).text


def test_icon_is_served_and_announced(client):
    assert client.get("/favicon.ico").status_code == 200
    assert client.get("/icon.png").headers["content-type"] == "image/png"
    response = client.post("/mcp", headers=MCP_HEADERS, json={"jsonrpc": "2.0", "id": 1, "method": "ping"})
    assert response.status_code == 401                            # ikon açık, MCP korumalı


def test_server_info_carries_icons(small_db):
    remote = create_server(Library(small_db[0]), PUBLIC, AuthStore(Path(small_db[0]).parent / "a.db"))
    assert remote._lowlevel_server.icons[0].src == f"{PUBLIC}/icon.png"
    local = create_server(Library(small_db[0]))
    assert local._lowlevel_server.icons[0].src.startswith("data:image/png;base64,")
