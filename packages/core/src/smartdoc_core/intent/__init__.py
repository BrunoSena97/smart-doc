"""
Intent Classification Module

Provides LLM-based intent classification for clinical queries.
"""

from .classifier import LLMIntentClassifier

__all__ = ["LLMIntentClassifier"]

# Convenience alias
IntentClassifier = LLMIntentClassifier
