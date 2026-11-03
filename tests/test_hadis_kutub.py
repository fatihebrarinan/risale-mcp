"""Hadis kitapları (`hadis_kutub.py`): OpenITI JK baskılarının başlıkları, numaraları ve künyenin bölgesi.

Örnekler ham dosyaların gerçek satırlarındandır, kısaltılmıştır.
"""

from risale_mcp.hadis_kutub import Index, check, numbers_of, parse, split, split_refs, to_json

HEADER = "######OpenITI#\n#META#Header#End#\n"


def test_tagged_headings_and_tirmidhi_numbers():
    raw = HEADER + ("### | ( 1 كتاب أبواب الطهارة )\n### || ( 1 باب ما جاء لا تقبل صلاة بغير طهور )\n### ||| 1\n"
                    "# حدثنا قتيبة بن سعيد حدثنا أبو عوانة * لا تقبل صلاة بغير طهور PageV01P005\n"
                    "~~قال أبو عيسى هذا الحديث\n### || ( 2 باب ما جاء في فضل الطهور )\n### ||| 2\n# حدثنا إسحاق\n")
    nodes, hadiths, _ = parse("tirmidhi", raw)
    assert [(n.level, n.number) for n in nodes] == [("kitab", 1), ("bab", 1), ("bab", 2)]
    assert hadiths[0].id == "tirmidhi/1" and hadiths[0].node_id == "tirmidhi/k01/b001"
    assert "PageV" not in hadiths[0].paragraphs[0] and hadiths[0].paragraphs[0].endswith("قال أبو عيسى هذا الحديث")


def test_pipe_headings_repeated_numbers_and_continuations():
    """Müslim: "# | 1 ( … )" başlıklar; numarasız paragraf ve tarik önceki hadisin; aynı numara "-2" eki alır."""
    raw = HEADER + ("# | 1 ( 1 كتاب الإيمان )\n# | 1 ( 1 باب بيان الإيمان )\n# 8 حدثني أبو خيثمة * بينما نحن\n"
                    "# | 1 ( قال فأتم له رسول الله )\n# 8 وحدثنا محمد بن عبيد * مثله\n")
    _, hadiths, _ = parse("muslim", raw)
    assert [h.id for h in hadiths] == ["muslim/8", "muslim/8-2"]
    assert hadiths[0].paragraphs[-1] == "( قال فأتم له رسول الله )"


def test_concatenated_number_takes_the_following_one():
    raw = HEADER + "# | 1 ( 1 كتاب الزهد )\n# 291429132913 2913 وحدثني زهير بن حرب\n"
    _, hadiths, stats = parse("muslim", raw)
    assert hadiths[0].number == 2913 and stats["birlesik_numara"] == 1


def test_gap_count_does_not_build_the_whole_range():
    """Yanlış okunmuş büyük numara (291429132913) belleği doldurmuştu (2026-11-03): boşluk ayrı raporlanır."""
    _, hadiths, _ = parse("muslim", HEADER + "# 1 حدثنا\n# 3 حدثنا\n# 291429132913 حدثنا\n")
    result = check(hadiths)
    assert result["eksik_sayisi"] == 1 and result["buyuk_bosluk"] == [(3, 291429132913)]


def test_abu_dawud_first_kitab_and_muwatta_references():
    nodes, _, _ = parse("abudawud", HEADER + "# 1 كتاب الطهارة\n# | 1 ( 1 باب التخلي عند قضاء الحاجة )\n# 1 حدثنا\n")
    assert [(n.level, n.title) for n in nodes] == [("kitab", "كتاب الطهارة"), ("bab", "باب التخلي عند قضاء الحاجة")]
    assert split_refs("قبل أن تظهر س 1 - 16 ت 8 - 10") == ("قبل أن تظهر", "س 1 - 16 ت 8 - 10")
    assert split("حدثنا مالك عن نافع * أن عمر كتب") == ("حدثنا مالك عن نافع", "أن عمر كتب")


def test_citation_numbers_and_region():
    assert numbers_of("15,35") == {15, 35} and numbers_of("3-5") == {3, 4, 5}
    raw = HEADER + ("### | ( 10 كتاب الأذان )\n### || ( 147 باب )\n# 830 حدثنا * أ\n### || ( 148 باب التشهد )\n"
                    "# 831 حدثنا * التحيات لله\n### || ( 160 باب )\n# 850 حدثنا * ب\n")
    nodes, hadiths, _ = parse("nasai", raw)
    data = to_json("nasai", nodes, hadiths)
    data["outline"][0]["api_sections"] = [10]
    index = Index({"nasai": data})
    assert [h["id"] for h in index.cited("nasai", 10, "148")] == ["nasai/831"]      # Nesâî: bâb tam
    assert index.cited("nasai", 11, "148") == []
