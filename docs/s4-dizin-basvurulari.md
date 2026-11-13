# S4: Dizin başvuruları, yapılacaklar (2026-11-13)

`PLANLAR.md` S4'ün uygulama belgesi: altı başvurunun her biri için sizin yapacaklarınız, portala yapıştırılacak
metinler (İngilizce; hakemler İngilizce okur) ve göndermeden önceki denetimler. Eski belgeler ayrıntı ve geçmiştir:
`docs/dizin-basvurusu.md` (Claude, Risale), `docs/chatgpt-dizin-basvurusu.md` (OpenAI, Risale),
`docs/dizin-politikalari.md` (iki dizinin kuralları).

| # | Dizin | Eklenti | Durum | Bu belgede |
|---|---|---|---|---|
| 1 | Claude | Risale-i Nur | "in review" (S4.3) | §2: listeleme metnini düzeltin (eski sayılar, kaldırılan Diyanet meali) |
| 2 | Claude | Hadis | gönderilmedi | §3 |
| 3 | Claude | Tefsir | gönderilmedi | §4 |
| 4 | OpenAI | Risale | reddedildi (kimlik) | §5–§6: kişisel kimliğe geçiş, düzeltilmiş paket, yeniden başvuru |
| 5 | OpenAI | Hadis | gönderilmedi | §7 |
| 6 | OpenAI | Tefsir | gönderilmedi | §7 |

Önerilen sıra: §1 (ortak hazırlık; sitedeki yayıncı adı OpenAI için şart) → §2 → §3 ve §4 (Claude, aynı gün olabilir)
→ §5 ve §6 (OpenAI Risale) → kabul ya da ilk geri dönüt gelince §7 (OpenAI'de aynı ret sebebi üç kez gelmesin diye
önce bir başvurunun sonucu görülür). OpenAI'nin alan adı doğrulaması tek dosyadır (§1.5): üç başvuru aynı anda
doğrulanamaz.

## 1. Ortak hazırlık (bir kez)

### 1.1 Yayıncı adı (sizin kararınız; OpenAI için şart)

OpenAI'nin kuralı: dizindeki geliştirici adı doğrulanmış kimlikten gelir, eklentinin açık adresleri (site, gizlilik,
şartlar) "aynı yayıncıyı göstermeli" (S4.1'in araştırması). Kararınız (a): doğrulanmış kendi adınızla. Bu yüzden:

- `site/gizlilik.html` "Sorumlu" ve `site/en/privacy.html` aynı bölüm: "Nur Hadimleri" yerine doğrulanmış adınız
  (OpenAI'deki doğrulamada yazdığı biçimiyle, harfi harfine).
- `site/kullanim-sartlari.html`, `site/en/terms.html`: hizmeti sunanın adı aynı ad.
- Sayfaların alt bilgisi ("Nur Hadimleri: gönüllü ve bağımsız bir projedir…", `scripts/site-uret.py` üretir):
  öneri "Risale MCP: [adınız] tarafından yürütülen gönüllü ve bağımsız bir projedir; herhangi bir yayınevi ya da
  cemaatin resmî hizmeti değildir." "Nur Hadimleri" adı sitede kalmaz ya da yalnız tarihçe olarak geçer.
- Claude başvurusundaki "Company name" (`docs/dizin-basvurusu.md` §5): aynı ad ya da "Risale MCP". Claude kimlik
  doğrulaması istemedi; ama iki dizinde aynı yayıncı görünmesi daha temiz.

Bunları ben yapabilirim (site üretimi, `?v=N`, `scripts/deploy.sh --code`); deploy sizin onayınızla. Adın yazılışını
OpenAI'deki doğrulamadan siz verin.

### 1.2 Eski bilgilerin düzeltilmesi (her listelemede)

| Eski metin | Doğrusu (2026-11-13, `scripts/site-uret.py` sayıları) |
|---|---|
| "About 126,000 sentences across 44 works" | "About 131,000 sentences across 53 works" (Osmanlıca ciltler hariç; 16 Osmanlıca cilt ayrıca) |
| "two Turkish translations by Diyanet" (Claude listelemesi) | "the Türkiye Diyanet Foundation's Turkish translation" (Diyanet İşleri meali 2026-11-12'de çıkarıldı, B6) |
| "10 tools" | Risale 12, Hadis 9, Tefsir 11 araç; hepsi `readOnlyHint: true`, `destructiveHint: false`, `openWorldHint: false`, başlıklı (`server.py` `read_only`; 23 kayıt denetlendi) |

### 1.3 Gizli hata ayıklama adresleriyle deneme

Her başvurudan önce, o eklentinin test istemleri claude.ai'de ve ChatGPT'de bir kez çalıştırılır; araç zinciri gizli
adresle izlenir:

```
scripts/sunucu.sh auth debug-url --new                      # Risale: https://mcp.risalemcp.com/mcp/<anahtar>
scripts/sunucu.sh auth --server hadis debug-url --new       # Hadis: /hadis/<anahtar>
scripts/tefsir-sunucu.sh auth debug-url --new               # Tefsir: /tefsir/<anahtar> (kayıt tefsir makinesinde)
scripts/sunucu.sh auth usage --user '(debug)' --params      # kayıt (Risale ve Hadis; --only hadis süzer)
```

Denedikten sonra adresleri kapatın (`--revoke`).

### 1.4 Simgeler

Üç eklenti bugün aynı simgeyi kullanıyor (`src/risale_mcp/static/icon.png`, 256×256). Dizinde üç aynı simge kafa
karıştırır. Öneri: aynı çizgide üç ayrı simge (ör. ortak zemin, üstünde "R", "H", "T" ya da renk farkı). Karar
sizin; isterseniz `icon.svg`'den üç türev çıkarırım (`scripts/ikon.sh`). Hadis ve tefsir sunucuları simgeyi
`/favicon.ico`'dan değil, başvuruda yüklenen dosyadan alır.

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

## 2. Claude: Risale-i Nur (incelemede)

Portal: https://claude.ai/directory/manage. Başvuruyu açın, **Edit**:

1. **Description**: §1.2'deki iki düzeltme. Yeni metin:

   > Risale-i Nur gives Claude the complete works of Bediüzzaman Said Nursî (1878–1960): the Risale-i Nur Collection
   > (Sözler, Mektubat, Lem'alar, Şualar, the Lâhikas, Tarihçe-i Hayat), the works of his early period, the
   > compilations and the Hizbs, in Turkish and, for the works he wrote in Arabic, in Arabic too. About 131,000
   > sentences across 53 works, together with the Qur'an's vowelled Arabic text and the Türkiye Diyanet
   > Foundation's Turkish translation.
   >
   > (sonraki paragraflar `docs/dizin-basvurusu.md` §3'teki gibi; yalnız son paragrafın sonu:)
   > All tools are read-only and work without an account. The texts come, unchanged and with permission, from
   > e-Risale, risaleoku.com and nurpedia.org; the Qur'an's text from the Tanzil Project. A volunteer,
   > non-commercial project.

   Not: eski metin kaynaklarda "risale.online" diyor; o kaynak yalnız yerelde (Sirâcü'n-Nûr'un Hayrat baskısı),
   genel sunucuda yok. Genel sunucunun kaynakları e-Risale, risaleoku.com, nurpedia.org, Keşif programı (Ta'likat)
   ve kullanıcının PDF'i (Rumuzat tabloları).

2. **Use cases**: aynen kalır. İsterseniz bir satır ekleyin (hadis aracı sonradan geldi):
   | Find where a hadith is quoted in the works and how well it is attested | Where does the Risale-i Nur quote the hadith "تفكر ساعة خير من عبادة سنة" and what is the evidence for it? |
3. **Company name**: §1.1'in kararı.
4. **Instructions for reviewers**: `docs/dizin-basvurusu.md` §8'in sonuna ekleyin:
   > - "Where does the Risale-i Nur quote the hadith 'تفكر ساعة خير من عبادة سنة'? What is the evidence for it?" (find_hadith, get_hadith)
5. Hakeme kısa not (değişiklik bildirimi):
   > Listing updated: corrected counts (53 works, about 131,000 sentences) and the Qur'an translation (one Turkish
   > translation, by the Türkiye Diyanet Foundation; the other was removed at its publisher's request). Two tools
   > were added since submission (find_hadith, get_hadith), both read-only. Everything else is unchanged.

## 3. Claude: Hadis (yeni başvuru)

Portal › **Submit new** › **MCP connector**.

- **Server URL:** `https://mcp.risalemcp.com/hadis` · Users connect to different URLs: **no**.
- **Server name** (öneri; karar sizin): `Risale MCP Hadis`. Gerekçe: "Hadis" tek başına genel bir ad, dizinde
  aranmaz ve başka eklentilerle karışır; "Risale MCP" alan adımızın adıdır, üç eklentiyi bir aile olarak gösterir.
  Slug (değişmez): `risale-mcp-hadis`.
- **One-liner** (≤200):
  > Read and cite eighteen classical hadith collections in Arabic, report by report, with grades only as the
  > sources give them.
- **Description** (≤2000):
  > Risale MCP Hadis gives Claude eighteen classical hadith collections in their original Arabic: the Six Books
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
- **Categories:** Education, Research / Reference, Religion (portalda hangisi varsa).
- **Documentation URL:** `https://risalemcp.com/en/hadith.html` · **Privacy:** `https://risalemcp.com/en/privacy.html`
  (üç eklentiyi kapsıyor) · **Support:** `destek@risalemcp.com` · **Icon:** §1.4.
- **Use cases:**

  | Use case | Example prompt |
  |---|---|
  | Find in which books a saying occurs, without a ruling | In which books does the saying "اختلاف أمتي رحمة" occur, and what is said about it? With sources, without a ruling. |
  | Go from a reference to the report | Show me Bukhari, Adhan: 148 with its chain and text, and translate it. |
  | Find reports on a topic by meaning | Find reports about visiting the sick, with their sources. |
  | Find reports by a narrator | Which reports in Muslim's Sahih does Abu Hurayra narrate about fasting on the day of Arafa? |
  | Browse a collection | Show the chapters of the Book of Prayer in Sunan Abi Dawud. |
  | See where the Risale-i Nur quotes a report | Where does the Risale-i Nur quote the report "تفكر ساعة خير من عبادة سنة"? |

- **What users need before they can connect:** "Nothing. There are no accounts and no sign-in: every tool works for
  everyone. Search by meaning has a shared daily limit and requests a shared per-minute limit."
- **Reads / writes:** reads only. **Company:** §1.1. **Authentication:** None. **Data handling:** own API (kendi
  veritabanımız; anlamsal arama sorgusu vektör için Voyage AI'ya gider, gizlilik politikasında yazılı). Personal
  health data: no. Sponsored content: no. **Test account:** yok.
- **Instructions for reviewers:**
  > 1. Add a custom connector with the URL https://mcp.risalemcp.com/hadis. No sign-in is needed.
  > 2. Prompts that exercise every tool (the books are in Arabic; questions can be asked in English):
  >    - "List the books in the Hadis connector and show the outline of Sunan Abi Dawud." (list_books, get_outline)
  >    - "Show the chapter on the call to prayer (adhan) in Sahih al-Bukhari." (read_chapter)
  >    - "Find Bukhari, Adhan: 148 and show its chain and text." (find_by_citation, get_hadith)
  >    - "Search for reports with the words 'إنما الأعمال بالنيات'." (search_hadith)
  >    - "Find reports about kindness to neighbours." (semantic_search)
  >    - "Show the verse Bakara 2:255." (get_ayah)
  >    - Any answer that quotes a report calls cite before it is written.
  > 3. Expected: Arabic quoted exactly in block quotes, the assistant's translation labelled as its own, each
  >    quotation marked [1], [2]… with a sources list at the end; no ruling on a report's soundness (grades only as
  >    the source gives them, with the scholar's name).
- **Compliance:** yedi onay (§2 ile aynı gerekçeler). Göndermeden önce istemleri claude.ai'de deneyin (§1.3).

## 4. Claude: Tefsir (yeni başvuru)

- **Server URL:** `https://mcp.risalemcp.com/tefsir` · different URLs: **no**.
- **Server name** (öneri): `Risale MCP Tefsir`, slug `risale-mcp-tefsir` (§3'teki gerekçe).
- **One-liner:**
  > Read and cite thirteen classical works of Qur'anic exegesis in Arabic, verse by verse, from al-Tabari to
  > al-Alusi.
- **Description:**
  > Risale MCP Tefsir gives Claude thirteen classical works of Qur'anic exegesis (tafsir) in their original
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
- **Docs:** `https://risalemcp.com/en/tafsir.html` · Privacy, support, icon: §3 gibi.
- **Use cases:**

  | Use case | Example prompt |
  |---|---|
  | Compare what classical exegetes say about a verse | What do al-Zamakhshari and al-Baydawi say about "iyyaka na'budu" (al-Fatiha 1:5)? Quote them with sources. |
  | Survey the exegetes on a verse in order | Go through the exegetes on Ayat al-Kursi (al-Baqara 2:255) in order of their deaths, one key point each. |
  | Find a term across the works | Where do the exegetes discuss "الحروف المقطعة" (the disjointed letters)? |
  | Find a discussion by meaning | Which exegetes explain why the Qur'an uses parables, and how? |
  | Locate a sentence someone quotes | Find the sentence in al-Kashshaf that begins "فإن قلت: لم قضيت لهذه الألفاظ" (al-Baqara 2:1). |

- Ön koşul, yazma, şirket, kimlik doğrulama, veri, hesap: §3 gibi.
- **Instructions for reviewers:**
  > 1. Add a custom connector with the URL https://mcp.risalemcp.com/tefsir. No sign-in is needed.
  > 2. Prompts that exercise every tool:
  >    - "List the works in the Tefsir connector and show the outline of al-Baydawi's Anwar al-Tanzil." (list_works, get_outline)
  >    - "What do the exegetes say about al-Fatiha 1:5? Read al-Zamakhshari's unit and quote him." (find_ayah, read_section, get_passage, cite)
  >    - "Search the works for 'الحروف المقطعة'." (search) and "Which exegetes explain the purpose of the Qur'an's parables?" (semantic_search)
  >    - "Find the sentence that begins 'فإن قلت: لم قضيت لهذه الألفاظ' in al-Kashshaf." (find_sentence)
  >    - "Show the verse al-Baqara 2:255 and any recorded links between texts on it." (get_ayah, text_links)
  > 3. Expected: Arabic quoted exactly, the assistant's translation labelled as its own, a numbered sources list;
  >    the assistant never calls its own summary "tafsir".

Not: tefsir sunucusunun yükü ayrı makinededir (CAX21); hakem denemesinde bir sorun olursa Caddy'nin `/tefsir`
yönlendirmesi ve `scripts/tefsir-sunucu.sh` kayıtları.

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

Değişecekler (`packaging/chatgpt/plugin.json`; S4.2 kararı: uygulama adı "Risale MCP"):

| Alan | Bugün | Yeni |
|---|---|---|
| `name` | `risale-i-nur` | `risale-mcp` |
| `interface.displayName` | Risale-i Nur | Risale MCP |
| `interface.developerName`, `author.name` | Nur Hadimleri | doğrulanmış adınız (§1.1) |
| `interface.shortDescription` (≤30) | Cite the Risale-i Nur exactly | Cite the Risale-i Nur exactly (kalır) |
| açıklamalar | "126,000 sentences across 44 works", "by Nur Hadimleri" | "131,000 sentences across 53 works"; son cümle "A volunteer, non-commercial project." |
| `tr-TR` açıklama | aynı eski sayılar ve "Nur Hadimleri'nin…" | "53 eserde yaklaşık 131 bin cümle"; son cümle "Gönüllü ve ticari olmayan bir projedir." |
| `mcp.json` sunucu anahtarı | `risale-i-nur` | `risale-mcp` (adres aynı) |
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

## 7. OpenAI: Hadis ve Tefsir

Her biri ayrı paket (`packaging/chatgpt-hadis/`, `packaging/chatgpt-tefsir/`; betik eklenti adını alacak biçimde
genişletilir; ben hazırlarım):

| Alan | Hadis | Tefsir |
|---|---|---|
| `name` | `risale-mcp-hadis` | `risale-mcp-tefsir` |
| `displayName` | Risale MCP Hadis | Risale MCP Tefsir |
| `shortDescription` (≤30) | Cite hadith collections | Cite classical tafsir works |
| sunucu | `https://mcp.risalemcp.com/hadis` | `https://mcp.risalemcp.com/tefsir` |
| açıklama | §3'teki Description ("Claude" yerine "ChatGPT") | §4'teki Description |
| `websiteURL` | `https://risalemcp.com/en/hadith.html` | `https://risalemcp.com/en/tafsir.html` |
| `defaultPrompt` | §3'ün ilk üç kullanım istemi | §4'ün ilk üç kullanım istemi |
| kategori, gizlilik, şartlar, destek, yayıncı | Risale ile aynı | Risale ile aynı |

Test senaryoları (pakete):
- **Hadis olumlu:** (1) "اختلاف أمتي رحمة" hangi kitaplarda (search_hadith, get_hadith, cite; beklenen: Keşfü'l-Hafâ
  gibi kitapların `book_note`'u, hüküm yok); (2) "Bukhari, Adhan: 148" (find_by_citation, get_hadith); (3) hasta
  ziyareti (semantic_search); (4) Ebû Dâvûd'un namaz kitabının bölümleri (list_books, get_outline, read_chapter);
  (5) "تفكر ساعة خير من عبادة سنة" Risale'de nerede (get_hadith'in `linked_in_works`'ü; metni vermez, yerini verir).
- **Tefsir olumlu:** (1) Fâtiha 1:5'te Zemahşerî ve Beyzâvî (find_ayah, read_section, cite); (2) Âyetü'l-Kürsî'de
  müfessirler vefat sırasıyla (find_ayah); (3) "الحروف المقطعة" (search); (4) Kur'ân'da temsillerin hikmeti
  (semantic_search); (5) Keşşâf'ta "فإن قلت: لم قضيت لهذه الألفاظ" (Bakara 2:1) (find_sentence).
- **Olumsuz (ikisinde):** hava durumu; "bu hadis sahih mi, sen karar ver" (hüküm vermez, derecesi kaynağında varsa
  âlimin adıyla verir; Hadis'te); "yeni bir tefsir yaz" (yazdığına tefsir demez; Tefsir'de); ilgisiz bir çeviri.

Her başvuruda tanıtım videosu ayrı (o eklentinin beş senaryosu) ve alan adı jetonu ayrı (§1.5).

## 8. Kontrol listesi (gönderirken işaretleyin)

- [ ] §1.1 yayıncı adı kararlaştırıldı, site ve politikalar yayında (`scripts/deploy.sh --code`)
- [ ] §1.4 simgeler (üç ayrı ya da bilerek aynı)
- [ ] Claude Risale: açıklama düzeltildi, hakeme not
- [ ] Claude Hadis: test istemleri denendi, gönderildi
- [ ] Claude Tefsir: test istemleri denendi, gönderildi
- [ ] OpenAI Risale: paket güncellendi, video, jeton, gönderildi
- [ ] OpenAI Hadis: paket, video, jeton, gönderildi (Risale'nin sonucundan sonra)
- [ ] OpenAI Tefsir: paket, video, jeton, gönderildi (Risale'nin sonucundan sonra)
- [ ] Kabullerden sonra: sitedeki kurulum sayfalarında dizinden ekleme yolu (`site/claude.html`'deki yorum satırı),
      Yenilikler yazısı
