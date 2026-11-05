"""Metin kullanım izinleri: `docs/izinler.md`'nin koddaki karşılığı (H3, `docs/tefsir-altyapi-plani.md`).

Her eser bir izin kaydına bağlıdır (`Work.permission`; verilmezse kaynağın sitesinden). Genel profil (sunucuya giden
veritabanı) yalnız `public` izinli eserleri kurar; izin kaydı olmayan ya da reddedilen kaynaktan gelen bir eser
genel profile girmeye kalkarsa kurulum durur (`build_db`). Eser sessizce düşmez: kullanıcı ya izni yazar ya eseri
`private` yapar. İstisna `Work.public_without_record`: kullanıcının kararını bekleyen açık mesele; kurulum raporu
her seferinde uyarır.

Yeni izin önce `docs/izinler.md`'ye, sonra buraya yazılır; ikisi aynı şeyi söylemelidir.
"""

from dataclasses import dataclass
from enum import StrEnum

from risale_mcp.catalog.model import Site


class Kind(StrEnum):
    GRANTED = "izin"           # kaynak açıkça izin verdi
    LICENCE = "lisans"         # genel lisans ya da telif bildirimiyle serbest
    UNRECORDED = "kayit-yok"   # izin kaydı yok
    REFUSED = "reddetti"       # kaynak izin vermedi


@dataclass(frozen=True)
class Permission:
    key: str
    source: str                # kim
    kind: Kind
    conditions: str            # şart
    record: str                # nasıl, ne zaman (izinler.md'deki "Kayıt")

    @property
    def public(self) -> bool:
        return self.kind in (Kind.GRANTED, Kind.LICENCE)


PERMISSIONS: dict[str, Permission] = {p.key: p for p in (
    Permission("erisale", "erisale.com (e-Risale)", Kind.GRANTED, "Kaynak gösterilecek",
               "Sözlü izin, görüşme 2026-10-30; her kullanım, kullanıcının bildirimi 2026-11-05"),
    Permission("risaleoku", "risaleoku.com", Kind.GRANTED, "Kazanç olmayacak, kaynak gösterilecek",
               "Site sahibinin yazılı cevabı (data/raw/kullanici/izinler/); her kullanım, 2026-11-05"),
    Permission("kesif", "Keşif Yolculukları Risale-i Nur Eğitim Programı (Ediz Sözüer)", Kind.LICENCE,
               "Asliyetini korumak ve kaynak belirtmek", "Telif bildirimi"),
    Permission("kastamonur", "kastamonur.com", Kind.GRANTED, "Kayıtlı değil", "Kullanıcının bildirimi, 2026-11-02"),
    Permission("nurpedia", "nurpedia.org", Kind.GRANTED, "Şart yok (\"uygun bulduğunuz şekilde\"); kaynak gösterme ricası",
               "Yazılı cevap, 2026-11-05 (data/raw/kullanici/izinler/)"),
    Permission("kullanici", "Kullanıcının dosyası", Kind.UNRECORDED, "Hak sahibi kayıtlı değil", "Kayıt yok"),
    Permission("risale-online", "risale.online (Hayrat)", Kind.UNRECORDED, "Kayıtlı değil", "Kayıt yok"),
    Permission("rasaelalnour", "Hizmet Vakfı (rasaelalnour.com)", Kind.REFUSED, "İzin verilmedi", "2026-10-30"),
    Permission("openiti", "OpenITI (KITAB projesi, Aga Khan University)", Kind.LICENCE,
               "CC BY-NC-SA 4.0: kaynak gösterilir (dosya ve sürüm), ticari kullanılmaz, aynı lisansla paylaşılır",
               "Lisans (Zenodo sürüm kaydı)"),
    Permission("yeniasya", "Yeni Asya", Kind.UNRECORDED, "Ortak proje planda; mevcut veri kullanılmıyor", "Kayıt yok"),
)}

SITE_PERMISSION = {
    Site.ERISALE: "erisale", Site.RISALEOKU_APP: "risaleoku", Site.RISALEOKU: "risaleoku", Site.KESIF: "kesif",
    Site.KASTAMONUR: "kastamonur", Site.KULLANICI: "kullanici", Site.RISALE_ONLINE: "risale-online",
    Site.RASAELALNOUR: "rasaelalnour", Site.YENIASYA: "yeniasya", Site.NURPEDIA: "nurpedia",
    Site.OPENITI: "openiti",
}
