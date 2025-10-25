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
    """Response from createRoadmapSkeleton or editRoadmapSkeleton tool."""
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


# ============= Graduation Project Questions =============

class QuestionDifficulty(str, Enum):
    """Question difficulty levels."""
    INTRODUCTORY = "introductory"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class GraduationProjectQuestionSchema(BaseModel):
    """Schema for a single graduation project question."""
    question_id: str = Field(..., description="Stable slug (kebab-case)")
    prompt: str = Field(..., description="The open-ended question text")
    rationale: str = Field(..., description="Why this question assesses the intended competency")
    goals_covered: List[int] = Field(..., description="Array of goal IDs")
    materials_covered: List[int] = Field(..., description="Array of material IDs")
    expected_competencies: List[str] = Field(..., description="Array of competency strings")
    difficulty: QuestionDifficulty = Field(..., description="Question difficulty level")
    estimated_time_minutes: int = Field(..., ge=10, le=45, description="Estimated time to answer")
    evaluation_rubric: List[str] = Field(..., description="3-5 evaluation criteria")
    answer_min_chars: int = Field(default=500, description="Minimum answer length")
    answer_max_chars: int = Field(default=2500, description="Maximum answer length")
    requires_material_citations: bool = Field(default=False, description="Whether citations are required")


class GraduationProjectContext(BaseModel):
    """Graduation project context for question generation."""
    title: str = Field(..., description="Graduation project title")
    description: str = Field(..., description="Graduation project full description")


class GenerateQuestionsResponse(BaseModel):
    """Response from graduation project question generation."""
    graduation_project: GraduationProjectContext
    questions: List[GraduationProjectQuestionSchema] = Field(..., description="Exactly 5 questions")
    graduation_project_db_id: Optional[int] = None
    question_db_ids: List[Optional[int]] = Field(default_factory=list)


class MaterialCitation(BaseModel):
    """Citation from a learning material."""
    material_id: int = Field(..., description="Referenced material ID")
    excerpt: Optional[str] = Field(None, description="Quoted fragment from material description")


class QuestionAnswer(BaseModel):
    """User's answer to a graduation project question."""
    question_id: str = Field(..., description="Question slug (kebab-case)")
    text: str = Field(..., description="User's free-form answer")
    citations: Optional[List[MaterialCitation]] = Field(default=None, description="Material citations (optional)")


class SubmitAnswersRequest(BaseModel):
    """Request to submit graduation project question answers."""
    session_id: int
    answers: List[QuestionAnswer] = Field(..., min_items=5, max_items=5, description="Exactly 5 answers")


class SubmissionEvaluation(BaseModel):
    """Evaluation result for a submission."""
    submission_id: int = Field(..., description="Submission database ID")
    question_id: str = Field(..., description="Question slug")
    score: float = Field(..., ge=0.0, le=1.0, description="Evaluation score (0-1)")
    feedback: str = Field(..., description="AI-generated feedback")
    rubric_scores: Optional[Dict[str, float]] = Field(None, description="Per-criterion scores")
    error: Optional[str] = Field(None, description="Error message if evaluation failed")


class SubmitAnswersResponse(BaseModel):
    """Response after submitting answers."""
    session_id: int
    submission_ids: List[int] = Field(..., description="Database IDs of created submissions")
    message: str = Field(default="Answers submitted successfully")
    evaluations: Optional[List[SubmissionEvaluation]] = None
class QuizQuestion(BaseModel):
    """Quiz question representation."""
    question: str = Field(..., description="The quiz question text")
    options: List[str] = Field(..., description="Array of multiple choice options (A, B, C, D)")
    correctAnswer: str = Field(..., description="The correct answer option (A, B, C, or D)")

class QuizForGoalResponse(BaseModel):
    """Response from createQuizForGoal tool."""
    quiz: List[QuizQuestion] = Field(..., description="List of quiz questions")


# ============= Quiz Database Models =============

class QuizQuestionCreate(BaseModel):
    """Request to create a quiz question."""
    question_text: str = Field(..., description="The quiz question text")
    question_order: int = Field(..., description="Order within the quiz")
    options: List[str] = Field(..., min_items=4, max_items=4, description="Exactly 4 multiple choice options")
    correct_answer: str = Field(..., pattern="^[ABCD]$", description="Correct answer (A, B, C, or D)")
    explanation: Optional[str] = Field(None, description="Explanation of the correct answer")
    points: int = Field(1, ge=1, description="Points for correct answer")


class QuizQuestionResponse(BaseModel):
    """Quiz question response."""
    id: int
    quiz_id: int
    question_text: str
    question_order: int
    options: List[str]
    correct_answer: str
    explanation: Optional[str]
    points: int
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True


class QuizCreate(BaseModel):
    """Request to create a quiz."""
    goal_id: int = Field(..., description="Associated roadmap goal ID")
    title: str = Field(..., description="Quiz title")
    description: Optional[str] = Field(None, description="Quiz description")
    difficulty_level: Optional[SkillLevel] = Field(SkillLevel.BEGINNER, description="Quiz difficulty level")
    time_limit_minutes: Optional[int] = Field(None, ge=1, description="Time limit in minutes")
    passing_score_percentage: float = Field(70.0, ge=0.0, le=100.0, description="Passing score percentage")
    max_attempts: int = Field(3, ge=1, description="Maximum attempts allowed")
    questions: List[QuizQuestionCreate] = Field(..., min_items=1, description="Quiz questions")


class QuizUpdate(BaseModel):
    """Request to update a quiz."""
    title: Optional[str] = None
    description: Optional[str] = None
    difficulty_level: Optional[SkillLevel] = None
    time_limit_minutes: Optional[int] = Field(None, ge=1)
    passing_score_percentage: Optional[float] = Field(None, ge=0.0, le=100.0)
    max_attempts: Optional[int] = Field(None, ge=1)
    is_active: Optional[bool] = None


class QuizResponse(BaseModel):
    """Quiz response."""
    id: int
    goal_id: int
    title: str
    description: Optional[str]
    difficulty_level: str
    time_limit_minutes: Optional[int]
    passing_score_percentage: float
    max_attempts: int
    is_active: bool
    total_questions: int
    created_at: str
    updated_at: str
    questions: List[QuizQuestionResponse] = []
    
    class Config:
        from_attributes = True


class QuizListResponse(BaseModel):
    """List of quizzes response."""
    quizzes: List[QuizResponse]
    total: int
    skip: int
    limit: int


class QuizAttemptCreate(BaseModel):
    """Request to start a quiz attempt."""
    quiz_id: int = Field(..., description="Quiz ID to attempt")
    user_id: str = Field(..., description="User ID attempting the quiz")


class QuizAnswerSubmit(BaseModel):
    """Request to submit an answer to a quiz question."""
    question_id: int = Field(..., description="Question ID")
    selected_answer: str = Field(..., pattern="^[ABCD]$", description="Selected answer (A, B, C, or D)")
    time_spent_seconds: Optional[int] = Field(0, ge=0, description="Time spent on this question")


class QuizAttemptSubmit(BaseModel):
    """Request to submit a completed quiz attempt."""
    attempt_id: int = Field(..., description="Attempt ID")
    answers: List[QuizAnswerSubmit] = Field(..., description="All answers for the quiz")


class QuizAnswerResponse(BaseModel):
    """Quiz answer response."""
    id: int
    attempt_id: int
    question_id: int
    selected_answer: Optional[str]
    is_correct: bool
    points_earned: int
    time_spent_seconds: int
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True


class QuizAttemptResponse(BaseModel):
    """Quiz attempt response."""
    id: int
    quiz_id: int
    user_id: str
    attempt_number: int
    started_at: str
    completed_at: Optional[str]
    total_questions: int
    correct_answers: int
    score_percentage: float
    passed: bool
    time_spent_minutes: int
    status: str
    created_at: str
    updated_at: str
    answers: List[QuizAnswerResponse] = []
    
    class Config:
        from_attributes = True


class QuizAttemptListResponse(BaseModel):
    """List of quiz attempts response."""
    attempts: List[QuizAttemptResponse]
    total: int
    skip: int
    limit: int


class QuizStatsResponse(BaseModel):
    """Quiz statistics response."""
    quiz_id: int
    total_attempts: int
    average_score: float
    pass_rate: float
    best_score: float
    total_questions: int
    is_active: bool
