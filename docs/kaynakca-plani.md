# Kaynakçada âyet ve hadis; hadis adaylarının araçlara girmesi

> Güncel plan, durum ve sıra `PLANLAR.md`'dedir (2026-11-09); bu belge ayrıntı ve geçmiştir.

Genel sıranın 2. adımı ve kullanıcının isteği (2026-11-03): Risale'den yapılan bir alıntı âyet ya da hadis
içeriyorsa kaynakçada onun adresi de verilir. Hadiste kaynağın (nâşirin) künyesi derlemde doğrulanamasa da verilir,
"(doğrulanmadı)" notuyla; Risale'yi yayına hazırlayanların künyesi değerli bir kanıttır.

## Bugünkü durum (genel veritabanı, Osmanlıca hariç)

- **Âyet:** 7.000'den çok geçişin sûre ve âyet numarası var, Kur'ân metniyle denetlenmiş (`ayah_check`: `exact`
  9.875, `iktibas` 15, `dizgi_suphesi` 3). Numarası olmayanlar çoğunlukla Osmanlıca ciltler ve Hizbler.
- **Hadis:** 643 geçişin 638'inde künye var (kaynağınki geçiş başına, nurpedia'nınki parça başına). Künyesiz 5.
  Künyeler `hadith_citations.raw`'da; `arabic.source` risaleoku'da meal ile künyeyi karışık taşır, kaynakçada
  kullanılmaz.
- **`cite`** bugün yalnız Risale atfını verir; âyet ve hadis cümlenin içinde kalır, kaynakçaya girmez.
- **Adım 3–7** (lafız farkı adayları, rivayet denetimi, künye uyumu, model okuması) yalnız `data/interim/`'de.

## Kararlar

1. **Kaynakçaya künye girer, meal girmez.** Meal cevabın metninde kalır (`publisher_translation`, nâşirin olduğu
   söylenerek). Kaynakça adres listesidir.
2. **Satır biçimi:** Risale atfının altında, aynı numaraya bağlı alt satırlar:

   ```
   [1] Mektubat › Yirmi Dokuzuncu Mektub › … › “Hadîs-i şerifte …”
     - Hadis: Tirmizî, İlim: 19; İbn Mâce, Zühd: 15 (doğrulanmadı)
     - Âyet: Bakara Sûresi, 2:255
   ```

   Numaralama bozulmaz, Risale'nin cümlesiyle bağı görünür. Âyet ve hadis ayrı numara almaz.
3. **Hangi parçalar girer:** Alıntı verilmişse yalnız alıntının içine düşen parçalar ("…" ile atlananlar girmez);
   alıntısız (yalnız dayanılan) kaynakta aralığın bütün parçaları. Hâşiyedekiler, hâşiye ayrı kaynak olarak
   anıldıysa girer. Bir kaynakta aynı âyet ya da künye bir kez yazılır.
4. **Âyet notları:** Kur'ân metniyle tutan numara notsuzdur. `iktibas` "(iktibas)", `dizgi_suphesi`
   "(numara metinle tutmuyor)". Numarası olmayan âyet satıra girmez (adres uydurulmaz).
5. **Hadis notları:** Gösterilen künye geçişin kendi künyesidir; yoksa nurpedia'nınki. Not:
   - notsuz: Arapçası derlemde kelimesi kelimesine (`found`) bulundu ve bulunan rivayetlerden biri künyedeki
     kitapta; ya da kısa parça künyenin anılan bölümünde (`located_chapter`).
   - "(lafız farkıyla bulundu)": `partly_found`, künyedeki kitapta.
   - "(okumayla bulundu)": künyenin bölgesinde (Kütüb-i Sitte, Muvatta) iki kör okuyucu aynı sözü buldu (Adım 9;
     kullanıcının kararı, 2026-11-03: bu bulgular "doğrulanmadı" kalmaz).
   - "(doğrulanmadı)": öbür bütün künyeli durumlar. Adım 3–7'nin okumaları bu notu kaldırmaz.
   - künye yoksa: "Hadis (kaynakta künye yok)". `kind_unverified` parça: "hadis olarak sunulmuş (künye yok)".
6. **Adım 3–7 yalnız `kisisel` profilde** araçlara girer, hadisçinin kararlarına kadar genel sunucuya çıkmaz. Kaynakça
   kuralları (madde 1–5) iki profilde de aynıdır.

## Adımlar

Her adımın sonunda çıktı gösterilir, onaydan sonra sonrakine geçilir. Kullanıcı biçimi, notları ve kaynakçaya meal
girmemesini onayladı (2026-11-03).

| # | İş | Çıktı |
|---|---|---|
| K1 | Cümle aralığı ve alıntıdan, içindeki âyet ve hadis parçalarını ve notlarını çıkaran işlev (`library.py`); künyenin temiz yazılışı (`hadith_citations.raw`'dan, artık ayraç ve "Bkz." atılır, kitap adı yazılışı kaynağınki kalır) | 40 rastgele kaynak için önizleme tablosu: alıntı, parçalar, kaynakça satırları |
| K2 | `cite` kaynakçaya alt satırları ekler; `sources`'ta parça başına ayrıntı (`embedded`). `CITE_NOTE`, sunucu talimatı ve sitedeki dört proje talimatı: alt satırlar da değiştirilmeden kopyalanır. `citations.check` alt satırlı kaynakçayı okur. Testler | Birim testleri; birkaç örnek cevap |
| K3 | Adım 3–7 `kisisel` veritabanına: adaylar ve model okuması (ilişki, söz sahibi, ret ifadesi) ayrı tablolarda, `hadith_support` değişmez. `find_hadith`, `get_passage`, `read_section`: `candidate_reports` ("model reading, not verified" notuyla), rivayet denetiminin uyarıları. Talimat: aday hüküm değildir | Araç çıktısı örnekleri; `genel` veritabanında bu tabloların olmadığının testi |
| K4 | Ölçüm: altın soruların 7'lik hız kümesi (B7 B8 C11 D16 E19 K3 K5): alt satırlar kopyalanıyor mu, atıflar doğrulanıyor mu, süre ve token farkı | `data/interim/golden/<zaman>/report.md`, önceki çalıştırmayla karşılaştırma |
| K5 | Yayın: `genel` için K1–K2 (`scripts/deploy.sh`); claude.ai'de elle bir deneme | Canlıda bir alıntının kaynakçası |

## K1 sonucu

`Library.embedded` (cümlelerdeki âyet ve hadis parçaları ve satırları), `citations.embedded_lines` (alıntıya düşenler).
Önizleme `data/interim/kaynakca/onizleme.md` (40 cümle, alıntısız, Arapçalı ve Arapçası atlanmış alıntıyla).

- **Künye artıkları kaynağında düzeltildi** (`hadis_kunye.parse`): künyeden sonra süren cümleyi kesen kural yalnız
  konumlara uygulanıyordu, ham künyeye uygulanmıyordu (baskı ayracı tek boşlukla değiştiği için konumlar kayıyordu).
  Ham künye artık meal ayracının kapanışında, sondaki "Ayrıca bk." ve "… için bk" açıklamasında biter; ";"den sonraki
  kayıtsız yazar ve kitaplar ("Mer'î b. Yûsuf", "Tevrat, Tesniye") kalır. 461 künye metninin 44'ünde ham künye
  değişti; 5.030 künyede artık 0. Dayanak sayıları değişmedi.
- **Notlar** (genel, Türkçe eserler, hadis geçen cümlelerde satır başına): notsuz 139 (1'i "iktibas"), "lafız
  farkıyla bulundu" 15, "doğrulanmadı" 449 (15'i "mânen", 6'sı "iktibas" ile), künye yok 5.
- Alıntı Arapçayı ortasından kesebilir: parçanın ardışık 3 kelimesi alıntıdaysa ya da alıntının ardışık Arapça
  kelimeleri (en az 2) parçadaysa parça girer.
- "iktibas" ve "mânen" künyelerin hepsinde ortaksa notun içinde bir kez yazılır ("(iktibas, doğrulanmadı)").

## K2–K5 sonucu (2026-11-03)

- **K2:** `cite` her kaynağın altına "  - Âyet: …" ve "  - Hadis: …" satırlarını ekler (`sources[].embedded`); `CITE_NOTE`,
  sunucu talimatı ve sitedeki dört proje talimatı bunların notlarıyla kopyalanmasını söyler. Alt satırlarda "›" yoktur,
  `citations.check` onları atıf saymaz.
- **K3:** `hadis_okumalar.py` Adım 3–7'yi `data/library/hadis/readings.json`'a toplar; `build_db` yalnız `kisisel`
  profilde yükler (şema 12: `hadith_readings`, `hadith_flags`, `hadith_verdicts`). `find_hadith`: `model_readings`,
  `report_flags`, `verdicts`; `get_passage`/`read_section`: `model_reading` işareti. `hadith_support` değişmez.
  Kisisel: 160 okuma, 52 uyarı, 13 ifade; genel: 0.
- **K4:** `20261103-081252`, 7 soru: 52/52 atıf doğrulandı, beklenen bölümler okundu (önceki çalıştırmada K3'te
  okunmamıştı). Ortalama 40 sn / 4.000 token / 0,26 $ (önce 48 sn / 4.899 / 0,30 $). İki soruda `cite` âyet satırı
  döndürdü (C11: Furkān 25:77, Mü'min 40:60; E19: Bakara 2:117), model ikisinde de aynen kopyaladı. Hadis satırı
  çıkan soru yoktu. B7'deki tek hata modelin aracı öneksiz çağırmasıydı. K5 cevabında model Nutuk'ta "birinci kılıç"
  başlığının altında Divan-ı Harb-i Örfî'den bir paragraf olduğunu söyledi: bakılacak.
- **K5:** 2026-11-03'te yayınlandı (şema 12). Canlıda `cite` alt satırları verdi, `find_hadith` genelde model okuması
  vermedi.

## Kapsam dışı

- Yalnız Türkçe aktarılan hadisler (101 aday cümle): Arapçası olmadığı için parça yok; kaynakçaya girmez.
- Hadisin derece bilgisi kaynakçaya girmez (`get_hadith`'te âlimin adıyla kalır).
- Diyanet mealleri kaynakçaya girmez; âyetin kendisi `get_ayah` ile ayrıca alıntılanırsa onun `ref`'i zaten atıftır.

## Olası hatalar

1. Künye geçişe değil parçaya bağlıysa (nurpedia) başka yerin künyesi gösterilebilir: nurpedia künyesi yalnız
   geçişin kendi künyesi yoksa kullanılır.
2. Alıntının sınırı Arapça parçayı yarıda kesebilir: parçanın bir kısmı alıntıdaysa girer.
3. Uzun kaynakça modeli kısaltmaya iter: K4'te ölçülür; gerekirse bir kaynakta en çok N künye.
4. "Notsuz" satır okuyucuya "sağlam hadis" gibi görünebilir: notsuz yalnız "metin künyedeki kitapta var" demektir,
   talimat bunu söyler, derece için `get_hadith`.
