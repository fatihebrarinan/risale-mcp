"""Hadisçi örneklemi ve kararların kilitlenmesi (`docs/hadis-plani.md`, Adım 8).

    uv run python -m risale_mcp.hadis_ornek prepare            # data/interim/hadis/ornek/hadis-orneklemi.xlsx, key.json
    uv run python -m risale_mcp.hadis_ornek collect <dosya>    # kararlar -> tests/golden/hadis_review.json, ornek/karsilastirma.md

Kitap gözden geçirene model kararlarını, seviyeleri, tabakaları göstermez (`key.json` ayrıdır, gönderilmez); kitabı
dolduran bilgilendirilir ki bazı satırlar kontroldür, hangileri olduğu söylenmez. Öncelik 1 tabakalı 40 satırdır,
40'ta hata çıkmasa bile gerçek oran ≈%7'ye kadar olabilir. Kilitlenen kararlar hadisçinindir, hüküm dosyası değildir:
`hadith_support`'u kendiliğinden değiştirmez. openpyxl geliştirme bağımlılığıdır, sunucuya gitmez.
"""

import json
import random
import sys
from collections import Counter
from pathlib import Path

from risale_mcp.db import connect
from risale_mcp.hadis import read_reports
from risale_mcp.hadis_okuma import SAME, window
from risale_mcp.paths import DB_PATH, INTERIM_DIR, RAW_DIR, ROOT

OUT = INTERIM_DIR / "hadis" / "ornek"
GOLDEN = ROOT / "tests" / "golden" / "hadis_review.json"
BOOK = "hadis-orneklemi.xlsx"
# Tabaka: öncelik 1'e giren sayı; kalanlar öncelik 2.
STRATA = {"by_meaning": 10, "other_speaker": 8, "denied": 4, "rejected": 3, "located": 6, "verbatim": 3, "decoy": 4, "trap": 2}
LIMITS = {"located": 12, "verbatim": 8, "decoy": 6, "disputed": 6}
RELATIONS = ("Aynı lafız", "Kısaltılmış", "Mânen nakil", "İlgili, aynı söz değil", "Farklı", "Karar veremedim")
SPEAKERS = ("Peygamber", "Sahâbî", "Başka biri", "Belirsiz")
MODEL_SAME = {"Aynı lafız": "verbatim", "Kısaltılmış": "abridged", "Mânen nakil": "by_meaning"}
# Adım 4 denemesi: Türkçe söz, modelin bulduğu rivayet. Metindeki ibare ve rivayet kimliği.
TRAPS = (("iki yüz defa daha", "tirmidhi:2590"), ("Size ders vermek için", "sanadset:255137"), ("Dünya Âhiret mezraasıdır", "sanadset:225925"))
HEADERS = ("No", "Öncelik", "Risale'deki yer", "Risale'deki söz", "Nâşir meali", "Künye", "Derlemdeki rivayet (eşleşen yer ve çevresi)",
           "Kitap", "Rivayet kimliği", "Senet halkası", "İlişki", "Söz sahibi", "Sıhhat bilgisi", "Not")
WIDTHS = (6, 8, 34, 40, 34, 30, 70, 24, 18, 8, 18, 14, 24, 34)


def strata(rows: list[dict]) -> dict[str, list[dict]]:
    """Okuma satırlarından tabakalar; bir çift ilk uyduğu tabakada kalır."""
    real = [r for r in rows if not r["decoy"]]
    both = lambda r, test: all(test(a) for a in r["answers"])
    groups = {
        "denied": [r for r in real if both(r, lambda a: a["denied"])],
        "other_speaker": [r for r in real if both(r, lambda a: a["relation"] in SAME and a["speaker"] == "other")],
        "rejected": [r for r in real if both(r, lambda a: a["relation"] not in SAME)],
        "by_meaning": [r for r in real if both(r, lambda a: a["relation"] == "by_meaning")],
        "disputed": [r for r in real if not r["agree"]],
        "verbatim": [r for r in real if r["set"] == "found" and both(r, lambda a: a["relation"] == "verbatim" and a["speaker"] == "prophet")],
        "decoy": [r for r in rows if r["decoy"]]}
    seen, out = set(), {}
    for name, members in groups.items():
        out[name] = [r for r in members if r["id"] not in seen]
        seen |= {r["id"] for r in out[name]}
    return out


def passage(conn, key: str) -> dict:
    row = conn.execute("SELECT s.ref, a.meal, a.source FROM arabic a JOIN sentences s ON s.id = a.sentence_id"
                       " JOIN works w ON w.slug = s.work WHERE a.hadith_key = ? AND w.language != 'os'"
                       " ORDER BY a.source IS NULL, s.seq LIMIT 1", (key,)).fetchone()
    return dict(row) if row else {"ref": None, "meal": None, "source": None}


def located_rows(conn) -> list[dict]:
    rows = conn.execute("SELECT a.hadith_key AS key, a.source, s.ref, a.meal, l.report_id AS report, r.title,"
                        " substr(p.text, a.span_start + 1, a.span_end - a.span_start) AS part FROM hadith_located l"
                        " JOIN arabic a ON a.paragraph_id = l.paragraph_id AND a.ord = l.ord"
                        " JOIN paragraphs p ON p.id = a.paragraph_id JOIN sentences s ON s.id = a.sentence_id"
                        " JOIN works w ON w.slug = s.work JOIN hadith_reports r ON r.id = l.report_id"
                        " WHERE l.rank = 0 AND w.language != 'os'").fetchall()
    return list({r["key"]: dict(r) for r in rows}.values())


def choose(db: Path = DB_PATH, seed: int = 14) -> list[dict]:
    conn, rng = connect(db), random.Random(seed)
    read = json.loads((INTERIM_DIR / "hadis" / "okuma.json").read_text("utf-8"))["rows"]
    groups = strata(read)
    items = []
    for name, members in groups.items():
        members = sorted(members, key=lambda r: r["id"])
        rng.shuffle(members)
        for r in members[:LIMITS.get(name)]:
            items.append({"stratum": name, "key": r["key"], "part": r["part"], "report": r["report"], "title": r["title"],
                          "model": [a["relation"] for a in r["answers"]], "speaker": [a["speaker"] for a in r["answers"]], **passage(conn, r["key"])})
    located = sorted(located_rows(conn), key=lambda r: r["key"])
    rng.shuffle(located)
    items += [{"stratum": "located", "model": [], "speaker": [], **r} for r in located[:LIMITS["located"]]]
    for phrase, report in TRAPS:
        found = conn.execute("SELECT s.text, s.ref FROM sentences s JOIN works w ON w.slug = s.work WHERE w.language = 'tr'"
                             " AND s.text LIKE ? ORDER BY s.seq LIMIT 1", (f"%{phrase}%",)).fetchone()
        if found is None:
            raise ValueError(f"tuzak cümlesi bulunamadı: {phrase}")
        items.append({"stratum": "trap", "key": None, "part": found["text"], "report": report, "title": None, "model": [], "speaker": [],
                      "ref": found["ref"], "meal": None, "source": None})
    picked = Counter()
    for item in items:
        picked[item["stratum"]] += 1
        item["priority"] = 1 if picked[item["stratum"]] <= STRATA.get(item["stratum"], 0) else 2
    rng.shuffle(items)
    items.sort(key=lambda i: i["priority"])
    for n, item in enumerate(items, 1):
        item["no"] = n
    return items


def workbook(items: list[dict], reports: dict) -> "openpyxl.Workbook":
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.datavalidation import DataValidation
    from openpyxl.worksheet.properties import PageSetupProperties
    font, bold = Font(name="Arial", size=11), Font(name="Arial", size=11, bold=True)
    fill, head = PatternFill("solid", fgColor="FFF7CC"), PatternFill("solid", fgColor="E7E6E6")
    thin = Side(style="thin", color="BFBFBF")
    book = Workbook()
    guide = book.active
    guide.title = "Nasıl doldurulur"
    guide.column_dimensions["A"].width = 26
    guide.column_dimensions["B"].width = 90
    text = [("Risale-i Nur hadis örneklemi", ""),
            ("Amaç", "Risale-i Nur'daki hadislerin rivayetlerle yapılan eşleşmelerini ehlinin gözüyle sınamak. Hiçbir hüküm önceden verilmedi; "
                     "eşleşmeler bir kelime aramasının ve model okumasının sonucudur, doğrulanmamıştır."),
            ("Ne dolduracaksınız", "'Örneklem' sayfasında yalnız sarı sütunlar: İlişki, Söz sahibi, Sıhhat bilgisi, Not. Öteki sütunlara dokunmayın."),
            ("Öncelik", "Öncelik 1 satırları (40) esastır. Vaktiniz olursa Öncelik 2 satırlarına devam edin. Boş satır, karar verilmemiş sayılır."),
            ("İlişki", "Aynı lafız: söz rivayette aynen var. Kısaltılmış: aynı söz, bir kısmı atılmış. Mânen nakil: başka kelimelerle aynı söz. "
                       "İlgili, aynı söz değil: aynı konu, başka söz. Farklı: ilgisiz. Karar veremedim: bu satırda bilgi yetmiyor."),
            ("Söz sahibi", "Gösterilen rivayette bu sözü kim söylüyor: Peygamber, Sahâbî, Başka biri, Belirsiz."),
            ("Sıhhat bilgisi", "İsteğe bağlı, serbest metin. Bildiğiniz bir hüküm varsa âlimiyle yazın (ör. 'Tirmizî: hasen'). Bilmiyorsanız boş bırakın."),
            ("Kontrol satırları", "Bazı satırlar kontrol amacıyla bilerek eklenmiştir; söz ile rivayet birbirini tutmayabilir. Hangileri olduğu burada söylenmez."),
            ("Meal", "Nâşir meali Bediüzzaman'ın değil, sonradan nâşirlerin tercümesidir; yalnız anlamı kolay takip etmek içindir."),
            ("Örnek satır (biçim için)", "İlişki: Mânen nakil | Söz sahibi: Peygamber | Sıhhat bilgisi: Tirmizî: hasen | Not: Rivayette 'iman' geçiyor, söz aynı. "
                                         "Bu yalnız yazım örneğidir, gerçek bir karar değildir."),
            ("Kaynak", "Rivayetler: Sanadset 650K (CC BY 4.0) ve Hadith API (Unlicense). Metinleri baskısından teyit edilmemiştir.")]
    for i, (a, b) in enumerate(text, 1):
        guide.cell(i, 1, a).font = bold
        guide.cell(i, 2, b).font = font
        guide.cell(i, 2).alignment = Alignment(wrap_text=True, vertical="top")
        guide.cell(i, 1).alignment = Alignment(vertical="top", wrap_text=True)
        guide.row_dimensions[i].height = 16 * max(1, 1 + len(b) // 85)
    sheet = book.create_sheet("Örneklem")
    for c, (title, width) in enumerate(zip(HEADERS, WIDTHS), 1):
        cell = sheet.cell(1, c, title)
        cell.font, cell.fill = bold, fill if c >= 11 else head
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        sheet.column_dimensions[get_column_letter(c)].width = width
    sheet.freeze_panes = "C2"
    for i, item in enumerate(items, 2):
        r = reports[item["report"]]
        title = r[0]
        values = (item["no"], item["priority"], item["ref"], item["part"], item["meal"], item["source"], item["shown"], title, item["report"], item["chain"])
        for c, value in enumerate(values, 1):
            cell = sheet.cell(i, c, value)
            cell.font = font
            arabic = c == 7 or (c == 4 and item["stratum"] != "trap")
            cell.alignment = Alignment(wrap_text=True, vertical="top", horizontal="right" if arabic else None, readingOrder=2 if arabic else 0)
        for c in range(11, 15):
            cell = sheet.cell(i, c)
            cell.fill, cell.font = fill, font
            cell.alignment = Alignment(wrap_text=True, vertical="top")
        for c in range(1, 15):
            sheet.cell(i, c).border = Border(bottom=thin)
        lines = max(1 + len(str(v or "")) * 3 // (WIDTHS[c] * 2) for c, v in enumerate(values))
        sheet.row_dimensions[i].height = min(400, 16 * lines)
    last = len(items) + 1
    for column, options in (("K", RELATIONS), ("L", SPEAKERS)):
        rule = DataValidation(type="list", formula1='"' + ",".join(options) + '"', allow_blank=True, showErrorMessage=True,
                              errorTitle="Liste", error="Listeden seçiniz.")
        rule.add(f"{column}2:{column}{last}")
        sheet.add_data_validation(rule)
    sheet.auto_filter.ref = f"A1:N{last}"
    sheet.page_setup.orientation, sheet.page_setup.fitToWidth, sheet.page_setup.fitToHeight = "landscape", 1, 0
    sheet.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
    sheet.print_title_rows = "1:1"
    guide.page_setup.fitToWidth, guide.page_setup.fitToHeight = 1, 0
    guide.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
    book.active = 1
    return book


def prepare(db: Path = DB_PATH, raw: Path = RAW_DIR, out: Path = OUT) -> Counter:
    from risale_mcp.hadis_rivayet import _chain, chains
    items = choose(db)
    wanted = {i["report"] for i in items}
    reports = {r.id: (r.title, r.text) for r in read_reports(raw) if r.id in wanted}
    known = chains({int(r.split(":")[1]) for r in wanted if r.startswith("sanadset:")}, raw)
    for item in items:
        item["shown"] = window(item["part"], reports[item["report"]][1]) if item["stratum"] != "trap" else reports[item["report"]][1][:900]
        item["chain"] = _chain(item["report"], known)
    out.mkdir(parents=True, exist_ok=True)
    workbook(items, reports).save(out / BOOK)
    (out / "key.json").write_text(json.dumps(items, ensure_ascii=False, indent=0), "utf-8")
    return Counter((i["stratum"], i["priority"]) for i in items)


def read_book(path: Path) -> list[dict]:
    from openpyxl import load_workbook
    sheet = load_workbook(path)["Örneklem"]
    decisions = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        relation, speaker, grade, note = row[10:14]
        if relation or speaker or grade or note:
            decisions.append({"no": row[0], "report": row[8], "relation": relation, "speaker": speaker, "grade": grade, "note": note})
    return decisions


def compare(items: list[dict], decisions: list[dict]) -> tuple[list[dict], list[str]]:
    by_no = {i["no"]: i for i in items}
    locked, tally = [], Counter()
    for d in decisions:
        item = by_no[d["no"]]
        if item["report"] != d["report"]:
            raise ValueError(f"{d['no']}. satırın rivayeti anahtarla tutmuyor: dosya başka bir örneklemin olabilir")
        locked.append({**d, "stratum": item["stratum"], "key": item["key"], "model": item["model"]})
        tally[item["stratum"], "karar"] += 1
        tally[item["stratum"], "aynı söz"] += d["relation"] in MODEL_SAME
        tally[item["stratum"], "model ile aynı tür"] += MODEL_SAME.get(d["relation"]) in item["model"]
    lines = ["# Hadisçi kararları ve model okuması\n", "| tabaka | karar | aynı söz | model ile aynı tür |", "|---|---|---|---|"]
    for name in sorted({s for s, _ in tally}):
        lines.append(f"| {name} | {tally[name, 'karar']} | {tally[name, 'aynı söz']} | {tally[name, 'model ile aynı tür']} |")
    return locked, lines


def collect(path: Path, out: Path = OUT, golden: Path = GOLDEN) -> list[str]:
    items = json.loads((out / "key.json").read_text("utf-8"))
    locked, lines = compare(items, read_book(path))
    golden.write_text(json.dumps({"note": "Hadisçinin kararları; hüküm dosyası değildir.", "decisions": locked}, ensure_ascii=False, indent=0), "utf-8")
    (out / "karsilastirma.md").write_text("\n".join(lines) + "\n", "utf-8")
    return lines


def main() -> None:
    if sys.argv[1:2] == ["prepare"]:
        print(sorted(prepare().items()))
    else:
        print("\n".join(collect(Path(sys.argv[2]))))


if __name__ == "__main__":
    main()
