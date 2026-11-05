## Ek: Projenin kısa tanıtımı (gönüllü denetçiler için; taslak, 2. tur, 2026-11-05)

Kullanıcının doğaçlama metninden (2026-11-05) düzenlendi. Amaç: Y0.2'deki davet için günlük dilde kısa bir tanıtım ve
proje uzasa da yerinde duracak temel taşlar. Birkaç turda son hâlini alacak; düzeltme notları metnin altında.

### Metin

**Risale-i Nur MCP: kaynağa bağlı bir tefsir altyapısı**

https://risalemcp.com

Bediüzzaman Said Nursî, İşârâtü'l-İ'câz'ın başında, bu eserin Risalelerle beraber "me'haz" olacağını ve "ileride
bahtiyar bir hey'et"in onlardan "bir tefsir-i Kur'ânî" yazacağını ümit eder. Bu projenin temel amacı, o heyetin elinde
olacak altyapıyı hazırlamaktır. Biz tefsir yazmıyoruz; tefsiri yazacak mütehassıs ve muhakkik âlimlerin işini
kolaylaştıracak, kaynağa bağlı bir kütüphane ve bağ ağı kuruyoruz. Bu altyapı hüküm vermez: kimin, neyi, hangi
kanıtla söylediğini kaydeder.

**Yapının şeması.** En dış halkada Kur'ân-ı Kerîm var; her şeyi kuşatır ve ortak adrestir: her eser, her bağ
sonunda bir âyete ya da âyetin bir lafzına varır. İçeride Risale-i Nur ve müfessirlerin eserleri (Beyzâvî,
Zemahşerî, Râzî…) durur. Risale-i Nur, müellifin ifadesiyle Kur'ân'ın "kuvvetli bir tefsiri"dir ve bu yapının
eksenidir: bir âyette önce Risale'nin o âyetle kurduğu bağlar gösterilir,
müfessirlerin her biri ona ayrı ayrı bağlanabilir; müfessirlerin eserleri de kendi aralarında bağlanır. Hepsi
hadislere bağlanır. Bir eserin sözü her zaman kendi sahibine aittir; bir âlimin sözü başkasına, yapay zekânın
yazdığı hiçbir şey de bir âlime mal edilmez.

**Bağ nedir?** İki metnin aynı âyetten bahsetmesi tek başına bağ değildir. Bağ, iki yer arasındaki ilişkinin türüyle
(aynı söz, nakil, aynı görüş, farklı görüş, itiraz, âyete işaret…), kanıtıyla ve onu kimin denetlediğiyle kayıtlı
olmasıdır. Bir kısmını bilgisayar bulur (bir tefsirde geçen âyet alıntıları gibi), bir kısmı ancak ehil bir okumayla
bulunur (iki müfessirin aynı görüşte olup olmadığı gibi). Her ikisinde de son sözü insan denetçi söyler.

**Programdaki karşılığı.** Bütün metinler ve bağlar tek bir kütüphanede durur. Bu kütüphaneyi kullanıcıya üç ayrı
MCP sunucusu açar: Risale-i Nur, Hadis ve Tefsir. Her sunucu kendi alanının metnini taşır, öbür alanların metnini
kopyalamaz, yalnız adresini verir; Kur'ân hepsinde vardır. Kullanıcı Claude ya da ChatGPT gibi bir yapay zekâ
uygulamasına bu sunucuları ekler; yapay zekâ cevap verirken dayandığı yeri cümlesine kadar gösterir.

**Bugün nerede?**
- **Risale-i Nur sunucusu çalışıyor** (`mcp.risalemcp.com`): külliyatın tamamı, Kızıl İcaz'ın Türkçesi dışında, cümle cümle adresli; Kur'ân, âyet
  bağları ve ilk hadis eşleşmeleriyle birlikte. Bundan sonrası genel bir doğruluk
  kontrolü (cümle bölmesi, başlıklar, âyet ve hadis bağları) ve Osmanlıca metin desteği.
- **Tefsir tarafında ilk deneme bitti:** Beyzâvî'nin Envârü't-Tenzîl'i, İşârât'ın kapsadığı kısımda (Fâtiha ve Bakara
  1–33) alındı; 977 cümle, âyet alıntıları ve Risale ile bağları kuruldu, örneklem elle denetlendi. Sıradaki eser
  Keşşâf. Her yeni eserde âyet alıntılarını, hadis bağlarını ve öbür eserlerle ilişkilerini denetleyecek ehil
  insanlara ihtiyaç var.
- **Türkçe desteği** henüz yok ama planda: müfessirlerin eserleri şimdilik yalnız Arapça aslıyla duruyor.
- **Hadis sunucusu** yakın zamanda kurulacak. Risale'deki hadislerin kaynaklarda bulunup bulunmadığı bugün
  bilgisayarla aranıyor; bunun da bir hadisçinin gözünden geçmesi gerekiyor.

**Bağ önerme ve denetim.** Sunucuya bir "bağ önerme" kapısı eklenecek: izin verilen kişiler (ya da yapabilen herkes;
henüz karar verilmedi) iki yer arasında bir bağ önerebilecek, türünü ve kanıtını yazarak. Öneri önce "aday" olarak
bekler; o alanda ehil bir denetçi bağın doğru olup olmadığına ve ne kadar güçlü olduğuna karar verince kütüphaneye
girer. Denetçiler birbirinin kararını silmez, itiraz gerekçesiyle kayıtlı kalır; her kararın altında denetçinin adı
ve tarihi durur. Kapı ilim ve ihtisasa göre açılır, meşrebe göre değil.

**Varılacak yer: âyet dosyaları.** Bağlar ve eserler oturdukça her âyet (gerekirse her lafız) için bir dosya
hazırlanacak: önce Risale-i Nur'un o âyetle ilgili yerleri, sonra müfessirlerin kendi sözleriyle söyledikleri,
dayandıkları hadisler ve bunların kaynaklardaki durumu (hüküm verilmeden), kayıtlı bağlar, açık sorular. Yapay zekâ
bu bilgileri derleyip yorumlayabilir; ama yazdığı ayrı başlıkta ve "yapay zekâ derlemesidir, tefsir değildir"
işaretiyle durur. Bu dosyalar, ileride tefsiri yazacak heyete bir me'haz olacak.

**İlkeler.** Her adres veriden gelir, tahmin edilmez. Her söz sahibine aittir. Metinler izin veren kaynaklardan
alınır ve her cevapta kaynak gösterilir; proje kazanç amacı gütmez, sunucular
ücretsiz ve hesapsız kullanılır. Ölçüt hız değil sağlamlıktır; iş birkaç yıl sürebilir.

**Sizden ne istiyoruz?** Şu alanlardan birinde ehliyeti olan gönüllü denetçiler arıyoruz: Arapça okuyup bir tefsirdeki
âyet alıntısını tanıyabilen, hadis ilminde ehil olan, tefsir usûlünü bilen, Risale-i Nur'u iyi bilen. Arapça
bilmeyenlerin de yapabileceği bir iş var: Risale-i Nur metninin cümle bölmesini, başlıklarını ve âyet bağlarını
kontrol etmek. Denetim bilgisayar başında, küçük örneklemler hâlinde, kendi vaktinizde yapılır: önünüze bağ ve
kanıtı konur, "doğru / yanlış / not" dersiniz. Kararınız adınızla kaydedilir.

İletişim: destek@risalemcp.com · https://risalemcp.com

### Düzeltme notları (1. tur)

Metinde değiştirilenler ve eklenenler, gerekçeleriyle:

1. **Müellifin sözü eklendi.** Amaç, İşârât'taki "me'haz" tarifine dayandırıldı (`isaratul-icaz/mukaddemat/tenbih/c012`);
   projenin en sağlam temel taşı bu. Alıntılar o cümleden aynen.
2. **"Diğer tefsirler" yerine "müfessirlerin eserleri".** Proje kuralı: Risale'nin bir yeri bir âyetin "tefsiri"
   diye anılmaz (bağ türü hükümdür). Risale'yi metinde "tefsir" diye saymamak bu kurala uyar; ama müellif Risale'yi
   "manevî tefsir" diye anar. Tanıtımda Risale'nin bütününe "Kur'ân'ın manevî tefsiri" demek ister misiniz? (Soru 1)
3. **Hiyerarşi veride değil görünümde.** "Risale diğer tefsirlere teker teker bağlı" cümlesi, her müfessirin
   Risale'ye otomatik bağlı olduğu gibi okunabiliyordu. Gerçekte aynı âyetten bahsetmek bağ değildir; bağ türüyle,
   kanıtıyla ve denetimiyle kurulur. "Bağ nedir?" paragrafı bunun için eklendi.
4. **"Üç profil" yerine "tek kütüphane, üç sunucu".** Programda profil bir sunucunun hangi koleksiyonlardan kurulduğudur
   (bugün `kisisel` ve `genel`; `hadis` ve tefsir profilleri plandadır); bağlar profillerin arasında değil, ortak
   kütüphanede (`data/links/`) durur. Davet metninde teknik ayrıntı gerekmediği için yalnız "tek kütüphane, üç
   sunucu" dendi.
5. **"Risale profili tamam" yumuşatıldı:** 73/74 eser, Kızıl İcaz'ın Türkçesi eksik; Risale'deki hadis eşleşmeleri
   de elle doğrulanmadı, hadisçi denetimi Risale sunucusu için de gerekli.
6. **Beyzâvî pilotunun sonucu eklendi:** okuyan "ilk deneme yapıldı mı" diye soracak; somut sonuç güven verir.
7. **"Sağlık derecesi" yerine "doğru olup olmadığı ve ne kadar güçlü olduğu".** "Sıhhat" hadis ilminde terimdir;
   denetçinin hadise sıhhat hükmü verdiği sanılmasın. Altyapıda bağın durumu (denetlendi, itiraz edildi, geri
   çekildi) ve denetçinin güç hükmü ayrıdır.
8. **Denetimin kuralları eklendi:** aday durumu, ihtisasa göre denetim, kararların silinmemesi, adla kayıt. Davet
   edilen kişi en çok bunu soracak.
9. **"Yapay zekâ yorumları" damgalı:** kullanıcının kuralı, yapay zekânın yazdığı "tefsir" diye anılmaz; dosyada ayrı
   başlıkta durur.
10. **İlkeler ve davet bölümü eklendi:** tanıtım bir davetle bitmeli: hangi ihtisas, nasıl bir iş, karşılığında ne
    (adla kayıt).

Atlanan ama tanıtıma girip girmeyeceği size kalan:

- **Türkçe erişim** (Y0.4): müfessirlerin eserleri Arapça; Arapça bilmeyen okuyucu için ne yapılacağı henüz karar.
  Tanıtıma girerse "karar verilmedi" diye girer. (Soru 2)
- **Kimin bağ önerebileceği** kararı açık (metinde "henüz karar verilmedi" diye duruyor). (Soru 3)
- **Denetçinin vakti:** ne kadar iş beklendiği (ör. tur başına 40 satırlık örneklem) yazılırsa davet daha somut olur.
- **İletişim yolu ve kimin adına davet edildiği** (yayıncı adı "Nur Hadimleri" mi, kendi adınız mı). (Soru 4)

Sorular:
1. Risale-i Nur tanıtımda "Kur'ân'ın manevî tefsiri" diye anılsın mı, yoksa bugünkü gibi yalnız "eksen" mi?
2. Türkçe erişim meselesi tanıtıma girsin mi?
3. Bağ önerme kapısı tanıtımda "izinli kişiler" diye mi geçsin, yoksa karar açık mı kalsın?
4. Davet kimin adına ve hangi iletişim yoluyla?

### Düzeltme notları (2. tur)

Kullanıcının cevapları (2026-11-05): Risale tanıtımda tefsir diye anılır; Türkçe desteği "henüz yok, planda" diye
geçer, yapılınca değişir; bağ önerme kararı açık kalır; iletişim bilgilerini kullanıcı yazar.

1. **Risale'nin tefsir oluşu müellifin sözüyle:** "Kur'ân'ın … kuvvetli bir tefsiri" (Şualar › Birinci Şuâ,
   `sualar/1/sual-02/c008`; aynı ifade Afyon müdafaasında da var). Bağ düzeyindeki kural değişmez: Risale'nin tek
   bir yeri bir âyetin "tefsiri" diye işaretlenmez, çünkü o bir hükümdür.
2. **Site bağlantısı** başlığın altına ve iletişim satırına eklendi.
3. **Unutulanlar (tekrar kontrolde bulunan):** Arapça bilmeyen gönüllülere de iş var (Risale metninin doğruluk
   kontrolü, Aşama 16); denetimin küçük örneklemlerle, kişinin kendi vaktinde yapıldığı; kaynakların izinli olduğu ve
   sunucuların ücretsiz, hesapsız kullanıldığı.

### Son hâl (2026-11-05)

Kullanıcı metni son hâli saydı. Son düzeltmeler: kaynakların adları "İlkeler"den çıkarıldı (kullanıcının isteği);
"74 eserden 73'ü" yerine "külliyatın tamamı, Kızıl İcaz'ın Türkçesi dışında" (74 yerel profilin sayısıdır, yalnız
yerelde duran eserler dahil; genel sunucuda 70 eserden 69'u, sitedeki "53 eser ve 16 Osmanlıca cilt" ile aynı).
Bu metin sitede yayımlanmaz (aşağıya bakın).

**Sitenin katkı sayfası kısaltıldı (2026-11-05).** Görüşülen ehil kişilerin tavsiyesiyle projenin amacı ve
özellikleri sitede ulu orta yayılmaz; tanıtım metni yalnız bu dosyada kalır. `site/katki.html` ve
`site/en/contribute.html` yalnız aranan dört niteliği (âyet alıntısı, hadis, tefsirler arası bağlantı, Risale ile
kaynak karşılaştırması), işin nasıl yapılacağının henüz belli olmadığını ve iletişimi söyler; platform hazır olunca
güncellenir.

**WhatsApp mesajı** (kişiye özel; telefon numarası sitede değil, yalnız burada):

> Selamün aleyküm. Risale-i Nur MCP projesinde metinleri ve kaynaklarını denetleyecek gönüllüler arıyoruz: Arapça okuyup tefsirlerdeki âyet alıntılarını ya da hadisleri tanıyabilen, tefsir usûlünü bilen, Risale-i Nur'u iyi bilen kişiler.
> Ayrıntı: https://risalemcp.com/katki.html
> İletişim: destek@risalemcp.com
