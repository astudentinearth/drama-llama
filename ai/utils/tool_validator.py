"""
Tool Validation and Fallback Mechanisms.

This module provides validation, error handling, and fallback mechanisms
for tool execution to ensure robust operation.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of tool validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]


@dataclass
class FallbackStrategy:
    """Fallback strategy configuration."""
    strategy_type: str  # "retry", "alternative_tool", "graceful_degradation", "manual_fallback"
    max_attempts: int = 3
    delay_seconds: float = 1.0
    alternative_tools: List[str] = None
    degradation_message: str = ""


class ToolValidator:
    """
    Validates tool calls and provides fallback mechanisms.
    
    This class ensures that:
    1. Tool parameters are valid and complete
    2. Prerequisites are met
    3. System resources are available
    4. Fallback strategies are available when tools fail
    """
    
    def __init__(self):
        self.validation_rules = self._initialize_validation_rules()
        self.fallback_strategies = self._initialize_fallback_strategies()
        self.execution_history: List[Dict[str, Any]] = []
    
    def _initialize_validation_rules(self) -> Dict[str, Dict[str, Any]]:
        """Initialize validation rules for each tool."""
        return {
            "createRoadmapSkeleton": {
                "required_params": ["user_request"],
                "param_types": {
                    "user_request": str,
                    "job_listings": list,
                    "user_summarized_cv": str,
                    "user_expertise_domains": list
                },
                "param_validation": {
                    "user_request": lambda x: len(x.strip()) > 10,
                    "job_listings": lambda x: isinstance(x, list) and all(isinstance(item, str) for item in x),
                    "user_summarized_cv": lambda x: len(x.strip()) > 0 if x else True,
                    "user_expertise_domains": lambda x: isinstance(x, list) and all(isinstance(item, str) for item in x)
                },
                "prerequisites": [],
                "timeout_seconds": 30,
                "max_retries": 3
            },
            "createLearningMaterials": {
                "required_params": [],  # Gets everything from session's roadmap
                "param_types": {},
                "param_validation": {},
                "prerequisites": ["createRoadmapSkeleton"],
                "timeout_seconds": 60,  # Increased timeout as it generates multiple materials
                "max_retries": 2
            }
        }
    
    def _initialize_fallback_strategies(self) -> Dict[str, List[FallbackStrategy]]:
        """Initialize fallback strategies for each tool."""
        return {
            "createRoadmapSkeleton": [
                FallbackStrategy(
                    strategy_type="retry",
                    max_attempts=3,
                    delay_seconds=2.0
                ),
                FallbackStrategy(
                    strategy_type="graceful_degradation",
                    degradation_message="I'll provide you with general career guidance instead of a detailed roadmap."
                )
            ],
            "createLearningMaterials": [
                FallbackStrategy(
                    strategy_type="retry",
                    max_attempts=2,
                    delay_seconds=1.5
                ),
                FallbackStrategy(
                    strategy_type="alternative_tool",
                    alternative_tools=["createRoadmapSkeleton"],
                    degradation_message="I'll create a new roadmap instead of learning materials."
                ),
                FallbackStrategy(
                    strategy_type="graceful_degradation",
                    degradation_message="I'll provide you with general learning resources instead."
                )
            ]
        }
    
    async def validate_tool_call(self, tool_name: str, params: Dict[str, Any], 
                               context: Dict[str, Any] = None) -> ValidationResult:
        """
        Validate a tool call before execution.
        
        Args:
            tool_name: Name of the tool to validate
            params: Parameters for the tool call
            context: Additional context for validation
            
        Returns:
            ValidationResult with validation status and issues
        """
        errors = []
        warnings = []
        suggestions = []
        
        if tool_name not in self.validation_rules:
            errors.append(f"Unknown tool: {tool_name}")
            return ValidationResult(False, errors, warnings, suggestions)
        
        rules = self.validation_rules[tool_name]
        
        # Check required parameters
        for required_param in rules["required_params"]:
            if required_param not in params or params[required_param] is None:
                errors.append(f"Missing required parameter: {required_param}")
            elif not self._validate_parameter_type(required_param, params[required_param], rules):
                errors.append(f"Invalid type for parameter '{required_param}'")
            elif not self._validate_parameter_value(required_param, params[required_param], rules):
                errors.append(f"Invalid value for parameter '{required_param}'")
        
        # Check prerequisites
        if not self._check_prerequisites(tool_name, context or {}):
            errors.append(f"Prerequisites not met for tool: {tool_name}")
        
        # Check system resources
        resource_check = await self._check_system_resources(tool_name)
        if not resource_check["available"]:
            warnings.append(f"System resources may be limited: {resource_check['reason']}")
        
        # Generate suggestions for improvement
        if params.get("user_request") and len(params["user_request"]) < 20:
            suggestions.append("Consider providing more detailed information about your learning goals")
        
        is_valid = len(errors) == 0
        
        return ValidationResult(is_valid, errors, warnings, suggestions)
    
    def _validate_parameter_type(self, param_name: str, value: Any, rules: Dict[str, Any]) -> bool:
        """Validate parameter type."""
        expected_type = rules["param_types"].get(param_name)
        if expected_type is None:
            return True  # No type constraint
        
        if expected_type == list:
            return isinstance(value, list)
        elif expected_type == str:
            return isinstance(value, str)
        else:
            return isinstance(value, expected_type)
    
    def _validate_parameter_value(self, param_name: str, value: Any, rules: Dict[str, Any]) -> bool:
        """Validate parameter value using custom validation functions."""
        validation_func = rules["param_validation"].get(param_name)
        if validation_func is None:
            return True  # No validation constraint
        
        try:
            return validation_func(value)
        except Exception:
            return False
    
    def _check_prerequisites(self, tool_name: str, context: Dict[str, Any]) -> bool:
        """Check if tool prerequisites are met."""
        rules = self.validation_rules.get(tool_name, {})
        prerequisites = rules.get("prerequisites", [])
        
        if not prerequisites:
            return True
        
        # Check if prerequisites were met in recent conversation
        conversation_history = context.get("conversation_history", [])
        for prereq in prerequisites:
            if not self._prerequisite_met_in_conversation(prereq, conversation_history):
                return False
        
        return True
    
    def _prerequisite_met_in_conversation(self, prerequisite: str, conversation_history: List[Dict[str, str]]) -> bool:
        """Check if prerequisite was met in conversation history."""
        # Look for prerequisite indicators in recent messages
        recent_messages = conversation_history[-5:]  # Check last 5 messages
        
        for message in recent_messages:
            content = message.get("content", "").lower()
            if prerequisite == "createRoadmapSkeleton":
                if any(keyword in content for keyword in ["roadmap", "learning path", "study plan"]):
                    return True
        
        return False
    
    async def _check_system_resources(self, tool_name: str) -> Dict[str, Any]:
        """Check if system has sufficient resources for tool execution."""
        # This is a simplified check - in production, you'd check actual system metrics
        rules = self.validation_rules.get(tool_name, {})
        timeout = rules.get("timeout_seconds", 30)
        
        # Simulate resource check
        if timeout > 30:
            return {
                "available": True,
                "reason": "Sufficient resources available"
            }
        else:
            return {
                "available": True,
                "reason": "Resources adequate for execution"
            }
    
    async def execute_with_fallback(self, tool_name: str, params: Dict[str, Any], 
                                   tool_function, context: Dict[str, Any] = None) -> Tuple[Any, bool, str]:
        """
        Execute tool with fallback mechanisms.
        
        Args:
            tool_name: Name of the tool to execute
            params: Parameters for the tool
            tool_function: Function to execute
            context: Additional context
            
        Returns:
            Tuple of (result, success, message)
        """
        # Validate tool call first
        validation = await self.validate_tool_call(tool_name, params, context)
        
        if not validation.is_valid:
            return None, False, f"Validation failed: {', '.join(validation.errors)}"
        
        # Get fallback strategies
        strategies = self.fallback_strategies.get(tool_name, [])
        
        for strategy in strategies:
            try:
                if strategy.strategy_type == "retry":
                    result = await self._execute_with_retry(tool_function, params, strategy)
                    if result is not None:
                        return result, True, "Tool executed successfully"
                
                elif strategy.strategy_type == "alternative_tool":
                    # Try alternative tools
                    for alt_tool in strategy.alternative_tools:
                        try:
                            # This would need to be implemented based on your tool structure
                            alt_result = await self._execute_alternative_tool(alt_tool, params, context)
                            if alt_result is not None:
                                return alt_result, True, f"Executed alternative tool: {alt_tool}"
                        except Exception as e:
                            logger.warning(f"Alternative tool {alt_tool} failed: {e}")
                            continue
                
                elif strategy.strategy_type == "graceful_degradation":
                    return strategy.degradation_message, False, "Graceful degradation applied"
                
            except Exception as e:
                logger.error(f"Strategy {strategy.strategy_type} failed: {e}")
                continue
        
        return None, False, "All fallback strategies failed"
    
    async def _execute_with_retry(self, tool_function, params: Dict[str, Any], 
                                strategy: FallbackStrategy) -> Any:
        """Execute tool with retry logic."""
        last_exception = None
        
        for attempt in range(strategy.max_attempts):
            try:
                if attempt > 0:
                    await asyncio.sleep(strategy.delay_seconds * attempt)
                
                result = await tool_function(**params)
                return result
                
            except Exception as e:
                last_exception = e
                logger.warning(f"Tool execution attempt {attempt + 1} failed: {e}")
        
        raise last_exception
    
    async def _execute_alternative_tool(self, alt_tool: str, params: Dict[str, Any], 
                                       context: Dict[str, Any]) -> Any:
        """Execute alternative tool (placeholder implementation)."""
        # This would need to be implemented based on your specific tool structure
        # For now, return a placeholder response
        return f"Alternative tool {alt_tool} would be executed here"
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """Get statistics about tool executions."""
        if not self.execution_history:
            return {"total_executions": 0}
        
        successful = len([h for h in self.execution_history if h.get("success", False)])
        total = len(self.execution_history)
        
        return {
            "total_executions": total,
            "successful_executions": successful,
            "success_rate": successful / total if total > 0 else 0.0,
            "average_execution_time": sum(h.get("execution_time", 0) for h in self.execution_history) / total if total > 0 else 0.0
        }
    
    def log_execution(self, tool_name: str, success: bool, execution_time: float, 
                     error: str = None, metadata: Dict[str, Any] = None):
        """Log tool execution for monitoring."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "tool_name": tool_name,
            "success": success,
            "execution_time": execution_time,
            "error": error,
            "metadata": metadata or {}
        }
        
        self.execution_history.append(log_entry)
        logger.info(f"Tool execution logged: {tool_name} - {'success' if success else 'failed'}")


class ToolExecutionMonitor:
    """
    Monitor tool execution performance and health.
    
    This class provides monitoring capabilities for:
    1. Execution time tracking
    2. Success rate monitoring
    3. Error pattern detection
    4. Performance alerts
    """
    
    def __init__(self):
        self.metrics: Dict[str, List[Dict[str, Any]]] = {}
        self.alerts: List[Dict[str, Any]] = []
        self.performance_thresholds = {
            "max_execution_time": 60.0,  # seconds
            "min_success_rate": 0.8,    # 80%
            "max_error_rate": 0.2       # 20%
        }
    
    def record_execution(self, tool_name: str, success: bool, execution_time: float, 
                        error: str = None):
        """Record tool execution metrics."""
        if tool_name not in self.metrics:
            self.metrics[tool_name] = []
        
        self.metrics[tool_name].append({
            "timestamp": datetime.now(),
            "success": success,
            "execution_time": execution_time,
            "error": error
        })
        
        # Keep only last 100 executions per tool
        if len(self.metrics[tool_name]) > 100:
            self.metrics[tool_name] = self.metrics[tool_name][-100:]
        
        # Check for performance issues
        self._check_performance_alerts(tool_name)
    
    def _check_performance_alerts(self, tool_name: str):
        """Check for performance issues and generate alerts."""
        tool_metrics = self.metrics.get(tool_name, [])
        if len(tool_metrics) < 5:  # Need minimum data points
            return
        
        recent_metrics = tool_metrics[-10:]  # Last 10 executions
        
        # Check execution time
        avg_time = sum(m["execution_time"] for m in recent_metrics) / len(recent_metrics)
        if avg_time > self.performance_thresholds["max_execution_time"]:
            self._create_alert(tool_name, "slow_execution", 
                             f"Average execution time {avg_time:.2f}s exceeds threshold")
        
        # Check success rate
        success_count = sum(1 for m in recent_metrics if m["success"])
        success_rate = success_count / len(recent_metrics)
        if success_rate < self.performance_thresholds["min_success_rate"]:
            self._create_alert(tool_name, "low_success_rate", 
                             f"Success rate {success_rate:.2%} below threshold")
    
    def _create_alert(self, tool_name: str, alert_type: str, message: str):
        """Create a performance alert."""
        alert = {
            "timestamp": datetime.now().isoformat(),
            "tool_name": tool_name,
            "alert_type": alert_type,
            "message": message,
            "severity": "warning"
        }
        
        self.alerts.append(alert)
        logger.warning(f"Performance alert for {tool_name}: {message}")
    
    def get_tool_health(self, tool_name: str) -> Dict[str, Any]:
        """Get health status for a specific tool."""
        tool_metrics = self.metrics.get(tool_name, [])
        if not tool_metrics:
            return {"status": "no_data", "message": "No execution data available"}
        
        recent_metrics = tool_metrics[-20:]  # Last 20 executions
        
        success_count = sum(1 for m in recent_metrics if m["success"])
        success_rate = success_count / len(recent_metrics)
        avg_time = sum(m["execution_time"] for m in recent_metrics) / len(recent_metrics)
        
        # Determine health status
        if success_rate >= 0.9 and avg_time < 30:
            status = "healthy"
        elif success_rate >= 0.7 and avg_time < 60:
            status = "degraded"
        else:
            status = "unhealthy"
        
        return {
            "status": status,
            "success_rate": success_rate,
            "average_execution_time": avg_time,
            "total_executions": len(tool_metrics),
            "recent_errors": [m["error"] for m in recent_metrics if not m["success"] and m["error"]]
        }
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health."""
        all_tools = list(self.metrics.keys())
        if not all_tools:
            return {"status": "no_data", "message": "No tool execution data available"}
        
        tool_healths = {tool: self.get_tool_health(tool) for tool in all_tools}
        
        healthy_tools = sum(1 for health in tool_healths.values() if health["status"] == "healthy")
        total_tools = len(all_tools)
        
        overall_status = "healthy" if healthy_tools == total_tools else "degraded"
        
        return {
            "status": overall_status,
            "total_tools": total_tools,
            "healthy_tools": healthy_tools,
            "tool_healths": tool_healths,
            "recent_alerts": self.alerts[-10:]  # Last 10 alerts
        }
