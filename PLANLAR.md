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

Son verilen kimlikler: E8, S13, A4, D16, B11 (yeni iş bir sonrakini alır).

## Sıradaki

Sıra kullanıcının kararıdır. Sıranın ve "Sıradaki"nin tarihli geçmiş notları `KAYIT.md` › "Sıradaki'nin notları"nda.

**Şimdi** (her adımda güncellenir; kullanıcının kararı, 2026-11-19: oturum devri için; önde tek iş; eski notlar
`KAYIT.md` › "Sıradaki'nin notları"):
- **Son adım (2026-11-25):** **S12 bitti ve yayında** (`https://risalemcp.com/sohbet/`, Haiku 5.5 medium; ayrıntı
  `KAYIT.md` › S12). Kullanıcı telefonda denedi ve onayladı, model Haiku medium kaldı, ntfy'ye abone oldu, gizlilik
  ve şartlar sayfaları yayında. **Deneme kısaldı** (kullanıcının kararı, 2026-11-25): ay yerine **5 kişi, bir hafta**;
  maliyet düşük çıktığı için sürdürme kararı büyük ölçüde verildi, deneme gerçek kullanımın sayılarını (düzeltilen,
  doğrulanamayan, 👎) görmek içindir. Deneyenler iyi bir arayüzle karşılaşsın diye önce **S13.1** (sol panel, sunucuda
  konuşma geçmişi, sağda Kaynaklar, altta ayarlar), sonra 5 kişiyle bir hafta, sonra S13'ün kalanı. **S13.1'in kodu
  yayında** (2026-11-25, commit `6ce4a22`, `yayin-20261125-200319`, araç çıktısında fark yok; testler ve 42 denetimli
  arayüz denemesi geçti, gizlilik sayfaları güncel). Sırada: kullanıcı telefonda bakar, sonra 5 kişilik deneme
  (başlarken `sohbet usage` kaydı); ondan önce **S13.2** (panel genişliği, sekmeli ayarlar: yayında,
  `yayin-20261125-202918`); **S13.3** karşılama, yeni konuşma sayfası, durum satırları: yayında, `yayin-20261125-212720`).
  **S13.4** (2026-11-25): geri bildirim tıklayınca gider, kullanıcının hesabı sınırsız (yayında); bekleyen düzeltmeler
  (c), (h) yapıldı (geçmişe okunanlar, okumadan söz yok); (d)–(g), (i) orada. **S13.5** konuşmanın tek kaynakçası, **S13.6**
  kaynakların parçalara toplanması (yayında). **S13.7** (2026-11-26) tevekkül konuşmasının bulguları: âyet ve hadis satırları metin panelinde, sayfa notunda okunan yerin başlığı, Vakıf ve telif tarihi kuralları. **S13.9** (2026-11-26) hiss-i kable'l-vukû' konuşması: Nokta artık "tercüme" denmiyor, sohbette satır içi kısa alıntı serbest; okuma hataları not edildi. **S13.10** (2026-11-26) tefekkür-tezekkür ve isim önerisi konuşması: bulgular yazıldı (Lemeât/Lem'alar, `kelime*`siz dar arama, parçalı alıntının yanlış parçası, tersine okuma), çözüm kararı bekliyor. **S13.11** (2026-11-26) hata ayıklama turları: `sohbet dene`; tur 1 (Haiku ve Sonnet) ve tur 2 bitti; sunucu düzeltmeleri, dil, takvim ve Lemeât satırları, `search`'ün ipuçları yayında; tur 3 bitti, (a)–(d) ve Mukaddime'nin telif kaydı düzeltmesi yapıldı; Hubâb'ın hutbesi ve tarih notu yayında; tur 4'ün düzeltmesi ve "kesin sözü kesin aktar" satırı yayında; tur 5 ve durum değerlendirmesi bitti, Haiku sürer; **S13.12** kipler: belge, ad dizini, bölüm künyesi ve konu taraması kipi yapıldı ve yayında; sırada aşama 2 (ikinci kütüphane) ya da tarama kipinin denemesi. Kullanıcı şimdi çok soruyor; sonra konuşmalarına birlikte bakılıp hata ayıklanacak. Sonra B11 ve öbürleri.
  Yerel deneme: `uv run --extra sohbet python -m risale_mcp.sohbet serve --dev` → `http://127.0.0.1:8010/sohbet/`
  (kod `data/interim/sohbet/eposta.log`'a; deneme hesabı `deneme@example.com`), arayüz denemesi
  `uv run --no-project --with playwright python scripts/sohbet-arayuz-dene.py`, ölçüm `… sohbet olc [--hizli]`,
  kullanım `… sohbet usage`, geri bildirim `… sohbet geri-bildirim` (sunucuda `.venv/bin/python -m …`). Yalnız sohbetin
  değişikliği `scripts/deploy.sh --sohbet` ile gider (≈10 sn; kayıt alınmaz, sohbet dışı kod değiştiyse durur; 2026-11-26). Telefon
  uygulaması "Sonra"da (S13'ten sonra, koşullu).
- **Kendi kendine sürenler:** D5 kuyruğu sunucuda Bakara'nın sonuna kadar (`scripts/taslak-sunucu.sh durum`,
  `https://risalemcp.com/taslak/d5.html`). Dizin başvuruları (S4.1, S4.3, S4.7) ve Elmalılı izni (E6.1) "Bekleyen"de.
- **Tarihli hatırlatmalar:** (0) **Sohbetin denemesi başladı (2026-11-25), bitişi ≈2026-12-02:** 5 kişi, bir
  hafta. Başlangıç kaydı `data/interim/sohbet/deneme-baslangic-20261125.md` (o gün 3 kişi, 8 soru, 0,056 $, soru başı
  0,007 $, doğrulanamayan 0, 👍 2). Bitince yine `usage` ve `geri-bildirim --days 7` (sunucuda
  `.venv/bin/python -m risale_mcp.sohbet …`), sonra S13'ün sırası yazılır; öbür eklentiler (S13 (11)) o hafta
  yalnız yerelde hazırlanır. (1) **≈2026-11-30:** Anthropic'ten Risale için cevap yoksa S4.3'ün yedek yolu. (2)
  **2026-12-13:** kullanıcı mesaj gönderecek; taslaklar bitmemişse kuyruk durdurulur (`scripts/taslak-sunucu.sh dur`):
  Max 2026-12-14'te biter, Pro'ya geçmeden önce kuyruk durmalı (aynı aboneliği kullanır). (3) **Kuyruk durunca
  (Aralık):** tek tefsir kurulumu ("Sıradaki" 7: B3, E6) ve D16.
- **Kullanıcıdan beklenen:** "Bekleyen"deki cevaplar gelince haber vermek; dizin metinleri başvurular sonuçlanınca
  (`docs/e5-dizin-metni-taslagi.md`); S10'un karşılama sayfası (`/oku/#/~hosgeldin`) ve kopyalama damgası, sonra ilk
  davetler (`scripts/sunucu.sh taslak davet <e-posta>`); lügatın eşleme örnekleri (`data/interim/lugat/olcum.md`);
  "Sıradaki" 3 (Risale'si az birimler); E8.6 için Arapça okuyan bir denetçi.
- Bir birimin durumu: `uv run python scripts/d1-durum.py [birim]`. `data/d1` her adımda commit ve push. Uzun işler
  `scripts/d1-arka.sh baslat <ad> …` ile.

Sıra (kullanıcının kararı, 2026-11-22): dış adımlar önce (cevapları haftalar sürer); davetin ön şartları (S10, A4) Max
bitmeden (2026-12-14); mekanik işler (E5, E7) Pro'da da yürür; tefsir verisine Aralık'ta tek dokunuş.

| Sıra | Kimlik | İş | Eski adı |
|---:|---|---|---|
| 1 | S13.1 | Sohbet: sol panel ve sunucuda konuşma geçmişi, sağda Kaynaklar, altta ayarlar (5 kişilik denemeden önce) | |
| 2 | B11 | Kaynakçada kaynak adı (e-Risale, risaleoku.com…): izinlerin şartı; MCP bağdaştırıcılarında | |
| 3 | B10 | Arapça Mesnevî'nin sonundaki muhakkik eki (müellifin metni gibi duruyor) | |
| 4 | — | Risale'si az birimlere göz atmak (kullanıcının işi; kıssa birimleri yazıldı) | D5.2 |
| 5 | E7 | Hadis: (a) rivayet grupları, (c) yalnız Türkçe aktarılan hadisler | HA7 |
| 6 | B9 | Türk hattının iki kaynağı arasındaki işaret farkları | |
| 7 | E8 | Külliyatın Arapça tercümesi (İhsan Kasım; risaleoku'nun izni, 2026-11-23): ayrıştırma, bölüm eşlemesi, Sîret-i Zâtiyye mecmua, Arapça arama | |
| 8 | B3, E6 | **Aralık'ta, D5 kuyruğu durunca, tek tefsir kurulumu:** B3 (uzun cümleler, kayan âyet birimleri), E6 Elmalılı'nın eklenmesi, el-Bahru'l-Muhît (sıraya girince kimlik alır) | |
| 9 | D16 | Kuyruk durunca: Bakara'nın maliyet raporu ve hesap kararı | |
| 10 | S13 | Sohbet sayfasının asıl geliştirmesi: S12'nin 5 kişilik denemesinden sonra | |

- S13 **Sohbet sayfasının asıl geliştirmesi** (kullanıcının kararı, 2026-11-25): S12'nin deneme ayından sonra, onun
  ölçüleri ve geri bildirimiyle. İlk turda yapılmayan her şey burada: (1) ön arama (soru gelince anlamsal ve kelime
  araması birlikte, aday bölümler baştan; risk: modelin kendi aramasını daraltır), (2) model yönlendirme (Haiku okur,
  Sonnet yazar ya da soruya göre), (3) gerçek kullanımdan öğrenmek (👎 alan ve doğrulanamayan alıntılı cevaplar,
  onayla gelenlerden altın soru adayı), (4) kipler (ders hazırla, beni sına, müzakere, konu taraması), (5) lügat
  (alıntıda kelimeye dokununca; okuma platformunun `lugatWords`'ü), (6) okuma platformuyla bağ ("bu bölüm hakkında
  sor"), (7) âyet görünümü (Türk hattı, Medine seçilebilir; meal ayrı ve etiketli), (8) PWA (ana ekrana eklenebilen
  uygulama; mağaza gerekmez), (9) alıntıyı kişisel deftere kaydetmek, cevabı kalıcı bağlantıyla paylaşmak, "devamını
  oku" ve "aynı konunun geçtiği öbür yerler", kısa ya da ayrıntılı cevap, (10) İngilizce ve Arapça arayüz, (11) öbür
  eklentiler (hadis, tefsir, klasik), (12) ad ve alan adı (eski S12.8): `risalemcp.com/sohbet` geçicidir, ileride
  vurucu bir ad ve kendi alan adı (ör. "ustad.com" gibi); hesaplar alana bağlı değil (taşınınca bir kez yeniden
  giriş), e-posta gönderen ve SPF/DKIM yeni alana göre; ad, sayfanın müellif adına konuştuğu izlenimini vermemeli
  (sayfada açık "yapay zekâ cevabıdır" ibaresi). Sıra denemenin sonucuna göre yazılır.
  **Deneme kısaldı** (kullanıcının kararı, 2026-11-25): ay yerine 5 kişi, bir hafta; başlamadan ve bitince `sohbet usage`
  kaydı (S13'ün değişiklikleri onunla karşılaştırılır). Maliyet uyarısı: model yönlendirme (Sonnet) ve öbür eklentiler
  soru başını birkaç katına çıkarabilir, tavanlar buna göre tartılır.
  - S13.1 **Sol panel ve konuşma geçmişi** (kullanıcının kararı, 2026-11-25: denemeden önce, deneyenler iyi bir
    arayüzle karşılaşsın). Büyük sohbet uygulamalarının düzeni: solda açılıp kapanan panel (geçmiş konuşmalar, "Yeni
    konuşma" düğmesi, en altta profil ve ayarlar), sağda açılıp kapanan Kaynaklar paneli; telefonda ikisi de çekmece.
    **Geçmiş sunucuda** (yol (b); kullanıcının kararı: büyük şirketler de öyle, paylaşım bağlantısı da bunu ister):
    gizlilik ve şartlar sayfaları değişir, konuşma tek tek ve hepsi birden silinir, hesap silinince hepsi gider.
    Konuşma başlığı ilk sorudan kısaltılır (modele yazdırılmaz). Ayarlar bugün az şey taşır (çıkış, hesabı silme,
    gizlilik ve şartlar), S13'ün seçeneklerine (dil, hat, cevap boyu) yer kalır. **Çatı yok** (kullanıcının kararı):
    sade JS, `sohbet.js` modüllere bölünür; asıl altyapı veri biçimidir: konuşma kimliği, turun taşıdıkları (soru,
    cevap, Kaynaklar, düzeltmeler), API; paylaşım bağlantısına (S13 (9)) uygun kurulur. Tanıtım sitesi statik kalır.
    **Kararlar (kullanıcı, 2026-11-25):** (1) saklama varsayılan açık, ayarlarda kapatılabilir (geçici konuşma: yalnız
    tarayıcıda, bugünkü gibi); (2) konuşma kullanıcı silene kadar durur, hesap silinince hepsi gider; (3) ekip
    konuşmaları okumaz, yalnız 👎/👍 ile gönderilenleri (gizlilik sayfası bunu söyler); (4) gizlilik ve şartlar metnini
    Claude hazırlar ve yayımlar, kullanıcının ayrıca görmesi gerekmez; (5) giriş kutusunun altındaki gizlilik ve şartlar
    bağlantıları ayarlara taşınır, altta yalnız "Tefsir ve fetva değildir, müellife mal edilmez." ve günün kalan hakkı
    ("8/10" gibi).
    **Bitti ve yayında (2026-11-25, `6ce4a22`, `yayin-20261125-200319`).** Sunucu: `conversations`, `turns`, `users.keep_history`;
    `sohbet.Conversations`; yollar `api/durum`, `api/ayarlar`, `api/konusmalar`, `api/konusma`, `api/konusma/ad`,
    `api/konusma/sil`; saklanan konuşmanın geçmişi sunucudan (tarayıcınınki yok sayılır), konuşma ilk cevap bitince
    açılır, başkasının kimliği 404; oy saklanan tura da yazılır. Sayfa: sol panel (Bugün, Dün, Son 7 gün… gruplar; ad
    değiştirme ve silme satırın üstünde, silme iki adımlı), sağda Kaynaklar (1200 pikselden geniş ekranda yerinde,
    daha darda çekmece; 960'tan darda sol panel de çekmece), panel tercihi tarayıcıda, ayarlar `<dialog>`. `sohbet.js`
    tek dosya kaldı (bölmek önbellek sürümlemesini değiştirirdi; büyüyünce). Gizlilik sayfaları (tr, en) güncel.
    `olc --hizli` çalıştırılmadı: cevap yolu değişmedi (geçmiş aynı metin, yalnız yeri sunucu).
  - S13.2 **Panel genişliği ve sekmeli ayarlar** (kullanıcının isteği, 2026-11-25; S13.1'i telefonda denedi, uygun
    buldu): (1) sol ve sağ panelin genişliği aradaki çizgiyi sürükleyerek ayarlanır (geniş ekranda; tercih tarayıcıda,
    klavyeyle de, çift tıklayınca eski genişlik); (2) ayarlar sekmelere ayrılır: Hesap, Konuşmalar, Görünüm (tema: sistem,
    açık, koyu; cevapların yazı boyutu), Belgeler; ileride öbür eklentiler gelince "Eklentiler" sekmesi (açıp kapama).
    **Bitti ve yayında (2026-11-25, `7098841`, `yayin-20261125-202918`).** Sürükleme çizgileri yalnız panel yerinde ve açıkken (sol 200–440,
    Kaynaklar 280–720 piksel; sohbet en az 420 piksel kalır); odaklanınca ok tuşları (Shift ile büyük adım), Home/End,
    Enter ya da çift tıklama eski genişlik; Görünüm'de "Panel genişliklerini sıfırla" (telefonda gizli). Tema
    `html[data-tema]`, yazı boyutu `html[data-boyut]` (dört boy; cevap, soru ve metin paneli). Sekmeler ok tuşlarıyla
    gezilir, telefonda üstte. Arayüz denemesi 55 denetim, hepsi geçti.
  - S13.3 **Karşılama, yeni konuşma sayfası, durum satırları** (kullanıcının isteği, 2026-11-25): (1) girişsiz
    `/sohbet/` hesap oluşturma sayfasını açar (tanıtımlı, süslü: platformu tanıtan başlık, arka planda desen), altta
    "Zaten hesabınız var mı? Giriş yapın"; (2) yeni konuşma sayfası daha şık, örnek sorular küçük ve sayfanın farklı
    yeteneklerini gösterir; (3) cevap beklenirken "Düşünüyor" yerine ne yapıldığı ("Yirmi Dokuzuncu Söz okunuyor",
    "Kaynaklar hazırlanıyor"). Ad (S13 (12)) konuşuluyor: kullanıcının adayı "Fidanlık".
    **Bitti ve yayında (2026-11-25, `2511de5`, `yayin-20261125-212720`).** (1) Girişsiz `/sohbet/` → `kayit`; kayıt ve giriş sayfaları tanıtımlı
    (`sohbet_hesap.HERO`, `SHELL_STYLE`): solda yeşil zemin, yavaş kayan sekiz köşeli yıldız deseni (satır içi SVG),
    başlık, üç özellik, veritabanıyla doğrulanmış bir örnek alıntı (Lem'alar › Yirmialtıncı Lem'a › Üçüncü Ricâ); telefonda
    kısa tanıtım üstte, form ilk ekranda. (2) Yeni konuşma: ortada başlık, sekiz yetenekten (konu taraması, bugünün
    diliyle, bir bölümü anlamak, temsiller, âyetler, kelimeler, hadisler, meseleler) rastgele altı küçük kart, türüyle;
    "Başka örnekler". (3) Durum: "Sözler › Yirmidokuzuncu Söz okunuyor" gibi satırlar (`status_line`), araç adımları
    beklerken dizilir; model beklenirken "Soru inceleniyor…" / "Okunanlar değerlendiriliyor…", sonda "Alıntılar
    eserlerle denetleniyor, Kaynaklar hazırlanıyor…"; adımlar cevabın üstünde açılır özet ("5 adımda hazırlandı · 3 yer
    okundu"), saklanan turda da (`turns.steps`). Gizlilik sayfaları buna göre.
  - S13.4 **Denemenin ilk bulguları** (2026-11-25; kayıtlar ve kullanıcının paylaştığı iki 👍 cevaptan; öbür
    kişilerin konuşmaları okunmadı). Öbür eklentiler (S13 (11)) şimdilik bekler (kullanıcının kararı).
    (a) **Geri bildirim kolaylaştı (kullanıcının isteği; yapıldı):** emoji yerine çizgi simge (seçilince yeşil), oy
    tıklanınca gider, not yazmayı bırakınca (1,5 sn) ya da kutudan çıkınca, onay kutusu değişince gider; Gönder ve
    Vazgeç yok. Sunucu ilk kayıtta numara (`id`) döndürür, sonrakiler aynı satırı günceller (oy değişebilir; kutu
    kalkınca soru ve cevap silinir). Sayfa yenilenince oy görünür, değiştirilemez. Gizlilik sayfaları buna göre.
    (b) **Sınırsız hesap (kullanıcının isteği; yapıldı):** `.env` `SOHBET_SINIRSIZ` (virgülle adresler; koda
    yazılmaz, deploy gönderir): günlük soru sınırı yok, hak satırı görünmez, bütçe tavanları geçerli. Kullanıcı
    çok soracak, sonra konuşmalara birlikte bakılıp hata ayıklanacak. (a) ve (b) yayında (`a765aa5`,
    `yayin-20261125-220248`, araç çıktısında fark yok).
    **Bekleyen düzeltmeler** (henüz yapılmadı; sırası denemenin sonucuyla): (c) **Geçmişte araç sonucu yok:** ikinci
    soruda model "önceki cevabımda … doğrulamadan verdim, okumadan kullandım" dedi; geçmişe yalnız cevap metni
    giriyor (`Chat.messages`), model ilk turun okumalarını görmeyince kendi atıflarını doğrulanmamış sanıyor (atıflar
    sunucuda denetlenmişti). **İkinci örnek düzeltti (2026-11-25, 11. Söz konuşması):** orada ilk cevap Şems
    Sûresi için "Türkiye Diyanet Vakfı meali, metinde verilen çeviriyle aynıdır" dedi ama `get_ayah` hiç
    çağrılmamıştı (yalnız `get_outline` ve `read_section`); ikinci cevaptaki "kontrol etmedim" düzeltmesi yerindeydi.
    **Üçüncü örnek (aynı konuşma, 4. cevap):** "Fatiha 1:5'i yayıncının çevirisi olarak sundum… kontrol etmedim,
    doğrulanmamış sayın" dedi; oysa 3. cevap `read_section sozler/11` ile c103 ve c109'u okumuştu, araç sonucunda âyet
    (`Fâtiha Sûresi, 1:5`, `exact`) ve nâşirin meali vardı: haksız itiraf, okuyucuyu doğru bilgiden şüpheye düşürüyor.
    Üç örnekte ikisi haksız, biri yerinde: model geçmişte araç kaydını görmeden ikisini ayıramıyor.
    Yani sunucu yalnız işaretli alıntıları denetler, işaretsiz söz denetlenmez: "önceki cevaplar denetlendi" demek
    yanlış olur. Çözüm: geçmişe her cevabın altına o turda çağrılan araçların kısa listesi ("okunanlar:
    read_section sozler/11, get_ayah 91:1–10"), talimata "önceki cevaptaki işaretli alıntılar denetlendi; bir sözün
    dayanağını o listeden bil". (h) **Okunmadan söz:** ilk cevaptaki Vakıf meali iddiası, aracını çağırmadan
    verilmiş bir bilgi; talimata "bir meali, âyeti ya da başka bir metni ancak bu cevapta araçla okuduysan anlat"
    (Haiku'da ölçülür). Aynı cevapta "Verse göre" (İngilizce sızıntı, (f) ile birlikte).
    **(c) ve (h) yapıldı (2026-11-25, kullanıcının isteği: "şimdi düzelt"):** her turun çağırdığı araçlar `turns.reads`'e
    (geçici konuşmada tarayıcı `r` ile geri gönderir), sonraki soruda son sorunun önüne sayfa notu ("Answer 1:
    read_section(section=sozler/11, …)"; eski turlar "not recorded"); talimatta yeni kural (`EARLIER`): önceki söz o
    çağrılarla örtülüyorsa "denetlenmedi" denmez, dayanağı yoksa yeni cevabın başında tek cümleyle düzeltilir; meal,
    âyet ya da metin ancak araçla okunduysa anlatılır, Vakıf meali yalnız `get_ayah`'tan. MCP talimatı değişmedi.
    Ölçüm: kullanıcının 11. Söz konuşmasının benzeri, beş soru (≈0,027 $): haksız itiraf yok; 4. cevaptaki tek
    düzeltme yerinde (metni yeniden okuyup "c109'da istiğfar geçmiyor"); Şems karşılaştırmasından önce `get_ayah`
    çağrıldı. `olc --hizli` 57/57 atıf doğrulandı (`20261125-233814-…`). (i) **Yeni bulgu:** meal sorusunda model
    nâşirin mealini `>` blokta işaretle alıntıladı; meal cümlenin metni olmadığı için "doğrulanamadı" çıktı (2).
    Çözüm adayı: işaretli cümlenin Arapça parçasının meali alıntıyla tutuyorsa "nâşirin meali" diye göster.
    (c), (h) yayında (`8928685`, `yayin-20261125-234137`). (d) **Yan yana aynı işaret:** "[23] [23]";
    `check` art arda gelen aynı işareti teke indirsin. (e) **Telif tarihi gereksiz yere metinde:** "kaynak
    1936–1943, Kastamonu'dur (kastamonur.com)", "Hayrat listesi 1933–34 der" (`written` alanından); talimat: tarih
    yalnız soruyla ilgiliyse. (f) **Yabancı harf:** "göktə" (Azerice ə); şimdilik yalnız not, tekrarlarsa cevapta
    Türkçe dışı Latin harf denetimi. (g) **İzlenecek sayı:** işaretsiz paragraf oranı öbür deneyenlerde yüksek (4/9,
    6/8, 9/12; kullanıcıda 2/15, 3/9); yorum paragrafları da sayılır, hafta sonunda bakılır.
  - S13.5 **Konuşmanın tek kaynakçası** (kullanıcının fikri, 2026-11-25): her cevabın ayrı kaynakçası vardı; aynı
    kaynak bir cevapta [3], öbüründe [7] oluyordu. Numaralar konuşma boyunca verilir: kaynak ilk geçtiği yerde
    numarasını alır, sonra hep onunla anılır, yeniler kaldığı yerden sürer. Aynı kaynak: aynı cümle ya da aynı aralık
    (iç içe aralıklar ayrı; doğrulanamayan ayrı). Sağ panel tek liste (her kaynak bir kez, hangi sorularda geçtiği
    yanında); dar ekranda cevabın altında yalnız o cevabın kaynakları, konuşmadaki numaralarıyla. **Yalnız sayfada**
    (kullanıcı onayladı): sunucu her cevabı kendi kaynakçasıyla denetler ve saklar; veri, denetim ve ölçüm değişmez,
    tek cevabın paylaşımı (S13 (9)) kendi kaynakçasıyla kalır. "Soruyu ve bu cevabı da gönder" metni sayfadaki
    numaralarla gider (not "[7] yanlış" derse aynı kaynağa denk gelsin). **Yapıldı (2026-11-25):** `sohbet.js`
    `numberSources` (numara kaynağın nesnesine değil `WeakMap`'e; yerel kayda girmez), sağ panelde kaynak adıyla aynı
    satırda "1. ve 2. soruda"; arayüz denemesine hazır iki turlu konuşmayla 7 denetim (API çağrısı yok), 74 denetim geçti.
    Yayında (`acd790a`, `yayin-20261125-231927`, araç çıktısında fark yok).
    **Hata (2026-11-25, kullanıcı buldu; düzeltildi):** kaynağa tıklayınca "Bu adreste metin bulunamadı": metin uç
    noktası önce atıf dizinine (`checker.nodes`) bakıyordu, dizin ilk alıntı denetiminde kuruluyor; servis yeniden
    başlayıp soru sorulmadan eski konuşmanın kaynağı açılınca hata yutuluyordu (S12'den beri; gece dört deploy
    görünür kıldı). `sohbet.source_text` önce dizini kurar; test yeni servisle sınar (`8481d83`, `yayin-20261125-235352`).
  - S13.6 **Kaynakların toparlanması** (kullanıcının fikri ve onayı, 2026-11-26): 11. Söz'ü işleyen bir konuşmada 40'tan
    çok kaynak birikti; çoğu aynı bölümün yan yana ya da iç içe cümleleri (dokuz emir tek tek alıntılanmış). Kural:
    **kaynak, bir bölümün kesintisiz bir parçasıdır**: aynı bölümde örtüşen ya da bitişik cümleler tek kaynakta
    birleşir, en çok 8 cümle (projenin aralık sınırı), fazlası yeni kaynak. Numara parçanın ilk geçtiği yerde verilir.
    Metindeki [n] tıklanınca parça açılır, o atfın dayandığı cümleler koyu, parçanın öbür cümleleri açık vurgulu. Sağ
    panel bölüm başlıklarıyla gruplu: yol bir kez, altında "[3] “Şu kasrın meliki…” · 3 cümle". Hâşiye cümleleri,
    bölüm atıfları ve doğrulanamayan alıntılar birleşmez. Yalnız sayfada (S13.5 gibi): sunucunun cümle düzeyindeki
    kaydı ve denetimi değişmez. Kullanıcının konuşmasında ilk dört cevapta ≈36 kaynak 17'ye iner (elle hesap).
    **Yapıldı (2026-11-26):** `sohbet.js` `numberSources` parçaları kurar (`pieceOf`), `openText(parça, atıf)` parçanın
    aralığını ister, atfın cümleleri dolgulu, öbürleri altı çizili (`mark.acik`); liste `kaynak-grup` başlıklarıyla,
    kaynak adı tekse listenin altında bir kez. "Soruyu ve bu cevabı da gönder" metni parçalarla. Arayüz denemesi:
    hazır konuşma bitişik, iç içe ve 8'i aşan durumları sınar; 77 denetim geçti. Yayında (`da166fb`, `yayin-20261126-000506`). Kullanıcının 11. Söz konuşması 44 kaynaktan 21'e indi, vurguyu beğendi.
  - S13.7 **Tevekkül konuşmasının bulguları** (2026-11-26; kullanıcının konuşması, üç cevap; kullanıcı hepsini
    onayladı). Bütün işaretli alıntılar doğru, "Diğer yerler" arama sonuçlarıyla tutuyor (iki arama yeniden
    çalıştırıldı). Bulgular: (1) **Kaynakçada Âyet ve Hadis satırları gereksiz** (kullanıcının fikri): sayfada kaynağa
    tıklayınca metin açılıyor, âyetin ve hadisin adresi orada; üstelik alıntısız atıfta cümlenin bütün parçaları
    giriyor (cevapta geçmeyen bir hadis satırı). Ama metin paneli "(doğrulanmadı)" notunu ve meali olmayan parçanın
    adresini göstermiyor. Çözüm: satırlar listeden kalkar, metin panelinde her âyet ve hadisin altında "Âyet: …" /
    "Hadis: … (doğrulanmadı)" satırı (meal varsa yanında), meali olmasa da. Yalnız sayfada; sunucunun verisi ve
    ölçüm metni (`answer_text`) değişmez. (2) **Haksız düzeltme:** 2. cevap "Talâk 65:3'ün mealini okumadan yazdım,
    dikkate almayın" dedi; meal okunan cümleden gelmişti. Kökü 1. cevapta: okunmamış Vakıf meali anılmış ("Vakıf'ın
    değil, yayıncının çevirisidir"). Talimat: nâşirin meali yalnız nâşirinki diye anılır, `get_ayah` çağrılmadıysa
    Vakıf hiç anılmaz. (3) **"O bölümü okumadım":** 1. cevapta okunan Lem'alar › İkinci Lem'a › Beşinci Nükte için;
    sayfa notu yalnız çağrıları ("get_passage(id=…)") veriyor. Çözüm: notta okunan yerlerin Türkçe başlıkları da
    (adımlardaki gibi). (4) **Telif tarihi yine metinde** ((e)'nin ikinci örneği, "kaynak sitesinde 1943–1944"):
    talimat: tarih yalnız soru telif zamanını ya da yerini soruyorsa. (5) **Okuma kalitesi** (talimatla çözülmez,
    not): 3. cevap Onüçüncü Şuâ'nın bu bölümünü "öğrencilere yönelik" sundu, oysa Denizli hapsindeki arkadaşlara
    yazılmış (c002: Risale okuyan hapishanede "talebe-i ulûmun şerefini" kazanır); 1. cevap "terettüb-ü netice"yi
    "sonuç doğduktan sonra" diye açıkladı. Hafta sonunda model yönlendirme konuşulurken örnek olur.
    **Yapıldı (2026-11-26):** (1) `sohbet.arabic_refs`: metin uç noktası her cümleye `refs` ({line, meal}) koyar
    (`Library.embedded`'ın satırı, notuyla); `sohbet.js` listede satır göstermez, metin panelinde gösterir. (3)
    `read_place`: sayfa notunda okuma çağrısının ardına "= read: <başlık>" (not kurulurken bulunur, eski turlarda da).
    (2) Ölçümde kökün başka olduğu çıktı: tek sorulu cevapta da (A1) "Vakıf çevirisi değil, yayıncının çevirisi"
    yazılıyor (25 Kasım ölçümlerinde de var; ortak talimatın "name the translation (Türkiye Diyanet Vakfı)" cümlesi);
    sohbete ayrı kural `VERSES` (6. kural): nâşirin meali alıntı bloğunun dışında, kendi satırında, okuyucunun
    dilinde ("nâşirin meali") anılır; Vakıf yalnız `get_ayah` okunduysa anılır. Aynı kural İngilizce "publisher's
    translation" sızıntısını ve mealin alıntı bloğuna girip "doğrulanamadı" çıkmasını ((i)'nin bir biçimi) da
    azaltır. (4) `SHAPE`: telif tarihi yalnız soru onu soruyorsa. MCP talimatı değişmedi. Ölçüm: tevekkül
    konuşmasının üç sorusu altı kez art arda (≈0,08 $): haksız "okumadım" ya da düzeltme yok (birindeki düzeltme
    yerindeydi: o cevap Lem'alar'ı yalnız aramadan aktarmıştı), telif tarihi yok; `olc --hizli` dört kez, sonuncusu
    79/80 (tek ✗ raporun ayrıştırmasından: başlığında virgül olan bölüm; sayfa doğruladı), Vakıf ve İngilizce
    sızıntı yok. Arayüz denemesi 79 denetim (hadisli hazır tur: listede satır yok, metinde notuyla var). Yayında (`80e28a3`, `deploy.sh --sohbet`).
  - S13.8 **Arapçada kaybolan harf** (kullanıcı buldu, 2026-11-26): "حَسْبُنَا اللّٰهُ وَنِعْمَ الْوَك۪يلُ"de kef
    görünmüyordu. Sebep: sohbetin Arapça yazı tipi yoktu; sistem yazı tipleri Risale'nin kesre işaretini (U+06EA ۪)
    taşımıyor, işaretli harf boş kalıyor (Linux'ta Brave ile yeniden üretildi; system-ui'de kutu). **Yapıldı:**
    sitenin Noto Naskh'ı (`naskh.woff2`, 63 KB) sohbetin kendi dosyalarında (`static/naskh.woff2`, ileride ayrı alan
    adında da çalışsın), `@font-face` yalnız Arapça harf aralıklarında (`unicode-range`), `size-adjust: 125%` (Latin
    harflerin yanında küçük kalıyordu); bütün yazı tipi dizilerinin başında. Test yazı tipinin sunulduğunu sınar,
    arayüz denemesi 79 denetim.
  - S13.9 **Hiss-i kable'l-vukû' konuşmasının bulguları** (2026-11-26; kullanıcının konuşması `jLArMwtzIwbJ9Kl_`, üç
    cevap; okunan bütün yerler veritabanıyla karşılaştırıldı). Bütün işaretli alıntılar doğru, düzeltme yok; hatalar
    okumada, veride ve kuralda. (A) **Nokta "tercüme" diye sunuldu** ("Bu cümle bir Türkçe çeviri metinden alındı",
    "Türkçe çeviri metinde şöyle denir"): Mesnevî-i Nuriye eser düzeyinde `translation=True`, Nokta ise aslı Türkçe;
    bölüm düzeyinde işaret yoktu. (B) **Okuma hataları** (Haiku; talimatla kısmen): (1) sâika ve şâika'yı
    hiss-i kable'l-vukû'dan ayrı hisler saydı, "metin tanımlamıyor" dedi; oysa Mektubat 28 › Beşincisi c004 onları
    hiss-i kable'l-vukû'un iki adı diye veriyor (2. turda okunmuştu), Nokta c003–c004 "hiss-i sâdise-i sâdıka olan
    sâika", "hiss-i sâbia-i bârika olan şâika" diyor; (2) "gayb hakkında kesin bilgi değil, bir tür sezi" dedi, okunan
    Nokta c005–c006 "O şevk ve sevk yalan söylemez. Yanlış gidemez."; (3) Mektubat c015'in "şu nev'i hassâsiyet"ini
    (gelen adamı sezmek) yağmur hassasiyetiyle birleştirdi; (4) Lem'alar 16 c029'un teşbihini ("Nasıl …") yağmurun
    hükmü gibi sundu; (5) "Allah'ın 'sevk-i kaderî' dediği" (terim müellifin); (6) 1. cevabın Yorum'unda dayanaksız
    "hayatı boyunca önemli bir kavram olmuştur"; Nokta'nın "İkincisi"ne "İkinci mesele" dedi. (C) **Satır içi
    alıntı:** 2. ve 3. cevapta tam cümleler düz yazıda tırnakla; ortak kural (`server.QUOTE_EXACTLY`) yalnız tek terime
    izin veriyordu, sayfanın denetleyicisi (`INLINE_QUOTE`) ise bunları denetleyip kabul ediyordu. (D) **Kapsam:**
    "başka hassalar var mı?" sorusunda arama dardı ("beş duyudan başka hassa", "hassâsiyet"); Lem'alar 16'nın
    "Letâif-i Aşere" bölümü (`lemalar/16/letaif-i-asere-ve-mana-yi-ismi`) ve "latîfe-i Rabbâniye" (10 cümle) gelmedi,
    aynı Lem'a'nın başka bölümü okunduğu hâlde. (E) **Yan konuşma** (`XpZEvaWwAxaBcDgW`, "Altıncı ve yedinci his"):
    "altıncı ve yedinci his diye numaralanmış duyu geçmiyor" dedi, Nokta tam bunu diyor; lügat notu "sâika =
    yıldırım" (o صاعقه; buradaki sevk eden سائقه): lügat Latin yazılışı aynı sesteş maddeleri ayırmıyor.
    **Yapıldı (2026-11-26):** (A) `Work.original_sections` (Mesnevî-i Nuriye: `mukaddime`, `nokta`; ikisi de Arapça
    baskıda "aslı Türkçe" diye işaretli), `build_db` düğümün `extra`sına `original` yazar (eserde olmayan kimlik
    kurulumu durdurur), `Library._work_status` o bölümde ve altında `translation` yerine `original_text` verir
    (`read_section`, `get_passage`, `search`, `semantic_search`); katalog notu da söyler. MCP talimatı değişmedi;
    sabit çağrı setinde yalnız `list_works` değişir (notu; deploy'da `DEPLOY_EXPECT="list_works"`, kod ve veri gider:
    `--sohbet` yetmez).
    (C) kullanıcının kararı: sohbette satır içi kısa alıntı serbest; sohbetin kendi kuralı `sohbet.QUOTE_EXACTLY`
    (bir ibare ya da kısa tek cümle, işareti kapanış tırnağının hemen ardında; işaretsizse yine tek terim), MCP'ninki
    aynı kaldı; test satır içi alıntının da asıl yerine taşındığını sınar. Yayında (`70a35bb`, `yayin-20261126-013044`,
    beklenmeyen fark yok; sunucuda Nokta `original_text` veriyor). **Açık:** (B) ve (D) hafta sonunda model
    yönlendirme konuşulurken örnek; Mukaddime'nin kendi telif kaydı yok, eserin kaydını ("Arapça … Metnimiz
    tercümedir") miras alıyor: tarihi kaynaktan bulunmadan yazılmaz; (E)'nin lügat sesteşleri ayrı iş.
  - S13.10 **Tefekkür-tezekkür ve isim önerisi konuşmasının bulguları** (2026-11-26; kullanıcının konuşması
    `0Yp0TRsZt60ZTxf-`, üç cevap: fark, Risale'den platform adı, "genel İslâmî bağlamda" ad; okunan bütün yerler ve
    modelin aramaları genel veritabanında yeniden çalıştırıldı). Bir alıntı dışında işaretli alıntıların sözleri doğru;
    lügat, Ahzâb 33:46 ve nâşirin meali, Hulûsi Bey'in sözünün müellife mal edilmemesi, Ta'likat'ın tercüme diye
    anılması doğru. (A) **Lemeât = Lem'alar sanıldı** (2. cevap, iki kez): Emirdağ Lâhikası 263 c008 "bu Lemeât, …
    bir fidanlık nümûnesidir"; model "Lem'alar için şöyle denir", Yorum'da "Lem'alar'ın bir numune olduğu". (B) **Dar
    arama, yanlış sayı** (1. cevap): "tezekkür iki yerde geçer"; model tam kelimeyi aradı (`tezekkür`, 2 sonuç),
    `tezekkür*` 4 verir: Mesnevî-i Nuriye › Şule › İkinci Kısım c046 "nisyan ve tezekkürde müteâkistirler" (müellifin
    kullanımı, modelin "hatırlama" okumasını destekler), Divan-ı Harb-i Örfî c211 "derdest-i tezekkürdür" (müzakere
    anlamı, istisna). Kur'ân'daki karşılıkları aranmadı: Sözler 22 › Birinci Makam `يَتَذَكَّرُونَ` ile
    `يَتَفَكَّرُونَ` âyetleriyle açılır; Nokta › Üçüncü Bürhan › Birincisi c009 "Kur'ân, kâinâtta tefekküre emir
    verdiği gibi … اَفَلَا يَتَذَكَّرُونَ". (C) **Parçalı alıntının yanlış parçası ekranda kaldı** (1. cevap, [1]):
    Lem'alar 29 › İfâde-i Merâm c001'de "tefekküre teşvik ettiği", metin "tefekkür mesleğine teşvik ettiği"; cümle
    doğru, "…" ile birleşen parçalardan biri tutmuyor, sunucu taşıyacak yer bulamadı, "⚠ doğrulanamadı" gösterdi ama
    yanlış sözler cevapta tırnakta duruyor. Aynı paragrafta işaretsiz tırnak "Bazen bir saat tefekkür, bir sene
    ibadet hükmündedir" metnin sözü değil, denetime girmedi. (D) **Tersine okuma** (3. cevap, [2]): "bunun bir yorum
    olduğu açıkça belirtilir"; Barla Lâhikası 281 c021 "… bu âyetin bu fıkrasından mülhemdir denilebilir ve
    çekinmeyerek deriz" (iddia, çekince değil); adı İmam Ali'nin verdiği ve tevafukun cifrî olduğu ("lafzan ve ma'nen
    ve cifren") söylenmedi; bölüm bir talebenin (Ahmet Nazif Çelebi'nin) istihracı, "metinde" dendi. (E) **Küçükler:**
    kullanıcının "fidanlık" örneğine en uygun yer gelmedi: Mesnevî-i Nuriye › Mukaddime › Dördüncü Nokta c003–c004
    "Demek o fidanlık Mesnevî … Bahçesi olan Risale-i Nur" (müellifin sözü; "fidan OR fidanlık OR bahçe OR çiçek"
    aramasında kısa cümleler önüne geçti); "Nur bahçesi" Hâfız Zühtü'nün mektubundan, "Risale'nin kendi benzetmesi"
    dendi; Kastamonu 119 c009 "Hizmet-i Kur'ân, inşâallâh muhâfaza edecektir" "Risale'nin çalışmasını tarif eder"
    diye sunuldu (yazmaktan korkana "seni korur" diyor); "Sirâcü'n-Nur"un zaten bir mecmuanın adı olduğu söylenmedi;
    Mektubat 29 › İkinci Telvih c001 okunmadan, arama sonucundan alıntılandı (sözleri doğru). **Örüntü:** S13.9'un (B)
    okuma ve (D) kapsam hataları yine (Haiku). **Çözüm adayları (karar yok):** (1) `search` az sonuçta `kelime*`'nin
    sayısını bildirsin (ya da talimat); (2) "…" ile birleşen alıntıda tek parça tutmuyorsa, cümle belli olduğu için
    sunucu o parçayı metindeki karşılığıyla düzeltsin ya da atsın; (3) Lemeât ≠ Lem'alar için talimatta ya da
    `list_works` notunda bir satır; (4) işaretsiz tırnaklı söz denetimi.
  - S13.11 **Hata ayıklama turları** (kullanıcının kararı, 2026-11-26): kullanıcının konuşmalarını incelemek yerine
    konuşmaları Claude Code da kurar, sorar ve inceler. Yerelde, sohbetin kendi koduyla (canlı sohbete gitmez,
    denemenin sayılarına karışmaz): `uv run --extra sohbet python -m risale_mcp.sohbet dene <dosya> [ad …]`
    (`sohbet_dene.py`; soru dosyası `## ad` ve satır başına soru, takip soruları aynı geçmişle; döküm
    `data/interim/sohbet/dene/<zaman>-<model>-<dosya>/`: her turun araç girdisi ve sonucu, modelin ham cevabı,
    okuyucunun gördüğü cevap, Kaynaklar). Soru dosyaları `tests/golden/sohbet_konusmalar/tur-NN.txt` (gerileme seti).
    Kullanıcının kararları: bariz sunucu hataları doğrudan düzeltilir, talimat değişikliği ona getirilir; bir kez
    Sonnet'le karşılaştırılır; tur sayısı sonra.
    **Tur 1** (`tur-01.txt`: 6 konuşma, 14 soru; tefekkür, Lemeât, kimin sözü, sabır, tuzak, hadis). Haiku 0,064 $
    (cevap başı ≈0,005 $, ≈21 sn), Sonnet 0,82 $ (≈0,06 $, ≈17 sn; ≈13 kat). İyi: tuzak sorularında ikisi de
    uydurmadı ("yapay zekâ" yok dedi), hadiste ikisi de hüküm vermedi, Haiku'nun kimin-sözü konuşması doğru (Ahmed
    Nazif Çelebi'nin mektubu, M. Sungur'un notu), sabır taraması iyi. **Haiku'nun hataları:** (1) **dil:** "Lemeât
    nedir…" sorusuna İngilizce cevap; (2) **kimin sözü:** Lemeât'ın Tenbih'i talebelerin (imza Sungur, Mehmed Feyzi,
    Husrev; c004 "Üstadımızın…"), "the author says" dedi (Sonnet doğru); (3) **temsil düz okundu:** Sözler 22 › Birinci
    Makam › Üçüncü ve Dördüncü Bürhan'daki "makine" temsildir (c007'nin hâşiyesi: meyveli ağaç), "o dönemin mekanik
    makineleri üzerine yazılmış" dedi (Sonnet hâşiyeyi okudu, doğru); (4) **nâşirin künyesi müellife:** "Risale …
    kaynak olarak Keşfü'l-Hafâ ve Feyzü'l-Kadîr'i gösteriyor" (Sonnet "nâşirin gösterdiği"); (5) **veri notu metne:**
    Otuz Birinci Lem'a'nın `written` notunu ("Şualar tek tek tarihlidir") "bu Lem'a belirtir" diye sundu; (6)
    **kaçan kaynak:** ümitsizlikte Âsâr-ı Bediiyye › Devâü'l-Ye's'i okudu ama anmadı; (7) "söylenir: [3]" diye
    alıntısız iki nokta. **İkisinin ortak hataları:** (8) **dar arama** (S13.10 (B) yine): "tezekkür iki yerde"
    (`tezekkür*` 4); âyet sonlarını Latin harfle aradılar ("tetefekkerûn", 0 sonuç), Arapçayı (`يتذكرون`) aramadılar,
    anlamsal aramayla kurtardılar; (9) **takvim:** Lemeât hâşiyesi "(Bin üç yüz otuz yedi eder.)", Haiku hicrî sayıp
    "1921 ile uyuşmuyor", Sonnet hicrî sayıp "uyuşur" dedi (hicrî 1337 = 1918–19, rûmî 1337 = 1921; metin takvimi
    söylemiyor). Sonnet'in kendine özgü: Lemeât konuşmasında kendini düzeltirken karıştırdı ("Otuz İkinci Mektub
    okuduğum metinlerde geçmiyor", talimat veriyor; "Otuz Birinci Mektub Mektubat'ın içinde de anılır").
    **Sunucu hataları, düzeltildi** (testli, `tests/test_sohbet.py` `s13_11`): (a) iki cümleye yayılan alıntı ilk
    cümleye işaretlenince taşınamıyordu (dizin cümle başına; ilk cümlenin kelimeleriyle aranır, aralığa taşınır); (b)
    taşınan işaret yanındakiyle aynı yere düşünce "[2] [2]", aralıktakiyle "[1] [2]" kalıyordu (yanındaki işaretin
    aralığında kalan işaret düşer); (c) modelin "nâşirin meali" diye tırnakla verip işaretlediği meal "doğrulanamadı"
    görünüyordu (işaretin cümlelerindeki Arapçanın mealiyse kabul, alıntı sayılmaz); (d) satır ortasına yazılan
    alıntı bloğu ("söyler: > "…" [1] > "…" [2]") okuyucuya ">" olarak görünüyordu (her blok kendi satırına). Yayında
    değil. **Karar bekleyen (talimat ve araç):** (1) cevabın dili (sohbetin talimatı; gerekirse sunucu dil denetimi);
    (2) dar arama: `search` az sonuçta `kelime*`'nin sayısını versin, Latin harfle yazılmış Arapça için Arapça aramayı
    önersin; (3) Lemeât ≠ Lem'alar (S13.10 (3)); (4) takvim: `written` ve metindeki yıl için "hicrî/rûmî belirtilmemişse
    hesap yapma"; (5) Haiku'nun okuma hataları (2)–(5) model yönlendirme konuşmasına örnek.
    **Kullanıcının kararları (2026-11-26):** sunucu düzeltmeleri gönderilir; (1) dil satırı denenir (alıntıları
    çevirmeye kalkarsa geri alınır); (2) arama değişiklikleri uygun, beklenen farkla deploy; (3)–(4) satırlar uygun.
    **Yapıldı:** sohbet talimatına (`SHAPE`) üç satır: cevabın tamamı son sorunun dilinde, alıntı çevrilmez; takvimi
    belirtilmemiş yıl olduğu gibi verilir, çevrilmez ve başka tarihle hesapla karşılaştırılmaz; Lemeât (Otuz İkinci
    Mektub, Otuz İkinci Lem'a) ile Lem'alar ayrı eserdir. MCP talimatı değişmedi. `search` (`Library.search`, bütün
    profiller): 10'dan az sonuçta `word_starts` (`kelime*` ile kaç cümle; "tezekkür" 2, 4), sıfır sonuçta ve sorguda
    Arapça harf yoksa `hint` (Latin harfle yazılmış Arapça bir şey bulmaz, Arapçasını ya da anlamsal aramayı dene);
    `tests/test_search_hints.py`. Düz yazıda tek başına "c013" de kimlik sızıntısı sayılır, silinir. Yayında (`0b608d2`, `yayin-20261126-111734`, `--code`, `DEPLOY_EXPECT="search"`: 1 farklı çağrı, beklenmeyen yok; 29 soruluk ölçüm 196/196 atıf). Tefsir ve klasik sunucularına sonraki gönderimde gider (`search` farkı beklenir).
    **Tur 1'in tekrarı** (yeni talimat ve aramayla, Haiku): bütün cevaplar Türkçe; âyet sonları sorusunda `hint`
    üzerine `لعلكم تتفكرون` ve `لعلكم تذكرون` arandı; "tezekkür" için sayı iddiası yok ama `word_starts` görülüp
    `tezekkür*` yine aranmadı; Lemeât konuşmasında karışıklık yok.
    **Tur 2** (`tur-02.txt`: 7 konuşma, 16 soru; isim (S13.10 gerilemesi), İşârât'ın iki dili, Nûr 24:35, Onuncu Söz
    zinciri, İkinci Söz'ün temsili, İngilizce soru, takvim; Haiku, ≈0,06 $). İyi: isim konuşmasında Lemeât
    karışmadı, Fihrist'in "Risale-i Nur'un bir nev'i çekirdeği ve fidanlığı hükmündeki … Mesnevî-i Nûriye" cümlesi
    bulundu, talebe sözü (Halil İbrahim) ayrıldı; temsil konuşmasında yanlış öncül ("bahçe") düzeltildi; Onuncu Söz
    zinciri dört soruda bağlamı taşıdı; İngilizce soruya İngilizce, Türkçe takibine Türkçe cevap, alıntılar
    çevrilmedi; Vakıf meali `get_ayah`'tan doğru. **Hatalar:** (1) **yersiz geri alma:** takvim 2'de 1. cevabın doğru
    sözünü ("Mukaddime ve Nokta'nın aslı Türkçe", `list_works` notu) "baktığım kayıtlarda yoktu, dikkate almayın"
    diye geri aldı (2. turda `list_works`'ü `osmanlica` süzgeciyle çağırmıştı); (2) **numara:** `lemalar/26`
    "Yirmi Beşinci Lem'a" dendi; (3) **düz yazıda numara:** "Dokuzuncu Hakikat'in 52. cümlesindeki", "(c013 sonrası
    …)" (ikincisi artık sunucuda düşer); (4) **İngilizce kelime:** "Arabic metin" (üç kez, Türkçe cevapta); (5)
    alıntısız numara "Türkçe karşılığı: [4] ve [5]."; (6) "Diyanet meâline göre" (Vakıf'ın meali; Başkanlık mealiyle
    karışır); (7) takvim 2'de "fark yok" (kayıtta tercümenin tarihi yok); (8) İngilizce cevapta kendi tercümesini
    tırnakla işaretledi ("the purpose of the universe", doğrulanamadı); (9) "Haşirle en doğrudan ilgili Dokuzuncu
    Hakikat'tir" dayanaksız. **Karar bekleyen (talimat):** (a) önceki cevabı yalnız şimdi okunan bir sonuç
    çelişiyorsa geri al, yeniden görülmeyen kayıt kanıt değildir (`EARLIER`); (b) Türkçe cevapta İngilizce kelime yok
    ("Arapça", "Türkiye Diyanet Vakfı meali"); (c) bölüm adları ve numaraları araçların `ref`'inden; (d) kendi
    tercümen tırnaklı alıntı değildir, işaretlenmez.
    **(a)–(d) yapıldı** (kullanıcının onayı, 2026-11-26; yalnız sohbet talimatı): (a) `EARLIER`: önceki söz kendi
    başına geri alınmaz; yalnız okuyucu sorarsa, şimdi okunan bir sonuç kendi sözüyle tersini söylerse ya da çağrılarda
    hiç dayanağı yoksa (tur 3'te ilk biçimi ("yalnız şimdi okunan sonuç çelişirse") iki konuşmada çiğnendi, bu
    biçimle aynı iki konuşmada geri alma yok); (b) `SHAPE` dil satırı: Türkçe cevapta İngilizce kelime yok, `get_ayah`'ın
    meali her zaman "Türkiye Diyanet Vakfı meali", "Diyanet meali" değil; (c) bölüm adı ve numarası araçların `ref`'inden
    (`lemalar/26` Yirmialtıncı Lem'a), düz yazıda cümle numarası yok (`NO_REFERENCES`); (d) kendi tercümesi ya da
    özeti tırnaklı, işaretli alıntı değildir (`QUOTE_EXACTLY`). **Veri:** aslı Türkçe bölüm (`original`) üst bölümün
    telif kaydını miras almaz (`Library._written`): Mesnevî-i Nuriye › Mukaddime eserin "Arapça … Metnimiz
    tercümedir" kaydını alıyordu, model `original_text` ile çelişkiye düşüp doğru sözünü geri aldı; artık `written`
    yok (S13.9'un açığı: tarihi kaynaktan bulunmadan yazılmaz).
    **Tur 3** (`tur-03.txt`: 7 konuşma, 14 soru; künye, hâşiye ve şerh, şefkat taraması, Osmanlıca, geri alma,
    İngilizce temsil, Yirmi Altıncı Lem'a; Haiku ≈0,06 $). İyi: "Ben gizli bir hazine idim"in künyesi nâşirin diye
    ayrıldı, hüküm yok; Kızıl İcaz'da Said Nursî'nin hâşiyesi ile Abdülmecid Nursî'nin şerhi ayrı, ikisinin tercümesi
    "Yapay zekâ tercümesi" damgalı; şefkat taraması geniş ve merkez yerleri ayırdı; Osmanlıca nüsha doğru; Yirmi
    Altıncı Lem'a doğru adıyla, Vakıf meali `get_ayah`'tan; İngilizce cevapta alıntılar çevrilmedi. **Hatalar:** (1)
    geri alma iki kez (yukarıda, düzeltildi); (2) "tek hâşiye" (İşârât'ta 15 hâşiye paragrafı; "hâşiye" kelimesiyle
    aradı, yalnız başlık geldi; hâşiyeleri listeleyen araç yok); hâşiyenin içeriği yanlış özetlendi; (3) künye
    konuşmasında hadis "Muhyiddin-i Arabî'nin sözü olarak geçiyor" (metin: Muhyiddin'in o hadisin beyânı); İşârât'ın
    Türkçesinden "Bediüzzaman şöyle yazıyor" (tercüme katmanı anılmadı); (4) Kızıl İcaz'ın Arapça İzâh'ından Türkçe
    söz tırnakla işaretlendi (d), doğrulanamadı (yeniden soruşta yok); (5) "Diyanet meali (Türkiye Diyanet Vakfı)",
    nâşirin meali alıntı bloğunda ve işaretli; (6) "Osmanlıca metin, Latin metnin yazılmış hâlidir" (ters). **Bekleyen
    (karar):** Hubâb › "Meclis-i Meb'ûsân'a Hitâben Yazdığım Bir Hutbenin Sûretidir" metinde "Bu kısım müellifin kendi
    Türkçesidir" diyor, `original_sections`'ta yok (eklemek veri kurulumu ve veri gönderimi ister); Mesnevî-i Nuriye'nin
    `written`'ı Arapça aslın tarihidir, model onu tercümenin tarihi diye okudu ("Türkçe Mesnevî-i Nuriye 1921–1923'te
    yazılmış").
    **Kullanıcının kararları (2026-11-26):** gönder; hutbe eklensin; tarih notu eklensin. **Yapıldı:**
    `original_sections`'a `mesnevi-i-nuriye/hubab/meclis-i-mebusana-hitaben-yazdigim-bir` (artık `original_text`, telif
    kaydı yok: Hubâb'ınki Arapça aslındır); `telif.json` Mesnevî-i Nuriye notu: "tarih Arapça aslının (el-Mesnevî
    el-Arabî), Türkçe tercümenin tarihi değildir". `build mesnevi-i-nuriye` genel ve kişisel veritabanlarını kurdu
    (hadis profilinin kurulumu süre sınırında kesildi, değişiklik onu ilgilendirmiyor, eski `hadis.db` yerinde).
    Yayında (`facc731`, `yayin-20261126-120412`, kod ve veri, beklenmeyen fark yok).
    **Tur 4** (`tur-04.txt`: 7 konuşma, 13 soru; itiraz, fetva, Mevlânâ taraması, mânâ-yı harfî, Risale-i Nur'a işaret
    eden âyetler, Yirmi Üçüncü ve Otuzuncu Söz'ün karşılaştırması, "Dünya âhiretin tarlasıdır"; Haiku ≈0,07 $). İyi:
    okuyucunun yanlış itirazına ("Yirmi Dokuzuncu Söz") boyun eğmedi, Zülfikâr'ın "Onuncu Söz Haşir Risalesi" kaydı ve
    iki Söz'ün alt başlığıyla cevap verdi; fetva sorusunda hüküm yok, Risale'nin ilgili yerine döndü; Mevlânâ taraması
    geniş ve doğru (Mevlevî benzetmesi ayrı, Câmî ve Mevlâna Hâlid ayrıldı); mânâ-yı harfî Lem'alar 16, Sözler 12 ve
    30'dan, âyine temsiliyle; işaret konuşmasında talebe istihracları (Küçük Hüsrev, Hâfız Ali, Nur'un İlk Kapısı'ndaki
    mektup) müellife mal edilmedi; "tarla" hadisini "mezraa" ile buldu, kaynak bulunamadı dedi, hüküm yok. **Hatalar:**
    (1) alıntısız iki nokta ("… belirtilir: [2]", karşılaştırma cevabında altı kez); **düzeltildi** (sunucu:
    ardından blok ya da liste gelmeyen satırın sonundaki iki nokta noktaya döner, `_dangling_colons`, testli; yayında
    değil); (2) **kesin sözü çekince okumak ve müellifi notlamak:** Birinci Şuâ c037 "kanâat-ı kat'iyye verdiğinden
    çekinmeyerek kanâatimi …", model "yazar da bu esnekliği kendisi belirtiyor"; Yorum'da "yazarın dindar bir yorumu",
    "Kur'ân'ı sayı ve harf hesabıyla yeni olaylara bağlamanın tipik bir örneği" (S13.10 (D) ile aynı örüntü); (3)
    sorulmadan telif tarihi ("1936'da Eskişehir Hapsi'nde"); (4) Mesnevî-i Nuriye › Mukaddime › İkinci Nokta c001'in
    öznesi Said ("Mevlâna … gibi akıl ve kalb ittifakıyla gittiği için … Eski Said Yeni Said'e inkılâb etmiş"), model
    Mevlânâ'yı özne yaptı; (5) karşılaştırma cevabında hiç alıntı yok, yalnız özet ve işaret. **Karar bekleyen
    (talimat):** müellif bir sözü kesin söylüyorsa ("kanâat-ı kat'iyye", "çekinmeyerek deriz") kesin diye aktar; Yorum
    açıklar, müellifin iddiasını notlamaz ("tipik örnek", "dindar bir yorum" gibi hüküm yok).
    **Kullanıcının kararları (2026-11-26):** gönder; satır eklensin. **Yapıldı:** `SHAPE`'e "The author's firmness"
    satırı (kesin söz kesin aktarılır; yorum müellifin iddiasını notlamaz); hızlı ölçüm 73/74 (doğrulanamayan,
    Muhakemat'tan sözleri değiştirilmiş bir alıntı, kuralla ilgisiz).
    Yayında (`1b54a50`, `--sohbet`).
    **Tur 5** (`tur-05.txt`: 8 konuşma, 10 soru; yarısı gerileme, yarısı doğal soru; Haiku ≈0,04 $). **Tutanlar:**
    kesin söz (Birinci Şuâ: "kesin bir kanaatte", "kanâat-ı kat'iyye" alıntılandı); Sirâcü'n-Nur (İkinci Şuâ'dan İmam
    Ali'nin Kaside-i Celcelûtiye'si, Ahmet Nazif Çelebi'nin istihracı ayrı, "çekinmeyerek deriz" alıntılandı, Vakıf
    meali tam adıyla); özne (Mukaddime'de Said); tezekkür (`tezekkür*` arandı, 4 yer doğru); kader (Yirmi Altıncı
    Söz, sadeleştirmede temsil doğru); teselli (On Dördüncü Şuâ'nın iki mektubu); ene. **Kalanlar:** (1) Sirâcü'n-Nur
    Yorum'unda "metin bunu bir yorum olarak sunuyor, kesin bir hüküm olarak değil" ("çekinmeyerek deriz"e karşın;
    kesin söz kuralı gövdede tuttu, yorumda tutmadı); (2) ihlâs: Emirdağ'daki "İhlâs Risalesi"ni Lem'alar 20–21'den
    "ayrı bir risale" sandı, "en kısası" sorusuna ihlâsı işlemeyen o mektubu verdi; (3) düz yazıda cümle numarası
    ("(46. cümle)" dört kez) ve "**Yorum**" başlığından önce alıntısız iki nokta; **düzeltildi** (sunucu: parantezli
    cümle numarası silinir; iki noktanın ardındaki satır "**…**" ise liste sayılmaz; testli; yayında değil); (4)
    kader Yorum'unda tırnaklı ve işaretli ama metinde olmayan sözler (doğrulanamadı); (5) sorulmadan telif tarihi
    (teselli). Ardından durum değerlendirmesi (kullanıcının kararı).
    **Durum değerlendirmesi (kullanıcının kararları, 2026-11-26):** Haiku sürer (Sonnet 13 kat pahalı ve dar
    aramayı o da düzeltmedi); kalan hatalar talimatla değil sunucuyla çözülür: kipler (S13.12). Tur 5'in iki sunucu
    düzeltmesi yayında (`ee58394`, `--sohbet`).
  - S13.12 **Kipler ve kapsam** (kullanıcıyla konuşuldu, 2026-11-26; tasarım aşamasında, kod yok). **Fikir:** kapsamı
    (bütün yerleri bulmak) sunucu yapar, model sınırlı bir "dosya" üzerinde okur ve yazar; eksik tarama, kimin sözü ve
    sayım hataları modelden alınır. **İki eksen:** kip (ne yapılıyor) ve kapsam (hangi kütüphaneler: Risale, Kur'ân ve
    tefsir, hadis, klasik; ileride ilgili kaynaklar, tercümeler, başka alanlar). **Kavramlar:** birim (her kütüphanenin
    atıf birimi, sahibi, katmanı, dili, kaynağı aynı biçimde), dosya (adaylar ve neden geldikleri), bağ yürüyüşü (ortak
    adresler ve bağ tabloları üzerinden, modelsiz; ortak âyet ilişki değildir), kip kaydı (tarif: aramalar, sıra, çıktı
    biçimi, denetimler, sona eklenen mekanik listeler), yönlendirici (ileride otomatik kip). **Kataloğ:** konu taraması,
    âyet çalışması, hadis kontrolü, kavram ve terim, karşılaştırma, ders, beni sına, müzakere, serbest soru (varsayılan,
    bugünkü akış). **Kullanıcının kararları:** (1) kip şimdilik yalnız açık seçimle; altyapı otomatik seçime (yönlendirici)
    göre kurulur; (2) konu taramasının sonunda mekanik aday listesi ("Konunun geçtiği öbür yerler", "aday" etiketiyle)
    uygun; (3) ad dizini ve kavram listesi sohbet ederken ortaya çıkar, ayrı onay turu yok; (4) kip kaydı tek kaynak:
    sohbet talimatının kip parçaları, MCP hazır komutları ve eklentinin skill'leri ondan üretilir; (5) çok kütüphaneye
    erişim (süreç içi kopya ya da uzak çağrı) ölçerek, ikinci kütüphane aşamasında kararlaştırılır. **Yalınlık ilkesi**
    (kullanıcının sorusu, 2026-11-26: "fazla karmaşıklaştırıyor muyuz?"): kipler ve dosya yalnız seçilen kipte çalışır;
    serbest soru bugünkü yoldur, yeni kütüphane eklemek onun kapsamını değiştirmez (varsayılan kapsam Risale kalır);
    basit soruya yalnız küçük, ortak araçlar (ad dizini, bölümün imzası, bölüm künyesi) ve gerekirse tek satırlık
    talimat değişikliği dokunur. Her aşama tek başına işe yarar, sonrakini beklemez. **Aşamalar:** (0) tasarım belgesi
    `docs/kipler-plani.md` (kısa); (1) ortak çekirdek yalnız Risale ile: ad dizini, bölümün imzası, `section_profile`,
    birim ve dosya yapısı, kip kaydı, Risale taramasının kapsam ölçümü (modelsiz), sohbette konu taraması kipi; (2) ikinci
    kütüphane: erişim kararı, alan adlı işaret (`[[tefsir:…]]`) ve çok alanlı denetim, âyet çalışması kipi; (3) ders
    (Word), sına, müzakere, kavram, karşılaştırma; (4) yönlendirici (önce öneri, sonra otomatik). Sıra ve başlangıç
    kullanıcının kararını bekliyor.
    **Kullanıcının kararı (2026-11-26):** kısa belge, üç küçük araç ve konu taraması kipi yapılsın. **Yapıldı:** (0)
    `docs/kipler-plani.md`. (1a) Risale adları dizini `books/risale_adlari.json` (29 ad, her biri kanıtıyla: adı o yere
    bağlayan cümle ya da başlığı adı veren düğüm; `tests/test_risale_adlari.py` hepsini sınar); `search` ve
    `semantic_search` sorguda ad geçerse `named_sections` verir. (1b) Bölüm künyesi `Library.profile`: hâşiye ve âyet
    sayısı, imzalar (`signed`, en çok 5); `get_outline` kökünde, `read_section`'ın ilk sayfasında `profile` (ayrı araç
    açılmadı: yalınlık). (1c) Konu taraması: kip kaydı `kipler.py` (serbest, tarama); dosya `dosya.py` (ad dizini,
    başlık araması, kelime başı araması, anlamsal aramanın 300 cümlesi; risale düzeyi: eserin birinci katı, Lâhikalar,
    Tarihçe ve Sikke'de mektup; Fihrist özetleri ve Hizbler aday olmaz; aday başına `why`, `focus`, `closest`,
    `signed`); sohbette `survey` aracı yalnız tarama kipinde, kipin talimatı sayfa notu olarak (sistem talimatı önbellekte
    kalır), cevaptan sonra anılmayan adaylar "Konunun geçtiği öbür yerler (adaylar; okunmadı, sırası hüküm değildir)"
    (en çok 15); arayüzde soru kutusunun üstünde kip seçimi, "Konu taraması" örnek kartı kipi seçer, tur `turns.mode`;
    `sohbet dene` `## ad [kip: tarama]`. **Kapsam ölçümü** (modelsiz, 50 soruluk anlamsal set): dosyanın ilk 5 adayı
    40/50, ilk 10'u 44, ilk 25'i 49; anlamsal aramanın 5 bölümü 32/50. **Tur 6** (`tur-06.txt`, tarama kipiyle 6 konuşma
    ve kipsiz bir karşılaştırma; Haiku ≈0,08 $): ihlâs Lem'alar 20–21 merkezde, öbür yerler listesi Lâhikaların ihlâs
    mektuplarını getirdi; hâşiye sorusunda model künyeden "yaklaşık 15 hâşiye" deyip bulduklarını imzalarıyla ayırdı
    (talebeler, Mütercim Abdülmecîd, M. Sungur), bulamadıklarını söyledi (tur 3'te "tek hâşiye"); kipsiz ihlâs sorusu da
    ad dizini sayesinde "İhlâs Risalesi = Lem'alar 20–21" dedi. Kalan: şefkatte Onuncu Lem'a (Şefkat Tokatları) okunmadı
    (listede var); düz yazıda "44. cümlenin hâşiyesi" (parantezsiz cümle numarası sunucuda düşmüyor). Testler 771, hızlı
    ölçüm 60/60, arayüz denemesi 79/79. **Yayında** (kullanıcı gönderdi, 2026-11-26: `--code`,
    `DEPLOY_EXPECT="get_outline read_section search semantic_search"`, 24 çağrıda beklenen fark, beklenmeyen yok,
    `yayin-20261126-133746`). Tefsir ve klasik sunucularına sonraki gönderimde gider (`profile`, `named_sections`
    farkı beklenir).
- B11 **Kaynakçada kaynak adı** (S12'nin kritiğinden, kullanıcı onayladı, 2026-11-25): e-Risale ve risaleoku izni
  "kaynak gösterilmesi" şartlı; bağdaştırıcıların kaynakçası (`cite_as`, `bibliography`) yalnız yolu verir, kaynağın
  adını vermez (talimat "the bibliography does" diyor). Kaynakça satırına ya da listenin sonuna kaynak adı
  (`works.site`). Araç çıktısı değişir: deploy'da `DEPLOY_EXPECT="cite"`; talimat cümlesi de buna göre.
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
- **Risale'si az birimlere göz atmak** (eski D5.2; isteğe bağlı, bir kez, kullanıcının işi): bir kıssa birimi
  (İsrâiloğulları, 40–74; yazıldı) ve bir ahkâm birimi (178–283; Aralık'a doğru). Sebep: sınanan birimlerin hepsi
  Risale'ce zengindi; Bakara 34–283'te âyetlerin ≈%78'inde Risale'den doğrudan alıntı yok. Okuma değil, göz atmak
  yetebilir (2026-11-21).
- E7 **Hadis tarafını derinleştirmek** (kullanıcının kararı, 2026-11-22; kullanımda hadis eklentisi Risale'yi geçti,
  2026-11-20–22): (a) hadis – hadis rivayet grupları (Y2.1'in kalanı): aynı hadisin rivayetleri, lafızla (mekanik);
  (c) yalnız Türkçe aktarılan hadisler (HA7, 101 aday cümle, Adım 4): künye varsa künyenin bölgesinde aranır. (b) yeni
  kitaplar "Sonra"da. Ön çalışma ve karar listesi: `docs/e7-on-calisma.md` (2026-11-25). **E7'nin ilk adımı:**
  raporun sonundaki beş kararı kullanıcıya sormak; kullanıcı onları E7'nin başında verecek (2026-11-25).
- B10 **Arapça Mesnevî'nin muhakkik eki** (E5 ön çalışmasının yan bulgusu, 2026-11-24): `el-mesnevi-el-arabi/nur/tetimme`'nin
  64–128. cümleleri risaleoku baskısının ekidir (resim etiketleri `img alt=…`, yazma nüshaların resim altları, Ziriklî'nin
  el-A'lâm'ından "نبذة عن بعض الأعلام" biyografi sözlüğü); araçlarda müellifin metni gibi dönüyor. `isaratul-icaz-arabi`'de
  de bir `img alt` satırı var. Düzeltme ayrıştırıcıda (`books/risaleoku_app.py` ya da şablon): ek atılır ya da `notes`'a
  geçer; öbür risaleoku eserlerinde aynı ek var mı bakılır. Kimlik değişikliği (`--accept-id-changes`), sonra deploy.
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
- D16 **Bakara'nın maliyet raporu ve hesap kararı** (D5'ten kalan; kuyruk durunca, Bakara bitmese de): sûre başına
  maliyet (destekçiye "şu kadar para, şu kadar sûre"; kuyruğun birim kayıtları `data/d1/d5/bakara.json`) ve hesap
  ayrımı kararı (ayrı abonelik ya da API hesabı; hat ikisine de tek ayarla geçebilecek şekilde). "Fikirler" ›
  "Kur'ân'ın geri kalanı"nın ön şartı.

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
- **Telefon uygulaması: Android ve iOS** (kullanıcının kararı, 2026-11-25: S13'ten sonra, koşullu ve iki basamaklı).
  Önce S13'te ad ve alan adı, sonra PWA (ana ekrana eklenen web uygulaması; mağaza ve ayrı kod yok); birkaç hafta
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
- **el-Bahru'l-Muhît** (Ebû Hayyân, `docs/eserler/tefsir.md` (b)): Aralık'taki tek tefsir kurulumunda ("Sıradaki" 7),
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
  **2026-11-25: S12 oldu** (ücretsiz sohbet sayfası, model eğitimi yok; "Sıradaki").

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

- S12 Sohbet sayfası (2026-11-25, yayında): `risalemcp.com/sohbet`, Claude API'siyle (Haiku 5.5 medium), yalnız
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
  Bakara'nın sonuna kadar kendi kendine sürüyor; 2026-12-13'te bitmemişse durdurulur ("Şimdi"). Kalanlar "Sonra" ›
  "D5'ten kalanlar" ve "Fikirler"de; ayrıntı `KAYIT.md` › "Kimlikli işler" › D5.
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
