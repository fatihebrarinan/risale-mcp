#!/usr/bin/env bash
# İkonları src/risale_mcp/static/icon.svg'den üretir ve sunucuya ve siteye koyar:
#   icon.png (256×256) ve favicon.ico (16–256 piksel, PNG'li ICO). Claude ve bağlayıcı dizini simgeyi
#   sunucu adresindeki favicon'dan alır (bkz. CLAUDE.md, Logo). Sonra: scripts/deploy.sh --code
#
#   scripts/ikon.sh
set -euo pipefail
cd "$(dirname "$0")/.."
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
svg=src/risale_mcp/static/icon.svg
for size in 16 32 48 64 128 256; do
    uvx -q --from cairosvg cairosvg "$svg" -o "$tmp/$size.png" -W $size -H $size
done
python3 - "$tmp" <<'PY'
import struct, sys
from pathlib import Path
tmp = Path(sys.argv[1])
images = [(size, (tmp / f"{size}.png").read_bytes()) for size in (16, 32, 48, 64, 128, 256)]
head = struct.pack("<HHH", 0, 1, len(images))
offset, entries = 6 + 16 * len(images), b""
for size, data in images:                       # 256 piksel ICO'da 0 diye yazılır
    entries += struct.pack("<BBBBHHII", size % 256, size % 256, 0, 0, 1, 32, len(data), offset)
    offset += len(data)
(tmp / "favicon.ico").write_bytes(head + entries + b"".join(d for _, d in images))
PY
for dir in src/risale_mcp/static site; do
    cp "$tmp/256.png" "$dir/icon.png"
    cp "$tmp/favicon.ico" "$dir/favicon.ico"
done
file src/risale_mcp/static/favicon.ico
