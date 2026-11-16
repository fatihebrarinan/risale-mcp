<!--
D12 iki eleştirmenin notlarının karşılaştırması (PLANLAR.md D12, "Kapalı ve açık kitap eleştirmen" (2)). Sürümlüdür.
`scripts/d1-duzelt.py notlar` "---- KARSILASTIRMA ----" bölümünü alır, {yer tutucuları} doldurur; model araçsız
(girdilerin hepsi istemde). Amaç: açık kitap eleştirmenin yakalayıp kapalının kaçırdıklarını "yalnız gizli metinden
bilinebilir" ve "kapalının da görebileceği" diye ayırmak; ikincisi küçükse kapalı eleştirmen D5'e hazırdır.

Sürümler:
- n1 (2026-11-16): ilk sürüm; D12.1, 31–33 taslak 7.
-->

---- KARSILASTIRMA ----

# Bağlam

Bir yapay zekâ, İşârâtü'l-İ'câz'ın usulüyle {sura_name} {ayahs}. âyetler için bir taslak yazdı; İşârât'ın bu
âyetlerdeki kısmı ondan saklandı. Taslağı iki eleştirmen bölüm bölüm okudu:

- **Kapalı kitap eleştirmen** (notları `K…`): İşârât'ın bu âyetlerdeki kısmını görmedi; usul özeti, İşârât'ın öbür
  birimleri, müfessirler, belâgat ve terim eserleri, hadis kitapları açıktı.
- **Açık kitap eleştirmen** (notları `A…`): aynı kaynaklara ek olarak İşârât'ın bu âyetlerdeki kısmını okudu.

İşârât'ın bu âyetlerdeki kısmı aşağıda (Arapça asıl ve Abdülmecid Nursî tercümesi).

# Görev

Açık kitap eleştirmenin **her notu** için:

1. `eslesen`: kapalı kitap eleştirmenin aynı şeyi (aynı yerde aynı kusuru ya da aynı iyiliği; sözü farklı olabilir)
   söyleyen notları. Yalnız konu yakınlığı yetmez: aynı yapılacak işe varmalı. Yoksa boş liste.
2. `tur`: eşleşen yoksa bu not neye dayanıyor?
   - `yalniz_gizli`: İşârât'ın bu âyetlerdeki metnini bilmeden yazılamazdı (o metindeki bir nükteyi, bir sözü,
     bir sırayı anıyor; taslağı onunla kıyaslıyor).
   - `gorulebilirdi`: İşârât'ın bu metni olmadan da usulden, dilden, belâgatten, kaynaklardan ya da taslağın
     kendisinden görülebilirdi (yanlış nisbet, kaynakta olmayan söz, tutarsızlık, açılmamış takdir, atlanan harf…).
     Not İşârât'ı anıyor olsa bile asıl kusur böyle görülebiliyorsa bu türdür.
   - `karisik`: ikisi birden (asıl yapılacak iş görülebilirdi, ama notun bir kısmı gizli metne dayanıyor).
   Eşleşen varsa `tur` `eslesti`.
3. `gerekce`: bir cümle.

Sonra kapalı kitap eleştirmenin, açığın hiçbir notuyla eşleşmeyen notlarına bak ve her biri için `deger` ver:
`yerinde` (taslakta gerçek bir kusur ya da iyilik), `supheli` (kusur iddiası metne ya da İşârât'a göre zayıf),
`yanlis` (İşârât'ın bu metnine ya da taslağın kendisine göre açıkça yanlış).

Cevabın yalnız tek bir ```json kod bloğudur:

```json
{{
  "acik": [{{"not": "A1", "eslesen": ["K3"], "tur": "eslesti | yalniz_gizli | gorulebilirdi | karisik", "gerekce": "…"}}],
  "kapali_tek": [{{"not": "K7", "deger": "yerinde | supheli | yanlis", "gerekce": "…"}}]
}}
```

# İşârât'ın bu âyetlerdeki kısmı

## Arapça asıl

{arapca}

## Tercüme

{turkce}

# Açık kitap eleştirmenin notları

{acik}

# Kapalı kitap eleştirmenin notları

{kapali}
