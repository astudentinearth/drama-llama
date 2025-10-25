# Database Configuration and CRUD Operations

This module provides comprehensive database operations for the Drama Llama AI learning platform.

## Overview

The database layer is organized into:
- **`database.py`**: Database connection, session management, and initialization
- **`crud.py`**: CRUD operations for all models
- **`__init__.py`**: Exports all functions for easy importing
- **`usage_examples.py`**: Practical examples demonstrating usage

## Database Models

The system manages five main entities:

1. **Session**: Container for user learning journeys
2. **Roadmap**: Learning roadmap skeleton with goals and graduation project
3. **RoadmapGoal**: Individual learning objectives within a roadmap
4. **LearningMaterial**: Educational resources for each goal
5. **UserSkill**: User's skills and proficiency levels

## Quick Start

### Database Initialization

```python
from db_config import init_db, drop_db

# Initialize database (create all tables)
init_db()

# Drop all tables (use carefully!)
drop_db()
```

### Using Database Context

```python
from db_config import get_db_context, create_session

# For standalone scripts
with get_db_context() as db:
    session = create_session(
        db,
        user_id=123,
        session_name="My Learning Journey"
    )
    # Changes are automatically committed

# For FastAPI endpoints
from db_config import get_db

@app.get("/sessions/{session_id}")
def get_session_endpoint(session_id: int, db: Session = Depends(get_db)):
    return get_session(db, session_id)
```

## API Reference

### Session Operations

#### `create_session(db, user_id, session_name=None, description=None, status=SessionStatusEnum.ACTIVE)`
Create a new learning session for a user.

**Parameters:**
- `user_id` (int): User ID from main backend
- `session_name` (str, optional): User-defined session name
- `description` (str, optional): Session description
- `status` (SessionStatusEnum, optional): Initial status

**Returns:** `SessionModel`

#### `get_session(db, session_id)`
Retrieve a session by ID.

#### `get_sessions_by_user(db, user_id, status=None, skip=0, limit=100)`
Get all sessions for a user with optional filtering.

**Parameters:**
- `status` (SessionStatusEnum, optional): Filter by status (ACTIVE, COMPLETED, ARCHIVED)
- `skip` (int): Pagination offset
- `limit` (int): Maximum results

#### `update_session(db, session_id, **kwargs)`
Update session fields.

#### `delete_session(db, session_id)`
Delete a session (cascades to roadmap, goals, and materials).

#### `count_user_sessions(db, user_id, status=None)`
Count sessions for a user.

---

### Roadmap Operations

#### `create_roadmap(db, session_id, user_request, **kwargs)`
Create a roadmap for a session.

**Key Parameters:**
- `user_request` (str, required): User's learning request
- `user_summarized_cv` (str): CV summary
- `user_expertise_domains` (List[str]): Existing expertise areas
- `total_estimated_weeks` (int): Total duration estimate
- `graduation_project` (str): Final project description
- `graduation_project_requirements` (List[str]): Project requirements

#### `get_roadmap(db, roadmap_id)`
Retrieve a roadmap by ID.

#### `get_roadmap_by_session(db, session_id)`
Get the roadmap for a specific session.

#### `update_roadmap(db, roadmap_id, **kwargs)`
Update roadmap fields.

#### `delete_roadmap(db, roadmap_id)`
Delete a roadmap.

---

### Goal Operations

#### `create_goal(db, roadmap_id, goal_number, title, description, **kwargs)`
Create a learning goal.

**Key Parameters:**
- `goal_number` (int): Order in roadmap
- `title` (str): Goal title
- `description` (str): Detailed description
- `priority` (int): 1-5 scale (default: 3)
- `skill_level` (SkillLevelEnum): Target skill level
- `estimated_hours` (int): Time estimate
- `prerequisites` (List[str]): Required prerequisites

#### `get_goal(db, goal_id)`
Retrieve a goal by ID.

#### `get_goals_by_roadmap(db, roadmap_id, completed_only=False, skip=0, limit=100)`
Get all goals for a roadmap.

#### `update_goal(db, goal_id, **kwargs)`
Update goal fields.

#### `mark_goal_started(db, goal_id)`
Mark a goal as started (sets `started_at` timestamp).

#### `mark_goal_completed(db, goal_id)`
Mark a goal as completed (sets `is_completed` and `completed_at`).

#### `update_goal_progress(db, goal_id, completion_percentage, actual_hours_spent=None)`
Update goal completion percentage and time spent.

#### `delete_goal(db, goal_id)`
Delete a goal.

#### `count_goals_by_roadmap(db, roadmap_id, completed_only=False)`
Count goals in a roadmap.

---

### Learning Material Operations

#### `create_learning_material(db, goal_id, title, material_type, **kwargs)`
Create a learning material.

**Key Parameters:**
- `title` (str): Material title
- `material_type` (str): Type (article, video, tutorial, course, documentation)
- `content` (str): Material content
- `source_url` (str): Original URL
- `estimated_time_minutes` (int): Time to complete
- `difficulty_level` (SkillLevelEnum): Difficulty level
- `end_of_material_project` (str): Practice project
- `project_requirements` (List[str]): Project requirements
- `relevance_score` (float): Relevance (0-1)
- `quality_score` (float): Quality (0-1)

#### `get_learning_material(db, material_id)`
Retrieve a material by ID.

#### `get_materials_by_goal(db, goal_id, material_type=None, completed_only=False, skip=0, limit=100)`
Get all materials for a goal with optional filtering.

#### `get_materials_by_roadmap(db, roadmap_id, material_type=None, skip=0, limit=100)`
Get all materials across all goals in a roadmap.

#### `update_learning_material(db, material_id, **kwargs)`
Update material fields.

#### `mark_material_completed(db, material_id, user_rating=None, user_notes=None)`
Mark a material as completed with optional feedback.

#### `delete_learning_material(db, material_id)`
Delete a learning material.

#### `count_materials_by_goal(db, goal_id, completed_only=False)`
Count materials for a goal.

---

### User Skill Operations

#### `create_user_skill(db, user_id, skill_name, skill_level=SkillLevelEnum.BEGINNER, **kwargs)`
Create a user skill.

**Key Parameters:**
- `skill_name` (str): Skill name
- `skill_level` (SkillLevelEnum): Proficiency level
- `confidence_score` (float): Confidence (0-1)
- `source` (str): Origin (cv, course_completion, self_reported, assessment)
- `verified` (bool): Verification status

#### `get_user_skill(db, skill_id)`
Retrieve a skill by ID.

#### `get_user_skills(db, user_id, skill_level=None, verified_only=False, skip=0, limit=100)`
Get all skills for a user with optional filtering.

#### `get_user_skill_by_name(db, user_id, skill_name)`
Get a specific skill by name.

#### `update_user_skill(db, skill_id, **kwargs)`
Update skill fields.

#### `upsert_user_skill(db, user_id, skill_name, skill_level, **kwargs)`
Create or update a skill (idempotent operation).

#### `delete_user_skill(db, skill_id)`
Delete a skill.

#### `bulk_create_user_skills(db, user_id, skills)`
Bulk create skills from a list of dictionaries.

**Example:**
```python
skills = [
    {
        "skill_name": "Python",
        "skill_level": SkillLevelEnum.EXPERT,
        "confidence_score": 0.95,
        "source": "cv"
    },
    # ... more skills
]
bulk_create_user_skills(db, user_id=123, skills=skills)
```

---

### Complex/Aggregate Queries

#### `get_session_with_full_roadmap(db, session_id)`
Get a session with all related data (roadmap, goals, materials) in a single query using eager loading.

#### `get_user_progress_stats(db, user_id)`
Get comprehensive progress statistics for a user.

**Returns:**
```python
{
    'total_sessions': int,
    'active_sessions': int,
    'completed_sessions': int,
    'total_goals': int,
    'completed_goals': int,
    'total_materials': int,
    'completed_materials': int,
    'total_hours_estimated': int,
    'total_hours_spent': int
}
```

#### `get_next_incomplete_goal(db, roadmap_id)`
Get the next incomplete goal in a roadmap (ordered by goal_number).

#### `search_learning_materials(db, roadmap_id, search_term, skip=0, limit=50)`
Search materials by title or description within a roadmap.

---

## Enums

### SessionStatusEnum
- `ACTIVE`: Session is currently active
- `COMPLETED`: Session has been completed
- `ARCHIVED`: Session has been archived

### RoadmapStatusEnum
- `DRAFT`: Roadmap is being created
- `IN_PROGRESS`: Roadmap is active
- `COMPLETED`: All goals completed
- `ARCHIVED`: Roadmap archived

### SkillLevelEnum
- `BEGINNER`: Beginner level
- `INTERMEDIATE`: Intermediate level
- `ADVANCED`: Advanced level
- `EXPERT`: Expert level

---

## Common Patterns

### Creating a Complete Learning Path

```python
from db_config import (
    get_db_context,
    create_session,
    create_roadmap,
    create_goal,
    create_learning_material
)

with get_db_context() as db:
    # 1. Create session
    session = create_session(db, user_id=123, session_name="My Journey")
    
    # 2. Create roadmap
    roadmap = create_roadmap(
        db,
        session_id=session.id,
        user_request="Learn web development"
    )
    
    # 3. Create goals
    goal = create_goal(
        db,
        roadmap_id=roadmap.id,
        goal_number=1,
        title="Learn JavaScript",
        description="Master modern JavaScript"
    )
    
    # 4. Add materials
    material = create_learning_material(
        db,
        goal_id=goal.id,
        title="JavaScript Course",
        material_type="course"
    )
```

### Tracking Progress

```python
from db_config import (
    get_db_context,
    mark_goal_started,
    update_goal_progress,
    mark_material_completed,
    mark_goal_completed
)

with get_db_context() as db:
    # Start a goal
    mark_goal_started(db, goal_id=1)
    
    # Update progress
    update_goal_progress(db, goal_id=1, completion_percentage=50.0)
    
    # Complete a material
    mark_material_completed(db, material_id=1, user_rating=5)
    
    # Complete the goal
    mark_goal_completed(db, goal_id=1)
```

### Querying User Data

```python
from db_config import (
    get_db_context,
    get_sessions_by_user,
    get_user_progress_stats,
    get_next_incomplete_goal
)

with get_db_context() as db:
    # Get active sessions
    sessions = get_sessions_by_user(db, user_id=123, status=SessionStatusEnum.ACTIVE)
    
    # Get progress stats
    stats = get_user_progress_stats(db, user_id=123)
    print(f"Completed {stats['completed_goals']}/{stats['total_goals']} goals")
    
    # Get next goal to work on
    next_goal = get_next_incomplete_goal(db, roadmap_id=1)
```

---

## Best Practices

1. **Always use context managers** (`get_db_context()`) for standalone scripts
2. **Use dependency injection** (`Depends(get_db)`) in FastAPI endpoints
3. **Check for None** when retrieving entities (they might not exist)
4. **Use transactions** for operations that modify multiple entities
5. **Leverage eager loading** (`get_session_with_full_roadmap`) for complex queries
6. **Use enums** for status and level fields to ensure data consistency
7. **Validate data** before passing to CRUD functions
8. **Handle exceptions** appropriately in your application logic

---

## Error Handling

```python
from sqlalchemy.exc import IntegrityError
from db_config import get_db_context, create_session

with get_db_context() as db:
    try:
        session = create_session(db, user_id=123)
    except IntegrityError:
        # Handle constraint violations
        print("Failed to create session")
    except Exception as e:
        # Handle other errors
        print(f"Error: {e}")
```

---

## Testing

See `usage_examples.py` for comprehensive examples of all operations.

To run examples:
```bash
python db_config/usage_examples.py
```

---

## Migration Notes

When adding new fields or tables:
1. Update models in `models/db_models.py`
2. Add corresponding CRUD operations in `crud.py`
3. Export new functions in `__init__.py`
4. Update this README
5. Run `init_db()` to create new tables (or use Alembic for migrations)

