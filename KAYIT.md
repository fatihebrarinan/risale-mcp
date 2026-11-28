# Kayıt

Adım kaydı: biten işlerin ayrıntısı ve eski aşamalar. 2026-11-19'a kadar `PLANLAR.md`'nin "Kayıt" bölümüydü;
plan belgesi açık işleri taşısın diye ayrıldı (kullanıcının kararı, 2026-11-19). Açık işler, sıra ve kurallar
`PLANLAR.md`'dedir; biten iş orada "Biten" bölümüne tek satır iner, ayrıntısı buraya ("Kimlikli işler") gelir.

## Sıradaki'nin notları

`PLANLAR.md` "Sıradaki"nin başındaki tarihli notlar (2026-11-12 – 2026-11-19); yerini "Şimdi" bloğu aldı.

Sıra kullanıcının kararıdır (2026-11-12; 2026-11-13'te D1 bölündü; 2026-11-15'te D8 kapandı, D11 açıldı).
**2026-11-16 (kullanıcının değerlendirmesi):** S4'e ara verildi (Claude'da üç eklenti dizinde, Risale için dizin ekibine
e-posta gitti; OpenAI'de kendi adıyla başvuru kararı kullanıcıda), "Bekleyen"e geçti. D11 ve D5 için hazır değiliz,
çok ar-ge gerekiyor: D12 açıldı, masanın ikinci hâli S6. D1–D9'un ortak zemini, döngü ve D8 "Kayıt › Kimlikli
işler"e taşındı (bitmişlerdi, "Sıradaki"de kalmışlardı).
**2026-11-17 (kullanıcının kararı):** "Sıradaki" yalnız taslakların ar-gesi ve yazımıdır: A1, A2 ve küçük açıklar
"Sonra"ya indi; S6 bitti; D12 bitti, kalan turları D14'e geçti; D13 (me'haz) açıldı. D11 bitti, kalanı D5.0;
saklı birimlerde ölçüm kendi aşaması (D15). Yol: D13 → D14 → D15 → D5.
**2026-11-17 (D13'ten sonra):** D13 bitti, h3 taban; biten D11, D12, D13 ve S6'nın ayrıntısı "Kayıt › Kimlikli
işler"e taşındı. Yol: D14 → D15 → D5.
**2026-11-19 (D14.7'den sonra):** D14 bitti, **h10 taban** (kullanıcının kararı). Sırada D15; kullanıcı yeni oturumda
başlayacak (`/clear`), D15'in başlangıç tarifi aşağıda D15'te.
**2026-11-19 (D15'in başı):** D14'ün ayrıntısı "Kayıt › Kimlikli işler"e taşındı. D15.1 (21–22) başladı; yan yana
D5.0.4 birim bölmesi (kural b5, Bakara 34–286 153 birim). Aynı gün (kullanıcının kararı): yan işler (bölme,
S7) plana yazılıp bekler, önde tek iş D15; D5.0 alt adımlara bölündü (D5.0.1–D5.0.9); S7 okuma platformu oldu.

**"Şimdi" bloğunun 2026-11-23 – 2026-11-25 notları** (2026-11-25'te sadeleştirildi, kullanıcının isteği):
- **2026-11-25 (gece):** **E5 bitti ve yayında** (kesintisiz, kullanıcının izniyle). Klasik eklentide 12 eser:
  yedi yeni eser (Şerhu'l-Mevâkıf, Şerhu'l-Makāsıd, et-Telvîh, el-Fıkhu'l-Ekber, el-Munkız, el-Mevâhib, İhyâ),
  `risale_refs`, İhyâ'da Irâkî'nin tahrici şerh ve Risale hadislerine lafız bağı; site ve talimat yeni tanıtımla.
  2026-11-25: kullanıcı `risale_refs` listesine baktı; Yenilikler'de iki duyuru yayımlandı (klasik eserlerin 2.
  dilimi, İşârât'ın misli çalışması; taslak masada açılmıyordu, sunucudaki `docs/` eskiydi: `deploy.sh --site` artık
  yazıların aslını da gönderir); Claude eklentisi 1.0.2 ve ana depo push edildi (dizin eklentiyi yeniden tarar).
  **Kullanıcıdan beklenen:** dizin metinleri başvurular sonuçlanınca (`docs/e5-dizin-metni-taslagi.md`).
  **B10 açık** ("Sıradaki" 1).
  **E7'nin ön çalışması bitti** (2026-11-25, yayınsız; `docs/e7-on-calisma.md`): (a) Kütüb-i Sitte ve Muvatta'da
  lafız gruplaması denendi; geçişli grup zincirleme yapıyor (0,4'te 439'luk grup), öneri çift çift ortak lafız bağı;
  (c) 101 Türkçe sözün 9'unda yalnız kitap düzeyinde künye var; anlamsal arama 10 sözde 0,6'nın üstünde aday buldu.
  Raporun sonundaki beş kararı kullanıcı **E7'nin başında** verecek (kullanıcının kararı, 2026-11-25): E7'ye
  geçilince önce bu kararlar sorulur, sonra iş başlar.
- **Önde (2026-11-23):** **S11 bitti ve yayında:** site yazılarının taslakları masadan düzenlenir (Okumalar › Yazı
  taslakları; düzeltmeler yayımlarken depoya alınır). **A4 bitti ve yayında** (lügat: Risale eklentisinde `lookup_word`, okuma platformunda
  kelimeye dokununca anlam). Kullanıcıdan beklenen: Yenilikler taslağını (`docs/yenilikler/2026-11-23-lugat.md`,
  önizleme `python3 scripts/site-uret.py onizle`) okuyup yayımlamak; eşleme örneklerine bakmak
  (`data/interim/lugat/olcum.md`). Önceki adım **S10** de yayında; kullanıcıdan beklenen: karşılama sayfasını
  (`/oku/#/~hosgeldin`) ve kopyalama damgasını okuyup düzeltmek, sonra ilk davetler (`scripts/sunucu.sh taslak davet
  <e-posta>`). **E6.1 bitti (2026-11-23):** Elmalılı'nın kaynak adayları bulundu, Yazma Eserler Kurumu'na izin
  e-postası gitti ("Bekleyen"); ekleme Aralık'taki tefsir kurulumunda kalır (kullanıcının kararı). **S4.7 bitti (2026-11-23):** Claude eklentisi
  (plugin) 1.0.1 dizine gönderildi; cevap "Bekleyen"de. S4'ün bütün cevapları "Bekleyen"de: Anthropic (S4.3 dört
  bağdaştırıcı, S4.7 eklenti), OpenAI (S4.1). E8 (Arapça tercüme) "Sıradaki" 5'te. D5'in kuyruğu sunucuda Bakara'nın sonuna kadar kendi kendine
  sürüyor (`d1-kuyruk`; durum `scripts/taslak-sunucu.sh durum`, `https://risalemcp.com/taslak/d5.html`).
- **Tarihli hatırlatmalar:** (0) **Kuyruk durunca (Aralık):** B3 (tefsirde uzun cümleler ve kayan âyet birimleri;
  "Sıradaki"de). (1) S8'in site sürümü 2026-11-24'te kendiliğinden yayımlandı;
  Yeniliklere duyurusu 2026-11-25'te yayımlandı. Zamanlı yayının commit'i taşınan eski
  dosyanın silinişini dışarıda bırakıyordu (düzeltildi, 2026-11-25). (2) **≈2026-11-30:** Anthropic'ten Risale için cevap yoksa S4.3'ün
  yedek yolu ("Bekleyen"). (3) **2026-12-13:** kullanıcı mesaj gönderecek; taslaklar bitmemişse
  kuyruk durdurulur (`scripts/taslak-sunucu.sh dur`): Max 2026-12-14'te biter, Pro'ya geçmeden önce kuyruk durmalı
  (aynı aboneliği kullanır, Pro kotasını yer).
- **Kullanıcıdan beklenen:** "Bekleyen"deki cevaplar gelince haber vermek; "Sıradaki" 2 (Risale'si az birimlere göz
  atmak); E8.6 için Arapça okuyan bir denetçi aramak.
- Bir birimin durumu ve sıradaki komutu: `uv run python scripts/d1-durum.py [birim]`. `data/d1` her adımda commit ve push.
  Uzun işler `scripts/d1-arka.sh baslat <ad> …` ile (terminal kapansa da sürer, uyku engellenir).

**"Şimdi" bloğunun 2026-11-26 – 2026-11-27 notları ve 2026-11-22'nin sıra gerekçesi** (2026-11-27'de
sadeleştirildi, kullanıcının isteği: "Şimdi" yalnız şu anki işi taşır; değiştirilmeden):

**Şimdi** (her adımda güncellenir; kullanıcının kararı, 2026-11-19: oturum devri için; önde tek iş; eski notlar
`KAYIT.md` › "Sıradaki'nin notları"):
- **Son adım (2026-11-27):** S13.15.4 bitti: sohbet **`chat.ayinedar.org`**'da, adı Âyinedâr (yayın 2026-11-27 00.36;
  eski `risalemcp.com/sohbet/*` 308 ile aynı yola). Kullanıcı telefonda ve masaüstünde girdi, kod e-postası geldi;
  deneme kullanıcılarına yeni adresi kendisi gönderiyor. Ayrıntı `KAYIT.md` › S13.15.4. Ondan önce S13.15.1–S13.15.3
  (alan adları, DNS ve Caddy, logo) ve S13.17 (öbür kütüphaneler ve âyet çalışması kipi sohbette, yayında), S13.16,
  B11, B10 bitti. **S13.15.5 da bitti (2026-11-27):** okuma platformu `read.ayinedar.org`, masa `lab.ayinedar.org`;
  eski adresler 308 ile; taslak sunucusunun kodu kuyrukta sıradaki birimin başında geçer. **Önde S13.15.6** (çatı
  sitesi `ayinedar.org`). Yeni davet bağlantıları `read.ayinedar.org/davet/…` verir. Açık kalan küçük iş:
  girişsiz tanıtım (`sohbet_hesap.HERO`) yalnız Risale'yi anar, Hakkında bütün kütüphaneleri; tanıtımdan önce bakılır
  (S13.15.6 ile). DMARC ≈2026-12-10'da `p=quarantine`. S12 (sohbet) yayında, Haiku 5.5 medium; 5 kişilik deneme yakın çevreyle sürüyor.
  Yerel deneme: `uv run --extra sohbet python -m risale_mcp.sohbet serve --dev` → `http://127.0.0.1:8010/sohbet/`
  (kod `data/interim/sohbet/eposta.log`'a; deneme hesabı `deneme@example.com`), arayüz denemesi
  `uv run --no-project --with playwright python scripts/sohbet-arayuz-dene.py`, ölçüm `… sohbet olc [--hizli]`,
  kullanım `… sohbet usage`, geri bildirim `… sohbet geri-bildirim` (sunucuda `.venv/bin/python -m …`). Yalnız sohbetin
  değişikliği `scripts/deploy.sh --sohbet` ile gider (≈10 sn; kayıt alınmaz, sohbet dışı kod değiştiyse durur; 2026-11-26). Telefon
  uygulaması "Sonra"da (S13.15'ten sonra, koşullu).
- **Kendi kendine sürenler:** D5 kuyruğu sunucuda Bakara'nın sonuna kadar (`scripts/taslak-sunucu.sh durum`,
  `https://lab.ayinedar.org/d5.html`). Dizin başvuruları (S4.1, S4.3, S4.7) ve Elmalılı izni (E6.1) "Bekleyen"de.
- **Tarihli hatırlatmalar:** (0) **Sohbetin denemesi başladı (2026-11-25), bitişi ≈2026-12-02:** 5 kişi, bir
  hafta. Başlangıç kaydı `data/interim/sohbet/deneme-baslangic-20261125.md` (o gün 3 kişi, 8 soru, 0,056 $, soru başı
  0,007 $, doğrulanamayan 0, 👍 2). Bitince yine `usage` ve `geri-bildirim --days 7` (sunucuda
  `.venv/bin/python -m risale_mcp.sohbet …`), sonra S13.17–S13.21'in sırası gözden geçirilir; öbür eklentiler (S13.17) o hafta
  yalnız yerelde hazırlanır. (1) **≈2026-11-30:** Anthropic'ten Risale için cevap yoksa S4.3'ün yedek yolu. (2)
  **2026-12-13:** kullanıcı mesaj gönderecek; taslaklar bitmemişse kuyruk durdurulur (`scripts/taslak-sunucu.sh dur`):
  Max 2026-12-14'te biter, Pro'ya geçmeden önce kuyruk durmalı (aynı aboneliği kullanır). (3) **Kuyruk durunca
  (Aralık):** tek tefsir kurulumu ("Sıradaki" 6: B3, E6) ve D16.
- **Kullanıcıdan beklenen:** "Bekleyen"deki cevaplar gelince haber vermek; dizin metinleri başvurular sonuçlanınca
  (`docs/e5-dizin-metni-taslagi.md`); S10'un karşılama sayfası (`read.ayinedar.org/#/~hosgeldin`) ve kopyalama damgası, sonra ilk
  davetler (`scripts/sunucu.sh taslak davet <e-posta>`); lügatın eşleme örnekleri (`data/interim/lugat/olcum.md`);
  "Sıradaki" 2 (Risale'si az birimler); E8.6 için Arapça okuyan bir denetçi.
- Bir birimin durumu: `uv run python scripts/d1-durum.py [birim]`. `data/d1` her adımda commit ve push. Uzun işler
  `scripts/d1-arka.sh baslat <ad> …` ile.

Sıra (kullanıcının kararı, 2026-11-22): dış adımlar önce (cevapları haftalar sürer); davetin ön şartları (S10, A4) Max
bitmeden (2026-12-14); mekanik işler (E5, E7) Pro'da da yürür; tefsir verisine Aralık'ta tek dokunuş.

## Aşamalar ve kimlikli işler

2026-11-09'a kadar CLAUDE.md'deki aşama ve adım listesi, değiştirilmeden taşındı. Dondurulan işlerin maddeleri
(HA4, HA6, Y0.2, Y1.3, Y1.4, Y1.8, Y3, Y4, tercüme programı) `PLANLAR.md` "Dondurulan" bölümüne göre okunur.

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

**B13. Sohbette tarayıcı kapanınca cevap ve hak kaybı** (bitti ve yayında, 2026-11-27 17.30, `deploy.sh --sohbet`;
kullanıcının bulduğu: telefonda soru sorulduktan sonra tarayıcı arkada kapandı, cevap gelmedi, hak gitti). Sebep: cevap
sayfanın bağlantısına bağlıydı; kopunca model yarıda kesiliyor, `usage`'a `cancelled` satırı yazılıyor, `asked_today`
her satırı sayıyordu (o gün 3 kesik soru, 13–25 sn). Yapılan: cevap ayrı bir iş (`sohbet.Job`): olaylar bellekte birikir,
sayfa `api/sor/devam?from=N` ile kaldığı yerden yeniden bağlanır (6 deneme, artan bekleme), açılışta süren ya da
ulaşmamış cevabı alır (`resumePending`: konuşmaya yazılmışsa konuşma açılır); biten iş sayfaya bir kez ulaşınca ya da
bir saat sonra silinir, diske yazılmaz. Servis kapanırken süren cevaplar beklenir (`_drain`, `DRAIN_SECONDS = 80`,
Starlette lifespan). Hak yalnız `outcome = 'done'` satırından düşer (geriye dönük: kesik sorular sayılmaz). Gizlilik
sayfaları (tr, en): ulaşmamış cevap en çok bir saat yalnız bellekte. Deneme: testler (3 yeni) ve başsız tarayıcıyla
gerçek API'de üç durum: sayfa kapatılıp 40 sn sonra açıldı (cevap konuşmasıyla geldi), 6 sn çevrimdışı (yeniden bağlanıp
bitti), sayfa kapalıyken servis durduruldu (cevap beklendi, konuşmaya yazıldı).

**S13.23. Arayüz ve deneyim: planın son hâli** (2026-11-28'de "Sıradaki"nden taşındı; S13.23.5 S14.5'e katıldı)

- S13.23 **Arayüz ve deneyim** (kullanıcının önerisi ve kararları, 2026-11-27; sıra içinde aşağıdaki gibi):
  - S13.23.1 (bitti ve yayında, 2026-11-27; `KAYIT.md` › S13.23.1) **Doğrulama e-postası:** kayıtta kod ≈2 dakikada ve spam'e geliyor, anında gelmeli. Ölçüm (2026-11-27):
    Scaleway bugünkü Gmail iletilerini 1–11 sn içinde teslim etmiş (250 OK), 25 Kasım'da bir Proton iletisi
    Scaleway'de 2 dk 20 sn beklemiş; gecikme kimi zaman sağlayıcıda, kimi zaman alıcıda. Spam'in sebebi yeni alan
    adının itibarsızlığı ve paylaşılan IP (SPF, DKIM, DMARC geçiyor). Yapılacak: kod sayfasına "Spam / Gereksiz
    klasörüne bakın, 'Spam değil' deyin" notu; gönderimden sonra Scaleway'den akıbet sorulup teslim edilemeyen ileti
    sebebiyle okuyucuya söylenir (2026-11-27'de bir okuyucunun kodu Gmail kutusu dolu diye hiç ulaşmadı, sayfa
    söylemedi); `mailer.send` olay döngüsünü tıkamasın (`asyncio.to_thread`); istekten teslime geçen süre kayda
    girer; kullanıcı Google Postmaster Tools'a kaydolur. Bir hafta sonra hâlâ geç ya da spam ise sağlayıcı
    değişikliği konuşulur (gizlilik sayfası da değişir); "Google ile giriş" yok.
  - S13.23.2 (bitti, 2026-11-27; `KAYIT.md` › S13.23.2) **Sitede küçük düzeltmeler** (tek site gönderimi): ana sayfadan `lab.ayinedar.org` satırı; RSS
    bağlantıları (alt satırlar, Yenilikler'deki cümle, `<link rel="alternate">`; `yenilikler.xml` üretilmeye devam
    eder, görünmez); "6.236 âyet" sayısı (`ayinedar.org` ve `risalemcp.com` ana sayfaları).
  - S13.23.3 (bitti, 2026-11-27; `KAYIT.md` › S13.23.3) **Kipler açılır menüde** (S13.18'in kipleri düğme taşımaz; her kipin altında kısa açıklama).
    **Eklentiler Ayarlar'da:** oradaki seçim varsayılandır; âyet çalışmasının tefsiri açması ve konuşmada işareti
    geçen kütüphanenin açık kalması sürer; soru kutusunun yanında açık kütüphaneleri gösteren küçük işaret ("Risale
    + Tefsir").
  - S13.23.4 (bitti, 2026-11-27; `KAYIT.md` › S13.23.4) **Temalar ve figür:** 3–4 tema (açık, koyu, sepya, belki simgenin renklerinden), Ayarlar › Görünüm'de;
    yeni konuşma sayfasında simgenin kemerli aynası ve kırmızı kapaklı kitabıyla büyük, sade bir figür, adla. Ölçü
    CLAUDE.md › Âyinedâr: yanındaki söz yapay zekâya vasıf yüklemez. Birkaç seçenek kullanıcıya gösterilir.
  - S13.23.5 **Giriş sayfasının yenilenmesi:** kullanıcı ayrıntıyı sonra verecek; o zamana kadar beklemede.
  - S13.23.6 (bitti, 2026-11-27; `KAYIT.md` › S13.23.6; okuma platformu ve lügat adımı sonraya) **İlk girişte tanıtım:** konuşma listesinde salt okunur "Örnek konuşma" ve üstünde 3–4 adımlık rehber
    (soru kutusu, [1] işareti, Kaynaklar paneli ve metni okumak, kip menüsü, ayarlar); örnek soru "İmanımı nasıl
    arttırabilirim? Risale-i Nur'dan cevapla" gibi (kullanıcının seçimi); cevap sistemin gerçek cevabıdır,
    kısaltılmaz ve düzeltilmez, alıntıları veritabanıyla denetlenir; görüldüğü hesapta tutulur, Ayarlar'dan yeniden
    açılır, haktan düşmez. Lügat gelince rehbere adım eklenir. Okuma platformunun karşılamasına (`#/~hosgeldin`) da
    aynı rehber. S13.23.3 ve S13.23.4'ten sonra, rehberin gösterdiği ekran değişmesin diye. İngilizce ve Arapça arayüz
    (S13.20) bunun ardından: yeni yazılar önce bitsin, sonra hepsi birlikte çevrilsin.
  - S13.23.7 (bitti ve yayında, 2026-11-28; `KAYIT.md` › S13.23.7) **Rehber bildirimle başlar:** ilk girişte rehber
    kendiliğinden açılmaz; sağ üstte "Nasıl kullanacağınızı öğrenin" bildirimi çıkar, "Başlayın" rehberi açar
    (kullanıcının önerisi, 2026-11-28).
  - S13.23.8 (bitti ve yayında, 2026-11-28; `KAYIT.md` › S13.23.8) **Okuma platformunda rehber** (S13.23.6'nın ikinci
    yarısı): karşılamadan sonra sağ üstte aynı bildirim, "Başlayın" taslaklı ilk birimde yedi adım; görüldüğü hesapta.

**S13.23.1. Doğrulama e-postası** (bitti ve yayında, 2026-11-27, `deploy.sh --sohbet`). Ölçüm (`sohbet_hesap
eposta-sure`, son 20 ileti): Scaleway'den alıcı sunucuya ortanca 3 sn; Gmail'e 1–11 sn; tek uzun bekleme 25 Kasım'da bir
Proton iletisi (140 sn, Scaleway'in sırasında). Kullanıcının gördüğü ≈2 dakikalık gecikme Gmail'in içinde (yeni alan
adı). Yapılan: kod sayfası iletinin akıbetini sayfaya özgü jetonla sorar (`kayit/eposta?t=…`, `kod.js`, `delivery`):
ulaştıysa süresi, ulaşmadıysa sebebi ("gelen kutunuz dolu", "bu adreste bir e-posta kutusu bulunamadı"); adres sorguya
girmez. Spam klasörü ve "Spam değil" notu. `mailer.send` `asyncio.to_thread` ile (önceden olay döngüsünü tıkıyordu).
Kullanıcı Google Postmaster Tools'a kaydoldu (2026-11-27). ≈2026-12-04 teslim süreleri ve spam yeniden bakılır.

**S13.23.2. Sitede küçük düzeltmeler** (2026-11-27): çatının ana sayfasından (tr, en) ar-ge masası satırı kalktı
(Belgeler'deki adres tablosu ve gizlilik sayfaları masayı anmaya devam eder: politika gereği); RSS bağlantıları (alt
satırlar, Yenilikler ve Çalışmalar'ın giriş cümlesi, `<link rel="alternate">`) kalktı, `yenilikler.xml` ve
`calismalar.xml` üretilmeye devam eder; "6.236 âyet" sayısı dört ana sayfadan (çatı ve risalemcp.com, tr ve en) kalktı,
sayı şeridi çatıda dört, risalemcp.com'da üç sütun; `ASSET_VERSION` 13.

**S13.23.6. İlk girişte örnek konuşma ve rehber** (2026-11-27; sohbet tarafı). Örnek soru kullanıcının seçimi:
"İmanımı nasıl arttırabilirim? Risale-i Nur'dan cevapla." Cevap sistemin gerçek cevabıdır, kısaltılmaz ve
düzeltilmez: `sohbet ornek` (yeni komut; denetimden geçmeyen alıntı varsa yazmaz) dört kez çalıştırıldı (her biri
≈0,005–0,007 $), en temizi seçildi: birincisinde aynı cümle Tarihçe'deki kopyası ve Şualar'daki aslıyla iki numara
almış, bir yere okunmadan dayanılmış, nâşirin hadis meali tırnakta; ikincisinde yine nâşir meali; dördüncüsünde okunmadan
dayanılan bir yer; seçilen üçüncüsünde bütün dayanılan yerler okunmuş, tefekkür cümlesi müellifin sözü (Emirdağ
Lâhikası), alıntılar blok ve numaralı. Dosya `sohbet_assets/ornek-konusma.json`; kaynaklarının veritabanında durduğu
test edilir. Sayfa: konuşma listesinin başında hep "Örnek · İmanımı nasıl ar…" (salt okunur, geri bildirim yok, soru
sorulunca yeni konuşma açılır; adres `#ornek`). Rehber beş adım (örnek cevap, alıntının numarası, Kaynaklar panelinde
metin, kip menüsü, kütüphaneler ve ayarlar; son düğme "Kendi sorumu soracağım" yeni konuşma açar): ışık halkası ve
dört dikdörtgenli perde (clip-path'li yarı saydam perde başsız tarayıcıda çizilmedi sanıldı; piksel ölçümü çizildiğini
gösterdi, yine de en sağlam yol seçildi), panel animasyonundan sonra yeniden ölçülür. İlk girişte kendiliğinden açılır;
görüldüğü `users.tour_seen` (eklenen sütun; mevcut hesaplar da bir kez görür), `api/durum` `tour`, `api/ayarlar`
`tour_seen`; yeniden Ayarlar › Belgeler › "Tanıtımı yeniden göster" ya da `#tanitim`. Deneme: geniş ve telefon
genişliğinde baştan sona (beş adım, son adımda yeni konuşma, yeniden açılışta rehber yok, sayfa hatası yok).
Okuma platformunun karşılamasına aynı rehber sonraki iş.
Kullanıcı örnek cevabı onayladı (2026-11-27) ve iki düzeltme istedi: başlığın altındaki "Cevaplar Risale-i Nur'dan
alıntılarla gelir; her alıntının yeri Kaynaklar'dadır." cümlesi kalktı (rehber anlatıyor); okuyucuya görünen ad "kip"
değil **"mod"** (menüde "Mod · Serbest soru", rehberde ve Ayarlar › Kütüphaneler'de de). Koddaki adlar (`kipler.py`,
`mode`) ve iç belgeler değişmedi.

**S13.23.7. Rehber bildirimle başlar** (2026-11-28; kullanıcının önerisi). İlk girişte rehberin kendiliğinden açılması
yerine sağ üstte, başlığın altında bir bildirim: "Nasıl kullanacağınızı öğrenin" (örnek konuşma üzerinde beş adım;
sonra Ayarlar › Belgeler'den de açılır), düğmeler "Başlayın" ve "Şimdi değil" (× da aynı). "Başlayın" rehberi
açar; rehber bitince ya da bildirim kapatılınca `tour_seen` yazılır. Bildirime dokunmadan soru sorulursa yalnız o
açılışta kalkar, sonraki girişte yine çıkar. `#tanitim` ve Ayarlar › Belgeler rehberi doğrudan açar. Dar ekranda
boydan boya. Başsız tarayıcıda geniş ve telefon genişliğinde denendi (görünür, Başlayın → rehber, Şimdi değil →
kaydedildi, yeniden yüklemede çıkmıyor; sayfa hatası yok).

**S13.23.8. Okuma platformunda rehber** (2026-11-28; kullanıcının isteği, S13.23.6'nın ikinci yarısı). Sohbetteki
bildirim ve rehberin aynısı `scripts/oku-app.html`'de (yalnız platformda, masada yok). Karşılama sayfası (S10,
"tefsir değildir" uyarısıyla) yerinde kalır; "Okumaya başla"dan sonra sağ üstte "Nasıl okuyacağınızı öğrenin" bildirimi
çıkar. "Başlayın" taslağı ve İşârât'ı olan ilk birimi (bugün Bakara 9–10) taslak sekmesinde açar, yedi adım: Kur'ân
paneli (telefonda ☰), sekmeler (müellifin sözü ve taslak), görünen ilk atıf numarası, kaynağın metni (geniş ekranda
yan sütun, dar ekranda paragrafın altı; adım bitince kapanır), Arapça/İzah/Lügat düğmeleri, "Not ekle", Notlarım.
Birimde olmayan adım atlanır. Bitince ya da Escape ile okuyucu başladığı yere döner. Bildirim kapatılınca ya da rehber
bitince `users.toured` yazılır (`site_auth.py`, `POST /api/rehber`, `/ben` `toured` verir); bildirime dokunulmazsa
sonraki açılışta yine çıkar. Panelin altında "Tanıtım" bağlantısı, karşılama sayfasında (ikinci gelişte) "Tanıtımı
göster"; `#/~tanitim` doğrudan açar. Deneme: `tests/test_site_auth.py` (rehber bayrağı); başsız tarayıcıda geniş, orta ve
telefon genişliğinde sahte giriş servisiyle (karşılama → bildirim → yedi adım → giriş sayfası, bayrak yazıldı, yeniden
yüklemede çıkmıyor; "Şimdi değil"; panelden açılıp Escape ile dönüş; sayfa hatası yok). İlk denemede 3. adım gizli
Arapça satırdaki numarayı hedefliyordu: görünen ilk numara seçilir, ışık köşeli ayracın tamamına düşer.

**S13.23.4. Temalar, ayna figürü, dinamik karşılama** (2026-11-27; kullanıcının fikri ve kararları aynı gün).
Kullanıcı başlığın üstünde "ayna, aynanın içinde kütüphane, logodan ayrıntılı" istedi; üç seçenek gösterildi (A raflar,
kandil, rahle üstünde logonun kırmızı kapaklı kitabı; B iki yanı raflı koridor, sonda kemerli pencereden ışık; C A'nın
çizgi hâli), kullanıcı Claude'un değişen karşılamasından ilhamla dördüncüyü (D, B'nin çizgi hâli) ve hepsinin rastgele
gösterilmesini istedi. Çizimler `scripts/ayna-figur.py` (sabit tohum; `--onizleme` dört temada önizleme) →
`sohbet_assets/ayna-{a,b,c,d}.svg`; A ve B kendi renkleriyle, C ve D CSS maskesiyle temanın vurgu renginde; adreste sürüm
(`?v=`, sayfanın sürüm özetine girer). Karşılama sözleri (kullanıcı onayladı, noktalı virgüller virgül oldu): "Ne
sormak istersiniz?", "Bugün hangi meseleye bakalım?", "Aklınızdaki soru nedir?", "Kütüphane açık, ne arıyorsunuz?",
"Hangi bahsi okumak istersiniz?", "Bir âyet, bir hadis, bir mesele…", "Merak ettiğiniz bir mesele mi var?", "Hangi
risaleden başlayalım?"; sabah 5–11 "Hayırlı sabahlar, bugün neyi okuyalım?", Cuma "Hayırlı Cumalar, ne sormak
istersiniz?" havuza katılır. Ölçü: söz yapay zekâya vasıf yüklemez, eserlerden söz aktarmaz. Figür ve söz her yeni
konuşmada (ve açılışta) seçilir, bir öncekinin aynısı gelmez, sayfa açıkken değişmez. Temalar: Sepya (kâğıt) ve Zümrüt
(simgenin yeşili ve altını) eklendi. Telefonda Ayarlar sekmeleri iki satıra sarılır (yana kayınca sağdakiler
görünmüyordu). Deneme: dört temada ve telefonda başsız tarayıcı, sayfa hatası yok.

**S13.23.3. Kip menüsü, kütüphaneler Ayarlar'da** (2026-11-27). Soru kutusunun üstünde tek satır: solda kip açılır
menüsü ("Kip · Serbest soru", yukarı açılan liste, her kipin altında açıklaması; klavyeyle ok, Home/End, Enter, Escape;
serbest dışındaki kipte düğme vurgulu), sağda açık kütüphanelerin işareti ("Risale-i Nur + Tefsir"; dokununca Ayarlar ›
Kütüphaneler). Ayarlar'da yeni sekme Kütüphaneler: Risale-i Nur sabit, öbürleri onay kutusuyla, seçim bu cihazda
(`sohbet:kutuphaneler`). Davranış değişikliği: kipin (âyet çalışması → Tefsir) ya da konuşmanın açtığı kütüphane
artık okuyucunun varsayılanına yazılmaz, yalnız o konuşmada açık görünür (sunucu zaten böyle: `Chat.ask`); işaret
okuyucunun seçimi, kipin kütüphaneleri ve konuşmanın turlarındaki kütüphanelerin birleşimidir (`kipler.public`
`libraries` verir). Dar ekranda ayar sekmeleri yana kayar, seçilen görünür. Deneme: testler ve başsız tarayıcıda
geniş ve telefon genişliği (menü, klavye, işaret, ayar sekmesi; sayfa hatası yok); `scripts/sohbet-arayuz-dene.py`
yeni menüye uyarlandı.

**S13.15.6. Çatı sitesi `ayinedar.org`** (bitti ve yayında, 2026-11-27 gecesi, kullanıcının izniyle kesintisiz;
yayın `yayin-20261127-020105`, araç çıktısında fark yok). Kullanıcının kararları (2026-11-27): yazılar **hemen taşınır**
("sayfayı taşıma derdini tekrar taşımayalım"); çatı ve **sohbet arama motorlarına açılır**, üstte görünmeye yarayan ne
varsa yapılır; başlık ve tanım bütün kütüphaneleri kapsar, "yapay zekâ" başlıkta da geçer; kısa `/en/`; ar-ge masası
altta tek satır; alt bilgide bağımsızlık cümlesi, "Nur Hadimleri", `destek@ayinedar.org`; ana sayfada sohbetten
kısaltılmamış örnek cevap; sohbetin tavanları aynı; gece yayına alınır (denetimler temizse).
- **Çatı** (`site-ayinedar/`): ana sayfa (logo, "Risale-i Nur'a, tefsirlere, hadis kitaplarına ve klasik eserlere
  sorun; cevabı kaynağıyla okuyun", "Sohbete başlayın", aynanın cümlesi, beş sayı, Nasıl çalışır, örnek cevap,
  Projeler: Sohbet, Eklentiler, Okuma platformu (davetli), masa tek satır, Neye güvenebilirsiniz, son yenilikler,
  kaynaklar), Belgeler (Âyinedâr nedir, hizmetler ve adresleri, ilkeler, kaynaklar ve izinler, politikalar, iletişim),
  gizlilik (çerez, sayaç, erişim günlüğü yok; hizmetlerin kendi politikalarına tablo), kullanım şartları, `en/`
  (ana sayfa, gizlilik, şartlar), 404, `robots.txt`, `sitemap.xml`; görünüş `ayinedar.css` (Literata ad yazısı, logonun
  altını), paylaşım kartı `img/paylasim.png` (`scripts/paylasim-ayinedar.py cati`).
- **Örnek cevap:** "Hastalığa nasıl sabredilir? Risale-i Nur'dan kısaca anlatır mısın?" sohbete yerelden soruldu (Haiku
  5.5, 26 sn, 0,008 $; denetimde düzeltilen ya da doğrulanamayan yok), kısaltılmadan ve düzeltilmeden konuldu. Dokuz
  alıntının dokuzu da Yirmi Beşinci Lem'a'nın atıf verilen cümlelerinde (biri şapkada ayrılıyor: model "hàlis"i
  "hâlis" yazdı; sohbetin denetimi şapkayı yok sayar). Model alıntıları blok değil satır içinde verdi; sohbetin
  gerçek davranışı olduğu için öyle bırakıldı.
- **`site-uret.py` iki site kurar:** yazılar, dizinleri, RSS (`guid` eski risalemcp.com adresi) ve önizleme çatının
  iskeletiyle; `style.css`, `site.js` ve Naskh `site/`'tan kopyalanır; yazıdaki eklenti sayfası bağlantısı risalemcp.com'a
  tam adres olur (`cross_links`); çatının sayfalarında simgeler, `ayinedar.css`, kanonik adres ve başlık soneki
  `cati_head` ile; iki site haritası; risalemcp.com'un menüsündeki Yenilikler ve Çalışmalar ile ana sayfa şeridi çatıya
  tam adresle, alt bilgisinde "Âyinedâr'ın eklentileri". İşârât'ın usul özeti (`isarat-usul/`) çatıya taşındı
  (`scripts/d1-okur.py` oraya yazar). Atıf satırı "Âyinedâr, «…»".
- **Sohbet:** girişsiz açılış kökte, yönlendirmesiz (önce `/kayit`'e 302); tanıtımlı sayfalar (açılış, kayıt, giriş)
  dizine açık, kanonik kök, başlık "Âyinedâr · Sohbet: Risale-i Nur, Tefsir, Hadis ve Klasik Eserler için Yapay Zekâ",
  JSON-LD (WebApplication); kod, hesap ve çevrimdışı sayfaları `noindex`; `robots.txt`, `sitemap.xml`; belge
  sayfalarına kanonik; tanıtım (`HERO`) öbür kütüphaneleri anar ("Bütün külliyat, isterseniz daha fazlası"); gizlilik
  ve şartlar (iki dil) çatının politikalarına da gönderir. Test `test_search_engines`.
- **Caddy:** `ayinedar.org` dizine açık, HSTS, 404 sayfası (Caddy 2.6'da `handle_errors` durum kodu almıyor:
  `expression` eşleyicisi); `connect.` S13.22'ye kadar risalemcp.com'a 302; risalemcp.com'da `/yenilikler*`,
  `/calismalar*`, `/isarat-usul*` çatıya 308, eski `/taslak/isarat-usulu.*` doğrudan çatıya; lab'ın önizlemesi stili
  çatıdan alır; sohbetten `X-Robots-Tag` kalktı. Yapılandırma önce sunucuda `caddy validate` ile denendi.
- **Denetim:** yerelde iki tarayıcı turu (açık, koyu, telefon; konsol hatası ve kırık istek yok), 824 test, canlıda
  durum kodları ve yönlendirmeler, iki başlık (`X-Robots-Tag` yok), sohbetin canlı açılışı.
- **Kalan:** Search Console ve Bing doğrulaması kullanıcıda (Cloudflare TXT). Yenilikler'e çatı için bir duyuru
  yazılmadı (istenmedi).

**S13.15. Ad, logo ve site düzeni: Âyinedâr — kapanış kaydı** (2026-11-27): S13.15.6 ile bitti. "Sıradaki"deki son hâli:

- S13.15 **Ad, logo ve site düzeni: Âyinedâr** (kullanıcının kararı, 2026-11-26; eski S13 (12) ve S12.8): platform
  tanıtılmadan önce kendi adı, logosu ve sitesiyle tanınsın. Ad Âyinedâr. Adın geçmişi ve gerekçesi, düzenin kararları
  (a)–(e) `KAYIT.md` › S13.15'te; kalıcı olanlar (alt alan haritası, tanıtımın ölçüsü, proje adının kuralı) CLAUDE.md'de.
  - S13.15.1–S13.15.5 bitti (2026-11-26 – 2026-11-27): alan adları (marka başvurusu yapılmaz), alt alan haritası ve
    Caddy, logo, sohbet `chat.`, okuma platformu `read.` ve masa `lab.`. Ayrıntı `KAYIT.md` › S13.15.x.
  - **S13.15.6 Çatı sitesi `ayinedar.org`** (kullanıcının kararları, 2026-11-27): ana sayfa önce sohbete çağırır, öbür
    projeler ikinci sırada (okuma platformu davetli; eklentiler bugün risalemcp.com'da; ar-ge masası altta tek satır,
    "deneysel, girişli"). Yenilikler ve Çalışmalar **hemen taşınır** (risalemcp.com'daki adresleri 308 ile; taşıma
    ikinci kez yapılmasın), çatının belgeleri, gizlilik ve şartları; kısa `/en/` (ana sayfa, gizlilik, şartlar).
    Çatı ve **sohbet arama motorlarına açılır** (canonical, hreflang, site haritası, JSON-LD, Open Graph; analitik ve
    dışarıya istek yok); okuma platformu ve masa `noindex` kalır. Başlık ve tanım bütün kütüphaneleri kapsar,
    "yapay zekâ" başlıkta da geçer. Alt bilgide bağımsızlık cümlesi, "Nur Hadimleri", `destek@ayinedar.org`. Ana
    sayfada sohbetten kısaltılmamış, düzeltilmemiş bir örnek cevap. Sohbetin tavanları aynı kalır; girişsiz tanıtımı
    (`sohbet_hesap.HERO`) öbür kütüphaneleri de anar. risalemcp.com'da eklentilerin sayfaları kalır, menüdeki
    Yenilikler ve Çalışmalar çatıya gider, alt bilgiye çatı bağlantısı. Denetimler (bağlantılar, araç çıktısı
    karşılaştırması, tarayıcı denemesi) temizse gece yayına alınır. Sonra kullanıcı Search Console ve Bing doğrulaması.

**S13.15. Ad, logo ve site düzeni: Âyinedâr — ana kayıt** (2026-11-26 – 2026-11-27; "Sıradaki"den değiştirilmeden
taşındı, 2026-11-27, kullanıcının kararı: "Sıradaki" kısalsın; S13.15.7 aynı gün S13.22 oldu):

- S13.15 **Ad, logo ve site düzeni: Âyinedâr** (kullanıcının kararı, 2026-11-26; eski S13 (12) ve S12.8; önce
  "sohbetin kendi adı, logosu ve sitesi"ydi, 2026-11-26 akşam bütün projelerin düzenine genişledi): kullanıcı platformu
  yakın çevresi dışında kimseye tanıtmadı; insanlar onu kendi adıyla, logosuyla, sitesiyle tanısın, bu hâliyle
  (`risalemcp.com/sohbet`) tanıtılmaz. Gerçek geri bildirim tanıtımdan sonra gelir; 5 kişilik deneme yakın çevreyle
  sürer. Adın ölçütleri: müellif adına konuşuyor izlenimi vermez; "Risale-i Nur" adını tek başına almaz; kısa, Türkçe
  söylenişi kolay; alan adı alınabilir; başka bir hizmetle karışmaz; hadis, tefsir eklenince de uyar; ölçü adın kendisidir, sözlük
  tanımı değil (kullanıcı: "Claude", "Gemini" de mantıkla bakınca mantıksız).
  **Adın geçmişi (2026-11-26):** adaylar Fidanlık (S13.3), Tahkik, Hemdem, Kubbe; sonra Âyinedâr, Bezm, Hüdhüd. Önce
  Tahkik seçildi (tahkik.org; TÜRKPATENT 9/41/42'de kayıt yok); tahkik.com'da tescilsiz bir Türk hukuk yazılımı
  (2022'den beri), tahkik.app'te aynı alanda yapay zekâlı bir doğrulama aracı ("Tahkîk — Akademik Araştırma ve
  Doğrulama Çalışma Alanı", alan adı 2026-08-08) çıktı; Âyinedâr yedek kaldı. Hemdem düştü (hemdem.app tanışma
  uygulaması, TÜRKPATENT'te çok kayıt).
  **Karar (kullanıcı, 2026-11-26 akşam): ad Âyinedâr.** Gerekçe: işi anlatıyor (ayna kendi ışığını vermez, gösterdiğini
  kaynağa borçludur: "yapay zekânın ürettiği hiçbir şey tefsir diye anılmaz" ilkesinin adı gibi), bütün uzantılar boş,
  web aramasında marka ya da uygulama çıkmadı. Eserlerde 82 cümlede geçer (Sözler › Otuz Üçüncü Söz › Otuz Birinci
  Pencere'de iki bölüm başlığı "… Âyinedârlık İse"); çoğunlukla varlıkların Esmâ-i Hüsnâ'ya âyinedârlığı için,
  Hanımlar Rehberi'nin "Nurcuların Kasidesi"nde Risale-i Nur'un kendisi için ("Kur'ân'ın bir âyinedarlığını"). Bu yüzden
  **tanıtımın ölçüsü** "eserlerin ne dediğini yansıtır"dır, "Kur'ân'ın âyinedârı" denmez (Risale'ye verilen vasıf
  yapay zekâya verilmez). Yazım: metinde ve logoda "Âyinedâr", alan adında `ayinedar`.
  **Düzenin kararları (kullanıcı onayladı, 2026-11-26):**
  (a) Alt alan adları **işlevli, İngilizce ve kalıcı** (kullanıcının kararı, 2026-11-26: uluslararası hedef için;
  önce Türkçe önerilmişti); proje adları üstüne giyen addır, adrese girmez (ad bir günde iki kez değişti; "kimlikler
  değişmez" ilkesi). Tek kelime, kısaltma yok, Türk okuyucunun da bildiği kelimeler. **Harita (kullanıcı onayladı,
  2026-11-26):** `ayinedar.org` çatı (projeler, yenilikler, çalışmalar, belgeler, gizlilik; ana sayfa önce sohbete
  çağırır), `chat.ayinedar.org` sohbet, `read.ayinedar.org` okuma platformu (davetli), `lab.ayinedar.org` ar-ge masası
  (bugünkü `/taslak/`; deneysel olduğunu söyler), `connect.ayinedar.org` eklentilerin tanıtımı ve kurulumu (Claude
  "connector", ChatGPT "app" der; ikisini kapsar; risalemcp.com'un sayfaları oraya yönlenir, S13.15.7). `www.` ve
  `ayinedar.com` köke yönlenir. **Adresin dili sabit, sayfanın dili yolda:** Türkçe varsayılan, `/en/`, ileride `/ar/`
  (S13.20). Ayrılmış: `mcp.` (ileride ayinedar altına girecek bir MCP sunucusu için; bugünkü MCP adresleri
  risalemcp.com'da kalır, (e)). "ai." kullanılmaz (ehil okuyucuya yapay zekâ öne çıkmasın). Eski eklenti adreslerinin
  Türkçe olması (`hadis.`, `tefsir.`, `klasik.risalemcp.com`) ayrı alan adında olduğu için düzeni bozmaz. Kazancı: her
  alt alan ayrı servis, gerekirse ayrı makine; çerezler kendiliğinden ayrılır.
  (b) **Asıl adres .org**, .com ona 301 ile yönlenir (izinlerin çoğu "kazanç olmadığı sürece" şartlı; e-posta
  göndericisi tek alanda: `noreply@ayinedar.org`). tahkik.org alınmamıştı.
  (c) **İç ad ile dışa açık ad ayrı:** okuyucu tek ad ve işlev görür ("Âyinedâr · Sohbet", "Âyinedâr · Okuma"); iç
  proje adları aramızda ve planda serbest. Proje adının kuralı: (1) eser ya da bölüm adıyla çakışmaz (araçlar onları
  adresler), (2) müellife ya da eserine verilmiş bir vasıf değildir, (3) yapay zekânın ürününe hüküm yüklemez. Bu
  yüzden "Miftah" düştü (Barla Lâhikası'nda Üstad için "Hazine-i Kur'ân'ın bir miftahıdır" başlığı; klasik kütüphanede
  Sekkâkî'nin Miftâhu'l-Ulûm'u); taslaklar için alçakgönüllü bir ad aranır (öneri "Müsvedde"; karar yok).
  (d) **Model adları:** "Habbe / Kubbe" düştü ("habbeyi kubbe yapmak" abartmak demek, Emirdağ Lâhikası'nda bu anlamda
  başlık; Habbe Mesnevî-i Nuriye'nin bir risalesi, `mesnevi-i-nuriye/habbe`). İkinci model gelirse seçicide işlevsel
  etiket ("Hızlı", "Derinlemesine"), ayrıntıda çalışan model açıkça; ad modelin kimliğini saklamaz. Maliyet, kota ve
  ölçüm birlikte tartılır ("Fikirler" › Sohbette model kademeleri).
  (e) **Dokunulmayanlar:** eklentilerin MCP adresleri (mcp., hadis., tefsir., klasik.risalemcp.com: kullanıcıların
  ayarlarında, dizin başvurularında, eklenti deposunda, OpenAI alan doğrulamasında kayıtlı); risalemcp.com kökünün
  favicon'u (Claude eklenti simgesini oradan alır; kök yönlense de favicon sunulur); dizin başvurularında adı geçen
  gizlilik ve kurulum sayfaları, başvurular sonuçlanana kadar. Geçişi ucuz tutmak için ad yalnız ayarlarda
  (`SOHBET_NAME` …) ve metinlerde durur; logonun simgesi addan bağımsız çizilir.
  Adımlar (sıra bu; kullanıcının onayı, 2026-11-26):
  - **S13.15.1 Ad ve alan adları** (bitti, 2026-11-26): kullanıcı `ayinedar.org` ve `ayinedar.com`'u aldı (ad
    sunucuları Cloudflare'de; kayıtlar S13.15.2'de, DNS only). **Marka başvurusu yapılmaz** (kullanıcının kararı,
    2026-11-26): "Biz bir marka değiliz, ticari değiliz; insanlara İslâmî kaynaklara ücretsiz erişim sağlamaya
    çalışıyoruz." TÜRKPATENT'ten bir şey alınmaz; ileride adla ilgili zor duruma düşülürse kullanıcı o zaman başvurur.
    Bu yüzden metinlerde "marka" denmez; ad bir hizmetin adıdır.
  - **S13.15.2 Alt alan haritası** (bitti, 2026-11-26): harita (a). DNS (kullanıcı açtı): iki kökte A
    `95.217.21.105`, alt alan adları CNAME ile köke (sunucu değişirse iki kayıt değişir; CAX11 yükseltilirse IP aynı
    kalır), ayinedar.com'da `v=spf1 -all` ve DMARC `p=reject` (e-posta göndermez); ayinedar.org'un e-posta kayıtları
    S13.15.4'te. Caddy (`docs/Caddyfile`): kök ve dört alt alan adı `site-ayinedar/`'ın "hazırlanıyor" sayfası
    (`noindex`), `www.` ve .com 301 ile `ayinedar.org{uri}`'ye; sertifikalar alındı. `deploy.sh` sayfayı tam
    gönderimde ve `--site`'ta `/var/www/ayinedar`'a gönderir. Bu sefer yalnız sayfa ve Caddyfile gönderildi
    (kullanıcının kararı: kod gitmedi, servis yeniden başlamadı); önceki Caddyfile sunucuda
    `/etc/caddy/Caddyfile.onceki-20261126`.
  - **S13.15.3 Logo** (bitti, 2026-11-26): kullanıcının seçimi **kemerli aynada açık, kırmızı kapaklı kitap**
    ("eserlerin ne dediğini yansıtır"). Taslaklar claude.ai'de: Tahkik'in altı fikri
    (`claude.ai/artifact/VCzNVxxTiu2fcRPwUEfzrj`), ayna üzerine dört çeşit (kemerli, oval, aynada kitap, güneş ve
    aksi; `claude.ai/artifact/7wdoa4VY7eYXiWqVhy35jG`, dosyaları `data/interim/ayinedar-logo/`); kullanıcı 3'ü seçti,
    kemerli aynaya aldırdı, kapağı kırmızı ve aynanın içini kitabın etrafında boşluk kalacak kadar geniş istedi.
    Renkler: zemin `#1d4d3c` (eklentilerin yeşili), cam `#2b6a53`, çerçeve ve taban `#e8c766`, kapak `#b8322a`/
    `#9e2a23`, sayfalar `#f6efdc`/`#e6dbbd`. Dosyalar `site-ayinedar/`: `icon.svg` (asıl), `icon-kucuk.svg` (16 ve 32
    piksel: kalın çerçeve, parıltısız, kitap iki düz parça), `icon-maskable.svg` (köşesiz, güvenli alanda; PWA ve
    Apple); `scripts/ikon-ayinedar.sh` `favicon.ico`, `icon.png`, `icon-192.png`, `icon-512.png`,
    `icon-maskable-512.png`, `apple-touch-icon.png` üretir. Yazı: Literata 500 ("Âyinedâr"; OFL); sayfalara
    girerken kendi sunucumuzdan verilir (dışarıya istek yok). Eklentilerin simgeleri değişmedi (`scripts/ikon.sh`).
  - **S13.15.4 Sohbetin taşınması** (bitti, 2026-11-27): sohbet `chat.ayinedar.org`'da, adı Âyinedâr; eski adres 308
    ile aynı yola; e-posta `noreply@ayinedar.org` (Reply-To ve `destek@ayinedar.org`), kod e-postasında bağlantı yok;
    simgeler ve ad yazısı, PWA, Hakkında (`/hakkinda`, Diyanet bildirgesinin 7. maddesi), güvenlik başlıkları, 404,
    paylaşım kartı, tanıtıma kadar `noindex`. Yapılmayan: `__Host-` çerez öneki (gerekçe `KAYIT.md`), mağaza uygulaması
    ("Sonra"). DMARC bir iki hafta sorunsuz gönderimden sonra `p=quarantine`. Ayrıntı `KAYIT.md` › S13.15.4.
  - **S13.15.5 Okuma platformu ve masanın taşınması** (bitti, 2026-11-27): platform `read.ayinedar.org`, masa
    `lab.ayinedar.org` (disk düzeni aynı); giriş servisi iki bölümde aynı kısa yollar, bölüm `X-Bolum` başlığından,
    masaya yalnız `masa` kapsamı; çerez alan adına bağlı (kullanıcının kararı: masa hesabı iki yere ayrı girer); eski
    sayfaların `/taslak/` öneki atılır, `risalemcp.com/oku/*` ve `/taslak/*` 308 ile aynı yola (açık davetler çalışır);
    ad ve simge Âyinedâr. Ayrıntı `KAYIT.md` › S13.15.5.
  - **S13.15.6 Çatı sitesi:** `ayinedar.org`; ana sayfa önce sohbete çağırır, öbür projeler ikinci sırada; yenilikler,
    çalışmalar, belgeler, gizlilik buraya (`scripts/site-uret.py`).
  - **S13.15.7 Eklentilerin tanıtımı:** `connect.ayinedar.org`; en son, dizin kararlarından sonra; risalemcp.com'dan yönlendirme (favicon ve
    MCP adresleri yerinde).

**S13.17. Öbür kütüphaneler sohbette** (bitti ve yayında, 2026-11-26; kapandı 2026-11-27, kullanıcının kararı:
"S13.17 bitti, onu kapat"; "Kalan" (c) daha çok deneme turu ayrı adım olarak açılmadı). "Sıradaki"den değiştirilmeden:

- S13.17 **Öbür kütüphaneler sohbette** (eski S13 (11) ve S13.12'nin 2. aşaması): hadis, tefsir, klasik; erişim kararı
  (süreç içi kopya ya da uzak çağrı, ölçerek), alan adlı işaret (`[[tefsir:…]]`) ve çok alanlı denetim, âyet çalışması
  kipi. Maliyet uyarısı: soru başını birkaç katına çıkarabilir, tavanlar buna göre tartılır. Hassas alanlarda (hadis,
  fıkıh) serbest yorum alanı daraltılır, cevap ağırlıkla alıntı ve künye (S13.14'ün kararı).
  Kullanıcının kararları (2026-11-26): S13.15'in adı beklenirken başlar, deneme haftasında yalnız yerelde; bütün
  eklentiler bir gün tek makinede durursa o makine 8 GB olmalı (4 GB eser eklendikçe az kalır); altyapı bitince
  önceki gibi çeşitli sorularla deneme turları (`sohbet dene`, `tests/golden/sohbet_konusmalar/`).
  **S13.17.1 erişim ölçümü (2026-11-26):** `data/interim/sohbet/erisim-olcumu-20261126.md`. Süreç içi tefsir ≈1,26 GB
  (anlamsal dizin 1,1 GB, ≈650 MB'ı Python yapıları), hepsi ≈2,3 GB ve MCP servisleriyle iki kez; makineler arası MCP
  çağrısı ≈90 ms ekler (ortanca 139 ms), hadis 127.0.0.1'den 16 ms. Öneri: Risale süreç içi, öbürleri MCP istemcisiyle,
  sınırsız ve girdisiz kayıtlı iç anahtarla (açık kipin ortak sınırını yemesin).
  **Kullanıcının kararları (2026-11-26):** öneri onaylandı; hangi kütüphanelerin açık olduğunu okuyucu seçer, ama
  altyapı dördünün her soruda açık olmasına da uygun kurulur (seçim bir ayar; varsayılan yalnız Risale).
  **S13.17.2 altyapı (2026-11-26, yerelde; deneme bitene kadar yayına gitmez):** MCP sunucularına iç erişim adresi
  (`auth internal-key`: sınırsız, girdisiz kayıt, `(iç:sohbet)`); `kutuphaneler.py` (MCP istemcisi ya da süreç içi,
  önekli araçlar, `cite`/`get_ayah` gitmez, sonuç 40 bin karakterde kesilir); işaret `[[tefsir:…]]`, denetim o
  kütüphanenin `cite`'ı, Kaynaklar tek liste, metin paneli öbür kütüphanenin metnini de açar; sayfada "Kütüphaneler:"
  seçicisi (Risale hep açık, seçim tarayıcıda, turda `libraries`); tercüme satırı alıntıya karışmaz, öbür kütüphanenin
  paragrafındaki tırnaklı tercüme Risale'de aranmaz. **Tur 7** (`tests/golden/sohbet_konusmalar/tur-07.txt`, 11
  konuşma, 14 cevap, 0,11 $, cevap başı ≈0,008 $): tuzaklarda doğru (hadiste hüküm yok, fıkıhta "hangisi doğru"ya karar
  yok, Beyzâvî–Zemahşerî ilişkisi "kayıtlı değil, yorum"), kütüphaneler açıkken yalnız Risale'lik soru sapmadı; ⚠
  uyarıları 20'den fazladan 3–5'e indi. **Kalan:** (a) yayın: iç anahtarlar ve `SOHBET_*_URL` (deneme bitince,
  ≈2026-12-02; kullanıcının kararıyla öne alındı, aşağıda), (b) âyet çalışması kipi (yapıldı, aşağıda), (c) daha çok
  deneme turu, (d) kalan ⚠'lerin metni öbür kütüphane açıkken
  "eserlerde" yerine "Risale'de bu sözlerle bulunamadı; tercüme ya da özet olabilir" (kullanıcının kararı, yapıldı).
  **Yayında (2026-11-26, kullanıcının kararı: deneme haftası beklenmez, kütüphaneler okuyucu açmadıkça kapalı):** üç
  MCP sunucusuna iç anahtar (`internal-key --new sohbet`), adresler git dışı `.env.sunucu`'da (`deploy.sh` gönderir),
  tefsir ve klasik `tefsir-sunucu.sh gonder --kod` ile (yalnız kod). Canlıda sunucunun içinden üç kütüphane uzak
  çağrıyla açılıyor; kader sorusu (üç kütüphane) 35 sn, 0,009 $.
  **S13.17.3 âyet çalışması kipi (2026-11-26, yayında):** kullanıcının kararları: sabit tefsir yok, âyeti en kapsamlı
  işleyenler önce (birimin bu âyete düşen kelime payı; `get_outline` kökte `words` verir: cümle sayısı Râzî'de
  yanıltıyordu); hadis yalnız okuyucu açarsa, kapalıyken ve hadis önemliyse model "Hadis kütüphanesini açın" der. Kip
  tefsiri kendiliğinden açar; `verse_file` (`ayet_dosyasi.py`) dosyayı sunucuda kurar (âyet ve Vakıf meali, Risale'nin
  bağları güçlüler önce ve alıntı yerleri, tefsir birimleri vefat sırasıyla ve `read_first`); cevaptan sonra kapalı ek
  "Âyetin okunmayan öbür yerleri". Konuşmada işareti geçen kütüphane takip sorularında açık kalır. **Tur 8** (7
  konuşma, 8 cevap, 0,06 $; cevap başı ≈0,008 $): sıra doğru (âyet, Risale, tefsirler, yorum), bağı olmayan âyette
  (Bakara 282) "bağ yok" dedi, hadis notu yerinde; canlıda Yâsîn 82 32 sn. Gözlenen: Haiku bir cevapta tefsirleri
  okuduğu sırayla dizdi (talimat sıkılaştırıldı), Râzî'nin Fâtiha birimleri küçük görünüyor (B3, kayan birimler).

**Risale'si az birimlere göz atmak (eski D5.2)** (bitti, 2026-11-27): kullanıcı baktı, dersler ve nazımlar
uygundu; kuyruk sürüyor. "Sıradaki"deki kaydı:

- **Risale'si az birimlere göz atmak** (eski D5.2; isteğe bağlı, bir kez, kullanıcının işi): bir kıssa birimi
  (İsrâiloğulları, 40–74; yazıldı) ve bir ahkâm birimi (178–283; Aralık'a doğru). Sebep: sınanan birimlerin hepsi
  Risale'ce zengindi; Bakara 34–283'te âyetlerin ≈%78'inde Risale'den doğrudan alıntı yok. Okuma değil, göz atmak
  yetebilir (2026-11-21).

**S13.15.5. Okuma platformu ve masanın taşınması** (bitti ve yayında, 2026-11-27; kullanıcının kararları: çerez alan
adına bağlı, masa hesabı iki yere ayrı girer; ad ve simge şimdi).

- **Adresler:** okuma platformu `read.ayinedar.org` (diskte `/var/www/ozel/taslak/oku/`), ar-ge masası
  `lab.ayinedar.org` (`/var/www/ozel/taslak/`). Disk düzeni değişmedi: D5 sunucusunun kısıtlı gönderme anahtarı
  (`rrsync -wo /var/www/ozel/taslak`), setgid ve `deploy.sh`'in hedefleri aynı kaldı.
- **Giriş servisi** (`site_auth.py`): iki bölümde aynı kısa yollar (`/giris`, `/cikis`, `/ben`, `/api/…`; davet
  `read.ayinedar.org/davet/<jeton>`); bölümü Caddy'nin `X-Bolum` başlığı söyler (üstüne yazılır; yoksa `lab`, dar olan).
  Masaya yalnız `masa` kapsamı girer: `oku` hesabı masada giriş yapamaz (403, platformun adresi), başka yerden taşınan
  çerezle masaya gelirse platforma yönlenir. Çerez `Domain`sız: chat. ve köke gitmez. Giriş sayfaları Âyinedâr adı ve
  simgesiyle, alt satır çatıya ve gizlilik politikasına. `masa.py` ve `yazilar.py`'nin API'si `/api/`.
- **Caddy:** `read.` ve `lab.` blokları (HSTS, `noindex`); Âyinedâr simgeleri girişsiz; masada olmayan ama sitede olan
  dosya (yazı önizlemesinin stil ve resimleri) `/var/www/risalemcp`'den, girişsiz (zaten herkese açık). **Eski
  sayfalar:** önceden üretilmiş D5, tur ve fark sayfaları `/taslak/api/…` ve `/taslak/ben`'i çağırır; iki alan adında
  da `/taslak` öneki atılır, yeniden üretmek gerekmedi. `risalemcp.com/oku/*` ve `/taslak/*` 308 ile aynı yola
  (`/oku/davet/<jeton>` → `read.ayinedar.org/davet/<jeton>`: 23 Kasım'da verilen üç açık davet çalışır);
  `isarat-usulu` yönlendirmeleri önde kaldı.
- **Şablonlar ve betikler:** platform (`oku-app.html`: API, `/ben`, masa düğmesi, kopyalama damgası "Âyinedâr …
  (read.ayinedar.org)", başlık "Kur'ân Taslakları · Âyinedâr", simge), masa (`d1-masa-sablon.html`: hesap adı artık
  `location.pathname` yerine sitede açılınca alınır), masanın girişi, tur ve fark şablonları, yazı düzenleyici, önizleme
  (`site-uret.py` `PREVIEW_URL = "/onizleme"`), D5 iletileri ve ntfy bağlantıları (`lab.ayinedar.org/d5.html`),
  `masa-gorev.py` (makine istemcisi: POST 308'i izlemez, adresi değişti), `taslak-gonder.sh`, Word damgası
  (`docx_yaz.py`), gizlilik sayfaları (iki dilde; tarih 27 Kasım 2026).
- **Yayın:** `deploy.sh --code` (araç çıktısında fark yok, `yayin-20261127-011658`), Caddy yeniden yüklendi;
  `taslak-sunucu.sh gonder` (kuyruk sürüyor: kod sıradaki birimin başında geçer; o zamana kadar sunucunun ürettiği
  sayfalar eski yolları kullanır, önek atıldığı için çalışır; yalnız masada hesabın adı görünmez). **Deneme:** curl
  ile kapılar ve yönlendirmeler; geçici `oku` hesabıyla platforma giriş (303, çerez `read.ayinedar.org`'un), `/ben`,
  eski API yolu, masada giriş reddi (403), taşınan çerezle masa → platform, çıkış; hesap silindi. Açık oturumlar
  (eski alan adının çerezi) bir kez yeniden giriş ister.

**S13.15.4. Sohbetin `chat.ayinedar.org`'a taşınması** (bitti ve yayında, 2026-11-26 – 2026-11-27; alt adımlar
kullanıcının onayıyla, taşınma deneme bitmeden: "site neredeyse kimseyle paylaşılmadı").

- **(1) E-posta.** Scaleway'de `ayinedar.org` gönderici alanı (API ile açıldı, alan kimliği `57070baa…`); kullanıcı
  Cloudflare'de Email Routing'i açtı (`destek@ayinedar.org` → kendi adresi), SPF'i tek kayıtta birleştirdi
  (`include:_spf.mx.cloudflare.net include:_spf.tem.scaleway.com ~all`), DKIM ve DMARC (`p=none`) ekledi; Scaleway'in
  önerdiği "blackhole" MX eklenmedi (MX'ler yönlendirmenin). Kayıtlar `data/interim/ayinedar-eposta-kayitlari.txt`.
  Kodda destek adresi `SOHBET_DESTEK` (sayfaların iletişim satırı) ve e-postaya Reply-To. **Proton denemeleri:**
  `noreply@ayinedar.org` → `destek@ayinedar.org` reddedildi (`554 5.7.1 rejected by rspamd filter`, Cloudflare
  `521 5.3.0`); ayrıştırma: eski gönderici → yeni yönlendirme ve yeni gönderici → eski yönlendirme geçti, gerçek kod
  e-postası bağlantıyla reddedildi, bağlantısız geçti: **yeni alan adına bağlantı süzgece takılıyor**; kod
  e-postasından bağlantı kaldırıldı (okuyucu kodu açık sayfaya yazar; bağlantısız kod e-postası oltalamaya da kapalı).
  mail-tester.com 10/10 (SPF, DKIM, DMARC geçer). Yönlendirmeyle gelen üç ileti (eski göndericininki de) Proton'da
  spam'e düştü: sebep yönlendirme; doğrudan gönderilen kod kullanıcıya ulaştı.
- **(2) Ad ve adres.** Çatı bağlantısı `SOHBET_CATI`; politika sayfalarındaki kökten bağlantılar risalemcp.com'a tam
  adres; adın geçtiği cümleler `{{NAME}}`; simgeler (`favicon.ico`, `icon-kucuk.svg`, `apple-touch-icon.png`; kopyalarını
  `scripts/ikon-ayinedar.sh` yazar); ad yazısı Literata 500, optik boy 24, yalnız Türkçe Latin harfleri (10 KB,
  `scripts/literata-alt.py`; kaynak google/fonts, OFL; telif ve lisans satırları dosyada).
- **(3) PWA.** `manifest.webmanifest`, `sw.js` (yalnız sayfa açılışı; bağlantı yoksa `/cevrimdisi`; cevap, metin ve
  API önbelleğe alınmaz), simgeler (192, 512, maskable), Ayarlar › Görünüm'de "Ana ekrana ekleyin" (Android/Chrome'da
  tarayıcının penceresi, iPhone'da Safari'nin yolu).
- **(4) Hakkında.** `/hakkinda` (`sohbet_assets/hakkinda.html`, girişsiz): ilk taslak ayrıntılı ve Risale'ye
  odaklıydı; kullanıcının isteğiyle kısa, genel ve bütün kütüphaneleri kapsayan metin: nedir, neye dayanır, sınırları,
  "Bir araştırma aracı" (23–24 Kasım 2026 İstanbul toplantısının sonuç bildirgesinin 7. maddesi, kullanıcının verdiği
  metinden aynen), kimin. Bağlantıları: hesap ve belge sayfalarının altı, girişsiz tanıtım, Ayarlar › Belgeler.
- **(5) Yayın** (2026-11-27 00.36, `scripts/deploy.sh --code`; araç çıktısında fark yok, `yayin-20261127-003609`).
  Caddy: `chat.ayinedar.org` → 127.0.0.1:8010 (HSTS, `noindex`, tamponsuz), `risalemcp.com/sohbet/*` `handle_path` ile
  308 aynı yola (sorgu dizgisi dahil). Ayarlar servis biriminde (`SOHBET_PREFIX=/` …); koddaki varsayılan yerel
  geliştirmenin `/sohbet/` düzeni kalır (testler ve arayüz denemesi değişmedi). Güvenlik başlıkları uygulamada
  (`sohbet_hesap.SECURITY`, saf ASGI ara katmanı: SSE'yi tamponlamaz): CSP `script-src 'self'` (satır içi betik yok),
  stil `'unsafe-inline'` (hesap sayfalarının `<style>`'ı), `frame-ancestors 'none'`. Adla 404 (API'de JSON). Paylaşım
  kartı (Open Graph; `site-ayinedar/paylasim-sohbet.html` → `paylasim.jpg`, 47 KB, `scripts/paylasim-ayinedar.py`).
  `POLICY_DATE` 27 Kasım 2026. Gönderimden önce Caddyfile sunucuda ayrıca doğrulandı (betik geçersiz dosyada sessizce
  eskide kalır). Arayüz denemesi yeni düzende 86/86 (betik artık konsol hatalarını da topluyor: CSP ihlalleri). 3
  hesap, geçmiş saklamayı kapatan yok (kaybolan konuşma yok), açık oturumlar bir kez yeniden giriş. **Yapılmayan:**
  `__Host-` çerez öneki (çerez adı 56 yerde; kazancı yalnız kendi alt alan adlarımızın çerezi gölgelemesine karşı,
  çerez zaten alan adına bağlı, HttpOnly, Secure). Bilinen: kayıt sayfası HEAD isteğine 400 döner (eskiden de).
- **(6), (7)** kullanıcının denemesiyle: telefonda ve masaüstünde giriş, kod e-postası geldi; deneme kullanıcılarına
  yeni adresi kendisi gönderiyor.

**S13.16, B11, B10. Küçük açıklar** (2026-11-26; kullanıcı S13.15'in adını düşünürken; kararları aynı gün: "a
onaylıyorum, c onaylıyorum, d uygun, B11 biçim ve kapsam önerilerin uygun, B10 ek çıksın, deploy'ları sen yap").

- S13.16 **Sohbetin küçük açıkları.** (a) **Dil:** sohbet talimatına "dili belli olmayan soru (yalnız ad ya da terim,
  "Mevlânâ", "haşir") sayfanın diliyle, Türkçe cevaplanır" (MCP talimatı değişmedi). (b) **Lügat sesteşleri:**
  "sâika" (سائقه, sevk eden) "saîka/sâıka" (صاعقه, yıldırım) maddesine de bağlanıyordu. İlk deneme şapkanın yeriydi
  ("sâika" ↔ "saîka"): lügat şapkayı tutarsız yazdığı için ("ilahî" ↔ "İlâhiye") iki test düştü, bırakıldı. Asıl
  ayırıcı ünlüden sonraki ı/i: lügat ayınlı kelimeyi ı ile yazar ("sâıka", "vaız"), hemzeliyi i ile ("sâika", "vaiz").
  Kural (`lugat._gaps_agree`): maddenin yazılışları o yerde yalnız öbür harfi taşıyorsa metinle eşlenmez; "î" iki
  yana da sayılmaz. Etki: Türkçe metinde ünlü+ı/i taşıyan 1.685 kelime biçiminden 28'i (124 geçiş): sâika ve ekli
  biçimleri yalnız "saik", vâiz yalnız "vaiz" (vaız değil), "ictimaıye" yalnız "içtimaî", bir "menbai" yalnız
  "menba"; `lugat olc` ölçümü değişmedi. (c) **Parçalı alıntı** (`sohbet._repair`): "…" ile birleşen alıntının bir
  parçası işaretin cümlelerinde yoksa, öbürleri varsa, parça o cümlelerdeki en yakın karşılığıyla (harf düzeyinde
  benzerlik ≥0,7, metnin kendi sözleri) değişir, karşılığı yoksa "…" olur; parça cevapta aynen bulunamazsa onarılmaz,
  "doğrulanamadı" kalır. Gerçek örnek (S13.10 (C)): "tefekküre teşvik ettiği" → "tefekkür mesleğine teşvik ettiği".
  (d) **İşaretsiz tırnaklı söz** (`sohbet.unmarked_quotes`): dört kelime ve üstü, ardında (aynı cümlede) işaret
  olmayan tırnak ya da işaretsiz alıntı bloğu eserlerde aranır: bulunursa işaret alır (okunan yer önce); okunan bir
  cümlede çok yakın karşılığı varsa (≥0,8) metnin sözleriyle değişir ve işaret alır; bulunmazsa ardına "(⚠ eserlerde bu
  sözlerle bulunamadı)", söz silinmez. Nâşirin ve Vakıf'ın meali, bölüm başlığı ve bulunamayan Arapça dokunulmaz.
  S13.10'un örneği "Bazen bir saat tefekkür, bir sene ibadet hükmündedir" uyarı alır. Hızlı ölçüm (`olc --hizli`,
  `20261126-163959`): 8 soru, ortalama 28 sn, soru başı ≈0,007 $; (c) hiç gerekmedi, (d) 4 sözü kaynağına bağladı,
  2'sine uyarı koydu: biri modelin kendi yorumunu tırnağa koyması (doğru uyarı), öbürü "Ben filân reisin adıyla
  gezerim" (metin "ismiyle"): bunun üzerine yakın karşılık kuralı eklendi.
- B11 **Kaynakçada kaynak adı.** `cite`'ın kaynakça satırı kaynağın adıyla biter: "[1] Sözler › … › “…” (e-Risale)";
  ad eserin izin kaydından (`works.permission` → `permissions.SOURCE_LABELS`; yerel profilde risale.online ve
  rasaelalnour.com da), sonuçta `source_name`. Dört eklenti: Risale, tefsir ve klasik aynı `CitationChecker`'la (tefsir
  ve klasikte "(OpenITI)"), hadis `cite_reports`'ta kitabın kaynak kaydından (`permissions.book_source_label`, hepsi
  OpenITI). Talimat değişmedi ("which the bibliography does" artık doğru), eklenti (plugin) yeniden üretilmedi. Atıf
  denetimi (`citations.check`) eki sorunsuz okur.
- B10 **Arapça Mesnevî'nin muhakkik eki.** `risaleoku_app.ENDS_AT`'a Mesnevî: ek "img alt" satırıyla başlar, oradan
  sonrası alınmaz, kökte not (`ENDS_NOTE`). `el-mesnevi-el-arabi/nur/tetimme` c064–c128 silindi (65 cümle, kayma yok,
  `--accept-id-changes`; 63 cümle kaldı, vektörleri yeniden çıkarıldı). İşârât'ın Arapçasındaki resim satırı
  (`isaratul-icaz-arabi/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-07/c018`) **yerinde kaldı:**
  atılınca bölümün 197 cümlesi kayıyordu ve D1 taslakları (`data/d1/bolme/`, `provalar/47-48/`) c019–c045'e atıf
  veriyor. Öbür risaleoku eserlerinde "img alt" yalnız henüz katalogda olmayan Arapça Tarihçe'de var (20; E8'de
  bakılır). Kurulum notu: `build` 25 dakikalık `timeout`'a takıldı (hadis profili yarıda; `hadis.db` etkilenmedi);
  kalan adımlar elle (`local_only`, `embeddings build`).
- **Yayında (2026-11-26):** Risale ve hadis `DEPLOY_EXPECT="cite list_works read_section risale://works"
  HADIS_EXPECT="cite" scripts/deploy.sh --hadis` (genel sürüm `2026-11-26`, `yayin-20261126-171957`: 10 çağrıda
  beklenen fark; hadis 3 çağrıda; sohbet de yeniden başladı). Tefsir ve klasik `TEFSIR_EXPECT="cite get_outline
  get_passage read_section"` (`tefsir-yayin-20261126-172609`, `klasik-yayin-20261126-172934`): ilk deneme yalnız
  `cite` ile durdu, çünkü iki sunucu S13.12 ve S13.14'ten beri gönderilmemişti; ortak kütüphanenin `profile`,
  `coverage`, `of_section` alanları ("sonraki gönderimde gider", S13.14) bu gönderimle gitti. Farkların hepsi yeni
  alan ya da "(OpenITI)" ekidir, metin değişmedi. Canlıda denendi: `cite` "(e-Risale)", "(risaleoku.com)",
  "(OpenITI)"; `lookup_word` "sâika" yalnız "sevk eden".

**S13.1–S13.14. Sohbetin ilk geliştirme adımları** (bitti ve yayında, 2026-11-25 – 2026-11-26; S13.14 kullanıcının kararıyla durduruldu). S13'ün ana kaydı ve alt adımları, "Sıradaki"den değiştirilmeden (2026-11-26, kullanıcının kararı: S13 genel ad olarak sıradan kalktı, açık maddeleri S13.15–S13.21 diye sıraya girdi):

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
  - S13.13 **Haşir konuşmasının bulguları: tarama kipinin ilk gerçek kullanımı** (2026-11-26; kullanıcının konuşması
    `cKtFoJwL-6hnvx7G`, üç tur: "haşrin irili ufaklı geçtiği her yeri bul ve say" (tarama), Dokuzuncu Şuâ ile 29. Söz'ün
    farkı (tarama kipi açık kalmış), Nokta'nın haşir kısmıyla karşılaştırma (serbest); kayıt sunucudan kullanıcının
    izniyle okundu, okunan yerler ve tarama genel veritabanında yeniden kuruldu). **İşleyen:** kip mekanik olarak doğru
    çalıştı (`survey` bir kez, `*`'lı terimlerle; altı aday okundu, eserlere göre gruplu, model kendi listesini yazmadı,
    sayfa adayları ekledi; S13.10 (B)'nin dar araması kalktı); bütün alıntılar doğru (`corrected` 0, doğrulanamayan
    yok), Vakıf ve telif tarihi yok, satır içi kısa alıntı işaretli; sınırlar dürüst ("tam bir döküm değil",
    "Okuyamadıklarım"). **Sunucu ve tasarım açıkları:** (1) **Sayı:** okuyucu "say" dedi, cevap "647 aday yer" dedi:
    `total_places` kelime, başlık ve anlam adaylarının toplamıdır, sayım değildir. Gerçek sayı: "haşir/haşr" 589
    cümlede, 133 risalede. (2) **ş = s yanlış eşleşmesi:** `haşr*` "hasr", "hasr-ı", "hasret", "hasretmek",
    `haşir*` "hâsir", "hasır" da tutuyor: 737 cümlenin 148'i (%20). Lügattaki harf biçimi (`Form`) kuralı gibi bir
    süzgeç ister. (3) **"Öbür yerler" 15'le sınırlı:** "her yer" isteğinde Yirminci Mektub (Onuncu Kelime; 29. Söz
    c010 haşir için oraya gönderir), Mektubat 28, Lem'alar 30 listede yok; Meyve ile Tarihçe'deki kopyası iki ayrı aday.
    (4) **Kip açık kalıyor:** 2. tur bir karşılaştırma sorusuydu, kip "tarama" kaldı: ikinci `survey`, cevaba
    gereksiz bir aday listesi; listede 1. turda okunup alıntılanan yerler (Nokta, Muhakemat, Kastamonu 69) "okunmadı"
    diye duruyor. **Okuma hataları** (Haiku; S13.9 (B), S13.10 (D) örüntüsü): (5) merkez seçiminde İşârât › Bakara 4 ›
    Delâil-i Haşr (3. aday, başlığı eşleşiyor) yerine 11 cümlelik Kastamonu 69 okundu; okunan Nokta'nın Medhal'i
    (c003, "İşârâtü'l-İ'câz'da yazmıştım") gönderme olduğu hâlde İşârât'a gidilmedi. (6) **Şuâ'nın kendi çerçevesi
    tersine okundu:** "Şuâ kendisini Onuncu Söz ile 29. Söz'ün arasına yerleştirir" (`sualar/9/c007`); metin ise
    Muhâkemât'ın vaad ettiği iki âyetten birincisinin (Rûm 30:50) tefsiri Onuncu ve 29. Söz'dür, bu Şuâ ikincisinindir
    diyor (c003–c010; Muhâkemât `makale-03/maksad-03/maksad-02` aynı sözü alıntılar). Şuâ'nın yalnız Mukaddime'si
    yazılmış, "Dokuz Âlî Makam" yazılmamıştır (Kastamonu 125 c006, c022; Barla 285 c013); 1. turda okunan Kastamonu 69
    c006 birinci makamın yerine Otuzuncu Lem'a'nın Dördüncü Remzi'ni koyar; Şuâ'nın alt başlığı "Onuncu Sözün Mühim
    Bir Zeyli". Hiçbiri söylenmedi; Kastamonu 125 2. turun aday listesindeydi. İkinci Nokta'nın 100 cümlesinden 26'sı
    okundu (`next_cursor` sürmedi, cevapta söylenmedi); onun bütün iman rükünlerinin şehâdeti olduğu (c001, c044,
    c083) "peygamberlik ve Kur'ân" diye daraltıldı. (7) **29. Söz–Nokta ilişkisi kaçtı ve tersine yorumlandı:** 2. turda
    okunan ve [7] diye alıntılanan 29. Söz c009 "Eski Said'in Nokta Risalesi'ndeki beyânâtı tarzında bahsedeceğiz"
    der; 3. turun Yorum'u "Nokta'nın dört temeli Söz'ün dizisinin bir özeti gibi" dedi. Söz'ün İkinci Maksad'ı Nokta'nın
    dört makamına esas esas karşılık gelir (Birinci Esas ↔ Dördüncü Makam, rûhun bekâsı; Üçüncü Esas'ta altı temsîl;
    Dördüncü Esas'ta Tekvîr ve İnfitâr). (8) **Okumadan hüküm:** yalnız İkinci Esas okunduğu hâlde "altı temsîl ve
    Tekvîr–İnfitâr Nokta'ya özgü, Söz'deki karşılığı daha kısa" dendi (yanlış); "Söz'ün on birinci medarı" (yok;
    Onuncu Medâr). **Çözüm adayları (karar yok):** (1)–(2) `survey` sayımı ayrı versin (kelimenin geçtiği cümle ve
    risale sayısı, harf biçimi süzgecinden sonra), "aday" toplamı sayı diye sunulmasın; (3) "her yer" isteğinde bütün
    kelime adayları açılır bir ek liste; Tarihçe'deki kopyalar asıllarıyla birleşsin; (4) tarama cevabından sonra kip
    serbeste dönsün ya da `survey` aynı konuda ikinci kez çalışmasın; "okunmadı" konuşmanın önceki okumalarını
    saysın; (5)–(8) talimatla kısmen: karşılaştırmada iki tarafın da karşılaştırılan bütün kısımları okunur, okunmayan
    kısım hakkında "özgü/yok/daha kısa" denmez; bölümün kendi hakkında söylediği (amaç, yer, hangi esere bağlandığı)
    önce okunur (karşılaştırma kipi, S13.12 aşama 3).
    **Kullanıcının kararı (2026-11-26):** (1), (3), (4) yapılsın; (2) kalsın (okuyucu İngilizce klavyeyle ş yerine s
    yazabilir; model sonuçlardan bağlama göre doğru seçtikçe). **Yapıldı:** (1) `dosya` `count` verir (kelimelerin
    geçtiği cümle ve yer, kopyalar bir kez), `total_places` yerine `candidates_total`; notta ve kipin talimatında "okuyucu
    sayı sorarsa sayfanın sayımı, aday toplamı sayı değildir". (3) `places`: kelimelerin geçtiği bütün yerler, sayılarıyla;
    modele gitmez (`sohbet.PAGE_ONLY`), cevabın sonuna kapalı ek olarak (`:::ek` → `<details class="ek">`, yalnız sayfada;
    geçmişe girmez). Kopyalar: Tarihçe'deki adayın kelime cümlelerinin %60'ı (ilk 8 kelimeyle; metin özeti, cümle farklı
    bölündüğünde tutmuyordu) Tarihçe dışında daha büyük bir adayda varsa asla katılır, "(Tarihçe-i Hayat'ta da)".
    Yalnız Tarihçe: genel kural Dokuzuncu Şuâ'yı Onuncu Söz'e (lâhikası), On Dokuzuncu Söz'ü Ondokuzuncu Mektub'a
    katıyordu. (4) Sayfa tarama cevabından sonra kipi serbeste döndürür (`sohbet dene` de: kip yalnız ilk soruda);
    "öbür yerler" bu cevapta ya da önceki turlarda okunan ve alıntılanan yerleri saymaz (`earlier_places`).
    `deploy.sh --sohbet` `dosya.py`, `kipler.py`, `sohbet_dene.py`'yi de sohbetin sayar. **Sınama:** testler (iki yeni),
    arayüz denemesi (kapalı ek, gerçek API ile tarama sorusu ve kipin dönüşü; hepsi geçti), haşir konuşması yeniden
    (`tur-06.txt` › `hasir`, Haiku ≈0,026 $): 1. cevap "194 yerde, 710 cümlede" dedi, sonda bütün yerler, Meyve
    Tarihçe'yle tek satır; 2. tur serbest kipte, `survey` ve liste yok; model Şuâ'yı Onuncu Söz'ün zeyli ve Rûm
    âyetlerinin tefsiri diye andı (önceki koşuda yoktu), dokuz makamın yazılmadığını yine bilmedi ("okumadım"); 3. turda
    okuma hataları sürüyor ("Söz'deki gibi altı soruyla ilerlemez", menba'a "mâden"). **Yeni bulgu:** arayüz denemesinde
    tek kelimelik tarama sorusuna ("Mevlânâ") İngilizce cevap: dil kuralı "son sorunun dili" diyor, ad tek başına dil
    belirtmez; tarama kipi tek kelimeli konuyu teşvik ediyor. Talimat önerisi (karar bekliyor): dili belli olmayan soru
    (yalnız ad ya da terim) Türkçe cevaplanır.
  - S13.14 **Okuma hataları: araştırma ve katmanlı plan** (kullanıcının sorusu, 2026-11-26: "okuma hataları
    yapısal ve sistemsel olarak çözülebilir mi?"; dinî metinde en küçük hata ciddidir). **Araştırma** (rapor
    `reports/Okuma hatalarını azaltma yöntemleri.md`, notları `research_notes/`, ikisi de git dışı): sıfırlanmaz,
    daraltılır. Satıcı araçları (Citations API, Check Grounding, Azure, AWS) uydurma alıntıyı hedefliyor, bizde o
    mekanik olarak çözülü; "doğru alıntı, yanlış okuma" için ölçülmüş azalma yayımlayan yok. Hukukta (Stanford: ticari
    araçlarda %17–33, Westlaw'ın hatalarının %61'i doğru getirilen metnin yanlış yorumu; Princeton: en zor tür içerik
    çarpıtma) ve İslâmî ürünlerde (IslamicEval, Ansari: "dayanak gerekli ama yeterli değil") aynı sonuç. Hatalarımız iki
    sınıf: sunucunun verisiyle kanıtlanabilenler (uydurma yapı, okunmayan yer hakkında hüküm, izlenmeyen gönderme,
    ilk sayfadan genelleme) kurala bağlanır; anlam hataları (ters okuma, çerçeve, temsil/hüküm, söyleyen) yalnız
    daralır; orada güvenin kaynağı şeffaflık (kapsam notu). Şablon sarmalama (Cursor tarzı) bir taşıyıcıdır: sunucunun
    hesapladığı olguyu ve sabit usulü taşıdığında yararlı, yeni yasak eklemek değil ("doğru ol" istemleri tıpta ters
    tepti). Model yükseltmek açık çare değil (Vectara'da Haiku 4.5 %9,8, Opus 5.5 %9,9). **Sıra** (kullanıcının onayı,
    2026-11-26; ilk taslaktan değişti: sohbete eklenen denetim eklentilere ulaşmaz, araç sonucu ikisine de ulaşır;
    ağır hatalar okunan metinde): (1) Türkçe ölçüm seti; (2) araç katmanında olgular; (3) sohbette kapsam notu; (4)
    karşılaştırma kipi (okuma planını sunucu kurar); (5) doğrulayıcı denemesi (yalnız ilişki ve karşılaştırma
    iddiaları, ölçümle); (6) cevap metnine kesin kurallar (ölçüm sık gösterirse). Fıkıh ve hadis gelince ehil insan
    denetimi; Diyanet'in 24 Kasım 2026 bildirgesi (7. madde: "araştırma aracı … fetva makamı olarak görülmemelidir")
    sayfanın dipnotu için dış dayanak.
    **(1)–(3) yapıldı (2026-11-26):** (1) `tests/golden/okuma_seti.json`: S13.7–S13.13'te elle bulunan hatalardan
    13 madde (olgular kanıt cümleleriyle, bilinen yanlış iddialar, okunması beklenen yerler); `okuma_olc.py`
    (`uv run --extra sohbet python -m risale_mcp.okuma_olc run | hakem <klasör> | karsilastir <a> <b>`): sohbetin
    koduyla sorar, son cevabı Sonnet hakeme verir (olgu: stated/partly/absent/contradicted; yanlış: present/absent;
    gerekçe Türkçe), okumayı mekanik sayar; koşu ≈0,07 $ sohbet + ≈0,10 $ hakem. (2) `pointers.py`: okunan
    cümlelerdeki göndermeler (gönderme fiili ve çözülen hedef birlikte: sıra sayılı Söz/Mektub/Lem'a/Şuâ ve
    Hâtime'si, eski adlar, risale adları, eser adları; tek kelimelik ad büyük harfle; külliyatta 748 cümle, örneklem
    temiz) `read_section` ve `get_passage`'ta `points_to`; `read_section`'da kısmi sayfaya `coverage`
    ("1–65 / 350" ve "next_cursor ile sürdür" notu), `get_passage`'ta `of_section`; bölüm künyesine
    `books/bolum_notlari.json` (bölümün kendi metninden anlaşılmayan olgular, kanıtlı; ilki Dokuzuncu Şuâ'nın
    yazılmamış dokuz makamı; metinde duran bilgi girmez, setin cevabını hazır vermesin diye). (3) sohbette her cevabın
    altında kapalı ek "Bu cevabın dayandığı okumalar": kısmen okunanlar (n/m cümle), cevabın dayandığı bölümlerden
    çıkıp bu konuşmada okunmayan göndermeler, okunmadan yalnız arama sonucundan dayanılanlar, okunanlar (yalnız
    sayfada, geçmişe girmez). **Ölçüm** (aynı set ve hakem; tek koşu gürültülü): önce 13,5/17 olgu, 2 ve 3 yanlış;
    sonra 14,5, 15 ve 14/17 olgu, 2, 2 ve 3 yanlış; okuma 12/12. Kazanç küçük ve gürültü içinde; en belirgini
    Dokuzuncu Şuâ maddesi (0,5 ve 1 → 1, 2 ve 1; dokuz makam bilgisi künyeden geliyor, bağımsız kanıt değil). Set
    büyük ölçüde doymuş: yeni maddeler (ve karşılaştırma kipi) gerekir. Maliyet ≈%10 arttı (daha çok okuma).
    Kapsam notu ilk koşuda gerçek bir durumu gösterdi: Sirâcü'n-Nur cevabında "okunmadan, yalnız arama sonucundan:
    İkinci Şuâ". Testler 781, arayüz denemesi 86 denetim. Araç çıktısı: `get_passage`, `read_section` değişir
    (`tool_snapshot` 21 çağrıda beklenen fark); deploy `--code`, `DEPLOY_EXPECT="get_passage read_section"`; tefsir ve
    klasik sunucularına sonraki gönderimde gider (`coverage`, `of_section`; gönderme yalnız Türkçe külliyatta).
    **Kullanıcının kararı (2026-11-26): durduruldu.** İlk üç adımın kazancı gürültü içinde kaldı; Haiku'nun okuma
    sınırı kabul edilir, zorlanmaz. Yapılanlar yayında kalır (`yayin-20261126-152749`, `--code`, 21 çağrıda beklenen
    fark): kapsam notu şeffaflık içindir, göndermeler ve okunan pay eklentilerdeki güçlü modellere de gider, ölçüm seti
    model ya da talimat değişince geriye gidişi görmek için durur. (4)–(6) dondu. Hassas alanlar (hadis, fıkıh)
    sohbete eklenince orada serbest yorum alanı daraltılır (cevap ağırlıkla alıntı ve künye); karar o gün.

**S12. Sohbet sayfası** (bitti ve yayında, 2026-11-25; deneme ayı 2026-11-25 – 2026-12-25, sonrası S13). "Sıradaki"deki kayıt (kararlar dahil):

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
    b8'de 2 işaret sunucuca taşındı, c13'te 1 doğrulanamayan, 1 silinen işaret. c13'ün doğrulanamayanı yanlış alarm:
    model cümle yerine bölüm kimliği yazmış (`[[sozler/33]]`), alıntı bölümün alt başlığı (S12.10'da talimata: kimlik
    yalnız cümlenindir; sık görülürse bölüm kimliği bölüm atfı olarak kabul edilir). İşaretsiz paragraf 26/40 (giriş,
    yorum ve b7'de işaretsiz temsil özeti dahil; ölçü kabadır).
  - S12.10 **Sohbete ayrı talimat** (kullanıcının kararı, 2026-11-25). `server.py`'nin Risale talimatı bloklara
    ayrılır (iş akışı, cevap kuralları, müellifin sözü olmayan katmanlar); MCP'nin metni bayt bayt aynı kalır (araç
    çıktısı kaydı denetler). Sohbetin talimatı kendi girişi, akışı ve cevap biçiminden (okuyucu kim, önce kısa cevap,
    sonra metin, sonra yorum; uzunluk; sade Türkçe; kapsam) ve **ortak katman bloğundan** kurulur; MCP'ye özgü
    kısımlar (bağdaştırıcılar arası numaralama, denetçi alanları, `cite`) çıkar. Kaynağa bağlılığın koruması ortak
    blokta kalır, kopya olmaz. S12.9'dan not: işaret yalnız cümle kimliğidir, bölüm kimliği değil (c13); özetlenen
    temsil ve "metnin söylediği" paragrafı da işaretlenir (b7'de işaretsiz kaldı).
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
    a1 ve a5'te birer eksik, k3'te kazanç: gürültü sınırında), 21 sn (aynı), toplam 0,125 $ (0,137), model turu yok;
    sunucu 3 bölüm işaretini sildi (bu ölçümden sonra bölüm atfı oldu), 1 alıntı doğrulanamadı (k4: Tarihçe'de lafız
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
    **Bitti (2026-11-25):** cevabın altında "Bu cevap işinize yaradı mı? 👍 👎"; seçince not (en çok 1.000 karakter) ve
    "Soruyu ve bu cevabı da gönder" kutusu (varsayılan kapalı; işaretlenirse okuyucunun gördüğü cevap ve Kaynaklar düz
    metin olarak gider). `sohbet.db` `feedback` (zaman, hesap, oy, not, soru, cevap, model); kişi başına günde 50;
    hesap silinince hesap, not, soru ve cevap silinir, oy kalır. Okuma `uv run --extra sohbet python -m
    risale_mcp.sohbet geri-bildirim [--days 7]`, `usage` 👍/👎 sayısını verir. Arayüz denemesine katıldı.
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
    **Koşular yapıldı (2026-11-25):** hızlı set koda girdi (`sohbet olc --hizli`, `QUICK`; döküm adı düşünme düzeyini
    taşır). Sonuçlar (8 soru; beklenen bölüm okundu, ortalama süre, soru başı gerçek maliyet): Haiku medium 12/14,
    23 sn, 0,0056 $; Haiku high 12/14, 49 sn, 0,0105 $, 2 doğrulanamayan alıntı; Sonnet 5.5 medium 7/14, 23 sn,
    0,070 $ (daha az araç çağırıyor: bölümleri arama sonucundan adlandırıp okumadan anıyor). Ölçüte göre (ayda 100 $)
    Haiku medium ayda ≈18.000 soruya, Sonnet ≈1.400'e yeter. **Karar (kullanıcı, 2026-11-25): Haiku 5.5 medium**
    (bugünkü ayar, değişiklik gerekmedi). Yan yana sayfa `https://risalemcp.com/taslak/s12-modeller.html` (girişli). Değişirse servis ortamında
    `SOHBET_MODEL`, `SOHBET_EFFORT`.
  - S12.4 **Bütçe ve kota:** kişi başına günlük soru sınırı (başlangıç 10), servis düzeyinde günlük ve aylık dolar
    tavanı (100 $; aşılınca "bugünlük doldu"), Console tavanı yedek. Maliyet her cevabın `usage`'ından hesaplanır.
    **Harcama uyarısı:** günlük maliyet bir eşiği geçince kullanıcıya haber (ntfy düzeni hazır). Açılıştan önce hazır
    olmalı (davet yok; adres bir paylaşımla hızla yayılabilir). **Sayılar (kullanıcının kararı, 2026-11-25):** servis
    günde 5 $ (dolunca sayfa herkese "bugünlük doldu" der), ayda 100 $; günlük harcama 2 $'ı geçince ntfy bildirimi.
    **Bitti (2026-11-25):** `sohbet.Limits` (ayar `SOHBET_GUNLUK_SORU`, `SOHBET_GUNLUK_BUTCE`, `SOHBET_AYLIK_BUTCE`,
    `SOHBET_UYARI`); gün ve ay İstanbul saatiyle, maliyet `usage`'dan. Soru öncesi `refusal`: aylık tavan, günlük tavan,
    kişinin günlük hakkı (429 ve okuyucuya açık ileti). Her sorudan sonra aşılan eşik bir kez bildirilir (`alerts`:
    günlük 2 $, günlük tavan, aylık tavanın %80'i ve tamamı); ntfy konusu `SOHBET_NTFY` ya da `data/sohbet-ntfy`
    (git'e girmez; deploy'da açılır), gönderim sohbeti bekletmez. Okuyucuya kalan hakkı 3 ve altına inince
    gösterilir. `sohbet usage` bugünkü ve bu ayki harcamayı verir. Console'daki aylık tavan yedek.
  - S12.5 **API'nin açtığı fazladan imkânlar** (kullanıcının kararı, 2026-11-25: on madde). İlk sürümün üç maddesi
    S12.3'te yapıldı: Kaynaklar'ı sunucu kurar, tutmayan alıntı (S12.9 ile sunucu düzeltir), alıntıya dokununca metin.
    Kalan maddeler, havuz ve S12.8 (ad ve alan adı) **S13'e taşındı** (kullanıcının kararı, 2026-11-25). S12.8'in
    taşınabilirlik kuralı S12'de de geçerlidir: yol öneki, alan adı, ad ve gönderen ayardandır, sayfada sabit adres yok.
  - S12.6 **Gizlilik ve şartlar:** gizlilik politikası (soruların Anthropic'e gitmesi, e-posta servisi, saklanan ve
    saklanmayan, geri bildirim ve onayla gönderilen soru-cevap, konuşmanın tarayıcıda durması), kullanım şartları (yapay zekâ cevabıdır, tefsir ve fetva değildir), `en/` karşılıkları.
    Önce taslak: kullanıcı okuyup düzeltir, sonra deploy'la çıkar (kullanıcının kararı, 2026-11-25).
    Saklama süreleri koda girdi: kullanım satırı 90 gün, geri bildirim bir yıl. **Ayrı sayfalar (kullanıcının kararı,
    2026-11-25):** sitenin ana gizlilik ve şartlar sayfalarına dokunulmaz (eklentilerin dizin başvurularında
    gösterildiler; sohbetin verisi oraya girerse eklentinin özelliği sanılabilir). Sohbetin kendi sayfaları servisin
    içinde, girişsiz: `/sohbet/gizlilik`, `/sohbet/sartlar`, `/sohbet/en/privacy`, `/sohbet/en/terms`
    (`sohbet_assets/{gizlilik,sartlar,en-privacy,en-terms}.html`, `sohbet_hesap.DOCS`, tarih `POLICY_DATE`); hesap
    sayfaları ve sohbetin alt satırı bunlara bağlanır. Sohbet kendi alan adına taşınınca sayfalar da onunla gider. İlk
    taslak (`docs/s12-gizlilik-taslak.md`) kaldırıldı. Kullanıcı okudu, onayladı; **yayında** (2026-11-25,
    `deploy.sh --code`, araç çıktısında 0 fark, `yayin-20261125-190324`).
  - S12.7 **Deneme ayı:** başlangıç tarihi açılışta yazılır. Ölçüler: kayıtlı ve etkin kullanıcı, günlük soru, soru başı
    gerçek maliyet, atıf denetiminin geçme oranı, 👍/👎 (not isteğe bağlı, kullanıcının onayıyla saklanır). Haftalık
    rapor; ay sonunda sürdürme kararı (eşiği açılıştan önce kullanıcıyla yazılır). Duyuru yok (kullanıcının kararı,
    2026-11-25: adres bilinmiyor, bilen kullanır); Yenilikler yazısı S13'te. **Deploy ve açılış (kullanıcının kararı,
    2026-11-25):** testler ve 29 soru geçince deploy kullanıcıya sormadan yapılır (adres duyurulmadığı için açılış
    sayılmaz; telefon görünümü önce Chrome'da telefon genişliğinde denenir); kullanıcı kendi telefonunda baştan sona
    dener, onaylarsa deneme ayı o gün başlar. **Başarı ölçütü (kullanıcının kararı, 2026-11-25):** ay içinde en az
    10 ayrı hesap açılıp sohbet ederse ve genel olarak olumsuz geri bildirim yoksa (kullanıcıya söylenen ya da çok
    sayıda 👎) başarılı sayılır. 👍/👎 ölçüt değil, yan bilgidir; "etkin kullanıcı" ölçüt değildir.
    **Deploy edildi (2026-11-25, `scripts/deploy.sh --code`, araç çıktısında 0 fark, `yayin-20261125-164823`):**
    `https://risalemcp.com/sohbet/` (Caddy: tamponsuz, sıkıştırmasız, `noindex`), servis `risale-sohbet` (127.0.0.1:8010,
    model Haiku 5.5 medium), `.env`'e sohbet anahtarları (deploy artık `--code`'da da anahtar satırlarını yazar), ntfy
    konusu `data/sohbet-ntfy` (sunucuda; adı kullanıcıya verildi). Sunucuda hesapsız deneme (`sohbet sor`) geçti, 12 sn,
    0,002 $. Gizlilik ve şartlar (S12.6) onaylanıp yayımlandı. **Kullanıcı telefonda
    baştan sona denedi ve onayladı; deneme ayı başladı: 2026-11-25 – 2026-12-25.** ntfy konusuna telefonda abone oldu.
    Haftalık rapor sunucuda `sohbet usage` ve `sohbet geri-bildirim --days 7` ile; ay sonunda başarı ölçütüne göre
    sürdürme kararı, sonra S13.

**E6.1. Elmalılı'nın kaynak adayları** (bitti, 2026-11-23).
Adaylar: (A) archive.org `ElmaliliKuranTefsiri`: 114 sûre
PDF'i, "Mürşit 3.2"den (2015), sadeleştirilmemiş Latin harfli metin, Eser Neşriyat 1979 (3. baskı) sayfa işaretleri
("Sh:»152"), âyet grubu → "Meali Şerifi" → âyet numaralı izah; telif notu yok, lisans alanı boş; Arapça eski bir
yazı tipinin (`Arapca3`) glif kodlarıyla, çözülmesi gerekir (Kur'ân alıntılarıyla eşleme tablosu çıkarılabilir;
denenmedi). (B) islamilimleri.com "Elmalılı - Orijinal": aynı metin HTML'de, Arapçası "........" ile silinmiş;
telif notu yok. (C) Türkiye Yazma Eserler Kurumu'nun tenkitli neşri (Köksal, Kaya; ekitap.yek.gov.tr PDF'leri,
Fikriyat da dağıtıyor): en iyi metin (Unicode Arapça, 1935 baskısının sayfaları), ama "Her hakkı mahfuzdur": kurala
göre alınmaz, ancak izin istenirse. Elenenler: archive.org'daki öbür takımlar (Azim, Yenda: sadeleştirilmiş;
"(original)" kopyası kaldırılmış), kuranikerim.com (sadeleştirilmiş, kapalı), acikkuran ve kuran.gen.tr (yalnız
meal), Osmanlıca 1935 taramaları (metin değil).
Kurum'un şartları: ticari olmayan kullanıma izin veren yazılı bir hüküm bulunamadı. Bulunanlar:
PDF künyesi "izni olmaksızın tümüyle veya kısmen, hiçbir yolla ve hiçbir ortamda yayımlanamaz ve çoğaltılamaz";
e-kitap sitesinin alt bilgisi "Tüm Hakları Saklıdır"; PDF'leri açan duyuru (yek.gov.tr, n_id=114) "filigranlı pdf
… şahsî bilgisayarlara", amaç okuma ve referans; Çeviri ve Yayım Yönetmeliği elektronik yayını "sadece okunabilmesi
amacıyla" diye tanımlar, hazırlayanlar çoğaltma ve umuma iletim haklarını Başkanlığa devreder, Başkanlık üçüncü
kişilere kullandırabilir. Kullanıcının bildiği izin (ticari değilse ve metin başka yerde kendi adımıza
yayımlanmazsa) yazılı değilse yazılı teyit gerekir.
Kullanıcının elinde belge yok: teyit e-postası (`docs/yek-izin-epostasi.md`, Çeviri ve Yayım Daire Başkanlığı'na) gönderildi
(2026-11-23; "Bekleyen"). Kullanıcının kararı (2026-11-23): ekleme (E6.2) Aralık'taki tefsir kurulumunda B3 ile kalır;
koddan bakıldı: eser eklemek D5'i etkilemez (kuyruk taslak sunucusundaki kendi kopyasını okur, `taslak-sunucu.sh veri`
elle yeniler; yeni eser var olan kimlikleri değiştirmez), ama bağlar, vektörler ve deploy bir kez yapılsın diye
birlikte. Kaynak: izin gelirse C, gelmezse A (Arapçanın çözülmesi ayrı iş).

**S11. Site yazılarını web'de düzenlemek** (bitti ve yayında, 2026-11-23; kullanıcının kararları: birinci yol, yani
aslı taslak süresince sunucuda, yayımlama yerelde; yalnız kendisi düzenler; Markdown yeter; telefona da uysun. Aynı
gün önce masanın girişine Okumalar › Yazı taslakları kondu, `liste.json`):
- **Sunucu** (`yazilar.py`, giriş servisinin içinde; `/taslak/api/yazi`): her "Kaydet" `data/yazilar.db`'de yeni
  sürümdür (silinmez); sürüm başladığı depo metninin özetini (`taban`) taşır. Düzenleyici web sürümünü ya da depodaki
  dosyayı açar; depo web düzeltmeleri sürerken başka türlü değiştiyse çakışma uyarısı, iki metin, seçim. Yalnız taslak
  yazı; yetki `yazilar izin <e-posta>` (sunucuda risale kullanıcısıyla). Görünüş sitedeki programla
  (`site-uret.py preview_html`; `parse_post` metinden okur).
- **Düzenleyici** (`scripts/yazi-duzenle.html` → önizleme klasöründe `duzenle.html`): solda Markdown, sağda görünüş
  (yazdıkça, 0,7 sn sonra), Kaydet ve Ctrl+S, sürüm listesinden geri dönme, kaydedilmemiş metin tarayıcıda yedek,
  sayfadan çıkarken uyarı; 900 pikselin altında "Metin | Görünüş" sekmeleri, 16 piksel yazı (telefon yakınlaştırmasın).
- **Yerel** (`site-uret.py cek`): SSH ile `yazilar disa`; yerel dosya web sürümlerinin tabanı ya da onlardan biriyse
  ileri sarar ve commit eder, değilse `<ad>.web.md` yazıp durur. `yayinla`, `zamanla` ve zamanlı yayın (`zamanli`) önce
  bunu yapar; sunucuya ulaşılamazsa durur (zamanlı yayın masaüstüne haber verir).
- Testler `tests/test_yazilar.py` (yetki, sürümler, depo yetişince taban, çakışma, yayımlanmış ve kötü adlar,
  görünüş). Yerelde tarayıcıyla denendi (geniş ve 390 piksel).

**A4. Lügat** (bitti ve yayında, 2026-11-23; kullanıcının kararları 2026-11-22 ve 2026-11-23: atıf "risaleoku.com
lügatı", kaynağı risaleoku'ya sorulmaz; platformda bütün Türkçe metinde; yayın ve Yenilikler taslağı izni):
- **Kaynak:** risaleoku kataloğunun `dictionary`/`tr` kaydı, sürüm 41, 62 dosya (harf başına `x.txt` "madde=anlam",
  `x_f.txt` "madde=çeşitler:bayrak"). Tahmin edilen 14 bin değil **39.155 madde** (≈24 bini tamlama). 48 madde iki kez
  yazılmış (aynı anlam bir kez tutulur), 8 madde anlamsız ("imam-ı ömer="), bayrak 1 olan 30 kısa madde ("as", "âl")
  yalnız kendisi olarak eşlenir (bizim yorumumuz). Tek başına "hakikat" lügatta yok (yalnız tamlamaları var).
- **Eşleme** (`lugat.py`): anahtar `search_words`; bulunmazsa son kelimeden Türkçe ekler atılır (yumuşama, düşen
  ünlü). İlk ölçümde yanlışlar çıktı ve kurallar sıkılaştı: kesme işareti ve ş/s farkı anahtarda yok sayıldığı için
  "bir" → bi'r (kuyu), "şu" → şu', "sen" → şe'n, "kurtuluşu" → kürdî, "esrarımı" → eşrar, "bütün" → bu'd. Çözüm:
  harf biçimi (`Form`: ş ç ğ ö ü ve kesmelerin yeri) tutmayan madde eşlenmez; yalnız "n"/"m" eki atılmaz ("olan",
  "benim"); atılan ek ş/ö taşımaz; metindeki kesmeden sonrası ektir ("Kur’ân’ın" → Kur'ân); sesteş Türkçe kelimeler
  `STOP` ("dahi" dâhî değildir). Son ölçüm (3.000 cümle, 46 bin kelime): %26 tam, %20 ek atılarak, %2 çeşit
  yazılıştan; bulunamayanların başı "ve, bu, gibi, bir" gibi Türkçe kelimeler. Rapor `data/interim/lugat/olcum.md`.
- **Araç:** `lookup_word(words)` (en çok 30), talimata `LUGAT_INSTRUCTIONS` (nâşirin lügatı; anlamı kendi sözüyle ver,
  adını an, Kaynaklar'a koyma). Uçtan uca deneme (`claude -p`, genel profil, "haşr-i cismanî ne demek?"): model
  lügate iki kez baktı, lügatın adını ve "Bediüzzaman'ın sözü değildir" notunu verdi, alıntılar `cite`'tan geçti.
- **Platform:** `oku-veri.py` her birim için `veri/<birim>.lugat.json` (birim 88: 1.575 anahtar, 1.026 madde,
  ≈175 KB; ilk dokunuşta yüklenir). Dokunulan kelimeyi kapsayan en uzun tamlama metinde belirtilir, kutuda madde ve
  anlam; "Lügat" düğmesi kapatır; karşılama sayfasına bir madde. Masa (`/taslak/ayet.html`) dışarıda kaldı.
- **Site:** belgelerde araç satırı (Türkçe, İngilizce), Risale sayfalarında kaynak, dört proje talimatına bir satır
  (ChatGPT kullanıcıları eklentiyi yenilemeli; Yenilikler taslağı söyler).

**S10. Davet altyapısı ve okuma platformu** (bitti ve yayında, 2026-11-23; kullanıcının kararları 2026-11-22 ve
2026-11-23: kaldığı yer sunucuda, hesaba bağlı; Notlarım Word dosyası olarak, çünkü okuyucular bilgisayarla haşir neşir
olmayabilir; "yalnız siz görürsünüz" ifadesi; eski notlar ar-ge kaydı olarak ayrı; taslak sunucusuna giden dışa
aktarım defter notlarını vermez; deploy ve canlı deneme izni):
- **Hesap ve davet** (`site_auth.py`): `davet <e-posta> [--masa] [--name]` tek kullanımlık bağlantı verir
  (`https://risalemcp.com/oku/davet/<jeton>`, 7 gün, yalnız özeti saklanır, yenisi eskisini bozar); hesap yoksa açılır,
  varsa parolası yenilenir (oturumları kapanır, kapsamı değişmez). Okuyucu parolasını kendisi koyar (en az 10 karakter),
  girmiş olur. `davetler` bekleyenleri listeler. `add-user` varsayılanı artık `oku` (`--masa` açıkça). Caddy
  `/oku/davet/*`'i girişsiz servise verir (`no-referrer`). Girişsiz `/oku/` isteği girişten sonra `/oku/`'ya döner
  (önceden Caddy'nin iç yolu `/taslak/oku/`).
- **Kişisel defter** (`masa.py`, `notlar.kapsam`): platformdan yazılan not `defter`dir: herkes (yönetici de) yalnız
  kendi notunu görür, yazan düzenler (`PUT /taslak/api/not/<id>`) ve gerçekten siler (`DELETE`; geçmişi de), tür ve
  durum yok, dışa aktarmaya ve `notlarla`ya girmez, hesap silinince (`remove-user`) silinir. Notta birimin adı
  (`etiket`) ve paragrafın ilk sözleri (`baglam`) durur. S10'dan önceki notlar `arge` (silinmez kuralı, durumları,
  dışa aktarım onlarındır); masa onları `?arge=1` ile görür (`d1-masa-sablon.html`). Notlarım: `GET /taslak/api/defter`,
  Word dosyası `defter.docx` (`docx_yaz.py`; yeni bağımlılık yok, düz XML; Word, LibreOffice ve Google Dokümanlar açar).
- **Platform** (`scripts/oku-app.html`): paragraf altında yalnız "✎ Not ekle" (atıf ve bağlantı kalktı); not açılınca
  paragrafın adresi adres çubuğuna yazılır; telefonda düğmeye dokununca kaybolan seçim saklanır; not kartında düzenle ve
  satır içi onaylı sil; ilk girişte karşılama (`#/~hosgeldin`: taslak, tefsir değildir; not nasıl bırakılır; ne
  saklanır; kopyalama), Notlarım (`#/~notlarim`), giriş sayfası `#/~giris`; kopyalanan metnin sonuna damga ("— Risale
  MCP okuma platformu, Bakara 2:40, taslak sürüm 1, <paragrafın adresi>. Yapay zekâ taslağıdır; tefsir değildir.";
  taslak dışı yerde birimin adresi ve "Bu sayfadaki taslaklar yapay zekânındır"); kaldığı yer (`/taslak/api/yer`,
  birime girince ve kaydırınca) ve `/oku/` boş adresle açılınca oraya gider. Telefonda başlıkta "geniş" ve "Usul"
  gizli (taşıyordu).
- **Notlar metnin içinde** (kullanıcının geri dönüşü ve kararları, aynı gün): işaretlenen söz çok açık sarı zeminle
  işaretlenir, sonunda (kelime bölünmesin diye kelimenin sonunda) ✎ durur; ✎'ye ya da sarı alana dokununca not
  paragrafın altında açılır ve kapanır, sarı alan bir an koyulaşır. Açılışta notlar kapalı; "Notlar (n)" düğmesi hepsini
  açar ve kapar. Aynı söze yazılan notlar tek ✎ altında (✎2), kesişen işaretlerin ortak kısmı daha koyu. Seçimsiz not:
  paragrafın sonunda ✎. Söz bu sürümde yoksa not açık durur, "bu sürümde bulunamadı" der; söz gizli kısımdaysa (Arapça
  kapalı) ✎ paragrafın sonunda. Seçici artık boşluksuz metinle saklanır ve aranır (önü ve ardıyla, aynı söz birden çok
  geçerse doğrusu); ✎ kopyalanan metne girmez; seçim yaparken sarı alana dokunmak notu açmaz. Paragraf değişirse
  notun görünmemesi açığı PLANLAR "Sonra"da.
- **Açık davet** (kullanıcının kararı, aynı gün: okuyucuya önce e-postasını sormak gerekmesin; e-posta doğrulaması
  gerekmez, çünkü e-posta yalnız giriş adıdır ve doğrulama sitenin e-posta göndermesini isterdi): `davet --acik
  [--not "Ahmet Hoca"]` adressiz bağlantı verir, okuyucu e-postasını ve parolasını yazar. Yalnız yeni hesap açar:
  adresin hesabı varsa reddeder (başkasının hesabı ele geçirilmesin), parola yenileme adresli bağlantıyla kalır.
  Yöneticinin notu (`label`) hesaba geçer, `users` ve `davetler` gösterir, `set-label` değiştirir. Bağlantı aynı anda iki
  kez gönderilirse ikincisi işlemez. Gizlilik politikasına iki cümle (doğrulanmayan adres, yöneticinin notu).
- **Gizlilik politikası** (Türkçe, İngilizce, 23 Kasım 2026): eski metin "notlar sunucuya gönderilmez" diyordu (S7'den
  beri yanlıştı); yeni metin davet, saklananlar, kaldığı yer ve defter notlarını anlatır.
- **Deneme:** 27 yeni ya da değişen test; yerelde tarayıcıda (masaüstü ve 390 px) davet → karşılama → not → düzenle →
  sil → kopyalama → Notlarım → dönüş; canlıda uydurma bir hesapla curl ile baştan sona (davet, tek kullanım, kapsam,
  karşılama, yer, not, Word, ar-ge kapalı, silme), sonra hesap silindi. Canlıda tarayıcıyla girişi kullanıcı yapar
  (model canlı sitede parola girmez).
- **Taslak sunucusu:** kuyruk her birimden sonra `/oku/index.html`'i ve masa kabuğunu kendi kodundan kurar; yeni kod
  `taslak-sunucu.sh gonder` ile `~/kod-bekleyen`'e kondu, sıradaki birimin başında geçer. Arada eski kodla biten birim
  eski uygulamayı geri koyarsa yerelden yeniden gönderildi.
- **Bulunan açık (S7'den beri):** `deploy.sh --code` yereldeki `data/interim/oku-masa/`'yı (21 Kasım kopyası) `/taslak/`'a
  gönderiyordu: 21 Kasım'dan beri her deploy masanın girişini, panosunu, birim listesini, deneyler defterini ve bazı
  `masa-veri` dosyalarını eskisiyle eziyordu (bugünkü iki deploy dahil). Taslak sunucusunun kendi kopyasından geri
  yüklendi; `deploy.sh` artık platformu ve masayı göndermez (kuyruk gönderir), `data/d1/masa`'yı `-u` ile gönderir;
  yerelde `oku-veri.py --gonder` yalnız platformu gönderir.

**Küçük açıklar B4, B7, B8 (2026-11-21, kullanıcının onayı: "önerdiğin sıraya başla"; B2 ve B5 aynı gün kapandı):**
- **B4 Mecmua eşlemesi:** Nutuk'ta "üç elmas kılıç"ın "Birincisi"nin altındaki iki kelimelik "İttihad-ı millî...",
  ikinci geçişte (`_fill_between`) Divan-ı Harb'in uzun "Yaşasın Şerîat-ı Garrâ! … Yaşasın ittihâd-ı millî! …"
  paragrafına bağlanmıştı (kısa satır komşu paragrafta kelimesi kelimesine geçince bağlanıyordu). Kural
  (`mecmua._drop_lone_parts`): paragrafın yarısından küçük parça ancak paragrafın başı ya da sonuysa ("Elcevab:",
  "Üçüncüsü:", paragrafı bitiren Arapça) ya da yanındaki mecmua paragrafı aynı paragrafa eşlenmişse kalır. İlk
  sürüm (yalnız komşu şartı) 43 paragrafı çözüyordu, çoğu doğru etiket eşlemesiydi; baş ve son şartıyla 3'e indi:
  Nutuk (asıl hata), Fihrist `lemalar/lema-21/p003` (üç satırlık âyetin ortası, okurken iki kez görünüyordu) ve
  Tılsımlar `dal-05/meyve-05/p028` (Câmî'nin Farsça satırı uzun paragrafın tamamını gösteriyordu). Kimlik değişikliği:
  1 silinen, 26 metni değişen, 4 eklenen cümle (`data/manifest/genel/changes/`), kullanıcının onayıyla kabul.
- **B7 Bitişik yazılan kelimeler:** ölçüm: `"âhir zaman"` 1 / bitişik 31, `"her şey"` 15 / 289, `"hiç bir"` 20 /
  1.625, `"bu gün"` 3 / 168. Tırnaklı ifadenin boşlukla ayrılmış tek kelimeleri bitişik yazılışlarıyla da aranır
  (`search.joined_forms`, en çok 4 kelime, Arapça hariç); `NEAR(…)` içinde her birleşim ayrı NEAR. Bulunan eski
  hata: `NEAR` içinde Arapça kelime (önekli biçimlerin OR grubu) FTS5 sözdizimi hatası veriyordu; NEAR içinde düz
  biçim. `search` aracının açıklamasına bir cümle, yalnız Risale sunucusunda (`SEARCH_JOINED_HELP`).
- **B8 Delâil'in dipnot rakamları:** 4.507 cümlenin 1.173'ünde 1.414 işaret ("الأولى2،"); aramada kelimeyi bozuyordu
  ("الأولى" bulunmuyordu; `nazm` 174 → 178 sonuç), `cite`'ta rakamsız alıntı tutmuyordu. Ayrıştırıcıda
  (`klasik_openiti._line`) metinden ayrılır, sayfa sonları kaydırılır, sayısı `notes`'ta; kimlikler ve basılı
  sayfalar aynı. Esrâr'da 1. Kalan tek bitişik rakam bir âyet adresi (`[الأنبياء100 - 101]`), dokunulmadı.
- Vektörler: değişen bölümlerin 3.929 cümlesi (0,19 M token); `export-public` genel ve klasik. Testler
  `tests/test_kucuk_aciklar.py`, `tests/test_search.py`.

**D5'in plan metni** (bitti, 2026-11-21, kullanıcının kararı: "sistem artık tamamen kuruldu, arka planda sunucuda
Bakara sûresi yazılmaya devam ediyor"; `PLANLAR.md` "Sıradaki"nden değiştirilmeden taşındı; D5.2 ve maliyet raporu
"Sonra" › "D5'ten kalanlar"a, istem adayı "Fikirler"e geçti).

**D5. Asıl iş: Bakara 34–286** (eski D1.8; 2026-11-20, kullanıcının kararı: D5 yalnız Bakara, Kur'ân'ın geri kalanı "Sonra"da). Tek adım değil, küçük adımlar; D15'ten çıkan hatla (2026-11-17).
- **D5.0 Üretim hazırlığı** (D11'in kalanı, kullanıcının kararları 2026-11-17 ve 2026-11-18; 2026-11-19'da alt adımlara
  bölündü, kullanıcının kararı: eski "D5.0 (n)" göndermeleri D5.0.n diye okunur). **D5'te birim başına insan onayı
  yoktur** (kullanıcı, 2026-11-19: bütün Kur'ân'ın taslağı birinin onayına sunulmak için değil, okunmak için): kalite
  makineden gelir.
  **D5'te okuma** (kullanıcının kararı, 2026-11-21: "D5 ve S7'nin ortak amacı taslakları insanlarla buluşturmak …
  okumalar ar-ge için taslağı geliştirmek için yok muydu?"): okumalar yalnız ar-ge içindir (hattı geliştirmek, bir
  sürümü sınamak), onay değildir. Bu yüzden (1) kuyruk okuma görevi açmaz, "her 20 birimden biri" okuma listesi
  kalktı; alarmlar ar-ge bilgisi olarak Panoda ve durum sayfasında durur, görev açmaz; (2) okuma görevleri (S7.2)
  yalnız deneyler için, elle açılır (kabul 30, ileride bir istem değişikliği, belki ehil okuması); (3) D5.1'de
  okuma yok (kabul 30 zaten D5 koşullarında: önceki birimin taslağını görür, kendi İşârât'ı gizli); 34'ü kuyruk
  yazarken durum Panodan izlenir; (4) D5.2 bir kez yapılır (30'un kapsamadığı tek risk: Risale'si az birimler), okuma
  yerine göz atmak yetebilir. Yanlışı görüp not etmek okuyucuların işi (S7.4); bir notu düzeltmeye vermek elle
  (S7 (f)).
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
    **Sunucuya taşıma: karar verildi** (kullanıcı, 2026-11-20): bilgisayar bir ay açık kalmasın; D5'in yazdırması
    sunucuda döner (ayrıntı aşağıda "Bilgisayardan bağımsız çalışma"). **Bakara bu planla**
    (kaba hesap, 2026-11-20): haftalık pencere %40 dolu, 23 Kasım'da sıfırlanır; 11 Aralık'a kadar ≈4,5 haftalık kota
    (bu haftanın kalanı, üç hafta, bir ücretsiz sıfırlama); D5 birimi haftalığın ≈%1,5–3'ü: 160–270 birim, gereken
    154; dar ama mümkün. Şartlar: D5.0 bir haftada biter, iş kesintisiz döner, öbür kullanım az, ücretsiz sıfırlama sona
    saklanır. Taslaklar sırayla yazılır (D5.0.5: her birim önceki birimin taslağını bekler). Kesin hesap D5.1'den sonra.
    **Asıl ürün altyapı; hesap ve kapsam** (kullanıcının değerlendirmesi, 2026-11-20): işin bu kadar uzun ve maliyetli
    olacağı hesaba katılmamıştı; önemli olan hazır bir altyapı (hat, kalite kapısı, bölme, kuyruk, birim başına bilinen
    maliyet), biri destek olursa o parayla işin yapılabilmesi. Kaba ölçü (D15.2, 26–27): bir ar-ge birimi 18,9 $ liste
    fiyatı, 5 saatlik pencerenin ≈%25'i, haftalığın ≈%2'si, 56 dk. D5 birimi tahmini ≈13–16 $ (taslak, kapalı, nisbet,
    düzeltme, izah), haftalığın ≈%1,5–3'ü: tek abonelikle haftada ≈35–60 birim; Bakara (153 birim) ≈3–5 hafta
    (API'de ≈2.000–2.500 $), bütün Kur'ân (≈3.000–3.800 birim, tahmin) ≈1–2 yıl (API'de ≈40–60 bin $). Darboğaz saat
    değil kota. Kotayı düşürme adayları (D5.0'da sınanır): hafif işler (nisbet, izah) Sonnet'e, düzeltme yalnız yüksek
    öncelikli bulguda, kapalı eleştirmen yalnız işaretlenen paragraflara, taslakta düşünme "orta". **Kararlar
    (kullanıcı kabul etti, 2026-11-20):** (a) kapsam ve hesap kararı D5.1 ve D5.2'den sonra, gerçek D5 zincirinin
    ölçülen birim başı kotası ve maliyetiyle; (b) **sûre başına maliyet raporu** (destekçiye "şu kadar para, şu kadar
    sûre"); (c) **hesap ayrımı:** iş kişisel hesaptan ayrılacak; iki yol: ayrı abonelik (ucuz; tüketici şartlarına
    bakılmalı: kişinin ikinci hesabı ve aboneliğin sunucuda toplu işte kullanımı) ya da API hesabı (Console;
    kullandıkça öde, harcama sınırı, fatura ve kullanım raporu, kota yok; Batch ve önbellek indirimleri hattın bir
    kısmının yeniden yazılmasını ister); (d) **hat hesaptan bağımsız:** abonelik ya da API anahtarı tek ayarla
    değişir; API'de sınır korumasının yerini iş başına harcama tavanı alır. D5.1 ve D5.2 bugünkü hesapla.
    **Bilgisayardan bağımsız çalışma** (kullanıcı kabul etti, 2026-11-19; karar yeri gelince): D5'te birimler günlerce
    sürer; iş sunucuda döner. Parçalar: `claude setup-token` (aboneliğin uzun ömürlü giriş anahtarı, tarayıcısız;
    kullanım aynı pencereden düşer, `claude_p`'nin koruması orada da çalışır); genel ve hadis veritabanları, Kur'ân,
    vektörler sunucuya (deploy betiğinin uzantısı); `data/d1` sunucuda her adımda commit ve push, yerelde `git pull`;
    okuma sayfaları sunucudan doğrudan `/taslak/`'a. **Kuruldu (2026-11-20, kullanıcının seçimi "A": tefsir
    makinesi; yük ≈0, 5 GB boş bellek):** ayrı kullanıcı `taslak`, `scripts/taslak-sunucu.sh` (CLAUDE.md "Taslak hattı
    ve kullanım sınırı"); veri sunucudan sunucuya (yayındaki kopyalar yereldekiyle aynı, `ozet`; evden yükleme ≈15
    KB/s, kullanılmaz); özel depoya yazma izinli deploy anahtarı eklendi; işler Nice=10. **Kalan:** kullanıcının
    `giris`'i (aboneliğin anahtarı), sunucuda ilk gerçek model çağrısı (yoklama ve bir taslak), okuma sayfalarının
    sunucudan gönderilmesi (bugün yerelden `taslak-gonder.sh`).
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
    **Bakara kesinleşti (2026-11-20):** kullanıcı 20 geçişi okudu (`d1-bolme.py inceleme`, sayfa `bolme-bakara.html`);
    19'unda koşuların çoğunluğuyla aynı, 73|74'te "sınır" (74 uzun, yeni bir misal getiriyor: "72–74 tek başına
    incelendiğinde 74'ün kendine has nükteleri kaçırılabilir"): kural b6 (5. kural genişledi). **Bakara 176 birim**
    (1–33 İşârât'ın 22 birimi, 34–286 154 birim), kimlik âyet aralığı (`34`, `35-37`…): `data/d1/bolme/bakara/birimler.json`
    (kalıcı adres). Kararlar `bakara/karar/`. **Kalan:** bütün Kur'ân (b6 ile; kısa sûreler ve ahkâm için kuralın
    uzatması ayrıca konuşulur); sırası gelince.
  - **D5.0.5 Önceki birim:** birinci vecih için İşârât'ın önceki birimi yerine önceki birimin taslağı; D15.3'te 28'de
    sınanır (26–27'nin h9 taslağı).
  - **D5.0.6 Kalite kapısı: denetle, düzelt, yayımla** (2026-11-19'da yeniden tarif: insan onayı olmadığı için kör
    aletler insanı yönlendirmek için değil otomatik düzeltme için): nisbet denetçisi (D14.5b), kapalı eleştirmen (tek
    çağrı), düzeltme turu (D12.1: kapalı notlarla düzeltme işe yaradı ama uzattı; sınanmalı), mekanik denetimler ve
    **biçim denetimi** (her Arapça paragrafın tercümesi hemen arkasında mı; D15.1'de taslak tercümeyi topluca verdi;
    yazımdan hemen sonra çalışır, kullanıcı kabul etti 2026-11-19).
    Ayar verisi D15'ten (D15.1: kapalı İşârât'sız görülebileni kaçırmıyor, nisbet onu tamamlıyor).
    **İlk sınama (2026-11-20, 26–27 ve 28'in h9 taslakları, istem d2):** ilk ölçüm geçersizdi (düzeltmeyi uygulayan kod
    `###` alt başlıklarını sayıyordu, değişiklikler komşu paragrafa iniyordu; 28'de 51'in 47'si; onarıldı `7e0a5e5`,
    D12'nin düzeltmeleri etkilenmemiş, taslaklar aynı model çıktısından yeniden kuruldu, hatalılar `hatali-capa/`).
    Doğru kurulumla: nisbet hatası 26–27'de 11/71 → 7/96, 28'de 2/25 → 6/54; **eski hataların hepsi düzeldi, kalan
    hataların hepsi düzeltmenin eklediği yeni kaynaklardan ya da yeniden yazdığı paragraflardan** (26–27: 7'si de yeni
    kaynak; 28: 3 yeni kaynak, 2 değişen paragraf, 1 eskiden kalan). İşârât karşılaştırmasının hükmü ikisinde de
    değişmedi (düzeltmeyle), "eksik" notları azalmadı (12 → 12, 7 → 10). Arapça %10,4 ve %12,8 uzadı (sınır %10).
    Maliyet birim başına ≈6–7 $ (kapalı 2,3, nisbet 1, düzeltme 2,6–3,4). **Öneri (kullanıcının kararını bekliyor):**
    d3: düzeltme yeni kaynak eklemez, yalnız düzeltir, daraltır, siler; eksik nükte notları düzeltmeye girmez (okuma
    sayfasında not olarak durur); değişen paragraflara ucuz bir nisbet geçişi.
    **d3 kabul edildi ve sınandı (2026-11-21):** nisbet hatası 26–27'de 11/71 → **3/79** (ikinci tura not çıkmadı;
    kalan üçü düzeltmenin dokunmadığı sözlerde), 28'de 2/25 → 2/37 → ikinci turdan sonra **0/37**; Arapça %9,3 ve %6,6
    uzadı (sınırın içinde); İşârât karşılaştırmasında "kaynak" notları 26–27'de 3 → 0, hüküm ikisinde de "düzeltmeyle"
    (beklenen: kapı nükte eklemez). Yazar 14 ve 9 notu gerekçesiyle reddetti. Maliyet birim başına ≈6–7,5 $ (kapalı
    2,3, nisbet 1, düzeltme 2,2–2,9, ikinci nisbet 0,6, gerekirse ikinci tur 1,2). **Kapı d3 ile hatta girer.**
  - **D5.0.7 Maliyet:** taslak ≈4,5–5,5 $, konu ve tablo ≈0,3 $, nisbet ≈1 $, kapalı ≈3 $, düzeltme (ölçülecek);
    Bakara'nın kalanı **154 birim** (b6, kesin), bütün Kur'ân ≈3.400 birim tahmini (bölmeden sonra güncellenir).
  - **D5.0.8 Soru kalıpları listesinin bütün İşârât'tan yeniden kuruluşu:** gerek kalmadı (2026-11-20: hat h9,
    liste ve Tarama yalnız h10'daydı). Yerine D15'in açık sorusu: edatın ve kaydın taalluku (bkz. D15 "Hat h9").
  - **D5.0.9 Kabul birimi 30:** D5.0'ın değişiklikleri (D5.0.4–D5.0.8) bitince hattın son sınaması; 30 hiçbir denemeye
    ve listeye girmez.
- **D5.1'den önce hepsi** (kullanıcının kararı, 2026-11-21: "D5.1'de Bakara'nın tamamı yazdırılırken durum nasıl
  olacak, onu görmek istiyorum"; D5.1 üretimin aynısı olmalı). Sıra: (a) h12 ✓ (`4393a54`); (b) **D5 kipi**: birimler
  `bolme/bakara/birimler.json`'dan, prova veritabanı yok (genel veritabanlarına bağ), sızıntı testi yok, önceki birim
  İşârât'sa (34'ün öncesi 31–33) İşârât, değilse önceki birimin son taslağı (D5.0.5), Ek 3b'nin garaz özetleri İşârât'ın
  birimlerinden ve D5'te yazılmış taslaklardan (her birimden sonra bir özet); (c) **tek komutla birim** (`d1-birim.py`):
  istem, taslak, kapı d3 (kapalı, nisbet, düzeltme, ikinci tur), garaz özeti, izah (D5.0.3), D5 okuma sayfası
  (taslak, dersler, kapının düzelttikleri, eksik notları; İşârât yok), birim kaydı (son taslak, maliyet, süre);
  (d) **kuyruk**: Bakara sırasıyla, kesintide kaldığı birimden, sunucuda `d1-arka.sh` ile; sayfalar sunucudan siteye;
  (e) **telefona bildirim ve harcama tavanı** (D5.0.1'in "sonra"sı); (f) **kabul birimi 30** sunucuda, h12 ve h9 kör A/B
  (kullanıcı 3 yeri okur: birinci vecih, bir taalluk yeri, Risale dersi; kartlar içeriğe göre seçilir, iki taraf
  gönderilmeden okunur); h9 mı h12 mi orada belli olur. Sonra D5.1 (Bakara 34), D5.2.
  **Hepsi yapıldı (2026-11-21).** Kabul 30'un sonucu (kullanıcının kararı): okuma 3 yerde eşit; ölçüler h9 lehine
  (h12 %39 pahalı, %19 uzun, nisbet hatası daha çok, dersinde damga hatası; İşârât karşılaştırması ve envanter eşit) →
  **D5 istemi h9** (`D5_SURUM`, varsayılan h9); "bu kadar okuma yeter" (h12 denemesi kapandı). **Kaynak
  tercümesi D5'in adımı** (kullanıcının kararı): her birimden sonra taslağın andığı tefsir ve klasik yerler çevrilir
  (`kaynak-tercume.py`, Sonnet, 3 paralel; birim başına ≈0,4–0,5 $, birimin ≈%3'ü), `D5_TERCUME=0` ile atlanır.
- **Büyük işin kolaylıkları** (kullanıcı kabul etti, 2026-11-21; D5.1'den önce; model çağrısız): (1) her birimden
  sonra `data/d1` commit ve push (kuyruk tek uzun iş); (2) kuyruk sunucunun açılışında başlayan, düşünce yeniden kalkan
  hizmet (`d1-kuyruk`); (3) **haftalık pencere koruması: %90** (kullanıcının eşiği; geçince durur, sıfırlanınca sürer,
  telefona haber); (4) kalite alarmları (kapıdan sonra kalan nisbet hatası, eksik vecih, Arapça uzunluk aykırı, Risale
  dersi yok, kapı notların çoğunu reddetti, izah eksik): kuyruk durmaz, alarm birime yazılır, telefona düşer (görev açmaz);
  (5) durum sayfası `/taslak/d5.html` (birimler, bağlantılar, alarmlar, maliyet, haftalık kota, bitiş tahmini) ve
  günlük özet bildirimi; (6) geçici hatada bir kez yeniden deneme; (7) kod güncellemesi yalnız birimler arasında
  (sunucuda bekleyen kod, sıradaki birimin başında geçer); (8) **kolay durdurma ve sürdürme** (kullanıcı: "önümüzdeki
  haftalarda sık kullanabilirim"): `scripts/taslak-sunucu.sh dur | devam | hemen-dur | durum` ya da telefondan Claude'a
  söylemek; `dur` birimi bitirip durur, `hemen-dur` ortada keser (sürdürünce biten adımlar atlanır). Okuma listesi
  2026-11-21'de kalktı ("D5'te okuma").
- **D5'in başlangıç sırası** (kullanıcı kabul etti, 2026-11-20): (1) Bakara bölmesinin 20 geçişi (D5.0.4); (2) kalite
  kapısı D15'in taslakları üzerinde, İşârât doğru cevap olarak (D5.0.6); (3) **h9'a bir iyileştirme turu** (h11;
  kullanıcının kararı: yapılacak; adaylar D15 raporundan: birinci vechin genişliği, ders seçiminde isabet ölçüsü,
  taalluk sorusu; saklı birim 29'da h9'a karşı); (4) tek komutla birim hattı (D5.0.1); (5) kabul birimi 30 (D5.0.9);
  (6) D5.1, D5.2. İzah (D5.0.3) S7 ile.
- **h11'in tanımı** (kullanıcı kabul etti, 2026-11-20): (a) **birinci vechin genişliği:** kaynak dosyasına sûrenin
  şimdiye kadarki birimlerinin kısa garaz özetleri (İşârât'tan; D5'te taslaklardan) ve sonraki 3–5 âyetin metni;
  istemde birinci vecih için "önceki bahislere, sonraki âyetlere ve Kur'ân'ın bütününe uzanan hatları say"; (b)
  **ders seçimi:** zorunlu ders başlığının isabeti en güçlü tek bölümden değil ilk birkaç bölümün toplamından (28'de
  haşir konusu: Onuncu Söz 19, öbürleri 17, 15; Risale'nin en geniş işlediği konu tek bölümde 25'i bulamadığı için
  ders açılmadı); (c) **taalluk:** istemde ikinci ve üçüncü vecih için üç soru (edat, kayıt ya da cümle neye bağlı;
  zâhiren ne beklenirdi; neden bu geldi; bağ için söylenmemiş bir şey varsa takdiri), geliştirme birimlerinden iki
  kısa İşârât örneğiyle; h10'daki gibi tablo yok (zorlama). Sınama: saklı birim 29'da h9'a karşı (kör A/B ve
  kullanıcının okuması).
- D5.1 Bakara 34, kuyruğun ilk birimi; okuma yok (2026-11-21; önceden "okumayı kullanıcı yapar", 2026-11-20), durum
  Panodan. **Kapsam yalnız 34** (kullanıcının kararı, 2026-11-21: "okumaya sabırsızlanıyorum"; 35–40 sonra).
  **Bitti (2026-11-21):** 38 dk, ≈12,1 $ kullanım değeri, haftalık kota %57 → %59; kapı 25 not (20 karşılandı, 5
  reddedildi), ikinci tur 5 not (hepsi reddedildi), son taslak 3. Alarm "kapıdan sonra nisbet 6/56" büyük ölçüde
  denetçinin hatası: kaynağın bağlamı baştan 4.000 harfte kesiliyordu, Ebüssuûd'un uzun önceki cümleleri atfedilen
  cümleyi dışarıda bırakıyordu (5 yanlış "kaynakta yok"; yazar beşini alıntıyla reddetti); kesim artık atfedilen
  cümlenin etrafından (`d1-nisbet.clip`, `f1aac75`). Kullanıcı 34'ü okuyor ("şu ana kadar gayet iyi"); sunuşa dair
  eleştirileri S7e–S7g oldu.
- **D5.2 Risale'si az iki birim, kuyruk büyümeden önce** (kullanıcının kararı, 2026-11-19; 2026-11-21: göz atmak
  yetebilir, bir kez; birimler sırayla yazıldığı için kıssa 40'ta erken gelir (kuyruk 40'tan sonra durur), ahkâm
  178'den sonra, geldiğinde): bir kıssa (İsrâiloğulları,
  40–74) ve bir ahkâm birimi (178–283) okunur. Sebep: D15'in saklı birimlerinin hepsi Risale'ce zengin (Risale'deki
  doğrudan alıntı 21–22'de 30, 26–27'de 14, 28'de 7); Bakara 34–283'te âyetlerin ≈%78'inde doğrudan alıntı yok (34–39:
  6'da 5, 40–74: 35'te 26, 178–283: 106'da 86; konu üzerinden gelen yerler sayılmadı). h10'un kazancı büyük ölçüde
  Risale dersinden; kuyruk "önce Risale'nin bağ kurduğu âyetler" sırasıyla başlarsa düşüş geç görülür.
- **İstem adayı** (D5.1'in okumasından, kullanıcı kabul etti, 2026-11-21; şimdi değil; S7 bitince buraya taşındı):
  "kelime mânâsında tek müfessire dayanma": taslak bir kelimenin mânâsını bir müfessirden alıp kendi sözü gibi
  kullanıyor, öbürlerini tartmıyor (34'te «kâne» yalnız Ebüssuûd'dan). Aday kural: bir kelimenin mânâsını bir
  müfessirden alırken öbürlerinin o kelimede ne dediğine bak, ayrılıyorlarsa söyle. Yeni istem sürümü ve deneme ister
  (h9 kararı bozulmaz); kapı ve nisbet bunu yakalamaz (atfın doğruluğuna bakarlar, tercihin tartılmasına değil). Usul
  sayfasında sınır olarak yazılı. Bkz. "Fikirler" › "Taslak usulünün hedeflere göre değişmesi".

**S8 ve S9'un plan metni** (bitti, 2026-11-21, kullanıcının kararı: "S8 ve S9 kapanır"; `PLANLAR.md` "Sıradaki"nden
değiştirilmeden taşındı).

**S8. Sonuç yazısı** (kullanıcı kabul etti, 2026-11-21): taslak işinin cevabı tek ve kalıcı bir yazıda: "Yapay
zekâ İşârât'ın mislini yazabilir mi?" Usul (hat, kapı, ölçüler), Bakara 1–33'teki İşârât karşılaştırmasının sonuçları
(yapabildikleri: garaz, omurga, Risale dersi; yapamadıkları: takdir zincirleri, taalluk, temsil ve îcâz, birinci vechin
genişliği, tartma), okuma turlarının kararları, örnekler (34'te «kâne», Risale dersi), maliyet. Şimdi
`KAYIT.md`'ye, deneyler defterine ve usul sayfasına dağınık; ehil okuyucu taslaklardan önce bunu okur. Yeri sitede
(yenilikler ya da platformun usul sayfasının genişi), kullanıcıyla kararlaştırılır.
**Taslak yazıldı (2026-11-21):** `docs/s8-sonuc-yazisi.md`. Kaynakları yazının sonundaki "Kayıtlar"da (yayımlanmaz).
Toplarken çıkan yeni sayı: İşârât karşılaştırması saklı beş birimin on iki taslağının on ikisinde bütün için
"düzeltmeyle" dedi (45 bölümün 8'i "yeterli", hiç "yetersiz" yok). **İki sürüm** (kullanıcının kararı, 2026-11-21): (1) **iç sürüm:** `docs/s8-sonuc-yazisi.md` bugünkü hâliyle
kalır (okuma platformunu, kayıtları ve iç ayrıntıyı taşır); (2) **site sürümü:** S9'un "Çalışmalar" kısmında
yayımlanmak üzere ayrı yazılır: okuma platformundan açıkça bahsetmez (platform davetle; "Bundan sonra"daki platform
anlatımı ve okuyucu notu çıkar, yerine genel bir cümle), siteye uygun (programcı ayrıntısı, sürüm adları (h9, d3),
dosya yolları ve "Kayıtlar" yok; S9'un iskeletine göre: kısa cevap kutusu, sınırlar, kaynaklar). Yer: S9.
Okuyucunun cümlesi (kullanıcının kararı, 2026-11-21; "ehil değil" yerine): "Okumaları projeyi yürüten kişi yaptı;
tefsir ve belâgat alanında uzman değildir, bilmediğini kaynaktan araştırdı ya da ehline sordu. Bu alanların
uzmanlarının okuması henüz yok." 

**S9. Sitede "Çalışmalar" kısmı** (kullanıcının fikri ve kararları, 2026-11-21): Yenilikler'den ayrı, blog yazısı
tarzında bir kısım; projenin ne denediğini ve ne öğrendiğini anlatan uzun, kaynaklı yazılar. Ad **"Çalışmalar"**
(kullanıcı kabul etti). Yenilikler'den farkı: Yenilikler eklentide ne değiştiğini kısa, örnek soruyla, eklentiyi
kullanan herkese anlatır; Çalışmalar ehil ve tefsirle ilgilenen okuyucu için uzun, sayılı ve kaynaklıdır, tarihli
ama "son gözden geçirme" tarihiyle güncellenebilir. Bir çalışma yayımlanınca Yenilikler'e kısa bir duyuru düşer ve
yazıya bağlanır.
- **İskelet (her yazıda):** başlık, tarih, son gözden geçirme, okuma süresi; başta **"Kısa cevap"** kutusu; gövde;
  **"Sınırlar"** kısmı (zorunlu); **Kaynaklar** (Risale ve İşârât alıntıları sitenin atıf biçimiyle); isteğe bağlı PDF
  ve "Bu yazıya atıf" satırı; yapay zekâ taslağından alıntı varsa damga.
- **Teknik:** `scripts/site-uret.py`'nin yolu: yazılar `docs/calismalar/<tarih>-<ad>.md` (üst bilgi Yenilikler'deki
  gibi, ek olarak `gozden_gecirme`), çıktı `site/calismalar/<ad>.html` ve `site/calismalar.html`; menüye
  "Çalışmalar"; Open Graph, RSS, site haritası aynı yoldan. Markdown çevirisi genişler: tablo, sağdan sola Arapça
  alıntı (sitenin Naskh yazı tipiyle), "Kısa cevap" kutusu. CSS ya da JS değişirse `ASSET_VERSION`.
- **Taslak, önizleme, yayın** (kullanıcının isteği ve kararı, 2026-11-21: "yayından önce benim son düzenlemeleri
  yapıp yayınlayabileceğim bir yapı"; Yenilikler için de): (a) yazının üst bilgisinde `durum: taslak | yayinda`;
  taslak herkese açık listeye, RSS'e, site haritasına, ana sayfa şeridine girmez, `site/`'a yazılmaz; (b) **önizleme**
  girişli kısımda (`/taslak/onizleme/`, masa hesabıyla; telefonda da), sitedeki görünüşüyle; yerelde de bakılabilir;
  (c) **yayınlama tek komut:** durum `yayinda`, tarih o gün, site üretilir, bağlantılar ve paylaşım resmi denetlenir,
  gönderilir; Çalışmalar yazısıysa Yenilikler'in kısa duyurusu taslak olarak hazırlanır, o da kullanıcının onayıyla
  yayımlanır. Düzenleme Markdown dosyasında (kullanıcı kendisi ya da önizlemeyi okurken söyler, Claude işler); her
  değişiklik git'te. Tarayıcıda düzenleme kurulmaz (hesap, kaydetme, çakışma; kazancı az).
- **İlk yazılar:** (1) **İşârât'ın usulü, son sürümüyle herkese açık** (kullanıcının kararı): bugün `/isarat-usul/`
  yalnız bağlantıyla paylaşılıyor, `noindex`; sitedeki kopya `docs/d1/usul-ozeti.md`'nin son hâlinden eski (site
  2026-11-16 08.54, özet 21.28): `scripts/d1-okur.py` son özetten yeniden üretir (HTML ve PDF), `noindex` kalkar,
  menüde ve site haritasında Çalışmalar'ın yazısı olarak durur; eski adresler (`/isarat-usul/`, `/taslak/isarat-usulu.*`)
  yeni yere yönlenir ya da sayfa yerinde kalıp listeye bağlanır (yapılırken seçilir; paylaşılmış bağlantılar
  kırılmaz). Alıntılar `scripts/d1-usul-denetim.py` ile yeniden denetlenir. (2) **S8'in site sürümü** (bkz. S8).
- **Sonraki adaylar** (karar yok): "Müellifin sözünden birim bölmek" (bölme kuralı), "Neden atıf birimi cümle"
  (MCP'nin kaynağa bağlılık tasarımı).
- **İngilizce sonra** (kullanıcının kararı). Deploy `scripts/deploy.sh --code` (site); araç çıktısı değişmez.
- **Yapılanlar (2026-11-21):** `scripts/site-uret.py` iki türlü (Yenilikler, Çalışmalar), taslak, önizleme (`onizle`
  yerelde; deploy `/taslak/onizleme/`'ye), `yayinla` (geçici bir yazıyla sınandı: ad ve tarih o gün, duyuru taslağı,
  menü), Markdown'da kutu, tablo, çizgi, başlık kimlikleri ve içindekiler, Arapça işareti; sitenin Naskh yazı tipi
  (`site/fonts/naskh.woff2`, OFL; `?v=12`); menüde "Çalışmalar" ilk yazı yayımlanınca görünür; testler
  `tests/test_site_uret.py`. İşârât'ın usulü son özetten yeniden üretildi (148 alıntı denetimden geçti; 2.7
  Muhâkemât eklendi, okur betiği artık İşârât dışı kimlikleri de çözer). İki taslak bekliyor: `docs/calismalar/
  2026-11-21-isarat-usulu.md` (`adres: /isarat-usul/`) ve `2026-11-21-isarat-misli.md` (S8'in site sürümü).
  **Yayında (2026-11-21, kullanıcının onayıyla, `yayin-20261121-181953`, araç çıktısında fark yok):** site,
  stil `?v=12`, yeni usul sayfası (yayına kadar `noindex`), önizleme `/taslak/onizleme/` (girişli).
  **İşârât'ın usulü yayında** (2026-11-21, kullanıcının onayı: "sayfa uygun"; Çalışmalar'ın ilk yazısı, menüde
  Çalışmalar açıldı, `noindex` kalktı, site haritasında; `yayin-20261121-182932`). Yeniliklere duyurusu taslak
  (`docs/yenilikler/2026-11-21-isarat-usulu.md`, "Yeni bölüm: Çalışmalar…"). **S8'in site sürümü kısaltıldı**
  (kullanıcı: "gereğinden fazla ayrıntılı ve uzun … yalnız insanları ilgilendiren kısımları"; 2.192 → 695 kelime:
  ölçüler tablosu, yolun adımları, sayıların çoğu, maliyet ve okuma çağrısı çıktı; ayrıntılı hâli git geçmişinde ve iç
  sürümde `docs/s8-sonuc-yazisi.md`). Kullanıcının okumasından (2026-11-21): Yenilikler duyurusu yayında; S8'den
  "Bir şey daha öğrendik" paragrafı ve Bakara 34 örneği çıktı (551 kelime, alıntısız); **S8 2026-11-24'te kendiliğinden
  yayımlanacak** (kullanıcının isteği: "hemen yayınlama, 3 gün sonra"). Zamanlı yayın kuruldu: `yayin_tarihi`,
  `site-uret.py zamanla|zamanli`, `systemd --user` zamanlayıcısı `site-zamanli.timer` (her sabah 09.00), yalnız site
  gönderen `deploy.sh --site`; `yayinla` artık türüyle de (`yenilikler/ad`; aynı ad iki türde olabiliyor).
  **Kalan:** 24 Kasım'da S8'in yayımlandığına bakmak (commit edilir, push kullanıcıda).

**S7. Okuma platformu ve ar-ge masası (2026-11-21, kullanıcı yokken; kullanıcının onayı ve deploy izni):**
- **Masanın girişi** (`scripts/masa-giris.py`, `34873a6`): `/taslak/` = Pano · Okumalar · Birimler; kabuk +
  `pano.json`, okumalar canlı API'den; D5 kuyruğu her birimden sonra yeniler. **Okuma mantığı** (kullanıcının
  kararı): okumalar yalnız ar-ge, onay değil; "her 20 birimden biri" listesi ve kendiliğinden görev açma düştü
  (`2d68ab3`); D5.1'de okuma yok; D5.2 bir kez, göz atmak yeter.
- **Okuma platformu `/oku/` ve masanın birim görünümü** (`3b8716d`, `e1c7af0`, ders/arama eki): tek uygulama
  (`oku-app.html`), veri `oku-veri.py` (yayın dosyasından; İşârât 1–33, Risale'deki yerler `find_ayah` bağlarından,
  13 müfessir isteğe bağlı dosyada, kaynak adı ve bağlantısı her atıfta). Hesap kapsamı `masa`/`oku` (`site_auth.py`;
  çerez `/`; `oku` masaya ve okuma görevlerine giremez, yalnız kendi notunu görür); Caddy `/oku/` →
  `/var/www/ozel/taslak/oku/` (D5 sunucusunun kısıtlı anahtarı oraya yazabilsin); `/var/www/ozel/taslak` setgid
  (sunucudan gelen dosyalar `root` grubuyla Caddy'ye kapalı kalacaktı). Yayın: Arapça–Türkçe eşleme `d1-yz.pairs`'e
  geçti (önceki "son Arapça" eşlemesi kayıyordu), ders başlıkları `ust_baslik`; ar-ge birimleri v1 → v2. Yazı tipi
  Noto Naskh Arabic (OFL, `scripts/oku-fonts/`). Masa: bütün taslaklar, yan yana, kapı ve kapalı eleştirmen (her
  düzeltme ayrı; "kısmen" = karşılandı, bir kısmı reddedildi), nisbet, notların hayatı.
- **Okuyucu notundan düzeltme** (S7 (f)): `d1-birim.py notlarla <birim> [--deneme]`; d3 kuralları, karşılanan not
  "işlendi" (makine ucu `/taslak/api/not-durum`), reddedilen açık kalır. Henüz gerçek notla çalıştırılmadı.
- **Deneyler defteri** (`scripts/deneyler.py`, `00e728a`): 38 istem sürümü (`docs/d1/*-istemi.md`), 14 okuma turu
  (kollar, kör A/B, İşârât karşılaştırması, okuyucu kararları sabit numarayla, KAYIT kaydı), aşamalar D11–D15, alet
  ayarı (kör A/B ile okuyucu 9 turun 6'sında aynı taslak), kayma (garaz özetleri, birinci vecih), arama (bütün
  taslaklar ve okuma gerekçeleri).
- **S7b (2026-11-21, kullanıcının eleştirileri):** (1) masa ekranın tamamı; platformda ölçülü metin sütunu, sağda
  kaynak yan sütunu, "geniş" düğmesi; (2) Kur'ân paneli her ekranda açılıp kapanır, hatırlanır; (3) kaynaklı işaretler
  mavi, numarasız etiketler turuncu; bulunan hata: `[dil; 35]` biçimindeki atıflar tıklanmıyordu (30'un h12 son
  taslağında 19 atıf); (4) masanın birim sayfası eski âyet masası oldu, genişletildi (Kur'ân paneli, 6 yan, Kalite
  kapısı, Nisbet ve Okuyucu notları yanları, lafız süzgeciyle; D5 ve envantersiz birimlerde de kurulur); `birim.html`
  emekli. Kapı yanında her düzeltme denemesi ayrı, "kısmen" = karşılandı ama bir kısmı reddedildi.
- **S7c (2026-11-21):** masa sadeleşti (kör kip, tur bağlantıları ve D7–D9'un bütün işaretleme araçları kalktı; üst
  satır ☰ · birim · + yan · Dil; kör okuması sürerse yalnız uyarı), her yanda içindekiler ağacı (her müfessir, her
  taslağın eleştirileri ayrı yan; lafız sayıları; bölüm atlama), D5'te kelime sayıları taslaktan. İşârât eşlemesi:
  program envanterle %77 (±1 cümle %88), model 3 birimde 163/164 → kullanıcının kararıyla model, 37 bölüm (≈7 $).
  Kaynak tercümesi: ilk koşu sıralı ≈2 saat sürdü; 3 paralel çağrı ve orta düşünmeyle yeniden. Kabul 30'un okuması:
  3 yerde eşit, karar h9; iki kart tekrarı benim kart kurma hatamdı (`d1-tur.dedupe`). D5.1 (yalnız 34) başladı;
  kuyruğun ilk koşusunda `data/d1/d5/` yokken günlük özet hatası, düzeltildi.
- **D5.1 Bakara 34 (2026-11-21):** kuyrukla, h9; 38 dk, ≈12,1 $, haftalık %2; son taslak 3; alarm nisbet 6/56. Kuyruğun
  ilk koşusunda `data/d1/d5/` yoktu (günlük özet), ikinci koşuda bekleyen kod `systemd` yeniden deneme beklerken
  `devam` takıldı (`restart --no-block` ile). Masada S7c2 (katmanlar bugünkü hatta göre) ve S7d (tek kabuk, bütün âyetler,
  Fâtiha 7 birim, dört büyük düğme); giriş ve deneyler defteri iki makinede yazılıp çakıştığı için git'ten çıktı.
- **S7e Türk hattı (2026-11-21):** kullanıcının kararı: Kur'ân metni masada, platformda ve D5 sayfalarında Türk hattıyla
  (varsayılan), Medine seçilebilir. Kaynak risaleoku'nun Kur'ân'ı (`kuran_turk.py`; 6236 âyet, iskelet denetimi, 3 imlâ
  farkı 21:88, 63:10, 72:16). Masanın kelime düğmeleri iskelet konumlarıyla Türk hattının kelimelerine eşlendi (293/293
  âyet; bitişik yazılan "ذُوفَضْلٍ" düğme sınırından bölünür). Aynı gün: Türkçe metnin içindeki Arapça Kur'ân işaretleri
  (U+06DF) boş kutu çıkıyordu; Türkçe yazı tipi listelerine sitenin Naskh'ı yedek olarak eklendi.
- **S7f Alıntının cümlesi (2026-11-21):** kullanıcının sorusu (Bakara 34: «تولّد أنانية إبليس فيما بين الملائكة» altındaki
  "İblis'in enâniyetinin melâike arasında tevellüdü." neden orada?): taslak İşârât'ın cümlesinden yüklemsiz bir parça
  alıntılamış, altına da modelin tercümesi konmuştu. Kararı: platformda ve masada İşârât alıntısının Türkçesi eşlemeden
  Abdülmecid Nursî tercümesi; parça alıntıda "kaynaktaki cümlenin tamamı" (`scripts/alinti.py`; yalnız sunuş).
- **S7g Etiketler (2026-11-21):** kullanıcının önerisi: her paragrafın başındaki "Yapay zekâ tercümesi" ve izahın
  "yapay zekâ izahı" etiketi kalktı (platform ve masa); damga sayfa başında ve platformun üst çubuğunda her zaman
  ("yapay zekâ taslağı · tefsir değildir"; ekran görüntüsüne de girer). Kalanlar: alıntı, alıntının tercümesi (yapay zekâ
  ya da Abdülmecid Nursî), kaynakların Türkçesi; kopyalanan atıf satırı ve indirilen dosyalar kendi damgasını taşır.
- **S7h Alıntının kaynağı (2026-11-21):** kullanıcının bulgusu: Arapça gizliyken müfessir alıntısının yalnız yapay zekâ
  tercümesi kalıyordu, alıntı kutusunda değildi ve kaynağı belli değildi (numara Arapçadaydı). Platformda alıntı ve
  Türkçesi tek kutuda, başında kaynağın adı ve tıklanır numarası ("Alıntı: İrşâdü'l-Akli's-Selîm [30] · yapay zekâ
  tercümesi"); masada blok başlığında kaynak. Aynı gün: tam masa kurulumu sunucuda bitti ama son adımda yerelin gönderme
  betiği (yerel anahtar) kullanıldığı için platform gönderilmedi; kabuk kurulumun başında yazıldığından S7g'siz kaldı;
  ikisi elle düzeltildi.
- **D5.1'in okuması (kullanıcı, 2026-11-21):** "Genel olarak nazım nükteleri, daha öncekiler gibi, yerinde." Sınır:
  «وَكَانَ مِنَ الْكَافِرِينَ»'da «kâne»nin mânâsı kayıtsız şartsız Ebüssuûd'dan alındı (iki vecih, nisbeti doğru; tartma
  yok, öbür müfessirlere bakılmadı); yeniden yazdırmak çözmez. Güçlü yan: "Risale-i Nur'dan ders çok çok iyi" (âyetin
  Risale'de doğrudan bağı yok; dersi anlamsal aramayla buldu: D5.2'nin çekincesine karşı iyi işaret). Sonuç: usul
  sayfasına sınır satırı, istem adayı plana; 34'ün yayını düzeltilmiş nisbet denetçisiyle v2 (eski hükümler
  `nisbet-taslak-2.eski-kesik.*`); kuyruk 35–40 (`taslak-sunucu.sh devam 40`, yeni: o birim bitince durur).
- Denendi: `node` ile her birim ve sekme çizildi (176/176), tarayıcıda yerel deneme sunucusunda not, kaynak kutusu,
  ders, arama, kesintisiz okuma; canlıda girişsiz istekler girişe yönleniyor, API 401. **Canlıda girişle denenmedi.**

**S7'nin plan metni** (bitti, 2026-11-21, kullanıcının kararı: "S7 bitti"; `PLANLAR.md` "Sıradaki"nden değiştirilmeden
taşındı; açık kalanları `PLANLAR.md` "Sonra" › "Okuma platformu ve ar-ge masasının açıkları", istem adayı D5'te).

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

- **S7'nin yönü** (kullanıcı kabul etti, 2026-11-21; "ekleyecek çok şey çıkar"): (1) **durum sayfası ar-ge masasının
  girişi** (pano); okuma platformunda yalnız tek satırlık ilerleme. (2) **Eleştiriler ve nisbet:** ar-ge masasında
  hepsi ham hâliyle (kapalı eleştirmenin notları, nisbet hükümleri, kabul ve ret gerekçeleri, düzeltme farkı,
  alarmlar); okuma platformunda ham not yok (eleştirmen de yapay zekâ, isabeti %83; iç dil), sonuçları var: atıfın
  yanında işaret (kapının düzeltemediği kuşkulu atıf "kaynağın dediğini aşıyor olabilir"), "bu taslak nasıl yazıldı"
  künyesi (notlar, düzeltilen, reddedilen, geçtiği denetimler), "eleştirmenin gördüğü ama taslağa eklenmeyenler"
  (eksik notları, "yapay zekâ eleştirmeninin notu, denetlenmedi" diye). (3) **Katkıya açık platformun zemini:**
  kalıcı adresler (birim âyet aralığı; paragraf yayımlanınca değişmeyen kimlik alır, sıra numarası değil); değişmeyen
  sürümler (yayımlanan sürüm dondurulur, silinmez; not sürüme ve işaretlediği söze (önü ve ardıyla) bağlanır, yeni
  sürümde söz duruyorsa taşınır; web'in not alma usulü, W3C Web Annotation gibi); kim, ne, hangi sıfatla (müellif,
  müfessir, yapay zekâ, okuyucu, ileride ehil; not silinmez, geri çekilir; davet, hesap, rol: okuyucu → katkıcı →
  ehil); tek veri biçimi, iki görünüm (birim başına yayın dosyası; masa ve platform ondan çizilir; notlar ana
  makinede `/taslak/` hesaplarıyla, dışa aktarılabilir). Dondurulan heyet akışı (2026-11-09) açılmaz, yalnız zemini
  kurulur. Ekler: telefona göre tasarım; harekeli Arapça için tam yazı tipi kendi sitemizden (Google Fonts yok);
  ar-ge'de kayma görünümü (ardışık birimlerin garaz özetleri, birinci vecihlerin bağları); D5 S7'yi beklemez (kimlikler
  değişmeyen taslaklardan sonradan üretilir). D5 okuma sayfası (`d1-d5-sayfa.py`) yeni platforma taşınır.
  **Ar-ge masasının ekleri** (kullanıcı kabul etti, 2026-11-21): (a) **okuma görevleri** (2026-11-21: yalnız deneyler için, elle açılır; bkz. D5 "D5'te okuma") (kullanıcının fikri: "benim
  veya ehil birinin yapması gereken okumalar ve gönderdiği notlar otomatikleşmeli"; dağınık okuma sayfaları toplanır):
  okumalar kutusu (atanmış okumalar, yer sayısı, süre, durum, sekmede bekleyen sayısı), yazdıkça sunucuya kayıt
  (dışa aktarma kalkar; telefonda yarım, bilgisayarda devam), bitince haber ve taslak deposuna kendiliğinden, okuyucu
  hesabına bağlı (ad yayımlanmaz, sabit numara), kör okumada taraflar karar gönderilene kadar sunucuda saklı;
  (b) **deneyler defteri**: her deneme bir kayıt (ne sınandı, kollar, maliyet, makinelerin ölçüleri, okuyucunun
  kararları, verilen karar); **şimdiye kadarki bütün sürümler de yazılır** (kullanıcının isteği: istem h1–h12,
  düzeltme d1–d3, eleştirmen ve ölçü sürümleri, D11–D15 ve D5.0'ın denemeleri; `docs/d1/*-istemi.md` "Sürümler",
  KAYIT.md, `data/d1/provalar/*`), bundan sonrakiler de; (c) **alet ayarı**: okuyucunun kararlarıyla makinelerin
  (kör eleştirmen, İşârât karşılaştırması, kapalı eleştirmen) örtüşmesi, okuma biriktikçe; (d) **notun hayatı**: açık
  → işlendi → kapandı, işleyen sürüme bağlı, silinmez; (e) **arama**: bütün taslaklarda ve notlarda (tutarlılık).
  Arayüz: Pano · Okumalar (n) · Birimler · Deneyler · Arama; telefonda da. Zemin: `/taslak/` girişinin servisinin
  (`site_auth.py`) yanında küçük bir veritabanı (okumalar, notlar, deneyler, kararlar), her gece taslak deposuna kopya.
  (f) **okuyucu notundan düzeltme** (kullanıcı kabul etti, 2026-11-21): bir okumada bulunan hata, kapının notları gibi
  düzeltmeye verilebilir; yalnız okuyucunun istediği birimde, elle başlatılır ("notlarımla düzelt"), kuyruk
  kendiliğinden yapmaz. Yazar her notu karşılar ya da gerekçesiyle reddeder (kapı d3'ün kuralları: yeni kaynak yok);
  yeni sürüm açılır, eski silinmez, fark masada. Sonraki birimler eski sürümü görerek yazılmış kalır (geri sarılmaz).
  ≈1–3 $ bir tur.
  **Yapılanlar (2026-11-21):** S7.1 yayın dosyası (`scripts/d1-yayin.py`, `2846310`: değişmez sürümler
  `data/d1/yayin/bakara/<birim>/v<k>.json`, içerikten paragraf kimliği, sahiplik, kalan kuşkulu atıflar, kapı özeti,
  eksik notları, kaynak metinleri; her D5 biriminden sonra). S7.2'nin zemini (`9ab73f8`, ana makinede): masa servisi
  `src/risale_mcp/masa.py` (`/taslak/api/`, `data/masa.db`: görevler, kararlar silinmez, kör eşleme sunucuda,
  notlar ve geçmişi, jetonla görev açma ve dışa aktarma, ad yok); okuma sayfaları kararları sunucuya yazar, "Okumayı
  bitir" tarafları açar (`d1-tur.py okuma-tek`, görevsiz eski düzen `--gorevsiz`); `scripts/masa-gorev.py ac | al`
  (jeton `~taslak/.masa-token`, yerelde `.env` `MASA_TOKEN`).
  **Yapılanlar (2026-11-21, ikinci kısım; ayrıntı KAYIT.md "S7"):** masanın girişi (Pano · Okumalar · Birimler),
  birimin ar-ge görünümü (`/taslak/birim.html`: bütün taslaklar, yan yana, kapı ve eleştirmen ham, nisbet, notlar),
  okuma platformu `/oku/` (S7.3: Kur'ân paneli, âyete git, yalnız son taslak, 1–33'te önce İşârât, Arapça ve izah
  açılır, atıfta kaynağın metni ve adı, işaretler, künye, eksik notları, Risale'deki yerler, 13 müfessir, ders kutusu ve
  Risale'deki genişi, konu araması, kesintisiz okuma, indirme ve atıf satırı, kaldığı yer, usul sayfası), okuyucu notu
  (S7.4: sürüme ve paragrafa bağlı, seçilen söz, geri çekme; okuyucu yalnız kendininkini görür), "notlarımla düzelt"
  (S7 (f), elle), deneyler defteri, alet ayarı, kayma, arama; hesap kapsamı `oku` (davetli okuyucu masaya giremez).
  **S7b (kullanıcının eleştirileri, 2026-11-21) yapıldı:** masa tam genişlik, platformda ölçülü metin ve kaynak yan
  sütunu, Kur'ân paneli açılıp kapanır, renkler (kaynak mavi, etiket turuncu), `[dil; 35]` atıfları tıklanır; masanın
  birim sayfası eski âyet masası, genişletilmiş (Kur'ân paneli, 6 yan, kapı/nisbet/not yanları lafız süzgeciyle).
  **Konuşulacak (kullanıcı):** masanın kolaylıklarından hangileri okuma platformuna taşınacak.
  **S7c. Âyet masasının sadeleşmesi ve kaynakların Türkçesi** (kullanıcının kararları, 2026-11-21; kullanıcı "eski
  masa iyi, ama etraf çok dağınık ve çalışması zor" dedi; **hepsi yapıldı**, sonuçlar aşağıda "S7c–S7g"). Sıra:
  - **S7c.1 Sadeleşme:** kör kip kalkar (kör okuma görevli sayfalarda, taraflar sunucuda; kör okuması süren birimin
    masasında yalnız üstte uyarı "bu birimin kör okuması sürüyor"); üstteki tur ve fark okuması bağlantıları kalkar
    (Pano › Okumalar ve Birimler sekmesinde var; birimin kendi okumaları Kur'ân panelinde birimin altında küçük
    bağlantı); D7–D9'un işaretleme araçları **tamamen kalkar** (işaret sayacı, okuyucu adı, dışa ve içe aktarma,
    örneklem, sistemli başlık ve bilirkişi işaretleme listeleri, işaret düğmeleri; kullanıcının kararı); üst satır:
    ☰ · birim · + yan · Dil.
  - **S7c.2 Yan içinde içindekiler ağacı** (seçicinin yerine; açılır kapanır): Kaynaklar › İşârât · Tefsirler (13
    müfessirin adı) · Klasik eserler · Risale-i Nur'daki yerler; Taslaklar › her taslak (sürümüyle); Model
    eleştirileri › kapalı eleştirmen · açık eleştirmen · İşârât karşılaştırması; Nisbet denetçisi; Kalite kapısı;
    Okuyucu notları. Yaprağa tıklayınca yan onu gösterir (ör. Râzî, Beyzâvî ve bir taslak üç yanda yan yana); lafız
    seçiliyse dallarda o lafza düşen sayı; uzun içerikte bölüm atlama (Mukaddime, vecihler, Dersler).
  - **S7c.3 Lafız düğmelerinin sayısı:** D5 birimlerinde (İşârât yok) İşârât'ın nükte sayısı yerine taslak paragrafı
    ve not sayısı.
  - **S7c.4 İşârât'ta Arapça–Türkçe eşlemesi: önce sınama** (kullanıcının şartı: cümle düzeyinde mümkün olmayabilir).
    Birkaç birimde (ör. 13, 28, 30) Arapça cümlelerle Abdülmecid tercümesinin cümlelerini eşlemeyi dene: önce program
    (âyet ve Arapça alıntılar iki metinde ortak çapa; aradaki cümleler sıra ve uzunlukla), gerekirse model; sonuç
    örneklemle kullanıcıya: cümle düzeyinde tutuyor mu, yoksa paragraf ya da bölüm düzeyinde mi kalmalı. Karar ondan
    sonra; tutarsa eşleme kalıcı veri, masada ve platformda Türkçe dilde İşârât kaynağı Abdülmecid tercümesiyle.
  - **S7c.5 Taslağın andığı tefsir ve klasik yerlerin tercümesi:** birim kurulurken taslağın atıf yaptığı cümleler
    (birimde ≈30–50 kısa parça) hafif modelle, "Yapay zekâ tercümesi" damgalı, alıntının altında ayrı; lisans satırı
    (OpenITI, CC BY-NC-SA 4.0: türetilmiş eser, ticari değil, aynı lisans). Dil Türkçe iken kaynak kutusunda Türkçesi
    önde. Kaynaklar yanındaki bütün tefsir birimlerinin tercümesi **sonraya** (kota D5 ile ortak; istenirse birim
    başına düğmeyle sıraya).
  **S7c–S7g: sonuçlar ve oturumdaki kararlar** (2026-11-21; kullanıcının okumasından ve eleştirilerinden; ayrıntı
  ve commitler KAYIT.md "S7"):
  - **S7c'nin sonuçları.** (1) Sadeleşme yapıldı (kör kip, tur bağlantıları, D7–D9 işaretleme araçları kalktı).
    (2) İçindekiler ağacı her yanda; her müfessir ve her taslağın eleştirileri ayrı yaprak. (3) D5'te lafız sayıları
    taslaktan. (4) **İşârât eşlemesi:** program envanterle %77 (±1 cümle %88), model 3 birimde 163/164 → kullanıcının
    kararı: **model**; Fâtiha ve Bakara'nın 37 bölümü (2706 Arapça cümle, ≈7 $; `isarat-esleme.py --butun`,
    `data/d1/isarat-esleme/esleme.json`, rapor `esleme-rapor.md`); Bakara 17–20'nin belâgat faslı ve 10 mesele
    Türkçede karşılıksız. (5) **Kaynak tercümesi:** yalnız taslakların andığı yerler (kullanıcının kararı; bütün tefsir
    birimlerinin tercümesi sonraya), 528 parça (`data/d1/tercume/kaynaklar.json`); ilk koşu sıralı ≈2 saatti, 3 paralel
    ve orta düşünmeyle hızlandı; D5'te her birimin adımı (bkz. D5).
  - **S7c2 Masanın üst satırı ve katmanları** (kullanıcının dört maddesi, 2026-11-21): âyet seçicisi kalktı (Kur'ân
    paneli yeter); sağ üstte büyük düğmeler Masanın girişi · Okuma platformu · Çıkış; okumalar Kur'ân paneline
    karışmaz, yalnız masanın girişinde; katmanlar bugünkü hatta göre: Kalite kapısı (yazarın cevabıyla, son taslağa
    taşınmış), Nisbet, İşârât karşılaştırması, eski D9 eleştirmeni yalnız o eleştirinin yapıldığı birimlerde (kapalı
    ve açık kitap eleştirileri de öyle). Bulunan hata: 30'un taslak 4'ünde eleştirmen notları görünmüyordu (düzeldi).
  - **S7d Masa tek kabuk, bütün âyetler** (kullanıcının kararları): masanın girişinde dört büyük düğme (Âyet masası,
    Okuma platformu, Deneyler defteri, D5 durumu); âyet masasının küçük giriş sayfası (ne olduğu, "soldan bir âyet
    seçin"); Kur'ân paneli sûrelere göre, Fâtiha'nın 7 âyeti (İşârât'ın lafız bölümleri âyetlerine dağıtılır, Besmele
    1. âyet; `d1-masa.FATIHA`) ve Bakara'nın 176 birimi; taslağı yazılmamış birimde yalnız kaynaklar (İşârât işlediği
    yerde, her yerde tefsirler, klasik eserler, Risale'deki yerler), sayı yok, taslak yazıldıkça kendiliğinden gelir;
    **veri birim açılınca yüklenir** (kullanıcı: "site çok büyüyebilir, altyapıyı sağlam kuralım"; `ayet.html` +
    `masa-veri/<b>.json`, birim başına 0,1–2 MB); eski `<b>.html` yönlendirme.
  - **S7e Türk hattı** (kullanıcının kararı): Kur'ân metni masada, platformda ve D5 sayfalarında varsayılan Türk
    hattıyla (risaleoku), Medine seçilebilir (masada "Hat", platformda âyetin altında); yalnız görüntü, araçlar ve
    eşleme Tanzil'de. Taslakların içindeki âyet alıntıları Tanzil'den geldiği için Medine imlâsıyla kalır.
  - **S7f Alıntının cümlesi** (kullanıcının sorusu ve kararı): İşârât alıntısının Türkçesi eşlemeden Abdülmecid
    Nursî tercümesi (modelinki değil); cümleden koparılmış alıntıda "kaynaktaki cümlenin tamamı"; müfessir
    alıntılarında yapay zekâ tercümesi kalır.
  - **S7g Etiketler** (kullanıcının önerisi): taslağın kendi paragraflarındaki "Yapay zekâ tercümesi" ve izah etiketi
    kalktı; damga sayfa başında ve platformun üst çubuğunda her zaman; alıntı ve alıntının tercümesi etiketli kalır
    (kaynağın sözü ile modelin sözü karışmasın); atıf satırı ve indirilen dosyalar damgalı.
  - **Görüntü düzeltmeleri:** tur okuma sayfaları ekranın tamamı, numarasız etiketler turuncu; okuma kartında aynı
    alıntının iki kez çıkması (kart kurma hatası, `d1-tur.dedupe`); Türkçe metnin içindeki Arapçada Kur'ân işaretleri
    (U+06DF) boş kutu çıkıyordu → bütün sayfalarda Türkçe yazı tipi listesine sitenin Naskh'ı yedek (kullanıcı:
    "düzeldi").
  - **Altyapı:** masanın bütün çıktısı yeniden üretilir ve git dışındadır (`data/interim/oku-masa/`: `ayet.html`,
    `masa-veri/`, giriş, pano, deneyler defteri; iki makine yazıp `data/d1`'de çakışıyordu); hepsini kurmak sunucuda
    `d1-masa.py --hepsi` (≈25 dk, `d1-arka.sh`); sunucuya geçen kod kuyruk durmuşsa hemen, sürüyorsa sıradaki birimde.
  **Kararlar (kullanıcı, 2026-11-21, oturum):** sıra: birimin ar-ge görünümü (hafif: ham notlar, nisbet, kapının
  kabul ve retleri, düzeltme farkı, alarmlar) → S7.3 → S7.4; deneyler defteri, alet ayarı, arama sonra, D5'i
  beklemeden. **Ar-ge masasında da** Kur'ân paneli ve okuma platformunun kolaylıkları olur (kullanıcı: "unutma").
  Platform: aynı davetli hesaplar, ayrı yol (`/oku/`; masa `/taslak/`'ta). Yayın: D5'te bütün birimler; Bakara 1–33
  vitrin (önce İşârât, yanında taslak); **okuma platformunda yalnız son taslak, ar-ge masasında hepsi.** İlk davetliler
  kullanıcının işi.
  **Ekler** (kullanıcı kabul etti, 2026-11-21): (1) **her alıntıda kaynağın adı ve bağlantısı** (izinlerin şartı:
  e-Risale, risaleoku, müfessirin baskısı, Vakıf meali; zorunlu); (2) **usul sayfası** "Bu taslaklar nasıl
  yazılıyor" (hat, kapı, ölçüler, eleştirmenin isabeti, yapay zekânın yapamadıkları, neden "tefsir" denmez; künyeler
  buraya bağlanır); (3) **taslaklar yan yana** (yalnız masada; aynı birimin taslakları vecih vecih; vecih haritasının
  öncüsü); (4) **indirme ve atıf biçimi** (birimin yayın dosyası ve düz metin, sûre tek dosya; paragrafın hazır atıf
  satırı "Risale MCP yapay zekâ taslağı, Bakara 2:30, sürüm 2, paragraf …"); (5) **âyetle gitmek** ("2:255" → birim);
  (6) **kaldığı yer** (tarayıcıda). Önerilmeyenler: beğeni ya da "faydalı" işareti (meşrebe göre oy gibi işler),
  çevrimdışı uygulama ve yazdırma. Arayüz minimal ve basit (kullanıcı). Kullanıcı yokken deploy izni verdi (bu iş için).
  **Sıra:** S7.1 veri katmanı (yayın dosyası, kalıcı paragraf kimlikleri, sürümler) → S7.2 ar-ge masası (pano girişte,
  birim başına eleştiri, nisbet ve kapı) → S7.3 okuma platformu ilk sürüm (Kur'ân paneli, birim sayfası, izah, atıfta
  kaynağın metni, künye, işaretler) → S7.4 okuyucu notu (sunucuda, kalıcı adrese bağlı). S7.1 ve S7.2 D5 dönerken
  (model çağrısız).

**D15. Saklı birimlerde son ölçüm** (bitti, 2026-11-20, kullanıcının kararı: rapor `data/d1/d15-rapor.md` uygun, hat h9; aşağısı kayıttır) (kullanıcının kararı, 2026-11-17: kendi aşaması; "D5'ten önceki son düzlük, o
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
  yerine 26–27'nin h9 taslağı verilir (D5.0.5); istem değişmez, birinci vecih raporda ayrı ölçülür. (3) **30 yedekte:**
  D5.0'ın kabul birimi; D15'e, soru kalıpları listesinin yeniden kuruluşuna ve hiçbir denemeye girmez (25 ve 29
  harcanabilir). Maliyet birim başına ≈14–15 $, toplam ≈45 $: iki pencere.
- **D15 yazılırken yan yana** (kullanıcının isteği, 2026-11-19; aynı gün geri alındı: "birkaç işi aynı anda yapabilirim
  diye düşünmüştüm, fakat bunda çok zorlandım"): D5.0.4 birim bölmesi yapıldı ve plana yazıldı, S7 konuşulup plana
  yazıldı; ikisi de yeri gelince sürer. D15 boyunca önde tek iş.
- **Hat h9; h10 bırakıldı** (kullanıcının kararı, 2026-11-20, D15.1'den sonra: "h9 gerçekten daha akıcı ve açık bir
  şekilde yazıyordu"). Gerekçe: kullanıcının okuması iki birimde de h10'dan yana değil (14–15: h10 1, emin değil 2;
  21–22: h9 6, h10 1); h10'un tek açık kazancı (14–15'te envanter +15 puan) 21–22'de tekrar etmedi (%40 / %42),
  kusurları tekrar etti (Tarama'da zorlama, çelişki, müfessir adı, tercümeyi topluca verme); okuma platformu
  kararından sonra akıcılık asıl ürünün niteliği. "Üç birimde ikisi" kuralı erken bırakıldı (üçüncü birim tabloyu
  ancak eşitlerdi). **D15.2 ve D15.3 yalnız h9:** envanter, İşârât karşılaştırması, kör aletlerin ayarı (kapalı
  eleştirmen ve nisbet artık h9 taslağında: D5'in hattı), kullanıcının "kendi başına yeterli mi" okuması (tek
  taslaklı kartlar). h10'un kodu (`--tarama`, soru kalıpları) durur. **D5'e açık soru** (kullanıcının 21–22 gözlemi):
  İşârât fâ'nın gerçekten hangi cümleye, hangi kelimeye bağlandığını sorar, taslaklar fâya bir mânâ verir; model
  edatın ve kaydın taallukunu sormuyor; liste de sordurmadı (D5.0'da konuşulur, D15 boyunca hat donuk).
- **h9 ikinci kol** (kullanıcının kararı, 2026-11-19; 2026-11-20'de yerini yukarıdaki karara bıraktı: "h10'dan biraz şüpheliyim"): üç birimde de h9 yazılır (21–22
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
  İşârât yan yana, hüküm yeterli / düzeltmeyle / yetersiz, aletler "Aç"tan sonra; ≈22 dk (okunmadı, yerine birleşik sayfa).
  **h9 kolu (2026-11-19):** taslak 2 (h9, ≈4,90 $; tercümeyi paragraf paragraf verdi, topluca verme h10'a özgü çıktı).
  Kapsama %42 (mukaddimesiz %53), fazla 25, çelişki 0 (h10: %40, %50, 44, 1). İşârât karşılaştırması "düzeltmeyle"
  (≈3,09 $; «لكم» ihtisası iki taslakta da; teâvün tefsirinin yanlış âyete nisbeti; vücud-vahdet-istihkak omurgası
  eksik). **Kör A/B (o3, ≈2,20 $): h9 bütünde ve dört bölümün dördünde hafif, me'hazda açık** (h10'da iki tercüme hatası
  «الآجلة» ve «الضمان», iltifatta İşârât'la çelişki, nükteleri müfessir adıyla kurma; h9 İşârât'ın nazîrlerini daha çok
  kullanıyor; h10 «تجعلوا» ve «لله»da üstün; h9'un kusurları: Beyzâvî'nin zayıf dediği vechi kaydını düşürerek verme,
  Keşşâf'taki bir nükteyi istinbat sayma, bir Risale sözünü değiştirme). **Birleşik okuma sayfası** (`d1-tur.py
  okuma-tek 21-22 --taslak 1 2`, kartlar `provalar/21-22/yerler-D15.1-ab.json`): 9 kart (önceki yedi yer iki taslakla,
  kör eleştirmenin ayırdığı iki yer: semânın iadesi, «لله»); A = h10, B = h9 (kör); iki soru. Birim ≈32,6 $.
  **Okuma (2026-11-20): h9 6, h10 1, eşit 1, emin değil 1** (h9: «لكم» "olay gayet iyi özetlenmiş", fâ "çok daha
  oturaklı", mukadder sualler "olay akışı daha iyi", nimet dersi, semâ "İşârât'taki cihet mânâsını taşıyor", «لله»;
  h10: iltifat; eşit: takva dersi; emin değil: nübüvvet bağı). **Yeterlilik** (daha iyi bulunan için): yeterli 4
  («لكم», nimet dersi, takva, semâ), emin değil 3 (fâ, mukadder sualler, «لله»), yetersiz 2 (iltifat: İşârât'ın
  "meşakkat hitabın lezzetiyle karşılanır" mantığı yok; nübüvvet: İşârât'ın bağı yok, "taslaklar bambaşka bir yönden").
  Kullanıcının notları: "her şeyi de bulamazlar", modelin bir sınırı; fâ'da İşârât "fâ gerçekten hangi cümleye,
  hangi kelimeye bağlı" sorusunu cevaplıyor, taslaklar fâya mânâ veriyor: "bambaşka bir dünya". Kural 4.4: kör
  eleştirmen ve kullanıcı aynı yönde: **21–22'de h9.** Kullanıcı İşârât karşılaştırmasından (dört bölümde
  "düzeltmeyle") daha cömert: dokuz yerin dördünde "yeterli". Okuma dosyası `data/d1/notlar/d1-tur-21-22-D15.1-Fatih-*.json`.
  **D15.1 bitti.**
- **D15 bitince** (kullanıcının kararı, 2026-11-19): işi biten birimlerin prova veritabanları silinir
  (`data/interim/d1-prova/<birim>/risale.db`, `tefsir.db`; birim başına ≈1,5 GB, toplam ≈11 GB; yeniden üretilebilir,
  `d1-prova.py hazirla`). Envanter, taslaklar ve ölçüler `data/d1`'de kalır. 30'unki (kabul birimi) D5.0.9'a kadar.
- **D15.2 26–27 (2026-11-20; hat h9; ≈18,9 $):** birim kaydı (iki dilde tek düğüm; usul özetinin 3.3 "saat
  milleri" başlığı bütün dayanağı bu birimden olduğu için dayanağıyla çıktı); sızıntı testinde istem için kabul edilen
  ibare listesi eklendi (`sizinti_kabul_ibare`: usul özetinin alıntıladığı «عباراتنا شتى» beyti). Envanter 120 kalem.
  Taslak 1 (h9, ≈4,74 $; tercüme paragraf paragraf). Kapsama %44, fazla 57, çelişki 2. İşârât karşılaştırması
  "düzeltmeyle" (≈2,42 $; garaz ve omurga doğru, Risale dersleri yerinde; eksik: itiraz silsilesi ve iki silsile,
  «لا يستحيي»deki ilzam, tenezzülât-ı İlâhiye, teklif suali, nakzın tefriki; Müfredât'a aşan bir nisbet). **Kör aletler:**
  açık notların 16'sından kapalı 5'ini (+1 kısmen) buldu, 10'u yalnız gizli metinden, **görebileceği hâlde kaçırdığı
  yine 0**; kapalının tek kalan 20 notundan 13'ü yerinde, 6'sı şüpheli, 1'i yanlış (21–22'de 18/20: isabet düştü);
  nisbet 71 hükümde 11 "aşıyor". Okuma sayfası `tur-26-27-D15.2.html` (7 kart: beş "düzeltilecek", iki Risale dersi;
  tek taslak ve İşârât; ≈29 dk). **Okuma (2026-11-20): yeterli 2, düzeltmeyle 2, emin değil 1, yetersiz 2.** Yeterli:
  «لا يستحيي» ("«لا يترك» ile kıyas yok, fakat mânâ orada"), hüsran ve önceki âyetlerle bağ ("ana fikir orada"; asıl
  sorun kaynak nisbeti, kapalı eleştirmenin bulduğu). Düzeltmeyle: «فيقولون» (mukabilin muktezası «فلا يعلمون» yok;
  İşârât'ın îcâzı: "bilmez, tereddüde düşer, inkâra girer, istifham şeklinde istihkar eder"), halk ve kesb dersi
  (İşârât'ın asıl mânâsı imtihanın gerekliliği; Risale'nin "Ebû Cehil ile Ebû Bekir arasındaki fark bilinsin"
  kısımları da münasip düşerdi). Yetersiz: itiraz silsilesi ("İşârât'ın açıkladığı kadar kapsamlı değil"), nakz
  ("İşârât'ın temsili ve hayali kapsayıcı anlatışının yanında"). Emin değil: sivrisinek dersi ("ders âyetle bağlantılı,
  ama İşârât işin başka yerinde": İşârât zâhiren basit misallerin zikrinin hikmetini, taslak o varlıkların aslında
  mânidar olduğunu anlatıyor). Gözlem: kullanıcı İşârât karşılaştırmasıyla bu birimde aynı ölçüde; taslak garazda ve
  mânâda yeterli, İşârât'ın kendine has takdir zincirlerinde ve temsillerinde değil (21–22'deki iltifat ve nübüvvet
  gibi). Okuma dosyası `data/d1/notlar/d1-tur-26-27-D15.2-Fatih-*.json`. **D15.2 bitti.**
- **D15.3 28 (2026-11-20, başladı):** birim kaydı; D5.0.5 için `onceki_taslak` (kaynak dosyasının 1. bölümü: önceki
  birimin taslağı, "İşârât değil, atıf verilemez" notuyla; `d1-hat._taslak_prev`) ve `ek_gizle` (İşârât'ın 26–27'si
  prova veritabanından da silinir; sızıntı testi yalnız 28'e bakar). Usul özeti ve çizelgeden 28'in örnekleri çıktı;
  kabul: müellifin birim başı kalıbı «اعلم أن لهذه الآية أيضاً الوجوه الثلاثة النظمية». **Ölçüldü (≈12,2 $; küçük
  birim, envanter 55 kalem):** taslak 1 (h9, ≈3,36 $). Kapsama **%64** (21–22 %42, 26–27 %44), fazla 30, çelişki 2.
  İşârât karşılaştırması bütünde "düzeltmeyle", mukaddime (beş düğümlü silsile) "yeterli"; "ciddi bir yanlış ya da
  uydurma yok". **D5'in şartı:** birinci vecih âyeti önceki iki âyete (fâsıkların vasfı, hüsran) sağlam bağladı; eksik
  olan İşârât'ın ileriye bakan ekseni (bu âyet ve sonraki üç âyet delil taşıyan nimetleri sayar), önceki birimle ilgili
  değil. Kör aletler: kapalı ilk kez İşârât'sız görülebilecek bir notu kaçırdı (1), yalnız gizli 8, eşleşen 3; kapalının
  tek notlarından 22/24 yerinde; nisbet 25 hükümde 2 "aşıyor". Okuma sayfası `tur-28-D15.3.html` (7 kart: öncesiyle bağ
  (D5'in şartı), nimetler ekseni, silsile, «كنتم/تكفرون», berzah, rücû, ölüm dersi; ≈27 dk). **Okuma (2026-11-20):
  yeterli 2 (rücû, ölüm dersi), düzeltmeyle 1 (öncesiyle bağ: "İşârât yalnız önceki âyete değil, önceden geçen bütün
  bahislere bakıyor; bizimki önceki iki âyete"), emin değil 2 (nimetler ekseni: "inâyete ve ibadete delil" tespiti yok;
  silsile: rücû açıklanmamış), yetersiz 2 («كنتم»: İşârât "âlem-i zerrâtta bir nevi vücud", taslak "yalnız mevtin
  mahalli", «تكفرون» nüktesi yok; berzah: hayat-ı uhreviye taslakta yok, "Risale-i Nur'da çokça bahsedilen ve ders
  verilmeye çok müsait"). **D15.3 bitti.**
- **D15'in raporu** (`data/d1/d15-rapor.md`, 2026-11-20): üç birimde 23 yer: yeterli 8, düzeltmeyle 3, emin değil 6,
  yetersiz 6 (kartlar bilerek zayıf yerlerden). Taslak garazı, omurgayı ve Risale dersini kuruyor; İşârât'ın takdir
  zincirlerini, taallukunu, temsil ve îcâzını, birinci vechin genişliğini yapamıyor. Kapalı eleştirmen İşârât'sız
  görülebileni neredeyse hiç kaçırmıyor (46 notta 1; kendi notlarında isabet %83), nisbet tamamlıyor. D5'in şartı yakın
  bağda tuttu. D5.0'a çıkanlar: hat h9; kalite kapısı (düzeltme en çok nisbet ve çelişki için); birinci vechin genişliği
  (önceki birimlerin garazı, sonraki âyetler); konu düzeyinde ders; taalluk sorusu; biçim denetimi. Harcama ≈64 $.
- **Birim kurulumu (her dilimin başı):** saklı birimler `d1-prova.UNITS`'te yok. `_dev_unit` gibi kayıt: Arapça ve
  Türkçe düğümler (Türkçede 21 ve 22 ayrı bölüm), vecihlerin ilk cümleleri (`sections`), ince Ek 3 için komşu
  birimler, usul özeti ve birim çizelgesinden o birimin örneklerini çıkaran düzeltmeler (`ozet`, `cizelge`; usul
  özeti maksat birimlerinden alıntı taşıyabilir: sızıntı testi gösterir). Sonra `d1-prova.py hazirla <birim>` (prova
  veritabanları), `d1-yz.py envanter <birim>`, `d1-hat.py hazirla <birim> --tarama`, sızıntı testi temiz olmalı;
  soru kalıpları listesi saklı birimlerden alınmadı (sızıntı testi temiz, `data/d1/kaliplar/sizinti-k1.md`).

**D14. Taslak hattının turları** (bitti, 2026-11-19, kullanıcının kararı: h10 taban; aşağısı kayıttır) (kullanıcının kararı, 2026-11-17: D12'nin kalanı ayrı aşama). **Taban h3** (D13; 9–10
taslak 5: me'haz hiyerarşisi, istinbat etiketi). İşleyiş D12.5'inki: her tur tek değişiklik, taban ve yeni kol, kör
eleştirmen (o3), envanter (ayar), kullanıcının okuması (plan belgesi `docs/d1/d12-rapor-ve-plan.md` 4.3, 4.4; okuma
standardı 4.10). Tur sayısına tavan konmaz: taslağın hazır ya da hazıra yakın olduğu okumada hissedilince D15'e
geçilir (kullanıcı); harcama tavanı ≈250 $ (D12.5 ve D13'te ≈60 $ harcandı).

**D13'ün okumasından çıkan iki sorun** (kullanıcı, 2026-11-17: "taslaktaki okumalarımda gördüğüm iki büyük problem"):
1. **Risale-i Nur anılıyor ama açılmıyor** ("Risale-i Nur'da da böyledir" deyip bırakmak; kizb ve sıdk dersi N41–N47
   yok; 22 Arapça paragrafın 6'sı Risale'ye dayanıyor). Üç sebep (kullanıcı: "çok kıymetli"): (a) dosyanın düzeni:
   267 paragraf kitap sırasıyla, âyetin bir sözünün dersi dağınık; (b) dil: taslak Arapça, Risale Türkçe, dersi açmak
   onu Arapçaya kendi sözüyle aktarmayı ister, kolayı adını anıp geçmek; (c) kural yazmak yetmez (D12'nin dersi).
2. **Akıl yürütemediği yerde Zemahşerî'ye yaslanıyor:** Keşşâf dosyadaki tek tefsir. Tabanın beğenilen "mantık
   silsilesi" de büyük ihtimalle dosyasındaki müfessirlerdendi; asıl eksik İşârât'ın kendi yolu (takdir zinciri,
   mukadder sual, "neden şu lafız").

**Kararlar (kullanıcı, 2026-11-17):** sıra önce D14.1 (ilk geçiş), sonra düzeltme (k3; 2026-11-17'de D14.2 ders adaylarına verildi, düzeltme D14.3 oldu); Risale'nin dersi **Arapça
metinde, kendi sözüyle ve atıfla** açılır, Türkçe tercümede gerekirse Risale'nin Türkçe aslından kısa alıntı;
Zemahşerî dosyadan çıkar, tefsirlerin başında araçla.

- **D14.1 Dosyanın düzeni** (sürüm h4; 9–10; taban taslak 5, yeni taslak 6). Tek değişiklik, "yazarın Risale-i Nur'u ve
  Zemahşerî'yi önünde nasıl bulduğu":
  1. **Risale-i Nur'un yerleri âyetin sözüne göre:** âyetin sözü → konusu → o konunun Risale paragrafları, benzerlik
     sırasıyla (kitap sırası değil). Yazar bir lafzı işlerken onun dersini tek yerde bulur. Seçim D13'ünkiyle aynı
     (konu başına ilk 100'ün üst yarısı).
  2. **Keşşâf dosyadan çıkar:** `tefsir` eklentisinde tefsirlerin başında; istemde "tefsirlere bakacaksan önce
     Zemahşerî". Dosyada belâgat ve lügat eserleri kalır.
  3. **İstemde dersin açılışı:** Risale-i Nur'un dersi Arapça metinde kendi sözüyle ve atıfla açılır; Türkçe tercümede
     gerekirse Türkçe aslından kısa blok alıntı (numarasıyla). Anıp geçmek yetmez.
  Ölçü: kör eleştirmen o3, envanter, D9.1, me'haz dağılımı (Risale'ye dayanan paragraf, Keşşâf'a atıf), uzunluk;
  okuma standardıyla 3 nükte. ≈10 $.
  **Yazıldı ve ölçüldü (2026-11-17; ≈9,6 $; rapor `data/d1/provalar/9-10/d14-1-rapor.md`):** taslak 6 (h4). Envanter
  %60 → **%74**; kör eleştirmen (o3) yeniyi bütün olarak ve me'hazda hafif tercih etti (V3'te İşârât'ın dört temel
  nüktesi; hasrın sualine cevap ilk kez); taban Mukaddime (dört maksat) ve V2'de (yedi cümle; yeni "altı cümle")
  hafif. Keşşâf atfı 16 → 10, belâgat atfı 7 → 13; Risale'ye dayanan paragraf oranı aynı (≈%28). "Altı cümle" 9–10'da
  üçüncü kez. Okuma `tur-9-10-D14.1.html` (N40, N01, N17; ≈708 kelime).
  **Okuma (2026-11-17):** taban 1 (N40: h4 kısalmış, mânâ kaybolmuş, Risale'den yorumsuz alıntı; h3 "böyledir" deyip
  geçiyor), eşit 1 (N01), yeni 1 (N17: "Zemahşerî'den alıntı alıp sıyrılma furyası artık yok"; ama kartın sorusu
  paragraflarla alakasızdı, okuma standardına kural eklendi). Kullanıcı: "bu sefer durum karışık." Kural 4.4: kullanıcı
  kararsız, eleştirmen hafif: başka birimde bir kez daha. **Karar (kullanıcı, 2026-11-17): h4 taban.** Bulgu: Zemahşerî'ye yaslanma giderildi; Risale'nin dersi iki
  kolda da açılmıyor (h3 anıp geçiyor, h4 yorumsuz alıntılıyor): talimat biçimi değiştirdi, düşünceyi değil. Karar
  bekliyor.
- **D14.2'nin hazırlığı: İşârât'ta üç vecih dışındaki kısımlar (bitti, 2026-11-17; ≈3,5 $; kullanıcının isteği:
  "dersin sabit bir yeri var mı, ne kadar uzun"):** `scripts/d1-yapi.py`, istem `docs/d1/yapi-istemi.md` y1, sonuç
  `data/d1/isarat-yapi/sonuc.md`. Sabit yer yok: münafıklar bahsinde (9–16) ders V3'ün içinde, kendisini doğuran lafzın
  yerinde (altı birimin beşinde; biçimi soru–cevap ya da "إشارة إلى"; lafız başına %3–11, birim başına ≈%10); iman
  rükünlerinde (17–33) mukaddime ve mesele olarak, çoğu kez V1'den önce (%13–45). 9–10'da sonda olması «يَكْذِبُونَ»'un
  son kelime olmasından. D14.2'nin kararı bu sonuçla (kullanıcı).
- **D14.2 Ders adayları ve tek kaide** (kullanıcının kararları, 2026-11-17; sürüm h5; 9–10; taban taslak 6 (h4), yeni
  taslak 7). Hazırlığın sonucu (yukarıda) ve kullanıcı: taslağı İşârât'ın usulüne yaklaştırmak ve Risale-i Nur'u daha
  çok dahil etmek için gerekli yerlere dersler ya da izahlar; Risale-i Nur'dan ve modelin kendi istinbatından, gerekirse
  öbür eserlerden; yeri, biçimi ve payı münasebete göre. **İşârât Risale-i Nur'dan önce yazıldı**: müellifin elinde
  külliyat yoktu, bizim var; İşârât'taki ders sıklığı üst sınır değildir.
  - **Tek kaide** (mukaddime kuralıyla birleşik): ders, meseleyi doğuran şeyin yanında verilir. Bir lafızdan doğuyorsa
    o lafzın yerinde (çoğu kez V3, cümleler arasıysa V2; soru–cevap ya da "إشارة إلى"); âyetin bütün meâlinden ya da
    bir iman rükününden doğuyorsa vecihlerden önce mukaddime, bir lafza bağlı büyük meseleyse vecihlerin arasında
    mesele. Uzunluk meselenin genişliğine göre; **bütçe toplamda** (Arapça İşârât'ın 1–2 katı), derse ayrı pay yok.
  - **Ders adayları programla** (`d1-hat.py`, yazımdan önce): her konunun iki sorgusunun ilk 100 sonucunda isabetlerin
    **yoğunlaştığı bölüm** birinci tetikleyici, **âyeti anan bölüm** ikinci; **eşiği aşan her aday** gelir (ilk eşik:
    bölümde en az 12 isabet; sonra ayarlanır); aynı metnin kopyaları (Tarihçe'deki Hutbe gibi) tek aday. Adaylar dosyada
    lafzın başlığı altında, bölümün ana teziyle. Konu adımı konunun kapsamını da yazar (lafız ya da âyetin bütünü); 9–10'un
    sekiz konusu önceki gibi (hepsi lafız; Risale seçimi h4'le aynı kalsın diye yeniden çıkarılmaz).
  - **Yazar** aday lafzı işlerken orada durur: münasebet güçlüyse dersi açar (Risale-i Nur'un dersi ve kendi istinbatı,
    Arapçada kendi sözüyle, atıfla), zayıfsa kısa atıfla geçer; biçim ve uzunluk onun. İstemde İşârât'tan ders örnekleri
    (sınanan birim dışındaki geliştirme birimlerinden, prova kuralıyla).
  - **Yazımdan sonra program sayar:** hangi adaylarda ders açılmış, Risale'ye atıf, yazarın kendi Arapça sözü mü yalnız
    alıntı mı.
  - **Yedek adım** (kullanıcı): yazar dersi ısrarla açmazsa program aday lafızlar için başlığı kendisi açar, yazar altını
    doldurmak zorunda kalır.
  - Ölçü: kör eleştirmen o3, envanter (N41–N47), D9.1, me'haz dağılımı ve ders sayımı, uzunluk; okuma standardıyla.
  - **Yazıldı ve ölçüldü (2026-11-17; ≈7,9 $ ve hazırlık 3,5 $; rapor `data/d1/provalar/9-10/d14-2-rapor.md`):**
    taslak 7 (h5). Risale'ye atıf 19 → 39, adaylara atfın taşıdığı söz her yerde arttı (Hutbe 0 → 31, İkinci Lem'a
    17 → 56) ama 60 kelimeyi bir yerde geçti; envanter %74 → %53, iki İşârât çelişkisi (elîm "mü'lim"; mü'minler zâhirde
    aldanır); kör eleştirmen bütünde tabanı, me'hazda yeniyi hafif tercih etti; "altı cümle" ilk kez yok. Okuma
    `tur-9-10-D14.2.html` (N40, N17, N38; ≈825 kelime).
    **Okuma (2026-11-18):** yeni 2 (N40: "konuyu daha iyi açıklamış… ama bizim istediğimiz mânâda bir Risale dersi
    burada yok"; N38: düşünce akışı net, Risale'nin fikri iyi söylenmiş), taban 1 (N17). Kural 4.4: eleştirmenle
    ayrılık, kullanıcının hükmü geçer: **h5 taban** (kullanıcı onayladı, 2026-11-18). Yedek adımın şartı oluştu: ders en güçlü adayda
    bile açılmıyor.
- **D14.3 Zorunlu ders başlıkları** (D14.2'nin yedek adımı; kullanıcının kararları, 2026-11-18; sürüm h6; 9–10; taban
  taslak 7 (h5), yeni taslak 8). Okuma: ders en güçlü adayda bile açılmadı. **Program başlığı açar:** ders adayının
  isabeti en az 25 olan lafızlar için üçüncü vecihte lafzın yerinde `### Ders: «…»` (9–10'da dört: يَكْذِبُونَ,
  مَرَضٌ, فَزَادَهُمُ, يُخَادِعُونَ اللّٰهَ); yazar altını doldurmak zorunda. **Dersin tarifi** (kullanıcının 9–10 ve
  31–33 örneklerinden): lafızdan kalkıp okuyucuya döner; lafzın nüktesinden insana, İslâm âlemine, beşere dair umumî bir
  hakikate geçer; müellifin biçimleriyle (temsil, soru–cevap, silsile, taksim, hitap) kurulur; kısa değildir; müellifin
  sözüdür. **Bu derslerin genişi Risale-i Nur'dadır** (9–10'un kizb ve sıdk dersi Hutbe-i Şâmiye'nin "Sıdk" kelimesi;
  31–33'ün mukaddimesi Yirminci Söz'ün İkinci Makamı): yazarın işi Risale'deki dersi telhis edip lafza bağlamaktır; D5'in
  işi de budur. 9–10 temiz sınav: gizli olan İşârât'ın kizb ve sıdk dersi (N41–N47), yazarın elindeki onun genişi.
  Alıntı en çok dayanak; bütçe toplamda, üst kısmı derse kullanılabilir (h5 bütçenin üçte birini kullanmadı). İkinci
  vecihte temsil serbest. Ek 4'e 31–33'ün mukaddimesinden bir parça eklenir (sınanan birim dışından). Ölçü: N41–N47,
  başlıkların doluluğu ve kendi sözü, kör eleştirmen o3, envanter (D14.2'deki düşüş izlenir), okuma.
  **Yazıldı ve ölçüldü (2026-11-18; ≈8,6 $; rapor `data/d1/provalar/9-10/d14-3-rapor.md`):** taslak 8 (h6). Dört
  başlığın dördü dolu; **İşârât'ın kizb ve sıdk dersinin yedi nüktesinden altısı ilk kez "kısmen"** (bugüne kadar
  sıfır); açılan ders 1 → 6, Hutbe'ye atfın taşıdığı söz 31 → 160 kelime; envanter %53 → %60; kör eleştirmen yeniyi
  **bütünde ve me'hazda açık** tercih etti. Ölçüm düzeltmesi: kaynak eşlemesi her sunucunun yalnız son `cite`
  çağrısını okuyordu, artık hepsini birleştiriyor. Okuma sayfası paragrafın devamını (alıntı ve tercüme parçaları)
  da gösteriyor. Okuma `tur-9-10-D14.3.html` (N40, N38, N16; ≈1.140 kelime).
  **Okuma (2026-11-18): yeni 3, taban 0** (N40: "Risale'den alınmış çok çok iyi bir ders, gerçekten bravo"; N38: "her
  türlü baştan sona B daha iyi"; N16: "açık ara, silsile yerinde"). Kural 4.4: eleştirmen ve kullanıcı aynı yönde, açık:
  **h6 taban.** N40'ın kartı nazım ile dersi karşılaştırdı (B'de ikisi beraberdi, kart yalnız dersi gösterdi): okuma
  standardına kural eklendi.
- **D14.4 Yeni birimde sınama: 13'te h2 ile h6** (kullanıcının kararı, 2026-11-18; dokuz taslağın hepsi 9–10'da
  yazıldı, ayar riski). Taban taslak 1 (h2, Tur 0'da kurulan istemle), yeni taslak 2 (h6). D13 ve D14'ün bütün kazancı
  tek A/B'de. Kurulumda konu adımına Arapça `lafiz` alanı eklendi (13'te konu modeli "neden"i Latin harfli okunuşla
  yazdı, başlığa cümle girdi) ve âyetin bütününe dair konunun ders başlığı mukaddimeye (tek kaide). 13'te iki zorunlu
  başlık: «ٱلنَّاسُ» (Yirmi Üçüncü Söz, 54 isabet), «أَلَآ إِنَّهُمْ هُمُ ٱلسُّفَهَآءُ» (Otuz İkinci Söz). Gerekirse sonra
  h6 üzerinde kapalı eleştirmenin zaaf profili.
  **Yazıldı ve ölçüldü (2026-11-18; ≈11,5 $; rapor `data/d1/provalar/13/d14-4-rapor.md`):** kör eleştirmen h6'yı
  **bütünde ve me'hazda açık** tercih etti (V3 açık; V1'de h2 hafif); envanter %62 → %74; Risale atfı 2 → 31, öbür
  tefsirlere atıf 37 → 4; iki ders başlığı dolu; h6 uzunluk hedefini %13 aştı (kısa birim). Okuma `tur-13-D14.4.html`
  (N43, N01, N21; A = h6, B = h2). Okuma kartına `ek_capa` (dersin nazım paragrafı) ve `sinir_asimi` seçenekleri.
  **Okuma (2026-11-18): h6 3, h2 0** (N43: "cümlenin parça parça nazmını vermede, Risale-i Nur'lara bağlamada, mantık
  silsilesini kurmada daha iyi"; N01: "yoruma gerek yok", eleştirmen burada h2'yi tercih etmişti). **h6'nın kazancı yeni
  birimde doğrulandı.**
- **D14.5 Uzunluk kuralı ve nisbet denetçisi** (kullanıcının kararları, 2026-11-18). Konuşma: kalan zaaflar (uzunluk,
  birkaç nisbet hatası, İşârât'la gerilimli istinbatlar, kaçırılan nükteler) için genel düzeltme yanlış ya da büyük
  alet (düzeltme uzatır; birim başına ≈11 $; k2 nakle iter); gerilimli istinbat ve kaçırılan nükteler ehlin okumasının
  (D5.1) konusu. Kullanıcı: "uzunluğu kısacağız diye kaliteden kaybetmek istemiyorum"; ders sayısına sınır yok.
  - **D14.5a Dersler uzunluk hedefinin dışında** (h7; 13; taban taslak 2 (h6), yeni taslak 3): hedef (İşârât'ın 1–2
    katı) yalnız nazım kısmına (üç vechin tahlili) uygulanır, çünkü İşârât'la kıyaslanabilir olan odur; dersler hedefin
    dışında, meselenin genişliğine göre, îcâzla, alıntı dayanak. Her dersin sonunda `### Dersin sonu` işareti (dersin
    uzunluğu ayrı ölçülsün). Ölçü: nazım kısmının uzunluğu, ders başına kelime ve alıntı, kör eleştirmen o3, envanter,
    okuma. Soru: dersler serbest kalınca ne kadar yazılıyor, nazım kısmı ve kalite ne oluyor.
  - **D14.5b Nisbet denetçisi** (`scripts/d1-nisbet.py`; mevcut taslaklarda: 9–10 taslak 8, 13 taslak 2, kontrol 13
    taslak 1): atıf verilen her kaynak için atıf verilen yer bağlamıyla ve ona atıf veren taslak cümleleri tek model
    çağrısında; hüküm: doğru nisbet, kaynağın naklettiği görüş, itirazı, reddettiği vecih, kaynakta yok, kaynağın sözünü
    aşıyor. Doğruluğu kör eleştirmenin bulduğu nisbet hatalarıyla ölçülür (Lem'alar'daki zamir; Âlûsî'nin naklettiği
    istidlal; adı anılmadan alınan Ebüssuûd tespiti). Güvenilirse D5.0'da üretim hattının kalite kapısı; cümle düzeyinde
    düzeltme adımı sonra.
  - **D14.5b bitti (2026-11-18; ≈4 $; rapor `data/d1/d14-5b-nisbet.md`):** isabet ≈%80 (beş bulgudan dördü doğru),
    yakalama ≈%45 (bilinen 13 hatadan 6'sı; kaçırılanların çoğu atıf verilen yerin dışında); **h6 taslaklarında nisbet
    hatası az** (2 ve 1; h2'de 11 ve 8). D5.0'da kalite kapısı; yakalama için bağlam genişletilebilir.
  - **D14.5a yazıldı ve ölçüldü (2026-11-18; ≈6,5 $; rapor `data/d1/provalar/13/d14-5a-rapor.md`):** taslak 3 (h7).
    Dersleri sınırdan çıkarınca toplam kısaldı ve hedefe girdi (13.581 → 11.613; nazım 8.558, dersler ≈1.500'er harf,
    derli toplu, işaretle kapanmış); kör eleştirmen h7'yi bütünde ve me'hazda hafif tercih etti; envanter %74 → %64.
    Okuma `tur-13-D14.5a.html` (N43, N03, N46; A = h6, B = h7).
    **Okuma (2026-11-18):** emin değil 2, h6 1 ("İkisi de ayrı güzel"; h7'nin "Müellif … saymıştır" cümleleri
    istenmiyor), h7 0: kalite denk. Kural 4.4: eleştirmen hafif, kullanıcı kararsız; h6'nın uzunluk bayrağı var, h7'nin
    yok. **Karar (kullanıcı, 2026-11-18): h7 taban**, üslûp notuyla (İşârât'ın öbür birimleri "Müellif … saymıştır"
    diye anılmaz; istemde, ayrıca sınanmadı). D14.5 bitti.
- **D14.6 D5'e hazırlık için iki deneme** (kullanıcının kararları, 2026-11-18; 13; taban taslak 3 (h7)). D5'te
  İşârât olmayacağı için uzunluk hedefinin dayanağı kalkıyor (D11'in oranı birimden birime 138–1.238 harf);
  yazar dosyadan yalnız en yakın Risale yerlerini kullanıyor (kullanılanların konu içi sırası çoğunlukla 1–5; ilk 10
  ≈%93'ünü karşılıyor); istemin büyüklüğü maliyete az yansıyor (3 kat istem, %5–40 maliyet).
  - **D14.6a Uzunluk sınırı yok** (h8a, taslak 4): h7'nin aynısı, uzunluk hedefi yok (îcâz kuralı kalır). Soru: model
    doğal olarak ne kadar yazıyor, kalite değişiyor mu. Kullanıcının kısa okuması.
  - **D14.6b Risale yerleri konu başına ilk 10** (h8b, taslak 5): h7'nin aynısı, dosyada konu başına benzerlikçe ilk 10
    paragraf (ders adayları aynı: ilk 100'deki yoğunluktan). Soru: odak ve maliyet; mekanik ölçü ve kör eleştirmen,
    eleştirmen düşüş görürse okuma.
  - **D14.6 ölçüldü (2026-11-18; ≈13,3 $; rapor `data/d1/provalar/13/d14-6-rapor.md`).** (a) h8a: sınırsız model
    şişmiyor (toplam 11.613 → 11.506; nazım kısaldı, dersler uzadı); kör eleştirmen h7'yi hafif tercih etti, envanter
    %64 → %70; okuma `tur-13-D14.6a.html` (N43 ders, N35, N17; A = h7, B = h8a). (b) h8b: maliyet %11 düştü (3,72 →
    3,29 $), kör eleştirmen h8b'yi bütünde hafif tercih etti (me'haz eşit), envanter %68; dersler uzadı (2.519 ve 3.066
    harf), toplam 14.217; okuma gerekmiyor.
    **D14.6a okuması (2026-11-18):** eşit 1, emin değil 2: kalite denk; sınırsız tarafta paragraf düzeyinde uzatma
    (sefehin lügat mânâsı) ve tekrar kalıbı (art arda üç "Denilmiştir ki"); "îcâz söz konusuysa A'yı tercih ederim".
    Taslaklar arası farkları doğal fark sayıyor. **Karar (kullanıcı, 2026-11-18): h9 = h7 + uzunluk hedefi yok (h8a) +
    konu başına ilk 10 Risale yeri (h8b) + îcâz notları** (lügat mânâsı bir iki cümle; aynı kalıp art arda kullanılmaz;
    nükte bir yerde söylenir); ayrı sınama yok, derslerin uzaması D15'te izlenir. D14.6 bitti.
- **Genel düzeltme (k3) ertelendi** (2026-11-18): D15'te h6'nın çözemediği türden kusurlar çıkarsa yeniden açılır.
- Sonraki adaylar: garaz (kapanış dersi garazdan sapıyor), başka birim (13), takdir zinciri alanları, üslûp belgesi.
  Nisbet denetimi ve uzunluk şimdilik gerekmiyor (h3'te nisbet hatası çıkmadı, uzunluk hedefte).

**D14.7 İşârât'ın soru kalıpları ve tarama tablosu** (kullanıcının kararı, 2026-11-18: ar-ge adımı; tutarsa D15'in
hattı h10, tutmazsa h9). Sebep: üç taslağın üçü de 13'te İşârât'ın aynı nüktelerini kaçırdı (cumhura ittiba, fâsıla,
i'raz): oynaklık değil, yazar bazı soruları hiç sormuyor; usul özetinde bu kalıplar yok ("fâsıla", "i'râz", "iltifat",
"meçhul", "hazf" hiç geçmiyor). Kullanıcı: istemde liste durursa model takip etmeyebilir (h5'in dersleri gibi); bu yüzden
program uygular (h6'nın başlıkları gibi).
- **(1) Liste:** İşârât'ın birimden birime tekrar ettiği soru kalıpları (≈20–30; her biri soru, İşârât'ın tipik
  cevapları, örnek yerler). Kaynak yalnız geliştirme birimleri: 9–10, 11–12, 13, 31–33'ün envanterleri ve metni;
  Fâtiha, 1–8, 17–20, 23–24'ün metni. 14–15 (sınanan), 16 (yedek temiz birim) ve saklı birimler (21–22, 25, 26–27, 28,
  29, 30) girmez; sızıntı testi hepsine karşı. Kalıp cümle değil türdür. Kullanıcı onaylar.
- **(2) Tarama tablosu:** yazımdan önce program birimin lafızlarına sorulabilecek kalıpları çıkarır (kurallı: fâsıla,
  tarif lâmı, te'kid edatları, ayırma zamiri, meçhul fiil; küçük model çağrısı: hazf, iltifat, sîga). Âyetin kendisinden
  kurulur, İşârât'tan değil.
- **(3) Yazar:** taslaktan önce "Tarama" çalışma bölümünde her satıra "taşıyor" (nükte bir cümle, taslakta yerinde
  açılır) ya da "taşımıyor" (yarım cümle gerekçe) der; "taşımıyor" meşrudur. Program Tarama'yı yayımlanan taslaktan
  çıkarır, ölçü için saklar (kaçırılan nükte tabloda yok muydu, yoksa yazar "taşımıyor" mu dedi).
- **(4) Sınama:** 14–15 (hiç dokunulmamış geliştirme birimi; konu, ders adayları, envanter kurulur), h9 ve h10 (h9 + liste
  + tarama). Ölçü: envanterde kaçırılan nükteler azaldı mı, zorlama var mı (kör eleştirmen ve kullanıcının okuması).
  ≈20 $.
- **(1) bitti (2026-11-18; ≈4,3 $):** `docs/d1/soru-kaliplari.md` k1, 35 kalıp (kelime 18, cümle 8, cümleler arası 4,
  âyetin bütünü 5); sızıntı testi temiz; dört örnek kaynakla doğrulandı. Kullanıcı onayladı. **Kararlar:** (a) üç kalıp
  tabloya girmez, yalnız listede kalır: vecihlerin çokluğu, kayıtların tek garaza akması, dört esas maksadın remzi
  (bütün âyete bakan usuller; zorlama riski); (b) **h10 taban olursa D5.0'da liste bütün İşârât'tan yeniden kurulur**
  (bugün yalnız geliştirme birimleri; D15'ten sonra saklı birimler de girebilir).
- **Listenin modele verilişi** (kullanıcı onayladı, 2026-11-18): üç parça. (a) **Ek 5:** listenin tamamı (dağarcık:
  cevap türleri ve dikkat notları). (b) **Tarama tablosu** istemin gövdesinde, birime özel: program âyetin metninden
  kurar (fâsıla her âyette kuralla; öbürleri küçük bir model çağrısıyla, İşârât'sız), satırlar `T01…` (lafız, kalıp).
  (c) **Yazar çıktısında doldurur:** iş sırası kaynakları oku → Tarama → taslak; çıktı `## Tarama` bölümüyle başlar,
  her satıra "taşıyor: …" (taslakta yerinde açılır: kelime üçüncü vecihte, cümleler arası ikinci vecihte) ya da
  "taşımıyor: …" (meşru; dikkat notuna uyuyorsa doğru cevap); tablo taban, tavan değil; Türkçe ve kısa. Program
  Tarama'yı taslaktan ayırır (`taslak-N.tarama.md`), eksik satırları raporlar, kaçırılan her nükte için "tabloda yok /
  yazar taşımıyor dedi / taşıyor deyip yazmadı" ayrımını ölçer. Ayrı tarama çağrısı önerilmedi (maliyet; notları
  yine atlayabilir).
- **D14.7 ölçüldü (2026-11-18; ≈18,3 $; rapor `data/d1/provalar/14-15/d14-7-rapor.md`):** 14–15, taslak 1 (h9), taslak
  2 (h10). **Envanter %52 → %67**; kör eleştirmen h10'u bütünde ve me'hazda hafif tercih etti (te'kid nükteleri
  İşârât'la uyumlu; V2'de h9 hafif); Tarama 60 satır, hepsi cevaplı, taşıyor 57 (zorlama riski); çelişki 1 → 3, müfessir
  adı 5 → 11; h10'un kusurları: Âlûsî'ye nisbet, "meşkûk küfür"ü kapsamını aşarak uygulamak. Okuma
  `tur-14-15-D14.7.html` (N35, N09, N64; A = h10, B = h9).
  **Okuma (2026-11-19):** h10 1 (N09: "soruya A daha iyi cevap veriyor … daha derli toplu"), emin değil 2 (N35'te
  h10'a "his olarak"; N64'te h9'un dersi, ama kart h10'un «يَعْمَهُونَ» dersini göstermemişti: kart hatası). Kural 4.4:
  eleştirmen ve kullanıcı aynı yönde (h10). **Karar (kullanıcı, 2026-11-19): h10 taban; D14 bitti.** Hat D15 boyunca
  donar; zorlama (Tarama'da "taşımıyor" oranı), çelişki ve müfessir adı D15'te ölçülerek izlenir, düzeltme gerekirse
  D5.0'da. Okuma kartları için ders kuralı: bir tarafın kartında bir lafzın dersi görünüyorsa öbür tarafın aynı lafız
  dersi de karta girer (D14.7'nin N64 kartında h10'un dersi görünmemişti; D15'in başında `d1-tur okuma`'ya eklenir).

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

**S6. Âyet masasının ikinci hâli** (bitti, 2026-11-17, kullanıcının kararı; kullanıcının fikirleri, 2026-11-16; "Sonra"daki masa açıkları buraya bakar):
- Sol ve sağ yanda ne duracağını kullanıcı seçer (kaynaklar ya da bir taslak); iki taslak yan yana karşılaştırılır.
- Yapay zekâ kısmının odağı taslaktır; İşârât'la karşılaştırma, eleştirmen ve bilirkişi soruları taslağın yanında
  sekme değil, taslağın üzerinde açılan ayrı birimlerdir.
- Üstte "Önceki âyetlerle münasebet"in yanında "metinlerin tamamı" düğmesi; kaynaklardaki "İşârât'ın bu birimdeki
  metninin tamamı" ve taslaktaki "bütün taslağı göster" onunla kalkar.
- **Düzeltildi (2026-11-16):** masa tek birimlikti; 31–33 kurulunca 11–12'nin sayfası üzerine yazılmıştı ("Âyet"
  seçicisinde 11–12 yoktu). Artık birim başına sayfa: `data/d1/masa/<birim>.html`, `index.html` son birim; seçici
  öbürüne gider; deploy klasörü gönderir.

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
- S4.7 ve kapanış (2026-11-22 – 2026-11-23; "Şimdi" bloğundan taşındı). **2026-11-22:** S4.3 için dört sunucu dizin
  ölçütleriyle denetlendi, düzeltmeler yayında (`yayin-20261122-173908`), e-posta mcp-review@anthropic.com'a gitti
  (taslak `docs/s4-dizin-basvurulari.md` §2e). OpenAI için yayıncı satırı doğrulanmış kişisel ada çevrildi ("Fatih
  Ebrar İnan"; gizlilik, şartlar, paket; S4.6'daki "kişisel ad hiçbir yerde" kararı bu kadarıyla değişti; dernek yolu
  bırakıldı: OpenAI'nin işletme doğrulaması Türkiye belgelerinde belirsiz). **Dizin adları İngilizce** (kullanıcının
  kararı): "Risale-i Nur Library", "Hadith Library", "Tafsir Library", "Classical Islamic Library"; yayıncı "Risale
  MCP"; dört sunucunun başlığı yayında (`yayin-20261122-232806`). OpenAI organizasyon adı "Risale MCP", eski projenin
  anahtarları iptal; paket iç adı `risale-i-nur` (portal değiştirtmiyor), görünen ad "Risale-i Nur Library" (adda
  "MCP" olamaz), hakeme not §6. S4.7 (Claude eklentisi, plugin) açıldı. **2026-11-23:** Claude'da dört listeleme yeni
  adla incelemede; alan adı Anthropic'te DNS TXT ile kanıtlandı ("Verified" talep edilmedi: şirket içindir). OpenAI'de
  Risale yeniden gönderildi; Hadis, Tefsir, Klasik paketleri (`data/interim/chatgpt/{hadith,tafsir,classical-islamic}-library.zip`,
  §7) ve üç alt alan adının jetonu hazırlandı. Hadis sunucusunda bâb künyeleri hep boştu (Kütüb-i Sitte dizini sunucuya
  gitmemişti) ve İngilizce künye tanınmıyordu: düzeltildi (`yayin-20261123-000026`). Demo videoları
  (`~/Videolar/hadis-demo-2026-11-23_10.23.06.mp4`, `tafsir-library-demo.mp4`, `klasik-demo-2026-11-23_10.35.52.mp4`;
  Tefsir'in 3. ve 5. senaryosu yeniden çekildi: ilkinde web araması ve Klasik eklentisi devreye girmişti; Hadis'in 5.
  senaryosunda Risale eklentisi de kullanıldı, kullanıcının kararı: sorun değil); üç başvuru Risale'nin sonucu
  beklenmeden gönderildi (kullanıcının kararı; inceleme ≈1 ay). E8'in ilk adımı Sözler e-postası yerine risaleoku'ya
  soru oldu (kullanıcının kararı; gerekçe aşağıda, "E8 izin"), mesaj gitti. **S4 kapandı** (kullanıcının
  kararı, 2026-11-23): cevaplar `PLANLAR.md` › "Bekleyen"de (S4.3 Anthropic, S4.1 OpenAI, E8 risaleoku), S4.7
  "Sıradaki"nde.
- S4.7 **Claude eklentisi** (bitti, 2026-11-23; "Sıradaki"den taşındı) (plugin, kullanıcının kararı, 2026-11-22): küçük, herkese açık GitHub deposu (proje
  talimatı skill olarak, dört bağdaştırıcının adresi, README, lisans; metin girmez). Önce yerelde kurulup skill'in
  sohbette ne zaman yüklendiği denenir (her sohbette değil, açıklaması eşleşince yüklenir: proje talimatının birebir
  yerini tutmayabilir), sonra portaldan "Plugin bundle". S4'ün öbür adımları kapandı (2026-11-23).
  **Hazır (2026-11-23; kullanıcının kararları: tek eklenti, hazır komutlar skill olur, skill'ler İngilizce):** depo
  `github.com/fatihebrarinan/risale-library-plugin` (herkese açık, MIT; ad `risale-library`, görünen ad "Risale-i Nur
  Library", yazar "Risale MCP"), kaynakları `packaging/claude-plugin/`, üretici `scripts/claude-plugin.py`; ana skill
  `site/en/instructions.md`'den üretilir. Sekiz skill: `risale-library` (ana kurallar), `verse-study`, `hadith-check`
  (eklentiler arası akışlar), hazır komutlardan `topic-survey`, `text-and-commentary`, `study-circle`, `self-test`,
  `lesson-plan`. Claude Code'da 12 soruluk deneme (`tests/golden/claude_plugin_prompts.json`; rapor
  `data/interim/claude-plugin/dene-20261123-16*.md`): 11'inde beklenen skill yüklendi, denetim sorusunda hiçbiri; tek
  tefsir sorusunda yüklenmedi ama cevap doğru; üç eklentili cevapta tek Kaynaklar listesi. claude.ai'de
  kullanıcı denedi: hesapta kurulu bağdaştırıcıları kendiliğinden gördü, skill doğru yüklendi (orada yalnız skill ve
  bağdaştırıcı çalışır; komut, hook, alt ajan yok). **Portalın denetimi** (2026-11-23) iki şey istedi, 1.0.1'de düzeldi:
  yazar adı "Risale MCP" dizindeki "riddle-mcp"ye benziyordu (NAME_CONFUSABLE), yazar ve marketplace sahibi artık
  "Nur Hadimleri" (dizin başvurularındaki yayıncı adı; eklentinin adı ve görünen adı değişmedi, o yüzden e-posta
  gerekmedi); üç skill'in açıklaması tırnaksız ": " taşıyordu (YAML okuyucusu orada durur): sekizinin açıklaması çift
  tırnaklı, `claude-plugin.py` tırnaksızı reddeder. Listeleme alanları (`documentationUrl`, `privacyPolicyUrl`,
  `supportUrl`, `termsOfServiceUrl`, `icon`) için uyarılar "no action needed". **Gönderildi** (2026-11-23, `main @
  54ebcd6`; listelendiği yerler Claude Code, Cowork, Claude uygulamaları; auto-publish açık). Veri işleme cevapları:
  kişisel veri yok; skill'ler beyan edilen bağdaştırıcılardan başka yere veri göndermez (Voyage sunucunun içinde);
  saklama "Not retained" (araç girdileri saklanmaz; 90 günlük kullanım kaydı içeriksiz işletme kaydı); 18 yaş altı için
  değil. Ardından gizlilik politikası (iki dil) bağdaştırıcıları alt alan adlarıyla yazacak biçimde düzeltildi
  (`hadis.risalemcp.com/mcp` …; önceden `/hadis` gibi eski yollar), yayında. Cevap `PLANLAR.md` › "Bekleyen"de.
- E8 izin (2026-11-23): önce risaleoku'ya soruldu, Sözler'e değil (gerekçe: izin vermiş birine, aynı sohbette; soru
  20'yi aşkın dili birden kapsar; tercümenin hakkı yayıncının ve mütercimin olduğu için rıza sorusu da mesajdaydı).
  risaleoku'nun cevabı ("RN Kütüphanesi", 12.03): "yabancı dillerde mütercimler tarafından
  izinli olarak kullanılmaktadır.. ticari bir amacınız olmadığı için bizzat izin almadan kullanabilirsiniz". İzin
  Risale'nin diğer dillerdeki tercümelerini de kapsar; şart aynı (kazanç yok, kaynak), tercümelerde mütercim ve yayınevi
  anılır. Ekran görüntüsü `data/raw/kullanici/izinler/risaleoku-cevap-diller.jpeg`; `docs/izinler.md` güncellendi
  ("Bekleyen"den çıktı). Planın (a) şıkkı: Sözler'e izin değil bilgi e-postası. Sözler'e e-posta şimdilik gitmez (kullanıcının kararı). E8 "Sıradaki" 9'a girdi (B3'ten önce; kullanıcının
  kararları: kapsam altı cilt ve Saykal'ın kalanı, Sîret-i Zâtiyye mecmua, kimlikler Osmanlıca gibi kendi yapısıyla,
  ilk adımda bölüm eşlemesi, paragraf eşlemesi denenir, varsayılan aramaya girmez, öbür diller "Sonra"da); alt
  adımlar E8.1–E8.6 `PLANLAR.md` › "Sıradaki" › E8.


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

**E5. Kalan klasik eserler ve yeni tanıtım (bitti, 2026-11-25; yayında).** "Sıradaki"deki kayıt (kararlar dahil):

- E5 **Kalan klasik eserler:** E2'den sonra, aynı ölçütle (`docs/eserler/klasik.md`). Sırada (b)'nin 2. dilimi (kullanıcı, 2026-11-13); 3. dilim ve (c) "Sonra"da. **Tanıtım** (kullanıcının kararı, 2026-11-22: eklenti zayıf kaldı, bu hafta 68 çağrı): eklenti "Risale'nin havale ettiği klasikler" diye tanıtılır (seçim Risale'deki anmalardan); sitede, sunucu talimatında ve dizin metinlerinde.
  **Ön çalışma ve kararlar (2026-11-24):** Risale'de adı geçen eserler türleriyle (`docs/e5-risalede-anilan-eserler.md`:
  102 eser, 792 cümle; havale yalnız 24 cümle). Kullanıcının kararları: (1) tanıtımın sözü **"Risale'nin havale ettiği
  ve dayandığı klasikler"**, her eserin Risale'deki yeri türüyle (havale, nakil, değerlendirme); (2) **`risale_refs`**:
  her klasik eserin kaydında Risale'nin onu andığı cümlelerin kimliği ve türü (`catalog/klasik.py`'de elle, onaylı
  liste), `build` atfı genel veritabanından alır, `list_works` döndürür (Risale'nin metni kopyalanmaz); (3)
  **Şerhu'l-Mevâkıf (c)'den 2. dilime** (nüsha: OpenITI `0756CadudDinIji.Mawaqif.JK001335`, Umeyre, Dâru'l-Cîl 1997:
  adı "el-Mevâkıf" ama Seyyid Şerîf'in şerhi, metin `# المتن #` ile ayrılıyor; 460 bin kelime); (4)
  **er-Risâletü'l-Hamîdiyye** (Hüseyin el-Cisr) (c)'ye: OpenITI'de yok, izinli nüsha aranır.
  **Bu turun eserleri (kullanıcının kararı, 2026-11-24):** Şerhu'l-Mevâkıf, Şerhu'l-Makāsıd, et-Telvîh (tamamı;
  `risale_refs` Mukaddemât-ı İsnâ Aşer'i gösterir), el-Fıkhu'l-Ekber, el-Munkız (tanıtımda "Risale'de adıyla anılmaz"),
  el-Mevâhibü'l-Ledünniyye (3. dilimden alındı: havale edilen eser); ≈1,44 milyon kelime. İhyâ son alt adım.
  - E5.1 İndirme (`fetch klasik`) ve ham verinin incelemesi: başlık yapısı, katmanlar (Îcî'nin metni ve Cürcânî'nin
    şerhi `# المتن #` ile; Telvîh'te Tavzîh'in metni), sayfa ve dipnotlar; örnekler kullanıcıya.
  - E5.2 Ayrıştırma (`books/klasik_openiti.py`), testler; `risale_refs` listesi (rapordan, kullanıcı onaylar) ve
    `list_works`'te gösterimi.
  - E5.3 Profil, vektörler, talimat (`KLASIK_INSTRUCTIONS`: kelâm, tasavvuf ve siyer de), tanıtım (site, dizin
    metinleri, eklenti skill'i), çağrı seti, yayın; Yenilikler taslağı.
  - E5.4 İhyâu Ulûmi'd-Dîn: ayrı kurulum, anlamsal aramaya etkisi ölçülür.
  **Önceden verilen kararlar (kullanıcı, 2026-11-24):** (1) şerhin içindeki metin (Îcî'nin Mevâkıf'ı, Sadrüşşerîa'nın
  Tavzîh'i) aynı eserde işaretli katmandır, eser şârihindir, ayrı eser çıkarılmaz; (2) `risale_refs` yalnız müellifin
  sözündeki havale, nakil ve değerlendirmeyi kapsar (tefe'ül, yalnız anma, talebe sözü girmez; kopyalar asıl yere
  indirgenir), 1. dilim eserleri dahil; liste rapordan çıkarılıp okunur, kullanıcı bakar, sonra kataloğa girer;
  (3) nüsha kötü çıkarsa OpenITI'deki başka sürüme geçilir, sebebi örnekle bildirilir; (4) dizin metinleri (Anthropic,
  OpenAI) başvurular sonuçlanınca değişir, taslağı hazır bekler; site, talimat ve eklenti skill'i E5.3'te; (5) uçtan
  uca deneme temiz ve araç çıktısı farkı yalnız beklenen farksa yayın sorulmadan yapılır, sorun çıkarsa durulur;
  (6) İhyâ anlamsal aramada öbürlerinin önüne geçerse (ölçüm) varsayılan aramadan çıkar, eser verilince aranır;
  (7) İhyâ'da Irâkî'nin tahrici varsa ayrı katman; Risale'nin İhyâ künyeli hadisleri İhyâ'daki yerine mekanik lafız
  bağıyla bağlanır.

Yapılanlar (2026-11-24 gece – 2026-11-25; kullanıcı bu seferlik E5.1'in örneklerini göstermeden sürmeye izin verdi):
- **Ön çalışma:** `docs/e5-risalede-anilan-eserler.md`: Risale'de adı geçen 102 eser, 792 cümle; havale yalnız 24
  cümle (14 eser). Yan bulgu B10 (Arapça Mesnevî'nin muhakkik eki).
- **E5.1 nüshalar** (ham verinin incelemesinden): Şerhu'l-Mevâkıf OpenITI'de Îcî'nin adı altında "المواقف"
  (Umeyre, Dâru'l-Cîl 1997; içi Seyyid Şerîf'in şerhi): ShamAY0033881 (başlıklı) alındı, JK001335 aynı baskı,
  başlıksız. Şerhu'l-Makāsıd JK001157 (başlık satırı yok; ShamAY da öyle). Telvîh: JK007110 yalnız Teftâzânî'nin
  şerhi, başlıksız; ShamAY0034200 aynı baskıda Tavzîh'le sayfa sayfa iç içe: metin JK'dan, başlıklar ShamAY'den
  eşleştirmeyle. Munkız ShamAY0033739 (Câbir; JK 23 uzun paragraf). Fıkh-ı Ekber Shamela0006388. Mevâhib
  Shamela0023685. İhyâ JK000001 (Irâkî'nin tahrici metnin içinde "+ حديث … +"), başlıklar Shamela0009472'den.
- **E5.2 ayrıştırma** (`books/klasik_serh.py`): seri kuralıyla başlık ağacı (sıra sayılı başlık ancak serisinin
  sıradaki numarasıysa bölüm açar; içindekiler satırları ve tekrarlar metin kalır; Mevâkıf'ta 396 başlıktan 19'u
  reddedildi, bir başlık tür kelimesiyle düzeltildi). Mevâkıf'ta baskının "المتن"/"الشرح" satırları alt bölüm,
  metin bölümü katman (`authority: metin`, Îcî; 146). Makāsıd'da bölümler "قال المبحث …" aktarmalarından, sabit
  seviyeyle (مقصد > فصل > مبحث). Telvîh ve İhyâ'da paragraf başlıklı sürümde ilk kelimeleriyle bulunur (Telvîh 6
  kelime, yayımlanan kimlikler bununla; İhyâ 8 kelime, pencereli: sık kalıplar imleci kaydırıyordu). İhyâ'da 4.486
  tahric ve Irâkî'nin mukaddimesi (hutbenin ortasında) Irâkî'nin şerhi (`commentator`), Gazâlî'nin metninde "+"
  kalmadı; açık kalan tahric sonraki paragrafa yalnız oradaki ilk "+" kapanışsa sürer. Muhakkikin «1» işaretleri
  (Mevâhib) ayrıldı. Sınırlama: Makāsıd ve Telvîh noktalamasız (cümle ortalama ≈250 ve ≈110 kelime; B3 gibi).
- **`risale_refs`** (`catalog/klasik.RISALE_REFS`, `RISALE_UNNAMED`): 24 kayıt, müellifin sözündeki havale, nakil,
  değerlendirme; kopyalar asıl yere; Telvîh'te Mukaddemât'ın yeri `section_here`. `build_db` klasik profilde
  `work_refs` (atıf genel veritabanından), `list_works` döndürür. İhyâ künyeli hadisler: `risale_quotes` (her
  kurulumda hesaplanır, Osmanlıca ciltler hariç; 13 hadis, 45 yer), İhyâ cümlesinde `in_risale`.
- **E5.3 sunum:** `KLASIK_INSTRUCTIONS` (kelâm, usûl, tasavvuf, siyer; katmanlar; `risale_refs` türleri;
  `in_risale`), klasik `list_works` açıklaması (`KLASIK_DOCS`), site (`klasik.html`, `en/classical.html`, ana sayfa
  kartı), eklenti 1.0.2 (yandaki depoda commit, push kullanıcıda), çağrı seti, Yenilikler taslağı
  `docs/yenilikler/2026-11-25-klasik-eserler-2.md`, dizin metni taslağı `docs/e5-dizin-metni-taslagi.md`.
- **Vektörler:** 57.510 cümle, Voyage ≈4,8 milyon token (2,91 + 1,91). İhyâ'nın anlamsal aramaya etkisi (12 soru):
  ilk 10'un %23'ü, tasavvuf sorusunda 10/10, öbür alanlarda 0–6/10, öbür eserleri dışarı itmiyor: varsayılan aramada
  kaldı (karar 6).
- **Uçtan uca deneme** (claude -p, yalnız klasik sunucu, üç soru): `risale_refs`'i türüyle kullanıyor, Risale'yi
  okumadığını söylüyor; Îcî'nin metni ile şerhi ayrı alıntılıyor; Telvîh'te "dört mukaddime" ile Risale'nin "isnâ
  aşer"ini tespit edemediğini açıkça söylüyor; İhyâ'da tahrici Irâkî'ye veriyor.
- **Yayın:** `PROFIL=klasik scripts/tefsir-sunucu.sh gonder` iki kez (kayıtlar `klasik-yayin-20261125-005834`,
  `klasik-yayin-20261125-012923`; beklenen farklar talimat, eser listesi, arama sırası, yeni çağrılar, âyet alıntı
  sayısı), tefsir sunucusunun çıktısı değişmedi; site `scripts/deploy.sh --site`. Klasik veritabanı 177 MB.

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
