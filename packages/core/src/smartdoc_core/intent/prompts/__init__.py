#!/usr/bin/env python3
"""
Intent Classification Prompt Builders

Provides different strategies for building prompts for LLM intent classification.
"""

from .base import IntentPromptBuilder
from .default import DefaultIntentPrompt

__all__ = [
    "IntentPromptBuilder",
    "DefaultIntentPrompt",
]
