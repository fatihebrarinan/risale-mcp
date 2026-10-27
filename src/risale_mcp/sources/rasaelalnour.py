"""rasaelalnour.com: İhsan Kasım es-Sâlihî'nin Arapça Külliyatı (Word dosyaları, RAR arşivinde).

Aslı Arapça olan eserlerin (İşaratü'l-İ'caz, Kızıl İcaz, Ta'likat) Arapça metni buradan gelir.
Arşivler RAR5'tir; sistemdeki eski 7z onları sessizce boş açar, bu yüzden `libarchive` kullanılır.
Word dosyaları eski biçimdedir (.doc); LibreOffice ile .docx'e çevrilip okunur.

Sitede yalnızca bir telif satırı vardır, ayrı bir kullanım şartı yoktur. Kullanım kişiseldir.

Ham arşiv (`data/raw/rasaelalnour/<kitap>/`): archive.rar, manifest.json
Açılmış ve çevrilmiş dosyalar (`data/interim/rasaelalnour/<kitap>/`): <ad>.doc, docx/<ad>.docx
"""

import shutil
import subprocess
from pathlib import Path
from typing import Callable

import libarchive

from risale_mcp.paths import INTERIM_DIR
from risale_mcp.sources.archive import fetch_cached, write_manifest
from risale_mcp.sources.http import PoliteClient

BASE_URL = "https://www.rasaelalnour.com/dosyalar"
EXTRACT_DIR = INTERIM_DIR / "rasaelalnour"


def archive_path(root: Path, book: str) -> Path:
    return root / book / "archive.rar"


def members(path: Path) -> list[tuple[str, int]]:
    """Arşivdeki dosyalar (klasörsüz ad, boyut)."""
    with libarchive.file_reader(str(path)) as archive:
        return [(Path(e.pathname).name, e.size) for e in archive if not e.isdir]


def fetch_book(book: str, root: Path, client: PoliteClient, *,
               refresh: bool = False, log: Callable[[str], None] = print) -> None:
    url = f"{BASE_URL}/{book}.rar"
    fetch_cached(archive_path(root, book), url, client, refresh)
    write_manifest(root / book / "manifest.json", site="rasaelalnour", book=book, url=url)
    log(f"{book}: {len(members(archive_path(root, book)))} dosya")


def check_book(book: str, root: Path) -> tuple[list[str], bool]:
    """Arşiv açılabilmeli ve içindeki her dosya boş olmamalı."""
    path = archive_path(root, book)
    if not path.exists():
        return [f"rasaelalnour/{book}: indirilmemiş"], False
    files = members(path)
    empty = [name for name, size in files if not size]
    lines = [f"rasaelalnour/{book}: {len(files)} dosya, boş {empty}"]
    lines += [f"  {size:>9} {name}" for name, size in files]
    return lines, bool(files) and not empty


def docx(root: Path, book: str, name: str) -> Path:
    """Arşivdeki `name` (.doc ya da .docx) dosyasının .docx hâli; gerekirse açar ve LibreOffice ile çevirir."""
    out_dir = EXTRACT_DIR / book
    target = out_dir / "docx" / (Path(name).stem + ".docx")
    if target.exists():
        return target
    out_dir.mkdir(parents=True, exist_ok=True)
    with libarchive.file_reader(str(archive_path(root, book))) as archive:
        for entry in archive:
            if not entry.isdir and Path(entry.pathname).name == name:
                with open(out_dir / name, "wb") as f:
                    for block in entry.get_blocks():
                        f.write(block)
                break
        else:
            raise FileNotFoundError(f"{book}.rar içinde {name} yok")
    target.parent.mkdir(exist_ok=True)
    if name.endswith(".docx"):
        shutil.copy(out_dir / name, target)
        return target
    soffice = shutil.which("soffice")
    if soffice is None:
        raise RuntimeError(".doc dosyasını çevirmek için LibreOffice (soffice) gerekli.")
    subprocess.run([soffice, "--headless", "--convert-to", "docx", "--outdir", str(target.parent), str(out_dir / name)],
                   check=True, capture_output=True, timeout=600)
    if not target.exists():
        raise RuntimeError(f"{name} .docx'e çevrilemedi")
    return target

