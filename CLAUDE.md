# Risale-i Nur MCP — Proje Belgesi

Bu dosya projenin kalıcı bağlamıdır. Her oturumda önce bunu oku.

## Amaç

Risale-i Nur Külliyatı'nı yapay zekâ modellerinin **kaynağa bağlı kalarak** kullanabileceği bir MCP sunucusu geliştirmek. MVP yalnızca **Sözler** kitabını kapsar.

Nihai kullanım hedefleri:
1. Model bir konuda yorum yaptığında, dayandığı yeri tam adresiyle göstersin (ör. `Sözler › Onuncu Söz › Dokuzuncu Hakikat › ¶3`).
2. Bir konunun Külliyat'ta geçtiği yerler listelenebilsin.
3. Farklı bakış açılarıyla yapılan yorumlar da metindeki pasajlara dayansın.

MVP yalnızca 1. hedefin altyapısını kurar. 2. ve 3. hedefler sonraki aşamalardır.

## Temel ilke

**Her pasajın adresi veriden gelir, asla tahmin edilmez.** Sunucunun döndürdüğü her metin parçası, kitaptaki hiyerarşik konumunu ve PDF sayfa numarasını taşır. Adres üretemediğimiz metin, adres uydurularak değil, açıkça "adres belirsiz" işaretiyle saklanır.

## Teknik tercihler

- Dil: Python 3.11+
- Ortam ve bağımlılıklar: `uv`
- PDF okuma: PyMuPDF (`pymupdf`). Font boyutu ve kalınlık bilgisi başlık tespitinde kullanılacak.
- Veritabanı: SQLite + FTS5 (kelime araması). Anlamsal arama MVP'de **yok**.
- MCP: resmi Python SDK'sı (`mcp` paketi, FastMCP). Not: `@modelcontextprotocol/sdk` TypeScript paketidir, kullanmıyoruz.
- Test: `pytest` + MCP Inspector + Claude Code'a `claude mcp add` ile bağlayarak elle deneme.
- Platform: Linux Mint.

## Klasör yapısı

```
risale-mcp/
├── CLAUDE.md
├── data/
│   ├── raw/            # Kaynak PDF (git'e eklenmez)
│   ├── interim/        # Ayrıştırma ara çıktıları: sozler.json, outline.txt,
│   │                   #   fihrist_check.txt, review.html (kontrol arayüzü)
│   └── risale.db       # SQLite veritabanı (git'e eklenmez)
├── src/risale_mcp/
│   ├── inspect_pdf.py  # Aşama 1: PDF yapısını inceleme
│   ├── parse.py        # Aşama 2: PDF → hiyerarşik JSON
│   ├── normalize.py    # Türkçe metin normalizasyonu, sıra sayıları, slug
│   ├── review_ui.py    # Taksimat kontrol arayüzü: sozler.json → review.html
│   ├── review_assets/  # Arayüzün template.html, style.css, app.js dosyaları
│   ├── build_db.py     # Aşama 3: JSON → SQLite
│   └── server.py       # Aşama 4: MCP sunucusu
└── tests/
    ├── test_parse.py         # Yardımcılar ve sozler.json yapı testleri
    ├── test_review_ui.py     # Arayüz üreticisi testleri
    └── golden_questions.md   # Kullanıcının yazdığı test soruları
```

## Veri modeli

Risale'nin iç yapısı düzensizdir: Söz, Makam, Mebhas, Mesele, Nükte, Hakikat, Esas, Lem'a, İşaret, Remiz, Hâşiye, Zeyl vb. Bu yüzden **sabit sütunlar yerine esnek bir başlık yolu** kullanılır.

`passages` tablosu (taslak, Aşama 1 bulgularına göre güncellenebilir):

| Alan | Açıklama |
|---|---|
| `id` | Kararlı kimlik, ör. `sozler/10/hakikat-09/p003` |
| `book` | `sozler` |
| `path` | JSON liste, ör. `["Onuncu Söz", "Dokuzuncu Hakikat"]` |
| `ref` | İnsan okunur adres, ör. `Sözler › Onuncu Söz › Dokuzuncu Hakikat › ¶3` |
| `seq` | Kitap içindeki genel sıra (komşu pasajlar için) |
| `text` | Orijinal metin, değiştirilmeden |
| `text_search` | Aramaya özel normalize edilmiş metin |
| `kind` | `paragraph`, `hasiye`, `arabic`, `heading` |
| `parent_id` | Hâşiyeler için bağlı olduğu pasaj |
| `page_start`, `page_end` | PDF sayfa numaraları |

Ek olarak `outline` tablosu: başlık ağacı (id, başlık, seviye, ebeveyn, ilk ve son `seq`).

### Dikkat edilecek noktalar
- **Türkçe büyük/küçük harf:** Python'un `str.lower()` fonksiyonu `İ` ve `I` harflerini Türkçe kurallara göre çevirmez. `normalize.py` içinde Türkçeye özel bir dönüşüm yaz. Şapkalı harfler (â, î, û) aramada düz harfle eşleşmeli. Orijinal `text` alanı ise asla değiştirilmez.
- **Sayfa üstbilgi/altbilgileri:** Her sayfadaki tekrar eden başlık ve sayfa numaraları metne karışmamalı.
- **Hâşiyeler (dipnotlar):** Ana metinden ayrılmalı ve bağlı oldukları pasaja işaret etmeli.
- **Arapça metinler:** Korunmalı ve `kind` alanıyla işaretlenmeli.
- **Sayfaya bölünmüş paragraflar:** Sayfa sonunda bölünen paragraflar birleştirilmeli.

### Verilen kararlar (Aşama 1–2)
- **Arapça:** Kaynak PDF'teki Arapça fontların Unicode eşlemesi yok. Şimdilik yer tutucu kullanılıyor: blok için `kind="arabic"` ve `[Arapça metin]`, cümle içinde `[Arapça]`. Ham glif kodları `arabic_glyphs` alanında saklanır; ileride başka PDF'lerle karşılaştırılarak çözülecek.
- **Sayfa numarası ikincildir:** `page_start` ve `page_end` PDF'ten alınır, ama pasajlar hiyerarşik adresle anılır (`Sözler › Onuncu Söz › Dokuzuncu Hakikat › ¶3`).
- **Düğümler:** Her numaralı Hakikat, Nükte, Esas, Sır vb. ayrı bir düğümdür. Başlıkların hemen altındaki açıklama satırları `subtitle` alanına yazılır.
- **Hâşiyeler** `seq` almaz; `parent_id` ile bağlı oldukları pasaja işaret eder. Adres örneği: `… › ¶3 › Hâşiye`; bir pasajın birden fazla hâşiyesi varsa `Hâşiye 1`, `Hâşiye 2`.
- Birinci Söz'den önceki giriş metni için yapay bir `sozler/giris` düğümü vardır.

## Taksimat kontrol arayüzü

Ayrıştırılan başlık ağacını kitapla yan yana elle kontrol etmek içindir.

```
uv run python -m risale_mcp.parse       # sozler.json üret
uv run python -m risale_mcp.review_ui   # data/interim/review.html üret
xdg-open data/interim/review.html
```

- **Tek dosya:** Veri, stil ve betik dosyanın içine gömülüdür; sunucu ya da internet gerekmez. Kaynak dosyalar `src/risale_mcp/review_assets/` altındadır. `review_ui.py` yalnızca bunları birleştirir.
- **Sayfa bilgisi yok:** Arayüzde hiçbir yerde sayfa numarası olmaz, `page_*` alanları HTML'e hiç yazılmaz. Gezinme tamamen hiyerarşiktir.
- **Sol panel:** Başlık ağacı ve başlıklarda arama.
- **Sağ panel:** Seçilen düğümün yolu, başlığı, alt başlığı ve kimliği; numaralı paragraflar (`¶n`); paragrafın altında hâşiyeler; alt bölümlerin listesi; önceki/sonraki bölüm bağlantıları (← / → tuşları da çalışır). Her düğüme tıklanınca o düğümün kendi paragrafları görünür.
- **URL:** Seçili düğümü tutar (`review.html#sozler/10/hakikat-09`).
- **İşaretler:**
  - Her düğüme ve pasaja "✓ doğru / ✗ hatalı / ✎ not" konabilir. İşaretler tarayıcının `localStorage`'ında saklanır (`risale-review:sozler`).
  - Ağaçta, altında hatalı işaret bulunan düğümler kırmızı noktayla gösterilir.
  - "Notları dışa aktar" düğmesi `sozler-kontrol-notlari.json` dosyasını indirir. Her kayıtta `id`, `target` (node/passage/missing), `ref`, `status`, `note` bulunur. Bu dosya ayrıştırma düzeltmelerinin girdisidir.
  - "İçe aktar" ile başka bir tarayıcıya ya da bilgisayara taşınabilir.
- **Uyarı:** Kimlikler ayrıştırma kurallarına bağlıdır. `parse.py` değişince bazı kimlikler değişebilir; eski işaretler dışa aktarımda `target: "missing"` olarak görünür.

## MCP araçları (MVP)

1. **`get_outline(book: str = "sozler", depth: int = 2)`**
   Kitabın başlık ağacını döndürür.
2. **`get_passage(id: str, context: int = 0)`**
   Bir pasajı `ref` ve sayfa bilgisiyle döndürür. `context > 0` ise önceki ve sonraki pasajları da ekler. Hâşiyeleri de içerir.
3. **`search_passages(query: str, limit: int = 20)`**
   FTS5 ile BM25 sıralı kelime araması yapar. Her sonuç için `id`, `ref`, kısa önizleme ve sayfa bilgisi döner.

Sonraki aşamalar (MVP'de yapma): `find_topic` (etiket tabanlı konu fihristi), anlamsal arama, atıf doğrulama.

### Sunucu talimatları (`instructions` alanı)
Sunucu, istemci modele şu kuralları iletmeli:
- Risale'ye ait her iddiayı araç sonuçlarındaki `ref` ile göster. Adres uydurma.
- Araç sonuçlarında bulunmayan bilgiyi Risale'ye atfetme. Bulamazsan bunu açıkça söyle.
- Metnin söylediği ile senin yorumunu ayrı başlıklar altında ver.

## Çalışma kuralları

- Aşamaları sırayla yap. Her aşamanın sonunda **dur**, bulguları özetle ve onay bekle.
- Ayrıştırma kurallarını tahmine dayanarak yazma. Önce PDF'i incele, örnek sayfaları göster.
- Her aşamada kullanıcının elle doğrulayabileceği bir çıktı üret (örnek JSON, başlık ağacı, sayım tablosu).
- Belirsiz durumlarda en makul varsayımı yap, ama bunu açıkça belirt.
- Kod tanımlayıcıları İngilizce, açıklamalar ve kullanıcıyla iletişim Türkçe.

## Aşamalar

1. **PDF inceleme:** Yapıyı, fontları, başlık örüntülerini, üstbilgileri ve hâşiyeleri raporla. Ayrıştırma kurallarını öner.
2. **Ayrıştırma:** PDF'ten hiyerarşik JSON üret. Başlık ağacını PDF'in fihristiyle karşılaştır.
3. **Veritabanı:** SQLite ve FTS5 kurulumu, normalizasyon, birim testler.
4. **MCP sunucusu:** Üç aracı yaz. MCP Inspector ile test et.
5. **Uçtan uca test:** `claude mcp add` ile bağla, `tests/golden_questions.md` sorularıyla dene. Adreslerin doğruluğunu elle kontrol et.
