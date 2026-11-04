"""Basılı sayfa (`printed`): paragraftan cümleye (kullanıcının kararı, 2026-11-04).

Risale eserlerinde sayfa tutulmaz; bu modül yalnız kaynağı sayfa veren klasik eserler içindir (`books/beyzavi.py`).
Paragraf iki alan taşır: `printed` ({volume, page} ve sayfa aşıyorsa `end` "1/42") ve `page_breaks`
([[konum, "1/41"], …]: o konumda biten sayfa; OpenITI'nin kuralı, `openiti.py`). Cümlenin sayfası, harfinden sonra
gelen ilk sayfa sonudur; paragrafın içinde yoksa paragrafın bittiği sayfa. Sayfa kimliğe girmez, tahmin edilmez:
paragrafın sayfası bilinmiyorsa cümleninki de yoktur.
"""


def _page(value: str) -> dict:
    volume, page = value.split("/")
    return {"volume": int(volume), "page": int(page)}


def label(printed: dict) -> str:
    return f"{printed['volume']}/{printed['page']}"


def apply(data: dict) -> int:
    """Sayfası bilinen paragrafların cümlelerine `printed` yazar; yazılan cümle sayısını döndürür."""
    paragraphs = {p["id"]: p for p in data["paragraphs"] if p.get("printed")}
    count = 0
    for s in data["sentences"]:
        p = paragraphs.get(s["paragraph_id"])
        if p is None:
            continue
        last = p["printed"].get("end") or label(p["printed"])

        def page_at(pos: int) -> str:
            return next((page for at, page in p.get("page_breaks", []) if at > pos), last)

        start, end = page_at(s["start"]), page_at(s["end"] - 1)
        s["printed"] = _page(start) | ({"end": end} if end != start else {})
        count += 1
    return count
