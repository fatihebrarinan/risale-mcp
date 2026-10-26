"""Aşama 8: anlamsal arama (sunucunun çalışma anı).

Cümle vektörleri `embeddings.py` ile çıkarılır; burada yalnızca okunur. Sorgunun vektörü her aramada
sağlayıcıdan alınır (aynı sorgu bellekte önbelleğe alınır), benzerlik yerelde hesaplanır.

- Sonuçlar: sorguya anlamca en yakın cümleler (kosinüs benzerliği), eser ya da gruba göre süzülebilir.
- Bölümler: en yakın `POOL` cümle kendi bölümüne ve üst bölümlerine puan verir (her bölüme en çok
  `PER_SECTION` cümle); en yüksek puanlı bölümler konunun yoğunlaştığı yerlerdir. Değerlendirmede
  asıl işlendiği yeri cümlelerden daha iyi buldu.
- Vektörü olmayan cümleler (ayrıştırma sonrası değişmiş ya da yeni metin) aranmaz; sayıları
  `unindexed`'dadır. `embeddings build` ile tamamlanır.
"""

import sqlite3
from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np

from risale_mcp import embeddings

POOL = 300           # bölüm puanına katılan en yakın cümle sayısı
PER_SECTION = 5      # bir bölüme puan verebilecek en çok cümle
SECTIONS = 5         # sonuçta gösterilen bölüm sayısı


class SemanticUnavailable(RuntimeError):
    pass


@dataclass(frozen=True)
class Hit:
    sentence_id: str
    node_id: str
    work: str
    score: float


@dataclass(frozen=True)
class SectionHit:
    node_id: str
    score: float
    matches: int


@lru_cache(maxsize=512)
def _query_vector(model_name: str, query: str) -> np.ndarray:
    return embeddings.embed_query(embeddings.MODELS[model_name], query)


class SemanticIndex:
    """Bir veritabanı bağlantısı için vektör deposu ile cümleler arasındaki eşleme."""

    def __init__(self, conn: sqlite3.Connection, model_name: str = embeddings.SEARCH_MODEL,
                 directory: Path | None = None) -> None:
        self.model = embeddings.MODELS[model_name]
        variant = "context" if self.model.contextual else "sentence"
        self.store = embeddings.VectorStore(self.model.name, variant, directory)
        if not self.store.keys:
            raise SemanticUnavailable(f"no vectors for {self.model.name}")
        rows, self.sentences = [], []
        self.unindexed = 0
        for unit in embeddings.units(conn, variant):
            row = self.store.index.get(unit.key)
            if row is None:
                self.unindexed += len(unit.sentences)
                continue
            for sentence in unit.sentences:
                rows.append(row)
                self.sentences.append(sentence)
        self.rows = np.array(rows)
        work_of = {n: w for n, w in conn.execute("SELECT id, work FROM nodes")}
        self.works = np.array([work_of[node] for _, node in self.sentences])
        self.parent = {n: (p, d) for n, p, d in conn.execute("SELECT id, parent_id, depth FROM nodes")}

    def search(self, query: str, works: set[str] | None = None, limit: int = 10,
               offset: int = 0) -> tuple[list[Hit], list[SectionHit]]:
        """En yakın cümleler (`offset`ten itibaren `limit` tane) ve konunun yoğunlaştığı bölümler."""
        scores = self.store.scores(self.query_vector(query))[self.rows]
        candidates = np.flatnonzero(np.isin(self.works, list(works))) if works else np.arange(len(scores))
        wanted = min(len(candidates), max(offset + limit, POOL))
        top = candidates[np.argpartition(-scores[candidates], wanted - 1)[:wanted]] if wanted else candidates[:0]
        top = top[np.argsort(-scores[top])]
        hits = [Hit(*self.sentences[i], str(self.works[i]), float(scores[i])) for i in top]
        return hits[offset:offset + limit], self._sections(hits[:POOL])

    def query_vector(self, query: str) -> np.ndarray:
        return _query_vector(self.model.name, query)

    def _sections(self, hits: list[Hit]) -> list[SectionHit]:
        score, count = defaultdict(float), defaultdict(int)
        for hit in hits:
            node = hit.node_id
            while node and self.parent[node][1] >= 1:      # eserin kendisi (kök) sayılmaz
                if count[node] < PER_SECTION:
                    score[node] += hit.score
                    count[node] += 1
                node = self.parent[node][0]
        best = sorted(score, key=lambda n: -score[n])[:SECTIONS]
        return [SectionHit(n, score[n], count[n]) for n in best]
