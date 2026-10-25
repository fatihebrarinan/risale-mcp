"""Taksimat ve cümle kontrol arayüzü: data/books/*.json -> data/interim/review/.

Kullanım:
    uv run python -m risale_mcp.review_ui              # bütün eserler
    uv run python -m risale_mcp.review_ui sozler       # yalnızca seçilenlerin metni yenilenir
    xdg-open data/interim/review/index.html

Tek sayfadır: sol paneldeki ağaçta bütün eserler gruplarıyla durur. Sayfa sunucusuz,
internetsiz açılır. Bütün eserlerin başlık ağaçları `index.html`'in içindedir (küçüktür); bir
eserin paragraf ve cümleleri `data/<eser>.js` dosyasındadır ve o eserden bir başlık açılınca
yüklenir. Arayüz yalnızca hiyerarşiyi gösterir; sayfa bilgisi veride zaten yoktur.
"""

import argparse
import html
import json
from collections import Counter, defaultdict
from pathlib import Path

from risale_mcp.books.model import REF_SEPARATOR
from risale_mcp.catalog import WORKS
from risale_mcp.checklist import GROUP_TITLES
from risale_mcp.paths import BOOKS_DIR, INTERIM_DIR, ROOT

OUT_DIR = INTERIM_DIR / "review"
DATA_DIR = OUT_DIR / "data"
ASSETS = Path(__file__).resolve().parent / "review_assets"
TITLE = "Risale-i Nur Taksimat Kontrolü"

OUTLINE_FIELDS = ("id", "title", "subtitle", "parent_id", "ref", "sources")


def load_books() -> list[dict]:
    """Ayrıştırılmış eserler, katalog sırasıyla."""
    paths = [BOOKS_DIR / f"{w.slug}.json" for w in WORKS]
    return [json.loads(p.read_text(encoding="utf-8")) for p in paths if p.exists()]


def index_view(books: list[dict]) -> dict:
    """Sayfanın kendisine gömülen veri: eserler, gruplar ve bütün başlık ağaçları."""
    works = []
    outline = []
    for book in books:
        own = Counter(p["node_id"] for p in book["paragraphs"] if p["kind"] != "hasiye")
        works.append({
            "slug": book["work"], "title": book["title"], "group": book["group"],
            "language": book.get("language", "tr"),
            "counts": {"nodes": len(book["outline"]), "passages": sum(own.values()),
                       "sentences": len(book.get("sentences", []))},
        })
        outline += [{f: n[f] for f in OUTLINE_FIELDS if n.get(f) is not None} | {"p": own[n["id"]]}
                    for n in book["outline"]]
    groups = [{"id": str(g), "title": t} for g, t in GROUP_TITLES.items() if any(w["group"] == g for w in works)]
    return {"title": TITLE, "groups": groups, "works": works, "outline": outline}


def book_view(book: dict) -> dict:
    """Bir eserin metni: `data/<eser>.js`. Paragraf metni olduğu gibi kalır; cümleler ve hâşiye
    işaretleri konumlarıyla gelir, arayüz onları metne yerleştirir."""
    refs = {node["id"]: node["ref"] for node in book["outline"]}
    hasiyeler = defaultdict(list)
    for p in book["paragraphs"]:
        if p["kind"] == "hasiye":
            hasiyeler[p["parent_id"]].append(p["id"])

    passages = []
    for p in book["paragraphs"]:            # hâşiye, bağlı olduğu kayıttan sonra gelir
        # Ana cilde eşlenmiş paragrafın metni yoktur; `source` ana ciltteki paragraflardır.
        record = {"id": p["id"], "node_id": p["node_id"], "kind": p["kind"], "text": p.get("text", "")}
        if "source" in p:
            record["source"] = p["source"]
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
        "passages": passages,
        "sentences": [{"id": s["id"], "p": s["paragraph_id"], "s": s["start"], "e": s["end"], "n": s["n"],
                       "incipit": s["incipit"], "ref": s["ref"]} for s in book.get("sentences", [])],
    }


def embed_json(payload: dict) -> str:
    # "</script>" dizisi gömülü JSON'u erken kapatmasın.
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def render_index(books: list[dict]) -> str:
    template = (ASSETS / "template.html").read_text(encoding="utf-8")
    return (template
            .replace("/*__STYLE__*/", (ASSETS / "style.css").read_text(encoding="utf-8"))
            .replace("/*__SCRIPT__*/", (ASSETS / "app.js").read_text(encoding="utf-8"))
            .replace("__TITLE__", html.escape(TITLE))
            .replace("__DATA__", embed_json(index_view(books))))


def render_book(book: dict) -> str:
    """`<script src>` ile yüklenen veri dosyası; dosya adresinden (file://) de çalışır."""
    return f"RisaleReview.register({embed_json(book_view(book))});\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("works", nargs="*", help="metni yenilenecek eser slug'ları (varsayılan: hepsi)")
    args = parser.parse_args()
    books = load_books()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for book in books:
        if not args.works or book["work"] in args.works:
            (DATA_DIR / f"{book['work']}.js").write_text(render_book(book), encoding="utf-8")
    for old in OUT_DIR.glob("*.html"):            # eski, eser başına bir dosyalık arayüz
        if old.stem in {w.slug for w in WORKS}:
            old.unlink()
    out = OUT_DIR / "index.html"
    out.write_text(render_index(books), encoding="utf-8")
    size = sum(p.stat().st_size for p in DATA_DIR.glob("*.js")) / 1e6
    print(f"{out.relative_to(ROOT)}  ({out.stat().st_size / 1e6:.1f} MB; eser metinleri {size:.0f} MB)")


if __name__ == "__main__":
    main()
