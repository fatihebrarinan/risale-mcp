from risale_mcp.hadis_rivayet import audit, book_kind, plain, queues, speaker, verdict


def row(**kw):
    return {"verdict": None, "book_kind": "hadis", "speaker": "prophet", "chain": 3, **kw}


def test_book_kind():
    assert book_kind("Sahîh-i Buhârî") == "hadis"
    assert book_kind("مسند أحمد بن حنبل") == "hadis"
    assert book_kind("الأسرار المرفوعة في الأخبار الموضوعة") == "mevzu"
    assert book_kind("جامع البيان عن تأويل آي القرآن") == "tefsir"
    assert book_kind("الأغاني") == "diger"


def test_verdict_ignores_the_words_it_contains():
    assert verdict("وهو كلام صحيح ليس بحديث") == "denied"
    assert verdict("قال ابن حجر لا اصل له") == "denied"
    assert verdict("ليس بموضوع") is None
    assert verdict("رواه البخاري في الصحيح") is None         # "واه"
    assert verdict("فان الصدق طمانينه وان الكذب ريبه") is None
    assert verdict("هذا ضعيف") == "weakened"
    assert verdict("هو من كلام السري السقطي") == "other_saying"


def test_speaker():
    assert speaker(plain("قال رسول الله صلى الله عليه وسلم :")) == "prophet"
    assert speaker(plain("قلت يا رسول الله")) == "addressed"
    assert speaker(plain("قال النبي ثم قال ابن عباس")) == "other"
    assert speaker("حدثنا فلان") == "none"
    assert speaker("") == "start"


def test_audit_reads_around_the_match():
    found = audit("الضرورات تبيح المحظورات", "حديث الضرورات تبيح المحظورات ليس بحديث وهو كلام صحيح", "الأسرار المرفوعة", 0)
    assert (found.book_kind, found.chain, found.speaker, found.verdict) == ("mevzu", 0, "none", "denied")
    before = audit("الضرورات تبيح المحظورات", "ليس بحديث عندهم الضرورات تبيح المحظورات", "مسند", 2)
    assert before.verdict is None


def test_queue_needs_every_report():
    assert queues([row(), row(book_kind="mevzu", speaker="none", chain=0)]) == []
    assert queues([row(book_kind="mevzu", speaker="none", chain=0)]) == ["only_caution", "no_prophet", "no_chain"]
    assert queues([row(verdict="denied"), row()]) == ["denied"]
