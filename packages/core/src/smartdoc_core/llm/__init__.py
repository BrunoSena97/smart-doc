#!/usr/bin/env python3
"""
LLM Module for SmartDoc

Provides shared LLM provider abstractions and implementations
that can be used across discovery, intent classification, and
other AI-powered features in SmartDoc.
"""

from .providers import LLMProvider, OllamaProvider

__all__ = ["LLMProvider", "OllamaProvider"]
