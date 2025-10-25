"""
Groq API Client using OpenAI SDK.
Provides a wrapper around OpenAI SDK configured for Groq's API endpoint.
"""

import os
import time
from typing import List, Dict, Any, Optional, Union
from openai import OpenAI
from config import settings


class AIResponse:
    """
    AI Response wrapper for structured response handling.
    Similar to the PHP AIResponse class from reference.
    """
    
    def __init__(self, response: Any, request: Dict[str, Any]):
        """
        Initialize AIResponse with raw OpenAI response and request.
        
        Args:
            response: Raw response from OpenAI API
            request: Original request payload
        """
        self.raw_response = response
        self.request = request
        
        # Extract message from choices
        if hasattr(response, 'choices') and len(response.choices) > 0:
            self.message = {
                'role': response.choices[0].message.role,
                'content': response.choices[0].message.content or '',
            }
            
            # Add tool calls if present
            if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls:
                self.message['tool_calls'] = [
                    {
                        'id': tc.id,
                        'type': tc.type,
                        'function': {
                            'name': tc.function.name,
                            'arguments': tc.function.arguments
                        }
                    }
                    for tc in response.choices[0].message.tool_calls
                ]
        else:
            self.message = {'role': 'assistant', 'content': ''}
    
    def get_content(self) -> str:
        """Get the message content."""
        return self.message.get('content', '')
    
    def get_message(self) -> Dict[str, Any]:
        """Get the complete message object."""
        return self.message
    
    def has_tool_calls(self) -> bool:
        """Check if response contains tool calls."""
        return 'tool_calls' in self.message and len(self.message['tool_calls']) > 0
    
    def get_tool_calls(self) -> List[Dict[str, Any]]:
        """Get list of tool calls."""
        return self.message.get('tool_calls', [])
    
    def get_usage(self) -> Dict[str, int]:
        """Get token usage statistics."""
        if hasattr(self.raw_response, 'usage'):
            usage = self.raw_response.usage
            return {
                'prompt_tokens': usage.prompt_tokens if hasattr(usage, 'prompt_tokens') else 0,
                'completion_tokens': usage.completion_tokens if hasattr(usage, 'completion_tokens') else 0,
                'total_tokens': usage.total_tokens if hasattr(usage, 'total_tokens') else 0
            }
        return {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}
    
    def get_finish_reason(self) -> str:
        """Get finish reason."""
        if hasattr(self.raw_response, 'choices') and len(self.raw_response.choices) > 0:
            return self.raw_response.choices[0].finish_reason or ''
        return ''
    
    def was_truncated(self) -> bool:
        """Check if response was truncated due to length."""
        return self.get_finish_reason() == 'length'
    
    def get_model(self) -> str:
        """Get model used for completion."""
        return getattr(self.raw_response, 'model', '')
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return {
            'content': self.get_content(),
            'has_tool_calls': self.has_tool_calls(),
            'tool_calls': self.get_tool_calls(),
            'usage': self.get_usage(),
            'model': self.get_model(),
            'finish_reason': self.get_finish_reason(),
            'was_truncated': self.was_truncated()
        }


class GroqClient:
    """
    Groq API Client wrapper using OpenAI SDK.
    Handles API requests with retries, error handling, and structured outputs.
    """
    
    DEFAULT_TIMEOUT = 60
    DEFAULT_RETRIES = 3
    RATE_LIMIT_DELAY = 1
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_RETRIES
    ):
        """
        Initialize Groq client.
        
        Args:
            api_key: Groq API key (defaults to settings.groq_api_key)
            model: Model to use (defaults to settings.groq_model)
            temperature: Temperature for generation (0.0-2.0)
            max_tokens: Maximum tokens to generate
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries on failure
        """
        self.api_key = api_key or settings.groq_api_key
        self.model = model or settings.groq_model
        self.temperature = temperature
        self.max_tokens = max_tokens or settings.groq_max_tokens
        self.timeout = max(1, timeout)
        self.max_retries = max(0, max_retries)
        
        if not self.api_key:
            raise ValueError("Groq API key is required. Set GROQ_API_KEY environment variable.")
        
        # Initialize OpenAI client configured for Groq
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1",
            timeout=self.timeout,
            max_retries=0  # We handle retries ourselves
        )
    
    def execute(
        self,
        messages: Union[List[Dict[str, Any]], str],
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
        response_format: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> AIResponse:
        """
        Main execution method - handles completions and tool calls.
        
        Args:
            messages: List of message dicts or single string prompt
            tools: Optional list of tool definitions
            tool_choice: Optional tool choice strategy ('auto', 'required', or specific tool)
            response_format: Optional response format specification
            **kwargs: Additional parameters to pass to API
        
        Returns:
            AIResponse object with response data
        """
        # Convert string to messages format
        if isinstance(messages, str):
            messages = [{'role': 'user', 'content': messages}]
        
        request = self._build_request(messages, tools, tool_choice, response_format, **kwargs)
        response = self._send_request_with_retry(request)
        
        return AIResponse(response, request)
    
    def execute_with_tools(
        self,
        messages: Union[List[Dict[str, Any]], str],
        tools: List[Dict[str, Any]],
        tool_choice: Optional[Union[str, Dict[str, Any]]] = 'auto',
        **kwargs
    ) -> AIResponse:
        """
        Execute with tools available.
        
        Args:
            messages: List of message dicts or single string prompt
            tools: List of tool definitions
            tool_choice: Tool choice strategy (default: 'auto')
            **kwargs: Additional parameters
        
        Returns:
            AIResponse with potential tool calls
        """
        return self.execute(messages, tools=tools, tool_choice=tool_choice, **kwargs)
    
    def complete(
        self,
        messages: Union[List[Dict[str, Any]], str],
        **kwargs
    ) -> str:
        """
        Simple completion - returns string content only.
        
        Args:
            messages: List of message dicts or single string prompt
            **kwargs: Additional parameters
        
        Returns:
            String content of response
        """
        response = self.execute(messages, **kwargs)
        return response.get_content()
    
    def _build_request(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]],
        tool_choice: Optional[Union[str, Dict[str, Any]]],
        response_format: Optional[Dict[str, Any]],
        **kwargs
    ) -> Dict[str, Any]:
        """Build request payload."""
        request = {
            'model': kwargs.get('model', self.model),
            'messages': messages,
            'temperature': kwargs.get('temperature', self.temperature),
        }
        
        # Add max_tokens if specified
        max_tokens = kwargs.get('max_tokens', self.max_tokens)
        if max_tokens:
            request['max_tokens'] = max_tokens
        
        # Add tools if provided
        if tools:
            request['tools'] = tools
            if tool_choice:
                request['tool_choice'] = tool_choice
        
        # Add response format if provided
        if response_format:
            request['response_format'] = response_format
        
        # Add any other kwargs
        for key, value in kwargs.items():
            if key not in ['model', 'temperature', 'max_tokens']:
                request[key] = value
        
        return request
    
    def _send_request_with_retry(self, request: Dict[str, Any]) -> Any:
        """
        Send request with retry logic.
        
        Args:
            request: Request payload
        
        Returns:
            Raw OpenAI response
        
        Raises:
            Exception: If all retries fail
        """
        attempt = 0
        last_exception = None
        
        while attempt <= self.max_retries:
            try:
                start_time = time.time()
                
                # Make the API call
                response = self.client.chat.completions.create(**request)
                
                duration = (time.time() - start_time) * 1000
                print(f"Groq API request completed in {duration:.2f}ms (attempt {attempt + 1})")
                
                return response
                
            except Exception as e:
                last_exception = e
                attempt += 1
                
                print(f"Groq API request failed (attempt {attempt}): {str(e)}")
                
                # Don't retry on certain errors
                if self._should_not_retry(e):
                    raise
                
                # Don't sleep after the last attempt
                if attempt <= self.max_retries:
                    delay = self._calculate_backoff_delay(attempt)
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
        
        # All retries failed
        raise Exception(
            f"Request failed after {self.max_retries + 1} attempts. Last error: {str(last_exception)}"
        )
    
    def _should_not_retry(self, exception: Exception) -> bool:
        """Check if error should not be retried."""
        error_msg = str(exception).lower()
        
        # Don't retry on authentication, permission, or bad request errors
        non_retryable_patterns = [
            'unauthorized',
            'forbidden',
            'invalid_api_key',
            'bad request',
            'invalid_request_error'
        ]
        
        return any(pattern in error_msg for pattern in non_retryable_patterns)
    
    def _calculate_backoff_delay(self, attempt: int) -> int:
        """Calculate exponential backoff delay."""
        # Exponential backoff: 1s, 2s, 4s, 8s... (max 30s)
        return min(self.RATE_LIMIT_DELAY * (2 ** (attempt - 1)), 30)

