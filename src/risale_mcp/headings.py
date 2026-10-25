"""Başlıkların anlamı: tür ("Hakikat", "Söz"), numara ve düğüm kimliğindeki yerel ad.

    "Dokuzuncu Hakikat"                   -> Hakikat 9   -> hakikat-09
    "Zeylin İkinci Parçası"               -> Parça 2     -> parca-02
    "Ondördüncü Lem'a'nın İkinci Makamı"  -> Makam 2     -> makam-02
    "Hâtime"                              -> Hâtime      -> hatime
    "On iki Hakikat"                      -> (tür yok)   -> on-iki-hakikat
    "297. Emirdağı'nın manidar bir hatırası" -> 297      -> 297
"""

import re
from dataclasses import dataclass

from risale_mcp.normalize import fold, parse_ordinal, slugify

# Bölüm türlerinin kanonik adları. Ekli biçimler ("Makamı", "Hatvede") bunlara indirgenir.
KNOWN_TYPES = {fold(t): t for t in [
    "Söz", "Mektub", "Lem'a", "Şuâ", "Makam", "Mebhas", "Maksad", "Mevkıf", "Mukaddime",
    "Mukaddeme", "Hâtime", "Zeyl", "Esas", "Hakikat", "Nükte", "Sır", "Sûret", "İşaret", "Remiz",
    "Nokta", "Mes'ele", "Pencere", "Bürhan", "Levha", "Kâr", "Hasaret", "Asıl", "Vecih",
    "Temsil", "Sual", "Meyve", "Medar", "Menba'", "Basamak", "Şu'le", "Ziya", "Işık", "Misal",
    "Fıkra", "Hüccet", "Dal", "Hatve", "Cilve", "Şavk", "Sebeb", "Kısım", "Cüz'", "Nur",
    "Hikmet", "Müşkil", "Reşha", "Parça", "Mertebe", "Mukayese", "Ders", "Kelime", "Cihet",
    "Hikâye", "Hâşiye", "Delil", "Merhem", "Nümune", "Bab", "Makale", "Tenbih", "İhtar",
    "Lâhika", "Fasıl", "Bahis", "Âyet", "Nota", "Devâ", "Cinayet", "Ricâ", "Muhal", "Madde",
    "Emare", "Telvih", "Meslek", "Cümle", "Me'haz", "Desise", "Katre", "Menzil", "İkaz", "Alâmet",
    "Şehadet", "Kelâm", "Maden", "Düstur", "Nevi", "Hadise", "Şube", "Umde", "Varta", "Şık",
    "Keramet", "Hatıra", "Vehim", "Cinayet",
]}
# Ek alınca ses düşen türler: "Remzi", "Sırrı", "Kısmı", "Vechi", "Aslı".
KNOWN_TYPES |= {fold(stem): KNOWN_TYPES[fold(t)] for stem, t in [
    ("Remz", "Remiz"), ("Sırr", "Sır"), ("Kısm", "Kısım"), ("Vech", "Vecih"), ("Asl", "Asıl"),
    ("Mektûp", "Mektub"), ("Bahs", "Bahis"), ("Fasl", "Fasıl"), ("Cüz", "Cüz'"),
]}
# Numarasız da olsa yapısal sayılan türler: "Hâtime", "Onuncu Söz'ün Zeyli".
UNNUMBERED_TYPES = {fold(t) for t in ["Mukaddime", "Mukaddeme", "Hâtime", "Zeyl", "Hâşiye"]}
# Ekli biçimler: "Makamı", "Hatvede", "Nüktesinin", "Mektûbun".
SUFFIXES = ["iniz", "ınız", "unuz", "ünüz", "sinin", "sının", "sunun", "sünün", "sidir", "sıdır", "sudur", "südür",
            "nın", "nin", "nun", "nün", "dir", "dır", "dur", "dür", "sı", "si", "su", "sü",
            "ın", "in", "un", "ün", "ye", "ya", "de", "da", "ı", "i", "u", "ü"]
# Kitabın ana birimi kitap düzeyinde yalnızca numarasıyla anılır: sozler/10, mektubat/29.
MAIN_UNITS = {fold(t) for t in ["Söz", "Mektub", "Lem'a", "Şuâ"]}

_LEADING_NUMBER = re.compile(r"^(\d+)\.\s+")
_HYPHENS = re.compile(r"[‐‑‒–-]")


@dataclass(frozen=True)
class HeadingInfo:
    type: str | None = None
    number: int | None = None


def _words(text: str) -> list[str]:
    return re.findall(r"[^\W\d_]+(?:['’‘ʼ][^\W\d_]+)*", _HYPHENS.sub("-", text).replace("-", " "))


def canonical_type(word: str) -> str | None:
    """'Makamı' -> 'Makam', 'Esâs' -> 'Esas'; bilinmeyen kelimede None."""
    folded = fold(word)
    if folded in KNOWN_TYPES:
        return KNOWN_TYPES[folded]
    for suffix in SUFFIXES:
        if folded.endswith(suffix) and folded[: -len(suffix)] in KNOWN_TYPES:
            return KNOWN_TYPES[folded[: -len(suffix)]]
    return None


def _ordinal_before(words: list[str], end: int) -> int | None:
    """`end` konumundan önce biten sıra sayısı: 'Sekizinci' ya da bölünmüş 'Yirmi Sekizinci'."""
    if end >= 2 and (n := parse_ordinal(words[end - 2] + words[end - 1])) is not None:
        return n
    return parse_ordinal(words[end - 1]) if end >= 1 else None


def _ordinal_at_start(words: list[str]) -> tuple[int | None, int]:
    """Baştaki sıra sayısı ve kaç kelime tuttuğu: 'Birinci' (1) ya da 'Yirmi Sekizinci' (2)."""
    if len(words) >= 2 and (n := parse_ordinal(words[0] + words[1])) is not None:
        return n, 2
    n = parse_ordinal(words[0]) if words else None
    return n, (1 if n is not None else 0)


def _head(words: list[str]) -> tuple[HeadingInfo, int] | None:
    """'Birinci Kelime…' kalıbı: (bilgi, sıra sayısı ve türün tuttuğu kelime sayısı)."""
    number, used = _ordinal_at_start(words)
    if number is None or len(words) <= used:
        return None
    type_ = canonical_type(words[used])
    return (HeadingInfo(type_, number), used + 1) if type_ else None


def _rest_after(title: str, word: str) -> str:
    i = title.find(word)
    return title[i + len(word):].strip() if i >= 0 else ""


def parse_heading(title: str) -> HeadingInfo:
    """Blok başlığının türü ve numarası.
    - Sondan: 'Zeylin İkinci Parçası', 'Ondördüncü Lem'a'nın İkinci Makamı', 'Yirmi Sekizinci Lem'a'.
    - Baştan, yalnızca başlık orada bitiyor ya da ':', '(', '—' ile sürüyorsa: 'Birinci Kelime: El-Emel'.
      'Yirmi Beşinci Söz, Kur'ân'ı çok güzel tarif eder' gibi cümle başlıkları türsüz kalır.
    İkisi de uymazsa tür yoktur."""
    leading = _LEADING_NUMBER.match(title)
    if leading:
        return HeadingInfo(number=int(leading[1]))
    words = _words(title)
    if len(words) >= 2 and (type_ := canonical_type(words[-1])):
        number = _ordinal_before(words, len(words) - 1)
        if number is not None:
            return HeadingInfo(type_, number)
    head = _head(words)
    if head and (len(words) == head[1] or _rest_after(title, words[head[1] - 1])[:1] in (":", "(", "—", "–")):
        return head[0]
    if words and (type_ := canonical_type(words[-1])) and fold(type_) in UNNUMBERED_TYPES:
        return HeadingInfo(type_)
    return HeadingInfo()


def parse_inline_label(label: str) -> HeadingInfo | None:
    """Paragraf başındaki biçimli etiket düğüm açar mı? Yalnızca numaralı birimler açar:
    'Birinci Esas:', 'Üçüncü Mes'ele Ki:', 'Birinci Hatvede:', 'Birinci kısım'.
    Açmayanlar: 'Birincisi:' (sayı sıfatı), 'Onuncu Söz'den' (kaynak etiketi),
    'İkinci kısmın…' (ilgi hâli: etiket değil, cümlenin başı)."""
    label = label.strip()
    words = _words(label)
    head = _head(words)
    if head is None:
        return None
    info, used = head
    extra = words[used:]
    bare = not extra or (len(extra) == 1 and fold(extra[0]) == "ki")
    if not (bare or label.endswith(":") and len(extra) <= 2) or _is_genitive(words[used - 1]):
        return None
    return info


def _is_genitive(word: str) -> bool:
    folded = fold(word)
    return folded not in KNOWN_TYPES and folded.endswith(("ın", "in", "un", "ün"))


def local_id(info: HeadingInfo, title: str, top_level: bool) -> str:
    """Düğümün, ebeveyninin kimliğine eklenen yerel adı."""
    if info.type is None and info.number is not None:
        return str(info.number)
    if info.type and info.number is not None:
        if top_level and fold(info.type) in MAIN_UNITS:
            return str(info.number)
        return f"{slugify(info.type)}-{info.number:02d}"
    if info.type:
        return slugify(info.type)
    return slugify(" ".join(title.split()[:5])) or "bolum"


def clean_label(label: str) -> str:
    """'Birinci Esâs:' -> 'Birinci Esâs'."""
    return label.strip().rstrip(":").strip()
