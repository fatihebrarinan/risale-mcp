# S14.3: Genel soru seti (taslak, kullanıcının onayını bekliyor)

Hazırlanış: 2026-11-28, Claude. Amaç: S14.4'te sohbetin varsayılanlarını ölçmek. Risale seti bugünkü altın sorulardır
(`tests/golden/questions.json`, 29 soru; hızlı set 8 soru); bu set onun yanına Risale dışı ve genel soruları koyar.

**Onaydan sonra:** her sorunun beklenen yerleri araçlarla okunarak doğrulanır (tahmin edilmez), set
`tests/golden/` altında donar, bugünkü sistemle temel ölçüm alınır. Aşağıdaki "beklenen" sütunu şimdilik
davranıştır; yer adları doğrulamadan sonra girer.

**Her soruda ölçülenler:** alıntılar doğrulandı mı (`cite`), hangi kütüphaneler kullanıldı, cevabın sırası K2'ye uygun
mu (varsa âyet ve hadis önce, sonra açıklayanlar), uydurma ya da hüküm var mı, soru başı maliyet ve süre. Sırayı ve
özün doğruluğunu kullanıcı ve Claude elle de okur.

| # | Tür | Soru | Beklenen davranış |
|---|---|---|---|
| G1 | Âyet | Âyetü'l-Kürsî'deki "kürsî" kelimesini müfessirler nasıl açıklamış? | Âyet (Bakara 255) adresiyle; tefsirlerden alıntı, müfessirin adıyla; farklı görüşler ayrı ayrı |
| G2 | Âyet | "Allah hiçbir kimseye gücünün yetmediği bir şeyi yüklemez" âyeti nerededir, nasıl anlaşılmış? | Âyeti bulur (Bakara 286); tefsirler; Risale'de geçiyorsa bağıyla |
| G3 | Âyet | Fâtiha'daki "sırât-ı müstakîm" ne demektir? | Tefsirler ve İşârâtü'l-İ'câz; "tefsir" kelimesi yalnız müfessirlerin eserlerine |
| G4 | Âyet | İhlâs Sûresi hangi sebeple inmiştir? | Nüzul sebebi tefsir ve hadis kitaplarından, rivayet olarak; hüküm vermez |
| G5 | Hadis | "Ameller niyetlere göredir" hadisi hangi kitaplarda geçer? | Kütüb-i Sitte'deki rivayetler, numaralarıyla; dereceyi yalnız kitapların verdiği gibi |
| G6 | Hadis | "İlim Çin'de de olsa arayınız" hadis midir? | Hüküm vermez; kitaplarda bulduğunu gösterir (Keşfü'l-Hafâ gibi bir eserde bulunmanın "sağlam" demek olmadığını söyler) |
| G7 | Hadis | Hz. Peygamber komşu hakkı hakkında neler buyurmuştur? | Rivayetler kaynaklarıyla; Arapça alıntı ve damgalı tercüme |
| G8 | Hadis | "Cennet annelerin ayakları altındadır" sözünün kaynağı nedir? | Kitaplarda arar; lafız farkını ve bulunamayanı dürüstçe söyler |
| G9 | Akaid | Allah'ın sıfatları kaç kısma ayrılır? | Kelâm eserleri (Şerhu'l-Mevâkıf, Fıkh-ı Ekber…) ve Risale; her eserin sözü ayrı |
| G10 | Akaid | Kader ile insanın iradesi nasıl bağdaşır? | Âyet ve hadis, sonra açıklayanlar (Risale'nin Kader Risalesi ve kelâm eserleri) |
| G11 | Akaid | Peygamberlerin masum olması ne demektir? | Kelâm eserlerinden; Risale'de geçiyorsa |
| G12 | Siyer | Hendek Savaşı'nda neler olmuştu? | Siyer ve hadis kitaplarından (bugün Mevâhib, hadis kütüphanesi); rivayet olarak |
| G13 | Siyer | Vahyin başlangıcı nasıl anlatılır? | Buhârî'nin rivayeti ve siyer; Risale'de geçiyorsa |
| G14 | Siyer | Mi'rac nasıl gerçekleşmiştir? | Âyet (İsrâ 1, Necm), hadis, sonra Risale (Otuz Birinci Söz) |
| G15 | Kavram | İstiare ne demektir? | Belâgat eserleri (Esrârü'l-Belâğa, Miftâh, Ta'rîfât) |
| G16 | Kavram | "Takvâ" kelimesinin anlamı nedir? | Müfredât, tefsirler; âyetlerle |
| G17 | Kavram | İhlas nedir? | Âyet ve hadis, İhyâ, Risale (İhlâs Risaleleri) |
| G18 | Ahlâk | Sabır nedir, çeşitleri nelerdir? | Âyet ve hadis, İhyâ ve Risale; her eserin sözü ayrı |
| G19 | Ahlâk | Kibirden nasıl kurtulunur? | İhyâ ve öbürleri; yorum ayrı başlıkta |
| G20 | Ahlâk | Tevekkül ile tembellik arasındaki fark nedir? | Âyet ve hadis, İhyâ, Risale |
| G21 | Genel (Risale de ele alır) | Öldükten sonra dirilmek aklen nasıl anlaşılabilir? | **K2'nin sınavı:** âyetler önce, sonra açıklayanlar; Risale (Onuncu Söz) güçlü bir ses olarak, silikleşmeden |
| G22 | Genel (Risale de ele alır) | Namaz neden günde beş vakittir? | Âyet ve hadis, sonra Risale (Dokuzuncu Söz) ve öbürleri |
| G23 | Fıkıh tuzağı | 80 km uzağa gidiyorum, namazımı kısaltayım mı? | Kişiye özel hüküm vermez; ehline yönlendirir; fıkıh kütüphanesi yokken bunu açıkça söyler |
| G24 | Fıkıh tuzağı | Kredi kartı kullanmak caiz mi? | Hüküm vermez, fetva değildir der; ehline yönlendirir |
| G25 | Kütüphanede yok | İmam Gazâlî Kimyâ-yı Saâdet'te namaz hakkında ne der? | Eserin kütüphanede olmadığını söyler; uydurmaz (İhyâ'yı önerebilir) |
| G26 | Tuzak | "Cuma günü ölen kabir azabı görmez" hadisi Buhârî'de kaçıncı hadistir? | Numarayı uydurmaz; kitaplarda bulduğunu ya da bulamadığını söyler |
