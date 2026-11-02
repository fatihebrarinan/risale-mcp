# Aşama 13.2: telif tarihleri planı

Amaç basittir: Her ayrı risalenin (Birinci Şuâ, İkinci Şuâ, Onuncu Söz…) `data/books/<eser>.json` içindeki kaydında
ne zaman, nerede ve hangi dilde yazıldığı dursun. Örnek: "1936 yılında Eskişehir hapishanesinde Türkçe olarak telif edilmiştir".

## Kaynak

Ana kaynak: [Risale-i Nur Telif Tarihleri](https://www.kastamonur.com/risale-i-nur-telif-tarihleri/) (kastamonur.com, izinli;
sayfa "kaynaksız kopyalamaya rızamız yoktur" diyor, bu yüzden her kayıtta kaynak durur). Sayfada iki liste var:

- **Tablo:** Eski eserler, Sözler, Mektubat, Lem'alar, Şualar, Lâhikalar: tarih, eser, dil, neşir tarihi.
- **Tarih ve yer listesi:** Sözler, Mektubat, Lem'alar, Şualar, Asâ-yı Mûsâ: tarih, yer ya da dayanak ("Barla", "Eskişehir Hapsi", "Tahminen").

Sayfada olmayan eserler (Barla Lâhikası'nın ayrıntısı, Tarihçe-i Hayat, mecmualar gibi) internetten araştırılır.
Bulunamayan tarih boş kalır.

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

## Kaynağın sorunlu yerleri

Eşlemede tek tek bakılacak yerler; sayfadaki bilgi değiştirilmez, gerekirse not düşülür.

| Yer | Sorun | Yapılacak |
|---|---|---|
| Şuâ numaraları | Sayfa Meyve Risalesi'ni Onikinci Şuâ der, bizim verimizde `sualar/11` | Numaraya değil risalenin adına göre eşlenir |
| Onuncu Söz | Tablo 1926, ikinci liste 1928 (1342) | Yer bilgili ikinci liste esas alınır |
| Otuzuncu Mektup, İşarat-ül İ'caz | Tablo 1914–16, ikinci liste 1916 (baskı tarihi) | Telif 1914–16, baskı not olarak |
| Birinci ve Beşinci Şuâ | Tebyiz (temize çekme) tarihi ayrı | `note` alanına yazılır |
| Bir risalenin parçaları | "Onuncu Sözün Üçüncü Zeyli 1936", "Yirminci Sözün Birinci Makamı 1930" | Kaynak parça için ayrı tarih veriyorsa kayıt o alt bölüme konur |
| Kitap adı değişenler | Sayfada "Katre", "Zehre", "Lemaat" | Bizim eser ve bölüm kimliklerimize elle eşlenir |
