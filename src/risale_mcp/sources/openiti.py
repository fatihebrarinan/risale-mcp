"""OpenITI indiricisi (H6): bir metin dosyası ve üst bilgisi, sabit commit'ten.

OpenITI (KITAB projesi) eserleri dönem depolarında durur (`0275AH`, `0700AH`…); dosya yolu
`data/<yazar>/<eser>/<sürüm>` biçimindedir. Depo sabit bir commit'ten okunur: aynı metin yeniden indirilse de
değişmez, atıf yıllar sonra yeniden üretilebilir. Lisans CC BY-NC-SA 4.0 (kaynak, ticari olmayan, aynı lisans).

Ham veri `data/raw/openiti/<anahtar>.txt` ve `<anahtar>.yml` (sürümün açıklaması: hangi baskıyla karşılaştırıldığı,
temizlenme notları). Klasör alanlar arasında ortaktır (hadis kitapları, ileride müfessirlerin eserleri); `manifest.json`
her indirmede birleştirilir, başka alanın kaydını silmez.
"""

import json
from dataclasses import dataclass
from pathlib import Path

from risale_mcp.catalog.excluded import openiti_reason
from risale_mcp.sources.archive import fetch_cached, read_raw, write_manifest
from risale_mcp.sources.http import PoliteClient

RAW = "https://raw.githubusercontent.com/OpenITI"
SOURCE = "OpenITI (KITAB project)"
LICENCE = "CC BY-NC-SA 4.0"


@dataclass(frozen=True)
class Text:
    """Bir OpenITI sürüm dosyası: depo, sabit commit ve depodaki yol (`data/` sonrası, uzantısıyla)."""
    repo: str
    commit: str
    path: str

    def __post_init__(self):
        if reason := openiti_reason(self.path):
            raise ValueError(f"kaynak alınmaz ({reason}): {self.path}")

    @property
    def version(self) -> str:
        """Sürüm adı (`0256Bukhari.Sahih.JK000110-ara1`): `.yml`'nin adı, `.completed` ya da `.mARkdown` eki olmadan."""
        return self.path.rsplit("/", 1)[1].removesuffix(".completed").removesuffix(".mARkdown")

    @property
    def file(self) -> str:
        return f"{self.repo}/data/{self.path}"

    def url(self, path: str | None = None) -> str:
        return f"{RAW}/{self.repo}/{self.commit}/data/{path or self.path}"

    def yml_url(self) -> str:
        return self.url(self.path.rsplit("/", 1)[0] + f"/{self.version}.yml")


def fetch(texts: dict[str, Text], root: Path, client: PoliteClient, *, refresh: bool = False, **note) -> None:
    """Metinleri ve üst bilgilerini indirir (diskte varsa indirmez); manifestoya kendi kayıtlarını ekler."""
    for key, text in texts.items():
        fetch_cached(root / f"{key}.txt", text.url(), client, refresh)
        fetch_cached(root / f"{key}.yml", text.yml_url(), client, refresh)
    path = root / "manifest.json"
    old = json.loads(read_raw(path)) if path.exists() else {}
    commits = {**old.get("commits", {}), **{t.repo: t.commit for t in texts.values()}}
    files = {**old.get("files", {}), **{key: t.file for key, t in texts.items()}}
    write_manifest(path, source=SOURCE, licence=LICENCE, commits=commits, files=files,
                   **{k: v for k, v in old.items() if k not in ("source", "licence", "commits", "files", "fetched_at")},
                   **note)
