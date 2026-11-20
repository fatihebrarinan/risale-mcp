"""D5'in tek komutla birim hattı ve kuyruğu (PLANLAR D5.0.1; kullanıcının kararı, 2026-11-21: D5.1'den önce üretimin
hepsi hazır olsun).

    uv run python scripts/d1-birim.py yaz 34                 # bir birim, baştan sona (biteni atlar)
    uv run python scripts/d1-birim.py kuyruk [--kadar 60]    # Bakara sırasıyla, bitmemiş ilk birimden; tavan ve bildirimle
    uv run python scripts/d1-birim.py durum                  # birimlerin kaydı: son taslak, maliyet, süre

Uzun iş olduğu için `scripts/d1-arka.sh baslat <ad> uv run python scripts/d1-birim.py …` ile (sunucuda
`scripts/taslak-sunucu.sh calistir scripts/d1-arka.sh baslat …`).

Bir birimin adımları (her biri dosyası varsa atlanır; kesintiden sonra kaldığı yerden):
  1. kurulum: `d1-prova.py hazirla` (D5: genel veritabanlarına bağ), `d1-hat.py hazirla --surum <S>` (istem; konular
     bir küçük model çağrısı)
  2. taslak: `d1-hat.py yazdir --yoksa`
  3. kapı d3: kapalı eleştirmen (tek çağrı), nisbet denetçisi, düzeltme, gerekirse ikinci küçük tur (`d1-duzelt.py kapi`)
  4. garaz özeti: son taslaktan iki cümle (`data/d1/garaz/d5-bakara.json`; sonraki birimin Ek 3b'si)
  5. izah: son taslağın günümüz Türkçesiyle izahı (`d1-hat.py izah`, D5.0.3)
  6. okuma sayfası (`d1-d5-sayfa.py`), birim kaydı (`data/d1/d5/bakara.json`)
Birimin sırası kesindir: her birim önceki birimin son taslağını bekler (D5.0.5).
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SURUM = os.environ.get("D5_SURUM", "h12")      # kabul birimi 30'dan sonra kesinleşir (h9 ya da h12)


def _load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / file)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


P = _load("d1_prova", "d1-prova.py")
Y = _load("d1_yz", "d1-yz.py")

S = _load("d1_d5_sayfa", "d1-d5-sayfa.py")
GARAZ_D5 = P.KEEP / "garaz" / "d5-bakara.json"
GARAZ_ISTEM = """Aşağıda Bakara Sûresi {ayahs}. âyetler için yazılmış bir yapay zekâ taslağı var (İşârâtü'l-İ'câz usulüyle;
Arapça). **İki cümleyi geçmeyen Türkçe bir özet** yaz: bu âyetler neyi anlatıyor ve taslağa göre **asıl garazı**
(maksadı) ne. Kurallar: yalnız bu âyetler; taslağın **sonraki âyetlere** dair söylediğini (onları hazırlaması, onlarla
bağı) **yazma**; alıntı yapma; kendi yorumunu katma. Cevabın yalnız şu JSON: {{"ozet": "..."}}

{taslak}
"""


def run(*args: str) -> str:
    """Bir hattın komutu; çıktısı günlüğe akar, döndürülür. Geçici hataya karşı bir kez yeniden denenir (adımlar biteni
    atlar); ikincisinde iş durur."""
    cmd = ["uv", "run", "python", *args]
    for attempt in (1, 2):
        print(f"$ {' '.join(args)}" + (" (yeniden)" if attempt == 2 else ""), flush=True)
        p = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        sys.stdout.write(p.stdout)
        sys.stdout.flush()
        if not p.returncode:
            return p.stdout
        if attempt == 1:
            print(f"  adım başarısız ({p.returncode}); 2 dk sonra bir kez daha", flush=True)
            time.sleep(120)
    raise SystemExit(f"adım başarısız ({p.returncode}): {' '.join(args)}")


def depo(msg: str) -> None:
    """`data/d1` commit, öbür makinenin yazdıklarını çek, push (her birimden sonra; kuyruk tek uzun iş)."""
    g = ["git", "-C", str(P.KEEP)]
    if not subprocess.run(g + ["status", "--porcelain"], capture_output=True, text=True).stdout.strip():
        return
    ok = (subprocess.run(g + ["add", "-A"]).returncode == 0
          and subprocess.run(g + ["commit", "-qm", msg]).returncode == 0
          and subprocess.run(g + ["pull", "-q", "--rebase"]).returncode == 0
          and subprocess.run(g + ["push", "-q"]).returncode == 0)
    print("data/d1 commit ve push edildi" if ok else "UYARI: data/d1 commit ya da push edilemedi", flush=True)


def save_state(unit: str, **kw) -> None:
    st = P.d5_state()
    st["birimler"].setdefault(unit, {}).update(kw)
    P.D5_STATE.parent.mkdir(parents=True, exist_ok=True)
    P.D5_STATE.write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")


def draft_of_version(unit: str, surum: str) -> int | None:
    d = P.DRAFTS / unit
    for p in sorted(d.glob("taslak-*.json"), key=lambda x: int(x.stem.split("-")[1]) if x.stem.split("-")[1].isdigit() else 0):
        n = p.stem.split("-")[1]
        if n.isdigit():
            m = json.loads(p.read_text(encoding="utf-8"))
            if m.get("surum") == surum and not m.get("duzeltme"):
                return int(n)
    return None


def unit_cost(unit: str) -> float:
    """Birimin bütün model çağrılarının toplamı (taslaklar, düzeltmeler, ölçüler, izah, garaz)."""
    total = 0.0
    for base in (P.DRAFTS / unit, Y.out_dir(unit)):
        for f in base.glob("*.meta.json"):
            total += json.loads(f.read_text(encoding="utf-8")).get("cost_usd") or 0
        for f in base.glob("taslak-*.json"):
            if f.stem.split("-")[1].isdigit():
                m = json.loads(f.read_text(encoding="utf-8"))
                if not m.get("duzeltme"):
                    total += m.get("cost_usd") or 0
    return round(total, 2)


def garaz(unit: str, n: int) -> str:
    data = json.loads(GARAZ_D5.read_text(encoding="utf-8")) if GARAZ_D5.exists() else {"ozetler": {}, "taslak": {}}
    if data["taslak"].get(unit) == n:
        return data["ozetler"][unit]
    blocks, _ = Y.draft_blocks(unit, n)
    text = "\n\n".join(("> " if q else "") + t for _, lang, q, t in blocks if lang == "ar")
    cfg = P.UNITS[unit]
    stem = Y.out_dir(unit) / f"garaz-taslak-{n}"
    res = Y.run_model(GARAZ_ISTEM.format(ayahs=P.ayah_range(cfg), taslak=text), "opus", stem, {"gorev": "garaz", "taslak": n})
    if not res or not res.get("ozet"):
        raise SystemExit("garaz özeti çıkarılamadı")
    data["ozetler"][unit], data["taslak"][unit] = res["ozet"], n
    GARAZ_D5.parent.mkdir(parents=True, exist_ok=True)
    GARAZ_D5.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    return res["ozet"]


def kapi(unit: str, n: int) -> int:
    """Kalite kapısı d3: kapalı eleştirmen (tek çağrı), nisbet denetçisi, düzeltme, gerekirse ikinci tur. Son taslak;
    `<birim>/kapi-son-<n>.txt`'ye de yazılır (iş dosyaları okur)."""
    if not (Y.out_dir(unit) / f"kapali-elestiri-taslak-{n}.json").exists():
        run("scripts/d1-duzelt.py", "kapali", unit, "--taslak", str(n), "--butun")
    if not (Y.out_dir(unit) / f"nisbet-taslak-{n}.json").exists():
        run("scripts/d1-nisbet.py", "denetle", unit, "--taslak", str(n))
    out = run("scripts/d1-duzelt.py", "kapi", unit, "--taslak", str(n))
    son = int(next(l.split(":")[1] for l in out.splitlines() if l.startswith("kapının son taslağı:")))
    (P.DRAFTS / unit / f"kapi-son-{n}.txt").write_text(f"{son}\n", encoding="utf-8")
    return son


def yaz(unit: str, surum: str = SURUM) -> int:
    cfg = P.UNITS.get(unit)
    if not cfg or not cfg.get("d5"):
        raise SystemExit(f"{unit} bir D5 birimi değil")
    started = time.monotonic()
    st = P.d5_state()["birimler"].get(unit, {})
    if st.get("bitti"):
        print(f"{unit}: bitti (son taslak {st['son_taslak']})")
        return st["son_taslak"]
    save_state(unit, surum=surum, basladi=st.get("basladi") or datetime.now().isoformat())
    run("scripts/d1-prova.py", "hazirla", unit)
    if not (P.OUT / unit / f"istem-hat-{surum}.md").exists():
        run("scripts/d1-hat.py", "hazirla", unit, "--surum", surum)
    run("scripts/d1-hat.py", "yazdir", unit, "--surum", surum, "--yoksa")
    n = draft_of_version(unit, surum)
    if n is None:
        raise SystemExit("taslak yazılamadı")
    save_state(unit, taslak=n)
    son = kapi(unit, n)
    save_state(unit, son_taslak=son)
    print(f"garaz: {garaz(unit, son)}")
    run("scripts/d1-hat.py", "izah", unit, "--taslak", str(son))
    run("scripts/d1-d5-sayfa.py", unit)
    yayimla(P.KEEP / "masa" / f"d5-{unit}.html")
    save_state(unit, bitti=datetime.now().isoformat(), maliyet=unit_cost(unit), alarmlar=alarmlar(unit, n, son),
               sure_dk=round((time.monotonic() - started) / 60 + (st.get("sure_dk") or 0)))
    s = P.d5_state()["birimler"][unit]
    print(f"== {unit} bitti: son taslak {son}, ≈{s['maliyet']} $, {s['sure_dk']} dk; alarm: {s['alarmlar'] or 'yok'}")
    durum_sayfasi()
    depo(f"D5: {unit} (son taslak {son})")
    return son


# ---------------------------------------------------------------- kalite alarmları (model çağrısız)
# Birim başına insan onayı yok (kullanıcının kararı): program her birimden sonra bakar; kuyruk durmaz, birim
# "okunmalı" işaretlenir, telefona düşer.
NISBET_ESIK = 0.08       # kapıdan sonra kalan nisbet hatası / hüküm
RED_ESIK = 0.5           # kapının reddettiği / karşılanması gereken not


def alarmlar(unit: str, n: int, son: int) -> list[str]:
    out = []
    d, keep = Y.out_dir(unit), P.DRAFTS / unit
    reg = json.loads((keep / "duzeltmeler.json").read_text(encoding="utf-8")) if (keep / "duzeltmeler.json").exists() else {}
    first = next((int(m) for m, r in reg.items() if r["kaynak"] == n and r["notlar"] == "kapi"), None)
    if first and (d / f"nisbet-taslak-{first}.json").exists():
        hs = json.loads((d / f"nisbet-taslak-{first}.json").read_text(encoding="utf-8"))["hukumler"]
        err = sum(h["hukum"] in ("asiyor", "kaynakta_yok") for h in hs)
        fixed = 0
        if son != first:
            fixed = json.loads((keep / f"taslak-{son}.json").read_text(encoding="utf-8"))["duzeltme"].get("karsilanan", 0)
        if hs and (err - fixed) / len(hs) > NISBET_ESIK:
            out.append(f"nisbet: kapıdan sonra {err - fixed}/{len(hs)} hata")
    if first:
        rep = json.loads((keep / f"taslak-{first}.json").read_text(encoding="utf-8"))["duzeltme"]
        need = rep.get("karsilanmasi_gereken") or 0
        if need and rep.get("reddedilen", 0) / need > RED_ESIK:
            out.append(f"kapı notların çoğunu reddetti ({rep['reddedilen']}/{need})")
        if rep.get("anilmayan"):
            out.append(f"kapıda anılmayan not: {len(rep['anilmayan'])}")
    blocks, sources = Y.draft_blocks(unit, son)
    secs = {a.split("/")[0] for a, *_ in blocks}
    missing = [k for k in ("V1", "V2", "V3") if k not in secs]
    if missing:
        out.append("eksik vecih: " + ", ".join(missing))
    ids = P.draft_sources(keep / f"taslak-{son}.jsonl") if (keep / f"taslak-{son}.jsonl").exists() else {}
    if not any(srv == "risale" for srv, _ in ids.values()):
        out.append("Risale-i Nur'dan kaynak yok")
    ar = sum(len(t) for _, lang, q, t in blocks if lang == "ar" and not q)
    others = [x["ar_harf"] for k, x in P.d5_state()["birimler"].items() if k != unit and x.get("ar_harf")]
    save_state(unit, ar_harf=ar)
    if len(others) >= 5:
        import statistics
        med = statistics.median(others)
        if ar < 0.5 * med or ar > 2 * med:
            out.append(f"Arapça uzunluğu aykırı ({ar} harf; ortanca {med:.0f})")
    izf = d / f"izah-taslak-{son}.json"
    if izf.exists():
        den = json.loads(izf.read_text(encoding="utf-8")).get("denetim", {})
        if den.get("eksik"):
            out.append(f"izahta eksik paragraf: {len(den['eksik'])}")
    else:
        out.append("izah yok")
    return out


SITE_KEY = Path.home() / ".ssh" / "site_gonder"      # sunucuda: yalnız /var/www/ozel/taslak'a yazar (rrsync -wo)
SITE_HOST = os.environ.get("D5_SITE_HOST", "root@100.108.174.19")
NTFY_FILE = Path.home() / ".d5-ntfy"                 # ntfy.sh konusu (tahmin edilemez ad; git'e girmez)


def yayimla(page: Path) -> None:
    """Okuma sayfası siteye (`/taslak/`, girişli): sunucuda kısıtlı anahtarla; anahtar yoksa (yerel) atlanır."""
    if not SITE_KEY.exists():
        print(f"siteye gönderilmedi (anahtar yok): scripts/taslak-gonder.sh {page.relative_to(ROOT)}")
        return
    p = subprocess.run(["rsync", "-rt", "--chmod=F640", "-e", f"ssh -i {SITE_KEY} -o BatchMode=yes", str(page),
                        f"{SITE_HOST}:/"], text=True, capture_output=True)
    print(f"https://risalemcp.com/taslak/{page.name}" if p.returncode == 0 else f"siteye gönderilemedi: {p.stderr.strip()}")


def bildir(baslik: str, metin: str) -> None:
    """Telefona bildirim (ntfy.sh; konu `D5_NTFY` ya da `~/.d5-ntfy`; yoksa yalnız günlük)."""
    topic = os.environ.get("D5_NTFY") or (NTFY_FILE.read_text().strip() if NTFY_FILE.exists() else None)
    if not topic:
        return
    import urllib.request
    try:
        # başlık HTTP başlığıdır (latin-1); Türkçesi bozulmasın diye başlık da gövdeye, ilk satır olarak
        urllib.request.urlopen(urllib.request.Request(f"https://ntfy.sh/{topic}",
                                                      data=f"{baslik}\n{metin}".encode("utf-8")), timeout=20)
    except OSError as e:
        print(f"bildirim gitmedi: {e}")


STOP = Path.home() / ".d5-dur"                     # `taslak-sunucu.sh dur`: birim bitince dur
STAGING = Path.home() / "kod-bekleyen"              # `taslak-sunucu.sh gonder` kuyruk sürerken kodu buraya koyar
HAFTA_ESIK = 0.90                                   # kullanıcının eşiği (2026-11-21): haftalık pencere %90


def durum_sayfasi() -> None:
    yayimla(S.durum_sayfasi())


def kod_guncelle() -> None:
    """Bekleyen kod varsa (birimler arasında) geçir ve kuyruğu yeni kodla yeniden başlat."""
    if not (STAGING / ".hazir").exists():
        return
    print("bekleyen kod geçiriliyor", flush=True)
    subprocess.run(["rsync", "-a", "--exclude", ".hazir", f"{STAGING}/", f"{ROOT}/"], check=True)
    subprocess.run(["uv", "sync", "--frozen", "-q"], cwd=ROOT, check=True)
    (STAGING / ".hazir").unlink()
    bildir("D5: kod güncellendi", "kuyruk yeni kodla sürüyor")
    os.execv(sys.executable, [sys.executable, *sys.argv])


def bekle_hafta(env: dict) -> bool:
    """Haftalık pencere eşiği aşıldıysa sıfırlanmaya kadar bekler (durdurma işaretine bakarak). False: durduruldu."""
    st = P.limit_probe(env, max_age=0)
    week = st.get("week")
    if week is None or week < HAFTA_ESIK:
        return True
    reset = st.get("week_reset") or time.time() + 6 * 3600
    when = datetime.fromtimestamp(reset)
    bildir("D5 bekliyor: haftalık kota", f"%{week * 100:.0f} ≥ %{HAFTA_ESIK * 100:.0f}; {when:%d.%m %H:%M}'de sürer")
    print(f"⏸ haftalık pencere %{week * 100:.0f}; {when:%d.%m %H:%M}'e kadar bekleniyor", flush=True)
    while time.time() < reset + P.LIMIT_MARGIN:
        if STOP.exists():
            return False
        time.sleep(300)
    return True


def gunluk_ozet() -> None:
    st = P.d5_state()
    last = st.get("son_ozet")
    if last and time.time() - last < 24 * 3600:
        return
    b = st["birimler"]
    units = [u["id"] for u in P.d5_units() if u["kaynak"] != "isarat"]
    done = [u for u in units if (b.get(u) or {}).get("bitti")]
    son24 = [u for u in done if time.time() - datetime.fromisoformat(b[u]["bitti"]).timestamp() < 24 * 3600]
    al = [u for u in done if b[u].get("alarmlar")]
    lim = json.loads(P.LIMIT_STATE.read_text(encoding="utf-8")) if P.LIMIT_STATE.exists() else {}
    bildir("D5 günlük özet", f"son 24 saatte {len(son24)} birim; toplam {len(done)}/{len(units)}; alarmlı {len(al)}; "
                             f"haftalık kota %{(lim.get('week') or 0) * 100:.0f}. https://risalemcp.com/taslak/d5.html")
    st["son_ozet"] = time.time()
    P.D5_STATE.write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")


def kuyruk(kadar: int | None, tavan: float | None) -> None:
    env = {k: v for k, v in os.environ.items() if k not in P.PARENT_ENV}
    done, spent = 0, 0.0
    if STOP.exists():
        print("durdurma işareti var (~/.d5-dur): kuyruk başlamadı; `taslak-sunucu.sh devam`")
        return
    bildir("D5 kuyruğu başladı", "sıradaki birimden sürüyor")
    while True:
        kod_guncelle()
        units = [u for u in P.d5_units() if u["kaynak"] != "isarat"]
        uid = next((u["id"] for u in units if not (P.d5_state()["birimler"].get(u["id"]) or {}).get("bitti")), None)
        if uid is None:
            bildir("D5 kuyruğu bitti", f"Bakara'nın {len(units)} birimi yazıldı")
            return
        if STOP.exists():
            bildir("D5 durdu", f"isteğinizle; sıradaki {uid}. Sürdürmek: devam")
            print(f"durdurma işareti: durdu (sıradaki {uid})")
            return
        if (kadar is not None and done >= kadar) or (tavan is not None and spent >= tavan):
            bildir("D5 durdu: sınır", f"bu koşuda {done} birim, {spent:.0f} $; sıradaki {uid}")
            return
        if not bekle_hafta(env):
            bildir("D5 durdu", f"isteğinizle (kota beklerken); sıradaki {uid}")
            return
        gunluk_ozet()
        P.UNITS.pop(uid, None)
        P._d5_register()                       # önceki birimin son taslağı kayda girsin
        before = (P.limit_probe(env, max_age=600) or {}).get("week")
        save_state(uid, hafta_once=before)
        try:
            yaz(uid)
        except SystemExit as e:
            depo(f"D5: {uid} yarıda ({e})")
            bildir(f"D5 hata: {uid}", f"{e}. Kuyruk durdu; düzeltilince devam")
            raise
        after = (P.limit_probe(env, max_age=0) or {}).get("week")
        save_state(uid, hafta_sonra=after)
        s = P.d5_state()["birimler"][uid]
        spent += s.get("maliyet") or 0
        done += 1
        al = s.get("alarmlar") or []
        bildir(f"D5: {uid} bitti" + (" ⚠" if al else ""),
               f"≈{s.get('maliyet')} $, {s.get('sure_dk')} dk" + (f"; alarm: {'; '.join(al)}" if al else "")
               + f". https://risalemcp.com/taslak/d5-{uid}.html")
        durum_sayfasi()
        depo(f"D5: {uid} kaydı")


def durum() -> None:
    st = P.d5_state()["birimler"]
    units = [u for u in P.d5_units() if u["kaynak"] != "isarat"]
    bitti = [u["id"] for u in units if (st.get(u["id"]) or {}).get("bitti")]
    print(f"D5 Bakara: {len(bitti)}/{len(units)} birim bitti; toplam ≈{sum((st[u].get('maliyet') or 0) for u in bitti):.0f} $")
    for u in units:
        s = st.get(u["id"])
        if s:
            print(f"  {u['id']:>8}: {'bitti' if s.get('bitti') else 'sürüyor'}, {s.get('surum')}, taslak {s.get('taslak')} → "
                  f"son {s.get('son_taslak')}, ≈{s.get('maliyet')} $, {s.get('sure_dk')} dk")
    nxt = next((u["id"] for u in units if u["id"] not in bitti), None)
    print(f"sıradaki: {nxt}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("yaz")
    p.add_argument("unit")
    p.add_argument("--surum", default=SURUM)
    p = sub.add_parser("kuyruk")
    p.add_argument("--kadar", type=int, help="en çok bu kadar birim")
    p.add_argument("--tavan", type=float, help="bu koşuda harcama tavanı ($, kullanım değeri)")
    sub.add_parser("durum")
    sub.add_parser("sayfa", help="durum sayfasını yeniden kur ve gönder")
    p = sub.add_parser("kapi", help="bir taslağa kalite kapısı d3 (kabul biriminde)")
    p.add_argument("unit")
    p.add_argument("--taslak", type=int, required=True)
    p = sub.add_parser("garaz", help="bir taslağın garaz özeti (Ek 3b; kabul biriminde önceki birim için)")
    p.add_argument("unit")
    p.add_argument("--taslak", type=int, required=True)
    a = ap.parse_args()
    if a.cmd == "yaz":
        yaz(a.unit, a.surum)
    elif a.cmd == "kuyruk":
        kuyruk(a.kadar, a.tavan)
    elif a.cmd == "sayfa":
        durum_sayfasi()
    elif a.cmd == "kapi":
        print(f"kapının son taslağı: {kapi(a.unit, a.taslak)}")
    elif a.cmd == "garaz":
        print(garaz(a.unit, a.taslak))
    else:
        durum()


if __name__ == "__main__":
    main()
