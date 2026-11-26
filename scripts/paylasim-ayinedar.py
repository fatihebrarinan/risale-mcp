"""Âyinedâr'ın paylaşım kartları (Open Graph, 1200×630): sohbetinki (S13.15.4) ve çatınınki (S13.15.6).

    uv run --no-project --with playwright python scripts/paylasim-ayinedar.py [sohbet] [cati]

Şablonlar `scripts/paylasim-*.html`; simge ve ad yazısı `site-ayinedar/`'dan.
"""
import asyncio
import sys
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
CARDS = {"sohbet": (ROOT / "scripts/paylasim-sohbet.html", ROOT / "src/risale_mcp/sohbet_assets/paylasim.jpg"),
         "cati": (ROOT / "scripts/paylasim-cati.html", ROOT / "site-ayinedar/img/paylasim.png")}


async def main(names: list[str]) -> None:
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(executable_path="/usr/bin/brave-browser")
        page = await browser.new_page(viewport={"width": 1200, "height": 630})
        for name in names:
            source, out = CARDS[name]
            out.parent.mkdir(parents=True, exist_ok=True)
            await page.goto(source.as_uri())
            await page.evaluate("document.fonts.ready")
            if out.suffix == ".jpg":
                await page.screenshot(path=out, type="jpeg", quality=85)
            else:
                await page.screenshot(path=out, type="png")
            print(out.relative_to(ROOT), out.stat().st_size, "bayt")
        await browser.close()


asyncio.run(main(sys.argv[1:] or list(CARDS)))
