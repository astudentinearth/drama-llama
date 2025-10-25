"""
Tool Decision Engine for intelligent tool calling decisions.

This module provides a sophisticated decision mechanism for determining
when and which tools to call based on user intent, context, and system state.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple, Union
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import json
import re

from models.schemas import IntentType, IntentDetectionRequest, IntentDetectionResponse
from services.OllamaClient import OllamaClient
from utils.tool_validator import ToolValidator, ToolExecutionMonitor
from utils.decision_monitor import DecisionMonitor

logger = logging.getLogger(__name__)


class ToolCallDecision(str, Enum):
    """Decision outcomes for tool calling."""
    CALL_TOOL = "call_tool"
    NO_TOOL = "no_tool"
    CLARIFY_INTENT = "clarify_intent"
    DECLINE_REQUEST = "decline_request"


class ToolExecutionStatus(str, Enum):
    """Tool execution result status."""
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL_SUCCESS = "partial_success"
    SKIPPED = "skipped"


@dataclass
class ToolDecisionContext:
    """Context for tool decision making."""
    user_message: str
    conversation_history: List[Dict[str, str]]
    available_tools: List[str]
    previous_tool_calls: List[Dict[str, Any]] = None
    user_profile: Dict[str, Any] = None
    system_state: Dict[str, Any] = None


@dataclass
class ToolDecision:
    """Result of tool decision analysis."""
    decision: ToolCallDecision
    confidence: float
    recommended_tools: List[str]
    reasoning: str
    extracted_params: Dict[str, Any]
    requires_clarification: bool = False
    clarification_questions: List[str] = None


@dataclass
class ToolExecutionResult:
    """Result of tool execution."""
    tool_name: str
    status: ToolExecutionStatus
    result: Any
    error: Optional[str] = None
    execution_time: float = 0.0
    metadata: Dict[str, Any] = None

class IntentionResult:
    """Result of intention detection."""
    intent: IntentType
    confidence: float
    extracted_params: Dict[str, Any]
    requires_clarification: bool
    clarification_questions: List[str]

class ToolDecisionEngine:
    """
    Intelligent tool decision engine that determines when and which tools to call.
    
    This engine uses multiple strategies:
    1. Intent detection using LLM
    2. Pattern matching for common requests
    3. Context analysis from conversation history
    4. Tool availability and prerequisites checking
    5. Confidence scoring and fallback mechanisms
    """
    
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client
        self.validator = ToolValidator()
        self.monitor = ToolExecutionMonitor()
        self.decision_monitor = DecisionMonitor()
        self.decision_history: List[Dict[str, Any]] = []
        self.tool_execution_history: List[ToolExecutionResult] = []
        
        # Tool definitions with metadata
        self.tool_definitions = {
            "createRoadmapSkeleton": {
                "description": "Creates a learning roadmap for skill development",
                "prerequisites": [],
                "triggers": [
                    "roadmap", "learning path", "skill development", "career path",
                    "what should I learn", "how to become", "prepare for job",
                    "learning plan", "study plan", "curriculum"
                ],
                "required_params": ["user_request"],
                "optional_params": ["job_listings", "user_summarized_cv", "user_expertise_domains"],
                "confidence_threshold": 0.7
            },
            "createLearningMaterials": {
                "description": "Creates learning materials for specific topics",
                "prerequisites": ["createRoadmapSkeleton"],
                "triggers": [
                    "learning materials", "resources", "tutorials", "exercises",
                    "practice materials", "study resources", "course content"
                ],
                "required_params": ["things_to_learn", "end_of_roadmap_project"],
                "optional_params": [],
                "confidence_threshold": 0.8
            }
        }
        
        # Intent patterns for quick matching
        self.intent_patterns = {
            IntentType.GENERATE_ROADMAP: [
                r"(?i)(create|build|generate|make).*(roadmap|learning path|study plan)",
                r"(?i)(what|how).*(should i learn|to become|to get into)",
                r"(?i)(prepare|ready).*(for|to get).*(job|position|role)",
                r"(?i)(skill|skills).*(development|learning|improvement)",
                r"(?i)(career|professional).*(development|growth|path)"
            ],
            IntentType.GENERATE_COURSE: [
                r"(?i)(create|build|generate).*(course|materials|resources)",
                r"(?i)(learning|study).*(materials|resources|content)",
                r"(?i)(tutorials|exercises|practice).*(for|about)",
                r"(?i)(teach me|show me).*(how to|about)"
            ]
        }
    
    async def analyze_intent(self, context: ToolDecisionContext) -> IntentDetectionResponse:
        """
        Analyze user intent using LLM and pattern matching.
        
        Args:
            context: Decision context with user message and history
            
        Returns:
            IntentDetectionResponse with detected intent and confidence
        """
        try:
            # Quick pattern matching first
            pattern_confidence = self._pattern_match_intent(context.user_message)
            
            # LLM-based intent detection
            llm_response = await self._llm_intent_detection(context)
            
            # Combine results with weighted scoring
            final_intent = self._combine_intent_results(pattern_confidence, llm_response)
            
            return final_intent
            
        except Exception as e:
            logger.error(f"Intent analysis failed: {e}")
            return IntentDetectionResponse(
                intent=IntentType.CHAT,
                confidence=0.0,
                extracted_params={},
                requires_clarification=True,
                clarification_questions=["Could you please clarify what you'd like help with?"]
            )
    
    def _pattern_match_intent(self, message: str) -> Dict[str, float]:
        """Quick pattern matching for common intents."""
        scores = {}
        
        for intent_type, patterns in self.intent_patterns.items():
            max_score = 0.0
            for pattern in patterns:
                if re.search(pattern, message):
                    # Calculate confidence based on pattern match strength
                    confidence = min(0.9, 0.5 + (len(re.findall(pattern, message)) * 0.1))
                    max_score = max(max_score, confidence)
            
            if max_score > 0:
                scores[intent_type] = max_score
        
        return scores
    
    async def _llm_intent_detection(self, context: ToolDecisionContext) -> IntentDetectionResponse:
        """Use LLM for sophisticated intent detection."""
        prompt = f"""
        Analyze the user's intent from their message and conversation history.
        
        User Message: "{context.user_message}"
        
        Conversation History: {json.dumps(context.conversation_history[-3:], indent=2)}
        
        Available Intents:
        - CHAT: General conversation, questions, advice
        - GENERATE_ROADMAP: User wants a learning roadmap or career path
        - GENERATE_COURSE: User wants learning materials or course content
        
        Available Extracted Parameters:
        - job_listings (list of links to job listings)

        Determine:
        1. The most likely intent
        2. Confidence score (0.0-1.0)
        3. Any extracted parameters
        4. Whether clarification is needed
        """
        
        try:
            response = await self.ollama_client.generate(
                prompt="Analyze the user's intent from their message and conversation history. Only respond in JSON format.",
                system_prompt=prompt,
                temperature=0.1,
                format=IntentDetectionResponse.model_json_schema()
            )

            print(response)
            
            response_json = json.loads(response.get("response", ""))
            return IntentDetectionResponse(**response_json)
        except Exception as e:
            logger.error(f"LLM intent detection error: {e}")
            return IntentDetectionResponse(
                intent=IntentType.CHAT,
                confidence=0.0,
                extracted_params={},
                requires_clarification=True
            )
    
    def _combine_intent_results(self, pattern_scores: Dict[str, float], 
                               llm_response: IntentDetectionResponse) -> IntentDetectionResponse:
        """Combine pattern matching and LLM results."""
        if not pattern_scores:
            return llm_response
        
        # Find best pattern match
        best_pattern_intent = max(pattern_scores.items(), key=lambda x: x[1])
        pattern_intent, pattern_confidence = best_pattern_intent
        
        # Weighted combination: 60% LLM, 40% pattern matching
        if llm_response.intent == pattern_intent:
            combined_confidence = (llm_response.confidence * 0.6) + (pattern_confidence * 0.4)
        else:
            # If they disagree, use the higher confidence one
            if llm_response.confidence > pattern_confidence:
                combined_confidence = llm_response.confidence * 0.8
            else:
                combined_confidence = pattern_confidence * 0.8
                llm_response.intent = pattern_intent
        
        llm_response.confidence = min(1.0, combined_confidence)
        return llm_response
    
    async def make_tool_decision(self, context: ToolDecisionContext) -> ToolDecision:
        """
        Make a decision about whether to call tools and which ones.
        
        Args:
            context: Decision context
            
        Returns:
            ToolDecision with recommendation
        """
        try:
            # Step 1: Analyze intent
            intent_response = await self.analyze_intent(context)
            
            # Step 2: Determine if tools should be called
            decision = self._determine_tool_decision(intent_response, context)
            
            # Step 3: Select appropriate tools
            recommended_tools = self._select_tools(decision, intent_response, context)
            
            # Step 4: Extract parameters
            extracted_params = self._extract_parameters(intent_response, context)
            
            # Step 5: Generate reasoning
            reasoning = self._generate_reasoning(decision, intent_response, recommended_tools)
            
            # Log decision
            self._log_decision(context, decision, recommended_tools, reasoning)
            
            # Log to decision monitor
            self.decision_monitor.log_decision({
                "decision": decision.value,
                "confidence": intent_response.confidence,
                "reasoning": reasoning,
                "recommended_tools": recommended_tools,
                "extracted_params": extracted_params,
                "user_message": context.user_message,
                "session_id": context.user_profile.get("session_id", "anonymous") if context.user_profile else "anonymous"
            })
            
            return ToolDecision(
                decision=decision,
                confidence=intent_response.confidence,
                recommended_tools=recommended_tools,
                reasoning=reasoning,
                extracted_params=extracted_params,
                requires_clarification=intent_response.requires_clarification,
                clarification_questions=intent_response.clarification_questions
            )
            
        except Exception as e:
            logger.error(f"Tool decision failed: {e}")
            return ToolDecision(
                decision=ToolCallDecision.NO_TOOL,
                confidence=0.0,
                recommended_tools=[],
                reasoning=f"Decision failed due to error: {str(e)}",
                extracted_params={}
            )
    
    def _determine_tool_decision(self, intent_response: IntentDetectionResponse, 
                                context: ToolDecisionContext) -> ToolCallDecision:
        """Determine the tool calling decision based on intent and context."""
        
        # Check if request is career/skill related
        if not self._is_career_related(context.user_message):
            return ToolCallDecision.DECLINE_REQUEST
        
        # Check confidence threshold
        if intent_response.confidence < 0.5:
            return ToolCallDecision.CLARIFY_INTENT
        
        # Check for tool-specific intents
        if intent_response.intent in [IntentType.GENERATE_ROADMAP, IntentType.GENERATE_COURSE]:
            return ToolCallDecision.CALL_TOOL
        
        # Check for explicit tool triggers
        if self._has_tool_triggers(context.user_message):
            return ToolCallDecision.CALL_TOOL
        
        # Default to no tool for general conversation
        return ToolCallDecision.NO_TOOL
    
    def _is_career_related(self, message: str) -> bool:
        """Check if message is career or skill development related."""
        career_keywords = [
            "career", "job", "skill", "learn", "study", "develop", "improve",
            "roadmap", "path", "course", "training", "education", "professional"
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in career_keywords)
    
    def _has_tool_triggers(self, message: str) -> bool:
        """Check if message contains tool trigger phrases."""
        message_lower = message.lower()
        
        for tool_name, tool_def in self.tool_definitions.items():
            for trigger in tool_def["triggers"]:
                if trigger.lower() in message_lower:
                    return True
        
        return False
    
    def _select_tools(self, decision: ToolCallDecision, intent_response: IntentDetectionResponse,
                     context: ToolDecisionContext) -> List[str]:
        """Select appropriate tools based on decision and context."""
        if decision != ToolCallDecision.CALL_TOOL:
            return []
        
        selected_tools = []
        
        # Check tool prerequisites
        for tool_name, tool_def in self.tool_definitions.items():
            if self._should_call_tool(tool_name, intent_response, context):
                selected_tools.append(tool_name)
        
        return selected_tools
    
    def _should_call_tool(self, tool_name: str, intent_response: IntentDetectionResponse,
                        context: ToolDecisionContext) -> bool:
        """Determine if a specific tool should be called."""
        tool_def = self.tool_definitions.get(tool_name)
        if not tool_def:
            return False
        
        # Check confidence threshold
        if intent_response.confidence < tool_def["confidence_threshold"]:
            return False
        
        # Check prerequisites
        for prereq in tool_def["prerequisites"]:
            if not self._prerequisite_met(prereq, context):
                return False
        
        # Check if message matches tool triggers
        message_lower = context.user_message.lower()
        for trigger in tool_def["triggers"]:
            if trigger.lower() in message_lower:
                return True
        
        return False
    
    def _prerequisite_met(self, prerequisite: str, context: ToolDecisionContext) -> bool:
        """Check if a tool prerequisite is met."""
        if prerequisite == "createRoadmapSkeleton":
            # Check if roadmap was created in recent conversation
            for msg in context.conversation_history[-5:]:
                if "roadmap" in msg.get("content", "").lower():
                    return True
        return False
    
    def _extract_parameters(self, intent_response: IntentDetectionResponse,
                           context: ToolDecisionContext) -> Dict[str, Any]:
        """Extract parameters for tool calls."""
        params = intent_response.extracted_params.copy()
        
        # Add user message as user_request for roadmap creation
        if "createRoadmapSkeleton" in context.available_tools:
            params["user_request"] = context.user_message
        
        return params
    
    def _generate_reasoning(self, decision: ToolCallDecision, intent_response: IntentDetectionResponse,
                          recommended_tools: List[str]) -> str:
        """Generate human-readable reasoning for the decision."""
        if decision == ToolCallDecision.CALL_TOOL:
            return f"User intent '{intent_response.intent}' with confidence {intent_response.confidence:.2f} suggests calling tools: {', '.join(recommended_tools)}"
        elif decision == ToolCallDecision.CLARIFY_INTENT:
            return f"Intent unclear (confidence: {intent_response.confidence:.2f}), need clarification"
        elif decision == ToolCallDecision.DECLINE_REQUEST:
            return "Request not related to career/skill development"
        else:
            return "General conversation, no tools needed"
    
    def _log_decision(self, context: ToolDecisionContext, decision: ToolCallDecision,
                     recommended_tools: List[str], reasoning: str):
        """Log the decision for monitoring and debugging."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_message": context.user_message[:100] + "..." if len(context.user_message) > 100 else context.user_message,
            "decision": decision.value,
            "recommended_tools": recommended_tools,
            "reasoning": reasoning,
            "conversation_length": len(context.conversation_history)
        }
        
        self.decision_history.append(log_entry)
        logger.info(f"Tool decision: {decision.value} - {reasoning}")
    
    async def execute_tools(self, tools: List[str], params: Dict[str, Any],
                           context: ToolDecisionContext) -> List[ToolExecutionResult]:
        """
        Execute the recommended tools with proper error handling and validation.
        
        Args:
            tools: List of tool names to execute
            params: Parameters for tool execution
            context: Decision context
            
        Returns:
            List of execution results
        """
        results = []
        
        for tool_name in tools:
            start_time = datetime.now()
            
            try:
                # Validate tool call before execution
                validation = await self.validator.validate_tool_call(
                    tool_name, params, {
                        "conversation_history": context.conversation_history,
                        "user_profile": context.user_profile,
                        "system_state": context.system_state
                    }
                )
                
                if not validation.is_valid:
                    logger.warning(f"Tool validation failed for {tool_name}: {validation.errors}")
                    execution_result = ToolExecutionResult(
                        tool_name=tool_name,
                        status=ToolExecutionStatus.FAILED,
                        result=None,
                        error=f"Validation failed: {', '.join(validation.errors)}",
                        execution_time=0.0,
                        metadata={"validation_errors": validation.errors}
                    )
                    results.append(execution_result)
                    continue
                
                # Execute tool with fallback mechanisms
                result, success, message = await self.validator.execute_with_fallback(
                    tool_name, params, self._get_tool_function(tool_name), {
                        "conversation_history": context.conversation_history,
                        "user_profile": context.user_profile,
                        "system_state": context.system_state
                    }
                )
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                execution_result = ToolExecutionResult(
                    tool_name=tool_name,
                    status=ToolExecutionStatus.SUCCESS if success else ToolExecutionStatus.FAILED,
                    result=result,
                    error=None if success else message,
                    execution_time=execution_time,
                    metadata={
                        "timestamp": start_time.isoformat(),
                        "validation_warnings": validation.warnings,
                        "validation_suggestions": validation.suggestions
                    }
                )
                
                results.append(execution_result)
                self.tool_execution_history.append(execution_result)
                
                # Record metrics for monitoring
                self.monitor.record_execution(
                    tool_name, success, execution_time, 
                    None if success else message
                )
                
                # Log to decision monitor
                self.decision_monitor.log_tool_execution({
                    "tool_name": tool_name,
                    "success": success,
                    "execution_time": execution_time,
                    "error": None if success else message,
                    "error_type": "validation_failed" if not success else None,
                    "session_id": context.user_profile.get("session_id", "anonymous") if context.user_profile else "anonymous"
                })
                
            except Exception as e:
                execution_time = (datetime.now() - start_time).total_seconds()
                logger.error(f"Tool execution failed for {tool_name}: {e}")
                
                execution_result = ToolExecutionResult(
                    tool_name=tool_name,
                    status=ToolExecutionStatus.FAILED,
                    result=None,
                    error=str(e),
                    execution_time=execution_time,
                    metadata={"timestamp": start_time.isoformat()}
                )
                
                results.append(execution_result)
                self.tool_execution_history.append(execution_result)
                
                # Record failed execution
                self.monitor.record_execution(
                    tool_name, False, execution_time, str(e)
                )
                
                # Log to decision monitor
                self.decision_monitor.log_tool_execution({
                    "tool_name": tool_name,
                    "success": False,
                    "execution_time": execution_time,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "session_id": context.user_profile.get("session_id", "anonymous") if context.user_profile else "anonymous"
                })
        
        return results
    
    async def _execute_single_tool(self, tool_name: str, params: Dict[str, Any],
                                  context: ToolDecisionContext) -> Any:
        """Execute a single tool with proper parameter mapping."""
        # Import tool functions dynamically
        from utils.llm_tools import createRoadmapSkeleton, createLearningMaterials
        
        tool_functions = {
            "createRoadmapSkeleton": createRoadmapSkeleton,
            "createLearningMaterials": createLearningMaterials
        }
        
        if tool_name not in tool_functions:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        tool_function = tool_functions[tool_name]
        
        # Map parameters to function arguments
        if tool_name == "createRoadmapSkeleton":
            return await tool_function(
                db=None,  # TODO: Pass actual db connection
                user_request=params.get("user_request", ""),
                job_listings=params.get("job_listings"),
                user_summarized_cv=params.get("user_summarized_cv"),
                user_expertise_domains=params.get("user_expertise_domains")
            )
        elif tool_name == "createLearningMaterials":
            return await tool_function(
                db=None,  # TODO: Pass actual db connection
                things_to_learn=params.get("things_to_learn", []),
                end_of_roadmap_project=params.get("end_of_roadmap_project", "")
            )
    
    def get_decision_stats(self) -> Dict[str, Any]:
        """Get statistics about decision making."""
        if not self.decision_history:
            return {"total_decisions": 0}
        
        decisions = [entry["decision"] for entry in self.decision_history]
        tool_calls = [entry for entry in self.decision_history if entry["decision"] == "call_tool"]
        
        return {
            "total_decisions": len(self.decision_history),
            "tool_calls": len(tool_calls),
            "no_tool_calls": len([d for d in decisions if d == "no_tool"]),
            "clarification_requests": len([d for d in decisions if d == "clarify_intent"]),
            "declined_requests": len([d for d in decisions if d == "decline_request"]),
            "tool_execution_success_rate": self._calculate_success_rate()
        }
    
    def _calculate_success_rate(self) -> float:
        """Calculate tool execution success rate."""
        if not self.tool_execution_history:
            return 0.0
        
        successful = len([r for r in self.tool_execution_history if r.status == ToolExecutionStatus.SUCCESS])
        total = len(self.tool_execution_history)
        
        return successful / total if total > 0 else 0.0
    
    def _get_tool_function(self, tool_name: str):
        """Get the tool function for execution."""
        from utils.llm_tools import createRoadmapSkeleton, createLearningMaterials
        
        tool_functions = {
            "createRoadmapSkeleton": createRoadmapSkeleton,
            "createLearningMaterials": createLearningMaterials
        }
        
        if tool_name not in tool_functions:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        return tool_functions[tool_name]
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health including decision engine and tool execution."""
        decision_stats = self.get_decision_stats()
        monitor_health = self.monitor.get_system_health()
        decision_monitor_health = self.decision_monitor.get_system_health_report()
        
        return {
            "decision_engine": decision_stats,
            "tool_execution": monitor_health,
            "decision_monitoring": decision_monitor_health,
            "overall_status": "healthy" if decision_stats.get("tool_execution_success_rate", 0) > 0.8 else "degraded"
        }
    
    def get_analytics_report(self) -> Dict[str, Any]:
        """Get comprehensive analytics report."""
        return {
            "decision_metrics": self.decision_monitor.get_decision_metrics(),
            "performance_metrics": self.decision_monitor.get_performance_metrics(),
            "error_analysis": self.decision_monitor.get_error_analysis(),
            "system_health": self.get_system_health(),
            "export_data": self.decision_monitor.export_analytics("json")
        }
