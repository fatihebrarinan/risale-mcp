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


# OpenITI depoları sabit commit'ten okunur: aynı metin yeniden indirilse de değişmez.
OPENITI_RAW = "https://raw.githubusercontent.com/OpenITI"
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


def openiti_url(book: str, suffix: str = "") -> str:
    repo, path = OPENITI_BOOKS[book]
    return f"{OPENITI_RAW}/{repo}/{OPENITI_COMMITS[repo]}/data/{path}{suffix}"


def fetch_openiti(root: Path, client: PoliteClient, *, refresh: bool = False) -> None:
    for book, (repo, path) in OPENITI_BOOKS.items():
        fetch_cached(root / f"{book}.txt", openiti_url(book), client, refresh)
        version = path.rsplit("/", 1)[1].removesuffix(".completed").removesuffix(".mARkdown")
        fetch_cached(root / f"{book}.yml", openiti_url(book, "").rsplit("/", 1)[0] + f"/{version}.yml", client, refresh)
    write_manifest(root / "manifest.json", source="OpenITI (KITAB project), JK editions", licence="CC BY-NC-SA 4.0",
                   commits=OPENITI_COMMITS, files={b: f"{r}/data/{p}" for b, (r, p) in OPENITI_BOOKS.items()})
