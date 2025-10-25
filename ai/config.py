"""Configuration management for AI service."""
import os
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings."""
    
    # Ollama Configuration
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
    ollama_timeout: int = int(os.getenv("OLLAMA_TIMEOUT", "300"))
    ollama_max_tokens: int = int(os.getenv("OLLAMA_MAX_TOKENS", "4096"))
    
    # API Configuration
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8001"))
    api_reload: bool = os.getenv("API_RELOAD", "True").lower() == "true"
    
    # Security
    api_key_secret: str = os.getenv("API_KEY_SECRET", "dev-secret-key")
    cors_origins: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: str = os.getenv("LOG_FILE", "ai_service.log")
    
    # Cache Configuration
    enable_cache: bool = os.getenv("ENABLE_CACHE", "True").lower() == "true"
    cache_ttl: int = int(os.getenv("CACHE_TTL", "3600"))
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = int(os.getenv("REDIS_PORT", "6379"))
    redis_db: int = int(os.getenv("REDIS_DB", "0"))
    
    # Rate Limiting
    rate_limit_per_user: int = int(os.getenv("RATE_LIMIT_PER_USER", "100"))
    rate_limit_window: int = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))
    
    ai_database_url: str = os.getenv(
        "AI_DATABASE_URL",
        "postgresql://ai_user:ai_password@localhost:5432/dramallama_ai"
    )
    class Config:
        env_file = ".env"


settings = Settings()

