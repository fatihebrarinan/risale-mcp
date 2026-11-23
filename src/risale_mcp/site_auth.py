"""S5: sitenin girişli bölümü (`risalemcp.com/taslak/`) için kimlik doğrulama.

Kullanıcının kararı (2026-11-14): âyet masası taslakları taşır, yayımlanmaz; yalnız davet edilen kişiler girer.
Hesaplar MCP sunucusunun hesapları değildir (`auth.py`), yalnız siteye giriş içindir: ayrı veritabanı
`data/site_auth.db`, kullanıcı adı e-posta adresidir. Parola özeti ve kilit kuralı `auth.py`'dekiyle aynıdır.

S10 (kullanıcının kararları, 2026-11-22): hesap **davet bağlantısıyla** açılır. Yönetici `davet <e-posta>` der, çıkan
bağlantıyı kendi e-postasıyla gönderir (site e-posta göndermez, dışarıya istek yok); okuyucu bağlantıyı açıp parolasını
kendisi koyar ve girmiş olur. Bağlantı tek kullanımlıktır, 7 gün geçerlidir, yalnız özeti saklanır; aynı adrese yeni
bağlantı eskisini geçersiz kılar. Parolasını unutan okuyucuya da yeni bağlantı verilir (hesap varsa parolası değişir,
açık oturumları kapanır). Hesabın varsayılan kapsamı `oku`dur; masa açıkça istenir (`--masa`). İlk girişte platform
karşılama sayfasını gösterir (`welcomed` boşsa); okuyucunun kaldığı yer (`place`: birim ve paragraf) hesabındadır.

**Açık davet** (kullanıcının kararı, 2026-11-23: okuyucuya önce e-postasını sormak gerekmesin): `davet --acik` adressiz
bağlantı verir; okuyucu e-postasını ve parolasını kendisi yazar. Açık bağlantı yalnız yeni hesap açar: adresin hesabı
varsa reddeder (başkasının hesabı ele geçirilmesin); parola yenileme adresli bağlantıyla kalır. E-posta doğrulanmaz:
yalnız giriş adıdır, site e-posta göndermez; kapı bağlantının kendisidir. Davete yöneticinin notu konabilir (`--not`):
hesap açılınca hesabın `label`ı olur, `users` gösterir, okuyucu görmez (gizlilik politikası söyler).

Düzen: sayfalar statik dosyadır (`/var/www/ozel/taslak/`); Caddy her istekte bu servise sorar (`forward_auth`,
`GET /_auth`). Oturum çerezi geçerliyse 200, değilse giriş sayfasına yönlendirme. Giriş ve çıkış sayfaları da bu
servistedir (`/taslak/giris`, `/taslak/cikis`). İşaretler sunucuda tutulmaz: tarayıcıda kalır, dışa aktarılır.
`/taslak/ben` girişli kişinin adını verir (`name`, yoksa e-posta): sayfa işaretlere okuyucu adı olarak onu yazar.

S7.3 (2026-11-21): okuma platformu `/oku/` aynı hesaplarla açılır; çerez bu yüzden bütün sitenin yolundadır (`/`;
yalnız HttpOnly oturum jetonu). Hesabın kapsamı (`scope`): `masa` hem ar-ge masasına (`/taslak/`) hem platforma,
`oku` yalnız platforma girer (davetli okuyucular; `add-user --oku`). Önceki hesaplar `masa`dır.

Saklananlar (gizlilik politikası söyler): e-posta, parola özeti, yanlış deneme sayısı, son giriş zamanı, karşılamanın
görüldüğü zaman, kaldığı yer; oturumun ve davet bağlantısının yalnız özeti, zamanları. IP ve gezinti kaydı tutulmaz.
Okuyucunun notları `masa.py`'dedir (kişisel defter); hesap silinince onlar da silinir.

    uv run python -m risale_mcp.site_auth serve [--port 8009]
    uv run python -m risale_mcp.site_auth davet <e-posta> [--masa] [--name <ad>] [--not <not>]   # sunucuda: scripts/sunucu.sh taslak …
    uv run python -m risale_mcp.site_auth davet --acik [--not <not>] [--masa]                   # e-postayı okuyucu yazar
    uv run python -m risale_mcp.site_auth set-label <e-posta> <not>
    uv run python -m risale_mcp.site_auth davetler                                   # bekleyen bağlantılar
    uv run python -m risale_mcp.site_auth add-user <e-posta> [--generate] [--name <ad>] [--masa]
    uv run python -m risale_mcp.site_auth set-name <e-posta> <ad>
    uv run python -m risale_mcp.site_auth users | sessions | passwd <e-posta> | remove-user <e-posta> | revoke <e-posta>
"""

import argparse
import getpass
import hashlib
import html
import json
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
OKU = "/oku/"
COOKIE = "taslak_oturum"
COOKIE_PATH = "/"                                # /taslak/ ve /oku/ aynı oturumla (S7.3)
SCOPES = ("masa", "oku")
SESSION_DAYS = 30
SITE = "https://risalemcp.com"
INVITE = "/oku/davet/"
INVITE_DAYS = 7
MIN_PASSWORD = 10
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_DUMMY = hash_password(secrets.token_hex(8))

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    email        TEXT PRIMARY KEY,
    name         TEXT,                     -- işaretlerdeki okuyucu adı (isteğe bağlı; yoksa e-posta)
    scope        TEXT NOT NULL DEFAULT 'oku',    -- masa: /taslak/ ve /oku/; oku: yalnız /oku/ (S10'dan önce varsayılan masa)
    password     TEXT NOT NULL,
    created      REAL NOT NULL,
    failures     INTEGER NOT NULL DEFAULT 0,
    locked_until REAL NOT NULL DEFAULT 0,
    last_login   REAL,
    welcomed     REAL,                     -- karşılama sayfası görüldü (S10)
    place        TEXT,                     -- kaldığı yer {birim, paragraf, zaman} (JSON; S10)
    label        TEXT                      -- yöneticinin notu (hesabı tanımak için; okuyucu görmez)
);
CREATE TABLE IF NOT EXISTS invites (
    id       TEXT PRIMARY KEY,             -- bağlantıdaki jetonun SHA-256 özeti
    email    TEXT NOT NULL,                -- boş: açık davet (okuyucu yazar)
    scope    TEXT,                         -- yeni hesabın kapsamı (hesap varsa dokunulmaz, NULL)
    name     TEXT,
    label    TEXT,                         -- yöneticinin notu; hesap açılınca hesaba geçer
    created  REAL NOT NULL,
    expires  REAL NOT NULL,
    used     REAL
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
            cols = {r[1] for r in c.execute("PRAGMA table_info(users)")}
            if "name" not in cols:                                                     # 2026-11-14'ten önceki dosya
                c.execute("ALTER TABLE users ADD COLUMN name TEXT")
            if "scope" not in cols:                                                    # 2026-11-21'den önceki dosya
                c.execute("ALTER TABLE users ADD COLUMN scope TEXT NOT NULL DEFAULT 'masa'")
            for col in ("welcomed REAL", "place TEXT", "label TEXT"):                  # S10'dan önceki dosya
                if col.split()[0] not in cols:
                    c.execute(f"ALTER TABLE users ADD COLUMN {col}")
            if "label" not in {r[1] for r in c.execute("PRAGMA table_info(invites)")}:
                c.execute("ALTER TABLE invites ADD COLUMN label TEXT")
        path.chmod(0o600)                                # e-postalar ve parola özetleri: yalnız servisin kullanıcısı

    def _conn(self) -> sqlite3.Connection:
        c = sqlite3.connect(self.path)
        c.row_factory = sqlite3.Row
        c.execute("PRAGMA foreign_keys = ON")
        return c

    def _run(self, sql: str, params: tuple = ()) -> list[sqlite3.Row]:
        with self._conn() as c:
            return c.execute(sql, params).fetchall()

    # ------------------------------------------------------------ hesaplar

    def add_user(self, email: str, password: str, name: str | None = None, scope: str = "oku") -> None:
        if scope not in SCOPES:
            raise ValueError(f"kapsam: {scope}")
        email = norm_email(email)
        if not EMAIL.match(email):
            raise ValueError(f"e-posta adresi değil: {email}")
        if self._run("SELECT 1 FROM users WHERE email = ?", (email,)):
            raise ValueError(f"hesap zaten var: {email}")
        self._run("INSERT INTO users (email, name, password, created, scope) VALUES (?, ?, ?, ?, ?)",
                  (email, (name or "").strip() or None, hash_password(password), time.time(), scope))

    def scope(self, email: str) -> str:
        rows = self._run("SELECT scope FROM users WHERE email = ?", (norm_email(email),))
        return rows[0]["scope"] if rows else "oku"

    def set_scope(self, email: str, scope: str) -> None:
        if scope not in SCOPES:
            raise ValueError(f"kapsam: {scope}")
        if not self._run("SELECT 1 FROM users WHERE email = ?", (norm_email(email),)):
            raise ValueError(f"hesap yok: {norm_email(email)}")
        self._run("UPDATE users SET scope = ? WHERE email = ?", (scope, norm_email(email)))

    def set_name(self, email: str, name: str) -> None:
        email = norm_email(email)
        if not self._run("SELECT 1 FROM users WHERE email = ?", (email,)):
            raise ValueError(f"hesap yok: {email}")
        self._run("UPDATE users SET name = ? WHERE email = ?", (name.strip() or None, email))

    def display_name(self, email: str) -> str:
        rows = self._run("SELECT name FROM users WHERE email = ?", (norm_email(email),))
        return (rows[0]["name"] if rows else None) or email

    def set_password(self, email: str, password: str) -> None:
        email = norm_email(email)
        if not self._run("SELECT 1 FROM users WHERE email = ?", (email,)):
            raise ValueError(f"hesap yok: {email}")
        self._run("UPDATE users SET password = ?, failures = 0, locked_until = 0 WHERE email = ?",
                  (hash_password(password), email))
        self.revoke(email)

    def exists(self, email: str) -> bool:
        return bool(self._run("SELECT 1 FROM users WHERE email = ?", (norm_email(email),)))

    def remove_user(self, email: str) -> None:
        email = norm_email(email)
        self.revoke(email)
        self._run("DELETE FROM invites WHERE email = ?", (email,))
        self._run("DELETE FROM users WHERE email = ?", (email,))

    # ------------------------------------------------------------ davet (S10)

    def invite(self, email: str | None, scope: str | None = None, name: str | None = None, now: float | None = None,
               label: str | None = None) -> str:
        """Tek kullanımlık bağlantının jetonu. Hesap yoksa açılınca `scope` (varsayılan `oku`), `name` ve `label` alır;
        hesap varsa bağlantı yalnız parolasını yeniler. Aynı adresin kullanılmamış eski bağlantıları geçersiz olur.
        `email` yoksa açık davettir: adresi okuyucu yazar, yalnız yeni hesap açılır."""
        now = now or time.time()
        if scope is not None and scope not in SCOPES:
            raise ValueError(f"kapsam: {scope}")
        label = (label or "").strip()[:200] or None
        token = secrets.token_urlsafe(32)
        if email is None:
            self._run("INSERT INTO invites (id, email, scope, name, label, created, expires) VALUES (?, '', ?, ?, ?, ?, ?)",
                      (_digest(token), scope or "oku", (name or "").strip() or None, label, now, now + INVITE_DAYS * 86400))
            return token
        email = norm_email(email)
        if not EMAIL.match(email):
            raise ValueError(f"e-posta adresi değil: {email}")
        new = not self.exists(email)
        self._run("DELETE FROM invites WHERE email = ? AND used IS NULL", (email,))
        self._run("INSERT INTO invites (id, email, scope, name, label, created, expires) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (_digest(token), email, (scope or "oku") if new else None, (name or "").strip() or None if new else None,
                   label, now, now + INVITE_DAYS * 86400))
        return token

    def invite_email(self, token: str | None, now: float | None = None) -> str | None:
        """Bağlantı geçerliyse (kullanılmamış, süresi dolmamış) adresi; açık davette boş dizi. Geçersizse None."""
        if not token:
            return None
        rows = self._run("SELECT email FROM invites WHERE id = ? AND used IS NULL AND expires > ?",
                         (_digest(token), now or time.time()))
        return rows[0]["email"] if rows else None

    def accept(self, token: str, password: str, now: float | None = None, email: str | None = None) -> str:
        """Okuyucu parolasını koyar: hesap yoksa açılır, varsa parolası değişir (oturumları kapanır). Açık davette
        adresi okuyucu verir (`email`) ve yalnız yeni hesap açılır. Adresi döner."""
        now = now or time.time()
        bound = self.invite_email(token, now)
        if bound is None:
            raise ValueError("Bu bağlantının süresi dolmuş ya da daha önce kullanılmış.")
        if not bound:
            email = norm_email(email or "")
            if not EMAIL.match(email):
                raise ValueError("Geçerli bir e-posta adresi yazın.")
            if self.exists(email):
                raise ValueError("Bu adresle bir hesap zaten var. Giriş sayfasından girin; parolanızı unuttuysanız "
                                 "site yöneticisinden yeni bir bağlantı isteyin.")
        else:
            email = bound
        if len(password) < MIN_PASSWORD:
            raise ValueError(f"Parola en az {MIN_PASSWORD} karakter olmalı.")
        row = self._run("SELECT scope, name, label FROM invites WHERE id = ?", (_digest(token),))[0]
        if self.exists(email):
            self.set_password(email, password)
        else:
            self.add_user(email, password, row["name"], row["scope"] or "oku")
        # bağlantı bir kez: aynı anda iki gönderimde ikincisi işlemez
        with self._conn() as c:
            if c.execute("UPDATE invites SET used = ? WHERE id = ? AND used IS NULL", (now, _digest(token))).rowcount != 1:
                raise ValueError("Bu bağlantının süresi dolmuş ya da daha önce kullanılmış.")
        self._run("UPDATE users SET last_login = ?, label = coalesce(?, label) WHERE email = ?", (now, row["label"], email))
        return email

    def set_label(self, email: str, label: str) -> None:
        email = norm_email(email)
        if not self.exists(email):
            raise ValueError(f"hesap yok: {email}")
        self._run("UPDATE users SET label = ? WHERE email = ?", (label.strip()[:200] or None, email))

    def invites(self, now: float | None = None) -> list[sqlite3.Row]:
        return self._run("SELECT email, scope, label, created, expires FROM invites WHERE used IS NULL AND expires > ? "
                         "ORDER BY created", (now or time.time(),))

    # ------------------------------------------------------------ karşılama ve kaldığı yer (S10)

    def welcomed(self, email: str) -> bool:
        rows = self._run("SELECT welcomed FROM users WHERE email = ?", (norm_email(email),))
        return bool(rows and rows[0]["welcomed"])

    def mark_welcomed(self, email: str) -> None:
        self._run("UPDATE users SET welcomed = coalesce(welcomed, ?) WHERE email = ?", (time.time(), norm_email(email)))

    def place(self, email: str) -> dict | None:
        rows = self._run("SELECT place FROM users WHERE email = ?", (norm_email(email),))
        return json.loads(rows[0]["place"]) if rows and rows[0]["place"] else None

    def set_place(self, email: str, birim: str, paragraf: str | None = None) -> None:
        place = {"birim": str(birim)[:40], "paragraf": str(paragraf)[:80] if paragraf else None, "zaman": time.time()}
        self._run("UPDATE users SET place = ? WHERE email = ?", (json.dumps(place, ensure_ascii=False), norm_email(email)))

    def users(self) -> list[sqlite3.Row]:
        return self._run("SELECT email, name, scope, label, created, last_login, failures, locked_until FROM users "
                         "ORDER BY email")

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

SHELL = """<!doctype html><html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">
<meta name="referrer" content="no-referrer"><title>{title} · Davetli bölüm</title><style>
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
a {{ color: inherit; }} input[readonly] {{ color: var(--muted); }}
</style></head><body><main>
{body}
<p><a href="/">risalemcp.com</a> · <a href="/gizlilik.html">Gizlilik</a></p>
</main></body></html>"""

LOGIN = """<h1>Davetli bölüm</h1>
<p>Bu bölüm yalnız davet edilen kişilere açıktır. Hesabınız yoksa ya da parolanızı unuttuysanız site yöneticisinden
yeni bir davet bağlantısı isteyin.</p>
{message}
<form method="post" action="{action}">
<label>E-posta<input type="email" name="email" autocomplete="username" required value="{email}"></label>
<label>Parola<input type="password" name="password" autocomplete="current-password" required></label>
<button type="submit">Giriş</button>
</form>"""

INVITE_FORM = """<h1>Parolanızı belirleyin</h1>
<p>Bu bağlantı size özeldir ve bir kez kullanılır. Parolanızı belirleyince giriş yapmış olursunuz; sonraki girişlerde
e-posta adresinizle ve bu parolayla girersiniz.</p>
{message}
<form method="post" action="{action}">
<label>E-posta<input type="email" name="email" autocomplete="username" readonly value="{email}"></label>
<label>Parola (en az {min} karakter)<input type="password" name="password" autocomplete="new-password" minlength="{min}" required></label>
<label>Parola (tekrar)<input type="password" name="password2" autocomplete="new-password" minlength="{min}" required></label>
<button type="submit">Parolayı kaydet ve gir</button>
</form>"""

INVITE_OPEN_FORM = """<h1>Hesabınızı açın</h1>
<p>Bu bağlantı size özeldir ve bir kez kullanılır. E-posta adresinizi ve kendinize bir parola yazın; hesabınız açılır ve
giriş yapmış olursunuz. Sonraki girişlerde bu adresle ve bu parolayla girersiniz. E-posta adresiniz yalnız giriş
adınızdır: size e-posta gönderilmez.</p>
{message}
<form method="post" action="{action}">
<label>E-posta<input type="email" name="email" autocomplete="username" required value="{email}"></label>
<label>Parola (en az {min} karakter)<input type="password" name="password" autocomplete="new-password" minlength="{min}" required></label>
<label>Parola (tekrar)<input type="password" name="password2" autocomplete="new-password" minlength="{min}" required></label>
<button type="submit">Hesabı aç ve gir</button>
</form>"""

INVITE_GONE = """<h1>Bağlantı geçersiz</h1>
<p>Bu davet bağlantısının süresi dolmuş ya da daha önce kullanılmış. Site yöneticisinden yeni bir bağlantı isteyin.
Hesabınız varsa <a href="/taslak/giris">giriş sayfasından</a> girebilirsiniz.</p>"""


def safe_next(target: str | None, default: str = PREFIX) -> str:
    """Girişten sonra gidilecek yer yalnız girişli bölümlerin (/taslak/, /oku/) içi olabilir (açık yönlendirme
    olmasın)."""
    if target and target.startswith((PREFIX, OKU)) and not target.startswith("//") and "\\" not in target \
            and not target.startswith(PREFIX + "giris"):
        return target
    return default


def allowed(scope: str, uri: str) -> bool:
    """`oku` kapsamı ar-ge masasına (/taslak/) giremez, platforma girer: /oku/… Caddy'de /taslak/oku/…'ya çevrilir
    (dosyalar orada). API'yi uygulama kendisi denetler."""
    return scope == "masa" or uri.startswith(("/oku", PREFIX + "oku/")) or not uri.startswith(PREFIX.rstrip("/"))


def build_app(store: Store, masa_store=None):
    from starlette.applications import Starlette
    from starlette.requests import Request
    from starlette.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse
    from starlette.routing import Route

    def shell(title: str, body: str, status: int = 200) -> HTMLResponse:
        return HTMLResponse(SHELL.format(title=title, body=body), status_code=status,
                            headers={"Cache-Control": "no-store", "Referrer-Policy": "no-referrer"})

    def page(next_url: str, message: str = "", email: str = "", status: int = 200) -> HTMLResponse:
        action = f"{PREFIX}giris?next={quote(next_url, safe='/')}"
        return shell("Giriş", LOGIN.format(message=message, action=html.escape(action, quote=True),
                                           email=html.escape(email, quote=True)), status)

    def set_session(response, email: str, request: Request) -> None:
        response.delete_cookie(COOKIE, path=PREFIX)                 # 2026-11-21'den önceki çerez (/taslak/ yolunda)
        response.set_cookie(COOKIE, store.open_session(email), max_age=SESSION_DAYS * 86400, path=COOKIE_PATH,
                            httponly=True, secure=secure(request), samesite="lax")

    def secure(request: Request) -> bool:
        return request.headers.get("x-forwarded-proto", request.url.scheme) == "https"

    async def check(request: Request):
        uri = request.headers.get("x-forwarded-uri", PREFIX)
        email = store.check(request.cookies.get(COOKIE))
        if email:
            if allowed(store.scope(email), uri):
                return PlainTextResponse("ok", headers={"Cache-Control": "no-store"})
            return RedirectResponse(OKU, status_code=302)        # yalnız okuyucu: masaya değil platforma
        if uri.startswith(PREFIX + "oku/"):                     # Caddy'nin iç yolu: okuyucu /oku/… adresine dönsün
            uri = OKU + uri[len(PREFIX + "oku/"):]
        return RedirectResponse(f"{PREFIX}giris?next={quote(safe_next(uri), safe='/')}", status_code=302)

    async def login(request: Request):
        next_url = safe_next(request.query_params.get("next"), default="")
        if request.method == "GET":
            email = store.check(request.cookies.get(COOKIE))
            if email:
                return RedirectResponse(next_url or (PREFIX if store.scope(email) == "masa" else OKU), status_code=302)
            msg = '<p class="ok">Oturum kapatıldı.</p>' if request.query_params.get("cikis") else ""
            return page(next_url, msg)
        form = await request.form()
        email, password = str(form.get("email", "")), str(form.get("password", ""))
        ok, error = store.login(email, password)
        if not ok:
            return page(next_url, f'<p class="err">{html.escape(error)}</p>', email, status=401)
        scope = store.scope(email)
        if not next_url or not allowed(scope, next_url):
            next_url = PREFIX if scope == "masa" else OKU
        response = RedirectResponse(next_url, status_code=303)
        set_session(response, email, request)
        return response

    async def invite(request: Request):
        """S10: davet bağlantısı. Okuyucu parolasını koyar, oturum açılır, platforma gider."""
        token = request.path_params["token"]
        email = store.invite_email(token)
        if email is None:
            return shell("Bağlantı geçersiz", INVITE_GONE, 410)
        action = html.escape(INVITE + token, quote=True)
        typed = ""

        def form(message: str = "", status: int = 200) -> HTMLResponse:
            page_ = INVITE_FORM if email else INVITE_OPEN_FORM
            return shell("Parola" if email else "Hesap", page_.format(message=message, action=action, min=MIN_PASSWORD,
                                                                     email=html.escape(email or typed, quote=True)), status)
        if request.method == "GET":
            return form()
        data = await request.form()
        password, again = str(data.get("password", "")), str(data.get("password2", ""))
        typed = str(data.get("email", "")).strip()[:200]
        if password != again:
            return form('<p class="err">İki parola aynı değil.</p>', 400)
        try:
            email = store.accept(token, password, email=None if email else typed)
        except ValueError as e:
            return form(f'<p class="err">{html.escape(str(e))}</p>', 400)
        scope = store.scope(email)
        response = RedirectResponse(PREFIX if scope == "masa" else OKU, status_code=303)
        set_session(response, email, request)
        return response

    async def me(request: Request):
        email = store.check(request.cookies.get(COOKIE))
        if not email:
            return JSONResponse({"error": "oturum yok"}, status_code=401, headers={"Cache-Control": "no-store"})
        return JSONResponse({"email": email, "name": store.display_name(email), "scope": store.scope(email),
                             "welcomed": store.welcomed(email), "place": store.place(email)},
                            headers={"Cache-Control": "no-store"})

    async def welcomed(request: Request):
        """S10 (c): karşılama sayfası görüldü."""
        email = store.check(request.cookies.get(COOKIE))
        if not email:
            return JSONResponse({"error": "oturum yok"}, status_code=401, headers={"Cache-Control": "no-store"})
        store.mark_welcomed(email)
        return JSONResponse({"ok": True}, headers={"Cache-Control": "no-store"})

    async def place(request: Request):
        """S10 (f): kaldığı yer (birim ve paragraf), hesaba bağlı."""
        email = store.check(request.cookies.get(COOKIE))
        if not email:
            return JSONResponse({"error": "oturum yok"}, status_code=401, headers={"Cache-Control": "no-store"})
        if request.method == "PUT":
            body = await request.json()
            if not body.get("birim"):
                return JSONResponse({"error": "birim gerekli"}, status_code=400, headers={"Cache-Control": "no-store"})
            store.set_place(email, body["birim"], body.get("paragraf"))
        return JSONResponse({"place": store.place(email)}, headers={"Cache-Control": "no-store"})

    async def logout(request: Request):
        store.close_session(request.cookies.get(COOKIE))
        response = RedirectResponse(f"{PREFIX}giris?cikis=1", status_code=303)
        response.delete_cookie(COOKIE, path=PREFIX)
        response.delete_cookie(COOKIE, path=COOKIE_PATH)
        return response

    from risale_mcp import masa                     # S7.2: ar-ge masası (okumalar, kararlar, notlar)
    return Starlette(routes=[Route("/_auth", check), Route(f"{PREFIX}giris", login, methods=["GET", "POST"]),
                             Route(f"{PREFIX}cikis", logout, methods=["GET", "POST"]), Route(f"{PREFIX}ben", me),
                             Route(INVITE + "{token}", invite, methods=["GET", "POST"]),
                             Route(f"{PREFIX}api/karsilandi", welcomed, methods=["POST"]),
                             Route(f"{PREFIX}api/yer", place, methods=["GET", "PUT"]),
                             *masa.routes(store, masa_store or masa.MasaStore())])


# ---------------------------------------------------------------- komut satırı

def _when(ts: float | None) -> str:
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(ts)) if ts else "—"


def _password(generate: bool) -> str:
    if generate:
        pw = secrets.token_urlsafe(12)
        print(f"parola: {pw}")
        return pw
    pw = getpass.getpass("parola: ")
    if len(pw) < MIN_PASSWORD:
        raise SystemExit(f"parola en az {MIN_PASSWORD} karakter olmalı")
    if pw != getpass.getpass("parola (tekrar): "):
        raise SystemExit("parolalar aynı değil")
    return pw


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="risalemcp.com/taslak/ girişi")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("serve")
    p.add_argument("--port", type=int, default=8009)
    p = sub.add_parser("davet", help="tek kullanımlık davet bağlantısı (7 gün; hesap varsa parola yenileme)")
    p.add_argument("email", nargs="?")
    p.add_argument("--acik", action="store_true", help="adressiz: e-postayı okuyucu yazar, yalnız yeni hesap açar")
    p.add_argument("--not", dest="label", help="hesabı tanımak için notunuz (ör. kimin için); okuyucu görmez")
    p.add_argument("--masa", action="store_true", help="yeni hesap ar-ge masasına da girer (varsayılan: yalnız /oku/)")
    p.add_argument("--name", help="masada işaretlerde görünecek ad (yoksa e-posta)")
    sub.add_parser("davetler", help="kullanılmamış, süresi dolmamış davetler")
    for name in ("add-user", "passwd"):
        p = sub.add_parser(name)
        p.add_argument("email")
        p.add_argument("--generate", action="store_true", help="parolayı üret ve göster")
        if name == "add-user":
            p.add_argument("--name", help="işaretlerde görünecek okuyucu adı (yoksa e-posta)")
            p.add_argument("--masa", action="store_true", help="ar-ge masasına da girer (varsayılan: yalnız /oku/)")
            p.add_argument("--oku", action="store_true", help=argparse.SUPPRESS)    # S10'dan önceki adı; artık varsayılan
    p = sub.add_parser("set-scope")
    p.add_argument("email")
    p.add_argument("scope", choices=SCOPES)
    p = sub.add_parser("set-label", help="hesaba yöneticinin notu")
    p.add_argument("email")
    p.add_argument("label")
    p = sub.add_parser("set-name")
    p.add_argument("email")
    p.add_argument("name")
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
    elif args.command == "davet" and (args.acik or not args.email):
        if not args.acik or args.email:
            raise SystemExit("ya e-posta adresi verin ya da --acik (adressiz davet); ikisi birden değil")
        token = store.invite(None, "masa" if args.masa else None, args.name, label=args.label)
        print(f"açık davet ({args.label or 'notsuz'}; yeni hesap, {'masa' if args.masa else 'oku'}, "
              f"{INVITE_DAYS} gün geçerli, tek kullanımlık; e-postayı okuyucu yazar):")
        print(f"{SITE}{INVITE}{token}")
    elif args.command == "davet":
        existed = store.exists(args.email)
        token = store.invite(args.email, "masa" if args.masa else None, args.name, label=args.label)
        if existed and args.masa:
            print("not: hesap zaten var, kapsamı değişmedi (set-scope ile değişir)")
        print(f"{'parola yenileme' if existed else 'yeni hesap'} ({norm_email(args.email)}, {INVITE_DAYS} gün geçerli, tek kullanımlık):")
        print(f"{SITE}{INVITE}{token}")
    elif args.command == "davetler":
        for d in store.invites():
            print(f"{d['email'] or '(açık davet)'}  {'yeni hesap, ' + d['scope'] if d['scope'] else 'parola yenileme'}"
                  f"{'  not: ' + d['label'] if d['label'] else ''}  verildi {_when(d['created'])}  biter {_when(d['expires'])}")
    elif args.command == "add-user":
        store.add_user(args.email, _password(args.generate), args.name, "masa" if args.masa else "oku")
        print(f"hesap açıldı: {norm_email(args.email)} ({'/taslak/ ve /oku/' if args.masa else 'yalnız /oku/'})")
    elif args.command == "set-scope":
        store.set_scope(args.email, args.scope)
        print(f"kapsam: {args.scope}")
    elif args.command == "passwd":
        store.set_password(args.email, _password(args.generate))
        print("parola değişti, açık oturumlar kapatıldı")
    elif args.command == "set-label":
        store.set_label(args.email, args.label)
        print("not kaydedildi")
    elif args.command == "set-name":
        store.set_name(args.email, args.name)
        print(f"ad: {store.display_name(args.email)}")
    elif args.command == "remove-user":
        from risale_mcp.masa import MasaStore
        n = MasaStore().forget(norm_email(args.email))
        store.remove_user(args.email)
        print(f"hesap silindi ({n} defter notu da silindi)")
    elif args.command == "revoke":
        print(f"{store.revoke(args.email)} oturum kapatıldı")
    elif args.command == "users":
        for u in store.users():
            lock = f" kilitli ({_when(u['locked_until'])}'e kadar)" if u["locked_until"] > time.time() else ""
            print(f"{u['email']}  ({u['name'] or 'adsız'}, {u['scope']}){'  not: ' + u['label'] if u['label'] else ''}  açıldı {_when(u['created'])}  son giriş {_when(u['last_login'])}{lock}")
    elif args.command == "sessions":
        for s in store.sessions():
            print(f"{s['email']}  açıldı {_when(s['created'])}  son görülme {_when(s['last_seen'])}  biter {_when(s['expires'])}")


if __name__ == "__main__":
    main()
