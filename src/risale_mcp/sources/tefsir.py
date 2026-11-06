"""Müfessirlerin eserleri (`docs/tefsir-altyapi-plani.md`): OpenITI sürümleri, sabit commit'ten.

    uv run python -m risale_mcp.fetch tefsir        # data/raw/openiti/<anahtar>.txt ve .yml

Pilot Beyzâvî'nin Envârü't-Tenzîl'idir (T0). OpenITI'de beş sürümü var; hepsi indirilir, karşılaştırma ve nüsha
seçimi `docs/tefsir-altyapi-plani.md`'de (T0). Lisans CC BY-NC-SA 4.0 (`docs/izinler.md`, OpenITI satırı).
"""

from pathlib import Path

from risale_mcp.sources import openiti
from risale_mcp.sources.http import PoliteClient

COMMIT_0700 = "3d8ff4e7b035aaa4ca5dda52c7322645f3401dcf"          # OpenITI/0700AH, 2025-11-28
_BEYZAVI = "0685NasirDinBaydawi/0685NasirDinBaydawi.AnwarTanzil/0685NasirDinBaydawi.AnwarTanzil"
TEXTS = {
    "beyzavi-jk": openiti.Text("0700AH", COMMIT_0700, f"{_BEYZAVI}.JK000128-ara1"),
    "beyzavi-shamay": openiti.Text("0700AH", COMMIT_0700, f"{_BEYZAVI}.ShamAY0034065-ara1"),
    "beyzavi-shamela": openiti.Text("0700AH", COMMIT_0700, f"{_BEYZAVI}.Shamela0023588-ara1"),
    "beyzavi-shia": openiti.Text("0700AH", COMMIT_0700, f"{_BEYZAVI}.Shia002637Vols-ara1"),
    "beyzavi-tafsir": openiti.Text("0700AH", COMMIT_0700, f"{_BEYZAVI}.Tafsir01006-ara1"),
}


# MVP (`docs/mvp-kitaplar.md`, M1): her eserin seçilen Shamela sürümü (metin, sayfa, muhakkik) ve altafsir.com
# sürümü (`Tafsir…`; her âyet biriminin başında `[sûre.âyet]`, sayfasız ve "eksik metin" işaretli): âyet sınırları
# ondan alınır, Shamela metnine ilk kelimelerinden çapalanır (`books/tefsir_openiti.py`).
COMMITS = {
    "0325AH": "089e665b4958e0f145a46941987fb81cf3dda1b8", "0350AH": "3f52b87dc367365000b32f815a3d0077451c46f4",
    "0550AH": "6c414b1e23f2646d30e4f7f08f4b07be9832367c", "0625AH": "f1e38210b32fd0d043949ff6471e869d658c3b16",
    "0675AH": "4b1d2886508b435eb0377ccab96e1da96cc8ee0a", "0700AH": COMMIT_0700,
    "0725AH": "056df249d6619b428a78f1d69a8ab2851b97b0a6", "0775AH": "61b0c7891699554aeff8dffdb8b1a2a59d2d22ab",
    "0925AH": "4f0f4562d1e13083c593e3a0ca6a19a3eb33805e", "1000AH": "55a280982e225ff8652737b70d99a337cb939546",
    "1150AH": "c3f5524572733bb60fa64f891823fdeffc23d92f", "1275AH": "d6d3091d7477cc4d2f4cdcd71e5873e90f5d28e8",
}
# eser -> (depo, yazar/eser klasörü, Shamela dosyası, altafsir dosyası)
MVP = {
    "taberi": ("0325AH", "0310Tabari/0310Tabari.JamicBayan",
               "Shamela0007798-ara1.inProgress", "Tafsir01001-ara1"),
    "maturidi": ("0350AH", "0333AbuMansurMaturidi/0333AbuMansurMaturidi.Tafsir",
                 "Shamela0095590-ara1", "Tafsir02094-ara1"),
    "kessaf": ("0550AH", "0538JarAllahZamakhshari/0538JarAllahZamakhshari.Kashshaf",
               "Shamela0023627-ara1", "Tafsir01002-ara1"),
    "razi": ("0625AH", "0606FakhrDinRazi/0606FakhrDinRazi.MafatihGhayb", "Shamela0023635-ara1", "Tafsir01004-ara1"),
    "kurtubi": ("0675AH", "0671AbuCabdAllahQurtubi/0671AbuCabdAllahQurtubi.JamicLiAhkamQuran",
                "Shamela0020855-ara1", "Tafsir01005-ara1"),
    "nesefi": ("0725AH", "0710IbnAhmadHafizDinNasafi/0710IbnAhmadHafizDinNasafi.Tafsir",
               "Shamela0001394-ara1", "Tafsir02017-ara1"),
    "ibnkesir": ("0775AH", "0774IbnKathir/0774IbnKathir.TafsirQuran",
                 "Shamela0008473-ara1.mARkdown", "Tafsir01007-ara7"),
    "celaleyn": ("0925AH", "0911Suyuti/0911Suyuti.TafsirJalalayn", "Shamela0012876-ara1", "Tafsir01008-ara1"),
    "durr": ("0925AH", "0911Suyuti/0911Suyuti.DurrManthur", "Shamela0012884-ara1.completed", "Tafsir02026-ara1"),
    "ebussuud": ("1000AH", "0982IbnMuhammadAbuSucud/0982IbnMuhammadAbuSucud.IrshadCaqlSalim",
                 "Shamela0001429-ara1", "Tafsir02028-ara1"),
    "bursevi": ("1150AH", "1127IsmacilHaqqiBurusawi/1127IsmacilHaqqiBurusawi.RuhBayan",
                "Shamela0023612-ara1", "Tafsir03036-ara1"),
    "alusi": ("1275AH", "1270ShihabDinAlusi/1270ShihabDinAlusi.RuhMacani", "Shamela0022835-ara1", "Tafsir07052-ara1"),
}
for _key, (_repo, _dir, _shamela, _altafsir) in MVP.items():
    _base = f"{_dir}/{_dir.rsplit('/', 1)[1]}"
    TEXTS[f"{_key}-shamela"] = openiti.Text(_repo, COMMITS[_repo], f"{_base}.{_shamela}")
    TEXTS[f"{_key}-altafsir"] = openiti.Text(_repo, COMMITS[_repo], f"{_base}.{_altafsir}")


def fetch(root: Path, client: PoliteClient, *, refresh: bool = False) -> None:
    openiti.fetch(TEXTS, root, client, refresh=refresh)
