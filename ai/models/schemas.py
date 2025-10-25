from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


# ============= Common Models =============

class SkillLevel(str, Enum):
    """Skill proficiency levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class Skill(BaseModel):
    """Skill representation."""
    name: str
    level: SkillLevel
    confidence: float = Field(ge=0.0, le=1.0, default=0.8)


class Goal(BaseModel):
    """Learning goal representation."""
    goal_number: int
    title: str
    description: str
    priority: int = Field(ge=1, le=5)
    estimated_hours: int
    prerequisites: List[str] = []


# ============= Chat Models =============

class ChatRequest(BaseModel):
    """Chat request."""
    session_id: int
    userPrompt: str


class ChatResponse(BaseModel):
    """Chat response."""
    message: str
    suggestions: List[str] = []


# ============= API Response Wrapper =============

class APIResponse(BaseModel):
    """Standard API response wrapper."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None


class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str
    ollama_connected: bool
    model: str


# ============= Session Management =============

class SessionStatus(str, Enum):
    """Session status types."""
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class SessionCreate(BaseModel):
    """Request from main backend to create a new session."""
    user_id: str
    session_name: Optional[str] = None
    description: Optional[str] = None
    status: SessionStatus = SessionStatus.ACTIVE


class SessionUpdate(BaseModel):
    """Request to update a session."""
    session_name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[SessionStatus] = None


class SessionResponse(BaseModel):
    """Session response."""
    id: int
    user_id: str
    session_name: Optional[str]
    description: Optional[str]
    status: str
    created_at: str
    updated_at: str
    completed_at: Optional[str]
    
    class Config:
        from_attributes = True


class SessionListResponse(BaseModel):
    """List of sessions with metadata."""
    sessions: List[SessionResponse]
    total: int
    skip: int
    limit: int


class SessionProgressStats(BaseModel):
    """Session progress statistics."""
    total_goals: int
    completed_goals: int
    total_materials: int
    completed_materials: int
    total_hours_estimated: int
    total_hours_spent: int
    completion_percentage: float


class MessageRole(str, Enum):
    """Message role types."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class MessageCreate(BaseModel):
    """Request to add a message to a session."""
    role: MessageRole
    content: str
    metadata: Optional[Dict[str, Any]] = None


class MessageResponse(BaseModel):
    """Message response."""
    role: str
    content: str
    timestamp: str
    metadata: Dict[str, Any] = {}


class MessagesListResponse(BaseModel):
    """List of messages response."""
    session_id: int
    messages: List[MessageResponse]
    total: int


# ============= AI Tool Response Models =============

class ToolCallInstruction(BaseModel):
    """Tool call instruction from AI."""
    tool_name: str = Field(..., description="Name of the tool to call")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Arguments for the tool")
    call_id: str = Field(..., description="Unique identifier for this tool call")


class AIToolResponse(BaseModel):
    """Response from AI with optional tool calls."""
    content: str = Field(..., description="AI response content")
    has_tool_calls: bool = Field(default=False, description="Whether response contains tool calls")
    tool_calls: List[ToolCallInstruction] = Field(default_factory=list, description="List of tool calls")
    finish_reason: str = Field(default="", description="Reason for completion finish")
    usage: Dict[str, int] = Field(default_factory=dict, description="Token usage statistics")


class RoadmapGoalSchema(BaseModel):
    """Schema for a single roadmap goal."""
    goal_number: int = Field(..., description="Sequential goal number")
    title: str = Field(..., description="Goal title")
    description: str = Field(..., description="Detailed goal description")
    priority: int = Field(..., ge=1, le=5, description="Priority level (1=highest)")
    estimated_hours: int = Field(..., description="Estimated hours to complete")
    prerequisites: List[str] = Field(default_factory=list, description="Prerequisites")


class RoadmapSkeletonResponse(BaseModel):
    """Response from createRoadmapSkeleton tool."""
    goals: List[RoadmapGoalSchema] = Field(..., description="List of learning goals")
    graduation_project: str = Field(..., description="Capstone project description")
    graduation_project_title: str = Field(..., description="Capstone project title")


class LearningExample(BaseModel):
    """Example for learning material."""
    title: str = Field(..., description="Example title")
    code: str = Field(default="", description="Code snippet")
    explanation: str = Field(..., description="Explanation of the example")


class LearningMaterialResponse(BaseModel):
    """Response from createLearningMaterials tool."""
    title: str = Field(..., description="Material title")
    description: str = Field(..., description="Material description")
    content: str = Field(..., description="Main content in Markdown")
    estimated_time_minutes: int = Field(..., description="Estimated completion time")
