"""SQLite veritabanının şeması ve bağlantısı.

Veritabanı `data/books/*.json` dosyalarından `build_db` ile her seferinde sıfırdan kurulur;
asıl kaynak JSON'lardır, veritabanı elle düzenlenmez.

Kimlikler ve sıralar:
- `id` sütunları JSON'daki kalıcı kimliklerdir (`sozler/10/c032`); atıflar bunlarla yapılır.
- `seq` yalnızca bu veritabanında geçerli tamsayı anahtardır (FTS5 satır numarası). Eserler
  katalog sırasıyla, her eserin kayıtları kitap sırasıyla dizildiği için `seq` sırası okuma sırasıdır.
- `ord` eser içindeki sıradır. Düğümün alt ağacı `ord`..`last_ord` aralığındaki düğümlerdir.

Arama dizinleri metni `normalize.search_words` biçiminde tutar (işaretsiz, ı = i). Sorgular da
aynı biçime çevrilir (`search.py`); biçim değişirse `NORMALIZATION` artırılır ve veritabanı yeniden kurulur.

Anlamsal aramaya hazırlık: vektörler bu dosyaya değil, yeniden kurulumdan etkilenmeyen ayrı bir
dosyaya `(model, sentences.hash)` anahtarıyla yazılacak. Cümle metni değişmedikçe özeti de değişmez,
vektör geçerli kalır; aynı metin (ör. "﷽") tek vektör paylaşır. Sonuçlar `sentences.hash` üzerinden
birleştirilir ve kelime aramasıyla aynı `search.Hit` biçiminde döner.
"""

import sqlite3
from pathlib import Path

from risale_mcp.paths import DB_PATH

SCHEMA_VERSION = 3
NORMALIZATION = "search_words-1"

SCHEMA = """
CREATE TABLE meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

-- Katalogdaki bütün eserler; JSON'u olmayanlar (bulunamayan, ertelenen) `built = 0`.
CREATE TABLE works (
    slug        TEXT PRIMARY KEY,
    ord         INTEGER NOT NULL,
    title       TEXT NOT NULL,
    group_name  TEXT NOT NULL,
    language    TEXT NOT NULL,
    status      TEXT NOT NULL,
    note        TEXT,
    site        TEXT,
    source_book TEXT,
    built       INTEGER NOT NULL,
    json_sha1   TEXT
);

CREATE TABLE nodes (
    seq       INTEGER PRIMARY KEY,
    id        TEXT NOT NULL UNIQUE,
    work      TEXT NOT NULL REFERENCES works(slug),
    parent_id TEXT REFERENCES nodes(id),
    ord       INTEGER NOT NULL,
    last_ord  INTEGER NOT NULL,
    depth     INTEGER NOT NULL,
    title     TEXT NOT NULL,
    subtitle  TEXT,
    toc_title TEXT,
    type      TEXT,
    number    INTEGER,
    heading   TEXT,
    ref       TEXT NOT NULL,
    url       TEXT
);
CREATE INDEX nodes_work_ord ON nodes(work, ord);
CREATE INDEX nodes_parent ON nodes(parent_id);

-- Mecmua düğümünün ana ciltteki karşılıkları.
CREATE TABLE node_sources (
    node_id        TEXT NOT NULL REFERENCES nodes(id),
    ord            INTEGER NOT NULL,
    source_node_id TEXT NOT NULL,
    PRIMARY KEY (node_id, ord)
);
CREATE INDEX node_sources_source ON node_sources(source_node_id);

-- `text` NULL ise paragraf mecmuada ana cilde eşlenmiştir (`paragraph_sources`).
-- Hâşiyede `parent_id` bağlı olduğu paragraf (ya da başlıktaysa düğüm), `anchor` bağlı olduğu cümle.
CREATE TABLE paragraphs (
    id          TEXT PRIMARY KEY,
    work        TEXT NOT NULL REFERENCES works(slug),
    node_id     TEXT NOT NULL REFERENCES nodes(id),
    ord         INTEGER NOT NULL,
    kind        TEXT NOT NULL,
    text        TEXT,
    parent_id   TEXT,
    mark_offset INTEGER,
    anchor      TEXT,
    center      INTEGER NOT NULL DEFAULT 0,
    continued   INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX paragraphs_node ON paragraphs(node_id, ord);
CREATE INDEX paragraphs_parent ON paragraphs(parent_id);

CREATE TABLE paragraph_sources (
    paragraph_id        TEXT NOT NULL REFERENCES paragraphs(id),
    ord                 INTEGER NOT NULL,
    source_paragraph_id TEXT NOT NULL,
    PRIMARY KEY (paragraph_id, ord)
);
CREATE INDEX paragraph_sources_source ON paragraph_sources(source_paragraph_id);

-- Atıf birimi. `span_start`/`span_end` paragraf metnindeki konumdur; `hash` metnin SHA-1 özeti.
CREATE TABLE sentences (
    seq          INTEGER PRIMARY KEY,
    id           TEXT NOT NULL UNIQUE,
    work         TEXT NOT NULL REFERENCES works(slug),
    node_id      TEXT NOT NULL REFERENCES nodes(id),
    paragraph_id TEXT NOT NULL REFERENCES paragraphs(id),
    n            INTEGER NOT NULL,
    hasiye       INTEGER NOT NULL,
    span_start   INTEGER NOT NULL,
    span_end     INTEGER NOT NULL,
    text         TEXT NOT NULL,
    incipit      TEXT NOT NULL,
    hash         TEXT NOT NULL,
    ref          TEXT NOT NULL
);
CREATE INDEX sentences_node ON sentences(node_id, seq);
CREATE INDEX sentences_paragraph ON sentences(paragraph_id, seq);
CREATE INDEX sentences_hash ON sentences(hash);

-- Metindeki Arapça (ve Farsça…) parçalar. Âyette kaynak çözülebildiyse sûre ve âyet numaraları dolu.
-- `meal` nâşirin tercümesidir, müellifin değil. `ayah_check`: kaynağın verdiği numara Kur'ân metniyle
-- (Tanzil) denetlendi: exact, near (metin komşu âyetlerde), differs (iktibas, kısaltma ya da yanlış numara), empty.
CREATE TABLE arabic (
    paragraph_id TEXT NOT NULL REFERENCES paragraphs(id),
    ord          INTEGER NOT NULL,
    sentence_id  TEXT REFERENCES sentences(id),
    span_start   INTEGER NOT NULL,
    span_end     INTEGER NOT NULL,
    kind         TEXT NOT NULL,
    meal         TEXT,
    source       TEXT,
    sura         INTEGER,
    ayah_start   INTEGER,
    ayah_end     INTEGER,
    ayah_check   TEXT,
    PRIMARY KEY (paragraph_id, ord)
);
CREATE INDEX arabic_ayah ON arabic(sura, ayah_start);
CREATE INDEX arabic_sentence ON arabic(sentence_id);

-- Sûre adları veriden çıkarılır ("Bakara Sûresi, 2:255"). `key` adın arama biçimi, `name` en sık yazılışı.
CREATE TABLE sura_names (
    key    TEXT PRIMARY KEY,
    number INTEGER NOT NULL,
    name   TEXT NOT NULL
);

-- Kur'ân katmanı (data/quran.json, Tanzil): atıf birimi âyettir. `text` Medine Mushafı hattı, harekeli
-- (kullanıcıya gösterilen); `text_simple` imlâî yazım, harekeli. Mealler mütercimleriyle ayrı tabloda.
-- Kaynağın âyet olarak işaretlemediği Kur'ân alıntıları (Hizbler, el-Mesnevî el-Arabî); Arapça parçanın
-- içinde Tanzil metniyle bulundu. `n` parçadaki sırası; `span_*` paragraf metnindeki konumu.
CREATE TABLE ayah_quotes (
    paragraph_id TEXT NOT NULL REFERENCES paragraphs(id),
    ord          INTEGER NOT NULL,
    n            INTEGER NOT NULL,
    sentence_id  TEXT REFERENCES sentences(id),
    span_start   INTEGER NOT NULL,
    span_end     INTEGER NOT NULL,
    sura         INTEGER NOT NULL,
    ayah_start   INTEGER NOT NULL,
    ayah_end     INTEGER NOT NULL,
    PRIMARY KEY (paragraph_id, ord, n)
);
CREATE INDEX ayah_quotes_ayah ON ayah_quotes(sura, ayah_start);

CREATE TABLE quran_suras (
    number  INTEGER PRIMARY KEY,
    name    TEXT NOT NULL,
    name_ar TEXT NOT NULL,
    ayahs   INTEGER NOT NULL
);

CREATE TABLE quran_ayahs (
    sura        INTEGER NOT NULL REFERENCES quran_suras(number),
    ayah        INTEGER NOT NULL,
    text        TEXT NOT NULL,
    text_simple TEXT NOT NULL,
    PRIMARY KEY (sura, ayah)
);

CREATE TABLE quran_translators (
    id   TEXT PRIMARY KEY,
    ord  INTEGER NOT NULL,
    name TEXT NOT NULL
);

-- Bir meal art arda birkaç âyeti birlikte tercüme edebilir: `first_ayah`..`last_ayah` (tek âyette ikisi de `ayah`).
CREATE TABLE quran_translations (
    translator TEXT NOT NULL REFERENCES quran_translators(id),
    sura       INTEGER NOT NULL,
    ayah       INTEGER NOT NULL,
    text       TEXT NOT NULL,
    first_ayah INTEGER NOT NULL,
    last_ayah  INTEGER NOT NULL,
    PRIMARY KEY (sura, ayah, translator)
);

CREATE TABLE notes (
    work    TEXT NOT NULL REFERENCES works(slug),
    node_id TEXT NOT NULL,
    after   TEXT,
    text    TEXT NOT NULL
);

-- Kaynakta bulunamayan bloklar; metin uydurulmaz. `after` NULL ise düğümün başındadır.
-- `note`: eksiğin açıklaması (ör. başka bir baskıda olup bu baskıda olmayan makale).
CREATE TABLE gaps (
    work           TEXT NOT NULL REFERENCES works(slug),
    node_id        TEXT NOT NULL,
    after          TEXT,
    missing_blocks INTEGER NOT NULL,
    note           TEXT
);

-- Arama dizinleri: satır numarası `sentences.seq` / `nodes.seq`. Metin önceden normalleştirilir;
-- `remove_diacritics 0` ile FTS5 onu yalnızca kelimelere böler, harflere dokunmaz.
CREATE VIRTUAL TABLE sentences_fts USING fts5(words, tokenize = "unicode61 remove_diacritics 0");
CREATE VIRTUAL TABLE nodes_fts USING fts5(words, tokenize = "unicode61 remove_diacritics 0");
"""


class DatabaseError(RuntimeError):
    pass


def connect(path: Path = DB_PATH) -> sqlite3.Connection:
    """Salt okunur bağlantı; veritabanı yoksa ya da şeması eskiyse açıklayıcı hata verir."""
    if not path.exists():
        raise DatabaseError(f"{path} yok; önce `uv run python -m risale_mcp.build_db` çalıştırın.")
    conn = sqlite3.connect(f"{path.resolve().as_uri()}?mode=ro", uri=True, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    version = conn.execute("SELECT value FROM meta WHERE key = 'schema_version'").fetchone()
    if version is None or int(version["value"]) != SCHEMA_VERSION:
        conn.close()
        raise DatabaseError(f"{path} eski şemada; `uv run python -m risale_mcp.build_db` ile yeniden kurun.")
    return conn
