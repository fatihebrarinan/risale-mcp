# Hadis kitapları: ilk dilim (Kütüb-i Sitte ve Muvatta)

Genel sıranın 2b adımı (kullanıcı, 2026-11-03). Hadis kitapları Risale'deki eserler gibi kitap başına ayrı dosyada,
kitap ve bâb ağacıyla tutulur; `hadis` profilinin temelidir. Bu dilim yalnız yedi kitaptır; sonraki kitaplar bu
dilimin sonuçlarına göre seçilir.

## Kaynak araştırması (2026-11-03)

Bâb taşıyan, izni açık bir kaynak arandı:

| Kaynak | Bâb | Lisans | Karar |
|---|---|---|---|
| AhmedBaset/hadith-json (kullanıcının önerisi) | Yok: `chapters` kitap düzeyinde (Buhârî'de 97) | Yok; sunnah.com'dan kazınmış, İngilizce tercümeler yayınevlerinin | Alınmaz |
| Hadith API (kullanılıyor) | Yok: `sections` kitap düzeyinde | Unlicense | Derece ve numara karşılığı için kalır |
| LK-Hadith-Corpus (Leeds, King Saud) | Var (`Section_*`), senet ve metin ayrı | Yok; makaleye atıf istenir | Muvatta yok, lisansı yok: alınmaz |
| Open-Hadith-Data | Yok: numara, metin, şerh | ODbL deniyor, ama alt kaynak "Copyright Islam Ware" | Alınmaz |
| **OpenITI** (KITAB projesi; Shamela ve JK baskıları) | **Var**: kitap ve numaralı bâb başlıkları; hadis numarası; senet ile metin çoğunlukla "*" ile ayrılmış | **CC BY-NC-SA 4.0** (Zenodo sürüm kaydı) | **Seçildi** |

OpenITI'de yedi kitabın JK (Jâmiʿ al-Kutub) baskıları var. Başlık yazılışı kitaba göre değişir:

- Buhârî, Tirmizî, Nesâî: `### |` kitap, `### ||` bâb (Tirmizî'de `### |||` hadis numarası).
- Müslim, İbn Mâce, Ebû Dâvûd, Muvatta: `# | 1 ( N كتاب … )` kitap, `# | 1 ( N باب … )` bâb; başlıksız bâb `# | 1 ( N … )`.

Lisans şartı: kaynak gösterilir (OpenITI, sürüm ve dosya adı), ticari kullanılmaz, türetilen veri aynı lisansla
paylaşılır. Proje ticari değildir; kitap dosyaları bu lisansla işaretlenir.

## Kararlar (önerilen tercihlerle)

1. **Baskı:** her kitapta JK baskısı (yapısal etiketli, hadis numaralı, senet ayrımlı). Metin harekesizdir;
   harekeli metin Hadith API'den numara karşılığıyla gösterilebilir. Ham dosyalar sabit commit'ten indirilir
   (`data/raw/openiti/`, `manifest.json`'da commit ve sha256).
2. **Dosya:** `data/library/hadis/kutub/<kitap>.json`, kitap başına. Alanlar: `book`, `title`, `source`
   (OpenITI URI, commit, lisans), `outline` (kitap ve bâb düğümleri: `id`, `parent_id`, `number`, `title`),
   `hadiths` (`id`, `number`, `node_id`, `isnad`, `matn`, `text`, `page`, `api` = Hadith API numarası).
3. **Kimlik:** `bukhari/52` (kitap ve hadis numarası; Risale kimlikleri gibi değişmez); düğüm `bukhari/k02/b003`.
   Hadis numarası baskının numarasıdır (Fuad Abdülbaki sistemi); Hadith API numarasıyla karşılığı metinden kurulur.
4. **Künyeye bağ:** Risale künyesi "Buharî, Ezân: 148" kitap adı ve bâb numarasıdır. Kitap adı `hadis_kitaplar`'daki
   Türkçe adlardan bu dosyanın kitap düğümüne, numara bâba eşlenir. Bu bağın doğruluğu ölçülür (aşağıda).
5. **Kapsam:** yalnız yerel. `hadis` profili ve genel sunucuya çıkış ayrı karardır.
6. **Ham metinde düzeltme yok:** sayfa işaretleri (`PageV01P003`), `ms0001`, dipnot işaretleri (`\ 1 \`) ve
   `@QB@ … @QE@` (âyet) ayıklanır, metin değiştirilmez; âyet yerleri işaretlenir.

## Doğrulama (her kitap için)

- Sayım: kitap, bâb, hadis; numaralarda boşluk ve tekrar.
- Senet ayrımı: "*" taşıyan hadis oranı.
- Hadith API ile karşılık: metin sonu iskeletiyle eşleşen hadis oranı, numara farkı.
- **Künye–bâb ölçümü:** derlemde kelimesi kelimesine bulunmuş (`found`) ve künyesi bu kitabı gösteren Risale
  parçalarında, künyedeki bâb numarasının gösterdiği bâbda o metin var mı. Karşılaştırma: karıştırılmış künye.
  Bu oran 2a-2'nin dayanağıdır: düşükse bâb bağı kanıt sayılmaz.

## Adımlar

| # | İş | Çıktı |
|---|---|---|
| H1 | İndirici (`sources/hadis.py`, `fetch hadis`) | `data/raw/openiti/` |
| H2 | Ayrıştırıcı `hadis_kutub.py` | `data/library/hadis/kutub/*.json`, rapor `data/interim/hadis/kutub.md` |
| H3 | Hadith API karşılığı ve künye–bâb ölçümü | raporda tablo |
