#!/usr/bin/env python3
"""
SmartDoc - Main entry point

A hybrid AI system that combines rule-based dialogue management with Large Language Model
based natural language generation to create realistic virtual standardized patient interactions.

Usage:
    python main.py
"""

import sys
import os

# Add the project root to the Python path so we can import from smartdoc package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from smartdoc.web.app import app
from smartdoc.config.settings import config
from smartdoc.utils.logger import sys_logger

def main():
    """Main entry point for the SmartDoc application."""
    try:
        sys_logger.log_system("info", "Starting SmartDoc application...")
        sys_logger.log_system("info", f"Configuration: Flask running on {config.FLASK_HOST}:{config.FLASK_PORT}")
        sys_logger.log_system("info", f"Debug mode: {config.FLASK_DEBUG}")

        # Run the Flask application
        app.run(
            host=config.FLASK_HOST,
            port=config.FLASK_PORT,
            debug=config.FLASK_DEBUG
        )

    except Exception as e:
        sys_logger.log_system("critical", f"Failed to start SmartDoc application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
