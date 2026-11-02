from risale_mcp.hadis_turkce import form, quote


def test_quoted_hadith():
    assert form("Hadîste vardır ki; “Hastaların duâsını alınız; onların duâsı makbûldür.”") == "quoted_hadith"
    assert form("“Sadaka belâyı def'eder.” meâlindeki hadîs-i sahîhin hükmüyle, böyledir.") == "quoted_hadith"


def test_hadise_is_not_hadith():
    assert form("Bu hâdiseye dair “çok uzun bir söz burada duruyor” dediler.") is None
    assert form("Bu hadisat içinde “çok uzun bir söz burada duruyor” dediler.") is None


def test_quoted_prophet_is_the_speaker():
    assert form("Resûl‑i Ekrem Aleyhissalâtü Vesselâm dedi: “Bir parça su bulunuz.”") == "quoted_prophet"
    assert form("Biri geldi, Resûl-i Ekrem Aleyhissalâtü Vesselâm’a dedi ki: “Meşhûr münâfık öldü.”") is None


def test_reported_needs_content():
    assert form("Birincisi: Bir rivâyette var ki, o keçinin kolu haber verdi.") == "reported"
    assert form("Ye'cüc hâdisâtının icmâli Kur'ân’da olduğu gibi, rivâyette bir kısım tafsilât var.") is None


def test_quote_takes_the_longest():
    assert quote("“kısa” ve “daha uzun bir söz” dedi.") == "daha uzun bir söz"
    assert quote("tırnaksız") is None
