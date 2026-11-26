# Yerelde olup sunucuda olmayan veriler

> Bu dosya `uv run python -m risale_mcp.local_only` ile üretilir (`build` sonunda da); elle düzenlemeyin.
> Bir eseri yerelde tutan `Work.private` işaretidir: `src/risale_mcp/catalog/`. İzinler: `docs/izinler.md`.

| Veritabanı | Eser | Bölüm | Paragraf | Cümle | Arapça parça |
|---|---:|---:|---:|---:|---:|
| Yerel (`data/dist/kisisel/`) | 98 | 58.872 | 461.553 | 884.460 | 72.063 |
| Sunucu (`data/dist/genel/`) | 69 | 9.002 | 107.210 | 242.696 | 25.566 |
| **Fark** | **29** | **49.870** | **354.343** | **641.764** | **46.497** |

Ortak eserlerde metin aynıdır (JSON özetleri tutuyor).

## Yalnız yerelde olan eserler

| # | Eser | Kaynak | Bölüm | Paragraf | Cümle | Neden yerelde |
|---:|---|---|---:|---:|---:|---|
| 1 | el-Mesnevî el-Arabî en-Nurî (harekeli) | `rasaelalnour/mesnevi` | 130 | 2.023 | 7.020 | Abdülkadir Badıllı'nın "el-Kâmil" baskısı (harekeli); yalnızca kullanıcıda, genel sunucuya çıkmaz. |
| 2 | Siracü'n-Nur (Hayrat) | `risale_online/siracun-nur` | 250 | 1.349 | 1.848 | Hayrat baskısı; Onikinci Şuâ'ya bağlı belgeler (raporlar, müdafaalar) yalnız burada. Yalnızca kullanıcıda. |
| 3 | Esasat-ı Nuriye | `risaleoku_app/esasat` | 56 | 4.648 | 4.782 | Sonradan derleme: Rüşdü Tafral ve İttihad İlmî Araştırma Heyeti (İttihad Yayıncılık); Bediüzzaman'ın tertibi değil. |
| 4 | Hizmet Rehberi ve Düsturları | `risaleoku_app/hizmettoplama` | 166 | 5.499 | 3.219 | Sonradan derleme: Ahmet Koçoğlu (2018); Bediüzzaman'ın tertibi değil. |
| 5 | Câmiu'l-Beyân | `openiti/taberi-shamela` | 3.997 | 10.939 | 39.924 | OpenITI Shamela0007798 (Dâru Hecr, 1422); âyet birimleri altafsir.com sürümünden (MVP, `books/tefsir_openiti.py`). |
| 6 | Te'vîlâtü'l-Kur'ân | `openiti/maturidi-shamela` | 1.228 | 46.160 | 53.769 | OpenITI Shamela0095590 (Dâru'l-Kütübi'l-İlmiyye, 1426); âyet birimleri altafsir.com sürümünden (MVP, `books/tefsir_openiti.py`). |
| 7 | el-Keşşâf | `openiti/kessaf-shamela` | 3.064 | 8.718 | 33.869 | OpenITI Shamela0023627 (Dâru'l-Kitâbi'l-Arabî, 3. baskı 1407); âyet birimleri altafsir.com sürümünden (MVP, `books/tefsir_openiti.py`). |
| 8 | Mefâtîhu'l-Gayb | `openiti/razi-shamela` | 3.473 | 32.192 | 52.106 | OpenITI Shamela0023635 (Dâru İhyâi't-Türâs, 3. baskı 1420); âyet birimleri altafsir.com sürümünden (MVP, `books/tefsir_openiti.py`). |
| 9 | el-Câmi' li-Ahkâmi'l-Kur'ân | `openiti/kurtubi-shamela` | 3.361 | 8.418 | 111.898 | OpenITI Shamela0020855 (Dâru'l-Kütübi'l-Mısriyye, 2. baskı 1384); âyet birimleri altafsir.com sürümünden (MVP, `books/tefsir_openiti.py`). |
| 10 | Envârü't-Tenzîl | `openiti/beyzavi-shamela` | 3.447 | 11.753 | 24.283 | Envârü't-Tenzîl ve Esrârü't-Te'vîl. OpenITI Shamela0023588 (Maraşlî tahkiki, Dâru İhyâi't-Türâsi'l-Arabî, 1418). Eserin tamamı (MVP; pilot T3'te Bakara 33'e kadardı). |
| 11 | Medâriku't-Tenzîl | `openiti/nesefi-shamela` | 1.067 | 16.791 | 16.134 | OpenITI Shamela0001394 (Dâru'l-Kelimi't-Tayyib, 1419); âyet birimleri altafsir.com sürümünden (MVP, `books/tefsir_openiti.py`). |
| 12 | Tefsîru'l-Kur'âni'l-Azîm | `openiti/ibnkesir-shamela` | 2.002 | 25.708 | 55.204 | OpenITI Shamela0008473 (Dâru Tayyibe, 2. baskı 1420); âyet birimleri altafsir.com sürümünden (MVP, `books/tefsir_openiti.py`). |
| 13 | Tefsîru'l-Celâleyn | `openiti/celaleyn-shamela` | 6.231 | 12.278 | 12.318 | OpenITI Shamela0012876 (Dâru'l-Hadîs, Kahire); âyet birimleri altafsir.com sürümünden (MVP, `books/tefsir_openiti.py`). |
| 14 | ed-Dürrü'l-Mensûr | `openiti/durr-shamela` | 2.185 | 61.408 | 61.398 | OpenITI Shamela0012884 (Dâru'l-Fikr, Beyrut); âyet birimleri altafsir.com sürümünden (MVP, `books/tefsir_openiti.py`). |
| 15 | İrşâdü'l-Akli's-Selîm | `openiti/ebussuud-shamela` | 2.396 | 18.177 | 18.603 | OpenITI Shamela0001429 (Dâru İhyâi't-Türâs, Beyrut); âyet birimleri altafsir.com sürümünden (MVP, `books/tefsir_openiti.py`). |
| 16 | Rûhu'l-Beyân | `openiti/bursevi-shamela` | 6.024 | 6.320 | 25.105 | OpenITI Shamela0023612 (Dâru'l-Fikr, Beyrut); âyet birimleri altafsir.com sürümünden (MVP, `books/tefsir_openiti.py`). |
| 17 | Rûhu'l-Meânî | `openiti/alusi-shamela` | 6.150 | 23.101 | 47.600 | OpenITI Shamela0022835 (Dâru'l-Kütübi'l-İlmiyye, 1415); âyet birimleri altafsir.com sürümünden (MVP, `books/tefsir_openiti.py`). |
| 18 | el-Fıkhu'l-Ekber | `openiti/fikhul-ekber` | 27 | 39 | 39 | OpenITI Shamela0006388 (Furkân 1419; Aliyyü'l-Kārî'nin şerhinden ayıklanmış metin, başlıklar yayıncının). |
| 19 | Delâilü'l-İ'câz | `openiti/delailul-icaz` | 760 | 3.023 | 4.507 | OpenITI Shamela0012055 (Medenî, 3. baskı 1413). Muhakkikin fıkra numaraları düğümdür. |
| 20 | Esrârü'l-Belâğa | `openiti/esrarul-belaga` | 36 | 1.257 | 1.635 | OpenITI Shamela0008187 (Medenî; muhakkik satırı boş). Sürümün sonunda son paragrafın devamı eksik. |
| 21 | el-Müfredât fî Garîbi'l-Kur'ân | `openiti/mufredat` | 1.630 | 2.392 | 4.494 | OpenITI JK001150 (Kîlânî, Dâru'l-Ma'rife). Harf kitabı ve madde (kök) düğümdür. Dâvûdî baskısının Shamela sürümünde madde başlığı işareti kelimelerin içine girmiş, metin kurulamıyor. |
| 22 | İhyâu Ulûmi'd-Dîn | `openiti/ihya` | 645 | 19.519 | 19.519 | OpenITI JK000001 (Dâru'l-Ma'rife, Beyrut; muhakkik yazılmamış). Irâkî'nin hadis tahrici metinden ayrıldı, şerh olarak geçtiği cümleye bağlı. Başlıklar aynı baskının Shamela0009472 sürümünün içindekilerinden. |
| 23 | el-Munkız mine'd-Dalâl | `openiti/munkiz` | 1 | 31 | 327 | OpenITI ShamAY0033739 (Câbir, el-Mektebetü's-Sekâfiyye). Sürümde başlık yok: eser tek bölümdür. |
| 24 | Miftâhu'l-Ulûm | `openiti/miftahul-ulum` | 130 | 1.386 | 2.237 | OpenITI Shamela0026581 (Dâru'l-Kütübi'l-İlmiyye, 2. baskı 1407; muhakkik yazılmamış). |
| 25 | et-Telvîh ilâ Keşfi Hakāiki't-Tenkîh | `openiti/telvih` | 199 | 2.028 | 2.028 | OpenITI JK007110 (Umeyrât, Dâru'l-Kütübi'l-İlmiyye 1416): yalnız Teftâzânî'nin şerhi; Sadrüşşerîa'nın Tavzîh'i yok, "قوله" ile anılır. Başlıklar aynı baskının ShamAY0034200 sürümünün içindekilerinden. |
| 26 | Şerhu'l-Makāsıd | `openiti/serhul-makasid` | 126 | 1.177 | 1.183 | OpenITI JK001157 (Nu'mâniyye, Lahor 1401; muhakkik yazılmamış). Başlık satırı yok: bölümler Teftâzânî'nin kendi metnini "قال" ile aktardığı yerlerden. |
| 27 | et-Ta'rîfât | `openiti/tarifat` | 30 | 2.088 | 2.275 | OpenITI Shamela0007312 (Dâru'l-Kütübi'l-İlmiyye, 1403; "ضبطه وصححه جماعة من العلماء بإشراف الناشر"). |
| 28 | Şerhu'l-Mevâkıf | `openiti/serhul-mevakif` | 705 | 14.291 | 14.344 | OpenITI ShamAY0033881 (Umeyre, Dâru'l-Cîl 1417; OpenITI'de Îcî'nin adı altında "المواقف"). Îcî'nin metni baskının "المتن" diye ayırdığı yerde ayrı katmandır. Başlıklar Şâmile'nin içindekilerinden. |
| 29 | el-Mevâhibü'l-Ledünniyye | `openiti/mevahib` | 354 | 11.630 | 20.096 | OpenITI Shamela0023685 (Tevfîkıyye, Kahire; muhakkik yazılmamış). |

## Eser olmayan yerel veriler

Ham kaynak verisi hiçbir zaman sunucuya gitmez.

| `data/raw/` | Boyut | Durum |
|---|---:|---|
| `erisale` | 112 MB | Kullanımda: genel sunucunun birincil kaynağı |
| `risaleoku_app` | 21 MB | Kullanımda: genel sunucu |
| `kesif` | 23 MB | Kullanımda: Ta'likat'ın Türkçesi |
| `tanzil` | 6 MB | Kullanımda: Kur'ân katmanı |
| `risale_online` | 31 MB | Yalnız yerel Siracü'n-Nur (Hayrat) |
| `kullanici` | 206 MB | Rumuzat-ı Semaniye sunucuda; Kızıl İcaz'ın Türkçe PDF'i yalnız yerelde, ayrıştırılmadı (Aşama 17) |
| `rasaelalnour` | 3 MB | Yalnız yerel harekeli Mesnevî; izin vermedi, sunucuya çıkmaz |
| `qurancom` | 1 MB | Yalnız yerel harekeli Mesnevî'deki âyetlerin çözümü |
| `kastamonur` | 1 MB | Telif tarihi sayfaları kullanımda; Nutuk ve Makalat artık risaleoku'dan; izin var (`docs/izinler.md`) |
| `nurpedia` | 9 MB | Ham sayfalar yerelde: hadis işaretleri ve künyeleri (Aşama 14); sunucuya yalnız sonuçları çıkar |
| `sanadset` | 1.431 MB | Hadis katmanı (Aşama 14): CC BY 4.0, eşleşen rivayetler sunucuya gider |
| `hadith_api` | 44 MB | Hadis katmanı (Aşama 14): Unlicense; âlimlerin dereceleri |
| `openiti` | 606 MB | Hadis kitapları (Kütüb-i Sitte, Muvatta; bâblı): CC BY-NC-SA 4.0, kitaplar yerelde; okumayla bulunan rivayetler sunucuda (`docs/izinler.md`) |
| `risaleoku` | 2 MB | Kullanılmıyor: sitenin kapanan eski sayfaları, karşılaştırma için |
| `yeniasya` | 5 MB | Kullanılmıyor: bozuk kodlu PDF metni, karşılaştırma için |

Anlamsal aramanın 641.669 vektörü de yalnız yereldedir: `scripts/deploy.sh` sunucuya süzülmüş kopyayı gönderir (`embeddings export-public`).
