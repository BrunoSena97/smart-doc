#!/usr/bin/env python3
"""
Ollama LLM Provider Implementation

Provides integration with Ollama for local LLM inference.
"""

import requests
from typing import Optional
from .base import LLMProvider


class OllamaProvider(LLMProvider):
    """
    Ollama LLM provider for local model inference.

    Connects to a local Ollama instance to generate text using
    various open-source models like Llama, Gemma, etc.
    """

    def __init__(self, base_url: str, model: str):
        """
        Initialize the Ollama provider.

        Args:
            base_url: URL of the Ollama API server
            model: Name of the model to use (e.g., "gemma3:4b-it-q4_K_M")
        """
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.1,
        top_p: float = 0.9,
        timeout_s: int = 30
    ) -> str:
        """
        Generate text using Ollama API.

        Args:
            prompt: Input prompt for the model
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            timeout_s: Request timeout in seconds

        Returns:
            Generated text response

        Raises:
            requests.HTTPError: If the API request fails
            requests.Timeout: If the request times out
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "top_p": top_p
            },
        }

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=timeout_s
        )
        response.raise_for_status()

        data = response.json()
        return data.get("response", "")
