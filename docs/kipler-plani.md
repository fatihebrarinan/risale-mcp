# Kipler ve kapsam (S13.12)

Kısa tasarım belgesi. Durum ve sıra `PLANLAR.md` › S13.12'dedir; bu belge yalnız fikri ve kararları tutar.

## Neden

Beş hata ayıklama turunda (S13.11) Haiku'nun kalıcı hataları aynı yere çıktı: bir konunun **bütün** yerlerini
bulmak. "Tek hâşiye" (15 vardı), "tezekkür iki yerde" (4), "İhlâs Risalesi ayrı bir eser" (Lem'alar 20–21). Okumak ve
yazmak çoğu zaman iyi; kapsam zayıf. Kapsam belirlenimci bir iştir: sunucu yapar, model önüne konan sınırlı bir dosya
üzerinde okur ve yazar.

## İki eksen

- **Kip**: ne yapılıyor. Konu taraması, âyet çalışması, hadis kontrolü, kavram ve terim, karşılaştırma, ders, beni
  sına, müzakere, serbest soru (varsayılan, bugünkü akış).
- **Kapsam**: nerede aranıyor. Risale; Kur'ân ve tefsir; hadis; klasik; ileride ilgili kaynaklar, tercümeler, başka
  alanlar. Her kipin varsayılanı vardır, okuyucu açıp kapatır.

## Kavramlar

- **Birim**: her kütüphanenin atıf birimi (Risale'de cümle ve bölüm, Kur'ân'da âyet, tefsirde âyet birimi, hadiste
  rivayet, klasikte bölüm, lügatta madde), aynı biçimde: kimlik, atıf, sahibi ve katmanı (müellif, talebe imzası,
  nâşir, müfessir, muhakkik, Zehebî…), dil, tercüme mi, kaynak ve izin. Etiketi sunucu koyar, model hatırlamaz.
- **Dosya**: sunucunun bir soru için topladığı adaylar, her birinin **neden** geldiğiyle (başlıkta geçiyor, kaç
  cümlede kelime geçiyor, anlamca ne kadar yakın, adıyla anılıyor) ve en yakın birkaç cümlesiyle. Dosya kütüphaneden
  bağımsızdır.
- **Bağ yürüyüşü**: kütüphaneler arası geçiş ortak adreslerle ve bağ tablolarıyla, modelsiz (konu → Risale bölümleri
  → âyetleri → tefsir birimleri; hadisleri → rivayetler; andığı klasikler). Ortak âyet ilişki değildir: dosya "ortak
  adres" der, ilişkiyi model kurarsa yorumdur.
- **Kip kaydı**: tarif (aramalar, sıra, çıktı biçimi, sunucunun denetimleri, sona eklenen mekanik listeler).
  **Tek kaynaktır**: sohbet talimatının kip parçaları, MCP hazır komutları ve eklentinin skill'leri ondan üretilir.
- **Yönlendirici** (ileride): sorudan `{kip, kapsam}`; açık seçim de yönlendirici de aynı tarifi çağırır.

## Yalınlık ilkesi

Kipler ve dosya yalnız seçilen kipte çalışır. Serbest soru bugünkü yoldur; yeni kütüphane eklemek onun kapsamını
değiştirmez (varsayılan Risale). Basit soruya yalnız küçük ortak araçlar dokunur (risale adları, bölümün imzası,
bölüm künyesi). Her aşama tek başına işe yarar.

## Kararlar (kullanıcı, 2026-11-26)

1. Kip şimdilik açık seçimle; altyapı otomatik seçime göre kurulur.
2. Konu taramasının sonunda mekanik aday listesi ("Konunun geçtiği öbür yerler", "aday" diye) uygun.
3. Ad dizini ve kavram listesi sohbet ederken büyür; ayrı onay turu yok.
4. Kip kaydı tek kaynak.
5. Çok kütüphaneye erişim (süreç içi kopya ya da uzak çağrı) ikinci kütüphane aşamasında ölçerek seçilir.

## Aşamalar

0. Bu belge.
1. Ortak çekirdek, yalnız Risale: risale adları, bölümün imzası, bölüm künyesi; birim ve dosya yapısı; kip kaydı;
   taramanın kapsam ölçümü (modelsiz); sohbette konu taraması kipi.
2. İkinci kütüphane: erişim kararı, alan adlı işaret (`[[tefsir:…]]`), çok alanlı denetim, âyet çalışması kipi.
3. Ders (Word), sına, müzakere, kavram, karşılaştırma.
4. Yönlendirici: önce öneri, sonra otomatik.

## Ölçüm

Her katman ayrı: kütüphane başına kapsam (beklenen birimlerin kaçı dosyada; modelsiz, bedava), cevabın atıfları, kip
başına konuşma setleri (`tests/golden/sohbet_konusmalar/`, `## ad [kip: …]`), yönlendirici için soru → kip seti
(kullanıcıların sorularından değil, bizim yazdığımız setlerden: konuşmaları ekip okumaz).
