"""S13.15.4: chat.ayinedar.org'un paylaşım kartı (site-ayinedar/paylasim-sohbet.html → sohbet_assets/paylasim.jpg).

    uv run --no-project --with playwright python scripts/paylasim-ayinedar.py
"""
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
SOURCE, OUT = ROOT / "site-ayinedar/paylasim-sohbet.html", ROOT / "src/risale_mcp/sohbet_assets/paylasim.jpg"


async def main() -> None:
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(executable_path="/usr/bin/brave-browser")
        page = await browser.new_page(viewport={"width": 1200, "height": 630})
        await page.goto(SOURCE.as_uri())
        await page.evaluate("document.fonts.ready")
        await page.screenshot(path=OUT, type="jpeg", quality=85)
        await browser.close()
    print(OUT.relative_to(ROOT), OUT.stat().st_size, "bayt")


asyncio.run(main())
