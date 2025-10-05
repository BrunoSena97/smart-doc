"""
Ollama LLM Provider

Implements the LLM provider interface for Ollama local models.
"""

import requests
from .base import LLMProvider


class OllamaProvider(LLMProvider):
    """Ollama LLM provider implementation."""

    def __init__(self, base_url: str, model: str):
        """
        Initialize Ollama provider.

        Args:
            base_url: Ollama API base URL
            model: Model name to use
        """
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.1,
        top_p: float = 0.9,
        timeout_s: int = 120
    ) -> str:
        """Generate text using Ollama API."""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "top_p": top_p
            }
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            headers=headers,
            timeout=timeout_s
        )

        response.raise_for_status()
        return response.json().get("response", "")
