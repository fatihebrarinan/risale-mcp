# Tefsir altyapısı planı

Kullanıcının kararıyla açıldı (2026-11-04). Uzun vadeli bir iştir; birkaç yıl sürebilir. Hız değil sağlamlık
ölçüttür: her adres veriden gelir, her bağın kanıtı ve yöntemi vardır, her karar geri izlenebilir.

## Terimler

- **Bizim işimiz tefsir yazmak değildir; tefsir altyapısı kurmaktır.** Projenin hiçbir çıktısı, aracı, sayfası ya da
  talimatı kendini "tefsir" diye anmaz. Model de bir yeri "tefsir" diye sunmaz (Âyet ilişkileri'ndeki kural genişler).
- **Müfessirin eseri:** Beyzâvî'nin Envârü't-Tenzîl'i gibi, kendi adıyla anılan eser. "Tefsir" kelimesi yalnızca
  bu eserlerin türünü söylemek için ve kendi adlarında geçer.
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
| H1 | Yalnız Sözler'in birkaç düğümünün cümleleri kilitli (`tests/golden/sentences_sozler.json`). Cümle bölücü ortaktır: Arapça nesir için yapılacak bir değişiklik `isaratul-icaz-arabi` ya da `el-mesnevi-el-arabi`'nin numaralarını sessizce kaydırabilir. Veritabanında yalnız `built_at` var; derlem sürümü yok. | **Kimlik manifestosu ve derlem sürümü:** her eserin bütün cümle kimlikleri ve özetleri (`hash`) bir manifestoda; `build` bir öncekiyle karşılaştırır, kayan, silinen ve metni değişen kimlikleri raporlar (kasıtlı değilse durur). Yayına çıkan veritabanına sürüm etiketi; `cite` sonucunda sürüm. Sonraki her adım bununla ölçülür, bu yüzden ilk. |
| H2 | `Work` müellifi örtük olarak Bediüzzaman sayar: `Authority.MUELLIF` "müellifin eseri", talimat "the author" der. Eserin yazarı alanı yok; `Group` yalnız Risale gruplarını bilir. | **Eserin yazarı:** `Work.author` (ad, vefat; varsayılan Bediüzzaman), `authority` eserin kendi yazarına göre okunur. Risale için davranış değişmez; talimat değişikliği T6'da. |
| H3 | Eser kaynağı yalnız site ve kitap kimliği (`SourceRef`); baskı, muhakkik, lisans `docs/izinler.md`'de düz yazı. | **Baskı kaydı:** eser düzeyinde baskı, muhakkik, dijital nüsha (sabit commit), lisans ve izin satırı. 74 eser için doldurulur; genel profil izni yazılmamış eseri kurmaz (bugün bu kural yalnız `private` ile korunuyor). |
| H4 | Bağın kaynağı örtük olarak Risale cümlesi; metinden metne hedef yalnız `risale:`. | **Bağ uçlarının genelleşmesi:** iki uç da herhangi bir eserin cümlesi ya da bölümü olabilir; ad alanı koleksiyondan (`risale:`, ileride `tefsir:`). Metinden metne ilişki türleri için yer açılır (aynı söz, nakil, aynı görüş, farklı görüş, itiraz); türlerin kendisi T5'te okumayla kesinleşir. |
| H5 | Denetim kararları tek bir test dosyasında (`tests/golden/ayah_links_review.json`, 62 âyet ilişkisi kararı); bağlar her kurulumda yeniden üretildiği için karar bağın içine yazılamaz. | **Denetim kaydı:** bağlardan ayrı, yalnız eklenen dosyalar (`data/links/reviews/`): bağın anahtarı (kaynak, hedef, tür, parça), durum (`reviewed`, `disputed`, `withdrawn`), denetçi, tarih, gerekçe. Denetçi listesi isimlidir. İlk veri bugünkü 62 karar (denetçi: kullanıcı); test aynı kararları buradan okur. Araçlar bağın denetim durumunu verir. |
| H6 | OpenITI okuyucu hadis kitaplarına gömülü (`hadis_kutub.py`, `sources/hadis.py`); sayfa işaretleri (`PageV01P003`) atılıyor. | **Ortak OpenITI okuyucu:** indirme (sabit commit, üst bilgi), mARkdown ayrıştırma, `@QB@…@QE@` âyet işaretleri ve sayfa işaretinden `printed`. Hadis kitapları da bunu kullanır; HA3'teki Müsned künyeleri (cilt:sayfa) için de gereklidir. |

Önerilen sıra: H1, sonra H2–H3 (eser modeli), H4–H5 (bağlar), H6. H1 en önce gelir, çünkü öbürlerinin "hiçbir şey
kaymadı" ölçütünü o verir.

Kaynak durumu (2026-11-04, yalnız listeleme): OpenITI'de Envârü't-Tenzîl'in beş nüshası var
(`0700AH/data/0685NasirDinBaydawi/0685NasirDinBaydawi.AnwarTanzil`: `JK000128`, `ShamAY0034065`, `Shamela0023588`,
`Shia002637Vols`, `Tafsir01006`), Keşşâf da (`0550AH/data/0538JarAllahZamakhshari.Kashshaf`). Nüsha seçimi T0'dır.

## Pilot: Beyzâvî, İşârâtü'l-İ'câz'ın kapsadığı aralık

İşârât Fâtiha'yı ve Bakara'nın 1–33. âyetlerini işler (39 bölüm, 5.224 cümle). Pilot aynı aralıkta Beyzâvî'nin
Envârü't-Tenzîl'ini alır (kullanıcının seçimi). İkinci eser olarak Zemahşerî'nin Keşşâf'ı düşünülebilir: İşârât onu
adıyla anar, Beyzâvî de büyük ölçüde ondan süzülmüştür.

| # | İş | Çıktı |
|---|---|---|
| T0 | Kaynak: Beyzâvî OpenITI'de aranır (baskı, commit, lisans); başka nüsha gerekirse izin istenir | `docs/izinler.md` satırı, ham veri `data/raw/openiti/` |
| T1 | Ham veriyi incelemek: âyet işaretleri, bölümler, hâşiyeler, nakil kalıpları; örnekler kullanıcıya | Örnek dökümü |
| T2 | Kararlar: koleksiyon (`library/tefsir/`), şema, kimlik biçimi | Bu belgenin "Kararlar"ı |
| T3 | Ayrıştırıcı ve cümle bölücü (Arapça nesir, el-Mesnevî el-Arabî'nin kuralları) | `data/library/tefsir/beyzavi.json`, altın örnekler |
| T4 | Beyzâvî'nin bağları için H4 ve H5'in eksik kalan kısmı | `links.py`, testler |
| T5 | Bağlar: Beyzâvî parçası → âyet (yapıdan); Beyzâvî'nin âyet ve hadis alıntıları (bugünkü yöntemler); İşârât bölümü ↔ Beyzâvî parçası (aynı âyet aralığı yalnız aday; ilişki türü okumayla) | `data/links/tefsir/*.jsonl`, sayım ve örneklem |
| T6 | Araçlar: âyetten Risale'nin ve Beyzâvî'nin yerleri, Risale önce; talimat ("tefsir" denmez, eserin sahibi söylenir) | Altın sorular |
| T7 | Kullanıcı örneklemi denetler; kararlar `tests/golden/`'a kilitlenir | Karar dosyası |

Pilotun ölçütü: Beyzâvî'nin her parçası âyet aralığıyla adreslenir, cümle düzeyinde atfedilir, Risale'nin aynı
âyetteki yeriyle yan yana okunur; hiçbir bağ kanıtsız ve yöntemsiz değildir. Ölçüt tutarsa sıradaki eser ve aralık
kullanıcıyla seçilir.

## Açık sorular

- Beyzâvî'nin hangi nüshası; hâşiyeleri (Şeyhzâde, Kâdî hâşiyeleri) ayrı eser mi, katman mı.
- Çalışmalar katmanı (katkıcı notları) hangi profilde durur; genel sunucuya ne zaman çıkar.
- Denetçi kimdir: ilk aşamada kullanıcının davet ettiği isimli âlimler; seçim ölçütü yazılı olmalı.
