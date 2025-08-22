"""
Discovery Processing Module

Handles progressive disclosure of clinical information based on intent classification.
Provides LLM-based clinical discovery processing with configurable providers and prompts.
"""

from .processor import LLMDiscoveryProcessor
from .types import DiscoveryLLMIn, DiscoveryLLMOut

__all__ = ["LLMDiscoveryProcessor", "DiscoveryLLMIn", "DiscoveryLLMOut"]

# Convenience alias
DiscoveryProcessor = LLMDiscoveryProcessor
