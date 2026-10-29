# Risale-i Nur MCP — Proje Belgesi

Bu dosya projenin kalıcı bağlamıdır. Her oturumda önce bunu oku.

## Amaç

Bediüzzaman Said Nursî'nin **bütün eserlerini** (Eski Said eserleri, Risale-i Nur ana ciltleri, Lâhikalar, Tarihçe-i Hayat, mecmualar, Hizbler) yapay zekâ modellerinin **kaynağa bağlı kalarak** kullanabileceği bir MCP sunucusu geliştirmek.

Nihai kullanım hedefleri:
1. Model bir konuda yorum yaptığında, dayandığı yeri **cümle düzeyinde** tam adresiyle göstersin.
2. Bir konunun eserlerde geçtiği yerler listelenebilsin.
3. Farklı bakış açılarıyla yapılan yorumlar da metindeki cümlelere dayansın.

İlk hedef 1. hedefin altyapısıdır. 2. ve 3. hedefler sonraki aşamalardır.

## Temel ilkeler

- **Her adres veriden gelir, asla tahmin edilmez.** Adres üretemediğimiz metin, adres uydurularak değil, açıkça "adres belirsiz" işaretiyle saklanır.
- **Atıf birimi cümledir.** Paragraflar yalnızca görüntü ve bağlam için tutulur.
  - MCP ↔ model arasında: `Sözler › Onuncu Söz › On iki Hakikat › Dokuzuncu Hakikat › 32. cümle`
  - Model ↔ kullanıcı arasında: `Sözler › Onuncu Söz › On iki Hakikat › Dokuzuncu Hakikat › "Şüphesiz ki bu haşri gösterir…"` (cümlenin ilk kelimeleri)
  - Bir temsil, misal ya da tek bir düşünce aynı bölümde birkaç cümle sürüyorsa ardışık cümleler tek atıfla verilir (en çok 8; paragraf sınırı yok, çünkü paragraflar her yerde anlama göre ayrılmamıştır): `Sözler › Birinci Söz › "Bedevî Arab çöllerinde…" ile başlayan 4 cümle`; MCP ↔ model arasında kimlik `…/c004..c007`, yol `… › 4.–7. cümle`.
- **Sayfa numarası yoktur.** Hiçbir veri dosyasında basılı sayfa bilgisi tutulmaz.
- **Metin tek yerde durur.** Mecmualar (Asâ-yı Mûsâ, Zülfikâr…) ana ciltlerdeki metne işaret eden içindekiler listeleridir; yalnızca mecmuaya özgü parçalar mecmuada saklanır.
- **Kaynak web'dir.** Ham yanıtlar bir kez indirilip diske kaydedilir; ayrıştırma her zaman diskten yapılır.

## Kapsam ve kaynaklar

Eserlerin listesi, her birinin kaynağı ve durumu tek yerde tutulur: `src/risale_mcp/catalog.py`. Her eserin hangi aşamada olduğu `ESERLER.md` kontrol listesindedir (`uv run python -m risale_mcp.checklist` ile diskten üretilir, elle düzenlenmez).

| Site | Rol | Notlar |
|---|---|---|
| **erisale.com** | Birincil kaynak (≈30 eser) | Standart baskı. Her bölüm ayrı sayfa; sayfa listesi `sitemap-tr.xml`'den. Metin sayfaya gömülü RSC verisinde yapısal ağaç olarak gelir: blok türleri (`H2`, `H3`, `Paragraph`, `CenteredParagraph`, `HeadingDescription`…), satır içi başlıklar (`Heading`), Arapça (`RTL`, türü âyet/hadis/Arapça, meali `rtl.txn`), hâşiye tam geçtiği yerde (`FootnoteRef` → `Footnote`). `blockIndex` kitap içinde süreklidir; boşluk = eksik bölüm. robots.txt yalnızca `/api/` yolunu yasaklar; biz yalnızca okuma sayfalarını indiririz. |
| risale.online | Zülfikâr, Tılsımlar, Sirâcü'n-Nûr, Gençlik ve Hanımlar Rehberi (mecmualar) | Hayrat baskısı, JSON API (`/risale-api/fihrist`, `/risale-api/paragraf`). Yapı fihristten (sayfa numaralı, iç içe); paragraf HTML'i kelime gruplarıdır, Arapça meali ve kaynağıyla (`data-mehaz-*`), hâşiye `<aside>`. |
| risaleoku.com | Hizbler, Küçük Sözler, (Fihrist Risalesi); Arapça Mesnevî'nin eski kaynağı (ham verisi karşılaştırma için duruyor) | `/oku/<kitap>` okuyucu sayfası: sayfa sayısı, kitabın başladığı sayfa (`baslangic`) ve fihrist ağacı (`#treemenu1`); `/ajax/<kitap>/<n>` sayfa metni. Renkli `font` "tefekkür" boyamasıdır, başlık değildir. Arapça Mesnevî'nin ağacı boş: başlıklar ortalı "الرسالة …" satırlarından; ilk başlıktan önceki sayfalar tahkik edenin girişidir. Hizbü'l-Kur'ân'ın fihristi güvenilmez (sûre sayfası bazen bir sayfa geri, bazı sûrelerin girdisi yok): sûreler metindeki "سُورَةُ …" başlığından açılır, adı Tanzil'in sûre adlarıyla tanınır (başka adla anılanlar `quran.OTHER_SURA_NAMES`; aynı iskelete inen adlar sırayla ayrılır), girdisi olmayan sûre "77-Mürselât" diye eklenir. Sitede Hizbü'l-Kur'ân'ın bir sayfası boştur (Lokmân'ın başı); `gaps`'te işaretli. Hizbü Envâri'l-Hakāik Cevşenü'l-Kebîr'i içerir. `Crawl-delay: 10`. |
| kastamonur.com | Makalat, Nutuk | Âsâr-ı Bedîiyye baskısından "Nutuklar ve Makaleler" tek bir WordPress yazısıdır (MediaWiki'den aktarılmış): `h1` "Nutuklar" ve ortalı "Makaleler Kısmı" iki bölüm, her `h2` ("Makale – 5") bir makale, basılı adı altındaki tamamı kalın paragraf, yayın satırları alt başlık, `h3` alt bölüm. Arapça `dir="rtl"` ve Unicode sunum biçimleriyle (NFKC ile standart harfe çevrilir). Dipnotlar `<sup class="reference">`, numaraları her bölümde baştan; "(Müellif)" ya da "[Haşiye]" müellifin hâşiyesi, diğerleri nâşir notu (`notes`). Sitede Makale – 13 yok, "Makale – 16" iki kez. Site "TELİF UYARISI" taşır: izinsiz ve kaynaksız kullanılamaz. |
| rasaelalnour.com | Aslı Arapça eserlerin Arapçası (Aşama 11): İşârâtü'l-İ'câz, el-Mesnevî el-Arabî (Badıllı'nın "el-Kâmil" baskısı; Nokta risalesi İhsan Kasım baskısından), Saykalü'l-İslâm'dan Kızıl İcaz, Ta'likat ve Hutbe-i Şamiye'nin Arapçası | İhsan Kasım es-Sâlihî'nin Arapça Külliyatı; Word dosyaları RAR5 arşivinde (`/dosyalar/<kitap>.rar`). Sistemdeki eski 7z RAR5'i sessizce boş açar: `libarchive-c` kullanılır; .doc LibreOffice (`soffice`) ile .docx'e çevrilir (`data/interim/rasaelalnour/`). Word dosyası basılı kitabın düz dökümüdür, biçim stili yoktur; ayrıntı `books/rasaelalnour.py` başında. Saykalü'l-İslâm (`saykulislam`) dosyaları aynı düz dökümdür; ayrıştırıcısı `books/saykal.py` (Hutbe: İhsan Kasım'ın Türkçeden tercümesi, aslı değil; kullanıcının isteğiyle "İhsan Kasım tercümesi" diye işaretli). Sitede yalnızca telif satırı var; kullanım kişisel. |
| Kullanıcının dosyaları (`kullanici`) | Rumuzat-ı Semaniye | İnternette serbest metni olmayan eserlerin kullanıcının verdiği PDF'leri; `data/` altına konur, `fetch get` ham arşive kopyalar (`sources/kullanici.py`). Rumuzat PDF'i LibreOffice çıktısıdır; Arapçası metin olarak bozuk okunur, glif kimliklerinden çözülür (`books/pdf_text.py`). Mektubat'ta da bulunan paragrafları oraya eşlenir (ikincil kaynak gibi). |
| Keşif Yolculukları Risale-i Nur Eğitim Programı | Ta'likat'ın Türkçesi | Ediz Sözüer'in programı; kitapları Google Drive'da Word dosyası. Ta'likat kitabı Arapçanın sayfa resimleri ve Protranslate'in tam tercümesi; yalnız Türkçe metin okunur. Telif bildirimi "asliyetini korumak ve kaynak belirtmek şartıyla" serbest kullanım tanır. |
| api.quran.com | Mushaf sayfa yazı tiplerinin (QCF v1) kelime kodları | Badıllı'nın Mesnevî baskısı âyetleri Kur'ân Kompleksi'nin sayfa yazı tipleriyle yazar ("QCF_P286": 286. sayfa; her karakter o sayfadaki bir kelimenin glifi). `/api/v4/verses/by_page/<n>?words=true&word_fields=code_v1,text_uthmani` her kelimenin kodunu, âyetini ve Osmanî metnini verir; yalnızca dosyada geçen 144 sayfa indirilir (2 sn arayla). |
| tanzil.net | Kur'ân-ı Kerîm (Aşama 9) | Arapça metin üç biçimde (Medine Mushafı hattı `uthmani`, imlâî `simple`, harekesiz `simple-clean`) ve iki Diyanet meali (`tr.diyanet`, `tr.vakfi`), XML. Metin değiştirilmeden, kaynağı (Tanzil Project) ve tanzil.net bağlantısı belirtilerek kullanılır; mealler yalnızca ticari olmayan kullanım içindir. Meal dosyalarının açıklama satırları XML'de geçersiz `--` taşır; ayrıştırmadan önce atılır. robots.txt yalnızca `/res/` yolunu yasaklar. |
| Yeni Asya | (artık kullanılmıyor) | Makalat ve Nutuk'un eski kaynağı. "Eski Saîd Dönemi Eserleri" cildinin `basic-html` katmanı; Arapça okunamadığı ("[Arapça]") için kastamonur.com'a geçildi. Ham veri ve ayrıştırıcı karşılaştırma için duruyor. |

- **Ertelendi:** Fihrist Risalesi (yalnızca Osmanlıca bulundu; 2026-10-27 aramasında Latin harfli tek baskı Yeni Asya'nın basılı "Fihrist Risalesi"ydi (2024, telifli). Kullanıcının önerisi: ana ciltlerin fihrist bölümlerini bir mecmua olarak birleştirmek).
- **Kaynağı bulunamadı:** Kızıl İcaz'ın Türkçesi (tam tercümeler basılı ve telifli; Arapçası `kizil-icaz-arabi`; kullanıcı kendi kitabından PDF yapacak). Hizb-i Nurî (Hizbü'l-Ekber-i Nurî): 2026-10-27'de nurpedia.org'da ("Risale:Hizb'ül Ekber-in Nuri", MediaWiki) 33 mertebe hâlinde harekeli Arapça ve Türkçe karşılığıyla bulundu; telif ve tercümenin kime ait olduğu belirsiz, kullanıcının kararı bekleniyor.
- **Doğrulandı:** el-Mesnevî el-Arabî (İhsan Kasım es-Sâlihî tahkiki), Hizbü Envâri'l-Hakāik (Cevşenü'l-Kebîr'i içerir).
- **Sitede eksik:** Sikke-i Tasdik-i Gaybî'de aynı başlıklı iki bölüm aynı adresi paylaştığından 15 blok indirilemiyor; `gaps` alanında işaretli. Mecmua eşlemesinde (Aşama 4) ana ciltlerden tamamlanacak.
- Bir kaynak kitabı birden çok esere bölünebilir: erisale'nin "İlk Dönem Eserleri" kitabı Divan-ı Harb-i Örfî, Münazarat, Sünuhat vb. eserlere ayrılır. Lemeat (Sözler'in sonu) ve Hakikat Çekirdekleri (Mektubat'ın sonu) ayrı eserdir. Seçim, katalogdaki bölüm slug önekleriyle yapılır.

Kullanım kişiseldir. Uygulama olarak yayımlanırsa kaynak sitelerden izin alınacak. Ham ve ara veri git'e eklenmez.

## Derlemler (plan, henüz uygulanmadı)

Aynı altyapı üç ayrı metin derlemine hizmet edecek. Kod tek olur, veri ve sunucular ayrılır:

| Derlem | Metin | Kullanım |
|---|---|---|
| `kisisel` | Bugünkü veri: bütün kaynakların en kapsamlı birleşimi | Yalnızca kullanıcının kendi çalışması; hiçbir ortak sunucuya çıkmaz |
| `erisale` | Yalnızca e-Risale metni (sonra e-Risale'nin resmi verisi) | e-Risale ile iş birliği (kullanıcı e-Risale ekibinde) |
| `yeniasya` | Yalnızca Yeni Asya'nın verdiği izinli PDF'ler; mevcut verinin hiçbiri kullanılmaz | Yeni Asya ile ortak proje; PDF için ayrı ayrıştırıcı |

- Her derlemin kendi katalogu, `data/<derlem>/` klasörü (ham veri, kitap JSON'ları, veritabanı, vektörler), kimlikleri ve altın soruları olur. Bir derlemin metni başka derleme karışmaz.
- Sunucu derlemi parametreyle seçer (`risale-mcp --corpus erisale`); her derlemin sunucu adı, talimatları ve kurulumu ayrıdır. Uzak sunucuya yalnızca o derlemin verisi çıkar.
- Ortak olan: ayrıştırıcılar, cümle bölücü, eşleme, arama, atıf denetimi, kontrol arayüzü. Bölme kuralı değişikliği bütün derlemlerin numaralarını etkileyebileceği için altın örnek testleri her derlem için ayrı çalışır.
- Kur'ân katmanının Arapça metni Tanzil şartıyla her derlemde kullanılabilir; Diyanet mealleri yalnızca ticari olmayan kullanım içindir, ortak derlemlere girerse Diyanet'ten izin gerekir.
- Kod ve mantık kullanıcıda kalır; ortaklara hizmet olarak sunulur. Bu, ortaklarla yazılı olarak (mülkiyet, münhasır olmama) netleştirilecek. Yeni Asya PDF'lerinin `kisisel` derleme girmesi onların iznine bağlıdır; varsayılan olarak girmez.
- Bugünkü `data/` ileride `kisisel` derlemi olur. Ayrım, ortakların verisi gelince yapılır.

## Teknik tercihler

- Dil: Python 3.11+
- Ortam ve bağımlılıklar: `uv`
- HTTP: standart kütüphane (`urllib`), `sources/http.py` içindeki nazik istemci (istekler arası bekleme, yeniden deneme). Varsayılan bekleme 5 sn; risaleoku için 10 sn.
- Veritabanı: SQLite + FTS5 (kelime araması). Anlamsal arama: Voyage `voyage-context-4` vektörleri ayrı dosyada, benzerlik numpy ile (bkz. Anlamsal arama).
- API anahtarları proje klasöründeki `.env` dosyasında (`VOYAGE_API_KEY`, `OPENAI_API_KEY`; git'e eklenmez, `env.py` okur). Her şey ileride bir internet sunucusuna taşınacakmış gibi tasarlanır: sunucuda yalnızca numpy, sağlayıcı SDK'sı yok.
- MCP: resmi Python SDK'sı (`mcp` paketi, FastMCP). Not: `@modelcontextprotocol/sdk` TypeScript paketidir, kullanmıyoruz.
- Test: `pytest` + MCP Inspector + Claude Code'a `claude mcp add` ile bağlayarak elle deneme.
- Platform: Linux Mint.
- PDF: Aşama 2'deki PDF kodu karşılaştırmadan sonra kaldırıldı (`da37ba2`). PyMuPDF kullanıcının PDF'leri (Rumuzat) için yeniden bağımlılıktır; yalnızca ayrıştırmada kullanılır.

## Klasör yapısı

```
risale-mcp/
├── CLAUDE.md
├── docs/claude-proje-talimati.md   # claude.ai Projesi talimatı (bağlayıcıyla atıflı cevap için; kullanıcı yapıştırır)
├── docs/risale-mcp.service        # sunucuyu kullanıcının bilgisayarında çalıştıran systemd kullanıcı servisi (artık yedek)
├── docs/risale-mcp.server.service # uzak sunucudaki systemd servisi (kopyası; asıl /etc/systemd/system'de)
├── scripts/deploy.sh              # kodu ve hazır veriyi uzak sunucuya gönderir (auth.db'ye dokunmaz)
├── scripts/sunucu.sh              # uzak sunucuyu yönetir: hesaplar, kayıt, servis, günlük
├── scripts/gecis.sh               # tek seferlik: Funnel'dan risalemcp.com'a geçiş (Caddy, güvenlik duvarı, servis)
├── docs/Caddyfile                 # uzak sunucudaki Caddy yapılandırması (kopyası)
├── site/                          # risalemcp.com: ana sayfa, belgeler.html, gizlilik.html, en/ (docs, privacy); deploy.sh gönderir
├── docs/kaynak-bilgilendirme-epostasi.md  # kaynak sitelere bilgilendirme e-postası: liste ve taslaklar (Aşama 12)
├── docs/dizin-basvurusu.md       # Anthropic bağlayıcı dizini başvurusu: portalın adımlarıyla metinler (hakem hesabı `admin`)
├── data/
│   ├── vectors/                   # Anlamsal arama vektörleri <model>.<seçenek>.npy + .keys.json (git'e eklenmez)
│   ├── raw/                       # Ham kaynak yanıtları (git'e eklenmez)
│   │   ├── erisale/               # sitemap-tr.xml, <kitap>/manifest.json, pages/<bölüm>.html.gz
│   │   ├── risale_online/         # eserler.json, <kitap>/fihrist.json, paragraf/<ilk>-<son>.json
│   │   ├── risaleoku/             # <kitap>/index.html.gz, pages/<n>.html.gz
│   │   ├── yeniasya/              # <kitap>/toc.html.gz, pages/<n>.html.gz (artık kullanılmıyor)
│   │   ├── kastamonur/            # <yazı>/manifest.json, page.html.gz
│   │   ├── tanzil/                # manifest.json, quran-<biçim>.xml, tr.diyanet.xml, tr.vakfi.xml
│   │   ├── rasaelalnour/          # <kitap>/archive.rar, manifest.json (isaretulicaz, saykulislam, mesnevi)
│   │   ├── qurancom/              # pages/<sayfa>.json.gz: QCF glif kodlarının âyet ve kelimeleri
│   │   ├── kesif/talikat/         # talikat.docx, manifest.json: Ta'likat'ın Türkçe tam tercümesi (Keşif Yolculukları programı)
│   │   ├── kullanici/<kitap>/     # <kitap>.pdf, manifest.json: kullanıcının verdiği PDF (Rumuzat-ı Semaniye)
│   │   └── logs/                  # toplu indirme günlükleri
│   ├── interim/                   # Ara çıktılar
│   │   ├── erisale/<kitap>.blocks.json   # birleştirilmiş, doğrulanmış bloklar (git'e eklenmez)
│   │   ├── review/index.html      # kontrol arayüzü: bütün eserler tek sayfada; metinler review/data/<eser>.js (git'e eklenmez)
│   │   ├── outline/<eser>.txt     # elle kontrol için girintili başlık ağacı (git'e eklenmez)
│   │   ├── quran/ayah_check.md    # âyet denetimi: kaynağın numarası Kur'ân metniyle tutmayan yerler
│   │   ├── ayah_links/            # links.md (bütün âyet ilişkileri), sample-<tur>.md (gözden geçirme örneklemi)
│   │   ├── rasaelalnour/<kitap>/  # arşivden açılan Word dosyaları ve docx/ çevirileri (git'e eklenmez)
│   │   └── build.log              # son toplu ayrıştırmanın raporu
│   ├── books/<eser>.json          # Her eserin JSON'u (git'e eklenmez)
│   ├── quran.json                 # Kur'ân katmanı: metin, mealler, sûre adları (git'e eklenmez)
│   ├── risale.db                  # SQLite veritabanı (git'e eklenmez)
│   └── auth.db                    # hesaplar, OAuth istemcileri ve jetonları, kullanım kaydı (git'e eklenmez; risale.db gibi yeniden kurulmaz)
├── src/risale_mcp/
│   ├── paths.py        # Proje klasörleri
│   ├── catalog.py      # Bütün eserler, kaynakları ve durumları
│   ├── checklist.py    # ESERLER.md kontrol listesi
│   ├── fetch.py        # Aşama 1: indirme ve bütünlük doğrulama CLI'ı
│   ├── build.py        # Aşama 2: ham veri -> data/books/<eser>.json CLI'ı
│   ├── headings.py     # Başlık türü, numarası, kimlikteki yerel ad
│   ├── sentences.py    # Aşama 3: cümle bölücü, incipit, atıflar, altın örnekler
│   ├── books/
│   │   ├── model.py          # Kaynaktan bağımsız eser modeli: düğüm, paragraf, hâşiye, Arapça parça
│   │   ├── erisale.py        # erisale blokları -> eser modeli
│   │   ├── risale_online.py  # risale.online fihrist + paragraf HTML'i -> eser modeli
│   │   ├── risaleoku.py      # risaleoku sayfaları + fihrist ağacı -> eser modeli
│   │   ├── yeniasya.py       # Yeni Asya satır düzeni -> eser modeli (artık kullanılmıyor)
│   │   ├── kastamonur.py     # kastamonur.com yazısı -> Nutuk ve Makalat
│   │   ├── rasaelalnour.py   # rasaelalnour Word dosyası -> İşârâtü'l-İ'câz'ın Arapça aslı
│   │   ├── mesnevi_arabi.py  # Badıllı'nın Mesnevî Word dosyası (QCF âyetleri, Word dipnotları) -> el-Mesnevî el-Arabî
│   │   ├── saykal.py         # Saykalü'l-İslâm (Kızıl İcaz, Ta'likat, Hutbe-i Şamiye Arapçası) ve Ta'likat'ın Türkçesi
│   │   ├── pdf_text.py       # LibreOffice PDF'inden satırlar ve tablolar; Arapça glif kimliklerinden (rumuzat_glyphs.tsv)
│   │   ├── rumuzat.py        # Rumuzat-ı Semaniye PDF'i -> eser modeli
│   │   └── mecmua.py         # Mecmuaların (ve ikincil kaynaktaki eserlerin) ana ciltlere eşlenmesi
│   ├── sources/
│   │   ├── http.py           # Nazik HTTP istemcisi
│   │   ├── archive.py        # Ham yanıtı diske yazma, önbellekten okuma
│   │   ├── erisale.py        # erisale: sitemap, ham arşiv, blok çıkarma, birleştirme, doğrulama
│   │   ├── risale_online.py  # risale.online JSON API (yalnızca ham kayıt + doğrulama)
│   │   ├── risaleoku.py      # risaleoku sayfaları (yalnızca ham kayıt + doğrulama)
│   │   ├── yeniasya.py       # Yeni Asya basic-html sayfaları (artık kullanılmıyor)
│   │   ├── kastamonur.py     # kastamonur.com yazısı (yalnızca ham kayıt + doğrulama)
│   │   ├── rasaelalnour.py   # rasaelalnour RAR arşivleri (ham kayıt, doğrulama, .doc -> .docx)
│   │   ├── kesif.py          # Keşif Yolculukları programının Word dosyası (Ta'likat'ın Türkçesi; ham kayıt + doğrulama)
│   │   ├── kullanici.py      # kullanıcının PDF'leri (data/ altından ham arşive kopyalama + doğrulama)
│   │   ├── qurancom.py       # api.quran.com: QCF sayfa yazı tiplerinin kelime kodları
│   │   └── tanzil.py         # tanzil.net Kur'ân metni ve mealleri (yalnızca ham kayıt + doğrulama)
│   ├── normalize.py    # Türkçe metin normalizasyonu, sıra sayıları, slug
│   ├── review_ui.py    # Kontrol arayüzü: kitap JSON'ları → review/index.html + data/<eser>.js
│   ├── review_assets/  # Arayüzün template.html, style.css, app.js dosyaları
│   ├── db.py           # Aşama 5: veritabanı şeması ve salt okunur bağlantı
│   ├── build_db.py     # Aşama 5: JSON → SQLite CLI'ı (sûre/âyet çözümü, doğrulama)
│   ├── search.py       # Aşama 5: sorgu dili → FTS5, cümle ve başlık araması
│   ├── library.py      # Aşama 6: veritabanı üzerindeki okuma işleri (MCP'den bağımsız)
│   ├── quran.py        # Aşama 9: Kur'ân katmanı (ham -> data/quran.json), harf iskeleti, âyet eşleme
│   ├── ayah_links.py   # Aşama 10: âyet ilişkileri (kurallar, gözden geçirme raporu ve örneklem)
│   ├── citations.py    # Atıf denetimi: metindeki "Eser › Bölüm › “ilk kelimeler”" atıfları (araç ve altın sorular)
│   ├── env.py          # .env dosyasındaki API anahtarları
│   ├── embeddings.py   # Aşama 8: vektör sağlayıcıları (Voyage, OpenAI), vektör deposu, vektör çıkarma CLI'ı
│   ├── semantic.py     # Aşama 8: sunucunun anlamsal araması (en yakın cümleler, bölüm sıralaması)
│   ├── search_eval.py  # Aşama 8: arama değerlendirmesi (hit@k, MRR) ve model karşılaştırması
│   ├── server.py       # Aşama 6: MCP sunucusu (araçlar, kaynaklar, hazır komutlar)
│   ├── static/         # sunucunun ikonu (icon.svg, icon.png, favicon.ico): MCP `icons` ve /icon.png, /favicon.ico
│   ├── auth.py         # Aşama 12: OAuth sağlayıcısı, giriş sayfası, hesaplar, oturumlar, kullanım kaydı (data/auth.db)
│   └── golden.py       # Aşama 7: altın sorularla uçtan uca deneme (Claude Code istemci)
└── tests/
    ├── test_catalog.py
    ├── test_erisale.py
    ├── test_sources.py
    ├── test_normalize.py
    ├── test_headings.py
    ├── test_books.py
    ├── test_mecmua.py
    ├── test_other_sources.py
    ├── test_sentences.py
    ├── golden/sentences_sozler.json  # kilitli altın örnekler (Sözler'den seçilmiş düğümler)
    ├── test_review_ui.py
    ├── conftest.py           # ortak küçük veritabanı (iki elle yazılmış eser)
    ├── test_build_db.py
    ├── test_server.py
    ├── test_citations.py
    ├── test_embeddings.py
    ├── test_semantic.py
    ├── test_search_eval.py
    ├── test_golden.py
    ├── test_quran.py
    ├── test_ayah_links.py
    ├── test_rasaelalnour.py
    ├── test_mesnevi_arabi.py
    ├── test_saykal.py
    ├── test_rumuzat.py
    ├── test_auth.py
    └── golden/
        ├── golden_questions.md   # kullanıcının yazdığı test soruları
        ├── questions.json        # aynı sorular, doğrulanmış beklenen bölümlerle (düzenek bunu okur)
        ├── ayah_links_review.json  # kullanıcının âyet ilişkisi örneklem kararları (Aşama 10)
        └── semantic_queries.json # anlamsal arama değerlendirme seti (50 soru, kullanıcı onayladı)
```

## Veri modeli

Eserlerin iç yapısı düzensizdir: Söz, Makam, Mebhas, Mesele, Nükte, Hakikat, Esas, Lem'a, İşaret, Remiz, Hâşiye, Zeyl, Mektub, Şuâ vb. Bu yüzden **sabit sütunlar yerine esnek bir başlık yolu** kullanılır.

Her eser `data/books/<eser>.json` dosyasıdır (`uv run python -m risale_mcp.build --all`). `build` sonunda veritabanını da yeniden kurar (`--no-db` ile atlanır).

- Üst alanlar: `work`, `title`, `group`, `language` (`tr` | `ar`), `source`.
- **`outline`**: başlık ağacı, kitap sırasıyla. İlk kayıt eserin kendisidir (kök).
  - `id`, `parent_id`, `title` (basılı başlık), `ref` (`Sözler › Onuncu Söz › On iki Hakikat › Dokuzuncu Hakikat`)
  - isteğe bağlı: `subtitle`, `toc_title` (kaynağın içindekilerdeki adı, farklıysa), `type`, `number`, `heading` (`H1`…`H6` ya da `inline`), `url` (kaynaktaki bölüm sayfası; doğrulama için), `sources` (mecmuada: karşılık gelen ana cilt düğümleri)
- **`paragraphs`**: görüntü ve bağlam için, kitap sırasıyla; hâşiye bağlı olduğu kaydın hemen ardından gelir.
  - `id` (`<düğüm>/p003`), `node_id`, `kind`, `text`
  - `kind`: `paragraph`, `arabic` (tamamı Arapça), `poem` (kıta; satırlar `\n` ile), `quote`, `signature`, `table`, `hasiye`
  - `arabic`: metindeki Arapça parçalar `[{start, end, kind, meal, source}]`; `kind` âyet/hadis/arabi/farsi…, `source` âyette "Bakara Sûresi, 2:117"
  - isteğe bağlı: `center` (ortalı), `continued` (araya giren bloktan sonra süren paragraf)
  - mecmuada ana cilde eşlenmiş paragrafta `text` yoktur; `source` ana ciltteki paragraf kimlikleridir (baskılar paragrafları farklı bölebildiği için birden çok olabilir). Bu paragrafların cümlesi de ana ciltte durur.
  - hâşiyede: `parent_id` (paragraf, hâşiye ya da başlıktaysa düğüm), `offset` (işaretin metindeki konumu), `anchor` (bağlı olduğu cümle; başlıktaysa düğüm), kimlik `<paragraf>/h1`
  - başkasının şerhi (Kızıl İcaz'da Abdülmecid Nursî'nin): hâşiye gibi bağlanır, `commentator` taşır, kimlik `<paragraf>/s1`; veritabanında `paragraphs.commentator`, araçlarda `commentary_by`
- **`notes`**: kaynağın editör notları; metne girmez.
- **`gaps`**: kaynakta bulunamayan bloklar `{node_id, missing_blocks, after, note?}` (`after` yoksa düğümün başı). Metin uydurulmaz. Makalat'ta Yeni Asya baskısında olup Âsâr-ı Bedîiyye'de olmayan 5 parça da burada (`books/kastamonur.py`, `EDITION_GAPS`).
- **`sentences`**: atıf birimi, kitap sırasıyla. Alanlar:
  - `id`, ör. `sozler/10/on-iki-hakikat/hakikat-09/c032`; hâşiye cümlesi `…/c032/h1/c002`
  - `node_id`, `paragraph_id`, `n` (düğüm içindeki, hâşiyede hâşiye içindeki sıra)
  - `start`, `end`: paragraf metnindeki konum; `text` bu dilimin kendisidir (değiştirilmez)
  - `incipit` (ilk kelimeler), `hash` (metnin SHA-1 özetinin ilk 12 hanesi)
  - `ref`, ör. `Sözler › Onuncu Söz › On iki Hakikat › Dokuzuncu Hakikat › 32. cümle`

### Ayrıştırma kuralları (erisale, Aşama 2)
Ayrıntı `books/erisale.py` başındaki açıklamadadır. Özet:
- Her H1–H6 başlığı bir düğümdür; ağaç başlık seviyelerinden kurulur. Grup başlıkları ("On iki Hakikat") da düğümdür ve atıfta görünür.
- `TocOnly` başlık yalnızca içindekilerde görünür ama düğümdür. `BookOnly` başlık yeni düğüm açmaz, eşleşen düğümün basılı başlığıdır. Atıflarda basılı başlık kullanılır; içindekiler adı `toc_title`'dadır.
- Başlıktaki satır içi başlık ve başlıktan hemen sonraki `HeadingDescription` alt başlıktır.
- Paragraf başındaki biçimli numaralı etiket ("Birinci Esas:", "Birinci Kâr:") düğüm açar; etiket metinde de kalır. Yeni seri, açık seri aynı bölümde sürüyorsa onun içine, sürmüyorsa yanına yerleşir.
- Seçilen bölümlerde tek bir en üst başlık varsa o eserin kendisidir (İlk Dönem Eserleri içindeki "Münâzarât").
- Başlığın başındaki numara erisale'nin sıra numarasıdır ve atılır ("1. Zaman cemaat zamanıdır": Lâhika mektubu, numarası kimlikte). Ardından "Âyetin/Âyetlerin" geliyorsa numara başlığın kendisidir ve kalır: İşaratü'l-İ'caz'ın "6. Âyetin Tefsiri" başlıkları (önceden 15'i "Âyetin Tefsiri" diye aynı yolu paylaşıyordu).
- Kimlikler: kitap düzeyindeki ana birim yalnızca numara (`sozler/10`, `mektubat/29`), numaralı birim `hakikat-09`, numarasız tür `hatime`, diğerleri başlığın slug'ı; Lâhika mektupları erisale numarası (`emirdag-lahikasi/297`). Aynı adlı kardeşler `-2`, `-3` eki alır.

### Mecmuaların eşlenmesi (Aşama 4)
Ayrıntı `books/mecmua.py` başındaki açıklamadadır. Mecmualar ve ikincil kaynaktaki eserler (`catalog.SECONDARY_SITES`: Âsâr-ı Bedîiyye'den Makalat ve Nutuk) ana ciltlere (Eski Said eserleri ve ana ciltler, erisale/risaleoku) eşlenir:
- Metinler baskıdan bağımsız kelimelere indirilir (`normalize.match_words`: işaretler, noktalama, Arapça harf çeşitleri gider; "Risâle-i Nûr’un" = "Risale-i Nur’un"), 5 kelimelik diziler karşılaştırılır.
- En çok diziyi paylaşan ana cilt paragrafından başlanır, yakın komşular kapsamı artırdıkça eklenir. Dizilerin en az %35'i ve en az 3 dizi tutarsa eşlenir.
- Aynı metin birden çok yerdeyse önceki eşlemenin ardından gelen seçilir; kısa paragraflar ("﷽") önceki ya da sonraki eşlemenin komşusuysa bağlanır.
- Mecmua bir ana cilt paragrafını bölmüşse (Hayrat şiirin her satırını ayrı paragraf yapar) art arda gelen, ana ciltte örtüşen eşlemeler tek kayıtta birleşir; kimlikler yeniden numaralanmaz.
- Hayrat baskısının şiirlerdeki kıta numaraları ("1", "2"… tek başına paragraf) ana ciltlerde yoktur, atılır.
- Eşlenemeyen paragraflar mecmuaya özgüdür ve metinleriyle kalır (ör. Sekizinci ve On Sekizinci Lem'a'nın asıl yeri Sikke-i Tasdik-i Gaybî'dir).
- Eşleme oranları `ESERLER.md`'de. Erisale mecmualarında %66–99, Hayrat baskısındakilerde %59–82 (kalanlar çoğunlukla Hayrat'ın kendi başlık ve tanıtım satırları).

### Cümle kuralları
- Numaralar her düğümün **kendi metninde** 1'den başlar; alt düğümler kendi sayımını yapar.
- **Hâşiye cümleleri** kendi içinde numaralanır: `… › 32. cümle › Hâşiye › 2. cümle`. Bir cümlede birden çok hâşiye varsa `Hâşiye 1`, `Hâşiye 2`. Şerh ayrı sayılır: `…/c032/s1/c002`, `… › 32. cümle › Şerh › 2. cümle`.
- **Bölme:**
  - Cümle şu işaretlerden (ve ardından gelebilecek kapanış tırnağından) sonra biter: `.` `!` `?` `…` `‥`. Şart: ardından büyük harf, açılış tırnağı ya da parantezi, Arapça bir parça ya da madde numarası ("2. Yâhut") gelmeli.
  - `;` ve `:` cümleyi bitirmez ("Hiç mümkün müdür ki;", "Elcevab:").
  - Kısaltma ve baş harflerden sonra bölünmez: "Hz.", "Dr.", "No.", "M. Kemâl", "(İ.G.Z.)". Madde numarasından ("1.") sonra da bölünmez.
  - Tırnak içindeki konuşma da aynı kurala uyar; büyük harfle süren her cümlesi ayrı cümledir.
  - Şiir düz metin gibi bölünür; tablonun her satırı ve imza bir cümledir.
- **Arapça:**
  - Tamamen Arapça bir blok tek cümledir.
  - Cümle içindeki Arapça o cümlede kalır; Arapça parçanın içinde bölünmez.
  - Cümle sonundan sonra gelen Arapça ("…gördüm. اَيُحِبُّ اَحَدُكُمْ… âyeti") yeni cümle başlatır. Arapça nesirde (el-Mesnevî el-Arabî) cümle `.` `؟` `!` sonrasında Arapça harfle başlar.
- **`incipit`:** O düğüm içinde başka bir cümleyle karışmayacak kadar uzun tutulur (en az 4 kelime).
- **Cümle sonu olarak "*":** eser `stops: "*"` taşıyorsa (Badıllı'nın el-Mesnevî el-Arabî baskısı) iki yanı boşluklu "*" ardından Arapça harf gelince cümleyi bitirir; öbür eserlerde "*" cümle bitirmez.
- **Kayan numaralara karşı önlem:** Bölme kuralları değişirse numaralar kayabilir. Bu yüzden kurallar `tests/test_sentences.py` ve `tests/golden/sentences_sozler.json` ile kilitlenir; her cümlenin metin özeti (hash) ve `incipit`'i saklanır. Eski atıflar ve kontrol işaretleri `incipit`'ten yeniden bulunur. Kurallar bilerek değiştirilirse altın örnekler `uv run python -m risale_mcp.sentences --golden` ile yenilenir ve fark gözden geçirilir.

### Dikkat edilecek noktalar
- **Türkçe büyük/küçük harf:** Python'un `str.lower()` fonksiyonu `İ` ve `I` harflerini Türkçe kurallara göre çevirmez; `normalize.py` kullanılır.
- **Yazım işaretleri:** Aramada şapkalı ve uzatma işaretli harfler (â, î, û, ā, ī, ū, à) düz harfle eşleşmeli. Kesmeler (' ' ‘ ’) ve bölünmez tire (U+2011) normalleştirilmeli.
- **Orijinal metin:** `text` alanı asla değiştirilmez.
- **Hâşiyeler** ana metinden ayrılır ve geçtikleri cümleye bağlanır.
- **Arapça** korunur ve işaretlenir; erisale'nin âyet/hadis/Arapça ayrımı saklanır. Meali ve türü verilmemiş Arapça (erisale'de `rtl` bilgisi olmayan `RTL`, risale.online'da `data-mehaz-*` taşıyan her parça) da Arapça parçadır, türü `arabi`. erisale art arda iki Arapça parçayı boşluksuz verir; araya boşluk konur. Arapça harf taşımayan "Arapça" parça işaretsiz kalır.
- **Mealler nâşirindir.** Âyet ve hadis mealleri (`meal`) Bediüzzaman'ın değil, sonradan nâşirlerin eklediği tercümelerdir; baskıdan baskıya değişir (erisale ile Hayrat farklı). Araç sonuçlarında `publisher_translation` adıyla gider; model onları anlamı aktarmak için kullanır, müellife mal etmez, metin diye alıntılamaz. Müellifin kendi izahı Arapçanın hemen ardından metnin içindedir ("Yani, …") ve metin olarak atfedilir.
- **Arapça türü kaynaktan gelir.** Âyet/hadis/Arapça ayrımını biz yapmayız, kaynağın işaretidir: "Mâşâallâh" gibi kalıp ifadeler `arabi`, aynı sözler bir âyetin parçası olarak alıntılanmışsa (Kehf 18:39) `ayet`. risaleoku eserlerinde (Hizbler, el-Mesnevî el-Arabî) âyetler işaretlenmemiştir; ﴿ ﴾ içindeki Kur'ân metni `arabi` olarak durur ve Kur'ân metninde bulunarak âyete bağlanır (`ayah_quotes`, bkz. Kur'ân katmanı).
- erisale'nin Arapça metindeki köşeli numaraları ("[4]فَهَذَا…") Arapça asıl ile hâşiyedeki tercümesini eşleştirir; metinde kalır.

## Veritabanı (Aşama 5)

`uv run python -m risale_mcp.build_db` komutu `data/books/*.json` dosyalarından `data/risale.db`'yi her seferinde sıfırdan kurar (≈17 sn). Asıl kaynak JSON'lardır, veritabanı elle düzenlenmez. Kurulum geçici dosyaya yapılır, sayılar JSON'larla tutmazsa veritabanı yazılmaz. Şemanın açıklaması `db.py`'de, kurulum kuralları `build_db.py`'nin başındadır.

- **Tablolar:** `works` (katalogdaki bütün eserler; JSON'u olmayanlar `built = 0`), `nodes` (`ord`..`last_ord` alt ağaçtır), `node_sources`, `paragraphs` (eşlenmiş mecmua paragrafında `text` NULL), `paragraph_sources`, `sentences`, `arabic` (cümleye bağlı; âyette `sura`, `ayah_start`, `ayah_end`), `sura_names` (veriden öğrenilen yazılışlar ve Kur'ân katmanının 114 Türkçe adı), `notes`, `gaps`, `meta`; Kur'ân katmanı `quran_suras`, `quran_ayahs`, `quran_translators`, `quran_translations`, `ayah_quotes`; âyet ilişkileri `ayah_links`. Arama dizinleri `sentences_fts` ve `nodes_fts` (başlık, alt başlık, içindekiler adı).
- **Kimlikler:** `id` JSON'daki kalıcı kimliktir; `seq` yalnızca bu veritabanında geçerli tamsayı anahtardır ve okuma sırasını verir.
- **Normalizasyon:** Dizin ve sorgu `normalize.search_words` biçimindedir. Şapka, çengel (ş/s, ç/c, ğ/g, ö/o, ü/u), Arapça hareke, kesme ve tatvil yok sayılır; ayrıca **ı = i** sayılır (klavyesiz "isik" → "ışık"). Biçim değişirse `db.NORMALIZATION` artırılır.
- **Sorgu dili** (`search.py`): kelimeler (hepsi geçmeli), `"tam ifade"`, `haşr*` (kelime başı), `OR`, `-kelime` / `NOT`, `NEAR(a b, 5)`. Sıralama BM25'tir; kısa cümleler öne çıkma eğilimindedir.
- **Mecmualar:** Ana cilde eşlenen paragrafların cümlesi yoktur. Bu yüzden aynı cümle aramada iki kez çıkmaz.
- **Âyetler:** İki biçim çözülür: "Bakara Sûresi, 2:255" ve Hayrat'ın "Sûre-i Bakara, 255" biçimi. Sûre adlarının numaraları, veride numarasıyla geçen yazılışlardan öğrenilir. Birden çok âyet sayılmışsa ilk aralık alınır. 4.000 âyetin hepsi çözüldü. `data/quran.json` varsa her biri Kur'ân metniyle denetlenir (`arabic.ayah_check`) ve işaretsiz alıntılar bulunur (bkz. Kur'ân katmanı).
- **Anlamsal arama** veritabanında değil, ayrı vektör dosyasındadır (bkz. Anlamsal arama); veritabanı yeniden kurulsa da vektörler kaybolmaz.

## Kur'ân katmanı (Aşama 9)

Kur'ân-ı Kerîm Risale eserlerinden ayrı bir katmandır; atıf birimi âyettir ("Bakara Sûresi, 2:255", `›` olmadan; `cite` bu atıfları denetlemez, doğruluğu `get_ayah`'tan gelir). Ayrıntı `quran.py` başındaki açıklamadadır.

```
uv run python -m risale_mcp.fetch quran   # tanzil.net'ten ham veri (bir kez, 5 dosya)
uv run python -m risale_mcp.quran         # data/raw/tanzil -> data/quran.json
uv run python -m risale_mcp.build_db      # Kur'ân tabloları, âyet denetimi ve eşleme; rapor data/interim/quran/ayah_check.md
```

- **Metin:** kullanıcıya her zaman harekeli Medine Mushafı hattı (`quran_ayahs.text`) gösterilir (kullanıcının isteği: harekesiz okuyamıyor). İmlâî harekeli metin `text_simple`, harekesiz metin yalnızca eşlemede.
- **Mealler:** Diyanet İşleri Başkanlığı ve Türkiye Diyanet Vakfı (Tanzil'den). Diyanet İşleri meali 570 yerde art arda âyetleri (toplam 1.413 âyet, en çok 12) birlikte tercüme eder; Tanzil aynı metni her âyete yazar. Bunlar `first_ayah`..`last_ayah` ile işaretlidir, araç `covers_verses` der. Üç meal türü karıştırılmaz: müellifin "Yani" izahı (metin), nâşirin meali (`publisher_translation`), Diyanet mealleri (`get_ayah`).
- **Sûre adları:** Türkçe 114 ad `quran.SURA_NAMES`'tedir (Tanzil yalnızca Arapça adı verir); veride hiç geçmeyen sûreler de adıyla aranır.
- **Harf iskeleti (`quran.skeleton`):** Risale'nin imlâsı (Türk mushafı, "﷽", "…الخ") Tanzil'inkinden farklıdır. İki metin de iskelete indirilir: hareke ve işaretler, hemze, elif, vav, ye atılır; elif çeşitleri, tâ-i merbûta (ة = ت), Farsça harfler birleştirilir. Alıntı "…" ve "الخ" yerlerinden parçalara bölünür; her parça Osmanî ya da imlâî iskelette aranır.
- **Kaynağın âyetleri denetlenir** (`arabic.ayah_check`): 4.089 âyetin (4.000'i erisale ve Hayrat, 89'u Arapça İşaratü'l-İ'caz) 4.038'i numarasıyla tutar (`exact`), 8'i komşu âyette (`near`), 31'i kelimesi kelimesine tutmaz (`differs`: iktibas, tekrarlanan ifade, birden çok kaynak, Zülfikâr'da âyet diye işaretlenmiş şerh), 12'si boş. Veri değiştirilmez; `find_ayah` sonucunda `check` uyarısı gider. Liste `data/interim/quran/ayah_check.md`'de.
- **İşaretsiz âyetler bulunur** (`ayah_quotes`): Hizb paragrafları numarayı mushaftaki gibi sonda verir ("…﴿٢﴾"); her numaradan önceki metin o numaralı âyetle biten yerde aranır. Kısa ve birden çok sûrede geçen âyet ("الٓمٓ﴿١﴾"), bölümde bulunan öbür âyetlerin en az %80'i aynı sûredense o sûrede aranır. el-Mesnevî el-Arabî'nin "﴿ … ﴾" alıntısı yalnızca Kur'ân'da tek yerde geçiyorsa (iskelette en az 6 harf) bağlanır. 2.373 alıntı bulundu (Hizbü'l-Kur'ân 1.848, Hizbü Envâr 266, el-Mesnevî el-Arabî 259); 161'i bağlanamadı (Hizbü Envâr'daki ﴿n﴾ sayaçları, dua içindeki iktibaslar, birden çok âyette geçen kısa ifadeler).
- **Hizbü'l-Kur'ân'ın sûre sınırları** artık fihristten değil metindeki Arapça başlıklardan gelir (bkz. risaleoku satırı); 1.850 âyetin hepsi kendi sûresinin altındadır.

## Âyet ilişkileri (Aşama 10)

Risale'nin bir yerinin bir âyetle kurduğu bağ (`ayah_links` tablosu). `build_db` Kur'ân katmanını kurduktan sonra kurallarla çıkarır; ayrıntı `ayah_links.py` başındadır. Bu bağlar **"tefsir" diye anılmaz** (kullanıcının kararı): bir yerin bir âyetin tefsiri olduğu bir hükümdür, kural ise yalnızca metnin âyetle kurduğu bağı bulur; yanlışlıkla tefsir sınıfına alınan bir yan cümle vebal olur.

```
uv run python -m risale_mcp.ayah_links    # data/interim/ayah_links/links.md (hepsi) ve sample-<tur>.md (40'lık örneklem)
```

- **Türler:** `isaret` (âyetin geçtiği cümlede "işâret, remz, nükte, tefsir, mânâ, meâl"), `acilis` (bölümün ilk paragrafı âyet; Besmele sayılmaz), `izah` (âyetin hemen ardından ya da sonraki cümlenin başında müellifin "Yani"si; aslı Arapça eserlerde Türkçe ifade mütercimindir), `dayanak` ("… sırrınca, sırrıyla, fermânıyla"), `risale` (âyetin Risale-i Nur'a işâreti: Şualar › Birinci Şuâ ve başlığında "Risale-i Nur'a işâret" geçen bölümler; ayrı tür, kullanıcının kararı).
- **Kapsam ve güç:** bağ bölümün ilk iki cümlesindeyse ve açılışta bölümün tamamı (`section`), değilse kanıt cümlesi (`sentence`). Bölüm kapsamlılar ve `izah` güçlü, öbürleri zayıf: zayıf ilişki yalnızca bir cümlenin âyete atfıdır, bölümün konusu gibi sunulmaz (kullanıcının "zayıf ilişki" fikri).
- **İlk gözden geçirmeden çıkan kurallar** (kullanıcı, 1. tur): "işâret" gibi kelime âyete en çok 8 Türkçe kelime uzakta olmalı, âyet cümlenin başında değilse (önünde en çok 3 kelime: "İkinci Cümle: …") uzaktaki kelime bağ kurmaz; sûreyi adlandıran âyet ("Sûre‑i وَالتّ۪ينِ", "اِقْرَأْ … Sûresi") zayıf; cifir/ebced cümlesi, âyet başta değilse zayıf; "İşârât-ı Kur'âniye", "İşârâtü'l-İ'câz" risale adı, kanıt değil; mektup eserlerinde yalnız "وَاِنْ مِنْ شَيْءٍ اِلَّا يُسَبِّحُ بِحَمْدِه۪" ile açılış bir açılış ibaresidir, `acilis` değil (Sözler'in Pencereleri öyle değil).
- **Kararlar kilitli:** kullanıcının örneklem kararları `tests/golden/ayah_links_review.json`'da; gerçek veritabanında hepsinin tuttuğu test edilir, yeni örneklem bunları dışarıda bırakır. Kaynakta âyet ile önündeki Arapça ayrı işaretlidir ("فَاسْتَمِعْ اٰيَةَ" `arabi`); tabloda âyetin eserdeki metni ayrı sütundur.
- **Kapsam dışı:** Hizbler (Kur'ân metninin kendisi), mecmualar (metni ana ciltlerde), Fihrist bölümleri (özet).
- **Sayılar** (2026-10-27, 1. tur düzeltmelerinden sonra; Arapça İşaratü'l-İ'caz'ın 37 açılışı eklenince 920 ilişki, 292'si güçlü): 883 ilişki, 255'i güçlü: `isaret` 86 güçlü / 437 zayıf, `acilis` 76, `izah` 55, `dayanak` 17 / 136, `risale` 21 / 55. 1. turda kullanıcının baktığı 22 güçlü ilişkiden 17'si doğru, 5'i yanlıştı; düzeltmeden sonra 22'si de kararıyla uyumlu. 2. turda (düzeltilmiş kurallarla, yeni 40'lık örneklem) 40'ın 40'ı doğru; 62 karar kilitli. Kullanıcının örneği (Lem'alar › Otuzuncu Lem'a › Altıncı Nükte › İkinci Şuâ › Birinci Mes'ele: Bakara 2:255, Hûd 11:56, Zümer 39:63) bölüm kapsamlı `isaret`'tir.
- **Gözden geçirme:** güçlüler doğrudan kabul edilir; kullanıcı her turda 40'lık örneklemi (`sample-<tur>.md`) kontrol eder, bulduğu hatalar kurallara ve karar dosyasına döner. Zayıflar tek tek gözden geçirilmez.
- **Araçlar:** `find_ayah` tek âyette `links` (güçlüler önce, kanıt cümlesiyle), `get_ayah` `linked_in_works`, `read_section` başlıkta `linked_verses`. Talimat: ilişkiyi türüyle ve kanıtıyla an, "tefsir" deme; ilişkili âyetleri her alıntının ardına ekleme, kullanıcı sorarsa ya da âyet soruyla ilgiliyse ver (kullanıcının isteği).

## Aslı Arapça eserler (Aşama 11)

Bediüzzaman'ın Arapça yazdığı eserlerin hem Arapça aslı hem Türkçesi tutulur; ikisi ayrı eserdir, bölüm kimlikleri paraleldir (`isaratul-icaz-arabi/sure-i-bakara/6` ↔ `isaratul-icaz/sure-i-bakara/6`). Anlamsal arama iki dili aynı bölümde buluşturur.

| Eser | Arapça | Türkçe |
|---|---|---|
| el-Mesnevî el-Arabî | `el-mesnevi-el-arabi` (rasaelalnour, Badıllı'nın "el-Kâmil" baskısı) | `mesnevi-i-nuriye` (erisale) |
| İşaratü'l-İ'caz | `isaratul-icaz-arabi` (rasaelalnour) | `isaratul-icaz` (erisale, Abdülmecid Nursî tercümesi) |
| Kızıl İcaz | `kizil-icaz-arabi` (Saykalü'l-İslâm) | ücretsiz kaynak yok; tam tercümeler basılı ve telifli (Akgündüz, Niyazi Beki); `kizil-icaz` bekliyor |
| Ta'likat | `talikat-arabi` (Saykalü'l-İslâm) | `talikat` (Protranslate tercümesi, Keşif Yolculukları programı) |
| Hutbe-i Şamiye | `hutbe-i-samiye-arabi`: İhsan Kasım'ın Türkçeden tercümesi (1911 aslı değil) | `hutbe-i-samiye` (erisale) |
| Rumuzat-ı Semaniye | — | `rumuzat-i-semaniye` (kullanıcının PDF'i; aslı Türkçe, bkz. aşağıda) |

**İşârâtü'l-İ'câz (Arapça)** (kurallar `books/rasaelalnour.py` başında, kullanıcının kararlarıyla):
- Eser "مقدمة الترجمة التركية"den "باسمه سبحانه"ya (talebelerin sözü) kadardır; muhakkikin ön sözleri, takriz ve "قالوا عن القرآن" alınmaz. Müellifin Türkçe yazdığı ön kısım (Tenbih, üç Nükte) İhsan Kasım'ın tercümesidir; alınır, alt başlıkta işaretlidir.
- Sayfa satırları ("إشارات الإعجاز - ص: 38") atılır; sayfa sonunda bölünen paragraf birleşir. Dipnotlar "_____" çizgisinden sonra ya da çizgisiz sayfada sonda "(1) …" diye; numara her sayfada baştan, metindeki işaret ("كان 1", "الجعل(1)") silinir. "(المؤلف)" / "- المؤلف." müellifin hâşiyesi (6), "(ت: n)" Türkçe tercümeden açıklama (not), işaretsizler muhakkikin notu (not).
- Bakara'nın âyet bölümleri Türkçe eserle aynı adı ("6. Âyetin Tefsiri") ve kimliği taşır (Türkçe eserin aynı âyetleri kapsayan bölümünden); basılı âyet satırı alt başlıktır. Âyet bölümü, açılmış son âyetten sonraki âyet numaralarını taşıyan ortalı satırlarla açılır (önünde "***" olabilir ya da olmayabilir; eksik basılmış numara sıradan tamamlanır); "***"tan sonra açılmış âyetleri tekrar eden satırlar ortalı paragraftır. Arapça baskı 21-22'yi tek bölümde işler (Türkçede ayrı).
- Fâtiha'nın bölümleri paragraf başındaki parantezli âyet parçasıyla ("(الحَمْدُ)") açılır; kimlikler Türkçe eserden (`FATIHA_SECTIONS`). Ortalı "مقدمة", "فصل…" ve tek başına "المبحث الاول:" gibi etiketler alt bölümdür.
- Paragraf başındaki numaralı "المسألة/المبحث/المأخذ/الوجه …:" etiketi de bölüm açar (Türkçedeki "Birinci Mes'ele" gibi; 28 ve 29. âyetler); Türkçede bölüm olmayan "النكتة", "المقام" açmaz.
- **Âyetler:** muhakkikin "سورة الأنعام: 90" dipnotu, hemen önündeki parantezli alıntıyı âyet yapar (kaynağı bu not; Türkçe sûre adıyla "En'âm Sûresi, 6:90"): 89 alıntı, 88'i Kur'ân metniyle tutar. Dipnotsuz parantezli alıntılar `build_db`'de (`quran.verse_context`, `Quran.locate_quote`) bulunduğu bölümün işlediği âyetlerde aranır: Bakara'da başlıktaki numaralar, Fâtiha'da bölümün âyet parçası (`quran.FATIHA_VERSES`); bulunmazsa yalnızca Kur'ân'da tek yerde geçen uzun alıntı. 548 alıntı (`ayah_quotes`, `via: text`); bölüm tek âyeti işliyorsa iki harfli parça da ("(رَبِّ)") aranır. Her âyet bölümü işlediği âyetle `acilis` ilişkisi kurar (37).
- Sayılar: 86 düğüm, 1.283 paragraf, 3.550 cümle, 6 hâşiye, 328 dipnot (1'i işaretsiz kaldı).

**el-Mesnevî el-Arabî** (kullanıcının kararıyla Abdülkadir Badıllı'nın "el-Kâmil" baskısı; kurallar `books/mesnevi_arabi.py` başında). Neden bu baskı: tamamen harekeli (harflerin %80'i; risaleoku ve İhsan Kasım Word'ü %5–10), müellifin hâşiyeleri işaretli, Lem'alar ve Reşhalar Türkçe eserin numaralarıyla bölünmüş. risaleoku metninde dipnotlar yoktu.
- Badıllı'nın ön sözü ve sondaki fihrist alınmaz; eser "ترجمة المقدمة التركية"den başlar. Müellifin Türkçe yazdığı Mukaddime'nin Arapçası tercümedir; alt başlıkta işaretli.
- Risaleler ve bölümler Türkçe eserin kimliklerini taşır, başlıklar basılı Arapçadır: `mukaddime/nokta-01..05`, `itizar`, `lemalar/lema-01..14`, `reshalar/resha-01..14` (Ondördüncü Reşha'nın Katre ve Noktaları içinde), `lasiyyemalar`, `katre` (`bab-01..04`, Birinci Bâb'ın hâtimesi `bab-01/hatime`, `hatime` ve Nükte/Nokta dizisi, `zeyl` ve 22 Remz), `hubab` (Meclis-i Mebusan hutbesi, `zeylul-hubab`), `habbe` (`zeylul-habbe`, `zeyl`), `zuhre`, `zerre`, `semme`, `onuncu-risale`, `sule`. Türkçe Mesnevî'de olmayan "نور من أنوار نجوم القرآن" `nur` kimliğiyle. Türkçedeki "Nokta" risalesi bu baskıda yok; arşivdeki ayrı dosyadan (İhsan Kasım baskısı, harekesiz) `nokta` olarak eklenir: aslı Türkçedir, alt başlıkta "İhsan Kasım es-Sâlihî'nin tercümesi" diye işaretli; `ifade-i-meram` (dört bürhânı kısaca sayan `ifade-i-meram/burhan-01..04`) ve `burhan-01..04`, Türkçeyle aynı kimlikler. Paragraf başındaki "اَللَّمْعَةُ الرَّابِعَةُ:", "اَلرَّشْحَةُ …", "النُّقْطَةُ …" etiketleri bölüm açar (11–14: "الحادية عشرة").
- Dipnotlar gerçek Word dipnotudur: "ـ المؤلف ـ" (harekeli de) müellifin hâşiyesi (9), "ـ الناشر ـ", nüsha farkları ("بتصحيح المؤلف", "في نسخة …") ve öbürleri naşirin notu (542).
- **Âyetler:** 310 âyet QCF yazı tipiyle kodlu; glif kodları Quran.com verisiyle âyetin adresine ve Osmanî harekeli metnine çevrilir, kaynak glifin kendisidir (301'i Kur'ân metniyle birebir tutar). Tanınmayan glif aynı sayfada tanınan kelimelerin arasındaysa sayfa verisinden tamamlanır. "{اِعْلَمْ}" gibi süslü parantezler âyet değildir.
- **Cümleler:** bu baskı cümleleri klasik baskılar gibi " * " ile ayırır; eserin JSON'u `stops: "*"` taşır ve cümle bölücü yalnızca bu eserde "*"ı da cümle sonu sayar (Nokta ile 7.020 cümle).
- Arapça Mesnevî'nin kimlikleri değişince ona eşlenen mecmualar (`build --all`) yeniden eşlendi.

**Saykalü'l-İslâm eserleri** (kurallar `books/saykal.py` başında; sayfa ve dipnot işleri İşârâtü'l-İ'câz'la ortak). Muhakkikin ön sözleri alınmaz, kökte notla belirtilir. Bu üç eserde parantezli âyet alıntıları da Kur'ân'da tek yerde geçiyorsa bulunur (`build_db` artık bütün Arapça eserlerde arar).
- **Kızıl İcaz (Arapça)** (`kizil-icaz-arabi`): Ahdarî'nin manzum Süllem'ine hâşiye. Kalın beyitler Süllem'indir, `quote` olarak durur (müellifin sözü değil); "[1] …" satırları ve "اعلم!" bahisleri müellifin metnidir, "[n]" numaraları beytin kelimesiyle eşleşir ve metinde kalır. Sayfa dipnotları Molla Abdülmecid'in şerhidir: kullanıcının isteğiyle okunur bir katmandır (228), hâşiye gibi cümlesine bağlıdır ama `commentator: "Abdülmecid Nursî"` taşır, atfı "› Şerh ›"; müellife mal edilmez. Abdülmecid'in mukaddimesi ve i'tizârı alınmaz. Bölümler Süllem'in fasılları (`fasl-01..08`; `fasl-02/delalet`, `fasl-07/muharrefat`); ilk fasıldan önceki beyitlerin düğümü `dibace`: "ديباجة" başlığı kaynakta yok, alt başlıkta "Bu başlık kaynakta yoktur…" diye işaretli (Türkçe Ta'likat'ın "Hadd Bâbı" ve "Dördüncü Bâb: Deliller" başlıkları da). Türkçesi yok (`kizil-icaz` bekliyor). 13 düğüm, 413 paragraf, 879 cümle.
- **Ta'likat** Arapça (`talikat-arabi`, Saykal) ve Türkçe (`talikat`, Protranslate'in tam tercümesi; Keşif Yolculukları programının Word dosyası, telif bildirimi kaynak belirtmek şartıyla serbest kullanım tanır). Gelenbevî'nin Burhân'ına hâşiye; bölümler Burhân'ın müellifin alıntıladığı bölüm başlarıdır ("[فصل في الكليّ والجزئي]" / "﴾Mutlak olarak yüklem faslı…vs.﴿", ortalı Türkçe başlıklar), iki dilde aynı 11 kimlik (`saykal.TALIKAT_SECTIONS`; Türkçe başlıkların bir kısmı bizim: "Hadd Bâbı" gibi). Arapçada dipnotlar müellifin satır arası ve "(تقرير)" hâşiyeleridir (430), Badıllı'nın Burhân göndermeleri ("كلنبوي ص/…") ve "ع. ب" notları not. Türkçede Word dipnotları hâşiyelerin tercümesi (420), köşeli ayraçlı açıklamalar ve Badıllı/Gelenbevî notları not; "-A. B.-" (Badıllı'nın tercümesi) not olur, "[Sayfa: N]" satırları atılır. Arapça 2.933, Türkçe 3.989 cümle.
- **Hutbe-i Şamiye (Arapça)** (`hutbe-i-samiye-arabi`): İhsan Kasım'ın Türkçe metinden tercümesi (1911'de okunan Arapça aslı değil); kökün alt başlığında işaretli. Bölümler Türkçe eserin kimliklerini Türkçe başlıktan alır (`saykal.HUTBE_SECTIONS`; Kelime ve Vehim numarayla); Türkçede ayrı bölüm olmayan "فقرة تركتها من فهرس المقاصد" `zeyl/fihristul-makasid-fikrasi`. Arapça baskıda Hakikat Çekirdekleri ve İkinci Zeyl yok. "المؤلف" dipnotu müellifin hâşiyesi (4), "المترجم" ve öbürleri not. 32 düğüm, 805 cümle.
- Sunucu talimatına 14. kural eklendi: eserin her katmanı müellifin değildir (tercüme alt başlıkları, Süllem beyitleri, `commentary_by` taşıyan Abdülmecid şerhi: onun adıyla atfedilir).

## Rumuzat-ı Semaniye (kullanıcının PDF'i)

Kurallar `books/rumuzat.py` ve `books/pdf_text.py` başında. PDF Yirmi Dokuzuncu Mektub'un Üçüncü (Dokuz Mes'ele), Dördüncü (üç Nükte; lafz-ı Kur'ân ve lafz-ı Resul silsileleri) ve Sekizinci Kısmını (Remizler) taşır; kimlikler Mektubat'ınkiyle aynı (`kisim-03/mesele-01`). erisale'nin Mektubat'ında yalnızca Üçüncü Kısım'ın Birinci Mes'elesi ve Dördüncü Kısım'ın Üçüncü Nüktesi var: o paragraflar (ve Barla Lâhikası'ndaki birkaç parça) eşlenir; yalnız düz paragraflar eşlenir, âyet listesi maddeleri bu eserde kalır.
- **Arapça:** PDF'in karakter eşlemesi Arapçada bozuktur (hareke ve noktalar harf diye gelir). Gömülü DejaVu Sans glifleri sistemdeki DejaVu ile birebir eşlendi, Arial'ın 38 glifi gözle okundu; tablo `rumuzat_glyphs.tsv`. Bazı harfler noktasız gövde + ayrı nokta glifidir; nokta sayısı ve yeri harfi verir (ب ت ث ن ي, ف ق). Harekeler akışta ardından geldiği harfe, akışta yalnızsa ("۪" Arial'dadır) konumla bağlanır; "۪" uzun "i"nin önündeki harfe. Glifler görsel sırada gelir; Arapça parçalar ters çevrilir, rakam dizileri ve ayraçlar düzeltilir. Sonuç sayfa görüntüsüyle karşılaştırıldı; çözülemeyen glif 0. Metin kaynağın imlâsıdır (Farsça ک, ھ; kelimeler bazen bitişik).
- **Yapı:** kalın ≥14 punto (ya da kalın, köşeli ayraçlı) satırlar başlık; paragraf başındaki numaralı etiketler (Mes'ele, Nükte, Silsile, Remiz, Parça, Kısım, Letafet, Misal, Esas, Makam) bölüm açar. Sekizinci Kısım'ın "Birinci remiz altı remizdir" dediği alt remizler kaynakta başlığı olmayan `kisim-08/remiz-01`'de toplanır (alt başlıkta işaretli).
- **Hâşiye:** metindeki küçük mavi "(Hâşiye)" işaretleri, metni sol kenarda aynı etiketle başlayan satırlar; her metin aynı etiketli en yakın önceki işarete bağlanır (20). İki hâşiyenin işareti PDF'te yok; önceki paragrafın sonuna bağlandı.
- **Tablolar** (24; silsile sahife numaraları, cüz cüz lafzullah sayıları, sûrelerin harf/kelime/âyet sayıları) `table` paragrafıdır; sayfada bölünen tablo birleşir. Âyet ve hadis türü PDF'te işaretli değil: `arabi`.
- Sayılar: 73 düğüm, 341 paragraf, 1.942 cümle, 572 Arapça parça.

## Anlamsal arama (Aşama 8)

Kelime araması metindeki kelimelere bağlıdır: "ümitsizlik" diye sorulunca "ye's" geçen yer bulunmaz. Anlamsal arama cümlelerin anlamca yakınlığına bakar. İki arama ayrı araçtır (`search`, `semantic_search`); birleştirmek (RRF) değerlendirmede sonucu bozdu.

```
uv run python -m risale_mcp.embeddings build voyage-context-4    # eksik vektörleri çıkar (yalnızca değişen metin)
uv run python -m risale_mcp.embeddings status                    # depolar ve eksikler
uv run python -m risale_mcp.search_eval run words server sections  # değerlendirme
```

- **Model:** Voyage `voyage-context-4` (`embeddings.SEARCH_MODEL`). Bağlamlı modeldir: bir bölümün kendi cümleleri birlikte gönderilir (uzun bölüm ≈8 bin tokenlık parçalara bölünür), her cümlenin vektörü bölümün bağlamını taşır. Vektörler sağlayıcıdan 512 boyutlu int8 alınır (≈56 MB); 1024 boyutlu float16 ile aynı isabet.
- **Anahtar:** vektörü çıkarılan metinden gelir (bölüm metninin özeti + cümlenin sırası). Ayrıştırma bir bölümü değiştirirse yalnızca onun vektörleri yeniden çıkarılır; `build` sonunda eksik vektör sayısını bildirir. Vektörü olmayan cümle aranmaz, sonuçta `unindexed_sentences` sayılır.
- **Sorgu:** her aramada sorunun vektörü Voyage'dan alınır (bellekte önbellek), benzerlik yerelde (numpy, kosinüs). Anahtar ya da vektör yoksa araç modele açıklamalı hata verir, kelime aramasına yönlendirir.
- **Bölümler:** en yakın 300 cümle kendi bölümüne ve üst bölümlerine puan verir (bölüm başına en çok 5); en yüksek 5 bölüm `sections`'tadır. Asıl işlendiği yeri cümlelerden iyi bulur.
- **Değerlendirme:** `tests/golden/semantic_queries.json` (50 soru, günümüz Türkçesi, beklenen ve yan bölümler; kullanıcı onayladı) ve `search_eval.py`. Ölçüler: hit@k (beklenen bölümden bir cümle ilk k sonuçta), MRR, any@10 (yan bölümler dahil). Raporlar `data/interim/search_eval/`.
- **Model karşılaştırması** (2026-10-26, ilk 10'da beklenen bölüm / MRR): kelime araması %2 / 0,02, kelimelerden biri %18 / 0,09, OpenAI `3-small` %26 / 0,11, `3-large` %48 / 0,27, Voyage `multilingual-2` %42 / 0,20, `4-lite` %42 / 0,24, `4` %46 / 0,27, `4-large` %70 / 0,40, `4-large` + bölüm yolu %52 / 0,26, **`context-4` %74 / 0,49**, `context-4` + kelime araması (RRF) %64 / 0,38. Ölçüm temkinlidir: kaçırılan sorularda model çoğu zaman konunun başka bir geçtiği yeri bulur.

## Taksimat kontrol arayüzü

Ayrıştırılan başlık ağacını, metni ve cümle bölmesini elle kontrol etmek içindir. `data/books/<eser>.json` okur.

```
uv run python -m risale_mcp.review_ui [eser…]   # data/interim/review/ üret (eser verilirse yalnızca onların metni yenilenir)
xdg-open data/interim/review/index.html
```

- **Tek sayfa, bütün eserler:** Sol paneldeki ağaçta eserler gruplarıyla (Eski Said dönemi, ana ciltler, mecmualar, Hizbler) durur. Bütün başlık ağaçları `index.html`'e gömülüdür; bir eserin paragraf ve cümleleri `data/<eser>.js` dosyasındadır ve o eserden bir başlık açılınca `<script>` ile yüklenir. Sunucu ya da internet gerekmez. Kaynak dosyalar `src/risale_mcp/review_assets/` altındadır; `review_ui.py` yalnızca bunları birleştirir.
- **Sayfa bilgisi yok.** Gezinme tamamen hiyerarşiktir.
- **Sol panel:** Başlık ağacı ve başlıklarda arama.
- **Sağ panel:** Seçilen düğümün yolu, başlığı, alt başlığı, kimliği ve kendi metni; hâşiyeler (metindeki işarete tıklanınca vurgulanır); alt bölümler; önceki/sonraki bölüm (← / →).
- **Arapça eserler** sağdan sola gösterilir. **Mecmualarda** ana cilde eşlenen paragrafın yerinde, ana cildin o bölümünü açan bağlantı durur; düğüm başlığında ana ciltteki karşılıkları listelenir.
- **Cümleler:** Her cümlenin başında küçük numarası durur. Numaraya tıklanınca cümlenin atfı, incipit'i, kimliği ve işaret düğmeleri açılır. İşaretli cümlenin altı yeşil (✓) ya da kırmızı (✗) çizilir. Arapça paragraflar sağdan sola gösterilir; Kur'an işaretlerinin düzgün görünmesi için Amiri ya da Scheherazade New yazı tipi gerekir.
- **URL:** Seçili düğümü tutar (`index.html#sozler/10/on-iki-hakikat/hakikat-09`); mecmuadaki ana cilt bağlantıları aynı sayfada açılır. ← / → bütün eserler boyunca kitap sırasında gezer.
- **İşaretler:**
  - Her düğüme, paragrafa ve cümleye "✓ doğru / ✗ hatalı / ✎ not" konabilir; eser başına ayrı anahtarda (`risale-review:<eser>`) `localStorage`'da saklanır.
  - Dışa aktarma bütün eserlerin işaretlerini tek dosyaya yazar (`risale-kontrol-notlari.json`). Her kayıtta `book`, `id`, `target` (`node` | `passage` | `sentence` | `missing`), `ref`, `incipit`, `status`, `note` bulunur. Bu dosya ayrıştırma düzeltmelerinin girdisidir.
  - "İçe aktar" ile başka bir tarayıcıya taşınabilir; eski, eser başına dışa aktarılmış dosyaları da okur.
  - Cümle işaretleri incipit ve düğümle birlikte saklanır. Kimlik kayarsa işaret, açılışta aynı düğümde (yoksa bütün eserde tek eşleşen) incipit'ten yeniden bağlanır. Bağlanamayan `target: "missing"` olarak görünür.

## MCP sunucusu (Aşama 6)

`src/risale_mcp/server.py` (resmi Python SDK 2.x, `MCPServer`; v1'deki adı FastMCP). Veritabanı işleri `library.py`'dedir; sunucu yalnızca araç, kaynak ve hazır komut katmanıdır. Sunucunun adı `risale`, adresleri `risale://…`.

```
uv run risale-mcp                                       # stdio (Claude Desktop / Claude Code başlatır)
uv run risale-mcp --transport streamable-http --no-auth # yerel HTTP 127.0.0.1:8000/mcp (kimlik doğrulamasız, yalnız bu bilgisayar)
uv run risale-mcp --transport streamable-http --public-url https://<makine>.<ağ>.ts.net   # OAuth'lu (bkz. Uzaktan erişim)
uv run risale-mcp --transport streamable-http --public-url https://<…> --anonymous   # hesapsızlar da (sınırlı), hesaplılar sınırsız
npx @modelcontextprotocol/inspector uv run risale-mcp   # MCP Inspector
```

Claude Desktop (`claude_desktop_config.json`; Linux'ta `~/.config/Claude/`):
```json
{"mcpServers": {"risale": {"command": "/home/fatih/.local/bin/uv",
  "args": ["--directory", "/home/fatih/Belgeler/Coding/Projects/risale-mcp", "run", "risale-mcp"]}}}
```

- **Dil:** Modelin okuduğu her şey (talimatlar, araç ve parametre açıklamaları, hazır komutlar, hata iletileri) İngilizcedir; model kullanıcıya onun dilinde cevap verir. Kod açıklamaları Türkçe.
- **Sonuçlar** sıkıştırılmış JSON metnidir (SDK'nın girintili JSON'u uzun metinde boşa token harcar). Bütün araçlar salt okunur (`read_only_hint`).
- **Veritabanı yenilenince** (`build`/`build_db`) sunucu yeniden başlatılmadan bir sonraki çağrıda yeni dosyayı açar.
- **Hatalar:** bilinmeyen kimlik, geçersiz sorgu gibi düzeltilebilir hatalar modele açıklamalı ileti olarak gider (`ToolError`).

| Araç | İşi |
|---|---|
| `list_works(group?)` | Eserler, kimlikleri, grupları, boyutları; metni bulunamayanlar `available: false` |
| `get_outline(section, depth=2)` | Başlık ağacı; her düğümde alt ağacın ana metin cümle sayısı, derinlik sınırında `subsections` |
| `read_section(section, cursor?, max_words=1500)` | Bölümü alt bölümleriyle kitap sırasıyla okur: başlıklar (`ref`; bölümün bağ kurduğu âyetler `linked_verses`), paragraflar (cümle `id` + metin), hâşiyeler (`hasiye_of`), âyet/hadis meal ve kaynağı, eksikler (`gap`). Paragraf sınırında sayfalar, `next_cursor` ile sürer. Mecmuada eşlenmiş paragraf ana cildin cümleleriyle (`canonical`) gelir. |
| `get_passage(id, context=0)` | Cümle ya da aralık (`…/c010..c015`), `ref` ve `incipit` ile; bağlı hâşiyeler ve âyet mealleri. Bir bölümde en çok 8 cümlelik aralıkta kullanıcıya gösterilecek atıf (`cite_as`: "… ile başlayan N cümle"). Bölümün sonunu aşan aralık son cümlede kesilir (`note`). |
| `search(query, work?, group?, limit=20, offset=0)` | Cümle araması (`search.py` sorgu dili); toplam, eser başına sayı, eşleşen başlıklar |
| `find_sentence(incipit, scope?)` | İlk kelimelerden cümle (işaretsiz; son kelime eksik olabilir) |
| `find_ayah(sura, ayah?)` | Âyetin eserlerde geçtiği cümleler; sûre numarası ya da adı. `via: source` kaynağın işaretlediği, `via: text` Kur'ân metninde bulunan işaretsiz alıntı; `check` kaynağın numarası metinle tutmuyorsa uyarır; tek âyette âyetin kendisi (`quran`) ve âyetle bağ kuran yerler (`links`: tür, güç, kanıt cümlesi; güçlüler önce) |
| `get_ayah(sura, ayah, end?, context=0)` | Kur'ân'dan âyet ya da aralık (en çok 30): harekeli metin, iki Diyanet meali (`covers_verses`: birlikte tercüme edilen âyetler), atıf (`ref`), eserlerde kaç kez geçtiği ve kaç yerin bağ kurduğu (`linked_in_works`), Tanzil atfı |
| `semantic_search(query, work?, group?, limit=10, offset=0)` | Anlamca en yakın cümleler (`similarity`) ve konunun yoğunlaştığı bölümler (`sections`); kavram ve günümüz Türkçesiyle sorular için. Kelime araması (`search`) ayrı kalır. |
| `cite(sources)` | Cevaptan önce bir kez: dayanılan cümle ya da aralıkların kimlikleri ve alıntılanan sözler (`[{id, quote?}]`, kaynakça sırasıyla). Her biri için tam atıf (`cite_as`), sorun (aralık 8 cümleyi ya da bölümü aşıyor, alıntı o cümlelerde yok: asıl yeriyle, bilinmeyen kimlik) ve cevabın "Kaynaklar" listesi (`bibliography`: "[n] cite_as"). Önceki `verify_citations(text)` taslağın tamamını alıyordu (bkz. Hız ve token) |

### Uzaktan erişim ve OAuth (Aşama 12)
Ayrıntı `auth.py` başındadır. Sunucu internete yalnızca OAuth ile açılır; `--no-auth` yalnız `127.0.0.1`'de çalışır, stdio değişmedi.
```
uv run risale-mcp auth add-user <ad> [--generate]   # hesap (parola en az 10 karakter; --generate rastgele üretir)
uv run risale-mcp auth passwd|remove-user <ad>      # parola değişince ve silinince oturumlar kapanır
uv run risale-mcp auth users | sessions [--user]    # hesaplar, açık oturumlar
uv run risale-mcp auth revoke --user <ad> | --session <id> | --all
uv run risale-mcp auth usage [--user <ad>] [--limit 50]   # kullanım kaydı
```
- **Hesaplar** kişi başınadır (kullanıcının kararı); herkese bütün derlem açıktır. Parola scrypt özetiyle `data/auth.db`'de; 5 yanlış denemeden sonra hesap 60 sn (her yeni hatada iki katı) kilitlenir.
- **Akış:** SDK'nın yerleşik yetkilendirme sunucusu (üst veri, dinamik kayıt, PKCE S256, jeton, iptal) ve bizim sağlayıcımız (`auth.Provider`). `/authorize` giriş sayfasına (`/login`) yönlendirir; sayfa hangi istemcinin hangi adrese döneceğini gösterir, yerel adreste uyarır. Erişim jetonu 1 saat, yenileme jetonu 30 gün; yenileme jetonu her kullanımda değişir, kullanılmışı `invalid_grant` alır. Jetonların yalnızca SHA-256 özetleri saklanır.
- **Hesapsız erişim (`--anonymous`; kullanıcının kararı 2026-10-28: avukatının görüşü ve kaynaklara izin isteyen e-postadan sonra herkese açık, "hesaplılar sınırsız, hesapsızlar sınırlı"):** Claude'un "lazy authentication"ı (https://claude.com/docs/connectors/building/lazy-authentication.md). `/mcp` önündeki `auth.AnonymousGate` jetonsuz isteği doğrudan MCP'ye geçirir; jeton taşıyan istek eskisi gibi denetlenir. `sign_in` aracı hesapsız çağrılınca HTTP 401 + `WWW-Authenticate` döner, Claude sohbette "Bağlan" kartı gösterir (hesabı olan böyle giriş yapar). Hesapsızların anlamsal araması günde toplam 2.000 ile (`--anonymous-semantic`), bütün hesapsız istekler dakikada toplam 120 ile sınırlı (429); sınır adres başına değil, çünkü claude.ai'nin istekleri hep Anthropic'in adreslerinden gelir. Hesapsız istekler kullanım kaydında kullanıcısız durur. Maliyet: Voyage sorgu başına onlarca token harcar (ilk 200 milyon token ücretsiz, 2026-10-28'de 12,5 milyonu kullanılmış, sonrası milyon token başına 0,12 $); günlük sınır maliyetten çok yükü sınırlar.
- **Kayıt** yalnızca `https://claude.ai/api/mcp/auth_callback`, `https://claude.com/api/mcp/auth_callback` ve yerel adresleri kabul eder; yerel adreste port karşılaştırılmaz (Claude Code, MCP Inspector).
- **Kullanım kaydı:** her MCP isteği kim, ne zaman, hangi araç, süre ve hatayla `usage` tablosuna yazılır (`auth.usage_middleware`). Parametreler (sorgular, alıntılar) 2026-10-29'dan beri kaydedilmez, eskileri açılışta silinir; hatanın yalnızca türü yazılır, kayıtlar 90 gün tutulur (`auth.USAGE_DAYS`), uygulamanın erişim günlüğü kapalı (IP adresi yazıyordu). Gizlilik politikası (`site/gizlilik.html`) bunları söyler; değişirse orası da değişir. Gerekçe: Anthropic'in dizin politikası (Software Directory Policy 1E, 1G) gereksiz konuşma verisini kayıt için bile toplamayı yasaklar (kullanıcının kararı, dizin başvurusu için).
- **Uzak sunucu (2026-10-28):** Hetzner Cloud CAX11 (ARM, 2 çekirdek, 4 GB; Helsinki; Ubuntu 24.04; ≈7 $/ay), adı `risale-mcp`, genel IPv4 `95.217.21.105`. Bağlayıcı adresi **`https://mcp.risalemcp.com/mcp`** (2026-10-29'dan beri Caddy; önce Tailscale Funnel `https://risale.taile0138b.ts.net/mcp`, kapandı). Makinenin Tailscale adı `risale`, adresi `100.108.174.19` (SSH için). Servis `risale-mcp` (`User=risale`, `/home/risale/risale-mcp`, `--anonymous`, açılışta başlar; birimi `docs/risale-mcp.server.service`). Otomatik güvenlik güncellemeleri açık, saat dilimi İstanbul. Güvenlik duvarı: Hetzner'de 22, 80 ve 443/tcp; sunucuda `ufw` yalnızca 80 ve 443'e izin verir, SSH yalnızca `tailscale0` arayüzünden. SSH anahtarı `~/.ssh/risale_hetzner`.
  - Güncelleme: `scripts/deploy.sh` (kod + `risale.db` + vektörler + `quran.json` + `.env`'den yalnız `VOYAGE_API_KEY`; `uv sync --no-dev --frozen`; servisi yeniden başlatır), yalnız kod için `--code`. Ayrıştırma ve veritabanı kurulumu yerelde yapılır; ham veri sunucuya gitmez.
  - **`data/auth.db`'nin asıl kopyası sunucudadır** (hesaplar, oturumlar, kullanım kaydı); deploy ona dokunmaz. Yönetim: `scripts/sunucu.sh auth …` (ör. `auth add-user <ad> --generate`, `auth usage`), `status|restart|logs|ssh`.
- **Eski yerel çalıştırma (artık yedek):** Funnel `sudo tailscale funnel --bg 8000` ile kalıcı açık, adres `https://fatih-thinkbook-15-g2-itl.taile0138b.ts.net/mcp`. Sunucu systemd kullanıcı servisiyle açılıp kapanır: `docs/risale-mcp.service` (kurulum ve komutlar dosyanın başında; kullanıcı kendisi kurar).
- **Dışarı açma:** önce kullanıcının bilgisayarında Tailscale Funnel (`https://<makine>.<ağ>.ts.net`, alan adı gerekmez); `--public-url` Host başlığı denetimine (DNS rebinding) de eklenir. Bilgisayar kapalıyken erişim için sonra bir sunucuya (Oracle Always Free ya da Hetzner) taşınacak; kod aynı kalır. claude.ai'de özel bağlayıcı adresi `https://<…>/mcp`.
- **Logo:** claude.ai özel bağlayıcıları logosuz, "Custom" diye gösterir; sunucunun `icons` alanını ve favicon'unu kullanmaz. Logo yalnızca Anthropic'in bağlayıcı dizinine kabul edilen bağlayıcılarda görünür.
- **Kendi alan adı (2026-10-29):** `risalemcp.com` (Cloudflare'de, kayıtlar "DNS only": proxy uzun MCP bağlantılarını 100 sn'de keser, Anthropic'in isteklerine bot doğrulaması gösterebilir). Bağlayıcı `https://mcp.risalemcp.com/mcp`, tanıtım sitesi `https://risalemcp.com` (depoda `site/`). İkisini de aynı makinede Caddy sunar ve sertifikayı Let's Encrypt'ten kendisi alır (`docs/Caddyfile`); Hetzner'de ve `ufw`'de 80/443 açık, SSH hâlâ yalnızca Tailscale'den. Geçiş `scripts/gecis.sh` ile yapıldı (2026-10-29; Funnel 443'ü tuttuğu için önce o kapanmalı); Funnel adresi kapandı, bağlayıcı yeni adresle eklenir. Araçların hepsinde `title` var.
- **Dizin başvurusu (2026-10-29, hazırlanıyor):** kaynak siteler (kastamonur ve diğerleri) e-postaya cevap verip herkese açık kullanıma izin verdi. Yayıncı adı "Nur Hadimleri". Yapıldı: kendi alan adı, her araçta `title`, kullanım kaydında parametre yok, belgeler (`/belgeler.html`, `/en/docs.html`) ve gizlilik politikası (`/gizlilik.html`, `/en/privacy.html`). Kalan: destek e-postası (`destek@risalemcp.com`, Cloudflare e-posta yönlendirmesi), hakem hesabı, tanıtım sitesinin ekran görüntülü rehberi, başvuru metinleri.
- **claude.ai'de ilk deneme (2026-10-28):** bağlantı ve giriş çalıştı; ama model yalnızca iki arama yaptı, hiçbir yeri okumadan ve atıfları denetlemeden cevap verdi (kısaltılmış yol, cümle numarası, alıntısız). Bunun üzerine: `search` ve `semantic_search` sonuçları artık her cümle için `cite_as` (tam yol + ilk kelimeler; `ref` ve cümle numarası yerine) ve okumadan atıf verilmemesini hatırlatan bir `note` taşır (`library.SEARCH_NOTE`); claude.ai'de bir Proje açılıp talimatına `docs/claude-proje-talimati.md` yapıştırılır (her kullanıcı kendi hesabında). Etki kullanım kaydından (okuma ve atıf aracı çağrıları) ölçülür.
- Testler (`tests/test_auth.py`) Claude'un gereksinimlerini süreç içinde dener: jetonsuz istek 401 ve `resource_metadata`, üst veri, kayıt kısıtı, PKCE, yanlış parola ve kilit, vazgeçme, yenileme ve döndürme, port farkı, kullanıcı başına oturum kapatma, kullanım kaydında kullanıcı adı.

### Atıf denetimi (`citations.py`)
Ayrıntı modülün başındaki açıklamadadır. `cite` aracı kimliklerden atıf kurar (`CitationChecker.sources`); altın soru raporu yazılmış cevaptaki atıfları denetler (`check`). Kaynakçalı cevapta "[n]" ile biten alıntı bloğu kaynakçadaki n numaralı atfa bağlanır.
- Satır `›` işaretlerinden bölünür; bir satırda birden çok atıf, atıftan önce ve sonra düz yazı olabilir. Atıf alıntıyla ya da "32. cümle" ile biter.
- Başlık basılı adla, içindekiler adıyla, tür ve numarayla ("İkinci Makam" = "Yirminci Söz’ün İkinci Makamı"), ekli ("Dördüncü Söz'de"), "(asm)" gibi ayraçsız ya da "…" ile kısaltılmış yazılabilir; ara başlıklar atlanabilir. Bunlar geçerlidir ama tam yolu yazılmamış sayılır (`exact`), araç tam atfı verir.
- "…", "aynı yer", "(› …" ve eser adı yazılmamış yol bir önceki atfa göre çözülür. Yol birden çok bölüme uyarsa önce alıntının geçtiği, sonra önceki atfa yakın, ana ciltteki ve üst seviyedeki bölüm seçilir.
- Ardışık cümleler: "“…” ile başlayan N cümle" ya da "› 4.–7. cümle". Aralık bulunan cümleden başlar, aynı bölümün ana metninde (hâşiyede aynı hâşiyede) sürer; 8'i aşarsa `range_too_long`, bölümü aşarsa `range_past_section`.
- Alıntı bloğu: atfın hemen önündeki ya da ardındaki `> "…"` bloğu (araya yalnızca boş satır girebilir) atfın kapsadığı cümlelerde aranır; "…" ile atlanan yer serbesttir. İki atıf arasındaki blok uyduğu atfa bağlanır. Uymazsa `block_ok` yanlıştır.
- Sonuçlar: `ok`, `section`, `mid_sentence`, `quote_not_found` (alıntının asıl yeri `elsewhere`), `no_such_sentence`, `unknown_section`, `ambiguous`, `range_too_long`, `range_past_section`.

### Hız ve token (2026-10-28)
Kullanıcı resmi kullanımda cevapları yavaş buldu. Ölçümler ve yapılanlar:
- **Sunucu yavaş değildi:** kullanım kaydında `get_passage` 18 ms, `verify_citations` 79 ms, `search` 6 ms, `read_section` 2 ms. Gecikme modelin yazdıklarıydı: `verify_citations(text)` cevabın taslağını girdi olarak istiyordu; claude.ai'de model taslağın tamamını çoğu kez üç kez gönderiyordu, cevap 3–4 kez yazılıyordu.
- **`cite` aracı** onun yerine geldi: yalnızca kimlik listesi alır, kaynakça satırlarını döndürür; model cevabı bir kez yazar ve yolu kendisi kurmaz. İlk sürümü alıntıları da alıyordu; model onları cevapta bir kez daha yazdığı için araç claude.ai'de 5 sn sürüyordu (sunucuda 4 ms). Yalnız kimlik alan bir sürüm denendi (2026-10-29): girdi 1.300'den 400 karaktere indi, ama claude.ai'de hız farkı kullanıcının beklediği kadar olmadı (son okumadan `cite`'a 20 sn, çoğu modelin planlaması); kullanıcı alıntı denetimini korumak için alıntılı sürüme dönmeyi seçti.
- **Kaynakça** (kullanıcının kararı, 2026-10-29): kısa ya da uzun her cevapta alıntı sonunda "[1]" ve sonda "Kaynaklar"; metnin içinde atıf yolu yazılmaz. claude.ai'nin yerleşik kaynak kutucukları (API'nin `search_result` blokları) MCP araç sonuçlarında desteklenmiyor (bağlayıcı belgesi: yalnızca metin ve resim), bu yüzden biçim talimatla kurulur.
- **Yapılandırılmış çıktı kapalı** (`structured_output=False`): metin döndüren araçlarda SDK sonucu ayrıca `{"result": "<JSON>"}` olarak gönderiyordu ve Claude Code modele bu kaçışlı biçimi veriyordu.
- **Talimat ve araç tanımları** 19.200 karakterden 13.900'e indi (talimat 7.000 → 3.100); âyet ilişkisi türleri `find_ayah` tanımına taşındı.
- **Isınma:** anlamsal aramanın eşlemesi (sunucuda 1,6 sn) ve atıf dizini sunucu açılırken arka planda kurulur (`server._warm`). Anlamsal aramanın kalan süresi Voyage'ın sorgu vektörüdür (0,3–0,8 sn; TLS 0,04 sn, kalıcı bağlantı kazandırmaz).
- **Sonuç** (`golden.py`, 7 soru: B7 B8 C11 D16 E19 K3 K5; rapor üretilen token ve atıf aracı çağrısını da sayar): ortalama süre 50 → 40 sn, üretilen token 4.992 → 4.237, maliyet 0,33 → 0,27 $; atıfların hepsi doğrulandı, tuzak doğru (`20261028-231108` → `20261028-231718`). Yalnız kimlikli `cite` ve her cevapta kaynakça ile (`20261029-000115`, sonra geri alındı): 41 sn, 3.929 token, 0,25 $; bütün atıflar doğrulandı, atıflı her cevapta "Kaynaklar" var. 8 cümleyi aşan aralık verilince model `cite`'ı bir kez daha çağırır. Claude Code taslağın yalnızca atıflı kısmını gönderiyordu; claude.ai'de kazanç daha büyük olmalı, kullanım kaydından izlenir.

- **Kaynaklar** (kullanıcının sohbete eklediği bağlam): `risale://works`, `risale://outline/{work}`, `risale://text/{+section}` (ör. `risale://text/sozler/10`; numaralı cümlelerle Markdown).
- **Hazır komutlar** (İngilizce adlar): `topic_survey(topic, scope?)` konunun eserlerde geçtiği yerler (2. hedef), `text_and_commentary(question)` "metin ne diyor" ve "yorum" ayrı (3. hedef), `discuss(topic)` müzakere, `self_test(section)` bölümden soru sorup cevabı metinle denetler, `lesson_plan(subject)` atıflı ders planı.
- **Sunucu talimatları:** atıfı araç sonucundan al ve uydurma; kullanıcıya cümleyi numarasıyla değil yol + incipit ile göster; yolu eserden başlayarak tam ve kısaltmadan yaz, önceki atfa göre göreli yazma, `›` işaretini yalnızca atıfta kullan; tırnağı yalnızca metnin kendi sözlerine koy; aynı bölümde birkaç cümle süren temsil, misal ya da düşünceyi tek blokta ve "… ile başlayan N cümle" atfıyla ver (en çok 8 cümle, hâşiye ayrı); her alıntıyı (kısa olanlar ve öncekini genişletenler de) düz yazının içinde değil, kendi satırında tırnak içinde alıntı bloğu (`> "…"`) olarak ver, düz yazıda en çok tek bir terim tırnağa alınır (kullanıcının isteği); cevaptan önce dayanılan cümleleri ve alıntılanan sözleri bir kez `cite`'a ver; her cevapta alıntı sonunda [1] işareti ve cevabın sonunda `cite`'ın verdiği "Kaynaklar" listesi, metnin içinde atıf yolu yok (kullanıcının kararı, 2026-10-29); âyetin Arapçasını yalnızca harekeli ve `get_ayah`'tan (ya da eserin alıntıladığı gibi) ver, ezberden yazma, atfı "Bakara Sûresi, 2:255" biçiminde `›` olmadan yaz, Diyanet mealini adıyla an, birlikte tercüme edilen âyetleri söyle, hiçbir mealin Kur'ân'ın yerini tutmadığını hatırla; âyet ilişkilerini asla "tefsir" diye anma, türüyle ve kanıt cümlesiyle ver, zayıf ilişkiyi bölümün konusu gibi sunma, ilişkili âyetleri her alıntının ardına ekleme (sorulursa ya da konuyla ilgiliyse ver); âyet ve hadis mealleri nâşirindir, müellife mal etme ve metin diye alıntılama, müellifin "Yani, …" izahı metindir; bulamazsan söyle; metni ve yorumu ayır; önce ara, sonra bağlamı oku.

Sonraki aşamalar için bkz. "Aşamalar" (12–17).

## Uçtan uca deneme (Aşama 7)

Linux'ta Claude Desktop olmadığı için MCP istemcisi olarak Claude Code kullanılır. Üç katman:

1. **Araç düzeyi:** `npx @modelcontextprotocol/inspector uv run risale-mcp` (tarayıcıda araçları elle çağırma).
2. **Elle sohbet:** `uv run python -m risale_mcp.golden sandbox ~/risale-deneme` sonra `cd ~/risale-deneme && claude`. Klasör proje dışındadır (Claude Code üst klasörlerdeki `CLAUDE.md`'yi okur); yalnızca bu sunucu açık, dosya/kabuk/web araçları kapalıdır. Hazır komutlar `/mcp__risale__topic_survey`, kaynaklar `@risale:risale://text/sozler/10`.
3. **Altın sorular:** `uv run python -m risale_mcp.golden run A1 B7 …` (ya da `--all`). Her soru `claude -p` ile geçici, boş bir klasörde, yerleşik araçlar kapalı (`--tools ""`), yalnızca bu sunucuyla (`--strict-mcp-config`) ve varsayılan modelle sorulur. `--bare` kullanılmaz (OAuth'u kapatır). Döküm ve rapor: `data/interim/golden/<zaman>/` (`report.md`, git'e eklenmez).

Raporun otomatik kontrolleri:
- **Atıflar:** cevaptaki "Yol › … › “ilk kelimeler”" ya da "… › 32. cümle" zincirleri `citations.py` ile veritabanında aranır: ✓ cümle bulundu, ◑ alıntı metinde var ama cümle başı değil, ◐ yalnızca bölüm, ✗ bölüm ya da cümle yok (uydurma olabilir; alıntı başka yerdeyse orası gösterilir). Yanındaki alıntı bloğu atfın cümlelerinde olmayan atıf da ✗ sayılır. Doğru ama kısaltılmış yolla yazılan atıflar tabloda "(n kısa)", ardışık cümle atıfları "(n aralık)" diye sayılır.
- **Beklenen bölüm:** model okudu mu (`read_section`, `get_passage`, `find_sentence`; arama sonucu ve başlık ağacı okumak sayılmaz), cevapta adı geçiyor mu.
- **Araç kullanımı:** çağrılar, parametreleri ve hatalar.

Metin–yorum ayrımı, özetin doğruluğu ve tuzak sorulardaki davranış elle değerlendirilir. İlk denemede (A1, B7, D16, K5) dört sorunun dördünde model doğru yeri buldu, tuzakta uydurmadı, yorumu ayrı başlıkta verdi. 25 sorunun tamamında (`20261026-113635`) 428 alıntının hiçbiri uydurma çıkmadı, dört tuzağın dördü doğru. Atıfların çoğu kısaltılmış ya da göreli yolla yazılmıştı; bunun üzerine talimatlara tam yol kuralı ve `verify_citations` eklendi.

## Çalışma kuralları

- Aşamaları sırayla yap. Her aşamanın sonunda **dur**, bulguları özetle ve onay bekle.
- Ayrıştırma kurallarını tahmine dayanarak yazma. Önce kaynağın ham verisini incele, örnekleri göster.
- Her aşamada kullanıcının elle doğrulayabileceği bir çıktı üret (örnek JSON, başlık ağacı, sayım tablosu).
- Belirsiz durumlarda en makul varsayımı yap, ama bunu açıkça belirt.
- Kaynak sitelere nazik davran: isteklerin arasında bekle, ham yanıtı kaydet, aynı sayfayı ikinci kez indirme.
- Kod tanımlayıcıları İngilizce, açıklamalar ve kullanıcıyla iletişim Türkçe.

## Aşamalar

Tamamlananlar (PDF dönemi): PDF inceleme, Sözler'in PDF'ten ayrıştırılması ve kontrol arayüzü. Aşama 1–7 tamamlandı (cümle ve eşleme kontrolü kullanım sırasında sürecek). Ardından atıf denetimi (`citations.py`; önce `verify_citations`, 2026-10-28'den beri `cite`) eklendi.

1. **İndirici:** Katalog, nazik istemci, dört sitenin indiricisi ve bütünlük doğrulaması. Önce Sözler pilotu, ardından bütün eserler toplu indirildi:
   `uv run python -m risale_mcp.fetch get --all --site <site>` (her site ayrı süreçte; günlükler `data/raw/logs/`).
2. **Ayrıştırıcı:** erisale blokları → `data/books/<eser>.json` (başlık ağacı, paragraflar, hâşiyeler): `uv run python -m risale_mcp.build --all`. erisale'deki 27 eser ayrıştırıldı; Sözler PDF çıktısıyla karşılaştırıldı, PDF kodu silindi.
3. **Cümleler:** Cümle bölücü (`sentences.py`, `build` içinde çalışır) ve altın örnek testleri; kontrol arayüzüne kitap seçici, cümle numaraları ve cümle düzeyinde işaretler eklendi. Kullanıcı Sözler'i kontrol eder.
4. **Diğer eserler:** risale.online, risaleoku ve kastamonur.com (önce Yeni Asya) ayrıştırıcıları; mecmuaların ana ciltlere eşlenmesi; bulunamayan eserler için kaynak araması. 38/43 eser ayrıştırıldı (`ESERLER.md`).
5. **Veritabanı:** SQLite ve FTS5 kurulumu, normalizasyon, sorgu dili, âyet dizini, birim testler: `uv run python -m risale_mcp.build_db`.
6. **MCP sunucusu:** `library.py` + `server.py`; araçlar, kaynaklar, hazır komutlar; süreç içi istemciyle testler. MCP Inspector ile elle deneme.
7. **Uçtan uca test:** `golden.py` ile Claude Code'u istemci yaparak (Linux'ta Claude Desktop yok) `tests/golden/` sorularıyla dene, adreslerin doğruluğunu elle kontrol et.

Ardından tamamlananlar (numaralar 2026-10-28'de yeniden düzenlendi; eski commit mesajlarındaki "Aşama 13, 14, 15" bugünkü 9, 10, 11'dir):

8. **Anlamsal arama:** A: değerlendirme seti (50 soru, kullanıcı onayladı); B: yerel/API modellerin karşılaştırması (kullanıcı API'yi tercih etti; `voyage-context-4` seçildi); C: `semantic_search` aracı, bölüm sıralaması, 512 boyut int8 depo. Bkz. Anlamsal arama.
9. **Kur'ân katmanı:** Tanzil'den metin ve iki Diyanet meali, `get_ayah` aracı, kaynağın âyetlerinin denetimi ve işaretsiz âyetlerin bulunması. Bkz. Kur'ân katmanı.
10. **Âyet ilişkileri:** Risale'nin hangi yerinin hangi âyetle bağ kurduğu; kurallarla, kanıt cümlesiyle. "Tefsir" denmez (kullanıcının kararı: kuralla bulunan bağ bir hüküm değildir). Kullanıcı güçlü ilişkilerden 40'lık örneklemi gözden geçirir. Bkz. Âyet ilişkileri.
11. **Aslı Arapça eserler:** Arapça aslı ve Türkçesi ayrı eser olarak tutulur, bölüm kimlikleri birbirine paralel; ayrıca Rumuzat-ı Semaniye (kullanıcının PDF'i). Bkz. Aslı Arapça eserler.

Sonraki aşamalar (kullanıcının 2026-10-28 kararıyla bu sırayla):

12. **Sunucu kimlik doğrulaması ve uzaktan erişim (OAuth):** (**tamamlandı 2026-10-28**: kod, testler, claude.ai'den gerçek deneme (hesapsız ve hesaplı), Hetzner'e taşıma, ikon; bkz. Uzaktan erişim ve OAuth; kaynak sitelere herkese açık kullanım için izin isteyen e-posta gönderildi (2026-10-28), hesapsız erişim (`--anonymous`) eklendi; bir kaynak itiraz ederse eseri çıkarılır (`docs/kaynak-bilgilendirme-epostasi.md`; kullanıcının avukatı telif sorunu görmüyor, e-posta nezaket içindir); bkz. Uzaktan erişim ve OAuth) Amaç sunucuyu claude.ai'den (tarayıcı, Desktop, telefon) ve uzaktaki Claude Code'dan özel bağlayıcı olarak kullanmak. Bugün `streamable-http` kimlik doğrulamasızdır ve yalnızca `127.0.0.1`'de dinler; bu hâliyle dışarı açılmaz, çünkü metinler herkese açılmış olur (kaynak sitelerin telif uyarısı, kullanım kişiseldir). Yapılacaklar: MCP'nin yetkilendirme yöntemi (OAuth 2.1, PKCE S256, korumalı kaynak üst verisi RFC 9728, yetkilendirme sunucusu üst verisi RFC 8414, dinamik istemci kaydı RFC 7591) ile tek kullanıcılı erişim; sunucuyu dışarı açan bir tünel; stdio kullanımının değişmemesi; yetkisiz isteğin reddedildiğini gösteren testler. Claude'un gereksinimleri (2026-10-28'de belgelerden doğrulandı, https://claude.com/docs/connectors/building/authentication): oturum açma `401` + `WWW-Authenticate: Bearer resource_metadata=…` ile başlar; üst verinin `resource` alanı sunucu adresiyle birebir aynı olmalı; geri dönüş adresi `https://claude.ai/api/mcp/auth_callback`, Claude Code için portu yok sayılan `http://localhost/callback` ve `http://127.0.0.1/callback`; jeton uç noktası form gövdesi kabul eder, geçersiz yenileme jetonunda `invalid_grant` döner, açık istemcilerde yenileme jetonu döndürülür (rotation); keşif, kayıt ve jeton uç noktaları 10 saniyede cevap verir; istekler Anthropic'in `160.79.104.0/21` aralığından gelir (sunucu internetten erişilebilir olmalı).
13. **İç atıf ağı:** Risale'nin kendi göndermeleri ("Yirmi Beşinci Söz'de beyan edildiği gibi", "Onuncu Söz'ün İkinci Hakikati'nde") bölüm kimliklerine çözülür; kanıt cümlesiyle, kurallarla. Model bir konuyu Bediüzzaman'ın kendi bağlantılarıyla izler. Çözülemeyen göndermeler açıkça listelenir; adres tahmin edilmez.
14. **Hadis katmanı:** Açık ve güvenilir bir hadis derleminin (aşamanın başında araştırılır, lisansı doğrulanır) eklenmesi; Risale'deki hadislerin (kaynağın işaretlediği 463 parça ve metne gömülü olanlar) Kur'ân katmanındaki gibi iskeletle eşlenmesi. Sıhhat derecesi kaynak verisinden gelir, biz hüküm vermeyiz; eşleme "tam alıntı / mânen / bulunamadı" diye ayrılır.
15. **Konu fihristi (2. hedef):** Konu → cümle listeleri. Anlamsal aramanın üzerine kurulur; konu listesi (eserlerin fihrist bölümleri ve kullanıcının listesi) ve her konunun cümleleri elle gözden geçirilebilir bir dosyada durur, sunucuya araç ya da kaynak olarak eklenir. Asıl paragraflar değişmez; konu, ardışık cümle aralıklarından ("pasaj") oluşan ayrı bir katmandır.
16. **Kontrol işaretlerinin işlenmesi:** Arayüzden dışa aktarılan `risale-kontrol-notlari.json` dosyasındaki ✓/✗ ve notlar ayrıştırıcı düzeltmelerine dönüşür. Her ✗ için kök neden bulunur, kural düzeltilir, altın örnekler gerekirse yenilenir; düzeltilemeyenler açıkça listelenir. Kullanıcının yükünü azaltmak için önce bir kontrol kuyruğu: şüpheli yerler (çok uzun cümleler, boş bölümler, düşük eşleme oranı, PDF kaynaklı eserler) otomatik listelenir.
17. **Eksik eserler:** Fihrist Risalesi (ana ciltlerin fihrist bölümlerinden bir mecmua olarak), Kızıl İcaz'ın Türkçesi (kullanıcının PDF'i bekleniyor), Hizb-i Nurî (nurpedia'da bulundu, karar bekliyor). Bkz. Kapsam ve kaynaklar.
