# Tefsir altyapısı planı

> Güncel plan, durum ve sıra `PLANLAR.md`'dedir (2026-11-09); bu belge ayrıntı ve geçmiştir.

Kullanıcının kararıyla açıldı (2026-11-04). Uzun vadeli bir iştir; birkaç yıl sürebilir. Hız değil sağlamlık
ölçüttür: her adres veriden gelir, her bağın kanıtı ve yöntemi vardır, her karar geri izlenebilir.

## Terimler

- **Bizim işimiz tefsir yazmak değildir; tefsir altyapısı kurmaktır.** Yapay zekânın ürettiği hiçbir şey (taslak,
  özet, karşılaştırma, modelin kendi açıklaması) "tefsir" diye anılmaz; ileride heyete yapay zekâyla taslak
  hazırlansa da (kullanıcının açıklaması, 2026-11-04).
- **Müfessirin eseri:** Beyzâvî'nin Envârü't-Tenzîl'i gibi, kendi adıyla anılan eser. Bunlar gerçek tefsir
  kitaplarıdır, içlerindeki cümleler birer tefsirdir: öyle anılabilir ("Beyzâvî'nin tefsiri", "âyetin Envâr'daki
  tefsiri"). Ayrım şudur: müfessirin sözü tefsirdir, modelin sözü tefsir değildir.
- **Risale-i Nur'un âyetle bağı** ayrı bir karardır (Aşama 10, âyet ilişkileri): kuralla bulunan bir bağ, Risale'nin
  bir yerini bir âyetin tefsiri diye anmaya yetmez; bağ türüyle ve kanıtıyla anılır. İşârâtü'l-İ'câz'ın kendi
  başlıkları ("Âyetin Tefsiri") basıldığı gibi kalır.
- **Me'haz:** müellifin İşârâtü'l-İ'câz ve Risaleler için kullandığı kelime (aşağıda). Altyapının vazifesi, ileride
  bu işi yapacak heyetin elinde en iyi me'haz ve en iyi araç olmaktır.

## Dayanak: metin ne diyor

Plan aşağıdaki cümlelere dayanır; hepsi veritabanından okundu.

- Müellif İşârâtü'l-İ'câz'ı ve Risaleleri ileride yapılacak işin me'hazı olarak gösterir:
  "Belki inşâallâh, şu cüz'‑ü tefsir ve altmış altı aded, belki yüz otuz aded “Sözler” ve “Mektûbat” Risaleleriyle
  beraber me'haz olursa, ileride bahtiyar bir hey'et öyle bir tefsir-i Kur'ânî yazsın, inşâallâh…"
  (`isaratul-icaz/mukaddemat/tenbih/c012`; bir önceki cümle c011 Mektubat'taki "müteferrik hakàik-ı tefsiriye"yi de
  sayar).
- Heyetin vasfı ilim ve ihtisastır: "Muhakkìkîn-i ulemâdan herbiri bir fende mütehassıs, geniş fikre, ince nazara
  mâlik allâmelerden müteşekkil bir hey'et…" (`emirdag-lahikasi/emirdag-lahikasi-2/293/c019`).
- Hüccet bir usulden değil, kabulden doğar: "Eğer cumhûr-u ulemâ onun fehmini kabûl ile başkalara şümûlünü gösterse o
  vakit … hakîki tam tefsir olabilir." (c013); heyet "umumun emniyetine mazhariyetleriyle ve cumhûr-u ulemânın onlara
  i'timâdıyla" icmâ hüccetinin sırrına mazhar olur (c016).
- Ferdin fehmi meşrebinin tesirinden zor kurtulur (c009); bir cemaatin ihlâsla tesânüdü ferdde olmayan bir hassa
  verir (c023–c025).
- Müellif kendi eserini de tefsir diye değil, "tefsirin bazı vücûhuna bir nev'i me'haz olarak" ulemânın nazarına arz
  eder (c039).

Bundan çıkan sınırlar:

1. **Altyapı hüccet üretmez.** Hiçbir onay süreci, oy ya da puan bir yoruma "kabul edilmiş" vasfı vermez; altyapı
   yalnızca kimin neyi, hangi kanıtla, ne zaman söylediğini kaydeder.
2. **Katkı kapısı ilim ve ihtisasa göre açılır** (kullanıcının kararı), meşrebe göre değil. Nur talebesi olmak ne
   şarttır ne engeldir.
3. **Kamuya dönük tarif:** "Kur'ân çalışmaları için kaynağa bağlı altyapı". Projeyi o heyetin kendisi ya da bir
   "dijital şahs-ı manevî" diye sunmak, ihtiyaç duyduğumuz âlimlerin itimadını baştan zedeler.

## Yapı: Kur'ân, hadis ve Risale-i Nur'un yeri

Kullanıcının görüşü: işin me'hazı ve ekseni İşârâtü'l-İ'câz ve Risale-i Nur'dur; Kur'ân ve hadis her yerdedir, en
dışta hepsini kapsayan katmandır; öbür eserler bunun içinde Risale'ye dayanır. Plan bunu şöyle kurar:

| Katman | Veride ne | Görünümde ne |
|---|---|---|
| **Kur'ân** | Ortak adres uzayı: her parça, her bağ âyet kimliğine (`quran:2:255`) bağlanır. Metin tek yerde, kopyalanmaz. | Her şey âyetten açılabilir; âyetin kendisi her zaman gösterilir. |
| **Hadis** | Her katmandan bağlanabilen kaynak katmanı: Risale'nin, Beyzâvî'nin ve öbür eserlerin hadis alıntıları aynı bağ biçimiyle rivayete bağlanır (HA1). Hüküm verilmez, kanıt gösterilir; ayrı sunucu (HA5). | Hadis geçen her yerde dayanağı ve rivayetler. |
| **Risale-i Nur ve İşârâtü'l-İ'câz** | Öbür eserler gibi bir eser; metni ve kimlikleri değişmez. | **Eksen:** bir âyette önce Risale'nin söylediği; klasik eserlerin parçaları Risale'den açılan bağlarla ve âyet üzerinden gelir. Talimat ve araç sırası bunu kurar. |
| **Müfessirlerin eserleri** | Kendi metni, kendi kimlikleri, kendi baskı kaydı; her parça âyet aralığını taşır. | Risale'nin ve âyetin yanında, kendi adıyla. |
| **Çalışmalar** (ileride) | Katkıcıların notları, karşılaştırmaları, itirazları: ayrı katman, `authority` müellif olamaz. | Metinden her zaman ayrı ve imzalı. |

Kararlar ve gerekçeleri:

- **Eksen görünümdedir, veride değil.** Beyzâvî (ö. 685/1286) Risale'ye dayanmaz; bağımlılık tersinedir, Risale
  klasik eserlerle konuşur (İşârât Zemahşerî'yi ve Sekkâkî'yi adıyla anar). Veride bir eseri ötekinin altına koymak
  tarihî bir yanlış olur ve klasik metni Risale'nin bakışıyla değiştirmiş gibi gösterir. Bu yüzden veri tarafsızdır
  (her eser kendi metninin sahibidir), "Risale-i Nur me'hazdır" kararı ise sıralamada, araçların varsayılanında ve
  sunucu talimatında durur.
- **Risale her âyete bağlı değildir.** Bugün genel profilde Risale'nin alıntıladığı farklı âyet 2.406'dır (6.236'nın
  ≈%39'u); bağ kurduğu âyet (âyet ilişkileri) 425. Âyetlerin çoğunda eksen boş kalır. Yapı Risale'yi zorunlu bir ara
  halka yaparsa bu âyetler altyapı dışında kalır. Adres Kur'ân'dır; Risale'nin bağı varsa önce o gelir.
- **"Risale'ye dayanmak" bir bağ türüdür.** Klasik bir parçayla Risale'nin bir yeri arasındaki ilişki (aynı söz,
  nakil, aynı görüş, farklı görüş, Risale'nin itirazı) türüyle, kanıtıyla ve kimin kurduğuyla bağ dosyasına yazılır.
  Ortak âyet ortak görüş demek değildir.
- **Ortak âyet bir bağ değildir.** İki eserin aynı âyetin altında durması ilişki sayılmaz; bağ kurulmadıkça "aynı
  şeyi söylüyorlar" denmez.

## Sunucular

Kural ve tablo `CLAUDE.md`'de ("Sunucular ve kapsam", kullanıcının kararı 2026-11-04). Bu plan için sonucu:
müfessirlerin eserleri risale sunucusuna girmez, kendi sunucusunda durur (ileride; pilot yalnız yerelde). O sunucu
Kur'ân'ı taşır; bir âyette önce Risale'nin bağlarını kimlik ve atıfla verir, Risale'nin metnini kopyalamaz. Risale
sunucusunun talimatı ve çıktıları müfessirlerin eserleri yüzünden değişmez.

## Altyapıda neler var, neler eksik

Var (bugünkü sistem):

- Değişmez kimlikler; cümle atıf birimi; atıf denetimi (`cite`).
- Kur'ân katmanı ve âyet kimliği.
- Metnin sahibi (`authority`), tercüme, şerh (`commentator`) ayrımı.
- Bağ kaydı (HA1): kaynak, hedef, tür, ilişki, yöntem, güç, kanıt; `data/links/<alan>/<yöntem>.jsonl`.
- Kaynak ve izin kaydı (`docs/izinler.md`); kullanıcı kararlarının testlere kilitlenmesi (`tests/golden/`); model
  okumalarının yalnız yerelde kalması.

Eksik (önem sırasıyla):

1. **Denetim kaydı.** Her bağın ve ileride her katkının durumu: `proposed`, `reviewed`, `disputed`, `withdrawn`;
   kim (isimli denetçi), ne zaman, gerekçe; itirazlar silinmez. Model önerisi ile insan denetimi her zaman ayrıdır.
   Dosya tabanlı olduğu için git'te gözden geçirilebilir: "pull request" fikrinin veri karşılığı budur. Önce birkaç
   isimli denetçiyle; platform sonra.
2. **Derlem sürümü.** Veritabanı her kurulumda sıfırdan oluşuyor. Yıllar sonra bir atfın hangi metin sürümüne
   dayandığı yeniden üretilebilmeli: `cite` sonucunda sürüm etiketi, yayınlarda dondurulmuş anlık görüntü, sürümler
   arası kimlik değişikliklerinin listesi.
3. **Baskı kaydı.** Müfessirlerin eserlerinde tahkik farkları çoktur: eser düzeyinde baskı, muhakkik, dijital nüsha
   (OpenITI commit'i), lisans.
4. **Müfessir eserinin şeması** (pilotta kesinleşir): parça, âyet aralığı, katman (müellif, muhakkik notu, hâşiye),
   nakledilen görüş ve kime nispet edildiği ("قال ابن عباس", "قيل", "عن الزجاج"). Nispetler eserler arası nakil
   zincirinin altyapısıdır.
5. **Basılı sayfa (karar, 2026-11-04).** Risale'de sayfa yoktur ve kalır. Klasik eserlerde âlimlerin atıf geleneği
   baskı, cilt ve sayfadır: asıl adres yapısaldır (âyet aralığı + parça kimliği), basılı cilt ve sayfa kaynak
   verdiyse ikincil bilgidir (`printed`). Sayfa hiçbir zaman kimliğe girmez, tahmin edilmez.
6. **İzinler.** Klasik metnin kendisi serbest, dijital nüshalar lisanslıdır (OpenITI CC BY-NC-SA 4.0). Türkçe
   eserlerde aslı serbest, sadeleştirilmiş baskı telifli olabilir. Her eserde izin ayrıştırmadan önce gelir.

## Kapsam dışı (bilerek)

- Yeni bir veritabanı yığını (PostgreSQL, vektör veritabanı, grafik veritabanı). SQLite, dosya tabanlı bağlar ve
  numpy yeter; "bilgi grafiği" `links` tablosudur.
- Her esere ayrı MCP sunucusu. Karşılaştırma ortak veritabanı ister; ileride tek bir sunucu, içinde birçok eser
  (hadis sunucusu gibi ayrı bağlayıcı, bağlar ortak).
- Çok model orkestrasyonu. İstemcinin işidir; sunucu modelden bağımsız kalır.
- Kimlik ve ehliyet doğrulamalı geniş katkı platformu. En sona kalır; önce denetim kaydı ve isimli denetçiler.

## Hazırlık: pilottan önce altyapı (H)

Kod incelemesinden (2026-11-04). Her biri bugünkü Risale verisinde yapılır ve sınanır; Beyzâvî gelmeden önce
bitmesi, pilotun yeni bir şey değil yalnız yeni bir eser eklemesini sağlar. Ölçüt her adımda aynıdır: Risale'nin
kimlikleri, sayıları ve araç çıktıları değişmez.

| # | Bugün | İş |
|---|---|---|
| H0 (bitti) | Testler ve altın sorular var, ama araçların cevabının dünküyle aynı kaldığını gösteren bir karşılaştırma yok (HA1'in B3 adımında elle yapıldı). Sunucunun kullanıcıları var; hazırlık adımları onların gördüğünü değiştirmemeli. | **Araç çıktısı karşılaştırması:** sabit bir çağrı seti (≈100: her araçtan, âyet, hadis, mecmua, Arapça eser, hatalı girdi), genel profilde çalışır, çıktılar kaydedilir; her adımdan sonra fark raporu. Fark yalnız adımın beklediği yerde olur (ör. `cite`'ta sürüm alanı); beklenmeyen fark varsa deploy edilmez. H1 verinin, H0 kullanıcının gördüğünün kaymadığını denetler. Komut ve ayrıntı `tool_snapshot.py` başında. |
| H1 (bitti) | Yalnız Sözler'in birkaç düğümünün cümleleri kilitli (`tests/golden/sentences_sozler.json`). Cümle bölücü ortaktır: Arapça nesir için yapılacak bir değişiklik `isaratul-icaz-arabi` ya da `el-mesnevi-el-arabi`'nin numaralarını sessizce kaydırabilir. Veritabanında yalnız `built_at` var; derlem sürümü yok. | **Kimlik manifestosu ve derlem sürümü:** her eserin bütün cümle kimlikleri ve özetleri (`hash`) bir manifestoda; `build` bir öncekiyle karşılaştırır, kayan, silinen ve metni değişen kimlikleri raporlar (kasıtlı değilse durur). Yayına çıkan veritabanına sürüm etiketi; `cite` sonucunda sürüm. Sonraki her adım bununla ölçülür, bu yüzden ilk. |
| H2 (bitti) | `Work` müellifi örtük olarak Bediüzzaman sayar: `Authority.MUELLIF` "müellifin eseri", talimat "the author" der. Eserin yazarı alanı yok; `Group` yalnız Risale gruplarını bilir. | **Eserin yazarı:** `Work.author` (ad, vefat; varsayılan Bediüzzaman), `authority` eserin kendi yazarına göre okunur. Risale için davranış değişmez; talimat değişikliği T6'da. |
| H3 (bitti) | Eser kaynağı yalnız site ve kitap kimliği (`SourceRef`); baskı, muhakkik, lisans `docs/izinler.md`'de düz yazı. | **Baskı kaydı:** eser düzeyinde baskı, muhakkik, dijital nüsha (sabit commit), lisans ve izin satırı. 74 eser için doldurulur; genel profil izni yazılmamış eseri kurmaz (bugün bu kural yalnız `private` ile korunuyor). |
| H4 (bitti) | Bağın kaynağı örtük olarak Risale cümlesi; metinden metne hedef yalnız `risale:`. | **Bağ uçlarının genelleşmesi:** iki uç da herhangi bir eserin cümlesi ya da bölümü olabilir; ad alanı koleksiyondan (`risale:`, ileride `tefsir:`). Metinden metne ilişki türleri için yer açılır (aynı söz, nakil, aynı görüş, farklı görüş, itiraz); türlerin kendisi T5'te okumayla kesinleşir. |
| H5 (bitti) | Denetim kararları tek bir test dosyasında (`tests/golden/ayah_links_review.json`, 62 âyet ilişkisi kararı); bağlar her kurulumda yeniden üretildiği için karar bağın içine yazılamaz. | **Denetim kaydı:** bağlardan ayrı, yalnız eklenen dosyalar (`data/links/reviews/`): bağın anahtarı (kaynak, hedef, tür, parça), durum (`reviewed`, `disputed`, `withdrawn`), denetçi, tarih, gerekçe. Denetçi listesi isimlidir. İlk veri bugünkü 62 karar (denetçi: kullanıcı); test aynı kararları buradan okur. Araçlar bağın denetim durumunu verir. |
| H6 (bitti) | OpenITI okuyucu hadis kitaplarına gömülü (`hadis_kutub.py`, `sources/hadis.py`); sayfa işaretleri (`PageV01P003`) atılıyor. | **Ortak OpenITI okuyucu:** indirme (sabit commit, üst bilgi), mARkdown ayrıştırma, `@QB@…@QE@` âyet işaretleri ve sayfa işaretinden `printed`. Hadis kitapları da bunu kullanır; HA3'teki Müsned künyeleri (cilt:sayfa) için de gereklidir. |

Önerilen sıra: H0 ve H1, sonra H2–H3 (eser modeli), H4–H5 (bağlar), H6.

H4–H5'in sonucu (2026-11-04): ayrıntı CLAUDE.md'de ve `links.py`, `link_reviews.py` başında. T4'e kalanlar: metin
hedefli bağın `display`'i (bugün yalnız kaynağın atfı var; hedef de başka sunucudaysa iki atıf gerekir), bağ
araçlarının metinden metne bağları göstermesi, denetim kaydına yazan bir araç ya da arayüz (bugün dosyaya elle ya da
`link_reviews.append` ile), denetçinin görünen adı ve seçim ölçütü (Açık sorular). H0 ile H1 en önce gelir, çünkü öbürlerinin
"hiçbir şey kaymadı" ölçütünü onlar verir.

Kullanıcıya dönük güvenceler (kullanıcının kaygısı, 2026-11-04: sunucunun kullanıcı kitlesi oluşuyor):

- Hazırlık adımları kendiliğinden canlıya çıkmaz; deploy kullanıcıdadır ve H0 temiz olmadan yapılmaz.
- H3'ün izin kuralı eseri sessizce düşürmez: kaydı eksik eser kurulumu durdurur; deploy'dan önce eser sayısı
  karşılaştırılır.
- Beyzâvî pilotu `private` kalır: yalnız yerel sunucuda; genel sunucuya sonuçlar görüldükten sonra ayrı kararla.

Kaynak durumu (2026-11-04, yalnız listeleme): OpenITI'de Envârü't-Tenzîl'in beş nüshası var
(`0700AH/data/0685NasirDinBaydawi/0685NasirDinBaydawi.AnwarTanzil`: `JK000128`, `ShamAY0034065`, `Shamela0023588`,
`Shia002637Vols`, `Tafsir01006`), Keşşâf da (`0550AH/data/0538JarAllahZamakhshari.Kashshaf`). Nüsha seçimi T0'dır.

## Pilot: Beyzâvî, İşârâtü'l-İ'câz'ın kapsadığı aralık

İşârât Fâtiha'yı ve Bakara'nın 1–33. âyetlerini işler (39 bölüm, 5.224 cümle). Pilot aynı aralıkta Beyzâvî'nin
Envârü't-Tenzîl'ini alır (kullanıcının seçimi). İkinci eser olarak Zemahşerî'nin Keşşâf'ı düşünülebilir: İşârât onu
adıyla anar, Beyzâvî de büyük ölçüde ondan süzülmüştür.

| # | İş | Çıktı |
|---|---|---|
| T0 (bitti) | Kaynak: Beyzâvî OpenITI'de aranır (baskı, commit, lisans); başka nüsha gerekirse izin istenir | `docs/izinler.md` satırı, ham veri `data/raw/openiti/` |
| T1 | Ham veriyi incelemek: âyet işaretleri, bölümler, hâşiyeler, nakil kalıpları; örnekler kullanıcıya | Örnek dökümü |
| T2 | Kararlar: koleksiyon (`library/tefsir/`), şema, kimlik biçimi | Bu belgenin "Kararlar"ı |
| T3 (bitti) | Ayrıştırıcı ve cümle bölücü (Arapça nesir, el-Mesnevî el-Arabî'nin kuralları) | `data/library/tefsir/beyzavi.json`, altın örnekler |
| T4 (bitti) | Beyzâvî'nin bağları için H4 ve H5'in eksik kalan kısmı | `links.py`, testler |
| T5 (bitti) | Bağlar: Beyzâvî parçası → âyet (yapıdan); Beyzâvî'nin âyet ve hadis alıntıları (bugünkü yöntemler); İşârât bölümü ↔ Beyzâvî parçası (aynı âyet aralığı yalnız aday; ilişki türü okumayla) | `data/links/tefsir/*.jsonl`, sayım ve örneklem |
| T6 (bitti) | Araçlar: âyetten Risale'nin ve Beyzâvî'nin yerleri, Risale önce; talimat ("tefsir" denmez, eserin sahibi söylenir) | Altın sorular |
| T7 (bitti) | Kullanıcı örneklemi denetler; kararlar `tests/golden/`'a kilitlenir | Karar dosyası |

### T0: nüsha (bitti, 2026-11-04)

Beş OpenITI sürümü de sabit commit'ten indirildi (`0700AH` @ `3d8ff4e`, 2025-11-28; `uv run python -m risale_mcp.fetch
tefsir`, `sources/tefsir.py`; ham veri `data/raw/openiti/beyzavi-*.txt`). Özet `uv run python -m risale_mcp.openiti
beyzavi-jk …`. Dördünün `.yml`'si doldurulmamış şablondur; baskı bilgisi yalnız üst bilgidendir.

| Sürüm | Baskı (üst bilgi) | Sayfa | Âyet ayrımı | Not |
|---|---|---|---|---|
| **Shamela0023588** | Maraşlî tahkiki, Dâru İhyâi't-Türâsi'l-Arabî, Beyrut, 1. baskı 1418 | 5 cilt, işaretler neredeyse kesintisiz (cilt başına 0–5 boşluk) | Her âyete başlık: `[سورة البقرة (2) : آية 1]` (bazısı satıra bölünmüş, `</span>` artığı) | Noktalama ve «» var; Kur'ân alıntısı işaretsiz. Başta muhakkikin girişi (≈18 sayfa, 1418): Maraşlî'nin diye işaretli alınır |
| JK000128 | Dâru'l-Fikr, Beyrut, 5 cilt; muhakkik yok | 1/3–5/554, 1. ciltte 18 boşluk; hutbe içinde sayfalar ikişer atlıyor (3→7, 11→13→15): baskıda araya başka metin giriyor olabilir | Yok; `< >` içinde dijitalleştirenin başlıkları ("أسماء السورة") | Tek `@QB@…@QE@` işaretli sürüm (24.813). Noktalama az |
| ShamAY0034065 | Dâru'l-Fikr (Shamela "موافق للمطبوع") | JK ile aynı (1/2–5/554) | Sûre başlıkları | JK'nın aynı baskısı, işaretsiz |
| Shia002637Vols | 5 cilt | JK ile aynı | Yok | 2.559 paragraf: satırlar birleşmiş |
| Tafsir01006 | Yok (altafsir.com) | Yok | En temiz: `[2.1]` başlıkları, lemma `{ }` içinde; Bakara 31–33 tek başlıkta | `.yml`: eksik metin (giriş yok), baskıya dayanmıyor |

**Seçim: Shamela0023588.** Gerekçe: adı bilinen tek tahkikli baskı (baskı kaydı ve `printed` ona dayanır), sayfa
işaretleri tutarlı, her âyetin başlığı var (âyet aralığı yapıdan gelir), noktalama cümle bölmeye elverişli. Kur'ân
alıntıları işaretsiz olduğu için Risale'deki gibi Kur'ân metninde aranır (`quran.skeleton`); JK'nın `@QB@`
işaretleri bu aramanın denetimi olarak kullanılabilir (T1). Muhakkikin girişi alınır (kullanıcının kararı,
2026-11-04), ama müellifin metni değildir: Maraşlî'ye ait olduğu işaretli ayrı bir katman olarak durur, müellife mal
edilmez. Öbür dört sürüm ham veri olarak karşılaştırma için
durur. İzin: OpenITI satırı (CC BY-NC-SA 4.0); klasik metin serbest, tahkik farkları baskı kaydında. Başka kaynaktan
izin gerekmedi. Pilot `private` kalır.

### T1: ham veri incelemesi (2026-11-04)

Döküm `data/interim/tefsir/beyzavi-t1.md` (pilot aralığı: baştan Bakara 33'ün sonuna).

- **Kısımlar:** Maraşlî'nin girişi 300 paragraf, 4.153 kelime (1/5–1/23; kendi dipnot işaretleri «n», dipnotlar
  OpenITI temizliğinde atılmış); müellifin hutbesi 315 kelime (başlığı "خطبة الكتاب" baskının); Fâtiha ve Bakara
  1–33: 39 âyet birimi, 23.853 kelime, 1/25–1/70.
- **Âyet birimleri:** her birimde başlık, âyetin metni ("… (6)") ve şerh. 39 başlığın 30'u satırlara bölünmüş
  (`### |` boş, `</span>` artığı); birleştirince 39'unun da numarası ve âyet satırı Tanzil'le tutuyor, aralıkta boşluk
  ve tekrar yok. Fâtiha 3–4 tek birim.
- **Lemma:** şerh âyetin lafzını işaretsiz tekrar ederek ilerler ("صراط الذين أنعمت عليهم بدل من الأول…"); şerh
  paragraflarının 98'i (446'dan) lemmayla başlıyor, öbürleri paragraf içinde. Lemmanın sonu işaretli değil.
- **Paragraflar:** 407 sınırın 96'sı cümle ortasında, 110'u ":" ya da "»"dan sonra: Shamela'nın biçim kalıntısı
  (hadis ve âyet ayrı `span`'deydi), yazarın paragrafı değil. 13 paragraf ". " ile başlıyor.
- **Kur'ân alıntıları işaretsiz:** JK'nın aynı aralıktaki 424 `@QB@` işaretinden 6 harften uzun 314'ünün 304'ü
  Shamela'nın şerhinde aynı harflerle geçiyor: alıntılar var, Kur'ân metninde aranarak bulunur.
- **«» içinde 31 söz:** hadisler ("كل أمر ذي بال…"), kırâatler ("وغير الضالين"), dilbilgisi alıntıları.
- **Nispet kalıpları:** قيل 87, قوله تعالى 85, قال 44, قرئ/قرأ 38, عليه الصلاة والسلام 23, روي 14, المعتزلة 8,
  عن ابن عباس 4; Zemahşerî ve Keşşâf adıyla hiç anılmıyor.
- **Noktalama:** 848 cümle sonu işareti, ortalama 28 kelimede bir; uzun cümleler "،" ile sürüyor.
- **Sayfa:** aralıkta 62 işaret, 54'ü kendi satırında; girişin başında `PageV00P000` (0/0).
- **Baskılar:** Shamela'nın 5'li kelime dizilerinin %94,5'i JK'da da var (JK'nınkilerin %92'si Shamela'da).

### T2: kararlar (2026-11-04, kullanıcı onayladı)

Kullanıcı T1'in beş önerisini onayladı; tek değişiklik: âyet birimin başında durur. Prototip ve örnek birim
`data/interim/tefsir/beyzavi-t2-ornek.json` (39 birim, 445 ham satır → 240 paragraf, 768 cümle).

1. **Yer ve ad alanı:** yeni koleksiyon `Collection.TEFSIR = "tefsir"` (`data/library/tefsir/beyzavi.json`; ad
   alanı kendiliğinden `tefsir:`, H4). Eser `beyzavi`: kök başlığı "Envârü't-Tenzîl" (Arapça eserler gibi atıf kökü
   Türkçe, alt başlıklar basılı Arapça), `language: ar`, `author` Nâsırüddîn el-Beyzâvî, `editor` Muhammed
   Abdurrahman el-Maraşlî, `authority: muellif`, `private`. Yeni site `Site.OPENITI`, izin satırı OpenITI; baskı kaydı
   üst bilgiden ve commit'ten (`openiti.Document.edition`, H3/H6).
2. **Kapsam:** muhakkikin girişi, hutbe, Fâtiha, Bakara 1–33. Gerisi pilotta ayrıştırılmaz (eserin notunda yazılı).
3. **Başlık ağacı ve kimlikler:**
   - `beyzavi/mukaddime-tahkik`: Maraşlî'nin girişi, ayrı katman (`authority: muhakkik`, `by`: Maraşlî); alt
     başlıkları düğüm olur, "1- …" gibi numaralı liste maddeleri paragraf kalır (ayrıntısı T3'te örnekle).
   - `beyzavi/hutbe`: müellifin hutbesi; başlık ("خطبة الكتاب") baskının, alt başlıkta işaretli.
   - `beyzavi/1`, `beyzavi/2`: sûre düğümleri, başlık basılı hâliyle "سورة الفاتحة" (numarası `verses`'te), baskının diye
     işaretli; sûrenin ilk âyet başlığından önceki metni ("مكية وآيها سبع آيات…") müellifindir, düğümün kendi metnidir.
   - Âyet birimleri `beyzavi/<sûre>/<âyet>` ya da `beyzavi/1/3-4`: başlık basılı hâliyle "آية 6" / "الآيات 3 الى 4",
     `verses: {sura, start, end}`, baskının başlığı diye işaretli. Atıf: "Envârü't-Tenzîl › سورة البقرة › آية 6 › 3. cümle".
4. **Birimin başındaki âyet (kullanıcının kararı):** baskının âyet satırı birimin ilk paragrafıdır, basıldığı gibi
   (`kind: "ayah"`, `verses: "quran:2:6"`). Beyzâvî'nin cümlesi sayılmaz, numarası yoktur: adresi âyetin kendisidir,
   atıf Kur'ân'a gider. "Müfessirin eseri Kur'ân metnini kopyalamaz" kuralının tek istisnası budur: görüntü içindir,
   Kur'ân'ın metni ve adresi yine Kur'ân katmanınındır. Bakara 1'in başındaki besmele satırı da `ayah` paragrafıdır,
   numarasız (sûre başı).
5. **Paragraflar:** paragraf yalnız cümle sonunda (. ؟ !) biter; öbür satırlar bir sonrakine bir boşlukla eklenir,
   noktalamayla başlayan satır (". ولنا") boşluksuz. Satırların içi değişmez. Her paragrafta `printed` (başladığı ve
   bittiği sayfa).
6. **Cümleler:** bugünkü bölücü, kural değişmeden (Arapça nesir: `.` `؟` `!` ardından Arapça harf). Kimlik
   `beyzavi/2/6/c003`; her cümlede `printed`. Uzun cümleler (26'sı 100 kelimeyi aşıyor, en uzunu 203) bölünmez,
   T7 örnekleminde bakılır.
7. **Lemma:** parça sınırı değil; cümle başı biriminin âyet lafzıyla başlıyorsa `lemma` adayı işareti (T5'te üretilir,
   T7'de denetlenir).
8. **Kur'ân alıntıları ve hadisler:** ayrıştırıcı işaretlemez; T5'te bugünkü yöntemlerle (`quran_text`, hadis
   eşlemesi) bağ olarak çıkar, JK'nın `@QB@` işaretleri ölçüm için.
9. **Muhakkikin dipnot işaretleri** («1»): metinde kalır (metin değişmez); dipnotların kaynakta olmadığı eserin
   `notes`'unda.
10. **Ölçüt:** eser `private`, genel profile girmez: genel profilin araç çıktısında fark olmamalı (H0), Risale'nin
   kimlikleri değişmemeli (H1); yerel profilde yalnız eklenen kimlikler.

### T3: ayrıştırıcı (bitti, 2026-11-04)

`books/beyzavi.py`; JSON `data/library/tefsir/beyzavi.json` (yalnız yerel profil). 46 düğüm, 422 paragraf, 40 âyet
satırı, 977 cümle (âyet birimlerinde 767), hepsi basılı sayfalı (1/5–1/70). T2'den ayrılan ya da netleşenler:

- Girişin başlık seviyeleri tutarsız (liste maddeleri, tam cümleler `### |`): alt düğüm yalnız girişin kendi
  içindekiler listesinin iki ana kısmı (`mukaddime-tahkik/1`, `/2`); öbür başlık satırları kendi paragrafını açar.
- `### $` (mARkdown'da kişi ya da madde başlığı) okuyucuya eklendi; hadis kitaplarında yok, onlar değişmedi.
- "[الجزء الاول]" cilt etiketi metne değil `notes`'a.
- Genel profil: araç çıktısında fark yok (`tool_snapshot` t3), kimlik farkı yok. Yerel profil: 977 cümle ve 46
  bölüm eklendi; `build_db`'nin bugünkü parantezli alıntı yöntemi 3 Kur'ân alıntısı buldu (Kıyâme 40, Bakara 11 ve 14).
- T6'ya kalan: `read_section` cümlesi olmayan paragrafın metnini göstermiyor, âyet satırı boş görünüyor; düğümün
  `verses`, `authority` ve `printed` alanları araçlara henüz gitmiyor.

### T4: bağların eksikleri (bitti, 2026-11-04)

H4–H5'ten T4'e kalanlar yapıldı (ayrıntı CLAUDE.md'de ve `links.py`, `link_reviews.py` başında):

- **Hedefin atfı** (`target_display`) ve iki ucun atfını veriden kuran `links.cite_as`; doğrulama hedefin kaymasını
  da yakalar. Şema 18.
- **Sızma koruması:** metin hedefli bağ, hedefin eseri yalnız yerelde duruyorsa o eseri taşımayan profile girmez;
  hedef başka sunucunun alanındaysa yalnız atfı kayıtlıysa girer (o sunucu metni değil atfı gösterir).
- **İki yönlü okuma:** `Library.text_links` (araç T6'da).
- **Yöntem `structure`:** T5'te Beyzâvî biriminin âyetle bağı için (birim başlığı söylüyor; okuma değil).
- **Denetim kaydına yazma komutu:** `link_reviews add`.
- Kalan açık soru: denetçi seçme ölçütü (Açık sorular).

### T5: bağlar (2026-11-04)

`links_tefsir.py` (kurallar başında); dosyalar `data/links/tefsir/` (`private`), raporlar `data/interim/tefsir/t5-*.md`.

| Bağ | Sayı | Yöntem |
|---|---|---|
| Birim → âyetleri (`verse_unit`) | 39 | `structure`: birimin başlığı |
| İşaretsiz Kur'ân alıntısı | 419 (lemma adayı 115, kendi âyeti 239) | `quran_text`: kelime sınırlı iskelet araması |
| Hadis («» ve hadis işareti) | 10 (18 sözden: bulundu 1, kısmen 4, bulunamadı 11, kısa 1, Kur'ân 1) | `corpus`: Risale'ninkiyle aynı eşleyici |

- **Eşik ölçümü** (JK'nın `@QB@` işaretleri, yalnız müellifin metni): 3 kelime / 7 harfte isabet %96, kapsama %92;
  örneklemde sık kalıplar başka sûreye bağlanıyordu ("ما تقدم من" → Fetih 2), seçilen 3 kelime / 9 harf: isabet
  %97,5, kapsama %90,5. Kendi âyetinde bağlam doğruladığı için 2 kelime / 4 harf; cümle ortasındakiler zayıf.
- **Birden çok yerde geçen söz** (33) numarasız kalır, bağ kurulmaz (Risale'deki kural).
- **İşârât:** her Beyzâvî biriminin İşârât'ta aynı âyetle açılan bölümü var (Türkçe ve Arapça). Arapça İşârât ile
  ortak 4 kelimelik diziler yalnız kalıp ifadeler ("ابن عباس رضي الله تعالى عنهم"); İşârât Beyzâvî'yi lafzen aktarmıyor.
  İlişki (aynı görüş, farklı görüş, nakil) ancak okumayla kurulur: aday listesi `t5-isarat.md`, bağ yok.
- **Ölçüt:** tefsir bağlarıyla ve onlarsız yerel kurulumda Risale'nin hadis, âyet ve denetim tabloları aynı; genel
  sunucunun araç çıktısı aynı.
- T7'ye: lemma adayları ve Kur'ân alıntısı örneklemi (`t5-kuran.md`), hadis adayları.

### T6: araçlar (bitti, 2026-11-04)

Her ek veriye bağlı: yalnız veritabanında müfessir eseri varsa görünür (yerel profil). Genel sunucunun araç çıktısı ve
talimatı aynı kaldı. Ayrıntı CLAUDE.md'de. Âyetten: önce Risale'nin yerleri (`results`, `links`), sonra
`classical_works` (birim ve şerhteki alıntılar). Eserin yazarı her sonuçta; muhakkikin girişi `layer` ile; baskının
âyet satırı metniyle ama cümle değil. Yeni araç `text_links`. Altın sorular T1–T4: içerik (Bakara 6, Kûfeliler),
İşârât ile Beyzâvî ayrı ayrı (Fâtiha 5), muhakkik katmanının atfı (vefat tarihi), tuzak (Beyzâvî'nin Risale'den
nakli).

Altın soruların ilk çalıştırması (`20261104-164638`, yerel sunucu): dördünde de beklenen bölüm okundu ve anıldı,
12 atfın 12'si doğrulandı, araç hatası yok, ortalama 46 sn ve 0,25 $. T1 sözü Beyzâvî'ye verdi, tercümesini "benim"
diye ayırdı; T2 önce İşârât'ı sonra Beyzâvî'yi ayrı başlıklarda verdi ve aralarında kayıtlı bağ olmadığını söyledi;
T3 bilgiyi Maraşlî'nin girişine verdi; T4 nakil uydurmadı. Kullanıcıya sorulacaklar:
- (Kullanıcı cevapladı, 2026-11-04: müfessirin eseri tefsirdir ve öyle anılır; yasak yapay zekânın ürettiği metin
  için. Bkz. Terimler.) Model eserleri "tefsir" diye anıyor ("iki tefsiri ayrı ayrı veriyorum", "2:6'nın tefsirinin başında"). Kural bir
  yerin bir âyetin tefsiri diye anılmamasıydı; tür adı olarak "tefsir" (Envârü't-Tenzîl bir tefsir kitabıdır) ayrı mı?
- T4'te model "Risale'de Beyzâvî'ye atıf yok" dedi; T3'teki model Muhâkemat'ta "Tefsîr-i Beyzâvî"yi buldu. Sebep
  aramanın eki ayırmaması ("Beyzavi" tam kelime, metinde "Beyzâvî'nin"); `Beyzav*` buluyor. T6 değil, bugünkü
  arama; ayrı iş.

### T7: kullanıcı örneklemi (bitti, 2026-11-04)

Örneklem `data/interim/tefsir/t7-orneklem.html` (Arapça tek yazı tipi, büyük; `.md` ve numara anahtarları `.json`),
`uv run python -m risale_mcp.links_tefsir --sample` (önceki seçimi ve numaraları korur).

İlk tur ve çıkanlar:
- **Gösterim hatası (bende):** âyetin metni 160 harfte kesiliyordu; uzun âyetlerin sonu görünmediği için A9, A11, A24,
  A38 "aynı âyet değil" göründü. Artık tam metin, bulunan kelimeler âyetin içinde de vurgulu (vakıf işaretleri kelime
  sayılmaz; Bakara 21'de hat ile imlâ kelime sayısı tutmadığından vurgu yok).
- **Anahtar hatası:** aynı cümlede aynı âyetin iki alıntısı aynı bağ anahtarına düşüyordu (A11 ile A24). Kur'ân
  alıntısı bağı artık alıntının iskeletini parça anahtarı olarak taşır (`links.check` işaretsiz metinde parçayı
  cümlenin iskeletinde arar).
- **Kural hataları:** A24 "عز من قائل" kalıbının "قائل"ını alıntıya katıyordu (iskelette "قالوا"): alıntıyı haber
  veren kelimeler başta atlanır (`QUOTE_FORMULAS`). A25 "لما علم ما" âyetin "أعلم ما"sı sanıldı: kendi âyetinin 2
  kelimelik gevşek eşiği yalnız cümle başında (lemma). Alıntılar 419 → 330, isabet %97,8, kapsama %89,9.
- **Kararlar** (denetim kaydı, `tefsir/quran_text.jsonl`, `origin: T7`): lemma 13 ✓, A35 ✓ (grubun adı
  düzeltildi: "birimin kendi âyeti dışında"). 8 satırın bağı kural değişikliğiyle kalktı.
- **B (hadis):** kullanıcı Arapçayı ayırt edemiyor; hadisçiye bırakıldı (HA6), karar yazılmadı.
- **C:** 28 uzun cümlenin hepsi kalır; `tests/golden/beyzavi_long_sentences.json` kilitler.
- İkinci tur (düzeltilmiş gösterimle): kalan 18 satırın hepsi doğru (A9, A11, A24, A38 dahil). Sonuç: 40'lık örneklemin
  32'si doğru ve kayıtlı, 8'inin bağı kullanıcının bulduğu kural hatalarının düzeltmesiyle kalktı; kalan bağlarda
  örneklemde yanlış yok. Denetim kaydında 32 karar (güç: bağın bugünkü gücü), `find_ayah`'ın `classical_works`
  alıntılarında `reviews` olarak görünür.

**Pilotun ölçütü tuttu:** Beyzâvî'nin her parçası âyet aralığıyla adreslenir (39 birim, Fâtiha ve Bakara 1–33 eksiksiz),
cümle düzeyinde atfedilir (977 cümle, basılı sayfasıyla), Risale'nin aynı âyetteki yeriyle yan yana okunur
(`find_ayah`: önce Risale, sonra `classical_works`), her bağın türü, yöntemi ve kanıtı vardır; alıntı bağları
kullanıcının örnekleminden geçti. Açık kalanlar: hadis bağları hadisçiye (HA6), İşârât ile ilişki okumayla (bağ
yok), aramanın ek ayırmaması (T6), genel sunucuya çıkış ayrı karar (pilot `private`). Sıradaki eser ve aralık
kullanıcıyla seçilir.

Pilotun ölçütü: Beyzâvî'nin her parçası âyet aralığıyla adreslenir, cümle düzeyinde atfedilir, Risale'nin aynı
âyetteki yeriyle yan yana okunur; hiçbir bağ kanıtsız ve yöntemsiz değildir. Ölçüt tutarsa sıradaki eser ve aralık
kullanıcıyla seçilir.

Değerlendirme ve sonraki adımlar: `docs/tefsir-pilot-degerlendirme.md` (2026-11-04).

## Açık sorular

- ~~Beyzâvî'nin hangi nüshası~~ (T0: Shamela0023588, Maraşlî); hâşiyeleri (Şeyhzâde, Kâdî hâşiyeleri) ayrı eser mi, katman mı.
- Çalışmalar katmanı (katkıcı notları) hangi profilde durur; genel sunucuya ne zaman çıkar.
- Denetçi kimdir: ilk aşamada kullanıcının davet ettiği isimli âlimler; seçim ölçütü yazılı olmalı.
