# S14.2: Envanter — "Risale-i Nur" nerede geçiyor, ne olmalı

Hazırlanış: 2026-11-28, Claude. Kararlar `docs/s14-acilis-plani.md` › Kararlar (K1–K5). Bu belge yayına dokunmaz.

**Nasıl işaretlenir:** her satırın "Öneri" sütunu Claude'un önerisidir. Kullanıcı son sütuna ✓ (öneri uygun), ✗
(kalsın / olmasın) ya da kısa bir not yazar. **Öneriler:** *kalır* (dokunulmaz), *genelleşir* (K1–K3'e göre yeniden
yazılır), *karar* (kullanıcının ayrıca karar vermesi gereken). **Adım:** değişikliğin yapılacağı adım (S14.4 davranış,
S14.5 metin, S13.22 eklentilerin göçü).

Dışarıda tutulanlar (kalır, listelenmedi): Yenilikler ve Çalışmalar yazıları (tarihli kayıt, o günün sözüdür);
kaynak adları ("e-Risale", "Kaynak: e-Risale" satırları, izinlerin şartı); atıf yolları ve örnek cevapların metni
(sistemin gerçek cevabıdır, düzeltilmez); kod içi açıklamalar ve iç proje adı "Risale MCP" (K4).

## 1. Çatı sitesi (`ayinedar.org`, `site-ayinedar/`; tr ve en)

| # | Yer | Bugün | Öneri | Adım | İşaret |
|---|---|---|---|---|---|
| 1.1 | Başlık, Open Graph başlığı (`index.html`, en) | "Âyinedâr: Risale-i Nur, Tefsir, Hadis ve Klasik Eserler için Yapay Zekâ" | genelleşir: K1'in tarifiyle | S14.5 | |
| 1.2 | Açıklama (meta, og, JSON-LD `description`) | "Bediüzzaman Said Nursî'nin eserlerine, klasik tefsirlere, hadis kitaplarına ve klasik İslâm eserlerine dayanan…" | genelleşir: önce Kur'ân ve Sünnet, kütüphaneler K1 sırasıyla | S14.5 | |
| 1.3 | Paylaşım resminin açıklaması (`og:image:alt`; `site-uret.py`) | "Risale-i Nur, tefsir, hadis ve klasik eserlerden…" | genelleşir | S14.5 | |
| 1.4 | Paylaşım kartı (`scripts/paylasim-cati.html` → `img/paylasim.png`) | alt yazı "Risale-i Nur · Tefsir · Hadis · Klasik eserler" | genelleşir (ör. "Kur'ân · Hadis · Tefsir · Risale-i Nur · Klasik eserler") | S14.5 | |
| 1.5 | Ana sayfanın başlığı ve giriş paragrafı | "Risale-i Nur'a, tefsirlere… sorun"; "sorularınızı Bediüzzaman Said Nursî'nin eserlerinden cevaplayan… İsterseniz… açarsınız" | genelleşir: K1 tarifi, ikinci yarısı usul (her söz kaynağıyla) | S14.5 | |
| 1.6 | Sayılar şeridi | "53 eser Risale-i Nur…", "12 eser Risale-i Nur'un dayandığı klasikler" | sıra K1'e göre (Kur'ân, hadis, tefsir, Risale, klasik); klasikler "İslâm ilimlerinin klasikleri" (K3) | S14.5 | |
| 1.7 | "Nasıl çalışır" | "…bir âyeti Risale-i Nur ve tefsirlerle birlikte çalışmak için ayrı kipleri vardır" | genelleşir (modlar S14.4'ün seçimine göre) | S14.5 | |
| 1.8 | "Bir soru, bir cevap" örneği | yalnız Risale sorusu ("Hastalığa nasıl sabredilir? Risale-i Nur'dan…") | K3: iki örnek, biri genel (âyet, hadis ve açıklayanlarla), biri bu Risale örneği; genel örnek sistemin gerçek cevabı (S14.4'ten sonra alınır) | S14.5 | |
| 1.9 | Sohbet kartı | "Risale-i Nur her zaman açıktır; tefsir, hadis ve klasik eserler kütüphanelerini siz açarsınız" | genelleşir: S14.4'ün seçimine göre; "Risale-i Nur'dan cevapla" seçeneği anılır | S14.5 | |
| 1.10 | Eklentiler kartı | "dört eklentiyle…: Risale-i Nur, Hadis, Tefsir ve Klasik Eserler" | kalır (eklenti adları); sıra K1'e göre olabilir | S14.5 | |
| 1.11 | Risale okuyanlara bölüm | yok | K3: yeni kısa bölüm ("Risale-i Nur okuyorsanız…", seçenek ve külliyatın özelliği) | S14.5 | |
| 1.12 | "Kaynaklar ve teşekkür" | "Risale-i Nur için e-Risale ve risaleoku.com; hadis… OpenITI; Kur'ân… Tanzil" | kalır; sıra K1'e göre (Kur'ân önce) | S14.5 | |
| 1.13 | "Son yenilikler" şeridi | 25 Kasım duyurusu: "Risale-i Nur'un havale ettiği kitaplar geldi" | kalır (tarihli yazı); S14.6'nın duyurusu gelince yerini alır | — | |
| 1.14 | Alt bilgi (bütün sayfalar; `site-uret.py` `FOOTER_CATI`) | "…cemaatin resmî hizmeti değildir. Yayıncısı Nur Hadimleri." | K4: "Yayıncısı Nur Hadimleri" çıkar; bağımsızlık cümlesi kalır | S14.5 | |
| 1.15 | JSON-LD kurum adı (`index.html`) | "Nur Hadimleri" | K4: "Âyinedâr" | S14.5 | |
| 1.16 | Belgeler (`belgeler.html`) | "Âyinedâr, Bediüzzaman Said Nursî'nin eserlerini, Kur'ân-ı Kerîm'i, … ve Risale-i Nur'un dayandığı klasik eserleri … sunan…; Yayıncısı Nur Hadimleri" | genelleşir (K1 sırası, K3), yayıncı adı çıkar (K4); kaynak listesi (e-Risale, risaleoku…) kalır | S14.5 | |
| 1.17 | Kullanım şartları (`kullanim-sartlari.html`, en `terms.html`) | aynı tarif ve "yayıncısı Nur Hadimleri" | genelleşir, yayıncı adı çıkar; şartların özü değişmez | S14.5 | |
| 1.18 | Gizlilik (`gizlilik.html`, en `privacy.html`) | "yayıncısı Nur Hadimleri, sorumlusu Fatih Ebrar İnan"; eklentiler satırı | yayıncı adı çıkar, **sorumlu kişi kalır** (gizlilik politikasının şartı); toplanan veri değişmediği için öz değişmez | S14.5 | |
| 1.19 | 404 sayfası | alt bilgi | 1.14 ile | S14.5 | |
| 1.20 | İngilizce ana sayfa (`en/index.html`) | 1.1–1.12'nin İngilizcesi; "Published by Nur Hadimleri" | Türkçesiyle birlikte genelleşir | S14.5 | |

## 2. Sohbet (`chat.ayinedar.org`)

### 2a. Görünen metinler

| # | Yer | Bugün | Öneri | Adım | İşaret |
|---|---|---|---|---|---|
| 2.1 | Girişsiz açılış (`sohbet_hesap.HERO`): başlık | "Risale-i Nur'a sorun, cevabı kaynağıyla okuyun." | genelleşir: K1 tarifi (eski S13.23.5, giriş sayfası) | S14.5 | |
| 2.2 | HERO: tanıtım paragrafı | "Sorularınızı Bediüzzaman Said Nursî'nin eserlerinden, isterseniz klasik tefsirlerden…" | genelleşir | S14.5 | |
| 2.3 | HERO: üç özellik | "Her alıntı kaynağıyla"; "Bütün külliyat, isterseniz daha fazlası (Sözler'den Lâhikalara…)"; "Bugünün diliyle sorun" | 1. ve 3. kalır; 2. genelleşir (kütüphaneler K1 sırasıyla; Risale K3'le anılır) | S14.5 | |
| 2.4 | HERO: örnek | "Ümitsizliğe düşen birine ne söylenir?" + Risale alıntısı | karar: kalır mı, genel bir örnekle mi değişir, ikisi mi (dar ekranda yer az) | S14.5 | |
| 2.5 | Arama motoru başlığı ve açıklaması (`SEO_TITLE`, `DESCRIPTION`), JSON-LD | "…Sohbet: Risale-i Nur, Tefsir, Hadis ve Klasik Eserler için Yapay Zekâ"; yayıncı "Nur Hadimleri" | genelleşir; yayıncı K4 | S14.5 | |
| 2.6 | PWA manifestosu açıklaması | "Sorularınızı Bediüzzaman Said Nursî'nin eserlerinden, kaynağıyla cevaplayan yapay zekâ." | genelleşir | S14.5 | |
| 2.7 | Paylaşım kartı (`scripts/paylasim-sohbet.html` → `paylasim.jpg`) | "İslâmî kaynaklar üzerine sorun; cevap kaynakların kendi sözleriyle ve yerleriyle gelsin." | zaten geneldir; K1'in tarifine yaklaştırılabilir ("Kur'ân ve Sünnet etrafında…") | S14.5 | |
| 2.8 | Kütüphane seçicisi (`sohbet.js` 62–79, `sohbet.html` 153) | "Risale-i Nur: … her soruda açık"; "Cevaplar her zaman Risale-i Nur'a dayanır. İsterseniz öbür kütüphaneleri de açın"; soru kutusunun yanında "Risale-i Nur + Tefsir" | **S14.4'ün seçimine bağlı** (A hepsi açık / B model seçer / C okuyucu); "Risale-i Nur'dan cevapla" seçeneği buraya ya da modlara (K2) | S14.4 | |
| 2.9 | Mod açıklamaları (`kipler.py`) | Serbest soru: "Risale-i Nur'a dair bir soru yazın"; Âyet çalışması: "…Risale'de ve tefsirlerde birlikte bakalım" | Serbest soru genelleşir ("Bir soru yazın"); Âyet çalışması kalır (Risale ve tefsirler doğru tarif); "Risale-i Nur'dan cevapla" yeni mod olabilir (K2) | S14.4–S14.5 | |
| 2.10 | Konu taraması modu (`dosya.py`: "Şimdilik yalnız Risale") | konu taraması yalnız Risale'de | **karar:** "Risale-i Nur'da konu taraması" diye açıkça Risale'ye ait kalır mı, yoksa öbür kütüphanelere de genişler mi (genişlemek ayrı bir iş, dizin ve ölçüm ister) | S14.4 | |
| 2.11 | Örnek soru kartları (`sohbet.js` 535–547, 6 türde ≈30 soru) | çoğu Risale sorusu ("Risale-i Nur'da şefkat…", "Hayatı anlamsız bulan birine Risale ne söyler?", "Hastalar Risalesi…") | genelleşir: türler korunur, sorular karışır (genel ve Risale), hadis ve âyet örnekleri öbür kütüphanelerle | S14.5 | |
| 2.12 | Karşılama sözleri (`GREETINGS`) | "Ne sormak istersiniz?", "Bugün hangi meseleye bakalım?"… | kalır (zaten nötr) | — | |
| 2.13 | Rehber metni (`TOUR`, `sohbet.js` 1338, 1348) | "Cevaplar Risale-i Nur'dan alıntılarla gelir"; "Cevaplar her zaman Risale-i Nur'a dayanır…" | genelleşir (S14.4'ün seçimine göre) | S14.5 | |
| 2.14 | Örnek konuşma (`ornek-konusma.json`) | "İmanımı nasıl arttırabilirim? Risale-i Nur'dan cevapla." (kullanıcının seçimi) | karar: kalır (Risale seçeneğini de gösterir) ya da genel bir örnekle değişir; yeni örnek yine sistemin gerçek cevabı | S14.5 | |
| 2.15 | Alt satır | "Tefsir ve fetva değildir, müellife mal edilmez." | kalır; "müellif" genelde de doğru (her eserin müellifi) | — | |
| 2.16 | Hakkında (`hakkinda.html`) | "Kur'ân-ı Kerîm, Bediüzzaman Said Nursî'nin eserleri, klasik tefsirler…" | sıra K1'e göre, Risale K3'le; nasıl çalışır ve sınırlar kalır | S14.5 | |
| 2.17 | Sohbetin gizlilik ve şartları (`gizlilik.html`, `sartlar.html`, en) | "sorularınızı Bediüzzaman Said Nursî'nin eserlerinden cevaplayan…"; "Risale MCP eklentileri…" | tarif genelleşir; "Risale MCP eklentileri" adı S13.22'ye kadar kalır (eklentilerin adı o); toplanan veri değişmezse öz değişmez, `POLICY_DATE` yenilenir | S14.5 | |
| 2.18 | Hizmetin adı ayarı (`sohbet_hesap.Config.name` varsayılanı) | "Risale MCP" (yayında `SOHBET_NAME` "Âyinedâr") | kalır (yalnız yerel geliştirme varsayılanı) | — | |

### 2b. Modelin talimatı (okuyucu görmez; davranışı belirler)

| # | Yer | Bugün | Öneri | Adım | İşaret |
|---|---|---|---|---|---|
| 2.19 | Giriş (`sohbet.py` 99–105) | "You answer readers' questions on the Risale-i Nur chat page…"; "You read the works of Bediüzzaman…" | K1–K2'ye göre yeniden: Kur'ân ve Sünnet merkezli sayfa, kütüphaneler | S14.4 | |
| 2.20 | Okuyucular (`SHAPE`) | "people who read the Risale-i Nur, some for years…" | genelleşir: Risale okuyanlar ve okumayanlar | S14.4 | |
| 2.21 | Kapsam (`SHAPE`) | "…say briefly that this page answers only from the Risale-i Nur" | genelleşir: "only from these libraries"; fıkıh sınırı K5'le (E10 gelince sıkılaşır) | S14.4 | |
| 2.22 | Öbür kütüphanelerin talimatı (`kutuphaneler.py` 53, 384–395) | "beside the Risale-i Nur"; "Keep the Risale-i Nur first and apart" | K2: önce Kur'ân ve Sünnet, sonra açıklayanlar; Risale sorusunda ve "Risale-i Nur'dan cevapla" seçeneğinde Risale önce; "apart" (her kütüphanenin sözü ayrı, birbirine mal edilmez) kalır | S14.4 | |
| 2.23 | Klasik kütüphanenin tarifi (`kutuphaneler.py` 73, 97) | "the classical works the Risale-i Nur refers its reader to and relies on"; seçicide "Risale'nin havale ettiği klasikler" | genelleşir: "İslâm ilimlerinin klasikleri"; Risale'deki anmalar (`risale_refs`) özellik olarak kalır | S14.4–S14.5 | |
| 2.24 | Ortak bloklar (`server.py`: `FIND`, `GROUNDED`, `risale_layers`…) | Risale talimatının kuralları | **kalır** (MCP talimatıyla bayt bayt aynı olmalı); Risale'ye özgü bloklar yalnız Risale araçları için | — | |

## 3. Okuma platformu (`read.ayinedar.org`, `scripts/oku-app.html`)

| # | Yer | Bugün | Öneri | Adım | İşaret |
|---|---|---|---|---|---|
| 3.1 | Karşılama ve giriş sayfası | "kaynaklara (Risale-i Nur, klasik tefsirler, belâgat eserleri, hadis kitapları) bağlı kalarak yazıldılar" | kalır: platform Kur'ân taslaklarıdır, Risale orada gerçekten kaynaklardan biri ve İşârât'ın usulü eksendir | — | |
| 3.2 | "Risale-i Nur'da genişi", "Âyetin Risale-i Nur'daki yerleri", Abdülmecid Nursî tercümesi | kaynak ve bağ etiketleri | kalır (verinin adı) | — | |

## 4. Eklentilerin sitesi (`risalemcp.com`, `site/`) ve dizinler

| # | Yer | Bugün | Öneri | Adım | İşaret |
|---|---|---|---|---|---|
| 4.1 | Sitenin adı ve marka çubuğu (`site-uret.py`: "Risale-i Nur MCP", `FOOTER` "Risale MCP: gönüllü…") | eklentilerin tanıtımı | S13.22'de `connect.ayinedar.org`'a göçerken genelleşir; o zamana kadar kalır | S13.22 | |
| 4.2 | Paylaşım resmi (`site-uret.py` 780–781: "Risale-i Nur MCP", "Risale-i Nur · Hadis · Tefsir") | eski kart (Klasik eserler de yok) | S13.22 ile | S13.22 | |
| 4.3 | Dizinlerdeki yayıncı adı ("Nur Hadimleri") ve Claude eklentisinin genel adı ("Risale-i Nur Library"), eklentinin açıklamaları ("the Risale MCP libraries") | başvurular incelemede | K4: başvurular sonuçlanınca "Âyinedâr" | S13.22 | |
| 4.4 | Eklentilerin talimatları (`server.py`) ve araç açıklamaları | her eklenti kendi kütüphanesini anlatır | kalır: Risale eklentisi Risale'nindir; öbür eklentiler zaten kendi alanlarını anlatır | — | |
| 4.5 | MCP adresleri, `risalemcp.com` alan adı | `mcp.`, `hadis.`, `tefsir.`, `klasik.risalemcp.com` | kalır (K4) | — | |

## Kullanıcının işaretleri (2026-11-28)

- **Öbür satırlar:** öneriler uygun.
- **2.4 ve 2.14:** genel bir örnekle değişir. Altyapı (S14.4) hazır olana kadar bugünküler kalır. Soru, Risale-i Nur'un
  da ele aldığı bir konudan seçilir: böylece cevapta âyet ve hadisin yanında Risale'den de alıntı bulunur. Örnek yine
  sistemin gerçek cevabıdır (kısaltılmaz, düzeltilmez); soruyu kullanıcı seçer.
- **2.10:** (cevap bekleniyor)

## Özet

- **S14.5'in metin işleri:** 1.1–1.12, 1.14–1.20, 2.1–2.7, 2.11, 2.13, 2.16, 2.17 (çatı ve sohbetin görünen metinleri).
- **S14.4'ün davranış işleri:** 2.8, 2.9, 2.19–2.23 (kütüphane varsayılanı, "Risale-i Nur'dan cevapla", talimat).
- **Kullanıcının ayrıca karar vereceği üç satır:** 2.4 (giriş sayfasındaki örnek), 2.10 (konu taraması yalnız Risale'de
  mi kalsın), 2.14 (örnek konuşma).
- **Kalır:** 1.13, 2.12, 2.15, 2.18, 2.24, 3.x, 4.4, 4.5; eklenti sitesi (4.1–4.3) S13.22'ye kadar.
