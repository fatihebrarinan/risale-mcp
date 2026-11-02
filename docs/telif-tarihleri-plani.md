# Aşama 13.2: telif tarihleri planı

Amaç basittir: Her ayrı risalenin (Birinci Şuâ, İkinci Şuâ, Onuncu Söz…) `data/books/<eser>.json` içindeki kaydında
ne zaman, nerede ve hangi dilde yazıldığı dursun. Örnek: "1936 yılında Eskişehir hapishanesinde Türkçe olarak telif edilmiştir".

## Kaynak

Ana kaynak: [Risale-i Nur Telif Tarihleri](https://www.kastamonur.com/risale-i-nur-telif-tarihleri/) (kastamonur.com, izinli;
sayfa "kaynaksız kopyalamaya rızamız yoktur" diyor, bu yüzden her kayıtta kaynak durur). Sayfada iki liste var:

- **Tablo:** Eski eserler, Sözler, Mektubat, Lem'alar, Şualar, Lâhikalar: tarih, eser, dil, neşir tarihi.
- **Tarih ve yer listesi:** Sözler, Mektubat, Lem'alar, Şualar, Asâ-yı Mûsâ: tarih, yer ya da dayanak ("Barla", "Eskişehir Hapsi", "Tahminen").

Sayfada olmayanlar ve sorunlu yerler başka kaynaklarla karşılaştırılır (aşağıda). Bulunamayan tarih boş kalır.

## Yapılacaklar

1. **Sayfayı kaydet:** `data/raw/kastamonur/telif-tarihleri/`.
2. **Tarih dosyasını hazırla:** `src/risale_mcp/books/telif.json`. `data/books` her `build`'de yeniden üretildiği ve
   git'e girmediği için asıl liste burada durur. Her risale bölüm kimliğiyle eşlenir. İnceleme için tablo da üretilir.

   ```json
   {
     "sualar/2": {"date": "1936", "place": "Eskişehir Hapsi", "language": "Türkçe", "source": "kastamonur"},
     "sualar/4": {"date": "1938", "language": "Türkçe", "estimated": true, "source": "kastamonur"},
     "sualar/9": {"status": "tesbit edilemedi", "source": "kastamonur"},
     "lemalar/5": {"status": "telif edilmedi", "source": "kastamonur"}
   }
   ```

3. **`data/books`'a ekle:** `build` bu bilgiyi ilgili düğüme `written` alanı olarak yazar. Dosyada olup kitapta bulunmayan
   kimlik kurulumu durdurur; böylece yanlış eşleme fark edilir.
4. **Veritabanı ve araçlar:** `nodes` tablosuna eklenir. `list_works`, `get_outline` ve `read_section` gösterir; alt bölüm
   okunurken bağlı olduğu risalenin bilgisi gelir. Cümle kimlikleri ve vektörler değişmez.
5. **Talimat:** Model tarihi yalnız bu alandan söyler, "tahminen" olanı öyle belirtir, kaynağı anar; alan boşsa bilinmediğini söyler.

Tek yeni kod `build` ve veritabanındaki bu küçük eklemedir; asıl iş eşlemedir. Kullanıcı 2. adımın tablosunu gördükten sonra
3. adıma geçilir.

## Karşılaştırma sonuçları

Durum: uygulandı (2026-11-02). Liste `src/risale_mcp/books/telif.json` (177 kayıt), inceleme tablosu `docs/telif-tablosu.md`.

kastamonur'un listeleri bağımsız değildir: tablosu Risale-i Nur Enstitüsü'nün kronolojisi (Köprü, 2000), tarih ve yer listesi
Sorularla Risale'nin listesidir. Bağımsız ikinci kol Hayrat'ın listesidir (risale.online); toplu tarihler verir.

**Karar kuralı:** Eserin kendi künyesi ya da ifadesi önce gelir; sonra kastamonur'un ayrıntılı listesi esastır. Kaynak boşsa ya da
"tesbit edilemedi" diyorsa Hayrat'ın toplu tarihi alınır ve kayıtta belirtilir. Ayrılan kaynak `note` alanına yazılır.

| Yer | Kaynaklar | Karar |
|---|---|---|
| Onuncu Söz | Enstitü 1926, Hayrat 1927, Sorularla Risale 1928 (1342), Nurpedia 1927–28; ilk baskı 1928 | 1927. Müellifin andığı Rûmî 1342, 13 Mart 1927'de biter; Barla'ya resmî varış 1 Mart 1927 |
| Meyve Risalesi | Tablolar adı Onikinci Şuâ'nın yanına yazar | `sualar/11`, 1943–1944 Denizli (kullanıcının kararı). `sualar/12` 1944 |
| İşârâtü'l-İ'câz, Otuzuncu Mektup | 1914–16, 1916–18, 1914–18; baskı 1916 ya da 1918 | 1914–1916, baskı 1918, dil Arapça |
| Sekizinci Şuâ | kastamonur ve Enstitü 1942, Hayrat 1938 | "1938 veya 1942" (kullanıcının kararı) |
| Dokuzuncu Şuâ | kastamonur "tesbit edilemedi", Hayrat 1938 | ~1938: eserin "dokuz-on sene sonra" ifadesiyle uyumlu |
| Ondokuzuncu Lem'a | Tablo 1935, liste 1934, Hayrat 1934–35 | 1934–1935 |
| Hutuvat-ı Sitte | Eser ve bir liste 1920, tablo 1922 | 1920 |
| Nutuk | Tablo 1911, liste 1908–09 | 1908–1909 |
| Yirmidokuzuncu Lem'a, Otuzüçüncü Lem'a | Tablo dili Türkçe der | Arapça |
| Birinci ve Beşinci Şuâ | Tebyiz tarihi ayrı | 1936 ve 1938, `note` alanında |
| Yirmialtıncı ve Yirmisekizinci Mektup | Parçaların tarihi bizim bölümlerimize eşlenemedi | Mektubun tamamına aralık yazıldı; tahmin edilmedi |
| Küçük Sözler ve "1926 – Barla" kayıtları | Hayrat 1927; Barla'ya resmî varış 1 Mart 1927 | 1926 kalır, `note` alanında (kullanıcının kararı) |

Doğrulama kaynakları: [Köprü](https://www.koprudergisi.com/bahar-2000/risale-i-nur-kulliyatinin-telif-kronolojisi/),
[Hayrat](https://risale.online/soru-cevap/risalelerin-telif-tarihleri),
[Sorularla Risale](https://sorularlarisale.com/risale-i-nur-kulliyatinin-telif-tarihleri-hakkinda-kronolojik-bilgi-verir-misiniz),
[Nurpedia, Onuncu Söz](https://nurpedia.org/wiki/Onuncu_S%C3%B6z),
[Risale Haber, Bilal Tunç](https://www.risalehaber.com/said-nursinin-ahireti-ispat-eden-hasir-risalesini-yazdigi-tam-tarih-432598h.htm),
[TDV](https://islamansiklopedisi.org.tr/said-nursi).
