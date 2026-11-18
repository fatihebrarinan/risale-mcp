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
- h4 (2026-11-17, D14.1 dosyanın düzeni; kullanıcının kararları): dosyada Risale-i Nur'un yerleri âyetin sözüne göre
  (söz → konu → paragraflar, en yakından başlayarak); Zemahşerî dosyadan çıktı, tefsirlerin başında eklentide ("önce
  Zemahşerî"); Risale-i Nur'un dersi Arapça metinde kendi sözüyle ve atıfla açılır, Türkçe tercümede gerekirse Türkçe
  aslından kısa blok alıntı. Yalnız "Me'haz" bölümünün 2–4. maddeleri değişti.
- h5 (2026-11-17, D14.2 ders adayları ve tek kaide; kullanıcının kararları): usulün 3. maddesi "Mukaddime" yerine "Ders
  ve mukaddime: tek kaide" (ders, meseleyi doğuran şeyin yanında; bütçe toplamda); dosyada lafızların altında programın
  seçtiği ders adayları; Ek 4: İşârât'tan ders örnekleri (sınanan birim dışındaki geliştirme birimlerinden).
- h6 (2026-11-18, D14.3 zorunlu ders başlıkları; kullanıcının kararları): program, ders adayı güçlü (en az 25 isabet)
  lafızlar için üçüncü vecihte `### Ders: «…»` başlığını açar, yazar altını doldurur; dersin tarifi (kullanıcının
  örneklerinden: lafızdan okuyucuya, umumî hakikat, müellifin biçimleri, kısa değil, Risale'deki dersin telhîsi); bütçenin
  üst kısmı derse kullanılabilir; Ek 4'e geniş ders örneği (31–33'ün mukaddimesi).
- h7 (2026-11-18, D14.5a; kullanıcının kararı: "uzunluğu kısacağız diye kaliteden kaybetmek istemiyorum"): uzunluk
  hedefi yalnız nazım kısmına (üç vechin tahlili); dersler hedefin dışında, meselenin genişliğine göre, îcâzla; her
  dersin sonunda `### Dersin sonu` işareti.
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
- **Uzunluk:** **nazım kısmının** (üç vechin tahlili; dersler hariç) Arapça paragraflarının toplamı **{en_az}–{en_cok}
  harf** (≈{kelime_az}–{kelime_cok} kelime). Bu, İşârât'ın bu boydaki bir biriminin nazım tahliline denktir. Dersler
  (usul 3) bu hedefin dışındadır. İşârât îcâzlıdır: bir nükte bir iki cümlede söylenir, gerekçesiyle.
  Kaynağın sözünü uzun nakletme; nükteyi kendi cümlenle söyle, kaynağın numarasını ver, gerekirse kısa bir ibaresini
  alıntıla. Az sayıda nükteyi gerekçesiyle söylemek, çok sayıda nükteyi gerekçesiz saymaktan iyidir. Tercüme ve
  kaynakça uzunluğa sayılmaz.

## Me'haz

Müellif İşârât'ı ve Risale-i Nur'u bu işe me'haz diye gösterdi. Me'hazın sırası budur; kaynak dosyası (Ek 3) da bu
sırayla dizildi:

1. **İşârâtü'l-İ'câz:** usul ve nazîr. Önceki birim dosyada; aynı türden öbür birimler `risale` eklentisinde
   (kimlikleri Ek 2'de). Usulün aslı Muhâkemât'tır (Ek 1, 2.7).
2. **Risale-i Nur:** mânâ ve ders. Dosyada âyetin her sözünün altında o sözün konusu ve Risale-i Nur'da işlendiği
   yerler var, en yakından başlayarak (program anlamsal aramayla buldu); devamı ve öbür yerler `risale` eklentisinde.
   Âyetin bir sözünü işlerken onun dersini oradan al ve **aç**: dersi, temsili, mizanı ve hükmü Arapça metinde kendi
   sözünle söyle ve Risale-i Nur'a atıf ver; Türkçe tercümede gerekirse Risale-i Nur'un Türkçe aslından kısa bir blok
   alıntı koy (numarasıyla). "Risale-i Nur'da da böyledir" deyip geçmek yetmez.
3. **Nazmın i'câzı:** belâgat ve lügat eserleri (Delâilü'l-İ'câz, Esrârü'l-Belâğa, Miftâhu'l-Ulûm, el-Müfredât,
   et-Ta'rîfât; dosyada âyetin geçtiği yerler, `klasik` eklentisi). Müellif nazmın i'câzını gösterirken bunların ve
   Zemahşerî'nin yöntemini izler.
4. **Klasik tefsirler** (`tefsir` eklentisi): dosyada yok. Bakacaksan **önce Zemahşerî'nin Keşşâf'ı**, sonra gerekirse
   öbürleri (Beyzâvî, Ebüssuûd, Âlûsî, Râzî…), ihtilafı ve yoklamayı görmek için. Taslağın sözü onlardan kurulmaz:
   akıl yürütmeyi onlara bırakma, nükteyi lafızdan, makamdan ve usulden (takdir zinciri, mukadder sual, "neden şu
   lafız, şu değil") kendin kur.
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
3. **Ders ve mukaddime: tek kaide.** İşârât'ta üç vechin olağan tahlili dışındaki her kısım bir meselenin dersidir ve
   **meseleyi doğuran şeyin yanında** verilir:
   - Mesele **bir lafızdan** doğuyorsa, o lafzın yerinde: çoğu kez üçüncü vecihte o lafız işlenirken, cümleler
     arasındaysa ikinci vecihte. Çoğu kez soru–cevap ("فإن قلت … قيل لك") ya da "… إشارة إلى" ile; gerekirse okuyucuya
     hitapla. Örnekleri Ek 4'te.
   - Mesele **âyetin bütün meâlinden** ya da bir iman rükününden doğuyorsa (dört maksattan biri, büyük bir kelâm
     ihtilafı, ilk kez toplu gelen bir üslûp türü), vecihlerden önce **mukaddime**; bir lafza bağlı büyük bir meseleyse
     vecihlerin arasında **mesele**.
   - **Ne zaman:** dosyada bir lafzın altında **ders adayı** varsa (Risale-i Nur o konuyu orada yoğun işliyor), o lafzı
     işlerken dur: münasebet güçlüyse dersi aç; zayıfsa kısa bir atıfla geç. Adayı güçlü lafızlar için program aşağıda
     (Şablon) **ders başlıklarını açtı**: bunların altını doldurmak zorunludur.
   - **Ders nedir:** lafızdan kalkar ve okuyucuya döner; lafzın nüktesinden insana, İslâm âlemine, beşere dair umumî bir
     hakikate geçer; müellifin biçimleriyle kurulur: temsil (bir nasihat sahnesi), soru–cevap (gerçek bir itiraz ve
     cevabı), silsile ("X, …dir; X, …dir" diye sıralanan hükümler ve sonunda "bu âyet … dikkate davet eder"), taksim
     ya da hitap. Kısa değildir: bir meseleyi gerekçesiyle açar. Bu derslerin genişi çoğu kez Risale-i Nur'dadır:
     müellif İşârât'ta dersi kendi öbür sözünden telhis eder. Senin işin de budur: Risale-i Nur'daki dersi bul,
     **telhis et**, âyetin lafzına bağla; Arapça metinde kendi sözünle, atıfla. Alıntı en çok dayanaktır; ders senin
     sözündür. "Risale-i Nur'da da böyledir" deyip geçmek ya da yorumsuz alıntı koymak ders değildir. Gerekirse öbür
     eserlerden.
   - **Ne kadar:** meselenin genişliğine göre. Dersler uzunluk hedefinin dışındadır: nazmın nüktelerini derse feda
     etme, dersi de nazım için kısma. Ama ders de îcâzlıdır: Risale-i Nur'un dersini telhis edersin, nakletmezsin;
     alıntı dayanaktır, dersin gövdesi değil.
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
   söylüyorsun, oysa lafızdan istinbat edilebilir mi? İnhisar kalıplarını kaynak mı söylüyor? Nazım kısmının Arapça
   uzunluğu hedefte mi (dersler hariç)?
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

- **Ders başlıkları** (program açtı; her birinin yeri yanında: çoğu üçüncü vecihte, o lafız işlenirken, lafzın
  nüktelerinden sonra; âyetin bütününe dair olanı mukaddimede; başlığı aynen yaz, altına dersi, Arapça paragraf ve
  tercümesiyle; dersin bitince ayrı satırda `### Dersin sonu` yaz, vechin devamı onun ardından başlıksız gelir):
{ders_basliklari}
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
