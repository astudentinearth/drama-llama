"""
Ollama health check tests.
Run these before integration tests to ensure Ollama is accessible.

Usage:
    pytest tests/test_ollama_health.py -v -s
"""
import pytest
from ollama import AsyncClient
from config import settings


@pytest.mark.integration
@pytest.mark.asyncio
class TestOllamaHealth:
    """Health check tests for Ollama service."""
    
    async def test_ollama_connection(self):
        """Test basic connectivity to Ollama."""
        client = AsyncClient(host=settings.ollama_host)
        
        response = await client.chat(
            model=settings.ollama_model,
            messages=[{"role": "user", "content": "Say 'Hello' and nothing else."}],
            options={"temperature": 0.1}
        )
        
        # Extract response content
        if hasattr(response, 'message'):
            content = response.message.content if hasattr(response.message, 'content') else str(response.message)
        else:
            content = response.get("message", {}).get("content", "")
        
        assert content is not None
        assert len(content) > 0
    
    async def test_model_availability(self):
        """Test if the configured model is available."""
        client = AsyncClient(host=settings.ollama_host)
        
        # Try to use the model with minimal generation
        response = await client.chat(
            model=settings.ollama_model,
            messages=[{"role": "user", "content": "Test"}],
            options={"num_predict": 1}  # Only generate 1 token
        )
        
        assert response is not None
    
    async def test_ollama_with_json_format(self):
        """Test Ollama's ability to generate structured JSON output."""
        client = AsyncClient(host=settings.ollama_host)
        
        schema = {
            "type": "object",
            "properties": {
                "message": {"type": "string"}
            },
            "required": ["message"]
        }
        
        response = await client.chat(
            model=settings.ollama_model,
            messages=[{
                "role": "user", 
                "content": "Respond with a JSON object containing a message field with value 'test successful'"
            }],
            format=schema,
            options={"temperature": 0.1}
        )
        
        if hasattr(response, 'message'):
            content = response.message.content if hasattr(response.message, 'content') else str(response.message)
        else:
            content = response.get("message", {}).get("content", "")
        
        assert content is not None
        assert len(content) > 0

