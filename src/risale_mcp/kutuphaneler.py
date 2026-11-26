"""S13.17: sohbetin öbür kütüphaneleri (hadis, tefsir, klasik).

Kullanıcının kararları (2026-11-26, `PLANLAR.md` S13.17):

- **Erişim ölçülerek seçildi** (`data/interim/sohbet/erisim-olcumu-20261126.md`): Risale sohbetin sürecinde kalır
  (`sohbet.Chat`), öbürleri MCP sunucularından çağrılır. Süreç içi tefsir ≈1,26 GB tutuyor ve veri MCP servisleriyle
  iki kez durur; makineler arası çağrı ≈90 ms ekler. Adres ayardandır (`SOHBET_<AD>_URL`, iç erişim adresiyle:
  `auth internal-key --new sohbet`, sınırsız ve girdisiz kayıtlı). Adres verilmemişse ve profilin veritabanı bu
  makinedeyse kütüphane süreç içinde açılır (yerel geliştirme, testler); ikisi de yoksa kütüphane yoktur.
  Hepsi ileride tek makineye taşınırsa yalnız adresler değişir.
- **Okuyucu seçer**, ama altyapı dördünün birlikte açık olmasına da uygundur: seçim sorunun bir parametresidir
  (`libraries`), varsayılan yalnız Risale. Seçilen kütüphanenin araçları alan önekiyle modele gider
  (`tefsir_find_ayah`); açıklamanın başında kütüphanenin adı durur. `cite` gitmez (Kaynaklar'ı sayfa kurar),
  `get_ayah` da gitmez (Kur'ân ortak adrestir, Risale'nin `get_ayah`'ı aynı metni ve meali verir).
- **İşaret:** model öbür kütüphanenin cümlesini ya da rivayetini alan adıyla işaretler (`[[tefsir:ibnkesir/2/255/c001]]`,
  `[[hadis:bukhari/1]]`); sayfa alıntıyı o kütüphanenin `cite`'ıyla denetler (`verify`), Kaynaklar tek listedir.
- **Hassas alanlar** (S13.14'ün kararı): hadiste cevap ağırlıkla rivayet, künye ve kitabın verdiği derecedir; serbest
  yorum dardır, hüküm verilmez.

Uzak çağrı MCP'nin streamable-http'sidir, en sade biçimiyle (`Remote`): bir kez `initialize`, oturum kimliği
saklanır, her araç çağrısı tek POST; oturum düşerse bir kez yeniden açılır. SDK'nın istemci oturumu uzun ömürlü bir
sunucuda görev sınırlarına bağlı kaldığı için kullanılmaz.
"""

import asyncio
import json
import os
import re
from dataclasses import dataclass, field

MAX_RESULT = 40_000          # öbür kütüphanenin bir araç sonucunun modele giden en çok karakteri
DROPPED_TOOLS = {"cite", "get_ayah"}
TIMEOUT = 60.0


@dataclass(frozen=True)
class Kutuphane:
    id: str                  # işaretin ve aracın öneki
    title: str               # sayfadaki adı
    label: str               # talimattaki ve araç açıklamasındaki adı
    profile: str             # süreç içi açılışın profili (`profiles.py`)
    host: str                # MCP sunucusunun Host adı (iç adreste de bu ad beklenir)
    hint: str                # sayfadaki açıklama
    rules: str               # talimata eklenen kurallar
    reading: dict = field(default_factory=dict)     # araç -> durum satırı


TEFSIR_RULES = """\
Tafsir Library (tools tefsir_…): classical works of Qur'anic exegesis in their original Arabic (al-Tabari, \
al-Maturidi, al-Zamakhshari, al-Razi, al-Qurtubi, al-Baydawi, al-Nasafi, Ibn Kathir, al-Jalalayn, al-Suyuti's \
al-Durr al-Manthur, Abu al-Su'ud, Isma'il Haqqi Bursawi, al-Alusi), each divided into verse units. For a verse, \
tefsir_find_ayah gives, for each work in the order of its author's death, the unit that treats it and its places in \
the Risale-i Nur first; read a unit with tefsir_read_section or tefsir_get_passage before relying on it. Each work \
belongs to its author: name him. A section with layer is another person's text (the editor's introduction). Two \
works treating the same verse is not a relation: never say one follows, quotes, agrees with or rejects another \
unless tefsir_text_links records it; a relation you notice yourself is your interpretation. A classical tafsir may \
be called tafsir; your own summary or comparison never is."""

HADIS_RULES = """\
Hadith Library (tools hadis_…): hadith collections in their original Arabic (the Six Books and the Muwatta, Ahmad's \
Musnad, al-Darimi, al-Mustadrak with al-Dhahabi's notes, Ibn Hibban with al-Albani's grading, Majma' al-Zawa'id, \
Kanz al-'Ummal, Fayd al-Qadir, Kashf al-Khafa, al-Shifa, Dala'il al-Nubuwwa); the unit is the report (id \
bukhari/1, musned/14870). Read a report with hadis_get_hadith before relying on it, and mark every claim drawn \
from a report (a grade, a scholar's note, where it is) with that report's id. Never rule on a report's \
soundness yourself: give grades only as the tools hold them, with the scholar's name; layers are other scholars' \
notes, never the book author's. A match in Kashf al-Khafa (book_note) means the saying is discussed there, not that \
it is sound. A narrator's or scholar's explanation inside a report is theirs, not the Prophet's words. This is a \
sensitive field: keep your own interpretation short; the answer is mostly the reports, where they are, and their \
grades as the books give them. Never give a legal ruling. To ask how a hadith in the Risale-i Nur is sourced, use \
find_hadith (Risale tools) first."""

KLASIK_RULES = """\
Classical Islamic Library (tools klasik_…): the classical works the Risale-i Nur refers its reader to and relies \
on, in their original Arabic: al-Fiqh al-Akbar, al-Jurjani's Dala'il al-I'jaz and Asrar al-Balagha, al-Raghib's \
al-Mufradat, al-Ghazali's al-Munqidh and Ihya' (with al-'Iraqi's takhrij as commentary), al-Sakkaki's Miftah \
al-'Ulum, al-Taftazani's al-Talwih and Sharh al-Maqasid, al-Sayyid al-Sharif's al-Ta'rifat and Sharh al-Mawaqif, \
al-Qastallani's al-Mawahib. klasik_list_works gives, for each work, risale_refs: the places where the Risale-i Nur \
names it, with their kind (havale, nakil, degerlendirme). Each work belongs to its author; a section with layer is \
another person's text (in Sharh al-Mawaqif the base text by al-Iji); commentary_by in al-Ihya is al-'Iraqi's, not \
al-Ghazali's. Section titles are the edition's. A rhetorical point you derive yourself is your interpretation."""

KUTUPHANELER = {
    "tefsir": Kutuphane("tefsir", "Tefsir", "Tafsir Library", "tefsir", "tefsir.risalemcp.com",
                        "Klasik tefsirler (Taberî, Râzî, Beyzâvî, Âlûsî…), Arapça aslından", TEFSIR_RULES,
                        {"find_ayah": "Tefsirlerde {ayah} âyetinin birimleri aranıyor",
                         "read_section": "Tefsirde {section} okunuyor", "get_passage": "Tefsirde okunuyor",
                         "search": "Tefsirlerde “{query}” aranıyor",
                         "semantic_search": "Tefsirlerde “{query}” anlamına yakın yerler aranıyor"}),
    "hadis": Kutuphane("hadis", "Hadis", "Hadith Library", "hadis", "hadis.risalemcp.com",
                       "Hadis kitapları (Kütüb-i Sitte, Müsned, Müstedrek…), Arapça aslından", HADIS_RULES,
                       {"get_hadith": "Hadis kitabında {id} okunuyor",
                        "search_hadith": "Hadis kitaplarında “{query}” aranıyor",
                        "semantic_search": "Hadis kitaplarında “{query}” anlamına yakın rivayetler aranıyor",
                        "find_by_citation": "Hadis kitaplarında “{citation}” künyesi aranıyor",
                        "read_chapter": "Hadis kitabında bir bâb okunuyor"}),
    "klasik": Kutuphane("klasik", "Klasik eserler", "Classical Islamic Library", "klasik", "klasik.risalemcp.com",
                        "Risale'nin havale ettiği klasikler (Delâil, Müfredât, İhyâ, Şerhu'l-Mevâkıf…)", KLASIK_RULES,
                        {"read_section": "Klasik eserde {section} okunuyor", "get_passage": "Klasik eserde okunuyor",
                         "search": "Klasik eserlerde “{query}” aranıyor",
                         "semantic_search": "Klasik eserlerde “{query}” anlamına yakın yerler aranıyor",
                         "list_works": "Klasik eserlerin listesine bakılıyor"}),
}
ORDER = ("tefsir", "hadis", "klasik")
MARK_PREFIX = re.compile(r"^(risale|tefsir|hadis|klasik):(.+)$")


def split_id(ident: str) -> tuple[str | None, str]:
    """`tefsir:ibnkesir/2/255/c001` -> ("tefsir", "ibnkesir/2/255/c001"); Risale'nin kimliği öneksizdir
    (modelin yazdığı `risale:` öneki atılır)."""
    m = MARK_PREFIX.match(ident)
    if not m:
        return None, ident
    return (None if m.group(1) == "risale" else m.group(1)), m.group(2)


def selected(value) -> tuple[str, ...]:
    """Okuyucunun seçimi, bilinen kütüphaneler sabit sırayla."""
    wanted = {str(v) for v in value} if isinstance(value, (list, tuple, set)) else set()
    return tuple(k for k in ORDER if k in wanted)


# ---------------------------------------------------------------- istemciler

class Unavailable(Exception):
    """Kütüphaneye ulaşılamıyor."""


class InProcess:
    """Profilin veritabanı bu makinedeyse kütüphane süreç içinde (yerel geliştirme, testler)."""

    def __init__(self, kutuphane: Kutuphane) -> None:
        self.kutuphane = kutuphane
        self._server = None
        self._lock = asyncio.Lock()      # aynı anda iki çağrı veritabanı bağlantısını paylaşmasın (deneme turları)

    def _open(self):
        if self._server is None:
            from risale_mcp.profiles import PROFILES
            from risale_mcp.server import create_server
            profile = PROFILES[self.kutuphane.profile]
            if self.kutuphane.profile == "hadis":
                from risale_mcp.hadis_library import HadisLibrary
                library = HadisLibrary(profile.db, profile.vectors)
            else:
                from risale_mcp.library import Library
                library = Library(profile.db, profile.vectors)
            library.conn
            self._server = create_server(library, profile=self.kutuphane.profile)
        return self._server

    async def list_tools(self) -> list[dict]:
        server = await asyncio.to_thread(self._open)
        return [{"name": t.name, "description": t.description or "", "input_schema": t.input_schema}
                for t in await server.list_tools()]

    async def call(self, name: str, args: dict) -> tuple[str, bool]:
        from mcp.server.mcpserver.exceptions import ToolError
        async with self._lock:
            server = await asyncio.to_thread(self._open)
            try:
                result = await server.call_tool(name, args)
            except ToolError as e:
                return str(e), True
        return "".join(getattr(c, "text", "") for c in result.content), bool(getattr(result, "is_error", False))


class Remote:
    """MCP sunucusu (streamable-http), iç erişim adresiyle."""

    def __init__(self, kutuphane: Kutuphane, url: str) -> None:
        self.kutuphane, self.url = kutuphane, url
        self.session: str | None = None
        self.version: str | None = None
        self._http = None
        self._lock = asyncio.Lock()
        self._next = 0

    def _client(self):
        if self._http is None:
            import httpx2
            self._http = httpx2.AsyncClient(timeout=TIMEOUT)
        return self._http

    def _headers(self) -> dict:
        h = {"Host": self.kutuphane.host, "Accept": "application/json, text/event-stream",
             "Content-Type": "application/json"}
        if self.session:
            h["Mcp-Session-Id"] = self.session
        if self.version:
            h["MCP-Protocol-Version"] = self.version
        return h

    async def _post(self, message: dict):
        try:
            response = await self._client().post(self.url, headers=self._headers(), content=json.dumps(message))
        except Exception as e:
            raise Unavailable(f"{self.kutuphane.id}: {type(e).__name__}") from None
        return response

    @staticmethod
    def _message(response, ident: int) -> dict:
        kind = response.headers.get("content-type", "")
        if kind.startswith("text/event-stream"):
            for block in response.text.split("\n\n"):
                data = "\n".join(line[5:].lstrip() for line in block.splitlines() if line.startswith("data:"))
                if data:
                    message = json.loads(data)
                    if message.get("id") == ident:
                        return message
            raise Unavailable("no response in the event stream")
        return response.json()

    async def _initialize(self) -> None:
        from mcp.types import LATEST_PROTOCOL_VERSION
        self.session = self.version = None
        self._next += 1
        ident = self._next
        response = await self._post({"jsonrpc": "2.0", "id": ident, "method": "initialize", "params": {
            "protocolVersion": LATEST_PROTOCOL_VERSION, "capabilities": {},
            "clientInfo": {"name": "risale-sohbet", "version": "1"}}})
        if response.status_code != 200:
            raise Unavailable(f"{self.kutuphane.id}: initialize HTTP {response.status_code}")
        result = self._message(response, ident).get("result") or {}
        self.session = response.headers.get("mcp-session-id")
        self.version = result.get("protocolVersion")
        await self._post({"jsonrpc": "2.0", "method": "notifications/initialized"})

    async def _rpc(self, method: str, params: dict) -> dict:
        """Kilit yalnız oturum açılırken: açık oturumda çağrılar aynı anda gider (okuyucular birbirini beklemesin)."""
        for attempt in range(2):
            async with self._lock:
                if self.session is None and self.version is None:
                    await self._initialize()
                self._next += 1
                ident, session = self._next, self.session
            response = await self._post({"jsonrpc": "2.0", "id": ident, "method": method, "params": params})
            if response.status_code in (400, 404) and attempt == 0:      # oturum düştü: bir kez yeniden
                async with self._lock:
                    if self.session == session:          # başka bir çağrı yenilemediyse
                        self.session = self.version = None
                continue
            if response.status_code != 200:
                raise Unavailable(f"{self.kutuphane.id}: HTTP {response.status_code}")
            message = self._message(response, ident)
            if "error" in message:
                raise Unavailable(f"{self.kutuphane.id}: {message['error'].get('message')}")
            return message.get("result") or {}
        raise Unavailable(f"{self.kutuphane.id}: session")

    async def list_tools(self) -> list[dict]:
        result = await self._rpc("tools/list", {})
        return [{"name": t["name"], "description": t.get("description") or "", "input_schema": t["inputSchema"]}
                for t in result.get("tools", [])]

    async def call(self, name: str, args: dict) -> tuple[str, bool]:
        result = await self._rpc("tools/call", {"name": name, "arguments": args})
        text = "".join(c.get("text", "") for c in result.get("content", []) if isinstance(c, dict))
        return text, bool(result.get("isError"))


def _client_for(kutuphane: Kutuphane):
    url = os.environ.get(f"SOHBET_{kutuphane.id.upper()}_URL", "").strip()
    if url:
        return Remote(kutuphane, url)
    from risale_mcp.profiles import PROFILES
    if PROFILES[kutuphane.profile].db.exists():
        return InProcess(kutuphane)
    return None


# ---------------------------------------------------------------- sohbetin kullandığı katman

class Kutuphaneler:
    """Öbür kütüphanelerin istemcileri, araçları ve işaret denetimi."""

    def __init__(self, clients: dict | None = None) -> None:
        self.clients = clients if clients is not None else {
            k: c for k in ORDER if (c := _client_for(KUTUPHANELER[k])) is not None}
        self._tools: dict[str, list[dict]] = {}

    def available(self) -> tuple[str, ...]:
        return tuple(k for k in ORDER if k in self.clients)

    def public(self) -> list[dict]:
        """Sayfanın seçicisi için."""
        return [{"id": k, "title": KUTUPHANELER[k].title, "hint": KUTUPHANELER[k].hint} for k in self.available()]

    async def tools(self, kutuphane: str) -> list[dict]:
        """Kütüphanenin araçları, önekli adlarıyla; ulaşılamazsa Unavailable."""
        if kutuphane not in self._tools:
            k = KUTUPHANELER[kutuphane]
            listed = await self.clients[kutuphane].list_tools()
            self._tools[kutuphane] = [
                {"name": f"{k.id}_{t['name']}", "description": f"[{k.label}] {t['description']}",
                 "input_schema": t["input_schema"]}
                for t in listed if t["name"] not in DROPPED_TOOLS]
        return self._tools[kutuphane]

    def owner(self, tool: str, chosen: tuple[str, ...]) -> tuple[str, str] | None:
        """Önekli araç adı seçilen bir kütüphanenin mi: (kütüphane, aracın kendi adı)."""
        head, _, name = tool.partition("_")
        return (head, name) if head in chosen and head in self.clients and name else None

    async def call(self, kutuphane: str, name: str, args: dict) -> tuple[str, bool]:
        try:
            text, error = await self.clients[kutuphane].call(name, args)
        except Unavailable:
            return (f"The {KUTUPHANELER[kutuphane].label} cannot be reached now; answer from the other libraries and "
                    "say that this one could not be checked."), True
        if len(text) > MAX_RESULT:
            text = (text[:MAX_RESULT] + f"\n[Result cut at {MAX_RESULT} characters: ask for less, e.g. a smaller "
                    "depth, a section or a limit.]")
        return text, error

    async def verify(self, kutuphane: str, items: list[dict]) -> list[dict]:
        """İşaretlerin denetimi: her öğe {id, quote?}; dönen her kayıtta cite_as, source_name ve tutmuyorsa problem
        (bilinmeyen kimlikte `unknown: True`). Kimlik cümle değilse ve alıntısızsa bölüm atfı denenir."""
        if not items:
            return []
        text, error = await self.call(kutuphane, "cite", {"sources": items})
        try:
            records = json.loads(text)["sources"] if not error else []
        except (ValueError, KeyError):
            records = []
        if len(records) != len(items):
            return [{"id": i["id"], "problem": "The library could not check this source.", "unchecked": True}
                    for i in items]
        out = []
        for item, record in zip(items, records):
            unknown = record.get("status") == "unknown_id" or "Unknown report id" in str(record.get("problem", ""))
            if unknown and not item.get("quote") and kutuphane != "hadis":
                section = await self._section(kutuphane, item["id"])
                if section:
                    out.append(section)
                    continue
            entry = {"id": item["id"], "cite_as": record.get("cite_as"), "source_name": record.get("source_name")}
            if record.get("status") not in (None, "ok") or record.get("problem"):
                entry["problem"] = record.get("problem") or "The quoted words are not in this source."
                entry["unknown"] = unknown
            out.append(entry)
        return out

    async def _section(self, kutuphane: str, ident: str) -> dict | None:
        text, error = await self.call(kutuphane, "get_outline", {"section": ident, "depth": 0})
        if error:
            return None
        try:
            node = json.loads(text)
        except ValueError:
            return None
        ref = node.get("ref") or node.get("title")
        return {"id": ident, "cite_as": ref, "section": True, "source_name": "OpenITI"} if ref else None

    async def text(self, kutuphane: str, ident: str) -> dict:
        """Sayfanın metin paneli için: Risale'ninkiyle aynı biçim (section_ref, sentences: id, text, target)."""
        if kutuphane == "hadis":
            body, error = await self.call("hadis", "get_hadith", {"id": ident})
            if error:
                raise LookupError(ident)
            report = json.loads(body)
            parts = [{"id": ident, "text": report.get("matn") or report.get("text") or "", "target": True}]
            if report.get("isnad") and report.get("matn"):
                parts.insert(0, {"id": ident + "#isnad", "text": report["isnad"], "target": False})
            return {"section_ref": report.get("cite_as"), "sentences": parts}
        body, error = await self.call(kutuphane, "get_passage", {"id": ident, "context": 2})
        if error:
            body, error = await self.call(kutuphane, "read_section", {"section": ident, "max_words": 300})
            if error:
                raise LookupError(ident)
            section = json.loads(body)
            sentences = [{"id": s["id"], "text": s["text"], "target": False}
                         for item in section.get("items", []) for s in item.get("sentences", [])][:8]
            return {"section_ref": section.get("ref") or ident, "sentences": sentences}
        passage = json.loads(body)
        return {"section_ref": passage.get("section_ref"),
                "sentences": [{"id": s["id"], "text": s["text"], "target": bool(s.get("target"))}
                              for s in passage.get("sentences", [])]}


def instructions(chosen: tuple[str, ...], unavailable: tuple[str, ...] = ()) -> str:
    """Seçilen kütüphanelerin talimata eklenen bloğu (sohbetin talimatının sonunda; seçime göre önbellekte ayrı)."""
    if not chosen:
        return ""
    lines = ["Other libraries the reader opened for this conversation, beside the Risale-i Nur:", ""]
    lines += [KUTUPHANELER[k].rules + "\n" for k in chosen]
    lines.append(
        "In these libraries: mark a quotation or a statement drawn from them with the library's name before the id: "
        "[[tefsir:ibnkesir/2/255/c001]], a range [[tefsir:ibnkesir/2/255/c001..c003]], a report [[hadis:bukhari/1]], "
        "[[klasik:tarifat/2/c001]]. The Risale-i Nur's ids stay without a name. Quote the Arabic exactly as returned, "
        "in a block quote, with no vowel marks added; after it, on its own line, give your own translation into the "
        "reader's language, labelled where it begins (in Turkish \"Yapay zekâ tercümesi:\"), never inside the "
        "quotation and never with a mark. Your rendering of these works' words inside your own sentences is never in "
        "quotation marks: write it as plain prose (\"Taberî halifeyi, yeryüzünde birbirinin yerine geçen nesil diye "
        "anlar\"). Keep the Risale-i Nur first and apart: what each library says has its own "
        "quotations and marks; never present a classical work's words as the Risale's, or the Risale's as a "
        "tafsir. Read in these libraries only what the question needs: their results are long.")
    if unavailable:
        lines.append("Not reachable now: " + ", ".join(KUTUPHANELER[k].label for k in unavailable)
                     + ". Say so if the question needs it.")
    return "\n".join(lines)


def status_line(kutuphane: str, name: str, args: dict) -> str:
    k = KUTUPHANELER[kutuphane]
    pattern = k.reading.get(name)
    if pattern:
        values = {key: " ".join(str(args.get(key) or "").split())[:60] for key in ("query", "section", "id",
                                                                                     "citation")}
        values["ayah"] = f"{args.get('sura', '')} {args.get('ayah', '')}".strip()
        try:
            return pattern.format(**values)
        except (KeyError, IndexError):
            pass
    return f"{k.title} kütüphanesine bakılıyor"
