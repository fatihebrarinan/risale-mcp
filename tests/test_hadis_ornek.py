import json

import pytest

pytest.importorskip("openpyxl")

from risale_mcp.hadis_ornek import GOLDEN, compare, read_book, strata, workbook


def row(id_, relation="verbatim", speaker="prophet", denied=False, **kw):
    answer = {"relation": relation, "speaker": speaker, "denied": denied}
    return {"id": id_, "decoy": False, "set": "found", "agree": True, "answers": [answer, answer], **kw}


def test_strata_keep_a_pair_once_and_hide_decoys_from_the_rest():
    rows = [row("a", "by_meaning", denied=True), row("b", "by_meaning"), row("c", "related", "unclear"),
            row("d", speaker="other"), row("e"), row("f", "different", decoy=True)]
    groups = strata(rows)
    assert [r["id"] for r in groups["denied"]] == ["a"]
    assert [r["id"] for r in groups["by_meaning"]] == ["b"]
    assert [r["id"] for r in groups["rejected"]] == ["c"]
    assert [r["id"] for r in groups["other_speaker"]] == ["d"]
    assert [r["id"] for r in groups["verbatim"]] == ["e"]
    assert [r["id"] for r in groups["decoy"]] == ["f"]


def item(no, stratum="verbatim", report="r:1", model=("verbatim",)):
    return {"no": no, "priority": 1, "stratum": stratum, "key": "k", "part": "سيد القوم", "report": report, "ref": "Sözler › X",
            "meal": None, "source": None, "shown": "سيد القوم خادمهم", "chain": 3, "model": list(model)}


def test_book_hides_the_key_and_reads_decisions_back(tmp_path):
    book = workbook([item(1, "decoy"), item(2)], {"r:1": ("Kitap", "metin")})
    sheet = book["Örneklem"]
    assert not {c.value for row_ in sheet.iter_rows() for c in row_} & {"decoy", "verbatim", "stratum"}
    sheet["K2"], sheet["L2"], sheet["N2"] = "Mânen nakil", "Peygamber", "not"
    path = tmp_path / "kitap.xlsx"
    book.save(path)
    assert read_book(path) == [{"no": 1, "report": "r:1", "relation": "Mânen nakil", "speaker": "Peygamber", "grade": None, "note": "not"}]


def test_compare_counts_and_refuses_another_sample():
    decisions = [{"no": 1, "report": "r:1", "relation": "Aynı lafız", "speaker": None, "grade": None, "note": None}]
    locked, lines = compare([item(1)], decisions)
    assert locked[0]["stratum"] == "verbatim"
    assert "| verbatim | 1 | 1 | 1 |" in lines
    with pytest.raises(ValueError):
        compare([item(1, report="r:2")], decisions)


def test_locked_decisions_are_well_formed():
    if not GOLDEN.exists():
        pytest.skip("hadisçi kararları henüz yok")
    decisions = json.loads(GOLDEN.read_text("utf-8"))["decisions"]
    assert all(d["report"] and d["stratum"] for d in decisions)
