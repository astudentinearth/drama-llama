"""Configuration management for caching service."""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Caching service settings."""
    
    # Qdrant Configuration
    qdrant_host: str = os.getenv("QDRANT_HOST", "localhost")
    qdrant_port: int = int(os.getenv("QDRANT_PORT", "6333"))
    qdrant_collection: str = os.getenv("QDRANT_COLLECTION", "learning_materials")
    qdrant_grpc_port: int = int(os.getenv("QDRANT_GRPC_PORT", "6334"))
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")  # Optional: for Qdrant Cloud or secured instances
    qdrant_url: str = os.getenv("QDRANT_URL", "")  # Optional: full URL for Qdrant Cloud (e.g., https://xxx.cloud.qdrant.io)
    qdrant_use_https: bool = os.getenv("QDRANT_USE_HTTPS", "False").lower() == "true"
    
    # Model Configuration
    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL", 
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # Vector Configuration
    vector_size: int = int(os.getenv("VECTOR_SIZE", "384"))  # all-MiniLM-L6-v2 dimension
    similarity_threshold: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.85"))
    
    # API Configuration
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8002"))
    api_title: str = "Caching Service API"
    api_version: str = "1.0.0"
    
    # Search Configuration
    max_search_results: int = int(os.getenv("MAX_SEARCH_RESULTS", "10"))
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
        
    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra environment variables


settings = Settings()

