"""
Discovery Processing Module

Handles progressive disclosure of clinical information based on intent classification.
"""

from .processor import LLMDiscoveryProcessor

__all__ = ["LLMDiscoveryProcessor"]

# Convenience alias
DiscoveryProcessor = LLMDiscoveryProcessor
