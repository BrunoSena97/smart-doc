"""
SmartDoc Core Package

Core AI and domain logic for the SmartDoc virtual patient simulation system.
Provides intent classification, discovery processing, clinical evaluation,
and simulation engines.
"""

__version__ = "0.1.0"

# Public API exports
from .intent import IntentClassifier
from .discovery import DiscoveryProcessor
from .clinical import ClinicalEvaluator
from .simulation import (
    IntentDrivenDisclosureManager,
    BiasEvaluator,
    SessionLogger,
    ProgressiveDisclosureStore,
    # Convenience aliases
    BiasAnalyzer,
    SessionTracker,
    StateManager,
)


def reply_to(message: str) -> str:
    """
    Simple API entry point for SmartDoc AI pipeline.

    TODO: Implement full pipeline:
    - Intent classification
    - Discovery processing
    - Clinical evaluation
    - Bias detection
    - Response generation

    Args:
        message: User input message

    Returns:
        AI-generated response
    """
    # Placeholder implementation
    return f"SmartDoc AI: Analyzing your question: '{message}' - Full AI pipeline coming soon!"


__all__ = [
    "reply_to",
    "IntentClassifier",
    "DiscoveryProcessor",
    "ClinicalEvaluator",
    "IntentDrivenDisclosureManager",
    "ProgressiveDisclosureStore",
    "BiasAnalyzer",
    "SessionTracker",
    "StateManager",
]
