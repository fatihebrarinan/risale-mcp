# Risale-i Nur MCP — Proje Belgesi

Bu dosya projenin kalıcı bağlamıdır. Her oturumda önce bunu oku.

## Amaç

Bediüzzaman Said Nursî'nin **bütün eserlerini** (Eski Said eserleri, Risale-i Nur ana ciltleri, Lâhikalar, Tarihçe-i Hayat, mecmualar, Hizbler) yapay zekâ modellerinin **kaynağa bağlı kalarak** kullanabileceği bir MCP sunucusu geliştirmek.

Nihai kullanım hedefleri:
1. Model bir konuda yorum yaptığında, dayandığı yeri **cümle düzeyinde** tam adresiyle göstersin.
2. Bir konunun eserlerde geçtiği yerler listelenebilsin.
3. Farklı bakış açılarıyla yapılan yorumlar da metindeki cümlelere dayansın.

İlk hedef 1. hedefin altyapısıdır. 2. ve 3. hedefler sonraki aşamalardır.

**İki gaye** (kullanıcının koyduğu, 2026-11-19): (1) **Kur'ân'ın sonsuz bir derya olduğunu görmeye ve göstermeye çalışmak.** Taslaklar arası farklar (tenevvü), vecih haritası ve okuma platformu buna hizmet eder; yapay zekânın neyi yapıp neyi yapamadığını dürüstçe göstermek de bunun parçasıdır. (2) **İleride tefsir üzerinde çalışacaklara kaynak ve çekirdek olmak.** Kaynağa bağlılık, kalıcı kimlikler, taslakların ve ölçü verilerinin silinmeden saklanması bunun içindir. İki gaye de "yapay zekânın ürettiği hiçbir şey tefsir diye anılmaz" ilkesinin içindedir.

**Uzun vadeli hedef (2026-11-04): tefsir altyapısı.** Müellifin İşârâtü'l-İ'câz'ı ve Risaleleri ileride bir heyetin yapacağı işe "me'haz" diye göstermesine (`isaratul-icaz/mukaddemat/tenbih/c012`) dayanır. Bizim işimiz tefsir yazmak değildir; o heyetin elinde olacak kaynağa bağlı altyapıyı kurmaktır. Yapay zekânın ürettiği hiçbir şey (taslak, özet, modelin açıklaması) "tefsir" diye anılmaz; müfessirlerin eserleri (Envârü't-Tenzîl) ise gerçek tefsirdir ve öyle anılır (kullanıcının açıklaması, 2026-11-04). Altyapı hüccet üretmez, kimin neyi hangi kanıtla söylediğini kaydeder. Katkı kapısı ilim ve ihtisasa göre açılır, meşrebe göre değil. Yapı: Kur'ân ortak adrestir, hadis her katmandan bağlanır, Risale-i Nur ve İşârât eksendir (veride değil görünümde: araçların sırası, varsayılanlar, talimat), müfessirlerin eserleri kendi metinlerinin sahibidir. Birkaç yıl sürebilir; ölçüt hız değil sağlamlıktır. Plan, hazırlık adımları (H) ve Beyzâvî pilotu (T): `docs/tefsir-altyapi-plani.md`; pilotun değerlendirmesi ve MVP: `docs/tefsir-pilot-degerlendirme.md`. MVP bitti (2026-11-07): metinler, adresleri ve mekanik bağlar üç bağdaştırıcıda yayında. **2026-11-09'da okumayla kurulan ve denetlenen bağlar (denetçi, katkı, heyet akışı) ve tercüme programı donduruldu:** model ilişkiyi metin önündeyken sohbette kuruyor; tercümeyi model damgalı yapar. Güncel yön `PLANLAR.md`.

## Temel ilkeler

- **Her adres veriden gelir, asla tahmin edilmez.** Adres üretemediğimiz metin, adres uydurularak değil, açıkça "adres belirsiz" işaretiyle saklanır.
- **Atıf birimi cümledir.** Paragraflar yalnızca görüntü ve bağlam için tutulur.
  - MCP ↔ model arasında: `Sözler › Onuncu Söz › On iki Hakikat › Dokuzuncu Hakikat › 32. cümle`
  - Model ↔ kullanıcı arasında: `Sözler › Onuncu Söz › On iki Hakikat › Dokuzuncu Hakikat › "Şüphesiz ki bu haşri gösterir…"` (cümlenin ilk kelimeleri)
  - Bir temsil, misal ya da tek bir düşünce aynı bölümde birkaç cümle sürüyorsa ardışık cümleler tek atıfla verilir (en çok 8; paragraf sınırı yok, çünkü paragraflar her yerde anlama göre ayrılmamıştır): `Sözler › Birinci Söz › "Bedevî Arab çöllerinde…" ile başlayan 4 cümle`; MCP ↔ model arasında kimlik `…/c004..c007`, yol `… › 4.–7. cümle`.
- **Risale'de sayfa numarası yoktur.** Risale eserlerinin hiçbir veri dosyasında basılı sayfa bilgisi tutulmaz. Klasik eserlerde (müfessirlerin eserleri, hadis kitapları) asıl adres yine yapısaldır; kaynak verdiyse basılı cilt ve sayfa ikincil bilgi olarak durur (`printed`; kullanıcının kararı, 2026-11-04). Sayfa kimliğe girmez, tahmin edilmez.
- **Metin tek yerde durur.** Mecmualar (Asâ-yı Mûsâ, Zülfikâr…) ana ciltlerdeki metne işaret eden içindekiler listeleridir; yalnızca mecmuaya özgü parçalar mecmuada saklanır.
- **Kaynak web'dir.** Ham yanıtlar bir kez indirilip diske kaydedilir; ayrıştırma her zaman diskten yapılır.

## Kapsam ve kaynaklar

Eserlerin listesi, her birinin kaynağı ve durumu tek yerde tutulur: `src/risale_mcp/catalog/` (koleksiyon başına bir dosya). Her eserin hangi aşamada olduğu `docs/eserler/` kontrol listelerindedir (`risale-kulliyat.md`; `tefsir.md`, `hadis.md`, `klasik.md` (koleksiyon `klasik`, 2026-11-13) üç bölümlü: (a) eklenenler üretilir, (b) eklenmesi çok iyi olacaklar ve (c) aklımızda bulunsun elle tutulur, işaret satırının altı yeniden üretimde korunur); kökteki `ESERLER.md` alanların dizinidir (`uv run python -m risale_mcp.checklist` ile diskten üretilir, elle düzenlenmez). Külliyatın 73 eserinin hepsi ayrıştırıldı (Kızıl İcaz'ın Türkçesi 2026-11-12'de katalogdan çıktı: model tercümesi damgalı yeter). Yerelde olup sunucuda olmayanların listesi `HUSUSI-VERILER.md`'dir (`uv run python -m risale_mcp.local_only`, `build` sonunda da üretilir, elle düzenlenmez).

Genel sunucunun kaynakları (kim, hangi şartla izin verdi: `docs/izinler.md`; yeni izin oraya yazılır):

| Kaynak | Rol | İzin ve notlar |
|---|---|---|
| **erisale.com** | Birincil kaynak: ana ciltler, Eski Said eserleri, Asâ-yı Mûsâ, Sikke, Muvazeneler (27 eser) | e-Risale'yi kaynak gösterdiğimiz sürece kullanım izni var (görüşme, 2026-10-30; sitede belgelerde gösteriliyor). Her bölüm ayrı sayfa; liste `sitemap-tr.xml`'den. Metin sayfaya gömülü RSC verisinde yapısal ağaçtır: blok türleri (`H2`, `H3`, `Paragraph`, `CenteredParagraph`, `HeadingDescription`…), satır içi başlıklar (`Heading`), Arapça (`RTL`, türü âyet/hadis/Arapça, meali `rtl.txn`), hâşiye tam geçtiği yerde (`FootnoteRef` → `Footnote`). `blockIndex` kitap içinde süreklidir; boşluk = eksik bölüm. robots.txt yalnızca `/api/` yolunu yasaklar; yalnızca okuma sayfaları indirilir. |
| **risaleoku.com** (`risaleoku_app`) | Mecmualar (Zülfikâr, Tılsımlar, Sirâcü'n-Nûr, Gençlik ve Hanımlar Rehberi, Küçük Sözler, Fihrist, Âsâr-ı Bediiyye), Nutuk, Makalat ve Âsâr parçaları, Hizbler ve dualar, aslı Arapça eserler, 16 Osmanlıca cilt, Türkçe lügat (A4) | Site sahibi, kazanç olmadığı ve kaynak gösterildiği sürece bütün eserlere izin verdi; diğer dillerdeki Risale tercümeleri de dahil (mütercimlerin izniyle paylaşıyorlar, 2026-11-23; Arapça külliyat E8). Katalog `/api/v1/content/changes`, dosyalar `/f/<sha256>.txt.gz`, meal `|n@` numarasıyla. `uv run python -m risale_mcp.fetch risaleoku [anahtar…]`; ham veri `data/raw/risaleoku_app/`. Biçim `books/risaleoku_app.py` başında. Sayfa başındaki ve Arapçadan sonraki satır cümle ortasında da girintili gelir: paragraf sürer. Sikke'nin ikinci "Husrev'in Bir Fıkrasıdır"ı erisale'de indirilemediği için Sözler Neşriyat baskısından gelir (`soz_stg`, `erisale.SUPPLEMENTS`; yazımı erisale'ye en yakın baskı, alt başlıkta işaretli). Aslı Arapça eserler başlık ağacını ve Türkçeyle paralel kimlikleri `books/outlines/<eser>.json` şablonundan alır, metin kelime çapalarıyla (bir kısmında `printed`: bu baskının başlık satırı, `start`: ilk kelimeleri) yerleşir. Geçişin kayıtları: `docs/risaleoku-gecis-plani.md`. |
| Keşif Yolculukları Risale-i Nur Eğitim Programı | Ta'likat'ın Türkçesi | Ediz Sözüer'in programı; Word dosyası Google Drive'da, Protranslate'in tam tercümesi. Telif bildirimi "asliyetini korumak ve kaynak belirtmek şartıyla" serbest kullanım tanır. |
| **nurpedia.org** (`nurpedia`) | Rumuzat-ı Semaniye'nin metni; hadis işaretleri ve künyeleri (Aşama 14) | Elindeki her şeye izin verdi (2026-11-02). MediaWiki sayfaları; `fetch nurpedia` (metin), `fetch hadis` (hadis sayfaları). |
| Kullanıcının dosyaları (`kullanici`) | Rumuzat-ı Semaniye'nin tabloları | Rumuzat'ın PDF'i (`data/raw/kullanici/<kitap>/<kitap>.pdf`); nurpedia tabloları resim verdiği için yalnız tablolar buradan, kullanıcının kararı ve sorumluluğuyla (2026-11-04). |
| tanzil.net | Kur'ân-ı Kerîm | Arapça metin üç biçimde ve Türkiye Diyanet Vakfı meali, XML (Diyanet İşleri Başkanlığı meali 2026-11-12'de çıkarıldı: Başkanlık yeniden yayına izin vermedi). Metin değiştirilmeden, kaynağı (Tanzil Project) ve bağlantısı belirtilerek kullanılır; mealler yalnızca ticari olmayan kullanım içindir. Meal dosyalarının açıklama satırları XML'de geçersiz `--` taşır; ayrıştırmadan önce atılır. |

- **Yalnız yerelde (`Work.private`):** Badıllı'nın harekeli Mesnevî'si (`el-mesnevi-el-arabi-harekeli`; rasaelalnour Word dosyası, kullanıcının isteği), Sirâcü'n-Nûr'un Hayrat baskısı (`siracun-nur-hayrat`, risale.online, JSON API `/risale-api/fihrist`, `/risale-api/paragraf`; Onikinci Şuâ'ya bağlı raporlar ve müdafaalar başka yerde yok), sonradan yapılmış derlemeler Esasat-ı Nuriye (İttihad, "her hakkı mahfuz") ve Hizmet Rehberi ve Düsturları (Ahmet Koçoğlu, 2018): ikisinde derleyicinin ≈28 bin kelimesi var, müellife mal edilmemeli. `build` iki profil kurar: `kisisel` (hepsi) ve `genel` (private'sız); `deploy.sh` sunucuya ikincisini ve yalnız onun vektörlerini gönderir (`embeddings export-public` → `data/dist/genel/vectors/`); private eserlerin vektörleri stdio kullanımı için yerelde kalır.
- **Bırakılan kaynaklar:** rasaelalnour.com (Hizmet Vakfı izin vermedi; Arapça eserler izin veren risaleoku'ya geçti, yalnız yerel harekeli Mesnevî kaldı, sınır karşılaştırması da oradan), kastamonur.com (sonradan izin verdi, gerekirse yeniden kullanılabilir), Yeni Asya, eski risaleoku sayfaları. Eserleri artık risaleoku'dan gelir; ayrıştırıcıları ve ham verileri karşılaştırma için duruyor. nurpedia.org izin verdi ama henüz bir şey alınmadı. Yeni kaynak eklenecekse önce izin istenir.
- **Osmanlıca (`osmanlica` grubu, dil `os`):** Envar baskısı, eşlenmez, Türkçe kimliklerle paralel değildir (`sozler-osmanlica/011/001`), anlamsal aramaya girmez (Türkçe sonuçları yinelemesin). Eşleme Aşama 19.
- **Fihrist Risalesi** mecmua olarak katalogdadır (`fihrist-risalesi`). **Hizb-i Nurî** Zülfikâr'ın hâtimesidir (`hizb-i-nuri`, müellifin takdimleriyle).
- Bir kaynak kitabı birden çok esere bölünebilir: erisale'nin "İlk Dönem Eserleri" kitabı Divan-ı Harb-i Örfî, Münazarat, Sünuhat vb. eserlere ayrılır. Lemeat (Sözler'in sonu) ve Hakikat Çekirdekleri (Mektubat'ın sonu) ayrı eserdir. Seçim, katalogdaki bölüm slug önekleriyle yapılır.

Ham ve ara veri git'e eklenmez. Denetim kararları (`data/links/reviews/`) insan emeğidir, yeniden üretilemez; ama denetçilerin adları ve kararları açık depoda durmaz (kullanıcının kararı, 2026-11-05): klasör kendi ayrı, yerel git deposundadır (`data/links/reviews/.git`), uzak kopyası özel depo `fatihebrarinan/risale-mcp-denetim`.

## Alanlar, koleksiyonlar, profiller

Sistem yalnız Risale-i Nur için değildir; hadis, tefsir ve ilgili kaynaklar da aynı altyapıya girer. Üç ayrı eksen vardır, klasör bunların yalnızca görünen kısmıdır:

- **Koleksiyon** (`catalog.Collection`): metnin ait olduğu yer; değeri `data/library/` altındaki yoldur. `risale/kulliyat` Bediüzzaman'ın eserleri ve mecmuaları, `risale/ilgili` külliyat dışı kaynaklar (Sorularla Risale, mufassal tarihçeler, hatıralar; henüz boş). Kur'ân `library/kuran/` altında ayrı katmandır, atıf birimi âyettir, eser kaydı tutulmaz.
- **Metnin sahibi** (`catalog.Authority`, `Work.authority`): `muellif`, `derleme`, `baskasi`, `nakil`, `serh`, `modern`; eserin kendi yazarına (`Work.author`) göre okunur, kişiler `translator`, `editor`, `compiler` alanlarındadır (H2). Müellifin olmayan metinde araçlar `authority` döndürür, talimat onu müellife mal etmeyi yasaklar. "Üstad dedi ki" diyen hatıra müellifin metni değil, anlatanın aktarmasıdır. Eser düzeyindedir. Tercüme asıl sahibinin eseri sayılır (`muellif`), `Work.translation` ile işaretlenir ve araçlarda `translation: true` döner; mütercim `note`'tadır. Şerh gibi eser içi katmanlar ve eserin içindeki tercüme bölümleri (Arapça Mesnevî'nin Nokta'sı) ayrıca işaretlidir.
- **Profil** (`profiles.py`): bir sunucunun hangi koleksiyonlardan kurulduğu; `data/dist/<profil>/` altında tek veritabanı ve vektörler. `kisisel` hepsi ve `private` eserler, `genel` sunucuya gider (`risale-mcp --profile genel`). Alanlar arası bağlar bir arada sorgulanabilsin diye alan başına değil profil başına tek veritabanı vardır. Kur'ân genel sunucuda kalır (`find_ayah` ve âyet bağları ona dayanır). **Hadis ayrı sunucudur** (kullanıcının kararı, 2026-11-03): hadis kitapları `hadis` profiliyle ayrı bir bağlayıcı olur (HA5); risale sunucusu yalnız Risale'ye bağlanan rivayetleri ve bugünkü ince hadis araçlarını taşır, hadis sunucusu olmadan da çalışır. İki sunucunun ortak verisi bağlardır (`data/links/`, HA1).

**Sunucular ve kapsam** (kullanıcının kararı, 2026-11-04): ana sunucu ya da alt sunucu yoktur. Hiyerarşi veridedir (Kur'ân ortak adres, hadis her yerden bağlanır, Risale eksen); sunucular aynı kütüphanenin eşit, birbirinden bağımsız görünümleridir. Üç katman: kütüphane (`data/library/` ve `data/links/`, tek ve ortak), profil (hangi koleksiyonlar hangi lisansla), sunucu (profil + talimat + araç seti + adres). Kural: **her sunucu kendi alanının metnini taşır; başka alanın metnini kopyalamaz, kimlik ve atıf (`display`) verir; Kur'ân her sunucudadır, çünkü ortak adres odur.** Böylece metin tek yerde durur, aynı cümle iki bağlayıcıdan gelmez, her sunucunun lisansı ve talimatı kendinedir; karşılaştırma ad alanlı kimliklerle (`risale:`, `hadis:`, `tefsir:`) ve ortak bağ dosyalarıyla yapılır.

| Sunucu | Kendi metni | Öbür alanlardan |
|---|---|---|
| `risale` (bugünkü, `genel`) | Bediüzzaman'ın eserleri | Kur'ân metni; Risale'den çıkan hadis bağları ve ince hadis araçları |
| `hadis` (HA5) | Hadis kitapları, dereceler | Kur'ân; rivayetin Risale'deki yerleri (kimlik ve atıf) |
| tefsir altyapısı (ileride) | Müfessirlerin eserleri | Kur'ân; bir âyette önce Risale'nin bağları (eksen), kimlik ve atıfla |
| `erisale`, `yeniasya` (ortak derlemler) | Yalnız o ortağın metni | Kur'ân |
| `kisisel` (yerel) | Hepsi | — |

Bedeli: tam deneyim için kullanıcı birden çok bağlayıcı ekler; talimat ve sitedeki kurulum sayfası bunu söyler. Hepsini tek bağlayıcıda toplayan çatı sunucusu kurulmaz (araç listesi ve talimatlar sulanır, lisanslar karışır, dizin başvurusu tek büyük paket olur); gerekirse bu yapı onu engellemez.

Kurallar:

- **Kimlikler değişmez, önek almaz** (`sozler/10/…`); eser kimliği katalogda tektir (`catalog/__init__.py` denetler).
- **İlgili kaynaklar varsayılan aramaya girmez.** Günümüz Türkçesiyle yazıldıkları için anlamsal aramada eski dilli asıl metnin önüne geçerler. `search` ve `semantic_search` süzgeçsiz çağrıda yalnız külliyata bakar; `include_related`, `work` ya da `group` verilirse gelir.
- **Yeni ilgili eser** `catalog/ilgili.py`'deki `ilgili()` ile eklenir: `authority` zorunlu, müellif olamaz, izin `docs/izinler.md`'ye yazılana kadar `private`. Grubu ilk eserle açılır.
- **Yeni alan:** kaynağın izni alınır, koleksiyon `Collection`'a, `catalog/` dosyası ve `checklist.COLLECTION_TITLES` eklenir, profil listeler. Birimi cümle değilse (hadis numarası, âyet) bugünkü eser modeline zorlanmaz, Kur'ân gibi kendi katmanını kurar; hadisin şeması Aşama 14'ün başında belirlenir.
- **Müfessirlerin eserleri (plan, `docs/tefsir-altyapi-plani.md`):** `library/tefsir/` altında durur, her parça âyet aralığını taşır, Kur'ân metnini kopyalamaz (tek istisna: baskının âyet satırı birimin başında görüntü için durur, cümle sayılmaz, adresi âyetin kendisidir; kullanıcının kararı, 2026-11-04), baskı kaydı ve lisansıyla gelir. Âyet kimliği ortak adres olduğu için eserler birbirine ve Risale'ye âyet üzerinden bulunur, ama ortak âyet bağ değildir: ilişki (aynı söz, nakil, aynı görüş, farklı görüş, itiraz) türü, kanıtı ve denetimiyle bağ dosyasına yazılır. Risale bir âyette önce gelir; bu sıralamadır, verinin hükmü değil. Risale'nin bir yeri yine "tefsir" diye anılmaz (bkz. Âyet ilişkileri). Pilot: Beyzâvî'nin Envârü't-Tenzîl'i, İşârât'ın aralığında (Fâtiha, Bakara 1–33).
- **`ayah_links`** ileride genel bir bağ tablosuna dönüşebilir (kaynak, hedef, tür, güç, kanıt, yöntem); ikinci bağ türü (Aşama 14) gelince değerlendirilir. `data/links/` klasörü dosya bazlı ilk bağ gelince açılır.

Ortak derlemler (`erisale`, `yeniasya`) tasarlandı, uygulanmadı: `PLANLAR.md` "Ortak derlemler".

## Teknik tercihler

- Dil: Python 3.11+
- Ortam ve bağımlılıklar: `uv`
- HTTP: standart kütüphane (`urllib`), `sources/http.py` içindeki nazik istemci (istekler arası bekleme, yeniden deneme).
- Veritabanı: SQLite + FTS5 (kelime araması). Anlamsal arama: Voyage `voyage-context-4` vektörleri ayrı dosyada, benzerlik numpy ile (bkz. Anlamsal arama).
- API anahtarları proje klasöründeki `.env` dosyasında (`VOYAGE_API_KEY`, `OPENAI_API_KEY`; git'e eklenmez, `env.py` okur). Her şey ileride bir internet sunucusuna taşınacakmış gibi tasarlanır: sunucuda yalnızca numpy, sağlayıcı SDK'sı yok.
- MCP: resmi Python SDK'sı (`mcp` paketi, FastMCP). Not: `@modelcontextprotocol/sdk` TypeScript paketidir, kullanmıyoruz.
- Test: `pytest` + MCP Inspector + Claude Code'a `claude mcp add` ile bağlayarak elle deneme.
- Platform: Linux Mint.
- PDF: PyMuPDF yalnızca kullanıcının PDF'lerini (Rumuzat'ın tabloları) ayrıştırmada kullanılır.

## Klasör yapısı

```
risale-mcp/
├── site/                  # risalemcp.com (eklentiler; S13.22'de connect.ayinedar.org): index, belgeler, gizlilik, kullanım şartları, en/; talimat.md, chatgpt-talimat.md (proje talimatları; site gösterir, kullanıcı kopyalar)
├── site-ayinedar/         # ayinedar.org, çatı (S13.15.6): ana sayfa, Yenilikler, Çalışmalar, isarat-usul/, belgeler, gizlilik, şartlar, en/, 404; Âyinedâr simgeleri
├── docs/                  # Caddyfile, servis birimleri, dizin başvuruları, izinler.md, telif-tablosu.md, telif-tarihleri-plani.md, izin e-postaları, ozellikler.md, risaleoku-gecis-plani.md, ayet-duzeltmeleri.md
├── scripts/               # deploy.sh (kod, hazır veri, site; auth.db'ye dokunmaz), sunucu.sh (uzak yönetim), chatgpt-paket.sh, ikon.sh
├── packaging/chatgpt/     # OpenAI eklenti paketi
├── data/                  # git'e eklenmez (README.md hariç, her klasörün işi orada; links/reviews/ kendi yerel deposunda)
│   ├── raw/<kaynak>/      # ham yanıtlar, kaynak başına; kullanıcının PDF'leri raw/kullanici/<kitap>/
│   ├── library/           # asıl veri: risale/kulliyat/<eser>.json, risale/ilgili/, kuran/quran.json, hadis/matches.json, lugat/risaleoku-tr.json
│   ├── dist/<profil>/     # kisisel, genel: risale.db ve vectors/ (kisisel/vectors asıl depo, ücretli çıkarılır)
│   ├── manifest/<profil>/ # kabul edilmiş kimlik manifestosu, sürümler, kimlik değişikliği raporları (silinmez: eski sürümlerin tek kaydı)
│   ├── interim/           # erisale/ blokları, review/ kontrol arayüzü (taşınmaz: tarayıcı işaretleri adrese bağlı olabilir), outline/, quran/ayah_check.md, ayah_links/, arabic_kinds/, golden/, search_eval/, tool_snapshot/, chatgpt/
│   ├── logs/, archive/    # günlükler; kullanılmayan eski dosyalar (asama-1/)
│   └── auth.db            # kullanım kaydı, hata ayıklama anahtarı; OAuth kipinde hesaplar (risale.db gibi yeniden kurulmaz)
├── src/risale_mcp/
│   ├── paths, profiles, checklist, env, normalize, headings
│   ├── catalog/           # model.py, kulliyat.py, ilgili.py, permissions.py (izinler.md'nin karşılığı), editions.py (baskı kaydı)
│   ├── fetch.py, build.py, build_db.py, db.py   # indirme, ayrıştırma, veritabanı CLI'ları
│   ├── sentences.py       # cümle bölücü, incipit, atıflar, altın örnekler
│   ├── arabic_kinds.py    # Arapça parçaların türü ve dayanağı, âyet adres düzeltmeleri
│   ├── lugat.py           # lügat (A4): ayrıştırma, kelimenin maddesini bulma, ölçüm
│   ├── quran.py, hadis.py, hadis_adaylar.py, hadis_turkce.py, hadis_rivayet.py, hadis_uyum.py, hadis_okuma.py, hadis_ornek.py, openiti.py, ayah_links.py, search.py, semantic.py, embeddings.py, search_eval.py, tool_snapshot.py
│   ├── library.py, server.py, citations.py, auth.py, golden.py, local_only.py, manifest.py
│   ├── review_ui.py, review_assets/, static/
│   ├── sources/           # site başına indirici (ham kayıt + doğrulama); openiti.py alanlar arası ortak
│   └── books/             # model.py, mecmua.py, telif.py, telif.json, old_names.json, kaynak başına ayrıştırıcı, outlines/, pdf_text.py, rumuzat.py
└── tests/                 # pytest; golden/ altında altın sorular, âyet kararları, arama seti, cümle örnekleri
```

## Veri modeli

Eserlerin iç yapısı düzensizdir: Söz, Makam, Mebhas, Mesele, Nükte, Hakikat, Esas, Lem'a, İşaret, Remiz, Hâşiye, Zeyl, Mektub, Şuâ vb. Bu yüzden **sabit sütunlar yerine esnek bir başlık yolu** kullanılır.

Her eser `Work.book_path` dosyasıdır (`data/library/<koleksiyon>/<eser>.json`) (`uv run python -m risale_mcp.build --all`). `build` sonunda veritabanını da yeniden kurar (`--no-db` ile atlanır).

- Üst alanlar: `work`, `title`, `group`, `language` (`tr` | `ar`), `source`.
- **`outline`**: başlık ağacı, kitap sırasıyla. İlk kayıt eserin kendisidir (kök).
  - `id`, `parent_id`, `title` (basılı başlık), `ref` (`Sözler › Onuncu Söz › On iki Hakikat › Dokuzuncu Hakikat`)
  - isteğe bağlı: `subtitle`, `toc_title` (kaynağın içindekilerdeki adı, farklıysa), `type`, `number`, `heading` (`H1`…`H6` ya da `inline`), `url` (kaynaktaki bölüm sayfası; doğrulama için), `sources` (mecmuada: karşılık gelen ana cilt düğümleri), `written` (telif bilgisi: `date`, `place`, `language`, `estimated`, `status`, `source`, `note`; `books/telif.json`'dan gelir, bkz. Telif tarihleri)
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

### Telif tarihleri (Aşama 13.2)
Asıl liste `books/telif.json`'dur (eser JSON'ları her `build`'de yeniden üretilir), elle düzenlenir; `build` düğümlere `written` yazar, eserde olmayan kimlik kurulumu durdurur. İnceleme tablosu `docs/telif-tablosu.md` (`uv run python -m risale_mcp.books.telif`). Tarih serbest metindir ("1938 veya 1942"). Karar kuralı: eserin kendi künyesi, sonra kastamonur'un ayrıntılı listesi, boşsa Hayrat'ın toplu tarihi; ayrılan kaynak `note`'ta. kastamonur'un listeleri bağımsız değildir (Enstitü ve Sorularla Risale). Kullanıcının kararları: Meyve Risalesi `sualar/11`, Sekizinci Şuâ "1938 veya 1942", "1926 – Barla" kayıtları 1926 kalır (Barla'ya resmî varış 1 Mart 1927 olsa da), Hayrat'ın tarihleri kaynak gösterilerek kullanılır. Karşılaştırma: `docs/telif-tarihleri-plani.md`.

## Veritabanı (Aşama 5)

`uv run python -m risale_mcp.build_db [--profile genel]` komutu profilin koleksiyonlarındaki JSON'lardan `data/dist/<profil>/risale.db`'yi her seferinde sıfırdan kurar (≈17 sn). Asıl kaynak JSON'lardır, veritabanı elle düzenlenmez. Kurulum geçici dosyaya yapılır, sayılar JSON'larla tutmazsa veritabanı yazılmaz. Şemanın açıklaması `db.py`'de, kurulum kuralları `build_db.py`'nin başındadır.

- **Tablolar:** `works` (profildeki bütün eserler, koleksiyon, `authority` ve `translation` ile; JSON'u olmayanlar `built = 0`), `nodes` (`ord`..`last_ord` alt ağaçtır), `node_sources`, `paragraphs` (eşlenmiş mecmua paragrafında `text` NULL), `paragraph_sources`, `sentences`, `arabic` (cümleye bağlı; âyette `sura`, `ayah_start`, `ayah_end`), `sura_names` (veriden öğrenilen yazılışlar ve Kur'ân katmanının 114 Türkçe adı), `notes`, `gaps`, `meta`; Kur'ân katmanı `quran_suras`, `quran_ayahs`, `quran_translators`, `quran_translations`, `ayah_quotes`; âyet ilişkileri `ayah_links`. Arama dizinleri `sentences_fts` ve `nodes_fts` (başlık, alt başlık, içindekiler adı).
- **Kimlikler:** `id` JSON'daki kalıcı kimliktir; `seq` yalnızca bu veritabanında geçerli tamsayı anahtardır ve okuma sırasını verir.
- **Normalizasyon:** Dizin ve sorgu `normalize.search_words` biçimindedir. Şapka, çengel (ş/s, ç/c, ğ/g, ö/o, ü/u), Arapça hareke, kesme ve tatvil yok sayılır; ayrıca **ı = i** sayılır (klavyesiz "isik" → "ışık"). Biçim değişirse `db.NORMALIZATION` artırılır.
- **Sorgu dili** (`search.py`): kelimeler (hepsi geçmeli), `"tam ifade"`, `haşr*` (kelime başı), `OR`, `-kelime` / `NOT`, `NEAR(a b, 5)`. Sıralama BM25'tir; kısa cümleler öne çıkma eğilimindedir.
- **Mecmualar:** Ana cilde eşlenen paragrafların cümlesi yoktur. Bu yüzden aynı cümle aramada iki kez çıkmaz.
- **Âyetler:** İki biçim çözülür: "Bakara Sûresi, 2:255" ve Hayrat'ın "Sûre-i Bakara, 255" biçimi. Sûre adlarının numaraları, veride numarasıyla geçen yazılışlardan öğrenilir. Birden çok âyet sayılmışsa ilk aralık alınır (bkz. `AYAH_FIXES`). `quran.json` varsa her biri Kur'ân metniyle denetlenir (`arabic.ayah_check`) ve işaretsiz alıntılar bulunur (bkz. Kur'ân katmanı).
- **Anlamsal arama** veritabanında değil, ayrı vektör dosyasındadır (bkz. Anlamsal arama); veritabanı yeniden kurulsa da vektörler kaybolmaz.

## Kur'ân katmanı (Aşama 9)

Kur'ân-ı Kerîm Risale eserlerinden ayrı bir katmandır; atıf birimi âyettir ("Bakara Sûresi, 2:255", `›` olmadan; `cite` bu atıfları denetlemez, doğruluğu `get_ayah`'tan gelir). Ayrıntı `quran.py` başındaki açıklamadadır.

```
uv run python -m risale_mcp.fetch quran   # tanzil.net'ten ham veri (bir kez)
uv run python -m risale_mcp.quran         # data/raw/tanzil -> data/library/kuran/quran.json
uv run python -m risale_mcp.build_db      # Kur'ân tabloları, âyet denetimi ve eşleme; rapor data/interim/quran/ayah_check.md
```

- **Metin:** kullanıcıya her zaman harekeli Medine Mushafı hattı (`quran_ayahs.text`) gösterilir (kullanıcının isteği: harekesiz okuyamıyor). İmlâî harekeli metin `text_simple`, harekesiz metin yalnızca eşlemede. **Türk hattı** (risaleoku'nun Kur'ân'ı, `kuran_turk.py` → `data/library/kuran/turk.json`; her âyetin iskeleti Tanzil'le denetlenir, 3 gerçek imlâ farkı) masada, okuma platformunda ve D5 sayfalarında varsayılandır, Medine hattı seçilebilir (kullanıcının kararı, 2026-11-21); yalnız görüntüdür, araçlar ve eşleme Tanzil'e dayanır.
- **Meal:** Türkiye Diyanet Vakfı (Tanzil'den). Diyanet İşleri Başkanlığı meali 2026-11-12'de çıkarıldı (Başkanlık yeniden yayına izin vermedi; kullanıcının kararı: risk alınmaz, Vakıf ayrı kuruluş). Meal art arda âyetleri birlikte tercüme edebilir (Vakıf'ta 20 âyet); bunlar `first_ayah`..`last_ayah` ile işaretlidir, araç `covers_verses` der. Üç meal türü karıştırılmaz: müellifin "Yani" izahı (metin), nâşirin meali (`publisher_translation`), Vakıf meali (`get_ayah`).
- **Sûre adları:** Türkçe 114 ad `quran.SURA_NAMES`'tedir; veride hiç geçmeyen sûreler de adıyla aranır.
- **Harf iskeleti (`quran.skeleton`):** Risale'nin imlâsı Tanzil'inkinden farklıdır. İki metin de iskelete indirilir: hareke ve işaretler, hemze, elif, vav, ye atılır; elif çeşitleri, tâ-i merbûta, Farsça harfler birleştirilir. Alıntı "…" ve "الخ" yerlerinden parçalara bölünür; her parça Osmanî ya da imlâî iskelette aranır.
- **Kaynağın âyetleri denetlenir** (`arabic.ayah_check`): `exact`, `near`, `iktibas` (müellifin uyarlaması, kısaltması ya da tekrarı), `dizgi_suphesi` (potansiyel hatalı, 3 kayıt), `empty`. Kullanıcının kararı: Kur'ân esastır, müellifin sözü değiştirilmez. Yanlış numara ve eksik aralık `arabic_kinds.AYAH_FIXES`'te düzeltilir (metin değil adres); dizgi şüphesi kullanıcıya gösterilmeden metne uygulanmaz (`docs/ayet-duzeltmeleri.md`). Araç `check` ile uyarır.
- **Âyet türü** `arabic_kinds.py`'den gelir (bkz. Dikkat edilecek noktalar). Bütün parça âyetse parça `ayet` olur (Hizbler, aslı Arapça eserlerin ﴿ ﴾ alıntıları); bir dua içinde geçen âyet `ayah_quotes`'ta kalır. Kısa ve birden çok sûrede geçen numaralı âyet ("الٓمٓ﴿١﴾"), bölümde bulunan öbür âyetlerin en az %80'i aynı sûredense o sûrede aranır. Âyet birden çok yerde geçiyorsa numara verilmez.
- **Hizbü'l-Kur'ân'ın sûre sınırları** metindeki Arapça başlıklardan gelir.

## Hadis katmanı (Aşama 14)

Risale'deki hadisler rivayetlerle eşlenir. Ayrıntı `hadis.py` başındadır.

```
uv run python -m risale_mcp.fetch hadis    # data/raw/{sanadset,hadith_api,nurpedia}
uv run python -m risale_mcp.build_db       # hadis parçaları türleriyle
uv run python -m risale_mcp.hadis          # parçalar -> data/library/hadis/matches.json (≈2 dk)
uv run python -m risale_mcp.build_db       # her profil için: eşlemeler veritabanına
uv run python -m risale_mcp.hadis_eval run <ad>  # ölçüm: data/interim/hadis/<ad>.md; donmuş kontrol tests/golden/hadis_control.json
```

Plan, kararlar, bilinen ve olası hatalar: `docs/hadis-plani.md`. Sıra orada. Kaynakçanın âyet ve hadis satırları: `docs/kaynakca-plani.md`; hadis kitapları: `docs/hadis-kitaplari-plani.md`. Lafız farkı adayları `uv run python -m risale_mcp.hadis_adaylar` (≈10 dk, yalnız `data/interim/hadis/adaylar.*`; eşleme değildir). Kitap kaydı `hadis_kitaplar.py`, künye ayrıştırıcı `hadis_kunye.py` (Risale'ye bağlı değiller, `hadis` profili de kullanır; rapor `uv run python -m risale_mcp.hadis_kunye`).

- **Kaynaklar:** eşleme Sanadset 650K (954 kitap, CC BY 4.0, atıf), Hadith API (Kütüb-i Sitte ağırlıklı, Unlicense, beş derlemde âlimlerin dereceleri). Türkçe mealler alınmaz (mütercimleri belli değil). Risaleoku'nun Kütüb-i Sitte'si kullanılmadı: Arapçası %0,9, Türkçe telif eseri gibi. Veritabanına yalnız eşleşen rivayetler girer; ileride `hadis` profili tam derlemi `library/hadis/`'e alır.
- **Hüküm verilmez, kanıt gösterilir** (kullanıcının kararı: hadis âlimi değil, örneklem elle denetlenmedi). Kaynağın işareti değişmez. `arabic.hadith_support` geçiş başınadır: `found`, `partly_found`, `located_chapter` (kısa parça, künyenin anılan bölümünde; kitapta geçmek karşı sınamada kanıt çıkmadı), `read_chapter` (künyenin bölgesinde okumayla bulundu), `cited`, `phrase_found`, `marked`, `unsupported`. `found` kelime sınırı ve en az 5 kelime ister: 4 ve daha az kelimede eşleşme rivayeti kanıtlamaz (`phrase_found`; donmuş kontrolde %20'ye karşı %0,6). Künye kanıtı arabic alanlarından ve nurpedia `Ayet-Hadis Mealleri`nden gelir; nurpedia her şeyin kullanımına izin verdi. Müellif hadisi çoğu yerde kendi ifadesiyle yazar: bulunamamak lafız farkı olabilir. Dorar kullanılmaz (`docs/izinler.md`). "Bulunamadı" hadis değildir demek değildir.
- **Derece:** yalnız Hadith API'nin listesi, âlimin adıyla. Buhârî ve Müslim'de hadis başına derece yok, araç `collection_note` der; model "sahih" diye hüküm vermez.
- **Kitap türü:** Sanadset'te tefsir ve tabakât da var; eşleşme her zaman hadis kitabı değildir. Mevzu ve zayıf rivayet derleyen kitaplar (`hadis.CAUTION_BOOKS`, adından) sonda sıralanır, `book_note` taşır: orada bulunmak "sağlam" demek değildir ("اختلاف امتي رحمة" yalnız böyle kitaplarda).
- **Sınıflandırıcı:** İhyâ hadis kitabı sayılmaz; hurûf-u mukattaa hadis adayı olmaz.
- **Araçlar:** `find_hadith(text)` Arapça sözden Risale'deki yerler, dayanak, künyeler (`cited_in`) ve rivayetler; `get_hadith(id)` rivayetin metni, dereceler, kaynak; `read_section` ve `get_passage` hadis parçasında `hadith_support`.
- **Kaynakçada âyet ve hadis** (`Library.embedded`, `citations.embedded_lines`): `cite` her kaynağın altına alıntının içindeki âyetin adresini ve hadisin nâşir künyesini girintili satır olarak ekler ("  - Hadis: Buharî, Ezân: 148 (doğrulanmadı)"); meal girmez. Not: metin künyedeki kitapta kelimesi kelimesine bulunduysa ya da kısa parça künyenin bölümündeyse notsuz, `partly_found` künyedeki kitapta ise "lafız farkıyla bulundu", künyenin bölgesinde iki kör okuyucu aynı söz dediyse "okumayla bulundu" (kullanıcının kararı, 2026-11-03), öbürleri "doğrulanmadı". Künyenin ham metni `hadis_kunye.parse`'ta künyenin bittiği yerde kesilir.
- **Bağlar** (`links.py`, `links_hadis.py`, `data/links/<alan>/<yöntem>.jsonl`; HA1, `docs/bag-altyapisi-plani.md`): hadis bağları dosyadadır, üreten iş yazar, `build_db` her profilde `links` tablosuna yükler ve hadis tablolarını oradan kurar. Âyet alıntısı, âyet ilişkileri ve eski adlar (`links_kuran.py`) her kurulumda hesaplanır, tabloya yazılır, yerel profil dosyaya döker (`computed`, geri okunmaz). `private` dosya (model okumaları) yalnız yerel profilde. Ters yön: `get_hadith` `linked_in_works`. Doğrulama `uv run python -m risale_mcp.links check`. Sade şema (kullanıcı onayladı, 2026-11-05; `docs/tefsir-pilot-degerlendirme.md` "Bağ şeması"): üç cins kalıcıdır (lafız `quote`, ilişki `relation`, gönderme `reference`), alan çifti yeni cins açmaz, yöntem ve alt tür ayrı görünür; hadis bağlarının hepsi lafız bağıdır (mânen nakil dahil); model okumaları aday durumuyla aynı kayda geçer (Y1.3); konu ortak adrestir, ikili konu bağı kurulmaz.
- **Model okumaları yalnız yerelde** (`hadis_okumalar.py` -> `data/library/hadis/readings.json`, şema 12 `hadith_readings`, `hadith_flags`, `hadith_verdicts`): Adım 3–7 ve 9'un adayları, okumaları, uyarıları. `build_db` yalnız `kisisel` profilde yükler; `find_hadith` `model_readings`, `report_flags`, `verdicts` verir. Hadisçi görmeden genel sunucuya çıkmaz.
- **Hadis kitapları** (`hadis_kutub.py`, `data/library/hadis/kutub/<kitap>.json`, yalnız yerelde): Kütüb-i Sitte ve Muvatta, OpenITI JK baskıları (CC BY-NC-SA 4.0, `fetch hadis` sabit commit'ten indirir): kitap ve bâb ağacı, senet ve metin, Hadith API numarası, basılı cilt ve sayfa (`printed`, üst bilgideki baskının; `source.edition`). Künyenin sayısı bâb (sünenler, Buhârî) ya da kitap içi sıradır (Müslim); `Index.cited` kitaba göre pencereli bölgeyi verir. Künyenin bölgesinde okuma `hadis_bolge.py` (Adım 9): bulunanlar `data/library/hadis/region.json`, iki profilde `hadith_region`; künyesi yalnız anılmış geçişin dayanağı `read_chapter`, `find_hadith` `read_reports`.
- **Sayılar** (Adım 0, ana metin, 359 tekil parça, derlem sonucu): `found` 83, `partly_found` 18, `phrase_found` 41, bulunamayan 142, 10 harften kısa 75. Geçiş başına dayanak ve kontrol: `data/interim/hadis/adim-0.md`. Eşleşmeler elle doğrulanmadı.
- **Âyet dizgi şüphesi** (üç yer, `docs/ayet-duzeltmeleri.md`): metin değişmez, araç uyarır (kullanıcının kararı, 2026-10-30; 2026-11-21'de onaylandı, B5).

## Âyet ilişkileri (Aşama 10)

Risale'nin bir yerinin bir âyetle kurduğu bağ (`ayah_links` tablosu). `build_db` Kur'ân katmanını kurduktan sonra kurallarla çıkarır; ayrıntı `ayah_links.py` başındadır. Bu bağlar **"tefsir" diye anılmaz** (kullanıcının kararı): bir yerin bir âyetin tefsiri olduğu bir hükümdür, kural ise yalnızca metnin âyetle kurduğu bağı bulur; yanlışlıkla tefsir sınıfına alınan bir yan cümle vebal olur.

```
uv run python -m risale_mcp.ayah_links    # data/interim/ayah_links/links.md (hepsi) ve sample-<tur>.md (40'lık örneklem)
```

- **Türler:** `isaret` (âyetin geçtiği cümlede "işâret, remz, nükte, tefsir, mânâ, meâl"), `acilis` (bölümün ilk paragrafı âyet; Besmele sayılmaz), `izah` (âyetin hemen ardından ya da sonraki cümlenin başında müellifin "Yani"si; aslı Arapça eserlerde Türkçe ifade mütercimindir), `dayanak` ("… sırrınca, sırrıyla, fermânıyla"), `risale` (âyetin Risale-i Nur'a işâreti: Şualar › Birinci Şuâ ve başlığında "Risale-i Nur'a işâret" geçen bölümler; ayrı tür, kullanıcının kararı).
- **Kapsam ve güç:** bağ bölümün ilk iki cümlesindeyse ve açılışta bölümün tamamı (`section`), değilse kanıt cümlesi (`sentence`). Bölüm kapsamlılar ve `izah` güçlü, öbürleri zayıf: zayıf ilişki yalnızca bir cümlenin âyete atfıdır, bölümün konusu gibi sunulmaz (kullanıcının "zayıf ilişki" fikri).
- **İlk gözden geçirmeden çıkan kurallar** (kullanıcı, 1. tur): "işâret" gibi kelime âyete en çok 8 Türkçe kelime uzakta olmalı, âyet cümlenin başında değilse (önünde en çok 3 kelime: "İkinci Cümle: …") uzaktaki kelime bağ kurmaz; sûreyi adlandıran âyet ("Sûre‑i وَالتّ۪ينِ", "اِقْرَأْ … Sûresi") zayıf; cifir/ebced cümlesi, âyet başta değilse zayıf; "İşârât-ı Kur'âniye", "İşârâtü'l-İ'câz" risale adı, kanıt değil; mektup eserlerinde yalnız "وَاِنْ مِنْ شَيْءٍ اِلَّا يُسَبِّحُ بِحَمْدِه۪" ile açılış bir açılış ibaresidir, `acilis` değil (Sözler'in Pencereleri öyle değil).
- **Kararlar kilitli:** kullanıcının örneklem kararları denetim kaydındadır (`data/links/reviews/kuran/relation.jsonl`, H5; önceden `tests/golden/ayah_links_review.json`); gerçek veritabanında hepsinin tuttuğu test edilir (`link_reviews check`), yeni örneklem bunları dışarıda bırakır. 1. turun örneklemi saklanmadığı için 5 karar bağın anahtarıyla değil bölüm öneki ve âyetle kayıtlıdır (`match`): 4'ünde iki aday bağ var, 1'inin bağı artık yok; araçlara gitmezler. Kaynakta âyet ile önündeki Arapça ayrı işaretlidir ("فَاسْتَمِعْ اٰيَةَ" `arabi`); tabloda âyetin eserdeki metni ayrı sütundur.
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
| Kızıl İcaz | `kizil-icaz-arabi` | yok (gerek görülmedi, 2026-11-12; model tercümesi damgalı) |
| Ta'likat | `talikat-arabi` | `talikat` (Keşif, Protranslate tercümesi) |
| Hutbe-i Şamiye | `hutbe-i-samiye-arabi`: İhsan Kasım'ın Türkçeden tercümesi (1911 aslı değil) | `hutbe-i-samiye` (erisale) |

- **Şablon:** `books/outlines/<eser>.json` başlık ağacı, kimlikler ve kelime çapaları; ilk çapadan önceki kısım (muhakkikin ön sözü) alınmaz, sondaki ekler de (`risaleoku_app.ENDS_AT`: İşârât'ta "باسمه سبحانه", Mesnevî'de resimler ve Ziriklî'den biyografiler, B10; not olarak işaretli). İşârât'ın Arapçasındaki tek resim satırı (`…/mesele-07/c018`, "img alt=…") yerinde durur: atılırsa bölümün sonraki cümleleri kayar, taslaklar onlara atıf veriyor. Sıra ve yerleşim bu baskıya göredir (Mesnevî'de Nokta Nûr'dan önce).
- **Mesnevî'nin bu baskıdaki farkları:** sınırlar yerel harekeli baskıyla karşılaştırıldı (yalnız sınır bilgisi, metin risaleoku'dan). Remz 20 ve 21 ile `katre/nukte` bu baskıda yok; Mebhas Reşha'da değil Nûr'un içinde geçer; takrizler bu baskıdaki yerindedir (`katre/takriz`, `zerre/takriz`). Habbe, Şemme ve Zeyl-ül Hubab'da kısa İfade-i Meram gövdeden önce gelir, ayıran başlık yoktur: ayrı bölüm açılmaz. Türkçedeki "Nokta" risalesi aslı Türkçedir, İhsan Kasım'ın tercümesi diye işaretlidir; Mukaddime de.
- **Kızıl İcaz:** Ahdarî'nin Süllem'ine hâşiye. `<…>` beyitleri Süllem'indir, `quote` olarak durur, müellifin sözü değildir. Sayfa dipnotları Molla Abdülmecid'in şerhidir: hâşiye gibi cümlesine bağlıdır, `commentator: "Abdülmecid Nursî"` taşır, atfı "› Şerh ›"; müellife mal edilmez. "ديباجة" gibi kaynakta olmayan başlıklar alt başlıkta işaretlidir (Türkçe Ta'likat'ın "Hadd Bâbı" gibi başlıkları da).
- **Ta'likat:** Gelenbevî'nin Burhân'ına hâşiye; iki dilde aynı 11 kimlik (`saykal.TALIKAT_SECTIONS`). Arapçada dipnotlar müellifin hâşiyeleridir, "ع. ب" gibi notlar not. 44 kısa not eski baskıda olup bu baskıda yoktur; izin vermeyen kaynaktan kopyalanmaz.
- **Dipnotlar:** çok satırlı olabilir; sayfanın son notunun işareti sonraki sayfada olabilir. "(المؤلف)" müellifin hâşiyesi, öbürleri muhakkikin notu (`notes`).
- Sunucu talimatı: eserin her katmanı müellifin değildir (tercüme alt başlıkları, Süllem beyitleri, `commentary_by` taşıyan Abdülmecid şerhi).

## Rumuzat-ı Semaniye (nurpedia, tabloları kullanıcının PDF'i)

Kaynak 2026-11-04'te kullanıcının PDF'inden nurpedia.org'a geçti (kullanıcının kararı: izin veren kaynak). Kurallar `books/nurpedia.py` ve `books/nurpedia_html.py` başında; indirme `uv run python -m risale_mcp.fetch nurpedia` (`data/raw/nurpedia/metin/rumuzat-i-semaniye/`, sayfa başına nurpedia sürüm numarası).
- **Metin:** dizin sayfasının dört metin sayfası nurpedia'nın sırasıyla: Yirmi Dokuzuncu Mektub'un Üçüncü, Dördüncü ve Sekizinci Kısmı ve Yirmi Sekizinci Mektub'un Yedinci Mes'elesinden bir parça (`mektub-28-mesele-07`, yeni). Fihrist sayfası alınmaz. Baskısı belirtilmemiş; PDF'ten daha geniş, ayrı bir baskı (5'li dizilerin %42'si ortak).
- **Kimlikler** (kullanıcının kararı: aynı kalır): eski bölümlerin hepsi korunur. Kaynağın tutarsız başlık seviyeleri `LEVEL_FIXES`, ad farkları `ID_FIXES`, nurpedia'da başlığı olmayan tetimme `INSERTED` (alt başlıkta işaretli) ile; yeni baskıda yeri değişen 4 bölüm (`remiz-01/zeyl` → `remiz-02/zeyl`, Beşinci Remzin üç mes'elesi → `maksat/bab-01` altı) takma addır (`aliases` → `node_aliases`, araçlar eskisini yenisine çözer). Yeni bölümler eklendi (125 düğüm; eskiden 73). Cümle numaraları ve metinleri değişti (`data/manifest/*/changes/20261104-*.md`).
- **Tablolar** (kullanıcının kararı ve sorumluluğuyla): nurpedia Yedinci Remz'in tablolarını resim verir (6 sûre, 30 cüz, 6 ek). Resimlerin yerine PDF'in aynı aralıktaki tabloları (20) ve tablo satırı parçaları konur (`source_edition: "pdf"`, `source_id`); yer, resim dizisinin önündeki ve ardındaki paragrafın PDF'teki karşılığıyla bulunur, cüz cetveli ilk cüzünün resminin yerine girer. Dördüncü Kısım'ın tabloları nurpedia'da metin satırıdır, PDF'ten alınmaz. Eski PDF ayrıştırıcısı (`books/rumuzat.py`, glif çözme `books/pdf_text.py`, `rumuzat_glyphs.tsv`) bunun için ve karşılaştırma için durur; eski JSON `data/archive/rumuzat-pdf/`.
- **Hâşiye:** sayfa sonu notları işaretin konumuna bağlanır (30). Kaynağın şablon artığı ("{{Arabi|") atılır, `notes`'ta.
- **Eşleme:** Mektubat'ta (ve Barla Lâhikası, İşârât, Tarihçe'de) da bulunan düz paragraflar oraya eşlenir (75 kayıt); âyet listeleri bu eserde kalır. Arapçanın türü işaretli değil: `arabi`.
- Sayılar: 125 düğüm, 1.557 paragraf, 2.634 cümle.

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

Ayrıştırılan başlık ağacını, metni ve cümle bölmesini elle kontrol etmek içindir. Eser JSON'larını okur.

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
uv run risale-mcp --transport streamable-http --public-url https://<…> --open --profile genel   # açık kip: OAuth yok, herkes sınırlı (genel sunucu)
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
| `list_works(group?)` | Eserler, kimlikleri, grupları, boyutları, telif bilgisi (`written`); metni bulunamayanlar `available: false` |
| `get_outline(section, depth=2)` | Başlık ağacı; her düğümde alt ağacın ana metin cümle sayısı, telif bilgisi (`written`), derinlik sınırında `subsections` |
| `read_section(section, cursor?, max_words=1500)` | Bölümü alt bölümleriyle kitap sırasıyla okur: telif bilgisi (`written`; üst risaleden geliyorsa `section` ile), başlıklar (`ref`; bölümün bağ kurduğu âyetler `linked_verses`), paragraflar (cümle `id` + metin), hâşiyeler (`hasiye_of`), âyet/hadis meal ve kaynağı, eksikler (`gap`). Paragraf sınırında sayfalar, `next_cursor` ile sürer. Mecmuada eşlenmiş paragraf ana cildin cümleleriyle (`canonical`) gelir. Metni başka yerde duran eski adlı bölümde (Otuz Birinci Mektub) `text_elsewhere`. |
| `get_passage(id, context=0)` | Cümle ya da aralık (`…/c010..c015`), `ref` ve `incipit` ile; bağlı hâşiyeler ve âyet mealleri. Bir bölümde en çok 8 cümlelik aralıkta kullanıcıya gösterilecek atıf (`cite_as`: "… ile başlayan N cümle"). Bölümün sonunu aşan aralık son cümlede kesilir (`note`). |
| `search(query, work?, group?, limit=20, offset=0, include_related=false)` | Cümle araması (`search.py` sorgu dili); toplam, eser başına sayı, eşleşen başlıklar. Süzgeçsiz yalnız külliyat |
| `find_sentence(incipit, scope?)` | İlk kelimelerden cümle (işaretsiz; son kelime eksik olabilir) |
| `find_ayah(sura, ayah?)` | Âyetin eserlerde geçtiği cümleler; sûre numarası ya da adı. `via: source` kaynağın işaretlediği, `via: text` Kur'ân metninde bulunan işaretsiz alıntı; `check` kaynağın numarası metinle tutmuyorsa uyarır; tek âyette âyetin kendisi (`quran`) ve âyetle bağ kuran yerler (`links`: tür, güç, kanıt cümlesi; güçlüler önce; denetlenmişse `reviews`: durum, denetçinin gücü, sabit numarası (ad yayımlanmaz), karşıladığı alanlar ya da `competent: false`, tarih, gerekçe; `review_fields`: bağın gerektirdiği ve ehil kabulle karşılanan alanlar) |
| `get_ayah(sura, ayah, end?, context=0)` | Kur'ân'dan âyet ya da aralık (en çok 30): harekeli metin, Vakıf meali (`covers_verses`: birlikte tercüme edilen âyetler), atıf (`ref`), eserlerde kaç kez geçtiği ve kaç yerin bağ kurduğu (`linked_in_works`), Tanzil atfı |
| `find_hadith(text, limit=20)`, `get_hadith(id)` | Hadisin eserlerdeki yerleri, dayanağı (`hadith_support`) ve rivayetleri; rivayetin metni, dereceler, kaynak ve Risale'de bağlı olduğu cümleler (`linked_in_works`, bağlardan) (bkz. Hadis katmanı) |
| (S13.12) | Risale adları dizini `books/risale_adlari.json` ("İhlâs Risalesi" → `lemalar/20`, `lemalar/21`; her kayıt kanıtıyla, sohbet ederken büyür): `search` ve `semantic_search` `named_sections` verir. Bölüm künyesi (`Library.profile`): `get_outline` kökünde ve `read_section`'ın ilk sayfasında `profile` (hâşiye ve âyet sayısı, imzalar: mektubu kim imzalamış) |
| `lookup_word(words)` | Eski kelime ve tamlamaların risaleoku.com lügatındaki maddeleri (`how`: exact, variant, stem; tamlama bulunmazsa kelimeleri `parts`); lügat nâşirindir, talimat (`LUGAT_INSTRUCTIONS`) metin gibi alıntılamayı ve Kaynaklar'a koymayı yasaklar. Yalnız lügatı olan veritabanında (Risale profilleri) |
| `semantic_search(query, work?, group?, limit=10, offset=0, include_related=false)` | Anlamca en yakın cümleler (`similarity`) ve konunun yoğunlaştığı bölümler (`sections`); kavram ve günümüz Türkçesiyle sorular için. Kelime araması (`search`) ayrı kalır. |
| `cite(sources)` | Cevaptan önce bir kez (kaynakça satırlarının altında alıntıdaki âyet ve hadis künyeleri) (gösterilecek her alıntı sözleriyle; sonradan eklenen alıntı için yeniden): dayanılan cümle ya da aralıkların kimlikleri ve alıntılanan sözler (`[{id, quote?}]`, kaynakça sırasıyla). Her biri için tam atıf (`cite_as`), sorun (aralık 8 cümleyi ya da bölümü aşıyor, alıntı o cümlelerde yok: asıl yeriyle, bilinmeyen kimlik) ve cevabın "Kaynaklar" listesi (`bibliography`: "[n] cite_as (kaynak adı)"; kaynak adı izinlerin şartıdır, `permissions.SOURCE_LABELS`: e-Risale, risaleoku.com, OpenITI; hadis sunucusunda da, B11). Önceki `verify_citations(text)` taslağın tamamını alıyordu (bkz. Hız ve token); sonuçtaki `note` (`citations.CITE_NOTE`) kaynakçanın değiştirilmeden kopyalanmasını, eser dışı kaynakların ayrı listede verilmesini söyler (ChatGPT satırları kendisi yazıyordu) |

### Uzaktan erişim
Ayrıntı `auth.py` başındadır.

- **Genel sunucu açık kipte çalışır** (`--open`; OAuth kullanıcının kararıyla 2026-10-29'da askıya alındı: OpenAI portalı OAuth bilgisini görünce "No authentication" seçilse de ısrar ediyordu). OAuth uç noktaları, giriş sayfası ve `sign_in` yoktur; herkes hesapsız ve sınırlıdır (anlamsal arama günde toplam 2.000, istekler dakikada toplam 120; sınır adres başına değil, çünkü claude.ai'nin istekleri Anthropic'in adreslerinden gelir). OAuth kodu ve testleri (kişi başına hesap, `--anonymous`) yerinde durur; ortak derlemler gibi erişimi kısıtlı bir sunucu gerekirse yeniden açılır.
- **Hata ayıklama adresi:** `scripts/sunucu.sh auth debug-url --new` gizli bir `https://mcp.risalemcp.com/mcp/<anahtar>` verir (anahtarın yalnızca özeti saklanır); o adrese gelen istekler `(debug)` kullanıcısıyla, girdileriyle 7 gün kaydedilir ve sınırlara takılmaz. Okuma `scripts/sunucu.sh auth usage --user '(debug)' --params`, kapatma `--revoke`. Anahtar sunucu başınadır (2026-11-07): hadis için `scripts/sunucu.sh auth --server hadis debug-url --new` (`https://hadis.risalemcp.com/mcp/<anahtar>`), tefsir için `scripts/tefsir-sunucu.sh auth debug-url --new` (`tefsir.risalemcp.com`, kayıt o makinede); `usage --only hadis` süzer.
- **Kullanım kaydı:** her MCP isteği zaman, araç, süre ve hata türüyle `usage` tablosuna yazılır, 90 gün tutulur. Parametreler (sorgular, alıntılar) kaydedilmez, IP de: Anthropic'in dizin politikası gereksiz konuşma verisini yasaklar (kullanıcının kararı). Gizlilik politikası (`site/gizlilik.html`) bunları söyler; değişirse orası da değişir.
- **Uzak sunucu:** Hetzner Cloud CAX11 (ARM, 4 GB, Helsinki, Ubuntu 24.04), genel IPv4 `95.217.21.105`, Tailscale adı `risale` (`100.108.174.19`; SSH yalnız oradan, anahtar `~/.ssh/risale_hetzner`). Bağlayıcı **`https://mcp.risalemcp.com/mcp`**, tanıtım sitesi `https://risalemcp.com`; ikisini Caddy sunar (`docs/Caddyfile`), sertifika Let's Encrypt. Alan adı Cloudflare'de "DNS only" (proxy uzun MCP bağlantılarını 100 sn'de keser). Servis `risale-mcp` (`docs/risale-mcp.server.service`). Güvenlik duvarı: 80, 443; SSH yalnız `tailscale0`.
- **Deploy'dan önce araç çıktısı kaydı** (kullanıcının kuralı, 2026-11-04; `--code` dahil): `deploy.sh` bunu kendisi yapar: veri gidecekse `manifest release`, sonra `tool_snapshot record aday-<zaman>` ve son `yayin-*` kaydıyla `compare`; beklenmeyen fark varsa hiçbir şey gönderilmez. Beklenen fark `DEPLOY_EXPECT="cite" scripts/deploy.sh` ile bildirilir. Gönderilen kayıt `yayin-<zaman>` olur (ilki `yayin-20261103-141900`: 2026-11-03'te deploy edilen hâl). **İstisna `--sohbet`** (kullanıcının kararı, 2026-11-26): yalnız sohbet sayfasının dosyaları gider (≈10 sn), yalnız `risale-sohbet` yeniden başlar, kayıt alınmaz; sunucudakinden farklı dosyalardan biri sohbetin dışında çalışan koddaysa (src/ altında sohbet olmayan, `pyproject.toml`, `uv.lock`, servis birimleri, Caddyfile) betik durur ve `--code` ister.
- **Güncelleme:** `scripts/deploy.sh` (kod, `genel` profilinin veritabanı ve vektörleri, `quran.json`, `.env`'den yalnız `VOYAGE_API_KEY`), yalnız kod ve site için `--code`. Ayrıştırma ve veritabanı kurulumu yerelde yapılır. `data/auth.db`'nin asıl kopyası sunucudadır, deploy ona dokunmaz. Yönetim: `scripts/sunucu.sh auth …`, `status|restart|logs|ssh`.
- **Âyinedâr (S13.15, 2026-11-26):** projelerin çatısı `ayinedar.org` (asıl; `www.` ve `ayinedar.com` 301 ile oraya), alt alan adları işlevli ve İngilizce: `chat.` (sohbet), `read.` (okuma platformu), `lab.` (ar-ge masası), `connect.` (eklentilerin tanıtımı); `mcp.` ayrılmış, `ai.` kullanılmaz. Ad yalnız ayarlarda ve metinde durur, adrese girmez. **Tanıtımın ölçüsü** "eserlerin ne dediğini yansıtır"dır; "Kur'ân'ın âyinedârı" denmez (eserlerde Risale-i Nur'a verilen vasıf yapay zekâya verilmez); metinlerde "marka" denmez, ad bir hizmetin adıdır (marka başvurusu yapılmaz). İç proje adı eser ya da bölüm adıyla çakışmaz, müellife ya da eserine verilmiş bir vasıf değildir, yapay zekânın ürününe hüküm yüklemez ("Miftah", "Habbe" bu yüzden düştü); okuyucu tek ad ve işlev görür ("Âyinedâr · Sohbet"). **Okuma platformu ve masa (S13.15.5, 2026-11-27):** `read.ayinedar.org` (diskte `/var/www/ozel/taslak/oku/`) ve `lab.ayinedar.org` (`/var/www/ozel/taslak/`); giriş servisi ikisinde aynı yolları verir (`/giris`, `/cikis`, `/ben`, `/api/…`; davet `read.ayinedar.org/davet/<jeton>`), bölümü Caddy'nin `X-Bolum` başlığı söyler, masaya yalnız `masa` kapsamı girer; çerez alan adına bağlı (masa hesabı iki yere ayrı girer); eski sayfaların `/taslak/…` yolları iki alan adında da çalışır (önek atılır); `risalemcp.com/oku/*` ve `/taslak/*` 308 ile aynı yola. DNS Cloudflare'de "DNS only", alt alan adları CNAME ile köke; aynı makinenin Caddy'si sunar (`site-ayinedar/` → `/var/www/ayinedar`). Simge kemerli aynada kırmızı kapaklı kitap: asılları `site-ayinedar/icon*.svg`, boyutları `scripts/ikon-ayinedar.sh` üretir (eklentilerinkiler ayrı, `scripts/ikon.sh`). Eklentilerin MCP adresleri ve risalemcp.com kökünün favicon'u yerinde kalır. **Çatı (S13.15.6, 2026-11-27):** `ayinedar.org` arama motorlarına açık (sohbetin tanıtımlı sayfaları da: kanonik kök, JSON-LD, `robots.txt` ve `sitemap.xml` uygulamada); ana sayfa önce sohbete çağırır, örnek cevabı sohbetten kısaltılmadan ve düzeltilmeden (alıntıları veritabanıyla denetlendi), sonra projeler. Yenilikler, Çalışmalar ve usul özeti çatıdadır (`site-uret.py` iki siteyi kurar: yazılar `site-ayinedar/`'a, `style.css`, `site.js` ve Naskh `site/`'tan kopyalanır, çatıya özgüsü `ayinedar.css`; yazıdaki eklenti sayfası bağlantısı risalemcp.com'a tam adres olur); risalemcp.com'daki eski adresleri Caddy 308 ile çatıya verir; lab'ın önizlemesi stili çatıdan alır; `connect.` S13.22'ye kadar risalemcp.com'a 302. Paylaşım kartları `scripts/paylasim-ayinedar.py [sohbet] [cati]` (şablonlar `scripts/paylasim-*.html`). Taşınma sırası `PLANLAR.md` › S13.15 ve S13.22 (eklentilerin `connect.`'e göçü).
- **Logo:** Claude bağlayıcının simgesini Google'ın simge servisinden kök alan adıyla alır (`risalemcp.com`'un favicon'u, 2026-11-16'da görüldü). Logo değişince `icon.svg`'den `icon.png` ve `favicon.ico` üretilir (`scripts/ikon.sh`), `src/risale_mcp/static/` ve `site/` altına konur. Hadis, tefsir ve klasik sunucularının kendi simgesi var (aynı çizim, zemin rengi farklı: `icon-hadis`, `icon-tefsir`, `icon-klasik`; S4.6); her biri kendi alt alan adında verir, sunucu başlıkları ve dizin adları "Risale-i Nur Library", "Hadith Library", "Tafsir Library", "Classical Islamic Library" (`server.RISALE_TITLE`, `VARIANTS`; kullanıcının kararı, 2026-11-22; proje ve yayıncı adı "Risale MCP" kalır). Claude'un arayüzü ise simgeyi Google'ın servisinden kök alan adıyla alır (`s2/favicons?domain=risalemcp.com`): orada dördü de yeşildir, ayrı simge yalnız dizin listelemesinde (portala yüklenen dosya).
- **Dizin başvuruları:** Claude (`docs/dizin-basvurusu.md`) ve OpenAI (`docs/chatgpt-dizin-basvurusu.md`) gönderildi, karar bekleniyor. Yayıncı adı "Nur Hadimleri". Kabul edilirse sitedeki kurulum adımlarına dizinden ekleme yolu açılır (`site/claude.html`'de yorum satırı olarak hazır).
- **Tanıtım sitesi** (kullanıcının kararları): ana sayfa (S2, 2026-11-09) sırasıyla giriş ve ekleme düğmeleri, sayılar, üç eklenti kartı, üç eklentili örnek cevap (claude.ai'den, kısaltılmadan; alıntılar veritabanıyla denetlendi), karşılaştırma, kimin için, neye güvenebilirsiniz, ekleme ve adresler, son yenilikler, kaynaklar; her eklentinin kendi sayfası (`risale.html`, `hadis.html`, `tefsir.html`); menü Eklentiler · Kurulum · Yenilikler · Çalışmalar · Belgeler (Çalışmalar ilk yazı yayımlanınca görünür), gizlilik, şartlar ve "Hata bildirin" (`katki.html`) alt bilgide; Türkçe sayfaların menüsü, alt bilgisi ve `<!-- sayi:… -->` sayıları `scripts/site-uret.py`'den; her platformun kurulumu, proje talimatı, sınama sorusu ve kurulum sorunları kendi sayfasında (`claude.html`, `chatgpt.html`, `en/` karşılıkları; alt alta durmaları kafa karıştırıyordu, 2026-11-05), ana sayfanın eski çapaları (`/#proje`…) `site.js` ile yeni sayfalara gider. Kurulum ekran görüntülerinin asılları `data/raw/kullanici/ekran-goruntuleri/`'ndedir (kişisel bilgi taşıyabilir, siteye konmaz); `python3 scripts/ekran-goruntuleri.py` bulanıklaştırır, kırpar ve `site/img/kurulum/*.webp`'ye yazar. Karşılaştırmadaki cevaplar claude.ai'den alındığı hâliyledir, **kısaltılmaz ve düzeltilmez**; işaretler bizimdir ve veritabanıyla denetlendi. Türkçe sayfalar "eklenti" der (kullanıcının kararı, 2026-11-09; önceden Claude'un arayüzündeki "bağdaştırıcı"); Claude'un menü adları ("Bağdaştırıcılar", "Özel bağdaştırıcı ekle") ve ekran görüntülerinin açıklamaları olduğu gibi kalır, kurulum yerinde "Claude eklentilere 'bağdaştırıcı' diyor" denir. Proje talimatları tek kaynaktan: `site/talimat.md`, `site/chatgpt-talimat.md` ve `en/` karşılıkları. Dışarıya istek yok (gizlilik politikası öyle diyor): yazı tipi Google Fonts'tan yüklenmez. CSS ya da JS değişince sayfalardaki `?v=N` artırılır. **Yenilikler** (S1): yazılar `docs/yenilikler/<tarih>-<ad>.md` (üst bilgi `baslik`, `tarih`, `ozet`, `whatsapp`), `python3 scripts/site-uret.py` yazı sayfalarını, `yenilikler.html`'i, RSS'i, ana sayfadaki son yazı şeridini ve bütün sayfaların Open Graph etiketlerini (`<!-- og -->` arası; paylaşım resmi `site/img/paylasim.png`, `--resim` ile) üretir; `?v=N` betikteki `ASSET_VERSION` ile aynı tutulur. **Çalışmalar** (S9, 2026-11-21): projenin ne denediğini ve ne öğrendiğini anlatan uzun, kaynaklı yazılar, `docs/calismalar/<tarih>-<ad>.md`, aynı betikle (kutu `:::kisa`, tablo, Arapça kendiliğinden sağdan sola ve sitenin Naskh'ıyla `site/fonts/naskh.woff2`, içindekiler, "Bu yazıya atıf"); `adres` üst bilgisi başka betiğin sayfasını listeye koyar (`/isarat-usul/`: `scripts/d1-okur.py`'nin ürettiği usul özeti ve PDF'i; yayımlanınca `noindex`i kalkar). **Yazılar önce taslaktır** (iki türde; kullanıcının kararı): `durum: taslak` siteye çıkmaz, önizlemesi `data/interim/onizleme/` → girişli `lab.ayinedar.org/onizleme/` (masanın girişinde Okumalar › Yazı taslakları, `liste.json`; deploy gönderir; yerelde `python3 scripts/site-uret.py onizle`); kullanıcı okur, düzeltir (S11: masanın Okumalar › Yazı taslakları'ndan web düzenleyici `lab.ayinedar.org/onizleme/duzenle.html#<tür>/<ad>`; her kayıt sürüm, ana sunucuda `data/yazilar.db`, `yazilar.py`; `site-uret.py cek` depoya alır, yayımlama ve zamanlama önce çeker), `python3 scripts/site-uret.py yayinla <tür>/<ad> [--gonder]` yayımlar (tarih ve dosya adı o gün, bağlantı denetimi, Çalışmalar için Yeniliklere duyuru taslağı; `--gonder` yalnız siteyi gönderir: `scripts/deploy.sh --site`, kod gitmez, servis yeniden başlamaz). **Zamanlı yayın:** `site-uret.py zamanla <tür>/<ad> <YYYY-AA-GG | iptal>` üst bilgiye `yayin_tarihi` yazar; bu bilgisayarda `systemd --user` zamanlayıcısı `site-zamanli.timer` (`docs/site-zamanli.{service,timer}`, her sabah 09.00, kapalıysa açılınca) `site-uret.py zamanli --gonder` çalıştırır: günü gelenleri yayımlar, commit eder (push kullanıcıda), siteyi gönderir, masaüstüne haber verir; günlük `journalctl --user -u site-zamanli`. **Ar-ge masası (`lab.ayinedar.org`; S13.15.5'e kadar `risalemcp.com/taslak/`) girişli çalışma bölümüdür** (S5, âyet masası): `site/`'ta değil, `data/d1/masa/<birim>.html` (`scripts/d1-masa.py`; `index.html` son birim) deploy'da `/var/www/ozel/taslak/`'a gider; Caddy `forward_auth` ile `site_auth.py`'ye sorar (servis `risale-taslak`, 127.0.0.1:8009, hesaplar `data/site_auth.db`, MCP hesapları değil; davetle: `scripts/sunucu.sh taslak davet <e-posta> [--masa]`); işaretler tarayıcıda kalır; `site/fonts/amiri-hadis.woff2` bir alt kümedir, genel Arapça metinde kullanılmaz. Yazılar `docs/yenilikler-kilavuzu.md`'ye göre yazılır (kullanıcıya "siz" diye, sade, örnek soruyla, yalnız onu ilgilendireni; "eklenti" denir).
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
- **Taslak hattının uzun işleri (model çağrısı içeren her iş) `scripts/d1-arka.sh baslat <ad> …` ile başlatılır**, Claude Code'un arka plan işi (`run_in_background`) olarak değil (kullanıcının kararı, 2026-11-19): terminal ya da oturum kapansa da sürer. Haber almak için hemen ardından `scripts/d1-arka.sh bekle <ad>` Claude Code'un arka plan işi olarak çalıştırılır; iş bitince bildirim gelir (masaüstüne de düşer). Çok adımlı iş bir dosyaya yazılıp (`data/interim/d1-isler/<ad>.sh`) `bash` ile verilir; iş bitince `data/d1` kendiliğinden commit ve push edilir. Kesintiden sonra `d1-arka.sh yeniden <ad>` (adımlar biteni atlar; taslak yazdırma `--yoksa` ile). Süreç durdurmak için `pkill -f` kullanılmaz (kendi komut satırını eşleştirir); `d1-arka.sh durdur <ad>`. Yeni oturumda önce `scripts/d1-arka.sh liste`: süren ya da biten iş var mı.
- **`data/d1` her adımın sonunda commit ve push edilir** (kullanıcının kararı, 2026-11-19): kendi git deposudur, uzak kopyası özel depo `fatihebrarinan/risale-mcp-taslak`; taslaklar, envanterler ve okumalar yeniden üretilemez. `git -C data/d1 add -A && git -C data/d1 commit -m "…" && git -C data/d1 push`. Sormadan yapılır; ana depoya push kullanıcıdadır.

## Altyapının kalıcı parçaları (H, T, MVP)

Adımların geçmişi `KAYIT.md`'dedir (2026-11-19'a kadar `PLANLAR.md` "Kayıt"); burada her oturumda gereken kısa tarif durur.

- **Araç çıktısı kaydı (H0):** `uv run python -m risale_mcp.tool_snapshot record <ad> [--profile tefsir|hadis]` sabit
  çağrı setini (`tests/golden/tool_calls.json`, `tool_calls_tefsir.json`, `tool_calls_hadis.json`; talimat ve araç
  şemaları dahil) kaydeder, `compare <önceki> <sonraki> [--expect araç…]` fark verir; beklenmeyen farkta çıkış kodu 1.
  Deploy betikleri bunu kendisi yapar (`DEPLOY_EXPECT`, `HADIS_EXPECT`, `TEFSIR_EXPECT`).
- **Kimlik manifestosu (H1):** `manifest.py`; her profil kurulumu cümle kimliklerini ve özetlerini
  `data/manifest/<profil>/accepted.json.gz` ile karşılaştırır; silinen ya da metni değişen cümle, silinen bölüm
  kurulumu durdurur (rapor `changes/`, kasıtlıysa `--accept-id-changes`). `manifest release` sürüm etiketi verir,
  `cite` `corpus_version` taşır. Hadis profilinde birim hadistir (`hadis_db.py`).
- **Eserin yazarı ve baskı (H2, H3):** `Work.author` (varsayılan Bediüzzaman; bilinmiyorsa boş), `translator`,
  `editor`, `compiler`; baskı kaydı `catalog/editions.py`, izin kapısı `catalog/permissions.py` (genel profil izni
  kayıtlı olmayan kaynaktan eser kurmaz; istisna `public_without_record`, yalnız Rumuzat). Hariç tutulan yazarlar
  `catalog/excluded.py` (Abduh, Menâr).
- **Bağlar (H4, H5):** `links.py` (uç: cümle, aralık ya da bölüm; ad alanı koleksiyondan; üç cins `quote`,
  `relation`, `reference`), `data/links/<alan>/<yöntem>.jsonl`, doğrulama `uv run python -m risale_mcp.links check`.
  Denetim kaydı `link_reviews.py`, `data/links/reviews/` (ayrı yerel git, uzak kopya özel depo; denetçi araçlarda
  sabit numarasıyla). Okumayla kurulan ve denetlenen bağlar 2026-11-09'da donduruldu (`PLANLAR.md`); mekanik bağlar
  (âyet birimi, Kur'ân alıntısı, hadis lafzı, âyet ilişkileri) sürer, 94 karar yüklenmeye devam eder.
- **OpenITI (H6):** indirme `sources/openiti.py` (sabit commit), okuma `openiti.py`; `PageV01P003` 3. sayfanın
  sonudur, son işaretten sonraki metnin sayfası bilinmez, tahmin edilmez.
- **Tefsir:** 13 müfessir `data/library/tefsir/` (Beyzâvî `books/beyzavi.py`; öbürleri `books/tefsir_openiti.py`:
  metin Shamela'dan, âyet sınırları altafsir sürümünden, ön metinler `FRONT`, muhakkik girişleri ayrı katman).
  Bağlar `uv run python -m risale_mcp.links_tefsir --mvp` (≈77 dk; âyet birimi ve Kur'ân alıntısı). Profil `tefsir`;
  `find_ayah` müfessirleri vefat sırasıyla verir (`catalog/tefsir.DIED`), Risale'nin yerlerini önce, metinsiz,
  atıfla (`risale_refs`).
- **Hadis kütüphanesi:** Kütüb-i Sitte ve Muvatta `hadis_kutub.py`; Müsned, Müstedrek ve öbür 9 kitap, eş-Şifâ,
  Delâil `hadis_openiti.py` (Zehebî, Esed, Elbânî katmanları `layers`). Risale'nin hadisleri yalnız kütüphaneyle
  eşlenir (HA2; Sanadset rivayet kaynağı değil). Hadis sunucusunun veritabanı `hadis_db.py` →
  `data/dist/hadis/hadis.db` (`build_db --profile hadis` reddeder), `hadis_library.HadisLibrary`, vektörler
  `hadis_vectors.py` (yalnız metin). Kimlik baskının numarası (`musned/14870`, tekrar `-2`, numarasız kitapta sıra
  `sifa/s00007`). `search_hadith(query?, narrator?)`: `narrator` senette; `ابن`/`بن` dizinde ve sorguda bir.
- **Üç bağdaştırıcı:** `risale` (genel profil) ve `hadis` aynı makinede (`mcp.risalemcp.com/mcp`, `hadis.risalemcp.com/mcp`; servis
  `risale-mcp-hadis`, 127.0.0.1:8001; `scripts/deploy.sh [--code] [--hadis]`); `tefsir` ayrı makinede (`tefsir-mcp`,
  Hetzner CAX21, Falkenstein, Tailscale `100.98.98.62`, servis `risale-mcp-tefsir` :8002; `scripts/tefsir-sunucu.sh
  kur|gonder|auth`), ana makinenin Caddy'si `tefsir.risalemcp.com`'u Tailscale üzerinden yönlendirir. Her eklenti kendi
  alt alan adında (S4.6, 2026-11-16: Claude simgeyi alan adından alır; OpenAI doğrulaması alan adı başına); eski yollar
  (`mcp.risalemcp.com/hadis` …) sürer, sunucu `--extra-host mcp.risalemcp.com` ile ikisini de kabul eder. Talimatlar
  `server.py` (`TEFSIR_INSTRUCTIONS`, `HADIS_INSTRUCTIONS`): üç `cite` `first` alır, başka bağdaştırıcı da
  kullanılırsa tek Kaynaklar listesi; modelin her tercümesi "Yapay zekâ tercümesi:" damgalı; alıntıya hareke
  eklenmez; web'den gelen her şey bu kitapların dışındadır; Risale'nin ne dediği yalnız Risale bağdaştırıcısında
  okunarak söylenir. ChatGPT talimatı ve araç tanımlarını önbelleğe alır: değişince kullanıcı bağdaştırıcıyı yeniler.
- **Klasik eserler (E2):** koleksiyon `klasik` (`catalog/klasik.py`), 1. dilim beş belâgat ve terim eseri
  (Delâilü'l-İ'câz, Esrârü'l-Belâğa, el-Müfredât, Miftâhu'l-Ulûm, et-Ta'rîfât); indirme `fetch klasik`
  (`sources/klasik.py`, sabit commit; anahtar eser kimliğidir, `data/raw/openiti/` ortaktır), ayrıştırma
  `books/klasik_openiti.py` (kurallar başında: kaynağın satırı baskının paragrafı, yalnız sayfa sınırında birleşir;
  cümle ortasına düşmüş "başlık" metne geri katılır; tek beyit `verse` paragrafı, tek cümle; Delâil'de Şâkir'in
  fıkraları düğüm; Müfredât'ta madde kökün ilk harfinden). Profil `klasik` (`data/dist/klasik/`), sunucu
  `KLASIK_INSTRUCTIONS` (tefsirinkiyle aynı araç seti), tefsir makinesinde 8003, `klasik.risalemcp.com/mcp`
  (`PROFIL=klasik scripts/tefsir-sunucu.sh gonder`), çağrı seti `tests/golden/tool_calls_klasik.json`. Kalan dilimler
  ve bekleyenler `docs/eserler/klasik.md` (b), (c).
  **E5 (2026-11-25):** yedi eser daha (Şerhu'l-Mevâkıf, Şerhu'l-Makāsıd, et-Telvîh, el-Fıkhu'l-Ekber, el-Munkız,
  el-Mevâhib, İhyâ); seçim Risale'deki anmalardan (`docs/e5-risalede-anilan-eserler.md`), tanıtım "Risale'nin havale
  ettiği ve dayandığı klasikler". Ayrıştırma `books/klasik_serh.py` (kurallar başında: seri kuralıyla başlık ağacı,
  Mevâkıf'ta Îcî'nin metni katman `authority: metin`, Makāsıd'da bölümler metin içi "قال …" aktarmalarından, Telvîh
  ve İhyâ'da başlıklar başka sürümden ilk kelime eşleştirmesiyle, İhyâ'da Irâkî'nin tahrici şerh `commentator`).
  Risale'nin eseri andığı yerler `catalog/klasik.RISALE_REFS` (elle, onaylı; yalnız müellifin sözü, türüyle: havale,
  nakil, değerlendirme; adıyla anılmayan `RISALE_UNNAMED`), `build_db` klasik profilde `work_refs` (atıf genel
  veritabanından), `list_works` `risale_refs`; İhyâ künyeli Risale hadislerine lafız bağı `risale_quotes` (her
  kurulumda hesaplanır), İhyâ cümlesinde `in_risale`. Telvîh'in yayımlanan kimlikleri altı kelimelik eşleştirmeyle
  kuruldu: ayarı değişirse cümleler kayar (`parse_telvih`).
- **Taslak hattı ve kullanım sınırı:** `scripts/d1-*.py`'nin bütün `claude -p` çağrıları `d1-prova.claude_p`'den geçer
  (önce Haiku yoklamasıyla 5 saatlik pencerenin doluluğu, eşiğin üstündeyse sıfırlanmaya kadar bekleme; sınıra
  takılırsa döküm `basarisiz/`'e, bekleme, yeniden deneme). Bir birimin durumu ve sıradaki adımı
  `uv run python scripts/d1-durum.py [birim]`; okuma sayfası siteye `scripts/taslak-gonder.sh <sayfa>`.
  Uzun işler terminalden bağımsız: `scripts/d1-arka.sh baslat <ad> <komut …>` (`systemd --user` hizmeti `d1-<ad>`,
  `loginctl enable-linger` açık, iş sürerken uyku engellenir; günlük `data/interim/d1-isler/<ad>.log`; `liste`, `log`,
  `durdur`). **D5 sunucuda döner** (kullanıcının kararı, 2026-11-20): tefsir makinesinde ayrı kullanıcı `taslak`
  (`/home/taslak/risale-mcp`), `scripts/taslak-sunucu.sh` (`kur`, `gonder` yalnız kod, `veri` sunucudan sunucuya,
  `ozet` yerelle aynı mı, `giris` aboneliğin anahtarı `~/.claude-token`, `d1` özel depoyu çeker, `calistir <komut>`,
  `durum`). Orada da işler `d1-arka.sh` ile (Nice=10); `data/d1` iki makineden yazılır, koşturucu push'tan önce
  `pull --rebase` yapar. Evden sunucuya bağlantı yavaş: büyük veri evden gönderilmez.
- **D5 hattı (Bakara 34–286):** birimler `data/d1/bolme/bakara/birimler.json` (`d1-prova.d5_units`, D5 kipi: genel
  veritabanlarına bağ, gizlenen yok); tek birim `uv run python scripts/d1-birim.py yaz <birim>` (istem `D5_SURUM`,
  varsayılan h12; taslak, kapı d3, garaz özeti, izah, okuma sayfası `masa/d5-<birim>.html`, kayıt
  `data/d1/d5/bakara.json`), kuyruk sunucuda kalıcı hizmet `d1-kuyruk` (`taslak-sunucu.sh kuyruk-kur` bir kez;
  **`devam`**, **`dur`** (birim bitince), **`hemen-dur`**, **`durum`**). Kuyruk her birimden sonra `data/d1`'i push
  eder, haftalık pencere %90'ı geçince sıfırlanmayı bekler (`esik 1.0`: yalnız o pencere için eşik; %98'de sıfırlanma
  12 saatten yakınsa çağrı bekleyip sürer), alarmları (`d1-birim.alarmlar`) birime yazar; durum sayfası
  `https://lab.ayinedar.org/d5.html`. Sayfaları sunucu kısıtlı anahtarla gönderir (`~/.ssh/site_gonder`, ana
  makinede `rrsync -wo /var/www/ozel/taslak`, yalnız tefsir makinesinden); bildirimler ntfy.sh (konu
  `~taslak/.d5-ntfy`, git'e girmez). Kuyruk sürerken `gonder` kodu `~/kod-bekleyen`'e koyar, sıradaki birimin başında
  geçer. D5 sürerken yerelde `data/d1`'e yazılmaz (önce `git -C data/d1 pull`).
- **Okuma platformu ve ar-ge masası (S7, 2026-11-21):** tek uygulama (`scripts/oku-app.html`), tek veri biçimi (yayın
  dosyası `scripts/d1-yayin.py`: `data/d1/yayin/<sûre>/<birim>/v<k>.json`, değişmez sürümler, içerikten paragraf
  kimliği). `uv run python scripts/oku-veri.py [--birim <b>] [--gonder]` platformu (`data/interim/oku/` →
  `/var/www/ozel/taslak/oku/`, `read.ayinedar.org`'un kökü) kurar. **Masanın birim sayfası eski âyet masasıdır**
  (`scripts/d1-masa.py` + `d1-masa-sablon.html`; S7b–S7d, kullanıcının kararları 2026-11-21): tek kabuk
  `ayet.html` (modül; birimin verisi açılınca `masa-veri/<b>.json`'dan yüklenir, adres `#/<b>`; birimsiz giriş sayfası),
  Kur'ân paneli sûrelere göre bütün âyetlerle (Fâtiha 7 birim: İşârât'ın lafız bölümleri âyetlerine `d1-masa.FATIHA`;
  Bakara 176), en çok 6 yan ve her yanda içindekiler ağacı, lafız ve düzey süzgeci, katmanlar bugünkü hatta göre
  (Kalite kapısı yazarın cevabıyla ve son taslağa taşınmış, Nisbet, İşârât karşılaştırması, eski D9 eleştirmeni);
  taslaksız birimde yalnız kaynaklar. Bütün çıktı yeniden üretilir: `data/interim/oku-masa/` (`ayet.html`,
  `masa-veri/`, `masa-birimler.json`, giriş `index.html`/`pano.json`, deneyler defteri) → `/var/www/ozel/taslak/`;
  `data/d1/masa/`'da yalnız okuma ve D5 sayfaları, eski `<b>.html` yönlendirmedir. Hepsini kurmak
  `uv run python scripts/d1-masa.py --hepsi` (≈25 dk; sunucuda `d1-arka.sh`). D5 kuyruğu her birimden sonra `d1-masa.py <b>` ve
  `oku-veri.py --birim <b> --gonder` çalıştırır. Platformda yalnız son taslak, masada hepsi;
  ar-ge birimlerinde platforma giden taslak `data/d1/oku/secim.json` (yoksa en sonuncu). Hesaplar `site_auth.py`:
  kapsam `oku` (varsayılan, yalnız platform) ya da `masa` (masa ve platform); hesap **davet bağlantısıyla** açılır
  (S10): `scripts/sunucu.sh taslak davet <e-posta> [--masa]` tek kullanımlık, 7 günlük bağlantı verir, kullanıcı kendi
  e-postasıyla gönderir, okuyucu parolasını kendisi koyar (unutursa yeni bağlantı; `davetler` bekleyenler); **açık
  davet** `davet --acik [--not <not>]`: adresi okuyucu yazar, yalnız yeni hesap açar (var olan hesabı reddeder), e-posta
  doğrulanmaz (yalnız giriş adı, site e-posta göndermez); `--not` yöneticinin hesabı tanıma notudur (`users` gösterir,
  `set-label`); çerez `/` yolunda. Okuyucu notu **kişisel defterdir** (`masa.py`, `kapsam = 'defter'`): herkes, yönetici de, yalnız kendi notunu
  görür, düzenler, gerçekten siler; dışa aktarıma ve "notlarımla düzelt"e girmez; Notlarım ve Word dosyası
  (`docx_yaz.py`). S10'dan önceki notlar ar-ge kaydıdır (`arge`; masa `?arge=1`); "notlarımla düzelt" yalnız onlarla, elle:
  `uv run python scripts/d1-birim.py notlarla <birim> [--deneme]`. Platform: karşılama (`#/~hosgeldin`), Notlarım
  (`#/~notlarim`), kopyalamada damga, kaldığı yer hesapta (`/api/yer`). Gizlilik politikası bunları anlatır;
  saklanan değişirse orası da değişir. Masanın girişi
  `scripts/masa-giris.py` (Pano · Okumalar · Birimler), deneyler defteri `scripts/deneyler.py` (sürümler, deneyler,
  alet ayarı, kayma, arama); ikisi her D5 biriminden sonra yenilenir. Okumalar yalnız ar-ge içindir, onay değildir:
  kuyruk okuma görevi açmaz (2026-11-21). `/var/www/ozel/taslak` setgid (`caddy` grubu): sunucunun kısıtlı anahtarla
  gönderdiği dosyalar Caddy'ye okunur kalır.
- **Lügat (A4, 2026-11-23):** risaleoku.com'un Türkçe lügatı (≈39 bin madde, sürüm 41). İndirme
  `uv run python -m risale_mcp.fetch lugat` (`data/raw/risaleoku_app/lugat-tr/`, dosyalar sıra numarasıyla, adları
  manifestoda), ayrıştırma `uv run python -m risale_mcp.lugat build` → `data/library/lugat/risaleoku-tr.json`,
  `build_db` Risale profillerinde `lugat` tablosuna yükler (şema sürümü artmadı; tablo yoksa araç yok). Eşleme kuralları
  `lugat.py` başında: anahtar `search_words`, ekler atılır, harf biçimi (`Form`: ş ç ğ ö ü, kesmeler ve ünlüden
  sonraki ı/i: "sâika" sevk eden, "sâıka" yıldırım) tutmayan madde eşlenmez ("bir" bi'r değildir), sesteş Türkçe kelimeler `STOP`. Elle bakmak için `lugat bak <kelime…>`, ölçüm
  `lugat olc` (`data/interim/lugat/olcum.md`). Okuma platformunda kelimeye dokununca anlam: `oku-veri.py` her birim
  için `veri/<birim>.lugat.json` yazar (birimin Türkçe metinlerinde bulunan anahtarlar; genel veritabanından), uygulama
  yalnız dokunulan kelimeyi kapsayan en uzun anahtarı arar (`lugatWords` = `search_words`; `tests/test_lugat.py` node
  ile denetler). Lügat nâşirindir, müellife mal edilmez.
- **Claude eklentisi (plugin, S4.7):** herkese açık depo `github.com/fatihebrarinan/risale-library-plugin` (dört
  bağdaştırıcının adresi ve sekiz İngilizce skill; metin yok). Kaynakları `packaging/claude-plugin/`, ana skill
  `site/en/instructions.md`'den üretilir (talimat değişirse `scripts/claude-plugin.py`'deki değişiklik listesi tutmaz,
  betik durur): `python3 scripts/claude-plugin.py build` (yandaki depoya yazar; commit, push, `version` artırılır),
  `check`, `zip` (claude.ai'ye elle yükleme), `dene [P1 …]` (Claude Code'da soru seti, hangi skill yüklendi; rapor
  `data/interim/claude-plugin/`). claude.ai'de eklentiden yalnız skill'ler ve bağdaştırıcılar çalışır. Yazar adı "Nur Hadimleri" ("Risale MCP" dizinde başka bir ada benziyor); skill açıklamaları çift tırnaklı (betik denetler). Dizine gönderildi (2026-11-23, 1.0.1, auto-publish); yeni sürüm yeniden taranır.
- **Sohbet sayfası (S12, 2026-11-25'te bitti; deneme 5 kişi ve bir hafta, S13.1'den sonra; ayrıntı `KAYIT.md` › S12):**
  **`chat.ayinedar.org`** (S13.15.4, 2026-11-27; adı Âyinedâr; önceki `risalemcp.com/sohbet/*` 308 ile aynı yola
  yönlenir). Yol, site, ad, gönderen, destek adresi ve çatı `SOHBET_PREFIX`, `SOHBET_SITE`, `SOHBET_NAME`,
  `SOHBET_FROM`, `SOHBET_DESTEK`, `SOHBET_CATI` ayarlarından: yayında servis biriminde (`docs/risale-sohbet.service`),
  koddaki varsayılan yerel geliştirmenin `/sohbet/` düzenidir. E-posta `noreply@ayinedar.org` (Scaleway'de doğrulandı;
  Reply-To destek, `destek@ayinedar.org` Cloudflare yönlendirmesiyle); kod e-postasında bağlantı yok (Proton'un süzgeci
  yeni alan adına bağlantıyı reddetti). PWA (manifesto, yalnız çevrimdışı sayfası olan `sw.js`), güvenlik başlıkları
  uygulamada (`sohbet_hesap.SECURITY`, saf ASGI; HSTS Caddy'de), paylaşım kartı `scripts/paylasim-ayinedar.py`, ad
  yazısı Literata alt kümesi (`scripts/literata-alt.py`), Hakkında `/hakkinda`. Claude API ile, yalnız Risale, model Haiku 5.5
  medium (`SOHBET_MODEL`, `SOHBET_EFFORT`; S12.1 ölçümü: `golden run … --model`, yan yana okuma `scripts/s12-karsilastir.py`). Hesaplar `sohbet_hesap.py`:
  davetli bölümden ayrı (`data/sohbet.db`, çerez `sohbet_oturum`), e-posta doğrulama koduyla kayıt ve parola yenileme
  tek akış, sınırlar modülün başında; e-posta Scaleway Transactional Email (AB; `.env` `SCW_SECRET_KEY`,
  `SCW_PROJECT_ID`; kökteki SPF'te `include:_spf.tem.scaleway.com`, MX'ler `destek@` yönlendirmesinindir, dokunulmaz),
  geliştirmede `serve --dev` (e-posta `data/interim/sohbet/eposta.log`'a). Kod sayfası iletinin akıbetini sayfaya özgü jetonla sorar (S13.23.1, `kayit/eposta`,
  `delivery`: teslim süresi ya da teslim edilemeyişin sebebi); son iletilerin teslim süreleri
  `uv run python -m risale_mcp.sohbet_hesap eposta-sure [--n 30]`. API anahtarı `ANTHROPIC_API_KEY`
  (Console'da ayrı çalışma alanı, aylık tavan 100 $); `golden` ölçümü aboneliği kullanır, anahtarı alt sürece geçirmez.
  Sohbet servisi `sohbet.py` (S12.3; kuralları modülün başında): araçlar süreç içinde `create_server`'dan, talimat
  Risale talimatından türetilir; model `[[kimlik]]` yazar, Kaynaklar'ı sunucu kurar, alıntıyı denetler ve tutmayanı kendisi düzeltir (S12.9: başka yerde bulunan alıntıya taşır, bulunmayanı "doğrulanamadı" diye gösterir; model turu `SOHBET_MODEL_FIX`; S13.16: "…" ile birleşen alıntının tutmayan parçası metindeki karşılığıyla değişir ya da atılır, dört kelimelik ve üstü işaretsiz tırnaklı söz aranır: bulunursa işaret alır, okunan bir cümlede çok yakın karşılığı varsa (≥0,8) metnin sözleriyle değişir, bulunmazsa "⚠ eserlerde bu sözlerle bulunamadı"; dili belli olmayan soru Türkçe cevaplanır). Komutlar
  `uv run --extra sohbet python -m risale_mcp.sohbet serve [--dev] | sor "<soru>" | olc [soru…] | usage`; `olc`
  altın soruları API'den sorar, raporu `golden.report` kurar (gerçek maliyet); `olc --hizli` 8 soruluk hızlı set
  (her değişiklikte), 29 soru model ya da talimat değişince ve deploy'dan önce. Hata ayıklama turu (S13.11) `… sohbet dene tests/golden/sohbet_konusmalar/tur-NN.txt [ad …]`: çok turlu konuşmaları yerelde sorar, her turun araç girdisi ve sonucuyla `data/interim/sohbet/dene/`'ye döker (model `SOHBET_MODEL` ile). **Kipler (S13.12, `docs/kipler-plani.md`; okuyucuya görünen adı "mod", kullanıcının kararı 2026-11-27):** kip kaydı `kipler.py` (tek kaynak: ileride MCP hazır komutları ve skill'ler de buradan); okuyucu soru kutusunun üstünden seçer (Serbest soru, Konu taraması), tur `turns.mode`'a yazılır. Konu taramasında model `survey(topic, terms)` çağırır: dosyayı sunucu kurar (`dosya.py`: ad dizini, başlık, kelime başı, anlamsal; risale düzeyinde adaylar, `why`, `focus`, `signed`), cevaptan sonra anılmayan ve konuşmada okunmamış adayları "Konunun geçtiği öbür yerler" diye, kelimelerin geçtiği bütün yerleri sayısıyla kapalı ek (`:::ek`) olarak sunucu ekler (S13.13; `count` sayımdır, aday toplamı değil; Tarihçe'deki kopyalar asıllarına katılır); tarama cevabından sonra kip serbeste döner. `dosya.py` ve `kipler.py` yalnız sohbetindir (`deploy.sh --sohbet` gönderir). **Okuma hataları (S13.14):** okuma araçları okunan cümlelerdeki göndermeleri (`pointers.py`, `points_to`), kısmi sayfanın payını (`coverage`, `of_section`) ve bölüm künyesinde metinden anlaşılmayan olguları (`books/bolum_notlari.json`, kanıtlı; metinde duran bilgi girmez) verir; sohbet her cevabın altına kapalı "Bu cevabın dayandığı okumalar" ekini koyar (kısmen okunan, okunmayan gönderme, okunmadan dayanılan). Ölçüm: `uv run --extra sohbet python -m risale_mcp.okuma_olc run` (set `tests/golden/okuma_seti.json`, elle bulunan hatalardan; hakem Sonnet, `OKUMA_HAKEM`; rapor `data/interim/sohbet/okuma/`); okumayı etkileyen her değişiklikte, tek koşu gürültülüdür. **Öbür kütüphaneler (S13.17):** `kutuphaneler.py`; okuyucu Tefsir, Hadis, Klasik eserler'i açar (varsayılan yalnız Risale; seçim tarayıcıda, turda `turns.libraries`), araçları önekli (`tefsir_find_ayah`; `cite` ve `get_ayah` gitmez), işaret `[[tefsir:…]]`, `[[hadis:…]]`, denetim o kütüphanenin `cite`'ı, Kaynaklar tek liste. Erişim `SOHBET_TEFSIR_URL`, `SOHBET_HADIS_URL`, `SOHBET_KLASIK_URL` (yalnız sunucuda: yereldeki git dışı `.env.sunucu`'da, `deploy.sh` gönderir; MCP sunucusunun iç erişim adresi: `scripts/sunucu.sh auth --server hadis internal-key --new sohbet`, `PROFIL=tefsir|klasik scripts/tefsir-sunucu.sh auth internal-key --new sohbet`; sınırsız, girdisiz kayıt, kullanıcı `(iç:sohbet)`); adres yoksa ve profilin veritabanı makinedeyse süreç içi (yerel). Deneme dosyasında `## ad [kütüphane: tefsir,hadis]`, tek soru `sor … --kutuphane tefsir [--kip ayet]`. Tefsir ve klasik sunucusuna yalnız kod: `scripts/tefsir-sunucu.sh gonder --kod`. **Âyet çalışması kipi (S13.17.3):** `ayet_dosyasi.py` (`verse_file`): Risale'nin bağları ve alıntı yerleri önce, tefsir birimleri vefat sırasıyla, önce okunacaklar âyete düşen kelime payına göre (sabit tefsir yok; `get_outline` kökte `words`); kip tefsiri açar, hadis yalnız okuyucu açarsa; konuşmada işareti geçen kütüphane sonraki sorularda açık kalır. Kapsam ölçümü modelsiz: `uv run --extra sohbet python -m risale_mcp.dosya olc` (anlamsal soru seti; 2026-11-26: ilk 5 aday 40/50, ilk 25 49/50, anlamsal aramanın 5 bölümü 32/50). Sohbetin talimatı kendisinindir,
  kaynağa bağlılığın kuralları `server.py`'deki ortak bloklardan gelir (MCP talimatı bayt bayt aynı kalmalı).
  **Genel sayfa (S14, 2026-11-28'den beri yayında):** `SOHBET_GENEL=1` (servis biriminde; silinirse bugünkü Risale
  sayfası döner): talimat Kur'ân ve Sünnet merkezli (`sohbet.INTRO_GENERAL`, `ORDER_GENERAL`, `FIND_GENERAL`: önce âyet
  ve hadis, sonra açıklayanlar, Risale'ye dair soruda Risale önce, fıkıhta hüküm yok), bütün kütüphaneler varsayılan
  açık (seçim `sohbet:kutuphaneler:genel`), ilk arama `search_all` (anlamca arama bütün açık kütüphanelerde, sonuç
  kütüphane kütüphane), Risale araçları modele `risale_…` adıyla (Kur'ân'ın `get_ayah`'ı öneksiz; içeride bugünkü
  adlar, `internal_name`), yanlış kütüphanenin kimliğine doğru aracı söyleyen ipucu (`wrong_library_hint`), öbür
  kütüphanelerin alıntısında tercüme ve tırnak kalıpları sayfada onarılır (`_foreign_quote_fixes`, `_prefix_foreign`).
  Kipler: "Risale-i Nur'dan" (`risale`: bugünkü talimat, yalnız Risale, testle kilitli), konu taraması genel sayfada
  "Risale-i Nur'da konu taraması" (`Kip.risale_scope`, S14.7'ye kadar). Metinler genel sayfaya göre
  (`sohbet_hesap.HERO_GENERAL`, `general_page()`), örnek konuşma `ornek-konusma-genel.json`. Ölçüm: Risale seti ve genel
  set (`tests/golden/genel_sorular.json`, 26 soru, beklenen yerler araçlarla doğrulandı): `SOHBET_GENEL=1 … sohbet olc
  [--set tests/golden/genel_sorular.json] --kutuphane tefsir,hadis,klasik` (paralel, varsayılan 10; genel setin raporu
  `genel_olc`); örnek üretmek `sohbet ornek --soru … --kutuphane … --cikti …`. Okuyucuya giden Türkçe metinde noktalı
  virgül yok (kullanıcının kararı, 2026-11-28).
  Sayfa (S13.1): solda konuşmalar (geçmiş, "Yeni konuşma", altta ayarlar penceresi: çıkış, saklama, hepsini sil,
  gizlilik ve şartlar, hesabı sil), sağda Kaynaklar (kaynak adı `catalog/permissions.SOURCE_LABELS`); ikisi de açılıp
  kapanır ve genişlikleri aradaki çizgiyle ayarlanır (S13.2), dar ekranda çekmece; ayarlar sekmeli (Hesap, Konuşmalar,
  Görünüm: tema ve yazı boyutu, Belgeler; görünüm ve genişlik tarayıcıda); alt satırda "Tefsir ve fetva değildir, müellife mal edilmez." ve günün kalan hakkı.
  Konuşmalar hesapta (`conversations`, `turns`; `users.keep_history` varsayılan açık, kapalıyken yalnız tarayıcıda);
  yalnız sahibine gösterilir, ekip okumaz; saklanan konuşmanın geçmişi sunucudan okunur; adres `#k/<kimlik>`.
  S13.3: girişsiz açılış hesap oluşturma (tanıtımlı, `sohbet_hesap.HERO`); yeni konuşmada yeteneklerden örnek kartlar;
  beklerken adımlar (`status_line`, `turns.steps`). 👍/👎 geri bildirim
  (`sohbet geri-bildirim`); kota ve bütçe `sohbet.Limits` (kişi günde 10 soru, servis günde 5 $, ayda 100 $, 2 $'da
  ntfy, konu sunucuda `data/sohbet-ntfy`). Yeni konuşma sayfasında ayna figürü (dördünden biri; `scripts/ayna-figur.py` üretir) ve karşılama sözü
  rastgele (S13.23.4); temalar Sistem, Açık, Koyu, Sepya, Zümrüt. İlk girişte rehber (S13.23.6): konuşma listesinin başında salt okunur örnek
  konuşma (`sohbet_assets/ornek-konusma.json`, sistemin gerçek cevabı; yeniden üretmek `… sohbet ornek [--cikti <dosya>]`,
  kullanıcı seçer) ve beş adımlık rehber; görüldüğü `users.tour_seen`'de, yeniden `#tanitim` ya da Ayarlar › Belgeler. Cevap sayfadan bağımsız sürer (B13, `sohbet.Job`): tarayıcı kapansa da biter ve konuşmaya
  yazılır, sayfa `api/sor/devam` ile yeniden bağlanır, servis kapanırken süren cevaplar beklenir; hak yalnız biten
  cevaptan düşer. Arayüz denemesi `uv run --no-project --with playwright python
  scripts/sohbet-arayuz-dene.py` (başsız Brave). Yayında: `deploy.sh` servisi `risale-sohbet` (:8010) kurar, Caddy
  `chat.ayinedar.org`'u tamponsuz ve sıkıştırmasız geçirir (S13.15.6'dan beri arama motorlarına açık), `.env`'den sohbet anahtarlarını da yazar. Kendi gizlilik ve şartlar sayfaları servisin içinde, girişsiz
  (`/gizlilik`, `/sartlar`, `/en/privacy`, `/en/terms`, `/hakkinda`; `sohbet_assets/`,
  `sohbet_hesap.DOCS`, tarih `POLICY_DATE`): sitenin ana politikasına sohbetin verisi girmez (eklentilerinkidir);
  saklanan değişirse bu sayfalar da değişir.
- **Altın sorular üç sunucuda:** `golden run … --servers risale,hadis,tefsir`, elle deneme `golden sandbox
  ~/risale-deneme --servers … --risale-profile genel`. Sunucu kapatılacaksa önce kullanıcıya hatırlatılır.

## Planlar

Bütün planlar, sıra, bekleyen ve dondurulan işler **`PLANLAR.md`**'dedir; başındaki **"Şimdi"** bloğu her adımda güncellenir (önde ne var, kullanıcıdan ne bekleniyor; oturum devri). Adım kaydı (biten işlerin ayrıntısı) **`KAYIT.md`**'dedir. Yeni plan, karar ve biten
adım oraya tarihli yazılır; buraya yalnız kalıcı bağlam (ilke, veri modeli, komut, kural) girer. `docs/` altındaki
plan belgeleri ayrıntı ve geçmiştir. İşler kimlikle anılır: alan harfi (E eserler, S sunum, A araç ve veri, D deneme,
B bakım) ve artan numara (`E2`, alt adım `E2.1`); kimlik değişmez, sıra ayrı tablodadır (`PLANLAR.md` "Adlandırma").
