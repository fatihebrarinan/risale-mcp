<!--
D12.5 Tur 1'in yeni kolu (PLANLAR.md D12.5; plan `docs/d1/d12-rapor-ve-plan.md` 4.2'nin 1. ve 5. adımı): okumayı
yazımdan ayırmak ve kelime/hey'et çizelgesi. Sürümlüdür: her değişiklik aşağıdaki "Sürümler"e tarihiyle yazılır.

`scripts/d1-tur.py` iki istem kurar. Ortak kısımlar (taslağın adı, dili ve uzunluğu; usul; şablon; işaretler ve
tırnak) **taban hattın isteminden** (`hat-istemi.md`, h2) aynen alınır: iki kol arasındaki tek fark işin bölünmesi ve
çizelgedir.
- **Okuma** (araçlı, prova sunucuları): h2'nin görevi, me'hazı ve usulü + aşağıdaki "OKUMA" kısmı + Ek 1–3 (h2'ninkiler).
  Çıktı yalnız JSON çizelgedir. Program satırları denetler: âyetin her kelimesinin satırı var mı, satır boş mu
  (i'râbı yok ya da müfessir, tercih ve nükte alanlarının üçü de boş), müfessir kimliği ve alıntısı gerçek mi. Eksik
  ve boş satırlar bir kez "TAMAMLA" kısmıyla aynı oturumun araçlarıyla geri gönderilir.
- **Yazım** (yalnız `cite` açık): h2'nin görevi, usulü ve şablonu + aşağıdaki "YAZIM" kısmı + Ek 1, Ek 2 ve Ek 3
  olarak çizelge. Okumayı yazımdan ayırmanın gerekçesi: istem kuralı düşünmeyi değiştirmiyor, adımı programla
  zorlamak değiştiriyor (D8, D9); yazım araçsız ve kısa olunca maliyet düşer (D11).

Sürümler:
- c1 (2026-11-16, D12.5 Tur 1, Bakara 9–10).
-->

---- OKUMA ----

## Bu oturumun işi: okuma ve çizelge (taslağı henüz yazma)

Bu iş iki adımdır. **Şimdi yalnız okuyorsun.** İkinci adımda başka bir oturum, araçsız, yalnız senin çizelgenden
taslağı yazacak: **çizelgeye yazmadığın hiçbir şey taslağa giremez**, çizelgedeki her alıntı ve kimlik de taslağa
olduğu gibi geçer. Yukarıdaki taslak kuralları (uzunluk, usul, şablon) yazanın kurallarıdır; sen onlara bakarak neyin
gerekeceğini bil, ama uzunluk sınırı çizelgeye yoktur: yazan seçecek.

Çizelge âyetin **her kelimesi için bir satırdır**, harfler dahil: kelimeye bitişik harf (و، ف، ب، ل، ك، س) ve
harf-i tarif satırın `harfler` alanında, kendi başına duran harf ve edat (إنّ، إذا، ما، لا، في، مِن، إلّا، ثمّ…)
kendi satırında. Her satırda sor: i'râbı ne; neden bu sîga, bu ta'rif ya da tenkir, bu takdim ya da te'hir; neden bu
lafız, şu değil; müfessirler burada ne diyor (kimliği ve sözüyle); sen burada bir nükte görüyor musun. Bir satırda
söyleyecek bir şey bulamadıysan bunu da yaz (`bos_gerekce`): satırı atlama.

Satırlardan sonra cümle düzeyine çık: âyetin cümleleri, her cümlenin hey'eti (ismiye ya da fiiliye, haber ya da
inşâ, te'kid, hasr, fasıl ya da vasl, iltifat), cümleler arasında söylenmeyen (mukadder) soru ve cevaplar, âyetin
öncesiyle bağı, müfessirlerin ayrıldığı yerler.

### Alıntı ve kimlik

- `soz` alanı araçların ya da kaynak dosyasının döndürdüğü metnin **harfi harfine** bir parçasıdır (bir iki
  cümleden uzun olmasın); `kimlik` o cümlenin ya da aralığın kimliğidir (`beyzavi/2/9/c004`,
  `…/c004..c006`). Program her alıntıyı kimliğinin metninde arar.
- Kendi sözün (`nukte_adayi`, `ozet`, `takdir`) alıntı değildir; Türkçe yaz, kısa yaz.

### Çıktı

Cevabın yalnız tek bir ```json kod bloğudur:

```json
{{
  "kelimeler": [
    {{"no": "K1", "ayet": 9, "cumle": "C1", "lafiz": "يُخَادِعُونَ",
      "harfler": [{{"harf": "…", "islev": "…"}}],
      "irab": "…", "siga": "…", "tarif_tenkir": "…", "takdim_tehir": "…", "tercih": "neden bu lafız, şu değil (yoksa boş)",
      "mufessirler": [{{"kimlik": "…/c004", "soz": "…", "ozet": "bu sözün buradaki işi, Türkçe bir cümle"}}],
      "nukte_adayi": "senin gördüğün nükte, Türkçe (yoksa boş)", "bos_gerekce": "yalnız satır boşsa: neden"}}
  ],
  "cumleler": [
    {{"no": "C1", "lafiz": "…", "heyet": "…", "mukadder": "cümleden sonra dinleyenin zihnindeki soru ya da takdir (yoksa boş)",
      "mufessirler": [{{"kimlik": "…", "soz": "…", "ozet": "…"}}]}}
  ],
  "onceki": [{{"bag": "âyetin öncesiyle bir bağı", "mufessirler": [{{"kimlik": "…", "soz": "…", "ozet": "…"}}]}}],
  "maksat": "âyetin asıl maksadı, bir iki cümle",
  "mukaddime": "gerekli mi, neden (usul 3)",
  "ayrilik": [{{"yer": "lafız ya da cümle", "gorusler": [{{"kimlik": "…", "soz": "…", "ozet": "…"}}], "not": "her görüş hangi itibarla doğru"}}],
  "isarat_nazir": [{{"kimlik": "İşârât'ın öbür bir biriminde aynı yapının işlendiği yer", "soz": "…", "ozet": "…"}}]
}}
```

## Çalışma sırası

1. Ek 1'i, Ek 2'yi ve Ek 3'ü (kaynak dosyası) oku.
2. İşârât'ın aynı türden bir iki birimini `risale` eklentisinde `read_section` ile oku (kimlikleri Ek 2'de); bir
   edatın ya da üslûbun kaidesine dayanacaksan onu İşârât'ın kendisinde ara (`search`, `semantic_search`,
   `work: "isaratul-icaz-arabi"`). Dosyada olmayan bir müfessiri ya da Risale bölümünü gerekirse oku. Bir belâgat
   teriminin tanımını terim eserinde gör.
3. Âyetin kelimelerini sırayla çizelgeye geçir; her satırda kaynakları aç, söyleneni kimliğiyle ve sözüyle yaz.
4. Cümle düzeyini, öncesiyle bağı, maksadı ve ayrılıkları yaz.
5. Öz denetim: âyetin her kelimesinin satırı var mı; her `soz` araçların döndürdüğü metin mi; kimlikler doğru mu.

---- TAMAMLA ----

# Çizelgenin eksikleri

Çizelgeni program denetledi. Aşağıdaki satırlar eksik ya da boş, ya da alıntıları kimliklerinin metninde bulunamadı.
Gerekirse kaynakları yeniden aç ve **yalnız bu satırları** düzelterek ya da yazarak ver; öbür satırlara dokunma.
Cevabın yalnız tek bir ```json kod bloğudur: `{{"kelimeler": [ … ]}}` (satır biçimi öncekinin aynısı; düzelttiğin
satır aynı `no`yu taşır, yeni satır yeni `no` alır).

{eksikler}

---- YAZIM ----

## Bu oturumun işi: çizelgeden yazım

Bu âyetlerin okuması yapıldı: Ek 3'teki **okuma çizelgesi**, önceki bir oturumun araçlarla kaynakları okuyarak
çıkardığıdır. Âyetin her kelimesi için bir satır (i'râb, harfler, sîga, ta'rif-tenkir, takdim-te'hir, tercih,
müfessirlerin sözü kimliğiyle, nükte adayı), cümle düzeyi, öncesiyle bağ, maksat ve müfessirlerin ayrıldığı yerler.

- **Senin elinde okuma aracı yok;** yalnız eklentilerin `cite` aracı açık (kaynakça ve alıntı denetimi için).
  Taslağı çizelgeden yaz: bir kaynağa ancak çizelgede kimliği ve sözü varsa dayan, alıntıyı ancak çizelgenin `soz`
  alanından (harfi harfine ya da bir parçası) al. Çizelgede olmayan bir kaynak ya da söz yazma.
- Çizelge hammaddedir, taslak değildir: her satırı yazmak zorunda değilsin. Uzunluk hedefine uy; asıl maksada hizmet
  edeni ve gerekçesi olanı seç; aynı nükteyi iki kez söyleme.
- Çizelgenin `nukte_adayi` ve `ozet` alanları okuyanın kendi sözüdür; taslakta kaynağın sözü gibi gösterme.
- Âyetin metni ve atfı Ek 3'ün başında; `## Âyet` bölümüne onu yaz, kaynakçaya âyet atfıyla ("Bakara Sûresi, 2:9")
  kendin ekle.

## Çalışma sırası

1. Ek 1'i, Ek 2'yi ve Ek 3'ü (okuma çizelgesi) oku.
2. Yazmadan önce kendin için çıkar: âyetin cümleleri, asıl maksadı, öncesiyle bağı, mukaddime gerekip gerekmediği,
   üslûbun beklenenden ayrıldığı yerler, müfessirlerin ayrıldığı yerler (çizelgede hepsinin satırı var).
3. Taslağı yaz (şablon yukarıda), uzunluk hedefine uyarak.
4. Öz denetim: tırnak içindeki her söz çizelgenin `soz` alanında mı? "Kendi tespiti" dediğin söz çizelgede bir
   müfessire mal edilmiş mi? İnhisar kalıplarını kaynak mı söylüyor? Arapça uzunluk hedefte mi?
5. Her eklentinin `cite` aracını, dayandığın ve alıntıladığın her cümle ya da aralıkla (çizelgenin kimlikleri) bir kez
   çağır; işaret ettiği sorunları düzelt. Tek "Kaynaklar" listesi ver (eklentiler sırayla: `first` ile numara sürer).
