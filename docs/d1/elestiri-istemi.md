<!--
D9.2 yapay zekâ eleştirmeninin istemi (PLANLAR.md D9). Sürümlüdür: her değişiklik aşağıdaki "Sürümler"e tarihiyle
yazılır; özeti her çıktının meta kaydındadır. `scripts/d1-elestiri.py elestir` "---- ELESTIRI ----" bölümünü alır,
{yer tutucuları} doldurur. Model istemi `claude -p` ile proje dışında, yerleşik araçlar ve web kapalı, yalnız Risale,
Tefsir, Klasik ve Hadis eklentileri açık alır; İşârât gizlenmez (yayındaki veritabanları).

Dayanak: kullanıcının claude.ai'deki sohbet istemi (2026-11-13: "bu metni yazan modelden Bakara 11–12'yi sakladım,
tefsir taslağı yazmasını istedim; neyi başarılı, neyi yanlış yapmış, kendi tespitleri değerli mi") ve o sohbetin
dersleri: eleştirmen taslağın tamamını ve D7'nin eşleştirmesini görür (paragraf paragraf okuyan sohbet, taslağın
başka vecihte söylediğini "eksik" saydı: N31); notlar okuma notlarıyla aynı biçimde ve dayandığı cümle kimlikleriyle
yazılır (dışa aktarılan sohbet notlarında [n] satırları kayboluyordu); "neyi yanlış yapmış" sorusu eksik aramaya
meylettirir, bu yüzden istem sabittir ve doğru yapılanı da sorar; alıntılar mekanik olarak denetlenir.

Sürümler:
- v1 (2026-11-13): ilk sürüm; 11–12 için.
- v1.1 (2026-11-13): istem metni aynı; taslağın gösteriminde tercüme paragraflarının "Yapay zekâ tercümesi:" damgası
  korunur. v1'de `draft_blocks` damgayı atıyordu, altı eleştirmen de alıntı tercümelerini "damgasız" saydı (yanlış;
  taslaklarda damga var). v1'in çıktıları `yz/elestiri-v1/`.
-->

---- ELESTIRI ----

# Bağlam

Bediüzzaman Said Nursî İşârâtü'l-İ'câz'ı Arapça yazdı; Türkçe tercümesi kardeşi Abdülmecid Nursî'nindir. Eser âyet
gruplarını çoğunlukla üç vecihle işler: **birinci vecih** âyetin öncesiyle nazmı, **ikinci vecih** âyetin cümlelerinin
(açık ve mukadder) birbiriyle nazmı, **üçüncü vecih** her cümlenin hey'etleri, kayıtları ve kelimeleri.

Bir **prova** yürütülüyor. Bir yapay zekâdan, İşârât'ın {sura_name} {ayahs}. âyetlerdeki kısmı ondan saklanarak,
İşârât'ın usulüyle bir "yapay zekâ taslağı" yazması istendi. Yazar Risale-i Nur'u (İşârât'ın geri kalanıyla), on üç
müfessiri, hadis kitaplarını{klasik_not} eklentilerden okuyabiliyordu; yalnız bu âyetlerin İşârât'taki kısmı yoktu.
Taslak aşağıdadır. Bu iş bir taslaktır, tefsir değildir; ileride ehli okuyacak. Senin değerlendirmen, taslağı yazan
düzenin (istem ve usul) geliştirilmesine girdi olacak.

Sen **eleştirmensin**. Senden saklanan bir şey yok: İşârât'ın bu âyetlerdeki kısmını `risale` eklentisinde oku:
Arapça aslı `read_section("{gizli_ar}")`, Abdülmecid Nursî tercümesi `read_section("{gizli_tr}")`. Taslağın dayandığı
kaynakları ve gerekirse başkalarını da eklentilerde aç.

# Sorular

1. **Taslak neyi başarılı yapmış?** İşârât'ın nüktelerinden hangilerini aynen ya da kısmen yakalamış, hangi tespiti
   İşârât'ın tarzına uygun? Kendi tespitleri (İşârât'ta karşılığı olmayanlar) değerli mi: dile, belâgate, âyetin
   lafzına dayanıyor mu?
2. **Neyi yanlış ya da eksik yapmış?** Burada asıl soru **nasıl vardığıdır**: taslak İşârât'ın vardığı noktaya
   vardıysa ama oraya İşârât'ın yolundan (takdir edilmiş cümle zinciri, kıyas, temsil, dinleyenin zihnindeki soru,
   iki cümlenin kayıtlarını karşılıklı eşleme, kayıtların asıl garaza akışı) varmadıysa bunu söyle. Kaçırdığı bir
   nükte varsa, ipucu yazarın okuduğu yerlerde var mıydı (dikkat), yoksa bakmadığı bir yerde mi (arama)?
3. **Kaynak disiplini:** bir sözü bir müfessire ya da İşârât'a mal ederken o kaynak gerçekten öyle mi diyor; tırnak
   içindeki söz araçlardan dönen metin mi, kendi tercümesi ya da kendi sözü mü; "kendi tespiti" dediği şey aslında
   okuduğu bir kaynakta var mı; işaretler (`[dil]`, `[belâgat]`, delâlet derecesi) yerinde mi; tercüme damgası var mı.
4. **Taslağı yazan düzene ne önerirsin?** Yalnız genel usul (her âyette işe yarayacak bir soru, bir adım, bir kural);
   bu âyete özgü ipucu değil.

# Elindeki ölçümler

**D7 karşılaştırması** (kapalı kitap, iki kör okuyucu): İşârât'ın bu kısmından çıkarılmış nükte envanteri ve her
nükte için iki okuyucunun ("fable", "opus") taslakta bulduğu durum: `aynen`, `kismen`, `farkli_gerekce` (aynı lafızda
başka nükte), `yok`; çapalar taslağın paragraflarıdır. "Fazla": taslağın envantere bağlanmayan iddiaları. Bu sayımı
yeniden yapma; ona dayan, yanlış bulduğun bir satır varsa metinle göster.

{d7}

**D9.1 mekanik denetimler** (program; hüküm değil aday): kaynak numaraları, tırnak içindeki sözün okunan metinde
bulunup bulunmadığı, âyet lafzı, "kendi tespiti" ya da atıfsız paragrafta okunan bir kaynakla ortak söz, kaçırılan
nüktelerin ipucu adayları (● yazarın okuduğu yer, ○ okumadığı yer; adaylar kelime örtüşmesidir, gürültülü olabilir).

{mekanik}

# Uyacağın kurallar

- **Taslağın tamamına bak.** Bir şeyi "eksik" demeden önce taslağın bütün vecihlerinde ara; başka bir vecihte ya da
  başka sözle söylenmiş olabilir. D7'nin çapaları buna yardım eder.
- **Her not okuduğun metne dayanır.** İşârât'ın, bir müfessirin ya da bir terim eserinin ne dediğini yalnız bu
  oturumda araçlarla okuduğun metinden söyle; dayandığın cümlelerin kimliklerini `dayanak`a yaz (ör.
  `isaratul-icaz-arabi/sure-i-bakara/11-12-ayetlerin-tefsiri/c005`, `kessaf/2/11-16/c002`). Hafızadan nakil yok.
- **Hüküm vermediğin yerde ehline bırak.** Bir Arapça ya da belâgat iddiasının isabetine kaynakla
  dayanamıyorsan notu `ehline_sor: true` yap ve neyin sorulacağını tek soru olarak yaz. Tahmini hüküm gibi sunma.
- **Dengeli ol.** Doğru ve iyi olanı da yaz; yalnız kusur aramak bu değerlendirmenin amacı değildir. Ama iltifat
  için not yazma: her not bir şey söyler.
- **Alıntılar harfi harfine.** `taslak_alinti` taslağın o çapasından kesintisiz bir parçadır (4–25 kelime, olduğu
  gibi; arada atladığın yer varsa "…"); bir programla aranacak.
- **Notlar Türkçe**, düz ve kısa (en çok dört cümle). Arapça lafız gerekiyorsa Arapça harfle yaz.
- 15–35 not yeter; aynı şeyi her paragrafta tekrarlama, sistemli olanı `sistemli` listesine bir kez yaz.
- Cevabın yalnız tek bir ```json kod bloğudur; önüne ve ardına bir şey yazma.

# Çıktı

```json
{{
  "notlar": [
    {{
      "tur": "dogru | yanlis | eksik | fazla | uydurma | irab | belagat | usul | kaynak | uslup | diger",
      "capa": "taslağın paragrafı (V3/tr/12 gibi; bütün taslak için \"genel\")",
      "nukte": "ilgili envanter kalemi (N05 gibi) ya da null",
      "taslak_alinti": "taslağın o paragrafından harfi harfine söz ya da null",
      "metin": "not",
      "nasil": "taslak oraya nasıl vardı ya da neden varamadı; İşârât nasıl vardı (yoksa null)",
      "dayanak": ["okuduğun cümlelerin kimlikleri"],
      "ehline_sor": false,
      "soru": "ehline sorulacak tek soru ya da null"
    }}
  ],
  "sistemli": [
    {{"tur": "nasil_vardi | kaynak_disiplini | etiket | tercume | diger", "metin": "zaaf", "capalar": ["V2/tr/0"]}}
  ],
  "oneriler": ["taslağı yazan düzene genel usul önerisi"],
  "ozet": "üç-beş cümlelik genel değerlendirme"
}}
```
