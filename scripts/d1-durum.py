"""Bir birimin durumu: neler var, sıradaki eksik adım, harcanan (kullanıcının kararı, 2026-11-19: oturum devri ve
pencere planlaması için; D5.0.1'deki tek komutla birim hattının ilk parçası). Model çağırmaz, yalnız dosyalara bakar.

    uv run python scripts/d1-durum.py 21-22          # bir birim
    uv run python scripts/d1-durum.py                # bütün birimler, kısa tablo

Sıradaki adım D15'in akışına göredir (PLANLAR.md D15). 2026-11-20'den beri hat h9, tek taslak: kurulum → envanter →
h9 → eşleştirme → İşârât karşılaştırması → kapalı eleştirmen → nisbet → aletlerin ayarı → okuma sayfası →
kullanıcının okuması. 21–22'de h10 ve h9 birlikteydi (eski akış). Geliştirme birimlerinde (D12–D14) akış başkaydı; onlarda yalnız var olan gösterilir.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

from risale_mcp.paths import ROOT

KEEP = ROOT / "data" / "d1"
PROVA = ROOT / "data" / "interim" / "d1-prova"
D15 = ("21-22", "26-27", "28")


def jload(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def cost_of(unit: str) -> tuple[float, dict]:
    """Birimin bütün model çağrılarının maliyeti: taslakların kaydı ve `yz/*.meta.json`."""
    d = KEEP / "provalar" / unit
    total, by = 0.0, {}
    for p in list(d.glob("taslak-*.json")) + list((d / "yz").glob("*.meta.json")):
        if p.name.endswith((".tarama.json",)):
            continue
        m = jload(p) or {}
        c = m.get("cost_usd")
        if not isinstance(c, (int, float)):
            continue
        kind = "taslak" if p.name.startswith("taslak-") else p.name.split("-taslak")[0].split(".meta")[0]
        kind = kind.rsplit("-", 1)[0] if kind.startswith(("eslestirme", "kor-olcu", "sina")) else kind
        by[kind] = by.get(kind, 0) + c
        total += c
    return total, by


def drafts(unit: str) -> list[dict]:
    out = []
    for p in sorted((KEEP / "provalar" / unit).glob("taslak-*.json"), key=lambda p: int(p.stem.split("-")[1])
                    if p.stem.split("-")[1].isdigit() else 0):
        if not p.stem.split("-")[1].isdigit():
            continue
        m = jload(p) or {}
        out.append({"n": int(p.stem.split("-")[1]), "surum": m.get("surum") or m.get("istem"), "model": m.get("model"),
                    "at": (m.get("at") or "")[:16], "cost": m.get("cost_usd")})
    return out


def state(unit: str) -> dict:
    d, yz = KEEP / "provalar" / unit, KEEP / "provalar" / unit / "yz"
    env = jload(yz / "envanter.json")
    ds = drafts(unit)
    per = {}
    for x in ds:
        n = x["n"]
        isr = jload(yz / f"isarat-karsilastirma-taslak-{n}.json")
        per[n] = {
            "eslestirme": (yz / f"eslestirme-taslak-{n}-opus.json").exists(),
            "isarat": (isr or {}).get("butun", {}).get("hukum") if isr else None,
            "kapali": (yz / f"kapali-elestiri-taslak-{n}.json").exists(),
            "nisbet": (yz / f"nisbet-taslak-{n}.json").exists(),
            "ayar": (yz / f"not-karsilastirma-taslak-{n}-isarat.json").exists(),
            "tarama": (d / f"taslak-{n}.tarama.md").exists(),
        }
    kor = {}
    for p in yz.glob("kor-olcu-*.json"):
        if p.name.endswith(".meta.json"):
            continue
        k = jload(p) or {}
        meta = jload(p.with_name(p.stem + ".meta.json")) or {}
        b = k.get("butun", {})
        win = {"A": meta.get("A"), "B": meta.get("B")}.get(b.get("tercih"), b.get("tercih"))
        kor[p.stem.removeprefix("kor-olcu-")] = f"taslak {win} ({b.get('guc')})" if isinstance(win, int) else str(win)
    turs = sorted(p.stem.removeprefix("tur-") for p in d.glob("tur-*.json"))
    reads = sorted(p.name for p in (KEEP / "notlar").glob(f"d1-tur-{unit}-*.json"))
    return {"kurulum": (PROVA / unit / "risale.db").exists(), "envanter": len(env["kalemler"]) if env else None,
            "taslaklar": ds, "olcu": per, "kor": kor, "turlar": turs, "okumalar": reads}


def next_step(unit: str, s: dict) -> str:
    """D15 akışında ilk eksik adım ve komutu."""
    if not s["kurulum"]:
        return f"birim kaydı (`d1-prova.UNITS`) ve `uv run python scripts/d1-prova.py hazirla {unit}`"
    if s["envanter"] is None:
        return f"`uv run python scripts/d1-yz.py envanter {unit}`"
    by_surum = {x["surum"]: x["n"] for x in s["taslaklar"]}
    if unit != "21-22":                  # 2026-11-20'den beri hat h9, tek taslak (D15.2, D15.3)
        if "h9" not in by_surum:
            return (f"`uv run python scripts/d1-hat.py hazirla {unit} --surum h9` ve "
                    f"`yazdir {unit} --surum h9 --yoksa`")
        n, o = by_surum["h9"], s["olcu"][by_surum["h9"]]
        for key, cmd in (("eslestirme", f"d1-yz.py eslestir {unit} --taslak {n} --modeller opus"),
                         ("isarat", f"d1-duzelt.py isarat {unit} --taslak {n}"),
                         ("kapali", f"d1-duzelt.py kapali {unit} --taslak {n} --butun"),
                         ("nisbet", f"d1-nisbet.py denetle {unit} --taslak {n}"),
                         ("ayar", f"d1-duzelt.py notlar {unit} --taslak {n} --acik isarat")):
            if not o[key]:
                return f"`uv run python scripts/{cmd}` (h9)"
        if not s["turlar"]:
            return "okuma sayfası (tek taslak): kartlar `provalar/<birim>/yerler-<tur>.json`, `d1-tur.py okuma-tek`, `taslak-gonder.sh`"
        if not s["okumalar"]:
            return "kullanıcının okuması (dışa aktarılan dosya `data/d1/notlar/`'a)"
        return "dilimin raporu ve PLANLAR.md"
    if "h10" not in by_surum:
        return (f"`uv run python scripts/d1-kalip.py tablo {unit}`, `d1-hat.py hazirla {unit} --tarama`, "
                f"`d1-hat.py yazdir {unit} --surum h10`")
    if "h9" not in by_surum:
        return f"`uv run python scripts/d1-hat.py hazirla {unit} --surum h9` ve `yazdir {unit} --surum h9`"
    for surum in ("h10", "h9"):
        n, o = by_surum[surum], s["olcu"][by_surum[surum]]
        if not o["eslestirme"]:
            return f"`uv run python scripts/d1-yz.py eslestir {unit} --taslak {n} --modeller opus` ({surum})"
        if not o["isarat"]:
            return f"`uv run python scripts/d1-duzelt.py isarat {unit} --taslak {n}` ({surum})"
    n, o = by_surum["h10"], s["olcu"][by_surum["h10"]]
    for key, cmd in (("kapali", f"d1-duzelt.py kapali {unit} --taslak {n} --butun"),
                     ("nisbet", f"d1-nisbet.py denetle {unit} --taslak {n}"),
                     ("ayar", f"d1-duzelt.py notlar {unit} --taslak {n} --acik isarat")):
        if not o[key]:
            return f"`uv run python scripts/{cmd}` (h10)"
    a, b = sorted((by_surum["h10"], by_surum["h9"]))
    if f"{a}-{b}" not in s["kor"]:
        return f"`uv run python scripts/d1-duzelt.py olc {unit} --cift {a}-{b}` (kör A/B)"
    if not s["turlar"]:
        return "okuma sayfası: kartları seç (`provalar/<birim>/yerler-<tur>.json`), `d1-tur.py okuma-…`, `taslak-gonder.sh`"
    if not s["okumalar"]:
        return "kullanıcının okuması (dışa aktarılan dosya `data/d1/notlar/`'a)"
    return "dilimin raporu ve PLANLAR.md"


def show(unit: str) -> None:
    s = state(unit)
    total, by = cost_of(unit)
    print(f"# {unit}")
    print(f"- kurulum (prova veritabanı): {'var' if s['kurulum'] else 'yok'}; envanter: "
          + (f"{s['envanter']} kalem" if s["envanter"] else "yok"))
    for x in s["taslaklar"]:
        o = s["olcu"][x["n"]]
        marks = [k for k in ("eslestirme", "kapali", "nisbet", "ayar", "tarama") if o[k]]
        print(f"- taslak {x['n']}: {x['surum']}, {x['at']}, ≈{(x['cost'] or 0):.2f} $; "
              + (", ".join(marks) or "ölçü yok") + (f"; İşârât karşılaştırması: {o['isarat']}" if o["isarat"] else ""))
    for k, v in sorted(s["kor"].items()):
        print(f"- kör A/B {k}: {v}")
    print(f"- okuma sayfaları: {', '.join(s['turlar']) or 'yok'}; kullanıcının okuması: {len(s['okumalar'])} dosya")
    print(f"- harcanan ≈{total:.2f} $ (" + ", ".join(f"{k} {v:.2f}" for k, v in sorted(by.items(), key=lambda kv: -kv[1])) + ")")
    if unit in D15:
        print(f"- **sıradaki:** {next_step(unit, s)}")


def main() -> None:
    units = sys.argv[1:]
    if units:
        for u in units:
            show(u)
            print()
        return
    print(f"Birimler ({datetime.now():%Y-%m-%d %H:%M})\n")
    print("| Birim | Envanter | Taslaklar | Okuma | Harcanan | Sıradaki (D15) |")
    print("|---|---|---|---|---|---|")
    for d in sorted((KEEP / "provalar").iterdir(), key=lambda p: [int(x) for x in p.name.split("-")]):
        s = state(d.name)
        total, _ = cost_of(d.name)
        ts = ", ".join(f"{x['n']}:{x['surum']}" for x in s["taslaklar"])
        print(f"| {d.name} | {s['envanter'] or '—'} | {ts} | {len(s['okumalar'])} | ≈{total:.0f} $ | "
              f"{next_step(d.name, s) if d.name in D15 else ''} |")


if __name__ == "__main__":
    main()
