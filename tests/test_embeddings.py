"""Aşama 8: cümle vektörleri. Sağlayıcılar sahte bir işlevle değiştirilir; ağa çıkılmaz."""

import numpy as np
import pytest

from risale_mcp import embeddings
from risale_mcp.db import connect
from risale_mcp.search_eval import rrf


@pytest.fixture
def conn(small_db):
    return connect(small_db[0])


@pytest.fixture
def fake_provider(monkeypatch, tmp_path):
    """Her metne kelimelerinden türeyen bir vektör verir; çağrıları sayar."""
    calls = []

    def vector(text: str) -> np.ndarray:
        v = np.zeros(8, dtype=np.float32)
        for word in text.lower().split():
            v[hash(word) % 8] += 1
        return v

    def embed_texts(model, texts, kind):
        calls.append(len(texts))
        return np.array([vector(t) for t in texts]), 10 * len(texts)

    monkeypatch.setattr(embeddings, "embed_texts", embed_texts)
    monkeypatch.setattr(embeddings, "VECTORS_DIR", tmp_path)
    return calls


def test_units_share_vectors_for_identical_sentences_and_carry_their_context(conn):
    (shared,) = embeddings.units(conn, "sentence")          # örnek veride bütün cümlelerin özeti aynı
    assert shared.key == "0" * 12 and len(shared.sentences) == 6
    title = {u.text for u in embeddings.units(conn, "title")}
    assert "Sözler › Onuncu Söz › Birinci Hakikat\nKıyâmet ve mîzan günü gelecek." in title
    context = embeddings.units(conn, "context")
    assert [u.key.split(":")[1] for u in context[:3]] == ["0", "1", "2"]      # Onuncu Söz'ün üç cümlesi bir belge
    assert len({u.key.split(":")[0] for u in context}) == 4


def test_build_embeds_only_missing_units_and_survives_reload(conn, fake_provider):
    model = embeddings.MODELS["openai-3-small"]
    store = embeddings.build(model, "title", conn)
    assert len(store.keys) == 6 and store.vectors.dtype == np.float16
    assert np.allclose(np.linalg.norm(store.vectors.astype(np.float32), axis=1), 1, atol=1e-3)
    calls = len(fake_provider)
    again = embeddings.build(model, "title", conn)
    assert len(fake_provider) == calls and again.keys == store.keys       # hepsi depoda: istek yok


def test_nearest_ranks_by_cosine_similarity(tmp_path):
    store = embeddings.VectorStore("m", "sentence", tmp_path)
    store.add(["a", "b", "c"], np.array([[1, 0], [0.8, 0.6], [0, 1]], dtype=np.float32))
    store.save()
    reloaded = embeddings.VectorStore("m", "sentence", tmp_path)
    assert [k for k, _ in reloaded.nearest(np.array([1, 0.1]), ["a", "b", "c"], 2)] == ["a", "b"]
    assert [k for k, _ in reloaded.nearest(np.array([1, 0.1]), ["b", "c"], 5)] == ["b", "c"]


def test_contextual_model_only_with_context_variant(conn):
    with pytest.raises(embeddings.EmbeddingError):
        embeddings.build(embeddings.MODELS["voyage-context-4"], "sentence", conn)


def test_rrf_rewards_hits_found_by_both_searches():
    a, b, c = ("s1", "n1"), ("s2", "n2"), ("s3", "n3")
    assert rrf([[a, b], [c, b]])[0] == b
