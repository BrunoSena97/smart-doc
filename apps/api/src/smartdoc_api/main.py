#!/usr/bin/env python3
"""
SmartDoc API Development Server

A clean development runner for the SmartDoc API.
For production, use gunicorn or similar WSGI server.

Usage:
    python -m smartdoc_api.main
    
Environment Variables:
    FLASK_ENV: development/production
    FLASK_HOST: Server host (default: 0.0.0.0)
    FLASK_PORT: Server port (default: 8000)
"""

import os
from . import create_app


def main():
    """Main entry point for development server."""
    app = create_app()

    # Development server configuration
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", 8000))
    debug = os.getenv("FLASK_ENV", "development") == "development"

    print(f"🚀 Starting SmartDoc API server on http://{host}:{port}")
    print(f"📊 Debug mode: {debug}")
    print(f"🏥 Health check: http://{host}:{port}/health")
    print(f"💬 Chat API: http://{host}:{port}/api/v1/chat")
    print(f"🔬 Simulation API: http://{host}:{port}/api/v1/simulation/start")
    print(
        f"🔄 Legacy routes: http://{host}:{port}/get_bot_response (for existing frontend)"
    )

    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    main()
