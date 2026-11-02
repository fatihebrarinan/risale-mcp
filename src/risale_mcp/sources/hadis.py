"""Hadis derlemleri: rivayetlerin metni ve âlimlerin dereceleri.

- Sanadset 650K (Mghari, Bouras, El Hibaoui; Data in Brief, 2022; Mendeley Data 5xth87zwb5/5): 954 kitap, senet ve
  metin ayrılmış. CC BY 4.0: kaynak gösterilir. Derece taşımaz.
- Hadith API (fawazahmed0/hadith-api): Kütüb-i Sitte ağırlıklı 10 derlem, beş derlemde âlimlerin dereceleri.
  Unlicense. Türkçe (`tur-*`) dosyalar alınmaz: mütercimleri belli değil.

Ham arşiv: `data/raw/sanadset/` (sanadset.csv, books.csv, manifest.json), `data/raw/hadith_api/` (ara-<derlem>.json).
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
