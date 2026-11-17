<!--
D14.2'nin hazırlığı (PLANLAR.md D14; kullanıcının kararı, 2026-11-17): İşârâtü'l-İ'câz'ın Bakara 9'dan 31–33'e kadarki
birimlerinde üç nazım vechinden başka neler var, nerede, ne kadar ve ne zaman. `scripts/d1-yapi.py oku` bu dosyanın
"---- YAPI ----" bölümünü alır, {yer tutucuları} doldurur; model istemi `claude -p` ile araçsız alır (birim başına bir
çağrı, birimin Arapça aslı cümle kimlikleriyle ve müellifin Türkçe hâşiyeleri). Uzunlukları program hesaplar.

Bu çalışma İşârât'ın usulünü anlamak içindir; saklı birimler de içindedir (21–22, 25, 26–27, 28, 29, 30). Sonuçtan
taslağa yalnız genel kural gider (dersin yeri, ne zaman geldiği, payı); hiçbir birimin içeriği yazara gitmez.

Sürümler:
- y1 (2026-11-17): ilk sürüm.
-->

---- YAPI ----

# Bağlam

Bediüzzaman Said Nursî İşârâtü'l-İ'câz'ı Arapça yazdı (Türkçe tercümesi Abdülmecid Nursî'nindir; aşağıdaki Türkçe
hâşiyeleri müellif sonradan yazdı). Eser âyet gruplarını çoğunlukla üç vecihle işler, her biri kendi geçiş cümlesiyle
açılır:

- **V1** âyetin öncesiyle nazmı (ör. "أما نظمها بما قبلها", "اعلم أن وجه النظم", "وجه نظم هذه الآية بسابقتها");
- **V2** âyetin cümlelerinin birbiriyle nazmı (ör. "وأما النظم بين جملها", "أما نظم الجمل بعضها مع بعض");
- **V3** her cümlenin hey'etleri, kayıtları ve kelimeleri (ör. "وأما نظم هيئات جملة جملة", "أما جملة ...").

Bunların dışında bazı birimlerde başka kısımlar da vardır: mukaddime, meseleler, okuyucuya dönen bir ders, bir
itiraz ve cevabı, bir tenbih… Senden bu birimin **üç vechin olağan nazım tahlili dışında kalan her kısmını** bulmanı
istiyoruz: ne olduğunu, nerede durduğunu, neye dayandığını.

# Birim: {birim}

Aşağıda birimin Arapça aslı var; her cümlenin başında kimliği (`c012`, alt bölümde `mukaddime/c012`), bölüm
başlıkları `###` ile. En sonda, varsa, müellifin bu birime yazdığı Türkçe hâşiyeler.

# Türler

- `mukaddime`: vecihlerden önce ya da arasında, bir meseleyi (iman rüknü, kelâm ihtilafı, bir üslûbun nazarî temeli)
  hazırlayan kısım; çoğu kez başlıklıdır.
- `mesele`: başlıklı ya da "المسألة …" diye açılan, bir lafzın tahkiki ya da bir meselenin ispatı.
- `ders`: âyetten **okuyucuya dönük** ahlâkî, imanî ya da içtimaî bir ders çıkaran kısım; nazmın nüktesini değil,
  âyetin insana ne öğrettiğini söyler. Çoğu kez bir hitapla ("أيها الناس", "أيها المسلمون", "فيا …", "إن هذه
  الآية تدعوكم") ya da bir uyarıyla açılır.
- `soru_cevap`: âyetin mânâsına ya da akideye dair bir itiraz ve cevabı (kelâmî, aklî, ahlâkî). **Belâgat nüktesine
  dair "إن قلت … قلت" soruları olağan nazım tahlilidir, sayma.**
- `tenbih`: "تنبيه" diye ya da benzeri bir uyarıyla açılan, okuyucunun dikkatini bir şeye çeken kısa kısım.
- `tezyil`: bir kısmın ardına eklenen tamamlayıcı ya da kapanış (hâtime).
- `diger`: yukarıdakilerden hiçbiri olmayan ama olağan nazım tahlili de olmayan kısım; türünü `ad` alanında adlandır.

Bir kısım bir vechin içinde de durabilir (9–10'da olduğu gibi üçüncü vechin sonunda bir lafızdan kalkan bir ders):
onu da yaz, yerini "V3 içinde, sonunda" diye belirt. Bir vechin içindeki kısa bir hüküm cümlesi ders değildir; ders
okuyucuya döner ve en az birkaç cümle sürer.

# Çıktı

Cevabın yalnız tek bir ```json kod bloğudur:

```json
{{
  "vecihler": {{"V1": "ilk cümle kimliği ya da null", "V2": "…", "V3": "…"}},
  "vecih_notu": "vecihler adıyla geçmiyorsa ya da sıra farklıysa kısa not",
  "kisimlar": [
    {{"tur": "ders", "ad": "kısa ad", "ilk": "c080", "son": "c099",
      "yer": "V1 öncesi | V1 içinde | V1 ile V2 arasında | V2 içinde | V2 ile V3 arasında | V3 içinde | V3 içinde, sonunda | V3 sonrası | birimin sonu",
      "lafiz": "dayandığı âyet lafzı (Arapça) ya da null",
      "hitap": true,
      "gerekce": "müellif bu kısmın neden burada geldiğini söylüyorsa o cümlenin kimliği ve kısa açıklama; söylemiyorsa null",
      "ozet": "bir iki cümle, Türkçe: ne söylüyor"}}
  ],
  "hasiyeler": [{{"sira": 1, "tur": "ders | soru_cevap | izah | diger", "ozet": "bir cümle, Türkçe"}}],
  "genel": "iki-üç cümle: bu birimde üç vecih dışında ne var, ne yok"
}}
```

Kısımlar birim sırasıyla. Hiç yoksa `kisimlar` boş liste. Her kimlik aşağıdaki metinde geçen bir kimlik olmalı.

{metin}
