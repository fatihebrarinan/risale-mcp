"""Risale-i Nur ile ilgili, külliyatta olmayan kaynaklar: Sorularla Risale, mufassal tarihçeler, hatıra kitapları.

Bu eserler müellifin metni değildir. Burada kayıt açmak için `ilgili()` kullanılır:
- `authority` zorunludur: nakil, serh, modern ya da derleme; `tests/test_collections.py` müellif kaydını reddeder.
- İzin gelene kadar `private` kalır; izin `docs/izinler.md`'ye yazılınca `private=False` verilir.
- Kelime ve anlamsal arama bu koleksiyona varsayılan olarak girmez: günümüz Türkçesiyle yazılmış metinler
  anlamsal aramada eski dilli asıl metnin önüne geçer. Araçta `include_related` ile istenir.

Grup (`Group`) ilk eser eklenirken açılır.
"""

from risale_mcp.catalog.model import Authority, Collection, Group, SourceRef, Work


def ilgili(slug: str, title: str, group: Group, source: SourceRef | None, authority: Authority,
           *, private: bool = True, **fields) -> Work:
    return Work(slug, title, group, source, private=private, authority=authority,
                collection=Collection.ILGILI, **fields)


ILGILI_WORKS: tuple[Work, ...] = ()
