"""Eser kataloğu: her eserin kaynağı, koleksiyonu ve statüsü tek yerde.

Kayıtlar koleksiyon başına ayrı dosyadadır (`kulliyat.py`, `ilgili.py`); yapı taşları `model.py`'de.
Eser kimliği bütün katalogda tektir: atıflar kimlikte eseri öneksiz taşır (`sozler/10/…`).
"""

from risale_mcp.catalog.ilgili import ILGILI_WORKS
from risale_mcp.catalog.kulliyat import KULLIYAT_WORKS
from risale_mcp.catalog.model import Authority, Collection, Group, Site, SECONDARY_SITES, SourceRef, Status, Work

WORKS: tuple[Work, ...] = KULLIYAT_WORKS + ILGILI_WORKS

_BY_SLUG = {work.slug: work for work in WORKS}
if len(_BY_SLUG) != len(WORKS):
    raise ValueError("Katalogda aynı kimlikle iki eser var.")


def get_work(slug: str) -> Work:
    try:
        return _BY_SLUG[slug]
    except KeyError:
        raise KeyError(f"Katalogda böyle bir eser yok: {slug!r}") from None


def works_from(site: Site, book: str) -> list[Work]:
    """Aynı kaynak kitabından beslenen eserler (ör. erisale/sozler -> Sözler ve Lemeat)."""
    return [w for w in WORKS if w.source and w.source.site == site and w.source.book == book]
