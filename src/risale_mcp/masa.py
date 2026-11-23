"""S7.2: ar-ge masasının sunucu tarafı: okuma görevleri, okuyucunun kararları, notlar (kullanıcının kararları,
2026-11-21; PLANLAR S7 "Ar-ge masasının ekleri").

Giriş servisinin (`site_auth.py`) aynı uygulamasında çalışır: hesap ve oturum ondan gelir. Ayrı veritabanı
`data/masa.db`. Kurallar:
- **Kararlar ve notlar silinmez.** Karar her değişiklikte yeni satırdır (sonuncusu geçerli, geçmiş durur); not geri
  çekilir (`geri_cekildi`), silinmez; notun her olayı `not_gecmisi`'ne yazılır.
- **Okuyucunun adı dışarı çıkmaz.** Dışa aktarmada okuyucu sabit numarasıyla (`okuyucu_no`) görünür, e-postası yok.
- **Kör okumada taraflar sunucuda saklı.** Görevin `gizli`'si (A/B'nin hangi taslak olduğu) okuyucu "bitir" diyene kadar
  verilmez; bitirince döner.
- **S10: notun iki yeri** (kullanıcının kararları, 2026-11-22). Platformdan yazılan not okuyucunun **kişisel
  defteridir** (`kapsam = 'defter'`): yalnız yazanı görür (yönetici de görmez), yazan düzenler ve gerçekten siler (geçmişi
  tutulmaz), dışa aktarmaya ve "notlarımla düzelt"e girmez, hesap silinince silinir. "Notlarım" bütün birimlerdekini
  verir, Word dosyası olarak da (`docx_yaz.py`). S10'dan önce yazılmış notlar **ar-ge kaydıdır** (`kapsam = 'arge'`):
  yukarıdaki silinmez kuralı onlarındır, masa `?arge=1` ile görür. (İleride "geliştirme için gönder": defter notu ar-ge
  notu olur; "Fikirler".)
- **Makine erişimi jetonla.** Taslak sunucusu görev açar (`POST /taslak/api/gorev`) ve sonuçları alır
  (`GET /taslak/api/disa`); jetonun yalnız SHA-256 özeti saklanır (`masa token --new`).

    uv run python -m risale_mcp.masa token --new        # sunucuda: makine jetonu (bir kez gösterilir)
    uv run python -m risale_mcp.masa gorevler           # görevler ve durumları
"""

from __future__ import annotations

import argparse
import hashlib
import json
import secrets
import sqlite3
import time
from pathlib import Path

from risale_mcp.paths import DATA_DIR

DB = DATA_DIR / "masa.db"
API = "/taslak/api/"

SCHEMA = """
CREATE TABLE IF NOT EXISTS okuyucular (
    email    TEXT PRIMARY KEY,
    no       INTEGER UNIQUE NOT NULL,      -- dışa aktarmadaki sabit numara (ad yayımlanmaz)
    rol      TEXT NOT NULL DEFAULT 'okuyucu',   -- okuyucu | katkici | ehil | yonetici (ileride)
    created  REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS okumalar (
    id          TEXT PRIMARY KEY,          -- ör. tur-30-D5-kabul
    tur         TEXT NOT NULL,             -- ab | tek | d5 | ornek
    birim       TEXT,
    baslik      TEXT NOT NULL,
    aciklama    TEXT,
    sayfa       TEXT,                      -- /taslak/ altındaki okuma sayfası
    atanan      TEXT,                      -- e-posta; NULL: herkes
    durum       TEXT NOT NULL DEFAULT 'bekliyor',   -- bekliyor | suruyor | bitti
    olusturuldu REAL NOT NULL,
    basladi     REAL,
    bitti       REAL,
    veri        TEXT,                      -- yerler, sayılar (JSON)
    gizli       TEXT,                      -- kör eşleme (JSON); bitene kadar okuyucuya gitmez
    kaynak      TEXT                       -- deney kimliği (deneyler defteri)
);
CREATE TABLE IF NOT EXISTS kararlar (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    okuma    TEXT NOT NULL REFERENCES okumalar(id),
    yer      TEXT NOT NULL,
    okuyucu  TEXT NOT NULL,
    veri     TEXT NOT NULL,                -- {secim, yeter, gerekce, …} (JSON)
    zaman    REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS notlar (
    id            TEXT PRIMARY KEY,
    birim         TEXT NOT NULL,
    surum         INTEGER,                 -- yayın sürümü (S7.1)
    paragraf      TEXT,                    -- kalıcı paragraf kimliği
    secici        TEXT,                    -- {exact, prefix, suffix} (W3C TextQuoteSelector gibi)
    okuyucu       TEXT NOT NULL,
    tur           TEXT NOT NULL DEFAULT 'not',   -- hata | soru | oneri | kaynak | not
    metin         TEXT NOT NULL,
    durum         TEXT NOT NULL DEFAULT 'acik',  -- acik | islendi | kapandi | geri_cekildi
    isleyen_surum INTEGER,
    okuma         TEXT,                    -- hangi okumada yazıldı
    zaman         REAL NOT NULL,
    guncellendi   REAL NOT NULL,
    kapsam        TEXT NOT NULL DEFAULT 'arge',   -- arge (S10'dan önce; silinmez) | defter (okuyucunun kişisel defteri)
    etiket        TEXT,                    -- birimin adı ("Bakara 40–46"; Notlarım için)
    baglam        TEXT                     -- paragrafın ilk sözleri (Notlarım için)
);
CREATE TABLE IF NOT EXISTS not_gecmisi (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    not_id  TEXT NOT NULL,
    zaman   REAL NOT NULL,
    kim     TEXT NOT NULL,
    olay    TEXT NOT NULL,                 -- yazildi | durum | metin
    veri    TEXT
);
CREATE TABLE IF NOT EXISTS jetonlar (
    ozet     TEXT PRIMARY KEY,
    ad       TEXT NOT NULL,
    created  REAL NOT NULL
);
"""


def _sha(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


class MasaStore:
    def __init__(self, path: Path = DB) -> None:
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        with self._conn() as c:
            c.executescript(SCHEMA)
            cols = {r[1] for r in c.execute("PRAGMA table_info(notlar)")}
            for col in ("kapsam TEXT NOT NULL DEFAULT 'arge'", "etiket TEXT", "baglam TEXT"):   # S10'dan önceki dosya
                if col.split()[0] not in cols:
                    c.execute(f"ALTER TABLE notlar ADD COLUMN {col}")
        path.chmod(0o600)

    def _conn(self) -> sqlite3.Connection:
        c = sqlite3.connect(self.path)
        c.row_factory = sqlite3.Row
        c.execute("PRAGMA foreign_keys = ON")
        return c

    def _run(self, sql: str, params: tuple = ()) -> list[sqlite3.Row]:
        with self._conn() as c:
            return c.execute(sql, params).fetchall()

    # ------------------------------------------------------------ okuyucular ve jetonlar

    def reader_no(self, email: str) -> int:
        rows = self._run("SELECT no FROM okuyucular WHERE email = ?", (email,))
        if rows:
            return rows[0]["no"]
        n = (self._run("SELECT max(no) AS m FROM okuyucular")[0]["m"] or 0) + 1
        self._run("INSERT INTO okuyucular (email, no, created) VALUES (?, ?, ?)", (email, n, time.time()))
        return n

    def new_token(self, name: str) -> str:
        token = secrets.token_urlsafe(32)
        self._run("INSERT INTO jetonlar (ozet, ad, created) VALUES (?, ?, ?)", (_sha(token), name, time.time()))
        return token

    def check_token(self, token: str | None) -> str | None:
        if not token:
            return None
        rows = self._run("SELECT ad FROM jetonlar WHERE ozet = ?", (_sha(token),))
        return rows[0]["ad"] if rows else None

    # ------------------------------------------------------------ görevler

    def add_task(self, task: dict) -> bool:
        """Görev açar; aynı kimlik varsa dokunmaz (False). Alanlar: id, tur, baslik, [birim, aciklama, sayfa, atanan,
        veri, gizli, kaynak]."""
        if self._run("SELECT 1 FROM okumalar WHERE id = ?", (task["id"],)):
            return False
        self._run("INSERT INTO okumalar (id, tur, birim, baslik, aciklama, sayfa, atanan, olusturuldu, veri, gizli, "
                  "kaynak) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (task["id"], task["tur"], task.get("birim"), task["baslik"], task.get("aciklama"), task.get("sayfa"),
                   task.get("atanan"), time.time(), json.dumps(task.get("veri") or {}, ensure_ascii=False),
                   json.dumps(task["gizli"], ensure_ascii=False) if task.get("gizli") is not None else None,
                   task.get("kaynak")))
        return True

    def _visible(self, row: sqlite3.Row, email: str) -> bool:
        return row["atanan"] in (None, "", email)

    def tasks_for(self, email: str) -> list[dict]:
        out = []
        for r in self._run("SELECT * FROM okumalar ORDER BY olusturuldu DESC"):
            if not self._visible(r, email):
                continue
            n = self._run("SELECT count(DISTINCT yer) AS n FROM kararlar WHERE okuma = ? AND okuyucu = ?",
                          (r["id"], email))[0]["n"]
            veri = json.loads(r["veri"] or "{}")
            out.append({"id": r["id"], "tur": r["tur"], "birim": r["birim"], "baslik": r["baslik"],
                        "aciklama": r["aciklama"], "sayfa": r["sayfa"], "durum": r["durum"],
                        "yer": len(veri.get("yerler") or []), "dakika": veri.get("dakika"), "karar": n,
                        "olusturuldu": r["olusturuldu"], "bitti": r["bitti"]})
        return out

    def task(self, tid: str, email: str) -> dict | None:
        rows = self._run("SELECT * FROM okumalar WHERE id = ?", (tid,))
        if not rows or not self._visible(rows[0], email):
            return None
        r = rows[0]
        latest = {}
        for k in self._run("SELECT yer, veri, zaman FROM kararlar WHERE okuma = ? AND okuyucu = ? ORDER BY id",
                           (tid, email)):
            latest[k["yer"]] = json.loads(k["veri"]) | {"zaman": k["zaman"]}
        out = {"id": r["id"], "tur": r["tur"], "birim": r["birim"], "baslik": r["baslik"], "durum": r["durum"],
               "veri": json.loads(r["veri"] or "{}"), "kararlar": latest}
        if r["durum"] == "bitti" and r["gizli"]:
            out["gizli"] = json.loads(r["gizli"])
        return out

    def add_decision(self, tid: str, yer: str, email: str, veri: dict) -> bool:
        rows = self._run("SELECT * FROM okumalar WHERE id = ?", (tid,))
        if not rows or not self._visible(rows[0], email):
            return False
        self.reader_no(email)
        self._run("INSERT INTO kararlar (okuma, yer, okuyucu, veri, zaman) VALUES (?, ?, ?, ?, ?)",
                  (tid, yer, email, json.dumps(veri, ensure_ascii=False), time.time()))
        if rows[0]["durum"] == "bekliyor":
            self._run("UPDATE okumalar SET durum = 'suruyor', basladi = ? WHERE id = ?", (time.time(), tid))
        return True

    def finish(self, tid: str, email: str) -> dict | None:
        rows = self._run("SELECT * FROM okumalar WHERE id = ?", (tid,))
        if not rows or not self._visible(rows[0], email):
            return None
        if rows[0]["durum"] != "bitti":
            self._run("UPDATE okumalar SET durum = 'bitti', bitti = ? WHERE id = ?", (time.time(), tid))
        return self.task(tid, email)

    # ------------------------------------------------------------ notlar (S7.4 ve notun hayatı; S10 kişisel defter)

    def add_note(self, email: str, note: dict, kapsam: str = "defter") -> str:
        """Defter notu (S10; varsayılan) ya da ar-ge notu (`kapsam='arge'`; geçmişi tutulur, silinmez)."""
        if kapsam not in ("defter", "arge"):
            raise ValueError(kapsam)
        nid = "n-" + secrets.token_hex(6)
        now = time.time()
        clip = lambda v, n: str(v)[:n] if v else None
        self._run("INSERT INTO notlar (id, birim, surum, paragraf, secici, okuyucu, tur, metin, okuma, zaman, guncellendi, "
                  "kapsam, etiket, baglam) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (nid, str(note["birim"])[:40], note.get("surum"), clip(note.get("paragraf"), 80),
                   json.dumps(note.get("secici") or {}, ensure_ascii=False), email,
                   (note.get("tur") or "not") if kapsam == "arge" else "not", str(note["metin"])[:20000],
                   note.get("okuma"), now, now, kapsam, clip(note.get("etiket"), 80), clip(note.get("baglam"), 300)))
        if kapsam == "arge":
            self.reader_no(email)
            self._run("INSERT INTO not_gecmisi (not_id, zaman, kim, olay, veri) VALUES (?, ?, ?, 'yazildi', ?)",
                      (nid, now, email, json.dumps({"metin": note["metin"]}, ensure_ascii=False)))
        return nid

    def _own(self, nid: str, email: str) -> bool:
        return bool(self._run("SELECT 1 FROM notlar WHERE id = ? AND okuyucu = ? AND kapsam = 'defter'", (nid, email)))

    def edit_note(self, nid: str, email: str, metin: str) -> bool:
        """Defter notunu yalnız yazanı düzenler."""
        if not metin.strip() or not self._own(nid, email):
            return False
        self._run("UPDATE notlar SET metin = ?, guncellendi = ? WHERE id = ?", (metin.strip()[:20000], time.time(), nid))
        return True

    def delete_note(self, nid: str, email: str) -> bool:
        """Defter notunu yalnız yazanı siler; gerçekten silinir (S10 (g4))."""
        if not self._own(nid, email):
            return False
        self._run("DELETE FROM not_gecmisi WHERE not_id = ?", (nid,))
        self._run("DELETE FROM notlar WHERE id = ?", (nid,))
        return True

    def forget(self, email: str) -> int:
        """Hesap silinince: okuyucunun defter notları (ar-ge kayıtları numarayla kalır)."""
        ids = [r["id"] for r in self._run("SELECT id FROM notlar WHERE okuyucu = ? AND kapsam = 'defter'", (email,))]
        for nid in ids:
            self._run("DELETE FROM not_gecmisi WHERE not_id = ?", (nid,))
        self._run("DELETE FROM notlar WHERE okuyucu = ? AND kapsam = 'defter'", (email,))
        return len(ids)

    @staticmethod
    def _defter_row(r: sqlite3.Row) -> dict:
        return {"id": r["id"], "birim": r["birim"], "surum": r["surum"], "paragraf": r["paragraf"],
                "secici": json.loads(r["secici"]), "metin": r["metin"], "etiket": r["etiket"], "baglam": r["baglam"],
                "zaman": r["zaman"], "guncellendi": r["guncellendi"], "benim": True}

    def defter(self, email: str, birim: str | None = None) -> list[dict]:
        """Okuyucunun kendi notları (bir birimde ya da hepsi), yazılış sırasıyla."""
        sql, params = "SELECT * FROM notlar WHERE okuyucu = ? AND kapsam = 'defter'", [email]
        if birim is not None:
            sql, params = sql + " AND birim = ?", params + [birim]
        return [self._defter_row(r) for r in self._run(sql + " ORDER BY zaman", tuple(params))]

    def set_note_state(self, nid: str, who: str, durum: str, surum: int | None = None) -> bool:
        if durum not in ("acik", "islendi", "kapandi", "geri_cekildi"):
            raise ValueError(durum)
        rows = self._run("SELECT okuyucu FROM notlar WHERE id = ? AND kapsam = 'arge'", (nid,))
        if not rows:
            return False                                   # defter notunun durumu yok (S10)
        if durum == "geri_cekildi" and rows[0]["okuyucu"] != who:
            return False                                   # notu yalnız yazan geri çeker
        now = time.time()
        self._run("UPDATE notlar SET durum = ?, isleyen_surum = coalesce(?, isleyen_surum), guncellendi = ? WHERE id = ?",
                  (durum, surum, now, nid))
        self._run("INSERT INTO not_gecmisi (not_id, zaman, kim, olay, veri) VALUES (?, ?, ?, 'durum', ?)",
                  (nid, now, who, json.dumps({"durum": durum, "surum": surum})))
        return True

    def notes(self, birim: str, email: str) -> list[dict]:
        """Ar-ge notları (S10'dan önce yazılanlar; masa görür)."""
        out = []
        for r in self._run("SELECT * FROM notlar WHERE birim = ? AND kapsam = 'arge' AND durum != 'geri_cekildi' "
                           "ORDER BY zaman", (birim,)):
            out.append({"id": r["id"], "surum": r["surum"], "paragraf": r["paragraf"], "secici": json.loads(r["secici"]),
                        "tur": r["tur"], "metin": r["metin"], "durum": r["durum"], "isleyen_surum": r["isleyen_surum"],
                        "benim": r["okuyucu"] == email, "okuyucu_no": self.reader_no(r["okuyucu"]),
                        "zaman": r["zaman"]})
        return out

    # ------------------------------------------------------------ dışa aktarma (taslak deposuna; ad yok)

    def export(self) -> dict:
        nos = {r["email"]: r["no"] for r in self._run("SELECT email, no FROM okuyucular")}
        tasks = []
        for r in self._run("SELECT * FROM okumalar ORDER BY olusturuldu"):
            ks = [{"yer": k["yer"], "okuyucu_no": nos.get(k["okuyucu"]), "veri": json.loads(k["veri"]),
                   "zaman": k["zaman"]} for k in self._run("SELECT * FROM kararlar WHERE okuma = ? ORDER BY id", (r["id"],))]
            tasks.append({k: r[k] for k in ("id", "tur", "birim", "baslik", "sayfa", "durum", "olusturuldu", "basladi",
                                            "bitti", "kaynak")}
                         | {"veri": json.loads(r["veri"] or "{}"), "gizli": json.loads(r["gizli"]) if r["gizli"] else None,
                            "kararlar": ks})
        notes = [{k: r[k] for k in ("id", "birim", "surum", "paragraf", "tur", "metin", "durum", "isleyen_surum", "okuma",
                                    "zaman", "guncellendi")} | {"secici": json.loads(r["secici"]),
                                                                "okuyucu_no": nos.get(r["okuyucu"])}
                 for r in self._run("SELECT * FROM notlar WHERE kapsam = 'arge' ORDER BY zaman")]
        hist = [{k: r[k] for k in ("not_id", "zaman", "olay")} | {"veri": json.loads(r["veri"] or "null"),
                                                                 "okuyucu_no": nos.get(r["kim"])}
                for r in self._run("SELECT g.* FROM not_gecmisi g JOIN notlar n ON n.id = g.not_id "
                                   "WHERE n.kapsam = 'arge' ORDER BY g.id")]    # defter notları dışarı çıkmaz (S10)
        return {"sema": "masa/1", "aktarildi": time.time(), "okumalar": tasks, "notlar": notes, "not_gecmisi": hist}


def routes(auth, store: MasaStore) -> list:
    """Starlette yolları (`site_auth.build_app` ekler). `auth`: site_auth.Store (oturum çerezinden e-posta)."""
    from starlette.requests import Request
    from starlette.responses import JSONResponse
    from starlette.routing import Route

    from risale_mcp.site_auth import COOKIE

    H = {"Cache-Control": "no-store"}

    def who(request: Request) -> str | None:
        return auth.check(request.cookies.get(COOKIE))

    def desk(request: Request) -> str | None:
        """Ar-ge masasının kişisi (kapsam `masa`); platformun okuyucusu (`oku`) okuma görevlerini görmez."""
        email = who(request)
        return email if email and auth.scope(email) == "masa" else None

    def machine(request: Request) -> str | None:
        h = request.headers.get("authorization", "")
        return store.check_token(h[7:] if h.lower().startswith("bearer ") else None)

    def deny(status: int = 401) -> JSONResponse:
        return JSONResponse({"error": "oturum yok" if status == 401 else "bulunamadı"}, status_code=status, headers=H)

    async def okumalar(request: Request):
        email = desk(request)
        return JSONResponse({"okumalar": store.tasks_for(email)}, headers=H) if email else deny()

    async def okuma(request: Request):
        email = desk(request)
        if not email:
            return deny()
        t = store.task(request.path_params["tid"], email)
        return JSONResponse(t, headers=H) if t else deny(404)

    async def karar(request: Request):
        email = desk(request)
        if not email:
            return deny()
        body = await request.json()
        ok = store.add_decision(request.path_params["tid"], request.path_params["yer"], email, body)
        return JSONResponse({"ok": True}, headers=H) if ok else deny(404)

    async def bitir(request: Request):
        email = desk(request)
        if not email:
            return deny()
        t = store.finish(request.path_params["tid"], email)
        return JSONResponse(t, headers=H) if t else deny(404)

    async def notlar(request: Request):
        """S10: herkes (yönetici de) yalnız kendi defterini görür; masa ar-ge notlarını `?arge=1` ile alır."""
        email = who(request)
        if not email:
            return deny()
        birim = request.path_params["birim"]
        if request.method == "POST":
            body = await request.json()
            if not str(body.get("metin") or "").strip():
                return JSONResponse({"error": "metin gerekli"}, status_code=400, headers=H)
            body["birim"] = birim
            return JSONResponse({"id": store.add_note(email, body)}, headers=H)
        if request.query_params.get("arge"):
            return JSONResponse({"notlar": store.notes(birim, email)}, headers=H) if desk(request) else deny()
        return JSONResponse({"notlar": store.defter(email, birim)}, headers=H)

    async def not_tek(request: Request):
        """S10 (g4): defter notunu düzenleme (PUT {metin}) ve silme (DELETE); yalnız yazanı."""
        email = who(request)
        if not email:
            return deny()
        nid = request.path_params["nid"]
        if request.method == "DELETE":
            ok = store.delete_note(nid, email)
        else:
            ok = store.edit_note(nid, email, str((await request.json()).get("metin") or ""))
        return JSONResponse({"ok": True}, headers=H) if ok else deny(404)

    async def defter(request: Request):
        """S10 (g2): Notlarım: bütün birimlerdeki kendi notları."""
        email = who(request)
        return JSONResponse({"notlar": store.defter(email)}, headers=H) if email else deny()

    async def defter_docx(request: Request):
        email = who(request)
        if not email:
            return deny()
        from starlette.responses import Response

        from risale_mcp.docx_yaz import notes_docx
        name = time.strftime("notlarim-%Y-%m-%d.docx")
        return Response(notes_docx(store.defter(email)), headers=H | {
            "Content-Disposition": f'attachment; filename="{name}"'},
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    async def not_durum(request: Request):
        """Ar-ge notlarının hayatı (masa); defter notunun durumu yoktur."""
        email = who(request)
        if not email:
            return deny()
        body = await request.json()
        if body.get("durum") != "geri_cekildi" and auth.scope(email) != "masa":
            return deny(404)                               # işlendi/kapandı masanın işi; yazan yalnız geri çeker
        ok = store.set_note_state(request.path_params["nid"], email, body.get("durum"), body.get("surum"))
        return JSONResponse({"ok": True}, headers=H) if ok else deny(404)

    async def gorev(request: Request):
        if not machine(request):
            return deny()
        return JSONResponse({"acildi": store.add_task(await request.json())}, headers=H)

    async def disa(request: Request):
        return JSONResponse(store.export(), headers=H) if machine(request) else deny()

    async def makine_not(request: Request):
        """S7 (f) "notlarımla düzelt": düzeltme notu işleyince işaretler (işlendi, işleyen sürümle)."""
        who = machine(request)
        if not who:
            return deny()
        body = await request.json()
        if body.get("durum") not in ("islendi", "acik", "kapandi"):
            return JSONResponse({"error": "durum"}, status_code=400, headers=H)
        ok = store.set_note_state(body.get("id", ""), f"makine:{who}", body["durum"], body.get("surum"))
        return JSONResponse({"ok": True}, headers=H) if ok else deny(404)

    return [Route(f"{API}okumalar", okumalar), Route(API + "okuma/{tid}", okuma),
            Route(API + "okuma/{tid}/karar/{yer}", karar, methods=["PUT"]),
            Route(API + "okuma/{tid}/bitir", bitir, methods=["POST"]),
            Route(API + "notlar/{birim}", notlar, methods=["GET", "POST"]),
            Route(API + "not/{nid}/durum", not_durum, methods=["PUT"]),
            Route(API + "not/{nid}", not_tek, methods=["PUT", "DELETE"]),
            Route(f"{API}defter", defter), Route(f"{API}defter.docx", defter_docx),
            Route(f"{API}gorev", gorev, methods=["POST"]), Route(f"{API}disa", disa),
            Route(f"{API}not-durum", makine_not, methods=["POST"])]


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("token")
    p.add_argument("--new", action="store_true")
    p.add_argument("--ad", default="taslak-sunucusu")
    sub.add_parser("gorevler")
    a = ap.parse_args(argv)
    store = MasaStore()
    if a.cmd == "token" and a.new:
        print(store.new_token(a.ad))
    elif a.cmd == "gorevler":
        for t in store._run("SELECT id, tur, durum, atanan, olusturuldu FROM okumalar ORDER BY olusturuldu"):
            print(f"{t['id']:<32} {t['tur']:<6} {t['durum']:<9} {t['atanan'] or 'herkes'}")


if __name__ == "__main__":
    main()
