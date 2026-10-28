"""Aşama 12: sunucunun kimlik doğrulaması (OAuth 2.1) ve kullanım kaydı.

Sunucu internete açıldığında (claude.ai özel bağlayıcısı, uzaktaki Claude Code) yalnızca hesabı olan kişiler
erişir. MCP SDK'sının yerleşik yetkilendirme sunucusu kullanılır: üst veri (RFC 8414, RFC 9728), dinamik istemci
kaydı (RFC 7591), PKCE S256 ve jeton uç noktası SDK'dadır. Bu modül SDK'nın "sağlayıcı"sıdır: istemcileri,
yetkilendirme kodlarını ve jetonları saklar, giriş sayfasını sunar, kullanıcıları ve kullanım kaydını tutar.

Claude'un gereksinimleri (https://claude.com/docs/connectors/building/authentication, 2026-10-28'de okundu):
- Geri dönüş adresi `https://claude.ai/api/mcp/auth_callback` (ileride `claude.com`); Claude Code yerel adrese
  (`http://localhost:<port>/callback`, `http://127.0.0.1:<port>/callback`) döner ve port her oturumda değişir:
  yerel adreslerde port karşılaştırılmaz (`Client.validate_redirect_uri`).
- Geçersiz ya da kullanılmış yenileme jetonu `invalid_grant` alır; yenileme jetonu her kullanımda yenilenir.
- Kayıt yalnızca bu adresleri kabul eder; başka adrese dönen bir istemci kaydedilemez.

Hesaplar (kullanıcının kararı: kişi başına hesap, herkese bütün derlem açık):
- `users`: kullanıcı adı ve parolanın scrypt özeti. Arka arkaya yanlış parolada hesap bir süre kilitlenir.
- Jetonlar ve kodlar rastgele üretilir, veritabanında yalnızca SHA-256 özetleri durur. Erişim jetonu 1 saat,
  yenileme jetonu 30 gün geçerlidir; kullanıcı silinince ya da oturumu kapatılınca jetonları silinir.
- `usage`: her MCP isteği (kim, ne zaman, hangi araç, hangi parametreler, süre, hata) kaydedilir
  (kullanıcının kararı; gelişim için). Parametreler kısaltılarak saklanır.

Hesapsız erişim (kullanıcının kararı, 2026-10-28; Claude'un "lazy authentication"ı,
https://claude.com/docs/connectors/building/lazy-authentication.md): `--anonymous` ile `Authorization` başlığı
taşımayan istekler de geçer (`AnonymousGate`). Jeton taşıyan istek eskisi gibi denetlenir (geçersizse 401, Claude
jetonu yeniler). Giriş gerektiren araç (`sign_in`) hesapsız çağrılınca HTTP 401 + `WWW-Authenticate` döner; Claude
sohbette "Bağlan" kartı gösterir, giriş sonrası aynı çağrıyı tekrarlar. Hesapsızlar için anlamsal aramanın günlük
toplam sınırı vardır (`ANON_SEMANTIC_PER_DAY`), bütün hesapsız istekler dakikada `ANON_PER_MINUTE` ile sınırlıdır
(claude.ai'nin istekleri hep aynı Anthropic adreslerinden geldiği için sınır adres başına değil, topludur).

Veri `data/auth.db`'dedir (git'e eklenmez); `risale.db` her kurulumda sıfırdan yazıldığı için oraya konmaz.

Yönetim: `risale-mcp auth add-user <ad>`, `passwd`, `remove-user`, `users`, `sessions`, `revoke`, `usage`.
"""

import argparse
import base64
import getpass
import hashlib
import hmac
import html
import json
import secrets
import sqlite3
import sys
import threading
import time
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from mcp.server.auth.middleware.auth_context import get_access_token
from mcp.server.auth.provider import (
    AccessToken,
    AuthorizationCode,
    AuthorizationParams,
    AuthorizeError,
    RefreshToken,
    RegistrationError,
    construct_redirect_uri,
)
from mcp.server.auth.settings import AuthSettings, ClientRegistrationOptions, RevocationOptions
from mcp.shared.auth import InvalidRedirectUriError, OAuthClientInformationFull, OAuthToken
from pydantic import AnyUrl
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse, Response

from risale_mcp.paths import DATA_DIR

AUTH_DB = DATA_DIR / "auth.db"
SCOPE = "risale:read"
ACCESS_TTL = 3600
REFRESH_TTL = 30 * 24 * 3600
CODE_TTL = 300
REQUEST_TTL = 600                      # giriş sayfasında bekleyen yetkilendirme isteği
MAX_FAILURES = 5                       # bundan sonra hesap kilitlenir; her yeni hatada süre ikiye katlanır
LOCK_SECONDS = 60
ARG_LIMIT = 2000                       # kullanım kaydında parametrelerin en çok uzunluğu
LOOPBACK = {"localhost", "127.0.0.1", "[::1]", "::1"}
HOSTED_CALLBACKS = {"https://claude.ai/api/mcp/auth_callback", "https://claude.com/api/mcp/auth_callback"}

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    name          TEXT PRIMARY KEY,
    password      TEXT NOT NULL,
    created       REAL NOT NULL,
    failures      INTEGER NOT NULL DEFAULT 0,
    locked_until  REAL NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS clients (
    client_id TEXT PRIMARY KEY,
    info      TEXT NOT NULL,
    created   REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS requests (
    id        TEXT PRIMARY KEY,
    client_id TEXT NOT NULL,
    params    TEXT NOT NULL,
    expires   REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS codes (
    hash      TEXT PRIMARY KEY,
    data      TEXT NOT NULL,
    expires   REAL NOT NULL
);
-- kind: access | refresh. Aynı girişten doğan jetonlar `session`'ı paylaşır (oturum kapatma için).
CREATE TABLE IF NOT EXISTS tokens (
    hash      TEXT PRIMARY KEY,
    kind      TEXT NOT NULL,
    session   TEXT NOT NULL,
    user      TEXT NOT NULL,
    client_id TEXT NOT NULL,
    scopes    TEXT NOT NULL,
    resource  TEXT,
    created   REAL NOT NULL,
    expires   REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS tokens_user ON tokens(user);
CREATE INDEX IF NOT EXISTS tokens_session ON tokens(session);
CREATE TABLE IF NOT EXISTS usage (
    ts        REAL NOT NULL,
    user      TEXT,
    client_id TEXT,
    method    TEXT NOT NULL,
    name      TEXT,
    params    TEXT,
    ms        INTEGER NOT NULL,
    error     TEXT
);
CREATE INDEX IF NOT EXISTS usage_ts ON usage(ts);
"""


def _digest(secret: str) -> str:
    return hashlib.sha256(secret.encode()).hexdigest()


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    n, r, p = 2**14, 8, 1
    key = hashlib.scrypt(password.encode(), salt=salt, n=n, r=r, p=p, dklen=32)
    return f"scrypt${n}${r}${p}${base64.b64encode(salt).decode()}${base64.b64encode(key).decode()}"


def check_password(password: str, stored: str) -> bool:
    _, n, r, p, salt, key = stored.split("$")
    got = hashlib.scrypt(password.encode(), salt=base64.b64decode(salt), n=int(n), r=int(r), p=int(p), dklen=32)
    return hmac.compare_digest(got, base64.b64decode(key))


def _is_loopback(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "http" and (parsed.hostname or "") in LOOPBACK


def allowed_redirect(url: str) -> bool:
    """Claude'un barındırılan uygulamaları ya da yerel adres (Claude Code, MCP Inspector)."""
    return url in HOSTED_CALLBACKS or _is_loopback(url)


class Client(OAuthClientInformationFull):
    """Yerel geri dönüş adreslerinde port karşılaştırılmaz (RFC 8252 §7.3; Claude Code her oturumda başka port)."""

    def validate_redirect_uri(self, redirect_uri: AnyUrl | None) -> AnyUrl:
        if redirect_uri is not None and _is_loopback(str(redirect_uri)):
            wanted = urlparse(str(redirect_uri))
            for registered in self.redirect_uris or []:
                have = urlparse(str(registered))
                if _is_loopback(str(registered)) and have.hostname == wanted.hostname and have.path == wanted.path:
                    return redirect_uri
            raise InvalidRedirectUriError(f"Redirect URI '{redirect_uri}' not registered for client")
        return super().validate_redirect_uri(redirect_uri)


class AuthStore:
    """`data/auth.db`: kullanıcılar, istemciler, kodlar, jetonlar, kullanım kaydı."""

    def __init__(self, path: Path = AUTH_DB) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        self._lock = threading.Lock()
        self.conn = sqlite3.connect(path, check_same_thread=False, isolation_level=None)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    def _run(self, sql: str, params: tuple = ()) -> list[sqlite3.Row]:
        with self._lock:
            return self.conn.execute(sql, params).fetchall()

    # ------------------------------------------------------------ kullanıcılar

    def add_user(self, name: str, password: str) -> None:
        if self._run("SELECT 1 FROM users WHERE name = ?", (name,)):
            raise ValueError(f"{name!r} zaten var")
        self._run("INSERT INTO users (name, password, created) VALUES (?, ?, ?)", (name, hash_password(password), time.time()))

    def set_password(self, name: str, password: str) -> None:
        if not self._run("SELECT 1 FROM users WHERE name = ?", (name,)):
            raise ValueError(f"{name!r} diye bir kullanıcı yok")
        self._run("UPDATE users SET password = ?, failures = 0, locked_until = 0 WHERE name = ?",
                  (hash_password(password), name))
        self.revoke(user=name)

    def remove_user(self, name: str) -> None:
        if not self._run("SELECT 1 FROM users WHERE name = ?", (name,)):
            raise ValueError(f"{name!r} diye bir kullanıcı yok")
        self.revoke(user=name)
        self._run("DELETE FROM users WHERE name = ?", (name,))

    def users(self) -> list[sqlite3.Row]:
        return self._run("SELECT name, created, failures, locked_until FROM users ORDER BY name")

    def login(self, name: str, password: str, now: float | None = None) -> tuple[bool, str | None]:
        """(başarılı mı, hata iletisi). Yanlış denemeler sayılır, sınırı aşan hesap kilitlenir."""
        now = now or time.time()
        rows = self._run("SELECT * FROM users WHERE name = ?", (name,))
        if not rows:
            hash_password(password)                     # süre farkından kullanıcı adı anlaşılmasın
            return False, "Kullanıcı adı ya da parola yanlış."
        user = rows[0]
        if user["locked_until"] > now:
            return False, f"Çok fazla yanlış deneme. {int(user['locked_until'] - now) + 1} saniye sonra tekrar deneyin."
        if check_password(password, user["password"]):
            self._run("UPDATE users SET failures = 0, locked_until = 0 WHERE name = ?", (name,))
            return True, None
        failures = user["failures"] + 1
        locked = now + LOCK_SECONDS * 2 ** (failures - MAX_FAILURES) if failures >= MAX_FAILURES else 0
        self._run("UPDATE users SET failures = ?, locked_until = ? WHERE name = ?", (failures, locked, name))
        return False, "Kullanıcı adı ya da parola yanlış."

    # ------------------------------------------------------------ oturumlar

    def sessions(self, user: str | None = None) -> list[sqlite3.Row]:
        sql = ("SELECT session, user, client_id, min(created) AS started, max(expires) AS expires FROM tokens"
               " WHERE kind = 'refresh' AND expires > ?" + (" AND user = ?" if user else "") +
               " GROUP BY session ORDER BY started")
        return self._run(sql, (time.time(), user) if user else (time.time(),))

    def revoke(self, user: str | None = None, session: str | None = None) -> int:
        if session:
            rows = self._run("DELETE FROM tokens WHERE session = ? RETURNING hash", (session,))
        elif user:
            rows = self._run("DELETE FROM tokens WHERE user = ? RETURNING hash", (user,))
        else:
            rows = self._run("DELETE FROM tokens RETURNING hash")
        return len(rows)

    def client_name(self, client_id: str) -> str:
        rows = self._run("SELECT info FROM clients WHERE client_id = ?", (client_id,))
        return (json.loads(rows[0]["info"]).get("client_name") or client_id) if rows else client_id

    # ------------------------------------------------------------ kullanım kaydı

    def log(self, user: str | None, client_id: str | None, method: str, name: str | None, params: Any,
            ms: int, error: str | None) -> None:
        text = json.dumps(params, ensure_ascii=False) if params is not None else None
        if text and len(text) > ARG_LIMIT:
            text = text[:ARG_LIMIT] + "…"
        self._run("INSERT INTO usage VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (time.time(), user, client_id, method, name, text, ms, error))

    def anonymous_calls(self, tool: str, since: float) -> int:
        return self._run("SELECT count(*) FROM usage WHERE user IS NULL AND method = 'tools/call' AND name = ?"
                         " AND ts >= ?", (tool, since))[0][0]

    def usage(self, user: str | None = None, limit: int = 50) -> list[sqlite3.Row]:
        sql = "SELECT * FROM usage" + (" WHERE user = ?" if user else "") + " ORDER BY ts DESC LIMIT ?"
        return self._run(sql, (user, limit) if user else (limit,))


class Provider:
    """MCP SDK'sının yetkilendirme sunucusu sağlayıcısı (`OAuthAuthorizationServerProvider`)."""

    def __init__(self, store: AuthStore, public_url: str) -> None:
        self.store = store
        self.public_url = public_url.rstrip("/")
        self.resource = f"{self.public_url}/mcp"

    # istemciler
    async def get_client(self, client_id: str) -> Client | None:
        rows = self.store._run("SELECT info FROM clients WHERE client_id = ?", (client_id,))
        return Client.model_validate_json(rows[0]["info"]) if rows else None

    async def register_client(self, client_info: OAuthClientInformationFull) -> None:
        bad = [str(u) for u in client_info.redirect_uris or [] if not allowed_redirect(str(u))]
        if bad or not client_info.redirect_uris:
            raise RegistrationError("invalid_redirect_uri",
                                    f"only Claude's callback or a loopback address is allowed, not {bad}")
        self.store._run("INSERT INTO clients VALUES (?, ?, ?)",
                        (client_info.client_id, client_info.model_dump_json(), time.time()))

    # yetkilendirme: giriş sayfasına yönlendirir; kod giriş başarılı olunca `complete` ile verilir
    async def authorize(self, client: OAuthClientInformationFull, params: AuthorizationParams) -> str:
        if params.resource and params.resource.rstrip("/") != self.resource:
            raise AuthorizeError("invalid_target", f"this server's resource is {self.resource}")
        request_id = secrets.token_urlsafe(24)
        now = time.time()
        self.store._run("DELETE FROM requests WHERE expires < ?", (now,))
        self.store._run("INSERT INTO requests VALUES (?, ?, ?, ?)",
                        (request_id, client.client_id, params.model_dump_json(), now + REQUEST_TTL))
        return f"{self.public_url}/login?request={request_id}"

    def pending(self, request_id: str) -> tuple[str, AuthorizationParams] | None:
        rows = self.store._run("SELECT * FROM requests WHERE id = ? AND expires > ?", (request_id, time.time()))
        if not rows:
            return None
        return rows[0]["client_id"], AuthorizationParams.model_validate_json(rows[0]["params"])

    def complete(self, request_id: str, user: str | None) -> str | None:
        """Giriş bitti: istemcinin geri dönüş adresi (kodla ya da `access_denied` hatasıyla)."""
        found = self.pending(request_id)
        if found is None:
            return None
        self.store._run("DELETE FROM requests WHERE id = ?", (request_id,))
        client_id, params = found
        if user is None:
            return construct_redirect_uri(str(params.redirect_uri), error="access_denied", state=params.state)
        code = secrets.token_urlsafe(32)
        data = AuthorizationCode(
            code="", scopes=params.scopes or [SCOPE], expires_at=time.time() + CODE_TTL, client_id=client_id,
            code_challenge=params.code_challenge, redirect_uri=params.redirect_uri,
            redirect_uri_provided_explicitly=params.redirect_uri_provided_explicitly,
            resource=params.resource, subject=user)
        self.store._run("INSERT INTO codes VALUES (?, ?, ?)", (_digest(code), data.model_dump_json(), data.expires_at))
        return construct_redirect_uri(str(params.redirect_uri), code=code, state=params.state)

    async def load_authorization_code(self, client: OAuthClientInformationFull, authorization_code: str
                                      ) -> AuthorizationCode | None:
        rows = self.store._run("SELECT data FROM codes WHERE hash = ?", (_digest(authorization_code),))
        if not rows:
            return None
        code = AuthorizationCode.model_validate_json(rows[0]["data"])
        return code.model_copy(update={"code": authorization_code}) if code.client_id == client.client_id else None

    async def exchange_authorization_code(self, client: OAuthClientInformationFull,
                                          authorization_code: AuthorizationCode) -> OAuthToken:
        self.store._run("DELETE FROM codes WHERE hash = ?", (_digest(authorization_code.code),))   # tek kullanımlık
        return self._issue(secrets.token_hex(8), authorization_code.subject or "", client.client_id,
                           authorization_code.scopes, authorization_code.resource)

    # jetonlar
    def _issue(self, session: str, user: str, client_id: str, scopes: list[str], resource: str | None) -> OAuthToken:
        now = time.time()
        access, refresh = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
        for token, kind, ttl in ((access, "access", ACCESS_TTL), (refresh, "refresh", REFRESH_TTL)):
            self.store._run("INSERT INTO tokens VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (_digest(token), kind, session, user, client_id, " ".join(scopes), resource, now, now + ttl))
        return OAuthToken(access_token=access, token_type="Bearer", expires_in=ACCESS_TTL,
                          scope=" ".join(scopes), refresh_token=refresh)

    def _token(self, token: str, kind: str) -> sqlite3.Row | None:
        rows = self.store._run("SELECT * FROM tokens WHERE hash = ? AND kind = ? AND expires > ?",
                               (_digest(token), kind, time.time()))
        return rows[0] if rows else None

    async def load_refresh_token(self, client: OAuthClientInformationFull, refresh_token: str) -> RefreshToken | None:
        row = self._token(refresh_token, "refresh")
        if row is None or row["client_id"] != client.client_id:
            return None
        return RefreshToken(token=refresh_token, client_id=row["client_id"], scopes=row["scopes"].split(),
                            expires_at=int(row["expires"]), resource=row["resource"], subject=row["user"])

    async def exchange_refresh_token(self, client: OAuthClientInformationFull, refresh_token: RefreshToken,
                                     scopes: list[str]) -> OAuthToken:
        row = self._token(refresh_token.token, "refresh")
        session = row["session"] if row else secrets.token_hex(8)
        # Döndürme: eski yenileme jetonu ve aynı oturumun erişim jetonları geçersiz olur.
        self.store._run("DELETE FROM tokens WHERE session = ?", (session,))
        return self._issue(session, refresh_token.subject or "", client.client_id, scopes, refresh_token.resource)

    async def load_access_token(self, token: str) -> AccessToken | None:
        row = self._token(token, "access")
        if row is None or (row["resource"] and row["resource"].rstrip("/") != self.resource):
            return None
        return AccessToken(token=token, client_id=row["client_id"], scopes=row["scopes"].split(),
                           expires_at=int(row["expires"]), resource=row["resource"], subject=row["user"])

    async def revoke_token(self, token: AccessToken | RefreshToken) -> None:
        self.store._run("DELETE FROM tokens WHERE hash = ?", (_digest(token.token),))


def settings(public_url: str) -> AuthSettings:
    base = public_url.rstrip("/")
    return AuthSettings(
        issuer_url=base, resource_server_url=f"{base}/mcp", required_scopes=[SCOPE],
        validate_token_resource=False,           # `Provider.load_access_token` jetonun kaynağını kendisi denetler
        client_registration_options=ClientRegistrationOptions(enabled=True, valid_scopes=[SCOPE],
                                                              default_scopes=[SCOPE]),
        revocation_options=RevocationOptions(enabled=True))


# ---------------------------------------------------------------- giriş sayfası

_PAGE = """<!doctype html><html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Risale-i Nur MCP: giriş</title>
<style>body{{font-family:system-ui,sans-serif;max-width:26rem;margin:3rem auto;padding:0 1rem;color:#222}}
label{{display:block;margin:.8rem 0 .2rem}}input{{width:100%;padding:.5rem;font-size:1rem;box-sizing:border-box}}
button{{margin-top:1rem;padding:.6rem 1rem;font-size:1rem}}.err{{color:#b00020}}.who{{background:#f4f4f4;padding:.6rem}}
</style></head><body><h1>Risale-i Nur MCP</h1>
<p class="who"><b>{client}</b> bu sunucudaki metinleri okumak için izin istiyor. Giriş başarılı olursa
<b>{host}</b> adresine dönülecek.</p>{warning}{error}
<form method="post"><input type="hidden" name="request" value="{request}">
<label for="u">Kullanıcı adı</label><input id="u" name="username" autocomplete="username" required autofocus>
<label for="p">Parola</label><input id="p" name="password" type="password" autocomplete="current-password" required>
<button type="submit" name="action" value="allow">Giriş yap ve izin ver</button>
<button type="submit" name="action" value="deny" formnovalidate>Vazgeç</button></form></body></html>"""


def _page(provider: Provider, request_id: str, error: str | None = None, status: int = 200) -> Response:
    found = provider.pending(request_id)
    if found is None:
        return HTMLResponse("<p>Bu giriş isteğinin süresi doldu. Bağlantıyı yeniden başlatın.</p>", status_code=400)
    client_id, params = found
    target = str(params.redirect_uri)
    warning = ("<p class='err'>Bu istek bu bilgisayardaki bir programa (yerel adres) dönecek. Bağlantıyı siz "
               "başlatmadıysanız izin vermeyin.</p>") if _is_loopback(target) else ""
    return HTMLResponse(_PAGE.format(
        client=html.escape(provider.store.client_name(client_id)), host=html.escape(urlparse(target).netloc),
        warning=warning, error=f"<p class='err'>{html.escape(error)}</p>" if error else "",
        request=html.escape(request_id)), status_code=status, headers={"Cache-Control": "no-store"})


def login_endpoint(provider: Provider) -> Callable[[Request], Awaitable[Response]]:
    async def login(request: Request) -> Response:
        if request.method == "GET":
            return _page(provider, request.query_params.get("request", ""))
        form = await request.form()
        request_id = str(form.get("request", ""))
        if provider.pending(request_id) is None:
            return _page(provider, request_id)
        if form.get("action") == "deny":
            return RedirectResponse(provider.complete(request_id, None), status_code=302)
        user = str(form.get("username", "")).strip()
        ok, error = provider.store.login(user, str(form.get("password", "")))
        if not ok:
            return _page(provider, request_id, error, status=401)
        return RedirectResponse(provider.complete(request_id, user), status_code=302)
    return login


# ---------------------------------------------------------------- kullanım kaydı (MCP ara katmanı)

def usage_middleware(store: AuthStore):
    """Her MCP isteğini (bildirimler hariç) kaydeder: kim, hangi yöntem ve araç, parametreler, süre, hata."""
    async def middleware(ctx, call_next):
        if ctx.request_id is None:                      # bildirim
            return await call_next(ctx)
        start = time.perf_counter()
        error = None
        try:
            return await call_next(ctx)
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"[:500]
            raise
        finally:
            token = get_access_token()
            params = ctx.params if isinstance(ctx.params, dict) else None
            name = params.get("name") or params.get("uri") if params else None
            args = params.get("arguments") if params and "arguments" in params else None
            if ctx.method not in ("ping",):
                store.log(token.subject if token else None, token.client_id if token else None, ctx.method,
                          name, args, int((time.perf_counter() - start) * 1000), error)
    return middleware


# ---------------------------------------------------------------- hesapsız erişim

ANON_PER_MINUTE = 120                  # bütün hesapsız MCP istekleri, toplam
ANON_SEMANTIC_PER_DAY = 2000           # hesapsızların günlük anlamsal arama sınırı, toplam
PROTECTED_TOOLS = frozenset({"sign_in"})


def start_of_day(now: float | None = None) -> float:
    t = time.localtime(now or time.time())
    return time.mktime((t.tm_year, t.tm_mon, t.tm_mday, 0, 0, 0, 0, 0, -1))


def _calls_protected_tool(body: bytes) -> bool:
    try:
        data = json.loads(body)
    except ValueError:
        return False
    for message in data if isinstance(data, list) else [data]:
        if isinstance(message, dict) and message.get("method") == "tools/call" \
                and (message.get("params") or {}).get("name") in PROTECTED_TOOLS:
            return True
    return False


class AnonymousGate:
    """`/mcp` önündeki kapı: jetonlu istek SDK'nın denetimine (`protected`), jetonsuz istek doğrudan MCP'ye
    (`inner`) gider; jetonsuz `sign_in` çağrısı 401 alır, hesapsız istekler dakika sınırını aşınca 429."""

    def __init__(self, protected, inner, resource_metadata_url: str, per_minute: int = ANON_PER_MINUTE) -> None:
        self.protected, self.inner = protected, inner
        self.challenge = (f'Bearer error="invalid_token", error_description="Sign in to use this tool", '
                          f'resource_metadata="{resource_metadata_url}", scope="{SCOPE}"')
        self.per_minute = per_minute
        self.recent: list[float] = []

    async def __call__(self, scope, receive, send) -> None:
        if any(name == b"authorization" for name, _ in scope.get("headers", [])):
            return await self.protected(scope, receive, send)
        body, more = b"", True
        if scope.get("method") == "POST":
            while more:
                message = await receive()
                body += message.get("body", b"")
                more = message.get("more_body", False)
            if _calls_protected_tool(body):
                return await self._reply(send, 401, {"error": "invalid_token",
                                                     "error_description": "Sign in to use this tool"},
                                         [(b"www-authenticate", self.challenge.encode())])
        now = time.monotonic()
        self.recent = [t for t in self.recent if now - t < 60] + [now]
        if len(self.recent) > self.per_minute:
            return await self._reply(send, 429, {"error": "too_many_requests",
                                                 "error_description": "Public access is busy; try again shortly."},
                                     [(b"retry-after", b"30")])
        replayed = False

        async def replay():
            nonlocal replayed
            if scope.get("method") == "POST" and not replayed:
                replayed = True
                return {"type": "http.request", "body": body, "more_body": False}
            return await receive()
        await self.inner(scope, replay, send)

    @staticmethod
    async def _reply(send, status: int, payload: dict, headers: list[tuple[bytes, bytes]]) -> None:
        data = json.dumps(payload).encode()
        await send({"type": "http.response.start", "status": status,
                    "headers": [(b"content-type", b"application/json"), (b"content-length", str(len(data)).encode()),
                                *headers]})
        await send({"type": "http.response.body", "body": data})


# ---------------------------------------------------------------- komut satırı

def _ask_password() -> str:
    first = getpass.getpass("Parola: ")
    if len(first) < 10:
        sys.exit("Parola en az 10 karakter olmalı.")
    if getpass.getpass("Parola (tekrar): ") != first:
        sys.exit("Parolalar aynı değil.")
    return first


def _when(ts: float) -> str:
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(ts))


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="risale-mcp auth", description="Hesaplar, oturumlar ve kullanım kaydı.")
    parser.add_argument("--db", type=Path, default=AUTH_DB)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("add-user", "passwd", "remove-user"):
        p = sub.add_parser(name)
        p.add_argument("user")
        if name == "add-user":
            p.add_argument("--generate", action="store_true", help="rastgele parola üret ve göster")
    sub.add_parser("users")
    p = sub.add_parser("sessions")
    p.add_argument("--user")
    p = sub.add_parser("revoke", help="oturumları kapat")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--user")
    group.add_argument("--session")
    group.add_argument("--all", action="store_true")
    p = sub.add_parser("usage")
    p.add_argument("--user")
    p.add_argument("--limit", type=int, default=50)
    args = parser.parse_args(argv)
    store = AuthStore(args.db)
    try:
        if args.command == "add-user":
            password = secrets.token_urlsafe(15) if args.generate else _ask_password()
            store.add_user(args.user, password)
            print(f"{args.user} eklendi." + (f" Parola: {password}" if args.generate else ""))
        elif args.command == "passwd":
            store.set_password(args.user, _ask_password())
            print(f"{args.user}: parola değişti, açık oturumları kapatıldı.")
        elif args.command == "remove-user":
            store.remove_user(args.user)
            print(f"{args.user} silindi, oturumları kapatıldı.")
        elif args.command == "users":
            for u in store.users():
                lock = f", kilitli {_when(u['locked_until'])}'e kadar" if u["locked_until"] > time.time() else ""
                print(f"{u['name']:20} {_when(u['created'])}{lock}")
        elif args.command == "sessions":
            for s in store.sessions(args.user):
                print(f"{s['session']}  {s['user']:16} {store.client_name(s['client_id']):24} "
                      f"başladı {_when(s['started'])}, bitiş {_when(s['expires'])}")
        elif args.command == "revoke":
            count = store.revoke(user=args.user, session=args.session) if not args.all else store.revoke()
            print(f"{count} jeton silindi.")
        elif args.command == "usage":
            for u in reversed(store.usage(args.user, args.limit)):
                status = f"HATA {u['error']}" if u["error"] else f"{u['ms']} ms"
                print(f"{_when(u['ts'])} {u['user'] or '-':12} {u['method']:16} {u['name'] or '':18} "
                      f"{status:10} {u['params'] or ''}")
    except ValueError as error:
        sys.exit(str(error))


if __name__ == "__main__":
    main()
