"""
Decision Monitoring and Analytics.

This module provides comprehensive monitoring, logging, and analytics
for the tool decision mechanism.
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import asyncio

logger = logging.getLogger(__name__)


@dataclass
class DecisionMetrics:
    """Metrics for decision monitoring."""
    total_decisions: int = 0
    tool_calls: int = 0
    no_tool_calls: int = 0
    clarification_requests: int = 0
    declined_requests: int = 0
    average_confidence: float = 0.0
    success_rate: float = 0.0
    error_rate: float = 0.0


@dataclass
class PerformanceMetrics:
    """Performance metrics for tool execution."""
    average_execution_time: float = 0.0
    max_execution_time: float = 0.0
    min_execution_time: float = 0.0
    total_executions: int = 0
    successful_executions: int = 0
    failed_executions: int = 0


class DecisionMonitor:
    """
    Comprehensive monitoring system for tool decision making.
    
    This class provides:
    1. Real-time decision tracking
    2. Performance analytics
    3. Error pattern detection
    4. User behavior analysis
    5. System health monitoring
    """
    
    def __init__(self):
        self.decisions: List[Dict[str, Any]] = []
        self.tool_executions: List[Dict[str, Any]] = []
        self.user_sessions: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.error_patterns: Dict[str, int] = defaultdict(int)
        self.performance_alerts: List[Dict[str, Any]] = []
        
        # Analytics cache
        self._metrics_cache: Optional[Dict[str, Any]] = None
        self._cache_timestamp: Optional[datetime] = None
        self._cache_ttl = timedelta(minutes=5)  # Cache TTL
    
    def log_decision(self, decision_data: Dict[str, Any]):
        """Log a decision event."""
        decision_data["timestamp"] = datetime.now().isoformat()
        decision_data["id"] = f"decision_{len(self.decisions)}_{int(datetime.now().timestamp())}"
        
        self.decisions.append(decision_data)
        
        # Update user session
        session_id = decision_data.get("session_id", "anonymous")
        self.user_sessions[session_id].append(decision_data)
        
        # Log to file
        logger.info(f"Decision logged: {decision_data.get('decision')} - {decision_data.get('reasoning', '')}")
        
        # Invalidate cache
        self._metrics_cache = None
    
    def log_tool_execution(self, execution_data: Dict[str, Any]):
        """Log a tool execution event."""
        execution_data["timestamp"] = datetime.now().isoformat()
        execution_data["id"] = f"execution_{len(self.tool_executions)}_{int(datetime.now().timestamp())}"
        
        self.tool_executions.append(execution_data)
        
        # Track error patterns
        if not execution_data.get("success", True):
            error_type = execution_data.get("error_type", "unknown")
            self.error_patterns[error_type] += 1
        
        # Log to file
        status = "success" if execution_data.get("success", True) else "failed"
        logger.info(f"Tool execution logged: {execution_data.get('tool_name')} - {status}")
        
        # Invalidate cache
        self._metrics_cache = None
    
    def get_decision_metrics(self, time_window: Optional[timedelta] = None) -> DecisionMetrics:
        """Get decision metrics for a time window."""
        if time_window:
            cutoff = datetime.now() - time_window
            recent_decisions = [
                d for d in self.decisions 
                if datetime.fromisoformat(d["timestamp"]) >= cutoff
            ]
        else:
            recent_decisions = self.decisions
        
        if not recent_decisions:
            return DecisionMetrics()
        
        # Calculate metrics
        total_decisions = len(recent_decisions)
        decision_types = Counter(d.get("decision", "unknown") for d in recent_decisions)
        
        tool_calls = decision_types.get("call_tool", 0)
        no_tool_calls = decision_types.get("no_tool", 0)
        clarification_requests = decision_types.get("clarify_intent", 0)
        declined_requests = decision_types.get("decline_request", 0)
        
        # Calculate confidence
        confidences = [d.get("confidence", 0.0) for d in recent_decisions if d.get("confidence") is not None]
        average_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        # Calculate success rate
        successful_tools = len([d for d in recent_decisions if d.get("success", False)])
        success_rate = successful_tools / total_decisions if total_decisions > 0 else 0.0
        
        # Calculate error rate
        errors = len([d for d in recent_decisions if d.get("error")])
        error_rate = errors / total_decisions if total_decisions > 0 else 0.0
        
        return DecisionMetrics(
            total_decisions=total_decisions,
            tool_calls=tool_calls,
            no_tool_calls=no_tool_calls,
            clarification_requests=clarification_requests,
            declined_requests=declined_requests,
            average_confidence=average_confidence,
            success_rate=success_rate,
            error_rate=error_rate
        )
    
    def get_performance_metrics(self, time_window: Optional[timedelta] = None) -> PerformanceMetrics:
        """Get performance metrics for tool execution."""
        if time_window:
            cutoff = datetime.now() - time_window
            recent_executions = [
                e for e in self.tool_executions 
                if datetime.fromisoformat(e["timestamp"]) >= cutoff
            ]
        else:
            recent_executions = self.tool_executions
        
        if not recent_executions:
            return PerformanceMetrics()
        
        # Calculate execution times
        execution_times = [e.get("execution_time", 0.0) for e in recent_executions if e.get("execution_time") is not None]
        
        average_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0.0
        max_execution_time = max(execution_times) if execution_times else 0.0
        min_execution_time = min(execution_times) if execution_times else 0.0
        
        # Calculate success/failure rates
        total_executions = len(recent_executions)
        successful_executions = len([e for e in recent_executions if e.get("success", False)])
        failed_executions = total_executions - successful_executions
        
        return PerformanceMetrics(
            average_execution_time=average_execution_time,
            max_execution_time=max_execution_time,
            min_execution_time=min_execution_time,
            total_executions=total_executions,
            successful_executions=successful_executions,
            failed_executions=failed_executions
        )
    
    def get_user_behavior_analysis(self, session_id: str) -> Dict[str, Any]:
        """Analyze user behavior for a specific session."""
        session_data = self.user_sessions.get(session_id, [])
        if not session_data:
            return {"error": "No session data found"}
        
        # Analyze decision patterns
        decisions = [d.get("decision") for d in session_data]
        decision_counts = Counter(decisions)
        
        # Analyze tool usage
        tool_usage = [d.get("recommended_tools", []) for d in session_data if d.get("recommended_tools")]
        all_tools = [tool for tools in tool_usage for tool in tools]
        tool_counts = Counter(all_tools)
        
        # Analyze confidence trends
        confidences = [d.get("confidence", 0.0) for d in session_data if d.get("confidence") is not None]
        confidence_trend = "increasing" if len(confidences) > 1 and confidences[-1] > confidences[0] else "stable"
        
        return {
            "session_id": session_id,
            "total_interactions": len(session_data),
            "decision_distribution": dict(decision_counts),
            "tool_usage": dict(tool_counts),
            "confidence_trend": confidence_trend,
            "average_confidence": sum(confidences) / len(confidences) if confidences else 0.0,
            "session_duration": self._calculate_session_duration(session_data)
        }
    
    def _calculate_session_duration(self, session_data: List[Dict[str, Any]]) -> float:
        """Calculate session duration in minutes."""
        if len(session_data) < 2:
            return 0.0
        
        timestamps = [datetime.fromisoformat(d["timestamp"]) for d in session_data]
        duration = max(timestamps) - min(timestamps)
        return duration.total_seconds() / 60.0
    
    def get_error_analysis(self) -> Dict[str, Any]:
        """Analyze error patterns and trends."""
        if not self.error_patterns:
            return {"error": "No error data available"}
        
        # Get most common errors
        most_common_errors = Counter(self.error_patterns).most_common(5)
        
        # Analyze error trends over time
        recent_errors = [
            e for e in self.tool_executions 
            if not e.get("success", True) and 
            datetime.fromisoformat(e["timestamp"]) >= datetime.now() - timedelta(hours=24)
        ]
        
        error_trend = "increasing" if len(recent_errors) > 5 else "stable"
        
        return {
            "most_common_errors": most_common_errors,
            "total_error_types": len(self.error_patterns),
            "recent_error_count": len(recent_errors),
            "error_trend": error_trend,
            "error_rate_24h": len(recent_errors) / max(1, len(self.tool_executions)) * 100
        }
    
    def get_system_health_report(self) -> Dict[str, Any]:
        """Generate comprehensive system health report."""
        # Get cached metrics or calculate new ones
        if self._metrics_cache and self._cache_timestamp and \
           datetime.now() - self._cache_timestamp < self._cache_ttl:
            return self._metrics_cache
        
        # Calculate fresh metrics
        decision_metrics = self.get_decision_metrics()
        performance_metrics = self.get_performance_metrics()
        error_analysis = self.get_error_analysis()
        
        # Determine overall health status
        health_score = self._calculate_health_score(decision_metrics, performance_metrics)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(decision_metrics, performance_metrics, error_analysis)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "health_score": health_score,
            "status": "healthy" if health_score > 0.8 else "degraded" if health_score > 0.5 else "unhealthy",
            "decision_metrics": asdict(decision_metrics),
            "performance_metrics": asdict(performance_metrics),
            "error_analysis": error_analysis,
            "recommendations": recommendations,
            "active_sessions": len(self.user_sessions),
            "total_decisions": len(self.decisions),
            "total_executions": len(self.tool_executions)
        }
        
        # Cache the report
        self._metrics_cache = report
        self._cache_timestamp = datetime.now()
        
        return report
    
    def _calculate_health_score(self, decision_metrics: DecisionMetrics, 
                               performance_metrics: PerformanceMetrics) -> float:
        """Calculate overall health score (0.0-1.0)."""
        # Decision success rate (40% weight)
        decision_score = decision_metrics.success_rate * 0.4
        
        # Performance score (30% weight)
        performance_score = min(1.0, performance_metrics.successful_executions / 
                              max(1, performance_metrics.total_executions)) * 0.3
        
        # Error rate penalty (20% weight)
        error_penalty = max(0.0, 1.0 - decision_metrics.error_rate) * 0.2
        
        # Execution time score (10% weight)
        time_score = max(0.0, 1.0 - (performance_metrics.average_execution_time / 60.0)) * 0.1
        
        return min(1.0, decision_score + performance_score + error_penalty + time_score)
    
    def _generate_recommendations(self, decision_metrics: DecisionMetrics,
                                performance_metrics: PerformanceMetrics,
                                error_analysis: Dict[str, Any]) -> List[str]:
        """Generate system improvement recommendations."""
        recommendations = []
        
        # Decision-related recommendations
        if decision_metrics.clarification_requests > decision_metrics.total_decisions * 0.3:
            recommendations.append("Consider improving intent detection to reduce clarification requests")
        
        if decision_metrics.declined_requests > decision_metrics.total_decisions * 0.2:
            recommendations.append("Review request filtering criteria to reduce declined requests")
        
        # Performance-related recommendations
        if performance_metrics.average_execution_time > 30.0:
            recommendations.append("Tool execution times are high - consider optimization or caching")
        
        if performance_metrics.failed_executions > performance_metrics.total_executions * 0.2:
            recommendations.append("High failure rate detected - review error handling and fallback mechanisms")
        
        # Error-related recommendations
        if error_analysis.get("error_rate_24h", 0) > 10:
            recommendations.append("Error rate is elevated - investigate recent changes or system issues")
        
        if not recommendations:
            recommendations.append("System is performing well - continue monitoring")
        
        return recommendations
    
    def export_analytics(self, format: str = "json") -> str:
        """Export analytics data in specified format."""
        report = self.get_system_health_report()
        
        if format == "json":
            return json.dumps(report, indent=2, default=str)
        elif format == "csv":
            # Simple CSV export for key metrics
            lines = [
                "metric,value",
                f"health_score,{report['health_score']}",
                f"total_decisions,{report['total_decisions']}",
                f"total_executions,{report['total_executions']}",
                f"active_sessions,{report['active_sessions']}"
            ]
            return "\n".join(lines)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def cleanup_old_data(self, retention_days: int = 30):
        """Clean up old data to prevent memory issues."""
        cutoff = datetime.now() - timedelta(days=retention_days)
        
        # Clean up decisions
        self.decisions = [
            d for d in self.decisions 
            if datetime.fromisoformat(d["timestamp"]) >= cutoff
        ]
        
        # Clean up tool executions
        self.tool_executions = [
            e for e in self.tool_executions 
            if datetime.fromisoformat(e["timestamp"]) >= cutoff
        ]
        
        # Clean up user sessions
        for session_id in list(self.user_sessions.keys()):
            self.user_sessions[session_id] = [
                d for d in self.user_sessions[session_id]
                if datetime.fromisoformat(d["timestamp"]) >= cutoff
            ]
            if not self.user_sessions[session_id]:
                del self.user_sessions[session_id]
        
        logger.info(f"Cleaned up data older than {retention_days} days")
    
    async def start_monitoring(self, interval_seconds: int = 300):
        """Start background monitoring task."""
        while True:
            try:
                # Generate health report
                report = self.get_system_health_report()
                
                # Check for alerts
                if report["health_score"] < 0.5:
                    logger.warning(f"System health degraded: {report['health_score']}")
                
                # Clean up old data
                self.cleanup_old_data()
                
                await asyncio.sleep(interval_seconds)
                
            except Exception as e:
                logger.error(f"Monitoring task error: {e}")
                await asyncio.sleep(60)  # Wait before retrying


# Global monitoring instance
monitor = DecisionMonitor()
