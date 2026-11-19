<!--
D15 İşârât karşılaştırması: tek taslak, İşârât'ın kendisiyle (PLANLAR.md D15; kullanıcının kararları 2026-11-18 ve
2026-11-19: h2 kolu yok; D5'te soru "eskisinden iyi mi" değil "kendi başına yeterli mi"). Sürümlüdür: her değişiklik
"Sürümler"e tarihiyle yazılır. `scripts/d1-duzelt.py isarat` "---- KARSILASTIRMA ----" bölümünü alır, {yer
tutucuları} doldurur. Model istemi `claude -p` ile, yerleşik araçlar ve web kapalı, **yayındaki** sunucularla alır
(açık kitap: İşârât'ın bu birimi okunabilir).

İki işi var: (1) mutlak hüküm (bölüm bölüm ve bütün: yeterli mi); (2) notlar, kapalı kitap eleştirmenin notlarıyla
aynı biçimde (`tur`, `capa`, `taslak_alinti`, `oncelik`, `dayanak`), ki D15'in kör aletler ayarında
(`d1-duzelt.py notlar --acik isarat`) karşılaştırılabilsin: kapalı eleştirmen ve nisbet denetçisi gerçek kusurların
ne kadarını yakalıyor. Notları taslağı yazana gitmez.

Sürümler:
- i1 (2026-11-19): ilk sürüm; D15.1, 21–22 taslak 1 (h10).
-->

---- KARSILASTIRMA ----

# Bağlam

Bediüzzaman Said Nursî İşârâtü'l-İ'câz'ı Arapça yazdı; Türkçe tercümesi kardeşi Abdülmecid Nursî'nindir. Eser âyet
gruplarını çoğunlukla üç vecihle işler: **birinci vecih** âyetin öncesiyle nazmı, **ikinci vecih** âyetin cümlelerinin
(açık ve mukadder) birbiriyle nazmı, **üçüncü vecih** her cümlenin hey'etleri, kayıtları ve kelimeleri. Asıl maksadı
taşıyan âyetlerde başta bir mukaddime gelebilir.

Bir yapay zekâ, İşârât'ın {sura_name} {ayahs}. âyetlerdeki kısmı ondan saklanarak, İşârât'ın usulüyle ve Risale-i
Nur'u me'haz alarak bir "yapay zekâ taslağı" yazdı. Bu bir taslaktır, tefsir değildir. Asıl iş İşârât'ın
bulunmadığı âyetlerde (Bakara 34 ve sonrası) yapılacak; orada taslaklar ehline okunmak üzere üretilecek. Senden
istenen, bu taslağı İşârât'ın kendisiyle karşılaştırarak **kendi başına yeterli mi** sorusuna cevap vermek. Başka
bir taslakla kıyas yok.

İşârât'ın bu âyetlerdeki kısmını `risale` eklentisinde oku: Arapça aslı `read_section("{gizli_ar}")`, Abdülmecid
Nursî tercümesi {gizli_tr_okuma}. Taslağın dayandığı kaynakları gerektikçe eklentilerde aç.

# Ölçü

"Yeterli", İşârât'ın yerini tutmak demek değildir: İşârât'ın her nüktesini bulmak beklenmez, müellifin dehası
taklit edilemez. Yeterli taslak: (a) **yanlışı ve İşârât'la çelişkisi yok ya da önemsiz**; (b) İşârât'ın bu
âyetlerdeki **asıl maksadını ve ana nüktelerini** (garaz, nazmın omurgası, başlıca takdir zincirleri, asıl dersi)
yakalıyor; (c) eklediği şey sağlam (âyetin lafzına, usule, Risale-i Nur'a ya da kaynağa dayanıyor, zorlama değil);
(d) kaynaklara nisbeti doğru. İşârât'tan farklı ama sağlam bir vecih kusur değildir; tenevvüdür, `dogru` diye yaz.

Hüküm üç derece: `yeterli` (ehline olduğu gibi gidebilir), `duzeltmeyle` (ehline gidebilir ama belirli yerleri
düzeltilmeli), `yetersiz` (asıl maksat ya da omurga kaçmış, ya da ciddi yanlış var).

# Sorular (bölüm bölüm: Mukaddime varsa, V1, V2, V3; sonra bütün)

1. **İşârât'ın ana nükteleri:** bu bölümde İşârât'ın en önemli nükteleri neler; taslak her birini yakalamış mı
   (aynen, kısmen, başka yoldan, hiç)? Yalnız önemli olanları say, her birine dayandığın İşârât cümlesinin
   kimliğiyle.
2. **Yanlış ve çelişki:** taslakta İşârât'la çelişen, dile ya da usule aykırı, kapsamını aşan ya da uydurma bir şey
   var mı?
3. **Taslağın katkısı:** İşârât'ta olmayan ama sağlam olan ne var (Risale-i Nur'dan ders, sağlam bir istinbat)?
   Zorlama var mı (lafzın taşımadığı nükte)?
4. **Nisbet:** bir sözü bir müfessire, İşârât'ın öbür bir birimine ya da Risale-i Nur'a mal ederken kaynak gerçekten
   öyle mi diyor? Türkçe «…» takdir ve beklenen söz işaretidir (yazarın kendi sözü); "…" ve “…” kaynağın sözüdür.

# Kurallar

- Her hüküm okuduğun metne dayanır; İşârât'ın ne dediğini yalnız bu oturumda okuduğundan söyle, `dayanak`a
  kimlikleri yaz.
- Notlar kusurlar ve katkılar içindir: her `eksik`, `yanlis`, `kaynak`, `kapsam`, `uydurma` ve `zorlama` notu tek bir
  yere bağlıdır (`capa`); İşârât'ta olup taslağın hiçbir yerinde olmayan nükte için `capa` "genel" ve `taslak_alinti`
  null. "Eksik" demeden önce taslağın bütün bölümlerinde ara.
- `oncelik`: `yuksek` (yanlış, çelişki, uydurma, yanlış nisbet; ya da asıl maksadın ya da ana nüktenin kaçması),
  `orta`, `dusuk`.
- `taslak_alinti` taslağın o çapasından harfi harfine kesintisiz bir parçadır (4–25 kelime; atladığın yer "…").
- Notlar Türkçe, düz ve kısa (en çok dört cümle). Cevabın yalnız tek bir ```json kod bloğudur.

# Çıktı

```json
{{
  "bolumler": [
    {{"bolum": "Mukaddime | V1 | V2 | V3", "hukum": "yeterli | duzeltmeyle | yetersiz",
      "ana_nukteler": [{{"nukte": "kısa", "dayanak": ["isaratul-icaz-arabi/…/c010"], "taslakta": "aynen | kismen | baska_yoldan | yok", "capa": "V2/tr/3 ya da null"}}],
      "gerekce": "iki-dört cümle"}}
  ],
  "butun": {{"hukum": "yeterli | duzeltmeyle | yetersiz", "gerekce": "üç-beş cümle",
             "duzeltilecekler": ["ehline gitmeden önce düzeltilmesi gereken en önemli en çok beş yer, çapasıyla"]}},
  "notlar": [
    {{"tur": "dogru | yanlis | eksik | fazla | kapsam | uydurma | zorlama | irab | belagat | usul | kaynak | uslup | diger",
      "capa": "V3/tr/12 ya da genel", "taslak_alinti": "… ya da null", "metin": "not",
      "oncelik": "yuksek | orta | dusuk", "dayanak": ["kimlikler"]}}
  ]
}}
```

# Taslak

Her paragrafın başında çapası var (`V3/ar/5`: üçüncü vecih, Arapça, 6. paragraf; `V3/tr/5` onun tercümesi).

{taslak}
