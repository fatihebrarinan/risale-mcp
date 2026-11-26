#!/usr/bin/env bash
# Âyinedâr simgeleri (S13.15.3): site-ayinedar/icon*.svg'den
#   favicon.ico      16 ve 32 piksel icon-kucuk.svg'den, 48–256 icon.svg'den (PNG'li ICO)
#   icon.png         256×256 (icon.svg)
#   icon-192.png, icon-512.png                 PWA (icon.svg)
#   icon-maskable-512.png, apple-touch-icon.png (180)   PWA "maskable" ve Apple (icon-maskable.svg; köşesiz)
# Eklentilerin simgeleri ayrıdır (scripts/ikon.sh). Sonra: scripts/deploy.sh --site
#
#   scripts/ikon-ayinedar.sh
set -euo pipefail
cd "$(dirname "$0")/../site-ayinedar"
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
svg() { uvx -q --from cairosvg cairosvg "$1" -o "$2" -W "$3" -H "$3"; }
for s in 16 32; do svg icon-kucuk.svg "$tmp/$s.png" $s; done
for s in 48 64 128 256; do svg icon.svg "$tmp/$s.png" $s; done
python3 - "$tmp" <<'PY'
import struct, sys
from pathlib import Path
tmp = Path(sys.argv[1])
images = [(s, (tmp / f"{s}.png").read_bytes()) for s in (16, 32, 48, 64, 128, 256)]
head = struct.pack("<HHH", 0, 1, len(images))
offset, entries = 6 + 16 * len(images), b""
for s, data in images:                       # 256 piksel ICO'da 0 diye yazılır
    entries += struct.pack("<BBBBHHII", s % 256, s % 256, 0, 0, 1, 32, len(data), offset)
    offset += len(data)
(tmp / "favicon.ico").write_bytes(head + entries + b"".join(d for _, d in images))
PY
cp "$tmp/favicon.ico" favicon.ico
cp "$tmp/256.png" icon.png
svg icon.svg icon-192.png 192
svg icon.svg icon-512.png 512
svg icon-maskable.svg icon-maskable-512.png 512
svg icon-maskable.svg apple-touch-icon.png 180
file favicon.ico icon.png icon-192.png icon-512.png icon-maskable-512.png apple-touch-icon.png
