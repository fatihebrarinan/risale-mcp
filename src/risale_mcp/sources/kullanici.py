"""Kullanıcının sağladığı dosyalar: internette serbest metni bulunmayan eserlerin PDF'leri.

Dosya indirilmez; kullanıcı `data/raw/kullanici/<kitap>/<kitap>.pdf` olarak koyar, `fetch get` manifest yazar.
Rumuzat-ı Semaniye: Üçüncü, Dördüncü ve Sekizinci Kısımları içeren mecmua (LibreOffice'ten PDF, 77 sayfa).
Kızıl İcaz'ın Türkçesi (`kizil-icaz/kizil-icaz.pdf`, 399 sayfa resim) aynı klasörde bekler; henüz ayrıştırılmaz (Aşama 17).

Ham arşiv (`data/raw/kullanici/<kitap>/`): <kitap>.pdf, manifest.json
"""

import hashlib
from collections.abc import Callable
from pathlib import Path

from risale_mcp.sources.archive import write_manifest
from risale_mcp.sources.http import PoliteClient

# kitap -> dosyanın kullanıcıdan geldiği adı (yalnızca manifestte kayıt için)
FILES = {"rumuzat-i-semaniye": "440516300-Rumuzat-i-Semaniye.pdf"}


def pdf_path(root: Path, book: str) -> Path:
    return root / book / f"{book}.pdf"


def fetch_book(book: str, root: Path, client: PoliteClient | None = None, *,
               refresh: bool = False, log: Callable[[str], None] = print) -> None:
    target = pdf_path(root, book)
    if not target.exists():
        raise FileNotFoundError(f"{target} yok: dosyayı bu adla oraya koyun")
    sha1 = hashlib.sha1(target.read_bytes()).hexdigest()
    write_manifest(root / book / "manifest.json", site="kullanici", book=book, file=FILES[book], sha1=sha1)
    log(f"{book}: {target.stat().st_size} bayt")


def check_book(book: str, root: Path) -> tuple[list[str], bool]:
    path = pdf_path(root, book)
    if not path.exists():
        return [f"kullanici/{book}: dosya yok"], False
    ok = path.read_bytes()[:5] == b"%PDF-"
    return [f"kullanici/{book}: {path.stat().st_size} bayt, {'PDF' if ok else 'PDF değil'}"], ok
