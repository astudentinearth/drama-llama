"""Utility functions for similarity calculations."""
import numpy as np
from typing import List


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.
    
    Args:
        vec1: First vector
        vec2: Second vector
        
    Returns:
        Cosine similarity score (0-1)
    """
    arr1 = np.array(vec1)
    arr2 = np.array(vec2)
    
    dot_product = np.dot(arr1, arr2)
    norm1 = np.linalg.norm(arr1)
    norm2 = np.linalg.norm(arr2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return float(dot_product / (norm1 * norm2))


def meets_threshold(similarity: float, threshold: float) -> bool:
    """
    Check if similarity score meets threshold.
    
    Args:
        similarity: Similarity score
        threshold: Minimum threshold
        
    Returns:
        True if meets threshold, False otherwise
    """
    return similarity >= threshold


def normalize_vector(vector: List[float]) -> List[float]:
    """
    Normalize a vector to unit length.
    
    Args:
        vector: Input vector
        
    Returns:
        Normalized vector
    """
    arr = np.array(vector)
    norm = np.linalg.norm(arr)
    
    if norm == 0:
        return vector
    
    normalized = arr / norm
    return normalized.tolist()

