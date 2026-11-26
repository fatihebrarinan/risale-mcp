"""S12.2: sohbet hesapları, e-posta doğrulama kodu, sınırlar."""

import re

import pytest
from starlette.testclient import TestClient

from risale_mcp import sohbet_hesap as sh
from risale_mcp.sohbet_hesap import COOKIE, Config, IpLimiter, LogMailer, Refused, Store, TooSoon, build_app

PW = "uzun-bir-parola"


@pytest.fixture
def store(tmp_path):
    return Store(tmp_path / "sohbet.db")


@pytest.fixture
def mailer(tmp_path):
    return LogMailer(tmp_path / "eposta.log")


@pytest.fixture
def client(store, mailer):
    return TestClient(build_app(store, mailer, Config()), base_url="https://risalemcp.com", follow_redirects=False)


def last_code(mailer) -> str:
    return re.search(r"\b(\d{6})\b", mailer.sent[-1][2]).group(1)


def test_code_creates_account_then_resets_password(store):
    code, existing = store.new_code("Ali@Example.com", 100, now=1000)
    assert not existing and re.fullmatch(r"\d{6}", code)
    assert store.redeem("ali@example.com", code, PW, now=1010) is True
    assert store.login("ali@example.com", PW, now=1020) == (True, None)
    token = store.open_session("ali@example.com", now=1030)
    code, existing = store.new_code("ali@example.com", 100, now=2000)
    assert existing
    assert store.redeem("ali@example.com", code, "yeni-parola-123", now=2010) is False
    assert store.check(token, now=2020) is None                      # parola yenilenince oturumlar kapanır
    assert store.login("ali@example.com", "yeni-parola-123", now=2030)[0]


def test_code_single_use_expiry_and_attempts(store):
    code, _ = store.new_code("a@b.co", 100, now=1000)
    assert store.redeem("a@b.co", code, PW, now=1001)
    with pytest.raises(Refused):
        store.redeem("a@b.co", code, PW, now=1002)                   # bir kez
    code, _ = store.new_code("a@b.co", 100, now=2000)
    with pytest.raises(Refused, match="süresi"):
        store.redeem("a@b.co", code, PW, now=2000 + sh.CODE_MINUTES * 60 + 1)
    code, _ = store.new_code("a@b.co", 100, now=3000)
    wrong = f"{(int(code) + 1) % 10 ** 6:06d}"
    for _ in range(sh.CODE_ATTEMPTS):
        with pytest.raises(Refused):
            store.redeem("a@b.co", wrong, PW, now=3001)
    with pytest.raises(Refused, match="süresi"):
        store.redeem("a@b.co", code, PW, now=3002)                   # hak bitince doğru kod da geçmez


def test_short_password_does_not_spend_code(store):
    code, _ = store.new_code("a@b.co", 100, now=1000)
    with pytest.raises(Refused, match="en az"):
        store.redeem("a@b.co", code, "kisa", now=1001)
    assert store.redeem("a@b.co", code, PW, now=1002)


def test_send_limits(store):
    store.new_code("a@b.co", 100, now=1000)
    with pytest.raises(TooSoon):
        store.new_code("a@b.co", 100, now=1000 + sh.RESEND_SECONDS - 1)
    t = 1000
    for _ in range(sh.CODES_PER_EMAIL_DAY - 1):
        t += sh.RESEND_SECONDS + 1
        store.new_code("a@b.co", 100, now=t)
    with pytest.raises(Refused, match="bugün"):
        store.new_code("a@b.co", 100, now=t + sh.RESEND_SECONDS + 1)
    store.new_code("a@b.co", 100, now=t + 86400 + 1)                  # ertesi gün yeniden


def test_daily_site_limit(store):
    store.new_code("x1@b.co", 2, now=1000)
    store.new_code("x2@b.co", 2, now=1000)
    with pytest.raises(Refused, match="Bugünlük"):
        store.new_code("x3@b.co", 2, now=1000)


def test_ip_limiter_in_memory():
    lim = IpLimiter(per_hour=2)
    assert lim.allow("1.2.3.4", 0) and lim.allow("1.2.3.4", 1)
    assert not lim.allow("1.2.3.4", 2)
    assert lim.allow("5.6.7.8", 2)
    assert lim.allow("1.2.3.4", 3601)


def test_lockout(store):
    code, _ = store.new_code("a@b.co", 100, now=1000)
    store.redeem("a@b.co", code, PW, now=1000)
    for _ in range(sh.MAX_FAILURES):
        assert not store.login("a@b.co", "yanlis-parola", now=1100)[0]
    ok, msg = store.login("a@b.co", PW, now=1101)
    assert not ok and "Çok fazla" in msg


def test_web_flow(client, mailer):
    assert client.get("/sohbet/").headers["location"] == "/sohbet/kayit"
    r = client.post("/sohbet/kayit", data={"email": "Okur@Example.com"})
    assert r.status_code == 200 and "Kodu yazın" in r.text
    assert mailer.sent[-1][0] == "okur@example.com" and "hesap açmak" in mailer.sent[-1][2]
    r = client.post("/sohbet/kayit/kod", data={"email": "okur@example.com", "code": last_code(mailer),
                                                 "password": PW, "password2": PW})
    assert r.status_code == 303 and COOKIE in r.cookies
    assert "okur@example.com" in client.get("/sohbet/").text
    assert client.get("/sohbet/api/ben").json() == {"email": "okur@example.com"}
    r = client.post("/sohbet/cikis")
    assert r.headers["location"] == "/sohbet/giris?cikis=1"
    client.cookies.clear()
    assert client.get("/sohbet/api/ben").status_code == 401
    r = client.post("/sohbet/giris", data={"email": "okur@example.com", "password": PW, "next": "//kotu.example"})
    assert r.status_code == 303 and r.headers["location"] == "/sohbet/"           # açık yönlendirme yok


def test_web_does_not_reveal_account(client, store, mailer):
    code, _ = store.new_code("var@b.co", 100, now=1)
    store.redeem("var@b.co", code, PW, now=2)
    a = client.post("/sohbet/kayit", data={"email": "var@b.co"})
    b = client.post("/sohbet/kayit", data={"email": "yok@b.co"})
    strip = lambda t: t.replace("var@b.co", "X").replace("yok@b.co", "X")
    assert strip(a.text) == strip(b.text)                             # sayfa aynı; yalnız e-postanın metni farklı
    assert "parolasını yenilemek" in mailer.sent[-2][2] and "hesap açmak" in mailer.sent[-1][2]


def test_web_delete_account(client, store, mailer):
    client.post("/sohbet/kayit", data={"email": "sil@b.co"})
    client.post("/sohbet/kayit/kod", data={"email": "sil@b.co", "code": last_code(mailer), "password": PW,
                                           "password2": PW})
    assert client.post("/sohbet/hesap", data={"password": "yanlis-parola"}).status_code == 401
    assert store.exists("sil@b.co")
    r = client.post("/sohbet/hesap", data={"password": PW})
    assert r.status_code == 200 and not store.exists("sil@b.co")


def test_mail_failure_is_reported(store, tmp_path):
    class Broken:
        def send(self, *a):
            raise OSError("ağ yok")
    c = TestClient(build_app(store, Broken(), Config()), base_url="https://risalemcp.com")
    r = c.post("/sohbet/kayit", data={"email": "a@b.co"})
    assert r.status_code == 502 and "gönderilemedi" in r.text


def test_config_prefix_is_portable(store, mailer, monkeypatch):
    monkeypatch.setenv("SOHBET_PREFIX", "/")
    monkeypatch.setenv("SOHBET_NAME", "Yeni Ad")
    config = Config.from_env()
    assert config.prefix == "/"
    c = TestClient(build_app(store, mailer, config), base_url="https://yeni.example", follow_redirects=False)
    assert c.get("/").headers["location"] == "/kayit"
    assert "Yeni Ad" in c.get("/giris").text


def test_policy_pages_are_public(tmp_path):
    """S12.6: sohbetin kendi gizlilik ve şartlar sayfaları girişsiz açılır, yer tutucu kalmaz, iki dil birbirine
    bağlanır; hesap sayfaları onlara bağlanır (sitenin ana sayfalarına değil)."""
    from starlette.testclient import TestClient
    from risale_mcp.sohbet_hesap import DOCS, LogMailer, Store, build_app, Config
    web = TestClient(build_app(Store(tmp_path / "s.db"), LogMailer(tmp_path / "e.log"), Config()),
                     base_url="https://testserver")
    for path in DOCS:
        r = web.get(f"/sohbet/{path}")
        assert r.status_code == 200 and "{{" not in r.text, path
        if path != "hakkinda":
            assert "risalemcp.com/sohbet/" in r.text, path
    assert 'href="/sohbet/en/privacy"' in web.get("/sohbet/gizlilik").text
    assert "Anthropic" in web.get("/sohbet/en/privacy").text
    login = web.get("/sohbet/giris").text
    assert 'href="/sohbet/gizlilik"' in login and "/gizlilik.html" not in login


def test_support_address_and_reply_to(tmp_path, monkeypatch):
    """S13.15.4: destek adresi ve ad ayardan gelir (sayfaların iletişim satırı, e-postanın Reply-To'su)."""
    import json
    from risale_mcp.sohbet_hesap import DOCS, ScalewayMailer, doc_page
    monkeypatch.setenv("SOHBET_DESTEK", "destek@yeni.example")
    monkeypatch.setenv("SOHBET_NAME", "Yeni Ad")
    config = Config.from_env()
    for path in DOCS:
        page = doc_page(path, config)
        assert "destek@yeni.example" in page and "destek@risalemcp.com" not in page, path
        assert "Yeni Ad" in page and "{{" not in page, path
    sent = []

    class Response:
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self): return b"{}"

    monkeypatch.setattr(sh.urllib.request, "urlopen", lambda req, timeout: sent.append(req) or Response())
    ScalewayMailer("anahtar", "proje", "noreply@yeni.example", "Yeni Ad", config.support).send("a@b.co", "Konu", "Metin")
    body = json.loads(sent[0].data)
    assert body["from"] == {"email": "noreply@yeni.example", "name": "Yeni Ad"}
    assert body["additional_headers"] == [{"key": "Reply-To", "value": "destek@yeni.example"}]


def test_pwa_files_are_public(store, mailer, monkeypatch):
    """S13.15.4 (3): manifesto, servis çalışanı ve çevrimdışı sayfası girişsiz açılır, ön eke uyar; servis çalışanı
    yalnız sayfa açılışlarına karışır (cevap önbelleğe alınmaz)."""
    monkeypatch.setenv("SOHBET_PREFIX", "/")
    monkeypatch.setenv("SOHBET_NAME", "Yeni Ad")
    c = TestClient(build_app(store, mailer, Config.from_env()), base_url="https://yeni.example")
    m = c.get("/manifest.webmanifest")
    assert m.status_code == 200 and m.headers["content-type"].startswith("application/manifest+json")
    data = m.json()
    assert data["start_url"] == data["scope"] == "/" and data["short_name"] == "Yeni Ad"
    assert {i["purpose"] for i in data["icons"]} == {"any", "maskable"}
    sw = c.get("/sw.js")
    assert sw.status_code == 200 and '"/cevrimdisi"' in sw.text and 'mode !== "navigate"' in sw.text
    assert c.get("/cevrimdisi").status_code == 200
    assert 'rel="manifest" href="/manifest.webmanifest"' in c.get("/kayit").text


def test_code_message_has_no_link():
    """S13.15.4: doğrulama e-postasında bağlantı yok (yeni alan adına bağlantı Proton'un süzgecine takıldı)."""
    for existing in (False, True):
        subject, text = sh.code_message(Config(), "123456", existing)
        assert "123456" in subject and "123456" in text and "http" not in text and "www." not in text


def test_security_headers_404_and_card(client):
    """S13.15.4 (5): her yanıtta güvenlik başlıkları; bilinmeyen sayfa adla 404, API'de JSON; paylaşım kartı tam adresle."""
    r = client.get("/sohbet/kayit")
    csp = r.headers["content-security-policy"]
    assert "script-src 'self'" in csp and "frame-ancestors 'none'" in csp and "unsafe-eval" not in csp
    assert r.headers["x-content-type-options"] == "nosniff" and r.headers["x-frame-options"] == "DENY"
    assert 'property="og:image" content="https://risalemcp.com/sohbet/static/paylasim.jpg"' in r.text
    missing = client.get("/sohbet/olmayan-sayfa")
    assert missing.status_code == 404 and "Sayfa bulunamadı" in missing.text and "content-security-policy" in missing.headers
    api = client.get("/sohbet/api/olmayan")
    assert api.status_code == 404 and api.json() == {"error": "yok"}
