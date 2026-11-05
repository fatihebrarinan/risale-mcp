#!/usr/bin/env python3
"""Kurulum sayfalarının ekran görüntülerini hazırlar.

Kullanıcının çektiği asıl görüntüler data/raw/kullanici/ekran-goruntuleri/ altındadır (git'e girmez,
sunucuya gitmez: kişisel bilgi taşıyabilirler). Bu betik her birini bulanıklaştırır (kişisel bilgiler),
küçültür ve site/img/kurulum/<ad>.webp olarak yazar; sitede yalnız bunlar durur.

Çalıştırma (Pillow sistem Python'ında var, projenin ortamında yok):
    python3 scripts/ekran-goruntuleri.py

Yeni görüntü eklenince IMAGES listesine bir satır eklenir. Bulanıklaştırma kutuları asıl görüntünün
piksel koordinatlarıdır (sol, üst, sağ, alt).
"""

from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data/raw/kullanici/ekran-goruntuleri"
OUT = ROOT / "site/img/kurulum"

WEB_WIDTH = 1280  # masaüstü görüntüleri
PHONE_WIDTH = 540  # telefon görüntüleri

# Kırpma kutuları: tam ekran görüntü 720 piksellik sütunda okunmuyor; pencere ya da menü kırpılır.
SIDEBAR = (0, 0, 960, 450)
TOPBAR = (560, 20, 1660, 360)
DIALOG = (640, 180, 1270, 770)
TALL_DIALOG = (650, 10, 1265, 924)
CONNECT = (880, 420, 1350, 650)

# (yayımlanan ad, asıl dosya, bulanıklaştırılacak kutular, kırpma kutusu ya da None)
IMAGES = [
    # Claude, web, sitedeki düğmeyle
    ("claude-web-dugme-1", "claude_web_linkle_1_tr.png", [], DIALOG),
    ("claude-web-dugme-2", "claude_web_linkle_2_tr.png", [], TALL_DIALOG),
    ("claude-web-dugme-3", "claude_web_linkle_3_tr.png", [], CONNECT),
    ("claude-web-dugme-1-en", "claude_web_linkle_1_en.png", [], DIALOG),
    ("claude-web-dugme-2-en", "claude_web_linkle_2_en.png", [], TALL_DIALOG),
    ("claude-web-dugme-3-en", "claude_web_linkle_3_en.png", [], CONNECT),
    # Claude, web, elle
    *[(f"claude-web-elle-{n}{lang}", f"claude_web_elle_{n}_{src}.png", [], box)
      for lang, src in (("", "tr"), ("-en", "en"))
      for n, box in ((1, SIDEBAR), (2, TOPBAR), (3, TOPBAR), (4, TOPBAR), (5, DIALOG))],
    # Claude, web, sohbette bağdaştırıcının açık olduğu
    ("claude-web-sohbette", "claude_web_aktivasyon_dogrulaması_tr.png", [], (740, 380, 1490, 740)),
    # Claude, web, proje ("İyi akşamlar, <ad>" selamı bulanık)
    ("claude-web-proje-1", "claude_web_proje_1.png", [(920, 330, 1290, 395)], SIDEBAR),
    ("claude-web-proje-2", "claude_web_proje_2.png", [], (560, 20, 1660, 220)),
    ("claude-web-proje-3", "claude_web_proje_3.png", [], (660, 250, 1255, 700)),
    ("claude-web-proje-4", "claude_web_proje_4.png", [], (460, 60, 1750, 480)),
    ("claude-web-proje-5", "claude_web_proje_5.png", [], (550, 190, 1360, 765)),
    # Claude, telefon, sitedeki düğmeyle (tarayıcı)
    *[(f"claude-mobil-dugme-{n}", f"claude_mobil_linkle_{n}.jpeg", [], None) for n in range(1, 5)],
    # Claude, telefon, uygulamada elle (5 ve 6: hesabın e-postası)
    *[(f"claude-mobil-elle-{n}", f"claude_mobil_elle_{n}.jpeg", [], None) for n in range(1, 5)],
    ("claude-mobil-elle-5", "claude_mobil_elle_5.jpeg", [(30, 190, 1044, 270)], None),
    ("claude-mobil-elle-6", "claude_mobil_elle_6.jpeg", [(30, 190, 1044, 270)], None),
    ("claude-mobil-elle-7", "claude_mobil_elle_7.jpeg", [], None),
    # Claude, telefon, proje
    *[(f"claude-mobil-proje-{n}", f"claude_mobil_proje_{n}.jpeg", [], None) for n in range(1, 6)],
    # ChatGPT, web (sol menüde kullanıcının sohbet ve proje adları var: kırpma dışarıda bırakır)
    ("chatgpt-web-1", "gpt_web_1.png", [], (1380, 0, 1919, 200)),
    ("chatgpt-web-2", "gpt_web_2.png", [], (1380, 0, 1919, 200)),
    ("chatgpt-web-3", "gpt_web_3.png", [], (655, 95, 1262, 800)),
    ("chatgpt-web-4", "gpt_web_4.png", [], (715, 228, 1202, 725)),
    ("chatgpt-web-proje-1", "gpt_web_proje_1.png", [], (0, 0, 720, 500)),
    ("chatgpt-web-proje-2", "gpt_web_proje_2.png", [], (700, 340, 1220, 615)),
    ("chatgpt-web-proje-3", "gpt_web_proje_3.png", [], (800, 55, 1460, 260)),
    ("chatgpt-web-proje-4", "gpt_web_proje_4.png", [], (800, 55, 1460, 260)),
    ("chatgpt-web-proje-5", "gpt_web_proje_5.png", [], (700, 160, 1220, 795)),
    # ChatGPT, web, İngilizce arayüz
    ("chatgpt-web-1-en", "gpt_web_1_en.png", [], (1380, 0, 1919, 200)),
    ("chatgpt-web-2-en", "gpt_web_2_en.png", [], (1380, 0, 1919, 200)),
    ("chatgpt-web-3-en", "gpt_web_3_en.png", [], (655, 90, 1262, 765)),
    ("chatgpt-web-4-en", "gpt_web_4_en.png", [], (715, 238, 1202, 720)),
    ("chatgpt-web-proje-1-en", "gpt_web_proje_1_en.png", [], (0, 0, 720, 500)),
    ("chatgpt-web-proje-2-en", "gpt_web_proje_2_en.png", [], (700, 345, 1220, 615)),
    ("chatgpt-web-proje-3-en", "gpt_web_proje_3_en.png", [], (800, 55, 1460, 265)),
    ("chatgpt-web-proje-4-en", "gpt_web_proje_4_en.png", [], (800, 55, 1460, 265)),
    ("chatgpt-web-proje-5-en", "gpt_web_proje_5_en.png", [], (700, 160, 1220, 800)),
    # ChatGPT, telefonun tarayıcısı (proje 3–5: adres çubuğunda projenin kimliği)
    *[(f"chatgpt-mobil-{n}", f"gpt_mobil_{n}.jpeg", [], None) for n in range(1, 6)],
    *[(f"chatgpt-mobil-proje-{n}", f"gpt_mobil_proje_{n}.jpeg", [], None) for n in range(1, 3)],
    *[(f"chatgpt-mobil-proje-{n}", f"gpt_mobil_proje_{n}.jpeg", [(0, 0, 1044, 130)], None) for n in range(3, 6)],
]


def blur(img: Image.Image, box: tuple[int, int, int, int]) -> None:
    region = img.crop(box)
    # Önce iyice küçültüp büyütmek yazıyı geri okunamaz kılar; ardından yumuşatılır.
    w, h = region.size
    region = region.resize((max(1, w // 24), max(1, h // 24))).resize((w, h))
    img.paste(region.filter(ImageFilter.GaussianBlur(8)), box)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, source, boxes, crop in IMAGES:
        img = Image.open(SRC / source).convert("RGB")
        for box in boxes:
            blur(img, box)
        if crop:
            img = img.crop(crop)
        width = PHONE_WIDTH if img.height > img.width else WEB_WIDTH
        if img.width > width:
            img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
        target = OUT / f"{name}.webp"
        img.save(target, "WEBP", quality=82, method=6)
        print(f"{target.relative_to(ROOT)}  {img.width}x{img.height}  {target.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
