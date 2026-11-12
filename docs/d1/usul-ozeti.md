# İşârâtü'l-İ'câz'ın usulü: kendi metninden döküm (D1, ikinci sürüm)

> **Bu belge nedir.** İşârâtü'l-İ'câz'ın bir âyeti ele alırken ne yaptığının ve hangi sırayla yaptığının dökümüdür
> (`PLANLAR.md` D1). Tefsir değildir, "tefsir" diye anılmaz; bir yapay zekâ derlemesidir ve ehlinin tashihine kadar
> taslaktır. Her madde eserin kendi cümlesine dayanır: alıntılar veritabanındaki metinle birebir aynıdır
> (sonda "Denetim"), her alıntının altında adresi ve kimliği durur. Derleyenin kendi çıkarımı olan her yer
> **[Çıkarım]** diye işaretlidir.
>
> **İkinci sürümde ne değişti (2026-11-10).** Birinci sürüm Türkçe tercümenin taranmasına dayanıyordu. Bu sürüm
> Arapça aslın baştan sona okunmasına dayanır (`docs/d1/birim-cizelgesi.md`, `docs/d1/okuma-notlari.md`): dayanak
> Arapça cümledir, yanında Abdülmecid Nursî tercümesindeki karşılığı durur. Karşılığı tercümede olmayan yerde
> "Yapay zekâ tercümesi" damgasıyla derleyenin tercümesi verilir; bu tercüme alıntı değildir, eserin sözü yerine
> geçmez. Eklenenler: usulün nazarî temeli (2), mukaddimelerin ne zaman geldiği (5), taslak için kararlaştırılan
> kurallar (8).
>
> **Hangi metin.** Arapça asıl `isaratul-icaz-arabi` (risaleoku metni), Türkçe tercüme `isaratul-icaz` (e-Risale
> metni, Abdülmecid Nursî tercümesi). Tenbih ve Hâşiye'yi müellif sonradan Türkçe yazmıştır: onlarda asıl
> Türkçedir. İfâdetü'l-Merâm'ın ve tefsirin aslı Arapçadır. Tercüme asıldan üç noktada ayrılır: âyetlerin ardındaki
> "Yani: …" mealleri asılda yoktur; tercüme yer yer kısaltır (müellifin kendi sözü, 1.4); Bakara 17–20'nin nazarî
> girişi (Cürcânî'den nakil ve on iki mesele) tercümede hiç yoktur. Arapça asıl 31. âyetin ortasında biter,
> tercümede devamı vardır.
>
> **Kapsam.** Arapça asıl baştan sona okundu (3.264 cümle: Fâtiha, Bakara 1–33). Okuma bir yapay zekâ okumasıdır;
> Arapça belâgat inceliklerinde yanılmış olabilir. Sayılar kelime taramasıdır, yaklaşık okunmalıdır.

## 1. Eser kendini nasıl tanımlıyor

### 1.1 Maksadı: nazımdaki i'câzın işaretleri

> "أولاً: أنَّ مقصدنا من هذه «الإشارات» تفسيرُ جملةٍ من رموز نظْمِ القرآن؛ لأن الإعجازَ يتجلى من نظمه."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Fâtiha › 5. cümle (`isaratul-icaz-arabi/sure-i-fatiha/c005`)

Tercümede:

> "Evvelâ: Şu İşârâtü'l‑İ'câz adlı eserden maksadımız; Kur'ânın nazmına, lafzına ve ibaresine ait i'câz işâretlerini ve remizlerini beyân etmektir."

— İşaratü'l-İ'caz › Sûre‑i Fâtiha › 4. cümle (`isaratul-icaz/sure-i-fatiha/c004`)

> "وما الإعجازُ الزاهر إلّا نقشُ النظم."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Fâtiha › 6. cümle (`isaratul-icaz-arabi/sure-i-fatiha/c006`)

Tercümede:

> "Çünkü, i'câzın mühim bir vechi, nazmından tecellî eder ve en parlak i'câz Kur'ânın nazmındaki nakışlardan ibarettir."

— İşaratü'l-İ'caz › Sûre‑i Fâtiha › 5. cümle (`isaratul-icaz/sure-i-fatiha/c005`)

### 1.2 Sınırı: lafzın delâleti ve işârâtı

Müellifin sonradan Türkçe yazdığı Hâşiye'den (aslı Türkçedir):

> "Eski Said, bu tefsirde, Risale-i Nur gibi, zihinleri bulandırmamak için yalnız belâğat noktasında lafzın delâletine ve işârâtına ehemmiyet vermiş."

— İşaratü'l-İ'caz › Mukaddemât › Hâşiye › Birinci Nükte › 4. cümle (`isaratul-icaz/mukaddemat/hasiye/nukte-01/c004`)

> "Münâfıklar hakkındaki âyetleri izâh ile en ince nükteleri beyân etmiş; fakat mütâlaacıların zihnini bulandırmamak için mâhiyet-i mesleklerini ve istinâd noktalarını mücmel bırakmış, izâh etmemiş."

— İşaratü'l-İ'caz › Mukaddemât › Hâşiye › Birinci Nükte › 2. cümle (`isaratul-icaz/mukaddemat/hasiye/nukte-01/c002`)

### 1.3 Niyeti: tefsir değil, bir heyetin yapacağı tefsire me'haz

> "فمع احتياجها إلى التصحيح والإصلاح لا يرضى قلبي بتغييرها وتبديلها؛ إذ ظهرتْ في حالةٍ من خلوص النية لا توجد الآن، فأعرِضُها لأنظار أهل الكمال لا لأنه تفسير للتنزيل، بل ليصير -لو ظفر بالقبول- نوعَ مأخذٍ لبعض وجوه التفسير."

— İşârâtü'l-İ'câz (Arapça) › افادة المرام › 12. cümle (`isaratul-icaz-arabi/ifadetul-meram/c012`)

Tercümede:

> "Maahazâ, kaleme aldığım şu İşârâtü'l‑İ'câz adlı eserimi, hakîki bir tefsir niyetiyle yapmadım; ancak Ulemâ-i İslâmdan ehl-i tahkîkin takdirlerine mazhar olduğu takdirde; uzak bir istikbâlde yapılacak yüksek bir tefsire bir örnek ve bir me'haz olmak üzere o zamanların insanlarına bir yâdigâr maksadıyla yaptım."

— İşaratü'l-İ'caz › Mukaddemât › İfâdetü'l‑Merâm › 21. cümle (`isaratul-icaz/mukaddemat/ifadetul-meram/c021`)

Tefsirin kim tarafından yapılacağı:

> "فكما لابد لتنظيم الأحكام واطّرادها ورفعِ الفوضى -الناشئة من حرية الفكر مع إهمال الإجماع- من وجود هيئة عالية من العلماء المحققين الذين -بمظهريتهم لأمنية العموم واعتمادِ الجمهور- يتقلّدون كفالةً ضمنية للأُمة، فيصيرون مظهرَ سرِّ حجِّيةِ الإجماع الذي لا تصير نتيجةُ الاجتهاد شرعاً ودستوراً إلّا بتصديقه وسِكّته؛ كذلك لابد لكشف معاني القرآن وجمعِ المحاسن المتفرقة في التفاسير وتثبيت حقائقه -المتجلية بكشف الفن وتمخيض الزمان- من انتهاض هيئة عالية من العلماء المتخصصين، المختلفين في وجوه الاختصاص، ولهم مع دقةِ نظرٍ وُسْعةُ فكرٍ لتفسيره."

— İşârâtü'l-İ'câz (Arapça) › افادة المرام › 3. cümle (`isaratul-icaz-arabi/ifadetul-meram/c003`)

Tercümede:

> "Binâenaleyh, Kur'ânın ince mânâlarının ve tefsirlerde dağınık bir sûrette bulunan mehâsininin ve zamanın tecrübesiyle fennin keşfi sâyesinde tecellî eden hakikatlerinin tesbitiyle, herbiri birkaç fende mütehassıs olmak üzere muhakkìkîn‑i ulemâdan yüksek bir hey'etin tedkîkàtıyla, tahkîkatıyla bir tefsirin yapılması lâzımdır."

— İşaratü'l-İ'caz › Mukaddemât › İfâdetü'l‑Merâm › 7. cümle (`isaratul-icaz/mukaddemat/ifadetul-meram/c007`)

Müellifin sonradan yazdığı Tenbih'ten (aslı Türkçedir):

> "Belki inşâallâh, şu cüz'‑ü tefsir ve altmış altı aded, belki yüz otuz aded “Sözler” ve “Mektûbat” Risaleleriyle beraber me'haz olursa, ileride bahtiyar bir hey'et öyle bir tefsir-i Kur'ânî yazsın, inşâallâh…"

— İşaratü'l-İ'caz › Mukaddemât › Tenbih › 12. cümle (`isaratul-icaz/mukaddemat/tenbih/c012`)

### 1.4 Yazılış şartları: me'hazsiz, kısa, sünûhat; tercümenin kaydı

> "ثم إني بينما كنت منتظراً ومتوجهاً لهذا المقصد بتظاهر هيئة كذلك -وقد كان هذا غايةَ خيالي من زمان مديد- إذ سنح لقلبي من قبيل «الحس قبل الوقوع» تقرّبُ زلزلة عظيمة، فشرعتُ -مع عجزي وقصوري والإغلاق في كلامي- في تقييد ما سنَح لي من إشارات إعجاز القرآن في نظمه وبيان بعض حقائقه، ولم يتيسر لي مراجعة التفاسير."

— İşârâtü'l-İ'câz (Arapça) › افادة المرام › 8. cümle (`isaratul-icaz-arabi/ifadetul-meram/c008`)

Tercümede:

> "“Bir şey tamamıyla elde edilemediği takdirde o şeyi tamamıyla terketmek câiz değildir!” kaidesine binâen, acz ve kusurumla beraber; Kur'ânın bazı hakikatleriyle, nazmındaki i'câzına dair bazı işâretleri tek başıma kaydetmeye başladım."

— İşaratü'l-İ'caz › Mukaddemât › İfâdetü'l‑Merâm › 14. cümle (`isaratul-icaz/mukaddemat/ifadetul-meram/c014`)

> "O zamanlarda, o gibi yerlerde, müracaat edilecek tefsirlerin, kitapların bulunması mümkün olmadığından, yazdıklarım, yalnız sünûhât-ı kalbiyemden ibaret kaldı."

— İşaratü'l-İ'caz › Mukaddemât › İfâdetü'l‑Merâm › 17. cümle (`isaratul-icaz/mukaddemat/ifadetul-meram/c017`)

> "فإن وافقها فبِها ونِعْمَتْ، وإلّا فالعُهدةُ عليّ."

— İşârâtü'l-İ'câz (Arapça) › افادة المرام › 9. cümle (`isaratul-icaz-arabi/ifadetul-meram/c009`)

Tercümede:

> "Şu sünûhâtım eğer tefsirlere muvâfık ise, nurun alâ nur; şâyet muhâlif cihetleri varsa, benim kusurlarıma atfedilebilir."

— İşaratü'l-İ'caz › Mukaddemât › İfâdetü'l‑Merâm › 18. cümle (`isaratul-icaz/mukaddemat/ifadetul-meram/c018`)

Tenbih'ten ve Hâşiye'den (asılları Türkçedir): kısalığın sebebi, ölçüsü ve tercümenin kaydı.

> "Sâlisen: Eski Said, en dakîk ve en ince olan nazm‑ı Kur'ân’daki îcâzlı olan i'câzı beyân ettiği için, kısa tâbirata mecbur olmuştur."

— İşaratü'l-İ'caz › Mukaddemât › Tenbih › 6. cümle (`isaratul-icaz/mukaddemat/tenbih/c006`)

> "Yazıldığı vakit dâima şehîd olmaya hazırlandığı için, hàlis bir niyet ile ve belâğatın kanunlarına ve ulûm‑u Arabiye’nin desâtiriyle tatbik ettiği için hiçbirini cerhedemedim."

— İşaratü'l-İ'caz › Mukaddemât › Tenbih › 9. cümle (`isaratul-icaz/mukaddemat/tenbih/c009`)

> "Türkçeye tercümesi, Arapçadaki cezâlet, belâğat ve hàrika kıymetini muhâfaza edememiş, bazen de muhtasar gitmiş."

— İşaratü'l-İ'caz › Mukaddemât › Hâşiye › Üçüncü Nükte › 1. cümle (`isaratul-icaz/mukaddemat/hasiye/nukte-03/c001`)

## 2. Usulün nazarî temeli

Eser usulünün dayandığı belâgat esaslarını kendisi verir: Bakara 17–20'nin girişinde, temsîlî âyetler vesilesiyle.
Bu giriş Türkçe tercümede yoktur; aşağıdaki tercümeler derleyenindir.

### 2.1 İ'câzın esası nazmın belâgatidir; iki kısmı vardır

> "اعلم أن أساس إعجاز القرآن الكريم في بلاغة نظمه."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 17‑20. Âyetlerin Tefsiri › 1. cümle (`isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/c001`)

Yapay zekâ tercümesi: Bil ki Kur'ân-ı Kerîm'in i'câzının esası, nazmının belâgatindedir.

> "ومَعدِنُه الذي يتحصّل منه هو: توخّي المعاني النحوية الحرفية فيما بين الكَلِم، كإذابة الذهب بين أحجار فضة."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 17‑20. Âyetlerin Tefsiri › 6. cümle (`isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/c006`)

Yapay zekâ tercümesi: Bu kısmın elde edildiği maden, kelimeler arasındaki nahvî ve harfî mânâların gözetilmesidir; gümüş taşların arasında altın eritmek gibi.

> "هو كلباسٍ عالٍ وحُلَّة فاخرة قُدّت من أسلوبٍ على مقدار قامات المعاني، وخيطَت من قِطَعات خيطاً منتظماً فيُلبَس على قامة المعنى أو القصة أو الغرض دفعةً."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 17‑20. Âyetlerin Tefsiri › 9. cümle (`isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/c009`)

Yapay zekâ tercümesi: İkinci kısım, mânâların boyuna göre üslûptan biçilmiş, parçalarından düzgünce dikilmiş yüksek bir elbise, değerli bir hulle gibidir; mânânın, kıssanın ya da garazın boyuna bir defada giydirilir.

Birincisini fenn-i meânî, ikincisini fenn-i beyân üstlenir; ikincinin en mühim meselesi temsildir (`isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/c007`, `isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/c010`, `isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/c011`). Ardından müellif Abdülkāhir el-Cürcânî'den uzun bir nakil yapar (`isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/fasil/c001..c009`) ve on iki mesele sayar:

> "ثم إني استخرجتُ -فيما مضى من الزمان- من أُسِّ أساس البلاغة مقدِّمةً لبيان إعجاز القرآن ثنتَي عشرة مسألة."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 17‑20. Âyetlerin Tefsiri › فصل ومقدمة › 11. cümle (`isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/fasil-2/c011`)

Yapay zekâ tercümesi: Sonra ben, geçmiş zamanda, Kur'ân'ın i'câzını beyana mukaddime olmak üzere belâgatin temelinin temelinden on iki mesele çıkarmıştım.

### 2.2 Belâgatin menşei mânâların nazmıdır, lafzın değil

> "ونظمُ المعاني: عبارة عن توخّي المعاني النحوية فيما بين الكلمات أي إذابة المعاني الحَرفية بين الكَلِم لتحصيل النقوش الغريبة."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 17‑20. Âyetlerin Tefsiri › المسألة الأولى: › 2. cümle (`isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/mesele-01/c002`)

Yapay zekâ tercümesi: Nazm-ı meânî, kelimeler arasında nahvî mânâları gözetmekten, yani garip nakışlar elde etmek için harfî mânâları kelimelerin arasında eritmekten ibarettir.

> "فالكلام إذا حذا حذوَ الواقع، وطابق نظمُه نظامَه حازَ الجزالةَ بحذافيرها."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 17‑20. Âyetlerin Tefsiri › المسألة الأولى: › 13. cümle (`isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/mesele-01/c013`)

Yapay zekâ tercümesi: Söz vâkıanın izinden gider ve nazmı onun nizamına uyarsa cezâleti bütünüyle elde eder.

### 2.3 Mânâ tabakaları ve delâlet dereceleri

> "فمن شأن البليغ أن يفيدَ بصريح الكلام ما تعلّق به الغرضُ واقتضاه المقامُ وطلبَه المخاطَبُ."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 17‑20. Âyetlerin Tefsiri › المسألة السادسة: › 11. cümle (`isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/mesele-06/c011`)

Yapay zekâ tercümesi: Belîğ olanın şanı, garazın taalluk ettiğini, makamın gerektirdiğini ve muhatabın istediğini sözün sarihiyle ifade etmektir.

> "ثم يُحيل الطبقاتِ الأُخَر -بمقدار نسبة درجة القُرب من الغرض- على دلالة القيود، وإشارةِ الفحوى، ورمز الكيفيات، وتلويح مستَتبعات التراكيب، وتلميحِ الأساليب، وإيماءِ أطوار المتكلم."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 17‑20. Âyetlerin Tefsiri › المسألة السادسة: › 12. cümle (`isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/mesele-06/c012`)

Yapay zekâ tercümesi: Sonra öbür tabakaları, garaza yakınlık derecesi nisbetinde, kayıtların delâletine, fahvânın işaretine, keyfiyetlerin remzine, terkiplerin müstetbeâtının telvihine, üslûpların telmihine ve mütekellimin tavırlarının îmâsına havale eder.

Eserde bir nüktenin derecesi bu terimlerle söylenir. Arapça asılda geçtikleri cümle sayısı: إشارة 289, رمز 141, إيماء 100, تلويح 45, تصريح 20, تلميح 16. Mânâlar arasında ihtimamın paylaşımının şartı da aynı yerdedir: garaza hizmet nisbetinde (`isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/mesele-06/c015`).

### 2.4 Her kayıt mukadder bir suale cevaptır

> "اعلم أن سلامة الكلام التي هي سببُ صحته وقوّته هي أن يكون الكلام بحيث يشير إلى المبادئ والدلائل، ويرمز إلى اللوازم والتوابع، وبقيود الموضوع والمحمول وكيفياتهما يومئ إلى ردِّ الأوهام ودفع الشبهات؛ كأنّ كلَّ قيدٍ جوابٌ لسؤال مقدّر."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 17‑20. Âyetlerin Tefsiri › المسألة العاشرة: › 5. cümle (`isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/mesele-10/c005`)

Yapay zekâ tercümesi: Bil ki sözün sıhhat ve kuvvetinin sebebi olan selâmeti şudur: söz mebdelere ve delillere işaret etmeli, levâzım ve tevâbie remzetmeli, mevzu ile mahmulün kayıtları ve keyfiyetleriyle vehimlerin reddine ve şüphelerin def'ine îmâ etmelidir; sanki her kayıt mukadder bir suale cevaptır.

### 2.5 Hayal hakikat çekirdeğine dayanır

> "ولابد في كل خيال من نواةٍ من الحقيقة نظيرَ هذا المثال، ولابد في زجاجةِ كلِّ مجازٍ من سراج الحقيقة، وإلّا كانت بلاغتُه الخيالية خرافةً بلا عِرقٍ لا تفيد إلّا حيرةً."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 17‑20. Âyetlerin Tefsiri › المسألة الثانية: › 7. cümle (`isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/mesele-02/c007`)

Yapay zekâ tercümesi: Bu misalde olduğu gibi her hayalde hakikatten bir çekirdek, her mecazın camında hakikatin bir lambası bulunmalıdır; yoksa o hayalî belâgat, kökü olmayan ve hayretten başka bir şey vermeyen bir hurafe olur.

### 2.6 Dayanağı: Abdülkāhir el-Cürcânî'nin mezhebi

İ'câzın ifade edilip edilemeyeceği meselesinde:

> "ثم إن «السكاكي» اختار: أن الإعجاز ذوقيٌّ لا يعبّر عنه ولا يُشرح بل يُذاق ذوقاً."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri › المسألة السابعة: › 165. cümle (`isaratul-icaz-arabi/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-07/c165`)

Tercümede:

> "“İ'câz, zevkîdir; ta'rif ve tâbir edilemez.”"

— İşaratü'l-İ'caz › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri (Nübüvvet Hakkında) › İ'câzın Vecihleri › Üçüncü Vecih › 124. cümle (`isaratul-icaz/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/icazin-vecihleri/vecih-03-2/c124`)

> "وأما صاحب دلائل الإعجاز فاختار أنه يمكن التعبير عنه."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri › المسألة السابعة: › 166. cümle (`isaratul-icaz-arabi/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-07/c166`)

Tercümede:

> "Lâkin Abdülkahir’in iltizam ettiği veche göre, i'câzı ta'rif ve tâbir etmek mümkündür."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri (Nübüvvet Hakkında) › İ'câzın Vecihleri › Üçüncü Vecih › 126. cümle (`isaratul-icaz/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/icazin-vecihleri/vecih-03-2/c126`)

> "ونحن على مذهبه في هذا البيان."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri › المسألة السابعة: › 167. cümle (`isaratul-icaz-arabi/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-07/c167`)

Tercümede:

> "Biz de bu vechi kabûl ediyoruz."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri (Nübüvvet Hakkında) › İ'câzın Vecihleri › Üçüncü Vecih › 127. cümle (`isaratul-icaz/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/icazin-vecihleri/vecih-03-2/c127`)

Yani eserin bütünü, nazımdaki i'câzın tabir edilebileceği kabulüne dayanan bir tatbiktir.

## 3. İlkeler

### 3.1 Dört maksat

> "وثانياً: أنَّ المقاصد الأساسية من القرآن وعناصرَه الأصلية أربعةٌ: التوحيد، والنبوة، والحشر، والعدالة؛"

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Fâtiha › 7. cümle (`isaratul-icaz-arabi/sure-i-fatiha/c007`)

Tercümede:

> "Sâniyen: Kur'ân’daki anâsır‑ı esâsiye ve Kur'ânın takib ettiği maksadlar; Tevhid, Nübüvvet, Haşir, Adâlet ile İbâdet olmak üzere dörttür."

— İşaratü'l-İ'caz › Sûre‑i Fâtiha › 6. cümle (`isaratul-icaz/sure-i-fatiha/c006`)

> "فكما تتراءى هذه المقاصدُ الأربعة في كله، كذلك قد تتجلى في سورةٍ سورةٍ، بل قد يُلْمَح بها في كلامٍ كلامٍ، بل قد يُرْمَز إليها في كلمةٍ كلمةٍ؛ لأن كلَّ جزءٍ فجزءٍ كالمرآةِ لكلٍّ فكلٍّ متصاعداً، كما أن الكلَّ يتراءى في جزءٍ فجزءٍ متسلسلاً."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Fâtiha › 24. cümle (`isaratul-icaz-arabi/sure-i-fatiha/c024`)

Tercümede:

> "C – O anâsır‑ı erbaa, Kur'ânın hey'et-i mecmuasında bulunduğu gibi; Kur'ânın sûrelerinde, âyetlerinde, kelâmlarında, hattâ kelimelerinde bile sarâhaten veya işâreten veya remzen bulunmaktadır."

— İşaratü'l-İ'caz › Sûre‑i Fâtiha › 28. cümle (`isaratul-icaz/sure-i-fatiha/c028`)

> "Çünkü, Kur'ânın küllü, cüz'lerinde göründüğü gibi, cüz'leri de, Kur'ânın küllüne âyinedir."

— İşaratü'l-İ'caz › Sûre‑i Fâtiha › 29. cümle (`isaratul-icaz/sure-i-fatiha/c029`)

> "أعني المقاصد الأربعة المشهورة، مع أن في أكثر السور يكون المقصودُ بالذات واحداً منها، والباقي استطرادياً."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 17. cümle (`isaratul-icaz-arabi/sure-i-bakara/c017`)

Yapay zekâ tercümesi: Yani meşhur dört maksat; bununla beraber sûrelerin çoğunda bizzat maksut olan bunlardan biridir, kalanı istitrâdîdir.

Tercümede bu cümlenin serbest karşılığı: `isaratul-icaz/sure-i-bakara/kisim-01/c016`.

Uygulaması Besmele ve Hamd'de gösterilir (`isaratul-icaz-arabi/sure-i-fatiha/c026..c036`) ve okura bırakılır:

> "هذا مثالاً فانسج على منواله."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Fâtiha › 37. cümle (`isaratul-icaz-arabi/sure-i-fatiha/c037`)

Yapay zekâ tercümesi: Bu bir misaldir; sen de onun tarzında doku.

Bir âyetin asıl maksadının bu dörtten hangisi olduğu yeri gelince adıyla söylenir (4. bölümdeki çizelge: Bakara 4, 21–22, 23–24, 25, 28, 29, 30).

### 3.2 Havuz ilkesi: her kelime, kayıt ve hey'et asıl maksada hizmet eder

> "اعلم أن من أساس البلاغة الذي به يبرُق حُسن الكلام تجاوب الهيئات وتداعي القيود وتآخذها على المقصد الأصلي، وإمداد كلٍّ بقدْرِ الطاقة للمقصد، الذي هو كمجمَع الأودية أو الحوض المتشرب من الجوانب، بأن تكون مصداقاً وتمثالاً لما قيل:"

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 2. Âyetin Tefsiri › مقدمة › 1. cümle (`isaratul-icaz-arabi/sure-i-bakara/2/mukaddime/c001`)

Tercümede:

> "Kelâmların hüsnünü artıran ve güzelliğini fazlaca parlatan belâğatın esâslarından biri de şudur ki: Bir havuzu doldurmak için etrafından süzülen sular gibi, belîğ kelâmlarda da zikredilen kelimelerin, kayıtların, hey'etlerin tamamen o kelâmın takib ettiği esâs maksada nâzır olmakla onun takviyesine hizmet etmeleri, belâğat mezhebinde lâzımdır."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 2. Âyetin Tefsiri › 3. cümle (`isaratul-icaz/sure-i-bakara/2/c003`)

Uygulamada önce âyetin maksadı tek cümleyle konur, sonra her kayıt hem o maksada hem kendi deliline bağlanır:

> "وبالخاصة ﴿ الٓمٓ ❀ ذٰلِكَ الْكِتَابُ لَا رَيْبَ ف۪يهِ هُدًى لِلْمُتَّق۪ينَ ﴾ لأنَّ هذه الآية ذُكرت لمَدح القرآن وإثبات الكمال له."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 2. Âyetin Tefsiri › مقدمة › 7. cümle (`isaratul-icaz-arabi/sure-i-bakara/2/mukaddime/c007`)

Tercümede:

> "Bu âyette maksad-ı esâs “Kur'ânın yüksekliğini göstermek”tir."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 2. Âyetin Tefsiri › İkinci Misâl › 2. cümle (`isaratul-icaz/sure-i-bakara/2/misal-02/c002`)

> "فكلٌّ كما يُمد المقصدَ ويلقي إليه حصتَه يرمز ويشفّ من تحته عن ما يستند إليه من الدليل وإنْ دقّ."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 2. Âyetin Tefsiri › مقدمة › 9. cümle (`isaratul-icaz-arabi/sure-i-bakara/2/mukaddime/c009`)

Tercümede:

> "Evet bu kayıtlar, istinâd ettikleri pek ince ve gizli delillerine işâret etmekle beraber, o maksadın takviyesine koşuyorlar."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 2. Âyetin Tefsiri › İkinci Misâl › 4. cümle (`isaratul-icaz/sure-i-bakara/2/misal-02/c004`)

### 3.3 Saat milleri: âyet, cümle ve hey'et aynı maksadın etrafında döner

> "ولنشرع في نظم هيئات جملةٍ جملةٍ، فاعلم أن الآيات وجمَلَها وهيئاتِها كأميال الساعة التي تعدّ الثواني والدقائقَ والساعاتِ، فكلما يُثبت هذا شيئاً يؤيّده ذاك بدرجته ويمدّه ذلك بنسبته، وكذا إذا أراد هذا شيئاً عاوَنه ذاك وساعده الآخر بحيث يُخطِر الحالُ ما قيل:"

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 26‑27. Âyetlerin Tefsiri › 112. cümle (`isaratul-icaz-arabi/sure-i-bakara/26-27-ayetlerin-tefsiri/c112`)

Tercümede:

> "Evvelâ bunu bilmek lâzımdır ki, Kur'ân‑ı Kerîm’in âyetleri ve âyetlerin cümleleri ve cümlelerin hey'etleri; sâniye, dakika, saatleri sayan saatin milleri gibidirler."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 26‑27. Âyetlerin Tefsiri › 241. cümle (`isaratul-icaz/sure-i-bakara/26-27-ayetlerin-tefsiri/c241`)

> "Millerin her ikincisi birincisine yardım ettiği gibi, bir âyet bir maksadı takib ettiği zaman, cümleleri de o maksadın etrafında dolaşırlar; cümlelerin hey'etleri dahi, cümlelerin izini takib ediyorlar."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 26‑27. Âyetlerin Tefsiri › 242. cümle (`isaratul-icaz/sure-i-bakara/26-27-ayetlerin-tefsiri/c242`)

### 3.4 Nazım tek bir ipe dizili değildir

> "اعلم أن نظم دُرَر القرآن ليس بخيط واحد بل النظمُ -في كثيرٍ- نقوشٌ تحصل من نسج خطوطِ نِسَبٍ متفاوتةٍ قُرباً وبُعداً، ظهوراً وخفاء."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Fâtiha › صِرَاطَ الَّذِينَ اَنْعَمْتَ عَلَيْهِمْ › 1. cümle (`isaratul-icaz-arabi/sure-i-fatiha/siratallezine-enamte-aleyhim/c001`)

Tercümede:

> "Kur'ânın inci gibi lafızlarının dizilmesi; bir hayta, bir çeşide, bir nakşa münhasır değildir."

— İşaratü'l-İ'caz › Sûre‑i Fâtiha › Sırâtallezine En'amte Aleyhim «صِرَاطَ الَّذ۪ينَ اَنْعَمْتَ عَلَيْهِمْ» › 2. cümle (`isaratul-icaz/sure-i-fatiha/siratallezine-enamte-aleyhim/c002`)

> "Belki; zuhûrca, hafâca, yakınlıkça, uzaklıkça mütefâvit çok tenâsüblerden hâsıl olan pek çok nakışlar üzerine dizilmişlerdir, nazmedilmişlerdir."

— İşaratü'l-İ'caz › Sûre‑i Fâtiha › Sırâtallezine En'amte Aleyhim «صِرَاطَ الَّذ۪ينَ اَنْعَمْتَ عَلَيْهِمْ» › 3. cümle (`isaratul-icaz/sure-i-fatiha/siratallezine-enamte-aleyhim/c003`)

Bir lafzın yalnız bir öncekiyle değil, yakın ve uzak birçok lafızla bağı aranır; eser bunu aynı yerde dokuz bağ sayarak gösterir (`isaratul-icaz-arabi/sure-i-fatiha/siratallezine-enamte-aleyhim/c003..c010`).

### 3.5 Bir nüktenin kabul ölçüleri

Birden çok vechin murad olabilmesi ve şartı:

> "ولقد نظّم القرآن جُمَله ووضعها في مكان ينفتح من جهاته وجوه محتملة لمراعاة الأفهام المختلفة ليأخذ كلُّ فهمٍ حصته."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 2. Âyetin Tefsiri › مقدمة › 79. cümle (`isaratul-icaz-arabi/sure-i-bakara/2/mukaddime/c079`)

Tercümede:

> "Hülâsa: Kur'ân‑ı Mu'cizü'l-Beyân; âyetlerini, cümlelerini öyle bir şekilde nazmetmiş ve vaz'etmiştir ki, her cihetten ihtimal yolları bulunsun ki, muhtelif fehimler ve isti'dâdlar, zevklerine göre hisselerini alabilsinler."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 2. Âyetin Tefsiri › İkinci Misâl › 75. cümle (`isaratul-icaz/sure-i-bakara/2/misal-02/c075`)

> "فإذن يجوز أن يكون الوجوهُ بتمامها مرادةً بشرط أن لا تردّها علومُ العربية، وبشرط أن تستحسنها البلاغةُ، وبشرط أن يقبلها علم أصول مقاصد الشريعة."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 2. Âyetin Tefsiri › مقدمة › 81. cümle (`isaratul-icaz-arabi/sure-i-bakara/2/mukaddime/c081`)

Tercümede:

> "Binâenaleyh, ulûm-u Arabiye’nin kaidelerine muvâfık ve belâğatın prensiplerine uygun ve ilm-i usûle mutâbık olmak şartıyla, o birbirine muhâlif müfessirlerin beyânâtı ve ihtimalleri; zamanlara, tabakalara ve fehimlere göre murad ve câizdir diye hükmedilebilir."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 2. Âyetin Tefsiri › İkinci Misâl › 76. cümle (`isaratul-icaz/sure-i-bakara/2/misal-02/c076`)

**[Çıkarım]** Arapça asılda üçüncü şart "علم أصول مقاصد الشريعة"dir (şeriatin maksatlarının usulü); tercümede "ilm-i usûl" diye geçer. Asıl daha dar ve daha açık bir ölçü verir.

Verilen mânânın kesinlik derecesi: ihtimalli yerde "murad olan mânâ budur" hükmü bağlayıcı değildir.

> "وإن كان ظاهراً، أو نصاً يحتمل معنى آخر، فالإنكار بناءً على التأويل-دون التشهّي- ليس بكفر."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 6. Âyetin Tefsiri › 42. cümle (`isaratul-icaz-arabi/sure-i-bakara/6/c042`)

Tercümede:

> "Şâyet Kur'ânın o kelâmı, başka bir mânâya ihtimali olan bir nass veya zâhir olursa, üçüncü kaziyeyi kabûl etmek lâzım olmadığı gibi inkârı da küfür değildir."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 6. Âyetin Tefsiri › 59. cümle (`isaratul-icaz/sure-i-bakara/6/c059`)

Bir kelimeye mânâ yüklemenin emâresi: o mânâlar çevredeki âyetlerde açıkça akıyor olmalıdır.

> "واعلم أن الأمارة لنظر البلاغة على تشرّب هذه الكلمة لهؤلاء اللطائف هي أن هذه المقاصد الخمسة كالأنهار الجارية تحت هذه الآيات، حتى يفورُ هذا بكماله في آية.."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 4. Âyetin Tefsiri › 63. cümle (`isaratul-icaz-arabi/sure-i-bakara/4/c063`)

Tercümede:

> "مِنْ قَبْلِكَ kelimesinin bu beş letâife ma'kes ve mazhar olmasına nazar‑ı belâğatça delâlet eden emâre şudur ki: Bu beş maksad, bir nehir gibi şu âyetlerin altında cereyan etmekle, âyetten âyete intikal neticesinde مِنْ قَبْلِكَ havuzunda ictimâ' etmiştir.Evet kelimenin sathında görünen bir tereşşuh, bir yaşlık, kelimenin altında havuzun bulunduğuna delâlet ve îmâ eder."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 4. Âyetin Tefsiri › Îmân‑ı Bil'âhiret › 108. cümle (`isaratul-icaz/sure-i-bakara/4/iman-i-bilahiret/c108`)

### 3.6 Kur'ân'ın bir kısmı bir kısmını tefsir eder

> "وما أُجمِلَ في ﴿ الَّذ۪ينَ اَنْعَمْتَ عَلَيْهِمْ ﴾ يفسرُه ﴿ فَاُو۬لٰٓئِكَ مَعَ الَّذ۪ينَ اَنْعَمَ اللّٰهُ عَلَيْهِمْ مِنَ النَّبِيّ۪نَ وَالصِّدّ۪يق۪ينَ وَالشُّهَدَٓاءِ وَالصَّالِح۪ينَ ﴾ (النساء:٦٩) إذ القرآن يفسر بعضُه بعضاً."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Fâtiha › صِرَاطَ الَّذِينَ اَنْعَمْتَ عَلَيْهِمْ › 18. cümle (`isaratul-icaz-arabi/sure-i-fatiha/siratallezine-enamte-aleyhim/c018`)

Tercümede:

> "Zâten Kur'ânın bir kısmı, bir kısmını tefsir eder."

— İşaratü'l-İ'caz › Sûre‑i Fâtiha › Sırâtallezine En'amte Aleyhim «صِرَاطَ الَّذ۪ينَ اَنْعَمْتَ عَلَيْهِمْ» › 25. cümle (`isaratul-icaz/sure-i-fatiha/siratallezine-enamte-aleyhim/c025`)

### 3.7 Kâinat bahsi tebeîdir

> "فذكرُ الكائنات في القرآن إنما هو تبَعيّ واستطراديّ للاستدلال؛ إذ ما نزل القرآنُ لدرس الجغرافيا والقوزموغرافيا،بل إنما ذكرَ الكائنات للاستدلال بالصنعة الإِلهية والنِظام البديع على النَّظّام الحقيقي جلّ جلالُه، والحال أن أثر الصنعة والعمد والنظام يتراءى في كل شيء."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri › المسألة السادسة: › 84. cümle (`isaratul-icaz-arabi/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-06/c084`)

Tercümede:

> "Çünkü Kur'ân-ı Kerîm; coğrafya, kozmoğrafya gibi kasden kâinâtın keyfiyetinden mânâ-yı ismiyle bahseden bir fen, bir kitab değildir."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri (Nübüvvet Hakkında) › Altıncı Mes'ele › Dördüncü Nükte › 145. cümle (`isaratul-icaz/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-06/nukte-04/c145`)

Zâhirin fenne uymayan görünüşü kinaye kabilindendir; hakikate karîneler ve emâreler işaret eder (`isaratul-icaz-arabi/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-06/c086`, `isaratul-icaz-arabi/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-06/c091`). Müellif yer yer zamanının fenniyle tatbik yapar ve bunu "caizdir" diye kayıtlar (`isaratul-icaz-arabi/sure-i-bakara/29/mesele-02/c010`); ardından ikinci cevabı verir: Kur'ân'ın maksadı hilkat tarihi dersi değildir (`isaratul-icaz-arabi/sure-i-bakara/29/mesele-02/c017`).

## 4. Bir âyette izlenen sıra

Eser sırayı kendisi söyler:

> "اعلم أن مدار النظر في هذه الآية أيضاً من ثلاثة وجوه: نظمُها بسابقتها، والنظمُ بين جملها، ثم النظر بين هيئات جملةٍ جملةٍ."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 17‑20. Âyetlerin Tefsiri › المسألة العاشرة: › 140. cümle (`isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/mesele-10/c140`)

Tercümede:

> "Birincisi: Bu âyetin mâkabliyle vech‑i irtibatı."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 17‑20. Âyetlerin Tefsiri › 171. cümle (`isaratul-icaz/sure-i-bakara/17-20-ayetlerin-tefsiri/c171`)

> "İkincisi: Cümleleri arasındaki cihet‑i intizam."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 17‑20. Âyetlerin Tefsiri › 172. cümle (`isaratul-icaz/sure-i-bakara/17-20-ayetlerin-tefsiri/c172`)

> "Üçüncüsü: Cümlelerin hey'etlerinde, eczâlarında, kelimelerindeki nizâmdır."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 17‑20. Âyetlerin Tefsiri › 173. cümle (`isaratul-icaz/sure-i-bakara/17-20-ayetlerin-tefsiri/c173`)

> "اعلم أن لهذه الآية أيضاً الوجوهَ الثلاثة النظمية:"

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 28. Âyetin Tefsiri › 1. cümle (`isaratul-icaz-arabi/sure-i-bakara/28/c001`)

Tercümede:

> "Âyetlerin nazmına ait üç vecih, bu âyette de cârîdir."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 28. Âyetin Tefsiri › 5. cümle (`isaratul-icaz/sure-i-bakara/28/c005`)

**[Çıkarım]** Tam okumanın bulgusu (`docs/d1/birim-cizelgesi.md`):

- Eser üç vechi dokuz ayrı yerde adıyla sayar ve "öbür âyetlerde olduğu gibi" der.
- Bakara 9'dan sonra sıra sabittir: öncesiyle nazım (V1), cümlelerin birbiriyle nazmı (V2), her cümlenin hey'et ve kayıtları (V3). On beş birimin on beşi böyledir; her vecih kendi geçiş cümlesiyle açılır.
- Bakara 1–8'de düzen henüz oturmamıştır: 1. âyette üç vecih yerine dört mebhas vardır; 2'de V1 yoktur (sûrenin başı); 3–8'de V1 ve V3 belirgindir, V2 ya dağınıktır ya yoktur. Müellif de Fâtiha'nın ve ilk yarının daha mücmel kaldığını söyler (Tenbih).
- Fâtiha'da birim âyet değil kelimedir: önce kelimenin öncekiyle nazmı, sonra kelimenin nükteleri; sıra sabit değildir.

| Âyet | Üç vecih | Mukaddime ya da mesele | Asıl maksat adıyla söyleniyor mu |
|---|---|---|---|
| 1 | yok (dört mebhas) | — | dolaylı |
| 2 | V2, V3 | başta ilke; sonda soru–cevap | evet: Kur'ân'ın medhi |
| 3 | V1, V3 (V2 dağınık) | içeride ve sonda mesele | dolaylı |
| 4 | V1, V2, V3 | son cümleden önce: haşrin on burhanı | evet: nübüvvet, haşir |
| 5 | V1, V2, V3 | yok | hayır |
| 6 | V1, V3 | içeride soru–cevap | evet: terhib |
| 7 | V1, V3 | başta iki mukaddime: cebir ve ihtiyar | hayır |
| 8 | V1, V3 | yok | hayır |
| 9–10, 11–12, 13, 14–15, 16 | V1, V2, V3 (sıralı) | yok | hayır |
| 17–18, 19–20 | V1, V2, V3 (sıralı) | başta nazarî giriş: temsil, on iki mesele | hayır |
| 21–22 | V1, V2, V3 (sıralı) | başta iki mukaddime: ibadet; Sâni'in delilleri | evet: tevhid |
| 23–24 | V1, V2, V3 (sıralı) | başta mukaddime: nübüvvet, i'câz | evet: nübüvvet |
| 25 | V1, V2, V3 (sıralı) | V1'den sonra mukaddime: haşir | evet: haşir |
| 26–27 | V1, V2, V3 (sıralı) | yok (itirazlara cevap V1'de) | hayır |
| 28 | V1, V2, V3 (sıralı) | V2 içinde beş mesele | evet: mebde ve meâd delilleri |
| 29 | V1, V2, V3 (sıralı) | V2 başında üç mesele (üç lafız) | evet: meâdın tahkiki |
| 30 | V1, V2, V3 (sıralı) | başta mukaddime: melâike | evet: iman rüknü |
| 31–33 | V1, V2, V3 (sıralı) | başta mukaddime: kıssalar ve mu'cizeler | hayır (asıl yarıda biter) |

### 4.1 Birinci vecih: öncesiyle nazım

Âyetin neden orada durduğu sorulur. Bağ yalnız bir önceki âyetle sınırlı değildir: sûrenin başına, önceki bahislerin tamamına, sonraki âyetlere ve Kur'ân'ın bütününe uzanan hatlar sayılır.

> "أما الأول: فاعلم أن لمآلها ارتباطاتٍ متفاوتة مع الآيات السابقة، وخطوطاً ممتدة بالاختلاف إلى الجمل السالفة."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 25. Âyetin Tefsiri › 2. cümle (`isaratul-icaz-arabi/sure-i-bakara/25/c002`)

Tercümede:

> "Bu âyetin geçen âyetler ile mütefâvit çok irtibatları vardır."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 25. Âyetin Tefsiri › 10. cümle (`isaratul-icaz/sure-i-bakara/25/c010`)

> "Yani mezkûr cümlelere doğru bu âyetten uzanıp giden muhtelif hatlar vardır."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 25. Âyetin Tefsiri › 11. cümle (`isaratul-icaz/sure-i-bakara/25/c011`)

> "اعلم أن في هذه الآية أيضاً الوجوهَ الثلاثة النظمية، وأن مآل المجموع ينظر إلى سوابقه وإلى لواحقه وإلى مجموع القرآن."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 26‑27. Âyetlerin Tefsiri › 1. cümle (`isaratul-icaz-arabi/sure-i-bakara/26-27-ayetlerin-tefsiri/c001`)

Tercümede:

> "Bu âyetin de sâir arkadaşları gibi mevzû‑i bahs olacak vücûh-u irtibatı ve cihât-ı nazmiyesi üçtür."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 26‑27. Âyetlerin Tefsiri › 8. cümle (`isaratul-icaz/sure-i-bakara/26-27-ayetlerin-tefsiri/c008`)

> "Maahazâ, bu âyetin meâli, hem mâkabline, hem mâba'dine, hem Kur'ânın tamamına bakıyor."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 26‑27. Âyetlerin Tefsiri › 9. cümle (`isaratul-icaz/sure-i-bakara/26-27-ayetlerin-tefsiri/c009`)

Bağın atıfla mı kurulduğu, atıfsız mı bırakıldığı da bir kurala bağlanır:

> "قيل لك: إنَّ حُسن العطف ينظر إلى حُسن المناسبة، وحُسن المناسبة يختلف باختلاف الغرض المَسوق له الكلامُ."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 6. Âyetin Tefsiri › 13. cümle (`isaratul-icaz-arabi/sure-i-bakara/6/c013`)

Tercümede:

> "C – Atfın hüsnü, münâsebetin hüsnüne bakar."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 6. Âyetin Tefsiri › 15. cümle (`isaratul-icaz/sure-i-bakara/6/c015`)

> "Hüsn‑ü münâsebet, her iki cümleden takib edilen garaz ve maksadın bir olmasına mütevakkıftır."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 6. Âyetin Tefsiri › 16. cümle (`isaratul-icaz/sure-i-bakara/6/c016`)

### 4.2 İkinci vecih: âyetin cümleleri arasındaki nazım

Cümlelerin birbirini nasıl istediği gösterilir. İki ana araç vardır. Birincisi temsildir: âyette söylenen ve söylenmeyen cümlelerin zinciri bir misalle kurulur.

> "وأما وجه النظم بين الجمل الصريحة والضمنية في هذه الآية فهو عينُ النظم والربط في ما أمثّل لك وهو أنك إذا رأيت أحداً يسلك في طريق تنجرّ إلى هلاكه، فأولاً تنصحه قائلا له: «مذهبُك هذا ينهار بك في البوار فتجنَّب»."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 11‑12. Âyetlerin Tefsiri › 4. cümle (`isaratul-icaz-arabi/sure-i-bakara/11-12-ayetlerin-tefsiri/c004`)

Tercümede:

> "Bu âyetin ihtiva ettiği mezkûr ve gayr‑ı mezkûr cümleler arasındaki vech-i irtibat bir misâlle izâh edilecektir.Şöyle ki:"

— İşaratü'l-İ'caz › Sûre‑i Bakara › 11‑12. Âyetlerin Tefsiri › 11. cümle (`isaratul-icaz/sure-i-bakara/11-12-ayetlerin-tefsiri/c011`)

İkincisi dinleyenin zihnidir: her cümleden sonra sâmiin zihninde doğan soru yazılır, sonraki cümle ona cevaptır (`isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/mesele-10/c164..c189`; `isaratul-icaz-arabi/sure-i-bakara/25/mukaddime/c112..c122`: sekiz müteselsil sual).

> "ثم بعد تمام السؤال والاستفسار والتعجب ينتظر ذهنُ السامع لجوابه تعالى."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 30. Âyetin Tefsiri › مقدمة › 36. cümle (`isaratul-icaz-arabi/sure-i-bakara/30/mukaddime/c036`)

Tercümede:

> "Melâikenin suâl‑i taaccüb ve istifsarları bittikten sonra, sâmi', Cenâb-ı Hak’tan verilecek cevabı beklerken Kur'ân-ı Kerîm, قَالَ اِنّ۪ٓي اَعْلَمُ مَا لَا تَعْلَمُونَ cümlesiyle cevab vermiştir."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 30. Âyetin Tefsiri › Cümlelerin Arasındaki İrtibata Geldik › Dördüncü Vecih › 17. cümle (`isaratul-icaz/sure-i-bakara/30/cumlelerin-arasindaki-irtibata-geldik/vecih-04/c017`)

### 4.3 Üçüncü vecih: cümlelerin hey'etleri, kayıtları ve kelimeleri

**[Çıkarım]** Arapça asılda tekrar eden işler (adresler `docs/d1/birim-cizelgesi.md` "Üçüncü vecihte neye bakılıyor" bölümünde):

**Bakılacak yerlerin önce sayılması.** Cümlenin başında nükte beklenen kayıtlar listelenir, sonra sırayla işlenir.

> "اعلم أن المظان التي تتلمّع فيها النُّكَتُ: هي نظمُها مع سابقها، ثم المحسوسيةُ في ﴿ اُو۬لٰٓئِكَ ﴾ ، ثم البُعْدية فيها، ثم العلوّ في ﴿ عَلٰى ﴾، ثم التنكير في ﴿ هُدًى ﴾، ثم لفظ ﴿ مِنْ ﴾، ثم التربية في ﴿ رَبِّهِمْ ﴾ ."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 5. Âyetin Tefsiri › 3. cümle (`isaratul-icaz-arabi/sure-i-bakara/5/c003`)

Tercümede:

> "Bu cümledeki nüktelere işâret eden me'hazler şunlardır:"

— İşaratü'l-İ'caz › Sûre‑i Bakara › 5. Âyetin Tefsiri › 2. cümle (`isaratul-icaz/sure-i-bakara/5/c002`)

**Tercih sorusu: neden şu lafız, şu değil.** Usulün en sık kullanılan aracıdır ("إيثار … على", "بدل": 66 cümle).

> "وأن إيثار ﴿ جَاعِلٌ ﴾ على «خالق» إشارةٌ إلى أن مدار الشبهة والاستفسار الجعلُوالتخصيص لعمارة الأرض لا الخلقُ والإيجاد، لأن الوجود خيرٌ محض والخلق فعلُه الذاتيّ لا يُسأل عنه.."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 30. Âyetin Tefsiri › مقدمة › 47. cümle (`isaratul-icaz-arabi/sure-i-bakara/30/mukaddime/c047`)

Tercümede:

> "جَاعِلٌ kelimesinin خَالِقٌ kelimesine tercihen zikri: Melâikenin medâr‑ı şübhe ve mûcib-i istifsarları, halk ve icâd fiili değildir."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 30. Âyetin Tefsiri › Cümlelerin hey'et ve nüktelerine geldik › 14. cümle (`isaratul-icaz/sure-i-bakara/30/cumlelerin-heyet-ve-nuktelerine-geldik/c014`)

**Beklenenle muvazene.** Üslûbun ya da makamın gerektirdiği ifade söylenir; âyetin ondan ayrıldığı nokta nükte olur.

> "ثم إن سجية الأسلوب تقتضي «وعليهم عقاب شديد»."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 7. Âyetin Tefsiri › مقدمة اخرى › 72. cümle (`isaratul-icaz-arabi/sure-i-bakara/7/mukaddime-2/c072`)

Tercümede:

> "S – Üslûbun mecrâ‑yı tabîisi وَعَلَيْهِمْ عِقَابٌ شَد۪يدٌ cümlesi iken, üslûbun muktezâsı olan şu cümlenin terkiyle وَلَهُمْ عَذَابٌ عَظ۪يمٌ cümlesi ihtiyar edilmiştir."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 7. Âyetin Tefsiri › İkinci Bir Mukaddime › Yedincisi › 64. cümle (`isaratul-icaz/sure-i-bakara/7/mukaddime-2/yedincisi/c064`)

**Kelimenin maddesi ve sîgası ayrı ayrı.**

> "ثم إن هذا حكايةٌ عن دعواهم ففي صورة الحكاية إشارةٌ إلى ردّ المَحكيّ بوجهين، كما أن في المَحكيّ إشارةً إلى قوته بجهتين؛ إذ ﴿ يَقُولُ ﴾ يرمز بمادَّته إلى أن قولَهم ليس عن اعتقادٍ وفعلٍ، بل يقولون بأفواههم ما ليس في قلوبهم.."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 8. Âyetin Tefsiri › 35. cümle (`isaratul-icaz-arabi/sure-i-bakara/8/c035`)

Tercümede:

> "يَقُولُ kelimesi, madde cihetiyle onların îmân da'vâsının an‑i'tikàd olmayıp ancak kuru bir sözden ibaret olduğuna işârettir."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 8. Âyetin Tefsiri › 57. cümle (`isaratul-icaz/sure-i-bakara/8/c057`)

> "وبصيغته يومئ إلى أن سببَ استمرار مُدافعَتهم وادعائهم مُراءاة الناس لا مُحرّك وجداني.."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 8. Âyetin Tefsiri › 36. cümle (`isaratul-icaz-arabi/sure-i-bakara/8/c036`)

Tercümede:

> "Kezâlik, muzârî sîgasıyla zikrinde, onları ale'd-devam yaptıkları müdafaaya sevk eden, vicdânî bir sebeb değildir, ancak halka karşı bir riyâkârlık olduğuna işârettir."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 8. Âyetin Tefsiri › 58. cümle (`isaratul-icaz/sure-i-bakara/8/c058`)

**Öbür işler:** âyetin îcâzı altındaki söylenmemiş (mukadder) cümlelerin açılması; iki cümlenin kayıtlarının karşılıklı eşlenmesi; sık geçen bir edatın her yerdeki hâssası ile bu makamdaki hususî nüktesinin ayrılması; şartiyelerin kıyas olarak tahlili; mücmel lafzın başka âyetle açılması; ve tahlilin sonunda bütün kayıtların asıl garaza nasıl aktığının tek bakışta toplanması.

Fâtiha'da aynı işler kelime ölçeğinde yapılır.

## 5. Mukaddime ve meseleler ne zaman gelir

**[Çıkarım]** Mukaddime usulün sabit bir basamağı değildir. Dört durumda gelir; eser çoğunda gerekçesini kendisi söyler.

| Durum | Birimler |
|---|---|
| (a) Âyetin meâli dört maksattan ya da iman rükünlerinden biridir | 4 (haşir), 21–22 (ibadet, tevhid), 23–24 (nübüvvet), 25 (haşir), 30 (melâike) |
| (b) Âyetin altında büyük bir kelâm ihtilafı vardır | 7 (cebir ve ihtiyar) |
| (c) Bir üslûp türü ilk kez toplu gelir ve nazarî temel ister | 2 (kayıtların tecâvübü), 17–20 (temsil), 31–33 (kıssa ve mu'cize) |
| (d) Bir lafız tahkik ister | 28 (her cümleye bir mesele), 29 (üç lafız) |

Gerekçe cümlelerinden örnekler. (a):

> "اعلم أنه كما أثبتت الآيةُ السابقة أوّلَ المقاصد الأساسية القرآنية وهو التوحيد؛ كذلك تثبت هذه الآية ثانيَ المقاصد الأربعة وهو إثبات نبوّة محمّد عليه الصلاة والسلام بأكمل معجزاته الذي هو التحدّي بإعجاز القرآن."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri › مقدمة في تحقيق النبوة › 1. cümle (`isaratul-icaz-arabi/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mukaddime/c001`)

Tercümede:

> "Birinci maksadı olan “Tevhid”, evvelki âyetle beyân edilmiştir."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri (Nübüvvet Hakkında) › Mukaddime › 2. cümle (`isaratul-icaz/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mukaddime/c002`)

> "Bu âyetle de, ikinci maksad olan “Nübüvvet” beyân ve izâh edilmiştir."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri (Nübüvvet Hakkında) › Mukaddime › 3. cümle (`isaratul-icaz/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mukaddime/c003`)

> "ولقد فصلنا دلائلَ نبوّته في كتاب آخر فلنلخِّص بعضها هنا في ستِّمسائل:"

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 23‑24. Âyetlerin Tefsiri › مقدمة في تحقيق النبوة › 2. cümle (`isaratul-icaz-arabi/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mukaddime/c002`)

Yapay zekâ tercümesi: Nübüvvetinin delillerini başka bir kitapta tafsil ettik; burada bir kısmını altı meselede hülâsa edelim.

> "اعلم أن مآل هذه الآية هو المقصدُ الرابع من المقاصد الأربعة المشهورة وهو «مسألة الحشر»."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 4. Âyetin Tefsiri › 69. cümle (`isaratul-icaz-arabi/sure-i-bakara/4/c069`)

Tercümede:

> "Bu âyet, Haşir mes'elesine işârettir."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 4. Âyetin Tefsiri › Delâil‑i Haşr › 2. cümle (`isaratul-icaz/sure-i-bakara/4/delail-i-hasr/c002`)

> "ثم إنّا قد استفدنا من نظم القرآن عشرةَ براهين عليها، ذكرناها في كتاب آخرفناسبَ تلخيصُها هنا."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 4. Âyetin Tefsiri › 70. cümle (`isaratul-icaz-arabi/sure-i-bakara/4/c070`)

Tercümede:

> "Haşrin isbâtı hakkında feyz‑i Kur'ân’dan fehmettiğim ve başka bir risalede tafsilâtıyla zikrettiğim on bürhânın hülâsasına burada işâret edeceğiz."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 4. Âyetin Tefsiri › Delâil‑i Haşr › 3. cümle (`isaratul-icaz/sure-i-bakara/4/delail-i-hasr/c003`)

(b):

> "اعلم أنه لزمنا أن نقف هنا حتى نستمع لما يتكلّم به المتكلمون؛ إذ تحت هذه الآية حربٌ عظيمة بين أهل الاعتزال وأهل الجبر وأهل السنة والجماعة."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 7. Âyetin Tefsiri › مقدمة › 1. cümle (`isaratul-icaz-arabi/sure-i-bakara/7/mukaddime/c001`)

Tercümede:

> "Bu âyetin üzerinde durmak icâb ediyor."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 7. Âyetin Tefsiri › Mukaddime › 1. cümle (`isaratul-icaz/sure-i-bakara/7/mukaddime/c001`)

> "Ehl‑i İ'tizâl, Ehl-i Cebir, Ehl-i Sünnet ve'l-Cemâat gibi ehl-i kelâmın şu âyet-i azîmenin altında yaptıkları muhârebe-i ilmiyelerini dinleyelim."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 7. Âyetin Tefsiri › Mukaddime › 2. cümle (`isaratul-icaz/sure-i-bakara/7/mukaddime/c002`)

(c):

> "كلٌّ منها خيطٌ لحقائقولما ذُكرت هذه الآيات التمثيلية هنا -دفعةً- ناسبَ تلخيص تلك المسائل فنقول وبالله التوفيق:"

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 17‑20. Âyetlerin Tefsiri › فصل ومقدمة › 12. cümle (`isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/fasil-2/c012`)

Yapay zekâ tercümesi: Her biri hakikatler için bir iptir. Bu temsîlî âyetler burada toplu olarak zikredilince o meseleleri hülâsa etmek münasip düştü; Allah'ın tevfikiyle deriz ki:

(d):

> "فاعلم أن لفظَ ﴿ جَم۪يعًا ﴾ في الجملة الأولى، ولفظَ ﴿ ثُمَّ ﴾ في الثانية، ولفظَ ﴿ سَبْعَ ﴾ في الثالثة تقتضي تحقيقاً."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 29. Âyetin Tefsiri › 11. cümle (`isaratul-icaz-arabi/sure-i-bakara/29/c011`)

Tercümede:

> "Birinci cümlede جَم۪يعًا , ikinci cümlede «ثُمّ» , üçüncü cümlede «سَبْعَ» kelimeleri için bir tahkîkat lâzımdır."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 29. Âyetin Tefsiri › 17. cümle (`isaratul-icaz/sure-i-bakara/29/c017`)

**[Çıkarım]** Mukaddimelerin ortak özellikleri:

- Çoğu, başka bir kitapta tafsil edilmiş bir meselenin hülâsasıdır (yukarıdaki iki cümle; `isaratul-icaz-arabi/sure-i-bakara/21-22-ayetlerin-tefsiri/mukaddime/c051`). Bilinen şey tekrar edilmez, ehlinin kitaplarına havale edilir (`isaratul-icaz-arabi/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-07/c002`).
- Mukaddimedeki her delil âyetin bir lafzına bağlanır (`isaratul-icaz-arabi/sure-i-bakara/21-22-ayetlerin-tefsiri/mukaddime/c075`, `isaratul-icaz-arabi/sure-i-bakara/21-22-ayetlerin-tefsiri/mukaddime/c076`): mesele âyetten kopuk bir risale değildir.
- Yeri sabit değildir: çoğu kez üç vecihten önce; 25'te V1'den sonra; 4'te son cümlenin nüktelerinden önce; 28 ve 29'da V2'nin içinde.
- Münafıklar bahsinde (9–16) hiç mukaddime yoktur; müellif sebebini söyler (1.2: şüpheleri zikretmemek).
- Birim sonunda kısa bir ders ya da soru–cevap olabilir (3: zekât ve ribâ; 7: ebedî ceza; 9–10: kizb ve sıdk).

## 6. Anlatım biçimi

**[Çıkarım]** Arapça asılda tekrar eden kalıplar:

- **Soru ve cevap.** Mukadder itiraz "إن قلت" diye sorulur, "قيل لك" ya da "قلت" diye cevaplanır (73'er cümle). Tercümede "S –", "C –".
- **Hitap.** Her bahis "اعلم" (bil ki) ile açılır (190 cümle). Tercümede yer yer "Arkadaş!".
- **Temsil.** Soyut bağ bir misalle gösterilir (4.2).
- **Kural, sonra uygulama.** Önce bir belâgat kuralı söylenir, sonra âyete uygulanır (4.1'deki atıf kuralı).
- **Örnek verip gerisini okura bırakmak.** "Kıyas et" ve benzerleri 30 cümlede geçer; on iki bağdan üçü gösterilir ve:

> "وعليك باستنباط البواقي."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 2. Âyetin Tefsiri › مقدمة › 48. cümle (`isaratul-icaz-arabi/sure-i-bakara/2/mukaddime/c048`)

Yapay zekâ tercümesi: Kalanlarını çıkarmak sana düşer.

- **Toplayış.** Tahlilden sonra kayıtlar tek bakışta asıl garaza bağlanır (`isaratul-icaz-arabi/sure-i-bakara/6/c082..c085`; `isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/mesele-10/c113`).
- **Beyit.** Yer yer bir beyitle bağlanır; 3.2'deki ilkenin beyti üç yerde geçer (`isaratul-icaz-arabi/sure-i-bakara/2/mukaddime/c002`, `isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/mesele-04/c002`, `isaratul-icaz-arabi/sure-i-bakara/26-27-ayetlerin-tefsiri/c113`).

## 7. Kaynaklarla ilişkisi

- Eser me'hazsiz yazılmıştır; tefsirlere müracaat edilememiştir (1.4). Tefsirlerle uyum ölçü olarak anılır, şart değil.
- Buna rağmen belâgat ve tefsir âlimleri adıyla anılır. **[Çıkarım]** Arapça asılda adıyla geçenler: Abdülkāhir el-Cürcânî (Delâilü'l-İ'câz, Esrârü'l-Belâga; 2.6), Sekkâkî (Miftâh ve hâtimesi: `isaratul-icaz-arabi/sure-i-bakara/2/mukaddime/c021`, `isaratul-icaz-arabi/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-07/c061`), Zemahşerî (Keşşâf: `isaratul-icaz-arabi/sure-i-bakara/2/mukaddime/c022`), Câhız, Fahreddin Râzî, Sa'd (Teftâzânî: `isaratul-icaz-arabi/sure-i-bakara/3/c023`), Sîbeveyh (`isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/mesele-08/c001`), Seyyid Şerif Cürcânî, İbn Arabî, Bûsîrî; İbn Abbâs'tan iki tefsir. Bir yerde Muhammed Abduh adıyla nakledilir ve müellif kendi görüşünü "أقول" diye ekler (`isaratul-icaz-arabi/sure-i-bakara/25/mukaddime/c090..c091`).
- Delillerin tafsili için başka tefsire gönderme yapılır:

> "وأما النقليّ مع الرمز للعقليّ فراجع هذا الموضع من تفسير فخر الدين الرازيفإنه عدّد الآيات المثبتة للحشر."

— İşârâtü'l-İ'câz (Arapça) › Sûre‑i Bakara › 25. Âyetin Tefsiri › مقدمة › 28. cümle (`isaratul-icaz-arabi/sure-i-bakara/25/mukaddime/c028`)

Tercümede:

> "Aklî ve naklî deliller ise: Fahreddinü'r‑Râzî’nin tefsirinde, bu kabîl delilleri bildiren âyetler beyân edilmiştir."

— İşaratü'l-İ'caz › Sûre‑i Bakara › 25. Âyetin Tefsiri › Üçüncü ve Dördüncü Noktalar › 12. cümle (`isaratul-icaz/sure-i-bakara/25/ucuncu-ve-dorduncu-noktalar/c012`)

## 8. Taslak için kurallar

Kullanıcının kararları (2026-11-09 ve 2026-11-10; `PLANLAR.md` D1). Bu bölüm eserin sözü değildir.

1. **Ad ve damga.** Yapay zekânın yazdığı "yapay zekâ taslağı"dır; "tefsir" denmez, yayımlanmaz. Ehlinin doğrulamasına, eklemesine ve çıkarmasına sunulur.
2. **Dil.** Taslak Arapça yazılır; Türkçesi onun tercümesidir (iki ayrı taslak değil). Tercüme Arapçadan paragraf paragraf yapılır ve damgalıdır. Usul Arapça asıldan öğretilir, Türkçe tercüme destek olur.
3. **Me'haz.** İşârâtü'l-İ'câz'ın tamamı, Risale-i Nur ve Tefsir ile Hadis eklentilerindeki eserler. Her iddia bir kaynağa, her nükte âyetin bir lafzına ya da hey'etine bağlanır. Dil ve belâgat iddiaları ayrı işaretlenir.
4. **Sıra.** Âyet; gerekiyorsa mukaddime; öncesiyle nazım; cümlelerin birbiriyle nazmı; her cümlenin hey'et ve kayıtları (4. bölüm).
5. **Dört maksat.** Asıl maksat her zaman söylenir. Öbür maksatlar yalnız âyetin bir lafzına ya da hey'etine dayandırılabiliyorsa ve derecesiyle (sarih, işaret, remiz…) söylenir; dördü her âyette zorla gösterilmez (3.1).
6. **Mukaddime.** Yalnız 5. bölümdeki dört durumdan biri varsa yazılır; kısa tutulur; her iddiası âyetin bir lafzına bağlanır. O mesele İşârâtü'l-İ'câz'da ya da Risale-i Nur'da işlenmişse yeniden kurulmaz, oraya atıfla hülâsa edilir.
7. **Kabul ölçüsü.** Bir nükte Arap dili ilimlerine, belâgate ve şeriatin maksatlarına uygun olmalı (3.5); hayal hakikat çekirdeğine dayanmalı (2.5); her nüktenin delâlet derecesi belirtilmeli (2.3).

## 9. Açık sorular

1. Bu belgedeki Arapça okuma bir yapay zekânındır; Arapça ve belâgat bilen biri çizelgedeki "şu cümle şu vechin başlangıcıdır" tespitlerini ve derleyenin tercümelerini denetlemelidir.
2. Bakara 1–8 ile sonrasının farkı (4. bölüm) usulün gelişmesi midir, yoksa o âyetlerin gereği mi? Taslak hangi düzeni esas almalı? **Kullanıcının görüşü (2026-11-10):** Bakara 9'dan sonraki sabit düzen (V1 → V2 → V3); öbür türlü usul sabit olmaz. Prova bu düzenle yapılır; mütehassısın görüşü de alınacak.
3. Arapça taslağın üslûbu eserin îcâzlı üslûbunu mu izlemeli, yoksa daha açık mı yazılmalı? Müellif kısalığın sebeplerini zamanın şartlarına ve talebelerinin zekâsına bağlar (Tenbih). **Kullanıcının görüşü (2026-11-11):** provada îcâzlı; gizlenen metinle yan yana okuma ancak böyle adil olur. Mütehassısın görüşü de alınacak.
4. Türkçe tercümenin dili: Abdülmecid Nursî tercümesinin diline mi yakın olmalı, bugünkü Türkçeye mi? **Kullanıcının görüşü (2026-11-10):** Abdülmecid Nursî tercümesinin diline yakın; o tercüme Arapça asla muvafık bir tarzdadır, taslağın tercümesi de o yoldan gider. Prova bu dille yapılır; mütehassısın görüşü de alınacak.

## Denetim

Bu belgedeki her alıntı, altındaki kimliğin veritabanındaki metniyle birebir karşılaştırılır; geçen bütün cümle kimliklerinin varlığı denetlenir:

```
python3 scripts/d1-usul-denetim.py
```

