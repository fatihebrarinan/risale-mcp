<!--
D12 kör ölçünün istemi (PLANLAR.md D12, "Ölçü"). Sürümlüdür: her değişiklik aşağıdaki "Sürümler"e tarihiyle yazılır.
`scripts/d1-duzelt.py olc` "---- OLCU ----" bölümünü alır, {yer tutucuları} doldurur. Model istemi `claude -p` ile,
yerleşik araçlar ve web kapalı, **yayındaki** sunucularla alır (açık kitap: İşârât'ın bu birimi okunabilir).

Kararlar (kullanıcı, 2026-11-16): eleştirmen asıl ölçüdür ama kör okur: notları yazandan ayrı, yeni bir sohbet;
hangi taslağın düzeltildiğini bilmez, "A" ve "B" diye görür, sıra karışık (programın sabit tohumuyla). Bütün olarak
okur (A/B bütünü tartar, ucuz). Taslakların istem, model ve düzeltme bilgisi verilmez.

Sürümler:
- o1 (2026-11-16): ilk sürüm; D12.1, 31–33.
- o2 (2026-11-16, D12.5 Tur 0): takdir işareti «…» (h2'den beri) 3. ölçüde açıklandı.
- o3 (2026-11-17, D13; kullanıcının kararı): yeni 3. ölçü "me'haz ve Risale-i Nur'un çizgisi" ve sonuçta ayrı hükmü
  (`mehaz`); "istinbat" etiketi (h3'ten beri) kaynak disiplininde açıklandı. İki kola birden uygulanır; o2'nin
  sayılarıyla doğrudan karşılaştırılmaz.
-->

---- OLCU ----

# Bağlam

Bediüzzaman Said Nursî İşârâtü'l-İ'câz'ı Arapça yazdı; Türkçe tercümesi kardeşi Abdülmecid Nursî'nindir. Eser âyet
gruplarını çoğunlukla üç vecihle işler: **birinci vecih** âyetin öncesiyle nazmı, **ikinci vecih** âyetin cümlelerinin
(açık ve mukadder) birbiriyle nazmı, **üçüncü vecih** her cümlenin hey'etleri, kayıtları ve kelimeleri.

Bir prova yürütülüyor: yapay zekâdan, İşârât'ın {sura_name} {ayahs}. âyetlerdeki kısmı ondan saklanarak, İşârât'ın
usulüyle "yapay zekâ taslağı" yazması istendi. Aşağıda böyle iki taslak var: **A** ve **B**. Hangisinin nasıl
yazıldığını bilmiyorsun ve bilmen gerekmiyor; yalnız metinlerine bak.

Senden saklanan bir şey yok: İşârât'ın bu âyetlerdeki kısmını `risale` eklentisinde oku: Arapça aslı
`read_section("{gizli_ar}")`, Abdülmecid Nursî tercümesi `read_section("{gizli_tr}")`. Taslakların dayandığı
kaynakları gerektikçe eklentilerde aç.

# Soru

Her bölüm için (Mukaddime, birinci, ikinci, üçüncü vecih; taslaklardan birinde olmayan bölüm de tartılır) ve bütün
olarak: **hangi taslak daha iyi?** Şu ölçülerle, bu sırayla:

1. **Doğruluk:** yanlış, uydurma, İşârât'la çelişki, kaynağa yanlış nisbet, kapsamı aşan hüküm daha az olan.
2. **İşârât'a yakınlık:** İşârât'ın nüktelerini ve oraya vardığı yolu (takdir zinciri, mukadder sual, kayıtların
   eşlenmesi, garaza akış) daha çok yakalayan.
3. **Me'haz ve Risale-i Nur'un çizgisi:** müellif İşârât'ı ve Risale-i Nur'u bu işe me'haz diye gösterdi. Taslak
   usulü ve nazîri İşârât'tan, mânâyı ve dersi Risale-i Nur'dan alıyor mu; Risale-i Nur'un bu âyetlerin konusundaki
   dersine dayanıyor mu (gerekirse `risale` eklentisinde `semantic_search` ile bak); yoksa nükteleri müfessirlerin
   sözleri üzerinden mi kuruyor (müfessirleri adıyla sayıp aktarmak)? İşârât müfessirleri çok az anar (cümlelerinin
   %1,3'ünde bir kaynak adı geçer); nükteleri büyük çoğunlukla müellifin istinbatıdır.
4. **Kaynak disiplini:** tırnak, işaret ("kendi tespiti" ya da "istinbat": âyetin lafzından, hey'etinden ve usulden
   yazarın vardığı nükte; bir müfessirde de bulunması onu nakil yapmaz) ve numaralar yerinde olan; bir kaynağa onun
   kendi görüşü olmayanın (naklettiği, itiraz ettiği ya da reddettiği vechin) mal edilmemesi. Taslaklarda Türkçe «…» **takdir ve beklenen söz** işaretidir (dinleyenin mukadder sorusu, takdir edilen cümle, makamın beklediği ifade): yazarın kendi sözüdür, kaynak iddia etmez; "…" ve “…” kaynağın sözüdür.
5. **Îcâz:** aynı şeyi daha az sözle söyleyen; nükteyi gerekçesiyle veren.

Taslaklar birbirine çok benzeyebilir; o zaman farkın bulunduğu yerlere bak. Fark tercih gerektirmeyecek kadar
küçükse `esit` de. Uzun olanı uzun diye, kısa olanı kısa diye tercih etme.

# Kurallar

- Her hüküm okuduğun metne dayanır; İşârât'ın ne dediğini yalnız bu oturumda okuduğundan söyle, dayandığın İşârât
  cümlelerinin kimliklerini yaz.
- Gerekçe iki taslaktan çapalarla (`A:V2/tr/3`, `B:V3/ar/5`) ve kısa (en çok dört cümle).
- Cevabın yalnız tek bir ```json kod bloğudur:

```json
{{
  "bolumler": [
    {{"bolum": "Mukaddime | V1 | V2 | V3", "tercih": "A | B | esit", "guc": "acik | hafif", "gerekce": "…",
      "dayanak": ["isaratul-icaz-arabi/…/c010"]}}
  ],
  "butun": {{"tercih": "A | B | esit", "guc": "acik | hafif", "gerekce": "üç-beş cümle"}},
  "mehaz": {{"tercih": "A | B | esit", "guc": "acik | hafif", "gerekce": "yalnız 3. ölçüye göre, iki-dört cümle, çapalarla"}},
  "yalniz_A_kusurlari": ["A'da olup B'de olmayan en önemli en çok üç kusur, çapasıyla"],
  "yalniz_B_kusurlari": ["B'de olup A'da olmayan en önemli en çok üç kusur, çapasıyla"]
}}
```

# Taslak A

{taslak_a}

# Taslak B

{taslak_b}
