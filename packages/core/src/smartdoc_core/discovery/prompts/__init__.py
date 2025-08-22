"""
Prompt builders for discovery processing

Exports available prompt builders for clinical discovery.
"""

from .base import PromptBuilder
from .default import DefaultDiscoveryPrompt

__all__ = ["PromptBuilder", "DefaultDiscoveryPrompt"]
