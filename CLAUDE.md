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
| risaleoku.com | Hizbler, Arapça Mesnevî, Küçük Sözler, (Fihrist Risalesi) | `/oku/<kitap>` okuyucu sayfası: sayfa sayısı, kitabın başladığı sayfa (`baslangic`) ve fihrist ağacı (`#treemenu1`); `/ajax/<kitap>/<n>` sayfa metni. Renkli `font` "tefekkür" boyamasıdır, başlık değildir. Arapça Mesnevî'nin ağacı boş: başlıklar ortalı "الرسالة …" satırlarından; ilk başlıktan önceki sayfalar tahkik edenin girişidir. Hizbü'l-Kur'ân'ın fihristi güvenilmez (sûre sayfası bazen bir sayfa geri, bazı sûrelerin girdisi yok): sûreler metindeki "سُورَةُ …" başlığından açılır, adı Tanzil'in sûre adlarıyla tanınır (başka adla anılanlar `quran.OTHER_SURA_NAMES`; aynı iskelete inen adlar sırayla ayrılır), girdisi olmayan sûre "77-Mürselât" diye eklenir. Sitede Hizbü'l-Kur'ân'ın bir sayfası boştur (Lokmân'ın başı); `gaps`'te işaretli. Hizbü Envâri'l-Hakāik Cevşenü'l-Kebîr'i içerir. `Crawl-delay: 10`. |
| kastamonur.com | Makalat, Nutuk | Âsâr-ı Bedîiyye baskısından "Nutuklar ve Makaleler" tek bir WordPress yazısıdır (MediaWiki'den aktarılmış): `h1` "Nutuklar" ve ortalı "Makaleler Kısmı" iki bölüm, her `h2` ("Makale – 5") bir makale, basılı adı altındaki tamamı kalın paragraf, yayın satırları alt başlık, `h3` alt bölüm. Arapça `dir="rtl"` ve Unicode sunum biçimleriyle (NFKC ile standart harfe çevrilir). Dipnotlar `<sup class="reference">`, numaraları her bölümde baştan; "(Müellif)" ya da "[Haşiye]" müellifin hâşiyesi, diğerleri nâşir notu (`notes`). Sitede Makale – 13 yok, "Makale – 16" iki kez. Site "TELİF UYARISI" taşır: izinsiz ve kaynaksız kullanılamaz. |
| tanzil.net | Kur'ân-ı Kerîm (Aşama 13) | Arapça metin üç biçimde (Medine Mushafı hattı `uthmani`, imlâî `simple`, harekesiz `simple-clean`) ve iki Diyanet meali (`tr.diyanet`, `tr.vakfi`), XML. Metin değiştirilmeden, kaynağı (Tanzil Project) ve tanzil.net bağlantısı belirtilerek kullanılır; mealler yalnızca ticari olmayan kullanım içindir. Meal dosyalarının açıklama satırları XML'de geçersiz `--` taşır; ayrıştırmadan önce atılır. robots.txt yalnızca `/res/` yolunu yasaklar. |
| Yeni Asya | (artık kullanılmıyor) | Makalat ve Nutuk'un eski kaynağı. "Eski Saîd Dönemi Eserleri" cildinin `basic-html` katmanı; Arapça okunamadığı ("[Arapça]") için kastamonur.com'a geçildi. Ham veri ve ayrıştırıcı karşılaştırma için duruyor. |

- **Ertelendi:** Fihrist Risalesi (yalnızca Osmanlıca bulundu), Rumuzat-ı Semaniye (hususi bir risale; kullanıcı kararıyla şimdilik eklenmiyor).
- **Kaynağı bulunamadı:** Kızıl İcaz, Ta'likat (ikisi de yalnızca basılı ve akademik çalışmalarda), Hizb-i Nurî (kısmen Lem'alar'da). Aşama 4'teki web aramasında da serbest bir metin bulunamadı.
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
- PDF kodu ve PyMuPDF Aşama 2'deki karşılaştırmadan sonra kaldırıldı (git geçmişinde `da37ba2`).

## Klasör yapısı

```
risale-mcp/
├── CLAUDE.md
├── data/
│   ├── vectors/                   # Anlamsal arama vektörleri <model>.<seçenek>.npy + .keys.json (git'e eklenmez)
│   ├── raw/                       # Ham kaynak yanıtları (git'e eklenmez)
│   │   ├── erisale/               # sitemap-tr.xml, <kitap>/manifest.json, pages/<bölüm>.html.gz
│   │   ├── risale_online/         # eserler.json, <kitap>/fihrist.json, paragraf/<ilk>-<son>.json
│   │   ├── risaleoku/             # <kitap>/index.html.gz, pages/<n>.html.gz
│   │   ├── yeniasya/              # <kitap>/toc.html.gz, pages/<n>.html.gz (artık kullanılmıyor)
│   │   ├── kastamonur/            # <yazı>/manifest.json, page.html.gz
│   │   ├── tanzil/                # manifest.json, quran-<biçim>.xml, tr.diyanet.xml, tr.vakfi.xml
│   │   └── logs/                  # toplu indirme günlükleri
│   ├── interim/                   # Ara çıktılar
│   │   ├── erisale/<kitap>.blocks.json   # birleştirilmiş, doğrulanmış bloklar (git'e eklenmez)
│   │   ├── review/index.html      # kontrol arayüzü: bütün eserler tek sayfada; metinler review/data/<eser>.js (git'e eklenmez)
│   │   ├── outline/<eser>.txt     # elle kontrol için girintili başlık ağacı (git'e eklenmez)
│   │   ├── quran/ayah_check.md    # âyet denetimi: kaynağın numarası Kur'ân metniyle tutmayan yerler
│   │   ├── ayah_links/            # links.md (bütün âyet ilişkileri), sample-<tur>.md (gözden geçirme örneklemi)
│   │   └── build.log              # son toplu ayrıştırmanın raporu
│   ├── books/<eser>.json          # Her eserin JSON'u (git'e eklenmez)
│   ├── quran.json                 # Kur'ân katmanı: metin, mealler, sûre adları (git'e eklenmez)
│   └── risale.db                  # SQLite veritabanı (git'e eklenmez)
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
│   │   └── mecmua.py         # Mecmuaların (ve ikincil kaynaktaki eserlerin) ana ciltlere eşlenmesi
│   ├── sources/
│   │   ├── http.py           # Nazik HTTP istemcisi
│   │   ├── archive.py        # Ham yanıtı diske yazma, önbellekten okuma
│   │   ├── erisale.py        # erisale: sitemap, ham arşiv, blok çıkarma, birleştirme, doğrulama
│   │   ├── risale_online.py  # risale.online JSON API (yalnızca ham kayıt + doğrulama)
│   │   ├── risaleoku.py      # risaleoku sayfaları (yalnızca ham kayıt + doğrulama)
│   │   ├── yeniasya.py       # Yeni Asya basic-html sayfaları (artık kullanılmıyor)
│   │   ├── kastamonur.py     # kastamonur.com yazısı (yalnızca ham kayıt + doğrulama)
│   │   └── tanzil.py         # tanzil.net Kur'ân metni ve mealleri (yalnızca ham kayıt + doğrulama)
│   ├── normalize.py    # Türkçe metin normalizasyonu, sıra sayıları, slug
│   ├── review_ui.py    # Kontrol arayüzü: kitap JSON'ları → review/index.html + data/<eser>.js
│   ├── review_assets/  # Arayüzün template.html, style.css, app.js dosyaları
│   ├── db.py           # Aşama 5: veritabanı şeması ve salt okunur bağlantı
│   ├── build_db.py     # Aşama 5: JSON → SQLite CLI'ı (sûre/âyet çözümü, doğrulama)
│   ├── search.py       # Aşama 5: sorgu dili → FTS5, cümle ve başlık araması
│   ├── library.py      # Aşama 6: veritabanı üzerindeki okuma işleri (MCP'den bağımsız)
│   ├── quran.py        # Aşama 13: Kur'ân katmanı (ham -> data/quran.json), harf iskeleti, âyet eşleme
│   ├── ayah_links.py   # Aşama 14: âyet ilişkileri (kurallar, gözden geçirme raporu ve örneklem)
│   ├── citations.py    # Atıf denetimi: metindeki "Eser › Bölüm › “ilk kelimeler”" atıfları (araç ve altın sorular)
│   ├── env.py          # .env dosyasındaki API anahtarları
│   ├── embeddings.py   # Aşama 8: vektör sağlayıcıları (Voyage, OpenAI), vektör deposu, vektör çıkarma CLI'ı
│   ├── semantic.py     # Aşama 8: sunucunun anlamsal araması (en yakın cümleler, bölüm sıralaması)
│   ├── search_eval.py  # Aşama 8: arama değerlendirmesi (hit@k, MRR) ve model karşılaştırması
│   ├── server.py       # Aşama 6: MCP sunucusu (araçlar, kaynaklar, hazır komutlar)
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
    └── golden/
        ├── golden_questions.md   # kullanıcının yazdığı test soruları
        ├── questions.json        # aynı sorular, doğrulanmış beklenen bölümlerle (düzenek bunu okur)
        ├── ayah_links_review.json  # kullanıcının âyet ilişkisi örneklem kararları (Aşama 14)
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
- **Hâşiye cümleleri** kendi içinde numaralanır: `… › 32. cümle › Hâşiye › 2. cümle`. Bir cümlede birden çok hâşiye varsa `Hâşiye 1`, `Hâşiye 2`.
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

## Kur'ân katmanı (Aşama 13)

Kur'ân-ı Kerîm Risale eserlerinden ayrı bir katmandır; atıf birimi âyettir ("Bakara Sûresi, 2:255", `›` olmadan; `verify_citations` bu atıfları denetlemez, doğruluğu `get_ayah`'tan gelir). Ayrıntı `quran.py` başındaki açıklamadadır.

```
uv run python -m risale_mcp.fetch quran   # tanzil.net'ten ham veri (bir kez, 5 dosya)
uv run python -m risale_mcp.quran         # data/raw/tanzil -> data/quran.json
uv run python -m risale_mcp.build_db      # Kur'ân tabloları, âyet denetimi ve eşleme; rapor data/interim/quran/ayah_check.md
```

- **Metin:** kullanıcıya her zaman harekeli Medine Mushafı hattı (`quran_ayahs.text`) gösterilir (kullanıcının isteği: harekesiz okuyamıyor). İmlâî harekeli metin `text_simple`, harekesiz metin yalnızca eşlemede.
- **Mealler:** Diyanet İşleri Başkanlığı ve Türkiye Diyanet Vakfı (Tanzil'den). Diyanet İşleri meali 570 yerde art arda âyetleri (toplam 1.413 âyet, en çok 12) birlikte tercüme eder; Tanzil aynı metni her âyete yazar. Bunlar `first_ayah`..`last_ayah` ile işaretlidir, araç `covers_verses` der. Üç meal türü karıştırılmaz: müellifin "Yani" izahı (metin), nâşirin meali (`publisher_translation`), Diyanet mealleri (`get_ayah`).
- **Sûre adları:** Türkçe 114 ad `quran.SURA_NAMES`'tedir (Tanzil yalnızca Arapça adı verir); veride hiç geçmeyen sûreler de adıyla aranır.
- **Harf iskeleti (`quran.skeleton`):** Risale'nin imlâsı (Türk mushafı, "﷽", "…الخ") Tanzil'inkinden farklıdır. İki metin de iskelete indirilir: hareke ve işaretler, hemze, elif, vav, ye atılır; elif çeşitleri, tâ-i merbûta (ة = ت), Farsça harfler birleştirilir. Alıntı "…" ve "الخ" yerlerinden parçalara bölünür; her parça Osmanî ya da imlâî iskelette aranır.
- **Kaynağın âyetleri denetlenir** (`arabic.ayah_check`): 4.000 âyetin 3.950'si numarasıyla tutar (`exact`), 8'i komşu âyette (`near`), 30'u kelimesi kelimesine tutmaz (`differs`: iktibas, tekrarlanan ifade, birden çok kaynak, Zülfikâr'da âyet diye işaretlenmiş şerh), 12'si boş. Veri değiştirilmez; `find_ayah` sonucunda `check` uyarısı gider. Liste `data/interim/quran/ayah_check.md`'de.
- **İşaretsiz âyetler bulunur** (`ayah_quotes`): Hizb paragrafları numarayı mushaftaki gibi sonda verir ("…﴿٢﴾"); her numaradan önceki metin o numaralı âyetle biten yerde aranır. Kısa ve birden çok sûrede geçen âyet ("الٓمٓ﴿١﴾"), bölümde bulunan öbür âyetlerin en az %80'i aynı sûredense o sûrede aranır. el-Mesnevî el-Arabî'nin "﴿ … ﴾" alıntısı yalnızca Kur'ân'da tek yerde geçiyorsa (iskelette en az 6 harf) bağlanır. 2.373 alıntı bulundu (Hizbü'l-Kur'ân 1.848, Hizbü Envâr 266, el-Mesnevî el-Arabî 259); 161'i bağlanamadı (Hizbü Envâr'daki ﴿n﴾ sayaçları, dua içindeki iktibaslar, birden çok âyette geçen kısa ifadeler).
- **Hizbü'l-Kur'ân'ın sûre sınırları** artık fihristten değil metindeki Arapça başlıklardan gelir (bkz. risaleoku satırı); 1.850 âyetin hepsi kendi sûresinin altındadır.

## Âyet ilişkileri (Aşama 14)

Risale'nin bir yerinin bir âyetle kurduğu bağ (`ayah_links` tablosu). `build_db` Kur'ân katmanını kurduktan sonra kurallarla çıkarır; ayrıntı `ayah_links.py` başındadır. Bu bağlar **"tefsir" diye anılmaz** (kullanıcının kararı): bir yerin bir âyetin tefsiri olduğu bir hükümdür, kural ise yalnızca metnin âyetle kurduğu bağı bulur; yanlışlıkla tefsir sınıfına alınan bir yan cümle vebal olur.

```
uv run python -m risale_mcp.ayah_links    # data/interim/ayah_links/links.md (hepsi) ve sample-<tur>.md (40'lık örneklem)
```

- **Türler:** `isaret` (âyetin geçtiği cümlede "işâret, remz, nükte, tefsir, mânâ, meâl"), `acilis` (bölümün ilk paragrafı âyet; Besmele sayılmaz), `izah` (âyetin hemen ardından ya da sonraki cümlenin başında müellifin "Yani"si; aslı Arapça eserlerde Türkçe ifade mütercimindir), `dayanak` ("… sırrınca, sırrıyla, fermânıyla"), `risale` (âyetin Risale-i Nur'a işâreti: Şualar › Birinci Şuâ ve başlığında "Risale-i Nur'a işâret" geçen bölümler; ayrı tür, kullanıcının kararı).
- **Kapsam ve güç:** bağ bölümün ilk iki cümlesindeyse ve açılışta bölümün tamamı (`section`), değilse kanıt cümlesi (`sentence`). Bölüm kapsamlılar ve `izah` güçlü, öbürleri zayıf: zayıf ilişki yalnızca bir cümlenin âyete atfıdır, bölümün konusu gibi sunulmaz (kullanıcının "zayıf ilişki" fikri).
- **İlk gözden geçirmeden çıkan kurallar** (kullanıcı, 1. tur): "işâret" gibi kelime âyete en çok 8 Türkçe kelime uzakta olmalı, âyet cümlenin başında değilse (önünde en çok 3 kelime: "İkinci Cümle: …") uzaktaki kelime bağ kurmaz; sûreyi adlandıran âyet ("Sûre‑i وَالتّ۪ينِ", "اِقْرَأْ … Sûresi") zayıf; cifir/ebced cümlesi, âyet başta değilse zayıf; "İşârât-ı Kur'âniye", "İşârâtü'l-İ'câz" risale adı, kanıt değil; mektup eserlerinde yalnız "وَاِنْ مِنْ شَيْءٍ اِلَّا يُسَبِّحُ بِحَمْدِه۪" ile açılış bir açılış ibaresidir, `acilis` değil (Sözler'in Pencereleri öyle değil).
- **Kararlar kilitli:** kullanıcının örneklem kararları `tests/golden/ayah_links_review.json`'da; gerçek veritabanında hepsinin tuttuğu test edilir, yeni örneklem bunları dışarıda bırakır. Kaynakta âyet ile önündeki Arapça ayrı işaretlidir ("فَاسْتَمِعْ اٰيَةَ" `arabi`); tabloda âyetin eserdeki metni ayrı sütundur.
- **Bilinen sorun:** İşaratü'l-İ'caz'da 15 bölümün başlığı aynıdır ("Âyetin Tefsiri"); atıf yolu bölümü ayırmaz (kimlikler `-2`, `-3`).
- **Kapsam dışı:** Hizbler (Kur'ân metninin kendisi), mecmualar (metni ana ciltlerde), Fihrist bölümleri (özet).
- **Sayılar** (2026-10-27, 1. tur düzeltmelerinden sonra): 883 ilişki, 255'i güçlü: `isaret` 86 güçlü / 437 zayıf, `acilis` 76, `izah` 55, `dayanak` 17 / 136, `risale` 21 / 55. 1. turda kullanıcının baktığı 22 güçlü ilişkiden 17'si doğru, 5'i yanlıştı; düzeltmeden sonra 22'si de kararıyla uyumlu. 2. turda (düzeltilmiş kurallarla, yeni 40'lık örneklem) 40'ın 40'ı doğru; 62 karar kilitli. Kullanıcının örneği (Lem'alar › Otuzuncu Lem'a › Altıncı Nükte › İkinci Şuâ › Birinci Mes'ele: Bakara 2:255, Hûd 11:56, Zümer 39:63) bölüm kapsamlı `isaret`'tir.
- **Gözden geçirme:** güçlüler doğrudan kabul edilir; kullanıcı her turda 40'lık örneklemi (`sample-<tur>.md`) kontrol eder, bulduğu hatalar kurallara ve karar dosyasına döner. Zayıflar tek tek gözden geçirilmez.
- **Araçlar:** `find_ayah` tek âyette `links` (güçlüler önce, kanıt cümlesiyle), `get_ayah` `linked_in_works`, `read_section` başlıkta `linked_verses`. Talimat: ilişkiyi türüyle ve kanıtıyla an, "tefsir" deme; ilişkili âyetleri her alıntının ardına ekleme, kullanıcı sorarsa ya da âyet soruyla ilgiliyse ver (kullanıcının isteği).

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
uv run risale-mcp --transport streamable-http           # yerel HTTP 127.0.0.1:8000/mcp (kimlik doğrulamasız)
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
| `verify_citations(text)` | Taslak cevaptaki atıfları denetler: bölüm var mı, alıntı bir cümlenin başı mı, aralık 8 cümleyi ve bölümü aşıyor mu, yanındaki alıntı bloğu atfın cümlelerinde mi; sorunlu atfa tam atıf ya da alıntının asıl yeri önerilir |

### Atıf denetimi (`citations.py`)
Ayrıntı modülün başındaki açıklamadadır. `verify_citations` aracı ve altın soru raporu aynı denetimi kullanır.
- Satır `›` işaretlerinden bölünür; bir satırda birden çok atıf, atıftan önce ve sonra düz yazı olabilir. Atıf alıntıyla ya da "32. cümle" ile biter.
- Başlık basılı adla, içindekiler adıyla, tür ve numarayla ("İkinci Makam" = "Yirminci Söz’ün İkinci Makamı"), ekli ("Dördüncü Söz'de"), "(asm)" gibi ayraçsız ya da "…" ile kısaltılmış yazılabilir; ara başlıklar atlanabilir. Bunlar geçerlidir ama tam yolu yazılmamış sayılır (`exact`), araç tam atfı verir.
- "…", "aynı yer", "(› …" ve eser adı yazılmamış yol bir önceki atfa göre çözülür. Yol birden çok bölüme uyarsa önce alıntının geçtiği, sonra önceki atfa yakın, ana ciltteki ve üst seviyedeki bölüm seçilir.
- Ardışık cümleler: "“…” ile başlayan N cümle" ya da "› 4.–7. cümle". Aralık bulunan cümleden başlar, aynı bölümün ana metninde (hâşiyede aynı hâşiyede) sürer; 8'i aşarsa `range_too_long`, bölümü aşarsa `range_past_section`.
- Alıntı bloğu: atfın hemen önündeki ya da ardındaki `> "…"` bloğu (araya yalnızca boş satır girebilir) atfın kapsadığı cümlelerde aranır; "…" ile atlanan yer serbesttir. İki atıf arasındaki blok uyduğu atfa bağlanır. Uymazsa `block_ok` yanlıştır.
- Sonuçlar: `ok`, `section`, `mid_sentence`, `quote_not_found` (alıntının asıl yeri `elsewhere`), `no_such_sentence`, `unknown_section`, `ambiguous`, `range_too_long`, `range_past_section`.

- **Kaynaklar** (kullanıcının sohbete eklediği bağlam): `risale://works`, `risale://outline/{work}`, `risale://text/{+section}` (ör. `risale://text/sozler/10`; numaralı cümlelerle Markdown).
- **Hazır komutlar** (İngilizce adlar): `topic_survey(topic, scope?)` konunun eserlerde geçtiği yerler (2. hedef), `text_and_commentary(question)` "metin ne diyor" ve "yorum" ayrı (3. hedef), `discuss(topic)` müzakere, `self_test(section)` bölümden soru sorup cevabı metinle denetler, `lesson_plan(subject)` atıflı ders planı.
- **Sunucu talimatları:** atıfı araç sonucundan al ve uydurma; kullanıcıya cümleyi numarasıyla değil yol + incipit ile göster; yolu eserden başlayarak tam ve kısaltmadan yaz, önceki atfa göre göreli yazma, `›` işaretini yalnızca atıfta kullan; tırnağı yalnızca metnin kendi sözlerine koy; aynı bölümde birkaç cümle süren temsil, misal ya da düşünceyi tek blokta ve "… ile başlayan N cümle" atfıyla ver (en çok 8 cümle, hâşiye ayrı); her alıntıyı (kısa olanlar ve öncekini genişletenler de) düz yazının içinde değil, kendi satırında tırnak içinde alıntı bloğu (`> "…"`) olarak ver, düz yazıda en çok tek bir terim tırnağa alınır (kullanıcının isteği); cevaptan önce atıfları `verify_citations` ile denetle; âyetin Arapçasını yalnızca harekeli ve `get_ayah`'tan (ya da eserin alıntıladığı gibi) ver, ezberden yazma, atfı "Bakara Sûresi, 2:255" biçiminde `›` olmadan yaz, Diyanet mealini adıyla an, birlikte tercüme edilen âyetleri söyle, hiçbir mealin Kur'ân'ın yerini tutmadığını hatırla; âyet ilişkilerini asla "tefsir" diye anma, türüyle ve kanıt cümlesiyle ver, zayıf ilişkiyi bölümün konusu gibi sunma, ilişkili âyetleri her alıntının ardına ekleme (sorulursa ya da konuyla ilgiliyse ver); âyet ve hadis mealleri nâşirindir, müellife mal etme ve metin diye alıntılama, müellifin "Yani, …" izahı metindir; bulamazsan söyle; metni ve yorumu ayır; önce ara, sonra bağlamı oku.

Sonraki aşamalar için bkz. "Aşamalar" (8–14).

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

Tamamlananlar (PDF dönemi): PDF inceleme, Sözler'in PDF'ten ayrıştırılması ve kontrol arayüzü. Aşama 1–7 tamamlandı (cümle ve eşleme kontrolü kullanım sırasında sürecek). Ardından atıf denetimi (`citations.py`, `verify_citations`) eklendi.

1. **İndirici:** Katalog, nazik istemci, dört sitenin indiricisi ve bütünlük doğrulaması. Önce Sözler pilotu, ardından bütün eserler toplu indirildi:
   `uv run python -m risale_mcp.fetch get --all --site <site>` (her site ayrı süreçte; günlükler `data/raw/logs/`).
2. **Ayrıştırıcı:** erisale blokları → `data/books/<eser>.json` (başlık ağacı, paragraflar, hâşiyeler): `uv run python -m risale_mcp.build --all`. erisale'deki 27 eser ayrıştırıldı; Sözler PDF çıktısıyla karşılaştırıldı, PDF kodu silindi.
3. **Cümleler:** Cümle bölücü (`sentences.py`, `build` içinde çalışır) ve altın örnek testleri; kontrol arayüzüne kitap seçici, cümle numaraları ve cümle düzeyinde işaretler eklendi. Kullanıcı Sözler'i kontrol eder.
4. **Diğer eserler:** risale.online, risaleoku ve kastamonur.com (önce Yeni Asya) ayrıştırıcıları; mecmuaların ana ciltlere eşlenmesi; bulunamayan eserler için kaynak araması. 38/43 eser ayrıştırıldı (`ESERLER.md`).
5. **Veritabanı:** SQLite ve FTS5 kurulumu, normalizasyon, sorgu dili, âyet dizini, birim testler: `uv run python -m risale_mcp.build_db`.
6. **MCP sunucusu:** `library.py` + `server.py`; araçlar, kaynaklar, hazır komutlar; süreç içi istemciyle testler. MCP Inspector ile elle deneme.
7. **Uçtan uca test:** `golden.py` ile Claude Code'u istemci yaparak (Linux'ta Claude Desktop yok) `tests/golden/` sorularıyla dene, adreslerin doğruluğunu elle kontrol et.

Sonraki aşamalar (sıra kullanıcıyla birlikte belirlenir):

8. **Anlamsal arama:** A: değerlendirme seti (50 soru, kullanıcı onayladı); B: yerel/API modellerin karşılaştırması (kullanıcı API'yi tercih etti; `voyage-context-4` seçildi); C: `semantic_search` aracı, bölüm sıralaması, 512 boyut int8 depo. Bkz. Anlamsal arama.
9. **Konu fihristi (2. hedef):** Konu → cümle listeleri. Anlamsal aramanın üzerine kurulur; konu listesi ve her konunun cümleleri elle gözden geçirilebilir bir dosyada durur, sunucuya araç ya da kaynak olarak eklenir.
10. **Kontrol işaretlerinin işlenmesi:** Arayüzden dışa aktarılan `risale-kontrol-notlari.json` dosyasındaki ✓/✗ ve notlar ayrıştırıcı düzeltmelerine dönüşür. Her ✗ için kök neden bulunur, kural düzeltilir, altın örnekler gerekirse yenilenir; düzeltilemeyenler açıkça listelenir.
11. **Eksik eserler:** Fihrist Risalesi, Rumuzat-ı Semaniye, Kızıl İcaz, Ta'likat, Hizb-i Nurî. Kaynak bulunmasına bağlıdır (bkz. Kapsam ve kaynaklar).
12. **Sunucu kimlik doğrulaması ve uzaktan erişim** (2026-10-27'de kullanıcı kararıyla ertelendi; kişisel kullanım için yerelde Claude Code yeterli, ortak derlemlerde yeniden gündeme gelir): Amaç sunucuyu claude.ai'den (tarayıcı ve telefon) özel bağlayıcı olarak kullanmak. Bugün `streamable-http` kimlik doğrulamasızdır ve yalnızca `127.0.0.1`'de dinler; bu hâliyle dışarı açılmaz, çünkü metinler herkese açılmış olur (kaynak sitelerin telif uyarısı, kullanım kişiseldir). Yapılacaklar: MCP'nin yetkilendirme yöntemi (OAuth 2.1) ile tek kullanıcılı erişim, sunucuyu dışarı açan bir tünel (Cloudflare Tunnel, Tailscale Funnel gibi), stdio kullanımının değişmemesi, yetkisiz isteğin reddedildiğini gösteren testler. claude.ai bağlayıcılarının ve SDK'nın güncel gereksinimleri aşamanın başında belgelerden doğrulanır; tahminle yazılmaz.
13. **Kur'ân katmanı:** Tanzil'den metin ve iki Diyanet meali, `get_ayah` aracı, kaynağın âyetlerinin denetimi ve işaretsiz âyetlerin bulunması. Bkz. Kur'ân katmanı.
14. **Âyet ilişkileri:** Risale'nin hangi yerinin hangi âyetle bağ kurduğu; kurallarla, kanıt cümlesiyle. "Tefsir" denmez (kullanıcının kararı: kuralla bulunan bağ bir hüküm değildir). Kullanıcı güçlü ilişkilerden 40'lık örneklemi gözden geçirir. Bkz. Âyet ilişkileri.
