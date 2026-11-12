"""PLANLAR.md'nin düzeni: "Sıradaki"de yalnız tablodaki işlerin ayrıntısı durur, biten iş oradan çıkar.

Kural belgenin başındadır (kullanıcının isteği, 2026-11-12: S1 ve S2 bittikten sonra ayrıntıları "Sıradaki"de
kalmıştı).
"""

import re
from pathlib import Path

PLANS = Path(__file__).resolve().parents[1] / "PLANLAR.md"
LETTERS = "ESADB"
ID = rf"[{LETTERS}]\d+"


def sections() -> dict[str, str]:
    text = PLANS.read_text(encoding="utf-8")
    parts = re.split(r"^## (.+)$", text, flags=re.M)
    return {parts[i].strip(): parts[i + 1] for i in range(1, len(parts), 2)}


def _expand(cell: str) -> set[str]:
    m = re.fullmatch(rf"([{LETTERS}])(\d+)\s*[–-]\s*[{LETTERS}]?(\d+)", cell.strip())
    if m:
        return {f"{m[1]}{n}" for n in range(int(m[2]), int(m[3]) + 1)}
    return set(re.findall(ID, cell))


def table_ids(body: str) -> set[str]:
    ids: set[str] = set()
    for line in body.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("|") and len(cells) >= 2 and re.match(ID, cells[1]):
            ids |= _expand(cells[1])
    return ids


def detail_ids(body: str) -> set[str]:
    """Ayrıntı başlıkları: `**D1. …**` ve `- D1.3 …` / `- B2 …` satırları (üst kimliğe indirilir)."""
    found = re.findall(rf"^\*\*({ID})\.", body, flags=re.M)
    found += re.findall(rf"^- ({ID})(?:\.\d+[a-z]?)?\s", body, flags=re.M)
    return set(found)


def test_next_details_are_in_table():
    s = sections()
    body = s["Sıradaki"]
    missing = detail_ids(body) - table_ids(body)
    assert not missing, f"'Sıradaki'de ayrıntısı olup tabloda olmayan işler (bittiyse Kayıt'a taşı): {sorted(missing)}"


def test_finished_not_in_next():
    s = sections()
    finished = set(re.findall(rf"^- ({ID})\s", s["Biten (özet)"], flags=re.M))
    nxt = s["Sıradaki"]
    both = finished & (table_ids(nxt) | detail_ids(nxt))
    assert not both, f"hem 'Biten'de hem 'Sıradaki'de: {sorted(both)}"


def test_ids_within_last_given():
    s = sections()
    m = re.search(r"Son verilen kimlikler: ([^(\n]+)", s["Adlandırma (kullanıcının kararı, 2026-11-09)"])
    last = {i[0]: int(i[1:]) for i in re.findall(ID, m[1])}
    assert set(last) == set(LETTERS)
    plan_sections = [k for k in s if not k.startswith(("Kayıt", "Ortak derlemler", "Adlandırma"))]
    used = {i for k in plan_sections for i in re.findall(rf"(?<![\w.]){ID}(?![\d])", s[k])}
    over = sorted(i for i in used if int(i[1:]) > last[i[0]])
    assert not over, f"'Son verilen kimlikler'i aşan kimlikler (satırı güncelle): {over}"
