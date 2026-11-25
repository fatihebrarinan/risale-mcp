"""S12.2: sohbet sayfasının hesapları (`risalemcp.com/sohbet/`), e-posta doğrulama koduyla.

Kullanıcının kararları (2026-11-25): sohbet için hesap şart; herkes kendisi açar ama adresini e-postayla gelen kodla
doğrular (sınırsız hesap açılmasın). Hesaplar davetli bölümün hesapları değildir (`site_auth.py`): ayrı veritabanı
`data/sohbet.db`, ayrı çerez. Sebep: kendi açılan hesap `/taslak/` ya da `/oku/`'ya hiçbir yoldan giremesin; sohbet
ileride kendi alan adına taşınacak (S12.8); saklananlar ayrı anlatılır. Parola özeti ve kilit kuralı `auth.py`'dekidir.

Akış tektir, kayıt ve parola yenileme aynı yoldan: (1) adres yazılır, (2) adrese 6 haneli kod gider (10 dk, en çok
5 deneme), (3) kod ve yeni parola yazılır: hesap yoksa açılır, varsa parolası değişir (oturumları kapanır), giriş
yapılmış olur. Sayfa hesabın var olup olmadığını söylemez (adres yoklanamasın); yalnız e-postanın metni farklıdır.

Sınırlar (kötüye kullanım ve e-posta servisinin kotası): aynı adrese 60 sn'de bir, günde en çok 5 kod; aynı IP'den
saatte en çok 10 kod (IP yalnız bellekte sayılır, yazılmaz); bütün site günde en çok `SOHBET_GUNLUK_KOD` (200) kod.
Doğrulama hesapları zorlaştırır, engellemez: asıl sınır kişi başı soru kotası ve bütçe tavanıdır (S12.4).

Saklananlar (gizlilik politikası söyler, S12.6): e-posta, parola özeti, açılış ve son giriş zamanı, yanlış deneme
sayısı; bekleyen kodun yalnız özeti ve zamanları (kullanılınca ya da bir gün sonra silinir); oturumun özeti; günlük
gönderilen kod sayısı (adressiz). Hesabı kullanıcı kendisi siler (`hesap`).

Taşınabilirlik (S12.8): yol öneki, sitenin adresi, sayfadaki ad ve gönderen adres ayardandır (`Config`, ortam
değişkenleri `SOHBET_*`); sayfalarda sabit adres yok.

E-posta: `ScalewayMailer` (Scaleway Transactional Email, AB; `SCW_SECRET_KEY`, `SCW_PROJECT_ID`), geliştirmede
`LogMailer` (kodu dosyaya yazar; yalnız `--dev`). Anahtar yoksa servis `--dev` olmadan açılmaz.

    uv run python -m risale_mcp.sohbet_hesap serve [--port 8010] [--dev]
    uv run python -m risale_mcp.sohbet_hesap users | remove-user <e-posta> | revoke <e-posta>
"""

import argparse
import hashlib
import html
import json
import os
import re
import secrets
import sqlite3
import time
import urllib.request
from collections import defaultdict, deque
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import quote

from risale_mcp.auth import LOCK_SECONDS, MAX_FAILURES, check_password, hash_password
from risale_mcp.paths import DATA_DIR, INTERIM_DIR

DB = DATA_DIR / "sohbet.db"
COOKIE = "sohbet_oturum"
SESSION_DAYS = 30
MIN_PASSWORD = 10
CODE_MINUTES = 10
CODE_ATTEMPTS = 5
RESEND_SECONDS = 60
CODES_PER_EMAIL_DAY = 5
CODES_PER_IP_HOUR = 10
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_DUMMY = hash_password(secrets.token_hex(8))


@dataclass(frozen=True)
class Config:
    """Alan adına ve ada bağlı her şey (S12.8: taşınınca yalnız burası değişir)."""
    prefix: str = "/sohbet/"
    site: str = "https://risalemcp.com"
    name: str = "Risale MCP"
    sender: str = "noreply@risalemcp.com"
    daily_codes: int = 200

    @classmethod
    def from_env(cls) -> "Config":
        d = cls()
        prefix = os.environ.get("SOHBET_PREFIX", d.prefix)
        return cls(prefix="/" + prefix.strip("/") + "/" if prefix.strip("/") else "/",
                   site=os.environ.get("SOHBET_SITE", d.site).rstrip("/"),
                   name=os.environ.get("SOHBET_NAME", d.name),
                   sender=os.environ.get("SOHBET_FROM", d.sender),
                   daily_codes=int(os.environ.get("SOHBET_GUNLUK_KOD", d.daily_codes)))


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    email        TEXT PRIMARY KEY,
    password     TEXT NOT NULL,
    created      REAL NOT NULL,
    failures     INTEGER NOT NULL DEFAULT 0,
    locked_until REAL NOT NULL DEFAULT 0,
    last_login   REAL
);
CREATE TABLE IF NOT EXISTS codes (
    email     TEXT PRIMARY KEY,         -- bekleyen tek kod; yenisi eskisini geçersiz kılar
    digest    TEXT NOT NULL,            -- adres ve kodun SHA-256 özeti
    created   REAL NOT NULL,
    expires   REAL NOT NULL,
    attempts  INTEGER NOT NULL DEFAULT 0,
    sends     TEXT NOT NULL DEFAULT '[]'   -- son bir gündeki gönderim zamanları (adres başına sınır)
);
CREATE TABLE IF NOT EXISTS sessions (
    id        TEXT PRIMARY KEY,         -- çerezdeki jetonun SHA-256 özeti
    email     TEXT NOT NULL REFERENCES users(email) ON DELETE CASCADE,
    created   REAL NOT NULL,
    expires   REAL NOT NULL,
    last_seen REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS daily_codes (
    day TEXT PRIMARY KEY,               -- YYYY-AA-GG (UTC); adres yok
    n   INTEGER NOT NULL
);
"""


def norm_email(email: str) -> str:
    return email.strip().lower()


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


class Refused(ValueError):
    """Kullanıcıya gösterilecek ret (sınır, yanlış kod…)."""


class TooSoon(Refused):
    """Az önce kod gönderildi: kod sayfası açık kalır."""


class Store:
    def __init__(self, path: Path = DB) -> None:
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        with self._conn() as c:
            c.executescript(SCHEMA)
        path.chmod(0o600)

    def _conn(self) -> sqlite3.Connection:
        c = sqlite3.connect(self.path)
        c.row_factory = sqlite3.Row
        c.execute("PRAGMA foreign_keys = ON")
        return c

    def _run(self, sql: str, params: tuple = ()) -> list[sqlite3.Row]:
        with self._conn() as c:
            return c.execute(sql, params).fetchall()

    # ------------------------------------------------------------ hesaplar

    def exists(self, email: str) -> bool:
        return bool(self._run("SELECT 1 FROM users WHERE email = ?", (norm_email(email),)))

    def users(self) -> list[sqlite3.Row]:
        return self._run("SELECT email, created, last_login, failures, locked_until FROM users ORDER BY created")

    def remove_user(self, email: str) -> None:
        email = norm_email(email)
        self._run("DELETE FROM sessions WHERE email = ?", (email,))
        self._run("DELETE FROM codes WHERE email = ?", (email,))
        self._run("DELETE FROM users WHERE email = ?", (email,))

    def login(self, email: str, password: str, now: float | None = None) -> tuple[bool, str | None]:
        now = time.time() if now is None else now
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

    # ------------------------------------------------------------ doğrulama kodu

    def new_code(self, email: str, daily_limit: int, now: float | None = None) -> tuple[str, bool]:
        """Adrese yeni kod; (kod, hesap var mı). Sınır aşılırsa `Refused`. Kod yalnız özetiyle saklanır."""
        now = time.time() if now is None else now
        email = norm_email(email)
        if not EMAIL.match(email) or len(email) > 200:
            raise Refused("Geçerli bir e-posta adresi yazın.")
        self._run("DELETE FROM codes WHERE expires < ? AND created < ?", (now, now - 86400))
        rows = self._run("SELECT sends FROM codes WHERE email = ?", (email,))
        sends = [t for t in json.loads(rows[0]["sends"]) if t > now - 86400] if rows else []
        if sends and now - sends[-1] < RESEND_SECONDS:
            raise TooSoon(f"Az önce bir kod gönderildi. {int(RESEND_SECONDS - (now - sends[-1])) + 1} saniye sonra "
                          "yeniden isteyebilirsiniz.")
        if len(sends) >= CODES_PER_EMAIL_DAY:
            raise Refused("Bu adrese bugün çok kod gönderildi. Yarın yeniden deneyin.")
        day = time.strftime("%Y-%m-%d", time.gmtime(now))
        sent_today = self._run("SELECT n FROM daily_codes WHERE day = ?", (day,))
        if sent_today and sent_today[0]["n"] >= daily_limit:
            raise Refused("Bugünlük yeni hesap sınırına ulaşıldı. Yarın yeniden deneyin.")
        code = f"{secrets.randbelow(10 ** 6):06d}"
        self._run("INSERT INTO codes (email, digest, created, expires, attempts, sends) VALUES (?, ?, ?, ?, 0, ?) "
                  "ON CONFLICT(email) DO UPDATE SET digest = excluded.digest, created = excluded.created, "
                  "expires = excluded.expires, attempts = 0, sends = excluded.sends",
                  (email, _digest(email + ":" + code), now, now + CODE_MINUTES * 60, json.dumps(sends + [now])))
        self._run("INSERT INTO daily_codes (day, n) VALUES (?, 1) ON CONFLICT(day) DO UPDATE SET n = n + 1", (day,))
        return code, self.exists(email)

    def redeem(self, email: str, code: str, password: str, now: float | None = None) -> bool:
        """Kod doğruysa hesap açılır (yoksa) ya da parolası değişir (varsa; oturumları kapanır). Yeni hesapsa True."""
        now = time.time() if now is None else now
        email = norm_email(email)
        if len(password) < MIN_PASSWORD:
            raise Refused(f"Parola en az {MIN_PASSWORD} karakter olmalı.")
        rows = self._run("SELECT digest, expires, attempts FROM codes WHERE email = ?", (email,))
        if not rows or rows[0]["expires"] < now or rows[0]["attempts"] >= CODE_ATTEMPTS:
            raise Refused("Kodun süresi dolmuş ya da çok yanlış denendi. Yeni kod isteyin.")
        code = re.sub(r"\s", "", code)
        if not secrets.compare_digest(rows[0]["digest"], _digest(email + ":" + code)):
            self._run("UPDATE codes SET attempts = attempts + 1 WHERE email = ?", (email,))
            left = CODE_ATTEMPTS - rows[0]["attempts"] - 1
            raise Refused(f"Kod yanlış. {left} deneme hakkınız kaldı." if left else "Kod yanlış. Yeni kod isteyin.")
        # kod bir kez: aynı anda iki gönderimde ikincisi işlemez
        with self._conn() as c:
            if c.execute("UPDATE codes SET expires = 0, attempts = ? WHERE email = ? AND expires >= ?",
                         (CODE_ATTEMPTS, email, now)).rowcount != 1:
                raise Refused("Kodun süresi dolmuş ya da çok yanlış denendi. Yeni kod isteyin.")
        new = not self.exists(email)
        if new:
            self._run("INSERT INTO users (email, password, created, last_login) VALUES (?, ?, ?, ?)",
                      (email, hash_password(password), now, now))
        else:
            self._run("UPDATE users SET password = ?, failures = 0, locked_until = 0, last_login = ? WHERE email = ?",
                      (hash_password(password), now, email))
            self.revoke(email)
        return new

    # ------------------------------------------------------------ oturumlar

    def open_session(self, email: str, now: float | None = None) -> str:
        now = time.time() if now is None else now
        token = secrets.token_urlsafe(32)
        self._run("INSERT INTO sessions (id, email, created, expires, last_seen) VALUES (?, ?, ?, ?, ?)",
                  (_digest(token), norm_email(email), now, now + SESSION_DAYS * 86400, now))
        self._run("DELETE FROM sessions WHERE expires < ?", (now,))
        return token

    def check(self, token: str | None, now: float | None = None) -> str | None:
        if not token:
            return None
        now = time.time() if now is None else now
        rows = self._run("SELECT email, expires, last_seen FROM sessions WHERE id = ?", (_digest(token),))
        if not rows or rows[0]["expires"] < now:
            return None
        if now - rows[0]["last_seen"] > 600:
            self._run("UPDATE sessions SET last_seen = ? WHERE id = ?", (now, _digest(token)))
        return rows[0]["email"]

    def close_session(self, token: str | None) -> None:
        if token:
            self._run("DELETE FROM sessions WHERE id = ?", (_digest(token),))

    def revoke(self, email: str) -> int:
        n = len(self._run("SELECT 1 FROM sessions WHERE email = ?", (norm_email(email),)))
        self._run("DELETE FROM sessions WHERE email = ?", (norm_email(email),))
        return n


class IpLimiter:
    """IP başına saatlik kod sınırı; yalnız bellekte (IP yazılmaz). Servis yeniden başlayınca sıfırlanır."""

    def __init__(self, per_hour: int = CODES_PER_IP_HOUR) -> None:
        self.per_hour = per_hour
        self.hits: dict[str, deque] = defaultdict(deque)

    def allow(self, ip: str, now: float | None = None) -> bool:
        now = time.time() if now is None else now
        q = self.hits[ip]
        while q and q[0] < now - 3600:
            q.popleft()
        if len(q) >= self.per_hour:
            return False
        q.append(now)
        if len(self.hits) > 10000:                      # unutulan adresler birikmesin
            for k in [k for k, v in self.hits.items() if not v or v[-1] < now - 3600]:
                del self.hits[k]
        return True


# ---------------------------------------------------------------- e-posta

def code_message(config: Config, code: str, existing: bool) -> tuple[str, str]:
    """(konu, düz metin)."""
    if existing:
        purpose = f"{config.name} hesabınızın parolasını yenilemek için"
    else:
        purpose = f"{config.name} sohbet sayfasında hesap açmak için"
    subject = f"{config.name} doğrulama kodunuz: {code}"
    text = (f"Merhaba,\n\n{purpose} doğrulama kodunuz:\n\n    {code}\n\n"
            f"Kod {CODE_MINUTES} dakika geçerlidir. Bu isteği siz yapmadıysanız bu e-postayı yok sayın; "
            f"hesabınızda bir şey değişmez.\n\n{config.site}{config.prefix}\n")
    return subject, text


@dataclass
class LogMailer:
    """Geliştirme: e-postayı dosyaya yazar (gönderilmez)."""
    path: Path = INTERIM_DIR / "sohbet" / "eposta.log"
    sent: list = field(default_factory=list)

    def send(self, to: str, subject: str, text: str) -> None:
        self.sent.append((to, subject, text))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(f"--- {time.strftime('%F %T')} → {to}\n{subject}\n\n{text}\n")


@dataclass
class ScalewayMailer:
    """Scaleway Transactional Email (AB, fr-par). Belge: Transactional Email API v1alpha1, `POST …/emails`."""
    secret: str
    project: str
    sender: str
    name: str
    region: str = "fr-par"

    def send(self, to: str, subject: str, text: str) -> None:
        body = {"from": {"email": self.sender, "name": self.name}, "to": [{"email": to}], "subject": subject,
                "text": text, "project_id": self.project}
        req = urllib.request.Request(
            f"https://api.scaleway.com/transactional-email/v1alpha1/regions/{self.region}/emails",
            data=json.dumps(body).encode(), method="POST",
            headers={"X-Auth-Token": self.secret, "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=20) as r:
            r.read()


def mailer_from_env(config: Config, dev: bool):
    secret, project = os.environ.get("SCW_SECRET_KEY"), os.environ.get("SCW_PROJECT_ID")
    if secret and project and not dev:
        return ScalewayMailer(secret, project, config.sender, config.name)
    if dev:
        return LogMailer()
    raise SystemExit("SCW_SECRET_KEY ve SCW_PROJECT_ID yok: e-posta gönderilemez (geliştirmede --dev)")


# ---------------------------------------------------------------- web

SHELL = """<!doctype html><html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">
<meta name="referrer" content="no-referrer"><title>{title} · {name}</title><style>
:root {{ --bg: #fbfaf7; --fg: #1d1d1b; --muted: #6b6a66; --line: #dcd8cf; --card: #fff; --accent: #1f5c3f; --bad: #a3271f; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg: #161614; --fg: #e8e6e1; --muted: #9c9a94; --line: #34332f;
  --card: #1f1e1b; --accent: #7cc49d; --bad: #f08a80; }} }}
body {{ margin: 0; background: var(--bg); color: var(--fg); font: 16px/1.6 system-ui, sans-serif; }}
main {{ max-width: 400px; margin: 10vh auto; padding: 0 16px; }}
h1 {{ font-size: 1.25rem; margin: 0 0 4px; }} p {{ color: var(--muted); font-size: .92rem; }}
form {{ background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 16px; margin: 12px 0; }}
label {{ display: block; font-size: .88rem; margin: 0 0 10px; }}
input {{ display: block; width: 100%; box-sizing: border-box; margin-top: 4px; padding: 8px 10px; font: inherit;
  border: 1px solid var(--line); border-radius: 6px; background: var(--bg); color: var(--fg); }}
input.code {{ font-size: 1.4rem; letter-spacing: .3em; text-align: center; }}
button {{ width: 100%; padding: 9px; font: inherit; border: 0; border-radius: 6px; background: var(--accent); color: var(--bg); cursor: pointer; }}
button.link {{ background: none; color: var(--fg); text-decoration: underline; padding: 0; width: auto; }}
.err {{ color: var(--bad); }} .ok {{ color: var(--accent); }}
a {{ color: inherit; }} input[readonly] {{ color: var(--muted); }} .small {{ font-size: .82rem; }}
</style></head><body><main>
{body}
<p class="small"><a href="/">{site_host}</a> · <a href="/gizlilik.html">Gizlilik</a> · <a href="/kullanim-sartlari.html">Kullanım şartları</a></p>
</main></body></html>"""

LOGIN = """<h1>{name} · Sohbet</h1>
<p>Risale-i Nur hakkındaki sorularınızı, cevapları eserlerden alıntı ve kaynakla veren bir yapay zekâya sorun.</p>
{message}
<form method="post" action="{p}giris">
<input type="hidden" name="next" value="{next}">
<label>E-posta<input type="email" name="email" autocomplete="username" required value="{email}"></label>
<label>Parola<input type="password" name="password" autocomplete="current-password" required></label>
<button type="submit">Giriş</button>
</form>
<p>Hesabınız yok mu? <a href="{p}kayit">Hesap açın</a> · <a href="{p}kayit">Parolamı unuttum</a></p>"""

REGISTER = """<h1>Hesap açın</h1>
<p>E-posta adresinizi yazın; adresinize 6 haneli bir doğrulama kodu gönderelim. Hesabınız varsa aynı yoldan yeni parola
belirlersiniz.</p>
{message}
<form method="post" action="{p}kayit">
<label>E-posta<input type="email" name="email" autocomplete="email" required value="{email}"></label>
<button type="submit">Kod gönder</button>
</form>
<p><a href="{p}giris">Giriş sayfasına dön</a></p>"""

CODE_FORM = """<h1>Kodu yazın</h1>
<p><strong>{email_text}</strong> adresine bir doğrulama kodu gönderdik (birkaç dakika sürebilir; gelmezse istenmeyen
e-posta klasörüne bakın). Kodu ve kendinize bir parola yazın. Hesabınız varsa parolanız yenilenir.</p>
{message}
<form method="post" action="{p}kayit/kod">
<input type="hidden" name="email" value="{email}">
<label>Doğrulama kodu<input class="code" name="code" inputmode="numeric" autocomplete="one-time-code" maxlength="7" required></label>
<label>Parola (en az {min} karakter)<input type="password" name="password" autocomplete="new-password" minlength="{min}" required></label>
<label>Parola (tekrar)<input type="password" name="password2" autocomplete="new-password" minlength="{min}" required></label>
<button type="submit">Doğrula ve gir</button>
<p class="small">Devam ederek <a href="/kullanim-sartlari.html">kullanım şartlarını</a> ve
<a href="/gizlilik.html">gizlilik politikasını</a> kabul etmiş olursunuz.</p>
</form>
<form method="post" action="{p}kayit" style="border:0;padding:0;background:none">
<input type="hidden" name="email" value="{email}"><button class="link" type="submit">Yeni kod gönder</button>
</form>"""

HOME = """<h1>{name} · Sohbet</h1>
<p class="ok">Giriş yaptınız: {email}</p>
<p>Sohbet sayfası hazırlanıyor.</p>
<form method="post" action="{p}cikis"><button type="submit">Çıkış</button></form>
<p><a href="{p}hesap">Hesabımı sil</a></p>"""

DELETE = """<h1>Hesabı sil</h1>
<p>Hesabınız ({email}) ve oturumlarınız kalıcı olarak silinir. Konuşmalarınız zaten sunucuda saklanmıyor.</p>
{message}
<form method="post" action="{p}hesap">
<label>Parolanız<input type="password" name="password" autocomplete="current-password" required></label>
<button type="submit">Hesabımı kalıcı olarak sil</button>
</form>
<p><a href="{p}">Vazgeç</a></p>"""


def build_app(store: Store, mailer, config: Config = Config(), limiter: IpLimiter | None = None, extra_routes=()):
    from starlette.applications import Starlette
    from starlette.requests import Request
    from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse
    from starlette.routing import Route

    p = config.prefix
    limiter = limiter or IpLimiter()
    host = config.site.split("://", 1)[-1]
    esc = lambda s: html.escape(str(s), quote=True)

    def shell(title: str, body: str, status: int = 200) -> HTMLResponse:
        return HTMLResponse(SHELL.format(title=esc(title), name=esc(config.name), body=body, site_host=esc(host)),
                            status_code=status, headers={"Cache-Control": "no-store", "Referrer-Policy": "no-referrer"})

    def err(text: str) -> str:
        return f'<p class="err">{esc(text)}</p>'

    def safe_next(target: str | None) -> str:
        if target and target.startswith(p) and not target.startswith("//") and "\\" not in target:
            return target
        return p

    def secure(request: Request) -> bool:
        return request.headers.get("x-forwarded-proto", request.url.scheme) == "https"

    def client_ip(request: Request) -> str:
        return request.client.host if request.client else "?"

    def signed_in(response, email: str, request: Request):
        response.set_cookie(COOKIE, store.open_session(email), max_age=SESSION_DAYS * 86400, path=p,
                            httponly=True, secure=secure(request), samesite="lax")
        return response

    def user(request: Request) -> str | None:
        return store.check(request.cookies.get(COOKIE))

    def code_page(email: str, message: str = "", status: int = 200) -> HTMLResponse:
        return shell("Kod", CODE_FORM.format(p=p, email=esc(email), email_text=esc(email), message=message,
                                             min=MIN_PASSWORD), status)

    async def home(request: Request):
        email = user(request)
        if not email:
            return RedirectResponse(f"{p}giris", status_code=302)
        return shell("Sohbet", HOME.format(p=p, name=esc(config.name), email=esc(email)))

    async def login(request: Request):
        if request.method == "GET":
            if user(request):
                return RedirectResponse(safe_next(request.query_params.get("next")), status_code=302)
            msg = '<p class="ok">Oturum kapatıldı.</p>' if request.query_params.get("cikis") else ""
            return shell("Giriş", LOGIN.format(p=p, name=esc(config.name), message=msg, email="",
                                               next=esc(safe_next(request.query_params.get("next")))))
        form = await request.form()
        email, password = str(form.get("email", ""))[:200], str(form.get("password", ""))
        ok, error = store.login(email, password)
        if not ok:
            return shell("Giriş", LOGIN.format(p=p, name=esc(config.name), message=err(error), email=esc(email),
                                               next=esc(safe_next(str(form.get("next", ""))))), 401)
        return signed_in(RedirectResponse(safe_next(str(form.get("next", ""))), status_code=303), email, request)

    async def register(request: Request):
        if request.method == "GET":
            return shell("Hesap", REGISTER.format(p=p, message="", email=""))
        form = await request.form()
        email = norm_email(str(form.get("email", ""))[:200])
        if not EMAIL.match(email):
            return shell("Hesap", REGISTER.format(p=p, message=err("Geçerli bir e-posta adresi yazın."),
                                                  email=esc(email)), 400)
        if not limiter.allow(client_ip(request)):
            return shell("Hesap", REGISTER.format(p=p, message=err("Bu bağlantıdan çok kod istendi. Bir saat sonra "
                                                                   "yeniden deneyin."), email=esc(email)), 429)
        try:
            code, existing = store.new_code(email, config.daily_codes)
        except TooSoon as e:                             # kod zaten gönderilmiş: kod sayfası açık kalsın
            return code_page(email, err(str(e)), 429)
        except Refused as e:
            return shell("Hesap", REGISTER.format(p=p, message=err(str(e)), email=esc(email)), 429)
        subject, text = code_message(config, code, existing)
        try:
            mailer.send(email, subject, text)
        except Exception:                                # servis hatası: kullanıcıya sade ileti, ayrıntı günlükte
            import logging
            logging.exception("sohbet: doğrulama e-postası gönderilemedi")
            return shell("Hesap", REGISTER.format(p=p, message=err("E-posta şu an gönderilemedi. Biraz sonra yeniden "
                                                                   "deneyin."), email=esc(email)), 502)
        return code_page(email)

    async def redeem(request: Request):
        form = await request.form()
        email = norm_email(str(form.get("email", ""))[:200])
        password, again = str(form.get("password", "")), str(form.get("password2", ""))
        if password != again:
            return code_page(email, err("İki parola aynı değil."), 400)
        try:
            store.redeem(email, str(form.get("code", ""))[:20], password)
        except Refused as e:
            return code_page(email, err(str(e)), 400)
        return signed_in(RedirectResponse(p, status_code=303), email, request)

    async def logout(request: Request):
        store.close_session(request.cookies.get(COOKIE))
        response = RedirectResponse(f"{p}giris?cikis=1", status_code=303)
        response.delete_cookie(COOKIE, path=p)
        return response

    async def delete(request: Request):
        email = user(request)
        if not email:
            return RedirectResponse(f"{p}giris", status_code=302)
        if request.method == "GET":
            return shell("Hesabı sil", DELETE.format(p=p, email=esc(email), message=""))
        form = await request.form()
        ok, error = store.login(email, str(form.get("password", "")))
        if not ok:
            return shell("Hesabı sil", DELETE.format(p=p, email=esc(email), message=err(error)), 401)
        store.remove_user(email)
        response = shell("Hesap silindi", f'<h1>Hesabınız silindi</h1><p><a href="{p}kayit">Yeni hesap açın</a></p>')
        response.delete_cookie(COOKIE, path=p)
        return response

    async def me(request: Request):
        email = user(request)
        if not email:
            return JSONResponse({"error": "oturum yok"}, status_code=401, headers={"Cache-Control": "no-store"})
        return JSONResponse({"email": email}, headers={"Cache-Control": "no-store"})

    return Starlette(routes=[
        Route(p, home), Route(f"{p}giris", login, methods=["GET", "POST"]),
        Route(f"{p}kayit", register, methods=["GET", "POST"]), Route(f"{p}kayit/kod", redeem, methods=["POST"]),
        Route(f"{p}cikis", logout, methods=["POST"]), Route(f"{p}hesap", delete, methods=["GET", "POST"]),
        Route(f"{p}api/ben", me), *extra_routes])


# ---------------------------------------------------------------- komut satırı

def _when(ts: float | None) -> str:
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(ts)) if ts else "—"


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="sohbet sayfasının hesapları (S12.2)")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("serve")
    p.add_argument("--port", type=int, default=8010)
    p.add_argument("--dev", action="store_true", help="e-posta gönderilmez, data/interim/sohbet/eposta.log'a yazılır")
    sub.add_parser("users")
    for name in ("remove-user", "revoke"):
        sub.add_parser(name).add_argument("email")
    args = parser.parse_args(argv)
    from risale_mcp.env import load_env
    load_env()
    store = Store()
    if args.command == "serve":
        import uvicorn
        config = Config.from_env()
        uvicorn.run(build_app(store, mailer_from_env(config, args.dev), config), host="127.0.0.1", port=args.port,
                    proxy_headers=True, forwarded_allow_ips="127.0.0.1", access_log=False)
    elif args.command == "users":
        rows = store.users()
        for u in rows:
            lock = f" kilitli ({_when(u['locked_until'])}'e kadar)" if u["locked_until"] > time.time() else ""
            print(f"{u['email']}  açıldı {_when(u['created'])}  son giriş {_when(u['last_login'])}{lock}")
        print(f"{len(rows)} hesap")
    elif args.command == "remove-user":
        store.remove_user(args.email)
        print("hesap silindi")
    elif args.command == "revoke":
        print(f"{store.revoke(args.email)} oturum kapatıldı")


if __name__ == "__main__":
    main()
