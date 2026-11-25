"""S12.3: sohbet servisi (`risalemcp.com/sohbet/`): Claude API'si ve Risale'nin araçlarıyla soru–cevap.

Kullanıcının kararları (2026-11-25, `PLANLAR.md` S12): yalnız Risale, model Haiku 5.5, hesap şart (`sohbet_hesap.py`),
ücretsiz. Yapı:

- **Araçlar süreç içinde.** MCP sunucusu (`server.create_server`, genel profil) bu süreçte kurulur; araçların adı,
  açıklaması ve şeması oradan alınır, çağrı `MCPServer.call_tool` ile yapılır. Tanım kopyalanmaz; MCP üzerinden
  gidilmez (hesapsızların ortak sınırını yemez, ağ dolaşması yok, sonuçlar elimizde). `cite` modele verilmez: Kaynaklar'ı
  sunucu kurar.
- **Talimat** Risale sunucusunun talimatından türetilir (`instructions`): atıfla ilgili iki madde sohbetinkiyle
  değiştirilir, web cümlesi çıkar, başa sohbetin bağlamı gelir. Değiştirilen metin sunucuda bulunmazsa servis açılmaz
  (talimat değişti: buradaki değişiklik gözden geçirilmeli).
- **Atıf koddadır** (S12.5 (a)): model alıntının ve dayandığı her sözün ardına yalnız cümle kimliğini yazar
  (`[[sozler/10/…/c032]]`, aralık `[[…/c010..c013]]`). Sunucu cevabı bitince işaretleri toplar, alıntıyı
  `CitationChecker.sources` ile veritabanında denetler, numaraları ve Kaynaklar listesini kendisi yazar. Tutmayan
  alıntı modele bir kez düzeltmeye gider (cevap baştan yazılır); yine tutmazsa kullanıcıya işaretli görünür ve kullanım
  satırına yazılır.
- **Akış:** cevap Server-Sent Events ile gelir (`status`: araç satırı, `delta`: metin, `clear`: araçtan önceki ara
  metin silinir, `restart`: düzeltme başladı, `done`: denetlenmiş cevap ve kaynaklar, `error`).
- **Saklanmayan:** konuşmalar sunucuda tutulmaz (tarayıcıda durur, her soruda önceki sorular ve cevaplar düz metin
  olarak yeniden gönderilir). Saklanan yalnız kullanım satırıdır (`usage`: hesap, zaman, model, token, maliyet, araç
  sayısı, atıf denetiminin sonucu; soru ve cevap yok). Hesap silinince satırları adsızlaşır.
- **Sınırlar:** soru başına araç çağrısı (`MAX_TOOL_CALLS`) ve model turu (`MAX_ROUNDS`), konuşma başına soru
  (`MAX_TURNS`), soru ve geçmiş uzunluğu; kişi başına aynı anda tek soru. Günlük kota ve bütçe tavanı S12.4.

    uv run --extra sohbet python -m risale_mcp.sohbet serve [--port 8010] [--dev]
    uv run --extra sohbet python -m risale_mcp.sohbet sor "soru"      # terminalden tek soru (geliştirme)
    uv run --extra sohbet python -m risale_mcp.sohbet usage [--days 7]
"""

import argparse
import asyncio
import json
import os
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import AsyncIterator

from risale_mcp import sohbet_hesap
from risale_mcp.sohbet_hesap import COOKIE, Config, Store

ASSETS = Path(__file__).parent / "sohbet_assets"
MODEL = "claude-haiku-5-5"
EFFORT = "medium"
MAX_TOKENS = 16000
MAX_TOOL_CALLS = 20           # soru başına
MAX_ROUNDS = 14               # soru başına model çağrısı (düzeltme dahil)
MAX_TURNS = 10                # konuşma başına soru
MAX_QUESTION = 2000           # karakter
MAX_HISTORY = 60000           # önceki soru ve cevapların toplamı, karakter
EXCLUDED_TOOLS = {"cite"}
STREAM_ATTEMPTS = 2           # akış ortasında kopan bağlantıda tur bir kez yeniden
# Akışta okuma zaman aşımı: model düşünürken de sunucu ara ara ping gönderir; 60 sn sessizlik kopmuş bağlantıdır
# (2026-11-25: askıda kalan bir bağlantı 6 dakika bekletti).
TIMEOUT = {"total": 300.0, "read": 60.0, "connect": 10.0}

# $ / milyon token: (girdi, çıktı); Haiku 5.5'te istem 100 bin tokeni aşınca ikinci fiyat. Önbelleğe yazma girdinin
# 1,25 katı, okuma 0,1 katı (yaklaşık; asıl fatura Console'dadır).
PRICES = {"claude-haiku-5-5": ((0.10, 0.50), (0.50, 2.50), 100_000),
          "claude-sonnet-5-5": ((2.00, 10.00), (2.00, 10.00), 10**9)}
CACHE_WRITE, CACHE_READ = 1.25, 0.10

INLINE_QUOTE = re.compile(r"[\"“]([^\"“”]{8,})[\"”]\s*$")
# Düz metne yazılmış kimlik ya da cümle numarası: "(sozler/1/c016)", "(c033)", "(c034–c036)", "sozler/1/c016"
_ID = r"(?:[a-z0-9][a-z0-9-]*/)*c\d{3}(?:/[hs]\d+/c\d{3})?"
BARE_ID = re.compile(rf"[ \t]*\(\s*{_ID}(?:\s*(?:\.\.|[–—-])\s*{_ID})?\s*\)|(?<![\w/])[a-z][a-z0-9-]*(?:/[a-z0-9-]+)+/c\d{{3}}\b")
MARK = re.compile(r"\[\[\s*([^\[\]\s]+?)\s*\]\]")
SOURCES_HEADING = re.compile(r"^\s*(?:#{1,6}\s*)?(?:\*\*)?(?:Kaynaklar|Kaynakça|Sources)(?:\*\*)?\s*:?\s*(?:\*\*)?\s*$",
                             re.M | re.I)

# ---------------------------------------------------------------- talimat

PREAMBLE = """\
You answer readers' questions on the Risale-i Nur chat page of {name}. The reader sees only your final answer, \
rendered from Markdown; while you work, each tool call shows as a short status line. Do not write anything before \
or between tool calls: write only the final answer. You have no web access and no memory of other conversations.

Scope: this page answers only from the works of Bediüzzaman Said Nursî and the Qur'an, through the tools below. For \
a question outside them, say briefly that this page answers only from the Risale-i Nur. Your answers are an AI's \
answers: never speak as the author or in his name, and never present your words as tafsir or a fatwa. Answer in the \
reader's language, plainly; keep the answer as long as the question needs.

"""

CHAT_STEP = """\
3. Mark every quotation, and every statement drawn from a passage, with the id of the sentence or range you read it \
in, in double square brackets right after it: > "…" [[sozler/10/on-iki-hakikat/hakikat-09/c032]], or a range \
[[sozler/10/on-iki-hakikat/hakikat-09/c032..c034]] (at most 8 consecutive sentences of one section). Use only ids \
the tools returned in this conversation. The page checks every marked quotation against the works, numbers the \
sources and adds the Kaynaklar list itself.

"""

CHAT_CITING = """\
4. Never write references, section paths, sentence numbers, [1]-style numbers or a sources list yourself: the \
[[id]] marks are the references. An id or a sentence number (c033) never appears anywhere else in the answer, not in \
parentheses either: the reader never sees ids. Quote only words a tool returned, exactly, and put the mark right after the \
closing quotation mark. Quotations stand only in block quotes on their own line; in your prose put quotation \
marks around at most a single term. A passage you name or summarize without quoting is marked the same way.
"""

REPLACEMENTS = [   # (eski metnin başı, sonu: sonu kalır) → yeni
    ("3. Before writing the answer, call cite once", "\nAnswering:", CHAT_STEP),
    ("4. Always cite through a bibliography", "5. Keep what the text says apart", CHAT_CITING),
    ("Use the web only for outside context, listed apart. ", "Never invent references", ""),
]


def instructions(server_instructions: str, name: str) -> str:
    """Risale sunucusunun talimatından sohbetinki. Değiştirilecek yer bulunmazsa durur."""
    text = server_instructions
    for start, end, new in REPLACEMENTS:
        i = text.find(start)
        j = text.find(end, i + 1) if i >= 0 else -1
        if i < 0 or j < 0:
            raise RuntimeError(f"sohbet talimatı: sunucu talimatında {start!r} … {end!r} yok; "
                               "server.INSTRUCTIONS değişti, sohbet.REPLACEMENTS'ı gözden geçirin")
        text = text[:i] + new + text[j:]
    if any(phrase in text for phrase in ("call cite", "cite returns", "'s cite")):
        raise RuntimeError("sohbet talimatı: `cite` hâlâ anılıyor; sohbet.REPLACEMENTS'ı gözden geçirin")
    return PREAMBLE.format(name=name) + text


# ---------------------------------------------------------------- atıf

@dataclass
class Checked:
    markdown: str                      # işaretler [n] olmuş, modelin kendi Kaynaklar'ı atılmış
    sources: list[dict]                # n, id, cite_as, embedded, problem
    problems: list[dict] = field(default_factory=list)


def strip_own_sources(text: str) -> str:
    """Modelin yine de yazdığı Kaynaklar bölümü (sonda) atılır: listeyi sunucu kurar."""
    matches = list(SOURCES_HEADING.finditer(text))
    if matches and len(text) - matches[-1].start() < 4000:
        return text[:matches[-1].start()].rstrip()
    return text


def marks(text: str) -> list[tuple[str, str | None, tuple[int, int]]]:
    """(kimlik, alıntı ya da None, işaretin yeri) metindeki sırayla. Alıntı: işaretin bulunduğu alıntı bloğunun
    (`>` satırları) önceki işaretten sonraki kısmı; bloğun hemen altındaki yalnız işaretli satır da o bloğa aittir.
    Bloğun dışında işaretten hemen önce tırnak içinde duran söz de alıntı sayılır."""
    out = []
    pos = 0
    pending: list[str] = []            # açık alıntı bloğunun son işaretten sonraki metni
    in_block = False
    for line in text.split("\n"):
        quoted = line.lstrip().startswith(">")
        mark_only = bool(MARK.search(line)) and not MARK.sub("", line).strip()
        if quoted or (in_block and mark_only):
            in_block = True
        else:
            in_block, pending = False, []
        last = 0
        for m in MARK.finditer(line):
            before = line[last:m.start()]
            if in_block:
                quote = _quote_text("\n".join(pending + [before]))
                pending = []
            else:
                inline = INLINE_QUOTE.search(before)
                quote = _quote_text(inline.group(1)) if inline else None
            out.append((m.group(1), quote, (pos + m.start(), pos + m.end())))
            last = m.end()
        if in_block:
            pending.append(line[last:])
            if mark_only and not quoted:
                in_block, pending = False, []
        pos += len(line) + 1
    return out


def _quote_text(text: str) -> str | None:
    text = re.sub(r"^\s*>\s?", "", text, flags=re.M)
    text = re.sub(r"[*_]{1,2}", "", text).strip()
    text = re.sub(r"\[\d+\]", "", text).strip()
    return text.strip('"“”«» \n') or None


def check(checker, text: str) -> Checked:
    """İşaretleri numaralar, alıntıları denetler. Aynı kimlik aynı numarayı alır; birden çok alıntısı "…" ile
    birleşip birlikte denetlenir."""
    text = strip_own_sources(text)
    leaks = [m.group().strip() for m in BARE_ID.finditer(MARK.sub(" ", text))]
    found = marks(text)
    order: dict[str, int] = {}
    quotes: dict[str, list[str]] = {}
    for ident, quote, _ in found:
        order.setdefault(ident, len(order) + 1)
        if quote:
            quotes.setdefault(ident, []).append(quote)
    leak_problems = [{"id": leak, "problem": "An id or sentence number written in the prose: the reader must not "
                      "see ids. Put an id only inside [[ ]] right after the words it supports, or drop it."}
                     for leak in dict.fromkeys(leaks)]
    if not order:
        return Checked(_drop_leaks(text), [], leak_problems)
    items = [{"id": ident, **({"quote": " … ".join(quotes[ident])} if ident in quotes else {})} for ident in order]
    result = checker.sources(items)
    sources, problems = [], []
    for item, record in zip(items, result["sources"]):
        source = {"n": record["n"], "id": item["id"], "cite_as": record.get("cite_as")}
        if record.get("embedded"):
            source["embedded"] = record["embedded"]
        if record.get("problem"):
            source["problem"] = record["problem"]
            problems.append({"id": item["id"], "quote": item.get("quote"), "problem": record["problem"]})
        sources.append(source)
    out, last = [], 0
    for ident, _, (start, end) in found:
        out.append(text[last:start])
        out.append(f"[{order[ident]}]")
        last = end
    out.append(text[last:])
    markdown = re.sub(r"[ \t]+(\[\d+\])", r" \1", _drop_leaks("".join(out)))
    return Checked(markdown, sources, problems + leak_problems)


def _drop_leaks(text: str) -> str:
    """Düzeltmeden sonra da kalan düz kimlikler okuyucuya gösterilmez."""
    return re.sub(r"[ \t]+([.,;:])", r"\1", BARE_ID.sub("", text))


def correction(problems: list[dict]) -> str:
    lines = ["[Automatic check of your answer, not written by the reader] These marked quotations or references did "
             "not pass the check against the works:"]
    for p in problems:
        quote = f' "{p["quote"][:300]}"' if p.get("quote") else ""
        lines.append(f"- [[{p['id']}]]{quote}: {p['problem']}")
    lines.append("Write your whole answer again with these fixed: read the place again if needed, quote only words "
                 "the tools returned, exactly, and mark each with the sentence or range it is in; drop a quotation "
                 "you cannot place. Do not mention this check; the reader sees only the new answer.")
    return "\n".join(lines)


# ---------------------------------------------------------------- maliyet

def cost(model: str, usage) -> float:
    (inp, out), (long_in, long_out), threshold = PRICES.get(model, PRICES[MODEL])
    write = getattr(usage, "cache_creation_input_tokens", 0) or 0
    read = getattr(usage, "cache_read_input_tokens", 0) or 0
    prompt = usage.input_tokens + write + read
    if prompt > threshold:
        inp, out = long_in, long_out
    return (usage.input_tokens * inp + write * inp * CACHE_WRITE + read * inp * CACHE_READ
            + usage.output_tokens * out) / 1e6


@dataclass
class Tally:
    rounds: int = 0
    tools: int = 0
    input: int = 0
    output: int = 0
    cache_write: int = 0
    cache_read: int = 0
    cost: float = 0.0
    calls: list = field(default_factory=list)      # (araç, girdi, sonuç, hata mı): ölçüm dökümü için (`olc`)

    def add(self, model: str, usage) -> None:
        self.rounds += 1
        self.input += usage.input_tokens
        self.output += usage.output_tokens
        self.cache_write += getattr(usage, "cache_creation_input_tokens", 0) or 0
        self.cache_read += getattr(usage, "cache_read_input_tokens", 0) or 0
        self.cost += cost(model, usage)


# ---------------------------------------------------------------- araç satırları

def _short(text, n: int = 60) -> str:
    text = " ".join(str(text or "").split())
    return text if len(text) <= n else text[:n - 1] + "…"


def status_line(library, name: str, args: dict) -> str:
    def where(section: str) -> str:
        try:
            return library.outline(section, 0)["ref"]
        except Exception:
            return section
    try:
        match name:
            case "semantic_search":
                return f"Anlamca aranıyor: “{_short(args.get('query'))}”"
            case "search":
                return f"Kelime aranıyor: “{_short(args.get('query'))}”"
            case "read_section":
                return f"Okunuyor: {where(args.get('section', ''))}"
            case "get_outline":
                return f"İçindekilere bakılıyor: {where(args.get('section', ''))}"
            case "get_passage":
                ident = str(args.get("id", "")).split("..")[0]
                return f"Cümleler okunuyor: {where(ident.rsplit('/', 1)[0])}"
            case "find_sentence":
                return f"Cümle aranıyor: “{_short(args.get('incipit'))}”"
            case "find_ayah":
                return f"Âyetin geçtiği yerler aranıyor: {args.get('sura')}" + (f":{args['ayah']}" if args.get("ayah") else "")
            case "get_ayah":
                return f"Âyet okunuyor: {args.get('sura')}:{args.get('ayah')}"
            case "find_hadith" | "get_hadith":
                return "Hadis kaynaklarına bakılıyor"
            case "lookup_word":
                return f"Lügate bakılıyor: {_short(', '.join(map(str, args.get('words') or [])))}"
            case "list_works":
                return "Eserlerin listesine bakılıyor"
    except Exception:
        pass
    return "Eserlere bakılıyor"


# ---------------------------------------------------------------- sohbet

def _connection_error(error: Exception) -> bool:
    try:
        import anthropic
        return isinstance(error, (anthropic.APIConnectionError, anthropic.APITimeoutError))
    except ImportError:
        return False


class Refusal(Exception):
    """Kullanıcıya gösterilecek ret (sınır, geçersiz istek)."""


@dataclass
class Settings:
    model: str = MODEL
    effort: str = EFFORT

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(model=os.environ.get("SOHBET_MODEL", MODEL), effort=os.environ.get("SOHBET_EFFORT", EFFORT))


class Chat:
    def __init__(self, library, client, config: Config = Config(), settings: Settings = Settings()) -> None:
        from risale_mcp.citations import CitationChecker
        from risale_mcp.server import create_server
        self.library = library
        self.client = client
        self.config = config
        self.settings = settings
        self.server = create_server(library, profile="genel")
        self.checker = CitationChecker(library)
        self.system = instructions(self.server.instructions, config.name)
        self._tools: list[dict] | None = None

    async def tools(self) -> list[dict]:
        if self._tools is None:
            self._tools = [{"name": t.name, "description": t.description or "", "input_schema": t.input_schema}
                           for t in await self.server.list_tools() if t.name not in EXCLUDED_TOOLS]
        return self._tools

    def messages(self, history: list[dict], question: str) -> list[dict]:
        question = (question or "").strip()
        if not question:
            raise Refusal("Soru boş.")
        if len(question) > MAX_QUESTION:
            raise Refusal(f"Soru çok uzun (en çok {MAX_QUESTION} karakter).")
        if len(history) >= MAX_TURNS:
            raise Refusal(f"Bu konuşma {MAX_TURNS} soruya ulaştı; yeni bir konuşma başlatın.")
        out, size = [], 0
        for turn in history:
            q, a = str(turn.get("q", "")).strip(), str(turn.get("a", "")).strip()
            if not q or not a:
                continue
            size += len(q) + len(a)
            out += [{"role": "user", "content": q}, {"role": "assistant", "content": a}]
        if size > MAX_HISTORY:
            raise Refusal("Bu konuşma çok uzadı; yeni bir konuşma başlatın.")
        return out + [{"role": "user", "content": question}]

    def _params(self, tools: list[dict], messages: list[dict]) -> dict:
        return {"model": self.settings.model, "max_tokens": MAX_TOKENS,
                "system": [{"type": "text", "text": self.system, "cache_control": {"type": "ephemeral"}}],
                "tools": tools, "messages": messages, "cache_control": {"type": "ephemeral"},
                "output_config": {"effort": self.settings.effort}}

    async def _call_tool(self, block) -> dict:
        from mcp.server.mcpserver.exceptions import ToolError
        args = block.input if isinstance(block.input, dict) else {}
        try:
            result = await self.server.call_tool(block.name, args)
            text = "".join(getattr(c, "text", "") for c in result.content)
            return {"type": "tool_result", "tool_use_id": block.id, "content": text,
                    **({"is_error": True} if getattr(result, "is_error", False) else {})}
        except ToolError as e:
            return {"type": "tool_result", "tool_use_id": block.id, "content": str(e), "is_error": True}
        except Exception:
            import logging
            logging.exception("sohbet: araç hatası %s", block.name)
            return {"type": "tool_result", "tool_use_id": block.id, "is_error": True,
                    "content": f"The tool {block.name} failed; try another way."}

    async def ask(self, history: list[dict], question: str, tally: Tally | None = None) -> AsyncIterator[tuple[str, dict]]:
        """(olay, veri) üretir; sonuncusu `done` ya da `error`. `tally` kullanım satırı için doldurulur."""
        tally = tally if tally is not None else Tally()
        messages = self.messages(history, question)
        tools = await self.tools()
        corrected = False
        while True:
            text = None
            async for event in self._loop(tools, messages, tally):
                if event[0] == "final":
                    text = event[1]["text"]
                else:
                    yield event
            if text is None:
                return
            checked = await asyncio.to_thread(check, self.checker, text)
            if checked.problems and not corrected and tally.rounds < MAX_ROUNDS:
                corrected = True
                messages.append({"role": "user", "content": correction(checked.problems)})
                yield "restart", {"text": "Alıntılar eserlerle denetleniyor; düzeltiliyor…"}
                continue
            yield "done", {"markdown": checked.markdown, "raw": strip_own_sources(text), "sources": checked.sources,
                           "problems": len(checked.problems), "corrected": corrected,
                           "usage": {"cost": round(tally.cost, 5), "tools": tally.tools, "rounds": tally.rounds}}
            return

    async def _loop(self, tools: list[dict], messages: list[dict], tally: Tally):
        while True:
            if tally.rounds >= MAX_ROUNDS:
                yield "error", {"message": "Bu soru için okuma sınırına ulaşıldı. Soruyu daraltarak yeniden sorun."}
                return
            yield "status", {"text": "Düşünüyor…"}
            message = None
            for attempt in range(STREAM_ATTEMPTS):
                try:
                    async with self.client.messages.stream(**self._params(tools, messages)) as stream:
                        async for event in stream:
                            if event.type == "text" and event.text:
                                yield "delta", {"text": event.text}
                        message = await stream.get_final_message()
                    break
                except Exception as error:      # akış ortasında kopan bağlantı: SDK yeniden denemez, tur baştan
                    if attempt + 1 >= STREAM_ATTEMPTS or not _connection_error(error):
                        raise
                    import logging
                    logging.warning("sohbet: akış koptu (%s), tur yeniden", type(error).__name__)
                    yield "clear", {}
                    yield "status", {"text": "Bağlantı yenileniyor…"}
            tally.add(self.settings.model, message.usage)
            messages.append({"role": "assistant", "content": message.content})
            uses = [b for b in message.content if b.type == "tool_use"]
            if message.stop_reason == "refusal":
                yield "error", {"message": "Bu soruya cevap verilemedi."}
                return
            if message.stop_reason != "tool_use" or not uses:      # end_turn; max_tokens'ta yarım araç çalıştırılmaz
                text = "".join(b.text for b in message.content if b.type == "text").strip()
                if not text:
                    yield "error", {"message": "Cevap yazılamadı. Yeniden deneyin."}
                    return
                yield "final", {"text": text}
                return
            yield "clear", {}
            results = []
            for block in uses:
                if tally.tools >= MAX_TOOL_CALLS:
                    results.append({"type": "tool_result", "tool_use_id": block.id, "is_error": True,
                                    "content": "The tool limit for this question is reached: answer now with what "
                                               "you have read, and say what you could not check."})
                    continue
                tally.tools += 1
                yield "status", {"text": status_line(self.library, block.name, block.input or {})}
                results.append(result := await self._call_tool(block))
                tally.calls.append((block.name, block.input or {}, result["content"], bool(result.get("is_error"))))
            messages.append({"role": "user", "content": results})


# ---------------------------------------------------------------- kullanım satırı

def log_usage(store: Store, email: str | None, model: str, tally: Tally, seconds: float, outcome: str,
              done: dict | None = None) -> None:
    store._run("INSERT INTO usage VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
               (time.time(), email, model, tally.rounds, tally.tools, tally.input, tally.output, tally.cache_write,
                tally.cache_read, round(tally.cost, 6), round(seconds, 2),
                len(done["sources"]) if done else None, done["problems"] if done else None,
                int(done["corrected"]) if done else None, outcome))


# ---------------------------------------------------------------- web

def page(config: Config, email: str) -> str:
    import html as _html
    version = _asset_version()
    return ((ASSETS / "sohbet.html").read_text(encoding="utf-8")
            .replace("{{P}}", _html.escape(config.prefix)).replace("{{NAME}}", _html.escape(config.name))
            .replace("{{EMAIL}}", _html.escape(email)).replace("{{V}}", version))


def _asset_version() -> str:
    import hashlib
    h = hashlib.sha256()
    for name in ("sohbet.js", "sohbet.css"):
        h.update((ASSETS / name).read_bytes())
    return h.hexdigest()[:10]


CSP = ("default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self'; "
       "font-src 'self'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'")


def routes(chat: Chat, store: Store, config: Config):
    from starlette.requests import Request
    from starlette.responses import FileResponse, HTMLResponse, JSONResponse, StreamingResponse
    from starlette.routing import Route

    p = config.prefix
    busy: set[str] = set()
    headers = {"Cache-Control": "no-store", "Referrer-Policy": "no-referrer", "Content-Security-Policy": CSP}

    def user(request: Request) -> str | None:
        return store.check(request.cookies.get(COOKIE))

    def home(request: Request, email: str) -> HTMLResponse:
        return HTMLResponse(page(config, email), headers=headers)

    async def asset(request: Request):
        name = request.path_params["name"]
        media = {"sohbet.js": "text/javascript", "sohbet.css": "text/css"}.get(name)
        if not media:
            return JSONResponse({"error": "yok"}, status_code=404)
        return FileResponse(ASSETS / name, media_type=media, headers={"Cache-Control": "public, max-age=31536000"})

    async def text(request: Request):
        if not user(request):
            return JSONResponse({"error": "oturum yok"}, status_code=401, headers=headers)
        ident = request.query_params.get("id", "")[:300]
        try:
            passage = await asyncio.to_thread(chat.library.passage, ident, 3)
        except Exception:
            return JSONResponse({"error": "Bu adreste metin bulunamadı."}, status_code=404, headers=headers)
        return JSONResponse(passage, headers=headers)

    async def ask(request: Request):
        email = user(request)
        if not email:
            return JSONResponse({"error": "Oturumunuz kapanmış; yeniden giriş yapın."}, status_code=401,
                                headers=headers)
        if not request.headers.get("content-type", "").startswith("application/json"):
            return JSONResponse({"error": "geçersiz istek"}, status_code=415, headers=headers)
        try:
            body = await request.json()
            history = [t for t in body.get("history", []) if isinstance(t, dict)][:MAX_TURNS + 1]
            question = str(body.get("question", ""))
        except Exception:
            return JSONResponse({"error": "geçersiz istek"}, status_code=400, headers=headers)
        if email in busy:
            return JSONResponse({"error": "Önceki sorunuzun cevabı sürüyor."}, status_code=429, headers=headers)

        async def stream():
            busy.add(email)
            tally, start, outcome, done = Tally(), time.time(), "cancelled", None
            try:
                async for event, data in chat.ask(history, question, tally):
                    if event == "done":
                        outcome, done = "done", data
                    elif event == "error":
                        outcome = "error"
                    yield f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"
            except Refusal as e:
                outcome = "refused"
                yield f"event: error\ndata: {json.dumps({'message': str(e)}, ensure_ascii=False)}\n\n"
            except Exception:
                import logging
                logging.exception("sohbet: cevap yazılamadı")
                outcome = "error"
                yield "event: error\ndata: " + json.dumps({"message": "Bir hata oldu; biraz sonra yeniden deneyin."},
                                                          ensure_ascii=False) + "\n\n"
            finally:
                busy.discard(email)
                if outcome != "refused":
                    log_usage(store, email, chat.settings.model, tally, time.time() - start, outcome, done)

        return StreamingResponse(stream(), media_type="text/event-stream",
                                 headers={**headers, "X-Accel-Buffering": "no"})

    return home, [Route(f"{p}api/sor", ask, methods=["POST"]), Route(f"{p}api/metin", text),
                  Route(f"{p}static/{{name}}", asset)]


def build(chat: Chat, store: Store, mailer, config: Config):
    home, extra = routes(chat, store, config)
    return sohbet_hesap.build_app(store, mailer, config, extra_routes=extra, home_page=home)


def _client():
    import anthropic
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("ANTHROPIC_API_KEY yok (.env)")
    return anthropic.AsyncAnthropic(timeout=anthropic.Timeout(TIMEOUT["total"], read=TIMEOUT["read"],
                                                              connect=TIMEOUT["connect"]))


def _library():
    from risale_mcp.library import Library
    from risale_mcp.profiles import GENEL
    library = Library(GENEL.db, GENEL.vectors)
    library.conn                       # veritabanı yoksa başlarken açık hata
    return library


# ---------------------------------------------------------------- ölçüm (S12.1'in teyidi)

def answer_text(done: dict) -> str:
    """Okuyucunun gördüğü cevap düz metin olarak: cevap ve Kaynaklar (altın soru denetimi bunu okur)."""
    lines = [done["markdown"].rstrip(), "", "Kaynaklar"]
    for s in done["sources"]:
        lines.append(f"[{s['n']}] {s.get('cite_as') or s['id']}")
        lines += [f"  - {e['line']}" for e in s.get("embedded", ())]
    return "\n".join(lines) if done["sources"] else done["markdown"]


async def measure(chat: Chat, ids: list[str]) -> Path:
    """Altın soruları bu servisle sorar; dökümü `golden` biçiminde (`<soru>.jsonl`) yazar, raporu `golden.report`
    kurar. Maliyet API'nin gerçek fiyatıdır (S12.1'inki Claude Code'un istemiyle eşdeğer maliyetti)."""
    from datetime import datetime
    from risale_mcp import golden
    questions = [q for q in golden.load_questions() if q["id"] in ids] if ids else \
        [q for q in golden.load_questions() if not q.get("profile")]
    out = golden.RUNS_DIR / f"{datetime.now():%Y%m%d-%H%M%S}-sohbet-{chat.settings.model}"
    out.mkdir(parents=True)
    (out / "model.json").write_text(json.dumps({"model": chat.settings.model, "effort": chat.settings.effort,
                                                "kind": "sohbet"}), encoding="utf-8")
    print(f"{len(questions)} soru; döküm: {out}", flush=True)
    for q in questions:
        tally, start, done, failure, restarts = Tally(), time.time(), None, None, 0
        try:
            async for event, data in chat.ask([], q["question"], tally):
                if event == "done":
                    done = data
                elif event == "error":
                    failure = data["message"]
                elif event == "restart":
                    restarts += 1
        except Exception as error:                       # bir sorunun hatası ölçümü durdurmasın
            failure = f"{type(error).__name__}: {error}"
        lines = []
        for i, (name, args, result, error) in enumerate(tally.calls):
            lines.append({"type": "assistant", "message": {"content": [
                {"type": "tool_use", "id": f"t{i}", "name": name, "input": args}]}})
            lines.append({"type": "user", "message": {"content": [
                {"type": "tool_result", "tool_use_id": f"t{i}", "content": result, "is_error": error}]}})
        lines.append({"type": "result", "subtype": "success" if done else "error",
                      "is_error": done is None, "result": answer_text(done) if done else "",
                      "total_cost_usd": tally.cost, "num_turns": tally.rounds,
                      "duration_ms": int((time.time() - start) * 1000), "usage": {"output_tokens": tally.output},
                      "sohbet": {"corrected": bool(done and done["corrected"]), "problems": done and done["problems"],
                                 "failure": failure, "input": tally.input, "cache_write": tally.cache_write,
                                 "cache_read": tally.cache_read}})
        (out / f"{q['id']}.jsonl").write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in lines) + "\n",
                                              encoding="utf-8")
        print(f"  {q['id']}: {time.time() - start:.0f} sn, {tally.tools} araç, {tally.cost:.4f} $"
              + (" düzeltildi" if done and done["corrected"] else "") + (f" HATA {failure}" if failure else ""),
              flush=True)
    golden.report(out)
    return out


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="sohbet servisi (S12.3)")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("serve")
    p.add_argument("--port", type=int, default=8010)
    p.add_argument("--dev", action="store_true", help="e-posta gönderilmez, data/interim/sohbet/eposta.log'a yazılır")
    p = sub.add_parser("sor", help="terminalden tek soru")
    p.add_argument("question")
    p = sub.add_parser("olc", help="altın soruları bu servisle sor (S12.1'in teyidi); varsayılan: Risale soruları")
    p.add_argument("ids", nargs="*")
    p = sub.add_parser("usage")
    p.add_argument("--days", type=float, default=7)
    args = parser.parse_args(argv)
    from risale_mcp.env import load_env
    load_env()
    import logging
    logging.getLogger("httpx").setLevel(logging.WARNING)       # her API isteğinin satırı günlüğü doldurmasın
    config, settings = Config.from_env(), Settings.from_env()
    if args.command == "serve":
        import uvicorn
        store = Store()
        chat = Chat(_library(), _client(), config, settings)
        app = build(chat, store, sohbet_hesap.mailer_from_env(config, args.dev), config)
        uvicorn.run(app, host="127.0.0.1", port=args.port, proxy_headers=True, forwarded_allow_ips="127.0.0.1",
                    access_log=False)
    elif args.command == "sor":
        chat = Chat(_library(), _client(), config, settings)

        async def run():
            tally, start = Tally(), time.time()
            async for event, data in chat.ask([], args.question, tally):
                if event == "status":
                    print(f"  · {data['text']}", flush=True)
                elif event == "restart":
                    print(f"  ! {data['text']}", flush=True)
                elif event == "error":
                    print("HATA:", data["message"])
                elif event == "done":
                    print("\n" + data["markdown"] + "\n\nKaynaklar")
                    for s in data["sources"]:
                        print(f"[{s['n']}] {s.get('cite_as') or s['id']}" + (f"  ⚠ {s['problem']}" if s.get("problem") else ""))
                        for e in s.get("embedded", ()):
                            print(f"  - {e['line']}")
            print(f"\n{tally.rounds} tur, {tally.tools} araç, girdi {tally.input} (önbellek yazma {tally.cache_write}, "
                  f"okuma {tally.cache_read}), çıktı {tally.output}, ≈{tally.cost:.4f} $, {time.time() - start:.1f} sn")
        asyncio.run(run())
    elif args.command == "olc":
        asyncio.run(measure(Chat(_library(), _client(), config, settings), args.ids))
    elif args.command == "usage":
        store = Store()
        since = time.time() - args.days * 86400
        rows = store._run("SELECT outcome, COUNT(*) n, SUM(cost) c, AVG(cost) a, AVG(tools) t, AVG(seconds) s, "
                          "SUM(problems > 0) bad, SUM(corrected) fix FROM usage WHERE ts >= ? GROUP BY outcome", (since,))
        users = store._run("SELECT COUNT(DISTINCT email) FROM usage WHERE ts >= ?", (since,))[0][0]
        print(f"son {args.days:g} gün, {users} kullanıcı")
        for r in rows:
            print(f"{r['outcome']:10} {r['n']:5} soru  toplam {r['c'] or 0:.3f} $  soru başı {r['a'] or 0:.4f} $  "
                  f"araç {r['t'] or 0:.1f}  {r['s'] or 0:.1f} sn  düzeltilen {r['fix'] or 0}  denetimden düşen {r['bad'] or 0}")


if __name__ == "__main__":
    main()
