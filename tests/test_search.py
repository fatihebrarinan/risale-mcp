

def test_an_arabic_word_is_searched_with_its_attached_forms():
    """MVP M4: dizinde "والكتاب" tek kelimedir; "الكتاب" ve "كتاب" arayan onu da bulur (sorgu tarafında açılır)."""
    from risale_mcp.search import arabic_forms, to_fts
    forms = arabic_forms("الكتاب")
    assert forms[0] == "الكتاب" and {"كتاب", "والكتاب", "بالكتاب", "للكتاب", "فالكتاب"} <= set(forms)
    assert '"والكتاب"' in to_fts("الكتاب") and '"والكتاب"' not in to_fts('"الكتاب"')    # tırnaklı ifade açılmaz


def test_turkish_words_become_word_starts_only_when_asked():
    from risale_mcp.search import to_fts
    assert to_fts("beyzavi") == '("beyzavi")'
    assert to_fts("beyzavi", prefix_all=True) == '("beyzavi"*)'
    assert to_fts('"beyzavi"', prefix_all=True) == '("beyzavi")'


def test_hadith_word_folds_ibn_into_bin():
    from risale_mcp.search import hadith_word, to_fts
    assert [hadith_word(w) for w in ("ابن", "وابن", "فابن", "لابن", "ابنة", "بن")] == ["بن", "وبن", "فبن", "لابن", "ابنة", "بن"]
    assert '"بن مريم"' in to_fts('"ابن مريم"', canon=hadith_word)
    assert '"ابن مريم"' in to_fts('"ابن مريم"')            # Risale'nin araması değişmez
    assert '"لبن"' not in to_fts("ابن", canon=hadith_word)  # süt değil


def test_joined_forms_b7():
    """B7: tırnaklı ifade bitişik yazılışıyla da aranır; NEAR içinde OR grubu yok."""
    from risale_mcp.search import joined_forms, to_fts
    assert joined_forms("âhir zaman") == ["ahir zaman", "ahirzaman"]
    assert joined_forms("hiç bir şey") == ["hic bir sey", "hicbir sey", "hic birsey", "hicbirsey"]
    assert joined_forms("ehl-i iman") == ["ehl i iman"]
    assert to_fts('"âhir zaman"') == '(("ahir zaman" OR "ahirzaman"))'
    assert "OR" not in to_fts("NEAR(الكتاب لا, 5)")
    assert to_fts('NEAR("âhir zaman" deccal, 10)') == \
        '((NEAR("ahir zaman" "deccal", 10) OR NEAR("ahirzaman" "deccal", 10)))'
