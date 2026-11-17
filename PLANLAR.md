# Planlar

Projenin bütün planları, sırası, bekleyen ve dondurulan işleri ve adım kaydı bu belgededir (kullanıcının kararı,
2026-11-09). Kurallar:

- Yeni plan, karar ve biten adım buraya, tarihli yazılır. CLAUDE.md yalnız kalıcı bağlamı tutar (ilke, veri modeli,
  komut, kural). Bir adımın kalıcı bir altyapısı çıkarsa onun kısa tarifi CLAUDE.md'ye de girer.
- Bir işin ayrıntılı planı gerekirse `docs/` altında ayrı belge olabilir, ama durumu ve sırası burada tutulur.
  `docs/` altındaki eski plan belgeleri (`tefsir-altyapi-plani.md`, `tefsir-pilot-degerlendirme.md`,
  `tercume-programi.md`, `mvp-kitaplar.md`, `bag-altyapisi-plani.md`, `hadis-plani.md`…) ayrıntı ve geçmiştir.
- İşler kimlikle anılır ("Adlandırma"). Biten iş **aynı değişiklikte** "Biten" bölümüne tek satır olarak taşınır,
  ayrıntısı "Kayıt › Kimlikli işler"e ya da belgesine gider; "Sıradaki"de yalnız tablodaki işlerin ayrıntısı durur.
  `tests/test_planlar.py` bunu denetler (ayrıntısı tabloda olmayan iş, hem "Biten"de hem "Sıradaki"de duran iş,
  "Son verilen kimlikler"i aşan kimlik).

## Yön (kullanıcının kararları, 2026-11-09)

MVP bitti (2026-11-07): risale, hadis ve tefsir bağdaştırıcıları yayında, cevapların doğruluğu iyi. Sonraki yol
konuşuldu:

1. **Okumayla kurulan ve denetlenen bağlar donduruldu.** Geri dönüt: bağdaştırıcıyı kullanan model, eserler
   arasındaki ilişkiyi metin önündeyken sohbet sırasında zaten kuruyor; bu MCP'lerin varlık sebebi de bu. İlişkiyi
   önceden kaydetmek ancak onu denetleyecek bir heyet varsa değer taşır, o heyet yok. Mekanik bağlar (âyet birimi,
   tefsirdeki Kur'ân alıntısı, Risale'nin hadislerinin lafzı, âyet ilişkileri) birer dizindir, model onları sohbette
   kuramaz: kalır ve yenilenir.
2. **Tercüme programı donduruldu.** İzinler parça parça gelir, her tercüme ayrıştırma, hizalama ve kaynak ister;
   emeğin karşılığı az. Modelin tercümesi "Yapay zekâ tercümesi" damgasıyla verilir (bugünkü kural). Talimata
   "tercümeyi internette ara" konmaz (web'den gelen söz kütüphanenin bulgusu gibi sunuluyordu, 2026-11-09 10.59
   sohbeti); kullanıcı yayımlanmış tercümeyi açıkça sorarsa model web'e bakabilir, bulduğunu yayıncısıyla ve
   Kaynaklar'ın dışında verir. Diyanet izin vermedi (2026-11-12, "Bekleyen"den kapandı): Kur'an Yolu yok, Diyanet İşleri meali
   çıkarıldı (B6); Elmalılı asıl metninden (E6).
3. **Planlar tek belgede:** bu belge.
4. **Eser ekleme ölçütü** (aşağıda E2): her tavsiye edilen eser eklenmez; ölçütle seçilir.
5. **Kendi model ve üyelik:** konuşuldu, karar yok (aşağıda "Fikirler").

## Adlandırma (kullanıcının kararı, 2026-11-09)

Her iş bir **kimlik** alır: alan harfi ve o alanda artan numara (`E2`), alt adım noktayla (`E2.1`). Kimlik verilince
değişmez, biten ya da bırakılan işin kimliği yeniden kullanılmaz. **Sıra** ayrıdır: aşağıdaki tablonun satır
sırasıdır; sıra değişince yalnız satırlar yer değiştirir. Eski adlar (Aşama 20, HA7, Y1.1…) "Eski adı" sütununda
durur, "Kayıt"taki geçmiş onlarla okunur.

| Harf | Alan |
|---|---|
| **E** | Eserler: listeler, ekleme, nüsha |
| **S** | Sunum ve erişim: site, yenilikler, dizinler, yeni platformlar |
| **A** | Araç ve veri: Risale tarafındaki yetenekler |
| **D** | Deneme ve araştırma |
| **B** | Bakım: kontrol ve küçük açıklar |

Son verilen kimlikler: E6, S6, A3, D15, B8 (yeni iş bir sonrakini alır).

## Sıradaki

Sıra kullanıcının kararıdır (2026-11-12; 2026-11-13'te D1 bölündü; 2026-11-15'te D8 kapandı, D11 açıldı).
**2026-11-16 (kullanıcının değerlendirmesi):** S4'e ara verildi (Claude'da üç eklenti dizinde, Risale için dizin ekibine
e-posta gitti; OpenAI'de kendi adıyla başvuru kararı kullanıcıda), "Bekleyen"e geçti. D11 ve D5 için hazır değiliz,
çok ar-ge gerekiyor: D12 açıldı, masanın ikinci hâli S6. D1–D9'un ortak zemini, döngü ve D8 "Kayıt › Kimlikli
işler"e taşındı (bitmişlerdi, "Sıradaki"de kalmışlardı).
**2026-11-17 (kullanıcının kararı):** "Sıradaki" yalnız taslakların ar-gesi ve yazımıdır: A1, A2 ve küçük açıklar
"Sonra"ya indi; S6 bitti; D12 bitti, kalan turları D14'e geçti; D13 (me'haz) açıldı. D11 bitti, kalanı D5.0;
saklı birimlerde ölçüm kendi aşaması (D15). Yol: D13 → D14 → D15 → D5.

| Sıra | Kimlik | İş | Eski adı |
|---:|---|---|---|
| 1 | D13 | Me'haz: taslak İşârât ve Risale-i Nur'dan konuşsun (plan onaylandı, 2026-11-17; sırada D13.2) | |
| 2 | D14 | Taslak hattının turları (D12.5'in kalan turları; sırası D13'ün sonunda) | |
| 3 | D15 | Saklı birimlerde son ölçüm: ar-genin sonu, D5'ten önceki son düzlük (eski D12.6) | |
| 4 | D5 | Asıl iş: Bakara 34 ve sonrası, küçük adımlarla; ilk adım D5.0 üretim hazırlığı (D11'in kalanı) | D1.8 |

**D13. Me'haz: taslak İşârât ve Risale-i Nur'dan konuşsun** (kullanıcının değerlendirmesi ve kararları, 2026-11-17;
plan `docs/d1/d13-mehaz-plani.md`). D12.5'in T1 ve D turlarından sonra kullanıcı: d2 maliyetine değmez (kazancı d1'in
çok azı); asıl sorun me'haz ve mânâ: taslaklar müfessirlerden konuşuyor (9–10 taslak 1'in Arapçasında müfessir adı
49, İşârât 17, Risale'nin öbür eserleri 0; düzeltmeden sonra 75), Risale-i Nur'dan konuşmuyor (İşârât'ın 9–10'daki
son yedi nüktesi, kizb ve sıdk dersi, dört taslağın hiçbirinde yok); kaynaktan caydıran kuralın olumsuz yüzü.
Sebep yapıda: kaynak dosyası dört müfessiri tam metin veriyor, Risale-i Nur'dan yalnız âyetin geçtiği yerleri (9–10'da
bir cümle); Muhâkemât (usul 2.7) yazara gitmiyor; ölçüler me'hazı görmüyor. Kararlar:
- **Me'haz sırası:** (1) İşârât (ve usul 2.7 yazara da); (2) Risale-i Nur'un konuya dair yerleri, **çok sayıda**
  ("sonuçların yarısı falan": konu başına anlamsal aramanın ilk 100 sonucunun üst yarısı, paragrafıyla); (3) nazımdaki
  i'câzı gösteren eserler: Keşşâf ve belâgat eserleri ("Üstad üstü kapalı olarak bizdeki belâgat eserleri ve
  Zemahşerî'nin yöntemini izliyor"); (4) klasik tefsirler **dosyada değil, yalnız araçla**. Kullanıcı: "yapı zaten en
  başından beri böyle olmalıydı."
- Nakil ve istinbat ayrımı (T2'nin özü) D13'e katılır: lafızdan çıkan nükte istinbattır, müfessirde de bulunması onu
  nakil yapmaz; müfessir yalnız kendine has sözü alınınca adıyla.
- **Kör eleştirmene "Risale çizgisi" sorusu** (o3; iki kola birden). Birim **9–10**; taban taslak 1 (h2), yeni taslak 5.
- **d2 bırakıldı;** düzeltme d1 hatta kalır, eleştirmeni (k3) D13 kazanırsa aynı me'haz anlayışına çekilir.
- Adımlar D13.1–D13.8 (planın 3. bölümü); D13.2'den sonra kısa durak (konu listesi, dosyanın sayıları). ≈11–14 $.
- **D13.1 Plan (onaylandı, 2026-11-17).**
- **D13.2 Dosya (kuruldu, 2026-11-17; kısa durakta):** `d1-hat.py dosya` h3 (`konular`, `risale_konu`): 8 konu (Opus,
  yalnız âyetler ve meal, 0,08 $), konu başına iki sorgunun en iyisiyle ilk 100'ün üst 50'si; 377 cümle, 267 paragraf,
  152 bölüm, 25 eser; dosya 27.367 kelime (Risale bölümü 21.177; h2'nin dosyası 11.845, kopyası `dosya-h2.md`).
- **D13.3 İstem h3 (yazıldı, 2026-11-17):** `hat-istemi.md` h3 (me'haz bölümü, istinbat etiketi, Ek 1'e usul 2.7);
  istem 283 bin harf (h2 ≈94 bin), sızıntı testi temiz. Etiket "istinbat" D9.1, D7 raporu ve masada "kendi tespiti"
  gibi sayılır.
- **D13.4 Ölçü (2026-11-17):** kör eleştirmen o3 (`kor-olcu-istemi.md`: me'haz ve Risale çizgisi ayrı ölçü ve ayrı
  hüküm `mehaz`), me'haz dağılımı (`d1-tur.py mehaz`).
- **D13.5–D13.6 Taslak 5 ve ölçüm (2026-11-17; ≈9 $; rapor `data/d1/provalar/9-10/d13-rapor.md`):** müfessir adı
  64 → 8, öbür tefsirlere atıf 51 → 7, Risale-i Nur'un öbür eserlerine atıf 5 → 17, Arapça 18.997 → 12.448 harf,
  envanter %57 → %60, farklı görüş adayı 4 → 0; kör eleştirmen (o3) yeniyi bütün olarak hafif, **me'hazda açık**
  tercih etti (tabanda iki nisbet hatası). İşârât'ın kizb ve sıdk dersi (N41–N47) yine yok. Okuma `tur-9-10-D13.html`
  (N39, N17, N24; ≈808 kelime).
- **D13.7 Okuma (2026-11-17):** yeni 2 (N39 "açık ara": müfessir sayımı yerine usulle kelime ve mânâ; N24 "çok daha
  iyi": vâv, nazîr, Risale'den alıntı), taban 1 (N17: tabanın usul ve mantık silsilesi, yeninde yalnız Zemahşerî).
  Kullanıcı: "sonuçlar ümit verici." Kural 4.4: eleştirmen ve kullanıcı aynı yönde, **h3 yeni taban** (D13.8, kullanıcı
  onayladı: "sonuçlar çok iyi"; D13 bitti; D14'ün ilk adımı konuşuluyor). Dersler: Risale-i Nur anılıyor ama açılmıyor; yazar akıl yürütmesini kuramadığı yerde Zemahşerî'ye yaslanıyor.

**D14. Taslak hattının turları** (kullanıcının kararı, 2026-11-17: D12'nin kalanı ayrı aşama). **Sırası D13'ün
sonunda belirlenir** (şimdi yazılmaz). Tur sayısına tavan konmaz: taslağın hazır ya da hazıra yakın olduğu okumada
hissedilince D15'e geçilir (kullanıcı); harcama tavanı D12.5'inkiyle ortak, ≈250 $. D13'ün sonucuyla kurulan tabanla, D12.5'in işleyişiyle (her tur tek değişiklik, taban ve yeni kol, kör
eleştirmen, envanter ayar, kullanıcının okuması; plan belgesi `docs/d1/d12-rapor-ve-plan.md` 4.3, 4.4, 4.10). Adaylar
(sıra D13'ün sonucundan ve tabanın zaaf profilinden; `data/d1/provalar/9-10/d12-5-profil.md`):
- **Düzeltme eleştirmeni k3:** D13'ün me'haz anlayışı ("kaynakta var, adını ver" notları kalkar; Risale-i Nur'un
  ilgili dersine dayanmayan yer sorulur). D13 kazanırsa ilk iş.
- **Nisbet denetimi** (profilin en ağır kusuru, yüksek notların 6/9'u): nakledilen söz kaynağın kendi görüşü mü,
  itirazın parçası mı, naklettiği ya da reddettiği vecih mi; yapıyla (programın sorusu), kuralla değil.
- **Yazarın notu tartması:** 45/45 kabul, 0 ret; yanlış not (K30, "altı cümle") taslağa geçti.
- **Uzunluk:** düzeltme Arapçayı %23 uzatıyor, hedef aşılıyor.
- D12.5'ten kalan turlar: garaz (eski T3), takdir zinciri alanları (T4), üslûp belgesi ve usul yazımda (T5; usulün
  2.7'si D13'le yazara gidiyor).

**D15. Saklı birimlerde son ölçüm** (kullanıcının kararı, 2026-11-17: kendi aşaması; "D5'ten önceki son düzlük, o
aşamaya kadar ar-ge"; eski D12.6). D14'ün en iyi hattı saklı birimlerde (21–22, 25, 30, 28, 29, 26–27) bir kez, aynı
ölçüyle: kör eleştirmen, envanter (ayar), kullanıcının okuması. D5'e geçiş ölçütü plan belgesi 4.7 (yeni hat çoğunlukla
tercih ediliyor, kapsama düşmüyor, uzunluk hedefte). Burada hat değiştirilmez; açık çıkarsa D14'e dönülür.

**D12. Taslak altyapısının ar-gesi** (bitti, 2026-11-17, kullanıcının kararı: D12.1–D12.4, D12.5'in Tur 0, T1 ve D
turu yapıldı; kalan turlar ve D12.6 D14'e geçti; aşağısı kayıttır) (kullanıcının değerlendirmesi, 2026-11-16). D8 istemle denedi, pahalı ve açıkça
yürümedi (ders: istem kuralı düşünmeyi değiştirmiyor). D11 maliyeti düşürdü ama eleştirmenin sistemli zaafları (Z1, Z4,
Z6, Z7, Z10) aynı kaldı. Hedef: eleştirmenin haklı ve olumsuz eleştirilerinden sıyrılmış taslak yazabilen bir altyapı.
Kullanıcının fikirleri:
- İşârât'ın Bakara 9'dan 31–33'e kadarki her birimi bir deneme şansıdır (cevabı bilinen, kör prova); hepsi ya da
  gerektiği kadarı kullanılır.
- Her taslak iki kez yazılır: önce sıfırdan, sonra eleştiriler (belki İşârât'a dayanan kısımları çıkarılarak) yazana
  gösterilip yeniden; sonuca bakılır.
- İşârât'a daha uygun bir iş akışı aranır.
- Yazana usul belgesi gibi bir üslûp belgesi ve Risale-i Nur'dan çıkarılan öbür gerekli belgeler verilir: müellif
  Risale-i Nur ve İşârât'ı "me'haz" diye gösterir.
**Kararlar (kullanıcı, 2026-11-16):**
- Birimler ikiye ayrılır. Geliştirme: 9–10, 13, 14–15, 16 (kısa, 11–12 türü; İşârât'ına serbestçe bakılır). Saklı:
  21–22, 25, 30 (maksat), 28, 29 (lafız tahkiki), 26–27 (mağlata cevabı); yalnız sonda, bir kez.
- İki kez yazdırma üç şartla: düzeltme notlarını kapalı kitap eleştirmen yazar (İşârât'ın o birimi gizli, öbür her
  şey MCP'den açık: D5'in şartı); baştan yazdırma yerine düzeltme (yalnız değişen paragraflar); notlar süzülmeli mi
  ayrı ölçülür (bütün notlarla ve kullanıcının süzdükleriyle).
- İşârât'a uygun yapılı akış onaylandı: (1) okuma ve kelime/hey'et çizelgesi (boş satır reddedilir; Z11), (2) garaz
  ve her nüktede "garaza hizmeti" alanı (Z10), (3) ikinci vecihte takdir zinciri alanları (lafız → mukadder sual →
  halka; Z1), (4) kaynak etiketini program koyar (Z5–Z7), (5) araçsız yazım, üslûp belgesi yalnız burada, (6) kapalı
  kitap eleştiri ve düzeltme.
- Üslûp belgesi İşârât'ın Arapçasından mekanik çıkarılır (kalıp, sıklık, cümle kimlikli örnek). **Muhâkemât usul
  özetine eklenir:** müellif onu "yazdığı tefsir mukaddimesi" diye anar
  (`muhakemat/makale-03/maksad-03/maksad-02/c004`), İkinci Makale "Unsur-u Belâğat"; usul özetinde hiç yoktu.
- S6'nın tasarımı (iki yan seçilir, taslak belge gibi, eleştirmen/bilirkişi kenar işareti, karşılaştırma renk,
  "Metinlerin tamamı" yer düğmesi) kullanıcının hayal ettiği gibi.
- **Ölçü** (kullanıcının kararı, 2026-11-16, konuşmadan sonra): eleştirmenin notları güvenilir (D7.7 %95, D9.3
  10/10, D11'de tutmayan alıntı yok); çekince yalnız aynı eleştirmenin hem yön verip hem ölçmesine (notları
  karşılanan taslağı kendiliğinden beğenir; aynı modelin ortak kör noktaları). D5'te ölçü zaten eleştirmen ve
  kullanıcı olacak; ar-ge eleştirmeni ayarlar. Üç ayak: (a) **eleştirmen asıl ölçü, kör:** notları yazandan ayrı yeni
  sohbet, hangi taslağın düzeltildiğini bilmez ("A" ve "B", sıra karışık); (b) **kullanıcı:** deney başına 5–10 yerde
  kör A/B tercihi ve kısa gerekçe, yanında süzgeç örneklemi (≈1 saat); (c) **İşârât envanteri** yalnız ar-gede,
  ilk ikisini ayarlamak için, hedef değil.
- **Kapalı ve açık kitap eleştirmen** (kullanıcının kararı, 2026-11-16). D5'te ayrım kalkar (İşârât yok): kapalı
  kitap eleştirmen (MCP'de her şey açık, yalnız İşârât'ın o birimi gizli) D5'in eleştirmeninin kendisidir; açık
  kitap yalnız ar-gede var, değeri cevabı bilmesi. Kullanımı: (1) kör ölçü (notları yazana gitmez); (2) kapalıyı
  ayarlama: aynı taslakta iki not listesi karşılaştırılır, açığın yakalayıp kapalının kaçırdıkları "yalnız gizli
  metinden bilinebilir" ve "kapalının da görebileceği" diye ayrılır; ikincisi küçükse kapalı D5'e hazır; (3) üst
  sınır kolu: taslak 7 açık kitap notlarıyla da düzeltilir (notları D11'de yazıldı); açık notlu düzeltme çok iyiyse
  darboğaz eleştirmen, benzerse yazanın düzeltme gücü; bu kolu açık eleştirmen adil ölçemez, envanter ve kullanıcı
  ölçer; (4) açık notların genel dersleri D12.3'ün yapısına gider, aynı birimin yazarına hiç gitmez.
- **Eleştiri biçimi** (kullanıcının kararı, 2026-11-16; D11.3'ün sorusuydu): düzeltmeye giden kapalı eleştiri
  **bölüm bölüm** (Mukaddime ve üç vecih; her çağrı taslağın tamamını bağlam görür; yeri belli not, ≈3 kat not);
  yazan bir notu gerekçeyle reddedebilir ("V2'de söyledim"), retler notların kalitesini de ölçer. Ölçü **bütün**
  (A/B bütünü tartar, ucuz).
- **D11.3 D12.1'in okumasına katılır** (2026-11-16): taslak 7 tek başına okunmaz; düzeltilmiş hâlinin yanında
  (isteyince taslak 3 de) okunur. Tek okuma üç soruyu cevaplar: D11 değer kaybettirdi mi (7–3), düzeltme işe yaradı
  mı (7–7'), süzgeç. Bunun için S6'nın iki yanlı kısmı okumadan önce gelir.
Adımlar (sıra, 2026-11-16):
- **D12.1 Düzeltme deneyi (bitti, 2026-11-16; ≈25,9 $):** rapor `data/d1/provalar/31-33/d12-1-rapor.md`, sayılar
  `d12-1-sayilar.md`; betik `scripts/d1-duzelt.py` (`kapali`, `duzelt`, `olc`, `notlar`, `rapor`), istemler
  `docs/d1/elestiri-kapali-istemi.md` k1, `duzeltme-istemi.md` d1, `kor-olcu-istemi.md` o1, `not-karsilastirma-istemi.md`
  n1. Kapalı kitap bölüm eleştirisi 58 not (43 karşılanacak; ≈8,1 $). Taslak 8 = 7 + kapalı notlar (41/43
  karşılandı), taslak 9 = 7 + D11'in açık notları (46/51). Bulgular: (1) **kapalı notlarla düzeltme işe yaradı:** kör
  ölçücü 8'i her bölümde 7'ye tercih etti (önce doğruluk: yanlış nisbetler gitti); kaynakta bulunmayan Türkçe tırnak
  24 → 0; (2) **ama uzattı ve yeni iddia getirdi:** Arapça +%28 (hedefi 49 harf aştı), yeni kaynaklardan envanterde 5
  yeni çelişki (eski 3'ün 2'si gitti; tek okuyucu, elle bakılmalı); "düzeltmek uzatmak değildir" kuralı tutmadı;
  (3) kapalı eleştirmen D5'e büyük ölçüde hazır: açığın kapalının da görebileceği halde kaçırdığı 57'de 8 not,
  kapalının tek kalan 24 notunun hiçbiri yanlış değil; (4) üst sınır kolu (9: kapsama %53 → %64, mukaddimesiz %72 →
  %86, çelişki 0): darboğaz yazarın düzeltme gücü değil eleştirmenin bilebildiği; (5) yazar İşârât'ın kendi
  temsilini "kaynakta dayanağı yok" diye reddetti: kaynağa bağlılık kuralı müellifin özgün nüktelerini caydırıyor,
  D12.4–D12.5'te bakılır. Düzeltmenin sonraki sürümü için iki aday (program uzunluk bütçesi; düzeltilmiş
  paragraflara kısa ikinci kapalı eleştiri), kullanıcının okumasından sonra. Masa 8 ve 9'la kuruldu (yayına
  gönderilmedi).
- D12.2 **Fark kartları ve kör A/B kaydı** (kullanıcının kararı, 2026-11-16; tam S6 yerine, D12.3 bunu yeter):
  yalnız düzeltmenin değiştirdiği paragraf çiftleri, eski ve yeni yan yana, kör (sol/sağ sabit tohumla karışık, "A"
  ve "B"); kart başına tercih ve kısa gerekçe; tercihten sonra "aç": hangisinin düzeltilmiş olduğu, envanterin ve kör
  eleştirmenin o yer için dediği, çelişki adayıysa ikinci soru (gerçek çelişki / farklı görüşün nakli / çelişki
  değil / emin değilim). Dışa aktarma JSON.
- D12.3 **Fark okuması** (kullanıcının kararı, 2026-11-16; D11.3 buna katıldı): 7 ile 8, değişen ≈14 çiftten 8–10
  yer: **ölçülerin ayrıldığı yerler** (envanter 8'de yeni çelişki diyor, kör eleştirmen 8'i tercih ediyor: 5 yer) ve
  eleştirmenin "8 açıkça iyi" ya da "8 zayıf" dediği yerler. Taslak 9 ve 3 dışarıda (9'un sorusu cevaplandı; 3'ünkü
  yapılı akışla önemini yitirdi). Süzülmüş notlar kolu düştü (kapalının tek kalan notlarının hiçbiri yanlış değil;
  asıl risk düzeltmenin eklediği). ≈30–45 dk.
  **Bitti (2026-11-16):** rapor `data/d1/provalar/31-33/d12-3-okuma.md`, dosya `data/d1/notlar/d1-fark-31-33-7-8-Fatih-202611162030.json`.
  10 yerde 8: 6, 7: 1, eşit 1, emin değilim 2. Kör eleştirmenle uyum: kesin tercihlerin 6/7'si 8 (eleştirmen 8 diyordu);
  **envanterin 8'deki 5 "yeni çelişki"sinin hiçbiri gerçek değil** (2 farklı görüşün nakli, 3 çelişki değil): envanter
  "farklı görüş adayı" diye okunur, D12.1'in o bulgusu düzeltildi. Düzeltmenin kazancı dayanak (dayanaksız tespiti
  kaynağa bağlama, Arapça alıntı); kaybı îcâz ve kendi sözü (Mukaddime/1'de 7 daha iyi, V3/3 "alıntı yağmuru", V1/4'te
  7'nin kısa sözü); yan etkisi belirsiz gönderme ("şarttaki", "onda") ve düşen fikir (V3/3). Kullanıcı: takdir ve beklenen
  sözü tırnakla göstermek gerekli, sistem buna izin vermeli (V2/0). Fark kartlarında kaynak metni yoktu (Mukaddime/0'da
  hüküm verilemedi). d2 için önerim: (b) düzeltilmiş paragraflara üç soruluk ikinci kapalı eleştiri (düşen fikir,
  belirsiz gönderme, nakil kendi sözün yerine mi geçti) ve istemde "iyi kendi sözünü silme, etiketle"; karar kullanıcıda.
- **D12.5'in döngüsü** (kullanıcının kararı, 2026-11-16): her tur **tek bir değişikliği** sınar (ör. uzunluk
  bütçesi, çizelge adımı, nakil–istinbat ayrımı): yeni hâl o anki en iyi hatla bir geliştirme biriminde yan yana,
  aynı üç ayaklı ölçüyle; kazanan sonraki turun hattı; tur başına ≈20–35 $ ve kullanıcının ≈30–45 dk fark okuması.
  Geliştirme birimleri tekrar kullanılabilir (son hüküm saklı birimlerde). Durma: üst üste iki tur ölçülür iyileşme
  yoksa ya da kalan kusurlar yalnız ehlin görebileceği türdense saklı birimlere geçilir ("eleştirmen kusur bulmuyor"
  ölçüt değildir). Tavan ≈8 tur ya da ≈250 $, sonra konuşulur. D5'e geçiş: saklı birimlerde yeni hat D11'in hattına
  karşı kör ölçüde ve kullanıcının A/B'sinde çoğunlukla tercih ediliyor, çelişki artmıyor, uzunluk hedefte. D5'e
  geçince ar-ge yavaşlar, durmaz (taslak ≈5–10 $: hat iyileşince eski birimler yeniden yazdırılabilir).
- **S6'ya ek** (kullanıcının fikri, 2026-11-16): **dinamik yanlar.** Âyetin altındaki alan N sütunlu: "+ yan ekle"
  her basışta bir yan açar (bir yan tam, iki yan ikiye, üç yan üçe); her yanın kendi seçicisi (Kaynaklar, taslak N,
  İşârât) ve kapatma düğmesi; seçilen yer bütün yanları süzer; kör kipte yanlar "A, B, C" ve sıra karışık;
  masaüstünde en çok 3 (genişte 4), telefonda alt alta ya da sekme. S6'nın tamamı D12.4'ün yanında.
- **S6 yapıldı (2026-11-16):** `scripts/d1-masa-sablon.html` yeniden kuruldu (yardımcılar ve kartlar aynen taşındı,
  yan düzeni ve olaylar yeni): dinamik yanlar (en çok 4), her yanın seçicisi (Kaynaklar, İşârât'ın metni, taslak N),
  taslak yanında üç katman (karşılaştırma renk ve sonda kaçırılanlar; eleştirmen ve bilirkişi paragraf üstü işaret,
  kartlar yerinde açılır; işaretleme listeleri katmanın başında), "Metinlerin tamamı" yer düğmesi, kör kip. İşaret
  anahtarları ve dışa aktarma aynı. jsdom'da duman testi (24 adım) geçti; gerçek tarayıcıda kullanıcı dener.
  Kapalı kitap eleştirmen (D12.1) ayrı katman (2026-11-16, kullanıcının isteği): notlar K1… numarasıyla, öncelik, yazara
  önerisi ve düzeltmedeki akıbeti (taslak 8: karşılandı ya da gerekçeli reddedildi); bölüm özetleri ve sistemli zaaflar.
- **Notlar (kullanıcı, 2026-11-16, D12.1'den):**
  - Düzeltmenin sonraki sürümü (d2) için iki aday: (a) **program uzunluk bütçesi** (paragraf başına harf sınırı;
    aşan değişiklik reddedilir ya da yazara geri döner), (b) **düzeltilmiş paragraflara kısa ikinci kapalı eleştiri**
    (yalnız yeni eklenen iddialar için). Hangisi denenecek, kullanıcının okumasından sonra.
  - **Kaynağa bağlılık kuralı özgünlüğü kısıtlıyor; yapılacak.** D12.1'de yazar İşârât'ın kendi temsilini (bal)
    "okunabilen hiçbir kaynakta dayanak yok; temsil uydurmak usule aykırı" diye reddetti. İşârât'ın en özgün kısmı
    (müellifin kendi temsil, takdir ve nükteleri) kaynaksızdır; taslak bunları "kendi tespiti" etiketiyle, gerekçesi
    âyetin lafzı, hey'eti ve usul olarak yazabilmeli. Kural iki şeyi ayırmalı: **nakil** (bir kaynağa mal edilen söz:
    kaynağa bağlı, mekanik denetimli) ve **istinbat** (âyetin lafzından ve usulden kendi çıkarımı: serbest, ama
    etiketli, derecesiyle ve gerekçesi lafza bağlı). D12.4–D12.5'te yapılır.
- **D12.4 Üslûp belgesi ve Muhâkemât (bitti, 2026-11-16; kullanıcı okudu: "uygunlar"):**
  - **Usul özeti 2.7** (`docs/d1/usul-ozeti.md`, üçüncü sürüm): İşârât'ın Bakara 17–20'deki on iki meselesi
    Muhâkemât'ın İkinci Makalesinin ("Unsur-u Belâğat") Arapça telhîsidir; müellif Muhâkemât'ı "tefsir mukaddimesi"
    diye anar (`muhakemat/makale-03/maksad-03/maksad-02/c004`). Türkçe aslı telhîste olmayan tatbik ve talimatları
    taşır: Dördüncü Mes'ele bir âyetin (Enbiyâ 21:46) her harfini ve hey'etini garaza bağlayıp "bu sana ser-meşktir"
    der (harfler, Z11; garaz, Z10); Sekizinci harflerin mânâ alışverişi; On Birinci kayıt–mukadder sual (Z1); Beşinci
    ve Altıncı derece ve pay (kapsam); On İkinci "hikâyede mahkiyyün-anh yerine geçmek" (kıssa) ve "harice boykotaj"
    (nakil–istinbat). 37 yeni alıntı; denetim `python3 scripts/d1-usul-denetim.py` 148 alıntı, 195 kimlik, 0 sorun
    (denetim artık `muhakemat` kimliklerini de tanır). Prova kopyaları (`ek-ozet.md`, 11–12 ve 31–33) yenilendi,
    sızıntı testi temiz. Not: kapalı eleştirmen usulün 2–5. bölümlerini aldığı için bundan sonraki kapalı
    eleştiriler 2.7'yi de görür (ölçü aleti D12.1'den farklı). Sitedeki okur sürümü (`site/isarat-usul/`,
    `scripts/d1-okur.py`) kullanıcı onaylayınca yenilenir.
  - **Üslûp belgesi** (`docs/d1/uslup-belgesi.md`, `scripts/d1-uslup.py`; prova kopyası `--prova <birim>` ile
    `data/interim/d1-prova/<birim>/ek-uslup.md`, sınanan birim sayım ve örneklerden çıkar): ölçüler (3.264 cümle,
    ortanca 15 kelime, paragraf başına ortanca 1 cümle), 8 grupta 33 kalıp (açılış ve geçiş, delâlet derecesi, takdir,
    hey'et ve harf, garaz, ihtimal, temsil), her biri cümle ve birim sayısıyla ve iki kimlikli örnekle, ve "وأما ﴿…﴾"
    ile açılan üç tam paragraf. **Nakil–istinbat ölçüsü:** cümlelerin yalnız 43'ünde (%1,3; 42 birimin 17'sinde) bir
    âlimin, eserin, mezhebin ya da "قيل:" ile bir kavlin adı geçer; eserin nükteleri büyük çoğunlukla istinbattır.
    31–33 kopyasının sızıntı testi 3 ortak dizi verdi; üçü de vecih açılış kalıbı ("أما نظم الجمل بعضها مع بعض",
    "إن لهذه الآية أيضاً الوجوه الثلاثة"), belgenin öğretmesi gereken şey: kabul edildi.
  - Hangi belgenin yazım hattında nereye gireceği (yazar, kapalı eleştirmen, yalnız yazım adımı) D12.5'te karar.
- **Kararlar (kullanıcı, 2026-11-16, D12.3'ten sonra):** envanterin çelişki sinyali "farklı görüş adayı" diye okunur;
  düzeltmenin kazancı ve kaybı (dayanak; îcâz ve kendi sözü) kabul; düzeltmenin yan etkilerini gidermek D12.5'in
  konusu; **tırnak kuralı: takdir için ayrı işaret**; düzeltmenin sonraki sürümü (ikinci kapalı eleştiri ya da
  uzunluk bütçesi) henüz karara bağlanmadı.
- D12.5 Yapılı akış ve ar-ge döngüsü. **Rapor ve plan** (kullanıcının isteği, 2026-11-16): `docs/d1/d12-rapor-ve-plan.md`
  (D12.5'e kadar öğrenilenler, kalıcı dersler, hedef hat, bir turun adımları, karar kuralı, tur sırası T1 çizelge ve
  okuma–yazım ayrımı, T2 nakil–istinbat, T3 garaz, T4 takdir zinciri, T5 belgeler yazımda, D düzeltme d2; Tur 0
  hazırlığı: dört geliştirme biriminin prova düzeni, takdir işareti, masada kör A/B kaydı, fark kartlarında kaynak
  metni, taban h2). **Onaylandı (kullanıcı, 2026-11-16):** yöntem ve tur sırası uygun; **kullanıcının örneklemi her
  turda en az tutulur**; takdir işareti Türkçede «…» (takdir ve beklenen söz), "…" kaynağın sözü (modelin hiç tırnak
  kullanamaması çözülür); düzeltmenin ikinci sürümü (d2) **ikinci kapalı eleştiri** (yalnız düzeltilen paragraflara:
  düşen fikir, belirsiz gönderme, nakil kendi sözün yerine mi geçti).
  **İşleyiş** (onaylandı, 2026-11-16): plan belgesi 4.10 (kullanıcı turda bir okuma, 3 yer; Claude yürütür, okuma
  hazır olunca ve karar belirsizken durur; tur raporu `data/d1/provalar/<birim>/d12-5-T<n>.md`).
  - **Tur 0 (bitti, 2026-11-17; ≈7 $):** (1) dört geliştirme biriminin prova düzeni (`d1-prova.UNITS`, `_dev_unit`):
    **Türkçe tercümenin düğüm sınırları âyetlerle örtüşmüyor** (13'ün Türkçesi `14-15` düğümünün c001–c010'unda, 14–15'inki
    `16`nın c001–c003'ünde sürer); gizleme düğüm düzeyinde komşu Türkçe düğümü de siler (fazla gizlemek zararsız),
    gizlenen metnin kendisi `parcalar` ile kesin aralık (`unit_sentences`, `local_id`). Sızıntı testi dördünde temiz;
    9–10'da kizb ve sıdk dersindeki düstur (لا يلزم من لزوم صدق كل قول…) Hutbe-i Şâmiye ve Hakikat Çekirdekleri'nde de
    geçer: müellifin başka eserdeki sözü, kabul edildi (`sizinti_kabul`). Kaynak dosyasında "önceki birim" programla.
    Envanterler (Fable çıkarır, Opus denetler): 9–10 47, 13 50, 14–15 64, 16 24 kalem; açık öneriler (2–7) bakılmadı.
    (2) **h2** = h1 + takdir işareti (`hat-istemi.md`: "…" kaynağın sözü, «…» takdir ve beklenen söz); D9.1 h2'den
    beri Türkçe «…»'yı `takdir` sayar (tırnak değil); kör ölçü o2 ve kapalı eleştirmen k2 işaretin anlamını bilir.
    (3) masada **tur okuması** (`d1-masa-sablon.html`): `provalar/<birim>/tur-T<n>.json`'un yerleri âyetin altında;
    yer başına A/B/eşit/emin değilim, gerekçe, sonra "Aç"; yer adına tıklayınca kör kipte Kaynaklar + A + B açılır;
    dışa aktarmada `ab`. (4) fark kartlarında paragrafların andığı kaynakların metni (açılır kutu).
  - **T1 (sürüyor, 2026-11-17):** okuma ve yazım ayrı + kelime/hey'et çizelgesi, 9–10. Yeni kol `scripts/d1-tur.py`
    (istem `docs/d1/cizelge-istemi.md` c1; ortak kısımlar h2'den aynen): okuma oturumu araçlı, çıktısı JSON çizelge
    (âyetin her kelimesine satır: i'râb, harfler, sîga, ta'rif-tenkir, takdim-te'hir, tercih, müfessirler kimlik ve
    aynen sözle, nükte adayı; cümleler, öncesiyle bağ, maksat, ayrılıklar); program eksik ve boş satırı ve kimliğinde
    bulunmayan alıntıyı bir kez geri gönderir; yazım oturumunda yalnız `cite` açık. Taban taslak 1 (h2), yeni taslak 2.
    **Ölçüm (2026-11-17; rapor `data/d1/provalar/9-10/d12-5-T1.md`):** kör eleştirmen yeniyi bütün olarak **hafif**
    tercih etti (V3 yeni açık: tenvin, şuurun nefyi, sirayet; V2 taban açık: yeni iki âyeti "altı cümle" saydı, hata
    çizelgenin cümle bölmesinden); envanter kapsaması %57 → %70; kelime ve harf ölçüsü eşit (18/22); yan etkiler:
    blok alıntı 29 → 91 ("alıntı yağmuru"), Arapçada "قال الماتريدي ما يلي" boşlukları, maliyet 4,37 → 9,46 $ (okuma
    tek başına tabandan pahalı). Kural (4.4): hafif → başka birimde bir kez daha. **Bekleyen:** kullanıcının okuması
    (masa 9–10, tur kutusu, 3 yer: ikinci vecih, «فِى», «مَّرَضٌ») ve tekrar kararı. Ayrıştırıcı başlık önekine ve
    alıntılardan sonra gelen paragraf tercümesine göre esnetildi (`heading_key`, `quote_tr_is_paragraph`).
    **Okuma (2026-11-17):** taban 2 (N26 «فِى», N10 halka), yeni 0, emin değil 1 (N32 tenvin); gerekçe: taban daha
    kapsamlı ve anlaşılır, zinciri akıcı. Kural 4.4: kullanıcı yeniye karşı, eleştirmen yeniyi hafif tercih ediyordu;
    kullanıcının hükmü geçer, **T1 değişikliği taban olmaz**; taban h2 kalır (T1 bitti).
    **Okuma standardı** (kullanıcının kararları, 2026-11-17; plan belgesi 4.10): turda tek sayfa, yer = envanterin tek
    nüktesi, yan başına en çok 2 paragraf ve ≈250 kelime, Türkçe önde, İşârât'ın sözü "Aç"tan sonra, sarı fark yalnız D
    turunda. İlk sayfa (`fark-9-10-T1.html`, "İkinci vecih" düzeyini yer saydığı için bir yanda 19 paragraf) kalktı;
    yerine `data/d1/masa/tur-9-10-T1.html` (`d1-tur.py okuma`, şablon `d1-tur-okuma-sablon.html`): N26 «فِى» lafzı
    (hipotez), N10 zincirin altıncı halkası (ayrılık), N32 «مَرَضٌ»'un tenvini (eleştirmen); ≈911 kelime, ≈15 dk.
    **Eşleme hatası düzeltildi:** taslak çapaları dil başına sayıldığı için `/ar/k` ile `/tr/k` her zaman eş değil
    (Türkçesiz Arapça alıntı ya da Arapçasız Türkçe alıntı sırayı kaydırır); masa ve denetimler sıra numarasıyla
    eşliyordu. Yanlış Türkçe gösterilen taslaklar: 9–10'un 1 (9 paragraf) ve 2'si (51), 31–33'ün 1–4 ve 6'sı;
    D12.3'ün okuduğu 31–33 taslak 7 ve 8 doğru. Eş artık paragraf sırasından (`d1-yz.pairs`; masa, izah ve not
    denetimleri, bilirkişi ve iddia çıkarımı, eşleştirme raporu). Ölçümler (eşleştirme, kör ölçü, D9.1) çapaları
    doğrudan kullandığı için etkilenmedi. Eşi olmayan Türkçe paragraf (Risale'den Türkçe alıntı) masada hâlâ görünmez.
  - **D turu (sürüyor, 2026-11-17; ≈23,7 $; rapor `data/d1/provalar/9-10/d12-5-D.md`):** kullanıcının kararı T1'den
    sonra önce D, profil ölçümüyle. **Profil** (`d12-5-profil.md`): tabanın kapalı eleştirisinde 45 olumsuz not, en
    ağırı yanlış nisbet (yüksek 9'un 6'sı: kaynağın söylemediği, itirazın parçası ya da reddettiği vecih ona mal
    ediliyor), sonra nakil–istinbat etiketi (9; iki yönde bozuk), hey'et ve harf (7), zincir (5), kapsam (5). **d1**
    (taslak 3, 45/45) kör ölçüde tabana karşı açık kazanç, ama K30'un yanlış notuyla "altı cümle" hatası geldi; **d2**
    (taslak 4: ikinci kapalı eleştiri `elestiri-ikinci-istemi.md` i1, 13 not, ikinci geçiş) d1'e karşı hafif; Arapça
    18.997 → 23.426 → 22.834 (hedef ≤21.328), envanter %57 → %64 → %62. Okuma `tur-9-10-D.html` (N14, N13, N38;
    ≈977 kelime, sarı fark). Masa son turu kayıt tarihinden seçer (`tur-*.json`).
    **Okuma (2026-11-17):** d2 1 (N14: d2 kendi tespitini açtı, mânâ netleşti), eşit 1 (N38), emin değil 1 (N13: iki
    hâl neredeyse aynı; envanter gürültüsü, seçim kuralına eklendi). Kural 4.4: eleştirmen hafif, kullanıcı karşı değil:
    başka birimde bir kez daha (kullanıcının kararı bekleniyor).
    **Karar (kullanıcı, 2026-11-17): d2 bırakıldı** (kazancı d1'in çok azı, birim başına ≈5 $); tekrar yapılmaz. D turu
    bitti; d1 hatta kalır. Sıradaki aşama D13 (me'haz).
- D12.6 (D14'ün son adımına geçti, 2026-11-17) Saklı birimlerde son ölçüm; sonra D11'in kuyruğu ve D5. S6'nın kalanı (katmanlar, "Metinlerin tamamı")
  D12.5'ten önce.

**S6. Âyet masasının ikinci hâli** (bitti, 2026-11-17, kullanıcının kararı; kullanıcının fikirleri, 2026-11-16; "Sonra"daki masa açıkları buraya bakar):
- Sol ve sağ yanda ne duracağını kullanıcı seçer (kaynaklar ya da bir taslak); iki taslak yan yana karşılaştırılır.
- Yapay zekâ kısmının odağı taslaktır; İşârât'la karşılaştırma, eleştirmen ve bilirkişi soruları taslağın yanında
  sekme değil, taslağın üzerinde açılan ayrı birimlerdir.
- Üstte "Önceki âyetlerle münasebet"in yanında "metinlerin tamamı" düğmesi; kaynaklardaki "İşârât'ın bu birimdeki
  metninin tamamı" ve taslaktaki "bütün taslağı göster" onunla kalkar.
- **Düzeltildi (2026-11-16):** masa tek birimlikti; 31–33 kurulunca 11–12'nin sayfası üzerine yazılmıştı ("Âyet"
  seçicisinde 11–12 yoktu). Artık birim başına sayfa: `data/d1/masa/<birim>.html`, `index.html` son birim; seçici
  öbürüne gider; deploy klasörü gönderir.

**D11. Üretim hattı: birim başına tek, kısa, ucuz taslak; pilot 31–33'te** (bitti, 2026-11-17, kullanıcının kararı: hat tabana dönüştü, kalanı D5.0'da; aşağısı kayıttır) (kullanıcının kararları, 2026-11-15; D8'in
bulgularından; "bir sonraki tur" ama istem değil yöntem sınanır). Amaç asıl işi yapılabilir ve erişilebilir kılmak:
taslak yine kıymetli olmalı, İşârât'ın usulünü ve Risale-i Nur'un çizgisini izlemeli, eldeki verileri kullanmalı.
Kararlar:
- **Birim başına tek taslak**; ucuz önlemler: D9.1 her taslakta (bedava), eleştiri örneklemle.
- **Katmanlar:** Arapça taslak, Türkçe tercüme (sadık, Risale'nin diline yakın) ve **günümüz Türkçesiyle izah**
  (kullanıcının isteği). İzah ayrı adımda, Opus ile, yalnız paragrafın Arapçası ve tercümesinden: taslağın
  söylemediğini söylemez, kaynak numarası ve tırnak eklemez, terimi ilk geçtiği yerde açar; program izahta taslakta
  olmayan [n] ya da tırnak arar; eleştirmen izahı görmez. İzah her paragrafın altında (önce böyle; izahları
  birleştirme adımı "Sonra"da).
- **Uzunluk:** Arapçada İşârât'ın 1–2 katı. D5'te İşârât olmadığı için hedef orandan gelir: Bakara 1–33'te âyetin
  kelimesi başına İşârât'ın harfi; pilotta oran ile 31–33'ün gerçek uzunluğu karşılaştırılır (tutmazsa tür türe).
- **Maliyet kaldıraçları:** kaynak dosyası (müfessirlerin altı taslağın hepsinde okunan birimleri, Risale'nin âyete
  bağlı yerleri, klasik eserlerde âyetin kelimeleri; program toplar, masa gibi), kısa istem (usul özetinin taslağın
  kullandığı özü, v2'nin tutan biçim kuralları), uzunluk sınırı, yazar Opus. Araçla arama kısıtlanmaz (kullanıcı:
  çok kısıtlamak değer kaybettirebilir); kaç çağrı yaptığı ölçülür.
- **Geri çekilme** (pilot kötü çıkarsa): önce belirtiye göre (ipucu dosyada değildi → dosyayı zenginleştir;
  nükte sıkışmış → sınırı 2–3 kata; usul hatası arttı → istemin bölümünü geri koy; çıkarım sığ → Fable). Belirti açık
  değilse sabit sıra: model → uzunluk → istem → dosya (en büyük tasarruf dosyada, en sona). "Kötü": mukaddimesiz
  kapsama altı taslağın en düşüğünün (%66) altında **ve** kullanıcının okuması eskiyi açıkça üstün buluyor. En çok
  iki adım, sonra konuşulur.
- **Eleştiri biçimi** (kullanıcının sorusu: paragraf paragraf bakmak daha çok bulur mu): pilot taslak ve eski bir
  taslak (taslak 3) iki kez eleştirilir: bütün olarak (v1.2) ve bölüm bölüm (aynı sorular, yalnız gördüğü parça
  değişir). Kullanıcı iki not listesini süzer.
- **Kuyruk:** hattın adımları pilotla kesinleşince; birimleri sırayla yazdırır, kullanım sınırına takılınca
  sıfırlanma saatine kadar bekleyip sürer (gece ve gündüz pencereleri boşa gitmez), pencere başına ve haftalık
  sığan işi ölçer. Sıra önerisi: önce Risale-i Nur'un bağ kurduğu âyetler.
Adımlar:
- **D11.1 Hat (bitti, 2026-11-15):** `scripts/d1-hat.py` (`dosya`, `hazirla`, `yazdir`, `izah`, `bolum`, `orneklem`,
  `oran`), istemler `docs/d1/hat-istemi.md` (h1) ve `docs/d1/izah-istemi.md` (i1). Kaynak dosyası 65 bin harf
  (Keşşâf, Beyzâvî, Ebüssuûd, Âlûsî tam; İşârât'ın önceki birimi; Risale'nin yerleri bölümün başıyla; klasik
  eserler); istem 94 bin harf, sızıntı testi temiz. Bölüm eleştirisinde eleştirmen taslağın tamamını bağlam olarak
  görür, notu yalnız kendi bölümüne yazar (N31 dersi). Masa izahı paragrafın altında, bölüm notlarını etiketle
  gösterir.
- **D11.2 Pilot (bitti, 2026-11-15):** rapor `data/d1/provalar/31-33/d11-rapor.md`. Taslak 7 (Opus, h1): 3,1 $
  (eskiler 8,6–12,5), 27 tur (51–76), Arapça 11,5 bin harf (hedef 7–14); kapsama tek okuyucuyla %53, mukaddimesiz %72
  (eskiler aynı okuyucuyla %49–55, %69–79), çelişki 3 (1–5); eleştirmen 26 not (23–31), "doğru" notu 4 (6–9), aynı
  sistemli zaaflar (Z1, Z4, Z6, Z7, Z10) ve istemin ihtilaf kuralının kalıplaşması. Geri çekilme gerekmedi. İzah
  ≈1 $, mekanik denetimde temiz. Bölüm eleştirisi ≈3 kat not (84'e 29, 77'ye 26), ≈3 kat maliyet (≈9,5 $'a 3 $),
  denetimde tutmayan yok. Uzunluk oranı: Bakara 8–33'te âyet kelimesi başına ≈440 harf (138–1238); 31–33 en seyrek
  (Arapça asıl 31'in ortasında biter), D5'te tek oran yetmez. Birim başına tahmin: taslak + izah + D9.1 ≈4,1 $
  (pencerede ≈11 birim). Pilotun toplamı ≈28 $. Kod düzeltmeleri: D9.1 kaynak dosyasını okunan saymıyordu; D7
  raporu tek okuyuculu taslakta boş "ikisi de" satırı veriyordu; masa bölüm notlarını iki kez sayıyordu.
- D11.3 Kullanıcının okuması (2026-11-16: okunmadı, D12.3'e katıldı; eleştiri biçimi D12'de kararlaştı): pilot (taslak 7, izahıyla) ile taslak 3
  yan yana; 20 notluk süzgeç (`yz/d11-orneklem.json`: iki taslak × iki biçim × 5; D8'in 9 notluk süzgecinin yerine).
  Ondan sonra iki karar: eleştirinin biçimi ve sıklığı; D5'in birimleri (İşârât 33'te bitiyor) ve uzunluk hedefi.
- D11.4 Kuyruk, sonra D5.

**D5. Asıl iş: Bakara 34 ve sonrası** (eski D1.8). Tek adım değil, küçük adımlar; D15'ten çıkan hatla (2026-11-17).
- **D5.0 Üretim hazırlığı** (D11'in kalanı, kullanıcının kararı, 2026-11-17): (1) kuyruk (eski D11.4: birimleri sırayla
  yazdırmak, kullanım sınırına takılınca sıfırlanmayı bekleyip sürmek, pencere başına sığan işi ölçmek; sıra önerisi:
  önce Risale-i Nur'un bağ kurduğu âyetler); (2) İşârât'ın olmadığı âyetlerde uzunluk hedefi (D11.2: âyet kelimesi
  başına 138–1238 harf, tek oran yetmez); (3) izah katmanı (günümüz Türkçesiyle, `d1-hat.py izah`; izahları birleştirme
  "Sonra"da).
- D5.1 Bakara 34, tek birim, ehlin okuması.

## Bekleyen (başkasının cevabı)

| Kimlik | İş | Kimde | Eski adı |
|---|---|---|---|
| S4.3 | Claude dizini: Risale başvurusu "In review"; dizin ekibine e-posta gitti (2026-11-16) | Anthropic | M7 |
| S4.1 | OpenAI: doğrulanmış kendi adıyla dizine başvurulsun mu | Kullanıcı | M7 |

Kapananlar (2026-11-12): E4 Kızıl İcaz'ın Türkçesi (gerek yok, "Biten"); Diyanet (izin yok, "Biten"); Osmanlıcanın
kaynağı (A2'nin ön şartı değil).

## Sonra (sırası belli değil; sıraya girince kimlik alır)

Kimliği olanlar ("Sıradaki"nden indi, kullanıcının kararı, 2026-11-17: sıra yalnız taslakların ar-gesi ve yazımı):
A1 kaynakçada doğrudan bağlantı (Aşama 20), A2 Osmanlıca–Türkçe eşleme (Aşama 19), küçük açıklar B2, B3, B4, B5, B7, B8.

**A1, A2:** ayrıntıları "Kayıt"ta eski adlarıyla (Aşama 20, 19). **A2 durumu (2026-11-12):** e-Risale kaynaklarını
kullanmaya izin verdi; erisale'nin Osmanlıcası ön şart değil, Osmanlıca külliyat elimizde (risaleoku, 16 cilt, Envar
baskısı, `osmanlica` grubu). erisale'den alınabilirse baskı farkı kalkar, ama beklenmez. Şimdilik sırada kalır, sonra
yeniden bakılır.

**Küçük açıklar:**
- B2 Risale talimatının öbür bağdaştırıcılara bilgi kipinde gönderme cümlesi (MVP'nin "Kalan"ı; tek kaynakça kuralı
  onları anıyor, yeterli mi bakılır).
- B3 Tefsirde noktalaması seyrek eserlerin uzun cümleleri (Bursevî ortalama 97 kelime) ve âyet birimlerinin %0,9'unun
  denetimden geçmemesi (`data/interim/tefsir/mvp-denetim.md`, çoğu yanlış alarm): ölçüldü, düzeltilmedi.
- B4 Nutuk'ta "birinci kılıç" başlığının altındaki paragraf (B1'in kuyruğundan; B1 donunca buraya kaldı).
- B5 Üç âyet dizgi şüphesi (`docs/ayet-duzeltmeleri.md`), kullanıcının kararı.
- B7 Kelime aramasında bitişik yazılan kelimeler (2026-11-16, gizli adresli deneme, kullanıcı küçük açıklara aldı):
  Risale "Âhirzaman" diye bitişik yazar; `"âhir zaman"` 1, `âhirzaman` 31 sonuç (genel profil). Model anlamsal
  aramayla telafi etti, ama kelime araması yanıltıcı biçimde boşa yakın döndü. "hiçbir", "her şey" gibi öbür bileşikler
  de ölçülür. Seçenekler: (a) iki kelimelik ifade az sonuç verince bitişik biçimi de denemek ya da sonuçta önermek,
  (b) `search` açıklamasına bir satır. Araç çıktısı değişirse deploy'da `DEPLOY_EXPECT="search"`.
- B8 Delâilü'l-İ'câz'da muhakkikin dipnot işaretleri metinde (2026-11-16, aynı deneme): "…في الوجود1، …"; 4.507
  cümlenin ≈1.070'inde (Esrâr'da 1, öbür üç eserde yok). Bilinen ve kayıtlı (`books/klasik_openiti.py`: dipnotlar
  OpenITI'de yok); model alıntıyı rakamıyla verdi, okuyana göze batıyor. `text` değişmez; işaret ayrı tutulup
  görüntüde ve alıntıda atlanabilir (`cite` dipnot işaretini atlayan alıntıyı zaten kabul ediyor mu, bakılır).

Kimliksizler:

- **Konu fihristi** (Aşama 15): dondurulması önerildi (anlamsal arama bu işi büyük ölçüde görüyor); karar kullanıcıda.
- **Kur'ân'a kelime düzeyinde adres** (Y1.1): mekanik; bir ihtiyaç doğarsa.
- **Hadis – hadis rivayet grupları** (Y2.1'in kalanı): aynı hadisin rivayetleri, lafızla (mekanik).
- **Risale'nin müfessiri adıyla anması** (Y1.7'nin mekanik kısmı).
- **Yalnız Türkçe aktarılan hadisler** (HA7, 101 aday cümle).
- **Gönderme tablosu** (Aşama 13'ün ertelenen kısmı).
- **Yerel indirilebilir paket** (Y2.7).
- **Ortak derlemler** (e-Risale, Yeni Asya): tasarım aşağıda.
- **E3 Sorularla Risale:** web araması değil; izin alınırsa `risale/ilgili` koleksiyonuna (`authority: modern`,
  varsayılan aramaya girmez). İzin e-postası gönderilmedi (2026-11-12), izin yoksa eklenmez. Bkz. "Fikirler".
- **E5 Kalan klasik eserler:** E2'den sonra, aynı ölçütle (`docs/eserler/klasik.md`). Önce (b)'nin 2. dilimi, sonra 3. dilimi (kullanıcı, 2026-11-13); (c)'dekiler yer ve zaman müsait olunca.
- **Âyet masasının açıkları** (S5'ten, 2026-11-14): müfessirlerin Türkçesi (yapay zekâ tercümesi, damgalı); bilirkişi
  kartında maddenin paragrafındaki bütün kaynaklar ve kaynak metni gösterilen maddede dayanak varsayılanı (D6'nın
  dersi); işaretlerin sunucuda toplanması ayrı karardır (heyet akışı, dondurulan). Köklü değişiklik yeni kimlik alır.
- **E6 Elmalılı'nın Hak Dini Kur'an Dili, asıl metni:** sadeleştirilmemiş, aslına sadık metin (kullanıcının kararı,
  2026-11-12: Diyanet'in baskısı yok). Müellif 1942'de vefat etti, metnin hakkı 2013'te düştü; ama harf çevirisi ve
  dizgisi baskının yayıncısınındır: kaynak seçilirken bakılır. Bir arkadaşın gönderdiği PDF'ler biçimi bozuk, son çare.

## Dondurulan

Kod, veri ve belgeler yerinde durur; ileride bir heyet çıkarsa altyapı hazır olur.

2026-11-12 (kullanıcının kararı):
- **S3 Gemini** (Aşama 18): Gemini uygulamasında Türkiye için uzak MCP desteği yok (Antigravity ve CLI hariç); şu an
  yapılamaz.
- **B1 Kontrol kuyruğu ve işaretlerin işlenmesi** (Aşama 16): kuyruk paragraflara ayırma içindi, atıf birimi cümle
  olunca gereği kalmadı; Risale'den bugüne hata çıkmadı, çıkarsa kullanıcı bildirir. Kuyruktaki tek şüphe B4'te.
- **A3 Kaynak seçimi** (Aşama 13.3): şu an gerekmiyor.

2026-11-09:

- **Okumayla kurulan ve denetlenen bağlar:** denetçi daveti (Y0.2), aday bağ durumu (Y1.3), denetim arayüzü (Y1.4),
  âyet dosyaları (Y1.8), katkı altyapısı (Y3: OAuth'lu katkı bağdaştırıcısı, `propose_link`, kuyruk), katkılar ve
  aday bağlar (Y4), hadisçi örneklemi (HA6), metinden metne ilişki bağları (`same_view`, `different_view`,
  `objection`, okumayla nakil), hadis model okumalarının bağ kaydına geçişi. Duran: `links.py`, `link_reviews.py`,
  94 denetim kararı (özel depo `data/links/reviews/`), `docs/denetci-olcutu.md`, `docs/denetci-daveti.md`,
  `docs/katki-sartlari.md`, `docs/bag-altyapisi-plani.md`.
- **Tercüme programı:** TR1–TR5, HA4 (hadis tercümeleri), Y0.4'ün (a) şıkkı (izinli tercümeler). Duran: TR1
  envanteri (`docs/tercumeler.md`), `docs/tercume-programi.md`, `docs/turkce-erisim.md`; Risale'deki nâşir mealleri;
  damgalı model tercümesi kuralı.

## Fikirler (konuşuldu, karar yok)

- **Kendi yapay zekâ modeli ve üyelik (2026-11-09):** model eğitmek ya da ince ayar önerilmedi: kaynağa bağlılık
  ilkesine ters (model metni ezberler, atfı hafızadan verir). Claude API'si ve bu bağdaştırıcılarla kendi sohbet
  uygulaması teknik olarak mümkün; eksikleri hesap (OAuth kodu askıda), ödeme, arayüz, kötüye kullanım sınırı, KVKK,
  API maliyeti (altın soru çalıştırmalarından ölçülebilir: M6'da soru başına ≈0,31 $). Asıl engel izinler: risaleoku
  "kazanç olmaması", OpenITI CC BY-NC-SA, Tanzil'in Diyanet mealleri ticari olmayan kullanım; ücretli üyelik bunlarla
  çatışır, önce her kaynaktan yeni izin gerekir. Öneri: düşünülecekse ücretsiz ve bağış destekli, kaynaklara sorarak.

- **Sorularla Risale (öneri, 2026-11-09):** modelin Risale'yi okurken web'deki kaynaklara (Sorularla Risale) bakması
  önerildi. Kullanıcı web aramasına sıcak bakmıyor (belirsizlik, kanıtsızlık). Doğru yol web araması değil, izin
  alınıp `risale/ilgili` koleksiyonuna (`authority: modern`, varsayılan aramaya girmez) eklemek; izin yoksa
  eklenmez, talimata web araması konmaz.
- **Günümüz Türkçesiyle yapay zekâ izahı (2026-11-13; kullanıcının meşveretinden):** taslaklara Arapça asıl ve
  Abdülmecid Nursî üslûbundaki tercümeden sonra üçüncü katman olarak günümüz Türkçesi. Dayanak: amaç i'câzı daha çok
  kişiye açmak; müellif kısalığı zamanın şartlarına bağlar ("kısa tâbirata mecbur olmuştur", `docs/d1/usul-ozeti.md`
  Tenbih). Öneri: bugünkü taslaklara eklenmez (provanın ölçtüğüne katkısı yok, maliyet ≈1/3 artar, okuyucunun notu
  Arapçadan sade metne kayar; nüktelerin çoğu takdim-te'hir, ta'rif-tenkir, edat gibi Arapçanın yapısına bağlı,
  sade Türkçede tercüme değil şerh olur; müellif Abdülmecid tercümesi için bile cezâletin korunamadığını söyler; en
  kolay yayılacak ve "tefsir" diye dolaşacak katman budur). Yeri: ehil Arapçayı onayladıktan sonra, **onaylanmış
  Arapçadan** (taslaktan değil) ayrı yazılır, "yapay zekâ izahı" damgalı. Aradaki dönemde okuyucuya belâgat
  terimleri sözlüğü (hasr, tenkir, takdim, i'tirâz cümlesi…). Bir yol daha: sade Türkçe yerine Risale-i Nur'un o
  âyetle bağlı yerlerini göstermek (müellifin bu asra hitabı İşârât'ı sadeleştirmek değil, temsil ve misalle başka
  bir anlatımdı; modelin yorumu, metinle denetlenmedi). D1.6 okuyucularına sorulabilir: Türkçe tercümeyi rahat
  okuyabildiniz mi, sade bir izah ister miydiniz?
- **Kelime ve hey'et ara çizelgesi (2026-11-13; kullanıcının "kelime kelime taslak" sorusundan):** taslağı kelime
  kelime ayrı ayrı yazdırmak önerilmedi: İşârât'ın esası nazımdır (belâgatin menşei mânâların nazmı, usul özeti 2.2),
  V1 ve V2 doğrudan ilişki, V3'ün işleri de ilişkisel ("neden şu lafız", muvazene, kayıtların garaza akması); ayrı
  üretimler asıl maksatta çelişir, maliyet kelime sayısıyla katlanır, kör prova birim başınadır. (Fâtiha'da birim
  kelimedir ama her kelime öncekiyle nazmıyla açılır.) Yerine bir birim içinde iki geçiş: (1) kelime ve hey'et
  çizelgesi, satır başına i'râb, takdim-te'hir, ta'rif-tenkir, müfessirlerin o kelimede dedikleri ve kaynak
  numaraları; (2) üç vecihli taslak bu çizelgeden seçilerek yazılır. İşârât'ın "bakılacak yerleri önce say" adımının
  genişletilmişi; kazancı atlanan kelimenin görünmesi ve mütehassısın i'râbı hücre hücre denetlemesi. Çizelge ara
  çıktıdır, taslak değil. D2'ye katılmaz (orada değişen yalnız eserler); D3'te ya da ayrı değişke olarak denenir.
  Ölçüt: çizelgeyle V3 gizlenen metnin nüktelerinden daha çoğunu yakalıyor mu.
## Biten (özet)

- D12 Taslak altyapısının ar-gesi (2026-11-17): düzeltme deneyi, fark okuması, üslûp ve Muhâkemât, D12.5'in Tur 0,
  T1 (okuma–yazım ayrımı taban olmadı) ve D turu (d1 kalır, d2 bırakıldı); kalanı D14'te.
- S6 Âyet masasının ikinci hâli (2026-11-17, kullanıcının kararı).
- D11 Üretim hattı (2026-11-17): hat ve pilot (D11.1–D11.2) bugünkü tabanın temeli; D11.3 D12.3'e katıldı; kuyruk,
  D5'te uzunluk hedefi ve izah D5.0'a geçti.
- Aşamalar 1–12, 13 (küçültülmüş), 13.2, 14; veri düzeni (2026-11-02); risaleoku geçişi (2026-10-30).
- Tefsir hazırlığı H0–H6 ve Beyzâvî pilotu T0–T7 (2026-11-04).
- Y0.1, Y0.3, Y0.5, Y0.6, Y1.2 (2026-11-05/07).
- MVP M0–M7 (2026-11-06/07): 13 tefsir, hadis kütüphanesi (Kütüb-i Sitte, Muvatta, 9 kitap, eş-Şifâ, Delâil),
  HA2, hadis ve tefsir bağdaştırıcıları yayında.
- D2 Bakara 11–12, E2'nin eserleriyle (2026-11-13): eserler kapsamayı artırmadı, dayanağı güçlendirdi (Delâil 264 ve
  425 bu âyeti işliyor; 26 klasik dayanağın hiçbiri yanlış değil); rapor `data/d1/provalar/11-12/d2-rapor.md`,
  ayrıntı "Kayıt › Kimlikli işler"de.
- E2 Belâgat eserleri ve klasik eserler eklentisi (2026-11-13, yayında): 1. dilim beş eser (Delâilü'l-İ'câz,
  Esrârü'l-Belâğa, el-Müfredât, Miftâhu'l-Ulûm, et-Ta'rîfât), "Klasik Eserler" eklentisi (`/klasik`), site sayfası
  ve Yenilikler yazısı; 2. ve 3. dilim E5'te. Ayrıntı "Kayıt › Kimlikli işler"de.
- E1 Eser listeleri (2026-11-09): `docs/eserler/tefsir.md`, `hadis.md` (yeni; kütüphanedeki 18 kitaptan üretilir), `klasik.md` (yeni) üç bölümlü; `checklist` elle tutulan (b) ve (c)'yi korur, OpenITI indirmelerini görür ("ham veri 0/13" düzeldi). (b) ve (c) `docs/mvp-kitaplar.md`'deki önerilerden ve künye sayılarından dolduruldu; "?" işaretli şartlar E2.1'de sayılacak.
- S1 Yenilikler ve Open Graph (2026-11-09, yayında): `scripts/site-uret.py`, `docs/yenilikler/`, yazım kılavuzu `docs/yenilikler-kilavuzu.md`; bütün Türkçe sitede "eklenti".
- S2 Sitenin yenilenmesi (2026-11-09, yayında): üç eklentiyi anlatan ana sayfa, `risale.html`, "Hata bildirin", İngilizcesi; ayrıntı "Kayıt › Kimlikli işler"de.
- E4 kapandı (2026-11-12, kullanıcının kararı): Kızıl İcaz'ın Türkçesine gerek yok, model tercümesi damgalı yeter;
  katalogdaki kayıt silindi (73/73). Akgündüz e-postası hiç gönderilmemişti.
- Diyanet'in cevabı (2026-11-12): kaynak dosyalar paylaşılmaz, toplu aktarılmaz, yeniden yayımlanmaz. Kur'an Yolu
  yok; Diyanet İşleri Başkanlığı meali çıkarılır (B6), Türkiye Diyanet Vakfı'nın meali (ayrı kuruluş) kalır;
  Elmalılı E6.
- B6 Diyanet İşleri Başkanlığı meali çıkarıldı (2026-11-12, yayında): Kur'ân katmanı, üç sunucunun talimatı ve
  `get_ayah`, site, ChatGPT paketi, belgeler; Vakfın meali kalır. Yayın kaydı `yayin-20261112-175213`, hadis ve tefsir
  aynı gün; araç çıktısında beklenmeyen fark yok.
- S5 Âyet masası (2026-11-14): âyetten başlayan girişli çalışma sayfası (risalemcp.com/taslak/; solda kaynaklar,
  sağda yapay zekâ taslakları, karşılaştırma, eleştirmen, bilirkişi soruları); "Âyet başına çalışma platformu"
  fikrinin ilk hâli. Açıkları "Sonra"da. Ayrıntı "Kayıt › Kimlikli işler"de.
- D8 Döngü 2, 31–33'te v1 ve v2 (2026-11-14/15): altı taslak, aynı ölçü; v2 ölçülür iyileşme getirmedi (kapsama %51 →
  %49), yalnız Arapça tırnak kuralı tuttu; Z1 ve Z6 altı taslağın hepsinde. Döngü durdu, karşılaştırma (D7) döngüden
  çıktı, asıl iş için yeni hat D11'e. Ayrıntı "Sıradaki › D8"de.
- D9 Yapay zekâ eleştirmeni ve mekanik denetimler (2026-11-13/14): mekanik denetimler (kapsam adayıyla), Opus
  eleştirmeni (176 not), süzgeç örneklemle (10 notun 10'u, 9 başlığın 9'u kalsın); taslakların sistemli zaafı "nasıl
  vardığı"; D8'e 11 genel usul maddesi; rapor `data/d1/provalar/11-12/d9-rapor.md`. Ayrıntı "Kayıt › Kimlikli işler"de.
- D6 Bilirkişi okuması (2026-11-13/14; bilirkişi kullanıcı): 24 maddenin 20'si doğru, 3'ü emin değilim, 1'i yanlış;
  ölçme düzeninin kör noktası kapsam ve derece (mutlaklaştırma), D9'a kalıcı denetim; rapor
  `data/d1/provalar/11-12/d6-rapor.md`. Ayrıntı "Kayıt › Kimlikli işler"de.
- D7 Yapay zekâ karşılaştırıcısı (2026-11-13/14): envanter (41 nükte), 6 taslak × iki kör okuyucu (Fable 5.2, Opus
  5.5), rapor `data/d1/provalar/11-12/yz-karsilastirma.md`; D7.7 sınaması âyet masasında: örneklemin 30 satırında
  güven %95, hiç "tutmuyor" yok; dersler (aynen cömert, iki okuyucu kalır) D8'e. Ayrıntı "Kayıt › Kimlikli işler"de.
- D1 Taslakların yazılması (2026-11-10/12; kapandı 2026-11-13, kullanıcının kararı): İşârât usul özeti (Arapça asla
  dayanan ikinci sürüm, okur sayfası ve PDF), birim çizelgesi, prova düzeni (`scripts/d1-prova.py`, gizleme profili,
  tam ve ince istem), Bakara 11–12'nin üç taslağı, ölçüt çizelgesi; kalanı D6, D7, D8 oldu; ayrıntı "Kayıt › Kimlikli
  işler"de.
- D4 Prova okuma ve not platformu (2026-11-12): `data/d1/okuma.html` (iki kip, iki dil, kaynak cümleleri, notlar,
  ölçüt çizelgesi, dışa aktarma), notların rapora işlenmesi, belgeler `docs/d1/`, kapalı kayıtlar `data/d1/` (kendi
  git deposu).
- MVP sonrası düzeltmeler (2026-11-07/09): hata ayıklama adresleri, râvi araması ve `ibn`, hadis `cite`'ında alıntı
  denetimi, tercüme damgası, ChatGPT önbelleği, kesik kaynakça, web içeriği kuralı.

## Ortak derlemler (tasarım, uygulanmadı)

CLAUDE.md'den taşındı (2026-11-09), değiştirilmeden.

Aynı altyapı üç ayrı metin derlemine hizmet edecek. Derlem bir profildir; kod tek, metinler ayrıdır:

| Derlem | Metin | Kullanım |
|---|---|---|
| `kisisel` | Bugünkü veri: bütün kaynakların en kapsamlı birleşimi | Yalnızca kullanıcının kendi çalışması; hiçbir ortak sunucuya çıkmaz |
| `erisale` | Yalnızca e-Risale metni (sonra e-Risale'nin resmi verisi) | e-Risale ile iş birliği (kullanıcı e-Risale ekibinde) |
| `yeniasya` | Yalnızca Yeni Asya'nın verdiği izinli PDF'ler; mevcut verinin hiçbiri kullanılmaz | Yeni Asya ile ortak proje; PDF için ayrı ayrıştırıcı |

- Ortak derlemin metni kardeş koleksiyonda durur (`risale/kulliyat-erisale`, `risale/kulliyat-yeniasya`), profili onu seçer. Böylece metinler karışmaz, Kur'ân ve hadis gibi ortak alanlar kopyalanmaz. Kardeş koleksiyonlarda kimlikler paralel olabilir: o gün tekillik kuralı profil başına iner.
- Her derlemin katalogu, kimlikleri ve altın soruları kendinedir. Sunucu derlemi `--profile` ile seçer; sunucu adı, talimatları ve kurulumu ayrıdır. Uzak sunucuya yalnızca o profilin verisi çıkar.
- Ortak olan: ayrıştırıcılar, cümle bölücü, eşleme, arama, atıf denetimi, kontrol arayüzü. Bölme kuralı değişikliği bütün derlemlerin numaralarını etkileyebileceği için altın örnek testleri her derlem için ayrı çalışır.
- Kur'ân katmanının Arapça metni Tanzil şartıyla her derlemde kullanılabilir; Diyanet mealleri yalnızca ticari olmayan kullanım içindir, ortak derlemlere girerse Diyanet'ten izin gerekir.
- Kod ve mantık kullanıcıda kalır; ortaklara hizmet olarak sunulur. Bu, ortaklarla yazılı olarak (mülkiyet, münhasır olmama) netleştirilecek. Yeni Asya PDF'lerinin `kisisel` derleme girmesi onların iznine bağlıdır; varsayılan olarak girmez.
## Kayıt

2026-11-09'a kadar CLAUDE.md'deki aşama ve adım listesi, değiştirilmeden taşındı. Dondurulan işlerin maddeleri
(HA4, HA6, Y0.2, Y1.3, Y1.4, Y1.8, Y3, Y4, tercüme programı) yukarıdaki "Dondurulan" bölümüne göre okunur.

### Aşamalar

Tamamlananlar: 1–12, 13 (küçültülmüş), 13.2 ve 14 (indirici, ayrıştırıcı, cümleler, diğer eserler, veritabanı, MCP sunucusu, uçtan uca test, anlamsal arama, Kur'ân katmanı, âyet ilişkileri, aslı Arapça eserler, uzaktan erişim, hadis katmanı), bir de veri düzeni (alanlar, koleksiyonlar, profiller; 2026-11-02). Geçiş kalitesi 2026-10-30'da bitti (`docs/risaleoku-gecis-plani.md`).

Sıradakiler (kullanıcının sırası):

13. **İç atıf ağı (küçültüldü, 2026-11-02):** Ölçüm: anlamsal aramanın kaçırdığı 8 soruda (15'in her ikincisi) gönderme beklenen bölüme 2'sinde götürdü, 1'inde zayıf bağ, 5'inde yol yok; ikisi de düz numaralı, metinde görünen göndermeydi. Bu yüzden yalnız iki iş yapıldı: sunucu talimatında "metin başka yere gönderiyorsa orayı da oku" kuralı ve eski adlar sözlüğü (`books/old_names.json`; her kayıt kanıtlı; `read_section`, `get_outline` `text_elsewhere` verir, talimatta liste). Gönderme tablosu ve ters yön aracı ("buraya kim gönderiyor") ertelendi; Aşama 15 isterse başında yapılır (≈1.700 numaralı gönderme; Fihrist ve derlemeler dışarıda; talebe mektupları ayırt edilemediği için "metnin göndermesi" denir, müellife mal edilmez; `Şuâ` alt başlık da olabilir). Gönderme tablosu gelince Risale – Risale gönderme bağı olarak `data/links/risale/`'ye girer, eski adların yanına.
13.3. **Kaynak seçimi:** Hangi eser için hangi kaynağın kullanılacağını kullanıcının istediği zaman belirleyebileceği bir sistem; arayüzü de olabilir. Bugün seçim `catalog/`'da koddadır. Kaynak değişince kimlikler ve cümle numaraları kayabilir: seçim, eski atıfların etkisini göstermelidir. `docs/izinler.md`'de izni olmayan kaynak genel sunucu için seçilemez.
15. **Konu fihristi (2. hedef):** Konu → cümle listeleri. Anlamsal aramanın üzerine kurulur; konu listesi ve her konunun cümleleri elle gözden geçirilebilir bir dosyada durur, sunucuya araç ya da kaynak olarak eklenir. Konu, ardışık cümle aralıklarından ("pasaj") oluşan ayrı bir katmandır. Konu ortak adrestir (âyet gibi; `konu:` ad alanı, ilişki bağı, denetimli): iki yer arasında konu bağı kurulmaz, sohbetteki "başka nerede geçiyor" cevabı arama sonucudur, bağ değildir (kullanıcının kararı, 2026-11-05). Konu listesinin nasıl kurulacağı aşamanın başında kararlaşır (öneri: Fihrist Risalesi'nden ve başlıklardan, düz liste, bölüm düzeyi; konu adı yorumdur).
16. **Kontrol işaretlerinin işlenmesi:** Arayüzden dışa aktarılan `risale-kontrol-notlari.json` ayrıştırıcı düzeltmelerine dönüşür. Her ✗ için kök neden bulunur. Önce bir kontrol kuyruğu: şüpheli yerler (çok uzun cümleler, boş bölümler, düşük eşleme oranı, PDF kaynaklı eserler) otomatik listelenir.
    - Kuyrukta bekleyen (kullanıcı: şimdilik kenarda, 2026-11-03): Nutuk'ta "birinci kılıç" başlığının altında Divan-ı Harb-i Örfî'den bir paragraf duruyor olabilir (altın soru K5'in cevabında model bildirdi, `20261103-081252`; Âsâr-ı Bediiyye'de birinci kılıç "İttihad-ı millî"). Bakılmadı.
17. **Kızıl İcaz'ın Türkçesi:** Prof. Dr. Ahmed Akgündüz'e izin ve dijital nüsha isteği (`docs/akgunduz-izin-epostasi.md`, Ta'likat tercümesi de), cevap bekleniyor. PDF ayrıştırmasına cevap gelmeden başlanmaz (kullanıcının kararı). İzin kısmı tercüme programındadır (`docs/tercume-programi.md`).
    - Dijital nüsha gelirse doğrudan ondan ayrıştırılır. Gelmezse ve kullanım izni varsa `data/raw/kullanici/kizil-icaz/kizil-icaz.pdf` (399 sayfa resim, kalem işaretli) Claude API Message Batches ile Opus okunur (yerel OCR yetersiz; tahmin ≈12–15 $).
    - Yalnızca Türkçe tercüme okunur; bölümler `kizil-icaz-arabi`'ye paralel kimliklerle bağlanır; baştaki mütercim girişi alınmaz. Okunmuş sayfalar ham veri olarak PDF'in yanında saklanır. Bloklar türüyle işaretlenir (beyit, şerh, hâşiye, dipnot, başlık); okunamayan yer tahmin edilmez. Önce 10 sayfalık deneme, kullanıcı onaylarsa kalanı. Ayrıştırıcı `books/kizil_icaz.py`.
    - İzin yoksa eser `private` kalır, sunucuya gitmez.
18. **Gemini:** uzak MCP bağlayıcısının Gemini uygulamasında (ve Gemini CLI'da) nasıl eklendiği aşamanın başında araştırılır; sitede "yakında". Sunucu değişmez.
19. **Osmanlıca–Türkçe eşleme:** Kullanıcının Osmanlıca istemesinin asıl sebebi: bir alıntıda isterse Türkçe metinle birlikte oranın Osmanlıcasını da vermek. Türkçe ve Osmanlıca paragrafların (harf çevirisi ya da çapa olarak Arapça satırlar ve başlıklar) eşlenmesi, Türkçe cümleden Osmanlıca karşılığa bağlantı, `get_passage`/`read_section`'a isteğe bağlı Osmanlıca çıktı. Baskı farkı: Osmanlıca Envar, Türkçe erisale. Bir eşleme örneklemi kullanıcıya gösterilir.
    - **Önce kontrol: Osmanlıcalar erisale'den alınabiliyor mu?** Ön bulgu (2026-11-02): erisale'nin okuma ayarlarında "Osmanlıca (Hatt-ı Kur'ân)" görünümü ve kelime düzeyinde "Osmanlıca/Türkçe Okuma İpucu" var (`osmanlicaVisibility`, `osmTooltipVisibility`; varsayılan kapalı). Ama indirdiğimiz sayfalarda Osmanlıca metin yok, `sitemap-tr.xml`'de Osmanlıca sayfa da yok; metnin nereden geldiği bulunamadı. `/api/` yolu robots.txt'te yasak, oradan indirilmez. Kullanıcı e-Risale ekibinde olduğu için kaynak ve izin ekipten sorulur (mevcut iznin Osmanlıcayı kapsayıp kapsamadığı dahil). Metin alınabilirse kelime eşleşmesi hazır gelebilir ve baskı farkı kalkar: Envar'lı eşleme yapılmadan önce karar verilir.
20. **Kaynakçada doğrudan bağlantı:** e-Risale ile görüşmeden çıkan öneri (2026-10-30): kaynakçada yolun yanında metnin kendisine bağlantı verilir, kullanıcı metne doğrudan ulaşır. Atıf hangi kaynakta geçiyorsa (erisale.com ya da risaleoku.com) o kaynağın ilgili yerine bağlantı konur. erisale'de bölümün `url`'si outline'da var; risaleoku uygulamasında bölüme doğrudan bağlantı olup olmadığı ve sayfa/bölüm adresinin biçimi aşamanın başında araştırılır. `cite` sonucu (`cite_as`, `bibliography`), sunucu talimatı, proje talimatları ve `citations.CITE_NOTE` buna göre değişir; bağlantı veriden gelir, tahmin edilmez, kaynakta karşılığı olmayan atıf bağlantısız kalır. Yerel eserler ve Kur'ân ayrı düşünülür.

#### Hadis aşamaları

Hadis katmanının kendi sırası (kullanıcı, 2026-11-03). Risale aşamalarından ayrı numaralanır (HA). Önerilen sıra
aşağıdadır, kullanıcının onayıyla değişir. Ayrıntılı geçmiş: `docs/hadis-plani.md`, kitaplar: `docs/hadis-kitaplari-plani.md`.

- **HA1. Bağ altyapısı (Risale–hadis bağlarını kendi yapısına taşımak):** Bugün bağlar dağınık: `arabic.hadith_support`, `hadith_matches`, `hadith_located`, `hadith_region`, `hadith_readings`. Ortak bir bağ kaydına taşınır: kaynak (cümle ya da geçiş), hedef (rivayet kimliği `bukhari/52`), tür (lafız, kısaltma, mânen, künye), güç, kanıt, yöntem (derlem, künyeli arama, okuma), `data/links/` altında dosya. `ayah_links` aynı yapıya geçer: bütün eserlerin bağ ağının altyapısı budur (Risale içi göndermeler, ileride tefsir). Önce yapılır, çünkü sonraki aşamalar bağ üretir; bağlar iki kez taşınmasın. `hadith_support` bağlardan türetilen özet olur.
- **HA2. Hadis kaynaklarını kütüphaneyle sınırlamak:** Eşleşme yalnız `data/library/hadis/` kitaplarından gelir; Sanadset'teki tefsir, tarih, tabakât ve mevzu derleyen kitaplar rivayet kaynağı olmaktan çıkar (bugün eşleşmelerin bir kısmı oradan). Künyedeki kitap adı (İhyâ, Keşfü'l-Hafâ…) nâşirin künyesi olarak kalır; o kitaplar rivayet kaynağı sayılmaz. HA3 ile birlikte ilerler: kitap eklenmeden Sanadset'ten gelen sağlam eşleşmeler (Müsned, Müstedrek…) kaybolmasın; geçişte kaybolanlar sayılır.
- **HA3. Doğrulanmış hadis kaynaklarını eklemek:** İlk dilim (Kütüb-i Sitte, Muvatta) bitti. Sonraki kitaplar doğrulanamayan künyelerin sıklığına göre: Müsned, Müstedrek, Dârimî, İbn Hibbân, Beyhakî, Taberânî, sonra derleme kitapları (Mecmaü'z-Zevâid, Keşfü'l-Hafâ, Feyzü'l-Kadîr, Kenzü'l-Ummâl). Kaynak önce OpenITI'de aranır; her kitapta künyenin numara sistemi (Müsned'de cilt:sayfa) ve bölge ölçümü yapılır; ardından künyenin bölgesinde okuma (Adım 9) o kitaplara genişler. Okumaya kelimesi benzeyen ama sözü ya da sayısı farklı tuzak kontroller eklenir (Adım 9'un açığı).
- **HA4. Türkçe tercümeler:** Mütercimi belli ve izinli kaynak gerekir (Hadith API'nin `tur-*` baskılarının mütercimi bilinmiyor, alınmaz; risaleoku'nun Kütüb-i Sitte'si telifli). İzin istenecek adaylar: Diyanet (Tecrid-i Sarih, Hadislerle İslâm), İbrahim Canan'ın Kütüb-i Sitte Tercüme ve Şerhi (Akçağ). İzin gelmeden başlanmaz; e-posta taslağı kullanıcının seçtiği yayıncıya hazırlanır. Risale'deki hadislerin nâşir mealleri (`publisher_translation`) zaten vardır. Tercüme programına taşındı (`docs/tercume-programi.md`, 2026-11-06).
- **HA5. Hadis sunucusu (`hadis` profili):** Karar (kullanıcı, 2026-11-03): ayrı bağlayıcı, kod ve depo tek. `risale-mcp --profile hadis`, aynı makinede ayrı adres (ör. `mcp.risalemcp.com/hadis`); kendi sunucu adı, talimatı, gizlilik ve tanıtım sayfası, ayrı dizin başvurusu. Kullanıcı iki bağlayıcıyı birlikte ekleyebilir; araç adları sunucu adıyla ayrılır.
  - **Hadis sunucusunun araçları:** kitapları ve bâb ağacını okuma, rivayet arama (Arapça kelime ve anlamsal; Türkçe tercüme gelirse o da), künyeden ("Buharî, Ezân: 148") bölgeye ve rivayete gitme, rivayetin Risale'de geçtiği yerler (bağlardan, ters yön; Risale metnini kopyalamaz, atıf ve kimlik verir), dereceler âlimin adıyla.
  - **Risale sunucusunda kalan:** `find_hadith`, `get_hadith`, kaynakçanın hadis satırları; veritabanında yalnız Risale'ye bağlanan rivayetler. Hadis sunucusundaki tam rivayete kimlikle (`bukhari/52`) gönderme yapılabilir.
  - **Ortak veri:** bağlar `data/links/` dosyalarındadır (HA1), iki profil de oradan kurar; hadis kitapları `data/library/hadis/` (yalnız `hadis` profili tamamını alır).
  - **Lisans:** genel hadis sunucusuna yalnız izni açık kitaplar çıkar (OpenITI CC BY-NC-SA: kaynak, ticari olmayan, aynı lisans); Türkçe tercümeler kendi iznine bağlıdır (HA4). Ortak derlemler (e-Risale, Yeni Asya) hadis kitaplarını taşımaz.
- **HA6. Hadisçi:** Örneklem okumayla bulunanlardan (Adım 9) bir dilimle yenilenir; kararlar `tests/golden/`'a kilitlenir ve kurallara döner.
- **HA7. Yalnız Türkçe aktarılan hadisler:** 101 aday cümle (Adım 4); künye varsa künyenin bölgesinde aranır.

#### Tefsir altyapısı aşamaları

Ayrıntı ve gerekçeler `docs/tefsir-altyapi-plani.md`'de. Önce hazırlık, sonra pilot; her hazırlık adımı bugünkü Risale verisinde yapılır, ölçütü Risale'nin kimliklerinin, sayılarının ve araç çıktılarının değişmemesidir (sunucunun kullanıcıları var; hazırlık onların gördüğünü değiştirmez, pilot `private` kalır).

- **H0. Araç çıktısı karşılaştırması (bitti, 2026-11-04):** `uv run python -m risale_mcp.tool_snapshot record <ad>` sabit 96 çağrıyı (`tests/golden/tool_calls.json`: her araç, kaynaklar, hazır komutlar, hatalı girdiler; talimat ve araç şemaları da) genel profilde süreç içi MCP istemcisiyle kaydeder, `compare <önceki> <sonraki> [--expect araç…]` fark raporu verir (`data/interim/tool_snapshot/`); beklenmeyen fark varsa çıkış kodu 1, deploy edilmez. Anlamsal aramanın sorgu vektörleri diskte sabitlenir (Voyage aynı soruya biraz farklı vektör veriyor).
- **H1. Kimlik manifestosu ve derlem sürümü (bitti, 2026-11-04):** `manifest.py`. Her profil kurulumu bütün cümle kimliklerini özetleriyle ve bölüm yollarını kabul edilmiş manifestoyla (`data/manifest/<profil>/accepted.json.gz`) karşılaştırır: eklenen kabul edilir, silinen ya da metni değişen cümle ve silinen bölüm kurulumu durdurur (veritabanı yazılmaz; rapor `changes/`, kayma başladığı cümleyle; kasıtlıysa `--accept-id-changes`). `meta`da `corpus_hash`; `manifest release` yayına giden veritabanına etiket verir (`releases/`, önceki sürümle farklar), `cite` sonucu `corpus_version` taşır. `deploy.sh` veri gönderirken release'i kendisi yapar.
- **H2. Eserin yazarı (bitti, 2026-11-04):** `Work.author` (varsayılan Bediüzzaman; başkasının metninde bilinmiyorsa boş, tahmin edilmez), `translator`, `editor` (muhakkik), `compiler`; `authority` eserin kendi yazarına göre okunur. Değerler yalnız katalogun notlarının söylediği.
- **H3. Baskı kaydı ve izin kapısı (bitti, 2026-11-04):** `catalog/editions.py` her eserin dijital nüshasını ham verinin kendi bilgisinden kurar (indirme manifestosu: adres, zaman, dosya özeti; risaleoku kataloğu: raf ve raf grubu, yayınevi diye yorumlanmaz; Sikke'nin ek bölümü), `works.edition`'a yazılır. `catalog/permissions.py` `docs/izinler.md`'nin koddaki karşılığıdır; eser izin kaydına bağlıdır (varsayılanı sitesinden). Genel profil izni kayıtlı olmayan ya da reddedilen kaynaktan eser kurmaz: kurulum durur, eser sessizce düşmez. İstisna `Work.public_without_record` (kurulum her seferinde uyarır): yalnız Rumuzat-ı Semaniye, karar kullanıcıda. Şema 15; araç çıktıları değişmedi.
- **H4. Bağ uçlarının genelleşmesi (bitti, 2026-11-04):** `links.py`. Bağın iki ucu da bir eserin cümlesi, aralığı (`…/c004..c007`, aynı bölümde) ya da bölümü olabilir; metnin ad alanı koleksiyondan türer (`risale/kulliyat` → `risale:`; yeni koleksiyon eklenince ad alanı kendiliğinden geçerli olur, `tefsir:` bugün geçersiz). Kaynakta önek isteğe bağlıdır (öneksiz kimlik bu kütüphanenin metni; bugünkü dosyalar değişmedi), veritabanına öneksiz yazılır, hedef önekli kalır. `links.resolve` ucu çözer, önek eserin koleksiyonuyla tutmalı. Metinden metne türler (`TEXT_RELATIONS`, geçici, T5'te kesinleşir): `quote` + `same_words` / `transmits` (nakil), `relation` + `same_view` / `different_view` / `objection`; metne giden bağda tür zorunlu. Bağın anahtarı (`Link.key`): kaynak, hedef, tür, parça.
- **H5. Denetim kaydı (bitti, 2026-11-04):** `link_reviews.py`, `data/links/reviews/<alan>/<yöntem>.jsonl` (ayrı yerel git deposunda, açık depoda değil) ve `reviewers.json` (isimli denetçiler). Denetçinin adı ve kimliği araçlara ve veritabanına girmez, sabit numarası (`number`) girer (şema 20, kullanıcının kararı, 2026-11-05). Denetçinin ihtisası (Y1.2, şema 21): `reviewers.json`'da `fields` (`kuran`, `hadis`, `tefsir`, `risale`, `metin`; her biri `since`, isteğe bağlı `trial`, `until`); bağın gerektirdiği alanlar cinsinden ve uçlarından (`link_reviews.needed_fields`: lafızda hedefin, ilişkide iki ucun alanı, Kur'ân ile müfessir arasında yalnız `tefsir`, göndermede gönderenin); alanı tutmayan karar kaydedilir ama sayılmaz (`competent: false`), bağ ancak gereken alanların hepsi ehil kabulle karşılanınca "denetlendi"dir. Katılım şartları (Y0.5, `docs/katki-sartlari.md`; CC BY 4.0, toplu atıf, sitede yayımlanmaz, yalnız davetliye): denetçinin kabulü `reviewers.json`'da `terms` (`TERMS_VERSION`), kabulden önceki karar kurulumu durdurur; proje sahibi `owner: true`. Tefsir – tefsir ve Risale – tefsir bağlarında (iki ucu metin, lafız ya da ilişki) gerekçe her kararda zorunlu (`needs_reason`, 2026-11-05); denetçi ölçütü `docs/denetci-olcutu.md`. Satır bir karardır: bağın anahtarı, `status` (`reviewed`, `disputed` gerekçeli, `withdrawn`), denetçinin `strength` hükmü, tarih, gerekçe, `seen`, `origin`. Yalnız eklenir; denetçi ve bağ başına son satır geçerlidir, denetçiler birbirini silmez, model denetçi değildir. Geçersiz kayıt (listede olmayan denetçi, gerekçesiz itiraz) kurulumu durdurur; bağı profilde olmayan karar yüklenmez (`reviews_unmatched`). Şema 17, `link_reviews` tablosu; `find_ayah` bağın yanında `reviews` verir. İlk veri âyet ilişkilerinin 62 kararı (denetçi: kullanıcı, 2026-10-27; 57'si tam anahtarlı). Talimat değişti: deploy `DEPLOY_EXPECT="find_ayah instructions"` ile (`--expect` artık talimatı ve araç açıklamasını da kapsar).
- **H6. Ortak OpenITI okuyucu (bitti, 2026-11-04):** indirme `sources/openiti.py` (`Text`: depo, sabit commit, yol; `.txt` ve `.yml`, `data/raw/openiti/` alanlar arasında ortak, manifesto birleşir), okuma `openiti.py` (alana bağlı değil): üst bilgi ve baskı (`edition`: muhakkik, yayınevi, yer, yıl), `.yml` açıklaması (`version_info`: hangi baskıyla karşılaştırıldığı), paragraflar ve başlık seviyesi, `@QB@…@QE@` âyet aralıkları (metinde ﴿ ﴾), sayfa işaretinden paragrafın başladığı ve bittiği sayfa. OpenITI'nin kuralı: `PageV01P003` 3. sayfanın sonudur; son işaretten sonraki metnin sayfası bilinmez (`None`), tahmin edilmez. Sayfalar üst bilgideki baskınındır, `.yml`'deki karşılaştırma baskısının değil. `uv run python -m risale_mcp.openiti [anahtar…]` özet verir. `hadis_kutub.py` buna geçti: yedi kitabın 55.911 paragrafında metin eskisiyle harfi harfine aynı, kutub JSON'ları yalnız `printed` ve `source.edition` kazandı; 35.778 hadisin hepsi sayfalı, sayfa hiçbir kitapta geri gitmiyor (Buhârî 1 → 1/3, Buğa baskısı). Risale tarafında araç çıktısı değişmedi.
- **T0. Nüsha (bitti, 2026-11-04):** Envârü't-Tenzîl'in beş OpenITI sürümü sabit commit'ten (`fetch tefsir`, `sources/tefsir.py`, `data/raw/openiti/beyzavi-*`). Asıl nüsha **Shamela0023588** (Maraşlî tahkiki, Dâru İhyâi't-Türâsi'l-Arabî, 1418): adı bilinen tek tahkik, tutarlı sayfa işaretleri, her âyete başlık, noktalama. Kur'ân alıntıları işaretsiz (Kur'ân metninde aranır; JK'nın `@QB@` işaretleri denetim için). Muhakkikin girişi alınır, Maraşlî'nin diye işaretli ayrı katman olarak (kullanıcının kararı, 2026-11-04); müellife mal edilmez. Karşılaştırma tablosu `docs/tefsir-altyapi-plani.md`'de. `openiti.version_info` doldurulmamış `.yml` şablonunu bilgi saymaz.
- **T1. Ham veri incelemesi (bitti, 2026-11-04):** döküm `data/interim/tefsir/beyzavi-t1.md`: 39 âyet birimi, başlıkları birleşince hepsi Tanzil'le tutuyor; lemma işaretsiz; paragraf sınırları Shamela'nın biçim kalıntısı; Kur'ân alıntıları işaretsiz ama metinde.
- **T2. Kararlar (bitti, 2026-11-04, kullanıcı onayladı):** `docs/tefsir-altyapi-plani.md` "T2". Koleksiyon `tefsir`, eser `beyzavi` (`private`, Maraşlî `editor`), kimlik `beyzavi/2/6/c003`, giriş `beyzavi/mukaddime-tahkik` (muhakkik katmanı), hutbe, sûre düğümleri; birimin başında baskının âyet satırı (`kind: ayah`, cümle sayılmaz); paragraf yalnız cümle sonunda biter; bölücü değişmez; lemma aday işareti (T5). Örnek `data/interim/tefsir/beyzavi-t2-ornek.json`.
- **T3. Ayrıştırıcı (bitti, 2026-11-04):** `books/beyzavi.py` (kurallar başında), `catalog/tefsir.py`, yeni `Collection.TEFSIR`, `Group.TEFSIR`, `Site.OPENITI` ve izin kaydı `openiti`; baskı kaydı OpenITI manifestosundan ve üst bilgiden (`printed_edition`). `uv run python -m risale_mcp.build beyzavi` → `data/library/tefsir/beyzavi.json`: 46 düğüm (giriş ve iki kısmı, hutbe, 2 sûre, 39 âyet birimi), 422 paragraf ve 40 âyet satırı (`kind: ayah`, cümle değil), 977 cümle (birimlerde 767), hepsinde `printed` (`books/printed.py` paragrafın `page_breaks`'inden). Girişin alt düğümleri yalnız kendi içindekiler listesindeki iki kısım; öbür başlık satırları paragraf açar. `Node.extra` başlık ağacına `verses`, `printed`, `authority`, `by` yazar. `openiti.py` `### $` satırlarını tanır (`entity`). Yalnız yerel profil (`KISISEL` koleksiyonlarına `tefsir` eklendi); genel profilde araç çıktısı ve kimlikler değişmedi, yerelde 977 cümle ve 46 bölüm eklendi. `build_db`'nin parantezli alıntı yöntemi 3 Kur'ân alıntısı buldu (asıl tarama T5). Varsayılan arama Beyzâvî'yi getirmez (yalnız külliyat). Eksik: `read_section` âyet satırının metnini göstermiyor (T6).
- **T4. Bağların eksikleri (bitti, 2026-11-04):** `Link.target_display` (metin hedefinin atfı: hedefin metni o profilde yoksa gösterilen) ve `links.cite_as` (iki ucun atfı veriden: cümle, "… ile başlayan N cümle", bölüm); `check` hedefin kaymasını da yakalar (`target_moved`). Şema 18: `links.display`, `links.target_display`. `build_db` metin hedefli bağı ancak hedef bu veritabanındaysa ya da hedefin eseri katalogda, profile açık ve atfı kayıtlıysa yükler: yalnız yerelde duran esere (`private`, ör. Beyzâvî) giden bağ genel profile hiç girmez (`links_target_private`), atfı olmayan `links_target_no_display`. `Library.text_links(id)` bir cümleye, aralığa ya da bölüme dokunan metinden metne bağları iki yönde verir (öbür ucun atfı, bu sunucuda olup olmadığı, denetim kararları; araca T6'da bağlanır). Yeni yöntem `structure` (eserin yapısı söylüyor: müfessirin âyet birimi). Denetim kaydına komutla yazma: `uv run python -m risale_mcp.link_reviews add <alan/yöntem.jsonl> --source … --target … --type … --status … --reviewer …` (bağ veritabanında olmalı, `seen` veriden). Genel profilde araç çıktısı değişmedi; şema değiştiği için deploy veriyle.
- **T5. Bağlar (bitti, 2026-11-04, kullanıcının bakışını bekliyor):** `links_tefsir.py` (`uv run python -m risale_mcp.links_tefsir`, ≈3,5 dk; yerel veritabanından) → `data/links/tefsir/` (hepsi `private`): `structure.jsonl` 39 (birim → âyetleri, `verse_unit`, yöntem `structure`), `quran_text.jsonl` 419 (işaretsiz Kur'ân alıntısı: kelime sınırlı iskelet araması; en az 3 kelime ve 9 harf, birimin kendi âyetinde 2 kelime ve 4 harf; birden çok yerde geçen söze numara verilmez, 33; `lemma` adayı 115 = kendi âyetinin sözü cümle başında; kendi âyetinin cümle ortasındaki sözü zayıf), `corpus.jsonl` 10 («» içinde hadis işaretli 18 sözden 1'i derlemde bulundu, 4'ü kısmen, 11'i bulunamadı; parça anahtarı yok: Risale'nin hadis tablolarına karışmaz; rivayet metinleri `data/library/hadis/tefsir-beyzavi.json`). Eşik JK'nın `@QB@` işaretleriyle ölçüldü: isabet %97,5, JK'nın en az 2 kelimelik işaretlerinin %90,5'i kapsanıyor. Raporlar `data/interim/tefsir/t5-kuran.md` (ölçüm tablosu, 30'luk örneklem), `t5-hadis.md`, `t5-isarat.md`. İşârât ile Beyzâvî: her birimin İşârât'ta karşılığı var ama Arapça İşârât ile ortak 4 kelimelik diziler yalnız kalıp ifadeler: lafzen aktarım yok, ilişki okumayla. Ölçüt tuttu: tefsir bağlarıyla ve onlarsız kurulumlar arasında Risale'nin hadis, âyet ve denetim tabloları aynı; genel sunucunun araç çıktısı aynı. Not: `data/library/tefsir/` altındaki her JSON eser sayılır, başka dosya konmaz.
- **T6. Araçlar (bitti, 2026-11-04):** her ek veriye bağlıdır: veritabanında müfessir eseri varsa (`Library.has_classical`, bugün yalnız yerel profil) görünür, genel sunucunun araç çıktısı ve talimatı değişmedi (`tool_snapshot` t6). Şema 19: `nodes.extra` (âyet birimi `verses`, `printed`, katman `authority`/`by`), `sentences.printed`, `paragraphs.verses`. Eserin yazarı varsayılandan farklıysa sonuçlarda `author` (`list_works`, `search`, `semantic_search`, `get_passage`, `read_section`). `read_section`: birim başlığında `verses`, `printed`, katmanda `layer`; baskının âyet satırı metniyle (`kind: ayah`, `verses`, get_ayah'a yönlendiren not; cümle değil); cümlelerde `printed`. `get_passage` ve arama: muhakkikin girişindeki cümlede `layer` ("… Maraşlî's text, not the work's author's"). `find_ayah` tek âyette Risale'nin yerlerinden sonra `classical_works` (eser, yazar, âyeti işleyen birim, şerhteki alıntılar cümle başına bir kayıt). Yeni araç `text_links` (metinden metne bağlar, iki yön) ve talimata `CLASSICAL_INSTRUCTIONS` (yazarı söyle, Bediüzzaman'a mal etme, âyet satırı Kur'ân'dır, Risale önce, aynı âyet ilişki değildir, "tefsir" deme) yalnız o zaman. Altın sorular T1–T4 (`tests/golden/questions.json`, kategori `tefsir` ve tuzak; `golden_questions.md`'de yok, kullanıcının onayını bekliyor); ilk çalıştırma `20261104-164638`: 12/12 atıf doğrulandı, dördünde beklenen bölüm okundu; açık sorular (eserin "tefsir" diye anılması, aramanın ek ayırmaması) planda.
- **T7. Kullanıcı örneklemi (bitti, 2026-11-04):** `uv run python -m risale_mcp.links_tefsir --sample` → `data/interim/tefsir/t7-orneklem.html` (Arapça tek yazı tipi, büyük; önceki seçim ve numaralar korunur). İlk turdan: âyet metni kesilmeden ve bulunan kelimeler âyette vurgulu gösterilir; Kur'ân alıntısı bağı alıntının iskeletini parça anahtarı taşır (aynı cümlede iki alıntı ayrı bağ); alıntıyı haber veren kalıp kelimeler ("قائل", "قوله"…) alıntının başı olmaz; kendi âyetinin 2 kelimelik eşiği yalnız cümle başında (alıntılar 419 → 330, isabet %97,8). Kararlar denetim kaydında (`origin: T7`): lemma 13 ✓, A35 ✓; B hadisçiye bırakıldı; C (28 uzun cümle) kalır, `tests/golden/beyzavi_long_sentences.json`. İkinci turda kalan 18 satırın hepsi doğru: 40'lık örneklemin 32'si kayıtlı ✓, 8'inin bağı kural düzeltmesiyle kalktı; `find_ayah` müfessirin alıntılarında da `reviews` verir. **Pilotun ölçütü tuttu** (planda); sıradaki eser ve aralık kullanıcıyla seçilir, genel sunucuya çıkış ayrı karar.
- **Yol haritası (Y0–Y4, 2026-11-04):** pilotun değerlendirmesi ve nihai adım listesi `docs/tefsir-pilot-degerlendirme.md`'de. Y0 kişiler, izinler, kararlar (denetçi ölçütü ve adayları, izin soruları, Türkçe erişim kararı, katkı şartları, dizin politikaları; hemen ve paralel); Y1 planda yedi değişiklik ve âyet dosyası pilotu (kelime adresi, denetçi ihtisası, `proposed`, denetim arayüzü, HA2–HA3, arama, Keşşâf, Fâtiha dosyası); Y2 hadis ve tefsir sunucuları; Y3 katkı altyapısı (OAuth, `propose_link`, kuyruk, denetim akışı); Y4 katkılar, aday bağlar, âyet dosyaları. Kullanıcının dört adımı Y1–Y4'tür.

#### Yol haritası adımları (Y)

Her adımın sonucu ve kullanıcının kararları burada, bittikçe (kullanıcının isteği, 2026-11-05). Adımların tanımı
ve sırası `docs/tefsir-pilot-degerlendirme.md` "Nihai adım listesi"nde.

- **Bağ şeması (kullanıcı onayladı, 2026-11-05):** üç cins kalıcı: lafız (`quote`), ilişki (`relation`), gönderme
  (`reference`); alan çifti yeni cins açmaz, yöntem ve alt tür ayrı görünür. Hadis bağlarının hepsi lafız bağıdır
  (mânen nakil dahil); model okumaları Y1.3'te aday olarak aynı kayda girer. Risale – tefsir ve tefsir – tefsir:
  mekanik olanlar (aynı sözle nakil, Risale'nin müfessiri adıyla anması) Y1.7'de, okuma isteyenler katkı aşamasında;
  önce Y1.8'de bir denetçiyle biçim denemesi. Konu ortak adrestir, ikili konu bağı kurulmaz (Aşama 15). Hadis – hadis
  (aynı hadisin rivayetleri) Y2.1'de. Ayrıntı: `docs/tefsir-pilot-degerlendirme.md` "Bağ şeması".
- **Y0.1 Denetçi ölçütü (bitti, 2026-11-05):** `docs/denetci-olcutu.md`. Alanlar `kuran`, `hadis`, `tefsir`,
  `risale` ve bağ dışı `metin` (Arapça ayrı alan değil). Bağ → alan kuralı cinsten ve uçlardan: lafızda hedefin,
  ilişkide iki ucun alanı (Kur'ân – Risale `kuran` ve `risale`; Kur'ân – müfessir yalnız `tefsir`; Risale – tefsir
  `tefsir` ve `risale`), göndermede gönderenin. Davetle girilir (sayfadan yazan davet edilirse); her alan için 10
  satırlık deneme (en çok 1 hata, yanlışların hepsi yakalanır). İhtilafta oylama yok. Kullanıcının alanları `kuran`,
  `risale`, `metin`. Tefsir – tefsir ve Risale – tefsir kararlarında gerekçe zorunlu (`needs_reason`). Görünen ad:
  gerçek ad ya da kısaltma, takma ad yok; ayrılan denetçinin adı istenirse gizlenir.
- **Kararlar açık depoda değil (2026-11-05):** depo herkese açık kalır; `data/links/reviews/` `.gitignore`'da, kendi
  git deposunda, uzak kopyası özel `fatihebrarinan/risale-mcp-denetim` (karar ekleyince orada commit ve push).
  Araçlar ve veritabanı denetçinin adını değil sabit numarasını taşır (`number`, şema 20; kullanıcı 1). Adı proje
  sahibi ve tefsiri yazacak heyet bilir.
- **Y1.2 Denetçinin ihtisası (bitti, 2026-11-05):** şema 21; `reviewers.json` `fields` (`since`, `trial`, `until`);
  karar yalnız denetçinin karar tarihindeki alanlarında sayılır, alanı tutmayan `competent: false`; araçlarda kararın
  `fields`, bağda `review_fields: {needs, covered}`. Kullanıcının eşleşen 89 kararı ehil ve tam. Deploy edildi
  (`yayin-20261105-230221`).
- **Y0.2 Denetçi daveti (sürüyor):** `docs/denetci-daveti.md`: yedi adım (aday, davet, cevap, deneme, şartlar,
  kayıt, ilk tur), e-posta ve WhatsApp metni, alan paragrafları, deneme planı. Adaylar yalnız özel depoda
  (`data/links/reviews/adaylar.md`). Kararlar: hadis denemesi cevabı yapıdan bilinen satırlarla; tefsir daveti Y1.7'yi
  bekler (aday yok); davet "adınızı heyet ve proje sahibi bilir" der. Kullanıcı bir adayla görüşüyor (Risale, Kur'ân,
  hadis); haber gelince deneme dosyası hazırlanır.
- **Y0.5 Katılım şartları (bitti, 2026-11-05):** `docs/katki-sartlari.md`. Katkı lisansı CC BY 4.0, toplu atıfla
  ("Risale-i Nur MCP denetçileri (Denetçi N)"); lisans geri alınamaz, geri çekme kararın geçerliliğini kaldırır.
  Yapay zekâ yardımı gerekçede belirtilerek serbest. Şartlar sitede yayımlanmaz, yalnız davetliye; gizlilik bilgisi
  şartların 11. maddesinde, sitedeki politika değişmedi (Y3'te değişir). Kabul `reviewers.json`'da `terms`
  (`TERMS_VERSION` 1); kabulden önceki karar kurulumu durdurur; proje sahibi `owner: true`.
- **Y0.3 İzinler (bitti, 2026-11-05):** e-Risale (sözlü, yazılı nüsha yok) ve risaleoku (yazılı: kazanç olmaması ve
  kaynak gösterilmesi şartıyla) kullanıcının metinlerle yapacağı her işi, nurpedia şartsız ("uygun bulduğunuz
  şekilde", kaynak gösterme ricası) kabul etti. Ayrı sunucular ve yerel paket kapsamda (pakette kaynaklara nezaketen
  bilgi ve şartlar paketin içinde); Osmanlıca izin değil teknik soru (Aşama 19). Yazılı cevaplar yerelde
  `data/raw/kullanici/izinler/`; kayıt `docs/izinler.md` "Kapsam" ve `catalog/permissions.py`.
- **Y0.4 Türkçe erişim (kararlar 2026-11-05):** `docs/turkce-erisim.md`. Sohbette modelin tercümesi damgalı ("yapay zekâ tercümesi"), alıntı bloğunda yalnız Arapça asıl, `cite`'a ve kaynakçaya girmez, müfessire mal edilmez; kütüphanede model tercümesi saklanmaz (veride kaynak gibi görünür); denetim arayüzünde Arapçası sınırlı denetçiye geçici, damgalı yardımcı tercüme; uzun vadede izinli tercümeler, bütün alanlar için bir tercüme programıyla (öneri bekliyor). Talimata işlenmesi Y1.8 ve tefsir sunucusuyla.
- **Tercüme programı (kullanıcı onayladı, 2026-11-06):** `docs/tercume-programi.md`. Bütün alanların izinli Türkçe
  tercümeleri tek programda (HA4 ve Aşama 17'nin izin kısmı buraya taşındı): TR1 envanter (`docs/tercumeler.md`,
  künyeler katalogdan doğrulanır), TR2 öncelik (Risale'deki ağırlık, iznin alınabilirliği, dijital nüsha), TR3 izin
  dalgaları (önce devlet kurumları: Diyanet, TDV, TYEK; e-postayı kullanıcı gönderir), TR4 tercüme katmanı (ayrı eser,
  `Work.translation`, paralel kimlik, hizalama; araçta önce izinli tercüme, yoksa damgalı yapay zekâ tercümesi), TR5
  tercümesi olmayanlar için gönüllü mütercimler (açık ilke sorusu).
- **TR1 Envanter, 1. tur (2026-11-06):** `docs/tercumeler.md`: 14 hadis, 6 tefsir, 2 Risale tercümesi, her biri
  doğrulama düzeyiyle (kütüphane kataloğu / yayınevi-ilan / çelişkili). Bulgular: devlet kurumlarının tercümeleri
  az ve tam değil (Diyanet'in Buhârî'si muhtasar Tecrîd-i Sarîh, TYEK'in Keşşâf'ı sürüyor, metinle birlikte); tam
  hadis tercümeleri çoğunlukla eski ve ticari yayınevlerinde (hak mütercimde de olabilir); hiçbirinin dijital nüshası
  doğrulanmadı (Hadislerle İslâm hariç, o da seçme). Telif süresi notu: Babanzâde'nin kısmı (ö. 1934) serbest, ama
  Diyanet baskısının düzenlemesi sorulmadan alınmaz. Sırada 2. tur (eksik künyeler, dijital nüsha) ve TR2.
- **MVP (kullanıcının kararı, 2026-11-06):** `docs/tefsir-pilot-degerlendirme.md` "MVP". Bütün metinler, adresleri
  ve yalnız net bağlar (âyet birimi, tefsirdeki Kur'ân alıntısı, Risale'nin hadislerinin yeni kitaplarda lafzı;
  mevcut bağlar kalır; okuma isteyen ilişki kurulmaz); tercüme eklenmez (Risale'dekiler kalır), kullanıcı Arapça
  konuşmuyorsa model alıntıyı kendisi çevirir ve kendi çevirisi olduğunu söyler; modelin bulduğu ilişki yorumdur.
  Adımlar M0 kitap listesi, M1 kapasite ve maliyet, M2 ortak ayrıştırıcılar (tefsir, hadis), M3 net bağlar, M4 arama
  (Arapça önek, Türkçe ek), M5 hadis ve tefsir sunucuları, M6 ölçüm, M7 yayın. Gerekçe (kullanıcı): bağlanan yapay
  zekâ metinler arası ilişkiyi metin önündeyse iyi bulur; denetimli bağlar sonra güçlendirir. MVP'den sonra sırasıyla
  Türkçe ve İngilizce desteği (tercüme programı; TR1 envanteri hazır, 2. tur ertelendi), denetçi bulununca denetimli
  bağlar (Y1.3, Y1.4; Y0.2 sürer), katkı altyapısı (Y3), sonra eklenenler (Y1.1, Y1.8, Y2.7, Y4).
- **M0 Kitap listesi, 1. tur (2026-11-06):** `docs/mvp-kitaplar.md`. Kullanıcının 12 tefsirinden 10'u OpenITI'de
  (Keşşâf, Râzî, Taberî, Kurtubî, İbn Kesîr, Beyzâvî, Celâleyn, Mâtürîdî, Ebüssuûd; Fî Zılâl'in dosyası eksik görünüyor
  ve yazarın hakkı 2036'ya kadar sürüyor); Elmalılı ve Kur'an Yolu Türkçe, OpenITI'de yok. Kullanıcının kuralı:
  Muhammed Abduh'tan kaynak alınmaz (Menâr'ın da hariç tutulması soruldu). Hadis önerileri Risale'nin künye
  sıklığından (`data/interim/hadis/kunye.md`): Müsned, Keşfü'l-Hafâ, Müstedrek, Mecmaü'z-Zevâid, Feyzü'l-Kadîr,
  Dârimî, Kenzü'l-Ummâl, İbn Hibbân, Câmiu's-Sağîr, Mu'cemü's-Sağîr (kitap anmalarının %39'u → %71). İlk kapasite
  tahmini: vektör ücreti küçük (birkaç $), belirleyici sunucu belleği (8 GB öneri).
- **M0 kararları (kullanıcı, 2026-11-06):** MVP tefsirleri 13 (Taberî, Mâtürîdî, Keşşâf, Râzî, Kurtubî, Beyzâvî
  tamamı, Nesefî, İbn Kesîr, Celâleyn, Suyûtî ed-Dürrü'l-Mensûr, Ebüssuûd, Bursevî, Âlûsî; hepsi OpenITI), hadiste
  önerilen ilk dilim (10 kitap + mevcut Kütüb-i Sitte ve Muvatta; "Mucmelussair" = el-Mu'cemü's-Sağîr). Fî Zılâl
  eklenmez, listede kalır. Elmalılı ve Kur'an Yolu için izin MVP sürerken Diyanet'ten (`docs/diyanet-izin-epostasi.md`,
  kullanıcı gönderir), izin gelince eklenir. Abduh ve Menâr kaynak alınmaz: `catalog/excluded.py` (OpenITI'den
  indirilemez, katalogda yazar olamaz). Klasik eserler sunucusu (İhyâ, Miftâh, Cürcânî) MVP'den sonra. Liste son hâli
  değil; MVP şişirilmez. eş-Şifâ sorusu cevapsız (MVP'de değil).
- **M1 Nüsha ve kapasite (2026-11-06):** `docs/mvp-kitaplar.md` "M1". 22 eserin ≈100 sürümü Range ile yoklandı
  (`data/interim/mvp/probe/`); kelime sayısı `.yml`'deki `LENGTH`: tefsir 21,8 milyon, yeni hadis 8,6 milyon. Nüshalar
  muhakkiki bilinen, başlıklı Shamela sürümleri (öneri, tabloda). Riskler: altı tefsirde âyet başlığı yok (birim
  metindeki âyetten çıkarılmalı), Kur'ân alıntısı araması pilot hızında günler sürer (indeksli yöntem). Kapasite:
  üç süreç ≈2,7 GB bellek, sunucu 3,8 GB: 8 GB'a geçilmeli; vektör ücreti büyük ihtimalle ücretsiz (200 milyon token).
- **M1 kararları (kullanıcı, 2026-11-06):** nüshalar uygun; el-Câmiu's-Sağîr MVP'den çıktı (listede kalır), MVP'nin
  hadis kitapları dokuz; sunucu CAX21'e (8 GB) büyütülür (kullanıcı panelden). Diyanet e-postası gönderiliyor
  (meallerin izni de istenir).
- **Sunucu (2026-11-06):** Helsinki'de ARM serisinde kapasite yok, rescale olmadı. Karar M7'de; öneri hadis ve
  tefsir için ayrı sunucu (risale sunucusu taşınmaz, Caddy Tailscale üzerinden yönlendirir). Rescale için kapatılınca
  sunucu birkaç dakika kapalı kaldı: sunucu kapatılacaksa önce kullanıcıya hatırlatılır.
- **M2 (bitti, 2026-11-06):** `docs/mvp-kitaplar.md` "M2". 13 tefsir (Beyzâvî tamamı kendi ayrıştırıcısıyla; öbür
  12'si `books/tefsir_openiti.py`: metin Shamela'dan, âyet sınırları altafsir.com sürümünden, harf iskeleti ve
  sıklıkla tartılmış dizilerle küresel tutarlı zincir; satır çapadan bölünür; âyetin sözü birime alınır) ve 9 hadis
  kitabı (`hadis_openiti.py`; Zehebî, Esed ve Elbânî katmanları ayrı `layers`). 43.115 âyet biriminin %0,9'u
  denetimden geçmiyor (`data/interim/tefsir/mvp-denetim.md`, çoğu yanlış alarm). İlk birimden önceki ön metin alınmadı
  (müellif mukaddimesi ile muhakkik girişi ayrılmamış; eser başına karar sonra). Yerel veritabanı 1,45 GB (+545 bin
  cümle), kimlikler kaymadı; genel profil ve araç çıktısı aynı. Sınır: noktalaması seyrek eserlerde cümleler uzun
  (Bursevî ortalama 97 kelime). Kur'ân alıntısı araması kelime başına ≈0,6 ms.
- **M3 (2026-11-06):** `docs/mvp-kitaplar.md` "M3". Tefsir: `links_tefsir --mvp` 43.115 âyet birimi ve 402.479 Kur'ân
  alıntısı bağı (13 eser, private, ≈77 dk); 94 denetim kararı bağını buluyor; yerel veritabanı 1,66 GB, genel aynı.
  Hadis: HA2 ölçümü (`hadis_kutuphane.py`, `data/interim/hadis/ha2-olcum.md`): yalnız kütüphaneyle tam bulunan 83 → 73,
  bulunamayan 150 → 164; kaybedilenlerin çoğu hadis kitabı değil, beşi eş-Şifâ ve Delâil'de. Geçiş (ve eş-Şifâ,
  Delâil'in eklenmesi) kullanıcının kararı; `matches.json` değişmedi.
- **M4 Arama (2026-11-06):** sorgu tarafında, dizin değişmedi: tırnaksız Arapça kelime önekli biçimleriyle
  (`search.arabic_forms`), sonuçsuz sorguda kelimeler bir kez kelime başı olarak (`expanded`; "Beyzavi" → "Beyzâvî'nin").
  Genel sunucuda fark yalnız `search` (deploy `DEPLOY_EXPECT="search"`, henüz gönderilmedi).
- **M5 tefsir sunucusu (yerelde, 2026-11-06):** `docs/mvp-kitaplar.md` "M5". Profil `tefsir` (Kur'ân + 13 müfessir,
  1,3 GB), `risale-mcp --profile tefsir`: ad `tefsir`, `TEFSIR_INSTRUCTIONS` (damgalı model tercümesi, ilişki yorumdur,
  Risale kendi bağdaştırıcısında), 11 araç (hadis araçları, kaynaklar, hazır komutlar yok). `find_ayah` müfessirleri
  vefat sırasıyla verir (`catalog/tefsir.DIED`). Genel sunucuda fark yalnız M4'ün `search`'ü. O gün eksik olan
  vektörler, Risale bağlarının atıfla gösterimi ve altın sorular 2026-11-07'de tamamlandı (aşağıda).
- **Gece işi kararları (kullanıcı, 2026-11-06):** hadis birimi şeması onaylandı (atıf birimi hadis `musned/14870`,
  kitap/bâb/sahâbî ağacı adres, katmanlar ayrı; uzun şerhte cümle); eş-Şifâ ve Delâil eklenir; HA2: Risale'nin
  hadisleri yalnız kütüphaneyle eşlenir (genel sunucuya sabah onayıyla); vektörler tefsir ve hadis, üst sınır 150
  milyon token, hadiste hadis başına ve yalnız metin (matn; senet ve katmanlar girmez); `claude -p` altın sorular
  için serbest; push, deploy, dışarıya ileti yok. Sıra: eş-Şifâ ve Delâil, HA2, hadis sunucusu, vektörler, altın
  sorular, Risale'nin âyet bağlarının tefsir sunucusunda adres ve türle gösterimi (metin yok), tefsir ön metinleri
  envanteri, küçük düzeltmeler, Y0.6 araştırması, site sayfası taslakları (`docs/`).
- **HA2 (yerelde, 2026-11-06):** `docs/mvp-kitaplar.md` "HA2". eş-Şifâ ve Delâil kütüphanede (sıra kimlikli birim);
  Risale'nin hadisleri yalnız kütüphaneyle eşlenir (`hadis.py` varsayılanı): tam bulunan 83 → 90, bulunamayan 150 → 140.
  Sanadset rivayet kaynağı değil; numaralar baskının. Genel sunucuya `DEPLOY_EXPECT="search find_hadith get_hadith"`
  ile, kullanıcının onayıyla.
- **M5 hadis sunucusu (yerelde, 2026-11-06):** `docs/mvp-kitaplar.md` "M5: hadis". `hadis_db.py` → `data/dist/hadis/hadis.db`
  (18 kitap, 169.137 hadis, Risale'den 2.981 bağ; Kur'ân tabloları genel profilden), `hadis_library.HadisLibrary`,
  `risale-mcp --profile hadis` (ad `hadis`, `HADIS_INSTRUCTIONS`, 8 araç). Kimlik: baskının numarası, tekrar eden
  numarada `-2`, numarasız kitapta sıra (`sifa/s00007`). `build_db --profile hadis` reddeder.
- **Gece işi, devam (2026-11-07):** tefsir sunucusunda `find_ayah` önce Risale'nin yerlerini kimlik, atıf ve türle
  verir (`risale_refs`, genel profilden; metin yok). Tefsirlerin ön metinleri envanteri `docs/tefsir-on-metinler.md`
  (10 eserde müellifin mukaddimesi; Mâtürîdî ve Kurtubî'de muhakkik ve baskı kısmı; karar kullanıcıda). Âyet
  denetimi raporu yalnız Risale profillerinden. Y0.6 dizin politikaları `docs/dizin-politikalari.md`: okuma
  sunucuları açık kipte kalabilir, katkı ayrı OAuth'lu bağdaştırıcı, talimatlar başka bağdaştırıcıyı çağırmayı
  emretmez (bilgi kipine çevrildi); Claude başvurusu artık claude.ai/directory/manage portalında.
- **Gece işi, sonuç (2026-11-07):** `docs/mvp-kitaplar.md` "Gece işi". Vektörler: hadis 169.137 rivayet (yalnız
  metin, 15,8 M token, `hadis_vectors.py`), tefsir 546.329 cümle (45,1 M + Taberî düzeltmesinden sonra 6,1 M); tefsir
  sunucusunun kopyası `embeddings export-public --profile tefsir`; iki sunucuda `semantic_search` çalışıyor. Altın
  sorular kendi sunucusunda (`golden.py`, sorunun `profile`'ı); 12 yeni soru (TF1–TF6, HD1–HD6) onay bekliyor; hüküm
  verilmedi, uydurma yok. Çalıştırmadan çıkan düzeltmeler: Kütüb-i Sitte ve Muvatta'ya kök düğüm (`get_outline`
  kitap kimliğiyle), `in_risale` tekrarsız ve Türkçe önce, cildi bilinmeyen sayfa "(cilt bilinmiyor)", OpenITI'nin
  `PageEnd` işareti (Taberî'nin 7.972 cümlesinde metinde kalmıştı; yerel, kabul edildi). Site taslakları
  `docs/site-taslaklari.md` (yayımlanmadı). Push ve deploy yok.
- **Sabah işleri (kullanıcı, 2026-11-07):** genel sunucu deploy edildi (`yayin-20261107-091207`: M4 arama, HA2
  hadisleri), push. Altın sorular (T1–T4, TF1–TF6, HD1–HD6) onaylandı (`golden_questions.md` 3. bölüm). Tefsirlerin
  ön metinleri alındı (`books/tefsir_openiti.FRONT`): müellifin mukaddimesi `<eser>/mukaddime`, muhakkikin ve baskının
  girişleri ayrı katman (Mâtürîdî, Kurtubî); bu sırada Râzî'nin, Kurtubî'nin ve Mâtürîdî'nin ön metne düşmüş besmele
  tefsiri birimine döndü, ed-Dürrü'l-Mensûr'un kayık Fâtiha birimleri 1:1 ve 2–7 oldu (`docs/mvp-kitaplar.md` "Sabah").
  Sunucular: risale ve hadis aynı makinede, tefsir ayrı makinede (kullanıcının kararı; ölçüm hadis ≈250 MB, tefsir
  ≈1,2 GB); hadis için `scripts/deploy.sh --hadis` ve `/hadis` yolu, tefsir için `scripts/tefsir-sunucu.sh` hazır;
  kullanım kaydı `server` sütunu taşır. Dizin başvurusu kullanıcıda, acelesi yok. Ön metinlerden sonra tefsir bağları
  yenilendi (43.112 âyet birimi, 403.526 Kur'ân alıntısı; 94 denetim kararının hepsi bağını buluyor), yeni cümlelerin
  vektörleri 5.943 (0,45 M token); yerel ve tefsir profilinde kimlik değişikliği kabul edildi, genel profil aynı.
- **H0 ve H1 her profilde (2026-11-07):** tefsir ve hadis sunucusunun kendi çağrı setleri (`tests/golden/tool_calls_tefsir.json`,
  `tool_calls_hadis.json`; `tool_snapshot record <ad> --profile tefsir|hadis`), hadis profilinin kimlik manifestosu
  (`hadis_db.py`; birim hadis, `--accept-id-changes`); `deploy.sh --hadis` ve `tefsir-sunucu.sh gonder` sürüm etiketi
  alır, son `hadis-yayin-*` / `tefsir-yayin-*` kaydıyla karşılaştırır (`HADIS_EXPECT`, `TEFSIR_EXPECT`). İlk kayıtta
  bulunan hata düzeldi: tefsir sunucusunda eser süzgeçsiz kelime araması boş dönüyordu (varsayılan süzgeç yalnız
  külliyat; `Library._scope` artık yalnız külliyatı olan veritabanında süzer).
- **M6 ilk ölçüm (2026-11-07):** üç bağdaştırıcı kipi `golden run --servers risale,hadis,tefsir` (risale genel
  profille; atıf iki veritabanında aranır, rapor sunucu başına çağrı, başka sunucunun kimliği, `cite`'ın sunucuları ve
  Arapça alıntının damgasını sayar) ve elle deneme klasörü `golden sandbox ~/risale-deneme --servers … --risale-profile
  genel`. 41 soru: başka sunucunun kimliğiyle çağrı 0, atıf 233/252 (17'si ölçüm artığı, 2'si model hatası). Çıkan iki
  düzeltme yapıldı (kullanıcı onayladı, yeniden ölçülmedi): üç sunucunun `cite`'ı `first` alır ve üç talimat "başka
  bağdaştırıcının kaynakları da varsa tek Kaynaklar listesi, numara sürer" der; tefsir talimatı 13 eserin kimliğini
  yazarıyla listeler (katalogdan). Araç çıktısında fark yalnız `cite` ve talimat; genel sunucuya
  `DEPLOY_EXPECT="cite instructions"` ile.
- **Yayın (2026-11-07):** genel sunucu (`yayin-20261107-224059`: `cite` `first`, tek kaynakça kuralı) ve **hadis
  sunucusu** `https://mcp.risalemcp.com/hadis` (aynı makine, servis `risale-mcp-hadis`, 127.0.0.1:8001; ilk kayıt
  `hadis-yayin-20261107-224059`, sürüm `2026-11-07`). Bellek: genel 376 MB, hadis 87 MB (ısınınca ≈250 MB), makine
  3,8 GB. Uzaktan denendi: 9 araç, kelime ve anlamsal arama, künye.
- **Tefsir makinesi (2026-11-07):** `tefsir-mcp`, Hetzner CAX21 (ARM, 8 GB, Falkenstein `fsn1`), Tailscale
  `100.98.98.62`, güvenlik duvarı yalnız `tailscale0`; `scripts/tefsir-sunucu.sh kur|gonder` (varsayılan bu adres),
  servis `risale-mcp-tefsir` 0.0.0.0:8002 (1,3 GB bellek), ilk kayıt `tefsir-yayin-20261107-230200`, sürüm
  `2026-11-07`. Ana makinenin Caddy'si `/tefsir` ve `/tefsir/<anahtar>` yollarını Tailscale üzerinden ona yönlendirir
  (`docs/Caddyfile`; ana makineden 200 döndü). Kullanım kaydı o makinede ayrı. Tailscale anahtarlarının süresi
  dolmamalı (mevcut makinede 2027-04-26): kullanıcıya iki makinede "Disable key expiry" önerildi.
- **Site (2026-11-07):** `site/hadis.html`, `site/tefsir.html` ve `en/hadith.html`, `en/tafsir.html` (taslaklardan);
  bütün sayfaların menüsünde Hadis ve Tefsir; ana sayfada ve kurulum sayfalarında bağdaştırıcılar bölümü; belgelerde
  adresler ve kaynaklar (OpenITI, nurpedia); gizlilik ve kullanım şartları üç bağdaştırıcı ve iki veri merkeziyle (7
  Kasım 2026); Sanadset kaynak listesinden çıktı (HA2); proje talimatlarına tek kaynakça ve yapay zekâ tercümesi
  bölümü. Yayında (`yayin-20261107-232006`, araç çıktısında fark yok). **Tefsir bağdaştırıcısı yayında:**
  `https://mcp.risalemcp.com/tefsir`, uzaktan denendi (11 araç, kelime ve anlamsal arama, `find_ayah`). MVP'de kalan
  yalnız dizin başvuruları (kullanıcı).
- **MVP bitti (kullanıcı, 2026-11-07).** Dizin başvuruları sonra; sıradaki iş MVP'den sonraki sıra (Türkçe ve
  İngilizce desteği, denetimli bağlar, katkı altyapısı; `docs/tefsir-pilot-degerlendirme.md` "MVP'den sonra").
- **MVP'nin kalanı (2026-11-07 denetimi, `docs/tefsir-pilot-degerlendirme.md` "Kalan"):** M5'te risale talimatının
  öbür bağdaştırıcılara gönderme cümlesi (yayınla; tek kaynakça kuralı bilgi kipinde öbür bağdaştırıcıları anıyor); M7'de genel çıkış kararı
  (müfessirler `private`'tan çıkar), hadis sunucusunu açma onayı, tefsir makinesi, site sayfaları ve gizlilik eki.
- **Hata ayıklama adresleri ve ilk inceleme (2026-11-07):** anahtar sunucu başına (`auth --server hadis`,
  `tefsir-sunucu.sh auth`). ChatGPT'yle Deccal/Hz. İsa sohbetinin kaydı yerelde yeniden çalıştırıldı (kayıtta sonuç
  yok, yalnız girdi ve boy). Bulgular: (1) tefsirde `cite` baskının dipnot işaretlerini (`(9)`, `«2»`) atlayan alıntıyı
  reddediyordu, model alıntıyı bıraktı: `citations._NOTE_MARK` ile düzeldi (`dcc0d5c`), henüz yayında değil
  (`DEPLOY_EXPECT="cite" scripts/deploy.sh --code`, `TEFSIR_EXPECT="cite" scripts/tefsir-sunucu.sh gonder`);
  (2) risale ve hadis `cite`'ı aynı cevapta ikisi de [1]'den başlamış olabilir (hadiste `first` yok), cevaplar
  görülmedi; (3) aşağıdaki sıradaki adım.
- **Sıradaki adım (kullanıcının kararı, 2026-11-07): hadis aramasında râvi ve `ibn` farkı.** Bulgu: Müslim'in Nevvâs
  hadisi (`muslim/2937`) kütüphanede olduğu hâlde modelin hiçbir aramasında çıkmadı, model Nevvâs hadisi diye
  `musned/17629`'u verdi. Sebepler: `search_hadith` yalnız metinde (matn) arar, isnadda aramaz (sahâbî ya da râvi adıyla
  bulunamıyor); `بن` ile `ابن` eşleşmez (metin `المسيح بن مريم`, model `ابن مريم` aradı); uzun ve çok konulu rivayette
  anlamsal benzerlik düşük (0,44). Öneri: `search_hadith`'e isnadda arayan `narrator` parametresi (isnad ayrı FTS
  sütunu; metin araması bugünkü gibi yalnız matn kalır), aramada `ابن`/`بن` farkının iki tarafta yok sayılması
  (normalizasyon değişirse sürüm artar), araç açıklamasına "sahâbî ya da râvi adıyla `narrator`" ve kelime araması
  sonuçsuzsa lafız farkı uyarısı. `hadis_db` yeniden kurulur (kimlikler değişmez, H1 manifestosu denetler), hadis
  çağrı setine bu örnekler eklenir (`tool_calls_hadis.json`: Nevvâs, `ابن مريم`), `HADIS_EXPECT="search_hadith"`
  ile `deploy.sh --hadis`. Ölçüt: "النواس بن سمعان" + "الدجال" `muslim/2937`'yi ilk sonuçlarda verir.
- **Râvi araması ve `ibn` (yerelde bitti, 2026-11-09):** `search_hadith(query?, narrator?)`: `narrator` senette aranır
  (`hadis_db` yeni `lib_isnad_fts`: baskı senedi ayırdıysa senet, ayırmadıysa bütün metin; senedi ayrı olan 35.721
  hadis, çoğu Kütüb-i Sitte ve Muvatta), ikisi verilirse ikisi de tutmalı. `ابن`/`وابن`/`فابن` hadis dizininde ve
  sorgusunda `بن`'e iner (`search.hadith_word`, `to_fts(canon=…)`; `لابن` gibiler "لبن"e düşmesin diye kalır; Risale'nin
  araması değişmez, genel sunucuda fark yok). Sonuçsuz metin aramasında lafız farkı notu. Ölçüt tuttu: "الدجال" +
  `narrator` Nevvâs 9 sonuç, `muslim/2937`, `abudawud/4321`, `ibnmajah/4075`, `tirmidhi/2240` aralarında; "… باب لد"
  araması 10 → 16. Hadis çağrı setine 5 çağrı; `tool_snapshot compare` artık beklenen aracın sete yeni eklenen
  çağrısını beklenen sayar ve her profilin çağrı setinden aracı bulur. Kimlik değişikliği yok. Yayın:
  `HADIS_EXPECT="search_hadith instructions" scripts/deploy.sh --code --hadis`.
- **ChatGPT cevaplarının incelemesi ve hadis `cite`'ı (2026-11-09):** râvi araması yayında
  (`hadis-yayin-20261109-094358`), `cite`'ın dipnot düzeltmesi risale ve tefsirde yayında. Dört cevap veritabanıyla
  denetlendi: Risale cevabının 7 alıntısı birebir; kaynakçalar ayrı cevaplarda olduğu için çakışma yok (önceki 2. bulgu
  kapandı). Hadis cevabında Arapça doğru ama model hareke eklemiş, Tirmizî'nin "hasen-sahih"i Buhârî'nin numarasına
  bağlanmış, kullanılmayan kaynak kaynakçada, râvinin izahı ("فأمكم بكتاب ربكم") hadisin sözü gibi sunulmuş, ve
  Risale araçları çağrılmadan "Bediüzzaman bu hadisi Kastamonu Lâhikası'nda ele alır" denmiş (yanlış: Beşinci Şuâ,
  rivayet adı verilmeden). Nevvâs hadisinin tam tercümesi damgasız. Tefsir cevabı iyi (Beyzâvî'ye hareke, Kurtubî'nin
  anmadığı Nevvâs adı). Kullanıcının kabul ettiği üç düzeltme (yerelde, yayında değil): (1) hadis `cite`'ı
  `sources: [{id, quote}]` alır ve alıntıyı rivayetin metninde denetler (hareke, `ابن`/`بن`, dipnot işareti yok
  sayılır, "…" atlanır; söz başkasının katmanındaysa onu, başka rivayetteyse oranın kimliğini söyler; eski `ids`
  biçimi de kabul edilir; risale ve tefsir `cite`'ı zaten denetliyordu); (2) hadis ve tefsir talimatı: Risale'nin ne
  dediğini yalnız Risale bağdaştırıcısında okuyup oradan atıfla söyle, okumadıysan söyleme; (3) tercüme damgası üç
  talimatta: modelin her tercümesi (cümle, rivayetin tamamı, bölüm bölüm aktarım) başında "Yapay zekâ tercümesi:";
  hadis ve tefsirde alıntıya hareke eklenmez, râvinin izahı Peygamber'in sözü değildir. Yayın:
  `DEPLOY_EXPECT="instructions" HADIS_EXPECT="cite instructions" scripts/deploy.sh --code --hadis` ve
  `TEFSIR_EXPECT="instructions" scripts/tefsir-sunucu.sh gonder`.
- **ChatGPT önbelleği ve kesik kaynakça (2026-11-09):** iki ChatGPT denemesinin kaydı (10.05–10.10, 10.27): ChatGPT
  araç tanımlarını ve talimatı bağdaştırıcı eklenince önbelleğe alıyor; hata ayıklama adresli hadis bağdaştırıcısı
  2026-11-07 23:36'dan beri `tools/list` istemedi, `cite` hep eski `ids` biçimiyle geldi (yeni talimat, `narrator` ve
  alıntı denetimi görülmedi). Kullanıcının yenilemesi o bağdaştırıcıya ulaşmadı (10:26'da genel adrese hesapsız bir
  `tools/list` geldi). Araç sonuçları önbelleğe girmez: yeni `cite` notu ve sunucu tarafındaki arama düzeltmeleri
  modele ulaştı (opening-words aramasıyla Nevvâs'ın dört rivayeti bulundu). Cevaplar denetlendi: alıntıların harfleri
  hepsi metinde (hareke model ekliyor), Tirmizî numarası düzeldi, Beşinci Şuâ'dan doğru atıf. Tefsir cevabının
  kaynakçası ilk satırın ilk kelimelerindeki `{` işaretinde kesildi (Taberî birim başı "تعالى: {وإن…"; tefsirde 55.606
  cümlenin ilk kelimelerinde `{` var). Düzeltmeler (yerelde): `library.opening` gösterilen ilk kelimelerde `{ }`
  yerine ﴿ ﴾ (U+FD3F/U+FD3E, verideki âyet işaretiyle aynı; metin değişmez, atıf denetimi ikisini de yok sayar);
  hadis `cite`'ı eski `ids` biçimiyle çağrılınca nota "alıntı denetlenmedi, bağdaştırıcı güncellendi, kullanıcıya
  yenilemesini söyle" eklenir (`LEGACY_NOTE`). Genel sunucuda fark yok. Yayın: `HADIS_EXPECT="cite"
  scripts/deploy.sh --code --hadis` ve `TEFSIR_EXPECT="cite get_passage search semantic_search find_ayah"
  scripts/tefsir-sunucu.sh gonder`.
- **10.37 sohbeti ve araç sonuçlarındaki hatırlatmalar (2026-11-09):** bağdaştırıcı yenilenince ChatGPT `tools/list`
  istedi, `narrator` ve `sources` kullandı. Hatalar: uzun tercüme yeni talimata rağmen damgasız; gösterilen alıntı
  `cite`'a sözsüz verildi; 10.27'de senet "Velîd → Müslim" diye kısaltılıp Ebû Hayseme ve ikinci tarik atlandı; yalnız
  râviyle aramada `muslim/2937` 72'de 20. sıradaydı. Talimat yetmediği için kurallar modelin her seferinde okuduğu
  sonuçlara kondu: `get_hadith` notu tercüme damgasını ve senedi `isnad`'daki gibi, her tarikiyle vermeyi söyler;
  `cite` alıntısız gönderilen kaynakları sayar ve söz gösterilecekse yeniden çağırmayı söyler; yalnız râviyle arama
  kitap sırasıyla (Kütüb-i Sitte ve Muvatta önce; `muslim/2937` 4.). Web'den resim eklemesi kullanıcıya göre sorun
  değil. Yayın: `HADIS_EXPECT="cite get_hadith search_hadith"`.
- **10.59 sohbeti (2026-11-09):** araç tarafı temiz (73 çağrı, hata yok; tek kaynakça risale [1]–[10] → hadis
  `first: 11`; 16 alıntının hepsi birebir, hareke yok, damgalar tam). Hatalar: web'den (islamweb, et-Temhîd) gelen söz
  "veritabanı taraması"nın bulgusu gibi sunuldu, Arapçası denetimsiz ve tercümesi damgasız; kullanılmayan Risale
  kaynağı kaynakçada; Müsned 11130'daki "ehl-i beytimden bir adam" Mehdî diye verildi. Düzeltmeler: risale
  `CITE_NOTE` "yalnız cevabın kullandığı kaynakları listele"; hadis ve tefsir talimatı: web'den gelen her şey bu
  kitapların dışındadır, öyle söylenir, Kaynaklar'dan ayrı verilir, tercümesi damgalanır, kütüphanenin bulgusu gibi
  sunulmaz.

#### Kimlikli işler (2026-11-09'dan sonra)

**İşârât usulüyle yapay zekâ taslağı: ortak zemin, döngü ve D8** ("Sıradaki"den taşındı, 2026-11-16; bitmişlerdi).

D7.7, D9.3 ve D6.2 `okuma-yz.html`'de yürümedi; âyet masasında (S5) yapıldı; D7, D6 ve D9 kapandı (2026-11-14), D2
bitti (2026-11-13). D8 dördünün dersleriyle yapılır: girdisi `data/d1/provalar/11-12/d9-rapor.md` › "D8'e geçenler"
(11 genel usul maddesi), `d6-rapor.md`, `d2-rapor.md`, `yz-karsilastirma.md`.

**İşârât usulüyle yapay zekâ taslağı: ortak zemin** (D1–D9 ve D5'in; kullanıcının yola çıkarkenki fikri, "Fikirler"den
alındı, 2026-11-09). D1 (taslakların yazılması, Bakara 11–12 provası) bitti; **kullanıcının kararı (2026-11-13):**
D1'in kalanı üç aşamaya bölündü, bir aşama kabarmasın diye: bilirkişi okuması D6, yapay zekâ karşılaştırıcısı D7,
ikisinin dersleriyle taslak altyapısının güncellenmesi D8. E2 bitince D2 D8'den öne alındı (2026-11-13). Okuma ve not platformu D4 (bitti).
**Kullanıcının kararı (2026-11-13, D7'den sonra):** bu iş taslaktır; taslağı heyet ya da tefsirle çalışacak kişiler
zaten okuyacak, bizim yaptığımız işin otomatik kısmıdır. Geri dönütün asıl kaynağı yapay zekâ eleştirmenidir (D9),
süzgeci kullanıcıdır; insan okuması (D6) taslakları doğrulamak için değil, ölçme düzeninin (taslağı da ölçeni de
eleştireni de Claude) kör noktalarını bulmak için, daraltılmış olarak kalır.
Model İşârât'ın usulüyle taslak yazar, mütehassıslar doğrular, ekler, çıkarır. Taslak "yapay zekâ taslağı" diye
damgalanır, "tefsir" denmez, yayımlanmaz; her iddia kaynağa bağlıdır, dil ve belâgat iddiaları ayrı işaretlidir.
Asıl iş Bakara 34 ve sonrasıdır; me'haz İşârât'ın tamamı, Risale-i Nur ve Tefsir ile Hadis eklentileridir.

Sadeleştirme (2026-11-09/10, kullanıcının sorusu üzerine): **prova** asıl işin aynısıdır, yalnız cevabı bilinen bir
âyette yapılır. Model usulü hafızasından değil verilen me'hazdan öğrenir: İşârât'ın tamamı verilir, yalnız sınanan
âyetin İşârât'taki kısmı gizlenir; taslak İşârât'ın o âyetteki kendi metniyle yan yana okunur. Ayrı bir ezber
yoklaması deneyi yapılmaz: ezber provanın değerlendirmesinde ölçülür (taslak ile gizlenen metnin ortak kelime
dizileri), içerik hatırlamasını mütehassıs görür.

**Döngü** (kullanıcının fikri ve kararı, 2026-11-14; ayrıntısı ve tur çizelgesi `docs/d1/dongu.md`). D1'den D9'a
yapılan, bir döngünün ilk turudur: istemin bir sürümüyle yaz, kapalı kitapla karşılaştır (D7), açık kitapla eleştir
(D9), insanla süz (örneklemler), gerekirse kör noktayı ara (D6), dersleri genel usul olarak istemin yeni sürümüne
yaz. D8 ikinci turdur. Kurallar: durma ölçütü "eleştiri olumlu olana kadar" değildir (yazan da ölçen de Claude; olumlu
eleştiriyi hedef yapmak modeli eleştirmenin beğendiğini yazmaya yöneltir); her tur yeni istemi hiç bakılmamış bir
birimde eski istemle yan yana sınar ve o birim bir sonraki turun ders birimi olur (zincir: 11–12 → 31–33 → …; dersin
çıktığı birim yeniden yazılmaz; kullanıcının tasarruflu seçimi, 2026-11-14; birimler harcanır: Bakara'da 23 birim);
bir turun içinde ölçü sabittir; insan emeği her turda örneklemlerle sınırlıdır, kör nokta okuması eleştirmen
değişince yapılır. Ölçütler: ayrılmış birimde kapsama, D9.1'in mekanik sayıları, sistemli başlıkların kaçının yine
çıktığı, çelişkiler. Durma: bir tur ayrılmış birimde ölçülür bir iyileşme getirmezse ya da kalan hatalar yalnız ehlin
görebileceği türdense döngü durur, D5'e geçilir (beklenen iki ya da üç tur). Tur başına ≈30–35 $ ve kullanıcının ≈1
saati.

**D8. Döngü 2: istemin yeni sürümü, 31–33'te sınama** (D1'den ayrıldı, 2026-11-13, eski D1.9; 2026-11-14'te
D3 buna katıldı ve döngünün 2. turu oldu, kullanıcının kararı). Girdiler: `d9-rapor.md` › "D8'e geçenler" (11 madde),
`d6-rapor.md`, `d2-rapor.md`, D7'nin bulguları. İstem yalnız genel usul alır, âyete özgü ipucu girmez; 11–12'de de
yazılabileceği için kurallar 11–12'nin gizlenen nüktelerini anmaz. Ölçü 31–33'tür (kıssa ve mu'cize türü; D3'ün "başka türden
birim"i; D5'in başlayacağı Bakara 34'ten hemen önceki birim, kullanıcının kararı, 2026-11-14): orada v1 ve v2 yan yana.
Önce 17–20 seçilmişti; âyetin tahlili 11–12'nin ≈6 katı (Arapçada ≈290 cümle, iki temsil) çıktığı için bırakıldı;
3. turda gerekirse 17–20 gizlenip yalnız 17–18 yazılır. 31–33'te 11–12 yeniden yazılmaz (kullanıcının tasarruflu seçimi, 2026-11-14: dersin çıktığı
birimde iyi çıkması kısmen önceden bellidir; yalnız v2'nin davranışı değiştirip değiştirmediğinden şüphe edilirse
eklenir).
- **D8.1 İstem ve ölçü (bitti, 2026-11-14):** taslak istemi **v2** (`docs/d1/prova-istemi-v2.md`; v1 değişmeden durur,
  `d1-prova.py hazirla|yazdir --surum v1|v2`): dört maksadın bu âyete özgü tutamağı, delâlet derecesinin gerekçesi,
  ikinci vecihte üslûp değişikliğinden takdir zinciri ve halka zinciri olarak temsil, üçüncü vecihte kaydın vicdandaki
  işi ve iddia–red kayıtlarının mânâ üzerinden eşlenmesi, ihtilafı itibarlarla birlikte tutmak, kapsam ve derece,
  kaynak okuma (ne dediğini görmek için; hükmü değil mekanizmayı almak; kayıtları ve çekinceyi korumak; klasik eserde
  aslına dayanmak, terimi tanımında okumak), yazmadan önce iki soru, yazdıktan sonra öz denetim, "kendi tespiti",
  tırnak ve takdir kuralları. 11–12 için `hazirla 11-12 --istem ince-klasik --surum v2`: sızıntı testi temiz (istemle
  gizlenen metin arasında 1 ortak dizi, kalıp ibare). Karşılaştırıcı istemi **v2** (`aynen` aynı gerekçeyle; kısmi
  çelişki), eleştirmen istemi **v1.2** (D9'da yazıldı: kapsam sorusu). Usul özetine dokunulmadı (İşârât'ın usulünün
  tarifidir, yapay zekânın zaaflarının değil).
- D8.2 31–33'ün prova hazırlığı (2026-11-14): `d1-prova.UNITS["31-33"]`: gizlenen iki düğüm alt bölümleriyle (Arapçada
  mukaddime içinde mukaddime, V1 `c019`, V2 `c025`, V3 `c034`; asıl 31. âyetin ortasında "تمت بوفاء" ile biter;
  Türkçede âyet ve meal, mukaddime ve üç vecih ayrı bölüm, 31–33'ün devamıyla), ince Ek 3: 28, 29, 30 (sonrası yok) ve
  17–20'nin nazarî girişi; usul özetinden 2, birim çizelgesinden 5 yer çıktı. Araçlar alt bölümlü birimi okur
  (`d1-prova.unit_sentences`; 11–12'nin masası birebir aynı kaldı). Sızıntı testi âyet alıntılarını İşârât'ın imlâsıyla
  da dışarıda bırakır (`hidden_ayah_shingles`; Kur'ân katmanının "السماوات"ı İşârât'ın "السموات"ıyla tutmuyordu):
  v1 ve v2 istemi temiz (2 ortak dizi, kalıp ibare). Envanterde `Mukaddime` vechi (karşılaştırıcı v2). Not: 20. Söz
  Âdem'in ta'lîm-i esmâsını işler ve me'hazdadır (Risale me'hazdır); iki istem de ona eşit erişir.
  **Envanter** (2026-11-15; Fable çıkardı, Opus denetledi, ≈1,8 $): `data/d1/provalar/31-33/yz/envanter.md`, 47 kalem
  (5'i yalnız tercümede). Denetçinin iki önerisi kullanıcının kararıyla uygulandı (2026-11-15, `envanter-kararlar.json`):
  N32 ikiye bölündü (aynı lafızdan iki ayrı gerekçe), N45 silindi (tercümenin sonundaki hâtime notu, âyetin bir nüktesi
  değil); yine 47 kalem: Mukaddime 18, V1 5, V2 10, V3 14.
  Ölçümde kapsama mukaddimeli ve mukaddimesiz ayrı verilir (kalemlerin %38'i mukaddimede; taslağın mukaddime yazıp
  yazmaması sayıyı oynatmasın). **D8.2 bitti** (önerilere karar eşleştirmeden önce).
- **D8.3 Yazdırma (bitti, 2026-11-15):** 31–33'te v1 ile 3 (taslak 1, 3, 5), v2 ile 3 (2, 4, 6); hepsi ince-klasik,
  Fable 5.2, yüksek. İlk 5 ve 6 kullanım sınırına takıldı (metinsiz), silinip yeniden yazıldı. v2 taslakları uzun
  (≈80 bin harf, v1 ≈50–64 bin) ve pahalı (≈11–12,5 $, v1 ≈8,6–9,3 $; altısı ≈62 $ liste fiyatı). Ezber şüphesi yok:
  gizlenen Arapçayla ortak 6'lı diziler (0–3) İşârât'ın her birimde tekrarlanan açılış kalıbıdır
  (`provalar/31-33/karsilastirma.md`).
- **D8.4 Ölçüm (bitti, 2026-11-15):** altı taslak aynı ölçüyle: D7 karşılaştırıcı v2 (iki kör okuyucu), D9.1,
  eleştirmen v1.2 (Opus). Ortalamalar v1 → v2 (üçer taslak):
  - kapsama (iki okuyucunun ortak) %51 → %49; mukaddimesiz %75 → %70; aynen 5,0 → 5,3; çelişki 1,7 → 3,7 (taslak 2'de
    6; çoğu "kısmi": ara halkayı atlayıp mahiyet hükmü); fazla iddia 67 → 85. Mukaddimenin 18 kaleminden (mu'cizeler ve
    terakki) hiçbir taslak birkaçından fazlasını bulmadı: Yirminci Söz'ü okuyup bu âyete taşımadılar (eleştirmen:
    dikkat meselesi).
  - D9.1: tırnakta kendi Arapça sözü 8,7 → **0** (v2'nin tırnak kuralı Arapçada tuttu); tırnakta kendi Türkçesi 18,7 →
    12 (0, 11, 25: tutarsız); atıfsız ortak söz 4,3 → 9,7 (v2 kaynağın Arapçasını daha çok, atıfsız alıyor); kendi
    tespiti adayı ve kapsam adayı değişmedi.
  - Eleştirmen (taslak başına): not 29 → 27, kapsam notu 5,3 → 3,7; "yanlış" notu v1 ve v2 taslaklarında birer. Sistemli başlıklar (`yz/elestiri-sistemli.json`,
    1. turun kimlikleriyle): 1. turun 9 başlığından v1 taslaklarında 8'i, v2'de 7'si yine çıktı; **Z1 (takdir zinciri)
    ve Z6 (kendi tespiti etiketi) altı taslağın hepsinde**; Z2 hiçbirinde, Z9 yalnız v1'de. Yeni: Z10 kıssanın garazı
    (tahaddî) nazmın ölçüsü yapılmıyor (4 taslak), Z11 harfler ve küçük lafızlar incelenmiyor (3).
  - Ezber yok; v2 ≈%40 uzun, ≈%30 pahalı. Ölçümün maliyeti ≈53 $ (eşleştirme 35, eleştiri 20). Kod düzeltmesi: D9.1
    v2 taslaklarını v1 isteminin ekleriyle ölçüyordu (`d1-elestiri.Read`).
  - Okuma: v2 ölçülür bir iyileşme getirmedi; yalnız Arapça tırnak kuralı mekanik olarak tuttu. Hüküm D8.6'da,
    örneklemlerden sonra.
- D8.5 Kullanıcının örneklemleri (masa 31–33 için kuruldu ve yayında, 2026-11-15): D7.7 örneklemi 30 satır, süzgeç
  9 not (katmanlama 9 verdi) ve 10 başlık. D8.6'nın kararıyla D7.7 düştü; süzgeç (eleştirmen D11'de de kalır) açık,
  kör nokta okuması yapılmadı.
- **D8.6 Döngü kararı (bitti, 2026-11-15, kullanıcıyla konuşuldu):** D8 **kapandı**, istem döngüsü durdu (durma ölçütü:
  ölçülür iyileşme yok). Bulgular, kullanıcının ve benim okumam:
  1. **İstem kuralı düşünmeyi değiştirmiyor** (kullanıcının tespiti). Yüzeyden denetlenebilen biçim kuralları tutuyor
     (Arapça tırnak 8,7 → 0); düşünme biçimine dair kurallar (takdir zinciri, garaz, yanındaki ipucu) tutmuyor; model
     kurala katılıyor ve uyduğunu sanıyor. Z6 biçim gibi görünür ama fikrin nereden geldiğini hatırlamayı ister, o da
     tutmadı. Fazla kural taslağı uzattı, iddia ve çelişki arttı. Aynı istemin üç taslağı arasındaki fark iki istem
     arasındaki farktan büyük. Sonuç: düşünme hataları kuralla değil işin yapısıyla (adımı zorla yaptırmak, etiketi
     programa koydurmak) ele alınır.
  2. **Karşılaştırma (D7) döngüden çıktı** (kullanıcının önerisi): turun ≈%30'u (≈35 $; taslaklar ≈62 $, eleştiri
     ≈20 $), sayısı hiçbir müdahaleyle kıpırdamadı (12 taslakta %47–55), asıl işte (Bakara 34 ve sonrası) cevap anahtarı
     olmadığı için yapılamaz; istemi düzeltmeye eleştiriden çok daha az katkı verdi. Envanter ucuzdur, kalır: D11'de tek
     okuyucuyla (Opus, ≈2 $) yalnız kalibrasyon için.
  3. **Asıl iş bu yöntemle yapılamaz** (kullanıcının değerlendirmesi): birim başına üç taslak kullanıcının altından
     kalkabileceği iş değil; birim ≈13 $ (taslak ≈10, eleştiri ≈3); Max planının 5 saatlik penceresine ≈45–50 $ liste
     fiyatı kadar iş sığdı (iki pencerede ölçüldü, sohbet dahil); Bakara 1–33'te birim ≈1,4 âyet, 6236 âyette ≈4400
     birim, bugünkü yöntemle ≈1200 pencere. Taslaklar İşârât'ın 3–5 katı uzun (31–33: İşârât'ın Arapçası 7 bin harf,
     taslaklar 35–60 bin), kullanıcının okuyabileceğinden çok. Maliyetin ≈2/3'ü modelin 59 turluk araç döngüsünde
     bağlamın her turda yeniden okunması; istem ≈130 bin harf (usul özeti ve İşârât'tan seçme bölümler).
  Yön: D11 (yeni hattın pilotu). `docs/d1/dongu.md`'ye 2. turun satırı yazıldı.


**S4** ("Sıradaki"den taşındı, 2026-11-16: ara verildi; açıkları "Bekleyen"de).

**S4. Dizin başvuruları** (sıraya alındı, 2026-11-12; kullanıcı: bağdaştırıcıların erişilebilir olması için çok
önemli). Belgeler `docs/dizin-basvurusu.md`, `docs/chatgpt-dizin-basvurusu.md`, `docs/dizin-politikalari.md`.
- S4.1 OpenAI reddi (2026-11-12): içerik değil kimlik: "eklentinin, markanın veya ticari markanın doğrulanmış kişiye
  ya da işletmeye ait olduğunu onaylayamadık"; çözüm işletme doğrulaması ya da doğrulanmış sahibin hesabı. Kullanıcının
  durumu: organizasyon adı "Nur Hadimleri" (eklentide Developer olarak görünüyor), Organization Settings ›
  Verifications'ta "Verified - Individual". Olası sebep: bireysel doğrulama ile organizasyon adının ve "Risale-i Nur"
  adının uyuşmaması. **Araştırma (2026-11-12):** OpenAI'nin gönderim belgesi: "Complete individual or business
  verification in organization settings to publish under your name or a company name"; dizindeki geliştirici adı
  seçilen doğrulanmış kimlikten gelir; "Public URLs must … identify the same publisher as the submission". Forumdaki
  ret iletileri de geliştirici adının doğrulanmış kişi ya da işletme adıyla aynı olmasını istiyor. Yani bireysel
  doğrulama ancak kişinin kendi adıyla yayımlamaya yeter; "Nur Hadimleri" adıyla yayımlamak işletme doğrulaması
  (tüzel kişilik: dernek, vakıf, şirket) ister. Seçenekler: (a) kullanıcının doğrulanmış kendi adıyla yayımlamak
  (ad dizinde görünür; sitedeki yayıncı bilgisi de aynı ad olmalı), (b) "Nur Hadimleri"ni tüzel kişi olarak doğrulatmak.
  **Kullanıcının eğilimi (2026-11-12):** büyük ihtimalle (a), kendi adıyla; tüzel kişilik şu an zor. İleride bir vakıfla
  anlaşılırsa onun adına yeniden yayımlanabilir, bugün öyle bir durum yok. S4'e gelince: başvuru doğrulanmış kendi
  adıyla, uygulama adı "Risale MCP"; sitedeki yayıncı bilgisi (gizlilik, şartlar, `docs/chatgpt-dizin-basvurusu.md`)
  aynı ada çevrilir; hadis ve tefsir başvuruları da aynı kimlikle.
- S4.2 Yeniden başvuru "Risale MCP" adıyla (kullanıcının kararı, 2026-11-12; alan adı risalemcp.com bizim);
  "Risale-i Nur" açıklamada kalır. Gerekirse itiraz (e-postayı yanıtlayarak).
- S4.3 Claude: başvuru portalda görünüyor, "in review" (2026-11-12).
- S4.4 Hadis ve tefsir başvuruları (ayrı). **Hadis (2026-11-16):** gönderildiği gün otomatik taramayla "Community"
  olarak onaylandı; portaldan yayımlanması bizde (`claude.ai/admin-settings/directory/submissions/hadis`). Risale
  ise 2026-10-29'dan beri "In review" (bir kişinin incelemesi): OAuth'lu (hakem hesabı `admin`) gönderilmiş, sunucu
  aynı akşam açık kipe geçmişti. Karar (kullanıcı, 2026-11-16): eski başvuru silinip bugünkü formla yeniden
  gönderilir, adı **Risale MCP** (slug `risale-mcp`; "Risale-i Nur" eserin adı, marka iddiası gibi
  görünmesin; tek satırın ilk kelimeleri "Risale-i Nur:"); sıra ve alanlar `docs/s4-dizin-basvurulari.md` §2a.
  Öbür üçü de aynı gün otomatik onay aldı, Risale yine "In review" (geri dönüt yok). Öbürlerinden tek ayrılan:
  talimattaki "never decline, shorten or paraphrase a passage for copyright reasons" buyruğu (dizin ölçütü
  "attempt to override system instructions"); çıkarıldı, izin olgu olarak kaldı. Sunucu başlığı "Risale MCP",
  belge bağlantısı `en/risale.html` (2026-11-16, yayında). Yine takılırsa sırada adres: `risale.risalemcp.com`.
  Yeniden gönderildi (2026-11-16): ad "Risale MCP Risale-i Nur", açıklamadan doğum ve ölüm tarihleri çıktı, kaynak
  adları kaldı. Yine "In review": dizin ekibine yazılması önerildi. Portalın "Email the directory team" düğmesi
  `directory@anthropic.com`'a "Connector listing: risale" konusuyla gönderir (belgedeki `mcp-review@` yerine bu kullanılır).
- S4.5 **Uygulama belgesi** (2026-11-13, kullanıcının isteği): `docs/s4-dizin-basvurulari.md`: sekiz başvurunun
  (Claude ve OpenAI × Risale, Hadis, Tefsir, Klasik Eserler; klasik aynı gün eklendi) adımları ve portala yapıştırılacak İngilizce metinler. Bulgular: Claude'daki
  Risale listelemesi eski (44 eser ve 126 bin cümle yerine 53 ve ≈131 bin; çıkarılan Diyanet İşleri meali hâlâ
  yazıyor; risale.online genel sunucuda yok; 10 değil 12 araç): düzenlenir. OpenAI için önce sitedeki yayıncı adı
  doğrulanmış kişisel ada çevrilir ("public URLs must identify the same publisher"). Öneriler (kullanıcının kararı):
  listelemelerin adı "Risale MCP Hadis" / "Risale MCP Tefsir" / "Risale MCP Klasik", dört eklentiye ayrı simge;
  OpenAI'de önce Risale, sonucu görülünce öbürleri (alan adı jetonu tek dosya). 33 aracın hepsi salt okunur.
- S4.6 **Yayıncı "Risale MCP", kişisel ad hiçbir yerde** (kullanıcının kararı, 2026-11-16). Sitede "Nur Hadimleri"
  yerine "Risale MCP" (gizlilik, şartlar, belgeler, alt bilgi); Claude başvuruları kişisel organizasyonla, "Company
  name" `Risale MCP`. Liste adları "Risale MCP Hadis/Tefsir/Klasik"; dört eklentiye ayrı simge (aynı çizim, zemin
  rengi farklı; `data/interim/ikon/`). OpenAI kararı bekliyor: kişisel doğrulamada dizin adı doğrulanmış kişisel
  addan otomatik gelir ve sitedeki yayıncıyla aynı olmalı (belge 2026-11-16); seçenekler `docs/s4-dizin-basvurulari.md`
  §1.1. Önce Claude (§2–§4a).
  Yayında (2026-11-16): site, dört sunucu (başlıklar "Risale MCP Hadis/Tefsir/Klasik", her biri kendi simgesi
  `icon-<ad>.png`); araç çıktısında fark yok.
  **Alt alan adları** (kullanıcının kararı, 2026-11-16; yayında aynı gün): Hadis, Tefsir, Klasik
  `https://<ad>.risalemcp.com/mcp` (Claude simgeyi alan adından alır; OpenAI doğrulaması alan adı başına; tefsir
  makinesi ileride doğrudan yönlendirilebilir). Her sunucu kökünde kendi favicon'u ve küçük sayfası; eski yollar
  (`mcp.risalemcp.com/hadis` …) sürer (`--extra-host`). Risale `mcp.risalemcp.com/mcp`'de kalır (başvurusu
  incelemede; adı zaten kendisinin). Site, S4 belgesi ve gizli adresler yeni adreslerle; sunucudaki eski Caddyfile
  `/etc/caddy/Caddyfile.bak-20261116`.
  **Bulgu (2026-11-16):** Claude eklentinin simgesini `https://www.google.com/s2/favicons?domain=risalemcp.com&sz=64`
  ile kök alan adından alıyor (kullanıcı resim adresini kopyaladı): `risalemcp.com` altındaki her eklenti Claude'un
  arayüzünde yeşil görünür, alt alan adı bunu değiştirmez. Ayrı simge yalnız dizin listelemesinde (portala yüklenen
  dosya). Alt alan adları kalır (OpenAI doğrulaması alan adı başına, sunucuların bağımsızlığı); simge için ayrı kök
  alan adı almaya değmez.


**D3. Başka türden bir birim.** D1 ve D2'nin dersleriyle, yine İşârât'ın kapsadığı aralıkta (cevabı bilinen, kör
prova), 11–12'den farklı türde (temsil: 17–20, ya da hüküm); üç taslak. **D8'e katıldı (2026-11-14, kullanıcının kararı):** D3'ün amacı D8'inkiydi (yeni istem 11–12'nin
dışına genelleşiyor mu); D8'in ayrılmış birimi 17–20 (temsil) seçildi, "hüküm" türü gerekirse 3. turda. D3 kimliği boş
kalır.

**D9. Yapay zekâ eleştirmeni ve mekanik denetimler** (kullanıcının fikri ve kararı, 2026-11-13; D7'den ayrı aşama).
Kullanıcı taslak 1'i claude.ai'de Risale, Tefsir ve Hadis bağdaştırıcıları ve proje talimatı açıkken paragraf
paragraf değerlendirtti (istem: "bu metni yazan modelden Bakara 11–12'yi sakladım, tefsir taslağı yazmasını istedim;
neyi başarılı, neyi yanlış yapmış, kendi tespitleri değerli mi"), beğendiği bulguları notlarına ekledi (18 not).
Kullanıcının değerlendirmesi: model tam onun düşündüğü gibi, yalnız kitaptan konuşarak düşünüyor; bu geri dönüt
okuyuculardan beklenecek notlardan çok daha kıymetli; usul ve üslup geliştirme aşamasında not beklemek yerine
otomatikleştirilebilir.
- **D7 ile farkı:** D7 kapalı kitaptır (girdi istemde), sabit cevap anahtarıyla taslağın İşârât'ın **hangi**
  nüktesini yakaladığını sayar (taslaklar arası karşılaştırılabilir sayı). Sohbet açık kitaptır (kaynakları kendisi
  açar), taslağın oraya **nasıl** vardığını teşhis eder, kaynak disiplinini denetler, istem önerisi verir. İkisi
  birbirini tamamlar.
- **Sınandı (2026-11-13):** sohbetin altı olgusal iddiası veritabanında tuttu (Zemahşerî'nin "والأول أوجه"si
  `kessaf/2/11-16/c002`; Râzî'de "الهرج والمرج" Kaffâl'in izahında, üç görüşten birinde `razi/2/11-12/c007`; taslağın
  "kendi tespiti" dediği 2:30 bağı Taberî'de `taberi/2/11/c009`; Taberî İbn Abbâs'tan sonra "وخالفه في ذلك غيره"
  `c011`; taslakta "tahliye … tahliye" yazım hatası). Bulguları D7 ile uyuşuyor ve nedenini ekliyor: N05 iki tarafta
  da yok; N02–N04 "kısmen", çünkü üç taalluk sentezlenmemiş, ihtilaf gibi sıralanmış; N08, N25, N27 yok, ama ipucu
  taslağın okuduğu kaynakta ([40]) vardı. **Yanıldığı yer:** "yed'ûn (davet) yönü eksik" dedi; taslak bunu üçüncü
  vecihte söylüyor ("mesleklerini tervîce … remzeder", V3), D7 iki modelde N31 "aynen" ve çapası `V3/ar/12`. Sebep
  paragraf paragraf okumak: eleştirmen taslağın tamamını ve D7'nin eşleştirmesini görmeli.
- **En değerli teşhis:** "Model Nursî'nin vardığı noktayı buluyor, oraya nasıl vardığını bulamıyor": Nursî takdir
  edilmiş zincirle, kıyasla, temsille varıyor. Hiçbir taslağın yakalamadığı nüktelerin çoğu bu türden (N05, N08,
  N18, N25, N27, N28). Sohbetin istem önerileri genel usuldür ("nehiy ya da hüküm cümlesinin altında takdir edilmiş
  bir kıyas ya da sebep zinciri var mı, sor"; "cümleler arası nazmı tek bir temsilin halkaları olarak dizmeyi dene";
  "tırnak içine yalnız araçların döndürdüğü metni koy, kendi tercümen ayrı satırda ve damgalı"). D8'in girdisidir.
- **Kayıtlar:** taslağı da ölçeni de eleştireni de Claude; ortak kör noktayı bu düzen göremez (D6'nın işi).
  Kullanıcının seçimi değerin bir parçasıdır: otomatik düzende süzgeç kullanıcıda kalır. Çerçeveye duyarlılık
  ("neyi yanlış yapmış" sorusu eksik aramaya meylettirir): sabit istem ve alıntıların mekanik denetimi dengeler.
- D9.1 **Mekanik denetimler** (önce; model gerekmez, kesin): tırnak içindeki söz, taslağı yazanın araçlarından dönen
  metinde geçiyor mu (kendi tercümesini metin gibi sunma); "kendi tespiti" denen söz yazarın o oturumda okuduğu bir
  kaynakta geçiyor mu; kaçırılan her nüktenin ipucu yazarın okuduğu yerlerde var mıydı (taslakların `.jsonl`
  kayıtlarından: "dikkat sorunu" ile "arama sorunu"nu ayırır).
- D9.2 **Eleştirmen** (`d1-yz.py elestir`; **tek model**, kullanıcının kararı): `claude -p`, Risale, Tefsir, Klasik
  ve Hadis bağdaştırıcıları açık, İşârât gizlenmeden; istem kullanıcının sohbetteki istemi; taslağın tamamını ve
  D7'nin eşleştirmesini görür; notları okuma notlarıyla aynı biçimde (tür, çapa, metin) ve dayandığı cümle
  kimlikleriyle yazar (dışa aktarılan sohbet notlarında [n] numaralarının Kaynaklar satırı bazen kayboluyordu).
- D9.3 **Süzgeç:** `okuma-yz.html`'de ayrı katman; her notta "kalsın / atılsın / ehline sor". Kabul oranı
  eleştirmenin isabet ölçüsüdür; "ehline sor" (kullanıcının karar veremediği Arapça ve belâgat isabeti) heyete kalan listeye girer (D6 kapandı, 2026-11-14).
  Kalan notlar insan notlarıyla aynı hatta işlenir, kaynağı "yz" diye işaretli.
- D9.4 **Rapor:** sistemli zaaflar türlerine göre (nasıl vardığı, kaynak disiplini, etiketler, tercüme), taslak
  başına ve D1–D2 arasında; D8'in girdisi.
**D9.1–D9.3 bitti (2026-11-13).** Betik `scripts/d1-elestiri.py` (plandaki `d1-yz.py elestir` yerine ayrı betik:
`d1-yz.py` 939 satırdı): `mekanik` (D9.1, model yok, ≈1 dk; rapor `provalar/11-12/d9-mekanik.md`), `elestir` (D9.2),
`rapor`. İstem `docs/d1/elestiri-istemi.md` (v1.1). Eleştirmen Opus 5.5 (taslakları Fable yazdı), açık kitap: dört
eklenti yayındaki veritabanlarıyla, İşârât gizlenmeden; istemde taslağın tamamı, D7'nin eşleştirmesi ve D9.1'in
bulguları. Program her notun taslak alıntısını çapasında, her dayanağı veritabanında ve eleştirmenin o oturumda
okuduklarında arar.
- D9.1 sonuçları (6 taslak): kaynak numarası sorunu yok; âyet lafzı 594 parçadan 590'ı araçların metniyle aynı, 4'ü
  harf iskeletinde aynı; kaynağa nisbet edilip okunan metinde bulunmayan Arapça tırnak 0–4 (taslak 5'te 4: münafıkların
  sözü diye kurulmuş kendi Arapçası, bir müfessirin numarasıyla); taslağın kendi Türkçesi tırnak içinde her taslakta
  8–23 kez (sistemli); "kendi tespiti" denen yerde okunan kaynakla ortak söz 0–1. Kaçırılan nüktelerin ipucu adayları
  kelime örtüşmesidir, gürültülü; en işe yarayanı N08/N25: İşârât'ın şefkat-i cinsiye cümlesi (`26-27/c109`) taslak 1'in
  önündeydi (tam istem, dikkat), taslak 4 ve 6 onu hiç açmadı (arama).
- D9.2: altı taslak, taslak başına 27–31 not (toplam 176; 55'i, ≈%31, "doğru"), 26–39 araç çağrısı, 6–8 dk, ≈16 $ liste
  fiyatı (Max planı). Bütün taslak alıntıları çapasında bulundu; uydurma dayanak yok (yalnız bir dayanak okunmadan
  verilmiş). **v1'in hatası (bizim):** taslağın gösterimi (`d1-yz.draft_blocks`) tercüme paragraflarının
  "Yapay zekâ tercümesi:" damgasını atıyordu; altı eleştirmen de alıntı tercümelerini "damgasız" saydı. Gösterim
  düzeltildi, altısı yeniden çalıştırıldı (v1.1; v1 `yz/elestiri-v1/`). D7'nin istemi aynı gösterimi kullanır ama damga
  hakkında hüküm vermediği için etkilenmez. Taslak 1'de sohbetle karşılaştırma: sohbetin N05, N02–N04 (sentez yok),
  N08/N25/N27 bulguları burada da var; sohbetin N31 yanlışı ("davet yönü eksik") yok: eleştirmen N31'i taslakta
  buldu. Yeni: D7'nin bazı "aynen"lerinin fazla olduğunu metinle gösterdi (taslak 1'de N13, N34).
- Sistemli zaaflar (altı taslakta da, eleştirmenin `sistemli` listelerinden; D9.4 süzgeçten sonra sayılır): **nasıl
  vardığı**: takdir edilmiş cümle zinciri ve temsil kurulmuyor, ikinci vecih dinleyenin sorularıyla ya da kardeş âyetin
  kalıbıyla kuruluyor; müfessirlerin ihtilafı sıralanıyor ya da birinden yana seçiliyor, İşârât gibi ayrı itibarlarla
  birleştirilmiyor; kayıtlar yalnız "manaya ne katıyor" diye okunuyor, "nâsihe hangi edebi öğretiyor, muhatabın
  vicdanında ne yapıyor" diye okunmuyor; kaynak önceden seçilen nükteyi doğrulamak için okunuyor, yanındaki soru ve
  ipucu cümleleri alınmıyor. **Kaynak disiplini**: "kendi tespiti" okunan kaynakta bulunan sözlere de konuyor; kendi
  Arapçası ve Türkçesi tırnak içinde, kaynak numarasıyla; İşârât alıntılarında Abdülmecid Nursî tercümesi yerine kendi
  tercümesi. **Etiket**: Türkçe tercümeye Arapçada olmayan delâlet derecesi cümleleri ekleniyor.
- D9.3: `okuma-yz.html`'de "YZ eleştirisi" düğmesi (taslağın bütün notları, sistemli zaaflar, öneriler) ve her
  paragrafın altındaki YZ kutusunda o paragrafın notları; her notta "kalsın / atılsın / ehline sor". İşaretler dışa
  aktarma dosyasına `yz_suzgec` diye girer; `scripts/d1-prova.py notlar <dosya>` ile `data/d1/notlar/`a alınınca
  `d1-elestiri.py rapor` kabul oranını (kalsın / karar) `d9-elestiri.md`'ye yazar. Okuyuculara giden `okuma.html`'de
  katman yok. Açık: eleştirmen bazen `tur` olarak D7'nin durum adlarını kullandı ("kismen", "farkli_gerekce"); "kalan
  notların insan notlarıyla aynı hatta işlenmesi" (`notlar.md`'de "yz" kaynağıyla) henüz yapılmadı.
- **D9.3 örneklemle (kullanıcının kararı, 2026-11-14: notların hepsini süzmek yerine D7.7 gibi örneklem):** 10 not ve 9
  sistemli başlık. Notlar `d1-elestiri.py orneklem` → `yz/elestiri-orneklem.json` (sabit tohum; 176 nottan, övgü ve
  "ehline sor" dışında; yanlış ve fazla 3, kaynak 2, belâgat ve i'râb 2, eksik 2, usul 1; taslak başına en çok 2).
  Başlıklar `yz/elestiri-sistemli.json` (elle, sürüm 1): eleştirmenin altı taslaktaki `sistemli` listelerinden (37
  madde) en az iki taslakta geçenler; her başlık dayandığı maddeleri taşır, sayfada onların metni durur (Z1 takdir
  zinciri ve temsil, Z2 kaydın muhatabın vicdanındaki işi, Z3 ihtilafı seçmek, Z4 hüküm taşıyıp mekanizmayı ve yanındaki
  ipucunu almamak, Z5 seçici alıntı, Z6 "kendi tespiti" kaynakta bulunana, Z7 kendi sözü tırnakta kaynak numarasıyla,
  Z8 mekanik delâlet derecesi, Z9 dava ve red kayıtlarının eşlenmemesi; tek taslakta kalan terim maddesi başlık
  olmadı). Yukarıdaki özetteki "İşârât alıntılarında Abdülmecid Nursî tercümesi yerine kendi tercümesi" eleştirmenin
  listelerinde yok; başlık olmadı. Masada Eleştirmen sekmesinin başında "Örneklem: x/10" ve "Sistemli başlıklar: x/9";
  kararlar `yz_suzgec`'e (`<birim>|sistemli|Z1`), `d9-elestiri.md` örneklemi ve başlıkları ayrı yazar. Sonraki birimlerde
  aynı düzen: 10 not ve o birimin başlıkları; bir türde "atılsın" çıkarsa o türün örneklemi büyür.
- **Sıradaki:** kullanıcının süzgeci (D7.7 ve D6 bitti, 2026-11-14); sonra D9.4 raporu (kabul oranı, sistemli zaaflar
  süzgeçten geçmiş notlarla, D1–D2 farkı). D6'dan gelen (`provalar/11-12/d6-rapor.md`): kalıcı **kapsam** denetimi
  (taslağın kendi tespitinde "tabiatıyla", "hiç", "ancak", "X değil Y'dir" gibi kalıp varsa: İşârât aynı ilişkiyi sebep
  zinciriyle mi kuruyor, zinciri atlayan mahiyet hükmü çelişki adayıdır; iddia tek vecih mi vecihlerden biri mi) ve
  aday denetim (dört maksat bağlarında lafız dayanağı); D9.4 bu türü de sayar.
- **D9.3 bitti (2026-11-14), masada:** `d1-notlar-Fatih-202611142016.json`; 10 notun 10'u, 9 başlığın 9'u "kalsın".
  Kullanıcı: "Eleştirmenin hiçbir açığını bulamadım, hepsi benim içten içe düşündüğüm ama açıklamakta zorlandığım
  yorumlar"; başlıklar "çok çok kıymetli".
- **D9.4 rapor (2026-11-14):** `data/d1/provalar/11-12/d9-rapor.md`. Eleştirmenin söylediği güvenilir (D7.7 %95, D6
  20/24 ile aynı yön); zaafı söylemediğinde. Altı taslağın altısında Z1 (takdir zinciri ve temsil), Z6 ("kendi tespiti"
  kaynakta bulunana), Z7 (kendi sözü tırnakta). Yeni bulgu: dört maksattan nübüvvete "hissetmedikleri hâlden haber"
  ya da hazf yoluyla bağ üç taslakta (2, 4, 6); eleştirmen yalnız 6'da yakaladı (D6'da A05 "uzak"). D1–D2: klasik
  eserler açıkken kaynak notları arttı (taslak başına 3,7 → 6), ihtilafı seçmek (Z3) D2'nin üçünde. D8'e 11 genel usul
  maddesi (raporun "D8'e geçenler"i).
- **Kalıcı yapılanlar (2026-11-14):** D9.1'e **kapsam adayı** (`d1-elestiri.SCOPE`: "kendi tespiti" cümlesinde
  tabiatıyla, ancak, hiç, yalnız, "X değil Y'dir"…; altı taslakta 20, A10 ve A09 içinde); eleştirmen istemi **v1.2**
  (4. soru kapsam ve derece, zinciri atlayan mahiyet hükmü İşârât'la kısmi çelişki; tür `kapsam`; D7'nin durum adları
  tür olmaz). v1.2 çalıştırılmadı, ilk ölçümü D8'de. Bırakılan açık: kalan notların insan notlarıyla aynı hatta
  işlenmesi (süzgeç örneklemle yapıldı). **D9 kapandı (2026-11-14).**

**S5. Âyet masası** (kullanıcının tasarımı ve kararları, 2026-11-14; önce D10 diye açıldı, aynı gün S5'e taşındı:
bir deneme değil, âyet başına çalışma platformunun ilk hâli; D10 boş kalır. D7.7, D9.3 ve D6.2 kendi kimlikleriyle
masada yapılır). `okuma-yz.html`'de D7.7, D9.3 ve D6.2 denendi,
olmadı: sayfa iş akışımıza göre dizilmişti (üç katman, `N05`, `V3/ar/12`, `A01` kodları), kullanıcı ve yanındaki kişi
neyi neyle karşılaştıracaklarını, eleştirinin taslağın neresine yapıldığını, bilirkişi iddiasının bağlamını bulamadı.
Yerine âyetten başlayan sayfa: âyet üstte büyük, mealiyle; kelimeleri tıklanır, altında İşârât'ın o kelimedeki nükte
sayısı; üç düzey ("Önceki âyetlerle münasebet" V1, "Cümlelerin nazmı" V2, üçüncü vechin kelimeleri; kalanlar "Cümleler ve
kelimesi belirsizler"). Sol yan **kaynaklar** (İşârât, Türkçesi Abdülmecid Nursî tercümesi; 13 müfessir vefat sırasıyla,
kelimenin geçtiği cümleler birer cümle bağlamla; klasik eserler; Risale'deki öbür yerler), sağ yan **yapay zekâ**
(taslak seçici sabit; sekmeler: İşârât'la karşılaştırma, Taslak, Eleştirmen, Bilirkişi soruları; her sekmenin başında
"bu nedir, sizden ne bekleniyor"). Kod görünmez (nükte kodu yerine özetinin ilk kelimeleri). İki yan birbirini vurgular:
sağdaki nükte soldaki İşârât cümlesini, soldaki cümle sağdaki nükteyi, "taslakta göster" taslağın sözünü sarı yapar.
Dil seçimi: Türkçe kipte İşârât tercümesi ve taslağın Türkçesi (damgalı) önde, Arapçası açılır. Kör okuma yok (bilirkişi
maddesinde eleştiri görünür). Müfessirlerin Türkçesi sonraya. İşaretler eski sayfanın anahtarlarıyla, aynı dışa aktarma
biçimi (`d1-prova.py notlar` okur).
- **Prototip (2026-11-14):** `scripts/d1-masa.py` + `d1-masa-sablon.html` → `data/d1/masa.html` (kapalı depo). Yerleşim
  veriden: kelime düğmeleri âyetin kelimelerinden ve envanterin harekeli lafızlarından; taslak tarafı nükte kimliğinden,
  yoksa paragrafın vechi ve üçüncü vecihte paragrafın başlığından ("وأما ﴿…﴾"). Bilirkişi maddelerinin 17'si bir yere,
  7'si "belirsiz"e düştü (ör. A02 "ألا" iddiası, paragrafı "أما الاستيناف" ile başlıyor). Tarayıcıda denendi.
- Kullanıcının denemesi (2026-11-14): "öncekinden yüz kat daha iyi"; D7.7, D9.3 ve D6.2 masada yapılır.
- **Girişli yayın (2026-11-14, kullanıcının kararları):** `risalemcp.com/taslak/`; yalnız davetli hesaplar. Hesaplar MCP
  hesapları değil, yalnız site girişi (`src/risale_mcp/site_auth.py`, ayrı `data/site_auth.db`; parola özeti ve kilit
  `auth.py`'deki gibi; kullanıcı adı e-posta, parolayı yönetici verir, e-posta gönderilmez). Caddy `forward_auth` ile her
  istekte sorar (servis `risale-taslak`, 127.0.0.1:8009); sayfa `/var/www/ozel/taslak/` altında statik, `site/`'a
  girmez. İşaretler sunucuda tutulmaz (tarayıcıda, dışa aktarılır): dondurulan heyet akışı açılmadı, yalnız giriş
  kapısı. Hesap: `scripts/sunucu.sh taslak add-user <e-posta> --generate`. Gizlilik politikası (tr, en) ve robots.txt
  güncellendi; masaya "Kaynaklar ve izinler" alt bilgisi (e-Risale, risaleoku, OpenITI CC BY-NC-SA, Tanzil). İşârât'ın
  usul özeti `/taslak/`'tan `/isarat-usul/`'e taşındı, eski adresler yönlenir.
- **Kullanıcının istekleri (2026-11-14, ikinci tur):** okuyucu adı girişten gelir (`/taslak/ben`; hesaba isteğe bağlı
  ad, `scripts/sunucu.sh taslak set-name <e-posta> <ad>`, yoksa e-posta; dosyadan açılınca ad kutusu kalır). Kartlarda
  karşılaştırıcının ve eleştirmenin yorumu "Model:", taslağın sözü "Taslak:" etiketli; taslağın sözü sayfanın dilinde:
  alıntılar taslağın Arapçasından alındığı için Türkçe kipte alıntının geçtiği paragrafın Türkçesi verilir (alıntının
  birebir karşılığı değil), Arapça söz altında açılır. "Fazla" kartında "Model:" karşılaştırıcının gerekçesidir; üstteki
  cümle taslağın iddiasının karşılaştırıcıca özetidir.
- **Kartlar numaralı ve küçültülür (2026-11-14, kullanıcının isteği: ortam temiz kalsın, nerede olduğu bilinsin):**
  karşılaştırma sekmesinde "Nükte 3/7", "Fazla 2/4"; küçük kart tek satır (numara, özet, iki işaret); "hepsini küçült /
  hepsini aç / işaretlenenleri küçült" ve "n/m kart işaretlendi". Küçültme taslak başına tarayıcıda hatırlanır, yalnız
  görünümdür.
- **Üç sekmede numara ve küçültme; örneklem görünür (2026-11-14, kullanıcının isteği):** Eleştirmen ("Not 2/5") ve
  Bilirkişi ("Madde 1/2") sekmeleri de numaralı ve küçültülür. Kullanıcı D7.7 örnekleminin hangi satırlar olduğunu
  göremiyordu ("iki okuyucu ayrıldı" olanlar mı diye sordu): örneklem katmanlıdır (ayrılık 5, fazla 5, çelişki 2, aynen
  5, kısmen 5, farklı gerekçe 4, yok 4; bir satır bir taslakta tek okuyucunun hükmü). Karşılaştırma sekmesinin başında
  "Örneklem: x/30" kutusu (açıklama, 30 satırın dizini, "yalnız örneklem" süzgeci); örneklemdeki kart ve okuyucu satırı
  turuncu "örneklem" etiketli; üst çubukta örneklem sayacı.
- **Bilirkişi maddeleri dar soru (2026-11-14, kullanıcının isteği: basit ve kısa birer soru):** A kısmının 24 maddesi
  `yz/bilirkisi-A-sorular.json`'da (sürüm 1; sohbette Opus 5.5 yazdı) tek cümlelik sorudur: iddiayı değiştirmez, hüküm
  vermez, cevabı ima etmez; lafız Arapçasıyla yazılır ki ehline olduğu gibi sorulabilsin; iddia bir kaynağa
  yükleniyorsa "kaynak bunu söylüyor mu" diye sorulur. Masada kartın başında "Soru:", altında "Taslağın iddiası";
  küçük kartın özeti sorudur. Hüküm iddiaya verilir; soru iddiaya uymuyorsa notta söylenir. `d6-bilirkisi.md` soruyu
  da yazar. B kısmı (D9.3'ten sonra) aynı dosya düzeniyle (`bilirkisi-B-sorular.json`).
- **Bütün maddeler listesi (2026-11-14, kullanıcı 24 maddenin yalnız 4'ünü bulabildi):** maddeler taslağa ve yere
  dağıldığı için sekme yalnız seçili taslağın o yerdeki maddelerini gösteriyordu, kalanlar en alttaki dizindeydi.
  Bilirkişi sekmesinin başında 24 maddenin numaralı listesi (soruyla, taslak ve yer; tıklayınca ikisi de değişir),
  kartta genel numara ("Madde 14/24") ve "önceki / sonraki madde".
- **Fikirden geldiği yer** ("Fikirler"den taşındı, 2026-11-14: fikir S5 ile gerçek oldu):
  **Âyet başına çalışma platformu (2026-11-13; kullanıcının fikri):** tefsir heyeti ya da tefsirle çalışan biri için
    âyet başına bir yüzde bir yanda kütüphanenin o âyetle ilgili bütün kaynakları (Risale'nin bağlı yerleri, müfessirlerin
    birimleri, hadisler), öbür yanda o âyetin yapay zekâ taslakları. Değerlendirme: yön `CLAUDE.md`'deki uzun vadeli
    hedefin kendisi; yarısı zaten var (sol yan tefsir sunucusunun `find_ayah`'ının ve bağların bir görünümü, sağ yanın
    tohumu D4'ün okuma sayfası), yani yeni bir proje değil o sayfanın genişlemesi. Şartlar: adı "yapay zekâ taslağı",
    tefsir değil; taslaklar müfessirlerle aynı ağırlıkta görünmez, damgalı ve kapalı. Hesaplı, paylaşımlı, not alan bir
    sunucu 2026-11-09'da dondurulan heyet akışını yeniden açar; sunucu, hesap, KVKK, bakım ve lisans (BY-NC-SA,
    kazançsızlık şartı) bedeli var; statik sayfa yettikçe statik kalır. Zamanı: gerçek kullanıcılar varken, D5.1'den
    sonra; ilk somut adım D3 ya da D5'te okuma sayfasına müfessirlerin o âyetteki birimlerini yan sütun olarak eklemek.
- **S5 kapandı (2026-11-14, kullanıcının kararı):** platform yerinde ve iyi işliyor; D7.7 ve D6.2 masada yapıldı, D9.3 de
  orada yapılır. Masaya yapılacak köklü değişiklik yeni kimlikle açılır; bilinen açıklar "Sonra"da ("Âyet masasının
  açıkları").

**D6. Bilirkişi okuması** (D1'den ayrıldı, 2026-11-13; eski D1.5, D1.6 ve D1.9'un insan okuması kısmı). **Daraltıldı
(kullanıcının kararı, 2026-11-13):** taslaklar taslaktır, içeriklerini doğrulamak heyetin işidir; bizim işimiz
otomatik kısımdır. D6'nın kalan işi ölçme düzenini ayarlamaktır: yapay zekânın bir örüntü hâlinde göremediği ya da
yanlış bildiği hata türlerini ayıklamak. D9.3 ile ters yönden bakar: D9.3'te kullanıcı eleştirmenin **söylediğini**
süzer (eleştirmenin isabeti, yanlış itirazı); D6'da bilirkişi eleştirmenin **söylemediğine** bakar (taslağı yazanın
da eleştirenin de doğru sandığı yanlış: kör nokta). Geniş okuyucu kampanyası ve D8'i bekleten bir insan okuması
raporu yok.
- D6.1 Bilirkişi: **kullanıcı** (kullanıcının kararı, 2026-11-13; eski D1.5'in Arapça ve belâgat bilen, İşârât'ı
  okumuş tek kişisinin yerine). Arapçayı okuyup anlaması zayıf, belâgat bilmiyor; bilmediğini kaynaktan araştırarak
  ya da çevresindeki ehline dar sorular sorarak bulur. Gerekçe: örneklemin maddeleri dar iddialardır ("şu kelimede şu
  sanat var", "şu kelime şöyle i'râb edilir"); tek bir soruyu birine sormak, birine taslağı baştan sona okutmaktan
  kolaydır. Kullanıcı D9.3'te eleştirmenin söylediğini de süzdüğü için iki yön (söylediği ve söylemediği) aynı
  kişide birleşir. Sonradan bir bilirkişi bulunursa ona yalnız "emin değilim" kalanlar gider.
- D6.2 Ayar okuması (D9'un ilk çalışmasından sonra, bir kez): taslakların eleştirmenin itiraz etmediği belâgat ve
  i'râb iddialarından 20–30'luk örneklem ve kullanıcının D9.3'te "ehline sor" dediği notlar; her biri için "doğru /
  yanlış / emin değilim" ve not. Bir maddeye nasıl bakılacağına (kaynakta arama, birine sorma, açık bırakma)
  kullanıcı maddeye göre karar verir; maddeler önceden kümelere ayrılmaz. Bulunan hata türleri D9'a kalıcı denetim
  olarak girer (insan emeği bir kez, makineye kural olarak geçer). D8'le paralel, D5'ten önce biter (D5'te gizlenen
  İşârât metni, yani cevap anahtarı yok; eleştirmenin en güçlü dayanağı gider). **Dikkat edilecekler** (2026-11-13):
  - **Dayanak yapay zekâ olmaz.** D6'nın amacı taslağı yazanın da eleştirenin de (ikisi de Claude) doğru sandığı
    yanlışı bulmaktır; bir maddeyi claude.ai'ye ya da başka bir modele sorarak çözmek kör noktayı ölçülecek yere geri
    getirir. Her hükmün yanına dayanağı yazılır: **kaynak** (cümle kimliğiyle; ör. iddia edilen sanat ya da i'râb
    aynı âyette Beyzâvî, Ebüssuûd, Âlûsî'de geçiyor mu, terimin tanımı et-Ta'rîfât'ta ya da Miftâh'ta bu kullanıma
    uyuyor mu), **kişi** (adı yazılmaz, yalnız alanı: Arapça hocası, ilahiyatçı…) ya da **kendi kanaati**. Yapay
    zekâya dayanan hüküm "emin değilim" sayılır.
  - **Başarı ölçütü zayıflar.** Bilirkişi olmayan okuyucunun bir şey bulamaması bilirkişininkinden az şey söyler.
    Ölçüt: "kullanıcının kaynakla ve sorarak denetleyebildiği kadarıyla yeni hata türü çıkmadı"; o zaman düzen bu
    ölçüde güvenilir sayılır, "emin değilim" kalanlar heyete (ya da sonradan bulunacak bilirkişiye) kalır.
  - **Bazı maddeler çözülmeyebilir.** İnce belâgat isabeti (bir nüktenin yerinde olup olmadığı) ancak sorulan kişi
    ehilse çözülür; "emin değilim" kalması kusur değildir.
  **Örneklem hazır (2026-11-14; kullanıcının kararları: 24 madde, B ayrı sayılır, itiraz edilen 4 madde kalır).**
  `scripts/d1-elestiri.py bilirkisi 11-12` → `yz/bilirkisi-A.json` (sabit tohum; `--yeniden` verilmedikçe korunur).
  Havuz: tercüme paragraflarındaki `[dil]` ve `[belâgat]` işaretleri, işaret başına bir iddia (6 taslakta 388);
  "itiraz" = eleştirmenin o paragrafa yanlış, belâgat, i'râb, kaynak, uydurma, fazla türünde ya da "ehline sor" notu
  var (paragraf düzeyinde, kaba). Taslak başına 4: belâgat kendi tespiti 10 (havuz 122), belâgat kaynaklı 6 (114),
  dil 4 (41; ikisi kendi tespiti), itiraz edilen paragraftan 4 (111; eleştirmenin itirazına ters yoklama). Kaynaklı
  maddelerde kaynağın metni veritabanından gelir. `okuma-yz.html` › "Bilirkişi örneklemi": hüküm (doğru / yanlış /
  emin değilim), dayanak türü (kaynak / kişi / kendi kanaati / yapay zekâ; yapay zekâ seçilince hüküm "emin değilim"
  olur), dayanak ve not; kör okuma: tabaka ve itiraz gösterilmez, maddeden taslağa giden bağlantı YZ katmanını kapalı
  açar. İşaretler dışa aktarma dosyasına `bilirkisi` diye girer; `d1-elestiri.py rapor` → `provalar/11-12/d6-bilirkisi.md`
  (tabakayı gösterir: kullanıcı bitirmeden açmaz). B kısmı D9.3'ten sonra: `bilirkisi 11-12 --kisim B` (süzgeçte
  "ehline sor" denen notlar). Kullanıcının sırası: D7.7 (bitti, 2026-11-14), D6.2 A (eleştirmenin notlarını okumadan), D9.3, D6.2 B.
- D6.3 Gelen notlar: okuyuculara gönderilen `data/d1/okuma.html`'den notlar gelirse `scripts/d1-prova.py notlar` →
  `provalar/11-12/notlar.md` ile az emekle işlenir; beklenmez, yeniden davet edilmez. Kullanıcının ilk izlenimi
  (2026-11-13): taslak işliyor, yapay zekâ bazı yerlerde çok iyi tespit ve çıkarımlarda bulunmuş; özellikle üçüncü
  vecihte bazı kelimelerin ele alınışı İşârât'ın tarzına çok uygun. Tarz ile isabet ayrı not edilir.
- **D6.2 A bitti (2026-11-14), masada:** `d1-notlar-Fatih-202611141941.json`; 24 maddenin 20'si doğru, 3'ü emin
  değilim (A05, A11, A17), 1'i yanlış (A10). Kullanıcının dediği gibi hepsi kanaat; atıf maddelerinde kartın gösterdiği
  kaynak metnine bakıldı. Rapor `data/d1/provalar/11-12/d6-rapor.md` (elle; madde madde döküm `d6-bilirkisi.md`).
  - **Kör nokta: kapsam ve derece (mutlaklaştırma).** A10'da taslak 3 «لا تنافقوا» yerine ﴿لا تفسدوا﴾ denmesini
    "nifâkın tabiatıyla ifsad olduğuna işaret" sayıyor. İşârât ilişkiyi sebep zinciriyle kurar ("yalan → fitne →
    ifsad", `11-12-ayetlerin-tefsiri/c007–c008`; N23'ün kıyâsı); kullanıcı: nifâk tabiatıyla ifsad değil, ifsada açılır.
    D7 bunu "fazla, kendi tespiti", D9 "eksik: ara halkalar yok" diye kaydetti; ikisi de İşârât açıkken hükmün
    genişliğine itiraz etmedi. Yumuşak biçimi üç "doğru" notunda (A09 "kat'î değil", A12 "yalnız bu meselede", A18
    "tek maksat değil"). Eleştirmenin 6 taslaktaki notlarında iddianın kapsamını soran not yok.
  - Uzak işaret (A05, tek örnek): dört maksattan nübüvvete لا يشعرون'un mef'ûlünün hazfiyle telvih.
  - Kaynağa dayanan iddialar sağlam: atıf soruları 5/5, İşârât'ın kuralını buraya uygulama 5/5.
  - Ters yoklama (eleştirmenin notu olan paragraf, 4 madde) bilgi vermedi: notların hiçbiri o iddianın kendisine
    değildi.
  - Düzenin kendi kusurları: A19'un sorusu iddiayı aştı ("kalıcı" sözünü soru ekledi); A12 ile A20 aynı iddia; A16'nın
    kartında paragrafın Âlûsî atfı yoktu; dayanak alanı 7 maddede boş, A05'te notla çelişiyor.
  - **Geçenler:** D9'a kalıcı "kapsam" denetimi (inhisar ve mutlaklık kalıplarında İşârât'ın aynı ilişkiyi sebep
    zinciriyle kurup kurmadığı; zinciri atlayıp mahiyet hükmü çelişki adayı; iddia tek vecih mi vecihlerden biri mi);
    aday denetim: dört maksat bağlarında lafız dayanağı. D7'nin çelişki tanımına "kısmi çelişki". D8'in istemine
    ihtimal dili ve zinciri atlamama. Masaya: kartta paragrafın bütün kaynakları, atıf maddesinde dayanak varsayılanı.
- **Kapanış (2026-11-14, kullanıcının isteği: "D6'yı bitir"):** D6.2 B ayrı okuma olarak yapılmaz: D9.3'te "ehline sor"
  denen notlar A'nın emin değilimleriyle heyete kalan listeye girer (süzgeçte de aynı kişi bakıyor). D6.3 iş olarak
  kapanır; not gelirse `d1-prova.py notlar` işler. **D6 kapandı (2026-11-14).**

**D7. Yapay zekâ karşılaştırıcısı** (kullanıcının fikri, 2026-11-13: taslağı yazan bir yapay zekâ olduğu gibi onu
metinle karşılaştıran da bir yapay zekâ olsun). Rapor "taslak İşârât'ın şu nüktelerini aynen ya da kısmen yakaladı,
şunları atladı, şunları fazladan söyledi" der; okuyucunun işi bulmaktan doğrulamaya döner, D2 ve D3'ün farkı sayıyla
verilir. **İlkeler (kullanıcı onayladı, 2026-11-13):**
- Eşleştirir, hüküm vermez: fazladan söylenenin doğru olup olmadığına karar vermez, "ehline sor"a koyar; Arapça ve
  belâgat isabeti bilirkişinindir.
- Her satır iki ucuyla: İşârât'ın gizlenen cümle kimlikleri ve taslağın bloğu (okuma sayfasının çapası, `V3/ar/5`);
  iki taraftan alıntılanan söz kendi metninde mekanik olarak aranır.
- İki kör okuyucu: iki farklı model (Fable 5.2 ve Opus 5.5) birbirini görmeden; uyuştukları satırlar sağlam,
  ayrıldıkları satırlar işaretli (hadiste `read_chapter` gibi). Taslakları Fable yazdı: tek başına onun okuması kendi
  üslûbuna yumuşak bakabilir.
- Okuyuculara gösterilmez (ona göre okumasınlar): okuyuculara giden okuma sayfası değişmez, karşılaştırma katmanı
  kullanıcının ayrı sayfasındadır.
- **Güven (kullanıcının düzeltmesi, 2026-11-13):** ölçü insan notlarıyla uyuşmak değil, metne bakınca tutmaktır
  (okuyucunun görmediğini yapay zekâ görmüş olabilir; küçük eksikleri bilindikçe kabul). Örneklem metne bakılarak
  sınanır; insan notlarıyla fark iki yönlü sayılır: yapay zekânın görüp okuyucunun görmediği, metinde tutuyorsa
  kazançtır; okuyucunun görüp yapay zekânın görmediği eksiğidir.
- Sınırı: D5'te (Bakara 34 ve sonrası) gizlenen İşârât metni yok; orada aynı araç taslağı müfessirlerle karşılaştırır
  (daha zayıf bir kontrol). Bu D5'e gelince ayrıca konuşulur.
**D7.1–D7.6 bitti (2026-11-13).** `scripts/d1-yz.py` (`envanter`, `eslestir`, `rapor`), istem
`docs/d1/karsilastirma-istemi.md` (v1), sayfa `data/d1/okuma-yz.html` (`d1-prova.py okuma` sonuç varsa yazar; okuyuculara
giden `okuma.html`'de katman yok), rapor `data/d1/provalar/11-12/yz-karsilastirma.md`. Sonuçlar: envanter 41 kalem (V1 6,
V2 12, V3 23; Opus eksik bulmadı, bir silme önerdi: N30, kullanıcıya açık). Kapsama (aynen + kısmen) iki okuyucuya
göre taslak 1 %71/%73, taslak 2 %76/%76, taslak 3 %80/%73; iki okuyucu kalemlerin 41/40/36'sında aynı ya da yakın
(✓/◐), ayrılık 1/0/5. Hiçbir taslağın yakalamadığı: N05 (hamliyeden şartiyeye üslûp değişikliğinin mukadder kelâma
remzi), N08, N25, N27 (fi'l-arz'ın nehyi şefkat-i cinsiye ve nefret-i umumiye ile idâmesi), N20 (yalnız tercümedeki
vasıf), N30. Üçünün de yakaladığı 26 kalem. Fazla (envanterde karşılığı olmayan iddia) taslak başına 39–52; çelişki
yalnız 1 (zayıf: taslak Ebüssuûd'un görüşünü nakledip iki vechi birlikte tutuyor). Bütün alıntılar metinde bulundu
(denetimsiz 0). Maliyet ≈14,7 $ liste fiyatı (envanter 1,68, eşleştirme 13,05; Max planı), süre ≈20 dk. D7.7
kullanıcıda: `okuma-yz.html` › "YZ örneklemi" (30 satır), notlar dışa aktarılır, `notlar` ve `rapor` güveni yazar;
D6'nın notları gelince iki yönlü fark.

Ayrıntılı plan (2026-11-13; kullanıcı üç öneriyi onayladı: envanteri Fable çıkarır, Opus denetler; envanter
eşleştirmeden önce onay beklemez; Fable 5.2 ve Opus 5.5 yüksek düşünmeyle, örneklem ≈30). Yeri `scripts/d1-yz.py`
(plandaki `d1-prova.py` alt komutları yerine ayrı betik: o dosya 850 satırdı),
çıktılar `data/d1/provalar/<birim>/` (kapalı depo). Çağrılar taslak yazımıyla aynı düzende: `claude -p`, proje dışında,
araçsız (girdi istemdedir), yüksek düşünme.
- D7.1 İstem ve şema: `docs/d1/karsilastirma-istemi.md` (sürümlü; sürüm özeti her çıktıda), iki görev (envanter,
  eşleştirme), JSON çıktı şeması. Girdiler: gizlenen metin (Arapça asıl cümle kimlikleriyle, Türkçe tercüme
  yanında), taslak (okuma sayfasının blok çapalarıyla, Arapça ve tercümesi), envanter.
- D7.2 Envanter (cevap anahtarı): gizlenen metin nükte nükte, taslaklardan bağımsız: kimlik (`N01`…), vecih, ilgili
  lafız ya da hey'et (Arapça), nükte (kısa Türkçe), İşârât'ın Arapça ve Türkçe cümle kimlikleri, Arapça alıntı. Fable
  çıkarır, Opus metne bakarak denetler (eksik, birleştirilmesi ya da bölünmesi gereken, yanlış); ayrılıklar
  kullanıcıya. Sabitlenir (`envanter.json`, sürümlü); D8 ve D2'de aynı envanter kullanılır.
- D7.3 Eşleştirme: 3 taslak × 2 model (Fable 5.2, Opus 5.5), birbirini görmeden. Envanterin her nüktesi için durum
  (`aynen`, `kismen`, `farkli_gerekce`: aynı lafızda başka nükte, `yok`), taslağın çapaları ve taslaktan birebir
  alıntı, bir cümle gerekçe. Envantere bağlanmayan her taslak iddiası `fazla`: çapası, alıntısı, taslağın kendi
  işareti (kaynaklı ya da kendi tespiti), İşârât'la çelişiyorsa hangi nükteyle; `fazla`nın hepsi "ehline sor".
- D7.4 Denetim ve birleştirme: alıntılar kendi metninde aranır (hareke ve noktalama yok sayılarak), kimlik ve çapa
  denetlenir; geçmeyen satır silinmez, `denetimsiz` işaretlenir. İki modelin uyuştuğu ve ayrıldığı satırlar; sayılar:
  kapsama (`aynen` + `kismen` / envanter), `farkli_gerekce`, `yok`, `fazla` (kaynaklı, kendi tespiti), çelişki.
- D7.5 Rapor: `yz-karsilastirma.md`: taslak başına sayılar ve iki modelin ayrılık oranı; nükte × taslak çizelgesi
  (hiçbir taslağın yakalamadığı, hepsinin yakaladığı nükteler); taslak başına fazlalar ve çelişkiler; ayrılıklar.
- D7.6 Kullanıcının sayfası: `okuma --yz` → `data/d1/okuma-yz.html` (okuyuculara giden `okuma.html` değişmez):
  İşârât paragrafının yanında nükteleri ve taslaklardaki karşılıkları, taslak bloğunun yanında bağlı nükte ya da
  "fazla"; satır başına "metinde tutuyor / kısmen / tutmuyor" işareti ve dışa aktarma.
- D7.7 Sınama: örneklem (≈30 satır, durumlara ve uyuşma/ayrılığa göre katmanlı) kullanıcı metne bakarak işaretler,
  güven oranı rapora; D6'nın notları gelince iki yönlü fark (yapay zekânın kazancı, eksiği) rapora. **Durum (2026-11-13):** ilk dışa aktarımda
  (`d1-notlar-Fatih-202611131237.json`) 8 işaret, hepsi taslak 1'in N01–N04 satırları, örneklemden yalnız biri.
  **Bitti (2026-11-14), âyet masasında:** `d1-notlar-Fatih-202611141813.json`, 38 işaret; örneklemin 30 satırının
  30'u işaretli: 27 tutuyor, 3 kısmen, 0 tutmuyor, **güven %95** (tutuyor + kısmen/2). Katmanlar: ayrılık 5 satırda %80
  (3 tutuyor, 2 kısmen), aynen 5'te %90 (taslak 1 N19'da iki okuyucunun "aynen"i kısmen tutuyor), çelişki 2, fazla 5,
  kısmen 5, farklı gerekçe 4, yok 4'ün hepsi tutuyor. Örneklem dışı 11 işaret (ikisi 13'ündeki dosyadan) %95, güvene
  girmez. Rapor `provalar/11-12/yz-karsilastirma.md` › "Sınama (D7.7)": örneklem ve örneklem dışı ayrı, ayrılıklarda
  her okuyucunun hükmü ve kullanıcının işareti, tam tutmayanlar (`d1-yz.py rapor`; önceden örneklem dışı işaretler
  güvene karışıyordu). İki yönlü fark (okuyucu notlarıyla) D6'nın daralmasıyla D6.3'e kaldı: 13'ündeki dosyanın 18
  notu ve ölçüt çizelgesi `notlar.md`'ye işlendi.
- **Dersler (D8'e ve karşılaştırıcının sonraki sürümüne):**
  - Karşılaştırıcı güvenilir: "yok", "farklı gerekçe", "fazla" ve çelişki hükümleri örneklemde hiç şaşmadı. Fazlanın
    "İşârât'ta karşılığı yok" tespiti tutuyor; fazlanın kendisinin doğru olup olmadığı yine ehlinindir (D6, D9).
  - "Aynen" bazen cömert: N19'da iki okuyucu birlikte "aynen" dedi, metin kısmen tutuyor; D9 da taslak 1'de N13 ve
    N34'ün "aynen"inin fazla olduğunu göstermişti. İstemin sonraki sürümünde "aynen" ölçütü sıkılaşır (nüktenin
    gerekçesi de taslakta olmalı, yalnız lafız ve sonuç değil).
  - Ayrılıklarda tek okuyucu sistemli olarak haklı değil: işaretli dört ayrılığın ikisinde Opus ("yok" dedi, Fable'ın
    "kısmen"i fazla buldu), birinde Fable, birinde ikisi de tutuyor; N22'de yalnız Opus işaretli, tutuyor. İki kör
    okuyucu kalır; ayrılık işareti "buraya bak" olarak doğru çalışıyor.
  - "Kısmen" ile "farklı gerekçe"nin sınırı bulanık (N38'de ikisi de tutuyor): ikisi sayılarda ayrı kalır ama kapsama
    oranı yalnız aynen + kısmen olduğu için bu sınır kapsamayı oynatır; D8'in ölçümünde iki okuyucunun ortalaması ve
    farklı gerekçe ayrıca verilir.
**D7 kapandı (2026-11-14).**

**D2. Bakara 11–12, E2'nin eserleriyle** (eski D1.7). Aynı birim, aynı model ve düşünme, aynı istem sürümü; değişen
yalnız eklenen eserler (E2 ve klasik eserler bağdaştırıcısı prova sunucularına girer). Üç taslak (kullanıcı onayladı,
2026-11-12; aynı şartlarda üç taslak birbirinden epey farklıydı: İşârât'tan 29, 21, 36 yer). Fark: yeni eserlere
dayanan iddia, belâgat isabeti, uydurma, okuyucuların notları; D1 ile aynı ölçüt çizelgesi; D7'nin envanteriyle
kapsama. **Sıra ve taban (kullanıcının kararı, 2026-11-13; önceki "D8'den sonra" kararının yerine):** D2'nin şartı
D1 ile aynı olmaktır; bu yüzden D8'den önce, D1'in istemiyle (`prova-istemi.md` v1-ince) yazılır ve D1'in
taslaklarıyla karşılaştırılır. İstemde değişen yalnız me'haz listesine eklenen klasik eserler satırıdır (eklenti
olmadan eserler görünmez; usule dokunmaz); sürümü `v1-ince-klasik` diye yazılır. Prova sunucularına `klasik` profili
eklenir (İşârât'ı taşımadığı için gizleme gerekmez; sızıntı testi yine çalışır). D8 sonra istemi değiştirir ve
D2'nin taslaklarıyla karşılaştırılır.
**Bitti (2026-11-13).** Taslak 4–6 (`istem-ince-klasik.md`: D1'in `istem-ince.md`'si ve me'hazda klasik eserler satırı;
Fable 5.2, yüksek; 698–730 sn, 7,56–8,10 $), taban D1'in ince taslakları 2 ve 3 (kullanıcının önerisi: taslak 1 tam
istemle, yalnız bilgi). Ölçüm D7'nin karşılaştırıcısıyla ve yeni `KAYNAK` göreviyle (`d1-yz.py kaynak`, `d2-veri`).
Rapor `data/d1/provalar/11-12/d2-rapor.md`. **Sonuç: eserler kapsamayı artırmadı, dayanağı güçlendirdi.** Kapsama D1
ortalaması 30, D2 28,7 kalem (taslaklar arası oynamanın içinde); aynen yakalanan 11'den 12,3'e. Hiçbir taslağın
bulamadığı nükteler aynı (N05, N08, N24, N25, N27, N28, N22): İşârât'a has, kaynakta hazır durmuyor. Üç taslak da
Delâil'in bu âyeti işleyen iki yerini buldu: fıkra 425 (إنما'nın malûmiyeti, ألا ve إنّ ile red: İşârât'ın N32, N38,
N39 nüktelerinin aslı; D1 bunları müfessirlerden ya da kendi tespiti olarak veriyordu) ve fıkra 264 ("ألا إنهم هم
المفسدون"un isti'nâfı: İşârât'ta yok, doğru bir fazla). Klasik esere dayanan 26 iddianın hiçbirinde kaynak iddiayı
yalanlamıyor (Fable 22, Opus 20 tam destekli, kalanı kısmen); 19'u İşârât'ın bir nüktesine karşılık geliyor. Risk:
kayıtlı sözün genellenmesi ("قد", "من معاني" → "hâssa-i âmme") ve kaidenin kaynakta olmayan sonuca taşınması; ehline
altı not. Klasik kaynaklar tefsir kaynaklarının yerini almadı, yanlarına geldi (5–8 kaynak). Ezber şüphesi artmadı.
Dersler D8'e (aşağıda).

**E2. Belâgat eserleri ve Risale'nin andığı önemli kaynaklar (bitti, 2026-11-13; 1. dilim)** (kullanıcının kararı, 2026-11-12: klasik eserler iki
parçaya ayrıldı; kalanı E5). Ölçüt (kullanıcı onayladı, 2026-11-09): bir eser şu üç şarttan en
az ikisini tutarsa girer:
1. Risale onu ya da müellifini adıyla anıyor, ya da Risale'deki bir hadisin künyesi o kitabı gösteriyor (veriden
   sayılır: `search` ile adlar, `data/interim/hadis/kunye.md` künyeler).
2. Muhakkiki bilinen bir dijital nüshası ve açık izni ya da lisansı var (önce OpenITI).
3. Gerçekçi bir sohbette ona soru gelir (medrese ders kitaplarının çoğu bunu tutmaz).

Gerekçe: her eser anlamsal aramayı sulandırır ve bellek ister (tefsir makinesi 8 GB, 1,3 GB kullanılıyor).
"Bediüzzaman'ın ezberlediği 90 kitap" bir liste değil, bir rivayettir; çoğu ders kitabıdır. Beklenen sonuç 15–30
eserlik bir küme, 90 değil. Abduh ve Menâr kaynak alınmaz (`catalog/excluded.py`).
- E2.1 Aday listesi: önce belâgat (İşârât'ın adıyla dayandığı Delâilü'l-İ'câz, Esrârü'l-Belâga, Miftâhu'l-Ulûm;
  Keşşâf tefsirde var), sonra Risale'nin adıyla andığı önemli kaynaklar; her aday üç şartla ve OpenITI nüshasıyla
  (`docs/eserler/klasik.md` (b) ve (c)).
  **Bitti (2026-11-13):** `docs/e2-adaylar.md`. Anma sayıları genel veritabanından (Türkçe ve Arapça yazılışlarla),
  nüshalar OpenITI'den (GitHub, salt okuma; muhakkik ve yayınevi sürümün `#META#` satırlarından). Öneri: **1. dilim
  (belâgat ve terim, D2'nin ön şartı):** Delâilü'l-İ'câz (Şâkir), Esrârü'l-Belâğa, Miftâhu'l-Ulûm, et-Ta'rîfât,
  el-Müfredât (≈2,5 milyon kelime); **2.** Şerhu'l-Makāsıd, et-Telvîh, el-Munkız, el-Fıkhu'l-Ekber, İhyâ; **3.**
  Şerhu'ş-Şifâ (öneri: hadis sunucusunda eş-Şifâ'nın yanında), el-Mevâhib; seçmeli Sîbeveyh, Îzâh ya da Muhtasar,
  Kâmûs; bekleyen (nüsha ya da boyut) Şerhu'l-Mevâkıf (yalnız OCR), Fütûhât, Bidâye, Fütûhu'l-Gayb ve Mektûbât
  (OpenITI'de yok), Nesîmü'r-Riyâz, Mîzân-ı Şa'rânî. Dört soru kullanıcıya (belgenin sonu).
- E2.2 **Seçim (kullanıcı, 2026-11-13):** önerilen eserlerin hepsi kıymetli, hepsi listelere girer. 1. dilim
  (Delâilü'l-İ'câz, Esrârü'l-Belâğa, Miftâhu'l-Ulûm, et-Ta'rîfât, el-Müfredât) şimdi: E2.3 bunlarla. 2. ve 3. dilim
  sonra, bu sırayla (E5): `docs/eserler/klasik.md` (b). Şerhu'ş-Şifâ hadis sunucusuna (`docs/eserler/hadis.md` (b)).
  Seçmelilerden şimdi giren yok; seçmeliler ve bekleyenler (Fütûhu'l-Gayb, Mesnevî, Mektûbât "çok çok kıymetli")
  klasik.md (c)'de, yer ve zaman müsait olunca E5'te. Kullanıcının D7 üzerine sözü: karşılaştırıcının bulguları
  muhteşem, yakalanmayan nükteler beklenenden çok az; taslağın fazladan yakaladığı her şey projenin amacı olan ayrı bir
  zenginliktir.
- E2.3 Ayrıştırma: OpenITI ortak ayrıştırıcılarıyla (`books/tefsir_openiti.py`, `hadis_openiti.py` örnek).
  **Bitti (2026-11-13, 1. dilim):** `catalog/klasik.py`, `sources/klasik.py` (`fetch klasik`), `books/klasik_openiti.py`.
  Ham verinin incelemesinden çıkanlar: (1) Shamela sürümlerinde başlık işareti yer yer metnin içine düşmüş (Esrâr'da
  "الفصل" kelimesinin "فصل"i, Miftâh'ta mukaddimedeki kısım sayımı): başlıktan sonraki satır `</span>` ya da
  noktalamayla sürüyorsa başlık metne geri katılır, kelime düşmez; (2) kaynağın satırı baskının paragrafıdır, yalnız
  sayfa sınırında bölünmüştür (tefsirlerdeki "cümle sonunda biter" kuralı Esrâr'ı 1.520 satırdan 74 paragrafa
  indiriyordu); (3) beyitlerin mısralarını ayıran "..." cümle sonu sayılıyordu: tek beyit `verse` paragrafı, tek cümle
  (`sentences.split_paragraph`); (4) Müfredât'ın Dâvûdî baskısında (Shamela) madde başlığı işareti kelimelerin içine
  girmiş ("[الح|شر|/ 14]"), metin kurulamıyor: Kîlânî'nin JK sürümü alındı, madde (kök) düğümü paragrafın "kök :"
  başlangıcından, harf kitabı kökün ilk harfinden (bu baskıda و ه'den önce); (5) Ta'rîfât'ta Ebyârî'nin JK sürümünde
  OCR artıkları var: DKİ'nin Shamela sürümü alındı; (6) Esrâr'ın bu sürümü son paragrafın ortasında biter (`gaps`).
  Sonuç: 5 eser, 2.586 bölüm (Delâil 58 bölüm ve Şâkir'in 700 fıkrası, Müfredât 28 harf kitabı ve 1.600 madde,
  Ta'rîfât 28 bab), 15.148 cümle, ≈570 bin kelime. Testler `tests/test_klasik.py`. E2.1'in kelime sayıları yanlıştı
  (harf sayısıydı), `docs/e2-adaylar.md` ve `klasik.md`'de düzeltildi.
- E2.4 Nerede durur: **karar (kullanıcı, 2026-11-12): yeni bir "klasik eserler" bağdaştırıcısı**, tefsirlerle
  karışmasın diye; tefsir makinesinde (8 GB, bunun için alındı), tefsir sunucusunun yanında. Kurulum: profil, sunucu
  ve talimat, Caddy yönlendirmesi, sitede eklenti sayfası.
  **Yayında (2026-11-13; kullanıcının onayıyla):** profil `klasik` (`data/dist/klasik/risale.db` 40 MB,
  vektörler 15.148, Voyage ≈1,2 milyon token), sunucu `KLASIK_INSTRUCTIONS` (araçlar tefsirinkiyle aynı: list_works,
  get_outline, read_section, get_passage, search, semantic_search, find_sentence, find_ayah, get_ayah, cite;
  muhakkikin girişi `layer`), servis `docs/risale-mcp-klasik.server.service` (8003), Caddy `/klasik`,
  `scripts/tefsir-sunucu.sh` `PROFIL=klasik` ile, çağrı seti `tool_calls_klasik.json`, site `klasik.html`,
  `en/classical.html`, ana sayfada dördüncü kart, gizlilik politikası dört eklenti. Uçtan uca deneme (claude -p,
  yalnız bu sunucu): Delâil'in i'câz-nazım delili 7 kaynakla, fıkralar doğru, tercüme damgalı. Risale ve Tefsir
  sunucularının araç çıktısı son yayına göre değişmedi. Yayın: `PROFIL=klasik scripts/tefsir-sunucu.sh gonder`
  (kayıt `klasik-yayin-20261113-135607`), `scripts/deploy.sh --code` (Caddy, site; `yayin-20261113-135715`, fark yok).
  Canlı adreste başlatma, `find_sentence` ve `semantic_search` denendi. Yenilikler yazısı
  `docs/yenilikler/2026-11-13-klasik-eserler.md` (iki örnek soru eklentide denendi).

Biten kimlikli işin ayrıntısı "Sıradaki"den buraya taşınır ("Biten"de tek satırı kalır).

**S1. Yenilikler sayfası.** Sitede tarihli kısa yazılar (ilki: hadis ve tefsir bağdaştırıcıları), her yazının
sonunda WhatsApp'a kopyalanacak metin; paylaşılınca önizleme çıksın diye bütün sayfalara Open Graph etiketleri.
Dışarıya istek yok kuralı sürer.
Durum (2026-11-09): kullanıcının kararları betik, yalnız Türkçe, sade kart. `scripts/site-uret.py`, yazılar `docs/yenilikler/` (iki taslak: hadis ve tefsir bağdaştırıcıları, ilk düzeltmeler), 18 sayfada Open Graph, menüde Yenilikler, RSS. Yayın: `scripts/deploy.sh --code`; sonra telefonda bir bağlantı paylaşılarak önizleme denenir.

**S2. Sitenin yenilenmesi.** Karar (2026-11-09): bütün Türkçe sitede "eklenti" (yapıldı); Claude'un menü adları kurulum adımlarında kalır. Site üç bağdaştırıcılı ağı anlatır: Risale eksende; Kur'ân, hadis kitapları ve
tefsirler etrafında; her söz cümle düzeyinde adresli. Ana sayfada üç sunucuyu birlikte kullanan gerçek bir cevap
(kısaltılmadan, işaretleri veritabanıyla denetlenmiş), sayılar, "kimin için" (araştırmacı, akademisyen, ders
hazırlayan).
Kararlar (kullanıcı, 2026-11-09): plan ve öneriler onaylandı; Katkı sayfası "Hata bildirin" oldu (D1'in mütehassısı ilanla değil davetle), girişte süs âyet yok, İngilizce sonra.
- S2.1 Ana sayfa (bitti): giriş, sayılar, üç eklenti kartı, üç eklentili örnek cevap (kullanıcının claude.ai sohbeti, 9 Kasım 22.15; 13 kaynağın alıntıları veritabanıyla birebir; soru metni sohbette yoktu, önerilen soru yazıldı), karşılaştırma, kimin için, güvence, ekleme ve adresler, son yenilikler, kaynaklar.
- S2.2 `risale.html` (bitti), `katki.html` "Hata bildirin" (bitti).
- S2.3 Betik `scripts/site-uret.py` (eski adı site-yenilikler.py): menü ve alt bilgi ortak, sayılar veritabanından, son üç yazı, `sitemap.xml`; `robots.txt` (bitti).
- S2.4 İngilizce sayfalar (bitti): ana sayfa, `en/risale.html`, `en/contribute.html` "Report a mistake"; menü ve alt bilgi betikten.
- S2.5 Yayın (2026-11-09).

**D1 Taslakların yazılması (D1.1–D1.4, D1.7, D1.8; kapandı 2026-11-13).** Kalanı ayrı aşamalar oldu (kullanıcının
kararı, 2026-11-13): D1.5 ve D1.6 → D6 (bilirkişi okuması), D1.9 → D8 (taslak altyapısının güncellenmesi); yeni D7
(yapay zekâ karşılaştırıcısı).

- **Fikirden geldiği yer** ("Fikirler"den taşındı, 2026-11-14: fikir D1 olarak sıraya alınmıştı):
  **İşârâtü'l-İ'câz usulüyle yapay zekâ taslağı (yeniden değerlendirme, 2026-11-09; D1 olarak sıraya alındı):** kullanıcının yola çıkarkenki
    asıl fikri: model İşârât'ın usulüyle taslak yazar, mütehassıslar doğrular, ekler, çıkarır. Bilgili kişilerin
    geri dönütü: model İşârât'ın şeklini ve usulünü iyi takip edip tatbik edebilir, bu kullanılmalı. 2026-11-04
    değerlendirmesi (`docs/tefsir-pilot-degerlendirme.md` "4") taslağa karşıydı (akıcılık eksiği gizler, heyeti
    düzeltmeye bağlar, sorumluluk). Yeni öneri: kör denemeyle sınamak. İşârât'ın kapsadığı aralıkta (Fâtiha, Bakara
    1–33) model İşârât'ın usulünü (kendi Mukaddemat'ı ve önceki âyetler) görür, sınanan âyetin İşârât metnini görmez;
    taslak İşârât'ın kendi metniyle ve mütehassısların gözüyle karşılaştırılır. Tutarsa asıl hedef: İşârât'ın
    bittiği yerden (Bakara 34) sonrası. Şartlar: "yapay zekâ taslağı" damgası, "tefsir" denmez; her iddia kaynağa
    bağlı (âyet, tefsir sunucusundaki müfessirler, Risale); dil ve belâgat iddiaları ayrı işaretli; taslak kapalı
    kalır, yayımlanmaz. Bağ altyapısı gerekmez (dosya ve mütehassıs notu yeter). Karar kullanıcıda.

- D1.1 **Usul özeti** (taslak hazır, 2026-11-10: `docs/d1/usul-ozeti.md`). İşârât'ın bir âyeti ele alırken ne
  yaptığının ve hangi sırayla yaptığının dökümü; tefsir değildir. Her madde İşârât'ın kendi cümlesine dayanır,
  adresi ve kimliğiyle; derleyenin çıkarımı "[Çıkarım]" diye işaretlidir. İçeriği: eserin kendini tanımlaması
  (maksat nazımdaki i'câz, sınır lafzın delâleti ve işârâtı, niyet bir heyetin tefsirine örnek ve me'haz), ilkeler
  (dört maksat, havuz ilkesi, saat milleri, birden çok mânânın şartı), bir âyette izlenen sıra (âyet, gerekirse
  mukaddime, mâkabliyle irtibat, cümleler arası intizam, hey'etler ve kelimeler), üçüncü vecihte bakılanlar,
  anlatım biçimi, kaynaklarla ilişkisi, mütehassısa sorular. Üç işi var: usulü önce kullanıcı ve mütehassıs onaylar;
  mütehassısın taslağı ölçeceği ölçü olur; modele neye bakacağını söyler. Alıntılar `python3
  scripts/d1-usul-denetim.py` ile veritabanıyla denetlenir (48 alıntı, hepsi birebir). Türkçe tercümeden
  derlendi; Arapça asılla karşılaştırma ve "usul hangi dilden öğretilir" sorusu mütehassısa ve kullanıcıya açık.
  Okur sürümü (2026-11-10, kullanıcının isteği: paylaşılacak, programcı ayrıntısı olmadan): `python3
  scripts/d1-okur.py` → `site/taslak/isarat-usulu.html` ve `.pdf` (kimlik yerine eser, bölüm ve ilk kelimeler;
  "Derleyenin notu"; yalnız bağlantıyla: menüde ve site haritasında yok, `noindex`; açık olması sorun değil).
  Adres: https://risalemcp.com/taslak/isarat-usulu.html
- D1.2 Kullanıcı okudu ve bildiği uygun kişilere gönderdi (2026-11-10). **Kararlar (kullanıcı, 2026-11-10):**
  - Özetin mütehassısa sorduğu ilk üç soruyu (üç vecih her birimde var mı, mukaddimeler, terimlerin Arapça asıldaki
    dağılımı) model metnin tamamını okuyarak cevaplar: **birim çizelgesi** (D1.2a). Sınırlar: "taslakta ne zaman
    mukaddime yazılır" kuralını model bulgudan önerir, kullanıcı karara bağlar; Arapça belâgat inceliklerinde model
    yanılabilir, her hücre adresli kalır.
  - **Dört maksat kuralı:** asıl maksat her zaman söylenir; öbürleri yalnız âyetin bir kelimesine ya da hey'etine
    dayandırılabiliyorsa, derecesiyle (sarih, işaret, remiz) söylenir; dördü her âyette zorla gösterilmez.
    Dayanak: Fâtiha girişi ("sarâhaten veya işâreten veya remzen") ve Bakara girişinin Arapça aslı (çoğu sûrede biri
    asıl, kalanı tebeî).
  - **Dil:** tefsir Arapça yazılmalıdır (kullanıcının görüşü; müellifin sözü değil, onun üç tespitinden çıkardığı
    sonuç: tercüme cezâleti koruyamamış, Arapça tefsir ayrıca neşredilecek, Arapçasındaki tevâfuklar korunmalı).
    Usul Arapça asıldan öğretilir, Türkçe tercüme destek olur. Taslak **Arapça asıl ve onun Türkçe tercümesidir**
    (iki ayrı taslak değil): tercüme Arapçadan paragraf paragraf, damgalı; kullanıcı Türkçesini okur, Arapça bilen
    aynı paragrafın aslını denetler; provada Arapça taslak İşârât'ın gizlenen Arapça kısmıyla yan yana okunur.
  - **Mütehassıs** bu iş için: Arapça ve belâgat bilen, İşârât'ı okumuş biri (Arapça taslağı kullanıcı denetleyemez).
- D1.2a **Tam okuma ve birim çizelgesi** (bitti, 2026-11-10): Arapça asıl baştan sona okundu (3.264 cümle;
  15 Fâtiha kelime bahsi, 23 Bakara âyet bahsi). Çizelge `docs/d1/birim-cizelgesi.md` (239 adres, `python3
  scripts/d1-usul-denetim.py docs/d1/birim-cizelgesi.md` ile denetlenir), okuma notları `docs/d1/okuma-notlari.md`.
  Bulgular: (1) eser üç vechi dokuz yerde adıyla sayar; Bakara 9'dan sonra sıra sabit (V1 → V2 → V3, 15/15 birim),
  1–8'de düzen henüz oturmamış, Fâtiha'da birim kelime. (2) Mukaddime sabit basamak değil; dört durumda gelir:
  âyetin meâli dört maksattan ya da iman rükünlerinden biri, âyetin altında büyük kelâm ihtilafı, bir üslûp türünün
  ilk kez toplu gelmesi, tahkik isteyen lafız; çoğu "başka kitapta tafsil ettik, burada hülâsa" diye gelir, her
  delil âyetin bir lafzına bağlanır. (3) Üçüncü vecihte yapılan işler: bakılacak yerlerin sayılması, tercih sorusu
  ("neden şu lafız, şu değil"), beklenenle muvazene, mukadder cümleler, sâmiin zihni, karşılıklı eşleme, genel ve
  hususî nükte, toplayış. (4) Okumayla çıkanlar: nazarî temel Bakara 17–20'deki on iki mesele; dayanak Cürcânî
  ("ونحن على مذهبه"); adıyla anılan kaynaklar (Cürcânî, Sekkâkî ve Miftâh, Zemahşerî ve Keşşâf, Râzî, Câhız,
  Teftâzânî, Sîbeveyh…; bir yerde Abduh'tan nakil); bir nüktenin kabul ölçüleri (üçüncü şart Arapçada
  "makàsıd-ı şeriat usulü"); Arapça asıl 31. âyetin ortasında biter. **Mukaddime kuralı (kullanıcı onayladı,
  2026-11-10):** taslakta mukaddime yalnız dört durumdan biri varsa yazılır, kısa tutulur, her iddiası âyetin bir
  lafzına bağlanır, mesele İşârât'ta ya da Risale-i Nur'da işlenmişse oraya atıfla hülâsa edilir.
  E2 için not: Miftâh, Delâilü'l-İ'câz, Esrârü'l-Belâga ve Keşşâf eserin adıyla dayandığı kaynaklar.
- D1.2b **Özetin ikinci sürümü** (bitti, 2026-11-10): `docs/d1/usul-ozeti.md` Arapça asla dayanır. 55 Arapça
  alıntı; 40'ının yanında Abdülmecid Nursî tercümesindeki karşılığı, 15'inde "Yapay zekâ tercümesi" damgalı model
  tercümesi (11'i Bakara 17–20'nin tercümede bulunmayan nazarî girişinden). Yeni bölümler: usulün nazarî temeli (2:
  i'câzın esası nazmın belâgati, nazm-ı meânî, mânâ tabakaları ve delâlet dereceleri, her kayıt mukadder suale
  cevap, hayalde hakikat çekirdeği, Cürcânî'nin mezhebi), âyet âyet sıra çizelgesi (4), mukaddimelerin dört durumu
  ve gerekçe cümleleri (5), taslak için kurallar (8: ad ve damga, dil, me'haz, sıra, dört maksat, mukaddime, kabul
  ölçüsü), açık sorular (9). 112 alıntı ve 148 kimlik veritabanıyla denetlendi, 0 sorun. Okur sayfası ve PDF aynı
  adreste yenilendi (`scripts/d1-okur.py`: Arapça sağdan sola, altında tercümedeki karşılığı; 23 sayfa); yayına
  gitmesi için `scripts/deploy.sh --code` gerekir. Model tercümeleri ve Arapça–Türkçe eşlemeleri ehli görmedi.
- D1.2c Özetin açık sorularına kullanıcının görüşleri (2026-11-10/11; özette ve okur sayfasında soru olarak kalır,
  mütehassısın görüşü de alınacak): **düzen** Bakara 9'dan sonraki sabit sıra (V1 → V2 → V3), öbür türlü usul sabit
  olmaz; **Türkçe tercümenin dili** Abdülmecid Nursî tercümesine yakın (Arapça asla muvafık tarz); **üslûp** provada
  îcâzlı. Prova bunlarla yapılır. Açık: Arapça okumanın ehlince denetimi (1).
- D1.3 Prova düzeni: sınanan âyetin İşârât metnini (Türkçe ve Arapça) dışarıda bırakan deneme profili, taslak
  şablonu ve damgası, farklı türden 4–5 âyet (hurûf-u mukattaa, hüküm, temsil, öncesiyle bağı ince olan…).
  **Kararlar (kullanıcı, 2026-11-11):** âyet âyet gidilir: bir birim yazdırılır, kullanıcı (gerekirse başkaları)
  inceler, hata varsa aynı birim yeniden, uygunsa sonrakine; her birim iki kez yazdırılır. Öneriler (onay bekliyor):
  model Fable 5.2, yüksek düşünme, prova boyunca ve asıl işte aynı; gizleme birim başına prova profiliyle (yalnız
  sınanan birim çıkar, İşârât'ın kalanı görünür; asıl işte profil gerekmez); istem sürümlü tek dosya, düzeltmeler
  yalnız genel usule, âyete özgü ipucu girmez.
  **Kurulum (2026-11-11):** `scripts/d1-prova.py` (`hazirla`, `yazdir`, `karsilastir`), istem `docs/d1/prova-istemi.md`
  (v1). Gizleme kurulumda: yayındaki `genel` ve `tefsir` veritabanlarının kopyasından sınanan birimin Türkçe ve Arapça
  düğümleri ve onlara bağlı her satır silinir (cümle, paragraf, Arapça, bağlar, âyet ilişkileri, `risale_refs`, notlar,
  FTS), Osmanlıca İşârât bütünüyle çıkar (birimleri paralel değil); vektörler değişmez (dizin bölümleri veritabanından
  kurar). Eklerden (usul özeti, birim çizelgesi) sınanan birimden alınan her şey çıkar; 11–12'de V2'nin temsil örneği
  eserde yalnız orada geçtiği için onu anlatan cümle de çıktı. Sızıntı testi: gizlenen cümlelerin Kur'ân dışı 6'lı
  dizileri; risale ve istemde 3 ve üstü ortak dizi sızıntıdır (1–2'si kalıp ibare: "mâkabliyle vech‑i irtibatı").
  İstem ≈456 bin karakter: görev, usul, çalışma sırası, şablon, ekler ve İşârât'ın Arapça aslının tamamı (birim hariç).
  Taslağı yazan oturum: Fable 5.2, yüksek, proje dışında, yerleşik araçlar ve web kapalı, üç prova sunucusu.
  Not: Arapça baskıda birimin âyet satırı bir önceki düğümün sonunda kalır (9–10 c100–c101); yalnız âyet metnidir.
  **İnce istem (2026-11-12):** tam istemle taslak 1 ≈11,85 $ (liste fiyatı) tuttu, 5 saatlik limitin tamamını
  harcadı; maliyetin ≈3/4'ü istemin önbelleğe yazılması ve 32 turda yeniden okunmasıdır, istemin %88'i Ek 3. Taslak 1
  İşârât'tan 29 yer andı, 11 birimden (Fâtiha, Bakara 2 mukaddimesi, 6, 26–27, 30 mukaddimesi gibi uzak yerler dahil):
  tam metnin asıl katkısı bu olabilir. Kullanıcının kararı: tam istem kalır, ince biçim eklenir, taslak 2 onunla
  yazılır ve taslak 1'le karşılaştırılır (İşârât'a dayanan iddia, uzak birim sayısı, kendi tespiti oranı, uydurma);
  sonuca göre Max planı düşünülecek. `hazirla|yazdir 11-12 --istem ince`: Ek 3 yalnız Bakara 8, 9–10, 13, 14–15, 16 ve
  17–20'nin iki faslı; İşârât'ın kalanı `risale` eklentisinden (`read_section`, `search`, `semantic_search`), istem
  bunu söyler. `istem-ince.md` 171 bin karakter (tam 759 bin; tam biçim dünkü istemi harfi harfine aynı üretir).
  Veritabanları ortak, yeniden kurulmadı. Sızıntı testi temiz (`sizinti-ince.md`: istemde 1 kalıp ibare).
  **Taslak 2 (ince istem, 2026-11-12):** 690 sn, 37 tur, ≈7,55 $ (taslak 1: 11,85 $; araç sonuçları birikip bağlam
  ≈270 bine çıktı, tasarruf üçte ikide kaldı). İşârât'tan 21 yer, 10 birim; taslak 1'in uzak birimlerinin hepsini
  (2 mukaddimesi, 6, 26–27, 30 mukaddimesi, 17–20 mesele 5 ve 10) `search`, `semantic_search`, `get_passage` ile
  buldu, yalnız Fâtiha yok. İşaretler: kaynaklı 39, kendi tespiti 35 (taslak 1: 23 ve 42). Gizlenen metinle ortak
  6'lı dizi 4, hepsi geçiş kalıbı ("اعلم ان وجه نظم هذه الاية", "واما جملة …"). İlk bakışta tam metnin katkısı
  görülmedi; içerik değerlendirmesi kullanıcıda. Kullanıcı Max planına geçti.
  **Taslak 3 (ince istem, 2026-11-12):** 696 sn, ≈7,65 $. İşârât'tan 36 yer, 13 birim (Fâtiha ve Bakara 5 dahil);
  kaynaklı işaret 38, kendi tespiti 27; ortak 6'lı dizi 4, yine geçiş kalıpları. İki ince taslak da uzak birimlere
  araçla ulaştı; sayılarda tam istemin üstünlüğü yok. Okuma sayfasında üç taslak; değerlendirme kullanıcıda.
- D1.4 Değerlendirme ölçütü: usul özetinin maddeleri (münasebet, cümleler arası intizam, hey'et ve kelime
  nükteleri), i'râb ve belâgat doğruluğu, uydurma; mütehassıs taslağı İşârât'ın kendi metniyle yan yana okur; ezber
  otomatik ölçülür. Okuma sayfasında ölçüt çizelgesi olur (D4).
- D1.7 D2 oldu; D1.8 D5 oldu (2026-11-12).

**D4. Prova okuma ve not platformu** (kullanıcı bütün önerileri onayladı, 2026-11-12). D1, D2, D3 ve D5'e hizmet eder.
- Seçim: birim → taslak → dil; iki kip: taslak ile İşârât'ın gizlenen metni, taslak ile taslak (D2'de önce ve sonra).
- Notlar paragrafa ya da vecihe bağlı; türü (doğru, yanlış, eksik, fazla, uydurma, i'râb/belâgat, usul), önemi,
  okuyucunun adı; "ehline sor" işareti (Arapçayı kullanıcı denetleyemez; mütehassısa ayrı liste).
- Taslaktaki kaynak numarasının üzerinde dayandığı cümlenin kendisi; gizlenen metinle ortak kelime dizileri işaretli.
- Ölçüt çizelgesi (D1.4) her taslak için 0–2; taslaklar ve provalar sayıyla karşılaştırılır.
- Notlar tarayıcıda, dışa aktarma ile dosya; okuyucu dosyayı gönderir, betik birleştirip rapora işler. Taslaklar
  kapalı kalır: açık adreste durmaz.
- Belgeler `docs/d1/` altında (README durum ve dizin, prova başına rapor). Taslaklar, dökümler ve notlar
  yeniden üretilemez ve kapalıdır: ayrı yerel git deposunda, uzak kopyası özel depoda (denetim kayıtları gibi).
- **Kuruldu (2026-11-12):** `uv run python scripts/d1-prova.py okuma` → `data/d1/okuma.html` (tek dosya, bütün
  birimler; şablon `scripts/d1-okuma-sablon.html`); kaynak metinleri taslağın dökümündeki `cite` çağrılarından
  (üç taslağın 164 kaynağının hepsi); `notlar <dosya>` → `data/d1/notlar/` ve `provalar/<birim>/notlar.md`. Belgeler `docs/d1/`
  (README), kapalı kayıtlar `data/d1/` (kendi git deposu, README, `provalar/11-12/rapor.md` iskeleti). Tarayıcıda
  denendi: not, kaynak, iki kip, iki dil, çizelge, dışa aktarma ve rapor. Uzak özel depo kullanıcıda.
