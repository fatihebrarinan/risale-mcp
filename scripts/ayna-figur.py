"""S13.23.4: sohbetin yeni konuşma sayfasındaki ayna figürleri (kullanıcının fikri, 2026-11-27: başlığın üstünde
ayna, aynanın içinde kütüphane; her yeni konuşmada dördünden biri rastgele).

A: raflar, kandil, rahle üstünde açık kitap (logodaki kırmızı kapaklı kitap). B: derinlik, iki yanı raflı koridor,
sonda kemerli pencereden ışık. C ve D: A'nın ve B'nin çizgi hâlleri; sayfada rengini temadan alır (CSS maskesi).
Kitap sırtları sabit tohumla üretilir: betik yeniden çalışınca çizim değişmez.

    python3 scripts/ayna-figur.py              # src/risale_mcp/sohbet_assets/ayna-{a,b,c,d}.svg
    python3 scripts/ayna-figur.py --onizleme <klasör>   # dört temada önizleme sayfası da
"""
import random
import sys
from pathlib import Path
OUT = str(Path(__file__).resolve().parent.parent / "src" / "risale_mcp" / "sohbet_assets") + "/"
GOLD, GOLD_D, GOLD_L = "#e8c766", "#b8953a", "#f5dc8e"
SPINES = ["#b8322a", "#9e2a23", "#e6dbbd", "#c9a24e", "#3e7f66", "#2f4f6f", "#7a4b2a", "#d9c08a", "#5b3a5e", "#c46a3a"]

FRAME_OUT = "M40 292 V132 C40 72 84 34 120 16 C156 34 200 72 200 132 V292 Z"
GLASS = "M52 286 V134 C52 82 90 48 120 31 C150 48 188 82 188 134 V286 Z"

def defs(uid):
    return f'''<defs>
<clipPath id="cam-{uid}"><path d="{GLASS}"/></clipPath>
<linearGradient id="arka-{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2f6f57"/><stop offset="1" stop-color="#163a2e"/></linearGradient>
<radialGradient id="isik-{uid}" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{GOLD_L}" stop-opacity=".9"/><stop offset=".35" stop-color="{GOLD}" stop-opacity=".35"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>
<linearGradient id="cerceve-{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{GOLD_L}"/><stop offset=".5" stop-color="{GOLD}"/><stop offset="1" stop-color="{GOLD_D}"/></linearGradient>
<linearGradient id="parilti-{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
</defs>'''

def shelf_row(rng, y, x0, x1, hmin=26, hmax=38):
    out, x = [], x0
    while x < x1 - 6:
        w = rng.choice([5, 6, 7, 7, 8, 9, 10])
        if x + w > x1: break
        h = rng.randint(hmin, hmax)
        c = rng.choice(SPINES)
        lean = rng.random() < .07 and x + w + 8 < x1
        if lean:
            out.append(f'<rect x="{x+3}" y="{y-h}" width="{w}" height="{h}" rx="1" fill="{c}" transform="rotate(14 {x+3} {y})"/>')
            x += w + 9; continue
        out.append(f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}" rx="1" fill="{c}"/>')
        if rng.random() < .55:
            out.append(f'<rect x="{x}" y="{y-h+5}" width="{w}" height="1.6" fill="{GOLD}" opacity=".75"/>')
            out.append(f'<rect x="{x}" y="{y-9}" width="{w}" height="1.6" fill="{GOLD}" opacity=".75"/>')
        out.append(f'<rect x="{x+w-1.2}" y="{y-h}" width="1.2" height="{h}" fill="#000" opacity=".18"/>')
        x += w + (1 if rng.random() < .8 else 3)
    return "".join(out)

def frame_back(uid):
    return f'''<path d="{FRAME_OUT}" fill="url(#cerceve-{uid})" stroke="url(#cerceve-{uid})" stroke-width="8" stroke-linejoin="round"/>
<path d="M46 290 V133 C46 77 87 41 120 23 C153 41 194 77 194 133 V290" fill="none" stroke="{GOLD_L}" stroke-width="1.2" opacity=".8"/>'''


def frame(uid):
    return f'''<path d="{GLASS}" fill="none" stroke="{GOLD_D}" stroke-width="2" opacity=".95"/>
<path d="M33 128 C33 66 80 26 120 8 C160 26 207 66 207 128" fill="none" stroke="{GOLD}" stroke-width="1.4" opacity=".55"/>
<circle cx="120" cy="9" r="5" fill="url(#cerceve-{uid})"/><path d="M120 1 L123 6 L117 6 Z" fill="{GOLD}"/>
<rect x="24" y="288" width="192" height="14" rx="7" fill="url(#cerceve-{uid})"/>
<rect x="36" y="300" width="168" height="6" rx="3" fill="{GOLD_D}"/>'''

def glint(uid):
    return f'''<path d="M64 150 L104 70 L116 70 L76 150 Z" fill="url(#parilti-{uid})"/>
<path d="M82 168 L118 96 L123 96 L87 168 Z" fill="url(#parilti-{uid})" opacity=".7"/>'''

def lectern():
    # rahle ve açık, kırmızı kapaklı kitap (logodaki gibi)
    return f'''<g>
<path d="M98 286 L142 252 M142 286 L98 252" stroke="#7a4b2a" stroke-width="5" stroke-linecap="round"/>
<path d="M98 286 L142 252 M142 286 L98 252" stroke="#a0683a" stroke-width="2" stroke-linecap="round"/>
<path d="M120 252 C109 245 97 243 86 244 L86 262 C97 261 109 263 120 270 Z" fill="#b8322a"/>
<path d="M120 252 C131 245 143 243 154 244 L154 262 C143 261 131 263 120 270 Z" fill="#9e2a23"/>
<path d="M120 248 C110 241 100 239 91 240 L91 257 C100 256 110 258 120 265 Z" fill="#f6efdc"/>
<path d="M120 248 C130 241 140 239 149 240 L149 257 C140 256 130 258 120 265 Z" fill="#e6dbbd"/>
<path d="M96 245 h16 M96 249 h18 M96 253 h15 M127 245 h16 M126 249 h18 M128 253 h15" stroke="#9a8f74" stroke-width=".9" opacity=".7"/>
</g>'''

def lamp(uid, cx=120, cy=70):
    return f'''<circle cx="{cx}" cy="{cy+10}" r="34" fill="url(#isik-{uid})"/>
<path d="M{cx} 31 V{cy-6}" stroke="{GOLD_D}" stroke-width="1.2"/>
<path d="M{cx-9} {cy-6} h18 l-3 8 h-12 Z" fill="{GOLD}"/>
<path d="M{cx-7} {cy+2} C{cx-10} {cy+12} {cx+10} {cy+12} {cx+7} {cy+2} Z" fill="{GOLD_L}"/>
<circle cx="{cx}" cy="{cy+7}" r="2.4" fill="#fff8dc"/>'''

def variant_a(uid="a", seed=7):
    rng = random.Random(seed)
    shelves = [128, 176, 224, 272]
    parts = [f'<rect x="40" y="20" width="160" height="280" fill="url(#arka-{uid})"/>']
    # rafların arka duvarı: hafif dikey bölmeler
    parts.append('<rect x="52" y="96" width="136" height="190" fill="#000" opacity=".12"/>')
    for y in shelves:
        parts.append(shelf_row(rng, y, 54, 186))
        parts.append(f'<rect x="50" y="{y}" width="140" height="5" fill="#7a4b2a"/><rect x="50" y="{y}" width="140" height="1.5" fill="#c79a5a"/>')
    parts.append('<rect x="52" y="96" width="5" height="190" fill="#5e3a20"/><rect x="183" y="96" width="5" height="190" fill="#5e3a20"/>')
    parts.append(lamp(uid))
    parts.append('<rect x="52" y="236" width="136" height="50" fill="#163a2e" opacity=".55"/>')
    parts.append(lectern())
    parts.append(glint(uid))
    inner = "".join(parts)
    return svg(uid, inner)

def variant_b(uid="b", seed=11):
    """Derinlik: raflar iki yanda uzaklaşır, sonda kemerli pencereden ışık."""
    rng = random.Random(seed)
    p = [f'<rect x="40" y="20" width="160" height="280" fill="url(#arka-{uid})"/>']
    vx, vy = 120, 150   # kaçış noktası
    # uzaktaki kemerli pencere ve ışık
    p.append(f'<circle cx="{vx}" cy="{vy-8}" r="46" fill="url(#isik-{uid})"/>')
    p.append(f'<path d="M108 168 V140 C108 130 114 124 120 121 C126 124 132 130 132 140 V168 Z" fill="{GOLD_L}" opacity=".85"/>')
    p.append(f'<path d="M120 121 V168 M108 146 H132" stroke="#2f6f57" stroke-width="1.2" opacity=".6"/>')
    # zemin
    p.append(f'<path d="M52 286 L108 168 H132 L188 286 Z" fill="#173d30"/>')
    p.append(f'<path d="M120 168 V286 M114 168 L96 286 M126 168 L144 286" stroke="#2f6f57" stroke-width="1" opacity=".5"/>')
    # iki yandaki raf duvarları (yamuk), raf çizgileri ve kitap sırtları
    for side in (-1, 1):
        xn, xf = (52, 108) if side < 0 else (188, 132)
        wall = f'M{xn} 60 L{xf} 128 L{xf} 168 L{xn} 286 Z'
        p.append(f'<path d="{wall}" fill="#24563f"/>')
        levels = 5
        for i in range(levels + 1):
            t = i / levels
            yn, yf = 60 + t * 226, 128 + t * 40
            p.append(f'<path d="M{xn} {yn:.1f} L{xf} {yf:.1f}" stroke="#7a4b2a" stroke-width="{2.6 - 1.2*0:.1f}"/>')
        # kitaplar: her rafta, yakından uzağa daralan sırtlar
        for i in range(levels):
            t0, t1 = i / levels, (i + 1) / levels
            k = 0.0
            while k < 0.94:
                w = rng.uniform(.035, .07) * (1 - .55 * k)
                c = rng.choice(SPINES)
                a, b = k, min(k + w, 1)
                def pt(u, tt):
                    x = xn + (xf - xn) * u
                    ytop = 60 + tt * 226 + ((128 + tt * 40) - (60 + tt * 226)) * u
                    return x, ytop
                hfrac = rng.uniform(.62, .92)
                x1, ya1 = pt(a, t1); x2, yb1 = pt(b, t1)
                _, ya0 = pt(a, t0); _, yb0 = pt(b, t0)
                ytopa = ya1 - (ya1 - ya0) * hfrac
                ytopb = yb1 - (yb1 - yb0) * hfrac
                p.append(f'<path d="M{x1:.1f} {ya1-1:.1f} L{x1:.1f} {ytopa:.1f} L{x2:.1f} {ytopb:.1f} L{x2:.1f} {yb1-1:.1f} Z" fill="{c}"/>')
                k = b + .004
        p.append(f'<path d="{wall}" fill="none" stroke="#000" stroke-opacity=".15"/>')
    # tavan kemeri
    p.append(f'<path d="M52 60 L108 128 H132 L188 60" fill="none" stroke="#7a4b2a" stroke-width="3"/>')
    p.append(lectern())
    p.append(glint(uid))
    return svg(uid, "".join(p))

def variant_c(uid="c", seed=5):
    """Çizgi: tema rengiyle (currentColor), sade."""
    rng = random.Random(seed)
    p = []
    for y in (128, 176, 224):
        x = 58
        while x < 180:
            w = rng.choice([5, 6, 7, 8]); h = rng.randint(24, 36)
            if x + w > 182: break
            p.append(f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}" rx="1"/>')
            x += w + 2
        p.append(f'<path d="M52 {y} H188"/>')
    lampc = '<path d="M120 31 V58 M111 58 h18 l-3 8 h-12 Z M113 66 C110 76 130 76 127 66"/>'
    book = ('<path d="M120 256 C109 249 97 247 86 248 L86 266 C97 265 109 267 120 274 Z M120 256 C131 249 143 247 154 248 '
            'L154 266 C143 265 131 267 120 274 Z"/><path d="M98 286 L142 260 M142 286 L98 260"/>')
    inner = "".join(p) + lampc + book
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 310" class="ayna-c">
<g fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round">
<path d="{FRAME_OUT}" stroke-width="3"/><path d="{GLASS}"/>
<rect x="24" y="288" width="192" height="14" rx="7" stroke-width="2"/>
<circle cx="120" cy="9" r="4"/>
<g opacity=".8">{inner}</g>
<path d="M66 146 L100 80 M80 160 L112 98" opacity=".35"/>
</g></svg>'''

def variant_d(uid="d", seed=11):
    """B'nin çizgi hâli: koridor, iki yanda raflar, sonda kemerli pencere; tema renginde (currentColor)."""
    rng = random.Random(seed)
    p = []
    p.append('<path d="M52 60 L108 128 H132 L188 60"/>')                       # tavan
    p.append('<path d="M52 286 L108 168 H132 L188 286"/>')                    # zemin kenarları
    p.append('<path d="M108 128 V168 M132 128 V168"/>')
    p.append('<path d="M110 168 V142 C110 133 115 127 120 124 C125 127 130 133 130 142 V168 Z M120 124 V168 M110 148 H130"/>')
    p.append('<path d="M114 172 L104 246 M126 172 L136 246" opacity=".4"/>')
    for side in (-1, 1):
        xn, xf = (52, 108) if side < 0 else (188, 132)
        levels = 5
        for i in range(levels + 1):
            tt = i / levels
            p.append(f'<path d="M{xn} {60 + tt*226:.1f} L{xf} {128 + tt*40:.1f}"/>')
        for i in range(levels):
            t0, t1 = i / levels, (i + 1) / levels
            k = 0.02
            while k < 0.9:
                w = rng.uniform(.08, .13) * (1 - .45 * k)
                u = k
                x = xn + (xf - xn) * u
                ybot = 60 + t1 * 226 + ((128 + t1 * 40) - (60 + t1 * 226)) * u
                ytop0 = 60 + t0 * 226 + ((128 + t0 * 40) - (60 + t0 * 226)) * u
                h = (ybot - ytop0) * rng.uniform(.6, .9)
                p.append(f'<path d="M{x:.1f} {ybot-1:.1f} V{ybot-h:.1f}"/>')
                k += w
    book = ('<path d="M120 256 C109 249 97 247 86 248 L86 266 C97 265 109 267 120 274 Z M120 256 C131 249 143 247 154 248 '
            'L154 266 C143 265 131 267 120 274 Z"/><path d="M98 286 L142 260 M142 286 L98 260"/>')
    inner = "".join(p) + book
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 310" class="ayna-d">
<g fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round">
<path d="{FRAME_OUT}" stroke-width="3"/><path d="{GLASS}"/>
<rect x="24" y="288" width="192" height="14" rx="7" stroke-width="2"/>
<circle cx="120" cy="9" r="4"/>
<g opacity=".8" stroke-width="1.3">{inner}</g>
<path d="M66 146 L100 80 M80 160 L112 98" opacity=".35"/>
</g></svg>'''

def svg(uid, inner):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 310">{defs(uid)}{frame_back(uid)}
<g clip-path="url(#cam-{uid})">{inner}</g>{frame(uid)}</svg>'''

THEMES = {
    "Açık": dict(bg="#fbfaf7", fg="#1d1d1b", muted="#6b6a66", line="#dcd8cf", card="#fff", accent="#1f5c3f", soft="#e3efe7"),
    "Koyu": dict(bg="#161614", fg="#e8e6e1", muted="#9c9a94", line="#34332f", card="#1f1e1b", accent="#7cc49d", soft="#22352a"),
    "Sepya": dict(bg="#f4ecd8", fg="#3b2f20", muted="#7a6a52", line="#dccfb0", card="#fbf5e6", accent="#7a4b2a", soft="#ead9b8"),
    "Zümrüt": dict(bg="#10291f", fg="#efe8d4", muted="#a9b8a8", line="#24493a", card="#163528", accent="#e8c766", soft="#22432f"),
}

def panel(theme, t, fig, label):
    return f'''<div class="p" style="background:{t['bg']};color:{t['fg']};border-color:{t['line']}">
<div class="tag" style="color:{t['muted']}">{theme} · {label}</div>
<div class="fig" style="color:{t['accent']}">{fig}</div>
<h2>Ne sormak istersiniz?</h2>
<p style="color:{t['muted']}">Cevaplar Risale-i Nur'dan alıntılarla gelir.</p>
<div class="card" style="background:{t['card']};border-color:{t['line']}"><b style="color:{t['accent']}">MESELELER</b><br>Kader ile cüz-i ihtiyarî nasıl bağdaşır?</div>
<div class="btn" style="background:{t['accent']};color:{t['bg']}">Sor</div>
</div>'''

css = """body{margin:0;font:15px/1.5 system-ui;background:#888}
.row{display:grid;grid-template-columns:repeat(4,300px);gap:14px;padding:14px}
.p{border:1px solid;border-radius:14px;padding:18px;text-align:center}
.tag{font-size:12px;text-align:left;margin-bottom:6px}
.fig svg{width:150px;height:auto;filter:drop-shadow(0 6px 14px rgba(0,0,0,.22))}
h2{font:600 22px Georgia,serif;margin:8px 0 2px}.p p{margin:0 0 12px;font-size:13px}
.card{border:1px solid;border-radius:10px;padding:8px 10px;text-align:left;font-size:13px;margin-bottom:10px}
.btn{display:inline-block;border-radius:8px;padding:6px 16px}"""

def main() -> None:
    a, b, c, dd = variant_a(), variant_b(), variant_c(), variant_d()
    for name, s in (("a", a), ("b", b), ("c", c), ("d", dd)):
        Path(OUT + f"ayna-{name}.svg").write_text(s + "\n", encoding="utf-8")
    print(f"yazıldı: {OUT}ayna-{{a,b,c,d}}.svg")
    if "--onizleme" in sys.argv:
        folder = Path(sys.argv[sys.argv.index("--onizleme") + 1])
        folder.mkdir(parents=True, exist_ok=True)
        rows = ""
        for n, th in THEMES.items():
            rows += '<div class="row">' + "".join(panel(n, th, fig, label) for fig, label in
                                                  ((a, "A"), (b, "B"), (c, "C"), (dd, "D"))) + "</div>"
        (folder / "onizleme.html").write_text(f"<!doctype html><meta charset=utf-8><style>{css}</style>{rows}",
                                              encoding="utf-8")
        print(f"önizleme: {folder / 'onizleme.html'}")


if __name__ == "__main__":
    main()
