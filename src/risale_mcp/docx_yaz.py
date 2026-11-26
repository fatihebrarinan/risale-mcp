"""S10 (g2): okuyucunun "Notlarım"ı Word dosyası olarak (kullanıcının kararı, 2026-11-23: bilgisayarla haşir neşir
olmayan okuyucu için Markdown ya da JSON değil, Word).

Yeni bağımlılık eklenmez (sunucu ARM; python-docx lxml ister): en küçük geçerli .docx elle yazılır, `zipfile` ve düz
XML ile. Word, LibreOffice ve Google Dokümanlar açar. Birimler sırasıyla başlık olur; her notta paragrafın ilk
sözleri, işaretlenen söz, not ve paragrafa giden bağlantı durur. Damga: notların bağlı olduğu metin yapay zekâ
taslağıdır, tefsir değildir.
"""

from __future__ import annotations

import io
import re
import time
import zipfile
from xml.sax.saxutils import escape

PLATFORM = "https://read.ayinedar.org/"
MONTHS = ("Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık")

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
</Types>"""

ROOT_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
</Relationships>"""

CORE = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<dc:title>Notlarım</dc:title><dc:creator>Âyinedâr okuma platformu</dc:creator>
<dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
</cp:coreProperties>"""

STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Arial"/><w:sz w:val="24"/>
<w:szCs w:val="24"/><w:lang w:val="tr-TR"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/>
<w:pPr><w:spacing w:after="60"/></w:pPr><w:rPr><w:b/><w:sz w:val="40"/><w:szCs w:val="40"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/>
<w:pPr><w:keepNext/><w:spacing w:before="360" w:after="120"/><w:outlineLvl w:val="0"/></w:pPr>
<w:rPr><w:b/><w:color w:val="1F5C3F"/><w:sz w:val="30"/><w:szCs w:val="30"/></w:rPr></w:style>
<w:style w:type="character" w:styleId="Hyperlink"><w:name w:val="Hyperlink"/><w:rPr><w:color w:val="1F4F7A"/>
<w:u w:val="single"/></w:rPr></w:style>
</w:styles>"""

DOC_RELS_HEAD = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
"""

DOC_HEAD = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><w:body>
"""

DOC_TAIL = """<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1418" w:right="1418" w:bottom="1418" w:left="1418"
 w:header="708" w:footer="708" w:gutter="0"/></w:sectPr></w:body></w:document>"""

_CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def turkish_date(ts: float) -> str:
    t = time.localtime(ts)
    return f"{t.tm_mday} {MONTHS[t.tm_mon - 1]} {t.tm_year}"


def _run(text: str, *, italic=False, bold=False, small=False, grey=False) -> str:
    props = ("<w:i/>" if italic else "") + ("<w:b/>" if bold else "") \
        + ('<w:color w:val="6B6A66"/>' if grey else "") + ('<w:sz w:val="20"/><w:szCs w:val="20"/>' if small else "")
    parts = _CTRL.sub("", text).split("\n")
    body = '<w:br/>'.join(f'<w:t xml:space="preserve">{escape(p)}</w:t>' for p in parts)
    return f"<w:r>{f'<w:rPr>{props}</w:rPr>' if props else ''}{body}</w:r>"


def _para(*runs: str, style: str | None = None, indent: int = 0, after: int | None = None) -> str:
    ppr = (f'<w:pStyle w:val="{style}"/>' if style else "") + (f'<w:ind w:left="{indent}"/>' if indent else "") \
        + (f'<w:spacing w:after="{after}"/>' if after is not None else "")
    return f"<w:p>{f'<w:pPr>{ppr}</w:pPr>' if ppr else ''}{''.join(runs)}</w:p>\n"


def _unit_key(birim: str) -> tuple:
    m = re.match(r"\d+", birim or "")
    return (int(m.group()) if m else 10 ** 6, birim or "")


def notes_docx(notes: list[dict], now: float | None = None) -> bytes:
    """Defter notlarından (`MasaStore.defter`) .docx baytları."""
    now = now or time.time()
    links: list[str] = []

    def link(url: str, text: str) -> str:
        links.append(url)
        return (f'<w:hyperlink r:id="rIdL{len(links)}" w:history="1"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/>'
                f'<w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:t xml:space="preserve">{escape(text)}</w:t></w:r>'
                "</w:hyperlink>")

    body = [_para(_run("Notlarım"), style="Title"),
            _para(_run(f"Âyinedâr okuma platformu · {turkish_date(now)} tarihinde indirildi · {len(notes)} not",
                       small=True, grey=True)),
            _para(_run("Notlarınızın bağlı olduğu metinler yapay zekâ taslağıdır; tefsir değildir. Bu dosyayı yalnız "
                       "siz indirebilirsiniz; notlarınız sitede de yalnız size görünür.", small=True, italic=True),
                  after=240)]
    if not notes:
        body.append(_para(_run("Henüz notunuz yok.")))
    groups: dict[str, list[dict]] = {}
    for n in notes:
        groups.setdefault(n["birim"], []).append(n)
    for birim in sorted(groups, key=_unit_key):
        ns = sorted(groups[birim], key=lambda n: n["zaman"])
        body.append(_para(_run(next((n["etiket"] for n in ns if n.get("etiket")), None) or f"Birim {birim}"),
                          style="Heading1"))
        for n in ns:
            if n.get("baglam"):
                body.append(_para(_run("Paragraf: ", small=True, grey=True),
                                  _run(f"«{n['baglam']}…»", small=True, grey=True), after=40))
            exact = (n.get("secici") or {}).get("exact")
            if exact:
                body.append(_para(_run("İşaretlediğiniz söz: ", small=True),
                                  _run(f"«{exact}»", italic=True, small=True), indent=284, after=40))
            body.append(_para(_run(n["metin"]), indent=284, after=40))
            when = turkish_date(n["zaman"]) + (" (düzenlendi)" if n.get("guncellendi", n["zaman"]) - n["zaman"] > 60 else "")
            runs = [_run(when, small=True, grey=True)]
            if n.get("paragraf"):
                runs += [_run(" · ", small=True, grey=True), link(f"{PLATFORM}#/{birim}/{n['paragraf']}", "paragrafı aç")]
            body.append(_para(*runs, indent=284, after=240))
    rels = DOC_RELS_HEAD + "".join(
        f'<Relationship Id="rIdL{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" '
        f'Target="{escape(u, {chr(34): "&quot;"})}" TargetMode="External"/>\n' for i, u in enumerate(links, 1)) + "</Relationships>"
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", ROOT_RELS)
        z.writestr("docProps/core.xml", CORE.format(now=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))))
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/_rels/document.xml.rels", rels)
        z.writestr("word/document.xml", DOC_HEAD + "".join(body) + DOC_TAIL)
    return buf.getvalue()
