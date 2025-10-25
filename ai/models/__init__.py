"""AI Models package - contains Prompt class and Pydantic schemas."""

from .Prompt import Prompt
from .schemas import (
    # Enums
    IntentType,
    SkillLevel,
    
    # Router & Intent Detection
    IntentDetectionRequest,
    IntentDetectionResponse,
    
    # Common Models
    Skill,
    Goal,
    
    # Roadmap Generation
    RoadmapInputRequest,
    ExtractedProfile,
    RoadmapResponse,
    
    # Course Generation
    CourseGenerationRequest,
    Exercise,
    CourseSection,
    CourseContent,
    GraduationProjectRequest,
    GraduationProject,
    
    # Assessment & Testing
    QuizGenerationRequest,
    QuizOption,
    QuizQuestion,
    Quiz,
    EvaluationCriterion,
    ProjectEvaluationRequest,
    Feedback,
    ProjectEvaluation,
    
    # Resume Analysis
    ResumeAnalysisRequest,
    ResumeAnalysisResponse,
    
    # Job Posting Generation
    JobPostingRequest,
    JobPosting,
    JobPostingOptimizationRequest,
    OptimizationSuggestion,
    JobPostingOptimization,
    CandidateAnalysisRequest,
    CandidatePoolAnalysis,
    ApplicationRankingRequest,
    CandidateScore,
    ApplicationRanking,
    ResumeEnhancementRequest,
    ChatRequest,
    ChatResponse,
    ResumeSuggestion,
    ResumeEnhancement,
    
    # API Response Wrapper
    APIResponse,
    HealthCheckResponse,
)

__all__ = [
    # Prompt class
    "Prompt",
    
    # Enums
    "IntentType",
    "SkillLevel",
    
    # Router & Intent Detection
    "IntentDetectionRequest",
    "IntentDetectionResponse",
    
    # Common Models
    "Skill",
    "Goal",
    
    # Roadmap Generation
    "RoadmapInputRequest",
    "ExtractedProfile",
    "RoadmapResponse",
    
    # Course Generation
    "CourseGenerationRequest",
    "Exercise",
    "CourseSection",
    "CourseContent",
    "GraduationProjectRequest",
    "GraduationProject",
    
    # Assessment & Testing
    "QuizGenerationRequest",
    "QuizOption",
    "QuizQuestion",
    "Quiz",
    "EvaluationCriterion",
    "ProjectEvaluationRequest",
    "Feedback",
    "ProjectEvaluation",
    
    # Resume Analysis
    "ResumeAnalysisRequest",
    "ResumeAnalysisResponse",
    
    # Job Posting Generation
    "JobPostingRequest",
    "JobPosting",
    "JobPostingOptimizationRequest",
    "OptimizationSuggestion",
    "JobPostingOptimization",
    "CandidateAnalysisRequest",
    "CandidatePoolAnalysis",
    "ApplicationRankingRequest",
    "CandidateScore",
    "ApplicationRanking",
    "ResumeEnhancementRequest",
    "ChatRequest",
    "ChatResponse",
    "ResumeSuggestion",
    "ResumeEnhancement",
    
    # API Response Wrapper
    "APIResponse",
    "HealthCheckResponse",
]
