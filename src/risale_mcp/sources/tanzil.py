"""tanzil.net: Kur'ân-ı Kerîm'in Arapça metni ve Türkçe mealleri.

Metin şartları (tanzil.net/download): metin değiştirilmeden kopyalanıp dağıtılabilir; kullanılan
yerde kaynağın (Tanzil Project) açıkça belirtilmesi ve tanzil.net'e bağlantı verilmesi gerekir.
Meal şartları (tanzil.net/trans): yalnızca ticari olmayan kullanım; başka kullanım için mütercimden ya
da yayınevinden izin gerekir. Kullanım kişiseldir.

Arapça metin üç biçimde indirilir:
- `uthmani`: Medine Mushafı hattı, harekeli; kullanıcıya gösterilen metin budur.
- `simple`: imlâî yazım, harekeli.
- `simple-clean`: harekesiz ve işaretsiz; yalnızca Risale'deki âyetleri metinle eşlemek için.

Ham arşiv (`data/raw/tanzil/`):
    manifest.json, quran-<biçim>.xml, <meal>.xml (tr.diyanet, tr.vakfi)
"""

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Callable

from risale_mcp.sources.archive import fetch_cached, read_raw, write_manifest
from risale_mcp.sources.http import PoliteClient

BASE_URL = "https://tanzil.net"
TEXT_TYPES = ("uthmani", "simple", "simple-clean")
# Tanzil'in kimliği -> açıklama. İkisi de Diyanet'in mealidir: İşleri Başkanlığı ve Vakfı.
TRANSLATIONS = {
    "tr.diyanet": "Diyanet İşleri Başkanlığı meali",
    "tr.vakfi": "Türkiye Diyanet Vakfı meali",
}
SURAS, AYAHS = 114, 6236
ATTRIBUTION = "Tanzil Project (tanzil.net)"


def text_url(text_type: str) -> str:
    # İndirme sayfasındaki varsayılan seçenekler: vakıf ve secde işaretleri, elif ve tatvil düzeltmesi.
    return (f"{BASE_URL}/pub/download/index.php?marks=true&sajdah=true&alef=true&tatweel=true"
            f"&quranType={text_type}&outType=xml&agree=true")


def translation_url(trans_id: str) -> str:
    return f"{BASE_URL}/trans/?transID={trans_id}&type=xml"


def text_path(root: Path, text_type: str) -> Path:
    return root / f"quran-{text_type}.xml"


def translation_path(root: Path, trans_id: str) -> Path:
    return root / f"{trans_id}.xml"


def read_xml(path: Path) -> ET.Element:
    # Meal dosyalarının başlık açıklaması "# ----" satırları taşır; XML açıklamasında "--" geçersizdir.
    text = re.sub(r"<!--.*?-->", "", read_raw(path).decode("utf-8"), count=1, flags=re.S)
    return ET.fromstring(text)


def ayahs(root_element: ET.Element) -> dict[tuple[int, int], str]:
    """`<sura index><aya index text/>` biçimindeki dosyadan (sûre, âyet) -> metin."""
    return {(int(sura.get("index")), int(aya.get("index"))): aya.get("text")
            for sura in root_element.iter("sura") for aya in sura.iter("aya")}


def fetch_book(book: str, root: Path, client: PoliteClient, *,
               refresh: bool = False, log: Callable[[str], None] = print) -> None:
    files = {}
    for text_type in TEXT_TYPES:
        url = text_url(text_type)
        fetch_cached(text_path(root, text_type), url, client, refresh)
        files[text_path(root, text_type).name] = url
    for trans_id in TRANSLATIONS:
        url = translation_url(trans_id)
        fetch_cached(translation_path(root, trans_id), url, client, refresh)
        files[translation_path(root, trans_id).name] = url
    write_manifest(root / "manifest.json", site="tanzil", book=book, files=files, attribution=ATTRIBUTION)
    log(f"tanzil: {len(files)} dosya")


def check_book(book: str, root: Path) -> tuple[list[str], bool]:
    """Her dosyada 114 sûre ve 6236 âyet olmalı; bütün dosyalar aynı âyetleri taşımalı."""
    if not (root / "manifest.json").exists():
        return ["tanzil: indirilmemiş"], False
    files = json.loads((root / "manifest.json").read_text(encoding="utf-8"))["files"]
    lines, keys, ok = [f"tanzil: {len(files)} dosya"], None, True
    for name in files:
        found = ayahs(read_xml(root / name))
        suras = len({sura for sura, _ in found})
        empty = sum(not text for text in found.values())
        same = keys is None or set(found) == keys
        keys = keys or set(found)
        good = suras == SURAS and len(found) == AYAHS and not empty and same
        ok &= good
        lines.append(f"  {name:24} {suras} sûre, {len(found)} âyet, boş {empty}{'' if same else ', ÂYETLER FARKLI'}"
                     f"{'' if good else '  <-- sorun'}")
    return lines, ok
