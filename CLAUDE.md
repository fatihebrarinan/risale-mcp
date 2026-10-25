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
- **Sayfa numarası yoktur.** Hiçbir veri dosyasında basılı sayfa bilgisi tutulmaz.
- **Metin tek yerde durur.** Mecmualar (Asâ-yı Mûsâ, Zülfikâr…) ana ciltlerdeki metne işaret eden içindekiler listeleridir; yalnızca mecmuaya özgü parçalar mecmuada saklanır.
- **Kaynak web'dir.** Ham yanıtlar bir kez indirilip diske kaydedilir; ayrıştırma her zaman diskten yapılır.

## Kapsam ve kaynaklar

Eserlerin listesi, her birinin kaynağı ve durumu tek yerde tutulur: `src/risale_mcp/catalog.py`. Her eserin hangi aşamada olduğu `ESERLER.md` kontrol listesindedir (`uv run python -m risale_mcp.checklist` ile diskten üretilir, elle düzenlenmez).

| Site | Rol | Notlar |
|---|---|---|
| **erisale.com** | Birincil kaynak (≈30 eser) | Standart baskı. Her bölüm ayrı sayfa; sayfa listesi `sitemap-tr.xml`'den. Metin sayfaya gömülü RSC verisinde yapısal ağaç olarak gelir: blok türleri (`H2`, `H3`, `Paragraph`, `CenteredParagraph`, `HeadingDescription`…), satır içi başlıklar (`Heading`), Arapça (`RTL`, türü âyet/hadis/Arapça, meali `rtl.txn`), hâşiye tam geçtiği yerde (`FootnoteRef` → `Footnote`). `blockIndex` kitap içinde süreklidir; boşluk = eksik bölüm. robots.txt yalnızca `/api/` yolunu yasaklar; biz yalnızca okuma sayfalarını indiririz. |
| risale.online | Zülfikâr, Tılsımlar, Sirâcü'n-Nûr, Gençlik ve Hanımlar Rehberi (mecmualar) | Hayrat baskısı, JSON API (`/risale-api/fihrist`, `/risale-api/paragraf`). Yapı fihristten (sayfa numaralı, iç içe); paragraf HTML'i kelime gruplarıdır, Arapça meali ve kaynağıyla (`data-mehaz-*`), hâşiye `<aside>`. |
| risaleoku.com | Hizbler, Arapça Mesnevî, Küçük Sözler, (Fihrist Risalesi) | `/oku/<kitap>` okuyucu sayfası: sayfa sayısı, kitabın başladığı sayfa (`baslangic`) ve fihrist ağacı (`#treemenu1`); `/ajax/<kitap>/<n>` sayfa metni. Renkli `font` "tefekkür" boyamasıdır, başlık değildir. Arapça Mesnevî'nin ağacı boş: başlıklar ortalı "الرسالة …" satırlarından; ilk başlıktan önceki sayfalar tahkik edenin girişidir. Hizbü Envâri'l-Hakāik Cevşenü'l-Kebîr'i içerir. `Crawl-delay: 10`. |
| kastamonur.com | Makalat, Nutuk | Âsâr-ı Bedîiyye baskısından "Nutuklar ve Makaleler" tek bir WordPress yazısıdır (MediaWiki'den aktarılmış): `h1` "Nutuklar" ve ortalı "Makaleler Kısmı" iki bölüm, her `h2` ("Makale – 5") bir makale, basılı adı altındaki tamamı kalın paragraf, yayın satırları alt başlık, `h3` alt bölüm. Arapça `dir="rtl"` ve Unicode sunum biçimleriyle (NFKC ile standart harfe çevrilir). Dipnotlar `<sup class="reference">`, numaraları her bölümde baştan; "(Müellif)" ya da "[Haşiye]" müellifin hâşiyesi, diğerleri nâşir notu (`notes`). Sitede Makale – 13 yok, "Makale – 16" iki kez. Site "TELİF UYARISI" taşır: izinsiz ve kaynaksız kullanılamaz. |
| Yeni Asya | (artık kullanılmıyor) | Makalat ve Nutuk'un eski kaynağı. "Eski Saîd Dönemi Eserleri" cildinin `basic-html` katmanı; Arapça okunamadığı ("[Arapça]") için kastamonur.com'a geçildi. Ham veri ve ayrıştırıcı karşılaştırma için duruyor. |

- **Ertelendi:** Fihrist Risalesi (yalnızca Osmanlıca bulundu), Rumuzat-ı Semaniye (hususi bir risale; kullanıcı kararıyla şimdilik eklenmiyor).
- **Kaynağı bulunamadı:** Kızıl İcaz, Ta'likat (ikisi de yalnızca basılı ve akademik çalışmalarda), Hizb-i Nurî (kısmen Lem'alar'da). Aşama 4'teki web aramasında da serbest bir metin bulunamadı.
- **Doğrulandı:** el-Mesnevî el-Arabî (İhsan Kasım es-Sâlihî tahkiki), Hizbü Envâri'l-Hakāik (Cevşenü'l-Kebîr'i içerir).
- **Sitede eksik:** Sikke-i Tasdik-i Gaybî'de aynı başlıklı iki bölüm aynı adresi paylaştığından 15 blok indirilemiyor; `gaps` alanında işaretli. Mecmua eşlemesinde (Aşama 4) ana ciltlerden tamamlanacak.
- Bir kaynak kitabı birden çok esere bölünebilir: erisale'nin "İlk Dönem Eserleri" kitabı Divan-ı Harb-i Örfî, Münazarat, Sünuhat vb. eserlere ayrılır. Lemeat (Sözler'in sonu) ve Hakikat Çekirdekleri (Mektubat'ın sonu) ayrı eserdir. Seçim, katalogdaki bölüm slug önekleriyle yapılır.

Kullanım kişiseldir. Uygulama olarak yayımlanırsa kaynak sitelerden izin alınacak. Ham ve ara veri git'e eklenmez.

## Teknik tercihler

- Dil: Python 3.11+
- Ortam ve bağımlılıklar: `uv`
- HTTP: standart kütüphane (`urllib`), `sources/http.py` içindeki nazik istemci (istekler arası bekleme, yeniden deneme). Varsayılan bekleme 5 sn; risaleoku için 10 sn.
- Veritabanı: SQLite + FTS5 (kelime araması). Anlamsal arama ilk sürümde **yok**; şema ona hazırdır (bkz. Veritabanı).
- MCP: resmi Python SDK'sı (`mcp` paketi, FastMCP). Not: `@modelcontextprotocol/sdk` TypeScript paketidir, kullanmıyoruz.
- Test: `pytest` + MCP Inspector + Claude Code'a `claude mcp add` ile bağlayarak elle deneme.
- Platform: Linux Mint.
- PDF kodu ve PyMuPDF Aşama 2'deki karşılaştırmadan sonra kaldırıldı (git geçmişinde `da37ba2`).

## Klasör yapısı

```
risale-mcp/
├── CLAUDE.md
├── data/
│   ├── raw/                       # Ham kaynak yanıtları (git'e eklenmez)
│   │   ├── erisale/               # sitemap-tr.xml, <kitap>/manifest.json, pages/<bölüm>.html.gz
│   │   ├── risale_online/         # eserler.json, <kitap>/fihrist.json, paragraf/<ilk>-<son>.json
│   │   ├── risaleoku/             # <kitap>/index.html.gz, pages/<n>.html.gz
│   │   ├── yeniasya/              # <kitap>/toc.html.gz, pages/<n>.html.gz (artık kullanılmıyor)
│   │   ├── kastamonur/            # <yazı>/manifest.json, page.html.gz
│   │   └── logs/                  # toplu indirme günlükleri
│   ├── interim/                   # Ara çıktılar
│   │   ├── erisale/<kitap>.blocks.json   # birleştirilmiş, doğrulanmış bloklar (git'e eklenmez)
│   │   ├── review/index.html      # kontrol arayüzü: bütün eserler tek sayfada; metinler review/data/<eser>.js (git'e eklenmez)
│   │   ├── outline/<eser>.txt     # elle kontrol için girintili başlık ağacı (git'e eklenmez)
│   │   └── build.log              # son toplu ayrıştırmanın raporu
│   ├── books/<eser>.json          # Her eserin JSON'u (git'e eklenmez)
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
│   │   └── kastamonur.py     # kastamonur.com yazısı (yalnızca ham kayıt + doğrulama)
│   ├── normalize.py    # Türkçe metin normalizasyonu, sıra sayıları, slug
│   ├── review_ui.py    # Kontrol arayüzü: kitap JSON'ları → review/index.html + data/<eser>.js
│   ├── review_assets/  # Arayüzün template.html, style.css, app.js dosyaları
│   ├── db.py           # Aşama 5: veritabanı şeması ve salt okunur bağlantı
│   ├── build_db.py     # Aşama 5: JSON → SQLite CLI'ı (sûre/âyet çözümü, doğrulama)
│   ├── search.py       # Aşama 5: sorgu dili → FTS5, cümle ve başlık araması
│   └── server.py       # Aşama 6: MCP sunucusu
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
    ├── test_build_db.py
    └── golden_questions.md   # Kullanıcının yazdığı test soruları
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
- **`gaps`**: kaynakta bulunamayan bloklar `{node_id, missing_blocks, after}`. Metin uydurulmaz.
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
- erisale'nin Arapça metindeki köşeli numaraları ("[4]فَهَذَا…") Arapça asıl ile hâşiyedeki tercümesini eşleştirir; metinde kalır.

## Veritabanı (Aşama 5)

`uv run python -m risale_mcp.build_db` komutu `data/books/*.json` dosyalarından `data/risale.db`'yi her seferinde sıfırdan kurar (≈17 sn). Asıl kaynak JSON'lardır, veritabanı elle düzenlenmez. Kurulum geçici dosyaya yapılır, sayılar JSON'larla tutmazsa veritabanı yazılmaz. Şemanın açıklaması `db.py`'de, kurulum kuralları `build_db.py`'nin başındadır.

- **Tablolar:** `works` (katalogdaki bütün eserler; JSON'u olmayanlar `built = 0`), `nodes` (`ord`..`last_ord` alt ağaçtır), `node_sources`, `paragraphs` (eşlenmiş mecmua paragrafında `text` NULL), `paragraph_sources`, `sentences`, `arabic` (cümleye bağlı; âyette `sura`, `ayah_start`, `ayah_end`), `sura_names`, `notes`, `gaps`, `meta`. Arama dizinleri `sentences_fts` ve `nodes_fts` (başlık, alt başlık, içindekiler adı).
- **Kimlikler:** `id` JSON'daki kalıcı kimliktir; `seq` yalnızca bu veritabanında geçerli tamsayı anahtardır ve okuma sırasını verir.
- **Normalizasyon:** Dizin ve sorgu `normalize.search_words` biçimindedir. Şapka, çengel (ş/s, ç/c, ğ/g, ö/o, ü/u), Arapça hareke, kesme ve tatvil yok sayılır; ayrıca **ı = i** sayılır (klavyesiz "isik" → "ışık"). Biçim değişirse `db.NORMALIZATION` artırılır.
- **Sorgu dili** (`search.py`): kelimeler (hepsi geçmeli), `"tam ifade"`, `haşr*` (kelime başı), `OR`, `-kelime` / `NOT`, `NEAR(a b, 5)`. Sıralama BM25'tir; kısa cümleler öne çıkma eğilimindedir.
- **Mecmualar:** Ana cilde eşlenen paragrafların cümlesi yoktur. Bu yüzden aynı cümle aramada iki kez çıkmaz.
- **Âyetler:** İki biçim çözülür: "Bakara Sûresi, 2:255" ve Hayrat'ın "Sûre-i Bakara, 255" biçimi. Sûre adlarının numaraları, veride numarasıyla geçen yazılışlardan öğrenilir. Birden çok âyet sayılmışsa ilk aralık alınır. 4.001 âyetin hepsi çözüldü.
- **Anlamsal aramaya hazırlık:** Vektörler ayrı bir dosyada `(model, sentences.hash)` anahtarıyla tutulacak. Böylece veritabanı yeniden kurulsa da kaybolmaz; cümle metni değişmedikçe geçerli kalır. Sonuçlar `sentences.hash` üzerinden birleşir ve kelime aramasıyla aynı `search.Hit` biçiminde döner. Birleştirme RRF gibi sıraya dayalı olacak, çünkü puanlar yalnızca kendi araması içinde karşılaştırılabilir.

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

## MCP araçları (ilk sürüm)

1. **`list_books()`**: eserleri ve gruplarını döndürür.
2. **`get_outline(book: str, depth: int = 2)`**: eserin başlık ağacını döndürür.
3. **`get_passage(id: str, context: int = 0)`**: bir cümleyi ya da cümle aralığını `ref` ve `incipit` ile döndürür. `context > 0` ise komşu cümleleri de ekler. Hâşiyeleri de içerir.
4. **`search(query: str, book: str | None = None, limit: int = 20)`**: cümle düzeyinde FTS5/BM25 araması. Her sonuçta `id`, `ref`, `incipit` ve kısa önizleme döner.
5. **`find_sentence(node: str, incipit: str)`**: kullanıcının alıntıladığı ilk kelimelerden cümleyi bulur.

Sonraki aşamalar: `find_topic` (etiket tabanlı konu fihristi), anlamsal arama, atıf doğrulama.

### Sunucu talimatları (`instructions` alanı)
Sunucu, istemci modele şu kuralları iletmeli:
- Eserlere ait her iddiayı araç sonuçlarındaki `ref` ile göster. Adres uydurma.
- Kullanıcıya cümleyi numarasıyla değil, `incipit` ile göster.
- Araç sonuçlarında bulunmayan bilgiyi eserlere atfetme. Bulamazsan bunu açıkça söyle.
- Metnin söylediği ile senin yorumunu ayrı başlıklar altında ver.

## Çalışma kuralları

- Aşamaları sırayla yap. Her aşamanın sonunda **dur**, bulguları özetle ve onay bekle.
- Ayrıştırma kurallarını tahmine dayanarak yazma. Önce kaynağın ham verisini incele, örnekleri göster.
- Her aşamada kullanıcının elle doğrulayabileceği bir çıktı üret (örnek JSON, başlık ağacı, sayım tablosu).
- Belirsiz durumlarda en makul varsayımı yap, ama bunu açıkça belirt.
- Kaynak sitelere nazik davran: isteklerin arasında bekle, ham yanıtı kaydet, aynı sayfayı ikinci kez indirme.
- Kod tanımlayıcıları İngilizce, açıklamalar ve kullanıcıyla iletişim Türkçe.

## Aşamalar

Tamamlananlar (PDF dönemi): PDF inceleme, Sözler'in PDF'ten ayrıştırılması ve kontrol arayüzü. Aşama 1–4 tamamlandı (cümle ve eşleme kontrolü kullanım sırasında sürecek); Aşama 5 kullanıcının kontrolünü bekliyor.

1. **İndirici:** Katalog, nazik istemci, dört sitenin indiricisi ve bütünlük doğrulaması. Önce Sözler pilotu, ardından bütün eserler toplu indirildi:
   `uv run python -m risale_mcp.fetch get --all --site <site>` (her site ayrı süreçte; günlükler `data/raw/logs/`).
2. **Ayrıştırıcı:** erisale blokları → `data/books/<eser>.json` (başlık ağacı, paragraflar, hâşiyeler): `uv run python -m risale_mcp.build --all`. erisale'deki 27 eser ayrıştırıldı; Sözler PDF çıktısıyla karşılaştırıldı, PDF kodu silindi.
3. **Cümleler:** Cümle bölücü (`sentences.py`, `build` içinde çalışır) ve altın örnek testleri; kontrol arayüzüne kitap seçici, cümle numaraları ve cümle düzeyinde işaretler eklendi. Kullanıcı Sözler'i kontrol eder.
4. **Diğer eserler:** risale.online, risaleoku ve kastamonur.com (önce Yeni Asya) ayrıştırıcıları; mecmuaların ana ciltlere eşlenmesi; bulunamayan eserler için kaynak araması. 38/43 eser ayrıştırıldı (`ESERLER.md`).
5. **Veritabanı:** SQLite ve FTS5 kurulumu, normalizasyon, sorgu dili, âyet dizini, birim testler: `uv run python -m risale_mcp.build_db`.
6. **MCP sunucusu:** Araçları yaz. MCP Inspector ile test et.
7. **Uçtan uca test:** `claude mcp add` ile bağla, `tests/golden_questions.md` sorularıyla dene, adreslerin doğruluğunu elle kontrol et.
