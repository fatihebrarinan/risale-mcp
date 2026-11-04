"""Araç çıktısı karşılaştırması (H0, `docs/tefsir-altyapi-plani.md`).

    uv run python -m risale_mcp.tool_snapshot record <ad> [--profile genel] [--no-semantic]
    uv run python -m risale_mcp.tool_snapshot compare <önceki> <sonraki> [--expect araç…]
    uv run python -m risale_mcp.tool_snapshot list

Sunucunun kullanıcıları var: altyapı değişiklikleri onların gördüğünü kaydırmamalı. Bu modül sabit bir çağrı setini
(`tests/golden/tool_calls.json`, git'te) sunucunun kendisine, MCP istemcisiyle ve süreç içinde sorar; modelin
gördüğü her şeyi kaydeder: sunucu talimatı, araçların adı, açıklaması ve şeması, kaynaklar, hazır komutlar ve her
çağrının metni (hata ise `error: true`). Kayıt `data/interim/tool_snapshot/<ad>/` altına yazılır (git'e eklenmez):
`calls.json` (hepsi) ve `meta.json` (profil, veritabanının kuruluş zamanı, kod commit'i).

`compare` iki kaydı karşılaştırır, `data/interim/tool_snapshot/<sonraki>/diff-<önceki>.md` raporunu yazar. JSON
çıktılarda fark alan yoluyla verilir (`results[0].ref`). `--expect` ile adı verilen araçlardaki farklar beklenen
sayılır; başka fark varsa çıkış kodu 1'dir: deploy edilmez.

Anlamsal arama sorgu vektörünü Voyage'dan alır (ücretli, ağ) ve aynı soruya her seferinde biraz farklı vektör
döner: kayıt sorgu vektörlerini `query_vectors.npz`'de saklar, sonraki kayıtlar onları kullanır (yalnız sunucunun
değişikliği görünsün). `--no-semantic` o çağrıları atlar; atlanan çağrılar karşılaştırmada fark sayılmaz.
"""

import argparse
import asyncio
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from risale_mcp.paths import INTERIM_DIR, ROOT

CALLS_PATH = ROOT / "tests" / "golden" / "tool_calls.json"
SNAPSHOT_DIR = INTERIM_DIR / "tool_snapshot"
MAX_LINES = 400                  # raporda en çok bu kadar fark satırı


def load_calls(path: Path = CALLS_PATH) -> list[dict]:
    calls = json.loads(path.read_text(encoding="utf-8"))["calls"]
    names = [c["name"] for c in calls]
    if len(names) != len(set(names)):
        raise SystemExit(f"{path}: aynı adlı çağrılar var")
    return calls


def _text(content: list) -> str:
    return "\n".join(getattr(part, "text", "") or "" for part in content)


async def _record(library, calls: list[dict], semantic: bool) -> dict:
    from mcp import Client

    from risale_mcp.server import create_server

    server = create_server(library)
    out: dict = {"calls": {}}
    async with Client(server) as client:
        out["instructions"] = server.instructions
        tools = await client.list_tools()
        out["tools"] = {t.name: {"title": t.title, "description": t.description, "input": t.input_schema, "annotations": t.annotations.model_dump(exclude_none=True) if t.annotations else None}
                        for t in tools.tools}
        resources = await client.list_resources()
        templates = await client.list_resource_templates()
        out["resources"] = sorted(str(r.uri) for r in resources.resources) + \
            sorted(t.uri_template for t in templates.resource_templates)
        prompts = await client.list_prompts()
        out["prompts"] = {p.name: {"description": p.description, "arguments": [a.name for a in p.arguments or []]}
                          for p in prompts.prompts}
        for call in calls:
            kind = call.get("kind", "tool")
            if call.get("semantic") and not semantic:
                out["calls"][call["name"]] = {"skipped": True}
                continue
            try:
                if kind == "tool":
                    result = await client.call_tool(call["tool"], call.get("args", {}))
                    out["calls"][call["name"]] = {"error": bool(result.is_error), "text": _text(result.content)}
                elif kind == "resource":
                    result = await client.read_resource(call["uri"])
                    out["calls"][call["name"]] = {"text": "\n".join(c.text for c in result.contents)}
                elif kind == "prompt":
                    result = await client.get_prompt(call["prompt"], call.get("args", {}))
                    out["calls"][call["name"]] = {"text": "\n".join(_text([m.content]) for m in result.messages)}
                else:
                    raise SystemExit(f"bilinmeyen çağrı türü: {kind}")
            except Exception as error:                   # protokol hatası da kullanıcının göreceği bir sonuçtur
                out["calls"][call["name"]] = {"error": True, "exception": type(error).__name__, "text": str(error)}
    return out


def _fixed_query_vectors(path: Path | None = None) -> None:
    """Sorgu vektörlerini diskten verir: Voyage aynı soruya her seferinde küçük farklarla vektör döndürüyor
    (benzerlik üçüncü hanede oynuyor), karşılaştırma ise yalnız sunucunun değişikliğini görmeli. İlk kayıtta
    sağlayıcıdan alınan vektör saklanır, sonrakiler onu kullanır (ücret de bir kez ödenir)."""
    import numpy as np

    from risale_mcp import semantic

    path = path or SNAPSHOT_DIR / "query_vectors.npz"
    stored = dict(np.load(path)) if path.exists() else {}
    original = semantic._query_vector

    def cached(model_name: str, query: str):
        key = f"{model_name}\t{query}"
        if key not in stored:
            stored[key] = original(model_name, query)
            path.parent.mkdir(parents=True, exist_ok=True)
            np.savez(path, **stored)
        return stored[key]

    semantic._query_vector = cached


def record(name: str, profile_name: str, semantic: bool = True, calls_path: Path = CALLS_PATH,
           db: Path | None = None) -> Path:
    from risale_mcp.env import load_env
    from risale_mcp.library import Library
    from risale_mcp.profiles import PROFILES

    load_env()
    profile = PROFILES[profile_name]
    library = Library(db or profile.db, profile.vectors)
    calls = load_calls(calls_path)
    if semantic:
        _fixed_query_vectors()
    data = asyncio.run(_record(library, calls, semantic))
    built = library.conn.execute("SELECT value FROM meta WHERE key = 'built_at'").fetchone()
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    dirty = bool(subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True).stdout.strip())
    meta = {"name": name, "profile": profile.name, "db": str(db or profile.db), "db_built_at": built[0] if built else None,
            "commit": commit + ("-dirty" if dirty else ""), "semantic": semantic,
            "recorded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "calls": len(calls)}
    out = SNAPSHOT_DIR / name
    out.mkdir(parents=True, exist_ok=True)
    (out / "calls.json").write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (out / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    errors = sum(1 for c in data["calls"].values() if c.get("exception"))
    print(f"{len(calls)} çağrı kaydedildi: {out.relative_to(ROOT)}" + (f" ({errors} protokol hatası)" if errors else ""))
    return out


def _rel(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def _parse(text: str):
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return text


def _short(value) -> str:
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    return text if len(text) <= 160 else text[:157] + "…"


def json_diff(old, new, path: str = "") -> list[str]:
    """İki değerin farkları, alan yoluyla. Liste öğeleri sırasıyla karşılaştırılır."""
    if type(old) is not type(new):
        return [f"{path or '.'}: {_short(old)} → {_short(new)}"]
    if isinstance(old, dict):
        out = []
        for key in old.keys() | new.keys():
            sub = f"{path}.{key}" if path else str(key)
            if key not in new:
                out.append(f"{sub}: silindi ({_short(old[key])})")
            elif key not in old:
                out.append(f"{sub}: eklendi ({_short(new[key])})")
            else:
                out += json_diff(old[key], new[key], sub)
        return sorted(out)
    if isinstance(old, list):
        out = []
        for i, (a, b) in enumerate(zip(old, new)):
            out += json_diff(a, b, f"{path}[{i}]")
        if len(old) != len(new):
            out.append(f"{path}: {len(old)} öğe → {len(new)} öğe")
        return out
    return [] if old == new else [f"{path or '.'}: {_short(old)} → {_short(new)}"]


def compare(before: str, after: str, expect: tuple[str, ...] = ()) -> int:
    old = json.loads((SNAPSHOT_DIR / before / "calls.json").read_text(encoding="utf-8"))
    new = json.loads((SNAPSHOT_DIR / after / "calls.json").read_text(encoding="utf-8"))
    tool_of = {c["name"]: c.get("tool") or c.get("prompt") or c.get("uri") for c in load_calls()}
    sections: list[tuple[str, list[str], bool]] = []     # (başlık, farklar, beklenen mi)
    for key in ("instructions", "tools", "resources", "prompts"):
        diff = json_diff(old.get(key), new.get(key))
        if diff:
            sections.append((key, diff, False))
    for name in sorted(old["calls"].keys() | new["calls"].keys()):
        a, b = old["calls"].get(name), new["calls"].get(name)
        if a is None or b is None:
            sections.append((name, ["çağrı yalnız " + ("öncekinde" if b is None else "sonrakinde")], False))
            continue
        if a.get("skipped") or b.get("skipped"):
            continue
        diff = json_diff({"error": a.get("error", False), "text": _parse(a["text"])},
                         {"error": b.get("error", False), "text": _parse(b["text"])})
        if diff:
            sections.append((name, diff, tool_of.get(name) in expect))
    unexpected = [s for s in sections if not s[2]]
    lines = [f"# Araç çıktısı karşılaştırması: {before} → {after}", "",
             f"Çağrı: {len(new['calls'])}; farklı: {len(sections)}; beklenmeyen: {len(unexpected)}"
             + (f" (beklenen araçlar: {', '.join(expect)})" if expect else ""), ""]
    shown = 0
    for title, diff, expected in sections:
        lines.append(f"## {title}" + (" (beklenen)" if expected else ""))
        lines.append("")
        for line in diff:
            if shown >= MAX_LINES:
                break
            lines.append(f"- `{line}`")
            shown += 1
        lines.append("")
    if shown >= MAX_LINES:
        lines.append(f"(rapor {MAX_LINES} satırda kesildi)")
    report = SNAPSHOT_DIR / after / f"diff-{before}.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(sections)} çağrıda fark, {len(unexpected)} beklenmeyen. Rapor: {_rel(report)}")
    for title, diff, _ in unexpected[:10]:
        print(f"  {title}: {diff[0]}" + (f" (+{len(diff) - 1})" if len(diff) > 1 else ""))
    return 1 if unexpected else 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    rec = sub.add_parser("record", help="çağrı setini çalıştır ve kaydet")
    rec.add_argument("name")
    rec.add_argument("--profile", default="genel")
    rec.add_argument("--db", type=Path, help="profilin veritabanı yerine bu dosya")
    rec.add_argument("--no-semantic", action="store_true", help="anlamsal arama çağrılarını atla (Voyage'a gitmez)")
    cmp = sub.add_parser("compare", help="iki kaydı karşılaştır")
    cmp.add_argument("before")
    cmp.add_argument("after")
    cmp.add_argument("--expect", nargs="*", default=(), help="farkı beklenen araçlar")
    sub.add_parser("list", help="kayıtlar")
    args = parser.parse_args()
    if args.command == "record":
        record(args.name, args.profile, not args.no_semantic, db=args.db)
    elif args.command == "compare":
        sys.exit(compare(args.before, args.after, tuple(args.expect)))
    else:
        for path in sorted(SNAPSHOT_DIR.glob("*/meta.json")):
            meta = json.loads(path.read_text(encoding="utf-8"))
            print(f"{meta['name']}\t{meta['profile']}\t{meta['commit']}\t{meta['recorded_at']}")


if __name__ == "__main__":
    main()
