"""S11: site yazılarının taslaklarını web'de düzenlemek (kullanıcının kararları, 2026-11-23: yalnız kendisi düzenler,
Markdown yeter, telefona da uysun).

Yazının aslı depodaki dosyadır (`docs/yenilikler/<ad>.md`, `docs/calismalar/<ad>.md`); deploy onu sunucuya da götürür.
Web'de yapılan düzeltmeler taslak süresince bu sunucuda `data/yazilar.db`'de durur: her "Kaydet" yeni bir sürümdür
(silinmez, geri dönülür). Her sürüm hangi depo metninden başladığını (`taban`, metnin özeti) taşır. Kurallar:

- Düzenleyici web sürümü varsa onu, yoksa depodaki dosyayı açar. Depodaki dosya web sürümüyle aynıysa (geri çekilip
  deploy edilmiş) ya da web sürümü onun üstüne yazılmışsa sorun yoktur; depodaki dosya web düzeltmeleri sürerken
  başka türlü değiştiyse **çakışma** vardır: düzenleyici uyarır, iki metni de gösterir, kullanıcı birini seçer.
- Yalnız taslak (`durum: taslak`) yazılar düzenlenir; yayımlanmış yazı depoda düzeltilir.
- Kaydetme yetkisi yalnız listedeki hesaplardadır (`yazilar izin <e-posta>`); masanın öbür hesapları göremez.
- Yerel taraf: `scripts/site-uret.py cek` web sürümlerini SSH ile alır (`yazilar disa`) ve depodaki dosyaya yazar;
  `yayinla` ve zamanlı yayın bunu kendiliğinden yapar.

Görünüş sitedeki programla çizilir (`scripts/site-uret.py`, `preview_html`): sunucuda da durur, aynı sayfa çıkar.

    uv run python -m risale_mcp.yazilar izin <e-posta>       # sunucuda: kaydetme yetkisi ver (geri: --kaldir)
    uv run python -m risale_mcp.yazilar liste                # web sürümleri
    uv run python -m risale_mcp.yazilar disa                 # son web sürümleri, JSON (site-uret.py cek okur)
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sqlite3
import sys
import time
from pathlib import Path

from risale_mcp.paths import DATA_DIR, ROOT

DB = DATA_DIR / "yazilar.db"
API = "/taslak/api/yazi"
KINDS = ("yenilikler", "calismalar")
NAME = re.compile(r"^(yenilikler|calismalar)/([0-9a-z][0-9a-z-]{0,120})$")
MAX_TEXT = 400_000

SCHEMA = """
CREATE TABLE IF NOT EXISTS surumler (
    ad     TEXT NOT NULL,            -- yenilikler/2026-11-23-lugat
    n      INTEGER NOT NULL,         -- 1, 2, …
    metin  TEXT NOT NULL,
    sha    TEXT NOT NULL,            -- metnin özeti
    taban  TEXT NOT NULL,            -- başladığı depo metninin özeti
    kim    TEXT NOT NULL,
    zaman  REAL NOT NULL,
    PRIMARY KEY (ad, n)
);
CREATE TABLE IF NOT EXISTS duzenleyiciler (
    email  TEXT PRIMARY KEY,
    zaman  REAL NOT NULL
);
"""


def sha(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]


def repo_path(ad: str, root: Path = ROOT) -> Path:
    m = NAME.match(ad or "")
    if not m:
        raise ValueError("yazı adı tanınmadı")
    return root / "docs" / m[1] / f"{m[2]}.md"


def is_draft(text: str) -> bool:
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return bool(m and re.search(r"^durum:\s*taslak\s*$", m[1], re.M))


class YaziStore:
    def __init__(self, path: Path = DB, root: Path = ROOT) -> None:
        self.path, self.root = path, root
        self._conn: sqlite3.Connection | None = None

    @property
    def conn(self) -> sqlite3.Connection:
        """İlk kullanımda açılır (servis kurulurken dosya yaratılmasın)."""
        if self._conn is None:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            new = not self.path.exists()
            self._conn = sqlite3.connect(self.path, check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
            self._conn.executescript(SCHEMA)
            if new:
                self.path.chmod(0o600)
        return self._conn

    # ---------------------------------------------------------------- yetki
    def allow(self, email: str, on: bool = True) -> None:
        email = email.strip().lower()
        with self.conn:
            if on:
                self.conn.execute("INSERT OR REPLACE INTO duzenleyiciler VALUES (?, ?)", (email, time.time()))
            else:
                self.conn.execute("DELETE FROM duzenleyiciler WHERE email = ?", (email,))

    def can_edit(self, email: str | None) -> bool:
        return bool(email) and self.conn.execute("SELECT 1 FROM duzenleyiciler WHERE email = ?",
                                                 (email.strip().lower(),)).fetchone() is not None

    # ---------------------------------------------------------------- metin
    def repo_text(self, ad: str) -> str | None:
        p = repo_path(ad, self.root)
        return p.read_text(encoding="utf-8") if p.exists() else None

    def latest(self, ad: str) -> sqlite3.Row | None:
        return self.conn.execute("SELECT * FROM surumler WHERE ad = ? ORDER BY n DESC LIMIT 1", (ad,)).fetchone()

    def history(self, ad: str) -> list[dict]:
        return [{"n": r["n"], "zaman": r["zaman"], "boy": len(r["metin"])} for r in
                self.conn.execute("SELECT n, zaman, metin FROM surumler WHERE ad = ? ORDER BY n DESC", (ad,))]

    def version(self, ad: str, n: int) -> str | None:
        r = self.conn.execute("SELECT metin FROM surumler WHERE ad = ? AND n = ?", (ad, n)).fetchone()
        return r["metin"] if r else None

    def state(self, ad: str) -> dict:
        """Düzenleyicinin açacağı metin: web sürümü (varsa) ya da depodaki dosya; çakışma varsa ikisi de."""
        repo = self.repo_text(ad)
        if repo is None:
            raise LookupError("yazı depoda yok")
        last = self.latest(ad)
        out = {"ad": ad, "depo_sha": sha(repo), "taslak": is_draft(repo), "gecmis": self.history(ad)}
        if last is None or last["sha"] == sha(repo):
            return out | {"metin": repo, "kaynak": "depo", "surum": last["n"] if last else 0}
        out |= {"metin": last["metin"], "kaynak": "web", "surum": last["n"], "zaman": last["zaman"]}
        if last["taban"] != sha(repo):
            out |= {"cakisma": True, "depo_metin": repo}
        return out

    def save(self, ad: str, text: str, email: str, base: str | None = None) -> dict:
        """Yeni sürüm. `base`: düzenleyicinin açtığı depo metninin özeti (çakışmayı kullanıcı çözdüyse bugünkü depo)."""
        repo = self.repo_text(ad)
        if repo is None:
            raise LookupError("yazı depoda yok")
        if not is_draft(repo):
            raise PermissionError("yalnız taslak yazılar web'de düzenlenir")
        if len(text) > MAX_TEXT:
            raise ValueError("metin çok uzun")
        text = text.replace("\r\n", "\n")
        last = self.latest(ad)
        if last and last["metin"] == text:
            return {"surum": last["n"], "degismedi": True}
        if last is None and text == repo:
            return {"surum": 0, "degismedi": True}
        # taban: depo web sürümüne yetiştiyse (geri çekilip deploy edildi) bugünkü depo, değilse sürdürülen taban
        taban = base or (last["taban"] if last and last["sha"] != sha(repo) else sha(repo))
        n = (last["n"] if last else 0) + 1
        with self.conn:
            self.conn.execute("INSERT INTO surumler VALUES (?, ?, ?, ?, ?, ?, ?)",
                              (ad, n, text, sha(text), taban, email, time.time()))
        return {"surum": n, "zaman": time.time()}

    def export(self) -> dict:
        """Her yazının son web sürümü (yerel `site-uret.py cek` okur)."""
        rows = self.conn.execute("SELECT s.* FROM surumler s JOIN (SELECT ad, MAX(n) AS n FROM surumler GROUP BY ad) m"
                                 " ON s.ad = m.ad AND s.n = m.n ORDER BY s.ad")
        out = {r["ad"]: {"metin": r["metin"], "sha": r["sha"], "taban": r["taban"], "surum": r["n"],
                         "zaman": r["zaman"]} for r in rows}
        for ad, v in out.items():           # yerel metin bunlardan biriyse ileri sarmak güvenlidir
            v["bilinen"] = sorted({x for r in self.conn.execute("SELECT sha, taban FROM surumler WHERE ad = ?", (ad,))
                                   for x in (r["sha"], r["taban"])})
        return out


# ---------------------------------------------------------------- görünüş (sitedeki program)

_SITE = None


def _site(root: Path = ROOT):
    global _SITE
    if _SITE is None:
        spec = importlib.util.spec_from_file_location("site_uret", root / "scripts" / "site-uret.py")
        mod = importlib.util.module_from_spec(spec)
        sys.modules["site_uret"] = mod
        spec.loader.exec_module(mod)
        _SITE = mod
    return _SITE


def preview(ad: str, text: str, root: Path = ROOT) -> str:
    m = NAME.match(ad or "")
    if not m:
        raise ValueError("yazı adı tanınmadı")
    try:
        return _site(root).preview_html(m[1], m[2], text)
    except SystemExit as e:                  # üst bilgi hatası: sitedeki program sys.exit ile söyler
        raise ValueError(str(e)) from None


# ---------------------------------------------------------------- yollar

def routes(auth, store: YaziStore) -> list:
    """Starlette yolları (`site_auth.build_app` ekler); oturum `site_auth`'tan, yetki `duzenleyiciler`den."""
    from starlette.requests import Request
    from starlette.responses import JSONResponse
    from starlette.routing import Route

    from risale_mcp.site_auth import COOKIE

    H = {"Cache-Control": "no-store"}

    def editor(request: Request) -> str | None:
        email = auth.check(request.cookies.get(COOKIE))
        return email if email and auth.scope(email) == "masa" and store.can_edit(email) else None

    def err(msg: str, status: int) -> JSONResponse:
        return JSONResponse({"error": msg}, status_code=status, headers=H)

    async def get(request: Request):
        if not editor(request):
            return err("yetki yok", 403)
        ad = request.query_params.get("ad", "")
        try:
            if n := request.query_params.get("surum"):
                text = store.version(ad, int(n))
                return JSONResponse({"metin": text}, headers=H) if text is not None else err("sürüm yok", 404)
            return JSONResponse(store.state(ad), headers=H)
        except (ValueError, LookupError) as e:
            return err(str(e), 404)

    async def put(request: Request):
        email = editor(request)
        if not email:
            return err("yetki yok", 403)
        body = await request.json()
        try:
            return JSONResponse(store.save(body.get("ad", ""), str(body.get("metin", "")), email, body.get("taban")),
                                headers=H)
        except PermissionError as e:
            return err(str(e), 403)
        except (ValueError, LookupError) as e:
            return err(str(e), 400)

    async def show(request: Request):
        if not editor(request):
            return err("yetki yok", 403)
        body = await request.json()
        try:
            return JSONResponse({"html": preview(body.get("ad", ""), str(body.get("metin", "")))}, headers=H)
        except ValueError as e:
            return JSONResponse({"hata": str(e)}, headers=H)

    async def me(request: Request):
        return JSONResponse({"duzenleyebilir": editor(request) is not None}, headers=H)

    return [Route(API, get, methods=["GET"]), Route(API, put, methods=["PUT"]),
            Route(API + "/onizle", show, methods=["POST"]), Route(API + "/yetki", me, methods=["GET"])]


# ---------------------------------------------------------------- komut satırı

def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("izin", help="kaydetme yetkisi")
    p.add_argument("email")
    p.add_argument("--kaldir", action="store_true")
    sub.add_parser("liste")
    sub.add_parser("disa")
    a = ap.parse_args(argv)
    store = YaziStore()
    if a.cmd == "izin":
        store.allow(a.email, not a.kaldir)
        print(("kaldırıldı: " if a.kaldir else "izin verildi: ") + a.email)
    elif a.cmd == "liste":
        for ad, v in store.export().items():
            print(f"{ad}: sürüm {v['surum']}, {time.strftime('%Y-%m-%d %H:%M', time.localtime(v['zaman']))}")
    else:
        print(json.dumps(store.export(), ensure_ascii=False))


if __name__ == "__main__":
    main()
