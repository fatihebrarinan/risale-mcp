<!--
D1 provasının istemi, ikinci sürüm (PLANLAR.md D8, döngünün 2. turu; `docs/d1/dongu.md`). v1 `prova-istemi.md`'de
değişmeden durur: D8'de ayrılmış birimde eski ve yeni istem yan yana çalışır (`d1-prova.py --surum v1|v2`).

Asıl açıklama (v1'den):
D1 provasının istemi (PLANLAR.md D1.3). Sürümlüdür: her değişiklik aşağıdaki "Sürümler"e tarihiyle yazılır,
düzeltmeler yalnız genel usule yapılır, âyete özgü ipucu girmez. `scripts/d1-prova.py hazirla <birim>` bu dosyanın
"İSTEM" çizgisinden sonrasını alır, {yer tutucuları} doldurur ve sonuna ekleri koyar: usul özetinin ve birim
çizelgesinin prova kopyaları (sınanan birimden alınan her şey çıkarılmış) ve İşârât'ın Arapça aslı (sınanan birim
hariç). Model bu istemi `claude -p` ile, yerleşik araçlar ve web kapalı, yalnız prova sunucularıyla alır.

İki biçim (`hazirla <birim> --istem tam|ince`): `tam` Ek 3'te Arapça aslın tamamını verir (≈472 bin token), `ince`
yalnız birimin komşularını ve Bakara 17–20'nin nazarî girişini verir, kalanını eklentiden okutur (≈1/4'ü). `@tam `
ya da `@ince ` ile başlayan satır yalnız o biçimde kalır (önek atılır); öbür satırlar ikisinde de aynıdır. `ince-klasik`
biçimi `@ince ` ve `@klasik ` satırlarını alır (D2).

Sürümler:
- v1 (2026-11-11): ilk sürüm; 11–12 için.
- v1-ince (2026-11-12): v1'in ince biçimi; usul aynı, yalnız Ek 3'ün kapsamı ve İşârât'ın kalanına nasıl
  bakılacağı değişti. Neden: tam istem bir taslakta 5 saatlik limitin tamamını harcıyordu; ince taslak tam taslakla
  karşılaştırılarak tam metnin katkısı ölçülecek.
- v1-ince-klasik (2026-11-13, D2): v1-ince'nin aynısı; yalnız me'haz listesine `klasik` eklentisinin satırı eklendi
  (`@klasik ` önekli satırlar yalnız bu biçimde kalır). Usule dokunulmadı: D2'nin şartı D1 ile aynı olmaktır, değişen
  yalnız eserlerdir (kullanıcının kararı, 2026-11-13).
- **v2 (2026-11-14, D8):** 1. turun dersleri genel usul olarak (âyete özgü ipucu yok; örnekler yalnız İşârât'ın açık
  kısmından ve genel kalıplardan, sınanan birimin gizlenen nüktelerinden değil). Kaynaklar: `d9-rapor.md` "D8'e
  geçenler" (Z1–Z9, kapsam, dört maksat, terim), `d6-rapor.md` (kapsam ve derece), `d2-rapor.md` (klasik eserlere
  dayanış), D7 (aynı nokta, başka yol). Değişenler: usulde ikinci vecih (üslûp değişikliği, takdir zinciri, halkalı
  temsil), üçüncü vecih (kaydın vicdandaki işi, dava ve red kayıtlarının eşlenmesi), ihtilaf, kaynak okuma, dört
  maksadın tutamağı, kapsam ve derece, delâlet derecesinin gerekçesi; çalışma sırasına yazmadan önce iki soru ve
  yazdıktan sonra öz denetim; işaretlerde "kendi tespiti", tırnak ve takdir kuralları.
-->

---- İSTEM ----

# Görev: İşârâtü'l-İ'câz usulüyle bir yapay zekâ taslağı ({sura_name} {ayahs})

Bediüzzaman Said Nursî İşârâtü'l-İ'câz'ı, ileride bir heyetin yapacağı tefsire örnek ve me'haz olsun diye yazdı. Bu
çalışma o usulün bir yapay zekâ tarafından tatbik edilip edilemeyeceğini sınayan bir **provadır**. Senden
{sura_name} Sûresi {ayahs}. âyetler için İşârât'ın usulüyle bir **yapay zekâ taslağı** istiyoruz.

Bu bir provadır: İşârât'ın bu âyetlerdeki kısmı (Arapça aslı, Türkçe tercümesi ve Osmanlıca baskısı) sana verilen
me'hazdan çıkarıldı. Taslağın sonra o gizlenen metinle yan yana okunacak ve ehlince değerlendirilecek. Amaç usulün
tatbikini görmektir. İşârât'ın bu âyetlerde ne dediğini hatırlıyorsan ona dayanma ve ibarelerini yazma; usulü,
aşağıdaki eklerden ve me'hazdan öğrenerek kendin tatbik et.

## Taslağın adı ve sınırı

- Yazdığın şey "yapay zekâ taslağı"dır; hiçbir yerde "tefsir" deme. Ehlinin doğrulamasına, eklemesine ve
  çıkarmasına sunulacaktır.
- Taslak **Arapça** yazılır. Her Arapça paragrafın hemen altında onun **Türkçe tercümesi** durur (iki ayrı taslak
  değil: tercüme Arapçadan, paragraf paragraf). Her tercüme paragrafı "Yapay zekâ tercümesi:" diye başlar.
- Türkçe tercümenin dili Abdülmecid Nursî tercümesinin diline yakın olur: Arapça asla muvafık, terimleri koruyan,
  Osmanlı Türkçesi üslûbunda. Örnekleri usul özetinde Arapça cümlelerin altındaki "Tercümede" alıntılarıdır;
  Türkçe tercümeyi `risale` eklentisinde de okuyabilirsin.
- Arapçanın üslûbu İşârât gibi **îcâzlı**dır. Uzunluk için İşârât'ın benzer birimlerini (ör. {olcu}) ölçü al.

## Me'haz

@tam - İşârâtü'l-İ'câz: Arapça aslı bu istemin sonunda (Ek 3) cümle kimlikleriyle; Türkçe tercümesi ve Risale-i Nur'un
@tam   bütün eserleri `risale` eklentisinde.
@ince - İşârâtü'l-İ'câz: Arapça aslının bu âyetlere komşu birimleri ve Bakara 17–20'nin nazarî girişi bu istemin
@ince   sonunda (Ek 3) cümle kimlikleriyle; Arapça aslının tamamı, Türkçe tercümesi ve Risale-i Nur'un bütün eserleri
@ince   `risale` eklentisinde.
- Müfessirlerin eserleri (Taberî, Mâtürîdî, Zemahşerî, Râzî, Kurtubî, Beyzâvî, Nesefî, İbn Kesîr, Celâleyn,
  Süyûtî, Ebüssuûd, Bursevî, Âlûsî): `tefsir` eklentisinde.
- Hadis kitapları: `hadis` eklentisinde.
@klasik - Belâgat, dil ve terim eserleri (Abdülkāhir el-Cürcânî'nin Delâilü'l-İ'câz'ı ve Esrârü'l-Belâğa'sı, Sekkâkî'nin
@klasik   Miftâhu'l-Ulûm'u, Râgıb el-İsfahânî'nin el-Müfredât'ı, Seyyid Şerîf el-Cürcânî'nin et-Ta'rîfât'ı): `klasik`
@klasik   eklentisinde.
- Âyetin metni: `get_ayah`. Âyeti ve kendi alıntılarını eklentinin verdiği gibi, harf harf aynı yaz.

Her iddia bir kaynağa, her nükte âyetin bir lafzına ya da hey'etine bağlanır. Bir nükteyi bir müfessirden
alıyorsan onu an ve kaynağını göster; kendi tespitinse öyle işaretle (aşağıda). Bir müfessirin sözünü İşârât'a ya
da müellife mal etme.

**Kaynağı nasıl okursun:**
- Bir kaynağı, aklındaki nükteyi doğrulamak için değil, **ne dediğini görmek için** oku. Arama sonucundaki cümleyle
  yetinme: `get_passage` ile bağlamını, nazîr bir bölümse bölümün tamamını oku; aradığın cümlenin hemen yanındaki soru,
  cevap ve ipucu cümleleri çoğu zaman asıl nükteyi taşır.
- İşârât'ın nazîr bir âyetteki bahsinden ya da bir müfessirden **hükmü değil, oraya nasıl varıldığını** al. Aynı
  yerde bir hüküm ve onun mekanizması varsa ikisini birlikte taşı.
- Bir kaynağın sözünü kayıtlarıyla aktar: ihtimal ve çekince sözlerini ("قد", "من معاني", "يحتمل", "قيل") düşürme;
  aynı yerdeki aykırı hükmü ya da müellifin hemen ardından gelen çekincesini de göster. Kaynağın gerekçesini kendi
  gerekçenle karıştırma: kaynak bir nükteyi başka bir sebebe dayandırıyorsa öyle aktar.
@klasik - Bir nüktenin aslı belâgat eserlerindeyse önce ona dayan; müfessir de naklediyorsa ikisini ayrı an. Kaideyi
@klasik   kaynağa, âyete tatbikini "kendi tespiti"ne bağla. Bir belâgat terimini (bir bedî' sanatı, bir kasr türü)
@klasik   kullanmadan önce tanımını terim eserinde (Miftâhu'l-Ulûm, et-Ta'rîfât) oku; tanım âyetteki duruma uymuyorsa
@klasik   o terimi kullanma.

## Usul (Ek 1 ve Ek 2'nin özü)

1. **Düzen:** Bakara 9'dan sonraki sabit düzen: âyet; gerekiyorsa mukaddime; **birinci vecih** (âyetin öncesiyle
   nazmı); **ikinci vecih** (âyetin cümlelerinin birbiriyle nazmı); **üçüncü vecih** (her cümlenin hey'etleri,
   kayıtları ve kelimeleri). Her vecih İşârât'taki gibi kendi geçiş cümlesiyle açılır.
2. **Dört maksat:** âyetin asıl maksadı her zaman söylenir. Tevhid, nübüvvet, haşir ve adalet maksatlarından öbürleri
   yalnız âyetin bir lafzına ya da hey'etine dayandırılabiliyorsa ve derecesiyle (sarih, işaret, remiz, îmâ, telvih)
   söylenir; dördü her âyette zorla gösterilmez. Tutamak **bu âyete özgü** olmalıdır: hemen her âyete uyan bir
   gerekçe ("gizli bir hâlden haber vermek vahye işarettir", "bir mef'ûlün hazfi" gibi) tutamak sayılmaz. Tutamak
   yoksa o maksadı hiç anma; "kalan maksatlar için tekellüf edilmez" demen yeter.
3. **Mukaddime** yalnız şu dört durumdan biri varsa yazılır: âyetin meâli dört maksattan ya da iman rükünlerinden
   biridir; âyetin altında büyük bir kelâm ihtilafı vardır; bir üslûp türü ilk kez toplu gelir ve nazarî temel
   ister; bir lafız tahkik ister. Kısa tutulur, her iddiası âyetin bir lafzına bağlanır; mesele İşârât'ta ya da
   Risale-i Nur'da işlenmişse yeniden kurulmaz, oraya atıfla hülâsa edilir. Bu durumlardan biri yoksa mukaddime
   yazılmaz.
4. **Kabul ölçüsü:** bir nükte Arap dili ilimlerinin reddetmediği, belâgatin güzel bulduğu, şeriatin maksatlarına
   uygun bir nükte olmalı; hayal bir hakikat çekirdeğine dayanmalı. Nüktenin delâlet derecesi Arapçada söylenir ve
   **gerekçesi bellidir** (hangi lafız, hangi hey'et); derece kalıbı her paragrafın sonuna alışkanlıkla eklenmez.
   Gerekçesini gösteremediğin derece, nüktenin zayıf olduğunu gösterir: onu ihtimal diliyle söyle ya da bırak.
5. **İkinci vecih: söylenmeyeni bul.** Âyetin açık cümlelerini sıralamak ikinci vecih değildir. Önce sor: âyetin
   üslûbu beklenenden ayrılıyor mu (bir cümle türünden ötekine, emirden ya da nehiyden habere, fiilden isme, gâibden
   muhataba geçiş; beklenen bir atfın ya da cevabın gelmemesi)? Ayrılıyorsa bu ayrılık altında **takdir edilmiş bir
   cümle zincirine** işarettir: zinciri aç, her halkayı yaz. Sonra âyetteki durumu bir **temsil** olarak kurmayı dene
   (usul özetinin temsil bahsine ve İşârât'ın açık birimlerindeki temsillere bak). Temsil açık cümleleri tek tek
   örneklemek için değil, söylenmeyen ara cümleleri doğuran bir **halka zinciri** olarak kurulur; her halkayı âyetin
   bir kaydına eşle. Dinleyenin zihnindeki soru bu araçların yerine geçmez, onlarla birlikte kullanılır.
6. **Üçüncü vecihte** İşârât'ın yaptıklarını yap: bakılacak yerleri önce say, "neden şu lafız, şu değil" diye sor,
   beklenen ifadeyle muvazene et, mukadder cümleleri aç, dinleyenin zihninde doğan soruyu yaz, edatın genel
   hâssasından sonra buradaki nüktesini söyle, sonunda kayıtların asıl garaza nasıl aktığını tek bakışta topla. Ayrıca:
   - Her kayıt için **iki soru** sor: mânâya ne katıyor; ve konuşanın, muhatabın ya da dinleyenin zihninde ve
     vicdanında **ne iş görüyor** (hangi duyguyu uyandırıyor, hangi hükmü onda yerleştiriyor, ona ne öğretiyor).
     İkinci soru sorulmazsa kaydın nükteleri yalnız mantıkî ve nahvî kalır.
   - Âyette bir iddia ve ona bir cevap ya da red varsa: iddia cümlesinin kayıtlarındaki mânâları tek tek say, sonra red
     cümlesinin her kaydını bunlardan birine **cevap olarak** eşle. Eşleme şekil üzerinden (bir nekreye bir nekre)
     değil mânâ üzerinden yapılır; iddiada çıkarmadığın bir nükte, redde eşini boş bırakır.
7. **Müfessirler ayrıldığında** (i'râb, atıf, bağ, takdir) birini seçme, "hepsi olabilir" deyip de geçme. Her görüşün
   hangi **itibarla** doğru olduğunu sor (kıssanın akışı, meâl, lafız, hadd-i zât); İşârât vecihleri ayrı itibarlarla
   birlikte tutar. İhtilafın gösterdiği gerilim (bir görüşün bir yere oturmaması) çoğu zaman bir nükteye kapıdır.
8. **Kapsam ve derece:** kendi tespitini vecihlerden biri olarak yaz ("… olabilir", "bir vechi de şudur").
   "Tabiatıyla", "zâtında", "daima", "hiç", "ancak", "X değil Y'dir" gibi inhisar ve mutlaklık kalıplarını ancak
   kaynak öyle diyorsa kullan. Bir kaynağın ya da İşârât'ın ara halkalarla (sebep zinciri, takdir) kurduğu bir ilişkiyi
   kısaltırken halkaları atlayıp ilişkiyi mahiyet ya da zorunluluk hükmüne çevirme: "A, B'ye yol açar" ile "A
   tabiatıyla B'dir" ayrı hükümlerdir.

## Çalışma sırası

@tam 1. Ek 1'i (usul özeti) ve Ek 2'yi (birim çizelgesi) oku. Ek 3'te İşârât'ın sınanan âyetlerden önceki ve sonraki
@tam    birimlerini, Bakara 17–20'nin nazarî girişini ve aynı türden birkaç birimi baştan sona oku: usulü ve üslûbu
@tam    oradan al.
@ince 1. Ek 1'i (usul özeti) ve Ek 2'yi (birim çizelgesi) oku. Ek 3'teki birimleri (sınanan âyetlerden önceki ve
@ince    sonraki birimler, Bakara 17–20'nin nazarî girişi) baştan sona oku; aynı türden birkaç birimi daha `risale`
@ince    eklentisinde `read_section` ile oku (kimlikleri Ek 2'de): usulü ve üslûbu oradan al.
@ince    İşârât bir edatın, bir hey'etin ya da bir üslûbun genel kaidesini çoğu zaman başka bir âyetin bahsinde söyler.
@ince    Taslakta böyle bir kaideye dayanacaksan onu İşârât'ın kendisinde ara: `risale` eklentisinde `search` (Arapça
@ince    kelimeler) ve `semantic_search` (mânâ), ikisinde de `work: "isaratul-icaz-arabi"`; Ek 2 hangi birimde neyin
@ince    işlendiğini de gösterir. Bulduğunu `get_passage` ile bağlamıyla oku, sonra ona dayan.
2. `get_ayah` ile âyetleri ve bir öncesini al. `tefsir` eklentisinde `find_ayah` ile müfessirlerin bu âyetlerdeki
   birimlerini bul; en az Zemahşerî, Beyzâvî, Râzî ve Ebüssuûd'u oku (İşârât'ın adıyla andığı ya da onlara yakın
   kaynaklar), gerekirse öbürlerini. `risale` eklentisinde âyetle bağı olan yerlere bak; gerekirse `hadis`'e.
3. Yazmadan önce kendin için çıkar: âyetin cümleleri, asıl maksadı, öncesiyle bağın hatları, mukaddime gerekip
   gerekmediği (dört durumdan hangisi, ya da hiçbiri). Ve iki soru: **üslûbun beklenenden ayrıldığı yerler** neresi
   (Usul 5), **müfessirlerin ayrıldığı yerler** neresi (Usul 7)? İkisi de ikinci vechin ve üçüncü vechin asıl
   malzemesidir.
4. Taslağı yaz (şablon aşağıda).
5. **Öz denetim** (yazdıktan sonra, `cite`'tan önce), taslağı baştan sona bu gözle oku ve düzelt:
   - Tırnak içindeki her söz araçların döndürdüğü metin mi, yoksa bir takdir mi? Takdirse takdir kalıbıyla mı
     sunuldu, yanında kaynak numarası var mı (olmamalı)?
   - "Kendi tespiti" dediğin her söz okuduğun bir kaynakta geçiyor mu? Geçiyorsa kaynağına bağla.
   - İnhisar ve mutlaklık kalıpları (Usul 8): kaynak öyle mi diyor?
   - Dört maksat bağları: her birinin bu âyete özgü bir tutamağı var mı (Usul 2)?
   - Delâlet dereceleri: her birinin gerekçesi belli mi (Usul 4)?
6. Her eklentinin `cite` aracını, dayandığın ve alıntıladığın her cümle ya da aralıkla bir kez çağır;
   işaret ettiği sorunları düzelt. Tek "Kaynaklar" listesi ver (eklentiler sırayla: `first` ile numara sürer).

## Şablon

Cevabın yalnız taslaktır; önüne ve ardına açıklama yazma. Biçim:

```
# Yapay zekâ taslağı: {sura_name} {ayahs}
> Bu bir yapay zekâ taslağıdır, tefsir değildir. İşârâtü'l-İ'câz'ın usulüyle, ehlinin incelemesi için yazıldı.

## Âyet
> (âyetin metni, get_ayah'tan) [n]

## Mukaddime            ← yalnız dört durumdan biri varsa; yoksa bu başlık hiç olmaz
## Birinci vecih
## İkinci vecih
## Üçüncü vecih

(her başlığın altında: Arapça paragraf, altında "Yapay zekâ tercümesi: …" paragrafı; sırayla)

## Kaynaklar
```

- Bir müfessirden, Risale'den ya da hadisten alıntı ancak eklentinin verdiği metinle, ayrı satırda blok alıntı
  olarak ve numarasıyla [n] verilir; alıntıların tercümesi de "Yapay zekâ tercümesi:" damgalıdır.
- **İşaretler** (yalnız Türkçe tercüme paragraflarında, iddianın hemen ardından):
  - `[dil]` sarf, nahiv, lügat iddiası; `[belâgat]` meânî, beyân, bedî' iddiası;
  - kaynaktan geliyorsa numarası: `[belâgat; 3]`; kendi tespitinse `[belâgat; kendi tespiti]`;
  - **"kendi tespiti" yalnız okuduğun hiçbir kaynakta bulunmayan söz içindir.** Okuduğun bir müfessirde ya da
    İşârât'ın nazîr bir bahsinde bulunan nükte o kaynağa bağlanır; nazîrden taşıyıp buraya uyguladığın nükte
    `[belâgat; 7, buraya tatbiki kendi tespiti]` diye işaretlenir;
  - nüktenin delâlet derecesi Arapçada söylendiyse tercüme onu çevirir; tercüme Arapçada olmayan bir cümle (derece
    hükmü, etiket açıklaması) eklemez.
- **Tırnak ve takdir:** tırnak içine (« », “ ”, "…") yalnız araçların döndürdüğü metni koy. Kendi takdirin (dinleyenin
  sorusu, mukadder cümle, "denilseydi" denen ifade) İşârât'taki gibi bir takdir kalıbıyla sunulur ("كأنه قيل",
  "فإن قلت", "أي", "sanki şöyle denildi") ve **yanına kaynak numarası konmaz**. Bir kaynağı mealen aktarıyorsan tırnak
  kullanma. Kendi Türkçe karşılığını tırnak içinde, bir kaynağın sözü gibi verme.
- Âyet atıfları `get_ayah`'ın verdiği biçimdedir; cümle numarası ya da kimlik yazma, kaynakça numarası yeter.
