"""
Graduation Project Questions routes.
Handles generation and submission of graduation project assessment questions.
"""

from typing import List, Dict, Any, Optional
import json
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db_config import get_db
from db_config.crud import (
    get_session,
    get_roadmap_by_session,
    get_goals_by_roadmap,
    get_materials_by_goal,
    create_graduation_project_question,
    get_graduation_project_questions_by_session,
    get_graduation_project_question_by_slug,
    create_graduation_project_submission,
    get_submissions_by_session,
    delete_graduation_project_questions_by_session,
    update_submission_evaluation
)
from models.schemas import (
    APIResponse,
    GenerateQuestionsResponse,
    GraduationProjectQuestionSchema,
    GraduationProjectContext,
    SubmitAnswersRequest,
    SubmitAnswersResponse,
    QuestionDifficulty
)
from models.db_models import QuestionDifficultyEnum
from utils.auth import verify_api_key
from utils.prompt_loader import PromptLoader
from utils.groq_client import GroqClient

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/ai/graduation-project",
    tags=["graduation-project"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(verify_api_key)]
)

# Initialize prompt loader and Groq client
prompt_loader = PromptLoader()
groq_client = GroqClient()


def generate_questions_from_session_data(
    session_id: int,
    graduation_project_title: str,
    graduation_project_description: str,
    goals: List[Any],
    db: Session
) -> GenerateQuestionsResponse:
    """
    Generate 5 open-ended graduation project questions using LLM.
    
    This function uses the createGraduationProject prompt to generate
    comprehensive assessment questions based on session data.
    """
    
    # Extract material data for question generation
    all_materials = []
    goals_data = []
    
    for goal in goals:
        materials = get_materials_by_goal(db, goal.id)
        materials_data = []
        
        for material in materials:
            # Truncate content for summary (first 500 chars)
            content_summary = (material.content[:500] + "...") if material.content and len(material.content) > 500 else (material.content or "")
            
            material_dict = {
                'id': material.id,
                'title': material.title,
                'material_type': material.material_type or 'lesson',
                'description': material.description or '',
                'difficulty_level': material.difficulty_level.value if material.difficulty_level else 'intermediate',
                'content_summary': content_summary
            }
            materials_data.append(material_dict)
            all_materials.append(material_dict)
        
        goal_dict = {
            'id': goal.id,
            'goal_number': goal.goal_number,
            'title': goal.title,
            'description': goal.description,
            'skill_level': goal.skill_level.value,
            'estimated_hours': goal.estimated_hours,
            'materials': materials_data
        }
        goals_data.append(goal_dict)
    
    # Load the prompt
    try:
        prompt_data = prompt_loader.get_prompt('creategraduationproject')
    except Exception as e:
        logger.error(f"Failed to load prompt: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load question generation prompt: {str(e)}"
        )
    
    # Render the prompt manually (simple variable replacement)
    try:
        system_prompt = prompt_data.get('system_prompt', '')
        user_prompt = prompt_data.get('user_prompt', '')
        
        # Add explicit JSON instruction to system prompt
        system_prompt += "\n\nIMPORTANT: You MUST respond with ONLY valid JSON. Do not include any explanatory text, markdown formatting, or code blocks. Your entire response must be a single valid JSON object starting with { and ending with }."
        
        # Replace simple variables
        user_prompt = user_prompt.replace('{{graduation_project_title}}', graduation_project_title)
        user_prompt = user_prompt.replace('{{graduation_project_description}}', graduation_project_description)
        user_prompt = user_prompt.replace('{{total_goals}}', str(len(goals_data)))
        
        # Handle goals array (basic Handlebars-like each replacement)
        goals_section = ""
        for goal in goals_data:
            goals_section += f"\n### Goal ID={goal['id']}, Goal {goal['goal_number']}: {goal['title']}\n"
            goals_section += f"**Goal ID:** {goal['id']} (USE THIS NUMBER in goals_covered)\n"
            goals_section += f"**Description:** {goal['description']}\n"
            goals_section += f"**Skill Level:** {goal['skill_level']}\n"
            goals_section += f"**Estimated Hours:** {goal['estimated_hours']}\n\n"
            goals_section += "#### Learning Materials:\n"
            
            for material in goal['materials']:
                goals_section += f"- **Material ID={material['id']}** (USE THIS NUMBER): {material['title']}\n"
                goals_section += f"  - **Type:** {material['material_type']}\n"
                goals_section += f"  - **Description:** {material['description']}\n"
                goals_section += f"  - **Difficulty:** {material['difficulty_level']}\n"
                goals_section += f"  - **Key Content Summary:** {material['content_summary']}\n"
        
        # Replace the goals section (find the handlebars block and replace it)
        import re
        goals_pattern = r'{{#each goals}}.*?{{/each}}'
        user_prompt = re.sub(goals_pattern, goals_section, user_prompt, flags=re.DOTALL)
        
        # Add a final reminder about using integer IDs
        user_prompt += "\n\nREMINDER: In your JSON response, goals_covered and materials_covered MUST contain only integer IDs (numbers), not strings. For example: \"goals_covered\": [27, 28], NOT \"goals_covered\": [\"Goal 1: Programming\"]"
        
    except Exception as e:
        logger.error(f"Failed to render prompt: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to render prompt: {str(e)}"
        )
    
    # Call LLM to generate questions
    try:
        logger.info("Calling LLM to generate graduation project questions...")
        response = groq_client.execute(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=4000,
            response_format={"type": "json_object"}  # Force JSON mode
        )
        
        # Parse the response
        response_text = response.get_content().strip()
        
        logger.info(f"Raw LLM response (first 200 chars): {response_text[:200]}")
        
        # Remove markdown code blocks if present
        if response_text.startswith('```'):
            # Find the first newline after ```json or ```
            first_newline = response_text.find('\n')
            last_backticks = response_text.rfind('```')
            if first_newline != -1 and last_backticks != -1:
                response_text = response_text[first_newline+1:last_backticks].strip()
        
        questions_data = json.loads(response_text)
        logger.info(f"Successfully generated {len(questions_data.get('questions', []))} questions")
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse LLM response: {e}")
        logger.error(f"Response text: {response_text[:500]}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to parse LLM response. Please try again."
        )
    except Exception as e:
        logger.error(f"Failed to generate questions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate questions: {str(e)}"
        )
    
    # Validate and create question schemas
    questions = []
    question_db_ids = []
    
    for q_data in questions_data.get('questions', []):
        try:
            # Create Pydantic schema for validation
            question_schema = GraduationProjectQuestionSchema(
                question_id=q_data['question_id'],
                prompt=q_data['prompt'],
                rationale=q_data['rationale'],
                goals_covered=q_data['goals_covered'],
                materials_covered=q_data['materials_covered'],
                expected_competencies=q_data['expected_competencies'],
                difficulty=QuestionDifficulty(q_data['difficulty']),
                estimated_time_minutes=q_data['estimated_time_minutes'],
                evaluation_rubric=q_data['evaluation_rubric'],
                answer_min_chars=q_data.get('answer_min_chars', 500),
                answer_max_chars=q_data.get('answer_max_chars', 2500),
                requires_material_citations=False  # Citations not required
            )
            questions.append(question_schema)
            
            # Create database record
            db_question = create_graduation_project_question(
                db=db,
                session_id=session_id,
                question_id=question_schema.question_id,
                prompt=question_schema.prompt,
                rationale=question_schema.rationale,
                goals_covered=question_schema.goals_covered,
                materials_covered=question_schema.materials_covered,
                expected_competencies=question_schema.expected_competencies,
                difficulty=QuestionDifficultyEnum(question_schema.difficulty.value),
                estimated_time_minutes=question_schema.estimated_time_minutes,
                evaluation_rubric=question_schema.evaluation_rubric,
                answer_min_chars=question_schema.answer_min_chars,
                answer_max_chars=question_schema.answer_max_chars,
                requires_material_citations=question_schema.requires_material_citations
            )
            question_db_ids.append(db_question.id)
            
        except Exception as e:
            logger.error(f"Failed to create question: {e}")
            logger.error(f"Question data: {q_data}")
            continue
    
    if len(questions) != 5:
        logger.warning(f"Expected 5 questions, got {len(questions)}")
    
    return GenerateQuestionsResponse(
        graduation_project=GraduationProjectContext(
            title=graduation_project_title,
            description=graduation_project_description
        ),
        questions=questions,
        question_db_ids=question_db_ids
    )


@router.post("/{session_id}/generate-questions")
async def generate_graduation_questions(
    session_id: int,
    db: Session = Depends(get_db)
) -> APIResponse:
    """
    Generate 5 open-ended graduation project questions for a session.
    
    This endpoint:
    1. Fetches the session's roadmap and graduation project
    2. Analyzes all goals and their learning materials
    3. Generates 5 comprehensive questions covering all competencies
    4. Stores questions in the database
    5. Returns the structured question set
    """
    # Verify session exists
    session = get_session(db, session_id)   
    if not session:
        return APIResponse(
            success=False,
            error=f"Session {session_id} not found"
        )
    
    # Get roadmap
    roadmap = get_roadmap_by_session(db, session_id)
    if not roadmap:
        return APIResponse(
            success=False,
            error=f"No roadmap found for session {session_id}"
        )
    
    # Check if graduation project exists
    if not roadmap.graduation_project or not roadmap.graduation_project_title:
        return APIResponse(
            success=False,
            error="No graduation project defined in roadmap"
        )
    
    # Get all goals
    goals = get_goals_by_roadmap(db, roadmap.id)
    if not goals:
        return APIResponse(
            success=False,
            error="No goals found in roadmap"
        )
    
    # Delete existing questions if any
    delete_graduation_project_questions_by_session(db, session_id)
    
    # Generate questions
    try:
        response = generate_questions_from_session_data(
            session_id=session_id,
            graduation_project_title=roadmap.graduation_project_title,
            graduation_project_description=roadmap.graduation_project,
            goals=goals,
            db=db
        )
        
        return APIResponse(
            success=True,
            data=response.dict()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=f"Failed to generate questions: {str(e)}"
        )


@router.get("/{session_id}/questions")
async def get_graduation_questions(
    session_id: int,
    db: Session = Depends(get_db)
) -> APIResponse:
    """
    Get all graduation project questions for a session.
    """
    # Verify session exists
    session = get_session(db, session_id)
    if not session:
        return APIResponse(
            success=False,
            error=f"Session {session_id} not found"
        )
    
    # Get questions
    questions = get_graduation_project_questions_by_session(db, session_id)
    
    # Get roadmap for context
    roadmap = get_roadmap_by_session(db, session_id)
    if not roadmap:
        return APIResponse(
            success=False,
            error=f"No roadmap found for session {session_id}"
        )
    
    # Format response
    questions_data = [
        {
            "question_id": q.question_id,
            "prompt": q.prompt,
            "rationale": q.rationale,
            "goals_covered": q.goals_covered,
            "materials_covered": q.materials_covered,
            "expected_competencies": q.expected_competencies,
            "difficulty": q.difficulty.value,
            "estimated_time_minutes": q.estimated_time_minutes,
            "evaluation_rubric": q.evaluation_rubric,
            "answer_min_chars": q.answer_min_chars,
            "answer_max_chars": q.answer_max_chars,
            "requires_material_citations": q.requires_material_citations
        }
        for q in questions
    ]
    
    return APIResponse(
        success=True,
        data={
            "graduation_project": {
                "title": roadmap.graduation_project_title,
                "description": roadmap.graduation_project
            },
            "questions": questions_data
        }
    )


async def evaluate_submission(submission_id: int, db: Session) -> Dict[str, Any]:
    """
    Evaluate a single submission using LLM.
    
    Args:
        submission_id: ID of the submission to evaluate
        db: Database session
    
    Returns:
        Dictionary with evaluation results
    """
    # Get submission with question
    from models.db_models import GraduationProjectSubmission, LearningMaterial
    submission = db.query(GraduationProjectSubmission).filter(
        GraduationProjectSubmission.id == submission_id
    ).first()
    
    if not submission:
        raise ValueError(f"Submission {submission_id} not found")
    
    question = submission.question
    
    # Get relevant materials
    relevant_materials = []
    for material_id in question.materials_covered:
        material = db.query(LearningMaterial).filter(
            LearningMaterial.id == material_id
        ).first()
        
        if material:
            # Extract key concepts from material (first 300 chars or description)
            key_concepts = material.description or ""
            if len(key_concepts) > 300:
                key_concepts = key_concepts[:300] + "..."
            
            relevant_materials.append({
                'id': material.id,
                'title': material.title,
                'description': material.description or "",
                'key_concepts': key_concepts
            })
    
    # Load evaluation prompt
    try:
        prompt_data = prompt_loader.get_prompt('evaluategraduationprojectanswer')
    except Exception as e:
        logger.error(f"Failed to load evaluation prompt: {e}")
        raise
    
    # Render prompt manually
    try:
        system_prompt = prompt_data.get('system_prompt', '')
        user_prompt = prompt_data.get('user_prompt', '')
        output_format = prompt_data.get('output_format', '')
        
        # Add explicit JSON instruction to system prompt
        system_prompt += "\n\nIMPORTANT: You MUST respond with ONLY valid JSON. Do not include any explanatory text, markdown formatting, or code blocks. Your entire response must be a single valid JSON object starting with { and ending with }."
        
        # Replace simple variables
        user_prompt = user_prompt.replace('{{question_id}}', question.question_id)
        user_prompt = user_prompt.replace('{{question_prompt}}', question.prompt)
        user_prompt = user_prompt.replace('{{answer_text}}', submission.answer_text)
        user_prompt = user_prompt.replace('{{answer_length}}', str(len(submission.answer_text)))
        user_prompt = user_prompt.replace('{{citations_count}}', '0')  # No citations
        
        # Handle expected_competencies {{#each}} block
        competencies_text = ""
        for comp in question.expected_competencies:
            competencies_text += f"- {comp}\n"
        import re
        user_prompt = re.sub(
            r'{{#each expected_competencies}}.*?{{/each}}',
            competencies_text,
            user_prompt,
            flags=re.DOTALL
        )
        
        # Handle evaluation_rubric {{#each}} block
        rubric_text = ""
        for idx, criterion in enumerate(question.evaluation_rubric, 1):
            rubric_text += f"{idx}. {criterion}\n"
        user_prompt = re.sub(
            r'{{#each evaluation_rubric}}.*?{{/each}}',
            rubric_text,
            user_prompt,
            flags=re.DOTALL
        )
        
        # Handle relevant_materials {{#each}} block
        materials_text = ""
        for material in relevant_materials:
            materials_text += f"\n### Material {material['id']}: {material['title']}\n"
            materials_text += f"**Description:** {material['description']}\n"
            materials_text += f"**Key Concepts:** {material['key_concepts']}\n"
        user_prompt = re.sub(
            r'{{#each relevant_materials}}.*?{{/each}}',
            materials_text,
            user_prompt,
            flags=re.DOTALL
        )
        
        # Remove the entire {{#if citations}} block since we don't use citations
        user_prompt = re.sub(
            r'{{#if citations}}.*?{{/if}}',
            '',
            user_prompt,
            flags=re.DOTALL
        )
        
        # Append output format instructions to the end of user prompt
        if output_format:
            user_prompt += "\n\n" + output_format
        
    except Exception as e:
        logger.error(f"Failed to render evaluation prompt: {e}")
        raise
    
    # Call LLM for evaluation
    try:
        logger.info(f"Evaluating submission {submission_id} with LLM...")
        logger.info(f"System prompt length: {len(system_prompt)}, User prompt length: {len(user_prompt)}")
        
        response = groq_client.execute(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=3000,  # Increased for complex evaluation response
            response_format={"type": "json_object"}  # Force JSON mode
        )
        
        # Parse response
        response_text = response.get_content().strip()
        
        logger.info(f"Evaluation response length: {len(response_text)}")
        logger.info(f"Evaluation response (first 500 chars): {response_text[:500]}")
        logger.info(f"Evaluation response (last 200 chars): {response_text[-200:]}")
        
        # Remove markdown code blocks if present
        if response_text.startswith('```'):
            first_newline = response_text.find('\n')
            last_backticks = response_text.rfind('```')
            if first_newline != -1 and last_backticks != -1:
                response_text = response_text[first_newline+1:last_backticks].strip()
        
        evaluation_data = json.loads(response_text)
        logger.info(f"Successfully evaluated submission {submission_id}")
        logger.info(f"Evaluation data keys: {evaluation_data.keys()}")
        
        # Validate required keys
        required_keys = ['overall_score', 'feedback']
        missing_keys = [key for key in required_keys if key not in evaluation_data]
        if missing_keys:
            logger.error(f"Missing required keys in evaluation response: {missing_keys}")
            logger.error(f"Full evaluation data: {json.dumps(evaluation_data, indent=2)}")
            raise ValueError(f"LLM response missing required keys: {missing_keys}")
        
        # Update submission with evaluation results
        update_submission_evaluation(
            db=db,
            submission_id=submission_id,
            evaluation_score=evaluation_data.get('overall_score', 0.0),
            evaluation_feedback=evaluation_data.get('feedback', ''),
            rubric_scores=evaluation_data.get('rubric_scores')
        )
        
        return {
            "submission_id": submission_id,
            "question_id": question.question_id,
            "score": evaluation_data.get('overall_score', 0.0),
            "feedback": evaluation_data.get('feedback', ''),
            "rubric_scores": evaluation_data.get('rubric_scores')
        }
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse evaluation response: {e}")
        logger.error(f"Response text: {response_text[:500]}")
        raise
    except Exception as e:
        logger.error(f"Failed to evaluate submission: {e}")
        raise


@router.post("/{session_id}/submit")
async def submit_graduation_answers(
    session_id: int,
    request: SubmitAnswersRequest,
    db: Session = Depends(get_db)
) -> APIResponse:
    """
    Submit answers to graduation project questions.
    
    Validates:
    - Session exists
    - Exactly 5 answers provided
    - All question_ids are valid
    - Answer lengths are within bounds
    """
    # Verify session exists
    session = get_session(db, session_id)
    if not session:
        return APIResponse(
            success=False,
            error=f"Session {session_id} not found"
        )
    
    # Verify exactly 5 answers
    if len(request.answers) != 5:
        return APIResponse(
            success=False,
            error=f"Expected exactly 5 answers, got {len(request.answers)}"
        )
    
    # Get all questions for this session
    questions = get_graduation_project_questions_by_session(db, session_id)
    question_map = {q.question_id: q for q in questions}
    
    if len(questions) != 5:
        return APIResponse(
            success=False,
            error=f"Expected 5 questions in database, found {len(questions)}"
        )
    
    # Validate each answer
    submission_ids = []
    errors = []
    
    for answer in request.answers:
        # Check if question exists
        if answer.question_id not in question_map:
            errors.append(f"Invalid question_id: {answer.question_id}")
            continue
        
        question = question_map[answer.question_id]
        
        # Check answer length
        if len(answer.text) < question.answer_min_chars:
            errors.append(f"Answer for '{answer.question_id}' is too short (minimum {question.answer_min_chars} chars)")
        
        if len(answer.text) > question.answer_max_chars:
            errors.append(f"Answer for '{answer.question_id}' is too long (maximum {question.answer_max_chars} chars)")
    
    if errors:
        return APIResponse(
            success=False,
            error="; ".join(errors)
        )
    
    # Create submissions
    try:
        for answer in request.answers:
            question = question_map[answer.question_id]
            submission = create_graduation_project_submission(
                db=db,
                session_id=session_id,
                question_id=question.id,
                answer_text=answer.text,
                citations=None  # No citations needed
            )
            submission_ids.append(submission.id)
        
        # Trigger AI evaluation for all submissions
        logger.info(f"Starting AI evaluation for {len(submission_ids)} submissions...")
        from models.schemas import SubmissionEvaluation
        evaluation_results = []
        
        for submission_id in submission_ids:
            try:
                eval_result = await evaluate_submission(submission_id, db)
                evaluation = SubmissionEvaluation(
                    submission_id=eval_result['submission_id'],
                    question_id=eval_result['question_id'],
                    score=eval_result['score'],
                    feedback=eval_result['feedback'],
                    rubric_scores=eval_result.get('rubric_scores')
                )
                evaluation_results.append(evaluation)
            except Exception as e:
                logger.error(f"Failed to evaluate submission {submission_id}: {e}")
                # Add error result
                evaluation_results.append(SubmissionEvaluation(
                    submission_id=submission_id,
                    question_id="unknown",
                    score=0.0,
                    feedback="",
                    error=str(e)
                ))
        
        response_data = SubmitAnswersResponse(
            session_id=session_id,
            submission_ids=submission_ids,
            message="Answers submitted and evaluated successfully",
            evaluations=evaluation_results
        )
        
        return APIResponse(
            success=True,
            data=response_data.dict()
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=f"Failed to submit answers: {str(e)}"
        )


@router.get("/{session_id}/submissions")
async def get_graduation_submissions(
    session_id: int,
    db: Session = Depends(get_db)
) -> APIResponse:
    """
    Get all submissions for a session's graduation project questions.
    """
    # Verify session exists
    session = get_session(db, session_id)
    if not session:
        return APIResponse(
            success=False,
            error=f"Session {session_id} not found"
        )
    
    # Get submissions
    submissions = get_submissions_by_session(db, session_id)
    
    # Format response
    submissions_data = [
        {
            "id": s.id,
            "question_id": s.question.question_id,
            "answer_text": s.answer_text,
            "citations": s.citations,
            "evaluation_score": s.evaluation_score,
            "evaluation_feedback": s.evaluation_feedback,
            "rubric_scores": s.rubric_scores,
            "submitted_at": s.submitted_at.isoformat(),
            "evaluated_at": s.evaluated_at.isoformat() if s.evaluated_at else None
        }
        for s in submissions
    ]
    
    return APIResponse(
        success=True,
        data={
            "session_id": session_id,
            "submissions": submissions_data,
            "total": len(submissions_data)
        }
    )
