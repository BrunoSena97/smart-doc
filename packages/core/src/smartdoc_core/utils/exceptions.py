# exceptions.py - Custom exception classes for SmartDoc
"""
Custom exceptions for SmartDoc system to provide better error handling
and debugging capabilities.
"""


class SmartDocError(Exception):
    """Base exception class for all SmartDoc errors."""

    pass


class KnowledgeBaseError(SmartDocError):
    """Raised when knowledge base operations fail."""

    pass


class NLUError(SmartDocError):
    """Raised when Natural Language Understanding operations fail."""

    pass


class NLGError(SmartDocError):
    """Raised when Natural Language Generation operations fail."""

    pass


class DialogueManagerError(SmartDocError):
    """Raised when dialogue management operations fail."""

    pass


class OllamaConnectionError(NLGError):
    """Raised when connection to Ollama server fails."""

    pass


class OllamaModelError(NLGError):
    """Raised when Ollama model operations fail."""

    pass


class SBERTModelError(NLUError):
    """Raised when SBERT model operations fail."""

    pass


class ConfigurationError(SmartDocError):
    """Raised when configuration is invalid."""

    pass


class SessionError(SmartDocError):
    """Raised when session management fails."""

    pass


class LoggingError(SmartDocError):
    """Raised when logging operations fail."""

    pass
