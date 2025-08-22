#!/usr/bin/env python3
"""
Base Interface for Intent Classification Prompt Builders

Defines the contract for creating prompts for LLM intent classification
with support for general and context-aware classification.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class IntentPromptBuilder(ABC):
    """
    Abstract base class for building intent classification prompts.

    Allows for different prompt strategies and future admin-configurable
    prompt templates per agent or clinical phase.
    """

    @abstractmethod
    def build_general(
        self,
        *,
        doctor_input: str,
        intent_categories: Dict[str, Dict[str, Any]]
    ) -> str:
        """
        Build a general intent classification prompt.

        Args:
            doctor_input: The doctor's question or statement
            intent_categories: Dictionary of available intent categories

        Returns:
            Formatted prompt string for the LLM
        """
        pass

    @abstractmethod
    def build_context_aware(
        self,
        *,
        doctor_input: str,
        context: str,
        filtered_intents: Dict[str, Dict[str, Any]]
    ) -> str:
        """
        Build a context-aware intent classification prompt.

        Args:
            doctor_input: The doctor's question or statement
            context: Clinical context (anamnesis, exam, labs)
            filtered_intents: Dictionary of intents valid for this context

        Returns:
            Formatted prompt string for the LLM
        """
        pass
