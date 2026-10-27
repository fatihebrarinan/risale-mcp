"""Aşama 14: âyet ilişkileri (`ayah_links.py`).

Her tür için elle yazılmış küçük bir eser ve `conftest.py`'deki küçük Kur'ân'la kurulan veritabanı.
"""

import json
import sqlite3

import pytest

from conftest import AYAH, mini_quran
from risale_mcp.build_db import build
from risale_mcp.library import Library

IHLAS = "قُلْ هُوَ اللّٰهُ اَحَدٌ"
OPENING = "وَاِنْ مِنْ شَيْءٍ اِلَّا يُسَبِّحُ بِحَمْدِه۪"
SECTIONS = {   # bölüm -> paragraflar (tür, metin, cümleler)
    "lemalar/1": [("paragraph", f"Birinci: {AYAH} âyeti buna işâret eder.", None)],
    "lemalar/2": [("arabic", AYAH, None), ("paragraph", "Bu bölüm hayattan bahseder.", None)],
    "lemalar/3": [("paragraph", "Bir. İki. Üç: {AYAH} sırrınca herşey tesbih eder.".replace("{AYAH}", AYAH),
                   ["Bir.", "İki.", f"Üç: {AYAH} sırrınca herşey tesbih eder."])],
    "lemalar/4": [("paragraph", f"Ferman: {IHLAS} Yani, Allah birdir.", None)],
    "lemalar/fihrist/5": [("paragraph", f"Özet: {AYAH} âyetine işâret eder.", None)],
    # risale adı kanıt değil; sûre adı olarak anılan âyet zayıf; uzaktaki "işâret" zayıf
    "lemalar/6": [("paragraph", f"İşârât‑ı Kur'âniye risalesinde {AYAH} geçer.", None)],
    "lemalar/7": [("paragraph", f"Sûre‑i {IHLAS} mânâsını soruyor.", None)],
    "lemalar/8": [("paragraph", f"Pek uzun bir cümlenin ortasında {AYAH} geçer, sonra bir iki üç dört beş altı yedi "
                                "sekiz dokuz kelimeden sonra işâret eder.", None)],
}
LETTERS = {   # mektubun açılış ibaresi açılış ilişkisi değildir; Sözler'deki aynı açılış öyledir
    "mektubat/1": [("arabic", f"{OPENING}", None), ("paragraph", "Aziz kardeşlerim.", None)],
}
WINDOWS = {"sozler/33": [("arabic", f"{OPENING}", None), ("paragraph", "Her şey tesbih eder.", None)]}


def _book(work: str, sections: dict) -> dict:
    outline = [{"id": work, "parent_id": None, "title": work, "ref": work}]
    paragraphs, sentences = [], []
    for node, paras in sections.items():
        parent = node.rsplit("/", 1)[0]
        if not any(n["id"] == parent for n in outline):
            outline.append({"id": parent, "parent_id": work, "title": parent, "ref": parent})
        outline.append({"id": node, "parent_id": parent, "title": node, "ref": f"{work} › {node}"})
        n = 0
        for i, (kind, text, parts) in enumerate(paras, 1):
            pid = f"{node}/p{i:03}"
            arabic = []
            for ayah, source in ((AYAH, "Bakara Sûresi, 2:255"), (IHLAS, "İhlâs Sûresi, 112:1"),
                                 (OPENING, "İsrâ Sûresi, 17:44")):
                if ayah in text:
                    start = text.index(ayah)
                    arabic.append({"start": start, "end": start + len(ayah), "kind": "ayet", "meal": "", "source": source})
            paragraphs.append({"id": pid, "node_id": node, "kind": kind, "text": text, "arabic": arabic})
            for part in parts or [text]:
                n += 1
                start = text.index(part)
                sentences.append({"id": f"{node}/c{n:03}", "node_id": node, "paragraph_id": pid, "n": n,
                                  "start": start, "end": start + len(part), "text": part, "incipit": part[:20],
                                  "hash": "0" * 12, "ref": f"{work} › {node} › {n}. cümle"})
    return {"work": work, "title": work, "group": "ana-cilt", "source": {}, "outline": outline,
            "paragraphs": paragraphs, "sentences": sentences, "notes": [], "gaps": []}


@pytest.fixture(scope="module")
def db_path(tmp_path_factory):
    books = tmp_path_factory.mktemp("books")
    for work, sections in (("lemalar", SECTIONS), ("mektubat", LETTERS), ("sozler", WINDOWS),
                           ("sualar", {"sualar/1": [("paragraph", f"Bu {AYAH} âyeti Risale‑i Nur’a işâret eder.", None)]})):
        (books / f"{work}.json").write_text(json.dumps(_book(work, sections), ensure_ascii=False), "utf-8")
    data = mini_quran()
    isra = [{"ayah": n, "text": "نَصٌّ", "text_simple": "نَصٌّ", "text_clean": "نص", "translations": {}} for n in range(1, 45)]
    isra[43] = {"ayah": 44, "text": "وَإِن مِّن شَىْءٍ إِلَّا يُسَبِّحُ بِحَمْدِهِۦ", "text_simple": "",
                "text_clean": "وإن من شيء إلا يسبح بحمده", "translations": {}}
    data["suras"].insert(1, {"number": 17, "name": "İsrâ", "name_ar": "الإسراء", "ayahs": isra})
    quran = tmp_path_factory.mktemp("quran") / "quran.json"
    quran.write_text(json.dumps(data, ensure_ascii=False), "utf-8")
    out = books / "test.db"
    build(books, out, quran)
    return out


def test_link_kinds_scopes_and_strength(db_path):
    rows = sqlite3.connect(db_path).execute(
        "SELECT node_id, kind, strength, scope, sura, ayah_start, evidence_id FROM ayah_links ORDER BY node_id").fetchall()
    assert rows == [
        ("lemalar/1", "isaret", "strong", "section", 2, 255, "lemalar/1/c001"),        # ilk cümlede, metin söylüyor
        ("lemalar/2", "acilis", "strong", "section", 2, 255, "lemalar/2/c001"),        # bölüm âyetle açılıyor
        ("lemalar/3", "dayanak", "weak", "sentence", 2, 255, "lemalar/3/c003"),        # üçüncü cümlede: zayıf
        ("lemalar/4", "izah", "strong", "sentence", 112, 1, "lemalar/4/c001"),         # müellifin "Yani"si
        ("lemalar/7", "isaret", "weak", "sentence", 112, 1, "lemalar/7/c001"),         # sûre adı olarak âyet
        ("lemalar/8", "isaret", "weak", "sentence", 2, 255, "lemalar/8/c001"),         # "işâret" âyetten uzak
        ("sozler/33", "acilis", "strong", "section", 17, 44, "sozler/33/c001"),        # Pencere bu âyetle açılır
        ("sualar/1", "risale", "strong", "section", 2, 255, "sualar/1/c001"),          # Birinci Şuâ
    ]          # Fihrist, risale adındaki "işârât" (lemalar/6), mektubun açılış ibaresi (mektubat/1): ilişki yok


def test_tools_show_links(db_path):
    lib = Library(db_path)
    links = lib.find_ayah("2", 255)["links"]
    assert [l["strength"] for l in links] == ["strong"] * 3 + ["weak"] * 2                # güçlüler önce
    assert links[0]["evidence"]["ref"] == "lemalar › lemalar/1 › 1. cümle"
    assert lib.ayahs("2", 255)["ayahs"][0]["linked_in_works"] == {"strong": 3, "weak": 2}
    heading = lib.read_section("lemalar/1")["items"][0]
    assert heading["linked_verses"] == [{"verse": "Bakara Sûresi, 2:255", "kind": "isaret",
                                         "evidence": "lemalar/1/c001"}]
    lib.close()


def test_real_links_keep_the_users_review():
    """Kullanıcının örneklem kararları (tests/golden/ayah_links_review.json) gerçek veritabanında tutar."""
    from risale_mcp.ayah_links import load_reviews, review_status
    from risale_mcp.db import connect
    from risale_mcp.paths import DB_PATH
    if not DB_PATH.exists():
        pytest.skip("risale.db yok")
    conn = connect()
    wrong = [r for r in load_reviews() if (review_status(conn, r) == "strong") != (r["expect"] == "strong")]
    assert wrong == []
