# Birim bölümlemesi: İşârât'ın kuralı (b6)

D5.0 (4) (PLANLAR.md D5; kullanıcının kararı, 2026-11-19: önce İşârât'ın âyetleri neden birleştirip ayırdığı, sonra bütün
Kur'ân). Kaynak: Bakara 1–33'ün 32 geçişi ve her geçişte müellifin sözü (`data/d1/bolme/gecisler.md`, Opus okuması,
alıntılar programla denetlendi). Kuralı kullanıcı onaylar.

Sürümler: b1 (2026-11-19) ilk sürüm; b2 (2026-11-19) işlenebilirlik sınamasından sonra (`data/d1/bolme/sina.md`):
iki koşunun ikisi de 9|10'u (seriyi yeni üye sandı) ve 18|19'u (ikinci temsili ayrı birim sandı) ayırdı; 3. ve 4. alt
kural netleştirildi. b3 (2026-11-19): b2'nin üç koşusu da 6|7 ve 8|9'u birleştirdi (4. kuralın "netice ya da ceza"
eki fazla geniş); 1. kuralda dil bilgisindeki cezâ ile amele terettüp eden ukûbet ayrıldı («ترتّب العقاب على العمل»,
`B/7/mukaddime-2/c039`), 4. kuralda zümreyi tanıtan söz ile ilk fiil ayrıldı (`B/9-10-ayetlerin-tefsiri/c007`..`c009`). b4 (2026-11-19): b3'ün
üç koşusu da 14|15'i ukûbet sayıp ayırdı; aktarılan söze verilen karşılık («قابلَهم», `B/14-15-ayetlerin-tefsiri/c015`)
ile bir hâlin ardından gelen ukûbet ayrıldı. Kullanıcı b4'ü onayladı (2026-11-19). b5 (2026-11-19, kullanıcının kararı):
Bakara 34–286'da koşuların en çok ayrıldığı soru (51|52, 55|56, 63|64): «ثم» ile gelen âyet önceki üyenin devamıdır
(4. kurala eklendi; Bakara 1–33'te örneği yok). b6 (2026-11-20, kullanıcının Bakara 34–286 incelemesi: 20 geçişin
19'unda koşuların çoğunluğuyla aynı; ayrıldığı tek yer 73|74): 5. kural genişledi: uzun ve kendi başına çok nükte
taşıyan, yeni bir misal getiren âyet ayrı birimdir (74: kalplerin taşa benzetilmesi; "72–74 tek başına incelendiğinde
74'ün içindeki kendine has nükteler kaçırılabilir").

İki parça: **Kural** (genel; işlenebilirlik sınamasında modele yalnız bu gider, Bakara 1–33'ün bölmesini anmaz) ve
**Dayanak** (kimlikli örnekler; yalnız bizim için). `scripts/d1-bolme.py` Kural'ı `---- KURAL ----` ile
`---- DAYANAK ----` arasından okur.

---- KURAL ----

## Birim nedir

Birim, nazmı birlikte tahlil edilen âyet ya da âyetlerdir. Tahlilde iki ayrı bağ vardır: birimin öncesiyle bağı
("nazm-ı mecmû' bi-mâkablihi", birinci vecih) ve birimin içindeki cümlelerin birbiriyle bağı ("nazm-ı cümel", ikinci
vecih). İki âyet arasındaki bağ ikinci türdense aynı birimdedir, birinci türdense aralarında sınır vardır.

## Asıl ölçüt: bağın seviyesi

Müellif atfı üç seviyede ayırır: müfred müfrede hükümde ortaklık için, cümle cümleye **maksatta birlik** için, kıssa
kıssaya **garazda münasebet** için atfedilir. Ve "atfın güzelliği münasebetin güzelliğine, münasebetin güzelliği
sevkedilen garazın farkına bakar."

- İki âyet **tek bir maksadın parçaları** ise (ikincisi birincinin cümlesini tamamlıyor, ona cevap veriyor, onu
  açıklıyor, onun sahnesini sürdürüyor), bağ cümle seviyesindedir: **aynı birim**.
- İki âyet **ayrı maksatlar taşıyor ve aralarında yalnız garazda münasebet varsa** (aynı konunun bir sonraki adımı,
  terhibden sonra tergib, bir kısımdan öbür kısma geçiş, bir delilden sonraki delil), bağ kıssa seviyesindedir:
  **sınır**.
- Atıf harfinin varlığı ya da yokluğu tek başına belirleyici değildir; dil bilgisi bağımlılığı (sıfat, ism-i mevsûl,
  şart) çoğu zaman cümle seviyesine işaret eder ama aşağıdaki 2. kural onu sınırlar.

## Alt kurallar

1. **Cevap, red, cezâ birleştirir.** İkinci âyet birincideki açık bir söze verilen red ya da karşılıksa, bir şartın
   cezâsıysa (dil bilgisindeki şart ve cevabı), kıssa içinde karşılıklı konuşmanın devamıysa (dedi, dediler) aynı
   birimdir. **Aktarılan bir söze verilen karşılık** (onların "dediler"ine Allah'ın mukabelesi, çoğu zaman aynı
   lafızla: istihzaya istihza) da aynı birimdir. Buna karşılık bir hâlin ya da amelin **anlatımından** sonra ayrı
   âyette gelen **ukûbet** (amele terettüp eden ceza: "onlar iman etmez; Allah da kalplerini mühürledi") cevap değildir,
   amelden ukûbete geçiştir: **sınırdır**. Dinleyicinin zihnindeki
   takdirî bir soruya cevap ise ve bu cevap **yeni bir mevzu açıyorsa** (bir maksattan öbürüne geçiş) sınırdır;
   cevap aynı sahnenin içinde doğuyorsa birlikte kalır.
2. **Sıfat ve ism-i mevsûl ancak mevsûfunu açıklıyorsa birleştirir.** Sıfat mevsûfun ne olduğunu şerh ve keşf ediyor ya
   da emrin delilini veriyor ve aynı garaza hizmet ediyorsa aynı birimdir. Sıfat yeni bir maksat açıyorsa (övgüyü yeni
   bir özneye aktarıyor, umumdan sonra husus getirip başlı başına bir iman esasına yöneliyor) dil bilgisi bağına rağmen
   ayrı birimdir.
3. **Temsil ve kıssa sahnesi bölünmez.** Bir temsil ve bir kıssanın tek sahnesi tek birimdir. Aynı hâl için ikinci bir
   temsil getirilmişse (ör. "ya da" ile: aynı kimselerin aynı hâlinin ikinci tasviri) o da **aynı birimdedir**:
   ikincisi birincinin tekmilesidir; birim içinde iki temsil ayrı ayrı tahlil edilebilir, ama birim bir. Hakikatten temsile, temsilden hakikate, bir kıssadan öbür kıssaya, bir sahneden öbürüne
   geçiş sınırdır.
4. **Sayılan bir serinin her üyesi ayrı birimdir.** Âyetler bir üst garazın altında bir seri sayıyorsa (insanların
   kısımları, bir zümrenin cinayetleri, nimetler, deliller) her üye ayrı birimdir; bir üye birden çok âyete
   yayılabilir (o zaman o âyetler birlikte). **Yeni üye yeni bir fiil getirir;** aynı fiilin kalpteki iç sebebini
   (fiilin kaynağı olan hâl) bildiren âyet yeni üye değildir, o üyenin devamıdır. Bir zümreyi sözüyle ya da
   iddiasıyla **tanıtan** âyet serinin başıdır; o sözün altındaki ilk fiil (ne yaptıkları) yeni üyedir. **«ثم» ile
   başlayan âyet** (sonra affettik, sonra dirilttik, sonra yüz çevirdiniz…) önceki üyenin devamıdır, yeni üye değildir.
5. **Büyük mesele ayırır.** Tek garazın parçası olsa da kendi başına büyük bir ilmî ya da kelâmî mesele taşıyan
   âyet (uzun bir tahkik isteyen) ayrı birim olabilir. Uzun ve kendi başına çok nükte taşıyan, özellikle yeni bir
   misal ya da temsil getiren âyet de öyledir: önceki âyetlerle birleşirse kendi nükteleri kaçar. Bunu yalnız açık
   gerekçeyle uygula.
6. **Hurûf-u mukattaa** sûre başında ayrı tahlil edilir; ardından gelen âyet ayrı birimdir.

## Notlar

- "Mâkabl" her zaman bir önceki âyet değildir: bir birim birkaç âyet öncesine bağlanabilir (bir itiraza cevap,
  önceki temsillere bağlanır). Bu sınırı değiştirmez, birinci vecihte söylenir.
- Âyet uzunluğu ölçüt değildir; tek âyet de birim olur, kısa âyetler de birleşebilir.

---- DAYANAK ----

`B` = `isaratul-icaz-arabi/sure-i-bakara`.

## Asıl ölçüt

- Üç seviye: «كما يُعطَف المفردُ على المفردِ للاشتراك في الحُكم، والجملةُ على الجملةِ للاتحاد في المقصِد؛ كذلك قد تُعطَف
  القصةُ على القصة للتناسب في الغَرَض» (`B/8/c001`).
- «حُسن العطف ينظر إلى حُسن المناسبة، وحُسن المناسبة يختلف باختلاف الغرض المَسوق له الكلامُ» (`B/6/c013`); «ولما
  اختلف الغرضُ هنا وهنالك، لم يُستحسن العطفُ هنا» (`B/6/c014`): 5|6 sınır.
- Atıf belirleyici değil: 5|6 atıfsız ve sınır, 24|25 atıflı (وبشّر) ve sınır, 9|10 atıfsız ve birlikte.

## Bakara 1–33'ün geçişleri

| Kural | Birlikte | Sınır |
|---|---|---|
| 1 cevap, red, cezâ | 11–12 (red, «المعالجة» `B/11-12-ayetlerin-tefsiri/c011`), 14–15 (karşılık, `B/14-15-ayetlerin-tefsiri/c015`), 23–24 (şart ve cezâ, `B/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-07/c083`), 31–33 (مقاولة, `B/31-33-ayetlerin-tefsiri/mukaddime/c033`), 19\|20 (sahne içinde takdirî soru, `B/17-20-ayetlerin-tefsiri/mesele-10/c179`) | 4\|5 (istînaf, takdirî sorular, `B/5/c005`), 22\|23 (ibadetten nübüvvete, `B/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-07/c062`) |
| 2 sıfat ve mevsûl | 21–22 (delil, `B/21-22-ayetlerin-tefsiri/mukaddime/c142`, `c150`), 26–27 («شرحٌ وكشفٌ للفسق», `B/26-27-ayetlerin-tefsiri/c100`) | 2\|3 (Kur'ân'ın medhinden mü'minlerin medhine «انصباب», `B/3/c001`), 3\|4 («التخصيص بعد التعميم», `B/4/c006`) |
| 3 temsil ve kıssa | 17–20 (temsil ve tekrarı «كالتكملة والتتمة», `B/17-20-ayetlerin-tefsiri/mesele-10/c152`; İşârât içinde 17–18, 19–20 ayrı üç vecihle), 31–33 | 16\|17 (hakikatten temsile, `B/17-20-ayetlerin-tefsiri/mesele-10/c023`), 20\|21, 7\|8 (kıssadan kıssaya, `B/8/c001`) |
| 4 seri | 9–10 (ilk cinayetin cümleleri, `B/9-10-ayetlerin-tefsiri/c011`; 10 «أردفه … لترذيلهم بانفساد الجوهر», `B/9-10-ayetlerin-tefsiri/c032`) | 8\|9, 10\|11, 12\|13, 13\|14 (dört cinayet, `B/9-10-ayetlerin-tefsiri/c009`), 5\|6, 7\|8 (insanların kısımları), 27\|28, 28\|29 (nimetler, `B/28/c002`, `B/29/c003`) |
| 1 (ukûbet, b3) | | 6\|7: «ربطَ ختم ب لا يؤمنون … نظيرُ ترتّب العقابِ على العمل» (`B/7/mukaddime-2/c039`) |
| 5 büyük mesele | | 6\|7 ayrıca: müellif iki âyeti tek garaz sayar (`B/6/c083`), 7'nin önünde cebir ve ihtiyar mukaddimesi (`B/7/mukaddime/c001`); tahmin |
| 6 hurûf | | 1\|2 (`B/2/mukaddime/c031`) |
| Öbür sınırlar | | 15\|16 (icmal, «فذلكة», `B/16/c001`), 24\|25 (terhibden tergibe, `B/25/c008`), 25\|26 (itiraza cevap; mâkabli 17–20 ve 23–24, `B/26-27-ayetlerin-tefsiri/c004`) |

29\|30 ve 30\|31 yalnız tablodan (30 D5.0'ın kabul birimi, metni okunmadı).

## Bilinen sınırlar

- 32 geçiş, hepsi Bakara'nın başı (iman, nifak, temsil, kıssanın başı). Ahkâm, uzun kıssalar ve kısa sûreler için
  İşârât'ta örnek yok; oralarda kural bir uzatmadır.
- Fâtiha âyetlere değil lafızlara bölünür (15 birim); bu kural Fâtiha'yı açıklamaz.
- 5. kural tek örnekten (6|7); ölçüt "tahmin".
