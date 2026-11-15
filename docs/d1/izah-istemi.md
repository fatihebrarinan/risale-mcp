<!--
D11 izah adımının istemi (PLANLAR.md D11). Sürümlüdür. `scripts/d1-hat.py izah <birim> --taslak <n>` "---- İZAH ----"
bölümünü alır, {taslak} yerine taslağın paragraf çiftlerini (çapa, Arapça, tercüme) koyar. Model (Opus) araçsız
çalışır; kaynak dosyası verilmez: izah yalnız taslağın söylediğini açar. Program izahta taslakta olmayan kaynak
numarası ve tırnak arar.

Kararlar (kullanıcıyla, 2026-11-15): izah ayrı adımda; günümüz Türkçesiyle; her paragrafın altında (birleştirme
adımı sonra); taslağın söylemediğini söylemez, [n] ve tırnak eklemez, terimi ilk geçtiği yerde açar.

Sürümler:
- i1 (2026-11-15, D11 pilotu).
-->

---- İZAH ----

# Görev: yapay zekâ taslağının günümüz Türkçesiyle izahı

Aşağıda İşârâtü'l-İ'câz'ın usulüyle yazılmış bir **yapay zekâ taslağı** var ({sura_name} {ayahs}): her paragraf
Arapça, altında Osmanlı Türkçesi üslûbunda tercümesi. Tercüme terimleri koruduğu için bugünün okuyucusu çoğu yerini
anlamıyor. Senden her paragraf için **günümüz Türkçesiyle bir izah** istiyoruz: aynı şeyi, bugünün okuyucusunun
anlayacağı dille, açarak söyle.

## Kurallar

- **Taslağın söylemediğini söyleme.** İzah yeni bir nükte, yeni bir delil, yeni bir kaynak, yeni bir hüküm eklemez;
  taslakta "olabilir" denen yeri kesinleştirmez, kesin denen yeri yumuşatmaz. Taslakta bir şey eksik ya da yanlış
  görünse de düzeltme; izah taslağın aynasıdır.
- **Terimleri aç:** belâgat ve nahiv terimini (takdir, hazf, kasr, tağlîb, iltifat, terâhî, ta'rîz…) ilk geçtiği
  yerde bir iki kelimeyle tarif et ("hazf, yani sözün bir parçasının söylenmeyip anlaşılmaya bırakılması"); sonra
  tekrar tarif etme.
- **Takdir edilen cümleleri** (taslağın "sanki şöyle denildi", "كأنه قيل" diye kurduğu sözleri) günümüz Türkçesiyle
  yeniden kur ki zincir görünsün.
- **Arapça kelime ve ibareler:** âyetin bir kelimesini anarken Arapçasını yaz, yanında okunuşu ya da anlamı olsun
  ("عَلَّمَ (öğretti) fiili…"). Uzun Arapça yazma.
- **Kaynak numarası ([n]) ve tırnak içinde alıntı ekleme.** Taslak bir müfessire dayanıyorsa adını an ("Beyzâvî'ye
  göre"), numara yazma. Tercümedeki `[dil]`, `[belâgat]`, `[kendi tespiti]` işaretlerini taşıma; gerekiyorsa "taslağın
  kendi tespiti olarak" de.
- **Uzunluk:** paragrafın tercümesi kadar ya da biraz uzun; kısa paragrafa kısa izah. Kaynaktan blok alıntı
  paragrafına ("> …") izah yazma.
- Hitap: okuyucuya "siz" diye değil, düz anlatımla. "Yapay zekâ taslağı" ve "tefsir" kelimelerini kullanma.

## Çıktı

Yalnız şu JSON, başka açıklama yok:

```json
{{"izah": [{{"capa": "V1/tr/0", "metin": "…"}}, …]}}
```

Her tercüme paragrafı için bir kayıt; `capa` paragrafın başındaki çapadır (`/tr/` olan). Sıra taslağın sırasıdır.

# Taslak

Her paragrafın başında çapası var (`V3/ar/5`: üçüncü vecih, Arapça, 6. paragraf; `V3/tr/5` onun tercümesi).

{taslak}
