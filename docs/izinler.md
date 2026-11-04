# Metin kullanım izinleri

Eserlerini kullanmamıza kimin, hangi şartla izin verdiğinin tek listesi. Yeni kaynak eklenmeden önce buraya bakılır;
izin alınınca buraya, sonra koddaki karşılığına (`src/risale_mcp/catalog/permissions.py`) yazılır; genel profil
izni orada kayıtlı olmayan eseri kurmaz. Yazışmalar ve taslaklar: `docs/kaynak-bilgilendirme-epostasi.md`,
`docs/akgunduz-izin-epostasi.md`. Son güncelleme: 2026-11-03.

## Açıkça izin verenler

Kayıtlar kullanıcının bildirimine dayanır; iznin metni depoda yoktur.

| Kaynak | Kapsam | Şart | Kayıt | Şu anki kullanım |
|---|---|---|---|---|
| **erisale.com** (e-Risale) | Sitedeki metinler | Kaynak gösterilecek (sitede belgelerde gösteriliyor) | Görüşme, 2026-10-30 | Birincil kaynak: 27 eser, genel sunucuda |
| **risaleoku.com** | Bütün eserler (başkasının telifli tercümeleri, ör. Kütüb-i Sitte, bu izne dayanılarak alınmadı) | Kazanç olmayacak, kaynak gösterilecek | Site sahibi, 2026-10-30 | 42 eser; 40'ı genel sunucuda, 2 sonradan derleme yalnız yerelde. Sikke'nin ikinci "Husrev'in Bir Fıkrası" da buradan (Sözler Neşriyat baskısı) |
| **kastamonur.com** | Kayıtlı değil | Kayıtlı değil | Kullanıcının bildirimi, 2026-11-02 | Telif tarihleri (Aşama 13.2; sayfa "kaynaksız kopyalamaya rızamız yoktur" der, kaynak her kayıtta durur). Nutuk ve Makalat'ın ham verisi diskte; bu eserler risaleoku'dan gelir |
| **nurpedia.org** | Elindeki her şey | Kayıtlı değil | Kullanıcının bildirimi, 2026-11-02 (istek 2026-10-29) | Hadis işaretleri ve künyeleri (Aşama 14): `Risale:Hadisler` ve 120 kadar `Ayet-Hadis Mealleri` sayfası yerelde. robots.txt yapay zekâ botlarını kapatır, `*` okuma sayfalarına açıktır |

## Genel lisans ya da telif bildirimiyle serbest

Bize özel bir izin değildir; yayımlanan şartlara uyarak kullanıyoruz.

| Kaynak | Şart | Şu anki kullanım |
|---|---|---|
| Keşif Yolculukları (Ediz Sözüer) | "Asliyetini korumak ve kaynak belirtmek" | Ta'likat'ın Türkçesi, genel sunucuda |
| Tanzil Project | Metin değiştirilmez, kaynak ve bağlantı verilir | Kur'ân metni, genel sunucuda |
| Sanadset 650K (Mghari, Bouras, El Hibaoui; Mendeley Data 5xth87zwb5) | CC BY 4.0: kaynak gösterilir | Hadis eşlemesi (Aşama 14), genel sunucuda yalnız eşleşen rivayetler. Not: makale kaynak siteleri bilerek gizler ("we anonymize the website and Hadith pages"), kitap baskısı vermez; "kamu malı" ifadesi yazarların beyanıdır. Lisans yazarların veri setini kapsar, üst kaynağın hakkı doğrulanamadı. Metnin doğruluğu kullanıcının kararıyla kabul edildi (2026-11-02) |
| OpenITI (KITAB projesi, Aga Khan University; Zenodo sürüm kaydı) | CC BY-NC-SA 4.0: kaynak gösterilir (OpenITI, dosya ve sürüm), ticari kullanılmaz, türetilen veri aynı lisansla paylaşılır | Kütüb-i Sitte ve Muvatta'nın JK baskıları (`docs/hadis-kitaplari-plani.md`): kitaplar yalnız yerelde; künyenin bölgesinde okumayla bulunan rivayetlerin 6'sı yalnız JK metniyle genel sunucuda (2026-11-03) |
| Hadith API (fawazahmed0/hadith-api) | Unlicense. Yalnız Arapça ve dereceler; `tur-*` mealler alınmaz, mütercimleri belli değil | Hadis dereceleri (Aşama 14), genel sunucuda eşleşen rivayetlerle |
| Diyanet mealleri (Tanzil üzerinden) | Ticari olmayan kullanım; ortak derlemlere girerse Diyanet'ten izin gerekir | İki meal, genel sunucuda |

## Açık izin kaydı olmayanlar

Bu kaynaklar için izin kaydı bulunamadı. `site/kullanim-sartlari.html` metinlerin "izinle alındığını" söylediği için
genel sunucudaki Rumuzat satırı açık meseledir.

| Kaynak | Ne alındı | Nerede |
|---|---|---|
| risale.online | Siracü'n-Nur (Hayrat). Sikke'nin 13 bloğu 2026-11-02'de risaleoku'ya taşındı | Yalnız yerelde |
| **Rumuzat-ı Semaniye PDF'i** | Kullanıcının dosyası; hak sahibi kayıtlı değil | **Genel sunucuda** |
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
| Yeni Asya | Ortak proje, izinli PDF'ler | Planda; mevcut veri kullanılmıyor |
