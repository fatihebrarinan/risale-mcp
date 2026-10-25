"""Taksimat kontrol arayüzü: data/books/<eser>.json -> tek dosyalık review.html.

Kullanım:
    uv run python -m risale_mcp.review_ui            # Sözler
    uv run python -m risale_mcp.review_ui mektubat

Üretilen dosya sunucusuz, internetsiz açılır (veri, stil ve betik gömülüdür).
Arayüz yalnızca hiyerarşiyi gösterir; sayfa bilgisi veride zaten yoktur.
"""

import argparse
import html
import json
from collections import defaultdict
from pathlib import Path

from risale_mcp.books.model import REF_SEPARATOR
from risale_mcp.paths import BOOKS_DIR, INTERIM_DIR

OUT_PATH = INTERIM_DIR / "review.html"
ASSETS = Path(__file__).resolve().parent / "review_assets"

OUTLINE_FIELDS = ("id", "title", "subtitle", "parent_id", "ref")


def _marker(k: int) -> str:
    return f"(Haşiye-{k})"


def _with_markers(text: str, offsets: list[int]) -> str:
    """Hâşiye işaretlerini metindeki konumlarına yerleştirir: "… içindir. (Haşiye-1) Şükür …"."""
    out, last = [], 0
    for k, offset in enumerate(offsets, 1):
        out += [text[last:offset], f" {_marker(k)}"]
        last = offset
    out.append(text[last:])
    return "".join(out)


def to_view(book: dict) -> dict:
    """Eser JSON'unu arayüzün beklediği biçime çevirir: hâşiye işaretleri metne yerleşir,
    her kayıt görüntülenecek bir atıf (`ref`) taşır."""
    refs = {node["id"]: node["ref"] for node in book["outline"]}  # düğüm ya da paragraf -> atıf
    hasiyeler = defaultdict(list)
    for p in book["paragraphs"]:
        if p["kind"] == "hasiye":
            hasiyeler[p["parent_id"]].append(p)

    passages = []
    for p in book["paragraphs"]:            # hâşiye, bağlı olduğu kayıttan sonra gelir
        label = None
        if p["kind"] == "hasiye":
            siblings = hasiyeler[p["parent_id"]]
            k = siblings.index(p) + 1
            label = _marker(k)[1:-1]
            name = "Hâşiye" if len(siblings) == 1 else f"Hâşiye {k}"
            refs[p["id"]] = f"{refs[p['parent_id']]}{REF_SEPARATOR}{name}"
        else:
            refs[p["id"]] = f"{refs[p['node_id']]}{REF_SEPARATOR}¶{int(p['id'].rsplit('/p', 1)[1])}"
        own = hasiyeler.get(p["id"], [])
        record = {"id": p["id"], "node_id": p["node_id"], "kind": p["kind"],
                  "text": _with_markers(p["text"], [h["offset"] for h in own]),
                  "parent_id": p.get("parent_id"), "label": label, "ref": refs[p["id"]]}
        passages.append({key: value for key, value in record.items() if value is not None})

    return {
        "book": book["work"],
        "title": book["title"],
        "outline": [{f: n[f] for f in OUTLINE_FIELDS if n.get(f) is not None} for n in book["outline"]],
        "passages": passages,
    }


def embed_json(payload: dict) -> str:
    # "</script>" dizisi gömülü JSON'u erken kapatmasın.
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def render(book: dict) -> str:
    template = (ASSETS / "template.html").read_text(encoding="utf-8")
    return (template
            .replace("/*__STYLE__*/", (ASSETS / "style.css").read_text(encoding="utf-8"))
            .replace("/*__SCRIPT__*/", (ASSETS / "app.js").read_text(encoding="utf-8"))
            .replace("__TITLE__", html.escape(book["title"]))
            .replace("__DATA__", embed_json(to_view(book))))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("work", nargs="?", default="sozler", help="eser slug'ı (varsayılan: sozler)")
    args = parser.parse_args()
    book = json.loads((BOOKS_DIR / f"{args.work}.json").read_text(encoding="utf-8"))
    OUT_PATH.write_text(render(book), encoding="utf-8")
    print(f"Arayüz: {OUT_PATH}  ({OUT_PATH.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
