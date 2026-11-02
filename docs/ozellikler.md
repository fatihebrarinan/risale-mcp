# Göz önünde olmayan özellikler

Uygulamada bulunan ama kullanıcının kendiliğinden fark etmeyeceği özellikler. Yeri gelince tanıtım sitesine taşınır.
Yeni özellik eklenince buraya da yazılır. **Sitede** sütunu `site/belgeler.html` ve `site/index.html`'de geçip
geçmediğini söyler; **Yok** olanlar öncelikli adaydır.

Örnek sorular özelliğin nasıl kullanılacağını gösterir: kullanıcı aracı değil, soruyu yazar.

## Kur'ân

| Özellik | Örnek soru | Araç | Sitede |
|---|---|---|---|
| Risale'deki bir bölümün hangi âyetlerle bağ kurduğu | "Bu bölüm hangi âyetlerle ilişkili?" | `read_section` (`linked_verses`) | Kısmen ("Okurken dikkat") |
| Bir âyetle bağ kuran yerler, bağın türü ve kanıt cümlesi | "Âyetü'l-Kürsî'ye Risale'nin neresi işaret ediyor?" | `find_ayah` (`links`) | Kısmen (araç tablosu) |
| Bir âyetin Risale'de kaç kez geçtiği | "Bu âyet eserlerde kaç defa geçiyor?" | `get_ayah`, `find_ayah` | Yok |
| Kaynağın işaretlemediği âyet alıntılarını da bulma | "Bu âyeti geçen bütün yerleri göster" | `find_ayah` (`via: text`) | Yok |
| Eserlerdeki âyetlerin Kur'ân metniyle denetlenmesi; müellifin uyarlaması (iktibas) ve dizgi şüphesi uyarısı | "Buradaki âyet Mushaf'la aynı mı?" | `find_ayah` (`check`) | Yok |
| Âyetin Risale-i Nur'a işaret ettiği yerler (ayrı tür) | "Hangi âyetlerin Risale-i Nur'a işaret ettiği söylenir?" | `find_ayah` (`links`, tür `risale`) | Yok |
| Âyetin harekeli metni ve iki Diyanet meali, birlikte tercüme edilen âyetlerin işareti | "Bakara 255'in meali nedir?" | `get_ayah` | Evet |

## Atıf ve doğruluk

| Özellik | Örnek soru | Araç | Sitede |
|---|---|---|---|
| Her alıntının cevaptan önce metinle denetlenmesi; alıntı başka yerdeyse asıl yerinin gösterilmesi | Kendiliğinden | `cite` | Kısmen |
| Bir temsilin ya da düşüncenin ardışık cümleleri tek atıfla (en çok 8) | Kendiliğinden | `get_passage`, `cite` | Yok |
| Cümlenin ilk kelimelerinden yerini bulma | "'Hiç mümkün müdür ki' ile başlayan cümle nerede?" | `find_sentence` | Evet |
| Âyet ve hadisin türünün dayanağıyla verilmesi; yalnız bağlamdan hadis sayılanların işareti | "Bu hadis mi?" | `read_section`, `get_passage` (`kind_unverified`) | Yok |
| Nâşir mealinin müellifin sözünden ayrılması | Kendiliğinden | `publisher_translation` | Evet |

## Metin ve yapı

| Özellik | Örnek soru | Araç | Sitede |
|---|---|---|---|
| Hâşiyelerin geçtikleri cümleye bağlı okunması | "Bu cümlenin hâşiyesi var mı?" | `get_passage`, `read_section` | Kısmen |
| Mecmuaların ana ciltle eşlenmesi: Asâ-yı Mûsâ'dan okurken ana cildin adresi gelir, aynı cümle iki kez sayılmaz | "Zülfikâr'daki bu parça aslen nerede?" | `read_section` (`canonical`) | Evet |
| Aslı Arapça eserlerin iki dilde aynı bölüm kimliğiyle okunması | "İşaratü'l-İ'caz'ın bu bölümünün Arapçası?" | `read_section`, paralel kimlikler | Kısmen |
| Kızıl İcaz'da Süllem beyitlerinin ve Abdülmecid Nursî şerhinin müelliften ayrılması | "Bu söz Bediüzzaman'ın mı?" | `commentary_by`, `quote` paragrafı | Kısmen |
| 16 Osmanlıca ciltte kelime araması | "Sözler'in Osmanlıcasında bu kelimeyi ara" | `search` | Evet |
| Her risalenin yazıldığı tarih, yer ve dil, kaynağıyla; tahminler işaretli | "İkinci Şuâ ne zaman, nerede yazıldı?" | `list_works`, `get_outline`, `read_section` (`written`) | Yok |
| Konunun yoğunlaştığı bölümler | "Bu konu en çok nerede işlenir?" | `semantic_search` (`sections`) | Yok |

## Hazır komutlar

İstemcide komut olarak görünür (Claude Code'da `/mcp__risale__topic_survey`). Sitede geçmiyor.

| Komut | İşi |
|---|---|
| `topic_survey` | Bir konunun eserlerde geçtiği yerler |
| `text_and_commentary` | "Metin ne diyor" ile "yorum" ayrı başlıklarda |
| `discuss` | Bir konuda müzakere |
| `self_test` | Bölümden soru sorar, cevabı metinle denetler |
| `lesson_plan` | Atıflı ders planı |

Bağlam olarak eklenebilen kaynaklar: `risale://works`, `risale://outline/{work}`, `risale://text/{+section}`.

## Planlananlar

Eklenince yukarıdaki tablolara geçer. Ayrıntı `CLAUDE.md` › Aşamalar.

| Özellik | Aşama |
|---|---|
| Risale'nin kendi göndermelerini izleme ("Yirmi Beşinci Söz'de beyan edildiği gibi") | 13 |
| Eserlerin telif tarihleri | 13.2 |
| Hadislerin bir derlemle eşlenmesi: tam alıntı, mânen, bulunamadı | 14 |
| Konu fihristi | 15 |
| Kızıl İcaz'ın Türkçesi | 17 |
| Gemini desteği | 18 |
| Bir alıntının yanında Osmanlıcasını gösterme | 19 |
| Kaynakçadan metne doğrudan bağlantı | 20 |
