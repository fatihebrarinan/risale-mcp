# OpenAI eklenti dizini başvurusu

Portal: https://platform.openai.com/plugins › **Upload new or existing plugin**. Belgeler:
https://developers.openai.com/plugins/deploy/submission, kurallar: https://developers.openai.com/plugins/plugin-guidelines.
**Durum (2026-10-29): gönderildi, karar bekleniyor.** Kimlik doğrulama yok (OAuth askıda), hakem hesabı yok.
Yayıncı kimliği: kişisel doğrulama (2026-10-29, onaylandı; kurum doğrulaması "Nur Hadimleri" için yapılamadı).

## Paket

`scripts/chatgpt-paket.sh` → `data/interim/chatgpt/risale-i-nur.zip` (git'e eklenmez). Kaynağı `packaging/chatgpt/`:

- `plugin.json` (Agent Plugins 1.0.0 şeması): ad `risale-i-nur`, görünen ad "Risale-i Nur", kısa açıklama
  "Cite the Risale-i Nur exactly" (≤30), uzun açıklama (Claude dizinindekinin ChatGPT'ye uyarlanmışı; kullanıcılar ve
  sınırlar eklendi), Türkçe çeviri (`tr-TR`), 3 hazır istem, kategori `Education & Research` (portaldaki listeden
  doğrulanacak), dört adres (site, destek, gizlilik, kullanım şartları), 5 olumlu ve 3 olumsuz test senaryosu, sürüm notu.
- `mcp.json`: yalnızca `https://mcp.risalemcp.com/mcp`. Kimlik doğrulama türü pakette değil, portalda seçilir.
- `assets/logo.png`: `src/risale_mcp/static/icon.png` (256×256).

Test senaryoları pakette olduğu için portalda salt okunur görünür; değiştirmek için `packaging/chatgpt/plugin.json`
düzenlenir, paket yeniden üretilip yüklenir.

## Adımlar

1. **Kullanım şartları** (`termsOfServiceURL` zorunlu): `site/kullanim-sartlari.html`, `site/en/terms.html`
   (2026-10-29'da yayında; avukat uygun buldu).
2. **Paketi yükle.** Doğrulanmış kimliği seç. Bulgular çıkarsa düzelt, yeniden yükle.
3. **MCP kurulumu.**
   - Kimlik doğrulama: **No authentication**. Sunucu OAuth bilgisi yayımladığı sürece portal OAuth'ta ısrar etti
     (eklentiyi silip yeniden yüklemek de değiştirmedi); bu yüzden genel sunucu 2026-10-29'dan beri açık kipte
     (`--open`): OAuth uç noktaları ve `sign_in` yok. Hakem hesabı gerekmez.
   - Alan adı doğrulaması: portalın verdiği jeton `scripts/sunucu.sh openai-challenge <jeton>` ile
     `https://mcp.risalemcp.com/.well-known/openai-apps-challenge` adresine yazılır (Caddy düz metin verir).
   - Araç taraması: 10 araç, hepsinde `readOnlyHint: true`, `destructiveHint: false`, `openWorldHint: false`.
4. **İnceleme ayrıntıları.**
   - Test senaryolarının her biri başvurudan önce ChatGPT'de çalıştırılır. Araç zinciri gizli hata ayıklama adresiyle
     eklenmiş eklentiden izlenir (`scripts/sunucu.sh auth debug-url --new`, kayıt
     `scripts/sunucu.sh auth usage --user '(debug)' --params`).
   - **Tanıtım videosu** (zorunlu): beş olumlu senaryonun ChatGPT'de çalışması, hakemlerin açabileceği bir bağlantıyla
     (`review.demo_recording_url` pakete eklenir ya da portala yazılır).
   - Masaüstü ve mobilde deneme.
5. **Submit for review**, onaylar. Kabulden sonra yayına alma zamanı bizde. Sunucu her gün taranır; araç
   değişiklikleri yeni başvuru istemez, açıklama ve logo değişiklikleri ister.

## Açık sorular

- Paketteki `developerName` ve `author.name` "Nur Hadimleri" (kullanıcının kararı); dizin doğrulanmış kişisel kimliğin
  adını gösterir. Portal uyuşmazlık bulgusu verirse kullanıcının adı yazılır (sitedeki "Sorumlu" kısmı da).
- Kategori listesi portalda görülünce kesinleşir.
- ChatGPT'nin `clientInfo.name`'i "openai-mcp" (2026-10-29'da ayrıntılı kayıttan doğrulandı).
