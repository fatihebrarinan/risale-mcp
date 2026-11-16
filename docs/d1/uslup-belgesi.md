# İşârâtü'l-İ'câz'ın anlatım kalıpları: Arapça aslından sayım (D12.4)

> **Bu belge nedir.** İşârâtü'l-İ'câz'ın Arapça aslında tekrar eden anlatım kalıplarının programla çıkarılmış dökümüdür (`scripts/d1-uslup.py`, `PLANLAR.md` D12.4). Usul özeti (`usul-ozeti.md`) eserin **ne yaptığını**, bu belge **nasıl söylediğini** gösterir. Sayılar kelime taramasıdır (hareke atılarak; bir kalıp bir cümlede bir kez), yaklaşık okunmalıdır; kalıpların gruplanması derleyenindir. Örnekler veritabanındaki cümlelerdir, kimlikleriyle; uzun olanlar kısaltılmıştır (" …"). Tercüme verilmez.
> **Kapsam.** Arapça asıl, Fâtiha ve Bakara 1–33 (eserin tamamı).

## 1. Ölçüler

- 3.264 cümle. 42 birim. 1.475 paragraf.
- Cümle uzunluğu (kelime): ortanca 15, çeyrekler 8–23, en uzun 140.
- Paragraf başına cümle: ortanca 1, ortalama 2.2.
- **[Çıkarım]** Bir nükte çoğunlukla bir iki cümledir: îcâz cümle sayısında değil, cümlenin yükündedir; kayıtlar ".." ve "؛" ile aynı cümlede dizilir.

## 2. Nakil ve istinbat

Cümlelerin **43**'inde (%1.3) bir âlimin, bir eserin, bir mezhebin ya da "قيل:", "قال بعض" ile bir kavlin adı geçer ("قيل لك" takdir kalıbıdır, sayılmaz); geri kalanında müellif kaynak anmadan konuşur. Ad aramadır, yaklaşık okunmalı. Ad geçen birimler: 16/42.

- **[Çıkarım]** Eserin nükteleri büyük çoğunlukla **istinbattır**: âyetin lafzından, hey'etinden ve makamından kaynak anmadan çıkarılır (usul özeti 1.4: me'hazsiz yazıldı; 2.7: "harice boykotaj"). Nakil azdır ve adıyla yapılır. Taslakta da nakil kaynağa bağlı ve numaralı olmalı; istinbat ise kaynak aranmadan, etiketiyle ve gerekçesi lafza bağlı yazılabilmeli.

Ad geçen cümlelerden örnek:

- `isaratul-icaz-arabi/sure-i-bakara/25/mukaddime/c086`: وأما واو ﴿ وَعَمِلُوا ﴾ فإشارة -بسرّ المغايرة- إلى أن العمل ليس داخلاً في الإيمان كما قالت المعتزلة.
- `isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/c013`: وإن شئت التفصيل فاستمع معي لما يترنّم به صاحبُ «دلائل الإعجاز» في أسرار بلاغته؛حيث قال:
- `isaratul-icaz-arabi/sure-i-bakara/7/mukaddime/c004`: إنَّ مذهب أهل السنة والجماعة هو الصراطُ المستقيم، وما عداه إما إفراطٌ أو تفريط.

## 3. Açılış ve geçiş

Bir bahsin ve bir vechin nasıl açıldığı.

| Kalıp | İşi | Cümle | Birim |
|---|---|---:|---:|
| اعلم أن | bahsin açılışı | 79 | 23 |
| لهذه الآية … الوجوه الثلاثة | üç vechin anılması | 4 | 4 |
| أما نظمها/نظم … بسابقتها/بما قبلها | birinci vecih: öncesiyle nazım | 10 | 8 |
| وأما نظم الجمل | ikinci vecih: cümlelerin nazmı | 21 | 10 |
| وأما … الهيئات / جملة جملة | üçüncü vecih: hey'etler | 47 | 14 |
| وأما ﴿…﴾ | üçüncü vecihte bir lafzın ele alınışı | 66 | 12 |

Örnekler:

- *اعلم أن* · `isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/mesele-10/c005`: اعلم أن سلامة الكلام التي هي سببُ صحته وقوّته هي أن يكون الكلام بحيث يشير إلى المبادئ والدلائل، ويرمز إلى اللوازم والتوابع، وبقيود الموضوع والمحمول وكيفياتهما يومئ إلى …
- *اعلم أن* · `isaratul-icaz-arabi/sure-i-fatiha/siratallezine-enamte-aleyhim/c001`: اعلم أن نظم دُرَر القرآن ليس بخيط واحد بل النظمُ -في كثيرٍ- نقوشٌ تحصل من نسج خطوطِ نِسَبٍ متفاوتةٍ قُرباً وبُعداً، ظهوراً وخفاء.
- *لهذه الآية … الوجوه الثلاثة* · `isaratul-icaz-arabi/sure-i-bakara/31-33-ayetlerin-tefsiri/mukaddime/c018`: ثم إن لهذه الآية أيضاً الوجوه الثلاثة النظمية:
- *لهذه الآية … الوجوه الثلاثة* · `isaratul-icaz-arabi/sure-i-bakara/29/c001`: اعلم أن لهذه الآية أيضاً الوجوه الثلاثة النظمية؛
- *أما نظمها/نظم … بسابقتها/بما قبلها* · `isaratul-icaz-arabi/sure-i-bakara/16/c001`: اعلم أن وجه نظمها بسابقتها هو أن هذه الآية فذلكةٌ وإجمال للتفاصيل السابقة، وتصويرٌ لها بصورة عالية مؤثرة.
- *أما نظمها/نظم … بسابقتها/بما قبلها* · `isaratul-icaz-arabi/sure-i-bakara/28/c002`: أما نظمُ مآلها بسابقها، فاعلم أن الله تعالى لما دعا الناس إلى عبادته والاعتقادِ به، وذكر أصولَ العقائد والأحكام مشيراً إلى دلائلها إجمالاً؛ عاد في هذه الآية مع لواحقها …
- *وأما نظم الجمل* · `isaratul-icaz-arabi/sure-i-bakara/25/mukaddime/c030`: أما نظمُ جملها بعض مع بعض، فاعلم أن السلك الذي نُظّم فيه جواهرُ جُمل هذه الآية وسلسلتُها هي: أن السعادة الأبدية قسمان:
- *وأما نظم الجمل* · `isaratul-icaz-arabi/sure-i-bakara/30/mukaddime/c033`: وأما نظم الجمل بعضها مع بعض فهو: أن الآية تنصبُّ -بناءً على اقتضاءِ ﴿ اِذْ ﴾ رديفا لها، وعطفِه على ﴿ وَهُوَ بِكُلِّ شَيْءٍ عَل۪يمٌ ﴾ - إلى تقديرِ«إذ خلق ما خلق منتظما …
- *وأما … الهيئات / جملة جملة* · `isaratul-icaz-arabi/sure-i-bakara/31-33-ayetlerin-tefsiri/mukaddime/c034`: أما نظم هيئات جملة جملة:
- *وأما … الهيئات / جملة جملة* · `isaratul-icaz-arabi/sure-i-bakara/2/mukaddime/c030`: انظُر نظرة واحدة إلى تلك القيود والهيئات لترى كيف يلقي كلٌّ حصته إلى المقصد المشترك مع دليله الخاص، وكيف يفور نورُ البلاغة من الجوانب.
- *وأما ﴿…﴾* · `isaratul-icaz-arabi/sure-i-bakara/29/mesele-03/c069`: وأما ﴿ اسْتَوٰٓى ﴾ ففيه إيجاز، أي أراد أن يسوّي..
- *وأما ﴿…﴾* · `isaratul-icaz-arabi/sure-i-bakara/4/c167`: وأما ﴿ هُمْ ﴾ ففيه حصرٌ، وفي الحصر تعريض بأن إيمان من لم يؤمن بمحمد عليه الصلاة والسلام من أهل الكتاب ليس بيقين، بل إنما يظنونه يقيناً.

## 4. Delâlet derecesi

Bir nüktenin lafızdan ne kuvvette çıktığı (usul özeti 2.3).

| Kalıp | İşi | Cümle | Birim |
|---|---|---:|---:|
| إشارة / يشير | işaret | 372 | 32 |
| رمز / يرمز | remiz | 141 | 28 |
| إيماء / يومئ | îmâ | 114 | 23 |
| تلويح / يلوح | telvih | 35 | 12 |
| تعريض | ta'rîz | 11 | 6 |
| صريح / تصريح / نص | sarih | 18 | 11 |
| كناية | kinaye | 5 | 3 |

Örnekler:

- *إشارة / يشير* · `isaratul-icaz-arabi/sure-i-bakara/6/c063`: ثم في إيراد ﴿ كَفَرُوا ﴾ فعلاً ماضياً، إشارةٌ إلى أنهم اختاروا الكفر بعد تبيُّن الحقِّ فلذا لا يُفيدُ الإنذار.
- *إشارة / يشير* · `isaratul-icaz-arabi/sure-i-bakara/14-15-ayetlerin-tefsiri/c063`: وفيه إشارة إلى أنه لا مسلك لهم وليس لهم مقصود معين.
- *رمز / يرمز* · `isaratul-icaz-arabi/sure-i-fatiha/ve-led-dallin/c015`: والقمرَ والنجومَ والبحرَ وأخواتها يناجيه كلٌّ منها بلسانه الخاص وترمز إليه: ب«أهلاً وسهلاً، أمَا تعرفنا؟
- *رمز / يرمز* · `isaratul-icaz-arabi/sure-i-bakara/7/mukaddime-2/c050`: فإذاً في التعبير بالقلب رمزٌ إلى أن اللطيفةَ الربانيةَ لمعنويات الإنسان كالجسم الصنوبري لجسدِه.
- *إيماء / يومئ* · `isaratul-icaz-arabi/sure-i-bakara/13/c011`: وبناء المفعول في ﴿ ق۪يلَ ﴾ إيماء إلى أن وجوبَ النصيحة على سبيل الكفاية كما مرَّ.
- *إيماء / يومئ* · `isaratul-icaz-arabi/sure-i-bakara/c004`: و ﴿ وَيْلٌ يَوْمَئِذٍ ... ﴾ الخ..
- *تلويح / يلوح* · `isaratul-icaz-arabi/sure-i-fatiha/c030`: وفي تقديم الباء تلويحٌ إلى التوحيد..وفي ﴿ اَلرَّحْمٰنِ ﴾ تلميحٌ إلى نظام العدالة والإحسان..
- *تلويح / يلوح* · `isaratul-icaz-arabi/sure-i-bakara/2/mukaddime/c011`: وانظر الإشارة في ﴿ ذٰلِكَ ﴾ المختصة بالرجوع إلى الذات مع الصفات لتعلَم أنها كما تفيد التعظيم -لأنها إما إشارة إلى المشار إليه ب ﴿ الٓمٓ ﴾ أو المبشَّر به في التوراة …
- *تعريض* · `isaratul-icaz-arabi/sure-i-bakara/5/c040`: وأما ضميرُ الفصل فمع أنه تأكيدُ الحصر الذي فيه تعريضٌ بأهل الكتاب الذين لم يؤمنوا بالنبيّ عليه السلام، فيه نكتةٌ لطيفة وهي: أن توسُّط ﴿ هُم ﴾ بين المبتدأ والخبر من شأنه …
- *تعريض* · `isaratul-icaz-arabi/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-07/c192`: وكذا تعريضٌ بأنكم لستم من أهل الصدق إلّا أن يُفرَض فرضاً، بل من أهل السفسطة، ما وقعتم في الريب من طريق طلب الحق بل طلبتم فوقعتم فيه..
- *صريح / تصريح / نص* · `isaratul-icaz-arabi/sure-i-bakara/4/c008`: وأيضا التنصيصُ على قسْمَي المتقينللتصريح بشمول هداية القرآن لكافة الأُمم، والتلويحُ لعموم رسالة محمد عليه السلام لقاطبة المِلل..
- *صريح / تصريح / نص* · `isaratul-icaz-arabi/sure-i-bakara/31-33-ayetlerin-tefsiri/mukaddime/c041`: و ﴿ اٰدَمَ ﴾ أي الشخص الأرضي الذي أراد الله تعالى خلافته وسمّاه آدم فالتصريح بالعلم لتنويهه وتشهيره وإحضاره بصورته.
- *كناية* · `isaratul-icaz-arabi/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-07/c203`: والثانية: الإيجاز، إذ «فَعَل» كما أنه في الصَّرف ميزانُ الأفعال وجنسُها؛ كذلك في الأساليب مصدر الأعمال وملخص القصص كأنه ضمير الجمل كناية عنها.
- *كناية* · `isaratul-icaz-arabi/sure-i-bakara/9-10-ayetlerin-tefsiri/c087`: إلّا أن التعريض والكناية ليسا من الكذب.

## 5. Takdir ve mukadder sual

Söylenmeyenin açılışı (usul özeti 2.4; Muhâkemât On Birinci Mes'ele).

| Kalıp | İşi | Cümle | Birim |
|---|---|---:|---:|
| كأنه قيل | dinleyenin sorusu | 18 | 12 |
| فإن قلت / قلت / قيل لك | mukadder itiraz ve cevap | 148 | 24 |
| سؤال مقدر / جواب سؤال | sualin adıyla | 5 | 3 |
| تقديره / أي | takdir ve izah | 148 | 29 |
| مقدّر / محذوف | hazif ve takdir | 22 | 11 |

Örnekler:

- *كأنه قيل* · `isaratul-icaz-arabi/sure-i-bakara/8/c021`: كأنه يقول: كونُ المنافق الرذيل إنساناً عجيبٌ؛ إذ الإنسان مكرّم، ليس من شأنه أن يتنزّل إلى هذه الدَرَكة من الخِسّة.
- *كأنه قيل* · `isaratul-icaz-arabi/sure-i-fatiha/siratallezine-enamte-aleyhim/c015`: وفي نسبتها شافعٌ له كأنه يقول: يا إلهي!
- *فإن قلت / قلت / قيل لك* · `isaratul-icaz-arabi/sure-i-fatiha/siratallezine-enamte-aleyhim/c019`: ⦁ إن قلت: مسالك الأنبياء متفاوتةٌ وعباداتُهم مختلفة؟
- *فإن قلت / قلت / قيل لك* · `isaratul-icaz-arabi/sure-i-bakara/25/mukaddime/c018`: ⦁ فإن قلت: لِمَ كانت الكائنات مغيَّرة موقّتة تخرُب ثم تصير يوم القيامة مؤبَّدة مُحكَمةً ثابتة؟
- *سؤال مقدر / جواب سؤال* · `isaratul-icaz-arabi/sure-i-bakara/14-15-ayetlerin-tefsiri/c038`: مع أن هذه الجملة بدلٌ بجهةٍ وتأكيدٌ بجهة، وهما من كمال الاتصال، وجوابُ سؤالٍ مقدَّر بجهة أخرى، وهو من كمال الانقطاع لخبَرية الجواب وإنشائية السؤال في الأغلب..
- *سؤال مقدر / جواب سؤال* · `isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/mesele-10/c005`: اعلم أن سلامة الكلام التي هي سببُ صحته وقوّته هي أن يكون الكلام بحيث يشير إلى المبادئ والدلائل، ويرمز إلى اللوازم والتوابع، وبقيود الموضوع والمحمول وكيفياتهما يومئ إلى …
- *تقديره / أي* · `isaratul-icaz-arabi/sure-i-bakara/21-22-ayetlerin-tefsiri/mukaddime/c266`: أي لا شريك له في ذاته ولا في صفاته ولا في أفعاله..
- *تقديره / أي* · `isaratul-icaz-arabi/sure-i-bakara/9-10-ayetlerin-tefsiri/c027`: كذلك إن الله تعالى قال لزجر المنافقين: ﴿ يُخَادِعُونَ اللّٰهَ ﴾ بدل «يخادعون النبيّ» لتحميقهم، أي كيف يخادعون النبيّ عليه السلام والنبيُّ مبلِّغٌ عن الله تعالى، فحيلتُهم …
- *مقدّر / محذوف* · `isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/mesele-10/c193`: وأن ﴿ كَصَيِّبٍ ﴾ لعدم مطابقته للمَمثّل يقتضي تقديرَ لازمٍ، والسكوتُ عن إظهار المقدَّر للإيجاز، والإيجاز في اللفظ لإطناب المعنى بإحالته على خيال السامع بالاستمداد من …
- *مقدّر / محذوف* · `isaratul-icaz-arabi/sure-i-bakara/5/c005`: منها الاستيناف، أيجوابٌ لثلاثة أسئلة مقدَّرة:

## 6. Hey'et ve harf

Bir lafzın neden öyle geldiği (usul özeti 4.3).

| Kalıp | İşi | Cümle | Birim |
|---|---|---:|---:|
| التنكير / التعريف | ta'rif ve tenkir | 27 | 12 |
| التقديم / التأخير | takdim ve te'hir | 24 | 16 |
| الحصر / القصر | hasr | 38 | 16 |
| العطف / الفصل | atf ve fasl | 28 | 15 |
| صيغة / الجمع / الإفراد | sîga | 11 | 9 |
| حرف … (الواو، الفاء، ثم، إنّ، قد) | harfin adıyla | 8 | 5 |

Örnekler:

- *التنكير / التعريف* · `isaratul-icaz-arabi/sure-i-bakara/9-10-ayetlerin-tefsiri/c061`: وفي تنوين التنكير إشارة إلى أنه في مكمن عميق لا يُرى حتى يُداوى.
- *التنكير / التعريف* · `isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/mesele-10/c226`: وأما تنكير ﴿ ظُلُمَاتٌ ﴾ فللاستنكار ولجهل المخاطب، فهو تأكيدُ ﴿ ظُلُمَاتٌ ﴾ .
- *التقديم / التأخير* · `isaratul-icaz-arabi/sure-i-fatiha/iyyake-nabudu/c011`: واعلم أن تقديم ﴿ اِيَّاكَ ﴾ للإخلاص الذي هو روحُ العبادة.
- *التقديم / التأخير* · `isaratul-icaz-arabi/sure-i-bakara/7/mukaddime-2/c070`: قدّم ﴿ وَعَلٰٓى اَبْصَارِهِمْ ﴾ ليوجّه العيونَ إلى عيونهم، إذ العين مرآةُ سرائر القلب.
- *الحصر / القصر* · `isaratul-icaz-arabi/sure-i-bakara/13/c036`: ثم لفظ «هُم» للحصر لردّ تبرئة أنفسهم، ودفع تسفيههم للمؤمنين الذي أشاروا إليه ب ﴿ كَمَٓا اٰمَنَ السُّفَهَٓاءُ ﴾ .
- *الحصر / القصر* · `isaratul-icaz-arabi/sure-i-fatiha/ve-iyyake-nestein/c007`: وفي حصر ﴿ اِيَّاكَ ﴾ إشارةٌ إلى أن بهذه النسبة الشريفة التي هي العبادةُ والخدمة له تعالى يترفَّعُ العبدُ عن التذلل للأسباب والوسائط، بل تصيرُ الوسائطُ خادمةً له وهو لا …
- *العطف / الفصل* · `isaratul-icaz-arabi/sure-i-bakara/6/c012`: ⦁ إن قلت: فلِمَ لم يعطف هنا كما عطف في ﴿ اِنَّ الْاَبْرَارَ لَف۪ي نَع۪يمٍ ❀ وَاِنَّ الْفُجَّارَ لَف۪ي جَح۪يمٍ ﴾ (الانفطار:١٣-١٤) ؟
- *العطف / الفصل* · `isaratul-icaz-arabi/sure-i-bakara/8/c003`: أي عطفُ ملخّص اثنتي عشرة آية على مآل آيتين؛ إذ لما افتتح التنزيلُ بثناء ﴿ ذٰلِكَ الْكِتَابُ ﴾ فاستتبع ثمراتِ ثنائه من مدح المؤمنين، فاستردف ذمَّ أضدادهم بسرّ «إنما تُعرف …
- *صيغة / الجمع / الإفراد* · `isaratul-icaz-arabi/sure-i-bakara/21-22-ayetlerin-tefsiri/mukaddime/c263`: أما الجمعُ فإشارة إلى نهاية جهالة المشركين وإيماء إلى التهكّم بهم.
- *صيغة / الجمع / الإفراد* · `isaratul-icaz-arabi/sure-i-bakara/8/c037`: وفي الدعوى إيماءٌ منهم بصيغة الماضي إلى: «إنّا معاشرَ أهل الكتاب قد آمنا قبلُ فكيف لا نؤمن الآن»..
- *حرف … (الواو، الفاء، ثم، إنّ، قد)* · `isaratul-icaz-arabi/sure-i-bakara/4/c046`: اعلم أنه ما من كلمة في التنزيل يأبى عنها مكانُها، أو لم يرضَ بها، أو كان غيرُها أولى به.
- *حرف … (الواو، الفاء، ثم، إنّ، قد)* · `isaratul-icaz-arabi/sure-i-bakara/5/c026`: كما أن لفظ «بارَزَ» يفتح لك معركة الحرب، ولفظ «ثمرة» في الآية يفتح لك باب الجنة، وقِس!

## 7. Garaz ve toplayış

Kayıtların asıl maksada bağlanışı (usul özeti 3.2; Muhâkemât Dördüncü Mes'ele).

| Kalıp | İşi | Cümle | Birim |
|---|---|---:|---:|
| الغرض / المقصود / المقصد | asıl maksat | 71 | 22 |
| المقام / يقتضي / مقتضى | makam ve iktiza | 90 | 22 |
| فتأمل / فانظر / وقس | okura bırakılan | 99 | 22 |
| الحاصل / فالحاصل | toplayış | 22 | 9 |

Örnekler:

- *الغرض / المقصود / المقصد* · `isaratul-icaz-arabi/sure-i-bakara/7/mukaddime-2/c009`: وهمتُه بمقدار أهمية المقصد الذي يشتغل به.
- *الغرض / المقصود / المقصد* · `isaratul-icaz-arabi/sure-i-bakara/8/c001`: وجه النظم: أنه كما يُعطَف المفردُ على المفردِ للاشتراك في الحُكم، والجملةُ على الجملةِ للاتحاد في المقصِد؛ كذلك قد تُعطَف القصةُ على القصة للتناسب في الغَرَض.
- *المقام / يقتضي / مقتضى* · `isaratul-icaz-arabi/sure-i-bakara/9-10-ayetlerin-tefsiri/c054`: وفي الرابعة: أعني جملة ﴿ ف۪ي قُلُوبِهِمْ مَرَضٌۙ ﴾ هو أنَّ سَوقها يفيد أنهم لمّا لَم يعملوا بمقتضى المحاكمة العقلية والشعورِ الحسيّ ظهر أن في روحهم مرضاً فلا أقلَّ من أن …
- *المقام / يقتضي / مقتضى* · `isaratul-icaz-arabi/sure-i-fatiha/ve-iyyake-nestein/c003`: ولأن مقام العيان أعلى وأجلُّ من مقام البرهان..
- *فتأمل / فانظر / وقس* · `isaratul-icaz-arabi/sure-i-fatiha/rabbi/c003`: لو تأملتَ في الكائنات لرأيتَها كبني آدمَ طوائفَ وقبائلَ يشتغل كلٌّ منفرداً ومجتمعاً بوظيفته التي عيَّنَها له صانِعُه ساعياً مُجدّاً مطيعا لقانون خالقه.
- *فتأمل / فانظر / وقس* · `isaratul-icaz-arabi/sure-i-bakara/6/c048`: فتأمل!
- *الحاصل / فالحاصل* · `isaratul-icaz-arabi/sure-i-bakara/21-22-ayetlerin-tefsiri/mukaddime/c103`: الحاصل: أنَّ الطبيعة صنعةُ الله تعالى وشريعتُه الفطرية.
- *الحاصل / فالحاصل* · `isaratul-icaz-arabi/sure-i-bakara/4/c120`: وأما البرهان السادس الملوّح: فهو عدمُ تناهي استعدادات البشر؛ نعم، إن تصوراتِ البشر وأفكارَه التي لا تتناهى، المتولدةَ من آماله الغير المتناهية، الحاصلةِ من ميوله الغيرِ …

## 8. İhtimal ve çekince

Hükmün kuvveti; tek vecih mi, vecihlerden biri mi.

| Kalıp | İşi | Cümle | Birim |
|---|---|---:|---:|
| يحتمل / ويحتمل | ihtimal | 11 | 7 |
| لعل / ولا يبعد / يمكن | imkân | 141 | 25 |
| أو … (وجهان، وجوه) | birden çok vecih | 44 | 19 |

Örnekler:

- *يحتمل / ويحتمل* · `isaratul-icaz-arabi/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-06/c054`: والثالث: أنهم يقولون: إن بعض ظواهر القرآن أميَلُ إلى خلاف الدليل العقلي، فيَحتمل خلافَ الواقع، وهو مخالفٌ لصدقه.
- *يحتمل / ويحتمل* · `isaratul-icaz-arabi/sure-i-bakara/4/c004`: فلمراعاة هذه الطبقات، ولمجاورة هذه الأعصار، ليستفيد مخاطَبُ كلِ نوعٍ ما قُدِّرَ له من حصته، حَذَف القرآنُ في كثيرٍ للتعميم والتوزيع، وأطلق في كثيرٍ للتشميل والتقسيم، …
- *لعل / ولا يبعد / يمكن* · `isaratul-icaz-arabi/sure-i-bakara/3/c077`: ولا يفور من الطبقة السفلى إلى العليا إلّا أصداءالاختلال، وصياحُ الحسد، وأنينُ الحقد والنفرة بدلاً عن الاحترام والإطاعة والتحبب.
- *لعل / ولا يبعد / يمكن* · `isaratul-icaz-arabi/sure-i-fatiha/el-hamdu/c004`: فكأن ذكرَه تصوّرٌ للعلة الغائية..
- *أو … (وجهان، وجوه)* · `isaratul-icaz-arabi/sure-i-bakara/30/mukaddime/c026`: ثم إن نظم مآل هذه الآية بسابقها من أربعة وجوه:
- *أو … (وجهان، وجوه)* · `isaratul-icaz-arabi/sure-i-bakara/31-33-ayetlerin-tefsiri/mukaddime/c018`: ثم إن لهذه الآية أيضاً الوجوه الثلاثة النظمية:

## 9. Temsil ve benzetme

Soyut bağın misalle gösterilmesi (usul özeti 2.5; Muhâkemât Üçüncü ve Yedinci Mes'ele).

| Kalıp | İşi | Cümle | Birim |
|---|---|---:|---:|
| كما / مثل / كأن | benzetme | 157 | 33 |
| مثال / تمثيل | misal ve temsil | 146 | 26 |

Örnekler:

- *كما / مثل / كأن* · `isaratul-icaz-arabi/sure-i-bakara/5/c019`: فمن العهدالذِكْريّ ينفتح بابٌ إلى العهد الخارجيّ، ومن العهد الخارجي ينتقل إلى امتيازهم، وينظر إلى تلألئهم في نوع البشر كأنه مَن رفعَ رأسَه وفتح عينيه لا يتراءى له إلَّا …
- *كما / مثل / كأن* · `isaratul-icaz-arabi/sure-i-bakara/8/c021`: كأنه يقول: كونُ المنافق الرذيل إنساناً عجيبٌ؛ إذ الإنسان مكرّم، ليس من شأنه أن يتنزّل إلى هذه الدَرَكة من الخِسّة.
- *مثال / تمثيل* · `isaratul-icaz-arabi/sure-i-bakara/21-22-ayetlerin-tefsiri/mukaddime/c073`: فإذ تفهّمت ما في هذا المثال ورأيت عظمتَه مع صِغَره، ووسعتَه مع ضيقِه؛ فارفع رأسك وانظر في الكائنات ترَ وضوحَ «دليل العناية» وظهورَه بمقدار درجة وُسعة الكائنات.
- *مثال / تمثيل* · `isaratul-icaz-arabi/sure-i-fatiha/bismillahi/c001`: أما «الاسم» فاعلم أن لله أسماءً ذاتية، وأسماءً فعلية متنوعة كالغفار والرزاق والمحيي والمميت وأمثالِها.

## 10. Bir lafzın ele alınışı: üç paragraf

Üçüncü vecihte bir lafzı "وأما ﴿…﴾" ile açan kısa paragraflar, farklı birimlerden, bütün olarak. Bir paragraf: lafız, hey'eti ya da kaydı, onun mânâya kattığı ve çoğu zaman garaza bağlanışı.

`isaratul-icaz-arabi/sure-i-bakara/21-22-ayetlerin-tefsiri/mukaddime/c179` … (2 cümle)

> وأما ﴿ النَّاسُ ﴾ فإشارة -بحكم تلميح الوصفية الأصلية- إلى العتاب، أي «أيها الناس كيف تنسون الميثاق الأزلي؟» وأيضاً إلى العذر، أي «أيها الناس لابد أن يكون قصوركم عن السهو والنسيان لا بالعمد والجد!»

`isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/mesele-10/c302` … (1 cümle)

> وأما ﴿ اِنَّ ﴾ فمع إشارتها إلى أن هذا الحكم من الحقائق الراسخة، رمزٌ إلى عظمة المسألة ووُسعَتها ودقّتها، وعجزِ البشر وضعفه وقصوره عنها، المولِّدة للأوهام المُنتجة للتردّد في اليقينيات.

`isaratul-icaz-arabi/sure-i-bakara/23-24-ayetlerin-tefsiri-nubuvvet-hakkinda/mesele-07/c209` … (3 cümle)

> وأما ﴿ وَقُودُهَا النَّاسُ وَالْحِجَارَةُ ﴾ فالغرض كما مرَّ آنفاً الترهيبُ، والترهيب يؤكَّد بالتهويل والتشديد. فهوّلَ بلفظ ﴿ النَّاسُ ﴾ كما قرعَ به، وشدّد ب ﴿ وَالْحِجَارَةُ ﴾ كما وبّخ بها. أي ما ترجون منه النفعَ والنجاة وهو الأصنامُ يصير آلةً لتعذيبكم.

