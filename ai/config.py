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
    
    # GROQ API
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    # Note: Only certain models support json_schema structured outputs
    # Supported models: llama-3.1-70b-versatile, llama-3.1-8b-instant, gemma2-9b-it
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
    groq_max_tokens: int = int(os.getenv("GROQ_MAX_TOKENS", "4096"))
    groq_temperature: float = float(os.getenv("GROQ_TEMPERATURE", "0.1"))
    groq_timeout: int = int(os.getenv("GROQ_TIMEOUT", "60"))

    # API Configuration
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8001"))
    api_reload: bool = os.getenv("API_RELOAD", "True").lower() == "true"
    
    # Security
    api_key_secret: str = os.getenv("API_KEY_SECRET", "dev-secret-key")
    cors_origins: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Database
    ai_database_url: str = os.getenv(
        "AI_DATABASE_URL",
        "postgresql://ai_user:ai_password@localhost:5432/dramallama_ai"
    )
    class Config:
        env_file = ".env"


settings = Settings()

