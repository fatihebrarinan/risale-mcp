"""Hadis derlemleri: rivayetlerin metni ve âlimlerin dereceleri.

- Sanadset 650K (Mghari, Bouras, El Hibaoui; Data in Brief, 2022; Mendeley Data 5xth87zwb5/5): 954 kitap, senet ve
  metin ayrılmış. CC BY 4.0: kaynak gösterilir. Derece taşımaz.
- Hadith API (fawazahmed0/hadith-api): Kütüb-i Sitte ağırlıklı 10 derlem, beş derlemde âlimlerin dereceleri.
  Unlicense. Türkçe (`tur-*`) dosyalar alınmaz: mütercimleri belli değil.
- OpenITI (KITAB projesi): Kütüb-i Sitte ve Muvatta'nın JK baskıları; kitap ve bâb başlıkları, hadis numaraları.
  CC BY-NC-SA 4.0: kaynak gösterilir, ticari kullanılmaz, türetilen veri aynı lisansla (`docs/hadis-kitaplari-plani.md`).

Ham arşiv: `data/raw/sanadset/` (sanadset.csv, books.csv, manifest.json), `data/raw/hadith_api/` (ara-<derlem>.json),
`data/raw/openiti/` (<kitap>.txt, <kitap>.yml, manifest.json).
"""

import json
from pathlib import Path

from risale_mcp.sources import openiti
from risale_mcp.sources.archive import fetch_cached, write_manifest
from risale_mcp.sources.http import PoliteClient

SANADSET_API = "https://data.mendeley.com/public-api/datasets/5xth87zwb5/files?folder_id=root&version=5"
SANADSET_FILES = ("sanadset.csv", "books.csv")
HADITH_API = "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1"
COLLECTIONS = ("bukhari", "muslim", "abudawud", "tirmidhi", "nasai", "ibnmajah", "malik", "nawawi", "qudsi", "dehlawi")


def fetch_sanadset(root: Path, client: PoliteClient, *, refresh: bool = False) -> None:
    files = {f["filename"]: f["content_details"] for f in json.loads(client.get(SANADSET_API))}
    for name in SANADSET_FILES:
        fetch_cached(root / name, files[name]["download_url"], client, refresh)
    write_manifest(root / "manifest.json", dataset="Sanadset 650K, Mendeley Data 5xth87zwb5 v5", licence="CC BY 4.0",
                   sha256={n: files[n]["sha256_hash"] for n in SANADSET_FILES})


def fetch_hadith_api(root: Path, client: PoliteClient, *, refresh: bool = False) -> None:
    for name in COLLECTIONS:
        fetch_cached(root / f"ara-{name}.json", f"{HADITH_API}/editions/ara-{name}.min.json", client, refresh)
    write_manifest(root / "manifest.json", source="fawazahmed0/hadith-api@1", licence="Unlicense")


# OpenITI depoları sabit commit'ten okunur (`sources/openiti.py`): aynı metin yeniden indirilse de değişmez.
OPENITI_COMMITS = {"0200AH": "599f22fe249871f602efe2e0ddc801d3742960a3", "0275AH": "44e1c36738a2bf5c14dafa232a6ae1891e6171cd",
                   "0300AH": "01a1544130e0236850ef2698923ad01575c5bd7c", "0325AH": "089e665b4958e0f145a46941987fb81cf3dda1b8"}
OPENITI_BOOKS = {
    "bukhari": ("0275AH", "0256Bukhari/0256Bukhari.Sahih/0256Bukhari.Sahih.JK000110-ara1.completed"),
    "muslim": ("0275AH", "0261Muslim/0261Muslim.Sahih/0261Muslim.Sahih.JK000109-ara1"),
    "abudawud": ("0275AH", "0275AbuDawudSijistani/0275AbuDawudSijistani.Sunan/0275AbuDawudSijistani.Sunan.JK000142-ara1"),
    "tirmidhi": ("0300AH", "0279Tirmidhi/0279Tirmidhi.Sunan/0279Tirmidhi.Sunan.JK000140-ara1.completed"),
    "nasai": ("0325AH", "0303Nasai/0303Nasai.SunanSughra/0303Nasai.SunanSughra.JK000130-ara1.mARkdown"),
    "ibnmajah": ("0275AH", "0273IbnMaja/0273IbnMaja.Sunan/0273IbnMaja.Sunan.JK000141-ara1"),
    "malik": ("0200AH", "0179MalikIbnAnas/0179MalikIbnAnas.Muwatta/0179MalikIbnAnas.Muwatta.JK000466-ara1"),
}
OPENITI_TEXTS = {book: openiti.Text(repo, OPENITI_COMMITS[repo], path) for book, (repo, path) in OPENITI_BOOKS.items()}
# MVP hadis kitapları (`docs/mvp-kitaplar.md`, M1): seçilen sürümler (Shamela; Keşfü'l-Hafâ JK). Kütüb-i Sitte
# ayrıştırıcısı (`hadis_kutub.py`) bunları okumaz; Shamela biçimi `hadis_openiti.py`'dedir.
MVP_COMMITS = {"0250AH": "0cc00c0646c81988c75a3815fe6d9a5fa65ce592", "0275AH": OPENITI_COMMITS["0275AH"],
               "0375AH": "ab52219710c6bf15a93d6e39886f0ca602d27952", "0425AH": "3a3c829e55a1e4fb614aa857e0d85f51d6a9f0ee",
               "0750AH": "7c9c84d9f98581470aa2b7f8bee00ae285c5c707", "0825AH": "bae1fba53712c020fe43e3e60b37dfe61f2b64a8",
               "0975AH": "c47ff1c47a9108eab999d7fa68ef30be16bc0f85", "1050AH": "ab6ad0f2d84f53b4f87e6ca1fc53cafffaba0abf",
               "1175AH": "2c367f78b779757652ee59df503fdc9312ec2f06",
               "0475AH": "cc9beb0d9645e8cdce892556423b9926a127054f", "0550AH": "6c414b1e23f2646d30e4f7f08f4b07be9832367c"}
MVP_BOOKS = {
    "musned": ("0250AH", "0241IbnHanbal/0241IbnHanbal.Musnad/0241IbnHanbal.Musnad.Shamela0013157-ara1"),
    "darimi": ("0275AH", "0255CabdAllahDarimi/0255CabdAllahDarimi.Sunan/0255CabdAllahDarimi.Sunan.Shamela0021795-ara3"),
    "mucem-sagir": ("0375AH", "0360Tabarani/0360Tabarani.MucjamSaghir/0360Tabarani.MucjamSaghir.Shamela0013068-ara1"),
    "mustedrek": ("0425AH", "0405HakimNaysaburi/0405HakimNaysaburi.Mustadrak/0405HakimNaysaburi.Mustadrak.Shamela0002266-ara1"),
    "ihsan": ("0750AH", "0739CalaDinIbnBalban/0739CalaDinIbnBalban.Ihsan/0739CalaDinIbnBalban.Ihsan.Sham19Y0001734-ara1"),
    "mecma": ("0825AH", "0807NurDinHaythami/0807NurDinHaythami.MajmacZawaid/0807NurDinHaythami.MajmacZawaid.Shamela0000061-ara1"),
    "kenz": ("0975AH", "0975MuttaqiHindi/0975MuttaqiHindi.KanzCummal/0975MuttaqiHindi.KanzCummal.Shamela0002677-ara1"),
    "feyz": ("1050AH", "1031CabdRaufMunawi/1031CabdRaufMunawi.FaydQadir/1031CabdRaufMunawi.FaydQadir.Shamela0021660-ara1"),
    "sifa": ("0550AH", "0544QadiCiyad/0544QadiCiyad.Shifa/0544QadiCiyad.Shifa.Shamela0023645-ara1.completed"),
    "delail": ("0475AH", "0458Bayhaqi/0458Bayhaqi.DalailNubuwwa/0458Bayhaqi.DalailNubuwwa.Shamela0013115-ara1"),
    "kesfulhafa": ("1175AH", "1162IbnMuammadAbuFidaCajluni/1162IbnMuammadAbuFidaCajluni.KashfKhafa/1162IbnMuammadAbuFidaCajluni.KashfKhafa.JK000583-ara1"),
}
MVP_TEXTS = {book: openiti.Text(repo, MVP_COMMITS[repo], path) for book, (repo, path) in MVP_BOOKS.items()}


def fetch_openiti(root: Path, client: PoliteClient, *, refresh: bool = False) -> None:
    openiti.fetch(OPENITI_TEXTS, root, client, refresh=refresh)
    openiti.fetch(MVP_TEXTS, root, client, refresh=refresh)
