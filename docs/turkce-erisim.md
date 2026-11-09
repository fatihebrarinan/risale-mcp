# Türkçe erişim (Y0.4; kullanıcının kararlarıyla, 2026-11-05)

> **Donduruldu (2026-11-09).** Bu belge ayrıntı ve geçmiştir; güncel durum ve sıra `PLANLAR.md`'de.

Yol haritasının Y0.4 adımı (`docs/tefsir-pilot-degerlendirme.md`): müfessirlerin eserleri Arapça kaldıkça altyapı
yalnız Arapça okuyana açık olur (pilotta kullanıcı B bölümünde Arapçayı ayırt edemedi; Türk kullanıcının çoğu da
öyle). Karar: hangi yol, hangi şartla, hangi sunucuda. Âyet dosyası pilotundan (Y1.8) önce verilmeli.

## 1. Yollar

| | (a) İzinli Türkçe tercüme | (b1) Sohbette modelin tercümesi | (b2) Kütüphanede saklanan model tercümesi |
|---|---|---|---|
| Ne | Yayımlanmış bir tercüme, yayıncının izniyle, eserin yanında ayrı katman (mütercimin adıyla, paralel kimlik) | Model, Arapça cümleyi okuyan kullanıcıya sohbette Türkçe anlatır; hiçbir yere yazılmaz | Her cümlenin model tercümesi bir kez üretilir, veride durur, araçlar verir |
| Doğruluk | Mütercimin; kaynak gösterilerek atfedilebilir | Her sohbette yeniden; hata olabilir, denetlenmez | Bir kez üretilir, denetlenebilir; ama hatası her kullanıcıya gider |
| Yetki görüntüsü | Doğru: bir insanın tercümesi | Düşük: sohbetin parçası, damgalı | **Yüksek**: veride durduğu için kaynak gibi görünür; "yapay zekânın yazdığı bir âlime ya da esere mal edilmez" ilkesiyle gerilim |
| Maliyet ve hız | İzin yavaş ve belirsiz (HA4'teki gibi); tercümenin cümle cümle Arapçaya hizalanması iş ister | Yok; bugün de mümkün | Üretim ücreti, denetim yükü, her bölücü değişikliğinde yeniden |
| Kapsam | Yalnız izin verilen eser | Her eser | Her eser |

## 2. Yayımlanmış tercümeler (aday; doğrulanmadı)

Arama sonuçlarından; künyeler, tamlık ve hak sahibi izin istemeden önce doğrulanmalı.

- **Beyzâvî:** Işık Yayınları, "Beydavi Tefsiri", 3 cilt, 2.328 sayfa, 2013 (tam tercüme olup olmadığı kayıtta
  yazmıyor; [1000kitap](https://1000kitap.com/kitap/beydavi-tefsiri-3-kitap--334495)). 2010'da bir tercümenin
  çıktığı haberi ([Timeturk](https://www.timeturk.com/tr/2010/09/16/bir-tefsir-klasigi-turkce-ye-kazandirildi.html)),
  yayıncısı belirtilmemiş.
- **Keşşâf:** Türkiye Yazma Eserler Kurumu, metin ve tercüme, 5 cilt, 2017 (tercüme Muhammed Coşkun, Âdil Bebek,
  Abdülaziz Hatip, Murat Sülün; editör Murat Sülün; [Bilecik Üniversitesi kataloğu](https://katalog.bilecik.edu.tr/bib/61509)).
  Ekin Yayınları, Harun Ünal tercümesi, 6. cilt 2022 ([1000kitap](https://1000kitap.com/kitap/el-kessaf-6-cilt--355513)).
  TYEK bir devlet kurumudur; metin ve tercümeyi birlikte verdiği için hizalama kolaylaşabilir, izin için ilk aday.

## 3. Öneri

Üç katman, her biri kendi yerinde:

1. **Şimdi (b1), kuralla.** Tefsir eserinin bulunduğu her sunucuda (bugün yalnız yerel; ileride tefsir sunucusu)
   talimat: Arapça okumayan kullanıcıya cümlenin anlamını aktarırken bunun modelin tercümesi olduğunu söyle;
   alıntı bloğunda yalnız Arapça asıl durur, tercüme ayrı satırda ve damgalı ("yapay zekâ tercümesi"); `cite`'a
   ve kaynakçaya girmez, müfessire mal edilmez, mealin ya da metnin yerine geçmez. Âyet dosyası pilotunda (Y1.8)
   Türkçe yardım da bu biçimde, damgalı başlık altında.
2. **Kütüphanede model tercümesi saklanmaz (b2 yok).** Kütüphane yalnız kaynakların metnini tutar; veride duran
   yapay zekâ metni kaynak gibi görünür. Tek istisna denetim arayüzüdür (Y1.4): Risale denetçisi gibi Arapçası
   sınırlı birine örneklemde yardımcı tercüme gösterilebilir, damgalı ve geçici (arayüz dosyasında, kütüphanede
   değil); karar yine Arapça asla verilir.
3. **Uzun vadede (a), seçilmiş eserlerde.** İzin, Keşşâf için TYEK'ten başlar (Y1.7 ile birlikte; metni zaten
   alacağımız ikinci eser), Beyzâvî için yayıncı doğrulanınca. İzin gelirse tercüme ayrı eser ya da katman olur
   (`Work.translation`, mütercim `translator`; Risale'deki aslı Arapça eserler gibi paralel kimlik), sunucu atıfla
   verir. HA4'ün usulü: izin gelmeden başlanmaz.

## 4. Kararlar (kullanıcı, 2026-11-05)

1. Üç katman kabul: sohbette damgalı model tercümesi; kütüphanede model tercümesi saklanmaz; uzun vadede izinli
   tercümeler.
2. Damga: "yapay zekâ tercümesi".
3. Denetim arayüzünde Arapçası sınırlı denetçiye geçici, damgalı yardımcı tercüme gösterilir (kütüphanede değil).
4. İzinli tercümeler yalnız tefsirin değil bütün alanların meselesi (hadis kitapları, eklenecek tefsirler, aslı
   Arapça eserler): hem Türk kullanıcı için hem denetçinin yanında ikinci bir güvence olarak. Ayrı bir tercüme
   programıyla ele alınır (öneri sohbette, kullanıcının onayını bekliyor).

Neden saklanmıyor: saklanan model tercümesi araç sonucunda Arapçanın yanında aynı yapıda gelir; model alanları
karıştırabilir (nâşir mealleri için ayrı talimat gerekmişti), metin kopyalanıp dolaşınca kaynağı unutulur. Sohbetteki
tercüme o sohbetle sınırlıdır. Bedeli: saklanan tercüme denetlenebilir ve tutarlı olurdu; bu bilerek bırakıldı.
