# Anthropic bağlayıcı dizini başvurusu

Portal: https://claude.ai/directory/manage › **Submit new** › **MCP connector**. Adımlar portalın sırasıyladır.
Metinler İngilizcedir (dizin uluslararası; hakemler İngilizce okur). Hakem hesabının parolası burada yazılmaz:
sunucudadır, `scripts/sunucu.sh auth passwd admin` ile değiştirilir.

Belgeler: https://claude.com/docs/connectors/building/submission.md, ölçütler:
https://claude.com/docs/connectors/building/review-criteria.md, politika:
https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy.

## 1. Connection

- Server URL: `https://mcp.risalemcp.com/mcp`
- Users connect to different URLs: **hayır** (tek adres).

## 2. Tools

Sunucudan kendiliğinden gelir. 11 aracın hepsinde `title` ve `readOnlyHint: true` var; uyarı çıkmamalı.

## 3. Listing

**Server name** (≤100):

> Risale-i Nur

**One-liner** (≤200):

> Read and cite the complete works of Bediüzzaman Said Nursî, sentence by sentence, with the Qur'an's text alongside.

**Description** (≤2000):

> Risale-i Nur gives Claude the complete works of Bediüzzaman Said Nursî (1878–1960): the Risale-i Nur Collection (Sözler, Mektubat, Lem'alar, Şualar, the Lâhikas, Tarihçe-i Hayat), the works of his early period, the compilations and the Hizbs, in Turkish and, for the works he wrote in Arabic, in Arabic too. About 126,000 sentences across 44 works, together with the Qur'an's vowelled Arabic text and two Turkish translations by Diyanet.
>
> Every sentence has a stable address, so Claude can ground what it says in the text itself:
>
> - Search by the text's own words, or by meaning in today's language (a question about "despair" finds passages that speak of "ye's").
> - Read any section in book order, with the author's footnotes (hâşiye) and the sources of the verses and hadiths he quotes.
> - Quote the text exactly and end the answer with a list of sources giving work › section › the sentence's opening words. Quotations are checked against the cited sentences before the answer is sent.
> - Find where a Qur'anic verse is quoted in the works, and read the verse itself.
>
> The connector keeps layers apart that are easy to confuse: the publishers' translations of verses are not the author's words, the Turkish of his Arabic works is a translation, and a commentary by his brother is marked as his. When something is not in the works, Claude is told to say so instead of filling the gap.
>
> All tools are read-only and work without an account. The texts come, unchanged and with permission, from e-Risale, kastamonur.com, risale.online, risaleoku.com and rasaelalnour.com; the Qur'an's text from the Tanzil Project. A volunteer, non-commercial project by Nur Hadimleri.

**Categories** (1–5): portalın listesinden en yakınları: Education, Research / Reference, Religion / Culture (hangisi varsa).

- Documentation URL: `https://risalemcp.com/en/docs.html`
- Privacy policy URL: `https://risalemcp.com/en/privacy.html`
- Support contact: `destek@risalemcp.com`
- Icon: `src/risale_mcp/static/icon.png` (256×256 PNG)
- Slug (kalıcı, değişmez): `risale-i-nur`

## 4. Use cases

**Use cases** (portalda iki sütun: kullanım alanı ve örnek istem; her satır ayrı girilir):

| Use case | Example prompt |
|---|---|
| Answer questions about the Risale-i Nur with exact quotations and sources | Why is the time of the Last Day kept hidden, according to the Risale-i Nur? Quote the text and give the sources. |
| Survey where a topic is treated across the works | Where does Bediüzzaman write about patience in illness? List the main passages by work. |
| Study a section in order, with the author's footnotes | Read the Tenth Word's Ninth Truth with me and explain its argument step by step. |
| Prepare a lesson or study circle (ders) on a topic | Prepare a lesson on the parable of the two soldiers in the Third Word, with the passages to read aloud and questions for discussion. |
| Find a sentence someone quotes and see its context | Where is the sentence that begins "Hiç mümkün müdür ki; ölmüş" and what comes before and after it? |
| Find where a Qur'anic verse is quoted in the works and read the verse | Where is Âyetü'l-Kürsî (Bakara 2:255) quoted in the Risale-i Nur? Show the verse with a translation. |

**What users need before they can connect:**

> Nothing. Every tool works without an account. Users with an account (created by the administrator) have no usage limits; without one, search by meaning has a shared daily limit and requests a shared per-minute limit.

**Reads / writes:** reads data only.

## 5. Company

- Company name: `Nur Hadimleri`
- Website: `https://risalemcp.com`
- Primary contact: Fatih Ebrar İnan, `fatihebrarinan@protonmail.com` (ya da `destek@risalemcp.com`)

## 6. Authentication

- Authentication requirement: **Required when the server asks** (sunucu hesapsız açılır; yalnızca `sign_in` aracı girişi ister: lazy authentication).
- Authentication method: **OAuth**, Dynamic Client Registration ile. Anthropic'e istemci kimliği ve sırrı verilmez (alanlar boş).

## 7. Data handling

- Underlying API: **our own**. Sunucu kendi veritabanını sunar; metinler kaynak sitelerden izinle bir kez alınmıştır, çalışırken üçüncü bir API'ye istek gitmez. Tek istisna: anlamsal arama sorgusu vektör için Voyage AI'ya gider (gizlilik politikasında yazılı).
- Personal health data: **no**. Sponsored content: **no**.

## 8. Test & launch

**Test account:** kullanıcı adı `admin`, parola sunucuda (portala elle yazılır).

**Instructions for reviewers:**

> 1. Add a custom connector in Claude with the URL https://mcp.risalemcp.com/mcp. No sign-in is needed: every tool works without an account.
> 2. To test sign-in, ask Claude: "Sign in to Risale-i Nur." Claude shows a Connect card; sign in with the test account (user name: admin, password: below). The sign_in tool then reports the signed-in user.
> 3. Prompts that exercise every tool (the texts are in Turkish; questions can be asked in English):
>    - "List the works in the Risale-i Nur connector and show the outline of Sözler." (list_works, get_outline)
>    - "Why is the time of the Last Day kept hidden, according to the Risale-i Nur? Quote the text and give sources." (semantic_search, read_section or get_passage, cite)
>    - "Search the works for the phrase 'halk-ı şer şer değil' and explain the passage." (search, get_passage, cite)
>    - "Find the sentence that begins 'Hiç mümkün müdür ki; ölmüş'." (find_sentence)
>    - "Where is Âyetü'l-Kürsî (Bakara 2:255) quoted in the works? Show the verse with its translation." (find_ayah, get_ayah)
> 4. Expected: answers quote the text in block quotes, mark each quotation with [1], [2]… and end with a "Kaynaklar" (sources) list; asking about something that is not in the works (e.g. "Summarise the Fifteenth Truth of the Tenth Word") gets the answer that it does not exist.

Portalda "her aracı kendim çalıştırdım" onayı istenir: göndermeden önce yukarıdaki istemleri claude.ai'de bir kez deneyin.

## 9. Compliance

Yedi onayı okuyup işaretleyin. Bizimle ilgili olanlar: konuşma verisi toplamama (parametreler kaydedilmez, kayıt 90 gün), prompt injection (araç tanımları yalnızca aracın işini anlatır; sunucu talimatı atıf kurallarıdır), kamuya açık belgeler (risalemcp.com). Para transferi ve yapay zekâ ile medya üretimi yok.

## 10. Review and submit

Uyarıları okuyun, gönderin. Durum portalda; sorun olursa `mcp-review@anthropic.com`.
