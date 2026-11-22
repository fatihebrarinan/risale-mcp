# E8: Arapça Külliyat için izin e-postası (taslak, 2026-11-22)

`PLANLAR.md` E8 "Arap dünyasına açılmak": ilk adım, külliyatın Arapça tercümesini kullanmak için hak sahibinden
izin. Taslak Claude'un, gönderen kullanıcı.

**Ne biliniyor (2026-11-22):**
- Tercüme İhsan Kasım es-Sâlihî'nindir: risaleoku'daki Arapça ciltlerin kapağı `كليات رسائل النور › ترجمة إحسان
  قاسم الصّالحي` (`data/raw/risaleoku_app/ar_sozler/`, `ar_mektubat`, `ar_lemalar`, `ar_sualar`, `ar_tarihce`,
  `ar_lahikalar`; indirildi, ayrıştırılmadı). Tarihçe'nin takdimi Mustafa Sungur'un.
- Yayıncı Sözler Neşriyat'tır (شركة سوزلر للنشر, İstanbul ve Kahire): kitap kayıtları ve akademik kaynakçalar
  böyle anıyor. Mütercim 2020'lerde de etkin (Üsküdar Üniversitesi RİNAP programı).
- **Hak sahibinin kim olduğu doğrulanmadı** (yayınevi mi, mütercim mi, ikisi mi). Basılı bir cildin künye sayfasına
  bakılmalı ("حقوق الطبع محفوظة لـ…"); e-posta adresi yayınevinin kendi sitesinden ya da künyeden alınır, burada
  tahmin edilmez. Mütercime RİNAP (Üsküdar Üniversitesi) aracılığıyla da ulaşılabilir.
- risaleoku'nun izni bütün içeriğini kapsar, ama başkasının telifli tercümeleri bu izne dayanılarak alınmıyor
  (`docs/izinler.md`). İşârât'ın ve Mesnevî'nin Arapça asıllarını bugün İhsan Kasım'ın tahkikli baskısından
  (risaleoku) veriyoruz: e-postada bunu da açıkça söylüyoruz.
- Hizmet Vakfı (rasaelalnour.com) 2026-10-30'da izin vermemişti; o mesele kapalıdır ve bu e-posta ona gitmez.

**Göndermeden önce doldurulacaklar:** alıcı adresi, [adınız], [telefon] (isteğe bağlı). Arapçasını isterseniz
ayrıca hazırlarım; yayınevi Türkiye'de olduğu için ilk e-posta Türkçe.

**İzin gelirse:** `docs/izinler.md` ve `catalog/permissions.py`, eser kataloğa (`authority: muellif`,
`translation`, `translator: İhsan Kasım es-Sâlihî`), Arapça metin ayrıştırma, Türkçeyle paralel kimlikler; sitenin
ve talimatın Arapçası sonra.

## Taslak

**Alıcı:** Sözler Neşriyat [adres künyeden ya da yayınevinin sitesinden]; mümkünse bilgi olarak Üstad İhsan Kasım
es-Sâlihî

**Konu:** Külliyat-ı Resâili'n-Nûr'un Arapça tercümesinin yapay zekâ ile kaynağa bağlı kullanımı için izin talebi

Muhterem Sözler Neşriyat yetkilileri,

Selamün aleyküm. Ben [adınız]. Risale-i Nur'u yapay zekâ modellerinin kaynağa sadık kalarak kullanabilmesi için
ücretsiz ve ticari olmayan bir araç geliştiriyorum: Risale MCP (https://risalemcp.com).

Araç, Claude ve ChatGPT gibi bir yapay zekâ modeline bağlanan bir "MCP sunucusu"dur. Model, Risale-i Nur hakkında
bir soruya cevap verirken metni bu sunucudan okur ve dayandığı her yeri cümle düzeyinde, eser › bölüm › cümlenin
ilk kelimeleri şeklinde tam adresiyle gösterir. Amaç, modelin Risale-i Nur'a dair uydurma ya da kaynaksız söz
söylemesini önlemek, yorumunu metindeki cümlelere bağlamaktır. Bugün Bediüzzaman'ın bütün eserleri Türkçe
asıllarıyla, aslı Arapça eserler de Arapçalarıyla araçta bulunuyor. Metinleri kaynağını göstererek, izin veren
sitelerden (e-Risale, risaleoku.com) alıyoruz.

Arapça konuşan okuyucuların da Risale-i Nur'u bu araçla, kendi dillerinde ve kaynağına bağlı olarak okuyabilmesini
çok istiyoruz. Bunun için en sağlam yolun, Üstad İhsan Kasım es-Sâlihî'nin Külliyât-ı Resâili'n-Nûr tercümesi
olduğunu düşünüyoruz. Bu sebeple sizden şu hususlarda izin ve yardım istiyorum:

1. Külliyat'ın Arapça tercümesini (el-Kelimât, el-Mektûbât, el-Lem'ât, eş-Şuââ', es-Sîretü'z-Zâtiyye,
   el-Melâhık ve öbür ciltler) bu araçta kullanma izni.
2. Metni risaleoku.com'daki nüshadan alabilir miyiz, yoksa sizin tercih ettiğiniz bir dijital nüsha mı
   kullanmalıyız? Hangisini uygun görürseniz ona uyarız.
3. Hak sahibi siz değilseniz ya da Üstad İhsan Kasım'ın da izni gerekiyorsa, kime yazmamız gerektiğini
   bildirirseniz minnettar oluruz.

Kullanımla ilgili birkaç hususu açıkça belirtmek isterim:
- Metin bir web sitesinde okunacak şekilde yayımlanmaz; model yalnızca sorulan soruyla ilgili bölümleri okur ve
  cevabında kısa alıntılarla, tam adresiyle kullanır.
- Her atıfta mütercim ve yayınevi açıkça yazılır ("ترجمة: إحسان قاسم الصالحي، شركة سوزلر للنشر"). Metin
  değiştirilmez. Modelin kendi yaptığı her tercüme "yapay zekâ tercümesi" diye ayrıca işaretlenir ve sizin
  tercümenizle karıştırılmaz.
- Hiçbir ticari amacı ve geliri yoktur; sunucu masrafını kendim karşılıyorum.
- Uygun görürseniz kitaplarınızın satın alınabileceği yere bağlantı veririz.
- Şunu da bilgi olarak arz edeyim: İşârâtü'l-İ'câz'ın ve el-Mesnevî el-Arabî en-Nûrî'nin Arapça asıllarını bugün
  Üstad İhsan Kasım'ın tahkikiyle, risaleoku.com'daki nüshadan veriyoruz. Bunun için de bir şartınız varsa
  bildirmenizi rica ederim.
- Bir şartınız varsa ona uyarım; kullanımı uygun görmezseniz tercümeyi araca eklemem.

Aracın nasıl çalıştığını görmek isterseniz tanıtım ve kurulum sayfası: https://risalemcp.com. İsterseniz kısa bir
örnek de gönderebilirim.

Risale-i Nur'un Arap dünyasına ulaşmasındaki hizmetlerinizden dolayı Allah razı olsun.

Saygılarımla,
[adınız]
[e-posta]
[telefon]
