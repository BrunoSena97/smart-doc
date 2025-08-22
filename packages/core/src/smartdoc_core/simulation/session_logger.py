"""
Session Logger for SmartDoc Virtual Patient Simulation

This module provides an abstract session logger interface and default implementation
for tracking clinical simulation sessions without global state. Uses dependency
injection for clean testing and configurability.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, List, Optional
from smartdoc_core.utils.logger import sys_logger
from smartdoc_core.simulation.types import SessionInteraction


class SessionLogger(ABC):
    """Abstract session logger used by the engine (dependency injection)."""

    @abstractmethod
    def log_interaction(
        self, 
        *, 
        intent_id: str, 
        user_query: str, 
        vsp_response: str,
        nlu_output: Optional[Dict] = None, 
        dialogue_state: Optional[str] = None
    ) -> None:
        """Log a single interaction between user and VSP."""
        pass

    @abstractmethod
    def log_bias_warning(self, bias_event: Dict[str, Any]) -> None:
        """Log a bias warning event."""
        pass

    @abstractmethod
    def get_interactions(self) -> List[Dict[str, Any]]:
        """Get all interactions for bias analysis."""
        pass

    @abstractmethod
    def get_bias_summary(self) -> Dict[str, Any]:
        """Get summary of all bias warnings in this session."""
        pass

    @abstractmethod
    def get_session_summary(self) -> Dict[str, Any]:
        """Get comprehensive session summary."""
        pass

    @abstractmethod
    def export(self) -> Dict[str, Any]:
        """Export complete session data."""
        pass


class InMemorySessionLogger(SessionLogger):
    """Default, dependency-injectable implementation (no globals)."""

    def __init__(self, session_id: str):
        """Initialize session logger for specific session."""
        self.session_id = session_id
        self._data = {
            "session_id": session_id,
            "start_time": datetime.now().isoformat(),
            "interactions": [],
            "detected_biases": [],
            "bias_warnings": [],
            "current_state": "INTRODUCTION",
        }
        sys_logger.log_system("info", f"Started new session logger: {session_id}")

    def log_interaction(
        self, 
        *, 
        intent_id: str, 
        user_query: str, 
        vsp_response: str,
        nlu_output: Optional[Dict] = None, 
        dialogue_state: Optional[str] = None
    ) -> None:
        """Log a single interaction between user and VSP."""
        interaction = {
            "intent_id": intent_id,
            "user_query": user_query,
            "vsp_response": vsp_response,
            "timestamp": datetime.now().isoformat(),
            "nlu_output": nlu_output or {},
            "dialogue_state": dialogue_state or "UNKNOWN",
        }

        self._data["interactions"].append(interaction)

        # Update current state
        if dialogue_state:
            self._data["current_state"] = dialogue_state

        sys_logger.log_system(
            "debug", f"Logged interaction: {intent_id} in state {dialogue_state}"
        )

    def log_bias_warning(self, bias_event: Dict[str, Any]) -> None:
        """Log a bias warning event."""
        bias_warning = {
            "bias_type": bias_event.get("bias_type"),
            "message": bias_event.get("message"),
            "confidence": bias_event.get("confidence", 0.5),
            "timestamp": datetime.now().isoformat(),
        }
        self._data["bias_warnings"].append(bias_warning)
        sys_logger.log_system(
            "warning",
            f"BIAS WARNING: {bias_event.get('bias_type')} - {bias_event.get('message')}",
        )

    def get_interactions(self) -> List[Dict[str, Any]]:
        """Get all interactions for bias analysis."""
        return self._data["interactions"]

    def get_bias_summary(self) -> Dict[str, Any]:
        """Get summary of all bias warnings in this session."""
        warnings = self._data["bias_warnings"]
        bias_types: Dict[str, int] = {}
        for warning in warnings:
            bias_type = warning.get("bias_type", "unknown")
            bias_types[bias_type] = bias_types.get(bias_type, 0) + 1

        return {
            "total_warnings": len(warnings),
            "bias_types": bias_types,
            "warnings": warnings,
        }

    def get_session_summary(self) -> Dict[str, Any]:
        """Get comprehensive session summary."""
        start = datetime.fromisoformat(self._data["start_time"])
        duration_minutes = round((datetime.now() - start).total_seconds() / 60, 1)
        
        return {
            "session_id": self.session_id,
            "duration_minutes": duration_minutes,
            "total_interactions": len(self._data["interactions"]),
            "current_state": self._data["current_state"],
            "bias_summary": self.get_bias_summary(),
        }

    def export(self) -> Dict[str, Any]:
        """Export complete session data."""
        return dict(self._data)

    def get_session_duration_minutes(self) -> float:
        """Get session duration in minutes as a float."""
        start = datetime.fromisoformat(self._data["start_time"])
        duration = (datetime.now() - start).total_seconds() / 60
        return round(duration, 1)


# Factory function for creating session loggers
def create_session_logger(session_id: str) -> SessionLogger:
    """Factory function for creating session loggers."""
    return InMemorySessionLogger(session_id)
