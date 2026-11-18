<!--
D14.7 (h10) taslak istemine giren tarama parçaları (PLANLAR.md D14.7; kullanıcı onayladı, 2026-11-18). `scripts/d1-hat.py
hazirla <birim> --tarama` her "---- ad ----" bölümünü `docs/d1/hat-istemi.md`'deki aynı adlı yer tutucuya koyar
(h9'da hepsi boş ya da h9 metni). {tablo}: `scripts/d1-kalip.py tablo <birim>`'in kurduğu tarama tablosu.

Sürümler:
- t1 (2026-11-18): ilk sürüm.
-->

---- tarama_usul ----
 Bakılacak yerlerin bir kısmını program **tarama tablosunda** önceden çıkardı (aşağıda, "Tarama"); tablo bir taban,
   tavan değil.
---- tarama_bolum ----
## Tarama (İşârât'ın soru kalıpları)

İşârât bir âyetin nazmını işlerken her birimde aynı türden soruları sorar: "fiil neden meçhul?", "âyet neden bu
kelimeyle bitti?", "neden vâv ile atfedilmedi?", "neden isim cümlesi?". Bu soruların kalıpları, İşârât'ın onlara
verdiği cevap türleri, örnekleri ve her birinin "dikkat" notu **Ek 5**'tedir.

Program bu âyetlerin lafızlarına sorulabilecek kalıpları aşağıdaki tabloda çıkardı (âyetin metninden; İşârât'tan
değil). Taslağı yazmadan önce tabloyu cevabının başında doldur:

- **Her satıra cevap ver:** **taşıyor** (lafız bu soruya bir nükte veriyor: nükteyi bir cümleyle yaz) ya da
  **taşımıyor** (yarım cümle gerekçe).
- **"Taşımıyor" meşrudur:** Ek 5'teki dikkat notu uyuyorsa, yani soru burada boşa soruluyorsa, doğru cevap odur.
  Lafzın taşımadığı nükteyi uydurma.
- **"Taşıyor" dediğin her nükteyi taslakta yerinde aç:** kelime ve cümle kalıpları üçüncü vecihte, cümleler arası
  kalıplar ikinci vecihte (öncesiyle bağsa birinci vecihte), âyetin bütününe dair olanı yerine göre. Ek 5'teki cevap
  türleri dağarcıktır, sınır değil.
- **Tablo bir taban, tavan değil:** tabloda olmayan bir nükteyi de yaz.
- Tarama **Türkçe ve kısa**dır: satır başına bir cümle. Taslağın usulü, me'hazı ve dersleri yukarıdaki gibidir.

{tablo}

---- tarama_adim ----
Tarama'yı doldur (tablo yukarıda; cevabının başında). 
---- tarama_denetim ----
 Tarama'da "taşıyor" dediğin her nükte taslakta yerinde açıldı mı?
---- cevap ----
Cevabın önce `## Tarama` bölümü, sonra taslaktır; önüne ve ardına başka açıklama yazma. Program Tarama'yı taslaktan
ayırır; okuyucu yalnız taslağı görür.
---- tarama_baslik ----
## Tarama
- T01 «…» · kalıp — taşıyor: (nükte, bir cümle)
- T02 «…» · kalıp — taşımıyor: (gerekçe, yarım cümle)
  (tablonun her satırı için, sırayla)

