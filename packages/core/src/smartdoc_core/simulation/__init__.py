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
from .session_tracker import SessionLogger
from .state_manager import ProgressiveDisclosureManager

__all__ = [
    "IntentDrivenDisclosureManager",
    "BiasEvaluator",
    "SessionLogger",
    "ProgressiveDisclosureManager",
]

# Convenience aliases
BiasAnalyzer = BiasEvaluator
SessionTracker = SessionLogger
StateManager = ProgressiveDisclosureManager
