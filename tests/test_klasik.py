"""Klasik eserlerin ayrıştırma kuralları (E2.3, `books/klasik_openiti.py`): ham veri diskteyse gerçek metinle."""

import pytest

from risale_mcp.books import klasik_openiti
from risale_mcp.catalog import get_work
from risale_mcp.paths import RAW_DIR
from risale_mcp.sentences import split_paragraph

RAW = RAW_DIR / "openiti"


def _book(slug):
    if not (RAW / f"{slug}.txt").exists():
        pytest.skip("ham veri yok (uv run python -m risale_mcp.fetch klasik)")
    book, report = klasik_openiti.parse(get_work(slug))
    return book.to_json(), report


def test_verse_is_one_sentence():
    # mısraları ayıran "..." cümle sonu değildir
    para = {"kind": "poem", "verse": True, "text": "يا شبيه البدر في الحس ... ن وفي بعد المنال"}
    assert split_paragraph(para) == [(0, len(para["text"]))]
    assert klasik_openiti._is_verse(para["text"])
    assert not klasik_openiti._is_verse("هذا كلام طويل ... ثم يتم الكلام ويستمر حتى ينتهي.")


def test_heading_inside_text_goes_back_into_the_text():
    # Esrâr: metindeki "فصلا" kelimesinin "فصل"i başlık diye işaretlenmiş; kelime bölünmeden geri katılır
    book, report = _book("esrarul-belaga")
    texts = " ".join(p["text"] for p in book["paragraphs"])
    assert "لا تجد فصلا بين" in texts
    assert "</span>" not in texts
    assert any(n["title"] == "مقدمة المصنف" for n in book["outline"])


def test_miftah_preface_list_stays_text():
    # Miftâh: mukaddimedeki "القسم الأول في علم الصرف، القسم الثاني…" sayımı başlık değil, metin
    book, _ = _book("miftahul-ulum")
    assert any("القسم الأول في علم الصرف، القسم الثاني في علم النحو" in p["text"] for p in book["paragraphs"])


def test_delail_layers_and_fikra():
    book, report = _book("delailul-icaz")
    intro = next(n for n in book["outline"] if n["id"] == "delailul-icaz/mukaddime-tahkik")
    assert intro.get("authority") == "muhakkik" and intro.get("by") == "Mahmûd Muhammed Şâkir"
    assert next(n for n in book["outline"] if n["id"] == "delailul-icaz/1/f1")["title"] == "1"
    assert not any("الفهارس" == n["title"] for n in book["outline"])        # fihrist alınmaz
    assert report.fikra > 600


def test_mufredat_entries_from_roots():
    book, report = _book("mufredat")
    kitab = [n for n in book["outline"] if n.get("parent_id") == "mufredat" and n["id"] != "mufredat/mukaddime"]
    assert [n["title"] for n in kitab][-3:] == ["كتاب الواو", "كتاب الهاء", "كتاب الياء"]    # bu baskının sırası
    assert len(kitab) == 28 and report.entries == 1600
    first = next(n for n in book["outline"] if n["id"] == "mufredat/01/001")
    assert first["title"] == "أبا"
    texts = " ".join(p["text"] for p in book["paragraphs"])
    assert "= كتاب" not in texts and " | " not in texts


def test_no_unpaged_front_matter_page():
    book, _ = _book("delailul-icaz")
    assert not any(p.get("printed", {}).get("volume") == 0 for p in book["paragraphs"])


# ---------------------------------------------------------------- E5 (`books/klasik_serh.py`)

from risale_mcp.books import klasik_serh  # noqa: E402
from risale_mcp.books.model import Book  # noqa: E402


def test_ordinals():
    o = lambda s: klasik_serh.ordinal(klasik_serh.fold(s).split())
    assert o("الأول في المقدمات") == 1 and o("الثانى") == 2 and o("الحادي عشر") == 11
    assert o("الرابع العشر") == 14 and o("الثالث والعشرون") == 23 and o("في الطريق") is None
    assert klasik_serh.heading_kind("المقصر الثاني") == ("المقصد", 2)          # dizgi hatası
    assert klasik_serh.heading_kind("قدم مباحث الوجود") == (None, None)


def _tree(relaxed=False, ranks=None):
    book = Book("x", "X", {})
    return book, klasik_serh.Tree(book, klasik_serh.Report(), relaxed=relaxed, ranks=ranks)


def test_series_rule():
    book, t = _tree()
    m1 = t.place("الموقف الأول", None)
    r1 = t.place("المرصد الأول", None)
    assert t.place("المقصد الأول", None).parent is r1
    assert t.place("المرصد الثالث في الكم", None) is None        # içindekiler satırı: seri tutmuyor, metin kalır
    r2 = t.place("المرصد الثاني", None)
    assert r2.parent is m1
    assert t.place("المرصد الثاني", None) is None                # tekrar
    intro = t.place("المقدمة", None)
    assert intro.parent is r2
    assert t.place("الفصل الأول", None).parent is r2              # sırasız bölüm kapanır
    assert t.place("الموقف الثاني", None).parent is book.root


def test_relaxed_ranks_keep_levels():
    # Makāsıd: serinin ilki eksik olsa da fasıl mebhasın altına girmez
    book, t = _tree(relaxed=True, ranks={"المقصد": 1, "الفصل": 2, "المبحث": 3})
    m = t.place("المقصد الثالث", None)
    b = t.place("المبحث الثاني", None)
    assert b.parent is m
    f = t.place("الفصل الثاني", None)
    assert f.parent is m
    assert t.place("الفصل الثاني", None) is None                 # aktarmanın tekrarı
    assert t.place("المبحث الأول", None).parent is f


def test_mevakif_layers_and_tree():
    book, report = _book("serhul-mevakif")
    nodes = {n["id"]: n for n in book["outline"]}
    assert nodes["serhul-mevakif/1/1"]["title"].startswith("المرصد الأول")
    assert nodes["serhul-mevakif/1/2"]["title"].startswith("المرصد الثاني")
    matn = [n for n in book["outline"] if n.get("authority") == "metin"]
    assert len(matn) > 140 and all(n["by"] == "Adudüddîn el-Îcî" and n["title"] == "المتن" for n in matn)
    fixed = next(n for n in book["outline"] if n["title"] == "المرصد الرابع في الوحدة والكثرة")
    assert "düzeltildi" in fixed["subtitle"]


def test_makasid_and_telvih():
    book, _ = _book("serhul-makasid")
    tops = [n["title"] for n in book["outline"] if n.get("parent_id") == "serhul-makasid"]
    assert tops[0] == "مقدمة المؤلف" and tops[1:] == [f"المقصد {x}" for x in
                                                       ("الأول", "الثاني", "الثالث", "الرابع", "الخامس", "السادس")]
    book, report = _book("telvih")
    assert report.unmatched < 60 and len(book["outline"]) > 150
    assert any(p["text"].startswith("قوله المقدمة الأولى") for p in book["paragraphs"]
               if p["node_id"] == "telvih/3/3/4/3")                # Risale'nin andığı Mukaddemât (risale_refs)


def test_risale_refs_point_to_works():
    from risale_mcp.catalog.klasik import KLASIK_WORKS, RISALE_REFS, RISALE_UNNAMED
    slugs = {w.slug for w in KLASIK_WORKS}
    assert set(RISALE_REFS) <= slugs and set(RISALE_UNNAMED) <= slugs
    assert not set(RISALE_REFS) & set(RISALE_UNNAMED)
    assert all(r["kind"] in ("havale", "nakil", "degerlendirme") and r["note"] for refs in RISALE_REFS.values()
               for r in refs)


def test_ihya_tahric_is_iraqis_commentary():
    book, report = _book("ihya")
    body = [p for p in book["paragraphs"] if p["kind"] != "hasiye"]
    notes = [p for p in book["paragraphs"] if p["kind"] == "hasiye"]
    assert report.lost == 0 and len(notes) > 4400
    assert all(p["commentator"] == "Zeynüddîn el-Irâkî" for p in notes)
    assert not any("+" in p["text"] for p in body)                     # "+ حديث … +" işaretleri metinden ayrıldı
    assert any(p["text"] == "فيه ميزابان يصبان فيه من الكوثر" for p in body)   # tahric paragraf sonunda biter
    assert any(p["text"].startswith("الحمد لله الذي أحيا علوم الدين") for p in notes)  # Irâkî'nin mukaddimesi
    assert not any(p["text"].startswith("الحمد لله الذي أحيا علوم الدين") for p in body)
    assert len(book["outline"]) > 600
