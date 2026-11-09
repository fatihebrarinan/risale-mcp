# Yenilikler yazma kılavuzu

Sitedeki Yenilikler yazıları (`docs/yenilikler/`, `scripts/site-uret.py`) bu kılavuza göre yazılır. Kurallar
kullanıcının isteğidir (2026-11-09); yeni bir istek gelince buraya eklenir.

## Kime yazıyoruz

Okuyan, eklentiyi kullanan ya da kullanacak kişidir: Risale-i Nur okuyan, ders hazırlayan, merak eden biri. Yazılımcı
değildir, projenin içini bilmez ve bilmesi de gerekmez. Yazı WhatsApp gruplarında paylaşılacak: telefonda, kısa bir
bakışta anlaşılmalı.

## Ton: onunla konuşur gibi

- Okuyana doğrudan "siz" diye seslenin, bir arkadaşa anlatır gibi sıcak ve sade yazın. Resmî duyuru dili
  kullanmayın.
- Cümleyi okuyanın gözünden kurun: "sizin", "sizin için", "artık şunu yapabilirsiniz".

| Böyle değil | Böyle |
|---|---|
| ChatGPT eklentinin talimatını eklendiği gün kaydediyor. | ChatGPT, eklentinizin talimatını sizin eklediğiniz gün hafızasına kaydediyor. |
| Râvi adıyla arama desteği eklendi. | Artık bir hadisi, onu rivayet eden sahâbînin adıyla da bulabilirsiniz. |
| Asistanın tercümeleri damgalanır. | Yapay zekâ bir metni sizin için tercüme ettiğinde bunu açıkça söyler: tercümenin başında "Yapay zekâ tercümesi" yazar. |

## Önce katkı

Her yazı, yeniliğin kullanıcıya ne kazandırdığıyla başlar. Okuyan ilk paragrafta "bu benim ne işime yarar" sorusunun
cevabını bulmalı. Ne yapıldığı, ardından gelir.

- Yeni bir eklenti ya da kitap: hangi kapıyı açtığı. Örneğin Hadis ve Tefsir eklentileri, Risale-i Nur'da geçen bir
  hadisin ya da âyetin izini asıl kaynaklarında sürmeyi, bir konuyu Risale-i Nur'dan hadis kitaplarına ve klasik
  tefsirlere uzanarak daha ayrıntılı öğrenmeyi, ders ve akademik çalışmalar için adresli bir zemin kurmayı mümkün
  kılar.
- Bir iyileştirme: cevaplarda neyin daha güvenilir ya da kolay olduğu. Örneğin "Artık neyin kitabın kendisi, neyin
  yapay zekânın çevirisi olduğunu her zaman bileceksiniz."
- Katkı abartılmaz: yalnız eklentinin gerçekten yaptığı söylenir. Yapay zekânın yazdığı şey "tefsir" ya da "hüküm"
  diye sunulmaz.

## Ne yazılır, ne yazılmaz

Yalnız kullanıcıyı ilgilendiren şey yazılır: artık ne yapabiliyor, ne değişti, bir şey yapması gerekiyor mu.

- **Yazılır:** yeni bir eklenti ya da kitap, yeni bir soru türü, cevaplarda okuyanın fark edeceği bir değişiklik,
  kullanıcının yapması gereken bir şey (yenileme gibi).
- **Yazılmaz:** içerideki düzeltmeler ve teknik ayrıntılar. Örnekler: "ibn" ile "bin"in aramada aynı sayılması,
  veritabanı, dizin, sürüm, sunucu, araç adları (`search_hadith`, `cite`), profil, vektör, deploy.
- Bir düzeltme kullanıcıya bir fayda olarak yansıyorsa, faydasıyla yazılır. "Alıntı denetimi eklendi" değil, "Yapay
  zekâ bir hadisten söz aktarırken artık o sözün rivayette gerçekten geçtiğine bakıyor."

## Basit anlatın, örnek verin

- Her yenilik için mümkünse bir örnek soru verin: okuyan onu kopyalayıp hemen deneyebilsin. Örnek soru alıntı
  bloğunda durur:

  > Nevvâs b. Sem'ân'ın rivayet ettiği Deccâl hadisini bul.

- Örnek soruyu yazmadan önce eklentide deneyin; çalışmayan örnek yazılmaz.
- Bir terim gerekiyorsa (senet, künye, müfessir) ilk geçtiği yerde kısaca açıklayın: "senet, yani hadisi nakledenlerin
  zinciri".
- Rakamlar yuvarlak ve anlaşılır olsun: "yaklaşık 169 bin hadis". İç sayımlar ("%0,9'u") yazılmaz.

## Kelimeler

- **Eklenti** denir, "bağdaştırıcı", "MCP sunucusu", "konektör" denmez. İnsanlar bu kelimeyi tanıyor.
  - Bir uygulamanın menüsünü tarif ederken menünün kendi adı yazılır, çünkü okuyan onu ekranda arayacak:
    "Claude'da Özelleştirme › Bağdaştırıcılar". Gerekirse açıklayın: "Claude eklentilere 'bağdaştırıcı' diyor."
- Eklentilerin adları: Risale-i Nur eklentisi, Hadis eklentisi, Tefsir eklentisi.
- "Yapay zekâ" ya da uygulamanın adı (Claude, ChatGPT) denir; "asistan", "model" denmez.
- Projenin kendi kurallarındaki iki ayrım okuyana da doğru aktarılır, ama sade dille:
  - Yapay zekânın yazdığı hiçbir şey "tefsir" diye anılmaz; tefsir müfessirin eseridir.
  - Eklenti bir hadise "sahih" ya da "zayıf" demez; âlimlerin hükmünü âlimin adıyla gösterir.

## Yazım ve noktalama

- **Devrik cümle kurulmaz.** Yüklem cümlenin sonundadır. "Geldi iki yeni eklenti" değil, "İki yeni eklenti geldi".
  "Bilmenizi isteriz bir şeyi" değil, "Bir şeyi bilmenizi isteriz".

Türk Dil Kurumunun yazım kurallarına uyulur. Özellikle:

- **Virgül:** "ve", "ile", "veya", "ya da" bağlaçlarından önce virgül konmaz. Uzun cümlede özneden sonra
  okumayı kolaylaştırmak için konur ("ChatGPT, eklentinizin talimatını…"). "Örneğin", "Ayrıca", "Yani" gibi başlangıç
  sözlerinden sonra konur.
- **Noktalı virgül:** az kullanılır. Bir cümlede iki ayrı düşünce varsa iki cümle yazın. Noktalı virgül yalnız
  içinde virgül olan sıralamaları ayırmak için.
- **İki nokta:** ardından açıklama ya da örnek gelir; cümle değilse küçük harfle başlar.
- **Bitişik ve ayrı yazılanlar:** bağlaç olan "de/da", "ki", soru eki "mı/mi" ayrı yazılır.
- **Kesme işareti:** özel adlara gelen ekler ayrılır: ChatGPT'de, Claude'a, Buhârî'nin.
- **Şapka:** sitenin yazımı sürer: "yapay zekâ", eser ve müellif adları sitedeki gibi (Beyzâvî, İşârâtü'l-İ'câz).
- Tırnak içindeki örnek sözler çift tırnakla: "Yapay zekâ tercümesi".

## Yazının yapısı

1. **Başlık:** haberi söyler, kısa: "Hadis ve Tefsir eklentileri açıldı".
2. **Giriş:** önce okuyana ne kazandırdığı ("Önce katkı"), sonra ne olduğu; iki üç cümle.
3. **Yenilikler:** her biri kısa bir başlık ya da madde, ardından ne işe yaradığı ve örnek soru.
4. **Sizin yapmanız gereken** (varsa): adım adım, menü adlarıyla.
5. **Kapanış:** nereden eklenir ya da nereden okunur (site sayfasına bağlantı).

Uzunluk: telefonda iki üç kaydırmada biter, yaklaşık 150–350 kelime.

## Üst bilgi

```
---
baslik: Hadis ve Tefsir eklentileri açıldı
tarih: 2026-11-07
ozet: Dizinde ve WhatsApp önizlemesinde görünen tek cümle.
whatsapp: |
  Gruba atılacak metin: iki üç satır, aynı sıcak tonla.
  Sonuna yazının adresi betikle eklenir, buraya yazılmaz.
---
```

- `ozet` tek cümledir ve kendi başına anlaşılır.
- `whatsapp` metni yazıyı okumayan birinin de anlayacağı kadar açıktır: ne yeni, kime yarar.

## Yazdıktan sonra

1. `python3 scripts/site-uret.py`, sonra `python3 -m http.server -d site 8080` ile
   `http://localhost:8080/yenilikler.html` adresinde bakın.
2. Kontrol: ilk paragraf katkıyı söylüyor mu, kılavuzdaki kelimeler (eklenti), yalnız kullanıcıyı ilgilendirenler,
   her örnek soru denenmiş, devrik cümle yok, noktalama.
3. Kullanıcı okuyup onaylar; yayın `scripts/deploy.sh --code`.
