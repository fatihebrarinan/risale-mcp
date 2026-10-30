"""risale.online, risaleoku ve Yeni Asya indiricilerinin ağ gerektirmeyen kısımları."""

import gzip
import json

import pytest

from risale_mcp.sources import risale_online, risaleoku, yeniasya
from risale_mcp.sources.archive import fetch_cached, read_raw


class FakeClient:
    def __init__(self, responses: dict[str, bytes]):
        self.responses = responses
        self.requested: list[str] = []

    def get(self, url: str) -> bytes:
        self.requested.append(url)
        return self.responses[url]


def test_fetch_cached_downloads_once_and_compresses_gz(tmp_path):
    client = FakeClient({"u": b"<p>metin</p>"})
    path = tmp_path / "a" / "page.html.gz"
    assert fetch_cached(path, "u", client) == b"<p>metin</p>"
    assert fetch_cached(path, "u", client) == b"<p>metin</p>"
    assert client.requested == ["u"]
    assert gzip.decompress(path.read_bytes()) == b"<p>metin</p>"
    assert read_raw(path) == b"<p>metin</p>"


def test_risale_online_requests_eight_pages_at_a_time():
    assert risale_online._chunks(19) == [(1, 8), (9, 16), (17, 19)]


def test_risale_online_check_reports_pages_without_paragraphs(tmp_path):
    book = tmp_path / "zulfikar"
    (book / "paragraf").mkdir(parents=True)
    (book / "manifest.json").write_text(json.dumps({"page_count": 3}))
    (book / "fihrist.json").write_text("[]")
    (book / "paragraf" / "0001-0003.json").write_text(json.dumps([{"sayfa": "1"}, {"sayfa": "3"}]))
    lines, ok = risale_online.check_book("zulfikar", tmp_path)
    assert not ok
    assert "[2]" in lines[1]


def test_risale_online_rejects_books_without_text(tmp_path):
    books = [{"id": 23, "slug": "nurun-ilk-kapisi", "sayfa_sayisi": 157, "metin_var_mi": False}]
    client = FakeClient({f"{risale_online.API_URL}/eserler": json.dumps(books).encode()})
    with pytest.raises(ValueError, match="metni yok"):
        risale_online.book_meta(tmp_path, client, "nurun-ilk-kapisi")


def test_risaleoku_page_count_and_text():
    index = '<div class="sh_label">\n  <div>&nbsp;/&nbsp;&nbsp;</div>\n  <div>147</div>\n</div>'
    assert risaleoku.page_count(index) == 147
    assert risaleoku.page_text("<span class='ortali'>Hizb-ül Kur&#039;an</span> <br />") == "Hizb-ül Kur'an"
    with pytest.raises(ValueError):
        risaleoku.page_count("<html></html>")


def test_yeniasya_check_requires_decodable_pages(tmp_path):
    book = tmp_path / "eski"
    (book / "pages").mkdir(parents=True)
    (book / "manifest.json").write_text(json.dumps({"page_count": 2}))
    (book / "pages" / "0001.html.gz").write_bytes(gzip.compress("bafllar›z".encode(yeniasya.ENCODING)))
    lines, ok = yeniasya.check_book("eski", tmp_path)
    assert not ok and "[2]" in lines[1]  # 2. sayfa eksik


def test_polite_client_retries_read_timeouts(monkeypatch):
    from risale_mcp.sources import http

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return b"ok"

    calls = []

    def fake_urlopen(request, timeout):
        calls.append(request.full_url)
        if len(calls) == 1:
            raise TimeoutError("The read operation timed out")
        return Response()

    monkeypatch.setattr(http.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(http.time, "sleep", lambda seconds: None)
    assert http.PoliteClient(delay=0).get("https://example.org/") == b"ok"
    assert len(calls) == 2


def test_risaleoku_app_pages_catalog_and_verifies_files(tmp_path):
    import hashlib
    import json

    from risale_mcp.sources import risaleoku_app

    text = "#3 \n<Başlık> \n".encode()
    book = {"key": "abed", "shelf_id": 25, "sort": 1, "title": "Âsâr", "version": 4,
            "files": {"text": {"url": "https://risaleoku.com/f/a.txt.gz", "sha256": hashlib.sha256(text).hexdigest()},
                      "footnotes": None}}
    pages = [{"records": [{"kind": "book", "id": 1, "seq": 1, "data": book}], "has_more": True, "next_cursor": 1},
             {"records": [{"kind": "book", "id": 2, "seq": 2, "data": None}], "has_more": False}]
    calls = []

    class Client:
        def get(self, url):
            calls.append(url)
            return json.dumps(pages.pop(0)).encode() if "changes" in url else text

    risaleoku_app.fetch_book("abed", tmp_path, Client(), log=lambda _: None)
    assert "after=1" in calls[1]
    assert risaleoku_app.check_book("abed", tmp_path)[1]
    assert risaleoku_app.shelf_books(json.loads((tmp_path / "catalog.json").read_text()), 25) == ["abed"]

    (tmp_path / "abed" / "text.txt.gz").unlink()
    assert not risaleoku_app.check_book("abed", tmp_path)[1]
