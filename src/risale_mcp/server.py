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
import threading
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
from pydantic import BaseModel, Field
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
from risale_mcp.citations import CitationChecker
from risale_mcp.db import DatabaseError
from risale_mcp.env import load_env
from risale_mcp.library import Library, LibraryError
from risale_mcp.paths import DB_PATH

NAME = "risale"
RESOURCE_TEXT_WORDS = 20000      # kaynak olarak eklenen bölüm metninin üst sınırı

INSTRUCTIONS = """\
Read access to the complete works of Bediüzzaman Said Nursî (the Risale-i Nur volumes, the early works, the \
compilations (mecmua), the Hizbs, and the works he wrote in Arabic with their Turkish translations) and to the \
Qur'an. Texts are split into sentences with stable ids.

Workflow:
1. Find: semantic_search for concepts and questions in today's words (the text often uses older words); search \
for the text's own words, names and terms. Results are candidates, not evidence.
2. Read what you will rely on, in context: get_passage (a sentence or a range first..last, with context) or \
read_section.
3. Before writing the answer, call cite once with every sentence or range you quote or rely on, and the exact \
words you quote. Use the cite_as it returns and fix what it flags.

Answering:
1. Every statement about the works rests on text you read. Never invent references, ids, quotations or titles; \
if the tools do not return something, say you could not find it in the works.
2. Quote the works only in block quotes on their own line (> "…"), exactly as returned; in your prose put \
quotation marks around at most a single term. A parable or one line of thought running over consecutive \
sentences of one section is quoted as one block with one source (a range, at most 8 sentences).
3. References are cite_as, written exactly: the full path from the work and the opening words, never shortened, \
never a sentence number. With one or two references, put each on its own line right after its quotation. With \
more, end each quotation (and each claim drawn from a source) with its number, e.g. [1], and finish the answer \
with a "Kaynaklar" list: one line per source, the bibliography cite returns.
4. Keep what the text says apart from your own interpretation, under separate headings. Answer in the user's \
language.

Layers that are not the author's words:
- Translations of verses and hadiths in the works (publisher_translation) are the publishers'. Use them only to \
convey the meaning, say whose they are, never quote them as the text. The author's own explanation ("Yani, …") \
is text.
- Qur'an: copy the vowelled Arabic from get_ayah (or as the works quote it), never from memory. Cite a verse as \
get_ayah's ref ("Bakara Sûresi, 2:255", no ›), name the Diyanet translation you use and mention covers_verses. \
A translation aids the meaning; it does not replace the Arabic.
- Verse links (find_ayah links, read_section linked_verses) were found by rules, not verdicts: never call a \
passage the tafsir of a verse; give the link's kind and evidence sentence; a weak link is one sentence's \
reference, not the section's topic. Bring verses up only when they matter to the question.
- The Turkish versions of works the author wrote in Arabic are translations (parallel ids: isaratul-icaz-arabi/… \
↔ isaratul-icaz/…). Sections marked as İhsan Kasım's translation render Turkish originals: quote the original. \
In Kızıl İcaz, "quote" paragraphs are Ahdarî's verses; commentary_by marks Abdülmecid Nursî's commentary, \
cite it as his. Check subtitles and paragraph kinds.
- Compilations reuse main-volume text: cite the main volume's sentences they return.
"""


class Source(BaseModel):
    id: str = Field(description="A sentence id, or a range 'first_id..last_id' (the last may be short: "
                                "'sozler/10/c010..c015'), as the tools return them.")
    quote: str | None = Field(default=None, description="The words you quote from it, exactly as you will show them "
                                                         "(… for omitted parts); leave out if you only paraphrase.")


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


def _warm(library: Library, citations: CitationChecker) -> None:
    """Dizinleri ilk aramadan önce kurar: anlamsal aramanın eşlemesi (sunucuda ≈1,6 sn) ve başlık ağacı."""
    citations.refresh()
    try:
        library._semantic_index()
    except Exception:                    # vektör yoksa araç çağrılınca açıklamalı hata verir
        pass


def create_server(library: Library, public_url: str | None = None, store: AuthStore | None = None,
                  anonymous: bool = False, anonymous_semantic: int = ANON_SEMANTIC_PER_DAY,
                  warm: bool = False) -> MCPServer:
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
    if warm:
        threading.Thread(target=_warm, args=(library, citations), daemon=True).start()

    @server.tool(annotations=READ_ONLY, structured_output=False)
    def list_works(
        group: Annotated[str | None, Field(description="Only this group: eski-said, ana-cilt, mecmua or hizb.")] = None,
    ) -> str:
        """List the works with their ids, groups and sizes. Works whose text could not be found are listed as
        not available."""
        with _tool_errors():
            return _json(library.works(group))

    @server.tool(annotations=READ_ONLY, structured_output=False)
    def get_outline(
        section: Annotated[str, Field(description="A work id (e.g. 'sozler') or a section id (e.g. 'sozler/10').")],
        depth: Annotated[int, Field(description="How many levels of subsections to include.", ge=0, le=6)] = 2,
    ) -> str:
        """Show the heading tree of a work or section: ids, titles, subtitles and the number of sentences under each
        section. Sections cut off by the depth limit show their number of subsections."""
        with _tool_errors():
            return _json(library.outline(section, depth))

    @server.tool(annotations=READ_ONLY, structured_output=False)
    def read_section(
        section: Annotated[str, Field(description="A section id from get_outline or a search result's ref path.")],
        cursor: Annotated[str | None, Field(description="next_cursor from the previous call, to continue.")] = None,
        max_words: Annotated[int, Field(description="Approximate size of one page.", ge=200, le=8000)] = 1500,
    ) -> str:
        """Read a section and its subsections in book order: headings (ref; linked_verses: verses the section
        links to), paragraphs as sentences (id, text), the author's hâşiyes (hasiye_of: their sentence;
        commentary_by: someone else's commentary), the publisher's translations of quoted verses and hadiths, and
        gaps where the source lacks text. Long sections come in pages: pass next_cursor back to continue."""
        with _tool_errors():
            return _json(library.read_section(section, cursor, max_words))

    @server.tool(annotations=READ_ONLY, structured_output=False)
    def get_passage(
        id: Annotated[str, Field(description="A sentence id, or a range 'first_id..last_id' (the last may be short: "
                                             "'sozler/10/c010..c015').")],
        context: Annotated[int, Field(description="Neighbouring sentences to add on each side.", ge=0, le=20)] = 0,
    ) -> str:
        """Get sentences (or a range) with their text, attached hâşiyes and the publisher's translations of quoted
        verses, optionally with neighbouring sentences. A range of up to 8 sentences in one section also returns
        cite_as, its reference. A range past the end of its section stops at its last sentence (see note)."""
        with _tool_errors():
            return _json(library.passage(id, context))

    @server.tool(annotations=READ_ONLY, structured_output=False)
    def search(
        query: Annotated[str, Field(description="Words (all must occur), \"exact phrase\", prefix*, OR, -exclude, "
                                                "NEAR(a b, 5). Marks and Turkish letters are optional.")],
        work: Annotated[str | None, Field(description="Only this work id.")] = None,
        group: Annotated[str | None, Field(description="Only this group: eski-said, ana-cilt, mecmua or hizb.")] = None,
        limit: Annotated[int, Field(ge=1, le=50)] = 20,
        offset: Annotated[int, Field(ge=0)] = 0,
    ) -> str:
        """Search all works sentence by sentence by the text's own words, best matches first: the total, matches
        per work, matching section titles, and sentences (id, cite_as, text). Read a result in context before
        relying on it."""
        with _tool_errors():
            return _json(library.search(query, work, group, limit, offset))

    @server.tool(annotations=READ_ONLY, structured_output=False)
    def semantic_search(
        query: Annotated[str, Field(description="A question or concept in your own (today's) words, e.g. "
                                                "'Ölüm neden bir nimettir?' or 'ümitsizlik'.")],
        work: Annotated[str | None, Field(description="Only this work id.")] = None,
        group: Annotated[str | None, Field(description="Only this group: eski-said, ana-cilt, mecmua or hizb.")] = None,
        limit: Annotated[int, Field(ge=1, le=50)] = 10,
        offset: Annotated[int, Field(ge=0)] = 0,
    ) -> str:
        """Find passages by meaning: the sentences closest to the query (id, cite_as, text, similarity) and the
        sections where the topic concentrates. For concepts and questions; the text often uses other, older words.
        For exact words, phrases or terms use search. Read a result in context before relying on it."""
        with _tool_errors():
            if anonymous and get_access_token() is None \
                    and store.anonymous_calls("semantic_search", start_of_day()) >= anonymous_semantic:
                raise ToolError("The daily limit of semantic searches for users without an account is reached. "
                                "Use search with the text's own words instead. A user with an account can sign "
                                "in with the sign_in tool for unlimited use.")
            return _json(library.semantic_search(query, work, group, limit, offset))

    if anonymous:
        @server.tool(annotations=READ_ONLY, structured_output=False)
        def sign_in() -> str:
            """Sign in to this server with an account (only if the user asks to sign in or has an account): without
            an account, semantic_search has a shared daily limit. Calling this without being signed in makes Claude
            show the user a sign-in card; afterwards it reports who is signed in."""
            token = get_access_token()
            return _json({"signed_in_as": token.subject if token else None})

    @server.tool(annotations=READ_ONLY, structured_output=False)
    def find_sentence(
        incipit: Annotated[str, Field(description="The first words of the sentence, as the user quotes them.")],
        scope: Annotated[str | None, Field(description="Only inside this work or section id.")] = None,
    ) -> str:
        """Find a sentence from its opening words, e.g. when the user quotes a sentence or gives a reference like
        Dokuzuncu Hakikat › "Hiç mümkün müdür ki; ölmüş…". Marks are optional and the last word may be incomplete."""
        with _tool_errors():
            return _json(library.find_sentence(incipit, scope))

    @server.tool(annotations=READ_ONLY, structured_output=False)
    def find_ayah(
        sura: Annotated[str, Field(description="Sura number (1–114) or name, e.g. '2' or 'Bakara'.")],
        ayah: Annotated[int | None, Field(description="Verse number; without it, every quoted verse of the sura.")] = None,
        limit: Annotated[int, Field(ge=1, le=50)] = 30,
        offset: Annotated[int, Field(ge=0)] = 0,
    ) -> str:
        """List where a Qur'anic verse (or any verse of a sura) is quoted in the works: the sentence, the Arabic
        as quoted, the publisher's translation and source. via 'source': marked as a verse by the edition; via
        'text': an unmarked quotation found in the Qur'an's text. check warns when the words differ from the
        named verse. For one verse it also returns the verse (quran) and links: places that tie themselves to it,
        strong first, each with its evidence sentence. Link kinds: isaret (the text says it points to, alludes to
        or explains the verse), acilis (the section opens with it), izah (the author's "Yani…" explanation; in
        works he wrote in Arabic the Turkish wording is the translator's), dayanak (the text relies on it: "…
        sırrınca"), risale (the verse's allusion to the Risale-i Nur)."""
        with _tool_errors():
            return _json(library.find_ayah(sura, ayah, limit, offset))

    @server.tool(annotations=READ_ONLY, structured_output=False)
    def get_ayah(
        sura: Annotated[str, Field(description="Sura number (1–114) or name, e.g. '2' or 'Bakara'.")],
        ayah: Annotated[int, Field(description="Verse number.", ge=1)],
        end: Annotated[int | None, Field(description="Last verse of a range (at most 30 verses).", ge=1)] = None,
        context: Annotated[int, Field(description="Neighbouring verses to add on each side.", ge=0, le=10)] = 0,
    ) -> str:
        """Get a verse (or a range) of the Qur'an itself: the vowelled Arabic (Medina Mushaf), the Diyanet İşleri
        Başkanlığı and Türkiye Diyanet Vakfı translations, the ref to cite ("Bakara Sûresi, 2:255"), and how often
        the works quote it and link to it (find_ayah lists them). A translation of several verses together says
        which (covers_verses); ask for that range to read it whole."""
        with _tool_errors():
            return _json(library.ayahs(sura, ayah, end, context))

    @server.tool(annotations=READ_ONLY, structured_output=False)
    def cite(
        sources: Annotated[list[Source], Field(description="The sentences you quote or rely on, in the order of "
                                                           "their numbers in your answer ([1], [2]…).",
                                               min_length=1, max_length=50)],
    ) -> str:
        """Get the references to show for the passages you use, checked against the works. Call it once before
        writing the answer, with every sentence or range you quote or rely on and the words you quote. Returns,
        for each source, cite_as (the full reference to show), a problem to fix if any (a range longer than 8
        sentences or past its section, quoted words that are not in those sentences, with where they occur), and
        the bibliography lines "[n] cite_as" for the answer's Kaynaklar list."""
        with _tool_errors():
            return _json(citations.sources([source.model_dump() for source in sources]))

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
        create_server(library, warm=True).run("stdio")
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
        create_server(library, warm=True).run("streamable-http", host=args.host, port=args.port, transport_security=security)
        return
    if args.anonymous and not args.public_url:
        sys.exit("--anonymous yalnızca --public-url ile kullanılır.")
    server = create_server(library, args.public_url, anonymous=args.anonymous,
                           anonymous_semantic=args.anonymous_semantic, warm=True)
    uvicorn.run(http_app(server, args.public_url, args.anonymous), host=args.host, port=args.port)


if __name__ == "__main__":
    main()
