# Klasik eserler: kontrol listesi

> (a) `uv run python -m risale_mcp.checklist` ile üretilir, elle düzenlemeyin; (b) ve (c) elle tutulur, yeniden üretimde korunur.
> Koleksiyonu henüz yok; ilk eser eklenince katalogdan üretilir.
> Eser ekleme ölçütü ve sıra: `PLANLAR.md` E2.

## (a) Eklenenler

Henüz eklenen eser yok.

Kaynak alınmaz (`catalog/excluded.py`, kullanıcının kararı): Muhammed Abduh: kaynak alınmaz; Tefsîru'l-Menâr: Abduh'un derslerine dayanır, kaynak alınmaz.

<!-- Bu satırın altı elle tutulur; checklist yeniden üretirken korur. -->

Şartlar (PLANLAR.md E2): **1** Risale'de anılma ya da künye, **2** muhakkiki bilinen nüsha ve açık izin, **3** gerçekçi soru. "?" henüz sayılmadı (E2.1). Künye sayıları `data/interim/hadis/kunye.md`'den, boyutlar `docs/mvp-kitaplar.md`'den (2026-11-06).

## (b) Eklenmesi çok iyi olacaklar

E2.1'in aday listesinden (`docs/e2-adaylar.md`, 2026-11-13); seçim kullanıcının (E2.2, 2026-11-13). Sıra: 1. dilim şimdi
(E2.3), 2. dilim sonra, 3. dilim ondan sonra (E5). Nüsha sütunu öneridir; muhakkiki yazılmamış olanlarda E2.3'te
sürümün kendisinde bakılır. "Anma": Risale'de eserin adı / müellifin adı (cümle sayısı).

**1. dilim: belâgat ve terim (E2.3, şimdi; D2'nin ön şartı)**

| Eser | Müellif (ö.) | Nüsha (OpenITI) | Kelime | Anma | 1 | 2 | 3 | Gerekçe |
|---|---|---|---:|---|:-:|:-:|:-:|---|
| Delâilü'l-İ'câz | Abdülkāhir el-Cürcânî (471) | `0471CabdQahirJurjani.DalailIcjaz.Shamela0012055`: Mahmûd M. Şâkir, Medenî | 484 bin | 1+9 / 13 | ✓ | ✓ | ✓ | İşârât'ın nazım nazariyesinin kaynağı ("ونحن على مذهبه"); Muhakemat ve Kızıl İcaz adıyla anar |
| Esrârü'l-Belâğa | Abdülkāhir el-Cürcânî (471) | `0471CabdQahirJurjani.AsrarBalagha.Shamela0008187`: Medenî (Şâkir baskısı) | 315 bin | Delâil'le / 13 | ✓ | ✓ | ✓ | İşârât okuru temsil bahsinde ona gönderir ve ondan uzun alıntı yapar |
| Miftâhu'l-Ulûm | Sekkâkî (626) | `0626IbnMuhammadKhwarazmiSakkaki.MiftahCulum.Shamela0026581`: DKİ (muhakkik yazılmamış) | 572 bin | 2 / 17 | ✓ | ◐ | ✓ | İşârât "خاتمة مفتاح السكاكي"ye gönderir; medrese belâgatının çerçevesi |
| et-Ta'rîfât | Seyyid Şerîf el-Cürcânî (816) | `0816IbnMuhammadSharifJurjani.Tacrifat.JK000768`: İbrâhîm el-Ebyârî | 218 bin | ? / 4 | ◐ | ✓ | ✓ | Terim sözlüğü: İşârât, Kızıl İcaz ve Ta'likat okuru için |
| el-Müfredât | Râgıb el-İsfahânî (502) | `0502RaghibIsbahani.Mufradat.Shamela0023636`: Safvân Dâvûdî, Dâru'l-Kalem | 891 bin | — | ✗ | ✓ | ✓ | Kur'ân kelimelerinin sözlüğü; taslakların "dil" iddiaları ve tefsir altyapısı |

**2. dilim: Risale'nin okuru gönderdiği kelâm ve tasavvuf eserleri (sonra, E5)**

| Eser | Müellif (ö.) | Nüsha (OpenITI) | Kelime | Anma | 1 | 2 | 3 | Gerekçe |
|---|---|---|---:|---|:-:|:-:|:-:|---|
| Şerhu'l-Makāsıd | Teftâzânî (792) | `0792IbnCumarTaftazani.SharhMaqasid.JK001157`: Nu'mâniyye, Lahor (muhakkik yazılmamış) | 1,30 milyon | 2 / 11 | ✓ | ◐ | ✓ | Risale kelâmın tafsilatını ona ve Şerhu'l-Mevâkıf'a havale eder (Sözler › Otuzüçüncü Söz › Otuzuncu Pencere) |
| et-Telvîh | Teftâzânî (792) | `0792IbnCumarTaftazani.TalwihCalaTawdih.JK007110`: Zekeriyyâ Umeyrât, DKİ | 997 bin | 3 (+4 "Mukaddemât-ı İsnâ Aşer") | ✓ | ✓ | ◐ | Mektubat kader meselesinde onun Mukaddemât-ı İsnâ Aşer'ini anar; gerekirse yalnız o bölüm |
| el-Munkız mine'd-Dalâl | Gazâlî (505) | `0505Ghazali.Munqidh.JK009330`: Muhammed M. Câbir | 48 bin | — / 39 | ◐ | ✓ | ✓ | Gazâlî'nin kendi yolunu anlattığı kısa eser |
| el-Fıkhu'l-Ekber | Ebû Hanîfe (150) | `0150AbuHanifa.FiqhAkbar.JK001085`: Furkân (şerhten ayıklanmış) | 7 bin | 1 / 39 | ✓ | ◐ | ✓ | Sünuhat selefin kitabı diye anar; akîdenin en kısa klasik metni |
| İhyâu Ulûmi'd-Dîn | Gazâlî (505) | `0505Ghazali.IhyaCulumDin.JK000001`: Dâru'l-Ma'rife (muhakkik yazılmamış) | 4,12 milyon | 82 künye / 39 | ✓ | ◐ | ✓ | Risale'nin 82 hadis künyesi ona gider (hadis kitabı sayılmaz) |

**3. dilim: siyer ve mu'cizât (2. dilimden sonra, E5)**

| Eser | Müellif (ö.) | Nüsha (OpenITI) | Kelime | Anma | 1 | 2 | 3 | Gerekçe |
|---|---|---|---:|---|:-:|:-:|:-:|---|
| el-Mevâhibü'l-Ledünniyye | Kastalânî (923) | `0923AhmadQastallani.MawahibLaduniyya.Shamela0023685`: Tevfîkıyye (muhakkik yazılmamış) | 1,88 milyon | 1 / 1, 4 künye | ✓ | ◐ | ◐ | Şuââtü Ma'rifeti'n-Nebî mu'cizâtın tafsili için onu Şifâ ile birlikte anar |

3. dilimin öbür eseri Şerhu'ş-Şifâ hadis sunucusuna girer (kullanıcının kararı, 2026-11-13): `docs/eserler/hadis.md` (b).

## (c) Aklımızda bulunsun

Kullanıcının kararı (2026-11-13): seçmeliler ve bekleyenler burada durur; yer ve zaman müsait olunca E5'te eklenmeye
çalışılır. Fütûhu'l-Gayb, Mesnevî ve Mektûbât "çok çok kıymetli" (kullanıcı): nüsha ve izin yolu açılınca öncelikli.

| Eser | Neden beklediği |
|---|---|
| Fütûhu'l-Gayb (Abdülkādir-i Geylânî, 561) | Risale adıyla 12 kez anar (tefe'ül hikâyesi). OpenITI'de yok; izinli başka nüsha aranır |
| Mektûbât (İmâm-ı Rabbânî, 1034) | Risale çok anar (Tarihçe'deki tefe'ül; müellif 56). Aslı Farsça; OpenITI'de yok, Arapça tercümesi de yok |
| Mesnevî (Mevlânâ, 672) | Risale çok anar (Mevlânâ 53). Farsça; nüsha ve izin aranır |
| Şerhu'l-Mevâkıf (Seyyid Şerîf, 816) | Risale adıyla anar ve alıntı yapar. OpenITI'de yalnız OCR sürümü (Kraken, baskısı yazılmamış, 3,9 milyon kelime); Îcî'nin el-Mevâkıf'ı (`JK001335`, Umeyre, Dâru'l-Cîl) şerhle basılmış olabilir, bakılacak |
| el-Fütûhâtü'l-Mekkiyye (İbn Arabî, 638) | Adıyla 3, müellif 55. 7,5 milyon kelime, muhakkiki yok |
| el-Bidâye ve'n-Nihâye (İbn Kesîr, 774) | 48 künye; Türkî tahkiki var (`Shamela0004445`). 8,9 milyon kelime; yalnız siyer kısmı (`Shamela0000930`, 2,2 milyon) bir seçenek |
| el-Mîzânü'l-Kübrâ (Şa'rânî, 973) | Sözler "Mîzan-ı Şa'rânî" der, 4 künye; OpenITI'de yok |
| el-Kitâb (Sîbeveyh, 180) | Seçmeli: İşârât harflerin mânâsında ona dayanır; Abdüsselâm Hârûn tahkiki var (`JK006989`), 1,12 milyon. Çok teknik |
| el-Îzâh (Hatîb el-Kazvînî, 739) ya da Muhtasarü'l-Meânî (Teftâzânî) | Seçmeli: medrese belâgatının ölçünlü terimleri; Risale adlarını anmaz. İkisinden biri yeter (`JK001001` Gazzâvî; `ShamAY0033799`) |
| el-Kâmûsu'l-Muhît (Fîrûzâbâdî, 817) | Seçmeli: Tarihçe'de ezber hikâyesi, Kızıl İcaz anar. Birimi madde: ayrı bir model ister |
| el-Beyân ve't-Tebyîn (Câhız, 255) | İşârât Câhız'ı i'câzın üçüncü yolunda anar, ama o görüş bu eserde değil; muhakkiki yok |
| er-Risâletü'l-Kuşeyriyye, Lisânü'l-Arab | Risale anmaz; öncelik yok (Lisân 12,5 milyon kelime) |
| "Bediüzzaman'ın ezberlediği 90 kitap" | Bir liste değil, bir rivayet; çoğu medrese ders kitabıdır ve 3. şartı tutmaz. Ad ad bilinenler E2.1'de sınandı |
| Süllem (Ahdarî), Burhân (Gelenbevî) | Kızıl İcaz ve Ta'likat'ın metinleri; Süllem'in beyitleri Kızıl İcaz'da, Burhân'ınki Ta'likat'ın Arapçasında aralara serpilmiş. OpenITI'de yoklar |

Nesîmü'r-Riyâz (Hafâcî; 58 künye) hadis listesinin (c)'sindedir.
