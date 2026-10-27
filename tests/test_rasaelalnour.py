"""İşârâtü'l-İ'câz'ın Arapça aslı (rasaelalnour.com Word dosyası) ayrıştırıcısı.

Satırlar elle yazılmıştır; Word dosyası gerekmez. Son test gerçek dosyayı kullanır; yoksa atlanır.
"""

import json

import pytest

from risale_mcp.books.rasaelalnour import Row, parse_rows
from risale_mcp.catalog import get_work
from risale_mcp.paths import BOOKS_DIR

WORK = get_work("isaratul-icaz-arabi")


def page(n: int) -> Row:
    return Row(f"إشارات الإعجاز - ص: {n}", "end")


def c(text: str) -> Row:
    return Row(text, "center")


ROWS = [
    c("هذا التحقيق"), Row("مقدمة المحقق لا تؤخذ."),                       # muhakkikin girişi: alınmaz
    c("مقدمة الترجمة التركية"), c("تنبيه"), Row("لقد تم تأليف التفسير."),
    Row("النكتة الاولى:"), Row("نكتة اولى."),
    c("افادة المرام"), Row("اقول: كلام المؤلف 1 هنا."),
    Row("_____________________"), Row("1 جواب لما .. (المؤلف)."),
    page(2),
    c("لمعة من تعريف القرآن"), Row("القرآن ما هو؟"),
    c("بسْمِ الله الرَّحْمَن الرَّحِيم"), Row("فنحمده."),
    Row("(الحَمْدُ)"), Row("وجه النظم: ان الرحمن 1 والرحيم"),
    Row("_____________________"), Row("1 اى الانعام (ت: 16)"),
    page(3),
    Row("دلتا على النعم."),                                                # sayfa sonunda bölünen paragraf
    c("***"), c("بسْمِ الله الرَّحْمَن الرَّحِيم"), c("السورة الاولى من الزَّهْرَاوَيْنِ 1"),
    Row("ان قلت: في القرآن تكرار."),
    Row("(1) عن ابى أمامة رضى الله عنه."),                                 # çizgisiz sayfanın dipnotu
    page(4),
    c("الم 1"), Row("المبحث الاول:"), Row("ان الاعجاز قد تنفس."),
    c("***"), c("خَتَمَ الله عَلَى قُلُوبِهِمْ"), c("وَلَهُمْ عَذابٌ عَظِيمٌ 2"),       # numara son satırda
    c("مـقـدمـة"), Row("اعلم!"),
    page(5),
    c("وَاِذَا قِيلَ لَهُمْ لا تُفْسِدُوا 1"), c("أَلا اِنَّهُمْ هُمُ الْمُفْسِدُونَ 4"),  # 3 eksik basılmış
    Row("كلام."), c("***"), c("أَلا اِنَّهُمْ هُمُ الْمُفْسِدُونَ 4"),         # tekrar: bölüm açmaz
    Row("وايضا."),
    c("باسمه سبحانه"), Row("كلمة لستة من طلاب النور: لا تؤخذ."),
]


@pytest.fixture(scope="module")
def book():
    book, report = parse_rows(WORK, ROWS)
    return book.to_json(), report


def test_structure_follows_the_turkish_work(book):
    data, _ = book
    titles = {n["id"].removeprefix("isaratul-icaz-arabi/"): (n["title"], n.get("subtitle")) for n in data["outline"]}
    assert list(titles)[1:] == [
        "mukaddime-tercume", "mukaddime-tercume/tenbih", "mukaddime-tercume/tenbih/nukte-01",
        "ifadetul-meram", "kuran-nedir-tarifi-nasildir", "sure-i-fatiha", "sure-i-fatiha/el-hamdu",
        "sure-i-bakara", "sure-i-bakara/1", "sure-i-bakara/1/mebhas-01", "sure-i-bakara/2",
        "sure-i-bakara/2/mukaddime", "sure-i-bakara/3-4-ayetlerin-tefsiri"]
    assert titles["mukaddime-tercume"][1].startswith("İhsan Kasım")             # müellifin Türkçesinin tercümesi
    assert titles["sure-i-bakara/2"] == ("2. Âyetin Tefsiri", "خَتَمَ الله عَلَى قُلُوبِهِمْ وَلَهُمْ عَذابٌ عَظِيمٌ")
    assert titles["sure-i-bakara/3-4-ayetlerin-tefsiri"][0] == "3‑4. Âyetlerin Tefsiri"


def test_text_without_pages_editor_matter_and_markers(book):
    data, report = book
    texts = [p["text"] for p in data["paragraphs"]]
    assert not any("ص:" in t or "لا تؤخذ" in t for t in texts)
    assert "اقول: كلام المؤلف هنا." in texts                                  # dipnot işareti silindi
    assert "وجه النظم: ان الرحمن والرحيم دلتا على النعم." in texts             # sayfa sonunda birleşti
    repeated = [p for p in data["paragraphs"] if p["text"].endswith("الْمُفْسِدُونَ 4")]
    assert repeated and repeated[0]["center"]                                    # tekrar edilen âyet
    assert report.unanchored == []


def test_footnotes_by_author_translator_and_editor(book):
    data, _ = book
    hasiye = [p for p in data["paragraphs"] if p["kind"] == "hasiye"]
    assert [(h["parent_id"].rsplit("/", 1)[-1], h["text"]) for h in hasiye] == [("p001", "جواب لما ..")]
    notes = [n["text"] for n in data["notes"][1:]]
    assert notes == ["(Türkçe tercümeden) اى الانعام", "عن ابى أمامة رضى الله عنه."]


def test_real_isarat():
    path = BOOKS_DIR / "isaratul-icaz-arabi.json"
    if not path.exists():
        pytest.skip("isaratul-icaz-arabi.json yok; önce `uv run python -m risale_mcp.build isaratul-icaz-arabi`")
    data = json.loads(path.read_text(encoding="utf-8"))
    ids = {n["id"].removeprefix("isaratul-icaz-arabi/") for n in data["outline"]}
    turkish = json.loads((BOOKS_DIR / "isaratul-icaz.json").read_text(encoding="utf-8"))
    sections = {n["id"].removeprefix("isaratul-icaz/") for n in turkish["outline"]
                if n["parent_id"] in ("isaratul-icaz/sure-i-bakara", "isaratul-icaz/sure-i-fatiha")}
    # Arapça baskı 21 ve 22. âyetleri tek bölümde işler; Türkçede "Birinci kısım" basılı bir başlıktır.
    assert sections - ids == {"sure-i-bakara/21", "sure-i-bakara/22", "sure-i-bakara/kisim-01"}
    assert sum(p["kind"] == "hasiye" for p in data["paragraphs"]) == 6
