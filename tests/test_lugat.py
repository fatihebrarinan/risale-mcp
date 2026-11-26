"""Lügat (A4): ham verinin ayrıştırılması, kelimenin maddesini bulma kuralları, okuma platformuyla aynı bölme."""

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

from risale_mcp.lugat import Lexicon, form, key, parse, surface, tokens_of
from risale_mcp.normalize import search_words

ROOT = Path(__file__).resolve().parents[1]

RAW = {
    "a.txt": "âb-ı hayat=Hayat suyu.\nakıl=(akl) anlama gücü\nâkil=Yiyen.\nalem=Dünya.\nalem=Dünya.\n",
    "a_f.txt": "âb-ı hayat=âb-ul hayat:0|akıl=akl:0|âkil=:0|alem=:0|",
    "b.txt": "bi'r=Kuyu.\nbey'=Satış.\n",
    "b_f.txt": "bi'r=:0|bey'=:0|",
    "d.txt": "dâhî=Üstün zekâlı.\n",
    "d_f.txt": "dâhî=:0|",
    "e.txt": "eşk=Gözyaşı.\nesrar=Sırlar.\neşrar=Şerliler.\n",
    "e_f.txt": "eşk=:0|esrar=:0|eşrar=:0|",
    "h.txt": "haşir=Yeniden diriliş.\nhaşrî=Haşirle ilgili.\nhikmet-i ilahî=Allah'ın hikmeti.\n",
    "h_f.txt": "haşir=haşr:0|haşrî=:0|hikmet-i ilahî=hikmet-i ilahiye:0|",
    "i.txt": "ihtiyaç=Gereklilik.\ni'tikad=İnanç.\nilim=Bilgi.\n",
    "i_f.txt": "ihtiyaç=:0|i'tikad=itikad:0|ilim=ilm:0|",
    "k.txt": "kâinat=Evren.\nkalb=Yürek.\nkalbî=Kalbe ait.\nkur'an=Kitap.\nkürt=Bir millet.\n",
    "k_f.txt": "kâinat=kainat:0|kalb=kalp:0|kalbî=:0|kur'an=:0|kürt=:0|",
    "m.txt": "mana=1. anlam\n2. iç yüz\n",
    "m_f.txt": "mana=mâna:0|",
    "n.txt": "nur=Işık.\n",
    "n_f.txt": "nur=:0|",
    "s.txt": "sabır=Dayanma.\nsâbir=Sabreden.\nsır=Gizli.\nas=Selam olsun.\n",
    "s_f.txt": "sabır=sabr:0|sâbir=:0|sır=sırr:0|as=:1|",
}


@pytest.fixture(scope="module")
def lex() -> Lexicon:
    entries, _ = parse(RAW)
    return Lexicon(entries)


def words(lex: Lexicon, text: str) -> list[str]:
    return [m.entry["word"] for m in lex.lookup(text)]


def test_parse_continuations_duplicates_variants():
    entries, report = parse(RAW)
    by = {e["word"]: e for e in entries}
    assert by["mana"]["meaning"] == "1. anlam\n2. iç yüz"            # numaralı satır öncekinin devamı
    assert by["alem"]["meaning"] == "Dünya."                         # aynısı iki kez: bir kez
    assert report["duplicates"] == ["alem"]
    assert by["âb-ı hayat"]["variants"] == ["âb-ul hayat"]
    assert by["as"]["exact"] is True


def test_exact_variant_and_phrases(lex):
    assert words(lex, "kâinat") == ["kâinat"]
    assert [m.how for m in lex.lookup("akl")] == ["variant"]
    assert words(lex, "Âb-ı hayat") == ["âb-ı hayat"]
    assert words(lex, "hikmet-i İlâhiye") == ["hikmet-i ilahî"]


def test_suffixes(lex):
    assert words(lex, "kâinatın") == ["kâinat"]
    assert words(lex, "nurun") == ["nur"]
    assert words(lex, "âb-ı hayatı") == ["âb-ı hayat"]
    assert words(lex, "hikmet-i İlâhiyenin") == ["hikmet-i ilahî"]
    assert words(lex, "kalbi") == ["kalbî", "kalb"]                  # ikisi de okunabilir
    assert words(lex, "ihtiyacı") == ["ihtiyaç"]                     # yumuşayan son harf
    assert words(lex, "sabrı")[0] == "sabır"                         # düşen ünlü geri konur (ı = i: sâbir de aday)
    assert words(lex, "ilmi") == ["ilim"]
    assert words(lex, "haşrin") == ["haşir"]                         # yalnız "n" eki atılmaz: haşrî değil
    assert words(lex, "esrarımı") == ["esrar"]                       # eşrar değil


def test_apostrophes(lex):
    assert words(lex, "Kur’ân’ın") == ["kur'an"]                     # kesmeden sonrası ek
    assert words(lex, "i’tikadın") == ["i'tikad"]
    assert words(lex, "bir") == []                                   # bi'r'in kesmesi metinde yok
    assert words(lex, "beyle") == []                                 # bey'
    assert words(lex, "bi’r") == ["bi'r"]


def test_no_false_matches(lex):
    assert words(lex, "dahi") == []                                  # sesteş Türkçe kelime (STOP)
    assert words(lex, "kurtuluşu") == []                             # atılan ek ş taşımaz
    assert words(lex, "eskide") == []                                # eşk: harfi tutmuyor
    assert words(lex, "kürt") == ["kürt"]
    assert words(lex, "aslı") == []                                  # "as" yalnız kendisi (bayrak 1)
    assert words(lex, "as") == ["as"]


def test_spans_and_surface(lex):
    text = "Âb-ı hayatı ve kâinatın sırrı, Kur’ân’ın nuru."
    found = {(i, n): [m.entry["word"] for m in f] for i, n, f in lex.spans(text)}
    toks = [w for w, _ in tokens_of(text)]
    assert toks == search_words(text)
    assert found[(0, 3)] == ["âb-ı hayat"]
    assert surface(text, 0, 3) == "Âb-ı hayatı"
    assert found[(toks.index("kainatin"), 1)] == ["kâinat"]
    assert found[(toks.index("kuranin"), 1)] == ["kur'an"]


def test_form_aligns_with_key():
    for text in ["Kur’ân’ın", "Âb-ı hayat", "i'tikad", "İnşâallah", "ŞEFKAT", "sırr-ı ihlâs"]:
        f = form(text)
        assert f is not None and len(f.letters) == len(key(text)), text


# --------------------------------------------------------------- okuma platformu (oku-app.html) aynı böler

SAMPLES = ["Âb-ı hayatı ve kâinatın sırrı, Kur’ân’ın nuru.", "İnşâallah ŞEFKAT-İ İLÂHİYE’NİN", "i'tikad-ı bâtıl",
           "ilmî ve aklî", "Hâlık-ı Rahîm’in ism-i Vedûd’u", "أَحْسَنُ الْخَالِق۪ينَ ve el-Hakîm"]


@pytest.mark.skipif(shutil.which("node") is None, reason="node yok")
def test_platform_tokenizer_matches_python(tmp_path):
    app = (ROOT / "scripts" / "oku-app.html").read_text(encoding="utf-8")
    m = re.search(r"const lugatWords = (t => .*?\);)\n", app, re.S)
    t = re.search(r"const re = (/\[.*?\]\+/gu);", app)
    assert m and t, "lugatWords ya da kelime düzeni bulunamadı"
    script = (f"const lugatWords = {m[1]}\nconst re = {t[1]};\nconst out = [];\n"
              f"for (const s of {json.dumps(SAMPLES, ensure_ascii=False)}) {{ const w = []; let x;\n"
              "  while ((x = re.exec(s))) w.push(...lugatWords(x[0])); re.lastIndex = 0; out.push(w); }\n"
              "console.log(JSON.stringify(out));\n")
    path = tmp_path / "t.js"
    path.write_text(script, encoding="utf-8")
    got = json.loads(subprocess.run(["node", str(path)], capture_output=True, text=True, check=True).stdout)
    assert got == [search_words(s) for s in SAMPLES]


def test_vowel_then_i_or_dotless_i_tells_homographs_apart():
    # S13.16 (b): sâika (سائقه, sevk eden) yıldırım (saîka, sâıka: صاعقه) değildir; vâiz (vaaz eden) vaız değildir.
    # Maddeler gerçek lügattaki yazılışlarıyla.
    lex = Lexicon([
        {"id": 1, "word": "saîka", "meaning": "Yıldırım.", "variants": ["saıka", "sâıka"]},
        {"id": 2, "word": "saik", "meaning": "Sevkeden.", "variants": ["sâik", "sâika", "saika"]},
        {"id": 3, "word": "vaız", "meaning": "Öğüt."},
        {"id": 4, "word": "vaiz", "meaning": "Vaaz eden."},
        {"id": 5, "word": "hikmet-i ilahî", "meaning": "Allah'ın hikmeti.", "variants": ["hikmet-i ilâhiye"]},
    ])
    assert words(lex, "sâika") == ["saik"]
    assert words(lex, "sâikasıyla") == ["saik"]
    assert "saîka" in words(lex, "sâıka") and "saik" not in words(lex, "sâıka")
    assert words(lex, "vâiz") == ["vaiz"]
    assert words(lex, "hikmet-i İlâhiye") == ["hikmet-i ilahî"]       # şapkanın yeri ayırmaz
