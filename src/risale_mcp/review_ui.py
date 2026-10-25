"""Taksimat ve cümle kontrol arayüzü: data/books/<eser>.json -> data/interim/review/<eser>.html.

Kullanım:
    uv run python -m risale_mcp.review_ui              # bütün eserler
    uv run python -m risale_mcp.review_ui sozler       # yalnızca seçilenler
    xdg-open data/interim/review/sozler.html

Her dosya sunucusuz, internetsiz açılır (veri, stil ve betik gömülüdür). Kenar
çubuğundaki seçici aynı klasördeki diğer eserlerin dosyalarına geçer.
Arayüz yalnızca hiyerarşiyi gösterir; sayfa bilgisi veride zaten yoktur.
"""

import argparse
import html
import json
from collections import defaultdict
from pathlib import Path

from risale_mcp.books.model import REF_SEPARATOR
from risale_mcp.catalog import WORKS
from risale_mcp.paths import BOOKS_DIR, INTERIM_DIR, ROOT

OUT_DIR = INTERIM_DIR / "review"
ASSETS = Path(__file__).resolve().parent / "review_assets"

OUTLINE_FIELDS = ("id", "title", "subtitle", "parent_id", "ref")


def available_books() -> list[dict]:
    """Ayrıştırılmış eserler, katalog sırasıyla: seçicinin listesi."""
    return [{"slug": w.slug, "title": w.title} for w in WORKS if (BOOKS_DIR / f"{w.slug}.json").exists()]


def to_view(book: dict, books: list[dict]) -> dict:
    """Eser JSON'unu arayüzün beklediği biçime çevirir. Paragraf metni olduğu gibi kalır;
    cümleler ve hâşiye işaretleri konumlarıyla gelir, arayüz onları metne yerleştirir."""
    refs = {node["id"]: node["ref"] for node in book["outline"]}
    hasiyeler = defaultdict(list)
    for p in book["paragraphs"]:
        if p["kind"] == "hasiye":
            hasiyeler[p["parent_id"]].append(p["id"])

    passages = []
    for p in book["paragraphs"]:            # hâşiye, bağlı olduğu kayıttan sonra gelir
        record = {"id": p["id"], "node_id": p["node_id"], "kind": p["kind"], "text": p["text"]}
        if p["kind"] == "hasiye":
            siblings = hasiyeler[p["parent_id"]]
            k = siblings.index(p["id"]) + 1
            name = "Hâşiye" if len(siblings) == 1 else f"Hâşiye {k}"
            refs[p["id"]] = f"{refs[p['parent_id']]}{REF_SEPARATOR}{name}"
            record |= {"parent_id": p["parent_id"], "offset": p["offset"], "label": f"Haşiye-{k}"}
        else:
            refs[p["id"]] = f"{refs[p['node_id']]}{REF_SEPARATOR}¶{int(p['id'].rsplit('/p', 1)[1])}"
        passages.append(record | {"ref": refs[p["id"]]})

    return {
        "book": book["work"],
        "title": book["title"],
        "books": books,
        "outline": [{f: n[f] for f in OUTLINE_FIELDS if n.get(f) is not None} for n in book["outline"]],
        "passages": passages,
        "sentences": [{"id": s["id"], "p": s["paragraph_id"], "s": s["start"], "e": s["end"], "n": s["n"],
                       "incipit": s["incipit"], "ref": s["ref"]} for s in book.get("sentences", [])],
    }


def embed_json(payload: dict) -> str:
    # "</script>" dizisi gömülü JSON'u erken kapatmasın.
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def render(book: dict, books: list[dict] | None = None) -> str:
    template = (ASSETS / "template.html").read_text(encoding="utf-8")
    view = to_view(book, books or [{"slug": book["work"], "title": book["title"]}])
    return (template
            .replace("/*__STYLE__*/", (ASSETS / "style.css").read_text(encoding="utf-8"))
            .replace("/*__SCRIPT__*/", (ASSETS / "app.js").read_text(encoding="utf-8"))
            .replace("__TITLE__", html.escape(book["title"]))
            .replace("__DATA__", embed_json(view)))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("works", nargs="*", help="eser slug'ları (varsayılan: ayrıştırılmış bütün eserler)")
    args = parser.parse_args()
    books = available_books()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for slug in args.works or [b["slug"] for b in books]:
        book = json.loads((BOOKS_DIR / f"{slug}.json").read_text(encoding="utf-8"))
        out = OUT_DIR / f"{slug}.html"
        out.write_text(render(book, books), encoding="utf-8")
        print(f"{out.relative_to(ROOT)}  ({out.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
