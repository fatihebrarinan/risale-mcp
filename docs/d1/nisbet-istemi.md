<!--
D14.5b nisbet denetçisinin istemi (PLANLAR.md D14.5b; kullanıcının kararı, 2026-11-18). `scripts/d1-nisbet.py` bu
dosyanın "---- NISBET ----" bölümünü alır, {yer tutucuları} doldurur; model istemi `claude -p` ile araçsız alır (taslak
başına bir çağrı). Her kaynak için atıf verilen cümleler bağlamıyla (önceki ve sonraki cümleler) ve o kaynağa atıf veren
taslak cümleleri verilir; model her taslak cümlesinin nisbetini tartar. Denetçi taslağın bütün değerini değil, yalnız
"bu söz bu kaynağa doğru mal edilmiş mi"yi sorar.

Sürümler:
- n1 (2026-11-18): ilk sürüm.
-->

---- NISBET ----

# Görev: nisbet denetimi

Bir yapay zekâ, İşârâtü'l-İ'câz'ın usulüyle {sura_name} {ayahs}. âyetler için Arapça bir taslak ve Türkçe tercümesini
yazdı. Taslak birçok yerde bir sözü, görüşü ya da tespiti bir kaynağa mal ediyor ve köşeli numarayla ([12]) o kaynağın
belli cümlelerine atıf veriyor.

Senin işin dar: **her atıfta taslağın o kaynağa mal ettiği şey, kaynağın o cümlelerinde gerçekten kaynağın kendi
sözü ya da görüşü mü?** Taslağın doğru, güzel ya da usule uygun olup olmadığını tartma; yalnız nisbeti.

Aşağıda her kaynak için: atıf satırı, atıf verilen cümleler (»…« arasında) önceki ve sonraki cümleleriyle birlikte, ve o
kaynağa atıf veren taslak cümleleri (Türkçe tercümeden; numaralı).

# Hükümler

- `dogru`: taslağın mal ettiği şey kaynağın o cümlelerinde kaynağın kendi sözü ya da görüşü olarak var (mealen de olabilir).
- `nakil`: kaynak bunu bir başkasından naklediyor ("قيل", "قال فلان", "ذكر بعضهم", "ve dediler ki"), kendi görüşü değil;
  taslak ise kaynağın kendi görüşü gibi sunuyor.
- `itiraz`: söz kaynakta bir itirazın, sorunun ya da muhalifin sözünün parçası ("فإن قيل", "إن قلت", "قالت المعتزلة"),
  taslak kaynağın kendi görüşü gibi sunuyor.
- `reddedilen`: kaynak bu görüşü anıp reddediyor ya da zayıf buluyor, taslak kaynağın görüşü gibi sunuyor.
- `kaynakta_yok`: taslağın mal ettiği şey bu cümlelerde yok (bağlamda da yok).
- `asiyor`: kaynak benzerini söylüyor ama taslak onu genişletiyor, mutlaklaştırıyor ya da başka bir şeye bağlıyor
  (kaynağın sözünü aşan nisbet); ya da cümlenin öznesini, zamirin göndermesini yanlış okuyor.
- `nisbet_yok`: taslak cümlesi bu kaynağa bir söz mal etmiyor (yalnız "bkz." gibi gösteriyor ya da kendi istinbatını
  kaynağı dayanak göstererek söylüyor ve dayanak uyuyor).

Emin değilsen `dogru` deme; gerekçende neden emin olmadığını söyle.

Cevabın yalnız tek bir ```json kod bloğudur:

```json
{{"hukumler": [{{"kaynak": "12", "cumle": 1, "hukum": "itiraz", "gerekce": "kısa; kaynağın hangi cümlesine dayandığını söyle",
                "taslak_alinti": "taslak cümlesinden kısa parça"}}]}}
```

Her taslak cümlesi için bir hüküm.

# Kaynaklar ve taslak cümleleri

{kalemler}
