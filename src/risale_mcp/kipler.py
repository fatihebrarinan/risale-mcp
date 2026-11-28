"""S13.12: kip kaydı. Bir kip, sohbetin bir soruyu nasıl ele aldığının tarifidir: okuyucuya görünen adı ve açıklaması,
modele giden kısa talimatı (sayfa notu olarak), modele açılan ek araçları, cevaptan sonra sunucunun eklediği mekanik
listeler. Kayıt **tek kaynaktır** (kullanıcının kararı, 2026-11-26): ileride MCP hazır komutları ve eklentinin
skill'leri de buradan üretilir (`docs/kipler-plani.md`). Kipler şimdilik okuyucunun açık seçimiyle çalışır;
yönlendirici (otomatik kip) aynı kaydı kullanacak.

Yalınlık ilkesi: serbest soru bugünkü akıştır; kipin parçaları yalnız o kip seçilince devreye girer.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Kip:
    id: str
    title: str                     # okuyucuya (Türkçe)
    hint: str                      # okuyucuya kısa açıklama, giriş kutusunun yer tutucusu
    instructions: str = ""         # modele (İngilizce), sorunun önünde sayfa notu olarak
    tools: tuple[str, ...] = ()    # bu kipte açılan ek araçlar (sohbetin kendi araçları)
    post: tuple[str, ...] = ()     # cevaptan sonra sunucunun eklediği listeler
    scope: tuple[str, ...] = field(default=("risale",))   # varsayılan kapsam (ileride: kuran, tefsir, hadis, klasik)
    libraries: tuple[str, ...] = ()   # S13.17: kipin kendiliğinden açtığı öbür kütüphaneler (okuyucunun seçimine eklenir)
    # S14.4: genel sayfanın kipi (yalnız `SOHBET_GENEL` açıkken görünür); `risale_only`: bugünkü Risale talimatı,
    # yalnız Risale'nin araçları (okuyucunun açtığı kütüphaneler de kapanır)
    general_only: bool = False
    risale_only: bool = False
    # S14.2 (2.10, kullanıcının kararı 2026-11-28): genel sayfada da Risale'ye ait kip (konu taraması yalnız Risale'de
    # tarar): orada adı `general_title`, davranışı "Risale-i Nur'dan" gibi (bugünkü talimat, yalnız Risale)
    risale_scope: bool = False
    general_title: str = ""


SURVEY_INSTRUCTIONS = """\
Mode chosen by the reader: topic survey (where a topic is treated across the works).
1. First call survey once, with the topic and its words: the words the text itself would use, old and suffixed \
forms with * (ihlâs*, ihlas*; sabr*, sabır*; ye's, me'yus*), and names of treatises if the reader used one. The page \
gathers the candidate places from every search (names, headings, words, meaning) and returns them ranked, each with \
why it came and where to read (focus).
2. Read the central candidates (their focus, with read_section or get_passage): usually four to six. A word match \
alone is not a treatment; a candidate signed by a student is a student's letter.
3. Answer: the places grouped by work, the central ones first, each with what it says, quoted and marked. Name only \
places you read. Do not write a list of further places yourself: the page adds the candidates you did not cite at the \
end, as candidates, and every place with the words and their count. If the reader asks how many, give the page's \
count (sentences and places with the words); the number of candidates is not a count."""

VERSE_INSTRUCTIONS = """\
Mode chosen by the reader: verse study (one verse of the Qur'an, in the Risale-i Nur and in the classical tafsirs).
1. Call verse_file once with the verse (sura number or name, verse number). If the reader named the verse by its \
words or its common name and you are not sure which it is, find it first (search, get_ayah). verse_file returns the \
verse with the Türkiye Diyanet Vakfı translation; the places in the Risale-i Nur tied to it (kind of tie, strong \
first) and the sections that quote it; and the tafsir units that treat it, in the order of their authors' death, \
with how much each devotes to this verse (share) and read_first: the units that treat it most extensively.
2. Read the Risale's strong ties first (read_section or get_passage at their evidence), then the tafsir units in \
read_first with tefsir_read_section (max_words about 1200; at most four units; go further only if the question \
needs it). Never choose a tafsir by its fame: follow read_first unless the reader names a work.
3. Answer in this order, with short headings: the verse and its translation (name it as the Türkiye Diyanet Vakfı \
translation); in the Risale-i Nur (name each tie by its kind; a Risale passage is never called a tafsir of the \
verse; if there is no tie, say so plainly and give where it is quoted); in the tafsirs (each work apart, strictly in \
the order verse_file lists them, which is the order of their authors' death, never by the order you read them; its \
Arabic quoted exactly with your labelled translation); then your interpretation \
under its own heading, where any relation between the works is yours. Do not list the units or places you did not \
read: the page adds them. Follow verse_file's note about the Hadith Library."""

KIPLER: dict[str, Kip] = {k.id: k for k in (
    Kip("serbest", "Serbest soru", "Risale-i Nur'a dair bir soru yazın"),
    # S14.1 K2 (kullanıcının kararı, 2026-11-28): "Risale-i Nur'dan cevapla" seçeneği; açıkken bugünkü davranış aynen
    Kip("risale", "Risale-i Nur'dan", "Cevap yalnız Risale-i Nur'dan gelsin", general_only=True, risale_only=True),
    Kip("tarama", "Konu taraması", "Bir konu yazın; eserlerde geçtiği yerleri toplayalım",
        instructions=SURVEY_INSTRUCTIONS, tools=("survey",), post=("other_places",),
        risale_scope=True, general_title="Risale-i Nur'da konu taraması"),
    Kip("ayet", "Âyet çalışması", "Bir âyet yazın (Bakara 255, Âyetü'l-Kürsî); Risale'de ve tefsirlerde birlikte bakalım",
        instructions=VERSE_INSTRUCTIONS, tools=("verse_file",), post=("verse_places",), libraries=("tefsir",)),
)}
DEFAULT = "serbest"


def get(kip_id: str | None) -> Kip:
    return KIPLER.get(kip_id or DEFAULT, KIPLER[DEFAULT])


def risale_only(kip: Kip, general: bool) -> bool:
    """Bu kip bu sayfada yalnız Risale mi (bugünkü talimat, öbür kütüphaneler kapalı)."""
    return kip.risale_only or (general and kip.risale_scope)


def public(general: bool = False) -> list[dict]:
    """Arayüz için: id, ad, açıklama. Genel sayfanın kipleri yalnız `general` açıkken (S14.4); genel sayfada Risale'ye
    ait kipin adı `general_title`, `risale_only` işaretiyle (sayfa kütüphane işaretini ona göre gösterir)."""
    return [{"id": k.id, "title": (k.general_title if general and k.general_title else k.title), "base": k.title,
             "hint": k.hint,
             "libraries": list(k.libraries), **({"risale_only": True} if risale_only(k, general) else {})}
            for k in KIPLER.values() if general or not k.general_only]


# ------------------------------------------------------------ sohbetin kendi araçları

SURVEY_TOOL = {
    "name": "survey",
    "description": ("Gather every candidate place where a topic is treated in the works (Risale-i Nur): treatises "
                    "named in the query, matching headings, sentences with the topic's words (word starts with *), "
                    "and meaning. Returns candidates ranked, each with why it came (named, heading, words in N "
                    "sentences, meaning), its size, focus (subsections to read), the closest sentences, and signed "
                    "(who signs a letter). Call it once at the start of a topic survey."),
    "input_schema": {
        "type": "object",
        "properties": {
            "topic": {"type": "string", "description": "The topic in the reader's words (today's language is fine)."},
            "terms": {"type": "array", "items": {"type": "string"},
                      "description": ("The text's own words for it, old and suffixed forms with * (ihlâs*, ihlas*), "
                                      "and treatise names if any (İhlâs Risalesi).")},
        },
        "required": ["topic"],
    },
}
VERSE_TOOL = {
    "name": "verse_file",
    "description": ("Gather a verse study's file: the verse with the Türkiye Diyanet Vakfı translation, the places in "
                    "the Risale-i Nur tied to it (kind, strength, evidence sentence) and the sections quoting it, and "
                    "the tafsir units treating it in the order of their authors' death, each with its share of this "
                    "verse; read_first lists the most extensive. Call it once at the start of a verse study."),
    "input_schema": {
        "type": "object",
        "properties": {
            "sura": {"type": "string", "description": "Sura number (1–114) or name, e.g. '2' or 'Bakara'."},
            "ayah": {"type": "integer", "minimum": 1, "description": "Verse number."},
        },
        "required": ["sura", "ayah"],
    },
}
# S14.4 (genel setin ölçümü, 2026-11-28): genel sayfada model ilk aramayı Risale'nin `semantic_search`'üyle yapıyor,
# Türkçe ve zengin sonuçla yetinip öbür kütüphanelere hiç bakmıyordu (yalnız Risale'den cevaplanan yedi sorunun
# yedisinde ilk adım buydu). Bu araç anlamca aramayı bütün açık kütüphanelerde birlikte yapar ve sonuçları kütüphane
# kütüphane, yan yana verir: tek listede sıralansa Türkçe soru Türkçe külliyatta hep yüksek puan alır.
SEARCH_ALL_TOOL = {
    "name": "search_all",
    "description": ("Find passages by meaning in every open library at once: the Risale-i Nur and, if open, the hadith "
                    "collections, the tafsirs and the classical works. Returns, library by library, the closest "
                    "sentences or reports (id with the library's name, work, excerpt) and the sections where the topic "
                    "concentrates. Similarity is comparable only within one library (a question in Turkish scores "
                    "higher in the Turkish Risale). Use it first for a question in today's words; then read the "
                    "candidates that answer the question best, in their own library."),
    "input_schema": {
        "type": "object",
        "properties": {"query": {"type": "string", "description": "The question or topic, in any language."}},
        "required": ["query"],
    },
}
LOCAL_TOOLS = {"survey": SURVEY_TOOL, "verse_file": VERSE_TOOL, "search_all": SEARCH_ALL_TOOL}
