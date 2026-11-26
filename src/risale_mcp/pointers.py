"""S13.14: metin içi göndermeler. Müellif okuyucuyu çoğu zaman başka bir yere gönderir ("Onuncu Söz'ün Hâtimesi'nde
icmâlen ve Nokta Risalesi'nde ve Yirminci Mektûb'da izâhen beyân etmişiz", "İşârâtü'l-İ'câz'da yazmıştım"). Model
bu göndermeleri izlemiyordu (haşir konuşması, 2026-11-26). Okuma araçları (`read_section`, `get_passage`) okunan
cümlelerdeki göndermeleri hedefleri çözülmüş olarak verir (`points_to`); hem bağdaştırıcıda hem sohbette çalışır.

Bir cümle gönderme sayılır, iki şart birlikte tutarsa:
- **fiil:** cümlede gönderme kelimelerinden biri (`TRIGGERS`: tafsilen, müracaat, izah, beyan, isbat, zikredilmiş,
  bahsedilmiş, yazmıştım, bakınız…, kelime başı olarak);
- **hedef:** çözülebilen bir yer: sıra sayısı ve tür ("Yirmi Dokuzuncu Söz", "Onuncu Söz'ün Hâtimesi",
  "Yirminci Mektûb", "Otuzuncu Lem'a", "Yedinci Şuâ"; eski adı olan numara `old_names.json`'daki asıl yerine),
  risale adı (`risale_adlari.json`: "Haşir Risalesi") ya da eser adı (`WORK_NAMES`: "İşârâtü'l-İ'câz").
Adın son kelimesi ekli olabilir ("Nokta Risalesi'nde", "İşârâtü'l-İ'câz'da"). Tek kelimelik adlar (Lemeât,
Muhâkemât) yalnız metinde büyük harfle başlıyorsa sayılır ("nokta", "meyve", "muhâkemât-ı akliye" sıradan
kelimedir); "Sünûhât" sıradan kelime olarak da çok geçtiği için eser adı listesinde yoktur. Okunan bölümün kendisi, üstü ya da altı hedef sayılmaz. Hüküm değildir: gönderme gösterir, okunmasını
model seçer; amaç "orada yazılmış" denen yerin okunmadan geçilmemesidir.
"""

import json
import re
from pathlib import Path

from risale_mcp.normalize import fold, parse_ordinal, search_words

BOOKS = Path(__file__).parent / "books"
OLD_NAMES = json.loads((BOOKS / "old_names.json").read_text(encoding="utf-8"))["sections"]
RISALE_NAMES = json.loads((BOOKS / "risale_adlari.json").read_text(encoding="utf-8"))["names"]

TRIGGERS = ("tafsil", "muracaat", "izah", "beyan", "isbat", "ispat", "zikred", "zikrol", "zikril", "bahsed",
            "bahsol", "bahsedil", "yazmis", "yazdi", "yazil", "yazacag", "mutalaa", "gosterilmis", "gostermis",
            "mufassal", "icmalen", "dercedil", "dercet")
TRIGGER_WORDS = {"bak", "bakiniz", "bakin", "bakilsin"}
# tür kelimesinin başı (fold: küçük harf, şapkasız, kesmesiz) -> eser
TYPES = {"söz": "sozler", "mektub": "mektubat", "mektup": "mektubat", "lema": "lemalar", "şua": "sualar"}
WORK_NAMES = {           # eser adları (yalnız ayırt edici olanlar; Sözler, Lem'alar gibi ciltler hedef değildir)
    "isaratul-icaz": ["İşârâtü'l-İ'câz", "İşaratü'l-İ'caz", "İşârât-ül İ'câz"],
    "muhakemat": ["Muhâkemât"],
    "munazarat": ["Münâzarât"],
    "lemeat": ["Lemeât"],
    "hutbe-i-samiye": ["Hutbe-i Şâmiye"],
    "mesnevi-i-nuriye": ["Mesnevî-i Nuriye", "Mesnevî-i Nûriye"],
    "el-mesnevi-el-arabi": ["Mesnevî-i Arabî", "Arabî Mesnevî", "Mesnevî-i Arabî-i Nurî"],
    "divan-i-harb-i-orfi": ["Divan-ı Harb-i Örfî"],
    "hutuvat-i-sitte": ["Hutuvât-ı Sitte"],
    "talikat": ["Ta'likat"],
    "rumuzat-i-semaniye": ["Rumuzat-ı Semaniye"],
}
MAX_POINTERS = 12
SUFFIX = 6
WORD = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*")


def _names() -> list[tuple[list[str], list[str], bool]]:
    """(arama kelimeleri, hedefler, tek kelime mi) listesi: risale adları ve eser adları."""
    out = []
    for entry in RISALE_NAMES:
        for alias in (entry["name"], *entry.get("aliases", ())):
            if key := search_words(alias):
                out.append((key, entry["ids"], len(key) == 1))
    for work, aliases in WORK_NAMES.items():
        for alias in aliases:
            if key := search_words(alias):
                out.append((key, [work], len(key) == 1))
    return out


NAMES = _names()


def _trigger(words: list[str]) -> bool:
    return any(w in TRIGGER_WORDS or w.startswith(TRIGGERS) for w in words)


def _numbered(text: str, exists) -> list[str]:
    """"Yirmi Dokuzuncu Söz", "Onuncu Söz'ün Hâtimesi" -> ['sozler/29', 'sozler/10/hatime']."""
    tokens = WORD.findall(text)
    out = []
    for i, token in enumerate(tokens):
        folded = fold(token)
        work = next((w for stem, w in TYPES.items() if folded.startswith(stem) and len(folded) <= len(stem) + 6), None)
        if work is None or i == 0:
            continue
        number = None
        if i >= 2:
            number = parse_ordinal(fold(tokens[i - 2]) + fold(tokens[i - 1]))
        if number is None:
            number = parse_ordinal(fold(tokens[i - 1]))
        if number is None:
            continue
        if work == "lemalar" and folded.startswith("lemalar"):
            continue                          # "Lem'alar" cildin adıdır, sıra sayısıyla bir Lem'a değil
        target = f"{work}/{number}"
        if target in OLD_NAMES:
            out += OLD_NAMES[target]["elsewhere"][:1]
            continue
        if i + 1 < len(tokens) and fold(tokens[i + 1]).startswith("hatime") and exists(f"{target}/hatime"):
            target = f"{target}/hatime"
        if exists(target):
            out.append(target)
    return out


def _named(text: str, words: list[str]) -> list[str]:
    out = []
    for key, ids, single in NAMES:
        n = len(key)
        if not any(_matches(words[i:i + n], key) for i in range(len(words) - n + 1)):
            continue
        if single and not any(t[:1].isupper() and _matches(search_words(t)[:1], key) for t in WORD.findall(text)):
            continue
        out += ids
    return out


def _matches(window: list[str], key: list[str]) -> bool:
    """Adın kelimeleri; sonuncusu ekli olabilir (en çok `SUFFIX` harf: "risalesinde", "icazda")."""
    return (len(window) == len(key) and window[:-1] == key[:-1] and window[-1].startswith(key[-1])
            and len(window[-1]) - len(key[-1]) <= SUFFIX)


def find(sentences: list[dict], here: str, exists, ref) -> list[dict]:
    """Okunan cümlelerdeki göndermeler: [{sentence, to: [{id, ref}]}]. `here` okunan bölüm (kendisi, üstü ve altı
    hedef sayılmaz); `exists(id)` düğüm var mı, `ref(id)` atıf yolu."""
    out = []
    for s in sentences:
        text = s.get("text") or ""
        words = search_words(text)
        if not words or not _trigger(words):
            continue
        targets = []
        for target in [*_numbered(text, exists), *_named(text, words)]:
            related = target == here or here.startswith(target + "/") or target.startswith(here + "/")
            if not related and target not in targets and exists(target):
                targets.append(target)
        if targets:
            out.append({"sentence": s["id"], "to": [{"id": t, "ref": ref(t)} for t in targets]})
            if len(out) >= MAX_POINTERS:
                break
    return out
