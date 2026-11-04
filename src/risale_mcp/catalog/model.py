"""Katalogun yapı taşları: eser kaydı, grup, kaynak, koleksiyon ve metnin kime ait olduğu.

Bir eserin yeri ve statüsü buradaki alanlardan gelir; klasörler bunlardan türer, tersi değil.
"""

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from risale_mcp.paths import LIBRARY_DIR


class Collection(StrEnum):
    """Eser JSON'larının durduğu koleksiyon; değeri `data/library/` altındaki yoldur.

    Koleksiyon, eserin hangi alana ait olduğunu söyler, hangi sunucuya çıktığını değil (o `profiles.py`'dedir).
    Kur'ân ayrı bir katmandır (`data/library/kuran/`): atıf birimi âyettir, eser kaydı tutulmaz.
    """
    KULLIYAT = "risale/kulliyat"    # Bediüzzaman'ın eserleri ve mecmuaları
    ILGILI = "risale/ilgili"        # Külliyat dışı: Sorularla Risale, mufassal tarihçeler, hatıralar
    TEFSIR = "tefsir"               # Müfessirlerin eserleri (`docs/tefsir-altyapi-plani.md`); ad alanı `tefsir:`


AUTHOR = "Bediüzzaman Said Nursî"      # külliyatın müellifi: `Work.author`'un varsayılanı


class Authority(StrEnum):
    """Metnin kime ait olduğu: araçlar model bunu müellife mal etmesin diye söyler.

    Eserin kendi yazarına (`Work.author`) göre okunur: `muellif` "eserin yazarının metni" demektir; külliyatta yazar
    Bediüzzaman'dır, ileride bir müfessirin eserinde o müfessir. Eser düzeyindedir. Tercüme asıl sahibinin eseri sayılır, `Work.translation` ile işaretlenir; eserin içindeki
    katmanlar (şerh, tercüme bölümleri) ayrıca işaretlidir (`commentator`, alt başlıklar; bkz. CLAUDE.md, Aslı Arapça eserler).
    """
    MUELLIF = "muellif"     # müellifin eseri ya da onun metinlerinden oluşan mecmua
    DERLEME = "derleme"     # sonradan derleme: derleyicinin sözleri ve tertibi var
    BASKASI = "baskasi"     # başkasının metni (kaside, dua): müellifin eseri değil
    NAKIL = "nakil"         # hatıra, rivayet: "Üstad dedi ki" müellifin metni değil, anlatanın aktarmasıdır
    SERH = "serh"           # başkasının şerhi
    MODERN = "modern"       # günümüz yazarının açıklaması (soru-cevap, makale)


class Group(StrEnum):
    ESKI_SAID = "eski-said"
    ANA_CILT = "ana-cilt"
    MECMUA = "mecmua"
    HIZB = "hizb"
    OSMANLICA = "osmanlica"
    TEFSIR = "tefsir"                # müfessirlerin eserleri


class Status(StrEnum):
    READY = "ready"          # kaynak belli, indirilebilir
    VERIFY = "verify"        # kaynak belli ama içeriğin tam/doğru olduğu doğrulanmalı
    DEFERRED = "deferred"    # kullanıcı kararıyla ertelendi
    MISSING = "missing"      # henüz kaynak bulunamadı


class Site(StrEnum):
    ERISALE = "erisale"              # erisale.com: standart baskı, birincil kaynak
    RISALE_ONLINE = "risale_online"  # risale.online: Hayrat baskısı
    RISALEOKU = "risaleoku"          # risaleoku.com'un eski sitesi (kapandı; ham veri karşılaştırma için durur)
    RISALEOKU_APP = "risaleoku_app"  # risaleoku.com uygulaması: katalog ve kitap dosyaları
    YENIASYA = "yeniasya"            # yeniasya.com.tr/risaleinur: bozuk kodlu PDF metni, Arapçasız (artık kullanılmıyor)
    KASTAMONUR = "kastamonur"        # kastamonur.com: Âsâr-ı Bedîiyye'den Nutuklar ve Makaleler
    RASAELALNOUR = "rasaelalnour"    # rasaelalnour.com: İhsan Kasım'ın Arapça Külliyatı (Word, RAR arşivi)
    KESIF = "kesif"                  # Keşif Yolculukları Risale-i Nur Eğitim Programı: Ta'likat'ın Türkçesi (Word)
    KULLANICI = "kullanici"          # kullanıcının sağladığı dosya (PDF): internette serbest metni olmayan eserler
    NURPEDIA = "nurpedia"            # nurpedia.org (MediaWiki): Rumuzat-ı Semaniye'nin metni
    OPENITI = "openiti"              # OpenITI (KITAB projesi): klasik eserlerin sabit commit'teki sürümleri (`sources/openiti.py`)


# Bu kaynaklardaki eserler ana metin sayılmaz: ana ciltlerde de geçen parçaları oraya eşlenir.
SECONDARY_SITES = frozenset({Site.YENIASYA, Site.KASTAMONUR, Site.KULLANICI})


@dataclass(frozen=True)
class SourceRef:
    site: Site
    book: str                          # sitenin kitap kimliği
    sections: tuple[str, ...] = ()     # boşsa kitabın tamamı
    exclude: tuple[str, ...] = ()      # başka esere ait olduğu için çıkarılan bölümler

    def includes(self, section: str) -> bool:
        def matches(prefixes: tuple[str, ...]) -> bool:
            return any(section == p or section.startswith(p + "-") for p in prefixes)
        return (not self.sections or matches(self.sections)) and not matches(self.exclude)


@dataclass(frozen=True)
class Work:
    slug: str
    title: str
    group: Group
    source: SourceRef | None
    status: Status = Status.READY
    note: str = ""
    language: str = "tr"            # metnin dili: "tr", "ar" ya da "os" (Arapça harfli eserler sağdan sola)
    private: bool = False           # yalnızca kullanıcının yerel veritabanında; genel sunucuya çıkmaz
    secondary: bool = False         # ana metin sayılmaz: ana ciltlerde de geçen paragrafları oraya eşlenir
    collection: Collection = Collection.KULLIYAT
    authority: Authority = Authority.MUELLIF
    translation: bool = False       # eser tercümedir: `authority` asıl metnin sahibini söyler, mütercim `translator`
    # Kişiler (H2): yalnız kaynağın ya da kaydın söylediği; bilinmeyen boş kalır, tahmin edilmez.
    author: str | None = AUTHOR     # eserin yazarı; başkasının metninde (Tesbihat) bilinmiyorsa None
    translator: str | None = None   # tercümede mütercim
    editor: str | None = None       # muhakkik ya da baskıyı hazırlayan (İhsan Kasım es-Sâlihî tahkiki)
    compiler: str | None = None     # derleyen (mecmuayı ya da sonradan derlemeyi tertip eden, müellif değilse)
    # İzin (H3): `catalog/permissions.py`'deki kayıt; verilmezse kaynağın sitesinden.
    permission: str | None = None
    public_without_record: str = "" # izin kaydı olmadan genel profilde: kullanıcının kararını bekleyen açık mesele

    @property
    def book_path(self) -> Path:
        """Eserin JSON'u."""
        return LIBRARY_DIR / self.collection / f"{self.slug}.json"

    @property
    def permission_key(self) -> str | None:
        from risale_mcp.catalog.permissions import SITE_PERMISSION
        return self.permission or (SITE_PERMISSION.get(self.source.site) if self.source else None)

    @property
    def is_secondary(self) -> bool:
        return self.secondary or (self.source is not None and self.source.site in SECONDARY_SITES)
