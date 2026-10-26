"""Ortam değişkenleri: proje klasöründeki `.env` dosyası (API anahtarları).

Biçim: her satırda `AD=değer`; boş satırlar ve `#` ile başlayanlar atlanır. Ortamda zaten tanımlı
olan değişken değiştirilmez (sunucuda systemd'nin `EnvironmentFile`'ı ya da kabuktaki `export`
önceliklidir). Dosya git'e eklenmez.
"""

import os
from pathlib import Path

from risale_mcp.paths import ROOT

ENV_FILE = ROOT / ".env"


def load_env(path: Path = ENV_FILE) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, _, value = line.partition("=")
        os.environ.setdefault(name.strip(), value.strip())
