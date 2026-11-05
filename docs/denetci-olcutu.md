# Denetçi ölçütü (Y0.1; taslak, 1. tur, 2026-11-05)

Yol haritasının ilk adımı (`docs/tefsir-pilot-degerlendirme.md`, Y0.1). Taslak modelindir, kararlar kullanıcınındır;
kullanıcının kararı gereken her yer **[Karar n]** diye işaretli ve sonda toplu. Onaylanınca Y1.2 (denetçinin ihtisası,
`reviewers.json`'a `fields`) ve Y0.2 (davet) bu belgeye dayanır.

Bugünkü durum: tek denetçi kullanıcı (`fatihebrarinan`, "proje sahibi", 2026-10-27'den); 94 karar (62 âyet ilişkisi,
32 Beyzâvî'nin Kur'ân alıntısı). Kayıt düzeni H5'tir (`link_reviews.py`): yalnız eklenen satırlar, `reviewed` /
`disputed` (gerekçeli) / `withdrawn`, denetçinin güç hükmü, denetçiler birbirini silmez, model denetçi değildir.
Bu belge o düzenin **kim** ve **hangi alanda** sorusunu cevaplar; kayıt düzenini değiştirmez.

## 1. İlkeler

1. **Kapı ilim ve ihtisasa göre açılır, meşrebe göre değil.** Denetçiye cemaati, mensubiyeti, görüşü sorulmaz ve
   kayda girmez. Sorulan tek şey: bu alanda bu işi yapabiliyor mu.
2. **Ehliyet alan başınadır.** Hadisçi olmak âyet ilişkisinde, Risale'yi iyi bilmek hadiste söz hakkı vermez. Bir
   kişinin birden çok alanı olabilir.
3. **Ehliyet gösterilir, beyan yetmez.** Diploma ya da icazet bir işarettir, ama asıl ölçü işin kendisidir: her alanda
   cevabı bilinen küçük bir deneme örneklemi (bkz. 4). Böylece belge doğrulamak gerekmez ve resmî eğitimi olmayan
   ehil kişi de girebilir.
4. **Denetçi hüküm vermez, bağı denetler.** Kararın konusu bağdır (bu iki yer arasında bu ilişki var mı, kanıtı
   doğru mu, ne kadar güçlü). Hadise sıhhat hükmü, bir yere "tefsir" hükmü denetçinin işi değildir; kayıt bunları
   almaz.
5. **Her karar adla ve gerekçeyle kalır.** Kararlar silinmez; itiraz ve geri çekme yeni satırdır (H5).
6. **Denetçi insandır.** Model öneri hazırlar, örneklemi sunar, karar vermez; modelin hazırladığı satır denetçinin
   kararı sayılmaz. Komutu ya da düğmeyi bir insan çalıştırır.

## 2. Alanlar

Plan beş alan sayıyordu (Kur'ân alıntısı, Arapça dil, hadis, tefsir, Risale), katkı sayfası dört nitelik
(`site/katki.html`). Öneri, bağ türleriyle birebir eşlenen beş alan ve ayrı tutulan bir metin kontrolü:

| Alan (`fields`) | İşi | Asgari ehliyet (öneri) |
|---|---|---|
| `kuran` | Bir metindeki Arapçanın Kur'ân'dan alıntı olup olmadığı, hangi âyet ve hangi lafız; işaretsiz alıntı, iktibas, kalıp ifade ayrımı | Mushafı akıcı okumak, Arapça cümlenin sınırını görmek; hâfızlık ya da kıraat bilgisi artı |
| `arapca` | Arapça metinde lafzın sınırı (lemma), iki Arapça metnin aynı söz olup olmadığı (`same_words`), Arapça eserlerin cümle bölmesi, tercümenin asla uyması | Klasik Arapça metni harekesiz okuyup anlamak (nahiv, sarf); ilahiyat ya da medrese eğitimi işaret |
| `hadis` | Bir sözün rivayet olup olmadığı, künyenin gösterdiği yerde bulunması, lafız farkı, mânen nakil; tefsirlerdeki «» sözleri | Hadis usûlü ve kaynakları; kitapta bâb ve numara bulabilmek. Derece hükmü istenmez (ilke 4) |
| `tefsir` | Müfessirlerin eserleri arasında ilişki: nakil (`transmits`), aynı görüş, farklı görüş, itiraz; müfessirin âyet birimi | Tefsir usûlü; en az bir klasik tefsiri (Beyzâvî, Keşşâf…) Arapçasından okumuş olmak |
| `risale` | Risale'nin bir yerinin âyetle kurduğu bağın türü ve gücü (işaret, açılış, izah, dayanak); Risale içi göndermeler; Risale ile müfessir arasındaki ilişkide Risale tarafı | Külliyatı bütün olarak okumuş, bölümlerin yerini ve göndermelerini bilen; Arapça yalnız `kuran` ile birlikte gerekir |
| `metin` (ayrı) | Risale metninin cümle bölmesi, başlıkları, mecmua eşlemesi (Aşama 16) | Risale'yi okuyabilmek; Arapça gerekmez |

`metin` bir bağ denetimi değildir: kararları kontrol arayüzünün işaretleri gibi ayrıştırıcıya döner, `link_reviews`'a
girmez. Yine de aynı listede adla durması, tanıtımdaki "Arapça bilmeyenlerin de yapabileceği iş"in karşılığıdır.
**[Karar 1]**

### Bağ → gereken alan

Y1.2.2'nin eşlemesi. Bir kararın "denetlendi" sayılması için denetçi gereken alanda kayıtlı olmalı; öbürlerinin
kararı kaydedilir, araçta görünür, ama `competent: false` taşır.

Bağlar üç cinstir (sade şema, 2026-11-05, `docs/tefsir-pilot-degerlendirme.md` "Bağ şeması"): **lafız** (söz geçiyor),
**ilişki** (iki yer arasında anlamca bağ var), **gönderme** (metin oraya gönderiyor). Gereken alan dosyanın adından
değil, bağın cinsinden ve iki ucundan okunur; yeni bir eser ya da alan eklenince kural kendiliğinden işler:

- **Lafız bağı:** hedefin alanı. Hedef Kur'ân ise `kuran`, hadis ise `hadis`, bir Arapça metin ise `arapca`.
- **İlişki bağı:** iki ucun alanı. Kur'ân ile Risale arasında `risale`, Kur'ân ile müfessir arasında `tefsir`, iki
  müfessir arasında `tefsir`, Risale ile müfessir arasında `tefsir` ve `risale`.
- **Gönderme bağı:** gönderen metnin alanı (Risale'de `risale`).

Bugün elimizdeki ve ileride gelecek bağlar, bu kurala göre:

| Bağ | Cinsi | Ne bağlar | Bugün | Alan |
|---|---|---|---|---|
| Kur'ân – Risale | lafız | Risale'deki âyet alıntısı (kaynağın işaretlediği ya da Kur'ân metninde bulunan) | 10.283 | `kuran` |
| Kur'ân – Risale | ilişki | Risale'nin bir yerinin âyetle kurduğu bağ (işaret, açılış, izah, dayanak, Risale'ye işaret) | 961 | `risale` **[Karar 2]** |
| Kur'ân – tefsir | lafız | Müfessirin cümlesindeki âyet alıntısı ve lemma (cümleyi âyetin sözüyle açması) | 330 (yerelde) | `kuran` |
| Kur'ân – tefsir | ilişki | Müfessirin âyet birimi ve işlediği âyetler (eserin kendi yapısı söyler) | 39 (yerelde) | `tefsir` |
| Hadis – Risale | lafız | Risale'deki sözün rivayette bulunması: derlemde kelimesi kelimesine, künyenin bölümünde, okumayla (mânen nakil de buradadır) | 3.380; ayrıca 1.446 model adayı | `hadis` |
| Hadis – tefsir | lafız | Müfessirin naklettiği sözün rivayette bulunması | 10 (yerelde) | `hadis` |
| Hadis – Risale, Hadis – tefsir | ilişki | Bir yerin hadisi aktarmadan onun konusunu işlemesi | yok (ileride) | `hadis` ve uçtaki metnin alanı |
| Risale – Risale | gönderme | Eski adlar; ileride numaralı göndermeler (Aşama 13) | 15 | `risale` |
| Risale – tefsir | gönderme | Risale'nin müfessiri adıyla anması ("Zemahşerî'nin dediğine göre") | yok (Y1.7) | `risale` ve `tefsir` |
| Tefsir – tefsir | lafız | Bir müfessirin öbüründen aynı sözle naklettiği yer (Beyzâvî → Keşşâf) | yok (Y1.7) | `arapca` ya da `tefsir` |
| Tefsir – tefsir | ilişki | Aynı görüş, farklı görüş, itiraz | yok (katkı aşaması) | `tefsir` |
| Risale – tefsir | ilişki | Aynı görüş, farklı görüş, itiraz | yok (katkı aşaması) | `tefsir` ve `risale` (iki ayrı karar ya da iki alanlı bir denetçi) **[Karar 3]** |
| Hadis – hadis | ilişki | Aynı hadisin başka rivayeti | yok (hadis sunucusu) | `hadis` |
| Konu – Risale ve öbürleri | ilişki | Bir bölümün bir konuyu işlemesi (konu ortak adrestir, iki yer arasında konu bağı kurulmaz) | yok (Aşama 15) | uçtaki metnin alanı |

Model adayları (bugün Hadis – Risale'deki 1.446 okuma) bağ değildir; Y1.3'te "aday" durumuyla aynı bağ kaydına
girerler ve denetçi kabul edince bağ olurlar.

## 3. Davet ve kayıt usulü

1. **Aday:** kullanıcının tanıdığı ya da tavsiye edilen kişi, ya da katkı sayfasından (`destek@risalemcp.com`) yazan.
   İlk aşamada yalnız davetle **[Karar 4]**.
2. **Tanışma:** tanıtım metni (`docs/tefsir-tanitim.md`) kişiye özel gider; aday hangi alanda katkı vereceğini ve
   kendi ehliyetini kısaca yazar (eğitim, okuduğu eserler; serbest metin, kayda girmez).
3. **Deneme örneklemi:** her alan için cevabı bilinen 10 satır (kullanıcının kararlarından ve kurulumun bilinen
   hatalarından; en az 2'si yanlış bağ, 1'i tuzak: kelimesi benzeyen ama sözü farklı). Ölçü: en çok 1 hata ve
   yanlışların hepsinin yakalanması. Tutmayan aday reddedilmez, o alanda kaydedilmez; gerekçe kendisine söylenir.
   Deneme kararları `origin: {"trial": …}` ile ayrı dosyada durur, araçlara gitmez. **[Karar 5]**
4. **Kabul:** kullanıcı onaylar; denetçi `reviewers.json`'a alanlarıyla yazılır (`fields`, `since`, alan başına
   deneme tarihi). Kayıttan önce şartları kabul eder: kararların adıyla yayımlanacağı, silinmeyeceği, lisansı
   (Y0.5).
5. **İlk tur:** kendi alanından 40'lık örneklem (T7 gibi); sonuçları kullanıcıyla birlikte gözden geçirilir.

Kayıt alanları (Y1.2.1 için öneri; iletişim bilgisi bu dosyaya girmez):

```json
"ornek-kimlik": {
  "name": "Görünen ad",
  "fields": {"kuran": {"since": "2026-11-20", "trial": "2026-11-18"}, "arapca": {"since": "2026-11-20"}},
  "note": "isteğe bağlı kısa tanım (ör. 'ilahiyat, tefsir ABD')",
  "since": "2026-11-20"
}
```

Kullanıcının mevcut kaydı: `fields` kullanıcıya sorularak yazılır (Y1.2.3; öneri: `kuran`, `risale`; 94 karar bu iki
alanda). Proje sahibi olmak alan vermez. **[Karar 6]**

## 4. Kararların geçerliliği, itiraz, geri çekme

Bugünkü kurallar sürer; eklenenler:

- **Alanı tutmayan karar** kaydedilir, silinmez, `competent: false` ile görünür; bağı "denetlendi" yapmaz.
- **İki ehil denetçi ayrılırsa** (biri `reviewed`, öbürü `disputed`): bağ "ihtilaflı" görünür, iki karar gerekçesiyle
  yan yana; oylama yapılmaz, sayı üstünlük vermez. Araç ve talimat ihtilafı hüküm gibi değil ihtilaf olarak sunar.
  Gerekirse üçüncü bir ehil denetçinin görüşü eklenir, ama o da yalnız bir karardır. **[Karar 7]**
- **Güçte ayrılık** (biri `strong`, öbürü `weak`): ikisi de görünür; araç en temkinli olanı öne alır (`weak`).
- **Geri çekme** yalnız denetçinin kendi kararınadır (bugün öyle).
- **Kurallar değişince** kararın verildiği hâl `seen`'de durur; bağ değişmişse karar "eski hâle verildi" diye
  işaretlenir, yeniden bakılması için kuyruğa düşer (bugün `seen` var, işaretleme Y1.4'te).
- **Denetçinin ayrılması:** isterse ya da ehliyeti sorgulanırsa kayıt `until` tarihi alır; geçmiş kararları durur,
  ayrıldığı tarih görünür. Kararların silinmesini isterse: satırlar silinmez, ama görünen adı "ayrılan denetçi"ye
  çevrilebilir (kimliği kayıtta kalır). **[Karar 8]**
- **Kötüye kullanım** (bilerek yanlış karar, toplu itiraz, meşrep kavgası): kullanıcı kaydı `until` ile kapatır,
  kararları `competent: false` sayılır; gerekçe kayıtta.
- **Çıkar çatışması:** denetçi kendi eserinin ya da önerdiği bağın kararını veremez (katkı açıldığında, Y3; öneriyi
  verenle denetleyen ayrı kişi).

## 5. Görünen ad ve gizlilik

- **İsimli denetim:** kararın değeri kimin verdiğine bağlıdır; bu yüzden varsayılan gerçek ad (unvanıyla ya da
  unvansız, kişinin seçtiği biçimde). Takma ada izin verilir mi: **[Karar 9]** (öneri: hayır; ama ad kısaltması,
  "M. Yılmaz" gibi, olabilir).
- **Yayımlanan:** görünen ad, alanlar, kayıt tarihi, kararları (araç sonuçlarında ve depoda). Yayımlanmayan:
  e-posta, telefon, eğitim beyanı, deneme sonuçlarının ayrıntısı; bunlar git'e girmez, kullanıcının kendi kaydında
  durur.
- **Depo:** `data/links/reviews/` git'tedir; depo açıksa (GitHub `fatihebrarinan/risale-mcp`) görünen ad ve kararlar
  herkese açıktır. Davette bu açıkça söylenir. **[Karar 10]**
- **Gizlilik politikası:** bugün denetçiden söz etmiyor. Denetçi kaydı sunucuda değil depoda tutulduğu sürece
  değişmesi gerekmez; katkı sunucudan yapılınca (Y3) Y0.5 ile birlikte değişir.

## 6. Bu belgenin bağladıkları

- Y1.2: `reviewers.json` şeması (`fields`, `since`, `until`, `note`), bağ türü → alan eşlemesi (2), `competent`.
- Y0.2: davet metni ve deneme örneklemleri (3).
- Y0.5: kayıtta kabul edilen şartlar, lisans.
- Y1.4: arayüz denetçinin alanını bilir, alanı dışındaki bağı ona göstermez ya da işaretli gösterir.

## Kararlar (kullanıcının)

1. Alanlar: `kuran`, `arapca`, `hadis`, `tefsir`, `risale` ve ayrı `metin` mi? (`arapca` ile `kuran` birleşsin mi?)
2. Kur'ân – Risale ilişki bağları için gereken alan yalnız `risale` mi, `risale` ve `kuran` birlikte mi?
3. Risale ile müfessir arasındaki ilişki iki alan mı ister (`tefsir` ve `risale`), biri yeter mi?
4. İlk aşamada yalnız davetle mi, yoksa sayfadan yazan herkes deneme örneklemine girebilir mi?
5. Deneme örneklemi: 10 satır, en çok 1 hata ve yanlışların hepsi yakalanmalı. Kabul mü, başka ölçü mü? Deneme
   olmadan, kullanıcının tanıdığı ehil kişi doğrudan kaydedilebilir mi?
6. Kullanıcının kendi alanları: `kuran` ve `risale` mi?
7. İhtilafta oylama yok, iki karar yan yana: kabul mü?
8. Ayrılan denetçinin adı istenirse gizlenebilir mi?
9. Takma ad olmaz, kısaltma olabilir: kabul mü?
10. Depo açık mı kalacak; denetçilerin adları ve kararları herkese açık olacak mı?
