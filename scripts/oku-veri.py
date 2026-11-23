"""S7.3 okuma platformu ve ar-ge masasının birim görünümü: veri ve sayfalar (kullanıcının kararları, 2026-11-21;
PLANLAR S7). Tek veri biçimi, iki görünüm: ikisi de yayın dosyasından (`d1-yayin.py`) ve aynı uygulamadan
(`scripts/oku-app.html`) çizilir.

- **Okuma platformu** (`risalemcp.com/oku/`, davetli): her birimde yalnız son taslak (yayın dosyasının son sürümü);
  Bakara 1–33'te önce müellifin sözü (İşârâtü'l-İ'câz), yanında İşârât'ı görmeden yazılmış taslak; âyetin Risale'deki
  yerleri (müellifin sözüyle), müfessirler (Arapça, istek üzerine), künye, işaretler, indirme ve atıf satırı.
  Çıktı `data/interim/oku/` (yeniden üretilir, git'e girmez); sitede `/var/www/ozel/taslak/oku/` (Caddy `/oku/`'yu
  oraya çevirir; D5 sunucusunun kısıtlı anahtarı yalnız taslak klasörüne yazabildiği için).
- **Ar-ge masası:** birim sayfası eski âyet masasıdır (`scripts/d1-masa.py`; S7b, kullanıcının kararı 2026-11-21);
  bu betiğin `masa_data`'sı ona kapı, nisbet ve alarm verir. Önceki `/taslak/birim.html` emekli. Eski not:
  karşılaştırma, kapı ve eleştirmen notları (ham), nisbet hükümleri, alarmlar, eski sayfalar. Çıktı
  `data/interim/oku-masa/` → `/var/www/ozel/taslak/` (`birim.html`, `birim/<birim>.json`).

Kaynak adları (izinlerin şartı, `docs/izinler.md`): Risale'nin cümleleri eserin sitesi ve bölüm bağlantısıyla (e-Risale,
risaleoku.com, nurpedia.org, Keşif), müfessirler ve klasikler OpenITI (dosya, CC BY-NC-SA 4.0), Kur'ân Tanzil, meal
Türkiye Diyanet Vakfı.

    uv run python scripts/oku-veri.py                 # bütün birimler (yayını olmayan ar-ge birimleri yayımlanır)
    uv run python scripts/oku-veri.py --birim 34      # bir birim (D5 kuyruğu her birimden sonra)
    uv run python scripts/oku-veri.py --gonder        # ve siteye
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, file: str):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / file)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


P = _load("d1_prova", "d1-prova.py")
Y = _load("d1_yz", "d1-yz.py")
YAY = _load("d1_yayin", "d1-yayin.py")
DUR = _load("d1_durum", "d1-durum.py")

from risale_mcp.library import Library          # noqa: E402
from risale_mcp.paths import DIST_DIR           # noqa: E402
from risale_mcp.quran import SURA_NAMES         # noqa: E402

OUT = ROOT / "data" / "interim" / "oku"
OUT_MASA = ROOT / "data" / "interim" / "oku-masa"
APP = ROOT / "scripts" / "oku-app.html"
USUL = ROOT / "scripts" / "oku-usul.html"
TERCUME = P.KEEP / "tercume" / "kaynaklar.json"
ISARAT = _load("isarat_esleme", "isarat-esleme.py")
ALINTI = _load("alinti", "alinti.py")        # S7f: alıntının kaynaktaki cümlesi ve İşârât'ta Abdülmecid tercümesi
CHOICE = P.KEEP / "oku" / "secim.json"          # ar-ge birimlerinde platforma giden taslak (yoksa en son taslak)
SITE_HOST = os.environ.get("D5_SITE_HOST", "root@100.108.174.19")
SITE_KEY = Path.home() / ".ssh" / "site_gonder"                 # sunucuda (rrsync, kök /var/www/ozel/taslak)
LOCAL_KEY = Path.home() / ".ssh" / "risale_hetzner"             # yerelde (tam erişim)

SITES = {"erisale": ("e-Risale", "https://www.erisale.com"), "risaleoku_app": ("risaleoku.com", "https://risaleoku.com"),
         "nurpedia": ("nurpedia.org", "https://www.nurpedia.org"),
         "kesif": ("Keşif Yolculukları Risale-i Nur Eğitim Programı (Protranslate tercümesi)", None)}
OPENITI = ("OpenITI (KITAB projesi), CC BY-NC-SA 4.0", "https://github.com/OpenITI")
TANZIL = ("Tanzil Project (tanzil.net)", "https://tanzil.net")
LINK_KINDS = {"acilis": "bölüm bu âyetle açılıyor", "izah": "âyetin ardından müellifin izahı (\"Yani\")",
              "isaret": "cümlede âyete işaret", "dayanak": "âyete dayanan söz (\"… sırrınca\")",
              "risale": "âyetin Risale-i Nur'a işareti"}
ISARAT_TR, ISARAT_AR = "isaratul-icaz/sure-i-bakara", "isaratul-icaz-arabi/sure-i-bakara"


# ---------------------------------------------------------------- kaynaklar

class Libs:
    def __init__(self) -> None:
        self._lib: dict[str, Library | None] = {}
        self._conn: dict[str, sqlite3.Connection | None] = {}

    def lib(self, profile: str) -> Library | None:
        if profile not in self._lib:
            path = DIST_DIR / profile / "risale.db"
            self._lib[profile] = Library(path) if path.exists() else None
        return self._lib[profile]

    def conn(self, profile: str) -> sqlite3.Connection | None:
        if profile not in self._conn:
            path = DIST_DIR / profile / ("hadis.db" if profile == "hadis" else "risale.db")
            self._conn[profile] = sqlite3.connect(f"file:{path}?mode=ro", uri=True) if path.exists() else None
        return self._conn[profile]

    def source(self, server: str | None, sid: str | None) -> dict:
        """Kaynağın adı ve bağlantısı (izinlerin şartı)."""
        if sid is None:
            return {"ad": TANZIL[0], "bag": TANZIL[1]}
        first = sid.split("..")[0]
        if server == "risale":
            c = self.conn("genel")
            row = c.execute("SELECT n.url, w.site FROM sentences s JOIN nodes n ON n.id = s.node_id "
                            "JOIN works w ON w.slug = n.work WHERE s.id = ?", (first,)).fetchone() if c else None
            if row:
                name, home = SITES.get(row[1], (row[1], None))
                return {"ad": name, "bag": row[0] or home}
            return {"ad": "Risale-i Nur", "bag": None}
        if server in ("tefsir", "klasik"):
            c = self.conn(server)
            row = c.execute("SELECT edition FROM works WHERE slug = ?", (first.split("/")[0],)).fetchone() if c else None
            ed = json.loads(row[0]) if row and row[0] else {}
            return {"ad": OPENITI[0] + (f" · {ed['file']}" if ed.get("file") else ""), "bag": OPENITI[1]}
        if server == "hadis":
            return {"ad": "Hadis kitapları (OpenITI ve öbür kaynaklar, Risale MCP Hadis)", "bag": None}
        return {"ad": server or "?", "bag": None}

    def node_url(self, node_id: str) -> str | None:
        c = self.conn("genel")
        row = c.execute("SELECT url FROM nodes WHERE id = ?", (node_id,)).fetchone() if c else None
        return row[0] if row else None


def read_all(lib: Library, section: str) -> list[dict]:
    """Bölümün bütün öğeleri (başlıklar ve paragraflar), sayfa sayfa."""
    items, cursor = [], None
    while True:
        r = lib.read_section(section, cursor=cursor, max_words=200000)
        items += r["items"]
        cursor = r.get("next_cursor")
        if not cursor:
            return items


def slim(items: list[dict]) -> list[dict]:
    """Okuma için sade öğe: başlık ya da paragraf (metin, tür, hâşiye mi)."""
    out = []
    for it in items:
        if "sentences" in it:
            out.append({"k": it.get("kind") or "paragraph", "t": " ".join(s["text"] for s in it["sentences"]),
                        **({"h": 1} if it.get("hasiye_of") else {})})
        elif it.get("title"):
            out.append({"k": "baslik", "t": it["title"]})
    return out


def isarat_nodes(libs: Libs, unit: str) -> dict:
    """İşârât'ın bu birime düşen bölümleri: Türkçe (21–22 iki bölüm) ve Arapça aslı."""
    c = libs.conn("genel")
    out = {}
    for lang, parent in (("tr", ISARAT_TR), ("ar", ISARAT_AR)):
        kids = [r[0] for r in c.execute("SELECT id FROM nodes WHERE parent_id = ? ORDER BY ord", (parent,))]
        tail = {k.rsplit("/", 1)[1]: k for k in kids}
        hit = [k for t, k in tail.items() if t == unit or t.startswith(unit + "-")]
        if not hit and "-" in unit:
            a, b = (int(x) for x in unit.split("-"))
            hit = [tail[str(x)] for x in range(a, b + 1) if str(x) in tail]
        out[lang] = hit
    return out


def isarat(libs: Libs, unit: str) -> dict | None:
    nodes = isarat_nodes(libs, unit)
    if not nodes["tr"] and not nodes["ar"]:
        return None
    lib = libs.lib("genel")
    res = {}
    for lang, ids in nodes.items():
        parts = []
        for nid in ids:
            r = lib.read_section(nid, max_words=1)
            parts.append({"bolum": nid, "ref": r["ref"], "bag": libs.node_url(nid), "ogeler": slim(read_all(lib, nid))})
        res[lang] = parts
    res["kaynak"] = {"tr": "e-Risale (Abdülmecid Nursî tercümesi)", "ar": "risaleoku.com"}
    return res


def risale_links(libs: Libs, sura: int, ayahs: range) -> list[dict]:
    """Âyetin Risale'deki yerleri (âyet ilişkileri): türü, gücü, bölüm, kanıt cümlesi müellifin sözüyle."""
    lib = libs.lib("genel")
    out = []
    for k in ayahs:
        try:
            links = lib.find_ayah(str(sura), k).get("links") or []
        except Exception:                     # noqa: BLE001 (veri yoksa platform yine kurulur)
            links = []
        for x in links:
            ev = x.get("evidence") or {}
            text = None
            if ev.get("id") and x.get("scope") == "sentence":
                try:
                    text = lib.passage(ev["id"]).get("text")
                except Exception:             # noqa: BLE001
                    text = None
            out.append({"ayet": k, "tur": x["kind"], "tur_adi": LINK_KINDS.get(x["kind"], x["kind"]),
                        "guc": x.get("strength"), "kapsam": x.get("scope"), "ref": x.get("ref"),
                        "bag": libs.node_url(x.get("section") or ""), "kanit": ev.get("ref"),
                        "metin": text or ev.get("opening")})
    out.sort(key=lambda x: (x["guc"] != "strong", x["ayet"]))
    return out


def tefsir_units(libs: Libs, sura: int, ayahs: range) -> list[dict]:
    """Müfessirlerin bu âyetleri işleyen birimleri (vefat sırasıyla; metin ayrı dosyada, istek üzerine)."""
    lib = libs.lib("tefsir")
    if lib is None:
        return []
    by: dict[str, dict] = {}
    for k in ayahs:
        for w in lib.find_ayah(str(sura), k).get("classical_works") or []:
            e = by.setdefault(w["work"], {"eser": w["work"], "ad": w["title"], "musannif": w["author"], "birimler": []})
            for u in w.get("units") or []:
                if u["section"] not in [x["bolum"] for x in e["birimler"]]:
                    e["birimler"].append({"bolum": u["section"], "ref": u["ref"], "basili": u.get("printed")})
    return list(by.values())


def tefsir_text(libs: Libs, section: str) -> Path:
    path = OUT / "veri" / "t" / (section.replace("/", "_") + ".json")
    if not path.exists():
        lib = libs.lib("tefsir")
        data = {"bolum": section, "ogeler": slim(read_all(lib, section)),
                "kaynak": libs.source("tefsir", section)}
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return path


# ---------------------------------------------------------------- birimler

def published(unit: str) -> dict | None:
    """Platforma giden yayın sürümü: D5'te son sürüm; ar-ge biriminde seçilen (yoksa en son) taslak yayımlanır."""
    idx_path = YAY.YAYIN / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8")) if idx_path.exists() else {"birimler": {}}
    if unit not in P.UNITS or not (P.DRAFTS / unit).is_dir():
        return None
    cfg = P.UNITS[unit]
    if not cfg.get("d5"):                 # ar-ge birimi (Bakara 1–33)
        choice = json.loads(CHOICE.read_text(encoding="utf-8")) if CHOICE.exists() else {}
        if unit in choice and not choice[unit]:   # 0/null: henüz yayımlanmaz (ör. kör okuması sürerken)
            return None
        n = choice.get(unit) or max((d["n"] for d in DUR.drafts(unit)), default=None)
        if not n:
            return None
        if not SITE_KEY.exists():  # ar-ge birimlerini yerel yayımlar (sunucu yazmaz: iki makinede v1 çakışmasın)
            YAY.yayinla(unit, n)                  # içerik aynıysa sürüm kalır, değiştiyse yeni sürüm
            idx = json.loads(idx_path.read_text(encoding="utf-8"))
    cur = idx["birimler"].get(unit)
    return json.loads((YAY.YAYIN / cur["yol"]).read_text(encoding="utf-8")) if cur else None


_TURK: dict | None = None


def turk_hatti(sura: int, ayah: int) -> str | None:
    """Âyetin Türk hattı (`risale_mcp.kuran_turk`, risaleoku; görüntü için)."""
    global _TURK
    if _TURK is None:
        f = ROOT / "data" / "library" / "kuran" / "turk.json"
        _TURK = json.loads(f.read_text(encoding="utf-8"))["suras"] if f.exists() else {}
    row = _TURK.get(str(sura)) or []
    return row[ayah - 1] if ayah <= len(row) else None


def unit_data(libs: Libs, u: dict) -> dict:
    unit, (a, b) = u["id"], u["ayet"]
    cfg = P.UNITS.get(unit, {"sura": 2, "sura_name": "Bakara"})
    sura = cfg["sura"]
    pub = published(unit)
    q = Q_AYAHS
    d = {"birim": unit, "sure": sura, "sure_adi": cfg["sura_name"], "ayet": [a, b],
         "ayetler": [{"n": k, "metin": q[k]["text"], "turk": turk_hatti(sura, k),
                      "meal": q[k]["translations"]["diyanet-vakfi"]} for k in range(a, b + 1)],
         "ayet_kaynak": {"metin": TANZIL[0] + ", Medine Mushafı hattı", "turk": "risaleoku.com, Türk hattı",
                         "meal": "Türkiye Diyanet Vakfı meali (Tanzil üzerinden)", "bag": TANZIL[1]},
         "isarat": isarat(libs, unit) if u["kaynak"] == "isarat" else None,
         "risale": risale_links(libs, sura, range(a, b + 1)),
         "tefsir": tefsir_units(libs, sura, range(a, b + 1)),
         "bolum_adlari": P.SECTION_TITLES}
    if pub:
        tercume = json.loads(TERCUME.read_text(encoding="utf-8")) if TERCUME.exists() else {}
        for k, v in pub["kaynaklar"].items():
            v["kaynak"] = libs.source(v.get("sunucu"), v.get("kimlik"))
            if v.get("kimlik") in tercume:                  # S7c.5: andığı tefsir ve klasik yerin Türkçesi (yapay zekâ)
                v["tercume"] = tercume[v["kimlik"]]["tr"]
            elif v.get("sunucu") == "risale" and (amt := ISARAT.turkcesi(v.get("kimlik"))):   # S7c.4: Abdülmecid
                v["tercume"], v["tercume_kim"] = amt, "abdulmecid"
        by_tr = {b.get("tercumesi"): b for b in pub["bloklar"] if b.get("tercumesi")}
        for b in pub["bloklar"]:                         # S7f: alıntının cümlesi, İşârât'ta Abdülmecid tercümesi
            if b["tur"] not in ("alinti_ar", "alinti"):
                continue
            for k in b.get("kaynaklar") or []:
                v = pub["kaynaklar"].get(k) or {}
                if ctx := ALINTI.context(v.get("sunucu"), v.get("kimlik"), b["metin"]):
                    if ctx.get("cumle"):
                        b["cumle"] = ctx["cumle"]
                    if ctx.get("amt") and (tr := by_tr.get(b["id"])):
                        tr["abdulmecid"] = ctx["amt"]
                    break
        d["taslak"] = {k: pub[k] for k in ("surum", "yayimlandi", "kunye", "bloklar", "kaynaklar", "eksik", "icerik_sha")
                       if k in pub} | {"onceki_surum": pub.get("onceki_surum")}
    for w in d["tefsir"]:
        for x in w["birimler"]:
            x["dosya"] = "t/" + tefsir_text(libs, x["bolum"]).name
    return d


def masa_data(unit: str, base: dict) -> dict:
    """Ar-ge masasının ekleri: bütün taslaklar, kapı ve eleştirmen notları, nisbet, alarmlar (ham)."""
    out = {"taslaklar": [], "kapi": [], "kapali": [], "nisbet": [], "acik": [], "alarmlar": [], "sayfalar": []}
    if not (P.DRAFTS / unit).is_dir():
        return out
    yz = Y.out_dir(unit)
    reg_path = P.DRAFTS / unit / "duzeltmeler.json"
    reg = json.loads(reg_path.read_text(encoding="utf-8")) if reg_path.exists() else {}
    for t in DUR.drafts(unit):
        n = t["n"]
        meta = json.loads((P.DRAFTS / unit / f"taslak-{n}.json").read_text(encoding="utf-8"))
        try:
            blocks, sources = Y.draft_blocks(unit, n)
        except Exception as e:               # noqa: BLE001 (eski biçim)
            blocks, sources = [], {"hata": str(e)}
        out["taslaklar"].append({"n": n, "surum": t["surum"], "model": t["model"], "at": t["at"], "maliyet": t["cost"],
                                 "duzeltme": meta.get("duzeltme"), "kaynak_taslak": (reg.get(str(n)) or {}).get("kaynak"),
                                 "bloklar": [{"capa": a, "dil": lang, "alinti": q, "metin": x} for a, lang, q, x in blocks],
                                 "kaynaklar": sources})
        # kapının her düzeltmesi ayrı (aynı taslaktan birden çok deneme olabilir: 26–27, 28)
        files = {"kapi": ("kapi-notlar-taslak-{n}.json", "Q"), "kapi2": ("kapi2-notlar-taslak-{n}.json", "R"),
                 "okuyucu": ("okuyucu-notlar-taslak-{n}.json", "O")}
        for new, r in sorted(((int(k), v) for k, v in reg.items() if v["kaynak"] == n), key=lambda kv: kv[0]):
            fname, prefix = files.get(r["notlar"], files["kapi"])
            f = yz / fname.format(n=n)
            dzp = P.DRAFTS / unit / f"taslak-{new}.duzeltme.json"
            if not f.exists() or not dzp.exists():
                continue
            notes = json.loads(f.read_text(encoding="utf-8"))["notlar"]
            dz = json.loads(dzp.read_text(encoding="utf-8"))
            handled, rejected = {}, {r2.get("not"): r2.get("gerekce", "") for r2 in dz.get("reddedilen", [])}
            for ch in dz.get("degisiklikler", []):
                for no in ch.get("notlar", []):
                    handled.setdefault(no, []).append(f"{ch.get('islem')} {ch.get('capa') or ch.get('sonra') or ''}")
            rows = []
            for i, x in enumerate(notes, 1):
                no = f"{prefix}{i}"
                state = ("kısmen" if no in rejected else "karşılandı") if no in handled else (
                    "reddedildi" if no in rejected else "anılmadı")
                rows.append({"no": no, "tur": x.get("tur"), "kaynak": x.get("kaynak"), "capa": x.get("capa"),
                             "oncelik": x.get("oncelik"), "alinti": x.get("taslak_alinti"), "metin": x.get("metin"),
                             "oneri": x.get("oneri"), "durum": state, "nasil": handled.get(no),
                             "gerekce": rejected.get(no)})
            out["kapi"].append({"tur": r["notlar"], "surum": r.get("surum"), "taslak": n, "yeni": new, "notlar": rows,
                                "ozet": dz.get("ozet")})
        for f in sorted(yz.glob(f"kapali-elestiri-taslak-{n}*.json")):
            if f.name.endswith(".meta.json"):
                continue
            k = json.loads(f.read_text(encoding="utf-8"))
            out["kapali"].append({"taslak": n, "dosya": f.stem, "surum": k.get("surum"),
                                  "notlar": [{kk: x.get(kk) for kk in ("tur", "capa", "taslak_alinti", "metin", "nasil",
                                                                       "oneri", "oncelik", "ehline_sor", "soru")}
                                             for x in k.get("notlar", [])], "ozet": k.get("ozet")})
        f = yz / f"nisbet-taslak-{n}.json"
        if f.exists():
            k = json.loads(f.read_text(encoding="utf-8"))
            out["nisbet"].append({"taslak": n, "hukumler": k.get("hukumler", [])})
        f = yz / f"kapi-acik-notlar-taslak-{n}.json"
        if f.exists():
            out["acik"].append({"taslak": n, "notlar": json.loads(f.read_text(encoding="utf-8"))["notlar"]})
    st = P.d5_state()["birimler"].get(unit, {})
    out["alarmlar"] = st.get("alarmlar") or []
    out["sayfalar"] = [p.name for p in (P.KEEP / "masa").glob("*.html")
                       if p.stem == unit or p.stem.startswith((f"tur-{unit}-", f"d5-{unit}", f"fark-{unit}-"))]
    return out


def plain(d: dict) -> str:
    """Birimin düz metni (indirme): âyet, taslağın Türkçesi, kaynakça; damgasıyla."""
    L = [f"{d['sure_adi']} {d['ayet'][0]}" + (f"–{d['ayet'][1]}" if d['ayet'][1] != d['ayet'][0] else ""),
         "Yapay zekâ taslağıdır; tefsir değildir, müellife ya da İşârât'a mal edilmez. Risale MCP (risalemcp.com/oku/)", ""]
    for x in d["ayetler"]:
        L += [f"{x['metin']} ﴿{x['n']}﴾", f"Meal (Türkiye Diyanet Vakfı): {x['meal']}", ""]
    t = d.get("taslak")
    if not t:
        return "\n".join(L + ["(Taslak yok.)"])
    L.append(f"Sürüm {t['surum']} · yayımlandı {t.get('yayimlandi', '')[:10]}")
    sec = None
    for blk in t["bloklar"]:
        if blk["bolum"] != sec:
            sec = blk["bolum"]
            L += ["", "## " + P.SECTION_TITLES.get(sec, sec), ""]
        L += [blk["metin"], f"  [{blk['id']}]", ""]
    L += ["", "## Kaynaklar", ""] + [f"[{k}] {v['satir']} — {v['kaynak']['ad']}" for k, v in t["kaynaklar"].items()]
    return "\n".join(L) + "\n"


Q_AYAHS: dict = {}


def build(only: str | None = None) -> list[str]:
    global Q_AYAHS
    q = json.loads((ROOT / "data" / "library" / "kuran" / "quran.json").read_text(encoding="utf-8"))
    Q_AYAHS = {v["ayah"]: v for v in q["suras"][1]["ayahs"]}
    libs = Libs()
    units = P.d5_units()
    (OUT / "veri").mkdir(parents=True, exist_ok=True)
    (OUT / "indir").mkdir(parents=True, exist_ok=True)
    OUT_MASA.mkdir(parents=True, exist_ok=True)
    idx_path = OUT / "veri" / "index.json"
    if only and not idx_path.exists():           # ilk kurulum (ör. sunucuda): bütün birimler
        only = None
    old = {x["id"]: x for x in json.loads(idx_path.read_text(encoding="utf-8"))["birimler"]} if idx_path.exists() else {}
    rows, done = [], []
    for u in units:
        uid = u["id"]
        has_dir = (P.DRAFTS / uid).is_dir() and bool(DUR.drafts(uid))      # boş klasör sayılmaz
        relevant = u["kaynak"] == "isarat" or has_dir
        if (only and uid != only) or not relevant:
            rows.append(old.get(uid) or {"id": uid, "ayet": u["ayet"], "tur": "d5" if u["kaynak"] != "isarat" else "isarat",
                                         "taslak": False, "isarat": u["kaynak"] == "isarat"})
            continue
        d = unit_data(libs, u)
        (OUT / "veri" / f"{uid}.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        (OUT / "indir" / f"bakara-{uid}.txt").write_text(plain(d), encoding="utf-8")
        m = masa_data(uid, d)
        rows.append({"id": uid, "ayet": u["ayet"], "tur": "d5" if u["kaynak"] != "isarat" else "isarat",
                     "taslak": bool(d.get("taslak")), "isarat": bool(d.get("isarat")),
                     "surum": (d.get("taslak") or {}).get("surum"), "masa_taslak": len(m["taslaklar"])})
        done.append(uid)
        print(f"{uid}: taslak {'v' + str(d['taslak']['surum']) if d.get('taslak') else '—'}, İşârât "
              f"{'var' if d.get('isarat') else '—'}, Risale yeri {len(d['risale'])}, müfessir {len(d['tefsir'])}, "
              f"masa taslak {len(m['taslaklar'])}", flush=True)
    index = {"sema": "oku/1", "uretildi": time.time(),
             "sureler": [{"n": i + 1, "ad": name, "ayet": len(q["suras"][i]["ayahs"])} for i, name in enumerate(SURA_NAMES)],
             "sure": {"n": 2, "ad": "Bakara"}, "birimler": rows}
    idx_path.write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
    # arama dizini: yayımlanan taslakların Türkçe paragrafları ve izahları (platformda konu araması)
    ara = []
    for r in rows:
        f = OUT / "veri" / f"{r['id']}.json"
        if r.get("taslak") and f.exists():
            t = json.loads(f.read_text(encoding="utf-8"))["taslak"]
            for blk in t["bloklar"]:
                if blk["tur"] in ("tr", "tercume", "alinti", "alinti_tercume"):
                    ara.append({"b": r["id"], "p": blk["id"], "t": blk["metin"]})
                if blk.get("izah"):
                    ara.append({"b": r["id"], "p": blk["id"], "t": blk["izah"]["metin"], "i": 1})
    (OUT / "veri" / "ara.json").write_text(json.dumps(ara, ensure_ascii=False), encoding="utf-8")
    # sûrenin tamamı: taslağı olan birimler, sırayla
    whole = [json.loads((OUT / "veri" / f"{r['id']}.json").read_text(encoding="utf-8")) for r in rows
             if r.get("taslak") and (OUT / "veri" / f"{r['id']}.json").exists()]
    (OUT / "indir" / "bakara.json").write_text(json.dumps({"sema": "oku-sure/1", "sure": 2, "birimler": [
        {k: x[k] for k in ("birim", "ayet", "ayetler", "taslak") if k in x} for x in whole]}, ensure_ascii=False),
        encoding="utf-8")
    (OUT / "indir" / "bakara.txt").write_text("\n\n".join(plain(x) for x in whole), encoding="utf-8")
    app = APP.read_text(encoding="utf-8")
    for path, conf in ((OUT / "index.html", {"__MASA__": "false", "__TITLE__": "Kur'ân Taslakları",
                                               "__FONT__": "fonts/naskh.ttf", "__USUL__": "usul.html",
                                               "__EXTRA__": ' <a class="hbtn" href="/taslak/cikis">Çıkış</a>'}),):
        # masanın birim görünümü eski âyet masasıdır (d1-masa.py; S7b, kullanıcının kararı 2026-11-21)
        page = app
        for k, v in conf.items():
            page = page.replace(k, v)
        path.write_text(page, encoding="utf-8")
    (OUT / "usul.html").write_text(USUL.read_text(encoding="utf-8"), encoding="utf-8")
    (OUT / "fonts").mkdir(exist_ok=True)
    font = ROOT / "scripts" / "oku-fonts" / "NotoNaskhArabic-Regular.ttf"
    if not (OUT / "fonts" / "naskh.ttf").exists():
        (OUT / "fonts" / "naskh.ttf").write_bytes(font.read_bytes())
        (OUT / "fonts" / "OKUBENI.md").write_bytes((font.parent / "OKUBENI.md").read_bytes())
    return done


def gonder() -> None:
    """Siteye: platform `/var/www/ozel/taslak/oku/`, D5 birimlerinin masası `/var/www/ozel/taslak/` (`d1-masa.py`)."""
    if SITE_KEY.exists():                    # D5 sunucusu: kısıtlı anahtar, kök taslak klasörü
        ssh, dest_oku, dest_masa = f"ssh -i {SITE_KEY} -o BatchMode=yes", f"{SITE_HOST}:/oku/", f"{SITE_HOST}:/"
        extra = []
    else:
        ssh = f"ssh -i {LOCAL_KEY} -o BatchMode=yes"
        dest_oku, dest_masa = f"{SITE_HOST}:/var/www/ozel/taslak/oku/", f"{SITE_HOST}:/var/www/ozel/taslak/"
        extra = ["--chown=root:caddy"]
        subprocess.run(["ssh", "-i", str(LOCAL_KEY), "-o", "BatchMode=yes", SITE_HOST,
                        "install -d -o root -g caddy -m 2750 /var/www/ozel/taslak/oku"], check=True)
    pairs = [(f"{OUT}/", dest_oku), (f"{OUT_MASA}/", dest_masa)]
    if not SITE_KEY.exists():
        # yerelde masa gönderilmez (S10, 2026-11-23): masayı taslak sunucusu kurar, yereldeki kopya eskidir ve onun
        # daha yeni dosyalarını ezerdi
        pairs = pairs[:1]
        print("yerelden yalnız platform gönderiliyor (masa taslak sunucusundan gider)")
    for src, dest in pairs:
        subprocess.run(["rsync", "-rtz", "--chmod=D2750,F640", *extra, "-e", ssh, src, dest], check=True)
    print("https://risalemcp.com/oku/")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--birim")
    ap.add_argument("--gonder", action="store_true")
    a = ap.parse_args()
    build(a.birim)
    if a.gonder:
        gonder()


if __name__ == "__main__":
    main()
