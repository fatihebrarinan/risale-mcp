"""Keşif Yolculukları Risale-i Nur Eğitim Programı (Ediz Sözüer): Ta'likat'ın Türkçe tam tercümesi.

Program kitaplarını Google Drive'da Word dosyası olarak yayımlar. Ta'likat kitabı Arapça aslın sayfa
resimleri ile Protranslate'in Türkçe tercümesini birlikte verir; biz yalnızca Türkçe metni okuruz.
Kitabın telif bildirimi "asliyetini korumak ve kaynak belirtmek şartıyla" serbest kullanım tanır.

Ham arşiv (`data/raw/kesif/<kitap>/`): <kitap>.docx, manifest.json
"""

import zipfile
from pathlib import Path
from typing import Callable

from risale_mcp.sources.archive import fetch_cached, write_manifest
from risale_mcp.sources.http import PoliteClient

URLS = {"talikat": "https://drive.usercontent.google.com/download?id=19wWPTHxtzVS3ZUB11HkeSxmJ8TfvQNh4"
                   "&export=download&confirm=t"}


def docx_path(root: Path, book: str) -> Path:
    return root / book / f"{book}.docx"


def fetch_book(book: str, root: Path, client: PoliteClient, *,
               refresh: bool = False, log: Callable[[str], None] = print) -> None:
    fetch_cached(docx_path(root, book), URLS[book], client, refresh)
    write_manifest(root / book / "manifest.json", site="kesif", book=book, url=URLS[book])
    log(f"{book}: {docx_path(root, book).stat().st_size} bayt")


def check_book(book: str, root: Path) -> tuple[list[str], bool]:
    """Word dosyası açılabilmeli, metni ve dipnotları bulunmalı."""
    path = docx_path(root, book)
    if not path.exists():
        return [f"kesif/{book}: indirilmemiş"], False
    try:
        names = set(zipfile.ZipFile(path).namelist())
    except zipfile.BadZipFile:
        return [f"kesif/{book}: Word dosyası değil"], False
    ok = {"word/document.xml", "word/footnotes.xml"} <= names
    return [f"kesif/{book}: {path.stat().st_size} bayt, metin ve dipnot {'var' if ok else 'eksik'}"], ok
