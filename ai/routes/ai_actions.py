"""
AI Action routes.
Handles AI chat and tool execution endpoints.
"""

import json
import asyncio
from typing import Dict, Any, Optional, AsyncIterator
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from utils.pdf_parse import extract_text_from_pdf
from db_config import get_db, add_message_to_session, get_session
from models.schemas import (
    AIToolResponse,
    RoadmapSkeletonResponse,
    LearningMaterialResponse,
    APIResponse,
    MessageRole,
    ToolCallInstruction
)
from utils.ai.service import AIService
from utils.groq_client import GroqClient
from utils.auth import verify_api_key


router = APIRouter(
    prefix="/ai",
    tags=["ai"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(verify_api_key)]
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


@router.post("/sessions/{session_id}/chat")
async def chat_with_ai_stream(
    session_id: int,
    request: ChatRequest,
    db: Session = Depends(get_db),
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Chat with AI using Server-Sent Events (SSE) streaming.
    
    This endpoint:
    1. Streams the initial AI response with tool calls (event: master_prompt)
    2. Automatically executes any tool calls
    3. Streams tool execution results (event: tool_name)
    4. Ends with done event
    
    Args:
        session_id: Session ID
        request: Chat request with user message
    
    Returns:
        StreamingResponse with SSE events
    """
    async def event_generator() -> AsyncIterator[str]:
        """Generate SSE events for the chat response."""
        try:
            # Verify session exists
            session = get_session(db, session_id)
            if not session:
                yield format_sse_event('error', {
                    'message': f'Session {session_id} not found'
                })
                return
            
            # Save user message to session
            try:
                add_message_to_session(
                    db=db,
                    session_id=session_id,
                    role=MessageRole.USER.value,
                    content=request.message
                )
            except Exception as e:
                yield format_sse_event('error', {
                    'message': f'Failed to save message: {str(e)}'
                })
                return
            
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
                
                # Send master prompt response as single event
                yield format_sse_event('master_prompt', {
                    'response': response.content,
                    'has_tool_calls': response.has_tool_calls,
                    'tool_calls': [
                        {
                            'tool_name': tc.tool_name,
                            'arguments': tc.arguments,
                            'call_id': tc.call_id
                        }
                        for tc in response.tool_calls
                    ],
                    'finish_reason': response.finish_reason,
                    'usage': response.usage
                })
                
                # Yield control to ensure the event is sent before tool execution
                await asyncio.sleep(0)
                
                # Execute tool calls if any (send each as separate event)
                if response.has_tool_calls:
                    for tool_call in response.tool_calls:
                        try:
                            tool_result = await execute_tool_call(
                                session_id=session_id,
                                tool_call=tool_call,
                                ai_service=ai_service,
                                db=db
                            )
                            
                            # Stream tool result with appropriate event name
                            event_name = get_tool_event_name(tool_call.tool_name)
                            yield format_sse_event(event_name, tool_result)
                            
                            # Yield control between tool executions
                            await asyncio.sleep(0)
                            
                        except Exception as e:
                            yield format_sse_event('error', {
                                'operation': tool_call.tool_name,
                                'message': f'Tool execution failed: {str(e)}'
                            })
                
                # Stream done event
                yield format_sse_event('done', {
                    'message': 'Request completed successfully'
                })
                
            except ValueError as e:
                yield format_sse_event('error', {
                    'message': f'Validation error: {str(e)}'
                })
            except Exception as e:
                yield format_sse_event('error', {
                    'message': f'AI service error: {str(e)}'
                })
                
        except Exception as e:
            yield format_sse_event('error', {
                'message': f'Unexpected error: {str(e)}'
            })
    
    return StreamingResponse(
        event_generator(),
        media_type='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no'  # Disable nginx buffering
        }
    )

class SummarizeCVRequest(BaseModel):
    cv_url: str = Field(..., description="URL of the CV")

@router.post("/sessions/{session_id}/summarize-cv", response_model=APIResponse)
def execute_summarize_cv(
    session_id: int,
    request: SummarizeCVRequest,
    db: Session = Depends(get_db),
    ai_service: AIService = Depends(get_ai_service),
):
    """
    Summarize the CV of the user.
    """
    # Verify session exists
    session = get_session(db, session_id)
    if not session:
        return APIResponse(
            success=False,
            error=f"Session {session_id} not found"
        )
    try:
        cv_text = extract_text_from_pdf(request.cv_url)
        summary = ai_service.extract_cv_information(cv_text)
        return APIResponse(
            success=True,
            data={
                'summary': summary
            }
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=f"Failed to summarize CV: {str(e)}"
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


# ============= SSE Helper Functions =============

def format_sse_event(event_name: str, data: Dict[str, Any]) -> str:
    """
    Format data as Server-Sent Event.
    
    Args:
        event_name: Name of the event
        data: Data to send
    
    Returns:
        Formatted SSE string
    """
    json_data = json.dumps(data, ensure_ascii=False)
    return f"event: {event_name}\ndata: {json_data}\n\n"


def get_tool_event_name(tool_name: str) -> str:
    """
    Map tool name to SSE event name.
    
    Args:
        tool_name: Tool function name
    
    Returns:
        Event name for SSE
    """
    tool_event_map = {
        'createRoadmapSkeleton': 'roadmap_skeleton',
        'createLearningMaterials': 'learning_materials'
    }
    return tool_event_map.get(tool_name, tool_name.lower())


async def execute_tool_call(
    session_id: int,
    tool_call: 'ToolCallInstruction',
    ai_service: AIService,
    db: Session
) -> Dict[str, Any]:
    """
    Execute a tool call and return result.
    Runs synchronous tool execution in a thread pool to avoid blocking.
    
    Args:
        session_id: Session ID
        tool_call: Tool call instruction
        ai_service: AI service instance
        db: Database session
    
    Returns:
        Tool execution result
    """
    # Run synchronous tool execution in thread pool
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,  # Use default executor
        _execute_tool_call_sync,
        session_id,
        tool_call,
        ai_service,
        db
    )


def _execute_tool_call_sync(
    session_id: int,
    tool_call: 'ToolCallInstruction',
    ai_service: AIService,
    db: Session
) -> Dict[str, Any]:
    """
    Synchronous tool execution (runs in thread pool).
    
    Args:
        session_id: Session ID
        tool_call: Tool call instruction
        ai_service: AI service instance
        db: Database session
    
    Returns:
        Tool execution result
    """
    tool_name = tool_call.tool_name
    arguments = tool_call.arguments
    
    if tool_name == 'createRoadmapSkeleton':
        # Execute roadmap creation
        roadmap_response = ai_service.execute_roadmap_creation(
            session_id=session_id,
            tool_arguments=arguments,
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
        
        return {
            'success': True,
            'operation': 'createRoadmapSkeleton',
            'data': {
                'goals': [goal.dict() for goal in roadmap_response.goals],
                'graduation_project': roadmap_response.graduation_project,
                'graduation_project_title': roadmap_response.graduation_project_title,
                'total_goals': len(roadmap_response.goals)
            },
            'message': f'Successfully created roadmap with {len(roadmap_response.goals)} goals'
        }
    
    elif tool_name == 'createLearningMaterials':
        # Get goal_id from arguments
        goal_id = arguments.get('goal_id')
        if not goal_id:
            raise ValueError("goal_id is required for createLearningMaterials")
        
        # Execute material creation
        material_response = ai_service.execute_material_creation(
            goal_id=goal_id,
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
                'goal_id': goal_id,
                'material_title': material_response.title,
                'estimated_time': material_response.estimated_time_minutes
            }
        )
        
        return {
            'success': True,
            'operation': 'createLearningMaterials',
            'data': material_response.dict(),
            'message': f'Successfully created learning materials: {material_response.title}'
        }
    
    else:
        raise ValueError(f"Unknown tool: {tool_name}")

