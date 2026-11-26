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
end, as candidates."""

KIPLER: dict[str, Kip] = {k.id: k for k in (
    Kip("serbest", "Serbest soru", "Risale-i Nur'a dair bir soru yazın"),
    Kip("tarama", "Konu taraması", "Bir konu yazın; eserlerde geçtiği yerleri toplayalım",
        instructions=SURVEY_INSTRUCTIONS, tools=("survey",), post=("other_places",)),
)}
DEFAULT = "serbest"


def get(kip_id: str | None) -> Kip:
    return KIPLER.get(kip_id or DEFAULT, KIPLER[DEFAULT])


def public() -> list[dict]:
    """Arayüz için: id, ad, açıklama."""
    return [{"id": k.id, "title": k.title, "hint": k.hint} for k in KIPLER.values()]


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
LOCAL_TOOLS = {"survey": SURVEY_TOOL}
