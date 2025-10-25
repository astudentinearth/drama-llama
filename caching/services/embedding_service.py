"""Embedding service using sentence-transformers."""
import logging
from typing import List, Union
from sentence_transformers import SentenceTransformer
import torch
from config import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating embeddings using sentence-transformers."""
    
    def __init__(self):
        """Initialize the embedding service."""
        self.model_name = settings.embedding_model
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Embedding service will use device: {self.device}")
    
    def load_model(self) -> None:
        """Load the sentence-transformers model."""
        try:
            logger.info(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name, device=self.device)
            logger.info(f"Embedding model loaded successfully on {self.device}")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise
    
    def is_loaded(self) -> bool:
        """Check if the model is loaded."""
        return self.model is not None
    
    def encode(self, texts: Union[str, List[str]], batch_size: int = 32) -> List[List[float]]:
        """
        Generate embeddings for given text(s).
        
        Args:
            texts: Single text string or list of text strings
            batch_size: Batch size for processing multiple texts
            
        Returns:
            List of embedding vectors (384-dimensional for all-MiniLM-L6-v2)
        """
        if not self.is_loaded():
            raise RuntimeError("Embedding model not loaded. Call load_model() first.")
        
        try:
            # Convert single string to list
            if isinstance(texts, str):
                texts = [texts]
            
            # Generate embeddings
            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                show_progress_bar=False,
                convert_to_numpy=True
            )
            
            # Convert numpy arrays to lists
            # Handle both single and multiple texts
            if embeddings.ndim == 1:
                # Single embedding, wrap in list
                return [embeddings.tolist()]
            else:
                # Multiple embeddings
                return embeddings.tolist()
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
    
    def encode_single(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Input text string
            
        Returns:
            Embedding vector as list of floats
        """
        embeddings = self.encode(text)
        return embeddings[0]
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of the embedding vectors.
        
        Returns:
            Embedding dimension (384 for all-MiniLM-L6-v2)
        """
        if not self.is_loaded():
            return settings.vector_size
        return self.model.get_sentence_embedding_dimension()


# Global instance
embedding_service = EmbeddingService()

