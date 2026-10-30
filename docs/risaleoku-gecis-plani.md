# risaleoku.com'a geçiş planı

2026-10-30'da kullanıcının kararı. Site sahibi kazanç olmadığı ve kaynak gösterildiği sürece bütün eserlerin
kullanımına izin verdi ("kullanabilirsiniz, güzel çalışma olmuş, ellerinize sağlık"). Amaç: kaynak çeşitliliğini
azaltmak; izin ve metin tutarlılığını tek kaynakta toplamak.

## Yapılanlar (2026-10-30)

Kullanıcının kararları: Arapça eserler risaleoku'ya geçti, Badıllı'nın harekeli Mesnevî'si yalnız kullanıcıda kaldı;
mecmualar taşındı; sıra Hizbler → Nutuk/Makalat → Arapça → Osmanlıca; Âsâr-ı Bediiyye parçaları, Fihrist, dualar eklendi.

- **Ortak ayrıştırıcı:** `books/risaleoku_app.py`.
- **Taşınan:** Hizbler, Küçük Sözler, Nutuk, Makalat, Zülfikâr, Tılsımlar, Sirâcü'n-Nûr, Gençlik ve Hanımlar Rehberi,
  İşârâtü'l-İ'câz, el-Mesnevî el-Arabî, Kızıl İcaz, Ta'likat, Hutbe (Arapça).
- **Eklenen:** Âsâr-ı Bediiyye (mecmua), Fihrist Risalesi, Hizb-i Nurî (Zülfikâr'ın içinden), Teşhisü'l-İllet'in Zeyli,
  Hakikat Çekirdekleri (İkinci Cüz), Vukufsuz Ehl-i Vukufa Cevap, Namaz Tesbihatı, Celcelutiye, Kenzü'l-Arş,
  16 Osmanlıca cilt; yalnız yerelde Esasat-ı Nuriye ve Hizmet Rehberi.
- **Sayılar:** 72 eser, 256.719 cümle (Osmanlıca dışı 144.853); genel veritabanı 69 eser.

## Açık kalanlar

- **Kur'ân:** sitedeki metin Tanzil'le iskelet olarak 6.235/6.236 aynı, yalnız hat farklı (Risale'nin Türk hattı).
  İstenirse `get_ayah`'a ikinci hat olarak eklenebilir. Meal iki Diyanet mealinden de farklı ve adı belli değil: alınmadı.
- **Osmanlıca kimlikleri** Türkçeyle paralel değil (`sozler-osmanlica/011/001`); paralellik ayrı iş.
- **Mesnevî (Arapça, genel):** İhsan Kasım baskısının düzeni Badıllı'dan farklı; şablonun 19 bölümü yerleşmedi.

## Dikkat

- Cümle kimlikleri kayabilir; her değişimde eski ve yeni metin karşılaştırılır.
- erisale birincil kaynak olarak kalır, bu plan onu değiştirmez (kullanıcı ayrıca karar vermedikçe).

## Bulgular (2026-10-30)

İndirici: `uv run python -m risale_mcp.fetch risaleoku [anahtar…]` (`sources/risaleoku_app.py`). Katalog 559 kitap,
37 raf; arayüzde görünmeyen raflar da var (Envar, Rnk, Sözler, İhlas Nur baskıları). 44 kitap `data/raw/risaleoku_app/`
altında, özetleri doğrulandı.

**Metin biçimi** (satır başı işaretleri, `>` ile kapanır): `#n` sayfa; `<…>` ortalı başlık; `&…` kitap başlığı;
`€`, `∑` üst başlık; `` ` `` iç başlık; `,` ortalı süs/satır; `÷`, `§` imza; `{…}` hâşiye (eski baskılarda metnin içinde);
`~…|n@` Arapça satır (`n` kitap içi sıra); `\…>` satır içi başlık; `∫` paragrafın sürmesi. Yeni baskılarda ve Arapçada
hâşiye `footnotes` dosyasında: `sayfa|işaret|metin`. Fihrist: sekmeyle girintili `başlık[@kısa ad]|sayfa`.

**Eski metinle örtüşme** (5 kelimelik diziler, eskinin yenide bulunan oranı):

| Eser | Yeni kitap | Oran | Not |
|---|---|---|---|
| Nutuk / Makalat | `abed` | %82 / %91 | Makalat'tan 2 paragraf yok |
| Zülfikâr | `ihlas_zulfikar` | %80 | fihrist tek satır; başlıklar metinden |
| Tılsımlar | `ihlas_tilsimlar` | %83 | |
| Sirâcü'n-Nûr | `ihls_siracunnur` | %63 | Hayrat baskısı daha uzun (ör. Sekizinci Hüccet-i Îmâniye yok) |
| Gençlik / Hanımlar Rehberi | `rnk_gencreh`, `rnk_hanimreh` | %82 / %70 | Hanımlar'da 92 paragraf yok |
| İşârâtü'l-İ'câz (Ar.) | `ar_isarat` | %90 | aynı İhsan Kasım metni; harekesiz |
| el-Mesnevî el-Arabî | `ar_mesnevi` | %83 | Badıllı değil, harekesiz (%9); fihrist tek satır |
| Kızıl İcaz / Ta'likat / Hutbe (Ar.) | `ar_asaribediyye` | %87 / %74 / %92 | aynı kitabın içinde; bölünmeli |
| Hizbü Envâr | `hizbulhakaik` | %99 | yeni sürümde 18 başlıklı fihrist |
| Küçük Sözler | `rnk_ksozler` | %88 | |

**Sitede yok:** Kızıl İcaz'ın ve Ta'likat'ın Türkçesi, Hizb-i Nurî, Rumuzat-ı Semaniye.

**Osmanlıca:** 16 cilt (`os*`), harfler Arapça, Arapça satırlar `~`, 156 başlıklı fihrist (Sözler). Raf altyazısı Envar.
