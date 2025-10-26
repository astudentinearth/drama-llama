export interface ISession {
  id: number;
  user_id: string;
  session_name: string;
  description: string;
  status: string;
  created_at: string;
  updated_at: string;
  completed_at: string | null;
}

export interface IRoadmap {
  id: number;
  user_request: string;
  total_estimated_weeks: number;
  graduation_project: string;
  graduation_project_title: string;
  status: string;
  created_at: string;
}

export interface IMaterial {
  id: number;
  goal_id: number;
  title: string;
  material_type: string;
  description: string;
  content: string;
  estimated_time_minutes: number;
  difficulty_level: string;
  is_completed: boolean;
}

export interface IGoal {
  id: number;
  goal_number: number;
  title: string;
  description: string;
  priority: number;
  skill_level: string;
  estimated_hours: number;
  actual_hours_spent: number;
  completion_percentage: number;
  materials: IMaterial[];
}

export interface FullSessionResponse {
  success: true;
  data: {
    session: ISession;
    roadmap: IRoadmap;
    goals: IGoal[];
  };
  error: null;
}

export interface SessionProgress {
  total_goals: number;
  completed_goals: number;
  total_materials: number;
  completed_materials: number;
  total_hours_estimated: number;
  total_hours_spent: number;
  completion_percentage: number;
}

export interface IToolCall {
    tool_name: string;
    arguments: Record<string, string>;
    call_id: string;
}

export interface IMessageMetadata {
    has_tool_calls: boolean;
    tool_calls: IToolCall[];
    usage: {
        prompt_tokens: number;
        completion_tokens: number;
        total_tokens: number;
    
    }
}

export interface IMessage {
    role: "user" | "assistant";
    content: string;
    timestamp: string;
    metadata: IMessageMetadata;
}

export interface RoadmapResponse {
    success: true;
    data: {
        roadmap: IRoadmap;
        goals: IGoal[];
    };
    error: null;
}

// Graduation Project Types
export interface IGraduationProject {
    title: string;
    description: string;
}

export interface IQuestion {
    question_id: string;
    prompt: string;
    rationale: string;
    goals_covered: number[];
    materials_covered: number[];
    expected_competencies: string[];
    difficulty: "beginner" | "intermediate" | "advanced";
    estimated_time_minutes: number;
    evaluation_rubric: string[];
    answer_min_chars: number;
    answer_max_chars: number;
    requires_material_citations: boolean;
}

export interface GenerateQuestionsResponse {
    success: true;
    data: {
        graduation_project: IGraduationProject;
        questions: IQuestion[];
        graduation_project_db_id: number | null;
        question_db_ids: number[];
    };
    error: null;
}

export interface GetQuestionsResponse {
    success: true;
    data: {
        graduation_project: IGraduationProject;
        questions: IQuestion[];
    };
    error: null;
}

export interface IAnswer {
    question_id: string;
    text: string;
}

export interface SubmitAnswersRequest {
    session_id: number;
    answers: IAnswer[];
}

export interface SubmitAnswersResponse {
    success: true;
    data: {
        message: string;
        score?: number;
        feedback?: string;
    };
    error: null;
}

