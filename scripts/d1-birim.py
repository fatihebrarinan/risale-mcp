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

GARAZ_D5 = P.KEEP / "garaz" / "d5-bakara.json"
GARAZ_ISTEM = """Aşağıda Bakara Sûresi {ayahs}. âyetler için yazılmış bir yapay zekâ taslağı var (İşârâtü'l-İ'câz usulüyle;
Arapça). **İki cümleyi geçmeyen Türkçe bir özet** yaz: bu âyetler neyi anlatıyor ve taslağa göre **asıl garazı**
(maksadı) ne. Kurallar: yalnız bu âyetler; taslağın **sonraki âyetlere** dair söylediğini (onları hazırlaması, onlarla
bağı) **yazma**; alıntı yapma; kendi yorumunu katma. Cevabın yalnız şu JSON: {{"ozet": "..."}}

{taslak}
"""


def run(*args: str) -> str:
    """Bir hattın komutu; çıktısı günlüğe akar, döndürülür. Hata işi durdurur."""
    cmd = ["uv", "run", "python", *args]
    print(f"$ {' '.join(args)}", flush=True)
    p = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    sys.stdout.write(p.stdout)
    sys.stdout.flush()
    if p.returncode:
        raise SystemExit(f"adım başarısız ({p.returncode}): {' '.join(args)}")
    return p.stdout


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
    if not (Y.out_dir(unit) / f"kapali-elestiri-taslak-{n}.json").exists():
        run("scripts/d1-duzelt.py", "kapali", unit, "--taslak", str(n), "--butun")
    if not (Y.out_dir(unit) / f"nisbet-taslak-{n}.json").exists():
        run("scripts/d1-nisbet.py", "denetle", unit, "--taslak", str(n))
    out = run("scripts/d1-duzelt.py", "kapi", unit, "--taslak", str(n))
    son = int(next(l.split(":")[1] for l in out.splitlines() if l.startswith("kapının son taslağı:")))
    save_state(unit, son_taslak=son)
    print(f"garaz: {garaz(unit, son)}")
    run("scripts/d1-hat.py", "izah", unit, "--taslak", str(son))
    if (ROOT / "scripts" / "d1-d5-sayfa.py").exists():
        run("scripts/d1-d5-sayfa.py", unit)
    save_state(unit, bitti=datetime.now().isoformat(), maliyet=unit_cost(unit),
               sure_dk=round((time.monotonic() - started) / 60 + (st.get("sure_dk") or 0)))
    s = P.d5_state()["birimler"][unit]
    print(f"== {unit} bitti: son taslak {son}, ≈{s['maliyet']} $, {s['sure_dk']} dk")
    return son


def bildir(baslik: str, metin: str) -> None:
    """Telefona bildirim (`D5_NTFY`: ntfy.sh konusu; yoksa yalnız günlük)."""
    topic = os.environ.get("D5_NTFY")
    if not topic:
        return
    import urllib.request
    try:
        urllib.request.urlopen(urllib.request.Request(f"https://ntfy.sh/{topic}", data=metin.encode(),
                                                      headers={"Title": baslik.encode("utf-8").decode("latin-1", "ignore")}),
                               timeout=20)
    except OSError as e:
        print(f"bildirim gitmedi: {e}")


def kuyruk(kadar: int | None, tavan: float | None) -> None:
    done = 0
    spent = 0.0
    for u in P.d5_units():
        if u["kaynak"] == "isarat":
            continue
        uid = u["id"]
        if (P.d5_state()["birimler"].get(uid) or {}).get("bitti"):
            continue
        if kadar is not None and done >= kadar:
            break
        if tavan is not None and spent >= tavan:
            bildir("D5 durdu: harcama tavanı", f"{spent:.0f} $ ≥ {tavan:.0f} $; sıradaki {uid}")
            print(f"harcama tavanı: {spent:.2f} $ ≥ {tavan} $; durdu (sıradaki {uid})")
            return
        P._d5_register()                       # önceki birimin son taslağı kayda girsin
        P.UNITS.pop(uid, None)
        P._d5_register()
        try:
            yaz(uid)
        except SystemExit as e:
            bildir(f"D5 hata: {uid}", str(e))
            raise
        s = P.d5_state()["birimler"][uid]
        spent += s.get("maliyet") or 0
        done += 1
        bildir(f"D5: {uid} bitti", f"≈{s.get('maliyet')} $, {s.get('sure_dk')} dk; bu koşuda {done} birim, {spent:.0f} $")
    bildir("D5 kuyruğu bitti", f"{done} birim, {spent:.0f} $")


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
    p = sub.add_parser("garaz", help="bir taslağın garaz özeti (Ek 3b; kabul biriminde önceki birim için)")
    p.add_argument("unit")
    p.add_argument("--taslak", type=int, required=True)
    a = ap.parse_args()
    if a.cmd == "yaz":
        yaz(a.unit, a.surum)
    elif a.cmd == "kuyruk":
        kuyruk(a.kadar, a.tavan)
    elif a.cmd == "garaz":
        print(garaz(a.unit, a.taslak))
    else:
        durum()


if __name__ == "__main__":
    main()
