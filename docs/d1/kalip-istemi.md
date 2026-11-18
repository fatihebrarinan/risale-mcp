<!--
D14.7 (1) İşârât'ın soru kalıpları listesinin istemi (PLANLAR.md D14.7; kullanıcının kararı, 2026-11-18).
`scripts/d1-kalip.py liste` bu dosyanın "---- KALIP ----" bölümünü alır, {kaynaklar}'ı doldurur; model istemi `claude -p`
ile araçsız alır. Kaynak yalnız geliştirme birimleridir (Fâtiha, Bakara 1–8, 9–10, 11–12, 13, 17–20, 23–24, 31–33);
14–15, 16 ve saklı birimler (21–22, 25, 26–27, 28, 29, 30) verilmez. Çıktı taslak yazarının istemine ve tarama
tablosuna girer; sızıntı testi saklı birimlere karşı yapılır.

Sürümler:
- k1 (2026-11-18): ilk sürüm.
-->

---- KALIP ----

# Görev: İşârâtü'l-İ'câz'ın soru kalıpları

Aşağıda Bediüzzaman Said Nursî'nin İşârâtü'l-İ'câz'ından birkaç birimin Arapça metni ve bir kısmı için okumayla
çıkarılmış nükte listeleri (envanter) var.

İşârât bir âyetin nazmını işlerken her birimde aynı türden soruları tekrar tekrar sorar: "fiil neden meçhul?", "lâm-ı
tarif ne için?", "âyet neden bu kelimeyle bitti?", "neden vâv ile atfedilmedi?", "neden isim cümlesi?", "mef'ûl neden
hazfedildi?" gibi. Senin işin bu **soru kalıplarını** çıkarmak.

Bu liste, İşârât'ın usulüyle yeni âyetler için taslak yazan bir yazara verilecek. Yazar her âyette lafızları bu
kalıplarla tarayacak ve lafız taşıyorsa nükteyi yazacak. Bu yüzden:

- **Kalıp bir türdür, tek bir nükte değil.** "قِيلَ meçhuldür, nasihat farz-ı kifâyedir" bir nüktedir; kalıp "fiil neden
  meçhul getirildi?" sorusudur ve İşârât'ın ona verdiği cevap çeşitleridir.
- **Yalnız tekrar eden kalıplar:** en az iki ayrı yerde (tercihen iki ayrı birimde) sorulmuş olmalı.
- **Her kalıp için İşârât'ın tipik cevapları:** bu soruya İşârât'ın verdiği cevap türleri, Türkçe ve kısa, kendi
  sözünle (İşârât'ın cümlelerini kopyalama). Cevap türü de genel olsun: "faile dikkat çekilmez, fiilin kendisi
  önemlidir", "fail belirsizdir ya da herkestir".
- **Örnekler:** her kalıp için verilen metinlerden bir iki yer: birimin adı, lafız (âyetten, Arapça) ve nüktenin bir
  cümlelik Türkçe özeti.
- **Tanıma:** bu sorunun sorulacağı yer âyetin metninden nasıl tanınır? Kuralla tanınabiliyorsa `kural` ve hangi
  kural (aşağıdaki listeden), değilse `model` (bir okuyucunun bakması gerekir: hazf, iltifat, takdim-tehir gibi).
  Kurallar: `fasila` (âyetin son kelimesi ya da son cümlesi), `tarif` (lâm-ı tarifli isim), `tenkir` (tenvinli
  nekre), `tekid` (إنّ، أنّ، ألا، لام التأكيد، قد، نون التوكيد), `zamir_fasl` (ayırma zamiri), `mechul` (meçhul
  fiil), `siga_fiil` (mâzî ya da muzâri fiil), `isim_cumlesi` (isim cümlesi), `atif` (vâv, fâ, sümme ile atıf), `fasl`
  (atıfsız ardışık cümle), `sart` (إن، إذا، لو), `nefy` (لا، ما، لم، لن، ليس), `istifham` (soru edatı), `istidrak`
  (لكن), `harf_cer` (harf-i cer), `cem_ifrad` (cemi ya da müfred isim), `ism_isaret` (işaret ismi), `ism_mevsul`
  (mevsul), `nida` (nidâ). Gerekirse yeni bir kural adı öner (açıklamasıyla).
- **Dikkat:** kalıbın zorlanmaması için kısa bir uyarı: hangi durumda bu soru boşa sorulur, İşârât ne zaman bu
  lafızda bir şey söylemez.
- **Düzey:** `kelime` (tek lafız), `cumle` (cümlenin kuruluşu), `cumleler` (cümleler arası: atıf, fasl, sıra),
  `ayet` (âyetin bütünü: fâsıla, üslûp, iltifat).

20 ile 35 arasında kalıp bekliyorum; az geçen ama İşârât'ın usulünde ağırlığı olan kalıbı (cumhura ittiba gibi) atlama.
Kalıpları düzeye göre, her düzeyde sıklığa göre sırala. Vecihlerin kendisini (birinci vecih: öncesiyle nazım, ikinci
vecih: cümleler arası, üçüncü vecih: kelimeler) kalıp sayma; onlar yazarın zaten bildiği yapıdır.

Cevabın yalnız tek bir ```json kod bloğudur:

```json
{{"kaliplar": [{{"ad": "Meçhul bina", "duzey": "kelime", "soru": "Fiil neden meçhul getirildi?",
  "cevaplar": ["…", "…"], "tanima": "kural", "kural": "mechul",
  "ornekler": [{{"birim": "Bakara 13", "lafiz": "قِيلَ", "nukte": "…"}}],
  "dikkat": "…", "siklik": 4}}]}}
```

`siklik`: verilen metinlerde bu kalıbın kabaca kaç yerde sorulduğu.

# Metinler

{kaynaklar}
