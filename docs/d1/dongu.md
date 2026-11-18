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
  2026-11-14). Her turun yeni birimi bir sonraki turun ders birimidir: 11–12 → 31–33 → …. Yeni birimde **eski ve yeni
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
| 2 (D8; 2026-11-14/15) | v1-ince-klasik (1, 3, 5) ve v2-ince-klasik (2, 4, 6) yan yana | **31–33** (yeni birim, kıssa ve mu'cize türü) | 3 + 3 | v1 %47, %53, %53; v2 %49, %49, %49 (mukaddimesiz v1 %75, v2 %70) | Örneklemler yapılmadı (D7.7 düştü) | **Dur**: ölçülür iyileşme yok; yalnız Arapça tırnak kuralı tuttu, Z1 ve Z6 altı taslağın hepsinde. Karşılaştırma döngüden çıktı; asıl iş için yöntem değişir (D11: tek, kısa, ucuz taslak; istem değil hat sınanır) |
| 3 | Açılmadı: döngü 2. turda durdu (2026-11-15) | | | | | |
| D12.5 T1 (2026-11-17) | h2 (1) ve çizelge c1: okuma ayrı, yazım yalnız cite (2) | 9–10 (geliştirme) | 1 + 1 | tek okuyucu: %57, %70 | 3 nükte (okuma standardı): taban 2, yeni 0, emin değil 1 | Kör eleştirmen yeni hafif (V3 yeni açık, V2 taban açık); maliyet 2,2 kat, alıntı yağmuru; sizin hükmünüz tabandan yana: **yeni kol taban olmaz** (bitti; `provalar/9-10/d12-5-T1.md`) |
| D12.5 D (2026-11-17) | d1: kapalı notlarla düzeltme (3) ve d2: + ikinci kapalı eleştiri ve ikinci geçiş (4), taban taslak 1 (h2) | 9–10 | 2 düzeltme | tek okuyucu: 1 %57, 3 %64, 4 %62 | 3 nükte: d2 1, eşit 1, emin değil 1 | Kör: 1→3 açık, 3→4 hafif; Arapça +%23, sonra −%2,5; yanlış not (K30) düzeltmeye geçti; **d2 bırakıldı** (kullanıcı: maliyetine değmez), d1 kalır (`provalar/9-10/d12-5-D.md`) |
| D13 (2026-11-17) | h2 (1) ve h3 (5): me'haz hiyerarşisi (İşârât, Risale-i Nur'un konuya dair 267 paragrafı, Keşşâf ve belâgat; tefsirler araçla; istinbat etiketi) | 9–10 | 1 + 1 | tek okuyucu: %57, %60; farklı görüş adayı 4 → 0 | 3 nükte: yeni 2 (ikisi açık), taban 1 | Kör (o3): yeni bütün hafif, me'haz açık; **h3 yeni taban**; müfessir adı 64 → 8, Risale atfı 5 → 17, Arapça −%34 (`provalar/9-10/d13-rapor.md`) |
| D14.1 (2026-11-17) | h3 (5) ve h4 (6): Risale yerleri âyetin sözüne göre, Keşşâf dosyadan çıktı, dersi açma talimatı | 9–10 | 1 + 1 | tek okuyucu: %60, %74 | 3 nükte: taban 1, eşit 1, yeni 1 (kararsız) | Kör (o3): yeni bütün hafif, me'haz hafif; Zemahşerî'ye yaslanma gitti, Risale açılmıyor (h4'te yorumsuz alıntı); Keşşâf atfı 16 → 10; "altı cümle" yine (`provalar/9-10/d14-1-rapor.md`) |
| D14.2 (2026-11-17) | h4 (6) ve h5 (7): ders adayları programla, tek kaide (ders meseleyi doğuranın yanında), Ek 4 ders örnekleri | 9–10 | 1 + 1 | tek okuyucu: %74, %53 | 3 nükte: yeni 2, taban 1; "istediğimiz mânâda Risale dersi yok" | Kör (o3): bütün taban hafif, me'haz yeni hafif; Risale atfı 19 → 39, ders kısmen açılıyor; iki İşârât çelişkisi (`provalar/9-10/d14-2-rapor.md`) |
| D14.3 (2026-11-18) | h5 (7) ve h6 (8): program dört lafızda ders başlığı açar, dersin tarifi | 9–10 | 1 + 1 | tek okuyucu: %53, %60; kizb ve sıdk dersi 0 → 6/7 | 3 nükte: yeni 3, taban 0 ("gerçekten bravo") | Kör (o3): yeni bütün açık, me'haz açık; **h6 taban**; açılan ders 1 → 6 (`provalar/9-10/d14-3-rapor.md`) |
| D14.4 (2026-11-18) | h2 (1) ve h6 (2): D13 ve D14'ün bütün kazancı yeni birimde | 13 | 1 + 1 | tek okuyucu: %62, %74 | 3 nükte: h6 3, h2 0 | Kör (o3): h6 bütün açık, me'haz açık; yeni birimde doğrulandı; Risale atfı 2 → 31; h6 uzunluğu hedefi %13 aştı (`provalar/13/d14-4-rapor.md`) |
| D14.5a (2026-11-18) | h6 (2) ve h7 (3): uzunluk hedefi yalnız nazım kısmına, dersler dışında, ders sonu işareti | 13 | 1 + 1 | tek okuyucu: %74, %64 | 3 nükte: emin değil 2, h6 1 (kalite denk) | Kör (o3): h7 bütün hafif, me'haz hafif; toplam hedefe girdi (13.581 → 11.613) (`provalar/13/d14-5a-rapor.md`) |
| D14.6a (2026-11-18) | h7 (3) ve h8a (4): uzunluk hedefi yok | 13 | 1 + 1 | tek okuyucu: %64, %70 | 3 nükte: eşit 1, emin değil 2 (kalite denk; B'de paragraf düzeyinde uzatma) | Kör (o3): h7 hafif, me'haz h7 hafif; toplam aynı (11.506) (`provalar/13/d14-6-rapor.md`) |
| D14.6b (2026-11-18) | h7 (3) ve h8b (5): Risale yerleri konu başına ilk 10 | 13 | 1 + 1 | tek okuyucu: %64, %68 | Gerekmiyor | Kör (o3): h8b bütün hafif, me'haz eşit; maliyet −%11, dersler uzadı (`provalar/13/d14-6-rapor.md`) |

1. tur ayrıntıları: `data/d1/provalar/11-12/` (`rapor.md`, `d2-rapor.md`, `yz-karsilastirma.md`, `d9-rapor.md`,
`d6-rapor.md`). 1. turda D1 ile D2'nin farkı yalnız eserlerdi (klasik eserler kapsamayı artırmadı, dayanağı
güçlendirdi); tam istem ince istemden iyi değildi.

2. turun sonucu (kullanıcıyla, 2026-11-15): istem kuralı düşünme biçimini değiştirmiyor; yüzeyden denetlenebilen
biçim kuralları tutuyor. Döngünün kuralları (zincir, birimlerin harcanması, turda sabit ölçü) D11'in pilotunda da
geçerlidir; ölçüden karşılaştırma (D7) çıktı, envanter yalnız tek okuyuculu kalibrasyon için kaldı. Ayrıntı
`PLANLAR.md` › D8.6 ve D11.

## Birimler

| Birim | Tür | Durum |
|---|---|---|
| 11–12 | nazm ve lafız (nehiy, iddia ve red) | 1. turun birimi ve 2. turun ders birimi; yeniden yazılmaz |
| 9–10, 13 | nazm ve lafız | 1. turda eleştiride çok okundu: kör sınama için kullanılmaz |
| 17–20 | temsil (Kur'ân'ın meseli) | Âyetin tahlili 11–12'nin ≈6 katı (Arapçada ≈290 cümle, iki temsil); 2. tur için bırakıldı. 3. turda gerekirse tamamı gizlenir, yalnız 17–18 yazılır. Nazarî girişi (giriş, iki fasıl, 1–9. meseleler) genel usuldür, me'hazda kalır |
| 31–33 | kıssa ve mu'cize (başta mukaddime) | 2. turun yeni birimi; Arapça asıl 31. âyetin ortasında biter, Türkçede devamı var |
| 21, 22 | hüküm, emir | 3. tur için aday (D3'ün "hüküm" türü) |
| Öbürleri | | Kenarda; D5'e geçerken birkaçı kör sınama için ayrılmış kalır |
