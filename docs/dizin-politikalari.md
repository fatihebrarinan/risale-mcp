# Dizin politikaları (Y0.6; araştırma notu, 2026-11-07)

Soru (yol haritası Y0.6): Claude ve OpenAI dizinleri birden çok bağdaştırıcıya (risale, tefsir, hadis), yazma
araçlarına (katkı: `propose_link`, `report_error`) ve kimlik doğrulamaya nasıl bakıyor; okuma sunucusunun
başvurusu etkilenir mi. Kaynaklar sonda; hepsi web'den okundu, hiçbir yere bir şey gönderilmedi.

## Claude (Anthropic) Connectors Directory

- **Başvuru yolu değişti:** artık geliştirici portalı `claude.ai/directory/manage` ("Submit new › MCP connector").
  Gönderilen başvurunun durumu ve hakem notları orada görünür. Gönderim otomatik taranır, varsayılan olarak
  "Community" bağdaştırıcı olarak listelenir; yararlı bulunanlar sonra "Verified" incelemesine alınır. Bizim
  2026-10'daki başvurumuz eski yoldan gitti: portalda durumuna bakılmalı (kullanıcı).
- **Kimlik doğrulama:** "OAuth 2.0 if your tools act on a user's account, or no authentication for public data".
  Okuma sunucularımız (açık kip, hesapsız) bu kurala uyuyor. Katkı sunucusu kullanıcının hesabıyla iş yapacağı
  için OAuth 2.0 ister; portalda "Required when the server asks" seçeneği var: sunucu girişsiz açılır, yalnız bazı
  araçlar giriş ister. Bu, okuma ve yazmayı tek sunucuda tutmaya da izin verir, ama ayrı sunucu daha temiz (aşağıda).
- **Araç işaretleri:** her araçta `title` ve `readOnlyHint` ya da `destructiveHint` zorunlu. Okuma araçları onaysız
  çalışır, "destructive" araçlar her çağrıda onay ister. Okuma ve yazma aynı araçta olamaz ("A single tool that
  accepts both … is rejected"); yazma araçları işe göre ayrılmalı.
- **Tool açıklamaları:** modele davranış söyleyen açıklama reddedilir: "Instruct Claude to call external software or
  tools the user didn't request", "Interfere with Claude calling other tools", "Direct Claude to pull behavioral
  instructions from external sources". **Bize etkisi:** tefsir ve hadis sunucularının talimatındaki "Risale
  bağdaştırıcısı ekliyse oraya sor" cümlesi araç açıklamasında değil sunucu talimatında; yine de hakem "başka bir
  aracı çağırmaya yönlendirme" sayabilir. Başvurudan önce bilgi kipine çevrilmeli ("metni Risale-i Nur
  sunucusundadır"; çağırmayı emretmeden). Araç açıklamalarımız (find_ayah, get_hadith) yalnız ne verdiğini
  söylüyor; uygun.
- **Veri:** "Don't collect conversation data beyond what the tool needs"; Claude'un hafızası ve geçmişi sorgulanmaz.
  Kullanım kaydımız (araç, süre, hata; parametre yok) uyuyor. Katkı aracı yalnız önerinin kendisini almalı.
- **Gizlilik politikası:** her başvuruda URL istenir; uzak sunucuda yerelin ayrıntılı listesi şart değil ama
  politika veri toplama, saklama, paylaşım, süre ve iletişimi anlatmalı. Tek politika birden çok sunucuyu
  kapsayabilir (kurala aykırı bir şey bulunmadı), her sunucunun ne topladığı içinde yazmalı.
- **Birden çok bağdaştırıcı:** aynı yayıncının birden çok bağdaştırıcısı hakkında bir kural bulunmadı (yasak ya da
  sınır yok). Her biri ayrı başvuru, ayrı listeleme, ayrı slug.
- **Yeni: "Compliance" adımı** yedi onay ister (yönergeler, birinci taraf API, finans, yapay zekâ medya üretimi,
  prompt injection, konuşma verisi toplama, açık belge). "API ownership": sunucu kendi ya da izinli proxy API'sini
  çağırmalı; bizimki kendi verisi (izinli kaynaklardan), "Data handling" adımında "proxied with permission" ya da
  "own" seçilir.

## OpenAI (ChatGPT Apps / plugin dizini)

- Uzak, üretimde çalışan sunucu; "Developer Mode"da denenmiş olmalı; gönderen doğrulanmış kişi ya da kurum.
- **Yazma araçları:** `readOnlyHint: false` dış durumu değiştiren her araçta; silme, üzerine yazma ve geri
  alınamayan gönderimde `destructiveHint: true`. "Annotations don't replace human confirmation for irreversible
  operations"; yan etki gizli olamaz.
- **Kimlik doğrulama:** gerekiyorsa açık ve şeffaf, istenen izinler sınırlı; hakemlere örnek veriyle demo hesabı
  (kayıt ya da iki adımlı doğrulama gerektiren reddedilir). Kimliksiz sunucu için ayrı şart yok.
- **Gizlilik:** yayımlanmış politika (toplanan veri türleri, amaç, alıcılar, saklama süresi, kullanıcı denetimi);
  en az veri ("just in case" alan yok); araç tüm konuşma geçmişini ya da kesin konumu istemez.
- **Birden çok uygulama:** kural bulunmadı.

## Sonuçlar (öneri)

1. **Okuma sunucuları (risale, tefsir, hadis) açık kipte kalabilir:** iki dizin de kamuya açık veride kimlik
   doğrulama istemiyor. Her biri ayrı başvuru; aynı gizlilik politikası her sunucunun verisini ayrı ayrı anlatarak
   hepsini kapsayabilir.
2. **Katkı (Y3) ayrı bir bağdaştırıcı olmalı:** OAuth'lu, yazma araçları `destructiveHint` ile ve işe göre ayrı
   (`propose_link`, `report_error`; tek "write" aracı değil). Okuma sunucusunun dizin listelemesi değişmez,
   açık kalır. ("Required when the server asks" ile tek sunucuda da olur ama okuma listelemesine OAuth bilgisi
   girer; OpenAI portalının OAuth'ta ısrar ettiği 2026-10'daki sorun yeniden doğabilir.)
3. **Başvurudan önce:** tefsir ve hadis talimatlarındaki "öbür bağdaştırıcıya sor" ifadeleri bilgi kipine
   çevrilir; her yeni sunucuya gizlilik politikasında bölüm; hakem için kurulum belgesi (sitede).
4. **Kullanıcının yapacağı:** portalda (claude.ai/directory/manage) mevcut başvurunun durumuna bakmak.

## Kaynaklar

- [Submit a connector to the directory (Claude)](https://claude.com/docs/connectors/building/submission)
- [Connector pre-submission checklist (Claude)](https://claude.com/docs/connectors/building/review-criteria)
- [Anthropic connectors directory FAQ](https://support.claude.com/en/articles/11596036-anthropic-mcp-directory-faq)
- [App submission guidelines (OpenAI)](https://developers.openai.com/apps-sdk/app-submission-guidelines)
- [Submitting apps (OpenAI)](https://developers.openai.com/apps-sdk/deploy/submission)
