"""Saykalü'l-İslâm Word dosyaları (Kızıl İcaz, Ta'likat, Hutbe-i Şamiye'nin Arapçası) ve Ta'likat'ın Türkçesi.

Satırlar elle yazılmıştır; Word dosyası gerekmez. Son testler gerçek eserleri kullanır; yoksa atlanır.
"""

import json
import re

import pytest

from risale_mcp.books.rasaelalnour import Row
from risale_mcp.books.saykal import (OUR_TITLE, TALIKAT_SECTIONS, parse_hutbe, parse_kizil_icaz, parse_talikat_arabic)
from risale_mcp.catalog import get_work
from risale_mcp.paths import BOOKS_DIR
from risale_mcp.sentences import segment


def page(n: int, book: str = "قزل إيجاز") -> Row:
    return Row(f"صيقل الإسلام/{book} - ص: {n}")


def b(text: str) -> Row:
    return Row(text, bold=True)


KIZIL = [
    b("قزل ايجاز"), page(164),
    b("ايضاح"), Row("على كل حال فقد كتبتُ هذا الاثر."), Row("سعيد"),
    Row("ملاحظة: قام السيد الفاضل بتصحيح هذه الرسالة."), Row("احسان قاسم الصالحي"),
    page(165), b("بسم الله الرحمن الرحيم"), Row("\"مقدمة الملا عبدالمجيد النورسي\""), Row("أشكر على حمدي."),
    page(167), b("بسم [1] الله [2] الرحمن"),
    Row("[1] الباء للمصاحبة 1."), Row("[2] مستجمع لجميع الصفات 2."),
    Row("_____"), Row("1 (الباء للمصاحبة) اذ يلزم."), Row("2 (مستجمع) أي البيّن."),
    page(168), b("فصل في جواز الاشتغال به"), b("والخلف [1] في جواز الاشتغال به"),
    Row("[1] اعلم! أن الخلاف لفظي."), b("[2] اعلم!"), Row("كلام في المسألة."),
    b("اعتذار"), Row("لئن ادركت في شرحي فتوراً"),
]


def test_kizil_icaz_layers():
    book, report = parse_kizil_icaz(get_work("kizil-icaz-arabi"), KIZIL)
    data = book.to_json()
    ids = [n["id"].removeprefix("kizil-icaz-arabi/") for n in data["outline"][1:]]
    assert ids == ["izah", "dibace", "fasl-01"]
    kinds = [(p["kind"], p["text"]) for p in data["paragraphs"]]
    assert ("quote", "بسم [1] الله [2] الرحمن") in kinds                   # Süllem'in beyti: müellifin değil
    assert ("paragraph", "[1] الباء للمصاحبة.") in kinds                  # "[1]" kalır, dipnot işareti gider
    assert ("paragraph", "[2] اعلم!") in kinds                           # kalın ama müellifin bahsi
    assert not any("أشكر" in t or "ملاحظة" in t or "لئن" in t for _, t in kinds)
    assert data["notes"][1:] == []                                       # şerh not değil, okunur katman
    sharh = [p for p in data["paragraphs"] if p.get("commentator")]
    assert [(p["kind"], p["text"], p["commentator"]) for p in sharh] == [
        ("hasiye", "(الباء للمصاحبة) اذ يلزم.", "Abdülmecid Nursî"), ("hasiye", "(مستجمع) أي البيّن.", "Abdülmecid Nursî")]
    assert all(p["id"].rsplit("/", 1)[1] == "s1" for p in sharh)
    assert data["outline"][2]["subtitle"] == OUR_TITLE                    # "ديباجة" kaynakta yok
    refs = {x["id"].split("/", 1)[1]: x["ref"] for x in segment(data)}
    assert refs["dibace/c002/s1/c001"].endswith("› ديباجة › 2. cümle › Şerh › 1. cümle")
    assert report.unanchored == []


TALIKAT = [Row("مقدمة المحقق لا تؤخذ."), b("بسم الله الرحمن الرحيم"), Row("اعلم! ان المنطق آلة 1."),
           Row("_____"), Row("1 كما صار عادة.(تقرير)"),
           page(254, "تعليقات"), Row("[فصل في الكليّ والجزئي] 1"), Row("كلام."),
           Row("_____"), Row("1 كلنبوي ص/3 س/22"), page(255, "تعليقات")]
TALIKAT += [Row(f"[{s.arabic}] كلام في الباب.") for s in TALIKAT_SECTIONS[1:] if s.local != "mukaddime"]
TALIKAT.insert(11, b("مقدمة:"))


def test_talikat_sections_and_footnotes():
    book, _ = parse_talikat_arabic(get_work("talikat-arabi"), TALIKAT)
    data = book.to_json()
    ids = [n["id"].removeprefix("talikat-arabi/") for n in data["outline"][1:]]
    assert ids == [s.local for s in TALIKAT_SECTIONS]
    assert not any("لا تؤخذ" in p["text"] for p in data["paragraphs"])
    hasiye = [p["text"] for p in data["paragraphs"] if p["kind"] == "hasiye"]
    assert hasiye == ["كما صار عادة.(تقرير)"]                             # müellifin derste yazdırdığı
    assert "كلنبوي ص/3 س/22" in [n["text"] for n in data["notes"]]          # Badıllı'nın Burhân göndermesi
    hadd = next(n for n in data["outline"] if n["id"].endswith("/hadd"))
    assert hadd.get("heading") == "inline"                                # alıntıdan sonra metin sürüyor


def test_hutbe_ids_follow_the_turkish_work(tmp_path):
    turkish = tmp_path / "hutbe.json"
    titles = {"mukaddime": "Arabî Hutbe‑i Şâmiye’nin Mukaddimesidir", "zeyl": "Hutbe‑i Şâmiye’nin Zeylinin Zeyli",
              "zeyl/hakikat": "Hakikat", "hakikat-cekirdekleri": "Hakikat Çekirdekleri",
              "zeyl/reddul-evham": "Reddü'l‑Evhâm"}
    turkish.write_text(json.dumps({"outline": [{"id": "h", "title": "x"}] + [
        {"id": f"h/{k}", "title": v} for k, v in titles.items()]}, ensure_ascii=False), encoding="utf-8")
    rows = [b("بين يدي هذه الرسالة"), Row("مقدمة المحقق."), b("مقدّمة"), b("الخطبة الشامية للمؤلف"),
            Row("هذه الرسالة 1."), Row("_____"), Row("1 تعداد المسلمين آنذاك. المترجم"),
            page(482, "الخطبة الشامية"), b("ذيل الذيل"), b("حـقيـقـة"), Row("ان السبيل 1."), Row("_____"),
            Row("1 اي التوحيد. المؤلف."), page(483, "الخطبة الشامية"), b("رد الاوهام"), b("الوهم الاول:"), Row("كلام."), Row("سعيد النورسي")]
    book, _ = parse_hutbe(get_work("hutbe-i-samiye-arabi"), rows, turkish)
    data = book.to_json()
    ids = [n["id"].removeprefix("hutbe-i-samiye-arabi/") for n in data["outline"][1:]]
    assert ids == ["mukaddime", "zeyl", "zeyl/hakikat", "zeyl/reddul-evham", "zeyl/reddul-evham/vehim-01"]
    assert data["outline"][0]["subtitle"].startswith("İhsan Kasım")
    assert data["outline"][1]["subtitle"] == "الخطبة الشامية للمؤلف"
    assert [p["text"] for p in data["paragraphs"] if p["kind"] == "hasiye"] == ["اي التوحيد"]
    assert data["paragraphs"][-1]["kind"] == "signature"


@pytest.mark.parametrize("slug", ["talikat", "talikat-arabi"])
def test_real_talikat_is_parallel(slug):
    path = BOOKS_DIR / f"{slug}.json"
    if not path.exists():
        pytest.skip(f"{slug}.json yok")
    data = json.loads(path.read_text(encoding="utf-8"))
    assert [n["id"].removeprefix(f"{slug}/") for n in data["outline"][1:]] == [s.local for s in TALIKAT_SECTIONS]
    assert not any("[Sayfa:" in p["text"] or re.search(r"(?:^|\s)ص:\s*\d", p["text"]) for p in data["paragraphs"])


def test_real_hutbe_sections_exist_in_turkish():
    arabic, turkish = BOOKS_DIR / "hutbe-i-samiye-arabi.json", BOOKS_DIR / "hutbe-i-samiye.json"
    if not (arabic.exists() and turkish.exists()):
        pytest.skip("Hutbe-i Şamiye JSON'ları yok")
    tr = {n["id"].removeprefix("hutbe-i-samiye/") for n in json.loads(turkish.read_text())["outline"]}
    ar = {n["id"].removeprefix("hutbe-i-samiye-arabi/") for n in json.loads(arabic.read_text())["outline"][1:]}
    assert ar - tr == {"zeyl/fihristul-makasid-fikrasi"}               # Türkçede ayrı bölüm değil
