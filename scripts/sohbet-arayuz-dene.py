"""S12.11: sohbet sayfasını başsız tarayıcıda baştan sona dener (masaüstü ve telefon genişliği).

Yerel sunucu açık olmalı (`uv run --extra sohbet python -m risale_mcp.sohbet serve --dev`). Deneme hesabına
(`deneme@example.com`, yoksa açılır) oturum açar, bir soru sorar (gerçek API, ≈0,003 $), cevabı, sol Kaynaklar panelini,
metin görünümünü, telefonda çekmeceyi, perdeyi ve Escape'i dener; ekran görüntüleri `data/interim/sohbet/arayuz/`.
Tarayıcı Brave (Chromium); Playwright proje bağımlılığı değildir:

    uv run --no-project --with playwright python scripts/sohbet-arayuz-dene.py [--url http://127.0.0.1:8010/sohbet/]
"""
import argparse
import asyncio
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "interim" / "sohbet" / "arayuz"
BROWSER = "/usr/bin/brave-browser"
EMAIL = "deneme@example.com"
QUESTION = "Birinci Söz'deki iki adam temsilini kısaca anlatır mısın?"


def session() -> str:
    """Deneme hesabına oturum (proje ortamı olmadan: `sohbet_hesap.Store.open_session` ile aynı kayıt)."""
    import subprocess
    out = subprocess.run(["uv", "run", "python", "-c", "from risale_mcp.sohbet_hesap import Store; "
                          f"s = Store(); print(s.open_session({EMAIL!r}))"], cwd=ROOT, capture_output=True, text=True)
    if out.returncode:
        raise SystemExit(f"oturum açılamadı (hesap {EMAIL} var mı?):\n{out.stderr}")
    return out.stdout.strip()


async def run(url: str) -> None:
    from playwright.async_api import async_playwright
    OUT.mkdir(parents=True, exist_ok=True)
    origin = url.split("/sohbet")[0]
    token = session()
    checks: list[tuple[str, bool]] = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=BROWSER, headless=True)
        ctx = await browser.new_context(viewport={"width": 1280, "height": 820})
        await ctx.add_cookies([{"name": "sohbet_oturum", "value": token, "url": origin}])
        page = await ctx.new_page()
        errors: list[str] = []
        page.on("pageerror", lambda e: errors.append(f"pageerror {e}"))
        page.on("response", lambda r: r.status >= 400 and errors.append(f"{r.status} {r.url}"))
        await page.goto(url)
        await page.evaluate("localStorage.clear()")
        await page.reload()
        checks.append(("boş konuşmada rozet gizli", not await page.locator("#yan-sayi").is_visible()))
        await page.screenshot(path=OUT / "1-bos.png")
        await page.fill("#soru", QUESTION)
        await page.click("#gonder")
        await page.wait_for_selector("#yan-liste .kaynak", timeout=180000)
        await page.screenshot(path=OUT / "2-cevap-masaustu.png")
        checks.append(("masaüstünde cevabın altındaki liste gizli", not await page.locator(".tur .kaynaklar").first.is_visible()))
        checks.append(("kaynak adı var", "Kaynak:" in await page.inner_text("#yan-liste")))
        await page.click(".cevap .ref >> nth=0")
        await page.wait_for_selector("#metin-govde .cumle", timeout=20000)
        await page.screenshot(path=OUT / "3-metin-masaustu.png")
        checks.append(("metinde işaretli cümle", await page.locator("#metin-govde mark").count() > 0))
        checks.append(("metinde kaynak adı", "Kaynak:" in await page.inner_text("#metin-kaynak")))
        await page.set_viewport_size({"width": 390, "height": 844})
        await page.reload()
        await page.wait_for_selector(".tur .cevap p")
        await page.screenshot(path=OUT / "4-telefon-cevap.png")
        checks.append(("telefonda çekmece kapalı", not await page.locator("#yan").is_visible()))
        checks.append(("telefonda cevabın altında kaynaklar", await page.locator(".tur .kaynaklar").first.is_visible()))
        await page.click("#yan-ac")
        await page.wait_for_timeout(400)
        await page.screenshot(path=OUT / "5-telefon-cekmece.png")
        checks.append(("düğmeyle çekmece açılır", await page.locator("#yan-liste").is_visible()))
        await page.click("#yan-liste .kaynak >> nth=0")
        await page.wait_for_selector("#metin-govde .cumle")
        await page.wait_for_timeout(300)
        await page.screenshot(path=OUT / "6-telefon-metin.png")
        await page.click("#yan-geri")
        await page.click("#perde", position={"x": 200, "y": 40})
        await page.wait_for_timeout(400)
        checks.append(("perdeye dokununca kapanır", not await page.locator("#yan").is_visible()))
        await page.click(".cevap .ref >> nth=0")
        await page.wait_for_timeout(500)
        checks.append(("[n] çekmeceyi metinle açar", await page.locator("#yan-metin").is_visible()))
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(400)
        checks.append(("Escape kapatır", not await page.locator("#yan").is_visible()))
        await browser.close()
    checks.append(("tarayıcı hatası yok", not errors))
    for name, ok in checks:
        print(("✓ " if ok else "✗ ") + name)
    for e in errors:
        print("  ", e)
    print(f"ekran görüntüleri: {OUT}")
    if not all(ok for _, ok in checks):
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8010/sohbet/")
    asyncio.run(run(parser.parse_args().url))
