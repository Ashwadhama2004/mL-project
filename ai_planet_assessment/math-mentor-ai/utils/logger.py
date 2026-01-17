"""
Agent Logger for Math Mentor AI

This module provides structured logging for agent execution traces,
enabling transparency and debugging of the multi-agent system.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum
import threading


class AgentStatus(Enum):
    """Status of agent execution."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    HITL_REQUIRED = "hitl_required"


@dataclass
class AgentLogEntry:
    """A single log entry for an agent."""
    timestamp: str
    agent_name: str
    status: AgentStatus
    message: str
    input_data: Optional[Dict] = None
    output_data: Optional[Dict] = None
    duration_ms: Optional[float] = None
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            "timestamp": self.timestamp,
            "agent_name": self.agent_name,
            "status": self.status.value,
            "message": self.message,
        }
        if self.input_data:
            result["input_data"] = self._truncate_data(self.input_data)
        if self.output_data:
            result["output_data"] = self._truncate_data(self.output_data)
        if self.duration_ms is not None:
            result["duration_ms"] = self.duration_ms
        if self.error:
            result["error"] = self.error
        return result
    
    def _truncate_data(self, data: Dict, max_length: int = 500) -> Dict:
        """Truncate long strings in data for display."""
        result = {}
        for k, v in data.items():
            if isinstance(v, str) and len(v) > max_length:
                result[k] = v[:max_length] + "..."
            elif isinstance(v, dict):
                result[k] = self._truncate_data(v, max_length)
            elif isinstance(v, list) and len(v) > 10:
                result[k] = v[:10] + ["..."]
            else:
                result[k] = v
        return result


@dataclass
class ExecutionTrace:
    """Complete execution trace for a problem-solving session."""
    session_id: str
    start_time: str
    entries: List[AgentLogEntry] = field(default_factory=list)
    end_time: Optional[str] = None
    total_duration_ms: Optional[float] = None
    final_status: str = "in_progress"
    
    def add_entry(self, entry: AgentLogEntry) -> None:
        """Add a log entry to the trace."""
        self.entries.append(entry)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "session_id": self.session_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_duration_ms": self.total_duration_ms,
            "final_status": self.final_status,
            "entries": [e.to_dict() for e in self.entries]
        }
    
    def get_summary(self) -> List[Dict[str, str]]:
        """Get a summary of agent execution for UI display."""
        summary = []
        for entry in self.entries:
            status_icon = {
                AgentStatus.PENDING: "⏳",
                AgentStatus.RUNNING: "🔄",
                AgentStatus.COMPLETED: "✓",
                AgentStatus.FAILED: "✗",
                AgentStatus.HITL_REQUIRED: "⚡"
            }.get(entry.status, "?")
            
            summary.append({
                "agent": entry.agent_name,
                "status": f"{status_icon} {entry.status.value}",
                "message": entry.message,
                "duration": f"{entry.duration_ms:.0f}ms" if entry.duration_ms else ""
            })
        return summary


class AgentLogger:
    """
    Logger for tracking agent execution.
    
    Thread-safe logging for multi-agent systems.
    """
    
    def __init__(self, session_id: str = None):
        """
        Initialize the logger.
        
        Args:
            session_id: Unique identifier for this session
        """
        self.session_id = session_id or datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        self.trace = ExecutionTrace(
            session_id=self.session_id,
            start_time=datetime.now().isoformat()
        )
        self._lock = threading.Lock()
        self._agent_start_times: Dict[str, datetime] = {}
        
        # Also set up Python logging
        self.logger = logging.getLogger(f"MathMentor.{self.session_id}")
        self.logger.setLevel(logging.DEBUG)
    
    def start_agent(
        self,
        agent_name: str,
        input_data: Dict = None,
        message: str = None
    ) -> None:
        """
        Log the start of an agent's execution.
        
        Args:
            agent_name: Name of the agent
            input_data: Input data for the agent
            message: Optional message
        """
        with self._lock:
            now = datetime.now()
            self._agent_start_times[agent_name] = now
            
            entry = AgentLogEntry(
                timestamp=now.isoformat(),
                agent_name=agent_name,
                status=AgentStatus.RUNNING,
                message=message or f"Starting {agent_name}",
                input_data=input_data
            )
            self.trace.add_entry(entry)
            
            self.logger.info(f"[{agent_name}] Started: {message or 'Processing'}")
    
    def complete_agent(
        self,
        agent_name: str,
        output_data: Dict = None,
        message: str = None
    ) -> None:
        """
        Log the successful completion of an agent.
        
        Args:
            agent_name: Name of the agent
            output_data: Output data from the agent
            message: Optional message
        """
        with self._lock:
            now = datetime.now()
            duration = None
            
            if agent_name in self._agent_start_times:
                start = self._agent_start_times.pop(agent_name)
                duration = (now - start).total_seconds() * 1000
            
            entry = AgentLogEntry(
                timestamp=now.isoformat(),
                agent_name=agent_name,
                status=AgentStatus.COMPLETED,
                message=message or f"Completed {agent_name}",
                output_data=output_data,
                duration_ms=duration
            )
            self.trace.add_entry(entry)
            
            self.logger.info(
                f"[{agent_name}] Completed in {duration:.0f}ms: {message or 'Done'}"
            )
    
    def fail_agent(
        self,
        agent_name: str,
        error: str,
        message: str = None
    ) -> None:
        """
        Log a failed agent execution.
        
        Args:
            agent_name: Name of the agent
            error: Error message
            message: Optional message
        """
        with self._lock:
            now = datetime.now()
            duration = None
            
            if agent_name in self._agent_start_times:
                start = self._agent_start_times.pop(agent_name)
                duration = (now - start).total_seconds() * 1000
            
            entry = AgentLogEntry(
                timestamp=now.isoformat(),
                agent_name=agent_name,
                status=AgentStatus.FAILED,
                message=message or f"Failed {agent_name}",
                error=error,
                duration_ms=duration
            )
            self.trace.add_entry(entry)
            
            self.logger.error(f"[{agent_name}] Failed: {error}")
    
    def hitl_required(
        self,
        agent_name: str,
        reason: str,
        question: str = None
    ) -> None:
        """
        Log that HITL intervention is required.
        
        Args:
            agent_name: Name of the agent requesting HITL
            reason: Reason for HITL
            question: Question to ask the user
        """
        with self._lock:
            entry = AgentLogEntry(
                timestamp=datetime.now().isoformat(),
                agent_name=agent_name,
                status=AgentStatus.HITL_REQUIRED,
                message=reason,
                output_data={"hitl_question": question} if question else None
            )
            self.trace.add_entry(entry)
            
            self.logger.warning(f"[{agent_name}] HITL Required: {reason}")
    
    def log_info(self, agent_name: str, message: str, data: Dict = None) -> None:
        """Log an informational message."""
        self.logger.info(f"[{agent_name}] {message}")
    
    def finalize(self, status: str = "completed") -> ExecutionTrace:
        """
        Finalize the execution trace.
        
        Args:
            status: Final status of the session
            
        Returns:
            Complete ExecutionTrace
        """
        with self._lock:
            now = datetime.now()
            self.trace.end_time = now.isoformat()
            self.trace.final_status = status
            
            # Calculate total duration
            start = datetime.fromisoformat(self.trace.start_time)
            self.trace.total_duration_ms = (now - start).total_seconds() * 1000
            
            return self.trace
    
    def get_trace(self) -> ExecutionTrace:
        """Get the current execution trace."""
        return self.trace
    
    def get_summary(self) -> List[Dict[str, str]]:
        """Get a summary for UI display."""
        return self.trace.get_summary()
    
    def to_json(self) -> str:
        """Export trace as JSON."""
        return json.dumps(self.trace.to_dict(), indent=2)


# Thread-local storage for current logger
_current_logger = threading.local()

def get_current_logger() -> Optional[AgentLogger]:
    """Get the current thread's logger."""
    return getattr(_current_logger, 'logger', None)

def set_current_logger(logger: AgentLogger) -> None:
    """Set the current thread's logger."""
    _current_logger.logger = logger

def create_session_logger() -> AgentLogger:
    """Create and set a new session logger."""
    logger = AgentLogger()
    set_current_logger(logger)
    return logger


def main():
    """Test the logger."""
    print("=" * 60)
    print("Math Mentor AI - Agent Logger Test")
    print("=" * 60)
    
    import time
    
    # Create logger
    logger = create_session_logger()
    
    # Simulate agent executions
    agents = ["Parser", "Router", "Solver", "Verifier", "Explainer"]
    
    for agent in agents:
        logger.start_agent(agent, {"problem": "x^2 - 5x + 6 = 0"})
        time.sleep(0.1)  # Simulate work
        
        if agent == "Verifier":
            logger.hitl_required(agent, "Low confidence", "Please verify the solution")
        
        logger.complete_agent(agent, {"result": "success"}, f"{agent} completed successfully")
    
    # Finalize
    trace = logger.finalize("completed")
    
    # Print summary
    print("\nExecution Summary:")
    for item in trace.get_summary():
        print(f"  {item['status']} {item['agent']}: {item['message']} ({item['duration']})")
    
    print(f"\nTotal Duration: {trace.total_duration_ms:.0f}ms")
    print(f"Final Status: {trace.final_status}")


if __name__ == "__main__":
    main()
