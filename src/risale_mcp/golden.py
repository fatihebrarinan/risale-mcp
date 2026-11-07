"""Aşama 7: altın sorularla uçtan uca deneme. MCP istemcisi olarak Claude Code kullanılır.

Kullanım:
    uv run python -m risale_mcp.golden run A1 B7 D14         # seçilen sorular
    uv run python -m risale_mcp.golden run --all
    uv run python -m risale_mcp.golden report [klasör]       # son (ya da verilen) çalıştırmanın raporu
    uv run python -m risale_mcp.golden sandbox ~/risale-deneme   # elle sohbet için klasör

Her soru `claude -p` ile ayrı ve boş bir oturumda sorulur: proje klasörünün dışında, geçici bir
klasörde (bulunduğu yerde `CLAUDE.md` yoktur), yerleşik araçlar kapalı (`--tools ""`) ve yalnızca bu
sunucu açıkken (`--strict-mcp-config`). Model cevabı ancak MCP araçlarıyla bulabilir; diskteki
veriyi okuyamaz, web'de arayamaz. Model varsayılan modeldir.

Döküm (`stream-json`) `data/interim/golden/<zaman>/<soru>.jsonl` dosyasına yazılır; rapor aynı
klasördeki `report.md`'dir. Otomatik kontroller:
- Atıflar: cevaptaki "Yol › Yol › “ilk kelimeler…”" atıfları `citations.py` ile veritabanında aranır
  (`citations.py`; kaynakçalı cevapta "[n]" işaretli alıntı blokları kaynakçadaki atfa bağlanır). Bölümü ya da cümlesi bulunamayan atıf uydurma
  olabilir; kısaltılmış yolla yazılan atıf geçerlidir ama ayrıca sayılır.
- Beklenen bölüm: model beklenen bölümü (alt bölümleriyle) okudu mu, cevapta adı geçiyor mu.
- Araç kullanımı: hangi araçlar, kaç kez, hatalı çağrılar.
Metin–yorum ayrımı ve özetin doğruluğu elle değerlendirilir (rapordaki "Değerlendirme" satırı).
"""

import argparse
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from risale_mcp.citations import Citation, CitationChecker
from risale_mcp.library import Library
from risale_mcp.normalize import search_words
from risale_mcp.paths import INTERIM_DIR, ROOT

QUESTIONS = ROOT / "tests" / "golden" / "questions.json"
RUNS_DIR = INTERIM_DIR / "golden"
SERVER = "risale"
TIMEOUT = 15 * 60                 # bir soru için saniye
# Elle deneme klasöründe kapatılan yerleşik araçlar: model yalnızca MCP'yi kullanır.
BUILTIN_TOOLS = ("Bash", "Read", "Edit", "Write", "Glob", "Grep", "NotebookEdit", "WebFetch", "WebSearch", "Agent")
# İç içe çalıştırmada üst Claude Code oturumunun ortam değişkenleri yeni oturuma geçmesin.
PARENT_ENV = ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_JOB_DIR")


def load_questions(path: Path = QUESTIONS) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["questions"]


def server_config(profile: str | None = None) -> dict:
    """Sorunun sunucusu: varsayılan yerel profil; `profile` verilmişse (tefsir, hadis) o sunucu, kendi adıyla."""
    uv = shutil.which("uv") or "uv"
    args = ["--directory", str(ROOT), "run", "risale-mcp"] + (["--profile", profile] if profile else [])
    return {"mcpServers": {profile or SERVER: {"type": "stdio", "command": uv, "args": args}}}


def library_for(profile: str | None) -> Library:
    """Raporun denetim kütüphanesi: sorunun sunucusunun veritabanı."""
    if not profile:
        return Library()
    from risale_mcp.profiles import PROFILES
    if profile == "hadis":
        from risale_mcp.hadis_library import HadisLibrary
        return HadisLibrary(PROFILES[profile].db)
    return Library(PROFILES[profile].db)


# ---------------------------------------------------------------- çalıştırma

def run_question(question: dict, out_dir: Path, workdir: Path, config: Path, servers: list[str] | None = None) -> Path:
    """Soruyu temiz bir Claude Code oturumunda sorar; dökümü `<soru>.jsonl`'e yazar. `servers` verilirse (M6) üç
    bağdaştırıcı birlikte açıktır, sorunun kendi sunucusu değil."""
    allowed = ",".join(f"mcp__{n}" for n in servers) if servers else f"mcp__{question.get('profile') or SERVER}"
    command = ["claude", "-p", question["question"], "--output-format", "stream-json", "--verbose",
               "--mcp-config", str(config), "--strict-mcp-config", "--tools", "",
               "--allowedTools", allowed, "--no-session-persistence"]
    env = {k: v for k, v in os.environ.items() if k not in PARENT_ENV}
    out = out_dir / f"{question['id']}.jsonl"
    started = time.monotonic()
    with out.open("w", encoding="utf-8") as stdout:
        done = subprocess.run(command, cwd=workdir, env=env, stdout=stdout, stderr=subprocess.PIPE,
                              text=True, timeout=TIMEOUT, check=False)
    if done.returncode or done.stderr.strip():
        (out_dir / f"{question['id']}.stderr.txt").write_text(done.stderr, encoding="utf-8")
    print(f"  {question['id']}: {time.monotonic() - started:.0f} sn, çıkış kodu {done.returncode}", flush=True)
    return out


MULTI_RISALE_PROFILE = "genel"          # üç bağdaştırıcı kipinde risale yayındaki hâliyle (müfessirler tefsirde)


def run(ids: list[str], servers: list[str] | None = None) -> Path:
    questions = load_questions()
    chosen = questions if not ids else [q for q in questions if q["id"] in ids]
    unknown = set(ids) - {q["id"] for q in questions}
    if unknown:
        sys.exit(f"Bilinmeyen soru: {sorted(unknown)}")
    out_dir = RUNS_DIR / (datetime.now().strftime("%Y%m%d-%H%M%S") + ("-coklu" if servers else ""))
    out_dir.mkdir(parents=True)
    if servers:
        (out_dir / "servers.json").write_text(json.dumps({"servers": servers, "risale_profile": MULTI_RISALE_PROFILE}),
                                              encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="risale-golden-") as tmp:
        workdir = Path(tmp)
        configs = {}
        if servers:
            multi = workdir / "mcp-coklu.json"
            multi.write_text(json.dumps(servers_config(servers, MULTI_RISALE_PROFILE)), encoding="utf-8")
            configs = {q.get("profile"): multi for q in chosen}
        else:
            for profile in {q.get("profile") for q in chosen}:
                configs[profile] = workdir / f"mcp-{profile or SERVER}.json"
                configs[profile].write_text(json.dumps(server_config(profile)), encoding="utf-8")
        print(f"{len(chosen)} soru; döküm: {out_dir.relative_to(ROOT)}", flush=True)
        for question in chosen:
            run_question(question, out_dir, workdir, configs[question.get("profile")], servers)
    report(out_dir)
    return out_dir


# ---------------------------------------------------------------- döküm

@dataclass
class ToolCall:
    name: str
    arguments: dict
    result: str = ""
    error: bool = False
    server: str = SERVER                                     # çağrının gittiği sunucu (mcp__<sunucu>__araç)


@dataclass
class Transcript:
    answer: str = ""
    calls: list[ToolCall] = field(default_factory=list)
    servers: list[dict] = field(default_factory=list)      # oturum başındaki MCP sunucuları ve durumları
    cost_usd: float | None = None
    turns: int | None = None
    seconds: float | None = None
    output_tokens: int | None = None                         # modelin ürettiği tokenlar (araç girdileri dahil)
    failure: str | None = None


def _text_of(content) -> str:
    if isinstance(content, str):
        return content
    return "".join(c.get("text", "") for c in content or [] if isinstance(c, dict))


def read_transcript(path: Path) -> Transcript:
    """`claude -p --output-format stream-json` dökümü: başlangıç, mesajlar ve sonuç kayıtları."""
    transcript = Transcript()
    by_id: dict[str, ToolCall] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        kind = event.get("type")
        if kind == "system" and event.get("subtype") == "init":
            transcript.servers = event.get("mcp_servers", [])
        elif kind in ("assistant", "user"):
            for block in event.get("message", {}).get("content", []):
                if block.get("type") == "tool_use":
                    server = m.group(1) if (m := re.match(r"^mcp__([^_]+)__", block["name"])) else ""
                    name = re.sub(r"^mcp__[^_]+__", "", block["name"])
                    by_id[block["id"]] = call = ToolCall(name, block.get("input", {}), server=server)
                    transcript.calls.append(call)
                elif block.get("type") == "tool_result" and block.get("tool_use_id") in by_id:
                    call = by_id[block["tool_use_id"]]
                    call.result, call.error = _text_of(block.get("content")), bool(block.get("is_error"))
        elif kind == "result":
            transcript.answer = event.get("result") or ""
            transcript.cost_usd = event.get("total_cost_usd")
            transcript.turns = event.get("num_turns")
            transcript.seconds = (event.get("duration_ms") or 0) / 1000
            transcript.output_tokens = (event.get("usage") or {}).get("output_tokens")
            if event.get("is_error") or event.get("subtype") != "success":
                transcript.failure = event.get("subtype") or "error"
    if not transcript.answer and transcript.failure is None:
        transcript.failure = "sonuç kaydı yok"
    return transcript


# ---------------------------------------------------------------- kontroller

def _key(text: str) -> str:
    return " ".join(search_words(text))


class Checker:
    """Cevabı ve araç çağrılarını veritabanına karşı denetler. Atıflar `citations.py`'de denetlenir."""

    def __init__(self, library: Library) -> None:
        self.library = library
        self.verifier = CitationChecker(library)

    def citations(self, answer: str) -> list[Citation]:
        return self.verifier.check(answer)

    def read_sections(self, calls: list[ToolCall]) -> set[str]:
        """Modelin metnini okuduğu düğümler (read_section, get_passage; aramada çıkan sonuçlar sayılmaz)."""
        read = set()
        for call in calls:
            if call.error:
                continue
            if call.name == "read_section":
                read.add(call.arguments.get("section", ""))
            elif call.name in ("read_chapter", "get_hadith"):
                read.add(call.arguments.get("id") or "")
            elif call.name == "get_passage":
                first = call.arguments.get("id", "").split("..")[0]
                read.add(re.sub(r"/c\d+(/.*)?$", "", first))
            elif call.name == "find_sentence" and call.result:
                read |= {re.sub(r"/c\d+(/.*)?$", "", m["id"]) for m in json.loads(call.result).get("matches", [])}
        return read - {""}

    def title(self, node_id: str) -> str:
        row = self.library.conn.execute("SELECT title FROM nodes WHERE id = ?", (node_id,)).fetchone()
        if row is None:          # hadis sunucusu: bölüm kitap ağacındadır
            try:
                row = self.library.conn.execute("SELECT title FROM lib_nodes WHERE id = ?", (node_id,)).fetchone()
            except sqlite3.OperationalError:
                row = None
        return row[0] if row else node_id


class MultiChecker(Checker):
    """Üç bağdaştırıcı kipi (M6): atıf önce risale (genel) veritabanında, bulunamazsa tefsir veritabanında aranır;
    başlık üçünde. Araç çağrısının kimliği başka sunucunun ise (`cross_server`) sayılır."""

    def __init__(self) -> None:
        from risale_mcp.profiles import GENEL, TEFSIR
        super().__init__(Library(GENEL.db))
        self.tefsir = Checker(Library(TEFSIR.db))
        self.hadis = Checker(library_for("hadis"))
        self.risale_works = {r[0] for r in self.library.conn.execute("SELECT slug FROM works")}
        self.tefsir_works = {r[0] for r in self.tefsir.library.conn.execute("SELECT slug FROM works")}
        self.hadis_books = {r[0] for r in self.hadis.library.conn.execute("SELECT key FROM lib_books")}

    def citations(self, answer: str) -> list[Citation]:
        # iki denetçi aynı metni ayrı ayrı okur; bir atıf hangisinde doğrulanırsa o sayılır, ikisi de tanırsa birinde
        merged: dict[str, Citation] = {}
        for c in self.verifier.check(answer) + self.tefsir.verifier.check(answer):
            if c.written not in merged or (c.verified and not merged[c.written].verified):
                merged[c.written] = c
        return list(merged.values())

    def title(self, node_id: str) -> str:
        for checker in (super(), self.tefsir, self.hadis):
            title = checker.title(node_id)
            if title != node_id:
                return title
        return node_id

    def owner(self, ident: str) -> str | None:
        work = ident.split("/", 1)[0].split("..")[0]
        if work in self.risale_works:
            return "risale"
        if work in self.tefsir_works:
            return "tefsir"
        if work in self.hadis_books:
            return "hadis"
        return None

    def cross_server(self, calls: list[ToolCall]) -> list[ToolCall]:
        """Kimliği başka sunucunun eserine ait çağrılar (ör. risale'nin `get_passage`'ına tefsir kimliği)."""
        out = []
        for call in calls:
            ids = [v for k, v in call.arguments.items() if k in ("id", "section", "work", "book") and isinstance(v, str)]
            ids += [x.get("id") if isinstance(x, dict) else x for x in call.arguments.get("sources", [])
                    + call.arguments.get("ids", []) if x]
            owners = {self.owner(i) for i in ids if i} - {None}
            if owners and call.server not in owners:
                out.append(call)
        return out


_ARABIC_BLOCK = re.compile(r"^>\s*\"?[^\n]*[\u0600-\u06FF]{3,}", re.M)
_STAMP = re.compile(r"yapay zek[âa] (tercüme|çeviri)|kendi (tercüme|çeviri)|AI translation|my (own )?translation", re.I)


def _within(node: str, section: str) -> bool:
    return node == section or node.startswith(section + "/") or section.startswith(node + "/")


def evaluate(question: dict, transcript: Transcript, checker: Checker) -> dict:
    # Hadis sunucusunun atıfları eser yolu değil rivayet kimliğidir; `citations.py` onları denetlemez.
    citations = [] if question.get("profile") == "hadis" else checker.citations(transcript.answer)
    read = checker.read_sections(transcript.calls)
    answer_key = _key(transcript.answer)
    sections = [{"id": s, "read": any(_within(r, s) for r in read), "named": _key(checker.title(s)) in answer_key}
                for s in question["sections"]]
    multi = {}
    if isinstance(checker, MultiChecker):
        cites = [c for c in transcript.calls if c.name == "cite" and not c.error]
        arabic = len(_ARABIC_BLOCK.findall(transcript.answer))
        multi = {"cross": checker.cross_server(transcript.calls),
                 "by_server": {n: sum(c.server == n for c in transcript.calls) for n in ("risale", "hadis", "tefsir")},
                 "cite_servers": sorted({c.server for c in cites}),
                 "arabic_blocks": arabic, "stamped": bool(_STAMP.search(transcript.answer))}
    return {
        **multi,
        "tools": len(transcript.calls),
        "verify_calls": sum(c.name in ("cite", "verify_citations") for c in transcript.calls),
        "tool_errors": sum(c.error for c in transcript.calls),
        "citations": citations,
        "problems": [c for c in citations if not c.verified],
        "sections": sections,
    }


# ---------------------------------------------------------------- rapor

def _mark(ok: bool) -> str:
    return "✓" if ok else "✗"


def _call_line(call: ToolCall) -> str:
    args = json.dumps(call.arguments, ensure_ascii=False)
    return f"- `{call.server + '.' if call.server != SERVER else ''}{call.name}` {args}" + (" — **hata:** " + call.result[:200] if call.error else "")


def report(run_dir: Path) -> Path:
    questions = {q["id"]: q for q in load_questions()}
    checkers: dict[str | None, Checker] = {}
    multi = (run_dir / "servers.json").exists()
    multi_checker = MultiChecker() if multi else None
    multi_rows = []
    rows, sections, totals = [], [], []
    for path in sorted(run_dir.glob("*.jsonl"), key=lambda p: list(questions).index(p.stem)):
        q = questions[path.stem]
        profile = q.get("profile")
        checker = multi_checker or checkers.get(profile) or checkers.setdefault(profile, Checker(library_for(profile)))
        t = read_transcript(path)
        e = evaluate(q, t, checker)
        if multi:
            by = e["by_server"]
            stamp = "—" if not e["arabic_blocks"] else _mark(e["stamped"])
            multi_rows.append(f"| {q['id']} | {q.get('profile') or 'risale'} | {by['risale']} / {by['hadis']} / {by['tefsir']} "
                              f"| {len(e['cross'])} | {', '.join(e['cite_servers']) or '—'} | {e['arabic_blocks']} | {stamp} |")
        ok = sum(c.verified for c in e["citations"])
        short = sum(c.verified and not c.exact for c in e["citations"])
        ranges = sum(c.verified and c.count > 1 for c in e["citations"])
        expected = " ".join(f"{_mark(s['read'])}{_mark(s['named'])}" for s in e["sections"]) or "—"
        totals.append((t.seconds or 0, t.output_tokens or 0, t.cost_usd or 0, e["verify_calls"]))
        rows.append(f"| {q['id']} | {q['category']} | {e['tools']} ({e['tool_errors']} hata) | {e['verify_calls']} "
                    f"| {ok}/{len(e['citations'])}{f' ({short} kısa)' if short else ''}{f' ({ranges} aralık)' if ranges else ''} "
                    f"| {expected} | {t.seconds or 0:.0f} sn | {t.output_tokens or 0:,} | {t.cost_usd or 0:.2f} $ | {t.failure or ''} |")
        lines = [f"## {q['id']} · {q['category']}", "", f"**Soru:** {q['question']}", "",
                 f"**Beklenen:** {q['expected']}", ""]
        if q.get("absent"):
            lines += [f"**Tuzak:** “{q['absent']}” yoktur; model onu bulmuş gibi davranmamalı.", ""]
        if t.servers and any(s.get("status") != "connected" for s in t.servers):
            lines += [f"**Sunucu bağlanamadı:** {t.servers}", ""]
        lines += ["**Cevap:**", "", t.answer.strip() or f"*(cevap yok: {t.failure})*", "",
                  f"**Araç çağrıları ({len(t.calls)}):**", "", *(map(_call_line, t.calls)), ""]
        if multi and e["cross"]:
            lines += ["**Başka sunucunun kimliğiyle çağrı:**", "", *map(_call_line, e["cross"]), ""]
        if e["sections"]:
            lines += ["**Beklenen bölümler** (okundu / cevapta adı geçiyor):", "",
                      *(f"- `{s['id']}` {checker.title(s['id'])}: {_mark(s['read'])} {_mark(s['named'])}"
                        for s in e["sections"]), ""]
        if e["citations"]:
            lines += ["**Atıflar:**", "", *map(_citation_line, e["citations"]), ""]
        lines += ["**Değerlendirme:** ⬜ doğru ⬜ kısmen ⬜ yanlış — not:", "", "---", ""]
        sections.append("\n".join(lines))
    header = ["# Altın sorular", "", f"Çalıştırma: `{run_dir.name}`", "",
              "Beklenen bölüm sütununda her bölüm için iki işaret: okundu mu, cevapta adı geçiyor mu.", "",
              "Üretilen token: modelin yazdığı her şey (araç girdileri, taslaklar ve cevap).", "",
              "| Soru | Tür | Araç | Atıf aracı | Doğrulanan atıf | Beklenen bölüm | Süre | Üretilen token | Maliyet | Sorun |",
              "|---|---|---|---|---|---|---|---|---|---|", *rows]
    if totals:
        n = len(totals)
        header += [f"| **ortalama** | | | {sum(t[3] for t in totals) / n:.1f} | | | {sum(t[0] for t in totals) / n:.0f} sn "
                   f"| {sum(t[1] for t in totals) / n:,.0f} | {sum(t[2] for t in totals) / n:.2f} $ | |"]
    if multi:
        header += ["", "## Üç bağdaştırıcı (M6)", "",
                   "Çağrılar sunucu başına (risale / hadis / tefsir); başka sunucunun kimliğiyle yapılan çağrı; `cite` "
                   "hangi sunucularda çağrıldı (birden çoksa kaynakça numaraları çakışabilir); Arapça alıntı bloğu ve "
                   "\"yapay zekâ tercümesi\" damgası (otomatik, kaba; elle bakılır).", "",
                   "| Soru | Sorunun sunucusu | Çağrılar r / h / t | Başka sunucunun kimliği | cite | Arapça blok | Damga |",
                   "|---|---|---|---|---|---|---|", *multi_rows]
    header += ["", ""]
    out = run_dir / "report.md"
    out.write_text("\n".join(header + sections), encoding="utf-8")
    print(f"rapor: {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}")
    return out


_CITATION_MARK = {"ok": "✓", "mid_sentence": "◑", "section": "◐ (yalnızca bölüm)"}


def _citation_line(c: Citation) -> str:
    """✓ cümle bulundu, ◑ alıntı metinde ama cümle başı değil, ◐ yalnızca bölüm, ✗ bulunamadı ya da yanlış."""
    if c.verified:
        detail = "" if c.exact else f" — kısaltılmış yol; tam atıf: {c.cite_as}"
        if c.status == "mid_sentence":
            detail = " — alıntı metinde var, ama bir cümlenin başı değil" + detail
        return f"- {_CITATION_MARK[c.status]} {c.written}{detail}"
    detail = {
        "quote_not_found": f"bu sözler {c.ref} metninde yok",
        "no_such_sentence": f"{c.ref} içinde {c.number}. cümle yok",
        "unknown_section": f"“{c.missing}” bölümü yok" + (f" ({c.ref} altında)" if c.ref else ""),
        "ambiguous": "yol birden çok bölüme uyuyor: " + "; ".join(c.candidates),
        "range_too_long": f"aralık {c.count} cümle; en çok 8",
        "range_past_section": f"aralık bölümü aşıyor; bölümde {len(c.covered)} cümle kalıyor",
    }.get(c.status) or "yanındaki alıntı bloğu atfın cümlelerinde yok"
    if c.elsewhere:
        detail += "; alıntının geçtiği yer: " + "; ".join(e["cite_as"] for e in c.elsewhere)
    return f"- ✗ {c.written} — {detail}"


# ---------------------------------------------------------------- elle deneme klasörü

def servers_config(names: list[str], risale_profile: str | None = None) -> dict:
    """Birden çok bağdaştırıcı (M6): `risale` (profili `risale_profile`, yoksa yerel), `hadis`, `tefsir`, her biri
    kendi adıyla; kullanıcının claude.ai'de ekleyeceği gibi ayrı sunucular."""
    out = {}
    for name in names:
        profile = risale_profile if name == SERVER else name
        config = server_config(profile)["mcpServers"]
        out[name] = next(iter(config.values()))
    return {"mcpServers": out}


def sandbox(path: Path, names: list[str] | None = None, risale_profile: str | None = None) -> None:
    """Elle sohbet için klasör: seçilen sunucular açık, yerleşik dosya/kabuk/web araçları kapalı."""
    names = names or [SERVER]
    path = path.expanduser().resolve()
    if path == ROOT or ROOT in path.parents:
        sys.exit("Deneme klasörü proje klasörünün dışında olmalı (Claude Code üst klasörlerdeki CLAUDE.md'yi okur).")
    (path / ".claude").mkdir(parents=True, exist_ok=True)
    (path / ".mcp.json").write_text(json.dumps(servers_config(names, risale_profile), indent=2), encoding="utf-8")
    settings = {"enabledMcpjsonServers": names,
                "permissions": {"allow": [f"mcp__{n}" for n in names], "deny": list(BUILTIN_TOOLS)}}
    (path / ".claude" / "settings.json").write_text(json.dumps(settings, indent=2), encoding="utf-8")
    print(f"hazır: {path}\n  cd {path} && claude")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    run_parser = commands.add_parser("run", help="soruları sor ve raporla")
    run_parser.add_argument("ids", nargs="*", help="soru kimlikleri (A1, D14, K2…)")
    run_parser.add_argument("--all", action="store_true", help="bütün sorular")
    run_parser.add_argument("--servers", help="üç bağdaştırıcı kipi (M6): virgülle, ör. risale,hadis,tefsir")
    report_parser = commands.add_parser("report", help="bir çalıştırmanın raporunu yeniden üret")
    report_parser.add_argument("run_dir", nargs="?", type=Path, help="varsayılan: son çalıştırma")
    sandbox_parser = commands.add_parser("sandbox", help="elle deneme klasörü hazırla")
    sandbox_parser.add_argument("path", type=Path)
    sandbox_parser.add_argument("--servers", default=SERVER, help="virgülle: risale,hadis,tefsir")
    sandbox_parser.add_argument("--risale-profile", help="risale sunucusunun profili (genel: yayındaki hâli)")
    args = parser.parse_args()

    if args.command == "run":
        if not (args.all or args.ids):
            sys.exit("Soru kimliği ya da --all verin.")
        run([] if args.all else args.ids, args.servers.split(",") if args.servers else None)
    elif args.command == "report":
        runs = sorted(p for p in RUNS_DIR.iterdir() if p.is_dir()) if RUNS_DIR.exists() else []
        if not (args.run_dir or runs):
            sys.exit("Henüz çalıştırma yok.")
        report((args.run_dir or runs[-1]).resolve())
    else:
        sandbox(args.path, args.servers.split(","), args.risale_profile)


if __name__ == "__main__":
    main()
