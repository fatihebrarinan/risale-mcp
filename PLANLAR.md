# Planlar

Projenin bütün planları, sırası, bekleyen ve dondurulan işleri bu belgededir (kullanıcının kararı, 2026-11-09); adım kaydı
(biten işlerin ayrıntısı, eski aşamalar) 2026-11-19'dan beri `KAYIT.md`'dedir (kullanıcının kararı). Kurallar:

- Yeni plan, karar ve biten adım buraya, tarihli yazılır. CLAUDE.md yalnız kalıcı bağlamı tutar (ilke, veri modeli,
  komut, kural). Bir adımın kalıcı bir altyapısı çıkarsa onun kısa tarifi CLAUDE.md'ye de girer.
- Bir işin ayrıntılı planı gerekirse `docs/` altında ayrı belge olabilir, ama durumu ve sırası burada tutulur.
  `docs/` altındaki eski plan belgeleri (`tefsir-altyapi-plani.md`, `tefsir-pilot-degerlendirme.md`,
  `tercume-programi.md`, `mvp-kitaplar.md`, `bag-altyapisi-plani.md`, `hadis-plani.md`…) ayrıntı ve geçmiştir.
- İşler kimlikle anılır ("Adlandırma"). Biten iş **aynı değişiklikte** "Biten" bölümüne tek satır olarak taşınır,
  ayrıntısı `KAYIT.md` › "Kimlikli işler"e ya da belgesine gider; "Sıradaki"de yalnız tablodaki işlerin ayrıntısı durur.
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

**Yön (kullanıcının kararı, 2026-11-21; 2026-11-21'de düzeltildi):** taslak işinin **geliştirme aşaması bitti**:
kullanıcının sorusu ("yapay zekâ neyi yapabilir, neyi yapamaz, İşârât'ın bir mislini yazabilir mi?") cevabını buldu.
Çalışma temposu aynı kalır; değişen yalnız taslak hattının geliştirilmemesi. (1) D5 Max planı süresince sürer
(Max 2026-12-14'te biter, bir haftalık kullanım sıfırlama hakkı var), Bakara biterse ne âlâ. (2) Odak: MCP
sunucularının iyileşmesi, taslakların ve sunucuların insanlara, özellikle ehil ve tefsirle ilgilenenlere ulaşması
(S8 sonuç yazısı ile başlar). (3) Max'tan sonra Pro plana dönülür: **ondan önce taslak sunucusundaki D5 kuyruğu
durdurulur** (aynı aboneliği kullanır, Pro kotasını yer). (4) Taslak usulünün değişmesi ve vecih haritası
"Fikirler"de.

## Adlandırma (kullanıcının kararı, 2026-11-09)

Her iş bir **kimlik** alır: alan harfi ve o alanda artan numara (`E2`), alt adım noktayla (`E2.1`). Kimlik verilince
değişmez, biten ya da bırakılan işin kimliği yeniden kullanılmaz. **Sıra** ayrıdır: aşağıdaki tablonun satır
sırasıdır; sıra değişince yalnız satırlar yer değiştirir. Eski adlar (Aşama 20, HA7, Y1.1…) "Eski adı" sütununda
durur, `KAYIT.md`'deki geçmiş onlarla okunur.

| Harf | Alan |
|---|---|
| **E** | Eserler: listeler, ekleme, nüsha |
| **S** | Sunum ve erişim: site, yenilikler, dizinler, yeni platformlar |
| **A** | Araç ve veri: Risale tarafındaki yetenekler |
| **D** | Deneme ve araştırma |
| **B** | Bakım: kontrol ve küçük açıklar |

Son verilen kimlikler: E10, S14, A4, D16, B13 (yeni iş bir sonrakini alır).

## Sıradaki

Sıra kullanıcının kararıdır. Sıranın ve "Sıradaki"nin tarihli geçmiş notları `KAYIT.md` › "Sıradaki'nin notları"nda.

**Şimdi** (her adımda güncellenir; yalnız şu an yapılan iş, kullanıcıdan beklenen ve tarihli hatırlatmalar, kısa
tutulur: kullanıcının kararı, 2026-11-19 ve 2026-11-27; eski notlar `KAYIT.md` › "Sıradaki'nin notları"):
- **Son adım (2026-11-28): S14.8 bitti ve yayında.** Ayrıntı "Sıradaki" › S14 › S14.8. `search_all`'ın sırası
  (tefsir, Risale, hadis, klasik) kesin değil: kullanıcı cevaplara göre yeniden bakabilir. Sonra S14.7 (yeni modlar) ya
  da E9. **Kullanıcıdan beklenen:** Yenilikler duyurusunun taslağı (aşağıda).
- **Son adım (2026-11-28): S13.23 bitti, S14 planlandı.** Kullanıcının fikri: Âyinedâr bütün İslâm âleminin
  platformu olsun, Risale cevapları bugünkü gibi kalsın. Plan `docs/s14-acilis-plani.md` (kapılı; S14.6'ya kadar
  yayında değişiklik yok); S13.23.5 (giriş sayfası) S14.5'e katıldı. S14.1'in beş kararı verildi (2026-11-28: Kur'ân
  ve Sünnet merkezli; önce Kur'ân ve Sünnet, "Risale-i Nur'dan cevapla" seçeneği; Risale adıyla öne çıkan kütüphane;
  çatıda Âyinedâr adı; fıkıhta "kitaplar ne diyor, mezhebiyle"). S14.2 bitti (öneriler uygun; giriş
  sayfasının ve rehberin örneği altyapıdan sonra genel bir soruyla, Risale'nin de ele aldığı bir konudan; konu taraması
  Risale'ye ait kalır). S14.3 bitti: genel set dondu (`tests/golden/genel_sorular.json`,
  26 soru), temel ölçüm alındı. S14.4 bitti (2026-11-28): genel talimat, `search_all`, önekli Risale araçları,
  "Risale-i Nur'dan" modu; kullanıcı A'yı seçti (bütün kütüphaneler varsayılan açık), sayfaya bağlandı; hepsi
  `SOHBET_GENEL`'in arkasında, yayın S14.6'da. İnce ayarlar S14.8'de. S14.5 bitti (2026-11-28): metinler işlendi (çatı tr/en, sohbetin
  `SOHBET_GENEL`'e bağlı metinleri), genel örnek "Kişi imanını nasıl arttırır?" (22. üretim, kullanıcı seçti). S14.6: genel sayfa
  yayında (2026-11-28, `scripts/deploy.sh --code`, araç çıktısında fark yok, sunucuda uçtan uca denendi); okuyucuya giden
  metinlerde noktalı virgül virgüle çevrildi. **Kullanıcıdan beklenen:** Yenilikler duyurusunun taslağını okumak
  (`docs/yenilikler/2026-11-28-kuran-ve-sunnet-etrafinda.md`, önizleme `lab.ayinedar.org/onizleme/`); onaydan sonra
  `python3 scripts/site-uret.py yayinla yenilikler/2026-11-28-kuran-ve-sunnet-etrafinda --gonder`. Sonra S14.8 ya da S14.7.
- **Önceki adım (2026-11-27 gecesi): S13.15 bitti.** Çatı sitesi `ayinedar.org` yayında (S13.15.6): ana sayfa sohbete
  çağırır, Yenilikler ve Çalışmalar çatıda (risalemcp.com'daki adresler 308), çatı ve sohbet arama motorlarına açık.
  Ayrıntı `KAYIT.md` › S13.15.6. **Önde (kullanıcının kararı, 2026-11-27):** S13.23. B13, S13.23.1–S13.23.4 ve S13.23.6'nın
  sohbet tarafı yayında (örnek cevabı kullanıcı onayladı; okuyucuya görünen ad "mod"). S13.23.7 (rehber sağ üstteki bildirimle başlar) yayında (2026-11-28). S13.23.8 (okuma platformunda aynı
  bildirim ve rehber) yayında (2026-11-28). S13.20 (İngilizce ve Arapça arayüz) S14'ün anlatımından sonra. ≈2026-12-04 e-posta teslim süreleri ve spam yeniden bakılır
  (`sohbet_hesap eposta-sure`, Postmaster Tools). S13.22 dizin kararlarını bekliyor.
- **Arama motorları (2026-11-27):** kullanıcı siteye baktı (sorun yok), Search Console (alan adı mülkü `ayinedar.org`) ve Bing'e kaydoldu; iki site haritası ikisine de gönderildi. Google çatınınkini okudu (18 sayfa), sohbetinkine ilk anda "Getirilemedi" dedi (harita sorunsuz geliyor; birkaç gün içinde düzelmezse yeniden gönderilir).
- **Yenilikler duyurusu yayında (2026-11-27):** kullanıcı web düzenleyicide düzeltti, `ayinedar.org/yenilikler/2026-11-27-ayinedar.html`.
- **Kullanıcıdan beklenen:** "Bekleyen"deki
  cevaplar gelince haber; dizin metinleri başvurular sonuçlanınca (`docs/e5-dizin-metni-taslagi.md`); okuma
  platformunun karşılaması (`read.ayinedar.org/#/~hosgeldin`) ve ilk davetler (`scripts/sunucu.sh taslak davet
  <e-posta>`); lügatın eşleme örnekleri (`data/interim/lugat/olcum.md`); E8.6 için Arapça okuyan bir denetçi.
- **Tarihli hatırlatmalar:** ≈2026-11-30 Anthropic'ten Risale için cevap yoksa S4.3'ün yedek yolu. ≈2026-12-02 sohbet
  denemesinin sonu: `sohbet usage` ve `geri-bildirim --days 7` (sunucuda `.venv/bin/python -m risale_mcp.sohbet …`;
  başlangıç kaydı `data/interim/sohbet/deneme-baslangic-20261125.md`), sonra S13'ün sırası gözden geçirilir.
  ≈2026-12-10 DMARC `p=quarantine`. **2026-12-13** kullanıcı mesaj gönderecek; taslaklar bitmediyse D5 kuyruğu
  durdurulur (`scripts/taslak-sunucu.sh dur`; Max 2026-12-14'te biter, kuyruk aynı aboneliği kullanır). Kuyruk
  durunca B3, E6 ve D16.
- **Kendi kendine süren:** D5 kuyruğu Bakara'nın sonuna kadar (`scripts/taslak-sunucu.sh durum`,
  `https://lab.ayinedar.org/d5.html`).

Sıra (kullanıcının kararı, 2026-11-27): S13'ün açık adımları önde (S13.22 dizin kararlarına bağlı); sonra mekanik
işler (E7, B9, E8; Pro'da da yürür); tefsir verisine Aralık'ta, D5 kuyruğu durunca tek dokunuş (B3, E6), D16 da o
zaman. Önceki gerekçe (2026-11-22) `KAYIT.md` › "Sıradaki'nin notları"nda. **2026-11-28 (kullanıcının kararı):**
S14 en önde; E9 S14.6'dan sonra, E10 en son.

| Sıra | Kimlik | İş | Eski adı |
|---:|---|---|---|
| 1 | S14 | Bütün İslâm âlemine açılış: kararlar, envanter, ölçü setleri, sohbetin varsayılanları, anlatım (giriş sayfası dahil), yayın, yeni modlar | |
| 2 | S13.22 | Göçün tamamlanması: eklentilerin tanıtımı `connect.ayinedar.org`'a, risalemcp.com'un kalan sayfaları (dizin kararlarından sonra) | S13.15.7 |
| 3 | E9 | Siyer kütüphanesi: seçim ölçütü, eser listesi, `klasik` koleksiyonuna ayrıştırma, siyer modu (S14.6'dan sonra) | |
| 4 | S13.18 | Öbür kipler: ders, beni sına, müzakere, kavram, karşılaştırma; yönlendirici | S13 (4) |
| 5 | S13.19 | Okuma ve paylaşma: lügat, okuma platformuyla bağ, âyet görünümü, defter, paylaşım bağlantısı | S13 (5)–(9) |
| 6 | S13.20 | İngilizce ve Arapça arayüz | S13 (10) |
| 7 | S13.21 | Tanıtımdan sonra: gerçek kullanımdan öğrenmek | S13 (3) |
| 8 | E7 | Hadis: (a) rivayet grupları, (c) yalnız Türkçe aktarılan hadisler | HA7 |
| 9 | B9 | Türk hattının iki kaynağı arasındaki işaret farkları | |
| 10 | E8 | Külliyatın Arapça tercümesi (İhsan Kasım; risaleoku'nun izni, 2026-11-23): ayrıştırma, bölüm eşlemesi, Sîret-i Zâtiyye mecmua, Arapça arama | |
| 11 | B3, E6 | **Aralık'ta, D5 kuyruğu durunca, tek tefsir kurulumu:** B3 (uzun cümleler, kayan âyet birimleri), E6 Elmalılı'nın eklenmesi, el-Bahru'l-Muhît (sıraya girince kimlik alır) | |
| 12 | D16 | Kuyruk durunca: Bakara'nın maliyet raporu ve hesap kararı | |
| 13 | B12 | Anlamsal dizinin bellekteki Python yapılarını sıkıştırmak (tefsir 1,26 GB → ≈0,5 GB) | |
| 14 | E10 | Fıkıh kütüphanesi: sınır belgesi, dört mezhebin dengeli listesi, fetva tuzaklı ölçü, ayrıştırma (en son) | |

- S14 **Bütün İslâm âlemine açılış** (kullanıcının fikri ve kararı, 2026-11-28; plan `docs/s14-acilis-plani.md`):
  Âyinedâr Risale-i Nur'la hiç alakadar olmayanların da gönül rahatlığıyla kullanacağı, bütün İslâm âleminin platformu
  olsun; Risale sorularında cevaplar bugünkü gibi kalır (ölçüyle korunur). Kapılı plan: her adım kullanıcının
  kararıyla biter, **S14.6'ya kadar yayında hiçbir şey değişmez**.
  - S14.1 (bitti, 2026-11-28; kararlar `docs/s14-acilis-plani.md` › Kararlar) **Kararlar** (kullanıcı): K1 merkez (Kur'ân mı, nötr "İslâmî kaynaklar" mı), K2 genel soruda Risale'nin
    yeri, K3 Risale'nin anılışı (adıyla öne çıkan kütüphane), K4 adlar ("Risale MCP", `risalemcp.com`), K5 fıkıhta
    sınır (E10'dan önce).
  - S14.2 (bitti, 2026-11-28; `docs/s14-envanter.md` › Kullanıcının işaretleri) **Envanter** (Claude): "Risale-i Nur" nerede geçiyor, ne olmalı (`docs/s14-envanter.md`); kullanıcı işaretler.
  - S14.3 (bitti, 2026-11-28; sonuçlar `docs/s14-acilis-plani.md` › S14.3'ün temel ölçümü) **Ölçü setleri:** Risale seti (bugünkü altın sorular) ve yeni genel set (≈25 soru, kullanıcı onaylar);
    bugünkü sistemle temel ölçüm.
  - S14.4 (bitti, 2026-11-28; `docs/s14-acilis-plani.md` › S14.4'ün denemeleri; A seçildi) **Sohbetin varsayılanları** (yerelde): A bütün kütüphaneler açık, B model seçer, C okuyucu seçer; iki setle
    ölçülür (Risale seti düşmemeli, maliyet); kullanıcı seçer.
  - S14.5 (bitti, 2026-11-28; yayına S14.6'da; `docs/s14-anlatim-taslagi.md`) **Anlatım** (S13.23.5 giriş sayfası buraya katıldı): çatı, sohbetin girişi, Hakkında, modlar, örnekler;
    önizlemede, kullanıcı okur.
  - S14.6 (yayında, 2026-11-28; duyuru taslağı kullanıcının okumasını bekliyor; izleme kullanıcının kararıyla yok) **Yayın ve izleme:** S14.4 ve S14.5 birlikte; duyuru taslağı; bir hafta izleme; geri dönüş yolu.
  - S14.8 (bitti ve yayında, 2026-11-28, `deploy.sh --code`, araç çıktısında fark yok) **İnce ayarlar ve iyileştirmeler** (kullanıcının kararı, 2026-11-28: S14.4'ten sonra ayrı adım; sıra ve
    usul kullanıcının kararı, 2026-11-28: önce sorunların aslı, ara ölçüm yok, en sonda yalnız genel set). Sıra:
    1. (bitti) G5'in çökmesi: atıf dizini ilk kurulurken eşzamanlı istek yarım dizini görüyordu (yeniden üretildi;
       yayında da olabilirdi); kilit ve tek seferde yerine koyma, test.
    2. (bitti) İşaretsiz sözün yanlış uyarıları (son koşularda 45 → 29): Yorum başlığının altındaki söz bulunursa
       işaret alır, bulunmazsa uyarı almaz; tırnaklar türüyle eşlenir (işaretli ve kısa söz yeni söz açmıyor, iç içe
       «», "“…”"); lügat anlamları ve alt başlıklar söz sayılmaz. Kalan uyarılar çoğu yerinde (modelin tırnakladığı
       kendi özeti, âyet ve hadisin kendi tercümesi, harf çevirisi).
    3. (bitti) "Risale-i Nur'a göre" açılışı yalnız Risale'den kurulan cevaplarda çıkıyordu (kaynağı söylüyor). Kural
       (kullanıcının kararı): cevap tek kütüphaneye dayanıyorsa açılış bunu söyler.
    4. (bitti) G10, G24: `search_all` Şerhu'l-Mevâkıf'ı ve Kenz'in ribâ rivayetini buldu, model okumadı; Risale soruyu
       tam cevaplayınca duruyor (G9, G11'de klasiklere her koşuda gidiyor). Kullanıcının kararı: Risale kâfiyse yalnız
       Risale verilebilir, hiçbir kütüphane zorunlu değil; talimatta Risale'yi öne çıkaranlar kalktı ("fullest Turkish
       voice", "never leave it out", öbür kütüphanelere "only what the question needs"); `search_all` sırası tefsir,
       Risale, hadis, klasik, her kütüphane 5 sonuç. Sıra kesin değil (kullanıcı, 2026-11-28: cevaplara göre yeniden
       değişebilir; `sohbet.SEARCH_ALL_ORDER`).
    5. (bitti) Meal: iki meal için tek kural (nâşirin meali, Türkiye Diyanet Vakfı meali; birleşmez, alıntı bloğunda
       durmaz), iki sayfada. Sayfada onarım yok (gerekirse sonra).
    6. (bitti) Hizbü'l-Kur'âni'l-Muazzam sohbetin aramalarında ve `find_ayah`'ın yerlerinde yok (kullanıcının kararı;
       `Library.search_excluded`, eser ya da grup verilirse aranır; MCP değişmez; G19 âyeti yine Hizb'den almıştı).
    7. (bitti) K3: model aynı metni Onuncu Söz'ün Zeylinde okuyordu (müellif oraya da koymuş, kelimelerin %97,8'i
       aynı); altın soruda eşdeğer yer `"a | b"`. D15: konum sorusunda başlık ağacı yetiyor, sorun yok.
    8. (bitti) Bilinmeyen rivayet kimliğinde ipucu (model `muslim:4927`'yi hafızadan kurmuştu): kimlik yalnız
       sonuçlardan, künye `hadis_find_by_citation` ile.
    9. (bitti) Ölçüm (tek koşu): genel set doğrulanamayan 0, ortalama 45 → 38 sn, beklenen yerlerden okunan 77 → 70,
       kaynakçada 44 → 33 (düşüş sorulara dağılmış; G7'de aynı hadisin başka kitaptaki yolu okunmuş, set yalnız
       Buhârî ve Müslim'i kabul ediyor), 0,22 $; karışık meal etiketi 1 → 0, bloktaki meal 3 → 0, uyarı 12 → 4.
       Risale seti atıf %95,8 → %97,4, beklenen bölüm 28/34, 0,16 $; 3 doğrulanamayan modelin tek kelimelik
       aktarım hatasıydı: işaretli alıntıya da yakın karşılık onarımı eklendi (≥0,8, sözün metinde geçen kelimeleri
       kalır; o üçü ve bugünkü cevaplardaki iki tane daha metnin sözleriyle). Yayın `deploy.sh --code`.
  - S14.7 **Yeni modlar:** S13.18 ile birleşir (kavram, karşılaştırma, hadis kontrolü, siyer olayı), S14.6'dan sonra.
    Konu taramasının öbür kütüphanelere genişlemesi de burada (2.10).
- E9 **Siyer kütüphanesi** (S14'ün parçası; `docs/s14-acilis-plani.md` › E9): E9.1 genel platform için yazılı seçim
  ölçütü, E9.2 eser listesi ve kaynak (kullanıcı onaylar; bugün Mevâhib, eş-Şifâ, Delâil var; İbn Hişâm, İbn Sa'd
  aday), E9.3 `klasik` koleksiyonuna ayrıştırma (ayrı eklenti yok), E9.4 siyer modu. S14.6'dan sonra.
- E10 **Fıkıh kütüphanesi** (en son; `docs/s14-acilis-plani.md` › E10): E10.1 sınır belgesi (kitapların dediği
  mezhebiyle, hüküm yok, kişiye özel soruda ehline yönlendirme; K5), E10.2 dört mezhebin dengeli eser listesi,
  E10.3 fetva tuzaklı ölçü seti, E10.4 ayrıştırma; ayrı eklenti ileride.
- S13.22 **Göçün tamamlanması** (eski S13.15.7; kullanıcının kararı, 2026-11-27: S13.15'ten ayrı adım): eklentilerin
  tanıtımı ve kurulumu `connect.ayinedar.org`'a; risalemcp.com'un kalan sayfaları (eklenti sayfaları, kurulum,
  belgeler, hata bildirin, gizlilik ve şartlar, İngilizceleri) oraya 308 ile. Dizin başvuruları sonuçlandıktan sonra:
  başvurularda adı geçen gizlilik ve kurulum sayfaları o zamana kadar yerinde. Dokunulmayanlar: eklentilerin MCP
  adresleri (`mcp.`, `hadis.`, `tefsir.`, `klasik.risalemcp.com`) ve risalemcp.com kökünün favicon'u (Claude eklenti
  simgesini oradan alır; kök yönlense de favicon sunulur).
  S14.1 K4 (2026-11-28): aynı gönderimde dizinlerdeki yayıncı adı ("Nur Hadimleri") ve dört kütüphaneli Claude
  eklentisinin genel adı ("Risale-i Nur Library") "Âyinedâr" olur.
- S13.18 **Öbür kipler** (eski S13 (4) ve S13.12'nin 3.–4. aşaması): ders (Word), beni sına, müzakere, kavram ve terim,
  karşılaştırma; kip kaydı tek kaynak (`kipler.py`; MCP hazır komutları ve eklentinin skill'leri ondan); sonra
  yönlendirici (önce öneri, sonra otomatik kip). S14.7 ile birleşir (2026-11-28): S14'ün modları da buradan,
  yönlendirici S14.4'ün B seçeneğine bağlı.
- S13.19 **Okuma ve paylaşma** (eski S13 (5), (6), (7), (9)): alıntıda kelimeye dokununca lügat (okuma platformunun
  `lugatWords`'ü); okuma platformuyla bağ ("bu bölüm hakkında sor"); âyet görünümü (Türk hattı, Medine seçilebilir;
  meal ayrı ve etiketli); alıntıyı kişisel deftere kaydetmek, cevabı kalıcı bağlantıyla paylaşmak (tek cevabın
  paylaşımı kendi kaynakçasıyla), "devamını oku", kısa ya da ayrıntılı cevap.
- S13.20 **İngilizce ve Arapça arayüz** (eski S13 (10)).
- S13.21 **Tanıtımdan sonra: gerçek kullanımdan öğrenmek** (eski S13 (3)): 👎 alan ve doğrulanamayan alıntılı cevaplar,
  onayla gelenlerden altın soru ve okuma seti (`okuma_olc`) adayı; `sohbet usage` ve `geri-bildirim` düzenli.
- E7 **Hadis tarafını derinleştirmek** (kullanıcının kararı, 2026-11-22; kullanımda hadis eklentisi Risale'yi geçti,
  2026-11-20–22): (a) hadis – hadis rivayet grupları (Y2.1'in kalanı): aynı hadisin rivayetleri, lafızla (mekanik);
  (c) yalnız Türkçe aktarılan hadisler (HA7, 101 aday cümle, Adım 4): künye varsa künyenin bölgesinde aranır. (b) yeni
  kitaplar "Sonra"da. Ön çalışma ve karar listesi: `docs/e7-on-calisma.md` (2026-11-25). **E7'nin ilk adımı:**
  raporun sonundaki beş kararı kullanıcıya sormak; kullanıcı onları E7'nin başında verecek (2026-11-25).
- B9 **Türk hattının iki kaynağı** (S7'nin açığı, 2026-11-21): Diyanet baskısının Türk hattıyla risaleoku'nun Türk hattı
  arasındaki küçük işaret farkları (ör. durak işaretleri) bakılmadı; kaynak risaleoku. Kısa karşılaştırma, rapor.
- E8 **Külliyatın Arapça tercümesi** (kullanıcının kararları, 2026-11-23; izin `docs/izinler.md`, geçmişi `KAYIT.md`; Sözler'e e-posta şimdilik
  gitmez, taslak `docs/e8-arapca-kulliyat-izin-epostasi.md` durur).
  Kaynak risaleoku'nun "كتب عربية" rafı (`data/raw/risaleoku_app/ar_*`, diskte; Türkçe risaleoku ciltleriyle aynı
  biçim: `#` sayfa işareti, `toc`, `footnotes`), İhsan Kasım es-Sâlihî'nin tercümesi, Sözler Neşriyat (Kahire).
  İşârât ve Mesnevî'nin Arapça asılları, Kızıl İcaz, Ta'likat ve Hutbe zaten sistemde.
  **Kapsam:** الكلمات (≈235 bin kelime), المكتوبات (≈150 bin), اللمعات (≈144 bin), الشعاعات (≈177 bin; 1. ve 8. Şuâ
  yok), الملاحق (≈100 bin; üç Lâhika'dan seçme, başlıklar mütercimin), صيقل الإسلام'ın kalanı (Muhakemat, Divan-ı
  Harb-i Örfî, Sünuhat, Hutuvat-ı Sitte…), سيرة ذاتية (≈150 bin; Tarihçe-i Hayat değil, İhsan Kasım'ın Külliyat'tan
  tarih sırasıyla derlemesi: **mecmua** olur, pasajları öbür Arapça ciltlere eşlenir, `authority: derleme`,
  derleyen İhsan Kasım). **Kimlikler Osmanlıca gibi kendi yapısıyla** (`sozler-arabi/…`; Türkçe kimliklerle paralel
  tutmak sonra ayrıca karar). Öbür diller "Sonra"da.
  Alt adımlar:
  - E8.1 Ayrıştırma (mekanik): her cilt ayrı eser, dil `ar`, `translation: true`, `translator` İhsan Kasım, baskı
    kaydı (`catalog/editions.py`), yeni grup; `catalog/permissions.py`'deki risaleoku kaydına diğer diller.
    Katmanlar: "(المؤلف)" dipnot müellifin hâşiyesi (Sözler'de 268 notun 136'sı), öbürleri mütercimin notu
    (`notes`: hadis kaynakları, açıklamalar); mütercimin başlıkları, takdimler ("ما الملاحق؟", Mustafa Sungur'un
    takdimi, "هذه السيرة الذاتية"), "نبذة عن بعض الأعلام" işaretli katman, müellife mal edilmez. Sayfa numarası
    tutulmaz. Kontrol arayüzünde gözden geçirme.
  - E8.2 Sîret-i Zâtiyye mecmua olarak (`books/mecmua.py`, aynı dil, aynı mütercim: neredeyse kelimesi kelimesine).
  - E8.3 Türkçe asılla **bölüm düzeyinde** eşleme (Onuncu Söz ↔ الكلمة العاشرة; numara ve başlıktan, mekanik; bağ ya
    da `sources` gibi), eşleşmeyen ve yer değiştirenlerin raporu. **Paragraf düzeyi denenir** (çapa: iki metinde
    aynen duran müellifin Arapçası, âyet, hadis, dua; çok dilli vektörler), "olursa olur, olmazsa olmaz"; bir ciltte
    ölçülür.
  - E8.4 Arama: kelime araması hazır; Arapça vektörler (Voyage, maliyet önce ölçülür). **Varsayılan aramaya girmez**
    (Türkçe sonuçlara karışmasın, Osmanlıca gibi); Arapça sorguda, eser ya da dil verilince gelir.
  - E8.5 Talimat ve araçlar (Risale eklentisi; ayrı eklenti yok): Arapça soranda Arapça tercümeden alıntı, mütercim
    anılır, varsa Türkçe aslın adresi; atıf yolu Arapça başlıklarla; kaynakça satırında mütercim, yayınevi ve
    risaleoku (soruda verilen söz). Deploy'da beklenen fark.
  - E8.6 Ölçüm: 20–30 Arapça örnek soru ve birkaç uçtan uca deneme; **Arapça okuyan ehil bir denetçi gerekir**
    (kullanıcı arıyor); bulunana kadar bu adım bekler, öbürleri yürür.
  - Sonra (ayrı iş): sitenin, proje talimatının ve dizin metinlerinin Arapçası.
  Model çağrısı yok (Voyage hariç): Pro'da yürür.
- E6 **Elmalılı'nın Hak Dini Kur'an Dili, asıl metni:** sadeleştirilmemiş, aslına sadık metin (kullanıcının kararı,
  2026-11-12: Diyanet'in baskısı yok). Müellif 1942'de vefat etti, metnin hakkı 2013'te düştü; ama harf çevirisi ve
  dizgisi baskının yayıncısınındır: kaynak seçilirken bakılır. Bir arkadaşın gönderdiği PDF'ler biçimi bozuk, son çare.
  **Karar (kullanıcı, 2026-11-22, bir avukatla görüştükten sonra):** telifi bitmiş eseri internette yayımlayan,
  onu kullanıma açmıştır; amaç ticari değil. Yazım ve imlânın hakkının saklı olduğunu **açıkça belirtmeyen** bir
  yerden alınabilir. Sıra: (1) kaynak adayları aranır (aslına sadık, sadeleştirilmemiş; metin olarak alınabilen;
  telif notu olmayan), kullanıcıya örnekleriyle gösterilir; (2) seçilenden ekleme: tefsir koleksiyonuna, âyet
  birimleriyle, Türkçe cümle bölücüyle; Türkçe anlamsal aramada öne geçmesin diye eser ya da dil seçilmeden
  varsayılan aramaya girmez (`find_ayah` etkilenmez, vefat sırasıyla sonda gelir).
  **E6.1 bitti (2026-11-23):** kaynak adayları bulundu: (A) archive.org'daki Mürşit metni (sadeleştirilmemiş, telif
  notu yok; Arapçası eski yazı tipinin kodlarıyla, çözülmesi gerekir), (B) islamilimleri.com (aynı metin, Arapçası
  silinmiş), (C) Türkiye Yazma Eserler Kurumu'nun tenkitli neşri (en iyi metin; "Her hakkı mahfuzdur": izin
  istendi, "Bekleyen"). Ayrıntı `KAYIT.md` › "Kimlikli işler" › E6.1. **E6.2 ekleme:** Aralık'taki tefsir
  kurulumunda (B3 ile, kullanıcının kararı 2026-11-23); kaynak YEK'in cevabına göre C ya da A.
- D16 **Bakara'nın maliyet raporu ve hesap kararı** (D5'ten kalan; kuyruk durunca, Bakara bitmese de): sûre başına
  maliyet (destekçiye "şu kadar para, şu kadar sûre"; kuyruğun birim kayıtları `data/d1/d5/bakara.json`) ve hesap
  ayrımı kararı (ayrı abonelik ya da API hesabı; hat ikisine de tek ayarla geçebilecek şekilde). "Fikirler" ›
  "Kur'ân'ın geri kalanı"nın ön şartı.
- B12 **Anlamsal dizini sıkıştırmak** (S13.17.1'in yan bulgusu, kullanıcının kararıyla plana girdi, 2026-11-26):
  `semantic.SemanticIndex` her cümle için kimlik demeti, `VectorStore` anahtar listesi ve sözlüğü tutuyor; tefsirde
  552 bin cümlede vektörler 269 MB, bu yapılar ≈650 MB (servis 1,3 GB). Kimlikler ve eserler numpy dizileri (ya da
  veritabanının `seq`'i) olur, anahtar sözlüğü eşlemeden sonra atılır, kurulurken metinler bellekte tutulmaz. Sonuç ve
  sıra değişmez (`search_eval` ve `tool_snapshot` aynı kalmalı). Bütün profillerde (genel ≈230 MB kazanır); MCP
  servisleri, sohbet ve D5'in kendi kopyaları da hafifler.

**Küçük açıklar** (kullanıcının kararı, 2026-11-21: "önerdiğin sıraya başla"; B3 için: "gerçekten bir problem var mı
araştır, varsa düzelt"):
- B3 Tefsirde noktalaması seyrek eserlerin uzun cümleleri (Bursevî ortalama 97 kelime) ve âyet birimlerinin %0,9'unun
  denetimden geçmemesi (`data/interim/tefsir/mvp-denetim.md`, çoğu yanlış alarm): ölçüldü, düzeltilmedi.
  **Araştırıldı (2026-11-21):** (1) **Uzun cümleler gerçek:** 300 kelimeyi aşan cümle Bursevî'de %7,3 (en uzunu
  3.407 kelime, `bursevi/48/10/c001`), Taberî %3,6 (2.002), Âlûsî %2,5, Ebüssuûd %2,3, Râzî %1,0; öbürlerinde yok.
  Sebep kaynakta: Bursevî'nin Shamela metninde hiç nokta yok, Taberî'de yalnız virgül ve iki nokta; bölücü kurala
  uygun çalışıyor. Bedeli: atıf birimi bir sayfa olur, `get_passage` binlerce kelime verir. **Düzeltmenin bedeli:**
  yeniden bölmek bu eserlerin cümle kimliklerini değiştirir ("kimlikler değişmez"); tefsir bağları (âyet birimi
  43 bin, Kur'ân alıntısı 403 bin; `links_tefsir --mvp` ≈77 dk yeniden) ve taslak arşivi (yayın dosyaları,
  kaynak tercümeleri) bu kimlikleri anıyor; D5 kuyruğu sunucuda sürerken tefsir veritabanı değişirse eski ve yeni
  taslaklar farklı kimliklere atıf yapar. **Karar (kullanıcı, 2026-11-21): Aralık'ta, D5 kuyruğu durunca yapılır**
  (2026-12-13'te ya da Bakara daha önce biterse; o zamana kadar tefsir verisine dokunulmaz). Yapılacaklar: (a) uzun
  cümle için ikinci bölme kuralı yalnız noktalaması seyrek eserlerde (eşik ve sınır işaretleri: önce ölçülür;
  kaynakta işaret yoksa Bursevî'de kaynağın satır ya da sayfa sınırı); (b) kayan âyet birimleri (`razi/30/57`,
  `razi/57/5`, `razi/68/23`, `bursevi/38/85`…; listeyi `verify`'ın düzeltilmiş hâli verir: kısa kelimeli âyet ve
  hurûf-u mukattaa yanlış alarmı kalkar); (c) eski kimlikler yenilerine çözülür (takma ad, Rumuzat'taki gibi), kimlik
  değişikliği raporu kullanıcıya; (d) tefsir bağları yeniden (`links_tefsir --mvp`, ≈77 dk), tefsir vektörleri,
  taslak arşivinin tefsir atıflarının yeni kimliklere eşlenmesi (yayın dosyaları değişmez; eşleme tablosu);
  (e) deploy (`scripts/tefsir-sunucu.sh gonder`, beklenen farklar). (2) **Âyet birimleri:** 367
  geçmeyenin çoğu yanlış alarm (âyetin kelimeleri birimde var; hurûf-u mukattaa ve kısa kelimeli âyetlerde ölçünün
  kendisi yanılıyor: `razi/53/4` "إن هو إلا وحي يوحى" birimin başında). Gerçek kayma birkaç düzine: âyetin kendi
  satırı önceki birimin sonunda, şerhi doğru birimde (`razi/30/57`, `razi/57/5`, `razi/68/23`); bir gerçek kaydırma
  `bursevi/38/85` (metni 86'nın). Etkisi küçük; düzeltmek de kimlik değiştirir, (1) ile birlikte konuşulur.


## Bekleyen (başkasının cevabı)

| Kimlik | İş | Kimde | Eski adı |
|---|---|---|---|
| S4.3 | Claude dizini: Risale başvurusu "In review"; dizin ekibine e-posta gitti (2026-11-16). **Sonraki adım (kullanıcının kararı, 2026-11-22):** belgenin verdiği adrese (mcp-review@anthropic.com) listeleme adı, organizasyon ve durumla e-posta; bir hafta cevap yoksa başvuru silinip `risale.risalemcp.com/mcp` adresiyle yeniden gönderilir. Öncesinde dört sunucu dizin ölçütleriyle denetlenir (araçlarda `title` ve salt okunur işareti, hata iletileri, Voyage'ın beyanı). **Denetlendi (2026-11-22):** bulgular ve e-posta taslağı `docs/s4-dizin-basvurulari.md` §2e; düzeltmeler `aa9083d`. **E-posta gitti (2026-11-22);** dört listeleme yeni İngilizce adlarla incelemede (2026-11-23); alan adı Anthropic'te kanıtlandı (DNS TXT, 2026-11-23; "Verified" talep edilmedi: şirket içindir). Cevap yoksa ≈2026-11-30'da yedek yol | Anthropic | M7 |
| E6.1 | Elmalılı: Türkiye Yazma Eserler Kurumu'na izin e-postası gönderildi (2026-11-23; `docs/yek-izin-epostasi.md`): Hak Dini Kur'an Dili neşrinin (haz. Köksal, Kaya) ticari olmayan kullanımının yazılı teyidi ve dijital dosyası. İzin gelirse `docs/izinler.md`'ye, neşir C adayı olur; gelmezse yedek yol A (archive.org Mürşit metni). Birkaç hafta cevap yoksa telefon (0212 514 46 35, dahili 281–282) | Türkiye Yazma Eserler Kurumu | |
| S4.7 | Claude dizini: eklenti (plugin) "Risale-i Nur Library" 1.0.1 gönderildi (2026-11-23; depo `fatihebrarinan/risale-library-plugin` `54ebcd6`, yazar "Nur Hadimleri", auto-publish açık: onaylanınca kendiliğinden yayına girer). Önce güvenlik ve politika taraması, tutulursa hakem. Onaylanınca: sitedeki kurulum sayfalarına eklentiden kurma yolu, Yenilikler yazısı. Ret gelirse gerekçesine göre düzeltme, yeni sürüm (`version` artar) | Anthropic | |
| S4.1 | OpenAI: dört başvuru **kullanıcının doğrulanmış kendi adıyla** ("Fatih Ebrar İnan"; site ve paket aynı adla, yayında; organizasyon adı "Risale MCP"). Risale "Risale-i Nur Library" adıyla yeniden gönderildi (2026-11-23); Hadis, Tefsir, Klasik paketleri, alan adı jetonları ve demo videolarıyla Risale'nin sonucu beklenmeden gönderildi (2026-11-23; hakeme notlar `docs/s4-dizin-basvurulari.md` §6–§7). İnceleme ≈1 ay. Ret gelirse gerekçesine göre düzeltme ve itiraz (e-postayı yanıtlayarak) | OpenAI | M7 |

Kapananlar (2026-11-12): E4 Kızıl İcaz'ın Türkçesi (gerek yok, "Biten"); Diyanet (izin yok, "Biten"); Osmanlıcanın
kaynağı (A2'nin ön şartı değil).

## Sonra (sırası belli değil; sıraya girince kimlik alır)

"Sonra" 2026-11-22'de baştan gözden geçirildi (kullanıcının kararı: her iş tek tek; sıraya girenler "Sıradaki"nde,
fikir olanlar "Fikirler"de, gereği kalmayanlar "Dondurulan"da). Kalanlar:

- **Okuyucu notunun paragrafı değişirse** (S10'un açığı; kullanıcının kararı, 2026-11-23: "aklımızda bulunsun"):
  platformda paragrafın kimliği metninden üretilir (`d1-yayin.py`). Taslağın yeni sürümünde paragrafın metni değişirse
  kimliği de değişir; o paragrafa yazılmış not sayfada hiç görünmez, yalnız Notlarım'da ve Word dosyasında kalır.
  Yeni sürümler seyrek, şimdilik bırakıldı. Çözüm yolu: notun sürümü ve seçicisiyle (`secici`) yeni sürümde en yakın
  paragrafı bulup notu orada "önceki sürüme yazılmıştı" diye göstermek. (Söz paragrafta bulunamazsa not paragrafın
  altında açık durur, "bu sürümde bulunamadı" der: bu yapıldı.)
- **Telefon uygulaması: Android ve iOS** (kullanıcının kararı, 2026-11-25: S13.15'ten sonra, koşullu ve iki basamaklı).
  Ad ve alan adı kesinleşti, PWA (ana ekrana eklenen web uygulaması; mağaza ve ayrı kod yok) S13.15.4'te yapıldı; birkaç hafta
  ölçülür (kaç kişi ekledi). Mağaza uygulaması ancak PWA yetmezse (iOS'ta ekleyemeyenler, bildirim isteği, mağazada
  görünmek): önce Android (aynı sayfa ince kabukla, TWA; Play Store bir kerelik 25 $, alan adı doğrulaması), iOS en
  son ve gerekirse (yıllık 99 $; Apple web sarmalayan uygulamayı "asgari işlev" kuralıyla sık reddeder, kabul için
  bildirim ya da çevrimdışı okuma gibi yerel bir şey gerekir: gerçek geliştirme ve bakım). Mağazadaki ad sonradan zor
  değişir: ad ve alan adı önce kesinleşir.
- **Öbür dillerdeki tercümeler** (kullanıcının kararı, 2026-11-23: E8'in Arapça hattı oturduktan sonra, aynı yoldan):
  risaleoku'nun "Other Languages" rafı izne dahil. Tam ya da büyük takımlar: Almanca (14 kitap), İngilizce (11),
  İspanyolca (33), Rusça (20), Urduca (15), Özbekçe (≈97, iki alfabe), Macarca (15); öbürleri küçük kitaplar
  (Bengalce, Yunanca, Fince, Malayca, Felemenkçe, Lehçe, Portekizce, Türkmence, Uygurca, Çince…). Hangi dilin
  ekleneceği ayrı karar.
- **Kalan klasik eserler** (E5'ten sonra, `docs/eserler/klasik.md` (c)): er-Risâletü'l-Hamîdiyye (Risale'nin havale
  ettiği; OpenITI'de yok, izinli nüsha aranır), el-Mîzânü'l-Kübrâ (havale; OpenITI'de yok), el-Fütûhâtü'l-Mekkiyye
  (havale; 1,8 milyon kelime), Fütûhu'l-Gayb, Mektûbât, Mesnevî ve öbürleri; sıraya girince kimlik alır.
- **E7 (b) Yeni hadis kitapları**, OpenITI'de aynı lisansla: Beyhakî'nin es-Sünenü'l-Kübrâ'sı, İbn Ebî Şeybe ve
  Abdürrezzâk'ın Musannef'leri (nüshalar seçilirken bakılır). E7'nin (a) ve (c)'si "Sıradaki"nde.
- **el-Bahru'l-Muhît** (Ebû Hayyân, `docs/eserler/tefsir.md` (b)): Aralık'taki tek tefsir kurulumunda ("Sıradaki"nin B3, E6 satırı),
  o zaman kimlik alır.

## Dondurulan

Kod, veri ve belgeler yerinde durur; ileride bir heyet çıkarsa altyapı hazır olur.

2026-11-24 (kullanıcının kararı, birkaç kişiyle konuştuktan sonra):
- **A1 Kaynakçada doğrudan bağlantı** (Aşama 20; e-Risale'nin 2026-10-30 görüşmesindeki önerisi): kaynakçadaki her
  satırın yanına, metnin kaynak sitedeki yerine giden bağlantı. **Yoklama (2026-11-24):** erisale'de adres paragrafa
  kadar iner (`/tr/sozler/altinci-soz#180`; sayı ayrıştırıcıdaki `blockIndex`, eser JSON'una yazılmıyor);
  risaleoku'da yalnız sayfaya iner (`#reader/<kitap>?page=<n>`), bu da sayfa bilgisini saklamayı gerektirir
  ("Risale'de sayfa numarası yoktur" ilkesine dokunur), adres de kırılgandır (site Ekim'de baştan değişti, uygulama
  ≈45 MB); Tanzil'in âyet adresi basittir (`tanzil.net/#2:255`). **Dondurma sebepleri:** (1) Günlük kullanan
  okuyucunun kaynakçadaki yere bakmaya ihtiyacı yok; akademik kullanan okuyucunun o eserlere zaten erişimi var.
  (2) Külfeti çok: erisale sayfa ya da paragraf kimliklerini değiştirirse bizim de veriyi ve programı güncellememiz
  gerekir; bizim kimliklerimiz değişmez, onların adresleri değişebilir. (3) Kaynakça uzar: bir adres satırın kendisi
  kadar (≈80 karakter); 17 kaynaklı ciddi bir çalışmada kaynakça iki katına çıkar, model her seferinde bunu yazar,
  cevap yavaşlar. (4) Model adresi kısaltabilir, "düzeltebilir" ya da uydurabilir (ChatGPT satırları kendi yazmaya
  meyilliydi); bozuk bağlantı, hiç olmamasından kötü görünür. Bugün oturmuş olan kaynakça biçimi bozulmasın.
  (5) Tutarsızlık: risaleoku'dan gelen eserler, Ta'likat'ın Türkçesi ve yerel eserler bağlantısız kalırdı.
  e-Risale'nin şartı ("kaynak gösterilsin") bugün zaten yerine geliyor: her kaynakça satırında kaynak adı var.
  Konuşulan ara yol (bağlantılar `cite`'ta ayrı alanda, yalnız kullanıcı isterse) da yapılmadı. Kod değişmedi.

2026-11-22 (kullanıcının kararı; "Sonra"nın gözden geçirilmesi):
- **Konu fihristi** (Aşama 15): anlamsal arama bu işi büyük ölçüde görüyor. Konunun ortak adres olduğu karar yazılı
  kalır (`docs/tefsir-pilot-degerlendirme.md`).
- **Gönderme tablosu** (Aşama 13'ün ertelenen kısmı, ≈1.700 numaralı gönderme): talimatın "metin başka yere
  gönderiyorsa orayı da oku" kuralı ve eski adlar sözlüğü işin çoğunu görüyor.
- **Risale'nin müfessiri adıyla anması** (Y1.7'nin mekanik kısmı): birkaç düzine yer; model sohbette aramayla buluyor.
- **Âyet masasının açıkları** (S5'ten): masa ar-ge içindi, taslak hattının geliştirilmesi bitti.
- **"Notlarımla düzelt"in gerçek okuyucu notuyla denenmesi** (S7'nin açığı): notlar okuyucunun kendi defteri (S10);
  `notlarla` kodu durur.

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

- **Sohbette model kademeleri** (kullanıcının fikri, 2026-11-26; S13.15 (d)): hızlı ve derin iki model, okuyucu
  seçer. Ad işlevsel etiket ("Hızlı", "Derinlemesine"), çalışan model açıkça yazılır; eser ya da bölüm adı
  kullanılmaz. Açılırsa birlikte tartılır: maliyet (Sonnet soru başı Haiku'nun katları), kota (günlük sorunun kaçı
  derin), ölçüm (`sohbet olc` iki modelde).

- **Sohbette ön arama ve model yönlendirme** (eski S13 (1) ve (2), 2026-11-26'da sıradan çıktı): (1) soru gelince
  anlamsal ve kelime araması birlikte, aday bölümler baştan (konu taraması kipinin dosyası bunun bir kısmını yapıyor;
  risk: modelin kendi aramasını daraltır); (2) Haiku okur, Sonnet yazar ya da soruya göre model. Kullanıcının
  kararları: Haiku sürer (S13.11'in durum değerlendirmesi; Sonnet 13 kat pahalı, dar aramayı o da düzeltmedi), Haiku'nun
  okuma sınırı kabul, zorlanmaz (S13.14). Gerekirse yeniden açılır.

- **"Geliştirme için gönder"** (kullanıcının fikri, 2026-11-23; şimdi yapılmaz): okuyucu kendi defterindeki bir notu
  isterse geliştirmeye gönderir, o not ar-ge notu olur (`masa.py` `kapsam`: `defter` → `arge`). Kişisel defter ile
  ar-ge kaydı arasındaki ayrımı pekiştirir.

"Sonra"dan taşınanlar (kullanıcının kararı, 2026-11-22):
- **Kur'ân'ın geri kalanının taslakları** (kullanıcının kararı, 2026-11-20: D5 yalnız Bakara). Ön şartlar: bütün
  Kur'ân'ın bölmesi (D5.0.4, kural b6; kısa sûreler ve ahkâm için kuralın uzatılması), Bakara'nın gerçek maliyeti ve
  kalitesiyle kapsam ve hesap kararı (D16; ayrı hesap ya da API; gerekirse destek). Pro planında yürümez. Fâtiha ve
  Bakara 1–33'te İşârât var; oralarda taslak yalnız okuma platformunun vitrini için (isteğe bağlı).
- **A2 Osmanlıca–Türkçe eşleme** (Aşama 19): kalıcı değeri var, talebi yok; 16 cildin hizalanması büyük iş. e-Risale
  izin verdi, Osmanlıca külliyat elimizde (risaleoku, Envar baskısı, `osmanlica` grubu). Ehil okuyucular isterse açılır.
- **Kur'ân'a kelime düzeyinde adres** (Y1.1): tek kullanım yeri Arapça lügat (âyette kelimeye dokunmak); onunla birlikte.
- **Yerel indirilebilir paket** (Y2.7): talep yok; metnin tamamını dağıtmak izinlerin istisnası olur
  (`docs/izinler.md`). Talep gelirse.
- **Okuma platformunda bütün tefsir birimlerinin tercümesi** (S7'nin açığı): ağır kota ister, Pro'da yürümez.

- **Arapça lügat** (kullanıcının kararı, 2026-11-22: "Fikirler"de kalsın): okuma platformunda âyetteki bir kelimeye
  dokununca kökü ve el-Müfredât'ın o maddesi, Râgıb'ın sözüyle ve kaynağıyla (taslağın kelime mânâsını okuyucu
  lügatçiden denetler). Eklentilere kazancı küçük (Klasik'te el-Müfredât köklere göre bölümlü). Zorluk kök bulmak:
  Kur'ân kelimeleri için hazır sarf verisi var (lisansı bakılır), taslağın Arapça nesrinde zor. Yapılırsa küçük
  başlar: yalnız âyetin kelimeleri, yalnız el-Müfredât; ileride et-Ta'rîfât, Mekāyîs ya da Lisân.
- **Ortak derlemler** (e-Risale, Yeni Asya; "Sonra"dan taşındı, kullanıcının kararı, 2026-11-22): e-Risale kendi MCP
  sunucusunu yazmış, ortak çalışmak istemeyebilir; Yeni Asya'nın ihtiyaçları kullanıcının onlarla konuşmasıyla
  belirlenir. Tasarım aşağıda ("Ortak derlemler").
- **Taslak usulünün hedeflere göre değişmesi ve vecih haritası** (kullanıcının kararı, 2026-11-21: "Fikirler kısmında
  kalsın"; şimdi istekli değil). D5.1'in okumasından: model bulmada ve dizmede güçlü (Risale dersi, nazım nükteleri),
  tartmada zayıf (34'te «kâne» tek müfessirden). Fikir: taslak müfessirlerin ayrıldığı yerde tercih yapmak yerine
  ihtilafı göstersin ("burada ayrılıyorlar …; tercih ehlinindir"); iki gayeye (tenevvü, heyete çekirdek) ve dürüstlüğe
  hizmet eder, vecih haritasına doğal geçiştir. Aşağıdaki çerçeveyle birlikte duruyor (önceden "Sonra"daydı).
  **İstem adayı** (D5.1'in okumasından, kullanıcı kabul etti, 2026-11-21; D5 kapanınca buraya taşındı): "kelime
  mânâsında tek müfessire dayanma": bir kelimenin mânâsını bir müfessirden alırken öbürlerinin o kelimede ne dediğine
  bak, ayrılıyorlarsa söyle. Yeni istem sürümü ve deneme ister (h9 kararı bozulmaz); kapı ve nisbet bunu yakalamaz
  (atfın doğruluğuna bakarlar, tercihin tartılmasına değil). Usul sayfasında sınır olarak yazılı.
  **Vecih haritası ve açık yazım** (kullanıcının fikri, 2026-11-18; kullanıcının kararı: D5'le paralel değil, **D5'ten
  sonra büyük ve kendine has bir iş**; sıraya girince kimlik alır). Kaynak: taslaklar arası fark çok; kullanıcıya göre bu,
  "Kur'ân'ın sonsuz bir derya olduğunu gösterme" gizli hedefini açar. Çerçeve (konuşuldu): taslaklar ham madde, ürün
  lafız lafız **vecih haritası** (N taslağın nükteleri çıkarılır, aynı vecihler birleşir, ayrı olanlar dayanağıyla
  kalır: İşârât, Risale, belâgat, istinbat); haritaya girmeden önce tenevvü ile hata ayrılır (nisbet denetçisi, İşârât'la
  çelişki denetimi); ileride başkalarının kendi API anahtarıyla taslak yazdırabileceği bir arayüz (maliyet yazdırana;
  Voyage ve sunucu yükü bize; kaynak izinlerinin üçüncü kişilere nasıl taşınacağı; her metin "yapay zekâ taslağı" damgalı,
  "tefsir" diye anılmaz). Elde 13 için dört, 9–10 için dokuz taslak var: küçük bir harita denemesi buradan başlayabilir.
  **D5 için tek şart:** taslaklar ve ölçü verileri (istem sürümü, kaynaklar, eşleştirme) silinmeden ve yapısal saklanır.

- **Kendi yapay zekâ modeli ve üyelik (2026-11-09):** model eğitmek ya da ince ayar önerilmedi: kaynağa bağlılık
  ilkesine ters (model metni ezberler, atfı hafızadan verir). Claude API'si ve bu bağdaştırıcılarla kendi sohbet
  uygulaması teknik olarak mümkün; eksikleri hesap (OAuth kodu askıda), ödeme, arayüz, kötüye kullanım sınırı, KVKK,
  API maliyeti (altın soru çalıştırmalarından ölçülebilir: M6'da soru başına ≈0,31 $). Asıl engel izinler: risaleoku
  "kazanç olmaması", OpenITI CC BY-NC-SA, Tanzil'in Diyanet mealleri ticari olmayan kullanım; ücretli üyelik bunlarla
  çatışır, önce her kaynaktan yeni izin gerekir. Öneri: düşünülecekse ücretsiz ve bağış destekli, kaynaklara sorarak.
  **2026-11-25: S12 oldu** (ücretsiz sohbet sayfası, model eğitimi yok; "Biten").

- **E3 Sorularla Risale (öneri, 2026-11-09; 2026-11-22'de "Sonra"dan buraya):** İzin e-postası gönderilmedi. Modelin Risale'yi okurken web'deki kaynaklara (Sorularla Risale) bakması
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

- S13.23 Arayüz ve deneyim (2026-11-27 – 2026-11-28, yayında): doğrulama e-postasının akıbeti ve süresi, sitede küçük
  düzeltmeler, kip menüsü ve kütüphaneler Ayarlar'da, temalar ve ayna figürü, ilk girişte örnek konuşma ve rehber
  (sağ üstteki bildirimle; okuma platformunda da). S13.23.5 (giriş sayfası) S14.5'e katıldı (2026-11-28). Ayrıntı
  `KAYIT.md` › S13.23.x.
- B13 Sohbette tarayıcı kapanınca cevap ve hak kaybı (2026-11-27, yayında): cevap sayfadan bağımsız sürer,
  sayfa yeniden bağlanır, servis kapanırken beklenir, hak yalnız biten cevaptan düşer. Ayrıntı `KAYIT.md` › B13.
- S13.15 Ad, logo ve site düzeni: Âyinedâr (2026-11-26 – 2026-11-27, yayında): ad ve alan adları (`ayinedar.org`,
  marka başvurusu yok), işlevli alt alan adları, logo (kemerli aynada kırmızı kapaklı kitap), sohbet `chat.`, okuma
  platformu `read.`, masa `lab.`, çatı sitesi `ayinedar.org` (S13.15.6: sohbete çağıran ana sayfa, Yenilikler ve
  Çalışmalar çatıda, çatı ve sohbet arama motorlarına açık). Eklentilerin göçü S13.22. Ayrıntı `KAYIT.md` › S13.15.x.
- S13.17 Öbür kütüphaneler sohbette (2026-11-26, yayında; kapandı 2026-11-27, kullanıcının kararı): okuyucu tefsir,
  hadis ve klasik eserleri açar (varsayılan yalnız Risale), araçlar önekli, MCP sunucularına iç anahtarla uzak çağrı,
  alan adlı işaret ve o kütüphanenin `cite`'ıyla denetim, tek Kaynaklar; âyet çalışması kipi (S13.17.3); tur 7 ve 8.
  Ayrıntı `KAYIT.md` › "Kimlikli işler" › S13.17.
- Risale'si az birimlere göz atmak (eski D5.2; 2026-11-27, kullanıcı): dersler ve nazımlar uygundu; kuyruk sürüyor.
- S13.16, B11, B10 Küçük açıklar (2026-11-26, yayında; kullanıcının kararları aynı gün): sohbette dili belli olmayan
  soru Türkçe, lügatta ünlüden sonraki ı/i ("sâika" sevk eden, "sâıka" yıldırım), "…" ile birleşen alıntının tutmayan
  parçası metindeki karşılığıyla değişir ya da atılır, işaretsiz tırnaklı söz aranır (bulunursa kaynak, bulunmazsa
  uyarı); dört eklentide kaynakça satırı kaynak adıyla biter (e-Risale, risaleoku.com, OpenITI); Arapça Mesnevî'nin
  sonundaki muhakkik eki çıktı (65 cümle). Ayrıntı `KAYIT.md` › "Kimlikli işler" › S13.16, B11, B10.
- S13.1–S13.14 Sohbetin ilk geliştirme adımları (2026-11-25 – 2026-11-26, yayında): sol panel ve sunucuda konuşma
  geçmişi, sekmeli ayarlar, karşılama ve durum satırları, konuşmanın tek kaynakçası ve parçalı kaynaklar, Arapça yazı
  tipi; kullanıcının konuşmalarından ve hata ayıklama turlarından (`sohbet dene`, tur 1–6) gelen düzeltmeler; kipler
  (ad dizini, bölüm künyesi, konu taraması, sayım ve bütün yerler eki); okuma hataları araştırması, Türkçe ölçüm seti
  (`okuma_olc`), göndermeler, okunan pay ve kapsam notu (S13.14, kullanıcının kararıyla durduruldu: Haiku'nun okuma
  sınırı kabul). Açık kalanlar S13.15, S13.18–S13.22. Ayrıntı `KAYIT.md` › "Kimlikli işler" › S13.1–S13.14.
- S12 Sohbet sayfası (2026-11-25, yayında): `risalemcp.com/sohbet` (2026-11-27'den beri `chat.ayinedar.org`), Claude API'siyle (Haiku 5.5 medium), yalnız
  Risale; e-posta doğrulamalı hesap (Scaleway), araçlar süreç içinde, Kaynaklar'ı ve alıntı denetimini sunucu yapar
  (tutmayanı taşır ya da "doğrulanamadı" der), solda Kaynaklar (kaynak adıyla, telefonda çekmece), 👍/👎, kota ve
  bütçe (kişi günde 10, servis günde 5 $, ayda 100 $, ntfy), kendi gizlilik ve şartlar sayfaları. Kullanıcı telefonda
  denedi; deneme ayı 2026-11-25 – 2026-12-25 idi, aynı gün 5 kişi ve bir haftaya kısaldı (S13.1'den sonra). Ayrıntı
  `KAYIT.md` › "Kimlikli işler" › S12.
- E5 Kalan klasik eserler ve yeni tanıtım (2026-11-25, yayında): Risale'de adı geçen eserlerin raporu
  (`docs/e5-risalede-anilan-eserler.md`), yedi eser (Şerhu'l-Mevâkıf, Şerhu'l-Makāsıd, et-Telvîh, el-Fıkhu'l-Ekber,
  el-Munkız, el-Mevâhib, İhyâ; Îcî'nin metni ve Irâkî'nin tahrici ayrı katman), `risale_refs` (Risale'nin eseri andığı
  yerler, türüyle), İhyâ künyeli hadislere lafız bağı, tanıtım "Risale'nin havale ettiği ve dayandığı klasikler" (site,
  talimat, eklenti 1.0.2). Dizin metni taslağı başvurular sonuçlanınca. Ayrıntı `KAYIT.md` › "Kimlikli işler" › E5.
- S4.7 Claude eklentisi (2026-11-23, dizine gönderildi): herkese açık depo `fatihebrarinan/risale-library-plugin` (dört bağdaştırıcı, sekiz İngilizce skill, metin yok; kaynak `packaging/claude-plugin/`, üretici `scripts/claude-plugin.py`); Claude Code'da ve claude.ai'de denendi; portalın denetimiyle yazar adı "Nur Hadimleri" oldu, skill açıklamaları tırnaklandı (1.0.1). Cevap "Bekleyen"de. Ayrıntı `KAYIT.md` › "Kimlikli işler" › S4.
- E6.1 Elmalılı'nın kaynak adayları (2026-11-23): üç aday (archive.org Mürşit metni, islamilimleri.com, Yazma Eserler
  Kurumu neşri); Kurum'un şartları araştırıldı (her hakkı saklı), izin e-postası gitti ("Bekleyen"). Ekleme (E6.2)
  Aralık'ta. Ayrıntı `KAYIT.md` › "Kimlikli işler" › E6.1.
- S11 Site yazılarını web'de düzenlemek (2026-11-23, yayında; kullanıcının kararları: yalnız kendisi, Markdown,
  telefona da uysun): masanın Okumalar › Yazı taslakları'ndan düzenleyici (`/taslak/onizleme/duzenle.html#<tür>/<ad>`;
  solda metin, sağda sitedeki görünüşü, telefonda sekmeli), her "Kaydet" bir sürüm (`data/yazilar.db`, ana sunucu);
  `site-uret.py cek` düzeltmeleri depoya alır, `yayinla`, `zamanla` ve zamanlı yayın önce bunu yapar. Ayrıntı
  `KAYIT.md` › "Kimlikli işler" › S11.
- A4 Lügat (2026-11-23, yayında): risaleoku.com'un Türkçe lügatı (≈39 bin madde); Risale eklentisinde `lookup_word`
  (ekleri atarak, tamlamalarla; nâşirin lügatı diye), okuma platformunda kelimeye dokununca anlam ("Lügat" düğmesiyle
  kapanır). Atıf "risaleoku.com lügatı" (kullanıcının kararı: kaynağı sorulmaz). Yenilikler yazısı taslakta. Ayrıntı
  `KAYIT.md` › "Kimlikli işler" › A4.
- S10 Davet altyapısı ve okuma platformu (2026-11-23, yayında): tek kullanımlık davet bağlantısı (7 gün; okuyucu
  parolasını kendisi koyar, unutursa yeni bağlantı), varsayılan kapsam `oku`; okuyucunun kişisel defteri (herkes, yönetici
  de, yalnız kendi notunu görür; düzenler, gerçekten siler; tür seçimi yok; seçilen söz notun başında), Notlarım sayfası
  ve Word dosyası; paragraf altında yalnız "Not ekle"; ilk girişte karşılama; kopyalamada damgalı künye satırı; kaldığı
  yer hesapta; telefonda başlık sığar; gizlilik politikası (Türkçe, İngilizce) yenilendi. S10'dan önceki notlar ar-ge
  kaydı olarak ayrı. (h) lügat A4'te. Ayrıntı `KAYIT.md` › "Kimlikli işler" › S10.
- S4'ün dış adımları (kapandı, 2026-11-23, kullanıcının kararı): Claude'da dört listeleme İngilizce adlarla
  ("Risale-i Nur Library", "Hadith Library", "Tafsir Library", "Classical Islamic Library") incelemede, dizin ekibine
  e-posta gitti, alan adı kanıtlandı; OpenAI'de dört başvuru kullanıcının adıyla gönderildi; E8 için risaleoku'ya
  soru gitti. Cevaplar "Bekleyen"de; S4.7 ayrıca bitti. Ayrıntı `KAYIT.md` › "Kimlikli işler" › S4.
- B4, B7, B8 (2026-11-21, kullanıcının onayıyla; ayrıntı `KAYIT.md` › "Kimlikli işler" › "Küçük açıklar"): B4 mecmua
  eşlemesinde kısa satır uzun paragrafın ortasına bağlanmaz (Nutuk "İttihad-ı millî...", Fihrist ve Tılsımlar'da birer
  satır; kimlik değişikliği kabul edildi), B7 tırnaklı ifade bitişik yazılışıyla da aranır (`"her şey"` 15 → 304,
  `"hiç bir"` 20 → 1.645) ve `NEAR` içinde Arapça kelime artık sorguyu bozmuyor, B8 Delâil'in 1.414 dipnot rakamı
  ayrıştırıcıda metinden ayrıldı (arama ve `cite` düzeldi; kimlik ve sayfa değişmedi).
- B5 Üç âyet dizgi şüphesi (kapandı, 2026-11-21, kullanıcının onayı): 2026-10-30 kararı geçerli: metin değişmez,
  `ayah_check = dizgi_suphesi`, araç modele uyarır (`docs/ayet-duzeltmeleri.md`; öbür baskılarda da aynı).
- B2 Risale talimatında öbür eklentilere gönderme (kapandı, 2026-11-21, kullanıcının onayı): yeterli; talimat tek
  Kaynaklar kuralında öbür eklentileri anıyor, model araçlarını zaten görüyor; ayrı cümle eklenmedi.
- D5 Bakara 34–286 (2026-11-21, kullanıcının kararı: "sistem artık tamamen kuruldu"): üretim hattı (bölme b6, 154
  birim; h9 istemi; kalite kapısı d3; izah; kaynak tercümesi; tek komutla birim), sunucuda kalıcı kuyruk (`d1-kuyruk`,
  haftalık pencere koruması %90, alarmlar, durum sayfası, telefona bildirim), D5.1 (Bakara 34) okundu. Kuyruk
  Bakara'nın sonuna kadar kendi kendine sürüyor; 2026-12-13'te bitmemişse durdurulur ("Şimdi"). Kalanlar
  "Fikirler"de; ayrıntı `KAYIT.md` › "Kimlikli işler" › D5.
- S9 Sitede "Çalışmalar" kısmı (2026-11-21, yayında): uzun, kaynaklı yazılar (`docs/calismalar/`); Yenilikler ve
  Çalışmalar için taslak, girişli önizleme (`/taslak/onizleme/`), `yayinla`, zamanlı yayın (`yayin_tarihi`,
  `site-zamanli.timer`), yalnız site gönderen `deploy.sh --site`, sitenin Naskh yazı tipi. İlk yazı İşârât'ın usulü
  (son sürümüyle herkese açık), Yeniliklerde duyurusu. Ayrıntı `KAYIT.md` › "Kimlikli işler" › S9.
- S8 Sonuç yazısı "Yapay zekâ İşârât'ın mislini yazabilir mi?" (2026-11-21): iç sürüm `docs/s8-sonuc-yazisi.md`
  (ayrıntılı, kayıtlarıyla), site sürümü Çalışmalar'da, kısa (551 kelime), 2026-11-24'te kendiliğinden yayımlanır.
  Ayrıntı `KAYIT.md` › "Kimlikli işler" › S8.
- S7 Okuma platformu ve ar-ge masası (2026-11-21, yayında): yayın dosyası (değişmez sürümler, içerikten paragraf
  kimliği), okuma platformu `/oku/` (Kur'ân paneli, yalnız son taslak, izah, atıfta kaynağın metni, okuyucu notu,
  usul sayfası, davetli `oku` hesabı), ar-ge masası `/taslak/` (giriş, Pano, Okumalar, Birimler; tek kabuk âyet
  masası, bütün âyetler, içindekiler ağacı, kapı ve nisbet katmanları), deneyler defteri, İşârât'ın Arapça–Türkçe
  eşlemesi, kaynak tercümesi, Türk hattı; S7b–S7h kullanıcının okumasından. Açıkları "Sonra"da, ayrıntı `KAYIT.md` ›
  "Kimlikli işler" › S7.
- D15 Saklı birimlerde son ölçüm (2026-11-20): 21–22, 26–27, 28; hat h9 (h10 21–22'den sonra bırakıldı); 23 okunan
  yerde yeterli 8, düzeltmeyle 3, emin değil 6, yetersiz 6; kapalı eleştirmen İşârât'sız görülebileni neredeyse hiç
  kaçırmıyor, nisbet tamamlıyor; D5'in şartı (önceki birim taslaktan) tuttu. Rapor `data/d1/d15-rapor.md`.
- D14 Taslak hattının turları (2026-11-19): h3'ten h10'a yedi tur (Risale dersi, zorunlu ders başlıkları, uzunluk
  hedefi kalktı, konu başına ilk 10 Risale yeri, soru kalıpları ve tarama tablosu); 9–10, 13, 14–15'te kör eleştirmen
  ve kullanıcının okumasıyla. h10 taban; nisbet denetçisi (D14.5b) D5.0'ın kalite kapısı adayı.
- D12 Taslak altyapısının ar-gesi (2026-11-17): düzeltme deneyi, fark okuması, üslûp ve Muhâkemât, D12.5'in Tur 0,
  T1 (okuma–yazım ayrımı taban olmadı) ve D turu (d1 kalır, d2 bırakıldı); kalanı D14'te.
- S6 Âyet masasının ikinci hâli (2026-11-17, kullanıcının kararı).
- D13 Me'haz (2026-11-17): dosya İşârât, Risale-i Nur'un konuya dair yerleri (267 paragraf), Keşşâf ve belâgat;
  tefsirler araçla; istinbat etiketi; kör eleştirmen o3. h3 taban oldu (kör: bütün hafif, me'haz açık; kullanıcı 2'ye
  1, ikisi açık). Rapor `data/d1/provalar/9-10/d13-rapor.md`.
- D11 Üretim hattı (2026-11-17): hat ve pilot (D11.1–D11.2) bugünkü tabanın temeli; D11.3 D12.3'e katıldı; kuyruk,
  D5'te uzunluk hedefi ve izah D5.0'a geçti.
- Aşamalar 1–12, 13 (küçültülmüş), 13.2, 14; veri düzeni (2026-11-02); risaleoku geçişi (2026-10-30).
- Tefsir hazırlığı H0–H6 ve Beyzâvî pilotu T0–T7 (2026-11-04).
- Y0.1, Y0.3, Y0.5, Y0.6, Y1.2 (2026-11-05/07).
- MVP M0–M7 (2026-11-06/07): 13 tefsir, hadis kütüphanesi (Kütüb-i Sitte, Muvatta, 9 kitap, eş-Şifâ, Delâil),
  HA2, hadis ve tefsir bağdaştırıcıları yayında.
- D2 Bakara 11–12, E2'nin eserleriyle (2026-11-13): eserler kapsamayı artırmadı, dayanağı güçlendirdi (Delâil 264 ve
  425 bu âyeti işliyor; 26 klasik dayanağın hiçbiri yanlış değil); rapor `data/d1/provalar/11-12/d2-rapor.md`,
  ayrıntı `KAYIT.md` › "Kimlikli işler"de.
- E2 Belâgat eserleri ve klasik eserler eklentisi (2026-11-13, yayında): 1. dilim beş eser (Delâilü'l-İ'câz,
  Esrârü'l-Belâğa, el-Müfredât, Miftâhu'l-Ulûm, et-Ta'rîfât), "Klasik Eserler" eklentisi (`/klasik`), site sayfası
  ve Yenilikler yazısı; 2. ve 3. dilim E5'te. Ayrıntı `KAYIT.md` › "Kimlikli işler"de.
- E1 Eser listeleri (2026-11-09): `docs/eserler/tefsir.md`, `hadis.md` (yeni; kütüphanedeki 18 kitaptan üretilir), `klasik.md` (yeni) üç bölümlü; `checklist` elle tutulan (b) ve (c)'yi korur, OpenITI indirmelerini görür ("ham veri 0/13" düzeldi). (b) ve (c) `docs/mvp-kitaplar.md`'deki önerilerden ve künye sayılarından dolduruldu; "?" işaretli şartlar E2.1'de sayılacak.
- S1 Yenilikler ve Open Graph (2026-11-09, yayında): `scripts/site-uret.py`, `docs/yenilikler/`, yazım kılavuzu `docs/yenilikler-kilavuzu.md`; bütün Türkçe sitede "eklenti".
- S2 Sitenin yenilenmesi (2026-11-09, yayında): üç eklentiyi anlatan ana sayfa, `risale.html`, "Hata bildirin", İngilizcesi; ayrıntı `KAYIT.md` › "Kimlikli işler"de.
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
  fikrinin ilk hâli. Açıkları "Sonra"da. Ayrıntı `KAYIT.md` › "Kimlikli işler"de.
- D8 Döngü 2, 31–33'te v1 ve v2 (2026-11-14/15): altı taslak, aynı ölçü; v2 ölçülür iyileşme getirmedi (kapsama %51 →
  %49), yalnız Arapça tırnak kuralı tuttu; Z1 ve Z6 altı taslağın hepsinde. Döngü durdu, karşılaştırma (D7) döngüden
  çıktı, asıl iş için yeni hat D11'e. Ayrıntı "Sıradaki › D8"de.
- D9 Yapay zekâ eleştirmeni ve mekanik denetimler (2026-11-13/14): mekanik denetimler (kapsam adayıyla), Opus
  eleştirmeni (176 not), süzgeç örneklemle (10 notun 10'u, 9 başlığın 9'u kalsın); taslakların sistemli zaafı "nasıl
  vardığı"; D8'e 11 genel usul maddesi; rapor `data/d1/provalar/11-12/d9-rapor.md`. Ayrıntı `KAYIT.md` › "Kimlikli işler"de.
- D6 Bilirkişi okuması (2026-11-13/14; bilirkişi kullanıcı): 24 maddenin 20'si doğru, 3'ü emin değilim, 1'i yanlış;
  ölçme düzeninin kör noktası kapsam ve derece (mutlaklaştırma), D9'a kalıcı denetim; rapor
  `data/d1/provalar/11-12/d6-rapor.md`. Ayrıntı `KAYIT.md` › "Kimlikli işler"de.
- D7 Yapay zekâ karşılaştırıcısı (2026-11-13/14): envanter (41 nükte), 6 taslak × iki kör okuyucu (Fable 5.2, Opus
  5.5), rapor `data/d1/provalar/11-12/yz-karsilastirma.md`; D7.7 sınaması âyet masasında: örneklemin 30 satırında
  güven %95, hiç "tutmuyor" yok; dersler (aynen cömert, iki okuyucu kalır) D8'e. Ayrıntı `KAYIT.md` › "Kimlikli işler"de.
- D1 Taslakların yazılması (2026-11-10/12; kapandı 2026-11-13, kullanıcının kararı): İşârât usul özeti (Arapça asla
  dayanan ikinci sürüm, okur sayfası ve PDF), birim çizelgesi, prova düzeni (`scripts/d1-prova.py`, gizleme profili,
  tam ve ince istem), Bakara 11–12'nin üç taslağı, ölçüt çizelgesi; kalanı D6, D7, D8 oldu; ayrıntı `KAYIT.md` › "Kimlikli işler"de.
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
