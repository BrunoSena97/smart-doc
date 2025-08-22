#!/usr/bin/env python3
"""
Discovery Providers Package (Deprecated)

This module provides backward compatibility for existing imports.
Please use smartdoc_core.llm.providers instead.
"""

import warnings

# Issue deprecation warning once per import
warnings.warn(
    "Importing providers from discovery is deprecated; use smartdoc_core.llm.providers instead.",
    DeprecationWarning,
    stacklevel=2
)

# Temporary compatibility re-export (will be removed in future version)
from smartdoc_core.llm.providers import LLMProvider, OllamaProvider  # noqa: F401

__all__ = ["LLMProvider", "OllamaProvider"]
