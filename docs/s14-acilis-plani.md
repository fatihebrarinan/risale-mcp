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
sonra yönlendirici. S14.6'dan sonra.

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
