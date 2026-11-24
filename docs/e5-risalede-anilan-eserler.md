# Risale-i Nur'da adı geçen eserler (E5 ön çalışması, 2026-11-24)

Kullanıcının sorusu: Risale-i Nur'da adı geçen öbür eserlerin genel listesi; hangilerine bir konuyu **havale**
ediyor, hangilerine **başvuruyor**, hangilerini **yalnız anıyor**. Bu belge E5'in (kalan klasik eserler ve
eklentinin yeni tanıtımı) girdisidir; seçim kullanıcınındır.

## Nasıl yapıldı

1. **Derlem:** genel veritabanı (`data/dist/genel/risale.db`), külliyatın 54 eseri, ≈131 bin cümle; Osmanlıca
   ciltler dışarıda (aynı metni ikinci kez saymasın diye). Arapça asılla Türkçe tercümesi, Fihrist özetleri,
   Tarihçe'nin Lâhika'dan aldığı mektuplar ve Nur'un İlk Kapısı'nın İşârât'tan aldığı ek **ayrı sayıldı**: sayılar
   cümledir, "yer" değildir.
2. **Bilinen adlar:** ≈110 eser ve müellif adı, Türkçe ve Arapça yazılışlarıyla, normalize metinde arandı
   (`normalize.search_words`). Gürültülü kalıplar ("râzı", "makāsıd", "keşşâf", "telvih", "iktidar" içindeki
   "Dârimî") ham metinde ikinci bir denetimden geçirildi.
3. **Listede olmayanlar:** "kitab, eser, tefsir, şerh, hâşiye, müellif, كتاب, شرح…" geçen ve ilk adımda
   yakalanmayan 2.305 cümle dört okuyucuya (model) bölünüp baştan sona okundu; Bediüzzaman'ın kendi eserleri ve
   genel sözler ("kütüb-ü semâviye", "kitab-ı kâinat") ayıklandı.
4. **Türü:** her aday cümle (önceki ve sonraki cümleyle) okunup beş türden birine konuldu ve **kimin sözü olduğu**
   işaretlendi:
   - **havale:** okuru bir konunun tafsili ya da delili için o esere gönderir ("…'a git", "tafsilâtını … havale
     ederek", "كما في");
   - **nakil (başvuru):** o eserden ya da müelliften söz, rivayet, görüş, sayı aktarır;
   - **değerlendirme:** eseri ya da yolunu tartar, över, tenkit eder, Risale'yle karşılaştırır;
   - **tefe'ül:** kitap açılıp işaret aranır;
   - **anma:** okundu, ezberlendi, listede, hikâyede.
   Konuşan: müellif, talebe ya da derleyen (Lâhika mektupları, Tarihçe'nin anlatısı, Fihrist), başka (mahkeme,
   nâşir notu, "Ecnebî feylesoflar" ekindeki yazarlar), belirsiz.
5. **Kişi olarak anma** (Gavs-ı Âzam'ın ihbarı, "Muhyiddin-i Arabî gibi" diye bir velînin anılması) eser anması
   sayılmadı; Ek C'de yalnız sayısı var.

**Güvenilirlik.** Okuma ve türleme modelindir, elle denetlenmedi. 25 kayıtlık rastgele örneklemde 22'si açıkça
doğru; en zayıf sınır "nakil"le "anma" arası (aynı "Tevrat, İncil, Zebûr ve Suhuflarında beşâret vermişler"
cümlesi bir kitapta nakil, öbüründe anma sayılmış) ve "havale"yle "nakil" arası (Ercûze'yi sayfasıyla gösteren
cümle). Kalıp araması bir yazılışı kaçırabilir: Muhakemat'taki "“Makàsıd” ve “Mevâkıf”a git" ve İşârât'taki
"كما فسّره السعد" böyle kaçmıştı, elle eklendi. Hadis künyeleri (âyet ve hadis parçalarının nâşir kaynakları,
`data/interim/hadis/kunye.md`) **sayılmadı**: onlar müellifin değil nâşirin sözüdür (İhyâ'nın 82 künyesi gibi).

## Sonuç

**Genel tablo.** 102 eser ya da eser kümesi, 792 cümle. Bunların ≈%80'i müellifin kendi sözünde. Ağırlık
türlere göre: nakil %56, anma %23, değerlendirme %16, tefe'ül %2, **havale yalnız %3 (24 cümle, 14 eser)**.
Risale başka kitaplara az gönderir; çok şeyi aktarır, kendi yolunu çoğu yerde onlardan ayırarak anlatır.

### 1. Havale ettikleri (okuru gönderdiği eserler)

| Eser | Nereden, ne için | Kütüphanede |
|---|---|---|
| **Şerhu'l-Mevâkıf** ve **Şerhu'l-Makāsıd** | Sözler › Otuz Üçüncü Söz › Otuzuncu Pencere (kelâm delillerinin tafsili); Muhakemat › Birinci Makale › Birinci Mes'ele ("şübhen varsa Makàsıd ve Mevâkıf'a git") | Makāsıd 2. dilimde; Mevâkıf (c)'de (yalnız OCR nüsha) |
| **Fahreddîn-i Râzî'nin tefsiri** | Muhakemat › Birinci Mes'ele (arzın küreviyeti); İşârât › 25. âyet (haşrin delilleri) | Tefsir eklentisinde |
| **Delâilü'l-İ'câz**, **Esrârü'l-Belâğa** | İşârât (Arapça) › 17-20. âyetler, 10. mes'ele (müzeyyen üslûbun örneği); Muhakemat › Sekizinci Mes'ele (Delâil'in "221. kapısı") | Klasik eklentide |
| **Miftâhu'l-Ulûm** | İşârât (Arapça) › 23-24. âyetler, 7. mes'ele (nahvî itirazların cevabı için "hâtimesi") | Klasik eklentide |
| **eş-Şifâ** ve **el-Mevâhibü'l-Ledünniyye** | Şuââtü Ma'rifeti'n-Nebî › Mukaddime (mu'cizâtın tafsili); Mektubat › On Dokuzuncu Mektub › On Yedinci İşâret (ahlâk mu'cizesi) | Şifâ hadis eklentisinde; Mevâhib 3. dilimde |
| **er-Risâletü'l-Hamîdiyye** (Hüseyin el-Cisr) | Şuââtü Ma'rifeti'n-Nebî › 1 (beşâretlere dair yüz delil); 10 nakil daha (beşâretler) | **Listelerde yok**; OpenITI'de de yok |
| **el-Fütûhâtü'l-Mekkiyye** | İşârât › 3. âyet (namazın rükünlerinin esrarı), iki dilde | (c)'de (1,8 milyon kelime) |
| **el-Mîzânü'l-Kübrâ** (Şa'rânî) | Sözler › Yirmi Yedinci Söz › Hâtime (mezheplerin mizanı) | (c)'de; OpenITI'de yok |
| **Mecmûatü'l-Ahzâb** | Sikke › On Sekizinci Lem'a (Ercûze'nin cildi ve sayfası) | Dua mecmuası; kapsam dışı |
| **Sebîlürreşâd** | Emirdağ Lâhikası ve Tarihçe (müellifin o dergideki kendi makalesine) | Kendi yazısı |

### 2. Başvurdukları (nakil)

- **Hadis kitapları** (Buhârî 32, Müslim 19, Beyhakî 14, Tirmizî 8, Kütüb-i Sitte, Müsned, Nesâî, Ebû Dâvûd,
  Taberânî, Ebû Nuaym'ın Delâil'i…): neredeyse hepsi **Mektubat › On Dokuzuncu Mektub**'da ("başta Buhârî ve Müslim
  haber veriyorlar ki"). Bunlar müellifin kendi künyeleridir; nâşir künyelerinden ayrıdır. Hadis eklentisinde
  var.
- **Önceki kitaplar:** İncil 59, Tevrat 52, Suhuf 43, Zebur 22; ayrıca adıyla Eş'ıyâ (İşaya) ve Mîhâ (Mika)
  kitapları: beşâretler, On Dokuzuncu Mektub › On Altıncı İşâret ve Şuââtü Ma'rifeti'n-Nebî.
- **Tefsir:** Keşşâf ve Zemahşerî 19 (çoğu İşârât'ta, görüşü aktarılır ya da tartılır), Tenvîrü'l-Mikbâs 10
  (Rumuzat-ı Semaniye ve Lâhika'da sûrelerin kelime ve harf sayıları), Râzî 8, Taberî 4.
- **Belâgat:** Sekkâkî ve Miftâh 16 (İşârât), Abdülkāhir'in iki kitabı 9, Sîbeveyh 2, Câhız 1.
- **Kelâm:** Teftâzânî 8 (îmânın tarifi, mu'cizât üzerine görüşü; eser adı çoğu yerde yok), Şerhu'l-Makāsıd
  (Barla Lâhikası, rûhun mahlûkiyeti), Şerhu'l-Mevâkıf (Otuz İkinci Söz, muhabbetin sebebi).
- **Tasavvuf:** İmâm-ı Rabbânî 26 (sözleri; Mektûbât adıyla 6), İbn Arabî 16 + Râzî'ye mektubu 4, Geylânî 18,
  Gazâlî 11, Mevlânâ 9.
- **Dua ve vird:** Cevşen 54 (her türden), Ercûze 17 (Sikke'de Risale'ye işâretleri), Kasîdetü'l-Bürde 3.
- **Batılılar:** Carlyle 25, Bismarck 20 (Kur'ân'ı tasdik eden sözleri; çoğu İşârât'ın "Ecnebî feylesoflar" eki
  ve Hutbe-i Şâmiye), Gibbon 2.
- **Ahlâk:** Mâverdî'nin Edebü'd-Dünyâ ve'd-Dîn'i 2 (Zühre ve On Yedinci Lem'a: şeytanla Hz. İsâ kıssası).

### 3. Değerlendirdikleri

- **et-Telvîh:** Mektubat › Yirmi Sekizinci Mektub › Yedinci Mes'ele (ve iki kopyası): Teftâzânî'nin kader
  meselesini "Mukaddemât-ı İsnâ Aşer"de kırk-elli sahifede ancak hallettiği, Risale'nin kolayca açtığı.
  **Havale değil, karşılaştırma.**
- **Mesnevî** (Mevlânâ) 8, çoğu talebe mektuplarında Risale'yle karşılaştırma; **Muallakât** 11, Kur'ân'ın
  belâgati karşısında; **İbn Arabî** 11, vahdet-i vücûd meselesinde; **Dozy** 8 ve **İbn Teymiyye ile
  İbnü'l-Kayyim** 4, menfi değerlendirme; **Cevşen** 13, övgü.

### 4. Tefe'ül ettikleri

Fütûhu'l-Gayb 9 (Mektubat › Yirmi Sekizinci Mektub › Üçüncü Mes'ele ve kopyaları), İmâm-ı Rabbânî'nin
Mektûbât'ı 4, Ümmî Sinan Dîvânı, İbnü'l-Fârıd'ın Dîvânı, Sa'dî (birer).

### 5. Yalnız andıkları

Tarihçe'nin anlattığı medrese kitapları (Mirkât, Molla Câmî, Süyûtî'nin nahiv şerhi, Şerh-i Şemsiyye,
Cem'u'l-Cevâmi', Metâli', Makāmât, Kâmus'un ezberi), virdler (Delâilü'l-Hayrât, Evrâd-ı Bahâiye), dergiler
(Sebîlürreşâd, es-Sıddîk, Students' Voice).

### E5 için ne demek

1. **"Risale'nin havale ettiği klasikler" sözü 1. dilim için doğru**, 2. dilim için yalnız kısmen.
   - **1. dilim:** Delâil, Esrâr ve Miftâh adıyla havale edilir. Müfredât ve Ta'rîfât edilmez (müellifi yalnız
     Seyyid Şerîf olarak anılır).
   - **2. dilim:**
     - Şerhu'l-Makāsıd adıyla havale edilir (2 yer).
     - Telvîh yalnız karşılaştırılır.
     - el-Fıkhu'l-Ekber bir kez anılır.
     - İhyâ müellifin sözünde adıyla hiç geçmez (bir talebe mektubu; 82 künye nâşirin).
     - el-Munkız hiç anılmaz.
   - **Öneri:** Tanıtım iki parçalı olsun: "Risale'nin havale ettiği ve dayandığı klasikler". Her eserin Risale'deki
     yeri **türüyle** verilsin: havale, nakil, değerlendirme.
2. **Şerhu'l-Mevâkıf (c)'den öne alınmaya değer.** Risale'nin adıyla en açık havale ettiği iki kitaptan biri o
   (Otuz Üçüncü Söz ve Muhakemat); öbürü Makāsıd. Engel nüshası: OpenITI'de yalnız OCR sürümü var. Îcî'nin
   el-Mevâkıf'ının Umeyre baskısı şerhle basılmış olabilir; E2'de "bakılacak" diye kalmıştı.
3. **Yeni aday: er-Risâletü'l-Hamîdiyye** (Hüseyin el-Cisr, ö. 1327). Bir havale ve on nakil var, hepsi
   beşâretlerde. OpenITI'de yok (1350AH deposuna bakıldı, 2026-11-24). Başka izinli nüsha aranırsa (c)'ye
   yazılabilir.
4. **Tefe'ül ve anmalar** eser seçiminde ağırlık taşımaz. Fütûhu'l-Gayb'ın kıymeti bu yüzden değişmez: kullanıcının
   kararıyla "çok çok kıymetli".

### Yan bulgu: muhakkikin eki müellifin metninde (veri hatası)

`el-mesnevi-el-arabi/nur/tetimme`'nin 64–128. cümleleri Bediüzzaman'ın değil, risaleoku baskısının ekidir:
- resim etiketleri (`img alt="image" src=…`);
- yazma nüshaların resim altları;
- "نبذة عن بعض الأعلام" başlıklı biyografi sözlüğü (Ziriklî'nin el-A'lâm'ından, Şâfiî, Şa'rânî, İbn Arabî,
  Şâh-ı Nakşibend…).

Şu an araçlarda müellifin metni gibi dönüyor ve cümle olarak aranıyor. `isaratul-icaz-arabi`'de de bir `img alt`
satırı var. Düzeltme ayrıştırıcıdadır (`books/risaleoku_app.py` ya da Mesnevî'nin şablonu): ek ya atılır ya da
`notes`'a geçer. Kimlik değişikliği olur (manifesto durdurur, `--accept-id-changes`). Öneri: yeni bir B işi.

## Ek C. Kişi olarak anılanlar (eser anması sayılmadı)

Geylânî 175 (Gavs-ı Âzam'ın ihbarları dahil: kaside adıyla anılmıyorsa), Mevlânâ 52 (bir kısmı Mevlânâ Câmî ve
Mevlânâ Hâlid), İmâm-ı Rabbânî 51, İbn Arabî 45, Gazâlî 44, İbn Sînâ 20, Eflâtun ve Aristo 20, Abdülkāhir 14,
Fârâbî 8, Teftâzânî 7, Ahmed b. Hanbel 6, Râzî 5, Süyûtî 5, Câhız 5. Bu sayılar mekanik süzgeçten (alıntı fiili
yoksa kişi) ve okuyucuların "kişi" kararlarından gelir; kaba bir ölçüdür.

Ham çalışma dosyaları (aday listeleri, okuyucuların JSON kayıtları) yalnız bu oturumun geçici klasöründeydi.
Ek B her kaydın kimliğini taşır; gerekirse yeniden üretilebilir.

## Ek A. Eser başına sayılar

Sayılar cümledir (bir cümle birden çok eseri anabilir; kopyalar ayrı sayılır). H havale, N nakil, D değerlendirme, T tefe'ül, A anma; konuşan M müellif, T talebe ya da derleyen, B başka (mahkeme, nâşir, ecnebî yazar), ? belirsiz.


### Tefsir

| Eser | Müellif | Cümle | H | N | D | T | A | M/T/B/? | Risale eseri |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| el-Keşşâf / Zemahşerî | Zemahşerî | 19 | 1 | 15 | 3 |  |  | 19/0/0/0 | 8 |
| Tenvîrü'l-Mikbâs (Tefsîr-i İbn Abbâs) | İbn Abbâs'a nisbet; Fîrûzâbâdî | 10 |  | 7 | 3 |  |  | 10/0/0/0 | 2 |
| Mefâtîhu'l-Gayb / Fahreddîn-i Râzî | Fahreddîn er-Râzî | 8 | 2 | 6 |  |  |  | 8/0/0/0 | 4 |
| Câmiu'l-Beyân / Taberî | Taberî | 4 |  | 3 | 1 |  |  | 4/0/0/0 | 1 |
| "Mübarek bir zâtın tefsiri" (adı verilmez) | — | 2 |  |  | 2 |  |  | 2/0/0/0 | 1 |
| Envârü't-Tenzîl | Beyzâvî | 1 |  |  | 1 |  |  | 1/0/0/0 | 1 |

### Hadis ve siyer

| Eser | Müellif | Cümle | H | N | D | T | A | M/T/B/? | Risale eseri |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| Sahîh-i Buhârî | Buhârî | 32 |  | 27 | 3 |  | 2 | 32/0/0/0 | 1 |
| Sahîh-i Müslim | Müslim | 19 |  | 15 | 2 |  | 2 | 19/0/0/0 | 2 |
| Beyhakî (Sünen, Delâil, Şuab) | Beyhakî | 14 |  | 14 |  |  |  | 13/1/0/0 | 2 |
| Kütüb-i Sitte (topluca) | — | 9 |  | 7 | 1 |  | 1 | 7/1/1/0 | 3 |
| eş-Şifâ | Kādî Iyâz | 9 | 2 | 7 |  |  |  | 9/0/0/0 | 2 |
| Tirmizî (Sünen) | Tirmizî | 8 |  | 7 | 1 |  |  | 8/0/0/0 | 1 |
| Müsned | Ahmed b. Hanbel | 4 |  | 4 |  |  |  | 4/0/0/0 | 1 |
| Sünen-i Nesâî | Nesâî | 4 |  | 4 |  |  |  | 4/0/0/0 | 1 |
| Sünen-i Ebû Dâvûd | Ebû Dâvûd | 3 |  | 3 |  |  |  | 2/1/0/0 | 2 |
| Delâilü'n-Nübüvve | Ebû Nuaym | 3 |  | 3 |  |  |  | 3/0/0/0 | 1 |
| Süyûtî (hadis) | Süyûtî | 2 |  | 1 |  |  | 1 | 2/0/0/0 | 1 |
| Taberânî (Mu'cem) | Taberânî | 2 |  | 2 |  |  |  | 2/0/0/0 | 1 |
| İbn Hibbân (Sahîh) | İbn Hibbân | 2 |  | 1 | 1 |  |  | 2/0/0/0 | 1 |
| el-Muvatta' | İmâm Mâlik | 2 |  | 1 | 1 |  |  | 2/0/0/0 | 2 |
| Müsned-i Bezzâr | Bezzâr | 1 |  | 1 |  |  |  | 1/0/0/0 | 1 |
| el-Mevâhibü'l-Ledünniyye | Kastalânî | 1 | 1 |  |  |  |  | 1/0/0/0 | 1 |
| Sünen-i Dârimî | Dârimî | 1 |  | 1 |  |  |  | 1/0/0/0 | 1 |
| Sîre (İbn Hişâm / İbn İshak) | İbn Hişâm | 1 |  | 1 |  |  |  | 1/0/0/0 | 1 |
| el-Müstedrek | Hâkim | 1 |  | 1 |  |  |  | 0/1/0/0 | 1 |
| Sünen-i İbn Mâce | İbn Mâce | 1 |  | 1 |  |  |  | 1/0/0/0 | 1 |

### Kelâm, usûl ve reddiye

| Eser | Müellif | Cümle | H | N | D | T | A | M/T/B/? | Risale eseri |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| er-Risâletü'l-Hamîdiyye | Hüseyin el-Cisr | 11 | 1 | 10 |  |  |  | 11/0/0/0 | 7 |
| Teftâzânî (eser adı anılmadan) | Teftâzânî | 8 |  | 8 |  |  |  | 8/0/0/0 | 6 |
| et-Telvîh (Mukaddemât-ı İsnâ Aşer) | Teftâzânî | 6 |  |  | 6 |  |  | 6/0/0/0 | 3 |
| Şerhu'l-Mevâkıf | Seyyid Şerîf Cürcânî | 5 | 2 | 2 |  |  | 1 | 4/1/0/0 | 3 |
| İbn Teymiyye ve İbnü'l-Kayyim'in eserleri (adı verilmez) | İbn Teymiyye, İbnü'l-Kayyim | 4 |  |  | 4 |  |  | 4/0/0/0 | 2 |
| Cem'u'l-Cevâmi' (usûl) | Tâceddîn es-Sübkî | 3 |  |  |  |  | 3 | 0/3/0/0 | 1 |
| Şerhu'l-Makāsıd | Teftâzânî | 3 | 2 | 1 |  |  |  | 3/0/0/0 | 3 |
| Seyyid Şerîf (eser adı anılmadan) | Seyyid Şerîf Cürcânî | 2 |  | 2 |  |  |  | 2/0/0/0 | 2 |
| el-Fıkhu'l-Ekber | Ebû Hanîfe | 1 |  |  | 1 |  |  | 1/0/0/0 | 1 |
| İzhârü'l-Hak | Rahmetullah el-Hindî | 1 |  | 1 |  |  |  | 1/0/0/0 | 1 |
| Metâli' (hangisi olduğu yazılmaz) | — | 1 |  |  |  |  | 1 | 0/1/0/0 | 1 |

### Tasavvuf

| Eser | Müellif | Cümle | H | N | D | T | A | M/T/B/? | Risale eseri |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| Fütûhu'l-Gayb | Abdülkādir-i Geylânî | 20 |  | 1 | 2 | 9 | 8 | 14/6/0/0 | 6 |
| İmâm-ı Rabbânî (eser adı anılmadan) | İmâm-ı Rabbânî | 20 |  | 17 | 2 |  | 1 | 17/3/0/0 | 9 |
| Geylânî (eser adı anılmadan) | Abdülkādir-i Geylânî | 16 |  | 8 | 3 |  | 5 | 7/8/1/0 | 9 |
| İbn Arabî (eser adı anılmadan) | İbn Arabî | 16 |  | 5 | 11 |  |  | 9/7/0/0 | 7 |
| Gazâlî (eser adı anılmadan) | Gazâlî | 11 |  | 5 | 3 |  | 3 | 6/4/1/0 | 6 |
| Mevlânâ (eser adı anılmadan) | Mevlânâ | 9 |  | 7 | 1 |  | 1 | 6/3/0/0 | 7 |
| Mesnevî | Mevlânâ | 8 |  |  | 8 |  |  | 1/5/0/2 | 5 |
| Mektûbât | İmâm-ı Rabbânî | 6 |  | 2 |  | 4 |  | 6/0/0/0 | 3 |
| el-Fütûhâtü'l-Mekkiyye | İbn Arabî | 5 | 2 | 2 |  |  | 1 | 5/0/0/0 | 4 |
| İbn Arabî'nin Râzî'ye mektubu | İbn Arabî | 4 |  | 4 |  |  |  | 3/1/0/0 | 1 |
| Geylânî'nin kasidesi ve virdi | Abdülkādir-i Geylânî | 2 |  | 2 |  |  |  | 2/0/0/0 | 1 |
| el-Mîzânü'l-Kübrâ | Şa'rânî | 2 | 1 | 1 |  |  |  | 2/0/0/0 | 2 |
| Cünnetü'l-Esmâ | Gazâlî | 1 |  | 1 |  |  |  | 1/0/0/0 | 1 |
| el-Yevâkît ve'l-Cevâhir | Şa'rânî | 1 |  | 1 |  |  |  | 1/0/0/0 | 1 |
| İhyâu Ulûmi'd-Dîn | Gazâlî | 1 |  | 1 |  |  |  | 0/1/0/0 | 1 |
| el-Fusûs (Fusûsu'l-Hikem olabilir) | İbn Arabî (?) | 1 |  |  |  |  | 1 | 1/0/0/0 | 1 |
| Dîvân | İbnü'l-Fârıd | 1 |  |  |  | 1 |  | 0/1/0/0 | 1 |
| Dîvân | Ümmî Sinan | 1 |  |  |  | 1 |  | 0/1/0/0 | 1 |

### Belâgat, dil ve mantık

| Eser | Müellif | Cümle | H | N | D | T | A | M/T/B/? | Risale eseri |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| Miftâhu'l-Ulûm / Sekkâkî | Sekkâkî | 16 | 2 | 13 | 1 |  |  | 16/0/0/0 | 7 |
| Muallakāt-ı Seb'a | — | 11 |  |  | 8 |  | 3 | 9/0/2/0 | 8 |
| el-Kâmûsu'l-Muhît | Fîrûzâbâdî | 9 |  |  | 2 |  | 7 | 5/3/1/0 | 4 |
| Delâilü'l-İ'câz ve Esrârü'l-Belâğa | Abdülkāhir el-Cürcânî | 9 | 3 | 4 | 2 |  |  | 9/0/0/0 | 2 |
| el-Burhân | Gelenbevî | 9 |  | 7 |  |  | 2 | 1/0/8/0 | 3 |
| Molla Câmî (nahiv şerhi) | Câmî | 3 |  |  |  |  | 3 | 0/3/0/0 | 2 |
| Şerh-i Şemsiyye | Kutbüddîn er-Râzî | 2 |  |  |  |  | 2 | 0/2/0/0 | 2 |
| Sîbeveyh (el-Kitâb) | Sîbeveyh | 2 |  | 2 |  |  |  | 2/0/0/0 | 1 |
| Mirkât (mantık) | — | 2 |  |  |  |  | 2 | 0/2/0/0 | 1 |
| Süyûtî'nin nahiv şerhi | Süyûtî | 1 |  |  |  |  | 1 | 0/1/0/0 | 1 |
| Câhız | Câhız | 1 |  | 1 |  |  |  | 1/0/0/0 | 1 |
| Makāmât | Harîrî | 1 |  |  |  |  | 1 | 0/1/0/0 | 1 |

### Fıkıh

| Eser | Müellif | Cümle | H | N | D | T | A | M/T/B/? | Risale eseri |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| İbn Hacer el-Heytemî'nin fıkhı | İbn Hacer el-Heytemî | 3 |  | 1 | 2 |  |  | 3/0/0/0 | 2 |
| Mecmau'l-Enhur; Merâku'l-Felâh | Dâmâd; Şürünbülâlî | 1 |  | 1 |  |  |  | 1/0/0/0 | 1 |
| Halebî (Halebî-i Kebîr) | İbrâhim el-Halebî | 1 |  |  |  |  | 1 | 1/0/0/0 | 1 |

### Ahlâk

| Eser | Müellif | Cümle | H | N | D | T | A | M/T/B/? | Risale eseri |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| Edebü'd-Dünyâ ve'd-Dîn | Mâverdî | 2 |  | 2 |  |  |  | 2/0/0/0 | 2 |

### Dua ve vird

| Eser | Müellif | Cümle | H | N | D | T | A | M/T/B/? | Risale eseri |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| Cevşenü'l-Kebîr | Peygamber'e nisbet | 54 |  | 16 | 13 |  | 25 | 48/5/0/1 | 15 |
| Kaside-i Ercûze | Hz. Ali'ye nisbet | 17 | 1 | 14 |  |  | 2 | 13/4/0/0 | 6 |
| Mecmûatü'l-Ahzâb | Gümüşhânevî (derleyen) | 8 | 1 | 3 |  |  | 4 | 4/1/0/3 | 3 |
| Evrâd-ı Bahâiye | Şâh-ı Nakşibend'e nisbet | 5 |  | 1 |  |  | 4 | 4/1/0/0 | 2 |
| Kasîdetü'l-Bürde | Bûsîrî | 3 |  | 3 |  |  |  | 3/0/0/0 | 3 |
| Delâilü'l-Hayrât | Cezûlî | 2 |  |  |  |  | 2 | 1/1/0/0 | 2 |

### Edebiyat

| Eser | Müellif | Cümle | H | N | D | T | A | M/T/B/? | Risale eseri |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| Gülistân, Bostân / Sa'dî | Sa'dî-i Şîrâzî | 7 |  | 5 | 1 | 1 |  | 7/0/0/0 | 4 |
| Hâfız-ı Şîrâzî | Hâfız | 1 |  | 1 |  |  |  | 1/0/0/0 | 1 |

### Felsefe

| Eser | Müellif | Cümle | H | N | D | T | A | M/T/B/? | Risale eseri |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| İbn Sînâ (eser adı anılmadan) | İbn Sînâ | 12 |  | 7 | 5 |  |  | 5/7/0/0 | 9 |
| Fârâbî (eser adı anılmadan) | Fârâbî | 4 |  |  | 4 |  |  | 0/4/0/0 | 4 |
| Eflâtun / Aristo | — | 3 |  | 1 | 2 |  |  | 0/0/3/0 | 3 |

### Önceki kitaplar

| Eser | Müellif | Cümle | H | N | D | T | A | M/T/B/? | Risale eseri |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| İncil | — | 59 |  | 43 | 6 |  | 10 | 55/2/2/0 | 16 |
| Tevrat | — | 52 |  | 39 | 6 |  | 7 | 50/0/2/0 | 14 |
| Suhuf (İbrâhîm, Şuayb…) | — | 43 |  | 10 |  |  | 33 | 41/0/0/2 | 10 |
| Zebur | — | 22 |  | 8 | 2 |  | 12 | 21/1/0/0 | 8 |
| Kitâb-ı Mukaddes | — | 2 |  |  | 2 |  |  | 0/0/2/0 | 2 |
| Kitâb-ı Eş'ıyâ (İşaya) | — | 2 |  | 2 |  |  |  | 2/0/0/0 | 2 |
| Kitâb-ı Mîhâ (Mika) | — | 1 |  | 1 |  |  |  | 1/0/0/0 | 1 |

### Batı ve yeni zaman

| Eser | Müellif | Cümle | H | N | D | T | A | M/T/B/? | Risale eseri |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| Carlyle | Thomas Carlyle | 25 |  | 22 |  |  | 3 | 17/1/0/7 | 9 |
| Bismarck | Bismarck | 20 |  | 14 |  |  | 6 | 15/5/0/0 | 5 |
| Târîh-i İslâmiyet | Reinhart Dozy | 8 |  |  | 8 |  |  | 7/0/0/1 | 3 |
| Molière, Victor Hugo, Goethe | — | 3 |  |  | 3 |  |  | 0/3/0/0 | 1 |
| Renaud'nun Kur'ân tercümesi | Renaud | 2 |  |  | 2 |  |  | 0/0/2/0 | 2 |
| Roma İmparatorluğunun İnhitat ve Sukûtu | Edward Gibbon | 2 |  | 2 |  |  |  | 0/0/0/2 | 2 |

### Basın ve yeni yayınlar

| Eser | Müellif | Cümle | H | N | D | T | A | M/T/B/? | Risale eseri |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| Sebîlürreşâd (dergi) | — | 16 | 3 |  | 1 |  | 12 | 9/3/4/0 | 6 |
| es-Sıddîk (Pakistan, dergi) | — | 6 |  | 1 |  |  | 5 | 0/6/0/0 | 2 |
| el-Esâs fi's-Sünne | Saîd Havvâ | 2 |  | 2 |  |  |  | 0/0/2/0 | 2 |
| Students' Voice; "İslâmın Büyük Rönesansı" | Zafer Afaq Ansar | 2 |  | 2 |  |  |  | 0/2/0/0 | 1 |
| Radyo istasyonları cetveli | — | 1 |  | 1 |  |  |  | 1/0/0/0 | 1 |
| Safahât | Mehmed Âkif | 1 |  |  |  |  | 1 | 0/0/1/0 | 1 |
| Bediüzzaman'ın Tarihçe-i Hayatı | Müküslü Hamza | 1 |  |  |  |  | 1 | 0/0/1/0 | 1 |

## Ek B. Bütün yerler

Her satır: tür · konuşan · yer (cümle kimliği) · okuyucunun notu. Notlar ajanların okumasıdır, elle denetlenmedi (örneklem: 25'te 22 açıkça doğru).


### Tefsir

**el-Keşşâf / Zemahşerî** (Zemahşerî): 19

- havale · müellif · İşaratü'l-İ'caz › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri (Nübüvvet Hakkında) › İ'câzın Vecihleri › 9. cümle (`isaratul-icaz/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/icazin-vecihleri/c009`) — İ'câzın icmâlî bilgisi için belâgat imamlarının beyanına gönderir
- nakil · müellif · İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 17‑20. Âyetlerin Tefsiri › المسألة الثالثة: › 17. cümle (`isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/mesele-03/c017`) — Zemahşerî'nin Yâsîn 78'den meydan okuma üslubu sezişini nakleder
- nakil · müellif · İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 2. Âyetin Tefsiri › مقدمة › 22. cümle (`isaratul-icaz-arabi/sure-i-bakara/2/mukaddime/c022`) — 'Lâ rayb' vechinde Keşşâf'ın görüşünü nakleder
- nakil · müellif · İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri › المسألة السابعة: › 11. cümle (`isaratul-icaz-arabi/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-07/c011`) — Zemahşerî'nin mucizelerin bine ulaştığı sözünü nakleder
- nakil · müellif · İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri › المسألة السابعة: › 34. cümle (`isaratul-icaz-arabi/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-07/c034`) — İ'câzı bilmenin üç yolunu belâgat imamlarının tahkikine dayandırır
- nakil · müellif · İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri › المسألة السابعة: › 164. cümle (`isaratul-icaz-arabi/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-07/c164`) — İ'câzın sebebinde Cürcânî, Zemahşerî, Sekkâkî görüşünü esah sayar
- nakil · müellif · İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri › المسألة السابعة: › 170. cümle (`isaratul-icaz-arabi/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-07/c170`) — Sûrelere taksimin faydalarını Zemahşerî'nin beyanına dayandırır
- nakil · müellif · İşaratü'l-İ'caz › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri (Nübüvvet Hakkında) › İ'câzın Vecihleri › Üçüncü Vecih › 122. cümle (`isaratul-icaz/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/icazin-vecihleri/vecih-03-2/c122`) — Belâgat imamlarının i'câz görüşünü nakleder
- nakil · müellif · İşaratü'l-İ'caz › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri (Nübüvvet Hakkında) › İ'câzın Vecihleri › Üçüncü Vecih › 136. cümle (`isaratul-icaz/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/icazin-vecihleri/vecih-03-2/c136`) — Sûrelere taksimin faydalarını Zemahşerî'nin beyanıyla anar
- nakil · müellif · İşaratü'l-İ'caz › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri (Nübüvvet Hakkında) › Yedinci Mes'ele › 21. cümle (`isaratul-icaz/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-07/c021`) — Keşşâf müellifine göre mucizelerin bine ulaştığını nakleder
- nakil · müellif · Muhakemat › İkinci Makale › Üçüncü Mes'ele › 32. cümle (`muhakemat/makale-02/mesele-03/c032`) — Zemahşerî'nin Yâsîn 78'den meydan okuma üslubu sezişini nakleder
- nakil · müellif · Sözler › Yirmibeşinci Söz › İkinci Şu'le › Birinci Nur › 1. cümle (`sozler/25/sule-02/nur-01/c001`) — Kur'ân'ın tesanüdüne belâgat imamlarının şehadetini delil getirir
- nakil · müellif · Sözler › Yirmibeşinci Söz › Birinci Zeyl › Üçüncü Nokta › 5. cümle (`sozler/25/zeyl-01/nokta-03/c005`) — Belâgat imamlarının Kur'ân belâgatının beşer üstü olduğu kararını nakleder
- nakil · müellif · Şuaat-ı Marifetü'n-Nebi › Altıncı Şuâ › Yedinci Menba' › 3. cümle (`suaat-i-marifetin-nebi/6/menba-07/c003`) — Belâgat imamlarının i'câza üç yolla hükmettiğini nakleder
- nakil · müellif · Şualar › Yedinci Şuâ › Âyetü'l‑Kübrâ › Birinci Bâb (Berâhin‑i Ulûhiyet) › Onyedinci Mertebe (Kur'ân‑ı Mu'cizü'l-Beyân) › Üçüncü Nokta › 5. cümle (`sualar/7/ayetul-kubra/bab-01/mertebe-17/nokta-03/c005`) — Belâgat imamlarının Kur'ân belâgatının beşer üstü olduğu kararını nakleder
- nakil · müellif · Tarihçe-i Hayat › Dördüncü Kısım Kastamonu Hayatı › Âyetü'l‑Kübrâ › Onyedinci Mertebe (Kur'ân‑ı Mu'cizü'l-Beyân) › Üçüncü Nokta › 5. cümle (`tarihce-i-hayat/dorduncu-kisim-kastamonu-hayati/ayetul-kubra/mertebe-17/nokta-03/c005`) — Belâgat imamlarının Kur'ân belâgatının beşer üstü olduğu kararını nakleder
- değerlendirme · müellif · Mektubat › Yirmidokuzuncu Mektûb › Dokuzuncu Kısım: Telvihât‑ı Tis'a › Yedinci Telvih › Dördüncü Nükte › 4. cümle (`mektubat/29/kisim-09/telvih-07/nukte-04/c004`) — Zemahşerî'nin Ehl-i Sünnete şiddetli itirazlarına rağmen tekfir edilmediğini söyler
- değerlendirme · müellif · Mektubat › Yirmidokuzuncu Mektûb › Dokuzuncu Kısım: Telvihât‑ı Tis'a › Yedinci Telvih › Dördüncü Nükte › 7. cümle (`mektubat/29/kisim-09/telvih-07/nukte-04/c007`) — Zemahşerî'nin itirazlarının hak sevgisinden geldiğini söyler
- değerlendirme · müellif · Muhakemat › İkinci Makale › Onikinci Mes'ele › 12. cümle (`muhakemat/makale-02/mesele-12/c012`) — Zemahşerî'nin bazı kelâmlarını âlî üslûba misal gösterir

**Tenvîrü'l-Mikbâs (Tefsîr-i İbn Abbâs)** (İbn Abbâs'a nisbet; Fîrûzâbâdî): 10

- nakil · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Rumuzat‑ı Semaniye hakkında yazılmış mektuptur › 3. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/134/c003`) — Kâmûs sahibinin tefsiriyle hesaplarının tevafukunu karşılaştırır
- nakil · müellif · Rumuzat-ı Semaniye › Yirmi Dokuzuncu Mektub'un Sekizinci Kısmı › Yirmi Dokuzuncu Mektub'un Sekizinci Kısmının İkinci Remzi › İKİNCİ REMZ'İN MÜHİM BİR ZEYLİ › 31. cümle (`rumuzat-i-semaniye/kisim-08/remiz-02/zeyl/c031`) — Sûrelerin kelime/harf sayılarını Tenvîrü'l-Mikbâs'a göre verir
- nakil · müellif · Rumuzat-ı Semaniye › Yirmi Dokuzuncu Mektub'un Sekizinci Kısmı › Yirmi Dokuzuncu Mektub'un Sekizinci Kısmının İkinci Remzi › İKİNCİ REMZ'İN MÜHİM BİR ZEYLİ › 42. cümle (`rumuzat-i-semaniye/kisim-08/remiz-02/zeyl/c042`) — Sûrelerin kelime/harf sayılarını Tenvîrü'l-Mikbâs'a göre verir
- nakil · müellif · Rumuzat-ı Semaniye › Yirmi Dokuzuncu Mektub'un Sekizinci Kısmı › Yirmi Dokuzuncu Mektub'un Sekizinci Kısmı'nın Üçüncü Remzi › Birinci Kısım › Dördüncü Letafet › 28. cümle (`rumuzat-i-semaniye/kisim-08/remiz-03/kisim-01/letafet-04/c028`) — Sûrelerin kelime/harf sayılarını Tenvîrü'l-Mikbâs'a göre verir
- nakil · müellif · Rumuzat-ı Semaniye › Yirmi Dokuzuncu Mektub'un Sekizinci Kısmı › Yirmi Dokuzuncu Mektub'un Sekizinci Kısmı'nın Üçüncü Remzi › Üçüncü Nükte-i Kenzü'l-Arşiye'nin İkinci Kısmı › Birinci Misal › 1. cümle (`rumuzat-i-semaniye/kisim-08/remiz-03/kisim-02/misal-01/c001`) — Bakara'nın kelime sayısını Tenvîrü'l-Mikbâs hesabıyla verir
- nakil · müellif · Rumuzat-ı Semaniye › Yirmi Dokuzuncu Mektub'un Sekizinci Kısmı › Yirmi Dokuzuncu Mektub'un Sekizinci Kısmı'nın Üçüncü Remzi › Üçüncü Nükte-i Kenzü'l-Arşiye'nin İkinci Kısmı › Üçüncü Misal › 7. cümle (`rumuzat-i-semaniye/kisim-08/remiz-03/kisim-02/misal-03/c007`) — Sûrelerin tarihlere işaretini Tenvîrü'l-Mikbâs sayısına dayandırır
- nakil · müellif · Rumuzat-ı Semaniye › Yirmi Dokuzuncu Mektub'un Sekizinci Kısmı › Yirmi Dokuzuncu Mektub'un Sekizinci Kısmı'nın Üçüncü Remzi › Mukaddime › 3. cümle (`rumuzat-i-semaniye/kisim-08/remiz-03/mukaddime/c003`) — Kâmûs sahibinin tefsirine dayanarak sûre tevafuklarını yazdığını söyler
- değerlendirme · müellif · Rumuzat-ı Semaniye › Yirmi Dokuzuncu Mektub'un Sekizinci Kısmı › Yirmi Dokuzuncu Mektub'un Sekizinci Kısmı'nın Üçüncü Remzi › Birinci Kısım › Dördüncü Letafet › 30. cümle (`rumuzat-i-semaniye/kisim-08/remiz-03/kisim-01/letafet-04/c030`) — Sayıları Tenvîrü'l-Mikbâs'a dayandırır, rivayete dayandığı için muteber sayar
- değerlendirme · müellif · Rumuzat-ı Semaniye › Yirmi Dokuzuncu Mektub'un Sekizinci Kısmı › Yirmi Dokuzuncu Mektub'un Sekizinci Kısmı'nın Üçüncü Remzi › Üçüncü Nükte-i Kenzü'l-Arşiye'nin İkinci Kısmı › Mühim Bir İhtar › 21. cümle (`rumuzat-i-semaniye/kisim-08/remiz-03/kisim-02/muhim-bir-ihtar/c021`) — Tenvîrü'l-Mikbâs'ın sayım mikyasını teşhis edemediğini söyler
- değerlendirme · müellif · Rumuzat-ı Semaniye › Yirmi Dokuzuncu Mektub'un Sekizinci Kısmı › Yirmi Dokuzuncu Mektub'un Sekizinci Kısmı'nın Üçüncü Remzi › Üçüncü Nükte-i Kenzü'l-Arşiye'nin İkinci Kısmı › Mühim Bir İhtar › 36. cümle (`rumuzat-i-semaniye/kisim-08/remiz-03/kisim-02/muhim-bir-ihtar/c036`) — Tenvîrü'l-Mikbâs'taki sayıyı mikyasların en zâhiri sayar

**Mefâtîhu'l-Gayb / Fahreddîn-i Râzî** (Fahreddîn er-Râzî): 8

- havale · müellif · İşaratü'l-İ'caz › Sûre‑i Bakara › 25. Âyetin Tefsiri › Üçüncü ve Dördüncü Noktalar › 12. cümle (`isaratul-icaz/sure-i-bakara/25/ucuncu-ve-dorduncu-noktalar/c012`) — Haşrin aklî ve naklî delilleri için Râzî tefsirine gönderir
- havale · müellif · Muhakemat › Birinci Makale › Birinci Mes'ele › 3. cümle (`muhakemat/makale-01/mesele-01/c003`) — Arzın küreviyeti için Râzî'nin tefsirine gönderir
- nakil · müellif · Ta'likat (Arapça) › 153. cümle (`talikat-arabi/c153`) — İltizâmın mutâbakata lâzım olduğu Râzî görüşü (Arapça)
- nakil · müellif · Ta'likat › 88. cümle (`talikat/c088`) — Mantık meselesinde Râzî'nin görüşünü verir (Mefâtîh değil)
- nakil · müellif · Ta'likat › 187. cümle (`talikat/c187`) — İltizâmın mutâbakata lâzım olduğu Râzî görüşü
- nakil · müellif · Ta'likat › Küllî ve Cüzî Hakkında Bir Fasıl › 15. cümle › Hâşiye › 16. cümle (`talikat/kulli-ve-cuzi/c015/h1/c016`) — Haml türlerinde Râzî'nin görüşü (hâşiye)
- nakil · müellif · Ta'likat › Küllî ve Cüzî Hakkında Bir Fasıl › 17. cümle (`talikat/kulli-ve-cuzi/c017`) — Küllî-cüz'î meselesinde Râzî'nin görüşü
- nakil · müellif · Ta'likat › Şartlı Önerme Bölümü › 297. cümle › Hâşiye › 10. cümle (`talikat/sartiyye/c297/h1/c010`) — Haml türlerinde Râzî'nin görüşü; nâşir notu içerir

**Câmiu'l-Beyân / Taberî** (Taberî): 4

- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Bir İkram‑ı İlâhî ve Bir Eser-i İnâyet-i Rabbâniye › 13. cümle (`mektubat/19/bir-ikram-i-ilahi-ve-bir/c013`) — Mucize haberlerinin Taberî gibi kitaplardan nakledildiğini söyler
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Sekizinci İşâret › Altıncı Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-08/misal-06/c001`) — Ebû Katâde'nin su mucizesini Müslim ve Taberî'den aktarır
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Sekizinci İşâret › Altıncı Misâl › 5. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-08/misal-06/c005`) — Taberî'nin nakline göre sayının üç yüz olduğunu kaydeder
- değerlendirme · müellif · Mektubat › Yirmidokuzuncu Mektûb › Birinci Risale Olan Birinci Kısım › Birinci Nükte › 14. cümle (`mektubat/29/kisim-01/nukte-01/c014`) — Taberî'nin tefsirini senetle Risalete ulaştırdığını söyler

**"Mübarek bir zâtın tefsiri" (adı verilmez)** (—): 2

- değerlendirme · müellif · Rumuzat-ı Semaniye › Yirmi Sekizinci Mektub'un Yedinci Meselesindeki Mahremce Bir Suale Cevap › Yedinci Mesele'nin Hâtimesidir › İkinci Nükte › 1. cümle (`rumuzat-i-semaniye/mektub-28-mesele-07/hatime/nukte-02/c001`) — Tefsirdeki tevâfukları Sözler'inkilerle kıyaslıyor; Hulâsatü'l-Beyân olduğu söylenir, metinde ad yok.
- değerlendirme · müellif · Rumuzat-ı Semaniye › Yirmi Sekizinci Mektub'un Yedinci Meselesindeki Mahremce Bir Suale Cevap › Yedinci Mesele'nin Hâtimesidir › İkinci Nükte › İkinci fark › 2. cümle (`rumuzat-i-semaniye/mektub-28-mesele-07/hatime/nukte-02/ikinci-fark/c002`) — Tefsirin on beş senede dikkatle yazıldığını söyleyip farkı gösteriyor.

**Envârü't-Tenzîl** (Beyzâvî): 1

- değerlendirme · müellif · Muhakemat › Birinci Makale › Altıncı Mukaddeme › 46. cümle (`muhakemat/makale-01/mukaddeme-06/c046`) — Beyzâvî'nin Sedd te'viline kat'î bakmayı mantıksızlık sayar

### Hadis ve siyer

**Sahîh-i Buhârî** (Buhârî): 32

- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Bir İkram‑ı İlâhî ve Bir Eser-i İnâyet-i Rabbâniye › 13. cümle (`mektubat/19/bir-ikram-i-ilahi-ve-bir/c013`) — 19. Mektub'un nakillerinin kaynakları arasında Buhârî'yi sayar
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Beşinci Nükteli İşâret › 57. cümle (`mektubat/19/mucizat-i-ahmediye-asm/besinci-nukteli-isaret/c057`) — Anlatılacak gaybî haberlerde Buhârî ve Müslim'in müttefik olduğunu söyler
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Sekizinci İşâret › Birinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-08/misal-01/c001`) — Mucize haberini Buhârî ve Müslim'in rivayetiyle nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Sekizinci İşâret › İkinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-08/misal-02/c001`) — Mucize haberini Buhârî ve Müslim'in rivayetiyle nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Sekizinci İşâret › Üçüncü Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-08/misal-03/c001`) — Mucize haberini Buhârî ve Müslim'in rivayetiyle nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Sekizinci İşâret › Beşinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-08/misal-05/c001`) — Mucize haberini Buhârî ve Müslim'in rivayetiyle nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Sekizinci İşâret › Yedinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-08/misal-07/c001`) — Mucize haberini Buhârî ve Müslim'in rivayetiyle nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Sekizinci İşâret › Mukaddime › 14. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-08/mukaddime/c014`) — Parmaklardan su akması mucizesini Buhârî ve başkalarının naklinden bildirir
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onuncu İşâret › 15. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-10/c015`) — Hannâne mucizesini Buhârî ve Müslim'in tarikleriyle haber verir
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onbirinci İşâret › Birinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-11/misal-01/c001`) — Taamın tesbihi haberini Şifâ ve Buhârî sahibinden nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onbirinci İşâret › Beşinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-11/misal-05/c001`) — Uhud dağının titremesini Buhârî ve diğerlerinin rivayetiyle nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onikinci İşâret › İkinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-12/misal-02/c001`) — Mucize haberini Buhârî ve Müslim'in rivayetiyle nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onüçüncü İşâret › İkinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-13/misal-02/c001`) — Mucize haberini Buhârî ve Müslim'in rivayetiyle nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Ondördüncü İşâret › Birinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-14/misal-01/c001`) — Yağmur duasının kabulünü Buhârî ve Müslim'in naklinden bildirir
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Ondördüncü İşâret › Birinci Misâl › 10. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-14/misal-01/c010`) — Yağmur duasının kabulünü Buhârî ve Müslim'in naklinden bildirir
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Ondördüncü İşâret › Üçüncü Misâl › 3. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-14/misal-03/c003`) — Duanın kabulüne dair haberi Buhârî ve Müslim'den nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Ondördüncü İşâret › Üçüncü Misâl › 5. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-14/misal-03/c005`) — Duanın kabulüne dair haberi Buhârî ve Müslim'den nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Ondördüncü İşâret › Üçüncü Misâl › 15. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-14/misal-03/c015`) — Urve'ye bereket duasını Buhârî başta râvilerden nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Ondördüncü İşâret › Üçüncü Misâl › 17. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-14/misal-03/c017`) — Urve hakkında Buhârî'nin sözünü aktarır
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onbeşinci İşâret › Birinci Şûbesi › Dördüncü Hâdise › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-15/sube-01/hadise-04/c001`) — Hadiseyi Buhârî ve eimme-i hadisin rivayetiyle nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onbeşinci İşâret › İkinci Şûbe: › İkinci Cihet › 2. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-15/sube-02/cihet-02/c002`) — Hadiseyi Buhârî ve eimme-i hadisin rivayetiyle nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onbeşinci İşâret › Üçüncü Şûbe › Yedinci Hâdise › 3. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-15/sube-03/hadise-07/c003`) — Hadiseyi Buhârî ve eimme-i hadisin rivayetiyle nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Yedinci Nükteli İşâret › Birinci Misâli › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/yedinci-nukteli-isaret/misal-01/c001`) — Mucize haberini Buhârî ve Müslim'in rivayetiyle nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Yedinci Nükteli İşâret › Dördüncü Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/yedinci-nukteli-isaret/misal-04/c001`) — Mucize haberini Buhârî ve Müslim'in rivayetiyle nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Yedinci Nükteli İşâret › Ondördüncü Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/yedinci-nukteli-isaret/misal-14/c001`) — Mucize haberini Buhârî ve Müslim'in rivayetiyle nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Yedinci Nükteli İşâret › Onaltıncı Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/yedinci-nukteli-isaret/misal-16/c001`) — Mucize haberini Buhârî ve Müslim'in rivayetiyle nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Yedinci Nükteli İşâret › Onaltıncı Misâl › 15. cümle (`mektubat/19/mucizat-i-ahmediye-asm/yedinci-nukteli-isaret/misal-16/c015`) — Süt mucizesinin Buhârî başta Kütüb-i Sitte'deki naklini delil yapar
- değerlendirme · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Altıncı Nükteli İşâret › 110. cümle (`mektubat/19/mucizat-i-ahmediye-asm/altinci-nukteli-isaret/c110`) — Buhârî ve Müslim'in Kur'ân'dan sonra en sahih kitap olduğunu söyler
- değerlendirme · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Dördüncü Nükteli İşâret › Üçüncü Esâs › 16. cümle (`mektubat/19/mucizat-i-ahmediye-asm/dorduncu-nukteli-isaret/esas-03/c016`) — Buhârî ve Kütüb-i Sitte'nin kabul ettiği haber-i vâhidin kat'iyyetini söyler
- değerlendirme · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Dokuzuncu İşâret › Sekizinci Misâl › 10. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-09/misal-08/c010`) — Buhârî'de görmeyi sahabeden işitmek gibi sayar, sağlamlığını över
- anma · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Sekizinci İşâret › Mukaddime › 7. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-08/mukaddime/c007`) — Hadis kitaplarının Buhârî ve Müslim'e sağlam ulaştığını anlatır
- anma · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Yedinci Nükteli İşâret › Mukaddime › 16. cümle (`mektubat/19/mucizat-i-ahmediye-asm/yedinci-nukteli-isaret/mukaddime/c016`) — Hadislerin Buhârî, Müslim ve Kütüb-i Sitte ile muhafazasını tarihçe olarak anar

**Sahîh-i Müslim** (Müslim): 19

- nakil · müellif · Barla Lahikası › Mektûbat’ın Üçüncü Kısmı › Her risalede herkesin hissesi var, fakat herkes her şeyini bilmek lâzım değildir › 13. cümle (`barla-lahikasi/kisim-03/267/c013`) — Âl-i Abâ (mirt) hadisini Sahîh-i Müslim'den nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Beşinci Nükteli İşâret › 57. cümle (`mektubat/19/mucizat-i-ahmediye-asm/besinci-nukteli-isaret/c057`) — Anlatılacak haberlerde Buhârî ve Müslim'in müttefik olduğunu söyler
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Sekizinci İşâret › Altıncı Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-08/misal-06/c001`) — Ebû Katâde'nin kırba hadisesini Müslim'den nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Sekizinci İşâret › Yedinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-08/misal-07/c001`) — İmran b. Husayn'ın su mu'cizesini nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Dokuzuncu İşâret › Üçüncü Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-09/misal-03/c001`) — Câbir'in ağaçlar hadisesini Sahîh-i Müslim'den nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onikinci İşâret › Birinci Misâl › 4. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-12/misal-01/c004`) — Huneyn'de toprak atma mu'cizesini nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onüçüncü İşâret › İkinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-13/misal-02/c001`) — Hayber'de Hz. Ali'nin gözünün şifası rivayeti
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Ondördüncü İşâret › Birinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-14/misal-01/c001`) — Yağmur duâsının kabulünü nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Ondördüncü İşâret › Birinci Misâl › 10. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-14/misal-01/c010`) — Yağmur duâsı hadisesini nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Ondördüncü İşâret › Üçüncü Misâl › 3. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-14/misal-03/c003`) — İbn Abbâs'a duâ hadisini nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onbeşinci İşâret › İkinci Şûbe: › İkinci Cihet › 2. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-15/sube-02/cihet-02/c002`) — Cibrîl hadisini nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onbeşinci İşâret › Üçüncü Şûbe › Yedinci Hâdise › 3. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-15/sube-03/hadise-07/c003`) — 'Allah seni korur' âyeti sonrası nöbet hadisini nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Yedinci Nükteli İşâret › Birinci Misâli › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/yedinci-nukteli-isaret/misal-01/c001`) — Ümm-ü Süleym'in hurma mu'cizesini onlardan rivayet eder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Yedinci Nükteli İşâret › Dördüncü Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/yedinci-nukteli-isaret/misal-04/c001`) — Bir sâ' ekmek mu'cizesini kütüb-ü sahîhadan nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Yedinci Nükteli İşâret › Ondördüncü Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/yedinci-nukteli-isaret/misal-14/c001`) — Câbir'in babasının borcu hadisesini nakleder
- değerlendirme · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Altıncı Nükteli İşâret › 110. cümle (`mektubat/19/mucizat-i-ahmediye-asm/altinci-nukteli-isaret/c110`) — Buhârî ve Müslim'i Kur'ân'dan sonra en sahih kitap sayar
- değerlendirme · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Dördüncü Nükteli İşâret › Üçüncü Esâs › 16. cümle (`mektubat/19/mucizat-i-ahmediye-asm/dorduncu-nukteli-isaret/esas-03/c016`) — Kütüb-ü Sitte sahiblerinin tashihini tevâtür gibi kat'î sayar
- anma · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Sekizinci İşâret › Mukaddime › 7. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-08/mukaddime/c007`) — Hadis kitaplarının Buhârî ve Müslim'e sağlam ulaştığını söyler
- anma · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Ondördüncü İşâret › Yedinci Misâl › 11. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-14/misal-07/c011`) — Hammâd b. Seleme'yi Müslim'in güvendiği râvi diye anar

**Beyhakî (Sünen, Delâil, Şuab)** (Beyhakî): 14

- nakil · talebe · Barla Lahikası › Yirmiyedinci Mektûb’un Üçüncü Kısmı ve Üçüncü Zeylin Nihâyetidir › Şamlı Hafız Tevfik’in Risale‑i Nur’un hakkaniyetine dair yazdığı istihracî bir fıkrasıdır › 7. cümle (`barla-lahikasi/yirmiyedinci-mektubun-ucuncu-kismi-ve/142/c007`) — Müceddid hadisinin Beyhakî'nin Şuab'ında tahric edildiğini nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Bir İkram‑ı İlâhî ve Bir Eser-i İnâyet-i Rabbâniye › 13. cümle (`mektubat/19/bir-ikram-i-ilahi-ve-bir/c013`) — Mucizât-ı Ahmediye rivayetlerinin Beyhakî gibi kitaplardan alındığını söyler
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Altıncı Nükteli İşâret › 111. cümle (`mektubat/19/mucizat-i-ahmediye-asm/altinci-nukteli-isaret/c111`) — Mucizelerin Delâil-i Beyhakî gibi kitaplarda isnadıyla geçtiğini söyler
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Sekizinci İşâret › Dokuzuncu Misâl › 7. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-08/misal-09/c007`) — Mucize rivayetini Beyhakî'nin naklinden aktarır
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Dokuzuncu İşâret › Birinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-09/misal-01/c001`) — Mucize rivayetini Beyhakî'nin naklinden aktarır
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onüçüncü İşâret › Altıncı Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-13/misal-06/c001`) — Mucize rivayetini Beyhakî'nin naklinden aktarır
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onüçüncü İşâret › Sekizinci Misâl › 9. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-13/misal-08/c009`) — Mucize rivayetini Beyhakî'nin naklinden aktarır
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Ondördüncü İşâret › Üçüncü Misâl › 11. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-14/misal-03/c011`) — Mucize rivayetini Beyhakî'nin naklinden aktarır
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Ondördüncü İşâret › Yedinci Misâl › 3. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-14/misal-07/c003`) — Mucize rivayetini Beyhakî'nin naklinden aktarır
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onbeşinci İşâret › İkinci Şûbe: › 16. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-15/sube-02/c016`) — Mucize rivayetini Beyhakî'nin naklinden aktarır
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onbeşinci İşâret › İkinci Şûbe: › Üçüncü Hâdise › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-15/sube-02/hadise-03/c001`) — Mucize rivayetini Beyhakî'nin naklinden aktarır
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Yedinci Nükteli İşâret › Sekizinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/yedinci-nukteli-isaret/misal-08/c001`) — Mucize rivayetini Beyhakî'nin naklinden aktarır
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Yedinci Nükteli İşâret › Onüçüncü Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/yedinci-nukteli-isaret/misal-13/c001`) — Mucize rivayetini Beyhakî'nin naklinden aktarır
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Yedinci Nükteli İşâret › Onbeşinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/yedinci-nukteli-isaret/misal-15/c001`) — Mucize rivayetini Beyhakî'nin naklinden aktarır

**Kütüb-i Sitte (topluca)** (—): 9

- nakil · müellif · Barla Lahikası › Mektûbat’ın Üçüncü Kısmı › Her risalede herkesin hissesi var, fakat herkes her şeyini bilmek lâzım değildir › 16. cümle (`barla-lahikasi/kisim-03/267/c016`) — Âl-i Abâ'ya dair hadislerin Kütüb-i Sitte'de çok olduğunu söyler
- nakil · talebe · Barla Lahikası › Yirmiyedinci Mektûb’un Üçüncü Kısmı ve Üçüncü Zeylin Nihâyetidir › Şamlı Hafız Tevfik’in Risale‑i Nur’un hakkaniyetine dair yazdığı istihracî bir fıkrasıdır › 7. cümle (`barla-lahikasi/yirmiyedinci-mektubun-ucuncu-kismi-ve/142/c007`) — Müceddid hadisinin kaynaklarını sayar
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Altıncı Nükteli İşâret › 108. cümle (`mektubat/19/mucizat-i-ahmediye-asm/altinci-nukteli-isaret/c108`) — Gaybî haberlerin Kütüb-i Sitte'de senetleriyle zikredildiğini söyler
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Beşinci Nükteli İşâret › 57. cümle (`mektubat/19/mucizat-i-ahmediye-asm/besinci-nukteli-isaret/c057`) — Gaybî haberlerin çoğunda Kütüb-i Sitte'nin müttefik olduğunu söyler
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Yedinci Nükteli İşâret › Birinci Misâli › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/yedinci-nukteli-isaret/misal-01/c001`) — Velime mucizesini Kütüb-i Sitte'nin rivayetiyle aktarır
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Yedinci Nükteli İşâret › Onaltıncı Misâl › 15. cümle (`mektubat/19/mucizat-i-ahmediye-asm/yedinci-nukteli-isaret/misal-16/c015`) — Bereket mucizesinin Buhârî ve Kütüb-i Sitte'de naklini delil getirir
- nakil · başka · Ta'likat › Dördüncü Bâb: Deliller › 190. cümle › Hâşiye › 3. cümle (`talikat/edille/c190/h1/c003`) — Mütercim notu: et-Tâc'ın Kütüb-i Sitte'den naklettiği hadisi verir
- değerlendirme · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Dördüncü Nükteli İşâret › Üçüncü Esâs › 16. cümle (`mektubat/19/mucizat-i-ahmediye-asm/dorduncu-nukteli-isaret/esas-03/c016`) — Kütüb-i Sitte sahiplerinin kabulünü kat'iyet ölçüsü sayar
- anma · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Yedinci Nükteli İşâret › Mukaddime › 16. cümle (`mektubat/19/mucizat-i-ahmediye-asm/yedinci-nukteli-isaret/mukaddime/c016`) — Hadislerin Kütüb-i Sitte ile muhafazasını anlatır

**eş-Şifâ** (Kādî Iyâz): 9

- havale · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onyedinci İşâret › 5. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-17/c005`) — Ahlak mucizesinin beyanını Şifâ'ya havale eder
- havale · müellif · Şuaat-ı Marifetü'n-Nebi › Mukaddime › 22. cümle (`suaat-i-marifetin-nebi/mukaddime/c022`) — Mucizelerin tafsili için Şifâ ve Mevâhib'e gönderir
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Bir İkram‑ı İlâhî ve Bir Eser-i İnâyet-i Rabbâniye › 13. cümle (`mektubat/19/bir-ikram-i-ilahi-ve-bir/c013`) — 19. Mektub'un nakillerinin kaynakları arasında Şifâ'yı sayar
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Dokuzuncu İşâret › İkinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-09/misal-02/c001`) — Mucize haberini Kadı İyaz'ın Şifâ'sından nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onbirinci İşâret › Birinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-11/misal-01/c001`) — Mucize haberini Kadı İyaz'ın Şifâ'sından nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onüçüncü İşâret › Birinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-13/misal-01/c001`) — Mucize haberini Kadı İyaz'ın Şifâ'sından nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Yedinci Nükteli İşâret › Yedinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/yedinci-nukteli-isaret/misal-07/c001`) — Bereket mucizesini Şifâ ve hadis kitaplarının rivayetiyle nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Yedinci Nükteli İşâret › Sekizinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/yedinci-nukteli-isaret/misal-08/c001`) — Bereket mucizesini Şifâ ve hadis kitaplarının rivayetiyle nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Yedinci Nükteli İşâret › Dokuzuncu Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/yedinci-nukteli-isaret/misal-09/c001`) — Ehl-i Suffa bereket mucizesini Şifâ sahibi ve diğerlerinden nakleder

**Tirmizî (Sünen)** (Tirmizî): 8

- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Bir İkram‑ı İlâhî ve Bir Eser-i İnâyet-i Rabbâniye › 13. cümle (`mektubat/19/bir-ikram-i-ilahi-ve-bir/c013`) — Mucizât-ı Ahmediye rivayetlerinin Tirmizî gibi kitaplardan alındığını söyler
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Altıncı Nükteli İşâret › 111. cümle (`mektubat/19/mucizat-i-ahmediye-asm/altinci-nukteli-isaret/c111`) — Mucizelerin Sahîh-i Tirmizî gibi kitaplarda isnadıyla geçtiğini söyler
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Dokuzuncu İşâret › Sekizinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-09/misal-08/c001`) — Hurma dalı mucizesini Sahîh-i Tirmizî'den nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onbirinci İşâret › Beşinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-11/misal-05/c001`) — Mucize rivayetini Tirmizî'nin naklinden aktarır
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Ondördüncü İşâret › Üçüncü Misâl › 23. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-14/misal-03/c023`) — Mucize rivayetini Tirmizî'nin naklinden aktarır
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Yedinci Nükteli İşâret › Sekizinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/yedinci-nukteli-isaret/misal-08/c001`) — Mucize rivayetini Tirmizî'nin naklinden aktarır
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Yedinci Nükteli İşâret › Onbeşinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/yedinci-nukteli-isaret/misal-15/c001`) — Mucize rivayetini Tirmizî'nin naklinden aktarır
- değerlendirme · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Dokuzuncu İşâret › Sekizinci Misâl › 10. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-09/misal-08/c010`) — Tirmizî gibi kütüb-ü sahîhanın rivayet yolunu sağlam tuttuğunu söyler

**Müsned** (Ahmed b. Hanbel): 4

- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Altıncı Nükteli İşâret › 111. cümle (`mektubat/19/mucizat-i-ahmediye-asm/altinci-nukteli-isaret/c111`) — Mucize haberlerinin kaynakları arasında Müsned-i Ahmed'i sayar
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onikinci İşâret › Üçüncü Misâl › 2. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-12/misal-03/c002`) — Ahmed b. Hanbel'in tahric ve tashih ettiği mucize haberini nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Ondördüncü İşâret › Yedinci Misâl › 9. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-14/misal-07/c009`) — Mucize haberini Ahmed b. Hanbel'in rivayetiyle nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Yedinci Nükteli İşâret › Onüçüncü Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/yedinci-nukteli-isaret/misal-13/c001`) — Mucize haberini Ahmed b. Hanbel'in rivayetiyle nakleder

**Sünen-i Nesâî** (Nesâî): 4

- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Altıncı Nükteli İşâret › 111. cümle (`mektubat/19/mucizat-i-ahmediye-asm/altinci-nukteli-isaret/c111`) — Mucizelerin Nesâî gibi kitaplarda isnadıyla geçtiğini söyler
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onüçüncü İşâret › Üçüncü Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-13/misal-03/c001`) — Mucize rivayetini Nesâî'nin naklinden aktarır
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onüçüncü İşâret › Sekizinci Misâl › 9. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-13/misal-08/c009`) — Mucize rivayetini Nesâî'nin naklinden aktarır
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Yedinci Nükteli İşâret › Sekizinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/yedinci-nukteli-isaret/misal-08/c001`) — Mucize rivayetini Nesâî'nin naklinden aktarır

**Sünen-i Ebû Dâvûd** (Ebû Dâvûd): 3

- nakil · talebe · Barla Lahikası › Yirmiyedinci Mektûb’un Üçüncü Kısmı ve Üçüncü Zeylin Nihâyetidir › Şamlı Hafız Tevfik’in Risale‑i Nur’un hakkaniyetine dair yazdığı istihracî bir fıkrasıdır › 7. cümle (`barla-lahikasi/yirmiyedinci-mektubun-ucuncu-kismi-ve/142/c007`) — Müceddid hadisinin Sünen'de tahricini bildirir
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Altıncı Nükteli İşâret › 111. cümle (`mektubat/19/mucizat-i-ahmediye-asm/altinci-nukteli-isaret/c111`) — Mu'cize haberlerinin bu kitaplarda isnadıyla geçtiğini söyler
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Yedinci Nükteli İşâret › Onüçüncü Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/yedinci-nukteli-isaret/misal-13/c001`) — Ahmesî atlılarına zâd mu'cizesini nakleder

**Delâilü'n-Nübüvve** (Ebû Nuaym): 3

- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Bir İkram‑ı İlâhî ve Bir Eser-i İnâyet-i Rabbâniye › 13. cümle (`mektubat/19/bir-ikram-i-ilahi-ve-bir/c013`) — 19. Mektub'un nakillerinin kaynakları arasında Ebû Nuaym'ı sayar
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Ondördüncü İşâret › Yedinci Misâl › 5. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-14/misal-07/c005`) — Mucize haberini Ebû Nuaym'ın Delâil'inden nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onbeşinci İşâret › İkinci Şûbe: › Dördüncü Hâdise › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-15/sube-02/hadise-04/c001`) — Mucize haberini Ebû Nuaym'ın Delâil'inden nakleder

**Süyûtî (hadis)** (Süyûtî): 2

- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onüçüncü İşâret › Sekizinci Misâl › 14. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-13/misal-08/c014`) — Mübârekü'l-Yemâme hadisesini tahric ve tashihiyle nakleder
- anma · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Yedinci Nükteli İşâret › Mukaddime › 18. cümle (`mektubat/19/mucizat-i-ahmediye-asm/yedinci-nukteli-isaret/mukaddime/c018`) — Sahih hadisleri mevzulardan ayıran allâmeler arasında

**Taberânî (Mu'cem)** (Taberânî): 2

- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onbeşinci İşâret › İkinci Şûbe: › Dördüncü Hâdise › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-15/sube-02/hadise-04/c001`) — Zeyd b. Hârice'nin ölümden sonra konuşması rivayeti
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Yedinci Nükteli İşâret › Dokuzuncu Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/yedinci-nukteli-isaret/misal-09/c001`) — Ashâb-ı Suffa yemeği mu'cizesini rivayet eder

**İbn Hibbân (Sahîh)** (İbn Hibbân): 2

- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onbirinci İşâret › Beşinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-11/misal-05/c001`) — Uhud'un titremesi rivayetini İbn Hibbân'ın naklinden aktarır
- değerlendirme · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Dokuzuncu İşâret › Sekizinci Misâl › 10. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-09/misal-08/c010`) — İbn Hibbân gibi kütüb-ü sahîhanın rivayet yolunu sağlam tuttuğunu söyler

**el-Muvatta'** (İmâm Mâlik): 2

- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Sekizinci İşâret › Dördüncü Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-08/misal-04/c001`) — Tebük çeşmesi mucizesini Muvatta'dan nakleder
- değerlendirme · müellif · Sünuhat › Kur'ân’ın Hâkimiyet‑i Mutlakası › 28. cümle (`sunuhat/kuranin-hakimiyet-i-mutlakasi/c028`) — Muvatta'yı Kur'ân'ı gösteren şeffaf tefsir gibi kitaplara örnek verir

**Müsned-i Bezzâr** (Bezzâr): 1

- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Dokuzuncu İşâret › Birinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-09/misal-01/c001`) — Hz. Ömer'den ağaç mu'cizesi rivayeti

**el-Mevâhibü'l-Ledünniyye** (Kastalânî): 1

- havale · müellif · Şuaat-ı Marifetü'n-Nebi › Mukaddime › 22. cümle (`suaat-i-marifetin-nebi/mukaddime/c022`) — Mucizelerin tafsili için Şifâ ve Mevâhib'e gönderir

**Sünen-i Dârimî** (Dârimî): 1

- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Dokuzuncu İşâret › Birinci Misâl › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-09/misal-01/c001`) — Mahzun Peygambere ağacın gelmesi mucizesini Dârimî'den nakleder

**Sîre (İbn Hişâm / İbn İshak)** (İbn Hişâm): 1

- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Sekizinci İşâret › Dördüncü Misâl › 6. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-08/misal-04/c006`) — İbn İshak'ın çeşme suyunun akışına dair sözünü nakleder

**el-Müstedrek** (Hâkim): 1

- nakil · talebe · Barla Lahikası › Yirmiyedinci Mektûb’un Üçüncü Kısmı ve Üçüncü Zeylin Nihâyetidir › Şamlı Hafız Tevfik’in Risale‑i Nur’un hakkaniyetine dair yazdığı istihracî bir fıkrasıdır › 7. cümle (`barla-lahikasi/yirmiyedinci-mektubun-ucuncu-kismi-ve/142/c007`) — Müceddid hadisinin Müstedrek'te tahric edildiğini nakleder

**Sünen-i İbn Mâce** (İbn Mâce): 1

- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Ondördüncü İşâret › Yedinci Misâl › 6. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-14/misal-07/c006`) — Zemzem kovası mucizesini İbn Mâce'nin naklinden aktarır

### Kelâm, usûl ve reddiye

**er-Risâletü'l-Hamîdiyye** (Hüseyin el-Cisr): 11

- havale · müellif · Şuaat-ı Marifetü'n-Nebi › Birinci Şuâ › İkincisi › 3. cümle (`suaat-i-marifetin-nebi/1/ikincisi/c003`) — Beşâretlere dair yüz delil için Cisrî'nin risalesine havale
- nakil · müellif · İşaratü'l-İ'caz › Sûre‑i Bakara › 22. Âyetin Tefsiri › Delil‑i İhtirâî › 29. cümle (`isaratul-icaz/sure-i-bakara/22/delil-i-ihtirai/c029`) — Cisrî'nin ev ve ev sahibi temsilini nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › İkinci Hüccet › 6. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-02/c006`) — Semavî kitaplardan 114 delil çıkardığını bildirir
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › İkinci Hüccet › 7. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-02/c007`) — Bu delilleri Risale-i Hamîdiye'de yazdığını bildirir
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye’nin Birinci Zeyli › İkinci Reşha › 1. cümle › Hâşiye › 1. cümle (`mektubat/19/zeyl-01/resha-02/c001/h1/c001`) — Semavî kitaplardan 114 işaret çıkardığını delil eder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) Zeylinin Bir Parçasıdır › 6. cümle (`mektubat/19/zeyl-02/c006`) — Semavî kitaplardan 114 beşâret çıkardığını delil eder
- nakil · müellif · Muhakemat › Birinci Makale › Birinci Mes'ele › 8. cümle (`muhakemat/makale-01/mesele-01/c008`) — Cisrî'nin arzın küreviyetine dair sözünü dinlemeye çağırır
- nakil · müellif · Sözler › Ondokuzuncu Söz › İkinci Reşha › 2. cümle › Hâşiye › 1. cümle (`sozler/19/resha-02/c002/h1/c001`) — Semavî kitaplardan 114 işaret çıkardığını delil eder
- nakil · müellif · Sözler › Otuzbirinci Söz › Üçüncü Esâs › İkinci Temsîl › 30. cümle (`sozler/31/esas-03/temsil-02/c030`) — Semavî kitaplardan 114 beşâret çıkardığını delil eder
- nakil · müellif · Şualar › Onbeşinci Şuâ › Birinci Makam › Üçüncü Medrese‑i Yûsufiye’nin Tek Bir Dersinin Üçüncü Kısmı › İkinci İşâret › Onüçüncü Şehâdet › 6. cümle (`sualar/15/makam-01/kisim-03/isaret-02/sehadet-13/c006`) — Nübüvvete dair yüz âyeti kitabında yazdığını bildirir
- nakil · müellif · Zülfikâr › On Dokuzuncu Mektub › Mu'cizat-ı Ahmediye (A.S.M.) Zeylinin Bir Parçasıdır › 1. cümle (`zulfikar/mektub-19/mucizat-i-ahmediye-a-s-m-zeylinin-bir/c001`) — Semavî kitaplardan 114 beşâret çıkardığını delil eder

**Teftâzânî (eser adı anılmadan)** (Teftâzânî): 8

- nakil · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Ehl‑i Sünnet ve'l-Cemâat, Sahabeler zamanındaki fitnelerden bahis açmayı men etmişler › 11. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/151/c011`) — Taftazânî'nin Yezid'e lanetin caiz olduğu görüşünü nakleder
- nakil · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Ehl‑i Sünnet ve'l-Cemâat, Sahabeler zamanındaki fitnelerden bahis açmayı men etmişler › 47. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/151/c047`) — Taftazânî'nin cevazını Seyyid Şerif'in görüşüyle karşılaştırarak nakleder
- nakil · müellif · İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 3. Âyetin Tefsiri › 23. cümle (`isaratul-icaz-arabi/sure-i-bakara/3/c023`) — Îmânın tarifini Teftâzânî'den alır (كما فسّره السعد)
- nakil · müellif · İşaratü'l-İ'caz › Sûre‑i Bakara › 3. Âyetin Tefsiri › Îmân‑ı Bilgayb › 44. cümle (`isaratul-icaz/sure-i-bakara/3/iman-i-bilgayb/c044`) — Îmanın tarifini Taftazânî'den nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye’nin Birinci Zeyli › Ondokuzuncu ve Otuzbirinci Söz’lerin Zeyli › İkinci Nokta › 1. cümle (`mektubat/19/zeyl-01/zeyl/nokta-02/c001`) — Taftazânî ve muhakkiklerin bazı mucizelerin mütevatir olduğu hükmünü nakleder
- nakil · müellif · Sözler › Otuzbirinci Söz › Ondokuzuncu ve Otuzbirinci Söz’lerin Zeyli › İkinci Nokta › 1. cümle (`sozler/31/zeyl/nokta-02/c001`) — Taftazânî ve muhakkiklerin bazı mucizelerin mütevatir olduğu hükmünü nakleder
- nakil · müellif · Tarihçe-i Hayat › Altıncı Kısım Emirdağı Hayatı › Ehl‑i Sünnet ve’l-Cemaat, Sahabeler zamanındaki fitnelerden bahis açmayı men etmişler › 13. cümle (`tarihce-i-hayat/altinci-kisim-emirdagi-hayati/ehl-i-sunnet-vel-cemaat-sahabeler-zamanindaki/c013`) — Taftazânî'nin Yezid'e lanetin caiz olduğu görüşünü nakleder
- nakil · müellif · Tarihçe-i Hayat › Altıncı Kısım Emirdağı Hayatı › Ehl‑i Sünnet ve’l-Cemaat, Sahabeler zamanındaki fitnelerden bahis açmayı men etmişler › 49. cümle (`tarihce-i-hayat/altinci-kisim-emirdagi-hayati/ehl-i-sunnet-vel-cemaat-sahabeler-zamanindaki/c049`) — Taftazânî'nin cevazını Seyyid Şerif'in görüşüyle karşılaştırarak nakleder

**et-Telvîh (Mukaddemât-ı İsnâ Aşer)** (Teftâzânî): 6

- değerlendirme · müellif · Barla Lahikası › Yedinci Risale Olan Yedinci Mes'ele › Üçüncü İşâret › 4. cümle (`barla-lahikasi/mesele-07/isaret-03/c004`) — Telvih'in kırk-elli sayfada çözdüğü kaderi Söz'ün iki sayfada beyanıyla karşılaştırır
- değerlendirme · müellif · Barla Lahikası › Yedinci Risale Olan Yedinci Mes'ele › Üçüncü İşâret › 4. cümle (`barla-lahikasi/mesele-07/isaret-03/c004`) — Taftazânî'nin Telvih'teki kader bahsini Yirmi Altıncı Söz'le karşılaştırır
- değerlendirme · müellif · Mektubat › Yirmisekizinci Mektûb › Yedinci Risale Olan Yedinci Mes'ele › Üçüncü İşâret › 4. cümle (`mektubat/28/mesele-07/isaret-03/c004`) — Telvih'in kırk-elli sayfada çözdüğü kaderi Söz'ün iki sayfada beyanıyla karşılaştırır
- değerlendirme · müellif · Mektubat › Yirmisekizinci Mektûb › Yedinci Risale Olan Yedinci Mes'ele › Üçüncü İşâret › 4. cümle (`mektubat/28/mesele-07/isaret-03/c004`) — Taftazânî'nin Telvih'teki kader bahsini Yirmi Altıncı Söz'le karşılaştırır
- değerlendirme · müellif · Tarihçe-i Hayat › İkinci Kısım Barla Hayatı › Yirmisekizinci Mektûbun Yedinci Mes'elesi › Küllî Birkaç İnâyet‑i Rabbâniye’ye İşâretler › Üçüncü İşâret › 4. cümle (`tarihce-i-hayat/ikinci-kisim-barla-hayati/mesele-07/kulli-birkac-inayet-i-rabbaniyeye-isaretler/isaret-03/c004`) — Telvih'in kırk-elli sayfada çözdüğü kaderi Söz'ün iki sayfada beyanıyla karşılaştırır
- değerlendirme · müellif · Tarihçe-i Hayat › İkinci Kısım Barla Hayatı › Yirmisekizinci Mektûbun Yedinci Mes'elesi › Küllî Birkaç İnâyet‑i Rabbâniye’ye İşâretler › Üçüncü İşâret › 4. cümle (`tarihce-i-hayat/ikinci-kisim-barla-hayati/mesele-07/kulli-birkac-inayet-i-rabbaniyeye-isaretler/isaret-03/c004`) — Taftazânî'nin Telvih'teki kader bahsini Yirmi Altıncı Söz'le karşılaştırır

**Şerhu'l-Mevâkıf** (Seyyid Şerîf Cürcânî): 5

- havale · müellif · Muhakemat › Birinci Makale › Birinci Mes'ele › 2. cümle (`muhakemat/makale-01/mesele-01/c002`) — Arzın küreviyetinde şüphesi olanı Makâsıd ve Mevâkıf'a gönderir
- havale · müellif · Sözler › Otuzüçüncü Söz › Otuzuncu Pencere › 5. cümle (`sozler/33/pencere-30/c005`) — Tafsilat için Şerhu'l-Mevâkıf ve Şerhu'l-Makâsıd'a gönderir
- nakil · müellif · Sözler › Otuzikinci Söz › İkinci Mevkıf › Üçüncü Maksad › İkinci Şık Suâl ve Cevabı › İkinci Remiz › 1. cümle (`sozler/32/mevkif-02/maksad-03/ikinci-sik-sual-ve-cevabi/remiz-02/c001`) — Muhabbetin sebeplerine dair Şerhü'l-Mevâkıf'tan nakil
- nakil · müellif · Sözler › Otuzikinci Söz › İkinci Mevkıf › Üçüncü Maksad › İkinci Şık Suâl ve Cevabı › İkinci Remiz › 1. cümle (`sozler/32/mevkif-02/maksad-03/ikinci-sik-sual-ve-cevabi/remiz-02/c001`) — Seyyid Şerif'in muhabbet sebepleri tarifini aktarır
- anma · talebe · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › 62. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/c062`) — Günde iki yüz sahife okuduğu kitaplar arasında anılır

**İbn Teymiyye ve İbnü'l-Kayyim'in eserleri (adı verilmez)** (İbn Teymiyye, İbnü'l-Kayyim): 4

- değerlendirme · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Ehl‑i Sünnet ve'l-Cemâat, Sahabeler zamanındaki fitnelerden bahis açmayı men etmişler › 21. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/151/c021`) — Eserlerinin hocalar elinde bid'a ve evliya aleyhine kullanıldığını değerlendiriyor.
- değerlendirme · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Ehl‑i Sünnet ve'l-Cemâat, Sahabeler zamanındaki fitnelerden bahis açmayı men etmişler › 21. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/151/c021`) — Eserlerinin hocalar elinde bid'a ve evliya aleyhine kullanıldığını değerlendiriyor.
- değerlendirme · müellif · Tarihçe-i Hayat › Altıncı Kısım Emirdağı Hayatı › Ehl‑i Sünnet ve’l-Cemaat, Sahabeler zamanındaki fitnelerden bahis açmayı men etmişler › 23. cümle (`tarihce-i-hayat/altinci-kisim-emirdagi-hayati/ehl-i-sunnet-vel-cemaat-sahabeler-zamanindaki/c023`) — Eserleri nitelenip hocalar üzerindeki etkisi eleştiriliyor.
- değerlendirme · müellif · Tarihçe-i Hayat › Altıncı Kısım Emirdağı Hayatı › Ehl‑i Sünnet ve’l-Cemaat, Sahabeler zamanındaki fitnelerden bahis açmayı men etmişler › 23. cümle (`tarihce-i-hayat/altinci-kisim-emirdagi-hayati/ehl-i-sunnet-vel-cemaat-sahabeler-zamanindaki/c023`) — Eserleri nitelenip hocalar üzerindeki etkisi eleştiriliyor.

**Cem'u'l-Cevâmi' (usûl)** (Tâceddîn es-Sübkî): 3

- anma · talebe · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › 62. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/c062`) — Günde iki yüz sahife mütalaa ettiği kitaplar arasında
- anma · talebe · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › O Zamanki Hayatına Kısa Bir Bakış › 50. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/o-zamanki-hayatina-kisa-bir/c050`) — Cem'ül-Cevâmi'yi bir haftada ezberlemesi
- anma · talebe · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › O Zamanki Hayatına Kısa Bir Bakış › 51. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/o-zamanki-hayatina-kisa-bir/c051`) — Molla Fethullah'ın kitabın üzerine yazdığı söz

**Şerhu'l-Makāsıd** (Teftâzânî): 3

- havale · müellif · Muhakemat › Birinci Makale › Birinci Mes'ele › 2. cümle (`muhakemat/makale-01/mesele-01/c002`) — Arzın küreviyetinde şüphesi olanı Makâsıd ve Mevâkıf'a gönderir
- havale · müellif · Sözler › Otuzüçüncü Söz › Otuzuncu Pencere › 5. cümle (`sozler/33/pencere-30/c005`) — Tafsilat için Şerhu'l-Mevâkıf ve Şerhu'l-Makâsıd'a gönderir
- nakil · müellif · Barla Lahikası › Mektûbat’ın Üçüncü Kısmı › Hulûsî Bey’in sorularına cevap olarak yazılmış bir fıkradır › 11. cümle (`barla-lahikasi/kisim-03/213/c011`) — Teftâzânî'nin kanun-u emrin mahlukluğu hükmünü aktarır

**Seyyid Şerîf (eser adı anılmadan)** (Seyyid Şerîf Cürcânî): 2

- nakil · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Ehl‑i Sünnet ve'l-Cemâat, Sahabeler zamanındaki fitnelerden bahis açmayı men etmişler › 47. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/151/c047`) — Yezid'e lanet meselesinde Seyyid Şerif'in görüşünü nakleder
- nakil · müellif · Tarihçe-i Hayat › Altıncı Kısım Emirdağı Hayatı › Ehl‑i Sünnet ve’l-Cemaat, Sahabeler zamanındaki fitnelerden bahis açmayı men etmişler › 49. cümle (`tarihce-i-hayat/altinci-kisim-emirdagi-hayati/ehl-i-sunnet-vel-cemaat-sahabeler-zamanindaki/c049`) — Yezid'e lanet meselesinde Seyyid Şerif'in görüşünü nakleder

**el-Fıkhu'l-Ekber** (Ebû Hanîfe): 1

- değerlendirme · müellif · Sünuhat › Kur'ân’ın Hâkimiyet‑i Mutlakası › 28. cümle (`sunuhat/kuranin-hakimiyet-i-mutlakasi/c028`) — Fıkh-ı Ekber'i Kur'ân'ı gösteren selef kitabına örnek verir

**İzhârü'l-Hak** (Rahmetullah el-Hindî): 1

- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › İkinci Hüccet › 5. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-02/c005`) — Rahmetullah Hindî'nin tahrifatı isbatını anar; eser adı yok

**Metâli' (hangisi olduğu yazılmaz)** (—): 1

- anma · talebe · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › Genç Said’in Serbestiyet ve Hürriyet Aşkı ve Kırk Kadar Kitabı Ezberlemesi › 9. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/genc-saidin-serbestiyet-ve-hurriyet/c009`) — Ezberlediği kelâm eserleri arasında sayılıyor; hangi Metâli' olduğu belirtilmemiş.

### Tasavvuf

**Fütûhu'l-Gayb** (Abdülkādir-i Geylânî): 20

- nakil · müellif · Sikke-i Tasdik-i Gaybî › Sekizinci Lem'a › Mühim Bir İhbar‑ı Gaybî › Beşinci Vecih › 19. cümle (`sikke-i-tasdik-i-gaybi/lema-08/muhim-bir-ihbar-i-gaybi/vecih-05/c019`) — Fütûhu'l-Gayb'daki 'Yâ gulâm' hitabını kendine uygular
- değerlendirme · talebe · Şualar › Onbeşinci Şuâ › Takrizler › Risale‑i Nur Nedir? Risale-i Nur ve Tercümânı Ne Mâhiyettedirler? › 12. cümle (`sualar/15/takrizler/risale-i-nur-nedir-risale-i-nur/c012`) — Fütûhu'l-Gayb'ı ilhâmî eserler nev'inden sayar
- değerlendirme · talebe · Tarihçe-i Hayat › Yedinci Kısım Afyon Hayatı › Risale‑i Nur Nedir? Bediüzzaman Kimdir? › 14. cümle (`tarihce-i-hayat/yedinci-kisim-afyon-hayati/risale-i-nur-nedir-bediuzzaman-kimdir/c014`) — Fütûhu'l-Gayb'ı ilhâmî eserler nev'inden sayar
- tefe'ül · talebe · Barla Lahikası › Yirmiyedinci Mektûb’un Üçüncü Kısmı ve Üçüncü Zeylin Nihâyetidir › Nadire‑i cihan, hadim-i Kur’ân Said Nursî (ra) hakkında hissiyatımdan binden birini beyan ediyorum › 27. cümle (`barla-lahikasi/yirmiyedinci-mektubun-ucuncu-kismi-ve/133/c027`) — Fütûhu'l-Gayb ile tefe'ül ve çıkan ibare
- tefe'ül · talebe · Barla Lahikası › Yirmiyedinci Mektûb’un Üçüncü Kısmı ve Üçüncü Zeylin Nihâyetidir › Nadire‑i cihan, hadim-i Kur’ân Said Nursî (ra) hakkında hissiyatımdan binden birini beyan ediyorum › 27. cümle (`barla-lahikasi/yirmiyedinci-mektubun-ucuncu-kismi-ve/133/c027`) — Fütûhu'l-Gayb'ı tefe'ülen açınca çıkan ibareyi anlatır
- tefe'ül · müellif · Mektubat › Yirmisekizinci Mektûb › Üçüncü Mes'ele Olan Üçüncü Risale › Üçüncü Nokta › 5. cümle (`mektubat/28/ucuncu-mesele-olan-ucuncu-risale/nokta-03/c005`) — Fütûhu'l-Gayb ile tefe'ül eder
- tefe'ül · müellif · Mektubat › Yirmisekizinci Mektûb › Üçüncü Mes'ele Olan Üçüncü Risale › Üçüncü Nokta › 5. cümle (`mektubat/28/ucuncu-mesele-olan-ucuncu-risale/nokta-03/c005`) — Fütûhu'l-Gayb ile tefe'ül ettiğini anlatır
- tefe'ül · müellif · Sikke-i Tasdik-i Gaybî › Sekizinci Lem'a › Mühim Bir İhbar‑ı Gaybî › Beşinci Vecih › 10. cümle (`sikke-i-tasdik-i-gaybi/lema-08/muhim-bir-ihbar-i-gaybi/vecih-05/c010`) — Fütûhu'l-Gayb'ın tefe'ülünde çıkan fıkrayı anlatır
- tefe'ül · müellif · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › Dâru'l‑Hikmet’te İken Bir İnkılâb‑ı Rûhî Geçirmesi › 6. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/darul-hikmette-iken-bir-inkilab-i-ruhi/c006`) — Fütûhu'l-Gayb ile tefe'ül eder
- tefe'ül · müellif · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › Dâru'l‑Hikmet’te İken Bir İnkılâb‑ı Rûhî Geçirmesi › 6. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/darul-hikmette-iken-bir-inkilab-i-ruhi/c006`) — Fütûhu'l-Gayb ile tefe'ül ettiğini anlatır
- tefe'ül · talebe · Tarihçe-i Hayat › İkinci Kısım Barla Hayatı › Nadire‑i cihan, hadim-i Kur’ân Said Nursî (ra) hakkında hissiyatımdan binden birini beyan ediyorum › 29. cümle (`tarihce-i-hayat/ikinci-kisim-barla-hayati/nadire-i-cihan-hadim-i-kuran-said/c029`) — Fütûhu'l-Gayb'ı tefe'ülen açması ve çıkan ibare
- tefe'ül · talebe · Tarihçe-i Hayat › İkinci Kısım Barla Hayatı › Nadire‑i cihan, hadim-i Kur’ân Said Nursî (ra) hakkında hissiyatımdan binden birini beyan ediyorum › 29. cümle (`tarihce-i-hayat/ikinci-kisim-barla-hayati/nadire-i-cihan-hadim-i-kuran-said/c029`) — Fütûhu'l-Gayb'ı tefe'ülen açınca çıkan ibareyi anlatır
- anma · müellif · Lem'alar › Yirmialtıncı Lem'a › Dokuzuncu Ricâ › 30. cümle (`lemalar/26/rica-09/c030`) — Fütûhu'l-Gayb'ın gözünü açtırdığını anlatır
- anma · müellif · Lem'alar › Yirmialtıncı Lem'a › Dokuzuncu Ricâ › 30. cümle (`lemalar/26/rica-09/c030`) — Fütûhu'l-Gayb'ın gözünü açtırdığını söyler
- anma · müellif · Lem'alar › Yirmialtıncı Lem'a › Onuncu Ricâ › 43. cümle (`lemalar/26/rica-10/c043`) — Fütûhu'l-Gayb ile Gavs'ın ona üstad ve mürşid olduğunu söyler
- anma · müellif · Sikke-i Tasdik-i Gaybî › Sekizinci Lem'a › Gavs, birkaç yerde yine, işârî bir tarzda haber veriyor › 7. cümle (`sikke-i-tasdik-i-gaybi/lema-08/gavs-birkac-yerde-yine-isari/c007`) — Fütûhu'l-Gayb ile buhranı geçirdiğini anlatır
- anma · müellif · Sikke-i Tasdik-i Gaybî › Sekizinci Lem'a › Mühim Bir İhbar‑ı Gaybî › Beşinci Vecih › 8. cümle (`sikke-i-tasdik-i-gaybi/lema-08/muhim-bir-ihbar-i-gaybi/vecih-05/c008`) — Fütûhu'l-Gayb'ın tesadüfen eline geçtiğini anlatır
- anma · müellif · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › Esâretten Avdetinden Sonraki İstanbul Hayatına Dair Kaleme Aldığı Bir Parçadır › Onuncu Ricâ › 43. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/esaretten-avdetinden-sonraki-istanbul-hayatina/rica-10/c043`) — Fütûhu'l-Gayb ile Gavs'ın ona üstad ve mürşid olduğunu söyler
- anma · müellif · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › Yirmialtıncı Lem'anın Dokuzuncu Ricâsından Bir Kısım › 30. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/yirmialtinci-lemanin-dokuzuncu-ricasindan-bir/c030`) — Fütûhu'l-Gayb'ın gözünü açtırdığını anlatır (Lem'a'dan)
- anma · müellif · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › Yirmialtıncı Lem'anın Dokuzuncu Ricâsından Bir Kısım › 30. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/yirmialtinci-lemanin-dokuzuncu-ricasindan-bir/c030`) — Fütûhu'l-Gayb'ın gözünü açtırdığını söyler

**İmâm-ı Rabbânî (eser adı anılmadan)** (İmâm-ı Rabbânî): 20

- nakil · müellif · Barla Lahikası › Mektûbat’ın Üçüncü Kısmı › Maşaallah Yirminci Mektub'un kıymetini güzel anlamışsınız ve güzel de yazmışsınız › 8. cümle (`barla-lahikasi/kisim-03/224/c008`) — Âhirzamanda ilm-i kelamı beyan edecek zat haberini aktarır
- nakil · müellif · Kastamonu Lahikası › 106‑164 Mektuplar › Kendi kusurunu görmek, nefis ve enaniyeti bırakmak gerektir › Üçüncü Mes'ele › 7. cümle (`kastamonu-lahikasi/106-164-mektuplar/141/mesele-03/c007`) — Mecâzî nefs-i emmâreden haber verdiğini aktarır
- nakil · müellif · Kastamonu Lahikası › 106‑164 Mektuplar › Mesleğimizde ihlâs‑ı tammeden sonra en büyük esas sebat ve metanettir › 33. cümle (`kastamonu-lahikasi/106-164-mektuplar/153/c033`) — 'Bid'a olan yerlere girmeyiniz' sözünü aktarıp yorumlar
- nakil · müellif · Lem'alar › Onbirinci Lem'a › İkinci Nükte › 1. cümle (`lemalar/11/nukte-02/c001`) — Sünnete ittiba eden evliya hakkındaki sözünü aktarır
- nakil · müellif · Lem'alar › Onbirinci Lem'a › Dokuzuncu Nükte › 12. cümle (`lemalar/11/nukte-09/c012`) — Sünnetten mervî kelimatın nurluluğu sözünü aktarır
- nakil · müellif · Lem'alar › Otuzuncu Lem'a › Otuzuncu Lem'anın Altıncı Nüktesi › 12. cümle (`lemalar/30/nukte-06/c012`) — Mesele-i imaniyenin inkişafı sözünü aktarır
- nakil · talebe · Lem'alar › Fihrist › Onbirinci Lem'a › Üçüncü Nükte › 2. cümle (`lemalar/fihrist/lema-11/nukte-03/c002`) — Fihrist: Sünnet hakkındaki hükmünü tasdik ettiğini söyler
- nakil · müellif · Mektubat › Yirmisekizinci Mektûb › Sekizinci Risale Olan Sekizinci Mes'ele › Altıncı Nükte › 5. cümle (`mektubat/28/mesele-08/nukte-06/c005`) — Hindistan'a gelen nebiler hakkındaki sözünü aktarır
- nakil · müellif · Mektubat › Yirmisekizinci Mektûb › Üçüncü Mes'ele Olan Üçüncü Risale › İkinci Nokta › 1. cümle (`mektubat/28/ucuncu-mesele-olan-ucuncu-risale/nokta-02/c001`) — Hakâik-i imaniyenin inkişafı hakkındaki sözünü aktarır
- nakil · müellif · Mektubat › Sekizinci Mektûb › 13. cümle (`mektubat/8/c013`) — Hz. Yûsuf'a muhabbet hakkındaki sözünü aktarır
- nakil · müellif · Mesnevî-i Nuriye › Katre › Katre’nin Zeyli › Remz › 20. cümle (`mesnevi-i-nuriye/katre/zeyl/remz-3/c020`) — İmâm-ı Rabbânî'nin sözünü aktarır
- nakil · müellif · Mesnevî-i Nuriye › Mukaddime › Birinci Nokta › 7. cümle (`mesnevi-i-nuriye/mukaddime/nokta-01/c007`) — İmâm-ı Rabbânî'nin 'tevhid-i kıble et' sözünü aktarır
- nakil · müellif · Sözler › Yirmibeşinci Söz › Birinci Şu'le › Üçüncü Şuâ › Birinci Cilve › İkinci Şavk › 5. cümle (`sozler/25/sule-01/sua-03/cilve-01/savk-02/c005`) — Mukattaâttan gaybî haberler gördüğünü aktarır
- nakil · müellif · Sözler › Otuzbirinci Söz › İkinci Esâs › İkinci Temsîl › 132. cümle (`sozler/31/esas-02/temsil-02/c132`) — İhbarât-ı sâdıkasıyla ruhânî urûcunu aktarır
- nakil · müellif · Sözler › Otuzikinci Söz › Üçüncü Mevkıf › İkinci Noktanın İkinci Mebhası › Meşrû Muhabbetlerin Dâr‑ı Âhiretteki Neticeleri › Yedinci İşâret › 2. cümle (`sozler/32/mevkif-03/mebhas-02/mesru-muhabbetlerin-dar-i-ahiretteki-neticeleri/isaret-07/c002`) — Letâif-i Cennet hakkındaki sözünü aktarır
- nakil · talebe · Şualar › Fihrist › Yedinci Şuâ › Âyetü'l‑Kübrâ › İkinci Makam › İkinci Bâb › İkinci Menzil › İkinci sır › 4. cümle (`sualar/fihrist/sua-07/ayetul-kubra/makam-02/bab-02/menzil-02/sir-02/c004`) — Fihrist: 'tarikatların müntehası' sözünün derc edildiğini söyler
- nakil · müellif · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › Bediüzzaman, Yanında Başka Kitaplar Bulundurmuyordu › 7. cümle › Hâşiye › 8. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/bediuzzaman-yaninda-baska-kitaplar-bulundurmuyordu/c007/h1/c008`) — 'Tevhid-i kıble et' sözünü aktarır
- değerlendirme · talebe · İşaratü'l-İ'caz › Birkaç Defa Berâet Kazanan Risale‑i Nur’un Birkaç Vilâyette Haksız Müsâderesine Dair, Nur’un Yüksek Bir Talebesinin Mahkemesindeki Müdafaasından Bir Parçadır › 46. cümle (`isaratul-icaz/birkac-defa-beraet-kazanan-risale-i/c046`) — İmâm-ı Rabbânî'nin eserlerini işârî tefsir sayar
- değerlendirme · müellif · Mektubat › Sekizinci Mektûb › 8. cümle (`mektubat/8/c008`) — Yakub'un hissiyatı meselesinde İmâm-ı Rabbânî'ye muhalefet eder
- anma · müellif · Kastamonu Lahikası › 1‑105 Mektuplar › Zaman cemaat zamanıdır › 22. cümle (`kastamonu-lahikasi/1-105-mektuplar/2/c022`) — Eserleriyle hadisi fiilen tasdik ettiklerini anar

**Geylânî (eser adı anılmadan)** (Abdülkādir-i Geylânî): 16

- nakil · müellif · Barla Lahikası › Mektûbat’ın Üçüncü Kısmı › Size âlem‑i nurdan bahisler açma arzusu vardı. Maalesef bir hâdise zulmet âleminden bahsetmeye beni mecbur ediyor › Birinci kısım › 6. cümle (`barla-lahikasi/kisim-03/225/kisim-01/c006`) — Kasidedeki 'inâyet gözü altında' sözünü anar
- nakil · müellif · Barla Lahikası › Mektûbat’ın Üçüncü Kısmı › İki Ramazan içinde bir kefaret kâfidir, müteaddit vakıalara bir kefaret kifayet eder; çünkü tedahül var › 20. cümle (`barla-lahikasi/kisim-03/273/c020`) — Bekir Bey adını Gavs'ın tabiriyle anar
- nakil · talebe · Emirdağ Lahikası › Emirdağ Lâhikası 2 › Umum dostlarıma ve Nur kardeşlerime bu vasiyeti ilân ediyorum › 22. cümle (`emirdag-lahikasi/emirdag-lahikasi-2/365/c022`) — Kerâmet-i gaybiyesindeki 'teîşu saîden' fıkrasını nakleder
- nakil · talebe · Emirdağ Lahikası › Emirdağ Lâhikası 2 › Umum dostlarıma ve Nur kardeşlerime bu vasiyeti ilân ediyorum › 24. cümle (`emirdag-lahikasi/emirdag-lahikasi-2/365/c024`) — Önceki fıkradaki ihbarın Üstadda gerçekleştiğini söyler
- nakil · talebe · Kastamonu Lahikası › 106‑164 Mektuplar › Gavs‑ı Azam’ın da müjdesi ile Üstadımız inayet ve teshîle mazhardır › 1. cümle (`kastamonu-lahikasi/106-164-mektuplar/131/c001`) — Kasidesinden 'fe-inneke mahrûsun' fıkrasını delil eder
- nakil · müellif · Lem'alar › Yirmi Dokuzuncu Lem'a › اَلْبَابُ الرَّابِعُ › اَلْفَصْلُ الثَّانِي مِنَ الْبَابِ الرَّابِعِ › 1. cümle (`lemalar/29/bab-04/fasil-02/c001`) — Sabah virdindeki temcidi kendi tefekkür silsilesine çekirdek yapar
- nakil · müellif · Lem'alar › Yirmi Dokuzuncu Lem'a › اَلْبَابُ الرَّابِعُ › اَلْفَصْلُ الثَّانِي مِنَ الْبَابِ الرَّابِعِ › 6. cümle › Hâşiye › 8. cümle (`lemalar/29/bab-04/fasil-02/c006/h1/c008`) — Tercüme hâşiyesi: sabah virdi tefekküre çekirdek olmuş
- nakil · müellif · Sikke-i Tasdik-i Gaybî › Sekizinci Lem'a › Gavs, birkaç yerde yine, işârî bir tarzda haber veriyor › 40. cümle (`sikke-i-tasdik-i-gaybi/lema-08/gavs-birkac-yerde-yine-isari/c040`) — Kasidesinde iki yerde Said'den sarâhaten haber verdiğini söyler
- değerlendirme · talebe · İşaratü'l-İ'caz › Birkaç Defa Berâet Kazanan Risale‑i Nur’un Birkaç Vilâyette Haksız Müsâderesine Dair, Nur’un Yüksek Bir Talebesinin Mahkemesindeki Müdafaasından Bir Parçadır › 46. cümle (`isaratul-icaz/birkac-defa-beraet-kazanan-risale-i/c046`) — Geylânî'nin eserlerini işârî/manevî tefsir sayar
- değerlendirme · müellif · Kastamonu Lahikası › 1‑105 Mektuplar › Zaman cemaat zamanıdır › 22. cümle (`kastamonu-lahikasi/1-105-mektuplar/2/c022`) — Eserleriyle hadisi fiilen tasdik ettiklerini söyler
- değerlendirme · müellif · Sikke-i Tasdik-i Gaybî › Sekizinci Lem'a › Şu Kerâmet‑i Gavsiye Münâsebetiyle “üç Nokta” Beyân Edilecek › İkinci Nokta › 5. cümle (`sikke-i-tasdik-i-gaybi/lema-08/su-keramet-i-gavsiye-munasebetiyle-uc/nokta-02/c005`) — Kasidesindeki sözleri hangi makamdan söylediğini izah eder
- anma · talebe · Barla Lahikası › Mektûbat’ın Üçüncü Kısmı › Bu hakikatler gösterilen dokuz‑on delil ile ispat edildikten sonra, bu risale-i şerife ile ilân ediliyordu › 2. cümle (`barla-lahikasi/kisim-03/174/c002`) — Kasidesindeki ihbarları içeren risaleyi okuduğunu söyler
- anma · talebe · Barla Lahikası › Mektûbat’ın Üçüncü Kısmı › İstidadımın fevkinde şöyle bir kaç beyit kalbime ve kalemime geldi. Müşfik Üstadımın aflarına istinaden yazıyorum › 4. cümle (`barla-lahikasi/kisim-03/178/c004`) — Eserlerindeki gaybî ihbarın kendisini etkilediğini söyler
- anma · talebe · Nur'un İlk Kapısı › Ankara Üniversitesinde Okunan Bir Konferanstır › 28. cümle (`nurun-ilk-kapisi/ankara-universitesinde-okunan-bir-konferanstir/c028`) — Eserlerinin gençlikçe bilinmediğini söyler
- anma · başka · Şualar › Birinci Şuâ › İkinci Suâl › 1. cümle (`sualar/1/sual-02/c001`) — Kasidelerinden şâhid gösterildiği itirazı nakledilir
- anma · talebe · Tarihçe-i Hayat › İkinci Kısım Barla Hayatı › Üstad’ın Barla’da İkameti › 12. cümle (`tarihce-i-hayat/ikinci-kisim-barla-hayati/ustadin-barlada-ikameti/c012`) — Geceleri okuduğu münâcât ve hizbler arasında

**İbn Arabî (eser adı anılmadan)** (İbn Arabî): 16

- nakil · müellif · İşaratü'l-İ'caz › Sûre‑i Fâtiha › El‑Hamdü «اَلْحَمْدُ» › 17. cümle (`isaratul-icaz/sure-i-fatiha/el-hamdu/c017`) — Kenz-i mahfî hadisinin Muhyiddin'in izahını aktarır
- nakil · müellif · Kastamonu Lahikası › 106‑164 Mektuplar › Risale‑i Nur’a işaret eden Otuz Üçüncü Ayetin bir zeyli ve lâhikası › 29. cümle (`kastamonu-lahikasi/106-164-mektuplar/110/c029`) — Muhyiddin'in işârî tefsirlerindeki Mûsâ-Firavun yorumunu aktarır
- nakil · müellif · Lem'alar › Dokuzuncu Lem'a › İkinci Suâl › 2. cümle (`lemalar/9/sual-02/c002`) — Muhyiddin'in ruh hakkındaki sözünü soru olarak aktarır
- nakil · müellif · Mektubat › Yirminci Mektûb › İkinci Makam › Onuncu Kelime › Dördüncüsü › Birinci Sır › 14. cümle (`mektubat/20/makam-02/kelime-10/nukte-04/sir-01/c014`) — Muhyiddin'in 'lâ mevcûde illâ Hû' sözünü aktarır
- nakil · müellif · Sözler › Yirmibeşinci Söz › Birinci Şu'le › Üçüncü Şuâ › Birinci Cilve › İkinci Şavk › 4. cümle (`sozler/25/sule-01/sua-03/cilve-01/savk-02/c004`) — Muhyiddin'in Rum Sûresi'nde gaybî haberler bulduğunu aktarır
- değerlendirme · müellif · Âsâr-ı Bediiyye › Lemeât › Üçüncü cümle › 112. cümle (`asar-i-bediiyye/lemeat/cumle-03/c112`) — Muhyiddin'in işârât ve şatahatının hücuma sebep olduğunu söyler
- değerlendirme · talebe · Barla Lahikası › Mektûbat’ın Üçüncü Kısmı › Hulûsî Bey’in suallerine verilen cevaplara ait cihandeğer kıymetli, nurlu, feyizli sözlerinizi iki gün evvel aldım › 5. cümle (`barla-lahikasi/kisim-03/191/c005`) — Hulûsi: Muhyiddin'in hatası ve kitaplarının mühdî olmaması izahını över
- değerlendirme · talebe · Barla Lahikası › Mektûbat’ın Üçüncü Kısmı › Muhyiddin‑i Arabî’nin meşrebini izah edip, noksaniyetini beyan eden nurlu beyanatınızdan çok istifade ettim › 1. cümle (`barla-lahikasi/kisim-03/196/c001`) — Hulûsi: Muhyiddin meşrebinin noksanını izah eden dersten istifade
- değerlendirme · talebe · İşaratü'l-İ'caz › Birkaç Defa Berâet Kazanan Risale‑i Nur’un Birkaç Vilâyette Haksız Müsâderesine Dair, Nur’un Yüksek Bir Talebesinin Mahkemesindeki Müdafaasından Bir Parçadır › 46. cümle (`isaratul-icaz/birkac-defa-beraet-kazanan-risale-i/c046`) — Muhyiddin'in eserlerini işârî tefsir sayar
- değerlendirme · müellif · Lem'alar › Yirmi Sekizinci Lem'a › Yedinci Nükte › Bir Suâle Cevab › 13. cümle (`lemalar/28/nukte-07/bir-suale-cevab/c013`) — Muhyiddin'in Ehl-i Sünnete muhalif meselelerine taraftarlığı eleştirir
- değerlendirme · müellif · Lem'alar › Dokuzuncu Lem'a › İkinci Suâl › 3. cümle (`lemalar/9/sual-02/c003`) — Muhyiddin'in büyüklüğünü anıp sözüne cevap vermeye girişir
- değerlendirme · müellif · Lem'alar › Dokuzuncu Lem'a › İkinci Suâl › 46. cümle (`lemalar/9/sual-02/c046`) — Muhyiddin meşrebinin vahdet-i vücud yanlışını eleştirir
- değerlendirme · talebe · Lem'alar › Fihrist › Dokuzuncu Lem'a › Birinci suâl › 1. cümle (`lemalar/fihrist/lema-09/sual-01/c001`) — Fihrist: Muhyiddin'in ruh hakkındaki sözüne cevabı özetler
- değerlendirme · talebe · Lem'alar › Fihrist › Dokuzuncu Lem'a › Birinci suâl › 4. cümle (`lemalar/fihrist/lema-09/sual-01/c004`) — Fihrist: Muhyiddin'in vahdet-i vücuda gitme sebeplerini açıklar
- değerlendirme · talebe · Lem'alar › Fihrist › Dokuzuncu Lem'a › Birinci suâl › 5. cümle (`lemalar/fihrist/lema-09/sual-01/c005`) — Fihrist: risaleyi Muhyiddin'in eserleriyle ülfet edenlere ilaç sayar
- değerlendirme · talebe · Lem'alar › Fihrist › Yirmisekizinci Lem'a › Yedinci Nükte › 1. cümle (`lemalar/fihrist/lema-28/nukte-07/c001`) — Fihrist: Muhyiddin'in her kitabında mühdî olmadığını söyler

**Gazâlî (eser adı anılmadan)** (Gazâlî): 11

- nakil · müellif · Kastamonu Lahikası › 106‑164 Mektuplar › Riyaya dair yazılan Üç Nokta › 6. cümle (`kastamonu-lahikasi/106-164-mektuplar/109/c006`) — Şeâirle ilgili ibadetin izhârı daha sevaplı görüşünü dayanak yapar
- nakil · talebe · Sikke-i Tasdik-i Gaybî › On Sekizinci Lem'a › Üçüncü Emâre › 8. cümle (`sikke-i-tasdik-i-gaybi/lema-18/emare-03/c008`) — Altı ismi Gazâlî'den ders alıp vird edinmesi
- nakil · müellif · Şualar › İkinci Şuâ › Üçüncü Makam › İkinci Alâmet ve Hüccet Ki › 14. cümle (`sualar/2/makam-03/ikinci-alamet-ve-huccet-ki/c014`) — 'Leyse fi'l-imkân ebdau mimmâ kân' sözünü nakleder
- nakil · müellif · Şualar › Sekizinci Şuâ › Üçüncü Remz › Üçüncüsü › 26. cümle (`sualar/8/remiz-03/sir-03/c026`) — Celcelûtiye'nin yazılışına dair Gazâlî'nin sözünü nakleder
- nakil · müellif · Şualar › Sekizinci Şuâ › Üçüncü Remz › Üçüncüsü › 29. cümle (`sualar/8/remiz-03/sir-03/c029`) — Celcelûtiye'nin hazine olduğuna dair sözünü nakleder
- değerlendirme · talebe · İşaratü'l-İ'caz › Birkaç Defa Berâet Kazanan Risale‑i Nur’un Birkaç Vilâyette Haksız Müsâderesine Dair, Nur’un Yüksek Bir Talebesinin Mahkemesindeki Müdafaasından Bir Parçadır › 46. cümle (`isaratul-icaz/birkac-defa-beraet-kazanan-risale-i/c046`) — Gazâlî'nin eserlerini işârî/manevî tefsir sayar
- değerlendirme · müellif · Kastamonu Lahikası › 1‑105 Mektuplar › Zaman cemaat zamanıdır › 22. cümle (`kastamonu-lahikasi/1-105-mektuplar/2/c022`) — Eserleriyle hadisi fiilen tasdik ettiklerini söyler
- değerlendirme · müellif · Şualar › Sekizinci Şuâ › Dördüncü Remz › 32. cümle (`sualar/8/remiz-04/c032`) — Gazâlî'nin Süryânî kelimeleri tam izah etmediğini söyler
- anma · başka · Kastamonu Lahikası › 106‑164 Mektuplar › “Said yanında başka kitapları bulundurmuyor, demek onları beğenmiyor” ithamına verilen cevap › 11. cümle (`kastamonu-lahikasi/106-164-mektuplar/108/c011`) — Gazâlî'nin eserlerini yanında tutmadığı itirazı aktarılır
- anma · talebe · Nur'un İlk Kapısı › Ankara Üniversitesinde Okunan Bir Konferanstır › 28. cümle (`nurun-ilk-kapisi/ankara-universitesinde-okunan-bir-konferanstir/c028`) — Eserlerinin gençlikçe bilinmediğini söyler
- anma · talebe · Tarihçe-i Hayat › Sekizinci Kısım Isparta Hayatı › Nurlara Olan Taarruzların Bir Zararı Olsa Yirmi Faydası Vardır › 163. cümle (`tarihce-i-hayat/sekizinci-kisim-isparta-hayati/nurlara-olan-taarruzlarin-bir-zarari/c163`) — Gazâlî'nin eserlerini tetebbu eden âlimin sözünü tanıtır

**Mevlânâ (eser adı anılmadan)** (Mevlânâ): 9

- nakil · müellif · el-Mesnevî el-Arabî en-Nurî › قَطْرَةٌ › خَاتِمَةٌ › 3. cümle (`el-mesnevi-el-arabi/katre/hatime/c003`) — Mevlânâ'nın Farsça beytini kendi hâline uygular
- nakil · müellif · Mektubat › Altıncı Mektûb › 37. cümle (`mektubat/6/c037`) — Mevlânâ'nın nefsine dediği beyti aktarır
- nakil · müellif · Mektubat › Altıncı Mektûb › 51. cümle (`mektubat/6/c051`) — Mevlânâ'nın semâ hakkındaki beytini aktarır
- nakil · talebe · Mesnevî-i Nuriye › Fihrist › 8‑ Zerre › 14. cümle (`mesnevi-i-nuriye/fihrist/8-zerre/c014`) — Fihrist: risalenin Mevlânâ'nın bir beytiyle bittiğini söyler
- nakil · müellif · Şualar › İkinci Şuâ › Birinci Makam › Birinci Makamın Birinci Meyvesi › 19. cümle (`sualar/2/makam-01/meyve-01/c019`) — Mevlânâ'nın beytini tevhid sırrına delil getirir
- nakil · müellif · Tarihçe-i Hayat › İkinci Kısım Barla Hayatı › Altıncı Mektûb › 36. cümle (`tarihce-i-hayat/ikinci-kisim-barla-hayati/mektub-06/c036`) — Mevlânâ'nın nefsine dediği beyti aktarır
- nakil · müellif · Tarihçe-i Hayat › İkinci Kısım Barla Hayatı › Altıncı Mektûb › 50. cümle (`tarihce-i-hayat/ikinci-kisim-barla-hayati/mektub-06/c050`) — Mevlânâ'nın semâ hakkındaki beytini aktarır
- değerlendirme · talebe · Barla Lahikası › Kastamonu ve Emirdağı hayatında iken yazılan mektûblardır › Küçük Husrev Mehmed Feyzi’nin bir kasîdesi › 15. cümle › Hâşiye › 1. cümle (`barla-lahikasi/kastamonu-ve-emirdagi-hayatinda-iken/288/c015/h1/c001`) — Câmî'nin Mevlânâ ve kitabı hakkındaki övgü beytini aktarır
- anma · talebe · Nur'un İlk Kapısı › Ankara Üniversitesinde Okunan Bir Konferanstır › 28. cümle (`nurun-ilk-kapisi/ankara-universitesinde-okunan-bir-konferanstir/c028`) — Gençliğin Mevlânâ gibilerin eserlerini bilmediğini söyler

**Mesnevî** (Mevlânâ): 8

- değerlendirme · talebe · İşaratü'l-İ'caz › Birkaç Defa Berâet Kazanan Risale‑i Nur’un Birkaç Vilâyette Haksız Müsâderesine Dair, Nur’un Yüksek Bir Talebesinin Mahkemesindeki Müdafaasından Bir Parçadır › 47. cümle (`isaratul-icaz/birkac-defa-beraet-kazanan-risale-i/c047`) — Mesnevî'yi bir nevi manevî tefsir sayar
- değerlendirme · talebe · İşaratü'l-İ'caz › Birkaç Defa Berâet Kazanan Risale‑i Nur’un Birkaç Vilâyette Haksız Müsâderesine Dair, Nur’un Yüksek Bir Talebesinin Mahkemesindeki Müdafaasından Bir Parçadır › 47. cümle (`isaratul-icaz/birkac-defa-beraet-kazanan-risale-i/c047`) — Mesnevî'yi manevî tefsir sayıp Risale-i Nur'u o tarzın en yükseği der
- değerlendirme · müellif · Lem'alar › Yirmi Sekizinci Lem'a › On Dördüncü Nükte › 2. cümle (`lemalar/28/nukte-14/c002`) — Mesnevî'nin bir hakikatin aynası olduğunu, Risale-i Nur'u ona kıyaslar
- değerlendirme · belirsiz · Lem'alar › Fihrist › Yirmisekizinci Lem'a › On Dördüncü Nükte › 1. cümle (`lemalar/fihrist/lema-28/nukte-14/c001`) — Mesnevî'nin bir hakikatin aynası olduğunu, Risale-i Nur'u ona kıyaslar
- değerlendirme · belirsiz · Mesnevî-i Nuriye › Mukaddime › İkinci Nokta › 2. cümle (`mesnevi-i-nuriye/mukaddime/nokta-02/c002`) — Arabî Mesnevî'yi Mevlânâ'nın Mesnevî'sine benzetir
- değerlendirme · talebe · Şualar › Onbeşinci Şuâ › Takrizler › Risale‑i Nur Nedir? Risale-i Nur ve Tercümânı Ne Mâhiyettedirler? › 12. cümle (`sualar/15/takrizler/risale-i-nur-nedir-risale-i-nur/c012`) — Mesnevî'yi Peygamber'in manevî ilhamı olan eserler arasında sayar
- değerlendirme · talebe · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › Bediüzzaman, Yanında Başka Kitaplar Bulundurmuyordu › 7. cümle › Hâşiye › 16. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/bediuzzaman-yaninda-baska-kitaplar-bulundurmuyordu/c007/h1/c016`) — Arabî Mesnevî'yi Mevlânâ'nın Mesnevî'sine benzetir
- değerlendirme · talebe · Tarihçe-i Hayat › Yedinci Kısım Afyon Hayatı › Risale‑i Nur Nedir? Bediüzzaman Kimdir? › 14. cümle (`tarihce-i-hayat/yedinci-kisim-afyon-hayati/risale-i-nur-nedir-bediuzzaman-kimdir/c014`) — Mesnevî'yi Peygamber'in manevî ilhamı olan eserler arasında sayar

**Mektûbât** (İmâm-ı Rabbânî): 6

- nakil · müellif · el-Mesnevî el-Arabî en-Nurî › تَرْجَمَةُ المُقَدِّمَةِ التُّرْكِيَّةِ بِالْعَرَبِيَّةِ › النُّقْطَةُ الْأُولَى › 4. cümle (`el-mesnevi-el-arabi/mukaddime/nokta-01/c004`) — Mektûbât'taki 'tevhid-i kıble' emrini aktarır
- nakil · müellif · Mektubat › Beşinci Mektûb › 3. cümle (`mektubat/5/c003`) — Mektûbât'ından hakâik-i imaniye sözünü aktarır
- tefe'ül · müellif · Mektubat › Yirmisekizinci Mektûb › Üçüncü Mes'ele Olan Üçüncü Risale › Üçüncü Nokta › 22. cümle (`mektubat/28/ucuncu-mesele-olan-ucuncu-risale/nokta-03/c022`) — Mektûbât'ı eline alıp tefe'ül ettiğini anlatır
- tefe'ül · müellif · Mektubat › Yirmisekizinci Mektûb › Üçüncü Mes'ele Olan Üçüncü Risale › Üçüncü Nokta › 22. cümle (`mektubat/28/ucuncu-mesele-olan-ucuncu-risale/nokta-03/c022`) — Tefe'ül için İmam-ı Rabbânî'nin Mektubat'ını eline aldığını anlatır
- tefe'ül · müellif · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › Dâru'l‑Hikmet’te İken Bir İnkılâb‑ı Rûhî Geçirmesi › 22. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/darul-hikmette-iken-bir-inkilab-i-ruhi/c022`) — Mektûbât'ı eline alıp tefe'ül ettiğini anlatır
- tefe'ül · müellif · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › Dâru'l‑Hikmet’te İken Bir İnkılâb‑ı Rûhî Geçirmesi › 22. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/darul-hikmette-iken-bir-inkilab-i-ruhi/c022`) — Tefe'ül için İmam-ı Rabbânî'nin Mektubat'ını eline aldığını anlatır

**el-Fütûhâtü'l-Mekkiyye** (İbn Arabî): 5

- havale · müellif · İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 3. Âyetin Tefsiri › 42. cümle (`isaratul-icaz-arabi/sure-i-bakara/3/c042`) — Namaz rükünlerinin esrarını şerheden eser olarak Fütuhat'ı gösterir
- havale · müellif · İşaratü'l-İ'caz › Sûre‑i Bakara › 3. Âyetin Tefsiri › Îmân‑ı Bilgayb › 65. cümle (`isaratul-icaz/sure-i-bakara/3/iman-i-bilgayb/c065`) — Namaz rükünlerinin esrarını şerheden eser olarak Fütuhat'ı gösterir
- nakil · müellif · Mektubat › Onsekizinci Mektûb › Birinci Mes'ele‑i Mühimme › 1. cümle (`mektubat/18/birinci-mesele-i-muhimme/c001`) — Fütûhât'taki Meşmeşiye ve arz-ı beyzâ sözlerini soruya konu eder
- nakil · müellif · Mektubat › Onsekizinci Mektûb › Birinci Mes'ele‑i Mühimme › 1. cümle (`mektubat/18/birinci-mesele-i-muhimme/c001`) — Fütuhat'taki yedi arz ve Meşmeşiye acaibi anlatımını soru olarak aktarır
- anma · müellif · Mesnevî-i Nuriye › Şemme › 147. cümle (`mesnevi-i-nuriye/semme/c147`) — Şa'rânî'nin Fütuhat'ı bir günde iki buçuk kez okuduğu rivayetini anar

**İbn Arabî'nin Râzî'ye mektubu** (İbn Arabî): 4

- nakil · müellif · Mektubat › Yirmialtıncı Mektûb › Dördüncü Mebhas › İkinci Mes'ele › Birinci Suâli › 1. cümle (`mektubat/26/mebhas-04/mesele-02/sual-01/c001`) — Muhyiddin'in Râzî'ye mektubundaki sözünü soru olarak aktarır
- nakil · müellif · Mektubat › Yirmialtıncı Mektûb › Dördüncü Mebhas › İkinci Mes'ele › Birinci Suâli › 6. cümle (`mektubat/26/mebhas-04/mesele-02/sual-01/c006`) — Muhyiddin'in Râzî'ye o sözü niçin dediğini açıklar
- nakil · müellif · Mektubat › Yirmialtıncı Mektûb › Dördüncü Mebhas › İkinci Mes'ele › Birinci Suâli › 27. cümle (`mektubat/26/mebhas-04/mesele-02/sual-01/c027`) — Mektuptaki ihtarın anlamını özetler
- nakil · talebe · Mektubat › Fihrist › Yirmialtıncı Mektûb › İkinci Mes'ele › 2. cümle (`mektubat/fihrist/mektub-26/mesele-02/c002`) — Fihrist: Muhyiddin'in Râzî'ye sözünü anar

**Geylânî'nin kasidesi ve virdi** (Abdülkādir-i Geylânî): 2

- nakil · müellif · Sikke-i Tasdik-i Gaybî › Sekizinci Lem'a › Gavs, birkaç yerde yine, işârî bir tarzda haber veriyor › 22. cümle (`sikke-i-tasdik-i-gaybi/lema-08/gavs-birkac-yerde-yine-isari/c022`) — Kasidedeki kelimeye işaret bulunduğu söyleniyor.
- nakil · müellif · Sikke-i Tasdik-i Gaybî › Sekizinci Lem'a › Gavs, birkaç yerde yine, işârî bir tarzda haber veriyor › 30. cümle (`sikke-i-tasdik-i-gaybi/lema-08/gavs-birkac-yerde-yine-isari/c030`) — Kasidesi ve Virdü'l-İşâ'sında Hizbü'l-Kur'ân'a işaret bulur

**el-Mîzânü'l-Kübrâ** (Şa'rânî): 2

- havale · müellif · Sözler › Yirmiyedinci Söz › Hâtime › 42. cümle (`sozler/27/hatime/c042`) — Şeriat mizanlarını Şa'rânî'nin Mîzan'ıyla tartmaya gönderir
- nakil · müellif · Şualar › Ondördüncü Şuâ › Hatâlar ve Cevabları › 101. cümle (`sualar/14/hatalar-ve-cevablari/c101`) — Şa'rânî gibilerin kitaplarında tahdîs-i nimeti emsal gösterir

**Cünnetü'l-Esmâ** (Gazâlî): 1

- nakil · müellif · Barla Lahikası › Mektûbat’ın Üçüncü Kısmı › Siz beni bulduğunuzdan bir şükretseniz, ben sizi bulduğuma bin şükrediyorum › 18. cümle (`barla-lahikasi/kisim-03/256/c018`) — Altı ismi Cünnetü'l-Esmâ'da şerh ettiğini bildirir

**el-Yevâkît ve'l-Cevâhir** (Şa'rânî): 1

- nakil · müellif · Mesnevî-i Nuriye › Şemme › 147. cümle (`mesnevi-i-nuriye/semme/c147`) — Şa'rânî'nin Fütûhât'ı okuması Kitab-ı Yevâkît'in rivayetiyle aktarılır

**İhyâu Ulûmi'd-Dîn** (Gazâlî): 1

- nakil · talebe · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › O Zamanki Hayatına Kısa Bir Bakış › 7. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/o-zamanki-hayatina-kisa-bir/c007`) — İhyâ'daki kaideye uyarak ekmeği terk ettiği anlatılır

**el-Fusûs (Fusûsu'l-Hikem olabilir)** (İbn Arabî (?)): 1

- anma · müellif · el-Mesnevî el-Arabî en-Nurî › اَلرِّسَالَةُ الْعَاشِرَةُ › 191. cümle (`el-mesnevi-el-arabi/onuncu-risale/c191`) — Temsilde harf şekliyle öğretilen yaldızlı "Fusus kitabı"; hangi eser olduğu belirsiz

**Dîvân** (İbnü'l-Fârıd): 1

- tefe'ül · talebe · İşaratü'l-İ'caz › Sûre‑i Bakara › 31‑33. Âyetlerin Tefsiri › Mukaddime › 4. cümle › Hâşiye › 1. cümle (`isaratul-icaz/sure-i-bakara/31-33-ayetlerin-tefsiri/mukaddime/c004/h1/c001`) — Habib'in notu: İbnü'l-Fârıd'ın kitabından tefeül edip beyit çıkmış.

**Dîvân** (Ümmî Sinan): 1

- tefe'ül · talebe · Barla Lahikası › Mektûbat’ın Üçüncü Kısmı › İstidadımın fevkinde şöyle bir kaç beyit kalbime ve kalemime geldi. Müşfik Üstadımın aflarına istinaden yazıyorum › 13. cümle (`barla-lahikasi/kisim-03/178/c013`) — Hulûsi'nin şiirinde Ümmî Sinan Dîvânı'ndan tefe'ül anılıyor (bk. Sikke lema-08).

### Belâgat, dil ve mantık

**Miftâhu'l-Ulûm / Sekkâkî** (Sekkâkî): 16

- havale · müellif · İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri › المسألة السابعة: › 61. cümle (`isaratul-icaz-arabi/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-07/c061`) — Nahvî itirazların cevabı için Miftâh'ın hâtimesine gönderir
- havale · müellif · İşaratü'l-İ'caz › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri (Nübüvvet Hakkında) › İ'câzın Vecihleri › 9. cümle (`isaratul-icaz/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/icazin-vecihleri/c009`) — İ'câzın icmâlî bilgisi için belâgat imamlarının beyanına gönderir
- nakil · müellif · İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri › المسألة السابعة: › 34. cümle (`isaratul-icaz-arabi/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-07/c034`) — İ'câzı bilmenin üç yolunu belâgat imamlarının tahkikine dayandırır
- nakil · müellif · İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri › المسألة السابعة: › 164. cümle (`isaratul-icaz-arabi/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-07/c164`) — İ'câzın sebebinde Cürcânî, Zemahşerî, Sekkâkî görüşünü esah sayar
- nakil · müellif · İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri › المسألة السابعة: › 165. cümle (`isaratul-icaz-arabi/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-07/c165`) — Sekkâkî'nin i'câzın zevkî olduğu görüşünü nakleder
- nakil · müellif · İşaratü'l-İ'caz › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri (Nübüvvet Hakkında) › İ'câzın Vecihleri › 49. cümle (`isaratul-icaz/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/icazin-vecihleri/c049`) — Nahvî itirazlara Sekkâkî'nin cevabını nakleder
- nakil · müellif · İşaratü'l-İ'caz › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri (Nübüvvet Hakkında) › İ'câzın Vecihleri › 51. cümle (`isaratul-icaz/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/icazin-vecihleri/c051`) — Miftâh'ın sonunda câhil itirazcıların reddedildiğini söyler
- nakil · müellif · İşaratü'l-İ'caz › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri (Nübüvvet Hakkında) › İ'câzın Vecihleri › Üçüncü Vecih › 122. cümle (`isaratul-icaz/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/icazin-vecihleri/vecih-03-2/c122`) — Belâgat imamlarının i'câz görüşünü nakleder
- nakil · müellif · İşaratü'l-İ'caz › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri (Nübüvvet Hakkında) › İ'câzın Vecihleri › Üçüncü Vecih › 123. cümle (`isaratul-icaz/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/icazin-vecihleri/vecih-03-2/c123`) — Sekkâkî'nin 'i'câz zevkîdir' sözünü nakletmeye başlar
- nakil · müellif · Muhakemat › Birinci Makale › Sekizinci Mes'ele › 50. cümle (`muhakemat/makale-01/mesele-08/c050`) — Kalb-i hayâlî sanatını Miftâh'taki beyana dayandırır
- nakil · müellif · Sözler › Yirmibeşinci Söz › İkinci Şu'le › Birinci Nur › 1. cümle (`sozler/25/sule-02/nur-01/c001`) — Kur'ân'ın tesanüdüne belâgat imamlarının şehadetini delil getirir
- nakil · müellif · Sözler › Yirmibeşinci Söz › Birinci Zeyl › Üçüncü Nokta › 5. cümle (`sozler/25/zeyl-01/nokta-03/c005`) — Belâgat imamlarının Kur'ân belâgatının beşer üstü olduğu kararını nakleder
- nakil · müellif · Şuaat-ı Marifetü'n-Nebi › Altıncı Şuâ › Yedinci Menba' › 3. cümle (`suaat-i-marifetin-nebi/6/menba-07/c003`) — Belâgat imamlarının i'câza üç yolla hükmettiğini nakleder
- nakil · müellif · Şualar › Yedinci Şuâ › Âyetü'l‑Kübrâ › Birinci Bâb (Berâhin‑i Ulûhiyet) › Onyedinci Mertebe (Kur'ân‑ı Mu'cizü'l-Beyân) › Üçüncü Nokta › 5. cümle (`sualar/7/ayetul-kubra/bab-01/mertebe-17/nokta-03/c005`) — Belâgat imamlarının Kur'ân belâgatının beşer üstü olduğu kararını nakleder
- nakil · müellif · Tarihçe-i Hayat › Dördüncü Kısım Kastamonu Hayatı › Âyetü'l‑Kübrâ › Onyedinci Mertebe (Kur'ân‑ı Mu'cizü'l-Beyân) › Üçüncü Nokta › 5. cümle (`tarihce-i-hayat/dorduncu-kisim-kastamonu-hayati/ayetul-kubra/mertebe-17/nokta-03/c005`) — Belâgat imamlarının Kur'ân belâgatının beşer üstü olduğu kararını nakleder
- değerlendirme · müellif · Muhakemat › İkinci Makale › Onikinci Mes'ele › 12. cümle (`muhakemat/makale-02/mesele-12/c012`) — Sekkâkî'nin bazı kelâmlarını âlî üslûba misal gösterir

**Muallakāt-ı Seb'a** (—): 11

- değerlendirme · müellif · İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri › المسألة السابعة: › 39. cümle (`isaratul-icaz-arabi/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-07/c039`) — Kur'ân'ın belâgatı Muallakât'ı sildi
- değerlendirme · müellif · İşaratü'l-İ'caz › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri (Nübüvvet Hakkında) › İ'câzın Vecihleri › 19. cümle (`isaratul-icaz/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/icazin-vecihleri/c019`) — Kur'ân'ın belâgatı Muallakât'ı iftihar listesinden sildirdi
- değerlendirme · müellif · İşaratü'l-İ'caz › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri (Nübüvvet Hakkında) › İ'câzın Vecihleri › Üçüncü Vecih › 201. cümle (`isaratul-icaz/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/icazin-vecihleri/vecih-03-2/c201`) — Muallakât'ın Kur'ân'a yaklaşamadığını söyler
- değerlendirme · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onsekizinci İşâret › İkinci Nükte › 10. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-18/nukte-02/c010`) — Kur'ân Muallakât'ı kıymetten düşürdü
- değerlendirme · müellif · Sözler › Yirmibeşinci Söz › Birinci Zeyl › Üçüncü Nokta › 1. cümle (`sozler/25/zeyl-01/nokta-03/c001`) — Kur'ân karşısında Muallakât'ın kıymeti kalmadı
- değerlendirme · müellif · Şuaat-ı Marifetü'n-Nebi › Altıncı Şuâ › Yedinci Menba' › 7. cümle (`suaat-i-marifetin-nebi/6/menba-07/c007`) — Kur'ân'ın belâgatı Muallakât'ı sildi, söndürdü
- değerlendirme · müellif · Şualar › Yedinci Şuâ › Âyetü'l‑Kübrâ › Birinci Bâb (Berâhin‑i Ulûhiyet) › Onyedinci Mertebe (Kur'ân‑ı Mu'cizü'l-Beyân) › Üçüncü Nokta › 1. cümle (`sualar/7/ayetul-kubra/bab-01/mertebe-17/nokta-03/c001`) — Kur'ân karşısında Muallakât'ın kıymeti kalmadı
- değerlendirme · müellif · Tarihçe-i Hayat › Dördüncü Kısım Kastamonu Hayatı › Âyetü'l‑Kübrâ › Onyedinci Mertebe (Kur'ân‑ı Mu'cizü'l-Beyân) › Üçüncü Nokta › 1. cümle (`tarihce-i-hayat/dorduncu-kisim-kastamonu-hayati/ayetul-kubra/mertebe-17/nokta-03/c001`) — Kur'ân karşısında Muallakât'ın kıymeti kalmadı
- anma · başka · İşaratü'l-İ'caz › Ecnebî Feylesofların Kur'ânı Tasdiklerine Dair Şehâdetleri › Kur'ânın Lisânı, Nezâhet ve Belâğat İtibariyle Nazîrsizdir Kur'ân, Bizâtihi Muhteşem Bir Mu'cizedir › 10. cümle (`isaratul-icaz/ecnebi-feylesoflarin-kurani-tasdiklerine-dair/kuranin-lisani-nezahet-ve-belagat/c010`) — Lebîd'i Muallakât şairlerinden biri diye tanıtır
- anma · başka · Nur'un İlk Kapısı › Ecnebî Feylesofların Kur'ân’ı Tasdiklerine Dair Şehâdetleri › Kur'ân’ın Lisânı Nezâhet ve Belâğat İtibariyle Nazîrsizdir. Kur'ân, Bizâtihi Muhteşem Bir Mu'cizedir › 10. cümle (`nurun-ilk-kapisi/ecnebi-feylesoflarin-kurani-tasdiklerine-dair/kuranin-lisani-nezahet-ve-belagat/c010`) — Lebîd'i Muallakât şairlerinden biri diye tanıtır
- anma · müellif · Sözler › Yirmibeşinci Söz › Birinci Şu'le › Birinci Şuâ › Birinci Sûret › 10. cümle (`sozler/25/sule-01/sua-01/suret-01/c010`) — Arapların Muallakât'ı Kâbe'ye asıp iftihar ettiğini anlatır

**el-Kâmûsu'l-Muhît** (Fîrûzâbâdî): 9

- değerlendirme · müellif · Âsâr-ı Bediiyye › Bediüzzaman'ın Tarihçe-i Hayatı › 91. cümle (`asar-i-bediiyye/bediuzzamanin-tarihce-i-hayati/c091`) — Kâmûs'un usulünün tersine bir lügat yazmak istediğini söyler
- değerlendirme · müellif · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › O Zamanki Hayatına Kısa Bir Bakış › 112. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/o-zamanki-hayatina-kisa-bir/c112`) — Kâmûs'un usulünün tersine bir lügat yazmak istediğini söyler
- anma · talebe · Âsâr-ı Bediiyye › Bediüzzaman'ın Tarihçe-i Hayatı › 89. cümle (`asar-i-bediiyye/bediuzzamanin-tarihce-i-hayati/c089`) — Kâmus-u Okyanus'u Bâbü's-Sin'e kadar ezberlediği anlatılır
- anma · talebe · Âsâr-ı Bediiyye › Bediüzzaman'ın Tarihçe-i Hayatı › 90. cümle (`asar-i-bediiyye/bediuzzamanin-tarihce-i-hayati/c090`) — Kâmûs'u niçin ezberlediğini sorduğunu anlatır
- anma · müellif · Kızıl İcaz (Arapça) › فصل في انواع العلم الحادث › 31. cümle (`kizil-icaz-arabi/fasl-02/c031`) — Kâmûs'u geniş bir içerik örneği olarak anar
- anma · müellif · Kızıl İcaz (Arapça) › فصل في المعرفات › 19. cümle (`kizil-icaz-arabi/fasl-06/c019`) — Lafzî tarife örnek olarak Kâmûs'u anar
- anma · başka · Kızıl İcaz (Arapça) › فصل في المعرفات › 19. cümle › Şerh › 1. cümle (`kizil-icaz-arabi/fasl-06/c019/s1/c001`) — Şerh: Kâmûs'taki lügat beyanlarını lafzî tarif örneği sayar
- anma · müellif · Ta'likat (Arapça) › باب الحدّ › 5. cümle (`talikat-arabi/hadd/c005`) — Lafzî tarife örnek olarak Kâmûs'u anar
- anma · talebe · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › O Zamanki Hayatına Kısa Bir Bakış › 110. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/o-zamanki-hayatina-kisa-bir/c110`) — Kâmus-u Okyanus'u Bâbü's-Sin'e kadar ezberlediği anlatılır

**Delâilü'l-İ'câz ve Esrârü'l-Belâğa** (Abdülkāhir el-Cürcânî): 9

- havale · müellif · İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 17‑20. Âyetlerin Tefsiri › المسألة العاشرة: › 14. cümle (`isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/mesele-10/c014`) — Müzeyyen üslûbun örneği için iki kitaba gönderir
- havale · müellif · Muhakemat › Birinci Makale › Sekizinci Mes'ele › 45. cümle (`muhakemat/makale-01/mesele-08/c045`) — Delâil'in 221. kapısına gönderir, Abdülkahir'in tekdirini gösterir
- havale · müellif · Muhakemat › Birinci Makale › Sekizinci Mes'ele › 45. cümle (`muhakemat/makale-01/mesele-08/c045`) — Delâil'in 221. kapısına gönderir
- nakil · müellif · İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 17‑20. Âyetlerin Tefsiri › 13. cümle (`isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/c013`) — Temsil hakkında Esrârü'l-Belâğa'dan uzun alıntı yapar
- nakil · müellif · İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 17‑20. Âyetlerin Tefsiri › المسألة الأولى: › 1. cümle (`isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/mesele-01/c001`) — Abdülkahir'in iki kitabında lafızcılara reddini anar
- nakil · müellif · Muhakemat › İkinci Makale › Birinci Mes'ele › 22. cümle (`muhakemat/makale-02/mesele-01/c022`) — Abdülkahir'in iki kitabın üçte birini lafızperestliğe ayırdığını söyler
- nakil · müellif · Muhakemat › İkinci Makale › Birinci Mes'ele › 22. cümle (`muhakemat/makale-02/mesele-01/c022`) — Abdülkahir'in iki kitabın üçte birini lafızperestliğe ayırdığını söyler
- değerlendirme · müellif · Muhakemat › İkinci Makale › Onikinci Mes'ele › 10. cümle (`muhakemat/makale-02/mesele-12/c010`) — Abdülkahir'in sözünü üslûb-u müzeyyene örnek gösterir
- değerlendirme · müellif · Muhakemat › İkinci Makale › Onikinci Mes'ele › 10. cümle (`muhakemat/makale-02/mesele-12/c010`) — Abdülkahir'in sözünü üslûb-u müzeyyene örnek gösterir

**el-Burhân** (Gelenbevî): 9

- nakil · başka · Ta'likat › Akiste Fasıl › 1. cümle › Hâşiye › 1. cümle (`talikat/aks/c001/h1/c001`) — Mütercim notu: alıntılanan metnin Gelenbevî'deki sayfası
- nakil · başka · Ta'likat › Dördüncü Bâb: Deliller › 1. cümle › Hâşiye › 1. cümle (`talikat/edille/c001/h1/c001`) — Mütercim notu: bir kelimenin Gelenbevî metninde olup Ta'likat'ta olmadığı
- nakil · başka · Ta'likat › Dördüncü Bâb: Deliller › 2. cümle › Hâşiye › 1. cümle (`talikat/edille/c002/h1/c001`) — Mütercim notu: başlık Gelenbevî'den, devamı müellifin
- nakil · başka · Ta'likat › Şartlı Önerme Bölümü › 56. cümle › Hâşiye 1 › 1. cümle (`talikat/sartiyye/c056/h1/c001`) — Mütercim notu: alıntılanan metnin Gelenbevî'deki sayfası
- nakil · başka · Ta'likat › Şartlı Önerme Bölümü › 76. cümle › Hâşiye › 1. cümle (`talikat/sartiyye/c076/h1/c001`) — Mütercim notu: alıntılanan metnin Gelenbevî'deki sayfası
- nakil · başka · Ta'likat › Şartlı Önerme Bölümü › 105. cümle › Hâşiye › 1. cümle (`talikat/sartiyye/c105/h1/c001`) — Mütercim notu: alıntılanan metnin Gelenbevî'deki sayfası
- nakil · başka · Ta'likat › Vazgeçme ve Tahsil Etme Hakkında Fasıl › 109. cümle › Hâşiye › 1. cümle (`talikat/udul-ve-tahsil/c109/h1/c001`) — Mütercim notu: alıntılanan metnin Gelenbevî'deki sayfası
- anma · müellif · Kızıl İcaz (Arapça) › فصل في القضايا واحكامها › مقدمة في المحرَّفات › 35. cümle (`kizil-icaz-arabi/fasl-07/muharrefat/c035`) — Tafsil için Gelenbevî'ye yazdığı kendi Ta'likat'ına gönderir
- anma · başka · Ta'likat (Arapça) › 12. cümle (`talikat-arabi/c012`) — Muhakkik, baskıda Gelenbevî metinlerinin yerleşimini anlatır

**Molla Câmî (nahiv şerhi)** (Câmî): 3

- anma · talebe · Âsâr-ı Bediiyye › Bediüzzaman'ın Tarihçe-i Hayatı › 15. cümle (`asar-i-bediiyye/bediuzzamanin-tarihce-i-hayati/c015`) — Molla Câmî'den sonra ikmal-i nüsah
- anma · talebe · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › 50. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/c050`) — Molla Câmî'den sonuna kadar kitapları bitirmesi
- anma · talebe · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › O Zamanki Hayatına Kısa Bir Bakış › 36. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/o-zamanki-hayatina-kisa-bir/c036`) — Bu sene Molla Câmî'yi okuduğu sorulur

**Şerh-i Şemsiyye** (Kutbüddîn er-Râzî): 2

- anma · talebe · Âsâr-ı Bediiyye › Bediüzzaman'ın Tarihçe-i Hayatı › 38. cümle (`asar-i-bediiyye/bediuzzamanin-tarihce-i-hayati/c038`) — Kardeşinin Şerh-i Şemsiyye'yi okuduğunu söylemesi
- anma · talebe · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › O Zamanki Hayatına Kısa Bir Bakış › 23. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/o-zamanki-hayatina-kisa-bir/c023`) — Kardeşinin Şerh-i Şemsî'yi bitirdiğini söylediği konuşma

**Sîbeveyh (el-Kitâb)** (Sîbeveyh): 2

- nakil · müellif · İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 17‑20. Âyetlerin Tefsiri › المسألة الثامنة: › 1. cümle (`isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/mesele-08/c001`) — Harf-i cerlerin asıl mânâsı hakkında Sîbeveyh'in tasrihini nakleder
- nakil · müellif · İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 21‑22. Âyetlerin Tefsiri › مقدمة › 253. cümle (`isaratul-icaz-arabi/sure-i-bakara/21-22-ayetlerin-tefsiri/mukaddime/c253`) — "min"in ibtida mânâsı için Sîbeveyh'in görüşüne dayanır

**Mirkât (mantık)** (—): 2

- anma · talebe · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › Genç Said’in Serbestiyet ve Hürriyet Aşkı ve Kırk Kadar Kitabı Ezberlemesi › 19. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/genc-saidin-serbestiyet-ve-hurriyet/c019`) — Şerhsiz ezberlemeye başladığı kitap; hikâye.
- anma · talebe · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › Genç Said’in Serbestiyet ve Hürriyet Aşkı ve Kırk Kadar Kitabı Ezberlemesi › 20. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/genc-saidin-serbestiyet-ve-hurriyet/c020`) — Mirkât'ın hâşiye ve şerhiyle kendi görüşünü karşılaştırması anlatılıyor.

**Süyûtî'nin nahiv şerhi** (Süyûtî): 1

- anma · talebe · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › O Zamanki Hayatına Kısa Bir Bakış › 36. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/o-zamanki-hayatina-kisa-bir/c036`) — Geçen sene 'Süyûtî' okuduğu sorulur; Cem'u'l-Cevâmi' değil

**Câhız** (Câhız): 1

- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onsekizinci İşâret › İkinci Nükte › 42. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-18/nukte-02/c042`) — Câhız'ın muaraza ve muharebe sözünü aktarır

**Makāmât** (Harîrî): 1

- anma · talebe · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › O Zamanki Hayatına Kısa Bir Bakış › 47. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/o-zamanki-hayatina-kisa-bir/c047`) — Hafıza sınamasında kitab uzatılıyor; hikâye.

### Fıkıh

**İbn Hacer el-Heytemî'nin fıkhı** (İbn Hacer el-Heytemî): 3

- nakil · müellif · Mektubat › İkinci Mektûb › 35. cümle (`mektubat/2/c035`) — Salâhat niyetiyle verilen hediye hükmünü nakleder
- değerlendirme · müellif · Sünuhat › Kur'ân’ın Hâkimiyet‑i Mutlakası › 29. cümle (`sunuhat/kuranin-hakimiyet-i-mutlakasi/c029`) — İbn Hacer'e Kur'ân'ı anlamak için bakılmalı der
- değerlendirme · müellif · Sünuhat › Kur'ân’ın Hâkimiyet‑i Mutlakası › 30. cümle (`sunuhat/kuranin-hakimiyet-i-mutlakasi/c030`) — İbn Hacer'in ne dediği için bakılmamalı der

**Mecmau'l-Enhur; Merâku'l-Felâh** (Dâmâd; Şürünbülâlî): 1

- nakil · müellif · Barla Lahikası › Mektûbat’ın Üçüncü Kısmı › İki Ramazan içinde bir kefaret kâfidir, müteaddit vakıalara bir kefaret kifayet eder; çünkü tedahül var › 4. cümle (`barla-lahikasi/kisim-03/273/c004`) — Keffâret meselesinde Dâmâd ve Merâku'l-Felâh'ın hükmünü nakleder

**Halebî (Halebî-i Kebîr)** (İbrâhim el-Halebî): 1

- anma · müellif · Rumuzat-ı Semaniye › Yirmi Dokuzuncu Mektub'un Sekizinci Kısmı › BİRİNCİ REMİZ › Dördüncü Remiz › 46. cümle (`rumuzat-i-semaniye/kisim-08/remiz-01/remiz-04/c046`) — Harf tevafuku için Halebî kitabının satırlarına baktığını söyler

### Ahlâk

**Edebü'd-Dünyâ ve'd-Dîn** (Mâverdî): 2

- nakil · müellif · Lem'alar › Onyedinci Lem'a › Onüçüncü Nota › Birincisi › 2. cümle (`lemalar/17/nota-13/mesele-01/c002`) — Şeytanın Hz. İsâ'ya itirazı kıssasını o kitaptan naklediyor.
- nakil · müellif · Mesnevî-i Nuriye › Zühre › Onüçüncü Nota › Birincisi › 2. cümle (`mesnevi-i-nuriye/zuhre/nota-13/mesele-01/c002`) — Şeytanla Hz. İsa kıssasını o eserden naklediyor.

### Dua ve vird

**Cevşenü'l-Kebîr** (Peygamber'e nisbet): 54

- nakil · müellif · el-Mesnevî el-Arabî en-Nurî › اَلرِّسَالَةُ الْعَاشِرَةُ › 124. cümle (`el-mesnevi-el-arabi/onuncu-risale/c124`) — Tevhid hakikatine Cevşen'in münâcâtıyla işaret eder, örnek verir
- nakil · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Meşhûr duâ‑yı Nebevî olan Cevşenü'l-Kebîrin sevâb ve faziletine dair bir hadîs › 9. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/105/c009`) — Cevabını Kur'ân, Cevşen ve Nurlardan verdiğini söyler
- nakil · müellif · Hizbü'l-Ekber-i Nurî (Hizb-i Nurî) › 321. cümle (`hizb-i-nuri/c321`) — Cevşen'in hakikatlerinin işaretlerini şahit gösterir
- nakil · müellif · Hizbü Envari'l-Hakaiki'n-Nuriye (Büyük Cevşen) › Hülasat-ül Hülasa › 41. cümle (`hizbu-envaril-hakaik/hulasat-ul-hulasa/c041`) — Cevşen'in işaretlerini risalete şahit gösterir
- nakil · müellif · Lem'alar › Otuzuncu Lem'a › Otuzuncu Lem'anın Beşinci Nüktesi › Hâtime › 6. cümle (`lemalar/30/nukte-05/hatime/c006`) — Hâtimede Cevşen'den ism-i Hayy fıkrasını aktarır
- nakil · talebe · Lem'alar › Fihrist › Münâcât › 1. cümle (`lemalar/fihrist/munacat/c001`) — Münâcât'ın kaynaklarından biri olarak Cevşen'in ukdelerini sayar
- nakil · müellif · Lem'alar › Münâcât › Sekizinci Fıkra (Enbiyâ, Evliyâ, Asfiyâ) › 30. cümle (`lemalar/munacat/fikra-08/c030`) — Münâcât dersini Kur'ân ve Cevşen'den aldığını söyler
- nakil · müellif · Siracü'n-Nur › Üçüncü Şuâ (Münâcat Risalesi) › 18. cümle (`siracun-nur/sua-03/c018`) — Münâcât dersini Kur'ân ve Cevşen'den aldığını söyler
- nakil · müellif · Sözler › Yirmidördüncü Söz › Birinci Dal › 72. cümle (`sozler/24/dal-01/c072`) — Cevşen'de binbir isimle dua ve istiâzeyi delil getirir
- nakil · müellif · Sözler › Yirmibeşinci Söz › Onbirinci Şuâ Olan Meyve Risalesi’nin Onuncu Mes'elesi › 28. cümle (`sozler/25/mesele-10/c028`) — Cevşen'deki yüz defa tekrarlanan duayı tekrar hikmetine delil getirir
- nakil · müellif · Şualar › Meyve Risalesi › Onuncu Mes'ele › 28. cümle (`sualar/11/mesele-10/c028`) — Cevşen'deki yüz defa tekrarlanan duayı tekrar hikmetine delil getirir
- nakil · müellif · Şualar › Onbeşinci Şuâ › Birinci Makam › Üçüncü Medrese‑i Yûsufiye’nin Tek Bir Dersinin Üçüncü Kısmı › İkinci İşâret › Beşinci, Altıncı, Yedinci, Sekizinci Küllî Şehâdetler › 1. cümle (`sualar/15/makam-01/kisim-03/isaret-02/besinci-altinci-yedinci-sekizinci-kulli/c001`) — Cevşen'in işaretlerini risalete şahit gösterir
- nakil · müellif · Şualar › Onbeşinci Şuâ › Birinci Makam › Üçüncü Medrese‑i Yûsufiye’nin Tek Bir Dersinin Üçüncü Kısmı › İkinci İşâret › Onbeşinci Şehâdet › 4. cümle (`sualar/15/makam-01/kisim-03/isaret-02/sehadet-15/c004`) — Kur'ân ve Cevşen'in delâletini risalete şahit gösterir
- nakil · müellif · Şualar › Üçüncü Şuâ › Sekizinci Fıkra (Enbiyâ, Evliyâ, Asfiyâ) › 30. cümle (`sualar/3/fikra-08/c030`) — Münâcât dersini Kur'ân ve Cevşen'den aldığını söyler
- nakil · müellif · Şualar › Yedinci Şuâ › Mukaddime › İkinci Varta ve Çare‑i Necât › Birincisi › 8. cümle (`sualar/7/mukaddime/ikinci-varta-ve-care-i-necat/mesele-01/c008`) — Cevşen'in seksen altıncı ukdesinden alıntı yapar
- nakil · müellif · Tarihçe-i Hayat › Dördüncü Kısım Kastamonu Hayatı › Üçüncü Şuâ › Sekizinci Fıkra (Enbiyâ, Evliyâ, Asfiyâ) › 30. cümle (`tarihce-i-hayat/dorduncu-kisim-kastamonu-hayati/sua-03/fikra-08/c030`) — Münâcât dersini Kur'ân ve Cevşen'den aldığını söyler
- değerlendirme · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Benim çok kusurlu şahsıma, hüsn‑ü zan ile verdiğiniz makamlar cihetinde değil; belki vazife ve hizmet noktasında bakmalısınız › 7. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/40/c007`) — Risale-i Nur'un Cevşen'den kuvvet ve feyiz aldığını söyler
- değerlendirme · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Demek Risale‑i Nur’a ve şakirdlerine umumî bir taarruz yoktur, belki yalnız bana ve elimdeki Nurlara › 17. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/95/c017`) — Mektuptaki Cevşen'den alınan fıkraları güzel bulur
- değerlendirme · talebe · Hanımlar Rehberi › Nurcuların Kasidesi › 248. cümle (`hanimlar-rehberi/nurcularin-kasidesi/c248`) — Cevşen'i eşsiz dua diye övüp okumaya başladıklarını yazar
- değerlendirme · müellif · Hizbü'l-Ekber-i Nurî (Hizb-i Nurî) › 3. cümle (`hizb-i-nuri/c003`) — Cevşen'in kâinatı nurlandırdığını söyler
- değerlendirme · müellif · Kastamonu Lahikası › 106‑164 Mektuplar › Risale‑i Nur baştan başa kâinatı nurlandırıyor; ehl-i gaflet ve ehl-i dalâletin altında saklanmak istedikleri perdeleri yırtıyor › 4. cümle (`kastamonu-lahikasi/106-164-mektuplar/140/c004`) — Cevşen, Risale-i Nur ve Hizb-i Nurî'nin kâinatı nurlandırdığını söyler
- değerlendirme · müellif · Mektubat › Ondokuzuncu Mektûb › Âyetü'l‑Kübrâ Risalesi’nin Risalet-i Ahmediye’den Bahseden Onaltıncı Mertebesi › Üçüncüsü › 6. cümle (`mektubat/19/mertebe-16/isaret-03/c006`) — Cevşen'deki vasfın misilsiz olduğunu söyler
- değerlendirme · müellif · Mektubat › Ondokuzuncu Mektûb › Âyetü'l‑Kübrâ Risalesi’nin Risalet-i Ahmediye’den Bahseden Onaltıncı Mertebesi › Üçüncüsü › 7. cümle (`mektubat/19/mertebe-16/isaret-03/c007`) — Cevşen'in misli yoktur; Risale-i Münâcât'a bakmayı söyler
- değerlendirme · müellif · Şualar › Onbeşinci Şuâ › Birinci Makam › Üçüncü Medrese‑i Yûsufiye’nin Tek Bir Dersinin Üçüncü Kısmı › İkinci İşâret › Beşinci, Altıncı, Yedinci, Sekizinci Küllî Şehâdetler › 2. cümle (`sualar/15/makam-01/kisim-03/isaret-02/besinci-altinci-yedinci-sekizinci-kulli/c002`) — Cevşen'i en üstün münâcât sayar, Risale'nin ondan feyiz aldığını söyler
- değerlendirme · müellif · Şualar › Onbeşinci Şuâ › Birinci Makam › Üçüncü Medrese‑i Yûsufiye’nin Tek Bir Dersinin Üçüncü Kısmı › İkinci İşâret › Birincisi › 8. cümle (`sualar/15/makam-01/kisim-03/isaret-02/sehadet-01/c008`) — Cevşen'deki tavsifin emsalsiz olduğunu söyler
- değerlendirme · müellif · Şualar › Yedinci Şuâ › Âyetü'l‑Kübrâ › Birinci Bâb (Berâhin‑i Ulûhiyet) › Onaltıncı Mertebe (Muhammed‑i Arabî(asm)) › Üçüncüsü › 6. cümle (`sualar/7/ayetul-kubra/bab-01/mertebe-16/isaret-03/c006`) — Cevşen'deki vasfın misilsiz olduğunu söyler
- değerlendirme · müellif · Şualar › Yedinci Şuâ › Âyetü'l‑Kübrâ › Birinci Bâb (Berâhin‑i Ulûhiyet) › Onaltıncı Mertebe (Muhammed‑i Arabî(asm)) › Üçüncüsü › 7. cümle (`sualar/7/ayetul-kubra/bab-01/mertebe-16/isaret-03/c007`) — Cevşen'in misli yoktur; Risale-i Münâcât'a bakmayı söyler
- değerlendirme · müellif · Tarihçe-i Hayat › Dördüncü Kısım Kastamonu Hayatı › Âyetü'l‑Kübrâ › Onaltıncı Mertebe (Muhammed‑i Arabî(asm)) › Üçüncüsü › 5. cümle (`tarihce-i-hayat/dorduncu-kisim-kastamonu-hayati/ayetul-kubra/mertebe-16/isaret-03/c005`) — Cevşen'deki vasfın misilsiz olduğunu söyler
- değerlendirme · müellif · Tarihçe-i Hayat › Dördüncü Kısım Kastamonu Hayatı › Âyetü'l‑Kübrâ › Onaltıncı Mertebe (Muhammed‑i Arabî(asm)) › Üçüncüsü › 6. cümle (`tarihce-i-hayat/dorduncu-kisim-kastamonu-hayati/ayetul-kubra/mertebe-16/isaret-03/c006`) — Cevşen'in misli yoktur; Risale-i Münâcât'a bakmayı söyler
- anma · müellif · el-Mesnevî el-Arabî en-Nurî › اَلرِّسَالَةُ الْعَاشِرَةُ › الْدَّرْسُ الْخَامِسُ › 40. cümle (`el-mesnevi-el-arabi/onuncu-risale/ders-05/c040`) — Peygamber'in Rabbini Cevşen'le vasfettiğini anar
- anma · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Meşhûr duâ‑yı Nebevî olan Cevşenü'l-Kebîrin sevâb ve faziletine dair bir hadîs › 2. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/105/c002`) — Cevşen'in faziletine dair hadisten şüpheye düşen birini anlatır
- anma · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Haricî ve büyük bir düşmanın hücumu zamanında, dâhilî küçük düşmanlıkları bırakmak elzemdir › 14. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/153/c014`) — Cevşen'i iki imamdan ders aldığını anar
- anma · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Çok manidar ve kuvvetli bir tevafuk ve şakirdlerin sadakatlerine delil, bir zahir keramet‑i Nuriyeyi beyan etmeme bir ihtar aldım › 14. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/84/c014`) — Cevşen ve Evrâd-ı Bahâiye zehre galebe etti der
- anma · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Ben “Hülâsatü’l‑Hülâsa”yı okuduğum zaman, koca kâinat nazarımda bir halka-i zikir oluyor › 7. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/90/c007`) — Nükte Cevşen'i okurken kalbine zâhir oldu
- anma · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Halimin müsaadesizliği için müteaddit mektuplarınıza bir tek perişan mektubumla cevap verdiğimden gücenmeyiniz › 21. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/91/c021`) — Cevşen ve evrâdın onu ölüm tehlikesinden kurtardığını söyler
- anma · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 2 › İnşâallâh, kırk senedir takib ettiğimiz mühim bir maksadımızı, vatan ve milletin menfaati için yapmaya mecbur olduk › 33. cümle (`emirdag-lahikasi/emirdag-lahikasi-2/256/c033`) — Nazîf'in Cevşen'i teksir ettiğini anar
- anma · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 2 › İnşâallâh, kırk senedir takib ettiğimiz mühim bir maksadımızı, vatan ve milletin menfaati için yapmaya mecbur olduk › 35. cümle (`emirdag-lahikasi/emirdag-lahikasi-2/256/c035`) — Otuz beş senedir her gün Cevşen okuduğunu söyler
- anma · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 2 › İnşâallâh, kırk senedir takib ettiğimiz mühim bir maksadımızı, vatan ve milletin menfaati için yapmaya mecbur olduk › 38. cümle (`emirdag-lahikasi/emirdag-lahikasi-2/256/c038`) — Teksir edilen Cevşen'in Nurcuları tenvir edeceğini umar
- anma · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 2 › Bazı zatların mektuplarını berâ‑yı malûmat size gönderdim › 7. cümle (`emirdag-lahikasi/emirdag-lahikasi-2/259/c007`) — Eski harf Cevşen nüshalarının bedelini sorar
- anma · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 2 › Yeni hükûmet yavaş yavaş anlıyor ki hakikî kuvvet Kur’ân’dadır › 7. cümle (`emirdag-lahikasi/emirdag-lahikasi-2/275/c007`) — Cevşen'in neşrini büyük hizmet sayar
- anma · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 2 › Hizmet‑i imaniye içinde en büyük kuvveti Nurcular buldular › 19. cümle (`emirdag-lahikasi/emirdag-lahikasi-2/281/c019`) — Beş Cevşen nüshası gönderilmesini ister
- anma · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 2 › Eğirdir’den Barla’ya giderken denizin dehşetli fırtınası Leyle‑i Kadir’deki dehşetli hastalık gibi, zahmet noktasını kaldırıp büyük bir rahmete vesile oldu › 7. cümle (`emirdag-lahikasi/emirdag-lahikasi-2/342/c007`) — Fırtınada Cevşen okuduğunu anlatır
- anma · müellif · Hizbü'l-Ekber-i Nurî (Hizb-i Nurî) › 2. cümle (`hizb-i-nuri/c002`) — Cevşen ile Hizb-i Nurî'yi okuduğunu söyler
- anma · belirsiz · Hizbü Envari'l-Hakaiki'n-Nuriye (Büyük Cevşen) › Nebe' Suresi › 45. cümle (`hizbu-envaril-hakaik/nebe-suresi/c045`) — Hizb mecmuasında Cevşen'in başlığı
- anma · müellif · Kastamonu Lahikası › 1‑105 Mektuplar › Risale‑i Nur’un muhtelif hizmetinde gayret gösteren Nur Talebeleri › 25. cümle (`kastamonu-lahikasi/1-105-mektuplar/76/c025`) — Bir hemşirenin Cevşen'i ezberlediğini anar
- anma · müellif · Kastamonu Lahikası › 106‑164 Mektuplar › Risale‑i Nur baştan başa kâinatı nurlandırıyor; ehl-i gaflet ve ehl-i dalâletin altında saklanmak istedikleri perdeleri yırtıyor › 3. cümle (`kastamonu-lahikasi/106-164-mektuplar/140/c003`) — Cevşen'den bir kısım okurken gördüğünü anlatır
- anma · müellif · Lem'alar › Onyedinci Lem'a › Onüçüncü Nota › İkinci Mes'ele › 8. cümle (`lemalar/17/nota-13/mesele-02/c008`) — Faydası için Cevşen okumayı yanlış niyete örnek verir
- anma · müellif · Mesnevî-i Nuriye › Zühre › Onüçüncü Nota › İkinci Mes'ele › 8. cümle (`mesnevi-i-nuriye/zuhre/nota-13/mesele-02/c008`) — Faydası için Cevşen okumayı yanlış niyete örnek verir
- anma · müellif · Nur'un İlk Kapısı › Onuncu Ders › 96. cümle (`nurun-ilk-kapisi/ders-10/c096`) — Peygamber'in ubûdiyetini Cevşen ve emsâliyle anar
- anma · müellif · Sikke-i Tasdik-i Gaybî › İkinci Kerâmet‑i Aleviye › Kerâmet‑i Aleviye’nin Neticesi › 11. cümle (`sikke-i-tasdik-i-gaybi/ikinci-keramet-i-aleviye/keramet-i-aleviyenin-neticesi/c011`) — Risale müellifinin Cevşen'i vird ve üstad edindiğini anar
- anma · talebe · Sikke-i Tasdik-i Gaybî › Risale‑i Nur’dan Parlak Fıkralar ve Bir Kısım Güzel Mektûblar › Sabri’nin Mektûbunun Bir Parçasıdır › 9. cümle (`sikke-i-tasdik-i-gaybi/risale-i-nurdan-parlak-fikralar-ve-2/sabrinin-mektubunun-bir-parcasidir/c009`) — Kadir gecesi okunan virdler arasında Cevşen'i sayar
- anma · müellif · Tarihçe-i Hayat › Altıncı Kısım Emirdağı Hayatı › Üstad’ın Emirdağı’nda Zehirlenmesi › 2. cümle (`tarihce-i-hayat/altinci-kisim-emirdagi-hayati/ustadin-emirdaginda-zehirlenmesi/c002`) — Cevşen gibi evrâdın feyziyle zehirden korunduğunu söyler
- anma · talebe · Tarihçe-i Hayat › Dördüncü Kısım Kastamonu Hayatı › Üstad’ın, Kastamonu’dan Isparta’daki talebelerine gönderdiği mektûblarından bazıları › Mehmed Feyzi ve Çaycı Emin Efendinin Üstadımız Hakkındaki Kanâatleri › 41. cümle (`tarihce-i-hayat/dorduncu-kisim-kastamonu-hayati/ustadin-kastamonudan-ispartadaki-talebelerine-gonderdigi/mehmed-feyzi-ve-cayci-emin/c041`) — Üstad'ın Cevşen okuduğu anlatılır
- anma · talebe · Tarihçe-i Hayat › İkinci Kısım Barla Hayatı › Üstad’ın Barla’da İkameti › 12. cümle (`tarihce-i-hayat/ikinci-kisim-barla-hayati/ustadin-barlada-ikameti/c012`) — Barla'da geceleri Cevşen okuduğu anlatılır

**Kaside-i Ercûze** (Hz. Ali'ye nisbet): 17

- havale · müellif · Sikke-i Tasdik-i Gaybî › On Sekizinci Lem'a › 7. cümle (`sikke-i-tasdik-i-gaybi/lema-18/c007`) — Ercûze'nin Mecmuatü'l-Ahzâb'daki sayfalarını gösterir
- nakil · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Neden herkesten ziyâde medreseden çıkanlar Risale‑i Nur’a sarılmaları lâzım iken, en ziyâde çekinen, onlardan resmî vazifeyi alanlardır? › 6. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/106/c006`) — Ercûze'nin ulemâü's-sû' hakkındaki tokadını anar
- nakil · müellif · Lem'alar › Otuzuncu Lem'a › Otuzuncu Lem'anın Altıncı Nüktesi › 16. cümle (`lemalar/30/nukte-06/c016`) — Ercûze'de 'Sekîne' adıyla beyan edilen ism-i a'zama dayanır
- nakil · talebe · Lem'alar › Fihrist › Yirmisekizinci Lem'anın Fihristesinden Bir Parça › Üçüncü Emâre › 7. cümle (`lemalar/fihrist/yirmisekizinci-lemanin-fihristesinden-bir-parca/emare-03/c007`) — Ercûze ve Celcelûtiye'deki alâkanın Risale'ye ait olduğunu sonuçlar
- nakil · talebe · Lem'alar › Fihrist › Yirmisekizinci Lem'anın Fihristesinden Bir Parça › Birinci Nükte › 1. cümle (`lemalar/fihrist/yirmisekizinci-lemanin-fihristesinden-bir-parca/nukte-01/c001`) — Fihrist: Ercûze'den beyitlerin Risale'ye işaretini aktarır
- nakil · müellif · Sikke-i Tasdik-i Gaybî › İkinci Kerâmet‑i Aleviye › 7. cümle (`sikke-i-tasdik-i-gaybi/ikinci-keramet-i-aleviye/c007`) — Ercûze'deki 'kendini muhafaza et' emrini anar
- nakil · müellif · Sikke-i Tasdik-i Gaybî › İkinci Kerâmet‑i Aleviye › 25. cümle (`sikke-i-tasdik-i-gaybi/ikinci-keramet-i-aleviye/c025`) — Ercûze'deki kerâmeti teyid eden tevafuku anar
- nakil · müellif · Sikke-i Tasdik-i Gaybî › İkinci Kerâmet‑i Aleviye › Kerâmet‑i Aleviye’nin Neticesi › 4. cümle (`sikke-i-tasdik-i-gaybi/ikinci-keramet-i-aleviye/keramet-i-aleviyenin-neticesi/c004`) — Ercûze'de istikbalden haber verildiğini söyler
- nakil · müellif · Sikke-i Tasdik-i Gaybî › İkinci Kerâmet‑i Aleviye › Kerâmet‑i Aleviye’nin Neticesi › 15. cümle (`sikke-i-tasdik-i-gaybi/ikinci-keramet-i-aleviye/keramet-i-aleviyenin-neticesi/c015`) — Ercûze'nin Risale-i Nur'u alkışladığını sonuçlar
- nakil · müellif · Sikke-i Tasdik-i Gaybî › On Sekizinci Lem'a › 6. cümle (`sikke-i-tasdik-i-gaybi/lema-18/c006`) — Ercûze'nin Gavs'ın haberlerini tasdik ettiğini söyler
- nakil · müellif · Sikke-i Tasdik-i Gaybî › On Sekizinci Lem'a › 8. cümle (`sikke-i-tasdik-i-gaybi/lema-18/c008`) — Ercûze'nin mevzuunu ve maksadını anlatır
- nakil · müellif · Sikke-i Tasdik-i Gaybî › On Sekizinci Lem'a › 22. cümle (`sikke-i-tasdik-i-gaybi/lema-18/c022`) — Ercûze'deki altmışlık devir hesabını aktarır
- nakil · müellif · Şualar › Birinci Şuâ › İkinci Suâl › Yirmidokuzuncu Âyet › İkincisi › 8. cümle (`sualar/1/sual-02/ayet-29/ikincisi/c008`) — Ercûze'nin Risale-i Nur'a işaretini anar
- nakil · müellif · Şualar › Sekizinci Şuâ › Üçüncü Remz › Üçüncüsü › 9. cümle (`sualar/8/remiz-03/sir-03/c009`) — Ercûze'nin sonlarındaki fıkrayı cifrî işaret olarak aktarır
- nakil · talebe · Tarihçe-i Hayat › Dördüncü Kısım Kastamonu Hayatı › Üstad’ın, Kastamonu’dan Isparta’daki talebelerine gönderdiği mektûblarından bazıları › Mehmed Feyzi ve Çaycı Emin Efendinin Üstadımız Hakkındaki Kanâatleri › 5. cümle (`tarihce-i-hayat/dorduncu-kisim-kastamonu-hayati/ustadin-kastamonudan-ispartadaki-talebelerine-gonderdigi/mehmed-feyzi-ve-cayci-emin/c005`) — Ercûze'nin kerâmetkâr delâletini Üstad'a dair gösterir
- anma · talebe · Barla Lahikası › Mektûbat’ın Üçüncü Kısmı › Bu esma‑i mübarekenin vird edilmesine müsaade ve ne surette devam iktiza ettiğine emrinizi istirham ederim › 5. cümle (`barla-lahikasi/kisim-03/237/c005`) — Hulûsi Ercûze'yi Mecmuatü'l-Ahzâb'da bulduğunu anlatır
- anma · müellif · Barla Lahikası › Mektûbat’ın Üçüncü Kısmı › Siz beni bulduğunuzdan bir şükretseniz, ben sizi bulduğuma bin şükrediyorum › 16. cümle (`barla-lahikasi/kisim-03/256/c016`) — Ercûze'nin Mecmuatü'l-Ahzâb'da bulunduğunu söyler

**Mecmûatü'l-Ahzâb** (Gümüşhânevî (derleyen)): 8

- havale · belirsiz · Sikke-i Tasdik-i Gaybî › On Sekizinci Lem'a › 7. cümle (`sikke-i-tasdik-i-gaybi/lema-18/c007`) — Ercûze'nin Mecmua'daki sayfalarını gösterir
- nakil · belirsiz · Sikke-i Tasdik-i Gaybî › Sekizinci Lem'a › Gavs, birkaç yerde yine, işârî bir tarzda haber veriyor › 3. cümle (`sikke-i-tasdik-i-gaybi/lema-08/gavs-birkac-yerde-yine-isari/c003`) — Mecmua s. 563'teki beyti nakleder
- nakil · müellif · Sikke-i Tasdik-i Gaybî › Sekizinci Lem'a › Gavs, birkaç yerde yine, işârî bir tarzda haber veriyor › 15. cümle (`sikke-i-tasdik-i-gaybi/lema-08/gavs-birkac-yerde-yine-isari/c015`) — Mecmua'daki Virdü'l-İşâ fıkrasını nakleder
- nakil · belirsiz · Sikke-i Tasdik-i Gaybî › Sekizinci Lem'a › Mühim Bir İhbar‑ı Gaybî › 2. cümle (`sikke-i-tasdik-i-gaybi/lema-08/muhim-bir-ihbar-i-gaybi/c002`) — Geylânî kasidesinin beş satırını Mecmua'nın sayfasıyla nakleder
- anma · talebe · Barla Lahikası › Mektûbat’ın Üçüncü Kısmı › Bu esma‑i mübarekenin vird edilmesine müsaade ve ne surette devam iktiza ettiğine emrinizi istirham ederim › 5. cümle (`barla-lahikasi/kisim-03/237/c005`) — Ercûze kasidesini Mecmuatü'l-Ahzâb'da bulduğunu söyler
- anma · müellif · Barla Lahikası › Mektûbat’ın Üçüncü Kısmı › Siz beni bulduğunuzdan bir şükretseniz, ben sizi bulduğuma bin şükrediyorum › 16. cümle (`barla-lahikasi/kisim-03/256/c016`) — Hz. Ali'nin Ercûze'sinin Mecmuatü'l-Ahzâb'da olduğunu söyler
- anma · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 2 › Gördüğünüz meziyetler benim değil, Risale‑i Nur’undur. O da Kur’ân-ı Hakîm’in bir hakikatinin bir tefsiridir › Birinci Esâs › 5. cümle (`emirdag-lahikasi/emirdag-lahikasi-2/314/esas-01/c005`) — Mecmuatü'l-Ahzâb'daki Gazâlî'nin Hizb-i Kur'ânîsini örnek gösterir
- anma · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 2 › Gördüğünüz meziyetler benim değil, Risale‑i Nur’undur. O da Kur’ân-ı Hakîm’in bir hakikatinin bir tefsiridir › Birinci Esâs › 5. cümle (`emirdag-lahikasi/emirdag-lahikasi-2/314/esas-01/c005`) — Mecmuadaki Kur'ânî hizbleri örnek gösterir

**Evrâd-ı Bahâiye** (Şâh-ı Nakşibend'e nisbet): 5

- nakil · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Çok manidar ve kuvvetli bir tevafuk ve şakirdlerin sadakatlerine delil, bir zahir keramet‑i Nuriyeyi beyan etmeme bir ihtar aldım › 14. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/84/c014`) — Zehirlenmeye karşı Cevşen ve Bahâiye'nin galebesi
- anma · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Bugünlerde rahatsızlık için Evrad‑ı Bahaiye'yi ezber değil, kitaba bakarak okudum › 1. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/121/c001`) — Rahatsızlıkta Bahâiye'yi kitaba bakarak okudu
- anma · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Bugünlerde rahatsızlık için Evrad‑ı Bahaiye'yi ezber değil, kitaba bakarak okudum › 2. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/121/c002`) — Hâtimesini bilmediği için okumuyordu
- anma · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Bugünlerde rahatsızlık için Evrad‑ı Bahaiye'yi ezber değil, kitaba bakarak okudum › 6. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/121/c006`) — Otuz senelik Bahâiye virdine ekledi
- anma · talebe · Sikke-i Tasdik-i Gaybî › Risale‑i Nur’dan Parlak Fıkralar ve Bir Kısım Güzel Mektûblar › Sabri’nin Mektûbunun Bir Parçasıdır › 9. cümle (`sikke-i-tasdik-i-gaybi/risale-i-nurdan-parlak-fikralar-ve-2/sabrinin-mektubunun-bir-parcasidir/c009`) — Talebelerin okuduğu virdler arasında

**Kasîdetü'l-Bürde** (Bûsîrî): 3

- nakil · müellif · İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 17‑20. Âyetlerin Tefsiri › المسألة الثالثة: › 19. cümle (`isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/mesele-03/c019`) — Bûsîrî'nin hakîmâne üslubunu göstermek için beytini anar
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onbeşinci İşâret › İkinci Şûbe: › 21. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-15/sube-02/c021`) — Ölünün dirilmesi mucizesine işaret eden Bürde beytini nakleder
- nakil · müellif · Muhakemat › İkinci Makale › Üçüncü Mes'ele › 13. cümle (`muhakemat/makale-02/mesele-03/c013`) — Bürde'den nedamet beytini reçete olarak nakleder

**Delâilü'l-Hayrât** (Cezûlî): 2

- anma · müellif · Barla Lahikası › Mektûbat’ın Üçüncü Kısmı › Eğirdir müftüsüne son ihtar: Hakkı Efendi’nin hatırı için gayet mülâyim bir surette ihtar edildi › 39. cümle (`barla-lahikasi/kisim-03/170/c039`) — Delâil-i Hayrat okumaya vakti olmadığını söyleyen sözü aktarır
- anma · talebe · Sikke-i Tasdik-i Gaybî › Risale‑i Nur’dan Parlak Fıkralar ve Bir Kısım Güzel Mektûblar › Sabri’nin Mektûbunun Bir Parçasıdır › 9. cümle (`sikke-i-tasdik-i-gaybi/risale-i-nurdan-parlak-fikralar-ve-2/sabrinin-mektubunun-bir-parcasidir/c009`) — Kadir gecesinde okunan virdler arasında Delâil-i Hayrat'ı sayar

### Edebiyat

**Gülistân, Bostân / Sa'dî** (Sa'dî-i Şîrâzî): 7

- nakil · müellif · Lem'alar › Yirmi Sekizinci Lem'a › On Yedinci Nükte › 22. cümle (`lemalar/28/nukte-17/c022`) — Gülistan sahibi Sa'dî'nin naklettiği tekke-medrese hikâyesini aktarır
- nakil · müellif · Lem'alar › Yirmi Sekizinci Lem'a › On Yedinci Nükte › 30. cümle (`lemalar/28/nukte-17/c030`) — Aktarılan vakıanın Gülistan'da yazıldığını kaynak olarak gösterir
- nakil · müellif · Mektubat › Yirmialtıncı Mektûb › Dördüncü Mebhas › İkinci Mes'ele › Birinci Suâli › 15. cümle (`mektubat/26/mebhas-04/mesele-02/sual-01/c015`) — Sa'dî-i Şirâzî'nin Farsça beytini delil olarak aktarır
- nakil · müellif · Mektubat › Yirmialtıncı Mektûb › Dördüncü Mebhas › Beşinci Mes'ele › 8. cümle (`mektubat/26/mebhas-04/mesele-05/c008`) — Sa'dî-i Şirâzî'nin Farsça beytini delil olarak aktarır
- nakil · müellif · Mektubat › Yirmidokuzuncu Mektûb › Dokuzuncu Kısım: Telvihât‑ı Tis'a › Yedinci Telvih › Üçüncü Nükte › 4. cümle (`mektubat/29/kisim-09/telvih-07/nukte-03/c004`) — Sa'dî-i Şirâzî'nin Farsça beytini delil olarak aktarır
- değerlendirme · müellif · Muhakemat › Birinci Makale › Onuncu Mukaddeme › 17. cümle (`muhakemat/makale-01/mukaddeme-10/c017`) — Mesnevî sahibi ve Sa'dî'nin farazi hikâye kullanmasını meşru örnek gösterir
- tefe'ül · müellif · Sikke-i Tasdik-i Gaybî › Sekizinci Lem'a › Latîf Bir Tefe'ül › 1. cümle (`sikke-i-tasdik-i-gaybi/lema-08/latif-bir-tefeul/c001`) — Sözler hakkında Sa'dî'nin Bostan'ı açılarak tefe'ül yapılır

**Hâfız-ı Şîrâzî** (Hâfız): 1

- nakil · müellif · Mektubat › Yirmiikinci Mektûb › Birinci Mebhas › Dördüncü Vecih › Dördüncü Düstur › 28. cümle (`mektubat/22/mebhas-01/vecih-04/dustur-04/c028`) — Hâfız-ı Şirâzî'nin dünya hakkındaki beytini aktarır

### Felsefe

**İbn Sînâ (eser adı anılmadan)** (İbn Sînâ): 12

- nakil · müellif · Barla Lahikası › Yedinci Risale Olan Yedinci Mes'ele › Üçüncü İşâret › 2. cümle (`barla-lahikasi/mesele-07/isaret-03/c002`) — İbn Sînâ'nın 'akıl buna yol bulamaz' sözünü aktarır
- nakil · müellif · Lem'alar › Ondokuzuncu Lem'a › Yedinci Nükte › 55. cümle (`lemalar/19/nukte-07/c055`) — İbn Sînâ'nın âyeti tıbben tefsir eden beyitlerini aktarır
- nakil · müellif · Mektubat › Yirmisekizinci Mektûb › Yedinci Risale Olan Yedinci Mes'ele › Üçüncü İşâret › 2. cümle (`mektubat/28/mesele-07/isaret-03/c002`) — İbn Sînâ'nın 'akıl buna yol bulamaz' sözünü aktarır
- nakil · talebe · Mesnevî-i Nuriye › Fihrist › 3 ‑ Lâsiyyemâlar › 1. cümle (`mesnevi-i-nuriye/fihrist/3-lasiyyemalar/c001`) — Fihrist: İbn Sînâ'nın 'haşir naklîdir' sözünü aktarıp risaleyi üstün tutar
- nakil · müellif · Sözler › Onuncu Söz › Hâtime › 51. cümle (`sozler/10/hatime/c051`) — İbn Sînâ'nın 'haşir aklî kıyaslarla değil' sözünü aktarır
- nakil · müellif · Tarihçe-i Hayat › İkinci Kısım Barla Hayatı › Yirmisekizinci Mektûbun Yedinci Mes'elesi › Küllî Birkaç İnâyet‑i Rabbâniye’ye İşâretler › Üçüncü İşâret › 2. cümle (`tarihce-i-hayat/ikinci-kisim-barla-hayati/mesele-07/kulli-birkac-inayet-i-rabbaniyeye-isaretler/isaret-03/c002`) — İbn Sînâ'nın 'akıl buna yol bulamaz' sözünü aktarır
- nakil · talebe · Tarihçe-i Hayat › Sekizinci Kısım Isparta Hayatı › Nurlara Olan Taarruzların Bir Zararı Olsa Yirmi Faydası Vardır › 114. cümle (`tarihce-i-hayat/sekizinci-kisim-isparta-hayati/nurlara-olan-taarruzlarin-bir-zarari/c114`) — İbn Sînâ'nın 'haşir naklîdir' sözünü aktarıp Risale'yi üstün tutar
- değerlendirme · talebe · Asâ-yı Mûsâ › Nur Talebelerinin Mektûbları › Üniversite Nur Talebelerinden Mustafa Hilmi › 19. cümle (`asa-yi-musa/nur-talebelerinin-mektublari/universite-nur-talebelerinden-mustafa-hilmi/c019`) — Risale'nin isbat yolunu İbn Sînâ ve feylesoflarınkiyle karşılaştırır
- değerlendirme · talebe · Barla Lahikası › Yirmiyedinci Mektûb’un Üçüncü Kısmı ve Üçüncü Zeylin Nihâyetidir › Nadire‑i cihan, hadim-i Kur’ân Said Nursî (ra) hakkında hissiyatımdan binden birini beyan ediyorum › 31. cümle (`barla-lahikasi/yirmiyedinci-mektubun-ucuncu-kismi-ve/133/c031`) — Ta'likât'ın İbn Sînâ'nın te'lifâtını geçeceğini söyler
- değerlendirme · talebe · Gençlik Rehberi › Ankara Üniversitesi'nde okunan bir konferanstır › 26. cümle (`genclik-rehberi/ankara-universitesinde-okunan-bir-konferanstir/c026`) — Risale'nin isbat yolunu İbn Sînâ ve feylesoflarınkiyle karşılaştırır
- değerlendirme · talebe · Sikke-i Tasdik-i Gaybî › Risale‑i Nur’dan Parlak Fıkralar ve Bir Kısım Güzel Mektûblar › Üniversitedeki Nur Şâkirdlerinin, Nur Hakikatinin Fen Dâiresinde Fevkalâde Kıymetini Takdir Ettiklerine Bir Nümûnedir › 20. cümle (`sikke-i-tasdik-i-gaybi/risale-i-nurdan-parlak-fikralar-ve-2/universitedeki-nur-sakirdlerinin-nur-hakikatinin/c020`) — Risale'nin isbat yolunu İbn Sînâ ve feylesoflarınkiyle karşılaştırır
- değerlendirme · talebe · Tarihçe-i Hayat › İkinci Kısım Barla Hayatı › Nadire‑i cihan, hadim-i Kur’ân Said Nursî (ra) hakkında hissiyatımdan binden birini beyan ediyorum › 32. cümle (`tarihce-i-hayat/ikinci-kisim-barla-hayati/nadire-i-cihan-hadim-i-kuran-said/c032`) — Ta'likât'ın İbn Sînâ'nın te'lifâtını geçeceğini söyler

**Fârâbî (eser adı anılmadan)** (Fârâbî): 4

- değerlendirme · talebe · Asâ-yı Mûsâ › Nur Talebelerinin Mektûbları › Üniversite Nur Talebelerinden Mustafa Hilmi › 19. cümle (`asa-yi-musa/nur-talebelerinin-mektublari/universite-nur-talebelerinden-mustafa-hilmi/c019`) — Fârâbî'lerin delil yolunu Risale-i Nur'un isbatıyla karşılaştırır
- değerlendirme · talebe · Gençlik Rehberi › Ankara Üniversitesi'nde okunan bir konferanstır › 26. cümle (`genclik-rehberi/ankara-universitesinde-okunan-bir-konferanstir/c026`) — Fârâbî'lerin delil yolunu Risale-i Nur'un isbatıyla karşılaştırır
- değerlendirme · talebe · Sikke-i Tasdik-i Gaybî › Risale‑i Nur’dan Parlak Fıkralar ve Bir Kısım Güzel Mektûblar › Üniversitedeki Nur Şâkirdlerinin, Nur Hakikatinin Fen Dâiresinde Fevkalâde Kıymetini Takdir Ettiklerine Bir Nümûnedir › 20. cümle (`sikke-i-tasdik-i-gaybi/risale-i-nurdan-parlak-fikralar-ve-2/universitedeki-nur-sakirdlerinin-nur-hakikatinin/c020`) — Fârâbî'lerin delil yolunu Risale-i Nur'un isbatıyla karşılaştırır
- değerlendirme · talebe · Sözler › Konferans › 162. cümle (`sozler/konferans/c162`) — Said Nursî'nin felsefede Fârâbî gibi hükemayı geçtiğini söyler

**Eflâtun / Aristo** (—): 3

- nakil · başka · Ta'likat › Küllî ve Cüzî Hakkında Bir Fasıl › 5. cümle › Hâşiye › 26. cümle (`talikat/kulli-ve-cuzi/c005/h1/c026`) — Mütercim notu: 'küllî' teriminin Aristo'nun eserlerindeki aslını açıklar
- değerlendirme · başka · İşaratü'l-İ'caz › Ecnebî Feylesofların Kur'ânı Tasdiklerine Dair Şehâdetleri › Kur'ân, Öyle Bir Peygamber Sesidir Ki, Onu Bütün Dünya Dinleyebilir. Bu Sesin Aksi; Saraylarda, Çöllerde, Şehirlerde, Devletlerde Çınlar!‥ › 5. cümle (`isaratul-icaz/ecnebi-feylesoflarin-kurani-tasdiklerine-dair/kuran-oyle-bir-peygamber-sesidir/c005`) — Yabancı şahitlik: Kur'ân'ı Eflâtun'un nasihatlerinden ayırır
- değerlendirme · başka · Nur'un İlk Kapısı › Ecnebî Feylesofların Kur'ân’ı Tasdiklerine Dair Şehâdetleri › Kur'ân, Öyle Bir Peygamber Sesidir Ki, O’nu Bütün Dünya Dinleyebilir. Bu Sesin Aksi; Saraylarda, Çöllerde, Şehirlerde, Devletlerde Çınlar!‥ › 5. cümle (`nurun-ilk-kapisi/ecnebi-feylesoflarin-kurani-tasdiklerine-dair/kuran-oyle-bir-peygamber-sesidir/c005`) — Yabancı şahitlik: Kur'ân'ı Eflâtun'un nasihatlerinden ayırır

### Önceki kitaplar

**İncil** (—): 59

- nakil · müellif · Barla Lahikası › Mektûbat’ın Üçüncü Kısmı › Mesail‑i Müteferrika (Altı Mes'ele hâlinde bazı suallere cevap verir ve bazı konuları açıklar) › Beşinci Mes'ele › 33. cümle (`barla-lahikasi/kisim-03/220/mesele-05/c033`) — Fetih âyetinin İncil'i şahit göstermesini anlatır
- nakil · müellif · el-Mesnevî el-Arabî en-Nurî › حَــــبَّــــةٌ › 254. cümle (`el-mesnevi-el-arabi/habbe/c254`) — Peygamberin İncil'deki adının Ahmed olduğunu nakleder
- nakil · müellif · İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 2. Âyetin Tefsiri › مقدمة › 11. cümle (`isaratul-icaz-arabi/sure-i-bakara/2/mukaddime/c011`) — Âyetteki işaretin İncil'de müjdelenen Kur'ân'a dönebileceğini söyler
- nakil · müellif · İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 2. Âyetin Tefsiri › مقدمة › 12. cümle (`isaratul-icaz-arabi/sure-i-bakara/2/mukaddime/c012`) — Âyetteki işaretin İncil'de müjdelenen Kur'ân'a dönebileceğini söyler
- nakil · müellif · Kastamonu Lahikası › 106‑164 Mektuplar › İnsan için gerçek teselli, yardım ve dayanak noktasını veren Kur’an’ın esâsâtını bu zamanda en parlak ve kuvvetli gösteren Risale‑i Nur’dur › 5. cümle (`kastamonu-lahikasi/106-164-mektuplar/129/c005`) — Hz. İsâ'nın İncil'deki tesellici gelecek sözünü nakleder
- nakil · müellif · Lem'alar › Yedinci Lem'a › Yedincisi › 2. cümle (`lemalar/7/vecih-07/c002`) — İncil'in sahâbe ve Âlemin Reisi hakkındaki ifadesini nakleder
- nakil · müellif · Lem'alar › Yedinci Lem'a › Yedincisi › 3. cümle (`lemalar/7/vecih-07/c003`) — İncil'in sahâbe ve Âlemin Reisi hakkındaki ifadesini nakleder
- nakil · müellif · Lem'alar › Yedinci Lem'a › Yedincisi › 6. cümle (`lemalar/7/vecih-07/c006`) — İncil'in sahâbe ve Âlemin Reisi hakkındaki ifadesini nakleder
- nakil · müellif · Lem'alar › Yedinci Lem'a › Yedincisi › 8. cümle (`lemalar/7/vecih-07/c008`) — İncil'in sahâbe ve Âlemin Reisi hakkındaki ifadesini nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Âyetü'l‑Kübrâ Risalesi’nin Risalet-i Ahmediye’den Bahseden Onaltıncı Mertebesi › Dördüncüsü › 3. cümle (`mektubat/19/mertebe-16/isaret-04/c003`) — Enbiyânın İncil'de verdiği beşarete dayanır, tafsili Ondokuzuncu Mektub'a
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/c001`) — İncil'in nübüvvet-i Ahmediye'ye dair haberlerini konu edinir
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › İkinci Hüccet › 13. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-02/c013`) — Müslüman olan âlimlerin evsâf-ı Muhammediye'yi İncil'de gösterdiğini nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c001`) — İncil'deki beşaret âyetlerinden örnek vereceğini söyler
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 3. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c003`) — İncil'den Peygamber'e dair beşaret âyeti nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 5. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c005`) — İncil'den Peygamber'e dair beşaret âyeti nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 24. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c024`) — İncil'den Peygamber'e dair beşaret âyeti nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 26. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c026`) — Fetih Sûresi'nin İncil'deki misale işaretini İncil âyetiyle teyit eder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 49. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c049`) — İncil'den Peygamber'e dair beşaret âyeti nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 53. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c053`) — İncil'den Peygamber'e dair beşaret âyeti nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 59. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c059`) — İncil'den Peygamber'e dair beşaret âyeti nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 61. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c061`) — İncil'den Peygamber'e dair beşaret âyeti nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 63. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c063`) — İncil'den Peygamber'e dair beşaret âyeti nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 75. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c075`) — İncil'den Peygamber'e dair beşaret âyeti nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 77. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c077`) — İncil'den Peygamber'e dair beşaret âyeti nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 81. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c081`) — İncil'den Peygamber'e dair beşaret âyeti nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 82. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c082`) — İncil'den Peygamber'e dair beşaret âyeti nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 83. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c083`) — İncil'den Peygamber'e dair beşaret âyeti nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 88. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c088`) — İncil'den Peygamber'e dair beşaret âyeti nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 88. cümle › Hâşiye › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c088/h1/c001`) — Evliya Çelebi'nin eski bir İncil'de okuduğu beşareti nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 98. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c098`) — İncil ve diğer kitaplarda âhir peygambere dair çok âyet olduğunu söyler
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › İkinci Kısım › 35. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-02/c035`) — Peygamber'in sıfatını İncil'de gördüğünü söyleyen kişinin sözünü nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › İkinci Kısım › 36. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-02/c036`) — Peygamber'in sıfatını İncil'de gördüğünü söyleyen kişinin sözünü nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) Zeylinin Bir Parçasıdır › 6. cümle (`mektubat/19/zeyl-02/c006`) — Hüseyin Cisrî'nin İncil'den çıkardığı beşaretlere dayanır
- nakil · müellif · Mesnevî-i Nuriye › Habbe › İkinci misâl › 217. cümle (`mesnevi-i-nuriye/habbe/misal-02/c217`) — Peygamberin İncil'deki adının Ahmed olduğunu nakleder
- nakil · müellif · Sözler › Yirmiyedinci Söz › Yirmiyedinci Söz’ün Zeyli › 15. cümle (`sozler/27/zeyl/c015`) — Sahâbenin İncil'de medhedildiğini söyler
- nakil · müellif · Sözler › Otuzbirinci Söz › Üçüncü Esâs › İkinci Temsîl › 30. cümle (`sozler/31/esas-03/temsil-02/c030`) — Hüseyin Cisrî'nin İncil'den çıkardığı beşaretlere dayanır
- nakil · müellif · Şualar › Onbeşinci Şuâ › Birinci Makam › Üçüncü Medrese‑i Yûsufiye’nin Tek Bir Dersinin Üçüncü Kısmı › İkinci İşâret › Onüçüncü Şehâdet › 5. cümle (`sualar/15/makam-01/kisim-03/isaret-02/sehadet-13/c005`) — İncil'in nübüvvete dair âyetlerinin Ondokuzuncu Mektub'da yazıldığını söyler
- nakil · müellif · Şualar › Yedinci Şuâ › Âyetü'l‑Kübrâ › Birinci Bâb (Berâhin‑i Ulûhiyet) › Onaltıncı Mertebe (Muhammed‑i Arabî(asm)) › Dördüncüsü › 3. cümle (`sualar/7/ayetul-kubra/bab-01/mertebe-16/isaret-04/c003`) — Enbiyânın İncil'de verdiği beşarete dayanır, tafsili Ondokuzuncu Mektub'a
- nakil · müellif · Tarihçe-i Hayat › Dördüncü Kısım Kastamonu Hayatı › Âyetü'l‑Kübrâ › Onaltıncı Mertebe (Muhammed‑i Arabî(asm)) › Dördüncüsü › 3. cümle (`tarihce-i-hayat/dorduncu-kisim-kastamonu-hayati/ayetul-kubra/mertebe-16/isaret-04/c003`) — Enbiyânın İncil'de verdiği beşarete dayanır, tafsili Ondokuzuncu Mektub'a
- nakil · müellif · Zülfikâr › On Dokuzuncu Mektub › BU PARÇA ALTUN VE ELMAS İLE YAZILSA LİYAKATI VAR › ON ALTINCI İŞARET › Üçüncü Hüccet › 13. cümle (`zulfikar/mektub-19/bu-parca-altun-ve-elmas/isaret-16/huccet-03/c013`) — İncil'de Peygamber'in isimlerini nakleder
- nakil · müellif · Zülfikâr › On Dokuzuncu Mektub › BU PARÇA ALTUN VE ELMAS İLE YAZILSA LİYAKATI VAR › ON ALTINCI İŞARET › Üçüncü Hüccet › 15. cümle (`zulfikar/mektub-19/bu-parca-altun-ve-elmas/isaret-16/huccet-03/c015`) — İncil'de Peygamber'in isimlerini nakleder
- nakil · müellif · Zülfikâr › On Dokuzuncu Mektub › BU PARÇA ALTUN VE ELMAS İLE YAZILSA LİYAKATI VAR › ON ALTINCI İŞARET › Üçüncü Hüccet › 19. cümle (`zulfikar/mektub-19/bu-parca-altun-ve-elmas/isaret-16/huccet-03/c019`) — İncil'de Peygamber'in isimlerini nakleder
- nakil · müellif · Zülfikâr › On Dokuzuncu Mektub › Mu'cizat-ı Ahmediye (A.S.M.) Zeylinin Bir Parçasıdır › 1. cümle (`zulfikar/mektub-19/mucizat-i-ahmediye-a-s-m-zeylinin-bir/c001`) — Hüseyin Cisrî'nin İncil'den çıkardığı beşaretlere dayanır
- değerlendirme · başka · İşaratü'l-İ'caz › Ecnebî Feylesofların Kur'ânı Tasdiklerine Dair Şehâdetleri › Zamanlar Geçtikçe, Kur'ânın Ulvî Sırları İnkişaf Ediyor › 30. cümle (`isaratul-icaz/ecnebi-feylesoflarin-kurani-tasdiklerine-dair/zamanlar-gectikce-kuranin-ulvi-sirlari/c030`) — Ecnebî yazarın sözü: İncil hakkında şüpheler ileri sürüldüğü
- değerlendirme · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › İkinci Hüccet › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-02/c001`) — İncil ibarelerine tercümelerle yabancı kelimeler karıştığını söyler
- değerlendirme · müellif · Muhakemat › Birinci Makale › Dördüncü Mes'ele › 32. cümle (`muhakemat/makale-01/mesele-04/c032`) — Muharref İncil'deki kıssaları kabulün ismet-i enbiyâya aykırılığını söyler
- değerlendirme · müellif · Muhakemat › Birinci Makale › Üçüncü Mukaddeme › 16. cümle (`muhakemat/makale-01/mukaddeme-03/c016`) — Kıssaları muharref İncil'in Kur'ân tefsirine esas olamayacağını söyler
- değerlendirme · başka · Nur'un İlk Kapısı › Ecnebî Feylesofların Kur'ân’ı Tasdiklerine Dair Şehâdetleri › Zamanlar Geçtikçe, Kur'ân’ın Ulvî Sırları İnkişaf Ediyor › 30. cümle (`nurun-ilk-kapisi/ecnebi-feylesoflarin-kurani-tasdiklerine-dair/zamanlar-gectikce-kuranin-ulvi-sirlari/c030`) — Ecnebî yazarın sözü: İncil hakkında şüpheler ileri sürüldüğü
- değerlendirme · müellif · Şualar › Beşinci Şuâ › Mukaddime › Dördüncü Nokta › 10. cümle (`sualar/5/mukaddime/nokta-04/c010`) — İncil'deki müjdelerin perdeli ve kapalı geldiğini söyler
- anma · müellif · Âsâr-ı Bediiyye › Lemeât › Yedinci Menba' ise › 201. cümle (`asar-i-bediiyye/lemeat/yedinci-menba-ise/c201`) — Allah'ın kelâmları arasında İncil'i sayar
- anma · müellif · el-Mesnevî el-Arabî en-Nurî › رَشَــحَــاتٌ › اَلرَّشْحَةُ الثَّانِيَةُ › 2. cümle (`el-mesnevi-el-arabi/reshalar/resha-02/c002`) — Semavî kitapların beşaretleri arasında İncil'i sayar
- anma · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › İnsanın fıtratındaki merak, insaniyet damarıyla sizin farz vazifeniz zararına o geniş boğuşmalara sevk ediyor › 29. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/30/c029`) — Hıristiyanlığın İncil'le Kur'ân'a tâbi olup ittifakını ümit eder
- anma · talebe · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Yedi seneden beri ateş püsküren zâlim beşerin hâli, bugün daha çok ızdırâblı bir hâle girmiş bulunuyor › 23. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/36/c023`) — İncil'in Kur'ân'la ittihadıyla dinsizliğin yenileceğini söyler
- anma · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye’nin Birinci Zeyli › İkinci Reşha › 1. cümle (`mektubat/19/zeyl-01/resha-02/c001`) — Kütüb-ü semâviye arasında İncil'in işaratını anar
- anma · müellif · Nur'un İlk Kapısı › Ondördüncü Ders › Ondördüncü Lem'a › İkinci Reşha › 1. cümle (`nurun-ilk-kapisi/ders-14/lema-14/resha-02/c001`) — Kütüb-ü semâviye arasında İncil'in işaratını anar
- anma · müellif · Sözler › Ondokuzuncu Söz › İkinci Reşha › 2. cümle (`sozler/19/resha-02/c002`) — Kütüb-ü semâviye arasında İncil'in işaratını anar
- anma · müellif · Sözler › Yirmibeşinci Söz › Birinci Şu'le › Üçüncü Şuâ › Birinci Cilve › Birinci Şavk › 1. cümle (`sozler/25/sule-01/sua-03/cilve-01/savk-01/c001`) — Kur'ân'ın kıssaları Tevrat ve İncil'in tasdiki altında anlattığını söyler
- anma · talebe · Tarihçe-i Hayat › Altıncı Kısım Emirdağı Hayatı › Yedi seneden beri ateş püsküren zâlim beşerin hâli, bugün daha çok ızdırâblı bir hâle girmiş bulunuyor › 24. cümle (`tarihce-i-hayat/altinci-kisim-emirdagi-hayati/yedi-seneden-beri-ates-puskuren/c024`) — İncil'in Kur'ân'la ittihadıyla dinsizliğin yenileceğini söyler
- anma · müellif · Zülfikâr › ZÜLFİKAR › Bu Mecmua Üç Makam ve Bir Hatimedir › İkinci Esas › 3. cümle (`zulfikar/zulfikar/hatime/esas-02/c003`) — Bir misyonerin İncil-i Yuhanna atfındaki rakam hatasını gösterdiğini anlatır

**Tevrat** (—): 52

- nakil · müellif · Barla Lahikası › Mektûbat’ın Üçüncü Kısmı › Mesail‑i Müteferrika (Altı Mes'ele hâlinde bazı suallere cevap verir ve bazı konuları açıklar) › Beşinci Mes'ele › 33. cümle (`barla-lahikasi/kisim-03/220/mesele-05/c033`) — Fetih âyetinin Tevrat'ı şahit göstermesini anlatır
- nakil · müellif · el-Mesnevî el-Arabî en-Nurî › حَــــبَّــــةٌ › 254. cümle (`el-mesnevi-el-arabi/habbe/c254`) — Peygamberin Tevrat'taki adının Ahyed olduğunu nakleder
- nakil · müellif · İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 2. Âyetin Tefsiri › مقدمة › 11. cümle (`isaratul-icaz-arabi/sure-i-bakara/2/mukaddime/c011`) — Âyetteki işaretin Tevrat'ta müjdelenen Kur'ân'a dönebileceğini söyler
- nakil · müellif · İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 2. Âyetin Tefsiri › مقدمة › 12. cümle (`isaratul-icaz-arabi/sure-i-bakara/2/mukaddime/c012`) — Âyetteki işaretin Tevrat'ta müjdelenen Kur'ân'a dönebileceğini söyler
- nakil · müellif · Lem'alar › Yedinci Lem'a › Bu Tetimmeye İkinci Bir İzâh › 10. cümle (`lemalar/7/bu-tetimmeye-ikinci-bir-izah/c010`) — Ehl-i Suffa gibilerin Tevrat'ın senasına mazhar olduğunu söyler
- nakil · müellif · Lem'alar › Yedinci Lem'a › Altıncısı › 2. cümle (`lemalar/7/vecih-06/c002`) — Tevrat'taki sahâbe vasfını nakleder
- nakil · müellif · Lem'alar › Yedinci Lem'a › Altıncısı › 3. cümle (`lemalar/7/vecih-06/c003`) — Tevrat'taki sahâbe vasfını nakleder
- nakil · müellif · Lem'alar › Yedinci Lem'a › Altıncısı › 5. cümle (`lemalar/7/vecih-06/c005`) — Tahrifata rağmen Tevrat'ın Fetih âyetini tasdik ettiğini söyler
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Âyetü'l‑Kübrâ Risalesi’nin Risalet-i Ahmediye’den Bahseden Onaltıncı Mertebesi › Dördüncüsü › 3. cümle (`mektubat/19/mertebe-16/isaret-04/c003`) — Enbiyânın Tevrat'ta verdiği beşarete dayanır, tafsili Ondokuzuncu Mektub'a
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/c001`) — Tevrat'ın nübüvvet-i Ahmediye'ye dair haberlerini konu edinir
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › İkinci Hüccet › 13. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-02/c013`) — Müslüman olan âlimlerin evsâf-ı Muhammediye'yi Tevrat'ta gösterdiğini nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › İkinci Hüccet › 25. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-02/c025`) — Râhibin, Peygamber'in vasıflarının Tevrat'ta mezkûr olduğu sözünü nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c001`) — Tevrat'taki beşaret âyetlerinden örnek vereceğini söyler
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 7. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c007`) — Tevrat'tan Peygamber'e dair beşaret âyeti nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 9. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c009`) — Tevrat'tan Peygamber'e dair beşaret âyeti nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 13. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c013`) — Tevrat'tan Peygamber'e dair beşaret âyeti nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 18. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c018`) — Abdullah b. Selâm ve Kâ'b'ın Tevrat'tan gösterdiği âyeti nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 20. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c020`) — Tevrat'tan Peygamber'e dair beşaret âyeti nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 22. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c022`) — Tevrat'tan Peygamber'e dair beşaret âyeti nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 23. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c023`) — Tevrat'tan Peygamber'e dair beşaret âyeti nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 27. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c027`) — Tevrat'tan Peygamber'e dair beşaret âyeti nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 30. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c030`) — Tevrat'ın sahâbe hakkındaki âyetini nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 71. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c071`) — Tevrat'ta Peygamber'in isimlerini nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 72. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c072`) — Tevrat'ta Peygamber'in isimlerini nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 73. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c073`) — Tevrat'ta Peygamber'in isimlerini nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 98. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c098`) — Tevrat ve diğer kitaplarda âhir peygambere dair çok âyet olduğunu söyler
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) Zeylinin Bir Parçasıdır › 6. cümle (`mektubat/19/zeyl-02/c006`) — Hüseyin Cisrî'nin Tevrat'tan çıkardığı beşaretlere dayanır
- nakil · müellif · Mesnevî-i Nuriye › Habbe › İkinci misâl › 217. cümle (`mesnevi-i-nuriye/habbe/misal-02/c217`) — Peygamberin Tevrat'taki adının Ahyed olduğunu nakleder
- nakil · müellif · Sözler › Yirmiyedinci Söz › Yirmiyedinci Söz’ün Zeyli › 15. cümle (`sozler/27/zeyl/c015`) — Sahâbenin Tevrat'ta medhedildiğini söyler
- nakil · müellif · Sözler › Otuzbirinci Söz › Üçüncü Esâs › İkinci Temsîl › 30. cümle (`sozler/31/esas-03/temsil-02/c030`) — Hüseyin Cisrî'nin Tevrat'tan çıkardığı beşaretlere dayanır
- nakil · müellif · Şualar › Onbeşinci Şuâ › Birinci Makam › Üçüncü Medrese‑i Yûsufiye’nin Tek Bir Dersinin Üçüncü Kısmı › İkinci İşâret › Onüçüncü Şehâdet › 5. cümle (`sualar/15/makam-01/kisim-03/isaret-02/sehadet-13/c005`) — Tevrat'ın nübüvvete dair âyetlerinin Ondokuzuncu Mektub'da yazıldığını söyler
- nakil · müellif · Şualar › Yedinci Şuâ › Âyetü'l‑Kübrâ › Birinci Bâb (Berâhin‑i Ulûhiyet) › Onaltıncı Mertebe (Muhammed‑i Arabî(asm)) › Dördüncüsü › 3. cümle (`sualar/7/ayetul-kubra/bab-01/mertebe-16/isaret-04/c003`) — Enbiyânın Tevrat'ta verdiği beşarete dayanır, tafsili Ondokuzuncu Mektub'a
- nakil · müellif · Tarihçe-i Hayat › Dördüncü Kısım Kastamonu Hayatı › Âyetü'l‑Kübrâ › Onaltıncı Mertebe (Muhammed‑i Arabî(asm)) › Dördüncüsü › 3. cümle (`tarihce-i-hayat/dorduncu-kisim-kastamonu-hayati/ayetul-kubra/mertebe-16/isaret-04/c003`) — Enbiyânın Tevrat'ta verdiği beşarete dayanır, tafsili Ondokuzuncu Mektub'a
- nakil · müellif · Zülfikâr › On Dokuzuncu Mektub › BU PARÇA ALTUN VE ELMAS İLE YAZILSA LİYAKATI VAR › ON ALTINCI İŞARET › Üçüncü Hüccet › 6. cümle (`zulfikar/mektub-19/bu-parca-altun-ve-elmas/isaret-16/huccet-03/c006`) — Tevrat'ta Peygamber'in isimlerini nakleder
- nakil · müellif · Zülfikâr › On Dokuzuncu Mektub › BU PARÇA ALTUN VE ELMAS İLE YAZILSA LİYAKATI VAR › ON ALTINCI İŞARET › Üçüncü Hüccet › 8. cümle (`zulfikar/mektub-19/bu-parca-altun-ve-elmas/isaret-16/huccet-03/c008`) — Tevrat'ta Peygamber'in isimlerini nakleder
- nakil · müellif · Zülfikâr › On Dokuzuncu Mektub › BU PARÇA ALTUN VE ELMAS İLE YAZILSA LİYAKATI VAR › ON ALTINCI İŞARET › Üçüncü Hüccet › 9. cümle (`zulfikar/mektub-19/bu-parca-altun-ve-elmas/isaret-16/huccet-03/c009`) — Tevrat'ta Peygamber'in isimlerini nakleder
- nakil · müellif · Zülfikâr › On Dokuzuncu Mektub › BU PARÇA ALTUN VE ELMAS İLE YAZILSA LİYAKATI VAR › ON ALTINCI İŞARET › Üçüncü Hüccet › 10. cümle (`zulfikar/mektub-19/bu-parca-altun-ve-elmas/isaret-16/huccet-03/c010`) — Tevrat'ta Peygamber'in isimlerini nakleder
- nakil · müellif · Zülfikâr › On Dokuzuncu Mektub › BU PARÇA ALTUN VE ELMAS İLE YAZILSA LİYAKATI VAR › ON ALTINCI İŞARET › Üçüncü Hüccet › 11. cümle (`zulfikar/mektub-19/bu-parca-altun-ve-elmas/isaret-16/huccet-03/c011`) — Tevrat'ta Peygamber'in isimlerini nakleder
- nakil · müellif · Zülfikâr › On Dokuzuncu Mektub › Mu'cizat-ı Ahmediye (A.S.M.) Zeylinin Bir Parçasıdır › 1. cümle (`zulfikar/mektub-19/mucizat-i-ahmediye-a-s-m-zeylinin-bir/c001`) — Hüseyin Cisrî'nin Tevrat'tan çıkardığı beşaretlere dayanır
- değerlendirme · başka · İşaratü'l-İ'caz › Ecnebî Feylesofların Kur'ânı Tasdiklerine Dair Şehâdetleri › Zamanlar Geçtikçe, Kur'ânın Ulvî Sırları İnkişaf Ediyor › 30. cümle (`isaratul-icaz/ecnebi-feylesoflarin-kurani-tasdiklerine-dair/zamanlar-gectikce-kuranin-ulvi-sirlari/c030`) — Ecnebî yazarın sözü: Tevrat hakkında şüpheler ileri sürüldüğü
- değerlendirme · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › İkinci Hüccet › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-02/c001`) — Tevrat ibarelerine tercümelerle yabancı kelimeler karıştığını söyler
- değerlendirme · müellif · Muhakemat › Birinci Makale › Dördüncü Mes'ele › 32. cümle (`muhakemat/makale-01/mesele-04/c032`) — Muharref Tevrat'taki kıssaları kabulün ismet-i enbiyâya aykırılığını söyler
- değerlendirme · müellif · Muhakemat › Birinci Makale › Üçüncü Mukaddeme › 16. cümle (`muhakemat/makale-01/mukaddeme-03/c016`) — Kıssaları muharref Tevrat'ın Kur'ân tefsirine esas olamayacağını söyler
- değerlendirme · başka · Nur'un İlk Kapısı › Ecnebî Feylesofların Kur'ân’ı Tasdiklerine Dair Şehâdetleri › Zamanlar Geçtikçe, Kur'ân’ın Ulvî Sırları İnkişaf Ediyor › 30. cümle (`nurun-ilk-kapisi/ecnebi-feylesoflarin-kurani-tasdiklerine-dair/zamanlar-gectikce-kuranin-ulvi-sirlari/c030`) — Ecnebî yazarın sözü: Tevrat hakkında şüpheler ileri sürüldüğü
- değerlendirme · müellif · Şualar › Beşinci Şuâ › Mukaddime › Dördüncü Nokta › 10. cümle (`sualar/5/mukaddime/nokta-04/c010`) — Tevrat'taki müjdelerin perdeli ve kapalı geldiğini söyler
- anma · müellif · Âsâr-ı Bediiyye › Lemeât › Yedinci Menba' ise › 201. cümle (`asar-i-bediiyye/lemeat/yedinci-menba-ise/c201`) — Allah'ın kelâmları arasında Tevrat'ı sayar
- anma · müellif · el-Mesnevî el-Arabî en-Nurî › رَشَــحَــاتٌ › اَلرَّشْحَةُ الثَّانِيَةُ › 2. cümle (`el-mesnevi-el-arabi/reshalar/resha-02/c002`) — Semavî kitapların beşaretleri arasında Tevrat'ı sayar
- anma · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Birinci Hüccet › 3. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-01/c003`) — Kur'ân'ın Yahudilere 'Tevrat'ı getirin' meydan okumasını anar
- anma · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye’nin Birinci Zeyli › İkinci Reşha › 1. cümle (`mektubat/19/zeyl-01/resha-02/c001`) — Kütüb-ü semâviye arasında Tevrat'ın işaratını anar
- anma · müellif · Nur'un İlk Kapısı › Ondördüncü Ders › Ondördüncü Lem'a › İkinci Reşha › 1. cümle (`nurun-ilk-kapisi/ders-14/lema-14/resha-02/c001`) — Kütüb-ü semâviye arasında Tevrat'ın işaratını anar
- anma · müellif · Sözler › Ondokuzuncu Söz › İkinci Reşha › 2. cümle (`sozler/19/resha-02/c002`) — Kütüb-ü semâviye arasında Tevrat'ın işaratını anar
- anma · müellif · Sözler › Yirmibeşinci Söz › Birinci Şu'le › Üçüncü Şuâ › Birinci Cilve › Birinci Şavk › 1. cümle (`sozler/25/sule-01/sua-03/cilve-01/savk-01/c001`) — Kur'ân'ın kıssaları Tevrat ve İncil'in tasdiki altında anlattığını söyler

**Suhuf (İbrâhîm, Şuayb…)** (—): 43

- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Âyetü'l‑Kübrâ Risalesi’nin Risalet-i Ahmediye’den Bahseden Onaltıncı Mertebesi › Dördüncüsü › 3. cümle (`mektubat/19/mertebe-16/isaret-04/c003`) — Peygamberlerin suhuflarında Peygamber'in beşaretlerini bildirip 19. Mektub'a gönderir
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/c001`) — Eski kitapların Peygamber'e dair haberlerini konu olarak açar
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 70. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c070`) — Hz. Şuayb'ın suhufunda Peygamber'in ismini "Müşeffah" diye nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 72. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c072`) — Suhuf-u İbrahim ve Tevrat'ta Peygamber'in ismini nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 98. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c098`) — Eski kitaplarda âhir zaman peygamberine dair âyetler bulunduğunu bildirir
- nakil · belirsiz · Sözler › Fihrist › Sekizinci Söz › 1. cümle (`sozler/fihrist/soz-08/c001`) — Sekizinci Söz'ün temsilinin aslının Suhuf-u İbrahim'de bulunduğunu söyler
- nakil · müellif · Şualar › Yedinci Şuâ › Âyetü'l‑Kübrâ › Birinci Bâb (Berâhin‑i Ulûhiyet) › Onaltıncı Mertebe (Muhammed‑i Arabî(asm)) › Dördüncüsü › 3. cümle (`sualar/7/ayetul-kubra/bab-01/mertebe-16/isaret-04/c003`) — Peygamberlerin suhuflarında Peygamber'in beşaretlerini bildirip 19. Mektub'a gönderir
- nakil · müellif · Tarihçe-i Hayat › Dördüncü Kısım Kastamonu Hayatı › Âyetü'l‑Kübrâ › Onaltıncı Mertebe (Muhammed‑i Arabî(asm)) › Dördüncüsü › 3. cümle (`tarihce-i-hayat/dorduncu-kisim-kastamonu-hayati/ayetul-kubra/mertebe-16/isaret-04/c003`) — Peygamberlerin suhuflarında Peygamber'in beşaretlerini bildirip 19. Mektub'a gönderir
- nakil · müellif · Zülfikâr › On Dokuzuncu Mektub › BU PARÇA ALTUN VE ELMAS İLE YAZILSA LİYAKATI VAR › ON ALTINCI İŞARET › Üçüncü Hüccet › 5. cümle (`zulfikar/mektub-19/bu-parca-altun-ve-elmas/isaret-16/huccet-03/c005`) — Hz. Şuayb'ın suhufunda Peygamber'in ismini nakleder
- nakil · müellif · Zülfikâr › On Dokuzuncu Mektub › BU PARÇA ALTUN VE ELMAS İLE YAZILSA LİYAKATI VAR › ON ALTINCI İŞARET › Üçüncü Hüccet › 10. cümle (`zulfikar/mektub-19/bu-parca-altun-ve-elmas/isaret-16/huccet-03/c010`) — Suhuf-u İbrahim ve Tevrat'ta Peygamber'in "Mazmaz" ismini nakleder
- anma · müellif · Âsâr-ı Bediiyye › Lemeât › Yedinci Menba' ise › 201. cümle (`asar-i-bediiyye/lemeat/yedinci-menba-ise/c201`) — Tevrat, Zebur, Suhuf, İncil ve Kur'ân'ı sayar
- anma · müellif · Barla Lahikası › Mektûbat’ın Üçüncü Kısmı › Bu birbiri içinde üç nevi mahlûkatın ömürleri, saatin içindeki dakika, saniye, saatleri sayan çarkların nisbeti gibidir › Birinci Esâs › 4. cümle (`barla-lahikasi/kisim-03/250/esas-01/c004`) — Kur'ân hakikatinin peygamberlerin suhufunda neşrolduğunu anar
- anma · belirsiz · Barla Lahikası › Yirmiyedinci Mektûb’un Üçüncü Kısmı ve Üçüncü Zeylin Nihâyetidir › Bu nurlu eserler hem okşamak hem korkutmak gibi iki zıt tesiri hâizdir › 21. cümle (`barla-lahikasi/yirmiyedinci-mektubun-ucuncu-kismi-ve/118/c021`) — Kütüb ve suhufun indirilmesinde meleklerin vasıtalığını anar
- anma · müellif · İşaratü'l-İ'caz › Mukaddemât › Kur'ân Nedir? Ta'rifi Nasıldır? › 33. cümle (`isaratul-icaz/mukaddemat/kuran-nedir-tarifi-nasildir/c033`) — Kur'ân'dan sonra peygamberlerin kitap ve suhuflarının derecesini anar
- anma · müellif · Lem'alar › Yirmi Dokuzuncu Lem'a › اَلْبَابُ الثَّالِثُ › اَلْمَرْتَبَةُ السَّابِعَةُ › 3. cümle › Hâşiye › 10. cümle (`lemalar/29/bab-03/mertebe-07/c003/h1/c010`) — Bütün kütüb ve suhufun tevhide şehadetini genel olarak anar
- anma · müellif · Lem'alar › Yirmi Dokuzuncu Lem'a › اَلْبَابُ الثَّالِثُ › اَلْمَرْتَبَةُ السَّابِعَةُ › 6. cümle › Hâşiye › 1. cümle (`lemalar/29/bab-03/mertebe-07/c006/h1/c001`) — Bütün kütüb ve suhufun tevhide şehadetini genel olarak anar
- anma · müellif · Lem'alar › Münâcât › Sekizinci Fıkra (Enbiyâ, Evliyâ, Asfiyâ) › 7. cümle (`lemalar/munacat/fikra-08/c007`) — Suhuf ve kütüb-ü mukaddesedeki va'dlere dayanmayı genel olarak anar
- anma · müellif · Mektubat › Yirminci Mektûb › İkinci Makam › Birinci Kelime › 9. cümle (`mektubat/20/makam-02/kelime-01/c009`) — Bütün kütüb ve suhufun tevhide şehadetini genel olarak anar
- anma · müellif · Mektubat › Yirminci Mektûb › İkinci Makam › Birinci Kelime › 11. cümle (`mektubat/20/makam-02/kelime-01/c011`) — Bütün kütüb ve suhufun tevhide şehadetini genel olarak anar
- anma · müellif · Rumuzat-ı Semaniye › Yirmi Dokuzuncu Mektub'un Sekizinci Kısmı › Yirmi Dokuzuncu Mektub'un Sekizinci Kısmı'nın Üçüncü Remzi › Birinci Kısım › İkinci Letafet › 15. cümle (`rumuzat-i-semaniye/kisim-08/remiz-03/kisim-01/letafet-02/c015`) — Suhuf-u enbiyânın sayısına harf tevafukunu anar
- anma · müellif · Rumuzat-ı Semaniye › Yirmi Dokuzuncu Mektub'un Sekizinci Kısmı › Yirmi Dokuzuncu Mektub'un Sekizinci Kısmı'nın Üçüncü Remzi › Birinci Kısım › Üçüncü Letafet › 8. cümle (`rumuzat-i-semaniye/kisim-08/remiz-03/kisim-01/letafet-03/c008`) — Suhuf-u enbiyânın sayısına harf tevafukunu anar
- anma · müellif · Rumuzat-ı Semaniye › Yirmi Dokuzuncu Mektub'un Sekizinci Kısmı › Yirmi Dokuzuncu Mektub'un Sekizinci Kısmı'nın Sekizinci Remzi › 28. cümle (`rumuzat-i-semaniye/kisim-08/remiz-08/c028`) — Suhuf-u enbiyânın sayısına harf tevafukunu anar
- anma · müellif · Sözler › Onuncu Söz › Zeylin Birinci Parçası › İkinci Nokta › 19. cümle (`sozler/10/parca-01/nokta-02/c019`) — Semâvî suhufların haşri kısaca beyan edip Kur'ân'ı tasdikini söyler
- anma · müellif · Sözler › Onuncu Söz › Zeylin Birinci Parçası › İkinci Nokta › 24. cümle (`sozler/10/parca-01/nokta-02/c024`) — Suhuf ve kütüb-ü mukaddesedeki va'dlere dayanmayı genel olarak anar
- anma · müellif · Sözler › Onikinci Söz › Dördüncü Esâs › İkinci temsîl › 41. cümle (`sozler/12/esas-04/temsil-02/c041`) — Suhuf-u semâviyenin Kur'ân'dan sonraki derecesini anar
- anma · müellif · Sözler › Onüçüncü Söz › Onüçüncü Söz’ün İkinci Makamı › Risale‑i Nur Mîzanlarından Onüçüncü Söz’ün İkinci Makamının Hâşiyesidir › Risale‑i Nur’daki Hakîki Tesellîye Mahpuslar Çok Muhtaçtırlar › 19. cümle (`sozler/13/makam-02/hasiye/risale-i-nurdaki-hakiki-teselliye-mahpuslar/c019`) — Kütüb ve suhufun ebedî gençliği müjdelediğini genel olarak söyler
- anma · müellif · Sözler › Yirmibeşinci Söz › Mukaddime › İkinci Cüz' ve Tetimme‑i Ta'rif › 11. cümle (`sozler/25/mukaddime/cuz-02/c011`) — Kur'ân'dan sonra peygamberlerin kitap ve suhuflarının derecesini anar
- anma · müellif · Şualar › Meyve Risalesi › Dokuzuncu Mes'ele › Birinci Nokta › 15. cümle (`sualar/11/mesele-09/nokta-01/c015`) — Allah'ın suhuf ve kitap göndermesini genel olarak anar
- anma · müellif · Şualar › Meyve Risalesi › Dokuzuncu Mes'ele › İkinci Nokta › 1. cümle (`sualar/11/mesele-09/nokta-02/c001`) — Bütün semâvî kitap ve suhufların beş-altı esasa döndüğünü söyler
- anma · müellif · Şualar › Ondördüncü Şuâ › Gençlik Rehberinin Küçük Bir Hâşiyesi › 15. cümle (`sualar/14/hasiye/c015`) — Kütüb ve suhufun ebedî gençliği müjdelediğini genel olarak söyler
- anma · müellif · Şualar › Onbeşinci Şuâ › Birinci Makam › Fâtiha‑i Şerîfe’nin Bir Muhtasar Hülâsası › Dördüncü Kelime › Sâniyen › 1. cümle (`sualar/15/makam-01/kisim-02/kelime-04/saniyen/c001`) — Suhufun âhirete şehadetini genel olarak anar
- anma · müellif · Şualar › Onbeşinci Şuâ › Birinci Makam › Üçüncü Medrese‑i Yûsufiye’nin Tek Bir Dersinin Üçüncü Kısmı › İkinci İşâret › Dördüncü Şehâdet › 3. cümle (`sualar/15/makam-01/kisim-03/isaret-02/sehadet-04/c003`) — Kur'ân'ın kütüb ve suhufun tasdikine mazhar olduğunu anar
- anma · müellif · Şualar › Üçüncü Şuâ › Sekizinci Fıkra (Enbiyâ, Evliyâ, Asfiyâ) › 7. cümle (`sualar/3/fikra-08/c007`) — Suhuf ve kütüb-ü mukaddesedeki va'dlere dayanmayı genel olarak anar
- anma · müellif · Şualar › Dördüncü Şuâ › Üçüncü Mertebe‑i Nuriye-i Hasbiye › 18. cümle (`sualar/4/ucuncu-mertebe-i-nuriye-i-hasbiye/c018`) — Mukaddes kitap ve suhufların icmâını genel olarak anar
- anma · müellif · Şualar › Yedinci Şuâ › Âyetü'l‑Kübrâ › Birinci Bâb (Berâhin‑i Ulûhiyet) › Sekizinci Mertebe (Enbiyâlar) › 8. cümle (`sualar/7/ayetul-kubra/bab-01/mertebe-08/c008`) — Peygamberlerin elindeki kitap ve suhufları delil olarak anar
- anma · müellif · Şualar › Yedinci Şuâ › Âyetü'l‑Kübrâ › Birinci Bâb (Berâhin‑i Ulûhiyet) › Ondördüncü ve Onbeşinci Mertebe (Âlem‑i Gayb) › Vahiylerin Hakikati › 6. cümle (`sualar/7/ayetul-kubra/bab-01/ondorduncu-ve-onbesinci-mertebe-alem-i/vahiylerin-hakikati/c006`) — Kütüb-ü mukaddese ve suhufu vahyin delilleri arasında anar
- anma · müellif · Şualar › Sekizinci Şuâ › Birincisi › 30. cümle (`sualar/8/remiz-01/c030`) — Celcelûtiye'deki yüz on semâvî suhufu Risale'ye işaret için anar
- anma · müellif · Şualar › Dokuzuncu Şuâ › Mukaddime › İkinci Nokta › 20. cümle (`sualar/9/mukaddime/nokta-02/c020`) — Semâvî suhufların haşri kısaca beyan edip Kur'ân'ı tasdikini söyler
- anma · müellif · Şualar › Dokuzuncu Şuâ › Mukaddime › İkinci Nokta › 25. cümle (`sualar/9/mukaddime/nokta-02/c025`) — Suhuf ve kütüb-ü mukaddesedeki va'dlere dayanmayı genel olarak anar
- anma · müellif · Tarihçe-i Hayat › Dördüncü Kısım Kastamonu Hayatı › Âyetü'l‑Kübrâ › Sekizinci Mertebe (Enbiyâlar) › 8. cümle (`tarihce-i-hayat/dorduncu-kisim-kastamonu-hayati/ayetul-kubra/mertebe-08/c008`) — Peygamberlerin elindeki kitap ve suhufları delil olarak anar
- anma · müellif · Tarihçe-i Hayat › Dördüncü Kısım Kastamonu Hayatı › Âyetü'l‑Kübrâ › Ondördüncü ve Onbeşinci Mertebe (Âlem‑i Gayb) › Vahiylerin Hakikati › 6. cümle (`tarihce-i-hayat/dorduncu-kisim-kastamonu-hayati/ayetul-kubra/ondorduncu-ve-onbesinci-mertebe-alem-i/vahiylerin-hakikati/c006`) — Kütüb-ü mukaddese ve suhufu vahyin delilleri arasında anar
- anma · müellif · Tarihçe-i Hayat › Dördüncü Kısım Kastamonu Hayatı › Üçüncü Şuâ › Sekizinci Fıkra (Enbiyâ, Evliyâ, Asfiyâ) › 7. cümle (`tarihce-i-hayat/dorduncu-kisim-kastamonu-hayati/sua-03/fikra-08/c007`) — Suhuf ve kütüb-ü mukaddesedeki va'dlere dayanmayı genel olarak anar
- anma · müellif · Zülfikâr › YİRMİ DOKUZUNCU MEKTUP'UN SEKİZİNCİ KISMI'NIN İKİNCİ REMZ'İ › YİRMİ DOKUZUNCU MEKTUP'UN SEKİZİNCİ KISMI'NIN SEKİZİNCİ REMZİ › 15. cümle (`zulfikar/remiz-02/remiz-08/c015`) — Suhuf-u enbiyânın sayısına harf tevafukunu anar

**Zebur** (—): 22

- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c001`) — Peygamber'e ait âyetlerinden nümûneler göstereceğini söyler
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 2. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c002`) — Zebur'dan 'Mukîmü's-Sünne' âyetini nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 17. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c017`) — Zebur'dan Ahmed ve Muhammed adlı peygamber âyetini nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 42. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c042`) — Zebur'un Yetmiş ikinci Bâbından âyet nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 71. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c071`) — Zebur'da Peygamber'in 'El-Muhtâr' adıyla anıldığını nakleder
- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 72. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c072`) — Zebur'da 'Mukîmü's-Sünne' ismini nakleder
- nakil · müellif · Zülfikâr › On Dokuzuncu Mektub › BU PARÇA ALTUN VE ELMAS İLE YAZILSA LİYAKATI VAR › ON ALTINCI İŞARET › Üçüncü Hüccet › 7. cümle (`zulfikar/mektub-19/bu-parca-altun-ve-elmas/isaret-16/huccet-03/c007`) — Zebur'da 'El-Muhtâr' ismini nakleder
- nakil · müellif · Zülfikâr › On Dokuzuncu Mektub › BU PARÇA ALTUN VE ELMAS İLE YAZILSA LİYAKATI VAR › ON ALTINCI İŞARET › Üçüncü Hüccet › 9. cümle (`zulfikar/mektub-19/bu-parca-altun-ve-elmas/isaret-16/huccet-03/c009`) — Zebur'da 'Mukîmü's-Sünne' ismini nakleder
- değerlendirme · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › İkinci Hüccet › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-02/c001`) — İbarelerine tercümelerle yabancı kelimeler karıştığını söyler
- değerlendirme · müellif · Şualar › Beşinci Şuâ › Mukaddime › Dördüncü Nokta › 10. cümle (`sualar/5/mukaddime/nokta-04/c010`) — Peygamber'e dair müjdelerin perdeli geldiğini söyler
- anma · müellif · Âsâr-ı Bediiyye › Lemeât › Yedinci Menba' ise › 201. cümle (`asar-i-bediiyye/lemeat/yedinci-menba-ise/c201`) — Allah'ın kelâmı olan kitaplar listesinde
- anma · müellif · el-Mesnevî el-Arabî en-Nurî › رَشَــحَــاتٌ › اَلرَّشْحَةُ الثَّانِيَةُ › 2. cümle (`el-mesnevi-el-arabi/reshalar/resha-02/c002`) — Semavî kitapların beşâretleri tevhidi tasdik eder (Arapça)
- anma · talebe · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Hasan Feyzi’nin (rahmetullahi aleyh) bir şiiridir › 35. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/71/c035`) — Şiirde Hz. Dâvud'un Zebur okuması
- anma · müellif · Mektubat › Ondokuzuncu Mektûb › Âyetü'l‑Kübrâ Risalesi’nin Risalet-i Ahmediye’den Bahseden Onaltıncı Mertebesi › Dördüncüsü › 3. cümle (`mektubat/19/mertebe-16/isaret-04/c003`) — Beşâretleri anar, tafsili Ondokuzuncu Mektub'a bırakır
- anma · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › 1. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/c001`) — Bölüm başlığı: semavî kitapların Peygamber'e dair haberi
- anma · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 98. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c098`) — Semavî kitaplarda âhir peygamberden çok bahis olduğunu söyler
- anma · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) Zeylinin Bir Parçasıdır › 6. cümle (`mektubat/19/zeyl-02/c006`) — Kütüb-ü mukaddesedeki beşâretleri Cisrî'nin çıkardığını söyler
- anma · müellif · Sözler › Otuzbirinci Söz › Üçüncü Esâs › İkinci Temsîl › 30. cümle (`sozler/31/esas-03/temsil-02/c030`) — Kütüb-ü mukaddesedeki beşâretleri Cisrî'nin çıkardığını söyler
- anma · müellif · Şualar › Onbeşinci Şuâ › Birinci Makam › Üçüncü Medrese‑i Yûsufiye’nin Tek Bir Dersinin Üçüncü Kısmı › İkinci İşâret › Onüçüncü Şehâdet › 5. cümle (`sualar/15/makam-01/kisim-03/isaret-02/sehadet-13/c005`) — Zebur âyetlerinden yirmisinin Ondokuzuncu Mektub'da olduğunu söyler
- anma · müellif · Şualar › Yedinci Şuâ › Âyetü'l‑Kübrâ › Birinci Bâb (Berâhin‑i Ulûhiyet) › Onaltıncı Mertebe (Muhammed‑i Arabî(asm)) › Dördüncüsü › 3. cümle (`sualar/7/ayetul-kubra/bab-01/mertebe-16/isaret-04/c003`) — Beşâretleri anar, tafsili Ondokuzuncu Mektub'a bırakır
- anma · müellif · Tarihçe-i Hayat › Dördüncü Kısım Kastamonu Hayatı › Âyetü'l‑Kübrâ › Onaltıncı Mertebe (Muhammed‑i Arabî(asm)) › Dördüncüsü › 3. cümle (`tarihce-i-hayat/dorduncu-kisim-kastamonu-hayati/ayetul-kubra/mertebe-16/isaret-04/c003`) — Beşâretleri anar, tafsili Ondokuzuncu Mektub'a bırakır
- anma · müellif · Zülfikâr › On Dokuzuncu Mektub › Mu'cizat-ı Ahmediye (A.S.M.) Zeylinin Bir Parçasıdır › 1. cümle (`zulfikar/mektub-19/mucizat-i-ahmediye-a-s-m-zeylinin-bir/c001`) — Kütüb-ü mukaddesedeki beşâretleri Cisrî'nin çıkardığını söyler

**Kitâb-ı Mukaddes** (—): 2

- değerlendirme · başka · İşaratü'l-İ'caz › Ecnebî Feylesofların Kur'ânı Tasdiklerine Dair Şehâdetleri › Zât‑ı Kibriyâ Hakkındaki Âyetlerin Ulviyeti ve Kur'ânın Kudsî Nezâheti › 6. cümle (`isaratul-icaz/ecnebi-feylesoflarin-kurani-tasdiklerine-dair/zat-i-kibriya-hakkindaki-ayetlerin-ulviyeti/c006`) — Ecnebi yazar Kitab-ı Mukaddes'i noksanlıklarla eleştiriyor.
- değerlendirme · başka · Nur'un İlk Kapısı › Ecnebî Feylesofların Kur'ân’ı Tasdiklerine Dair Şehâdetleri › Zât‑ı Kibriyâ Hakkındaki Âyetlerin Ulviyeti ve Kur'ân’ın Kudsî Nezâheti › 6. cümle (`nurun-ilk-kapisi/ecnebi-feylesoflarin-kurani-tasdiklerine-dair/zat-i-kibriya-hakkindaki-ayetlerin-ulviyeti/c006`) — Ecnebi yazar Kitab-ı Mukaddes'i noksanlıklarla eleştiriyor.

**Kitâb-ı Eş'ıyâ (İşaya)** (—): 2

- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 33. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c033`) — Kitabın kırk ikinci bâbından âyet aktarıyor, nübüvvete delil olarak.
- nakil · müellif · Zülfikâr › On Dokuzuncu Mektub › BU PARÇA ALTUN VE ELMAS İLE YAZILSA LİYAKATI VAR › ON ALTINCI İŞARET › Üçüncü Hüccet › 1. cümle (`zulfikar/mektub-19/bu-parca-altun-ve-elmas/isaret-16/huccet-03/c001`) — Kırk ikinci bâbından ibare aktarılıyor.

**Kitâb-ı Mîhâ (Mika)** (—): 1

- nakil · müellif · Mektubat › Ondokuzuncu Mektûb › Mu'cizât‑ı Ahmediye (asm) › Onaltıncı İşâret › Birinci Kısım › Üçüncü Hüccet › 38. cümle (`mektubat/19/mucizat-i-ahmediye-asm/isaret-16/kisim-01/huccet-03/c038`) — Kitabın dördüncü bâbından âyet aktarıyor.

### Batı ve yeni zaman

**Carlyle** (Thomas Carlyle): 25

- nakil · müellif · Âsâr-ı Bediiyye › Makaleler Kısmı › DOKUZUNCU VEHİM › 240. cümle (`asar-i-bediiyye/makaleler-kismi/vehim-09/c240`) — Carlyle'ın İslâmiyetin kudsiyetini Avrupa'ya duyurduğunu söyler
- nakil · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Âlem‑i İslâmdan Müjdeli Haberler ve Bismarck’ın Fıkrası › 15. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/207/c015`) — Carlyle'ın "Başka kitaplar Kur'ân'a yetişemez" sözünü aktarır
- nakil · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Âlem‑i İslâmdan Müjdeli Haberler ve Bismarck’ın Fıkrası › 16. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/207/c016`) — Carlyle'ın sözünü bitirip ecnebide çok Carlyle'lar çıkacağını söyler
- nakil · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 2 › 1952’de İstanbul’da görülen Gençlik Rehberi mahkemesine, ehl‑i vukufa cevaben verilen itiraznamedir › 113. cümle (`emirdag-lahikasi/emirdag-lahikasi-2/310/c113`) — Müdafaada Hutbe'deki Carlyle ve Bismarck dayanaklı hükmü tekrar eder
- nakil · müellif · Hutbe-i Şamiye › Arabî Hutbe‑i Şâmiye Eserinin Tercümesi › Birinci Kelime: “El‑Emel” › Birinci Cihet Olan Ma'nen Terakkî › 74. cümle (`hutbe-i-samiye/arabi-hutbe-i-samiye-eserinin-tercumesi/kelime-01/birinci-cihet-olan-manen-terakki/c074`) — Carlyle'ın eserlerinde İslâm hakkında yazdığını aktarmaya başlar
- nakil · müellif · Hutbe-i Şamiye › Arabî Hutbe‑i Şâmiye Eserinin Tercümesi › Birinci Kelime: “El‑Emel” › Birinci Cihet Olan Ma'nen Terakkî › 79. cümle (`hutbe-i-samiye/arabi-hutbe-i-samiye-eserinin-tercumesi/kelime-01/birinci-cihet-olan-manen-terakki/c079`) — Carlyle'ın Peygamber'in sözü hakkındaki sözünü aktarır
- nakil · müellif · Hutbe-i Şamiye › Arabî Hutbe‑i Şâmiye Eserinin Tercümesi › Birinci Kelime: “El‑Emel” › Birinci Cihet Olan Ma'nen Terakkî › İkinci Misâl › 10. cümle (`hutbe-i-samiye/arabi-hutbe-i-samiye-eserinin-tercumesi/kelime-01/birinci-cihet-olan-manen-terakki/misal-02/c010`) — Carlyle ve Bismarck'ın sözlerine dayanarak Avrupa'nın İslâm'a gebe olduğunu söyler
- nakil · müellif · Hutbe-i Şamiye › Hutbe‑i Şâmiye’nin Zeylinin Zeyli › Reddü'l‑Evhâm › Beşinci Vehim › 3. cümle › Hâşiye › 1. cümle (`hutbe-i-samiye/zeyl/reddul-evham/vehim-05/c003/h1/c001`) — Hâşiye, Bismarck ve Carlyle'ın malum beyanlarına işaret edildiğini söyler
- nakil · belirsiz · İşaratü'l-İ'caz › Ecnebî Feylesofların Kur'ânı Tasdiklerine Dair Şehâdetleri › Kur'ân, Serâpâ Samîmiyet ve Hakkâniyetle Doludur › 1. cümle (`isaratul-icaz/ecnebi-feylesoflarin-kurani-tasdiklerine-dair/kuran-serapa-samimiyet-ve-hakkaniyetle/c001`) — Carlyle'ın Kur'ân hakkındaki sözünü aktarmaya başlar
- nakil · belirsiz · İşaratü'l-İ'caz › Ecnebî Feylesofların Kur'ânı Tasdiklerine Dair Şehâdetleri › Kur'ân, Serâpâ Samîmiyet ve Hakkâniyetle Doludur › 7. cümle (`isaratul-icaz/ecnebi-feylesoflarin-kurani-tasdiklerine-dair/kuran-serapa-samimiyet-ve-hakkaniyetle/c007`) — Aktarılan sözün sahibi olarak Carlyle'ın adı
- nakil · belirsiz · İşaratü'l-İ'caz › Ecnebî Feylesofların Kur'ânı Tasdiklerine Dair Şehâdetleri › Kur'ânın Cihan‑şümûl Hakikati: Kur'ân, Allah’ın Birliğine İnanmak Hakikat-i Kübrâsını İlân Eder › 3. cümle (`isaratul-icaz/ecnebi-feylesoflarin-kurani-tasdiklerine-dair/kuranin-cihan-sumul-hakikati-kuran-allahin/c003`) — Carlyle'ın Kur'ân'ın ulviyeti hakkındaki sözünü aktarır
- nakil · müellif · İşaratü'l-İ'caz › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri (Nübüvvet Hakkında) › Altıncı Mes'ele › Dördüncü Nükte › 16. cümle (`isaratul-icaz/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-06/nukte-04/c016`) — Carlyle'ın Goethe'den naklen Kur'ân hakkındaki sözünü aktarır
- nakil · müellif · İşaratü'l-İ'caz › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri (Nübüvvet Hakkında) › Altıncı Mes'ele › Dördüncü Nükte › 20. cümle (`isaratul-icaz/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-06/nukte-04/c020`) — Carlyle'ın Goethe'den naklen Kur'ân hakkındaki sözünü aktarır
- nakil · müellif · Makalat › Makale – 16 › LEMEÂN-I HAKİKAT VE İZÂLE-İ ŞÜBEHÂT › 107. cümle (`makalat/makale-16/lemean-i-hakikat-ve-izale-i-subehat/c107`) — Carlyle'ın İslâmiyetin kudsiyetini Avrupa'ya duyurduğunu söyler
- nakil · müellif · Muhakemat › Unsuru'l‑Akîde › İkinci Maksad › Dördüncü Meslek › 33. cümle (`muhakemat/makale-03/maksad-02/meslek-04/c033`) — Carlyle'ın bir Alman hakîminden naklettiği sözü aktarır
- nakil · belirsiz · Nur'un İlk Kapısı › Ecnebî Feylesofların Kur'ân’ı Tasdiklerine Dair Şehâdetleri › Kur'ân, Serâpâ Samîmiyet ve Hakkàniyetle Doludur › 1. cümle (`nurun-ilk-kapisi/ecnebi-feylesoflarin-kurani-tasdiklerine-dair/kuran-serapa-samimiyet-ve-hakk-niyetle/c001`) — Carlyle'ın Kur'ân hakkındaki sözünü aktarmaya başlar
- nakil · belirsiz · Nur'un İlk Kapısı › Ecnebî Feylesofların Kur'ân’ı Tasdiklerine Dair Şehâdetleri › Kur'ân, Serâpâ Samîmiyet ve Hakkàniyetle Doludur › 7. cümle (`nurun-ilk-kapisi/ecnebi-feylesoflarin-kurani-tasdiklerine-dair/kuran-serapa-samimiyet-ve-hakk-niyetle/c007`) — Aktarılan sözün sahibi olarak Carlyle'ın adı
- nakil · belirsiz · Nur'un İlk Kapısı › Ecnebî Feylesofların Kur'ân’ı Tasdiklerine Dair Şehâdetleri › Kur'ânın Cihan‑şümûl Hakikatı: Kur'ân, Allah’ın Birliğine İnanmak Hakikat-i Kübrâsını İlân Eder › 4. cümle (`nurun-ilk-kapisi/ecnebi-feylesoflarin-kurani-tasdiklerine-dair/kuranin-cihan-sumul-hakikati-kuran-allahin/c004`) — Carlyle'ın Kur'ân'ın ulviyeti hakkındaki sözünü aktarır
- nakil · müellif · Tarihçe-i Hayat › Altıncı Kısım Emirdağı Hayatı › Âlem‑i İslâmdan Müjdeli Haberler ve Bismarck’ın Fıkrası › 16. cümle (`tarihce-i-hayat/altinci-kisim-emirdagi-hayati/alem-i-islamdan-mujdeli-haberler-ve/c016`) — Carlyle'ın "Başka kitaplar Kur'ân'a yetişemez" sözünü aktarır
- nakil · müellif · Tarihçe-i Hayat › Altıncı Kısım Emirdağı Hayatı › Âlem‑i İslâmdan Müjdeli Haberler ve Bismarck’ın Fıkrası › 18. cümle (`tarihce-i-hayat/altinci-kisim-emirdagi-hayati/alem-i-islamdan-mujdeli-haberler-ve/c018`) — Carlyle'ın sözünü bitirip ecnebide çok Carlyle'lar çıkacağını söyler
- nakil · talebe · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › Hutbe‑i Şâmiye › Birinci Kelime: “El‑Emel” › Birinci Cihet Olan Ma'nen Terakkî › 44. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/hutbe-i-samiye/kelime-01/birinci-cihet-olan-manen-terakki/c044`) — Derleyici, Bediüzzaman'ın Carlyle'ın sözlerini naklettiğini bildirir
- nakil · müellif · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › Hutbe‑i Şâmiye › Birinci Kelime: “El‑Emel” › Birinci Cihet Olan Ma'nen Terakkî › 45. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/hutbe-i-samiye/kelime-01/birinci-cihet-olan-manen-terakki/c045`) — Carlyle ve Bismarck'ın sözlerine dayanarak hüküm verir
- anma · müellif · Âsâr-ı Bediiyye › ŞUAAT-Ü MARİFET-ÜN NEBÎYY › BEŞİNCİ ŞUA › 4. cümle (`asar-i-bediiyye/suaat-u-marifet-un-nebiyy/sua-05/c004`) — Kur'ân'ı tasdik eden dahiler örneği olarak Goethe ve Carlyle anılır
- anma · belirsiz · İşaratü'l-İ'caz › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri (Nübüvvet Hakkında) › Altıncı Mes'ele › Dördüncü Nükte › 24. cümle › Hâşiye › 1. cümle (`isaratul-icaz/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-06/nukte-04/c024/h1/c001`) — Hâşiye, Carlyle'ın tasdikinin Risale-i Nur'da beyan edildiğini söyler
- anma · müellif · Şuaat-ı Marifetü'n-Nebi › Beşinci Şuâ › 28. cümle (`suaat-i-marifetin-nebi/5/c028`) — Kur'ân'ı tasdik eden dahiler örneği olarak Goethe ve Carlyle anılır

**Bismarck** (Bismarck): 20

- nakil · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Âlem‑i İslâmdan Müjdeli Haberler ve Bismarck’ın Fıkrası › 4. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/207/c004`) — Denizli talebelerinin Bismarck'ın eserinden aldığı fıkrayı nakleder
- nakil · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Âlem‑i İslâmdan Müjdeli Haberler ve Bismarck’ın Fıkrası › 12. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/207/c012`) — Nakledilen fıkranın Bismarck imzası
- nakil · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Âlem‑i İslâmdan Müjdeli Haberler ve Bismarck’ın Fıkrası › 15. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/207/c015`) — Bismarck ve Carlyle'ın Kur'ân lehindeki sözlerini hayra alamet sayar
- nakil · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Aynen iade edilen bazı risalelerin eski hurufla teksirini bir suç sayıp ceza vermek, adliyeleri cidden alâkadar edip adalet şerefini kırıyor › 3. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/209/c003`) — Bismarck'ın Kur'ân'ı tasdik eden yazısının gazetelerde neşrini anlatır
- nakil · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 2 › 1952’de İstanbul’da görülen Gençlik Rehberi mahkemesine, ehl‑i vukufa cevaben verilen itiraznamedir › 113. cümle (`emirdag-lahikasi/emirdag-lahikasi-2/310/c113`) — Hutbe'deki Bismarck ve Carlyle'a dayanan hükmü mahkemeye tekrarlar
- nakil · talebe · Gençlik Rehberi › Siyah Dutun Bir Meyvesi › 7. cümle (`genclik-rehberi/siyah-dutun-bir-meyvesi/c007`) — Talebeler Bismarck'ın İslâmiyet hakkındaki sözlerini Üstad'a arz eder
- nakil · talebe · Gençlik Rehberi › Siyah Dutun Bir Meyvesi › 9. cümle (`genclik-rehberi/siyah-dutun-bir-meyvesi/c009`) — Talebeler Bismarck'ın İslâmiyet hakkındaki sözlerini Üstad'a arz eder
- nakil · talebe · Gençlik Rehberi › Siyah Dutun Bir Meyvesi › 25. cümle (`genclik-rehberi/siyah-dutun-bir-meyvesi/c025`) — Nakledilen beyanatın Bismarck imzası
- nakil · müellif · Hutbe-i Şamiye › Arabî Hutbe‑i Şâmiye Eserinin Tercümesi › Birinci Kelime: “El‑Emel” › Birinci Cihet Olan Ma'nen Terakkî › İkinci Misâl › 1. cümle (`hutbe-i-samiye/arabi-hutbe-i-samiye-eserinin-tercumesi/kelime-01/birinci-cihet-olan-manen-terakki/misal-02/c001`) — Bismarck'ın Kur'ân hakkındaki sözünü nakletmeye başlar
- nakil · müellif · Hutbe-i Şamiye › Arabî Hutbe‑i Şâmiye Eserinin Tercümesi › Birinci Kelime: “El‑Emel” › Birinci Cihet Olan Ma'nen Terakkî › İkinci Misâl › 10. cümle (`hutbe-i-samiye/arabi-hutbe-i-samiye-eserinin-tercumesi/kelime-01/birinci-cihet-olan-manen-terakki/misal-02/c010`) — Bismarck ve Carlyle'ın sözlerine dayanarak Avrupa'nın İslâm'a gebe olduğunu söyler
- nakil · müellif · Tarihçe-i Hayat › Altıncı Kısım Emirdağı Hayatı › Âlem‑i İslâmdan Müjdeli Haberler ve Bismarck’ın Fıkrası › 5. cümle (`tarihce-i-hayat/altinci-kisim-emirdagi-hayati/alem-i-islamdan-mujdeli-haberler-ve/c005`) — Denizli talebelerinin Bismarck'ın eserinden aldığı fıkrayı nakleder
- nakil · müellif · Tarihçe-i Hayat › Altıncı Kısım Emirdağı Hayatı › Âlem‑i İslâmdan Müjdeli Haberler ve Bismarck’ın Fıkrası › 13. cümle (`tarihce-i-hayat/altinci-kisim-emirdagi-hayati/alem-i-islamdan-mujdeli-haberler-ve/c013`) — Nakledilen fıkranın Bismarck imzası
- nakil · müellif · Tarihçe-i Hayat › Altıncı Kısım Emirdağı Hayatı › Âlem‑i İslâmdan Müjdeli Haberler ve Bismarck’ın Fıkrası › 16. cümle (`tarihce-i-hayat/altinci-kisim-emirdagi-hayati/alem-i-islamdan-mujdeli-haberler-ve/c016`) — Bismarck ve Carlyle'ın Kur'ân lehindeki sözlerini hayra alamet sayar
- nakil · müellif · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › Hutbe‑i Şâmiye › Birinci Kelime: “El‑Emel” › Birinci Cihet Olan Ma'nen Terakkî › 45. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/hutbe-i-samiye/kelime-01/birinci-cihet-olan-manen-terakki/c045`) — Bismarck ve Carlyle'ın sözlerine dayanarak Avrupa'nın İslâm'a gebe olduğunu söyler
- anma · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Âlem‑i İslâmdan Müjdeli Haberler ve Bismarck’ın Fıkrası › 16. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/207/c016`) — Bismarck'ın fıkrasını ekte gönderdiklerini söyler
- anma · talebe · Gençlik Rehberi › Siyah Dutun Bir Meyvesi › 5. cümle (`genclik-rehberi/siyah-dutun-bir-meyvesi/c005`) — Talebe mektubunun başlığı: Bismarck'ın beyanatı
- anma · müellif · Hutbe-i Şamiye › Hutbe‑i Şâmiye’nin Zeylinin Zeyli › Reddü'l‑Evhâm › Beşinci Vehim › 3. cümle › Hâşiye › 1. cümle (`hutbe-i-samiye/zeyl/reddul-evham/vehim-05/c003/h1/c001`) — Hâşiye metnin Bismarck ve Carlyle'ın beyanlarına işaret ettiğini söyler
- anma · müellif · İşaratü'l-İ'caz › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri (Nübüvvet Hakkında) › Altıncı Mes'ele › Dördüncü Nükte › 24. cümle › Hâşiye › 1. cümle (`isaratul-icaz/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-06/nukte-04/c024/h1/c001`) — Risale-i Nur'da Bismarck gibi filozofların tasdiklerinin beyan edildiğini söyler
- anma · müellif · Tarihçe-i Hayat › Altıncı Kısım Emirdağı Hayatı › Âlem‑i İslâmdan Müjdeli Haberler ve Bismarck’ın Fıkrası › 18. cümle (`tarihce-i-hayat/altinci-kisim-emirdagi-hayati/alem-i-islamdan-mujdeli-haberler-ve/c018`) — Bismarck'ın fıkrasını ekte gönderdiklerini söyler
- anma · talebe · Tarihçe-i Hayat › Birinci Kısım İlk Hayatı › Hutbe‑i Şâmiye › Birinci Kelime: “El‑Emel” › Birinci Cihet Olan Ma'nen Terakkî › 44. cümle (`tarihce-i-hayat/birinci-kisim-ilk-hayati/hutbe-i-samiye/kelime-01/birinci-cihet-olan-manen-terakki/c044`) — Derleyici, Bediüzzaman'ın Bismarck'ın sözlerini naklettiğini bildirir

**Târîh-i İslâmiyet** (Reinhart Dozy): 8

- değerlendirme · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 1 › Adliye Vekiliyle ve Risale‑i Nur’la alâkadar mahkemelerin hâkimleriyle bir hasbihâldir › İkinci Nümûne › 15. cümle (`emirdag-lahikasi/emirdag-lahikasi-1/7/numune-02/c015`) — Zındıkların eserleri arasında sayıp serbestliğini Risale'ye karşı kıyaslıyor.
- değerlendirme · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 2 › Üstadımız notalar hükmünde söyledi, biz de kaleme aldık › 16. cümle (`emirdag-lahikasi/emirdag-lahikasi-2/301/c016`) — İslâm aleyhinde diye niteleyip ellerde gezdiğini söylüyor; Üstad'ın söyledikleri, talebe kaleme almış.
- değerlendirme · müellif · Şualar › Onikinci Şuâ › Son Sözün Mühim Bir Parçası › 7. cümle (`sualar/12/son-sozun-muhim-bir-parcasi/c007`) — Eseri İslâm aleyhinde diye kınıyor, serbest okunmasını karşılaştırıyor.
- değerlendirme · müellif · Şualar › Ondördüncü Şuâ › Afyon Mahkemesinin Bizi İttiham Etmesine Karşı İ'tirâznâmenin Tetimmesidir › 4. cümle (`sualar/14/afyon-mahkemesinin-bizi-ittiham-etmesine/c004`) — Eserlerini muzır diye niteliyor; okuyanlar suçlu sayılmıyor diyor.
- değerlendirme · müellif · Şualar › Ondördüncü Şuâ › Hatâlar ve Cevabları › 152. cümle (`sualar/14/hatalar-ve-cevablari/c152`) — Kitabı ifsad için neşredilmiş diye niteliyor; aslî adı metinde yok.
- değerlendirme · belirsiz · Tarihçe-i Hayat › Altıncı Kısım Emirdağı Hayatı › Adliye Vekiliyle ve Risale‑i Nur’la Alâkadar Mahkemelerin Hâkimleriyle Bir Hasbihâl › İkinci nümûne › 12. cümle (`tarihce-i-hayat/altinci-kisim-emirdagi-hayati/adliye-vekiliyle-ve-risale-i-nurla/numune-02/c012`) — Zındık eserleri arasında sayılıp Risale'ye muameleyle kıyaslanıyor.
- değerlendirme · müellif · Tarihçe-i Hayat › Beşinci Kısım Denizli Hayatı › Bediüzzaman Said Nursî’nin Denizli Mahkemesi’nde Yaptığı Müdafaadan Bazı Kısımlar › İddianâmeye Karşı İ'tirâznâmenin Tetimmesidir › 4. cümle (`tarihce-i-hayat/besinci-kisim-denizli-hayati/bediuzzaman-said-nursinin-denizli-mahkemesinde/iddianameye-karsi-itiraznamenin-tetimmesidir/c004`) — Kur'ân aleyhinde muzır eser diye niteleniyor.
- değerlendirme · müellif · Tarihçe-i Hayat › Beşinci Kısım Denizli Hayatı › Bediüzzaman Said Nursî’nin Denizli Mahkemesi’nde Yaptığı Müdafaadan Bazı Kısımlar › Son Sözün Mühim Bir Parçası › 8. cümle (`tarihce-i-hayat/besinci-kisim-denizli-hayati/bediuzzaman-said-nursinin-denizli-mahkemesinde/son-sozun-muhim-bir-parcasi/c008`) — İslâmiyet aleyhinde serâpâ diye yargılanıyor.

**Molière, Victor Hugo, Goethe** (—): 3

- değerlendirme · talebe · Nur'un İlk Kapısı › Ankara Üniversitesinde Okunan Bir Konferanstır › 95. cümle (`nurun-ilk-kapisi/ankara-universitesinde-okunan-bir-konferanstir/c095`) — Konferansta eserleri Risale-i Nur'la kıyaslanıyor.
- değerlendirme · talebe · Nur'un İlk Kapısı › Ankara Üniversitesinde Okunan Bir Konferanstır › 95. cümle (`nurun-ilk-kapisi/ankara-universitesinde-okunan-bir-konferanstir/c095`) — Konferansta eserleri Risale-i Nur'la kıyaslanıyor.
- değerlendirme · talebe · Nur'un İlk Kapısı › Ankara Üniversitesinde Okunan Bir Konferanstır › 95. cümle (`nurun-ilk-kapisi/ankara-universitesinde-okunan-bir-konferanstir/c095`) — Konferansta eserleri Risale-i Nur'la kıyaslanıyor.

**Renaud'nun Kur'ân tercümesi** (Renaud): 2

- değerlendirme · başka · İşaratü'l-İ'caz › Ecnebî Feylesofların Kur'ânı Tasdiklerine Dair Şehâdetleri › Zamanlar Geçtikçe, Kur'ânın Ulvî Sırları İnkişaf Ediyor › 32. cümle (`isaratul-icaz/ecnebi-feylesoflarin-kurani-tasdiklerine-dair/zamanlar-gectikce-kuranin-ulvi-sirlari/c032`) — Ecnebi yazar Renaud'nun tercümesinin tashihini istiyor.
- değerlendirme · başka · Nur'un İlk Kapısı › Ecnebî Feylesofların Kur'ân’ı Tasdiklerine Dair Şehâdetleri › Zamanlar Geçtikçe, Kur'ân’ın Ulvî Sırları İnkişaf Ediyor › 32. cümle (`nurun-ilk-kapisi/ecnebi-feylesoflarin-kurani-tasdiklerine-dair/zamanlar-gectikce-kuranin-ulvi-sirlari/c032`) — Ecnebi yazar Renaud'nun tercümesinin tashihini istiyor.

**Roma İmparatorluğunun İnhitat ve Sukûtu** (Edward Gibbon): 2

- nakil · belirsiz · İşaratü'l-İ'caz › Ecnebî Feylesofların Kur'ânı Tasdiklerine Dair Şehâdetleri › Müslümanlık, Tecessüd ve Teslîs Akîdesini Reddeder › 1. cümle (`isaratul-icaz/ecnebi-feylesoflarin-kurani-tasdiklerine-dair/muslumanlik-tecessud-ve-teslis-akidesini/c001`) — Eserden alıntı yapılıyor.
- nakil · belirsiz · Nur'un İlk Kapısı › Ecnebî Feylesofların Kur'ân’ı Tasdiklerine Dair Şehâdetleri › Müslümanlık, Tecessüd ve Teslîs Akîdesini Reddeder › 1. cümle (`nurun-ilk-kapisi/ecnebi-feylesoflarin-kurani-tasdiklerine-dair/muslumanlik-tecessud-ve-teslis-akidesini/c001`) — Eserden alıntı yapılıyor.

### Basın ve yeni yayınlar

**Sebîlürreşâd (dergi)** (—): 16

- havale · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 2 › “Dinî hissiyatı siyasete alet ediyorum” diye ithamlarına karşı deriz › 38. cümle (`emirdag-lahikasi/emirdag-lahikasi-2/309/c038`) — Tesettür meselesinde Sebilürreşad 115. sayıdaki makalesine gönderir
- havale · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 2 › Mahkeme reisine yazılan bir mektuptur › 22. cümle (`emirdag-lahikasi/emirdag-lahikasi-2/316/c022`) — Dini siyasete alet ithamına Sebilürreşad 116. sayıdaki makalesini cevap gösterir
- havale · müellif · Tarihçe-i Hayat › Sekizinci Kısım Isparta Hayatı › İstanbul’daki Fa'âl Talebeleri, Gençlik Rehberi’ni Tab'ettirmişler (İstanbul Mahkemesi) › Üstad’ın Müdafaası › 36. cümle (`tarihce-i-hayat/sekizinci-kisim-isparta-hayati/istanbuldaki-faal-talebeleri-genclik-rehberini/ustadin-mudafaasi/c036`) — Dini siyasete alet ithamına Sebilürreşad 116. sayıdaki makalesini cevap gösterir
- değerlendirme · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 2 › Nur Risalelerinin ve Nurcuların siyasetle alâkaları yok › 7. cümle (`emirdag-lahikasi/emirdag-lahikasi-2/251/c007`) — Sebilürreşad'ı iman hizmeti için takdir eder, siyasette değil
- anma · başka · Âsâr-ı Bediiyye › Makaleler Kısmı › DOKUZUNCU VEHİM › 444. cümle (`asar-i-bediiyye/makaleler-kismi/vehim-09/c444`) — Nâşir notu, makalelerin önce Sebilürreşad'da neşredildiğini söyler
- anma · talebe · Emirdağ Lahikası › Emirdağ Lâhikası 2 › Hakikatin nâşiri olan Sebilürreşâd’a hâlen Halk Partisi nâmına yapılan yüz cihetle kanunsuz bir muâmele › 2. cümle (`emirdag-lahikasi/emirdag-lahikasi-2/238/c002`) — Sebilürreşad'a yapılan kanunsuz muameleyi arz eder
- anma · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 2 › Nur Risalelerinin ve Nurcuların siyasetle alâkaları yok › 3. cümle (`emirdag-lahikasi/emirdag-lahikasi-2/251/c003`) — Eşref Edib'i ve Sebilürreşad yazarlarını anar
- anma · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 2 › Gördüğünüz meziyetler benim değil, Risale‑i Nur’undur. O da Kur’ân-ı Hakîm’in bir hakikatinin bir tefsiridir › İkinci Mes'ele › 14. cümle (`emirdag-lahikasi/emirdag-lahikasi-2/314/mesele-02/c014`) — Sebilürreşad'ın neşrettiği ilanını anar
- anma · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 2 › Tarihçe‑i Hayat’ın Neşrolunmaması İçin Eski Partinin Bazı Memurları Sevketmesi › 4. cümle (`emirdag-lahikasi/emirdag-lahikasi-2/369/c004`) — Tarihçe-i Hayat'ın Sebilürreşad tarafından neşredildiğini söyler
- anma · talebe · İşaratü'l-İ'caz › Birkaç Defa Berâet Kazanan Risale‑i Nur’un Birkaç Vilâyette Haksız Müsâderesine Dair, Nur’un Yüksek Bir Talebesinin Mahkemesindeki Müdafaasından Bir Parçadır › 64. cümle (`isaratul-icaz/birkac-defa-beraet-kazanan-risale-i/c064`) — Müdafaada beraet kararını bildiren Sebilürreşad nüshasını mahkemeye sunduğunu söyler
- anma · başka · Makalat › Makale – 20 › KÜRDLER VE İSLÂMİYET › 39. cümle (`makalat/makale-20/kurdler-ve-islamiyet/c039`) — Nâşir notu, makalelerin önce Sebilürreşad'da neşredildiğini söyler
- anma · müellif · Şualar › Ondördüncü Şuâ › Sebilürreşâd’ın Lehimizdeki Yazıları Her Hâlde Aleyhimizdeki Kıskançları ve Gizli Düşman Zındıkları Şaşırtmış › 3. cümle (`sualar/14/sebilurresadin-lehimizdeki-yazilari-her-halde/c003`) — Sebilürreşad'ın lehteki yazılarının düşmanları şaşırttığını söyler
- anma · başka · Tarihçe-i Hayat › Risale‑i Nur ve Hariç Memleketler › M. Sabir İhsanoğlu’nun Mektûbları › M. Sabir İhsanoğlu’nun, Türkiye’de İslâmî inkişaf münâsebetiyle memnuniyetini izhâr eden bir mektûbu › 31. cümle (`tarihce-i-hayat/risale-i-nur-ve-haric-memleketler/m-sabir-ihsanoglunun-mektublari/m-sabir-ihsanoglunun-turkiyede-islami/c031`) — Mektup sahibi Sebilürreşad'a yazdığını söyler
- anma · başka · Tarihçe-i Hayat › Risale‑i Nur ve Hariç Memleketler › Risale‑i Nur’dan Gençlik Rehberi’nin İstanbul Mahkemesi’nde berâeti münâsebetiyle Bağdat’tan gelen tebrik telgrafı. › 1. cümle (`tarihce-i-hayat/risale-i-nur-ve-haric-memleketler/risale-i-nurdan-genclik-rehberinin-istanbul/c001`) — Tebrik telgrafının Sebilürreşad'a hitabı
- anma · talebe · Tarihçe-i Hayat › Sekizinci Kısım Isparta Hayatı › Tahliller › Demokrat Kardeşlere Tavsiye › 1. cümle (`tarihce-i-hayat/sekizinci-kisim-isparta-hayati/tahliller/demokrat-kardeslere-tavsiye/c001`) — Hasbihalin Sebilürreşad'da da neşredildiğini bildirir
- anma · müellif · Tarihçe-i Hayat › Sekizinci Kısım Isparta Hayatı › Tarihçe‑i Hayat’ın Neşrolunmaması İçin Eski Partinin Bazı Memurları Sevketmesi › 4. cümle (`tarihce-i-hayat/sekizinci-kisim-isparta-hayati/tarihce-i-hayatin-nesrolunmamasi-icin-eski/c004`) — Tarihçe-i Hayat'ın Sebilürreşad tarafından neşredildiğini söyler

**es-Sıddîk (Pakistan, dergi)** (—): 6

- nakil · talebe · Emirdağ Lahikası › Emirdağ Lâhikası 2 › Gayet ehemmiyetli bir hâdise, bir istida ve bir şekvadır › 2. cümle (`emirdag-lahikasi/emirdag-lahikasi-2/327/c002`) — Derginin yarısının Risale makaleleri olduğunu içeriğinden aktarıyor.
- anma · talebe · Emirdağ Lahikası › Emirdağ Lâhikası 2 › Gayet ehemmiyetli bir hâdise, bir istida ve bir şekvadır › 1. cümle (`emirdag-lahikasi/emirdag-lahikasi-2/327/c001`) — Pakistan'da çıkan derginin ele geçtiği haber veriliyor.
- anma · talebe · Emirdağ Lahikası › Emirdağ Lâhikası 2 › Gayet ehemmiyetli bir hâdise, bir istida ve bir şekvadır › 4. cümle (`emirdag-lahikasi/emirdag-lahikasi-2/327/c004`) — Dergideki tercümenin Türkçe aslını takdim edeceklerini söylüyor.
- anma · talebe · Emirdağ Lahikası › Emirdağ Lâhikası 2 › Gayet ehemmiyetli bir hâdise, bir istida ve bir şekvadır › 17. cümle (`emirdag-lahikasi/emirdag-lahikasi-2/327/c017`) — Dergide yayımlanan risalenin yurtta da serbest bırakılmasını istiyor.
- anma · talebe · Tarihçe-i Hayat › Risale‑i Nur ve Hariç Memleketler › 30 Nisan 1958 Tarihli Students' Voice Gazetesi: “İslâm Dünyasındaki Müsbet Uyanıklık” › 7. cümle (`tarihce-i-hayat/risale-i-nur-ve-haric-memleketler/30-nisan-1958-tarihli-students/c007`) — İktisad Risalesi tercümesinin çıktığı mecmua; resim altı.
- anma · talebe · Tarihçe-i Hayat › Risale‑i Nur ve Hariç Memleketler › 30 Nisan 1958 Tarihli Students' Voice Gazetesi: “İslâm Dünyasındaki Müsbet Uyanıklık” › 8. cümle (`tarihce-i-hayat/risale-i-nur-ve-haric-memleketler/30-nisan-1958-tarihli-students/c008`) — Hutuvât-ı Sitte tercümesinin çıktığı mecmua; resim altı.

**el-Esâs fi's-Sünne** (Saîd Havvâ): 2

- nakil · başka · Âsâr-ı Bediiyye › Makaleler Kısmı › DOKUZUNCU VEHİM › 428. cümle › Hâşiye › 1. cümle (`asar-i-bediiyye/makaleler-kismi/vehim-09/c428/h1/c001`) — Nâşir notu Kürtlerin nesebi için kitaba dayanıyor.
- nakil · başka · Makalat › Makale – 20 › KÜRDLER VE İSLÂMİYET › 23. cümle › Hâşiye › 1. cümle (`makalat/makale-20/kurdler-ve-islamiyet/c023/h1/c001`) — Nâşir notu, Kürdlerin nesebi için kitaba dayanıyor.

**Students' Voice; "İslâmın Büyük Rönesansı"** (Zafer Afaq Ansar): 2

- nakil · talebe · Tarihçe-i Hayat › Risale‑i Nur ve Hariç Memleketler › İslâm Kongresi Reisi “Zafer Afaq Ansar”ın “İslâm’ın Büyük Rönesansı” Adlı Makalesinden › 1. cümle (`tarihce-i-hayat/risale-i-nur-ve-haric-memleketler/islam-kongresi-reisi-zafer-afaq/c001`) — Mecmuadaki makaleden aktarma yapılıyor.
- nakil · talebe · Tarihçe-i Hayat › Risale‑i Nur ve Hariç Memleketler › İslâm Kongresi Reisi “Zafer Afaq Ansar”ın “İslâm’ın Büyük Rönesansı” Adlı Makalesinden › 1. cümle (`tarihce-i-hayat/risale-i-nur-ve-haric-memleketler/islam-kongresi-reisi-zafer-afaq/c001`) — Makalenin Bediüzzaman hakkındaki sözleri aktarılıyor.

**Radyo istasyonları cetveli** (—): 1

- nakil · müellif · Emirdağ Lahikası › Emirdağ Lâhikası 2 › Hüve Nüktesi'nin çok noktalarından yalnız üç noktasını sizlere beyan ediyorum › İkinci Nokta › 4. cümle (`emirdag-lahikasi/emirdag-lahikasi-2/285/nokta-02/c004`) — Basılı istasyon listesindeki iki yüz merkez delil olarak kullanılıyor.

**Safahât** (Mehmed Âkif): 1

- anma · başka · Tarihçe-i Hayat › Risale‑i Nur ve Hariç Memleketler › 30 Nisan 1958 Tarihli Students' Voice Gazetesi: “İslâm Dünyasındaki Müsbet Uyanıklık” › 3. cümle (`tarihce-i-hayat/risale-i-nur-ve-haric-memleketler/30-nisan-1958-tarihli-students/c003`) — Students' Voice makalesinde Âkif'in eseri anılıyor.

**Bediüzzaman'ın Tarihçe-i Hayatı** (Müküslü Hamza): 1

- anma · başka · Âsâr-ı Bediiyye › Bediüzzaman'ın Tarihçe-i Hayatı › 1. cümle (`asar-i-bediiyye/bediuzzamanin-tarihce-i-hayati/c001`) — Bölüm başlığı, başkasının yazdığı tarihçeyi künyeliyor.
