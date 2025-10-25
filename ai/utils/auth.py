"""
Authentication utilities for API key validation.
"""
from typing import Optional
from fastapi import Header, HTTPException, status
from config import settings


def verify_api_key(x_api_key: Optional[str] = Header(None, alias="X-API-Key")) -> str:
    """
    Verify the API key from the request header.
    
    Args:
        x_api_key: API key from X-API-Key header
        
    Returns:
        str: The validated API key
        
    Raises:
        HTTPException: 403 if API key is missing or invalid
    """
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key is required. Please provide X-API-Key header."
        )
    
    if x_api_key != settings.api_key_secret:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )
    
    return x_api_key
