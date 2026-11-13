"""Klasik eserler (E2, `docs/e2-adaylar.md`, `docs/eserler/klasik.md`): koleksiyon `klasik`, ad alanı `klasik:`.

Birinci dilim (kullanıcının seçimi, 2026-11-13): belâgat ve terim eserleri; D2'nin taslakları bunlarla yazılır.
Eserler kendi metinlerinin sahibidir (`author`); muhakkik `editor`'dadır (yalnız sürümün üst bilgisi söylüyorsa;
tahmin edilmez), girişi ayrı katmandır (`authority: muhakkik`). Genel sunucuya girmez (`private`): klasik eserler
kendi bağdaştırıcısındadır (`profiles.KLASIK`, E2.4). Ayrıştırma `books/klasik_openiti.py`.
"""

from risale_mcp.catalog.model import Collection, Group, Site, SourceRef, Work


def _klasik(slug: str, title: str, author: str, editor: str | None, note: str) -> Work:
    return Work(slug, title, Group.KLASIK, SourceRef(Site.OPENITI, slug), language="ar", private=True,
                collection=Collection.KLASIK, author=author, editor=editor, note=note)


# Sıra müellifin vefatına göre (hicrî): Cürcânî 471, Râgıb 502, Sekkâkî 626, Seyyid Şerîf 816.
KLASIK_WORKS: tuple[Work, ...] = (
    _klasik("delailul-icaz", "Delâilü'l-İ'câz", "Abdülkāhir el-Cürcânî", "Mahmûd Muhammed Şâkir",
            "OpenITI Shamela0012055 (Medenî, 3. baskı 1413). Muhakkikin fıkra numaraları düğümdür."),
    _klasik("esrarul-belaga", "Esrârü'l-Belâğa", "Abdülkāhir el-Cürcânî", None,
            "OpenITI Shamela0008187 (Medenî; muhakkik satırı boş). Sürümün sonunda son paragrafın devamı eksik."),
    _klasik("mufredat", "el-Müfredât fî Garîbi'l-Kur'ân", "Râgıb el-İsfahânî", "Muhammed Seyyid Kîlânî",
            "OpenITI JK001150 (Kîlânî, Dâru'l-Ma'rife). Harf kitabı ve madde (kök) düğümdür. Dâvûdî baskısının "
            "Shamela sürümünde madde başlığı işareti kelimelerin içine girmiş, metin kurulamıyor."),
    _klasik("miftahul-ulum", "Miftâhu'l-Ulûm", "Sekkâkî", None,
            "OpenITI Shamela0026581 (Dâru'l-Kütübi'l-İlmiyye, 2. baskı 1407; muhakkik yazılmamış)."),
    _klasik("tarifat", "et-Ta'rîfât", "Seyyid Şerîf el-Cürcânî", None,
            "OpenITI Shamela0007312 (Dâru'l-Kütübi'l-İlmiyye, 1403; \"ضبطه وصححه جماعة من العلماء بإشراف الناشر\")."),
)
