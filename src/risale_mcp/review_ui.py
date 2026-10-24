"""Taksimat kontrol arayüzü: sozler.json -> tek dosyalık review.html.

Kullanım:
    uv run python -m risale_mcp.review_ui

Üretilen dosya sunucusuz, internetsiz açılır (veri, stil ve betik gömülüdür).
Arayüz yalnızca hiyerarşiyi gösterir; sayfa alanları HTML'e hiç yazılmaz.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / "data" / "interim" / "sozler.json"
OUT_PATH = ROOT / "data" / "interim" / "review.html"
ASSETS = Path(__file__).resolve().parent / "review_assets"

OUTLINE_FIELDS = ("id", "title", "subtitle", "parent_id", "ref")
PASSAGE_FIELDS = ("id", "node_id", "kind", "text", "parent_id", "label", "ref")


def slim(data: dict) -> dict:
    """Arayüzün ihtiyaç duyduğu alanları seçer; sayfa bilgisi bilerek dışarıda kalır."""
    pick = lambda record, fields: {f: record[f] for f in fields if record.get(f) is not None}
    return {
        "book": data["book"],
        "title": data["title"],
        "outline": [pick(o, OUTLINE_FIELDS) for o in data["outline"]],
        "passages": [pick(p, PASSAGE_FIELDS) for p in data["passages"]],
    }


def embed_json(payload: dict) -> str:
    # "</script>" dizisi gömülü JSON'u erken kapatmasın.
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def render(data: dict) -> str:
    template = (ASSETS / "template.html").read_text(encoding="utf-8")
    return (template
            .replace("/*__STYLE__*/", (ASSETS / "style.css").read_text(encoding="utf-8"))
            .replace("/*__SCRIPT__*/", (ASSETS / "app.js").read_text(encoding="utf-8"))
            .replace("__DATA__", embed_json(slim(data))))


def main() -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    OUT_PATH.write_text(render(data), encoding="utf-8")
    print(f"Arayüz: {OUT_PATH}  ({OUT_PATH.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
