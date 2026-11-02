# data/

Bu klasörde yalnızca bu dosya git'tedir. Kod yollarını `src/risale_mcp/paths.py`'den alır.

```
data/
├── raw/<kaynak>/     Kaynaktan bir kez alınan ham veri; elle değiştirilmez
│   └── kullanici/    Kullanıcının dosyaları: <kitap>/<kitap>.pdf
├── books/            Her eserin JSON'u (asıl veri)
├── interim/          Üretilen ara çıktılar ve raporlar; silinse yeniden üretilir (`golden/` hariç)
│   ├── erisale/      doğrulanmış blok listeleri
│   ├── rasaelalnour/ açılmış Word dosyaları
│   ├── outline/      elle kontrol için başlık ağaçları
│   ├── review/       kontrol arayüzü (taşınmamalı, aşağıya bakın)
│   ├── quran/, ayah_links/, arabic_kinds/   denetim raporları ve örneklemler
│   ├── golden/       altın soru çalıştırmaları (eski ölçümler yeniden üretilemez)
│   ├── search_eval/  arama ölçümleri
│   ├── chatgpt/      OpenAI eklenti paketi
│   └── vectors-public/  sunucuya giden vektör kopyası (`deploy.sh` üretir)
├── vectors/          Anlamsal arama vektörleri (ücretli çıkarılır, silinmemeli)
├── logs/             İndirme ve kurulum günlükleri
├── archive/          Artık kullanılmayan, saklanan dosyalar (asama-1/: ilk Sözler PDF/EPUB denemesi)
├── quran.json        Kur'ân katmanı
├── risale.db         Yerel veritabanı (hepsi)
├── risale-public.db  Sunucuya giden kopya (`private` eserler yok)
└── auth.db           Kullanım kaydı; asıl kopyası sunucudadır, yeniden kurulmaz
```

- **Sunucuyla ilişki:** `quran.json`, `risale.db`, `vectors/` ve `auth.db` sunucuda da bu yollardadır (`risale.db` oradaki `risale-public.db`, `vectors/` oradaki `vectors-public/`); yerleri değişirse `scripts/deploy.sh` ve sunucu birlikte değişmelidir.
- **Kontrol arayüzü:** `interim/review/` taşınmamalıdır. Tarayıcı işaretleri `localStorage`'dadır ve dosya adresine bağlı olabilir; önce dışa aktarılmalıdır.
- **Kaynak klasörlerinin durumu** (kullanımda, yalnız yerel, kullanılmıyor): `HUSUSI-VERILER.md`.
- **Klasör adı kaynağın adıdır:** kullanılmayan kaynaklar da `raw/<kaynak>/` altında durur, çünkü kaynak seçimi (Aşama 13.3) onları yeniden seçebilir.
