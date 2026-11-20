"""Ar-ge masasının sunucusuyla makine konuşması (S7.2): okuma görevi açmak, sonuçları taslak deposuna almak.

    uv run python scripts/masa-gorev.py ac data/d1/provalar/30/gorev-D5-kabul.json   # görevi aç
    uv run python scripts/masa-gorev.py al                                           # sonuçlar → data/d1/okumalar/

Jeton: `MASA_TOKEN` ortamda, yoksa `~/.masa-token` (sunucuda) ya da `.env`'deki `MASA_TOKEN=` (yerelde); git'e girmez.
`al` her şeyi `data/d1/okumalar/masa.json`'a yazar (okuyucu adı yok, sabit numara) ve biten okumaları eski dışa aktarma
biçiminde de verir (`data/d1/notlar/d1-tur-<birim>-<tur>-okuyucu<no>.json`): mevcut çözümleme onu okur. Seçimler
harften (A/B) taslak adına sunucunun saklı eşlemesiyle çevrilir.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get("MASA_URL", "https://risalemcp.com/taslak/api/")
KEEP = ROOT / "data" / "d1"


def token() -> str:
    if os.environ.get("MASA_TOKEN"):
        return os.environ["MASA_TOKEN"]
    f = Path.home() / ".masa-token"
    if f.exists():
        return f.read_text().strip()
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("MASA_TOKEN="):
                return line.split("=", 1)[1].strip()
    sys.exit("masa jetonu yok (MASA_TOKEN, ~/.masa-token ya da .env)")


def call(path: str, body: dict | None = None) -> dict:
    req = urllib.request.Request(BASE + path, method="POST" if body is not None else "GET",
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": f"Bearer {token()}", "Content-Type": "application/json",
                                          "User-Agent": "risale-mcp-masa"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def ac(path: Path) -> None:
    task = json.loads(path.read_text(encoding="utf-8"))
    r = call("gorev", task)
    print(f"{task['id']}: {'açıldı' if r.get('acildi') else 'zaten var'} → https://risalemcp.com{task.get('sayfa', '')}")


def al() -> None:
    data = call("disa")
    out = KEEP / "okumalar"
    out.mkdir(parents=True, exist_ok=True)
    (out / "masa.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    legacy = 0
    for t in data["okumalar"]:
        if t["durum"] != "bitti" or t["tur"] not in ("ab", "tek"):
            continue
        gizli = t.get("gizli") or {}
        tur = t.get("kaynak") or t["id"]
        by_reader: dict[int, dict] = {}
        for k in t["kararlar"]:
            by_reader.setdefault(k["okuyucu_no"], {})[k["yer"]] = k["veri"]     # sırayla: sonuncusu geçerli
        for no, yerler in by_reader.items():
            ab = {}
            for yer, v in yerler.items():
                v = dict(v)
                if t["tur"] == "ab" and v.get("secim") in ("A", "B"):
                    v["harf"], v["secim"] = v["secim"], gizli.get(v["secim"], v["secim"])
                ab[f"{t['birim']}|{tur}|{yer}"] = v
            rec = {"kind": "d1-tur-okuma-tek", "unit": t["birim"], "tur": tur, "a": gizli.get("A"), "b": gizli.get("B"),
                   "reader": f"okuyucu{no}", "exported": t.get("bitti"), "kaynak": "masa", "ab": ab}
            (KEEP / "notlar" / f"d1-tur-{t['birim']}-{tur}-okuyucu{no}.json").write_text(
                json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
            legacy += 1
    print(f"{len(data['okumalar'])} okuma, {len(data['notlar'])} not → {(out / 'masa.json').relative_to(ROOT)}; "
          f"{legacy} biten okuma notlar/'a")


def main() -> None:
    if len(sys.argv) >= 3 and sys.argv[1] == "ac":
        ac(Path(sys.argv[2]))
    elif len(sys.argv) == 2 and sys.argv[1] == "al":
        al()
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
