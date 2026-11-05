# data/

Bu klasörde yalnızca bu dosya git'tedir; `links/reviews/` (denetim kararları) açık depoda değil, kendi ayrı, yerel git deposundadır (yedeği kullanıcıda). Kod yollarını `src/risale_mcp/paths.py`'den alır.

```
data/
├── raw/<kaynak>/         Kaynaktan bir kez alınan ham veri; elle değiştirilmez. Kaynak başınadır: bir site birkaç alanı besleyebilir, izin de kaynağa bağlıdır
│   └── kullanici/        Kullanıcının dosyaları: <kitap>/<kitap>.pdf
├── library/              Asıl veri, alan ve koleksiyon başına (`catalog.Collection`)
│   ├── risale/
│   │   ├── kulliyat/     Bediüzzaman'ın eserleri ve mecmuaları: <eser>.json
│   │   └── ilgili/       Külliyat dışı kaynaklar (henüz boş): Sorularla Risale, tarihçeler, hatıralar
│   ├── tefsir/           Müfessirlerin eserleri (pilot: beyzavi.json, yalnız yerel profil)
│   ├── kuran/quran.json  Kur'ân katmanı
│   └── hadis/matches.json  Risale'deki hadislerin rivayetlerle eşlemesi; `hadis.py` üretir. Tam derlem şimdilik `raw/`dedir; tefsir-beyzavi.json: Beyzâvî'nin hadis bağlarının rivayet metinleri (`links_tefsir.py`)
├── links/<alan>/<yöntem>.jsonl  Bağlar: Risale'nin âyet, hadis ve kendi içiyle bağları (`links.py`, `docs/bag-altyapisi-plani.md`); üreten iş yazar, her profil okur
│   └── reviews/          Denetim kararları (`link_reviews.py`, kendi yerel git deposunda): isimli denetçilerin bağlar üzerine kararları, yalnız eklenir; silinmemeli
├── dist/<profil>/        Kurulan çıktı (`profiles.py`); kişisel ve genel
│   ├── risale.db         Veritabanı; library'den yeniden kurulur
│   └── vectors/          Anlamsal arama vektörleri. kisisel/vectors asıl depodur (ücretli çıkarılır, silinmemeli); genel/vectors ondan süzülür
├── manifest/<profil>/    Kimlik manifestosu (`manifest.py`): kabul edilmiş hâl, sürümler, kimlik değişikliği raporları. Silinmemeli: eski sürümlerin tek kaydıdır
├── interim/              Üretilen ara çıktılar ve raporlar; silinse yeniden üretilir (`golden/` hariç)
│   ├── erisale/          doğrulanmış blok listeleri
│   ├── rasaelalnour/     açılmış Word dosyaları
│   ├── outline/          elle kontrol için başlık ağaçları
│   ├── review/           kontrol arayüzü (taşınmamalı, aşağıya bakın)
│   ├── quran/, ayah_links/, arabic_kinds/   denetim raporları ve örneklemler
│   ├── golden/           altın soru çalıştırmaları (eski ölçümler yeniden üretilemez)
│   ├── search_eval/      arama ölçümleri
│   ├── tool_snapshot/    araç çıktısı kayıtları (`tool_snapshot.py`); `yayin-*` kayıtları deploy'un karşılaştırma tabanıdır, silinmemeli
│   └── chatgpt/          OpenAI eklenti paketi
├── logs/                 İndirme ve kurulum günlükleri
├── archive/              Artık kullanılmayan, saklanan dosyalar (asama-1/: ilk Sözler PDF/EPUB denemesi)
└── auth.db               Kullanım kaydı; asıl kopyası sunucudadır, yeniden kurulmaz
```

- **Yeni alan:** kaynağın izni `docs/izinler.md`'ye yazılır, eserler katalogda bir koleksiyona bağlanır (`catalog/`), profil o koleksiyonu listeler. Klasör katalogdan türer. Alanlar arası bağlar profilin veritabanında durur.
- **Sunucuyla ilişki:** Sunucuda aynı yollar kullanılır: `dist/genel/`, `library/kuran/quran.json`, `auth.db`. Yerleri değişirse `scripts/deploy.sh`, `docs/risale-mcp.server.service` ve sunucu birlikte değişmelidir.
- **Kontrol arayüzü:** `interim/review/` taşınmamalıdır. Tarayıcı işaretleri `localStorage`'dadır ve dosya adresine bağlı olabilir; önce dışa aktarılmalıdır.
- **Kaynak klasörlerinin durumu** (kullanımda, yalnız yerel, kullanılmıyor): `HUSUSI-VERILER.md`.
- **Klasör adı kaynağın adıdır:** kullanılmayan kaynaklar da `raw/<kaynak>/` altında durur, çünkü kaynak seçimi (Aşama 13.3) onları yeniden seçebilir.
