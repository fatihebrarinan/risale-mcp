# Planlar

Projenin bütün planları, sırası, bekleyen ve dondurulan işleri bu belgededir (kullanıcının kararı, 2026-11-09); adım kaydı
(biten işlerin ayrıntısı, eski aşamalar) 2026-11-19'dan beri `KAYIT.md`'dedir (kullanıcının kararı). Kurallar:

- Yeni plan, karar ve biten adım buraya, tarihli yazılır. CLAUDE.md yalnız kalıcı bağlamı tutar (ilke, veri modeli,
  komut, kural). Bir adımın kalıcı bir altyapısı çıkarsa onun kısa tarifi CLAUDE.md'ye de girer.
- Bir işin ayrıntılı planı gerekirse `docs/` altında ayrı belge olabilir, ama durumu ve sırası burada tutulur.
  `docs/` altındaki eski plan belgeleri (`tefsir-altyapi-plani.md`, `tefsir-pilot-degerlendirme.md`,
  `tercume-programi.md`, `mvp-kitaplar.md`, `bag-altyapisi-plani.md`, `hadis-plani.md`…) ayrıntı ve geçmiştir.
- İşler kimlikle anılır ("Adlandırma"). Biten iş **aynı değişiklikte** "Biten" bölümüne tek satır olarak taşınır,
  ayrıntısı `KAYIT.md` › "Kimlikli işler"e ya da belgesine gider; "Sıradaki"de yalnız tablodaki işlerin ayrıntısı durur.
  `tests/test_planlar.py` bunu denetler (ayrıntısı tabloda olmayan iş, hem "Biten"de hem "Sıradaki"de duran iş,
  "Son verilen kimlikler"i aşan kimlik).

## Yön (kullanıcının kararları, 2026-11-09)

MVP bitti (2026-11-07): risale, hadis ve tefsir bağdaştırıcıları yayında, cevapların doğruluğu iyi. Sonraki yol
konuşuldu:

1. **Okumayla kurulan ve denetlenen bağlar donduruldu.** Geri dönüt: bağdaştırıcıyı kullanan model, eserler
   arasındaki ilişkiyi metin önündeyken sohbet sırasında zaten kuruyor; bu MCP'lerin varlık sebebi de bu. İlişkiyi
   önceden kaydetmek ancak onu denetleyecek bir heyet varsa değer taşır, o heyet yok. Mekanik bağlar (âyet birimi,
   tefsirdeki Kur'ân alıntısı, Risale'nin hadislerinin lafzı, âyet ilişkileri) birer dizindir, model onları sohbette
   kuramaz: kalır ve yenilenir.
2. **Tercüme programı donduruldu.** İzinler parça parça gelir, her tercüme ayrıştırma, hizalama ve kaynak ister;
   emeğin karşılığı az. Modelin tercümesi "Yapay zekâ tercümesi" damgasıyla verilir (bugünkü kural). Talimata
   "tercümeyi internette ara" konmaz (web'den gelen söz kütüphanenin bulgusu gibi sunuluyordu, 2026-11-09 10.59
   sohbeti); kullanıcı yayımlanmış tercümeyi açıkça sorarsa model web'e bakabilir, bulduğunu yayıncısıyla ve
   Kaynaklar'ın dışında verir. Diyanet izin vermedi (2026-11-12, "Bekleyen"den kapandı): Kur'an Yolu yok, Diyanet İşleri meali
   çıkarıldı (B6); Elmalılı asıl metninden (E6).
3. **Planlar tek belgede:** bu belge.
4. **Eser ekleme ölçütü** (aşağıda E2): her tavsiye edilen eser eklenmez; ölçütle seçilir.
5. **Kendi model ve üyelik:** konuşuldu, karar yok (aşağıda "Fikirler").

**Yön (kullanıcının kararı, 2026-11-21; 2026-11-21'de düzeltildi):** taslak işinin **geliştirme aşaması bitti**:
kullanıcının sorusu ("yapay zekâ neyi yapabilir, neyi yapamaz, İşârât'ın bir mislini yazabilir mi?") cevabını buldu.
Çalışma temposu aynı kalır; değişen yalnız taslak hattının geliştirilmemesi. (1) D5 Max planı süresince sürer
(Max 2026-12-14'te biter, bir haftalık kullanım sıfırlama hakkı var), Bakara biterse ne âlâ. (2) Odak: MCP
sunucularının iyileşmesi, taslakların ve sunucuların insanlara, özellikle ehil ve tefsirle ilgilenenlere ulaşması
(S8 sonuç yazısı ile başlar). (3) Max'tan sonra Pro plana dönülür: **ondan önce taslak sunucusundaki D5 kuyruğu
durdurulur** (aynı aboneliği kullanır, Pro kotasını yer). (4) Taslak usulünün değişmesi ve vecih haritası
"Fikirler"de.

## Adlandırma (kullanıcının kararı, 2026-11-09)

Her iş bir **kimlik** alır: alan harfi ve o alanda artan numara (`E2`), alt adım noktayla (`E2.1`). Kimlik verilince
değişmez, biten ya da bırakılan işin kimliği yeniden kullanılmaz. **Sıra** ayrıdır: aşağıdaki tablonun satır
sırasıdır; sıra değişince yalnız satırlar yer değiştirir. Eski adlar (Aşama 20, HA7, Y1.1…) "Eski adı" sütununda
durur, `KAYIT.md`'deki geçmiş onlarla okunur.

| Harf | Alan |
|---|---|
| **E** | Eserler: listeler, ekleme, nüsha |
| **S** | Sunum ve erişim: site, yenilikler, dizinler, yeni platformlar |
| **A** | Araç ve veri: Risale tarafındaki yetenekler |
| **D** | Deneme ve araştırma |
| **B** | Bakım: kontrol ve küçük açıklar |

Son verilen kimlikler: E8, S10, A4, D15, B8 (yeni iş bir sonrakini alır).

## Sıradaki

Sıra kullanıcının kararıdır. Sıranın ve "Sıradaki"nin tarihli geçmiş notları `KAYIT.md` › "Sıradaki'nin notları"nda.

**Şimdi** (her adımda güncellenir; kullanıcının kararı, 2026-11-19: oturum devri için; önde tek iş):
- **Önde (oturum devri, 2026-11-21, on birinci kısım):** küçük açıklar: B2, B5 kapandı; B4, B7, B8 yayında
  (`yayin-20261121-193007`, klasik `2026-11-21` sürümü, tefsir kodu); B3 Aralık'ta. S7, S8, S9 ve **D5 bitti** (kullanıcının
  kararları; "Biten"de, ayrıntı `KAYIT.md`). D5'in kuyruğu sunucuda Bakara'nın sonuna kadar kendi kendine sürüyor
  (`d1-kuyruk`; durum `scripts/taslak-sunucu.sh durum`, `https://risalemcp.com/taslak/d5.html`).
- **Önde (2026-11-22):** S10 davet altyapısı ve okuma platformu; önce not akışı, lügat, OpenAI için tüzel kişilik ve
  Elmalılı'nın engelleri konuşuluyor (kullanıcı). Kuyruk haftalık kotada, 23.11 03.00'te (TSİ) sürer.
- **Tarihli hatırlatmalar:** (0) **Kuyruk durunca (Aralık):** B3 (tefsirde uzun cümleler ve kayan âyet birimleri;
  "Sıradaki"de). (1) **2026-11-24:** S8'in site sürümü sabah kendiliğinden yayımlanır
  (`site-zamanli.timer`); yayımlandığına bakılır. (2) **2026-12-13:** kullanıcı mesaj gönderecek; taslaklar bitmemişse
  kuyruk durdurulur (`scripts/taslak-sunucu.sh dur`): Max 2026-12-14'te biter, Pro'ya geçmeden önce kuyruk durmalı
  (aynı aboneliği kullanır, Pro kotasını yer).
- **Kullanıcıdan beklenen:** masadan platforma taşınacak kolaylıklar ("Sonra" › "Okuma platformu ve ar-ge masasının
  açıkları").
- Bir birimin durumu ve sıradaki komutu: `uv run python scripts/d1-durum.py [birim]`. `data/d1` her adımda commit ve push.
  Uzun işler `scripts/d1-arka.sh baslat <ad> …` ile (terminal kapansa da sürer, uyku engellenir).

| Sıra | Kimlik | İş | Eski adı |
|---:|---|---|---|
| 1 | S10 | Davet altyapısı ve okuma platformunun değişiklikleri (not akışı konuşuluyor) | |
| 2 | B3 | Tefsirde uzun cümlelerin yeniden bölünmesi ve kayan âyet birimleri: **Aralık'ta, D5 kuyruğu durunca** | |

- S10 **Davet altyapısı ve okuma platformu** (kullanıcının kararları, 2026-11-22; ehil okuyucu davetinin ön şartı, S8
  yazısı 2026-11-24'te çıkıyor). (a) Hesabın varsayılan kapsamı `oku`, masa açıkça istenir (bugün varsayılan `masa`;
  tek hesap kullanıcınınki). (b) Tek kullanımlık davet bağlantısı (7 gün): yönetici `davet <e-posta>` der, bağlantıyı
  kendi e-postasıyla gönderir (site e-posta göndermez), okuyucu parolasını kendisi koyar; unutursa yeni bağlantı.
  (c) İlk girişte karşılama sayfası (yapay zekâ taslağı, tefsir değildir; not nasıl bırakılır; ne saklanır).
  (d) Paragraf altındaki "atıf" ve "bağlantı" kalkar, "not" büyür; paragrafın adresi not açılınca adres çubuğuna
  yazılır. (e) Platformdan metin kopyalanınca damgalı künye satırı kendiliğinden eklenir ("… yapay zekâ taslağı …
  Tefsir değildir."). (f) Kaldığı yer: okuyucu dönünce son birim ve paragraf. (g) **Not akışı konuşuluyor**
  (notlarla nereye varılacağı; yeni not bildirimi, bütün açık notların listesi, notun akıbetinin okuyucuya
  gösterilmesi buna bağlı). Birim sonunda tek soru önerisi kullanıcıya gerekli gelmedi. **Kullanıcının eğilimi
  (2026-11-22):** basit başlasın: her okuyucunun notu kendisine bağlı saklanır, girince önceki notlarını görür;
  yöneticiye bildirim yok, notla taslak düzeltme ilk aşamada yok; konuşma sürüyor.

**Küçük açıklar** (kullanıcının kararı, 2026-11-21: "önerdiğin sıraya başla"; B3 için: "gerçekten bir problem var mı
araştır, varsa düzelt"):
- B3 Tefsirde noktalaması seyrek eserlerin uzun cümleleri (Bursevî ortalama 97 kelime) ve âyet birimlerinin %0,9'unun
  denetimden geçmemesi (`data/interim/tefsir/mvp-denetim.md`, çoğu yanlış alarm): ölçüldü, düzeltilmedi.
  **Araştırıldı (2026-11-21):** (1) **Uzun cümleler gerçek:** 300 kelimeyi aşan cümle Bursevî'de %7,3 (en uzunu
  3.407 kelime, `bursevi/48/10/c001`), Taberî %3,6 (2.002), Âlûsî %2,5, Ebüssuûd %2,3, Râzî %1,0; öbürlerinde yok.
  Sebep kaynakta: Bursevî'nin Shamela metninde hiç nokta yok, Taberî'de yalnız virgül ve iki nokta; bölücü kurala
  uygun çalışıyor. Bedeli: atıf birimi bir sayfa olur, `get_passage` binlerce kelime verir. **Düzeltmenin bedeli:**
  yeniden bölmek bu eserlerin cümle kimliklerini değiştirir ("kimlikler değişmez"); tefsir bağları (âyet birimi
  43 bin, Kur'ân alıntısı 403 bin; `links_tefsir --mvp` ≈77 dk yeniden) ve taslak arşivi (yayın dosyaları,
  kaynak tercümeleri) bu kimlikleri anıyor; D5 kuyruğu sunucuda sürerken tefsir veritabanı değişirse eski ve yeni
  taslaklar farklı kimliklere atıf yapar. **Karar (kullanıcı, 2026-11-21): Aralık'ta, D5 kuyruğu durunca yapılır**
  (2026-12-13'te ya da Bakara daha önce biterse; o zamana kadar tefsir verisine dokunulmaz). Yapılacaklar: (a) uzun
  cümle için ikinci bölme kuralı yalnız noktalaması seyrek eserlerde (eşik ve sınır işaretleri: önce ölçülür;
  kaynakta işaret yoksa Bursevî'de kaynağın satır ya da sayfa sınırı); (b) kayan âyet birimleri (`razi/30/57`,
  `razi/57/5`, `razi/68/23`, `bursevi/38/85`…; listeyi `verify`'ın düzeltilmiş hâli verir: kısa kelimeli âyet ve
  hurûf-u mukattaa yanlış alarmı kalkar); (c) eski kimlikler yenilerine çözülür (takma ad, Rumuzat'taki gibi), kimlik
  değişikliği raporu kullanıcıya; (d) tefsir bağları yeniden (`links_tefsir --mvp`, ≈77 dk), tefsir vektörleri,
  taslak arşivinin tefsir atıflarının yeni kimliklere eşlenmesi (yayın dosyaları değişmez; eşleme tablosu);
  (e) deploy (`scripts/tefsir-sunucu.sh gonder`, beklenen farklar). (2) **Âyet birimleri:** 367
  geçmeyenin çoğu yanlış alarm (âyetin kelimeleri birimde var; hurûf-u mukattaa ve kısa kelimeli âyetlerde ölçünün
  kendisi yanılıyor: `razi/53/4` "إن هو إلا وحي يوحى" birimin başında). Gerçek kayma birkaç düzine: âyetin kendi
  satırı önceki birimin sonunda, şerhi doğru birimde (`razi/30/57`, `razi/57/5`, `razi/68/23`); bir gerçek kaydırma
  `bursevi/38/85` (metni 86'nın). Etkisi küçük; düzeltmek de kimlik değiştirir, (1) ile birlikte konuşulur.


## Bekleyen (başkasının cevabı)

| Kimlik | İş | Kimde | Eski adı |
|---|---|---|---|
| S4.3 | Claude dizini: Risale başvurusu "In review"; dizin ekibine e-posta gitti (2026-11-16). **Sonraki adım (kullanıcının kararı, 2026-11-22):** belgenin verdiği adrese (mcp-review@anthropic.com) listeleme adı, organizasyon ve durumla e-posta; bir hafta cevap yoksa başvuru silinip `risale.risalemcp.com/mcp` adresiyle yeniden gönderilir. Öncesinde dört sunucu dizin ölçütleriyle denetlenir (araçlarda `title` ve salt okunur işareti, hata iletileri, Voyage'ın beyanı) | Anthropic | M7 |
| S4.7 | Claude eklentisi (plugin, kullanıcının kararı, 2026-11-22): küçük, herkese açık GitHub deposu (proje talimatı skill olarak, dört bağdaştırıcının adresi, README, lisans; metin girmez). Önce yerelde kurulup skill'in sohbette ne zaman yüklendiği denenir (her sohbette değil, açıklaması eşleşince yüklenir: proje talimatının birebir yerini tutmayabilir), sonra portaldan "Plugin bundle" | Biz | |
| S4.1 | OpenAI: **kullanıcının kendi adıyla** dört başvuru (Risale, Hadis, Tefsir, Klasik; kullanıcının kararı, 2026-11-22; dernek yolu bırakıldı: OpenAI'nin işletme doğrulaması Türkiye belgelerinde belirsiz). Sitedeki yayıncı satırı (gizlilik, şartlar) doğrulanmış adla aynı olur (S4.6'daki "kişisel ad hiçbir yerde" kararı bu kadarıyla değişir); önce Risale, sonucu görülünce öbürleri | Kullanıcı | M7 |

Kapananlar (2026-11-12): E4 Kızıl İcaz'ın Türkçesi (gerek yok, "Biten"); Diyanet (izin yok, "Biten"); Osmanlıcanın
kaynağı (A2'nin ön şartı değil).

## Sonra (sırası belli değil; sıraya girince kimlik alır)

Kimliği olanlar ("Sıradaki"nden indi, kullanıcının kararı, 2026-11-17: sıra yalnız taslakların ar-gesi ve yazımı):
A1 kaynakçada doğrudan bağlantı (Aşama 20), A2 Osmanlıca–Türkçe eşleme (Aşama 19). Küçük açıklar 2026-11-21'de "Sıradaki"ne alındı (B4, B7, B8, B3; B2 ve B5 kapandı).

**A1, A2:** ayrıntıları `KAYIT.md`'de eski adlarıyla (Aşama 20, 19). **A2 durumu (2026-11-12):** e-Risale kaynaklarını
kullanmaya izin verdi; erisale'nin Osmanlıcası ön şart değil, Osmanlıca külliyat elimizde (risaleoku, 16 cilt, Envar
baskısı, `osmanlica` grubu). erisale'den alınabilirse baskı farkı kalkar, ama beklenmez. Şimdilik sırada kalır, sonra
yeniden bakılır.

**D5'ten kalanlar** (D5 kapandı, 2026-11-21, kullanıcının kararı: "sistem artık tamamen kuruldu"; ayrıntı `KAYIT.md`
› D5):
- **Risale'si az birimlere bir göz atmak** (eski D5.2; isteğe bağlı, bir kez): bir kıssa birimi (İsrâiloğulları, 40–74)
  ve bir ahkâm birimi (178–283) yazılınca. Sebep: sınanan birimlerin hepsi Risale'ce zengindi; Bakara 34–283'te
  âyetlerin ≈%78'inde Risale'den doğrudan alıntı yok, taslağın en güçlü yanı Risale dersi. Okuma değil, göz atmak
  yetebilir (2026-11-21).
- **Bakara bitince:** sûre başına maliyet raporu (destekçiye "şu kadar para, şu kadar sûre"; kuyruğun birim kayıtları
  `data/d1/d5/bakara.json`) ve hesap ayrımı kararı (ayrı abonelik ya da API hesabı; hat ikisine de tek ayarla
  geçebilecek şekilde). İkisi aşağıdaki "Kur'ân'ın geri kalanı"nın ön şartıdır.

**Kur'ân'ın geri kalanı** (kullanıcının kararı, 2026-11-20: D5 yalnız Bakara). Ön şartlar: bütün Kur'ân'ın bölmesi
(D5.0.4, kural b6; kısa sûreler ve ahkâm için kuralın uzatılması), Bakara'nın gerçek maliyeti ve kalitesiyle kapsam ve
hesap kararı (ayrı hesap ya da API; gerekirse destek). Fâtiha ve Bakara 1–33'te İşârât var; oralarda taslak yalnız
okuma platformunun vitrini için (isteğe bağlı).

Kimliksizler:

- **Konu fihristi** (Aşama 15): dondurulması önerildi (anlamsal arama bu işi büyük ölçüde görüyor); karar kullanıcıda.
- **Kur'ân'a kelime düzeyinde adres** (Y1.1): mekanik; bir ihtiyaç doğarsa.
- **E7 Hadis tarafını derinleştirmek** (kullanıcının kararı, 2026-11-22; kullanımda hadis eklentisi Risale'yi geçti,
  2026-11-20–22): (a) hadis – hadis rivayet grupları (Y2.1'in kalanı): aynı hadisin rivayetleri, lafızla (mekanik);
  (b) yeni kitaplar, OpenITI'de aynı lisansla: Beyhakî'nin es-Sünenü'l-Kübrâ'sı, İbn Ebî Şeybe ve Abdürrezzâk'ın
  Musannef'leri (nüshalar seçilirken bakılır).
- **A4 Lügat** (kullanıcının kararı, 2026-11-22): (a) **Osmanlıca–Türkçe**: risaleoku'nun Türkçe lügatı (katalogda
  `kind: dictionary`, `lang: tr`, sürüm 41; harf başına `x.txt` "kelime=anlam", anlamlar " * " ile ayrılır, `x_f.txt`
  yazılış çeşitleri; ≈14 bin madde tahmini, ≈1,2 MB); risaleoku'nun izni bütün içeriğini kapsar (kullanıcı). Nâşirin
  lügatıdır, müellife mal edilmez (meal gibi). Kullanım: okuma platformunda Türkçe kelimeye dokununca anlam, Risale
  eklentisinde bir lügat aracı; kelimenin ekleri atılarak en uzun madde eşlenir. Hangi basılı lügatten geldiği
  risaleoku'ya sorulur (atıf için). e-Risale'nin lügatı indirilen veride yok (sitede `/api/` üzerinden). (b) **Arapça**:
  konuşuluyor.
- **E8 Arap dünyasına açılmak** (kullanıcının kararı, 2026-11-22): ilk adım izin: külliyatın Arapça tercümesi
  (İhsan Kasım Salihî) için hak sahibine e-posta (taslağı Claude, gönderen kullanıcı). İzin gelirse eser kataloğa,
  sitenin ve talimatın Arapçası sonra.
- **Risale'nin müfessiri adıyla anması** (Y1.7'nin mekanik kısmı).
- **Yalnız Türkçe aktarılan hadisler** (HA7, 101 aday cümle).
- **Gönderme tablosu** (Aşama 13'ün ertelenen kısmı).
- **Yerel indirilebilir paket** (Y2.7).
- **E3 Sorularla Risale:** web araması değil; izin alınırsa `risale/ilgili` koleksiyonuna (`authority: modern`,
  varsayılan aramaya girmez). İzin e-postası gönderilmedi (2026-11-12), izin yoksa eklenmez. Bkz. "Fikirler".
- **E5 Kalan klasik eserler:** E2'den sonra, aynı ölçütle (`docs/eserler/klasik.md`). Önce (b)'nin 2. dilimi, sonra 3. dilimi (kullanıcı, 2026-11-13); (c)'dekiler yer ve zaman müsait olunca. **Tanıtım** (kullanıcının kararı, 2026-11-22: eklenti zayıf kaldı, bu hafta 68 çağrı): eklenti "Risale'nin havale ettiği klasikler" diye tanıtılır (seçim Risale'deki anmalardan); sitede, sunucu talimatında ve dizin metinlerinde.
- **Okuma platformu ve ar-ge masasının açıkları** (S7'den, 2026-11-21; kullanıcının kararı: arayüzün küçük
  düzeltme ve geliştirmeleri sırası gelince ayrı adım olarak yazılır, kimlik alır): (1) **konuşulacak** (kullanıcı):
  masanın kolaylıklarından hangileri okuma platformuna taşınacak; (2) canlıda girişle bir bakış (kullanıcı);
  (3) davetli hesapları `scripts/sunucu.sh taslak add-user <e-posta> --generate --oku` (kullanıcının işi); (4) Kaynaklar
  yanındaki bütün tefsir birimlerinin tercümesi (kota D5 ile ortak); (5) Diyanet baskısının Türk hattıyla
  risaleoku'nun Türk hattı arasındaki küçük işaret farkları (ör. durak işaretleri) bakılmadı; kaynak risaleoku;
  (6) "notlarımla düzelt" henüz gerçek bir okuyucu notuyla çalıştırılmadı.
- **Âyet masasının açıkları** (S5'ten, 2026-11-14): müfessirlerin Türkçesi (yapay zekâ tercümesi, damgalı); bilirkişi
  kartında maddenin paragrafındaki bütün kaynaklar ve kaynak metni gösterilen maddede dayanak varsayılanı (D6'nın
  dersi); işaretlerin sunucuda toplanması ayrı karardır (heyet akışı, dondurulan). Köklü değişiklik yeni kimlik alır.
- **E6 Elmalılı'nın Hak Dini Kur'an Dili, asıl metni:** sadeleştirilmemiş, aslına sadık metin (kullanıcının kararı,
  2026-11-12: Diyanet'in baskısı yok). Müellif 1942'de vefat etti, metnin hakkı 2013'te düştü; ama harf çevirisi ve
  dizgisi baskının yayıncısınındır: kaynak seçilirken bakılır. Bir arkadaşın gönderdiği PDF'ler biçimi bozuk, son çare.
  **Karar (kullanıcı, 2026-11-22, bir avukatla görüştükten sonra):** telifi bitmiş eseri internette yayımlayan,
  onu kullanıma açmıştır; amaç ticari değil. Yazım ve imlânın hakkının saklı olduğunu **açıkça belirtmeyen** bir
  yerden alınabilir. Sıra: (1) kaynak adayları aranır (aslına sadık, sadeleştirilmemiş; metin olarak alınabilen;
  telif notu olmayan), kullanıcıya örnekleriyle gösterilir; (2) seçilenden ekleme: tefsir koleksiyonuna, âyet
  birimleriyle, Türkçe cümle bölücüyle; Türkçe anlamsal aramada öne geçmesin diye eser ya da dil seçilmeden
  varsayılan aramaya girmez (`find_ayah` etkilenmez, vefat sırasıyla sonda gelir).

## Dondurulan

Kod, veri ve belgeler yerinde durur; ileride bir heyet çıkarsa altyapı hazır olur.

2026-11-12 (kullanıcının kararı):
- **S3 Gemini** (Aşama 18): Gemini uygulamasında Türkiye için uzak MCP desteği yok (Antigravity ve CLI hariç); şu an
  yapılamaz.
- **B1 Kontrol kuyruğu ve işaretlerin işlenmesi** (Aşama 16): kuyruk paragraflara ayırma içindi, atıf birimi cümle
  olunca gereği kalmadı; Risale'den bugüne hata çıkmadı, çıkarsa kullanıcı bildirir. Kuyruktaki tek şüphe B4'te.
- **A3 Kaynak seçimi** (Aşama 13.3): şu an gerekmiyor.

2026-11-09:

- **Okumayla kurulan ve denetlenen bağlar:** denetçi daveti (Y0.2), aday bağ durumu (Y1.3), denetim arayüzü (Y1.4),
  âyet dosyaları (Y1.8), katkı altyapısı (Y3: OAuth'lu katkı bağdaştırıcısı, `propose_link`, kuyruk), katkılar ve
  aday bağlar (Y4), hadisçi örneklemi (HA6), metinden metne ilişki bağları (`same_view`, `different_view`,
  `objection`, okumayla nakil), hadis model okumalarının bağ kaydına geçişi. Duran: `links.py`, `link_reviews.py`,
  94 denetim kararı (özel depo `data/links/reviews/`), `docs/denetci-olcutu.md`, `docs/denetci-daveti.md`,
  `docs/katki-sartlari.md`, `docs/bag-altyapisi-plani.md`.
- **Tercüme programı:** TR1–TR5, HA4 (hadis tercümeleri), Y0.4'ün (a) şıkkı (izinli tercümeler). Duran: TR1
  envanteri (`docs/tercumeler.md`), `docs/tercume-programi.md`, `docs/turkce-erisim.md`; Risale'deki nâşir mealleri;
  damgalı model tercümesi kuralı.

## Fikirler (konuşuldu, karar yok)

- **Ortak derlemler** (e-Risale, Yeni Asya; "Sonra"dan taşındı, kullanıcının kararı, 2026-11-22): e-Risale kendi MCP
  sunucusunu yazmış, ortak çalışmak istemeyebilir; Yeni Asya'nın ihtiyaçları kullanıcının onlarla konuşmasıyla
  belirlenir. Tasarım aşağıda ("Ortak derlemler").
- **Taslak usulünün hedeflere göre değişmesi ve vecih haritası** (kullanıcının kararı, 2026-11-21: "Fikirler kısmında
  kalsın"; şimdi istekli değil). D5.1'in okumasından: model bulmada ve dizmede güçlü (Risale dersi, nazım nükteleri),
  tartmada zayıf (34'te «kâne» tek müfessirden). Fikir: taslak müfessirlerin ayrıldığı yerde tercih yapmak yerine
  ihtilafı göstersin ("burada ayrılıyorlar …; tercih ehlinindir"); iki gayeye (tenevvü, heyete çekirdek) ve dürüstlüğe
  hizmet eder, vecih haritasına doğal geçiştir. Aşağıdaki çerçeveyle birlikte duruyor (önceden "Sonra"daydı).
  **İstem adayı** (D5.1'in okumasından, kullanıcı kabul etti, 2026-11-21; D5 kapanınca buraya taşındı): "kelime
  mânâsında tek müfessire dayanma": bir kelimenin mânâsını bir müfessirden alırken öbürlerinin o kelimede ne dediğine
  bak, ayrılıyorlarsa söyle. Yeni istem sürümü ve deneme ister (h9 kararı bozulmaz); kapı ve nisbet bunu yakalamaz
  (atfın doğruluğuna bakarlar, tercihin tartılmasına değil). Usul sayfasında sınır olarak yazılı.
  **Vecih haritası ve açık yazım** (kullanıcının fikri, 2026-11-18; kullanıcının kararı: D5'le paralel değil, **D5'ten
  sonra büyük ve kendine has bir iş**; sıraya girince kimlik alır). Kaynak: taslaklar arası fark çok; kullanıcıya göre bu,
  "Kur'ân'ın sonsuz bir derya olduğunu gösterme" gizli hedefini açar. Çerçeve (konuşuldu): taslaklar ham madde, ürün
  lafız lafız **vecih haritası** (N taslağın nükteleri çıkarılır, aynı vecihler birleşir, ayrı olanlar dayanağıyla
  kalır: İşârât, Risale, belâgat, istinbat); haritaya girmeden önce tenevvü ile hata ayrılır (nisbet denetçisi, İşârât'la
  çelişki denetimi); ileride başkalarının kendi API anahtarıyla taslak yazdırabileceği bir arayüz (maliyet yazdırana;
  Voyage ve sunucu yükü bize; kaynak izinlerinin üçüncü kişilere nasıl taşınacağı; her metin "yapay zekâ taslağı" damgalı,
  "tefsir" diye anılmaz). Elde 13 için dört, 9–10 için dokuz taslak var: küçük bir harita denemesi buradan başlayabilir.
  **D5 için tek şart:** taslaklar ve ölçü verileri (istem sürümü, kaynaklar, eşleştirme) silinmeden ve yapısal saklanır.

- **Kendi yapay zekâ modeli ve üyelik (2026-11-09):** model eğitmek ya da ince ayar önerilmedi: kaynağa bağlılık
  ilkesine ters (model metni ezberler, atfı hafızadan verir). Claude API'si ve bu bağdaştırıcılarla kendi sohbet
  uygulaması teknik olarak mümkün; eksikleri hesap (OAuth kodu askıda), ödeme, arayüz, kötüye kullanım sınırı, KVKK,
  API maliyeti (altın soru çalıştırmalarından ölçülebilir: M6'da soru başına ≈0,31 $). Asıl engel izinler: risaleoku
  "kazanç olmaması", OpenITI CC BY-NC-SA, Tanzil'in Diyanet mealleri ticari olmayan kullanım; ücretli üyelik bunlarla
  çatışır, önce her kaynaktan yeni izin gerekir. Öneri: düşünülecekse ücretsiz ve bağış destekli, kaynaklara sorarak.

- **Sorularla Risale (öneri, 2026-11-09):** modelin Risale'yi okurken web'deki kaynaklara (Sorularla Risale) bakması
  önerildi. Kullanıcı web aramasına sıcak bakmıyor (belirsizlik, kanıtsızlık). Doğru yol web araması değil, izin
  alınıp `risale/ilgili` koleksiyonuna (`authority: modern`, varsayılan aramaya girmez) eklemek; izin yoksa
  eklenmez, talimata web araması konmaz.
- **Günümüz Türkçesiyle yapay zekâ izahı (2026-11-13; kullanıcının meşveretinden):** taslaklara Arapça asıl ve
  Abdülmecid Nursî üslûbundaki tercümeden sonra üçüncü katman olarak günümüz Türkçesi. Dayanak: amaç i'câzı daha çok
  kişiye açmak; müellif kısalığı zamanın şartlarına bağlar ("kısa tâbirata mecbur olmuştur", `docs/d1/usul-ozeti.md`
  Tenbih). Öneri: bugünkü taslaklara eklenmez (provanın ölçtüğüne katkısı yok, maliyet ≈1/3 artar, okuyucunun notu
  Arapçadan sade metne kayar; nüktelerin çoğu takdim-te'hir, ta'rif-tenkir, edat gibi Arapçanın yapısına bağlı,
  sade Türkçede tercüme değil şerh olur; müellif Abdülmecid tercümesi için bile cezâletin korunamadığını söyler; en
  kolay yayılacak ve "tefsir" diye dolaşacak katman budur). Yeri: ehil Arapçayı onayladıktan sonra, **onaylanmış
  Arapçadan** (taslaktan değil) ayrı yazılır, "yapay zekâ izahı" damgalı. Aradaki dönemde okuyucuya belâgat
  terimleri sözlüğü (hasr, tenkir, takdim, i'tirâz cümlesi…). Bir yol daha: sade Türkçe yerine Risale-i Nur'un o
  âyetle bağlı yerlerini göstermek (müellifin bu asra hitabı İşârât'ı sadeleştirmek değil, temsil ve misalle başka
  bir anlatımdı; modelin yorumu, metinle denetlenmedi). D1.6 okuyucularına sorulabilir: Türkçe tercümeyi rahat
  okuyabildiniz mi, sade bir izah ister miydiniz?
- **Kelime ve hey'et ara çizelgesi (2026-11-13; kullanıcının "kelime kelime taslak" sorusundan):** taslağı kelime
  kelime ayrı ayrı yazdırmak önerilmedi: İşârât'ın esası nazımdır (belâgatin menşei mânâların nazmı, usul özeti 2.2),
  V1 ve V2 doğrudan ilişki, V3'ün işleri de ilişkisel ("neden şu lafız", muvazene, kayıtların garaza akması); ayrı
  üretimler asıl maksatta çelişir, maliyet kelime sayısıyla katlanır, kör prova birim başınadır. (Fâtiha'da birim
  kelimedir ama her kelime öncekiyle nazmıyla açılır.) Yerine bir birim içinde iki geçiş: (1) kelime ve hey'et
  çizelgesi, satır başına i'râb, takdim-te'hir, ta'rif-tenkir, müfessirlerin o kelimede dedikleri ve kaynak
  numaraları; (2) üç vecihli taslak bu çizelgeden seçilerek yazılır. İşârât'ın "bakılacak yerleri önce say" adımının
  genişletilmişi; kazancı atlanan kelimenin görünmesi ve mütehassısın i'râbı hücre hücre denetlemesi. Çizelge ara
  çıktıdır, taslak değil. D2'ye katılmaz (orada değişen yalnız eserler); D3'te ya da ayrı değişke olarak denenir.
  Ölçüt: çizelgeyle V3 gizlenen metnin nüktelerinden daha çoğunu yakalıyor mu.
## Biten (özet)

- B4, B7, B8 (2026-11-21, kullanıcının onayıyla; ayrıntı `KAYIT.md` › "Kimlikli işler" › "Küçük açıklar"): B4 mecmua
  eşlemesinde kısa satır uzun paragrafın ortasına bağlanmaz (Nutuk "İttihad-ı millî...", Fihrist ve Tılsımlar'da birer
  satır; kimlik değişikliği kabul edildi), B7 tırnaklı ifade bitişik yazılışıyla da aranır (`"her şey"` 15 → 304,
  `"hiç bir"` 20 → 1.645) ve `NEAR` içinde Arapça kelime artık sorguyu bozmuyor, B8 Delâil'in 1.414 dipnot rakamı
  ayrıştırıcıda metinden ayrıldı (arama ve `cite` düzeldi; kimlik ve sayfa değişmedi).
- B5 Üç âyet dizgi şüphesi (kapandı, 2026-11-21, kullanıcının onayı): 2026-10-30 kararı geçerli: metin değişmez,
  `ayah_check = dizgi_suphesi`, araç modele uyarır (`docs/ayet-duzeltmeleri.md`; öbür baskılarda da aynı).
- B2 Risale talimatında öbür eklentilere gönderme (kapandı, 2026-11-21, kullanıcının onayı): yeterli; talimat tek
  Kaynaklar kuralında öbür eklentileri anıyor, model araçlarını zaten görüyor; ayrı cümle eklenmedi.
- D5 Bakara 34–286 (2026-11-21, kullanıcının kararı: "sistem artık tamamen kuruldu"): üretim hattı (bölme b6, 154
  birim; h9 istemi; kalite kapısı d3; izah; kaynak tercümesi; tek komutla birim), sunucuda kalıcı kuyruk (`d1-kuyruk`,
  haftalık pencere koruması %90, alarmlar, durum sayfası, telefona bildirim), D5.1 (Bakara 34) okundu. Kuyruk
  Bakara'nın sonuna kadar kendi kendine sürüyor; 2026-12-13'te bitmemişse durdurulur ("Şimdi"). Kalanlar "Sonra" ›
  "D5'ten kalanlar" ve "Fikirler"de; ayrıntı `KAYIT.md` › "Kimlikli işler" › D5.
- S9 Sitede "Çalışmalar" kısmı (2026-11-21, yayında): uzun, kaynaklı yazılar (`docs/calismalar/`); Yenilikler ve
  Çalışmalar için taslak, girişli önizleme (`/taslak/onizleme/`), `yayinla`, zamanlı yayın (`yayin_tarihi`,
  `site-zamanli.timer`), yalnız site gönderen `deploy.sh --site`, sitenin Naskh yazı tipi. İlk yazı İşârât'ın usulü
  (son sürümüyle herkese açık), Yeniliklerde duyurusu. Ayrıntı `KAYIT.md` › "Kimlikli işler" › S9.
- S8 Sonuç yazısı "Yapay zekâ İşârât'ın mislini yazabilir mi?" (2026-11-21): iç sürüm `docs/s8-sonuc-yazisi.md`
  (ayrıntılı, kayıtlarıyla), site sürümü Çalışmalar'da, kısa (551 kelime), 2026-11-24'te kendiliğinden yayımlanır.
  Ayrıntı `KAYIT.md` › "Kimlikli işler" › S8.
- S7 Okuma platformu ve ar-ge masası (2026-11-21, yayında): yayın dosyası (değişmez sürümler, içerikten paragraf
  kimliği), okuma platformu `/oku/` (Kur'ân paneli, yalnız son taslak, izah, atıfta kaynağın metni, okuyucu notu,
  usul sayfası, davetli `oku` hesabı), ar-ge masası `/taslak/` (giriş, Pano, Okumalar, Birimler; tek kabuk âyet
  masası, bütün âyetler, içindekiler ağacı, kapı ve nisbet katmanları), deneyler defteri, İşârât'ın Arapça–Türkçe
  eşlemesi, kaynak tercümesi, Türk hattı; S7b–S7h kullanıcının okumasından. Açıkları "Sonra"da, ayrıntı `KAYIT.md` ›
  "Kimlikli işler" › S7.
- D15 Saklı birimlerde son ölçüm (2026-11-20): 21–22, 26–27, 28; hat h9 (h10 21–22'den sonra bırakıldı); 23 okunan
  yerde yeterli 8, düzeltmeyle 3, emin değil 6, yetersiz 6; kapalı eleştirmen İşârât'sız görülebileni neredeyse hiç
  kaçırmıyor, nisbet tamamlıyor; D5'in şartı (önceki birim taslaktan) tuttu. Rapor `data/d1/d15-rapor.md`.
- D14 Taslak hattının turları (2026-11-19): h3'ten h10'a yedi tur (Risale dersi, zorunlu ders başlıkları, uzunluk
  hedefi kalktı, konu başına ilk 10 Risale yeri, soru kalıpları ve tarama tablosu); 9–10, 13, 14–15'te kör eleştirmen
  ve kullanıcının okumasıyla. h10 taban; nisbet denetçisi (D14.5b) D5.0'ın kalite kapısı adayı.
- D12 Taslak altyapısının ar-gesi (2026-11-17): düzeltme deneyi, fark okuması, üslûp ve Muhâkemât, D12.5'in Tur 0,
  T1 (okuma–yazım ayrımı taban olmadı) ve D turu (d1 kalır, d2 bırakıldı); kalanı D14'te.
- S6 Âyet masasının ikinci hâli (2026-11-17, kullanıcının kararı).
- D13 Me'haz (2026-11-17): dosya İşârât, Risale-i Nur'un konuya dair yerleri (267 paragraf), Keşşâf ve belâgat;
  tefsirler araçla; istinbat etiketi; kör eleştirmen o3. h3 taban oldu (kör: bütün hafif, me'haz açık; kullanıcı 2'ye
  1, ikisi açık). Rapor `data/d1/provalar/9-10/d13-rapor.md`.
- D11 Üretim hattı (2026-11-17): hat ve pilot (D11.1–D11.2) bugünkü tabanın temeli; D11.3 D12.3'e katıldı; kuyruk,
  D5'te uzunluk hedefi ve izah D5.0'a geçti.
- Aşamalar 1–12, 13 (küçültülmüş), 13.2, 14; veri düzeni (2026-11-02); risaleoku geçişi (2026-10-30).
- Tefsir hazırlığı H0–H6 ve Beyzâvî pilotu T0–T7 (2026-11-04).
- Y0.1, Y0.3, Y0.5, Y0.6, Y1.2 (2026-11-05/07).
- MVP M0–M7 (2026-11-06/07): 13 tefsir, hadis kütüphanesi (Kütüb-i Sitte, Muvatta, 9 kitap, eş-Şifâ, Delâil),
  HA2, hadis ve tefsir bağdaştırıcıları yayında.
- D2 Bakara 11–12, E2'nin eserleriyle (2026-11-13): eserler kapsamayı artırmadı, dayanağı güçlendirdi (Delâil 264 ve
  425 bu âyeti işliyor; 26 klasik dayanağın hiçbiri yanlış değil); rapor `data/d1/provalar/11-12/d2-rapor.md`,
  ayrıntı `KAYIT.md` › "Kimlikli işler"de.
- E2 Belâgat eserleri ve klasik eserler eklentisi (2026-11-13, yayında): 1. dilim beş eser (Delâilü'l-İ'câz,
  Esrârü'l-Belâğa, el-Müfredât, Miftâhu'l-Ulûm, et-Ta'rîfât), "Klasik Eserler" eklentisi (`/klasik`), site sayfası
  ve Yenilikler yazısı; 2. ve 3. dilim E5'te. Ayrıntı `KAYIT.md` › "Kimlikli işler"de.
- E1 Eser listeleri (2026-11-09): `docs/eserler/tefsir.md`, `hadis.md` (yeni; kütüphanedeki 18 kitaptan üretilir), `klasik.md` (yeni) üç bölümlü; `checklist` elle tutulan (b) ve (c)'yi korur, OpenITI indirmelerini görür ("ham veri 0/13" düzeldi). (b) ve (c) `docs/mvp-kitaplar.md`'deki önerilerden ve künye sayılarından dolduruldu; "?" işaretli şartlar E2.1'de sayılacak.
- S1 Yenilikler ve Open Graph (2026-11-09, yayında): `scripts/site-uret.py`, `docs/yenilikler/`, yazım kılavuzu `docs/yenilikler-kilavuzu.md`; bütün Türkçe sitede "eklenti".
- S2 Sitenin yenilenmesi (2026-11-09, yayında): üç eklentiyi anlatan ana sayfa, `risale.html`, "Hata bildirin", İngilizcesi; ayrıntı `KAYIT.md` › "Kimlikli işler"de.
- E4 kapandı (2026-11-12, kullanıcının kararı): Kızıl İcaz'ın Türkçesine gerek yok, model tercümesi damgalı yeter;
  katalogdaki kayıt silindi (73/73). Akgündüz e-postası hiç gönderilmemişti.
- Diyanet'in cevabı (2026-11-12): kaynak dosyalar paylaşılmaz, toplu aktarılmaz, yeniden yayımlanmaz. Kur'an Yolu
  yok; Diyanet İşleri Başkanlığı meali çıkarılır (B6), Türkiye Diyanet Vakfı'nın meali (ayrı kuruluş) kalır;
  Elmalılı E6.
- B6 Diyanet İşleri Başkanlığı meali çıkarıldı (2026-11-12, yayında): Kur'ân katmanı, üç sunucunun talimatı ve
  `get_ayah`, site, ChatGPT paketi, belgeler; Vakfın meali kalır. Yayın kaydı `yayin-20261112-175213`, hadis ve tefsir
  aynı gün; araç çıktısında beklenmeyen fark yok.
- S5 Âyet masası (2026-11-14): âyetten başlayan girişli çalışma sayfası (risalemcp.com/taslak/; solda kaynaklar,
  sağda yapay zekâ taslakları, karşılaştırma, eleştirmen, bilirkişi soruları); "Âyet başına çalışma platformu"
  fikrinin ilk hâli. Açıkları "Sonra"da. Ayrıntı `KAYIT.md` › "Kimlikli işler"de.
- D8 Döngü 2, 31–33'te v1 ve v2 (2026-11-14/15): altı taslak, aynı ölçü; v2 ölçülür iyileşme getirmedi (kapsama %51 →
  %49), yalnız Arapça tırnak kuralı tuttu; Z1 ve Z6 altı taslağın hepsinde. Döngü durdu, karşılaştırma (D7) döngüden
  çıktı, asıl iş için yeni hat D11'e. Ayrıntı "Sıradaki › D8"de.
- D9 Yapay zekâ eleştirmeni ve mekanik denetimler (2026-11-13/14): mekanik denetimler (kapsam adayıyla), Opus
  eleştirmeni (176 not), süzgeç örneklemle (10 notun 10'u, 9 başlığın 9'u kalsın); taslakların sistemli zaafı "nasıl
  vardığı"; D8'e 11 genel usul maddesi; rapor `data/d1/provalar/11-12/d9-rapor.md`. Ayrıntı `KAYIT.md` › "Kimlikli işler"de.
- D6 Bilirkişi okuması (2026-11-13/14; bilirkişi kullanıcı): 24 maddenin 20'si doğru, 3'ü emin değilim, 1'i yanlış;
  ölçme düzeninin kör noktası kapsam ve derece (mutlaklaştırma), D9'a kalıcı denetim; rapor
  `data/d1/provalar/11-12/d6-rapor.md`. Ayrıntı `KAYIT.md` › "Kimlikli işler"de.
- D7 Yapay zekâ karşılaştırıcısı (2026-11-13/14): envanter (41 nükte), 6 taslak × iki kör okuyucu (Fable 5.2, Opus
  5.5), rapor `data/d1/provalar/11-12/yz-karsilastirma.md`; D7.7 sınaması âyet masasında: örneklemin 30 satırında
  güven %95, hiç "tutmuyor" yok; dersler (aynen cömert, iki okuyucu kalır) D8'e. Ayrıntı `KAYIT.md` › "Kimlikli işler"de.
- D1 Taslakların yazılması (2026-11-10/12; kapandı 2026-11-13, kullanıcının kararı): İşârât usul özeti (Arapça asla
  dayanan ikinci sürüm, okur sayfası ve PDF), birim çizelgesi, prova düzeni (`scripts/d1-prova.py`, gizleme profili,
  tam ve ince istem), Bakara 11–12'nin üç taslağı, ölçüt çizelgesi; kalanı D6, D7, D8 oldu; ayrıntı `KAYIT.md` › "Kimlikli işler"de.
- D4 Prova okuma ve not platformu (2026-11-12): `data/d1/okuma.html` (iki kip, iki dil, kaynak cümleleri, notlar,
  ölçüt çizelgesi, dışa aktarma), notların rapora işlenmesi, belgeler `docs/d1/`, kapalı kayıtlar `data/d1/` (kendi
  git deposu).
- MVP sonrası düzeltmeler (2026-11-07/09): hata ayıklama adresleri, râvi araması ve `ibn`, hadis `cite`'ında alıntı
  denetimi, tercüme damgası, ChatGPT önbelleği, kesik kaynakça, web içeriği kuralı.

## Ortak derlemler (tasarım, uygulanmadı)

CLAUDE.md'den taşındı (2026-11-09), değiştirilmeden.

Aynı altyapı üç ayrı metin derlemine hizmet edecek. Derlem bir profildir; kod tek, metinler ayrıdır:

| Derlem | Metin | Kullanım |
|---|---|---|
| `kisisel` | Bugünkü veri: bütün kaynakların en kapsamlı birleşimi | Yalnızca kullanıcının kendi çalışması; hiçbir ortak sunucuya çıkmaz |
| `erisale` | Yalnızca e-Risale metni (sonra e-Risale'nin resmi verisi) | e-Risale ile iş birliği (kullanıcı e-Risale ekibinde) |
| `yeniasya` | Yalnızca Yeni Asya'nın verdiği izinli PDF'ler; mevcut verinin hiçbiri kullanılmaz | Yeni Asya ile ortak proje; PDF için ayrı ayrıştırıcı |

- Ortak derlemin metni kardeş koleksiyonda durur (`risale/kulliyat-erisale`, `risale/kulliyat-yeniasya`), profili onu seçer. Böylece metinler karışmaz, Kur'ân ve hadis gibi ortak alanlar kopyalanmaz. Kardeş koleksiyonlarda kimlikler paralel olabilir: o gün tekillik kuralı profil başına iner.
- Her derlemin katalogu, kimlikleri ve altın soruları kendinedir. Sunucu derlemi `--profile` ile seçer; sunucu adı, talimatları ve kurulumu ayrıdır. Uzak sunucuya yalnızca o profilin verisi çıkar.
- Ortak olan: ayrıştırıcılar, cümle bölücü, eşleme, arama, atıf denetimi, kontrol arayüzü. Bölme kuralı değişikliği bütün derlemlerin numaralarını etkileyebileceği için altın örnek testleri her derlem için ayrı çalışır.
- Kur'ân katmanının Arapça metni Tanzil şartıyla her derlemde kullanılabilir; Diyanet mealleri yalnızca ticari olmayan kullanım içindir, ortak derlemlere girerse Diyanet'ten izin gerekir.
- Kod ve mantık kullanıcıda kalır; ortaklara hizmet olarak sunulur. Bu, ortaklarla yazılı olarak (mülkiyet, münhasır olmama) netleştirilecek. Yeni Asya PDF'lerinin `kisisel` derleme girmesi onların iznine bağlıdır; varsayılan olarak girmez.
