"""
Database CRUD operations for all models.
Contains create, read, update, and delete functions for:
- Session
- Roadmap
- RoadmapGoal
- LearningMaterial
- UserSkill
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from typing import List, Optional, Dict, Any
from datetime import datetime

from models.db_models import (
    Session as SessionModel,
    Roadmap,
    RoadmapGoal,
    LearningMaterial,
    UserSkill,
    Quiz,
    QuizQuestion,
    QuizAttempt,
    QuizAnswer,
    SessionStatusEnum,
    RoadmapStatusEnum,
    SkillLevelEnum
)


# ============================================================================
# SESSION OPERATIONS
# ============================================================================

def create_session(
    db: Session,
    user_id: str,
    session_name: Optional[str] = None,
    description: Optional[str] = None,
    status: SessionStatusEnum = SessionStatusEnum.ACTIVE
) -> SessionModel:
    """Create a new learning session."""
    session = SessionModel(
        user_id=user_id,
        session_name=session_name,
        description=description,
        status=status,
        messages=[]  # Initialize empty messages list
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_session(db: Session, session_id: int) -> Optional[SessionModel]:
    """Get a session by ID."""
    return db.query(SessionModel).filter(SessionModel.id == session_id).first()


def get_sessions_by_user(
    db: Session,
    user_id: str,
    status: Optional[SessionStatusEnum] = None,
    skip: int = 0,
    limit: int = 100
) -> List[SessionModel]:
    """Get all sessions for a user with optional status filter."""
    query = db.query(SessionModel).filter(SessionModel.user_id == user_id)
    
    if status:
        query = query.filter(SessionModel.status == status)
    
    return query.order_by(desc(SessionModel.created_at)).offset(skip).limit(limit).all()


def update_session(
    db: Session,
    session_id: int,
    session_name: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[SessionStatusEnum] = None
) -> Optional[SessionModel]:
    """Update a session."""
    session = get_session(db, session_id)
    if not session:
        return None
    
    if session_name is not None:
        session.session_name = session_name
    if description is not None:
        session.description = description
    if status is not None:
        session.status = status
        if status == SessionStatusEnum.COMPLETED:
            session.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(session)
    return session


def delete_session(db: Session, session_id: int) -> bool:
    """Delete a session (cascades to roadmap, goals, and materials)."""
    session = get_session(db, session_id)
    if not session:
        return False
    
    db.delete(session)
    db.commit()
    return True


def count_user_sessions(db: Session, user_id: str, status: Optional[SessionStatusEnum] = None) -> int:
    """Count sessions for a user."""
    query = db.query(SessionModel).filter(SessionModel.user_id == user_id)
    if status:
        query = query.filter(SessionModel.status == status)
    return query.count()


# ============================================================================
# MESSAGE OPERATIONS (for Session Chat)
# ============================================================================

def add_message_to_session(
    db: Session,
    session_id: int,
    role: str,
    content: str,
    metadata: Optional[Dict[str, Any]] = None
) -> SessionModel:
    """
    Add a message to a session's message history.
    
    Args:
        session_id: Session ID
        role: Message role (e.g., 'user', 'assistant', 'system')
        content: Message content
        metadata: Optional metadata (e.g., tokens, model, timestamp)
    
    Returns:
        Updated session with new message
    """
    session = get_session(db, session_id)
    if not session:
        raise ValueError(f"Session {session_id} not found")
    
    # Initialize messages if None
    if session.messages is None:
        session.messages = []
    
    # Create message object
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.utcnow().isoformat(),
        "metadata": metadata or {}
    }
    
    # Append message
    session.messages.append(message)
    
    # Mark as modified to trigger SQLAlchemy update
    from sqlalchemy.orm.attributes import flag_modified
    flag_modified(session, "messages")
    
    db.commit()
    db.refresh(session)
    return session


def get_session_messages(
    db: Session,
    session_id: int,
    limit: Optional[int] = None,
    role_filter: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get messages from a session.
    
    Args:
        session_id: Session ID
        limit: Maximum number of messages to return (newest first)
        role_filter: Filter by role (e.g., 'user', 'assistant')
    
    Returns:
        List of messages
    """
    session = get_session(db, session_id)
    if not session:
        return []
    
    messages = session.messages or []
    
    # Filter by role if specified
    if role_filter:
        messages = [m for m in messages if m.get("role") == role_filter]
    
    # Limit results (get most recent)
    if limit and limit > 0:
        messages = messages[-limit:]
    
    return messages


def get_last_n_messages(
    db: Session,
    session_id: int,
    n: int = 10
) -> List[Dict[str, Any]]:
    """
    Get the last N messages from a session.
    
    Args:
        session_id: Session ID
        n: Number of recent messages to retrieve
    
    Returns:
        List of last N messages
    """
    return get_session_messages(db, session_id, limit=n)


def clear_session_messages(
    db: Session,
    session_id: int
) -> SessionModel:
    """
    Clear all messages from a session.
    
    Args:
        session_id: Session ID
    
    Returns:
        Updated session with cleared messages
    """
    session = get_session(db, session_id)
    if not session:
        raise ValueError(f"Session {session_id} not found")
    
    session.messages = []
    
    from sqlalchemy.orm.attributes import flag_modified
    flag_modified(session, "messages")
    
    db.commit()
    db.refresh(session)
    return session


def count_session_messages(
    db: Session,
    session_id: int,
    role_filter: Optional[str] = None
) -> int:
    """
    Count messages in a session.
    
    Args:
        session_id: Session ID
        role_filter: Optional role filter
    
    Returns:
        Number of messages
    """
    messages = get_session_messages(db, session_id, role_filter=role_filter)
    return len(messages)


def delete_message_from_session(
    db: Session,
    session_id: int,
    message_index: int
) -> SessionModel:
    """
    Delete a specific message from a session by index.
    
    Args:
        session_id: Session ID
        message_index: Index of message to delete (0-based)
    
    Returns:
        Updated session
    """
    session = get_session(db, session_id)
    if not session:
        raise ValueError(f"Session {session_id} not found")
    
    if session.messages and 0 <= message_index < len(session.messages):
        session.messages.pop(message_index)
        
        from sqlalchemy.orm.attributes import flag_modified
        flag_modified(session, "messages")
        
        db.commit()
        db.refresh(session)
    
    return session


def update_message_in_session(
    db: Session,
    session_id: int,
    message_index: int,
    content: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> SessionModel:
    """
    Update a specific message in a session.
    
    Args:
        session_id: Session ID
        message_index: Index of message to update (0-based)
        content: New content (if provided)
        metadata: New metadata to merge (if provided)
    
    Returns:
        Updated session
    """
    session = get_session(db, session_id)
    if not session:
        raise ValueError(f"Session {session_id} not found")
    
    if session.messages and 0 <= message_index < len(session.messages):
        message = session.messages[message_index]
        
        if content is not None:
            message["content"] = content
        
        if metadata is not None:
            message["metadata"] = {**message.get("metadata", {}), **metadata}
        
        message["updated_at"] = datetime.utcnow().isoformat()
        
        from sqlalchemy.orm.attributes import flag_modified
        flag_modified(session, "messages")
        
        db.commit()
        db.refresh(session)
    
    return session


# ============================================================================
# ROADMAP OPERATIONS
# ============================================================================

def create_roadmap(
    db: Session,
    session_id: int,
    user_request: str,
    user_summarized_cv: Optional[str] = None,
    user_expertise_domains: Optional[List[str]] = None,
    job_listings: Optional[List[str]] = None,
    total_estimated_weeks: Optional[int] = None,
    graduation_project: Optional[str] = None,
    graduation_project_title: Optional[str] = None,
    graduation_project_requirements: Optional[List[str]] = None,
    graduation_project_estimated_hours: Optional[int] = None
) -> Roadmap:
    """Create a new roadmap for a session."""
    roadmap = Roadmap(
        session_id=session_id,
        user_request=user_request,
        user_summarized_cv=user_summarized_cv,
        user_expertise_domains=user_expertise_domains,
        job_listings=job_listings,
        total_estimated_weeks=total_estimated_weeks,
        graduation_project=graduation_project,
        graduation_project_title=graduation_project_title,
        graduation_project_requirements=graduation_project_requirements,
        graduation_project_estimated_hours=graduation_project_estimated_hours
    )
    db.add(roadmap)
    db.commit()
    db.refresh(roadmap)
    return roadmap


def get_roadmap(db: Session, roadmap_id: int) -> Optional[Roadmap]:
    """Get a roadmap by ID."""
    return db.query(Roadmap).filter(Roadmap.id == roadmap_id).first()


def get_roadmap_by_session(db: Session, session_id: int) -> Optional[Roadmap]:
    """Get roadmap for a specific session."""
    return db.query(Roadmap).filter(Roadmap.session_id == session_id).first()


def update_roadmap(
    db: Session,
    roadmap_id: int,
    **kwargs
) -> Optional[Roadmap]:
    """Update roadmap fields."""
    roadmap = get_roadmap(db, roadmap_id)
    if not roadmap:
        return None
    
    # Update allowed fields
    allowed_fields = [
        'user_request', 'user_summarized_cv', 'user_expertise_domains',
        'job_listings', 'total_estimated_weeks', 'graduation_project',
        'graduation_project_title', 'graduation_project_requirements',
        'graduation_project_estimated_hours', 'status'
    ]
    
    for field, value in kwargs.items():
        if field in allowed_fields and value is not None:
            setattr(roadmap, field, value)
            
    if kwargs.get('status') == RoadmapStatusEnum.COMPLETED:
        roadmap.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(roadmap)
    return roadmap


def delete_roadmap(db: Session, roadmap_id: int) -> bool:
    """Delete a roadmap (cascades to goals and materials)."""
    roadmap = get_roadmap(db, roadmap_id)
    if not roadmap:
        return False
    
    db.delete(roadmap)
    db.commit()
    return True


# ============================================================================
# ROADMAP GOAL OPERATIONS
# ============================================================================

def create_goal(
    db: Session,
    roadmap_id: int,
    goal_number: int,
    title: str,
    description: str,
    priority: int = 3,
    skill_level: SkillLevelEnum = SkillLevelEnum.BEGINNER,
    estimated_hours: Optional[int] = None,
    prerequisites: Optional[List[str]] = None
) -> RoadmapGoal:
    """Create a new roadmap goal."""
    goal = RoadmapGoal(
        roadmap_id=roadmap_id,
        goal_number=goal_number,
        title=title,
        description=description,
        priority=priority,
        skill_level=skill_level,
        estimated_hours=estimated_hours,
        prerequisites=prerequisites
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal


def get_goal(db: Session, goal_id: int) -> Optional[RoadmapGoal]:
    """Get a goal by ID."""
    return db.query(RoadmapGoal).filter(RoadmapGoal.id == goal_id).first()


def get_goals_by_roadmap(
    db: Session,
    roadmap_id: int,
    completed_only: bool = False,
    skip: int = 0,
    limit: int = 100
) -> List[RoadmapGoal]:
    """Get all goals for a roadmap."""
    query = db.query(RoadmapGoal).filter(RoadmapGoal.roadmap_id == roadmap_id)
    
    if completed_only:
        query = query.filter(RoadmapGoal.is_completed == True)
    
    return query.order_by(RoadmapGoal.goal_number).offset(skip).limit(limit).all()


def update_goal(
    db: Session,
    goal_id: int,
    **kwargs
) -> Optional[RoadmapGoal]:
    """Update goal fields."""
    goal = get_goal(db, goal_id)
    if not goal:
        return None
    
    allowed_fields = [
        'title', 'description', 'priority', 'skill_level', 'estimated_hours',
        'actual_hours_spent', 'prerequisites', 'is_completed', 
        'completion_percentage', 'started_at'
    ]
    
    for field, value in kwargs.items():
        if field in allowed_fields and value is not None:
            setattr(goal, field, value)
    
    # Handle completion
    if kwargs.get('is_completed') == True and not goal.completed_at:
        goal.completed_at = datetime.utcnow()
        goal.completion_percentage = 100.0
    
    # Handle starting
    if kwargs.get('started_at') and not goal.started_at:
        goal.started_at = kwargs.get('started_at')
    
    db.commit()
    db.refresh(goal)
    return goal


def mark_goal_started(db: Session, goal_id: int) -> Optional[RoadmapGoal]:
    """Mark a goal as started."""
    goal = get_goal(db, goal_id)
    if not goal or goal.started_at:
        return goal
    
    goal.started_at = datetime.utcnow()
    db.commit()
    db.refresh(goal)
    return goal


def mark_goal_completed(db: Session, goal_id: int) -> Optional[RoadmapGoal]:
    """Mark a goal as completed."""
    return update_goal(
        db,
        goal_id,
        is_completed=True,
        completion_percentage=100.0
    )


def update_goal_progress(
    db: Session,
    goal_id: int,
    completion_percentage: float,
    actual_hours_spent: Optional[int] = None
) -> Optional[RoadmapGoal]:
    """Update goal progress."""
    updates = {'completion_percentage': completion_percentage}
    if actual_hours_spent is not None:
        updates['actual_hours_spent'] = actual_hours_spent
    
    if completion_percentage >= 100.0:
        updates['is_completed'] = True
    
    return update_goal(db, goal_id, **updates)


def delete_goal(db: Session, goal_id: int) -> bool:
    """Delete a goal (cascades to learning materials)."""
    goal = get_goal(db, goal_id)
    if not goal:
        return False
    
    db.delete(goal)
    db.commit()
    return True


def count_goals_by_roadmap(
    db: Session,
    roadmap_id: int,
    completed_only: bool = False
) -> int:
    """Count goals in a roadmap."""
    query = db.query(RoadmapGoal).filter(RoadmapGoal.roadmap_id == roadmap_id)
    if completed_only:
        query = query.filter(RoadmapGoal.is_completed == True)
    return query.count()


# ============================================================================
# LEARNING MATERIAL OPERATIONS
# ============================================================================

def create_learning_material(
    db: Session,
    goal_id: int,
    title: str,
    material_type: str,
    content: Optional[str] = None,
    source_url: Optional[str] = None,
    description: Optional[str] = None,
    estimated_time_minutes: Optional[int] = None,
    difficulty_level: Optional[SkillLevelEnum] = None,
    end_of_material_project: Optional[str] = None,
    project_requirements: Optional[List[str]] = None,
    relevance_score: Optional[float] = None,
    quality_score: Optional[float] = None
) -> LearningMaterial:
    """Create a new learning material."""
    material = LearningMaterial(
        goal_id=goal_id,
        title=title,
        material_type=material_type,
        content=content,
        source_url=source_url,
        description=description,
        estimated_time_minutes=estimated_time_minutes,
        difficulty_level=difficulty_level,
        end_of_material_project=end_of_material_project,
        project_requirements=project_requirements,
        relevance_score=relevance_score,
        quality_score=quality_score
    )
    db.add(material)
    db.commit()
    db.refresh(material)
    return material


def get_learning_material(db: Session, material_id: int) -> Optional[LearningMaterial]:
    """Get a learning material by ID."""
    return db.query(LearningMaterial).filter(LearningMaterial.id == material_id).first()


def get_materials_by_goal(
    db: Session,
    goal_id: int,
    material_type: Optional[str] = None,
    completed_only: bool = False,
    skip: int = 0,
    limit: int = 100
) -> List[LearningMaterial]:
    """Get all learning materials for a goal."""
    query = db.query(LearningMaterial).filter(LearningMaterial.goal_id == goal_id)
    
    if material_type:
        query = query.filter(LearningMaterial.material_type == material_type)
    
    if completed_only:
        query = query.filter(LearningMaterial.is_completed == True)
    
    return query.order_by(desc(LearningMaterial.relevance_score)).offset(skip).limit(limit).all()


def get_materials_by_roadmap(
    db: Session,
    roadmap_id: int,
    material_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[LearningMaterial]:
    """Get all learning materials for a roadmap (across all goals)."""
    query = db.query(LearningMaterial).join(RoadmapGoal).filter(
        RoadmapGoal.roadmap_id == roadmap_id
    )
    
    if material_type:
        query = query.filter(LearningMaterial.material_type == material_type)
    
    return query.order_by(desc(LearningMaterial.relevance_score)).offset(skip).limit(limit).all()


def update_learning_material(
    db: Session,
    material_id: int,
    **kwargs
) -> Optional[LearningMaterial]:
    """Update learning material fields."""
    material = get_learning_material(db, material_id)
    if not material:
        return None
    
    allowed_fields = [
        'title', 'content', 'source_url', 'description', 'material_type',
        'estimated_time_minutes', 'difficulty_level', 'end_of_material_project',
        'project_requirements', 'relevance_score', 'quality_score',
        'is_completed', 'user_rating', 'user_notes'
    ]
    
    for field, value in kwargs.items():
        if field in allowed_fields and value is not None:
            setattr(material, field, value)
    
    if kwargs.get('is_completed') == True and not material.completed_at:
        material.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(material)
    return material


def mark_material_completed(
    db: Session,
    material_id: int,
    user_rating: Optional[int] = None,
    user_notes: Optional[str] = None
) -> Optional[LearningMaterial]:
    """Mark a learning material as completed."""
    updates = {'is_completed': True}
    if user_rating is not None:
        updates['user_rating'] = user_rating
    if user_notes is not None:
        updates['user_notes'] = user_notes
    
    return update_learning_material(db, material_id, **updates)


def delete_learning_material(db: Session, material_id: int) -> bool:
    """Delete a learning material."""
    material = get_learning_material(db, material_id)
    if not material:
        return False
    
    db.delete(material)
    db.commit()
    return True


def count_materials_by_goal(
    db: Session,
    goal_id: int,
    completed_only: bool = False
) -> int:
    """Count learning materials for a goal."""
    query = db.query(LearningMaterial).filter(LearningMaterial.goal_id == goal_id)
    if completed_only:
        query = query.filter(LearningMaterial.is_completed == True)
    return query.count()


# ============================================================================
# USER SKILL OPERATIONS
# ============================================================================

def create_user_skill(
    db: Session,
    user_id: str,
    skill_name: str,
    skill_level: SkillLevelEnum = SkillLevelEnum.BEGINNER,
    confidence_score: float = 0.8,
    source: str = "cv",
    verified: bool = False
) -> UserSkill:
    """Create a new user skill."""
    skill = UserSkill(
        user_id=user_id,
        skill_name=skill_name,
        skill_level=skill_level,
        confidence_score=confidence_score,
        source=source,
        verified=verified
    )
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


def get_user_skill(db: Session, skill_id: int) -> Optional[UserSkill]:
    """Get a user skill by ID."""
    return db.query(UserSkill).filter(UserSkill.id == skill_id).first()


def get_user_skills(
    db: Session,
    user_id: str,
    skill_level: Optional[SkillLevelEnum] = None,
    verified_only: bool = False,
    skip: int = 0,
    limit: int = 100
) -> List[UserSkill]:
    """Get all skills for a user."""
    query = db.query(UserSkill).filter(UserSkill.user_id == user_id)
    
    if skill_level:
        query = query.filter(UserSkill.skill_level == skill_level)
    
    if verified_only:
        query = query.filter(UserSkill.verified == True)
    
    return query.order_by(desc(UserSkill.confidence_score)).offset(skip).limit(limit).all()


def get_user_skill_by_name(
    db: Session,
    user_id: str,
    skill_name: str
) -> Optional[UserSkill]:
    """Get a specific skill for a user by skill name."""
    return db.query(UserSkill).filter(
        and_(
            UserSkill.user_id == user_id,
            UserSkill.skill_name == skill_name
        )
    ).first()


def update_user_skill(
    db: Session,
    skill_id: int,
    skill_level: Optional[SkillLevelEnum] = None,
    confidence_score: Optional[float] = None,
    verified: Optional[bool] = None
) -> Optional[UserSkill]:
    """Update a user skill."""
    skill = get_user_skill(db, skill_id)
    if not skill:
        return None
    
    if skill_level is not None:
        skill.skill_level = skill_level
    if confidence_score is not None:
        skill.confidence_score = confidence_score
    if verified is not None:
        skill.verified = verified
    
    db.commit()
    db.refresh(skill)
    return skill


def upsert_user_skill(
    db: Session,
    user_id: str,
    skill_name: str,
    skill_level: SkillLevelEnum,
    confidence_score: float = 0.8,
    source: str = "cv",
    verified: bool = False
) -> UserSkill:
    """Create or update a user skill."""
    existing_skill = get_user_skill_by_name(db, user_id, skill_name)
    
    if existing_skill:
        existing_skill.skill_level = skill_level
        existing_skill.confidence_score = confidence_score
        existing_skill.source = source
        existing_skill.verified = verified
        db.commit()
        db.refresh(existing_skill)
        return existing_skill
    else:
        return create_user_skill(
            db, user_id, skill_name, skill_level, 
            confidence_score, source, verified
        )


def delete_user_skill(db: Session, skill_id: int) -> bool:
    """Delete a user skill."""
    skill = get_user_skill(db, skill_id)
    if not skill:
        return False
    
    db.delete(skill)
    db.commit()
    return True


def bulk_create_user_skills(
    db: Session,
    user_id: str,
    skills: List[Dict[str, Any]]
) -> List[UserSkill]:
    """Bulk create user skills from a list of skill dictionaries."""
    skill_objects = []
    for skill_data in skills:
        skill = UserSkill(
            user_id=user_id,
            skill_name=skill_data['skill_name'],
            skill_level=skill_data.get('skill_level', SkillLevelEnum.BEGINNER),
            confidence_score=skill_data.get('confidence_score', 0.8),
            source=skill_data.get('source', 'cv'),
            verified=skill_data.get('verified', False)
        )
        skill_objects.append(skill)
    
    db.add_all(skill_objects)
    db.commit()
    for skill in skill_objects:
        db.refresh(skill)
    
    return skill_objects


# ============================================================================
# AGGREGATE/COMPLEX QUERIES
# ============================================================================

def get_session_with_full_roadmap(db: Session, session_id: int) -> Optional[SessionModel]:
    """Get session with all related data (roadmap, goals, materials)."""
    from sqlalchemy.orm import joinedload
    
    return db.query(SessionModel).filter(
        SessionModel.id == session_id
    ).options(
        joinedload(SessionModel.roadmap)
        .joinedload(Roadmap.goals)
        .joinedload(RoadmapGoal.learning_materials)
    ).first()


def get_user_progress_stats(db: Session, user_id: str) -> Dict[str, Any]:
    """Get comprehensive progress statistics for a user."""
    sessions = get_sessions_by_user(db, user_id)
    
    stats = {
        'total_sessions': len(sessions),
        'active_sessions': len([s for s in sessions if s.status == SessionStatusEnum.ACTIVE]),
        'completed_sessions': len([s for s in sessions if s.status == SessionStatusEnum.COMPLETED]),
        'total_goals': 0,
        'completed_goals': 0,
        'total_materials': 0,
        'completed_materials': 0,
        'total_hours_estimated': 0,
        'total_hours_spent': 0
    }
    
    for session in sessions:
        roadmap = get_roadmap_by_session(db, session.id)
        if roadmap:
            goals = get_goals_by_roadmap(db, roadmap.id)
            stats['total_goals'] += len(goals)
            
            for goal in goals:
                if goal.is_completed:
                    stats['completed_goals'] += 1
                if goal.estimated_hours:
                    stats['total_hours_estimated'] += goal.estimated_hours
                if goal.actual_hours_spent:
                    stats['total_hours_spent'] += goal.actual_hours_spent
                
                materials = get_materials_by_goal(db, goal.id)
                stats['total_materials'] += len(materials)
                stats['completed_materials'] += len([m for m in materials if m.is_completed])
    
    return stats


def get_next_incomplete_goal(db: Session, roadmap_id: int) -> Optional[RoadmapGoal]:
    """Get the next incomplete goal in a roadmap (by goal_number)."""
    return db.query(RoadmapGoal).filter(
        and_(
            RoadmapGoal.roadmap_id == roadmap_id,
            RoadmapGoal.is_completed == False
        )
    ).order_by(RoadmapGoal.goal_number).first()


def search_learning_materials(
    db: Session,
    roadmap_id: int,
    search_term: str,
    skip: int = 0,
    limit: int = 50
) -> List[LearningMaterial]:
    """Search learning materials by title or description."""
    search_pattern = f"%{search_term}%"
    
    return db.query(LearningMaterial).join(RoadmapGoal).filter(
        and_(
            RoadmapGoal.roadmap_id == roadmap_id,
            or_(
                LearningMaterial.title.ilike(search_pattern),
                LearningMaterial.description.ilike(search_pattern)
            )
        )
    ).offset(skip).limit(limit).all()


# ============================================================================
# GRADUATION PROJECT QUESTIONS OPERATIONS
# ============================================================================

from models.db_models import GraduationProjectQuestion, GraduationProjectSubmission, QuestionDifficultyEnum


def create_graduation_project_question(
    db: Session,
    session_id: int,
    question_id: str,
    prompt: str,
    rationale: str,
    goals_covered: List[int],
    materials_covered: List[int],
    expected_competencies: List[str],
    difficulty: QuestionDifficultyEnum,
    estimated_time_minutes: int,
    evaluation_rubric: List[str],
    answer_min_chars: int = 500,
    answer_max_chars: int = 2500,
    requires_material_citations: bool = False
) -> GraduationProjectQuestion:
    """Create a new graduation project question."""
    question = GraduationProjectQuestion(
        session_id=session_id,
        question_id=question_id,
        prompt=prompt,
        rationale=rationale,
        goals_covered=goals_covered,
        materials_covered=materials_covered,
        expected_competencies=expected_competencies,
        difficulty=difficulty,
        estimated_time_minutes=estimated_time_minutes,
        evaluation_rubric=evaluation_rubric,
        answer_min_chars=answer_min_chars,
        answer_max_chars=answer_max_chars,
        requires_material_citations=requires_material_citations
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question

# QUIZ OPERATIONS
# ============================================================================

def create_quiz(
    db: Session,
    goal_id: int,
    title: str,
    description: Optional[str] = None,
    time_limit_minutes: Optional[int] = None,
    passing_score_percentage: float = 70.0,
    max_attempts: int = 3,
    questions_data: Optional[List[Dict[str, Any]]] = None
) -> Quiz:
    """Create a new quiz with questions."""
    quiz = Quiz(
        goal_id=goal_id,
        title=title,
        description=description,
        time_limit_minutes=time_limit_minutes,
        passing_score_percentage=passing_score_percentage,
        max_attempts=max_attempts,
        total_questions=len(questions_data) if questions_data else 0
    )
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    
    # Add questions if provided
    if questions_data:
        for i, question_data in enumerate(questions_data):
            create_quiz_question(
                db=db,
                quiz_id=quiz.id,
                question_text=question_data['question_text'],
                question_order=i + 1,
                options=question_data['options'],
                correct_answer=question_data['correct_answer'],
                explanation=question_data.get('explanation'),
                points=question_data.get('points', 1)
            )
        
        # Update total questions count
        quiz.total_questions = len(questions_data)
        db.commit()
        db.refresh(quiz)
    
    return quiz


def get_quiz(db: Session, quiz_id: int) -> Optional[Quiz]:
    """Get a quiz by ID."""
    return db.query(Quiz).filter(Quiz.id == quiz_id).first()


def get_quizzes_by_goal(
    db: Session,
    goal_id: int,
    active_only: bool = True,
    skip: int = 0,
    limit: int = 100
) -> List[Quiz]:
    """Get all quizzes for a goal."""
    query = db.query(Quiz).filter(Quiz.goal_id == goal_id)
    
    if active_only:
        query = query.filter(Quiz.is_active == True)
    
    return query.order_by(desc(Quiz.created_at)).offset(skip).limit(limit).all()


def get_quizzes_by_roadmap(
    db: Session,
    roadmap_id: int,
    active_only: bool = True,
    skip: int = 0,
    limit: int = 100
) -> List[Quiz]:
    """Get all quizzes for a roadmap (across all goals)."""
    query = db.query(Quiz).join(RoadmapGoal).filter(
        RoadmapGoal.roadmap_id == roadmap_id
    )
    
    if active_only:
        query = query.filter(Quiz.is_active == True)
    
    return query.order_by(desc(Quiz.created_at)).offset(skip).limit(limit).all()


def update_quiz(
    db: Session,
    quiz_id: int,
    **kwargs
) -> Optional[Quiz]:
    """Update quiz fields."""
    quiz = get_quiz(db, quiz_id)
    if not quiz:
        return None
    
    allowed_fields = [
        'title', 'description', 'difficulty_level', 'time_limit_minutes',
        'passing_score_percentage', 'max_attempts', 'is_active'
    ]
    
    for field, value in kwargs.items():
        if field in allowed_fields and value is not None:
            setattr(quiz, field, value)
    
    db.commit()
    db.refresh(quiz)
    return quiz


def delete_quiz(db: Session, quiz_id: int) -> bool:
    """Delete a quiz (cascades to questions, attempts, and answers)."""
    quiz = get_quiz(db, quiz_id)
    if not quiz:
        return False
    
    db.delete(quiz)
    db.commit()
    return True


def count_quizzes_by_goal(
    db: Session,
    goal_id: int,
    active_only: bool = True
) -> int:
    """Count quizzes for a goal."""
    query = db.query(Quiz).filter(Quiz.goal_id == goal_id)
    if active_only:
        query = query.filter(Quiz.is_active == True)
    return query.count()


# ============================================================================
# QUIZ QUESTION OPERATIONS
# ============================================================================

def create_quiz_question(
    db: Session,
    quiz_id: int,
    question_text: str,
    question_order: int,
    options: List[str],
    correct_answer: str,
    explanation: Optional[str] = None,
    points: int = 1
) -> QuizQuestion:
    """Create a new quiz question."""
    question = QuizQuestion(
        quiz_id=quiz_id,
        question_text=question_text,
        question_order=question_order,
        options=options,
        correct_answer=correct_answer,
        explanation=explanation,
        points=points
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def get_graduation_project_questions_by_session(
    db: Session,
    session_id: int
) -> List[GraduationProjectQuestion]:
    """Get all graduation project questions for a session."""
    return db.query(GraduationProjectQuestion).filter(
        GraduationProjectQuestion.session_id == session_id
    ).all()


def get_graduation_project_question_by_slug(
    db: Session,
    question_id: str
) -> Optional[GraduationProjectQuestion]:
    """Get a graduation project question by its slug."""
    return db.query(GraduationProjectQuestion).filter(
        GraduationProjectQuestion.question_id == question_id
    ).first()


def create_graduation_project_submission(
    db: Session,
    session_id: int,
    question_id: int,
    answer_text: str,
    citations: Optional[List[Dict[str, Any]]] = None
) -> GraduationProjectSubmission:
    """Create a new graduation project submission."""
    submission = GraduationProjectSubmission(
        session_id=session_id,
        question_id=question_id,
        answer_text=answer_text,
        citations=citations or []
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission


def get_submissions_by_session(
    db: Session,
    session_id: int
) -> List[GraduationProjectSubmission]:
    """Get all submissions for a session."""
    return db.query(GraduationProjectSubmission).filter(
        GraduationProjectSubmission.session_id == session_id
    ).all()


def update_submission_evaluation(
    db: Session,
    submission_id: int,
    evaluation_score: float,
    evaluation_feedback: str,
    rubric_scores: Optional[Dict[str, float]] = None
) -> Optional[GraduationProjectSubmission]:
    """Update a submission with evaluation results."""
    submission = db.query(GraduationProjectSubmission).filter(
        GraduationProjectSubmission.id == submission_id
    ).first()
    
    if not submission:
        return None
    
    submission.evaluation_score = evaluation_score
    submission.evaluation_feedback = evaluation_feedback
    submission.rubric_scores = rubric_scores
    submission.evaluated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(submission)
    return submission


def delete_graduation_project_questions_by_session(
    db: Session,
    session_id: int
) -> int:
    """Delete all graduation project questions for a session."""
    count = db.query(GraduationProjectQuestion).filter(
        GraduationProjectQuestion.session_id == session_id
    ).delete()
    db.commit()
    return count


def get_quiz_question(db: Session, question_id: int) -> Optional[QuizQuestion]:
    """Get a quiz question by ID."""
    return db.query(QuizQuestion).filter(QuizQuestion.id == question_id).first()


def get_questions_by_quiz(
    db: Session,
    quiz_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[QuizQuestion]:
    """Get all questions for a quiz."""
    return db.query(QuizQuestion).filter(
        QuizQuestion.quiz_id == quiz_id
    ).order_by(QuizQuestion.question_order).offset(skip).limit(limit).all()


def update_quiz_question(
    db: Session,
    question_id: int,
    **kwargs
) -> Optional[QuizQuestion]:
    """Update quiz question fields."""
    question = get_quiz_question(db, question_id)
    if not question:
        return None
    
    allowed_fields = [
        'question_text', 'question_order', 'options', 'correct_answer',
        'explanation', 'difficulty_level', 'points'
    ]
    
    for field, value in kwargs.items():
        if field in allowed_fields and value is not None:
            setattr(question, field, value)
    
    db.commit()
    db.refresh(question)
    return question


def delete_quiz_question(db: Session, question_id: int) -> bool:
    """Delete a quiz question (cascades to answers)."""
    question = get_quiz_question(db, question_id)
    if not question:
        return False
    
    db.delete(question)
    db.commit()
    return True


def count_questions_by_quiz(db: Session, quiz_id: int) -> int:
    """Count questions in a quiz."""
    return db.query(QuizQuestion).filter(QuizQuestion.quiz_id == quiz_id).count()


# ============================================================================
# QUIZ ATTEMPT OPERATIONS
# ============================================================================

def create_quiz_attempt(
    db: Session,
    quiz_id: int,
    user_id: str
) -> QuizAttempt:
    """Start a new quiz attempt."""
    # Get the next attempt number for this user and quiz
    last_attempt = db.query(QuizAttempt).filter(
        and_(
            QuizAttempt.quiz_id == quiz_id,
            QuizAttempt.user_id == user_id
        )
    ).order_by(desc(QuizAttempt.attempt_number)).first()
    
    attempt_number = (last_attempt.attempt_number + 1) if last_attempt else 1
    
    # Get quiz details
    quiz = get_quiz(db, quiz_id)
    if not quiz:
        raise ValueError(f"Quiz {quiz_id} not found")
    
    # Check if user has exceeded max attempts
    if last_attempt and last_attempt.attempt_number >= quiz.max_attempts:
        raise ValueError(f"Maximum attempts ({quiz.max_attempts}) exceeded for this quiz")
    
    attempt = QuizAttempt(
        quiz_id=quiz_id,
        user_id=user_id,
        attempt_number=attempt_number,
        total_questions=quiz.total_questions
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt


def get_quiz_attempt(db: Session, attempt_id: int) -> Optional[QuizAttempt]:
    """Get a quiz attempt by ID."""
    return db.query(QuizAttempt).filter(QuizAttempt.id == attempt_id).first()


def get_attempts_by_quiz(
    db: Session,
    quiz_id: int,
    user_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[QuizAttempt]:
    """Get quiz attempts for a quiz."""
    query = db.query(QuizAttempt).filter(QuizAttempt.quiz_id == quiz_id)
    
    if user_id:
        query = query.filter(QuizAttempt.user_id == user_id)
    
    return query.order_by(desc(QuizAttempt.started_at)).offset(skip).limit(limit).all()


def get_attempts_by_user(
    db: Session,
    user_id: str,
    quiz_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[QuizAttempt]:
    """Get quiz attempts for a user."""
    query = db.query(QuizAttempt).filter(QuizAttempt.user_id == user_id)
    
    if quiz_id:
        query = query.filter(QuizAttempt.quiz_id == quiz_id)
    
    return query.order_by(desc(QuizAttempt.started_at)).offset(skip).limit(limit).all()


def submit_quiz_attempt(
    db: Session,
    attempt_id: int,
    answers: List[Dict[str, Any]]
) -> QuizAttempt:
    """Submit a completed quiz attempt with answers."""
    attempt = get_quiz_attempt(db, attempt_id)
    if not attempt:
        raise ValueError(f"Quiz attempt {attempt_id} not found")
    
    if attempt.status != "in_progress":
        raise ValueError("Quiz attempt is not in progress")
    
    # Get quiz questions
    questions = get_questions_by_quiz(db, attempt.quiz_id)
    question_map = {q.id: q for q in questions}
    
    correct_answers = 0
    total_points = 0
    earned_points = 0
    
    # Process each answer
    for answer_data in answers:
        question_id = answer_data['question_id']
        selected_answer = answer_data['selected_answer']
        time_spent_seconds = answer_data.get('time_spent_seconds', 0)
        
        question = question_map.get(question_id)
        if not question:
            continue
        
        is_correct = selected_answer == question.correct_answer
        points_earned = question.points if is_correct else 0
        
        # Create answer record
        answer = QuizAnswer(
            attempt_id=attempt_id,
            question_id=question_id,
            selected_answer=selected_answer,
            is_correct=is_correct,
            points_earned=points_earned,
            time_spent_seconds=time_spent_seconds
        )
        db.add(answer)
        
        if is_correct:
            correct_answers += 1
        total_points += question.points
        earned_points += points_earned
    
    # Calculate score
    score_percentage = (earned_points / total_points * 100) if total_points > 0 else 0
    
    # Get quiz passing score
    quiz = get_quiz(db, attempt.quiz_id)
    passed = score_percentage >= quiz.passing_score_percentage
    
    # Update attempt
    attempt.completed_at = datetime.utcnow()
    attempt.correct_answers = correct_answers
    attempt.score_percentage = score_percentage
    attempt.passed = passed
    attempt.status = "completed"
    
    # Calculate time spent
    if attempt.started_at:
        time_delta = attempt.completed_at - attempt.started_at
        attempt.time_spent_minutes = int(time_delta.total_seconds() / 60)
    
    db.commit()
    db.refresh(attempt)
    return attempt


def abandon_quiz_attempt(
    db: Session,
    attempt_id: int
) -> QuizAttempt:
    """Abandon a quiz attempt."""
    attempt = get_quiz_attempt(db, attempt_id)
    if not attempt:
        raise ValueError(f"Quiz attempt {attempt_id} not found")
    
    attempt.status = "abandoned"
    attempt.completed_at = datetime.utcnow()
    
    # Calculate time spent
    if attempt.started_at:
        time_delta = attempt.completed_at - attempt.started_at
        attempt.time_spent_minutes = int(time_delta.total_seconds() / 60)
    
    db.commit()
    db.refresh(attempt)
    return attempt


def delete_quiz_attempt(db: Session, attempt_id: int) -> bool:
    """Delete a quiz attempt (cascades to answers)."""
    attempt = get_quiz_attempt(db, attempt_id)
    if not attempt:
        return False
    
    db.delete(attempt)
    db.commit()
    return True


# ============================================================================
# QUIZ ANSWER OPERATIONS
# ============================================================================

def get_answers_by_attempt(
    db: Session,
    attempt_id: int
) -> List[QuizAnswer]:
    """Get all answers for a quiz attempt."""
    return db.query(QuizAnswer).filter(
        QuizAnswer.attempt_id == attempt_id
    ).order_by(QuizAnswer.question_id).all()


def get_answer_by_question_and_attempt(
    db: Session,
    question_id: int,
    attempt_id: int
) -> Optional[QuizAnswer]:
    """Get answer for a specific question in an attempt."""
    return db.query(QuizAnswer).filter(
        and_(
            QuizAnswer.question_id == question_id,
            QuizAnswer.attempt_id == attempt_id
        )
    ).first()


# ============================================================================
# QUIZ STATISTICS AND ANALYTICS
# ============================================================================

def get_quiz_stats(
    db: Session,
    quiz_id: int
) -> Dict[str, Any]:
    """Get comprehensive statistics for a quiz."""
    quiz = get_quiz(db, quiz_id)
    if not quiz:
        return {}
    
    attempts = get_attempts_by_quiz(db, quiz_id)
    
    if not attempts:
        return {
            'quiz_id': quiz_id,
            'total_attempts': 0,
            'average_score': 0.0,
            'pass_rate': 0.0,
            'best_score': 0.0,
            'total_questions': quiz.total_questions,
            'is_active': quiz.is_active
        }
    
    completed_attempts = [a for a in attempts if a.status == "completed"]
    scores = [a.score_percentage for a in completed_attempts]
    passed_attempts = [a for a in completed_attempts if a.passed]
    
    return {
        'quiz_id': quiz_id,
        'total_attempts': len(attempts),
        'completed_attempts': len(completed_attempts),
        'average_score': sum(scores) / len(scores) if scores else 0.0,
        'pass_rate': (len(passed_attempts) / len(completed_attempts) * 100) if completed_attempts else 0.0,
        'best_score': max(scores) if scores else 0.0,
        'total_questions': quiz.total_questions,
        'is_active': quiz.is_active
    }


def get_user_quiz_progress(
    db: Session,
    user_id: str,
    goal_id: Optional[int] = None
) -> Dict[str, Any]:
    """Get quiz progress statistics for a user."""
    query = db.query(QuizAttempt).filter(QuizAttempt.user_id == user_id)
    
    if goal_id:
        query = query.join(Quiz).filter(Quiz.goal_id == goal_id)
    
    attempts = query.all()
    completed_attempts = [a for a in attempts if a.status == "completed"]
    
    return {
        'total_attempts': len(attempts),
        'completed_attempts': len(completed_attempts),
        'passed_attempts': len([a for a in completed_attempts if a.passed]),
        'average_score': sum(a.score_percentage for a in completed_attempts) / len(completed_attempts) if completed_attempts else 0.0,
        'best_score': max(a.score_percentage for a in completed_attempts) if completed_attempts else 0.0
    }

