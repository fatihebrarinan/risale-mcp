# Tefsir ve hadis bağdaştırıcılarının site sayfaları (taslak, 2026-11-07; yayına alındı)

**2026-11-07:** taslaklar `site/hadis.html`, `site/tefsir.html`, `site/en/hadith.html`, `site/en/tafsir.html`, kurulum sayfalarındaki bölüm ve gizlilik ekiyle siteye geçti; asıl metin artık oradadır, bu dosya yalnız kayıttır. Tefsir sunucusu ayrı makinededir (Falkenstein), gizlilik sayfası bunu söyler.

Yayımlanmaz, `site/`'ye konmaz (oradaki her dosya deploy'la yayına çıkar). M7'de genel çıkış kararı verilince
`site/tefsir.html`, `site/hadis.html` (ve `en/`), kurulum sayfalarına birer bölüm ve gizlilik politikasına ek olur.
Adresler bugün kararlaştırılmış biçimdedir (`mcp.risalemcp.com/tefsir`, `/hadis`); sunucu M7'de kurulur.

## 1. Tefsir bağdaştırıcısı (`site/tefsir.html`)

**Başlık:** Tefsir: klasik tefsirler, cümle cümle ve kaynağıyla

Tefsir bağdaştırıcısı, Claude ve ChatGPT gibi yapay zekâ asistanlarına on üç klasik tefsiri açar: Taberî'nin
Câmiu'l-Beyân'ı, Mâtürîdî'nin Te'vîlât'ı, Zemahşerî'nin Keşşâf'ı, Râzî'nin Mefâtîhu'l-Gayb'ı, Kurtubî'nin el-Câmi'i,
Beyzâvî'nin Envârü't-Tenzîl'i, Nesefî'nin Medârik'i, İbn Kesîr'in tefsiri, Celâleyn, Suyûtî'nin ed-Dürrü'l-Mensûr'u,
Ebüssuûd'un İrşâd'ı, Bursevî'nin Rûhu'l-Beyân'ı ve Âlûsî'nin Rûhu'l-Meânî'si. Bir âyeti sorduğunuzda asistan her
müfessirin o âyetle ilgili sözünü kendi sözüyle, eserin adı ve âyet birimiyle gösterir.

**Nasıl çalışır**
- Her tefsir âyet birimlerine ayrılmıştır; asistan bir âyette önce Risale-i Nur'un o âyete bağlanan yerlerini (adı
  ve türüyle), sonra müfessirleri vefat sırasıyla verir.
- Metinler Arapça aslıyladır. Arapça bilmiyorsanız asistan alıntının ardından kendi çevirisini verir ve bunun
  yayımlanmış bir tercüme değil, yapay zekâ tercümesi olduğunu söyler.
- İki müfessirin aynı âyetten bahsetmesi aralarında bir ilişki olduğu anlamına gelmez; asistanın fark ettiği ilişki
  yorumdur ve ayrı başlıkta durur. Asistanın yazdığı hiçbir şey "tefsir" diye anılmaz.
- Risale-i Nur'un metni bu bağdaştırıcıda yoktur; Risale-i Nur bağdaştırıcısını da eklerseniz asistan oradan okur.

**Kaynaklar ve lisans:** Metinler OpenITI (KITAB projesi) sürümlerinden, her eserin seçilen baskısıyla (muhakkik ve
yayınevi her eserin kaydında); lisans CC BY-NC-SA 4.0: ticari olmayan kullanım, kaynak gösterme. Âyet birimlerinin
sınırları altafsir.com kaynaklı OpenITI sürümünden alınmıştır.

**Ekleyin:** Claude'da ad "Tefsir", adres `https://mcp.risalemcp.com/tefsir`; ChatGPT'de aynı adres (kurulum adımları
Risale-i Nur'unkiyle aynı).

**Sınama sorusu:** "Fâtiha'nın 'iyyâke na'büdü' âyetini Risale-i Nur ve Beyzâvî nasıl ele alıyor? Kaynaklarıyla."

## 2. Hadis bağdaştırıcısı (`site/hadis.html`)

**Başlık:** Hadis: rivayetler, baskısı ve numarasıyla

Hadis bağdaştırıcısı on sekiz hadis kitabını açar: Kütüb-i Sitte ve Muvatta, Ahmed b. Hanbel'in Müsned'i, Dârimî,
Taberânî'nin el-Mu'cemü's-Sağîr'i, Hâkim'in el-Müstedrek'i, İbn Hibbân (el-İhsân), Heysemî'nin Mecmaü'z-Zevâid'i,
Kenzü'l-Ummâl, Münâvî'nin Feyzü'l-Kadîr'i, Aclûnî'nin Keşfü'l-Hafâ'sı, Kādî İyâz'ın eş-Şifâ'sı ve Beyhakî'nin
Delâilü'n-Nübüvve'si. Atıf birimi hadistir: asistan bir rivayeti kitabı, baskının numarası ve basılı sayfasıyla gösterir.

**Nasıl çalışır**
- Arapça kelimeyle ya da anlamla (Türkçe soruyla da) arama; "Buharî, Ezân: 148" ya da "Müsned 14870" gibi bir künyeden
  rivayete gitme.
- Hüküm verilmez: asistan bir hadisin sahih ya da zayıf olduğuna kendisi karar vermez; dereceler yalnız kaynağın
  verdiği gibi ve âlimin adıyla gösterilir. Zehebî'nin, Elbânî'nin ve muhakkiklerin notları ayrı katmandır, kitabın
  müellifine mal edilmez.
- Künyedeki cilt ve sayfa başka bir baskıya ait olabilir; asistan bunu söyler.
- Bir rivayetin Risale-i Nur'da geçtiği yerler adı ve atfıyla verilir; metni Risale-i Nur bağdaştırıcısındadır.

**Kaynaklar ve lisans:** Kitaplar OpenITI sürümlerinden (CC BY-NC-SA 4.0); Kütüb-i Sitte ve Muvatta'nın numaraları ve
âlimlerin dereceleri Hadith API'den (Unlicense). Numarası olmayan kitaplarda (eş-Şifâ, Delâil) kimlik bu kütüphanenin
sırasıdır ve öyle belirtilir.

**Ekleyin:** ad "Hadis", adres `https://mcp.risalemcp.com/hadis`.

**Sınama sorusu:** "Risale-i Nur'da geçen 'Ümmetimin ihtilafı rahmettir' sözü hangi kitaplarda geçiyor, hakkında ne
deniyor? Hüküm vermeden, kaynaklarıyla."

## 3. Kurulum sayfalarına ek (`claude.html`, `chatgpt.html`)

"Diğer bağdaştırıcılar" bölümü: üç bağdaştırıcı ayrı ayrı eklenir; birlikte eklenince asistan bir âyette Risale-i
Nur'u, müfessirleri ve hadisleri ayrı kaynaklarıyla verir. Hepsi ücretsiz ve hesapsızdır.

## 4. Gizlilik politikasına ek (`gizlilik.html`)

"Bağdaştırıcılar" bölümü üç sunucuyu sayar ve her biri için aynı kuralı söyler: yalnız aracın girdisi gelir, kullanım
kaydı (zaman, araç, süre, hata türü) 90 gün tutulur, parametre ve IP kaydedilmez; anlamsal arama ifadesi Voyage AI'a
gider. Tefsir ve hadis sunucusu ayrı bir makinede çalışırsa (M7 kararı) barındırma bölümü ona göre yazılır.
