"""S12.11, S13.1, S13.5, S13.6, S13.7, S13.13, S13.14: sohbet sayfasını başsız tarayıcıda baştan sona dener (geniş, orta ve telefon genişliği).

Yerel sunucu açık olmalı (`SOHBET_GUNLUK_SORU=100 uv run --extra sohbet python -m risale_mcp.sohbet serve --dev`: deneme hesabının
günlük hakkı her koşuda bir azalır). Deneme hesabına
(`deneme@example.com`, yoksa açılır) oturum açar, iki soru sorar (gerçek API, ≈0,02 $; ikincisi konu taraması kipinde). Dener: sol panel (geçmiş,
konuşmanın adresi, yeniden yükleyince aynı konuşma, ad değiştirme, yeni konuşma, silme), sağda Kaynaklar ve metin
görünümü, ayarlar penceresi (saklama ayarı, belgeler), alt satır (uyarı ve günün kalan hakkı), geri bildirim,
orta genişlikte Kaynaklar çekmecesi, telefonda iki çekmece, perde ve Escape. Ekran görüntüleri
`data/interim/sohbet/arayuz/`. Tarayıcı Brave (Chromium); Playwright proje bağımlılığı değildir:

    uv run --no-project --with playwright python scripts/sohbet-arayuz-dene.py [--url http://127.0.0.1:8010/sohbet/]
"""
import argparse
import asyncio
import re
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


SEED = """
import json, sys
from risale_mcp.sohbet import Conversations
from risale_mcp.sohbet_hesap import Store
convs = Conversations(Store())
if sys.argv[1:2] == ["sil"]:
    convs.delete(EMAIL, sys.argv[2]); raise SystemExit
def src(n, a, b=None):
    span = f"c{a:03d}" + (f"..c{b:03d}" if b else "")
    tail = f"“İlk{a}…”" + (f" ile başlayan {b - a + 1} cümle" if b else "")
    return {"n": n, "id": "sozler/11/" + span, "cite_as": "Sözler › Onbirinci Söz › " + tail, "source_name": "e-Risale"}
one = {"raw": "", "markdown": 'Bir [1], iki [2], yirmi [3].', "sources": [src(1, 1), src(2, 2), src(3, 20)]}
two = {"raw": "", "markdown": 'Otuz [1], yine iki [2], aralık [3], sekiz [4], dokuzuncu [5].',
       "sources": [src(1, 30), src(2, 2), src(3, 19, 21), src(4, 40, 47), src(5, 48)]}
ident, _ = convs.add(EMAIL, None, "Kaynak numaralama denemesi", one)
convs.add(EMAIL, ident, "İkinci soru", two)
hadis = {"n": 1, "id": "sualar/13/talebe-i-ulumun-hatta-uykusu-dahi/c004", "source_name": "e-Risale",
         "cite_as": "Şualar › Onüçüncü Şuâ › Talebe‑i Ulûmun Hattâ Uykusu Dahi İbâdet Sayılır › “Böyle medresesiz bir zamanda,…”",
         "embedded": [{"kind": "hadis", "line": "Hadis: el-Aclûnî, Keşfü'l-Hafâ: 1:55 (doğrulanmadı)"}]}
convs.add(EMAIL, ident, "Üçüncü soru", {"raw": "", "markdown": "Hadisli cümle [1].\\n\\n:::ek Bütün yerler: 3 cümle, 2 yer\\n"
          "- Sözler › Onuncu Söz · 2 cümle\\n- Şualar › Meyve Risalesi (Tarihçe-i Hayat'ta da) · 1 cümle\\n:::", "sources": [hadis]})
print(ident)
"""


def seed(*args: str) -> str:
    """S13.5: iki turlu, ortak kaynaklı bir konuşma (API çağrısı yok); `seed("sil", kimlik)` siler."""
    import subprocess
    out = subprocess.run(["uv", "run", "python", "-c", f"EMAIL = {EMAIL!r}\n" + SEED, *args], cwd=ROOT,
                         capture_output=True, text=True)
    if out.returncode:
        raise SystemExit(f"deneme konuşması kurulamadı:\n{out.stderr}")
    return out.stdout.strip()


async def run(url: str) -> None:
    from playwright.async_api import async_playwright
    OUT.mkdir(parents=True, exist_ok=True)
    origin = url.split("/sohbet")[0]
    token = session()
    checks: list[tuple[str, bool]] = []
    check = lambda name, ok: checks.append((name, bool(ok)))
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=BROWSER, headless=True)
        ctx = await browser.new_context(viewport={"width": 1440, "height": 880})
        await ctx.add_cookies([{"name": "sohbet_oturum", "value": token, "url": origin}])
        page = await ctx.new_page()
        errors: list[str] = []
        page.on("pageerror", lambda e: errors.append(f"pageerror {e}"))
        page.on("console", lambda m: m.type == "error" and errors.append(f"console {m.text}"))   # CSP ihlalleri dahil
        page.on("response", lambda r: r.status >= 400 and errors.append(f"{r.status} {r.url}"))
        visible = lambda sel: page.locator(sel).first.is_visible()

        async def until(js: str, timeout: float = 10.0) -> None:
            """Playwright'ın bekleme işlevi sayfanın CSP'sine takılır (eval yok); `evaluate` takılmaz."""
            for _ in range(int(timeout * 10)):
                if await page.evaluate(js):
                    return
                await page.wait_for_timeout(100)
            raise TimeoutError(js)

        # ---------------------------------------------- geniş ekran: iki panel yerinde
        await page.goto(url)
        await page.request.post(f"{url}api/konusma/sil", data={"all": True})     # deneme hesabının eski konuşmaları
        await page.request.post(f"{url}api/ayarlar", data={"keep": True})       # yarım kalan koşu kapatmış olabilir
        await page.evaluate("localStorage.clear()")
        await page.reload()
        await page.wait_for_selector("#hak:not([hidden])")
        check("geniş: sol panel açık", await visible("#sol"))
        check("geniş: Kaynaklar paneli açık", await visible("#yan"))
        check("geniş: sol paneli açan düğme gizli", not await visible("#sol-ac"))
        footer = await page.inner_text(".alt .not")
        check("alt satır: uyarı", "Tefsir ve fetva değildir, müellife mal edilmez." in footer)
        check("alt satır: kalan hak", re.search(r"Bugünkü soru hakkı: \d+/\d+", footer))
        check("alt satırda gizlilik bağlantısı yok", await page.locator(".alt a").count() == 0)
        check("boş konuşmada rozet gizli", not await visible("#yan-sayi"))
        check("yeni konuşmada 6 örnek, her biri türüyle", await page.locator("#ornekler .ornek").count() == 6
              and await page.locator("#ornekler .ornek .ornek-tur").count() == 6)
        first = await page.inner_text("#ornekler")
        await page.click("#baska-ornek")
        check("başka örnekler", await page.locator("#ornekler .ornek").count() == 6)
        await page.screenshot(path=OUT / "1-bos.png")

        await page.fill("#soru", QUESTION)
        await page.click("#gonder")
        await page.wait_for_selector(".adimlar li", timeout=120000)
        check("beklerken adımlar dizilir", "okunuyor" in await page.inner_text(".tur") or "aranıyor" in await page.inner_text(".tur"))
        await page.screenshot(path=OUT / "2-adimlar.png")
        await page.wait_for_selector("#yan-liste .kaynak", timeout=180000)
        await until("location.hash.startsWith('#k/')")
        await page.wait_for_selector("#gecmis li.secili")
        await page.screenshot(path=OUT / "2-cevap-genis.png")
        ident = (await page.evaluate("location.hash"))[3:]
        check("konuşma adreste", len(ident) > 8)
        check("geçmişte seçili konuşma", QUESTION[:20] in await page.inner_text("#gecmis li.secili"))
        check("başlıkta konuşmanın adı", QUESTION[:20] in await page.inner_text("#baslik"))
        check("geniş: cevabın altındaki liste gizli", not await visible(".tur .kaynaklar"))
        check("cevabın üstünde adım özeti", "adımda hazırlandı" in await page.inner_text(".tur .adim-ozet summary"))
        check("kaynak adı var", "Kaynak:" in await page.inner_text("#yan-liste"))
        hak = await page.inner_text("#hak")
        await page.click(".cevap .ref >> nth=0")
        await page.wait_for_selector("#metin-govde .cumle", timeout=20000)
        await page.screenshot(path=OUT / "3-metin-genis.png")
        check("metinde işaretli cümle", await page.locator("#metin-govde mark").count() > 0)
        check("metinde kaynak adı", "Kaynak:" in await page.inner_text("#metin-kaynak"))
        await page.click("#yan-geri")
        # S12.12: geri bildirim (kutu işaretsiz: soru ve cevap gitmez); oy saklanan tura da yazılır
        # S13.4: oy tıklanınca gider, not yazmayı bırakınca; Gönder düğmesi yok
        await page.click(".geri .oy >> nth=0")
        await page.wait_for_selector(".geri .geri-durum >> text=Teşekkürler.", timeout=10000)
        check("oy tıklanınca gitti", await page.locator(".geri .oy.secili").count() == 1)
        check("Gönder düğmesi yok", await page.locator(".geri button[type=submit]").count() == 0)
        check("oy simgesi emoji değil", "👍" not in await page.inner_text(".geri"))
        await page.fill(".geri-form textarea", "arayüz denemesi")
        await page.wait_for_selector(".geri .geri-durum >> text=Notunuz alındı", timeout=10000)
        check("not kendiliğinden gitti", True)

        # yeniden yükleyince aynı konuşma, oyuyla
        await page.reload()
        await page.wait_for_selector(".tur .cevap p")
        check("adım özeti saklandı", await page.locator(".tur .adim-ozet").count() == 1)
        check("yeniden yüklemede aynı konuşma", await page.locator(".tur").count() == 1)
        check("oy saklandı", await page.locator(".geri >> text=Geri bildiriminiz alındı").count() == 1
              and await page.locator(".geri .oy.secili").count() == 1)
        check("kalan hak aynı", await page.inner_text("#hak") == hak)

        # ad değiştirme
        await page.hover("#gecmis li.secili")
        await page.click("#gecmis li.secili .islem .ikon >> nth=0")
        await page.fill("#gecmis input", "Arayüz denemesi")
        await page.keyboard.press("Enter")
        await page.wait_for_selector("#gecmis li.secili >> text=Arayüz denemesi")
        check("ad değişti (liste ve başlık)", "Arayüz denemesi" in await page.inner_text("#baslik"))

        # yeni konuşma ve geri dönüş
        await page.click("#yeni")
        check("yeni konuşma boş", await visible("#bos") and await page.locator(".tur").count() == 0)
        check("yeni konuşmada adres boş", await page.evaluate("location.hash") == "")
        await page.click("#gecmis li .ac >> text=Arayüz denemesi")
        await page.wait_for_selector(".tur .cevap p")
        check("listeden konuşma açılır", await page.locator(".tur").count() == 1)

        # ayarlar (S13.2: sekmeli)
        await page.click("#ayarlar-ac")
        await page.wait_for_selector("#ayarlar[open]")
        await page.screenshot(path=OUT / "4-ayarlar-hesap.png")
        check("ayarlar Hesap sekmesiyle açılır", await visible("#ayar-hesap") and not await visible("#ayar-konusmalar"))
        check("Hesap sekmesinde çıkış ve hesabı silme", "Çıkış yap" in await page.inner_text("#ayar-hesap")
              and "Hesabımı sil" in await page.inner_text("#ayar-hesap"))
        await page.click("#sekme-konusmalar")
        check("ayarlarda saklama açık", await page.is_checked("#sakla"))
        await page.click("#sakla")
        await until("!document.querySelector('#sakla').disabled")
        check("saklama kapanınca liste uyarır", "Saklama kapalı" in await page.inner_text("#gecmis"))
        await page.click("#sakla")
        await until("!document.querySelector('#sakla').disabled")
        await page.focus("#sekme-konusmalar")
        await page.keyboard.press("ArrowDown")
        check("ok tuşu sonraki sekmeye geçer", await visible("#ayar-gorunum"))
        size = await page.evaluate("getComputedStyle(document.querySelector('.cevap')).fontSize")
        await page.click("#ayar-gorunum label:has(input[value='koyu'])")
        await page.click("#ayar-gorunum label:has(input[value='buyuk'])")
        await page.screenshot(path=OUT / "4-ayarlar-gorunum.png")
        check("koyu tema", await page.evaluate("document.documentElement.dataset.tema") == "koyu")
        check("yazı büyür", float((await page.evaluate("getComputedStyle(document.querySelector('.cevap')).fontSize"))[:-2]) > float(size[:-2]))
        await page.click("#sekme-belgeler")
        text = await page.inner_text("#ayar-belgeler")
        check("Belgeler'de gizlilik ve şartlar", "Gizlilik politikası" in text and "Kullanım şartları" in text)
        await page.keyboard.press("Escape")
        check("Escape ayarları kapatır", not await visible("#ayarlar"))
        await page.reload()
        await page.wait_for_selector(".tur .cevap p")
        check("görünüm yeniden yüklemede kalır", await page.evaluate("document.documentElement.dataset.tema") == "koyu")
        await page.screenshot(path=OUT / "4-koyu.png")
        await page.evaluate("localStorage.removeItem('sohbet:gorunum')")
        await page.reload()
        await page.wait_for_selector(".tur .cevap p")

        # panel genişliği (S13.2): çizgiyi sürüklemek, klavye, çift tıklama
        width = lambda sel: page.evaluate(f"document.querySelector('{sel}').getBoundingClientRect().width")
        box = await page.locator("#ayir-sol").bounding_box()
        x, y = box["x"] + box["width"] / 2, box["y"] + 300
        await page.mouse.move(x, y)
        await page.mouse.down()
        await page.mouse.move(x + 80, y, steps=5)
        await page.mouse.up()
        check("sol panel sürüklenerek genişler", abs(await width("#sol") - 352) <= 2)
        box = await page.locator("#ayir-yan").bounding_box()
        x = box["x"] + box["width"] / 2
        await page.mouse.move(x, y)
        await page.mouse.down()
        await page.mouse.move(x - 100, y, steps=5)
        await page.mouse.up()
        check("Kaynaklar sürüklenerek genişler", abs(await width("#yan") - 480) <= 2)
        await page.screenshot(path=OUT / "4-genislik.png")
        await page.mouse.move(x - 100, y)
        await page.mouse.down()
        await page.mouse.move(x - 900, y, steps=5)
        await page.mouse.up()
        check("sohbet en dar 420 piksel kalır", await width(".orta") >= 419)
        await page.reload()
        await page.wait_for_selector(".tur .cevap p")
        check("genişlik yeniden yüklemede kalır", abs(await width("#sol") - 352) <= 2)
        await page.focus("#ayir-sol")
        await page.keyboard.press("ArrowLeft")
        check("ok tuşu daraltır", abs(await width("#sol") - 336) <= 2)
        await page.dblclick("#ayir-sol")
        check("çift tıklama eski genişlik", abs(await width("#sol") - 272) <= 2)
        await page.click("#ayarlar-ac")
        await page.click("#sekme-gorunum")
        await page.click("#genislik-sifirla")
        await page.keyboard.press("Escape")
        check("sıfırla: Kaynaklar eski genişlik", abs(await width("#yan") - 380) <= 2)

        # panelleri kapatıp açmak
        await page.click("#sol-kapat")
        check("sol panel kapanır", not await visible("#sol") and await visible("#sol-ac"))
        await page.click("#yan-kapat")
        check("Kaynaklar kapanınca liste cevabın altında", await visible(".tur .kaynaklar"))
        await page.screenshot(path=OUT / "5-paneller-kapali.png")
        await page.reload()
        await page.wait_for_selector(".tur .cevap p")
        check("panel tercihi kalır", not await visible("#sol") and not await visible("#yan"))
        await page.click("#sol-ac")
        await page.click("#yan-ac")
        check("paneller yeniden açılır", await visible("#sol") and await visible("#yan"))

        # ---------------------------------------------- orta genişlik: sol yerinde, Kaynaklar çekmece
        await page.set_viewport_size({"width": 1024, "height": 800})
        await page.wait_for_timeout(300)
        check("orta: sol yerinde", await visible("#sol"))
        check("orta: Kaynaklar kapalı, liste cevabın altında", not await visible("#yan") and await visible(".tur .kaynaklar"))
        await page.click("#yan-ac")
        await page.wait_for_timeout(400)
        check("orta: Kaynaklar çekmecesi açılır", await visible("#yan-liste"))
        await page.screenshot(path=OUT / "6-orta-cekmece.png")
        await page.click("#perde", position={"x": 100, "y": 300})
        await page.wait_for_timeout(400)

        # ---------------------------------------------- telefon: iki çekmece
        await page.set_viewport_size({"width": 390, "height": 844})
        await page.reload()
        await page.wait_for_selector(".tur .cevap p")
        await page.screenshot(path=OUT / "7-telefon-cevap.png")
        check("telefonda çekmeceler kapalı", not await visible("#sol") and not await visible("#yan"))
        check("telefonda cevabın altında kaynaklar", await visible(".tur .kaynaklar"))
        await page.click("#sol-ac")
        await page.wait_for_timeout(400)
        check("telefonda sol çekmece açılır", await visible("#gecmis"))
        await page.screenshot(path=OUT / "8-telefon-sol.png")
        await page.click("#gecmis li .ac >> text=Arayüz denemesi")
        await page.wait_for_timeout(400)
        check("konuşma seçilince çekmece kapanır", not await visible("#sol"))
        await page.click("#yan-ac")
        await page.wait_for_timeout(400)
        check("düğmeyle Kaynaklar çekmecesi açılır", await visible("#yan-liste"))
        await page.click("#yan-liste .kaynak >> nth=0")
        await page.wait_for_selector("#metin-govde .cumle")
        await page.wait_for_timeout(300)
        await page.screenshot(path=OUT / "9-telefon-metin.png")
        await page.click("#yan-geri")
        await page.click("#perde", position={"x": 15, "y": 400})
        await page.wait_for_timeout(400)
        check("perdeye dokununca kapanır", not await visible("#yan"))
        await page.click(".cevap .ref >> nth=0")
        await page.wait_for_timeout(500)
        check("[n] çekmeceyi metinle açar", await visible("#yan-metin"))
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(400)
        check("Escape kapatır", not await visible("#yan"))

        # silme (deneme hesabının konuşması)
        await page.set_viewport_size({"width": 1440, "height": 880})
        await page.wait_for_timeout(300)
        # S13.5: konuşmanın tek kaynakçası (hazır konuşma; API yok)
        seeded = seed()
        await page.goto(f"{url}#k/{seeded}")
        await page.reload()
        await page.wait_for_selector(".tur >> nth=1")
        refs = await page.locator(".tur >> nth=1").locator(".cevap .ref").all_inner_texts()
        # S13.6: bitişik (c001, c002) ve iç içe (c020 ⊂ c019..c021) birleşir; 8'i aşan (c040..c047 + c048) birleşmez
        check("ikinci cevapta konuşmanın numaraları, parçalarıyla", refs == ["[3]", "[1]", "[2]", "[4]", "[5]"])
        under = await page.locator(".tur >> nth=1").locator(".kaynaklar .no").all_inner_texts()
        check("cevabın altında yalnız onun kaynakları, sıralı", under == ["[1]", "[2]", "[3]", "[4]", "[5]"])
        side = await page.locator("#yan-liste .kaynak .no").all_inner_texts()
        check("sağda tek liste, her parça bir kez", side == ["[1]", "[2]", "[3]", "[4]", "[5]", "[6]"])
        check("bölüm başlığı bir kez", await page.locator("#yan-liste .kaynak-grup h3").all_inner_texts()
              == ["Sözler › Onbirinci Söz", "Şualar › Onüçüncü Şuâ › Talebe‑i Ulûmun Hattâ Uykusu Dahi İbâdet Sayılır"])
        check("listede âyet ve hadis satırı yok (S13.7)", "Hadis:" not in await page.inner_text("#yan-liste"))
        check("parça birleşik aralıkla", "“İlk19…” ile başlayan 3 cümle" in await page.inner_text('#yan-liste .kaynak[data-g="2"]'))
        check("ortak parçada iki soru", "1. ve 2. soruda" in await page.inner_text('#yan-liste .kaynak[data-g="1"]'))
        await page.screenshot(path=OUT / "14-tek-kaynakca.png")
        await page.locator(".tur >> nth=1").locator(".cevap .ref >> nth=1").click()
        await page.wait_for_selector("#metin-govde .cumle")
        check("atıf parçanın numarasıyla açılır", await page.inner_text("#yan-baslik") == "[1]")
        check("atfın cümlesi koyu, parçanın öbürü açık", await page.locator("#metin-govde mark:not(.acik)").count() == 1
              and await page.locator("#metin-govde mark.acik").count() == 1)
        await page.screenshot(path=OUT / "15-parca-vurgu.png")
        await page.click("#yan-geri")
        check("açılan kaynak listede seçili", await page.locator('#yan-liste .kaynak.secili[data-g="1"]').count() == 1)
        await page.locator(".tur >> nth=2").locator(".cevap .ref >> nth=0").click()
        await page.wait_for_selector("#metin-govde .meal")
        meals = await page.locator("#metin-govde .meal").all_inner_texts()
        check("metinde hadis satırı notu ve mealiyle (S13.7)",
              "Hadis: el-Aclûnî, Keşfü'l-Hafâ: 1:55 (doğrulanmadı) · nâşirin meali: İşlerin en hayırlısı zorlu olanıdır." in meals)
        await page.screenshot(path=OUT / "16-ayet-hadis-satiri.png")
        await page.click("#yan-geri")
        # S13.13: taramanın bütün yerleri kapalı ekte; açılınca liste
        ek = page.locator(".tur >> nth=2").locator("details.ek")
        check("kapalı ek: başlık görünür, liste kapalı", await ek.count() == 1 and not await ek.locator("li >> nth=0").is_visible())
        await ek.locator("summary").click()
        check("kapalı ek açılır", await ek.locator("li").count() == 2 and "Tarihçe-i Hayat'ta da" in await ek.inner_text())
        check("ekin işaretleri metne sızmaz", ":::" not in await page.inner_text(".tur >> nth=2"))
        seed("sil", seeded)
        await page.goto(url)
        await page.wait_for_selector("#gecmis li")
        await page.click("#gecmis li .ac >> text=Arayüz denemesi")
        await page.wait_for_selector("#gecmis li.secili")
        await page.hover("#gecmis li.secili")
        await page.click("#gecmis li.secili .islem .ikon >> nth=1")
        await page.click("#gecmis .onay .dolu-tehlike")
        await until("location.hash === ''")
        check("silinen konuşma listeden gider", await page.locator(f"#gecmis li .ac >> text=Arayüz denemesi").count() == 0)
        # S13.13: tarama kipinde bir soru (gerçek API); cevaptan sonra kip serbeste döner, sonda bütün yerler eki
        await page.click("#yeni")
        await page.click("#kipler .kip >> text=Konu taraması")
        check("tarama kipi seçilir", "Konu taraması" in await page.inner_text("#kipler .kip.secili"))
        await page.fill("#soru", "Mevlânâ")
        await page.click("#gonder")
        await page.wait_for_selector(".tur .cevap details.ek", timeout=240000)
        summaries = " | ".join(await page.locator(".tur .cevap details.ek summary").all_inner_texts())
        check("tarama cevabında öbür yerler ve bütün yerler eki", "Konunun geçtiği öbür yerler" in await page.inner_text(".tur .cevap")
              and "Kelimelerin geçtiği bütün yerler" in summaries)
        check("cevabın altında kapsam notu (S13.14)", "Bu cevabın dayandığı okumalar" in summaries)
        check("tarama cevabından sonra kip serbest", "Serbest soru" in await page.inner_text("#kipler .kip.secili"))
        await page.screenshot(path=OUT / "17-tarama.png")
        await page.hover("#gecmis li.secili")
        await page.click("#gecmis li.secili .islem .ikon >> nth=1")
        await page.click("#gecmis .onay .dolu-tehlike")
        await until("location.hash === ''")
        # girişsiz: hesap oluşturma sayfası, tanıtımlı (S13.3)
        anon = await browser.new_context(viewport={"width": 1440, "height": 880})
        apage = await anon.new_page()
        await apage.goto(url)
        check("girişsiz açılış hesap oluşturma", apage.url.endswith("/kayit") and "Hesap oluşturun" in await apage.inner_text("h1"))
        check("tanıtım var", await apage.locator(".tanitim h2").is_visible())
        await apage.screenshot(path=OUT / "11-kayit.png")
        await apage.click("text=Giriş yapın")
        check("girişe geçiş", apage.url.endswith("/giris") and "Giriş yapın" in await apage.inner_text("h1"))
        await apage.screenshot(path=OUT / "12-giris.png")
        await apage.set_viewport_size({"width": 390, "height": 844})
        await apage.goto(url)
        await apage.screenshot(path=OUT / "13-kayit-telefon.png", full_page=True)
        check("telefonda form görünür", await apage.locator('input[type="email"]').is_visible())
        await anon.close()
        await browser.close()
    check("tarayıcı hatası yok", not errors)
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
