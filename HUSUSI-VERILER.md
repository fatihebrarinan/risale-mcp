# Yerelde olup sunucuda olmayan veriler

> Bu dosya `uv run python -m risale_mcp.local_only` ile üretilir (`build` sonunda da); elle düzenlemeyin.
> Bir eseri yerelde tutan `Work.private` işaretidir: `src/risale_mcp/catalog/`. İzinler: `docs/izinler.md`.

| Veritabanı | Eser | Bölüm | Paragraf | Cümle | Arapça parça |
|---|---:|---:|---:|---:|---:|
| Yerel (`data/dist/kisisel/`) | 73 | 9.552 | 119.543 | 258.956 | 25.468 |
| Sunucu (`data/dist/genel/`) | 69 | 8.950 | 106.024 | 242.087 | 24.877 |
| **Fark** | **4** | **602** | **13.519** | **16.869** | **591** |

Ortak eserlerde metin aynıdır (JSON özetleri tutuyor).

## Yalnız yerelde olan eserler

| # | Eser | Kaynak | Bölüm | Paragraf | Cümle | Neden yerelde |
|---:|---|---|---:|---:|---:|---|
| 1 | el-Mesnevî el-Arabî en-Nurî (harekeli) | `rasaelalnour/mesnevi` | 130 | 2.023 | 7.020 | Abdülkadir Badıllı'nın "el-Kâmil" baskısı (harekeli); yalnızca kullanıcıda, genel sunucuya çıkmaz. |
| 2 | Siracü'n-Nur (Hayrat) | `risale_online/siracun-nur` | 250 | 1.349 | 1.848 | Hayrat baskısı; Onikinci Şuâ'ya bağlı belgeler (raporlar, müdafaalar) yalnız burada. Yalnızca kullanıcıda. |
| 3 | Esasat-ı Nuriye | `risaleoku_app/esasat` | 56 | 4.648 | 4.782 | Sonradan derleme: Rüşdü Tafral ve İttihad İlmî Araştırma Heyeti (İttihad Yayıncılık); Bediüzzaman'ın tertibi değil. |
| 4 | Hizmet Rehberi ve Düsturları | `risaleoku_app/hizmettoplama` | 166 | 5.499 | 3.219 | Sonradan derleme: Ahmet Koçoğlu (2018); Bediüzzaman'ın tertibi değil. |

## Eser olmayan yerel veriler

Ham kaynak verisi hiçbir zaman sunucuya gitmez.

| `data/raw/` | Boyut | Durum |
|---|---:|---|
| `erisale` | 112 MB | Kullanımda: genel sunucunun birincil kaynağı |
| `risaleoku_app` | 19 MB | Kullanımda: genel sunucu |
| `kesif` | 23 MB | Kullanımda: Ta'likat'ın Türkçesi |
| `tanzil` | 6 MB | Kullanımda: Kur'ân katmanı |
| `risale_online` | 31 MB | Yalnız yerel Siracü'n-Nur (Hayrat) |
| `kullanici` | 198 MB | Rumuzat-ı Semaniye sunucuda; Kızıl İcaz'ın Türkçe PDF'i yalnız yerelde, ayrıştırılmadı (Aşama 17) |
| `rasaelalnour` | 3 MB | Yalnız yerel harekeli Mesnevî; izin vermedi, sunucuya çıkmaz |
| `qurancom` | 1 MB | Yalnız yerel harekeli Mesnevî'deki âyetlerin çözümü |
| `kastamonur` | 1 MB | Telif tarihi sayfaları kullanımda; Nutuk ve Makalat artık risaleoku'dan; izin var (`docs/izinler.md`) |
| `risaleoku` | 2 MB | Kullanılmıyor: sitenin kapanan eski sayfaları, karşılaştırma için |
| `yeniasya` | 5 MB | Kullanılmıyor: bozuk kodlu PDF metni, karşılaştırma için |

Anlamsal aramanın 16.865 vektörü de yalnız yereldedir: `scripts/deploy.sh` sunucuya süzülmüş kopyayı gönderir (`embeddings export-public`).
