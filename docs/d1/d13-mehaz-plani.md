# D13. Me'haz: taslak İşârât ve Risale-i Nur'dan konuşsun (plan, 2026-11-17)

Kullanıcının değerlendirmesi ve kararları (2026-11-17, D12.5'in T1 ve D turlarından sonra). D12.5'ten ayrı bir aşamadır,
çünkü bir istem ya da adım değişikliği değil, **taslağın neye dayandığının** değişmesidir. Kullanıcı: "Şu ana kadar
yaptığımız taslak denemelerinden en büyük gelişme bu sefer olacak"; "yapı zaten en başından beri böyle olmalıydı,
ama gözden kaçırmışız."

## 1. Sorun

Me'hazımız İşârât ve Risale-i Nur'dur; taslaklar ise müfessirlerden konuşuyor.

| Taslak | Müfessir adı (Arapça metinde: Ebüssuûd, Âlûsî, Keşşâf, Râzî, Beyzâvî) | İşârât | Muhâkemât | Risale'nin öbür eserleri |
|---|---:|---:|---:|---:|
| 9–10 taslak 1 (h2, taban) | 49 | 17 | 1 | 0 |
| 9–10 taslak 3 (d1 düzeltmesi) | 75 | 23 | 1 | 0 |
| 31–33 taslak 7 ve 8 | atıfların %75'i müfessir | | | Sözler 7–9 atıf |

- İşârât'ın 9–10'daki son yedi nüktesi (N41–N47: kizbin tahribatı, maslahat için kizb, ta'riz ve kinâye, sükût, sıdkın
  îmanın hassası olması) **dört taslağın hiçbirinde yok**. Risale-i Nur'un en çok işlediği ders budur.
- İşârât'ın 3.264 cümlesinin 43'ünde (%1,3) bir kaynak adı geçer (D12.4); taslaklar müfessiri adıyla, bir taslakta
  Ebüssuûd'u 15 yerde anıyor.

**Sebep bizim yapımızdadır:**
1. **Kaynak dosyası** (`d1-hat.py dosya`; 9–10'da ≈11.800 kelime): önce dört müfessirin (Zemahşerî, Beyzâvî,
   Ebüssuûd, Âlûsî) bu âyetlerdeki birimleri **tam metin**, sonra İşârât'ın önceki birimi, sonra Risale-i Nur'dan
   yalnız **âyetin geçtiği yerler** (9–10'da tek yer: Muhâkemât'tan bir cümle), sonra klasik eserler. Risale-i Nur
   âyetleri değil konuları işler (nifak, kizb, kalb hastalığı); âyete göre arayınca bulunmaz. Yazar elinde ne varsa
   onu yazıyor.
2. **Kaynak kuralı:** "kendi tespiti yalnız okuduğun hiçbir kaynakta bulunmayan söz içindir": lafızdan çıkan her nükte
   bir müfessire bağlanıyor. Eleştirmen de "bu kendi tespitin değil, Ebüssuûd'da var" diye yazıyor (profilde 9 not);
   düzeltme müfessir adını ≈%50 artırıyor. Kaynaktan caydıran kuralın olumsuz yüzü.
3. **Muhâkemât (usul 2.7) yazara gitmiyor:** yazarın isteminde usul özetinin yalnız 4. ve 5. bölümleri var; 2.7
   yalnız eleştirmende.
4. **Ölçüler bunu görmüyor:** kör eleştirmen İşârât'a yakınlığı, envanter nükte sayısını ölçüyor; "me'hazı doğru mu,
   Risale-i Nur'un çizgisinde mi" sorulmuyor. Profilin en ağır kusuru (yanlış nisbet, yüksek notların 6/9'u) da
   müfessirden nakil çokluğunun bir belirtisidir.

## 2. Değişiklik: me'haz hiyerarşisi (kullanıcının kararları)

Bir bütün olarak tek değişiklik sayılır (dosya, istemin me'haz bölümü ve kaynak kuralı birlikte); kazanırsa
gerekirse parçalarına ayrılarak bakılır.

### 2.1 Kaynak dosyasının sırası ve içeriği

1. **İşârâtü'l-İ'câz:** önceki birim (bugünkü gibi) ve aynı türden birimler araçla; **usul özeti 2.7 (Muhâkemât)
   yazara da gider** (4. ve 5. bölümlerin yanında).
2. **Risale-i Nur'un konuya dair yerleri, çok sayıda** (kullanıcı: "sadece birkaç yer gelmesin; anlamsal aramada
   bulunan çok yer gelsin, sonuçların yarısı falan"):
   - **Konular:** kısa bir model adımı âyetler ve meali okuyup 6–8 konu yazar (günümüz Türkçesiyle ve Risale'nin
     terimleriyle; 9–10 için beklenen: nifak, kizb ve sıdk, hile ve aldatma, kalb hastalığı, hissetmemek ve şuursuzluk,
     elem ve azab). İşârât'ı görmez; liste kaydedilir.
   - **Arama:** her konu için anlamsal arama (Voyage, cümle vektörleri) **ilk 100 sonucu**; benzerliğe göre **üst
     yarısı (50 cümle)** alınır; her cümle paragrafıyla ve bölüm yoluyla gelir; aynı paragraf bir kez. Kapsam Risale-i
     Nur külliyatı (Muhâkemât dahil, Osmanlıca hariç); İşârât'ın kendisi bu bölüme girmez (1. bölümde ve araçla), sınanan
     birim hiçbir yerde yoktur. Âyetin geçtiği yerler de (bugünkü bölüm) buraya katılır.
   - Tahmin: 6–8 konu × 50 cümle, tekrarlar düşünce ≈150–250 paragraf, ≈25–45 bin kelime (bugünkü dosyanın 2–4 katı).
     Kesin sayı 2.4'teki durakta gösterilir.
3. **Nazımdaki i'câzı gösteren eserler** (kullanıcı: "Üstad üstü kapalı olarak bizdeki belâgat eserleri ve
   Zemahşerî'nin yöntemini izliyor"): **Zemahşerî'nin Keşşâf'ı** (bu âyetlerdeki birimi tam) ve **belâgat ve lügat
   eserleri** (Delâilü'l-İ'câz, Esrârü'l-Belâğa, Miftâhu'l-Ulûm, el-Müfredât, et-Ta'rîfât; bugünkü gibi âyetin geçtiği
   yerler).
4. **Klasik tefsirler** (Beyzâvî, Ebüssuûd, Âlûsî, Râzî ve öbürleri): **dosyada yok**, yalnız `tefsir` eklentisiyle
   açılır (kullanıcının kararı).

### 2.2 Yazarın istemi (h3 = h2 + me'haz bölümü)

- **Me'haz bölümü** yeni sırayı ve her katmanın işini söyler: usul ve nazîr İşârât'tan; mânâ ve ders Risale-i
  Nur'dan; nazmın i'câzı Keşşâf'tan ve belâgat eserlerinden; müfessirler ihtilafı ve yoklamayı görmek için.
- **Nakil ve istinbat** (D12'nin kalıcı dersi 3; T2'nin özü buraya katılır): nükte âyetin lafzından, hey'etinden,
  makamından ve usulden çıkıyorsa **istinbattır** ve öyle etiketlenir; bir müfessirde de bulunması onu nakil yapmaz
  (etiket "nereden vardım"ı söyler, yenilik iddia etmez). Bir müfessir yalnız onun kendine has bir sözü alındığında
  adıyla anılır; çoğu zaman İşârât gibi "قيل" yeter. Risale-i Nur'un sözü ise adıyla ve kaynağıyla anılır: me'hazdır.
- Görev, usul, uzunluk, şablon ve tırnak kuralları h2'nin aynısıdır.

### 2.3 Ölçü

- **Kör eleştirmen o3** = o2 + bir soru (kullanıcının kararı): "Taslak me'hazını doğru kullanıyor mu: İşârât'ın usulü
  ve Risale-i Nur'un çizgisinde mi, Risale-i Nur'un ilgili dersine dayanıyor mu, müfessirlerden mi konuşuyor?" İki kola
  birden uygulanır; eski turların o2 sayılarıyla doğrudan karşılaştırılmaz.
- **Yeni mekanik sayı (me'haz dağılımı):** Arapça metinde müfessir adı, İşârât ve Risale-i Nur adı; kaynakça
  atıflarının eser dağılımı (İşârât, Risale'nin öbür eserleri, Keşşâf, belâgat, öbür tefsirler); Risale-i Nur'a
  dayanan paragraf sayısı.
- **Envanter** (tek okuyucu, ayar): kapsama, özellikle N41–N47.
- D9.1 (nisbet, tırnak, kendi tespiti) ve uzunluk bugünkü gibi.

### 2.4 Kollar ve okuma

- **Taban:** taslak 1 (h2; yazılı ve ölçülü, yeniden yazılmaz; yalnız o3 ile yeniden ölçülür).
- **Yeni:** taslak 5 (h3 ve yeni dosya), aynı birim 9–10, aynı yazar (Opus 5.5, yüksek), aynı prova sunucuları.
- **Okuma** standartla (plan belgesi 4.10): 3 nükte, yan başına en çok 2 paragraf ve ≈250 kelime, Türkçe önde,
  İşârât'ın sözü "Aç"tan sonra, sarı fark yok (iki ayrı yazım). Yerlerden biri, yeni kol işlemişse N41–N47'den.
- **Karar** 4.4'ün kuralıyla; kör eleştirmen ve siz.

## 3. Adımlar

| Adım | İş | Kim | Durak |
|---|---|---|---|
| D13.1 | Bu plan | Claude | **Onayınız** |
| D13.2 | Dosyanın yeni kuruluşu: konu adımı, Risale-i Nur anlamsal derlemesi (konu × ilk 100 → üst yarı), Keşşâf ve belâgat; sızıntı testi (Risale-i Nur'da müellifin bu birimdeki sözünü başka eserde tekrarladığı yerler kabul edilir: asıl işte de me'hazdır, 9–10'un Hutbe-i Şâmiye düsturu gibi) | Claude | **Kısa durak:** konu listesi ve dosyanın sayıları (paragraf, kelime, eser dağılımı); "yarısı" fazla ya da az ise burada ayarlanır |
| D13.3 | Yazarın istemi h3 (me'haz bölümü, nakil–istinbat etiketi, usul 2.7), sızıntı testi | Claude | |
| D13.4 | Kör eleştirmen o3 ve me'haz dağılımı sayısı | Claude | |
| D13.5 | Yeni kol: taslak 5 | Claude | |
| D13.6 | Ölçüm: 1 ile 5 (o3, envanter, D9.1, me'haz dağılımı, uzunluk, maliyet); tur raporu `provalar/9-10/d13-rapor.md` | Claude | |
| D13.7 | Okuma (standart, 3 nükte) | siz | ≈15 dk |
| D13.8 | Karar; kazanırsa yeni taban (h3 ve yeni dosya) | birlikte | |

**Maliyet tahmini:** konu adımı ≈0,3 $; taslak 5 ≈6–9 $ (dosya büyüdüğü için tabandan pahalı olabilir); eşleştirme ≈2 $;
kör ölçü ≈2 $: **≈11–14 $**. Anlamsal arama sorguları birkaç kuruş.

## 4. Sonrası (D13 kazanırsa)

- **Düzeltme eleştirmeni (k3)** aynı me'haz anlayışına çekilir: "kaynakta var, adını ver" notları kalkar; yalnız
  gerçek nisbet hatası (kaynağın söylemediği, itirazın parçası ya da reddettiği vecih) işaretlenir; Risale-i Nur'un
  ilgili dersine dayanmayan yer sorulur. Düzeltme (d1) hatta kalır; **d2 bırakıldı** (kullanıcı, 2026-11-17: kazancı d1'in
  çok azı, birim başına ≈5 $).
- D12.5'in kalan turları (garaz T3, takdir zinciri T4, belgeler yazımda T5) yeni tabanla yeniden değerlendirilir; T2
  (nakil–istinbat) D13'e katıldı.
- Sonra D12.6 (saklı birimlerde son ölçüm) ve D5.

## 5. Nerede duruyoruz (2026-11-17)

- **D12.1–D12.4 bitti.**
- **D12.5:** Tur 0 bitti; **T1 bitti** (okuma ve yazım ayrı: yeni kol taban olmadı, sizin hükmünüz); **D turu bitti**
  (d1 hatta kalır, d2 bırakıldı); T2 D13'e katıldı; T3–T5 D13'ten sonra yeniden değerlendirilir. Taban: h2.
- **Şimdi: D13** (bu plan; onay bekliyor).
