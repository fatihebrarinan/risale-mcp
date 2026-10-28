"""Aşama 8: anlamsal arama (çalışma anı). Vektörler sahte bir sağlayıcıyla çıkarılır; ağa çıkılmaz.

Sahte vektör kelime sayımıdır: sorgu ile cümle ortak kelimeleri kadar yakındır. Böylece sıralama
elle öngörülebilir.
"""

import json

import numpy as np
import pytest
from mcp import Client

from risale_mcp import embeddings, semantic
from risale_mcp.db import connect
from risale_mcp.library import Library, LibraryError
from risale_mcp.normalize import search_words
from risale_mcp.server import create_server

pytestmark = pytest.mark.anyio
WORDS = ["haşr", "kıyâmet", "mîzan", "ışık", "bakara", "mecmûa", "allah", "geldi"]


def fake_vector(text: str) -> np.ndarray:
    words = search_words(text)
    return np.array([sum(w.startswith(search_words(k)[0]) for w in words) for k in WORDS], dtype=np.float32)


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def vectors(small_db, monkeypatch, tmp_path):
    """Örnek veritabanının vektörleri `tmp_path`'te; sorgu vektörü de sahte."""
    monkeypatch.setattr(embeddings, "VECTORS_DIR", tmp_path)
    monkeypatch.setattr(embeddings, "embed_documents",
                        lambda model, docs: ([np.array([fake_vector(t) * 10 for t in d]) for d in docs], 1))
    monkeypatch.setattr(embeddings, "embed_query", lambda model, query: fake_vector(query))
    semantic._query_vector.cache_clear()
    embeddings.build(embeddings.MODELS[embeddings.SEARCH_MODEL], "context", connect(small_db[0]))
    yield tmp_path
    semantic._query_vector.cache_clear()


@pytest.fixture
def library(small_db, vectors):
    lib = Library(small_db[0], vectors_dir=vectors)
    yield lib
    lib.close()


def test_store_holds_int8_vectors(vectors):
    store = embeddings.VectorStore(embeddings.SEARCH_MODEL, "context", vectors)
    assert store.dtype == np.int8 and len(store.keys) == 6


def test_closest_sentences_and_their_sections(library):
    result = library.semantic_search("kıyamet ve mizan")
    first = result["results"][0]
    assert first["id"] == "sozler/10/hakikat-01/c001" and first["similarity"] > 0.9
    assert first["cite_as"].endswith("› “Kıyâmet ve mîzan gün…”")
    assert "cite" in result["note"]
    assert [s["id"] for s in result["sections"]][:2] == ["sozler/10/hakikat-01", "sozler/10"]
    assert "unindexed_sentences" not in result


def test_filters_by_work_and_pages(library):
    assert {r["id"].split("/")[0] for r in library.semantic_search("haşir", work="asa-yi-musa")["results"]} == {"asa-yi-musa"}
    assert {r["id"].split("/")[0] for r in library.semantic_search("haşir", group="ana-cilt")["results"]} == {"sozler"}
    first, second = (library.semantic_search("haşir", limit=1, offset=i)["results"] for i in (0, 1))
    assert first != second and "sections" not in library.semantic_search("haşir", offset=1)
    with pytest.raises(LibraryError, match="Unknown group"):
        library.semantic_search("haşir", group="roman")


def test_sentences_without_vectors_are_reported(library, vectors):
    keys_path = vectors / f"{embeddings.SEARCH_MODEL}.context.keys.json"
    keys = json.loads(keys_path.read_text())
    keys[0] = "eski-anahtar"                       # bir cümlenin metni değişmiş gibi
    keys_path.write_text(json.dumps(keys))
    fresh = Library(library.path, vectors_dir=vectors)
    assert fresh.semantic_search("haşir")["unindexed_sentences"] == 1


def test_missing_vectors_give_a_readable_error(small_db, tmp_path):
    with pytest.raises(LibraryError, match="not available"):
        Library(small_db[0], vectors_dir=tmp_path).semantic_search("haşir")


async def test_server_tool(library):
    async with Client(create_server(library)) as client:
        result = await client.call_tool("semantic_search", {"query": "mecmûa haşir", "limit": 2})
        assert json.loads(result.content[0].text)["results"][0]["id"] == "asa-yi-musa/haşir/c001"
