# S4: Dizin başvuruları, yapılacaklar (2026-11-13)

`PLANLAR.md` S4'ün uygulama belgesi: sekiz başvurunun her biri için sizin yapacaklarınız, portala yapıştırılacak
metinler (İngilizce; hakemler İngilizce okur) ve göndermeden önceki denetimler. Eski belgeler ayrıntı ve geçmiştir:
`docs/dizin-basvurusu.md` (Claude, Risale), `docs/chatgpt-dizin-basvurusu.md` (OpenAI, Risale),
`docs/dizin-politikalari.md` (iki dizinin kuralları).

| # | Dizin | Eklenti | Durum | Bu belgede |
|---|---|---|---|---|
| 1 | Claude | Risale MCP (eski başvuruda Risale-i Nur) | 2026-10-29'dan beri "In review"; geri çekilip yeniden gönderilecek (2026-11-16) | §2a: sıra ve bütün alanlar |
| 2 | Claude | Hadis | otomatik incelemeyle "Community" olarak onaylandı (2026-11-16), yayımlanması bizde | §2b |
| 3 | Claude | Tefsir | gönderilmedi | §2c |
| 4 | OpenAI | Risale | reddedildi (kimlik) | §5–§6: kişisel kimliğe geçiş, düzeltilmiş paket, yeniden başvuru |
| 5 | OpenAI | Hadis | gönderilmedi | §7 |
| 6 | OpenAI | Tefsir | gönderilmedi | §7 |
| 7 | Claude | Klasik Eserler | gönderilmedi (eklenti 2026-11-13'te yayında) | §2d |
| 8 | OpenAI | Klasik Eserler | gönderilmedi | §7 |

Önerilen sıra: §1 (ortak hazırlık; sitedeki yayıncı adı OpenAI için şart) → §2 (Claude formu) → §2a → §2b, §2c, §2d
(Claude, aynı gün olabilir) → §5 ve §6 (OpenAI Risale) → kabul ya da ilk geri dönüt gelince §7 (OpenAI'de
aynı ret sebebi dört kez gelmesin diye önce bir başvurunun sonucu görülür). OpenAI'nin alan adı doğrulaması tek
dosyadır (§1.5): başvurular aynı anda doğrulanamaz.

## 1. Ortak hazırlık (bir kez)

### 1.1 Yayıncı adı: "Risale MCP" (karar 2026-11-16)

Kullanıcının kararı (2026-11-16): adı projede hiçbir yerde geçmez. Sitede ve Claude başvurularında yayıncı
**"Risale MCP"**dir; "Nur Hadimleri" siteden kalktı (gizlilik, şartlar, belgeler, alt bilgi; `scripts/site-uret.py`).
Şartlar sayfası Klasik Eserler'i de anıyor. Claude kimlik doğrulaması istemez: başvuru kişisel organizasyonla,
"Company name" `Risale MCP`.

OpenAI (karar bekliyor): belge "The directory name is set automatically from your selected verified developer
identity" ve "Public URLs must … identify the same publisher as the submission" diyor (2026-11-16'da bakıldı).
Kişisel doğrulamayla yayımlanırsa dizinde doğrulanmış kişisel ad görünür, sitede de aynı ad gerekir. Yollar:
(a) ad ChatGPT dizininde ve yalnız gizlilik ve şartların "Sorumlu" satırında, (b) tüzel kişilik ve işletme
doğrulaması, (c) OpenAI dizinine şimdilik başvurmamak (elle ekleme sürer). `packaging/chatgpt/` bu karara kadar
"Nur Hadimleri" adını taşır.

### 1.1a Hakeme ek not

Claude formunun "Ek notlar" alanı: yayıncının kayıtlı şirket olmadığı, kaynaklar ve test istemleri (formda hakem
talimatı alanı yok). Metinler §2'de (ortak paragraflar) ve §2a–§2d'de.

### 1.2 Eski bilgilerin düzeltilmesi (her listelemede)

| Eski metin | Doğrusu (2026-11-13, `scripts/site-uret.py` sayıları) |
|---|---|
| "About 126,000 sentences across 44 works" | "About 131,000 sentences across 53 works" (Osmanlıca ciltler hariç; 16 Osmanlıca cilt ayrıca) |
| "two Turkish translations by Diyanet" (Claude listelemesi) | "the Türkiye Diyanet Foundation's Turkish translation" (Diyanet İşleri meali 2026-11-12'de çıkarıldı, B6) |
| "10 tools" | Risale 12, Hadis 9, Tefsir 11, Klasik Eserler 10 araç; hepsi `readOnlyHint: true`, `destructiveHint: false`, `openWorldHint: false`, başlıklı (`server.py` `read_only`; 23 kayıt denetlendi) |

### 1.3 Gizli hata ayıklama adresleriyle deneme

Her başvurudan önce, o eklentinin test istemleri claude.ai'de ve ChatGPT'de bir kez çalıştırılır; araç zinciri gizli
adresle izlenir:

```
scripts/sunucu.sh auth debug-url --new                      # Risale: https://mcp.risalemcp.com/mcp/<anahtar>
scripts/sunucu.sh auth --server hadis debug-url --new       # Hadis: https://hadis.risalemcp.com/mcp/<anahtar>
scripts/tefsir-sunucu.sh auth debug-url --new               # Tefsir: https://tefsir.risalemcp.com/mcp/<anahtar> (kayıt tefsir makinesinde)
PROFIL=klasik scripts/tefsir-sunucu.sh auth debug-url --new # Klasik: https://klasik.risalemcp.com/mcp/<anahtar> (tefsir makinesinde)
scripts/sunucu.sh auth usage --user '(debug)' --params      # kayıt (Risale ve Hadis; --only hadis süzer)
```

Denedikten sonra adresleri kapatın (`--revoke`).

### 1.4 Simgeler (yapıldı, 2026-11-16)

Aynı çizim, zemin rengi farklı (kullanıcı onayladı): Risale yeşil `src/risale_mcp/static/icon.png`, Hadis lacivert
`icon-hadis.png`, Tefsir mor `icon-tefsir.png`, Klasik kahverengi `icon-klasik.png` (256×256; SVG'leri yanında).
Portalda her başvuruya kendi PNG'si yüklenir: dizinde ayrı simgenin tek yolu budur. Claude'un kendi arayüzü simgeyi
`google.com/s2/favicons?domain=risalemcp.com` ile kök alan adından alır, dört eklenti orada yeşil görünür (2026-11-16). Sunucular da kendi simgesini MCP `icons` ile duyurur
(`https://mcp.risalemcp.com/icon-<ad>.png`, kök sunucu verir) ve başlıkları liste adlarıyla aynıdır: "Risale-i Nur
Library", "Hadith Library", "Tafsir Library", "Classical Islamic Library" (2026-11-22; önceden "Risale MCP …").

### 1.5 OpenAI alan adı doğrulaması

Jeton `https://mcp.risalemcp.com/.well-known/openai-apps-challenge`'da tek dosyadır
(`scripts/sunucu.sh openai-challenge <jeton>`). Üç başvuru aynı alan adını kullandığı için her başvuru kendi
jetonunu ister. Biri doğrulanınca sonrakinin jetonu yazılır. Portal sonradan yeniden doğrulama isterse o başvurunun
jetonu yeniden yazılır.

### 1.6 Talimatların dizin kurallarına uygunluğu

Claude'un ölçütü, aracın ya da talimatın "kullanıcının istemediği bir aracı çağırmaya yönlendirmesini" reddeder
(`docs/dizin-politikalari.md`). Hadis ve tefsir talimatları Risale'yi yalnız bilgi kipinde anıyor: "Risale'nin ne
dediğini ancak bu sohbette Risale eklentisiyle okuduysan söyle, okumadıysan bakmadığını söyle". Bu bir çağırma emri
değil, bir sınır. Düşük risk; hakem sorarsa cevabı budur (B2 bunu ayrıca izler).

## 2. Claude portalı: formun alanları (2026-11-16, Risale formundan)

Portal: https://claude.ai/directory/manage. Form bölümleri ekrandaki sırayla; değerler eklentiye göre §2a–§2d'de.
Hakem talimatı için ayrı alan yok: test istemleri "Ek notlar"a girer. Kullanım alanı en fazla üçtür.

| Bölüm › alan | Ne girilir |
|---|---|
| Listeleme › Tek satırlık açıklama (≤200), Açıklama (≤2000) | eklentinin metni |
| Kategoriler (≤5) | Education, Nonprofit, Other (Risale'de seçilenler) |
| Simge | Risale boş (alan adının simgesi zaten yeşil); öbürleri `https://<ad>.risalemcp.com/icon.png` (§1.4) |
| Bağlantılar › Dokümantasyon, Destek, Gizlilik | `https://risalemcp.com/en/<sayfa>.html`, `destek@risalemcp.com`, `https://risalemcp.com/en/privacy.html` |
| Dizin sunumu › Şunlarla çalışır | Claude (web & mobile), Claude API, Claude Code, Claude Desktop |
| Yazar adı, Yazar URL'si | `Risale MCP`, `https://risalemcp.com/` |
| Sunucu etiketi | kısa ad (`risale`, `hadis`, `tefsir`, `klasik`); API'de ve Claude Code'da sunucunun adı olur |
| İzin özeti | eklentinin satırı (aşağıda); Risale'de boş kalmış, doldurulur |
| Hassas veri türleri | boş ("Kayıt yok") |
| MCP uygulaması var | işaretlenmez |
| Marka ve medya (logo, desen, video, karusel) | boş |
| Entegrasyon parçacıkları | Claude API metni, Claude Code metni, Claude Code dış bağlantısı (aşağıda) |
| Araçlar ve istemler | sihirbaz sunucudan okur; düzenlenmez |
| Bağlantı › Sunucu URL'si | eklentinin herkese açık adresi; "Kullanıcılar farklı URL'lere bağlanır" işaretlenmez |
| Kimlik doğrulama | Yok |
| Kullanım alanları (3 × kullanım alanı + örnek istem) | eklentinin üç satırı; yalnız hakemler görür |
| Ön koşullar | ortak metin (aşağıda) |
| Okuma/yazma | Salt okunur |
| API sahipliği; Kişisel sağlık verisi; Sponsorlu içerik | API bize ait; Hayır; Hayır |
| Test › Bizzat test edilmiş | denemeden sonra işaretlenir (§1.3 ve aşağıdaki not) |
| Politika beyanları | yedisi de işaretlenir |
| Ek notlar | eklentinin notu: yayıncı, kaynaklar, test istemleri |
| Şirket adı, web sitesi | `Risale MCP`, `https://risalemcp.com/` |
| Ad | `Risale-i Nur Library`, `Hadith Library`, `Tafsir Library`, `Classical Islamic Library` (kullanıcının kararı, 2026-11-22: İngilizce, "Risale MCP" öneki yok; yayıncı adı "Risale MCP" kalır. Önceden `Risale MCP Risale-i Nur`, `Risale MCP Hadis`, `Risale MCP Tefsir`, `Risale MCP Klasik`) |

**Araç taraması için bağdaştırıcı hesapta olmalı.** Portal araçları sizin hesabınızdaki bağdaştırıcıdan okur ve
"bu listelemenin gönderildiği bağdaştırıcı hesabınızda yok" diye uyarır. Gizli adres yetmez: listelemedeki adresin
aynısı (ör. `https://hadis.risalemcp.com/mcp`) Ayarlar › Bağdaştırıcılar'da özel bağdaştırıcı olarak ekli olmalı.
Gizli adresli olanı denemelerin kaydı için ayrıca tutabilirsiniz.

**Ortak metinler:**

- Ön koşullar:
  > Nothing. There are no accounts and no sign-in: every tool works for everyone. To protect the service, search by
  > meaning has a shared daily limit and requests a shared per-minute limit.
- Ek notların ilk paragrafı (yayıncı; her eklentide aynı):
  > Publisher: "Risale MCP" is the name of a volunteer, non-commercial project, not a registered company. It is run
  > by an individual (the holder of this account) and is named the same way on the website, the privacy policy and
  > the terms (risalemcp.com). The project runs four connectors under this name, submitted separately: Risale-i Nur
  > Library (mcp.risalemcp.com/mcp), Hadith Library (hadis.risalemcp.com/mcp), Tafsir Library
  > (tefsir.risalemcp.com/mcp) and Classical Islamic Library (klasik.risalemcp.com/mcp).
- Ek notların son paragrafı (her eklentide aynı):
  > All tools are read-only, there are no accounts, and no conversation content or tool inputs are stored (only the
  > tool name, time, duration and error type, for 90 days).

### 2a. Risale MCP (eski başvuru Risale-i Nur; geri çekilip yeniden gönderilecek, 2026-11-16)

**Karar (kullanıcı, 2026-11-16):** eski başvuru silinir, bugünkü formla yeniden gönderilir. Sebep: Hadis aynı gün
otomatik taramayla "Community" olarak onaylandı; Risale ise 2026-10-29'dan beri bir kişinin kuyruğunda ("In review").
O başvuru OAuth'lu (`sign_in`, hakem hesabı `admin`) gönderilmiş, sunucu aynı akşam açık kipe geçmişti; formdaki
kimlik doğrulama ve test hesabı bilgisi sunucuyla uyuşmuyor olabilir. Yeni başvuru Hadis'le aynı biçimde: OAuth
yok, test hesabı yok, bütün alanlar dolu. Bedeli: kuyruktaki yer gider; otomatik yoldan geçeceğinin garantisi yok
(Anthropic bazı başvuruları her durumda bir kişiye verir).

**Ad `Risale-i Nur Library`** (kullanıcının kararı, 2026-11-22; önceden `Risale MCP`, 2026-11-16, sonra `Risale
MCP Risale-i Nur`): "Library" eki adı bir marka iddiası değil bir tanım yapar; "Risale-i Nur" eserin adıdır, ek
notta bu söylenir. Tek satır artık "Risale-i Nur:" ile başlamaz (ad onu taşıyor). **Portalda değişecekler
(2026-11-22):** ad, tek satır, açıklamanın ilk kelimeleri, ek notların ortak ilk paragrafı ve "It is now named…"
cümlesi; Hadis, Tefsir ve Klasik'te ad, açıklamanın ilk kelimeleri ve ortak ilk paragraf.

**Sıra:**

1. Ayarlar › Bağdaştırıcılar'da `https://mcp.risalemcp.com/mcp` adresli bağdaştırıcı ekli olsun (portal araçları
   oradan okur). §1.3'teki gizli adresle aşağıdaki test istemlerini bir kez deneyin.
2. Eski başvuruyu portalda açın, menüsünden silin ya da geri çekin (**Withdraw/Delete**). Yeni başvuruyu ondan
   **sonra** gönderin: aynı adresli iki başvuru aynı anda durmasın.
3. Portal › **Submit new** › **MCP connector**, alanlar aşağıda ve §2'deki tabloda.
4. **Slug** `risale-mcp` (yayımlanınca değişmez; eski başvurunun `risale-i-nur`'u ile çakışmaz).
5. Gönderdikten sonra durum "Approved" olursa yayımlamak bizde (**Publish**); onaydan sonra yapılan her düzenleme
   listelemeyi yeniden incelemeye gönderir, düzenlemeyi yayımlamadan önce yapın. "In review" olursa beklenir.

**Alanlar:** sunucu URL'si `https://mcp.risalemcp.com/mcp`, ad `Risale-i Nur Library` (2026-11-22; önceden `Risale MCP Risale-i Nur`, kullanıcı 2026-11-16: yayıncı adıyla aynı olmasın), etiket `risale`, simge
`src/risale_mcp/static/icon.png` (yeşil; boş bırakılırsa alan adının simgesi), dokümantasyon
`https://risalemcp.com/en/risale.html` (öbürleri gibi eklentinin kendi sayfası; eski başvuruda `docs.html`),
kimlik doğrulama **Yok**, test hesabı yok.

- **Tek satır:**
  > Read and cite the complete works of Bediüzzaman Said Nursî, the Risale-i Nur, sentence by sentence, with the
  > Qur'an's text alongside.
- **Açıklama:**
  > Risale-i Nur Library gives Claude the complete works of Bediüzzaman Said Nursî: the Risale-i Nur Collection
  > (Sözler, Mektubat, Lem'alar, Şualar, the Lâhikas, Tarihçe-i Hayat), the works of his early period, the
  > compilations and the Hizbs, in Turkish and, for the works he wrote in Arabic, in Arabic too. About 131,000
  > sentences across 53 works, besides 16 volumes in Ottoman script, together with the Qur'an's vowelled Arabic
  > text and the Türkiye Diyanet Foundation's Turkish translation.
  >
  > Every sentence has a stable address, so Claude can ground what it says in the text itself:
  >
  > - Search by the text's own words, or by meaning in today's language (a question about "despair" finds
  >   passages that speak of "ye's").
  > - Read any section in book order, with the author's footnotes (hâşiye) and the sources of the verses and
  >   hadiths he quotes.
  > - Quote the text exactly and end the answer with a list of sources giving work › section › the sentence's
  >   opening words. Quotations are checked against the cited sentences before the answer is sent.
  > - Find where a Qur'anic verse or a hadith is quoted in the works, read the verse, and see the evidence for the
  >   hadith in the classical collections.
  >
  > The connector keeps layers apart that are easy to confuse: the publishers' translations of verses are not the
  > author's words, the Turkish of his Arabic works is a translation, and a commentary by his brother is marked as
  > his. When something is not in the works, Claude is told to say so instead of filling the gap.
  >
  > All tools are read-only and work without an account. The texts come, unchanged and with permission, from
  > e-Risale, risaleoku.com, nurpedia.org and the Keşif Yolculukları programme; the Qur'an's text from the Tanzil
  > Project. A volunteer, non-commercial project.
- **İzin özeti:**
  > Reads the works of Bediüzzaman Said Nursî and the Qur'an from this project's own library. It does not access
  > your accounts, files or personal data.
- **Entegrasyon:** Claude Code metni `claude mcp add --transport http risale https://mcp.risalemcp.com/mcp`; dış
  bağlantı `https://risalemcp.com/en/claude.html`; Claude API metni:
  > Add the connector to a Messages API request as an MCP server: {"type": "url", "url":
  > "https://mcp.risalemcp.com/mcp", "name": "risale"}. No authorization token is needed.
- **Kullanım alanları:**

  | Kullanım alanı | Örnek istem |
  |---|---|
  | Answer questions about the Risale-i Nur with exact quotations and sources | Why is the time of the Last Day kept hidden, according to the Risale-i Nur? Quote the text and give the sources. |
  | Survey where a topic is treated across the works | Where does Bediüzzaman write about patience in illness? List the main passages by work. |
  | Find where a Qur'anic verse is quoted in the works and read the verse | Where is Âyetü'l-Kürsî (Bakara 2:255) quoted in the Risale-i Nur? Show the verse with a translation. |

- **Ek notlar:** ortak ilk paragraf, sonra
  > The texts are served with the permission of their sources (e-Risale, risaleoku.com, nurpedia.org and the Keşif
  > Yolculukları programme), which are named on the website and in every answer's list of sources; the Qur'an's
  > text comes from the Tanzil Project. This replaces our earlier submission of the same connector (named
  > "Risale-i Nur", sent on 29 October with optional OAuth), which we withdrew. It is now named Risale-i Nur
  > Library, a description of what it holds: "Risale-i Nur" is the name of the works it serves, not a brand we
  > claim. The server has had no accounts and no OAuth since the evening of 29 October.
  >
  > How to test (the texts are in Turkish; questions can be asked in English): "List the works and show the outline
  > of Sözler." · "Why is the time of the Last Day kept hidden, according to the Risale-i Nur? Quote the text and
  > give sources." · "Search the works for 'halk-ı şer şer değil' and explain the passage." · "Find the sentence that
  > begins 'Hiç mümkün müdür ki; ölmüş'." · "Where is Âyetü'l-Kürsî (Bakara 2:255) quoted in the works? Show the
  > verse." · "Where does the Risale-i Nur quote the hadith 'تفكر ساعة خير من عبادة سنة'? What is the evidence for
  > it?" Expected: quotations in block quotes marked [1], [2]… and a "Kaynaklar" list; asking for something not in
  > the works (e.g. "Summarise the Fifteenth Truth of the Tenth Word") gets the answer that it does not exist.

  ve ortak son paragraf.

### 2b. Hadis (yeni başvuru)

Portal › **Submit new** › **MCP connector**. Sunucu URL'si `https://hadis.risalemcp.com/mcp`, ad `Hadith Library` (2026-11-22; önceden `Risale MCP Hadis`),
etiket `hadis`, simge `https://hadis.risalemcp.com/icon.png`, dokümantasyon `https://risalemcp.com/en/hadith.html`.

- **Tek satır:**
  > Read and cite eighteen classical hadith collections in Arabic, report by report, with grades only as the
  > sources give them.
- **Açıklama:**
  > Hadith Library gives Claude eighteen classical hadith collections in their original Arabic: the Six Books
  > (al-Bukhari, Muslim, Abu Dawud, al-Tirmidhi, al-Nasa'i, Ibn Majah) and the Muwatta, Ahmad's Musnad, al-Darimi,
  > al-Tabarani's al-Mu'jam al-Saghir, al-Hakim's al-Mustadrak with al-Dhahabi's notes, Ibn Hibban (al-Ihsan),
  > al-Haythami's Majma' al-Zawa'id, Kanz al-'Ummal, al-Munawi's Fayd al-Qadir, al-'Ajluni's Kashf al-Khafa, Qadi
  > 'Iyad's al-Shifa and al-Bayhaqi's Dala'il al-Nubuwwa: about 169,000 reports, together with the Qur'an's text.
  >
  > The unit of citation is the report, with its book, the edition's number and the printed page:
  >
  > - Search by Arabic words (forms with attached particles match), by a narrator's name in the chain, or by
  >   meaning in any language.
  > - Go from a reference such as "Bukhari, Adhan: 148" or "Musnad 14870" to the report; browse books and chapters.
  > - Read a report with its chain and text, the scholars' notes as a separate layer, and the places in the
  >   Risale-i Nur that quote it.
  > - Quote the Arabic exactly and end the answer with a numbered list of sources, checked against the reports.
  >
  > Claude never rules on a report's soundness: grades are shown only as the sources give them, with the scholar's
  > name; notes by al-Dhahabi, al-Albani and the editors are never attributed to the book's author. Claude's own
  > translations are labelled as AI translations.
  >
  > All tools are read-only and work without an account. The books come from OpenITI (CC BY-NC-SA 4.0), the
  > international numbers and grades of the Six Books and the Muwatta from Hadith API, the Qur'an's text from the
  > Tanzil Project. A volunteer, non-commercial project.
- **İzin özeti:**
  > Reads classical hadith collections and the Qur'an from this project's own library. It does not access your
  > accounts, files or personal data.
- **Entegrasyon:** `claude mcp add --transport http hadis https://hadis.risalemcp.com/mcp`; dış bağlantı
  `https://risalemcp.com/en/hadith.html`; API metni §2a'daki gibi (adres ve `"name": "hadis"`).
- **Kullanım alanları:**

  | Kullanım alanı | Örnek istem |
  |---|---|
  | Find in which books a saying occurs, without a ruling on it | In which books does the saying "اختلاف أمتي رحمة" occur, and what is said about it? With sources, without a ruling. |
  | Go from a reference to the report and read it | Show me Bukhari, Adhan: 148 with its chain and text, and translate it. |
  | Find reports on a topic by meaning | Find reports about visiting the sick, with their sources. |

- **Ek notlar:** ortak ilk paragraf, sonra
  > The books come from OpenITI (KITAB project, CC BY-NC-SA 4.0) and Hadith API (Unlicense), named on the website
  > and in every answer's list of sources; the Qur'an's text from the Tanzil Project. The connector never grades a
  > report itself: it shows grades only as the sources hold them, with the scholar's name.
  >
  > How to test (the books are in Arabic; questions can be asked in English): "List the books and show the outline
  > of Sunan Abi Dawud." · "Show the chapter on the call to prayer (adhan) in Sahih al-Bukhari." · "Find Bukhari,
  > Adhan: 148 and show its chain and text." · "Search for reports with the words 'إنما الأعمال بالنيات'." · "Find
  > reports about kindness to neighbours." · "Show the verse al-Baqara 2:255." Expected: Arabic quoted exactly in
  > block quotes, the assistant's translation labelled as its own, each quotation marked [1], [2]… with a sources
  > list at the end, and no ruling on a report's soundness.

  ve ortak son paragraf.

### 2c. Tefsir (yeni başvuru)

Sunucu URL'si `https://tefsir.risalemcp.com/mcp`, ad `Tafsir Library` (2026-11-22; önceden `Risale MCP Tefsir`), etiket `tefsir`, simge
`https://tefsir.risalemcp.com/icon.png`, dokümantasyon `https://risalemcp.com/en/tafsir.html`. Tefsir sunucusu ayrı
makinededir (CAX21); hakem denemesinde sorun olursa `scripts/tefsir-sunucu.sh status|logs`.

- **Tek satır:**
  > Read and cite thirteen classical works of Qur'anic exegesis in Arabic, verse by verse, from al-Tabari to
  > al-Alusi.
- **Açıklama:**
  > Tafsir Library gives Claude thirteen classical works of Qur'anic exegesis (tafsir) in their original
  > Arabic, in order of their authors' deaths: al-Tabari, al-Maturidi, al-Zamakhshari, Fakhr al-Din al-Razi,
  > al-Qurtubi, al-Baydawi, al-Nasafi, Ibn Kathir, al-Jalalayn, al-Suyuti's al-Durr al-Manthur, Abu al-Su'ud,
  > Isma'il Haqqi Bursawi and al-Alusi: about 552,000 sentences, together with the Qur'an's text.
  >
  > Each work is divided into verse units and every sentence has a stable address:
  >
  > - Ask about a verse and see, work by work, the unit that treats it and the sentences that quote it.
  > - Search by the works' own Arabic words or by meaning in any language.
  > - Read a unit or a passage in context and quote it exactly, with a numbered list of sources checked against
  >   the text.
  >
  > Each work belongs to its author: editors' introductions are a separate layer, and two exegetes treating the same
  > verse is never presented as one following another unless a link is recorded. Claude's own translations are
  > labelled as AI translations, and nothing Claude writes is called tafsir.
  >
  > All tools are read-only and work without an account. The texts come from OpenITI (KITAB project; CC BY-NC-SA
  > 4.0), each in its chosen edition; the Qur'an's text from the Tanzil Project. A volunteer, non-commercial
  > project.
- **İzin özeti:**
  > Reads classical works of Qur'anic exegesis and the Qur'an from this project's own library. It does not access
  > your accounts, files or personal data.
- **Entegrasyon:** `claude mcp add --transport http tefsir https://tefsir.risalemcp.com/mcp`; dış bağlantı
  `https://risalemcp.com/en/tafsir.html`; API metni §2a'daki gibi.
- **Kullanım alanları:**

  | Kullanım alanı | Örnek istem |
  |---|---|
  | Compare what classical exegetes say about a verse | What do al-Zamakhshari and al-Baydawi say about "iyyaka na'budu" (al-Fatiha 1:5)? Quote them with sources. |
  | Survey the exegetes on a verse in order | Go through the exegetes on Ayat al-Kursi (al-Baqara 2:255) in order of their deaths, one key point each. |
  | Find a discussion by meaning across the works | Which exegetes explain why the Qur'an uses parables, and how? |

- **Ek notlar:** ortak ilk paragraf, sonra
  > The texts come from OpenITI (KITAB project, CC BY-NC-SA 4.0), each in its chosen edition, named on the website
  > and in every answer's list of sources; the Qur'an's text from the Tanzil Project.
  >
  > How to test: "List the works and show the outline of al-Baydawi's Anwar al-Tanzil." · "What do the exegetes say
  > about al-Fatiha 1:5? Read al-Zamakhshari's unit and quote him." · "Search the works for 'الحروف المقطعة'." ·
  > "Which exegetes explain the purpose of the Qur'an's parables?" · "Find the sentence that begins 'فإن قلت: لم
  > قضيت لهذه الألفاظ' in al-Kashshaf." · "Show the verse al-Baqara 2:255 and any recorded links between texts on
  > it." Expected: Arabic quoted exactly, the assistant's translation labelled as its own, a numbered sources list;
  > the assistant never calls its own summary "tafsir".

  ve ortak son paragraf.

### 2d. Klasik Eserler (yeni başvuru)

Sunucu URL'si `https://klasik.risalemcp.com/mcp`, ad `Classical Islamic Library` (2026-11-22; önceden `Risale MCP Klasik`), etiket `klasik`, simge
`https://klasik.risalemcp.com/icon.png`, dokümantasyon `https://risalemcp.com/en/classical.html`.

- **Tek satır:**
  > Read and cite classical Arabic works on rhetoric, language and terms, from al-Jurjani's Dala'il al-I'jaz to
  > al-Sayyid al-Sharif's Ta'rifat.
- **Açıklama:**
  > Classical Islamic Library gives Claude classical Arabic works on rhetoric (balagha), language and terms in their original
  > Arabic: 'Abd al-Qahir al-Jurjani's Dala'il al-I'jaz and Asrar al-Balagha, al-Raghib al-Isfahani's al-Mufradat fi
  > Gharib al-Qur'an, al-Sakkaki's Miftah al-'Ulum and al-Sayyid al-Sharif al-Jurjani's al-Ta'rifat: about 15,000
  > sentences, together with the Qur'an's text. These are the masters of rhetoric that Bediüzzaman Said Nursî names
  > in his Isharat al-I'jaz.
  >
  > Every sentence has a stable address in the sections of its edition (the Dala'il in its editor's numbered
  > paragraphs, al-Mufradat by root, al-Ta'rifat by chapter):
  >
  > - Search by the works' own Arabic words and terms, or by meaning in any language.
  > - Read a section or a passage in context and quote it exactly, with a numbered list of sources checked against
  >   the text.
  > - Find where a Qur'anic verse is quoted, for example in al-Mufradat's explanation of a word.
  >
  > Each work belongs to its author: the editor's introduction is a separate layer, and a link between these works
  > and the Isharat is never presented as recorded unless Claude has read both. Claude's own translations are
  > labelled as AI translations.
  >
  > All tools are read-only and work without an account. The texts come from OpenITI (KITAB project; CC BY-NC-SA
  > 4.0), each in its chosen edition; the Qur'an's text from the Tanzil Project. A volunteer, non-commercial project.
- **İzin özeti:**
  > Reads classical Arabic works on rhetoric, language and terms, and the Qur'an, from this project's own library.
  > It does not access your accounts, files or personal data.
- **Entegrasyon:** `claude mcp add --transport http klasik https://klasik.risalemcp.com/mcp`; dış bağlantı
  `https://risalemcp.com/en/classical.html`; API metni §2a'daki gibi.
- **Kullanım alanları** (ilk ikisi 2026-11-13'te eklentide denendi):

  | Kullanım alanı | Örnek istem |
  |---|---|
  | Follow an argument in a classical work of rhetoric | How does al-Jurjani argue in the Dala'il al-I'jaz that inimitability lies in the arrangement (nazm)? With sources. |
  | Look up the meaning of a Qur'anic word | How does al-Raghib explain the word "nur" in al-Mufradat? With sources. |
  | Find the definition of a term | What is the definition of "الاستعارة" in al-Ta'rifat, and how does al-Sakkaki treat it in the Miftah? |

- **Ek notlar:** ortak ilk paragraf, sonra
  > The texts come from OpenITI (KITAB project, CC BY-NC-SA 4.0), each in its chosen edition, named on the website
  > and in every answer's list of sources; the Qur'an's text from the Tanzil Project. The Dala'il al-I'jaz keeps
  > its editor's footnote markers in the text as the source has them (the footnotes themselves are not in the
  > source).
  >
  > How to test: "List the works and show the outline of the Dala'il al-I'jaz." · "How does al-Jurjani argue that
  > inimitability lies in the arrangement? Quote him." · "Search the works for 'الاستعارة'." · "Find the sentence
  > that begins 'الابتداء: هو أول جزء' in al-Ta'rifat." · "Where is al-Baqara 2:255 quoted in these works? Show the
  > verse." Expected: Arabic quoted exactly, the assistant's translation labelled as its own, a numbered sources
  > list; the editor's introduction is never attributed to the author.

  ve ortak son paragraf.

## 5. OpenAI: kurum başvurusundan kişisel başvuruya

Ret sebebi (2026-11-12) içerik değil kimlikti: "Nur Hadimleri" adıyla yayımlamak için kurum (işletme) doğrulaması
gerekir, sizde kişisel doğrulama var. Kararınız: kişisel kimlikle yayımlamak.

1. https://platform.openai.com › **Organization settings › Verifications**: "Verified - Individual" olduğunu ve
   doğrulamadaki adın yazılışını görün (§1.1'de bu ad kullanılır).
2. Organizasyonun görünen adı "Nur Hadimleri" kalabilir (yalnız hesabınızın içinde görünür); dizinde görünen ad
   yayımlarken seçilen doğrulanmış kimlikten gelir. Portal "publish as" ya da benzeri bir seçim gösterirse
   **individual** kimliğinizi seçin. Ret iletisi bir kurum adı bekliyorsa tekrar gelebilir; o zaman organizasyonun
   adını da kendi adınıza çevirin.
3. Önce §1.1'i yayına alın (site ve gizlilik politikası yeni adı göstermeden gönderilirse "public URLs must identify
   the same publisher" ret sebebi olur).
4. Reddedilen başvuruyu portalda açın: düzenlenip yeniden gönderilebiliyorsa onu kullanın; değilse §6'daki paketle
   yeni başvuru. İsterseniz ret e-postasını yanıtlayarak düzeltmeyi kısaca bildirin:
   > Thank you for the review. The app is now published under my verified individual identity, [adınız], and the
   > website, privacy policy and terms name the same publisher. The app's name is now "Risale MCP" (our domain,
   > risalemcp.com); "Risale-i Nur" is only the name of the works it serves.

## 6. OpenAI: Risale (düzeltilmiş paket, yeniden başvuru)

**Yapıldı (2026-11-22):** doğrulanmış ad "Fatih Ebrar İnan" (Verified - Individual, "solo developer"). Gizlilik ve
şartlar sayfalarının yayıncı satırı bu ad (yayında); paket aşağıdaki tabloya göre güncellendi, `mcp.json` anahtarı
`risale-i-nur` (iç ad, portal değiştirtmiyor), zip `data/interim/chatgpt/risale-mcp.zip`. Kalan sizde: organizasyonun görünen adı ("Nur Hadimleri")
da aynı ada çevrilsin (ret iletisi markanın doğrulanmış kişiye ait olduğunu soruyor; iki ayrı ad kalmasın), sonra
§5 adım 4 ve aşağıdaki adımlar.

Değişecekler (`packaging/chatgpt/plugin.json`; S4.2 kararı: uygulama adı "Risale MCP"):

| Alan | Bugün | Yeni |
|---|---|---|
| `name` | `risale-i-nur` | `risale-i-nur` (kalır: portal mevcut başvurunun iç adını değiştirmeye izin vermiyor, 2026-11-22; dizinde görünmez) |
| `interface.displayName` | Risale-i Nur | Risale-i Nur Library (kullanıcının kararı, 2026-11-22, dört eklentinin yeni adlarıyla; arada "Risale Library" denendi. Adda "MCP" olamaz: portalın otomatik denetimi "Remove “MCP” from the plugin name" dedi; yönerge §1.3 adın sonuna "MCP" eklenmesini yasaklıyor. Yalnız OpenAI'de; Claude ve site "Risale MCP") |
| `interface.developerName`, `author.name` | Nur Hadimleri | doğrulanmış adınız (§1.1) |
| `interface.shortDescription` (≤30) | Cite the Risale-i Nur exactly | Cite the Risale-i Nur exactly (kalır) |
| açıklamalar | "126,000 sentences across 44 works", "by Nur Hadimleri" | "131,000 sentences across 53 works"; son cümle "A volunteer, non-commercial project." |
| `tr-TR` açıklama | aynı eski sayılar ve "Nur Hadimleri'nin…" | "53 eserde yaklaşık 131 bin cümle"; son cümle "Gönüllü ve ticari olmayan bir projedir." |
| `mcp.json` sunucu anahtarı | `risale-i-nur` | `risale-i-nur` (kalır, adres aynı) |
| `publication.release_notes` | First public release… | Aynı; başına "Resubmitted under the publisher's verified individual identity." eklenebilir |

Adımlar:
1. Paketi ben güncellerim (adınız gelince), `scripts/chatgpt-paket.sh` → `data/interim/chatgpt/risale-i-nur.zip`
   (dosya adını da `risale-mcp.zip` yaparım).
2. Portal: https://platform.openai.com/plugins › yükle › doğrulanmış kişisel kimliği seçin.
3. MCP: **No authentication**; alan adı jetonu (§1.5); araç taraması 12 araç, hepsi salt okunur.
4. Test senaryoları pakette (5 olumlu, 3 olumsuz). Her birini ChatGPT'de (Developer Mode, gizli adresle, §1.3)
   çalıştırın.
5. **Tanıtım videosu** (zorunlu): beş olumlu senaryonun ChatGPT'de çalışması; hakemlerin açabileceği bir bağlantı
   (liste dışı YouTube ya da paylaşılan Drive). Masaüstü ve mobilde birer deneme.
6. **Submit for review.**

**Additional Submission Context** (hakeme özel not; 2026-11-22'de Risale'nin yeniden başvurusunda kullanıldı). Öbür üç
başvuruda iskelet aynı: ilk madde (yayıncı) ve son paragraf aynen kalır, "Name" maddesi o eklentinin adına, "Content"
maddesi o sunucunun kaynaklarına (OpenITI CC BY-NC-SA 4.0, Hadith API, Sanadset…) göre yazılır; yeniden başvuru
değilse ilk cümle ve "previous version" atılır.

> This is a resubmission. The previous version was rejected because we could not show that the brand belongs to the
> verified developer. What changed:
>
> - Publisher: the app is now published under my verified individual identity, Fatih Ebrar İnan. The website's
>   privacy policy and terms name the same person as publisher and operator (risalemcp.com/en/privacy.html,
>   risalemcp.com/en/terms.html). The earlier name "Nur Hadimleri" was not a registered organization and has been
>   removed everywhere.
> - Name: the app is now "Risale-i Nur Library", a description of what it holds. "Risale-i Nur" is the name of
>   the works the app serves (the writings of Bediüzzaman Said Nursî, 1878–1960), not a brand we claim. The project's own name is "Risale MCP", after its
>   domain risalemcp.com, which I own and verify with the domain token. "MCP" is left out of the app name because
>   the guidelines require it.
> - Content: the texts are served unchanged, with written permission from their sources (e-Risale, risaleoku.com and
>   others), on condition that the source is named. The answers' bibliography names it. The Qur'an text and
>   translation come from Tanzil (tanzil.net), used as its terms allow.
>
> It is a volunteer, non-commercial project. All tools are read-only and work without an account or sign-in. No
> conversation content or tool inputs are stored; only the tool name, time, duration and error type are kept, for 90
> days.

## 7. OpenAI: Hadis, Tefsir ve Klasik Eserler

**Hazır (2026-11-22):** `packaging/chatgpt-hadis/`, `-tefsir/`, `-klasik/` (bir kez üretildi, artık asıl kaynak
bunlar); zip'ler `scripts/chatgpt-paket.sh hadis tefsir klasik` → `data/interim/chatgpt/hadith-library.zip`,
`tafsir-library.zip`, `classical-islamic-library.zip`. İç adlarda "mcp" yok (Risale'de görünen adın "MCP"si reddedildi).
Test senaryolarının iddiaları 2026-11-22'de canlı sunucularda denendi; Hadis'in "Bukhari, Adhan: 148" senaryosu künye
dizininin sunucuya gitmesini bekler (`2a33a3b`, `HADIS_EXPECT=find_by_citation scripts/deploy.sh --code --hadis`).
Alan adı jetonu her alt alan adında ayrı: `scripts/sunucu.sh openai-challenge <jeton> hadis|tefsir|klasik`.

| Alan | Hadis | Tefsir | Klasik Eserler |
|---|---|---|---|
| `name` | `hadith-library` | `tafsir-library` | `classical-islamic-library` |
| `displayName` | Hadith Library | Tafsir Library | Classical Islamic Library (kullanıcının kararı, 2026-11-22) |
| `shortDescription` (≤30) | Cite hadith collections | Cite classical tafsir works | Cite classical Arabic works |
| sunucu | `https://hadis.risalemcp.com/mcp` | `https://tefsir.risalemcp.com/mcp` | `https://klasik.risalemcp.com/mcp` |
| açıklama | §2b'deki açıklama ("Claude" yerine "ChatGPT") | §2c'deki açıklama | §2d'deki açıklama |
| `websiteURL` | `https://risalemcp.com/en/hadith.html` | `https://risalemcp.com/en/tafsir.html` | `https://risalemcp.com/en/classical.html` |
| `defaultPrompt` | §2b'nin üç kullanım istemi | §2c'nin üç kullanım istemi | §2d'nin üç kullanım istemi |
| kategori, gizlilik, şartlar, destek, yayıncı | Risale ile aynı | Risale ile aynı | Risale ile aynı |

Test senaryoları (pakete):
- **Hadis olumlu:** (1) "اختلاف أمتي رحمة" hangi kitaplarda (search_hadith, get_hadith, cite; beklenen: Keşfü'l-Hafâ
  gibi kitapların `book_note`'u, hüküm yok); (2) "Bukhari, Adhan: 148" (find_by_citation, get_hadith); (3) hasta
  ziyareti (semantic_search); (4) Ebû Dâvûd'un namaz kitabının bölümleri (list_books, get_outline, read_chapter);
  (5) "تفكر ساعة خير من عبادة سنة" Risale'de nerede (get_hadith'in `linked_in_works`'ü; metni vermez, yerini verir).
- **Tefsir olumlu:** (1) Fâtiha 1:5'te Zemahşerî ve Beyzâvî (find_ayah, read_section, cite); (2) Âyetü'l-Kürsî'de
  müfessirler vefat sırasıyla (find_ayah); (3) "الحروف المقطعة" (search); (4) Kur'ân'da temsillerin hikmeti
  (semantic_search); (5) Keşşâf'ta "فإن قلت: لم قضيت لهذه الألفاظ" (Bakara 2:1) (find_sentence).
- **Klasik Eserler olumlu:** (1) Delâil'de i'câz ve nazım (semantic_search, read_section, cite); (2) Müfredât'ta
  "nûr" (search ya da get_outline, read_section); (3) Ta'rîfât'ta istiarenin tarifi (search); (4) "الابتداء: هو أول
  جزء" (find_sentence); (5) Bakara 2:255'in bu eserlerde geçtiği yerler (find_ayah, get_ayah).
- **Olumsuz (hepsinde):** hava durumu; "bu hadis sahih mi, sen karar ver" (hüküm vermez, derecesi kaynağında varsa
  âlimin adıyla verir; Hadis'te); "yeni bir tefsir yaz" (yazdığına tefsir demez; Tefsir'de ve Klasik'te); ilgisiz bir çeviri.

Her başvuruda tanıtım videosu ayrı (o eklentinin beş senaryosu) ve alan adı jetonu ayrı (§1.5).

**Additional Submission Context** (2026-11-23; kullanıcının kararı: üçü Risale'nin sonucunu beklemeden gönderilir,
inceleme ≈1 ay sürüyor). Ortak maddeler (yayıncı, üçüncü taraf, son paragraf) üçünde aynı.

Hadith Library:

> - Publisher: the app is published under my verified individual identity, Fatih Ebrar İnan. The website's privacy
>   policy and terms name the same person as publisher and operator (risalemcp.com/en/privacy.html,
>   risalemcp.com/en/terms.html).
> - Name: "Hadith Library" describes what the app holds; it is not a brand we claim. It is one of four apps of the
>   same volunteer project, "Risale MCP", after its domain risalemcp.com, which I own; this app's server,
>   hadis.risalemcp.com, is verified with the domain token. The others are Risale-i Nur Library (in review), Tafsir
>   Library and Classical Islamic Library. "MCP" is left out of the app name because the guidelines require it.
> - Content: the books are classical hadith collections in their original Arabic, from OpenITI (KITAB project),
>   licensed CC BY-NC-SA 4.0. We serve the text unchanged, name the source and edition in each book's record, and the
>   project is non-commercial, as the licence requires. The international numbers and the scholars' grades for the
>   Six Books and the Muwatta come from Hadith API (Unlicense). The Qur'an's text and the Türkiye Diyanet Vakfı
>   translation come from Tanzil (tanzil.net), used as its terms allow (non-commercial).
> - Religious content: the app never rules on whether a report is authentic. Grades appear only where a source holds
>   them, with the scholar's name, and the server's instructions tell the assistant not to judge soundness itself. A
>   match in a book that collects sayings current among people (al-'Ajluni's Kashf al-Khafa) carries a note that it
>   is not a sign of soundness. Translations made by the assistant are labelled as AI translations.
> - Demo video: in the fifth scenario our Risale-i Nur Library app was also enabled in the chat, so ChatGPT read the
>   linked Risale-i Nur passages there as well. With Hadith Library alone, the app gives those places by citation
>   only (their text is not on this server), as the test case describes.
> - Third party: semantic_search sends only the search phrase to Voyage AI to compute its meaning; the server keeps
>   the result in memory and never writes it to disk (privacy policy). The server is open to all and its limits are
>   shared by all users (120 requests a minute, 2,000 semantic searches a day); if a test hits one, the error says
>   so and the word search keeps working.
>
> It is a volunteer, non-commercial project. All tools are read-only and work without an account or sign-in. No
> conversation content or tool inputs are stored; only the tool name, time, duration and error type are kept, for 90
> days.

Tafsir Library:

> - Publisher: (Hadith Library ile aynı)
> - Name: "Tafsir Library" describes what the app holds; it is not a brand we claim. It is one of four apps of the
>   same volunteer project, "Risale MCP", after its domain risalemcp.com, which I own; this app's server,
>   tefsir.risalemcp.com, is verified with the domain token. The others are Risale-i Nur Library (in review), Hadith
>   Library and Classical Islamic Library. "MCP" is left out of the app name because the guidelines require it.
> - Content: thirteen classical works of Qur'anic exegesis in their original Arabic, from OpenITI (KITAB project),
>   licensed CC BY-NC-SA 4.0, each in the edition named in its record; verse-unit boundaries come from OpenITI's
>   altafsir.com-based version, the text always from the chosen edition. We serve the text unchanged, name the
>   source, and the project is non-commercial, as the licence requires. The Qur'an's text and the Türkiye Diyanet
>   Vakfı translation come from Tanzil (tanzil.net), used as its terms allow (non-commercial).
> - Religious content: the classical works are tafsir and are named so; nothing the assistant writes (a summary, a
>   comparison, a draft) is called tafsir, and its translations are labelled as AI translations. Each work's words
>   are quoted exactly with their source, and two exegetes treating the same verse is never presented as one
>   following or answering the other unless the text records it.
> - Demo video: in the third scenario our Classical Islamic Library app was also enabled in the chat, so one result
>   comes from al-Raghib's al-Mufradat, which is on that server, not this one. All other results come from the
>   thirteen tafsir works.
> - Third party: (Hadith Library ile aynı)
>
> (Son paragraf Hadith Library ile aynı.)

Classical Islamic Library:

> - Publisher: (Hadith Library ile aynı)
> - Name: "Classical Islamic Library" describes what the app holds; it is not a brand we claim. It is one of four
>   apps of the same volunteer project, "Risale MCP", after its domain risalemcp.com, which I own; this app's server,
>   klasik.risalemcp.com, is verified with the domain token. The others are Risale-i Nur Library (in review), Hadith
>   Library and Tafsir Library. "MCP" is left out of the app name because the guidelines require it.
> - Content: five classical Arabic works on rhetoric, language and terms (al-Jurjani's Dala'il al-I'jaz and Asrar
>   al-Balagha, al-Raghib's al-Mufradat, al-Sakkaki's Miftah al-'Ulum, al-Sayyid al-Sharif al-Jurjani's al-Ta'rifat)
>   in their original Arabic, from OpenITI (KITAB project), licensed CC BY-NC-SA 4.0, each in the edition named in
>   its record. We serve the text unchanged, name the source, and the project is non-commercial, as the licence
>   requires. The Qur'an's text and the Türkiye Diyanet Vakfı translation come from Tanzil (tanzil.net), used as its
>   terms allow (non-commercial).
> - Authorship: each work's words are quoted exactly and attributed to its author; editors' introductions and the
>   editor's numbered paragraphs of the Dala'il are named as the editor's. Translations made by the assistant are
>   labelled as AI translations.
> - Demo video: the fifth scenario asks about one work ("Where is al-Baqara 2:255 quoted in Dala'il al-I'jaz?")
>   rather than all of them as in the test case. The app answers that the Dala'il does not quote the verse and that
>   the library's six occurrences are all in al-Mufradat, and gives the verse's text from the Qur'an tool.
> - Third party: (Hadith Library ile aynı)
>
> (Son paragraf Hadith Library ile aynı.)

## 2e. Claude Risale: dizin ekibine e-posta ve dört sunucunun denetimi (2026-11-22)

**Denetim** (dizin ölçütleri, `claude.com/docs/connectors/building/review-criteria`, 2026-11-22'de okundu; canlı
sunuculardan `tools/list` ve hatalı çağrı):

| Ölçüt | Bulgu | Durum |
|---|---|---|
| Her araçta `title` ve `readOnlyHint` | 42 aracın hepsinde (`readOnlyHint: true`, `destructiveHint: false`) | uygun |
| Açıklama aracın gerçek davranışına uymalı | **Tefsir ve Klasik, Risale'nin açıklamalarını aynen taşıyordu**: hâşiye, telif tarihi, Risale'nin bağ türleri, `sozler/10` örnekleri, `group` değerleri `eski-said, ana-cilt…` | düzeltildi (`server.TEXTS_DOCS`, `TEFSIR_DOCS`, `PARAM_HELP`; test) |
| Hata iletileri açıklamalı olmalı | Sorgu dilinin hataları Türkçeydi ("NEAR( kapanmamış."), dört sunucuda | İngilizceye çevrildi |
| Açık kipte doğru ileti | `semantic_search` günlük sınırında "A user with an account can sign in" diyordu; açık kipte hesap yok | düzeltildi |
| Sunucu bilgisi | `version` boştu, `website_url` yoktu | paket sürümü ve `risalemcp.com/en/<eklenti>.html` |
| Üçüncü taraf (Voyage AI) | Gizlilik politikası iki dilde anıyor: yalnız arama ifadesi gider, saklanmaz | uygun |
| Konuşma verisi | Parametre ve IP kaydedilmez (politika) | uygun |
| Açıklamada başka araca ya da davranışa buyruk | Yok; `cite` "cevaptan önce bir kez çağır" der (ne zaman çağrılacağını söylemek ölçüte uygun) | uygun |

Bilinen ve bırakılan: yanlış adlı parametrede SDK'nın pydantic iletisi ("Field required"); açıklamalı, ölçüte uygun.

**E-posta** (belgenin verdiği kanal: bağdaştırıcı için `mcp-review@anthropic.com`; `directory@` eklenti paketleri
içindir, cevabı gecikebilir). Belge şunları ister: listelemenin adı, gönderildiği organizasyon, portalın gösterdiği
durum. Gönderen: Claude hesabınızın birincil iletişim adresi. Köşeli ayraçlı yerleri portaldan doldurun. Kod
düzeltmeleri yayına çıkmadan göndermeyin (son paragraf onları anıyor).

> **To:** mcp-review@anthropic.com
> **Subject:** Connector listing "Risale MCP Risale-i Nur": In review since 16 November
>
> Hello,
>
> Our connector submission has been in "In review" for some time, and I would be grateful to know whether
> anything is needed from us.
>
> - Listing name: Risale MCP Risale-i Nur (slug: [portaldaki slug])
> - Organization: [portaldaki organizasyon adı]
> - Status shown in the portal: In review (resubmitted on 16 November 2026; the first submission was on
>   29 October 2026)
> - Server URL: https://mcp.risalemcp.com/mcp (no authentication, public read-only data)
>
> The connector gives Claude sentence-level, citable access to the works of Bediüzzaman Said Nursî, served with
> the permission of their sources. All 12 tools are read-only and carry titles and annotations; documentation is
> at https://risalemcp.com/en/risale.html and the privacy policy at https://risalemcp.com/en/privacy.html. Our
> three companion connectors from the same organization (Risale MCP Hadis, Tefsir and Klasik) were approved as
> Community listings by the automatic review on 16 November.
>
> On 22 November we reviewed all four servers against the pre-submission checklist and made small fixes (clearer
> English error messages for the search syntax, tool descriptions that match each server's own works, server
> version and documentation URL in the server info).
>
> If the review needs a test prompt, a demo, or any change on our side, please let me know.
>
> Thank you,
> [adınız]

Bir hafta cevap gelmezse (≈2026-11-30): başvuru silinir, `risale.risalemcp.com/mcp` adresiyle yeniden gönderilir
(`PLANLAR.md` S4.3).

## 8. Kontrol listesi (gönderirken işaretleyin)

- [x] §1.1 yayıncı adı "Risale MCP", site ve politikalar yayında (2026-11-16)
- [x] §1.4 dört ayrı simge, alt alan adları yayında (2026-11-16)
- [ ] Claude Risale: herkese açık adresli bağdaştırıcı hesapta, test istemleri denendi, eski başvuru silindi, yenisi gönderildi (§2a)
- [x] Claude Hadis: gönderildi, otomatik taramayla onaylandı (2026-11-16); yayımlanacak
- [ ] Claude Tefsir: aynı
- [ ] Claude Klasik Eserler: aynı
- [ ] OpenAI Risale: paket güncellendi, video, jeton, gönderildi
- [ ] OpenAI Hadis: paket, video, jeton, gönderildi (Risale'yi beklemeden, kullanıcının kararı 2026-11-23)
- [ ] OpenAI Tefsir: paket, video, jeton, gönderildi (Risale'yi beklemeden, kullanıcının kararı 2026-11-23)
- [ ] OpenAI Klasik Eserler: paket, video, jeton, gönderildi (Risale'yi beklemeden, kullanıcının kararı 2026-11-23)
- [ ] Claude eklentisi (plugin): depo hazır (§9); isteğe bağlı claude.ai denemesi; "Plugin bundle" gönderildi
- [ ] Kabullerden sonra: sitedeki kurulum sayfalarında dizinden ekleme yolu (`site/claude.html`'deki yorum satırı),
      Yenilikler yazısı


## 9. Claude eklentisi (plugin, S4.7; hazır 2026-11-23)

Depo: **https://github.com/fatihebrarinan/risale-library-plugin** (herkese açık, dal `main`, eklenti deponun kökünde).
İçerik `packaging/claude-plugin/`'den `python3 scripts/claude-plugin.py build` ile üretilir; değişiklikten sonra
depoda commit ve push, `plugin.json`'daki `version` artırılır (her yeni sürüm otomatik denetimden geçer).
`claude plugin validate` uyarısız geçti.

**İsteğe bağlı ön deneme (claude.ai):** Customize › Plugins › Add › Upload plugin, dosya
`data/interim/claude-plugin/risale-library-1.0.0.zip` (`python3 scripts/claude-plugin.py zip`). Sonra eklentinin
Connectors sekmesinden dört bağdaştırıcı eklenir (kullanıcı her birini ayrıca bağlar). Bakılacak: tevekkül gibi bir
soruda ve Âyetü'l-Kürsî sorusunda skill yükleniyor mu (Claude Code'da yüklendi; claude.ai'nin seçimi aynı olmayabilir).
Hesabınızda zaten ekli olan aynı adresli özel bağdaştırıcılar varsa araçlar iki kez görünebilir: denemede onları
kapatın.

**Portal:** https://claude.ai/directory/manage › Submit new › **Plugin bundle**

| Alan | Değer |
|---|---|
| Source: repository | `https://github.com/fatihebrarinan/risale-library-plugin` |
| Plugin path | `.` (kök) |
| Branch / tag | `main` |
| Listing | README listeleme metni olur; ad ve kısa açıklama `plugin.json`'dan ("Risale-i Nur Library") |
| Data handling | Eklentinin kendisi hiçbir şey göndermez, kod çalıştırmaz. Bağdaştırıcılar yalnız aracın girdisini alır (arama ifadesi, kimlik, alıntılanan sözler); anlamsal aramada arama ifadesi Voyage AI'a gider; istek başına zaman, bağdaştırıcı, araç, süre, hata türü 90 gün; ifade, alıntı ve IP kaydedilmez. Gizlilik: `https://risalemcp.com/en/privacy.html` |
| Compliance | iletişim `destek@risalemcp.com`, dört onay kutusu |
| Eşleştirme | Portal sunarsa eklenti, aynı adresli dört bağdaştırıcı listelemesiyle (§2a–§2d) eşleştirilir |

Ek not önerisi (portal sorarsa):

> This plugin bundles our four read-only MCP connectors, already submitted as connector listings with the same URLs
> (Risale-i Nur Library, Hadith Library, Tafsir Library, Classical Islamic Library), and eight skills that teach Claude
> how to search, read, quote and cite them: core citation rules, a cross-library workflow for a Qur'anic verse, a
> hadith-checking workflow, and our former MCP prompts (topic survey, text and commentary, study circle, self test,
> lesson plan). The plugin holds no texts and runs no code. Test prompts: "Risale-i Nur'da tevekkül nasıl anlatılır?",
> "Âyetü'l-Kürsî'yi Risale-i Nur nasıl ele alıyor, müfessirler ne diyor?", "\"Ümmetimin ihtilafı rahmettir\" sözü
> hadis mi?".
