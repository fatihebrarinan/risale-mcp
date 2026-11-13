"""Eser kataloğu: her eserin kaynağı, koleksiyonu ve statüsü tek yerde.

Kayıtlar koleksiyon başına ayrı dosyadadır (`kulliyat.py`, `ilgili.py`, `tefsir.py`, `klasik.py`); yapı taşları `model.py`'de.
Eser kimliği bütün katalogda tektir: atıflar kimlikte eseri öneksiz taşır (`sozler/10/…`).
"""

from risale_mcp.catalog.ilgili import ILGILI_WORKS
from risale_mcp.catalog.klasik import KLASIK_WORKS
from risale_mcp.catalog.kulliyat import KULLIYAT_WORKS
from risale_mcp.catalog.tefsir import TEFSIR_WORKS
from risale_mcp.catalog.model import Authority, Collection, Group, Site, SECONDARY_SITES, SourceRef, Status, Work

WORKS: tuple[Work, ...] = KULLIYAT_WORKS + ILGILI_WORKS + TEFSIR_WORKS + KLASIK_WORKS

_BY_SLUG = {work.slug: work for work in WORKS}
if len(_BY_SLUG) != len(WORKS):
    raise ValueError("Katalogda aynı kimlikle iki eser var.")


def _excluded_problems(works) -> list[str]:
    """Kaynak alınmayacak yazarın eseri katalogda olamaz (`catalog/excluded.py`)."""
    from risale_mcp.catalog.excluded import AUTHORS
    from risale_mcp.normalize import search_words
    out = []
    for work in works:
        text = " ".join(search_words(" ".join(filter(None, (work.author, work.title, work.slug)))))
        out += [f"{work.slug}: {reason}" for name, reason in AUTHORS.items() if name in text]
    return out


if _bad := _excluded_problems(WORKS):
    raise ValueError("Katalogda kaynak alınmayacak eser: " + "; ".join(_bad))


def get_work(slug: str) -> Work:
    try:
        return _BY_SLUG[slug]
    except KeyError:
        raise KeyError(f"Katalogda böyle bir eser yok: {slug!r}") from None


def works_from(site: Site, book: str) -> list[Work]:
    """Aynı kaynak kitabından beslenen eserler (ör. erisale/sozler -> Sözler ve Lemeat)."""
    return [w for w in WORKS if w.source and w.source.site == site and w.source.book == book]
