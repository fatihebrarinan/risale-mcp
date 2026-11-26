#!/usr/bin/env python3
"""Âyinedâr ad yazısının yazı tipi (S13.15.3–4): Literata (OFL 1.1, github.com/googlefonts/literata), ağırlık 500,
optik boy 24'te sabit, yalnız Türkçe Latin harfleri ve "·". Sayfalar kendi sunucumuzdan verir (dışarıya istek yok).

    curl -sSL -o <klasör>/literata.ttf "https://github.com/google/fonts/raw/main/ofl/literata/Literata%5Bopsz%2Cwght%5D.ttf"
    uv run --no-project --with fonttools --with brotli python -I scripts/literata-alt.py <klasör>/literata.ttf
"""
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = Path(__file__).resolve().parents[1]
OUT = [ROOT / "src/risale_mcp/sohbet_assets/literata-ad.woff2", ROOT / "site-ayinedar/literata-ad.woff2"]
TEXT = ("ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZQWX abcçdefgğhıijklmnoöprsştuüvyzqwx ÂÎÛâîû·'’-.,:0123456789")

font = instancer.instantiateVariableFont(TTFont(sys.argv[1]), {"wght": 500, "opsz": 24})
options = subset.Options()
options.flavor = "woff2"
options.layout_features = ["kern", "liga", "ccmp", "locl", "mark", "mkmk"]
options.name_IDs = [0, 1, 2, 13, 14]              # telif ve lisans satırları kalır (OFL şartı)
sub = subset.Subsetter(options)
sub.populate(text=TEXT)
sub.subset(font)
for out in OUT:
    font.flavor = "woff2"
    font.save(out)
    print(out.relative_to(ROOT), out.stat().st_size, "bayt")
