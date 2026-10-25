"""Bediüzzaman Said Nursî'nin eserleri ve her birinin metin kaynağı.

Her eser, `data/books/<slug>.json` dosyasına dönüşecek bir birimdir. Bir kaynak kitabı
birden fazla esere bölünebilir (ör. erisale'deki "İlk Dönem Eserleri"), bir eser de
başka bir kaynak kitabının yalnızca bazı bölümlerinden oluşabilir (ör. Lemeat).

Bölüm seçicileri (`sections`, `exclude`) kaynağa özgüdür. erisale için bunlar bölüm
slug'larının önekleridir: `"lemeat"` hem `lemeat` hem `lemeat-tenbih` bölümünü kapsar.
"""

from dataclasses import dataclass
from enum import StrEnum


class Group(StrEnum):
    ESKI_SAID = "eski-said"
    ANA_CILT = "ana-cilt"
    MECMUA = "mecmua"
    HIZB = "hizb"


class Status(StrEnum):
    READY = "ready"          # kaynak belli, indirilebilir
    VERIFY = "verify"        # kaynak belli ama içeriğin tam/doğru olduğu doğrulanmalı
    DEFERRED = "deferred"    # kullanıcı kararıyla ertelendi
    MISSING = "missing"      # henüz kaynak bulunamadı


class Site(StrEnum):
    ERISALE = "erisale"              # erisale.com: standart baskı, birincil kaynak
    RISALE_ONLINE = "risale_online"  # risale.online: Hayrat baskısı
    RISALEOKU = "risaleoku"          # risaleoku.com
    YENIASYA = "yeniasya"            # yeniasya.com.tr/risaleinur: bozuk kodlu PDF metni, son çare


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
    language: str = "tr"            # metnin dili: "tr" ya da "ar" (Arapça eserler sağdan sola)


def _erisale(book: str, *sections: str, exclude: tuple[str, ...] = ()) -> SourceRef:
    return SourceRef(Site.ERISALE, book, sections, exclude)


def _ilk_donem(*sections: str) -> SourceRef:
    return _erisale("ilk-donem-eserleri", *sections)


_E, _A, _M, _H = Group.ESKI_SAID, Group.ANA_CILT, Group.MECMUA, Group.HIZB

WORKS: tuple[Work, ...] = (
    # --- Eski Said dönemi
    Work("kizil-icaz", "Kızıl İcaz", _E, None, Status.MISSING, "Arapça mantık eseri.", language="ar"),
    Work("talikat", "Ta'likat", _E, None, Status.MISSING, "Arapça mantık eseri.", language="ar"),
    Work("divan-i-harb-i-orfi", "Divan-ı Harb-i Örfî", _E, _ilk_donem("divan-i-harb-i-orfi")),
    Work("nutuk", "Nutuk", _E, SourceRef(Site.YENIASYA, "eskisaiddonemieserleri", ("nutuk",)),
         note="Ana parçası (Hürriyete Hitab) erisale'de Divan-ı Harb-i Örfî içinde."),
    Work("makalat", "Makalat", _E, SourceRef(Site.YENIASYA, "eskisaiddonemieserleri", ("makalat",))),
    Work("muhakemat", "Muhakemat", _E, _erisale("muhakemat")),
    Work("hutbe-i-samiye", "Hutbe-i Şamiye", _E, _ilk_donem("hutbe-i-samiye")),
    Work("munazarat", "Münazarat", _E, _ilk_donem("munazarat")),
    Work("isaratul-icaz", "İşaratü'l-İ'caz", _E, _erisale("isaratul-icaz")),
    Work("sunuhat", "Sünuhat", _E, _ilk_donem("sunuhat")),
    Work("tuluat", "Tuluat", _E, _ilk_donem("tuluat")),
    Work("rumuz", "Rumuz", _E, _ilk_donem("rumuz")),
    Work("isarat", "İşarat", _E, _ilk_donem("isarat")),
    Work("lemeat", "Lemeat", _E, _erisale("sozler", "lemeat"),
         note="Standart baskıda Sözler'in sonunda."),
    Work("hutuvat-i-sitte", "Hutuvat-ı Sitte", _E, _ilk_donem("hutuvat-i-sitte")),
    Work("hakikat-cekirdekleri", "Hakikat Çekirdekleri", _E, _erisale("mektubat", "hakikat-cekirdekleri"),
         note="Standart baskıda Mektubat'ın sonunda."),
    Work("suaat-i-marifetin-nebi", "Şuaat-ı Marifetü'n-Nebi", _E, _ilk_donem("suaat-i-marifetin-nebi-asm")),
    Work("nokta", "Nokta", _E, _ilk_donem("nokta-risalesi")),
    Work("el-mesnevi-el-arabi", "el-Mesnevî el-Arabî en-Nurî", _E, SourceRef(Site.RISALEOKU, "ar_mesnevi"),
         note="Arapça asıl; İhsan Kasım es-Sâlihî tahkiki (Külliyât-ı Resâili'n-Nûr 6).", language="ar"),
    Work("mesnevi-i-nuriye", "Mesnevî-i Nuriye", _E, _erisale("mesnevi-i-nuriye"),
         note="el-Mesnevî el-Arabî'nin Türkçesi."),
    Work("nurun-ilk-kapisi", "Nur'un İlk Kapısı", _E, _ilk_donem("nurun-ilk-kapisi")),
    # --- Risale-i Nur ana ciltleri
    Work("sozler", "Sözler", _A, _erisale("sozler", exclude=("lemeat",))),
    Work("mektubat", "Mektubat", _A, _erisale("mektubat", exclude=("hakikat-cekirdekleri",))),
    Work("lemalar", "Lem'alar", _A, _erisale("lemalar")),
    Work("sualar", "Şualar", _A, _erisale("sualar")),
    Work("rumuzat-i-semaniye", "Rumuzat-ı Semaniye", _A,
         _erisale("mektubat", "yirmidokuzuncu-mektub-sekizinci-kisim-olan-rumuzat-i-semaniye"),
         Status.DEFERRED, "Hususi bir risale; kullanıcı kararıyla şimdilik eklenmiyor. erisale'de metin yok."),
    Work("barla-lahikasi", "Barla Lahikası", _A, _erisale("barla-lahikasi")),
    Work("kastamonu-lahikasi", "Kastamonu Lahikası", _A, _erisale("kastamonu-lahikasi")),
    Work("emirdag-lahikasi", "Emirdağ Lahikası", _A, _erisale("emirdag-lahikasi"), note="İki cilt."),
    Work("tarihce-i-hayat", "Tarihçe-i Hayat", _A, _erisale("tarihce-i-hayat")),
    # --- Tertip edilen mecmualar: metin ana ciltte bir kez durur, mecmua ona işaret eder.
    Work("asa-yi-musa", "Asâ-yı Mûsâ", _M, _erisale("asa-yi-musa")),
    Work("zulfikar", "Zülfikâr", _M, SourceRef(Site.RISALE_ONLINE, "zulfikar")),
    Work("tilsimlar", "Tılsımlar Mecmuası", _M, SourceRef(Site.RISALE_ONLINE, "tilsimlar")),
    Work("sikke-i-tasdik-i-gaybi", "Sikke-i Tasdik-i Gaybî", _M, _erisale("sikke-i-tasdik-i-gaybi")),
    Work("iman-ve-kufur-muvazeneleri", "İman ve Küfür Muvazeneleri", _M, _erisale("iman-ve-kufur-muvazeneleri")),
    Work("siracun-nur", "Siracü'n-Nur", _M, SourceRef(Site.RISALE_ONLINE, "siracun-nur")),
    Work("kucuk-sozler", "Küçük Sözler", _M, SourceRef(Site.RISALEOKU, "ksozler")),
    Work("fihrist-risalesi", "Fihrist Risalesi", _M, SourceRef(Site.RISALEOKU, "osfihrist"),
         Status.DEFERRED, "Yalnızca Osmanlıca bulundu."),
    Work("genclik-rehberi", "Gençlik Rehberi", _M, SourceRef(Site.RISALE_ONLINE, "genclik-rehberi")),
    Work("hanimlar-rehberi", "Hanımlar Rehberi", _M, SourceRef(Site.RISALE_ONLINE, "hanimlar-rehberi")),
    # --- Hizbler
    Work("hizbul-kuranil-muazzam", "Hizbü'l-Kur'ani'l-Muazzam", _H, SourceRef(Site.RISALEOKU, "hizbkuran"), language="ar"),
    Work("hizb-i-nuri", "Hizbü'l-Ekber-i Nurî (Hizb-i Nurî)", _H, None, Status.MISSING,
         "Kısmen Lem'alar'da.", language="ar"),
    Work("hizbu-envaril-hakaik", "Hizbü Envari'l-Hakaiki'n-Nuriye (Büyük Cevşen)", _H,
         SourceRef(Site.RISALEOKU, "hizbulhakaik"), note="Cevşenü'l-Kebîr bu cildin içindedir.", language="ar"),
)

_BY_SLUG = {work.slug: work for work in WORKS}


def get_work(slug: str) -> Work:
    try:
        return _BY_SLUG[slug]
    except KeyError:
        raise KeyError(f"Katalogda böyle bir eser yok: {slug!r}") from None


def works_from(site: Site, book: str) -> list[Work]:
    """Aynı kaynak kitabından beslenen eserler (ör. erisale/sozler -> Sözler ve Lemeat)."""
    return [w for w in WORKS if w.source and w.source.site == site and w.source.book == book]
