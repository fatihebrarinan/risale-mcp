"""S13.17 (3): sohbetin âyet çalışması kipinin dosyası (`verse_file`). Konu taramasının (`dosya.py`) kalıbı: dosyayı
sunucu mekanik olarak kurar, model okuyacağını seçer, cevapta anılmayanları sunucu ekler.

Kullanıcının kararları (2026-11-26):

- **Sabit tefsir yok:** âyeti en kapsamlı işleyen tefsirler önce okunur. Ölçü birimin bu âyete düşen payıdır: birimin
  kelime sayısı bölü kapsadığı âyet sayısı (çok âyetlik birim payını bölüşür). Birim yoksa âyetin eserde başka
  yerlerde alıntılanma sayısı ikinci ölçüdür. Pay kelimeyle ölçülür (`get_outline`'ın `words`'ü): cümle sayısı
  noktalaması seyrek baskılarda (Râzî'nin cümleleri çok uzun) kapsamı göstermiyordu. `read_first` en kapsamlı dört birimdir; cevapta tefsirler yine
  müellifin vefat sırasıyla durur.
- **Risale önce gelir** (eksen): âyetle bağ kuran yerler (türü, gücü, kanıt cümlesi; güçlüler önce) ve âyetin
  alıntılandığı bölümler (alıntı sayısıyla). Risale'nin bağı "tefsir" diye anılmaz.
- **Hadis yalnız okuyucu açarsa:** dosya hadis kütüphanesinin açık olup olmadığını söyler; kapalıysa ve hadis
  önemliyse model okuyucuya açmasını söyler.

Dosya modele kısa gider (tefsirin `find_ayah`'ı Âyetü'l-Kürsî'de 50 KB'tı, kesiliyordu); birimlerin metni gitmez.
"""

import asyncio
import json
import re

RISALE_TIES = 8              # dosyadaki en çok bağ
RISALE_PLACES = 8            # âyetin alıntılandığı en çok bölüm
READ_FIRST = 4               # önce okunacak tefsir birimi
_VERSES = re.compile(r"(\d+):(\d+)(?:\s*[-–]\s*(\d+))?")


def _verse_count(verses: str) -> int:
    m = _VERSES.search(verses or "")
    if not m:
        return 1
    return max(1, int(m.group(3) or m.group(2)) - int(m.group(2)) + 1)


def risale_part(library, sura: str, ayah: int) -> dict:
    """Âyetin Risale'deki bağları ve alıntılandığı bölümler."""
    first = library.find_ayah(sura, ayah, limit=50)
    rows, offset = list(first.get("results", [])), 50
    while offset < min(first.get("total", 0), 400):
        rows += library.find_ayah(sura, ayah, limit=50, offset=offset).get("results", [])
        offset += 50
    places: dict[str, dict] = {}
    for row in rows:
        section = row["id"].rsplit("/c", 1)[0]
        place = places.setdefault(section, {"section": section, "ref": row["ref"].rsplit(" › ", 1)[0],
                                            "sentences": 0, "first": row["id"]})
        place["sentences"] += 1
    ranked = sorted(places.values(), key=lambda p: -p["sentences"])
    ties = [{"section": t["section"], "ref": t["ref"], "kind": t["kind"], "strength": t["strength"],
             "scope": t["scope"], **({"evidence": t["evidence"]["id"]} if t.get("evidence") else {})}
            for t in first.get("links", [])[:RISALE_TIES]]
    return {"ties": ties, "quoted_sentences": first.get("total", 0), "quoted_places": len(places),
            "places": ranked[:RISALE_PLACES], "_all_places": ranked}


async def tefsir_part(client, sura: int, ayah: int) -> dict:
    """Tefsirlerde âyeti işleyen birimler, vefat sırasıyla, bu âyete düşen paylarıyla."""
    text, error = await client.call("find_ayah", {"sura": str(sura), "ayah": ayah})
    if error:
        return {"error": text[:300]}
    data = json.loads(text)
    works = []
    for w in data.get("classical_works", []):
        units = w.get("units", [])
        entry = {"work": w["work"], "title": w.get("title"), "author": w.get("author"),
                 "quoted_elsewhere": len([q for q in w.get("quotations", []) if not any(
                     q["id"].startswith(u["section"] + "/") for u in units)])}
        if units:
            unit = units[0]
            outline, oerr = await client.call("get_outline", {"section": unit["section"], "depth": 0})
            node = json.loads(outline) if not oerr else {}
            verses = _verse_count(unit.get("verses", ""))
            words = node.get("words") or node.get("sentences", 0) * 20     # eski sunucu: kelime sayısı yok
            entry.update({"unit": unit["section"], "ref": unit.get("ref"), "verses": unit.get("verses"),
                          "words": words, "share": round(words / verses)})
        works.append(entry)
    ranked = sorted((w for w in works if w.get("unit")), key=lambda w: -w["share"])
    return {"works": works, "read_first": [w["unit"] for w in ranked[:READ_FIRST]]}


async def verse_file(library, libraries, sura: str, ayah: int, hadis_open: bool) -> dict:
    """Modele giden dosya; `_page`: sayfanın cevaptan sonra eklediği liste için bütün yerler (modele gitmez)."""
    number = library._sura_number(sura)
    verse = library.ayahs(str(number), ayah)["ayahs"][0]
    translation = next((t for t in verse.get("translations", []) if t.get("text")), None)
    risale = await asyncio.to_thread(risale_part, library, str(number), ayah)
    out = {"verse": {"ref": verse["ref"], "text": verse["text"],
                     **({"translation": translation["text"], "translation_by": translation["translator"]}
                        if translation else {})},
           "risale": {k: v for k, v in risale.items() if not k.startswith("_")}}
    if "tefsir" in libraries.available():
        try:
            out["tefsir"] = await tefsir_part(libraries.clients["tefsir"], number, ayah)
        except Exception:
            import logging
            logging.exception("sohbet: âyet dosyasının tefsir kısmı")
            out["tefsir"] = {"error": "The Tafsir Library could not be reached; say so."}
    else:
        out["tefsir"] = {"error": "The Tafsir Library is not available on this page."}
    out["hadis"] = ("open: use the hadis_ tools if a hadith matters to the verse" if hadis_open else
                    "closed: if a hadith matters to this verse, tell the reader in one sentence that opening the "
                    "Hadis library above the question box gives more on it")
    out["_page"] = {"risale": risale["_all_places"], "tefsir": (out["tefsir"].get("works") or [])}
    return out


def verse_places(page: dict | None, sources: list[dict], read: set[str]) -> str:
    """Cevaptan sonra, kapalı ek: dosyada olup cevapta anılmayan ve okunmayan tefsir birimleri ve Risale'nin alıntı
    yerleri (mekanik liste; sırası hüküm değildir). `page`: dosyanın `_page`'i; `read`: okunan yerler (Risale'nin
    kimlikleri öneksiz, öbür kütüphaneninkiler `tefsir:` önekli)."""
    if not isinstance(page, dict) or not page:
        return ""
    cited = {str(s.get("id") or "").split("..")[0] for s in sources} | set(read)

    def used(place: str) -> bool:
        return any(c == place or c.startswith(place + "/") or place.startswith(c + "/") for c in cited if c)
    tefsir = [w for w in page.get("tefsir", []) if w.get("unit") and not used("tefsir:" + w["unit"])]
    risale = [p for p in page.get("risale", []) if not used(p["section"])]
    if not tefsir and not risale:
        return ""
    lines = []
    if tefsir:
        lines.append("- **Bu âyeti işleyen öbür tefsirler** (vefat sırasıyla; okunmadı): " + "; ".join(
            f"{w['author']}, {w['title']} ({w['words']} kelime)" for w in tefsir))
    if risale:
        lines.append("- **Âyetin Risale'de alıntılandığı öbür yerler:** " + "; ".join(
            f"{p['ref']} ({p['sentences']} cümle)" for p in risale[:15]) + (" …" if len(risale) > 15 else ""))
    return ":::ek Âyetin okunmayan öbür yerleri\n" + "\n".join(lines) + "\n:::"
