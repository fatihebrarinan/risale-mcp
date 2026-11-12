#!/usr/bin/env python3
"""docs/d1/usul-ozeti.md'deki alıntıları veritabanıyla denetler (PLANLAR.md D1).

    python3 scripts/d1-usul-denetim.py                               # usul özeti
    python3 scripts/d1-usul-denetim.py docs/d1/birim-cizelgesi.md    # yalnız adresler (F/, B/ kısaltmalı)

Her `> "…"` alıntısı, ardından gelen `— … (`kimlik`)` satırındaki cümlenin metniyle birebir aynı olmalı; satırdaki
yol (aynı yer denmediyse) cümlenin `ref`'iyle aynı olmalı; belgede geçen bütün cümle kimlikleri var olmalı.
"""
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
db = sqlite3.connect(ROOT / "data" / "dist" / "genel" / "risale.db")
target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "docs" / "d1" / "usul-ozeti.md"
lines = (target if target.is_absolute() else ROOT / target).read_text(encoding="utf-8").split("\n")
SHORT = {"F/": "isaratul-icaz-arabi/sure-i-fatiha/", "B/": "isaratul-icaz-arabi/sure-i-bakara/"}
bad = quotes = 0
for n, line in enumerate(lines):
    m = re.fullmatch(r'> "(.*)"', line)
    if not m or line.startswith("> **"):
        continue
    cite = next((l for l in lines[n + 1:n + 4] if l.startswith("— ")), None)
    ident = re.search(r"\(`([^`]+)`\)", cite or "")
    if not ident:
        print(f"satır {n + 1}: alıntının adresi yok"); bad += 1; continue
    row = db.execute("select text, ref from sentences where id = ?", (ident.group(1),)).fetchone()
    quotes += 1
    if not row:
        print(f"satır {n + 1}: kimlik yok: {ident.group(1)}"); bad += 1
    elif row[0] != m.group(1):
        print(f"satır {n + 1}: metin farklı: {ident.group(1)}\n  belge: {m.group(1)[:90]}\n  veri : {row[0][:90]}"); bad += 1
    elif not cite.startswith("— aynı yer") and cite[2:cite.index(" (`")] != row[1]:
        print(f"satır {n + 1}: yol farklı\n  belge: {cite[2:cite.index(' (`')]}\n  veri : {row[1]}"); bad += 1
ids = 0
for ident in sorted(set(re.findall(r"`(isaratul-icaz[\w/-]*/c\d+(?:\.\.c\d+)?)`", "\n".join(lines)))):
    first, _, last = ident.partition("..")
    for i in filter(None, (first, first.rsplit("/", 1)[0] + "/" + last if last else "")):
        ids += 1
        if not db.execute("select 1 from sentences where id = ?", (i,)).fetchone():
            print(f"kimlik yok: {i}"); bad += 1
last = None
for m in re.finditer(r"`([FB]/[\w/-]*c\d+)`|\.\.`(c\d+)`", "\n".join(lines)):
    if m.group(1):
        last = SHORT[m.group(1)[:2]] + m.group(1)[2:]
        ident = last
    else:
        ident = last.rsplit("/", 1)[0] + "/" + m.group(2)
    ids += 1
    if not db.execute("select 1 from sentences where id = ?", (ident,)).fetchone():
        print(f"kimlik yok: {ident}"); bad += 1
print(f"{quotes} alıntı, {ids} kimlik denetlendi; {bad} sorun")
sys.exit(1 if bad else 0)
