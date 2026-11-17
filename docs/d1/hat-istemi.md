<!--
D11 üretim hattının taslak istemi (PLANLAR.md D11). Sürümlüdür: her değişiklik aşağıdaki "Sürümler"e tarihiyle
yazılır. `scripts/d1-hat.py hazirla <birim>` bu dosyanın "İSTEM" çizgisinden sonrasını alır, {yer tutucuları} doldurur
ve sonuna ekleri koyar: kaynak dosyası (programın topladığı, `d1-hat.py dosya`), usul özetinin 4. ve 5. bölümleri ve
birim çizelgesinin Bakara tablosu (prova kopyaları: sınanan birimden alınan her şey çıkarılmış). Model istemi
`claude -p` ile, yerleşik araçlar ve web kapalı, prova sunucularıyla (risale, tefsir, hadis, klasik) alır.

D8'in istemlerinden (`prova-istemi.md` v1, `prova-istemi-v2.md` v2) farkı: usul özetinin tamamı ve İşârât'tan seçme
bölümler yerine kaynak dosyası ve usulün iki bölümü; Arapçada uzunluk hedefi; usul maddeleri v2'nin maddelerinin
kısaltılmışı (v2'nin tutan tırnak kuralı aynen). Araçla okuma kısıtlanmaz (kullanıcının kararı).

Sürümler:
- h1 (2026-11-15, D11 pilotu, 31–33).
- h2 (2026-11-16, D12.5 Tur 0; kullanıcının kararı): takdir işareti. Türkçede "…" yalnız kaynağın sözü, «…» takdir ve
  beklenen söz (D12.3: modelin hiç tırnak kullanamaması takdiri göstermeyi engelliyordu). Yalnız "Tırnak ve takdir"
  maddesi değişti. D12.5'in taban hattıdır.
- h3 (2026-11-17, D13 me'haz; kullanıcının kararları): me'haz hiyerarşisi. Kaynak dosyasının sırası İşârât, Risale-i
  Nur'un konuya dair yerleri (çok sayıda, anlamsal aramayla), Zemahşerî ve belâgat eserleri; öbür tefsirler dosyada
  yok, yalnız araçla. "Me'haz" bölümü yeniden yazıldı; "kendi tespiti" etiketinin yerine **istinbat** (lafızdan,
  hey'etten, makamdan ve usulden çıkan nükte; bir müfessirde de bulunması onu nakil yapmaz); Ek 1'e usulün 2.7'si
  (Muhâkemât). Görev, usul, uzunluk, şablon ve tırnak kuralları h2'nin aynısı.
-->

---- İSTEM ----

# Görev: İşârâtü'l-İ'câz usulüyle bir yapay zekâ taslağı ({sura_name} {ayahs})

Bediüzzaman Said Nursî İşârâtü'l-İ'câz'ı, ileride bir heyetin yapacağı tefsire örnek ve me'haz olsun diye yazdı.
Senden {sura_name} Sûresi {ayahs}. âyetler için İşârât'ın usulüyle bir **yapay zekâ taslağı** istiyoruz.

Bu bir provadır: İşârât'ın bu âyetlerdeki kısmı (Arapça aslı, Türkçe tercümesi, Osmanlıca baskısı) sana verilen
me'hazdan çıkarıldı; taslak sonra o gizlenen metinle yan yana okunacak. İşârât'ın bu âyetlerde ne dediğini
hatırlıyorsan ona dayanma ve ibarelerini yazma; usulü eklerden ve me'hazdan öğrenerek kendin tatbik et.

## Taslağın adı, dili ve uzunluğu

- Yazdığın şey "yapay zekâ taslağı"dır; hiçbir yerde "tefsir" deme. Ehlinin doğrulamasına sunulacaktır.
- Taslak **Arapça** yazılır. Her Arapça paragrafın hemen altında onun **Türkçe tercümesi** durur; her tercüme
  paragrafı "Yapay zekâ tercümesi:" diye başlar. Tercümenin dili Abdülmecid Nursî tercümesine yakındır: asla muvafık,
  terimleri koruyan, Osmanlı Türkçesi üslûbunda (örnekleri Ek 1'deki "Tercümede" alıntıları).
- **Uzunluk:** Arapça paragrafların toplamı **{en_az}–{en_cok} harf** (≈{kelime_az}–{kelime_cok} kelime). Bu,
  İşârât'ın bu boydaki bir birimine denktir. İşârât îcâzlıdır: bir nükte bir iki cümlede söylenir, gerekçesiyle.
  Kaynağın sözünü uzun nakletme; nükteyi kendi cümlenle söyle, kaynağın numarasını ver, gerekirse kısa bir ibaresini
  alıntıla. Az sayıda nükteyi gerekçesiyle söylemek, çok sayıda nükteyi gerekçesiz saymaktan iyidir. Tercüme ve
  kaynakça uzunluğa sayılmaz.

## Me'haz

Müellif İşârât'ı ve Risale-i Nur'u bu işe me'haz diye gösterdi. Me'hazın sırası budur; kaynak dosyası (Ek 3) da bu
sırayla dizildi:

1. **İşârâtü'l-İ'câz:** usul ve nazîr. Önceki birim dosyada; aynı türden öbür birimler `risale` eklentisinde
   (kimlikleri Ek 2'de). Usulün aslı Muhâkemât'tır (Ek 1, 2.7).
2. **Risale-i Nur:** mânâ ve ders. Dosyada bu âyetlerin konularına dair çok sayıda yer var (program anlamsal aramayla
   buldu); devamı ve öbür yerler `risale` eklentisinde. Âyetin söylediği şeyi Risale-i Nur nerede, nasıl işliyorsa
   oradan konuş: ders, temsil, mizan ve hükmü oradan al, Risale-i Nur'un sözünü adıyla ve kaynağıyla an.
3. **Nazmın i'câzı:** Zemahşerî'nin Keşşâf'ı (bu âyetlerdeki birimi dosyada tam) ve belâgat ve lügat eserleri
   (Delâilü'l-İ'câz, Esrârü'l-Belâğa, Miftâhu'l-Ulûm, el-Müfredât, et-Ta'rîfât; `klasik` eklentisi). Müellif nazmın
   i'câzını gösterirken bunların yöntemini izler.
4. **Klasik tefsirler** (Beyzâvî, Ebüssuûd, Âlûsî, Râzî ve öbürleri; `tefsir` eklentisi): dosyada yok. İhtilafı ve
   yoklamayı görmek için gerektikçe oku. Taslağın sözü onlardan kurulmaz.
- `hadis` eklentisi: hadis kitapları. Âyeti ve alıntılarını eklentinin verdiği gibi, harf harf aynı yaz.

**Nakil ve istinbat.** İşârât'ta nükteler büyük çoğunlukla müellifin istinbatıdır; cümlelerinin %1,3'ünde bir kaynak
adı geçer, o da çoğu zaman "قيل" ile. Taslak da böyle yazılır:
- **İstinbat:** âyetin lafzından, hey'etinden, makamından ve usulden senin vardığın nükte. Bir müfessirde de bulunması
  onu nakil yapmaz; etiketi "nereden vardım"ı söyler, yenilik iddia etmez. Gerekçesi lafza bağlıdır; derecesi
  (sarih, işaret, remiz, îmâ) ve ihtimali söylenir.
- **Nakil:** bir kaynağa mal ettiğin söz. Risale-i Nur ve İşârât adıyla anılır. Bir müfessir yalnız onun kendine has
  bir sözünü (bir görüşünü, bir vechini) alıyorsan adıyla anılır; ihtilafı göstermek için çoğu zaman "قيل" ya da
  "وقيل" yeter. Bir müfessirin sözünü İşârât'a ya da müellife mal etme. Bir kaynağa onun kendi görüşü olmayanı
  (naklettiği, itiraz ettiği ya da reddettiği vechi) mal etme.

Kaynağı aklındaki nükteyi doğrulamak için değil, ne dediğini görmek için oku; aradığın cümlenin yanındaki soru,
cevap ve çekince cümleleri çoğu zaman asıl nükteyi taşır. Kaynaktan hükmü değil, oraya nasıl varıldığını al; ihtimal
ve çekince sözlerini ("قد", "يحتمل", "قيل") düşürme. Risale-i Nur'da bir yer bu âyeti ya da konusunu işliyorsa o
bölümün ana tezini gör; mesele orada işlenmişse yeniden kurma, atıfla hülâsa et. Bir belâgat terimini kullanmadan önce
tanımını terim eserinde gör; uymuyorsa kullanma.

## Usul (Ek 1 ve Ek 2'nin özü)

1. **Düzen:** âyet; gerekiyorsa mukaddime; **birinci vecih** (öncesiyle nazım); **ikinci vecih** (cümlelerin
   birbiriyle nazmı); **üçüncü vecih** (her cümlenin hey'etleri, kayıtları ve kelimeleri). Her vecih İşârât'taki gibi
   kendi geçiş cümlesiyle açılır.
2. **Dört maksat:** asıl maksat her zaman söylenir; tevhid, nübüvvet, haşir ve adaletten öbürleri yalnız bu âyete
   özgü bir lafza ya da hey'ete dayanıyorsa ve derecesiyle (sarih, işaret, remiz, îmâ, telvih). Tutamak yoksa anma.
3. **Mukaddime** yalnız şu durumlarda: âyetin meâli dört maksattan ya da iman rükünlerinden biridir; altında büyük
   bir kelâm ihtilafı vardır; bir üslûp türü ilk kez toplu gelir; bir lafız tahkik ister. Kısa tutulur; Risale-i Nur'da
   ya da İşârât'ta işlenmişse oraya atıfla hülâsa edilir.
4. **Kabul ölçüsü:** Arap dili ilimlerinin reddetmediği, belâgatin güzel bulduğu, şeriatin maksatlarına uygun;
   delâlet derecesi Arapçada söylenir ve gerekçesi bellidir. Gerekçesini gösteremediğin nükteyi ihtimal diliyle söyle
   ya da bırak.
5. **İkinci vecih: söylenmeyeni bul.** Âyetin üslûbu beklenenden ayrılıyorsa (cümle türü, emirden habere, gâibden
   muhataba geçiş; beklenen bir atfın ya da cevabın gelmemesi) altında takdir edilmiş bir cümle zinciri vardır: zinciri
   aç, her halkayı yaz. Dinleyenin zihnindeki soruyu ve makamın neyi iktiza ettiğini birlikte kullan.
6. **Üçüncü vecih:** bakılacak yerleri önce say (harfler dahil); "neden şu lafız, şu değil" diye sor; mukadder
   cümleleri aç; her kaydın mânâya ne kattığını ve muhatabın vicdanında ne iş gördüğünü söyle; sonunda kayıtların asıl
   garaza nasıl aktığını topla.
7. **Müfessirler ayrıldığında** birini seçme, "hepsi olabilir" deyip de geçme; her görüşün hangi itibarla doğru
   olduğunu sor.
8. **Kapsam:** kendi tespitini vecihlerden biri olarak yaz ("… olabilir"). İnhisar ve mutlaklık kalıplarını ("ancak",
   "daima", "X değil Y'dir") ancak kaynak öyle diyorsa kullan; ara halkaları atlayıp ilişkiyi mahiyet hükmüne çevirme.

## Çalışma sırası

1. Ek 1'i, Ek 2'yi ve Ek 3'ü (kaynak dosyası) oku; Risale-i Nur'un yerlerini (Ek 3'ün 2. bölümü) baştan sona.
2. İşârât'ın aynı türden bir iki birimini `risale` eklentisinde `read_section` ile oku (kimlikleri Ek 2'de); bir
   edatın ya da üslûbun kaidesine dayanacaksan onu İşârât'ın kendisinde ara (`search`, `semantic_search`,
   `work: "isaratul-icaz-arabi"`). Risale-i Nur'da bir yerin devamını ya da dosyada olmayan bir konuyu gerekirse
   oku; bir müfessiri ihtilafı görmek için gerekirse aç.
3. Yazmadan önce kendin için çıkar: âyetin cümleleri, asıl maksadı, öncesiyle bağı, Risale-i Nur'un bu âyetlerin
   konusunda verdiği ders, mukaddime gerekip gerekmediği, üslûbun beklenenden ayrıldığı yerler, müfessirlerin
   ayrıldığı yerler.
4. Taslağı yaz (şablon aşağıda), uzunluk hedefine uyarak.
5. Öz denetim: tırnak içindeki her söz araçların döndürdüğü metin mi? Bir kaynağa mal ettiğin söz o kaynağın kendi
   görüşü mü (naklettiği, itiraz ettiği ya da reddettiği vecih değil mi)? Nükteyi bir müfessirin adıyla mı
   söylüyorsun, oysa lafızdan istinbat edilebilir mi? İnhisar kalıplarını kaynak mı söylüyor? Arapça uzunluk
   hedefte mi?
6. Her eklentinin `cite` aracını, dayandığın ve alıntıladığın her cümle ya da aralıkla bir kez çağır; işaret ettiği
   sorunları düzelt. Tek "Kaynaklar" listesi ver (eklentiler sırayla: `first` ile numara sürer).

## Şablon

Cevabın yalnız taslaktır; önüne ve ardına açıklama yazma. Biçim:

```
# Yapay zekâ taslağı: {sura_name} {ayahs}
> Bu bir yapay zekâ taslağıdır, tefsir değildir. İşârâtü'l-İ'câz'ın usulüyle, ehlinin incelemesi için yazıldı.

## Âyet
> (âyetin metni, get_ayah'tan) [n]

## Mukaddime            ← yalnız usul 3'teki durumlardan biri varsa; yoksa bu başlık hiç olmaz
## Birinci vecih
## İkinci vecih
## Üçüncü vecih

(her başlığın altında: Arapça paragraf, altında "Yapay zekâ tercümesi: …" paragrafı; sırayla)

## Kaynaklar
```

- Bir kaynaktan alıntı ancak eklentinin ya da dosyanın verdiği metinle, ayrı satırda blok alıntı olarak ve
  numarasıyla [n] verilir; alıntıların tercümesi de "Yapay zekâ tercümesi:" damgalıdır.
- **İşaretler** (yalnız Türkçe tercüme paragraflarında, iddianın hemen ardından): `[dil]` sarf, nahiv, lügat;
  `[belâgat]` meânî, beyân, bedî'; nakilse numarası (`[belâgat; 3]`); istinbatsa `[belâgat; istinbat]`
  (yukarıdaki "Nakil ve istinbat"); nazîrden taşıyıp buraya uyguladığın nükte `[belâgat; 7, buraya tatbiki istinbat]`.
  Tercüme Arapçada olmayan cümle eklemez.
- **Tırnak ve takdir: iki ayrı işaret.** Türkçe tercümede:
  - "…" (ya da “…”) **yalnız kaynağın sözü** içindir: araçların ya da dosyanın döndürdüğü metin, harfi harfine.
    Bir kaynağı mealen aktarıyorsan tırnak kullanma.
  - «…» **takdir ve beklenen söz** içindir: dinleyenin zihnindeki mukadder soru, takdir edilen cümle, makamın
    beklediği ama âyetin söylemediği ifade. Ör. sanki «Peki bunun sebebi nedir?» denildi; burada «…» beklenirdi,
    âyet onun yerine … dedi. «…» içindeki söz senindir: yanına kaynak numarası konmaz; kaynağın sözünü «…» içine
    koyma.
  - Arapçada takdir kalıbıyla sunulur ("كأنه قيل", "فإن قلت", "أي"); tırnak (« » ya da " ") yalnız kaynağın
    sözündedir.
- Âyet atıfları `get_ayah`'ın verdiği biçimdedir; cümle numarası ya da kimlik yazma, kaynakça numarası yeter.
