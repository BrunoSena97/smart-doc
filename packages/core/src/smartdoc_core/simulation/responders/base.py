"""
Base responder interface for simulation engine responses.

Provides abstract interface and shared helpers for different persona/context responders
in the SmartDoc simulation engine.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from smartdoc_core.llm.providers.base import LLMProvider


class Responder(ABC):
    """
    Abstract base class for simulation responders.

    Each responder handles a specific context (anamnesis, labs, exam) and persona,
    using dependency injection for LLM providers and prompts.
    """

    def __init__(self, provider: Optional[LLMProvider] = None):
        """
        Initialize responder with optional LLM provider.

        Args:
            provider: LLM provider instance for generating responses
        """
        self.provider = provider

    @abstractmethod
    def build_prompt(
        self,
        *,
        intent_id: str,
        doctor_question: str,
        clinical_data: List[Dict],
        context: str
    ) -> str:
        """
        Build the prompt for LLM generation.

        Args:
            intent_id: The classified intent ID
            doctor_question: The doctor's original question
            clinical_data: List of clinical data dictionaries with label, summary, content
            context: The clinical context (anamnesis, exam, labs)

        Returns:
            Formatted prompt string for LLM
        """
        pass

    def respond(
        self,
        *,
        intent_id: str,
        doctor_question: str,
        clinical_data: List[Dict],
        context: str
    ) -> str:
        """
        Generate a response using the LLM provider.

        Args:
            intent_id: The classified intent ID
            doctor_question: The doctor's original question
            clinical_data: List of clinical data dictionaries
            context: The clinical context

        Returns:
            Generated response text
        """
        prompt = self.build_prompt(
            intent_id=intent_id,
            doctor_question=doctor_question,
            clinical_data=clinical_data,
            context=context
        )

        if not self.provider:
            return self._fallback()

        # Use provider with appropriate generation parameters
        text = self.provider.generate(prompt)

        # Clean up the response by removing quotes and extra whitespace
        text = text.strip()

        # Remove surrounding quotes if present
        if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
            text = text[1:-1]

        # Remove any remaining leading/trailing quotes that might appear
        text = text.strip().strip('"').strip("'")

        return text

    def _fallback(self) -> str:
        """Default fallback response when no provider is available."""
        return "Let me tell you what I know about that."
