# Klasik eserler: kontrol listesi

> (a) `uv run python -m risale_mcp.checklist` ile üretilir, elle düzenlemeyin; (b) ve (c) elle tutulur, yeniden üretimde korunur.
> Eserlerin listesi ve kaynakları: `src/risale_mcp/catalog/`.
> Eser ekleme ölçütü ve sıra: `PLANLAR.md` E2.

## (a) Eklenenler

- **Ham veri:** 11/11 eser indirildi.
- **Ayrıştırma:** 11/11 eser.
- **Kaynağı bulunamayan:** yok.

İşaretler: ✅ tamam · ⚠️ kısmen · ⬜ yapılmadı · ❌ kaynak yok · ⏸️ ertelendi

### Belâgat ve terim (1. dilim)

| # | Eser | Kaynak | Ham veri | Ayrıştırma | Not |
|---:|---|---|---|---|---|
| 1 | el-Fıkhu'l-Ekber | `openiti/fikhul-ekber` | ✅ indirildi | ✅ 27 düğüm, 39 paragraf, 39 cümle | OpenITI Shamela0006388 (Furkân 1419; Aliyyü'l-Kārî'nin şerhinden ayıklanmış metin, başlıklar yayıncının). |
| 2 | Delâilü'l-İ'câz | `openiti/delailul-icaz` | ✅ indirildi | ✅ 760 düğüm, 3023 paragraf, 4507 cümle | OpenITI Shamela0012055 (Medenî, 3. baskı 1413). Muhakkikin fıkra numaraları düğümdür. |
| 3 | Esrârü'l-Belâğa | `openiti/esrarul-belaga` | ✅ indirildi | ✅ 36 düğüm, 1257 paragraf, 1635 cümle | OpenITI Shamela0008187 (Medenî; muhakkik satırı boş). Sürümün sonunda son paragrafın devamı eksik. |
| 4 | el-Müfredât fî Garîbi'l-Kur'ân | `openiti/mufredat` | ✅ indirildi | ✅ 1630 düğüm, 2392 paragraf, 4494 cümle | OpenITI JK001150 (Kîlânî, Dâru'l-Ma'rife). Harf kitabı ve madde (kök) düğümdür. Dâvûdî baskısının Shamela sürümünde madde başlığı işareti kelimelerin içine girmiş, metin kurulamıyor. |
| 5 | el-Munkız mine'd-Dalâl | `openiti/munkiz` | ✅ indirildi | ✅ 1 düğüm, 31 paragraf, 327 cümle | OpenITI ShamAY0033739 (Câbir, el-Mektebetü's-Sekâfiyye). Sürümde başlık yok: eser tek bölümdür. |
| 6 | Miftâhu'l-Ulûm | `openiti/miftahul-ulum` | ✅ indirildi | ✅ 130 düğüm, 1386 paragraf, 2237 cümle | OpenITI Shamela0026581 (Dâru'l-Kütübi'l-İlmiyye, 2. baskı 1407; muhakkik yazılmamış). |
| 7 | et-Telvîh ilâ Keşfi Hakāiki't-Tenkîh | `openiti/telvih` | ✅ indirildi | ✅ 199 düğüm, 2028 paragraf, 2028 cümle | OpenITI JK007110 (Umeyrât, Dâru'l-Kütübi'l-İlmiyye 1416): yalnız Teftâzânî'nin şerhi; Sadrüşşerîa'nın Tavzîh'i yok, "قوله" ile anılır. Başlıklar aynı baskının ShamAY0034200 sürümünün içindekilerinden. |
| 8 | Şerhu'l-Makāsıd | `openiti/serhul-makasid` | ✅ indirildi | ✅ 126 düğüm, 1177 paragraf, 1183 cümle | OpenITI JK001157 (Nu'mâniyye, Lahor 1401; muhakkik yazılmamış). Başlık satırı yok: bölümler Teftâzânî'nin kendi metnini "قال" ile aktardığı yerlerden. |
| 9 | et-Ta'rîfât | `openiti/tarifat` | ✅ indirildi | ✅ 30 düğüm, 2088 paragraf, 2275 cümle | OpenITI Shamela0007312 (Dâru'l-Kütübi'l-İlmiyye, 1403; "ضبطه وصححه جماعة من العلماء بإشراف الناشر"). |
| 10 | Şerhu'l-Mevâkıf | `openiti/serhul-mevakif` | ✅ indirildi | ✅ 705 düğüm, 14291 paragraf, 14344 cümle | OpenITI ShamAY0033881 (Umeyre, Dâru'l-Cîl 1417; OpenITI'de Îcî'nin adı altında "المواقف"). Îcî'nin metni baskının "المتن" diye ayırdığı yerde ayrı katmandır. Başlıklar Şâmile'nin içindekilerinden. |
| 11 | el-Mevâhibü'l-Ledünniyye | `openiti/mevahib` | ✅ indirildi | ✅ 354 düğüm, 11630 paragraf, 20096 cümle | OpenITI Shamela0023685 (Tevfîkıyye, Kahire; muhakkik yazılmamış). |

Kaynak alınmaz (`catalog/excluded.py`, kullanıcının kararı): Muhammed Abduh: kaynak alınmaz; Tefsîru'l-Menâr: Abduh'un derslerine dayanır, kaynak alınmaz.

<!-- Bu satırın altı elle tutulur; checklist yeniden üretirken korur. -->

Şartlar (PLANLAR.md E2): **1** Risale'de anılma ya da künye, **2** muhakkiki bilinen nüsha ve açık izin, **3** gerçekçi soru. "?" henüz sayılmadı (E2.1). Künye sayıları `data/interim/hadis/kunye.md`'den, boyutlar `docs/mvp-kitaplar.md`'den (2026-11-06).

## (b) Eklenmesi çok iyi olacaklar

E2.1'in aday listesinden (`docs/e2-adaylar.md`, 2026-11-13); seçim kullanıcının (E2.2, 2026-11-13). Sıra: 1. dilim şimdi
(E2.3), 2. dilim sonra, 3. dilim ondan sonra (E5). E5'in turu (2026-11-24): 2. dilim ve el-Mevâhib; İhyâ son alt adım (E5.4). Nüsha sütunu öneridir; muhakkiki yazılmamış olanlarda E2.3'te
sürümün kendisinde bakılır. "Anma": Risale'de eserin adı / müellifin adı (cümle sayısı).

**1. dilim: belâgat ve terim** eklendi (E2.3, 2026-11-13): yukarıda (a). Sürüm değişiklikleri ham verinin
incelemesinden: Ta'rîfât'ta Shamela sürümü (Ebyârî'nin JK sürümünde OCR artıkları var), Müfredât'ta Kîlânî'nin JK
sürümü (Dâvûdî'nin Shamela sürümünde madde başlığı işareti kelimelerin içine girmiş). Kurallar `books/klasik_openiti.py`.

**2. dilim: Risale'nin havale ettiği ve dayandığı kelâm ve tasavvuf eserleri (E5)**

"Risale'deki yeri" sütunu `docs/e5-risalede-anilan-eserler.md`'den (2026-11-24): müellifin sözünde havale (H), nakil (N),
değerlendirme (D), anma (A), cümle sayısıyla. Bu sütun `risale_refs`'in kaynağıdır. Şerhu'l-Mevâkıf (c)'den buraya alındı
(kullanıcının kararı, 2026-11-24).

| Eser | Müellif (ö.) | Nüsha (OpenITI) | Kelime | Risale'deki yeri | 1 | 2 | 3 | Gerekçe |
|---|---|---|---:|---|:-:|:-:|:-:|---|
| Şerhu'l-Mevâkıf | Seyyid Şerîf Cürcânî (816; metin Îcî, 756) | `0756CadudDinIji.Mawaqif.JK001335`: Abdurrahman Umeyre, Dâru'l-Cîl 1997 (adı "el-Mevâkıf", içi şerh; metin `# المتن #` ile ayrılır) | 460 bin | H2 (Sözler › Otuzüçüncü Söz › Otuzuncu Pencere; Muhakemat › Birinci Makale › Birinci Mes'ele), N2 (Sözler › Otuzikinci Söz, muhabbetin sebebi) | ✓ | ✓ | ✓ | Risale'nin adıyla en açık havale ettiği iki kitaptan biri |
| Şerhu'l-Makāsıd | Teftâzânî (792) | `0792IbnCumarTaftazani.SharhMaqasid.JK001157`: Nu'mâniyye, Lahor 1981 (muhakkik yazılmamış) | 296 bin | H2 (aynı iki yer), N1 (Barla Lâhikası, rûhun mahlûkiyeti); Teftâzânî'den eser adı anılmadan N8 | ✓ | ◐ | ✓ | Öbür havale edilen kitap |
| et-Telvîh | Teftâzânî (792) | `0792IbnCumarTaftazani.TalwihCalaTawdih.JK007110`: Zekeriyyâ Umeyrât, DKİ 1996 | 232 bin | D3 (Mektubat › Yirmisekizinci Mektûb › Yedinci Mes'ele, kopyaları Barla ve Tarihçe'de): kader meselesinde karşılaştırma, havale değil | ✓ | ✓ | ◐ | Mukaddemât-ı İsnâ Aşer'in yeri |
| el-Munkız mine'd-Dalâl | Gazâlî (505) | `0505Ghazali.Munqidh.JK009330`: Muhammed M. Câbir | 11 bin | Eser anılmaz; Gazâlî eser adı anılmadan N5, D3, A3 | ✗ | ✓ | ✓ | Gazâlî'nin kendi yolunu anlattığı kısa eser |
| el-Fıkhu'l-Ekber | Ebû Hanîfe (150) | `0150AbuHanifa.FiqhAkbar.JK001085`: Furkân (şerhten ayıklanmış) | 1.656 | D1 (Sünuhat, selefin kitabı) | ✓ | ◐ | ✓ | Akîdenin en kısa klasik metni |
| İhyâu Ulûmi'd-Dîn | Gazâlî (505) | `0505Ghazali.IhyaCulumDin.JK000001`: Dâru'l-Ma'rife (muhakkik yazılmamış) | 992 bin | Müellifin sözünde adıyla yok (bir talebe mektubunda N1); nâşirin 82 hadis künyesi | ✓ | ◐ | ✓ | Risale'deki hadislerin nâşir künyeleri ona gider |
| el-Mevâhibü'l-Ledünniyye | Kastalânî (923) | `0923AhmadQastallani.MawahibLaduniyya.Shamela0023685`: Tevfîkıyye (muhakkik yazılmamış) | 441 bin | H1 (Şuââtü Ma'rifeti'n-Nebî › Mukaddime: mu'cizâtın tafsili, Şifâ ile birlikte); 4 künye | ✓ | ◐ | ◐ | 3. dilimden bu tura alındı (kullanıcının kararı, 2026-11-24) |

**3. dilim: siyer ve mu'cizât** el-Mevâhib 2026-11-24'te 2. dilimle birlikte E5'e alındı.

3. dilimin öbür eseri Şerhu'ş-Şifâ hadis sunucusuna girer (kullanıcının kararı, 2026-11-13): `docs/eserler/hadis.md` (b).

## (c) Aklımızda bulunsun

Kullanıcının kararı (2026-11-13): seçmeliler ve bekleyenler burada durur; yer ve zaman müsait olunca E5'te eklenmeye
çalışılır. Fütûhu'l-Gayb, Mesnevî ve Mektûbât "çok çok kıymetli" (kullanıcı): nüsha ve izin yolu açılınca öncelikli.

| Eser | Neden beklediği |
|---|---|
| Fütûhu'l-Gayb (Abdülkādir-i Geylânî, 561) | Risale adıyla 12 kez anar (tefe'ül hikâyesi). OpenITI'de yok; izinli başka nüsha aranır |
| Mektûbât (İmâm-ı Rabbânî, 1034) | Risale çok anar (Tarihçe'deki tefe'ül; müellif 56). Aslı Farsça; OpenITI'de yok, Arapça tercümesi de yok |
| Mesnevî (Mevlânâ, 672) | Risale çok anar (Mevlânâ 53). Farsça; nüsha ve izin aranır |
| er-Risâletü'l-Hamîdiyye (Hüseyin el-Cisr, 1327) | Şuââtü Ma'rifeti'n-Nebî beşâretlerin yüz delili için ona havale eder, 10 nakil daha (`docs/e5-risalede-anilan-eserler.md`). OpenITI'de yok (2026-11-24); izinli nüsha aranır |
| el-Fütûhâtü'l-Mekkiyye (İbn Arabî, 638) | Adıyla 3, müellif 55. 1,83 milyon kelime, muhakkiki yok |
| el-Bidâye ve'n-Nihâye (İbn Kesîr, 774) | 48 künye; Türkî tahkiki var (`Shamela0004445`). 2,19 milyon kelime; yalnız siyer kısmı (`Shamela0000930`, 559 bin) bir seçenek |
| el-Mîzânü'l-Kübrâ (Şa'rânî, 973) | Sözler › Yirmiyedinci Söz › Hâtime mezheplerin mizanı için ona havale eder; 4 künye; OpenITI'de yok |
| el-Kitâb (Sîbeveyh, 180) | Seçmeli: İşârât harflerin mânâsında ona dayanır; Abdüsselâm Hârûn tahkiki var (`JK006989`), 278 bin. Çok teknik |
| el-Îzâh (Hatîb el-Kazvînî, 739) ya da Muhtasarü'l-Meânî (Teftâzânî) | Seçmeli: medrese belâgatının ölçünlü terimleri; Risale adlarını anmaz. İkisinden biri yeter (`JK001001` Gazzâvî; `ShamAY0033799`) |
| el-Kâmûsu'l-Muhît (Fîrûzâbâdî, 817) | Seçmeli: Tarihçe'de ezber hikâyesi, Kızıl İcaz anar. Birimi madde: ayrı bir model ister |
| el-Beyân ve't-Tebyîn (Câhız, 255) | İşârât Câhız'ı i'câzın üçüncü yolunda anar, ama o görüş bu eserde değil; muhakkiki yok |
| er-Risâletü'l-Kuşeyriyye, Lisânü'l-Arab | Risale anmaz; öncelik yok (Lisân 3 milyon kelime) |
| "Bediüzzaman'ın ezberlediği 90 kitap" | Bir liste değil, bir rivayet; çoğu medrese ders kitabıdır ve 3. şartı tutmaz. Ad ad bilinenler E2.1'de sınandı |
| Süllem (Ahdarî), Burhân (Gelenbevî) | Kızıl İcaz ve Ta'likat'ın metinleri; Süllem'in beyitleri Kızıl İcaz'da, Burhân'ınki Ta'likat'ın Arapçasında aralara serpilmiş. OpenITI'de yoklar |

Nesîmü'r-Riyâz (Hafâcî; 58 künye) hadis listesinin (c)'sindedir.
