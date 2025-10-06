"""
System Configuration Routes

Handles system-wide configuration settings that can be controlled
from the admin panel, such as hiding bias warnings for research studies.
"""

from flask import Blueprint, request, jsonify
from typing import Dict, Any
import json
import os
from pathlib import Path

bp = Blueprint('config', __name__)

# Configuration file path
CONFIG_DIR = Path(__file__).resolve().parents[6] / "configs"
SYSTEM_CONFIG_FILE = CONFIG_DIR / "system_config.json"

def load_system_config() -> Dict[str, Any]:
    """Load system configuration from file."""
    try:
        if SYSTEM_CONFIG_FILE.exists():
            with open(SYSTEM_CONFIG_FILE, 'r') as f:
                return json.load(f)
        return {"hide_bias_warnings": False}  # Default configuration
    except Exception as e:
        print(f"Error loading system config: {e}")
        return {"hide_bias_warnings": False}

def save_system_config(config: Dict[str, Any]) -> None:
    """Save system configuration to file."""
    try:
        # Ensure config directory exists
        CONFIG_DIR.mkdir(exist_ok=True)

        with open(SYSTEM_CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"Error saving system config: {e}")
        raise

@bp.route('/admin/config', methods=['GET'])
def get_config():
    """Get current system configuration."""
    try:
        config = load_system_config()
        return jsonify(config)
    except Exception as e:
        return jsonify({"error": f"Failed to load configuration: {str(e)}"}), 500

@bp.route('/admin/config', methods=['POST'])
def update_config():
    """Update system configuration."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No configuration data provided"}), 400

        # Validate configuration keys
        valid_keys = {"hide_bias_warnings"}
        config = {}

        for key, value in data.items():
            if key in valid_keys:
                config[key] = value
            else:
                return jsonify({"error": f"Invalid configuration key: {key}"}), 400

        # Save configuration
        save_system_config(config)

        return jsonify({
            "message": "Configuration updated successfully",
            "config": config
        })

    except Exception as e:
        return jsonify({"error": f"Failed to update configuration: {str(e)}"}), 500

@bp.route('/config', methods=['GET'])
def get_public_config():
    """Get public configuration (for frontend to check settings)."""
    try:
        config = load_system_config()
        # Only return configuration that affects frontend behavior
        public_config = {
            "hide_bias_warnings": config.get("hide_bias_warnings", False)
        }
        return jsonify(public_config)
    except Exception as e:
        return jsonify({"error": f"Failed to load configuration: {str(e)}"}), 500
