# risale-mcp

Bediüzzaman Said Nursî'nin eserlerini yapay zekâ modellerine **cümle düzeyinde, atıf verilebilir** biçimde açan bir [MCP](https://modelcontextprotocol.io) sunucusu.

Bağlı model bir konuda yorum yaptığında, dayandığı yeri tam adresiyle gösterir:

> Sözler › Onuncu Söz › On iki Hakikat › Dokuzuncu Hakikat › “Hiç mümkün müdür ki; ölmüş…”

Adresler her zaman veriden gelir; sunucu adres ya da alıntı üretmez. Model cevabını vermeden önce atıflarını sunucuya denetletir.

## Kapsam

Risale-i Nur ana ciltleri, Lâhikalar, Tarihçe-i Hayat, Eski Said dönemi eserleri, mecmualar ve Hizbler: 43 eserden 38'i, ≈7.300 bölüm ve ≈110.000 cümle. Hangi eserin hangi kaynaktan geldiği ve hangi aşamada olduğu [`ESERLER.md`](ESERLER.md)'de yazar.

Mecmualardaki (Asâ-yı Mûsâ, Zülfikâr…) metinler ana ciltlere eşlenmiştir; aynı metin tek yerde durur ve atıf ana cilde yapılır.

## Araçlar

| Araç | İşi |
|---|---|
| `list_works` | Eserler ve kimlikleri |
| `get_outline` | Bir eserin ya da bölümün başlık ağacı |
| `read_section` | Bölümü alt bölümleriyle, hâşiyeleri ve âyet mealleriyle okur |
| `get_passage` | Bir cümle ya da cümle aralığı, komşu cümlelerle |
| `search` | Kelime araması (şapka ve Türkçe harf duyarsız; `"ifade"`, `haşr*`, `OR`, `-kelime`, `NEAR`) |
| `find_sentence` | İlk kelimelerinden cümleyi bulur |
| `find_ayah` | Bir âyetin eserlerde geçtiği yerler |
| `verify_citations` | Taslak cevaptaki atıfları metne karşı denetler |

Ayrıca kaynaklar (`risale://text/sozler/10`) ve hazır komutlar vardır: konu taraması, "metin ne diyor / yorum" ayrımı, müzakere, kendini sınama, ders planı.

## Kurulum

Python 3.11+ ve [uv](https://docs.astral.sh/uv/) gerekir. Metinler depoda **yoktur**; kaynak sitelerden indirilip yerelde işlenir:

```sh
uv sync
uv run python -m risale_mcp.fetch get --all --site erisale   # her site için ayrı: risale_online, risaleoku, kastamonur
uv run python -m risale_mcp.build --all                      # data/books/*.json ve data/risale.db
```

İndirici siteleri yormamak için istekler arasında bekler. Bütün eserlerin indirilmesi saatler sürer.

## Kullanım

Claude Code:

```sh
claude mcp add risale -- uv --directory /yol/risale-mcp run risale-mcp
```

Claude Desktop (`claude_desktop_config.json`):

```json
{"mcpServers": {"risale": {"command": "uv", "args": ["--directory", "/yol/risale-mcp", "run", "risale-mcp"]}}}
```

Araçları elle denemek için: `npx @modelcontextprotocol/inspector uv run risale-mcp`

## Geliştirme

```sh
uv run pytest                                  # birim testler
uv run python -m risale_mcp.golden run --all   # altın sorularla uçtan uca deneme (Claude Code gerekir)
uv run python -m risale_mcp.review_ui          # başlık ağacı ve cümle bölmesini kontrol arayüzü
```

Tasarım, veri modeli ve ayrıştırma kuralları [`CLAUDE.md`](CLAUDE.md)'dedir.

## Kaynaklar ve kullanım

Metinler [erisale.com](https://www.erisale.com), [risale.online](https://risale.online), [risaleoku.com](https://www.risaleoku.com) ve [kastamonur.com](https://kastamonur.com) sitelerinden alınır. Proje kişisel kullanım içindir: indirilen metinler ve veritabanı paylaşılmaz. Sunucu kimlik doğrulaması olmadan dışarıya açılmamalıdır. Uygulama olarak yayımlanırsa kaynak sitelerden izin alınacaktır.
