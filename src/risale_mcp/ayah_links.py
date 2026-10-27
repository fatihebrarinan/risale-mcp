"""Aşama 14: âyet ilişkileri — Risale'nin hangi yerinin hangi âyetle bağ kurduğu.

Kullanım:
    uv run python -m risale_mcp.ayah_links     # data/interim/ayah_links/{links.md, sample-<tur>.md}

İlişkiler `build_db` sırasında veritabanından kurallarla çıkarılır (`ayah_links` tablosu); her biri
metindeki bir kanıt cümlesine dayanır. Bunlar "tefsir" diye anılmaz: bir yerin bir âyetin tefsiri
olduğu bir hükümdür, kurallar ise yalnızca metnin âyetle kurduğu bağı bulur (kullanıcının kararı).

Türler (`kind`):
- `isaret`: metin bağı kendisi söyler: âyetin geçtiği cümlede "işâret", "remz", "nükte", "tefsir",
  "mânâ", "meâl" ("…âyetlerin işâret ettiği…", "… âyeti buna işâret eder.").
- `acilis`: bölüm âyetle açılır: ilk paragrafı (hâşiye sayılmaz) âyet olan Arapça paragraftır.
  Besmele açılış sayılmaz. Arapça eserde (İşaratü'l-İ'caz) bütün metin Arapçadır: Bakara'nın âyet bölümü
  başlığındaki âyetle ("6. Âyetin Tefsiri", basılı âyet satırı alt başlıkta), Fâtiha'nın bölümü işlediği
  âyet parçasıyla ("(الحَمْدُ) …"; `quran.FATIHA_VERSES`) açılır.
- `izah`: müellifin kendi izahı: âyetten hemen sonra, ya da cümlesi âyetle bitiyorsa sonraki cümlenin
  başında "Yani". Aslı Arapça eserlerde (İşaratü'l-İ'caz, Mesnevî-i Nuriye) izah müellifin, Türkçe
  ifadesi mütercimindir.
- `dayanak`: metin âyete dayanır: "… sırrınca / sırrıyla / fermânıyla / mûcibince".
- `risale`: âyetin Risale-i Nur'a işâreti (Şualar › Birinci Şuâ ve başlığında "Risale-i Nur'a işâret"
  geçen bölümler). Klasik anlamda bir bağ değil, işârî bir delâlettir; ayrı tutulur.

Kapsam ve güç: bağ bölümün ilk iki cümlesinde kuruluyorsa (ve `acilis`'te) bölümün tamamını kapsar
(`scope = section`), değilse yalnızca o cümleyi (`sentence`). İlk gözden geçirmede (kullanıcı, 40'lık
örneklem) çıkan kurallar:
- "İşâret" gibi kelime âyetin yakınında olmalı (araya en çok `CUE_WORDS` Türkçe kelime; Arapça sayılmaz);
  uzun bir cümlenin başka yerindeyse bağ zayıftır. Âyet cümlenin başındaysa (önünde en çok `HEAD_WORDS`
  kelime) cümlenin öznesidir; kelime uzakta da olsa bağ kurulur.
- Âyet sûrenin adı olarak anılıyorsa ("Sûre‑i وَالتّ۪ينِ", "اِقْرَأْ … Sûresi") bağ zayıftır. Cümle cifir/ebced
  hesabıyla işâretten söz ediyorsa da zayıftır; ancak âyet cümlenin başındaysa ("İkinci Cümle: … kelime-i
  kudsiyesi … makam-ı cifrîsiyle … işâret ediyor") bölüm o âyetin işâretini anlatır, güçlü kalır.
- "İşârât-ı Kur'âniye", "İşârâtü'l-İ'câz" risale adlarıdır; içindeki "işârât" kanıt sayılmaz.
- Mektuplar ve Lâhikalar çoğu zaman "وَاِنْ مِنْ شَيْءٍ اِلَّا يُسَبِّحُ بِحَمْدِه۪" ibaresiyle açılır; bu bir
  açılış ibaresidir, bölümün konusu değildir: mektup eserlerinde yalnız başına bu ibareyle açılan bölüm
  `acilis` sayılmaz. Bölüm kapsamlılar ve `izah` güçlü
(`strong`), cümle kapsamlı `isaret`, `dayanak` ve `risale` zayıftır (`weak`): metin o cümlede âyete
atıf yapar, bölümün konusu olduğu söylenemez.

Hizbler (Kur'ân metninin kendisi) ve mecmualar (metni ana ciltlerde) ilişki üretmez; Fihrist
bölümleri de (içindekiler özetidir).
"""

import argparse
import json
import random
import re
import sqlite3
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from risale_mcp.db import connect
from risale_mcp.normalize import search_words
from risale_mcp.paths import INTERIM_DIR, ROOT
from risale_mcp.quran import skeleton, verse_context

OUT_DIR = INTERIM_DIR / "ayah_links"
REVIEWS = ROOT / "tests" / "golden" / "ayah_links_review.json"   # kullanıcının örneklem kararları
KINDS = ("isaret", "acilis", "izah", "dayanak", "risale")
OPENING_SENTENCES = 2           # bu kadar cümle içinde kurulan bağ bölümün tamamını kapsar
BESMELE = (1, 1)
SAMPLE_SIZE, SAMPLE_SEED = 40, 14

_ISARET = re.compile(r"işâret|işaret|remz|nükte|tefsîr|tefsir|mânâ|ma'nâ|meâl|meal", re.I)
_DAYANAK = re.compile(r"sırrınca|sırrına|sırrıyla|ferm[âa]nıyla|ferm[âa]nınca|mûcibince|mucibince", re.I)
_YANI = re.compile(r"^[\s\W]{0,4}(?:Yani|Yâni|Ya'ni|Ya‘ni|Ya’ni|Yanî|Yâ'ni|Yâ‘ni)\b")
_FIHRIST = re.compile(r"(^|/)fihrist(/|$)")
_BOOK_NAMES = re.compile(r"[İi]ş[âa]r[âa]t[\s\-‑]*ı[\s\-‑]*Kur'?[âa]niye|[İi]ş[âa]r[âa]t[üu]'?l[\s\-‑]*[İi]'?c[âa]z", re.I)
_SURA_BEFORE = re.compile(r"S[ûu]re[\s\-‑]*[iî]\W{0,3}$", re.I)       # "Sûre‑i وَالتّ۪ينِ"
_SURA_AFTER = re.compile(r"^\W{0,3}S[ûu]res", re.I)                     # "اِقْرَأْ بِاسْمِ رَبِّكَ Sûresi’nde"
_CIFIR = re.compile(r"cifir|cifr[îi]|ebced|makam[ıi]yla", re.I)
_LATIN_WORD = re.compile(r"[^\W\d_]*[A-Za-zÇĞİÖŞÜçğıöşüâîûÂÎÛ][^\W\d_]*")
HEAD_WORDS = 3                  # âyet cümlenin başında: önünde en çok bu kadar Türkçe kelime ("İkinci Cümle:")
CUE_WORDS = 8                   # "işâret" gibi kelime ile âyet arasında en çok bu kadar Türkçe kelime
LETTER_WORKS = frozenset({"mektubat", "barla-lahikasi", "kastamonu-lahikasi", "emirdag-lahikasi", "tarihce-i-hayat"})
LETTER_OPENING = (17, 44)       # "وَاِنْ مِنْ شَيْءٍ اِلَّا يُسَبِّحُ بِحَمْدِه۪": mektupların açılış ibaresi
RISALE_SECTIONS = ("sualar/1",)  # Birinci Şuâ: âyetlerin Risale-i Nur'a işâretleri


@dataclass
class Link:
    kind: str
    strength: str            # strong | weak
    sura: int
    ayah_start: int
    ayah_end: int
    node_id: str
    scope: str               # section | sentence
    evidence_id: str         # kanıt cümlesi


def _about_risale(node_id: str, node_ref: str) -> bool:
    if any(node_id == s or node_id.startswith(s + "/") for s in RISALE_SECTIONS):
        return True
    words = " ".join(search_words(node_ref))
    return "isaret" in words and any(w in words for w in ("risale i nur", "risaletun nur"))


def _cue_distance(text: str, cue: re.Pattern, start: int, end: int) -> tuple[int] | None:
    """Kanıt kelimesinin âyete en yakın geçişi: arada kaç Türkçe kelime var (Arapça sayılmaz)."""
    distances = []
    for m in cue.finditer(text):
        between = text[m.end():start] if m.end() <= start else text[end:m.start()] if m.start() >= end else ""
        distances.append(len(_LATIN_WORD.findall(between)))
    return (min(distances),) if distances else None


def _letter_opening(r: sqlite3.Row) -> bool:
    """Mektubun yalnızca "وَاِنْ مِنْ شَيْءٍ اِلَّا يُسَبِّحُ بِحَمْدِه۪" (önünde Besmele ya da "بِاسْمِه۪ سُبْحَانَهُ")
    ile açılması: açılış ibaresidir."""
    if r["work"] not in LETTER_WORKS or (r["sura"], r["ayah_start"]) != LETTER_OPENING:
        return False
    rest = skeleton(r["ptext"])
    for prefix in (skeleton("بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّح۪يمِ"), skeleton("بِاسْمِه۪ سُبْحَانَهُ")):
        rest = rest.removeprefix(prefix)
    return rest == skeleton("وَاِنْ مِنْ شَيْءٍ اِلَّا يُسَبِّحُ بِحَمْدِه۪")


def _quotes(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    """Hizb ve mecmua dışındaki bütün âyet alıntıları, cümleleri ve bölümleriyle."""
    return conn.execute("""
        SELECT q.sura, q.ayah_start, q.ayah_end, q.span_start, q.span_end, p.text AS ptext,
               s.id AS sid, s.n, s.hasiye, s.text, s.span_start AS s_start, s.span_end AS s_end,
               n.id AS node_id, n.ref AS node_ref
        FROM (SELECT sentence_id, paragraph_id, sura, ayah_start, ayah_end, span_start, span_end
              FROM arabic WHERE sura IS NOT NULL AND sentence_id IS NOT NULL
              UNION ALL SELECT sentence_id, paragraph_id, sura, ayah_start, ayah_end, span_start, span_end
              FROM ayah_quotes WHERE sentence_id IS NOT NULL) q
        JOIN sentences s ON s.id = q.sentence_id JOIN paragraphs p ON p.id = q.paragraph_id
        JOIN nodes n ON n.id = s.node_id JOIN works w ON w.slug = n.work
        WHERE w.group_name NOT IN ('hizb', 'mecmua') ORDER BY s.seq""").fetchall()


def find_links(conn: sqlite3.Connection) -> list[Link]:
    """Veritabanındaki âyet alıntılarından ilişkiler (bağlantının `row_factory`'si `sqlite3.Row` olmalı)."""
    out: list[Link] = []
    seen: set[tuple] = set()

    def add(kind: str, q, scope: str, evidence: str) -> None:
        if _FIHRIST.search(q["node_id"]):
            return
        if kind in ("isaret", "dayanak") and _about_risale(q["node_id"], q["node_ref"]):
            kind = "risale"
        key = (q["sura"], q["ayah_start"], q["node_id"] if scope == "section" else evidence)
        if key in seen:                      # aynı yer için ilk bulunan kalır: metnin söylediği açılıştan önce
            return
        seen.add(key)
        strong = scope == "section" or kind == "izah"
        out.append(Link(kind, "strong" if strong else "weak", q["sura"], q["ayah_start"], q["ayah_end"],
                        q["node_id"], scope, evidence))

    following: dict[str, sqlite3.Row | None] = {}
    for q in _quotes(conn):
        if (q["sura"], q["ayah_start"]) == BESMELE:
            continue
        text = _BOOK_NAMES.sub(lambda m: " " * len(m[0]), q["text"])     # risale adları kanıt değil
        start, end = q["span_start"] - q["s_start"], q["span_end"] - q["s_start"]   # âyetin cümledeki yeri
        opening = q["n"] <= OPENING_SENTENCES and not q["hasiye"]
        at_head = len(_LATIN_WORD.findall(text[:start])) <= HEAD_WORDS
        incidental = (_SURA_BEFORE.search(text[:start]) or _SURA_AFTER.match(text[end:])
                      or (_CIFIR.search(text) and not at_head))
        for kind, cue in (("isaret", _ISARET), ("dayanak", _DAYANAK)):
            if near := _cue_distance(text, cue, start, end):
                close = near[0] <= CUE_WORDS or at_head          # cümlenin başındaki âyet cümlenin öznesidir
                add(kind, q, "section" if opening and close and not incidental else "sentence", q["sid"])
                break
        # izah: âyetten hemen sonra "Yani", ya da âyet cümleyi bitiriyorsa sonraki cümlenin başında
        if _YANI.match(q["ptext"][q["span_end"]:]):
            add("izah", q, "sentence", q["sid"])
        elif not q["ptext"][q["span_end"]:q["s_end"]].strip(" .:;,…"):
            if q["sid"] not in following:
                following[q["sid"]] = conn.execute(
                    "SELECT id, text FROM sentences WHERE node_id = ? AND n = ? AND hasiye = ?",
                    (q["node_id"], q["n"] + 1, q["hasiye"])).fetchone()
            if (nxt := following[q["sid"]]) and _YANI.match(nxt["text"]):
                add("izah", q, "sentence", nxt["id"])

    # açılış: bölümün ilk paragrafı âyet olan Arapça paragraf
    for r in conn.execute("""
            SELECT n.id AS node_id, n.ref AS node_ref, n.work, a.sura, a.ayah_start, a.ayah_end, s.id AS sid,
                   p.text AS ptext
            FROM nodes n JOIN works w ON w.slug = n.work
            JOIN paragraphs p ON p.node_id = n.id AND p.kind = 'arabic' AND p.ord =
                 (SELECT min(ord) FROM paragraphs WHERE node_id = n.id AND kind != 'hasiye')
            JOIN (SELECT paragraph_id, sura, ayah_start, ayah_end FROM arabic WHERE sura IS NOT NULL
                  UNION ALL SELECT paragraph_id, sura, ayah_start, ayah_end FROM ayah_quotes) a
                 ON a.paragraph_id = p.id
            JOIN sentences s ON s.paragraph_id = p.id AND s.n = 1
            WHERE w.group_name NOT IN ('hizb', 'mecmua') ORDER BY n.seq"""):
        if (r["sura"], r["ayah_start"]) == BESMELE or _letter_opening(r):
            continue
        add("risale" if _about_risale(r["node_id"], r["node_ref"]) else "acilis", r, "section", r["sid"])
    _arabic_openings(conn, add)
    return out


def _arabic_openings(conn: sqlite3.Connection, add) -> None:
    """Arapça eserin (İşaratü'l-İ'caz) âyet bölümleri işledikleri âyetle açılır; kanıt bölümün ilk cümlesidir."""
    rows = conn.execute("""
        SELECT n.id AS node_id, n.ref AS node_ref, n.title, n.parent_id, n.work, n.ord, n.last_ord
        FROM nodes n JOIN works w ON w.slug = n.work
        WHERE w.language = 'ar' AND w.group_name NOT IN ('hizb', 'mecmua') ORDER BY n.seq""").fetchall()
    context = verse_context([{"id": r["node_id"], "parent_id": r["parent_id"], "title": r["title"]} for r in rows])
    for r in rows:
        first = conn.execute(
            "SELECT s.id FROM sentences s JOIN nodes n ON n.id = s.node_id WHERE n.work = ? AND n.ord BETWEEN ? AND ?"
            " AND s.hasiye = 0 ORDER BY s.seq LIMIT 1", (r["work"], r["ord"], r["last_ord"])).fetchone()
        if first is None:
            continue
        parent = (r["parent_id"] or "").rsplit("/", 1)[-1]
        if parent in ("sure-i-bakara", "sure-i-fatiha") and r["node_id"] in context:
            sura, start, end = context[r["node_id"]]
            add("acilis", {"sura": sura, "ayah_start": start, "ayah_end": end, "node_id": r["node_id"],
                           "node_ref": r["node_ref"]}, "section", first["id"])


# ---------------------------------------------------------------- elle gözden geçirme

def load_reviews(path: Path = REVIEWS) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["reviews"] if path.exists() else []


def review_status(conn: sqlite3.Connection, review: dict) -> str | None:
    """Kullanıcının kararındaki yerin bugünkü gücü: strong, weak ya da None (ilişki yok)."""
    row = conn.execute(
        "SELECT strength FROM ayah_links WHERE sura = ? AND ? BETWEEN ayah_start AND ayah_end AND node_id LIKE ?"
        " ORDER BY strength = 'weak' LIMIT 1", (review["sura"], review["ayah"], review["node"] + "%")).fetchone()
    return row[0] if row else None


def _rows(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute("""
        SELECT l.*, n.ref AS node_ref, s.ref AS evidence_ref, s.text AS evidence, q.name AS sura_name,
               (SELECT substr(p.text, a.span_start + 1, a.span_end - a.span_start)
                FROM (SELECT paragraph_id, sentence_id, sura, ayah_start, span_start, span_end FROM arabic
                      UNION ALL SELECT paragraph_id, sentence_id, sura, ayah_start, span_start, span_end
                      FROM ayah_quotes) a JOIN paragraphs p ON p.id = a.paragraph_id
                JOIN sentences e ON e.id = a.sentence_id
                WHERE e.node_id = l.node_id AND a.sura = l.sura AND a.ayah_start = l.ayah_start LIMIT 1) AS verse
        FROM ayah_links l JOIN nodes n ON n.id = l.node_id JOIN sentences s ON s.id = l.evidence_id
        LEFT JOIN quran_suras q ON q.number = l.sura ORDER BY l.kind, l.strength, n.seq""").fetchall()


def _cell(text: str | None, limit: int = 200) -> str:
    text = (text or "").replace("|", "/").replace("\n", " ")
    return text if len(text) <= limit else text[:limit].rsplit(" ", 1)[0] + " …"


def _table(rows: list[sqlite3.Row], numbered: bool = False) -> list[str]:
    columns = ["Tür", "Âyet", "Âyetin eserdeki metni", "Bölüm", "Bölüm kimliği", "Kapsam", "Kanıt cümlesi"]
    columns = (["#"] if numbered else []) + columns
    lines = ["| " + " | ".join(columns) + " |", "|" + "---|" * len(columns)]
    for i, r in enumerate(rows, 1):
        ayah = f"{r['sura_name'] or r['sura']} {r['sura']}:{r['ayah_start']}" + (
            f"-{r['ayah_end']}" if r["ayah_end"] != r["ayah_start"] else "")
        cells = [r["kind"], ayah, _cell(r["verse"], 120), r["node_ref"], f"`{r['node_id']}`", r["scope"],
                 _cell(r["evidence"])]
        lines.append("| " + " | ".join(([str(i)] if numbered else []) + cells) + " |")
    return lines


def write_reports(conn: sqlite3.Connection, round_: int) -> Counter:
    rows = _rows(conn)
    counts = Counter((r["kind"], r["strength"]) for r in rows)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    lines = ["# Âyet ilişkileri", "", "`build_db` kurar, `uv run python -m risale_mcp.ayah_links` yazar. "
             "Türler ve kurallar `ayah_links.py` başında.", ""]
    for kind in KINDS:
        for strength in ("strong", "weak"):
            group = [r for r in rows if r["kind"] == kind and r["strength"] == strength]
            if group:
                lines += [f"## {kind} — {strength} ({len(group)})", "", *_table(group), ""]
    (OUT_DIR / "links.md").write_text("\n".join(lines), encoding="utf-8")

    reviews = load_reviews()
    reviewed = {(r["sura"], r["ayah"], r["node"]) for r in reviews}
    strong = [r for r in rows if r["strength"] == "strong"
              and not any(r["sura"] == s and r["ayah_start"] <= a <= r["ayah_end"] and r["node_id"].startswith(n)
                          for s, a, n in reviewed)]
    sample = sorted(random.Random(SAMPLE_SEED + round_).sample(strong, min(SAMPLE_SIZE, len(strong))),
                    key=lambda r: (r["kind"], r["node_ref"]))
    (OUT_DIR / f"sample-{round_}.md").write_text("\n".join([
        f"# Güçlü ilişkilerden örneklem ({round_}. tur)", "",
        f"Daha önce gözden geçirilmemiş güçlü ilişkilerden rastgele {len(sample)} tanesi. Her satır için: ilişki",
        "doğru mu (✓), yanlış mı (✗), türü ya da kapsamı mı yanlış? Numarasıyla bildirin.", "",
        *_table(sample, numbered=True), ""]), encoding="utf-8")
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--round", type=int, default=1 + max((r["round"] for r in load_reviews()), default=0),
                        help="örneklem turu (varsayılan: gözden geçirilmiş son turun bir sonrası)")
    args = parser.parse_args()
    conn = connect()
    counts = write_reports(conn, args.round)
    for kind in KINDS:
        print(f"  {kind:8} güçlü {counts[(kind, 'strong')]:4}, zayıf {counts[(kind, 'weak')]:4}")
    reviews = load_reviews()
    agree = sum((review_status(conn, r) == "strong") == (r["expect"] == "strong") for r in reviews)
    print(f"  kullanıcı kararlarıyla uyum: {agree}/{len(reviews)}")
    print(f"  yazıldı: {(OUT_DIR / 'links.md').relative_to(ROOT)}, {(OUT_DIR / f'sample-{args.round}.md').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
