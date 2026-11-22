#!/usr/bin/env bash
# OpenAI eklenti dizini için ZIP paketleri: packaging/chatgpt*/ (plugin.json, mcp.json, assets/) ->
# data/interim/chatgpt/<ad>.zip. Portal: https://platform.openai.com/plugins (bkz. docs/s4-dizin-basvurulari.md §6, §7).
#
#   scripts/chatgpt-paket.sh              # Risale (packaging/chatgpt/ -> risale-mcp.zip; iç adı risale-i-nur)
#   scripts/chatgpt-paket.sh hadis tefsir klasik   # packaging/chatgpt-<ad>/ -> <plugin.json'daki name>.zip
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data/interim/chatgpt
uv run python - "${@:-risale}" <<'PY'
import json
import sys
import zipfile
from pathlib import Path
for ad in sys.argv[1:]:
    src = Path("packaging/chatgpt" if ad == "risale" else f"packaging/chatgpt-{ad}")
    name = "risale-mcp" if ad == "risale" else json.loads((src / "plugin.json").read_text())["name"]
    out = Path(f"data/interim/chatgpt/{name}.zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(p for p in src.rglob("*") if p.is_file()):
            z.write(f, f.relative_to(src))
    print(out, [i.filename for i in zipfile.ZipFile(out).infolist()])
PY
