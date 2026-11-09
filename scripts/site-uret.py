#!/usr/bin/env python3
"""Sitenin üretilen parçaları (PLANLAR.md S1, S2): Yenilikler, Open Graph, menü ve alt bilgi, sayılar, site haritası.

    python3 scripts/site-uret.py           # hepsi
    python3 scripts/site-uret.py --resim   # bir de paylaşım resmi (site/img/paylasim.png; uvx cairosvg)

Sonra: scripts/deploy.sh --code

- Yazılar `docs/yenilikler/<tarih>-<ad>.md` dosyalarıdır (site/ olduğu gibi yayımlandığı için kaynak orada durmaz).
  Baştaki üst bilgi: `baslik`, `tarih` (YYYY-AA-GG), `ozet` (dizinde ve önizlemede), `whatsapp` (`|` ile çok satırlı;
  paylaşım kutusundaki metin, sonuna yazının adresi eklenir). Gövde sade Markdown: `##`, `###`, paragraf, `-` ve `1.`
  listeleri, `>` alıntı, `**kalın**`, `*eğik*`, `` `kod` ``, `[metin](adres)`.
- Çıktı: `site/yenilikler/<ad>.html`, `site/yenilikler.html` (en yeni üstte), `site/yenilikler.xml` (RSS 2.0).
- Open Graph: `site/` ve `site/en/` altındaki her sayfada `<!-- og -->` ile `<!-- /og -->` arası her seferinde
  yeniden yazılır (yoksa `</title>` satırından sonra eklenir); başlık `<title>`'dan, açıklama `description`'dan.
  WhatsApp önizlemeyi adres başına önbelleğe alır: etiket değişince eski paylaşımlar bir süre eski görünür.
- Ana sayfa (`site/index.html`): `<!-- son-yenilik -->` arasında son yazıya şerit, `<!-- son-yenilikler -->` arasında
  son üç yazı.
- Menü ve alt bilgi: Türkçe sayfaların `<nav>` ve `<footer>` blokları her seferinde buradan yazılır (`nav_html`,
  `FOOTER`); İngilizce sayfalarınki elle. Menüdeki "English" bağlantısı sayfanın `hreflang="en"` adresidir.
- Sayılar: sayfalardaki `<!-- sayi:ad -->…<!-- /sayi -->` arası yerel veritabanlarından (`data/dist/`) yazılır
  (`numbers`); veritabanı yoksa olduğu gibi kalır.
- `site/sitemap.xml`: bütün sayfalar ve yazılar.
- Dışarıya istek yok kuralı sürer: "WhatsApp'ta paylaş" yalnız tıklanınca açılan bir bağlantıdır.
"""

import html
import re
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
POSTS = ROOT / "docs" / "yenilikler"
OUT = SITE / "yenilikler"
BASE = "https://risalemcp.com"
IMAGE = "/img/paylasim.png"
ASSET_VERSION = 10                      # style.css ve site.js sürümü (sayfalardaki ?v=N ile aynı tutulur)
MONTHS = ("Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık")


@dataclass
class Post:
    slug: str
    title: str
    day: date
    summary: str
    share: str
    body: str

    @property
    def path(self) -> str:
        return f"/yenilikler/{self.slug}.html"

    @property
    def date_tr(self) -> str:
        return f"{self.day.day} {MONTHS[self.day.month - 1]} {self.day.year}"


# ---- yazılar --------------------------------------------------------------------------------------------------

def read_post(path: Path) -> Post:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        sys.exit(f"{path.name}: üst bilgi yok (--- … ---)")
    meta, key = {}, None
    for line in m.group(1).split("\n"):
        if key and (line.startswith("  ") or not line.strip()):
            meta[key] += line[2:] + "\n"
        elif (kv := re.match(r"(\w+):\s*(.*)$", line)):
            k, v = kv.groups()
            key = k if v == "|" else None
            meta[k] = "" if v == "|" else v
        else:
            sys.exit(f"{path.name}: anlaşılmayan üst bilgi satırı: {line!r}")
    missing = {"baslik", "tarih", "ozet", "whatsapp"} - set(meta)
    if missing:
        sys.exit(f"{path.name}: eksik üst bilgi: {', '.join(sorted(missing))}")
    return Post(path.stem, meta["baslik"], date.fromisoformat(meta["tarih"]), meta["ozet"],
                meta["whatsapp"].strip(), text[m.end():])


def inline(text: str) -> str:
    out = html.escape(text, quote=False)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])", r"<em>\1</em>", out)
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: f'<a href="{html.escape(m.group(2))}">{m.group(1)}</a>', out)


def markdown(text: str) -> str:
    """Yazıların kullandığı kadar Markdown: başlık, paragraf, liste, alıntı."""
    blocks, out = re.split(r"\n\s*\n", text.strip()), []
    for block in blocks:
        lines = block.split("\n")
        if (h := re.match(r"(#{2,3}) (.+)$", lines[0])) and len(lines) == 1:
            level = len(h.group(1))
            out.append(f"<h{level}>{inline(h.group(2))}</h{level}>")
        elif all(re.match(r"[-*] ", l) or l.startswith("  ") for l in lines):
            out.append("<ul>\n" + "\n".join(f"  <li>{inline(i)}</li>" for i in _items(lines, r"[-*] ")) + "\n</ul>")
        elif all(re.match(r"\d+\. ", l) or l.startswith("   ") for l in lines):
            out.append("<ol>\n" + "\n".join(f"  <li>{inline(i)}</li>" for i in _items(lines, r"\d+\. ")) + "\n</ol>")
        elif all(l.startswith(">") for l in lines):
            inner = " ".join(l[1:].strip() for l in lines)
            out.append(f"<blockquote><p>{inline(inner)}</p></blockquote>")
        else:
            out.append(f"<p>{inline(' '.join(l.strip() for l in lines))}</p>")
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
       ("/belgeler.html", "Belgeler")]
# Sayfa -> menüde işaretli olan (sayfa adı; yazılar "yenilikler")
CURRENT = {"risale.html": "/#eklentiler", "hadis.html": "/#eklentiler", "tefsir.html": "/#eklentiler",
           "claude.html": "/#ekle", "chatgpt.html": "/#ekle", "yenilikler.html": "/yenilikler.html",
           "belgeler.html": "/belgeler.html"}
FOOTER = ("<footer>Nur Hadimleri: gönüllü ve bağımsız bir projedir; herhangi bir yayınevi ya da cemaatin resmî hizmeti "
          "değildir.<br><a href=\"/gizlilik.html\">Gizlilik</a> · <a href=\"/kullanim-sartlari.html\">Kullanım "
          "şartları</a> · <a href=\"/katki.html\">Hata bildirin</a> · <a href=\"/yenilikler.xml\">RSS</a> · "
          "<a href=\"mailto:destek@risalemcp.com\">destek@risalemcp.com</a></footer>")


def nav_html(current: str = "", en: str = "/en/") -> str:
    links = "\n".join(f'  <a href="{href}"' + (' aria-current="page"' if href == current else "") + f">{name}</a>"
                      for href, name in NAV)
    return f"""<nav>
  <a class="brand" href="/"><img src="/icon.png" alt="">Risale-i Nur MCP</a>
{links}
  <a href="{en}" lang="en">English</a>
  <button class="theme-toggle" type="button" data-theme-toggle aria-label="Açık ve koyu görünüm arasında geç" title="Açık ve koyu görünüm arasında geç"></button>
</nav>"""


def page(title: str, description: str, path: str, body: str, kind: str = "website", current: str = "",
         extra_head: str = "") -> str:
    return f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
{og_block(title, description, path, kind=kind)}
<meta name="description" content="{html.escape(description)}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="256x256" href="/icon.png">
<link rel="apple-touch-icon" href="/icon.png">
<link rel="stylesheet" href="/style.css?v={ASSET_VERSION}">
<link rel="alternate" type="application/rss+xml" title="Risale-i Nur MCP: Yenilikler" href="/yenilikler.xml">{extra_head}
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


def post_page(post: Post) -> str:
    share = f"{post.share}\n{BASE}{post.path}"
    body = f"""<article class="post">
<p class="muted small"><a href="/yenilikler.html">Yenilikler</a> · <time datetime="{post.day.isoformat()}">{post.date_tr}</time></p>
<h1>{inline(post.title)}</h1>
{markdown(post.body)}
</article>

<section class="card share">
  <h2>Paylaşın</h2>
  <pre>{html.escape(share)}</pre>
  <div class="actions">
    <button class="button" type="button" data-copy="{html.escape(share)}" data-done="Kopyalandı ✓">Metni kopyala</button>
    <a class="button primary" href="https://wa.me/?text={quote(share)}" rel="noopener">WhatsApp'ta paylaş</a>
  </div>
</section>"""
    return page(f"{post.title} · Risale-i Nur MCP", post.summary, post.path, body, kind="article",
                current="/yenilikler.html")


def index_page(posts: list[Post]) -> str:
    items = "\n".join(f"""<article class="post-item">
  <p class="muted small"><time datetime="{p.day.isoformat()}">{p.date_tr}</time></p>
  <h2><a href="{p.path}">{inline(p.title)}</a></h2>
  <p>{inline(p.summary)}</p>
</article>""" for p in posts)
    body = f"""<h1>Yenilikler</h1>
<p class="lead">Eklentilerde yeni olanlar, iyileştirmeler ve duyurular. Her yazının sonunda paylaşmak için kısa bir metin var. <a href="/yenilikler.xml">RSS</a> ile de takip edebilirsiniz.</p>

{items}"""
    return page("Yenilikler · Risale-i Nur MCP", "Risale-i Nur, Hadis ve Tefsir eklentilerinde yeni olanlar, "
                "iyileştirmeler ve duyurular.", "/yenilikler.html", body, current="/yenilikler.html")


def rss(posts: list[Post]) -> str:
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
  <title>Risale-i Nur MCP: Yenilikler</title>
  <link>{BASE}/yenilikler.html</link>
  <description>Risale-i Nur, Hadis ve Tefsir eklentilerinde yeni olanlar.</description>
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


def frame(path: Path) -> bool:
    """Türkçe elle yazılmış sayfanın menüsünü ve alt bilgisini ortak biçimle yeniden yazar."""
    text = path.read_text(encoding="utf-8")
    en = re.search(r'<link rel="alternate" hreflang="en" href="([^"]+)">', text)
    new = re.sub(r"<nav>.*?</nav>", lambda _: nav_html(CURRENT.get(path.name, ""), en.group(1) if en else "/en/"),
                 text, count=1, flags=re.S)
    new = re.sub(r"<footer>.*?</footer>", lambda _: FOOTER, new, count=1, flags=re.S)
    if new != text:
        path.write_text(new, encoding="utf-8")
    return new != text


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
    urls += ["/yenilikler.html"] + [p.path for p in posts]
    body = "\n".join(f"  <url><loc>{BASE}{u}</loc></url>" for u in urls)
    return (f'<?xml version="1.0" encoding="utf-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{body}\n</urlset>\n")


def latest_strip(post: Post) -> str:
    return (f'<!-- son-yenilik -->\n<p class="note small"><strong>Yeni:</strong> <a href="{post.path}">'
            f"{inline(post.title)}</a> · {post.date_tr}</p>\n<!-- /son-yenilik -->")


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

def main() -> None:
    if "--resim" in sys.argv:
        share_image()
    posts = sorted((read_post(p) for p in POSTS.glob("*.md")), key=lambda p: (p.day, p.slug), reverse=True)
    OUT.mkdir(exist_ok=True)
    keep = {f"{p.slug}.html" for p in posts}
    for old in OUT.glob("*.html"):
        if old.name not in keep:
            old.unlink()
            print(f"silindi: {old.relative_to(ROOT)}")
    for post in posts:
        (OUT / f"{post.slug}.html").write_text(post_page(post), encoding="utf-8")
    (SITE / "yenilikler.html").write_text(index_page(posts), encoding="utf-8")
    (SITE / "yenilikler.xml").write_text(rss(posts), encoding="utf-8")
    print(f"yazıldı: {len(posts)} yazı, site/yenilikler.html, site/yenilikler.xml")

    handmade = [p for p in sorted(SITE.glob("*.html")) + sorted((SITE / "en").glob("*.html"))
                if p.name != "yenilikler.html"]
    changed = sum(add_og(p) for p in handmade)
    print(f"Open Graph: {len(handmade)} sayfa, {changed} değişti")
    turkish = [p for p in handmade if p.parent == SITE]
    print(f"menü ve alt bilgi: {sum(frame(p) for p in turkish)} sayfa değişti")
    values = numbers()
    print(f"sayılar: {values}; {sum(fill_numbers(p, values) for p in turkish)} sayfa değişti")
    (SITE / "sitemap.xml").write_text(sitemap(handmade, posts), encoding="utf-8")

    index = SITE / "index.html"
    if posts:
        text = index.read_text(encoding="utf-8")
        new = _between(text, "<!-- son-yenilik -->", "<!-- /son-yenilik -->", latest_strip(posts[0]),
                       '<section class="hero">')
        if "<!-- son-yenilikler -->" in new:
            new = _between(new, "<!-- son-yenilikler -->", "<!-- /son-yenilikler -->", latest_list(posts), "")
        if new != text:
            index.write_text(new, encoding="utf-8")
            print("ana sayfadaki yenilikler güncellendi")


if __name__ == "__main__":
    main()
