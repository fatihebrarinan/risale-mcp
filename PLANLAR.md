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
- **Son adım (2026-11-25):** S12 sohbet sayfası sürüyor ("Sıradaki" 1). Bitti: S12.0 (API anahtarı), S12.1 (model
  Haiku 5.5), S12.2'nin yerel kısmı (hesaplar, Scaleway), **S12.3 yerel sürüm** (`sohbet.py`; araçlar süreç içinde,
  atıf koddadır; teyit ölçümü: 29 soru, beklenen bölüm 28/34, 21 sn, soru başı 0,0047 $). Kritik yapıldı, kararlar
  alındı (S12.3 altında "Kararlar"). **S12.9, S12.10, S12.11 bitti (2026-11-25):** tutmayan alıntıyı sunucu
  düzeltir; sohbetin kendi talimatı (ortak bloklar `server.py`'de); solda Kaynaklar paneli, kaynak adı, telefonda
  çekmece (ayrıntı her birinde). Kullanıcı 2026-11-25'te "S12'yi bitirene kadar durma" dedi; kararları S12.4, S12.6,
  S12.7, S12.13'te. **Önde, bu sırayla:** S12.12 geri bildirim, S12.13 hızlı ölçüm seti ve modelin yeniden tartılması (üç koşu), S12.4 kota, bütçe ve harcama uyarısı,
  S12.6 gizlilik ve şartlar, deploy (S12.2 ile; Caddy akışı tamponlamaz, `uv sync --extra sohbet`), S12.7 deneme
  ayı (davetsiz; adres bilinmiyor). Deneme ayından sonra S13 (asıl geliştirme). B11 (MCP kaynakçasında kaynak adı)
  sırada 2. Sonra B10, E7 (ilk iş `docs/e7-on-calisma.md` sonundaki beş kararı sormak).
  Yerel deneme: `uv run --extra sohbet python -m risale_mcp.sohbet serve --dev` → `http://127.0.0.1:8010/sohbet/` (kod `data/interim/sohbet/eposta.log`'a düşer; yerelde deneme hesabı
  `deneme@example.com` var). Tek soru `… sohbet sor "<soru>"`, ölçüm `… sohbet olc [soru…]` (hızlı set S12.13'te
  koda girecek). Telefon uygulaması "Sonra"da (S13'ten sonra, koşullu).
- **Kendi kendine sürenler:** D5 kuyruğu sunucuda Bakara'nın sonuna kadar (`scripts/taslak-sunucu.sh durum`,
  `https://risalemcp.com/taslak/d5.html`). Dizin başvuruları (S4.1, S4.3, S4.7) ve Elmalılı izni (E6.1) "Bekleyen"de.
- **Tarihli hatırlatmalar:** (1) **≈2026-11-30:** Anthropic'ten Risale için cevap yoksa S4.3'ün yedek yolu. (2)
  **2026-12-13:** kullanıcı mesaj gönderecek; taslaklar bitmemişse kuyruk durdurulur (`scripts/taslak-sunucu.sh dur`):
  Max 2026-12-14'te biter, Pro'ya geçmeden önce kuyruk durmalı (aynı aboneliği kullanır). (3) **Kuyruk durunca
  (Aralık):** tek tefsir kurulumu ("Sıradaki" 6: B3, E6) ve D16.
- **Kullanıcıdan beklenen:** "Bekleyen"deki cevaplar gelince haber vermek; dizin metinleri başvurular sonuçlanınca
  (`docs/e5-dizin-metni-taslagi.md`); S10'un karşılama sayfası (`/oku/#/~hosgeldin`) ve kopyalama damgası, sonra ilk
  davetler (`scripts/sunucu.sh taslak davet <e-posta>`); lügatın eşleme örnekleri (`data/interim/lugat/olcum.md`);
  "Sıradaki" 2 (Risale'si az birimler); E8.6 için Arapça okuyan bir denetçi.
- Bir birimin durumu: `uv run python scripts/d1-durum.py [birim]`. `data/d1` her adımda commit ve push. Uzun işler
  `scripts/d1-arka.sh baslat <ad> …` ile.

Sıra (kullanıcının kararı, 2026-11-22): dış adımlar önce (cevapları haftalar sürer); davetin ön şartları (S10, A4) Max
bitmeden (2026-12-14); mekanik işler (E5, E7) Pro'da da yürür; tefsir verisine Aralık'ta tek dokunuş.

| Sıra | Kimlik | İş | Eski adı |
|---:|---|---|---|
| 1 | S12 | Sohbet sayfası `risalemcp.com/sohbet`: Claude API'siyle, yalnız Risale, e-posta doğrulamalı hesap, bir aylık deneme (tavan 100 $) | |
| 2 | B11 | Kaynakçada kaynak adı (e-Risale, risaleoku.com…): izinlerin şartı; MCP bağdaştırıcılarında | |
| 3 | B10 | Arapça Mesnevî'nin sonundaki muhakkik eki (müellifin metni gibi duruyor) | |
| 4 | — | Risale'si az birimlere göz atmak (kullanıcının işi; kıssa birimleri yazıldı) | D5.2 |
| 5 | E7 | Hadis: (a) rivayet grupları, (c) yalnız Türkçe aktarılan hadisler | HA7 |
| 6 | B9 | Türk hattının iki kaynağı arasındaki işaret farkları | |
| 7 | E8 | Külliyatın Arapça tercümesi (İhsan Kasım; risaleoku'nun izni, 2026-11-23): ayrıştırma, bölüm eşlemesi, Sîret-i Zâtiyye mecmua, Arapça arama | |
| 8 | B3, E6 | **Aralık'ta, D5 kuyruğu durunca, tek tefsir kurulumu:** B3 (uzun cümleler, kayan âyet birimleri), E6 Elmalılı'nın eklenmesi, el-Bahru'l-Muhît (sıraya girince kimlik alır) | |
| 9 | D16 | Kuyruk durunca: Bakara'nın maliyet raporu ve hesap kararı | |
| 10 | S13 | Sohbet sayfasının asıl geliştirmesi: S12'nin deneme ayından sonra | |

- S12 **Sohbet sayfası** (kullanıcının kararları, 2026-11-25; fikrin geçmişi "Fikirler" › "Kendi yapay zekâ modeli ve
  üyelik"). Geri dönüt: insanlar eklenti kurmak istemiyor, "adres yazayım, sorayım" diyor. Model eğitilmez (kaynağa
  bağlılık); Claude API'si ve Risale'nin araçlarıyla bir sohbet sayfası kurulur. Kararlar: (1) **tavan aylık 100 $**:
  Max planıyla gelen API kredisi; (2) model **önce ölçülür**: Haiku 5.5 – Sonnet 5.5; (3) **hesap şart**, e-posta
  doğrulama koduyla (sınırsız hesap açılmasın); (4) ilk deneme `risalemcp.com/sohbet`, **yalnız Risale**; ücretsiz
  (risaleoku'nun "kazanç olmasın" şartı; bağış ya da üyelik düşünülürse önce kaynaklara sorulur). (5) "Eklentiler ve
  talimatla sınırlı kalmayalım" (kullanıcı): API'nin açtığı fazladan imkânlar konuşuluyor, seçilenler S12.5'e girer.
  - S12.0 **Hazırlık (kullanıcı):** Max'ın API kredisini almak, son kullanma tarihine bakmak; Console'da bu iş için ayrı
    bir çalışma alanı ve anahtar, **aylık harcama tavanı 100 $** (asıl sigorta); anahtar `.env`'de `ANTHROPIC_API_KEY`.
  - S12.1 **Ölçüm: Haiku 5.5 – Sonnet 5.5.** Altın soruların Risale'ye ait olanları iki modelle (`golden run` modele
    seçenek alır; `claude -p` aboneliği kullanır, API kredisi harcanmaz). Ölçüler: doğrulanan atıf, beklenen bölüm
    okundu mu, araç sayısı, süre, eşdeğer maliyet; kullanıcı birkaç cevabı yan yana okur. Sonuç model ve effort
    seçimidir; S12.3'ün kendi düzeninde kısa bir yeniden ölçümle (API'den, gerçek maliyetle) teyit edilir.
    **Ölçüldü (2026-11-25):** 29 Risale sorusu, genel profil, abonelikle; Haiku `20261125-141205-coklu-claude-haiku-5-5`,
    Sonnet `…-sonnet-5-5`, karşılaştırma için Opus (M6, 7 Kasım, üç eklenti). Doğrulanan atıf Haiku 212/215,
    Sonnet 123/123, Opus 167/178; beklenen bölüm okundu 28/34, 19/34, 31/34; süre 29, 22, 41 sn; eşdeğer maliyet
    0,009, 0,088, 0,30 $ (Claude Code'un istemi dahil). Sonnet'in 17 araç hatası Claude Code'a özgü: aracı önekiz
    çağırıyor (`get_outline` yerine `mcp__risale__get_outline`); kendi servisimizde olmaz. Otomatik ölçü kaliteyi
    tartmaz: kullanıcı yan yana okuyor, `https://risalemcp.com/taslak/s12-modeller.html` (girişli;
    `scripts/s12-karsilastir.py`, "adları gizle" kipi, tercihler tarayıcıda ve indirilebilir). **Karar (kullanıcı,
    2026-11-25, ilk beş soruyu okuyarak): Haiku 5.5.** S12.3'te kendi düzenimizde kısa yeniden ölçümle teyit edilir.
  - S12.2 **Hesaplar:** `site_auth.py`'ye kayıt: e-posta → 6 haneli kod (10 dk) → parola; yeni kapsam `sohbet`.
    Adres ve IP başına kayıt ve kod isteme sınırı. E-posta gönderimi için bir gönderim servisi gerekir (site bugün
    e-posta göndermez; Hetzner'den doğrudan SMTP teslim edilmez): **karar kullanıcının**. Öneri (2026-11-25):
    **Scaleway Transactional Email** (Fransa, AB; yalnız işlem e-postası; ayda 300 ücretsiz, sonrası 1.000'i ≈0,25 €;
    HTTP API, `urllib` yeter). Yedekler: Brevo (AB, günde 300 ücretsiz, pazarlama platformu), Resend (ABD, ayda 3.000).
    `risalemcp.com`'un SPF'i Cloudflare'de: `destek@` adresinin kaydı varsa yeni kayıt açılmaz, mevcut SPF'e eklenir;
    DKIM ve DMARC da eklenir.
    **Kod yazıldı (2026-11-25):** `sohbet_hesap.py` (ayrı veritabanı `data/sohbet.db`, çerez `sohbet_oturum`; davetli
    bölümün hesaplarıyla karışmaz: kendi açılan hesap `/taslak/` ve `/oku/`'ya giremez). Tek akış: adres → 6 haneli kod
    (10 dk, 5 deneme) → kod ve parola → hesap açılır ya da parola yenilenir; sayfa hesabın varlığını söylemez.
    Sınırlar: adres başına 60 sn'de bir ve günde 5 kod, IP başına saatte 10 (yalnız bellekte), site günde 200. Hesabı
    kullanıcı kendisi siler. Ayarlar `SOHBET_*` (S12.8). Testler `tests/test_sohbet_hesap.py`; yerelde `--dev` ile
    uçtan uca denendi (e-posta dosyaya). **Scaleway bağlandı (2026-11-25):** kullanıcı hesabı açtı, ücretsiz kota
    (ayda 300) yeter; DNS: kökteki SPF'e `include:_spf.tem.scaleway.com` eklendi, DKIM `<proje>._domainkey`, DMARC
    `p=none`; MX'lere dokunulmadı (`destek@` Cloudflare yönlendirmesi). Alan adı `checked`, ilk gönderim
    `destek@risalemcp.com`'a `250 Ok` (API biçimi `ScalewayMailer`'ınkiyle aynı). `.env`: `SCW_SECRET_KEY`,
    `SCW_PROJECT_ID` (`SCW_ACCESS_ID` da duruyor, gerekmiyor). Deneme e-postası gelen kutusuna düştü, SPF, DKIM ve
    DMARC geçti (kullanıcı baktı). **Kalan:** servis birimi `risale-sohbet` (:8010),
    Caddy `/sohbet/*`, deploy (`.env`'den yalnız `SCW_*` ve `ANTHROPIC_API_KEY` gider); S12.3'ün servisiyle birlikte. Doğrulama sınırsız hesabı zorlaştırır ama
    engellemez: asıl sınır kişi kotası ve bütçe tavanıdır (S12.4).
  - S12.3 **Sohbet servisi:** `risale-sohbet` (ana makine, 127.0.0.1:8010; Caddy `/sohbet/` sayfası ve `/sohbet/api/`,
    girişli). Araçlar **süreç içinde** `library.py`'den çağrılır, MCP üzerinden değil: hesapsızların ortak sınırını
    (dakikada 120, günde 2.000 anlamsal) yemez, bir ağ dolaşması az, araç sonuçları elimizdedir (S12.5 buna dayanır).
    Anthropic Python SDK'sı yalnız bu servisin bağımlılığıdır (sunucuda "sağlayıcı SDK'sı yok" kuralının bilinçli
    istisnası; MCP sunucusu etkilenmez). Talimat `server.py`'nin Risale talimatından ve sohbete özgü eklerden;
    araçlar ve talimat önbellekte (prompt caching). Cevap akışla gelir, araç çağrıları "Sözler okunuyor…" diye
    görünür. Soru başına araç çağrısı ve konuşma başına tur sınırı. Konuşmalar sunucuda saklanmaz (tarayıcıda);
    sunucu yalnız kullanım satırı tutar: kullanıcı, zaman, model, token, maliyet, araç sayısı, atıf denetiminin sonucu.
    **Yerel sürüm yazıldı (2026-11-25):** `sohbet.py` (+ `sohbet_assets/`, testler `tests/test_sohbet.py`). Araçlar
    `create_server(profile="genel")`'den (`list_tools`, `call_tool`; `cite` verilmez), talimat sunucunun talimatından
    üç değişiklikle (değişen yer bulunmazsa servis açılmaz). Model alıntıyı `[[kimlik]]` ile işaretler; sunucu
    `CitationChecker.sources` ile denetler, numaraları ve Kaynaklar'ı kurar; tutmayan alıntı ve düz metne yazılmış
    kimlik ("(c033)") modele bir kez döner, cevap baştan yazılır; yine kalan kimlik silinir, alıntı işaretli görünür.
    Akış SSE; kopan akışta tur bir kez yeniden (okuma zaman aşımı 60 sn: bir bağlantı 6 dk askıda kalmıştı). Kullanım
    satırı `sohbet.db` `usage` (hesap silinince adsız). `anthropic` isteğe bağlı bağımlılık (`--extra sohbet`).
    Servis birimi `docs/risale-sohbet.service` (Caddy yolu deploy'da). **Teyit ölçümü** (`sohbet olc`, 29 Risale
    sorusu, API'den; `data/interim/golden/20261125-153523-sohbet-claude-haiku-5-5/`): beklenen bölüm okundu 28/34
    (S12.1 ile aynı, aynı altı eksik), ortalama 21 sn (S12.1: 29), soru başı **0,0047 $** gerçek fiyat (toplam
    0,14 $), araç hatası 0, düzeltmeye giden 5/29, düzeltmeden sonra kalan sorun 0. "Doğrulanan atıf" artık ölçü
    değil (Kaynaklar'ı veritabanı yazıyor). Üç tuzak sorusunun cevabı elle okunacak (raporda "trap"). **Tarayıcıda baştan sona
    görülmedi** (eklenti koptu; akış `curl` ile, çizici Node ile sınandı).
    **Kritik ve kararlar (kullanıcı, 2026-11-25):** (1) Sohbet sayfasında solda "Kaynaklar" penceresi, kaynak adıyla
    (S12.11; e-Risale ve risaleoku izni "kaynak gösterilmesi" şartlı, `cite_as` yalnız yolu verir). (2) Düzeltmeyi
    sunucu yapar (S12.9). (3) Düz cümledeki iddia (yalnız alıntı denetleniyor; Haiku eser adını karıştırabiliyor:
    "Lemeat" yerine "Lem'alar") zamanla daha çok denetlenir; S12.9'un sayımı yol gösterir. (4) Sohbete MCP'lerinkinden
    ayrı talimat, ortak katman kurallarıyla (S12.10). (5) Geri bildirim ilk sürüme (S12.12). (6) Deneme ayından sonra
    asıl geliştirme S13: S12.5'in (b) ve (c)'si, havuz, S12.8 ve öbür eklentiler oraya taşındı. (7) Model gerçek
    fiyatla yeniden tartılır (S12.13). (8) Davet yok: adres bilinmiyor, bilen hesap açıp kullanır; günlük tavan ve
    harcama uyarısı açılıştan önce hazır (S12.4). (9) Deploy: Caddy `/sohbet/` yolunu tamponlamaz ve sıkıştırmaz,
    sunucuda `uv sync --extra sohbet` (deploy adımında; Caddyfile'a önceden girmez, başka bir deploy yolu erken
    açmasın). (10) Her değişiklikte 29 soru yerine hızlı set (S12.13). (11) MCP kaynakçasında da kaynak adı (B11).
  - S12.9 **Düzeltmeyi sunucu yapar** (kullanıcının kararı, 2026-11-25). Denetleyici sözü başka bir cümlede bulduysa
    kimliği sunucu değiştirir (birden çok yerdeyse modelin okuduğu bölümdeki); düz metne yazılmış kimlik sessizce
    silinir; eserlerde hiç bulunmayan alıntı modele sorulmadan "doğrulanamadı" işaretiyle gösterilir (yol (b)). Model
    turunun (yol (a)) gerekip gerekmediği zamanla, deneme ayının sayılarıyla anlaşılır. Kullanım satırına: sunucunun
    düzelttiği, doğrulanamayan alıntı ve işaretsiz paragraf sayısı (düz cümledeki iddianın sıklığı için).
    **Bitti (2026-11-25):** `sohbet.check` her işareti ayrı denetler: başka yerde bulunan alıntı oraya (kapsayan en kısa
    aralığa) taşınır, sıra okuma araçlarının döndürdüğü cümle (`read_ids`), sonra işaretin bölümü, sonra eseri, sonra
    kitap sırası; alıntısız işaretin aralığı 8 cümleye ya da bölüm sonuna kısalır, kimliği yoksa silinir; eserlerde
    bulunmayan alıntı ayrı numara alır, sayfada ⚠ "doğrulanamadı" (adres yoksa "Adresi bulunamadı"); düz kimlik silinir.
    Geçmişe giden cevap (`raw`) düzeltilmiş kimliklerle. Model turu `SOHBET_MODEL_FIX=1` ile açılır, varsayılan kapalı.
    `usage`'a `fixed`, `dropped`, `leaks`, `paragraphs`, `unmarked` (eski veritabanına sütun eklenir); `sohbet usage`
    bunları özetler, `olc` dökümü modelin düzeltilmemiş metnini de yazar. **Deneme** (geçen ölçümde düzeltmeye giden
    5 soru, `20261125-160727-…`): model turu yok, ortalama 15 sn ve toplam 0,014 $ (aynı sorular düzeltme turuyla 21 sn, 0,023 $);
    B8'de 2 işaret sunucuca taşındı, C13'te 1 doğrulanamayan, 1 silinen işaret. C13'ün doğrulanamayanı yanlış alarm:
    model cümle yerine bölüm kimliği yazmış (`[[sozler/33]]`), alıntı bölümün alt başlığı (S12.10'da talimata: kimlik
    yalnız cümlenindir; sık görülürse bölüm kimliği bölüm atfı olarak kabul edilir). İşaretsiz paragraf 26/40 (giriş,
    yorum ve B7'de işaretsiz temsil özeti dahil; ölçü kabadır).
  - S12.10 **Sohbete ayrı talimat** (kullanıcının kararı, 2026-11-25). `server.py`'nin Risale talimatı bloklara
    ayrılır (iş akışı, cevap kuralları, müellifin sözü olmayan katmanlar); MCP'nin metni bayt bayt aynı kalır (araç
    çıktısı kaydı denetler). Sohbetin talimatı kendi girişi, akışı ve cevap biçiminden (okuyucu kim, önce kısa cevap,
    sonra metin, sonra yorum; uzunluk; sade Türkçe; kapsam) ve **ortak katman bloğundan** kurulur; MCP'ye özgü
    kısımlar (bağdaştırıcılar arası numaralama, denetçi alanları, `cite`) çıkar. Kaynağa bağlılığın koruması ortak
    blokta kalır, kopya olmaz. S12.9'dan not: işaret yalnız cümle kimliğidir, bölüm kimliği değil (C13); özetlenen
    temsil ve "metnin söylediği" paragrafı da işaretlenir (B7'de işaretsiz kaldı).
    **Bitti (2026-11-25):** `server.py`'de Risale talimatı bloklardan kurulur (`RISALE_INTRO`, `FIND`, `READ`,
    `GROUNDED`, `NEVER_INVENT`, `QUOTE_EXACTLY`, `TEXT_APART`, `risale_layers(connectors)`; MCP'ye özgüler `MCP_*`); MCP
    metni bayt bayt aynı (bölmeden önceki metinle karşılaştırıldı). Sohbetin talimatı `sohbet.instructions`: giriş,
    akış (bul, oku, işaretle), "The answer" (okuyucu, önce iki üç cümlelik doğrudan cevap, sonra alıntılarla metin,
    sonra istenirse "Yorum"; uzunluk; kapsam), kurallar (ortak bloklar + işaret kuralı) ve ortak katman bloğu
    (`connectors=False`: başka bağdaştırıcı ve model okumaları anılmaz; denetçi cümlesi kaldı, çünkü sohbetin araçları
    da `reviews` döndürür) ve lügat. Bölüm kimliği: talimat yalnız "konunun işlendiği bölüm" için alıntısız bölüm
    kimliğine izin verir; sunucu alıntısız (ya da alıntısı bölümün başlığı/alt başlığı olan) bölüm işaretini bölüm
    atfı olarak kabul eder (silmez), alıntılı bölüm işaretini bölümün içindeki cümleye taşır, metin penceresi bölümün
    ilk cümlelerini açar. **Ölçüm** (29 soru, `20261125-162212-…`, önceki `153523` ile): beklenen bölüm 27/34 (28/34;
    A1 ve A5'te birer eksik, K3'te kazanç: gürültü sınırında), 21 sn (aynı), toplam 0,125 $ (0,137), model turu yok;
    sunucu 3 bölüm işaretini sildi (bu ölçümden sonra bölüm atfı oldu), 1 alıntı doğrulanamadı (K4: Tarihçe'de lafız
    farkı, ⚠ doğru). İşaretsiz paragraf 178/263: talimat bunu pek değiştirmedi (sayı kaba: giriş ve yorum da sayılıyor).
  - S12.11 **Sol "Kaynaklar" penceresi** (kullanıcının kararı, 2026-11-25). Konuşmanın kaynakları cevaplara göre;
    kaynağa ya da alıntıya dokununca metin aynı pencerede bağlamıyla açılır (cevap ve metin yan yana). Her satırda
    **kaynak adı** (e-Risale, risaleoku.com, Keşif, nurpedia; `works.site`): izinlerin şartı. **Telefonda** alttan
    açılan çekmece; kabul ölçütü: telefon görünümünde baştan sona denenmeden açılmaz (bugün tarayıcıda baştan sona
    görülmedi).
    **Bitti (2026-11-25):** sayfa iki sütun (≥960 px): solda konuşmanın kaynakları cevaplara göre, her satırda yol ve
    "Kaynak: e-Risale" (`catalog/permissions.SOURCE_LABELS`, `works.permission`'dan; B11 aynı tabloyu kullanır), kaynağa
    ya da cevaptaki [n]'ye dokununca metin aynı panelde bağlamıyla ve vurgulu (eski açılır pencere kalktı). Telefonda
    panel alttan çekmece (üstte "Kaynaklar" düğmesi ve sayısı, perde, ✕, Escape), cevabın altındaki liste telefonda
    kalır, masaüstünde gizlenir. Deneme Chrome eklentisi bağlanmadığı için başsız Brave ile:
    `uv run --no-project --with playwright python scripts/sohbet-arayuz-dene.py` (gerçek soru, 12 denetim, ekran
    görüntüleri `data/interim/sohbet/arayuz/`); masaüstü ve 390 px telefon görünümünde hepsi geçti. Kullanıcının kendi
    telefonunda denemesi deploy'dan sonra (S12.7).
  - S12.12 **Geri bildirim** (kullanıcının kararı, 2026-11-25: ilk sürüme). Her cevabın altında 👍/👎 ve isteğe bağlı
    not; "soruyu ve cevabı da gönder" kutusu, varsayılanı kapalı (konuşma sunucuda saklanmaz, yalnız onayla gelir;
    altın soru adayları buradan). Gizlilik politikası (S12.6) yazar.
  - S12.13 **Hızlı ölçüm seti ve modelin yeniden tartılması** (kullanıcının kararı, 2026-11-25). Her değişiklikte 29
    soru yerine 8 (altın soru kimlikleri küçük harfle, plan kimlikleriyle karışmasın): a1 (yer, iki bölüm), b7 (temsil,
    düzeltmeye gitmişti), c11 (metin), d15 (tuzak), e19 (yorum, uzun), k2 ve k4 (uzun araştırma, üçer bölüm), t2
    (tefsir türü); 29 sorunun tamamı model ya da talimat değişiminde ve
    deploy'dan önce. 8 soru yalnız büyük farkı gösterir. Deneme ayında geri bildirimden gelen gerçek sorular sete
    eklenir. Model: hızlı setle üç koşu (Haiku `medium`, Haiku `high`, Sonnet 5.5): gerçek maliyet, süre, sunucunun
    düzelttiği ve doğrulayamadığı alıntı, beklenen bölüm; kullanıcı cevapları yan yana okur
    (`scripts/s12-karsilastir.py`). Ölçüt: aylık 100 $ ÷ beklenen soru sayısı (ayda 1.000 soruda soru başı 0,10 $'a
    kadar: Sonnet sığar; 10.000'de 0,01 $: Haiku). Seçimi kullanıcı yapar: üç koşunun yan yana okuma sayfası
    hazırlanır, beklerken öbür adımlar sürer (kullanıcının kararı, 2026-11-25).
  - S12.4 **Bütçe ve kota:** kişi başına günlük soru sınırı (başlangıç 10), servis düzeyinde günlük ve aylık dolar
    tavanı (100 $; aşılınca "bugünlük doldu"), Console tavanı yedek. Maliyet her cevabın `usage`'ından hesaplanır.
    **Harcama uyarısı:** günlük maliyet bir eşiği geçince kullanıcıya haber (ntfy düzeni hazır). Açılıştan önce hazır
    olmalı (davet yok; adres bir paylaşımla hızla yayılabilir). **Sayılar (kullanıcının kararı, 2026-11-25):** servis
    günde 5 $ (dolunca sayfa herkese "bugünlük doldu" der), ayda 100 $; günlük harcama 2 $'ı geçince ntfy bildirimi.
  - S12.5 **API'nin açtığı fazladan imkânlar** (kullanıcının kararı, 2026-11-25: on madde). İlk sürümün üç maddesi
    S12.3'te yapıldı: Kaynaklar'ı sunucu kurar, tutmayan alıntı (S12.9 ile sunucu düzeltir), alıntıya dokununca metin.
    Kalan maddeler, havuz ve S12.8 (ad ve alan adı) **S13'e taşındı** (kullanıcının kararı, 2026-11-25). S12.8'in
    taşınabilirlik kuralı S12'de de geçerlidir: yol öneki, alan adı, ad ve gönderen ayardandır, sayfada sabit adres yok.
  - S12.6 **Gizlilik ve şartlar:** gizlilik politikası (soruların Anthropic'e gitmesi, e-posta servisi, saklanan ve
    saklanmayan, geri bildirim ve onayla gönderilen soru-cevap, konuşmanın tarayıcıda durması), kullanım şartları (yapay zekâ cevabıdır, tefsir ve fetva değildir), `en/` karşılıkları.
    Önce taslak: kullanıcı okuyup düzeltir, sonra deploy'la çıkar (kullanıcının kararı, 2026-11-25).
  - S12.7 **Deneme ayı:** başlangıç tarihi açılışta yazılır. Ölçüler: kayıtlı ve etkin kullanıcı, günlük soru, soru başı
    gerçek maliyet, atıf denetiminin geçme oranı, 👍/👎 (not isteğe bağlı, kullanıcının onayıyla saklanır). Haftalık
    rapor; ay sonunda sürdürme kararı (eşiği açılıştan önce kullanıcıyla yazılır). Duyuru yok (kullanıcının kararı,
    2026-11-25: adres bilinmiyor, bilen kullanır); Yenilikler yazısı S13'te. **Deploy ve açılış (kullanıcının kararı,
    2026-11-25):** testler ve 29 soru geçince deploy kullanıcıya sormadan yapılır (adres duyurulmadığı için açılış
    sayılmaz; telefon görünümü önce Chrome'da telefon genişliğinde denenir); kullanıcı kendi telefonunda baştan sona
    dener, onaylarsa deneme ayı o gün başlar. **Başarı ölçütü (kullanıcının kararı, 2026-11-25):** ay içinde en az
    10 ayrı hesap açılıp sohbet ederse ve genel olarak olumsuz geri bildirim yoksa (kullanıcıya söylenen ya da çok
    sayıda 👎) başarılı sayılır. 👍/👎 ölçüt değil, yan bilgidir; "etkin kullanıcı" ölçüt değildir.
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
  (sayfada açık "yapay zekâ cevabıdır" ibaresi). Sıra deneme ayının sonucuna göre yazılır.
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
- **el-Bahru'l-Muhît** (Ebû Hayyân, `docs/eserler/tefsir.md` (b)): Aralık'taki tek tefsir kurulumunda ("Sıradaki" 6),
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
