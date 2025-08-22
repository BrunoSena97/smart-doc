#!/usr/bin/env python3
"""
Base LLM Provider Interface

Defines the contract for LLM providers that can be used across
discovery, intent classification, and other AI-powered features.
"""

from abc import ABC, abstractmethod
from typing import Optional


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.

    Allows for different LLM services (Ollama, OpenAI, Claude, etc.)
    to be used interchangeably across SmartDoc components.
    """

    model: Optional[str] = None

    @abstractmethod
    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.1,
        top_p: float = 0.9,
        timeout_s: int = 30,
    ) -> str:
        """
        Generate text from the LLM.

        Args:
            prompt: The input prompt for the LLM
            temperature: Sampling temperature (0.0 = deterministic, 1.0 = creative)
            top_p: Nucleus sampling parameter
            timeout_s: Timeout in seconds for the request

        Returns:
            Generated text response from the LLM

        Raises:
            Exception: If the LLM request fails
        """
        pass
