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


# Sıra müellifin vefatına göre (hicrî): Ebû Hanîfe 150, Cürcânî 471, Râgıb 502, Gazâlî 505, Sekkâkî 626, Teftâzânî 792,
# Seyyid Şerîf 816, Kastalânî 923. E5'in eserleri (kullanıcının seçimi, 2026-11-24): `docs/e5-risalede-anilan-eserler.md`.
KLASIK_WORKS: tuple[Work, ...] = (
    _klasik("fikhul-ekber", "el-Fıkhu'l-Ekber", "Ebû Hanîfe", None,
            "OpenITI Shamela0006388 (Furkân 1419; Aliyyü'l-Kārî'nin şerhinden ayıklanmış metin, başlıklar yayıncının)."),
    _klasik("delailul-icaz", "Delâilü'l-İ'câz", "Abdülkāhir el-Cürcânî", "Mahmûd Muhammed Şâkir",
            "OpenITI Shamela0012055 (Medenî, 3. baskı 1413). Muhakkikin fıkra numaraları düğümdür."),
    _klasik("esrarul-belaga", "Esrârü'l-Belâğa", "Abdülkāhir el-Cürcânî", None,
            "OpenITI Shamela0008187 (Medenî; muhakkik satırı boş). Sürümün sonunda son paragrafın devamı eksik."),
    _klasik("mufredat", "el-Müfredât fî Garîbi'l-Kur'ân", "Râgıb el-İsfahânî", "Muhammed Seyyid Kîlânî",
            "OpenITI JK001150 (Kîlânî, Dâru'l-Ma'rife). Harf kitabı ve madde (kök) düğümdür. Dâvûdî baskısının "
            "Shamela sürümünde madde başlığı işareti kelimelerin içine girmiş, metin kurulamıyor."),
    _klasik("munkiz", "el-Munkız mine'd-Dalâl", "Gazâlî", "Muhammed Muhammed Câbir",
            "OpenITI ShamAY0033739 (Câbir, el-Mektebetü's-Sekâfiyye). Sürümde başlık yok: eser tek bölümdür."),
    _klasik("miftahul-ulum", "Miftâhu'l-Ulûm", "Sekkâkî", None,
            "OpenITI Shamela0026581 (Dâru'l-Kütübi'l-İlmiyye, 2. baskı 1407; muhakkik yazılmamış)."),
    _klasik("telvih", "et-Telvîh ilâ Keşfi Hakāiki't-Tenkîh", "Sa'deddîn et-Teftâzânî", "Zekeriyyâ Umeyrât",
            "OpenITI JK007110 (Umeyrât, Dâru'l-Kütübi'l-İlmiyye 1416): yalnız Teftâzânî'nin şerhi; Sadrüşşerîa'nın "
            "Tavzîh'i yok, \"قوله\" ile anılır. Başlıklar aynı baskının ShamAY0034200 sürümünün içindekilerinden."),
    _klasik("serhul-makasid", "Şerhu'l-Makāsıd", "Sa'deddîn et-Teftâzânî", None,
            "OpenITI JK001157 (Nu'mâniyye, Lahor 1401; muhakkik yazılmamış). Başlık satırı yok: bölümler "
            "Teftâzânî'nin kendi metnini \"قال\" ile aktardığı yerlerden."),
    _klasik("tarifat", "et-Ta'rîfât", "Seyyid Şerîf el-Cürcânî", None,
            "OpenITI Shamela0007312 (Dâru'l-Kütübi'l-İlmiyye, 1403; \"ضبطه وصححه جماعة من العلماء بإشراف الناشر\")."),
    _klasik("serhul-mevakif", "Şerhu'l-Mevâkıf", "Seyyid Şerîf el-Cürcânî", "Abdurrahman Umeyre",
            "OpenITI ShamAY0033881 (Umeyre, Dâru'l-Cîl 1417; OpenITI'de Îcî'nin adı altında \"المواقف\"). Îcî'nin "
            "metni baskının \"المتن\" diye ayırdığı yerde ayrı katmandır. Başlıklar Şâmile'nin içindekilerinden."),
    _klasik("mevahib", "el-Mevâhibü'l-Ledünniyye", "Kastalânî", None,
            "OpenITI Shamela0023685 (Tevfîkıyye, Kahire; muhakkik yazılmamış)."),
)


# Risale'nin bu eserleri andığı yerler (`risale_refs`, E5; kullanıcının kararları 2026-11-24): yalnız müellifin kendi
# sözünde, eserin adıyla geçen havale, nakil ve değerlendirme; kopyalar (Barla, Tarihçe, Fihrist, Türkçe tercüme) asıl
# yere indirgenmiştir. Kaynak `docs/e5-risalede-anilan-eserler.md`. Kimlikler genel profilin cümleleridir; `build_db`
# atfı oradan alır (Risale'nin metni klasik sunucuya kopyalanmaz). `target`: eserde Risale'nin kastettiği bölüm
# (biliniyorsa). Not İngilizce: modelin okuduğu alan.
RISALE_REFS: dict[str, tuple[dict, ...]] = {
    "delailul-icaz": (
        {"id": "muhakemat/makale-01/mesele-08/c045", "kind": "havale",
         "note": "Sends the reader to the Dala'il (its 221st 'gate') to see al-Jurjani rebuke those who cling to wording."},
        {"id": "isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/mesele-10/c014", "kind": "havale",
         "note": "For examples of adorned style, sends the reader to the Dala'il and the Asrar."},
        {"id": "isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/mesele-01/c001", "kind": "nakil",
         "note": "Eloquence lies in the arrangement of meanings (nazm), as al-Jurjani argued in the Dala'il and the Asrar."},
        {"id": "muhakemat/makale-02/mesele-01/c022", "kind": "nakil",
         "note": "Al-Jurjani filled a third of the Dala'il and the Asrar with remedies for attachment to wording."},
        {"id": "muhakemat/makale-02/mesele-12/c010", "kind": "degerlendirme",
         "note": "Praises the radiant prose of the Dala'il and the Asrar."},
    ),
    "esrarul-belaga": (
        {"id": "isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/mesele-10/c014", "kind": "havale",
         "note": "For examples of adorned style, sends the reader to the Dala'il and the Asrar."},
        {"id": "isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/c013", "kind": "nakil",
         "note": "Quotes the author of the Dala'il 'in his Asrar al-Balagha' on the effect of comparison (tamthil)."},
        {"id": "isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/mesele-01/c001", "kind": "nakil",
         "note": "Eloquence lies in the arrangement of meanings (nazm), as al-Jurjani argued in the Dala'il and the Asrar."},
        {"id": "muhakemat/makale-02/mesele-01/c022", "kind": "nakil",
         "note": "Al-Jurjani filled a third of the Dala'il and the Asrar with remedies for attachment to wording."},
        {"id": "muhakemat/makale-02/mesele-12/c010", "kind": "degerlendirme",
         "note": "Praises the radiant prose of the Dala'il and the Asrar."},
    ),
    "miftahul-ulum": (
        {"id": "isaratul-icaz-arabi/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-07/c061",
         "kind": "havale",
         "note": "Against those who claim to find grammatical faults in the Qur'an, sends the reader to the end (khatima) "
                 "of the Miftah."},
        {"id": "muhakemat/makale-01/mesele-08/c050", "kind": "nakil",
         "note": "As stated in the Miftah, rhetoricians use imaginary inversion (qalb) for rhetorical ends."},
    ),
    "telvih": (
        {"id": "mektubat/28/mesele-07/isaret-03/c004", "kind": "degerlendirme", "target": "telvih/3/3/4/3",
         "note": "Compares: al-Taftazani solved the question of destiny and free will only in forty-fifty pages, in the "
                 "'Twelve Premises' (al-muqaddimat al-ithna 'ashara) of the Talwih; the Risale explains it easily. Not a "
                 "referral."},
    ),
    "serhul-makasid": (
        {"id": "sozler/33/pencere-30/c005", "kind": "havale",
         "note": "Leaves the details of the proofs to the great books of the verifiers such as Sharh al-Mawaqif and "
                 "Sharh al-Maqasid."},
        {"id": "muhakemat/makale-01/mesele-01/c002", "kind": "havale",
         "note": "On the roundness of the earth: 'if you have a doubt, go to the Maqasid and the Mawaqif'."},
        {"id": "barla-lahikasi/kisim-03/213/c011", "kind": "nakil",
         "note": "Reports that Sa'd (al-Taftazani) holds in the Maqasid and its Sharh that the spirit is created."},
    ),
    "serhul-mevakif": (
        {"id": "sozler/33/pencere-30/c005", "kind": "havale",
         "note": "Leaves the details of the proofs to the great books of the verifiers such as Sharh al-Mawaqif and "
                 "Sharh al-Maqasid."},
        {"id": "muhakemat/makale-01/mesele-01/c002", "kind": "havale",
         "note": "On the roundness of the earth: 'if you have a doubt, go to the Maqasid and the Mawaqif'."},
        {"id": "sozler/32/mevkif-02/maksad-03/ikinci-sik-sual-ve-cevabi/remiz-02/c001", "kind": "nakil",
         "note": "Quotes Sayyid Sharif in Sharh al-Mawaqif on the four causes of love."},
    ),
    "fikhul-ekber": (
        {"id": "sunuhat/kuranin-hakimiyet-i-mutlakasi/c028", "kind": "degerlendirme",
         "note": "Names it, with the Muwatta', among the books of the early mujtahids."},
    ),
    "mevahib": (
        {"id": "suaat-i-marifetin-nebi/mukaddime/c022", "kind": "havale",
         "note": "For the miracles in detail: Qadi 'Iyad in al-Shifa' and al-Qastallani in al-Mawahib."},
    ),
}
RISALE_UNNAMED = {   # eser Risale'de adıyla anılmaz: araç bunu söyler (tanıtımın sözü "havale ettiği ve dayandığı")
    "munkiz": "The Risale-i Nur does not name this work; it cites al-Ghazali often as a source, without a title.",
    "mufredat": "The Risale-i Nur does not name this work or its author.",
    "tarifat": "The Risale-i Nur does not name this work; it names its author as the commentator of al-Mawaqif.",
}
