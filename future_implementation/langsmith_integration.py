# langsmith_integration.py
"""
Complete LangSmith Integration for Research Brief Generator
Provides comprehensive tracing, monitoring, token tracking, and observability
"""

import os
import time
import json
from datetime import datetime
from typing import Dict, Any, Optional, List
import threading
from dotenv import load_dotenv
load_dotenv()

class ResearchBriefTracer:
    """Enhanced tracing for research brief generation with LangSmith integration"""
    
    def __init__(self):
        self.session_id = None
        self.client = None
        self.setup_langsmith()
        
    def setup_langsmith(self):
        """Initialize LangSmith client with environment variables"""
        langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
        if langsmith_api_key:
            try:
                # Try to import LangSmith client
                try:
                    from langsmith import Client
                    self.client = Client(api_key=langsmith_api_key)
                except ImportError:
                    print("⚠️ LangSmith SDK not installed - using environment variables only")
                
                os.environ["LANGCHAIN_TRACING_V2"] = "true"
                os.environ["LANGCHAIN_API_KEY"] = langsmith_api_key
                os.environ["LANGCHAIN_PROJECT"] = "research-brief-generator"
                print("✅ LangSmith tracing enabled")
            except Exception as e:
                print(f"⚠️ LangSmith setup failed: {e}")
        else:
            print("⚠️ LANGSMITH_API_KEY not found - tracing disabled")
    
    def start_research_session(self, topic: str, user_id: str) -> str:
        """Start a new research session with metadata"""
        self.session_id = f"research_{int(time.time())}_{user_id}"
        
        if self.client:
            try:
                self.client.create_run(
                    name="research_brief_generation",
                    run_type="chain",
                    inputs={"topic": topic, "user_id": user_id},
                    session_name=self.session_id,
                    start_time=datetime.now()
                )
            except Exception as e:
                print(f"LangSmith session start failed: {e}")
        
        return self.session_id
    
    def log_node_execution(self, node_name: str, inputs: Dict, outputs: Dict, 
                          duration: float, tokens_used: int = 0, cost: float = 0.0):
        """Log individual node execution with performance metrics"""
        if self.client and self.session_id:
            try:
                self.client.create_run(
                    name=f"node_{node_name}",
                    run_type="llm" if "llm" in node_name.lower() else "chain",
                    inputs=inputs,
                    outputs=outputs,
                    session_name=self.session_id,
                    extra={
                        "duration_seconds": duration,
                        "tokens_used": tokens_used,
                        "estimated_cost": cost,
                        "node_type": node_name
                    }
                )
            except Exception as e:
                print(f"LangSmith node logging failed: {e}")

class TokenUsageTracker:
    """Track token usage and cost estimation across models"""
    
    def __init__(self):
        self.usage_stats = {
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_cost": 0.0,
            "model_usage": {},
            "node_usage": {},
            "session_history": []
        }
        self.lock = threading.Lock()
        
        # Model pricing (tokens per million - update with actual rates)
        self.model_costs = {
            "grok-4-fast": {"input": 0.0, "output": 0.0},  # Free tier
            "deepseek-chat-v3.1": {"input": 0.0, "output": 0.0},  # Free tier
            "nemotron-nano-9b-v2": {"input": 0.0, "output": 0.0},  # Free tier
            "search_engine": {"input": 0.0, "output": 0.0}  # No cost for search
        }
        
    def track_usage(self, model_name: str, node_name: str, 
                   input_tokens: int, output_tokens: int) -> Dict[str, Any]:
        """Track token usage and calculate costs"""
        with self.lock:
            # Update totals
            self.usage_stats["total_input_tokens"] += input_tokens
            self.usage_stats["total_output_tokens"] += output_tokens
            
            # Update model-specific usage
            if model_name not in self.usage_stats["model_usage"]:
                self.usage_stats["model_usage"][model_name] = {
                    "input_tokens": 0, "output_tokens": 0, "cost": 0.0, "calls": 0
                }
            
            model_stats = self.usage_stats["model_usage"][model_name]
            model_stats["input_tokens"] += input_tokens
            model_stats["output_tokens"] += output_tokens
            model_stats["calls"] += 1
            
            # Calculate cost (currently $0 for free models)
            if model_name in self.model_costs:
                input_cost = (input_tokens / 1_000_000) * self.model_costs[model_name]["input"]
                output_cost = (output_tokens / 1_000_000) * self.model_costs[model_name]["output"]
                total_cost = input_cost + output_cost
                model_stats["cost"] += total_cost
                self.usage_stats["total_cost"] += total_cost
            
            # Update node-specific usage
            if node_name not in self.usage_stats["node_usage"]:
                self.usage_stats["node_usage"][node_name] = {
                    "input_tokens": 0, "output_tokens": 0, "executions": 0, "total_cost": 0.0
                }
            
            node_stats = self.usage_stats["node_usage"][node_name]
            node_stats["input_tokens"] += input_tokens
            node_stats["output_tokens"] += output_tokens
            node_stats["executions"] += 1
            node_stats["total_cost"] += total_cost if 'total_cost' in locals() else 0.0
            
            # Add to session history
            self.usage_stats["session_history"].append({
                "timestamp": datetime.now().isoformat(),
                "model_name": model_name,
                "node_name": node_name,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost": total_cost if 'total_cost' in locals() else 0.0
            })
            
            return self.get_current_stats()
    
    def get_current_stats(self) -> Dict[str, Any]:
        """Get current usage statistics"""
        with self.lock:
            return {
                "timestamp": datetime.now().isoformat(),
                "total_tokens": self.usage_stats["total_input_tokens"] + self.usage_stats["total_output_tokens"],
                "input_tokens": self.usage_stats["total_input_tokens"],
                "output_tokens": self.usage_stats["total_output_tokens"],
                "estimated_cost": self.usage_stats["total_cost"],
                "model_breakdown": dict(self.usage_stats["model_usage"]),
                "node_breakdown": dict(self.usage_stats["node_usage"]),
                "recent_activity": self.usage_stats["session_history"][-10:]  # Last 10 activities
            }
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance and usage report"""
        with self.lock:
            total_calls = sum(model["calls"] for model in self.usage_stats["model_usage"].values())
            avg_tokens_per_call = ((self.usage_stats["total_input_tokens"] + self.usage_stats["total_output_tokens"]) / 
                                 max(total_calls, 1))
            
            return {
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total_tokens": self.usage_stats["total_input_tokens"] + self.usage_stats["total_output_tokens"],
                    "input_tokens": self.usage_stats["total_input_tokens"],
                    "output_tokens": self.usage_stats["total_output_tokens"],
                    "estimated_cost": self.usage_stats["total_cost"],
                    "total_model_calls": total_calls,
                    "average_tokens_per_call": round(avg_tokens_per_call, 2)
                },
                "model_breakdown": dict(self.usage_stats["model_usage"]),
                "node_breakdown": dict(self.usage_stats["node_usage"]),
                "cost_breakdown": {
                    model: stats["cost"] for model, stats in self.usage_stats["model_usage"].items()
                }
            }
    
    def reset_stats(self):
        """Reset usage statistics"""
        with self.lock:
            self.usage_stats = {
                "total_input_tokens": 0,
                "total_output_tokens": 0,
                "total_cost": 0.0,
                "model_usage": {},
                "node_usage": {},
                "session_history": []
            }

class PerformanceMonitor:
    """Monitor and report performance metrics for workflow execution"""
    
    def __init__(self):
        self.metrics = {
            "request_count": 0,
            "total_duration": 0.0,
            "node_durations": {},
            "error_count": 0,
            "success_count": 0,
            "active_requests": {},
            "throughput_history": []
        }
        self.lock = threading.Lock()
    
    def start_request(self) -> str:
        """Start monitoring a request"""
        request_id = f"req_{int(time.time() * 1000)}"
        with self.lock:
            self.metrics["active_requests"][request_id] = {
                "start_time": time.time(),
                "nodes_completed": []
            }
        return request_id
    
    def record_node_performance(self, node_name: str, duration: float, success: bool = True):
        """Record node execution performance"""
        with self.lock:
            if node_name not in self.metrics["node_durations"]:
                self.metrics["node_durations"][node_name] = {
                    "total_time": 0.0,
                    "execution_count": 0,
                    "average_time": 0.0,
                    "min_time": float('inf'),
                    "max_time": 0.0,
                    "success_count": 0,
                    "error_count": 0
                }
            
            node_stats = self.metrics["node_durations"][node_name]
            node_stats["total_time"] += duration
            node_stats["execution_count"] += 1
            node_stats["average_time"] = node_stats["total_time"] / node_stats["execution_count"]
            node_stats["min_time"] = min(node_stats["min_time"], duration)
            node_stats["max_time"] = max(node_stats["max_time"], duration)
            
            if success:
                node_stats["success_count"] += 1
                self.metrics["success_count"] += 1
            else:
                node_stats["error_count"] += 1
                self.metrics["error_count"] += 1
    
    def complete_request(self, request_id: str, total_duration: float, success: bool = True):
        """Complete request monitoring"""
        with self.lock:
            if request_id in self.metrics["active_requests"]:
                del self.metrics["active_requests"][request_id]
            
            self.metrics["request_count"] += 1
            self.metrics["total_duration"] += total_duration
            
            # Track throughput
            current_time = time.time()
            self.metrics["throughput_history"].append({
                "timestamp": current_time,
                "duration": total_duration,
                "success": success
            })
            
            # Keep only last 100 entries for throughput calculation
            if len(self.metrics["throughput_history"]) > 100:
                self.metrics["throughput_history"] = self.metrics["throughput_history"][-100:]
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report"""
        with self.lock:
            avg_request_time = (self.metrics["total_duration"] / self.metrics["request_count"] 
                              if self.metrics["request_count"] > 0 else 0)
            
            success_rate = (self.metrics["success_count"] / 
                           max(self.metrics["request_count"], 1)) * 100
            
            # Calculate recent throughput (last 10 minutes)
            recent_cutoff = time.time() - 600  # 10 minutes
            recent_requests = [req for req in self.metrics["throughput_history"] 
                             if req["timestamp"] > recent_cutoff]
            
            recent_throughput = len(recent_requests) / 10 if recent_requests else 0  # requests per minute
            
            return {
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total_requests": self.metrics["request_count"],
                    "average_request_time": round(avg_request_time, 2),
                    "total_successes": self.metrics["success_count"],
                    "total_errors": self.metrics["error_count"],
                    "success_rate": round(success_rate, 2),
                    "active_requests": len(self.metrics["active_requests"]),
                    "recent_throughput_per_minute": round(recent_throughput, 2)
                },
                "node_performance": {
                    node: {
                        "average_time": round(stats["average_time"], 2),
                        "min_time": round(stats["min_time"], 2) if stats["min_time"] != float('inf') else 0,
                        "max_time": round(stats["max_time"], 2),
                        "execution_count": stats["execution_count"],
                        "success_rate": round((stats["success_count"] / max(stats["execution_count"], 1)) * 100, 2)
                    }
                    for node, stats in self.metrics["node_durations"].items()
                },
                "system_health": {
                    "status": "healthy" if success_rate > 80 else "degraded" if success_rate > 50 else "unhealthy",
                    "avg_response_time": round(avg_request_time, 2),
                    "error_rate": round((self.metrics["error_count"] / max(self.metrics["request_count"], 1)) * 100, 2)
                }
            }
    
    def get_node_benchmark(self, node_name: str) -> Dict[str, Any]:
        """Get detailed benchmark for specific node"""
        with self.lock:
            if node_name not in self.metrics["node_durations"]:
                return {"error": f"No data found for node: {node_name}"}
            
            stats = self.metrics["node_durations"][node_name]
            return {
                "node_name": node_name,
                "performance_metrics": {
                    "total_executions": stats["execution_count"],
                    "average_duration": round(stats["average_time"], 3),
                    "min_duration": round(stats["min_time"], 3) if stats["min_time"] != float('inf') else 0,
                    "max_duration": round(stats["max_time"], 3),
                    "total_time": round(stats["total_time"], 3),
                    "success_rate": round((stats["success_count"] / max(stats["execution_count"], 1)) * 100, 2)
                },
                "benchmarks": {
                    "excellent": "< 5s",
                    "good": "5-15s", 
                    "acceptable": "15-30s",
                    "slow": "> 30s",
                    "current_performance": (
                        "excellent" if stats["average_time"] < 5 else
                        "good" if stats["average_time"] < 15 else
                        "acceptable" if stats["average_time"] < 30 else
                        "slow"
                    )
                }
            }

# Token counting utility
def count_tokens_estimate(text: str) -> int:
    """Estimate token count (rough approximation)"""
    # Simple estimation: ~1.3 tokens per word for most models
    words = len(str(text).split())
    return int(words * 1.3)

def count_tokens_tiktoken(text: str, model_name: str = "gpt-3.5-turbo") -> int:
    """Count tokens accurately using tiktoken (if available)"""
    try:
        import tiktoken
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")  # Use standard encoding
        return len(encoding.encode(str(text)))
    except ImportError:
        # Fallback to estimation
        return count_tokens_estimate(text)
    except Exception:
        # Fallback to estimation  
        return count_tokens_estimate(text)

# Global instances - ready to use
tracer = ResearchBriefTracer()
token_tracker = TokenUsageTracker()
performance_monitor = PerformanceMonitor()

# Utility functions for easy integration
def log_workflow_start(topic: str, user_id: str) -> str:
    """Convenient function to start workflow monitoring"""
    request_id = performance_monitor.start_request()
    session_id = tracer.start_research_session(topic, user_id)
    return request_id

def log_node_execution(node_name: str, duration: float, input_tokens: int, output_tokens: int, 
                      model_name: str = "unknown", success: bool = True):
    """Convenient function to log node execution"""
    # Track performance
    performance_monitor.record_node_performance(node_name, duration, success)
    
    # Track token usage
    if input_tokens > 0 or output_tokens > 0:
        token_tracker.track_usage(model_name, node_name, input_tokens, output_tokens)
    
    # Log to LangSmith
    tracer.log_node_execution(
        node_name, 
        {"input_tokens": input_tokens},
        {"output_tokens": output_tokens, "duration": duration},
        duration, 
        input_tokens + output_tokens
    )

def get_comprehensive_metrics() -> Dict[str, Any]:
    """Get all metrics in one comprehensive report"""
    return {
        "token_usage": token_tracker.get_performance_report(),
        "performance_metrics": performance_monitor.get_performance_report(),
        "system_status": {
            "monitoring_active": True,
            "langsmith_enabled": tracer.client is not None,
            "timestamp": datetime.now().isoformat()
        }
    }
