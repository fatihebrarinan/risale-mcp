"""Hadis kitaplarının kaydı: künyede geçen adlar, Arapça adlar, derlemdeki karşılıklar, bölümler.

Risale'ye bağlı değildir: ileride kurulacak `hadis` profili de bu kayda dayanır. Kimlik (`Book.id`) değişmez.

- `pattern` künyede kitabı tanır, `normalize_name` biçimine uygulanır (küçük harf, işaretsiz, kesme ve tire yok).
- `api`: Hadith API derlemi; `sanadset`: Sanadset'teki adlar. İkisi de yoksa kitap derlemde yoktur, künyesi yine durur.
- `kind`: hadis (rivayet kitabı), serh, tefsir, ikincil (rivayeti başkasından derleyen ya da kaynak gösteren), diger.
- `AUTHORS`: künyede yalnız müellif adı geçince varsayılan kitap.
- `SECTIONS`: Kütüb-i Sitte ve Muvatta'nın kitap adları -> Hadith API bölümü. Künyedeki "Edeb: 96"nın sayısı bâbdır,
  Hadith API'de bâb yoktur (`hadis_kunye` başı); kitap adı ise bölümle tutar, güvenilir olan odur.
"""

import re
import unicodedata
from dataclasses import dataclass

_TURKISH = str.maketrans({"ı": "i", "İ": "i", "I": "i"})


def normalize_name(text: str) -> str:
    return _fold(text)[0]


def _fold(text: str) -> tuple[str, list[int]]:
    """Küçük harf, işaretsiz, kesme ve tiresiz biçim ve her harfin özgün konumu. Sayı aralığının tiresi kalır."""
    out, where = [], []
    for at, ch in enumerate(text):
        if ch in "'’‘ʼ`´­":
            continue
        if ch in "-‑–":
            if at and text[at - 1].isdigit():
                out.append("-")
                where.append(at)
            continue
        base = unicodedata.normalize("NFKD", ch.translate(_TURKISH))
        base = "".join(c for c in base if not unicodedata.combining(c)).lower()
        for c in base:
            out.append(c)
            where.append(at)
    return "".join(out), where


@dataclass(frozen=True)
class Book:
    id: str
    title: str
    pattern: str
    ar: str = ""
    kind: str = "hadis"
    api: str = ""
    sanadset: tuple[str, ...] = ()


BOOKS = (
    # Önce uzun ve özel adlar: düzen arama sırasıdır.
    Book("tarih-kebir", "et-Târîhu'l-Kebîr", r"((el ?)?buhari, ?)?(et ?)?tarih\w* ?kebir", "التاريخ الكبير", "diger"),
    Book("tarih-sagir", "et-Târîhu's-Sağîr", r"((el ?)?buhari, ?)?(et ?)?tarih\w* ?sagir", "التاريخ الصغير", "diger"),
    Book("edebul-mufred", "el-Edebü'l-Müfred", r"((el ?)?buhari, ?)?(el ?)?edeb\w* ?mufred", "الأدب المفرد", sanadset=("الأدب المفرد للبخاري",)),
    Book("fethur-rabbani", "el-Fethu'r-Rabbânî", r"((es ?)?saati, ?)?(el ?)?feth\w* ?rabbani|(es ?)?saati", "الفتح الرباني", "ikincil"),
    Book("isabe", "el-İsâbe", r"((ibn\w* ?hacer|(el ?)?askalani), ?)?(el ?)?isabe\w*( fi temyiz\w*)?", "الإصابة في تمييز الصحابة", "diger"),
    Book("metalib", "el-Metâlibü'l-Âliye", r"((ibn\w* ?hacer|(el ?)?askalani), ?)?(el ?)?metalib\w* ?aliye", "المطالب العالية", "ikincil", sanadset=("المطالب العالية بزوائد المسانيد الثمانية لابن حجر",)),
    Book("zadul-mead", "Zâdü'l-Meâd", r"(ibn\w* ?(kayyim|el ?kayyim)( el ?cevziyye)?, ?)?zad\w* ?mead|ibn\w* ?kayyim( el ?cevziyye)?", "زاد المعاد", "diger"),
    Book("camiul-usul", "Câmiu'l-Usûl", r"((ibn\w* ?esir( el ?cizri)?), ?)?cami\w* ?usul", "جامع الأصول", "ikincil"),
    Book("nihaye", "en-Nihâye fî Garîbi'l-Hadîs", r"((ibn\w* ?esir( el ?cizri)?), ?)?(en ?)?nihaye fi\w*[^;,\d]*|ibn\w* ?esir( el ?cizri)?", "النهاية في غريب الحديث", "diger"),
    Book("kurtubi", "el-Câmi' li-Ahkâmi'l-Kur'ân", r"(el ?)?kurtubi", "الجامع لأحكام القرآن", "tefsir"),
    Book("nazmul-mutenasir", "Nazmü'l-Mütenâsir", r"((el ?)?kettani, ?)?nazm\w* ?mutenasir[^;,\d]*|(el ?)?kettani", "نظم المتناثر", "ikincil"),
    Book("meydani", "Mecmaü'l-Emsâl", r"(ebul ?fadl (ahmed [^;,]*)?el ?meydani, ?)?mecma\w* ?emsal[^;\d]*?(el ?meydani)?|(el ?)?meydani", "مجمع الأمثال", "diger"),
    Book("isaa", "el-İşâa", r"((el ?)?berzenci, ?)?(el ?)?isaa\w*[^;,\d]*|(el ?)?berzenci", "الإشاعة لأشراط الساعة", "ikincil"),
    Book("tacul-arus", "Tâcü'l-Arûs", r"((ez ?)?zebidi, ?)?tac\w* ?arus", "تاج العروس", "diger"),
    Book("mecmuatul-ahzab", "Mecmûatü'l-Ahzâb", r"((seyh )?(ahmed )?gumushanevi, ?)?mecmua\w* ?ahzab", "مجموعة الأحزاب", "diger"),
    Book("edebud-dunya", "Edebü'd-Dünyâ ve'd-Dîn", r"((ali )?(el ?)?maverdi, ?)?edeb\w* ?dunya\w*( ?veddin)?|(ali )?(el ?)?maverdi", "أدب الدنيا والدين", "diger"),
    Book("enbiya-kastalani", "el-Mevâhibü'l-Ledünniyye", r"((el ?)?kastalani, ?)?(el ?)?mevahib\w*( ?ledunni\w*)?|(el ?)?kastalani", "المواهب اللدنية", "diger"),
    Book("sire-ibn-hisam", "es-Sîretü'n-Nebeviyye", r"ibn\w* ?hisam(, ?(es ?)?sire\w*)?", "السيرة النبوية لابن هشام", "diger"),
    Book("muntehab", "Muntehabü Kenzi'l-Ummâl", r"(ali bin husamuddin, ?)?muntehab\w*[^;,\d]*|ali bin husamuddin", "منتخب كنز العمال", "ikincil"),
    Book("acurri", "eş-Şerîa", r"(el ?)?acur+i", "الشريعة", "diger"),
    Book("kandehlevi", "Hayâtü's-Sahâbe", r"(el ?)?kandehlevi", "حياة الصحابة", "diger"),
    Book("bikai", "Nazmü'd-Dürer", r"(el ?)?bikai", "نظم الدرر", "tefsir"),
    Book("tarih-taberi", "Târîhu'l-Ümem ve'l-Mülûk", r"((et ?)?taberi, ?)?tarih\w* ?umem\w*( ?vel ?muluk)?", "تاريخ الأمم والملوك", "diger"),
    Book("ezkar", "el-Ezkâr", r"((en ?)?nevevi, ?)?(el ?)?ezkar", "الأذكار", "ikincil"),
    Book("ithaf", "İthâfü's-Sâde", r"((ez ?)?zebidi, ?)?ithaf\w*", "إتحاف السادة المتقين", "serh"),
    Book("mizan-sarani", "el-Mîzânü'l-Kübrâ", r"(el ?)?mizan\w* ?kubra( ?sarani)?", "الميزان الكبرى", "diger"),
    Book("anka", "Ankâü Muğrib", r"anka\w* ?magrib( ?muhyiddini arabi)?", "عنقاء مغرب", "diger"),
    Book("nehcul-belaga", "Nehcü'l-Belâğa", r"nehc\w* ?belaga( ?imami ali)?", "نهج البلاغة", "diger"),
    Book("cevheret", "Şerhu Cevhereti't-Tevhîd", r"serh\w* ?cevhere\w*( ?tevhid)?", "شرح جوهرة التوحيد", "diger"),
    Book("esrar-merfua", "el-Esrârü'l-Merfûa", r"(el ?)?esrar\w* ?merfua", "الأسرار المرفوعة", "ikincil", sanadset=("الأسرار المرفوعة في الأخبار الموضوعة",)),
    Book("keskul", "el-Keşkûl", r"(el ?)?keskul", "الكشكول", "diger"),
    Book("mecmuu-fetava", "Mecmûu'l-Fetâvâ", r"(ibn\w* ?teymiye, ?)?mecmuu? ?fetava", "مجموع الفتاوى", "diger"),
    Book("tarihul-hulefa", "Târîhu'l-Hulefâ", r"((es ?)?suyuti, ?)?tarih\w* ?hulefa", "تاريخ الخلفاء", "diger"),
    Book("envar-muhammediyye", "el-Envârü'l-Muhammediyye", r"((yusuf )?(en ?)?nebhani, ?)?(el ?)?envar\w* ?muhammedi\w*[^;,\d]*", "الأنوار المحمدية", "diger"),
    Book("hallal", "el-Hallâl (eseri anılmamış)", r"(el ?)?hallal", "", "diger"),
    Book("curcani", "el-Cürcânî (eseri anılmamış)", r"(el ?)?curcani", "", "diger"),
    Book("magribi", "el-Mağribî (eseri anılmamış)", r"(el ?)?magribi", "", "ikincil"),
    Book("isfehani", "el-İsfehânî (eseri anılmamış)", r"(el ?)?isfehani", "", "diger"),
    Book("nevadir", "Nevâdirü'l-Usûl", r"((el ?)?hakim et ?tirmizi, ?)?nevadir\w*( ?usul)?|(el ?)?hakim et ?tirmizi", "نوادر الأصول", "ikincil"),
    Book("musned-firdevs", "Müsnedü'l-Firdevs", r"(ed ?)?deylemi|(musnedul|musned ul |musned[ -]?i )firdevs|firdevs", "مسند الفردوس", "ikincil"),
    Book("zuheru-firdevs", "Zühûrü'l-Firdevs", r"zuher\w* ?firdevs", "زهر الفردوس", "ikincil"),
    Book("musned-ebu-hanife", "Müsned (Ebû Hanîfe)", r"ebu hanife, ?(el ?)?musned", "مسند أبي حنيفة", sanadset=("مسند أبي حنيفة رواية أبي نعيم",)),
    Book("musned-bezzar", "Müsned (Bezzâr)", r"bezzar(, ?(el ?)?musned)?", "البحر الزخار بمسند البزار", sanadset=("البحر الزخار بمسند البزار",)),
    Book("musned-ebu-yala", "Müsned (Ebû Ya'lâ)", r"ebu ?yala(, ?(el ?)?musned)?", "مسند أبي يعلى الموصلي", sanadset=("مسند أبي يعلى الموصلي",)),
    Book("musned-tayalisi", "Müsned (Tayâlisî)", r"tayalisi(, ?(el ?)?musned)?", "مسند أبي داود الطيالسي", sanadset=("مسند أبي داود الطيالسي",)),
    Book("musned-sihab", "Müsnedü'ş-Şihâb", r"(el ?)?kudai|musnedussihab", "مسند الشهاب", sanadset=("مسند الشهاب",)),
    Book("fedailus-sahabe-ahmed", "Fedâilü's-Sahâbe (Ahmed b. Hanbel)", r"ahmed (bin|ibni|ibn|b\.) ?hanbel, ?fedail\w*", "فضائل الصحابة"),
    Book("zuhd-ahmed", "ez-Zühd (Ahmed b. Hanbel)", r"ahmed (bin|ibni|ibn|b\.) ?hanbel, ?(ez ?)?zuhd", "الزهد لأحمد بن حنبل", sanadset=("الزهد لأحمد بن حنبل",)),
    Book("zuhd-ibnul-mubarek", "ez-Zühd (İbnü'l-Mübârek)", r"(ez ?)?zuhd\b[^;]{0,6}ibn\w*[ ]?mubarek|ibnul ?mubarek(, ?(ez ?)?zuhd)?", "الزهد والرقائق لابن المبارك", sanadset=("الزهد والرقائق لابن المبارك",)),
    Book("zuhd-beyhaki", "ez-Zühd (Beyhakî)", r"(el ?)?beyhaki, ?(ez ?)?zuhd", "الزهد الكبير للبيهقي", sanadset=("الزهد الكبير للبيهقي",)),
    Book("hilye", "Hilyetü'l-Evliyâ", r"ebu ?nuaym, ?hilye\w*|hilye\w*|ebu ?nuaym, ?(el ?)?hilye", "حلية الأولياء", sanadset=("حلية الأولياء لأبي نعيم",)),
    Book("delail-ebu-nuaym", "Delâilü'n-Nübüvve (Ebû Nuaym)", r"ebu ?nuaym, ?delail\w*", "دلائل النبوة لأبي نعيم", sanadset=("دلائل النبوة لأبي نعيم",)),
    Book("delail-beyhaki", "Delâilü'n-Nübüvve (Beyhakî)", r"(el ?)?beyhaki, ?delail\w*|delail\w*", "دلائل النبوة للبيهقي", sanadset=("دلائل النبوة للبيهقي",)),
    Book("suab", "Şuabü'l-Îmân", r"((el ?)?beyhaki, ?)?suab\w*", "شعب الإيمان", sanadset=("شعب الإيمان للبيهقي",)),
    Book("sunen-beyhaki", "es-Sünenü'l-Kübrâ (Beyhakî)", r"(el ?)?beyhaki(, ?(es ?)?sunen\w*)?|sunen\w*[ -]?beyhaki", "السنن الكبرى للبيهقي", sanadset=("السنن الكبرى للبيهقي",)),
    Book("mustedrek", "el-Müstedrek", r"((el ?)?hakim, ?)?(el ?)?mustedrek\w*( ?hakim)?|(el ?)?hakim\b", "المستدرك على الصحيحين", sanadset=("المستدرك على الصحيحين",)),
    Book("sahih-ibn-hibban", "Sahîh-i İbn Hibbân", r"(sahihi? ?)?ibn\w* ?hibban(, ?sahih)?", "صحيح ابن حبان", sanadset=("صحيح ابن حبان",)),
    Book("sahih-ibn-huzeyme", "Sahîh-i İbn Huzeyme", r"ibn\w* ?huzeyme", "صحيح ابن خزيمة", sanadset=("صحيح ابن خزيمة",)),
    Book("mucemul-evsat", "el-Mu'cemü'l-Evsat", r"((et ?)?taberani, ?)?(el ?)?mucem\w* ?evsat", "المعجم الأوسط", sanadset=("المعجم الأوسط للطبراني",)),
    Book("mucemus-sagir", "el-Mu'cemü's-Sağîr", r"((et ?)?taberani, ?)?(el ?)?mucem\w* ?sagir", "المعجم الصغير", sanadset=("المعجم الصغير للطبراني",)),
    Book("mucemul-kebir", "el-Mu'cemü'l-Kebîr", r"((et ?)?taberani, ?)?(el ?)?mucem\w* ?kebir|mucemut ?taberani|(et ?)?taberani", "المعجم الكبير", sanadset=("المعجم الكبير للطبراني",)),
    Book("keşfu", "Keşfü'l-Hafâ", r"((el ?)?acluni, ?)?kesf\w* ?hafa\w*|(el ?)?acluni", "كشف الخفاء", "ikincil"),
    Book("kunuzul-hakaik", "Künûzü'l-Hakâik", r"((el ?)?munavi+, ?)?kunuz\w* ?hakaik", "كنوز الحقائق", "ikincil"),
    Book("feyzul-kadir", "Feyzü'l-Kadîr", r"((el ?)?munav[iî]+, ?)?feyz\w* ?kadir|(el ?)?munavi+", "فيض القدير", "serh"),
    Book("kenzul-ummal", "Kenzü'l-Ummâl", r"((ali )?el ?muttaki( el ?hindi)?, ?)?kenz\w* ?um+al|(ali )?el ?muttaki( el ?hindi)?|el ?hindi", "كنز العمال", "ikincil"),
    Book("mecmauz-zevaid", "Mecmaü'z-Zevâid", r"((el ?)?heysemi, ?)?mecm[ae]+u?\w* ?zevaid|(el ?)?heysemi", "مجمع الزوائد", "ikincil"),
    Book("fetava-hadisiye", "el-Fetâvâ'l-Hadîsiye", r"(el ?)?fetav\w* ?hadisiye", "الفتاوى الحديثية", "diger"),
    Book("ihya", "İhyâu Ulûmi'd-Dîn", r"((imami? ?)?(el ?)?gazal[iî], ?)?ihya\w*( ulum\w*( ?din)?)?|(imami? ?)?(el ?)?gazal[iî]", "إحياء علوم الدين", "diger"),
    Book("sifa", "eş-Şifâ", r"(kadi ?iyad?z?|kadi ?iyaz|kad[ -]?i ?iyaz)(, ?(es ?)?sifa)?|(es ?)?sifa\b(?!\w)", "الشفا بتعريف حقوق المصطفى", "ikincil", sanadset=("الشفا بأحوال المصطفى للقاضي عياض",)),
    Book("serhus-sifa-hafaci", "Nesîmü'r-Riyâz (Hafâcî)", r"(el ?)?hafac[iî](, ?serh\w* ?sifa)?", "نسيم الرياض", "serh"),
    Book("serhus-sifa-kari", "Şerhu'ş-Şifâ (Ali el-Kârî)", r"(a?li\w* ?(el ?)?kar[iî]|aliyyu\w* ?kar[iî])(, ?serh\w* ?sifa)?", "شرح الشفا", "serh"),
    Book("camius-sagir", "el-Câmiu's-Sağîr", r"((es ?)?suyuti, ?)?(el ?)?camiu?\w* ?sagir|(sahihu? )?cami\w* ?sagir", "الجامع الصغير", "ikincil"),
    Book("fethul-kebir", "el-Fethü'l-Kebîr", r"(el ?)?feth\w* ?kebir", "الفتح الكبير", "ikincil"),
    Book("durer", "ed-Dürerü'l-Müntesire", r"(ed ?)?durer\w* ?muntesire", "الدرر المنتثرة", "ikincil"),
    Book("hasais", "el-Hasâisü'l-Kübrâ", r"((es ?)?suyuti, ?)?(el ?)?hasais\w*", "الخصائص الكبرى", "ikincil"),
    Book("durrul-mensur", "ed-Dürrü'l-Mensûr", r"((es ?)?suyuti, ?)?(ed ?)?durr\w* ?mensur", "الدر المنثور", "tefsir"),
    Book("suyuti", "Süyûtî (eseri anılmamış)", r"(es ?)?suyuti", "", "ikincil"),
    Book("sirat-halebi", "es-Sîretü'l-Halebiye", r"((burhaneddin )?(el ?)?halebi, ?)?(es ?)?sire\w* ?halebiye|(burhaneddin )?(el ?)?halebi", "السيرة الحلبية", "diger"),
    Book("bidaye", "el-Bidâye ve'n-Nihâye", r"(ibn\w* ?kesir, ?)?(el ?)?bidaye\w*( ?ven?nihaye)?", "البداية والنهاية", "diger"),
    Book("tefsir-ibn-kesir", "Tefsîrü'l-Kur'âni'l-Azîm", r"ibn\w* ?kesir(, ?(tefsir\w*|muhtasar\w*)[^;,\d]*)?", "تفسير ابن كثير", "tefsir"),
    Book("fethul-bari", "Fethü'l-Bârî", r"((ibn\w* ?hacer|(el ?)?askalani), ?)?feth\w* ?bari", "فتح الباري", "serh"),
    Book("ibn-hacer", "İbn Hacer (eseri anılmamış)", r"ibn\w* ?hacer|(el ?)?askalani", "", "ikincil"),
    Book("tuhfe", "Tuhfetü'l-Ahvezî", r"((el ?)?mubarekfor[iî], ?)?tuhfe\w* ?ahvezi|(el ?)?mubarekfor[iî]", "تحفة الأحوذي", "serh"),
    Book("mevzuat-ibnul-cevzi", "el-Mevzûât", r"(ibn\w* ?cevzi, ?)?(el ?)?mevzuat\w*", "الموضوعات", "ikincil", sanadset=("الموضوعات الكبرى لابن الجوزي",)),
    Book("ibnul-cevzi", "İbnü'l-Cevzî (eseri anılmamış)", r"ibn\w* ?cevzi", "", "ikincil"),
    Book("tergib", "et-Terğîb ve't-Terhîb", r"((el ?)?munziri, ?)?(et ?)?tergib\w*( ?vet?terhib)?|(el ?)?munziri", "الترغيب والترهيب", "ikincil"),
    Book("mirkat", "Mişkâtü'l-Mesâbîh", r"((el ?)?elbani, ?|(et ?)?tebrizi, ?)?miskat\w*( ?mesabih)?|(et ?)?tebrizi", "مشكاة المصابيح", "ikincil"),
    Book("elbani", "el-Elbânî (eseri anılmamış)", r"(el ?)?elbani", "", "ikincil"),
    Book("temhid", "et-Temhîd", r"(ibn\w* ?abd\w*ber, ?)?(et ?)?temhid|ibn\w* ?abd\w*ber", "التمهيد لابن عبد البر", "serh", sanadset=("التمهيد لابن عبد البر",)),
    Book("tarih-bagdad", "Târîhu Bağdâd", r"((el ?)?hatib\w*( el ?bagdadi)?, ?)?tarih\w* ?bagdad|(el ?)?hatib\w*( el ?bagdadi)?", "تاريخ بغداد", "diger", sanadset=("تاريخ بغداد للخطيب البغدادي",)),
    Book("tecrid", "Tecrîd-i Sarîh Tercemesi", r"tecrid\w*( ?sarih)?( ?tercemesi)?( kilavuzu)?", "التجريد الصريح", "ikincil"),
    Book("cemul-fevaid", "Cem'u'l-Fevâid", r"cem\w* ?fevaid", "جمع الفوائد", "ikincil"),
    Book("et-tac", "et-Tâc", r"((mansur )?ali nasif, ?)?(et ?)?tac\b( ?(el ?)?camii?[^;,\d]*)?|mansur ali nasif", "التاج الجامع للأصول", "ikincil"),
    Book("serhus-sunne", "Şerhu's-Sünne", r"serh\w* ?sunne", "شرح السنة", sanadset=("شرح السنة",)),
    Book("kamil", "el-Kâmil fi'd-Duafâ", r"(el ?)?kamil fi\w* ?duafa|ibn\w* ?ad[iy]+\b", "الكامل في ضعفاء الرجال", "ikincil", sanadset=("الكامل في ضعفاء الرجال",)),
    Book("ramuz", "Râmûzü'l-Ehâdîs", r"ramuz\w* ?ehadis", "راموز الأحاديث", "ikincil"),
    Book("muhtar", "Muhtârü'l-Ehâdîs", r"muhtar\w* ?ehadis", "مختار الأحاديث", "ikincil"),
    Book("buluğ", "Bülûğu'l-Merâm", r"bulug\w* ?meram", "بلوغ المرام", "ikincil"),
    Book("hucce", "Hüccetullâh ale'l-Âlemîn", r"((yusuf )?(en ?)?nebhani, ?)?huccet\w*[^;,\d]*|(yusuf )?(en ?)?nebhani", "حجة الله على العالمين", "ikincil"),
    Book("sunen-darimi", "Sünen-i Dârimî", r"(ed ?)?dar[iîı]m[iî]", "سنن الدارمي", sanadset=("سنن الدارمي",)),
    Book("muvatta", "Muvatta'", r"(imam[ -]?i? ?malik, ?)?muvatta", "الموطأ", api="malik"),
    Book("bukhari", "Sahîh-i Buhârî", r"(sahihi? ?)?buhari", "صحيح البخاري", api="bukhari"),
    Book("muslim", "Sahîh-i Müslim", r"(sahihi? ?)?muslim\b", "صحيح مسلم", api="muslim"),
    Book("abudawud", "Sünen-i Ebû Dâvûd", r"(sunen ?i? ?)?ebu ?davu?d", "سنن أبي داود", api="abudawud"),
    Book("tirmidhi", "Sünen-i Tirmizî", r"(sahihi? |sunen ?i? ?)?tirmizi", "جامع الترمذي", api="tirmidhi"),
    Book("nasai", "Sünen-i Nesâî", r"(sunen ?i? ?)?nes[ae]i", "سنن النسائي", api="nasai"),
    Book("ibnmajah", "Sünen-i İbn Mâce", r"ibn\w* ?mace", "سنن ابن ماجه", api="ibnmajah"),
    Book("musned-ahmed", "Müsned (Ahmed b. Hanbel)", r"((imam[ -]?i? ?)?ahmed (bin|ibni|ibn|b\.) ?hanbel, ?)?(el ?)?musned\b|(imam[ -]?i? ?)?ahmed (bin|ibni|ibn|b\.) ?hanbel", "مسند أحمد بن حنبل", sanadset=("مسند أحمد بن حنبل",)),
)
BY_ID = {b.id: b for b in BOOKS}
MENTION = re.compile("|".join(f"(?P<b{i}>(?:{b.pattern}))" for i, b in enumerate(BOOKS)))


def _table(text: str) -> tuple[tuple[re.Pattern, int], ...]:
    """"ad=bölüm" satırları: ad `normalize_name` biçiminde düzenli ifadedir; baştaki harf-i tarif ve "kitabu" atlanır."""
    rows = (line.rsplit("=", 1) for line in text.split() if line)
    return tuple((re.compile(rf"(kitabu?[lszdtrn]?)?(e[lsdztrn])?(?:{name})"), int(n)) for name, n in rows)


SECTIONS = {
    "bukhari": _table(r"""
        bed\w*vahy=1 iman=2 ilim=3 vudu\w*=4 gusul=5 hayz=6 teyemmum=7 salat=8 mevak[iî]t\w*=9 ezan=10 cuma=11 havf=12
        iydeyn|ideyn=13 vitir|vitr=14 istiska=15 kusuf=16 sucud\w*=17 taksir\w*=18 teheccud=19 fadl\w*salat\w*=20
        amel\w*(fi\w*)?salat|amel=21 sehv=22 cenaiz=23 zekat=24 hac=25 umre=26 muhsar=27 ceza\w*sayd=28
        fedail\w*medine=29 savm=30 teravih=31 kadr|leyle\w*kadr=32 itikaf=33 buyu=34 selem=35 sufa=36 icare=37
        havale=38 kefale=39 vekale=40 hars|muzaraa=41 musakat=42 istikraz=43 husumat=44 lukata=45 mezalim=46
        sirket=47 rehin=48 itk=49 mukatep=50 hibe=51 sehadat=52 sulh=53 surut=54 vesaya=55 cihad=56 humus|fardulhumus=57
        cizye=58 bed\w*halk=59 enbiya|ehadisulenbiya=60 menakib=61 ashab|fe?[dz]ail\w*sahabe|fa?e?dail\w*ashab\w*=62
        menakib\w*ensar=63 megazi|magazi=64 tefsir\w*=65 fedail\w*kuran=66 nikah=67 talak=68 nafakat=69 etime=70
        akika=71 zebaih=72 edahi=73 esribe=74 merda=75 tib=76 libas=77 edeb=78 istizan=79 daavat|deavat=80 rikak=81
        kader=82 eyman\w*=83 keffarat=84 feraiz=85 hudud=86 diyat=87 istitabe\w*=88 ikrah=89 hiyel=90 tabir=91 fiten=92
        ahkam=93 temenni=94 ahbar\w*=95 itisam=96 tevhid=97"""),
    "muslim": _table(r"""
        mukaddime=0 iman=1 taharet=2 hayz=3 salat=4 mesacid=5 salat\w*musafirin=6 cuma=7 ideyn|iydeyn=8 istiska=9
        kusuf=10 cenaiz=11 zekat=12 siyam|savm=13 itikaf=14 hac=15 nikah=16 rada=17 talak=18 lian=19 itk=20 buyu=21
        musakat=22 feraiz=23 hibat|hibe=24 vasiyet|vesaya=25 nezir|nuzur=26 eyman=27 kasame=28 hudud=29 akdiye=30
        lukata=31 cihad=32 imaret?|imara=33 sayd=34 edahi=35 esribe=36 libas=37 edeb=38 selam=39 elfaz\w*=40 sir=41 ruya=42
        fedail|fezail=43 fa?e?[dz]ail\w*sahabe=44 birr\w*=45 kader=46 ilim=47 zikir|zikr=48 rikak=49 tevbe=50 munafikin|sifat\w*munafikin=51
        kiyamet?|sifat\w*kiyame\w*=52 cennet=53 fiten=54 zuhd|zuhud=55 tefsir=56"""),
    "tirmidhi": _table(r"""
        taharet=1 salat|mevak[iî]t=2 vitir|vitr=3 cuma=4 ideyn|iydeyn=5 sefer=6 zekat=7 savm=8 hac=9 cenaiz=10 nikah=11
        rada=12 talak=13 buyu=14 ahkam=15 diyat=16 hudud=17 sayd=18 edahi=19 nuzur=20 siyer=21 fedail\w*cihad=22
        cihad=23 libas=24 etime=25 esribe=26 birr\w*=27 tib=28 feraiz=29 vesaya=30 vela=31 kader=32 fiten=33 ruya=34
        sehadat=35 zuhd|zuhud|zuht=36 kiyame\w*|sifat\w*kiyame\w*=37 cennet|sifat\w*cennet=38 cehennem|sifat\w*cehennem=39
        iman=40 ilim=41 istizan=42 edeb=43 emsal=44 fedail\w*kuran=45 kiraat=46 tefsir\w*=47 daavat|deavat|dua=48 menakib=49"""),
    "abudawud": _table(r"""
        taharet=1 salat=2 istiska=3 sefer=4 tatavvu=5 ramazan=6 sucud=7 vitir|vitr=8 zekat=9 lukata=10 menasik|hac=11
        nikah=12 talak=13 savm=14 cihad=15 dahaya|edahi=16 sayd=17 vesaya=18 feraiz=19 harac=20 cenaiz=21 eyman=22
        buyu=23 icare=24 akdiye=25 ilim=26 esribe=27 etime=28 tib=29 kehanet=30 itk=31 huruf=32 hammam=33 libas=34
        teraccul=35 hatem=36 fiten=37 mehdi=38 melahim=39 hudud=40 diyat=41 sunnet?=42 edeb=43"""),
    "nasai": _table(r"""
        taharet=1 miyah=2 hayz=3 gusul=4 salat=5 mevak[iî]t=6 ezan=7 mesacid=8 kible=9 imamet?=10 iftitah=11 tatbik=12
        sehv|sehiv=13 cuma=14 taksir=15 kusuf=16 istiska=17 havf=18 ideyn|iydeyn=19 kiyam\w*leyl=20 cenaiz=21
        siyam|savm=22 zekat=23 menasik|hac=24 cihad=25 nikah=26 talak=27 hayl=28 ahbas=29 vesaya=30 nihal=31 hibe=32
        rukba=33 umra=34 eyman=35 isret\w*nisa=36 tahrim\w*=37 kasm\w*fey=38 beyat|biat|beya=39 akika=40 fera=41 sayd=42
        dahaya|edahi=43 buyu=44 kasame=45 sarik=46 iman=47 zinet=48 adab\w*kuda\w*|kudat=49 istiaze=50 esribe=51"""),
    "ibnmajah": _table(r"""
        mukadd[ie]me=0 taharet=1 salat=2 ezan=3 mesacid=4 ikamet?\w*=5 cenaiz=6 siyam|savm=7 zekat=8 nikah=9 talak=10
        keffarat=11 ticarat=12 ahkam=13 hibat=14 sadakat=15 ruhun=16 sufa=17 lukata=18 itk=19 hudud=20 diyat=21
        vesaya=22 feraiz=23 cihad=24 menasik|hac=25 edahi=26 zebaih=27 sayd=28 etime=29 esribe=30 tib=31 libas=32
        edeb=33 dua=34 tabir|ruya=35 fiten=36 zuhd|zuhud=37"""),
    "malik": _table(r"""
        vukut\w*salat=1 taharet=2 salat|nida=3 sehv=4 cuma=5 ramazan=6 salat\w*leyl=7 cemaat=8 kasr|sefer=9 ideyn|iydeyn=10 havf=11
        kusuf=12 istiska=13 kible=14 kuran|mes+\w*kuran=15 cenaiz=16 zekat=17 siyam|savm=18 itikaf=19 hac=20 cihad=21 nuzur=22
        dahaya=23 zebaih=24 sayd=25 akika=26 feraiz=27 nikah=28 talak=29 rada=30 buyu=31 kirad=32 musakat=33 kira=34
        sufa=35 akdiye=36 vasiyet|vesaya=37 itk=38 mukatep=39 mudebber=40 hudud=41 esribe=42 ukul=43 kasame=44
        medine|cami=45 kader=46 husn\w*hulu?k=47 libas=48 sifat\w*nebi=49 ayn=50 sar=51 ruya=52 selam=53 beyat=55
        kelam=56 cehennem=57 sadaka=58 ilim=59 dua=60 esma\w*nebi=61"""),
}


def section(api: str, chapter: str) -> int | None:
    """Künyedeki kitap adının Hadith API bölümü; bilinmiyorsa boş."""
    name = re.sub(r"\s+", "", normalize_name(chapter).strip(" .,:"))
    for pattern, number in SECTIONS.get(api, ()):
        if pattern.fullmatch(name):
            return number
    return None
