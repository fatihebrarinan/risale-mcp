"""api.quran.com: Medine Mushafı'nın sayfa yazı tiplerindeki (QCF v1) kelime kodları.

Bazı Word dosyaları (Badıllı'nın el-Mesnevî el-Arabî baskısı) âyetleri Kur'ân Kompleksi'nin sayfa yazı
tipleriyle yazar: "QCF_P286" yazı tipindeki her karakter, mushafın 286. sayfasındaki bir kelimenin glifidir
(`code_v1`). Bu kaynak, gereken sayfaların kelimelerini (kod, âyet, kelimenin sırası, Osmanî metni) verir;
glifler âyetin adresine ve harekeli metnine böyle çözülür. Sayfa sonundaki âyet numarası glifinin türü "end".

Ham arşiv (`data/raw/qurancom/`): pages/<sayfa>.json.gz (API yanıtı olduğu gibi)
"""

import json
from pathlib import Path

from risale_mcp.sources.archive import fetch_cached, read_raw
from risale_mcp.sources.http import PoliteClient

BASE_URL = "https://api.quran.com/api/v4/verses/by_page"
DELAY = 2.0


def page_path(root: Path, page: int) -> Path:
    return root / "pages" / f"{page:03d}.json.gz"


def page_url(page: int) -> str:
    return f"{BASE_URL}/{page}?words=true&word_fields=code_v1,text_uthmani&fields=verse_key&per_page=50"


def fetch_pages(pages: set[int], root: Path, client: PoliteClient | None = None) -> None:
    client = client or PoliteClient(DELAY)
    for page in sorted(pages):
        data = json.loads(fetch_cached(page_path(root, page), page_url(page), client))
        if data["pagination"]["total_pages"] != 1:
            raise ValueError(f"Mushaf sayfası {page} birden çok yanıt sayfasında; per_page artırılmalı")


def glyphs(root: Path, page: int) -> dict[str, dict]:
    """Sayfanın glif kodu -> {code, verse_key, position, type, text}, sayfa sırasıyla."""
    data = json.loads(read_raw(page_path(root, page)))
    return {w["code_v1"]: {"code": w["code_v1"], "verse_key": v["verse_key"], "position": w["position"],
                           "type": w["char_type_name"], "text": w.get("text_uthmani", "")}
            for v in data["verses"] for w in v["words"]}
