"""Aşama 6: MCP sunucusu.

Kullanım:
    uv run risale-mcp                                # stdio: Claude Desktop ve Claude Code başlatır
    uv run risale-mcp --db yol/risale.db
    uv run risale-mcp --transport streamable-http --public-url https://<adres>   # OAuth'lu HTTP (Aşama 12)
    uv run risale-mcp --transport streamable-http --no-auth   # yerel HTTP (127.0.0.1:8000/mcp), kimlik doğrulamasız
    uv run risale-mcp auth add-user <ad>             # hesaplar, oturumlar, kullanım kaydı (bkz. auth.py)
    npx @modelcontextprotocol/inspector uv run risale-mcp   # MCP Inspector ile elle deneme

Araçlar `library.Library` üzerinden veritabanını salt okunur kullanır; veritabanı yeniden
kurulursa bir sonraki çağrıda yeni dosya açılır. Modelin okuduğu her şey (talimatlar, araç
açıklamaları, hazır komutlar) İngilizcedir; model kullanıcıya onun dilinde cevap verir.
Araçlar sıkıştırılmış JSON metni döndürür (SDK'nın girintili JSON'u uzun metinde boşa token harcar).
"""

import argparse
import base64
import json
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Annotated
from urllib.parse import urlparse

import uvicorn
from mcp.server.auth.middleware.auth_context import get_access_token
from mcp.server.auth.middleware.bearer_auth import RequireAuthMiddleware
from mcp.server.auth.routes import build_resource_metadata_url
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.server.transport_security import TransportSecuritySettings
from mcp_types import Icon, ToolAnnotations
from pydantic import Field
from starlette.applications import Starlette
from starlette.responses import Response

from risale_mcp.auth import (
    ANON_SEMANTIC_PER_DAY,
    AnonymousGate,
    AuthStore,
    Provider,
    login_endpoint,
    start_of_day,
    usage_middleware,
)
from risale_mcp.auth import main as auth_main
from risale_mcp.auth import settings as auth_settings
from risale_mcp.citations import CitationChecker, summary
from risale_mcp.db import DatabaseError
from risale_mcp.env import load_env
from risale_mcp.library import Library, LibraryError
from risale_mcp.paths import DB_PATH

NAME = "risale"
RESOURCE_TEXT_WORDS = 20000      # kaynak olarak eklenen bölüm metninin üst sınırı

INSTRUCTIONS = """\
This server gives read access to the complete works of Bediüzzaman Said Nursî: the Risale-i Nur \
volumes (Sözler, Mektubat, Lem'alar, Şualar, the Lâhikas, Tarihçe-i Hayat), the works of the early \
period (Muhâkemât, Münâzarât, Makalat, Nutuk, İşârâtü'l-İ'câz, el-Mesnevî el-Arabî…), the \
compilations (mecmua: Asâ-yı Mûsâ, Zülfikâr…) and the Hizbs. Texts are split into sentences; every \
sentence has a stable id and a reference (ref) such as \
"Sözler › Onuncu Söz › On iki Hakikat › Dokuzuncu Hakikat › 1. cümle".

Rules:
1. Back every statement about the works with tool results and cite the ref or id they return. Never \
invent references, ids, quotations or section names.
2. When you show a reference to the user, give the section path and the sentence's opening words in \
quotes instead of its number, e.g. Sözler › Onuncu Söz › On iki Hakikat › Dokuzuncu Hakikat › \
"Hiç mümkün müdür ki; ölmüş…". The opening words are the sentence's incipit.
3. Write every reference in full, from the work down, exactly as the tools' ref gives it: printed \
titles unshortened ("Yirminci Söz’ün İkinci Makamı", not "İkinci Makam"), no levels left out, and \
never relative to an earlier reference ("…", "same place", a bare "Birinci Mebhas"). Use › only in \
references, not for your own labels.
4. Put quotation marks only around the text's own words, never around your paraphrase.
5. Every quotation from the works stands on its own line as a block quote in quotation marks \
(> "…"), with a blank line before and after it. This holds for every quotation of a sentence or part \
of one, also a short one. Inside your own prose, quote at most a single term or name (e.g. "tefânî").
6. When a parable, an example or one line of thought runs over several consecutive sentences of one \
section, do not split it into separate quotations: quote the sentences together in one block and give \
one reference for all of them, with the first sentence's opening words and the number of sentences, \
always in this form: Sözler › Birinci Söz › "Bedevî Arab çöllerinde seyahat eden…" ile başlayan 4 \
cümle. At most 8 sentences per reference; the sentences stay inside one section (a new heading starts \
a new reference) and hâşiyes are cited separately. get_passage with a range (first..last) returns the \
reference to use (cite_as). A single sentence is cited on its own as in rule 2.
7. Before giving an answer that contains references, pass them to verify_citations and correct every \
one it flags.
8. If the tools do not return something, say that you could not find it in the works. Do not fill \
the gap from memory.
9. Keep what the text says apart from your own interpretation, under separate headings.
10. Answer in the user's language (usually Turkish); quote the text as returned.
11. The translations of quoted verses and hadiths (publisher_translation) were added by the \
publishers, not by the author: Bediüzzaman quoted the Arabic and needed no translation, and editions \
translate differently. Use them only to convey what the Arabic means, say they are the publisher's \
translation, and never present them as the author's words or quote them as the text. The author's \
own explanation of a verse is part of the text itself, often right after the Arabic ("Yani, …"); \
quote and cite that as the text.
12. Qur'anic verses: show a verse's Arabic only fully vowelled, copied exactly from get_ayah (or as \
the works quote it); never write Qur'anic Arabic from memory and never drop its vowel marks. Cite a \
verse by the ref get_ayah returns, e.g. "Bakara Sûresi, 2:255", without ›. When you give its meaning \
from get_ayah, name the translation (Diyanet İşleri Başkanlığı meali, Türkiye Diyanet Vakfı meali) and \
keep it apart from the publishers' translations in the works and from the author's own explanation. \
A translation with covers_verses renders those verses together; say so instead of presenting it as \
the meaning of the one verse. \
No translation renders the Qur'an exactly or can replace its Arabic text; present translations as an \
aid to the meaning.
13. Links between the works and verses (links in find_ayah, linked_verses in read_section) were found \
by rules in the text's own wording; they are not verdicts. Never call a passage the tafsir (exegesis) \
of a verse on their basis; name the link by its kind and show its evidence sentence: isaret (the text \
says it points to, alludes to or explains the verse), acilis (the section opens with the verse), izah \
(the author's own "Yani…" explanation of it; in works the author wrote in Arabic, such as İşaratü'l-İ'caz \
and Mesnevî-i Nuriye, the Turkish wording is the translator's), dayanak (the text relies on it: "… sırrınca"), risale \
(the verse's allusion to the Risale-i Nur). A weak link is only a reference in one sentence; do not \
present it as what the section is about. Do not append linked verses to every quotation by default: \
bring them up when the user asks about verses or when a verse matters to the question.
14. Some works are not all the author's words; check the subtitle and the paragraph kind. Works the \
author wrote in Arabic exist in Arabic and in Turkish with parallel section ids (isaratul-icaz-arabi/… ↔ \
isaratul-icaz/…); the Turkish is a translation. Sections marked as İhsan Kasım's translation (Hutbe-i \
Şamiye (Arapça), the Nokta risale in el-Mesnevî el-Arabî, the Turkish-written prefaces) are translations of \
Turkish originals: quote the original Turkish work when it exists. In Kızıl İcaz the "quote" paragraphs are \
Ahdarî's Süllem verses that the author annotates, not his words; hâşiye records with commentary_by are his \
brother Abdülmecid Nursî's commentary (şerh) on the author's text: cite them as his, never as the author's.

How to navigate:
- semantic_search finds passages by meaning: use it for concepts and questions in today's words, \
which the text often expresses with other, Ottoman words ("ümitsizlik" finds "ye's"). It also names \
the sections where the topic concentrates. Its results are candidates: read them in context before \
relying on them.
- search finds sentences by the text's own words; marks and Turkish letters are optional ("hasir" \
finds "haşir"). Use it for exact words, phrases, names and technical terms. Use quotes for phrases, \
* for word beginnings, OR, -word to exclude, NEAR(a b, 5).
- Then read the context with read_section (a section and its subsections, in book order, page by \
page with next_cursor) or get_passage (a sentence or range with neighbours and hâşiyes).
- get_outline shows the structure of a work or section; list_works lists the works and their ids.
- find_sentence locates a sentence the user quotes by its first words; find_ayah lists where a \
Qur'anic verse is quoted in the works; get_ayah gives a verse of the Qur'an itself, vowelled, with \
two Diyanet translations and its neighbouring verses on request.
- Compilations (mecmua) reuse text from the main volumes: such paragraphs come with the main \
volume's sentences and refs; cite those. Hâşiye are the author's footnotes, attached to a sentence.
"""

READ_ONLY = ToolAnnotations(read_only_hint=True, destructive_hint=False, idempotent_hint=True, open_world_hint=False)


def _json(payload: object) -> str:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


@contextmanager
def _tool_errors() -> Iterator[None]:
    """Modelin düzeltebileceği hatalar (yanlış kimlik, geçersiz sorgu) ona ileti olarak gider."""
    try:
        yield
    except (LibraryError, DatabaseError) as error:
        raise ToolError(str(error)) from None


# ---------------------------------------------------------------- kaynaklar için Markdown

def _works_markdown(works: list[dict]) -> str:
    lines = ["# Works", ""]
    for w in works:
        size = f"{w['sentences']} sentences" if w.get("sentences") is not None else f"not available ({w['status']})"
        lines.append(f"- `{w['id']}` {w['title']} [{w['group']}] — {size}")
    return "\n".join(lines) + "\n"


def _outline_markdown(node: dict, depth: int = 0) -> list[str]:
    subtitle = f" — {node['subtitle']}" if node.get("subtitle") else ""
    lines = [f"{'  ' * depth}- {node['title']}{subtitle} `{node['id']}`"]
    for child in node.get("children", []):
        lines += _outline_markdown(child, depth + 1)
    return lines


def _section_markdown(section: dict) -> str:
    """Okuma sonucu: başlıklar, numaralı cümleler ("[32] …"), hâşiyeler."""
    lines = []
    for item in section["items"]:
        if "section" in item:
            lines += ["", f"## {item['ref']}", *([f"*{item['subtitle']}*"] if item.get("subtitle") else []), ""]
        elif "gap" in item:
            lines += [f"[{item['gap']}]", ""]
        else:
            text = " ".join(f"[{int(s['id'].rsplit('/c', 1)[1])}] {s['text']}" for s in item["sentences"])
            if "canonical" in item:
                text += f" (main volume: {item['canonical']['ref']})"
            if item["kind"] == "hasiye":
                text = f"> Commentary by {item['commentary_by']}: {text}" if "commentary_by" in item else f"> Hâşiye: {text}"
            lines += [text, ""]
    if section["next_cursor"]:
        lines.append(f"[Continues; read the rest with read_section(cursor={section['next_cursor']!r}).]")
    return "\n".join(lines).strip() + "\n"


# ---------------------------------------------------------------- sunucu

STATIC_DIR = Path(__file__).parent / "static"
STATIC = {"/icon.png": ("icon.png", "image/png"), "/icon.svg": ("icon.svg", "image/svg+xml"),
          "/favicon.ico": ("favicon.ico", "image/x-icon")}


def _icons(public_url: str | None) -> list[Icon]:
    """Sunucunun ikonu (MCP `icons`, 2025-11-25): HTTP'de adresiyle, stdio'da gömülü (data: URI)."""
    if public_url:
        base = public_url.rstrip("/")
        return [Icon(src=f"{base}/icon.png", mime_type="image/png", sizes=["256x256"]),
                Icon(src=f"{base}/icon.svg", mime_type="image/svg+xml", sizes=["any"])]
    data = base64.b64encode((STATIC_DIR / "icon.png").read_bytes()).decode()
    return [Icon(src=f"data:image/png;base64,{data}", mime_type="image/png", sizes=["256x256"])]


def _static(name: str, media: str):
    body = (STATIC_DIR / name).read_bytes()

    async def endpoint(_request) -> Response:
        return Response(body, media_type=media, headers={"Cache-Control": "public, max-age=86400"})
    return endpoint


def create_server(library: Library, public_url: str | None = None, store: AuthStore | None = None,
                  anonymous: bool = False, anonymous_semantic: int = ANON_SEMANTIC_PER_DAY) -> MCPServer:
    """`public_url` verilirse sunucu OAuth ile korunur (giriş sayfası `/login`) ve her istek kaydedilir.
    `anonymous`: hesapsızlar da kullanır (`http_app` kapıyı kurar); anlamsal aramaları günde `anonymous_semantic`
    ile sınırlıdır, hesabı olan `sign_in` aracıyla giriş yapar."""
    protected = {}
    if public_url:
        store = store or AuthStore()
        provider = Provider(store, public_url)
        protected = {"auth": auth_settings(public_url), "auth_server_provider": provider,
                     "middleware": [usage_middleware(store)]}
    server = MCPServer(NAME, title="Risale-i Nur", instructions=INSTRUCTIONS,
                       description="Sentence-level, citable access to the works of Bediüzzaman Said Nursî.",
                       icons=_icons(public_url), **protected)
    for path, (name, media) in STATIC.items():               # ikon: istemciler sunucu adresinden de alabilir
        server.custom_route(path, methods=["GET"], include_in_schema=False)(_static(name, media))
    if public_url:
        server.custom_route("/login", methods=["GET", "POST"], include_in_schema=False)(login_endpoint(provider))
    citations = CitationChecker(library)

    @server.tool(annotations=READ_ONLY)
    def list_works(
        group: Annotated[str | None, Field(description="Only this group: eski-said, ana-cilt, mecmua or hizb.")] = None,
    ) -> str:
        """List the works with their ids, groups and sizes. Works whose text could not be found are listed as
        not available."""
        with _tool_errors():
            return _json(library.works(group))

    @server.tool(annotations=READ_ONLY)
    def get_outline(
        section: Annotated[str, Field(description="A work id (e.g. 'sozler') or a section id (e.g. 'sozler/10').")],
        depth: Annotated[int, Field(description="How many levels of subsections to include.", ge=0, le=6)] = 2,
    ) -> str:
        """Show the heading tree of a work or section: ids, titles, subtitles and the number of sentences under each
        section. Sections cut off by the depth limit show their number of subsections."""
        with _tool_errors():
            return _json(library.outline(section, depth))

    @server.tool(annotations=READ_ONLY)
    def read_section(
        section: Annotated[str, Field(description="A section id from get_outline or a search result's ref path.")],
        cursor: Annotated[str | None, Field(description="next_cursor from the previous call, to continue.")] = None,
        max_words: Annotated[int, Field(description="Approximate size of one page.", ge=200, le=8000)] = 1500,
    ) -> str:
        """Read a section and its subsections in book order. Returns headings (with refs), paragraphs as lists of
        sentences (id and text), verses a heading's section links to (linked_verses: kind and evidence sentence;
        mention them only when verses matter to the question),
        the author's hâşiyes (hasiye_of: the sentence they belong to; with commentary_by, another person's
        commentary, not the author's), the publisher's
        translations and sources of quoted verses and hadiths, and gaps where the source lacks text. Long sections
        come in pages: pass next_cursor back to continue."""
        with _tool_errors():
            return _json(library.read_section(section, cursor, max_words))

    @server.tool(annotations=READ_ONLY)
    def get_passage(
        id: Annotated[str, Field(description="A sentence id, or a range 'first_id..last_id' (the last may be short: "
                                             "'sozler/10/c010..c015').")],
        context: Annotated[int, Field(description="Neighbouring sentences to add on each side.", ge=0, le=20)] = 0,
    ) -> str:
        """Get sentences with their ref, incipit and text, the hâşiyes attached to them, and the publisher's
        translation of quoted verses. Use it to check a quotation or to fetch the exact citation of a sentence. For a
        range of up to 8 sentences in one section it also returns cite_as, the reference to show for all of them. A
        range that runs past the end of its section stops at the section's last sentence (see note)."""
        with _tool_errors():
            return _json(library.passage(id, context))

    @server.tool(annotations=READ_ONLY)
    def search(
        query: Annotated[str, Field(description="Words (all must occur), \"exact phrase\", prefix*, OR, -exclude, "
                                                "NEAR(a b, 5). Marks and Turkish letters are optional.")],
        work: Annotated[str | None, Field(description="Only this work id.")] = None,
        group: Annotated[str | None, Field(description="Only this group: eski-said, ana-cilt, mecmua or hizb.")] = None,
        limit: Annotated[int, Field(ge=1, le=50)] = 20,
        offset: Annotated[int, Field(ge=0)] = 0,
    ) -> str:
        """Search all works sentence by sentence, best matches first. Returns the total, the number of matches per
        work, matching section titles, and sentences with id, ref and incipit. Read the context of a result with
        get_passage or read_section before relying on it."""
        with _tool_errors():
            return _json(library.search(query, work, group, limit, offset))

    @server.tool(annotations=READ_ONLY)
    def semantic_search(
        query: Annotated[str, Field(description="A question or concept in your own (today's) words, e.g. "
                                                "'Ölüm neden bir nimettir?' or 'ümitsizlik'.")],
        work: Annotated[str | None, Field(description="Only this work id.")] = None,
        group: Annotated[str | None, Field(description="Only this group: eski-said, ana-cilt, mecmua or hizb.")] = None,
        limit: Annotated[int, Field(ge=1, le=50)] = 10,
        offset: Annotated[int, Field(ge=0)] = 0,
    ) -> str:
        """Find passages by meaning rather than by exact words: the sentences closest in meaning to the query (id,
        ref, incipit, similarity) and the sections where the topic concentrates. Use it for concepts and questions;
        the text often says the same thing with other, older words. For exact words, phrases or terms use search.
        Read the context of a result with get_passage or read_section before relying on it."""
        with _tool_errors():
            if anonymous and get_access_token() is None \
                    and store.anonymous_calls("semantic_search", start_of_day()) >= anonymous_semantic:
                raise ToolError("The daily limit of semantic searches for users without an account is reached. "
                                "Use search with the text's own words instead. A user with an account can sign "
                                "in with the sign_in tool for unlimited use.")
            return _json(library.semantic_search(query, work, group, limit, offset))

    if anonymous:
        @server.tool(annotations=READ_ONLY)
        def sign_in() -> str:
            """Sign in to this server with an account (only if the user asks to sign in or has an account): without
            an account, semantic_search has a shared daily limit. Calling this without being signed in makes Claude
            show the user a sign-in card; afterwards it reports who is signed in."""
            token = get_access_token()
            return _json({"signed_in_as": token.subject if token else None})

    @server.tool(annotations=READ_ONLY)
    def find_sentence(
        incipit: Annotated[str, Field(description="The first words of the sentence, as the user quotes them.")],
        scope: Annotated[str | None, Field(description="Only inside this work or section id.")] = None,
    ) -> str:
        """Find a sentence from its opening words, e.g. when the user quotes a sentence or gives a reference like
        Dokuzuncu Hakikat › "Hiç mümkün müdür ki; ölmüş…". Marks are optional and the last word may be incomplete."""
        with _tool_errors():
            return _json(library.find_sentence(incipit, scope))

    @server.tool(annotations=READ_ONLY)
    def find_ayah(
        sura: Annotated[str, Field(description="Sura number (1–114) or name, e.g. '2' or 'Bakara'.")],
        ayah: Annotated[int | None, Field(description="Verse number; without it, every quoted verse of the sura.")] = None,
        limit: Annotated[int, Field(ge=1, le=50)] = 30,
        offset: Annotated[int, Field(ge=0)] = 0,
    ) -> str:
        """List where a Qur'anic verse (or any verse of a sura) is quoted in the works, with the sentence, the
        Arabic as quoted, the publisher's translation and its source. via 'source': the edition marks it as a
        verse; via 'text': an unmarked quotation found in the Qur'an's text (Hizbs, el-Mesnevî el-Arabî). check
        warns when the quoted words differ from the named verse. For one verse it also returns the verse itself
        (quran), as get_ayah does, and links: the places that tie themselves to the verse, by kind, strength
        and evidence sentence (strong first; see the instructions on how to name them)."""
        with _tool_errors():
            return _json(library.find_ayah(sura, ayah, limit, offset))

    @server.tool(annotations=READ_ONLY)
    def get_ayah(
        sura: Annotated[str, Field(description="Sura number (1–114) or name, e.g. '2' or 'Bakara'.")],
        ayah: Annotated[int, Field(description="Verse number.", ge=1)],
        end: Annotated[int | None, Field(description="Last verse of a range (at most 30 verses).", ge=1)] = None,
        context: Annotated[int, Field(description="Neighbouring verses to add on each side.", ge=0, le=10)] = 0,
    ) -> str:
        """Get a verse (or a range) of the Qur'an itself: the fully vowelled Arabic text (Medina Mushaf script),
        the Diyanet İşleri Başkanlığı and Türkiye Diyanet Vakfı translations, the ref to cite ("Bakara Sûresi,
        2:255"), how often each verse is quoted in the works and how many places link to it (linked_in_works;
        find_ayah lists both). A translation that
        renders several verses together says which (covers_verses); ask for that range to read it whole."""
        with _tool_errors():
            return _json(library.ayahs(sura, ayah, end, context))

    @server.tool(annotations=READ_ONLY)
    def verify_citations(
        text: Annotated[str, Field(description="Your draft answer, or the lines of it that contain references.")],
    ) -> str:
        """Check the references in a draft answer against the works before you send it. Finds every
        "Work › Section › “opening words”" reference (also "… ile başlayan N cümle" for consecutive sentences, or
        "› 12. cümle") and reports, for each, whether the section exists, the quoted words start a sentence there,
        a range stays within 8 sentences of its section, and the block quote next to it is in the cited sentences.
        Flagged references come with a problem and, where possible, the full reference to use instead or where
        the quoted words really occur. Pass the whole draft so that block quotes are checked too."""
        with _tool_errors():
            return _json(summary(citations.check(text)))

    # ------------------------------------------------------------ kaynaklar (kullanıcının eklediği bağlam)

    @server.resource("risale://works", name="works", mime_type="text/markdown",
                     description="All works with their ids.")
    def works_resource() -> str:
        return _works_markdown(library.works())

    @server.resource("risale://outline/{work}", name="outline", mime_type="text/markdown",
                     description="The full heading tree of a work.")
    def outline_resource(work: str) -> str:
        outline = library.outline(work, depth=20)
        return f"# {outline['ref']}\n\n" + "\n".join(_outline_markdown(outline)) + "\n"

    @server.resource("risale://text/{+section}", name="text", mime_type="text/markdown",
                     description="The text of a section with numbered sentences, e.g. risale://text/sozler/10.")
    def text_resource(section: str) -> str:
        return _section_markdown(library.read_section(section, max_words=RESOURCE_TEXT_WORDS))

    # ------------------------------------------------------------ hazır komutlar

    @server.prompt(title="Topic survey")
    def topic_survey(topic: str, scope: str = "") -> str:
        """Where a topic is treated across the works, grouped by work, with citations."""
        where = f" Limit the survey to {scope}." if scope else ""
        return (
            f"Survey where the topic “{topic}” is treated in the works.{where}\n"
            "1. Find the passages with semantic_search (the topic as a concept and as a question; its sections show "
            "where it concentrates) and with search for the text's own terms (Ottoman and modern spellings, word "
            "beginnings with *; by_work shows the spread).\n"
            "2. For the main passages, read enough context (get_passage with context, or read_section) to be sure "
            "the passage is really about the topic.\n"
            "3. Report the places grouped by work, in the works' order: for each, the reference with the incipit "
            "and one sentence on what is said there. Mark the central treatments.\n"
            "4. End with what you could not find or what remains uncertain."
        )

    @server.prompt(title="Text and commentary")
    def text_and_commentary(question: str) -> str:
        """Answer a question in two parts: what the text says, then interpretation."""
        return (
            f"Question: {question}\n"
            "Answer under two headings.\n"
            "## What the text says — only what the works say, as close quotations or paraphrases, each with its "
            "reference (section path and incipit). Search and read the passages first.\n"
            "## Commentary — your interpretation and synthesis, clearly marked as yours; tie each point to the "
            "passages above. If perspectives differ, give each with the sentences it rests on."
        )

    @server.prompt(title="Discussion partner")
    def discuss(topic: str) -> str:
        """Think through a topic together, grounded in the text."""
        return (
            f"Let us think through “{topic}” together, as in a müzakere (study circle).\n"
            "Find the relevant passages first and keep every step tied to them. Ask me questions, offer readings "
            "of the text and test them against other passages; point out where the text is silent. Keep "
            "quotations and your own views apart, and cite with section path and incipit."
        )

    @server.prompt(title="Self test")
    def self_test(section: str) -> str:
        """Quiz the user on a section and check the answers against the text."""
        return (
            f"Quiz me on the section {section}.\n"
            "Read the section with read_section (all pages). Ask one question at a time about its arguments, "
            "examples and terms, in order. After each answer, check it against the text, quote the relevant "
            "sentence with its reference, then ask the next question. At the end, summarise what to reread."
        )

    @server.prompt(title="Lesson plan")
    def lesson_plan(subject: str) -> str:
        """Prepare a cited lesson plan on a topic or section."""
        return (
            f"Prepare a lesson (ders) on: {subject}.\n"
            "If it is a section id, read it; if it is a topic, search for its main passages first. Give the plan as: "
            "aim; the passages to read aloud (references with incipits, in order); the main points of each passage "
            "with the sentences they rest on; difficult words and their meaning in context; questions for "
            "discussion. Do not include anything the text does not support."
        )

    return server


def http_security(public_url: str) -> TransportSecuritySettings:
    """DNS rebinding koruması: tünel isteği dış adresin Host başlığıyla iletir, o da izinlidir."""
    host = urlparse(public_url).netloc
    return TransportSecuritySettings(
        enable_dns_rebinding_protection=True, allowed_hosts=[host, "127.0.0.1:*", "localhost:*"],
        allowed_origins=[f"https://{host}", "https://claude.ai", "https://claude.com",
                         "http://127.0.0.1:*", "http://localhost:*"])


def http_app(server: MCPServer, public_url: str, anonymous: bool = False) -> Starlette:
    """OAuth'lu HTTP uygulaması; `anonymous` ise `/mcp` önüne hesapsız erişim kapısı (`auth.AnonymousGate`) konur."""
    app = server.streamable_http_app(transport_security=http_security(public_url))
    if anonymous:
        for route in app.router.routes:
            if getattr(route, "path", None) == "/mcp" and isinstance(route.app, RequireAuthMiddleware):
                metadata = str(build_resource_metadata_url(server.settings.auth.resource_server_url))
                route.app = AnonymousGate(route.app, route.app.app, metadata)
                break
        else:
            raise RuntimeError("/mcp route not found")
    return app


def main() -> None:
    if sys.argv[1:2] == ["auth"]:
        auth_main(sys.argv[2:])
        return
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--db", type=Path, default=DB_PATH, help="veritabanı dosyası")
    parser.add_argument("--transport", choices=("stdio", "streamable-http"), default="stdio")
    parser.add_argument("--host", default="127.0.0.1", help="HTTP için dinlenen adres (tünel aynı makinede)")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--public-url", help="HTTP: sunucunun dışarıdan adresi (https://…); OAuth'u açar")
    parser.add_argument("--no-auth", action="store_true", help="HTTP: kimlik doğrulamasız, yalnızca 127.0.0.1")
    parser.add_argument("--anonymous", action="store_true",
                        help="HTTP + --public-url: hesapsızlar da kullanır (anlamsal arama sınırlı), hesaplılar sınırsız")
    parser.add_argument("--anonymous-semantic", type=int, default=ANON_SEMANTIC_PER_DAY,
                        help="hesapsızların günlük toplam anlamsal arama sınırı")
    args = parser.parse_args()
    load_env()                                    # VOYAGE_API_KEY: proje klasöründeki .env
    library = Library(args.db)
    library.conn                                  # veritabanı yoksa başlarken açık hata
    if args.transport == "stdio":
        create_server(library).run("stdio")
        return
    if not (args.public_url or args.no_auth):
        sys.exit("HTTP için --public-url https://… (OAuth) ya da --no-auth (yalnızca bu bilgisayar) verin.")
    if args.no_auth and args.host != "127.0.0.1":
        sys.exit("--no-auth yalnızca 127.0.0.1'de çalışır: metinler kimlik doğrulamasız dışarı açılmaz.")
    security = None
    if args.public_url:
        if not args.public_url.startswith("https://"):
            sys.exit("--public-url https:// ile başlamalı.")
        if not AuthStore().users():
            sys.exit("Henüz hesap yok: önce `risale-mcp auth add-user <ad>`.")
        security = http_security(args.public_url)
    if args.no_auth:
        create_server(library).run("streamable-http", host=args.host, port=args.port, transport_security=security)
        return
    if args.anonymous and not args.public_url:
        sys.exit("--anonymous yalnızca --public-url ile kullanılır.")
    server = create_server(library, args.public_url, anonymous=args.anonymous,
                           anonymous_semantic=args.anonymous_semantic)
    uvicorn.run(http_app(server, args.public_url, args.anonymous), host=args.host, port=args.port)


if __name__ == "__main__":
    main()
