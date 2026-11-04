# Tefsir pilotunun değerlendirmesi ve sonraki adımlar (2026-11-04)

`docs/tefsir-altyapi-plani.md`'deki hazırlık (H0–H6) ve Beyzâvî pilotu (T0–T7) bitti. Bu belge sonuçların
değerlendirmesi, kullanıcının beş sorusuna cevap ve bundan sonraki yol haritasıdır. Değerlendirme modelindir
(Claude); kararlar kullanıcınındır. Yol haritası kullanıcının dört adımı, modelin kabul edilen eklemeleri ve bunların açılımı olan nihai adım
listesidir (Y0–Y4).

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

Modelin eklemeleri (kullanıcı hepsini kabul etti, 2026-11-04):

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

## Nihai adım listesi (Y)

Kullanıcının dört adımı Y1–Y4'tür; Y0 hepsinin ön şartı olan kişiler, izinler ve kararlardır, teknik değildir ve
hemen, öbürleriyle aynı anda başlar. Her alt adım: iş, çıktı, bağımlılık (←), ölçüt. Adlar mevcut aşamalarla
(H, T, HA, Risale aşamaları) çakışmasın diye Y önekiyle. Kural her adımda aynıdır: kullanıcının kararı gereken yerde
durulur; genel sunucunun gördüğü yalnız beklenen yerde değişir (H0 araç çıktısı, H1 kimlik manifestosu); denetçi
insandır, model öneri hazırlar.

### Y0. Kişiler, izinler, kararlar (hemen; teknik değil)

| # | İş | Çıktı | ← | Ölçüt |
|---|---|---|---|---|
| Y0.1 | Denetçi ölçütü: ihtisas alanları (Kur'ân alıntısı, Arapça dil, hadis, tefsir, Risale), alan başına asgari ehliyet, davet ve kayıt usulü, itiraz ve geri çekme kuralları, görünen ad ve gizlilik | `docs/denetci-olcutu.md` (model taslak, kullanıcı karar) | — | Kullanıcının onayı |
| Y0.2 | Denetçi adayları: her alandan en az bir isimli kişi; davet metni; kabul edenler `reviewers.json`'a alanlarıyla | Davet e-postası taslağı, kayıtlar | Y0.1, Y1.2 | Her alanda en az bir denetçi |
| Y0.3 | İzin soruları: e-Risale ve risaleoku izinleri yerel indirilebilir paketi ve ayrı sunucuları (hadis, tefsir) kapsıyor mu; e-Risale'ye Osmanlıca sorusu (Aşama 19) aynı yazışmada; nurpedia bilgilendirme | E-posta taslakları, cevaplar `docs/izinler.md` ve `catalog/permissions.py`'de | — | Her kaynakta yazılı cevap |
| Y0.4 | Türkçe erişim kararı: (a) izinli Türkçe tercümeler (Beyzâvî'nin yayımlanmış tercümeleri; yayıncı listesi, izin e-postası; HA4 ile aynı usul), (b) modelin tercümesi: işaretli ("yapay zekâ tercümesi"), metin yerine geçmez, alıntılanmaz, atfedilmez; hangisi, hangi şartla, hangi sunucuda | Karar kaydı (planda), e-posta taslakları | — | Kullanıcının kararı; Y1.8'den önce |
| Y0.5 | Katkı lisansı ve katılım şartları: katkının lisansı (ör. CC BY-SA), katkı verenin onayı, adının görünmesi, geri çekme hakkı, kötüye kullanım; gizlilik politikasına etkisi (katkıda kimlik ve içerik saklanır) | `site/katki-sartlari.html` taslağı, `site/gizlilik.html` değişikliği | — | Kullanıcının onayı; Y3'ten önce |
| Y0.6 | Dizin politikaları: Claude ve OpenAI dizinlerinin yazma araçlarına, kimlik doğrulamaya, ayrı bağdaştırıcıya bakışı; okuma sunucusunun başvurusunun etkilenmemesi | Araştırma notu | — | Y3.1'den önce |

### Y1. Planda yedi değişiklik ve âyet dosyası pilotu (kullanıcının 1. adımı)

**Y1.1 Kur'ân'a kelime düzeyinde adres**
- Y1.1.1 Kelime listesi: Medine Mushafı hattının kelimeleri esas (vakıf işaretleri kelime değil, T7'de görüldü);
  imlâî metinle hizalama (Bakara 21 gibi kelime sayısı tutmayan âyetler listelenir, elle karar); `quran.json`'a
  kelimeler.
- Y1.1.2 Kimlik biçimi `quran:1:7:1-4` (sûre:âyet:ilk kelime-son kelime); `links._TARGET`, `Link.problems`,
  doğrulama; âyet adresi değişmez, kelime adresi altına iner.
- Y1.1.3 `get_ayah` kelime numaralarını verir (isteğe bağlı alan); `find_ayah` kelime aralığına giden bağları âyette
  de gösterir.
- Y1.1.4 Lemma bağları (Beyzâvî) kelime aralığına taşınır; Risale'nin âyet alıntıları âyette kalır (kelime eşlemesi
  ayrı karar).
- Y1.1.5 Ölçüt: T7'de onaylanan 114'e yakın lemma bağının hepsi doğru kelime aralığına iner (örneklemle); genel
  sunucuda beklenen fark yalnız `get_ayah`/`find_ayah`'ın yeni alanları.

**Y1.2 Denetçinin ihtisası**
- Y1.2.1 `reviewers.json`'a `fields` (Y0.1'in alanları), `since`, isteğe bağlı açıklama.
- Y1.2.2 Bağ türü → gereken alan eşlemesi (Kur'ân alıntısı: Arapça/Kur'ân; hadis: hadis; metinden metne ilişki:
  tefsir/Risale); alanı tutmayan denetçinin kararı kaydedilir ama "denetlendi" sayılmaz (`competent: false`).
- Y1.2.3 Araçlarda karar denetçinin adı ve alanıyla; mevcut 94 kararın alanı (kullanıcı: Kur'ân alıntısı ve âyet
  ilişkisi) kullanıcıya sorularak yazılır.
- Y1.2.4 Ölçüt: test; mevcut kararlar geçerli kalır.

**Y1.3 Aday bağ (`proposed`)**
- Y1.3.1 Bağ kaydına durum: `status: proposed | accepted` (varsayılan accepted: bugünkü kural ve yapı bağları);
  aday bağın kim tarafından hangi yöntemle önerildiği (`proposed_by`: model okuması, kullanıcı, kural adayı).
- Y1.3.2 Araçlar adayı ayrı gösterir (`proposed: true`), talimat adayı hüküm gibi sunmayı yasaklar; genel profile aday
  girer mi: kullanıcının kararı (varsayılan: girmez).
- Y1.3.3 Hadis model okumaları (`reading_lead`) bu biçime geçer (bugün ayrı tablo).
- Y1.3.4 Denetçi kabulü adayı `accepted` yapar (denetim kaydıyla; bağ dosyası değil karar değişir).
- Y1.3.5 Ölçüt: genel sunucuda fark yok; yerelde adaylar görünür ve ayrı.

**Y1.4 Denetim arayüzü**
- Y1.4.1 T7 örneklem üreticisi genelleşir: herhangi bir bağ dosyası ve tür için tabakalı örneklem, önceki seçimi
  koruma, karar verilmişleri işaretleme (`links_tefsir --sample`'dan ortak modüle).
- Y1.4.2 Sunum kuralları kalıcı: tam âyet, bulunan kelime âyette vurgulu, Arapça tek yazı tipi ve büyük, bağlam,
  kesme yok (T7'nin dersleri); denetçinin alanına göre gösterim (hadisçiye rivayet, Arapça okumayana Türkçe yardım
  Y0.4'e göre).
- Y1.4.3 Karar düğmeleri (✓, ✗, not) tarayıcıda; dışa aktarılan dosya `link_reviews add` ile toplu işlenir
  (kontrol arayüzündeki işaret akışı gibi); sonra Y3'te sunucudan.
- Y1.4.4 Ölçüt: kullanıcı bir örneklemi yalnız arayüzle karara bağlar, elle numara yazmadan.

**Y1.5 Hadis kaynakları (HA2–HA3, tefsirin ön şartı)**
- Y1.5.1 HA3: Müsned, Müstedrek, Dârimî… OpenITI'den (H6 okuyucu, `printed`: Müsned künyelerinin cilt:sayfası);
  her kitapta künye ve bölge ölçümü.
- Y1.5.2 HA2: eşleşme yalnız kütüphane kitaplarından; geçişte kaybolanlar sayılır.
- Y1.5.3 Beyzâvî'nin hadis adayları yeni kütüphaneyle yeniden eşlenir; T5'teki 18 sözün sonucu karşılaştırılır.
- Y1.5.4 Ölçüt: Risale'nin hadis sayıları geçişte açıklanır (kayıp yoksa aynı); hadisçi örneklemi (HA6) Y0.2'ye bağlı.

**Y1.6 Arama**
- Y1.6.1 Türkçe ek: kelime aramasında tam kelime ekli biçimi de bulur ("Beyzavi" → "Beyzâvî'nin"); kesmeden sonra
  ek dizine ayrı girer ya da sorgu kelime başı aramaya genişler (ölçüme göre).
- Y1.6.2 Arapça önek: و ف ب ل ك ال ayrıştırma (müfessirin eserlerinde ve Risale'nin Arapçasında).
- Y1.6.3 `db.NORMALIZATION` artar; `search_eval` ve altın soru T4 yeniden; anlamsal arama etkilenmez.
- Y1.6.4 Ölçüt: T4 altın sorusunda Muhâkemat'taki "Tefsîr-i Beyzâvî" bulunur; arama ölçümü düşmez.

**Y1.7 Keşşâf (ikinci eser)**
- Y1.7.1 T0–T3: nüsha (OpenITI `0538JarAllahZamakhshari.Kashshaf`), inceleme, kararlar, ayrıştırıcı (Beyzâvî'ninki
  ortaklaşır: `books/tefsir_openiti.py`), aralık Fâtiha ve Bakara 1–33.
- Y1.7.2 T5: yapı, Kur'ân alıntısı, hadis (Y1.5 sonrası), lemma (Y1.1 sonrası).
- Y1.7.3 Metinden metne ilk bağlar: Beyzâvî → Keşşâf ortak uzun diziler (`same_words`, nakilse `transmits`;
  yöntem kelime dizisi, kanıt dizi); örneklem.
- Y1.7.4 Ölçüt: Beyzâvî ile Keşşâf'ın aynı lemmadaki cümleleri yan yana; nakil bağı örnekleminde kullanıcının
  kararı.

**Y1.8 Âyet dosyası pilotu (erken)**
- Y1.8.1 Biçim: âyet ya da lafız başına bölümler: Kur'ân (metin, mealler), Risale (yerler, bağ türü ve kanıtıyla,
  önce), müfessirler (kendi sözleri, atıflı), hadis (dayanak, hüküm yok), kayıtlı ilişkiler, açık sorular, yapay zekâ
  derlemesi (ayrı başlık, damgalı: "yapay zekâ derlemesidir, tefsir değildir").
- Y1.8.2 Üretim: model, araçlarla, katı biçimde; her cümle atıflı (`cite` denetimi); Türkçe yardım Y0.4'e göre.
- Y1.8.3 Pilot: Fâtiha'nın birkaç lafzı (Risale + İşârât + Beyzâvî, Y1.7 bittiyse Keşşâf).
- Y1.8.4 Ölçüt: kullanıcı ve mümkünse bir denetçi değerlendirir: dosya heyetin işini kısaltıyor mu, yanlış
  yönlendiriyor mu; biçim karara bağlanır.

Önerilen sıra: Y1.1 ve Y1.3 (veri modeli) → Y1.2 → Y1.4 → Y1.6 → Y1.5 → Y1.7; Y1.8 Y1.1 ve Y0.4'ten sonra, Y1.7'yi
beklemeden.

### Y2. Tefsir ve Hadis sunucuları (kullanıcının 2. adımı)

| # | İş | Çıktı | ← | Ölçüt |
|---|---|---|---|---|
| Y2.1 | Hadis sunucusu (HA5): `hadis` profili, talimatı, araçları (kitap ve bâb, rivayet arama, künyeden bölgeye, Risale'deki yerler kimlik ve atıfla, dereceler âlimin adıyla), adresi (`mcp.risalemcp.com/hadis`), gizlilik ve tanıtım sayfası | Sunucu, sayfalar | Y1.5, Y0.3 | Altın sorular; risale sunucusunun çıktısı değişmez |
| Y2.2 | Tefsir sunucusu: `tefsir` profili (Kur'ân + müfessirlerin eserleri), talimatı (müfessirin eseri tefsirdir, modelin yazdığı değildir; Risale'nin yerleri kimlik ve atıfla önce), araçları (âyetten ve lafızdan eserler, lemma hizası, metinden metne bağlar, âyet dosyası Y1.8'in biçimiyle) | Sunucu | Y1.1, Y1.3, Y1.7, Y1.8 | Altın sorular |
| Y2.3 | Genel çıkış kararı: Beyzâvî ve Keşşâf'ın `private`'tan çıkması (OpenITI lisansı, kullanıcının kararı); bugün yerel profilin `CLASSICAL_INSTRUCTIONS`'ı tefsir sunucusuna taşınır | Karar, katalog değişikliği | Y2.2 | Kullanıcının kararı |
| Y2.4 | Risale sunucusu: talimata öbür sunuculara gönderme ("hadis ve tefsir bağdaştırıcısı ekliyse kimliği orada sor"); kendi metni değişmez | Talimat değişikliği | Y2.1, Y2.2 | H0'da yalnız talimat farkı |
| Y2.5 | Sunucular arası ölçüm: üç bağdaştırıcı birlikte altın sorular (bir sunucunun kimliği öbürüne soruluyor mu, atıflar doğru sunucudan mı) | `golden` çoklu sunucu kipi, rapor | Y2.1, Y2.2 | Kullanıcının belirlediği oran |
| Y2.6 | Kurulum: sitedeki kurulum sayfası üç bağdaştırıcıyı anlatır (Claude, ChatGPT, mobil); her sunucunun dizin başvurusu ayrı | Site, başvurular | Y2.1, Y2.2, Y0.6 | Kullanıcının denemesi |
| Y2.7 | Yerel paket (araştırmacılar için, isteğe bağlı): profil veritabanı indirilebilir, stdio; anlamsal arama için kullanıcının anahtarı ya da yalnız sorgu vektörü veren uç | Paket, belge | Y0.3 | İzin kapsamı yazılı |
| Y2.8 | Maliyet ve kapasite: sunucu başına bellek, Voyage sorgu ücreti, sınırlar; gerekirse sunucu büyütme | Not, sınır ayarları | Y2.1, Y2.2 | Kullanıcının bütçe kararı |

### Y3. Katkı altyapısı (kullanıcının 3. adımı)

| # | İş | Çıktı | ← | Ölçüt |
|---|---|---|---|---|
| Y3.1 | Hesaplar: askıdaki OAuth katkı bağdaştırıcısı için açılır (okuma sunucuları açık kipte kalır); hesap, görünen ad, denetçi bağlantısı (`reviewers.json` ile) | Kimlik doğrulamalı katkı adresi | Y0.5, Y0.6 | Giriş, oturum, iptal testleri |
| Y3.2 | Katkı araçları: `propose_link` (iki uç, tür, kanıt sözü, not; uç ve kanıt sözü sunucuda denetlenir), `report_error` (bölme, âyet bağı, metin hatası), `my_proposals` (durum); araç ek açıklamaları yazma aracı olarak | Katkı sunucusu | Y3.1, Y1.3 | Testler; geçersiz öneri reddedilir |
| Y3.3 | Kuyruk: öneriler sunucuda ayrı veritabanında (auth.db gibi yeniden kurulmaz), yerele çekilir; kabul edilen `data/links/` ve `data/links/reviews/`'a (git) girer, model önerisi `proposed_by` ile işaretli | `contributions.db`, çekme komutu | Y3.2 | Kayıp yok, her öneri izlenebilir |
| Y3.4 | Denetim akışı: denetim arayüzü (Y1.4) kuyruğu okur; denetçi alanına uyan önerileri görür; karar → bağ ve denetim kaydı; öneriyi verene durum bildirimi | Akış | Y1.4, Y1.2, Y3.3 | Bir öneri uçtan uca kabul edilir |
| Y3.5 | Kötüye kullanım: hız sınırı, hesap başına günlük öneri, tekrar önerinin birleşmesi, itirazın silinmemesi, meşrep tartışmasına karşı yalnız kanıtlı öneri | Sınırlar | Y3.2 | Deneme saldırısı |
| Y3.6 | Lisans ve onay: ilk katkıda şartların kabulü (Y0.5), katkının lisansı kayıtta | Onay kaydı | Y0.5, Y3.1 | Onaysız katkı kabul edilmez |
| Y3.7 | Hata bildirimlerinin işlenmesi: `report_error` Aşama 16'nın kontrol kuyruğunu besler | Kuyruk birleşmesi | Y3.2 | Bir bildirim düzeltmeye dönüşür |
| Y3.8 | Pilot: kullanıcı ve Y0.2'nin denetçileriyle kapalı deneme; sonra açılış kararı | Rapor | Y3.1–Y3.7 | Kullanıcının kararı |

### Y4. Katkılar, bağlar, âyet dosyaları (kullanıcının 4. adımı)

| # | İş | Çıktı | ← | Ölçüt |
|---|---|---|---|---|
| Y4.1 | Aday bağ üretimi: lemma hizasıyla (Y1.1) aynı lafız üzerine eserlerin cümleleri eşlenir; model okumaları (iki kör okuyucu, hadiste olduğu gibi) ilişki türü önerir: İşârât ↔ Beyzâvî, Beyzâvî ↔ Keşşâf; hepsi `proposed` | Aday dosyaları | Y1.1, Y1.3, Y1.7 | Okuyucuların uyuşma oranı |
| Y4.2 | Denetçilere iş listeleri: alan başına sıralı örneklemler (Y1.4), tur başına rapor; kararlar kurallara döner | Tur raporları | Y4.1, Y0.2, Y3.4 | Tur başına doğruluk |
| Y4.3 | Âyet dosyası (Y1.8'in kararlaşmış biçimi) kalıcı araç: tefsir sunucusunda; müfessirlerin sözleri, denetlenmiş ve aday bağlar ayrı, ilim ehlinin katkıları adıyla, yapay zekâ derlemesi damgalı | Araç, örnek dosyalar | Y1.8, Y2.2, Y4.2 | Kullanıcı ve denetçi değerlendirmesi |
| Y4.4 | Kapsam: İşârât'ın aralığı (Fâtiha, Bakara 1–33) tamamlanınca sıradaki aralık ve eserler kullanıcıyla seçilir (Râzî, Ebüssuûd, Elmalılı…; izin ve nüsha T0'daki gibi) | Seçim kaydı | Y4.3 | Kullanıcının kararı |
| Y4.5 | Heyete sunum: heyetin kullanacağı görünüm (dosya, dışa aktarma, sürüm etiketi: H1'in `corpus_version`'ı ile atıfların yeniden üretilebilirliği) ve geri bildirim yolu | Görünüm, belge | Y4.3 | Heyetin ya da denetçilerin değerlendirmesi |

### Sürekli olanlar

- Her deploy'dan önce H0 karşılaştırması, her kurulumda H1 manifestosu; beklenen fark `DEPLOY_EXPECT` ile.
- Her yeni eser ve bağ türünde ölçüm (otomatik) ve örneklem (insan); sunum denetimin parçasıdır (T7'nin dersi).
- Maliyet her yeni sunucu ve kullanıcı artışında yeniden hesaplanır.
- Kullanıcının kararı gereken yerde durulur; karar planlara ve CLAUDE.md'ye yazılır.
