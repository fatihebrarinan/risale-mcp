"""S12.3: sohbet servisi (`risalemcp.com/sohbet/`): Claude API'si ve Risale'nin araçlarıyla soru–cevap.

Kullanıcının kararları (2026-11-25, `PLANLAR.md` S12): yalnız Risale, model Haiku 5.5, hesap şart (`sohbet_hesap.py`),
ücretsiz. Yapı:

- **Araçlar süreç içinde.** MCP sunucusu (`server.create_server`, genel profil) bu süreçte kurulur; araçların adı,
  açıklaması ve şeması oradan alınır, çağrı `MCPServer.call_tool` ile yapılır. Tanım kopyalanmaz; MCP üzerinden
  gidilmez (hesapsızların ortak sınırını yemez, ağ dolaşması yok, sonuçlar elimizde). `cite` modele verilmez: Kaynaklar'ı
  sunucu kurar.
- **Talimat** sohbetin kendisinindir (S12.10, `instructions`): giriş, akış, cevabın biçimi (okuyucu, önce kısa cevap,
  sonra metin, sonra yorum; uzunluk; kapsam) ve işaret kuralları burada; kaynağa bağlılığın kuralları ve müellifin
  sözü olmayan katmanlar Risale talimatının ortak bloklarından (`server.FIND`, `GROUNDED`, `risale_layers` …) gelir,
  kopyalanmaz. MCP'ye özgü kısımlar (web, `cite`, kaynakça, bağdaştırıcılar arası numaralama) girmez.
- **Atıf koddadır** (S12.5 (a)): model alıntının ve dayandığı her sözün ardına yalnız cümle kimliğini yazar
  (`[[sozler/10/…/c032]]`, aralık `[[…/c010..c013]]`). Sunucu cevabı bitince işaretleri toplar, alıntıyı
  `CitationChecker.sources` ile veritabanında denetler, numaraları ve Kaynaklar listesini kendisi yazar. **Düzeltmeyi
  sunucu yapar** (S12.9, `check`): eserlerde başka yerde bulunan alıntının işareti oraya taşınır (modelin okuduğu yer
  önce), alıntısız işaretin aralığı kısalır ya da kimliği yoksa silinir, düz metne yazılmış kimlik silinir; eserlerde
  hiç bulunmayan alıntı "doğrulanamadı" işaretiyle görünür. Modele düzeltme turu (yol (a)) varsayılan kapalıdır
  (`SOHBET_MODEL_FIX`). Kaç işaretin düzeltildiği, doğrulanamadığı ve işaretsiz paragraf sayısı kullanım satırındadır.
- **Akış:** cevap Server-Sent Events ile gelir (`status`: ne yapıldığı; araç adımında `step`, sayfa onları dizer; `delta`: metin, `clear`: araçtan önceki ara
  metin silinir, `restart`: düzeltme başladı, `done`: denetlenmiş cevap ve kaynaklar, `error`).
- **Konuşmalar** (S13.1, kullanıcının kararları 2026-11-25): hesapta saklanır (`Conversations`; ayar
  `users.keep_history`, varsayılan açık). Saklanan konuşmanın geçmişi sunucudan okunur, tarayıcının gönderdiği
  geçmişe güvenilmez; konuşma ilk cevap bitince açılır (hatalı soru boş konuşma bırakmaz), başlığı ilk sorudan
  kısaltılır. Yalnız sahibine gösterilir, ekip okumaz (gizlilik sayfası); tek tek ya da hepsi silinir, hesap silinince
  hepsi gider. Ayar kapalıyken konuşma S12'deki gibi yalnız tarayıcıda durur ve her soruda geçmiş tarayıcıdan gelir.
  Kullanım satırı (`usage`: hesap, zaman, model, token, maliyet, araç sayısı, atıf denetiminin sonucu) soru ve cevabı
  taşımaz; hesap silinince adsızlaşır.
- **Sınırlar:** soru başına araç çağrısı (`MAX_TOOL_CALLS`) ve model turu (`MAX_ROUNDS`), konuşma başına soru
  (`MAX_TURNS`), soru ve geçmiş uzunluğu; kişi başına aynı anda tek soru. Günlük kota ve bütçe tavanı S12.4.

    uv run --extra sohbet python -m risale_mcp.sohbet serve [--port 8010] [--dev]
    uv run --extra sohbet python -m risale_mcp.sohbet sor "soru"      # terminalden tek soru (geliştirme)
    uv run --extra sohbet python -m risale_mcp.sohbet dene <sorular.txt> [ad …]   # hata ayıklama turu (S13.11)
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
from risale_mcp.library import MAX_CITED as MAX_RANGE   # bir işaretin en çok cümlesi
from risale_mcp.normalize import search_words
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
MAX_TITLE = 80                # konuşma başlığı, karakter
MAX_LISTED = 500              # sol panelde gösterilen en çok konuşma
MAX_NOTE = 1000               # geri bildirim notu, karakter
MAX_SHARED = 40000            # onayla gönderilen soru ve cevap, karakter
FEEDBACK_PER_DAY = 50         # kişi başına
USAGE_DAYS = 90               # kullanım satırlarının saklanma süresi (MCP'nin kullanım kaydıyla aynı; gizlilik politikası)
FEEDBACK_DAYS = 365           # geri bildirimin saklanma süresi
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
BARE_ID = re.compile(rf"[ \t]*\(\s*{_ID}(?:\s*(?:\.\.|[–—-])\s*{_ID})?\s*\)|(?<![\w/])[a-z][a-z0-9-]*(?:/[a-z0-9-]+)+/c\d{{3}}\b"
                     # S13.11: cümle içinde tek başına "c013" ("(c013 sonrası … karşılaştırması)")
                     rf"|(?<![\w/\[])c\d{{3}}(?:\.\.c\d{{3}})?\b(?![\]/])")
MARK = re.compile(r"\[\[\s*([^\[\]\s]+?)\s*\]\]")
RELOCATE_CANDIDATES = 30      # başka yerde aranan alıntının bakılan en çok geçişi
SOURCES_HEADING = re.compile(r"^\s*(?:#{1,6}\s*)?(?:\*\*)?(?:Kaynaklar|Kaynakça|Sources)(?:\*\*)?\s*:?\s*(?:\*\*)?\s*$",
                             re.M | re.I)

# ---------------------------------------------------------------- talimat

INTRO = """\
You answer readers' questions on the Risale-i Nur chat page of {name}. The reader sees only your final answer, \
rendered from Markdown; while you work, each tool call shows as a short status line. Do not write anything before \
or between tool calls: write only the final answer. You have no web access and no memory of other conversations.

You read the works of Bediüzzaman Said Nursî (the Risale-i Nur volumes, the early works, the compilations, the \
Hizbs, the works he wrote in Arabic with their Turkish translations) and the Qur'an through the tools below. Texts \
are split into sentences; every sentence has an id.
"""

MARK_STEP = """\
Mark what you rely on: right after every quotation, and after every statement drawn from a passage (a summary of a \
parable, what a section says), write in double square brackets the id of the sentence or range you read it in: \
> "…" [[sozler/10/on-iki-hakikat/hakikat-09/c032]], or a range [[sozler/10/on-iki-hakikat/hakikat-09/c032..c034]] \
(at most 8 consecutive sentences of one section). A quotation is always marked with a sentence id (ending in c and \
a number). Only to name a whole section where a topic is treated, without quoting it, mark the section's id \
([[sozler/31]]); never put a section id after a quotation. Use only ids the tools returned in this conversation. The page checks every marked quotation against the works, numbers the sources and \
adds the Kaynaklar list itself."""

SHAPE = """\
The answer:
- The readers: people who read the Risale-i Nur, some for years and some for the first time, most of them on a \
phone, few of them specialists. Write plain, present-day prose in the reader's language; when an old word in a \
quotation matters to the point, explain it briefly in your own words.
- Language: write the whole answer, headings included, in the language of the reader's latest question (a question \
in Turkish gets a Turkish answer), even though the tool results and these instructions are in English. Quotations \
stay exactly as returned, in their own language: never translate a quotation. In a Turkish answer write no \
English words (Arapça, not Arabic); the translation get_ayah gives is the "Türkiye Diyanet Vakfı meali", always in \
full, never "Diyanet meali". A question whose language is unclear (only a name or a term, such as "Mevlânâ" or \
"haşir") is answered in the page's language, Turkish.
- Order: first answer the question directly in two or three sentences; then what the text says, in quotations \
joined by short sentences of your own; then, when the question asks for meaning or application, or a reader would \
expect it, your interpretation under its own heading (in Turkish "Yorum"), plainly marked as yours. A question \
about where a topic is treated is answered with the places, grouped by work, the central ones first.
- Length: as long as the question needs. A simple question gets a few paragraphs and one to three quotations; \
fewer well-chosen quotations are better than many. Use short headings only when the answer has more than one part.
- The author's firmness: when the author states something firmly ("kanâat-ı kat'iyye", "çekinmeyerek deriz", \
"elbette"), report it as firm, never as a hedge or a mere possibility. Your interpretation explains what the text \
says and how it holds together; it never grades the author's claims (no "a typical example of…", "a pious \
reading", "not a proof").
- Writing dates: say when or where a treatise was written only when the question asks about it. A year in the text \
or in a date record that does not name its calendar (hicrî, rûmî, milâdî) is given as it stands: never convert it, \
and never compare it with another date by your own reckoning.
- Names: Lemeât (also called the Thirty-Second Letter and the Thirty-Second Lem'a, at the end of Sözler) and \
Lem'alar are different works; when a passage names one, never call it by the other's name. Name a section and \
its number exactly as the ref the tools return (lemalar/26 is Yirmialtıncı Lem'a), never by your own count.
- Scope: only the works and the Qur'an through these tools. For a question outside them (news, other books, \
personal or legal rulings), say briefly that this page answers only from the Risale-i Nur. Your answers are an \
AI's answers: never speak as the author or in his name, and never present your words as tafsir or a fatwa."""

EARLIER = """\
Earlier answers in this conversation: before the reader's new question the page lists, for each of your earlier \
answers, the tools you called for it and, after each reading call, the title of the place read (a page note, not the \
reader's words). An earlier statement rests on what those calls returned: a section you read brings its sentences, \
its verses with their refs and the publisher's translations. The page checked your earlier marked quotations against \
the works. Never call an earlier statement unchecked when its calls cover it, and never say you have not read a place \
the note lists as read. Do not take back or "correct" an earlier statement on your own: the tools you called \
then returned more than you see now, and not seeing a record again (for example after calling a tool with another \
filter) is no evidence against it. Correct an earlier statement only when the reader questions it, when a result you \
read now says the opposite in its own words, or when it clearly had no basis in the calls (for example, you compared \
a translation you never read); then do it in one sentence at the start of your new answer. If the list says the calls were not \
recorded, say nothing about checking.
Say what a verse, a translation or any text says only if you read it with a tool in this conversation: the \
publisher's translation comes with the passage, the Türkiye Diyanet Vakfı translation of a verse only from get_ayah; \
never compare with a translation you have not read."""

VERSES = """\
Verses quoted in the works: the translation that comes with a passage (publisher_translation) is the publisher's. \
If you give it, put it on its own line after the quotation, never inside the quoted block, and call it the \
publisher's in the reader's language (in Turkish "nâşirin meali", never the English words). Naming the Türkiye Diyanet Vakfı translation is only for a verse you read with get_ayah; otherwise \
never mention that translation at all, not even to say that a translation is not it."""


NO_REFERENCES = """\
Never write references, section paths, sentence numbers, [1]-style numbers or a sources list yourself: the \
[[id]] marks are the references. An id or a sentence number (c033) never appears anywhere else in the answer, not in \
parentheses either: the reader never sees ids. Never write a sentence's number in the prose ("52. cümle"); \
name the section instead. Put the mark right after the closing quotation mark. A verse of the Qur'an is named in the prose by its ref, as below."""

# Sohbetin alıntı kuralı (kullanıcının kararı, 2026-11-26): MCP'ninki (`server.QUOTE_EXACTLY`) düz yazıda yalnız tek
# terime tırnak izin verir; sohbette cümleye örülmüş kısa alıntı serbesttir, çünkü sayfa onu da denetler
# (`INLINE_QUOTE`: kapanış tırnağının hemen ardındaki işaret). İşaretsiz satır içi alıntı denetlenmez: yasak kalır.
QUOTE_EXACTLY = """\
Quote the works exactly as returned. A quotation that carries the point goes in a block quote on its own line \
(> "…"). A short quotation (a phrase or one short sentence) may run inside your own sentence, in double quotation \
marks, with its mark right after the closing quotation mark; without the mark, put quotation marks around at most a \
single term. Your own translation or paraphrase of a passage is not a quotation: never put it in quotation marks \
with a mark; give it as your words, said to be your translation. A parable or one line of thought running over consecutive sentences of one section is quoted as one \
block with one source (a range, at most 8 sentences); a longer passage is quoted as consecutive blocks, each with its \
own range."""


def instructions(name: str, lugat: bool = True) -> str:
    """Sohbetin talimatı (S12.10): kendi girişi, akışı ve cevap biçimi; kaynağa bağlılığın kuralları ve müellifin sözü
    olmayan katmanlar Risale talimatının ortak bloklarından (`server`), kopyasız."""
    from risale_mcp import server as s
    return (INTRO.format(name=name) + f"""
Workflow:
1. {s.FIND}
2. {s.READ}
3. {MARK_STEP}

{SHAPE}

Rules:
1. {s.GROUNDED}{s.NEVER_INVENT}
2. {QUOTE_EXACTLY}
3. {NO_REFERENCES}
4. {s.TEXT_APART}
5. {EARLIER}
6. {VERSES}

""" + s.risale_layers(connectors=False) + (s.LUGAT_INSTRUCTIONS.lstrip("\n") + "\n" if lugat else ""))


# ---------------------------------------------------------------- atıf

@dataclass
class Checked:
    markdown: str                      # işaretler [n] olmuş, modelin kendi Kaynaklar'ı atılmış
    sources: list[dict]                # n, id, cite_as, embedded; doğrulanamayanda problem, unverified
    problems: list[dict] = field(default_factory=list)   # denetimden ilk geçişte düşen her işaret ve düz kimlik
    raw: str = ""                      # modelin cevabı, işaretler düzeltilmiş (sonraki soruda geçmiş olarak gider)
    counts: dict = field(default_factory=dict)          # fixed, repaired, unverified, dropped, leaks, paragraphs, unmarked, unmarked_found, unmarked_missing


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


def check(checker, text: str, read: frozenset[str] | set[str] = frozenset()) -> Checked:
    """İşaretleri denetler, düzeltir ve numaralar (S12.9: düzeltmeyi sunucu yapar). Her işaret ayrı denetlenir:

    - tutan işaret kalır;
    - alıntısı işaretin cümlelerinde olmayan, ama eserlerde bulunan işaret alıntının bulunduğu cümleye (ya da kapsayan
      en kısa aralığa) taşınır; birden çok yerde geçiyorsa modelin okuduğu (`read`: okuma araçlarının döndürdüğü
      cümle kimlikleri), sonra işaretin bölümündeki, sonra eserindeki yer seçilir;
    - alıntısız işaretin aralığı uzunsa ya da bölümü aşıyorsa geçerli kısmına kısalır; kimliği yoksa işaret silinir;
    - "…" ile birleşen alıntının bir parçası tutmuyorsa o parça metindeki karşılığıyla değişir ya da atılır (S13.16);
    - eserlerde hiç bulunmayan alıntı ayrı numara alır, kaynağı "doğrulanamadı" işaretiyle (`unverified`) görünür;
    - işaretsiz tırnaklı söz (dört kelime ve üstü) aranır: bulunursa işaret alır, bulunmazsa uyarı (S13.16);
    - düz metne yazılmış kimlik ("(c033)") silinir.

    Aynı kimlik aynı numarayı alır; birden çok alıntısı "…" ile birleşip birlikte denetlenir."""
    text, unmarked = unmarked_quotes(checker, _split_blocks(strip_own_sources(text)), read)
    leaks = list(dict.fromkeys(m.group().strip() for m in BARE_ID.finditer(MARK.sub(" ", text))))
    problems = [{"id": leak, "problem": "An id or sentence number written in the prose: the reader must not see ids. "
                 "Put an id only inside [[ ]] right after the words it supports, or drop it."} for leak in leaks]
    counts = {"fixed": 0, "repaired": 0, "unverified": 0, "dropped": 0, "leaks": len(leaks), **unmarked}
    found = marks(text)
    edits: dict[int, list[tuple[str, str]]] = {}     # S13.16 (c): onarılan alıntının cevaptaki sözleri
    checker.refresh()
    nodes = getattr(checker, "nodes", {})
    sections: set[str] = set()         # bölüm atfı: alıntısız ya da alıntısı bölümün başlığı olan bölüm kimliği
    resolved = []                      # (yeni kimlik ya da None: silinir, alıntı, doğrulandı mı, yer)
    for ident, quote, span in found:
        if (node := nodes.get(ident)) is not None and (not quote or _heading_quote(node, quote)):
            sections.add(ident)
            resolved.append((ident, None, True, span))
            continue
        record = checker.sources([{"id": ident, **({"quote": quote} if quote else {})}])["sources"][0]
        if not record.get("problem"):
            resolved.append((ident, quote, True, span))
            continue
        if quote and _meal_quote(checker, ident, quote):     # S13.11: nâşirin meali, metin değil; doğru aktarılmış
            resolved.append((ident, None, True, span))
            continue
        problems.append({"id": ident, "quote": quote, "problem": record["problem"]})
        fixed = _relocate(checker, ident, quote, read) if quote else _trim(checker, ident)
        segment = text[resolved[-1][3][1] if resolved else 0:span[0]]
        if fixed:
            counts["fixed"] += 1
            resolved.append((fixed, quote, True, span))
        elif quote and (repaired := _repair(checker, ident, quote, segment)):
            counts["repaired"] += 1
            edits[len(resolved)] = repaired[1]
            resolved.append((ident, repaired[0], True, span))
        elif quote:
            counts["unverified"] += 1
            resolved.append((ident, quote, False, span))
        else:
            counts["dropped"] += 1
            resolved.append((None, None, True, span))
    # S13.11: hemen yanındaki işaretin aralığında kalan işaret düşer (taşınan "[[c018..c019]] [[c019]]" → tek numara)
    for i in range(1, len(resolved)):
        (prev, _, prev_ok, (_, prev_end)), (ident, _, ok, (start, _)) = resolved[i - 1], resolved[i]
        if (prev and ident and prev_ok and ok and not text[prev_end:start].strip()
                and _covers(checker, prev, ident)):
            resolved[i] = (None, None, True, resolved[i][3])
    # numaralar: doğrulanan işaretler kimliğe göre birleşir, doğrulanamayan her alıntı ayrı numara alır
    keys: dict[tuple, int] = {}
    quotes: dict[tuple, list[str]] = {}
    for i, (ident, quote, ok, _) in enumerate(resolved):
        if ident is None:
            continue
        key = (ident,) if ok else (ident, i)
        keys.setdefault(key, len(keys) + 1)
        if quote:
            quotes.setdefault(key, []).append(quote)
    sources = []
    plain = [key for key in keys if key[0] not in sections]
    for key in keys:
        if key[0] in sections:
            source = {"n": keys[key], "id": key[0], "cite_as": nodes[key[0]].ref, "section": True}
            if name := source_name(checker, key[0]):
                source["source_name"] = name
            sources.append(source)
    if plain:
        items = [{"id": key[0], **({"quote": " … ".join(quotes[key])} if key in quotes else {})} for key in plain]
        for key, item, record in zip(plain, items, checker.sources(items)["sources"]):
            source = {"n": keys[key], "id": item["id"], "cite_as": record.get("cite_as")}
            if name := source_name(checker, item["id"]):
                source["source_name"] = name
            if record.get("embedded"):
                source["embedded"] = record["embedded"]
            if len(key) > 1 or record.get("problem"):
                source["problem"] = record.get("problem") or "The quoted words are not in the works."
                source["unverified"] = True
            sources.append(source)
    sources.sort(key=lambda source: source["n"])
    raw_out, out, last = [], [], 0          # düz kimlikler işaretlerin arasındaki metinden silinir
    for i, (ident, _, ok, (start, end)) in enumerate(resolved):
        raw_out.append(_drop_leaks(_apply_edits(text[last:start], edits[i]) if i in edits else text[last:start]))
        out.append(raw_out[-1])
        if ident is not None:
            raw_out.append(f"[[{ident}]]")
            out.append(f"[{keys[(ident,) if ok else (ident, i)]}]")
        last = end
    raw_out.append(_drop_leaks(text[last:]))
    out.append(raw_out[-1])
    raw = _dedupe(_tidy("".join(raw_out)), MARK_REPEAT)
    counts.update(_paragraphs(raw))
    markdown = _dedupe(re.sub(r"[ \t]+(\[\d+\])", r" \1", _tidy("".join(out))), NUMBER_REPEAT)
    return Checked(markdown, sources, problems, raw, counts)


# S13.11: taşınan işaret yanındakiyle aynı yere düşünce "[2] [2]" kalıyordu (Haiku, kimin-sözü konuşması)
MARK_REPEAT = re.compile(r"(\[\[\s*([^\[\]\s]+?)\s*\]\])(?:[ \t]*\[\[\s*\2\s*\]\])+")
NUMBER_REPEAT = re.compile(r"(\[(\d+)\])(?:[ \t]*\[\2\])+")


def _dedupe(text: str, pattern: re.Pattern) -> str:
    return pattern.sub(r"\1", text)


# S13.11: model alıntı bloğunu satırın ortasına yazınca ("… söyler: > "…" [[…]] > "…" [[…]]") Markdown onu blok
# saymıyor, okuyucu ">" görüyordu; her blok kendi satırına alınır. Yalnız tırnakla açılan ">" (karşılaştırma değil).
MIDLINE_BLOCK = re.compile(r"(?<=\S)[ \t]+>[ \t]*(?=[\"“])")


def _split_blocks(text: str) -> str:
    out = []
    for line in text.split("\n"):
        if not line.lstrip().startswith(">") and MIDLINE_BLOCK.search(line):
            parts = MIDLINE_BLOCK.split(line)
            line = parts[0].rstrip() + "\n\n" + "\n\n".join("> " + p.strip() for p in parts[1:])
        out.append(line)
    return _dangling_colons("\n".join(out))


# S13.11: Haiku "… şöyle belirtilir: [[…]]" yazıp alıntıyı vermiyordu (tur 4'te bir cevapta altı kez); ardından alıntı
# bloğu ya da liste gelmeyen satırın sonundaki iki nokta noktaya döner.
DANGLING_COLON = re.compile(r":(\s*(?:\[\[[^\[\]]+\]\]\s*)+)$")


def _dangling_colons(text: str) -> str:
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if line.lstrip().startswith(">") or not DANGLING_COLON.search(line):
            continue
        following = next((l.strip() for l in lines[i + 1:] if l.strip()), "")
        if not re.match(r">|[-*•+]\s|\d+[.)]\s", following):          # "**Yorum**" liste değildir
            lines[i] = DANGLING_COLON.sub(lambda m: "." + m.group(1), line)
    return "\n".join(lines)


def source_name(checker, ident: str) -> str | None:
    """Cümlenin ya da bölümün eserinin kaynağı (S12.11: izinlerin şartı), kısa adıyla: "e-Risale", "risaleoku.com".
    Kimliğin ilk parçası eserdir."""
    from risale_mcp.catalog.permissions import SOURCE_LABELS
    row = checker.refresh().execute("SELECT permission FROM works WHERE slug = ?", (ident.split("/")[0],)).fetchone()
    return SOURCE_LABELS.get(row[0]) if row else None


def _heading_quote(node, quote: str) -> bool:
    """Bölüm kimliğinin ardındaki alıntı bölümün başlığı ya da alt başlığı mı (C13: alt başlık alıntılanmıştı)."""
    from risale_mcp.citations import _key
    q = _key(quote)
    return bool(q) and any(q in _key(t) for t in (node.ref.rsplit(" › ", 1)[-1], node.subtitle or "") if t)


def _tidy(text: str) -> str:
    """Silinen işaretin bıraktığı boşluk."""
    text = re.sub(r"(?<=\S)[ \t]+([.,;:!?])", r"\1", re.sub(r"(?<=\S)[ \t]{2,}(?=\S)", " ", text))
    return re.sub(r"[ \t]+$", "", text, flags=re.M)


def _paragraphs(text: str) -> dict:
    """Düz cümledeki iddianın sıklığı için (S12.9): düz yazı paragrafları ve içinde hiç işaret olmayanlar.
    Başlık, alıntı bloğu ve ayraç sayılmaz; giriş ve yorum paragrafları da sayılır, sayı kabadır."""
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    prose = [b for b in blocks if not b.startswith(("#", ">")) and not re.fullmatch(r"[-*_\s]{3,}", b)]
    return {"paragraphs": len(prose), "unmarked": sum(not MARK.search(b) for b in prose)}


def _scope(checker, row) -> list:
    """Cümlenin aralık kurabileceği cümleler (bölümün ana metni ya da aynı hâşiye), ondan başlayarak."""
    where = ("paragraph_id = ?", row["paragraph_id"]) if row["hasiye"] else ("node_id = ? AND hasiye = 0", row["node_id"])
    return checker.refresh().execute(f"SELECT id FROM sentences WHERE {where[0]} AND seq >= ? ORDER BY seq LIMIT ?",
                                     (where[1], row["seq"], MAX_RANGE)).fetchall()


def _range_id(first: str, last: str) -> str:
    if first == last:
        return first
    prefix, _, local = last.rpartition("/")
    return f"{first}..{local}" if prefix == first.rpartition("/")[0] else f"{first}..{last}"


def _passes(checker, ident: str, quote: str | None) -> bool:
    return not checker.sources([{"id": ident, **({"quote": quote} if quote else {})}])["sources"][0].get("problem")


def _seqs(checker, ident: str) -> tuple[int, int] | None:
    from risale_mcp.citations import _full_id
    first_id, _, last_id = ident.partition("..")
    try:
        first = checker.library._sentence(first_id.strip())
        last = checker.library._sentence(_full_id(first["id"], last_id.strip())) if last_id else first
    except Exception:
        return None
    return first["seq"], last["seq"]


def _covers(checker, outer: str, inner: str) -> bool:
    if outer == inner:
        return True
    a, b = _seqs(checker, outer), _seqs(checker, inner)
    return bool(a and b) and a[0] <= b[0] and b[1] <= a[1]


def _meal_quote(checker, ident: str, quote: str) -> bool:
    """Alıntı işaretin cümlelerindeki Arapçanın nâşir mealinden mi (S13.11). Model meali "nâşirin meali" diye tırnakla
    verip işaretliyor; metinde olmadığı için "doğrulanamadı" görünüyordu. Kabul edilir, ama alıntı olarak kaynakçaya
    girmez (işaret alıntısız kalır)."""
    from risale_mcp.citations import _block_parts
    if (span := _seqs(checker, ident)) is None:
        return False
    meals = [r[0] for r in checker.refresh().execute(
        "SELECT a.meal FROM arabic a JOIN sentences s ON s.id = a.sentence_id WHERE s.seq BETWEEN ? AND ? "
        "AND a.meal IS NOT NULL", span)]
    parts = _block_parts(quote)
    return bool(parts and meals) and all(any(p in " ".join(_block_parts(m)) for m in meals) for p in parts)


def _relocate(checker, ident: str, quote: str, read) -> str | None:
    """Alıntının eserlerde bulunduğu en kısa aralık; yoksa None."""
    from risale_mcp.citations import _block_parts
    parts = [p for p in re.split(r"…|\.\.\.", quote) if _block_parts(p)]
    if not parts:
        return None
    rows = [row for _, row in checker._quote_sentences(parts[0], None, RELOCATE_CANDIDATES)]
    if not rows:     # S13.11: iki cümleye yayılan alıntının ilk kelimeleri tek cümlede aranır (dizin cümle başınadır)
        head = re.split(r"(?<=[.!?…])\s+", parts[0].strip().strip('"“”«» '), maxsplit=1)[0]
        if head != parts[0] and len(head.split()) >= 3:
            rows = [row for _, row in checker._quote_sentences(head, None, RELOCATE_CANDIDATES)]
    first_id = ident.split("..")[0].strip()
    node = first_id if first_id in getattr(checker, "nodes", {}) else first_id.rpartition("/")[0]
    work = first_id.split("/")[0]

    def rank(row):
        inside = row["node_id"] == node or row["node_id"].startswith(node + "/")
        return (row["id"] not in read, not inside, row["work"] != work)
    for row in sorted(rows, key=rank):          # sıralama kararlıdır: eşitlikte kitap sırası
        for last in _scope(checker, row):
            candidate = _range_id(row["id"], last["id"])
            if _passes(checker, candidate, quote):
                return candidate
    return None


REPAIR_RATIO = 0.7            # S13.16 (c): tutmayan parçanın metindeki karşılığı için en az harf benzerliği
_EDGE_PUNCT = " \t\n,;:.!?\"“”«»()'’"


def _span_text(checker, ident: str) -> str | None:
    """İşaretin cümlelerinin metni (aralıkta art arda)."""
    if (span := _seqs(checker, ident)) is None or not _passes(checker, ident, None):
        return None
    rows = checker.refresh().execute("SELECT text FROM sentences WHERE seq BETWEEN ? AND ? ORDER BY seq", span)
    return " ".join(r[0] for r in rows)


def _counterpart(part: str, text: str) -> str | None:
    """Parçanın metindeki en yakın karşılığı, metnin kendi sözleriyle; yeterince yakın değilse None. Karşılaştırma
    arama biçiminde (şapka, çengel, büyük harf yok sayılır), harf düzeyinde: "tefekküre teşvik ettiği" →
    "tefekkür mesleğine teşvik ettiği"."""
    from difflib import SequenceMatcher
    want = search_words(part)
    if not want:
        return None
    stream: list[tuple[str, int]] = []          # (kelime, metindeki sözün sırası)
    tokens = list(re.finditer(r"\S+", text))
    for i, token in enumerate(tokens):
        stream.extend((w, i) for w in search_words(token.group()))
    target = " ".join(want)
    best, where = 0.0, None
    for size in range(max(1, len(want) - 3), len(want) + 4):
        for start in range(0, max(0, len(stream) - size) + 1):
            window = stream[start:start + size]
            if not window:
                continue
            matcher = SequenceMatcher(None, target, " ".join(w for w, _ in window), autojunk=False)
            if matcher.real_quick_ratio() <= best or matcher.quick_ratio() <= best:
                continue
            if (ratio := matcher.ratio()) > best:
                best, where = ratio, (window[0][1], window[-1][1])
    if best < REPAIR_RATIO or where is None:
        return None
    return text[tokens[where[0]].start():tokens[where[1]].end()].strip(_EDGE_PUNCT) or None


def _repair(checker, ident: str, quote: str, segment: str) -> tuple[str, list[tuple[str, str]]] | None:
    """S13.16 (c), kullanıcının kararı (2026-11-26): "…" ile birleşen alıntının bir parçası işaretin cümlelerinde
    yoksa ve öbür parçalar varsa, cümle bellidir: tutmayan parça metindeki karşılığıyla değişir, karşılığı yoksa "…"
    olur. Parça cevapta (`segment`: önceki işaretten bu işarete kadarki metin) olduğu gibi bulunamazsa onarılmaz.
    (yeni alıntı, [(eski söz, yeni söz)]) ya da None."""
    from risale_mcp.citations import _key
    pieces = [p.strip().strip('"“”«» ') for p in re.split(r"…|\.\.\.", quote)]
    pieces = [p for p in pieces if _key(p)]
    if len(pieces) < 2 or (text := _span_text(checker, ident)) is None:
        return None
    covered = _key(text)
    good = [_key(p) in covered for p in pieces]
    if all(good) or not any(good):
        return None
    edits, kept = [], []
    for piece, ok in zip(pieces, good):
        if ok:
            kept.append(piece)
            continue
        if piece not in segment:
            return None
        new = _counterpart(piece, text)
        edits.append((piece, new or "…"))
        if new:
            kept.append(new)
    new_quote = " … ".join(kept)
    return (new_quote, edits) if _passes(checker, ident, new_quote) else None


# S13.16 (d), kullanıcının kararı (2026-11-26): işaretsiz tırnaklı söz. Dört ve daha çok kelimelik, ardında işaret
# olmayan tırnak (düz yazıda) ya da işaretsiz alıntı bloğu eserlerde aranır: bulunursa işareti eklenir (kaynağı
# Kaynaklar'a girer), bulunmazsa sözün ardına uyarı konur; söz silinmez (hadis, atasözü, başkasının sözü olabilir).
# Nâşirin ve Vakıf'ın meali, başlık adı ve bulunamayan Arapça dokunulmadan kalır.
UNMARKED_WORDS = 4
UNMARKED_QUOTE = re.compile(r"([\"“«])([^\"“”«»\n\[\]]{3,}?)([\"”»])(?![ \t]*\[\[)")
UNMARKED_NOTE = " (⚠ eserlerde bu sözlerle bulunamadı)"
ARABIC = re.compile(r"[؀-ۿ]")
_TRANSLATIONS: dict[int, list[str]] = {}


def _translations(checker) -> list[str]:
    """Nâşirin mealleri ve Vakıf meali, karşılaştırma biçiminde (veritabanı başına bir kez)."""
    from risale_mcp.citations import _key
    conn = checker.refresh()
    if id(conn) not in _TRANSLATIONS:
        _TRANSLATIONS.clear()
        rows = [r[0] for r in conn.execute("SELECT DISTINCT meal FROM arabic WHERE meal IS NOT NULL")]
        try:
            rows += [r[0] for r in conn.execute("SELECT text FROM quran_translations")]
        except Exception:
            pass
        _TRANSLATIONS[id(conn)] = [_key(r) for r in rows if r]
    return _TRANSLATIONS[id(conn)]


def _place_unmarked(checker, quote: str, read) -> str | None:
    """İşaretsiz sözün yeri: kimlik, uyarı ("") ya da dokunulmaz (None)."""
    from risale_mcp.citations import _block_parts, _key
    parts = _block_parts(quote)
    if not parts or len(" ".join(parts).split()) < UNMARKED_WORDS:
        return None
    meals = _translations(checker)
    if all(any(p in m for m in meals) for p in parts):
        return None
    if _key(quote) in getattr(checker, "by_key", {}):     # bölüm başlığı
        return None
    if found := _relocate(checker, "", quote, read):
        return found
    return None if ARABIC.search(quote) else ""


def unmarked_quotes(checker, text: str, read=frozenset()) -> tuple[str, dict]:
    """İşaretsiz tırnaklı sözlere işaret ya da uyarı ekler; (yeni metin, sayılar)."""
    counts = {"unmarked_found": 0, "unmarked_missing": 0}
    lines = text.split("\n")

    def place(quote: str) -> str | None:
        where = _place_unmarked(checker, quote, read)
        if where:
            counts["unmarked_found"] += 1
            return f" [[{where}]]"
        if where == "":
            counts["unmarked_missing"] += 1
            return UNMARKED_NOTE
        return None

    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith(">"):           # alıntı bloğu: hiç işareti yoksa bütünü bir söz
            j = i
            while j + 1 < len(lines) and lines[j + 1].lstrip().startswith(">"):
                j += 1
            after = lines[j + 1] if j + 1 < len(lines) else ""
            if not any(MARK.search(line) for line in lines[i:j + 1]) and not MARK.search(after):
                if (quote := _quote_text("\n".join(lines[i:j + 1]))) and (add := place(quote)):
                    lines[j] = lines[j].rstrip() + add
            i = j + 1
            continue
        line, out, last = lines[i], [], 0
        for m in UNMARKED_QUOTE.finditer(line):
            out.append(line[last:m.end()])
            last = m.end()
            # işaret aynı cümlede biraz sonra geliyorsa ("… sözü geçer [[…]].") söz işaretlidir
            tail = re.split(r"[\"“«]|[.!?](?:\s|$)", line[m.end():], maxsplit=1)[0]
            if not MARK.search(tail) and (add := place(m.group(2))):
                out.append(add)
        lines[i] = "".join(out) + line[last:]
        i += 1
    return "\n".join(lines), counts


def _apply_edits(segment: str, edits: list[tuple[str, str]]) -> str:
    for old, new in edits:
        at = segment.rfind(old)
        if at >= 0:
            segment = segment[:at] + new + segment[at + len(old):]
    segment = re.sub(r"(?:…|\.\.\.)(?:\s*(?:…|\.\.\.))+", "…", segment)     # atılan parçanın iki yanındaki "…"
    return re.sub(r"([\"“«])\s*…\s*([\"”»])", r"\1…\2", segment)


def _trim(checker, ident: str) -> str | None:
    """Alıntısız işaret: aralığın geçerli kısmı (ters aralık düzelir, uzun aralık 8 cümleye, bölümü aşan aralık bölümün
    sonuna kısalır); kimlik yoksa None."""
    first_id, _, last_id = ident.partition("..")
    try:
        first = checker.library._sentence(first_id.strip())
    except Exception:
        return None
    if last_id:
        from risale_mcp.citations import _full_id
        try:
            last = checker.library._sentence(_full_id(first["id"], last_id.strip()))
            if last["seq"] < first["seq"]:
                first, last = last, first
        except Exception:
            last = None
        ids = [r["id"] for r in _scope(checker, first)]
        if last is not None and last["id"] in ids:
            ids = ids[:ids.index(last["id"]) + 1]
        candidate = _range_id(ids[0], ids[-1])
    else:
        candidate = first["id"]
    return candidate if _passes(checker, candidate, None) else None


# S13.11: düz yazıya yazılmış cümle numarası ("(46. cümle)"): okuyucu numarayı görmez, kaynak işaretten gelir
SENTENCE_NUMBER = re.compile(r"[ \t]*\(\s*\d+\.\s*cümle(?:si)?\s*\)")


def _drop_leaks(text: str) -> str:
    """Düz kimlikler ve cümle numaraları okuyucuya gösterilmez."""
    text = SENTENCE_NUMBER.sub("", BARE_ID.sub("", text))
    return re.sub(r"\([ \t]+", "(", re.sub(r"[ \t]+([.,;:])", r"\1", text))


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
    model_text: str = ""                           # modelin son cevabı, sunucu düzeltmeden önce (`olc`)
    steps: list = field(default_factory=list)      # S13.3: okuyucuya gösterilen adımlar ("… okunuyor")
    survey_places: list | None = None              # S13.13: taramanın bütün yerleri (modele gitmez, sona eklenir)

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


def _sura(args: dict, with_ayah: bool = True) -> str:
    """"Bakara 255": sûre numarası ya da adı, âyetiyle."""
    from risale_mcp.quran import SURA_NAMES
    sura = args.get("sura")
    try:
        sura = SURA_NAMES[int(sura) - 1]
    except (TypeError, ValueError, IndexError):
        sura = str(sura or "").strip()
    ayah = args.get("ayah") if with_ayah else None
    return f"{sura} {ayah}" if ayah else sura


def status_line(library, name: str, args: dict) -> str:
    """S13.3: okuyucuya o an ne yapıldığını söyleyen satır ("Sözler › Yirmi Dokuzuncu Söz okunuyor")."""
    def where(section: str) -> str:
        try:
            return library.outline(section, 0)["ref"]
        except Exception:
            return section
    try:
        match name:
            case "semantic_search":
                return f"“{_short(args.get('query'))}” anlamına yakın yerler aranıyor"
            case "search":
                return f"“{_short(args.get('query'))}” geçen cümleler aranıyor"
            case "read_section":
                return f"{where(args.get('section', ''))} okunuyor"
            case "get_outline":
                return f"{where(args.get('section', ''))} bölümlerine bakılıyor"
            case "get_passage":
                ident = str(args.get("id", "")).split("..")[0]
                return f"{where(ident.rsplit('/', 1)[0])} okunuyor"
            case "find_sentence":
                return f"“{_short(args.get('incipit'))}” cümlesinin yeri aranıyor"
            case "find_ayah":
                return f"{_sura(args)} âyetinin eserlerde geçtiği yerler aranıyor" if args.get("ayah") else \
                    f"{_sura(args)} Sûresi'nin eserlerde geçtiği yerler aranıyor"
            case "get_ayah":
                return f"Kur'ân'dan {_sura(args)} okunuyor"
            case "find_hadith":
                return "Hadisin eserlerdeki yerleri ve kaynakları aranıyor"
            case "get_hadith":
                return "Rivayet kaynağında okunuyor"
            case "lookup_word":
                return f"Lügatte bakılıyor: {_short(', '.join(map(str, args.get('words') or [])))}"
            case "list_works":
                return "Eserlerin listesine bakılıyor"
            case "survey":
                return f"“{_short(args.get('topic'))}” konusunun eserlerdeki yerleri toplanıyor"
    except Exception:
        pass
    return "Eserlere bakılıyor"


THINKING_FIRST = "Soru inceleniyor…"
THINKING_LATER = "Okunanlar değerlendiriliyor…"
CHECKING = "Alıntılar eserlerle denetleniyor, Kaynaklar hazırlanıyor…"


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
    # S12.9: tutmayan alıntıyı sunucu düzeltir; model turu (yol (a)) kapalı. Gerekip gerekmediği deneme ayının
    # sayılarıyla anlaşılır (`SOHBET_MODEL_FIX=1`: önce modele bir kez döner, kalanı sunucu düzeltir).
    model_fix: bool = False

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(model=os.environ.get("SOHBET_MODEL", MODEL), effort=os.environ.get("SOHBET_EFFORT", EFFORT),
                   model_fix=os.environ.get("SOHBET_MODEL_FIX", "") not in ("", "0"))


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
        from risale_mcp.server import LUGAT_INSTRUCTIONS
        self.system = instructions(config.name, lugat=LUGAT_INSTRUCTIONS in self.server.instructions)
        self._tools: list[dict] | None = None

    async def tools(self, mode: str | None = None) -> list[dict]:
        """MCP araçları; seçilen kipin sohbete özgü araçları sona eklenir (S13.12: önbellek önek tutar)."""
        from risale_mcp import kipler
        if self._tools is None:
            self._tools = [{"name": t.name, "description": t.description or "", "input_schema": t.input_schema}
                           for t in await self.server.list_tools() if t.name not in EXCLUDED_TOOLS]
        extra = [kipler.LOCAL_TOOLS[name] for name in kipler.get(mode).tools]
        return self._tools + extra if extra else self._tools

    def messages(self, history: list[dict], question: str, mode: str | None = None) -> list[dict]:
        question = (question or "").strip()
        if not question:
            raise Refusal("Soru boş.")
        if len(question) > MAX_QUESTION:
            raise Refusal(f"Soru çok uzun (en çok {MAX_QUESTION} karakter).")
        if len(history) >= MAX_TURNS:
            raise Refusal(f"Bu konuşma {MAX_TURNS} soruya ulaştı; yeni bir konuşma başlatın.")
        out, size, notes = [], 0, []
        for turn in history:
            q, a = str(turn.get("q", "")).strip(), str(turn.get("a", "")).strip()
            if not q or not a:
                continue
            size += len(q) + len(a)
            out += [{"role": "user", "content": q}, {"role": "assistant", "content": a}]
            notes.append(reads_note(len(notes) + 1, turn.get("r"), self.library))
        if size > MAX_HISTORY:
            raise Refusal("Bu konuşma çok uzadı; yeni bir konuşma başlatın.")
        if notes:     # S13.4 (c): model önceki cevaplarının neye dayandığını görsün (sayfa notu, sorunun önünde)
            question = ("[Page note, not the reader's words: the tools you called for your earlier answers.\n"
                        + "\n".join(notes) + "]\n\n" + question)
        from risale_mcp import kipler
        if instructions := kipler.get(mode).instructions:    # S13.12: kipin talimatı, sistem talimatı önbellekte kalsın
            question = f"[Page note, not the reader's words. {instructions}]\n\n" + question
        return out + [{"role": "user", "content": question}]

    def _params(self, tools: list[dict], messages: list[dict]) -> dict:
        return {"model": self.settings.model, "max_tokens": MAX_TOKENS,
                "system": [{"type": "text", "text": self.system, "cache_control": {"type": "ephemeral"}}],
                "tools": tools, "messages": messages, "cache_control": {"type": "ephemeral"},
                "output_config": {"effort": self.settings.effort}}

    async def _call_tool(self, block) -> dict:
        from mcp.server.mcpserver.exceptions import ToolError
        from risale_mcp import kipler
        args = block.input if isinstance(block.input, dict) else {}
        if block.name in kipler.LOCAL_TOOLS:        # S13.12: sohbetin kendi araçları (kipin)
            return await self._call_local(block, args)
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

    async def _call_local(self, block, args: dict) -> dict:
        from risale_mcp import dosya
        try:
            if block.name == "survey":
                topic = str(args.get("topic") or "").strip()
                if not topic:
                    raise ValueError("Give the topic.")
                terms = [str(t) for t in (args.get("terms") or []) if str(t).strip()][:12]
                result = await asyncio.to_thread(dosya.survey, self.library, topic, terms)
                places = result.pop("places", [])        # S13.13: bütün yerler sayfaya; modele sayımı gider
                return {"type": "tool_result", "tool_use_id": block.id, PAGE_ONLY: places,
                        "content": json.dumps(result, ensure_ascii=False, separators=(",", ":"))}
            raise ValueError(f"Unknown tool {block.name}.")
        except ValueError as e:
            return {"type": "tool_result", "tool_use_id": block.id, "content": str(e), "is_error": True}
        except Exception:
            import logging
            logging.exception("sohbet: yerel araç hatası %s", block.name)
            return {"type": "tool_result", "tool_use_id": block.id, "is_error": True,
                    "content": f"The tool {block.name} failed; try another way."}

    async def ask(self, history: list[dict], question: str, tally: Tally | None = None,
                  mode: str | None = None) -> AsyncIterator[tuple[str, dict]]:
        """(olay, veri) üretir; sonuncusu `done` ya da `error`. `tally` kullanım satırı için doldurulur. `mode`: kip
        (S13.12, `kipler.py`); yoksa serbest soru."""
        from risale_mcp import kipler
        kip = kipler.get(mode)
        tally = tally if tally is not None else Tally()
        messages = self.messages(history, question, kip.id)
        tools = await self.tools(kip.id)
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
            tally.model_text = text
            yield "status", {"text": CHECKING}
            checked = await asyncio.to_thread(check, self.checker, text, read_ids(tally.calls))
            if (self.settings.model_fix and checked.problems and not corrected and tally.rounds < MAX_ROUNDS):
                corrected = True
                messages.append({"role": "user", "content": correction(checked.problems)})
                yield "restart", {"text": "Alıntılar eserlerle denetleniyor; düzeltiliyor…"}
                continue
            markdown, raw = checked.markdown, checked.raw
            if scope := scope_note(tally.calls, checked.sources, history, self.library):
                markdown += "\n\n" + scope                       # S13.14: yalnız sayfada, geçmişe girmez
            if "other_places" in kip.post:
                earlier = earlier_places(history)
                if others := other_places(tally.calls, checked.sources, earlier):
                    markdown, raw = markdown + "\n\n" + others, raw + "\n\n" + others
                if every := all_places(tally.survey_places):    # yalnız sayfada: geçmişe (modele) girmez
                    markdown += "\n\n" + every
            yield "done", {"markdown": markdown, "raw": raw, "sources": checked.sources, "mode": kip.id,
                           "problems": checked.counts["unverified"], "corrected": corrected, "checks": checked.counts,
                           "steps": tally.steps, "reads": reads(tally.calls),
                           "usage": {"cost": round(tally.cost, 5), "tools": tally.tools, "rounds": tally.rounds}}
            return

    async def _loop(self, tools: list[dict], messages: list[dict], tally: Tally):
        while True:
            if tally.rounds >= MAX_ROUNDS:
                yield "error", {"message": "Bu soru için okuma sınırına ulaşıldı. Soruyu daraltarak yeniden sorun."}
                return
            yield "status", {"text": THINKING_LATER if tally.calls else THINKING_FIRST}
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
                tally.steps.append(line := status_line(self.library, block.name, block.input or {}))
                yield "status", {"text": line, "step": True}
                result = await self._call_tool(block)
                if PAGE_ONLY in result:                  # API'ye gitmeyen, sayfanın kullandığı kısım
                    tally.survey_places = result.pop(PAGE_ONLY)
                results.append(result)
                tally.calls.append((block.name, block.input or {}, result["content"], bool(result.get("is_error"))))
            messages.append({"role": "user", "content": results})


OTHER_PLACES = 15           # konu taramasının sonundaki aday listesinde en çok yer
OTHER_PLACES_TITLE = "**Konunun geçtiği öbür yerler** (sayfanın aramasından adaylar; okunmadı, sırası hüküm değildir)"
PAGE_ONLY = "_page"         # yerel aracın sonucunda API'ye gitmeyen kısım (S13.13)
ALL_PLACES_TITLE = ("Kelimelerin geçtiği bütün yerler: {sentences} cümle, {places} yer (kelimeye göre sayıldı; aynı "
                    "harflerle yazılan başka kelimeler de girmiş olabilir)")


def _also(c: dict) -> str:
    """Kopyanın durduğu öbür yer (Tarihçe): "(Tarihçe-i Hayat'ta da)"."""
    works = []
    for x in c.get("also_in", []):
        work = x["ref"].split(" › ")[0]
        if work not in works:
            works.append(work)
    return f" ({', '.join(works)}'ta da)" if works else ""


def earlier_places(history: list[dict]) -> set[str]:
    """S13.13: konuşmanın önceki turlarında okunan ve alıntılanan yerler; "okunmadı" listesine girmezler (haşir
    konuşmasında 1. turda okunan Nokta 2. turun listesinde "okunmadı" diye duruyordu)."""
    out = set()
    for turn in history or []:
        for call in turn.get("r") or []:
            if isinstance(call, str) and (m := _READ_CALL.match(call)) and m.group(1) != "get_outline":
                out.add(_SENTENCE_PART.sub("", m.group(2)))
        out.update(MARK.findall(str(turn.get("a") or "")))
    return {p.split("..")[0] for p in out}


def other_places(calls: list, sources: list[dict], earlier: set[str] = frozenset()) -> str:
    """S13.12: konu taramasının dosyasında olup cevapta anılmayan adaylar, mekanik liste (kullanıcının kararı,
    2026-11-26). Cevabın bir kaynağı adayın içindeyse (ya da aday kaynağın içindeyse) aday anılmış sayılır; bu
    cevapta ya da önceki turlarda okunan yer de (S13.13: liste "okunmadı" der)."""
    dossier = None
    for name, _, result, error in calls:
        if name == "survey" and not error:
            try:
                dossier = json.loads(result)
            except ValueError:
                pass
    if not dossier:
        return ""
    cited = {s["id"].split("..")[0] for s in sources if s.get("id")} | set(earlier)
    for name, args, _, error in calls:
        if not error and name in ("read_section", "get_passage"):
            place = str((args or {}).get("section") or (args or {}).get("id") or "").split("..")[0]
            if place:
                cited.add(_SENTENCE_PART.sub("", place))

    def mentioned(unit: str) -> bool:
        return any(c == unit or c.startswith(unit + "/") or unit.startswith(c + "/") for c in cited)
    rows = [c for c in [*dossier.get("candidates", []), *dossier.get("others", [])] if not mentioned(c["id"])]
    if not rows:
        return ""
    return OTHER_PLACES_TITLE + "\n\n" + "\n".join(f"- {c['ref']}{_also(c)}" for c in rows[:OTHER_PLACES])


def all_places(places: list | None) -> str:
    """S13.13: kelimelerin geçtiği bütün yerler ve sayıları, kapalı bir ek ("her yeri say" isteği; öbür yerler
    listesi 15'le sınırlı). Okunup okunmadığına bakılmaz: sayımdır, hüküm değildir."""
    if not places:
        return ""
    title = ALL_PLACES_TITLE.format(sentences=sum(p["sentences"] for p in places), places=len(places))
    lines = [f"- {p['ref']}{_also(p)} · {p['sentences']} cümle" for p in places]
    return f":::ek {title}\n" + "\n".join(lines) + "\n:::"


SCOPE_TITLE = "Bu cevabın dayandığı okumalar"
SCOPE_ITEMS = 8             # kapsam notunun her satırında en çok yer


def _within(place: str, places) -> bool:
    """`place` okunan yerlerden birinin kendisi, içi ya da (cümle okunduysa) cümlesinin bölümü mü."""
    return any(place == p or place.startswith(p + "/") or p.startswith(place + "/") for p in places)


def scope_note(calls: list, sources: list[dict], history: list[dict] | None = None, library=None) -> str:
    """S13.14: cevabın altında, kapalı ek: neye dayandığı ve neyi okumadan söylediği (araştırma: güvenin kaynağı
    şeffaflık; Harvey'in "kapsam notu"). Mekaniktir, araçların sonuçlarından kurulur:
    - **kısmen okunan bölümler:** `read_section` sayfalarının kapsadığı cümleler bölümün tamamı değilse;
    - **metnin gönderdiği, okunmayan yerler:** cevabın dayandığı bölümlerdeki (Kaynaklar'ın cümlelerinin bölümü)
      `points_to` hedeflerinden bu konuşmada okunmayanlar; okunan her sayfanın bütün göndermeleri değil (haşir
      denemesinde 11'e çıkıyordu, çoğu soruyla ilgisiz). Bir göndermenin birden çok hedefi ("Nokta Risalesi": Nokta
      ve Mesnevî'deki Nokta) tek satırdır, biri okunduysa izlenmiş sayılır;
    - **okunmadan dayanılan yerler:** kaynağı okuma araçlarıyla okunmamış (yalnız arama sonucundan) alıntılar;
    - **okunanlar:** okunan bölümler.
    Okuma çağrısı olmayan cevapta (ör. yalnız selamlaşma) not yoktur."""
    pages: dict[str, dict] = {}                 # bölüm -> {ref, total, covered: set}
    passages: dict[str, dict] = {}
    pointers_seen: list[tuple[list[dict], str]] = []    # (hedefler, gönderen cümle)
    read_places: set[str] = set()
    for name, args, result, error in calls:
        if error or name not in ("read_section", "get_passage"):
            continue
        try:
            data = json.loads(result)
        except (TypeError, ValueError):
            continue
        section = data.get("section")
        if not section:
            continue
        read_places.add(section)
        if name == "read_section":
            entry = pages.setdefault(section, {"ref": data.get("ref"), "total": None, "covered": set(), "whole": False})
            coverage = data.get("coverage")
            if coverage is None:
                entry["whole"] = True
            else:
                a, _, b = str(coverage.get("sentences", "")).partition("–")
                if a.isdigit() and b.isdigit():
                    entry["covered"].update(range(int(a), int(b) + 1))
                    entry["total"] = coverage.get("of")
        else:
            part = data.get("of_section")
            entry = passages.setdefault(section, {"ref": data.get("section_ref"), "count": 0, "of": None})
            entry["count"] += part["sentences"] if part else 0
            entry["of"] = part["of"] if part else None
        for point in data.get("points_to") or []:
            if point.get("to"):
                pointers_seen.append((point["to"], point.get("sentence", "")))
    if not pages and not passages:
        return ""
    earlier = earlier_places(history or [])
    whole = {s for s, e in pages.items() if e["whole"] or (e["total"] and len(e["covered"]) >= e["total"])}
    partial = [(e["ref"], len(e["covered"]), e["total"]) for s, e in pages.items() if s not in whole and e["total"]]
    partial += [(e["ref"], e["count"], e["of"]) for s, e in passages.items()
                if e["of"] and e["count"] < e["of"] and not _within(s, whole) and not _within(s, pages)]
    relied = {_SENTENCE_PART.sub("", str(src.get("id") or "").split("..")[0]) for src in sources}
    pending, seen = [], set()
    for targets, sentence in pointers_seen:
        source = _SENTENCE_PART.sub("", sentence) if sentence else ""
        ids = tuple(t["id"] for t in targets)
        if source not in relied or ids in seen or any(_within(t, read_places | earlier) for t in ids):
            continue
        seen.add(ids)
        pending.append((" / ".join(t.get("ref") or t["id"] for t in targets), _place_ref(library, source)))
    ids = read_ids(calls)
    unread = []
    for src in sources:
        first = str(src.get("id") or "").split("..")[0]
        if first and first not in ids and not _within(first.rsplit("/", 1)[0], earlier | read_places):
            ref = str(src.get("cite_as") or first).split(" › “")[0]
            if ref not in unread:
                unread.append(ref)
    lines = []
    if partial:
        lines.append("- **Kısmen okunanlar:** " + "; ".join(f"{ref} ({n}/{of} cümle)" for ref, n, of in partial[:SCOPE_ITEMS]))
    if pending:
        lines.append("- **Metnin gönderdiği, bu konuşmada okunmayan yerler:** "
                     + "; ".join(f"{ref}" + (f" (gönderen: {src})" if src else "") for ref, src in pending[:SCOPE_ITEMS]))
    if unread:
        lines.append("- **Okunmadan, yalnız arama sonucundan dayanılanlar:** " + "; ".join(unread[:SCOPE_ITEMS]))
    full = [pages[s]["ref"] for s in pages if s in whole]
    if full:
        lines.append("- **Okunanlar:** " + "; ".join(full[:SCOPE_ITEMS]) + (" …" if len(full) > SCOPE_ITEMS else ""))
    flags = [f"{len(partial)} yer kısmen okundu" if partial else "", f"{len(pending)} gönderme okunmadı" if pending else "",
             f"{len(unread)} yer okunmadan" if unread else ""]
    summary = ", ".join(f for f in flags if f) or "dayanılan yerler okundu"
    return f":::ek {SCOPE_TITLE}: {summary}\n" + "\n".join(lines) + "\n:::"


def _place_ref(library, node_id: str) -> str:
    if not node_id or library is None:
        return node_id
    try:
        return library._node(node_id)["ref"]
    except Exception:
        return node_id


MAX_READS = 30              # bir cevabın kaydedilen en çok araç çağrısı
MAX_READ_LINE = 160


def reads(calls: list) -> list[str]:
    """S13.4 (c): cevabın çağırdığı araçlar, kısa satırlar ("read_section(section=sozler/11)"); sonraki soruda modele
    sayfa notu olarak gider (geçmişe yalnız cevabın metni girer, araç sonuçları girmez)."""
    out = []
    for name, args, _, error in calls[:MAX_READS]:
        shown = ", ".join(f"{k}={v}" for k, v in (args or {}).items() if v not in (None, "", []))
        line = f"{name}({shown})" + (" -> error" if error else "")
        out.append(line if len(line) <= MAX_READ_LINE else line[:MAX_READ_LINE - 1] + "…")
    return out


def reads_note(n: int, calls, library=None) -> str:
    if calls is None:
        return f"Answer {n}: not recorded."
    if not isinstance(calls, list):          # tarayıcıdan bozuk geldiyse: kayıt yok sayılır
        return f"Answer {n}: not recorded."
    calls = [read_place(library, str(c)[:MAX_READ_LINE]) for c in calls[:MAX_READS]]
    return f"Answer {n}: " + ("; ".join(calls) if calls else "no tools called.")


_READ_CALL = re.compile(r"^(?:(read_section|get_outline)\(section=|get_passage\(id=)([^,)\s]+)")
_SENTENCE_PART = re.compile(r"/c\d{3}(?:/[hs]\d+/c\d{3})?(?:\.\.c\d{3})?$")


def read_place(library, call: str) -> str:
    """S13.7 (3): okuma çağrısının ardına okunan yerin başlığı ("… = read: Lem'alar › İkinci Lem'a › …"). Model
    kimlikten yeri çıkaramayıp okuduğu bölüm için "okumadım" diyordu (tevekkül konuşması, 2026-11-25). Başlık notu
    kurarken bulunur: eski turlarda da çalışır; bulunamazsa çağrı olduğu gibi kalır."""
    m = _READ_CALL.match(call)
    if library is None or not m or call.endswith("-> error"):
        return call
    section = _SENTENCE_PART.sub("", m.group(2))
    try:
        ref = library.outline(section, 0)["ref"]
    except Exception:
        return call
    return f"{call} = {'outline of' if m.group(1) == 'get_outline' else 'read'}: {ref}"


READING_TOOLS = {"read_section", "get_passage", "find_sentence"}
_RESULT_ID = re.compile(r'"id"\s*:\s*"([^"]+/c\d{3}(?:/[hs]\d+/c\d{3})?)"')


def read_ids(calls: list) -> set[str]:
    """Modelin okuduğu cümleler: okuma araçlarının sonucundaki cümle kimlikleri (arama sonuçları okuma sayılmaz)."""
    return {m for name, _, result, error in calls if name in READING_TOOLS and not error
            for m in _RESULT_ID.findall(result or "")}


# ---------------------------------------------------------------- kota ve bütçe (S12.4)

@dataclass
class Limits:
    """Kullanıcının kararı (2026-11-25): kişi başına günde 10 soru; servis günde 5 $, ayda 100 $ (dolunca herkese
    "bugünlük doldu"); günlük harcama 2 $'ı geçince ntfy bildirimi. Gün ve ay İstanbul saatiyle. Console'daki aylık
    tavan yedektir. Maliyet her cevabın `usage`'ından hesaplanan yaklaşık tutardır (`cost`)."""
    questions: int = 10
    daily: float = 5.0
    monthly: float = 100.0
    alert: float = 2.0
    # Günlük soru sınırı olmayan hesaplar (kullanıcının kararı, 2026-11-25: yönetici hata ayıklamak için çok soracak).
    # Adresler koda değil `.env`'e yazılır (`SOHBET_SINIRSIZ`, virgülle); bütçe tavanları onlar için de geçerlidir.
    unlimited: frozenset = frozenset()

    @classmethod
    def from_env(cls) -> "Limits":
        d = cls()
        return cls(questions=int(os.environ.get("SOHBET_GUNLUK_SORU", d.questions)),
                   daily=float(os.environ.get("SOHBET_GUNLUK_BUTCE", d.daily)),
                   monthly=float(os.environ.get("SOHBET_AYLIK_BUTCE", d.monthly)),
                   alert=float(os.environ.get("SOHBET_UYARI", d.alert)),
                   unlimited=frozenset(sohbet_hesap.norm_email(e) for e in
                                       os.environ.get("SOHBET_SINIRSIZ", "").split(",") if e.strip()))

    def counted(self, email: str) -> bool:
        """Bu hesabın günlük soru sınırı var mı?"""
        return email not in self.unlimited


TZ = "Europe/Istanbul"
NTFY_FILE = Path(__file__).resolve().parents[2] / "data" / "sohbet-ntfy"   # ntfy.sh konusu (git'e girmez)


def _starts(now: float) -> tuple[float, float]:
    """Bugünün ve bu ayın başı (İstanbul saatiyle), zaman damgası."""
    from datetime import datetime
    from zoneinfo import ZoneInfo
    t = datetime.fromtimestamp(now, ZoneInfo(TZ))
    day = t.replace(hour=0, minute=0, second=0, microsecond=0)
    return day.timestamp(), day.replace(day=1).timestamp()


def spent(store: Store, now: float | None = None) -> tuple[float, float]:
    """Bugün ve bu ay harcanan, $."""
    day, month = _starts(time.time() if now is None else now)
    row = store._run("SELECT COALESCE(SUM(CASE WHEN ts >= ? THEN cost END), 0), COALESCE(SUM(cost), 0) FROM usage "
                     "WHERE ts >= ?", (day, month))[0]
    return row[0], row[1]


def asked_today(store: Store, email: str, now: float | None = None) -> int:
    day, _ = _starts(time.time() if now is None else now)
    return store._run("SELECT COUNT(*) FROM usage WHERE email = ? AND ts >= ?", (email, day))[0][0]


def refusal(store: Store, email: str, limits: Limits, now: float | None = None) -> str | None:
    """Soru sorulamıyorsa okuyucuya gösterilecek ileti."""
    today, month = spent(store, now)
    if month >= limits.monthly:
        return "Bu ayın sohbet bütçesi doldu; sayfa gelecek ayın başında yeniden açılır."
    if today >= limits.daily:
        return "Bugünlük sohbet bütçesi doldu; yarın yeniden sorabilirsiniz."
    if limits.counted(email) and asked_today(store, email, now) >= limits.questions:
        return f"Bugünlük soru hakkınız ({limits.questions}) doldu; yarın yeniden sorabilirsiniz."
    return None


def alerts(before: tuple[float, float], after: tuple[float, float], limits: Limits) -> list[str]:
    """Bu soruyla aşılan eşikler: günlük uyarı, günlük tavan, aylık tavanın %80'i ve tamamı."""
    out = []
    for (b, a), limit, text in (((before[0], after[0]), limits.alert, "Günlük harcama {:.2f} $ oldu (uyarı eşiği {:g} $)"),
                                ((before[0], after[0]), limits.daily, "Günlük tavan doldu: {:.2f} $ ({:g} $); sayfa yarına kadar kapalı"),
                                ((before[1], after[1]), limits.monthly * .8, "Aylık harcama {:.2f} $ (tavanın %80'i: {:g} $)"),
                                ((before[1], after[1]), limits.monthly, "Aylık tavan doldu: {:.2f} $ ({:g} $); sayfa ay sonuna kadar kapalı")):
        if b < limit <= a:
            out.append(text.format(a, limit))
    return out


def notify(text: str) -> None:
    """Telefona bildirim (ntfy.sh; konu `SOHBET_NTFY` ya da `data/sohbet-ntfy`); arka planda, sohbeti bekletmez."""
    topic = os.environ.get("SOHBET_NTFY") or (NTFY_FILE.read_text().strip() if NTFY_FILE.exists() else None)
    import logging
    logging.warning("sohbet: %s", text)
    if not topic:
        return

    def send():
        import urllib.request
        try:
            urllib.request.urlopen(urllib.request.Request(f"https://ntfy.sh/{topic}",
                                                          data=f"Sohbet sayfası\n{text}".encode("utf-8")), timeout=20)
        except OSError as e:
            logging.warning("sohbet: bildirim gitmedi: %s", e)
    import threading
    threading.Thread(target=send, daemon=True).start()


# ---------------------------------------------------------------- konuşmalar (S13.1)

def title_of(question: str) -> str:
    """İlk sorudan başlık: tek satır, kelime sınırında kısaltılır (modele yazdırılmaz)."""
    text = " ".join(question.split())
    if len(text) <= MAX_TITLE:
        return text
    cut = text[:MAX_TITLE].rsplit(" ", 1)[0]
    return (cut if len(cut) >= MAX_TITLE // 2 else text[:MAX_TITLE]).rstrip(" ,.;:") + "…"


class Conversations:
    """Hesapta saklanan konuşmalar. Her işlem sahibin adresiyle süzülür: başkasının konuşması yok sayılır."""

    def __init__(self, store: Store) -> None:
        self.store = store

    def keeps(self, email: str) -> bool:
        row = self.store._run("SELECT keep_history FROM users WHERE email = ?", (email,))
        return bool(row and row[0][0])

    def set_keeps(self, email: str, on: bool) -> None:
        self.store._run("UPDATE users SET keep_history = ? WHERE email = ?", (int(on), email))

    def owned(self, email: str, ident: str) -> bool:
        return bool(self.store._run("SELECT 1 FROM conversations WHERE id = ? AND email = ?", (ident, email)))

    def listing(self, email: str) -> list[dict]:
        rows = self.store._run("SELECT id, title, updated FROM conversations WHERE email = ? ORDER BY updated DESC "
                               "LIMIT ?", (email, MAX_LISTED))
        return [dict(r) for r in rows]

    def turns(self, email: str, ident: str) -> list[dict] | None:
        if not self.owned(email, ident):
            return None
        rows = self.store._run("SELECT n, question, raw, markdown, sources, corrected, feedback, steps, reads, mode FROM "
                               "turns WHERE conversation = ? ORDER BY n", (ident,))
        return [{"n": r["n"], "q": r["question"], "a": r["raw"], "markdown": r["markdown"],
                 "sources": json.loads(r["sources"]), "corrected": bool(r["corrected"]), "feedback": r["feedback"],
                 "steps": json.loads(r["steps"] or "[]"), "r": None if r["reads"] is None else json.loads(r["reads"]),
                 "mode": r["mode"] or "serbest"}
                for r in rows]

    def get(self, email: str, ident: str) -> dict | None:
        turns = self.turns(email, ident)
        if turns is None:
            return None
        title = self.store._run("SELECT title FROM conversations WHERE id = ?", (ident,))[0][0]
        return {"id": ident, "title": title, "turns": turns}

    def add(self, email: str, ident: str | None, question: str, done: dict, now: float | None = None) -> tuple[str, int]:
        """Cevabı biten turu yazar; konuşma yoksa açar. (konuşma kimliği, turun sırası)."""
        import secrets
        now = time.time() if now is None else now
        with self.store._conn() as c:
            if ident is None:
                ident = secrets.token_urlsafe(12)
                c.execute("INSERT INTO conversations (id, email, title, created, updated) VALUES (?, ?, ?, ?, ?)",
                          (ident, email, title_of(question), now, now))
                n = 0
            else:
                n = c.execute("SELECT COALESCE(MAX(n) + 1, 0) FROM turns WHERE conversation = ?", (ident,)).fetchone()[0]
                c.execute("UPDATE conversations SET updated = ? WHERE id = ? AND email = ?", (now, ident, email))
            c.execute("INSERT INTO turns (conversation, n, ts, question, raw, markdown, sources, corrected, steps, "
                      "reads, mode) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (ident, n, now, question.strip(), done["raw"], done["markdown"],
                       json.dumps(done["sources"], ensure_ascii=False), int(bool(done.get("corrected"))),
                       json.dumps(done.get("steps") or [], ensure_ascii=False),
                       json.dumps(done.get("reads") or [], ensure_ascii=False), done.get("mode") or "serbest"))
        return ident, n

    def rename(self, email: str, ident: str, title: str) -> bool:
        title = " ".join(str(title).split())[:MAX_TITLE]
        if not title:
            return False
        with self.store._conn() as c:
            return c.execute("UPDATE conversations SET title = ? WHERE id = ? AND email = ?",
                             (title, ident, email)).rowcount == 1

    def delete(self, email: str, ident: str | None = None) -> int:
        """Bir konuşmayı ya da (`ident` yoksa) hepsini siler; turları da gider."""
        with self.store._conn() as c:
            where, params = ("email = ?", (email,)) if ident is None else ("id = ? AND email = ?", (ident, email))
            c.execute(f"DELETE FROM turns WHERE conversation IN (SELECT id FROM conversations WHERE {where})", params)
            return c.execute(f"DELETE FROM conversations WHERE {where}", params).rowcount

    def vote(self, email: str, ident: str, n: int, vote: int) -> None:
        self.store._run("UPDATE turns SET feedback = ? WHERE conversation = ? AND n = ? AND conversation IN "
                        "(SELECT id FROM conversations WHERE email = ?)", (vote, ident, n, email))


# ---------------------------------------------------------------- kullanım satırı

def log_usage(store: Store, email: str | None, model: str, tally: Tally, seconds: float, outcome: str,
              done: dict | None = None) -> None:
    checks = (done or {}).get("checks", {})
    row = {"ts": time.time(), "email": email, "model": model, "rounds": tally.rounds, "tools": tally.tools,
           "input": tally.input, "output": tally.output, "cache_write": tally.cache_write,
           "cache_read": tally.cache_read, "cost": round(tally.cost, 6), "seconds": round(seconds, 2),
           "sources": len(done["sources"]) if done else None, "problems": done["problems"] if done else None,
           "corrected": int(done["corrected"]) if done else None, "outcome": outcome,
           **{k: checks.get(k) if done else None for k in ("fixed", "dropped", "leaks", "paragraphs", "unmarked")}}
    store._run(f"INSERT INTO usage ({', '.join(row)}) VALUES ({', '.join('?' * len(row))})", tuple(row.values()))
    store._run("DELETE FROM usage WHERE ts < ?", (row["ts"] - USAGE_DAYS * 86400,))


# ---------------------------------------------------------------- web

def feedback_row(body: dict, email: str, model: str) -> dict:
    """S12.12: geri bildirim satırı. Soru ve cevap yalnız `share` işaretliyse saklanır (konuşma sunucuda tutulmaz)."""
    vote = int(body.get("vote"))
    if vote not in (1, -1):
        raise ValueError("vote")
    note = str(body.get("note") or "").strip()[:MAX_NOTE] or None
    share = body.get("share") is True
    question = str(body.get("question") or "").strip()[:MAX_SHARED] if share else None
    answer = str(body.get("answer") or "").strip()[:MAX_SHARED] if share else None
    return {"ts": time.time(), "email": email, "vote": vote, "note": note, "question": question or None,
            "answer": answer or None, "model": model}


def source_text(chat: "Chat", ident: str) -> dict:
    """Kaynağın metni: bölüm atfında bölümün başı, cümle ya da aralıkta işaretli cümleler ve çevresi. Atıf dizini ilk
    denetimde kurulur: servis yeniden başlayıp henüz soru sorulmadıysa yoktu, her kaynak "bulunamadı" diyordu
    (2026-11-25); önce kurulur."""
    chat.checker.refresh()
    passage = section_opening(chat.checker, ident) if ident in chat.checker.nodes else chat.library.passage(ident, 3)
    return arabic_refs(chat.library, passage)


def arabic_refs(library, passage: dict) -> dict:
    """S13.7 (1): her cümlenin âyet ve hadis satırları (`refs`: kaynakçanın alt satırı, "Hadis: … (doğrulanmadı)",
    ve nâşirin meali). Sayfanın Kaynaklar listesi bu satırları artık göstermez, metin paneli gösterir; meali olmayan
    parçanın adresi ve hadisin notu da orada görünsün. Adresi olmayan ama meali olan parça (arabi) eskisi gibi."""
    sentences = passage.get("sentences", [])
    found: dict[str, list[dict]] = {}
    for entry in library.embedded([s["id"] for s in sentences]):
        found.setdefault(entry["sentence_id"], []).append(entry)
    for sentence in sentences:
        meals = {a.get("text"): a.get("publisher_translation") for a in sentence.get("arabic") or []
                 if a.get("publisher_translation")}
        refs, seen = [], set()
        for entry in found.get(sentence["id"], []):
            if entry["line"] not in seen:
                seen.add(entry["line"])
                refs.append({"line": entry["line"], "meal": meals.pop(entry["text"], None)})
        for part in sentence.get("arabic") or []:
            if part.get("text") in meals:
                refs.append({"line": part.get("source") or "", "meal": meals.pop(part["text"])})
        if refs:
            sentence["refs"] = refs
    return passage


def section_opening(checker, ident: str) -> dict:
    """Bölüm atfının metni: bölümün ilk cümleleri (işaretli cümle yok)."""
    node = checker.nodes[ident]
    row = checker.refresh().execute("SELECT id FROM sentences WHERE (node_id = ? OR node_id LIKE ?) AND hasiye = 0 "
                                    "ORDER BY seq LIMIT 1", (ident, ident + "/%")).fetchone()
    if row is None:
        raise LookupError(ident)
    passage = checker.library.passage(row[0], 6)
    for sentence in passage.get("sentences", []):
        sentence["target"] = False
    passage["section_ref"] = node.ref
    return passage


def page(config: Config, email: str) -> str:
    import html as _html
    version = _asset_version()
    return ((ASSETS / "sohbet.html").read_text(encoding="utf-8")
            .replace("{{P}}", _html.escape(config.prefix)).replace("{{NAME}}", _html.escape(config.name))
            .replace("{{EMAIL}}", _html.escape(email)).replace("{{INITIAL}}", _html.escape(email[:1].upper()))
            .replace("{{V}}", version)
            .replace("{{KIPLER}}", _html.escape(json.dumps(_kipler_public(), ensure_ascii=False))))


def _kipler_public() -> list[dict]:
    from risale_mcp import kipler
    return kipler.public()


def _asset_version() -> str:
    import hashlib
    h = hashlib.sha256()
    for name in ("sohbet.js", "sohbet.css"):
        h.update((ASSETS / name).read_bytes())
    return h.hexdigest()[:10]


CSP = ("default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self'; "
       "font-src 'self'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'")


def routes(chat: Chat, store: Store, config: Config, limits: Limits = Limits()):
    from starlette.requests import Request
    from starlette.responses import FileResponse, HTMLResponse, JSONResponse, StreamingResponse
    from starlette.routing import Route

    p = config.prefix
    busy: set[str] = set()
    headers = {"Cache-Control": "no-store", "Referrer-Policy": "no-referrer", "Content-Security-Policy": CSP}
    convs = Conversations(store)
    signed_out = {"error": "Oturumunuz kapanmış; yeniden giriş yapın."}

    def user(request: Request) -> str | None:
        return store.check(request.cookies.get(COOKIE))

    def reply(data: dict, status: int = 200) -> JSONResponse:
        return JSONResponse(data, status_code=status, headers=headers)

    async def json_body(request: Request) -> dict | None:
        if not request.headers.get("content-type", "").startswith("application/json"):
            return None
        try:
            body = await request.json()
        except Exception:
            return None
        return body if isinstance(body, dict) else None

    def remaining(email: str) -> int | None:
        """Bugün kalan soru; sınırsız hesapta None (sayfa hakkı göstermez)."""
        return max(0, limits.questions - asked_today(store, email)) if limits.counted(email) else None

    def home(request: Request, email: str) -> HTMLResponse:
        return HTMLResponse(page(config, email), headers=headers)

    async def asset(request: Request):
        name = request.path_params["name"]
        media = {"sohbet.js": "text/javascript", "sohbet.css": "text/css", "naskh.woff2": "font/woff2"}.get(name)
        if not media:
            return JSONResponse({"error": "yok"}, status_code=404)
        return FileResponse(ASSETS / name, media_type=media, headers={"Cache-Control": "public, max-age=31536000"})

    async def text(request: Request):
        if not user(request):
            return JSONResponse({"error": "oturum yok"}, status_code=401, headers=headers)
        ident = request.query_params.get("id", "")[:300]
        try:
            passage = await asyncio.to_thread(source_text, chat, ident)
        except Exception:
            return JSONResponse({"error": "Bu adreste metin bulunamadı."}, status_code=404, headers=headers)
        return JSONResponse(passage, headers=headers)

    async def ask(request: Request):
        email = user(request)
        if not email:
            return reply(signed_out, 401)
        if not request.headers.get("content-type", "").startswith("application/json"):
            return JSONResponse({"error": "geçersiz istek"}, status_code=415, headers=headers)
        try:
            body = await request.json()
            question = str(body.get("question", ""))
            from risale_mcp import kipler
            mode = kipler.get(str(body.get("mode") or "")).id      # S13.12: bilinmeyen kip serbest soru sayılır
            conversation = body.get("conversation")
            if conversation is not None:
                conversation = str(conversation)[:64]
                history = convs.turns(email, conversation)      # saklanan konuşmanın geçmişi sunucudan
                if history is None:
                    return reply({"error": "Bu konuşma bulunamadı; yeni bir konuşma başlatın."}, 404)
                keep = True
            else:
                keep = convs.keeps(email)
                history = [] if keep else [t for t in body.get("history", []) if isinstance(t, dict)][:MAX_TURNS + 1]
        except Exception:
            return JSONResponse({"error": "geçersiz istek"}, status_code=400, headers=headers)
        if email in busy:
            return JSONResponse({"error": "Önceki sorunuzun cevabı sürüyor."}, status_code=429, headers=headers)
        if message := refusal(store, email, limits):
            return JSONResponse({"error": message}, status_code=429, headers=headers)

        async def stream():
            busy.add(email)
            tally, start, outcome, done = Tally(), time.time(), "cancelled", None
            try:
                async for event, data in chat.ask(history, question, tally, mode):
                    if event == "done":
                        outcome, done = "done", data
                        left = remaining(email)
                        data["remaining"] = None if left is None else max(0, left - 1)
                        data["questions"] = limits.questions if limits.counted(email) else None
                        if keep:
                            data["conversation"], data["n"] = convs.add(email, conversation, question, data)
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
                    before = spent(store)
                    log_usage(store, email, chat.settings.model, tally, time.time() - start, outcome, done)
                    for text in alerts(before, spent(store), limits):
                        notify(text)

        return StreamingResponse(stream(), media_type="text/event-stream",
                                 headers={**headers, "X-Accel-Buffering": "no"})

    async def feedback(request: Request):
        email = user(request)
        if not email:
            return reply(signed_out, 401)
        try:
            body = await request.json()
            row = feedback_row(body, email, chat.settings.model)
        except (ValueError, TypeError, AttributeError):
            return JSONResponse({"error": "geçersiz istek"}, status_code=400, headers=headers)
        # S13.4: oy tıklanınca gider (Gönder düğmesi yok); not, onay kutusu ve oyun değişmesi aynı satırı günceller
        ident = body.get("id")
        if ident is not None:
            if not isinstance(ident, int) or isinstance(ident, bool):
                return JSONResponse({"error": "geçersiz istek"}, status_code=400, headers=headers)
            if not store._run("UPDATE feedback SET vote = ?, note = ?, question = ?, answer = ? WHERE rowid = ? AND "
                              "email = ? RETURNING rowid", (row["vote"], row["note"], row["question"], row["answer"],
                                                             ident, email)):
                return JSONResponse({"error": "Bu geri bildirim bulunamadı."}, status_code=404, headers=headers)
        else:
            today = store._run("SELECT COUNT(*) FROM feedback WHERE email = ? AND ts >= ?",
                               (email, time.time() - 86400))[0][0]
            if today >= FEEDBACK_PER_DAY:
                return JSONResponse({"error": "Bugün için yeterince geri bildirim gönderdiniz; teşekkürler."},
                                    status_code=429, headers=headers)
            ident = store._run(f"INSERT INTO feedback ({', '.join(row)}) VALUES ({', '.join('?' * len(row))}) "
                               "RETURNING rowid", tuple(row.values()))[0][0]
            store._run("DELETE FROM feedback WHERE ts < ?", (row["ts"] - FEEDBACK_DAYS * 86400,))
        if isinstance(body.get("conversation"), str) and isinstance(body.get("n"), int):
            convs.vote(email, body["conversation"], body["n"], row["vote"])     # saklanan turda oy görünsün
        return JSONResponse({"ok": True, "id": ident}, headers=headers)

    # ------------------------------------------------ S13.1: durum, ayar, konuşmalar

    async def status(request: Request):
        email = user(request)
        if not email:
            return reply(signed_out, 401)
        return reply({"email": email, "keep": convs.keeps(email),
                      "questions": limits.questions if limits.counted(email) else None, "remaining": remaining(email)})

    async def settings(request: Request):
        email = user(request)
        if not email:
            return reply(signed_out, 401)
        body = await json_body(request)
        if body is None or not isinstance(body.get("keep"), bool):
            return reply({"error": "geçersiz istek"}, 400)
        convs.set_keeps(email, body["keep"])
        return reply({"ok": True, "keep": body["keep"]})

    async def listing(request: Request):
        email = user(request)
        if not email:
            return reply(signed_out, 401)
        return reply({"conversations": convs.listing(email)})

    async def conversation(request: Request):
        email = user(request)
        if not email:
            return reply(signed_out, 401)
        found = convs.get(email, request.query_params.get("id", "")[:64])
        if found is None:
            return reply({"error": "Bu konuşma bulunamadı."}, 404)
        for turn in found["turns"]:
            del turn["a"], turn["r"]                       # modelin ham metni ve araç kaydı sayfaya gerekmez
        return reply(found)

    async def rename(request: Request):
        email = user(request)
        if not email:
            return reply(signed_out, 401)
        body = await json_body(request)
        if body is None or not convs.rename(email, str(body.get("id", ""))[:64], str(body.get("title", ""))):
            return reply({"error": "Ad değiştirilemedi."}, 400)
        return reply({"ok": True})

    async def remove(request: Request):
        email = user(request)
        if not email:
            return reply(signed_out, 401)
        body = await json_body(request)
        if body is None or not (body.get("all") is True or isinstance(body.get("id"), str)):
            return reply({"error": "geçersiz istek"}, 400)
        count = convs.delete(email, None if body.get("all") is True else body["id"][:64])
        return reply({"ok": True, "deleted": count})

    return home, [Route(f"{p}api/sor", ask, methods=["POST"]), Route(f"{p}api/metin", text),
                  Route(f"{p}api/geri-bildirim", feedback, methods=["POST"]), Route(f"{p}static/{{name}}", asset),
                  Route(f"{p}api/durum", status), Route(f"{p}api/ayarlar", settings, methods=["POST"]),
                  Route(f"{p}api/konusmalar", listing), Route(f"{p}api/konusma", conversation),
                  Route(f"{p}api/konusma/ad", rename, methods=["POST"]),
                  Route(f"{p}api/konusma/sil", remove, methods=["POST"])]


def build(chat: Chat, store: Store, mailer, config: Config, limits: Limits = Limits()):
    home, extra = routes(chat, store, config, limits)
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


# ---------------------------------------------------------------- ölçüm (S12.1'in teyidi, S12.13)

# Hızlı set (S12.13, kullanıcının kararı): her değişiklikte bu 8 soru; 29 sorunun tamamı model ya da talimat
# değişiminde ve deploy'dan önce. 8 soru yalnız büyük farkı gösterir.
QUICK = ["A1", "B7", "C11", "D15", "E19", "K2", "K4", "T2"]

def answer_text(done: dict) -> str:
    """Okuyucunun gördüğü cevap düz metin olarak: cevap ve Kaynaklar (altın soru denetimi bunu okur)."""
    lines = [done["markdown"].rstrip(), "", "Kaynaklar"]
    for s in done["sources"]:
        lines.append(f"[{s['n']}] {s.get('cite_as') or 'Adresi bulunamadı'}" + (" ⚠ doğrulanamadı" if s.get("unverified") else ""))
        lines += [f"  - {e['line']}" for e in s.get("embedded", ())]
    return "\n".join(lines) if done["sources"] else done["markdown"]


async def measure(chat: Chat, ids: list[str]) -> Path:
    """Altın soruları bu servisle sorar; dökümü `golden` biçiminde (`<soru>.jsonl`) yazar, raporu `golden.report`
    kurar. Maliyet API'nin gerçek fiyatıdır (S12.1'inki Claude Code'un istemiyle eşdeğer maliyetti)."""
    from datetime import datetime
    from risale_mcp import golden
    questions = [q for q in golden.load_questions() if q["id"] in ids] if ids else \
        [q for q in golden.load_questions() if not q.get("profile")]
    out = golden.RUNS_DIR / f"{datetime.now():%Y%m%d-%H%M%S}-sohbet-{chat.settings.model}-{chat.settings.effort}"
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
                                 "checks": done and done["checks"], "model_text": tally.model_text,
                                 "failure": failure, "input": tally.input, "cache_write": tally.cache_write,
                                 "cache_read": tally.cache_read}})
        (out / f"{q['id']}.jsonl").write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in lines) + "\n",
                                              encoding="utf-8")
        print(f"  {q['id']}: {time.time() - start:.0f} sn, {tally.tools} araç, {tally.cost:.4f} $"
              + (" model düzeltti" if done and done["corrected"] else "")
              + (f" sunucu {done['checks']['fixed']} düzeltti" if done and done["checks"]["fixed"] else "")
              + (f" {done['problems']} doğrulanamadı" if done and done["problems"] else "")
              + (f" HATA {failure}" if failure else ""),
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
    p = sub.add_parser("olc", help="altın soruları bu servisle sor; varsayılan: Risale'nin 29 sorusu. Model ve "
                                    "düşünme düzeyi SOHBET_MODEL, SOHBET_EFFORT")
    p.add_argument("ids", nargs="*")
    p.add_argument("--hizli", action="store_true", help=f"hızlı set (S12.13): {' '.join(QUICK)}")
    p = sub.add_parser("dene", help="hata ayıklama turu (S13.11): soru dosyasındaki konuşmaları yerelde sorar, "
                                     "araç çağrılarıyla döker (sohbet_dene.py)")
    p.add_argument("file", type=Path)
    p.add_argument("names", nargs="*", help="yalnız bu konuşmalar")
    p.add_argument("--paralel", type=int, default=4)
    p = sub.add_parser("usage")
    p.add_argument("--days", type=float, default=7)
    p = sub.add_parser("geri-bildirim", help="geri bildirimleri oku (S12.12)")
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
        app = build(chat, store, sohbet_hesap.mailer_from_env(config, args.dev), config, Limits.from_env())
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
                    print(f"  denetim: {data['checks']}")
                    print("\n" + data["markdown"] + "\n\nKaynaklar")
                    for s in data["sources"]:
                        print(f"[{s['n']}] {s.get('cite_as') or s['id']}" + (f"  ⚠ {s['problem']}" if s.get("problem") else ""))
                        for e in s.get("embedded", ()):
                            print(f"  - {e['line']}")
            print(f"\n{tally.rounds} tur, {tally.tools} araç, girdi {tally.input} (önbellek yazma {tally.cache_write}, "
                  f"okuma {tally.cache_read}), çıktı {tally.output}, ≈{tally.cost:.4f} $, {time.time() - start:.1f} sn")
        asyncio.run(run())
    elif args.command == "dene":
        from risale_mcp import sohbet_dene
        asyncio.run(sohbet_dene.run(Chat(_library(), _client(), config, settings), args.file, args.names,
                                    args.paralel))
    elif args.command == "olc":
        asyncio.run(measure(Chat(_library(), _client(), config, settings), QUICK if args.hizli else args.ids))
    elif args.command == "geri-bildirim":
        from datetime import datetime
        store = Store()
        for r in store._run("SELECT * FROM feedback WHERE ts >= ? ORDER BY ts", (time.time() - args.days * 86400,)):
            print(f"\n{datetime.fromtimestamp(r['ts']):%Y-%m-%d %H:%M}  {'👍' if r['vote'] > 0 else '👎'}  "
                  f"{r['email'] or '(silinmiş hesap)'}  {r['model'] or ''}")
            if r["note"]:
                print(f"  not: {r['note']}")
            if r["question"]:
                print(f"  soru: {r['question']}\n  cevap:\n" + "\n".join("    " + line for line in r["answer"].splitlines()))
    elif args.command == "usage":
        store = Store()
        since = time.time() - args.days * 86400
        rows = store._run("SELECT outcome, COUNT(*) n, SUM(cost) c, AVG(cost) a, AVG(tools) t, AVG(seconds) s, "
                          "SUM(problems > 0) bad, SUM(corrected) fix, SUM(fixed) srv, SUM(dropped) drop_, "
                          "SUM(leaks) leak, SUM(paragraphs) par, SUM(unmarked) unm "
                          "FROM usage WHERE ts >= ? GROUP BY outcome", (since,))
        users = store._run("SELECT COUNT(DISTINCT email) FROM usage WHERE ts >= ?", (since,))[0][0]
        votes = store._run("SELECT SUM(vote = 1), SUM(vote = -1) FROM feedback WHERE ts >= ?", (since,))[0]
        today, month = spent(store)
        limits = Limits.from_env()
        print(f"bugün {today:.3f} $ / {limits.daily:g} $, bu ay {month:.3f} $ / {limits.monthly:g} $")
        print(f"son {args.days:g} gün, {users} kullanıcı; geri bildirim 👍 {votes[0] or 0}, 👎 {votes[1] or 0}")
        for r in rows:
            print(f"{r['outcome']:10} {r['n']:5} soru  toplam {r['c'] or 0:.3f} $  soru başı {r['a'] or 0:.4f} $  "
                  f"araç {r['t'] or 0:.1f}  {r['s'] or 0:.1f} sn  doğrulanamayanlı cevap {r['bad'] or 0}  "
                  f"sunucunun düzelttiği işaret {r['srv'] or 0}, sildiği {r['drop_'] or 0}, düz kimlik {r['leak'] or 0}  "
                  f"işaretsiz paragraf {r['unm'] or 0}/{r['par'] or 0}  model turu {r['fix'] or 0}")


if __name__ == "__main__":
    main()
