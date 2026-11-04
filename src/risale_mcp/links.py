"""Bağlar: Risale'nin âyetlerle, hadislerle ve kendi içinde kurduğu bağların ortak kaydı (`docs/bag-altyapisi-plani.md`).

    uv run python -m risale_mcp.links check [--db yol]     # data/links/**/*.jsonl'yi veritabanına karşı denetler

Bir satır bir bağdır (JSON Lines); dosyanın ilk satırı üst bilgidir (`{"meta": {...}}`). Dosyalar
`data/links/<alan>/<yöntem>.jsonl`; bağı üreten iş yazar, her profilin `build_db`'si okur. Hadis sunucusu (HA5) Risale
veritabanı olmadan da okuyabilsin diye kaynağın atfı `display`'de durur.

Alanlar:

    source    bağın metindeki ucu: cümle kimliği, aralık (`…/c004..c007`, aynı bölümde) ya da bölüm kapsamlı bağda
              düğüm kimliği (`scope: section`). Önek isteğe bağlıdır: `risale:sozler/10/c001`; öneksiz kimlik bu
              kütüphanenin metnidir (bugünkü dosyalar öyle yazılır, kimlikler profilde tektir)
    part      cümlede birden çok Arapça parça varsa hangisi: parçanın iskelet anahtarı (`quran.skeleton`; hadiste
              `arabic.hadith_key` ile aynı). Sıra numarası değil: yeniden ayrıştırmada kaymasın. İşaretsiz metinde
              (müfessirin şerhi) alıntının iskeletidir, cümlenin iskeletinde geçmelidir
    target    ad alanlı kimlik: quran:2:255, quran:2:255-257, hadis:bukhari/52, hadis-derlem:sanadset:220501
              (kütüphanede henüz olmayan rivayet; Hadith API alt numarası tirmidhi:2780.2) ya da metin: bir eserin
              cümlesi, aralığı ya da bölümü, koleksiyonun ad alanıyla (risale:lemalar/30, risale:sozler/1/c004..c007;
              ileride tefsir:…)
    type      quote (söz aktarılıyor), relation (âyetle bağ), reference (başka yere gönderme)
    relation  alıntıda lafız ilişkisi (verbatim, abridged, by_meaning, phrase); ilişkide türü (isaret, acilis, izah,
              dayanak, risale); göndermede `old_name`. Metinden metne (`TEXT_RELATIONS`, H4; türler T5'te okumayla
              kesinleşir): quote ile same_words (aynı söz, kaynağı anılmadan) ya da transmits (nakil: kaynak hedefin
              sözünü aktarıyor), relation ile same_view, different_view, objection (kaynak hedefe itiraz ediyor)
    method    bağı kuran: source_mark, quran_text, corpus, cited_chapter, reading, rule, curated, structure (eserin
              yapısı söylüyor: müfessirin âyet birimi başlığı), scholar (isimli âlimin okuması)
    strength  strong | weak
    evidence  yönteme göre serbest (kanıt cümlesi, künye, okuyucu cevapları, puan)
    display   kaynağın gösterilecek atfı (`cite_as`); doğrulamada kimlik kaymasını yakalar
    target_display  metin hedefinin atfı (T4): hedefin metni bu profilde yoksa (başka sunucunun alanı) bağ yine
              gösterilebilsin; üreten iş `cite_as` ile yazar, doğrulama hedefin kaymasını yakalar. Yalnız yerelde
              duran (`private`) bir esere giden bağ, o eseri taşımayan profile hiç girmez (`build_db`)

Ad alanı (H4): metnin ad alanı eserin koleksiyonundan gelir (`risale/kulliyat` -> `risale`); yeni bir koleksiyon
(`tefsir/…`) eklenince ad alanı kendiliğinden geçerli olur. Kimlikler önek almaz: önek yalnız bağın ucundadır.

Denetim kararları bağların içinde değil, ayrı dosyalardadır (`link_reviews.py`, H5).

Doğrulama (`check`): kaynak cümle, aralık ya da düğüm var mı, önekliyse eser o ad alanında mı, `part` o cümlenin Arapça parçalarından biri mi, `display`
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

from risale_mcp.books.model import REF_SEPARATOR as REF_SEP
from risale_mcp.catalog.model import Collection
from risale_mcp.paths import DB_PATH, LINKS_DIR
from risale_mcp.quran import skeleton

TYPES = ("quote", "relation", "reference")
METHODS = ("source_mark", "quran_text", "corpus", "cited_chapter", "reading", "rule", "curated", "structure", "scholar")
STRENGTHS = ("strong", "weak")
SCOPES = ("sentence", "section")
# Metnin ad alanları: koleksiyonların ilk parçası (`risale/kulliyat` -> risale). Kur'ân ve hadis metin ad alanı değil.
TEXT_NAMESPACES = tuple(sorted({c.value.split("/", 1)[0] for c in Collection}))
# Metinden metne bağın türleri (hedef bir eserin metniyse): geçici, T5'te okumayla kesinleşir.
TEXT_RELATIONS = {"quote": ("same_words", "transmits"), "relation": ("same_view", "different_view", "objection"),
                  "reference": ("old_name",)}
_TEXT_ID = r"[a-z0-9][a-z0-9/._-]*"
_TARGET = re.compile(r"^(?:quran:(\d{1,3}):(\d{1,3})(?:-(\d{1,3}))?|hadis:[a-z0-9-]+/[0-9]+(?:-\d+)?"
                     r"|hadis-derlem:[a-z_]+:[0-9]+(?:\.[0-9]+)?"
                     rf"|(?:{'|'.join(TEXT_NAMESPACES)}):{_TEXT_ID})$")
_SOURCE = re.compile(rf"^(?:(?:{'|'.join(TEXT_NAMESPACES)}):)?{_TEXT_ID}$")


def text_endpoint(value: str) -> tuple[str | None, str] | None:
    """Metin ucu: (ad alanı ya da öneksizse None, yerel kimlik); Kur'ân ya da hadis ucuysa None."""
    namespace, sep, local = value.partition(":")
    if not sep:
        return None, value
    return (namespace, local) if namespace in TEXT_NAMESPACES else None


def local_id(value: str) -> str:
    """Metin ucunun veritabanındaki kimliği (önek atılmış); metin değilse olduğu gibi."""
    return end[1] if (end := text_endpoint(value)) else value


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
    target_display: str | None = field(default=None, hash=False, compare=False)

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
        if not _SOURCE.match(self.source):
            out.append(f"source {self.source!r}")
        if not (m := _TARGET.match(self.target)):
            out.append(f"target {self.target!r}")
        elif self.target.startswith("quran:") and not (1 <= int(m[1]) <= 114 and (m[3] is None or int(m[3]) >= int(m[2]))):
            out.append(f"target {self.target!r}")
        elif text_endpoint(self.target) and self.type in TEXT_RELATIONS and self.relation not in TEXT_RELATIONS[self.type]:
            out.append(f"relation {self.relation!r} (metinden metne {self.type}: {', '.join(TEXT_RELATIONS[self.type])})")
        return out

    @property
    def key(self) -> tuple:
        """Bağın anahtarı (denetim kararları buna bağlanır, H5): kaynak, hedef, tür, parça. Güç ve ilişki türü
        anahtarda değildir: kurallar değişince onlar değişebilir, kararın konusu da çoğu zaman onlardır."""
        return local_id(self.source), self.target, self.type, self.part or ""

    def to_json(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v not in (None, {}, "") and not (k == "scope" and v == "sentence")}


def part_key(text: str) -> str:
    """Arapça parçanın bağdaki anahtarı: iskelet (hadiste `arabic.hadith_key` ile aynı)."""
    return skeleton(text)


def write(path: Path, links: Iterable[Link], **meta) -> int:
    """Üst bilgi ve kitap sırasıyla değil, (kaynak, hedef) sırasıyla bağlar: dosya farkı okunur kalsın."""
    # Tekilleştirme kaydın tamamıyla: aynı yöntemle kurulmuş ama kanıtı ayrı iki bağ (Adım 7'nin ve Adım 9'un aynı
    # rivayet için okumaları) ayrı kalır.
    rows = sorted({json.dumps(l.to_json(), ensure_ascii=False, sort_keys=True): l for l in links}.values(),
                  key=lambda l: (l.source, l.part or "", l.target, l.method, json.dumps(l.evidence, sort_keys=True)))
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
    """Bağ dosyaları; `private=False` yalnız yerel işaretli dosyaları atlar (genel profil). Denetim kararları
    (`reviews/`, `link_reviews.py`) bağ değildir."""
    out = []
    for path in sorted(root.glob("**/*.jsonl")):
        if path.relative_to(root).parts[0] == "reviews":
            continue
        if private or not read_meta(path).get("private"):
            out.append(path)
    return out


def read_meta(path: Path) -> dict:
    """Yalnız ilk satır: bütün dosyayı okumadan üst bilgi."""
    with open(path, encoding="utf-8") as f:
        first = f.readline()
    return json.loads(first).get("meta", {}) if first.strip() else {}


def resolve(conn: sqlite3.Connection, value: str, scope: str | None = None) -> dict | None:
    """Metin ucunu veritabanında çözer: {kind: sentence | range | section, id, node, work, namespace} ya da None
    (yok, ad alanı tutmuyor ya da aralık bir bölümün içinde ileri gitmiyor). `scope` verilmezse (hedef) önce cümle
    ya da aralık, sonra bölüm denenir."""
    if (end := text_endpoint(value)) is None:
        return None
    namespace, local = end
    first, _, last = local.partition("..")
    row = None
    if scope != "section":
        row = conn.execute("SELECT s.id, s.node_id, s.seq, w.slug, w.collection FROM sentences s"
                           " JOIN works w ON w.slug = s.work WHERE s.id = ?", (first,)).fetchone()
    if row is not None:
        out = {"kind": "sentence", "id": local, "node": row[1], "work": row[3], "namespace": row[4].split("/", 1)[0]}
        if last:
            last = last if "/" in last else f"{first.rsplit('/', 1)[0]}/{last}"
            end_row = conn.execute("SELECT node_id, seq FROM sentences WHERE id = ?", (last,)).fetchone()
            if end_row is None or end_row[0] != row[1] or end_row[1] < row[2]:
                return None
            out["kind"] = "range"
    elif scope != "sentence" and not last and (node := conn.execute(
            "SELECT n.id, w.slug, w.collection FROM nodes n JOIN works w ON w.slug = n.work WHERE n.id = ?",
            (local,)).fetchone()):
        out = {"kind": "section", "id": local, "node": node[0], "work": node[1], "namespace": node[2].split("/", 1)[0]}
    else:
        return None
    return out if namespace in (None, out["namespace"]) else None


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
        source = resolve(conn, link.source, link.scope)
        if source is None:
            out.setdefault("no_source", []).append((link, link.source))
            continue
        if text_endpoint(link.target) and resolve(conn, link.target) is None:
            out.setdefault("no_target", []).append((link, link.target))
        if source["kind"] == "section":
            continue
        first = source["id"].partition("..")[0]
        row = sentence(first)
        # Parça: cümlenin işaretli Arapça parçalarından biri ya da (işaretsiz metinde, müfessirin şerhi) cümlenin
        # harf iskeletinin bir parçası: aynı cümlede aynı âyetin iki alıntısı ayrı bağdır (T7).
        if link.part and link.part not in keys(first) and link.part not in skeleton(row["text"]):
            out.setdefault("no_part", []).append((link, link.part))
        if link.display and row["incipit"] and not _opening_matches(link.display, row):
            out.setdefault("moved", []).append((link, row["incipit"]))
    for link in links:
        if not (link.target_display and text_endpoint(link.target)) or link.problems():
            continue
        target = resolve(conn, link.target)
        if target and target["kind"] != "section":
            row = sentence(target["id"].partition("..")[0])
            if row["incipit"] and not _opening_matches(link.target_display, row):
                out.setdefault("target_moved", []).append((link, row["incipit"]))
    return out


def cite_as(conn: sqlite3.Connection, value: str, scope: str | None = None) -> str | None:
    """Metin ucunun kullanıcıya gösterilecek atfı, veriden: cümlede "yol › “ilk kelimeler…”", aralıkta "… ile başlayan
    N cümle", bölümde yolun kendisi. Uç bu veritabanında yoksa None (o zaman bağın kayıtlı `display`'i kullanılır)."""
    from risale_mcp.library import cite, opening
    end = resolve(conn, value, scope)
    if end is None:
        return None
    if end["kind"] == "section":
        return conn.execute("SELECT ref FROM nodes WHERE id = ?", (end["id"],)).fetchone()[0]
    first, _, last = end["id"].partition("..")
    ref, incipit, text, n = conn.execute("SELECT ref, incipit, text, n FROM sentences WHERE id = ?", (first,)).fetchone()
    count = 1
    if last:                                  # düğüm içi sıra: aradaki hâşiye cümleleri sayılmaz
        last = last if "/" in last else f"{first.rsplit('/', 1)[0]}/{last}"
        count = conn.execute("SELECT n FROM sentences WHERE id = ?", (last,)).fetchone()[0] - n + 1
    return cite(ref.rsplit(REF_SEP, 1)[0], opening(incipit, text), count)


def _opening_matches(display: str, row: sqlite3.Row) -> bool:
    """`display`'deki ilk kelimeler (son “…” çifti: başlık da tırnak taşıyabilir, “Ye's”) cümleyle başlıyor mu."""
    if not (quoted := re.findall(r"“([^”]+)”", display)):
        return True
    shown = quoted[-1].rstrip("…").strip()
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
