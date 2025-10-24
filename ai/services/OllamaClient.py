import asyncio
import logging
from typing import Dict, Any, Optional, AsyncGenerator
from ollama import AsyncClient
from config import settings

logger = logging.getLogger(__name__)


class OllamaClient:
    """Wrapper for Ollama API client with error handling and retry logic."""
    
    def __init__(self):
        self.client = AsyncClient(host=settings.ollama_host)
        self.model = settings.ollama_model
        self.max_tokens = settings.ollama_max_tokens
        self.timeout = settings.ollama_timeout
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.1,
        max_retries: int = 3,
        format: Optional[Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate response from Ollama with retry logic.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            temperature: Temperature for generation (0.0-1.0)
            max_retries: Maximum number of retries on failure
            format: Response format - 'json' for generic JSON, or a dict/schema for structured output
            **kwargs: Additional options for Ollama
            
        Returns:
            Dict containing response and metadata
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        options = {
            "temperature": temperature,
            "num_predict": kwargs.get("max_tokens", self.max_tokens),
        }
        options.update(kwargs.get("options", {}))
        
        # Prepare chat parameters
        chat_params = {
            "model": self.model,
            "messages": messages,
            "options": options
        }
        
        # Add format parameter if specified (for structured output)
        if format:
            chat_params["format"] = format
        
        for attempt in range(max_retries):
            try:
                response = await asyncio.wait_for(
                    self.client.chat(**chat_params),
                    timeout=self.timeout
                )
                
                # Handle response - could be dict or object depending on version
                if hasattr(response, 'message'):
                    # Object response
                    content = response.message.content if hasattr(response.message, 'content') else str(response.message)
                    prompt_tokens = getattr(response, 'prompt_eval_count', 0)
                    completion_tokens = getattr(response, 'eval_count', 0)
                else:
                    # Dict response
                    content = response.get("message", {}).get("content", "")
                    prompt_tokens = response.get("prompt_eval_count", 0)
                    completion_tokens = response.get("eval_count", 0)
                
                return {
                    "success": True,
                    "response": content,
                    "model": self.model,
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens": prompt_tokens + completion_tokens,
                }
                
            except asyncio.TimeoutError:
                logger.error(f"Ollama request timeout (attempt {attempt + 1}/{max_retries})")
                if attempt == max_retries - 1:
                    return {
                        "success": False,
                        "error": "Request timeout",
                        "error_type": "TimeoutError"
                    }
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                
            except ConnectionError as e:
                logger.error(f"Ollama connection error: {e}")
                return {
                    "success": False,
                    "error": f"Connection error: {str(e)}",
                    "error_type": "ConnectionError"
                }
                
            except Exception as e:
                logger.error(f"Ollama generation error: {e}", exc_info=True)
                if attempt == max_retries - 1:
                    return {
                        "success": False,
                        "error": str(e),
                        "error_type": type(e).__name__
                    }
                await asyncio.sleep(2 ** attempt)
        
        # This part should be unreachable if max_retries > 0, but as a fallback:
        return {
            "success": False,
            "error": "Max retries reached without a definitive result.",
            "error_type": "MaxRetriesExceeded"
        }
    
    async def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.1,
        format: Optional[Any] = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """
        Generate streaming response from Ollama.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            temperature: Temperature for generation
            format: Response format - 'json' for generic JSON, or a dict/schema for structured output
            **kwargs: Additional options
            
        Yields:
            Chunks of generated text
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        options = {
            "temperature": temperature,
            "num_predict": kwargs.get("max_tokens", self.max_tokens),
        }
        
        # Prepare chat parameters
        chat_params = {
            "model": self.model,
            "messages": messages,
            "options": options,
            "stream": True
        }
        
        # Add format parameter if specified
        if format:
            chat_params["format"] = format
        
        try:
            stream = await self.client.chat(**chat_params)
            
            async for chunk in stream:
                # Handle both dict and object responses
                if hasattr(chunk, 'message'):
                    content = chunk.message.content if hasattr(chunk.message, 'content') else None
                else:
                    content = chunk.get("message", {}).get("content")
                
                if content:
                    yield content
                    
        except Exception as e:
            logger.error(f"Ollama streaming error: {e}")
            yield f"[ERROR: {str(e)}]"
    
    async def check_health(self) -> bool:
        """Check if Ollama service is healthy."""
        try:
            # Simple test generation
            response = await asyncio.wait_for(
                self.client.chat(
                    model=self.model,
                    messages=[{"role": "user", "content": "test"}],
                    options={"num_predict": 1}
                ),
                timeout=10
            )
            return True
        except Exception as e:
            logger.error(f"Ollama health check failed: {e}")
            return False


# Global client instance
ollama_client = OllamaClient()