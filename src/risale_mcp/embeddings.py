"""Aşama 8: cümle vektörleri (anlamsal arama).

Kullanım:
    uv run python -m risale_mcp.embeddings build voyage-4-large            # eksik vektörleri çıkar
    uv run python -m risale_mcp.embeddings build openai-3-large --variant title
    uv run python -m risale_mcp.embeddings status                                          # depolar ve eksikler

Sağlayıcılar API'dir; anahtarlar ortam değişkenindedir (`VOYAGE_API_KEY`, `OPENAI_API_KEY`;
proje klasöründeki `.env` dosyasından okunur, bkz. `env.py`). İstekler standart
kütüphaneyle yapılır; sunucuya yalnızca numpy gerekir. Bütün modeller 1024 boyutla kullanılır
(boyutu sabit olan `voyage-multilingual-2` dışında).

Vektörü çıkarılan metin (birim) seçeneğe (`variant`) göre değişir:
- sentence: cümlenin kendisi. Anahtar `sentences.hash`; aynı metinli cümleler tek vektör paylaşır.
- title: bölümün yolu ve cümle ("Sözler › Onuncu Söz › …" satırı, ardından cümle).
- context: yalnızca bağlamlı modellerde (`voyage-context-4`). Bir bölümün kendi cümleleri bir
  belgedir (uzun bölüm ardışık parçalara bölünür); her cümlenin vektörü belgenin bağlamını taşır.
Anahtar vektörü çıkarılan metinden gelir. Veritabanı yeniden kurulsa da metin değişmedikçe vektör
geçerli kalır; yalnızca değişen ya da yeni birimlerin vektörü çıkarılır.

Depo: `data/vectors/<model>.<variant>.npy` ve aynı adlı `.keys.json`. Vektörler float16 birim vektördür;
sunucunun modeli (`SEARCH_MODEL`, `voyage-context-4`) ise 512 boyutlu int8 vektörleri sağlayıcıdan hazır alır
(≈56 MB; değerlendirmede 1024 boyutlu float16 ile aynı isabet).
Değerlendirme sorularının vektörleri `data/vectors/queries.<model>.json`'da önbelleğe alınır.
"""

import argparse
import hashlib
import http.client
import json
import os
import sqlite3
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from risale_mcp.db import connect
from risale_mcp.env import load_env
from risale_mcp.paths import DATA_DIR, DB_PATH, ROOT

VECTORS_DIR = DATA_DIR / "vectors"
DIMENSIONS = 1024
CHARS_PER_TOKEN = 1.6      # token tahmini için temkinli oran (ölçülen ortalama ≈2,05; Arapça daha yoğun)
DOCUMENT_TOKENS = 8_000    # bağlamlı modelde bir belgenin en çok tahmini tokenı
SAVE_EVERY = 20            # kaç istekte bir depo diske yazılır
RETRIES = 8


@dataclass(frozen=True)
class Model:
    name: str               # bizim adımız
    provider: str           # "voyage" | "openai"
    api_name: str
    max_tokens: int         # bir istekte en çok token (sağlayıcının sınırı)
    max_items: int          # bir istekte en çok metin
    dimensions: int | None = DIMENSIONS     # None: modelin kendi boyutu
    contextual: bool = False
    int8: bool = False      # belge vektörleri sağlayıcıdan 8 bitlik tamsayı olarak alınır (sorgular float)


MODELS = {m.name: m for m in [
    Model("voyage-4-large", "voyage", "voyage-4-large", 120_000, 1000),
    Model("voyage-4", "voyage", "voyage-4", 320_000, 1000),
    Model("voyage-4-lite", "voyage", "voyage-4-lite", 1_000_000, 1000),
    Model("voyage-multilingual-2", "voyage", "voyage-multilingual-2", 120_000, 1000, dimensions=None),
    # Anlamsal aramanın modeli (SEARCH_MODEL): 512 boyut ve int8 isabeti düşürmeden depoyu dörtte bire indirir.
    Model("voyage-context-4", "voyage", "voyage-context-4", 32_000, 1000, dimensions=512, contextual=True, int8=True),
    Model("openai-3-large", "openai", "text-embedding-3-large", 100_000, 2048),   # büyük isteklerde bağlantı kopuyor
    Model("openai-3-small", "openai", "text-embedding-3-small", 100_000, 2048),
]}
VARIANTS = ("sentence", "title", "context")
SEARCH_MODEL = "voyage-context-4"     # sunucunun anlamsal araması (Aşama 8'deki karşılaştırmayla seçildi)


class EmbeddingError(RuntimeError):
    pass


class TooLarge(EmbeddingError):
    """İstek sağlayıcının token sınırını aştı; daha küçük parçalarla yeniden denenir."""


# ---------------------------------------------------------------- sağlayıcılar

def _post(url: str, key_name: str, body: dict) -> dict:
    """JSON isteği; hız sınırında ve sunucu hatasında bekleyip yeniden dener."""
    key = os.environ.get(key_name)
    if not key:
        raise EmbeddingError(f"{key_name} is not set (project .env file or environment).")
    request = urllib.request.Request(url, data=json.dumps(body).encode(),
                                     headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    for attempt in range(RETRIES):
        try:
            with urllib.request.urlopen(request, timeout=300) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            detail = error.read().decode(errors="replace")[:500]
            if error.code == 400 and "token" in detail.lower():
                raise TooLarge(detail) from None
            if error.code not in (429, 500, 502, 503, 504) or attempt == RETRIES - 1:
                raise EmbeddingError(f"{error.code}: {detail}") from None
            wait = float(error.headers.get("retry-after") or 2 ** attempt)
        except (urllib.error.URLError, http.client.HTTPException, ConnectionError, TimeoutError) as error:
            if attempt == RETRIES - 1:
                raise EmbeddingError(str(error)) from None
            wait = 2 ** attempt
        time.sleep(min(wait, 60))
    raise AssertionError("ulaşılmaz")


def embed_texts(model: Model, texts: list[str], kind: str) -> tuple[np.ndarray, int]:
    """Metinlerin vektörleri ve harcanan token. `kind`: "document" ya da "query"."""
    if model.provider == "voyage":
        body = {"input": texts, "model": model.api_name, "input_type": kind}
        if model.dimensions:
            body["output_dimension"] = model.dimensions
        result = _post("https://api.voyageai.com/v1/embeddings", "VOYAGE_API_KEY", body)
    else:
        body = {"input": texts, "model": model.api_name}
        if model.dimensions:
            body["dimensions"] = model.dimensions
        result = _post("https://api.openai.com/v1/embeddings", "OPENAI_API_KEY", body)
    rows = sorted(result["data"], key=lambda d: d["index"])
    return np.array([r["embedding"] for r in rows], dtype=np.float32), result["usage"]["total_tokens"]


def embed_documents(model: Model, documents: list[list[str]]) -> tuple[list[np.ndarray], int]:
    """Bağlamlı model: her belgenin parçalarının vektörleri (belge sırasıyla) ve harcanan token."""
    body = {"inputs": documents, "model": model.api_name, "input_type": "document"}
    if model.dimensions:
        body["output_dimension"] = model.dimensions
    if model.int8:
        body["output_dtype"] = "int8"
    result = _post("https://api.voyageai.com/v1/contextualizedembeddings", "VOYAGE_API_KEY", body)
    out = [None] * len(documents)
    for doc in result["data"]:
        chunks = sorted(doc["data"], key=lambda d: d["index"])
        out[doc["index"]] = np.array([c["embedding"] for c in chunks], dtype=np.float32)
    return out, result["usage"]["total_tokens"]


def embed_query(model: Model, query: str) -> np.ndarray:
    if model.contextual:
        body = {"inputs": [[query]], "model": model.api_name, "input_type": "query"}
        if model.dimensions:
            body["output_dimension"] = model.dimensions
        result = _post("https://api.voyageai.com/v1/contextualizedembeddings", "VOYAGE_API_KEY", body)
        vector = np.array(result["data"][0]["data"][0]["embedding"], dtype=np.float32)
    else:
        vector = embed_texts(model, [query], "query")[0][0]
    return _unit(vector)


def _unit(vectors: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(vectors, axis=-1, keepdims=True)
    return vectors / np.where(norms == 0, 1, norms)


# ---------------------------------------------------------------- birimler

@dataclass
class Unit:
    key: str
    text: str
    sentences: list[tuple[str, str]] = field(default_factory=list)   # (cümle, düğüm)


def _sha(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]


def units(conn: sqlite3.Connection, variant: str) -> list[Unit]:
    """Vektörü çıkarılacak birimler, kitap sırasıyla. `context`te bir belgenin birimleri art arda gelir."""
    rows = conn.execute("SELECT s.id, s.node_id, s.hash, s.text, n.ref FROM sentences s"
                        " JOIN nodes n ON n.id = s.node_id ORDER BY s.seq").fetchall()
    if variant == "context":
        return [u for document in documents(rows) for u in document]
    out: dict[str, Unit] = {}
    for sentence_id, node_id, hash_, text, ref in rows:
        if variant == "sentence":
            key, embedded = hash_, text
        else:
            embedded = f"{ref}\n{text}"
            key = _sha(embedded)
        out.setdefault(key, Unit(key, embedded)).sentences.append((sentence_id, node_id))
    return list(out.values())


def documents(rows: list) -> list[list[Unit]]:
    """Bağlamlı model için belgeler: bir bölümün kendi cümleleri, `DOCUMENT_TOKENS`'ı aşmayan ardışık parçalar.
    Birimin anahtarı belgenin metninden ve cümlenin sırasından gelir."""
    groups: list[list] = []
    for row in rows:
        if not groups or groups[-1][-1][1] != row[1] or _tokens([r[3] for r in groups[-1]] + [row[3]]) > DOCUMENT_TOKENS:
            groups.append([])
        groups[-1].append(row)
    out = []
    for group in groups:
        digest = _sha("\n".join(r[3] for r in group))
        out.append([Unit(f"{digest}:{i}", r[3], [(r[0], r[1])]) for i, r in enumerate(group)])
    return out


def _tokens(texts: list[str]) -> int:
    return int(sum(len(t) for t in texts) / CHARS_PER_TOKEN) + 4 * len(texts)


# ---------------------------------------------------------------- depo

class VectorStore:
    """Anahtar → vektör. Diskte `.npy` (float16 birim vektör ya da sağlayıcının int8 vektörü) ve `.keys.json`.
    Benzerlik kosinüstür; int8 vektörlerin uzunluğu bir kez hesaplanır."""

    BLOCK = 16_384           # puanlar bu kadar satırlık bloklarla hesaplanır (geçici bellek küçük kalır)

    def __init__(self, model: str, variant: str, directory: Path | None = None, dtype=np.float16) -> None:
        directory = directory or VECTORS_DIR
        self.path = directory / f"{model}.{variant}.npy"
        self.keys_path = directory / f"{model}.{variant}.keys.json"
        self.keys: list[str] = []
        self.vectors = np.zeros((0, 0), dtype=dtype)
        if self.path.exists():
            self.keys = json.loads(self.keys_path.read_text(encoding="utf-8"))
            self.vectors = np.load(self.path)
        self.dtype = self.vectors.dtype
        self.index = {k: i for i, k in enumerate(self.keys)}
        self._pending: list[np.ndarray] = []
        self._norms: np.ndarray | None = None

    def __contains__(self, key: str) -> bool:
        return key in self.index

    def add(self, keys: list[str], vectors: np.ndarray) -> None:
        for k in keys:
            self.index[k] = len(self.keys)
            self.keys.append(k)
        self._pending.append(vectors.astype(np.int8) if self.dtype == np.int8 else _unit(vectors).astype(self.dtype))

    def save(self) -> None:
        if not self._pending:
            return
        new = np.concatenate(self._pending)
        self.vectors = new if self.vectors.size == 0 else np.concatenate([self.vectors, new])
        self._pending = []
        self._write()

    def _write(self) -> None:
        self._norms = None
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp.npy")
        np.save(tmp, self.vectors)
        self.keys_path.write_text(json.dumps(self.keys), encoding="utf-8")
        tmp.replace(self.path)

    def keep(self, keys: set[str]) -> int:
        """Yalnızca `keys`'teki vektörler kalır, her anahtardan bir tane (metni değişmiş birimlerin eski
        vektörleri silinir)."""
        self.save()
        seen: set[str] = set()
        rows = [i for i, k in enumerate(self.keys) if k in keys and not (k in seen or seen.add(k))]
        removed = len(self.keys) - len(rows)
        if removed:
            self.keys = [self.keys[i] for i in rows]
            self.vectors = self.vectors[rows]
            self.index = {k: i for i, k in enumerate(self.keys)}
            self._write()
        return removed

    def scores(self, query: np.ndarray) -> np.ndarray:
        """Her satırın sorguyla kosinüs benzerliği."""
        query = _unit(query.astype(np.float32))
        out = np.concatenate([self.vectors[i:i + self.BLOCK].astype(np.float32) @ query
                              for i in range(0, len(self.vectors), self.BLOCK)])
        if self.dtype == np.int8:
            if self._norms is None:
                self._norms = np.concatenate([np.linalg.norm(self.vectors[i:i + self.BLOCK].astype(np.float32), axis=1)
                                              for i in range(0, len(self.vectors), self.BLOCK)])
            out /= np.where(self._norms == 0, 1, self._norms)
        return out

    def nearest(self, query: np.ndarray, keys: list[str], k: int) -> list[tuple[str, float]]:
        """`keys` arasından sorguya en yakın k birim."""
        rows = np.array([self.index[key] for key in keys if key in self.index])
        scores = self.scores(query)[rows]
        top = np.argsort(-scores)[:k]
        return [(self.keys[rows[i]], float(scores[i])) for i in top]


# ---------------------------------------------------------------- vektör çıkarma

def _batches(items: list[Unit], model: Model) -> Iterator[list[Unit]]:
    budget = int(model.max_tokens * 0.6)
    batch: list[Unit] = []
    for unit in items:
        if batch and (len(batch) >= model.max_items or _tokens([u.text for u in batch + [unit]]) > budget):
            yield batch
            batch = []
        batch.append(unit)
    if batch:
        yield batch


def _embed_units(model: Model, batch: list[Unit]) -> tuple[list[str], np.ndarray, int]:
    """Bir parti; sağlayıcı fazla büyük bulursa ikiye bölünür."""
    try:
        vectors, tokens = embed_texts(model, [u.text for u in batch], "document")
        return [u.key for u in batch], vectors, tokens
    except TooLarge:
        if len(batch) == 1:
            raise
        half = len(batch) // 2
        a, b = _embed_units(model, batch[:half]), _embed_units(model, batch[half:])
        return a[0] + b[0], np.concatenate([a[1], b[1]]), a[2] + b[2]


def _document_batches(docs: list[list[Unit]], model: Model) -> Iterator[list[list[Unit]]]:
    budget = int(model.max_tokens * 0.6)
    batch: list[list[Unit]] = []
    for doc in docs:
        texts = [u.text for d in batch + [doc] for u in d]
        if batch and (len(batch) >= model.max_items or _tokens(texts) > budget):
            yield batch
            batch = []
        batch.append(doc)
    if batch:
        yield batch


def build(model: Model, variant: str, conn: sqlite3.Connection) -> VectorStore:
    """Depoda olmayan birimlerin vektörlerini çıkarır; artık hiçbir birime ait olmayanları siler."""
    if (variant == "context") != model.contextual:
        raise EmbeddingError("`context` yalnızca bağlamlı modellerle, bağlamlı modeller yalnızca `context` ile.")
    store = VectorStore(model.name, variant, dtype=np.int8 if model.int8 else np.float16)
    current = units(conn, variant)
    if removed := store.keep({u.key for u in current}):
        print(f"{model.name}.{variant}: artık ya da tekrar eden {removed} vektör silindi", flush=True)
    todo = list({u.key: u for u in current if u.key not in store}.values())   # aynı metinli bölümler bir kez
    print(f"{model.name}.{variant}: {len(store.keys)} vektör var, {len(todo)} eksik", flush=True)
    started, spent, done = time.monotonic(), 0, 0
    if model.contextual:
        docs, current = [], None
        for unit in todo:                                  # belgeler art arda gelir
            digest = unit.key.split(":")[0]
            if digest != current:
                docs.append([])
                current = digest
            docs[-1].append(unit)
        batches = (([u for d in b for u in d], b) for b in _document_batches(docs, model))
    else:
        batches = ((b, None) for b in _batches(todo, model))
    for n, (batch, docs_batch) in enumerate(batches, 1):
        if docs_batch is not None:
            vectors, tokens = embed_documents(model, [[u.text for u in d] for d in docs_batch])
            store.add([u.key for u in batch], np.concatenate(vectors))
        else:
            keys, vectors, tokens = _embed_units(model, batch)
            store.add(keys, vectors)
        spent += tokens
        done += len(batch)
        if n % SAVE_EVERY == 0:
            store.save()
            elapsed = time.monotonic() - started
            print(f"  {done}/{len(todo)} · {spent / 1e6:.2f} M token · {elapsed:.0f} sn", flush=True)
    store.save()
    print(f"bitti: {done} vektör, {spent / 1e6:.2f} M token, {time.monotonic() - started:.0f} sn", flush=True)
    return store


def missing(conn: sqlite3.Connection, model_name: str = SEARCH_MODEL) -> int:
    """Anlamsal aramada vektörü olmayan cümle sayısı (ayrıştırma metni değiştirdiyse)."""
    model = MODELS[model_name]
    variant = "context" if model.contextual else "sentence"
    keys_path = VECTORS_DIR / f"{model.name}.{variant}.keys.json"
    known = set(json.loads(keys_path.read_text(encoding="utf-8"))) if keys_path.exists() else set()
    return sum(len(u.sentences) for u in units(conn, variant) if u.key not in known)


# ---------------------------------------------------------------- sorgu önbelleği

def query_vector(model: Model, query: str) -> np.ndarray:
    """Sorgunun vektörü; değerlendirmede aynı soru için yeniden istek yapılmaz."""
    path = VECTORS_DIR / f"queries.{model.name}.json"
    cache = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    if query not in cache:
        cache[query] = embed_query(model, query).tolist()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    return np.array(cache[query], dtype=np.float32)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    build_parser = commands.add_parser("build", help="eksik vektörleri çıkar")
    build_parser.add_argument("model", choices=sorted(MODELS))
    build_parser.add_argument("--variant", choices=VARIANTS)
    commands.add_parser("status", help="depolar ve eksik vektörler")
    parser.add_argument("--db", type=Path, default=DB_PATH)
    args = parser.parse_args()
    load_env()
    conn = connect(args.db)
    if args.command == "build":
        model = MODELS[args.model]
        variant = args.variant or ("context" if model.contextual else "sentence")
        try:
            build(model, variant, conn)
        except EmbeddingError as error:
            sys.exit(str(error))
    else:
        for path in sorted(VECTORS_DIR.glob("*.npy")):
            name, variant = path.stem.split(".")
            store = VectorStore(name, variant)
            missing = sum(u.key not in store for u in units(conn, variant))
            print(f"{path.relative_to(ROOT)}: {len(store.keys)} vektör, {missing} eksik")


if __name__ == "__main__":
    main()
