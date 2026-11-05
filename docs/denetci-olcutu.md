# Denetçi ölçütü (Y0.1; kullanıcı onayladı, 2026-11-05)

Yol haritasının ilk adımı (`docs/tefsir-pilot-degerlendirme.md`, Y0.1). Taslak modelin, kararlar kullanıcınındır
(2026-11-05; 1. turun soruları ve cevapları sonda). Y1.2 (denetçinin ihtisası, `reviewers.json`'a `fields`) ve Y0.2
(davet) bu belgeye dayanır.

Bugünkü durum: tek denetçi kullanıcı (`fatihebrarinan`, "proje sahibi", 2026-10-27'den); 94 karar (62 Kur'ân – Risale
ilişkisi, 32 Beyzâvî'nin Kur'ân alıntısı). Kayıt düzeni H5'tir (`link_reviews.py`): yalnız eklenen satırlar,
`reviewed` / `disputed` (gerekçeli) / `withdrawn`, denetçinin güç hükmü, denetçiler birbirini silmez, model denetçi
değildir. Bu belge o düzenin **kim** ve **hangi alanda** sorusunu cevaplar.

## 1. İlkeler

1. **Kapı ilim ve ihtisasa göre açılır, meşrebe göre değil.** Denetçiye cemaati, mensubiyeti, görüşü sorulmaz ve
   kayda girmez. Sorulan tek şey: bu alanda bu işi yapabiliyor mu.
2. **Ehliyet alan başınadır.** Hadisçi olmak Kur'ân – Risale ilişkisinde, Risale'yi iyi bilmek hadiste söz hakkı
   vermez. Bir kişinin birden çok alanı olabilir.
3. **Ehliyet gösterilir, beyan yetmez.** Diploma ya da icazet bir işarettir, ama asıl ölçü işin kendisidir: her alanda
   cevabı bilinen küçük bir deneme örneklemi (bkz. 3). Böylece belge doğrulamak gerekmez ve resmî eğitimi olmayan
   ehil kişi de girebilir.
4. **Denetçi hüküm vermez, bağı denetler.** Kararın konusu bağdır (bu iki yer arasında bu ilişki var mı, kanıtı
   doğru mu, ne kadar güçlü). Hadise sıhhat hükmü, bir yere "tefsir" hükmü denetçinin işi değildir; kayıt bunları
   almaz.
5. **Her karar adla ve gerekçeyle kalır.** Kararlar silinmez; itiraz ve geri çekme yeni satırdır (H5). Tefsir –
   tefsir ve Risale – tefsir bağlarında gerekçe her kararda zorunludur (bkz. 4).
6. **Denetçi insandır.** Model öneri hazırlar, örneklemi sunar, karar vermez; modelin hazırladığı satır denetçinin
   kararı sayılmaz. Komutu ya da düğmeyi bir insan çalıştırır.

## 2. Alanlar

Dört bağ alanı ve ayrı tutulan bir metin kontrolü (kullanıcının kararı: Arapça dil ayrı alan değildir; Arapça okumak
`kuran`, `hadis` ve `tefsir` alanlarının ehliyetinin içindedir):

| Alan (`fields`) | İşi | Asgari ehliyet |
|---|---|---|
| `kuran` | Bir metindeki Arapçanın Kur'ân'dan alıntı olup olmadığı, hangi âyet ve hangi lafız; işaretsiz alıntı, iktibas, kalıp ifade ayrımı; müfessirin cümleyi âyetin sözüyle açması (lemma) ve lafzın sınırı | Mushafı akıcı okumak, Arapça cümlenin sınırını görmek; hâfızlık ya da kıraat bilgisi artı |
| `hadis` | Bir sözün rivayet olup olmadığı, künyenin gösterdiği yerde bulunması, lafız farkı, mânen nakil; tefsirlerdeki «» sözleri | Arapça okumak; hadis usûlü ve kaynakları; kitapta bâb ve numara bulabilmek. Derece hükmü istenmez (ilke 4) |
| `tefsir` | Müfessirlerin eserleri arasında ilişki: aynı sözle nakil, aynı görüş, farklı görüş, itiraz; müfessirin âyet birimi | Klasik Arapça metni harekesiz okuyup anlamak; tefsir usûlü; en az bir klasik tefsiri (Beyzâvî, Keşşâf…) Arapçasından okumuş olmak |
| `risale` | Risale'nin bir yerinin âyetle kurduğu bağın türü ve gücü (işaret, açılış, izah, dayanak); Risale içi göndermeler; Risale ile müfessir arasındaki ilişkide Risale tarafı | Külliyatı bütün olarak okumuş, bölümlerin yerini ve göndermelerini bilen |
| `metin` (ayrı) | Risale metninin cümle bölmesi, başlıkları, mecmua eşlemesi (Aşama 16) | Risale'yi okuyabilmek; Arapça gerekmez (aslı Arapça eserlerin metin kontrolünde gerekir) |

`metin` bir bağ denetimi değildir: kararları kontrol arayüzünün işaretleri gibi ayrıştırıcıya döner, denetim kaydına
girmez. Yine de aynı listede adla durur; tanıtımdaki "Arapça bilmeyenlerin de yapabileceği iş" budur.

### Bağ → gereken alan

Y1.2.2'nin eşlemesi. Bir kararın "denetlendi" sayılması için denetçi gereken alanda kayıtlı olmalı; öbürlerinin
kararı kaydedilir, araçta görünür, ama `competent: false` taşır. İki alan gereken bağda (aşağıda "ve") bağ ya iki
alanı birden taşıyan bir denetçinin kararıyla ya da her alandan birer denetçinin ayrı kararlarıyla "denetlendi" olur;
tek alanlı denetçinin kararı o alanın payıdır.

Bağlar üç cinstir (sade şema, `docs/tefsir-pilot-degerlendirme.md` "Bağ şeması"): **lafız** (söz geçiyor), **ilişki**
(iki yer arasında anlamca bağ var), **gönderme** (metin oraya gönderiyor). Gereken alan bağın cinsinden ve iki
ucundan okunur; yeni bir eser ya da alan eklenince kural kendiliğinden işler:

- **Lafız bağı:** hedefin alanı. Hedef Kur'ân ise `kuran`, hadis ise `hadis`, bir müfessirin metni ise `tefsir`.
- **İlişki bağı:** iki ucun alanı. Kur'ân ile Risale arasında `kuran` ve `risale`, Kur'ân ile müfessir arasında
  `tefsir`, iki müfessir arasında `tefsir`, Risale ile müfessir arasında `tefsir` ve `risale`.
- **Gönderme bağı:** gönderen metnin alanı (Risale'de `risale`); hedef bir müfessirse `tefsir` de.

Bugün elimizdeki ve ileride gelecek bağlar, bu kurala göre:

| Bağ | Cinsi | Ne bağlar | Bugün | Alan |
|---|---|---|---|---|
| Kur'ân – Risale | lafız | Risale'deki âyet alıntısı (kaynağın işaretlediği ya da Kur'ân metninde bulunan) | 10.283 | `kuran` |
| Kur'ân – Risale | ilişki | Risale'nin bir yerinin âyetle kurduğu bağ (işaret, açılış, izah, dayanak, Risale'ye işaret) | 961 | `kuran` ve `risale` |
| Kur'ân – tefsir | lafız | Müfessirin cümlesindeki âyet alıntısı ve lemma (cümleyi âyetin sözüyle açması) | 330 (yerelde) | `kuran` |
| Kur'ân – tefsir | ilişki | Müfessirin âyet birimi ve işlediği âyetler (eserin kendi yapısı söyler) | 39 (yerelde) | `tefsir` |
| Hadis – Risale | lafız | Risale'deki sözün rivayette bulunması: derlemde kelimesi kelimesine, künyenin bölümünde, okumayla (mânen nakil de buradadır) | 3.380; ayrıca 1.446 model adayı | `hadis` |
| Hadis – tefsir | lafız | Müfessirin naklettiği sözün rivayette bulunması | 10 (yerelde) | `hadis` |
| Hadis – Risale, Hadis – tefsir | ilişki | Bir yerin hadisi aktarmadan onun konusunu işlemesi | yok (ileride) | `hadis` ve uçtaki metnin alanı |
| Risale – Risale | gönderme | Eski adlar; ileride numaralı göndermeler (Aşama 13) | 15 | `risale` |
| Risale – tefsir | gönderme | Risale'nin müfessiri adıyla anması ("Zemahşerî'nin dediğine göre") | yok (Y1.7) | `risale` ve `tefsir` |
| Tefsir – tefsir | lafız | Bir müfessirin öbüründen aynı sözle naklettiği yer (Beyzâvî → Keşşâf) | yok (Y1.7) | `tefsir`; **gerekçe zorunlu** |
| Tefsir – tefsir | ilişki | Aynı görüş, farklı görüş, itiraz | yok (katkı aşaması) | `tefsir`; **gerekçe zorunlu** |
| Risale – tefsir | ilişki | Aynı görüş, farklı görüş, itiraz | yok (katkı aşaması) | `tefsir` ve `risale`; **gerekçe zorunlu** |
| Hadis – hadis | ilişki | Aynı hadisin başka rivayeti | yok (hadis sunucusu) | `hadis` |
| Konu – Risale ve öbürleri | ilişki | Bir bölümün bir konuyu işlemesi (konu ortak adrestir, iki yer arasında konu bağı kurulmaz) | yok (Aşama 15) | uçtaki metnin alanı |

Model adayları (bugün Hadis – Risale'deki 1.446 okuma) bağ değildir; Y1.3'te "aday" durumuyla aynı bağ kaydına
girerler ve denetçi kabul edince bağ olurlar.

## 3. Davet ve kayıt usulü

1. **Yalnız davetle** (kullanıcının kararı). Aday kullanıcının tanıdığı ya da tavsiye edilen kişidir; katkı
   sayfasından (`destek@risalemcp.com`) yazan biri de kullanıcı onu davet ederse aday olur. Sayfadan yazmak tek
   başına adaylık vermez.
2. **Tanışma:** tanıtım metni (`docs/tefsir-tanitim.md`) kişiye özel gider; aday hangi alanda katkı vereceğini ve
   kendi ehliyetini kısaca yazar (eğitim, okuduğu eserler; serbest metin, kayda girmez).
3. **Deneme örneklemi:** her alan için cevabı bilinen 10 satır (kullanıcının kararlarından ve kurulumun bilinen
   hatalarından; en az 2'si yanlış bağ, 1'i tuzak: kelimesi benzeyen ama sözü farklı). Ölçü: en çok 1 hata ve
   yanlışların hepsinin yakalanması. Gerekçe zorunlu alanlarda (tefsir) denemenin gerekçeleri de okunur. Tutmayan aday
   reddedilmez, o alanda kaydedilmez; gerekçe kendisine söylenir. Deneme kararları ayrı dosyada durur
   (`origin: {"trial": …}`), araçlara gitmez. Deneme her davetli için ve her alan için ayrıdır; kullanıcının mevcut
   alanları denemesizdir (94 kararı o alanlarda verildi).
4. **Kabul:** kullanıcı onaylar; denetçi `reviewers.json`'a alanlarıyla yazılır (`fields`, `since`, alan başına
   deneme tarihi). Kayıttan önce şartları kabul eder: kararların adıyla kaydedileceği, silinmeyeceği, lisansı (Y0.5).
5. **İlk tur:** kendi alanından 40'lık örneklem (T7 gibi); sonuçları kullanıcıyla birlikte gözden geçirilir.

Kayıt alanları (Y1.2.1; iletişim bilgisi bu dosyaya girmez):

```json
"ornek-kimlik": {
  "name": "Görünen ad",
  "fields": {"kuran": {"since": "2026-11-20", "trial": "2026-11-18"}, "risale": {"since": "2026-11-20", "trial": "2026-11-19"}},
  "note": "isteğe bağlı kısa tanım (ör. 'ilahiyat, tefsir ABD')",
  "since": "2026-11-20"
}
```

Kullanıcının kaydı: `kuran`, `risale`, `metin` (kullanıcının kararı). Proje sahibi olmak alan vermez.

## 4. Kararların geçerliliği, gerekçe, itiraz, geri çekme

- **Gerekçe:** itirazda her zaman zorunludur. **Tefsir – tefsir ve Risale – tefsir bağlarında** (iki ucu da metin olan
  lafız ve ilişki bağları) kabulde de zorunludur: bu bağlarda kararın değeri neden verildiğindedir (kullanıcının
  kararı, 2026-11-05). Gerekçe kanıtı göstermelidir: hangi söz, hangi görüş, hangi farkla ("Beyzâvî 'الحمد' üzerine
  Keşşâf'ın sözünü kısaltarak aktarıyor; Keşşâf'taki ikinci vecih düşmüş"). Kayıtta `reason` alanıdır; gerekçesiz
  satır kurulumu durdurur (`link_reviews.needs_reason`). Denetim arayüzünde (Y1.4) ve katkı kapısında (Y3) bu bağların
  not kutusu zorunludur. Kur'ân ve hadis hedefli bağlarda kanıt veridedir (bulunan söz), göndermede metnin kendi
  sözüdür; orada gerekçe isteğe bağlıdır.
- **Alanı tutmayan karar** kaydedilir, silinmez, `competent: false` ile görünür; bağı "denetlendi" yapmaz.
- **İki ehil denetçi ayrılırsa** (biri `reviewed`, öbürü `disputed`): bağ "ihtilaflı" görünür, iki karar gerekçesiyle
  yan yana; oylama yapılmaz, sayı üstünlük vermez (kullanıcının kararı). Araç ve talimat ihtilafı hüküm gibi değil
  ihtilaf olarak sunar. Üçüncü bir ehil denetçinin görüşü eklenebilir, ama o da yalnız bir karardır.
- **Güçte ayrılık** (biri `strong`, öbürü `weak`): ikisi de görünür; araç en temkinli olanı öne alır (`weak`).
- **Geri çekme** yalnız denetçinin kendi kararınadır.
- **Kurallar değişince** kararın verildiği hâl `seen`'de durur; bağ değişmişse karar "eski hâle verildi" diye
  işaretlenir, yeniden bakılması için kuyruğa düşer (işaretleme Y1.4'te).
- **Denetçinin ayrılması:** kayıt `until` tarihi alır; geçmiş kararları durur. İsterse görünen adı "ayrılan denetçi"ye
  çevrilir, kimliği kayıtta kalır (kullanıcının kararı).
- **Kötüye kullanım** (bilerek yanlış karar, toplu itiraz, meşrep kavgası): kullanıcı kaydı `until` ile kapatır,
  kararları `competent: false` sayılır; gerekçe kayıtta.
- **Çıkar çatışması:** öneriyi verenle denetleyen ayrı kişidir (katkı açıldığında, Y3).

## 5. Görünen ad ve gizlilik

- **İsimli denetim:** görünen ad gerçek addır, kişinin seçtiği biçimde (unvanlı ya da unvansız); kısaltma olabilir
  ("M. Yılmaz"), takma ad olmaz (kullanıcının kararı).
- **Depo:** proje deposu açık kalır, ama denetçilerin adları ve kararları açık depoda durmaz (kullanıcının kararı,
  2026-11-05). `data/links/reviews/` ana depodan çıkarıldı (`.gitignore`) ve kendi ayrı, yerel git deposundadır
  (`data/links/reviews/.git`): kararlar yeniden üretilemez, geçmişi orada tutulur; yedeği (özel bir uzak depo ya da
  başka bir yer) kullanıcıdadır. Ayrılmadan önceki 94 karar ve kullanıcının adı ana deponun geçmişinde durur; bunlar
  kullanıcının kendi kararlarıdır.
- **Saklanan ama yayımlanmayan:** e-posta, telefon, eğitim beyanı, deneme sonuçlarının ayrıntısı; denetim deposuna
  da girmez, kullanıcının kendi kaydında durur.
- **Araç çıktısı: ad yok, sabit numara var** (kullanıcının kararı, 2026-11-05). Her denetçinin bir kez verilen,
  başkasına geçmeyen bir numarası vardır (`reviewers.json`'da `number`; kullanıcı 1). Araçlar kararı numarayla,
  durumu, gücü, tarihi ve gerekçesiyle verir (Y1.2'den sonra alanıyla da); okuyan kişiyi değil gerekçeyi tartar,
  aynı denetçinin kararlarının tutarlılığını numaradan görür. Ad ve denetçi kimliği veritabanına da girmez (genel
  sunucuya giden dosyada yoktur). Bu bir takma ad değildir: kişi seçmez, sistem verir.
- **Ad kime görünür:** veride her zaman durur (denetim deposu). Kişi kendi kayıtlarını ve önerilerinin durumunu
  girişli katkı bağdaştırıcısında görür (Y3); denetçiler birbirinin adını orada görebilir (karar Y3'te); tefsiri
  yazacak heyet ve araştırmacılar istek üzerine görür. Katılım şartları denetçinin buna onayını alır (Y0.5).
- **Lisansla uyum (Y0.5'e not):** katkılar CC BY-SA gibi atıf isteyen bir lisansla verilirse atıf açıkta adı
  ister. Ya katkı veren toplu atfı ("Risale-i Nur MCP denetçileri") ya da adının anılmamasını kabul eder (CC
  lisansları lisans verenin atfın biçimini belirlemesine izin verir), ya da katkılar atıf istemeyen bir lisansla
  (CC0) verilir. Davetten ve katılım şartlarından önce karara bağlanır.
- **Gizlilik politikası:** denetçi kaydı sunucuda değil yerelde tutulduğu sürece değişmesi gerekmez; katkı sunucudan
  yapılınca (Y3) Y0.5 ile birlikte değişir.

## 6. Bu belgenin bağladıkları

- Y1.2: `reviewers.json` şeması (`fields`, `since`, `until`, `note`), bağ → alan kuralı (2), `competent`, iki alanlı
  bağın payları.
- Y0.2: davet metni ve deneme örneklemleri (3).
- Y0.5: kayıtta kabul edilen şartlar, lisans.
- Y1.4: arayüz denetçinin alanını bilir, alanı dışındaki bağı ona göstermez ya da işaretli gösterir; tefsir – tefsir
  ve Risale – tefsir bağlarında not kutusu zorunlu.

## Kararlar (kullanıcı, 2026-11-05)

1. Alanlar: `kuran`, `hadis`, `tefsir`, `risale` ve ayrı `metin`; Arapça dil ayrı alan değil.
2. Kur'ân – Risale ilişkisi: `kuran` ve `risale` birlikte.
3. Risale – tefsir ilişkisi: `tefsir` ve `risale`.
4. Yalnız davetle; sayfadan yazan biri davet edilirse sayılır.
5. Deneme örneklemi (10 satır, en çok 1 hata, yanlışların hepsi yakalanmalı) uygun.
6. Kullanıcının alanları: `kuran`, `risale`, `metin`.
7. İhtilafta oylama yok, iki karar yan yana.
8. Ayrılan denetçinin adı istenirse gizlenebilir.
9. Takma ad olmaz, kısaltma olabilir.
10. Depo açık kalır; denetçilerin adları ve kararları açık depoda durmaz.
11. Tefsir – tefsir ve Risale – tefsir bağlarında gerekçe (not) her kararda zorunlu.

12. Araçlar denetçinin adını vermez, sabit numarasını verir; ad katkı bağdaştırıcısında rol bazında ve istek
    üzerine heyete açıktır; lisans Y0.5'te buna uyumlu seçilir.
