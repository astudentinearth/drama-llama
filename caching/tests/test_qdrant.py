"""Tests for Qdrant client service."""
import pytest
from services.qdrant_client import QdrantClientService
from models.schemas import Material


@pytest.fixture
def qdrant_service():
    """Create Qdrant service instance."""
    service = QdrantClientService()
    try:
        service.connect()
        service.create_collection()
        yield service
    except Exception as e:
        pytest.skip(f"Qdrant not available: {e}")


def test_connection(qdrant_service):
    """Test Qdrant connection."""
    assert qdrant_service.is_connected()


def test_store_and_retrieve(qdrant_service):
    """Test storing and retrieving a material."""
    material = Material(
        title="Test Material",
        content="This is test content for learning Python.",
        metadata={"category": "programming", "difficulty": "beginner"}
    )
    
    # Create dummy embedding
    embedding = [0.1] * 384
    
    # Store material
    material_id = qdrant_service.store_material(material, embedding)
    assert material_id is not None
    
    # Retrieve material
    retrieved = qdrant_service.get_material(material_id)
    assert retrieved is not None
    assert retrieved.title == material.title
    assert retrieved.content == material.content


def test_search_similar(qdrant_service):
    """Test searching similar materials."""
    # Store test materials
    materials = [
        Material(
            title="Python Tutorial",
            content="Learn Python programming",
            metadata={"category": "python"}
        ),
        Material(
            title="JavaScript Guide",
            content="Learn JavaScript programming",
            metadata={"category": "javascript"}
        )
    ]
    
    for material in materials:
        embedding = [0.1] * 384
        qdrant_service.store_material(material, embedding)
    
    # Search with similar embedding
    query_embedding = [0.1] * 384
    results = qdrant_service.search_similar(
        query_embedding=query_embedding,
        limit=5,
        score_threshold=0.5
    )
    
    assert len(results) > 0
    assert all(hasattr(r, 'material') for r in results)
    assert all(hasattr(r, 'similarity_score') for r in results)


def test_delete_material(qdrant_service):
    """Test deleting a material."""
    material = Material(
        title="To Delete",
        content="This material will be deleted",
        metadata={}
    )
    
    embedding = [0.1] * 384
    material_id = qdrant_service.store_material(material, embedding)
    
    # Delete material
    success = qdrant_service.delete_material(material_id)
    assert success
    
    # Verify deletion
    retrieved = qdrant_service.get_material(material_id)
    assert retrieved is None


def test_collection_stats(qdrant_service):
    """Test getting collection statistics."""
    stats = qdrant_service.get_collection_stats()
    
    assert "collection_name" in stats
    assert "total_materials" in stats
    assert "vector_size" in stats
    assert stats["vector_size"] == 384

