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
| 3 | Lafız farkı ve mânen nakil adayları | Sırada |
| 4 | Türkçe aktarılan hadisler için daraltılmış aday listesi | |
| 5 | Rivayet denetimi: senet, sözün sahibi, kitap türü, "hadis değildir" diyen geçiş | |
| 6 | Künye uyumu: yalnız künyesiz bulunan eşleşmelerde | |
| 7 | Bağımsız model okuması: künyeyi ve önceki kararı görmez | |
| 8 | Hadisçi örneklemi; kararlar `tests/golden/`'a kilitlenir | |

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

## Adım 3'e başlarken

Dal `hadis-katmani`, son commit'ler `b6e8d20`, `dd6fecd`, push kullanıcıda. Girdi: ana metinde 142 "bulunamadı" parça. Çıktı kesin eşleşme değil, gözden geçirilecek aday listesidir. Benzerlik otomatik eşleme olamaz (`اَوَّلُ مَا خَلَقَ اللّٰهُ نُور۪ي` için en yakın sonuç başka hadis olabilir). Künyedeki `by_meaning` işareti (194 kayıt) kanıttır. İlişki türleri: `verbatim`, `abridged`, `by_meaning`. Model gerekirse önce maliyet tahmini verilip sorulur. Adım sonunda `hadis_eval` raporu ve fark gösterilir, onay beklenir.

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
