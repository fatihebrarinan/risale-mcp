"""Künyenin bölgesinde okuma (`hadis_bolge.py`): aday sıralaması, gösterilen pencere, kontroller."""

from risale_mcp.hadis_adaylar import stems
from risale_mcp.hadis_bolge import rank, window


def test_the_closest_hadith_of_the_region_comes_first():
    region = [{"id": "x/1", "matn": "كان فزع بالمدينة فركب رسول الله فرسا لأبي طلحة فقال وإن وجدناه لبحرا", "text": ""},
              {"id": "x/2", "matn": "إذا قمت في صلاتك فصل صلاة مودع", "text": ""}]
    idf = {w: 1.0 for h in region for w in stems(h["matn"])}
    ranked = rank("وَجَدْتُ فَرَسَكَ بَحْرًا", list(reversed(region)), idf)
    assert ranked[0][1]["id"] == "x/1" and ranked[0][0] > ranked[1][0]


def test_a_short_report_is_shown_whole_and_a_long_one_around_the_match():
    assert window("قال رسول الله الحكمة ضالة المؤمن", 3, 5) == "قال رسول الله الحكمة ضالة المؤمن"
    long = " ".join(["كلمة"] * 200 + ["الحكمة", "ضالة", "المؤمن"] + ["كلمة"] * 200)
    shown = window(long, 200, 202)
    assert "الحكمة ضالة المؤمن" in shown and len(shown.split()) < 80
