"""Bağlar: Risale'nin âyetlerle, hadislerle ve kendi içinde kurduğu bağların ortak kaydı (`docs/bag-altyapisi-plani.md`).

    uv run python -m risale_mcp.links check [--db yol]     # data/links/**/*.jsonl'yi veritabanına karşı denetler

Bir satır bir bağdır (JSON Lines); dosyanın ilk satırı üst bilgidir (`{"meta": {...}}`). Dosyalar
`data/links/<alan>/<yöntem>.jsonl`; bağı üreten iş yazar, her profilin `build_db`'si okur. Hadis sunucusu (HA5) Risale
veritabanı olmadan da okuyabilsin diye kaynağın atfı `display`'de durur.

Alanlar:

    source    Risale'de bağın ucu: cümle kimliği; bölüm kapsamlı bağda düğüm kimliği (`scope: section`)
    part      cümlede birden çok Arapça parça varsa hangisi: parçanın iskelet anahtarı (`quran.skeleton`; hadiste
              `arabic.hadith_key` ile aynı). Sıra numarası değil: yeniden ayrıştırmada kaymasın
    target    ad alanlı kimlik: quran:2:255, quran:2:255-257, hadis:bukhari/52, hadis-derlem:sanadset:220501
              (kütüphanede henüz olmayan rivayet), risale:lemalar/30
    type      quote (söz aktarılıyor), relation (âyetle bağ), reference (başka yere gönderme)
    relation  alıntıda lafız ilişkisi (verbatim, abridged, by_meaning, phrase); ilişkide türü (isaret, acilis, izah,
              dayanak, risale); göndermede `old_name`
    method    bağı kuran: source_mark, quran_text, corpus, cited_chapter, reading, rule, curated (ileride scholar)
    strength  strong | weak
    evidence  yönteme göre serbest (kanıt cümlesi, künye, okuyucu cevapları, puan)
    display   kaynağın gösterilecek atfı (`cite_as`); doğrulamada kimlik kaymasını yakalar

Doğrulama (`check`): kaynak cümle ya da düğüm var mı, `part` o cümlenin Arapça parçalarından biri mi, `display`
kaynağın bugünkü atfıyla tutuyor mu, hedef biçimi geçerli mi. Tutmayan bağ yüklenmez, raporlanır.
"""

import json
import re
import sqlite3
import sys
from collections import Counter
from collections.abc import Iterable
from dataclasses import asdict, dataclass, field
from pathlib import Path

from risale_mcp.paths import DB_PATH, LINKS_DIR
from risale_mcp.quran import skeleton

TYPES = ("quote", "relation", "reference")
METHODS = ("source_mark", "quran_text", "corpus", "cited_chapter", "reading", "rule", "curated", "scholar")
STRENGTHS = ("strong", "weak")
SCOPES = ("sentence", "section")
_TARGET = re.compile(r"^(?:quran:(\d{1,3}):(\d{1,3})(?:-(\d{1,3}))?|hadis:[a-z0-9-]+/[0-9]+(?:-\d+)?"
                     r"|hadis-derlem:[a-z_]+:[0-9]+|risale:[a-z0-9/._-]+)$")


@dataclass(frozen=True)
class Link:
    source: str
    target: str
    type: str
    method: str
    strength: str = "strong"
    relation: str | None = None
    part: str | None = None
    scope: str = "sentence"
    evidence: dict = field(default_factory=dict, hash=False, compare=False)
    display: str | None = field(default=None, hash=False, compare=False)

    def problems(self) -> list[str]:
        """Kaydın kendi içindeki hatalar (veritabanına bakmadan)."""
        out = []
        if self.type not in TYPES:
            out.append(f"type {self.type!r}")
        if self.method not in METHODS:
            out.append(f"method {self.method!r}")
        if self.strength not in STRENGTHS:
            out.append(f"strength {self.strength!r}")
        if self.scope not in SCOPES:
            out.append(f"scope {self.scope!r}")
        if not (m := _TARGET.match(self.target)):
            out.append(f"target {self.target!r}")
        elif self.target.startswith("quran:") and not (1 <= int(m[1]) <= 114 and (m[3] is None or int(m[3]) >= int(m[2]))):
            out.append(f"target {self.target!r}")
        return out

    def to_json(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v not in (None, {}, "") and not (k == "scope" and v == "sentence")}


def part_key(text: str) -> str:
    """Arapça parçanın bağdaki anahtarı: iskelet (hadiste `arabic.hadith_key` ile aynı)."""
    return skeleton(text)


def write(path: Path, links: Iterable[Link], **meta) -> int:
    """Üst bilgi ve kitap sırasıyla değil, (kaynak, hedef) sırasıyla bağlar: dosya farkı okunur kalsın."""
    rows = sorted({(l.source, l.target, l.part or "", l.type, l.method): l for l in links}.values(),
                  key=lambda l: (l.source, l.part or "", l.target, l.method))
    bad = [(l, p) for l in rows if (p := l.problems())]
    if bad:
        raise ValueError(f"{path.name}: geçersiz bağ {bad[0][1]}: {bad[0][0]}")
    lines = [json.dumps({"meta": {**meta, "count": len(rows)}}, ensure_ascii=False)]
    lines += [json.dumps(l.to_json(), ensure_ascii=False) for l in rows]
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text("\n".join(lines) + "\n", encoding="utf-8")
    tmp.replace(path)
    return len(rows)


def read(path: Path) -> tuple[dict, list[Link]]:
    meta, links = {}, []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
        if not line.strip():
            continue
        row = json.loads(line)
        if n == 0 and "meta" in row:
            meta = row["meta"]
            continue
        links.append(Link(**row))
    return meta, links


def files(root: Path = LINKS_DIR, private: bool = True) -> list[Path]:
    """Bağ dosyaları; `private=False` yalnız yerel işaretli dosyaları atlar (genel profil)."""
    out = []
    for path in sorted(root.glob("**/*.jsonl")):
        if private or not read_meta(path).get("private"):
            out.append(path)
    return out


def read_meta(path: Path) -> dict:
    """Yalnız ilk satır: bütün dosyayı okumadan üst bilgi."""
    with open(path, encoding="utf-8") as f:
        first = f.readline()
    return json.loads(first).get("meta", {}) if first.strip() else {}


def check(conn: sqlite3.Connection, links: Iterable[Link]) -> dict[str, list]:
    """Bağları veritabanına karşı denetler: sorun türü -> [(bağ, ayrıntı)]. Boş sözlük: hepsi geçerli."""
    conn.row_factory = sqlite3.Row
    out: dict[str, list] = {}
    sentences: dict[str, sqlite3.Row | None] = {}
    parts: dict[str, set[str]] = {}

    def sentence(sid: str) -> sqlite3.Row | None:
        if sid not in sentences:
            sentences[sid] = conn.execute("SELECT s.id, s.ref, s.incipit, s.text, s.node_id FROM sentences s WHERE s.id = ?",
                                          (sid,)).fetchone()
        return sentences[sid]

    def keys(sid: str) -> set[str]:
        if sid not in parts:
            parts[sid] = {part_key(r[0]) for r in conn.execute(
                "SELECT substr(p.text, a.span_start + 1, a.span_end - a.span_start) FROM arabic a"
                " JOIN paragraphs p ON p.id = a.paragraph_id WHERE a.sentence_id = ?", (sid,))}
            parts[sid] |= {r[0] for r in conn.execute("SELECT hadith_key FROM arabic WHERE sentence_id = ? AND hadith_key IS NOT NULL", (sid,))}
        return parts[sid]

    for link in links:
        if p := link.problems():
            out.setdefault("invalid", []).append((link, "; ".join(p)))
            continue
        if link.scope == "section":
            if not conn.execute("SELECT 1 FROM nodes WHERE id = ?", (link.source,)).fetchone():
                out.setdefault("no_source", []).append((link, link.source))
            continue
        row = sentence(link.source)
        if row is None:
            out.setdefault("no_source", []).append((link, link.source))
            continue
        if link.part and link.part not in keys(link.source):
            out.setdefault("no_part", []).append((link, link.part))
        if link.display and row["incipit"] and not _opening_matches(link.display, row):
            out.setdefault("moved", []).append((link, row["incipit"]))
        if link.target.startswith("risale:") and not conn.execute(
                "SELECT 1 FROM nodes WHERE id = ?", (link.target.removeprefix("risale:"),)).fetchone():
            out.setdefault("no_target", []).append((link, link.target))
    return out


def _opening_matches(display: str, row: sqlite3.Row) -> bool:
    """`display`'deki ilk kelimeler (“…” içi) cümlenin incipit'iyle başlıyor mu; tırnak yoksa denetlenmez."""
    if not (m := re.search(r"“([^”]+)”", display)):
        return True
    shown = m[1].rstrip("…").strip()
    return row["text"].startswith(shown) or row["incipit"].startswith(shown) or shown.startswith(row["incipit"])


def check_files(db: Path = DB_PATH, root: Path = LINKS_DIR) -> dict[str, Counter]:
    conn = sqlite3.connect(db)
    report = {}
    for path in files(root):
        _, links = read(path)
        problems = check(conn, links)
        report[str(path.relative_to(root))] = Counter({"bağ": len(links), **{k: len(v) for k, v in problems.items()}})
    return report


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] != "check":
        sys.exit("kullanım: python -m risale_mcp.links check [--db yol]")
    db = Path(args[args.index("--db") + 1]) if "--db" in args else DB_PATH
    report = check_files(db)
    if not report:
        print(f"bağ dosyası yok: {LINKS_DIR}")
    for name, counts in report.items():
        print(f"{name}: {dict(counts)}")


if __name__ == "__main__":
    main()
