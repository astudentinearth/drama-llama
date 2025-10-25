from models import ChatRequest, ChatResponse
from models.Prompt import Prompt
from models.schemas import RoadmapResponse, LearningMaterialResponse
from services.OllamaClient import OllamaClient
from utils.tool_decision_engine import ToolDecisionEngine, ToolDecisionContext, ToolCallDecision
import asyncio
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)
"""
When user stated he/she want to apply for a job, how can I develop my self etc. this tool should be triggered.
This tool briefly takes summary of user request, and the links mentioned.
"""
async def createRoadmapSkeleton(user_request: str, job_listings: Optional[list[str]] = None, user_summarized_cv: Optional[str] = None, user_expertise_domains: Optional[list[str]] = None) -> str:
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
    
    # 5. put things-to-learn array and end of roadmap project details in session-db
    
    # 6. return this array and project inside a friendly/professinal text
    return async_response.get("response", "")

async def createLearningMaterials(things_to_learn: list[str], end_of_roadmap_project: str) -> str:
    learningmaterialsrequest = {
        "thingsToLearn": things_to_learn if things_to_learn else [],
        "endOfRoadmapProject": end_of_roadmap_project if end_of_roadmap_project else ""
    }
    prompt = Prompt("createlearningmaterials", format=learningmaterialsrequest)
    assert prompt is not None, "Prompt 'createlearningmaterials' could not be loaded."

    ollama_client = OllamaClient()
    response = ollama_client.generate(
        prompt=prompt.get_user_prompt(),
        system_prompt=prompt.get_system_prompt(),
        temperature=0.2,
        format=LearningMaterialResponse.model_json_schema()
    )

    # crawl web

    # scrape top 3 results

    # Check cache for old generations

    # 

    async_response = await response
    if not async_response.get("success", False):
        raise Exception(f"Failed to generate learning materials: {async_response.get('error', 'Unknown error')}")
    
    return async_response.get("response", "")

async def master(request: ChatRequest) -> Dict[str, Any]:
    """
    Enhanced master function with intelligent tool decision making.
    
    This function now uses the ToolDecisionEngine to intelligently determine
    when and which tools to call based on user intent and context.
    """
    try:
        # Initialize decision engine
        ollama_client = OllamaClient()
        decision_engine = ToolDecisionEngine(ollama_client)
        
        # Create decision context
        context = ToolDecisionContext(
            user_message=request.userPrompt,
            conversation_history=request.previousMessages,
            available_tools=["createRoadmapSkeleton", "createLearningMaterials"],
            previous_tool_calls=[]  # TODO: Extract from conversation history
        )
        
        # Make intelligent tool decision
        tool_decision = await decision_engine.make_tool_decision(context)
        
        logger.debug(f"Tool decision: {tool_decision}")
        
        logger.info(f"Tool decision: {tool_decision.decision.value} - {tool_decision.reasoning}")
        
        # Handle different decision outcomes
        if tool_decision.decision == ToolCallDecision.DECLINE_REQUEST:
            return {
                "response": "I'm sorry, but I can only help with career and skill development topics. Please ask me about learning paths, skill development, or career guidance.",
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
            return {
                "response": f"I'd be happy to help! {clarification_questions[0]}",
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
                return await _generate_tool_response(ollama_client, tool_results, request)
            else:
                # Fallback to regular chat if no tools were executed
                return await _generate_regular_response(ollama_client, request)
        
        else:  # NO_TOOL
            # Regular conversation without tools
            return await _generate_regular_response(ollama_client, request)
    
    except Exception as e:
        logger.error(f"Master function error: {e}")
        return {
            "response": "I apologize, but I encountered an error processing your request. Please try again.",
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