"""Aşama 9: Kur'ân-ı Kerîm katmanı ve Risale'deki âyetlerin Kur'ân metniyle eşlenmesi.

Kullanım:
    uv run python -m risale_mcp.fetch quran    # tanzil.net'ten ham veri (bir kez)
    uv run python -m risale_mcp.quran          # data/raw/tanzil -> data/quran.json

`data/quran.json` Risale eserlerinden ayrı bir katmandır; atıf birimi âyettir ("Bakara Sûresi, 2:255"),
cümle değil. `build_db` onu kendi tablolarına yazar ve Risale'deki Arapça parçaları onunla karşılaştırır.

Metin ve mealler:
- `text`: Medine Mushafı hattı (Tanzil "uthmani"), harekeli. Kullanıcıya gösterilen metindir.
- `text_simple`: imlâî yazım, harekeli. `text_clean`: harekesiz; yalnızca eşleme için.
- Mealler: Diyanet İşleri Başkanlığı (`tr.diyanet`) ve Türkiye Diyanet Vakfı (`tr.vakfi`). Tanzil'in
  şartı: ticari olmayan kullanım; ortak derlemlere girerse Diyanet'ten izin gerekir.
- Sûrelerin Türkçe adları aşağıdaki listededir (Tanzil yalnızca Arapça adları verir).
- Diyanet İşleri meali art arda birkaç âyeti birlikte tercüme eder (570 grup, 1.413 âyet); Tanzil aynı
  metni gruptaki her âyete yazar. Böyle bir âyette `spans` mealin kapsadığı ilk ve son âyettir.

Eşleme (`skeleton`): Risale'nin Arapça yazımı Tanzil'inkinden farklıdır (Türk mushafı imlâsı, "﷽" bağlaması,
"…الخ" ile kısaltma). Bu yüzden iki metin de harf iskeletine indirilir: hareke ve işaretler, hemze, elif,
vav ve ye atılır; elif çeşitleri, tâ-i merbûta (ة = ت) ve Farsça harfler birleştirilir. Alıntı "…" ve
"الخ" yerlerinden parçalara bölünür; her parça âyet metninde (Osmanî ya da imlâî iskelette) aranır.
"""

import argparse
import bisect
import json
import re
import unicodedata
from dataclasses import dataclass
from functools import cache, cached_property
from pathlib import Path

from risale_mcp.paths import DATA_DIR, RAW_DIR, ROOT
from risale_mcp.sources import tanzil

QURAN_PATH = DATA_DIR / "quran.json"
TANZIL_DIR = RAW_DIR / "tanzil"
TRANSLATIONS = {  # veritabanındaki kimlik -> (Tanzil kimliği, ad)
    "diyanet-isleri": ("tr.diyanet", "Diyanet İşleri Başkanlığı meali"),
    "diyanet-vakfi": ("tr.vakfi", "Türkiye Diyanet Vakfı meali"),
}

SURA_NAMES = (
    "Fâtiha", "Bakara", "Âl-i İmrân", "Nisâ", "Mâide", "En'âm", "A'râf", "Enfâl", "Tevbe", "Yûnus",
    "Hûd", "Yûsuf", "Ra'd", "İbrâhîm", "Hicr", "Nahl", "İsrâ", "Kehf", "Meryem", "Tâhâ",
    "Enbiyâ", "Hac", "Mü'minûn", "Nûr", "Furkān", "Şuarâ", "Neml", "Kasas", "Ankebût", "Rûm",
    "Lokmân", "Secde", "Ahzâb", "Sebe'", "Fâtır", "Yâsîn", "Sâffât", "Sâd", "Zümer", "Mü'min",
    "Fussilet", "Şûrâ", "Zuhruf", "Duhân", "Câsiye", "Ahkāf", "Muhammed", "Fetih", "Hucurât", "Kāf",
    "Zâriyât", "Tûr", "Necm", "Kamer", "Rahmân", "Vâkıa", "Hadîd", "Mücâdele", "Haşr", "Mümtehine",
    "Saf", "Cuma", "Münâfikūn", "Teğâbün", "Talâk", "Tahrîm", "Mülk", "Kalem", "Hâkka", "Meâric",
    "Nûh", "Cin", "Müzzemmil", "Müddessir", "Kıyâme", "İnsân", "Mürselât", "Nebe'", "Nâziât", "Abese",
    "Tekvîr", "İnfitâr", "Mutaffifîn", "İnşikāk", "Bürûc", "Târık", "A'lâ", "Gāşiye", "Fecr", "Beled",
    "Şems", "Leyl", "Duhâ", "İnşirâh", "Tîn", "Alak", "Kadr", "Beyyine", "Zilzâl", "Âdiyât",
    "Kāria", "Tekâsür", "Asr", "Hümeze", "Fîl", "Kureyş", "Mâûn", "Kevser", "Kâfirûn", "Nasr",
    "Tebbet", "İhlâs", "Felak", "Nâs",
)
assert len(SURA_NAMES) == tanzil.SURAS

# Mushaflarda Tanzil'deki addan başka adla anılan sûreler (Hizbü'l-Kur'ân'ın başlıkları).
OTHER_SURA_NAMES = {"المؤمن": 40, "الانشراح": 94, "الزلزال": 99}

MIN_CONTEXT = 3  # bölümün kendi âyetlerinde aranan parantezli alıntının iskeletteki en az harf sayısı
MIN_CONTEXT_ONE = 2  # bölüm tek bir âyeti işliyorsa ("(رَبِّ)" -> "رب")
MIN_UNIQUE = 6   # metinden (kaynak numarası olmadan) bulunan alıntının iskeletteki en az harf sayısı
NEAR = 2         # kaynağın numarasından en çok bu kadar âyet uzakta bulunan alıntı "komşu" sayılır

_LETTERS = str.maketrans({"ٱ": "ا", "أ": "ا", "إ": "ا", "آ": "ا", "ى": "ي", "ی": "ي", "ک": "ك", "ة": "ت",
                          "ؤ": "و", "ئ": "ي", "ھ": "ه", "ۀ": "ه"})
_DROPPED = str.maketrans({"ا": None, "و": None, "ي": None, "ء": None, "ـ": None})
_NOT_LETTER = re.compile(r"[^ء-ي]")
_BESMELE = "بسم الله الرحمن الرحيم"
_CUTS = re.compile(r"…|\.\.\.|[()\[\]﴿﴾❋*]|\bالخ\b")
_ETC_END = re.compile(r"[اٱ]?ل[ً-ْٰ]*خ[ً-ْ]*\W*$")   # sondaki "اَلْخ"
_AYAH_MARK = re.compile(r"﴿\s*([٠-٩0-9]+)\s*﴾")                                      # Hizb: "…﴿٢﴾"
_BRACKETED = re.compile(r"﴿([^﴾]*[^\s﴾٠-٩0-9–\-][^﴾]*)﴾")                              # Mesnevî: "﴿ metin ﴾"


def sura_ref(sura: int, start: int, end: int | None = None) -> str:
    """'Bakara Sûresi, 2:255' ya da 'Bakara Sûresi, 2:255-257' (kaynakların yazdığı biçim)."""
    ayahs = f"{start}" if not end or end == start else f"{start}-{end}"
    return f"{SURA_NAMES[sura - 1]} Sûresi, {sura}:{ayahs}"


def skeleton(text: str) -> str:
    """Arapça metnin harf iskeleti: hareke, işaret, hemze, elif, vav, ye ve boşluk yok."""
    text = unicodedata.normalize("NFKC", text.replace("﷽", _BESMELE))
    text = "".join(ch for ch in text if not unicodedata.category(ch).startswith("M"))
    return _NOT_LETTER.sub("", text.translate(_LETTERS).translate(_DROPPED))


def pieces(text: str, shortest: int = 2) -> list[str]:
    """Alıntının "…" ve "الخ" yerlerinden bölünmüş, iskelete indirilmiş parçaları (kısa olanlar atılır)."""
    text = _ETC_END.sub("", text.strip())
    return [p for p in map(skeleton, _CUTS.split(text)) if len(p) >= shortest]


@dataclass(frozen=True)
class Match:
    sura: int
    start: int
    end: int


class Quran:
    """`data/quran.json` ile âyet arama: âyet metni, iskelet ve bir parçanın geçtiği âyetler."""

    def __init__(self, data: dict) -> None:
        self.data = data
        self.ayahs = {(s["number"], a["ayah"]): a for s in data["suras"] for a in s["ayahs"]}
        self.counts = {s["number"]: len(s["ayahs"]) for s in data["suras"]}

    @classmethod
    def load(cls, path: Path = QURAN_PATH) -> "Quran | None":
        return cls(json.loads(path.read_text(encoding="utf-8"))) if path.exists() else None

    @cached_property
    def _skeletons(self) -> list[dict[int, tuple[str, list[int]]]]:
        """İki yazım için sûre başına iskelet dizisi ve her âyetin dizideki başlangıcı."""
        out = []
        for field in ("text", "text_clean"):
            suras = {}
            for number, count in self.counts.items():
                buf, starts = "", []
                for ayah in range(1, count + 1):
                    starts.append(len(buf))
                    buf += skeleton(self.ayahs[(number, ayah)][field])
                suras[number] = (buf, starts)
            out.append(suras)
        return out

    def find(self, piece: str, sura: int | None = None) -> set[Match]:
        """İskelet parçasının geçtiği bütün yerler (bir parça birden çok âyete taşabilir)."""
        hits = set()
        for suras in self._skeletons:
            for number, (buf, starts) in suras.items():
                if sura is not None and number != sura:
                    continue
                i = buf.find(piece)
                while i >= 0:
                    hits.add(Match(number, bisect.bisect_right(starts, i), bisect.bisect_right(starts, i + len(piece) - 1)))
                    i = buf.find(piece, i + 1)
        return hits

    def contains(self, parts: list[str], sura: int, start: int, end: int) -> bool:
        """Bütün parçalar âyet aralığının metninde (iki yazımdan birinde) geçiyor mu?"""
        if not parts or not 1 <= start <= end <= self.counts.get(sura, 0):
            return False
        for suras in self._skeletons:
            buf, starts = suras[sura]
            stop = starts[end] if end < len(starts) else len(buf)
            if all(p in buf[starts[start - 1]:stop] for p in parts):
                return True
        return False

    def check(self, text: str, sura: int, start: int, end: int) -> str:
        """Kaynağın verdiği numarayı metinle denetler: exact, near (komşu âyetlerde), differs, empty."""
        parts = pieces(text) or pieces(text, shortest=1)      # "يٰسٓ", "اِيَّاكَ" tek harfe iner
        if not parts:
            return "empty"
        if self.contains(parts, sura, start, end):
            return "exact"
        if self.contains(parts, sura, max(1, start - NEAR), min(self.counts.get(sura, 0), end + NEAR)):
            return "near"
        return "differs"

    def locate(self, text: str) -> list["Quote"]:
        """Kaynağı âyet olarak işaretlememiş Arapçadaki Kur'ân alıntıları.

        Hizb paragrafları âyet numarasını mushaftaki gibi metnin sonunda verir ("…﴿٢﴾"); her numaradan
        önceki metin o numaralı âyetle biten yerde aranır. el-Mesnevî el-Arabî âyeti "﴿ … ﴾" içine alır;
        numarasız alıntı yalnızca Kur'ân'da tek bir yerde geçiyorsa bulunmuş sayılır.
        """
        out = []
        marks = list(_AYAH_MARK.finditer(text))
        if marks:
            begin = 0
            for m in marks:
                number = int(m[1].translate(_DIGITS))
                # Numaralı âyet tek harfe inebilir ("يٰسٓ" -> "س"); yeri numarası ve sûresi belirler.
                parts = pieces(text[begin:m.start()], shortest=1)
                if parts:
                    hits = {h for h in self.find(max(parts, key=len))
                            if h.end == number and self.contains(parts, h.sura, h.start, h.end)}
                    out.append(Quote(begin, m.end(), parts, number, hits.pop() if len(hits) == 1 else None))
                begin = m.end()
            return out
        for m in _BRACKETED.finditer(text):
            parts = pieces(m[1])
            if parts and len(longest := max(parts, key=len)) >= MIN_UNIQUE:
                hits = {h for h in self.find(longest) if self.contains(parts, h.sura, h.start, h.end)}
                out.append(Quote(m.start(), m.end(), parts, None, hits.pop() if len(hits) == 1 else None))
        return out

    def locate_quote(self, text: str, context: tuple[int, int, int] | None) -> Match | None:
        """Parantezli alıntı ("(الذين يؤمنون بالغيب)"): önce bölümün işlediği âyetlerde (tek âyet öncelikli),
        sonra yalnızca Kur'ân'da tek bir yerde geçen uzun alıntıysa bütün Kur'ân'da."""
        parts = pieces(text)
        letters = sum(map(len, parts))
        single = context is not None and context[1] == context[2]
        if not parts or letters < (MIN_CONTEXT_ONE if single else MIN_CONTEXT):
            return None
        if context:
            sura, first, last = context
            for ayah in range(first, last + 1):
                if self.contains(parts, sura, ayah, ayah):
                    return Match(sura, ayah, ayah)
            if self.contains(parts, sura, first, last):
                return Match(sura, first, last)
        longest = max(parts, key=len)
        if len(longest) < MIN_UNIQUE:
            return None
        hits = {h for h in self.find(longest) if self.contains(parts, h.sura, h.start, h.end)}
        return hits.pop() if len(hits) == 1 else None

    def in_sura(self, quote: "Quote", sura: int) -> Match | None:
        """Kısa ya da birden çok sûrede geçen numaralı âyet, bölümün sûresi veriden bilinince."""
        if quote.number is None:
            return None
        for start in range(quote.number, max(0, quote.number - 5), -1):
            if self.contains(quote.parts, sura, start, quote.number):
                return Match(sura, start, quote.number)
        return None


@dataclass
class Quote:
    start: int              # Arapça parçanın içindeki konum
    end: int
    parts: list[str]        # iskelet parçaları
    number: int | None      # metnin verdiği âyet numarası (Hizb)
    match: Match | None     # bulunan yer; adaylar ayrılamadıysa None


_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")


_VERSE_TITLE = re.compile(r"^(\d+)(?:[‑-](\d+))?\. Âyet")      # "6. Âyetin Tefsiri", "17‑20. Âyetlerin Tefsiri"
_SURA_SECTIONS = {"sure-i-fatiha": (1, 1, 7), "sure-i-bakara": (2, None, None)}
# Fâtiha'nın bölümleri (İşaratü'l-İ'caz'ın Türkçesi ve Arapçası aynı kimlikle) -> işlediği âyet.
FATIHA_VERSES = {"bismillahi": 1, "er-rahmanir-rahim": 1, "el-hamdu": 2, "lillahi": 2, "rabbi": 2, "el-alemin": 2,
                 "er-rahmanir-rahim-2": 3, "maliki-yevmid-din": 4, "iyyake-nabudu": 5, "ve-iyyake-nestein": 5,
                 "ihdina": 6, "es-siratal-mustekim": 6, "siratallezine-enamte-aleyhim": 7,
                 "gayril-magdubi-aleyhim": 7, "ve-led-dallin": 7}


def verse_context(outline: list[dict]) -> dict[str, tuple[int, int, int]]:
    """İşaratü'l-İ'caz gibi âyet âyet ilerleyen eserde her bölümün işlediği âyetler: düğüm -> (sûre, ilk, son).
    Bakara'nın bölümü başlığındaki numaralardan ("6. Âyetin Tefsiri"), Fâtiha'nın bölümü işlediği âyet
    parçasından (`FATIHA_VERSES`; ilk "Er-Rahmânir-Rahîm" Besmele'deki, ikincisi 3. âyet); alt bölümler üst
    bölümünkini alır. Böyle bir yapısı olmayan eserde boştur."""
    out: dict[str, tuple[int, int, int]] = {}
    for node in outline:                      # başlık ağacı kitap sırasındadır: üst bölüm önce gelir
        local = node["id"].rsplit("/", 1)[-1]
        parent = node.get("parent_id")
        if local in _SURA_SECTIONS and _SURA_SECTIONS[local][1]:
            out[node["id"]] = _SURA_SECTIONS[local]
        elif parent and parent.rsplit("/", 1)[-1] == "sure-i-fatiha" and local in FATIHA_VERSES:
            out[node["id"]] = (1, FATIHA_VERSES[local], FATIHA_VERSES[local])
        elif parent and parent.rsplit("/", 1)[-1] == "sure-i-bakara" and (m := _VERSE_TITLE.match(node["title"])):
            out[node["id"]] = (2, int(m[1]), int(m[2] or m[1]))
        elif parent in out:
            out[node["id"]] = out[parent]
    return out


@cache
def arabic_sura_numbers(raw: Path = TANZIL_DIR) -> dict[str, frozenset[int]]:
    """Sûrenin Arapça adının iskeleti -> numaraları (Tanzil'den; ham veri yoksa boş). Bazı adlar aynı
    iskelete iner (en-Nisâ ile en-Nâs, el-Enbiyâ ile en-Nebe'); seçimi kullanan yapar."""
    path = tanzil.text_path(raw, "uthmani")
    if not path.exists():
        return {}
    keys: dict[str, set[int]] = {}
    for sura in tanzil.read_xml(path).iter("sura"):
        keys.setdefault(skeleton(sura.get("name")), set()).add(int(sura.get("index")))
    for name, number in OTHER_SURA_NAMES.items():
        keys.setdefault(skeleton(name), set()).add(number)
    return {key: frozenset(numbers) for key, numbers in keys.items()}


# ---------------------------------------------------------------- ham veri -> data/quran.json

def build_json(raw: Path = TANZIL_DIR) -> dict:
    texts = {t: tanzil.ayahs(tanzil.read_xml(tanzil.text_path(raw, t))) for t in tanzil.TEXT_TYPES}
    meals = {key: tanzil.ayahs(tanzil.read_xml(tanzil.translation_path(raw, tid)))
             for key, (tid, _) in TRANSLATIONS.items()}
    names = {int(s.get("index")): s.get("name") for s in tanzil.read_xml(tanzil.text_path(raw, "uthmani")).iter("sura")}
    suras = []
    for number in range(1, tanzil.SURAS + 1):
        count = sum(1 for s, _ in texts["uthmani"] if s == number)
        suras.append({
            "number": number, "name": SURA_NAMES[number - 1], "name_ar": names[number],
            "ayahs": [{"ayah": a, "text": texts["uthmani"][(number, a)], "text_simple": texts["simple"][(number, a)],
                       "text_clean": texts["simple-clean"][(number, a)],
                       "translations": {key: meal[(number, a)] for key, meal in meals.items()}}
                      for a in range(1, count + 1)],
        })
        _mark_spans(suras[-1]["ayahs"])
    return {
        "source": tanzil.ATTRIBUTION, "url": tanzil.BASE_URL,
        "terms": "Arapça metin değiştirilmeden, kaynağı (Tanzil Project) belirtilerek kullanılır. "
                 "Mealler yalnızca ticari olmayan kullanım içindir.",
        "translations": [{"id": key, "name": name, "tanzil_id": tid} for key, (tid, name) in TRANSLATIONS.items()],
        "suras": suras,
    }


def _mark_spans(ayahs: list[dict]) -> None:
    """Aynı meal metni art arda gelen âyetlerde tekrarlanıyorsa o meal bu âyetleri birlikte tercüme eder."""
    for key in TRANSLATIONS:
        i = 0
        while i < len(ayahs):
            j = i
            while j + 1 < len(ayahs) and ayahs[j + 1]["translations"][key] == ayahs[i]["translations"][key]:
                j += 1
            if j > i:
                for a in ayahs[i:j + 1]:
                    a.setdefault("spans", {})[key] = [ayahs[i]["ayah"], ayahs[j]["ayah"]]
            i = j + 1


def main() -> None:
    argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    lines, ok = tanzil.check_book("quran", TANZIL_DIR)
    if not ok:
        raise SystemExit("\n".join(lines) + "\nÖnce `uv run python -m risale_mcp.fetch quran`.")
    data = build_json()
    QURAN_PATH.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    ayahs = sum(len(s["ayahs"]) for s in data["suras"])
    print(f"{len(data['suras'])} sûre, {ayahs} âyet, {len(data['translations'])} meal")
    print(f"  yazıldı: {QURAN_PATH.relative_to(ROOT)} ({QURAN_PATH.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
