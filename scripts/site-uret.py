#!/usr/bin/env python3
"""Sitelerin üretilen parçaları (PLANLAR.md S1, S2, S9, S13.15.6): Yenilikler, Çalışmalar, önizleme, Open Graph, menü
ve alt bilgi, sayılar, site haritaları.

İki site var (S13.15.6, 2026-11-27): **çatı** `ayinedar.org` (`site-ayinedar/`: ana sayfa, Yenilikler, Çalışmalar,
belgeler, gizlilik ve şartlar; `en/`) ve **eklentilerin tanıtımı** `risalemcp.com` (`site/`; S13.22'de
`connect.ayinedar.org`'a taşınacak). Yazılar yalnız çatıdadır; risalemcp.com'daki eski adresleri Caddy 308 ile çatıya
yönlendirir (`docs/Caddyfile`). Çatının `style.css`, `site.js` ve Naskh yazı tipi `site/`'tan kopyalanır (tek kaynak);
çatıya özgü görünüş `site-ayinedar/ayinedar.css`'tedir. Yazının içindeki, çatıda olmayan ama risalemcp.com'da olan
iç bağlantı (`/klasik.html`, `/claude.html`…) tam adrese çevrilir (`cross_links`).

    python3 scripts/site-uret.py                    # hepsi (taslaklar yalnız önizlemeye)
    python3 scripts/site-uret.py --resim            # bir de risalemcp.com'un paylaşım resmi (site/img/paylasim.png;
                                                    # uvx cairosvg); çatınınki scripts/paylasim-ayinedar.py cati
    python3 scripts/site-uret.py onizle             # üretir ve yerelde açar: http://127.0.0.1:8090/onizleme/
    python3 scripts/site-uret.py yayinla <ad>       # taslağı yayımlar (durum, tarih, dosya adı; bağlantı denetimi)
    python3 scripts/site-uret.py yayinla <ad> --gonder   # … ve scripts/deploy.sh --site (yalnız site)
    python3 scripts/site-uret.py zamanla <ad> 2026-11-24 # o gün kendiliğinden yayımlansın (`iptal` kaldırır)
    python3 scripts/site-uret.py cek                     # web düzenleyicideki düzeltmeleri depoya al (S11), commit
    python3 scripts/site-uret.py zamanli --gonder        # günü gelenleri yayımla, commit, deploy.sh --site
                                                         # (günlük zamanlayıcı: docs/site-zamanli.timer)

Sonra: scripts/deploy.sh --code (önizleme de onunla gider: lab.ayinedar.org/onizleme/, girişli, masa hesabı)

- İki tür yazı (`KINDS`): **Yenilikler** `docs/yenilikler/<tarih>-<ad>.md` (eklentide ne değişti; kısa) ve
  **Çalışmalar** `docs/calismalar/<tarih>-<ad>.md` (ne denendi, ne öğrenildi; uzun, kaynaklı; S9). Siteler olduğu gibi
  yayımlandığı için kaynak orada durmaz. Üst bilgi: `baslik`, `tarih` (YYYY-AA-GG), `ozet` (dizinde ve önizlemede),
  `whatsapp` (`|` ile çok satırlı; paylaşım kutusundaki metin, sonuna yazının adresi eklenir; Yeniliklerde zorunlu),
  `durum` (`taslak` | `yayinda`; yoksa `yayinda`), Çalışmalarda isteğe bağlı `gozden_gecirme` (son gözden geçirme
  tarihi) ve `adres` (yazı başka bir betiğin ürettiği sayfaysa, ör. `/isarat-usul/`: gövdesi yoktur, yalnız listede
  durur; yayımlanınca o sayfanın `noindex`i kalkar ve site haritasına girer, taslakken `noindex` kalır).
- Gövde sade Markdown: `##`, `###`, paragraf, `-` ve `1.` listeleri, `>` alıntı, `**kalın**`, `*eğik*`, `` `kod` ``,
  `[metin](adres)`, `---` çizgi, `|` tablo (ikinci satır `|---|`), kutu (`:::kisa` … `:::`: "Kısa cevap";
  `:::not Başlık` … `:::`). Arapça kendiliğinden işaretlenir: çoğu Arapça olan alıntı ve paragraf sağdan sola,
  metin içindeki Arapça `lang="ar"` (sitenin Naskh yazı tipi, `site/fonts/naskh.woff2`).
- **Taslak** yazı çatıya yazılmaz; listeye, RSS'e, site haritasına, ana sayfa şeridine girmez. Önizlemesi
  `data/interim/onizleme/<tür>/<ad>.html`'dedir (sitedeki görünüşüyle, başında önizleme şeridi, `noindex`); deploy onu
  girişli `lab.ayinedar.org/onizleme/`'ye gönderir. `yayinla`: önce önizlemedeki iç bağlantılar denetlenir (yoksa durur), sonra
  `durum: yayinda`, `tarih` bugün, dosya adı bugünün tarihiyle (adres yayından sonra değişmez); Çalışmalar yazısıysa
  Yeniliklere kısa duyuru **taslak** olarak yazılır (o da `yayinla` ile).
- Çıktı: `site-ayinedar/<tür>/<ad>.html`, `site-ayinedar/<tür>.html` (en yeni üstte), `site-ayinedar/<tür>.xml`
  (RSS 2.0; `guid` eski risalemcp.com adresidir, okuyucular taşınan yazıyı yeni sanmasın).
- Open Graph: iki sitenin kökündeki ve `en/` altındaki her sayfada `<!-- og -->` ile `<!-- /og -->` arası her seferinde
  yeniden yazılır (yoksa `</title>` satırından sonra eklenir); başlık `<title>`'dan, açıklama `description`'dan.
  WhatsApp önizlemeyi adres başına önbelleğe alır: etiket değişince eski paylaşımlar bir süre eski görünür.
- Ana sayfalar (`site-ayinedar/index.html`, `site/index.html` tam adresle): `<!-- son-yenilik -->` arasında son yazıya şerit, `<!-- son-yenilikler -->` arasında
  son üç yazı.
- Menü ve alt bilgi: sayfaların `<nav>` ve `<footer>` blokları her seferinde buradan yazılır (`nav_html`, `FOOTER`;
  İngilizcede `nav_en`, `FOOTER_EN`). Öbür dile giden bağlantı sayfanın `hreflang` adresidir.
- Sayılar: sayfalardaki `<!-- sayi:ad -->…<!-- /sayi -->` arası yerel veritabanlarından (`data/dist/`) yazılır
  (`numbers`; İngilizce sayfalarda `ad_en`: "131,000"); veritabanı yoksa olduğu gibi kalır.
- `sitemap.xml` iki sitede: sayfalar; yazılar yalnız çatınınkinde. Alt klasördeki sayfalar (ör. `scripts/d1-okur.py`'nin
  ürettiği `site-ayinedar/isarat-usul/`) menü, alt bilgi ve Open Graph alır; haritaya yalnız bir Çalışmalar kaydı (`adres`)
  yayımlanmışsa girer.
- Dışarıya istek yok kuralı sürer: "WhatsApp'ta paylaş" yalnız tıklanınca açılan bir bağlantıdır.
"""

import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import date
from email.utils import format_datetime
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"                       # risalemcp.com: eklentilerin tanıtımı
CATI = ROOT / "site-ayinedar"              # ayinedar.org: çatı (S13.15.6); yazılar burada
PREVIEW = ROOT / "data" / "interim" / "onizleme"     # deploy: /var/www/ozel/taslak/onizleme/ (lab.ayinedar.org, girişli)
PREVIEW_URL = "/onizleme"                 # lab.ayinedar.org; sitenin dosyalarını Caddy orada da verir
BASE = "https://risalemcp.com"
CATI_BASE = "https://ayinedar.org"
CHAT = "https://chat.ayinedar.org/"
IMAGE = "/img/paylasim.png"                # iki sitede de aynı yolda, ayrı resim (çatınınki `--resim` ile değil,
                                           # scripts/paylasim-ayinedar.py ile)
SHARED = ("style.css", "site.js", "fonts/naskh.woff2")   # site/'tan çatıya kopyalanır
ASSET_VERSION = 12                      # style.css ve site.js sürümü (sayfalardaki ?v=N ile aynı tutulur)
MONTHS = ("Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık")
STATUSES = ("taslak", "yayinda")


@dataclass(frozen=True)
class Kind:
    key: str            # klasör ve adres adı
    title: str
    lead: str
    description: str
    required: frozenset

    @property
    def src(self) -> Path:
        return ROOT / "docs" / self.key

    @property
    def out(self) -> Path:
        return CATI / self.key

    @property
    def index(self) -> str:
        return f"/{self.key}.html"


KINDS = {
    "yenilikler": Kind("yenilikler", "Yenilikler",
                       "Sohbette ve eklentilerde yeni olanlar, iyileştirmeler ve duyurular. Her yazının sonunda "
                       "paylaşmak için kısa bir metin var.",
                       "Âyinedâr'da yeni olanlar: sohbet, Risale-i Nur, Hadis, Tefsir ve Klasik Eserler eklentileri; "
                       "iyileştirmeler ve duyurular.",
                       frozenset({"baslik", "tarih", "ozet", "whatsapp"})),
    "calismalar": Kind("calismalar", "Çalışmalar",
                       "Projenin ne denediği ve ne öğrendiği: usul, ölçüler, sonuçlar ve sınırlar. Uzun ve kaynaklı "
                       "yazılar; hiçbiri tefsir değildir.",
                       "Âyinedâr'ın çalışmaları: İşârâtü'l-İ'câz'ın usulü, yapay zekâ taslakları, ölçüler, sonuçlar "
                       "ve sınırlar.",
                       frozenset({"baslik", "tarih", "ozet"})),
}


@dataclass
class Post:
    kind: Kind
    slug: str
    title: str
    day: date
    summary: str
    share: str
    body: str
    status: str = "yayinda"
    review: date | None = None
    address: str | None = None
    source: Path | None = None
    scheduled: date | None = None       # `yayin_tarihi`: o gün (ya da makine açılınca) kendiliğinden yayımlanır

    @property
    def path(self) -> str:
        return self.address or f"/{self.kind.key}/{self.slug}.html"

    @property
    def preview_path(self) -> str:
        return self.address or f"{PREVIEW_URL}/{self.kind.key}/{self.slug}.html"

    @property
    def draft(self) -> bool:
        return self.status == "taslak"

    @property
    def date_tr(self) -> str:
        return date_tr(self.day)

    @property
    def minutes(self) -> int:
        return max(1, round(len(re.findall(r"\w+", self.body)) / 200))


def date_tr(d: date) -> str:
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


# ---- yazılar --------------------------------------------------------------------------------------------------

def front_matter(text: str, name: str) -> tuple[dict, int]:
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        sys.exit(f"{name}: üst bilgi yok (--- … ---)")
    meta, key = {}, None
    for line in m.group(1).split("\n"):
        if key and (line.startswith("  ") or not line.strip()):
            meta[key] += line[2:] + "\n"
        elif (kv := re.match(r"(\w+):\s*(.*)$", line)):
            k, v = kv.groups()
            key = k if v == "|" else None
            meta[k] = "" if v == "|" else v
        else:
            sys.exit(f"{name}: anlaşılmayan üst bilgi satırı: {line!r}")
    return meta, m.end()


def read_post(path: Path, kind: Kind) -> Post:
    return parse_post(path.read_text(encoding="utf-8"), kind, path.stem, path)


def parse_post(text: str, kind: Kind, slug: str, path: Path | None = None) -> Post:
    """Yazının metninden (üst bilgi ve gövde). Hata `sys.exit` ile (S11: web düzenleyici onu yakalar)."""
    name = path.name if path else f"{slug}.md"
    meta, end = front_matter(text, name)
    missing = kind.required - set(meta)
    if missing:
        sys.exit(f"{name}: eksik üst bilgi: {', '.join(sorted(missing))}")
    status = meta.get("durum", "yayinda").strip()
    if status not in STATUSES:
        sys.exit(f"{name}: durum {status!r} (taslak ya da yayinda olmalı)")
    try:
        day = date.fromisoformat(meta["tarih"].strip())
        review = date.fromisoformat(meta["gozden_gecirme"].strip()) if meta.get("gozden_gecirme") else None
        scheduled = date.fromisoformat(meta["yayin_tarihi"].strip()) if meta.get("yayin_tarihi") else None
    except ValueError as e:
        sys.exit(f"{name}: tarih YYYY-AA-GG biçiminde olmalı ({e})")
    return Post(kind, slug, meta["baslik"], day, meta["ozet"],
                meta.get("whatsapp", "").strip(), text[end:], status, review, meta.get("adres") or None, path,
                scheduled)


def preview_html(kind_key: str, slug: str, text: str) -> str:
    """S11: web düzenleyicinin görünüşü: yazı metninden önizleme sayfası (sitedeki gibi)."""
    return post_page(parse_post(text, KINDS[kind_key], slug), preview=True)


def read_posts(kind: Kind) -> list[Post]:
    kind.src.mkdir(parents=True, exist_ok=True)
    return sorted((read_post(p, kind) for p in kind.src.glob("*.md")), key=lambda p: (p.day, p.slug), reverse=True)


ARABIC = "؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿"
ARABIC_RUN = re.compile(rf"[{ARABIC}](?:[{ARABIC}\s‌‍…«»()﴾﴿،؛:.!]*[{ARABIC}])?")


def mostly_arabic(text: str) -> bool:
    ar = len(re.findall(rf"[{ARABIC}]", text))
    return ar > 0 and ar >= 2 * len(re.findall(r"[A-Za-zÇĞİÖŞÜçğıöşüÂÎÛâîû]", text))


def inline(text: str, arabic: bool = True) -> str:
    out = html.escape(text, quote=False)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])", r"<em>\1</em>", out)
    out = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: f'<a href="{html.escape(m.group(2))}">{m.group(1)}</a>', out)
    if arabic:
        out = ARABIC_RUN.sub(lambda m: f'<span lang="ar" dir="rtl">{m.group(0)}</span>', out)
    return out


def slugify(text: str) -> str:
    table = str.maketrans("çğıöşüâîûÇĞİÖŞÜÂÎÛ", "cgiosuaiuCGIOSUAIU")
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>", "", text).translate(table).lower()).strip("-")


BOX_TITLES = {"kisa": "Kısa cevap"}


def markdown(text: str) -> str:
    """Yazıların kullandığı kadar Markdown: başlık, paragraf, liste, alıntı, tablo, çizgi, kutu."""
    boxes: list[str] = []

    def box(m: re.Match) -> str:
        name, title, inner = m.group(1), (m.group(2) or "").strip(), m.group(3)
        title = title or BOX_TITLES.get(name, "")
        head = f"<p class=\"box-title\"><strong>{inline(title)}</strong></p>\n" if title else ""
        boxes.append(f'<div class="note box box-{name}">\n{head}{markdown(inner)}\n</div>')
        return f"\n\n\x00{len(boxes) - 1}\x00\n\n"

    text = re.sub(r"^:::(\w+)(?: (.*))?\n(.*?)\n:::\s*$", box, text.strip(), flags=re.S | re.M)
    blocks, out = re.split(r"\n\s*\n", text.strip()), []
    for block in blocks:
        lines = block.strip("\n").split("\n")
        if (b := re.fullmatch(r"\x00(\d+)\x00", block.strip())):
            out.append(boxes[int(b.group(1))])
        elif (h := re.match(r"(#{2,3}) (.+)$", lines[0])) and len(lines) == 1:
            level = len(h.group(1))
            out.append(f'<h{level} id="{slugify(h.group(2))}">{inline(h.group(2))}</h{level}>')
        elif len(lines) == 1 and re.fullmatch(r"-{3,}", lines[0].strip()):
            out.append("<hr>")
        elif len(lines) >= 2 and all(l.startswith("|") for l in lines) and re.fullmatch(r"[|\s:-]+", lines[1]):
            def cells(row: str) -> list[str]:
                return [c.strip() for c in row.strip().strip("|").split("|")]
            head = "".join(f"<th>{inline(c)}</th>" for c in cells(lines[0]))
            rows = "\n".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells(r)) + "</tr>" for r in lines[2:])
            out.append(f'<div class="table-wrap"><table>\n<thead><tr>{head}</tr></thead>\n<tbody>\n{rows}\n</tbody>\n'
                       f"</table></div>")
        elif all(re.match(r"[-*] ", l) or l.startswith("  ") for l in lines):
            out.append("<ul>\n" + "\n".join(f"  <li>{inline(i)}</li>" for i in _items(lines, r"[-*] ")) + "\n</ul>")
        elif all(re.match(r"\d+\. ", l) or l.startswith("   ") for l in lines):
            out.append("<ol>\n" + "\n".join(f"  <li>{inline(i)}</li>" for i in _items(lines, r"\d+\. ")) + "\n</ol>")
        elif all(l.startswith(">") for l in lines):
            inner = " ".join(l[1:].strip() for l in lines)
            if mostly_arabic(inner):
                out.append(f'<blockquote dir="rtl" lang="ar"><p>{inline(inner, arabic=False)}</p></blockquote>')
            else:
                out.append(f"<blockquote><p>{inline(inner)}</p></blockquote>")
        else:
            para = " ".join(l.strip() for l in lines)
            out.append(f'<p dir="rtl" lang="ar">{inline(para, arabic=False)}</p>' if mostly_arabic(para)
                       else f"<p>{inline(para)}</p>")
    return "\n".join(out)


def _items(lines: list[str], marker: str) -> list[str]:
    items: list[str] = []
    for line in lines:
        if re.match(marker, line):
            items.append(re.sub(marker, "", line, count=1))
        else:
            items[-1] += " " + line.strip()
    return items

# ---- sayfa iskeleti -------------------------------------------------------------------------------------------

def og_block(title: str, description: str, path: str, lang: str = "tr", kind: str = "website",
             cati: bool = False) -> str:
    base = CATI_BASE if cati else BASE
    if cati:
        alt = ("Âyinedâr: Risale-i Nur, tefsir, hadis ve klasik eserlerden kaynağıyla cevaplayan yapay zekâ"
               if lang == "tr" else "Âyinedâr: an AI that answers from the Risale-i Nur, tafsir, hadith and classical "
               "works, with sources")
    else:
        alt = ("Risale-i Nur MCP: Risale-i Nur, Hadis ve Tefsir eklentileri" if lang == "tr"
               else "Risale-i Nur MCP: the Risale-i Nur, hadith and tafsir connectors")
    tags = [("og:type", kind), ("og:site_name", "Âyinedâr" if cati else "Risale-i Nur MCP"), ("og:title", title),
            ("og:description", description), ("og:url", base + path), ("og:image", base + IMAGE),
            ("og:image:width", "1200"), ("og:image:height", "630"), ("og:image:alt", alt),
            ("og:locale", "tr_TR" if lang == "tr" else "en_US")]
    lines = [f'<meta property="{k}" content="{html.escape(v)}">' for k, v in tags]
    lines.append('<meta name="twitter:card" content="summary_large_image">')
    return "<!-- og -->\n" + "\n".join(lines) + "\n<!-- /og -->"


NAV = [("/#eklentiler", "Eklentiler"), ("/#ekle", "Kurulum"), (CATI_BASE + "/yenilikler.html", "Yenilikler"),
       (CATI_BASE + "/calismalar.html", "Çalışmalar"), ("/belgeler.html", "Belgeler")]
# Sayfa -> menüde işaretli olan (sayfa adı; yazılar "yenilikler")
CURRENT = {"risale.html": "/#eklentiler", "hadis.html": "/#eklentiler", "tefsir.html": "/#eklentiler",
           "klasik.html": "/#eklentiler",
           "claude.html": "/#ekle", "chatgpt.html": "/#ekle", "belgeler.html": "/belgeler.html"}
FOOTER = ("<footer>Risale MCP: gönüllü ve bağımsız bir projedir; herhangi bir yayınevi ya da cemaatin resmî hizmeti "
          "değildir.<br><a href=\"/gizlilik.html\">Gizlilik</a> · <a href=\"/kullanim-sartlari.html\">Kullanım "
          "şartları</a> · <a href=\"/katki.html\">Hata bildirin</a> · <a href=\"" + CATI_BASE + "/yenilikler.xml\">RSS</a> · "
          "<a href=\"mailto:destek@risalemcp.com\">destek@risalemcp.com</a> · <a href=\"" + CATI_BASE + "/\">Âyinedâr"
          "</a>'ın eklentileri</footer>")


NAV_EN = [("/en/#connectors", "Connectors"), ("/en/#add", "Setup"), ("/en/docs.html", "Documentation")]
CURRENT_EN = {"risale.html": "/en/#connectors", "hadith.html": "/en/#connectors", "tafsir.html": "/en/#connectors",
              "classical.html": "/en/#connectors",
              "claude.html": "/en/#add", "chatgpt.html": "/en/#add", "docs.html": "/en/docs.html"}
FOOTER_EN = ("<footer>Risale MCP: a volunteer, independent project, not an official service of any publisher or "
             "community.<br><a href=\"/en/privacy.html\">Privacy</a> · <a href=\"/en/terms.html\">Terms of use</a> · "
             "<a href=\"/en/contribute.html\">Report a mistake</a> · <a href=\"" + CATI_BASE + "/yenilikler.html\" "
             "lang=\"tr\">News (Turkish)</a> · <a href=\"mailto:destek@risalemcp.com\">destek@risalemcp.com</a> · "
             "the connectors of <a href=\"" + CATI_BASE + "/en/\">Âyinedâr</a></footer>")


def nav_en(current: str = "", tr: str = "/") -> str:
    links = "\n".join(f'  <a href="{href}"' + (' aria-current="page"' if href == current else "") + f">{name}</a>"
                      for href, name in NAV_EN)
    return f"""<nav>
  <a class="brand" href="/en/"><img src="/icon.png" alt="">Risale-i Nur MCP</a>
{links}
  <a href="{tr}" lang="tr">Türkçe</a>
  <button class="theme-toggle" type="button" data-theme-toggle aria-label="Switch between light and dark mode" title="Switch between light and dark mode"></button>
</nav>"""


# Çatı (ayinedar.org, S13.15.6): menünün başı sohbet; "Projeler" ana sayfadaki kartlar
NAV_CATI = [(CHAT, "Sohbet"), ("/#projeler", "Projeler"), ("/yenilikler.html", "Yenilikler"),
            ("/calismalar.html", "Çalışmalar"), ("/belgeler.html", "Belgeler")]
CURRENT_CATI = {"yenilikler.html": "/yenilikler.html", "calismalar.html": "/calismalar.html",
                "belgeler.html": "/belgeler.html"}
INDEPENDENT = "gönüllü ve bağımsız bir hizmettir; herhangi bir yayınevi ya da cemaatin resmî hizmeti değildir"
FOOTER_CATI = (f"<footer>Âyinedâr: {INDEPENDENT}. Yayıncısı Nur Hadimleri. Ücretsizdir, reklam ve ziyaretçi sayacı "
               "yoktur.<br><a href=\"/gizlilik.html\">Gizlilik</a> · <a href=\"/kullanim-sartlari.html\">Kullanım "
               "şartları</a> · <a href=\"/belgeler.html\">Belgeler</a> · <a href=\"/yenilikler.xml\">RSS</a> · "
               "<a href=\"mailto:destek@ayinedar.org\">destek@ayinedar.org</a></footer>")
NAV_CATI_EN = [(CHAT, "Chat"), ("/en/#projects", "Projects"), ("/en/privacy.html", "Privacy")]
CURRENT_CATI_EN = {"privacy.html": "/en/privacy.html"}
FOOTER_CATI_EN = ("<footer>Âyinedâr: a volunteer, independent service, not an official service of any publisher or "
                  "community. Published by Nur Hadimleri. Free of charge, with no ads and no visitor tracking.<br>"
                  "<a href=\"/en/privacy.html\">Privacy</a> · <a href=\"/en/terms.html\">Terms of use</a> · "
                  "<a href=\"/yenilikler.html\" lang=\"tr\">News (Turkish)</a> · "
                  "<a href=\"mailto:destek@ayinedar.org\">destek@ayinedar.org</a></footer>")
BRAND_CATI = '<a class="brand" href="{home}"><img src="/icon.svg" alt="" width="32" height="32"><span class="ad">Âyinedâr</span></a>'


def nav_cati(current: str = "", other: str = "/en/", en: bool = False) -> str:
    items = NAV_CATI_EN if en else NAV_CATI
    links = "\n".join(f'  <a href="{href}"' + (' aria-current="page"' if href == current else "") + f">{name}</a>"
                      for href, name in items if href not in NAV_HIDDEN)
    lang, label, toggle = (("tr", "Türkçe", "Switch between light and dark mode") if en
                           else ("en", "English", "Açık ve koyu görünüm arasında geç"))
    return f"""<nav>
  {BRAND_CATI.format(home="/en/" if en else "/")}
{links}
  <a href="{other}" lang="{lang}">{label}</a>
  <button class="theme-toggle" type="button" data-theme-toggle aria-label="{toggle}" title="{toggle}"></button>
</nav>"""


NAV_HIDDEN: set[str] = set()           # yazısı henüz yayımlanmamış türün menü bağlantısı (build doldurur)


def nav_html(current: str = "", en: str = "/en/") -> str:
    links = "\n".join(f'  <a href="{href}"' + (' aria-current="page"' if href == current else "") + f">{name}</a>"
                      for href, name in NAV if href not in NAV_HIDDEN)
    return f"""<nav>
  <a class="brand" href="/"><img src="/icon.png" alt="">Risale-i Nur MCP</a>
{links}
  <a href="{en}" lang="en">English</a>
  <button class="theme-toggle" type="button" data-theme-toggle aria-label="Açık ve koyu görünüm arasında geç" title="Açık ve koyu görünüm arasında geç"></button>
</nav>"""


HEAD_CATI = """<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#1d4d3c">
<link rel="stylesheet" href="/style.css?v={v}">
<link rel="stylesheet" href="/ayinedar.css?v={v}">"""


def page(title: str, description: str, path: str, body: str, kind: str = "website", current: str = "",
         extra_head: str = "", robots: str = "", feed: Kind | None = None) -> str:
    """Çatının sayfası (yazılar, dizinler, önizleme). Önizlemede kanonik adres yok."""
    feed = feed or KINDS["yenilikler"]
    robots_tag = f'\n<meta name="robots" content="{robots}">' if robots else ""
    canonical = "" if robots else f'\n<link rel="canonical" href="{CATI_BASE}{path}">'
    return f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
{og_block(title, description, path, kind=kind, cati=True)}
<meta name="description" content="{html.escape(description)}">{robots_tag}{canonical}
{HEAD_CATI.format(v=ASSET_VERSION)}
<link rel="alternate" type="application/rss+xml" title="Âyinedâr: {feed.title}" href="/{feed.key}.xml">{extra_head}
<script>try{{var t=localStorage.getItem("theme");if(t==="light"||t==="dark")document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<script src="/site.js?v={ASSET_VERSION}" defer></script>
</head>
<body>
<main>
{nav_cati(current)}

{body}

{FOOTER_CATI}
</main>
</body>
</html>
"""


def _share_card(post: Post) -> str:
    if not post.share:
        return ""
    share = f"{post.share}\n{CATI_BASE}{post.path}"
    return f"""
<section class="card share">
  <h2>Paylaşın</h2>
  <pre>{html.escape(share)}</pre>
  <div class="actions">
    <button class="button" type="button" data-copy="{html.escape(share)}" data-done="Kopyalandı ✓">Metni kopyala</button>
    <a class="button primary" href="https://wa.me/?text={quote(share)}" rel="noopener">WhatsApp'ta paylaş</a>
  </div>
</section>"""


def _rel(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else path.name


def _preview_banner(post: Post) -> str:
    rel = _rel(post.source) if post.source else post.slug
    when = (f" <strong>{date_tr(post.scheduled)} günü kendiliğinden yayımlanacak.</strong>" if post.scheduled else "")
    return (f'<p class="note preview-banner"><strong>Önizleme: yayımlanmadı.</strong>{when} Bu sayfayı yalnız girişli '
            f"hesaplar görür. Kaynak <code>{rel}</code>; hemen yayımlamak için "
            f"<code>python3 scripts/site-uret.py yayinla {post.kind.key}/{post.slug}</code>.</p>\n")


def _toc(body_html: str) -> str:
    heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body_html)
    if len(heads) < 4:
        return ""
    items = "\n".join(f'  <li><a href="#{i}">{t}</a></li>' for i, t in heads)
    return f'<div class="toc" role="navigation" aria-label="İçindekiler"><p class="muted small">İçindekiler</p>\n<ol>\n{items}\n</ol></div>\n'


def post_page(post: Post, preview: bool = False) -> str:
    kind, banner = post.kind, _preview_banner(post) if preview else ""
    path = post.preview_path if preview else post.path
    if kind.key == "calismalar":
        content = cross_links(markdown(post.body))
        meta = f'<time datetime="{post.day.isoformat()}">{post.date_tr}</time>'
        if post.review and post.review != post.day:
            meta += f' · son gözden geçirme <time datetime="{post.review.isoformat()}">{date_tr(post.review)}</time>'
        meta += f" · ≈{post.minutes} dk okuma"
        last = post.review or post.day
        cite = (f"Âyinedâr, «{post.title}», {post.date_tr}"
                + (f" (son gözden geçirme {date_tr(last)})" if last != post.day else "") + f". {CATI_BASE}{post.path}")
        body = f"""{banner}<article class="post study">
<p class="muted small"><a href="{kind.index}">{kind.title}</a> · {meta}</p>
<h1>{inline(post.title)}</h1>
<p class="lead">{inline(post.summary)}</p>
{_toc(content)}{content}
</article>

<section class="card">
  <h2>Bu yazıya atıf</h2>
  <pre>{html.escape(cite)}</pre>
  <div class="actions"><button class="button" type="button" data-copy="{html.escape(cite)}" data-done="Kopyalandı ✓">Atfı kopyala</button></div>
  <p class="small muted">Yanlış ya da eksik gördüğünüz bir yer için: <a href="mailto:destek@ayinedar.org">destek@ayinedar.org</a>.</p>
</section>{_share_card(post)}"""
    else:
        body = f"""{banner}<article class="post">
<p class="muted small"><a href="{kind.index}">{kind.title}</a> · <time datetime="{post.day.isoformat()}">{post.date_tr}</time></p>
<h1>{inline(post.title)}</h1>
{cross_links(markdown(post.body))}
</article>
{_share_card(post)}"""
    return page(f"{post.title} · Âyinedâr", post.summary, path, body, kind="article",
                current=kind.index, robots="noindex" if preview else "", feed=kind)


def index_page(kind: Kind, posts: list[Post]) -> str:
    items = "\n".join(f"""<article class="post-item">
  <p class="muted small"><time datetime="{p.day.isoformat()}">{p.date_tr}</time>{f" · ≈{p.minutes} dk okuma" if kind.key == "calismalar" and not p.address else ""}</p>
  <h2><a href="{p.path}">{inline(p.title)}</a></h2>
  <p>{inline(p.summary)}</p>
</article>""" for p in posts) or '<p class="muted">Henüz yazı yok.</p>'
    body = f"""<h1>{kind.title}</h1>
<p class="lead">{kind.lead} <a href="/{kind.key}.xml">RSS</a> ile de takip edebilirsiniz.</p>

{items}"""
    return page(f"{kind.title} · Âyinedâr", kind.description, kind.index, body, current=kind.index, feed=kind)


def preview_index(drafts: list[Post]) -> str:
    items = "\n".join(f"""<article class="post-item">
  <p class="muted small">{p.kind.title} · taslak{f" · <strong>{date_tr(p.scheduled)} günü yayımlanacak</strong>" if p.scheduled else ""} · <code>{_rel(p.source) if p.source else p.slug}</code></p>
  <h2><a href="{p.preview_path}">{inline(p.title)}</a></h2>
  <p>{inline(p.summary)}</p>
  <p class="small muted">{"" if p.address else f'<a href="{PREVIEW_URL}/duzenle.html#{p.kind.key}/{p.slug}">Düzenle</a> · '}Hemen yayımlamak için: <code>python3 scripts/site-uret.py yayinla {p.kind.key}/{p.slug}</code></p>
</article>""" for p in drafts) or '<p class="muted">Bekleyen taslak yok.</p>'
    body = f"""<h1>Önizleme</h1>
<p class="lead">Yayımlanmamış Yenilikler ve Çalışmalar yazıları, sitedeki görünüşleriyle. Bu sayfayı yalnız girişli hesaplar görür.</p>

{items}"""
    return page("Önizleme · Âyinedâr", "Yayımlanmamış yazılar.", f"{PREVIEW_URL}/", body, robots="noindex")


def rss(kind: Kind, posts: list[Post]) -> str:
    def stamp(d: date) -> str:
        return format_datetime(datetime(d.year, d.month, d.day, 12, tzinfo=timezone.utc))
    items = "\n".join(f"""  <item>
    <title>{html.escape(p.title)}</title>
    <link>{CATI_BASE}{p.path}</link>
    <guid isPermaLink="false">{BASE}{p.path}</guid>
    <pubDate>{stamp(p.day)}</pubDate>
    <description>{html.escape(p.summary)}</description>
  </item>""" for p in posts)
    return f"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">
<channel>
  <title>Âyinedâr: {kind.title}</title>
  <link>{CATI_BASE}{kind.index}</link>
  <description>{html.escape(kind.description)}</description>
  <language>tr</language>
{items}
</channel>
</rss>
"""


# ---- elle yazılmış sayfalar: Open Graph ve şerit --------------------------------------------------------------

def _between(text: str, start: str, end: str, new: str, anchor: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if pattern.search(text):
        return pattern.sub(lambda _: new, text, count=1)
    if anchor not in text:
        raise SystemExit(f"çapa yok: {anchor!r}")
    return text.replace(anchor, anchor + "\n" + new, 1)


def add_og(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    title = re.search(r"<title>(.*?)</title>", text, re.S)
    desc = re.search(r'<meta name="description" content="(.*?)">', text, re.S)
    if not title or not desc:
        print(f"atlandı (başlık ya da açıklama yok): {path.relative_to(ROOT)}")
        return False
    lang = re.search(r'<html lang="(\w+)"', text).group(1)
    cati = path.is_relative_to(CATI)
    rel = "/" + path.relative_to(CATI if cati else SITE).as_posix()
    rel = rel[: -len("index.html")] if rel.endswith("index.html") else rel
    block = og_block(html.unescape(title.group(1)), html.unescape(desc.group(1)), rel, lang, cati=cati)
    new = _between(text, "<!-- og -->", "<!-- /og -->", block, title.group(0))
    if new != text:
        path.write_text(new, encoding="utf-8")
    return new != text


OLD_ICONS = ('<link rel="icon" type="image/png" sizes="256x256" href="/icon.png">\n'
             '<link rel="apple-touch-icon" href="/icon.png">')


def cati_head(text: str, path: Path) -> str:
    """Çatının sayfasının başı: Âyinedâr simgeleri, `ayinedar.css`, başlığın soneki, kanonik adres (noindex değilse).
    Başka betiğin ürettiği sayfa da (isarat-usul) böyle düzelir."""
    text = text.replace(OLD_ICONS, '<link rel="icon" href="/icon.svg" type="image/svg+xml">\n'
                                   '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
                                   '<meta name="theme-color" content="#1d4d3c">')
    text = re.sub(r"(<title>.*?) · Risale-i Nur MCP</title>", r"\1 · Âyinedâr</title>", text, count=1)
    if "/ayinedar.css" not in text:
        text = re.sub(r'(<link rel="stylesheet" href="/style.css\?v=\d+">)',
                      lambda m: m.group(1) + f'\n<link rel="stylesheet" href="/ayinedar.css?v={ASSET_VERSION}">', text,
                      count=1)
    rel = "/" + path.relative_to(CATI).as_posix()
    rel = rel[: -len("index.html")] if rel.endswith("index.html") else rel
    canonical = f'<link rel="canonical" href="{CATI_BASE}{rel}">'
    noindex = re.search(r'<meta name="robots" content="[^"]*noindex', text)
    text = re.sub(r'\n<link rel="canonical" href="[^"]*">', "", text)
    if not noindex and path.name != "404.html":
        text = re.sub(r'(<meta name="description" content="[^"]*">)', lambda m: m.group(1) + "\n" + canonical, text,
                      count=1)
    return text


def frame(path: Path, current: str | None = None) -> bool:
    """Türkçe elle yazılmış sayfanın menüsünü ve alt bilgisini ortak biçimle yeniden yazar."""
    text = path.read_text(encoding="utf-8")
    if path.is_relative_to(CATI):
        en = path.parent.name == "en"
        alt = re.search(rf'<link rel="alternate" hreflang="{"tr" if en else "en"}" href="([^"]+)">', text)
        cur = CURRENT_CATI_EN if en else CURRENT_CATI
        here = current if current is not None else cur.get(path.name, "")
        nav = nav_cati(here, alt.group(1) if alt else ("/" if en else "/en/"), en=en)
        footer = FOOTER_CATI_EN if en else FOOTER_CATI
    elif path.parent.name == "en":
        tr = re.search(r'<link rel="alternate" hreflang="tr" href="([^"]+)">', text)
        nav, footer = nav_en(CURRENT_EN.get(path.name, ""), tr.group(1) if tr else "/"), FOOTER_EN
    else:
        en = re.search(r'<link rel="alternate" hreflang="en" href="([^"]+)">', text)
        here = current if current is not None else CURRENT.get(path.name, "")
        nav, footer = nav_html(here, en.group(1) if en else "/en/"), FOOTER
    new = re.sub(r"<nav>.*?</nav>", lambda _: nav, text, count=1, flags=re.S)
    new = re.sub(r"<footer>.*?</footer>", lambda _: footer, new, count=1, flags=re.S)
    if path.is_relative_to(CATI):
        new = cati_head(new, path)
    if new != text:
        path.write_text(new, encoding="utf-8")
    return new != text


ROBOTS = '<meta name="robots" content="noindex">'


def set_noindex(path: Path, on: bool) -> bool:
    """`adres`li Çalışmalar kaydının sayfası: taslakken `noindex`, yayımlanınca değil."""
    text = path.read_text(encoding="utf-8")
    if on and ROBOTS not in text:
        new = text.replace('<meta name="description"', ROBOTS + '\n<meta name="description"', 1)
    elif not on:
        new = text.replace(ROBOTS + "\n", "").replace(ROBOTS, "")
    else:
        new = text
    if new != text:
        path.write_text(new, encoding="utf-8")
    return new != text


def address_file(address: str) -> Path:
    rel = address.lstrip("/")
    return CATI / (rel + "index.html" if rel.endswith("/") or not rel else rel)


def _about(n: int) -> str:
    """Yuvarlak sayı: 131.224 -> "131 bin", 6.236 -> "6.236"."""
    return f"{round(n / 1000)} bin" if n >= 20000 else f"{n:,}".replace(",", ".")


def numbers() -> dict[str, str]:
    import sqlite3
    out: dict[str, str] = {}
    dist = ROOT / "data" / "dist"
    if (db := dist / "genel" / "risale.db").exists():
        c = sqlite3.connect(db)
        rows = dict(((o, (w, s)) for o, w, s in c.execute(
            "select w.group_name = 'osmanlica', count(distinct w.slug), count(s.id) from works w "
            "left join sentences s on s.work = w.slug where w.built = 1 group by 1")))
        out |= {"risale_eser": str(rows[0][0]), "risale_cumle": _about(rows[0][1]),
                "osmanlica_cilt": str(rows[1][0]),
                "ayet": _about(c.execute("select count(*) from quran_ayahs").fetchone()[0])}
    if (db := dist / "tefsir" / "risale.db").exists():
        c = sqlite3.connect(db)
        out |= {"tefsir_eser": str(c.execute("select count(*) from works where built = 1").fetchone()[0]),
                "tefsir_cumle": _about(c.execute("select count(*) from sentences").fetchone()[0])}
    if (db := dist / "klasik" / "risale.db").exists():
        c = sqlite3.connect(db)
        out |= {"klasik_eser": str(c.execute("select count(*) from works where built = 1").fetchone()[0])}
    if (db := dist / "hadis" / "hadis.db").exists():
        c = sqlite3.connect(db)
        out |= {"hadis_kitap": str(c.execute("select count(*) from lib_books").fetchone()[0]),
                "hadis_sayi": _about(c.execute("select count(*) from lib_units").fetchone()[0])}
    for key, value in list(out.items()):         # İngilizce: "131 bin" -> "131,000", "6.236" -> "6,236"
        out[key + "_en"] = value.replace(" bin", ",000").replace(".", ",")
    return out


def fill_numbers(path: Path, values: dict[str, str]) -> bool:
    text = path.read_text(encoding="utf-8")
    def put(m: re.Match) -> str:
        return f"<!-- sayi:{m.group(1)} -->{values.get(m.group(1), m.group(2))}<!-- /sayi -->"
    new = re.sub(r"<!-- sayi:(\w+) -->(.*?)<!-- /sayi -->", put, text)
    if new != text:
        path.write_text(new, encoding="utf-8")
    return new != text


def latest_list(posts: list[Post], base: str = "") -> str:
    items = "\n".join(f'  <li><a href="{base}{p.path}">{inline(p.title)}</a> <span class="muted small">· {p.date_tr}</span>'
                      f"<br><span class=\"small\">{inline(p.summary)}</span></li>" for p in posts[:3])
    return f'<!-- son-yenilikler -->\n<ul class="news">\n{items}\n</ul>\n<!-- /son-yenilikler -->'


def sitemap(pages: list[Path], posts: list[Post], cati: bool) -> str:
    root, base, urls = (CATI, CATI_BASE, []) if cati else (SITE, BASE, [])
    for page_path in pages:
        rel = "/" + page_path.relative_to(root).as_posix()
        urls.append(rel[: -len("index.html")] if rel.endswith("index.html") else rel)
    if cati:
        urls += [k.index for k in KINDS.values() if k.index not in NAV_HIDDEN] + [p.path for p in posts]
    body = "\n".join(f"  <url><loc>{base}{u}</loc></url>" for u in dict.fromkeys(urls))
    return (f'<?xml version="1.0" encoding="utf-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{body}\n</urlset>\n")


def latest_strip(post: Post, base: str = "") -> str:
    return (f'<!-- son-yenilik -->\n<p class="note small"><strong>Yeni:</strong> <a href="{base}{post.path}">'
            f"{inline(post.title)}</a> · {post.date_tr}</p>\n<!-- /son-yenilik -->")


def _target(root: Path, href: str) -> Path:
    target = root / href.lstrip("/")
    return target / "index.html" if href.endswith("/") else target


def cross_links(body: str) -> str:
    """Yazının çatıda olmayan ama risalemcp.com'da olan iç bağlantısı (eklenti sayfaları, kurulum) tam adres olur."""
    def fix(m: re.Match) -> str:
        href = m.group(1)
        path = href.split("#", 1)[0].split("?", 1)[0]
        owned = path.startswith(tuple(f"/{k}" for k in KINDS)) or path.startswith("/isarat-usul") or path == "/"
        if not owned and path and _target(SITE, path).exists() and not _target(CATI, path).exists():
            return f'href="{BASE}{href}"'
        return m.group(0)
    return re.sub(r'href="(/[^"]*)"', fix, body)


def broken_links(text: str, root: Path = CATI) -> list[str]:
    """Sayfadaki iç bağlantılardan sitesinde karşılığı olmayanlar (önizleme ve girişli bölüm sayılmaz)."""
    bad = []
    for href in re.findall(r'href="(/[^"#?]*)', text):
        if href.startswith((PREVIEW_URL + "/", "/taslak/", "/oku/")) or href in ("/",):
            continue
        target = root / href.lstrip("/")
        if href.endswith("/"):
            target = target / "index.html"
        if not target.exists():
            bad.append(href)
    return sorted(set(bad))


# ---- paylaşım resmi -------------------------------------------------------------------------------------------

def share_image() -> None:
    icon = (ROOT / "src/risale_mcp/static/icon.svg").read_text(encoding="utf-8")
    icon = icon.replace('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">',
                        '<svg x="96" y="187" width="256" height="256" viewBox="0 0 256 256">')
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <rect width="1200" height="630" fill="#141917"/>
  <rect x="0" y="600" width="1200" height="30" fill="#1d4d3c"/>
  {icon}
  <g font-family="DejaVu Sans" fill="#e8ece9">
    <text x="410" y="270" font-size="64" font-weight="bold">Risale-i Nur MCP</text>
    <text x="412" y="340" font-size="38" fill="#e8c766">Risale-i Nur · Hadis · Tefsir</text>
    <text x="412" y="410" font-size="28" fill="#a3ada7">Yapay zekâya metinden ayrılmadan,</text>
    <text x="412" y="450" font-size="28" fill="#a3ada7">her alıntı cümle düzeyinde adresli</text>
  </g>
  <text x="1104" y="560" font-family="DejaVu Sans" font-size="26" fill="#7cc59d" text-anchor="end">risalemcp.com</text>
</svg>"""
    target = SITE / IMAGE.lstrip("/")
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "paylasim.svg"
        src.write_text(svg, encoding="utf-8")
        subprocess.run(["uvx", "-q", "--from", "cairosvg", "cairosvg", str(src), "-o", str(target)], check=True)
    print(f"yazıldı: {target.relative_to(ROOT)} ({target.stat().st_size // 1024} KB)")


# ---- ana akış -------------------------------------------------------------------------------------------------

def _old_posts(say) -> None:
    """S13.15.6: yazılar çatıya taşındı; site/'taki eski kopyaları silinir (adresleri Caddy 308 ile çatıya gönderir)."""
    for key in KINDS:
        for old in [SITE / f"{key}.html", SITE / f"{key}.xml", *sorted((SITE / key).glob("*.html"))]:
            if old.exists():
                old.unlink()
                say(f"silindi (çatıya taşındı): {old.relative_to(ROOT)}")
        if (SITE / key).is_dir() and not any((SITE / key).iterdir()):
            (SITE / key).rmdir()


def handmade_pages(root: Path) -> list[Path]:
    """Elle yazılmış sayfalar (yazıların dizinleri hariç), kök ve en/."""
    return [p for p in sorted(root.glob("*.html")) + sorted((root / "en").glob("*.html"))
            if p.name not in {f"{k}.html" for k in KINDS}]


def build(quiet: bool = False) -> dict[str, list[Post]]:
    say = (lambda *_: None) if quiet else print
    everything = {key: read_posts(kind) for key, kind in KINDS.items()}
    published = {key: [p for p in posts if not p.draft] for key, posts in everything.items()}
    drafts = [p for posts in everything.values() for p in posts if p.draft]
    NAV_HIDDEN.clear()
    NAV_HIDDEN.update(k.index for key, k in KINDS.items() if not published[key])
    _old_posts(say)
    for rel in SHARED:                                    # çatının ortak stil, betik ve yazı tipi: site/'tan
        (CATI / rel).parent.mkdir(parents=True, exist_ok=True)
        if not (CATI / rel).exists() or (CATI / rel).read_bytes() != (SITE / rel).read_bytes():
            shutil.copyfile(SITE / rel, CATI / rel)
            say(f"kopyalandı: {rel} → {CATI.relative_to(ROOT)}/")

    written: list[Path] = []
    for key, kind in KINDS.items():
        posts = published[key]
        kind.out.mkdir(exist_ok=True)
        keep = {f"{p.slug}.html" for p in posts if not p.address}
        for old in kind.out.glob("*.html"):
            if old.name not in keep:
                old.unlink()
                say(f"silindi: {old.relative_to(ROOT)}")
        for post in posts:
            if not post.address:
                target = kind.out / f"{post.slug}.html"
                target.write_text(post_page(post), encoding="utf-8")
                written.append(target)
        (CATI / f"{key}.html").write_text(index_page(kind, posts), encoding="utf-8")
        (CATI / f"{key}.xml").write_text(rss(kind, posts), encoding="utf-8")
        written.append(CATI / f"{key}.html")
        say(f"{kind.title}: {len(posts)} yazı yayında, {sum(p.draft for p in everything[key])} taslak")

    # önizleme: yalnız taslaklar (her seferinde baştan)
    if PREVIEW.exists():
        shutil.rmtree(PREVIEW)
    for post in drafts:
        if post.address:
            continue
        target = PREVIEW / post.kind.key / f"{post.slug}.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(post_page(post, preview=True), encoding="utf-8")
    PREVIEW.mkdir(parents=True, exist_ok=True)
    (PREVIEW / "index.html").write_text(preview_index(drafts), encoding="utf-8")
    # S11: web düzenleyici (girişli; veri masa servisinden, src/risale_mcp/yazilar.py)
    shutil.copyfile(ROOT / "scripts" / "yazi-duzenle.html", PREVIEW / "duzenle.html")
    # ar-ge masasının giriş sayfası (Okumalar sekmesi) okunacak yazı taslaklarını buradan listeler
    (PREVIEW / "liste.json").write_text(json.dumps([
        {"tur": p.kind.title, "baslik": p.title, "ozet": p.summary, "sayfa": p.preview_path,
         "duzenle": None if p.address else f"{PREVIEW_URL}/duzenle.html#{p.kind.key}/{p.slug}",
         "kaynak": _rel(p.source) if p.source else p.slug, "ad": f"{p.kind.key}/{p.slug}",
         "yayin_tarihi": p.scheduled.isoformat() if p.scheduled else None} for p in drafts],
        ensure_ascii=False, indent=1), encoding="utf-8")
    say(f"önizleme: {len(drafts)} taslak, {PREVIEW.relative_to(ROOT)}/ → lab.ayinedar.org{PREVIEW_URL}/")

    # `adres`li Çalışmalar kayıtları (başka betiğin sayfası, çatıda): yayımlanmışsa dizine açık, taslaksa noindex
    addressed = {address_file(p.address): p for posts in everything.values() for p in posts if p.address}
    for path, post in addressed.items():
        if not path.exists():
            sys.exit(f"{post.slug}: adres {post.address} için sayfa yok ({path.relative_to(ROOT)})")
        if set_noindex(path, post.draft):
            say(f"{'noindex kondu' if post.draft else 'noindex kalktı'}: {path.relative_to(ROOT)}")

    values = numbers()
    currents = {path: post.kind.index for path, post in addressed.items()}
    for root, cati in ((SITE, False), (CATI, True)):
        handmade = handmade_pages(root)
        subpages = sorted(p for p in root.glob("*/*.html") if p.parent.name not in {"en", *KINDS})
        changed = sum(add_og(p) for p in handmade + subpages)
        name = root.relative_to(ROOT)
        say(f"{name}: Open Graph {len(handmade + subpages)} sayfa, {changed} değişti; menü ve alt bilgi "
            f"{sum(frame(p, currents.get(p)) for p in handmade + subpages)} değişti; sayılar "
            f"{sum(fill_numbers(p, values) for p in handmade)} değişti")
        listed = [p for p in subpages if p in addressed and not addressed[p].draft]
        pages = [p for p in handmade + listed if p.name != "404.html"]
        posts = [p for ps in published.values() for p in ps if not p.address] if cati else []
        (root / "sitemap.xml").write_text(sitemap(pages, posts, cati), encoding="utf-8")
        written += [] if cati else handmade

    news = published["yenilikler"]
    for index, base in ((SITE / "index.html", CATI_BASE), (CATI / "index.html", "")):
        if not news or not index.exists():
            continue
        text = index.read_text(encoding="utf-8")
        new = text
        if "<!-- son-yenilik -->" in new or '<section class="hero">' in new:
            new = _between(new, "<!-- son-yenilik -->", "<!-- /son-yenilik -->", latest_strip(news[0], base),
                           '<section class="hero">')
        if "<!-- son-yenilikler -->" in new:
            new = _between(new, "<!-- son-yenilikler -->", "<!-- /son-yenilikler -->", latest_list(news, base), "")
        if new != text:
            index.write_text(new, encoding="utf-8")
            say(f"{index.relative_to(ROOT)}: yenilikler güncellendi")

    for path in written + handmade_pages(CATI):
        root = CATI if path.is_relative_to(CATI) else SITE
        if bad := broken_links(path.read_text(encoding="utf-8"), root):
            print(f"uyarı: {path.relative_to(ROOT)}: kırık iç bağlantı: {', '.join(bad)}")
    return everything


def find_post(name: str) -> Post:
    """Yayımlanacak taslak: `ad`, `tarih-ad` ya da türüyle `calismalar/ad` (aynı ad iki türde olabilir)."""
    kind_key, _, name = name.rpartition("/")
    kinds = [KINDS[kind_key]] if kind_key in KINDS else list(KINDS.values())
    found = [p for kind in kinds for p in read_posts(kind) if p.draft
             and (p.slug == name or re.sub(r"^\d{4}-\d{2}-\d{2}-", "", p.slug) == name)]
    if len(found) != 1:
        sys.exit(f"{name}: {'taslak bulunamadı' if not found else 'birden çok taslak (türüyle yazın, ör. calismalar/ad): ' + ', '.join(f'{p.kind.key}/{p.slug}' for p in found)}")
    return found[0]


def _set_meta(text: str, key: str, value: str | None) -> str:
    """Üst bilgide bir alanı yazar; `value` None ise siler."""
    head, sep, rest = text.partition("\n---\n")
    if value is None:
        head = re.sub(rf"\n{key}:.*$", "", head, count=1, flags=re.M)
    elif re.search(rf"^{key}:.*$", head, re.M):
        head = re.sub(rf"^{key}:.*$", f"{key}: {value}", head, count=1, flags=re.M)
    else:
        head += f"\n{key}: {value}"
    return head + sep + rest


def _move(src: Path, dst: Path) -> None:
    tracked = subprocess.run(["git", "ls-files", "--error-unmatch", str(src)], cwd=ROOT,
                             capture_output=True).returncode == 0
    if tracked:
        subprocess.run(["git", "mv", str(src), str(dst)], cwd=ROOT, check=True)
    else:
        src.rename(dst)


def publish_post(post: Post) -> list[Path]:
    """Taslağı yayına alır (dosya düzeyinde; siteyi kurmaz): durum, tarih bugün, dosya adı bugünün tarihiyle.
    Değişen ya da yazılan dosyaları döndürür."""
    if not post.address:                                  # önce önizlemedeki bağlantılar
        build(quiet=True)
        preview = PREVIEW / post.kind.key / f"{post.slug}.html"
        if bad := broken_links(preview.read_text(encoding="utf-8")):
            sys.exit(f"{post.slug}: kırık iç bağlantı, yayımlanmadı: {', '.join(bad)}")
    today = date.today().isoformat()
    rest = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", post.slug)
    text = post.source.read_text(encoding="utf-8")
    text = _set_meta(_set_meta(_set_meta(text, "durum", "yayinda"), "tarih", today), "yayin_tarihi", None)
    target = post.source.with_name(f"{today}-{rest}.md")
    changed = [post.source, target]
    if target != post.source:
        if target.exists():
            sys.exit(f"{target.relative_to(ROOT)} zaten var")
        _move(post.source, target)
    target.write_text(text, encoding="utf-8")
    print(f"yayında: {target.relative_to(ROOT)}")
    if post.kind.key == "calismalar":                     # Yeniliklere kısa duyuru, taslak olarak
        note = KINDS["yenilikler"].src / f"{today}-{rest}.md"
        if not note.exists():
            url = post.address or f"/calismalar/{today}-{rest}.html"
            summary = post.summary.replace("\n", " ")
            note.write_text(f"""---
baslik: Yeni çalışma: {post.title}
tarih: {today}
ozet: {summary}
durum: taslak
whatsapp: |
  Âyinedâr'da yeni bir çalışma: «{post.title}».
  {summary}
---

Çalışmalar kısmına yeni bir yazı eklendi: **{post.title}**.

{summary}

[Yazının tamamı]({url})
""", encoding="utf-8")
            changed.append(note)
            print(f"Yeniliklere duyuru taslağı: {note.relative_to(ROOT)} (bakıp `yayinla yenilikler/{rest}` ile yayımlayın)")
    return changed


# ---- S11: web'de düzeltilen taslaklar (src/risale_mcp/yazilar.py) ------------------------------------------------

WEB_HOST = os.environ.get("RISALE_HOST", "root@100.108.174.19")
WEB_KEY = os.environ.get("RISALE_KEY", str(Path.home() / ".ssh" / "risale_hetzner"))


def _sha(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]


def pull_web(only: set[str] | None = None, commit: bool = False) -> list[Path]:
    """Web düzenleyicideki son sürümleri depodaki dosyalara yazar (sunucudan SSH ile `yazilar disa`). Yerel dosya web
    sürümlerinin başladığı metin ya da onlardan biriyse ileri sarılır; değilse (iki yerde de değişmiş) durur, web
    sürümü `<ad>.web.md` olarak yanına yazılır. Değişen dosyaları döndürür."""
    cmd = ["ssh", "-i", WEB_KEY, "-o", "BatchMode=yes", "-o", "ConnectTimeout=15", WEB_HOST,
           "cd /home/risale/risale-mcp && sudo -u risale .venv/bin/python -m risale_mcp.yazilar disa"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"web düzeltmeleri alınamadı (sunucuya bağlanılamadı ya da hata): {r.stderr.strip()[-300:]}")
    data = json.loads(r.stdout or "{}")
    changed, conflicts = [], []
    for ad, v in data.items():
        if only is not None and ad not in only:
            continue
        kind, _, slug = ad.partition("/")
        path = ROOT / "docs" / kind / f"{slug}.md"
        if kind not in KINDS or not path.exists():          # yayımlanıp adı değişmiş ya da silinmiş
            continue
        local = path.read_text(encoding="utf-8")
        if _sha(local) == v["sha"]:
            continue
        if _sha(local) not in v["bilinen"]:
            path.with_suffix(".web.md").write_text(v["metin"], encoding="utf-8")
            conflicts.append(ad)
            continue
        import difflib
        diff = list(difflib.unified_diff(local.splitlines(), v["metin"].splitlines(), "depo", f"web sürüm {v['surum']}",
                                         lineterm="", n=0))
        path.write_text(v["metin"], encoding="utf-8")
        changed.append(path)
        print(f"{ad}: web sürümü {v['surum']} alındı ({sum(1 for x in diff if x[:1] in '+-') - 2} satır farkı)")
    if conflicts:
        sys.exit("hem depoda hem web'de değişmiş (web sürümü yanına .web.md olarak yazıldı, birleştirip yeniden "
                 "deneyin): " + ", ".join(conflicts))
    if commit and changed:
        rel = [str(p.relative_to(ROOT)) for p in changed]
        subprocess.run(["git", "add", "--", *rel], cwd=ROOT, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "site: web düzeltmeleri alındı (" + ", ".join(p.stem for p in changed) + ")",
                        "--", *rel], cwd=ROOT, check=False)
    if not changed:
        print("web'de alınacak düzeltme yok")
    return changed


def publish(name: str, send: bool) -> None:
    post = find_post(name)
    if pull_web({f"{post.kind.key}/{post.slug}"}):
        post = find_post(name)
    publish_post(post)
    build()
    if send:
        subprocess.run([str(ROOT / "scripts" / "deploy.sh"), "--site"], cwd=ROOT, check=True)
    else:
        print("göndermek için: scripts/deploy.sh --site")


def schedule(name: str, day: str) -> None:
    """Taslağa yayın günü koyar (`yayin_tarihi`); `iptal` kaldırır. Önce web düzeltmeleri alınır (S11)."""
    post = find_post(name)
    if pull_web({f"{post.kind.key}/{post.slug}"}, commit=True):
        post = find_post(name)
    value = None if day == "iptal" else date.fromisoformat(day).isoformat()
    post.source.write_text(_set_meta(post.source.read_text(encoding="utf-8"), "yayin_tarihi", value), encoding="utf-8")
    print(f"{post.kind.key}/{post.slug}: " + (f"{value} günü yayımlanacak" if value else "yayın günü kaldırıldı"))
    build(quiet=True)


def _notify(text: str) -> None:
    print(text)
    if shutil.which("notify-send"):
        subprocess.run(["notify-send", "Risale MCP sitesi", text], check=False)


def publish_due(send: bool) -> None:
    """Yayın günü gelmiş taslakları yayımlar; değişenleri commit eder, `--gonder` ile siteyi gönderir
    (`scripts/deploy.sh --site`: yalnız site ve önizleme; kod gitmez). Günlük zamanlayıcı çağırır
    (`docs/site-zamanli.timer`, `systemd --user`; makine kapalıysa açılınca)."""
    today = date.today()
    due = [p for kind in KINDS.values() for p in read_posts(kind) if p.draft and p.scheduled and p.scheduled <= today]
    if not due:
        print(f"{today}: yayın günü gelmiş taslak yok")
        return
    try:                                                  # S11: web'de yapılan son düzeltmeler önce
        pulled = pull_web({f"{p.kind.key}/{p.slug}" for p in due})
    except SystemExit as e:
        _notify(f"Zamanlı yayın durdu: {e}")
        raise
    if pulled:
        due = [p for kind in KINDS.values() for p in read_posts(kind) if p.draft and p.scheduled and p.scheduled <= today]
    changed: list[Path] = list(pulled)
    for post in due:
        changed += publish_post(post)
    build()
    def git_ok(*args: str) -> bool:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True).returncode == 0
    # `git add` yalnız diskte ya da dizinde olan yolu alır; `git mv` ile taşınan eski dosya ikisinde de yoktur ama
    # HEAD'dedir: silinişi commit'e o yolla girer (önceden dışarıda kalıyordu, 2026-11-24)
    rel = {str(p.relative_to(ROOT)) for p in changed}
    add = sorted({r for r in rel if (ROOT / r).exists() or git_ok("ls-files", "--error-unmatch", r)} | {"site"})
    paths = sorted(set(add) | {r for r in rel if git_ok("cat-file", "-e", f"HEAD:{r}")})
    subprocess.run(["git", "add", "-A", "--", *add], cwd=ROOT, check=True)
    titles = ", ".join(f"«{p.title}»" for p in due)
    subprocess.run(["git", "commit", "-q", "-m", f"site: scheduled publish of {', '.join(p.slug for p in due)}",
                    "--", *paths], cwd=ROOT, check=False)
    if send:
        done = subprocess.run([str(ROOT / "scripts" / "deploy.sh"), "--site"], cwd=ROOT).returncode == 0
        _notify(f"Yayımlandı: {titles}" if done else f"Yayımlandı ama gönderilemedi: {titles} (scripts/deploy.sh --site)")
    else:
        _notify(f"Yayımlandı (gönderilmedi): {titles}")


def serve(port: int = 8090) -> None:
    """Yerel önizleme: çatı (site-ayinedar/) ve önizleme klasörü tek kökte (bağlantılar sitedeki gibi çalışır)."""
    import functools
    import http.server
    build()
    root = Path(tempfile.mkdtemp(prefix="site-onizle-"))
    for item in CATI.iterdir():
        (root / item.name).symlink_to(item)
    (root / "onizleme").symlink_to(PREVIEW)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
    print(f"önizleme: http://127.0.0.1:{port}{PREVIEW_URL}/ (durdurmak için Ctrl+C)")
    http.server.ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()


def main() -> None:
    args = sys.argv[1:]
    if "--resim" in args:
        share_image()
        args.remove("--resim")
    if args[:1] == ["yayinla"]:
        if len(args) < 2:
            sys.exit("kullanım: site-uret.py yayinla <ad> [--gonder]")
        publish(args[1], "--gonder" in args)
    elif args[:1] == ["zamanla"]:
        if len(args) != 3:
            sys.exit("kullanım: site-uret.py zamanla <ad> <YYYY-AA-GG | iptal>")
        schedule(args[1], args[2])
    elif args[:1] == ["zamanli"]:
        publish_due("--gonder" in args)
    elif args[:1] == ["cek"]:
        pull_web(commit=True)
    elif args[:1] == ["onizle"]:
        serve()
    elif not args:
        build()
    else:
        sys.exit(f"bilinmeyen: {' '.join(args)}")


if __name__ == "__main__":
    main()
