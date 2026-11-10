#!/usr/bin/env python3
"""İşârât'ın usul özetinin okur sürümü (PLANLAR.md D1.1): site sayfası ve PDF.

    python3 scripts/d1-okur.py          # site/taslak/isarat-usulu.html ve .pdf (PDF için uvx weasyprint; Arapça için sistemde
                                        # Noto Naskh Arabic gerekir: sitenin amiri-hadis.woff2'si alt kümedir)
    python3 scripts/site-uret.py        # sayfanın menüsü, alt bilgisi ve Open Graph etiketleri
    scripts/deploy.sh --code

Kaynak `docs/d1-usul-ozeti.md`'dir (programcı sürümü: kimlikler, denetim komutu). Okur sürümünde:
- cümle kimlikleri görünmez; her adres eser, bölüm ve cümlenin ilk kelimeleriyle yazılır (veritabanından: `ref`,
  `incipit`; aralık "… ile başlayan N cümle"), cümle numarası yazılmaz;
- Arapça alıntı sağdan sola, altında "Tercümede" etiketiyle Türkçe karşılığı; derleyenin tercümesi "Yapay zekâ
  tercümesi" damgasıyla (ikinci sürüm, D1.2b);
- baştaki teknik not yerine okura yazılmış giriş (`INTRO`), "Denetim" bölümü yerine tek cümle gelir;
- "[Çıkarım]" "Derleyenin notu" olur.
Sayfa yalnız bağlantıyla bulunur: menüde ve site haritasında yoktur, `noindex` taşır. Depo açık olduğu için gizli
değildir (kullanıcının kararı, 2026-11-10: açık olması sorun değil).
"""
import html
import re
import sqlite3
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "docs" / "d1-usul-ozeti.md"
OUT = ROOT / "site" / "taslak"
NAME = "isarat-usulu"
TITLE = "İşârâtü'l-İ'câz'ın usulü: kendi metninden bir döküm"
DESCRIPTION = ("İşârâtü'l-İ'câz'ın bir âyeti ele alırken ne yaptığını ve hangi sırayla yaptığını eserin kendi "
               "cümleleriyle gösteren taslak döküm.")
MONTHS = ("Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık")
ASSET_VERSION = 11

INTRO = """<div class="note">
<p><strong>Bu belge nedir?</strong> İşârâtü'l-İ'câz'ın bir âyeti ele alırken ne yaptığını ve hangi sırayla yaptığını, eserin kendi cümleleriyle gösteren bir dökümdür. Tefsir değildir. Bir yapay zekâ derlemesidir ve ehlinin tashihine sunulmuş bir taslaktır.</p>
<p><strong>Nasıl okunur?</strong> Çerçeveli sözler İşârâtü'l-İ'câz'dan aynen alınmıştır ve kaynak metinle birebir karşılaştırılmıştır. Dayanak eserin Arapça aslıdır; Arapça cümlenin altında, "Tercümede" diye, Abdülmecid Nursî tercümesindeki karşılığı durur. Her alıntının altında eserdeki yeri ve cümlenin ilk kelimeleri yazar; o cümleyi kitapta siz de bulabilirsiniz.</p>
<p><strong>İki işarete dikkat edin.</strong> <span class="mine">Yapay zekâ tercümesi</span> diye başlayan satırlar eserin sözü değildir: Arapça cümlenin tercümede karşılığı bulunmadığı yerde derleyenin yaptığı tercümedir, yanlış olabilir. <span class="mine">Derleyenin notu</span> diye başlayan yerler de derleyenin kendi tespitidir.</p>
<p><strong>Hangi metin?</strong> Arapça asıl risaleoku.com'daki metinden, Türkçe tercüme e-Risale'deki metinden alınmıştır. Tenbih'i ve Hâşiye'yi müellif sonradan Türkçe yazmıştır; onlarda asıl Türkçedir. Tercüme asıldan üç noktada ayrılır: âyetlerin ardındaki "Yani: …" mealleri asılda yoktur; tercüme yer yer kısaltır (1.4); Bakara 17–20'nin başındaki belâgat bahsi tercümede hiç yoktur (2. bölüm). Arapça asıl 31. âyetin ortasında biter.</p>
<p><strong>İkinci sürümde ne değişti?</strong> İlk sürüm Türkçe tercümenin taranmasına dayanıyordu. Bu sürüm için Arapça asıl baştan sona okundu (Fâtiha, Bakara 1–33). Eklenenler: usulün belâgat temeli (2), her âyette izlenen sıranın çizelgesi (4), mukaddimelerin ne zaman geldiği (5) ve taslak için kurallar (8).</p>
<p><strong>Sınırı nedir?</strong> Okuma bir yapay zekâ okumasıdır; Arapça belâgat inceliklerinde yanılmış olabilir. Sayılar bir kelime taramasından gelir, yaklaşık okunmalıdır.</p>
<p><strong>Düzeltmeleriniz</strong> için: <a href="mailto:destek@risalemcp.com">destek@risalemcp.com</a></p>
</div>"""
OUTRO = "<p class=\"muted small\">Bu belgedeki bütün alıntılar kaynak metinlerle (risaleoku.com, e-Risale) birebir karşılaştırılmıştır.</p>"
PAGE_CSS = """<style>
.reader blockquote.quote p.ar { direction: rtl; text-align: right; font-family: "Noto Naskh Arabic", "Amiri", "Scheherazade New", serif; font-size: 1.25rem; line-height: 2.1; }
.reader p.label { margin: 0 0 -8px; font-size: 0.85rem; color: var(--muted); }
</style>"""

db = sqlite3.connect(ROOT / "data" / "dist" / "genel" / "risale.db")


def place(ident: str) -> str:
    """Kimlikten okura gösterilecek adres: yol ve ilk kelimeler (aralıkta cümle sayısıyla)."""
    first, _, last = ident.partition("..")
    row = db.execute("select ref, incipit, node_id, n from sentences where id = ?", (first,)).fetchone()
    if not row:
        sys.exit(f"kimlik yok: {ident}")
    ref, incipit, node, n = row
    path = ref.rsplit(" › ", 1)[0]
    text = f"{path} › “{incipit}…”"
    if last:
        end = db.execute("select n from sentences where id = ?", (f"{node}/{last}",)).fetchone()
        if not end:
            sys.exit(f"kimlik yok: {ident}")
        text += f" ile başlayan {end[0] - n + 1} cümle"
    return text


_ID = r"isaratul-icaz[\w/-]*/c\d+(?:\.\.c\d+)?"


def inline(text: str) -> str:
    out = html.escape(text, quote=False)
    out = re.sub(rf"`({_ID})`", lambda m: html.escape(place(m.group(1)), quote=False), out)
    out = out.replace("**[Çıkarım]**", '<span class="mine">Derleyenin notu:</span>')
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    return re.sub(r"`([^`]+)`", r"\1", out)


def body() -> str:
    text = SOURCE.read_text(encoding="utf-8")
    text = text[: text.index("\n## Denetim")]
    blocks = [b for b in re.split(r"\n\s*\n", text) if b.strip()]
    out, i = [], 0
    while i < len(blocks):
        block = blocks[i]
        lines = block.split("\n")
        if block.startswith("# "):
            pass                                         # başlık sayfanın kendisinde
        elif block.startswith("> **"):
            pass                                         # programcı sürümünün baş notu: yerine INTRO
        elif (q := re.fullmatch(r'> "(.*)"', block)):
            cite = blocks[i + 1] if i + 1 < len(blocks) and blocks[i + 1].startswith("— ") else None
            ident = re.search(rf"\(`({_ID})`\)", cite or "")
            if not ident:
                sys.exit(f"alıntının adresi yok: {block[:60]}")
            arabic = ident.group(1).startswith("isaratul-icaz-arabi/")
            attrs = ' class="ar" dir="rtl" lang="ar"' if arabic else ""
            out.append(f'<blockquote class="quote"><p{attrs}>"{html.escape(q.group(1), quote=False)}"</p>'
                       f"<footer>{html.escape(place(ident.group(1)), quote=False)}</footer></blockquote>")
            i += 1
        elif (h := re.fullmatch(r"(#{2,3}) (.+)", block)):
            level = len(h.group(1))
            out.append(f"<h{level}>{inline(h.group(2))}</h{level}>")
        elif lines[0].startswith("|"):
            rows = [[c.strip() for c in l.strip("|").split("|")] for l in lines if not re.fullmatch(r"[|\-: ]+", l)]
            head = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
            cells = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
            out.append(f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{cells}</tbody></table></div>')
        elif all(re.match(r"- |  ", l) for l in lines):
            items = _items(lines, r"- ")
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>")
        elif all(re.match(r"\d+\. |   ", l) for l in lines):
            items = _items(lines, r"\d+\. ")
            out.append("<ol>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ol>")
        elif block == "Tercümede:":
            out.append('<p class="label">Tercümede (Abdülmecid Nursî):</p>')
        elif block.startswith("Yapay zekâ tercümesi: "):
            out.append(f'<p><span class="mine">Yapay zekâ tercümesi:</span> {inline(block.split(": ", 1)[1])}</p>')
        else:
            out.append(f"<p>{inline(' '.join(l.strip() for l in lines))}</p>")
        i += 1
    return "\n".join(out)


def _items(lines: list[str], marker: str) -> list[str]:
    items: list[str] = []
    for line in lines:
        if re.match(marker, line):
            items.append(re.sub(marker, "", line, count=1))
        else:
            items[-1] += " " + line.strip()
    return items


def stamp() -> str:
    today = date.today()
    return f"Taslak · {today.day} {MONTHS[today.month - 1]} {today.year}"


def page(content: str) -> str:
    return f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(TITLE)} · Risale-i Nur MCP</title>
<meta name="description" content="{html.escape(DESCRIPTION)}">
<meta name="robots" content="noindex">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="256x256" href="/icon.png">
<link rel="apple-touch-icon" href="/icon.png">
<link rel="stylesheet" href="/style.css?v={ASSET_VERSION}">
<script>try{{var t=localStorage.getItem("theme");if(t==="light"||t==="dark")document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<script src="/site.js?v={ASSET_VERSION}" defer></script>
{PAGE_CSS}
</head>
<body>
<main class="reader">
<nav></nav>

<p class="muted small">{stamp()} · <a href="/taslak/{NAME}.pdf">PDF olarak indir</a></p>
<h1>{html.escape(TITLE)}</h1>
{INTRO}
{content}
{OUTRO}

<footer></footer>
</main>
</body>
</html>
"""


PDF_CSS = """
@page { size: A4; margin: 22mm 20mm 20mm; @bottom-center { content: "%s · risalemcp.com · " counter(page); font: 8pt "DejaVu Sans"; color: #666; } }
body { font: 10.5pt/1.6 "DejaVu Serif", "Noto Naskh Arabic", serif; color: #1a1a1a; }
h1 { font-size: 18pt; line-height: 1.25; margin: 0 0 6pt; }
h2 { font-size: 13.5pt; margin: 20pt 0 6pt; border-bottom: 0.5pt solid #999; padding-bottom: 2pt; break-after: avoid; }
h3 { font-size: 11.5pt; margin: 14pt 0 4pt; break-after: avoid; }
.stamp { color: #666; font-size: 9pt; margin: 0 0 4pt; }
.note { border: 0.5pt solid #999; border-left: 3pt solid #1f5c3f; padding: 4pt 10pt; margin: 10pt 0 14pt; font-size: 9.5pt; }
.note p { margin: 5pt 0; }
blockquote.quote { margin: 8pt 0 10pt; padding: 5pt 10pt; border-left: 3pt solid #1f5c3f; background: #f3f1ea; break-inside: avoid; }
blockquote.quote p { margin: 0 0 3pt; }
blockquote.quote footer { font-size: 8.5pt; color: #555; }
blockquote.quote p.ar { direction: rtl; text-align: right; font-family: "Noto Naskh Arabic", serif; font-size: 12.5pt; line-height: 1.9; }
p.label { margin: 0 0 -4pt; font-size: 8.5pt; color: #555; }
.mine { font-size: 8.5pt; font-weight: bold; color: #8a4b00; border: 0.5pt solid #8a4b00; border-radius: 3pt; padding: 0 3pt; }
table { width: 100%%; border-collapse: collapse; font-size: 9.5pt; margin: 8pt 0; }
th, td { text-align: left; vertical-align: top; padding: 3pt 5pt; border-bottom: 0.5pt solid #bbb; }
a { color: inherit; text-decoration: none; }
.small { font-size: 9pt; color: #555; }
"""


def pdf(content: str) -> None:
    doc = (f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>{html.escape(TITLE)}</title>'
           f"<style>{PDF_CSS % stamp()}</style></head><body>"
           f'<p class="stamp">{stamp()} · Risale-i Nur MCP · risalemcp.com/taslak/{NAME}.html</p>'
           f"<h1>{html.escape(TITLE)}</h1>{INTRO}{content}{OUTRO}</body></html>")
    target = OUT / f"{NAME}.pdf"
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "okur.html"
        src.write_text(doc, encoding="utf-8")
        subprocess.run(["uvx", "-q", "weasyprint", str(src), str(target)], check=True, stderr=subprocess.DEVNULL)
    print(f"yazıldı: {target.relative_to(ROOT)} ({target.stat().st_size // 1024} KB)")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    content = body()
    target = OUT / f"{NAME}.html"
    target.write_text(page(content), encoding="utf-8")
    print(f"yazıldı: {target.relative_to(ROOT)}")
    pdf(content)


if __name__ == "__main__":
    main()
