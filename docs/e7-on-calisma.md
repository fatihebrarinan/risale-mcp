# E7 ön çalışması: rivayet grupları ve yalnız Türkçe aktarılan hadisler (2026-11-25)

Kullanıcının onayıyla (2026-11-24) E5'in ardından yapıldı: karar gerektirmeyen kısım. **Yayın yok, bağ dosyasına
yazılmadı, model okuması başlatılmadı.** Kararlar kullanıcıyla (sonda). Betikler `scripts/e7/`, çıktılar
`data/interim/hadis/e7-*.json`.

## (a) Aynı hadisin rivayetleri, lafızla

**Kapsam:** metni (matn) senetten ayrı duran yedi kitap: Kütüb-i Sitte ve Muvatta (34.049 rivayet; altı kelimeden
kısa metin dışarıda). Öbür kitaplarda (Müsned, Müstedrek, Mecma, Kenz…) metin senede bitişik: ortak râvi adları
sahte benzerlik üretir, önce metni ayırmak gerekir.

**Yöntem (deneme):** rivayetin metni 5 kelimelik dizilere bölündü (`normalize.search_words`), 40'tan çok
rivayette geçen diziler ("صلى الله عليه وسلم قال …" kalıpları) aday üretmedi. İki rivayetin benzerliği: kısa
olanın dizilerinin ötekinde geçen oranı (kapsama). Gruplar bağlı çiftlerin birleşimi (geçişli).

| Eşik (kapsama) | Grup | Gruplanan rivayet | Payı | Kitaplar arası grup | En büyük gruplar |
|---:|---:|---:|---:|---:|---|
| 0,9 | 1.640 | 4.653 | %14 | 1.299 | 26, 21, 20, 19 |
| 0,8 | 2.149 | 6.205 | %18 | 1.673 | 35, 26, 24, 20 |
| 0,6 | 3.322 | 10.736 | %32 | 2.688 | 63, 62, 45, 44 |
| 0,4 | 4.241 | 16.308 | %48 | 3.535 | **439**, 176, 126, 104 |

Gözlemler (örneklem `e7-gruplar-deneme.json` › `samples`):

- **0,8 ve üstü** neredeyse hep aynı hadis: lafız farkı yalnız "النبي / رسول الله", kısaltma, ravinin eklediği söz
  (Buhârî 1318 ~ 6225; Müslim 1118 ~ Muvatta 652).
- **0,6–0,8** çoğu aynı hadis, ama kısa bir hadis onu da içeren uzun bir rivayete bağlanıyor (Buhârî 2075 "نهى عن
  المحاقلة والمزابنة" ~ Ebû Dâvûd 3400, ardından başka bir söz).
- **0,4–0,6** karışık: aynı hadisin farklı lafızları (tahiyyât: Tirmizî 289 ~ Nesâî 1175; emâret: Buhârî 6727 ~
  Tirmizî 1529) ile aynı konunun başka hadisi (bey'at: Buhârî 6776 ~ Ebû Dâvûd 4945) yan yana.
- **Zincirleme asıl sorun:** grup geçişli kurulunca birkaç hadisi bir arada taşıyan rivayetler ayrı hadisleri
  birleştiriyor. 0,6'daki en büyük grupta "من كذب علي متعمدا", "أبردوا بالصلاة", "تسموا باسمي" birlikte (Buhârî 110
  üç hadisi bir arada taşıyor). 0,4'te 439'luk grup.

**Öneri:** grup değil, **çift çift "ortak lafız" bağı**. Her rivayet için ortak lafzı en yüksek komşular, puanı ve
ortak kısmıyla verilir; geçişli birleştirme yapılmaz. Eşik kapsama 0,6 ve en az 3 ortak dizi; puan çıktıda görünür.
Araçta söz: "shares wording with", "aynı hadis" hükmü değil. Bağ şemasında lafız (`quote`) cinsi, mekanik yöntem
(hadis bağlarının bugünkü düzeni). Kitaplar arası çiftler (Buhârî ~ Müslim gibi) asıl kazanç: 0,6'da 2.688 grup.

## (c) Yalnız Türkçe aktarılan hadisler

**Aday listesi:** `data/interim/hadis/turkce.json` (Adım 4): 101 cümle (`quoted_hadith` 61, `quoted_prophet` 23,
`reported` 17); 40'lık örneklemde 4'ü açıkça hadis değildi.

**Künye:** Türkçe sözün Arapça parçası olmadığı için nâşirin künyesi (`arabic.source`) yok. Müellif kaynağı 9 yerde
söylüyor, o da yalnız kitap adı ("Başta Buhârî ve Müslim … haber veriyorlar ki", çoğu On Dokuzuncu Mektub); 92 yerde
hiç künye yok. Yani "künyenin bölgesinde arama" (Adım 9'un yolu) yalnız 9 adayda ve bâb düzeyinde değil, kitap
düzeyinde mümkün.

**Mekanik aday (model okuması yok):** her sözün Türkçesiyle hadis kütüphanesinin vektörlerinde anlamsal arama (Voyage
sorgusu, 101 istek; `e7-turkce-adaylar.json`, ilk üç rivayet). En yakın rivayetin benzerliği:

| Benzerlik | Söz |
|---|---:|
| 0,6 ve üstü | 10 |
| 0,5–0,6 | 28 |
| 0,4–0,5 | 42 |
| 0,4'ün altı | 21 |

Örnekler: "Hastaların duâsını alınız; onların duâsı makbûldür" → Mecma 3759 "عودوا المرضى ومروهم فليدعوا لكم فإن
دعوة المريض…" (0,67, aynı söz); "Size iki şey bırakıyorum, onlara temessük etseniz necât bulursunuz" → Tirmizî 3788
(0,60); "Arz, sevr ve hût üzerindedir" en yakın 0,27 (karşılık yok: müellif Muhakemat'ta onu zaten "mervî" diye
tartışıyor). Benzerlik kanıt değildir: aynı konunun başka hadisi de yüksek çıkabilir (Adım 4'teki "iki yüz / yetmiş"
dersi). Aday, okunmadan bağ olamaz.

## Sizden istenen kararlar

1. **(a) Grup mu, çift mi?** Öneri: çift çift ortak lafız bağı (zincirleme yüzünden grup değil). Eşik 0,6 mı
   (yaklaşık 11 bin rivayet bir komşu kazanır), 0,8 mi (≈6 bin, daha temiz)?
2. **(a) Kapsam:** yalnız metni ayrı yedi kitap mı (bugün yapılabilir), yoksa önce öbür kitaplarda senedi metinden
   ayırmak mı (Müsned, Müstedrek, Mecma, Kenz: ayrı iş, kaynağın biçimine göre)?
3. **(a) Nerede görünür:** hadis sunucusunun `get_hadith`'inde "aynı lafzı paylaşan rivayetler" (en çok 10, puanla).
   Risale sunucusu etkilenmez.
4. **(c) Ne yapılsın?** (i) Aday listesi yerelde kalsın, şimdilik bir şey yapılmasın; (ii) iki kör okuyucu
   (model) her sözü ilk üç adayla okusun, ikisi aynı rivayet derse "okumayla bulundu" (Adım 9'un kuralı, iki
   profilde, 2026-11-03 kararı) olsun; (iii) okumalar yalnız yerelde kalsın (hadisçi görmeden çıkmasın). Öneri: (ii),
   ama yalnız benzerliği 0,5'in üstündeki 38 sözle başlamak; okuma `scripts/d1-arka.sh` ile (model çağrısı).
5. **(c) Liste temizliği:** örneklemde hadis olmadığı görülen 4 cümle (Ermeni fedâileri, İmam Şâfiî'den nakil, "hiç
   hadis yoktur" iddiası, genel cümle) okumaya girmesin mi? Öneri: girmesin, kural Adım 4'te düzeltilsin.
