"""erisale ham sayfa ayrıştırıcısının testleri (ağ bağlantısı gerektirmez)."""

import json

from risale_mcp.sources.erisale import (
    Archive, Page, extract_blocks, extract_breadcrumb, merge_pages, parse_sitemap,
)

SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://www.erisale.com</loc></url>
  <url><loc>https://www.erisale.com/tr/sozler/birinci-soz</loc></url>
  <url><loc>https://www.erisale.com/tr/sozler/ikinci-soz</loc></url>
  <url><loc>https://www.erisale.com/tr/mektubat/birinci-mektub</loc></url>
</urlset>"""


def block(index: int, kind: str = "Paragraph", text: str = "metin") -> dict:
    return {"bookId": "sozler", "blockIndex": index, "sectionIndex": 0, "pageNumber": 7,
            "content": {"type": kind, "children": [{"type": "Text", "value": text}]}}


def page_html(blocks: list[dict], title: str = "Birinci Söz — Sözler | eRisale") -> str:
    """Gerçek sayfalardaki gibi: RSC verisi JS dizgesi olarak, parçalara bölünmüş halde gömülü."""
    payload = "5:" + json.dumps({"blocks": blocks}, ensure_ascii=False)
    middle = len(payload) // 2
    pushes = "".join(
        f"<script>self.__next_f.push([1,{json.dumps(part, ensure_ascii=False)}])</script>"
        for part in (payload[:middle], payload[middle:])
    )
    return f"<html><head><title>{title}</title></head><body>{pushes}</body></html>"


def test_parse_sitemap_keeps_order_and_skips_non_book_urls():
    pages = parse_sitemap(SITEMAP)
    assert [(p.book, p.slug) for p in pages] == [
        ("sozler", "birinci-soz"), ("sozler", "ikinci-soz"), ("mektubat", "birinci-mektub")]


def test_extract_blocks_across_split_chunks():
    html = page_html([block(3, text="Arapça: بِسْمِ اللّٰهِ"), block(2), block(3)])
    blocks = extract_blocks(html)
    assert [b["blockIndex"] for b in blocks] == [2, 3]
    assert blocks[1]["content"]["children"][0]["value"] == "Arapça: بِسْمِ اللّٰهِ"


def test_breadcrumb_drops_book_name():
    html = page_html([], "Onuncu Söz — On iki Hakikat — Beşinci Hakikat — Sözler | eRisale")
    assert extract_breadcrumb(html) == ["Onuncu Söz", "On iki Hakikat", "Beşinci Hakikat"]


def test_merge_reports_gaps_conflicts_and_drops_page_info():
    first = (Page("sozler", "a", "u1"), page_html([block(1, "PageNumber"), block(2), block(3)]))
    second = (Page("sozler", "b", "u2"), page_html([block(3, text="farklı"), block(5)]))
    book = merge_pages("sozler", [first, second])

    assert book.first_index == 1
    assert book.missing == [4]
    assert book.conflicts == [3]
    assert [b["index"] for b in book.blocks] == [2, 3, 5]  # PageNumber bloğu ayıklandı
    assert all("pageNumber" not in b for b in book.blocks)
    assert [b["page"] for b in book.blocks] == ["a", "a", "b"]


def test_archive_roundtrip(tmp_path):
    archive = Archive(tmp_path)
    pages = parse_sitemap(SITEMAP)[:2]
    for page in pages:
        archive.write_page(page, page_html([block(0)]).encode("utf-8"))
    archive.write_manifest("sozler", pages)

    assert archive.read_manifest("sozler") == pages
    assert extract_blocks(archive.read_page(pages[0]))[0]["blockIndex"] == 0


def test_extract_blocks_resolves_text_rows():
    long_text = "O vakit nev'‑i insan der ki: “Eğer…”"
    size = format(len(long_text.encode("utf-8")), "x")
    payload = (
        '{"bookId":"sozler","blockIndex":7,"sectionIndex":1,"pageNumber":0,"content":{"type":"Paragraph",'
        '"children":[{"type":"Text","value":"$4c"},{"type":"Text","value":"$$5 kuruş"},{"type":"Text","value":"$9z"}]}}'
        f"\n4c:T{size},{long_text}5:[]"
    )
    html = f'<script>self.__next_f.push([1,{json.dumps(payload)}])</script>'
    block = extract_blocks(html)[0]
    values = [c["value"] for c in block["content"]["children"]]
    assert values == [long_text, "$5 kuruş", "$9z"]       # "$9z" başvuru değil, olduğu gibi kalır
