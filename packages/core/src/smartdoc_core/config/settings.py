# config.py - Unified YAML-based configuration management for SmartDoc
import os
import yaml
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class SmartDocConfig:
    """
    Unified configuration for SmartDoc system using YAML configs.
    Falls back to defaults if YAML config is not available.
    """

    # Case Data Configuration
    case_file: str = "data/raw/cases/intent_driven_case.json"

    # LLM Configuration (Ollama)
    ollama_base_url: str = "http://172.19.0.1:11434"
    ollama_model: str = "gemma3:4b-it-q4_K_M"

    @classmethod
    def from_yaml(cls, config_name: Optional[str] = None) -> "SmartDocConfig":
        """Create configuration from YAML files with fallbacks."""
        config_name = config_name or os.getenv("SMARTDOC_ENV", "dev")

        # Navigate to repo root to find configs directory
        # From packages/core/src/smartdoc_core/config/settings.py -> repo root
        current_dir = os.path.dirname(__file__)
        repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))))
        config_path = os.path.join(repo_root, "configs", f"{config_name}.yaml")

        # Load default config first
        default_config_path = os.path.join(repo_root, "configs", "default.yaml")
        config_data = {}

        try:
            with open(default_config_path, "r") as f:
                config_data = yaml.safe_load(f) or {}
        except FileNotFoundError:
            print(f"Warning: Default config {default_config_path} not found")

        # Override with environment-specific config
        if config_name != "default":
            try:
                with open(config_path, "r") as f:
                    env_config = yaml.safe_load(f) or {}
                    # Deep merge configs
                    config_data = cls._deep_merge(config_data, env_config)
            except FileNotFoundError:
                print(f"Warning: Config file {config_path} not found, using defaults")

        # Extract values with fallbacks
        case_file = "data/raw/cases/intent_driven_case.json"
        if "data" in config_data and "cases_path" in config_data["data"]:
            case_file = os.path.join(config_data["data"]["cases_path"], "intent_driven_case.json")

        ollama_base_url = "http://172.19.0.1:11434"
        ollama_model = "gemma3:4b-it-q4_K_M"
        if "ollama" in config_data:
            ollama_base_url = config_data["ollama"].get("base_url", ollama_base_url)
            ollama_model = config_data["ollama"].get("model", ollama_model)

        return cls(
            case_file=case_file,
            ollama_base_url=ollama_base_url,
            ollama_model=ollama_model,
        )

    @classmethod
    def from_env(cls) -> "SmartDocConfig":
        """Create configuration from environment variables with YAML fallbacks."""
        # First load from YAML
        config = cls.from_yaml()

        # Override with environment variables if present
        config.case_file = os.getenv("SMARTDOC_CASE_FILE", config.case_file)
        config.ollama_base_url = os.getenv("SMARTDOC_OLLAMA_BASE_URL", config.ollama_base_url)
        config.ollama_model = os.getenv("SMARTDOC_OLLAMA_MODEL", config.ollama_model)

        return config

    @staticmethod
    def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two dictionaries."""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = SmartDocConfig._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    def validate(self) -> bool:
        """Validate configuration values."""
        errors = []

        if not self.case_file:
            errors.append("case_file cannot be empty")

        if not self.ollama_base_url:
            errors.append("ollama_base_url cannot be empty")

        if not self.ollama_model:
            errors.append("ollama_model cannot be empty")

        if errors:
            raise ValueError(f"Configuration validation failed: {'; '.join(errors)}")

        return True

    def update_ollama_settings(self, base_url: str, model: str) -> bool:
        """Update Ollama-related settings dynamically."""
        try:
            # Validate inputs
            if not base_url or not model:
                raise ValueError("Base URL and model are required")

            # Update the settings
            self.ollama_base_url = base_url
            self.ollama_model = model

            return True
        except Exception as e:
            raise ValueError(f"Failed to update settings: {e}")

    def get_ollama_settings(self) -> dict:
        """Get current Ollama settings as a dictionary."""
        return {
            "base_url": self.ollama_base_url,
            "model": self.ollama_model,
        }

    # Legacy property accessors for backward compatibility
    @property
    def CASE_FILE(self) -> str:
        return self.case_file

    @property
    def OLLAMA_BASE_URL(self) -> str:
        return self.ollama_base_url

    @property
    def OLLAMA_MODEL(self) -> str:
        return self.ollama_model


# Global configuration instance
config = SmartDocConfig.from_env()

# Validate configuration on import
try:
    config.validate()
except ValueError as e:
    print(f"Configuration Error: {e}")
    print("Please check your YAML config files or environment variables.")
    raise
