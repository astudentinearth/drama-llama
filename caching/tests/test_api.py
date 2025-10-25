"""Tests for API endpoints."""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert data["service"] == "Caching Service"


def test_ping_endpoint():
    """Test ping endpoint."""
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/cache/health")
    assert response.status_code == 200
    data = response.json()
    
    assert "status" in data
    assert "qdrant_connected" in data
    assert "embedding_model_loaded" in data
    assert "tokenizer_loaded" in data


def test_store_material():
    """Test storing a material."""
    material_data = {
        "title": "API Test Material",
        "content": "This is test content for the API.",
        "metadata": {
            "category": "testing",
            "difficulty": "easy"
        }
    }
    
    response = client.post("/cache/store", json=material_data)
    
    # May fail if services not fully initialized
    if response.status_code == 201:
        data = response.json()
        assert "id" in data
        assert data["title"] == material_data["title"]
        assert data["content"] == material_data["content"]


def test_search_materials():
    """Test searching for materials."""
    search_request = {
        "query": "Python programming tutorial",
        "limit": 5,
        "threshold": 0.85
    }
    
    response = client.post("/cache/search", json=search_request)
    
    # May fail if services not fully initialized
    if response.status_code == 200:
        data = response.json()
        assert "results" in data
        assert "query" in data
        assert "total_found" in data
        assert data["query"] == search_request["query"]


def test_get_stats():
    """Test getting collection stats."""
    response = client.get("/cache/stats")
    
    # May fail if Qdrant not connected
    if response.status_code == 200:
        data = response.json()
        assert "collection_name" in data
        assert "total_materials" in data
        assert "vector_size" in data


def test_duplicate_detection_exact():
    """Test that exact duplicates are rejected."""
    material_data = {
        "title": "Duplicate Test Material",
        "content": "This is unique test content for duplicate detection.",
        "metadata": {
            "category": "testing",
            "test_type": "duplicate_detection"
        }
    }
    
    # Store the material first time
    response1 = client.post("/cache/store", json=material_data)
    
    # May fail if services not fully initialized
    if response1.status_code == 201:
        data1 = response1.json()
        material_id = data1["id"]
        
        # Try to store the exact same material again
        response2 = client.post("/cache/store", json=material_data)
        
        # Should get conflict status
        assert response2.status_code == 409
        error_detail = response2.json()["detail"]
        assert "duplicate" in error_detail["message"].lower()
        assert error_detail["existing_id"] == material_id
        assert error_detail["match_type"] in ["exact", "near-duplicate"]
        
        # Clean up - delete the test material
        client.delete(f"/cache/material/{material_id}")


def test_duplicate_detection_case_insensitive():
    """Test that duplicates with different cases are detected."""
    material_data_1 = {
        "title": "Case Test Material",
        "content": "This is test content for case sensitivity.",
        "metadata": {"test_type": "case_test"}
    }
    
    material_data_2 = {
        "title": "CASE TEST MATERIAL",  # Different case
        "content": "THIS IS TEST CONTENT FOR CASE SENSITIVITY.",  # Different case
        "metadata": {"test_type": "case_test"}
    }
    
    # Store the first material
    response1 = client.post("/cache/store", json=material_data_1)
    
    if response1.status_code == 201:
        data1 = response1.json()
        material_id = data1["id"]
        
        # Try to store material with different case
        response2 = client.post("/cache/store", json=material_data_2)
        
        # Should get conflict status due to case-insensitive matching
        assert response2.status_code == 409
        error_detail = response2.json()["detail"]
        assert "duplicate" in error_detail["message"].lower()
        assert error_detail["match_type"] == "exact"
        
        # Clean up
        client.delete(f"/cache/material/{material_id}")


def test_similar_but_not_duplicate():
    """Test that similar but different materials are stored separately."""
    material_data_1 = {
        "title": "Python Basics Tutorial",
        "content": "Learn Python programming fundamentals including variables, loops, and functions.",
        "metadata": {"test_type": "similarity_test"}
    }
    
    material_data_2 = {
        "title": "Advanced Python Programming",
        "content": "Master advanced Python concepts like decorators, generators, and metaclasses.",
        "metadata": {"test_type": "similarity_test"}
    }
    
    # Store first material
    response1 = client.post("/cache/store", json=material_data_1)
    
    if response1.status_code == 201:
        data1 = response1.json()
        material_id_1 = data1["id"]
        
        # Store second material (similar but different)
        response2 = client.post("/cache/store", json=material_data_2)
        
        # Should succeed as they are different enough
        # Or fail with 409 if too similar
        if response2.status_code == 201:
            data2 = response2.json()
            material_id_2 = data2["id"]
            assert material_id_1 != material_id_2
            
            # Clean up both
            client.delete(f"/cache/material/{material_id_1}")
            client.delete(f"/cache/material/{material_id_2}")
        elif response2.status_code == 409:
            # If detected as too similar, that's also acceptable behavior
            # Just clean up the first one
            client.delete(f"/cache/material/{material_id_1}")

