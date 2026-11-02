# Hadis katmanı: eşleme ve doğrulama planı

Hedef: Risale'deki hadisleri rivayetlere bağlamak, bağları doğrulamak, bilinen ve olası hataları en aza indirmek.
Yöntemin ayrıntısı `src/risale_mcp/hadis.py` başında, sayılar `uv run python -m risale_mcp.hadis_eval run`
raporundadır. Son güncelleme: 2026-11-02.

## Kararlar (kullanıcı, 2026-11-02)

- **Sanadset metni doğru kabul edilir.** Baskısından teyit plana girmez. Üst kaynağı bilinmediği için not `docs/izinler.md`'dedir.
- **Nurpedia:** elindeki her şeyi kullanmaya izin verdi; künyeleri kullanılır.
- **Dorar:** kullanıcı "sitede telif yazısı yoksa kullanılır" dedi. Yazı var (`docs/izinler.md`), şart oluşmadı, kullanılmıyor.
- **Hadisçi:** kullanıcı arıyor. Örneklem yine hazırlanır.
- **Ara sürüm:** Adım 0'dan sonra.
- **Mânen nakil asıl durumdur.** Müellif hadisi çoğu yerde rivayet edildiği gibi değil, kendi ifadesiyle yazar. Amaç "bu kısım şu hadisin müellif tarafından anlamı korunarak ifade edilmişidir" diyebilmektir. Lafız farkı eşleşmeme değil, ayrı bir ilişki türüdür (`verbatim`, `abridged`, `by_meaning`).
- **Künye ayrıştırması temeldir.** İleride kurulacak `hadis` profiline hizmet eder: kitaplar tek kayıtta (kimlik, Türkçe yazılışlar, Arapça ad, derlem karşılığı), künyeler Risale'den bağımsız yapıda durur.

## Sıra

Her adımın sonunda `hadis_eval` raporu ve önceki ölçümle fark gösterilir; kullanıcı onaylamadan sonrakine geçilmez.

| # | Adım | Durum |
|---|---|---|
| 0 | Kod hataları, kanıt modeli, `found` ayrımı, dondurulmuş ölçüm | Yapıldı |
| 1 | Künye ayrıştırma ve kitap kaydı | Yapıldı |
| 2 | Kısa parçalar için künyeli arama, geçiş başına | Yapıldı |
| 3 | Lafız farkı ve mânen nakil adayları | Yapıldı |
| 4 | Türkçe aktarılan hadisler için daraltılmış aday listesi | Yapıldı |
| 5 | Rivayet denetimi: senet, sözün sahibi, kitap türü, "hadis değildir" diyen geçiş | Yapıldı |
| 6 | Künye uyumu: yalnız künyesiz bulunan eşleşmelerde | Yapıldı |
| 7 | Bağımsız model okuması: künyeyi ve önceki kararı görmez | Yapıldı |
| 8 | Hadisçi örneklemi; kararlar `tests/golden/`'a kilitlenir | Örneklem hazır, hadisçi bekleniyor |

Yeni kaynak ayrı koldur: Keşfü'l-Hafâ, Feyzü'l-Kadîr, Kenzü'l-Ummâl, İhyâ, Mecmaü'z-Zevâid, el-Câmiu's-Sağîr. İzinli kaynak bulunmadan eklenmez.

## Adım 0 sonucu

Ana metin, 359 tekil parça: `found` 83, `partly_found` 18, `phrase_found` 41, bulunamayan 142, aranmayan 75. Önceki 126 `found`un 42'si `phrase_found`, 2'si `partly_found` oldu; 1 kesikli parça yeni bulundu, 1 `partly_found` düştü.
Donmuş kontrol (563): 4 ve daha az kelimede 8/41 `phrase_found`; 5 ve üstünde 3/522 `found`, 10/522 `partly_found`. `partly_found` %1,9 ile tamamen temiz değil, Adım 5–7'de sınanır.

## Adım 2 sonucu

Kısa parça, geçişin künyesindeki kitabın anılan bölümünde kelime sınırıyla geçiyorsa `located_chapter` olur; rivayetler `hadith_located`'da, geçiş başına. Yalnız Hadith API kitaplarında bölüm vardır (Kütüb-i Sitte, Muvatta); Müsned ve Sanadset kitapları bu yoldan bağlanamaz.

Karşı sınama (künyeler parçalar arasında karıştırılır, 5 tur):

| Kelime | Ayar: gerçek / karışık bölümde | Sınama: gerçek / karışık bölümde |
|---|---|---|
| 2 | %25 / %3,0 | %47 / %9,4 |
| 3 | %19 / %3,8 | %40 / %0 |
| 4 | %10 / %1,0 | %20 / %4,0 |

Kitap düzeyinde (ayar, bölümsüz ve bölümlü toplam) gerçek %31–35, karışık %27–36: kitapta geçmek kanıt değildir, `located_book` bu yüzden kaldırıldı. Tek kelimelik parça aranmaz. Küme küçük (sınamada 37 parça); oranlar yön gösterir, hassas ölçüm değildir. `located_chapter`'ın karışık künyeye göre hata tabanı kabaca her on bulgudan biridir, tekil kayıt doğrulanmış sayılmaz.

Kalan sınırlar:

- Sonuç: 26 tekil parça, 92 geçiş (ana metinde 61). Bulunan rivayetler `hadith_located`'da.
- Karışık künyeye göre kabaca her on bulgudan biri tesadüfi olabilir. Sınama kümesi küçüktür.
- Yalnız Kütüb-i Sitte ve Muvatta'da bölüm vardır. Müsned, Şifâ, Keşfü'l-Hafâ gibi kitaplara dayanan kısa parçalar bu yoldan bağlanamaz.
- Tek kelimelik parça aranmaz.
- Aynı parçanın geçişleri arasında dayanak farkı henüz çıkmadı; altyapı hazır.
- Bazı bulgular uzun bir duanın küçük parçasıdır ("لَهُ الْمُلْكُ"): rivayet doğru olsa da parça hadisin kendisi değildir.
- 12 örnekle bakıldı, tam doğrulama değildir.
- Sunucu Adım 0 sürümündedir (şema 9). Yerel şema 11: sonraki deploy veriyle yapılır, `--code` yetmez.

## Adım 8 durumu

`hadis_ornek.py`. Örneklem `data/interim/hadis/ornek/hadis-orneklemi.xlsx` (87 satır, 40'ı Öncelik 1); gönderilmeyecek anahtar aynı klasörde `key.json`. Biçim kullanıcıdan gelmedi, açılır seçimli Excel seçildi. Hadisçi model kararlarını ve tabakaları görmez; kontrol satırı olduğu söylenir, hangileri olduğu söylenmez.

Tabakalar (Öncelik 1 / toplam): `by_meaning` 10/23, başkasının sözü 8/17, reddeden ifade 4/6, modelin reddettiği aday 3/6, `located_chapter` 6/12, `verbatim` 3/8, kontrol 4/6, Türkçe tuzak 2/3, ilişki türünde ayrılan 0/6. `located_chapter` modelden geçmedi, bu örneklemde ilk kez okunacak.

Doldurulunca: `uv run python -m risale_mcp.hadis_ornek collect <dosya>` kararları `tests/golden/hadis_review.json`'a yazar, model okumasıyla karşılaştırmayı `ornek/karsilastirma.md`'ye. Dosya başka örneklemdense durur. Kilitlenen kararlar `hadith_support`'u kendiliğinden değiştirmez; hangi kararın veriye nasıl gireceği kararlar görüldükten sonra belirlenir.

Bekleyen: Yayın (`deploy`) ve şema değişikliği yapılmadı, sunucu Adım 0 sürümünde. Adım 3–8 çıktıları `data/interim/`'dedir, araçlara girmedi.

## Adım 7 sonucu

`hadis_okuma.py`, sonuç `data/interim/hadis/okuma.{md,json}`, ölçüm `adim-7.md`. `hadith_support` ve veritabanı değişmedi. İki bağımsız model okuyucu 190 çifti yalnız Arapçadan okudu: kitap adı, künye, seviye ve kuyruk gizliydi. 160'ı gerçek eşleşme, 30'u parçaya rastgele başka parçanın rivayeti verilmiş kontrol.

| Küme | Çift | İkisi de aynı söz | İkisi de değil | Ayrılan |
|---|---|---|---|---|
| Kontrol | 30 | 0 | 30 | 0 |
| `found` | 89 | 89 | 0 | 0 |
| `partly_found` | 19 | 19 | 0 | 0 |
| Aday `chapter` | 25 | 21 | 4 | 0 |
| Aday `close` | 27 | 25 | 2 | 0 |

Aynı söz mü sorusunda okuyucular 160/160 uyuştu; ilişki türünde 142/160 (ayrılanlar çoğunlukla `abridged` / `by_meaning`). Tam uyumda ilk okuyucunun ilişkisi: `verbatim` 92, `by_meaning` 29, `abridged` 15, `related` 5, `different` 1. Sınama kümesinde aynı söz 47/48, ayarda 107/112.

- 52 adayın 46'sını iki okuyucu da aynı söz dedi: Adım 3 listesi büyük ölçüde gerçek lafız farkıdır. 6'sı `related` ya da `different`; hepsi `chapter` 4 ve `close` 2.
- Söz sahibi, iki okuyucu da aynı dedi: Peygamber 126, başkası 17, belirsiz 15. Başkası denenlerin arasında "يا آل الذبيح" (görünmeyen bir ses), "تسمع بالمعيدي" (bir kadının sözü), "اذا جاء القدر" (Tirmizî'nin sözü), "حب الدنيا" (bu kayıtta Hz. İsâ'nın sözü) var. Tek rivayete dayanır: başka rivayette söz Peygamber'in olabilir.
- Reddi iki okuyucu da 6 çiftte gördü, kontrolde 0.

Kalan sınırlar:

- Kontrol kolaydı: rastgele çift çoğu zaman bambaşka konudur. 30'da 0 hata, "sayısı farklı ama çok benzeyen" tuzağı ("iki yüz defa" / "yetmiş") ölçmez. 30 örnekte hata çıkmasa bile gerçek oran ≈%10'a kadar olabilir.
- İki okuyucu aynı modeldir, hataları ortaktır: 160/160 uyum bağımsız iki uzman demek değildir.
- Okuyucular yalnız gösterilen rivayeti okudu (parça başına 1–2) ve "ezberden yargılama" dendiği hâlde bilgi sızmış olabilir.
- `found` için aynı söz cevabı neredeyse kelime eşleşmesinin tekrarıdır. Sıhhat, senet ve hüküm sorulmadı.
- Okuma Türkçe aktarılan 101 cümleyi kapsamadı.

## Adım 6 sonucu

`hadis_uyum.py`, liste `data/interim/hadis/uyum.{md,json}`, ölçüm `adim-6.md`. `hadith_support` değişmedi. Yalnız `found` ve `partly_found`; künyeyle bulunan `located_chapter` döngüsel olurdu, sınanmadı. Bulunan bütün rivayetlere bakıldı, seçilmiş 8'e değil. Sayım geçiş ve künye başınadır (112).

| Küme | Geçiş | `chapter` | `book` | `absent` | `no_corpus` |
|---|---|---|---|---|---|
| Ayar gerçek | 78 | 27 | 15 | 22 | 14 |
| Ayar karışık | 78 | 3,9 | 23,5 | 37,7 | 12,9 |
| Sınama gerçek | 34 | 10 | 9 | 11 | 4 |
| Sınama karışık | 34 | 1,2 | 9,6 | 18,1 | 5,1 |

Künyenin bölümü karışık künyeye göre yaklaşık 7–8 kat tutuyor. `book` karışıktan yüksek değil: Adım 2'deki gibi kitapta geçmek kanıt değildir, yalnız bölüm kanıttır.

Kitapta bulunan metinde bölüm 87 künyenin 83'ünde tuttu (Adım 1'deki %85 seçilmiş rivayetlerle, kısa parçalar dahildi; aynı ölçüm değildir). "no." 5'te 2 tuttu, küme çok küçük: rivayete doğrudan götürmez.

Kalan sınırlar:

- `absent` 33 geçiş: künye yanlıştır demek değildir. Örnekte çoğu bilinen hadis, künyedeki kitapta başka lafızla duruyor. 5'i "bk." ya da "iktibas". Lafız farkı mı yanlış künye mi ayrımı yapılmadı, Adım 7'nin girdisidir.
- `no_corpus` 18 geçiş sınanamadı (Keşfü'l-Hafâ gibi kitaplar).
- Bölüm yalnız Hadith API kitaplarındadır; öbür kitaplarda en çok `book` çıkar, bu da kanıt değildir.

Hadis işaretinin dayanağı (Adım 5'in `no_prophet` kuyruğu, 21 parça): `kaynak` 15, `meal` 15, `kaynakca` 5, `erisale` 1 (aynı parçada birden çoğu olabilir). "يا آل الذبيح" `kaynak` ve `meal`: işaret kaynağındır, kural gereği değişmez. "تسمع بالمعيدي" yalnız `kaynakca`: işareti `arabic_kinds` verdi, kaynakçası hadis kitabı gösteriyor; değiştirilmedi.

## Adım 5 sonucu

`hadis_rivayet.py`, liste `data/interim/hadis/rivayet.{md,json}`, ölçüm `adim-5.md`. Hüküm verilmez: hiçbir eşleşme silinmedi, `hadith_support`, veritabanı ve araçlar değişmedi. Denetim 101 eşleşmeli parçaya (`found`, `partly_found`) ve Adım 3'ün 51 adayına uygulandı.

| Kuyruk | found (83) | partly_found (18) | aday chapter (24) | aday close (27) |
|---|---|---|---|---|
| Sözün yanında reddeden ifade | 6 | 0 | 0 | 1 |
| Başkasının sözü denilmiş | 1 | 0 | 0 | 0 |
| Yalnız mevzu ve zayıf kitaplarında | 3 | 2 | 0 | 3 |
| Peygamber'e bağlı görünmüyor | 6 | 3 | 5 | 7 |
| Senet yok | 7 | 2 | 0 | 4 |
| Zayıflatan ifade | 2 | 0 | 0 | 0 |
| Kuyruk yok | 73 | 13 | 19 | 20 |

`denied` taşıyan 7 parçanın hepsi model tarafından okundu; kelime tutması çıkmadı, ifadeler gerçek tenkit ifadesidir (ör. "علماء امتي كأنبياء بني إسرائيل" için "لا اصل له"). Buhârî ve Müslim'den 71 kayıtta `denied` ve `weakened` 0. Bu, sözün çürük olduğunu göstermez: "حب الدنيا رأس كل خطيئة" aynı satırda Hasan Basrî'ye hasen isnadla bağlanır, "انا مدينة العلم"daki ifade tek bir rivayet yolu hakkındadır, âlimler arasında ihtilaf vardır.

Kalan sınırlar:

- Bir tenkit ifadesi birden çok âlimin görüşünden yalnız biridir; kaynak metnin içeriğini tek yönlü özetlemek yanıltır, ifade âlimin adıyla verilmelidir.
- Yalnız eşleşmeden sonraki 30 kelimeye bakılır: önceki ya da başka kitaptaki tenkit görülmez. Tenkit yoksa söz sağlam demek değildir, seçilmiş en çok 8 rivayete bakılıyor.
- `speaker` zayıftır: `none` çoğu kez örtük "قال"dır, tek rivayet için hüküm olmaz, yalnız parça kuyruğu verir. Peygamber anılan rivayette söz başkasının olabilir (`prophet` doğrulanmış değildir); 532 `prophet` kaydının küçük örneği okundu.
- `no_prophet` kuyruğu yanlış sınıflandırmayı da gösterebilir: "يا آل الذبيح" (Buhârî'de kâhin sözü) ve "تسمع بالمعيدي" (atasözü) hadis parçası sayılmış, kaynağın ya da `arabic_kinds`'ın işareti ayrıca bakılmalı.
- Hadith API'de senet uzunluğu yok; senedin sıhhati hiçbir kayıtta denetlenmedi, yalnız varlığı.
- Kitap türü adından çıkar; 63 kayıt `diger`. Kurallar ayar örneğiyle düzeltildi; kuyruklar okunurken sınama parçaları da görüldü, kurallar sonrasında değişmedi.

## Adım 4 sonucu

`hadis_turkce.py`, liste `data/interim/hadis/turkce.{md,json}`. Veritabanı ve `arabic` değişmedi. Kural 101 cümle buldu: `quoted_hadith` 61, `quoted_prophet` 23, `reported` 17 (17'si Arapçası yanında olduğu için elendi). Kapsam ana cilt ve Eski Said; mecmualar ve tercümeler dışarıda.

40 cümlelik örneklemi (son süzgeçten önceki 103 cümleden) model okudu, kullanıcı ya da hadisçi değil: 4'ü açıkça yanlış (Ermeni fedâileri, İmam Şâfiî'den nakil, "hiç hadis yoktur" diyen iddia, genel cümle), 1'i şüpheli (müellifin hadisten çıkardığı anlam). Kaçırma oranı ölçülmedi.

Deneme (14 söz, Arapçayı model ezberden yazdı, API yok): 13'ünde yakın bir rivayet çıktı, 1'inde (ukke) çıkmadı. Bu oran doğruluk değildir, 14 söz elle seçildi:

- Model hadisi tanıyıp Arapçasını yazınca arama onun tanıdığını bulur: öneri kanıt değildir (olası hata 5).
- "Cehennem ateşi … iki yüz defa" için bulunan rivayet "yetmiş"tir: yakın görünen ama sayısı farklı söz. Otomatik bağ yanlış olurdu.
- "Cebrâil ders" adayı başka bir olay olabilir. "Dünya Âhiret mezraası" yalnız mevzu kitabında çıktı.

Parçalı cümleler var: tırnak içi "‥" bölünmesi ("“Bir zaman gelecek, Allah‥") sözü yarım bırakır.

## Adım 3 sonucu

`hadis_adaylar.py`, liste `data/interim/hadis/adaylar.{md,json}`, ölçüm `adim-3.md`. Eşleme değildir: `arabic`, `hadith_support`, veritabanı ve araçlar değişmedi; önceki ölçümün sayıları aynı kaldı. 142 "bulunamadı" parçanın 51'i (66 geçiş) öne çıktı: `chapter` 24, `close` 27; `review` 91.

Arama künyeyi görmez; seviyeler iki bağımsız kanıttır. İlk 10 adayın künyenin anılan bölümünde olması:

| Küme | Künyesi bölüm gösteren | Gerçek künye | Karışık künye |
|---|---|---|---|
| Ayar | 37 | 18 | 1,7 |
| Sınama | 18 | 6 | 0,9 |

`close` eşiği (12+ kelime 0,5; 8–11 0,7; 5–7 0,9; 4 ve daha az yok) negatif kontrolde ayar 4/354, sınama 2/187 geçti. 5–7 kelimede sınama 2/33: ayardaki %3 hedefinin üstünde, küme küçük.

Kalan sınırlar:

- Sınamada oran düştü (%49'dan %33'e); ayar eşik seçiminde kullanıldı, asıl oran sınamadakine daha yakın sayılmalı.
- `chapter` puana bakmaz, zayıf adaylar da girer ("يلقون قتلا وتشريدا" için yalnız tek kelime). Karışık künyeye göre bulguların kabaca her 7–15'te biri tesadüfidir.
- `chapter` yalnız bölümü olan kitaplarda çalışır (55 parça); Müsned, Şifâ, Keşfü'l-Hafâ dayanaklı parçalar yalnız `close` yoluyla çıkabilir.
- `abridged` ve `variant` yalnız ipucudur. `by_meaning` künyesi yalnız 4 parçada var; mânen nakil hükmü hiçbir parçada verilmedi.
- Salâvat gibi kalıp çerçeveler benzerliği şişirebilir: alıntının kendisi değil, çerçeve tutabilir. Bir kısmı mevzu kitaplarından gelir, "ليس بحديث" diyen kayıtlar da vardır (Adım 5).
- `stem` kökün ilk harfini ön ek sanabilir ("كتب"→"تب"; "بكتب" ile ayrı düşer), kaçıran aday olabilir. Anlamsal (vektör) arama denenmedi.
- Kaçırma oranı ölçülmedi: `review`'daki 91 parçanın kaçında gerçek karşılık olduğu bilinmiyor. 12 örnekle bakıldı, liste okunmadı.

## Adım 1 sonucu

`hadis_kitaplar.py` kitap kaydı (Risale'ye bağlı değil, `hadis` profili de kullanır), `hadis_kunye.py` ayrıştırıcı, `hadith_books`, `hadith_citations`, `hadith_locators` tabloları. Rapor: `data/interim/hadis/kunye.md`.

- 370 parçanın 365'i künyeli; 461 künye metninin yalnız 1'inde kitap bulunamadı (ham metni durur).
- Künyedeki kitap adı, metin o kitapta bulunursa Hadith API bölümüyle %85 tutar (149'da 127).
- Kitap adından sonraki sayı hadis sırası değildir, çoğunlukla bâbdır. "no." sayıları 15'te 3 tuttu: rivayete doğrudan götürmez.
- Kaynaktaki yazım hataları düzeltilmez: "Buharî, Ahkâm: 4, İmâra: 36" ve "Müslim, … Vitir 24" gibi kitaba uymayan adlar eşlenmeden durur (`section` boş).
- Künyesi yalnız Kütüb-i Sitte, Muvatta ve Müsned dışı kitapları gösteren 151 parça var; bir kısmı derlemde olmayan kitaplara dayanıyor, Adım 2 onları çözemeyebilir.

Kalan sınırlar:

- 56 farklı adla 425 kitap adı konumu bölüme bağlanmadı; çoğu bölüm tablosu olmayan kitaplardan, hepsi tek tek bakılmadı.
- Künye içinde 33, başta 35 tür artık metin var; çoğu açıklama, küçük bir kısmı kayıtta olmayan kitap olabilir.
- %85 ve 15'te 3 tek seferlik ölçümdür; Adım 6'da `hadis_eval`'e girer. Tutmayan 22 vaka örnek düzeyinde incelendi.

## Veride doğrulanmış hatalar

| Hata | Ölçüm | Durum |
|---|---|---|
| Sanadset'teki Nesâî adı (`سنن النسائى الصغرى`) tekrar önleme listesinde yoktu | 5.668 kayıt | Adım 0'da düzeltildi |
| Bir parçada en çok 8 rivayet, seçim sıraya bağlı | 73 parça sınıra dayandı | Adım 0: önce farklı kitaplar, toplam `reports_total` |
| "…" ve "الخ" ile kesilen parça tek parça aranıyordu | 13 parça, 9'u bulunamadı | Adım 0: `pieces` |
| Kısa `found` zayıf kanıt | Donmuş havuzda (563) 4 ve daha az kelime %20, 5 ve üstü %0,6; ölçüt harf değil kelime | Adım 0: `phrase_found` |
| Kelime sınırı denetimi yoktu | 126'nın 2'si yalnız harf dizisi | Adım 0: `partly_found` |
| Künye anahtara yayılıyordu, oysa aynı parça farklı yerde farklı künye taşır | 365 künyeli parçanın 149'unda fark | Adım 0: kısa parçada yalnız kendi künyesi. Tam çözüm Adım 2 |
| `found`, künyedeki rivayetin bulunduğunu göstermez | 85 parçanın 36'sı anılan kitapta değil | Adım 6 |
| Benzerlik puanı başka hadise gidebilir | `اَوَّلُ مَا خَلَقَ اللّٰهُ نُور۪ي` için Ebû Dâvûd | Adım 3: yalnız aday, otomatik eşleme yok |
| Tek biçim yok | ≈331 kitap ve sayı, ≈160 cilt ve sayfa, 25 diğer | Adım 1 |
| Sayılar farklı sistemlerde olabilir | "Edeb: 96" bâb gibi, "Salâtü'l-Müsâfirîn: 139" kitap içi sıra gibi; doğrulanacak | Adım 1 |

## Olası hatalar

Eşlemede:

1. Künye yanlış ya da yalnız ilgili bir rivayeti gösteriyor olabilir; "bk." ve "İktibas olarak" zayıf işarettir.
2. Künyedeki numara ile Hadith API ve Sanadset numaraları aynı sistemde olmayabilir; doğrudan eşlenmez.
3. Künyeli arama sıradan ifadeyle sonucu şişirebilir ("لَا شَر۪يكَ لَهُ"): ayrı ve zayıf seviye olur, `found` sayılmaz.
4. Aynı kısa ifade başka yerde başka hadisin parçası ya da dua olabilir: karar geçiş başınadır.
5. Model Arapça uydurabilir: öneri kanıt değildir, derlemde bulunması kanıttır; kısa aday doğrudan eşleşme sayılmaz.
6. Yalnız Türkçe aktarılan hadisin işaretlenecek Arapçası yoktur: ayrı aday tablosu gerekir, `arabic` ve kaynağın işareti değişmez.

Doğrulamada:

7. Döngüsel doğrulama: künyeyle bulunan eşleşme künye uyumu sınamasına girmez.
8. Öneren model kendini onaylayamaz: okuyan model künyeyi ve önceki kararı görmez.
9. Eşikler aynı veriye uydurulabilir: parçaların üçte biri sınama kümesidir (`hadis_eval.is_holdout`), ayar için bakılmaz.
10. Negatif kontrol kirlenebilir: havuz `tests/golden/hadis_control.json`'da dondu, Adım 4'te değişmez.
11. Kitapta geçmek hadis olduğunu göstermez: mevzu kitabında söz "hadis değildir" denmek için geçebilir (Adım 5).
12. Yayın etkisi: seviyeler değişince şema, araç notları, sunucu talimatı değişir; `--code` yetmez.
13. Örnekleme payı: 40 örnekte hata çıkmasa bile gerçek oran ≈%7'ye kadar olabilir.
