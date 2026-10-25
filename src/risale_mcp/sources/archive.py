"""Ham yanıtları diske yazan ortak yardımcılar.

Dosyalar önce geçici adla yazılıp sonra yerine taşınır; indirme yarıda kesilirse
yarım dosya kalmaz ve bir sonraki çalıştırma kaldığı yerden devam eder.
"""

import gzip
import json
from datetime import datetime, timezone
from pathlib import Path

from risale_mcp.sources.http import PoliteClient


def write_atomic(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(data)
    tmp.replace(path)


def read_raw(path: Path) -> bytes:
    data = path.read_bytes()
    return gzip.decompress(data) if path.suffix == ".gz" else data


def fetch_cached(path: Path, url: str, client: PoliteClient, refresh: bool = False) -> bytes:
    """Diskte varsa onu, yoksa indirip kaydettiğini döndürür. `.gz` uzantılı dosyalar sıkıştırılır."""
    if path.exists() and not refresh:
        return read_raw(path)
    body = client.get(url)
    write_atomic(path, gzip.compress(body) if path.suffix == ".gz" else body)
    return body


def write_manifest(path: Path, **fields) -> None:
    data = {**fields, "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    write_atomic(path, json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8"))
