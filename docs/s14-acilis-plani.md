# S14: Bütün İslâm âlemine açılış (plan)

Kullanıcının fikri (2026-11-28): Âyinedâr yalnız Risale-i Nur okuyanların değil, Risale-i Nur'la hiç alakadar olmayan
insanların da gönül rahatlığıyla gelip kullanacağı, bütün İslâm âleminin platformu olsun. **Şart:** Risale-i Nur'la
ilgili sorulara cevaplar bugünkü gibi çok iyi kalır. Anlatım (siteler, sohbetin girişi) bu vizyona göre değişebilir;
genel kitle için fıkıh, siyer gibi kütüphaneler ve yeni modlar eklenebilir. Fıkıh ve siyer önce sohbette ve mevcut
eklentilerin içinde olur; ayrı eklenti ileride, istenirse.

Kullanıcının notu: bu büyük bir seçim, parçalara iyi ayrılmalı. Bu yüzden plan **kapılı**dır: her adım küçük bir
çıktı verir ve kullanıcının kararıyla biter; sonraki adım ancak o kararla başlar. **S14.6'ya kadar yayındaki hiçbir şey
değişmez**: envanter, ölçüm ve denemeler yerelde, metinler önizlemede durur. Her adımda geri dönülebilir.

Durum ve sıra `PLANLAR.md`'dedir; bu belge ayrıntıdır.

## Değişmeyenler

- Yapay zekânın ürettiği hiçbir şey tefsir ya da fetva diye anılmaz; her söz kaynağına bağlıdır, alıntılar denetlenir.
- Verinin yapısı değişmez: Risale'nin ekseni "veride değil görünümde"dir (CLAUDE.md › Amaç). Değişen yalnız görünüm
  katmanıdır: anlatım, varsayılanlar, talimat, araçların sırası.
- Risale-i Nur cevaplarının kalitesi ölçüyle korunur (S14.3); düşüş varsa değişiklik yayına çıkmaz.
- Yeni kaynak eklemeden önce izin (`docs/izinler.md`); eser seçimi ilim ve ihtisasa göre, meşrebe göre değil.

## Adımlar

### S14.1 Kararlar (kullanıcı, sohbetle)

Çıktı: bu belgenin "Kararlar" bölümü. Hepsi bir anda gerekmez; her birinin hangi adımdan önce gerektiği yazılı.

- **K1. Merkez** (S14.5'ten önce): platformun tarifi "Kur'ân ve onun etrafındaki ilimler" mi (Kur'ân ortak adres;
  birinci gayeyle doğrudan bağlı), yoksa daha nötr "İslâmî kaynaklar kütüphanesi" mi?
- **K2. Genel bir soruda Risale'nin yeri** (S14.4'ten önce): bugünkü talimat Risale'yi hep önce koyar. Genel soruda
  ("sabır nedir") Risale yine önce mi, yoksa ilgisine göre öbür kaynaklarla eşit mi? Risale'ye dair soruda Risale
  önce kalır.
- **K3. Risale'nin anılışı** (S14.5'ten önce): Risale markadan çıkıp adıyla anılan, öne çıkan bir kütüphane mi olur
  ("Risale-i Nur Külliyatı: bütün eserler, cümle düzeyinde atıfla")? Bugünkü okuyucular "artık bizim değil"
  hissetmesin.
- **K4. Adlar** (S14.5'ten önce): yayıncı adı "Risale MCP" ve `risalemcp.com` eklentiler için kalır mı, yoksa
  Âyinedâr çatısına mı geçer (S13.22 ile ilişkili; eklentilerin MCP adresleri değişmez)?
- **K5. Fıkıhta sınır** (E10'dan önce): "kitaplar ne diyor, mezhebiyle; hüküm yok, kişiye özel soruda ehline
  yönlendirme" yeterli mi, yoksa fıkıh soruları tamamen dışarıda mı kalır?

### S14.2 Envanter (Claude)

Bugün "Risale-i Nur" nerede geçiyor ve vizyona göre ne olmalı. Çıktı `docs/s14-envanter.md`: her satırda yer, bugünkü
metin ve öneri (kalır / genelleşir / kullanıcının kararı). Kapsam: çatı sitesi (`site-ayinedar/`, tr ve en; başlık,
açıklama, JSON-LD, paylaşım kartı), sohbet (giriş sayfası `sohbet_hesap.HERO`, Hakkında, gizlilik ve şartlar, PWA
manifestosu, mod açıklamaları `kipler.py`, örnek kartlar, karşılama sözleri, rehber metni ve örnek konuşma, alt satır,
kütüphane seçicisi), sohbetin talimatı (`sohbet.py`; ortak bloklar `server.py`, MCP talimatı bayt bayt aynı kalmalı),
okuma platformu (Kur'ân taslakları; Risale burada kaynaklardan biri), eklentilerin sitesi (`site/`; Risale'ye özgü
kalabilir), arama motorlarına giden açıklamalar. Yayına dokunmaz. **Kapı:** kullanıcı satırları işaretler.

### S14.3 Ölçü setleri (Claude; set kullanıcının onayıyla)

Değişiklikten önce iki set donar ve bugünkü sistemle temel ölçüm alınır.

- **Risale seti:** bugünkü altın sorular (`olc --hizli` 8 soru, tam set 29 soru). Ölçüt: doğrulanan atıf oranı,
  beklenen bölümün okunması, maliyet; S14.4'ten sonra düşmemeli.
- **Genel set** (yeni, ≈25 soru): tefsir, hadis ("bu söz hadis mi"), akaid ve kelâm, siyer, kavram ve terim, ahlâk,
  Risale'nin de değindiği genel konular, fıkıh tuzağı (kişiye özel fetva isteği), kütüphanede olmayan soru (dürüstçe
  "bulamadım" demeli). Kullanıcı soruları onaylar.

Çıktı: iki setin temel ölçümü (soru başı maliyet ve süre dahil). **Kapı:** kullanıcı seti onaylar.

### S14.4 Sohbetin varsayılanları (yerelde deneme)

Hangi kütüphanenin ne zaman açık olduğu ve talimatta Risale'nin yeri (K2'ye göre). Seçenekler:

- **A.** Bütün kütüphaneler varsayılan açık.
- **B.** Model soruya göre seçer (yönlendirici: Risale sorusu Risale'ye, âyet tefsire, rivayet hadise…).
- **C.** Bugünkü gibi okuyucu seçer, varsayılanlar ve anlatım değişir.

Her seçenek iki setle ölçülür; rapor: Risale seti düştü mü, genel set ne kazandı, soru başı maliyet ve süre (araç
sayısı arttıkça token artar; model Haiku). Yayına dokunmaz. **Kapı:** kullanıcı seçeneği seçer.

### S14.5 Anlatım (S13.23.5 buraya katıldı)

K1, K3, K4 ve S14.2'nin işaretleriyle yeni metinler: çatının ana sayfası, sohbetin giriş sayfası (S13.23.5), Hakkında,
mod açıklamaları, örnek kartlar, karşılama sözleri, rehber ve örnek konuşma (Risale dışı bir örnek de gerekebilir;
cevap sistemin gerçek cevabıdır, kısaltılmaz, düzeltilmez), paylaşım kartları ve arama motorlarına giden açıklamalar.
Ölçü yine "eserlerin ne dediğini yansıtır" (CLAUDE.md › Âyinedâr). Metinler önizlemede; **kapı:** kullanıcı okur ve
düzeltir.

### S14.6 Yayın ve izleme

S14.4'ün seçimi ve S14.5'in metinleri birlikte yayına çıkar (deploy öncesi kayıt kuralıyla). Yenilikler'e duyuru
taslağı (önce taslak, kullanıcı okur). Bir hafta kullanım ve geri bildirim izlenir (`sohbet usage`, `geri-bildirim`);
Risale seti yayından sonra yeniden ölçülür. Geri dönüş yolu: eski varsayılanlar bir ayarla geri gelebilmeli.

### S14.7 Yeni modlar

S13.18 ile birleşir (kip kaydı tek kaynak, `kipler.py`): kavram ve terim (Ta'rîfât, Müfredât), karşılaştırma (bir
meselede farklı eserler), hadis kontrolü (eklentideki skill'in sohbetteki karşılığı), siyer olayı (E9'dan sonra);
sonra yönlendirici. S14.6'dan sonra. Konu taramasının öbür kütüphanelere genişlemesi de burada düşünülür (S14.2,
2.10: o zamana kadar "Risale-i Nur'da konu taraması" olarak Risale'ye ait kalır).

## Kütüphaneler

### E9 Siyer

- **E9.1 Seçim ölçütü** (genel platform için yazılı ölçüt; E2'nin ölçütünün ve `catalog/excluded.py`'nin genişlemesi):
  ilmî kabul, muteber baskı, izin. Kullanıcı onaylar.
- **E9.2 Eser listesi ve kaynak:** bugün var olanlar (Mevâhib, eş-Şifâ, Delâilü'n-Nübüvve) ve adaylar (İbn Hişâm'ın
  es-Sîre'si, İbn Sa'd'ın et-Tabakāt'ı ve öbürleri), OpenITI'de sabit commit, lisans. **Kapı:** kullanıcı listeyi onaylar.
- **E9.3 Ayrıştırma:** `klasik` koleksiyonuna (ayrı eklenti gerekmez), klasik sunucusu ve sohbette Klasik eserler
  kütüphanesiyle.
- **E9.4** Siyer modu (S14.7).

### E10 Fıkıh (en son)

En riskli kütüphane: fıkıh sorusu amel için sorulur. Ayaktaki "fetva değildir" yazısı yalnız başına yetmez.

- **E10.1 Sınır belgesi** (K5): kitapların dediği mezhebiyle ve atfıyla; hüküm verilmez; kişiye özel soruda kitapların
  dediği gösterilir ve ehline (müftü) yönlendirilir. Kullanıcı onaylar.
- **E10.2 Eser listesi:** dört mezhebin muteber metinleri dengeli (meşrebe göre değil ilme göre), izin ve kaynak.
- **E10.3 Talimat ve ölçü:** fetva tuzaklı soru seti; talimat önce bununla ölçülür.
- **E10.4 Ayrıştırma**, sonra istenirse ayrı eklenti (E10.5, ileride).

## S14.3'ün temel ölçümü (2026-11-28; model Haiku 5.5 medium)

Raporlar `data/interim/golden/` altında (git'e girmez); rapor aracı `risale_mcp.genel_olc`.

| Ölçüm | Sonuç |
|---|---|
| Risale seti, bugünkü sistem (`20261128-092742-…`) | atıfların 314/329'u doğrulandı (%95,4); beklenen bölümlerin 27/34'ü okundu; 0,15 $ (soru başı 0,005 $), ortalama 21 sn |
| Genel set, yalnız Risale (bugünkü varsayılan, `20261128-093350-…`) | bütün cevaplar yalnız Risale'den; beklenen yerlerin 28/132'si okundu, 11/132'si kaynakçada; 3 doğrulanamayan; 0,15 $ |
| Genel set, bütün kütüphaneler açık (`20261128-094320-…`) | beklenen yerlerin 35/132'si okundu, 22/132'si kaynakçada; 2 doğrulanamayan; 0,16 $ |

**Bulgular (S14.4'ün girdisi):**
- Kütüphaneleri açmak tek başına yetmiyor: hepsi açıkken bile model hadis ve tefsir sorularının bir kısmı dışında
  hep Risale'ye gidiyor. Klasik eserler yalnız G25'te (Kimyâ-yı Saâdet) açıldı; siyer, akaid, kavram ve ahlâk
  sorularında Mevâhib, İhyâ, Şerhu'l-Mevâkıf, Ta'rîfât hiç okunmadı. Sebep talimat: "this page answers only from the
  Risale-i Nur", "Keep the Risale-i Nur first". G12'de (Hendek) model "bu sayfa yalnızca Risale-i Nur'dan cevap
  verdiği için savaşın tarihini anlatamam" dedi; Mevâhib açıktı.
- Maliyet farkı küçük (0,15 → 0,16 $); asıl maliyet sorusu talimat değişince ölçülür.
- Fıkıh tuzağında (G23) davranış iyi: kişiye özel hüküm yok, ehline yönlendirme var (Risale'nin kasr mektubuyla).
- Küçük hatalar: G25'te klasik eserden yapılan alıntı kaynakçada "Adresi bulunamadı ⚠ doğrulanamadı" oldu; aynı
  cevapta tırnak içindeki bir kitap adına "Risale'de bu sözlerle bulunamadı" uyarısı yanlışlıkla eklendi (S14.4'te
  bakılır).
- Rapor aracındaki bir hata (öneksiz Risale okuma araçları sayılmıyordu) ilk raporda düzeltildi; sayılar düzeltilmiş
  hâlidir.

## S14.4'ün denemeleri (2026-11-28; Haiku 5.5 medium, hepsi `SOHBET_GENEL=1` ile yerelde)

Genel set (26 soru; bütün kütüphaneler açık):

| Deneme | Okundu | Kaynakçada | Doğrulanamayan | Yalnız Risale'den cevaplanan | $ |
|---|---:|---:|---:|---|---:|
| Temel (eski talimat) | 35/132 | 22/132 | 2 | 19 soru | 0,16 |
| A1 genel talimat | 64 | 39 | 11 | 9 soru | 0,19 |
| A2 + İhyâ ve hadis aramasını adıyla isteyen cümle | 74 | 45 | 6 | 0 (hadis 19 soruda: gereğinden çok) | 0,20 |
| A3 search_all + Risale araçlarına etiket + "Risale varsayılan değildir" ilkesi | 67 | 40 | 0 | 2 (G10, G20) | 0,21 |
| **A4 search_all + Risale araçları önekli (`risale_…`), ilke yok** | 66 | 45 | 2 | 2 (G10 kader, G24 kredi kartı) | 0,18 |

Risale seti (29 soru): temel %95,4 atıf doğrulandı, beklenen bölümlerin 27/34'ü okundu; A4 iki koşuda %97,2 ve %96,8,
25/34 ve 26/34 (fark tek koşunun gürültüsü içinde; D15 iki koşuda da adıyla anıldı, okunmadı); Risale soruları yine
Risale'den (yalnız "Mi'rac nerede ele alınır" genel soru gibi klasik eserlere de baktı); doğrulanamayan 0.

**Bulunan sebepler** (kullanıcının sorusu: "neden yalnız Risale?"): (1) iş akışının ilk adımı her soruyu Risale'nin
anlamsal aramasına gönderiyordu; Türkçe soru Türkçe külliyatta yüksek puan alıyor (0,58'e karşı klasik 0,50, hadis
0,42), model zengin sonuçla yetiniyordu: yalnız Risale'den cevaplanan yedi sorunun yedisinde ilk adım buydu; Arapça
kütüphanelerde Türkçe arama iyi çalışıyor ("sabır nedir" İhyâ'nın sabır kitabını buluyor). (2) Risale'nin öneksiz
araçları varsayılan gibi görünüyordu; model öbür kütüphanelerin kimliklerini onlarla okumaya çalışıp (7 soruda 11
çağrı) hata alınca o kütüphaneyi bırakıyordu.

**Düzeltmeler** (konu dayatmadan; A2'nin adıyla isteyen cümlesi kullanıcının itirazıyla geri alındı): `search_all`
(anlamca arama bütün açık kütüphanelerde, sonuçlar kütüphane kütüphane); genel sayfada Risale araçları önekli
(`risale_search`…, kullanıcının önerisi; Kur'ân'ın `get_ayah`'ı ortak adres olduğu için öneksiz; önek yalnız modelin
yüzü, içeride bugünkü adlar); Risale aracına başka kütüphanenin kimliği gelirse hata iletisi doğru aracı söyler
(yalnız o kütüphane açıksa); öbür kütüphanelerin alıntısında üç kalıp sayfada onarılır (tırnaklı Türkçe tercüme,
alıntıyla işaret arasına yazılan tercüme, öneksiz kimlik); kitap adı gibi tırnaklı söz uyarı almaz. "Risale-i Nur'dan"
kipi bugünkü sayfanın aynısıdır (talimat ve araçlar testle kilitli). Ölçüm paralel (`olc --paralel`, varsayılan 10):
29 soru 2,5 dakika.

**Seçenekler:** B (model kütüphane açar) denenmedi: bütün kütüphaneleri açmak maliyeti az artırıyor (soru başı
≈0,007 $), `search_all` zaten soruya göre seçtiriyor. Öneri: A (genel sayfada bütün kütüphaneler varsayılan açık,
okuyucu kapatabilir) + "Risale-i Nur'dan" kipi.

## Açık sorular (sırası gelince)

- **Dil engeli:** Risale Türkçe, öbür kütüphaneler Arapça; genel Türk okuyucu Arapça alıntı ve "Yapay zekâ tercümesi"
  damgası görür. Tercüme programı 2026-11-09'da donduruldu; siyer gibi çok okunan alanlarda yayımlanmış Türkçe tercüme
  için izin aramak yeniden düşünülebilir.
- **Bütçe:** daha çok kütüphane daha çok token demek; aylık tavan (100 $) ve kişi başı günlük hak S14.4'ün ölçümüyle
  gözden geçirilir.

## Kararlar

- **K1 (2026-11-28): Kur'ân ve Sünnet merkezli.** Tarif: "Kur'ân ve Sünnet etrafında, İslâm ilimlerinin kaynakları."
  (Kullanıcının sözü; önerideki "klasik" kelimesi yok.) Anlatımın ikinci yarısı usuldür: her söz kaynağıyla, alıntılar
  denetlenir. Risale bu çerçevenin içinde durur. Örnek cümleler S14.5'te yazılır.
- **K2 (2026-11-28): önce Kur'ân ve Sünnet, sonra açıklayanlar.** Genel bir soruda cevabın iskeleti varsa ilgili âyet
  ve hadisle başlar; ardından onları açıklayanlar (tefsirler, Risale, klasik eserler) ilgisine göre. Soru açıkça
  Risale'ye dairse (eser adı, Bediüzzaman, "Risale'de…") Risale önce gelir, cevap bugünkü gibi kurulur. **"Risale-i
  Nur'dan cevapla" seçeneği kesinlikle olacak** (Ayarlar'da ya da modlarda; açıkken bugünkü davranış aynen sürer).
  Hangi sorunun "Risale'ye dair" sayılacağı ve kütüphanelerin kimin açtığı S14.4'te ölçüyle.
- **K3 (2026-11-28): Risale adıyla öne çıkan kütüphane.** Listede K1'in sırasıyla yerini alır, kendine has özelliğiyle
  anılır ("Risale-i Nur Külliyatı: Bediüzzaman'ın bütün eserleri, Türkçe, cümle düzeyinde atıfla"); ana sayfada bugünkü
  okuyuculara seslenen kısa bölüm ("Risale-i Nur'dan cevapla" seçeneğiyle). Klasik eserler "İslâm ilimlerinin
  klasikleri" diye tanıtılır (Risale'nin havale ettiği eserler bir özellik olarak anılabilir); ana sayfada iki örnek:
  genel soru ve Risale sorusu. Ayrı kapı (C) şimdilik yok, gerekirse B'nin üstüne kurulur.
- **K4 (2026-11-28): adlar.** (1) Çatı ve sohbette ayrı yayıncı adı anılmaz, hizmetin adı Âyinedâr (alt bilgi, JSON-LD
  kurum adı); S14.5'te. (2) Dizinlerdeki yayıncı adı ("Nur Hadimleri") ve dört kütüphaneli Claude eklentisinin genel
  adı ("Risale-i Nur Library") başvurular sonuçlanınca bir sonraki gönderimde "Âyinedâr" olur; S13.22 ile. (3) Eklenti
  tanıtımı S13.22'de `connect.ayinedar.org`'a. (4) `risalemcp.com` ve MCP adresleri değişmez (kurulumlar, dizin
  kayıtları, Claude'un simgesi). (5) İç proje adı "Risale MCP" kalır. "Nur Hadimleri"nin kullanıcı için özel bir yeri
  yok.
- **K5 (2026-11-28): fıkıhta "kitaplar ne diyor, mezhebiyle" (B).** Dört mezhepten muteber metinler; cevap "X kitabı
  şöyle der" diye kurulur, "mezhebin hükmü budur" diye değil; mezhepler arasında tercih ve hüküm yok; kişiye özel soruda
  kitapların dediği genel olarak gösterilir, açıkça ehline yönlendirilir. Eser seçiminde müftâ bih görüşü kendisi
  söyleyen eserler öne alınır (Hanefîlerde Reddü'l-Muhtâr gibi). Okuyucunun mezhep seçmesi (C) B ölçüldükten sonra
  ayrıca düşünülür. Fetva tuzaklı sorular ölçü setine girer (E10.3); "Tefsir ve fetva değildir" yazısı kalır.

**S14.1 bitti (2026-11-28).**
