"""Taslağın kaynaktan alıntısı, kaynaktaki cümlesiyle (S7f, kullanıcının kararı 2026-11-21).

Taslak bir kaynağın cümlesinden yalnız bir parça alıntılayabilir (Bakara 34: İşârât'tan «تولّد أنانية إبليس فيما بين
الملائكة», yüklemsiz bir tamlama); parça tek başına okunmaz. Okuma platformu ve masa için:

- `cumle`: alıntının geçtiği kaynak cümle(ler)in tamamı, alıntı cümlenin bir parçasıysa ("kaynaktaki cümlenin tamamı").
- `amt`: alıntı İşârât'ın Arapçasındansa o cümlenin Abdülmecid Nursî tercümesi (`isarat-esleme.turkcesi`); yapay zekâ
  tercümesinin yerine gösterilir (kullanıcının kararı: İşârât'ın Türkçesi Abdülmecid'in tercümesidir).

Yalnız sunuştur: taslağın metni ve yayın dosyası değişmez. Kaynak cümle, kaynakçadaki kimliğin aralığında aranır
(Arapça harf iskeletiyle, `quran.pieces`; Türkçe `normalize.search_words` ile; "…" atlanan yer).
"""
from __future__ import annotations

import importlib.util
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from risale_mcp.normalize import search_words      # noqa: E402
from risale_mcp.paths import DIST_DIR               # noqa: E402
from risale_mcp.quran import pieces, skeleton       # noqa: E402

PROFILE = {"risale": "genel", "tefsir": "tefsir", "klasik": "klasik"}
_CONN: dict[str, sqlite3.Connection | None] = {}
_ISARAT = None
ARABIC = re.compile(r"[؀-ۿ]")


def _isarat():
    global _ISARAT
    if _ISARAT is None:
        if "isarat_esleme" in sys.modules:
            _ISARAT = sys.modules["isarat_esleme"]
        else:
            spec = importlib.util.spec_from_file_location("isarat_esleme", ROOT / "scripts" / "isarat-esleme.py")
            _ISARAT = importlib.util.module_from_spec(spec)
            sys.modules["isarat_esleme"] = _ISARAT
            spec.loader.exec_module(_ISARAT)
    return _ISARAT


def _conn(server: str) -> sqlite3.Connection | None:
    if server not in _CONN:
        p = DIST_DIR / PROFILE.get(server, "") / "risale.db"
        _CONN[server] = sqlite3.connect(f"file:{p}?mode=ro", uri=True) if server in PROFILE and p.exists() else None
    return _CONN[server]


def sentences(server: str, kimlik: str) -> list[tuple[str, str]]:
    """Kaynakçadaki kimliğin cümleleri [(id, metin)] (`a..cNNN` aralığı aynı bölümde)."""
    c = _conn(server)
    if not c or not kimlik:
        return []
    first, _, last = kimlik.partition("..")
    end = first.rsplit("/", 1)[0] + "/" + last if last else first
    a = c.execute("SELECT seq, node_id FROM sentences WHERE id = ?", (first,)).fetchone()
    b = c.execute("SELECT seq FROM sentences WHERE id = ?", (end,)).fetchone()
    if not a:
        return []
    return c.execute("SELECT id, text FROM sentences WHERE node_id = ? AND seq BETWEEN ? AND ? ORDER BY seq",
                     (a[1], a[0], b[0] if b else a[0])).fetchall()


def clean(quote: str) -> str:
    q = re.sub(r"\[[^\]\n]{1,80}\]", "", quote).strip()
    return q.strip(" \"“”«»'‘’").strip()


def _norm(text: str, ar: bool) -> list[str]:
    if ar:
        return pieces(text)
    return [" ".join(search_words(p)) for p in re.split(r"…|\.\.\.", text) if search_words(p)]


def context(server: str | None, kimlik: str | None, quote: str) -> dict:
    """Alıntının kaynaktaki cümlesi: {"id", "cumle" (parçaysa), "amt" (İşârât'ın Arapçasıysa)}; bulunamazsa {}."""
    if server not in PROFILE or not kimlik:
        return {}
    q = clean(quote)
    ar = bool(ARABIC.search(q))
    want = _norm(q, ar)
    if not want:
        return {}
    rows = sentences(server, kimlik)
    norm = (lambda t: skeleton(t)) if ar else (lambda t: " ".join(search_words(t)))
    hit = next(([r] for r in rows if all(w in norm(r[1]) for w in want)), None)
    if hit is None:                                       # birden çok cümleye yayılan alıntı
        joined = " ".join(t for _, t in rows)
        if not rows or not all(w in norm(joined) for w in want):
            return {}
        idx = [i for i, (_, t) in enumerate(rows) if any(w[:12] in norm(t) for w in want)]
        hit = rows[min(idx):max(idx) + 1] if idx else rows
    text = " ".join(t for _, t in hit)
    out = {"id": hit[0][0] if len(hit) == 1 else f"{hit[0][0]}..{hit[-1][0].rsplit('/', 1)[1]}"}
    if sum(map(len, want)) < 0.9 * len(norm(text)):
        out["cumle"] = text
    if hit[0][0].startswith("isaratul-icaz-arabi/"):
        amt = [x for sid, _ in hit if (x := _isarat().turkcesi(sid))]
        if amt:
            out["amt"] = " ".join(dict.fromkeys(amt))
    return out
