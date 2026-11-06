# Tercüme programı (TR; kullanıcı onayladı, 2026-11-06)

Y0.4'ün (`docs/turkce-erisim.md`) dördüncü kararından çıktı: izinli Türkçe tercümeler yalnız tefsirin değil bütün
alanların meselesidir (hadis kitapları, eklenecek tefsirler, aslı Arapça eserler). İki işi vardır: Türk kullanıcıya
(bugün kullanıcıların hepsi) metnin insan elinden tercümesini vermek, denetçinin yanında ikinci bir güvence olmak.

Tercüme bulunamayan yerde Y0.4'ün kuralı geçerlidir: sohbette damgalı "yapay zekâ tercümesi", kütüphanede saklanmaz.

**Programa taşınanlar:** HA4 (hadis tercümeleri; Diyanet, Akçağ adayları) ve Aşama 17'nin izin kısmı (Akgündüz,
Kızıl İcaz ve Ta'likat tercümesi). Aşamaların teknik kısmı (Kızıl İcaz'ın ayrıştırılması) kendi yerinde kalır.

## TR1. Envanter

`docs/tercumeler.md`: kütüphanedeki ve sıradaki her Arapça eser için yayımlanmış Türkçe tercümeler.

- **Eserler:** Kütüb-i Sitte ve Muvatta; sırada Müsned, Müstedrek (HA3); Beyzâvî, Keşşâf, ileride Râzî; Risale
  tarafında Kızıl İcaz (Ta'likat'ın Türkçesi var: Keşif).
- **Her tercüme için:** mütercim, yayınevi, yıl, tam mı kısmi mi, metin ve tercüme birlikte mi, dijital nüsha var mı,
  hak sahibi ve türü (devlet kurumu, vakıf, ticari yayınevi, mütercim, tez).
- **Doğrulama:** künye kütüphane kataloğundan (Millî Kütüphane, İSAM, üniversite katalogları); arama sonucu yetmez
  (Işık'ın Beyzâvî baskısının kaydı tam olup olmadığını söylemiyor). Doğrulanamayan "doğrulanmadı" diye kalır.
- Dışarıya bir şey gönderilmez; yalnız arama.

## TR2. Öncelik

Üç ölçüt: (1) eserin Risale'deki ve yol haritasındaki ağırlığı (hadiste Risale'nin künyelerinin çoğu Buhârî ve
Müslim'de; tefsirde Keşşâf Y1.7'nin eseri); (2) iznin alınabilirliği (devlet kurumları ve vakıflar ticari olmayan
bir kamu hizmetine daha yakın); (3) dijital nüsha (taranmış kitabı okutmak pahalı ve hatalı). Ön tahmin, envanterden
sonra kesinleşir: hadiste Diyanet (Tecrid-i Sarih ya da Hadislerle İslâm), tefsirde TYEK'in Keşşâf'ı (metin ve
tercüme birlikte, 5 cilt, 2017).

## TR3. İzin dalgaları

- Tek e-posta taslağı (`docs/tercume-izin-epostasi.md`), hak sahibi türüne göre birer paragraf. Şartlar: ticari
  olmayan kullanım, kaynak ve mütercim gösterilir, metin değiştirilmez, yalnız ilgili sunucuda (hadis, tefsir),
  dijital nüsha rica edilir. Projenin kısa tanıtımı kişiye özel gider (`docs/tefsir-tanitim.md`).
- 1. dalga devlet kurumları (Diyanet, Türkiye Diyanet Vakfı, TYEK), 2. dalga vakıf ve ticari yayınevleri.
- Her istek `docs/izinler.md` "Bekleyen"e, cevabı `data/raw/kullanici/izinler/`'e, kodda `catalog/permissions.py`'ye.
- E-postayı kullanıcı gönderir. İzin gelmeden tercüme alınmaz (HA4'ün usulü).

## TR4. Tercüme katmanı (ilk izinle birlikte)

- Her tercüme ayrı eserdir: `Work.translation`, `translator`, kendi baskı kaydı (`catalog/editions.py`) ve izni;
  kimlikler Arapça eserle paralel (aslı Arapça Risale eserlerinde olduğu gibi).
- **Hizalama** alana göre: hadis rivayet numarasıyla (en kolay); tefsir âyet birimiyle, sonra paragrafla; Kızıl İcaz
  şablonla. Hizalamadan örneklem kullanıcıya gösterilir.
- **Araçlar ve talimat:** izinli tercüme varsa önce o, mütercime atfedilerek (`translation: true`, `translator`); yoksa
  damgalı yapay zekâ tercümesi. Mütercimin tercümesi de metnin sahibine değil mütercime aittir; alıntı bloğunda
  Arapça asıl, tercüme atfıyla.
- **Denetim arayüzü (Y1.4):** izinli tercüme önce, yapay zekâ yardımcı tercümesi yalnız yedek.
- Her sunucu kendi alanının tercümesini taşır (hadis tercümesi hadis sunucusunda).

## TR5. Tercümesi olmayan eserler (uzun vade)

Tercümesi hiç olmayan ya da hakkı alınamayan eserler için insan yolu: ehil gönüllü mütercimler, CC BY 4.0 (denetçi
programının uzantısı, `docs/katki-sartlari.md`). Açık ilke sorusu, iş başlamadan karara bağlanır: yapay zekânın
taslağını bir insan mütercim düzeltirse metin kimin olur, nasıl işaretlenir.

## Bağlantılar

- Y1.7 (Keşşâf): Arapçası alınırken TYEK'in izni beklenir; tercüme gelirse hizalama Keşşâf'ın işiyle birlikte.
- Y1.8 (âyet dosyası): izinli tercüme yoksa Türkçe yardım damgalı.
- HA3: yeni hadis kitapları eklendikçe envanter genişler.

## Durum

| Adım | Durum |
|---|---|
| TR1 Envanter | 1. tur bitti (2026-11-06): `docs/tercumeler.md`; ikinci tur katalog doğrulaması |
| TR2 Öncelik | — |
| TR3 İzin dalgaları | — |
| TR4 Tercüme katmanı | — |
| TR5 Tercümesi olmayanlar | — |
