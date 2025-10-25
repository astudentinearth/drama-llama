"""
Database configuration and CRUD operations.
Exports database utilities and all CRUD functions.
"""

from .database import (
    get_db,
    get_db_context,
    init_db,
    drop_db,
    engine,
    SessionLocal
)

from .crud import (
    # Session operations
    create_session,
    get_session,
    get_sessions_by_user,
    update_session,
    delete_session,
    count_user_sessions,
    
    # Message operations
    add_message_to_session,
    get_session_messages,
    get_last_n_messages,
    clear_session_messages,
    count_session_messages,
    delete_message_from_session,
    update_message_in_session,
    
    # Roadmap operations
    create_roadmap,
    get_roadmap,
    get_roadmap_by_session,
    update_roadmap,
    delete_roadmap,
    
    # Goal operations
    create_goal,
    get_goal,
    get_goals_by_roadmap,
    update_goal,
    mark_goal_started,
    mark_goal_completed,
    update_goal_progress,
    delete_goal,
    count_goals_by_roadmap,
    
    # Learning material operations
    create_learning_material,
    get_learning_material,
    get_materials_by_goal,
    get_materials_by_roadmap,
    update_learning_material,
    mark_material_completed,
    delete_learning_material,
    count_materials_by_goal,
    
    # User skill operations
    create_user_skill,
    get_user_skill,
    get_user_skills,
    get_user_skill_by_name,
    update_user_skill,
    upsert_user_skill,
    delete_user_skill,
    bulk_create_user_skills,
    
    # Complex queries
    get_session_with_full_roadmap,
    get_user_progress_stats,
    get_next_incomplete_goal,
    search_learning_materials,
    
    # Graduation project operations
    get_graduation_project_question_by_slug,
    create_graduation_project_question,
    get_graduation_project_questions_by_session,
    create_graduation_project_submission,
    get_submissions_by_session
)

__all__ = [
    # Database utilities
    'get_db',
    'get_db_context',
    'init_db',
    'drop_db',
    'engine',
    'SessionLocal',
    
    # Session operations
    'create_session',
    'get_session',
    'get_sessions_by_user',
    'update_session',
    'delete_session',
    'count_user_sessions',
    
    # Message operations
    'add_message_to_session',
    'get_session_messages',
    'get_last_n_messages',
    'clear_session_messages',
    'count_session_messages',
    'delete_message_from_session',
    'update_message_in_session',
    
    # Roadmap operations
    'create_roadmap',
    'get_roadmap',
    'get_roadmap_by_session',
    'update_roadmap',
    'delete_roadmap',
    
    # Goal operations
    'create_goal',
    'get_goal',
    'get_goals_by_roadmap',
    'update_goal',
    'mark_goal_started',
    'mark_goal_completed',
    'update_goal_progress',
    'delete_goal',
    'count_goals_by_roadmap',
    
    # Learning material operations
    'create_learning_material',
    'get_learning_material',
    'get_materials_by_goal',
    'get_materials_by_roadmap',
    'update_learning_material',
    'mark_material_completed',
    'delete_learning_material',
    'count_materials_by_goal',
    
    # User skill operations
    'create_user_skill',
    'get_user_skill',
    'get_user_skills',
    'get_user_skill_by_name',
    'update_user_skill',
    'upsert_user_skill',
    'delete_user_skill',
    'bulk_create_user_skills',
    
    # Complex queries
    'get_session_with_full_roadmap',
    'get_user_progress_stats',
    'get_next_incomplete_goal',
    'search_learning_materials',

    # Graduation project operations
    'get_graduation_project_question_by_slug',
    'create_graduation_project_question',
    'get_graduation_project_questions_by_session',
    'create_graduation_project_submission',
    'get_submissions_by_session'
]

