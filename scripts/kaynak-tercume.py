"""S7c.5: taslakların andığı tefsir ve klasik eser yerlerinin Türkçesi (kullanıcının kararı, 2026-11-21: "tefsirler için
şimdilik yalnız taslağın andığı yerler"; bütün tefsir birimlerinin tercümesi sonraya).

- Kaynak: bir birimin bütün taslaklarının kaynakçasında sunucusu `tefsir` ya da `klasik` olan yerler (kimlik ve metin;
  `d1-prova.draft_sources`, `SourceTexts`). Metin değiştirilmez; tercüme yanında ayrı durur.
- Tercüme hafif modelle (Sonnet, araçsız), "Yapay zekâ tercümesi" damgasıyla gösterilir; müellife mal edilmez, alıntının
  içine girmez. Lisans: OpenITI metinleri CC BY-NC-SA 4.0; tercüme türetilmiş eserdir (ticari değil, aynı lisans,
  kaynak gösterilir): sayfalar bunu tercümenin yanında yazar.
- Depo: `data/d1/tercume/kaynaklar.json` {kimlik: {ar, tr, model, at}} (kimliğe göre ortak; aynı yer başka taslakta ya
  da birimde anılırsa yeniden çevrilmez). Yeniden üretilebilir ama ücretlidir: taslak deposunda durur.

    uv run python scripts/kaynak-tercume.py 28 30          # eksikleri çevir (model; d1-arka.sh ile başlatılır)
    uv run python scripts/kaynak-tercume.py --hepsi --say  # model çağırmadan: kaç yer eksik
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import datetime
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


Y = _load("d1_yz", "d1-yz.py")
P = Y.P
STORE = P.KEEP / "tercume" / "kaynaklar.json"
SERVERS = ("tefsir", "klasik")
BATCH = 30
ISTEM = """Aşağıda klasik Arapça tefsir ve belâgat eserlerinden numaralı parçalar var. Her birini Türkçeye çevir.

Kurallar: anlamı sadık ver, eklemeden ve özetlemeden; terimleri (istiare, kinaye, takdim, hasr, i'rab terimleri) yerleşik
Türkçe karşılıklarıyla ya da olduğu gibi kullan; âyet ve hadis alıntılarını Arapçasıyla bırakıp yanına kısa meal koyma;
müellifin "قلت / فإن قلت" gibi kalıplarını "Derim ki / Eğer dersen" diye ver. Dil sade, günümüz Türkçesi.

Yalnız JSON döndür: {{"1": "tercüme", "2": "tercüme", ...}}

{parcalar}
"""


def load_store() -> dict:
    return json.loads(STORE.read_text(encoding="utf-8")) if STORE.exists() else {}


def cited(unit: str) -> dict[str, str]:
    """Birimin taslaklarının andığı tefsir ve klasik yerler: {kimlik: Arapça metin}."""
    texts = P.SourceTexts(unit)
    out = {}
    for n in Y.drafts_of(unit):
        log = P.DRAFTS / unit / f"taslak-{n}.jsonl"
        if not log.exists():
            continue
        _, cites = Y.draft_blocks(unit, n)
        for k, (server, sid) in P.draft_sources(log).items():
            if server in SERVERS and sid and sid not in out:
                t = texts.text(server, sid, (cites.get(k) or "").split(" · ")[0])
                if t:
                    out[sid] = t
    return out


def translate(unit: str, todo: dict[str, str], store: dict) -> int:
    done = 0
    items = list(todo.items())
    for b in range(0, len(items), BATCH):
        part = items[b:b + BATCH]
        prompt = ISTEM.format(parcalar="\n\n".join(f"{i + 1}. {t}" for i, (_, t) in enumerate(part)))
        stem = Y.out_dir(unit) / f"kaynak-tercume-{datetime.now():%Y%m%d-%H%M%S}-{b // BATCH + 1}"
        res = Y.run_model(prompt, "sonnet", stem, {"gorev": "kaynak-tercume", "birim": unit, "parca": len(part)})
        if not res:
            continue
        for i, (sid, ar) in enumerate(part):
            tr = res.get(str(i + 1))
            if isinstance(tr, str) and tr.strip():
                store[sid] = {"ar": ar, "tr": tr.strip(), "model": Y.MODELS["sonnet"], "at": datetime.now().isoformat()}
                done += 1
        STORE.parent.mkdir(parents=True, exist_ok=True)
        STORE.write_text(json.dumps(store, ensure_ascii=False, indent=1), encoding="utf-8")   # her partiden sonra
    return done


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("units", nargs="*")
    ap.add_argument("--hepsi", action="store_true", help="taslağı olan bütün birimler")
    ap.add_argument("--say", action="store_true", help="model çağırma, eksikleri say")
    a = ap.parse_args()
    units = a.units
    if a.hepsi:
        units = [u for u in P.UNITS if (P.DRAFTS / u).is_dir() and Y.drafts_of(u)]
    store = load_store()
    for u in units:
        c = cited(u)
        todo = {sid: t for sid, t in c.items() if sid not in store or store[sid].get("ar") != t}
        words = sum(len(t.split()) for t in todo.values())
        print(f"{u}: {len(c)} yer anılmış, {len(todo)} çevrilecek (≈{words} kelime)", flush=True)
        if todo and not a.say:
            print(f"  {translate(u, todo, store)} çevrildi", flush=True)


if __name__ == "__main__":
    main()
