# risale-mcp

Bediüzzaman Said Nursî'nin eserlerini yapay zekâ asistanlarına **metinden ayrılmadan** açan bir [MCP](https://modelcontextprotocol.io) sunucusu. Asistan konuşmadan önce metni okur, alıntısını eserlerin kendisinden yapar ve dayandığı her yeri cümle düzeyinde gösterir:

> Sözler › Onuncu Söz › On iki Hakikat › Dokuzuncu Hakikat › “Hiç mümkün müdür ki; ölmüş…”

Adresler her zaman veriden gelir; sunucu adres ya da alıntı üretmez. Asistan cevabından önce alıntılarını sunucuya denetletir, cevabın sonuna da "Kaynaklar" listesini koyar. Metnin söyledikleri ile asistanın yorumu ayrı tutulur.

**Tanıtım sitesi ve kurulum:** [risalemcp.com](https://risalemcp.com) ([English](https://risalemcp.com/en/))

## Kullanım

Sunucu herkese açık bir bağdaştırıcı olarak çalışır:

```
https://mcp.risalemcp.com/mcp
```

- **claude.ai, Claude masaüstü ve mobil:** [bağdaştırıcıyı ekle](https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Risale-i%20Nur&connectorUrl=https%3A%2F%2Fmcp.risalemcp.com%2Fmcp) ya da elle *Özelleştirme › Bağdaştırıcılar › Ekle › Özel bağdaştırıcı ekle*. Hesap gerekmez. Her cevapta metnin okunması ve kaynakça için sitedeki [proje talimatını](https://risalemcp.com/#proje) bir Claude projesine yapıştırmanızı öneririz.
- **Claude Code:** `claude mcp add --transport http risale https://mcp.risalemcp.com/mcp`
- **ChatGPT:** *Eklentiler › Ekle › Özel MCP sunucusu ekle*, kimlik doğrulama yok.
- **Gemini:** yakında.

Hesap gerekmez; kullanım toplam sınırlarla korunur. Belgeler: [risalemcp.com/belgeler.html](https://risalemcp.com/belgeler.html), gizlilik: [risalemcp.com/gizlilik.html](https://risalemcp.com/gizlilik.html).

## Kapsam

53 eser ve ≈131.000 cümle: Risale-i Nur Külliyatı (Sözler, Mektubat, Lem'alar, Şualar, Lâhikalar, Tarihçe-i Hayat…), Eski Said dönemi eserleri, aslı Arapça eserlerin hem Arapçası hem Türkçesi (İşârâtü'l-İ'câz, el-Mesnevî el-Arabî, Kızıl İcaz, Ta'likat…), mecmualar ve Hizbler. Ayrıca 16 Osmanlıca cilt ve Kur'ân-ı Kerîm: harekeli metin ve Diyanet'in iki meali; eserlerde geçen âyetler Kur'ân metniyle eşlenmiştir. Hangi eserin hangi kaynaktan geldiği ve hangi aşamada olduğunun listesi [`docs/eserler/`](ESERLER.md) altındadır, yalnız yerelde tutulanlar [`HUSUSI-VERILER.md`](HUSUSI-VERILER.md)'de yazar.

Mecmualardaki (Asâ-yı Mûsâ, Zülfikâr…) metinler ana ciltlere eşlenmiştir; aynı metin tek yerde durur ve atıf ana cilde yapılır. Âyet ve hadis mealleri nâşirlerindir, müellife mal edilmez.

## Araçlar

Hepsi yalnızca okur.

| Araç | İşi |
|---|---|
| `search` | Metnin kendi kelimeleriyle arama (şapka ve Türkçe harf duyarsız; `"ifade"`, `haşr*`, `OR`, `-kelime`, `NEAR`) |
| `semantic_search` | Anlama göre arama: günümüz kelimeleriyle sorulan kavramı metnin eski kelimelerinde bulur |
| `read_section` | Bölümü alt bölümleriyle, hâşiyeleri ve âyet mealleriyle okur |
| `get_passage` | Bir cümle ya da cümle aralığı, komşu cümlelerle |
| `get_outline` | Bir eserin ya da bölümün başlık ağacı |
| `list_works` | Eserler ve kimlikleri |
| `find_sentence` | İlk kelimelerinden cümleyi bulur |
| `find_ayah` | Bir âyetin eserlerde geçtiği yerler ve onunla bağ kuran bölümler |
| `get_ayah` | Kur'ân'dan âyet: harekeli metin ve iki Diyanet meali |
| `cite` | Alıntıları denetler, cevabın "Kaynaklar" listesini verir |

Ayrıca kaynaklar (`risale://text/sozler/10`) ve hazır komutlar vardır: konu taraması, "metin ne diyor / yorum" ayrımı, müzakere, kendini sınama, ders planı.

## Yerelde kurmak

Python 3.11+ ve [uv](https://docs.astral.sh/uv/) gerekir. Metinler depoda **yoktur**; kaynak sitelerden indirilip yerelde işlenir:

```sh
uv sync
uv run python -m risale_mcp.fetch get --all --site erisale   # her site ayrı: kesif, kullanici; yalnız yerel eserler için risale_online, rasaelalnour
uv run python -m risale_mcp.fetch risaleoku                  # risaleoku.com'daki kitaplar
uv run python -m risale_mcp.fetch quran                      # Kur'ân metni ve mealleri (tanzil.net)
uv run python -m risale_mcp.quran                            # Kur'ân katmanı
uv run python -m risale_mcp.build --all                      # data/library/ ve data/dist/<profil>/risale.db
uv run python -m risale_mcp.embeddings build voyage-context-4   # anlamsal arama vektörleri (.env'de VOYAGE_API_KEY)
```

İndirici siteleri yormamak için istekler arasında bekler; bütün eserlerin indirilmesi saatler sürer. Bazı eserler kullanıcının kendi dosyalarından gelir (`kullanici`, ayrıntı `CLAUDE.md`'de). Klasörlerin düzeni: [`data/README.md`](data/README.md).

Yerel sunucu:

```sh
uv run risale-mcp                                        # stdio (Claude Desktop, Claude Code)
uv run risale-mcp --transport streamable-http --no-auth  # 127.0.0.1:8000/mcp, yalnız bu bilgisayar
npx @modelcontextprotocol/inspector uv run risale-mcp    # araçları elle denemek
```

Genel sunucu açık kipte çalışır (`--public-url … --open`); uzak sunucuya gönderme `scripts/deploy.sh`, yönetim `scripts/sunucu.sh`.

## Geliştirme

```sh
uv run pytest                                  # birim testler
uv run python -m risale_mcp.golden run --all   # altın sorularla uçtan uca deneme (Claude Code gerekir)
uv run python -m risale_mcp.search_eval run words server sections   # arama değerlendirmesi
uv run python -m risale_mcp.review_ui          # başlık ağacı ve cümle bölmesini kontrol arayüzü
```

Tasarım, veri modeli, ayrıştırma kuralları ve aşamalar [`CLAUDE.md`](CLAUDE.md)'dedir. Tanıtım sitesi `site/` klasöründedir.

## Kaynaklar ve izinler

Genel sunucunun metinleri [erisale.com](https://www.erisale.com), [risaleoku.com](https://www.risaleoku.com) ve Keşif Yolculukları Risale-i Nur Eğitim Programı'ndan değiştirilmeden alınır; Kur'ân metni ve Diyanet mealleri [Tanzil Project](https://tanzil.net)'ten (mealler ticari olmayan kullanım için). Rumuzat-ı Semaniye kullanıcının sağladığı dosyadan gelir. Kim, hangi şartla izin verdi: [`docs/izinler.md`](docs/izinler.md). İndirilen metinler ve veritabanı depoya eklenmez.

Nur Hadimleri: gönüllü ve bağımsız bir projedir; herhangi bir yayınevi ya da cemaatin resmî hizmeti değildir. İletişim: [destek@risalemcp.com](mailto:destek@risalemcp.com)
