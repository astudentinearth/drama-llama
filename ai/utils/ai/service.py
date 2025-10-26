"""
AI Service Layer.
Handles AI operations including tool planning and execution.
"""

import json
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from utils.groq_client import GroqClient, AIResponse
from utils.ai.tool_specs import get_tool_definitions, get_response_schema, get_tool_spec
from models.Prompt import Prompt
from models.schemas import (
    AIToolResponse,
    ToolCallInstruction,
    RoadmapSkeletonResponse,
    LearningMaterialResponse,
    RoadmapGoalSchema,
    QuizForGoalResponse,
    LearningExample
)
from db_config.crud import (
    get_session_messages,
    get_session,
    get_roadmap_by_session,
    get_goals_by_roadmap,
    get_goal,
    get_materials_by_roadmap,
    create_roadmap,
    create_goal,
    create_learning_material
)
from models.db_models import SkillLevelEnum

class AIService:
    """
    AI Service for handling AI operations with Groq.
    Inspired by Functions.php from reference.
    """
    
    def __init__(self, groq_client: Optional[GroqClient] = None):
        """
        Initialize AI Service.
        
        Args:
            groq_client: Optional GroqClient instance. Creates new if not provided.
        """
        self.client = groq_client or GroqClient()
    
    def plan_action(
        self,
        session_id: int,
        user_prompt: str,
        db: Session
    ) -> AIToolResponse:
        """
        Analyze user request and return tool call instructions.
        Does NOT execute tools - returns instructions to frontend.
        
        Args:
            session_id: Session ID for context
            user_prompt: User's current request
            db: Database session
        
        Returns:
            AIToolResponse with tool call instructions
        """
        # Load session from database
        session = get_session(db, session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        # Get session message history
        message_history = get_session_messages(db, session_id)
        formatted_history = Prompt.format_session_history(message_history)
        
        # Exclude the last message if it matches the current user_prompt
        # (The current message was already saved to DB before calling plan_action)
        if formatted_history and formatted_history[-1].get('content') == user_prompt:
            formatted_history = formatted_history[:-1]
        
        # Format history as string for prompt (last 10 messages)
        # Make it very clear who said what
        history_str = ""
        if not formatted_history:
            history_str = "(No previous conversation - this is the first message)"
        else:
            for i, msg in enumerate(formatted_history[-10:], 1):
                role_label = "User said" if msg['role'] == 'user' else "You replied"
                history_str += f"{i}. {role_label}: {msg['content']}\n"
        
        # Check if roadmap exists for context
        roadmap = get_roadmap_by_session(db, session_id)
        has_roadmap = roadmap is not None

        learning_materials = get_materials_by_roadmap(db, roadmap.id) if has_roadmap else []
        has_learning_materials = len(learning_materials) > 0
        
        # Conditionally provide tools based on roadmap existence
        # This prevents the AI from trying to use unavailable functionality
        if has_learning_materials:
            # Roadmap exists: User can create learning materials OR create a new roadmap
            available_tools = []
        elif has_roadmap:
            available_tools = ["createLearningMaterials"]
        else:
            # No roadmap: User can ONLY create a roadmap first
            available_tools = ["createRoadmapSkeleton"]
        
        # Build context for the AI
        context_info = f"Session #{session_id}"
        if has_roadmap:
            goals = get_goals_by_roadmap(db, roadmap.id)
            context_info += f"\n- Existing roadmap: {roadmap.graduation_project_title}"
            context_info += f"\n- Total goals: {len(goals)}"
            context_info += f"\n- Completed goals: {sum(1 for g in goals if g.is_completed)}"
            context_info += "\n- Available goals for learning:"
            for goal in goals:
                status = "✓ Completed" if goal.is_completed else "○ Not started"
                context_info += f"\n  * Goal ID {goal.id}: {goal.title} [{status}]"
        else:
            context_info += "\n- No roadmap exists yet."
        
        # Load master prompt
        prompt = Prompt('master', {
            'previousMessages': history_str,
            'userPrompt': user_prompt,
            'content': context_info
        })
        
        # Get tool definitions
        tool_definitions = get_tool_definitions(available_tools)
        
        # Execute with tools
        messages = prompt.get_messages()
        
        # DEBUG: Log what we're sending to the AI
        import logging
        logger = logging.getLogger(__name__)
        logger.info("="*80)
        logger.info("SENDING TO AI:")
        logger.info(f"Session ID: {session_id}")
        logger.info(f"User Prompt: {user_prompt}")
        logger.info(f"History String:\n{history_str}")
        logger.info(f"Context Info:\n{context_info}")
        logger.info("-"*80)
        logger.info("FORMATTED MESSAGES:")
        for i, msg in enumerate(messages):
            logger.info(f"Message {i} ({msg['role']}):")
            logger.info(f"{msg['content'][:500]}...")  # First 500 chars
        logger.info("="*80)
        
        response = self.client.execute_with_tools(
            messages=messages,
            tools=tool_definitions,
            tool_choice='auto'
        )
        
        # Convert to AIToolResponse
        tool_calls = []
        if response.has_tool_calls():
            for tc in response.get_tool_calls():
                tool_name = tc['function']['name']
                arguments_str = tc['function']['arguments']
                
                # Parse arguments JSON
                try:
                    arguments = json.loads(arguments_str)
                except json.JSONDecodeError:
                    arguments = {}
                
                tool_calls.append(ToolCallInstruction(
                    tool_name=tool_name,
                    arguments=arguments,
                    call_id=tc['id']
                ))
        
        return AIToolResponse(
            content=response.get_content(),
            has_tool_calls=response.has_tool_calls(),
            tool_calls=tool_calls,
            finish_reason=response.get_finish_reason(),
            usage=response.get_usage()
        )
    
    def plan_action_stream(
        self,
        session_id: int,
        user_prompt: str,
        db: Session
    ):
        """
        Analyze user request and stream the response with tool call instructions.
        Yields chunks as they arrive from the LLM.
        
        Args:
            session_id: Session ID for context
            user_prompt: User's current request
            db: Database session
        
        Yields:
            Streaming chunks from the AI response
        """
        # Load session from database
        session = get_session(db, session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        # Get session message history
        message_history = get_session_messages(db, session_id)
        formatted_history = Prompt.format_session_history(message_history)
        
        # Exclude the last message if it matches the current user_prompt
        if formatted_history and formatted_history[-1].get('content') == user_prompt:
            formatted_history = formatted_history[:-1]
        
        # Format history as string for prompt (last 10 messages)
        history_str = ""
        if not formatted_history:
            history_str = "(No previous conversation - this is the first message)"
        else:
            for i, msg in enumerate(formatted_history[-10:], 1):
                role_label = "User said" if msg['role'] == 'user' else "You replied"
                history_str += f"{i}. {role_label}: {msg['content']}\n"
        
        # Check if roadmap exists for context
        roadmap = get_roadmap_by_session(db, session_id)
        has_roadmap = roadmap is not None
        
        # Conditionally provide tools based on roadmap existence
        if has_roadmap:
            available_tools = ["createLearningMaterials"]
        else:
            available_tools = ["createRoadmapSkeleton"]
        
        # Build context for the AI
        context_info = f"Session #{session_id}"
        if has_roadmap:
            goals = get_goals_by_roadmap(db, roadmap.id)
            context_info += f"\n- Existing roadmap: {roadmap.graduation_project_title}"
            context_info += f"\n- Total goals: {len(goals)}"
            context_info += f"\n- Completed goals: {sum(1 for g in goals if g.is_completed)}"
            context_info += "\n- Available goals for learning:"
            for goal in goals:
                status = "✓ Completed" if goal.is_completed else "○ Not started"
                context_info += f"\n  * Goal ID {goal.id}: {goal.title} [{status}]"
        else:
            context_info += "\n- No roadmap exists yet. You must create one first."
        
        # Load master prompt
        prompt = Prompt('master', {
            'previousMessages': history_str,
            'userPrompt': user_prompt,
            'content': context_info
        })
        
        # Get tool definitions
        tool_definitions = get_tool_definitions(available_tools)
        
        # Execute with tools in streaming mode
        messages = prompt.get_messages()
        
        # Stream the response
        for chunk in self.client.stream(
            messages=messages,
            tools=tool_definitions,
            tool_choice='auto'
        ):
            yield chunk
    
    def execute_roadmap_creation(
        self,
        session_id: int,
        tool_arguments: Dict[str, Any],
        db: Session
    ) -> RoadmapSkeletonResponse:
        """
        Execute createRoadmapSkeleton with structured output.
        Returns validated Pydantic model and saves to database.
        
        Args:
            session_id: Session ID
            tool_arguments: Arguments from tool call (userRequest, etc.)
            db: Database session
        
        Returns:
            RoadmapSkeletonResponse with created roadmap
        """
        # Check if roadmap already exists
        existing_roadmap = get_roadmap_by_session(db, session_id)
        if existing_roadmap:
            # Return existing roadmap instead of creating duplicate
            goals = get_goals_by_roadmap(db, existing_roadmap.id)
            return RoadmapSkeletonResponse(
                goals=[
                    RoadmapGoalSchema(
                        goal_number=goal.goal_number,
                        title=goal.title,
                        description=goal.description,
                        priority=goal.priority,
                        estimated_hours=goal.estimated_hours,
                        prerequisites=goal.prerequisites or []
                    )
                    for goal in sorted(goals, key=lambda g: g.goal_number)
                ],
                graduation_project=existing_roadmap.graduation_project or "",
                graduation_project_title=existing_roadmap.graduation_project_title or ""
            )
        
        # Load the roadmap creation prompt
        prompt = Prompt('createroadmapskeleton', {
            'userRequest': tool_arguments.get('userRequest', ''),
            'userExperience': tool_arguments.get('userExperience', 'Not provided'),
            'userDomains': tool_arguments.get('userDomains', 'Not specified'),
            'jobListings': tool_arguments.get('jobListings', 'No job listings provided')
        })
        
        # Get response format from prompt
        response_format = prompt.get_response_format()
        
        # Execute with structured output
        messages = prompt.get_messages()
        response = self.client.execute(
            messages=messages,
            response_format=response_format,
            temperature=prompt.get_temperature()
        )
        
        # Parse the JSON response
        content = response.get_content()
        try:
            roadmap_data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse roadmap response: {e}")
        
        # Validate with Pydantic
        roadmap_response = RoadmapSkeletonResponse(**roadmap_data)
        
        # Save to database
        self._save_roadmap_to_db(session_id, roadmap_response, tool_arguments, db)
        
        return roadmap_response

    def edit_roadmap_skeleton(
        self,
        session_id: int,
        tool_arguments: Dict[str, Any],
        db: Session
    ) -> RoadmapSkeletonResponse:
        """
        Execute editRoadmapSkeleton with structured output.
        Returns validated Pydantic model and saves to database.
        """
        # Get the roadmap
        roadmap = get_roadmap_by_session(db, session_id)
        if not roadmap:
            raise ValueError(f"No roadmap found for session {session_id}")
        # Load the roadmap creation prompt
        prompt = Prompt('editroadmapskeleton', {
            'userRequest': tool_arguments.get('userRequest', ''),
            'currentRoadmap': tool_arguments.get('currentRoadmap', 'Not provided'),
        })
        
        # Get response format from prompt
        response_format = prompt.get_response_format()
        
        # Execute with structured output
        messages = prompt.get_messages()
        response = self.client.execute(
            messages=messages,
            response_format=response_format,
            temperature=prompt.get_temperature()
        )
        
        # Parse the JSON response
        content = response.get_content()
        try:
            roadmap_data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse roadmap response: {e}")
        
        # Validate with Pydantic
        roadmap_response = RoadmapSkeletonResponse(**roadmap_data)
        
        # Save to database
        self._save_roadmap_to_db(session_id, roadmap_response, tool_arguments, db)
        return roadmap_response

    def execute_roadmap_skeleton_editing(
        self,
        session_id: int,
        tool_arguments: Dict[str, Any],
        db: Session
    ) -> RoadmapSkeletonResponse:
        """
        Execute editRoadmapSkeleton with structured output.
        Returns validated Pydantic model and saves to database.
        """
        # Get the roadmap
        roadmap = get_roadmap_by_session(db, session_id)
        if not roadmap:
            raise ValueError(f"No roadmap found for session {session_id}")
        
        # Load the roadmap editing prompt
        prompt = Prompt('editroadmapskeleton', {
            'userRequest': tool_arguments.get('userRequest', ''),
            'currentRoadmap': tool_arguments.get('currentRoadmap', 'Not provided'),
        })
        
        # Get response format from prompt
        response_format = prompt.get_response_format()
        
        # Execute with structured output
        messages = prompt.get_messages()
        response = self.client.execute(
            messages=messages,
            response_format=response_format,
            temperature=prompt.get_temperature()
        )
        
        # Parse the JSON response
        content = response.get_content()
        try:
            roadmap_data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse roadmap response: {e}")
        
        # Validate with Pydantic
        roadmap_response = RoadmapSkeletonResponse(**roadmap_data)
        
        # Save to database
        self._save_roadmap_to_db(session_id, roadmap_response, tool_arguments, db)
        return roadmap_response

    def execute_material_creation(
        self,
        goal_id: int,
        session_id: int,
        db: Session
    ) -> LearningMaterialResponse:
        """
        Execute createLearningMaterials with structured output.
        Returns validated Pydantic model and saves to database.
        
        Args:
            goal_id: Goal ID to create materials for
            session_id: Session ID for context
            db: Database session
        
        Returns:
            LearningMaterialResponse with created materials
        """
        # Get the goal
        goal = get_goal(db, goal_id)
        if not goal:
            raise ValueError(f"Goal {goal_id} not found")
        
        # Get roadmap to find previous and next goals
        roadmap = get_roadmap_by_session(db, session_id)
        if not roadmap:
            raise ValueError(f"No roadmap found for session {session_id}")
        
        goals = get_goals_by_roadmap(db, roadmap.id)
        
        # Find previous and next goals
        current_goal_number = goal.goal_number
        previous_goal = next((g for g in goals if g.goal_number == current_goal_number - 1), None)
        next_goal = next((g for g in goals if g.goal_number == current_goal_number + 1), None)
        
        # Load the learning material prompt
        prompt = Prompt('createlearningmaterial', {
            'currentGoalTitle': goal.title,
            'currentGoalDescription': goal.description,
            'previousGoalTitle': previous_goal.title if previous_goal else "None (first goal)",
            'previousGoalDescription': previous_goal.description if previous_goal else "",
            'nextGoalTitle': next_goal.title if next_goal else "None (final goal)",
            'nextGoalDescription': next_goal.description if next_goal else ""
        })
        
        # Get response format from prompt
        response_format = prompt.get_response_format()
        
        # Execute with structured output
        messages = prompt.get_messages()
        response = self.client.execute(
            messages=messages,
            response_format=response_format,
            temperature=prompt.get_temperature()
        )
        
        # Parse the JSON response
        content = response.get_content()
        try:
            material_data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse learning material response: {e}")
        
        # Validate with Pydantic
        material_response = LearningMaterialResponse(**material_data)
        
        # Save to database
        self._save_material_to_db(goal_id, material_response, db)
        
        return material_response
    
    def _save_roadmap_to_db(
        self,
        session_id: int,
        roadmap_response: RoadmapSkeletonResponse,
        tool_arguments: Dict[str, Any],
        db: Session
    ):
        """Save roadmap and goals to database."""
        # Calculate total estimated weeks (assuming 10 hours per week)
        total_hours = sum(goal.estimated_hours for goal in roadmap_response.goals)
        total_weeks = max(1, total_hours // 10)
        
        # Create roadmap
        roadmap = create_roadmap(
            db=db,
            session_id=session_id,
            user_request=tool_arguments.get('userRequest', ''),
            total_estimated_weeks=total_weeks,
            graduation_project=roadmap_response.graduation_project,
            graduation_project_title=roadmap_response.graduation_project_title
        )
        
        # Create goals
        for goal_data in roadmap_response.goals:
            # Determine skill level based on priority
            if goal_data.priority <= 2:
                skill_level = SkillLevelEnum.ADVANCED
            elif goal_data.priority == 3:
                skill_level = SkillLevelEnum.INTERMEDIATE
            else:
                skill_level = SkillLevelEnum.BEGINNER
            
            create_goal(
                db=db,
                roadmap_id=roadmap.id,
                goal_number=goal_data.goal_number,
                title=goal_data.title,
                description=goal_data.description,
                priority=goal_data.priority,
                skill_level=skill_level,
                estimated_hours=goal_data.estimated_hours,
                prerequisites=goal_data.prerequisites
            )
    
    def _save_material_to_db(
        self,
        goal_id: int,
        material_response: LearningMaterialResponse,
        db: Session
    ):
        """Save learning material to database."""
        # Determine difficulty level based on goal
        goal = get_goal(db, goal_id)
        difficulty_level = goal.skill_level if goal else SkillLevelEnum.INTERMEDIATE
        
        # Use Markdown content directly from response
        # The prompt instructs the model to include explanations, examples, and exercises in the content field
        full_content = material_response.content
        
        # No structured exercises provided in current schema; store empty list for project_requirements
        exercises_list: list = []
        
        create_learning_material(
            db=db,
            goal_id=goal_id,
            title=material_response.title,
            material_type="lesson",
            description=material_response.description,
            content=full_content,  # store Markdown content as-is
            estimated_time_minutes=material_response.estimated_time_minutes,
            difficulty_level=difficulty_level,
            project_requirements=exercises_list  # placeholder until structured exercises are added
        )
    
    def _save_quiz_to_db(
        self,
        goal_id: int,
        quiz_response: QuizForGoalResponse,
        db: Session
    ):
        """Save generated quiz to database."""
        from db_config.crud import create_quiz
        
        # Convert quiz questions to the format expected by create_quiz
        questions_data = []
        for question in quiz_response.quiz:
            questions_data.append({
                'question_text': question.question,
                'options': question.options,
                'correct_answer': question.correctAnswer,
                'explanation': question.explanation,
                'points': 1
            })
        
        # Create quiz with questions
        quiz = create_quiz(
            db=db,
            goal_id=goal_id,
            title=f"Quiz for Goal {goal_id}",
            description=f"Generated quiz questions for learning goal",
            time_limit_minutes=30,  # Default 30 minutes
            passing_score_percentage=70.0,
            max_attempts=3,
            questions_data=questions_data
        )
        
        return quiz
    
    def extract_cv_information(
        self,
        user_cv: str,
    ) -> str:
        """Extract CV information from the provided text."""
        prompt = Prompt('extractcvinformation', {
            'userCv': user_cv
        })
        messages = prompt.get_messages()
        response = self.client.execute(
            messages=messages,
            temperature=prompt.get_temperature()
        )
        return response.get_content()
    
    def execute_quiz_creation(
        self,
        goal_id: int,
        session_id: int,
        db: Session
    ) -> QuizForGoalResponse:
        """Execute quiz creation for a specific goal."""
        
        # Get goal information
        goal = get_goal(db, goal_id)
        if not goal:
            raise ValueError(f"Goal {goal_id} not found")
        
        # Create prompt for quiz generation
        prompt = Prompt('createquizforgoal', {
            'learningGoal': goal.title,
            'goalDescription': goal.description
        })
        
        # Get response format from prompt
        response_format = prompt.get_response_format()
        
        # Execute with structured output
        messages = prompt.get_messages()
        response = self.client.execute(
            messages=messages,
            response_format=response_format,
            temperature=prompt.get_temperature()
        )
        
        # Parse the JSON response
        content = response.get_content()
        try:
            quiz_data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse quiz response: {e}")
        
        # Validate with Pydantic
        quiz_response = QuizForGoalResponse(**quiz_data)
        
        # Save quiz to database
        self._save_quiz_to_db(goal_id, quiz_response, db)
        
        return quiz_response
        