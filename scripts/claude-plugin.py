#!/usr/bin/env python3
"""Claude eklentisi (plugin, S4.7): kaynaklardan herkese açık deponun içeriğini üretir.

Kaynaklar `packaging/claude-plugin/`'dedir; ana skill (`risale-library`) proje talimatının İngilizcesinden
(`site/en/instructions.md`) üretilir, böylece talimat değişince eklenti geride kalmaz (tek kaynak). Simge
`src/risale_mcp/static/icon.png`.

    python3 scripts/claude-plugin.py build [--out DİZİN]   # deponun çalışma kopyasına yazar (.git'e dokunmaz)
    python3 scripts/claude-plugin.py check [--out DİZİN]   # çalışma kopyası kaynaklarla aynı mı (çıkış kodu 1: değil)
    python3 scripts/claude-plugin.py zip                   # claude.ai'ye elle yüklemek için data/interim/claude-plugin/*.zip
    python3 scripts/claude-plugin.py dene [P1 P2 …]        # Claude Code'da soru seti: hangi skill yüklendi, cite, Kaynaklar

Deneme `tests/golden/claude_plugin_prompts.json`'daki soruları `claude -p` ile, boş geçici klasörde, yalnız bu eklentiyle
(claude.ai bağdaştırıcıları kapalı, yerleşik araç yok) sorar; rapor `data/interim/claude-plugin/dene-<zaman>.md`.
Claude Code'un skill seçimi claude.ai'ninkine benzer ama aynı değildir: asıl sınama claude.ai'de elle yapılır.

Varsayılan çıktı, ana deponun yanındaki `risale-library-plugin` deposudur.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "packaging" / "claude-plugin"
DEFAULT_OUT = ROOT.parent / "risale-library-plugin"
ZIP_DIR = ROOT / "data" / "interim" / "claude-plugin"
INSTRUCTIONS = ROOT / "site" / "en" / "instructions.md"
ICON = ROOT / "src" / "risale_mcp" / "static" / "icon.png"

# Proje talimatı "bu projede" ve "eklediyseniz" diye yazılmış; eklentide dört bağdaştırıcı hep birliktedir.
# Her değişiklik tam olarak bir kez geçmeli: talimat değişirse betik durur, bu liste elle güncellenir.
REPLACEMENTS = [
    ('In this project, answer every question about the Risale-i Nur with the tools of the "Risale-i Nur" connector.',
     "Answer every question about the Risale-i Nur with the tools of the Risale-i Nur Library connector."),
    ("Hadith and Tafsir connectors (if you added them):",
     "Hadith, Tafsir and Classical connectors:"),
    ('Use the "Hadis" connector for hadith collections and the "Tefsir" connector for classical tafsir works.',
     "Use the Hadith Library for hadith collections, the Tafsir Library for classical tafsir works and the Classical "
     "Islamic Library for classical works on rhetoric, language and terms."),
]
SECTION_LINES = ["Workflow:", "Citations and quotations:", "Text and interpretation:",
                 "Hadith, Tafsir and Classical connectors:"]


def instructions_markdown() -> str:
    text = INSTRUCTIONS.read_text(encoding="utf-8").strip()
    for old, new in REPLACEMENTS:
        if text.count(old) != 1:
            sys.exit(f"site/en/instructions.md değişmiş, şu ifade bulunamadı ya da birden çok: {old!r}")
        text = text.replace(old, new)
    lines = []
    for line in text.splitlines():
        lines.append(f"### {line[:-1]}" if line in SECTION_LINES else line)
    missing = [s for s in SECTION_LINES if f"### {s[:-1]}" not in lines]
    if missing:
        sys.exit(f"site/en/instructions.md'de bölüm başlığı yok: {missing}")
    return "\n".join(lines)


def files() -> dict[str, bytes]:
    """Yayımlanacak dosyalar: depodaki yol -> içerik."""
    out: dict[str, bytes] = {
        ".claude-plugin/plugin.json": (SRC / "plugin.json").read_bytes(),
        ".claude-plugin/marketplace.json": (SRC / "marketplace.json").read_bytes(),
        ".mcp.json": (SRC / "mcp.json").read_bytes(),
        "README.md": (SRC / "README.md").read_bytes(),
        "LICENSE": (SRC / "LICENSE").read_bytes(),
        "assets/icon.png": ICON.read_bytes(),
    }
    for skill in sorted((SRC / "skills").iterdir()):
        if (skill / "SKILL.md.in").exists():
            body = (skill / "SKILL.md.in").read_text(encoding="utf-8")
            body = body.replace("{{INSTRUCTIONS}}", instructions_markdown())
            out[f"skills/{skill.name}/SKILL.md"] = body.encode("utf-8")
        else:
            out[f"skills/{skill.name}/SKILL.md"] = (skill / "SKILL.md").read_bytes()
    validate(out)
    return out


def validate(out: dict[str, bytes]) -> None:
    """Dizin ölçütlerinin bizim elimizdeki kısmı (claude plugin validate ayrıca çalıştırılır)."""
    errors = []
    for name in (".claude-plugin/plugin.json", ".claude-plugin/marketplace.json", ".mcp.json"):
        json.loads(out[name])
    plugin = json.loads(out[".claude-plugin/plugin.json"])
    if json.loads(out[".claude-plugin/marketplace.json"])["plugins"][0]["name"] != plugin["name"]:
        errors.append("marketplace.json eklentinin adını taşımıyor")
    for path, data in out.items():
        if not path.endswith(".png") and len(data) > 256 * 1024:
            errors.append(f"{path} 256 KiB'tan büyük")
        if not path.startswith("skills/"):
            continue
        text = data.decode("utf-8")
        m = re.match(r"---\n(.*?)\n---\n", text, re.S)
        if not m:
            errors.append(f"{path}: üst bilgi yok")
            continue
        meta = dict(line.split(": ", 1) for line in m.group(1).splitlines())
        # Dizinin denetçisi tırnaksız değerde ": " görünce YAML okuyucusunun durduğunu söylüyor: description
        # her zaman çift tırnaklı (JSON dizesi YAML'da da geçerli çift tırnaklı değerdir)
        if not meta.get("description", "").startswith('"'):
            errors.append(f"{path}: description çift tırnak içinde değil")
        else:
            try:
                meta["description"] = json.loads(meta["description"])
            except json.JSONDecodeError as e:
                errors.append(f"{path}: description tırnağı bozuk ({e})")
        # claude.ai'ye yüklenen skill yalnız bu anahtarları kabul eder
        extra = set(meta) - {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
        if extra:
            errors.append(f"{path}: claude.ai'nin kabul etmediği anahtarlar {sorted(extra)}")
        if meta.get("name") != path.split("/")[1]:
            errors.append(f"{path}: name klasör adıyla aynı değil")
        if not re.fullmatch(r"[a-z0-9-]{1,64}", meta.get("name", "")):
            errors.append(f"{path}: name kurala uymuyor")
        if len(meta.get("description", "")) > 1024:
            errors.append(f"{path}: description 1024 karakteri aşıyor ({len(meta['description'])})")
        if "{{" in text:
            errors.append(f"{path}: doldurulmamış yer tutucu")
    words = len(re.sub(r"```.*?```", "", out["README.md"].decode("utf-8"), flags=re.S).split())
    if words < 40:
        errors.append("README 40 kelimeden kısa")
    if errors:
        sys.exit("\n".join(errors))


def build(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    wanted = files()
    for path in tracked(out_dir):          # kaynakta artık olmayan dosyaları sil (.git hariç)
        if path not in wanted:
            (out_dir / path).unlink()
    for path, data in wanted.items():
        target = out_dir / path
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists() or target.read_bytes() != data:
            target.write_bytes(data)
    for d in sorted((p for p in out_dir.rglob("*") if p.is_dir() and ".git" not in p.parts), reverse=True):
        if not any(d.iterdir()):
            d.rmdir()
    print(f"{len(wanted)} dosya -> {out_dir}")


def tracked(out_dir: Path) -> list[str]:
    return [str(p.relative_to(out_dir)) for p in out_dir.rglob("*")
            if p.is_file() and ".git" not in p.relative_to(out_dir).parts]


def check(out_dir: Path) -> int:
    wanted = files()
    have = set(tracked(out_dir)) if out_dir.exists() else set()
    diff = sorted(set(wanted) ^ have) + sorted(p for p in set(wanted) & have
                                               if (out_dir / p).read_bytes() != wanted[p])
    for p in diff:
        print(f"farklı: {p}")
    print("aynı" if not diff else f"{len(diff)} dosya farklı: python3 scripts/claude-plugin.py build")
    return 1 if diff else 0


def make_zip() -> Path:
    ZIP_DIR.mkdir(parents=True, exist_ok=True)
    name = json.loads((SRC / "plugin.json").read_text())["name"]
    version = json.loads((SRC / "plugin.json").read_text())["version"]
    target = ZIP_DIR / f"{name}-{version}.zip"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        for path, data in sorted(files().items()):
            z.writestr(f"{name}/{path}", data)
    print(target)
    return target


PROMPTS = ROOT / "tests" / "golden" / "claude_plugin_prompts.json"
SERVERS = ("risale", "hadith", "tafsir", "classical")


def run_prompt(item: dict, plugin_dir: Path) -> dict:
    """Bir soruyu eklentiyle sorar; çağrılan skill'ler, araçlar ve cevap."""
    name = json.loads((plugin_dir / ".claude-plugin" / "plugin.json").read_text())["name"]
    allowed = ["Skill"] + [f"mcp__plugin_{name}_{s}" for s in SERVERS]
    env = dict(os.environ, ENABLE_CLAUDEAI_MCP_SERVERS="false")
    with tempfile.TemporaryDirectory(prefix="claude-plugin-dene-") as cwd:
        command = ["claude", "-p", item["prompt"], "--output-format", "stream-json", "--verbose",
                   "--plugin-dir", str(plugin_dir), "--tools", "Skill", "--setting-sources", "",
                   "--allowedTools", *allowed, "--no-session-persistence", "--max-turns", "40"]
        start = time.time()
        proc = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, timeout=1200)
    skills, tools, answer = [], [], ""
    for line in proc.stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "assistant":
            for block in event["message"].get("content", []):
                if block.get("type") == "tool_use":
                    if block["name"] == "Skill":
                        skills.append(block["input"].get("skill", "?").split(":")[-1])
                    else:
                        tools.append(block["name"].replace(f"mcp__plugin_{name}_", ""))
        elif event.get("type") == "result":
            answer = event.get("result") or ""
    return {**item, "skills": skills, "tools": tools, "answer": answer, "seconds": round(time.time() - start),
            "returncode": proc.returncode, "stderr": proc.stderr[-500:]}


def trial(ids: list[str], plugin_dir: Path) -> Path:
    items = json.loads(PROMPTS.read_text(encoding="utf-8"))
    if ids:
        items = [i for i in items if i["id"] in ids]
    with ThreadPoolExecutor(3) as pool:
        results = list(pool.map(lambda i: run_prompt(i, plugin_dir), items))
    lines = ["# Claude eklentisi denemesi", "", f"Eklenti: `{plugin_dir}`", "",
             "| Soru | Beklenen | Yüklenen skill | cite | Kaynaklar | Araç | sn |", "|---|---|---|---|---|---:|---:|"]
    for r in results:
        cites = sum(1 for t in r["tools"] if t.endswith("__cite"))
        has_list = bool(re.search(r"^\s*#*\s*\**(Kaynaklar|Sources)\**:?\s*$", r["answer"], re.M | re.I))
        ok = "✓" if set(r["expect"]) <= set(r["skills"]) and (r["expect"] or not r["skills"]) else \
            ("○" if r.get("optional") else "✗")
        lines.append(f"| {r['id']} | {', '.join(r['expect']) or '—'} | {ok} {', '.join(r['skills']) or '—'} | {cites} | "
                     f"{'✓' if has_list else '—'} | {len(r['tools'])} | {r['seconds']} |")
    for r in results:
        lines += ["", f"## {r['id']}: {r['prompt']}", ""]
        if r.get("note"):
            lines += [f"_{r['note']}_", ""]
        lines += [f"Skill: {', '.join(r['skills']) or '—'}  ", f"Araçlar: {', '.join(r['tools']) or '—'}", ""]
        if r["returncode"]:
            lines += [f"Çıkış kodu {r['returncode']}: `{r['stderr']}`", ""]
        lines += ["<details><summary>Cevap</summary>", "", r["answer"], "", "</details>"]
    ZIP_DIR.mkdir(parents=True, exist_ok=True)
    report = ZIP_DIR / f"dene-{time.strftime('%Y%m%d-%H%M%S')}.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (report.with_suffix(".json")).write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n".join(lines[:len(results) + 6]))
    print(report)
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["build", "check", "zip", "dene"])
    ap.add_argument("ids", nargs="*", help="dene: soru kimlikleri (boşsa hepsi)")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    if args.command == "build":
        build(args.out)
    elif args.command == "check":
        return check(args.out)
    elif args.command == "zip":
        make_zip()
    else:
        trial(args.ids, args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
