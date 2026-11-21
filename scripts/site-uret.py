#!/usr/bin/env python3
"""Sitenin üretilen parçaları (PLANLAR.md S1, S2, S9): Yenilikler, Çalışmalar, önizleme, Open Graph, menü ve alt
bilgi, sayılar, site haritası.

    python3 scripts/site-uret.py                    # hepsi (taslaklar yalnız önizlemeye)
    python3 scripts/site-uret.py --resim            # bir de paylaşım resmi (site/img/paylasim.png; uvx cairosvg)
    python3 scripts/site-uret.py onizle             # üretir ve yerelde açar: http://127.0.0.1:8090/taslak/onizleme/
    python3 scripts/site-uret.py yayinla <ad>       # taslağı yayımlar (durum, tarih, dosya adı; bağlantı denetimi)
    python3 scripts/site-uret.py yayinla <ad> --gonder   # … ve scripts/deploy.sh --code

Sonra: scripts/deploy.sh --code (önizleme de onunla gider: risalemcp.com/taslak/onizleme/, girişli, masa hesabı)

- İki tür yazı (`KINDS`): **Yenilikler** `docs/yenilikler/<tarih>-<ad>.md` (eklentide ne değişti; kısa) ve
  **Çalışmalar** `docs/calismalar/<tarih>-<ad>.md` (ne denendi, ne öğrenildi; uzun, kaynaklı; S9). site/ olduğu gibi
  yayımlandığı için kaynak orada durmaz. Üst bilgi: `baslik`, `tarih` (YYYY-AA-GG), `ozet` (dizinde ve önizlemede),
  `whatsapp` (`|` ile çok satırlı; paylaşım kutusundaki metin, sonuna yazının adresi eklenir; Yeniliklerde zorunlu),
  `durum` (`taslak` | `yayinda`; yoksa `yayinda`), Çalışmalarda isteğe bağlı `gozden_gecirme` (son gözden geçirme
  tarihi) ve `adres` (yazı başka bir betiğin ürettiği sayfaysa, ör. `/isarat-usul/`: gövdesi yoktur, yalnız listede
  durur; yayımlanınca o sayfanın `noindex`i kalkar ve site haritasına girer, taslakken `noindex` kalır).
- Gövde sade Markdown: `##`, `###`, paragraf, `-` ve `1.` listeleri, `>` alıntı, `**kalın**`, `*eğik*`, `` `kod` ``,
  `[metin](adres)`, `---` çizgi, `|` tablo (ikinci satır `|---|`), kutu (`:::kisa` … `:::`: "Kısa cevap";
  `:::not Başlık` … `:::`). Arapça kendiliğinden işaretlenir: çoğu Arapça olan alıntı ve paragraf sağdan sola,
  metin içindeki Arapça `lang="ar"` (sitenin Naskh yazı tipi, `site/fonts/naskh.woff2`).
- **Taslak** yazı `site/`'a yazılmaz; listeye, RSS'e, site haritasına, ana sayfa şeridine girmez. Önizlemesi
  `data/interim/onizleme/<tür>/<ad>.html`'dedir (sitedeki görünüşüyle, başında önizleme şeridi, `noindex`); deploy onu
  girişli `/taslak/onizleme/`'ye gönderir. `yayinla`: önce önizlemedeki iç bağlantılar denetlenir (yoksa durur), sonra
  `durum: yayinda`, `tarih` bugün, dosya adı bugünün tarihiyle (adres yayından sonra değişmez); Çalışmalar yazısıysa
  Yeniliklere kısa duyuru **taslak** olarak yazılır (o da `yayinla` ile).
- Çıktı: `site/<tür>/<ad>.html`, `site/<tür>.html` (en yeni üstte), `site/<tür>.xml` (RSS 2.0).
- Open Graph: `site/` ve `site/en/` altındaki her sayfada `<!-- og -->` ile `<!-- /og -->` arası her seferinde
  yeniden yazılır (yoksa `</title>` satırından sonra eklenir); başlık `<title>`'dan, açıklama `description`'dan.
  WhatsApp önizlemeyi adres başına önbelleğe alır: etiket değişince eski paylaşımlar bir süre eski görünür.
- Ana sayfa (`site/index.html`): `<!-- son-yenilik -->` arasında son yazıya şerit, `<!-- son-yenilikler -->` arasında
  son üç yazı.
- Menü ve alt bilgi: sayfaların `<nav>` ve `<footer>` blokları her seferinde buradan yazılır (`nav_html`, `FOOTER`;
  İngilizcede `nav_en`, `FOOTER_EN`). Öbür dile giden bağlantı sayfanın `hreflang` adresidir.
- Sayılar: sayfalardaki `<!-- sayi:ad -->…<!-- /sayi -->` arası yerel veritabanlarından (`data/dist/`) yazılır
  (`numbers`; İngilizce sayfalarda `ad_en`: "131,000"); veritabanı yoksa olduğu gibi kalır.
- `site/sitemap.xml`: bütün sayfalar ve yayımlanmış yazılar. Alt klasördeki sayfalar (ör. `scripts/d1-okur.py`'nin
  ürettiği `site/isarat-usul/`) menü, alt bilgi ve Open Graph alır; haritaya yalnız bir Çalışmalar kaydı (`adres`)
  yayımlanmışsa girer.
- Dışarıya istek yok kuralı sürer: "WhatsApp'ta paylaş" yalnız tıklanınca açılan bir bağlantıdır.
"""

import html
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
SITE = ROOT / "site"
PREVIEW = ROOT / "data" / "interim" / "onizleme"     # deploy: /var/www/ozel/taslak/onizleme/ (girişli)
PREVIEW_URL = "/taslak/onizleme"
BASE = "https://risalemcp.com"
IMAGE = "/img/paylasim.png"
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
        return SITE / self.key

    @property
    def index(self) -> str:
        return f"/{self.key}.html"


KINDS = {
    "yenilikler": Kind("yenilikler", "Yenilikler",
                       "Eklentilerde yeni olanlar, iyileştirmeler ve duyurular. Her yazının sonunda paylaşmak için kısa "
                       "bir metin var.",
                       "Risale-i Nur, Hadis ve Tefsir eklentilerinde yeni olanlar, iyileştirmeler ve duyurular.",
                       frozenset({"baslik", "tarih", "ozet", "whatsapp"})),
    "calismalar": Kind("calismalar", "Çalışmalar",
                       "Projenin ne denediği ve ne öğrendiği: usul, ölçüler, sonuçlar ve sınırlar. Uzun ve kaynaklı "
                       "yazılar; hiçbiri tefsir değildir.",
                       "Risale-i Nur MCP'nin çalışmaları: İşârâtü'l-İ'câz'ın usulü, yapay zekâ taslakları, ölçüler, "
                       "sonuçlar ve sınırlar.",
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
    text = path.read_text(encoding="utf-8")
    meta, end = front_matter(text, path.name)
    missing = kind.required - set(meta)
    if missing:
        sys.exit(f"{path.name}: eksik üst bilgi: {', '.join(sorted(missing))}")
    status = meta.get("durum", "yayinda").strip()
    if status not in STATUSES:
        sys.exit(f"{path.name}: durum {status!r} (taslak ya da yayinda olmalı)")
    review = date.fromisoformat(meta["gozden_gecirme"]) if meta.get("gozden_gecirme") else None
    return Post(kind, path.stem, meta["baslik"], date.fromisoformat(meta["tarih"]), meta["ozet"],
                meta.get("whatsapp", "").strip(), text[end:], status, review, meta.get("adres") or None, path)


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

def og_block(title: str, description: str, path: str, lang: str = "tr", kind: str = "website") -> str:
    tags = [("og:type", kind), ("og:site_name", "Risale-i Nur MCP"), ("og:title", title),
            ("og:description", description), ("og:url", BASE + path), ("og:image", BASE + IMAGE),
            ("og:image:width", "1200"), ("og:image:height", "630"),
            ("og:image:alt", "Risale-i Nur MCP: Risale-i Nur, Hadis ve Tefsir eklentileri" if lang == "tr"
             else "Risale-i Nur MCP: the Risale-i Nur, hadith and tafsir connectors"),
            ("og:locale", "tr_TR" if lang == "tr" else "en_US")]
    lines = [f'<meta property="{k}" content="{html.escape(v)}">' for k, v in tags]
    lines.append('<meta name="twitter:card" content="summary_large_image">')
    return "<!-- og -->\n" + "\n".join(lines) + "\n<!-- /og -->"


NAV = [("/#eklentiler", "Eklentiler"), ("/#ekle", "Kurulum"), ("/yenilikler.html", "Yenilikler"),
       ("/calismalar.html", "Çalışmalar"), ("/belgeler.html", "Belgeler")]
# Sayfa -> menüde işaretli olan (sayfa adı; yazılar "yenilikler")
CURRENT = {"risale.html": "/#eklentiler", "hadis.html": "/#eklentiler", "tefsir.html": "/#eklentiler",
           "klasik.html": "/#eklentiler",
           "claude.html": "/#ekle", "chatgpt.html": "/#ekle", "yenilikler.html": "/yenilikler.html",
           "calismalar.html": "/calismalar.html",
           "belgeler.html": "/belgeler.html"}
FOOTER = ("<footer>Risale MCP: gönüllü ve bağımsız bir projedir; herhangi bir yayınevi ya da cemaatin resmî hizmeti "
          "değildir.<br><a href=\"/gizlilik.html\">Gizlilik</a> · <a href=\"/kullanim-sartlari.html\">Kullanım "
          "şartları</a> · <a href=\"/katki.html\">Hata bildirin</a> · <a href=\"/yenilikler.xml\">RSS</a> · "
          "<a href=\"mailto:destek@risalemcp.com\">destek@risalemcp.com</a></footer>")


NAV_EN = [("/en/#connectors", "Connectors"), ("/en/#add", "Setup"), ("/en/docs.html", "Documentation")]
CURRENT_EN = {"risale.html": "/en/#connectors", "hadith.html": "/en/#connectors", "tafsir.html": "/en/#connectors",
              "classical.html": "/en/#connectors",
              "claude.html": "/en/#add", "chatgpt.html": "/en/#add", "docs.html": "/en/docs.html"}
FOOTER_EN = ("<footer>Risale MCP: a volunteer, independent project, not an official service of any publisher or "
             "community.<br><a href=\"/en/privacy.html\">Privacy</a> · <a href=\"/en/terms.html\">Terms of use</a> · "
             "<a href=\"/en/contribute.html\">Report a mistake</a> · <a href=\"/yenilikler.html\" lang=\"tr\">News "
             "(Turkish)</a> · <a href=\"mailto:destek@risalemcp.com\">destek@risalemcp.com</a></footer>")


def nav_en(current: str = "", tr: str = "/") -> str:
    links = "\n".join(f'  <a href="{href}"' + (' aria-current="page"' if href == current else "") + f">{name}</a>"
                      for href, name in NAV_EN)
    return f"""<nav>
  <a class="brand" href="/en/"><img src="/icon.png" alt="">Risale-i Nur MCP</a>
{links}
  <a href="{tr}" lang="tr">Türkçe</a>
  <button class="theme-toggle" type="button" data-theme-toggle aria-label="Switch between light and dark mode" title="Switch between light and dark mode"></button>
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


def page(title: str, description: str, path: str, body: str, kind: str = "website", current: str = "",
         extra_head: str = "", robots: str = "", feed: Kind | None = None) -> str:
    feed = feed or KINDS["yenilikler"]
    robots_tag = f'\n<meta name="robots" content="{robots}">' if robots else ""
    return f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
{og_block(title, description, path, kind=kind)}
<meta name="description" content="{html.escape(description)}">{robots_tag}
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="256x256" href="/icon.png">
<link rel="apple-touch-icon" href="/icon.png">
<link rel="stylesheet" href="/style.css?v={ASSET_VERSION}">
<link rel="alternate" type="application/rss+xml" title="Risale-i Nur MCP: {feed.title}" href="/{feed.key}.xml">{extra_head}
<script>try{{var t=localStorage.getItem("theme");if(t==="light"||t==="dark")document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<script src="/site.js?v={ASSET_VERSION}" defer></script>
</head>
<body>
<main>
{nav_html(current)}

{body}

{FOOTER}
</main>
</body>
</html>
"""


def _share_card(post: Post) -> str:
    if not post.share:
        return ""
    share = f"{post.share}\n{BASE}{post.path}"
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
    return (f'<p class="note preview-banner"><strong>Önizleme: yayımlanmadı.</strong> Bu sayfayı yalnız girişli '
            f"hesaplar görür. Kaynak <code>{rel}</code>; yayımlamak için "
            f"<code>python3 scripts/site-uret.py yayinla {post.slug}</code>.</p>\n")


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
        content = markdown(post.body)
        meta = f'<time datetime="{post.day.isoformat()}">{post.date_tr}</time>'
        if post.review and post.review != post.day:
            meta += f' · son gözden geçirme <time datetime="{post.review.isoformat()}">{date_tr(post.review)}</time>'
        meta += f" · ≈{post.minutes} dk okuma"
        last = post.review or post.day
        cite = (f"Risale-i Nur MCP, «{post.title}», {post.date_tr}"
                + (f" (son gözden geçirme {date_tr(last)})" if last != post.day else "") + f". {BASE}{post.path}")
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
  <p class="small muted">Yanlış ya da eksik gördüğünüz bir yer için: <a href="/katki.html">Hata bildirin</a>.</p>
</section>{_share_card(post)}"""
    else:
        body = f"""{banner}<article class="post">
<p class="muted small"><a href="{kind.index}">{kind.title}</a> · <time datetime="{post.day.isoformat()}">{post.date_tr}</time></p>
<h1>{inline(post.title)}</h1>
{markdown(post.body)}
</article>
{_share_card(post)}"""
    return page(f"{post.title} · Risale-i Nur MCP", post.summary, path, body, kind="article",
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
    return page(f"{kind.title} · Risale-i Nur MCP", kind.description, kind.index, body, current=kind.index, feed=kind)


def preview_index(drafts: list[Post]) -> str:
    items = "\n".join(f"""<article class="post-item">
  <p class="muted small">{p.kind.title} · taslak · <code>{_rel(p.source) if p.source else p.slug}</code></p>
  <h2><a href="{p.preview_path}">{inline(p.title)}</a></h2>
  <p>{inline(p.summary)}</p>
  <p class="small muted">Yayımlamak için: <code>python3 scripts/site-uret.py yayinla {p.slug}</code></p>
</article>""" for p in drafts) or '<p class="muted">Bekleyen taslak yok.</p>'
    body = f"""<h1>Önizleme</h1>
<p class="lead">Yayımlanmamış Yenilikler ve Çalışmalar yazıları, sitedeki görünüşleriyle. Bu sayfayı yalnız girişli hesaplar görür.</p>

{items}"""
    return page("Önizleme · Risale-i Nur MCP", "Yayımlanmamış yazılar.", f"{PREVIEW_URL}/", body, robots="noindex")


def rss(kind: Kind, posts: list[Post]) -> str:
    def stamp(d: date) -> str:
        return format_datetime(datetime(d.year, d.month, d.day, 12, tzinfo=timezone.utc))
    items = "\n".join(f"""  <item>
    <title>{html.escape(p.title)}</title>
    <link>{BASE}{p.path}</link>
    <guid>{BASE}{p.path}</guid>
    <pubDate>{stamp(p.day)}</pubDate>
    <description>{html.escape(p.summary)}</description>
  </item>""" for p in posts)
    return f"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">
<channel>
  <title>Risale-i Nur MCP: {kind.title}</title>
  <link>{BASE}{kind.index}</link>
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
    rel = "/" + path.relative_to(SITE).as_posix()
    rel = rel[: -len("index.html")] if rel.endswith("index.html") else rel
    block = og_block(html.unescape(title.group(1)), html.unescape(desc.group(1)), rel, lang)
    new = _between(text, "<!-- og -->", "<!-- /og -->", block, title.group(0))
    if new != text:
        path.write_text(new, encoding="utf-8")
    return new != text


def frame(path: Path, current: str | None = None) -> bool:
    """Türkçe elle yazılmış sayfanın menüsünü ve alt bilgisini ortak biçimle yeniden yazar."""
    text = path.read_text(encoding="utf-8")
    if path.parent.name == "en":
        tr = re.search(r'<link rel="alternate" hreflang="tr" href="([^"]+)">', text)
        nav, footer = nav_en(CURRENT_EN.get(path.name, ""), tr.group(1) if tr else "/"), FOOTER_EN
    else:
        en = re.search(r'<link rel="alternate" hreflang="en" href="([^"]+)">', text)
        here = current if current is not None else CURRENT.get(path.name, "")
        nav, footer = nav_html(here, en.group(1) if en else "/en/"), FOOTER
    new = re.sub(r"<nav>.*?</nav>", lambda _: nav, text, count=1, flags=re.S)
    new = re.sub(r"<footer>.*?</footer>", lambda _: footer, new, count=1, flags=re.S)
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
    return SITE / (rel + "index.html" if rel.endswith("/") or not rel else rel)


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


def latest_list(posts: list[Post]) -> str:
    items = "\n".join(f'  <li><a href="{p.path}">{inline(p.title)}</a> <span class="muted small">· {p.date_tr}</span>'
                      f"<br><span class=\"small\">{inline(p.summary)}</span></li>" for p in posts[:3])
    return f'<!-- son-yenilikler -->\n<ul class="news">\n{items}\n</ul>\n<!-- /son-yenilikler -->'


def sitemap(pages: list[Path], posts: list[Post]) -> str:
    urls = []
    for page_path in pages:
        rel = "/" + page_path.relative_to(SITE).as_posix()
        urls.append(rel[: -len("index.html")] if rel.endswith("index.html") else rel)
    urls += [k.index for k in KINDS.values() if k.index not in NAV_HIDDEN] + [p.path for p in posts]
    body = "\n".join(f"  <url><loc>{BASE}{u}</loc></url>" for u in dict.fromkeys(urls))
    return (f'<?xml version="1.0" encoding="utf-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{body}\n</urlset>\n")


def latest_strip(post: Post) -> str:
    return (f'<!-- son-yenilik -->\n<p class="note small"><strong>Yeni:</strong> <a href="{post.path}">'
            f"{inline(post.title)}</a> · {post.date_tr}</p>\n<!-- /son-yenilik -->")


def broken_links(text: str) -> list[str]:
    """Sayfadaki iç bağlantılardan site/'da karşılığı olmayanlar (önizleme ve girişli bölüm sayılmaz)."""
    bad = []
    for href in re.findall(r'href="(/[^"#?]*)', text):
        if href.startswith(("/taslak/", "/oku/")) or href in ("/",):
            continue
        target = SITE / href.lstrip("/")
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

def build(quiet: bool = False) -> dict[str, list[Post]]:
    say = (lambda *_: None) if quiet else print
    everything = {key: read_posts(kind) for key, kind in KINDS.items()}
    published = {key: [p for p in posts if not p.draft] for key, posts in everything.items()}
    drafts = [p for posts in everything.values() for p in posts if p.draft]
    NAV_HIDDEN.clear()
    NAV_HIDDEN.update(k.index for key, k in KINDS.items() if not published[key])

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
        (SITE / f"{key}.html").write_text(index_page(kind, posts), encoding="utf-8")
        (SITE / f"{key}.xml").write_text(rss(kind, posts), encoding="utf-8")
        written.append(SITE / f"{key}.html")
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
    say(f"önizleme: {len(drafts)} taslak, {PREVIEW.relative_to(ROOT)}/ → risalemcp.com{PREVIEW_URL}/")

    # `adres`li Çalışmalar kayıtları (başka betiğin sayfası): yayımlanmışsa dizine açık, taslaksa noindex
    addressed = {address_file(p.address): p for posts in everything.values() for p in posts if p.address}
    for path, post in addressed.items():
        if not path.exists():
            sys.exit(f"{post.slug}: adres {post.address} için sayfa yok ({path.relative_to(ROOT)})")
        if set_noindex(path, post.draft):
            say(f"{'noindex kondu' if post.draft else 'noindex kalktı'}: {path.relative_to(ROOT)}")

    handmade = [p for p in sorted(SITE.glob("*.html")) + sorted((SITE / "en").glob("*.html"))
                if p.name not in {f"{k}.html" for k in KINDS}]
    subpages = sorted(p for p in SITE.glob("*/*.html") if p.parent.name not in {"en", *KINDS})
    changed = sum(add_og(p) for p in handmade + subpages)
    say(f"Open Graph: {len(handmade + subpages)} sayfa, {changed} değişti")
    currents = {path: post.kind.index for path, post in addressed.items()}
    say(f"menü ve alt bilgi: {sum(frame(p, currents.get(p)) for p in handmade + subpages)} sayfa değişti")
    values = numbers()
    say(f"sayılar: {sum(fill_numbers(p, values) for p in handmade)} sayfa değişti")
    listed = [p for p in subpages if p in addressed and not addressed[p].draft]
    (SITE / "sitemap.xml").write_text(sitemap(handmade + listed, [p for ps in published.values() for p in ps
                                                                  if not p.address]), encoding="utf-8")

    news = published["yenilikler"]
    index = SITE / "index.html"
    if news:
        text = index.read_text(encoding="utf-8")
        new = _between(text, "<!-- son-yenilik -->", "<!-- /son-yenilik -->", latest_strip(news[0]),
                       '<section class="hero">')
        if "<!-- son-yenilikler -->" in new:
            new = _between(new, "<!-- son-yenilikler -->", "<!-- /son-yenilikler -->", latest_list(news), "")
        if new != text:
            index.write_text(new, encoding="utf-8")
            say("ana sayfadaki yenilikler güncellendi")

    for path in written:
        if bad := broken_links(path.read_text(encoding="utf-8")):
            print(f"uyarı: {path.relative_to(ROOT)}: kırık iç bağlantı: {', '.join(bad)}")
    return everything


def find_post(name: str) -> Post:
    found = [p for kind in KINDS.values() for p in read_posts(kind)
             if p.slug == name or re.sub(r"^\d{4}-\d{2}-\d{2}-", "", p.slug) == name]
    if len(found) != 1:
        sys.exit(f"{name}: {'bulunamadı' if not found else 'birden çok yazı: ' + ', '.join(p.slug for p in found)}")
    return found[0]


def _set_meta(text: str, key: str, value: str) -> str:
    head, sep, rest = text.partition("\n---\n")
    if re.search(rf"^{key}:.*$", head, re.M):
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


def publish(name: str, send: bool) -> None:
    post = find_post(name)
    if not post.draft:
        sys.exit(f"{post.slug}: zaten yayında")
    if not post.address:                                  # önce önizlemedeki bağlantılar
        build(quiet=True)
        preview = PREVIEW / post.kind.key / f"{post.slug}.html"
        if bad := broken_links(preview.read_text(encoding="utf-8")):
            sys.exit(f"{post.slug}: kırık iç bağlantı, yayımlanmadı: {', '.join(bad)}")
    today = date.today().isoformat()
    rest = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", post.slug)
    text = post.source.read_text(encoding="utf-8")
    text = _set_meta(_set_meta(text, "durum", "yayinda"), "tarih", today)
    target = post.source.with_name(f"{today}-{rest}.md")
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
  Risale-i Nur MCP'de yeni bir çalışma: «{post.title}».
  {summary}
---

Çalışmalar kısmına yeni bir yazı eklendi: **{post.title}**.

{summary}

[Yazının tamamı]({url})
""", encoding="utf-8")
            print(f"Yeniliklere duyuru taslağı: {note.relative_to(ROOT)} (bakıp `yayinla {today}-{rest}` ile yayımlayın)")
    build()
    if send:
        subprocess.run([str(ROOT / "scripts" / "deploy.sh"), "--code"], cwd=ROOT, check=True)
    else:
        print("göndermek için: scripts/deploy.sh --code")


def serve(port: int = 8090) -> None:
    """Yerel önizleme: site/ ve önizleme klasörü tek kökte (bağlantılar sitedeki gibi çalışır)."""
    import functools
    import http.server
    build()
    root = Path(tempfile.mkdtemp(prefix="site-onizle-"))
    for item in SITE.iterdir():
        (root / item.name).symlink_to(item)
    (root / "taslak").mkdir()
    (root / "taslak" / "onizleme").symlink_to(PREVIEW)
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
    elif args[:1] == ["onizle"]:
        serve()
    elif not args:
        build()
    else:
        sys.exit(f"bilinmeyen: {' '.join(args)}")


if __name__ == "__main__":
    main()
