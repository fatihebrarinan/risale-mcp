"""Kullanıcının sağladığı dosyalar: internette serbest metni bulunmayan eserlerin PDF'leri.

Dosya indirilmez; kullanıcı `data/` altına koyar, `fetch get` onu ham arşive kopyalar ve bir manifest yazar.
Rumuzat-ı Semaniye: Üçüncü, Dördüncü ve Sekizinci Kısımları içeren mecmua (LibreOffice'ten PDF, 77 sayfa).

Ham arşiv (`data/raw/kullanici/<kitap>/`): <kitap>.pdf, manifest.json
"""

import hashlib
import shutil
from collections.abc import Callable
from pathlib import Path

from risale_mcp.paths import DATA_DIR
from risale_mcp.sources.archive import write_manifest
from risale_mcp.sources.http import PoliteClient

# kitap -> kullanıcının dosyası (data/ altında)
FILES = {"rumuzat-i-semaniye": "440516300-Rumuzat-i-Semaniye.pdf"}


def pdf_path(root: Path, book: str) -> Path:
    return root / book / f"{book}.pdf"


def fetch_book(book: str, root: Path, client: PoliteClient | None = None, *,
               refresh: bool = False, log: Callable[[str], None] = print) -> None:
    target = pdf_path(root, book)
    if refresh or not target.exists():
        source = DATA_DIR / FILES[book]
        if not source.exists():
            raise FileNotFoundError(f"{source} yok: dosyayı data/ altına koyun")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    sha1 = hashlib.sha1(target.read_bytes()).hexdigest()
    write_manifest(root / book / "manifest.json", site="kullanici", book=book, file=FILES[book], sha1=sha1)
    log(f"{book}: {target.stat().st_size} bayt")


def check_book(book: str, root: Path) -> tuple[list[str], bool]:
    path = pdf_path(root, book)
    if not path.exists():
        return [f"kullanici/{book}: kopyalanmamış"], False
    ok = path.read_bytes()[:5] == b"%PDF-"
    return [f"kullanici/{book}: {path.stat().st_size} bayt, {'PDF' if ok else 'PDF değil'}"], ok
