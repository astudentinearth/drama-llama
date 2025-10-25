# Caching Service

A vector-based caching microservice for learning materials using Qdrant, sentence-transformers.

## Features

- **Semantic Search**: Find similar learning materials using vector similarity (cosine distance)
- **Intelligent Caching**: Store materials with automatic embedding generation
- **Threshold-Based Matching**: Configurable similarity threshold (default: 0.85)
- **Metadata Filtering**: Filter search results by category, difficulty, tags, etc.
- **RESTful API**: Clean FastAPI interface for integration

## Architecture

### Components

1. **Qdrant Vector Database**: Stores embeddings and full content
2. **Embedding Service**: Generates 384-dim vectors using `all-MiniLM-L6-v2` (handles tokenization internally)
3. **FastAPI Application**: REST API for cache operations

### Technology Stack

- **FastAPI**: Web framework
- **Qdrant**: Vector database
- **sentence-transformers**: Embedding generation
- **transformers**: Tokenization
- **Docker**: Containerization

## Quick Start

### Prerequisites

- Docker and Docker Compose
- 4GB+ RAM (for model loading)
- ~2GB disk space (for models and data)

### Installation

1. **Clone and navigate to caching directory**:
```bash
cd caching
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Create environment file**:
```bash
cp .env.example .env
```


4. **Start Qdrant separately**:
```bash
docker run -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant-data:/qdrant/storage qdrant/qdrant
```

5. **Run the application**:
```bash
uvicorn main:app --host 0.0.0.0 --port 8002
```


6. **Verify health**:
```bash
curl http://localhost:8002/cache/health
```

## API Documentation

### Endpoints

#### POST /cache/search
Search for similar materials using semantic similarity.

**Request**:
```json
{
  "query": "Python Django REST API tutorial",
  "limit": 5,
  "threshold": 0.85,
  "filters": {
    "category": "web_development"
  }
}
```

**Response**:
```json
{
  "results": [
    {
      "material": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Django REST Framework Guide",
        "content": "Complete tutorial...",
        "metadata": {
          "category": "web_development",
          "difficulty": "intermediate"
        },
        "timestamp": "2024-01-15T10:30:00Z"
      },
      "similarity_score": 0.92
    }
  ],
  "query": "Python Django REST API tutorial",
  "total_found": 1,
  "threshold_used": 0.85
}
```

#### POST /cache/store
Store a new learning material with automatic embedding.

**Request**:
```json
{
  "title": "Python Django REST API Tutorial",
  "content": "This comprehensive guide covers...",
  "metadata": {
    "category": "web_development",
    "difficulty": "intermediate",
    "tags": ["python", "django", "rest", "api"]
  }
}
```

**Response**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Python Django REST API Tutorial",
  "content": "This comprehensive guide covers...",
  "metadata": {
    "category": "web_development",
    "difficulty": "intermediate",
    "tags": ["python", "django", "rest", "api"]
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### GET /cache/material/{id}
Retrieve a specific material by ID.

#### DELETE /cache/material/{id}
Delete a material by ID.

#### GET /cache/health
Health check endpoint.

**Response**:
```json
{
    "status": "healthy",
    "qdrant_connected": true,
    "embedding_model_loaded": true,
    "tokenizer_loaded": false,
    "details": {
        "collection_exists": true,
        "total_materials": 150,
        "embedding_dimension": 384,
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2"
    }
}
```

#### GET /cache/stats
Get collection statistics.

**Response**:
```json
{
  "collection_name": "learning_materials",
  "total_materials": 150,
  "vector_size": 384,
  "indexed": true
}
```

## Configuration

Edit `.env` file or set environment variables:

```bash
# Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION=learning_materials

# Models
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
TOKENIZER_MODEL=meta-llama/Llama-4-Scout-17b-16e-instruct

# Search
SIMILARITY_THRESHOLD=0.85
MAX_SEARCH_RESULTS=10

# API
API_HOST=0.0.0.0
API_PORT=8002
```

## Integration with AI Service

The AI service (`/ai/utils/llm_tools.py`) can integrate with this caching service:

```python
import httpx

async def createLearningMaterials(things_to_learn: list[str]) -> str:
    # Search cache first
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8002/cache/search",
            json={
                "query": " ".join(things_to_learn),
                "limit": 5,
                "threshold": 0.85
            }
        )
        
        if response.status_code == 200:
            results = response.json()
            if results["total_found"] > 0:
                # Use cached materials
                return format_cached_materials(results["results"])
    
    # Generate new materials if not found
    materials = await generate_new_materials(things_to_learn)
    
    # Store in cache
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://localhost:8002/cache/store",
            json={
                "title": " ".join(things_to_learn),
                "content": materials,
                "metadata": {"type": "learning_materials"}
            }
        )
    
    return materials
```

## Testing

Run tests with pytest:

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_embedding.py
```


## Support

For issues and questions, please open an issue on GitHub.

