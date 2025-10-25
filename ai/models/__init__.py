"""AI Models package - contains Prompt class and Pydantic schemas."""

from .Prompt import Prompt
from .db_models import (
    Base,
    SkillLevelEnum,
    RoadmapStatusEnum,
    Roadmap,
    RoadmapGoal,
    LearningMaterial,
    UserSkill,
)
from .schemas import (
    # Enums
    SkillLevel,
    SessionStatus,
    MessageRole,
    
    # Common Models
    Skill,
    Goal,
    
    # Chat Models
    ChatRequest,
    ChatResponse,
    
    # API Response Wrapper
    APIResponse,
    HealthCheckResponse,
    
    # Session Management
    SessionCreate,
    SessionUpdate,
    SessionResponse,
    SessionListResponse,
    SessionProgressStats,
    MessageCreate,
    MessageResponse,
    MessagesListResponse,
    
    # AI Tool Response Models
    ToolCallInstruction,
    AIToolResponse,
    RoadmapGoalSchema,
    RoadmapSkeletonResponse,
    LearningExample,
    LearningMaterialResponse,
)

__all__ = [
    # Prompt class
    "Prompt",
    
    # Database Models
    "Base",
    "SkillLevelEnum",
    "RoadmapStatusEnum",
    "Roadmap",
    "RoadmapGoal",
    "LearningMaterial",
    "UserSkill",
    
    # Enums
    "SkillLevel",
    "SessionStatus",
    "MessageRole",
    
    # Common Models
    "Skill",
    "Goal",
    
    # Chat Models
    "ChatRequest",
    "ChatResponse",
    
    # API Response Wrapper
    "APIResponse",
    "HealthCheckResponse",
    
    # Session Management
    "SessionCreate",
    "SessionUpdate",
    "SessionResponse",
    "SessionListResponse",
    "SessionProgressStats",
    "MessageCreate",
    "MessageResponse",
    "MessagesListResponse",
    
    # AI Tool Response Models
    "ToolCallInstruction",
    "AIToolResponse",
    "RoadmapGoalSchema",
    "RoadmapSkeletonResponse",
    "LearningExample",
    "LearningMaterialResponse",
]
