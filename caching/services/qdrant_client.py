"""Qdrant client service for vector operations."""
import logging
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)
from config import settings
from models.schemas import Material, MaterialResponse, SearchResult

logger = logging.getLogger(__name__)


class QdrantClientService:
    """Service for interacting with Qdrant vector database."""
    
    def __init__(self):
        """Initialize Qdrant client service."""
        self.host = settings.qdrant_host
        self.port = settings.qdrant_port
        self.collection_name = settings.qdrant_collection
        self.vector_size = settings.vector_size
        self.api_key = settings.qdrant_api_key
        self.url = settings.qdrant_url
        self.use_https = settings.qdrant_use_https
        self.client: Optional[QdrantClient] = None
    
    def connect(self) -> None:
        """Connect to Qdrant server with optional authentication and timeout handling."""
        try:
            # Priority 1: Use full URL if provided (for Qdrant Cloud)
            if self.url:
                logger.info(f"Connecting to Qdrant Cloud at {self.url}")
                self.client = QdrantClient(
                    url=self.url,
                    api_key=self.api_key if self.api_key else None,
                    timeout=10.0  # 10 second timeout for cloud connections
                )
                logger.info("Successfully connected to Qdrant Cloud")
            
            # Priority 2: Use host:port with optional API key (for local or self-hosted)
            else:
                logger.info(f"Connecting to Qdrant at {self.host}:{self.port} (https={self.use_https})")
                connection_params = {
                    "host": self.host,
                    "port": self.port,
                    "https": self.use_https,
                    "timeout": 10.0  # 10 second timeout
                }
                
                # Add API key if provided
                if self.api_key:
                    connection_params["api_key"] = self.api_key
                    logger.info("Using API key authentication")
                
                self.client = QdrantClient(**connection_params)
                logger.info("Successfully connected to Qdrant")
            
            # Test connection with a simple operation
            logger.info("Testing Qdrant connection...")
            self.client.get_collections()
            logger.info("Connection test successful")
                
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            logger.error(f"Connection details - Host: {self.host}, Port: {self.port}, HTTPS: {self.use_https}, URL: {self.url}")
            raise
    
    def is_connected(self) -> bool:
        """Check if connected to Qdrant."""
        if not self.client:
            return False
        try:
            # Try to get collections as a health check
            self.client.get_collections()
            return True
        except Exception as e:
            logger.error(f"Qdrant connection check failed: {e}")
            return False
    
    def create_collection(self) -> None:
        """Create the learning materials collection if it doesn't exist."""
        if not self.client:
            raise RuntimeError("Qdrant client not connected")
        
        try:
            # Check if collection exists
            collections = self.client.get_collections().collections
            collection_exists = any(col.name == self.collection_name for col in collections)
            
            if collection_exists:
                logger.info(f"Collection '{self.collection_name}' already exists")
                return
            
            # Create collection
            logger.info(f"Creating collection '{self.collection_name}'")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE
                )
            )
            logger.info(f"Collection '{self.collection_name}' created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create collection: {e}")
            raise
    
    def store_material(
        self,
        material: Material,
        embedding: List[float],
        material_id: Optional[str] = None
    ) -> str:
        """
        Store a learning material with its embedding in Qdrant.
        
        Args:
            material: Material object
            embedding: Vector embedding
            material_id: Optional custom ID (UUID generated if not provided)
            
        Returns:
            Material ID
        """
        if not self.client:
            raise RuntimeError("Qdrant client not connected")
        
        try:
            # Generate ID if not provided
            if not material_id:
                material_id = str(uuid.uuid4())
            
            # Prepare payload
            payload = {
                "title": material.title,
                "content": material.content,
                "metadata": material.metadata or {},
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Create point
            point = PointStruct(
                id=material_id,
                vector=embedding,
                payload=payload
            )
            
            # Upsert point
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            
            logger.info(f"Stored material with ID: {material_id}")
            return material_id
            
        except Exception as e:
            logger.error(f"Failed to store material: {e}")
            raise
    
    def search_similar(
        self,
        query_embedding: List[float],
        limit: int = 10,
        score_threshold: Optional[float] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """
        Search for similar materials using vector similarity.
        
        Args:
            query_embedding: Query vector embedding
            limit: Maximum number of results
            score_threshold: Minimum similarity score (default: from settings)
            filters: Optional metadata filters
            
        Returns:
            List of SearchResult objects
        """
        if not self.client:
            raise RuntimeError("Qdrant client not connected")
        
        try:
            # Use default threshold if not provided
            if score_threshold is None:
                score_threshold = settings.similarity_threshold
            
            # Build filter if provided
            qdrant_filter = None
            if filters:
                conditions = []
                for key, value in filters.items():
                    conditions.append(
                        FieldCondition(
                            key=f"metadata.{key}",
                            match=MatchValue(value=value)
                        )
                    )
                if conditions:
                    qdrant_filter = Filter(must=conditions)
            
            # Perform search
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                score_threshold=score_threshold,
                query_filter=qdrant_filter
            )
            
            # Convert to SearchResult objects
            results = []
            for hit in search_results:
                material_response = MaterialResponse(
                    id=str(hit.id),
                    title=hit.payload.get("title", ""),
                    content=hit.payload.get("content", ""),
                    metadata=hit.payload.get("metadata", {}),
                    timestamp=datetime.fromisoformat(hit.payload.get("timestamp"))
                )
                
                search_result = SearchResult(
                    material=material_response,
                    similarity_score=hit.score
                )
                results.append(search_result)
            
            logger.info(f"Found {len(results)} similar materials")
            return results
            
        except Exception as e:
            logger.error(f"Failed to search materials: {e}")
            raise
    
    def get_material(self, material_id: str) -> Optional[MaterialResponse]:
        """
        Retrieve a material by ID.
        
        Args:
            material_id: Material ID
            
        Returns:
            MaterialResponse or None if not found
        """
        if not self.client:
            raise RuntimeError("Qdrant client not connected")
        
        try:
            result = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[material_id]
            )
            
            if not result:
                return None
            
            point = result[0]
            material = MaterialResponse(
                id=str(point.id),
                title=point.payload.get("title", ""),
                content=point.payload.get("content", ""),
                metadata=point.payload.get("metadata", {}),
                timestamp=datetime.fromisoformat(point.payload.get("timestamp"))
            )
            
            return material
            
        except Exception as e:
            logger.error(f"Failed to retrieve material: {e}")
            raise
    
    def delete_material(self, material_id: str) -> bool:
        """
        Delete a material by ID.
        
        Args:
            material_id: Material ID
            
        Returns:
            True if deleted, False otherwise
        """
        if not self.client:
            raise RuntimeError("Qdrant client not connected")
        
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=[material_id]
            )
            logger.info(f"Deleted material with ID: {material_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete material: {e}")
            return False
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the collection.
        
        Returns:
            Dictionary with collection statistics
        """
        if not self.client:
            raise RuntimeError("Qdrant client not connected")
        
        try:
            collection_info = self.client.get_collection(self.collection_name)
            
            return {
                "collection_name": self.collection_name,
                "total_materials": collection_info.points_count,
                "vector_size": collection_info.config.params.vectors.size,
                "indexed": collection_info.status == "green"
            }
            
        except Exception as e:
            logger.error(f"Failed to get collection stats: {e}")
            raise


# Global instance
qdrant_service = QdrantClientService()

