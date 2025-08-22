"""
Simulation Module - Core Virtual Patient Simulation Engine

This module contains the core simulation components for SmartDoc:
- State management for patient sessions
- Simulation engine orchestration
- Bias detection and analysis
- Session tracking and logging
"""

# Import all simulation components
from .engine import IntentDrivenDisclosureManager
from .bias_analyzer import BiasEvaluator
from .session_logger import SessionLogger, InMemorySessionLogger
from .disclosure_store import ProgressiveDisclosureStore

# Legacy imports for backward compatibility
from .session_tracker import SessionLogger as LegacySessionLogger
from .state_manager import ProgressiveDisclosureManager as LegacyProgressiveDisclosureManager

__all__ = [
    "IntentDrivenDisclosureManager",
    "BiasEvaluator",
    "SessionLogger",
    "InMemorySessionLogger", 
    "ProgressiveDisclosureStore",
    # Legacy exports
    "LegacySessionLogger",
    "LegacyProgressiveDisclosureManager",
]

# Convenience aliases (updated to point to new implementations)
BiasAnalyzer = BiasEvaluator
SessionTracker = SessionLogger  # Now points to new interface
StateManager = ProgressiveDisclosureStore  # Now points to new store

# Legacy aliases for backward compatibility
ProgressiveDisclosureManager = LegacyProgressiveDisclosureManager
