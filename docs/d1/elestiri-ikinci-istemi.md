<!--
D12.5 D turu: düzeltmenin ikinci sürümünün (d2) ikinci kapalı kitap eleştirisi (PLANLAR.md D12.5; plan belgesi 4.5
"D"). Sürümlüdür: her değişiklik aşağıdaki "Sürümler"e tarihiyle yazılır. `scripts/d1-duzelt.py ikinci` bu dosyanın
"---- IKINCI ----" bölümünü alır, {yer tutucuları} doldurur ve en sona usul özetinin 2–5. bölümlerini koyar (prova
kopyası). Model `claude -p` ile, yerleşik araçlar ve web kapalı, **prova sunucularıyla** alır (İşârât'ın sınanan
birimi gizli, öbür her şey açık): kapalı kitap eleştirmenin (`elestiri-kapali-istemi.md`) şartıyla.

Neden (kullanıcının kararı, 2026-11-16; D12.3'ün okumasından): kapalı notlarla düzeltme işe yarıyor (kesin
tercihlerin 6/7'si düzeltilmiş taslak), ama yan etkileri var: uzama (Arapça +%28), düşen fikir, belirsiz gönderme
("şarttaki", "onda") ve kendi sözün yerine nakil ("alıntı yağmuru"; T1'de de). İkinci eleştiri yalnız düzeltilen
paragraflara bakar ve yalnız bu yan etkileri arar; notları aynı düzeltme istemiyle (d1) ikinci geçişe gider.

Sürümler:
- i1 (2026-11-17): ilk sürüm; D turu, 9–10 taslak 1'in düzeltmesi.
-->

---- IKINCI ----

# Bağlam

Bediüzzaman Said Nursî İşârâtü'l-İ'câz'ı Arapça yazdı; Türkçe tercümesi kardeşi Abdülmecid Nursî'nindir. Bir yapay
zekâ, İşârât'ın usulüyle {sura_name} {ayahs}. âyetler için bir "yapay zekâ taslağı" yazdı (tefsir değildir; ileride
ehli okuyacak). Bir eleştirmen taslağa notlar yazdı; yazar notlarla taslağı **düzeltti**. Aşağıda yalnız düzeltmenin
değiştirdiği yerler var: her yerde **önceki hâl**, **düzeltilmiş hâl** ve düzeltmenin karşıladığı notlar.

Sen **ikinci eleştirmensin**. Notların aynı yazara ikinci bir düzeltme için gidecek. İşin dar: düzeltmenin **yan
etkilerini** bulmak. Notların karşılanıp karşılanmadığını ya da taslağın öbür yerlerini yeniden eleştirme; ilk
eleştiri yapıldı. İşârât'ın bu âyetlerdeki kısmı ne yazarda ne sende var (eklentilerden çıkarıldı); ölçün İşârât'ın
usulü (en sondaki özet), Arap dili ve belâgat ve kaynakların ne dediği. Taslağın dayandığı kaynakları gerektiğinde aç.

# Dört soru (her düzeltilmiş yer için)

1. **Düşen fikir** (tür `dusen_fikir`): önceki hâlde doğru, usule uygun bir fikir, takdir, temsil ya da nükte vardı
   ve düzeltilmiş hâlde, hiçbir not bunu istemediği hâlde, düştü mü? Düştüyse neyin düştüğünü önceki hâlden kısa
   alıntıyla göster; öneri: onu geri getir (gerekirse ihtimal diliyle).
2. **Belirsiz gönderme** (tür `belirsiz_gonderme`): düzeltilmiş hâlde "bu", "onda", "şarttaki", "yukarıda geçen",
   "o söz" gibi gönderme paragraf tek başına okununca neyi kastettiği açık olmayan bir yere mi bakıyor? Öneri: göndermeyi
   açık söyle.
3. **Kendi sözün yerine nakil** (tür `nakil`): düzeltme, önceki hâlde taslağın **kendi istinbatı** olan bir nükteyi
   (âyetin lafzından, hey'etinden, makamından çıkarılmış) bir müfessirin sözünün ya da uzun bir alıntının arkasına mı
   itti; ya da nükteyi taşımayan alıntılar mı ekledi? İşârât'ın usulünde nükte müellifin kendi sözüyle söylenir;
   kaynak, varsa, dayanak olarak kısaca anılır. Öneri: istinbatı kendi sözüyle geri koy (gerekirse `[… kendi tespiti]`
   ile), alıntıyı kısalt ya da çıkar, kaynağı dayanak olarak bırak.
4. **Îcâz** (tür `icaz`): düzeltilmiş hâl notun gerektirdiğinden belirgin biçimde uzun mu (aynı şeyi iki kez söylemek,
   gereksiz nakil, açıklamanın açıklaması)? Öneri: hangi cümlenin kısalacağını ya da düşeceğini söyle.

Düzeltmenin iyi yaptığı ve ikinci düzeltmede korunması gereken bir yeri de söyleyebilirsin (tür `dogru`).
Bir yerde yan etki yoksa not yazma. **Notların az ve kesin olsun**: her not tek bir yan etki, tek bir yapılacak iş.

Cevabın yalnız tek bir ```json kod bloğudur; önüne ve ardına bir şey yazma:

```json
{{
  "notlar": [
    {{"capa": "V3/ar/14", "tur": "nakil", "oncelik": "yuksek",
      "taslak_alinti": "düzeltilmiş hâlden kısa ve harf harf alıntı",
      "onceki_alinti": "gerekirse önceki hâlden kısa ve harf harf alıntı",
      "metin": "yan etki ne", "oneri": "yazara yapılacak iş", "dayanak": ["gerekirse kaynak kimliği"]}}
  ],
  "ozet": "iki-üç cümle: düzeltmenin yan etkileri genel olarak ne"
}}
```

`capa` düzeltilmiş hâlin çapasıdır (aşağıda her yerin başında yazılı). `oncelik`: `yuksek`, `orta`, `dusuk`.

# Düzeltmenin değiştirdiği yerler

{yerler}
