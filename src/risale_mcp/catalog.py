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
    OSMANLICA = "osmanlica"


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

    @property
    def is_secondary(self) -> bool:
        return self.secondary or (self.source is not None and self.source.site in SECONDARY_SITES)


def _erisale(book: str, *sections: str, exclude: tuple[str, ...] = ()) -> SourceRef:
    return SourceRef(Site.ERISALE, book, sections, exclude)


def _ilk_donem(*sections: str) -> SourceRef:
    return _erisale("ilk-donem-eserleri", *sections)


_E, _A, _M, _H, _O = Group.ESKI_SAID, Group.ANA_CILT, Group.MECMUA, Group.HIZB, Group.OSMANLICA


def _app(book: str, *sections: str) -> SourceRef:
    return SourceRef(Site.RISALEOKU_APP, book, sections)   # bölümler: (ilk başlık, duracağı başlık)

WORKS: tuple[Work, ...] = (
    # --- Eski Said dönemi
    Work("kizil-icaz", "Kızıl İcaz", _E, None, Status.MISSING,
         "Türkçesi: ücretsiz tam tercüme bulunamadı (basılı tercümeler telifli). Arapçası Kızıl İcaz (Arapça)."),
    Work("kizil-icaz-arabi", "Kızıl İcaz (Arapça)", _E, _app("ar_asaribediyye", "قزل ايجاز", "تعليقات"),
         note="Arapça asıl: Ahdarî'nin Süllem'ine hâşiye; İhsan Kasım es-Sâlihî tahkiki (Saykalü'l-İslâm).",
         language="ar"),
    Work("talikat", "Ta'likat", _E, SourceRef(Site.KESIF, "talikat"),
         note="Türkçe tam tercüme (Protranslate; Keşif Yolculukları Risale-i Nur Eğitim Programı).",),
    Work("talikat-arabi", "Ta'likat (Arapça)", _E, _app("ar_asaribediyye", "تعليقات", "السانحات"),
         note="Arapça asıl: Gelenbevî'nin Burhân'ına hâşiye; İhsan Kasım es-Sâlihî tahkiki (Saykalü'l-İslâm).",
         language="ar"),
    Work("divan-i-harb-i-orfi", "Divan-ı Harb-i Örfî", _E, _ilk_donem("divan-i-harb-i-orfi")),
    Work("nutuk", "Nutuk", _E, _app("abed", "Nutuklar", "Makaleler Kısmı"), secondary=True,
         note="Âsâr-ı Bedîiyye baskısı. Ana parçası (Hürriyete Hitab) erisale'de Divan-ı Harb-i Örfî içinde."),
    Work("makalat", "Makalat", _E, _app("abed", "Makaleler Kısmı", "Lemeât"), secondary=True,
         note="Âsâr-ı Bedîiyye baskısı; 20 makale."),
    Work("muhakemat", "Muhakemat", _E, _erisale("muhakemat")),
    Work("teshisul-illet-zeyli", "Teşhisü'l-İllet'in Zeyli", _E,
         _app("abed", "TEŞHİS-ÜL İLLET'İN ZEYLİ", "İki Mekteb-i Musîbetin"),
         note="Hutbe-i Şamiye'nin Arapça zeylinin müellifçe Türkçeye çevrilmemiş kısımları; Âsâr-ı Bediiyye'deki tercüme."),
    Work("hakikat-cekirdekleri-2", "Hakikat Çekirdekleri (İkinci Cüz)", _E,
         _app("abed", "Hakikat Çekirdekleri (2)", "Bediüzzaman'ın Tarihçe-i Hayatı"), note="Âsâr-ı Bediiyye baskısı."),
    Work("vukufsuz-ehl-i-vukufa-cevap", "Vukufsuz Ehl-i Vukufa Cevap", _E,
         _app("abed", "VUKUFSUZ EHL-İ VUKUFA CEVAP", "HAZRET-İ ÜSTAD'IN TASHİH"), note="Âsâr-ı Bediiyye baskısı."),
    Work("hutbe-i-samiye", "Hutbe-i Şamiye", _E, _ilk_donem("hutbe-i-samiye")),
    Work("hutbe-i-samiye-arabi", "Hutbe-i Şamiye (Arapça)", _E, _app("ar_asaribediyye", "الخطبة الشامية", "الخطوات الست"),
         note="İhsan Kasım es-Sâlihî'nin Türkçeden tercümesi (1911'de okunan Arapça aslı değil).", language="ar"),
    Work("munazarat", "Münazarat", _E, _ilk_donem("munazarat")),
    Work("isaratul-icaz", "İşaratü'l-İ'caz", _E, _erisale("isaratul-icaz")),
    Work("isaratul-icaz-arabi", "İşârâtü'l-İ'câz (Arapça)", _E,
         _app("ar_isarat"),
         note="Arapça asıl; İhsan Kasım es-Sâlihî tahkiki. Türkçesi İşaratü'l-İ'caz (Abdülmecid Nursî tercümesi).",
         language="ar"),
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
    Work("el-mesnevi-el-arabi", "el-Mesnevî el-Arabî en-Nurî", _E, _app("ar_mesnevi"),
         note="Arapça asıl; İhsan Kasım es-Sâlihî tahkiki. Türkçesi Mesnevî-i Nuriye.", language="ar"),
    Work("el-mesnevi-el-arabi-harekeli", "el-Mesnevî el-Arabî en-Nurî (harekeli)", _E,
         SourceRef(Site.RASAELALNOUR, "mesnevi", ("المثنوي العربي النهائي.doc",)), private=True,
         note="Abdülkadir Badıllı'nın \"el-Kâmil\" baskısı (harekeli); yalnızca kullanıcıda, genel sunucuya çıkmaz.",
         language="ar"),
    Work("mesnevi-i-nuriye", "Mesnevî-i Nuriye", _E, _erisale("mesnevi-i-nuriye"),
         note="el-Mesnevî el-Arabî'nin Türkçesi."),
    Work("nurun-ilk-kapisi", "Nur'un İlk Kapısı", _E, _ilk_donem("nurun-ilk-kapisi")),
    # --- Risale-i Nur ana ciltleri
    Work("sozler", "Sözler", _A, _erisale("sozler", exclude=("lemeat",))),
    Work("mektubat", "Mektubat", _A, _erisale("mektubat", exclude=("hakikat-cekirdekleri",))),
    Work("lemalar", "Lem'alar", _A, _erisale("lemalar")),
    Work("sualar", "Şualar", _A, _erisale("sualar")),
    Work("rumuzat-i-semaniye", "Rumuzat-ı Semaniye", _A, SourceRef(Site.KULLANICI, "rumuzat-i-semaniye"),
         note="Yirmi Dokuzuncu Mektub'un Üçüncü, Dördüncü ve Sekizinci Kısımları; kullanıcının PDF'i. "
              "Mektubat'ta da bulunan paragraflar oraya eşlenir."),
    Work("barla-lahikasi", "Barla Lahikası", _A, _erisale("barla-lahikasi")),
    Work("kastamonu-lahikasi", "Kastamonu Lahikası", _A, _erisale("kastamonu-lahikasi")),
    Work("emirdag-lahikasi", "Emirdağ Lahikası", _A, _erisale("emirdag-lahikasi"), note="İki cilt."),
    Work("tarihce-i-hayat", "Tarihçe-i Hayat", _A, _erisale("tarihce-i-hayat")),
    # --- Tertip edilen mecmualar: metin ana ciltte bir kez durur, mecmua ona işaret eder.
    Work("asa-yi-musa", "Asâ-yı Mûsâ", _M, _erisale("asa-yi-musa")),
    Work("zulfikar", "Zülfikâr", _M, _app("ihlas_zulfikar")),
    Work("tilsimlar", "Tılsımlar Mecmuası", _M, _app("ihlas_tilsimlar")),
    Work("asar-i-bediiyye", "Âsâr-ı Bediiyye", _M, _app("abed"),
         note="Eski Said dönemi eserlerinin mecmuası; Abdülkadir Badıllı'nın derlemesi."),
    Work("sikke-i-tasdik-i-gaybi", "Sikke-i Tasdik-i Gaybî", _M, _erisale("sikke-i-tasdik-i-gaybi")),
    Work("iman-ve-kufur-muvazeneleri", "İman ve Küfür Muvazeneleri", _M, _erisale("iman-ve-kufur-muvazeneleri")),
    Work("siracun-nur", "Siracü'n-Nur", _M, _app("ihls_siracunnur")),
    Work("siracun-nur-hayrat", "Siracü'n-Nur (Hayrat)", _M, SourceRef(Site.RISALE_ONLINE, "siracun-nur"), private=True,
         note="Hayrat baskısı; Onikinci Şuâ'ya bağlı belgeler (raporlar, müdafaalar) yalnız burada. Yalnızca kullanıcıda."),
    Work("kucuk-sozler", "Küçük Sözler", _M, SourceRef(Site.RISALEOKU_APP, "rnk_ksozler")),
    Work("genclik-rehberi", "Gençlik Rehberi", _M, _app("rnk_gencreh")),
    Work("hanimlar-rehberi", "Hanımlar Rehberi", _M, _app("rnk_hanimreh")),
    Work("fihrist-risalesi", "Fihrist Risalesi", _M, _app("ihlas_fihristris"),
         note="Ana ciltlerin fihristelerinden derlenmiş; kullanıcının kararıyla 2026-10-30'da yeniden eklendi."),
    Work("esasat-i-nuriye", "Esasat-ı Nuriye", _M, _app("esasat"), private=True,
         note="Sonradan derleme: Rüşdü Tafral ve İttihad İlmî Araştırma Heyeti (İttihad Yayıncılık); Bediüzzaman'ın tertibi değil."),
    Work("hizmet-rehberi-ve-dusturlari", "Hizmet Rehberi ve Düsturları", _M, _app("hizmettoplama"), private=True,
         note="Sonradan derleme: Ahmet Koçoğlu (2018); Bediüzzaman'ın tertibi değil."),
    # --- Hizbler
    Work("hizbul-kuranil-muazzam", "Hizbü'l-Kur'ani'l-Muazzam", _H, SourceRef(Site.RISALEOKU_APP, "hizbkuran"), language="ar"),
    Work("hizb-i-nuri", "Hizbü'l-Ekber-i Nurî (Hizb-i Nurî)", _H,
         _app("ihlas_zulfikar", "Hizb-u Nur-il Ekber", "Hasan Feyzinin Mektubu"), language="ar",
         note="Zülfikâr'ın hâtimesi (İhlas Nur baskısı); müellifin takdimleriyle."),
    Work("hizbu-envaril-hakaik", "Hizbü Envari'l-Hakaiki'n-Nuriye (Büyük Cevşen)", _H,
         SourceRef(Site.RISALEOKU_APP, "hizbulhakaik"), note="Cevşenü'l-Kebîr bu cildin içindedir.", language="ar"),
    Work("tesbihat", "Namaz Tesbihatı", _H, _app("tesbihat"), language="ar",
         note="Beş vakit namazın tesbihatı; Bediüzzaman'ın eseri değil."),
    Work("celcelutiye", "Celcelutiye Kasidesi", _H, _app("celcelutiye"), language="ar",
         note="Bediüzzaman'ın eseri değil; rivayet edilen kaside."),
    Work("kenzul-ars", "Kenzü'l-Arş Duası", _H, _app("kenzulars"), language="ar",
         note="Bediüzzaman'ın eseri değil."),
    # --- Osmanlıca (Envar Neşriyat baskısı): Türkçe ciltlerin Arapça harfli metni; eşlenmez, anlamsal aramaya girmez.
    *(Work(f"{slug}-osmanlica", f"{title} (Osmanlıca)", _O, _app(book), language="os") for slug, title, book in (
        ("sozler", "Sözler", "ossozler"), ("mektubat", "Mektubat", "osmektubat"),
        ("lemalar", "Lem'alar", "oslemalar"), ("sualar", "Şualar", "ossualar"),
        ("mesnevi-i-nuriye", "Mesnevî-i Nuriye", "osmesnevi"), ("isaratul-icaz", "İşaratü'l-İ'caz", "osisarat"),
        ("barla-lahikasi", "Barla Lahikası", "osbarla"), ("kastamonu-lahikasi", "Kastamonu Lahikası", "oskastamonu"),
        ("emirdag-lahikasi-1", "Emirdağ Lahikası 1", "osemirdag1"), ("emirdag-lahikasi-2", "Emirdağ Lahikası 2", "osemirdag2"),
        ("sikke-i-tasdik-i-gaybi", "Sikke-i Tasdik-i Gaybî", "osstgayb"), ("tarihce-i-hayat", "Tarihçe-i Hayat", "ostarihce"),
        ("asa-yi-musa", "Asâ-yı Mûsâ", "osasamusa"), ("fihrist-risalesi", "Fihrist Risalesi", "osfihrist"),
        ("siracun-nur", "Siracü'n-Nur", "ossiracnur"), ("tilsimlar", "Tılsımlar", "ostilsimlar"))),
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
