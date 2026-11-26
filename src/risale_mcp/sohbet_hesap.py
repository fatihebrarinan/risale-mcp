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
gönderilen kod sayısı (adressiz); sohbetin kullanım satırları (`usage`, soru ve cevap yok; hesap silinince adsız);
S13.1'den beri saklanan konuşmalar (`conversations`, `turns`; ayar `users.keep_history`, varsayılan açık; yalnız
sahibine gösterilir, ekip okumaz; kullanıcı tek tek ya da hepsini siler, hesapla birlikte hepsi gider).
Hesabı kullanıcı kendisi siler (`hesap`).

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
ASSETS = Path(__file__).parent / "sohbet_assets"
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
CREATE TABLE IF NOT EXISTS usage (      -- S12.3: soru başına bir satır (`sohbet.log_usage`); soru ve cevap yok
    ts          REAL NOT NULL,
    email       TEXT,                   -- hesap silinince NULL
    model       TEXT NOT NULL,
    rounds      INTEGER NOT NULL,       -- model çağrısı
    tools       INTEGER NOT NULL,       -- araç çağrısı
    input       INTEGER NOT NULL,
    output      INTEGER NOT NULL,
    cache_write INTEGER NOT NULL,
    cache_read  INTEGER NOT NULL,
    cost        REAL NOT NULL,          -- $, yaklaşık (asıl fatura Console'da)
    seconds     REAL NOT NULL,
    sources     INTEGER,                -- cevaptaki kaynak sayısı
    problems    INTEGER,                -- düzeltmeden sonra da denetimden geçmeyen
    corrected   INTEGER,                -- düzeltmeye gitti mi
    outcome     TEXT NOT NULL,          -- done | error | cancelled
    fixed       INTEGER,                -- S12.9: sunucunun yerini düzelttiği işaret
    dropped     INTEGER,                -- kimliği olmadığı için silinen alıntısız işaret
    leaks       INTEGER,                -- düz metne yazılmış, silinen kimlik
    paragraphs  INTEGER,                -- cevabın düz yazı paragrafları
    unmarked    INTEGER                 -- içinde hiç işaret olmayanlar (düz cümledeki iddianın sıklığı için)
);
CREATE INDEX IF NOT EXISTS usage_ts ON usage(ts);
CREATE TABLE IF NOT EXISTS feedback (   -- S12.12: cevaba oy (1/-1), S13.4: tıklayınca, not sonra aynı satırda; soru ve cevap yalnız kullanıcı kutuyu işaretlediyse
    ts        REAL NOT NULL,
    email     TEXT,                     -- hesap silinince NULL (not, soru ve cevap da silinir; oy kalır)
    vote      INTEGER NOT NULL,         -- 1 | -1
    note      TEXT,
    question  TEXT,
    answer    TEXT,                     -- okuyucunun gördüğü cevap ve kaynakları, düz metin
    model     TEXT
);
CREATE INDEX IF NOT EXISTS feedback_ts ON feedback(ts);
CREATE TABLE IF NOT EXISTS conversations (   -- S13.1: saklanan konuşmalar; yalnız sahibine gösterilir, ekip okumaz
    id       TEXT PRIMARY KEY,          -- rastgele (paylaşım bağlantısı da ileride bunu kullanabilir)
    email    TEXT NOT NULL REFERENCES users(email) ON DELETE CASCADE,
    title    TEXT NOT NULL,             -- ilk sorudan kısaltılır; kullanıcı değiştirebilir
    created  REAL NOT NULL,
    updated  REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS conversations_user ON conversations(email, updated);
CREATE TABLE IF NOT EXISTS turns (
    conversation TEXT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    n         INTEGER NOT NULL,         -- konuşmadaki sıra, 0'dan
    ts        REAL NOT NULL,
    question  TEXT NOT NULL,
    raw       TEXT NOT NULL,            -- modelin cevabı, işaretler düzeltilmiş (sonraki soruda geçmiş olarak gider)
    markdown  TEXT NOT NULL,            -- okuyucunun gördüğü cevap
    sources   TEXT NOT NULL,            -- Kaynaklar, JSON
    corrected INTEGER NOT NULL DEFAULT 0,
    feedback  INTEGER,                  -- okuyucunun oyu (1 | -1); geri bildirimin kendisi `feedback` tablosunda
    PRIMARY KEY (conversation, n)
);
"""
# Sonradan eklenen sütunlar: eski veritabanına eklenir (CREATE TABLE IF NOT EXISTS var olan tabloyu değiştirmez).
ADDED_COLUMNS = {"usage": {**{c: "INTEGER" for c in ("fixed", "dropped", "leaks", "paragraphs", "unmarked")},
                           "libraries": "TEXT"},     # S13.17: sorunun açık öbür kütüphaneleri ("tefsir,hadis")
                 # S13.1: konuşmaları hesapta sakla (varsayılan açık; kapalıyken konuşma yalnız tarayıcıda)
                 "users": {"keep_history": "INTEGER NOT NULL DEFAULT 1"},
                 # S13.3: cevabın adımları ("… okunuyor"), JSON; S13.4 (c): çağrılan araçlar (sonraki soruda modele), JSON
                 "turns": {"steps": "TEXT", "reads": "TEXT",
                           "mode": "TEXT",           # S13.12: turun kipi (serbest, tarama…)
                           "libraries": "TEXT"}}     # S13.17: turda açık öbür kütüphaneler, JSON


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
            for table, columns in ADDED_COLUMNS.items():
                have = {r["name"] for r in c.execute(f"PRAGMA table_info({table})")}
                for column, kind in columns.items():
                    if column not in have:
                        c.execute(f"ALTER TABLE {table} ADD COLUMN {column} {kind}")
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
        self._run("DELETE FROM users WHERE email = ?", (email,))      # konuşmalar ve turları da (ON DELETE CASCADE)
        self._run("DELETE FROM conversations WHERE email = ?", (email,))   # yabancı anahtar kapalı eski kayıtlara karşı
        self._run("UPDATE usage SET email = NULL WHERE email = ?", (email,))    # maliyet sayımı kalır, adsız
        self._run("UPDATE feedback SET email = NULL, note = NULL, question = NULL, answer = NULL WHERE email = ?",
                  (email,))                                                  # oy kalır, yazdıkları silinir

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

# S13.3: hesap sayfaları. Kayıt ve giriş tanıtımlıdır (solda platformun tanıtımı, arka planda yavaş kayan sekiz köşeli
# yıldız deseni; telefonda üstte), öbürleri (kod, hesabı silme) yalnız formdur. Desen satır içi SVG'dir: dışarıya istek yok.
SHELL = """<!doctype html><html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">
<meta name="referrer" content="no-referrer"><title>{title} · {name}</title><style>{style}</style></head>
<body class="{kind}"><div class="sayfa">
{hero}<main><div class="kart">
{body}
</div>
<p class="alt-not"><a href="/">{site_host}</a> · <a href="{p}gizlilik">Gizlilik</a> · <a href="{p}sartlar">Kullanım şartları</a></p>
</main></div></body></html>"""

_STAR = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='64' height='64' viewBox='0 0 64 64'%3E"
         "%3Cg fill='none' stroke='white' stroke-width='1'%3E%3Crect x='18' y='18' width='28' height='28'/%3E"
         "%3Crect x='18' y='18' width='28' height='28' transform='rotate(45 32 32)'/%3E"
         "%3Ccircle cx='32' cy='32' r='5'/%3E%3Cpath d='M0 32h8M56 32h8M32 0v8M32 56v8'/%3E%3C/g%3E%3C/svg%3E")

SHELL_STYLE = """
:root { --bg: #fbfaf7; --fg: #1d1d1b; --muted: #6b6a66; --line: #dcd8cf; --card: #fff; --accent: #1f5c3f; --bad: #a3271f;
  --hero: #17402d; --hero2: #0f2c1f; --gold: #d9b45a; --serif: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif; }
@media (prefers-color-scheme: dark) { :root { --bg: #161614; --fg: #e8e6e1; --muted: #9c9a94; --line: #34332f;
  --card: #1f1e1b; --accent: #7cc49d; --bad: #f08a80; --hero: #12301f; --hero2: #0a1d13; } }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--fg); font: 16px/1.6 system-ui, sans-serif; }
a { color: inherit; }
.sayfa { min-height: 100dvh; display: flex; }
main { flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 32px 18px; }
.kart { width: 100%; max-width: 400px; }
h1 { font-size: 1.4rem; margin: 0 0 6px; } p { color: var(--muted); font-size: .92rem; }
form { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 18px; margin: 14px 0; }
label { display: block; font-size: .88rem; margin: 0 0 12px; }
input { display: block; width: 100%; margin-top: 4px; padding: 10px 12px; font: inherit; border: 1px solid var(--line);
  border-radius: 8px; background: var(--bg); color: var(--fg); }
input:focus { outline: 2px solid var(--accent); outline-offset: -1px; }
input.code { font-size: 1.4rem; letter-spacing: .3em; text-align: center; }
button { width: 100%; padding: 10px; font: inherit; font-weight: 600; border: 0; border-radius: 8px; background: var(--accent);
  color: var(--bg); cursor: pointer; }
button:hover { filter: brightness(1.08); }
button.link { background: none; color: var(--fg); text-decoration: underline; padding: 0; width: auto; font-weight: 400; }
form.yalin { border: 0; padding: 0; background: none; }
.err { color: var(--bad); } .ok { color: var(--accent); }
input[readonly] { color: var(--muted); } .small { font-size: .82rem; }
.gecis { text-align: center; font-size: .95rem; color: var(--fg); }
.gecis a { color: var(--accent); font-weight: 600; }
.alt-not { font-size: .8rem; text-align: center; margin-top: 18px; }

/* tanıtım */
.tanitim { position: relative; overflow: hidden; flex: 0 0 52%; color: #f3efe4; padding: 56px 56px 40px;
  display: flex; flex-direction: column; justify-content: center;
  background: radial-gradient(120% 90% at 15% 10%, #24603f 0%, var(--hero) 45%, var(--hero2) 100%); }
.tanitim::before { content: ""; position: absolute; inset: -64px; background-image: url("STAR"); background-size: 64px 64px;
  opacity: .07; animation: kay 90s linear infinite; pointer-events: none; }
.tanitim::after { content: ""; position: absolute; width: 520px; height: 520px; right: -180px; bottom: -220px; border-radius: 50%;
  background: radial-gradient(circle, rgba(217, 180, 90, .22), transparent 65%); pointer-events: none; }
@keyframes kay { to { transform: translate(64px, 64px); } }
@media (prefers-reduced-motion: reduce) { .tanitim::before { animation: none; } }
.tanitim > * { position: relative; z-index: 1; max-width: 560px; }
.ust-yazi { font-size: .8rem; letter-spacing: .12em; text-transform: uppercase; color: var(--gold); margin: 0 0 18px;
  font-weight: 600; }
.tanitim h2 { font-family: var(--serif); font-weight: 600; font-size: clamp(1.9rem, 3.2vw, 2.7rem); line-height: 1.18;
  margin: 0 0 16px; color: #fbf8ef; }
.tanitim .giris-yazi { color: #d7dfd6; font-size: 1.05rem; line-height: 1.65; margin: 0 0 28px; }
.ozellikler { list-style: none; padding: 0; margin: 0 0 30px; display: grid; gap: 16px; }
.ozellikler li { display: flex; gap: 14px; align-items: flex-start; }
.ozellikler svg { flex: none; width: 34px; height: 34px; padding: 7px; border-radius: 9px; background: rgba(255, 255, 255, .08);
  stroke: var(--gold); fill: none; stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round; }
.ozellikler strong { display: block; color: #fbf8ef; font-size: .98rem; }
.ozellikler span { color: #c3ccc2; font-size: .9rem; }
.ornek { background: rgba(255, 255, 255, .06); border: 1px solid rgba(255, 255, 255, .12); border-radius: 14px;
  padding: 16px 18px; backdrop-filter: blur(2px); }
.ornek .soru { display: inline-block; background: rgba(255, 255, 255, .12); border-radius: 10px 10px 2px 10px;
  padding: 5px 12px; font-size: .9rem; color: #fbf8ef; margin: 0 0 10px; }
.ornek blockquote { margin: 0; padding: 4px 0 4px 14px; border-left: 3px solid var(--gold); font-family: var(--serif);
  font-size: 1.1rem; color: #fbf8ef; }
.ornek sup { color: var(--gold); font-family: system-ui, sans-serif; font-size: .7em; margin-left: 3px; }
.ornek .kaynak { margin: 10px 0 0; font-size: .8rem; color: #b7c2b6; }
.ornek .etiket { float: right; font-size: .7rem; letter-spacing: .08em; text-transform: uppercase; color: #9fb09f; }
.uyari-not { font-size: .8rem; color: #a9b6a8; margin: 22px 0 0; }
@media (max-width: 899.98px) {
  .sayfa { flex-direction: column; }
  .tanitim { flex: none; padding: 36px 22px 30px; }
  .tanitim h2 { font-size: 1.75rem; }
  .ozellikler { gap: 12px; margin-bottom: 0; }
  .ornek, .uyari-not { display: none; }
  main { justify-content: flex-start; padding-top: 24px; }
}
@media (max-width: 599.98px) {      /* telefonda form ilk ekranda görünsün: özellikler gizli, tanıtım kısa */
  .tanitim { padding: 28px 20px 24px; }
  .ust-yazi { margin-bottom: 10px; }
  .tanitim h2 { font-size: 1.5rem; margin-bottom: 10px; }
  .tanitim .giris-yazi { font-size: .95rem; margin: 0; }
  .ozellikler { display: none; }
}
""".replace("STAR", _STAR)

_ICONS = {
    "kaynak": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/>'
              '<path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/><path d="M9 8h7M9 12h5"/></svg>',
    "kulliyat": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4h4v16H4zM10 4h4v16h-4z"/><path d="m16 5 3.8-1 3 15.5-3.8 1z"/></svg>',
    "dil": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 21l1.9-5.4A8 8 0 1 1 21 12z"/>'
           '<path d="M9 10h6M9 14h4"/></svg>',
}

HERO = """<aside class="tanitim" aria-label="Tanıtım">
<p class="ust-yazi">{name} · Sohbet</p>
<h2>Risale-i Nur'a sorun,<br>cevabı kaynağıyla okuyun.</h2>
<p class="giris-yazi">Sorularınızı Bediüzzaman Said Nursî'nin eserlerinden cevaplayan bir yapay zekâ. Dayandığı her söz
eserlerden alıntıdır; alıntılar eserlerin metniyle denetlenir, yeri ve kaynağıyla gösterilir.</p>
<ul class="ozellikler">
<li>{i_kaynak}<div><strong>Her alıntı kaynağıyla</strong><span>Alıntıya dokunun, metni eserdeki yerinde, öncesi ve
sonrasıyla okuyun.</span></div></li>
<li>{i_kulliyat}<div><strong>Bütün külliyat</strong><span>Sözler'den Lâhikalara, Arapça eserlerden Hizblere; âyetler, hadisler
ve eski kelimelerin lügat anlamı.</span></div></li>
<li>{i_dil}<div><strong>Bugünün diliyle sorun</strong><span>Metindeki kelimeyi bilmeseniz de anlamca arar; konunun geçtiği
yerleri bulur.</span></div></li>
</ul>
<div class="ornek"><span class="etiket">Örnek</span>
<p class="soru">Ümitsizliğe düşen birine ne söylenir?</p>
<blockquote>Karanlıklı ye'simi, nurlu bir ricâya çevirdi.<sup>[1]</sup></blockquote>
<p class="kaynak">[1] Lem'alar › Yirmialtıncı Lem'a › Üçüncü Ricâ · Kaynak: e-Risale</p>
</div>
<p class="uyari-not">Cevaplar yapay zekânındır; tefsir ve fetva değildir, müellife mal edilmez. Ücretsizdir.</p>
</aside>
"""


# S12.6: sohbet sayfasının kendi gizlilik politikası ve kullanım şartları (kullanıcının kararı, 2026-11-25: sitenin
# ana sayfaları eklentilerin dizin başvurularında gösterildi, onlara dokunulmaz; sohbet kendi alan adına taşınınca
# sayfaları da onunla gider). Metinler `sohbet_assets/`'te; tarih yayında değişir.
POLICY_DATE = ("25 Kasım 2026", "25 November 2026")
DOCS = {   # yol: (dosya, dil, başlık, öbür dildeki yol)
    "gizlilik": ("gizlilik.html", "tr", "Gizlilik", "en/privacy"),
    "sartlar": ("sartlar.html", "tr", "Kullanım şartları", "en/terms"),
    "en/privacy": ("en-privacy.html", "en", "Privacy", "gizlilik"),
    "en/terms": ("en-terms.html", "en", "Terms of use", "sartlar"),
}
DOC_SHELL = """<!doctype html><html lang="{lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><meta name="referrer" content="no-referrer">
<title>{title} · {name}</title><style>
:root {{ --bg: #fbfaf7; --fg: #1d1d1b; --muted: #6b6a66; --line: #dcd8cf; --accent: #1f5c3f; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg: #161614; --fg: #e8e6e1; --muted: #9c9a94; --line: #34332f;
  --accent: #7cc49d; }} }}
body {{ margin: 0; background: var(--bg); color: var(--fg); font: 16px/1.65 system-ui, sans-serif; }}
main {{ max-width: 720px; margin: 0 auto; padding: 24px 18px 48px; }}
nav {{ display: flex; justify-content: space-between; gap: 12px; font-size: .9rem; margin-bottom: 18px; }}
h1 {{ font-size: 1.5rem; margin: 0 0 4px; }} h2 {{ font-size: 1.08rem; margin: 1.6em 0 .3em; }}
.lead {{ color: var(--muted); margin-top: 0; }} a {{ color: var(--accent); }} li {{ margin: .3em 0; }}
footer {{ margin-top: 40px; border-top: 1px solid var(--line); padding-top: 12px; font-size: .85rem; color: var(--muted); }}
footer a {{ color: inherit; }}
</style></head><body><main>
<nav><a href="{p}">{back}</a><a href="{p}{other}" hreflang="{other_lang}">{other_label}</a></nav>
{body}
<footer>{name} · <a href="{p}">{chat}</a> · <a href="{p}{privacy}">{privacy_label}</a> · <a href="{p}{terms}">{terms_label}</a> ·
<a href="mailto:destek@risalemcp.com">destek@risalemcp.com</a></footer>
</main></body></html>"""


def doc_page(path: str, config: "Config") -> str:
    """Sohbet sayfasının gizlilik politikası ya da kullanım şartları (girişsiz)."""
    file, lang, title, other = DOCS[path]
    host = config.site.split("://", 1)[-1]
    body = ((ASSETS / file).read_text(encoding="utf-8").replace("{{P}}", html.escape(config.prefix))
            .replace("{{HOST}}", html.escape(host)).replace("{{DATE}}", POLICY_DATE[0])
            .replace("{{DATE_EN}}", POLICY_DATE[1]))
    tr = lang == "tr"
    return DOC_SHELL.format(lang=lang, title=html.escape(title), name=html.escape(config.name), p=html.escape(config.prefix),
                            body=body, back="← Sohbete dön" if tr else "← Back to the chat", other=other,
                            other_lang="en" if tr else "tr", other_label="English" if tr else "Türkçe",
                            chat="Sohbet" if tr else "Chat", privacy="gizlilik" if tr else "en/privacy",
                            terms="sartlar" if tr else "en/terms", privacy_label="Gizlilik" if tr else "Privacy",
                            terms_label="Kullanım şartları" if tr else "Terms of use")

LOGIN = """<h1>Giriş yapın</h1>
<p>Tekrar hoş geldiniz.</p>
{message}
<form method="post" action="{p}giris">
<input type="hidden" name="next" value="{next}">
<label>E-posta<input type="email" name="email" autocomplete="username" required value="{email}"></label>
<label>Parola<input type="password" name="password" autocomplete="current-password" required></label>
<button type="submit">Giriş yap</button>
</form>
<p class="gecis">Hesabınız yok mu? <a href="{p}kayit">Hesap oluşturun</a></p>
<p class="gecis small"><a href="{p}kayit">Parolamı unuttum</a></p>"""

REGISTER = """<h1>Hesap oluşturun</h1>
<p>E-posta adresinizi yazın; adresinize 6 haneli bir doğrulama kodu gönderelim. Parolanızı unuttuysanız da aynı yoldan
yenisini belirlersiniz.</p>
{message}
<form method="post" action="{p}kayit">
<label>E-posta<input type="email" name="email" autocomplete="email" required value="{email}"></label>
<button type="submit">Kod gönder</button>
</form>
<p class="gecis">Zaten hesabınız var mı? <a href="{p}giris">Giriş yapın</a></p>"""

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
<p class="small">Devam ederek sohbet sayfasının <a href="{p}sartlar">kullanım şartlarını</a> ve
<a href="{p}gizlilik">gizlilik politikasını</a> kabul etmiş olursunuz.</p>
</form>
<form method="post" action="{p}kayit" class="yalin">
<input type="hidden" name="email" value="{email}"><button class="link" type="submit">Yeni kod gönder</button>
</form>"""

HOME = """<h1>{name} · Sohbet</h1>
<p class="ok">Giriş yaptınız: {email}</p>
<p>Sohbet sayfası hazırlanıyor.</p>
<form method="post" action="{p}cikis"><button type="submit">Çıkış</button></form>
<p><a href="{p}hesap">Hesabımı sil</a></p>"""

DELETE = """<h1>Hesabı sil</h1>
<p>Hesabınız ({email}), oturumlarınız ve saklanan bütün konuşmalarınız kalıcı olarak silinir.</p>
{message}
<form method="post" action="{p}hesap">
<label>Parolanız<input type="password" name="password" autocomplete="current-password" required></label>
<button type="submit">Hesabımı kalıcı olarak sil</button>
</form>
<p><a href="{p}">Vazgeç</a></p>"""


def build_app(store: Store, mailer, config: Config = Config(), limiter: IpLimiter | None = None, extra_routes=(),
              home_page=None):
    """`home_page(request, email)`: girişli kullanıcının ana sayfası (S12.3: sohbet); yoksa yer tutucu sayfa."""
    from starlette.applications import Starlette
    from starlette.requests import Request
    from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse
    from starlette.routing import Route

    p = config.prefix
    limiter = limiter or IpLimiter()
    host = config.site.split("://", 1)[-1]
    esc = lambda s: html.escape(str(s), quote=True)

    hero = HERO.format(name=esc(config.name), **{f"i_{k}": v for k, v in _ICONS.items()})

    def shell(title: str, body: str, status: int = 200, intro: bool = False) -> HTMLResponse:
        return HTMLResponse(SHELL.format(title=esc(title), name=esc(config.name), body=body, site_host=esc(host), p=p,
                                         style=SHELL_STYLE, hero=hero if intro else "",
                                         kind="tanitimli" if intro else "yalin-sayfa"),
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
        if not email:                    # S13.3: ilk gelen hesap oluşturma sayfasını görür (altta girişe geçiş)
            return RedirectResponse(f"{p}kayit", status_code=302)
        if home_page:
            return home_page(request, email)
        return shell("Sohbet", HOME.format(p=p, name=esc(config.name), email=esc(email)))

    async def login(request: Request):
        if request.method == "GET":
            if user(request):
                return RedirectResponse(safe_next(request.query_params.get("next")), status_code=302)
            msg = '<p class="ok">Oturum kapatıldı.</p>' if request.query_params.get("cikis") else ""
            return shell("Giriş", LOGIN.format(p=p, name=esc(config.name), message=msg, email="",
                                               next=esc(safe_next(request.query_params.get("next")))), intro=True)
        form = await request.form()
        email, password = str(form.get("email", ""))[:200], str(form.get("password", ""))
        ok, error = store.login(email, password)
        if not ok:
            return shell("Giriş", LOGIN.format(p=p, name=esc(config.name), message=err(error), email=esc(email),
                                               next=esc(safe_next(str(form.get("next", ""))))), 401, intro=True)
        return signed_in(RedirectResponse(safe_next(str(form.get("next", ""))), status_code=303), email, request)

    async def register(request: Request):
        if request.method == "GET":
            return shell("Hesap", REGISTER.format(p=p, message="", email=""), intro=True)
        form = await request.form()
        email = norm_email(str(form.get("email", ""))[:200])
        if not EMAIL.match(email):
            return shell("Hesap", REGISTER.format(p=p, message=err("Geçerli bir e-posta adresi yazın."),
                                                  email=esc(email)), 400, intro=True)
        if not limiter.allow(client_ip(request)):
            return shell("Hesap", REGISTER.format(p=p, message=err("Bu bağlantıdan çok kod istendi. Bir saat sonra "
                                                                   "yeniden deneyin."), email=esc(email)), 429, intro=True)
        try:
            code, existing = store.new_code(email, config.daily_codes)
        except TooSoon as e:                             # kod zaten gönderilmiş: kod sayfası açık kalsın
            return code_page(email, err(str(e)), 429)
        except Refused as e:
            return shell("Hesap", REGISTER.format(p=p, message=err(str(e)), email=esc(email)), 429, intro=True)
        subject, text = code_message(config, code, existing)
        try:
            mailer.send(email, subject, text)
        except Exception:                                # servis hatası: kullanıcıya sade ileti, ayrıntı günlükte
            import logging
            logging.exception("sohbet: doğrulama e-postası gönderilemedi")
            return shell("Hesap", REGISTER.format(p=p, message=err("E-posta şu an gönderilemedi. Biraz sonra yeniden "
                                                                   "deneyin."), email=esc(email)), 502, intro=True)
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

    async def document(request: Request):
        return HTMLResponse(doc_page(request.url.path[len(p):].rstrip("/"), config),
                            headers={"Cache-Control": "public, max-age=3600", "Referrer-Policy": "no-referrer"})

    async def me(request: Request):
        email = user(request)
        if not email:
            return JSONResponse({"error": "oturum yok"}, status_code=401, headers={"Cache-Control": "no-store"})
        return JSONResponse({"email": email}, headers={"Cache-Control": "no-store"})

    return Starlette(routes=[
        Route(p, home), Route(f"{p}giris", login, methods=["GET", "POST"]),
        Route(f"{p}kayit", register, methods=["GET", "POST"]), Route(f"{p}kayit/kod", redeem, methods=["POST"]),
        Route(f"{p}cikis", logout, methods=["POST"]), Route(f"{p}hesap", delete, methods=["GET", "POST"]),
        Route(f"{p}api/ben", me), *[Route(f"{p}{path}", document) for path in DOCS], *extra_routes])


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
