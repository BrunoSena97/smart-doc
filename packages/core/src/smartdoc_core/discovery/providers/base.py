"""
Base provider interface for LLM services

Defines the abstract interface that all LLM providers must implement.
"""

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.1,
        top_p: float = 0.9,
        timeout_s: int = 30
    ) -> str:
        """
        Generate text completion from the LLM.

        Args:
            prompt: The input prompt text
            temperature: Sampling temperature (0.0 to 1.0)
            top_p: Nucleus sampling parameter
            timeout_s: Request timeout in seconds

        Returns:
            Generated text response

        Raises:
            Exception: If the generation fails
        """
        pass
