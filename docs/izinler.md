# Metin kullanım izinleri

Eserlerini kullanmamıza kimin, hangi şartla izin verdiğinin tek listesi. Yeni kaynak eklenmeden önce buraya bakılır;
izin alınınca buraya, sonra koddaki karşılığına (`src/risale_mcp/catalog/permissions.py`) yazılır; genel profil
izni orada kayıtlı olmayan eseri kurmaz. Yazışmalar ve taslaklar: `docs/kaynak-bilgilendirme-epostasi.md`,
`docs/akgunduz-izin-epostasi.md`. Son güncelleme: 2026-11-05.

## Açıkça izin verenler

Kayıtlar kullanıcının bildirimine dayanır. Yazılı cevaplar depoda değil, yerelde durur: `data/raw/kullanici/izinler/` (git dışı).

| Kaynak | Kapsam | Şart | Kayıt | Şu anki kullanım |
|---|---|---|---|---|
| **erisale.com** (e-Risale) | Sitedeki metinler; kullanıcının bu metinlerle yapacağı her iş (2026-11-05) | Kaynak gösterilecek (sitede belgelerde gösteriliyor) | Sözlü izin (görüşme, 2026-10-30), yazılı nüsha yok; kapsam kullanıcının bildirimi, 2026-11-05 | Birincil kaynak: 27 eser, genel sunucuda |
| **risaleoku.com** | Bütün eserler, kullanıcının bunlarla yapacağı her iş (2026-11-05; başkasının telifli tercümeleri, ör. Kütüb-i Sitte, bu izne dayanılarak alınmadı) | Kazanç olmayacak, kaynak gösterilecek | Site sahibinin yazılı cevabı (ekran görüntüsü `risaleoku-cevap.png`): "Kaynaklarımızı herhangi bir maddi kazanç olmaması ve kaynak gösterilmesi şartıyla kullanabilirsiniz." | 42 eser; 40'ı genel sunucuda, 2 sonradan derleme yalnız yerelde. Sikke'nin ikinci "Husrev'in Bir Fıkrası" da buradan (Sözler Neşriyat baskısı) |
| **kastamonur.com** | Kayıtlı değil | Kayıtlı değil | Kullanıcının bildirimi, 2026-11-02 | Telif tarihleri (Aşama 13.2; sayfa "kaynaksız kopyalamaya rızamız yoktur" der, kaynak her kayıtta durur). Nutuk ve Makalat'ın ham verisi diskte; bu eserler risaleoku'dan gelir |
| **nurpedia.org** | Elindeki her şey, "uygun bulduğunuz şekilde" | Şart yok; kaynak gösterme ricası ("Kaynak göstermenizden memnun oluruz"); gösteriyoruz | Yazılı cevap (`nurpedia-cevap.txt`; istek 2026-10-29, cevap kullanıcının aktarımıyla 2026-11-05) | Rumuzat-ı Semaniye'nin metni, genel sunucuda (2026-11-04'ten; kullanıcının kararı). Hadis işaretleri ve künyeleri (Aşama 14): `Risale:Hadisler` ve 120 kadar `Ayet-Hadis Mealleri` sayfası yerelde. robots.txt yapay zekâ botlarını kapatır, `*` okuma sayfalarına açıktır |

### Kapsam (Y0.3, 2026-11-05)

Kullanıcının bildirimi ve yazılı cevaplar: e-Risale (sözlü) ve risaleoku kullanıcının bu metinlerle yapacağı her işi
kaynak gösterilmesi (risaleoku: ve kazanç olmaması) şartıyla, nurpedia şartsız ("uygun bulduğunuz şekilde") kabul etti. Yol haritasının sorduğu üç kullanım bu kapsamdadır:

- **Ayrı sunucular** (hadis, tefsir; Y2): aynı kullanım, aynı kaynak gösterme. Her sunucunun talimatı ve
  kaynakçası kaynağı adıyla anar (risale sunucusunun bugünkü kuralı gibi); bu Y2'nin ölçütüdür.
- **Yerel paket** (Y2.7, isteğe bağlı): kapsamda, ama türü farklıdır: metnin tamamını başkasının bilgisayarına
  verir ve kullanım şartlarındaki "toplu indirme ve yeniden yayın yok" kuralının istisnası olur. Paket
  hazırlanırken kaynağa bir satırlık bilgi verilir (izin değil, nezaket); paketin içine kaynakların adları ve
  şartları (kaynak gösterme; risaleoku için kazanç olmaması) yazılır, paketi alan da bu şartlarla bağlıdır.
- **Osmanlıca** (Aşama 19): izin meselesi değil; e-Risale'nin Osmanlıca metninin nereden alınacağı teknik bir
  sorudur, aşamanın başında ekipten sorulur.

risaleoku'nun "kazanç olmayacak" şartı yazılı cevapta da vardır, yerinde durur. Yazılı cevaplar yerelde
(`data/raw/kullanici/izinler/`); e-Risale'ninki sözlüdür.

## Genel lisans ya da telif bildirimiyle serbest

Bize özel bir izin değildir; yayımlanan şartlara uyarak kullanıyoruz.

| Kaynak | Şart | Şu anki kullanım |
|---|---|---|
| Keşif Yolculukları (Ediz Sözüer) | "Asliyetini korumak ve kaynak belirtmek" | Ta'likat'ın Türkçesi, genel sunucuda |
| Tanzil Project | Metin değiştirilmez, kaynak ve bağlantı verilir | Kur'ân metni, genel sunucuda |
| Sanadset 650K (Mghari, Bouras, El Hibaoui; Mendeley Data 5xth87zwb5) | CC BY 4.0: kaynak gösterilir | Hadis eşlemesi (Aşama 14), genel sunucuda yalnız eşleşen rivayetler. Not: makale kaynak siteleri bilerek gizler ("we anonymize the website and Hadith pages"), kitap baskısı vermez; "kamu malı" ifadesi yazarların beyanıdır. Lisans yazarların veri setini kapsar, üst kaynağın hakkı doğrulanamadı. Metnin doğruluğu kullanıcının kararıyla kabul edildi (2026-11-02) |
| OpenITI (KITAB projesi, Aga Khan University; Zenodo sürüm kaydı) | CC BY-NC-SA 4.0: kaynak gösterilir (OpenITI, dosya ve sürüm), ticari kullanılmaz, türetilen veri aynı lisansla paylaşılır | Kütüb-i Sitte ve Muvatta'nın JK baskıları (`docs/hadis-kitaplari-plani.md`): kitaplar yalnız yerelde; künyenin bölgesinde okumayla bulunan rivayetlerin 6'sı yalnız JK metniyle genel sunucuda (2026-11-03). Beyzâvî'nin Envârü't-Tenzîl'i (tefsir pilotu, T0, 2026-11-04): beş sürüm indirildi, asıl nüsha Shamela0023588 (Maraşlî tahkiki, Dâru İhyâi't-Türâsi'l-Arabî 1418); yalnız yerelde. Lisans OpenITI'nin dijital metnini kapsar; muhakkikin girişi Maraşlî'nin diye işaretli alınır (kullanıcının kararı) |
| Hadith API (fawazahmed0/hadith-api) | Unlicense. Yalnız Arapça ve dereceler; `tur-*` mealler alınmaz, mütercimleri belli değil | Hadis dereceleri (Aşama 14), genel sunucuda eşleşen rivayetlerle |
| Diyanet mealleri (Tanzil üzerinden) | Ticari olmayan kullanım; ortak derlemlere girerse Diyanet'ten izin gerekir | İki meal, genel sunucuda |

## Açık izin kaydı olmayanlar

Bu kaynaklar için izin kaydı bulunamadı. Rumuzat'ın açık meselesi 2026-11-04'te kapandı: metin izin veren
nurpedia'dan gelir; yalnız nurpedia'nın resim verdiği tablolar PDF'ten, kullanıcının kararı ve sorumluluğuyla
("Bu PDF'i insanlara hizmet için internete yüklemişler. Tabloları oradan alma sorumluluğunu ben kendim üstleniyorum.").

| Kaynak | Ne alındı | Nerede |
|---|---|---|
| risale.online | Siracü'n-Nur (Hayrat). Sikke'nin 13 bloğu 2026-11-02'de risaleoku'ya taşındı | Yalnız yerelde |
| Rumuzat-ı Semaniye PDF'i | Kullanıcının dosyası; hak sahibi kayıtlı değil. Yalnız Yedinci Remz'in 20 tablosu (nurpedia'da resim) | Genel sunucuda, kullanıcının kararı ve sorumluluğuyla |
| Quran.com | Harekeli Mesnevî'deki âyetlerin kelime kodları | Yalnız yerelde |
| risale.online (Hayrat) | Telif tarihleri listesi (metin değil, tarih bilgisi; kaynak gösterilerek) | `telif.json`, genel sunucuda (kullanıcının kararı) |

## Reddeden

| Kaynak | Karar | Durum |
|---|---|---|
| Hizmet Vakfı (rasaelalnour.com) | 2026-10-30'da izin vermedi | Site bırakıldı, Arapça eserler risaleoku'dan alındı. Yalnız harekeli Mesnevî yerelde durur, sunucuya çıkmaz |

## Şartları kullanıma izin vermeyen

| Kaynak | Şart | Durum |
|---|---|---|
| Dorar (dorar.net) | Sitede "جميع الحقوق محفوظة"; SSS: ansiklopediler yalnız sitede arama ve gezinme içindir, kopyalanamaz. API şartları (`/api-services/terms`): içerik münhasıran Dorar'ın; toplu indirme ve tam depolama yasak; önbellek 24–48 saat; yeniden yayın ve üçüncü tarafa açmak yasak; hadis metni hüküm özetiyle birlikte gösterilir; kullanım onaylı ürünle sınırlı. robots.txt: `use=reference`, `ai-train=no` | Kullanılmıyor (kullanıcının şartı "telif yazısı yoksa"ydı; yazı var, 2026-11-02). Toplu alınmaz. Tek yol `/api-services/request` başvurusu; elle incelenir, kararı ve başvuruyu kullanıcı verir |

## Bekleyen

| Kaynak | İstek | Durum |
|---|---|---|
| Prof. Dr. Ahmed Akgündüz | Kızıl İcaz tercümesi: izin ve dijital nüsha, Ta'likat tercümesi de | Cevap bekleniyor (Aşama 17) |
| Diyanet İşleri Başkanlığı | Kur'an Yolu ve Hak Dini Kur'an Dili'nin (Diyanet baskısı) tefsir sunucusunda kullanımı, dijital nüsha (`docs/diyanet-izin-epostasi.md`) | Taslak hazır, kullanıcı gönderecek (2026-11-06) |
| Yeni Asya | Ortak proje, izinli PDF'ler | Planda; mevcut veri kullanılmıyor |
