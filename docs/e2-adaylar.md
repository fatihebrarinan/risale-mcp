# E2.1 Aday listesi: belâgat eserleri ve Risale'nin andığı önemli kaynaklar (2026-11-13)

`PLANLAR.md` E2'nin ilk adımı. Bu belge bir **öneridir**: seçim kullanıcınındır (E2.2). Seçilenler
`docs/eserler/klasik.md`'nin (b) bölümüne geçer, kalanlar (c)'ye.

## Ölçüt ve nasıl sayıldı

Bir eser şu üç şarttan en az ikisini tutarsa girer (kullanıcı onayladı, 2026-11-09):

1. **Risale onu ya da müellifini adıyla anıyor**, ya da Risale'deki bir hadisin künyesi o kitabı gösteriyor.
   Sayım genel veritabanından yapıldı (`data/dist/genel/risale.db`; Osmanlıca ciltler hariç, aynı metni ikinci kez
   saymasın diye). Kelime araması `search.py` sorgu diliyle ve her eser için birkaç yazılışla (Türkçe ve Arapça)
   yapıldı; sayılar cümle sayısıdır, bir adın her geçişi değil. Künye sayıları `data/interim/hadis/kunye.md`'den.
   Aşağıdaki tablolarda "anma" sütunu: eserin adı / müellifin adı. Yalnız müellif anılıyorsa eser için şart
   zayıftır ve öyle yazıldı.
2. **Muhakkiki bilinen bir dijital nüsha ve açık lisans.** Bakılan yer OpenITI (KITAB projesi; CC BY-NC-SA 4.0,
   tefsir ve hadis kütüphanesiyle aynı zemin). Sürümler GitHub'dan okundu (2026-11-13; salt okuma, bir şey
   indirilmedi). Muhakkik ve yayınevi sürüm dosyasının başındaki `#META#` satırlarından. "Muhakkik yok" diyen
   sürümde baskının adı var ama muhakkiki yazılmamış: E2.3'te sürümün kendisinde bakılır. Kelime sayısı sürümün
   `LENGTH` alanıdır.
3. **Gerçekçi bir sohbette ona soru gelir:** Risale okuyucusunun, İşârât üzerine çalışanın ya da D serisinin
   (taslakların dil ve belâgat iddiaları) ona başvurması. Bu şart yargıdır, gerekçesiyle yazıldı.

Kapasite: tefsir makinesi 8 GB, ≈1,3 GB kullanılıyor; 13 tefsir ≈24 milyon kelime. Aşağıdaki önerilen ilk dilim
≈570 bin kelime, hepsi birlikte (büyükler hariç) ≈3 milyon.

**Düzeltme (2026-11-13, E2.3):** bu belgenin ilk hâlindeki kelime sayıları yanlıştı: betik sürümün `.yml`'sinden
`LENGTH` yerine `CLENGTH`'i (harf sayısı) okumuştu; sayılar ≈4 kat büyüktü. Aşağıdakiler `LENGTH`'tir (kelime).

## Öneri özeti

| Dilim | Eserler | Neden önce |
|---|---|---|
| **1. Belâgat ve terim** (D2'nin ön şartı) | Delâilü'l-İ'câz, Esrârü'l-Belâğa, Miftâhu'l-Ulûm, et-Ta'rîfât, el-Müfredât | D2 bunlarla yazılır; İşârât'ın adıyla dayandığı nazım nazariyesi; ≈570 bin kelime |
| **2. Risale'nin okuru gönderdiği kelâm ve tasavvuf eserleri** | Şerhu'l-Makāsıd, et-Telvîh, el-Munkız, el-Fıkhu'l-Ekber, İhyâu Ulûmi'd-Dîn | Risale bunlara adıyla havale eder; İhyâ'da 82 künye |
| **3. Siyer ve mu'cizât** | Şerhu'ş-Şifâ, el-Mevâhibü'l-Ledünniyye | On Dokuzuncu Mektub'un ve Şuââtü Ma'rifeti'n-Nebî'nin kaynakları; Şerhu'ş-Şifâ'da 109 künye |
| **Seçmeli** (2 şart, 1. şart yok ya da zayıf) | el-Kitâb (Sîbeveyh), el-Îzâh (Kazvînî), Muhtasarü'l-Meânî (Teftâzânî), el-Kâmûsu'l-Muhît | Belâgat ve dil için değerli; Risale'de eserin adı geçmiyor ya da yalnız müellif geçiyor |
| **Bekleyen** (nüsha ya da boyut) | Şerhu'l-Mevâkıf, Fütûhât-ı Mekkiyye, el-Bidâye ve'n-Nihâye, Fütûhu'l-Gayb, Mektûbât-ı Rabbânî, Nesîmü'r-Riyâz, el-Mîzânü'l-Kübrâ | (c)'ye: sebebi her birinin satırında |

## 1. Belâgat ve terim (önerilen ilk dilim)

| Eser | Müellif (ö.) | Anma | Nüsha (OpenITI) | Kelime | 1 | 2 | 3 |
|---|---|---|---|---:|:-:|:-:|:-:|
| Delâilü'l-İ'câz | Abdülkāhir el-Cürcânî (471) | 1+9 eser / 9+4 müellif | `Shamela0012055`: Mahmûd Muhammed Şâkir, Medenî (Kahire–Cidde) | 122 bin | ✓ | ✓ | ✓ |
| Esrârü'l-Belâğa | Abdülkāhir el-Cürcânî (471) | eser Delâil'le birlikte / müellif aynı | `Shamela0008187`: Medenî (muhakkik satırı boş) | 77 bin | ✓ | ✓ | ✓ |
| Miftâhu'l-Ulûm | Sekkâkî (626) | 2 eser / 12+5 müellif | `Shamela0026581`: Dâru'l-Kütübi'l-İlmiyye (muhakkik yazılmamış) | 134 bin | ✓ | ◐ | ✓ |
| et-Ta'rîfât | Seyyid Şerîf el-Cürcânî (816) | eser adı belirsiz / 4 müellif | `Shamela0007312`: DKİ 1403 ("ضبطه وصححه جماعة من العلماء"); E2.3'te seçildi, Ebyârî'nin `JK000768` sürümünde OCR artıkları var | 49 bin | ◐ | ✓ | ✓ |
| el-Müfredât fî Garîbi'l-Kur'ân | Râgıb el-İsfahânî (502) | yok | `JK001150`: Muhammed Seyyid Kîlânî, Dâru'l-Ma'rife; E2.3'te seçildi, Dâvûdî'nin `Shamela0023636` sürümünde madde başlığı işareti kelimelerin içine girmiş | 186 bin | ✗ | ✓ | ✓ |

Gerekçeler:

- **Delâilü'l-İ'câz ve Esrârü'l-Belâğa.** İşârât'ın nazım nazariyesinin kaynağı: eser i'câzın sırrında "ونحن على
  مذهبه" der (İşârâtü'l-İ'câz (Arapça) › Sûre-i Bakara › 23-24. Âyetlerin Tefsiri › المسألة السابعة, 167. cümle;
  D1.2a). Muhakemat ikisini adıyla anar: Abdülkāhir lafızperestliği tedavi için "Delâil-i İ'câz ve
  Esrâru'l-Belâğat'ın bir sülüsünü" o ilaçlarla doldurmuştur (Muhakemat › İkinci Makale › Birinci Mes'ele, 22.
  cümle). İşârât'ın Arapçası temsilin tesirini anlatırken okuru doğrudan Esrârü'l-Belâğa'ya gönderir ve ondan
  uzun bir alıntı yapar ("فاستمع معي لما يترنّم به صاحبُ «دلائل الإعجاز» في أسرار بلاغته", 17-20. Âyetlerin Tefsiri,
  13. cümle); Kızıl İcaz "كما في دلائل الإعجاز" der (فصل في مباحث الالفاظ, 10. cümle). D1'in taslakları
  nazım nüktelerini tefsirlerden (Keşşâf, Beyzâvî) almak zorunda kaldı; D2'nin sorusu tam olarak budur: asıl kaynak
  verilince belâgat isabeti artıyor mu. Delâil'de Şâkir tahkiki standart baskıdır.
- **Miftâhu'l-Ulûm.** İşârât Sekkâkî'yi belâgat imamları arasında sayar ve "خاتمة مفتاح السكاكي"ye gönderir (23-24 ›
  المسألة السابعة, 61. cümle); Muhakemat "Miftâh-ı Sekkâkî"de beyan olunduğu gibi der (Birinci Makale › Sekizinci
  Mes'ele, 50. cümle). Medrese belâgatının çerçevesi (meânî, beyân, bedî' taksimi) buradan gelir. Nüshada muhakkik
  yazılmamış (◐): E2.3'te sürüm açılıp baskısı doğrulanır (DKİ'nin Na'îm Zerzûr baskısı olması muhtemel; tahmin,
  doğrulanmadı).
- **et-Ta'rîfât.** Terim sözlüğü: İşârât, Kızıl İcaz ve Ta'likat okuyanın her sayfada sorduğu "bu terim ne demek"
  sorusunun cevabı; modelin "Yapay zekâ tercümesi"nde terimleri doğru vermesine de yardım eder. Müellifi Risale'de
  dört kez anılır (Şerhü'l-Mevâkıf'ın şârihi olarak); eser adı Kızıl İcaz'daki "وتعريفات المصطلحات" ibaresinde geçiyor
  olabilir ama genel bir söz de olabilir (◐). Küçük (49 bin kelime).
- **el-Müfredât.** Kur'ân kelimelerinin sözlüğü; taslakların "dil" iddialarını (bir kelimenin aslî mânâsı) bir
  kaynağa bağlamanın en doğrudan yolu; tefsir altyapısının da ortak ihtiyacı. Risale anmaz (1. şart yok); 2 ve 3
  güçlü. Kâmûs'tan önce önerilir: birimi Kur'ân kelimesidir, cümle modeline daha kolay oturur.

## 2. Risale'nin okuru gönderdiği kelâm ve tasavvuf eserleri

| Eser | Müellif (ö.) | Anma | Nüsha (OpenITI) | Kelime | 1 | 2 | 3 |
|---|---|---|---|---:|:-:|:-:|:-:|
| Şerhu'l-Makāsıd | Sa'deddîn et-Teftâzânî (792) | 2 eser / 10+1 müellif | `JK001157`: Dâru'l-Maârifi'n-Nu'mâniyye, Lahor (muhakkik yazılmamış) | 296 bin | ✓ | ◐ | ✓ |
| et-Telvîh ale't-Tavzîh | Teftâzânî (792) | 3 eser ("Mukaddemât-ı İsnâ Aşer" 4) | `JK007110`: Zekeriyyâ Umeyrât, Dâru'l-Kütübi'l-İlmiyye | 232 bin | ✓ | ✓ | ◐ |
| el-Munkız mine'd-Dalâl | Gazâlî (505) | eser yok / 39 müellif | `JK009330`: Muhammed Muhammed Câbir, el-Mektebetü's-Sekâfiyye | 11 bin | ◐ | ✓ | ✓ |
| el-Fıkhu'l-Ekber | Ebû Hanîfe (150) | 1 eser / 39 müellif | `JK001085`: Mektebetü'l-Furkân (muhakkik yazılmamış; şerhinden ayıklanmış metin) | 1.656 | ✓ | ◐ | ✓ |
| İhyâu Ulûmi'd-Dîn | Gazâlî (505) | 82 künye / 39 müellif | `JK000001`: Dâru'l-Ma'rife (muhakkik yazılmamış; `Shamela0009472`'de eksik sayfalar var) | 992 bin | ✓ | ◐ | ✓ |

Gerekçeler:

- **Şerhu'l-Makāsıd.** Risale kelâm meselelerinin tafsilatını ona ve Şerhu'l-Mevâkıf'a havale eder ("Şerhü'l-Mevâkıf
  ve Şerhü'l-Makàsıd gibi muhakkiklerin büyük kitaplarına havale ederek…", Sözler › Otuzüçüncü Söz › Otuzuncu
  Pencere, 5. cümle; Muhakemat › Birinci Makale › Birinci Mes'ele, 2. cümle). İşârât îmânın tarifini "كما فسّره السعد"
  diye Teftâzânî'den verir (3. Âyetin Tefsiri, 23. cümle). Okurun "Risale'nin havale ettiği kitap ne diyor" sorusuna
  cevap. Lahor baskısı eski taş baskısıdır; muhakkik yok (◐).
- **et-Telvîh.** Risale kader ve cüz'-i ihtiyârî meselesinde Teftâzânî'nin "Mukaddemât-ı İsnâ Aşer" adıyla Telvîh'te
  kırk-elli sayfada ancak hallettiğini, Risale'nin aynı meseleyi kolayca açtığını söyler (Mektubat › Yirmisekizinci
  Mektûb › Yedinci Mes'ele › Üçüncü İşâret, 4. cümle; Barla Lâhikası ve Tarihçe'de de). Soru gerçekçi ama dar (bir
  usûl-i fıkıh kitabının bir bölümü): 3. şart ◐. İsterseniz yalnız o bölüm alınır.
- **el-Munkız.** Gazâlî Risale'de çok anılır (Mesnevî-i Nuriye'nin Mukaddimesi onu Mevlânâ ve İmâm-ı Rabbânî ile
  birlikte "kalb, rûh, akıl gözleri açık olarak" yürüyenlerden sayar: Birinci Nokta, 12. cümle), ama eser adı geçmez
  (◐). Gazâlî'nin kendi yolunu anlattığı kısa eser; o karşılaştırmanın öbür ucu.
  Çok küçük (11 bin kelime).
- **el-Fıkhu'l-Ekber.** Sünuhat selefin kitaplarını sayarken "Muvatta, Fıkh-ı Ekber gibi" der (Kur'ân'ın Hâkimiyet-i
  Mutlakası, 28. cümle). Akîde sorularının en kısa klasik metni (1.656 kelime). Nüsha bir şerhten ayıklanmış:
  E2.3'te metnin bütünlüğüne bakılır.
- **İhyâu Ulûmi'd-Dîn.** Risale'deki 82 hadis künyesi ona gidiyor (hadis kitabı sayılmadığı için hadis sunucusunda
  değil; `docs/eserler/klasik.md` (b)'de zaten vardı). Büyük (≈1 milyon kelime): kütüphanedeki büyük
  tefsirlerden biri kadar. Baskının muhakkiki yok (Dâru'l-Ma'rife); hadislerin tahrici (Irâkî) bu baskıda dipnotta
  olabilir, ayrı katman olur.

## 3. Siyer ve mu'cizât

| Eser | Müellif (ö.) | Anma | Nüsha (OpenITI) | Kelime | 1 | 2 | 3 |
|---|---|---|---|---:|:-:|:-:|:-:|
| Şerhu'ş-Şifâ | Aliyyü'l-Kārî (1014) | 109 künye | `Shamela0009918`: Dâru'l-Kütübi'l-İlmiyye (muhakkik yazılmamış) | 609 bin | ✓ | ◐ | ✓ |
| el-Mevâhibü'l-Ledünniyye | Kastalânî (923) | 1 eser / 1 müellif / 4 künye | `Shamela0023685`: el-Mektebetü't-Tevfîkıyye, Kahire (muhakkik yazılmamış) | 441 bin | ✓ | ◐ | ◐ |

- **Şerhu'ş-Şifâ.** Künyelerde hadis kitaplarından sonra en çok gösterilen eser (109). eş-Şifâ hadis sunucusunda
  zaten var; şerhi onun yanında, Zehebî'nin notları gibi ayrı katman olarak daha doğal durur. **Karar sizin:** hadis
  sunucusuna mı (öneri: oraya, eş-Şifâ'nın şerhi olarak), klasik eserler sunucusuna mı.
- **el-Mevâhib.** Şuââtü Ma'rifeti'n-Nebî "Kàdî İyâz Şifâ-i Şerîf'inde, Kastalânî Mevâhib-i Ledünniye'de mu'cizâtı
  güzel tafsil etmişlerdir" der (Mukaddime, 22. cümle). Mu'cizât soruları için; büyük.

## Seçmeli: iki şartı tutan, Risale'de eser adı geçmeyenler

| Eser | Müellif (ö.) | Anma | Nüsha | Kelime | Gerekçe |
|---|---|---|---|---:|---|
| el-Kitâb | Sîbeveyh (180) | müellif 2 (İşârât Arapça) | `JK006989`: Abdüsselâm Hârûn, Dâru'l-Cîl (Hâncî baskısı da var) | 278 bin | İşârât harflerin mânâsında ona dayanır (17-20 › المسألة الثامنة, 1. cümle; 21-22 › مقدمة, 253. cümle). Taslakların i'râb iddiaları için; çok teknik |
| el-Îzâh fî Ulûmi'l-Belâğa | Hatîb el-Kazvînî (739) | yok | `JK001001`: Behîc Gazzâvî, Dâru İhyâi'l-Ulûm | 73 bin | Miftâh'ın üçüncü kısmının şerhi ve medrese belâgatının ölçünlü terimleri; Telhîs'in iyi nüshası yok (biri OCR, biri eksik) |
| Muhtasarü'l-Meânî | Teftâzânî (792) | müellif 10; Kızıl İcaz'daki "المختصر … المطول" Teftâzânî'nin iki kitabını anıyor olabilir (tahmin) | `ShamAY0033799`: Dâru'l-Fikr, Kum 1411 (muhakkik yazılmamış) | 83 bin | Medresede okutulan belâgat kitabı; Îzâh ile ikisinden biri yeter |
| el-Kâmûsu'l-Muhît | Fîrûzâbâdî (817) | Tarihçe: Kâmûs'u "Bâbü's-Sîn'e kadar" ezberledi; Kızıl İcaz "كما في القاموس" | `JK001437`: Müessesetü'r-Risâle (muhakkik yazılmamış) | 569 bin | Lügat; ama birimi madde, cümle değil: ayrı bir model ister (Kur'ân ve hadis gibi). Müfredât önce |

## Bekleyen: (c)'ye önerilenler

| Eser | Neden bekliyor |
|---|---|
| Şerhu'l-Mevâkıf (Seyyid Şerîf) | Risale adıyla anar ve ondan alıntı yapar (Sözler › Otuzikinci Söz › İkinci Mevkıf › Üçüncü Maksad › … › İkinci Remiz, 1. cümle). Ama OpenITI'de yalnız bir OCR sürümü var (Kraken, baskısı yazılmamış, 891 bin kelime). Îcî'nin el-Mevâkıf'ı (`JK001335`, Abdurrahman Umeyre, Dâru'l-Cîl, 461 bin kelime) şerhle birlikte basılmış olabilir: E2.3'te bakılırsa birinci dilime girebilir |
| el-Fütûhâtü'l-Mekkiyye (İbn Arabî) | Risale adıyla anar (3) ve müellifini çok anar (55). 1,83 milyon kelime, muhakkiki yok. Boyutu yüzünden sonra |
| el-Bidâye ve'n-Nihâye (İbn Kesîr) | 48 künye; Türkî tahkiki var (`Shamela0004445`, Hecr). 2,19 milyon kelime: bütün klasik eserlerin toplamından büyük. Yalnız siyer kısmı (`Shamela0000930`, 559 bin) bir seçenek |
| Fütûhu'l-Gayb (Abdülkādir-i Geylânî) | Risale adıyla 12 kez anar (tefe'ül hikâyesi, Mektubat › Yirmisekizinci Mektûb › Üçüncü Mes'ele › Üçüncü Nokta, 5. cümle). OpenITI'de yok; izinli başka nüsha aranır |
| Mektûbât (İmâm-ı Rabbânî) | Risale çok anar (Tarihçe'deki tefe'ül; İmâm-ı Rabbânî 56). Aslı Farsça; OpenITI'de yok, Arapça tercümesi de yok |
| Mesnevî (Mevlânâ) | Farsça; Risale çok anar (Mevlânâ 53). Kapsam dışı (dil) |
| Nesîmü'r-Riyâz (Hafâcî) | 58 künye; OpenITI'de yok |
| el-Mîzânü'l-Kübrâ (Şa'rânî) | Sözler "Mîzan-ı Şa'rânî" der (Yirmiyedinci Söz › Hâtime, 42. cümle), 4 künye; OpenITI'de yok |
| el-Beyân ve't-Tebyîn (Câhız) | İşârât Câhız'ı i'câzın üçüncü yolunda anar, ama o görüşü bu eserde değil; nüshanın muhakkiki yok. Gerekirse Câhız'ın i'câz risaleleri (`HujajNubuwwa`) bakılır |
| er-Risâletü'l-Kuşeyriyye | Risale anmaz; 2 ve 3 tutar ama öncelik yok |
| Lisânü'l-Arab | Anılmaz; 3 milyon kelime |
| Süllem (Ahdarî), Burhân (Gelenbevî) | Kızıl İcaz ve Ta'likat'ın metinleri; Süllem'in beyitleri Kızıl İcaz'da, Burhân'ın metni Ta'likat'ın Arapçasında aralara serpilmiş. OpenITI'de yoklar. Ayrı eser olarak gerekmez |

Hadis sunucusuna ait olanlar (E2'nin dışında, HA sırasına): et-Terğîb ve't-Terhîb (33 künye), el-Metâlibü'l-Âliye
(31), Mu'cemü'l-Kebîr ve Evsat (19, 22), es-Sünenü'l-Kübrâ (16), Şerhu's-Sünne (15), Hilyetü'l-Evliyâ (15),
el-İsâbe (15).

## Sizden istenen (E2.2)

1. Birinci dilim (beş belâgat ve terim eseri) uygun mu? D2 bunlarla yazılacak.
2. İkinci ve üçüncü dilimden hangileri, hangi sırayla?
3. Şerhu'ş-Şifâ hadis sunucusuna mı, klasik eserler sunucusuna mı?
4. Seçmelilerden (Sîbeveyh, Îzâh ya da Muhtasar, Kâmûs) girecek olan var mı?

Seçimden sonra E2.3: her eser için sürüm açılıp baskısı ve başlık yapısı doğrulanır (muhakkik yazılmamış olanlarda
önce bu), sonra ayrıştırma.
