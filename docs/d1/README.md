# İşârât usulüyle yapay zekâ taslağı (D1–D5)

Durum, sıra ve kararlar `PLANLAR.md`'dedir (D1 prova, D2 aynı prova E2'nin eserleriyle, D3 başka türden bir birim,
D4 okuma ve not platformu, D5 asıl iş). Bu klasör işin açık belgeleridir; taslaklar burada durmaz.

## Belgeler

| Dosya | Ne |
|---|---|
| `usul-ozeti.md` | İşârât'ın bir âyette ne yaptığının kendi metninden dökümü (ikinci sürüm, Arapça asla dayanır). Okur sürümü `python3 scripts/d1-okur.py` → `site/taslak/isarat-usulu.html` ve `.pdf` |
| `birim-cizelgesi.md` | Arapça aslın birim birim çizelgesi (239 adres) |
| `okuma-notlari.md` | Tam okumanın notları, birim birim |
| `prova-istemi.md` | Taslağı yazan modelin istemi (sürümlü; `@tam`/`@ince` satırları) |

Alıntılar ve adresler veritabanıyla denetlenir: `python3 scripts/d1-usul-denetim.py [dosya]`.

## Kapalı olanlar: `data/d1/`

Taslaklar, dökümler, okuma sayfası ve okuyucuların notları yeniden üretilemez ve yayımlanmaz. Ayrı bir git deposunda
durur (`data/d1/.git`; ana depo onu görmez), uzak kopyası özel depodadır. Ayrıntı `data/d1/README.md`.

## Akış

```
uv run python scripts/d1-prova.py hazirla 11-12 --istem ince   # prova veritabanları, ekler, istem, sızıntı testi (data/interim/d1-prova/)
uv run python scripts/d1-prova.py yazdir 11-12 --istem ince    # bir taslak daha (data/d1/provalar/11-12/taslak-<n>)
uv run python scripts/d1-prova.py karsilastir 11-12            # ortak diziler, gizlenen metin
uv run python scripts/d1-prova.py okuma                        # data/d1/okuma.html: bütün birimler ve taslaklar
uv run python scripts/d1-prova.py notlar ~/İndirilenler/d1-notlar-*.json   # okuyucuların notları → notlar.md
```

## Okuma sayfası (D4)

`data/d1/okuma.html` tek dosyadır, internet gerektirmez; masaüstü tarayıcıda açılır.

- Üstte birim, kip (taslak ile İşârât'ın gizlenen metni ya da taslak ile taslak), taslak ve dil seçilir.
- Paragrafın yanındaki ✎ ile not: tür (doğru, yanlış, eksik, fazla, uydurma, i'râb, belâgat, usul, kaynak, üslûp),
  önem ve "ehline sor" işareti. Başlıktaki "bölüme not" eksik kalan şeyler içindir. İşârât'ın paragrafına da not
  konabilir ("taslak bunu kaçırdı").
- Taslaktaki `[14]` gibi bir kaynağa tıklanınca dayandığı metnin kendisi açılır.
- Sarı kelimeler gizlenen metinle ortak 6 kelimelik dizilerdir (ezber şüphesi; çoğu geçiş kalıbı).
- "Ölçüt çizelgesi" her taslak için 0–2 puan ve kısa gerekçe (D1.4'ün ölçütleri).
- Notlar tarayıcıda saklanır. **"Notları dışa aktar"** bir `.json` dosyası indirir; okuyucu onu geri gönderir,
  `notlar` komutu `data/d1/notlar/`a alır ve birim başına `notlar.md` raporunu yazar. "İçe aktar" başka bir okuyucunun
  dosyasını sayfada gösterir.

Okuyucuya gönderirken: dosya taslakları taşır, yalnız davet edilen kişiye dosya olarak gönderilir, açık bir adrese
konmaz.
