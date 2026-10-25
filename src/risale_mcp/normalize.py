"""Türkçe metin yardımcıları: büyük/küçük harf, sıra sayıları, slug ve arama normalizasyonu."""

import re
import unicodedata

_UNITS = ["", "birinci", "ikinci", "üçüncü", "dördüncü", "beşinci",
          "altıncı", "yedinci", "sekizinci", "dokuzuncu"]
_TENS_PREFIX = {1: "on", 2: "yirmi", 3: "otuz", 4: "kırk"}
_TENS_ORDINAL = {1: "onuncu", 2: "yirminci", 3: "otuzuncu", 4: "kırkıncı"}

_ORDINAL_VALUES: dict[str, int] = {}
for _n in range(1, 50):
    _t, _u = divmod(_n, 10)
    if _t == 0:
        _word = _UNITS[_u]
    elif _u == 0:
        _word = _TENS_ORDINAL[_t]
    else:
        _word = _TENS_PREFIX[_t] + _UNITS[_u]
    _ORDINAL_VALUES[_word] = _n


def tr_lower(text: str) -> str:
    return text.replace("I", "ı").replace("İ", "i").lower()


def tr_upper(text: str) -> str:
    return text.replace("i", "İ").replace("ı", "I").upper()


def tr_capitalize(word: str) -> str:
    return tr_upper(word[:1]) + tr_lower(word[1:]) if word else word


def tr_title(text: str) -> str:
    """Yalnızca TAMAMI BÜYÜK harfli kelimeleri baş harfi büyük yapar; 've' gibi bağlaçlar küçük kalır."""
    out = []
    for word in text.split(" "):
        letters = [c for c in word if c.isalpha()]
        if letters and all(c.isupper() for c in letters):
            lowered = tr_lower(word)
            word = lowered if lowered in {"ve", "ile", "ki"} else tr_capitalize(word)
        out.append(word)
    return " ".join(out)


def ordinal_word(n: int) -> str:
    """5 -> 'Beşinci', 14 -> 'Ondördüncü'."""
    for word, value in _ORDINAL_VALUES.items():
        if value == n:
            return tr_capitalize(word)
    raise ValueError(f"Desteklenmeyen sıra sayısı: {n}")


def parse_ordinal(word: str) -> int | None:
    """'BEŞİNCİ' -> 5, 'Onbesinci' -> 15 (süslü fontta ş -> s düşmesine toleranslı)."""
    w = tr_lower(word.strip(" '’"))
    if w in _ORDINAL_VALUES:
        return _ORDINAL_VALUES[w]
    w = w.replace("besinci", "beşinci")
    return _ORDINAL_VALUES.get(w)


_SLUG_MAP = str.maketrans("çğıöşüâîû", "cgiosuaiu")


def slugify(text: str) -> str:
    s = tr_lower(text).translate(_SLUG_MAP)
    s = re.sub(r"['’‘ʼ`]", "", s)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def fold(text: str) -> str:
    """Arama/karşılaştırma için: Türkçe küçük harf, şapkasız, kesme işaretsiz, tek boşluk."""
    s = tr_lower(text)
    # Yalnızca şapka (U+0302) kaldırılır; ç, ğ, ö, ş, ü korunur.
    s = unicodedata.normalize("NFC", unicodedata.normalize("NFD", s).replace("̂", ""))
    s = re.sub(r"['’‘ʼ`]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def match_words(text: str) -> list[str]:
    """Baskılar arası eşleme için kelimeler: Türkçe küçük harf, bütün işaretler (şapka, uzatma,
    Türkçe harflerin çengeli, Arapça hareke) ve noktalama atılmış.
    'Risâle-i Nûr’un' ve 'Risale-i Nur’un' aynı kelimelere iner: ['risale', 'i', 'nurun']."""
    s = unicodedata.normalize("NFD", tr_lower(text))
    s = "".join(ch for ch in s if not unicodedata.category(ch).startswith("M"))
    s = re.sub(r"['’‘ʼ`]", "", s).translate(_ARABIC_LETTER_VARIANTS)
    return re.findall(r"\w+", s)


# Baskılar Arapça harfleri farklı kodlayabilir: Farsça ye/kef, elif maksure, elif çeşitleri.
_ARABIC_LETTER_VARIANTS = str.maketrans({"ی": "ي", "ى": "ي", "ک": "ك", "ٱ": "ا", "أ": "ا", "إ": "ا", "آ": "ا"})
