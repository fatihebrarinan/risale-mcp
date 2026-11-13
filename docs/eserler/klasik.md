# Klasik eserler: kontrol listesi

> (a) `uv run python -m risale_mcp.checklist` ile üretilir, elle düzenlemeyin; (b) ve (c) elle tutulur, yeniden üretimde korunur.
> Eserlerin listesi ve kaynakları: `src/risale_mcp/catalog/`.
> Eser ekleme ölçütü ve sıra: `PLANLAR.md` E2.

## (a) Eklenenler

- **Ham veri:** 5/5 eser indirildi.
- **Ayrıştırma:** 5/5 eser.
- **Kaynağı bulunamayan:** yok.

İşaretler: ✅ tamam · ⚠️ kısmen · ⬜ yapılmadı · ❌ kaynak yok · ⏸️ ertelendi

### Belâgat ve terim (1. dilim)

| # | Eser | Kaynak | Ham veri | Ayrıştırma | Not |
|---:|---|---|---|---|---|
| 1 | Delâilü'l-İ'câz | `openiti/delailul-icaz` | ✅ indirildi | ✅ 760 düğüm, 3023 paragraf, 4507 cümle | OpenITI Shamela0012055 (Medenî, 3. baskı 1413). Muhakkikin fıkra numaraları düğümdür. |
| 2 | Esrârü'l-Belâğa | `openiti/esrarul-belaga` | ✅ indirildi | ✅ 36 düğüm, 1257 paragraf, 1635 cümle | OpenITI Shamela0008187 (Medenî; muhakkik satırı boş). Sürümün sonunda son paragrafın devamı eksik. |
| 3 | el-Müfredât fî Garîbi'l-Kur'ân | `openiti/mufredat` | ✅ indirildi | ✅ 1630 düğüm, 2392 paragraf, 4494 cümle | OpenITI JK001150 (Kîlânî, Dâru'l-Ma'rife). Harf kitabı ve madde (kök) düğümdür. Dâvûdî baskısının Shamela sürümünde madde başlığı işareti kelimelerin içine girmiş, metin kurulamıyor. |
| 4 | Miftâhu'l-Ulûm | `openiti/miftahul-ulum` | ✅ indirildi | ✅ 130 düğüm, 1386 paragraf, 2237 cümle | OpenITI Shamela0026581 (Dâru'l-Kütübi'l-İlmiyye, 2. baskı 1407; muhakkik yazılmamış). |
| 5 | et-Ta'rîfât | `openiti/tarifat` | ✅ indirildi | ✅ 30 düğüm, 2088 paragraf, 2275 cümle | OpenITI Shamela0007312 (Dâru'l-Kütübi'l-İlmiyye, 1403; "ضبطه وصححه جماعة من العلماء بإشراف الناشر"). |

Kaynak alınmaz (`catalog/excluded.py`, kullanıcının kararı): Muhammed Abduh: kaynak alınmaz; Tefsîru'l-Menâr: Abduh'un derslerine dayanır, kaynak alınmaz.

<!-- Bu satırın altı elle tutulur; checklist yeniden üretirken korur. -->

Şartlar (PLANLAR.md E2): **1** Risale'de anılma ya da künye, **2** muhakkiki bilinen nüsha ve açık izin, **3** gerçekçi soru. "?" henüz sayılmadı (E2.1). Künye sayıları `data/interim/hadis/kunye.md`'den, boyutlar `docs/mvp-kitaplar.md`'den (2026-11-06).

## (b) Eklenmesi çok iyi olacaklar

E2.1'in aday listesinden (`docs/e2-adaylar.md`, 2026-11-13); seçim kullanıcının (E2.2, 2026-11-13). Sıra: 1. dilim şimdi
(E2.3), 2. dilim sonra, 3. dilim ondan sonra (E5). Nüsha sütunu öneridir; muhakkiki yazılmamış olanlarda E2.3'te
sürümün kendisinde bakılır. "Anma": Risale'de eserin adı / müellifin adı (cümle sayısı).

**1. dilim: belâgat ve terim** eklendi (E2.3, 2026-11-13): yukarıda (a). Sürüm değişiklikleri ham verinin
incelemesinden: Ta'rîfât'ta Shamela sürümü (Ebyârî'nin JK sürümünde OCR artıkları var), Müfredât'ta Kîlânî'nin JK
sürümü (Dâvûdî'nin Shamela sürümünde madde başlığı işareti kelimelerin içine girmiş). Kurallar `books/klasik_openiti.py`.

**2. dilim: Risale'nin okuru gönderdiği kelâm ve tasavvuf eserleri (sonra, E5)**

| Eser | Müellif (ö.) | Nüsha (OpenITI) | Kelime | Anma | 1 | 2 | 3 | Gerekçe |
|---|---|---|---:|---|:-:|:-:|:-:|---|
| Şerhu'l-Makāsıd | Teftâzânî (792) | `0792IbnCumarTaftazani.SharhMaqasid.JK001157`: Nu'mâniyye, Lahor (muhakkik yazılmamış) | 296 bin | 2 / 11 | ✓ | ◐ | ✓ | Risale kelâmın tafsilatını ona ve Şerhu'l-Mevâkıf'a havale eder (Sözler › Otuzüçüncü Söz › Otuzuncu Pencere) |
| et-Telvîh | Teftâzânî (792) | `0792IbnCumarTaftazani.TalwihCalaTawdih.JK007110`: Zekeriyyâ Umeyrât, DKİ | 232 bin | 3 (+4 "Mukaddemât-ı İsnâ Aşer") | ✓ | ✓ | ◐ | Mektubat kader meselesinde onun Mukaddemât-ı İsnâ Aşer'ini anar; gerekirse yalnız o bölüm |
| el-Munkız mine'd-Dalâl | Gazâlî (505) | `0505Ghazali.Munqidh.JK009330`: Muhammed M. Câbir | 11 bin | — / 39 | ◐ | ✓ | ✓ | Gazâlî'nin kendi yolunu anlattığı kısa eser |
| el-Fıkhu'l-Ekber | Ebû Hanîfe (150) | `0150AbuHanifa.FiqhAkbar.JK001085`: Furkân (şerhten ayıklanmış) | 1.656 | 1 / 39 | ✓ | ◐ | ✓ | Sünuhat selefin kitabı diye anar; akîdenin en kısa klasik metni |
| İhyâu Ulûmi'd-Dîn | Gazâlî (505) | `0505Ghazali.IhyaCulumDin.JK000001`: Dâru'l-Ma'rife (muhakkik yazılmamış) | 992 bin | 82 künye / 39 | ✓ | ◐ | ✓ | Risale'nin 82 hadis künyesi ona gider (hadis kitabı sayılmaz) |

**3. dilim: siyer ve mu'cizât (2. dilimden sonra, E5)**

| Eser | Müellif (ö.) | Nüsha (OpenITI) | Kelime | Anma | 1 | 2 | 3 | Gerekçe |
|---|---|---|---:|---|:-:|:-:|:-:|---|
| el-Mevâhibü'l-Ledünniyye | Kastalânî (923) | `0923AhmadQastallani.MawahibLaduniyya.Shamela0023685`: Tevfîkıyye (muhakkik yazılmamış) | 441 bin | 1 / 1, 4 künye | ✓ | ◐ | ◐ | Şuââtü Ma'rifeti'n-Nebî mu'cizâtın tafsili için onu Şifâ ile birlikte anar |

3. dilimin öbür eseri Şerhu'ş-Şifâ hadis sunucusuna girer (kullanıcının kararı, 2026-11-13): `docs/eserler/hadis.md` (b).

## (c) Aklımızda bulunsun

Kullanıcının kararı (2026-11-13): seçmeliler ve bekleyenler burada durur; yer ve zaman müsait olunca E5'te eklenmeye
çalışılır. Fütûhu'l-Gayb, Mesnevî ve Mektûbât "çok çok kıymetli" (kullanıcı): nüsha ve izin yolu açılınca öncelikli.

| Eser | Neden beklediği |
|---|---|
| Fütûhu'l-Gayb (Abdülkādir-i Geylânî, 561) | Risale adıyla 12 kez anar (tefe'ül hikâyesi). OpenITI'de yok; izinli başka nüsha aranır |
| Mektûbât (İmâm-ı Rabbânî, 1034) | Risale çok anar (Tarihçe'deki tefe'ül; müellif 56). Aslı Farsça; OpenITI'de yok, Arapça tercümesi de yok |
| Mesnevî (Mevlânâ, 672) | Risale çok anar (Mevlânâ 53). Farsça; nüsha ve izin aranır |
| Şerhu'l-Mevâkıf (Seyyid Şerîf, 816) | Risale adıyla anar ve alıntı yapar. OpenITI'de yalnız OCR sürümü (Kraken, baskısı yazılmamış, 891 bin kelime); Îcî'nin el-Mevâkıf'ı (`JK001335`, Umeyre, Dâru'l-Cîl) şerhle basılmış olabilir, bakılacak |
| el-Fütûhâtü'l-Mekkiyye (İbn Arabî, 638) | Adıyla 3, müellif 55. 1,83 milyon kelime, muhakkiki yok |
| el-Bidâye ve'n-Nihâye (İbn Kesîr, 774) | 48 künye; Türkî tahkiki var (`Shamela0004445`). 2,19 milyon kelime; yalnız siyer kısmı (`Shamela0000930`, 559 bin) bir seçenek |
| el-Mîzânü'l-Kübrâ (Şa'rânî, 973) | Sözler "Mîzan-ı Şa'rânî" der, 4 künye; OpenITI'de yok |
| el-Kitâb (Sîbeveyh, 180) | Seçmeli: İşârât harflerin mânâsında ona dayanır; Abdüsselâm Hârûn tahkiki var (`JK006989`), 278 bin. Çok teknik |
| el-Îzâh (Hatîb el-Kazvînî, 739) ya da Muhtasarü'l-Meânî (Teftâzânî) | Seçmeli: medrese belâgatının ölçünlü terimleri; Risale adlarını anmaz. İkisinden biri yeter (`JK001001` Gazzâvî; `ShamAY0033799`) |
| el-Kâmûsu'l-Muhît (Fîrûzâbâdî, 817) | Seçmeli: Tarihçe'de ezber hikâyesi, Kızıl İcaz anar. Birimi madde: ayrı bir model ister |
| el-Beyân ve't-Tebyîn (Câhız, 255) | İşârât Câhız'ı i'câzın üçüncü yolunda anar, ama o görüş bu eserde değil; muhakkiki yok |
| er-Risâletü'l-Kuşeyriyye, Lisânü'l-Arab | Risale anmaz; öncelik yok (Lisân 3 milyon kelime) |
| "Bediüzzaman'ın ezberlediği 90 kitap" | Bir liste değil, bir rivayet; çoğu medrese ders kitabıdır ve 3. şartı tutmaz. Ad ad bilinenler E2.1'de sınandı |
| Süllem (Ahdarî), Burhân (Gelenbevî) | Kızıl İcaz ve Ta'likat'ın metinleri; Süllem'in beyitleri Kızıl İcaz'da, Burhân'ınki Ta'likat'ın Arapçasında aralara serpilmiş. OpenITI'de yoklar |

Nesîmü'r-Riyâz (Hafâcî; 58 künye) hadis listesinin (c)'sindedir.
