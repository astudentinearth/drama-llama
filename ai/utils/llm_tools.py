from models import ChatRequest, ChatResponse
from models.Prompt import Prompt
from models.schemas import RoadmapResponse, LearningMaterialResponse
from services.OllamaClient import OllamaClient
from utils.tool_decision_engine import ToolDecisionEngine, ToolDecisionContext, ToolCallDecision
import asyncio
from typing import Optional, Dict, Any
import logging
import json
from sqlalchemy.orm import Session
from db_config.crud import add_message_to_session, get_session_messages, create_roadmap, create_goal, get_roadmap_by_session, get_goals_by_roadmap, create_learning_material
from models.schemas import MessageCreate, MessageRole
from models.db_models import SkillLevelEnum
from datetime import datetime
logger = logging.getLogger(__name__)
"""
When user stated he/she want to apply for a job, how can I develop my self etc. this tool should be triggered.
This tool briefly takes summary of user request, and the links mentioned.
"""
async def createRoadmapSkeleton(db: Session, session_id: int, user_request: str, job_listings: Optional[list[str]] = None, user_summarized_cv: Optional[str] = None, user_expertise_domains: Optional[list[str]] = None) -> str:
    jobListings = ["this is an example job listing, requiring skills in python, django, rest api, sql, git, docker"]
    
    # 0. load prompt with variables
    roadmaprequest = {
        "userRequest": user_request if user_request else "",
        "jobListings": job_listings if job_listings else [],
        "userExperience": user_summarized_cv if user_summarized_cv else "",
        "userDomains": user_expertise_domains if user_expertise_domains else []
    }
    
    prompt = Prompt("createroadmapskeleton", format=roadmaprequest)
    assert prompt is not None, "Prompt 'createroadmapskeleton' could not be loaded."
    
    # 1. using users expertise domain(s) and users past experiences, generate search sentences and store
    
    # 2. search web for roadmaps/learningpaths about the requested expertise and store
    
    # 3. then using user request and related joblisting summarizations, find users needs to create roadmap (for example: user knows node.js , job needs express.js , don't request to learn node.js, since they are related to eachother)
    # 3.1 get joblistings from job microservice
    
    
    
    # 4. using created needs, create an ordered list of things-to-learn array and a end of roadmap project that summarizes all the materials and puts in use.
    # use ollama client here with the loaded prompt
    ollama_client = OllamaClient()
    response = ollama_client.generate(
        prompt=prompt.get_user_prompt(),
        system_prompt=prompt.get_system_prompt(),
        temperature=0.2,
        format=RoadmapResponse.model_json_schema()
    )
    
    async_response = await response
    if not async_response.get("success", False):
        raise Exception(f"Failed to generate roadmap skeleton: {async_response.get('error', 'Unknown error')}")
    
    # 5. Parse the LLM response and save to database
    try:
        # Parse the JSON response into RoadmapResponse model
        roadmap_data = json.loads(async_response.get("response", "{}"))
        roadmap_response = RoadmapResponse(**roadmap_data)
        
        # Create the roadmap in the database
        db_roadmap = create_roadmap(
            db=db,
            session_id=session_id,
            user_request=user_request,
            user_summarized_cv=user_summarized_cv,
            user_expertise_domains=user_expertise_domains,
            job_listings=job_listings,
            total_estimated_weeks=roadmap_response.total_estimated_weeks,
            graduation_project=roadmap_response.graduation_project
        )
        
        # Create roadmap goals in the database
        for goal in roadmap_response.goals:
            create_goal(
                db=db,
                roadmap_id=db_roadmap.id,
                goal_number=goal.goal_number,
                title=goal.title,
                description=goal.description,
                priority=goal.priority,
                skill_level=SkillLevelEnum.BEGINNER,  # Default for now
                estimated_hours=goal.estimated_hours,
                prerequisites=goal.prerequisites
            )
        
        logger.info(f"Created roadmap (ID: {db_roadmap.id}) with {len(roadmap_response.goals)} goals for session {session_id}")
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse roadmap response JSON: {e}")
        raise Exception(f"Failed to parse roadmap response: {str(e)}")
    except Exception as e:
        logger.error(f"Failed to save roadmap to database: {e}")
        raise Exception(f"Failed to save roadmap: {str(e)}")
    
    # 6. return this array and project inside a friendly/professional text
    return async_response.get("response", "")

async def createLearningMaterials(db: Session, session_id: int) -> str:
    """
    Generate learning materials for all goals in a roadmap.
    Retrieves the roadmap and its goals, generates materials for each goal,
    and saves them to the database.
    """
    # Get the roadmap for this session
    roadmap = get_roadmap_by_session(db, session_id)
    if not roadmap:
        raise Exception(f"No roadmap found for session {session_id}")
    
    # Get all goals for this roadmap
    goals = get_goals_by_roadmap(db, roadmap.id)
    if not goals:
        raise Exception(f"No goals found for roadmap {roadmap.id}")
    
    # Prepare the request for the LLM
    things_to_learn = [{"goal_id": goal.id, "title": goal.title, "description": goal.description} for goal in goals]
    learningmaterialsrequest = {
        "thingsToLearn": things_to_learn,
        "endOfRoadmapProject": roadmap.graduation_project if roadmap.graduation_project else ""
    }
    
    prompt = Prompt("createlearningmaterial", format=learningmaterialsrequest)
    assert prompt is not None, "Prompt 'createlearningmaterials' could not be loaded."

    ollama_client = OllamaClient()
    
    # Generate materials for each goal
    materials_created = 0
    all_materials = []
    
    for goal in goals:
        # Generate learning materials for this specific goal
        goal_request = {
            "goal": {
                "goal_number": goal.goal_number,
                "title": goal.title,
                "description": goal.description,
                "estimated_hours": goal.estimated_hours
            },
            "endOfRoadmapProject": roadmap.graduation_project if roadmap.graduation_project else ""
        }
        
        response = ollama_client.generate(
            prompt=prompt.get_user_prompt(),
            system_prompt=prompt.get_system_prompt(),
            temperature=0.2,
            format=LearningMaterialResponse.model_json_schema()
        )

        async_response = await response
        if not async_response.get("success", False):
            logger.warning(f"Failed to generate materials for goal {goal.id}: {async_response.get('error', 'Unknown error')}")
            continue
        
        try:
            # Parse the response
            material_data = json.loads(async_response.get("response", "{}"))
            material_response = LearningMaterialResponse(**material_data)
            
            # Save the learning material to database
            db_material = create_learning_material(
                db=db,
                goal_id=goal.id,
                title=f"Learning Materials for {goal.title}",
                material_type="comprehensive",
                content=material_response.material,
                description=f"Curated learning materials for {goal.title}",
                estimated_time_minutes=goal.estimated_hours * 60 if goal.estimated_hours else None,
                difficulty_level=goal.skill_level,
                end_of_material_project=material_response.end_of_material_project,
                relevance_score=1.0,
                quality_score=0.8
            )
            
            materials_created += 1
            all_materials.append({
                "goal": goal.title,
                "material_id": db_material.id,
                "material": material_response.material[:200] + "..." if len(material_response.material) > 200 else material_response.material
            })
            
            logger.info(f"Created learning material (ID: {db_material.id}) for goal {goal.id}")
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse learning material response for goal {goal.id}: {e}")
            continue
        except Exception as e:
            logger.error(f"Failed to save learning material for goal {goal.id}: {e}")
            continue
    
    if materials_created == 0:
        raise Exception("Failed to generate any learning materials")
    
    # Return a summary
    summary = f"Successfully generated {materials_created} learning materials for {len(goals)} goals.\n\n"
    for material_info in all_materials:
        summary += f"- {material_info['goal']}: Material created (ID: {material_info['material_id']})\n"
    
    logger.info(f"Created {materials_created} learning materials for session {session_id}")
    return summary

async def master(request: ChatRequest, db: Session) -> Dict[str, Any]:
    """
    Enhanced master function with intelligent tool decision making.
    
    This function now uses the ToolDecisionEngine to intelligently determine
    when and which tools to call based on user intent and context.
    """
    initial_message = MessageCreate(
        role=MessageRole.USER,
        content=request.userPrompt,
        metadata={
            "timestamp": datetime.utcnow().isoformat()
        }
    )

    session_id = request.session_id

    # get previous messages using session_id
    previous_messages = get_session_messages(db, session_id)

    # Save user message immediately
    add_message_to_session(db, session_id, initial_message.role, initial_message.content, initial_message.metadata)

    try:
        # Initialize decision engine
        ollama_client = OllamaClient()
        decision_engine = ToolDecisionEngine(ollama_client)
        
        # Create decision context
        context = ToolDecisionContext(
            user_message=request.userPrompt,
            conversation_history=previous_messages,
            available_tools=["createRoadmapSkeleton", "createLearningMaterials"],
            previous_tool_calls=[],  # TODO: Extract from conversation history
            db=db,
            session_id=session_id
        )
        
        # Make intelligent tool decision
        tool_decision = await decision_engine.make_tool_decision(context)
        
        logger.debug(f"Tool decision: {tool_decision}")
        
        logger.info(f"Tool decision: {tool_decision.decision.value} - {tool_decision.reasoning}")
        
        # Handle different decision outcomes
        if tool_decision.decision == ToolCallDecision.DECLINE_REQUEST:
            response_text = "I'm sorry, but I can only help with career and skill development topics. Please ask me about learning paths, skill development, or career guidance."
            add_message_to_session(db, session_id, MessageRole.ASSISTANT, response_text, {"timestamp": datetime.utcnow().isoformat()})
            return {
                "response": response_text,
                "decision_metadata": {
                    "decision": tool_decision.decision.value,
                    "reasoning": tool_decision.reasoning,
                    "confidence": tool_decision.confidence
                }
            }
        
        elif tool_decision.decision == ToolCallDecision.CLARIFY_INTENT:
            clarification_questions = tool_decision.clarification_questions or [
                "Could you please clarify what you'd like help with? Are you looking for career guidance, skill development, or learning resources?"
            ]
            response_text = f"I'd be happy to help! {clarification_questions[0]}"
            add_message_to_session(db, session_id, MessageRole.ASSISTANT, response_text, {"timestamp": datetime.utcnow().isoformat()})
            return {
                "response": response_text,
                "decision_metadata": {
                    "decision": tool_decision.decision.value,
                    "reasoning": tool_decision.reasoning,
                    "confidence": tool_decision.confidence,
                    "clarification_needed": True
                }
            }
        
        elif tool_decision.decision == ToolCallDecision.CALL_TOOL:
            # Execute recommended tools
            tool_results = await decision_engine.execute_tools(
                tools=tool_decision.recommended_tools,
                params=tool_decision.extracted_params,
                context=context
            )
            
            # Generate response based on tool results
            if tool_results:
                generated_response = await _generate_tool_response(ollama_client, tool_results, request)
                response_text = generated_response.get("response", "")
                add_message_to_session(db, session_id, MessageRole.ASSISTANT, response_text, {"timestamp": datetime.utcnow().isoformat()})
                return generated_response
            else:
                # Fallback to regular chat if no tools were executed
                generated_response = await _generate_regular_response(ollama_client, request)
                response_text = generated_response.get("response", "")
                add_message_to_session(db, session_id, MessageRole.ASSISTANT, response_text, {"timestamp": datetime.utcnow().isoformat()})
                return generated_response
        
        else:  # NO_TOOL
            # Regular conversation without tools
            generated_response = await _generate_regular_response(ollama_client, request)
            response_text = generated_response.get("response", "")
            add_message_to_session(db, session_id, MessageRole.ASSISTANT, response_text, {"timestamp": datetime.utcnow().isoformat()})
            return generated_response

    except Exception as e:
        logger.error(f"Master function error: {e}")
        error_response = "I apologize, but I encountered an error processing your request. Please try again."
        add_message_to_session(db, session_id, MessageRole.ASSISTANT, error_response, {"timestamp": datetime.utcnow().isoformat(), "error": str(e)})
        return {
            "response": error_response,
            "error": str(e),
            "decision_metadata": {
                "decision": "error",
                "reasoning": f"Error occurred: {str(e)}"
            }
        }


async def _generate_tool_response(ollama_client: OllamaClient, tool_results: list, request: ChatRequest) -> Dict[str, Any]:
    """Generate response after tool execution."""
    # Prepare tool context
    tool_context = "\n\n".join([
        f"Tool: {result.tool_name}\nStatus: {result.status.value}\nResult: {result.result}" 
        for result in tool_results if result.status.value == "success"
    ])
    
    # Generate final response
    final_prompt = f"""Based on the tool execution results below, provide a clear, friendly, and helpful response to the user.

Tool Results:
{tool_context}

Please format this information in a natural, conversational way that helps the user understand their learning roadmap and next steps."""

    response = await ollama_client.generate(
        prompt=final_prompt,
        system_prompt="You are a helpful career development assistant. Present information in a clear, motivating, and well-structured way.",
        temperature=0.4
    )
    
    return {
        "response": response.get("response", ""),
        "tool_results": [
            {
                "name": result.tool_name,
                "status": result.status.value,
                "result": result.result,
                "execution_time": result.execution_time
            }
            for result in tool_results
        ],
        "decision_metadata": {
            "decision": "call_tool",
            "tools_executed": [result.tool_name for result in tool_results],
            "success_count": len([r for r in tool_results if r.status.value == "success"])
        }
    }


async def _generate_regular_response(ollama_client: OllamaClient, request: ChatRequest) -> Dict[str, Any]:
    """Generate regular chat response without tools."""
    prompt = Prompt("master", request)
    assert prompt is not None, "Prompt 'master' could not be loaded."
    
    response = await ollama_client.generate(
        prompt=prompt.get_user_prompt(),
        system_prompt=prompt.get_system_prompt(),
        temperature=0.4
    )
    
    return {
        "response": response.get("response", ""),
        "decision_metadata": {
            "decision": "no_tool",
            "reasoning": "Regular conversation without tool calls"
        }
    }