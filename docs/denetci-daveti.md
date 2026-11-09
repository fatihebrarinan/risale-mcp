# Denetçi daveti (Y0.2; kullanıcının kararlarıyla, 2026-11-05)

> **Donduruldu (2026-11-09).** Bu belge ayrıntı ve geçmiştir; güncel durum ve sıra `PLANLAR.md`'de.

Yol haritasının Y0.2 adımı (`docs/tefsir-pilot-degerlendirme.md`): her alandan en az bir isimli denetçi. Usul ve
ölçüt `docs/denetci-olcutu.md`'dedir; bu belge davetin kendisidir: adımlar, davet metni, deneme örneklemleri.

**Adaylar bu depoda yazılmaz.** Depo herkese açıktır; adaylar, iletişim bilgileri ve durumları özel denetim
deposundadır (`data/links/reviews/adaylar.md`, `fatihebrarinan/risale-mcp-denetim`). Kabul edilen denetçi orada
`reviewers.json`'a alanlarıyla yazılır.

## 1. Adımlar

| # | Adım | Kim | Kayıt (`adaylar.md`) |
|---|---|---|---|
| 1 | Aday: tanıdık, tavsiye ya da katkı sayfasından yazan ve kullanıcının davet ettiği | Kullanıcı | `aday` |
| 2 | Davet: kişiye özel mesaj (aşağıda) ve tanıtım metni (`docs/tefsir-tanitim.md`) | Kullanıcı gönderir | `davet edildi`, tarih, kanal |
| 3 | Cevap: alanı ve kısa ehliyet beyanı (serbest metin, kayda girmez) | Aday | `kabul etti` / `istemedi` |
| 4 | Deneme: alan başına 10 satır (bkz. 3) | Model hazırlar, aday karar verir, kullanıcı değerlendirir | `deneme`, sonuç (alan başına) |
| 5 | Şartların kabulü: katılım şartları (`docs/katki-sartlari.md` 2, sürüm 1; e-postayla gönderilir, sitede yok) ve "kabul ediyorum" cevabı | Aday | `şartlar`, tarih; `reviewers.json`'da `terms` |
| 6 | Kayıt: `reviewers.json`'a numarası ve alanlarıyla (`since`, `trial`) | Kullanıcı onaylar | `kayıtlı`, numara |
| 7 | İlk tur: kendi alanından 40'lık örneklem | Aday | — |

Davet ve deneme Y0.5'ten önce yapılabilir; **kayıt Y0.5'i bekler**: aday neyi kabul ettiğini bilmeden kararı
adıyla kaydedilmez.

## 2. Davet metni

Kişiye özel gider; köşeli ayraçlı yerleri kullanıcı doldurur. Uzun hâli e-posta için, kısa hâli WhatsApp için.
Tanıtım metni (`docs/tefsir-tanitim.md`, "Metin") ekte ya da ardından gider.

### E-posta

> **Konu:** Risale-i Nur MCP: [alan] denetimi için davet
>
> Selamün aleyküm [hitap],
>
> [Sizi nereden tanıdığım / sizi kimin tavsiye ettiği.] Risale-i Nur'un ve tefsirlerin metinlerini cümle cümle
> kaynağına bağlayan bir altyapı üzerinde çalışıyoruz; kısa tanıtımı ekte. Bilgisayarın bulduğu bağların doğru
> olup olmadığına ancak ehil bir insan karar verebiliyor. [Alan] konusundaki bilginizden dolayı sizi bu işe
> davet etmek istiyorum.
>
> **İş nedir?** Önünüze bir bağ konur: iki yer (ör. bir tefsir cümlesi ve bir âyet) ve bağın kanıtı. Siz
> "doğru", "yanlış" ya da "not" dersiniz, isterseniz bağın gücünü de ("güçlü / zayıf"). Bir tur 40 satır
> kadardır; bilgisayar başında, kendi vaktinizde yapılır. Kaç tur yapacağınız size kalmış.
>
> [Alan paragrafı: aşağıdan]
>
> **Nasıl başlanır?** Önce cevabı bizce bilinen 10 satırlık küçük bir deneme gönderiyoruz. Amaç sizi sınamak
> değil, işin size uygun olup olmadığını ve bizim sunumumuzun anlaşılır olup olmadığını birlikte görmek.
>
> **Kararlarınız nasıl kaydedilir?**
> - Her karar adınızla ve tarihiyle kaydedilir, ama açıkta adınız görünmez: araçlarda yalnız size verilen sabit
>   bir numara ("Denetçi 3") ve alanınız görünür. Adınızı tefsiri yazacak heyet ve proje sahibi bilir.
> - Kararlar silinmez; fikriniz değişirse yeni bir kararla geri çekersiniz. Başka bir denetçi size katılmazsa iki
>   karar gerekçeleriyle yan yana durur, oylama yapılmaz.
> - Hüküm istemiyoruz: hadisin sıhhatine ya da bir yerin "tefsir" olduğuna karar vermiyorsunuz; yalnız bu iki yer
>   arasında söylenen bağın doğru olup olmadığına.
> - [Tefsir alanı için:] Tefsirler arası ve Risale ile tefsir arası bağlarda kararın gerekçesini kısaca yazmanızı
>   istiyoruz; bu bağlarda kararın asıl değeri gerekçesindedir.
> - Kayıttan önce katılım şartlarını (kararların lisansı, adınızın kimlerle paylaşılacağı, ayrılma hakkı) ayrıca
>   gönderiyoruz.
>
> Proje kazanç amacı gütmüyor; iş gönüllüdür. Uygun görürseniz hangi alanda yardımcı olabileceğinizi ve kısaca bu
> alandaki geçmişinizi yazmanız yeterli.
>
> [İmza, iletişim]

**Alan paragrafları:**

- **Kur'ân (`kuran`):** Tefsirlerde ve Risale'de geçen âyet alıntılarını denetliyoruz: bilgisayar bir cümlede
  Kur'ân'dan bir söz bulduğunu söylüyor; sözün gerçekten o âyetten olup olmadığını, müfessirin cümleyi âyetin
  hangi sözüyle açtığını ve kalıp ifadeyle alıntının ayrımını sizin gözünüz görür.
- **Hadis (`hadis`):** Risale'de ve tefsirlerde nakledilen hadislerin kaynaklarda bulunup bulunmadığını
  bilgisayarla aradık: bir kısmı kelimesi kelimesine çıktı, bir kısmı künyenin gösterdiği bölümde, bir kısmı
  mânen. Bulunanın gerçekten o rivayet olup olmadığına, lafız farkına ve mânen naklin yerinde olup olmadığına bir
  hadisçinin bakması gerekiyor. Derece hükmü istemiyoruz.
- **Tefsir (`tefsir`):** Müfessirlerin eserlerini (şimdilik Beyzâvî, sırada Keşşâf) âyet âyet aldık. Bir müfessirin
  öbüründen naklettiği yerleri, aynı ya da farklı görüşte oldukları yerleri ve Risale'nin bir müfessiri andığı
  yerleri ancak tefsir usûlünü bilen biri doğru bağlayabilir.
- **Risale (`risale`):** Risale'nin bir yerinin bir âyetle kurduğu bağı (âyete işaret, bölümün âyetle açılması,
  müellifin "Yani"si, "… sırrınca") kurallarla bulduk; bağın türü ve gücü doğru mu, Risale'yi bütün olarak bilen
  biri karar verir. Arapça bilmek bu alanda tek başına gerekmez, Kur'ân alanıyla birlikte istenir.
- **Metin (`metin`):** Risale metninin cümle bölmesini ve başlıklarını kontrol etmek. Arapça gerekmez; bu iş
  bağ denetimi değildir, kontrol arayüzüyle yapılır.

### WhatsApp (kısa)

> Selamün aleyküm [hitap]. Risale-i Nur ve tefsir metinlerini cümle cümle kaynağına bağlayan bir proje üzerinde
> çalışıyoruz; bilgisayarın bulduğu bağları denetleyecek ehil gönüllüler arıyoruz. [Alan] konusundaki bilginizden
> dolayı sizi davet etmek isterim. İş küçük örneklemlerle, kendi vaktinizde yapılıyor; kararlarınız adınızla
> kaydediliyor ama açıkta yalnız bir numara görünüyor. Uygun görürseniz kısa tanıtımı göndereyim.

## 3. Deneme örneklemleri

Ölçüt `docs/denetci-olcutu.md` 3'tedir: 10 satır, en az 2'si yanlış bağ, 1'i tuzak; en çok 1 hata ve
yanlışların hepsi yakalanmalı. Cevabın bilinmesi için kaynak gerekir; bugün alanlara göre:

| Alan | Doğru bilinen | Yanlış bilinen | Tuzak | Durum |
|---|---|---|---|---|
| `kuran` | Kullanıcının 30 güçlü kararı (Beyzâvî'nin Kur'ân alıntıları) ve 40 güçlü kararı (Kur'ân – Risale) | T7'de kural düzeltmesiyle kalkan 8 bağ ("قائل" kalıbı, "علم ما" kısa eşleşmesi); 2 zayıf karar | Kelimesi âyete benzeyen ama âyet olmayan söz (T7'nin kalıp ifadeleri) | Hazırlanabilir |
| `risale` | Kullanıcının 57 kararı (Kur'ân – Risale ilişkisi) | 5 "zayıf olmalı ya da olmamalı" kararı; 1. turun kural düzeltmeleri (uzaktaki "işâret" kelimesi, sûre adı, risale adı) | Âyet ile "işâret" kelimesi aynı cümlede ama birbirine bağlı değil | Hazırlanabilir |
| `hadis` | Yok: hiçbir hadis bağına ehil biri bakmadı | — | — | **Cevabı yapıdan bilinen satırlarla** (kullanıcının kararı): derlemde kelimesi kelimesine ve uzun bulunanlar doğru; aynı sözü başka bir rivayete, sayısı ya da bir kelimesi değiştirilmiş rivayete bağlayan kurgu satırlar yanlış (Adım 9'un tuzak kontrolleri gibi) |
| `tefsir` | Yok: tefsir alanında bugün yalnız âyet birimi bağları var (eserin yapısı söyler, sınanacak bir şey yok) | — | — | **Keşşâf'tan sonra** (Y1.7): Beyzâvî'nin Keşşâf'tan kelimesi kelimesine uzun nakilleri doğru, kaydırılmış nakil yanlış. Tefsir daveti Y1.7'yi bekler (kullanıcının kararı: bugün aday yok) |

Deneme dosyası T7 örneklemi gibi bir HTML'dir (tam âyet, vurgu, büyük Arapça); kalıcı denetim arayüzü (Y1.4)
gelince onunla. Deneme kararları ayrı dosyaya yazılır (`origin: {"trial": …}`), araçlara gitmez.

## 4. Kararlar (kullanıcı, 2026-11-05)

1. Adaylar: kullanıcı bir adayla görüşüyor (Risale, Kur'ân ve hadis alanları); adı özel depoda, sonuç gelince
   yazılır. Tefsir alanında bugün aday yok.
2. Hadis denemesi cevabı yapıdan bilinen satırlarla.
3. Tefsir daveti Keşşâf'ı (Y1.7) bekler.
4. Denetçinin adını tefsiri yazacak heyet ve proje sahibi bilir; davet metni bunu söyler. Denetçilerin birbirinin
   adını görmesi davette vaat edilmez (gerekirse Y3'te, denetçilerin onayıyla).
