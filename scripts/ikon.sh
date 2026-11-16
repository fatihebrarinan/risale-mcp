#!/usr/bin/env bash
# İkonları src/risale_mcp/static/icon*.svg'den üretir:
#   icon.svg        -> icon.png (256×256) ve favicon.ico (16–256 piksel, PNG'li ICO); sunucuya ve siteye
#   icon-<ad>.svg   -> icon-<ad>.png ve favicon-<ad>.ico (hadis, tefsir, klasik; yalnız sunucuya, S4.6)
# Claude ve bağlayıcı dizini simgeyi sunucunun alan adından alır (bkz. CLAUDE.md, Logo); her alt alan adlı sunucu
# kendi simgesini verir. Sonra: scripts/deploy.sh --code (ve tefsir makinesi için scripts/tefsir-sunucu.sh gonder)
#
#   scripts/ikon.sh
set -euo pipefail
cd "$(dirname "$0")/.."
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
static=src/risale_mcp/static
for svg in "$static"/icon.svg "$static"/icon-*.svg; do
    name=$(basename "$svg" .svg)                       # icon, icon-hadis…
    suffix=${name#icon}                                # "", -hadis…
    mkdir -p "$tmp/$name"
    for size in 16 32 48 64 128 256; do
        uvx -q --from cairosvg cairosvg "$svg" -o "$tmp/$name/$size.png" -W $size -H $size
    done
    python3 - "$tmp/$name" <<'PY'
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
    cp "$tmp/$name/256.png" "$static/$name.png"
    cp "$tmp/$name/favicon.ico" "$static/favicon$suffix.ico"
    if [[ -z "$suffix" ]]; then
        cp "$tmp/$name/256.png" site/icon.png
        cp "$tmp/$name/favicon.ico" site/favicon.ico
    fi
done
file "$static"/favicon*.ico
