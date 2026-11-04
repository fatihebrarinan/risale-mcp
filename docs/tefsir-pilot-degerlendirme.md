# Tefsir pilotunun değerlendirmesi ve sonraki adımlar (2026-11-04)

`docs/tefsir-altyapi-plani.md`'deki hazırlık (H0–H6) ve Beyzâvî pilotu (T0–T7) bitti. Bu belge sonuçların
değerlendirmesi, kullanıcının beş sorusuna cevap ve bundan sonraki yol haritasıdır. Değerlendirme modelindir
(Claude); kararlar kullanıcınındır. Yol haritası kullanıcının dört adımı ve modelin eklemeleridir; sıra ve kapsam
kullanıcının onayıyla kesinleşir.

## Pilot ne gösterdi

**Metin katmanı kolay ve güvenilir.** İyi bir OpenITI nüshası varsa bir müfessirin eseri bir iki günde alınıyor:
39 âyet biriminin 39'u Tanzil'le tuttu, 977 cümle basılı sayfasıyla geldi, âyet ortak adres olduğu için Risale ile
yan yana durmak kendiliğinden oldu. Hazırlık adımlarının değeri de görüldü: pilot boyunca genel sunucunun araç çıktısı
yedi karşılaştırmanın hepsinde aynı kaldı, kimlik manifestosu kayma göstermedi.

**Mekanik bağlar güvenilir, ama denetimle.** Kur'ân alıntılarında JK'nın işaretleriyle ölçülen isabet %97,8. Yine de
kullanıcının 40'lık örneklemi iki kural hatası buldu (kalıp kelime "قائل", kısa eşleşme "علم ما"); ikisi de ölçüye
görünmeyen türdendi. Ölçüm gerekli ama yeterli değil: insan örneklemi başka şey yakalıyor.

**Asıl değerli kısım, metinler arası ilişki, mekanik çıkmıyor.** Arapça İşârât ile Beyzâvî'nin ortak 4 kelimelik
dizileri yalnız kalıp ifadeler; İşârât Beyzâvî'yi lafzen aktarmıyor. "Aynı görüş", "farklı görüş", "itiraz" ancak
okumayla bulunur. Altyapının darboğazı veri değil, ehil okumadır.

**Hadis tarafı zayıf.** «» içindeki 18 sözden 1'i derlemde kelimesi kelimesine bulundu. Beyzâvî'nin rivayetleri büyük
ölçüde mânen, bir kısmı (sûre fazîletleri gibi) hadisçilerin tartıştığı türden. HA2–HA3 tefsir için de ön şart.

**Sunum denetimin parçasıdır.** Örneklemde âyetin 160 harfte kesilmesi, kullanıcıya doğru alıntılara "yanlış"
dedirtti; bir commit başarısız testlerle girdi; bir satır yanlış bağdan açıklandı. Denetçinin önüne konan sunum,
denetimin kendisi kadar önemli: yanlış sunum ehil denetçiyi de yanıltır.

## 1. Pilot, altyapının geleceği hakkında ne söylüyor

- **Ölçeklenebilen: metin ve adres.** OpenITI'de onlarca klasik tefsir var, çoğu âyet başlıklı; T0–T3 her eser için
  tekrarlanabilir. "Bir âyeti açınca Risale, sonra Beyzâvî, Keşşâf, Râzî… kendi sözleriyle, cümle düzeyinde atıfla"
  görünümü onlarca esere çıkabilir.
- **Ölçeklenemeyen: ilişki ve hüküm.** İnsan emeği ister; pilot bu emeğin nereye harcanacağını da gösterdi: alıntıyı
  Arapça okuyan denetleyebilir, hadisi ancak hadisçi. "Katkı kapısı ilim ve ihtisasa göre açılır" ilkesi somutlaştı.
- **Beklenmeyen bulgu: lemma.** 114 lemma adayı tefsirin doğal birimini gösteriyor: âyetin kelimeleri. Kur'ân'a
  kelime düzeyinde adres verilirse (`quran:1:7:1-4`), farklı müfessirlerin aynı lafız üzerine söyledikleri mekanik
  olarak yan yana gelir. İlişkiyi kurmaz, ama hangi cümlelerin karşılaştırılacağını kesinleştirir ve okuyucunun işini
  daraltır.

## 2. Planda değişiklikler (yedi öneri)

1. **Kur'ân'a kelime düzeyinde adres.** Lemma bağları âyete değil kelime aralığına gider; eserler arası hizalama lafız
   düzeyinde olur. Âyet adresi bozulmaz, altına iner.
2. **Denetçinin ihtisası kayıtlı.** `reviewers.json`'a alan (Kur'ân alıntısı, hadis, ilişki…); bir bağ türünde yalnız
   o alanda ehil olanın kararı "denetlendi" sayılır.
3. **"Aday" bağ için resmî durum (`proposed`).** Model okumaları ve kullanıcı önerileri bağın kendisinde aday olarak
   durur, araçlarda öyle görünür; denetlenmemiş bağ denetlenmiş gibi sunulmaz.
4. **Denetim arayüzü.** T7'de elle kurulan HTML kalıcılaşır: tam âyet, vurgu, büyük Arapça, karar düğmesi, doğrudan
   denetim kaydına yazma (kontrol arayüzü genişletilebilir).
5. **HA2–HA3 tefsirin ön şartı.** Hadis kitapları eklenmeden tefsir eserlerinin hadis bağları zayıf kalır.
6. **Arama.** Türkçede ek ("Beyzâvî'nin"), Arapçada önek (و ف ب ل ال) ayıran arama; T4 altın sorusunda model yanlış
   aramadan "atıf yok" sonucuna vardı.
7. **Sıradaki eser: Keşşâf.** İşârât onu adıyla anar, Beyzâvî büyük ölçüde ondan süzülmüştür: ilk gerçek nakil
   bağları (Beyzâvî → Keşşâf) mekanik bulunabilir; metinden metne bağların ilk sınavı.

## 3. Risale, Hadis ve Tefsir için üç ayrı MCP

Yapı zaten böyle seçildi (CLAUDE.md, "Sunucular ve kapsam"): her sunucu kendi metnini taşır, öbürlerine kimlik ve
atıfla gönderir. Pilot bunun işlediğini gösterdi: `target_display` metni taşımadığı yeri atfıyla gösterir, sızma
koruması yalnız yerelde duranı dışarı çıkarmaz.

- **Lehine:** lisanslar karışmaz (hadis kitapları ve OpenITI CC BY-NC-SA, e-Risale kaynak gösterme şartı); her
  sunucunun talimatı kendi alanına odaklı (tek sunucuda Risale'nin "tefsir deme" kuralı ile Beyzâvî'nin "tefsirdir"
  gerçeği aynı talimatta çatışırdı; bu oturumda görüldü); araç listeleri kısa; kullanıcı yalnız ihtiyacını ekler.
- **Aleyhine:** kullanıcı üç bağdaştırıcı ekler, kurulum sayfası bunu iyi anlatmalı; sunucular arası birleştirmeyi
  model yapar ve unutabilir: talimat bir sunucunun verdiği kimliği öbürüne sormayı açıkça istemeli, altın sorular
  ölçmeli.
- **"Kendi cihazında"** iki türlü: (a) kendi Claude/ChatGPT uygulamasında uzak bağdaştırıcıyla (varsayılan; telefon,
  masaüstü, web, kurulum yok); (b) kendi bilgisayarında yerel kurulum (araştırmacılar için isteğe bağlı paket,
  veritabanı ≈400 MB). Yerelde anlamsal arama sorgu vektörü için ya kullanıcının Voyage anahtarını ya da bizim yalnız
  sorgu vektörü veren bir ucumuzu ister. OpenITI ticari olmayan dağıtıma izin verir; e-Risale ve risaleoku izinlerinin
  indirilebilir paketi kapsayıp kapsamadığı sorulmalı.

## 4. Yapay zekâ tefsir taslağı

**Yazabilir:** akıcı, atıflı, ikna edici bir metin. T1–T3 cevapları iyiydi, 12 atfın 12'si doğrulandı.

**Yazmamalı** (en azından "tefsir taslağı" biçiminde):

1. Akıcılık eksikleri gizler: T4'te model yanlış bir aramadan "atıf yok" sonucunu güvenle çıkardı; taslakta bu tür
   boşluk nesrin içinde kaybolur.
2. Taslak heyetin işini daraltır: önüne hazır metin konan heyet düzeltmeye başlar, sıfırdan düşünmez. Müellifin
   tarifinde heyetin elinde me'haz vardır, taslak değil.
3. Sorumluluk taşınamaz: tefsir ehliyet ve vebal işidir. Kullanıcının kuralı (yapay zekânın yazdığı "tefsir" diye
   anılmaz) bunu söyler.

**Öneri: taslak değil, âyet dosyası (me'haz dosyası).** Her âyet ya da lafız için katı biçimli dosya: her kaynak ne
diyor (kendi sözüyle, cümle düzeyinde atıfla, önce Risale); nerede birleşiyor, nerede ayrılıyor (yalnız kayıtlı
bağlara ve açık kanıta dayanarak); hangi hadise dayanılıyor ve dayanağın durumu (hüküm vermeden); açık sorular.
Modelin yorumu varsa ayrı başlıkta, "yapay zekâ derlemesidir, tefsir değildir" damgasıyla. Bir pilotla sınanır
(Fâtiha'nın birkaç lafzı): ölçüt, dosyanın heyetin işini kısaltıp kısaltmadığı, yanlış yönlendirip yönlendirmediği.

## 5. Kullanıcıların bağ kurması (katkı)

MCP yazma araçlarına izin verir; ama doğrudan bağ yazma değil, **öneri**:

- **`propose_link`:** iki uç (kimlik), tür, kanıt sözü, not. Sunucu ucun varlığını ve kanıt sözünün kaynak cümlede
  geçtiğini denetler (`cite` gibi). Öneri `proposed` olarak ayrı bir kuyruğa düşer; bağ dosyasına ehil denetçi
  `link_reviews` ile onaylayınca girer.
- **`report_error`:** yanlış bölünmüş cümle, yanlış âyet bağı; Aşama 16'nın kontrol kuyruğunu besler.
- **Hesap gerekir:** bugün sunucu hesapsız (açık kip). OAuth kodu yerinde; yazma araçları yalnız giriş yapmış
  kullanıcıya, muhtemelen ayrı bir "katkı" bağdaştırıcısıyla (okuma sunucusunun dizin başvurusu karışmasın).
- **Model öneri hazırlar, karar vermez:** kayıt "kullanıcının isteğiyle modelin hazırladığı öneri" diye düşer;
  denetçi her zaman insandır (kullanıcının kararı).
- **Riskler:** spam ve meşrep kavgası (hız sınırı, ihtisas alanları, itirazın silinmemesi); katkıların lisansı (katkı
  verenden açık onay, ör. CC BY-SA).

Denetim kaydı (H5) böylece katkı platformunun çekirdeği olur. Platform sonra; önce birkaç isimli denetçiyle akışın
işlediği görülür.

## Yol haritası

Kullanıcının dört adımı (2026-11-04):

1. Planda yedi değişiklik (yukarıda 2).
2. Tefsir ve Hadis MCP sunucuları (yukarıda 3; hadis için HA5).
3. Katkı altyapısı (yukarıda 5).
4. Katkılar ve daha çok bağ; ardından müfessirlerin sözlerini, ilim ehli kullanıcıların bağlarını ve yapay zekâ
   derlemelerini içeren âyet dosyaları (yukarıda 4).

Modelin eklemeleri (kullanıcının onayını bekler):

- **Türkçe erişim.** Kullanıcı B bölümünde Arapçayı ayırt edemedi; Türk kullanıcının çoğu da öyle. Müfessirlerin
  eserleri Arapça kaldıkça altyapı yalnız Arapça okuyana açık olur. İki yol: izinli Türkçe tercümeler (ör. Beyzâvî'nin
  yayımlanmış tercümeleri, izinle; HA4'teki gibi) ya da modelin tercümesi, açıkça "yapay zekâ tercümesi" diye
  işaretli, metin yerine geçmeyen, alıntılanmayan. Hangi yolun, hangi şartla kullanılacağı bir karardır; âyet
  dosyalarından önce verilmeli.
- **Denetçi bulmak.** Teknik olmayan ama en belirleyici adım: isimli, ihtisası belli birkaç denetçi (Arapça okuyan,
  hadisçi, tefsir bilen). Seçim ölçütü yazılı olmalı (planın açık sorusu). Denetçi olmadan 3. ve 4. adım bekler; bu
  yüzden 1. adımla birlikte başlamalı.
- **Âyet dosyası pilotu erken.** 4. adımın sonunu beklemeden, bugünkü veriyle (Risale + Beyzâvî, Fâtiha) bir dosya
  biçimi denenir; biçim erken düzelir, katkı altyapısı da neyi beslediğini bilerek kurulur.
- **İzinler ve lisans önceden.** e-Risale ve risaleoku izinlerinin yerel paketi ve hadis/tefsir sunucularını kapsayıp
  kapsamadığı; katkılar için lisans ve katılım şartları; yazma araçlarının dizin politikalarına uygunluğu. Sunucular ve
  katkı altyapısı bunlara bağlı.
- **Hesaplar (OAuth) katkıdan önce.** 3. adımın ön şartı; askıdaki OAuth yeniden açılır, katkı bağdaştırıcısıyla
  sınırlı.
- **Sunucular arası davranışın ölçümü.** Üç bağdaştırıcı birlikteyken modelin bir sunucunun kimliğini öbürüne sorup
  sormadığı altın sorularla ölçülür (2. adımın ölçütü).
- **Maliyet ve sürdürülebilirlik.** Kullanıcı ve sunucu arttıkça Voyage sorgu ücreti, sunucu kapasitesi, sınırlar;
  her yeni sunucuda yeniden hesaplanır.
- **Mevcut kullanıcıların güvencesi sürer.** Her adımda H0 (araç çıktısı) ve H1 (kimlik manifestosu): genel sunucunun
  gördüğü, beklenen fark dışında değişmez.
