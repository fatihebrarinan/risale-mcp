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

Eserlerin listesi, her birinin kaynağı ve durumu tek yerde tutulur: `src/risale_mcp/catalog.py`. Her eserin hangi aşamada olduğu `ESERLER.md` kontrol listesindedir (`uv run python -m risale_mcp.checklist` ile diskten üretilir, elle düzenlenmez). 74 eserden 73'ü ayrıştırıldı; eksik olan Kızıl İcaz'ın Türkçesi (Aşama 17).

Genel sunucunun kaynakları (izinler `docs/kaynak-bilgilendirme-epostasi.md`):

| Kaynak | Rol | İzin ve notlar |
|---|---|---|
| **erisale.com** | Birincil kaynak: ana ciltler, Eski Said eserleri, Asâ-yı Mûsâ, Sikke, Muvazeneler (27 eser) | e-Risale'yi kaynak gösterdiğimiz sürece kullanım izni var (görüşme, 2026-10-30; sitede belgelerde gösteriliyor). Her bölüm ayrı sayfa; liste `sitemap-tr.xml`'den. Metin sayfaya gömülü RSC verisinde yapısal ağaçtır: blok türleri (`H2`, `H3`, `Paragraph`, `CenteredParagraph`, `HeadingDescription`…), satır içi başlıklar (`Heading`), Arapça (`RTL`, türü âyet/hadis/Arapça, meali `rtl.txn`), hâşiye tam geçtiği yerde (`FootnoteRef` → `Footnote`). `blockIndex` kitap içinde süreklidir; boşluk = eksik bölüm. robots.txt yalnızca `/api/` yolunu yasaklar; yalnızca okuma sayfaları indirilir. |
| **risaleoku.com** (`risaleoku_app`) | Mecmualar (Zülfikâr, Tılsımlar, Sirâcü'n-Nûr, Gençlik ve Hanımlar Rehberi, Küçük Sözler, Fihrist, Âsâr-ı Bediiyye), Nutuk, Makalat ve Âsâr parçaları, Hizbler ve dualar, aslı Arapça eserler, 16 Osmanlıca cilt | Site sahibi, kazanç olmadığı ve kaynak gösterildiği sürece bütün eserlere izin verdi. Katalog `/api/v1/content/changes`, dosyalar `/f/<sha256>.txt.gz`, meal `|n@` numarasıyla. `uv run python -m risale_mcp.fetch risaleoku [anahtar…]`; ham veri `data/raw/risaleoku_app/`. Biçim `books/risaleoku_app.py` başında. Sayfa başındaki ve Arapçadan sonraki satır cümle ortasında da girintili gelir: paragraf sürer. Aslı Arapça eserler başlık ağacını ve Türkçeyle paralel kimlikleri `books/outlines/<eser>.json` şablonundan alır, metin kelime çapalarıyla (bir kısmında `printed`: bu baskının başlık satırı, `start`: ilk kelimeleri) yerleşir. Geçişin kayıtları: `docs/risaleoku-gecis-plani.md`. |
| risale.online | Sikke'nin ikinci "Husrev'in Bir Fıkrasıdır"ı (13 blok, `erisale.SUPPLEMENTS`; alt başlıkta işaretli) | Hayrat baskısı, JSON API (`/risale-api/fihrist`, `/risale-api/paragraf`). |
| Keşif Yolculukları Risale-i Nur Eğitim Programı | Ta'likat'ın Türkçesi | Ediz Sözüer'in programı; Word dosyası Google Drive'da, Protranslate'in tam tercümesi. Telif bildirimi "asliyetini korumak ve kaynak belirtmek şartıyla" serbest kullanım tanır. |
| Kullanıcının dosyaları (`kullanici`) | Rumuzat-ı Semaniye | İnternette serbest metni olmayan eserin PDF'i; `data/` altına konur, `fetch get` ham arşive kopyalar. Mektubat'ta da bulunan paragraflar oraya eşlenir. |
| tanzil.net | Kur'ân-ı Kerîm | Arapça metin üç biçimde ve iki Diyanet meali, XML. Metin değiştirilmeden, kaynağı (Tanzil Project) ve bağlantısı belirtilerek kullanılır; mealler yalnızca ticari olmayan kullanım içindir. Meal dosyalarının açıklama satırları XML'de geçersiz `--` taşır; ayrıştırmadan önce atılır. |

- **Yalnız yerelde (`Work.private`):** Badıllı'nın harekeli Mesnevî'si (`el-mesnevi-el-arabi-harekeli`; rasaelalnour Word dosyası, kullanıcının isteği), Sirâcü'n-Nûr'un Hayrat baskısı (`siracun-nur-hayrat`; Onikinci Şuâ'ya bağlı raporlar ve müdafaalar başka yerde yok), sonradan yapılmış derlemeler Esasat-ı Nuriye (İttihad, "her hakkı mahfuz") ve Hizmet Rehberi ve Düsturları (Ahmet Koçoğlu, 2018): ikisinde derleyicinin ≈28 bin kelimesi var, müellife mal edilmemeli. `build` iki veritabanı kurar: `risale.db` (hepsi) ve `risale-public.db` (private'sız); `deploy.sh` sunucuya ikincisini gönderir.
- **Bırakılan kaynaklar:** rasaelalnour.com (Hizmet Vakfı izin vermedi; Arapça eserler izin veren risaleoku'ya geçti, yalnız yerel harekeli Mesnevî kaldı, sınır karşılaştırması da oradan), kastamonur.com, Yeni Asya, eski risaleoku sayfaları. Eserleri artık risaleoku'dan gelir; ayrıştırıcıları ve ham verileri karşılaştırma için duruyor. Yeni kaynak eklenecekse önce izin istenir.
- **Osmanlıca (`osmanlica` grubu, dil `os`):** Envar baskısı, eşlenmez, Türkçe kimliklerle paralel değildir (`sozler-osmanlica/011/001`), anlamsal aramaya girmez (Türkçe sonuçları yinelemesin). Eşleme Aşama 19.
- **Fihrist Risalesi** mecmua olarak katalogdadır (`fihrist-risalesi`). **Hizb-i Nurî** Zülfikâr'ın hâtimesidir (`hizb-i-nuri`, müellifin takdimleriyle).
- Bir kaynak kitabı birden çok esere bölünebilir: erisale'nin "İlk Dönem Eserleri" kitabı Divan-ı Harb-i Örfî, Münazarat, Sünuhat vb. eserlere ayrılır. Lemeat (Sözler'in sonu) ve Hakikat Çekirdekleri (Mektubat'ın sonu) ayrı eserdir. Seçim, katalogdaki bölüm slug önekleriyle yapılır.

Ham ve ara veri git'e eklenmez.

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
- Bugünkü `data/` ileride `kisisel` derlemi olur. Ayrım, ortakların verisi gelince yapılır. Genel sunucu bu derlemden private eserler çıkarılarak kurulur.

## Teknik tercihler

- Dil: Python 3.11+
- Ortam ve bağımlılıklar: `uv`
- HTTP: standart kütüphane (`urllib`), `sources/http.py` içindeki nazik istemci (istekler arası bekleme, yeniden deneme).
- Veritabanı: SQLite + FTS5 (kelime araması). Anlamsal arama: Voyage `voyage-context-4` vektörleri ayrı dosyada, benzerlik numpy ile (bkz. Anlamsal arama).
- API anahtarları proje klasöründeki `.env` dosyasında (`VOYAGE_API_KEY`, `OPENAI_API_KEY`; git'e eklenmez, `env.py` okur). Her şey ileride bir internet sunucusuna taşınacakmış gibi tasarlanır: sunucuda yalnızca numpy, sağlayıcı SDK'sı yok.
- MCP: resmi Python SDK'sı (`mcp` paketi, FastMCP). Not: `@modelcontextprotocol/sdk` TypeScript paketidir, kullanmıyoruz.
- Test: `pytest` + MCP Inspector + Claude Code'a `claude mcp add` ile bağlayarak elle deneme.
- Platform: Linux Mint.
- PDF: PyMuPDF yalnızca kullanıcının PDF'lerini (Rumuzat) ayrıştırmada kullanılır.

## Klasör yapısı

```
risale-mcp/
├── site/                  # risalemcp.com: index, belgeler, gizlilik, kullanım şartları, en/; talimat.md, chatgpt-talimat.md (proje talimatları; site gösterir, kullanıcı kopyalar)
├── docs/                  # Caddyfile, servis birimleri, dizin başvuruları, izin e-postaları, risaleoku-gecis-plani.md, ayet-duzeltmeleri.md
├── scripts/               # deploy.sh (kod, hazır veri, site; auth.db'ye dokunmaz), sunucu.sh (uzak yönetim), chatgpt-paket.sh, ikon.sh
├── packaging/chatgpt/     # OpenAI eklenti paketi
├── data/                  # git'e eklenmez
│   ├── raw/<kaynak>/      # ham yanıtlar; logs/
│   ├── interim/           # erisale/ blokları, review/ kontrol arayüzü, outline/, quran/ayah_check.md, ayah_links/, arabic_kinds/, golden/, search_eval/
│   ├── books/<eser>.json  # her eserin JSON'u
│   ├── vectors/           # anlamsal arama vektörleri
│   ├── quran.json, risale.db, risale-public.db
│   └── auth.db            # kullanım kaydı, hata ayıklama anahtarı; OAuth kipinde hesaplar (risale.db gibi yeniden kurulmaz)
├── src/risale_mcp/
│   ├── paths, catalog, checklist, env, normalize, headings
│   ├── fetch.py, build.py, build_db.py, db.py   # indirme, ayrıştırma, veritabanı CLI'ları
│   ├── sentences.py       # cümle bölücü, incipit, atıflar, altın örnekler
│   ├── arabic_kinds.py    # Arapça parçaların türü ve dayanağı, âyet adres düzeltmeleri
│   ├── quran.py, ayah_links.py, search.py, semantic.py, embeddings.py, search_eval.py
│   ├── library.py, server.py, citations.py, auth.py, golden.py
│   ├── review_ui.py, review_assets/, static/
│   ├── sources/           # site başına indirici (ham kayıt + doğrulama)
│   └── books/             # model.py, mecmua.py, kaynak başına ayrıştırıcı, outlines/, pdf_text.py, rumuzat.py
└── tests/                 # pytest; golden/ altında altın sorular, âyet kararları, arama seti, cümle örnekleri
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
- **`gaps`**: kaynakta bulunamayan bloklar `{node_id, missing_blocks, after, note?}` (`after` yoksa düğümün başı). Metin uydurulmaz. Şu an Makalat'ta Âsâr-ı Bedîiyye'de olmayan 3 parça.
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
Ayrıntı `books/mecmua.py` başındaki açıklamadadır. Mecmualar ve ikincil kaynaktaki eserler ana ciltlere (Eski Said eserleri ve ana ciltler) eşlenir:
- Metinler baskıdan bağımsız kelimelere indirilir (`normalize.match_words`), 5 kelimelik diziler karşılaştırılır. En çok diziyi paylaşan ana cilt paragrafından başlanır, yakın komşular kapsamı artırdıkça eklenir. Dizilerin en az %35'i ve en az 3 dizi tutarsa eşlenir.
- Aynı metin birden çok yerdeyse önceki eşlemenin ardından gelen seçilir; kısa paragraflar ("﷽") önceki ya da sonraki eşlemenin komşusuysa bağlanır. Tek kelimelik paragraf ("Elhâsıl:") komşu olmadan bağlanmaz. Hizb-i Nurî son çaredir, beraberlikte ana cilt aslı Arapça eserin önündedir.
- İkinci geçiş (`_fill_between`): iki eşlemenin arasında kalan paragraflar, o iki yerin arasındaki ana cilt paragraflarıyla kelime kelime hizalanır. Sonradan derlemelerde kapalıdır (dizin ve başlıklar yanlış bağlanıyordu).
- Eşlenen paragrafın metni silindiği için `keep_unique`: mecmuaya özgü kelimesi çok olan (en az 8 kelime ve %15) paragraf metniyle kalır. erisale mecmualarında kapalıdır (kimlikler kaymasın).
- Mecmua bir ana cilt paragrafını bölmüşse art arda gelen, örtüşen eşlemeler tek kayıtta birleşir; kimlikler yeniden numaralanmaz.
- Eşlenemeyen paragraflar mecmuaya özgüdür ve metinleriyle kalır (ör. Sekizinci ve On Sekizinci Lem'a'nın asıl yeri Sikke-i Tasdik-i Gaybî'dir). Oranlar `ESERLER.md`'de.

### Cümle kuralları
- Numaralar her düğümün **kendi metninde** 1'den başlar; alt düğümler kendi sayımını yapar.
- **Hâşiye cümleleri** kendi içinde numaralanır: `… › 32. cümle › Hâşiye › 2. cümle`. Bir cümlede birden çok hâşiye varsa `Hâşiye 1`, `Hâşiye 2`. Şerh ayrı sayılır: `…/c032/s1/c002`, `… › 32. cümle › Şerh › 2. cümle`.
- **Bölme:**
  - Cümle şu işaretlerden (ve ardından gelebilecek kapanış tırnağından) sonra biter: `.` `!` `?` `…` `‥`. Şart: ardından büyük harf, açılış tırnağı ya da parantezi, Arapça bir parça, madde numarası ("2. Yâhut") ya da tercümenin köşeli numarası ("[44]Kezâ") gelmeli.
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
- **Arapça türü ve dayanağı.** Kaynağın işareti (`kind_source = kaynak`) değiştirilmez. risaleoku âyet/hadis ayırmaz, erisale de bazı alıntıları `arabi` bırakır: `build_db` her parçayı `arabic_kinds.py`'den geçirir (JSON'lar değişmez). Dayanaklar: `kuran` (metin Kur'ân'da), `meal` (aynı Arapçanın risaleoku meal kaydı âyet numarası ya da hadis kaynağı veriyor), `kaynakca` (kaynakçası hadis kitabı), `erisale` (aynı Arapçayı erisale hadis diye işaretlemiş), `baglam` (yalnız yanındaki söz: hadis adayı, araçta `kind_unverified`). Kalıp ifadeler ("Mâşâallâh") `arabi` kalır, bağlamı "âyet" derse âyettir. Parçanın yalnız bir kısmı âyetse parça `arabi`, âyet `ayah_quotes`'tadır. Rapor ve gözden geçirme örneklemleri `data/interim/arabic_kinds/`.
- erisale'nin Arapça metindeki köşeli numaraları ("[4]فَهَذَا…") Arapça asıl ile hâşiyedeki tercümesini eşleştirir; metinde kalır.

## Veritabanı (Aşama 5)

`uv run python -m risale_mcp.build_db` komutu `data/books/*.json` dosyalarından `data/risale.db`'yi her seferinde sıfırdan kurar (≈17 sn). Asıl kaynak JSON'lardır, veritabanı elle düzenlenmez. Kurulum geçici dosyaya yapılır, sayılar JSON'larla tutmazsa veritabanı yazılmaz. Şemanın açıklaması `db.py`'de, kurulum kuralları `build_db.py`'nin başındadır.

- **Tablolar:** `works` (katalogdaki bütün eserler; JSON'u olmayanlar `built = 0`), `nodes` (`ord`..`last_ord` alt ağaçtır), `node_sources`, `paragraphs` (eşlenmiş mecmua paragrafında `text` NULL), `paragraph_sources`, `sentences`, `arabic` (cümleye bağlı; âyette `sura`, `ayah_start`, `ayah_end`), `sura_names` (veriden öğrenilen yazılışlar ve Kur'ân katmanının 114 Türkçe adı), `notes`, `gaps`, `meta`; Kur'ân katmanı `quran_suras`, `quran_ayahs`, `quran_translators`, `quran_translations`, `ayah_quotes`; âyet ilişkileri `ayah_links`. Arama dizinleri `sentences_fts` ve `nodes_fts` (başlık, alt başlık, içindekiler adı).
- **Kimlikler:** `id` JSON'daki kalıcı kimliktir; `seq` yalnızca bu veritabanında geçerli tamsayı anahtardır ve okuma sırasını verir.
- **Normalizasyon:** Dizin ve sorgu `normalize.search_words` biçimindedir. Şapka, çengel (ş/s, ç/c, ğ/g, ö/o, ü/u), Arapça hareke, kesme ve tatvil yok sayılır; ayrıca **ı = i** sayılır (klavyesiz "isik" → "ışık"). Biçim değişirse `db.NORMALIZATION` artırılır.
- **Sorgu dili** (`search.py`): kelimeler (hepsi geçmeli), `"tam ifade"`, `haşr*` (kelime başı), `OR`, `-kelime` / `NOT`, `NEAR(a b, 5)`. Sıralama BM25'tir; kısa cümleler öne çıkma eğilimindedir.
- **Mecmualar:** Ana cilde eşlenen paragrafların cümlesi yoktur. Bu yüzden aynı cümle aramada iki kez çıkmaz.
- **Âyetler:** İki biçim çözülür: "Bakara Sûresi, 2:255" ve Hayrat'ın "Sûre-i Bakara, 255" biçimi. Sûre adlarının numaraları, veride numarasıyla geçen yazılışlardan öğrenilir. Birden çok âyet sayılmışsa ilk aralık alınır (bkz. `AYAH_FIXES`). `data/quran.json` varsa her biri Kur'ân metniyle denetlenir (`arabic.ayah_check`) ve işaretsiz alıntılar bulunur (bkz. Kur'ân katmanı).
- **Anlamsal arama** veritabanında değil, ayrı vektör dosyasındadır (bkz. Anlamsal arama); veritabanı yeniden kurulsa da vektörler kaybolmaz.

## Kur'ân katmanı (Aşama 9)

Kur'ân-ı Kerîm Risale eserlerinden ayrı bir katmandır; atıf birimi âyettir ("Bakara Sûresi, 2:255", `›` olmadan; `cite` bu atıfları denetlemez, doğruluğu `get_ayah`'tan gelir). Ayrıntı `quran.py` başındaki açıklamadadır.

```
uv run python -m risale_mcp.fetch quran   # tanzil.net'ten ham veri (bir kez)
uv run python -m risale_mcp.quran         # data/raw/tanzil -> data/quran.json
uv run python -m risale_mcp.build_db      # Kur'ân tabloları, âyet denetimi ve eşleme; rapor data/interim/quran/ayah_check.md
```

- **Metin:** kullanıcıya her zaman harekeli Medine Mushafı hattı (`quran_ayahs.text`) gösterilir (kullanıcının isteği: harekesiz okuyamıyor). İmlâî harekeli metin `text_simple`, harekesiz metin yalnızca eşlemede. risaleoku'nun Türk hattı iskelet olarak aynıdır, istenirse ikinci hat olarak eklenebilir.
- **Mealler:** Diyanet İşleri Başkanlığı ve Türkiye Diyanet Vakfı (Tanzil'den). Diyanet İşleri meali art arda âyetleri birlikte tercüme edebilir; bunlar `first_ayah`..`last_ayah` ile işaretlidir, araç `covers_verses` der. Üç meal türü karıştırılmaz: müellifin "Yani" izahı (metin), nâşirin meali (`publisher_translation`), Diyanet mealleri (`get_ayah`).
- **Sûre adları:** Türkçe 114 ad `quran.SURA_NAMES`'tedir; veride hiç geçmeyen sûreler de adıyla aranır.
- **Harf iskeleti (`quran.skeleton`):** Risale'nin imlâsı Tanzil'inkinden farklıdır. İki metin de iskelete indirilir: hareke ve işaretler, hemze, elif, vav, ye atılır; elif çeşitleri, tâ-i merbûta, Farsça harfler birleştirilir. Alıntı "…" ve "الخ" yerlerinden parçalara bölünür; her parça Osmanî ya da imlâî iskelette aranır.
- **Kaynağın âyetleri denetlenir** (`arabic.ayah_check`): `exact`, `near`, `iktibas` (müellifin uyarlaması, kısaltması ya da tekrarı), `dizgi_suphesi` (potansiyel hatalı, 3 kayıt), `empty`. Kullanıcının kararı: Kur'ân esastır, müellifin sözü değiştirilmez. Yanlış numara ve eksik aralık `arabic_kinds.AYAH_FIXES`'te düzeltilir (metin değil adres); dizgi şüphesi kullanıcıya gösterilmeden metne uygulanmaz (`docs/ayet-duzeltmeleri.md`). Araç `check` ile uyarır.
- **Âyet türü** `arabic_kinds.py`'den gelir (bkz. Dikkat edilecek noktalar). Bütün parça âyetse parça `ayet` olur (Hizbler, aslı Arapça eserlerin ﴿ ﴾ alıntıları); bir dua içinde geçen âyet `ayah_quotes`'ta kalır. Kısa ve birden çok sûrede geçen numaralı âyet ("الٓمٓ﴿١﴾"), bölümde bulunan öbür âyetlerin en az %80'i aynı sûredense o sûrede aranır. Âyet birden çok yerde geçiyorsa numara verilmez.
- **Hizbü'l-Kur'ân'ın sûre sınırları** metindeki Arapça başlıklardan gelir.

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
- **Sayılar:** ≈980 ilişki, ≈310'u güçlü. 2. turda 40'lık örneklemin 40'ı doğruydu; 62 karar kilitli. Âyet işaretleri artınca ilişkiler de arttı, yeni örneklem henüz bakılmadı. Kullanıcının örneği (Lem'alar › Otuzuncu Lem'a › Altıncı Nükte › İkinci Şuâ › Birinci Mes'ele: Bakara 2:255, Hûd 11:56, Zümer 39:63) bölüm kapsamlı `isaret`'tir.
- **Gözden geçirme:** güçlüler doğrudan kabul edilir; kullanıcı her turda 40'lık örneklemi (`sample-<tur>.md`) kontrol eder, bulduğu hatalar kurallara ve karar dosyasına döner. Zayıflar tek tek gözden geçirilmez.
- **Araçlar:** `find_ayah` tek âyette `links` (güçlüler önce, kanıt cümlesiyle), `get_ayah` `linked_in_works`, `read_section` başlıkta `linked_verses`. Talimat: ilişkiyi türüyle ve kanıtıyla an, "tefsir" deme; ilişkili âyetleri her alıntının ardına ekleme, kullanıcı sorarsa ya da âyet soruyla ilgiliyse ver (kullanıcının isteği).

## Aslı Arapça eserler (Aşama 11)

Bediüzzaman'ın Arapça yazdığı eserlerin hem Arapça aslı hem Türkçesi tutulur; ikisi ayrı eserdir, bölüm kimlikleri paraleldir (`isaratul-icaz-arabi/sure-i-bakara/6` ↔ `isaratul-icaz/sure-i-bakara/6`). Anlamsal arama iki dili aynı bölümde buluşturur.

| Eser | Arapça (risaleoku, şablonlu) | Türkçe |
|---|---|---|
| el-Mesnevî el-Arabî | `el-mesnevi-el-arabi` (İhsan Kasım baskısı, harekesiz; harekeli Badıllı baskısı yalnız yerelde) | `mesnevi-i-nuriye` (erisale) |
| İşaratü'l-İ'caz | `isaratul-icaz-arabi` | `isaratul-icaz` (erisale, Abdülmecid Nursî tercümesi) |
| Kızıl İcaz | `kizil-icaz-arabi` | yok (Aşama 17) |
| Ta'likat | `talikat-arabi` | `talikat` (Keşif, Protranslate tercümesi) |
| Hutbe-i Şamiye | `hutbe-i-samiye-arabi`: İhsan Kasım'ın Türkçeden tercümesi (1911 aslı değil) | `hutbe-i-samiye` (erisale) |

- **Şablon:** `books/outlines/<eser>.json` başlık ağacı, kimlikler ve kelime çapaları; ilk çapadan önceki kısım (muhakkikin ön sözü) alınmaz. Sıra ve yerleşim bu baskıya göredir (Mesnevî'de Nokta Nûr'dan önce).
- **Mesnevî'nin bu baskıdaki farkları:** sınırlar yerel harekeli baskıyla karşılaştırıldı (yalnız sınır bilgisi, metin risaleoku'dan). Remz 20 ve 21 ile `katre/nukte` bu baskıda yok; Mebhas Reşha'da değil Nûr'un içinde geçer; takrizler bu baskıdaki yerindedir (`katre/takriz`, `zerre/takriz`). Habbe, Şemme ve Zeyl-ül Hubab'da kısa İfade-i Meram gövdeden önce gelir, ayıran başlık yoktur: ayrı bölüm açılmaz. Türkçedeki "Nokta" risalesi aslı Türkçedir, İhsan Kasım'ın tercümesi diye işaretlidir; Mukaddime de.
- **Kızıl İcaz:** Ahdarî'nin Süllem'ine hâşiye. `<…>` beyitleri Süllem'indir, `quote` olarak durur, müellifin sözü değildir. Sayfa dipnotları Molla Abdülmecid'in şerhidir: hâşiye gibi cümlesine bağlıdır, `commentator: "Abdülmecid Nursî"` taşır, atfı "› Şerh ›"; müellife mal edilmez. "ديباجة" gibi kaynakta olmayan başlıklar alt başlıkta işaretlidir (Türkçe Ta'likat'ın "Hadd Bâbı" gibi başlıkları da).
- **Ta'likat:** Gelenbevî'nin Burhân'ına hâşiye; iki dilde aynı 11 kimlik (`saykal.TALIKAT_SECTIONS`). Arapçada dipnotlar müellifin hâşiyeleridir, "ع. ب" gibi notlar not. 44 kısa not eski baskıda olup bu baskıda yoktur; izin vermeyen kaynaktan kopyalanmaz.
- **Dipnotlar:** çok satırlı olabilir; sayfanın son notunun işareti sonraki sayfada olabilir. "(المؤلف)" müellifin hâşiyesi, öbürleri muhakkikin notu (`notes`).
- Sunucu talimatı: eserin her katmanı müellifin değildir (tercüme alt başlıkları, Süllem beyitleri, `commentary_by` taşıyan Abdülmecid şerhi).

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
- **Son ölçüm** (2026-10-30, 74 eser sonrası): ilk 10'da %70 / MRR 0,46; 2026-10-26'da %74 / 0,49 idi, farkın nedeni araştırılmadı.
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
uv run risale-mcp --transport streamable-http --public-url https://<…>   # OAuth'lu (askıda)
uv run risale-mcp --transport streamable-http --public-url https://<…> --open   # açık kip: OAuth yok, herkes sınırlı (genel sunucu)
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
| `cite(sources)` | Cevaptan önce bir kez (gösterilecek her alıntı sözleriyle; sonradan eklenen alıntı için yeniden): dayanılan cümle ya da aralıkların kimlikleri ve alıntılanan sözler (`[{id, quote?}]`, kaynakça sırasıyla). Her biri için tam atıf (`cite_as`), sorun (aralık 8 cümleyi ya da bölümü aşıyor, alıntı o cümlelerde yok: asıl yeriyle, bilinmeyen kimlik) ve cevabın "Kaynaklar" listesi (`bibliography`: "[n] cite_as"). Önceki `verify_citations(text)` taslağın tamamını alıyordu (bkz. Hız ve token); sonuçtaki `note` (`citations.CITE_NOTE`) kaynakçanın değiştirilmeden kopyalanmasını, eser dışı kaynakların ayrı listede verilmesini söyler (ChatGPT satırları kendisi yazıyordu) |

### Uzaktan erişim
Ayrıntı `auth.py` başındadır.

- **Genel sunucu açık kipte çalışır** (`--open`; OAuth kullanıcının kararıyla 2026-10-29'da askıya alındı: OpenAI portalı OAuth bilgisini görünce "No authentication" seçilse de ısrar ediyordu). OAuth uç noktaları, giriş sayfası ve `sign_in` yoktur; herkes hesapsız ve sınırlıdır (anlamsal arama günde toplam 2.000, istekler dakikada toplam 120; sınır adres başına değil, çünkü claude.ai'nin istekleri Anthropic'in adreslerinden gelir). OAuth kodu ve testleri (kişi başına hesap, `--anonymous`) yerinde durur; ortak derlemler gibi erişimi kısıtlı bir sunucu gerekirse yeniden açılır.
- **Hata ayıklama adresi:** `scripts/sunucu.sh auth debug-url --new` gizli bir `https://mcp.risalemcp.com/mcp/<anahtar>` verir (anahtarın yalnızca özeti saklanır); o adrese gelen istekler `(debug)` kullanıcısıyla, girdileriyle 7 gün kaydedilir ve sınırlara takılmaz. Okuma `scripts/sunucu.sh auth usage --user '(debug)' --params`, kapatma `--revoke`.
- **Kullanım kaydı:** her MCP isteği zaman, araç, süre ve hata türüyle `usage` tablosuna yazılır, 90 gün tutulur. Parametreler (sorgular, alıntılar) kaydedilmez, IP de: Anthropic'in dizin politikası gereksiz konuşma verisini yasaklar (kullanıcının kararı). Gizlilik politikası (`site/gizlilik.html`) bunları söyler; değişirse orası da değişir.
- **Uzak sunucu:** Hetzner Cloud CAX11 (ARM, 4 GB, Helsinki, Ubuntu 24.04), genel IPv4 `95.217.21.105`, Tailscale adı `risale` (`100.108.174.19`; SSH yalnız oradan, anahtar `~/.ssh/risale_hetzner`). Bağlayıcı **`https://mcp.risalemcp.com/mcp`**, tanıtım sitesi `https://risalemcp.com`; ikisini Caddy sunar (`docs/Caddyfile`), sertifika Let's Encrypt. Alan adı Cloudflare'de "DNS only" (proxy uzun MCP bağlantılarını 100 sn'de keser). Servis `risale-mcp` (`docs/risale-mcp.server.service`). Güvenlik duvarı: 80, 443; SSH yalnız `tailscale0`.
- **Güncelleme:** `scripts/deploy.sh` (kod, `risale-public.db`, vektörler, `quran.json`, `.env`'den yalnız `VOYAGE_API_KEY`), yalnız kod ve site için `--code`. Ayrıştırma ve veritabanı kurulumu yerelde yapılır. `data/auth.db`'nin asıl kopyası sunucudadır, deploy ona dokunmaz. Yönetim: `scripts/sunucu.sh auth …`, `status|restart|logs|ssh`.
- **Logo:** Claude ve dizin bağlayıcının simgesini `https://mcp.risalemcp.com/favicon.ico`'dan alır. Logo değişince `icon.svg`'den `icon.png` ve `favicon.ico` üretilir (`scripts/ikon.sh`), `src/risale_mcp/static/` ve `site/` altına konur.
- **Dizin başvuruları:** Claude (`docs/dizin-basvurusu.md`) ve OpenAI (`docs/chatgpt-dizin-basvurusu.md`) gönderildi, karar bekleniyor. Yayıncı adı "Nur Hadimleri". Kabul edilirse sitedeki kurulum adımlarına dizinden ekleme yolu açılır (`site/index.html`'de yorum satırı olarak hazır).
- **Tanıtım sitesi** (kullanıcının kararları): ana sayfa sırasıyla vizyon, karşılaştırma, platformlara göre kurulum, kapsam; ekran görüntüsü yok. Karşılaştırmadaki cevaplar claude.ai'den alındığı hâliyledir, **kısaltılmaz ve düzeltilmez**; işaretler bizimdir ve veritabanıyla denetlendi. Türkçe sayfalar Claude'un arayüzündeki "bağdaştırıcı" kelimesini kullanır. Proje talimatları tek kaynaktan: `site/talimat.md`, `site/chatgpt-talimat.md` ve `en/` karşılıkları. Dışarıya istek yok (gizlilik politikası öyle diyor): yazı tipi Google Fonts'tan yüklenmez. CSS ya da JS değişince sayfalardaki `?v=N` artırılır.
- **ChatGPT:** ücretsiz hesapta da elle eklenir (`Eklentiler › Ekle › Özel MCP sunucusu ekle`, `Kimlik doğrulama yok`); `clientInfo.name` `openai-mcp`. Web'de eser içeriği için web aramasına kaçabildiği, kaynakça satırlarını kendisi yazabildiği için sunucu talimatında ve `citations.CITE_NOTE`'ta kurallar var; normal sohbette web araması kapalıyken sonuç en temiz.

### Atıf denetimi (`citations.py`)
Ayrıntı modülün başındaki açıklamadadır. `cite` aracı kimliklerden atıf kurar (`CitationChecker.sources`); altın soru raporu yazılmış cevaptaki atıfları denetler (`check`). Kaynakçalı cevapta "[n]" ile biten alıntı bloğu kaynakçadaki n numaralı atfa bağlanır.
- Satır `›` işaretlerinden bölünür; bir satırda birden çok atıf, atıftan önce ve sonra düz yazı olabilir. Atıf alıntıyla ya da "32. cümle" ile biter.
- Başlık basılı adla, içindekiler adıyla, tür ve numarayla ("İkinci Makam" = "Yirminci Söz’ün İkinci Makamı"), ekli ("Dördüncü Söz'de"), "(asm)" gibi ayraçsız ya da "…" ile kısaltılmış yazılabilir; ara başlıklar atlanabilir. Bunlar geçerlidir ama tam yolu yazılmamış sayılır (`exact`), araç tam atfı verir.
- "…", "aynı yer", "(› …" ve eser adı yazılmamış yol bir önceki atfa göre çözülür. Yol birden çok bölüme uyarsa önce alıntının geçtiği, sonra önceki atfa yakın, ana ciltteki ve üst seviyedeki bölüm seçilir.
- Ardışık cümleler: "“…” ile başlayan N cümle" ya da "› 4.–7. cümle". Aralık bulunan cümleden başlar, aynı bölümün ana metninde (hâşiyede aynı hâşiyede) sürer; 8'i aşarsa `range_too_long`, bölümü aşarsa `range_past_section`.
- Alıntı bloğu: atfın hemen önündeki ya da ardındaki `> "…"` bloğu (araya yalnızca boş satır girebilir) atfın kapsadığı cümlelerde aranır; "…" ile atlanan yer serbesttir. İki atıf arasındaki blok uyduğu atfa bağlanır. Uymazsa `block_ok` yanlıştır.
- Sonuçlar: `ok`, `section`, `mid_sentence`, `quote_not_found` (alıntının asıl yeri `elsewhere`), `no_such_sentence`, `unknown_section`, `ambiguous`, `range_too_long`, `range_past_section`.

### Hız ve token
- Gecikme sunucuda değil modelin yazdıklarındadır. Bu yüzden `cite` taslak almaz, kimlik ve alıntı alır; cevabın tamamını araca yazdırmak (eski `verify_citations`) cevabı 3–4 kez yazdırıyordu. Yalnız kimlikli sürüm denendi, kullanıcı alıntı denetimini korumayı seçti.
- **Kaynakça** (kullanıcının kararı): kısa ya da uzun her cevapta alıntı sonunda "[1]" ve sonda "Kaynaklar"; metnin içinde atıf yolu yazılmaz. claude.ai'nin kaynak kutucukları MCP sonuçlarında desteklenmiyor, biçim talimatla kurulur.
- Yapılandırılmış çıktı kapalı (`structured_output=False`). Anlamsal arama eşlemesi ve atıf dizini sunucu açılırken arka planda kurulur (`server._warm`).
- **Kaynaklar** (kullanıcının sohbete eklediği bağlam): `risale://works`, `risale://outline/{work}`, `risale://text/{+section}` (ör. `risale://text/sozler/10`; numaralı cümlelerle Markdown).
- **Hazır komutlar** (İngilizce adlar): `topic_survey(topic, scope?)` konunun eserlerde geçtiği yerler (2. hedef), `text_and_commentary(question)` "metin ne diyor" ve "yorum" ayrı (3. hedef), `discuss(topic)` müzakere, `self_test(section)` bölümden soru sorup cevabı metinle denetler, `lesson_plan(subject)` atıflı ders planı.
- **Sunucu talimatları** `server.py`'nin başındadır; asıl kuralları oradan oku (atıf, alıntı bloğu, kaynakça, metin ve yorum ayrımı, âyet, meal ve hadis katmanları).

## Uçtan uca deneme (Aşama 7)

Linux'ta Claude Desktop olmadığı için MCP istemcisi olarak Claude Code kullanılır. Üç katman:

1. **Araç düzeyi:** `npx @modelcontextprotocol/inspector uv run risale-mcp` (tarayıcıda araçları elle çağırma).
2. **Elle sohbet:** `uv run python -m risale_mcp.golden sandbox ~/risale-deneme` sonra `cd ~/risale-deneme && claude`. Klasör proje dışındadır (Claude Code üst klasörlerdeki `CLAUDE.md`'yi okur); yalnızca bu sunucu açık, dosya/kabuk/web araçları kapalıdır. Hazır komutlar `/mcp__risale__topic_survey`, kaynaklar `@risale:risale://text/sozler/10`.
3. **Altın sorular:** `uv run python -m risale_mcp.golden run A1 B7 …` (ya da `--all`). Her soru `claude -p` ile geçici, boş bir klasörde, yerleşik araçlar kapalı (`--tools ""`), yalnızca bu sunucuyla (`--strict-mcp-config`) ve varsayılan modelle sorulur. `--bare` kullanılmaz (OAuth'u kapatır). Döküm ve rapor: `data/interim/golden/<zaman>/` (`report.md`, git'e eklenmez).

Raporun otomatik kontrolleri:
- **Atıflar:** cevaptaki "Yol › … › “ilk kelimeler”" ya da "… › 32. cümle" zincirleri `citations.py` ile veritabanında aranır: ✓ cümle bulundu, ◑ alıntı metinde var ama cümle başı değil, ◐ yalnızca bölüm, ✗ bölüm ya da cümle yok (uydurma olabilir; alıntı başka yerdeyse orası gösterilir). Yanındaki alıntı bloğu atfın cümlelerinde olmayan atıf da ✗ sayılır. Doğru ama kısaltılmış yolla yazılan atıflar tabloda "(n kısa)", ardışık cümle atıfları "(n aralık)" diye sayılır.
- **Beklenen bölüm:** model okudu mu (`read_section`, `get_passage`, `find_sentence`; arama sonucu ve başlık ağacı okumak sayılmaz), cevapta adı geçiyor mu.
- **Araç kullanımı:** çağrılar, parametreleri ve hatalar.

Metin–yorum ayrımı, özetin doğruluğu ve tuzak sorulardaki davranış elle değerlendirilir. Hız ve maliyet karşılaştırması için 7 soru kullanılır: B7 B8 C11 D16 E19 K3 K5 (son çalıştırma `20261030-200047`: 84 atıfın 84'ü doğrulandı, K3'te model beklenen bölümü okumadı).

## Çalışma kuralları

- Aşamaları sırayla yap. Her aşamanın sonunda **dur**, bulguları özetle ve onay bekle.
- Ayrıştırma kurallarını tahmine dayanarak yazma. Önce kaynağın ham verisini incele, örnekleri göster.
- Her aşamada kullanıcının elle doğrulayabileceği bir çıktı üret (örnek JSON, başlık ağacı, sayım tablosu).
- Belirsiz durumlarda en makul varsayımı yap, ama bunu açıkça belirt.
- Kaynak sitelere nazik davran: isteklerin arasında bekle, ham yanıtı kaydet, aynı sayfayı ikinci kez indirme.
- Kod tanımlayıcıları İngilizce, açıklamalar ve kullanıcıyla iletişim Türkçe.

## Aşamalar

Tamamlananlar: 1–12 (indirici, ayrıştırıcı, cümleler, diğer eserler, veritabanı, MCP sunucusu, uçtan uca test, anlamsal arama, Kur'ân katmanı, âyet ilişkileri, aslı Arapça eserler, uzaktan erişim). Geçiş kalitesi 2026-10-30'da bitti (`docs/risaleoku-gecis-plani.md`).

Sıradakiler (kullanıcının sırası):

13. **İç atıf ağı:** Risale'nin kendi göndermeleri ("Yirmi Beşinci Söz'de beyan edildiği gibi") bölüm kimliklerine çözülür; kanıt cümlesiyle, kurallarla. Model bir konuyu Bediüzzaman'ın kendi bağlantılarıyla izler. Çözülemeyen göndermeler açıkça listelenir; adres tahmin edilmez.
14. **Hadis katmanı:** Açık ve güvenilir bir hadis derleminin (aşamanın başında araştırılır, lisansı doğrulanır) eklenmesi; Risale'deki hadislerin iskeletle eşlenmesi. Sıhhat derecesi kaynak verisinden gelir, biz hüküm vermeyiz; eşleme "tam alıntı / mânen / bulunamadı" diye ayrılır. Temeli `arabic_kinds.py`'nin işaretleridir (1.075 parça; `kind_source` dayanağı). **Aşamanın başında kullanıcı örneklemleri gözden geçirir** (`data/interim/arabic_kinds/sample-*.md`, önce `hadis-meal`, `hadis-erisale`, `hadis-baglam`, sonra `ayet-meal`): her kayıtta "bu tür doğru mu"; yanlışlar kurala döner, kararlar âyet ilişkilerindeki gibi kilitlenir. Örneklem önce yalnız Türkçe ciltlerden yeniden üretilir. Üç dizgi şüphesine de o sırada bakılabilir.
15. **Konu fihristi (2. hedef):** Konu → cümle listeleri. Anlamsal aramanın üzerine kurulur; konu listesi ve her konunun cümleleri elle gözden geçirilebilir bir dosyada durur, sunucuya araç ya da kaynak olarak eklenir. Konu, ardışık cümle aralıklarından ("pasaj") oluşan ayrı bir katmandır.
16. **Kontrol işaretlerinin işlenmesi:** Arayüzden dışa aktarılan `risale-kontrol-notlari.json` ayrıştırıcı düzeltmelerine dönüşür. Her ✗ için kök neden bulunur. Önce bir kontrol kuyruğu: şüpheli yerler (çok uzun cümleler, boş bölümler, düşük eşleme oranı, PDF kaynaklı eserler) otomatik listelenir.
17. **Kızıl İcaz'ın Türkçesi:** Prof. Dr. Ahmed Akgündüz'e izin ve dijital nüsha isteği (`docs/akgunduz-izin-epostasi.md`, Ta'likat tercümesi de), cevap bekleniyor. PDF ayrıştırmasına cevap gelmeden başlanmaz (kullanıcının kararı).
    - Dijital nüsha gelirse doğrudan ondan ayrıştırılır. Gelmezse ve kullanım izni varsa `data/kizil-icaz.pdf` (399 sayfa resim, kalem işaretli) Claude API Message Batches ile Opus okunur (yerel OCR yetersiz; tahmin ≈12–15 $).
    - Yalnızca Türkçe tercüme okunur; bölümler `kizil-icaz-arabi`'ye paralel kimliklerle bağlanır; baştaki mütercim girişi alınmaz. Okunmuş sayfalar ham veri olarak saklanır (`data/raw/kullanici/kizil-icaz/`). Bloklar türüyle işaretlenir (beyit, şerh, hâşiye, dipnot, başlık); okunamayan yer tahmin edilmez. Önce 10 sayfalık deneme, kullanıcı onaylarsa kalanı. Ayrıştırıcı `books/kizil_icaz.py`.
    - İzin yoksa eser `private` kalır, sunucuya gitmez.
18. **Gemini:** uzak MCP bağlayıcısının Gemini uygulamasında (ve Gemini CLI'da) nasıl eklendiği aşamanın başında araştırılır; sitede "yakında". Sunucu değişmez.
19. **Osmanlıca–Türkçe eşleme:** Kullanıcının Osmanlıca istemesinin asıl sebebi: bir alıntıda isterse Türkçe metinle birlikte oranın Osmanlıcasını da vermek. Türkçe ve Osmanlıca paragrafların (harf çevirisi ya da çapa olarak Arapça satırlar ve başlıklar) eşlenmesi, Türkçe cümleden Osmanlıca karşılığa bağlantı, `get_passage`/`read_section`'a isteğe bağlı Osmanlıca çıktı. Baskı farkı: Osmanlıca Envar, Türkçe erisale. Bir eşleme örneklemi kullanıcıya gösterilir.
20. **Kaynakçada doğrudan bağlantı:** e-Risale ile görüşmeden çıkan öneri (2026-10-30): kaynakçada yolun yanında metnin kendisine bağlantı verilir, kullanıcı metne doğrudan ulaşır. Atıf hangi kaynakta geçiyorsa (erisale.com ya da risaleoku.com) o kaynağın ilgili yerine bağlantı konur. erisale'de bölümün `url`'si outline'da var; risaleoku uygulamasında bölüme doğrudan bağlantı olup olmadığı ve sayfa/bölüm adresinin biçimi aşamanın başında araştırılır. `cite` sonucu (`cite_as`, `bibliography`), sunucu talimatı, proje talimatları ve `citations.CITE_NOTE` buna göre değişir; bağlantı veriden gelir, tahmin edilmez, kaynakta karşılığı olmayan atıf bağlantısız kalır. Yerel eserler ve Kur'ân ayrı düşünülür.
