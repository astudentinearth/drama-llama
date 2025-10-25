"""Tests for embedding service."""
import pytest
from services.embedding_service import EmbeddingService


@pytest.fixture
def embedding_service():
    """Create embedding service instance."""
    service = EmbeddingService()
    service.load_model()
    return service


def test_model_loading(embedding_service):
    """Test that model loads successfully."""
    assert embedding_service.is_loaded()
    assert embedding_service.model is not None


def test_single_text_encoding(embedding_service):
    """Test encoding a single text."""
    text = "Python programming tutorial"
    embedding = embedding_service.encode_single(text)
    
    assert isinstance(embedding, list)
    assert len(embedding) == 384  # all-MiniLM-L6-v2 dimension
    assert all(isinstance(x, float) for x in embedding)


def test_batch_encoding(embedding_service):
    """Test encoding multiple texts."""
    texts = [
        "Python programming tutorial",
        "JavaScript web development",
        "Machine learning basics"
    ]
    embeddings = embedding_service.encode(texts)
    
    assert len(embeddings) == 3
    assert all(len(emb) == 384 for emb in embeddings)


def test_embedding_consistency(embedding_service):
    """Test that same text produces same embedding."""
    text = "Test consistency"
    
    embedding1 = embedding_service.encode_single(text)
    embedding2 = embedding_service.encode_single(text)
    
    assert embedding1 == embedding2


def test_embedding_dimension(embedding_service):
    """Test getting embedding dimension."""
    dimension = embedding_service.get_embedding_dimension()
    assert dimension == 384

