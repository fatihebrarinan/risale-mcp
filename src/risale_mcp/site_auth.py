"""S5: sitenin girişli bölümü (`risalemcp.com/taslak/`) için kimlik doğrulama.

Kullanıcının kararı (2026-11-14): âyet masası taslakları taşır, yayımlanmaz; yalnız davet edilen kişiler girer.
Hesaplar MCP sunucusunun hesapları değildir (`auth.py`), yalnız siteye giriş içindir: ayrı veritabanı
`data/site_auth.db`, kullanıcı adı e-posta adresidir, parolayı yönetici verir (e-posta gönderilmez, dışarıya istek yok).
Parola özeti ve kilit kuralı `auth.py`'dekiyle aynıdır.

Düzen: sayfalar statik dosyadır (`/var/www/ozel/taslak/`); Caddy her istekte bu servise sorar (`forward_auth`,
`GET /_auth`). Oturum çerezi geçerliyse 200, değilse giriş sayfasına yönlendirme. Giriş ve çıkış sayfaları da bu
servistedir (`/taslak/giris`, `/taslak/cikis`). İşaretler sunucuda tutulmaz: tarayıcıda kalır, dışa aktarılır.

Saklananlar (gizlilik politikası söyler): e-posta, parola özeti, yanlış deneme sayısı, son giriş zamanı; oturumun
yalnız özeti, açılış ve son görülme zamanı. IP ve gezinti kaydı tutulmaz.

    uv run python -m risale_mcp.site_auth serve [--port 8009]
    uv run python -m risale_mcp.site_auth add-user <e-posta> [--generate]   # sunucuda: scripts/sunucu.sh taslak …
    uv run python -m risale_mcp.site_auth users | sessions | passwd <e-posta> | remove-user <e-posta> | revoke <e-posta>
"""

import argparse
import getpass
import hashlib
import html
import re
import secrets
import sqlite3
import time
from pathlib import Path
from urllib.parse import quote

from risale_mcp.auth import LOCK_SECONDS, MAX_FAILURES, check_password, hash_password
from risale_mcp.paths import DATA_DIR

DB = DATA_DIR / "site_auth.db"
PREFIX = "/taslak/"
COOKIE = "taslak_oturum"
SESSION_DAYS = 30
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_DUMMY = hash_password(secrets.token_hex(8))

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    email        TEXT PRIMARY KEY,
    password     TEXT NOT NULL,
    created      REAL NOT NULL,
    failures     INTEGER NOT NULL DEFAULT 0,
    locked_until REAL NOT NULL DEFAULT 0,
    last_login   REAL
);
CREATE TABLE IF NOT EXISTS sessions (
    id        TEXT PRIMARY KEY,            -- çerezdeki jetonun SHA-256 özeti
    email     TEXT NOT NULL REFERENCES users(email) ON DELETE CASCADE,
    created   REAL NOT NULL,
    expires   REAL NOT NULL,
    last_seen REAL NOT NULL
);
"""


def norm_email(email: str) -> str:
    return email.strip().lower()


def _digest(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


class Store:
    def __init__(self, path: Path = DB) -> None:
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        with self._conn() as c:
            c.executescript(SCHEMA)

    def _conn(self) -> sqlite3.Connection:
        c = sqlite3.connect(self.path)
        c.row_factory = sqlite3.Row
        c.execute("PRAGMA foreign_keys = ON")
        return c

    def _run(self, sql: str, params: tuple = ()) -> list[sqlite3.Row]:
        with self._conn() as c:
            return c.execute(sql, params).fetchall()

    # ------------------------------------------------------------ hesaplar

    def add_user(self, email: str, password: str) -> None:
        email = norm_email(email)
        if not EMAIL.match(email):
            raise ValueError(f"e-posta adresi değil: {email}")
        if self._run("SELECT 1 FROM users WHERE email = ?", (email,)):
            raise ValueError(f"hesap zaten var: {email}")
        self._run("INSERT INTO users (email, password, created) VALUES (?, ?, ?)",
                  (email, hash_password(password), time.time()))

    def set_password(self, email: str, password: str) -> None:
        email = norm_email(email)
        if not self._run("SELECT 1 FROM users WHERE email = ?", (email,)):
            raise ValueError(f"hesap yok: {email}")
        self._run("UPDATE users SET password = ?, failures = 0, locked_until = 0 WHERE email = ?",
                  (hash_password(password), email))
        self.revoke(email)

    def remove_user(self, email: str) -> None:
        email = norm_email(email)
        self.revoke(email)
        self._run("DELETE FROM users WHERE email = ?", (email,))

    def users(self) -> list[sqlite3.Row]:
        return self._run("SELECT email, created, last_login, failures, locked_until FROM users ORDER BY email")

    def login(self, email: str, password: str, now: float | None = None) -> tuple[bool, str | None]:
        now = now or time.time()
        email = norm_email(email)
        rows = self._run("SELECT * FROM users WHERE email = ?", (email,))
        if not rows:
            check_password(password, _DUMMY)            # süre farkından hesabın varlığı anlaşılmasın
            return False, "E-posta ya da parola yanlış."
        user = rows[0]
        if user["locked_until"] > now:
            return False, f"Çok fazla yanlış deneme. {int(user['locked_until'] - now) + 1} saniye sonra tekrar deneyin."
        if check_password(password, user["password"]):
            self._run("UPDATE users SET failures = 0, locked_until = 0, last_login = ? WHERE email = ?", (now, email))
            return True, None
        failures = user["failures"] + 1
        locked = now + LOCK_SECONDS * 2 ** (failures - MAX_FAILURES) if failures >= MAX_FAILURES else 0
        self._run("UPDATE users SET failures = ?, locked_until = ? WHERE email = ?", (failures, locked, email))
        return False, "E-posta ya da parola yanlış."

    # ------------------------------------------------------------ oturumlar

    def open_session(self, email: str, now: float | None = None) -> str:
        now = now or time.time()
        token = secrets.token_urlsafe(32)
        self._run("INSERT INTO sessions (id, email, created, expires, last_seen) VALUES (?, ?, ?, ?, ?)",
                  (_digest(token), norm_email(email), now, now + SESSION_DAYS * 86400, now))
        self._run("DELETE FROM sessions WHERE expires < ?", (now,))
        return token

    def check(self, token: str | None, now: float | None = None) -> str | None:
        if not token:
            return None
        now = now or time.time()
        rows = self._run("SELECT email, expires, last_seen FROM sessions WHERE id = ?", (_digest(token),))
        if not rows or rows[0]["expires"] < now:
            return None
        if now - rows[0]["last_seen"] > 600:            # son görülme on dakikada bir yazılır
            self._run("UPDATE sessions SET last_seen = ? WHERE id = ?", (now, _digest(token)))
        return rows[0]["email"]

    def close_session(self, token: str | None) -> None:
        if token:
            self._run("DELETE FROM sessions WHERE id = ?", (_digest(token),))

    def sessions(self) -> list[sqlite3.Row]:
        return self._run("SELECT email, created, expires, last_seen FROM sessions ORDER BY last_seen DESC")

    def revoke(self, email: str) -> int:
        n = len(self._run("SELECT 1 FROM sessions WHERE email = ?", (norm_email(email),)))
        self._run("DELETE FROM sessions WHERE email = ?", (norm_email(email),))
        return n


# ---------------------------------------------------------------- web

PAGE = """<!doctype html><html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">
<title>Giriş · Taslak çalışma</title><style>
:root {{ --bg: #fbfaf7; --fg: #1d1d1b; --muted: #6b6a66; --line: #dcd8cf; --card: #fff; --accent: #1f5c3f; --bad: #a3271f; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg: #161614; --fg: #e8e6e1; --muted: #9c9a94; --line: #34332f;
  --card: #1f1e1b; --accent: #7cc49d; --bad: #f08a80; }} }}
body {{ margin: 0; background: var(--bg); color: var(--fg); font: 16px/1.6 system-ui, sans-serif; }}
main {{ max-width: 380px; margin: 12vh auto; padding: 0 16px; }}
h1 {{ font-size: 1.2rem; margin: 0 0 4px; }} p {{ color: var(--muted); font-size: .9rem; }}
form {{ background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 16px; }}
label {{ display: block; font-size: .85rem; margin: 0 0 10px; }}
input {{ display: block; width: 100%; box-sizing: border-box; margin-top: 4px; padding: 7px 9px; font: inherit;
  border: 1px solid var(--line); border-radius: 6px; background: var(--bg); color: var(--fg); }}
button {{ width: 100%; padding: 8px; font: inherit; border: 0; border-radius: 6px; background: var(--accent); color: var(--bg); cursor: pointer; }}
.err {{ color: var(--bad); font-size: .88rem; }} .ok {{ color: var(--accent); font-size: .88rem; }}
a {{ color: inherit; }}
</style></head><body><main>
<h1>Taslak çalışma</h1>
<p>Bu bölüm yalnız davet edilen kişilere açıktır. Hesabınız yoksa site yöneticisinden isteyin.</p>
{message}
<form method="post" action="{action}">
<label>E-posta<input type="email" name="email" autocomplete="username" required value="{email}"></label>
<label>Parola<input type="password" name="password" autocomplete="current-password" required></label>
<button type="submit">Giriş</button>
</form>
<p><a href="/">risalemcp.com</a> · <a href="/gizlilik.html">Gizlilik</a></p>
</main></body></html>"""


def safe_next(target: str | None) -> str:
    """Girişten sonra gidilecek yer yalnız bu bölümün içi olabilir (açık yönlendirme olmasın)."""
    if target and target.startswith(PREFIX) and not target.startswith("//") and "\\" not in target \
            and not target.startswith(PREFIX + "giris"):
        return target
    return PREFIX


def build_app(store: Store):
    from starlette.applications import Starlette
    from starlette.requests import Request
    from starlette.responses import HTMLResponse, PlainTextResponse, RedirectResponse
    from starlette.routing import Route

    def page(next_url: str, message: str = "", email: str = "", status: int = 200) -> HTMLResponse:
        action = f"{PREFIX}giris?next={quote(next_url, safe='/')}"
        return HTMLResponse(PAGE.format(message=message, action=html.escape(action, quote=True),
                                        email=html.escape(email, quote=True)), status_code=status,
                            headers={"Cache-Control": "no-store"})

    def secure(request: Request) -> bool:
        return request.headers.get("x-forwarded-proto", request.url.scheme) == "https"

    async def check(request: Request):
        if store.check(request.cookies.get(COOKIE)):
            return PlainTextResponse("ok", headers={"Cache-Control": "no-store"})
        uri = request.headers.get("x-forwarded-uri", PREFIX)
        return RedirectResponse(f"{PREFIX}giris?next={quote(safe_next(uri), safe='/')}", status_code=302)

    async def login(request: Request):
        next_url = safe_next(request.query_params.get("next"))
        if request.method == "GET":
            if store.check(request.cookies.get(COOKIE)):
                return RedirectResponse(next_url, status_code=302)
            msg = '<p class="ok">Oturum kapatıldı.</p>' if request.query_params.get("cikis") else ""
            return page(next_url, msg)
        form = await request.form()
        email, password = str(form.get("email", "")), str(form.get("password", ""))
        ok, error = store.login(email, password)
        if not ok:
            return page(next_url, f'<p class="err">{html.escape(error)}</p>', email, status=401)
        response = RedirectResponse(next_url, status_code=303)
        response.set_cookie(COOKIE, store.open_session(email), max_age=SESSION_DAYS * 86400, path=PREFIX,
                            httponly=True, secure=secure(request), samesite="lax")
        return response

    async def logout(request: Request):
        store.close_session(request.cookies.get(COOKIE))
        response = RedirectResponse(f"{PREFIX}giris?cikis=1", status_code=303)
        response.delete_cookie(COOKIE, path=PREFIX)
        return response

    return Starlette(routes=[Route("/_auth", check), Route(f"{PREFIX}giris", login, methods=["GET", "POST"]),
                             Route(f"{PREFIX}cikis", logout, methods=["GET", "POST"])])


# ---------------------------------------------------------------- komut satırı

def _when(ts: float | None) -> str:
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(ts)) if ts else "—"


def _password(generate: bool) -> str:
    if generate:
        pw = secrets.token_urlsafe(12)
        print(f"parola: {pw}")
        return pw
    pw = getpass.getpass("parola: ")
    if len(pw) < 10:
        raise SystemExit("parola en az 10 karakter olmalı")
    if pw != getpass.getpass("parola (tekrar): "):
        raise SystemExit("parolalar aynı değil")
    return pw


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="risalemcp.com/taslak/ girişi")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("serve")
    p.add_argument("--port", type=int, default=8009)
    for name in ("add-user", "passwd"):
        p = sub.add_parser(name)
        p.add_argument("email")
        p.add_argument("--generate", action="store_true", help="parolayı üret ve göster")
    for name in ("remove-user", "revoke"):
        sub.add_parser(name).add_argument("email")
    sub.add_parser("users")
    sub.add_parser("sessions")
    args = parser.parse_args(argv)
    store = Store()
    if args.command == "serve":
        import uvicorn
        uvicorn.run(build_app(store), host="127.0.0.1", port=args.port, proxy_headers=True,
                    forwarded_allow_ips="127.0.0.1", access_log=False)
    elif args.command == "add-user":
        store.add_user(args.email, _password(args.generate))
        print(f"hesap açıldı: {norm_email(args.email)}")
    elif args.command == "passwd":
        store.set_password(args.email, _password(args.generate))
        print("parola değişti, açık oturumlar kapatıldı")
    elif args.command == "remove-user":
        store.remove_user(args.email)
        print("hesap silindi")
    elif args.command == "revoke":
        print(f"{store.revoke(args.email)} oturum kapatıldı")
    elif args.command == "users":
        for u in store.users():
            lock = f" kilitli ({_when(u['locked_until'])}'e kadar)" if u["locked_until"] > time.time() else ""
            print(f"{u['email']}  açıldı {_when(u['created'])}  son giriş {_when(u['last_login'])}{lock}")
    elif args.command == "sessions":
        for s in store.sessions():
            print(f"{s['email']}  açıldı {_when(s['created'])}  son görülme {_when(s['last_seen'])}  biter {_when(s['expires'])}")


if __name__ == "__main__":
    main()
