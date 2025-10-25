"""API routes for caching operations."""
import logging
from typing import List
from fastapi import APIRouter, HTTPException, status
from models.schemas import (
    MaterialCreate,
    MaterialResponse,
    SearchRequest,
    SearchResponse,
    CacheStats,
    HealthResponse
)
from services import embedding_service, qdrant_service
from config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/cache", tags=["cache"])


@router.post("/search", response_model=SearchResponse)
async def search_materials(request: SearchRequest):
    """
    Search for similar materials using semantic similarity.
    
    Args:
        request: Search request with query and optional filters
        
    Returns:
        SearchResponse with matched materials and similarity scores
    """
    try:
        # Generate embedding for query directly
        query_embedding = embedding_service.encode_single(request.query)
        
        # Use threshold from request or default
        threshold = request.threshold or settings.similarity_threshold
        
        # Search in Qdrant
        results = qdrant_service.search_similar(
            query_embedding=query_embedding,
            limit=request.limit,
            score_threshold=threshold,
            filters=request.filters
        )
        
        return SearchResponse(
            results=results,
            query=request.query,
            total_found=len(results),
            threshold_used=threshold
        )
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@router.post("/store", response_model=MaterialResponse, status_code=status.HTTP_201_CREATED)
async def store_material(material: MaterialCreate):
    """
    Store a new learning material with automatic embedding generation.
    Checks for duplicates before storing using both semantic similarity and exact content matching.
    
    Args:
        material: Material to store
        
    Returns:
        MaterialResponse with ID and timestamp
    """
    try:
        # Combine title and content for embedding
        text_for_embedding = f"{material.title}\n\n{material.content}"
        
        # Generate embedding directly
        embedding = embedding_service.encode_single(text_for_embedding)
        
        # Check for duplicates using a more reasonable similarity threshold (0.95)
        # This catches near-identical content without being too strict
        duplicate_results = qdrant_service.search_similar(
            query_embedding=embedding,
            limit=5,  # Check top 5 results to be thorough
            score_threshold=0.95,
            filters=None
        )
        
        # If similar materials exist, check for exact or near-exact matches
        if duplicate_results:
            for result in duplicate_results:
                existing = result.material
                similarity = result.similarity_score
                
                # Check for exact title and content match
                if (existing.title.strip().lower() == material.title.strip().lower() and 
                    existing.content.strip().lower() == material.content.strip().lower()):
                    logger.warning(
                        f"Exact duplicate detected: '{existing.title}' "
                        f"(ID: {existing.id}, similarity: {similarity:.4f})"
                    )
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail={
                            "message": "Exact duplicate material already exists",
                            "existing_id": existing.id,
                            "existing_title": existing.title,
                            "similarity_score": similarity,
                            "match_type": "exact"
                        }
                    )
                
                # Check for very high similarity (>= 0.98)
                elif similarity >= 0.98:
                    logger.warning(
                        f"Near-duplicate detected: '{existing.title}' "
                        f"(ID: {existing.id}, similarity: {similarity:.4f})"
                    )
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail={
                            "message": "Material with very high similarity already exists",
                            "existing_id": existing.id,
                            "existing_title": existing.title,
                            "similarity_score": similarity,
                            "match_type": "near-duplicate"
                        }
                    )
            
            # If we found similar results but none are duplicates, log for monitoring
            best_match = duplicate_results[0]
            logger.info(
                f"Storing new material '{material.title}'. "
                f"Similar content exists: '{best_match.material.title}' "
                f"(similarity: {best_match.similarity_score:.4f})"
            )
        
        # Store in Qdrant
        material_id = qdrant_service.store_material(
            material=material,
            embedding=embedding
        )
        
        # Retrieve and return stored material
        stored_material = qdrant_service.get_material(material_id)
        
        if not stored_material:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Material stored but could not be retrieved"
            )
        
        logger.info(f"Successfully stored new material: '{material.title}' (ID: {material_id})")
        return stored_material
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Store error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to store material: {str(e)}"
        )


@router.get("/material/{material_id}", response_model=MaterialResponse)
async def get_material(material_id: str):
    """
    Retrieve a specific material by ID.
    
    Args:
        material_id: Material ID
        
    Returns:
        MaterialResponse
    """
    try:
        material = qdrant_service.get_material(material_id)
        
        if not material:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Material with ID {material_id} not found"
            )
        
        return material
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Retrieve error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve material: {str(e)}"
        )


@router.delete("/material/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_material(material_id: str):
    """
    Delete a material by ID.
    
    Args:
        material_id: Material ID
    """
    try:
        success = qdrant_service.delete_material(material_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Material with ID {material_id} not found"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete material: {str(e)}"
        )


@router.get("/stats", response_model=CacheStats)
async def get_stats():
    """
    Get collection statistics.
    
    Returns:
        CacheStats with collection information
    """
    try:
        stats = qdrant_service.get_collection_stats()
        return CacheStats(**stats)
        
    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get statistics: {str(e)}"
        )


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        HealthResponse with service status
    """
    qdrant_connected = qdrant_service.is_connected()
    embedding_loaded = embedding_service.is_loaded()
    
    all_healthy = qdrant_connected and embedding_loaded
    
    details = {}
    
    if qdrant_connected:
        try:
            stats = qdrant_service.get_collection_stats()
            details["collection_exists"] = True
            details["total_materials"] = stats["total_materials"]
        except Exception as e:
            details["collection_error"] = str(e)
    
    if embedding_loaded:
        details["embedding_dimension"] = embedding_service.get_embedding_dimension()
        details["embedding_model"] = settings.embedding_model
    
    return HealthResponse(
        status="healthy" if all_healthy else "unhealthy",
        qdrant_connected=qdrant_connected,
        embedding_model_loaded=embedding_loaded,
        tokenizer_loaded=False,  # Not used
        details=details
    )

