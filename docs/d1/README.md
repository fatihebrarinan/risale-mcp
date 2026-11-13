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
| `karsilastirma-istemi.md` | D7 yapay zekâ karşılaştırıcısının istemi (sürümlü): envanter, denetim, eşleştirme |
| `elestiri-istemi.md` | D9 yapay zekâ eleştirmeninin istemi (sürümlü; açık kitap, dört eklenti) |

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

## Yapay zekâ karşılaştırıcısı (D7)

Taslakları İşârât'ın gizlenen metniyle eşleştiren iki kör okuyucu (Fable 5.2 ve Opus 5.5). Eşleştirir, hüküm
vermez; fazladan söyleneni "ehline sor"a koyar. Okuyuculara gösterilmez.

```
uv run python scripts/d1-yz.py envanter 11-12      # cevap anahtarı: Fable çıkarır, Opus denetler → yz/envanter.md
uv run python scripts/d1-yz.py eslestir 11-12      # 3 taslak × 2 model, birbirini görmeden (var olanı atlar; --yeniden)
uv run python scripts/d1-yz.py rapor 11-12         # alıntı denetimi, birleştirme → provalar/11-12/yz-karsilastirma.md
uv run python scripts/d1-prova.py okuma            # okuma.html (okuyuculara) ve okuma-yz.html (yalnız kullanıcıya)
```

## D2: klasik eserlerle aynı prova

D1'in istemi (`v1-ince`) ve me'hazda klasik eserler satırı (`v1-ince-klasik`; `istem-ince-klasik.md` D1'in
`istem-ince.md`'sinden yalnız o üç satır eklenerek kuruldu: `hazirla` yeniden çalıştırılırsa ek dosyalardaki yol
değişiklikleri de girer, D1 ile birebirlik bozulur). Prova sunucularına `klasik` profili eklenir (`mcp-klasik.json`).

```
uv run python scripts/d1-prova.py yazdir 11-12 --istem ince-klasik --kez 3   # taslak 4–6
uv run python scripts/d1-yz.py eslestir 11-12 --taslak 4 5 6                 # D7'nin envanteriyle eşleştirme
uv run python scripts/d1-yz.py kaynak 11-12 --taslak 4 5 6                   # klasik esere dayanış denetimi
uv run python scripts/d1-yz.py rapor 11-12 && uv run python scripts/d1-yz.py d2-veri 11-12   # veri; rapor d2-rapor.md
```

D9 (eleştirmen ve mekanik denetimler, `scripts/d1-elestiri.py`):

```
uv run python scripts/d1-elestiri.py mekanik 11-12    # D9.1: tırnak, âyet lafzı, kendi tespiti, kaçırılan nüktelerin ipucu → d9-mekanik.md
uv run python scripts/d1-elestiri.py elestir 11-12    # D9.2: eleştirmen (Opus 5.5), taslak başına → d9-elestiri.md
uv run python scripts/d1-elestiri.py rapor 11-12      # notların alıntı ve dayanak denetimi, rapor (model çağırmadan)
```

`okuma-yz.html`'de "YZ karşılaştırması" kutusu her paragrafın altına eşleşmeleri ve fazlaları açar; "YZ örneklemi"
30 satırlık sınama listesidir (D7.7): her satır metne bakılarak "metinde tutuyor / kısmen / tutmuyor" diye işaretlenir,
işaretler "Notları dışa aktar" dosyasına girer, `notlar` ile alınır ve `rapor` güven oranını yazar. Ölçü insanla
uyuşmak değil, metne bakınca tutmaktır. Notlarınızı karşılaştırmayı görmeden önce dışa aktarın: iki okuma ayrı kalsın.

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
