from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


# ============= Router & Intent Detection =============

class IntentType(str, Enum):
    """Types of user intents."""
    CHAT = "chat"
    GENERATE_ROADMAP = "generate_roadmap"
    GENERATE_COURSE = "generate_course"
    GENERATE_PROJECT = "generate_project"
    GENERATE_QUIZ = "generate_quiz"
    EVALUATE_PROJECT = "evaluate_project"
    ANALYZE_RESUME = "analyze_resume"
    GENERATE_JOB_POSTING = "generate_job_posting"
    RANK_CANDIDATES = "rank_candidates"
    OPTIMIZE_JOB_POSTING = "optimize_job_posting"
    ENHANCE_RESUME = "enhance_resume"
    ANALYZE_CANDIDATE_POOL = "analyze_candidate_pool"


class IntentDetectionRequest(BaseModel):
    """Request for intent detection."""
    user_message: str
    conversation_history: List[Dict[str, str]] = []


class IntentDetectionResponse(BaseModel):
    """Response from intent detection."""
    intent: IntentType
    confidence: float = Field(ge=0.0, le=1.0)
    extracted_params: Dict[str, Any] = {}
    requires_clarification: bool = False
    clarification_questions: List[str] = []


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


# ============= Roadmap Generation =============

class RoadmapInputRequest(BaseModel):
    """Request for roadmap input processing."""
    resume_text: Optional[str] = None
    job_posting_text: Optional[str] = None
    user_goals: Optional[str] = None


class ExtractedProfile(BaseModel):
    """Extracted user profile from resume."""
    skills: List[Skill]
    experience_years: int
    education: List[str]
    identified_gaps: List[str]
    recommended_focus: List[str]



class RoadmapResponse(BaseModel):
    """Complete roadmap response."""
    goals: List[Goal]
    total_estimated_weeks: int
    graduation_project: str


# ============= Course Generation =============

class CourseGenerationRequest(BaseModel):
    """Request for course content generation."""
    course_title: str
    topics: List[str]
    skill_level: SkillLevel
    context: Optional[str] = None


class Exercise(BaseModel):
    """Course exercise."""
    title: str
    description: str
    hints: List[str] = []


class CourseSection(BaseModel):
    """A section in a course."""
    title: str
    content: str
    key_points: List[str]


class CourseContent(BaseModel):
    """Complete course content."""
    title: str
    objectives: List[str]
    sections: List[CourseSection]
    exercises: List[Exercise]
    estimated_hours: int


class GraduationProjectRequest(BaseModel):
    """Request for graduation project generation."""
    course_title: str
    topics_covered: List[str]
    skill_level: SkillLevel

class GraduationProject(BaseModel):
    """Graduation project specification."""
    title: str
    overview: str
    requirements: List[str]
    steps: List[str]
    evaluation_criteria: List[str]
    estimated_hours: int


# ============= Assessment & Testing =============

class QuizGenerationRequest(BaseModel):
    """Request for quiz generation."""
    course_title: str
    course_content: str
    num_questions: int = Field(ge=5, le=50, default=5)
    skill_level: SkillLevel
    question_types: List[str] = ["multiple_choice", "scenario", "code"]


class QuizOption(BaseModel):
    """Multiple choice option."""
    option: str
    is_correct: bool
    explanation: Optional[str] = None


class QuizQuestion(BaseModel):
    """A quiz question."""
    question_type: str
    question: str
    options: Optional[List[QuizOption]]  # For multiple choice
    correct_answer: str
    explanation: str


class Quiz(BaseModel):
    """Complete quiz."""
    course_title: str
    questions: List[QuizQuestion]
    total_points: int
    passing_score: int


class EvaluationCriterion(BaseModel):
    """Evaluation criterion for projects."""
    criterion: str
    description: str
    weight: float = Field(ge=0.0, le=1.0)


class ProjectEvaluationRequest(BaseModel):
    """Request for project evaluation."""
    project_requirements: str
    submitted_work: str
    evaluation_rubric: List[EvaluationCriterion]


class Feedback(BaseModel):
    """Evaluation feedback."""
    criterion: str
    score: float = Field(ge=0.0, le=100.0)
    comments: str
    strengths: List[str]


class ProjectEvaluation(BaseModel):
    """Project evaluation result."""
    overall_score: float = Field(ge=0.0, le=100.0)
    feedback: List[Feedback]
    summary: str
    passed: bool


# ============= Resume Analysis =============

class ResumeAnalysisRequest(BaseModel):
    """Resume analysis request."""
    resume_text: str
    target_job: Optional[str] = None


class ResumeAnalysisResponse(BaseModel):
    """Resume analysis response."""
    skills: List[Skill]
    experience_years: int
    strengths: List[str]
    gaps: List[str]
    suggestions: List[str]
    ats_score: float = Field(ge=0.0, le=100.0)


# ============= Job Posting Generation =============

class JobPostingRequest(BaseModel):
    """Request for job posting generation."""
    company_name: str
    role_title: str
    department: Optional[str] = None
    experience_level: str
    key_requirements: List[str]
    responsibilities: List[str]
    company_culture: Optional[str] = None
    benefits: List[str] = []


class JobPosting(BaseModel):
    """Generated job posting."""
    title: str
    description: str
    requirements: List[str]
    responsibilities: List[str]
    benefits: List[str]
    company_culture: str
    application_instructions: str


class JobPostingOptimizationRequest(BaseModel):
    """Request for job posting optimization."""
    current_posting: str
    target_audience: Optional[str] = None


class OptimizationSuggestion(BaseModel):
    """Optimization suggestion."""
    current_text: str
    suggested_text: str
    reason: str


class JobPostingOptimization(BaseModel):
    """Job posting optimization result."""
    suggestions: List[OptimizationSuggestion]
    optimized_posting: str


class CandidateAnalysisRequest(BaseModel):
    """Request for candidate pool analysis."""
    job_posting: str
    market_data: Optional[Dict[str, Any]] = None
    company_profile: Optional[str] = None


class CandidatePoolAnalysis(BaseModel):
    """Candidate pool analysis result."""
    estimated_reach: str
    target_demographics: List[str]
    skill_availability: Dict[str, str]
    competition_level: str
    optimization_suggestions: List[str]
    estimated_applications: str


class ApplicationRankingRequest(BaseModel):
    """Request for application ranking."""
    job_requirements: str
    candidate_profiles: List[Dict[str, Any]]
    company_mission: Optional[str] = None
    company_vision: Optional[str] = None


class CandidateScore(BaseModel):
    """Candidate scoring."""
    candidate_id: str
    candidate_name: str
    technical_skills_score: float = Field(ge=0.0, le=100.0)
    experience_score: float = Field(ge=0.0, le=100.0)
    culture_fit_score: float = Field(ge=0.0, le=100.0)
    overall_score: float = Field(ge=0.0, le=100.0)
    strengths: List[str]


class ApplicationRanking(BaseModel):
    """Application ranking result."""
    ranked_candidates: List[CandidateScore]
    summary: str


class ResumeEnhancementRequest(BaseModel):
    """Request for resume enhancement."""
    current_resume: str
    completed_courses: List[str] = []
    completed_projects: List[str] = []
    target_jobs: List[str] = []

class ChatRequest(BaseModel):
    """Chat request."""
    message: str
    conversation_history: List[Dict[str, str]] = []

class ChatResponse(BaseModel):
    """Chat response."""
    message: str
    suggestions: List[str] = []

class ResumeSuggestion(BaseModel):
    """Resume enhancement suggestion."""
    section: str
    current_content: Optional[str] = None
    suggested_content: str
    priority: str


class ResumeEnhancement(BaseModel):
    """Resume enhancement result."""
    suggestions: List[ResumeSuggestion]
    enhanced_resume: str
    ats_score: float = Field(ge=0.0, le=100.0)
    key_improvements: List[str]


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
