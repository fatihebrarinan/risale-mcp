#!/usr/bin/env bash
# OpenAI eklenti dizini için ZIP paketi: packaging/chatgpt/ (plugin.json, mcp.json, assets/) ->
# data/interim/chatgpt/risale-i-nur.zip. Portal: https://platform.openai.com/plugins (bkz. docs/chatgpt-dizin-basvurusu.md).
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data/interim/chatgpt
uv run python - <<'PY'
import zipfile
from pathlib import Path
src, out = Path("packaging/chatgpt"), Path("data/interim/chatgpt/risale-i-nur.zip")
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(p for p in src.rglob("*") if p.is_file()):
        z.write(f, f.relative_to(src))
print(out, [i.filename for i in zipfile.ZipFile(out).infolist()])
PY
