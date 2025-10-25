"""
AI Action routes.
Handles AI chat and tool execution endpoints.
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from db_config import get_db, add_message_to_session, get_session
from models.schemas import (
    AIToolResponse,
    RoadmapSkeletonResponse,
    LearningMaterialResponse,
    APIResponse,
    MessageRole
)
from utils.ai.service import AIService
from utils.groq_client import GroqClient


router = APIRouter(
    prefix="/ai",
    tags=["ai"],
    responses={404: {"description": "Not found"}}
)


# Request/Response Models
class ChatRequest(BaseModel):
    """Chat request with user message."""
    message: str = Field(..., description="User's message")


class ExecuteToolRequest(BaseModel):
    """Request to execute a specific tool."""
    tool_arguments: Dict[str, Any] = Field(default_factory=dict, description="Tool arguments")


class CreateMaterialsRequest(BaseModel):
    """Request to create learning materials for a goal."""
    goal_id: int = Field(..., description="Goal ID to create materials for")


# Initialize AI Service (singleton pattern)
_ai_service: Optional[AIService] = None


def get_ai_service() -> AIService:
    """Get or create AI service instance."""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service


@router.post("/sessions/{session_id}/chat", response_model=AIToolResponse)
def chat_with_ai(
    session_id: int,
    request: ChatRequest,
    db: Session = Depends(get_db),
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Chat with AI and get response with potential tool call instructions.
    
    This endpoint:
    1. Analyzes user message with full session history
    2. Returns AI response with optional tool calls
    3. Does NOT execute tools automatically
    4. Saves user message to session history
    
    Args:
        session_id: Session ID
        request: Chat request with user message
    
    Returns:
        AIToolResponse with content and potential tool calls
    """
    # Verify session exists
    session = get_session(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found"
        )
    
    # Save user message to session
    try:
        add_message_to_session(
            db=db,
            session_id=session_id,
            role=MessageRole.USER.value,
            content=request.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save message: {str(e)}"
        )
    
    # Get AI response with tool planning
    try:
        response = ai_service.plan_action(
            session_id=session_id,
            user_prompt=request.message,
            db=db
        )
        
        # Save assistant response to session
        add_message_to_session(
            db=db,
            session_id=session_id,
            role=MessageRole.ASSISTANT.value,
            content=response.content,
            metadata={
                'has_tool_calls': response.has_tool_calls,
                'tool_calls': [tc.dict() for tc in response.tool_calls],
                'usage': response.usage
            }
        )
        
        return response
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI service error: {str(e)}"
        )


@router.post("/sessions/{session_id}/execute-tool/createRoadmapSkeleton", response_model=APIResponse)
def execute_create_roadmap(
    session_id: int,
    request: ExecuteToolRequest,
    db: Session = Depends(get_db),
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Execute createRoadmapSkeleton tool to generate a learning roadmap.
    
    This endpoint:
    1. Executes the roadmap creation with AI
    2. Saves roadmap and goals to database
    3. Returns structured roadmap response
    
    Args:
        session_id: Session ID
        request: Tool execution request with arguments
    
    Returns:
        APIResponse with roadmap data
    """
    # Verify session exists
    session = get_session(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found"
        )
    
    try:
        # Execute roadmap creation
        roadmap_response = ai_service.execute_roadmap_creation(
            session_id=session_id,
            tool_arguments=request.tool_arguments,
            db=db
        )
        
        # Save tool execution to message history
        add_message_to_session(
            db=db,
            session_id=session_id,
            role=MessageRole.ASSISTANT.value,
            content=f"Created roadmap with {len(roadmap_response.goals)} goals",
            metadata={
                'tool': 'createRoadmapSkeleton',
                'goals_count': len(roadmap_response.goals),
                'graduation_project': roadmap_response.graduation_project_title
            }
        )
        
        return APIResponse(
            success=True,
            data={
                'roadmap': roadmap_response.dict(),
                'message': f'Successfully created roadmap with {len(roadmap_response.goals)} goals'
            }
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create roadmap: {str(e)}"
        )


@router.post("/sessions/{session_id}/execute-tool/createLearningMaterials", response_model=APIResponse)
def execute_create_materials(
    session_id: int,
    request: CreateMaterialsRequest,
    db: Session = Depends(get_db),
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Execute createLearningMaterials tool to generate learning content.
    
    This endpoint:
    1. Executes learning material creation with AI
    2. Saves material to database linked to goal
    3. Returns structured material response
    
    Args:
        session_id: Session ID
        request: Request with goal_id
    
    Returns:
        APIResponse with learning material data
    """
    # Verify session exists
    session = get_session(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found"
        )
    
    try:
        # Execute material creation
        material_response = ai_service.execute_material_creation(
            goal_id=request.goal_id,
            session_id=session_id,
            db=db
        )
        
        # Save tool execution to message history
        add_message_to_session(
            db=db,
            session_id=session_id,
            role=MessageRole.ASSISTANT.value,
            content=f"Created learning materials: {material_response.title}",
            metadata={
                'tool': 'createLearningMaterials',
                'goal_id': request.goal_id,
                'material_title': material_response.title,
                'estimated_time': material_response.estimated_time_minutes
            }
        )
        
        return APIResponse(
            success=True,
            data={
                'material': material_response.dict(),
                'message': f'Successfully created learning materials: {material_response.title}'
            }
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create learning materials: {str(e)}"
        )


@router.get("/sessions/{session_id}/roadmap", response_model=APIResponse)
def get_session_roadmap(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Get roadmap for a session with all goals.
    
    Args:
        session_id: Session ID
    
    Returns:
        APIResponse with roadmap and goals
    """
    from db_config.crud import get_roadmap_by_session, get_goals_by_roadmap
    
    # Verify session exists
    session = get_session(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found"
        )
    
    # Get roadmap
    roadmap = get_roadmap_by_session(db, session_id)
    if not roadmap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No roadmap found for session {session_id}"
        )
    
    # Get goals
    goals = get_goals_by_roadmap(db, roadmap.id)
    
    return APIResponse(
        success=True,
        data={
            'roadmap': {
                'id': roadmap.id,
                'user_request': roadmap.user_request,
                'total_estimated_weeks': roadmap.total_estimated_weeks,
                'graduation_project': roadmap.graduation_project,
                'graduation_project_title': roadmap.graduation_project_title,
                'status': roadmap.status.value
            },
            'goals': [
                {
                    'id': goal.id,
                    'goal_number': goal.goal_number,
                    'title': goal.title,
                    'description': goal.description,
                    'priority': goal.priority,
                    'skill_level': goal.skill_level.value,
                    'estimated_hours': goal.estimated_hours,
                    'is_completed': goal.is_completed
                }
                for goal in goals
            ]
        }
    )


@router.get("/health", response_model=APIResponse)
def ai_health_check(ai_service: AIService = Depends(get_ai_service)):
    """
    Health check for AI service.
    Tests Groq API connectivity.
    
    Returns:
        APIResponse with connection status
    """
    try:
        # Test simple completion
        response = ai_service.client.complete("Say 'OK' if you can hear me.")
        
        return APIResponse(
            success=True,
            data={
                'status': 'connected',
                'model': ai_service.client.model,
                'test_response': response[:50]  # First 50 chars
            }
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=f"Groq API connection failed: {str(e)}"
        )

