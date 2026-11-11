<!--
D1 provasının istemi (PLANLAR.md D1.3). Sürümlüdür: her değişiklik aşağıdaki "Sürümler"e tarihiyle yazılır,
düzeltmeler yalnız genel usule yapılır, âyete özgü ipucu girmez. `scripts/d1-prova.py hazirla <birim>` bu dosyanın
"İSTEM" çizgisinden sonrasını alır, {yer tutucuları} doldurur ve sonuna ekleri koyar: usul özetinin ve birim
çizelgesinin prova kopyaları (sınanan birimden alınan her şey çıkarılmış) ve İşârât'ın Arapça aslı (sınanan birim
hariç). Model bu istemi `claude -p` ile, yerleşik araçlar ve web kapalı, yalnız prova sunucularıyla alır.

Sürümler:
- v1 (2026-11-11): ilk sürüm; 11–12 için.
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

- İşârâtü'l-İ'câz: Arapça aslı bu istemin sonunda (Ek 3) cümle kimlikleriyle; Türkçe tercümesi ve Risale-i Nur'un
  bütün eserleri `risale` eklentisinde.
- Müfessirlerin eserleri (Taberî, Mâtürîdî, Zemahşerî, Râzî, Kurtubî, Beyzâvî, Nesefî, İbn Kesîr, Celâleyn,
  Süyûtî, Ebüssuûd, Bursevî, Âlûsî): `tefsir` eklentisinde.
- Hadis kitapları: `hadis` eklentisinde.
- Âyetin metni: `get_ayah`. Âyeti ve kendi alıntılarını eklentinin verdiği gibi, harf harf aynı yaz.

Her iddia bir kaynağa, her nükte âyetin bir lafzına ya da hey'etine bağlanır. Bir nükteyi bir müfessirden
alıyorsan onu an ve kaynağını göster; kendi tespitinse öyle işaretle (aşağıda). Bir müfessirin sözünü İşârât'a ya
da müellife mal etme.

## Usul (Ek 1 ve Ek 2'nin özü)

1. **Düzen:** Bakara 9'dan sonraki sabit düzen: âyet; gerekiyorsa mukaddime; **birinci vecih** (âyetin öncesiyle
   nazmı); **ikinci vecih** (âyetin cümlelerinin birbiriyle nazmı); **üçüncü vecih** (her cümlenin hey'etleri,
   kayıtları ve kelimeleri). Her vecih İşârât'taki gibi kendi geçiş cümlesiyle açılır.
2. **Dört maksat:** âyetin asıl maksadı her zaman söylenir. Tevhid, nübüvvet, haşir ve adalet maksatlarından öbürleri
   yalnız âyetin bir lafzına ya da hey'etine dayandırılabiliyorsa ve derecesiyle (sarih, işaret, remiz, îmâ, telvih)
   söylenir; dördü her âyette zorla gösterilmez.
3. **Mukaddime** yalnız şu dört durumdan biri varsa yazılır: âyetin meâli dört maksattan ya da iman rükünlerinden
   biridir; âyetin altında büyük bir kelâm ihtilafı vardır; bir üslûp türü ilk kez toplu gelir ve nazarî temel
   ister; bir lafız tahkik ister. Kısa tutulur, her iddiası âyetin bir lafzına bağlanır; mesele İşârât'ta ya da
   Risale-i Nur'da işlenmişse yeniden kurulmaz, oraya atıfla hülâsa edilir. Bu durumlardan biri yoksa mukaddime
   yazılmaz.
4. **Kabul ölçüsü:** bir nükte Arap dili ilimlerinin reddetmediği, belâgatin güzel bulduğu, şeriatin maksatlarına
   uygun bir nükte olmalı; hayal bir hakikat çekirdeğine dayanmalı; her nüktenin delâlet derecesi belirtilmeli.
5. **Üçüncü vecihte** İşârât'ın yaptıklarını yap: bakılacak yerleri önce say, "neden şu lafız, şu değil" diye sor,
   beklenen ifadeyle muvazene et, mukadder cümleleri aç, dinleyenin zihninde doğan soruyu yaz, iki cümlenin
   kayıtlarını karşılıklı eşle, edatın genel hâssasından sonra buradaki nüktesini söyle, sonunda kayıtların asıl
   garaza nasıl aktığını tek bakışta topla.

## Çalışma sırası

1. Ek 1'i (usul özeti) ve Ek 2'yi (birim çizelgesi) oku. Ek 3'te İşârât'ın sınanan âyetlerden önceki ve sonraki
   birimlerini, Bakara 17–20'nin nazarî girişini ve aynı türden birkaç birimi baştan sona oku: usulü ve üslûbu
   oradan al.
2. `get_ayah` ile âyetleri ve bir öncesini al. `tefsir` eklentisinde `find_ayah` ile müfessirlerin bu âyetlerdeki
   birimlerini bul; en az Zemahşerî, Beyzâvî, Râzî ve Ebüssuûd'u oku (İşârât'ın adıyla andığı ya da onlara yakın
   kaynaklar), gerekirse öbürlerini. `risale` eklentisinde âyetle bağı olan yerlere bak; gerekirse `hadis`'e.
3. Yazmadan önce kendin için çıkar: âyetin cümleleri, asıl maksadı, öncesiyle bağın hatları, mukaddime gerekip
   gerekmediği (dört durumdan hangisi, ya da hiçbiri).
4. Taslağı yaz (şablon aşağıda).
5. Yazdıktan sonra her eklentinin `cite` aracını, dayandığın ve alıntıladığın her cümle ya da aralıkla bir kez çağır;
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
  - nüktenin delâlet derecesi tercümede açıkça söylenir (sarâhaten, işâreten, remzen, îmâen, telvîhen).
- Âyet atıfları `get_ayah`'ın verdiği biçimdedir; cümle numarası ya da kimlik yazma, kaynakça numarası yeter.
