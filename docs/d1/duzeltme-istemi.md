<!--
D12 düzeltme isteminin görev kısmı (PLANLAR.md D12). Sürümlüdür: her değişiklik aşağıdaki "Sürümler"e tarihiyle
yazılır. `scripts/d1-duzelt.py duzelt` taslağı yazan istemin **aynısını** (Ek 1–3 dahil; `istem-hat-h1.md`) başa koyar,
ardından bu dosyanın "---- DUZELTME ----" bölümünü {yer tutucuları} doldurarak ekler. Model aynı yazardır (Opus 5.5,
yüksek), aynı prova sunucularıyla (İşârât'ın sınanan birimi gizli); asıl oturumu görmez, taslağı ve notları görür.

Kararlar (kullanıcı, 2026-11-16): baştan yazdırma yerine düzeltme, yalnız değişen paragraflar; yazar bir notu
gerekçesiyle reddedebilir (retler notların kalitesini de ölçer); her not ya bir değişiklikte ya retlerde anılır.

Sürümler:
- d1 (2026-11-16): ilk sürüm; D12.1, 31–33 taslak 7 (kapalı ve açık kitap notlarıyla).
- d2 (2026-11-20, D5.0.6 kalite kapısı): uzunluk hedefi İşârât'tan gelmez (h9'da hedef yok): Arapça toplamı şimdiki
  uzunluğun en çok %10 üstüne çıkar ({en_cok} harf); notlar kalite kapısınındır (kapalı eleştirmen, nisbet denetçisi,
  biçim denetimi). `{en_az}` kullanılmaz.
- d3 (2026-11-21, kullanıcının kararı): d2'nin sınamasında düzeltme eski nisbet hatalarının hepsini giderdi ama
  eklediği yeni kaynaklar yeni hata getirdi, "eksik" notlarını karşılamak hükmü değiştirmedi. Düzeltme **yeni kaynak
  getirmez** (`cite` yok, yeni numara yok; program yeni numaralı değişikliği uygulamaz); kapalı eleştirmenin "eksik"
  notları düzeltmeye girmez (okuma sayfasında not olarak kalır). Düzeltmenin değiştirdiği sözlerde nisbet denetçisi
  hata bulursa yalnız onlarla ikinci, küçük bir tur (`kapi2`).
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
  iddiayı ihtimal diliyle söylemek ya da çıkarmaktır. Taslak şu an {simdi} harf; Arapça paragrafların toplamı en çok
  {en_cok} harfe çıkabilir (şimdikinin %10 fazlası). Bir nükte eklerken başka bir yerde kısalt.
- **Yalnız değişen paragrafları ver**; değişmeyene dokunma. Değiştirdiğin paragrafı tam ver. Arapçayı değiştirdiysen
  tercümesini de değiştir (ikisi ayrı değişiklik); tercüme Arapçada olmayan cümle eklemez.
- Yazım kuralları yukarıdakilerin aynısı: işaretler (`[dil; 3]`, `[belâgat; kendi tespiti]`…), tırnak ve takdir,
  âyetin ve alıntıların harf harf aynı yazılışı. Tercüme paragrafını **"Yapay zekâ tercümesi:" olmadan** ver; program
  ekler. Blok alıntı paragrafını `> ` ile başlat.
- **Yeni kaynak getirme.** Düzeltme yanlışı düzeltir, kaynağın sözünü aşan iddiayı kaynağın dediğine indirir ya da
  kendi tespitin, ihtimal olarak işaretler, dayanaksız sözü siler. Kaynak numaraları değişmez (taslağın kaynakçası
  aşağıda, kimlikleriyle); yeni numara açma, `cite` çağırma, `kaynaklar_ek` boş kalır. Bir notu karşılamak yeni bir
  nakil gerektiriyorsa onu `reddedilen`e "yeni kaynak gerekir" gerekçesiyle yaz. Kaynağı yeniden okumak serbesttir
  (nisbeti düzeltmek için); yeni bir kaynaktan nakil eklemek değil.
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
