<!--
D12 düzeltme isteminin görev kısmı (PLANLAR.md D12). Sürümlüdür: her değişiklik aşağıdaki "Sürümler"e tarihiyle
yazılır. `scripts/d1-duzelt.py duzelt` taslağı yazan istemin **aynısını** (Ek 1–3 dahil; `istem-hat-h1.md`) başa koyar,
ardından bu dosyanın "---- DUZELTME ----" bölümünü {yer tutucuları} doldurarak ekler. Model aynı yazardır (Opus 5.5,
yüksek), aynı prova sunucularıyla (İşârât'ın sınanan birimi gizli); asıl oturumu görmez, taslağı ve notları görür.

Kararlar (kullanıcı, 2026-11-16): baştan yazdırma yerine düzeltme, yalnız değişen paragraflar; yazar bir notu
gerekçesiyle reddedebilir (retler notların kalitesini de ölçer); her not ya bir değişiklikte ya retlerde anılır.

Sürümler:
- d1 (2026-11-16): ilk sürüm; D12.1, 31–33 taslak 7 (kapalı ve açık kitap notlarıyla).
-->

---- DUZELTME ----

# Şimdiki görev: taslağını düzeltmek

Yukarıdaki görevle {sura_name} {ayahs} için bir taslak yazıldı; aşağıda, her paragrafın başında çapasıyla
(`V2/ar/3`: ikinci vecih, Arapça, 4. paragraf; `V2/tr/3` onun tercümesi). Bir eleştirmen onu bölüm bölüm okudu ve
notlar yazdı ({not_kaynagi}); aşağıda `{onek}1`, `{onek}2`… diye numaralı. Senden taslağı **yeniden yazmanı değil,
düzeltmeni** istiyoruz.

- **Her notu tart.** Haklıysa karşıla. Haksızsa, taslakta zaten karşılanmışsa (başka bir vecihte söylenmiş gibi) ya
  da usule aykırı bir şey istiyorsa gerekçesiyle reddet. Eleştirmen de yanılabilir: bir notu kabul etmeden önce
  dayandığı kaynağı oku; bir nükte ekleyeceksen onu da bir kaynağa ya da âyetin lafzına bağla.
- **Düzeltmek uzatmak değildir.** Bir notu karşılamak çoğu zaman bir cümleyi değiştirmek, bir takdiri açmak, bir
  iddiayı ihtimal diliyle söylemek ya da çıkarmaktır. Arapça paragrafların toplamı hedefte kalır: {en_az}–{en_cok}
  harf; taslak şu an {simdi} harf.
- **Yalnız değişen paragrafları ver**; değişmeyene dokunma. Değiştirdiğin paragrafı tam ver. Arapçayı değiştirdiysen
  tercümesini de değiştir (ikisi ayrı değişiklik); tercüme Arapçada olmayan cümle eklemez.
- Yazım kuralları yukarıdakilerin aynısı: işaretler (`[dil; 3]`, `[belâgat; kendi tespiti]`…), tırnak ve takdir,
  âyetin ve alıntıların harf harf aynı yazılışı. Tercüme paragrafını **"Yapay zekâ tercümesi:" olmadan** ver; program
  ekler. Blok alıntı paragrafını `> ` ile başlat.
- **Kaynak numaraları:** eski numaralar değişmez (taslağın kaynakçası aşağıda, kimlikleriyle). Yeni bir kaynağa
  dayanırsan numarasını **{sonraki}**'den sürdür; düzeltmeyi bitirince yalnız yeni kaynaklarla ilgili eklentinin
  `cite` aracını `first` ile çağır (eklenti başına bir çağrı, numaralar art arda) ve döndürdüğü kaynakça satırlarını
  `kaynaklar_ek`'e olduğu gibi yaz. Kullanılmayan eski numara kalabilir.
- Tür `dogru` olan notlar korunacak yerleri gösterir: oraya dokunma. `ehline_sor` notları ehline bırakılır;
  düzeltme gerektirmez, anman gerekmez.
- **Her öbür not** ya bir değişikliğin `notlar` listesinde ya `reddedilen`de anılır.

Cevabın yalnız tek bir ```json kod bloğudur; önüne ve ardına bir şey yazma:

```json
{{
  "degisiklikler": [
    {{"islem": "degistir", "capa": "V2/ar/3", "metin": "paragrafın yeni hâli, tam", "notlar": ["{onek}4"]}},
    {{"islem": "sil", "capa": "V3/ar/7", "notlar": ["{onek}9"]}},
    {{"islem": "ekle", "sonra": "V2/tr/3", "bloklar": [{{"dil": "ar", "metin": "…"}}, {{"dil": "tr", "metin": "…"}}],
      "notlar": ["{onek}5"]}}
  ],
  "reddedilen": [{{"not": "{onek}7", "gerekce": "kısa gerekçe (taslakta nerede karşılandığı ya da neden haksız)"}}],
  "kaynaklar_ek": ["[{sonraki}] cite'ın döndürdüğü satır, olduğu gibi"],
  "ozet": "iki-üç cümle: neyi değiştirdin, neyi reddettin"
}}
```

Bir paragrafı silersen onun tercümesini de sil (ayrı değişiklik). `ekle` yeni paragraf çiftini `sonra`daki çapanın
ardına koyar (çapa düzeltmeden önceki taslağın çapasıdır).

# Taslak

{taslak}

# Eleştirmenin notları

{notlar}
