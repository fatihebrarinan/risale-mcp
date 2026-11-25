# S12.6 taslağı: sohbet sayfası için gizlilik politikası ve kullanım şartları

Kullanıcının kararı (2026-11-25): metinler önce taslaktır; kullanıcı okuyup düzeltir, sonra sayfalara işlenir
(`site/gizlilik.html`, `site/kullanim-sartlari.html`, `site/en/privacy.html`, `site/en/terms.html`) ve deploy'la çıkar.
Bu dosya onaydan sonra silinir. Her cümle koddaki duruma dayanır (`sohbet.py`, `sohbet_hesap.py`); kod değişirse burası
da değişir.

Kontrol etmenizi istediğim tek yer: Anthropic'in API verisini model eğitiminde kullanmadığı cümlesi. Anthropic'in ticari
şartlarının bugünkü hâline dayanıyor; kendi sayfalarına bağlantı veriyorum, ama siz de bakın.

---

## 1. Gizlilik politikası (Türkçe)

### Değişecek cümleler

- **Giriş paragrafı**, "…ve bu sitenin (`risalemcp.com`) hangi verileri işlediğini anlatır." yerine:
  "…bu sitenin (`risalemcp.com`) ve sitedeki sohbet sayfasının (`risalemcp.com/sohbet/`) hangi verileri işlediğini
  anlatır."
- **IP adresleri ve çerezler**, "yalnız aşağıda anlatılan davetli çalışma bölümü bir oturum çerezi kullanır" yerine:
  "yalnız aşağıda anlatılan davetli çalışma bölümü ve sohbet sayfası birer oturum çerezi kullanır".
- **Paylaşım**, "Yukarıda anılan Voyage AI dışında kimseyle paylaşılmaz." yerine:
  "Yukarıda anılan Voyage AI ile sohbet sayfası için Anthropic ve Scaleway dışında kimseyle paylaşılmaz."
- **Barındırma**, ilk cümlenin sonuna: "Sohbet sayfası da Helsinki'deki sunucudadır."
- **Haklarınız**, "tek istisna davetli çalışma bölümünün hesaplarıdır." yerine:
  "istisnalar davetli çalışma bölümünün ve sohbet sayfasının hesaplarıdır."
- **Son güncelleme** tarihi: yayın günü.

### Yeni bölüm ("Davetli bölümler"den sonra, "Paylaşım"dan önce)

**Sohbet sayfası**

`risalemcp.com/sohbet/` sayfasında sorularınızı Risale-i Nur'dan cevaplayan bir yapay zekâyla yazışırsınız. Cevabı
Anthropic'in Claude modeli yazar; eserleri bu sunucudaki araçlarla okur, alıntıları sunucu eserlerin metniyle denetler.
Sayfa deneme aşamasındadır.

*Hesap.* Sayfayı kullanmak için hesap açarsınız. Saklananlar: e-posta adresiniz; parolanızın geri çevrilemez özeti
(parolanın kendisi saklanmaz); hesabın açıldığı ve son giriş yapıldığı zaman; yanlış deneme sayısı. Adresinizi
doğrulamak için gönderilen 6 haneli kodun yalnız özeti ve zamanları saklanır, kod kullanılınca ya da en geç bir gün
sonra silinir. Kötüye kullanımı sınırlamak için aynı ağ adresinden (IP) saatte kaç kod istendiği sayılır; bu sayı
yalnız sunucunun belleğinde tutulur, IP adresiniz yazılmaz. Giriş yaptığınızda tarayıcınıza bir oturum çerezi konur
(yalnız `/sohbet/` yolunda, 30 gün; "Çıkış" ile hemen kapanır); sunucuda çerezin yalnız özeti durur.

*E-posta.* Doğrulama kodu ve parola yenileme kodu size [Scaleway](https://www.scaleway.com/en/privacy-policy/)'in
e-posta hizmetiyle (Fransa, AB) gönderilir; Scaleway'e yalnız adresiniz ve kodu içeren e-postanın metni gider. Size
başka e-posta gönderilmez.

*Sorularınız ve cevaplar.* Konuşmanız sunucuda **saklanmaz**; yalnız kendi tarayıcınızda durur ("Yeni konuşma" ile
silinir). Bir soru sorduğunuzda soru, aynı konuşmadaki önceki sorular ve cevaplar ve yapay zekânın okuduğu eser
metinleri cevabın yazılması için [Anthropic](https://www.anthropic.com/legal/privacy)'e (Claude API) gönderilir.
Anthropic bu verileri [ticari hizmet şartlarına](https://www.anthropic.com/legal/commercial-terms) göre işler;
bu şartlara göre API ile gönderilen veriler Anthropic'in modellerini eğitmekte kullanılmaz. Yapay zekâ anlama göre
arama yaptığında arama ifadesi yukarıda anlatıldığı gibi Voyage AI'a gider. Sorularınıza kişisel ya da hassas bilgi
yazmamanızı rica ederiz.

*Kullanım kaydı.* Her soru için şunlar kaydedilir: zaman, hesabınız, kullanılan model, işlenen ve üretilen metin
miktarı (token), yaklaşık maliyet, yapay zekânın kaç kez eserlere baktığı, cevabın süresi ve atıf denetiminin sayıları
(kaç kaynak, kaçı düzeltildi, kaçı doğrulanamadı). Soru ve cevap bu kayda **girmez**. Kayıt, kişi başına günlük soru
hakkını ve sayfanın bütçe sınırını uygulamak ve hizmetin nasıl çalıştığını izlemek içindir; **90 gün** sonra silinir.

*Geri bildirim.* Bir cevabı 👍 ya da 👎 ile değerlendirebilir, isterseniz not ekleyebilirsiniz. Saklananlar: zaman,
hesabınız, oyunuz, notunuz ve kullanılan model. Soru ve cevap yalnız "Soruyu ve bu cevabı da gönder" kutusunu
işaretlerseniz, yalnız o cevap için gönderilir; kutu kendiliğinden işaretli değildir. Geri bildirimi proje ekibi
cevapları iyileştirmek ve denemelerde kullanılacak soruları seçmek için okur; **bir yıl** sonra silinir.

*Hesabınızı silmek.* "Hesap › Hesabımı sil" ile hesabınızı kendiniz silersiniz. Hesabınız, oturumlarınız ve kodlarınız
silinir; kullanım kaydındaki satırlarınızdan ve geri bildirimlerinizden adresiniz kaldırılır; notlarınız, gönderdiğiniz
sorular ve cevaplar silinir, yalnız oylar adsız kalır.

---

## 2. Kullanım şartları (Türkçe)

### Değişecek cümle

- **Giriş**, "Bu şartlar Risale-i Nur MCP eklentisinin (`mcp.risalemcp.com`) ve bu sitenin (`risalemcp.com`)
  kullanımı içindir." yerine: "Bu şartlar Risale-i Nur MCP eklentisinin (`mcp.risalemcp.com`), bu sitenin
  (`risalemcp.com`) ve sitedeki sohbet sayfasının (`risalemcp.com/sohbet/`) kullanımı içindir."

### Yeni bölüm ("Yapay zekâ cevapları"ndan sonra)

**Sohbet sayfası**

- Sohbet sayfası Risale-i Nur'dan cevap veren, ücretsiz, deneme aşamasında bir hizmettir. Cevapları Anthropic'in Claude
  modeli yazar; cevaplar yapay zekânındır, müellife mal edilmez, tefsir ya da fetva değildir. Yukarıdaki "Yapay zekâ
  cevapları" bölümü burada da geçerlidir: önemli bir konuda alıntıyı ve bağlamını eserin kendisinden kontrol edin.
- Sayfa yalnız Bediüzzaman Said Nursî'nin eserleri ve Kur'ân-ı Kerîm hakkındaki sorulara cevap verir.
- Her kişi bir hesap açar; hesabınızı başkasıyla paylaşmayın, sayfayı otomatik araçlarla kullanmayın.
- Kişi başına günlük soru hakkı ve sayfanın günlük ve aylık bütçesi vardır; bütçe dolunca sayfa o gün ya da o ay soru
  almaz.
- Sorularınıza kişisel ya da hassas bilgi yazmayın: sorular cevabın yazılması için Anthropic'e gönderilir (bkz.
  gizlilik politikası).
- Deneme aşamasındaki hizmet önceden haber verilmeden değiştirilebilir ya da kapatılabilir.

---

## 3. Privacy policy (English)

### Changed sentences

- **Introduction**: the list of what the page covers gains "and the chat page on this website
  (`risalemcp.com/sohbet/`)".
- **IP addresses and cookies**: "only the invitation-only working area described below uses a session cookie" becomes
  "only the invitation-only working area and the chat page described below use a session cookie".
- **Sharing**: "It is shared with no one other than Voyage AI as described above." becomes "It is shared with no one
  other than Voyage AI as described above and, for the chat page, Anthropic and Scaleway."
- **Hosting**: add "The chat page runs on the server in Helsinki."
- **Your rights**: "the only exception is the accounts of the invitation-only working area" becomes "the exceptions
  are the accounts of the invitation-only working area and of the chat page".

### New section

**Chat page**

On `risalemcp.com/sohbet/` you converse with an AI that answers your questions from the Risale-i Nur. The answer is
written by Anthropic's Claude model; it reads the works with the tools on this server, and the server checks the
quotations against the text. The page is in a trial phase.

*Account.* To use the page you open an account. We store: your email address; an irreversible hash of your password
(not the password itself); when the account was opened and when you last signed in; the number of failed attempts. Of
the 6-digit code sent to verify your address only a hash and its times are stored; it is deleted when used or after a
day at the latest. To limit abuse, the number of codes requested per hour from one network (IP) address is counted in
the server's memory only; your IP address is not written down. When you sign in, a session cookie is set in your browser (path
`/sohbet/` only, 30 days; "Çıkış" ends it at once); the server keeps only its hash.

*Email.* Verification and password-reset codes are sent through [Scaleway](https://www.scaleway.com/en/privacy-policy/)'s
email service (France, EU); Scaleway receives only your address and the text of the email with the code. You are sent
no other email.

*Your questions and the answers.* Your conversation is **not stored** on the server; it stays in your own browser
("Yeni konuşma" clears it). When you ask a question, the question, the earlier questions and answers of the same
conversation and the texts the AI reads are sent to [Anthropic](https://www.anthropic.com/legal/privacy) (Claude API)
to write the answer. Anthropic processes them under its
[commercial terms](https://www.anthropic.com/legal/commercial-terms), under which data sent through the API is not
used to train its models. When the AI searches by meaning, the query goes to Voyage AI as described above. Please do
not put personal or sensitive information in your questions.

*Usage log.* For each question we log: the time, your account, the model, the amount of text processed and produced
(tokens), the approximate cost, how many times the AI consulted the works, how long the answer took, and the counts of
the citation check (how many sources, how many corrected, how many could not be verified). The question and the answer
are **not** in this log. It serves the daily question allowance per person, the page's budget limit and monitoring;
it is deleted after **90 days**.

*Feedback.* You can rate an answer 👍 or 👎 and add a note. We store the time, your account, your rating, your note
and the model. The question and the answer are sent only if you tick "Soruyu ve bu cevabı da gönder", and only for that
answer; the box is not ticked by default. The project team reads feedback to improve the answers and to choose test
questions; it is deleted after **one year**.

*Deleting your account.* "Hesap › Hesabımı sil" deletes your account yourself. Your account, sessions and codes are
deleted; your address is removed from your usage log rows and your feedback; your notes and any questions and answers
you sent are deleted, only the ratings remain, anonymous.

---

## 4. Terms of use (English)

- **Introduction**: "These terms apply to the Risale-i Nur MCP connector (`mcp.risalemcp.com`) and this website
  (`risalemcp.com`)." becomes "These terms apply to the Risale-i Nur MCP connector (`mcp.risalemcp.com`), this website
  (`risalemcp.com`) and its chat page (`risalemcp.com/sohbet/`)."

**Chat page** (after "AI answers")

- The chat page is a free service in a trial phase that answers from the Risale-i Nur. The answers are written by
  Anthropic's Claude model; they are an AI's answers, not attributed to the author, and not tafsir or a fatwa. The "AI
  answers" section above applies here too: on an important matter, check the quotation and its context in the work
  itself.
- The page answers only questions about the works of Bediüzzaman Said Nursî and the Qur'an.
- One account per person; do not share your account or use the page with automated tools.
- There is a daily question allowance per person and a daily and monthly budget for the page; when the budget is used
  up the page takes no questions for that day or month.
- Do not put personal or sensitive information in your questions: they are sent to Anthropic to write the answer (see
  the privacy policy).
- The service, being in a trial phase, may be changed or closed without notice.
