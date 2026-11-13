<!--
D7 yapay zekâ karşılaştırıcısının istemi (PLANLAR.md D7.1). Sürümlüdür: her değişiklik aşağıdaki "Sürümler"e
tarihiyle yazılır; sürüm özeti her çıktının meta kaydındadır. `scripts/d1-yz.py` bu dosyanın üç bölümünü ("---- ORTAK
----", "---- ENVANTER ----", "---- DENETIM ----", "---- ESLESTIRME ----") alır, {yer tutucuları} doldurur. Model
istemi `claude -p` ile, proje dışında, yerleşik araçlar, web ve eklentiler kapalı alır: bütün girdiler istemdedir.

İlkeler (kullanıcı onayladı, 2026-11-13): karşılaştırıcı eşleştirir, hüküm vermez (fazladan söylenenin doğruluğunu
ehli söyler); her satır iki ucuyla (İşârât'ın cümle kimliği, taslağın blok çapası) ve iki taraftan harfi harfine
alıntıyla; alıntılar sonra mekanik olarak denetlenir.

Sürümler:
- v1 (2026-11-13): ilk sürüm; 11–12 için.
-->

---- ORTAK ----

# Bağlam

Bediüzzaman Said Nursî İşârâtü'l-İ'câz'ı Arapça yazdı; Türkçe tercümesi kardeşi Abdülmecid Nursî'nindir. Eser her
âyet grubunu çoğunlukla üç vecihle işler: **birinci vecih** âyetin öncesiyle nazmı (irtibatı), **ikinci vecih**
âyetin cümlelerinin (açık ve mukadder) birbiriyle nazmı, **üçüncü vecih** her cümlenin hey'etleri, kayıtları ve
kelimeleri (takdim-te'hir, ta'rif-tenkir, edatlar, üslûp, "neden şu lafız, şu değil" soruları, kayıtların asıl
garaza nasıl aktığı).

Bir **prova** yürütülüyor: bir yapay zekâ, İşârât'ın {sura_name} {ayahs}. âyetlerdeki kısmını görmeden, İşârât'ın
usulüyle bir "yapay zekâ taslağı" yazdı (Arapça asıl, paragraf paragraf Türkçe tercümesiyle). Şimdi taslak İşârât'ın
gizlenen metniyle karşılaştırılacak. Senin işin bu karşılaştırmanın bir parçasıdır.

# Uyacağın kurallar

- **Eşleştir, hüküm verme.** Bir nüktenin taslakta bulunup bulunmadığını ve İşârât'la çelişip çelişmediğini
  söylersin; taslağın fazladan söylediği bir şeyin dil, belâgat ya da usulce doğru olup olmadığına karar vermezsin.
  O karar ehlinindir.
- **Yalnız verilen metne dayan.** İşârât'ın bu âyetlerde ne dediğine dair yalnız aşağıda verilen metni esas al;
  hafızandan ekleme yapma.
- **Alıntılar harfi harfine.** `alinti` alanına yazdığın her söz, gösterdiğin kimliğin ya da çapanın metninden
  kesintisiz bir parçadır, olduğu gibi kopyalanır (hareke eksik ya da fazla olabilir, kelimeler değişmez). Arada
  atladığın yer varsa "…" koy. 4–25 kelime yeter. Bu alıntılar sonra bir programla metinde aranacak; bulunmayan satır
  işaretlenir.
- **Açıklamalar Türkçe**, kısa ve düz: bir ya da iki cümle.
- Cevabın yalnız tek bir ```json kod bloğudur; önüne ve ardına bir şey yazma.

---- ENVANTER ----

# Görev: gizlenen metnin nükte envanteri

Aşağıda İşârât'ın {sura_name} {ayahs}. âyetlerdeki kısmı var: Arapça asıl (her cümle `[a001]` gibi kimliğiyle) ve
Abdülmecid Nursî tercümesi (her cümle `[t001]` gibi kimliğiyle). Bu metnin söylediği her **nükteyi** sırayla listele.
Bu liste bir cevap anahtarı olacak: üç ayrı yapay zekâ taslağının bu nüktelerden hangisini yakaladığı, hangisini
atladığı ona göre sayılacak. Bu yüzden eksiksiz ve dengeli olmalı.

**Nükte nedir:** metnin âyet hakkında yaptığı tek bir tespit: bir bağ (âyetin öncesiyle, iki cümlenin birbiriyle),
bir hey'etin, kaydın, kelimenin ya da edatın bir nüktesi, açılan bir mukadder cümle, âyetin maksadı hakkında bir hüküm,
bir temsilin gösterdiği şey, sonda yapılan toplayış.

**Ölçü:**
- Bir kalem = bir özellik (lafız, hey'et ya da bağ) + metnin onun için söylediği bir gerekçe. Metin aynı özellik için
  iki ayrı gerekçe veriyorsa iki kalem; bir gerekçeyi birkaç cümlede açıyorsa tek kalem.
- Geçiş cümleleri ("وأما جملة …", "اعلم أن وجه النظم …"), âyetin tekrarı ve "فتأمل" gibi sözler kalem değildir.
- Bir temsil (misal) birkaç cümle sürüyorsa, gösterdiği her ayrı bağ bir kalemdir; temsilin kendisini kalem yapma.
- Tercümede olup Arapçada olmayan (mütercimin eklediği) bir şey varsa onu da kalem yap ve `yalniz_tercume: true`
  işaretle. Arapçada olup tercümede olmayan kalemde `tr` boş kalır.
- Kalemleri metnin sırasıyla ver.

**Alanlar:**

```json
{{"kalemler": [
  {{"id": "N01",
   "vecih": "V1 | V2 | V3",
   "lafiz": "nüktenin bağlı olduğu lafız ya da hey'et, Arapça (ör. \"إِنَّمَا\", \"تعريف الْمُفْسِدُونَ\"); bağ kaleminde iki ucu (\"قَالُوا ← لَا تُفْسِدُوا\")",
   "nukte": "metnin bu özellik için söylediği, Türkçe, yorum katmadan; 1–2 cümle",
   "ar": ["a003"],
   "tr": ["t006", "t007"],
   "alinti": "a-kimliklerinden birinin metninden harfi harfine parça (yalniz_tercume ise t-kimliğinden)",
   "yalniz_tercume": false}}
]}}
```

# İşârâtü'l-İ'câz, {sura_name} {ayahs}: Arapça asıl

{arapca}

# Abdülmecid Nursî tercümesi

{turkce}

---- DENETIM ----

# Görev: nükte envanterini denetle

Aşağıda İşârât'ın {sura_name} {ayahs}. âyetlerdeki kısmı (Arapça asıl `[a001]`, tercüme `[t001]`) ve başka bir yapay
zekânın bu metinden çıkardığı **nükte envanteri** var. Envanter bir cevap anahtarı olacak: üç yapay zekâ taslağının bu
nüktelerden hangisini yakaladığı ona göre sayılacak. Metni baştan sona kendin oku, sonra envanteri denetle.

**Envanterin ölçüsü:** bir kalem = bir özellik (lafız, hey'et ya da bağ) + metnin onun için söylediği bir gerekçe;
aynı özellik için iki ayrı gerekçe iki kalemdir; geçiş cümleleri, âyetin tekrarı ve bir temsilin kendisi kalem
değildir (temsilin gösterdiği her bağ kalemdir).

**Bakacakların ve önerilerin türü (`tur`):**
- `eksik`: metnin söylediği bir nükte envanterde yok. `oneri`: yeni kalem (alanları envanterdeki gibi, `id` yazma).
- `bol`: bir kalem iki ayrı nükteyi birleştirmiş. `ilgili`: o kalem; `oneri`: yerine geçecek kalemlerin listesi.
- `birlestir`: iki ya da daha çok kalem aynı nükteyi tekrarlıyor. `ilgili`: o kalemler; `oneri`: birleşmiş kalem.
- `duzelt`: kalemin açıklaması metne uymuyor, kimliği ya da alıntısı yanlış. `ilgili`: o kalem; `oneri`: düzeltilmiş kalem.
- `sil`: kalem metinde yok ya da bir geçiş sözü. `ilgili`: o kalem.

Her öneride `gerekce` (Türkçe, kısa) ve dayandığın metnin kimliği bulunur. Sorun bulmadığın kalem için bir şey yazma.
Envanter iyiyse liste boş olabilir; zorla öneri üretme.

```json
{{"oneriler": [
  {{"tur": "eksik | bol | birlestir | duzelt | sil",
   "ilgili": ["N05"],
   "oneri": {{"vecih": "…", "lafiz": "…", "nukte": "…", "ar": ["a010"], "tr": ["t015"], "alinti": "…", "yalniz_tercume": false}},
   "gerekce": "…"}}
]}}
```

# İşârâtü'l-İ'câz, {sura_name} {ayahs}: Arapça asıl

{arapca}

# Abdülmecid Nursî tercümesi

{turkce}

# Denetlenecek envanter

```json
{envanter}
```

---- ESLESTIRME ----

# Görev: taslağı gizlenen metinle eşleştir

Aşağıda üç şey var:
1. İşârât'ın {sura_name} {ayahs}. âyetlerdeki kısmı: Arapça asıl `[a001]` ve tercüme `[t001]`.
2. Bu metnin **nükte envanteri** (cevap anahtarı; `N01`…).
3. Bir **yapay zekâ taslağı**: her paragrafın başında çapası var (`[V1/ar/0]` birinci vechin ilk Arapça paragrafı,
   `[V1/tr/0]` onun Türkçe tercümesi; `V2`, `V3`, `Mukaddime` aynı biçimde). Taslağın Türkçe paragraflarında yazarın
   kendi işaretleri var: `[belâgat; 3]` "bu iddia kaynakçadaki 3 numaralı kaynaktan", `[belâgat; kendi tespiti]`
   "yazarın kendi tespiti"; taslağın kaynakçası en sonda. Taslak gizlenen metni görmeden yazıldı.

İki iş yap.

**A. Envanterin her kalemi için** taslakta karşılığı olup olmadığını söyle (`nukteler`; envanterdeki her kalem bir
kez, sırasıyla):
- `aynen`: taslak aynı özelliğe (lafız, hey'et ya da bağ) bakıyor ve aynı nükteyi söylüyor; ifade, uzunluk ve vecih
  farklı olabilir.
- `kismen`: aynı nükteye değiniyor ama eksik, daha genel ya da gerekçenin yalnız bir kısmıyla.
- `farkli_gerekce`: aynı özelliğe bakıyor ama başka bir nükte çıkarıyor.
- `yok`: taslakta karşılığı yok.
`taslak` alanına karşılığın çapalarını yaz (Arapça paragrafın çapasını; tercümede kalmışsa tercümeninkini), `alinti`
alanına o paragraftan harfi harfine parça. `yok` ise ikisi boş kalır. `gerekce`: neden bu durum, bir cümle.
Karşılığı aramak için taslağın tamamına bak: aynı nükte başka bir vecihte, bir mukaddimede ya da bir alıntının
ardında olabilir. Taslak nükteyi bir kaynaktan (bir müfessirden, İşârât'ın başka bir yerinden) alıntıyla söylüyorsa da
karşılık sayılır.

**B. Taslağın fazlası** (`fazla`): taslağın envanterdeki hiçbir kalemle karşılanmayan her iddiası. İddia: taslağın
âyet hakkında yaptığı bir tespit (bağ, nükte, mukadder cümle, maksat hükmü, mukaddime iddiası, bir müfessirden nakil).
Geçiş sözleri, âyetin ve alıntıların kendisi, A'da bir kaleme karşılık saydığın yer fazla değildir. Ardışık cümleler
tek bir iddiayı açıyorsa tek kalem. Her kalemde:
- `taslak` (çapalar), `alinti` (Arapça paragraftan harfi harfine; Arapçada yoksa tercümeden), `iddia` (Türkçe, kısa);
- `isaret`: taslağın tercümesindeki işarete göre `kaynakli` (bir kaynak numarası var), `kendi_tespiti` ya da
  `isaretsiz`; `kaynak`: işaretteki numaralar (yoksa boş liste);
- `celiski`: iddia İşârât'ın bir kalemiyle çelişiyorsa o kalemin kimliği ve `gerekce`'de nasıl çeliştiği; çelişmiyorsa
  `null`. "İşârât bunu söylemiyor" çelişki değildir; çelişki, ikisinin birlikte doğru olamamasıdır.
Fazlanın doğru ya da değerli olup olmadığını söyleme.

```json
{{"nukteler": [
  {{"id": "N01", "durum": "aynen | kismen | farkli_gerekce | yok", "taslak": ["V1/ar/0"], "alinti": "…", "gerekce": "…"}}
 ],
 "fazla": [
  {{"taslak": ["V3/ar/5", "V3/tr/5"], "alinti": "…", "iddia": "…", "isaret": "kaynakli | kendi_tespiti | isaretsiz",
   "kaynak": ["3"], "celiski": null, "gerekce": ""}}
 ]}}
```

# İşârâtü'l-İ'câz, {sura_name} {ayahs}: Arapça asıl

{arapca}

# Abdülmecid Nursî tercümesi

{turkce}

# Nükte envanteri

```json
{envanter}
```

# Yapay zekâ taslağı

{taslak}
