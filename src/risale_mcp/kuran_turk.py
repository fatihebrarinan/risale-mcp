"""Kur'ân'ın Türk hattı: risaleoku'nun Kur'ân'ından (anahtar `kuran`) âyet başına metin.

Kullanıcının kararı (2026-11-21): masada ve okuma platformunda Kur'ân metni varsayılan olarak Türk hattıyla gösterilir,
Medine Mushafı hattı (Tanzil, `quran.json`) seçilebilir. İkisi aynı kıraattir (Hafs), yalnız imlâ ve işaret sistemi
farklıdır (vasıl elifi, okunmayan harf işareti, hemze, çeker esre, Secâvendî durakları). Asıl katman yine Tanzil'dir:
adres, eşleme ve araçlar ona dayanır; bu dosya yalnız görüntü içindir ve MCP araçlarına girmez.

Kaynak biçimi (`data/raw/risaleoku_app/kuran/text.txt.gz`): `#n` sayfa, `<114-Nâs>` sûre başı, `~…|@` satır;
sûrenin ilk satırı başlıktır (`~١١٤﴾ الناس`), Fâtiha dışında âyetten önce Besmele satırı gelir (âyet değildir, atılır).
Âyet `﴿n﴾` ile biter; sayfa sonu âyetin ortasına düşebilir (satırlar boşlukla birleşir). `ڛ ڝ ڞ ڟ` bu baskının cüz ve
hizb işaretleridir (kendi yazı tipinde), metne girmez. Sonda Hatim Duası vardır, alınmaz.

Denetim: her âyetin harf iskeleti (`quran.skeleton`) Tanzil'inkiyle aynı olmalı. Türk hattının üç gerçek imlâ farkı
(21:88 نُنْجِى, 63:10 مِمَّا, 72:16 وَاَنْ لَوِ) iskelette de farklıdır; benzerlik %90'ı geçerse alınır, `rasm`'da listelenir.
Tutmayan âyet yazılmaz (`null`, görüntü Medine hattına düşer).

    uv run python -m risale_mcp.kuran_turk      # data/library/kuran/turk.json
"""
from __future__ import annotations

import difflib
import gzip
import json
import re

from . import paths
from .quran import skeleton

RAW = paths.DATA_DIR / "raw" / "risaleoku_app" / "kuran" / "text.txt.gz"
OUT = paths.DATA_DIR / "library" / "kuran" / "turk.json"
QURAN = paths.DATA_DIR / "library" / "kuran" / "quran.json"
MARKERS = str.maketrans("", "", "ڛڝڞڟ")
SURA = re.compile(r"^<(\d+)-")
TITLE = re.compile(r"^[٠-٩]+﴾")
END = re.compile(r"﴿([٠-٩]+)﴾")
BESMELE = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّح۪يمِ"
SOURCE = {"name": "risaleoku.com, Kur'an-ı Kerim (Türk hattı)", "url": "https://risaleoku.com",
          "note": "Görüntü içindir; adres ve eşleme Tanzil metnine (Medine Mushafı) dayanır."}


def parse() -> dict[int, list[str]]:
    suras: dict[int, list[str]] = {}
    cur, buf = None, []

    def close():
        if cur is None:
            return
        text = " ".join(buf).translate(MARKERS)
        text = re.sub(r"\s+", " ", text).strip()
        words = text.split(" ")
        if cur != 1 and skeleton(" ".join(words[:4])) == skeleton(BESMELE):
            text = " ".join(words[4:])
        ayahs, pos = [], 0
        for m in END.finditer(text):
            n = int(m.group(1).translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")))
            if n != len(ayahs) + 1:
                raise ValueError(f"{cur}: beklenen {len(ayahs) + 1}, gelen {n}")
            ayahs.append(text[pos:m.start()].strip())
            pos = m.end()
        suras[cur] = ayahs

    for line in gzip.open(RAW, "rt", encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("<"):
            close()
            m = SURA.match(line)
            cur, buf = (int(m.group(1)) if m else None), []
            continue
        if cur is None or not line.startswith("~"):
            continue
        body = line[1:].replace("|@", " ").strip()
        if not buf and TITLE.match(body):
            continue
        buf.append(body)
    close()
    return suras


def build() -> dict:
    suras = parse()
    quran = json.loads(QURAN.read_text(encoding="utf-8"))
    out, bad, rasm = {}, [], []
    for s in quran["suras"]:
        turk = suras.get(s["number"], [])
        if len(turk) != len(s["ayahs"]):
            bad.append(f"{s['number']}: âyet sayısı {len(turk)} / {len(s['ayahs'])}")
        row = []
        for a in s["ayahs"]:
            t = turk[a["ayah"] - 1] if a["ayah"] <= len(turk) else ""
            k1, k2 = skeleton(t), skeleton(a["text"])
            if t and k1 == k2:
                row.append(t)
            elif t and difflib.SequenceMatcher(None, k1, k2).ratio() >= 0.9:   # Türk hattının imlâ farkı (مِمَّا / مِن مَّا)
                row.append(t)
                rasm.append(f"{s['number']}:{a['ayah']}")
            else:
                row.append(None)
                bad.append(f"{s['number']}:{a['ayah']}")
        out[str(s["number"])] = row
    return {"source": SOURCE, "suras": out, "unmatched": bad, "rasm": rasm}


def main() -> None:
    data = build()
    OUT.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    n = sum(1 for r in data["suras"].values() for t in r if t)
    print(f"{OUT}: {n} âyet; imlâ farkıyla {len(data['rasm'])} ({', '.join(data['rasm'])}); "
          f"iskeleti tutmayan {len(data['unmatched'])}: {', '.join(data['unmatched'][:40])}")


if __name__ == "__main__":
    main()
