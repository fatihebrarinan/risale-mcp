# Bağ altyapısı (HA1)

Hadis aşamalarının ilki (CLAUDE.md, "Hadis aşamaları"). Risale'nin âyet ve hadislerle, ileride kendi içinde ve
tefsirlerle kurduğu bağlar tek biçimde, tek yerde tutulur. Risale sunucusu ve hadis sunucusu (HA5) aynı bağları
okur: biri "bu cümle şu rivayete bağlı", öbürü "bu rivayet Risale'de şuralarda" der.

## Bugün (2026-11-03)

| Bağ | Yer | Sayı (kisisel) | Biçim |
|---|---|---|---|
| Âyet alıntısı | `arabic.sura`, `ayah_quotes` (`build_db`) | 10.296 parça | Kaynağın işareti ve Kur'ân metninde bulunan |
| Âyet ilişkisi | `ayah_links` (`build_db`, kurallar) | 977 | Bölüm ya da cümle → âyet, tür ve güç |
| Hadis, derlem | `matches.json` → `hadith_matches` | 789 | Parça anahtarı → rivayet (geçişe değil) |
| Hadis, künyeli arama | `matches.json` → `hadith_located` | 474 | Geçiş → rivayet |
| Hadis, okuma | `region.json` → `hadith_region` | 209 | Geçiş → rivayet |
| Model okumaları | `readings.json` → `hadith_readings` (yerel) | 520 | Parça anahtarı → rivayet, iki okuyucunun cevabı |
| Nâşirin künyesi | `hadith_citations` | 5.089 | Geçiş → künye metni ve konumları |
| Eski adlar | `books/old_names.json` | 13 | Bölüm → bölüm |

Sorunlar: her bağ türü kendi biçiminde ve kendi tablosunda; hadis bağının ucu bazen parça anahtarı bazen geçiş;
rivayet kimliği derlemin kimliği (`sanadset:220501`, `tirmidhi:3839`), kütüphanedeki kitabın değil (`tirmidhi/3839`);
`hadith_support` bağlardan değil, eşleme anında hesaplanır.

## Kararlar (önerilen)

1. **Bağ kaydı** (bir satır bir bağ, JSON Lines):

   ```json
   {"source": "mektubat/19/.../misal-15/c009", "part": "خذمجتبهوقبضعليهولتكبه",
    "target": "hadis:tirmidhi/3839", "type": "quote", "relation": "by_meaning",
    "method": "reading", "strength": "strong",
    "evidence": {"citation": "Tirmizî, Menâkıb: 47, no. 3839", "readers": ["by_meaning", "by_meaning"]}}
   ```

   - `source`: Risale'de bağın ucu. Cümle kimliği (atıf birimi); bölüm kapsamlı bağda düğüm kimliği ve `scope: section`.
     `part`: cümlede birden çok Arapça parça varsa hangisi (parçanın iskelet anahtarı; yeniden ayrıştırmada kayan
     sıra numarası değil).
   - `target`: ad alanlı kimlik. `quran:2:255` ya da `quran:2:255-257`, `hadis:bukhari/52` (kütüphanedeki kitap),
     kütüphanede olmayan rivayet için geçici `hadis-derlem:sanadset:220501` (HA2/HA3 bunları kütüphaneye taşır),
     `risale:lemalar/30` (Risale içi).
   - `type`: `quote` (söz aktarılıyor: âyet ya da hadis alıntısı), `relation` (âyetle bağ: işaret, açılış, izah,
     dayanak, risale), `reference` (metnin başka yere göndermesi, eski adlar).
   - `relation`: alıntıda lafız ilişkisi (`verbatim`, `abridged`, `by_meaning`, `phrase`); ilişkide türü (`isaret`…).
   - `method`: bağı kim kurdu: `source_mark` (kaynağın işareti), `quran_text` (Kur'ân metninde bulundu), `corpus`
     (derlemde kelimesi kelimesine), `cited_chapter` (künyenin bölümünde kısa parça), `reading` (künyenin bölgesinde
     iki kör okuyucu), `rule` (âyet ilişkisi kuralları), `curated` (elle, kanıtlı: eski adlar), ileride `scholar`.
   - `strength`: `strong` | `weak` (âyet ilişkilerindeki anlam; hadiste `corpus` ve `reading` güçlü, kısa parçanın
     `cited_chapter`'ı zayıf).
   - `evidence`: yönteme göre serbest (kanıt cümlesi, künye, okuyucu cevapları, eşleşme puanı).
   - `display`: hadis sunucusunun Risale metnini taşımadan gösterebilmesi için kaynağın atfı (`cite_as`).
2. **Dosyalar:** `data/links/<alan>/<yöntem>.jsonl` (`hadis/corpus.jsonl`, `hadis/reading.jsonl`, `kuran/quote.jsonl`,
   `kuran/relation.jsonl`, `risale/reference.jsonl`). İlk satır üst bilgidir (`{"meta": {...}}`: üreten komut, tarih,
   lisans notu, `private` ise yalnız yerel). Model okumalarının adayları (hüküm olmayanlar) `private`'tır.
3. **Üreten ve okuyan:** Bağı üreten iş (hadis eşlemesi, okuma, kurallar) dosyaya yazar; `build_db` her profil için
   dosyalardan tabloya yükler (`links`: tek tablo; bugünkü `hadith_matches`, `hadith_located`, `hadith_region`,
   `ayah_links` onun görünümleri olur). Âyet alıntıları ve ilişkileri metinden kurallarla çıktığı için `build_db`
   içinde hesaplanmaya devam eder, ama aynı biçimde dosyaya da yazılır: hadis sunucusu ve ileride başka profiller
   Risale veritabanı olmadan okuyabilsin.
4. **`hadith_support` özettir:** geçişin bağlarından ve künyesinden türetilir (en güçlü yöntem). Kaynakçanın notu da
   bağlardan gelir.
5. **Rivayet kimliği kütüphaneye geçer:** Hadith API karşılığı olan rivayet (yedi kitap) `hadis:<kitap>/<no>` olur
   (`hadis_kutub`'un `api` alanından); Sanadset'tekiler HA3'e kadar `hadis-derlem:` ile kalır, metinleri
   `data/library/hadis/derlem.json`'da (bugünkü `matches.json`'ın `reports`'u).
6. **Kimlikler kayarsa:** kaynak cümle kimliği yeniden ayrıştırmada kayabilir; bağ dosyası `part` (parça anahtarı) ve
   `display`'deki ilk kelimelerle denetlenir, tutmayan bağ yüklenmez ve raporlanır (kontrol işaretlerindeki gibi).

## Adımlar

| # | İş | Çıktı |
|---|---|---|
| B1 | `links.py`: kayıt, okuma/yazma, doğrulama (kaynak cümle var mı, `part` tutuyor mu) | Testler |
| B2 | Hadis bağlarını dosyaya: `hadis.py` (derlem, künyeli arama), `hadis_bolge` (okuma), `hadis_okumalar` (yerel adaylar); rivayet kimlikleri kütüphaneye | `data/links/hadis/*.jsonl`, sayım tablosu (bugünkü tablolarla birebir) |
| B3 | `build_db` bağları dosyadan yükler, `links` tablosu; `hadith_support` ve kaynakça notu bağlardan | İki profilde bütün sayılar ve testler değişmeden |
| B4 | Âyet alıntısı ve ilişkileri, eski adlar aynı biçimde dosyaya | `data/links/kuran/*`, `data/links/risale/*` |
| B5 | Araçlar `links` tablosundan; ters yön (`hadis:bukhari/52` → Risale'deki yerler) | `find_hadith`, `get_hadith` |

B3'ün ölçütü: veritabanının hadis ve âyet sayıları ve araç çıktıları geçişten önceki hâliyle aynı kalır.
