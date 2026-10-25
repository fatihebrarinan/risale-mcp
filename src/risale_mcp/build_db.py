"""Aşama 5: eser JSON'larından SQLite veritabanı.

Kullanım:
    uv run python -m risale_mcp.build_db     # data/books/*.json -> data/risale.db

Veritabanı her seferinde sıfırdan, geçici bir dosyaya kurulur ve doğrulandıktan sonra eskisinin
yerine konur; açık bir sunucu kurulum sırasında eski dosyayı okumaya devam eder. Şema `db.py`'dedir.

Kurulumda:
- Katalogdaki bütün eserler `works` tablosuna girer; JSON'u olmayanlar `built = 0` ile.
- Mecmuada ana cilde eşlenmiş paragrafların cümlesi yoktur (ana ciltte durur); arama dizinine
  yalnızca mecmuaya özgü cümleler girer, aynı cümle iki kez bulunmaz.
- Arapça parçalar geçtikleri cümleye bağlanır. Âyet kaynakları ("Bakara Sûresi, 2:255",
  Hayrat baskısında "Sûre-i Bakara, 255") sûre ve âyet numarasına çözülür; sûre adlarının
  numaraları da numaralı kaynaklardan öğrenilir. Çözülemeyenler raporda listelenir, numarası boş kalır.
- Sonunda sayılar JSON'larla karşılaştırılır; tutmazsa veritabanı yazılmaz.
"""

import argparse
import bisect
import hashlib
import json
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from risale_mcp.catalog import WORKS
from risale_mcp.db import NORMALIZATION, SCHEMA, SCHEMA_VERSION
from risale_mcp.normalize import search_words
from risale_mcp.paths import BOOKS_DIR, DB_PATH, ROOT

# "Bakara Sûresi, 2:255", "Âyet: Sûre-i Âl-i İmrân, 18", "Kalem Sûresi: 1", "Sûre-i Nasr, 1’den"
_SURA_NAME = re.compile(r"^(?:Âyet:\s*)?(?:Sûre-i\s+(?P<pre>[^,:\d]+?)|(?P<post>[^,:\d]+?)\s+S[ûu]resi)\s*[,:]?\s*(?=\d)")
_SURA_AYAH = re.compile(r"(?P<sura>\d+)\s*:\s*(?P<start>\d+)(?:\s*-\s*(?P<end>\d+))?")
_AYAH_ONLY = re.compile(r"(?P<start>\d+)(?:\s*-\s*(?P<end>\d+))?")
NO_SOURCE = "REF-YOK"


@dataclass(frozen=True)
class AyahRef:
    sura: int
    start: int
    end: int


@dataclass
class SuraNames:
    """Sûre adı -> numara; veride numarasıyla geçen yazılışlardan öğrenilir."""
    numbers: dict[str, Counter] = field(default_factory=lambda: defaultdict(Counter))
    spellings: dict[int, Counter] = field(default_factory=lambda: defaultdict(Counter))

    @staticmethod
    def key(name: str) -> str:
        return "".join(search_words(name))

    def learn(self, source: str) -> None:
        name, numbers = _split_source(source)
        if name and (m := _SURA_AYAH.match(numbers)):
            sura = int(m["sura"])
            self.numbers[self.key(name)][sura] += 1
            self.spellings[sura][name] += 1

    def number(self, name: str) -> int | None:
        counts = self.numbers.get(self.key(name))
        return counts.most_common(1)[0][0] if counts else None

    def rows(self) -> list[tuple[str, int, str]]:
        names = {sura: spellings.most_common(1)[0][0] for sura, spellings in self.spellings.items()}
        rows = [(key, counts.most_common(1)[0][0]) for key, counts in self.numbers.items()]
        return [(key, sura, names[sura]) for key, sura in sorted(rows, key=lambda r: (r[1], r[0]))]


def _split_source(source: str) -> tuple[str | None, str]:
    """'Bakara Sûresi, 2:255' -> ('Bakara', '2:255')."""
    source = source.strip()
    if not (m := _SURA_NAME.match(source)):
        return None, source
    return (m["pre"] or m["post"]).strip(), source[m.end():]


def parse_ayah_source(source: str, suras: SuraNames) -> AyahRef | None:
    """Âyet kaynağını sûre ve âyet numarasına çevirir; birden çok âyet sayılmışsa ilk aralık alınır."""
    name, numbers = _split_source(source)
    if m := _SURA_AYAH.search(numbers):
        sura = int(m["sura"])
    else:
        sura = suras.number(name) if name else None
        m = _AYAH_ONLY.match(numbers)
        if sura is None or m is None:
            return None
    start = int(m["start"])
    end = int(m["end"]) if m["end"] else start
    return AyahRef(sura, start, max(start, end))


@dataclass
class BuildReport:
    works: int = 0
    counts: Counter = field(default_factory=Counter)
    unresolved_ayah: Counter = field(default_factory=Counter)

    def lines(self) -> list[str]:
        c = self.counts
        lines = [
            f"{self.works} eser: {c['nodes']} düğüm, {c['paragraphs']} paragraf "
            f"({c['mapped']} tanesi ana cilde eşlenmiş), {c['sentences']} cümle",
            f"  Arapça parça : {c['arabic']} (âyet {c['ayah']}, numarası çözülen {c['ayah_resolved']})",
            f"  sûre adı     : {c['sura_names']} yazılış",
            f"  not / eksik  : {c['notes']} / {c['gaps']}",
        ]
        if self.unresolved_ayah:
            lines.append(f"  çözülemeyen âyet kaynağı: {sum(self.unresolved_ayah.values())}")
            lines += [f"      {n}× {s}" for s, n in self.unresolved_ayah.most_common(10)]
        return lines


def _load_books(books_dir: Path) -> dict[str, tuple[dict, str]]:
    books = {}
    for path in sorted(books_dir.glob("*.json")):
        raw = path.read_bytes()
        data = json.loads(raw)
        books[data["work"]] = (data, hashlib.sha1(raw).hexdigest())
    return books


def _subtree_ends(outline: list[dict]) -> list[int]:
    """Her düğümün alt ağacındaki son düğümün sırası (başlık ağacı kitap sırasındadır)."""
    index = {node["id"]: i for i, node in enumerate(outline)}
    last = list(range(len(outline)))
    for i in range(len(outline) - 1, 0, -1):
        parent = index[outline[i]["parent_id"]]
        last[parent] = max(last[parent], last[i])
    return last


def _depths(outline: list[dict]) -> list[int]:
    depth: dict[str, int] = {}
    for node in outline:
        depth[node["id"]] = depth[node["parent_id"]] + 1 if node["parent_id"] else 0
    return [depth[node["id"]] for node in outline]


def _insert_nodes(conn: sqlite3.Connection, work: str, outline: list[dict]) -> None:
    for ord_, (node, last, depth) in enumerate(zip(outline, _subtree_ends(outline), _depths(outline))):
        cur = conn.execute(
            "INSERT INTO nodes (id, work, parent_id, ord, last_ord, depth, title, subtitle, toc_title,"
            " type, number, heading, ref, url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (node["id"], work, node["parent_id"], ord_, last, depth, node["title"], node.get("subtitle"),
             node.get("toc_title"), node.get("type"), node.get("number"), node.get("heading"),
             node["ref"], node.get("url")))
        headings = " ".join(filter(None, (node["title"], node.get("subtitle"), node.get("toc_title"))))
        conn.execute("INSERT INTO nodes_fts (rowid, words) VALUES (?, ?)",
                     (cur.lastrowid, " ".join(search_words(headings))))
        conn.executemany("INSERT INTO node_sources VALUES (?, ?, ?)",
                         [(node["id"], i, source) for i, source in enumerate(node.get("sources", []))])


def _insert_paragraphs(conn: sqlite3.Connection, work: str, paragraphs: list[dict]) -> None:
    for ord_, p in enumerate(paragraphs):
        conn.execute(
            "INSERT INTO paragraphs (id, work, node_id, ord, kind, text, parent_id, mark_offset, anchor,"
            " center, continued) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (p["id"], work, p["node_id"], ord_, p["kind"], p.get("text"), p.get("parent_id"),
             p.get("offset"), p.get("anchor"), int(p.get("center", False)), int(p.get("continued", False))))
        conn.executemany("INSERT INTO paragraph_sources VALUES (?, ?, ?)",
                         [(p["id"], i, source) for i, source in enumerate(p.get("source", []))])


def _insert_sentences(conn: sqlite3.Connection, work: str, sentences: list[dict], hasiye: set[str]) -> None:
    for s in sentences:
        cur = conn.execute(
            "INSERT INTO sentences (id, work, node_id, paragraph_id, n, hasiye, span_start, span_end, text,"
            " incipit, hash, ref) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (s["id"], work, s["node_id"], s["paragraph_id"], s["n"], int(s["paragraph_id"] in hasiye),
             s["start"], s["end"], s["text"], s["incipit"], s["hash"], s["ref"]))
        conn.execute("INSERT INTO sentences_fts (rowid, words) VALUES (?, ?)",
                     (cur.lastrowid, " ".join(search_words(s["text"]))))


def _insert_arabic(conn: sqlite3.Connection, book: dict, suras: SuraNames, report: BuildReport) -> None:
    # Paragraf -> (cümle başları, cümle kimlikleri); parça, başladığı cümleye bağlanır.
    starts: dict[str, tuple[list[int], list[str]]] = defaultdict(lambda: ([], []))
    for s in book["sentences"]:
        offsets, ids = starts[s["paragraph_id"]]
        offsets.append(s["start"])
        ids.append(s["id"])
    for p in book["paragraphs"]:
        offsets, ids = starts.get(p["id"], ([], []))
        for i, part in enumerate(p.get("arabic", [])):
            k = bisect.bisect_right(offsets, part["start"]) - 1
            source = part.get("source") if part.get("source") != NO_SOURCE else None
            ayah = None
            if part["kind"] == "ayet" and source:
                report.counts["ayah"] += 1
                ayah = parse_ayah_source(source, suras)
                if ayah:
                    report.counts["ayah_resolved"] += 1
                else:
                    report.unresolved_ayah[source] += 1
            conn.execute(
                "INSERT INTO arabic VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (p["id"], i, ids[k] if k >= 0 else None, part["start"], part["end"], part["kind"],
                 part.get("meal"), source, ayah and ayah.sura, ayah and ayah.start, ayah and ayah.end))
            report.counts["arabic"] += 1


def _insert_book(conn: sqlite3.Connection, book: dict, suras: SuraNames, report: BuildReport) -> None:
    work = book["work"]
    _insert_nodes(conn, work, book["outline"])
    _insert_paragraphs(conn, work, book["paragraphs"])
    hasiye = {p["id"] for p in book["paragraphs"] if p["kind"] == "hasiye"}
    _insert_sentences(conn, work, book["sentences"], hasiye)
    _insert_arabic(conn, book, suras, report)
    conn.executemany("INSERT INTO notes VALUES (?, ?, ?, ?)",
                     [(work, n["node_id"], n.get("after"), n["text"]) for n in book.get("notes", [])])
    conn.executemany("INSERT INTO gaps VALUES (?, ?, ?, ?)",
                     [(work, g["node_id"], g.get("after"), g["missing_blocks"]) for g in book.get("gaps", [])])
    c = report.counts
    c["nodes"] += len(book["outline"])
    c["paragraphs"] += len(book["paragraphs"])
    c["mapped"] += sum("text" not in p for p in book["paragraphs"])
    c["sentences"] += len(book["sentences"])
    c["notes"] += len(book.get("notes", []))
    c["gaps"] += len(book.get("gaps", []))


def _verify(conn: sqlite3.Connection, report: BuildReport) -> None:
    """Tablolardaki sayılar JSON'lardan sayılanlarla aynı olmalı."""
    c = report.counts
    expected = {
        "nodes": c["nodes"], "nodes_fts": c["nodes"], "paragraphs": c["paragraphs"],
        "sentences": c["sentences"], "sentences_fts": c["sentences"], "arabic": c["arabic"],
        "notes": c["notes"], "gaps": c["gaps"], "works WHERE built = 1": report.works,
    }
    wrong = []
    for table, n in expected.items():
        found = conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
        if found != n:
            wrong.append(f"{table}: {found} (beklenen {n})")
    orphans = conn.execute(
        "SELECT count(*) FROM sentences s LEFT JOIN paragraphs p ON p.id = s.paragraph_id"
        " LEFT JOIN nodes n ON n.id = s.node_id WHERE p.id IS NULL OR n.id IS NULL").fetchone()[0]
    if orphans:
        wrong.append(f"paragrafı ya da düğümü olmayan cümle: {orphans}")
    if wrong:
        raise RuntimeError("Veritabanı JSON'larla tutmuyor:\n  " + "\n  ".join(wrong))


def build(books_dir: Path = BOOKS_DIR, out: Path = DB_PATH) -> BuildReport:
    books = _load_books(books_dir)
    unknown = set(books) - {w.slug for w in WORKS}
    if unknown:
        raise ValueError(f"Katalogda olmayan eser JSON'u: {sorted(unknown)}")

    suras = SuraNames()
    for data, _ in books.values():
        for p in data["paragraphs"]:
            for part in p.get("arabic", []):
                if part["kind"] == "ayet" and part.get("source"):
                    suras.learn(part["source"])

    tmp = out.with_name(out.name + ".tmp")
    tmp.unlink(missing_ok=True)
    report = BuildReport()
    conn = sqlite3.connect(tmp)
    try:
        conn.execute("PRAGMA journal_mode = OFF")
        conn.execute("PRAGMA synchronous = OFF")
        conn.executescript(SCHEMA)
        with conn:
            for ord_, work in enumerate(WORKS):
                data, sha1 = books.get(work.slug, (None, None))
                language = data.get("language", work.language) if data else work.language
                source = work.source
                conn.execute(
                    "INSERT INTO works VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (work.slug, ord_, work.title, work.group, language, work.status, work.note or None,
                     source and source.site, source and source.book, int(data is not None), sha1))
                if data:
                    _insert_book(conn, data, suras, report)
                    report.works += 1
            sura_rows = suras.rows()
            conn.executemany("INSERT INTO sura_names VALUES (?, ?, ?)", sura_rows)
            report.counts["sura_names"] = len(sura_rows)
            conn.executemany("INSERT INTO meta VALUES (?, ?)", [
                ("schema_version", str(SCHEMA_VERSION)),
                ("normalization", NORMALIZATION),
                ("built_at", datetime.now(timezone.utc).isoformat(timespec="seconds")),
            ])
        _verify(conn, report)
        for table in ("sentences_fts", "nodes_fts"):
            conn.execute(f"INSERT INTO {table} ({table}) VALUES ('optimize')")
        conn.execute("ANALYZE")
        conn.commit()
    except BaseException:
        conn.close()
        tmp.unlink(missing_ok=True)
        raise
    conn.close()
    tmp.replace(out)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--books", type=Path, default=BOOKS_DIR, help="eser JSON'larının klasörü")
    parser.add_argument("--out", type=Path, default=DB_PATH, help="yazılacak veritabanı")
    args = parser.parse_args()
    if not any(args.books.glob("*.json")):
        sys.exit(f"{args.books} içinde eser JSON'u yok; önce `uv run python -m risale_mcp.build --all`.")
    report = build(args.books, args.out)
    print("\n".join(report.lines()))
    out = args.out.resolve()
    shown = out.relative_to(ROOT) if out.is_relative_to(ROOT) else out
    print(f"  yazıldı: {shown} ({out.stat().st_size / 1e6:.0f} MB)")


if __name__ == "__main__":
    main()
