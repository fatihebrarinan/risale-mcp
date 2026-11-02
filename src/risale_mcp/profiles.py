"""Profiller: bir MCP sunucusunun hangi koleksiyonlardan kurulduğu.

Koleksiyon metnin nerede durduğunu, profil nereye çıktığını söyler. Her profilin tek veritabanı vardır: alanlar
arası bağlar (âyet ilişkileri, ileride hadis eşlemeleri) bir arada sorgulanır. Kendi sunucusu olacak yeni bir derlem
buraya yeni profil olarak eklenir (ör. `erisale`: yalnız e-Risale metni); `data/dist/<profil>/` altına kurulur.
Kurulum sırası bağımlılığı izler: Kur'ân, sonra Risale'nin âyet eşlemeleri (`build_db.build`).
"""

from dataclasses import dataclass
from pathlib import Path

from risale_mcp.catalog import Collection, Work
from risale_mcp.paths import DB_PATH, LIBRARY_DIR, PUBLIC_DB_PATH, PUBLIC_VECTORS_DIR, VECTORS_DIR


@dataclass(frozen=True)
class Profile:
    name: str
    collections: tuple[Collection, ...]
    db: Path
    vectors: Path
    private: bool = False       # `Work.private` eserler dahil mi

    @property
    def book_dirs(self) -> tuple[Path, ...]:
        return tuple(LIBRARY_DIR / c for c in self.collections)

    def includes(self, work: Work) -> bool:
        return work.collection in self.collections and (self.private or not work.private)


KISISEL = Profile("kisisel", (Collection.KULLIYAT, Collection.ILGILI), DB_PATH, VECTORS_DIR, private=True)
GENEL = Profile("genel", (Collection.KULLIYAT, Collection.ILGILI), PUBLIC_DB_PATH, PUBLIC_VECTORS_DIR)

PROFILES = {p.name: p for p in (KISISEL, GENEL)}
