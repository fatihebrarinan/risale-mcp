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
- Atıflar: cevaptaki "Yol › Yol › “ilk kelimeler…”" atıfları veritabanında aranır. Bölümü ya da
  cümlesi bulunamayan atıf uydurma olabilir.
- Beklenen bölüm: model beklenen bölümü (alt bölümleriyle) okudu mu, cevapta adı geçiyor mu.
- Araç kullanımı: hangi araçlar, kaç kez, hatalı çağrılar.
Metin–yorum ayrımı ve özetin doğruluğu elle değerlendirilir (rapordaki "Değerlendirme" satırı).
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from risale_mcp.library import Library, LibraryError
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


def server_config() -> dict:
    uv = shutil.which("uv") or "uv"
    return {"mcpServers": {SERVER: {"type": "stdio", "command": uv,
                                    "args": ["--directory", str(ROOT), "run", "risale-mcp"]}}}


# ---------------------------------------------------------------- çalıştırma

def run_question(question: dict, out_dir: Path, workdir: Path, config: Path) -> Path:
    """Soruyu temiz bir Claude Code oturumunda sorar; dökümü `<soru>.jsonl`'e yazar."""
    command = ["claude", "-p", question["question"], "--output-format", "stream-json", "--verbose",
               "--mcp-config", str(config), "--strict-mcp-config", "--tools", "",
               "--allowedTools", f"mcp__{SERVER}", "--no-session-persistence"]
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


def run(ids: list[str]) -> Path:
    questions = load_questions()
    chosen = questions if not ids else [q for q in questions if q["id"] in ids]
    unknown = set(ids) - {q["id"] for q in questions}
    if unknown:
        sys.exit(f"Bilinmeyen soru: {sorted(unknown)}")
    out_dir = RUNS_DIR / datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir.mkdir(parents=True)
    with tempfile.TemporaryDirectory(prefix="risale-golden-") as tmp:
        workdir = Path(tmp)
        config = workdir / "mcp.json"
        config.write_text(json.dumps(server_config()), encoding="utf-8")
        print(f"{len(chosen)} soru; döküm: {out_dir.relative_to(ROOT)}", flush=True)
        for question in chosen:
            run_question(question, out_dir, workdir, config)
    report(out_dir)
    return out_dir


# ---------------------------------------------------------------- döküm

@dataclass
class ToolCall:
    name: str
    arguments: dict
    result: str = ""
    error: bool = False


@dataclass
class Transcript:
    answer: str = ""
    calls: list[ToolCall] = field(default_factory=list)
    servers: list[dict] = field(default_factory=list)      # oturum başındaki MCP sunucuları ve durumları
    cost_usd: float | None = None
    turns: int | None = None
    seconds: float | None = None
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
                    name = block["name"].removeprefix(f"mcp__{SERVER}__")
                    by_id[block["id"]] = call = ToolCall(name, block.get("input", {}))
                    transcript.calls.append(call)
                elif block.get("type") == "tool_result" and block.get("tool_use_id") in by_id:
                    call = by_id[block["tool_use_id"]]
                    call.result, call.error = _text_of(block.get("content")), bool(block.get("is_error"))
        elif kind == "result":
            transcript.answer = event.get("result") or ""
            transcript.cost_usd = event.get("total_cost_usd")
            transcript.turns = event.get("num_turns")
            transcript.seconds = (event.get("duration_ms") or 0) / 1000
            if event.get("is_error") or event.get("subtype") != "success":
                transcript.failure = event.get("subtype") or "error"
    if not transcript.answer and transcript.failure is None:
        transcript.failure = "sonuç kaydı yok"
    return transcript


# ---------------------------------------------------------------- kontroller

# Yolun hemen ardından gelen alıntı: önce düz tırnak ("…" içinde “…” olabilir), sonra kıvrık tırnak.
_QUOTED = (re.compile(r'^"\s*(.+?)\s*(?:…|\.\.\.)?\s*"'), re.compile(r"^[“«]\s*(.+?)\s*(?:…|\.\.\.)?\s*[”»]"))
_SENTENCE_NO = re.compile(r"^(\d+)\.\s*cümle$")
_TRIM = " -–—:;,.()[]"


@dataclass
class Citation:
    text: str
    status: str            # "ok", "inside" (alıntı metinde var ama cümle başı değil), "section", "unresolved"
    node: str | None = None
    detail: str = ""


def _key(text: str) -> str:
    return " ".join(search_words(text))


def _quote(text: str) -> tuple[str | None, str]:
    """Metnin başındaki alıntı ve geri kalanı."""
    text = text.strip(" :–—")
    for pattern in _QUOTED:
        if m := pattern.match(text):
            return m[1], text[m.end():]
    return None, text


class Checker:
    """Cevabı ve araç çağrılarını veritabanına karşı denetler."""

    def __init__(self, library: Library) -> None:
        self.library = library
        self.refs: dict[tuple[str, ...], str] = {}
        self.by_last: dict[str, list[tuple[tuple[str, ...], str]]] = {}    # son başlık -> (yol, düğüm)
        for node_id, ref in library.conn.execute("SELECT id, ref FROM nodes"):
            path = tuple(_key(p) for p in ref.split("›"))
            if path not in self.refs:
                self.refs[path] = node_id
                self.by_last.setdefault(path[-1], []).append((path, node_id))

    def citations(self, answer: str) -> list[Citation]:
        out = []
        for line in answer.splitlines():
            for chain in re.findall(r"[^\n›]*(?:›[^\n›]*)+", line):
                parts = [re.sub(r"[*_`]+", "", p) for p in chain.split("›")]
                parts = [p.strip(_TRIM) for p in parts[:-1]] + [parts[-1].strip()]
                if len(parts) >= 2 and all(parts[:-1]):
                    out.append(self._resolve(parts))
        return out

    def _resolve(self, parts: list[str]) -> Citation:
        """Atıf zinciri: [önündeki metin + eser, bölüm…, başlık ya da alıntı + ardından gelen metin]."""
        incipit, _ = _quote(parts[-1])
        middle = parts[1:-1] if incipit is not None else parts[1:]
        # "… › 32. cümle (› Hâşiye › 2. cümle)": yol ilk cümle numarasına kadardır.
        sentence_no = None
        for i, p in enumerate(middle):
            if m := _SENTENCE_NO.match(p.strip(_TRIM)):
                sentence_no, middle, incipit = int(m[1]), middle[:i], None
                break
        head = parts[0].split()
        tail = middle[-1].split() if middle and incipit is None and sentence_no is None else None
        node, path = self._match(head, middle[:-1] if tail is not None else middle, tail)
        text = " › ".join(path) + (f" › “{incipit}”" if incipit else "") + (f" › {sentence_no}. cümle" if sentence_no else "")
        if node is None:
            return Citation(" › ".join(p.strip(_TRIM) for p in parts)[:160], "unresolved",
                            detail="bölüm yolu veritabanında yok")
        if sentence_no is not None:
            found = self.library.conn.execute("SELECT 1 FROM sentences WHERE node_id = ? AND n = ? AND hasiye = 0",
                                              (node, sentence_no)).fetchone()
            return Citation(text, "ok" if found else "unresolved", node, "" if found else "bu numarada cümle yok")
        if incipit is None:
            return Citation(text, "section", node)
        return self._check_quote(text, node, incipit)

    def _match(self, head: list[str], middle: list[str], tail: list[str] | None) -> tuple[str | None, list[str]]:
        """İlk parçanın sonundan ve (alıntısız atıfta) son parçanın başından en uzun uyan kelime dizileri."""
        tails = [tail[:j] for j in range(len(tail), 0, -1)] if tail else [None]
        for k in range(len(head)):
            for end in tails:
                path = [" ".join(head[k:]).strip(_TRIM), *middle] + ([" ".join(end)] if end else [])
                if node := self._node([_key(p) for p in path]):
                    return node, path
        return None, []

    def _node(self, path: list[str]) -> str | None:
        """Tam yol ya da (eser adı yazılmamışsa) tek bir düğüme uyan yol sonu."""
        path = tuple(path)
        if path in self.refs:
            return self.refs[path]
        tails = [node for ref, node in self.by_last.get(path[-1], ()) if ref[-len(path):] == path]
        return tails[0] if len(tails) == 1 else None

    def _check_quote(self, text: str, node: str, incipit: str) -> Citation:
        try:
            matches = self.library.find_sentence(incipit, scope=node)["matches"]
        except LibraryError:
            matches = []
        if matches:
            return Citation(text, "ok", node, matches[0]["id"])
        # Alıntı bir cümlenin başı değil ama bölümün metninde geçiyor mu (cümle sınırını aşan alıntı)?
        words = _key(incipit)
        paragraphs = self.library.conn.execute(
            "SELECT p.text FROM paragraphs p JOIN nodes n ON n.id = p.node_id JOIN nodes r ON r.id = ?"
            " WHERE n.work = r.work AND n.ord BETWEEN r.ord AND r.last_ord AND p.text IS NOT NULL", (node,))
        if words and any(words in _key(p[0]) for p in paragraphs):
            return Citation(text, "inside", node, "alıntı metinde var, ama bir cümlenin başı değil")
        return Citation(text, "unresolved", node, "bu sözler bölümün metninde yok")

    def read_sections(self, calls: list[ToolCall]) -> set[str]:
        """Modelin metnini okuduğu düğümler (read_section, get_passage; aramada çıkan sonuçlar sayılmaz)."""
        read = set()
        for call in calls:
            if call.error:
                continue
            if call.name == "read_section":
                read.add(call.arguments.get("section", ""))
            elif call.name == "get_passage":
                first = call.arguments.get("id", "").split("..")[0]
                read.add(re.sub(r"/c\d+(/.*)?$", "", first))
            elif call.name == "find_sentence" and call.result:
                read |= {re.sub(r"/c\d+(/.*)?$", "", m["id"]) for m in json.loads(call.result).get("matches", [])}
        return read - {""}

    def title(self, node_id: str) -> str:
        return self.library.conn.execute("SELECT title FROM nodes WHERE id = ?", (node_id,)).fetchone()[0]


def _within(node: str, section: str) -> bool:
    return node == section or node.startswith(section + "/") or section.startswith(node + "/")


def evaluate(question: dict, transcript: Transcript, checker: Checker) -> dict:
    citations = checker.citations(transcript.answer)
    read = checker.read_sections(transcript.calls)
    answer_key = _key(transcript.answer)
    sections = [{"id": s, "read": any(_within(r, s) for r in read), "named": _key(checker.title(s)) in answer_key}
                for s in question["sections"]]
    return {
        "tools": len(transcript.calls),
        "tool_errors": sum(c.error for c in transcript.calls),
        "citations": citations,
        "unresolved": [c for c in citations if c.status == "unresolved"],
        "sections": sections,
    }


# ---------------------------------------------------------------- rapor

def _mark(ok: bool) -> str:
    return "✓" if ok else "✗"


def _call_line(call: ToolCall) -> str:
    args = json.dumps(call.arguments, ensure_ascii=False)
    return f"- `{call.name}` {args}" + (" — **hata:** " + call.result[:200] if call.error else "")


def report(run_dir: Path) -> Path:
    questions = {q["id"]: q for q in load_questions()}
    checker = Checker(Library())
    rows, sections = [], []
    for path in sorted(run_dir.glob("*.jsonl"), key=lambda p: list(questions).index(p.stem)):
        q = questions[path.stem]
        t = read_transcript(path)
        e = evaluate(q, t, checker)
        ok = sum(c.status in ("ok", "section") for c in e["citations"])
        expected = " ".join(f"{_mark(s['read'])}{_mark(s['named'])}" for s in e["sections"]) or "—"
        rows.append(f"| {q['id']} | {q['category']} | {e['tools']} ({e['tool_errors']} hata) | {ok}/{len(e['citations'])} "
                    f"| {expected} | {t.seconds or 0:.0f} sn | {t.failure or ''} |")
        lines = [f"## {q['id']} · {q['category']}", "", f"**Soru:** {q['question']}", "",
                 f"**Beklenen:** {q['expected']}", ""]
        if q.get("absent"):
            lines += [f"**Tuzak:** “{q['absent']}” yoktur; model onu bulmuş gibi davranmamalı.", ""]
        if t.servers and any(s.get("status") != "connected" for s in t.servers):
            lines += [f"**Sunucu bağlanamadı:** {t.servers}", ""]
        lines += ["**Cevap:**", "", t.answer.strip() or f"*(cevap yok: {t.failure})*", "",
                  f"**Araç çağrıları ({len(t.calls)}):**", "", *(map(_call_line, t.calls)), ""]
        if e["sections"]:
            lines += ["**Beklenen bölümler** (okundu / cevapta adı geçiyor):", "",
                      *(f"- `{s['id']}` {checker.title(s['id'])}: {_mark(s['read'])} {_mark(s['named'])}"
                        for s in e["sections"]), ""]
        if e["citations"]:
            lines += ["**Atıflar:**", "", *(f"- {_CITATION_MARK[c.status]} {c.text}" + (f" — {c.detail}" if c.detail else "")
                                           for c in e["citations"]), ""]
        lines += ["**Değerlendirme:** ⬜ doğru ⬜ kısmen ⬜ yanlış — not:", "", "---", ""]
        sections.append("\n".join(lines))
    header = ["# Altın sorular", "", f"Çalıştırma: `{run_dir.name}`", "",
              "Beklenen bölüm sütununda her bölüm için iki işaret: okundu mu, cevapta adı geçiyor mu.", "",
              "| Soru | Tür | Araç | Doğrulanan atıf | Beklenen bölüm | Süre | Sorun |",
              "|---|---|---|---|---|---|---|", *rows, "", ""]
    out = run_dir / "report.md"
    out.write_text("\n".join(header + sections), encoding="utf-8")
    print(f"rapor: {out.relative_to(ROOT)}")
    return out


_CITATION_MARK = {"ok": "✓", "inside": "◑", "section": "◐ (yalnızca bölüm)", "unresolved": "✗"}


# ---------------------------------------------------------------- elle deneme klasörü

def sandbox(path: Path) -> None:
    """Elle sohbet için klasör: bu sunucu açık, yerleşik dosya/kabuk/web araçları kapalı."""
    path = path.expanduser().resolve()
    if path == ROOT or ROOT in path.parents:
        sys.exit("Deneme klasörü proje klasörünün dışında olmalı (Claude Code üst klasörlerdeki CLAUDE.md'yi okur).")
    (path / ".claude").mkdir(parents=True, exist_ok=True)
    (path / ".mcp.json").write_text(json.dumps(server_config(), indent=2), encoding="utf-8")
    settings = {"enabledMcpjsonServers": [SERVER],
                "permissions": {"allow": [f"mcp__{SERVER}"], "deny": list(BUILTIN_TOOLS)}}
    (path / ".claude" / "settings.json").write_text(json.dumps(settings, indent=2), encoding="utf-8")
    print(f"hazır: {path}\n  cd {path} && claude")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    run_parser = commands.add_parser("run", help="soruları sor ve raporla")
    run_parser.add_argument("ids", nargs="*", help="soru kimlikleri (A1, D14, K2…)")
    run_parser.add_argument("--all", action="store_true", help="bütün sorular")
    report_parser = commands.add_parser("report", help="bir çalıştırmanın raporunu yeniden üret")
    report_parser.add_argument("run_dir", nargs="?", type=Path, help="varsayılan: son çalıştırma")
    sandbox_parser = commands.add_parser("sandbox", help="elle deneme klasörü hazırla")
    sandbox_parser.add_argument("path", type=Path)
    args = parser.parse_args()

    if args.command == "run":
        if not (args.all or args.ids):
            sys.exit("Soru kimliği ya da --all verin.")
        run([] if args.all else args.ids)
    elif args.command == "report":
        runs = sorted(p for p in RUNS_DIR.iterdir() if p.is_dir()) if RUNS_DIR.exists() else []
        if not (args.run_dir or runs):
            sys.exit("Henüz çalıştırma yok.")
        report((args.run_dir or runs[-1]).resolve())
    else:
        sandbox(args.path)


if __name__ == "__main__":
    main()
