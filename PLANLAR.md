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

Son verilen kimlikler: E6, S7, A3, D15, B8 (yeni iş bir sonrakini alır).

## Sıradaki

Sıra kullanıcının kararıdır. Sıranın ve "Sıradaki"nin tarihli geçmiş notları `KAYIT.md` › "Sıradaki'nin notları"nda.

**Şimdi** (her adımda güncellenir; kullanıcının kararı, 2026-11-19: oturum devri için; önde tek iş):
- **Önde:** D15.1 (21–22). h10 (taslak 1) ölçüldü (İşârât karşılaştırması "düzeltmeyle"; kör aletlerin ayarı yapıldı).
  h9 (taslak 2) yazıldı ve eşleştirildi; İşârât karşılaştırması ve kör A/B (1–2) bağımsız işte: `d1-h9-21-22`
  (`scripts/d1-arka.sh log h9-21-22`; pencere doluysa sıfırlanmayı bekler; bitince `data/d1`'i commit ve push eder).
  Yeni oturumda: `scripts/d1-arka.sh liste`; iş bittiyse birleşik okuma sayfası (A/B ve İşârât yan yana, kartlar
  `provalar/21-22/yerler-D15.1.json`'dan genişletilir: iki taslağın en çok ayrıldığı yerler eklenir), `d1-tur.py`'ye
  A/B'li tek taslak kipi gerekir, sonra `scripts/taslak-gonder.sh`.
- **Kullanıcıdan beklenen:** 21–22'nin okuması, birleşik sayfa gelince (tek taslaklı `tur-21-22-D15.1.html` okunmaz).
- **Sonra:** D15.2 (26–27), D15.3 (28; D5.0.5'in sınaması), D15'in toplu raporu ve karar (h9 mı h10 mu).
- **Bekleyen yan işler** (yeri gelince; D15 sürerken açılmaz): D5.0.4 bölmenin kalanı, S7.
- Bir birimin durumu ve sıradaki komutu: `uv run python scripts/d1-durum.py [birim]`. `data/d1` her adımda commit ve push.
  Uzun işler `scripts/d1-arka.sh baslat <ad> …` ile (terminal kapansa da sürer, uyku engellenir).

| Sıra | Kimlik | İş | Eski adı |
|---:|---|---|---|
| 1 | D15 | Saklı birimlerde son ölçüm (hat h10; 21–22, 26–27, 28; üç dilim, iki kullanım penceresi) | |
| 2 | D5 | Asıl iş: Bakara 34 ve sonrası, küçük adımlarla; ilk adım D5.0 üretim hazırlığı | D1.8 |
| 3 | S7 | Okuma platformu (girişli, davetle) ve ar-ge masasının D5'e göre güncellenmesi | |

**D15. Saklı birimlerde son ölçüm** (kullanıcının kararı, 2026-11-17: kendi aşaması; "D5'ten önceki son düzlük, o
aşamaya kadar ar-ge"; eski D12.6). D14'ün en iyi hattı saklı birimlerde (21–22, 25, 30, 28, 29, 26–27) bir kez, aynı
ölçüyle: kör eleştirmen, envanter (ayar), kullanıcının okuması. D5'e geçiş ölçütü plan belgesi 4.7 (yeni hat çoğunlukla
tercih ediliyor, kapsama düşmüyor, uzunluk hedefte). Burada hat değiştirilmez; açık çıkarsa D14'e dönülür.
- **Kapsam** (2026-11-18 önerisi): her türden bir birim: 21–22 (maksat), 28 (lafız tahkiki), 26–27 (mağlata cevabı);
  25, 29, 30 gerekirse. Hat D14.7'den sonra donar.
- **Hat h10** (kullanıcının kararı, 2026-11-19; bkz. D14.7): `d1-hat.py hazirla <birim> --tarama` (istem
  `istem-hat-h10.md`; tarama tablosu `d1-kalip.py tablo <birim>`), yazdırma `d1-hat.py yazdir <birim> --surum h10`.
  Okumada her birimde **h10'u doğrudan İşârât'la karşılaştıran kart** (kullanıcı kabul etti, 2026-11-18; h2 kolu
  yok): D5'te soru "eskisinden iyi mi" değil, "kendi başına yeterli mi" olacak. Uzunluk
  hedefi kalktığı için geçiş ölçütündeki "uzunluk hedefte" yerine derslerin şişmesi izlenir; ayrıca Tarama'nın
  "taşımıyor" oranı (`d1-kalip.py kontrol`, `kayip`), çelişki ve müfessir adı.
- **Pencere** (kullanıcı, 2026-11-19: ≈50 $ tek kullanım penceresine sığmaz). Birim başına tahmin ≈16 $ (envanter ≈2,
  konu ve tablo ≈0,3, h10 taslağı ≈4,5, h2 taslağı ≈3,5, iki eşleştirme ≈3,5, kör ≈2,3) ve kurulum emeği. Üç dilim:
  **D15.1** 21–22, **D15.2** 26–27, **D15.3** 28 (2026-11-19'da sıra değişti, bkz. aşağıda) ve D15'in toplu raporu; bir pencerede en çok iki dilim (önerilen:
  1. pencere D15.1 + D15.2, 2. pencere D15.3). Her dilim kendi okumasıyla biter.
- **h2 kolu yok** (kullanıcının kararı, 2026-11-19): h2 yeniden kurulmaz (eski hat yeniden kurulmalıydı; birim başına
  ≈7 $). h10 tek başına: envanterin mutlak kapsaması, İşârât kartı, İşârât karşılaştırması (`docs/d1/isarat-karsilastirma-istemi.md`
  i1, `d1-duzelt.py isarat`: bölüm bölüm ve bütün "yeterli / düzeltmeyle / yetersiz", notlar kapalı eleştirmeninkiyle
  aynı biçimde).
- **D15'e üç ek** (kullanıcının kararları, 2026-11-19; sebep: saklı birimlerde cevap elde ama gizli, D5'te kalacak kör
  aletler burada doğru cevapla ayarlanır): (1) **kör aletlerin ayarı:** her birimde h10 taslağına nisbet denetçisi
  (≈1 $) ve kapalı eleştirmen (bütün taslağa tek çağrı, ≈2–3 $ tahmin); bulduklarıyla İşârât kartının ve envanterin
  bulduğu karşılaştırılır: D5'te gerçek kusurların ne kadarını makine yakalıyor, insan okuması nereye gitmeli.
  (2) **D5'in şartı 28'de:** dilim sırası 21–22 → 26–27 → 28; 28'in birinci vechine önceki birim olarak İşârât'ın 26–27'si
  yerine 26–27'nin h10 taslağı verilir (D5.0.5); istem değişmez, birinci vecih raporda ayrı ölçülür. (3) **30 yedekte:**
  D5.0'ın kabul birimi; D15'e, soru kalıpları listesinin yeniden kuruluşuna ve hiçbir denemeye girmez (25 ve 29
  harcanabilir). Maliyet birim başına ≈14–15 $, toplam ≈45 $: iki pencere.
- **D15 yazılırken yan yana** (kullanıcının isteği, 2026-11-19; aynı gün geri alındı: "birkaç işi aynı anda yapabilirim
  diye düşünmüştüm, fakat bunda çok zorlandım"): D5.0.4 birim bölmesi yapıldı ve plana yazıldı, S7 konuşulup plana
  yazıldı; ikisi de yeri gelince sürer. D15 boyunca önde tek iş.
- **h9 ikinci kol** (kullanıcının kararı, 2026-11-19: "h10'dan biraz şüpheliyim"): üç birimde de h9 yazılır (21–22
  dahil). Sebep: h10'un lehine kanıt tek birim (D14.7); Tarama'da zorlama işareti ("taşımıyor" hemen hiç yok: 57/60,
  59/59), 14–15'te çelişki 1 → 3 ve müfessir adı 5 → 11, 21–22'de tercümeyi topluca verme. h10 = h9 + liste + Tarama:
  tek farklı temiz kıyas (h2 kolunun vereceği cevabı daha ucuz verir). h9 kolunun ölçüsü: eşleştirme, İşârât
  karşılaştırması, kör A/B (o3); kapalı eleştirmen ve nisbet yalnız h10'da (işleri aletleri ayarlamak). Birim başına
  ≈12–13 $; D15'in kalanı ≈80 $, muhtemelen üç pencere. **Okuma tek oturum:** kartta A, B (h9 ve h10, kör) ve İşârât
  yan yana; iki soru: hangisi daha iyi, daha iyisi kendi başına yeterli mi; "Aç"tan sonra hangisi hangisi ve aletler;
  yerler iki taslağın en çok ayrıldığı ve "düzeltilecek" yerler, birim başına 6–8 kart. 21–22'nin tek taslaklı sayfası
  (`tur-21-22-D15.1.html`) okunmadan h9'la birleşik sayfaya döner. **Karar kuralı:** üç birimin en az ikisinde kör
  eleştirmen ve kullanıcının okuması h9'u eşit ya da üstün bulursa D5 h9 ile; değilse h10, Tarama'nın zorlaması D5.0'da
  (ara yol: liste kalır, Tarama çıkar).
- **Aletler** (2026-11-19): kapalı eleştirmen bütün taslağa tek çağrı (`d1-duzelt.py kapali <birim> --taslak n
  --butun`); kör aletlerin ayarı `d1-duzelt.py notlar <birim> --taslak n --acik isarat` (kapalı notlar İşârât
  karşılaştırmasının notlarıyla) ve nisbet denetçisinin bulguları aynı notlarla.
- **D15.1 21–22 (sürüyor, 2026-11-19):** birim kaydı (`d1-prova.UNITS`; Türkçe 21 ve 22 iki bölüm; usul özetinden ve
  çizelgeden 21–22'nin örnekleri ve yalnız ona dayanan "her delil bir lafza bağlanır" kuralı çıktı); sızıntı testinde
  kabul: Arapça Mesnevî'nin Nokta'sı (beş cümle, İhsan Kasım'ın tercümesi İşârât'ın Sâni'in delilleri ibaresini
  kullanıyor; müellifin eseri, 9–10 emsali) ve meşhur beyit «وفي كل شيء له آية»; h10 istemi temiz. Üç zorunlu ders
  (لعلكم تتقون، يا أيها الناس، اعبدوا ربكم). Envanter 127 kalem (≈4,5 $; büyük birim). Taslak 1 (h10, ≈5,45 $, 63 bin
  harf). Ölçü: kapsama %40 (mukaddimesiz %50; iki uzun mukaddime), fazla 44, çelişki 1; Tarama 59/59 "taşıyor"
  (zorlama işareti); nisbet denetçisi 57 hükümde 10 hata (≈0,85 $); İşârât karşılaştırması bütünde ve dört bölümde
  "düzeltmeyle" (≈2,95 $; uydurma yok, Risale dersleri sağlam; «لكم» ihtisası İşârât'la çelişki, fâ-i ta'kîb zinciri ve
  iltifat nüktesi yok, nübüvvet–tevhid nisbeti ters, üç mukadder sual eksik; nisbetleri doğru buldu: denetçiyle
  ayrılık, ayarda bakılacak). **Kapalı eleştirmen** (tek çağrı, ≈2,96 $): 31 not. **Kör aletlerin ayarı** (`notlar --acik
  isarat`, ≈0,73 $): İşârât karşılaştırmasının 18 kusur notundan kapalı 4'ünü (+1 kısmen) buldu, 13'ü "yalnız gizli
  metinden" (üç yüksek öncelikli dahil: «لكم» ihtisası, fâ zinciri, iltifat nüktesi), **kapalının görebileceği hâlde
  kaçırdığı 0**; kapalının tek kalan 20 notundan 18'i yerinde. Nisbet denetçisi öbür ikisini tamamlıyor (nübüvvet–tevhid
  nisbetini kapalı kaçırdı, denetçi buldu); 10 bulgusunun 3'ü başka aletle doğrulandı. D5 için ilk okuma: kapalı ve
  nisbet birlikte İşârât'sız görülebileni büyük ölçüde yakalıyor; insan okuması nüktenin derinliğine gider. **Biçim
  bulgusu:** taslak tercümeyi paragraf paragraf değil, birkaç Arapça paragraftan sonra topluca verdi (14–15'te yoktu);
  `Y.pairs` bunu ters eşliyor (masa ve bazı mekanik sayımlar etkilenir; eleştirmenlere giden metin etkilenmez,
  `render_draft` sırayla verir). Kartlarda eşler elle (`cift`); D5.0'ın mekanik kapısına biçim denetimi adayı.
  **Okuma sayfası** `data/d1/masa/tur-21-22-D15.1.html` (`d1-tur.py okuma-tek`, kartlar `provalar/21-22/yerler-D15.1.json`;
  kullanıcı kartları onayladı): yedi yer (beş "düzeltilecek", bir Risale dersi, bir kapalı–nisbet ayrılığı), taslak ve
  İşârât yan yana, hüküm yeterli / düzeltmeyle / yetersiz, aletler "Aç"tan sonra; ≈22 dk. Kalan: kullanıcının okuması.
- **D15 bitince** (kullanıcının kararı, 2026-11-19): işi biten birimlerin prova veritabanları silinir
  (`data/interim/d1-prova/<birim>/risale.db`, `tefsir.db`; birim başına ≈1,5 GB, toplam ≈11 GB; yeniden üretilebilir,
  `d1-prova.py hazirla`). Envanter, taslaklar ve ölçüler `data/d1`'de kalır. 30'unki (kabul birimi) D5.0.9'a kadar.
- **Birim kurulumu (her dilimin başı):** saklı birimler `d1-prova.UNITS`'te yok. `_dev_unit` gibi kayıt: Arapça ve
  Türkçe düğümler (Türkçede 21 ve 22 ayrı bölüm), vecihlerin ilk cümleleri (`sections`), ince Ek 3 için komşu
  birimler, usul özeti ve birim çizelgesinden o birimin örneklerini çıkaran düzeltmeler (`ozet`, `cizelge`; usul
  özeti maksat birimlerinden alıntı taşıyabilir: sızıntı testi gösterir). Sonra `d1-prova.py hazirla <birim>` (prova
  veritabanları), `d1-yz.py envanter <birim>`, `d1-hat.py hazirla <birim> --tarama`, sızıntı testi temiz olmalı;
  soru kalıpları listesi saklı birimlerden alınmadı (sızıntı testi temiz, `data/d1/kaliplar/sizinti-k1.md`).

**D5. Asıl iş: Bakara 34 ve sonrası** (eski D1.8). Tek adım değil, küçük adımlar; D15'ten çıkan hatla (2026-11-17).
- **D5.0 Üretim hazırlığı** (D11'in kalanı, kullanıcının kararları 2026-11-17 ve 2026-11-18; 2026-11-19'da alt adımlara
  bölündü, kullanıcının kararı: eski "D5.0 (n)" göndermeleri D5.0.n diye okunur). **D5'te birim başına insan onayı
  yoktur** (kullanıcı, 2026-11-19: bütün Kur'ân'ın taslağı birinin onayına sunulmak için değil, okunmak için): kalite
  makineden gelir, insan okuması (D5.1, D5.2) hattın kalitesini ölçen örneklemdir, kapı değil.
  - **D5.0.1 Kuyruk** (eski D11.4): birimleri sırayla yazdırmak, kullanım sınırına takılınca sıfırlanmayı bekleyip
    sürmek, pencere başına sığan işi ölçmek. Sıra önerisi: önce Risale-i Nur'un bağ kurduğu âyetler (D5.2'nin çekincesiyle).
    **Kullanım sınırına karşı koruma (yapıldı, 2026-11-19, kullanıcının isteği: "5 saatlik limitin dolması sık … büyük bir
    problem"):** bütün `claude -p` çağrıları `d1-prova.claude_p`'den geçer: çağrıdan önce Haiku yoklaması pencerenin
    doluluğunu öğrenir (`rate_limit_event`), eşiğin üstündeyse (taslak %75, eleştirmen ve ölçüler %85) sıfırlanmaya
    kadar bekler; çağrı yine takılırsa (`usage_limit_reached`) döküm `basarisiz/`'e alınır, beklenir, yeniden yapılır
    (en çok 4 deneme); yedi günlük pencere %98 doluysa durur. Ölçü (21–22): taslak pencerenin ≈%18'ini, İşârât
    karşılaştırması ≈%7'sini, kapalı eleştirmen ≈%12'sini yiyor.
    **Arka plan işleri (yapıldı, 2026-11-19):** `scripts/d1-arka.sh` (`systemd --user`, terminal ve oturumdan bağımsız,
    uyku engellenir; `baslat`, `liste`, `log`, `bekle`, `yeniden`, `durdur`), koşturucu `scripts/d1-arka-is.sh` (iş
    bitince `data/d1` commit ve push, masaüstü bildirimi). Yarıda kalan iş `yeniden` ile aynı komuttan sürer; adımlar
    biteni atlar, taslak yazdırma `d1-hat.py yazdir … --yoksa` ile (o sürümün taslağı varsa yazmaz).
    **Sonraya** (kullanıcının kararı, 2026-11-19; zamanı gelince): (a) **iş başına maliyet tavanı** (ör. "bu iş 15 $'ı
    aşarsa dur"; sınır koruması bekletir ama durdurmaz; D5'te kuyruk günlerce dönerken önemli); (b) **telefona
    bildirim** (masaüstü bildirimi yalnız bilgisayar başında işe yarar; iki yol: bir bildirim servisi (ör. ntfy; iş
    adı ve "bitti" dışarı gider, taslak gitmez) ya da kendi sunucumuzda kurulan bildirim servisi (dışarıya hiçbir şey
    çıkmaz); D5 sunucuya taşınınca daha anlamlı).
    **Bilgisayardan bağımsız çalışma** (kullanıcı kabul etti, 2026-11-19; karar yeri gelince): D5'te birimler günlerce
    sürer; iş sunucuda döner. Parçalar: `claude setup-token` (aboneliğin uzun ömürlü giriş anahtarı, tarayıcısız;
    kullanım aynı pencereden düşer, `claude_p`'nin koruması orada da çalışır); genel ve hadis veritabanları, Kur'ân,
    vektörler sunucuya (deploy betiğinin uzantısı); `data/d1` sunucuda her adımda commit ve push, yerelde `git pull`;
    okuma sayfaları sunucudan doğrudan `/taslak/`'a. **Açık karar:** tefsir sunucusu (4 çekirdek, 7 GB, tefsir ve
    klasik veritabanları orada; genel tefsir ve klasik bağlayıcılarını yavaşlatabilir, `nice` ile) ya da D5'e ayrı
    küçük sunucu (≈7 €/ay; genel hizmet etkilenmez). Güvenlik: abonelik anahtarı sunucuda (SSH yalnız Tailscale'den),
    git'e girmez. Kurulum ≈yarım gün. Bugünkü ara çözüm: `scripts/d1-arka.sh` (terminalden bağımsız, bilgisayar açık).
    **Tek komutla birim hattı** (kullanıcı kabul etti, 2026-11-19): bugün bir birim on küsur komut (kurulum, taslak,
    eşleştirme, eleştirmenler, kör A/B, okuma sayfası); tek komuta bağlanır.
  - **D5.0.2 Uzunluk hedefi:** kapandı, gerek yok (h9'da hedef kalktı, D14.6; derslerin şişmesi D15'te izleniyor).
  - **D5.0.3 İzah katmanı** (günümüz Türkçesiyle, `d1-hat.py izah`; izahları birleştirme "Sonra"da). Okuma platformunda
    (S7) geniş okuyucu için önem kazandı.
  - **D5.0.4 Birim bölmesi** (bekliyor, 2026-11-19, kullanıcının kararı: D15 sürerken yan iş zorladı, yeri gelince
    devam): kullanıcının kararı: önce İşârât'ın mantığı, sonra bütün
  Kur'ân. `scripts/d1-bolme.py`; veriler `data/d1/bolme/`. (a) Müfessirlerin grupları: Râzî Bakara 1–33'te İşârât'ın
  21 sınırının hepsini verir (3 fazla, temsil ve kıssa içinde), Suyûtî 19/21; Râzî'yle Bakara 34–286 ≈211 birim (D5.0
  (7)'deki ≈140 tahmininden fazla). (b) Müellifin her geçişteki sözü (Opus okuması, alıntılar denetlendi,
  `gecisler.md`): ölçüt müellifin kendisinde: atıf cümlede «الاتحاد في المقصد», kıssada «التناسب في الغرض»
  (`isaratul-icaz-arabi/sure-i-bakara/8/c001`); bağ cümle seviyesindeyse birlikte (ikinci vecih), garaz seviyesindeyse
  sınır (birinci vecih). (c) Kural `docs/d1/bolme-kurali.md`: b1'den b4'e dört tur işlenebilirlik sınaması (İşârât'ı
  görmeyen model, yalnız kuralla; kuralsız kol 17–19/21); **b4 üç koşuda üçünde 21/21, fazla yok** (≈3 $). Çekince: b4
  bu 32 geçişe uydurulmuş, genelleme kanıtı değil. **Kullanıcı b4'ü onayladı (2026-11-19)**; Bakara 34–286 b4 ile
  bölündü (≈50 âyetlik parça, üç koşu, çoğunluk; ≈7 $): 157 birim, 253 geçişin 230'unda oybirliği. Koşuların en çok
  ayrıldığı soru «ثم» ile gelen âyetti; **kullanıcının kararı (2026-11-19): önceki üyenin devamı** (b5; «ثم»li üç parça
  yeniden koştu, ≈4 $): **153 birim** (86'sı tek âyetli, en büyüğü 5), oybirliği olmayan 20, Râzî'den ayrılan 80
  (çoğunda biz birleştiriyoruz). İnceleme listesi `data/d1/bolme/bakara/bolme.md`; b4 hâli `bakara/b4/`. Sonra bütün
  Kur'ân; birim kimlikleri kalıcı adres olur.
    **Kalan:** inceleme listesindeki 20 geçiş (kullanıcıyla), sonra bütün Kur'ân (b5 ile; kısa sûreler ve ahkâm
    için kuralın uzatması ayrıca konuşulur).
  - **D5.0.5 Önceki birim:** birinci vecih için İşârât'ın önceki birimi yerine önceki birimin taslağı; D15.3'te 28'de
    sınanır (26–27'nin h10 taslağı).
  - **D5.0.6 Kalite kapısı: denetle, düzelt, yayımla** (2026-11-19'da yeniden tarif: insan onayı olmadığı için kör
    aletler insanı yönlendirmek için değil otomatik düzeltme için): nisbet denetçisi (D14.5b), kapalı eleştirmen (tek
    çağrı), düzeltme turu (D12.1: kapalı notlarla düzeltme işe yaradı ama uzattı; sınanmalı), mekanik denetimler ve
    **biçim denetimi** (her Arapça paragrafın tercümesi hemen arkasında mı; D15.1'de taslak tercümeyi topluca verdi;
    yazımdan hemen sonra çalışır, kullanıcı kabul etti 2026-11-19).
    Ayar verisi D15'ten (D15.1: kapalı İşârât'sız görülebileni kaçırmıyor, nisbet onu tamamlıyor).
  - **D5.0.7 Maliyet:** taslak ≈4,5–5,5 $, konu ve tablo ≈0,3 $, nisbet ≈1 $, kapalı ≈3 $, düzeltme (ölçülecek);
    Bakara'nın kalanı **153 birim** (b5), bütün Kur'ân ≈3.400 birim tahmini (bölmeden sonra güncellenir).
  - **D5.0.8 Soru kalıpları listesinin bütün İşârât'tan yeniden kuruluşu** (D14.7'nin kararı (b): h10 taban olursa;
    D15'ten sonra saklı birimler de girer, 30 hariç).
  - **D5.0.9 Kabul birimi 30:** D5.0'ın değişiklikleri (D5.0.4–D5.0.8) bitince hattın son sınaması; 30 hiçbir denemeye
    ve listeye girmez.
- D5.1 Bakara 34, tek birim, ehlin okuması.
- **D5.2 Risale'si az iki birim, kuyruk büyümeden önce** (kullanıcının kararı, 2026-11-19): bir kıssa (İsrâiloğulları,
  40–74) ve bir ahkâm birimi (178–283) okunur. Sebep: D15'in saklı birimlerinin hepsi Risale'ce zengin (Risale'deki
  doğrudan alıntı 21–22'de 30, 26–27'de 14, 28'de 7); Bakara 34–283'te âyetlerin ≈%78'inde doğrudan alıntı yok (34–39:
  6'da 5, 40–74: 35'te 26, 178–283: 106'da 86; konu üzerinden gelen yerler sayılmadı). h10'un kazancı büyük ölçüde
  Risale dersinden; kuyruk "önce Risale'nin bağ kurduğu âyetler" sırasıyla başlarsa düşüş geç görülür.

**S7. Okuma platformu ve ar-ge masası** (kullanıcının fikri 2026-11-18; vizyon 2026-11-19, kullanıcının kararları;
bekliyor, yeri gelince: D15 sürerken yan iş açılmaz). İki ayrı şey:
- **Okuma platformu (yeni):** D5'in sonucu, yani Kur'ân'ın taslakları, birinin onaylaması için değil, insanların
  okuyacağı, yapay zekânın neyi yapıp neyi yapamadığını göreceği, feyizleneceği bir yer. **Şimdilik basit ve temel:**
  solda Kur'ân paneli (sûre, âyet, birim); birim sayfasında âyet ve meal, taslak (Türkçe önde, Arapça açılır), izah
  katmanı (D5.0.3), atıfa tıklayınca kaynağın kendi metni (kaynağa bağlılığın okuyucuya görünen yüzü), her sayfada
  "yapay zekâ taslağıdır, tefsir değildir" damgası. Bakara 1–33 vitrin olabilir: önce müellifin sözü (İşârât), yanında
  İşârât'ı görmeden yazılmış taslak. Teknik: tek uygulama, birim verisi ayrı dosyalarda, istek üzerine (`review_ui`
  gibi). **Erişim girişli ve yalnız davetle** (kullanıcının kararı); ileride herkese açılırsa herkes hesap açabilir
  (o zaman izinler yeniden gözden geçirilir: taslaklar e-Risale, müfessirler ve Vakıf mealinden alıntı taşır).
  **Hangi taslakların yayımlanacağı** (hepsi mi, kapıdan geçenler mi) vakti gelince kararlaştırılır. **Heyetin
  kullanımı** ileride ayrı ve büyük bir iş (düzenleme altyapısı, ayrıntılı özellikler; dondurulan heyet akışına
  dokunur); bugünden yalnız kalıcı birim kimlikleri ve taslakların sürümlü saklanması gözetilir.
- **Ar-ge masası (bugünkü, güncellenecek):** iç araç olarak kalır; D5'e göre güncellenmesi gerekir (İşârât ve
  envanter olmayan birimlerde kör aletlerin notları, tercümeyi topluca veren taslaklarda eşleştirme (`Y.pairs`),
  birim başına büyük sayfa yerine istek üzerine veri). 2026-11-19'da önerilen "önce buraya bak", durum ve okuma
  işaretleri dilimi D5'te insan onayı olmayacağı için düştü.
- **Özellikler** (kullanıcı kabul etti, 2026-11-19; sıra zamanı gelince belirlenir):
  - İkisinde de: **atıfa tıklayınca kaynak yerinde açılır** (Risale'nin, müfessirin, klasik eserin o cümlesi
    paragrafın altında; yan seçmeden); **Arapça ile tercümesi paragraf paragraf hizalı**, isteğe bağlı üçüncü satırda
    izah (D5.0.3; platformda Türkçe ve izah önde, Arapça açılır; masada önce `Y.pairs` düzelmeli); **ders başlığından
    Risale'deki genişine tek tık**; **bütün taslaklarda arama** (platformda konu araması, masada tutarlılık: aynı nükte
    iki birimde çelişiyor mu).
  - Okuma platformunda: **sûre boyunca kesintisiz okuma kipi** (masada da birimler arası tekrar ve kopukluk denetimi
    için); **âyetin Risale'deki yerleri** müellifin kendi sözüyle (âyet ilişkileri, `find_ayah`; Risale'nin eksen
    oluşu okuyucuya böyle görünür); **"bu taslak nasıl yazıldı" künyesi** (hat sürümü, model, tarih, kaynaklar, geçtiği
    denetimler; birinci gayenin dürüstlük kısmı); **kalıcı bağlantı** (birime ve paragrafa doğrudan adres; ileride
    heyetin notları buna bağlanır); **müfessirler paneli** (aynı âyette on üç müfessirin birimi, Arapça, kapalı başlık);
    **davetli okuyucunun kısa notu** ("bu paragrafta sorun var"; sunucuda veri tutar).
  - Ar-ge masasında: **pano** (kuyruk, pencere başına birim, harcama, aletlerin işaret oranları; Risale'si az
    birimlerdeki düşüşü erken yakalamak için; platformda en çok tek satırlık ilerleme); **bir birimin taslakları
    arasında fark** (yeniden yazma ya da düzeltme gelince; D12.2'nin fark kartları); **okuma sonuçlarının sunucuda
    toplanması** (`/taslak/` hesabıyla, dışa aktarma adımı kalkar; heyet akışından ayrı, tek okuyucu için).

## Bekleyen (başkasının cevabı)

| Kimlik | İş | Kimde | Eski adı |
|---|---|---|---|
| S4.3 | Claude dizini: Risale başvurusu "In review"; dizin ekibine e-posta gitti (2026-11-16) | Anthropic | M7 |
| S4.1 | OpenAI: doğrulanmış kendi adıyla dizine başvurulsun mu | Kullanıcı | M7 |

Kapananlar (2026-11-12): E4 Kızıl İcaz'ın Türkçesi (gerek yok, "Biten"); Diyanet (izin yok, "Biten"); Osmanlıcanın
kaynağı (A2'nin ön şartı değil).

## Sonra (sırası belli değil; sıraya girince kimlik alır)

**Vecih haritası ve açık yazım** (kullanıcının fikri, 2026-11-18; kullanıcının kararı: D5'le paralel değil, **D5'ten
sonra büyük ve kendine has bir iş**; sıraya girince kimlik alır). Kaynak: taslaklar arası fark çok; kullanıcıya göre bu,
"Kur'ân'ın sonsuz bir derya olduğunu gösterme" gizli hedefini açar. Çerçeve (konuşuldu): taslaklar ham madde, ürün
lafız lafız **vecih haritası** (N taslağın nükteleri çıkarılır, aynı vecihler birleşir, ayrı olanlar dayanağıyla
kalır: İşârât, Risale, belâgat, istinbat); haritaya girmeden önce tenevvü ile hata ayrılır (nisbet denetçisi, İşârât'la
çelişki denetimi); ileride başkalarının kendi API anahtarıyla taslak yazdırabileceği bir arayüz (maliyet yazdırana;
Voyage ve sunucu yükü bize; kaynak izinlerinin üçüncü kişilere nasıl taşınacağı; her metin "yapay zekâ taslağı" damgalı,
"tefsir" diye anılmaz). Elde 13 için dört, 9–10 için dokuz taslak var: küçük bir harita denemesi buradan başlayabilir.
**D5 için tek şart:** taslaklar ve ölçü verileri (istem sürümü, kaynaklar, eşleştirme) silinmeden ve yapısal saklanır.

Kimliği olanlar ("Sıradaki"nden indi, kullanıcının kararı, 2026-11-17: sıra yalnız taslakların ar-gesi ve yazımı):
A1 kaynakçada doğrudan bağlantı (Aşama 20), A2 Osmanlıca–Türkçe eşleme (Aşama 19), küçük açıklar B2, B3, B4, B5, B7, B8.

**A1, A2:** ayrıntıları `KAYIT.md`'de eski adlarıyla (Aşama 20, 19). **A2 durumu (2026-11-12):** e-Risale kaynaklarını
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
