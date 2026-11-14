# Taslak döngüsü

İşârâtü'l-İ'câz usulüyle yapay zekâ taslağının geliştirilmesi bir döngüdür (kullanıcının fikri ve kararı,
2026-11-14). Her tur: **yaz** (istemin bir sürümüyle), **kapalı kitapla karşılaştır** (D7: İşârât'ın gizlenen metninin
nükte envanteriyle), **açık kitapla eleştir** (D9: eklentiler açık, İşârât gizlenmeden), **insanla süz** (örneklemler),
gerekirse **kör noktayı ara** (D6), **dersleri genel usul olarak istemin yeni sürümüne yaz**. Durumu ve sırası
`PLANLAR.md`'dedir; burada her tur bir satırdır, kararın gerekçesi yanında.

## Kurallar

- **Durma ölçütü "eleştiri olumlu olana kadar" değildir.** Yazan da ölçen de Claude'dur; eleştiri olumluya döndükçe
  ya taslak iyileşmiştir ya da ikisi aynı kör noktada buluşmuştur (D6'da A10). Olumlu eleştiriyi hedef yapmak modeli
  eleştirmenin beğendiğini yazmaya yöneltir.
- **Birimler zincir olur, karşılaştırma yeni birimde yapılır** (kullanıcının düzeni ve tasarruflu seçimi,
  2026-11-14). Her turun yeni birimi bir sonraki turun ders birimidir: 11–12 → 17–20 → 21. Yeni birimde **eski ve yeni
  istem yan yana**, üçer taslak yazılır: fark yalnız istemden gelir, birimin kolay ya da zor olmasından değil. Dersin
  çıktığı birimde yeni istemle yeniden yazılmaz (orada iyi çıkması kısmen önceden bellidir, kurallar o birimin
  eksiklerine göre seçildi); yalnız yeni istemin davranışı değiştirip değiştirmediğinden şüphe edilirse eklenir. Yeni
  birimin altı taslağı (eski ve yeni istem) bir sonraki turun ders verisidir.
- **Birimler harcanır.** Bir birimden ders çıkınca artık kör sınama olmaz. İşârât'ın kapsadığı aralıkta Bakara'da 23
  birim var (Fâtiha ayrıca, kelime kelime). Tur sayısının doğal sınırı budur.
- **Bir turun içinde ölçü sabittir.** Bir turun karşılaştırması aynı birimde, aynı ölçüyle (karşılaştırıcının ve
  eleştirmenin aynı sürümüyle) yapılır. Ölçü turlar arasında değişebilir; o zaman turların sayıları birbiriyle değil,
  her tur kendi içinde (eski ve yeni istem) karşılaştırılır.
- **Her turda değişmeyenler:** cevap anahtarı (envanter, birim başına bir kez), birim başına üç taslak, model ve
  düşünme düzeyi (Fable 5.2, yüksek), karşılaştırıcıda iki kör okuyucu (Fable 5.2, Opus 5.5), eleştirmen Opus 5.5.
- **İnsan emeği her turda:** D7.7 gibi karşılaştırma örneklemi (≈30 satır) ve D9.3 gibi süzgeç (10 not ve o turun
  sistemli başlıkları). **Eleştirmen değişince:** kör nokta okuması (D6 gibi, dar sorularla). Tur başına ≈1 saat.
- **Ölçütler** (her tur, ayrılmış birimde, eski ve yeni istem):
  1. D7 kapsaması (aynen + kısmen / envanter) ve aynenlerin sayısı;
  2. D9.1'in mekanik sayıları: kendi Türkçesi tırnakta, kaynağa nisbet edilip bulunmayan Arapça tırnak, "kendi
     tespiti" adayı, kapsam adayı;
  3. sistemli başlıklar (1. turda Z1–Z9): yeni taslakların eleştirisinde kaçı yine çıkıyor;
  4. çelişkiler (v2'den sonra kısmi çelişki dahil).
- **Durma:** bir tur ayrılmış birimde ölçülür bir iyileşme getirmezse ya da kalan hatalar yalnız ehlin görebileceği
  türdense (belâgat isabeti) döngü durur, D5'e (Bakara 34 ve sonrası) geçilir. Beklenen: iki ya da üç tur.
- **Maliyet:** tur başına 6 taslak; yazma, envanter (≈2 $), eşleştirme (≈13 $), eleştiri (≈16 $): ≈30–35 $ liste
  fiyatı (Max planı).

## Turlar

| Tur | İstem | Birim (rol) | Taslak | Kapsama (iki okuyucunun ortak) | İnsan | Karar |
|---|---|---|---|---|---|---|
| 1 (D1, D2, D7, D9, D6; 2026-11-10/14) | v1 tam (1), v1-ince (2–3), v1-ince-klasik (4–6) | 11–12 (ders) | 6 | %71, %76, %71; %68, %73, %68 | D7.7 güven %95 (30/30); D9.3 10/10 not, 9/9 başlık kalsın; D6 24'te 20 doğru, 1 yanlış | Devam: dersler istem v2'ye (`d9-rapor.md` "D8'e geçenler", 11 madde); ölçü: karşılaştırıcı v2, eleştirmen v1.2 |
| 2 (D8; planlı) | v1-ince-klasik ve v2-ince-klasik yan yana | **17–20** (yeni birim, temsil türü; 3. turun ders birimi) | 3 + 3 | — | D7.7 ve D9.3 gibi; eleştirmen v1.2 olduğu için kapsam notlarından dar bir kör nokta okuması | — |
| 3 (gerekirse) | v2 ve v3 yan yana | 21 (yeni birim, hüküm türü) | 3 + 3 | — | — | — |

1. tur ayrıntıları: `data/d1/provalar/11-12/` (`rapor.md`, `d2-rapor.md`, `yz-karsilastirma.md`, `d9-rapor.md`,
`d6-rapor.md`). 1. turda D1 ile D2'nin farkı yalnız eserlerdi (klasik eserler kapsamayı artırmadı, dayanağı
güçlendirdi); tam istem ince istemden iyi değildi.

## Birimler

| Birim | Tür | Durum |
|---|---|---|
| 11–12 | nazm ve lafız (nehiy, iddia ve red) | 1. turun birimi ve 2. turun ders birimi; yeniden yazılmaz |
| 9–10, 13 | nazm ve lafız | 1. turda eleştiride çok okundu: kör sınama için kullanılmaz |
| 17–20 | temsil (Kur'ân'ın meseli, nazarî giriş) | 2. turun yeni birimi, 3. turun ders birimi; hazırlığı usul özetinden (≈21 yer) ve birim çizelgesinden (≈13 yer) 17–20'ye dayanan örneklerin çıkarılmasını ister |
| 21, 22 | hüküm, emir | 21 3. turun yeni birimi (gerekirse; D3'ün "hüküm" türü); 22 kenarda |
| Öbürleri | | Kenarda; D5'e geçerken birkaçı kör sınama için ayrılmış kalır |
