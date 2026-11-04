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
   `hadiths` (`id`, `number`, `node_id`, `isnad`, `matn`, `text`, `refs`, `api` = Hadith API numarası). Sayfa
   bilgisi tutulmaz (projenin kuralı).
3. **Kimlik:** `bukhari/52` (kitap ve hadis numarası; Risale kimlikleri gibi değişmez); düğüm `bukhari/k02/b003`.
   Hadis numarası baskının numarasıdır (Fuad Abdülbaki sistemi); Hadith API numarasıyla karşılığı metinden kurulur.
4. **Künyeye bağ:** Risale künyesi "Buharî, Ezân: 148" kitap adı ve bâb numarasıdır. Kitap adı `hadis_kitaplar`'daki
   Türkçe adlardan bu dosyanın kitap düğümüne, numara bâba eşlenir. Bu bağın doğruluğu ölçülür (aşağıda).
5. **Kapsam:** yalnız yerel. `hadis` profili ve genel sunucuya çıkış ayrı karardır.
6. **Ham metinde düzeltme yok:** sayfa işaretleri (`PageV01P003`; H6 ile basılı cilt ve sayfa olarak saklanır, `printed`), `ms0001`, dipnot işaretleri (`\ 1 \`) ve
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

## Sonuç (2026-11-03)

`hadis_kutub.py`, rapor `data/interim/hadis/kutub.md`. Hepsi yalnız yerelde (`data/library/hadis/kutub/`).

| Kitap | Kitap | Bâb | Hadis (en büyük no) | Senetli | API karşılığı |
|---|---|---|---|---|---|
| Buhârî | 100 | 3.949 | 7.135 (7.124) | 7.125 | 6.694 |
| Müslim | 56 | 1.333 | 7.461 (3.033, Abdülbaki ana numarası; tarikler `-2`, `-3`) | 7.439 | 7.176 |
| Ebû Dâvûd | 32 | 1.876 | 5.274 (5.274) | 5.272 | 5.159 |
| Tirmizî | 50 | 2.220 | 3.976 (3.956) | 3.963 | 3.523 |
| Nesâî | 52 | 2.510 | 5.769 (5.758) | 5.762 | 5.633 |
| İbn Mâce | 39 | 1.533 | 4.341 (4.341) | 4.341 | 4.120 |
| Muvatta | 63 | 703 | 1.822 (1.823) | 1.819 | 1.587 |

- Kaynağın iki dizgi hatası: Müslim'de birleşik numara ("# 291429132913 2913"), asıl numara ardındaki sayı. Bu
  satır ilk denemede eksik numara sayımını 1'den 291 milyara kadar kurdurdu ve makinenin belleğini doldurdu
  (oturum iki kez kesildi); sayım artık boşluklardan yapılır, test kilitli.
- Muvatta'nın JK baskısı hadis sonuna tahric kodları koyar ("س 1 - 16 ت 8 - 10"): `refs`'e ayrıldı (1.283 hadis);
  ayrılmadan önce API karşılığı %19'du, sonra %87.
- Buhârî'nin JK numaraları (7.124'e kadar) Hadith API'ninkinden (7.563) farklıdır; karşılık metinden kurulur.
  Ebû Dâvûd, Tirmizî, Nesâî, İbn Mâce'de numaralar çoğunlukla aynıdır.
- JK bazı kitapları birleştirir (Ebû Dâvûd 32 kitap, API 43 bölüm): kitap düğümü kapsadığı API bölümlerini
  (`api_sections`) taşır.

**Künye–bölge ölçümü.** Künyenin sayısı kitaba göre başka şeydir (Wensinck): sünenlerde ve Buhârî'de bâb,
Müslim'de kitap içi hadis sırası. Baskılar bâbı ve tarikleri farklı saydığı için sayı kayar (Buhârî İman 7 = JK 6;
Müslim teşehhüd Abdülbaki 55–62 = JK sırası 61–65). Pencereler tekil künyede karıştırılmış künyeye karşı seçildi:
bâb Nesâî ve İbn Mâce tam, Tirmizî ±1, Buhârî ±3, Ebû Dâvûd ±5; sıra Müslim ±10 (Muvatta'da ölçülecek parça yok,
aynı kural). Sonuç (found ve partly_found parçalar, kaynak ve nurpedia künyeleri):

| Kitap | Künye | Bölgede | Karışık |
|---|---|---|---|
| Buhârî | 27 | 16 | 1,4 |
| Müslim | 25 | 10 | 1,1 |
| Ebû Dâvûd | 11 | 8 | 1,8 |
| Tirmizî | 28 | 19 | 1,7 |
| Nesâî | 7 | 6 | 0,9 |
| İbn Mâce | 16 | 9 | 1,3 |
| **Toplam** | 114 | 68 (%60) | 8,2 (%7) |

Kitap düzeyinde künye 91 tekil künyenin 78'inde tutar. Sınırlar: pencereler aynı veride seçildi, kümeler küçük;
Müslim'de künye yalnız yakın bölgeyi gösterir. Bölgede olmamak künyenin yanlış olduğunu göstermez (seçilmiş en çok
8 rivayete bakılıyor, aynı söz başka tarikle başka yerde olabilir).
