"""
Session management routes.
Handles CRUD operations for learning sessions.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from db_config import (
    get_db,
    create_session,
    get_session,
    get_sessions_by_user,
    update_session,
    delete_session,
    count_user_sessions,
    get_session_with_full_roadmap,
    get_roadmap_by_session,
    get_goals_by_roadmap,
    # Message operations
    add_message_to_session,
    get_session_messages,
    get_last_n_messages,
    clear_session_messages,
    count_session_messages,
)
from models.schemas import (
    SessionCreate,
    SessionUpdate,
    SessionResponse,
    SessionListResponse,
    SessionProgressStats,
    MessageCreate,
    MessageResponse,
    MessagesListResponse,
    APIResponse
)
from models.db_models import SessionStatusEnum

router = APIRouter(
    prefix="/sessions",
    tags=["sessions"],
    responses={404: {"description": "Session not found"}}
)


def format_datetime(dt):
    """Format datetime to ISO string."""
    return dt.isoformat() if dt else None


def session_to_response(session) -> SessionResponse:
    """Convert session model to response schema."""
    return SessionResponse(
        id=session.id,
        user_id=session.user_id,
        session_name=session.session_name,
        description=session.description,
        status=session.status.value,
        created_at=format_datetime(session.created_at),
        updated_at=format_datetime(session.updated_at),
        completed_at=format_datetime(session.completed_at)
    )


@router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_new_session(
    session_data: SessionCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new learning session for a user.
    
    - **user_id**: User ID from main backend
    - **session_name**: Optional descriptive name for the session
    - **description**: Optional detailed description
    - **status**: Initial status (default: ACTIVE)
    """
    try:
        # Convert string status to enum
        status_enum = SessionStatusEnum(session_data.status.value)
        
        new_session = create_session(
            db,
            user_id=session_data.user_id,
            session_name=session_data.session_name,
            description=session_data.description,
            status=status_enum
        )
        
        return session_to_response(new_session)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create session: {str(e)}"
        )


@router.get("/{session_id}", response_model=SessionResponse)
def get_session_by_id(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific session by ID.
    
    - **session_id**: Session ID
    """
    session = get_session(db, session_id)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with id {session_id} not found"
        )
    
    return session_to_response(session)


@router.get("/user/{user_id}", response_model=SessionListResponse)
def get_user_sessions(
    user_id: int,
    status_filter: Optional[str] = Query(None, description="Filter by status: active, completed, archived"),
    skip: int = Query(0, ge=0, description="Number of sessions to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of sessions to return"),
    db: Session = Depends(get_db)
):
    """
    Get all sessions for a specific user.
    
    - **user_id**: User ID
    - **status_filter**: Optional filter by status (active, completed, archived)
    - **skip**: Pagination offset
    - **limit**: Maximum results per page
    """
    # Convert status filter to enum if provided
    status_enum = None
    if status_filter:
        try:
            status_enum = SessionStatusEnum(status_filter.lower())
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status: {status_filter}. Must be one of: active, completed, archived"
            )
    
    sessions = get_sessions_by_user(
        db,
        user_id=user_id,
        status=status_enum,
        skip=skip,
        limit=limit
    )
    
    total = count_user_sessions(db, user_id, status=status_enum)
    
    return SessionListResponse(
        sessions=[session_to_response(s) for s in sessions],
        total=total,
        skip=skip,
        limit=limit
    )


@router.patch("/{session_id}", response_model=SessionResponse)
def update_session_by_id(
    session_id: int,
    session_data: SessionUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a session.
    
    - **session_id**: Session ID
    - **session_name**: New session name (optional)
    - **description**: New description (optional)
    - **status**: New status (optional)
    """
    # Check if session exists
    existing_session = get_session(db, session_id)
    if not existing_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with id {session_id} not found"
        )
    
    # Convert status to enum if provided
    status_enum = None
    if session_data.status:
        status_enum = SessionStatusEnum(session_data.status.value)
    
    try:
        updated_session = update_session(
            db,
            session_id=session_id,
            session_name=session_data.session_name,
            description=session_data.description,
            status=status_enum
        )
        
        return session_to_response(updated_session)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update session: {str(e)}"
        )


@router.delete("/{session_id}", response_model=APIResponse)
def delete_session_by_id(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a session and all associated data (roadmap, goals, materials).
    
    - **session_id**: Session ID
    
    **Warning**: This operation cascades and will delete all related data.
    """
    # Check if session exists
    existing_session = get_session(db, session_id)
    if not existing_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with id {session_id} not found"
        )
    
    try:
        success = delete_session(db, session_id)
        
        if success:
            return APIResponse(
                success=True,
                data={"message": f"Session {session_id} deleted successfully"}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete session"
            )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete session: {str(e)}"
        )


@router.get("/{session_id}/full", response_model=APIResponse)
def get_full_session_data(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Get complete session data including roadmap, goals, and learning materials.
    
    - **session_id**: Session ID
    
    Uses eager loading for efficient data retrieval.
    """
    session = get_session_with_full_roadmap(db, session_id)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with id {session_id} not found"
        )
    
    # Build comprehensive response
    session_data = {
        "session": {
            "id": session.id,
            "user_id": session.user_id,
            "session_name": session.session_name,
            "description": session.description,
            "status": session.status.value,
            "created_at": format_datetime(session.created_at),
            "updated_at": format_datetime(session.updated_at),
            "completed_at": format_datetime(session.completed_at)
        },
        "roadmap": None,
        "goals": [],
        "materials": []
    }
    
    if session.roadmap:
        roadmap = session.roadmap
        session_data["roadmap"] = {
            "id": roadmap.id,
            "user_request": roadmap.user_request,
            "total_estimated_weeks": roadmap.total_estimated_weeks,
            "graduation_project": roadmap.graduation_project,
            "graduation_project_title": roadmap.graduation_project_title,
            "status": roadmap.status.value,
            "created_at": format_datetime(roadmap.created_at)
        }
        
        for goal in roadmap.goals:
            goal_data = {
                "id": goal.id,
                "goal_number": goal.goal_number,
                "title": goal.title,
                "description": goal.description,
                "priority": goal.priority,
                "skill_level": goal.skill_level.value,
                "estimated_hours": goal.estimated_hours,
                "actual_hours_spent": goal.actual_hours_spent,
                "is_completed": goal.is_completed,
                "completion_percentage": goal.completion_percentage,
                "started_at": format_datetime(goal.started_at),
                "completed_at": format_datetime(goal.completed_at)
            }
            session_data["goals"].append(goal_data)
            
            for material in goal.learning_materials:
                material_data = {
                    "id": material.id,
                    "goal_id": material.goal_id,
                    "title": material.title,
                    "material_type": material.material_type,
                    "description": material.description,
                    "source_url": material.source_url,
                    "estimated_time_minutes": material.estimated_time_minutes,
                    "difficulty_level": material.difficulty_level.value if material.difficulty_level else None,
                    "is_completed": material.is_completed,
                    "user_rating": material.user_rating,
                    "relevance_score": material.relevance_score,
                    "quality_score": material.quality_score
                }
                session_data["materials"].append(material_data)
    
    return APIResponse(success=True, data=session_data)


@router.get("/{session_id}/progress", response_model=SessionProgressStats)
def get_session_progress(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Get progress statistics for a session.
    
    - **session_id**: Session ID
    
    Returns completion statistics for goals and materials.
    """
    session = get_session(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with id {session_id} not found"
        )
    
    roadmap = get_roadmap_by_session(db, session_id)
    
    stats = {
        "total_goals": 0,
        "completed_goals": 0,
        "total_materials": 0,
        "completed_materials": 0,
        "total_hours_estimated": 0,
        "total_hours_spent": 0,
        "completion_percentage": 0.0
    }
    
    if roadmap:
        goals = get_goals_by_roadmap(db, roadmap.id)
        stats["total_goals"] = len(goals)
        
        for goal in goals:
            if goal.is_completed:
                stats["completed_goals"] += 1
            if goal.estimated_hours:
                stats["total_hours_estimated"] += goal.estimated_hours
            if goal.actual_hours_spent:
                stats["total_hours_spent"] += goal.actual_hours_spent
            
            # Count materials
            materials = goal.learning_materials
            stats["total_materials"] += len(materials)
            stats["completed_materials"] += sum(1 for m in materials if m.is_completed)
        
        # Calculate overall completion percentage
        if stats["total_goals"] > 0:
            stats["completion_percentage"] = round(
                (stats["completed_goals"] / stats["total_goals"]) * 100, 2
            )
    
    return SessionProgressStats(**stats)


@router.post("/{session_id}/complete", response_model=SessionResponse)
def complete_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Mark a session as completed.
    
    - **session_id**: Session ID
    """
    session = get_session(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with id {session_id} not found"
        )
    
    updated_session = update_session(
        db,
        session_id=session_id,
        status=SessionStatusEnum.COMPLETED
    )
    
    return session_to_response(updated_session)


@router.post("/{session_id}/archive", response_model=SessionResponse)
def archive_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Archive a session.
    
    - **session_id**: Session ID
    """
    session = get_session(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with id {session_id} not found"
        )
    
    updated_session = update_session(
        db,
        session_id=session_id,
        status=SessionStatusEnum.ARCHIVED
    )
    
    return session_to_response(updated_session)


@router.get("/user/{user_id}/stats", response_model=APIResponse)
def get_user_session_stats(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get overall session statistics for a user.
    
    - **user_id**: User ID
    """
    stats = {
        "total_sessions": count_user_sessions(db, user_id),
        "active_sessions": count_user_sessions(db, user_id, status=SessionStatusEnum.ACTIVE),
        "completed_sessions": count_user_sessions(db, user_id, status=SessionStatusEnum.COMPLETED),
        "archived_sessions": count_user_sessions(db, user_id, status=SessionStatusEnum.ARCHIVED)
    }
    
    return APIResponse(success=True, data=stats)


# ============================================================================
# MESSAGE ROUTES
# ============================================================================

@router.post("/{session_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def add_message(
    session_id: int,
    message_data: MessageCreate,
    db: Session = Depends(get_db)
):
    """
    Add a message to a session's chat history.
    
    - **session_id**: Session ID
    - **role**: Message role (user, assistant, system)
    - **content**: Message content
    - **metadata**: Optional metadata (e.g., model, tokens)
    """
    try:
        updated_session = add_message_to_session(
            db,
            session_id=session_id,
            role=message_data.role.value,
            content=message_data.content,
            metadata=message_data.metadata
        )
        
        # Return the last message (the one just added)
        last_message = updated_session.messages[-1]
        return MessageResponse(**last_message)
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add message: {str(e)}"
        )


@router.get("/{session_id}/messages", response_model=MessagesListResponse)
def get_messages(
    session_id: int,
    limit: Optional[int] = Query(None, ge=1, le=1000, description="Limit number of messages (most recent)"),
    role: Optional[str] = Query(None, description="Filter by role (user, assistant, system)"),
    db: Session = Depends(get_db)
):
    """
    Get messages from a session.
    
    - **session_id**: Session ID
    - **limit**: Optional limit for number of messages (returns most recent)
    - **role**: Optional filter by role
    """
    # Check if session exists
    session = get_session(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with id {session_id} not found"
        )
    
    messages = get_session_messages(
        db,
        session_id=session_id,
        limit=limit,
        role_filter=role
    )
    
    return MessagesListResponse(
        session_id=session_id,
        messages=[MessageResponse(**msg) for msg in messages],
        total=len(messages)
    )


@router.get("/{session_id}/messages/recent", response_model=MessagesListResponse)
def get_recent_messages(
    session_id: int,
    n: int = Query(10, ge=1, le=100, description="Number of recent messages to retrieve"),
    db: Session = Depends(get_db)
):
    """
    Get the N most recent messages from a session.
    
    - **session_id**: Session ID
    - **n**: Number of recent messages (default: 10, max: 100)
    """
    # Check if session exists
    session = get_session(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with id {session_id} not found"
        )
    
    messages = get_last_n_messages(db, session_id, n=n)
    
    return MessagesListResponse(
        session_id=session_id,
        messages=[MessageResponse(**msg) for msg in messages],
        total=len(messages)
    )


@router.delete("/{session_id}/messages", response_model=APIResponse)
def clear_messages(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Clear all messages from a session.
    
    - **session_id**: Session ID
    
    **Warning**: This will delete all chat history for the session.
    """
    try:
        clear_session_messages(db, session_id)
        return APIResponse(
            success=True,
            data={"message": f"All messages cleared from session {session_id}"}
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear messages: {str(e)}"
        )


@router.get("/{session_id}/messages/count", response_model=APIResponse)
def get_message_count(
    session_id: int,
    role: Optional[str] = Query(None, description="Filter by role (user, assistant, system)"),
    db: Session = Depends(get_db)
):
    """
    Count messages in a session.
    
    - **session_id**: Session ID
    - **role**: Optional filter by role
    """
    # Check if session exists
    session = get_session(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with id {session_id} not found"
        )
    
    count = count_session_messages(db, session_id, role_filter=role)
    
    return APIResponse(
        success=True,
        data={
            "session_id": session_id,
            "message_count": count,
            "role_filter": role
        }
    )

