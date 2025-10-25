"""Pydantic schemas for caching service."""
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime


class Material(BaseModel):
    """Base material model."""
    title: str = Field(..., description="Title of the learning material")
    content: str = Field(..., description="Full content of the material")
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional metadata (category, difficulty, tags, etc.)"
    )


class MaterialCreate(Material):
    """Material creation request."""
    pass


class MaterialResponse(Material):
    """Material response with ID and timestamp."""
    id: str = Field(..., description="Unique identifier for the material")
    timestamp: datetime = Field(..., description="Creation timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Python Django REST API Tutorial",
                "content": "Complete guide to building REST APIs with Django...",
                "metadata": {
                    "category": "web_development",
                    "difficulty": "intermediate",
                    "tags": ["python", "django", "rest", "api"]
                },
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class SearchRequest(BaseModel):
    """Search request model."""
    query: str = Field(..., description="Search query text")
    limit: int = Field(default=10, ge=1, le=100, description="Maximum number of results")
    threshold: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Similarity threshold override (default: 0.85)"
    )
    filters: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Metadata filters (e.g., category, difficulty)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "Python Django REST API tutorial",
                "limit": 5,
                "threshold": 0.85,
                "filters": {"category": "web_development"}
            }
        }


class SearchResult(BaseModel):
    """Single search result with similarity score."""
    material: MaterialResponse
    similarity_score: float = Field(..., description="Cosine similarity score (0-1)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "material": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "title": "Python Django REST API Tutorial",
                    "content": "Complete guide...",
                    "metadata": {"category": "web_development"},
                    "timestamp": "2024-01-15T10:30:00Z"
                },
                "similarity_score": 0.92
            }
        }


class SearchResponse(BaseModel):
    """Search response with multiple results."""
    results: List[SearchResult]
    query: str
    total_found: int
    threshold_used: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "results": [],
                "query": "Python Django REST API tutorial",
                "total_found": 3,
                "threshold_used": 0.85
            }
        }


class CacheStats(BaseModel):
    """Collection statistics."""
    collection_name: str
    total_materials: int
    vector_size: int
    indexed: bool
    
    class Config:
        json_schema_extra = {
            "example": {
                "collection_name": "learning_materials",
                "total_materials": 1250,
                "vector_size": 384,
                "indexed": True
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service status (healthy/unhealthy)")
    qdrant_connected: bool = Field(..., description="Qdrant connection status")
    embedding_model_loaded: bool = Field(..., description="Embedding model status")
    tokenizer_loaded: bool = Field(..., description="Tokenizer status")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional details")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "qdrant_connected": True,
                "embedding_model_loaded": True,
                "tokenizer_loaded": True,
                "details": {
                    "qdrant_version": "1.7.0",
                    "collection_exists": True
                }
            }
        }

